from utils.fetch import Fetch


async def get_full_untranslated_conjugation(checked_verb: str):
    response = await Fetch(
        f"https://www.softcatala.org/conjugador-de-verbs/verb/{checked_verb.replace('-se', '').replace("-se'n", '')}",
    ).get()

    return response.text


async def get_infinitive_translation_from_diccionari_cat(verb: str) -> str:
    url = f"https://www.diccionari.cat/cerca/diccionari-catala-castella?search_api_fulltext_cust={verb}&search_api_fulltext_cust_1=&field_faceta_cerca_1=All&show=title"

    response = await Fetch(url).get()
    return response.text
