# Legacy — uso de IA (resumen antes del borrado)

Dónde vivía la IA en el código legacy (`apps/frontend` Next.js + `apps/backend`, ambos eliminados; ver git history).
La app nueva (`apps/web` + `apps/api`) no usa IA todavía; el plan (REFACTOR-PLAN.md, Fase 2)
prevé un proveedor con sesión propia (Mistral) para auto-relleno de conjugaciones.

## Flujo completo (auto-relleno de un verbo sin datos)

1. El frontend detecta un verbo sin `moods` y dispara la traducción/creación.
2. Llama al backend legacy `POST /api/v1/verbs` con el infinitivo (normalizado sin acentos).
3. El backend descarga la conjugación de Softcatalà (ver LEGACY-FETCH-VERBS.md), la parsea
   con BeautifulSoup y se la pasa a la IA para que genere la estructura completa y la
   traduzca al castellano forma a forma.
4. El resultado se guarda en Mongo y vuelve al frontend, que lo cachea en react-query.

## Frontend (apps/frontend)

- `lib/hooks/use-verb-translate.ts` — hook `useVerbTranslate({ verb })`: si `verb.moods` está
  vacío, ejecuta la mutación `translateVerb(verb.infinitive)` (react-query) y vuelca el resultado
  en la query cache (`verbsQueryKeys.getVerbByInfinitive`). Expõe `isTranslating` / `isError`.
- `actions/verbs.ts` — server action `translateVerb`: `_normalizeForm` (NFKD, quita diacríticos)
  + `ApiClient.post(createUrl("verbs"), { infinitive })` contra `BACKEND_URL` (`lib/constants.ts`,
  `NEXT_PUBLIC_BACKEND_URL || http://localhost:8000/api/v1`).
- `app/(main)/verbs/[infinitive]/client.tsx` — muestra `VerbTableLoading` mientras `isTranslating`
  y un footer con disclaimer: "Advertencia: traducciones están creadas por un modelo de IA y pueden
  no ser precisas" + enlaces a Softcatalà y Diccionari.cat.

## Backend (apps/backend)

- `src/utils/ai/ai_handler.py` — ABC `AIHandler` + `AIHandlerEnum` (solo `GEMINI`).
- `src/utils/ai/handlers.py` — `PydanticGeminiHandler` (pydantic_ai) con `query_api(messages, response_type=...)`.
- `src/utils/ai/clients.py` — factory `ai_handler_factory` + clientes:
  - `translation_client_gemini()` — modelo `gemini-2.5-flash`, `max_tokens=8192`,
    `temperature=0.5`, `top_p=0.95`, `thinking_budget=0`, respuesta tipada `AI__VerbOutput`.
  - `detection_client_gemini()` — modelo `gemini-2.5-flash-lite` para detección.
- `src/utils/ai/prompts.py` — `get_system_prompt(path)` lee el system prompt de un `.txt`.
- Prompts en `src/utils/prompts/verbs/`:
  - `gemini-2.5-flash-conjugador.txt` — pide la conjugación completa con modos/tiempos fijos
    (indicatiu: present, perfet, imperfet, plusquamperfet, passat_simple, passat_perifrastic,
    passat_anterior, passat_anterior_perifrastic, futur, futur_perfet, condicional,
    condicional_perfet; subjuntiu; imperatiu afirmativa/negativa; formes no personals).
  - `gemini-2.5-flash-translator.txt` — traducción al castellano por forma.
  - `gemini-2.5-flash-lite-detector.txt` — detección de verbo/reflexivo.
- `src/core/config.py` — claves: `AI_SECRET_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`,
  `OLLAMA_API_KEY`, `AI_MODEL` (default en `core/constants.py`), `OPENAI_MODEL`, etc.
- `src/schemas/verbs.py` — modelos pydantic de salida IA: `AI__VerbOutput`, `AI__ResponseIdentifiedVerb`.
- `src/v1/endpoints/verbs.py` — `POST /verbs` inyecta `translation_client_gemini` y
  `diccionari_parser` y llama a `verbs_service.create_verb(...)`.
- Tests: `src/tests/mocks/ai.py`, `src/tests/integration/test_int_verbs_gemini.py`
  (httpx ASGITransport), fixtures `src/tests/fixtures/*-gemini.json`, `*-translated.json`.

## Notas para la nueva arquitectura

- El disclaimer de "traducciones por IA" ya está portado a `apps/web` (footer de
  `verb-detail.tsx`).
- En la app nueva la IA irá por un endpoint propio de `apps/api` con proveedor intercambiable
  (Mistral primero), no como server action del frontend.
