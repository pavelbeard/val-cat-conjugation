import datetime
from schemas.verbs import (
    AI__ConjugatedForm,
    AI__MoodBlock,
    AI__TenseBlock,
    AI__VerbOutput,
    Database__ConjugatedForm,
    Database__MoodBlock,
    Database__TenseBlock,
    Fetch__VerbCreated,
)


test_parlar_original = Fetch__VerbCreated(
    infinitive="parlar",
    normalized_infinitive="parlar",
    translation="hablar",
    moods=[
        Database__MoodBlock(
            mood="indicatiu",
            tenses=[
                Database__TenseBlock(
                    tense="present",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["parlo", "parle", "parl"],
                            normalized_forms=["parlo", "parle", "parl"],
                            variation_types=["(cent.)", "(val.)", "(bal.)"],
                            translation="parlo",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["parles"],
                            normalized_forms=["parles"],
                            variation_types=None,
                            translation="parles",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["parla"],
                            normalized_forms=["parla"],
                            variation_types=None,
                            translation="parla",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["parlem", "parlam"],
                            normalized_forms=["parlem", "parlam"],
                            variation_types=[None, "(bal.)"],
                            translation="parlem",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["parleu", "parlau"],
                            normalized_forms=["parleu", "parlau"],
                            variation_types=[None, "(bal.)"],
                            translation="parleu",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["parlen"],
                            normalized_forms=["parlen"],
                            variation_types=None,
                            translation="parlen",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="perfet",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["he parlat"],
                            normalized_forms=["he parlat"],
                            variation_types=None,
                            translation="he parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["has parlat"],
                            normalized_forms=["has parlat"],
                            variation_types=None,
                            translation="has parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["ha parlat"],
                            normalized_forms=["ha parlat"],
                            variation_types=None,
                            translation="ha parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["hem parlat"],
                            normalized_forms=["hem parlat"],
                            variation_types=None,
                            translation="hem parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["heu parlat"],
                            normalized_forms=["heu parlat"],
                            variation_types=None,
                            translation="heu parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["han parlat"],
                            normalized_forms=["han parlat"],
                            variation_types=None,
                            translation="han parlat",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="imperfet",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["parlava"],
                            normalized_forms=["parlava"],
                            variation_types=None,
                            translation="parlava",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["parlaves"],
                            normalized_forms=["parlaves"],
                            variation_types=None,
                            translation="parlaves",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["parlava"],
                            normalized_forms=["parlava"],
                            variation_types=None,
                            translation="parlava",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["parlàvem"],
                            normalized_forms=["parlavem"],
                            variation_types=None,
                            translation="parlàvem",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["parlàveu"],
                            normalized_forms=["parlaveu"],
                            variation_types=None,
                            translation="parlàveu",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["parlaven"],
                            normalized_forms=["parlaven"],
                            variation_types=None,
                            translation="parlaven",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="plusquamperfet",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["havia parlat"],
                            normalized_forms=["havia parlat"],
                            variation_types=None,
                            translation="havia parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["havies parlat"],
                            normalized_forms=["havies parlat"],
                            variation_types=None,
                            translation="havies parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["havia parlat"],
                            normalized_forms=["havia parlat"],
                            variation_types=None,
                            translation="havia parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["havíem parlat"],
                            normalized_forms=["haviem parlat"],
                            variation_types=None,
                            translation="havíem parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["havíeu parlat"],
                            normalized_forms=["havieu parlat"],
                            variation_types=None,
                            translation="havíeu parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["havien parlat"],
                            normalized_forms=["havien parlat"],
                            variation_types=None,
                            translation="havien parlat",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="passat_simple",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["parlí"],
                            normalized_forms=["parli"],
                            variation_types=None,
                            translation="parlí",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["parlares"],
                            normalized_forms=["parlares"],
                            variation_types=None,
                            translation="parlares",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["parlà"],
                            normalized_forms=["parla"],
                            variation_types=None,
                            translation="parlà",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["parlàrem"],
                            normalized_forms=["parlarem"],
                            variation_types=None,
                            translation="parlàrem",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["parlàreu"],
                            normalized_forms=["parlareu"],
                            variation_types=None,
                            translation="parlàreu",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["parlaren"],
                            normalized_forms=["parlaren"],
                            variation_types=None,
                            translation="parlaren",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="passat_perifràstic",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["vaig parlar"],
                            normalized_forms=["vaig parlar"],
                            variation_types=None,
                            translation="vaig parlar",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["vas (vares) parlar"],
                            normalized_forms=["vas (vares) parlar"],
                            variation_types=None,
                            translation="vas (vares) parlar",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["va parlar"],
                            normalized_forms=["va parlar"],
                            variation_types=None,
                            translation="va parlar",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["vam (vàrem) parlar"],
                            normalized_forms=["vam (varem) parlar"],
                            variation_types=None,
                            translation="vam (vàrem) parlar",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["vau (vàreu) parlar"],
                            normalized_forms=["vau (vareu) parlar"],
                            variation_types=None,
                            translation="vau (vàreu) parlar",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["van (varen) parlar"],
                            normalized_forms=["van (varen) parlar"],
                            variation_types=None,
                            translation="van (varen) parlar",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="passat_anterior",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["haguí parlat"],
                            normalized_forms=["hagui parlat"],
                            variation_types=None,
                            translation="haguí parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["hagueres parlat"],
                            normalized_forms=["hagueres parlat"],
                            variation_types=None,
                            translation="hagueres parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["hagué parlat"],
                            normalized_forms=["hague parlat"],
                            variation_types=None,
                            translation="hagué parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["haguérem parlat"],
                            normalized_forms=["haguerem parlat"],
                            variation_types=None,
                            translation="haguérem parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["haguéreu parlat"],
                            normalized_forms=["haguereu parlat"],
                            variation_types=None,
                            translation="haguéreu parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["hagueren parlat"],
                            normalized_forms=["hagueren parlat"],
                            variation_types=None,
                            translation="hagueren parlat",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="passat_anterior_perifràstic",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["vaig haver parlat"],
                            normalized_forms=["vaig haver parlat"],
                            variation_types=None,
                            translation="vaig haver parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["vas haver parlat"],
                            normalized_forms=["vas haver parlat"],
                            variation_types=None,
                            translation="vas haver parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["va haver parlat"],
                            normalized_forms=["va haver parlat"],
                            variation_types=None,
                            translation="va haver parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["vam haver parlat"],
                            normalized_forms=["vam haver parlat"],
                            variation_types=None,
                            translation="vam haver parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["vau haver parlat"],
                            normalized_forms=["vau haver parlat"],
                            variation_types=None,
                            translation="vau haver parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["van haver parlat"],
                            normalized_forms=["van haver parlat"],
                            variation_types=None,
                            translation="van haver parlat",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="futur",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["parlaré"],
                            normalized_forms=["parlare"],
                            variation_types=None,
                            translation="parlaré",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["parlaràs"],
                            normalized_forms=["parlaras"],
                            variation_types=None,
                            translation="parlaràs",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["parlarà"],
                            normalized_forms=["parlara"],
                            variation_types=None,
                            translation="parlarà",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["parlarem"],
                            normalized_forms=["parlarem"],
                            variation_types=None,
                            translation="parlarem",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["parlareu"],
                            normalized_forms=["parlareu"],
                            variation_types=None,
                            translation="parlareu",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["parlaran"],
                            normalized_forms=["parlaran"],
                            variation_types=None,
                            translation="parlaran",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="futur_perfet",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["hauré parlat"],
                            normalized_forms=["haure parlat"],
                            variation_types=None,
                            translation="hauré parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["hauràs parlat"],
                            normalized_forms=["hauras parlat"],
                            variation_types=None,
                            translation="hauràs parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["haurà parlat"],
                            normalized_forms=["haura parlat"],
                            variation_types=None,
                            translation="haurà parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["haurem parlat"],
                            normalized_forms=["haurem parlat"],
                            variation_types=None,
                            translation="haurem parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["haureu parlat"],
                            normalized_forms=["haureu parlat"],
                            variation_types=None,
                            translation="haureu parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["hauran parlat"],
                            normalized_forms=["hauran parlat"],
                            variation_types=None,
                            translation="hauran parlat",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="condicional",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["parlaria"],
                            normalized_forms=["parlaria"],
                            variation_types=None,
                            translation="parlaria",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["parlaries"],
                            normalized_forms=["parlaries"],
                            variation_types=None,
                            translation="parlaries",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["parlaria"],
                            normalized_forms=["parlaria"],
                            variation_types=None,
                            translation="parlaria",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["parlaríem"],
                            normalized_forms=["parlariem"],
                            variation_types=None,
                            translation="parlaríem",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["parlaríeu"],
                            normalized_forms=["parlarieu"],
                            variation_types=None,
                            translation="parlaríeu",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["parlarien"],
                            normalized_forms=["parlarien"],
                            variation_types=None,
                            translation="parlarien",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="condicional_perfet",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["hauria (haguera) parlat"],
                            normalized_forms=["hauria (haguera) parlat"],
                            variation_types=None,
                            translation="hauria (haguera) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["hauries (hagueres) parlat"],
                            normalized_forms=["hauries (hagueres) parlat"],
                            variation_types=None,
                            translation="hauries (hagueres) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["hauria (haguera) parlat"],
                            normalized_forms=["hauria (haguera) parlat"],
                            variation_types=None,
                            translation="hauria (haguera) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["hauríem (haguérem) parlat"],
                            normalized_forms=["hauriem (haguerem) parlat"],
                            variation_types=None,
                            translation="hauríem (haguérem) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["hauríeu (haguéreu) parlat"],
                            normalized_forms=["haurieu (haguereu) parlat"],
                            variation_types=None,
                            translation="hauríeu (haguéreu) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["haurien (hagueren) parlat"],
                            normalized_forms=["haurien (hagueren) parlat"],
                            variation_types=None,
                            translation="haurien (hagueren) parlat",
                        ),
                    ],
                ),
            ],
        ),
        Database__MoodBlock(
            mood="subjuntiu",
            tenses=[
                Database__TenseBlock(
                    tense="present",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["parli", "parle"],
                            normalized_forms=["parli", "parle"],
                            variation_types=[None, "(val.)"],
                            translation="parli",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["parlis", "parles"],
                            normalized_forms=["parlis", "parles"],
                            variation_types=[None, "(val.)"],
                            translation="parlis",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["parli", "parle"],
                            normalized_forms=["parli", "parle"],
                            variation_types=[None, "(val.)"],
                            translation="parli",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["parlem"],
                            normalized_forms=["parlem"],
                            variation_types=None,
                            translation="parlem",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["parleu"],
                            normalized_forms=["parleu"],
                            variation_types=None,
                            translation="parleu",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["parlin", "parlen"],
                            normalized_forms=["parlin", "parlen"],
                            variation_types=[None, "(val.)"],
                            translation="parlin",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="perfet",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["hagi (haja) parlat"],
                            normalized_forms=["hagi (haja) parlat"],
                            variation_types=None,
                            translation="hagi (haja) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["hagis (hages) parlat"],
                            normalized_forms=["hagis (hages) parlat"],
                            variation_types=None,
                            translation="hagis (hages) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["hagi (haja) parlat"],
                            normalized_forms=["hagi (haja) parlat"],
                            variation_types=None,
                            translation="hagi (haja) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["hàgim (hàgem) parlat"],
                            normalized_forms=["hagim (hagem) parlat"],
                            variation_types=None,
                            translation="hàgim (hàgem) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["hàgiu (hàgeu) parlat"],
                            normalized_forms=["hagiu (hageu) parlat"],
                            variation_types=None,
                            translation="hàgiu (hàgeu) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["hagin (hagen) parlat"],
                            normalized_forms=["hagin (hagen) parlat"],
                            variation_types=None,
                            translation="hagin (hagen) parlat",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="imperfet",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["parlés", "parlara", "parlàs"],
                            normalized_forms=["parles", "parlara", "parlas"],
                            variation_types=[None, "(val.)", "(val., bal.)"],
                            translation="parlés",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=[
                                "parlessis",
                                "parlares",
                                "parlassis",
                                "parlesses",
                                "parlasses",
                            ],
                            normalized_forms=[
                                "parlessis",
                                "parlares",
                                "parlassis",
                                "parlesses",
                                "parlasses",
                            ],
                            variation_types=[
                                None,
                                "(val.)",
                                "(bal.)",
                                None,
                                "(val., bal.)",
                            ],
                            translation="parlessis",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["parlés", "parlara", "parlàs"],
                            normalized_forms=["parles", "parlara", "parlas"],
                            variation_types=[None, "(val.)", "(val., bal.)"],
                            translation="parlés",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=[
                                "parléssim",
                                "parlàrem",
                                "parlàssim",
                                "parléssem",
                                "parlàssem",
                            ],
                            normalized_forms=[
                                "parlessim",
                                "parlarem",
                                "parlassim",
                                "parlessem",
                                "parlassem",
                            ],
                            variation_types=[
                                None,
                                "(val.)",
                                "(bal.)",
                                None,
                                "(val., bal.)",
                            ],
                            translation="parléssim",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=[
                                "parléssiu",
                                "parlàreu",
                                "parlàssiu",
                                "parlésseu",
                                "parlàsseu",
                            ],
                            normalized_forms=[
                                "parlessiu",
                                "parlareu",
                                "parlassiu",
                                "parlesseu",
                                "parlasseu",
                            ],
                            variation_types=[
                                None,
                                "(val.)",
                                "(bal.)",
                                None,
                                "(val., bal.)",
                            ],
                            translation="parléssiu",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=[
                                "parlessin",
                                "parlaren",
                                "parlassin",
                                "parlessen",
                                "parlassen",
                            ],
                            normalized_forms=[
                                "parlessin",
                                "parlaren",
                                "parlassin",
                                "parlessen",
                                "parlassen",
                            ],
                            variation_types=[
                                None,
                                "(val.)",
                                "(bal.)",
                                None,
                                "(val., bal.)",
                            ],
                            translation="parlessin",
                        ),
                    ],
                ),
                Database__TenseBlock(
                    tense="plusquamperfet",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="jo",
                            forms=["hagués (haguera) parlat"],
                            normalized_forms=["hagues (haguera) parlat"],
                            variation_types=None,
                            translation="hagués (haguera) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["haguessis (hagueres) parlat"],
                            normalized_forms=["haguessis (hagueres) parlat"],
                            variation_types=None,
                            translation="haguessis (hagueres) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["hagués (haguera) parlat"],
                            normalized_forms=["hagues (haguera) parlat"],
                            variation_types=None,
                            translation="hagués (haguera) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["haguéssim (haguérem) parlat"],
                            normalized_forms=["haguessim (haguerem) parlat"],
                            variation_types=None,
                            translation="haguéssim (haguérem) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["haguéssiu (haguéreu) parlat"],
                            normalized_forms=["haguessiu (haguereu) parlat"],
                            variation_types=None,
                            translation="haguéssiu (haguéreu) parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["haguessin (hagueren) parlat"],
                            normalized_forms=["haguessin (hagueren) parlat"],
                            variation_types=None,
                            translation="haguessin (hagueren) parlat",
                        ),
                    ],
                ),
            ],
        ),
        Database__MoodBlock(
            mood="imperatiu",
            tenses=[
                Database__TenseBlock(
                    tense="present",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="tu",
                            forms=["parla"],
                            normalized_forms=["parla"],
                            variation_types=None,
                            translation="parla",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ell, ella, vostè",
                            forms=["parli", "parle"],
                            normalized_forms=["parli", "parle"],
                            variation_types=[None, "(val.)"],
                            translation="parli",
                        ),
                        Database__ConjugatedForm(
                            pronoun="nosaltres",
                            forms=["parlem"],
                            normalized_forms=["parlem"],
                            variation_types=None,
                            translation="parlem",
                        ),
                        Database__ConjugatedForm(
                            pronoun="vosaltres, vós",
                            forms=["parleu", "parlau"],
                            normalized_forms=["parleu", "parlau"],
                            variation_types=[None, "(bal.)"],
                            translation="parleu",
                        ),
                        Database__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            forms=["parlin", "parlen"],
                            normalized_forms=["parlin", "parlen"],
                            variation_types=[None, "(val.)"],
                            translation="parlin",
                        ),
                    ],
                )
            ],
        ),
        Database__MoodBlock(
            mood="formes_no_personals",
            tenses=[
                Database__TenseBlock(
                    tense="formes_no_personals",
                    conjugation=[
                        Database__ConjugatedForm(
                            pronoun="Infinitiu",
                            forms=["parlar"],
                            normalized_forms=["parlar"],
                            variation_types=None,
                            translation="parlar",
                        ),
                        Database__ConjugatedForm(
                            pronoun="Infinitiu compost",
                            forms=["haver parlat"],
                            normalized_forms=["haver parlat"],
                            variation_types=None,
                            translation="haver parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="Gerundi",
                            forms=["parlant"],
                            normalized_forms=["parlant"],
                            variation_types=None,
                            translation="parlant",
                        ),
                        Database__ConjugatedForm(
                            pronoun="Gerundi compost",
                            forms=["havent parlat"],
                            normalized_forms=["havent parlat"],
                            variation_types=None,
                            translation="havent parlat",
                        ),
                        Database__ConjugatedForm(
                            pronoun="Participi",
                            forms=["parlat", "parlada", "parlats", "parlades"],
                            normalized_forms=[
                                "parlat",
                                "parlada",
                                "parlats",
                                "parlades",
                            ],
                            variation_types=None,
                            translation="parlat",
                        ),
                    ],
                )
            ],
        ),
    ],
    clicks=0,
    created_at=datetime.datetime(2025, 9, 29, 17, 34, 30, 188153),
)

test_parlar_translated = AI__VerbOutput(
    initial_letter="p",
    infinitive="parlar",
    translation="hablar",
    moods=[
        AI__MoodBlock(
            mood="Indicatiu",
            tenses=[
                AI__TenseBlock(
                    tense="present",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hablo"),
                        AI__ConjugatedForm(pronoun="tu", translation="hablas"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="habla"
                        ),
                        AI__ConjugatedForm(pronoun="nosaltres", translation="hablamos"),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="habláis"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hablan"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="perfet",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="he hablado"),
                        AI__ConjugatedForm(pronoun="tu", translation="has hablado"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="ha hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hemos hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="habéis hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="han hablado"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="imperfet",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hablaba"),
                        AI__ConjugatedForm(pronoun="tu", translation="hablabas"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hablaba"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hablábamos"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hablabais"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hablaban"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="plusquamperfet",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="había hablado"),
                        AI__ConjugatedForm(pronoun="tu", translation="habías hablado"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="había hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="habíamos hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="habíais hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="habían hablado"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="passat_simple",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hablé"),
                        AI__ConjugatedForm(pronoun="tu", translation="hablaste"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="habló"
                        ),
                        AI__ConjugatedForm(pronoun="nosaltres", translation="hablamos"),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hablasteis"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hablaron"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="passat_perifrastic",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hablé"),
                        AI__ConjugatedForm(pronoun="tu", translation="hablaste"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="habló"
                        ),
                        AI__ConjugatedForm(pronoun="nosaltres", translation="hablamos"),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hablasteis"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hablaron"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="passat_anterior",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hube hablado"),
                        AI__ConjugatedForm(pronoun="tu", translation="hubiste hablado"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hubo hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hubimos hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hubisteis hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            translation="hubieron hablado",
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="passat_anterior_perifrastic",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hube hablado"),
                        AI__ConjugatedForm(pronoun="tu", translation="hubiste hablado"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hubo hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hubimos hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hubisteis hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            translation="hubieron hablado",
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="futur",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hablaré"),
                        AI__ConjugatedForm(pronoun="tu", translation="hablarás"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hablará"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hablaremos"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hablaréis"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hablarán"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="futur_perfet",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="habré hablado"),
                        AI__ConjugatedForm(pronoun="tu", translation="habrás hablado"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="habrá hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="habremos hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="habréis hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="habrán hablado"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="condicional",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hablaría"),
                        AI__ConjugatedForm(pronoun="tu", translation="hablarías"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hablaría"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hablaríamos"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hablaríais"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hablarían"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="condicional_perfet",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="habría hablado"),
                        AI__ConjugatedForm(pronoun="tu", translation="habrías hablado"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="habría hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="habríamos hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="habríais hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="habrían hablado"
                        ),
                    ],
                ),
            ],
        ),
        AI__MoodBlock(
            mood="Subjuntiu",
            tenses=[
                AI__TenseBlock(
                    tense="present",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hable"),
                        AI__ConjugatedForm(pronoun="tu", translation="hables"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hable"
                        ),
                        AI__ConjugatedForm(pronoun="nosaltres", translation="hablemos"),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="habléis"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hablen"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="perfet",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="haya hablado"),
                        AI__ConjugatedForm(pronoun="tu", translation="hayas hablado"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="haya hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hayamos hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hayáis hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hayan hablado"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="imperfet",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hablara"),
                        AI__ConjugatedForm(pronoun="tu", translation="hablaras"),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hablara"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="habláramos"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hablarais"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès", translation="hablaran"
                        ),
                    ],
                ),
                AI__TenseBlock(
                    tense="plusquamperfet",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="jo", translation="hubiera hablado"),
                        AI__ConjugatedForm(
                            pronoun="tu", translation="hubieras hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hubiera hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hubiéramos hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hubierais hablado"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            translation="hubieran hablado",
                        ),
                    ],
                ),
            ],
        ),
        AI__MoodBlock(
            mood="Imperatiu",
            tenses=[
                AI__TenseBlock(
                    tense="present",
                    conjugation=[
                        AI__ConjugatedForm(
                            pronoun="tu", translation="habla, no hables"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ell, ella, vostè", translation="hable, no hable"
                        ),
                        AI__ConjugatedForm(
                            pronoun="nosaltres", translation="hablemos, no hablemos"
                        ),
                        AI__ConjugatedForm(
                            pronoun="vosaltres, vós", translation="hablad, no habléis"
                        ),
                        AI__ConjugatedForm(
                            pronoun="ells, elles, vostès",
                            translation="hablen, no hablen",
                        ),
                    ],
                )
            ],
        ),
        AI__MoodBlock(
            mood="Formes no personals",
            tenses=[
                AI__TenseBlock(
                    tense="infinitiu",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="Infinitiu", translation="hablar")
                    ],
                ),
                AI__TenseBlock(
                    tense="infinitiu_compost",
                    conjugation=[
                        AI__ConjugatedForm(
                            pronoun="Infinitiu compost", translation="haber hablado"
                        )
                    ],
                ),
                AI__TenseBlock(
                    tense="gerundi",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="Gerundi", translation="hablando")
                    ],
                ),
                AI__TenseBlock(
                    tense="gerundi_compost",
                    conjugation=[
                        AI__ConjugatedForm(
                            pronoun="Gerundi compost", translation="habiendo hablado"
                        )
                    ],
                ),
                AI__TenseBlock(
                    tense="participi",
                    conjugation=[
                        AI__ConjugatedForm(pronoun="Participi", translation="hablado")
                    ],
                ),
            ],
        ),
    ],
    updated_at=datetime.datetime(2025, 9, 29, 17, 43, 9, 105337),
)
