# 🔄 Traducción de formas verbales catalanas al castellano (por ejemplo verbo: `anar`)

## 🎯 Objetivo

Traduce cada una de las siguientes formas verbales del catalán al **castellano**, manteniendo el orden original.

### 📌 Instrucciones

- Devuelve **solo** una lista de traducciones en **formato JSON**, **sin explicaciones**.
- No agrupes, no elimines duplicados, **traduce cada forma tal como aparece**.
- Vuelve el resultado sin **ordenar**, tal cual.
- Devuelve todos los verbos en la misma cantidad que aparecen en la entrada.
- Traduce el subjuntivo bien también
- **indicatiu_passat_perifràstic** es como pretérito simple en español, por lo tanto la traducción debe ser igual que con **passat_simple**
- **Ten cuidado** con paréntesis en la versión original — **ignóralos en salida**.

### 🧪 Ejemplo

#### Entrada

```json
[
  {"tense": "indicatiu_present", "conjugation": ["vaig", "vas", "va", "anem", "aneu", "van"]},
  ...
  {"tense": "indicatiu_passat_perifràstic", "conjugation": ["vaig anar", "vas (vares) anar", "va anar", "vam (vàrem) anar", "vau (vàreu) anar", "van (varen) anar"]},
  ...
  {"tense": "indicatiu_condicional_perfet", "conjugation": ["hauria (haguera) anat", "hauries (hagueres) anat", "hauria (haguera) anat", "hauríem (haguérem) anat", "hauríeu (haguéreu) anat", "haurien (hagueren) anat"]},
  ...
  {"tense": "subjuntiu_perfet", "conjugation": ["hagi (haja) anat", "hagis (hages) anat", "hagi (haja) anat", "hàgim (hàgem) anat", "hàgiu (hàgeu) anat", "hagin (hagen) anat"]},
  ...
  {"tense": "subjuntiu_plusquamperfet", "conjugation": ["hagués (haguera) anat", "haguessis (hagueres) anat", "hagués (haguera) anat", "haguéssim (haguérem) anat", "haguéssiu (haguéreu) anat", "haguessin (hagueren) anat"]}
]
```

#### Salida

```json
[
  {"tense": "indicatiu_present", "conjugation": ["voy", "vas", "va", "vamos", "vais", "van"]},
  ...
  {"tense": "indicatiu_passat_perifràstic", "conjugation": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"]},
  ...
  {"tense": "indicatiu_condicional_perfet", "conjugation": ["habría ido", "habrías ido", "habría ido", "habríamos ido", "habríais ido", "habrían ido"]},
  ...
  {"tense": "subjuntiu_perfet", "conjugation": ["haya ido", "hayas ido", "haya ido", "hayamos ido", "hayáis ido", "hayan ido"]},
  ...
  {"tense": "subjuntiu_plusquamperfet", "conjugation": ["hubiera ido", "hubieras ido", "hubiera ido", "hubiéramos ido", "hubierais ido", "hubieran ido"]}
]
```
