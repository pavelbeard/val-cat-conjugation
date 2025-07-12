# Traduce al español cada forma verbal de este verbo catalán/valenciano

- Devuelve el resultado en formato JSON con campos `tense` y `conjugation`.
- Traduce **cada forma literal** como está escrita (no agrupar).
- Ignora los paréntesis (como `(haja)`, `(vares)`, etc).
- Mantén el mismo orden de los elementos en la lista.
- No añadas explicaciones.

## Ejemplo

### Entrada

```json
[
  {"tense": "indicatiu_present", "conjugation": ["vaig", "vas", "va", "anem", "aneu", "van"]},
  {"tense": "indicatiu_passat_perifràstic", "conjugation": ["vaig anar", "vas (vares) anar", "va anar", "vam anar", "vau anar", "van anar"]},
  {"tense": "subjuntiu_perfet", "conjugation": ["hagi (haja) anat", "hagis (hages) anat", "hagi (haja) anat", "hàgim anat", "hàgiu anat", "hagin anat"]}
]
```

### Salida

```json
[
  {"tense": "indicatiu_present", "conjugation": ["voy", "vas", "va", "vamos", "vais", "van"]},
  {"tense": "indicatiu_passat_perifràstic", "conjugation": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"]},
  {"tense": "subjuntiu_perfet", "conjugation": ["haya ido", "hayas ido", "haya ido", "hayamos ido", "hayáis ido", "hayan ido"]}
]
```
