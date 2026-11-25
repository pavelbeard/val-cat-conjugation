# Conjugador val-cat-conjugation (refactor)

> **Plan de refactorización por fases y módulo a módulo: ver [REFACTOR-PLAN.md](REFACTOR-PLAN.md).**

Monorepo con dos apps nuevas:

- **apps/frontend** — SPA con **TanStack Router + Vite + React**. 100% estática, desplegable en Netlify/GH Pages.
- **apps/api** — API **Express + Mongoose** que sirve los verbos desde MongoDB (Netlify + Atlas). Expone `/api/verbs/search` (búsqueda **paginada** → `{ data, metadata }`), `/api/verbs/:infinitive` y un CRUD en `/api/admin` para el panel de administración.

Las apps antiguas (`apps/frontend`, `apps/backend`) **fueron eliminadas** tras el refactor; su información (uso de IA y fetch de recursos externos) quedó resumida en [LEGACY-IA.md](LEGACY-IA.md) y [LEGACY-FETCH-VERBS.md](LEGACY-FETCH-VERBS.md), y el código original sigue en el historial de git.

## Entorno de desarrollo con Docker (recomendado)

`docker-compose.yml` (raíz) encapsula los tres servicios de las apps nuevas:

| Servicio | Imagen/base | Puerto host | Notas |
| --- | --- | --- | --- |
| `mongo` | `mongo:7` | 27017 | Volumen `mongo-data`, healthcheck `ping` |
| `api` | `apps/api/Dockerfile` (node:24-alpine + pnpm) | 3001 | `MONGODB_URI=mongodb://mongo:27017/conjugador` |
| `web` | `apps/frontend/Dockerfile` (node:24-alpine + pnpm) | 5173 | Vite con `--host 0.0.0.0`, proxy `/api` → `http://api:3001` |
| `mongo-express` | `mongo-express` (perfil `tools`) | 8081 | GUI opcional de MongoDB |
| `dozzle` | `amir20/dozzle` (perfil `tools`) | 8080 (solo `127.0.0.1`) | Logs de contenedores con login obligatorio; volumen `dozzle-data` en `/data` |

En dev, el repo se monta como volumen sobre `/app` (los `node_modules` quedan en volúmenes anónimos de la imagen), así que los cambios en `apps/frontend` y `apps/api` se reflejan con hot reload sin reconstruir.

```
docker compose up --build                      # levantar mongo + api + web
docker compose run --rm api pnpm import:dump    # seed inicial desde dump/verbs/verbs.bson
docker compose --profile tools up -d            # dozzle en http://localhost:8080 + mongo-express en :8081
docker compose logs -f web                      # logs
docker compose down                             # parar (añade -v para borrar el volumen de Mongo)
```

O con los scripts del package.json raíz: `pnpm docker:up`, `pnpm docker:seed`, `pnpm docker:down`, `pnpm docker:logs`.

URLs: web en http://localhost:5173, API en http://localhost:3001 (`/api/health`), Mongo en `mongodb://localhost:27017/conjugador`, Dozzle en http://127.0.0.1:8080, mongo-express en http://localhost:8081 (ambos con `--profile tools`).

**Dozzle va cerrado:** solo publica `127.0.0.1:8080` y exige login (`DOZZLE_AUTH_PROVIDER: simple`). Los usuarios viven en `/data/users.yml` dentro del volumen `dozzle-data` (persistente, modo 600), así que nadie accede sin credenciales y la configuración no se pierde al recrear el contenedor. Usuario: `admin`. Para rotar la contraseña: genera un hash bcrypt con cualquier herramienta (formato `$2b$12$…`), actualiza `users.yml` en el volumen `dozzle-data` y `docker compose --profile tools restart dozzle`.

## Arquitectura de apps/api (por capas)

```
apps/api/src/
  server.ts               # entry: dotenv + connectMongo + listen
  app.ts                  # express app (exportada para tests con supertest)
  errors.ts               # HttpError / NotFoundError / BadRequestError
  db/mongoose.ts          # wrapper de Mongoose (connectMongo, disconnectMongo, withTransaction)
  middlewares/
    index.ts              # exporta mw (default): mw.validator(...) / mw.controller(...)
    controller.ts         # mw.controller(fn, {status?}): ejecuta el método, envía la respuesta y los errores
    response.ts           # respuestas centralizadas: sendOk / sendCreated / sendNoContent
    error-handler.ts      # notFoundHandler (404 global) + errorHandler (HttpError, 11000→409, ValidationError→400, 500)
  validator/              # wrapper de zod (DSL) para validadores
    dsl.ts                # objeto `validator` (string/number/bool/... con .required()/.notRequired()/.default(v) y shorthands stringRequired…), FieldBuilder, buildRequestSchema
    request.ts            # validateRequest (parsea {params,query,body} y devuelve datos), formatIssues, isSchema, tipos Validator
    index.ts              # re-exports + middleware validatorMw (expuesto como mw.validator)
  models/verb.ts          # modelo Mongoose
  verbs/
    verbs.router.ts       # mw.validator(validator.x) -> mw.controller(controller.x)
    verbs.controller.ts   # métodos async que DEVUELVEN el resultado
    verbs.validator.ts    # schemas zod, uno por método del controller (400 si falla)
    verbs.bll.ts          # lógica de negocio (inyección del repository)
    verbs.repository.ts   # acceso a BBDD (todas las queries Mongoose)
  admin/                  # misma estructura (CRUD)
```

**Patrón de middlewares** (en cada router):

```ts
import mw from '../middlewares/index.js'

router.get('/', mw.validator(verbsValidator.list), mw.controller(verbsController.list))
router.post('/verbs', mw.validator(adminValidator.create), mw.controller(adminController.create, { status: 201 }))
```

- `mw.validator(validator.x)`: valida el request antes del controller. Los validadores (`*.validator.ts`) son **descriptores DSL** (uno por método; `undefined` = sin validación, p. ej. `list`):

```ts
import { validator } from '../validator/index.js'

const search = {
  query: {
    form: validator.string.required(),
    verbose: validator.bool.notRequired().default(false),
  },
  params: { id: validator.stringRequired },
}

export const verbsValidator = { list: undefined, search, get }
```

`mw.validator` convierte el descriptor a zod (`buildRequestSchema`) y valida `{ params, query, body }`; si falla, lanza 400 con el detalle de los issues (`query.form: query param "form" is required`). Tipos: `string` (required = no vacío, con trim), `number` (coerce, para query strings), `bool` (acepta `true`/`"true"`), `array`, `object`; `.required()` / `.notRequired()` / `.default(v)` y shorthands `stringRequired`, `stringOptional`, etc.
- `mw.controller(controller.x, opts)`: ejecuta el método del controller, que es `async` y **devuelve** el resultado; el middleware envía la respuesta (`undefined` → 204, `opts.status` → p. ej. 201, si no 200 JSON) y manda cualquier error a `errorHandler`. Con `opts.pagination: true` el método devuelve `{ data, total }` y el middleware responde `{ data, metadata: { total, limit, skip, page, totalPages } }` (calculando `skip` desde `page`/`limit` del query validado).

**Búsqueda paginada de verbs** (nunca se cargan todos): `GET /api/verbs/search?q=&form=&letter=&sort=&page=&limit=&skip=` → `{ data: Verb[], metadata }`. El frontal (`/verbs?page=N`) consume solo esta ruta; el list-all `/api/verbs` está eliminado (404).


Convención de nombres: `*.router` (rutas), `*.controller` (métodos de controller),
`*.bll` (lógica de negocio), `*.repository` (acceso a BBDD). El wrapper de Mongoose
vive solo en `db/mongoose.ts`.

**Errores y respuestas centralizadas** en `src/middlewares/`: los routers montan la
cadena `middlewares -> controller` (`asyncHandler` envuelve cada método del controller,
así que ya no hay try/catch en los controllers), las respuestas usan `sendOk` /
`sendCreated` / `sendNoContent`, la validación de payload es un middleware (`validate`)
y todo error cae en `errorHandler` (ruta desconocida → 404 vía `notFoundHandler`,
`HttpError` → su status, clave duplicada de Mongo → 409, `ValidationError` → 400,
resto → 500).

## Tests

Los tests de la API pegan a un Mongo real (base de datos `conjugador_test`) y se
lanzan dentro de Docker:

```
pnpm run dockertest     # docker compose run api contra mongodb://mongo:27017/conjugador_test
pnpm --filter @vcc/api test   # en local, contra el Mongo publicado en localhost:27017
```

## Puesta en marcha local (sin Docker)

```
pnpm install
pnpm --filter @vcc/api dev       # API en :3001 (necesita apps/api/.env con MONGODB_URI)
pnpm --filter @vcc/api import:dump  # importar dump/verbs/verbs.bson a Mongo
pnpm --filter @vcc/frontend dev       # SPA en :5173 con proxy /api -> :3001
```
