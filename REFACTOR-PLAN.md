# Plan de refactorización — apps/web (React SPA)

Objetivo: llevar `apps/web` (Vite + React + TanStack Router) al nivel visual y
funcional de la app demo (la app Next.js existente en `apps/frontend`), **módulo
a módulo y paso a paso**, sin tocar el código legacy salvo como referencia de
estilos. La IA entra de otra manera: con sesión propia en un proveedor (Mistral
por ahora) para auto-relleno de conjugaciones, probablemente después de tener
gestión de usuarios.

> Nota: el canvas React "conjugador-valencia" de sesiones anteriores no está
> persistido en disco; la fuente de estilos de referencia es el look de
> `apps/frontend` (Tailwind v4 + shadcn, tema zinc, variables oklch en
> `app/globals.css`).

## Fase 0 — Base de estilos (demo → web)

- [x] Decidir stack de estilos de `apps/web`: Tailwind v4 (`@tailwindcss/vite`)
      con el mismo tema de la demo (base zinc, `--radius`, modo oscuro), para
      paridad con los componentes shadcn. Alternativa: CSS plano con las mismas
      variables.
- [x] Portar los tokens del tema: variables oklch de `apps/frontend/app/globals.css`
      → hoja de estilos de `apps/web`.
- [x] Crear `apps/web/src/components/ui/` con los equivalentes a los de la demo:
      `button`, `input`, `card`, `table`, `tabs`, `scroll-area`.
- [x] Verificar: `pnpm --filter @vcc/web typecheck && pnpm --filter @vcc/web build`
      y revisión visual con `docker compose up` (web en :5173).

## Fase 1 — Módulos, uno por paso (cada paso = un commit pequeño y verificable)

- [x] **Paso 1 — Layout global**: header/nav/footer en `src/routes/__root.tsx`
      con los estilos de la demo. (Hoy el nav enlaza a `/translator` y `/settings`
      y rompe el typecheck; se arregla al crear esas rutas.)
- [x] **Paso 2 — Lista de verbos + buscador** (`/verbs`): portar `verbs-search`,
      lista con letras y búsqueda por forma (`GET /api/verbs/search?form=`).
- [x] **Paso 3 — Detalle de verbo** (`/verbs/$verb`): tabs por modo, tabla por
      tiempo, columna bilingüe (formas en valencià + traducción por forma).
- [x] **Paso 4 — Página `/translator`** (existe en la demo, falta en web).
- [x] **Paso 5 — Página `/settings`** (tema, idioma, etc.; existe en la demo).
- [x] **Paso 6 — PWA**: manifest + service worker para desplegar en Netlify/GH
      Pages y poder instalarla en el iPhone (sin App Store por ahora).

Regla de cada paso: `typecheck` + `build` + verificación visual en Docker antes
de pasar al siguiente. Nada de refactor masivo de golpe.

## Fase 2 — Datos, usuarios e IA (en otro orden que antes)

- [x] Motor de conjugación por reglas (terminaciones por grupo: `-ar`,
      `-re/-er`, `-ir` incoativo) + listas de overrides para irregulares
      (ser, estar, anar, fer, venir, poder, córrer…), con motor paralelo en
      castellano. Dataset JSON estático (~300 irregulares) como fuente de verdad.
- [ ] **Gestión de usuarios primero** (si procede): auth en `/api/admin`
      (hay un TODO en `apps/api/src/routes/admin.ts`) antes de exponer la IA.
- [ ] **Proveedor de IA con sesión propia** (Mistral por ahora) para
      auto-relleno de conjugaciones: abstracción `AIProvider` con implementación
      Mistral, endpoint dedicado en `apps/api` y revisión humana de lo generado.
      No se usa todavía: primero datos estáticos + usuarios.

## Reglas de trabajo

- Legacy intocable: `apps/frontend` y `apps/backend` solo se leen como referencia.
- Código nuevo solo en `apps/web` y `apps/api`.
- Entorno Docker: `docker compose up` (mongo :27017, api :3001, web :5173),
  seed con `docker compose run --rm api pnpm import:dump`, logs en Dozzle
  (http://127.0.0.1:8080, con login) vía `docker compose --profile tools up -d`.
