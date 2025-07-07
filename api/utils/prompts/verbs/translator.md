# 🔄 Traducción de formas verbales catalanas al castellano (por ejemplo verbo: `anar`)

## 🎯 Objetivo

Traduce cada una de las siguientes formas verbales del catalán al **castellano**, manteniendo el orden original.

### 📌 Instrucciones

- Devuelve **solo** una lista de traducciones en **formato JSON**, **sin explicaciones**.
- Si hay variantes dentro de una misma forma (por ejemplo: `"aniré / iré"` o `"vaig (vares) anar"`), traduce **solo la forma principal** o **más estándar** al castellano.
- Ignora anotaciones como `(val.)`, `(bal.)`, `(haguera)`, etc.
- No agrupes, no elimines duplicados, **traduce cada forma tal como aparece**.
- Vuelve el resultado sin **ordenar**, tal cual.

### 🧪 Ejemplo

#### Entrada

```json
["vaig", "vas", "va", "anem", "aneu", "van"]
```

#### Salida

```json
["voy", "vas", "va", "vamos", "vais", "van"]
```
