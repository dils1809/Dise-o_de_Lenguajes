# Analizador Sintáctico Predictivo LL(1)

Proyecto del curso **Diseño de Lenguajes** — Semestre 7

- **Repositorio:** [dils1809/Dise-o_de_Lenguajes](https://github.com/dils1809/Dise-o_de_Lenguajes/tree/main/Dise-o_de_Lenguajes/Syntax_Table)
- **Video explicativo:** [https://youtu.be/6NNQVnYcxls](https://youtu.be/6NNQVnYcxls)

---

## Descripción del proyecto

Este programa procesa gramáticas libres de contexto (CFG) de forma **general**:
acepta cualquier gramática ingresada como diccionario Python, calcula
automáticamente los conjuntos **FIRST** y **FOLLOW**, construye la
**tabla de análisis sintáctico predictivo LL(1)** y determina si la gramática
cumple con la propiedad LL(1) o presenta conflictos.

---

## Estructura del repositorio

```
Syntax_Table/
├── main.py          — Punto de entrada; define las 3 gramáticas de prueba
├── grammar.py       — Utilidades: terminales, no terminales, símbolo inicial
├── first_follow.py  — Cálculo iterativo de FIRST y FOLLOW
├── parsing_table.py — Construcción de la tabla LL(1) y detección de conflictos
├── utils.py         — Funciones de impresión con formato legible
└── README.md        — Este archivo
```

---

## Cómo ejecutar el programa

### Requisitos

- Python 3.8 o superior (sin dependencias externas)

### Ejecución

```bash
# Desde la raíz del repositorio
python -X utf8 main.py
```

> La bandera `-X utf8` asegura que el símbolo ε se imprima correctamente
> en terminales Windows. En Linux / macOS no es necesaria.

### Agregar una gramática propia

Edita `main.py` y define un diccionario con el formato:

```python
mi_gramatica = {
    "S": [["a", "B"], ["c"]],
    "B": [["b", "B"], ["ε"]],
}
analyze_grammar("Mi gramática", mi_gramatica)
```

Cada llave es un **no terminal**; cada valor es una lista de producciones,
y cada producción es una lista de símbolos.  Usa `"ε"` para epsilon.

---

## Gramáticas utilizadas

### Gramática 1 — Expresiones Aritméticas (LL(1))

Gramática clásica transformada (sin recursión por la izquierda):

```
E  ->  T E'
E' ->  + T E'  |  ε
T  ->  F T'
T' ->  * F T'  |  ε
F  ->  ( E )   |  id
```

### Gramática 2 — Lenguaje de Sentencias Simple (LL(1))

Modela una secuencia de sentencias de asignación o retorno:

```
P  ->  S L
L  ->  S L  |  ε
S  ->  id = E ;  |  return E ;
E  ->  id  |  num
```

### Gramática 3 — Aritmética con Recursión Izquierda (NO LL(1))

La gramática aritmética original sin transformar:

```
E  ->  E + T  |  T
T  ->  T * F  |  F
F  ->  ( E )  |  id
```

---

## Resultados obtenidos

### Gramática 1 — Expresiones Aritméticas

**Conjuntos FIRST:**

| No terminal | FIRST |
|-------------|-------|
| E  | `{(, id}` |
| E' | `{+, ε}` |
| T  | `{(, id}` |
| T' | `{*, ε}` |
| F  | `{(, id}` |

**Conjuntos FOLLOW:**

| No terminal | FOLLOW |
|-------------|--------|
| E  | `{$, )}` |
| E' | `{$, )}` |
| T  | `{$, ), +}` |
| T' | `{$, ), +}` |
| F  | `{$, ), *, +}` |

**Tabla LL(1):**

|    | `(` | `)` | `*` | `+` | `id` | `$` |
|----|-----|-----|-----|-----|------|-----|
| E  | E → T E' | — | — | — | E → T E' | — |
| E' | — | E' → ε | — | E' → + T E' | — | E' → ε |
| T  | T → F T' | — | — | — | T → F T' | — |
| T' | — | T' → ε | T' → * F T' | T' → ε | — | T' → ε |
| F  | F → ( E ) | — | — | — | F → id | — |

**Resultado:** La gramática ES LL(1) — ninguna celda tiene más de una producción.

---

### Gramática 2 — Lenguaje de Sentencias

**Conjuntos FIRST:**

| No terminal | FIRST |
|-------------|-------|
| P | `{id, return}` |
| L | `{id, return, ε}` |
| S | `{id, return}` |
| E | `{id, num}` |

**Conjuntos FOLLOW:**

| No terminal | FOLLOW |
|-------------|--------|
| P | `{$}` |
| L | `{$}` |
| S | `{$, id, return}` |
| E | `{;}` |

**Tabla LL(1):**

|   | `id` | `num` | `return` | `;` | `=` | `$` |
|---|------|-------|----------|-----|-----|-----|
| P | P → S L | — | P → S L | — | — | — |
| L | L → S L | — | L → S L | — | — | L → ε |
| S | S → id = E ; | — | S → return E ; | — | — | — |
| E | E → id | E → num | — | — | — | — |

**Resultado:** La gramática ES LL(1) — sin conflictos.

---

### Gramática 3 — Aritmética con Recursión Izquierda

**Conjuntos FIRST:**

| No terminal | FIRST |
|-------------|-------|
| E | `{(, id}` |
| T | `{(, id}` |
| F | `{(, id}` |

**Conflictos en la tabla:**

| Celda | Producciones en conflicto |
|-------|--------------------------|
| M[E][(]  | E → E + T  /  E → T |
| M[E][id] | E → E + T  /  E → T |
| M[T][(]  | T → T * F  /  T → F |
| M[T][id] | T → T * F  /  T → F |

**Resultado:** La gramática NO es LL(1) — 4 conflictos detectados.

---

## Explicación de si son LL(1) o no

### ¿Por qué la Gramática 1 y 2 son LL(1)?

Una gramática es LL(1) si para cada no terminal **A** y cada par de
producciones distintas `A → α` y `A → β`:

1. `FIRST(α) ∩ FIRST(β) = ∅`
2. Si `ε ∈ FIRST(α)`, entonces `FIRST(β) ∩ FOLLOW(A) = ∅`

En la **Gramática 1**, las dos producciones de cada no terminal tienen
conjuntos FIRST disjuntos (por ejemplo, `E' → + T E'` comienza con `+`
y `E' → ε` usa FOLLOW(E') = `{$, )}`; no hay solapamiento).

En la **Gramática 2**, cada producción de `S` comienza con un terminal
diferente (`id` vs `return`), y `L → ε` solo aplica cuando el siguiente
token es `$`, que no está en FIRST(S).

### ¿Por qué la Gramática 3 NO es LL(1)?

La **Gramática 3** es **recursiva por la izquierda**.  La producción
`E → E + T` comienza con el propio no terminal `E`, cuyo FIRST es
`{(, id}`.  La otra producción `E → T` también tiene FIRST `{(, id}`.
Ambas contribuyen entradas a `M[E][(]` y `M[E][id]`, generando
conflictos irresolubles.

La solución estándar es eliminar la recursión izquierda (transformación
aplicada en la Gramática 1), obteniendo la forma iterativa con `E'`.

---

## Explicación del código

### `grammar.py`
Provee tres funciones auxiliares: `get_non_terminals`, `get_terminals`
y `get_start_symbol`.  El símbolo inicial es siempre el **primer key**
del diccionario.

### `first_follow.py`
- **`compute_first_of_sequence`** — aplica las reglas de FIRST sobre una
  secuencia de símbolos usando los conjuntos ya calculados (sin recursión
  directa, seguro para gramáticas con recursión izquierda).
- **`compute_all_first`** — punto fijo iterativo: repite hasta que ningún
  conjunto FIRST crezca.
- **`compute_follow`** — punto fijo iterativo con las 3 reglas de FOLLOW
  (símbolo inicial recibe `$`, se usa FIRST de lo que sigue, y se
  propaga FOLLOW cuando hay `ε`).

### `parsing_table.py`
- **`build_parsing_table`** — para cada producción `A → α` calcula
  `FIRST(α)`; registra la producción en `M[A][a]` para cada `a`.  Si
  `ε ∈ FIRST(α)`, usa FOLLOW(A).  Cada celda es una lista, permitiendo
  detectar múltiples entradas.
- **`is_ll1`** — recorre la tabla y recopila celdas con más de una
  producción.

### `utils.py`
Funciones `print_*` con formato de columnas para mostrar la tabla de
forma alineada en la terminal.
