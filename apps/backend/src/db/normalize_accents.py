def normalize(txt: str) -> str:
    import unicodedata

    if not txt:
        return txt
    return unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("utf-8")

