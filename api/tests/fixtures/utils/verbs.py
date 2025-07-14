from api.schemas.verbs import VerbConjugation, VerbMode, VerbOut


fake_data = VerbOut(
    _id="test_id",
    infinitive="test",
    translation="test",
    conjugation=[
        VerbMode(
            tense="test_tense",
            conjugation=[
                VerbConjugation(
                    pronoun="p1",
                    forms=["f1"],
                    variation_types=None,
                    translation="f1",
                ),
                VerbConjugation(
                    pronoun="p2",
                    forms=["f2"],
                    variation_types=None,
                    translation="f2",
                ),
            ],
        ),
        VerbMode(
            tense="another_tense",
            conjugation=[
                VerbConjugation(
                    pronoun="p1",
                    forms=["f3"],
                    variation_types=None,
                    translation="f3",
                ),
                VerbConjugation(
                    pronoun="p2",
                    forms=["f4"],
                    variation_types=None,
                    translation="f4",
                ),
            ],
        ),
    ],
    created_at="2023-10-01T00:00:00Z",
)

fake_conjugation_data = [
    {
        "tense": "indicatiu_present",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["vaig"],
                "variation_types": None,
                "translation": "vaig",
            },
            {
                "pronoun": "tu",
                "forms": ["vas"],
                "variation_types": None,
                "translation": "vas",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["va"],
                "variation_types": None,
                "translation": "va",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["anem", "anam"],
                "variation_types": [None, "(bal.)"],
                "translation": "anem",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["aneu", "anau"],
                "variation_types": [None, "(bal.)"],
                "translation": "aneu",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["van"],
                "variation_types": None,
                "translation": "van",
            },
        ],
    },
    {
        "tense": "indicatiu_perfet",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["he anat"],
                "variation_types": None,
                "translation": "he anat",
            },
            {
                "pronoun": "tu",
                "forms": ["has anat"],
                "variation_types": None,
                "translation": "has anat",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["ha anat"],
                "variation_types": None,
                "translation": "ha anat",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["hem anat"],
                "variation_types": None,
                "translation": "hem anat",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["heu anat"],
                "variation_types": None,
                "translation": "heu anat",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["han anat"],
                "variation_types": None,
                "translation": "han anat",
            },
        ],
    },
    {
        "tense": "indicatiu_imperfet",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["anava"],
                "variation_types": None,
                "translation": "anava",
            },
            {
                "pronoun": "tu",
                "forms": ["anaves"],
                "variation_types": None,
                "translation": "anaves",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["anava"],
                "variation_types": None,
                "translation": "anava",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["anàvem"],
                "variation_types": None,
                "translation": "anàvem",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["anàveu"],
                "variation_types": None,
                "translation": "anàveu",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["anaven"],
                "variation_types": None,
                "translation": "anaven",
            },
        ],
    },
    {
        "tense": "indicatiu_plusquamperfet",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["havia anat"],
                "variation_types": None,
                "translation": "havia anat",
            },
            {
                "pronoun": "tu",
                "forms": ["havies anat"],
                "variation_types": None,
                "translation": "havies anat",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["havia anat"],
                "variation_types": None,
                "translation": "havia anat",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["havíem anat"],
                "variation_types": None,
                "translation": "havíem anat",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["havíeu anat"],
                "variation_types": None,
                "translation": "havíeu anat",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["havien anat"],
                "variation_types": None,
                "translation": "havien anat",
            },
        ],
    },
    {
        "tense": "indicatiu_passat_simple",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["aní"],
                "variation_types": None,
                "translation": "aní",
            },
            {
                "pronoun": "tu",
                "forms": ["anares"],
                "variation_types": None,
                "translation": "anares",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["anà"],
                "variation_types": None,
                "translation": "anà",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["anàrem"],
                "variation_types": None,
                "translation": "anàrem",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["anàreu"],
                "variation_types": None,
                "translation": "anàreu",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["anaren"],
                "variation_types": None,
                "translation": "anaren",
            },
        ],
    },
    {
        "tense": "indicatiu_passat_perifràstic",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["vaig anar"],
                "variation_types": None,
                "translation": "vaig anar",
            },
            {
                "pronoun": "tu",
                "forms": ["vas (vares) anar"],
                "variation_types": None,
                "translation": "vas (vares) anar",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["va anar"],
                "variation_types": None,
                "translation": "va anar",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["vam (vàrem) anar"],
                "variation_types": None,
                "translation": "vam (vàrem) anar",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["vau (vàreu) anar"],
                "variation_types": None,
                "translation": "vau (vàreu) anar",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["van (varen) anar"],
                "variation_types": None,
                "translation": "van (varen) anar",
            },
        ],
    },
    {
        "tense": "indicatiu_passat_anterior",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["haguí anat"],
                "variation_types": None,
                "translation": "haguí anat",
            },
            {
                "pronoun": "tu",
                "forms": ["hagueres anat"],
                "variation_types": None,
                "translation": "hagueres anat",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["hagué anat"],
                "variation_types": None,
                "translation": "hagué anat",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["haguérem anat"],
                "variation_types": None,
                "translation": "haguérem anat",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["haguéreu anat"],
                "variation_types": None,
                "translation": "haguéreu anat",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["hagueren anat"],
                "variation_types": None,
                "translation": "hagueren anat",
            },
        ],
    },
    {
        "tense": "indicatiu_passat_anterior_perifràstic",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["vaig haver anat"],
                "variation_types": None,
                "translation": "vaig haver anat",
            },
            {
                "pronoun": "tu",
                "forms": ["vas haver anat"],
                "variation_types": None,
                "translation": "vas haver anat",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["va haver anat"],
                "variation_types": None,
                "translation": "va haver anat",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["vam haver anat"],
                "variation_types": None,
                "translation": "vam haver anat",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["vau haver anat"],
                "variation_types": None,
                "translation": "vau haver anat",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["van haver anat"],
                "variation_types": None,
                "translation": "van haver anat",
            },
        ],
    },
    {
        "tense": "indicatiu_futur",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["aniré / iré"],
                "variation_types": None,
                "translation": "aniré / iré",
            },
            {
                "pronoun": "tu",
                "forms": ["aniràs / iràs"],
                "variation_types": None,
                "translation": "aniràs / iràs",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["anirà / irà"],
                "variation_types": None,
                "translation": "anirà / irà",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["anirem / irem"],
                "variation_types": None,
                "translation": "anirem / irem",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["anireu / ireu"],
                "variation_types": None,
                "translation": "anireu / ireu",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["aniran / iran"],
                "variation_types": None,
                "translation": "aniran / iran",
            },
        ],
    },
    {
        "tense": "indicatiu_futur_perfet",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["hauré anat"],
                "variation_types": None,
                "translation": "hauré anat",
            },
            {
                "pronoun": "tu",
                "forms": ["hauràs anat"],
                "variation_types": None,
                "translation": "hauràs anat",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["haurà anat"],
                "variation_types": None,
                "translation": "haurà anat",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["haurem anat"],
                "variation_types": None,
                "translation": "haurem anat",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["haureu anat"],
                "variation_types": None,
                "translation": "haureu anat",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["hauran anat"],
                "variation_types": None,
                "translation": "hauran anat",
            },
        ],
    },
    {
        "tense": "indicatiu_condicional",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["aniria / iria"],
                "variation_types": None,
                "translation": "aniria / iria",
            },
            {
                "pronoun": "tu",
                "forms": ["aniries / iries"],
                "variation_types": None,
                "translation": "aniries / iries",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["aniria / iria"],
                "variation_types": None,
                "translation": "aniria / iria",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["aniríem / iríem"],
                "variation_types": None,
                "translation": "aniríem / iríem",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["aniríeu / iríeu"],
                "variation_types": None,
                "translation": "aniríeu / iríeu",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["anirien / irien"],
                "variation_types": None,
                "translation": "anirien / irien",
            },
        ],
    },
    {
        "tense": "indicatiu_condicional_perfet",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["hauria (haguera) anat"],
                "variation_types": None,
                "translation": "hauria (haguera) anat",
            },
            {
                "pronoun": "tu",
                "forms": ["hauries (hagueres) anat"],
                "variation_types": None,
                "translation": "hauries (hagueres) anat",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["hauria (haguera) anat"],
                "variation_types": None,
                "translation": "hauria (haguera) anat",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["hauríem (haguérem) anat"],
                "variation_types": None,
                "translation": "hauríem (haguérem) anat",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["hauríeu (haguéreu) anat"],
                "variation_types": None,
                "translation": "hauríeu (haguéreu) anat",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["haurien (hagueren) anat"],
                "variation_types": None,
                "translation": "haurien (hagueren) anat",
            },
        ],
    },
    {
        "tense": "subjuntiu_present",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["vagi", "vaja"],
                "variation_types": [None, "(val.)"],
                "translation": "vagi",
            },
            {
                "pronoun": "tu",
                "forms": ["vagis", "vages"],
                "variation_types": [None, "(val.)"],
                "translation": "vagis",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["vagi", "vaja"],
                "variation_types": [None, "(val.)"],
                "translation": "vagi",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["anem"],
                "variation_types": None,
                "translation": "anem",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["aneu"],
                "variation_types": None,
                "translation": "aneu",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["vagin", "vagen"],
                "variation_types": [None, "(val.)"],
                "translation": "vagin",
            },
        ],
    },
    {
        "tense": "subjuntiu_perfet",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["hagi (haja) anat"],
                "variation_types": None,
                "translation": "hagi (haja) anat",
            },
            {
                "pronoun": "tu",
                "forms": ["hagis (hages) anat"],
                "variation_types": None,
                "translation": "hagis (hages) anat",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["hagi (haja) anat"],
                "variation_types": None,
                "translation": "hagi (haja) anat",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["hàgim (hàgem) anat"],
                "variation_types": None,
                "translation": "hàgim (hàgem) anat",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["hàgiu (hàgeu) anat"],
                "variation_types": None,
                "translation": "hàgiu (hàgeu) anat",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["hagin (hagen) anat"],
                "variation_types": None,
                "translation": "hagin (hagen) anat",
            },
        ],
    },
    {
        "tense": "subjuntiu_imperfet",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["anés", "anara", "anàs"],
                "variation_types": [None, "(val.)", "(val., bal.)"],
                "translation": "anés",
            },
            {
                "pronoun": "tu",
                "forms": ["anessis", "anares", "anassis", "anesses", "anasses"],
                "variation_types": [None, "(val.)", "(bal.)", None, "(val., bal.)"],
                "translation": "anessis",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["anés", "anara", "anàs"],
                "variation_types": [None, "(val.)", "(val., bal.)"],
                "translation": "anés",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["anéssim", "anàrem", "anàssim", "anéssem", "anàssem"],
                "variation_types": [None, "(val.)", "(bal.)", None, "(val., bal.)"],
                "translation": "anéssim",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["anéssiu", "anàreu", "anàssiu", "anésseu", "anàsseu"],
                "variation_types": [None, "(val.)", "(bal.)", None, "(val., bal.)"],
                "translation": "anéssiu",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["anessin", "anaren", "anassin", "anessen", "anassen"],
                "variation_types": [None, "(val.)", "(bal.)", None, "(val., bal.)"],
                "translation": "anessin",
            },
        ],
    },
    {
        "tense": "subjuntiu_plusquamperfet",
        "conjugation": [
            {
                "pronoun": "jo",
                "forms": ["hagués (haguera) anat"],
                "variation_types": None,
                "translation": "hagués (haguera) anat",
            },
            {
                "pronoun": "tu",
                "forms": ["haguessis (hagueres) anat"],
                "variation_types": None,
                "translation": "haguessis (hagueres) anat",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["hagués (haguera) anat"],
                "variation_types": None,
                "translation": "hagués (haguera) anat",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["haguéssim (haguérem) anat"],
                "variation_types": None,
                "translation": "haguéssim (haguérem) anat",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["haguéssiu (haguéreu) anat"],
                "variation_types": None,
                "translation": "haguéssiu (haguéreu) anat",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["haguessin (hagueren) anat"],
                "variation_types": None,
                "translation": "haguessin (hagueren) anat",
            },
        ],
    },
    {
        "tense": "imperatiu_present",
        "conjugation": [
            {
                "pronoun": "tu",
                "forms": ["ves", "vés"],
                "variation_types": [None, "(ort. pre-2017)"],
                "translation": "ves",
            },
            {
                "pronoun": "ell, ella, vostè",
                "forms": ["vagi", "vaja"],
                "variation_types": [None, "(val.)"],
                "translation": "vagi",
            },
            {
                "pronoun": "nosaltres",
                "forms": ["anem"],
                "variation_types": None,
                "translation": "anem",
            },
            {
                "pronoun": "vosaltres, vós",
                "forms": ["aneu", "anau"],
                "variation_types": [None, "(bal.)"],
                "translation": "aneu",
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["vagin", "vagen"],
                "variation_types": [None, "(val.)"],
                "translation": "vagin",
            },
        ],
    },
    {
        "tense": "formes_no_personals",
        "conjugation": [
            {
                "pronoun": "Infinitiu",
                "forms": ["anar"],
                "variation_types": None,
                "translation": "anar",
            },
            {
                "pronoun": "Infinitiu compost",
                "forms": ["haver anat"],
                "variation_types": None,
                "translation": "haver anat",
            },
            {
                "pronoun": "Gerundi",
                "forms": ["anant"],
                "variation_types": None,
                "translation": "anant",
            },
            {
                "pronoun": "Gerundi compost",
                "forms": ["havent anat"],
                "variation_types": None,
                "translation": "havent anat",
            },
            {
                "pronoun": "Participi",
                "forms": ["anat", "anada", "anats", "anades"],
                "variation_types": None,
                "translation": "anat",
            },
        ],
    },
]
