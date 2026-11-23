# Legacy — fetch de verbos desde recursos externos (resumen antes del borrado)

De dónde salían los datos de conjugación en el código legacy (`apps/backend`, eliminado; ver git history).
La app nueva (`apps/api`) importa los datos ya volcados en `dump/verbs/verbs.bson`
(vía `pnpm --filter @vcc/api import:dump`); no hace scraping en runtime.

## Recursos externos usados

- **Softcatalà** — conjugador de verbos:
  `https://www.softcatala.org/conjugador-de-verbs/verb/{verbo}`
  (se quita `-se` / `-se'n` del infinitivo antes de la URL).
- **Diccionari.cat** — traducción infinitivo cat→cast:
  `https://www.diccionari.cat/cerca/diccionari-catala-castella?search_api_fulltext_cust={verbo}`
  con normalización previa de acentos (à→a, ç→c, ·→, ŀ→l, …) en `neutralizar_acentos`.

## Código legacy involucrado

- `src/utils/fetch.py` — clase `Fetch(url)` con `httpx.AsyncClient(follow_redirects=True)`;
  404 → `AppException(NOT_FOUND)`, 500 → `AppException(INTERNAL_SERVER_ERROR)`, 200 → response.
- `src/utils/api_queries/verbs.py` —
  - `get_full_untranslated_conjugation(checked_verb)` → HTML de Softcatalà.
  - `get_infinitive_translation_from_diccionari_cat(verb)` → HTML de Diccionari.cat.
- `src/utils/parsers/parser.py` + `src/utils/parsers/handlers.py` — parsing con
  BeautifulSoup/lxml: `VerbUntranslatedTable` recorre las tablas `<tr>` de Softcatalà y
  construye `Database__MoodBlock` / `TenseBlock` / `ConjugatedForm`, con `variation_types`
  (`None` = central, o `cent.` / `val.` / `bal.` desde `<span class="variant">`);
  `diccionari_parser` extrae la traducción del HTML de Diccionari.cat.
- `src/utils/verbs.py` — helpers BeautifulSoup + `add_reflexive_prefix` (repone `-se`/`-se'n`).
- `src/db/seed_db.py` — seed masivo recorriendo letras A–Z.
- `src/v1/endpoints/verbs.py` — `POST /verbs` orquesta fetch + parse + IA (ver LEGACY-IA.md);
  `GET /verbs` (búsqueda por form/letra), `PATCH` (incrementa `clicks`), `DELETE`.
- Frontend: `apps/frontend/lib/utils/api-client.ts` (`ApiClient` sobre `BACKEND_URL`),
  `actions/verbs.ts`, y enlaces de referencia en `app/(main)/verbs/[infinitive]/client.tsx`
  a Softcatalà y Diccionari.cat (portados al footer de `apps/web`).
- Tests: `src/tests/verbs/test_verbs_utils.py` (BeautifulSoup sobre fixtures HTML),
  `src/tests/integration/test_int_verbs_database.py`, fixture `src/tests/fixtures/prettified_anar.html`.

## Datos resultantes

- `dump/verbs/verbs.bson` — dump de Mongo con todos los verbos ya scrapeados/traducidos
  (unos 8000 documentos). Es la fuente que `apps/api` importa con `import:dump`.
  **No borrar `dump/`.**
