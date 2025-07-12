import datetime
from api.schemas.verbs import VerbConjugation, VerbCreate, VerbMode

create_verb_data = VerbCreate(
    infinitive="anar",
    translation="anar",
    conjugation=[
        VerbMode(
            tense="indicatiu_present",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["vaig"],
                    variation_types=None,
                    translation="voy",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["vas"],
                    variation_types=None,
                    translation="vas",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["va"],
                    variation_types=None,
                    translation="va",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["anem", "anam"],
                    variation_types=[None, "(bal.)"],
                    translation="vamos",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["aneu", "anau"],
                    variation_types=[None, "(bal.)"],
                    translation="vais",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["van"],
                    variation_types=None,
                    translation="van",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_perfet",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["he anat"],
                    variation_types=None,
                    translation="he ido",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["has anat"],
                    variation_types=None,
                    translation="has ido",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["ha anat"],
                    variation_types=None,
                    translation="ha ido",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["hem anat"],
                    variation_types=None,
                    translation="hemos ido",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["heu anat"],
                    variation_types=None,
                    translation="habéis ido",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["han anat"],
                    variation_types=None,
                    translation="han ido",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_imperfet",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["anava"],
                    variation_types=None,
                    translation="iba",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["anaves"],
                    variation_types=None,
                    translation="ibas",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["anava"],
                    variation_types=None,
                    translation="iba",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["anàvem"],
                    variation_types=None,
                    translation="íbamos",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["anàveu"],
                    variation_types=None,
                    translation="ibais",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["anaven"],
                    variation_types=None,
                    translation="iban",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_plusquamperfet",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["havia anat"],
                    variation_types=None,
                    translation="había ido",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["havies anat"],
                    variation_types=None,
                    translation="habías ido",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["havia anat"],
                    variation_types=None,
                    translation="había ido",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["havíem anat"],
                    variation_types=None,
                    translation="habíamos ido",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["havíeu anat"],
                    variation_types=None,
                    translation="habíais ido",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["havien anat"],
                    variation_types=None,
                    translation="habían ido",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_passat_simple",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["aní"],
                    variation_types=None,
                    translation="fui",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["anares"],
                    variation_types=None,
                    translation="fuiste",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["anà"],
                    variation_types=None,
                    translation="fue",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["anàrem"],
                    variation_types=None,
                    translation="fuimos",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["anàreu"],
                    variation_types=None,
                    translation="fuisteis",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["anaren"],
                    variation_types=None,
                    translation="fueron",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_passat_perifràstic",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["vaig anar"],
                    variation_types=None,
                    translation="fui a",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["vas (vares) anar"],
                    variation_types=None,
                    translation="fuiste a",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["va anar"],
                    variation_types=None,
                    translation="fue a",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["vam (vàrem) anar"],
                    variation_types=None,
                    translation="fuimos a",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["vau (vàreu) anar"],
                    variation_types=None,
                    translation="fuisteis a",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["van (varen) anar"],
                    variation_types=None,
                    translation="fueron a",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_passat_anterior",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["haguí anat"],
                    variation_types=None,
                    translation="hube ido",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["hagueres anat"],
                    variation_types=None,
                    translation="hubiste ido",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["hagué anat"],
                    variation_types=None,
                    translation="hubo ido",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["haguérem anat"],
                    variation_types=None,
                    translation="hubimos ido",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["haguéreu anat"],
                    variation_types=None,
                    translation="hubisteis ido",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["hagueren anat"],
                    variation_types=None,
                    translation="hubieron ido",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_passat_anterior_perifràstic",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["vaig haver anat"],
                    variation_types=None,
                    translation="hube habido ido",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["vas haver anat"],
                    variation_types=None,
                    translation="hubiste habido ido",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["va haver anat"],
                    variation_types=None,
                    translation="hubo habido ido",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["vam haver anat"],
                    variation_types=None,
                    translation="hubimos habido ido",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["vau haver anat"],
                    variation_types=None,
                    translation="hubisteis habido ido",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["van haver anat"],
                    variation_types=None,
                    translation="hubieron habido ido",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_futur",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["aniré / iré"],
                    variation_types=None,
                    translation="iré",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["aniràs / iràs"],
                    variation_types=None,
                    translation="irás",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["anirà / irà"],
                    variation_types=None,
                    translation="irá",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["anirem / irem"],
                    variation_types=None,
                    translation="iremos",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["anireu / ireu"],
                    variation_types=None,
                    translation="iréis",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["aniran / iran"],
                    variation_types=None,
                    translation="irán",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_futur_perfet",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["hauré anat"],
                    variation_types=None,
                    translation="habré ido",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["hauràs anat"],
                    variation_types=None,
                    translation="habrás ido",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["haurà anat"],
                    variation_types=None,
                    translation="habrá ido",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["haurem anat"],
                    variation_types=None,
                    translation="habremos ido",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["haureu anat"],
                    variation_types=None,
                    translation="habréis ido",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["hauran anat"],
                    variation_types=None,
                    translation="habrán ido",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_condicional",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["aniria / iria"],
                    variation_types=None,
                    translation="iría",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["aniries / iries"],
                    variation_types=None,
                    translation="irías",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["aniria / iria"],
                    variation_types=None,
                    translation="iría",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["aniríem / iríem"],
                    variation_types=None,
                    translation="iríamos",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["aniríeu / iríeu"],
                    variation_types=None,
                    translation="iríais",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["anirien / irien"],
                    variation_types=None,
                    translation="irían",
                ),
            ],
        ),
        VerbMode(
            tense="indicatiu_condicional_perfet",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["hauria (haguera) anat"],
                    variation_types=None,
                    translation="habría ido",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["hauries (hagueres) anat"],
                    variation_types=None,
                    translation="habrías ido",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["hauria (haguera) anat"],
                    variation_types=None,
                    translation="habría ido",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["hauríem (haguérem) anat"],
                    variation_types=None,
                    translation="habríamos ido",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["hauríeu (haguéreu) anat"],
                    variation_types=None,
                    translation="habríais ido",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["haurien (hagueren) anat"],
                    variation_types=None,
                    translation="habrían ido",
                ),
            ],
        ),
        VerbMode(
            tense="subjuntiu_present",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["vagi", "vaja"],
                    variation_types=[None, "(val.)"],
                    translation="vaya",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["vagis", "vages"],
                    variation_types=[None, "(val.)"],
                    translation="vayas",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["vagi", "vaja"],
                    variation_types=[None, "(val.)"],
                    translation="vaya",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["anem"],
                    variation_types=None,
                    translation="vayamos",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["aneu"],
                    variation_types=None,
                    translation="vayáis",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["vagin", "vagen"],
                    variation_types=[None, "(val.)"],
                    translation="vayan",
                ),
            ],
        ),
        VerbMode(
            tense="subjuntiu_perfet",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["hagi (haja) anat"],
                    variation_types=None,
                    translation="haya ido",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["hagis (hages) anat"],
                    variation_types=None,
                    translation="hayas ido",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["hagi (haja) anat"],
                    variation_types=None,
                    translation="haya ido",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["hàgim (hàgem) anat"],
                    variation_types=None,
                    translation="hayamos ido",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["hàgiu (hàgeu) anat"],
                    variation_types=None,
                    translation="hayáis ido",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["hagin (hagen) anat"],
                    variation_types=None,
                    translation="hayan ido",
                ),
            ],
        ),
        VerbMode(
            tense="subjuntiu_imperfet",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["anés", "anara", "anàs"],
                    variation_types=[None, "(val.)", "(val., bal.)"],
                    translation="fuera",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=[
                        "anessis",
                        "anares",
                        "anassis",
                        "anesses",
                        "anasses",
                    ],
                    variation_types=[
                        None,
                        "(val.)",
                        "(bal.)",
                        None,
                        "(val., bal.)",
                    ],
                    translation="fueras",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["anés", "anara", "anàs"],
                    variation_types=[None, "(val.)", "(val., bal.)"],
                    translation="fuera",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=[
                        "anéssim",
                        "anàrem",
                        "anàssim",
                        "anéssem",
                        "anàssem",
                    ],
                    variation_types=[
                        None,
                        "(val.)",
                        "(bal.)",
                        None,
                        "(val., bal.)",
                    ],
                    translation="fuéramos",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=[
                        "anéssiu",
                        "anàreu",
                        "anàssiu",
                        "anésseu",
                        "anàsseu",
                    ],
                    variation_types=[
                        None,
                        "(val.)",
                        "(bal.)",
                        None,
                        "(val., bal.)",
                    ],
                    translation="fueseis",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=[
                        "anessin",
                        "anaren",
                        "anassin",
                        "anessen",
                        "anassen",
                    ],
                    variation_types=[
                        None,
                        "(val.)",
                        "(bal.)",
                        None,
                        "(val., bal.)",
                    ],
                    translation="fueran",
                ),
            ],
        ),
        VerbMode(
            tense="subjuntiu_plusquamperfet",
            conjugation=[
                VerbConjugation(
                    pronoun="jo",
                    forms=["hagués (haguera) anat"],
                    variation_types=None,
                    translation="hubiera ido",
                ),
                VerbConjugation(
                    pronoun="tu",
                    forms=["haguessis (hagueres) anat"],
                    variation_types=None,
                    translation="hubieras ido",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["hagués (haguera) anat"],
                    variation_types=None,
                    translation="hubiera ido",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["haguéssim (haguérem) anat"],
                    variation_types=None,
                    translation="hubiéramos ido",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["haguéssiu (haguéreu) anat"],
                    variation_types=None,
                    translation="hubierais ido",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["haguessin (hagueren) anat"],
                    variation_types=None,
                    translation="hubieran ido",
                ),
            ],
        ),
        VerbMode(
            tense="imperatiu_present",
            conjugation=[
                VerbConjugation(
                    pronoun="tu",
                    forms=["ves", "vés"],
                    variation_types=[None, "(ort. pre-2017)"],
                    translation="ve",
                ),
                VerbConjugation(
                    pronoun="ell, ella, vostè",
                    forms=["vagi", "vaja"],
                    variation_types=[None, "(val.)"],
                    translation="vaya",
                ),
                VerbConjugation(
                    pronoun="nosaltres",
                    forms=["anem"],
                    variation_types=None,
                    translation="vamos",
                ),
                VerbConjugation(
                    pronoun="vosaltres, vós",
                    forms=["aneu", "anau"],
                    variation_types=[None, "(bal.)"],
                    translation="id",
                ),
                VerbConjugation(
                    pronoun="ells, elles, vostès",
                    forms=["vagin", "vagen"],
                    variation_types=[None, "(val.)"],
                    translation="vayan",
                ),
            ],
        ),
        VerbMode(
            tense="formes_no_personals",
            conjugation=[
                VerbConjugation(
                    pronoun="Infinitiu",
                    forms=["anar"],
                    variation_types=None,
                    translation="ir",
                ),
                VerbConjugation(
                    pronoun="Infinitiu compost",
                    forms=["haver anat"],
                    variation_types=None,
                    translation="haber ido",
                ),
                VerbConjugation(
                    pronoun="Gerundi",
                    forms=["anant"],
                    variation_types=None,
                    translation="yendo",
                ),
                VerbConjugation(
                    pronoun="Gerundi compost",
                    forms=["havent anat"],
                    variation_types=None,
                    translation="habiendo ido",
                ),
                VerbConjugation(
                    pronoun="Participi",
                    forms=["anat", "anada", "anats", "anades"],
                    variation_types=None,
                    translation="ido",
                ),
            ],
        ),
    ],
    created_at=datetime.datetime(2025, 7, 10, 18, 28, 6, 367064),
)
