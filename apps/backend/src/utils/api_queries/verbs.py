from utils.fetch import Fetch


async def get_full_untranslated_conjugation(checked_verb: str):
    response = await Fetch(
        f"https://www.softcatala.org/conjugador-de-verbs/verb/{checked_verb.replace('-se', '').replace("-se'n", '')}",
    ).get()

    return response.text


async def get_infinitive_translation_from_diccionari_cat(verb: str) -> str:
    def neutralizar_acentos(texto: str) -> str:
        reemplazos = {
            "à": "a",
            "á": "a",
            "è": "e",
            "é": "e",
            "í": "i",
            "ì": "i",
            "ò": "o",
            "ó": "o",
            "ù": "u",
            "ú": "u",
            "À": "A",
            "Á": "A",
            "È": "E",
            "É": "E",
            "Ì": "I",
            "Í": "I",
            "Ò": "O",
            "Ó": "O",
            "Ù": "U",
            "Ú": "U",
        }

        return "".join(reemplazos.get(c, c) for c in texto)

    normalized_verb = neutralizar_acentos(verb).lower()

    url = f"https://www.diccionari.cat/cerca/diccionari-catala-castella?search_api_fulltext_cust={normalized_verb}&search_api_fulltext_cust_1=&field_faceta_cerca_1=All&show=title"

    response = await Fetch(url).get()
    return response.text
