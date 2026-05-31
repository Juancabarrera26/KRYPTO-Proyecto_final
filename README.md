# KRYPTO

**KRYPTO** es un lenguaje de programación de dominio específico con paradigma funcional, diseñado para ejecutar operaciones matemáticas, de álgebra lineal, aprendizaje automático y ciencia de datos directamente desde su propia sintaxis.

Implementado en Python 3 con ANTLR4 como motor de parsing. Todas las librerías internas (matemáticas, matrices, ML, DL, ciencia de datos, gráficas, archivos) están escritas desde cero en Python puro, sin dependencias externas más allá del runtime de ANTLR4.

---

## Tabla de contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
  - [Opción 1 — Instalación nativa](#opción-1--instalación-nativa)
  - [Opción 2 — Entorno virtual](#opción-2--entorno-virtual-recomendado)
  - [Regenerar la gramática](#regenerar-la-gramática-opcional)
- [Cómo ejecutar](#cómo-ejecutar)
- [Sintaxis del lenguaje](#sintaxis-del-lenguaje)
- [Librerías built-in](#librerías-built-in)
- [Ciencia de datos — KRYPTODS](#ciencia-de-datos--kryptods)
- [Por qué KRYPTO está orientado a IA y Data Science](#por-qué-krypto-está-orientado-a-ia-y-data-science)
- [Scripts de prueba explicados](#scripts-de-prueba-explicados)
- [Ejemplos de uso cotidiano](#ejemplos-de-uso-cotidiano)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Palabras clave reservadas](#palabras-clave-reservadas)

---

## Requisitos

| Componente             | Versión mínima                         |
| ---------------------- | -------------------------------------- |
| Python                 | 3.10+                                  |
| Java (JRE)             | 11+ — solo si se regenera la gramática |
| antlr4-python3-runtime | 4.13.1                                 |

En Debian / Ubuntu:

```
sudo apt update
sudo apt install python3 python3-pip python3-venv default-jre -y
```

---

## Instalación

### Opción 1 — Instalación nativa

```
git clone https://github.com/SebastianAcosta2006/KRYPTO-2
cd KRYPTO-2
pip install antlr4-python3-runtime==4.13.1
python3 main.py scripts/test_all.kr
```

### Opción 2 — Entorno virtual (recomendado)

Aísla la dependencia del sistema. No requiere permisos de administrador.

```
git clone https://github.com/SebastianAcosta2006/KRYPTO-2
cd KRYPTO-2

python3 -m venv .venv
source .venv/bin/activate

pip install antlr4-python3-runtime==4.13.1

python3 main.py scripts/test_all.kr
```

Para salir del entorno virtual:

```
deactivate
```

Para reactivarlo en sesiones futuras:

```
source .venv/bin/activate
```

> `.venv/` está en `.gitignore` y no se sube al repositorio.

O usa el script de setup incluido que hace todo en un paso:

```
bash setup.sh
```

### Regenerar la gramática (opcional)

Solo necesario si modificas los archivos `.g4` en `gramatica/`.

```
cd gramatica
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -no-listener KryptoLexer.g4
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -no-listener KryptoParser.g4
cd ..
```

---

## Cómo ejecutar

**Ejecutar un script `.kr`:**

```
python3 main.py scripts/mi_script.kr
```

**Shell interactivo (REPL):**

```
python3 repl.py
```

```
KRYPTO Shell v2.0  |  type exit() to quit
krypto> num x = 42;
krypto> kprint(x * 2);
84
krypto> exit()
```

---

## Sintaxis del lenguaje

KRYPTO usa palabras clave propias. Todo bloque de control termina con `stop`. Las sentencias terminan con `;`.

### Tipos de datos

| Palabra clave | Tipo            | Ejemplo                      |
| ------------- | --------------- | ---------------------------- |
| `num`         | Entero          | `num x = 10;`                |
| `dec`         | Decimal         | `dec pi = 3.14;`             |
| `logic`       | Booleano        | `logic activo = sisas;`      |
| `text`        | Cadena de texto | `text nombre = "KRYPTO";`    |
| `chain`       | Lista           | `chain nums = [1, 2, 3];`    |
| `grid`        | Matriz          | `grid M = [[1, 2], [3, 4]];` |

Los booleanos usan `sisas` (verdadero) y `nokas` (falso).

### Variables

La declaración de tipo es obligatoria al crear la variable. La reasignación no requiere tipo:

```
num edad = 25;
dec temperatura = 36.6;
text ciudad = "Bogotá";
logic conectado = nokas;

edad = 26;
ciudad = "Medellín";
```

### Operadores

**Aritméticos:** `+` `-` `*` `/` `%` `^`

**Comparación:** `==` `!=` `<` `>` `<=` `>=`

**Lógicos:** `&&` `||` `!`

### Condicionales

```
num nota = 75;

krif (nota >= 60) {
    kprint("Aprobado");
} krelse {
    kprint("Reprobado");
} stop
```

El bloque `krelse` es opcional.

### Ciclos

**While — `krloop`:**

```
num i = 1;
krloop (i <= 5) {
    kprint(i);
    i = i + 1;
} stop
```

**For — `krfor`:**

```
krfor (num j = 0; j < 10; j = j + 1) {
    kprint(j * j);
} stop
```

### Funciones

Se declaran con `krfunc` y retornan con `yield`. El bloque cierra con `stop`.

```
krfunc area_circulo(r) {
    yield 3.14159 * r * r;
} stop

kprint(area_circulo(5));
```

**Recursión:**

```
krfunc fibonacci(n) {
    krif (n <= 1) {
        yield n;
    } krelse {
        yield fibonacci(n - 1) + fibonacci(n - 2);
    } stop
} stop

kprint(fibonacci(10));
```

### Listas y matrices

```
chain precios = [120, 340, 89, 450, 220];
kprint(precios[0]);
kprint(bubble_sort(precios));

// Modificar por índice
precios[1] = 999;
kprint(precios);
```

Matrices:

```
grid A = [[1, 2], [3, 4]];
kprint(transpose(A));
kprint(determinant(A));
kprint(inverse(A));
```

### Archivos

```
kwrite("resultados.txt", "Experimento finalizado\n");

text contenido = kread("resultados.txt");
kprint(contenido);
```

### Gráficas ASCII

Renderiza directamente en terminal, sin librerías externas.

```
chain x = [-3, -2, -1, 0, 1, 2, 3];
chain y = [9, 4, 1, 0, 1, 4, 9];

k_title("Parabola y = x^2");
k_xlabel("x");
k_ylabel("y");
k_plot(x, y);
k_show();
```

---

## Librerías built-in

Todas implementadas desde cero en Python puro. No se importa ninguna librería externa en los módulos del lenguaje.

### KRYPTOMATH

| Función                       | Descripción                              | Algoritmo                     |
| ----------------------------- | ---------------------------------------- | ----------------------------- |
| `sqrt(x)`                     | Raíz cuadrada                            | Newton-Raphson                |
| `sin(x)` `cos(x)` `tan(x)`    | Trigonometría                            | Series de Taylor              |
| `asin(x)` `acos(x)` `atan(x)` | Inversas trigonométricas                 | Método de Newton              |
| `exp(x)`                      | e^x                                      | Taylor con reducción de rango |
| `ln(x)`                       | Logaritmo natural                        | Método de Halley              |
| `log(x, base)`                | Logaritmo en base arbitraria             | `ln(x) / ln(base)`            |
| `abs(x)`                      | Valor absoluto                           | —                             |
| `pow(base, exp)`              | Potencia general                         | Exponenciación por cuadrados  |
| `factorial(n)`                | Factorial                                | Recursión                     |
| `gcd(a, b)`                   | Máximo común divisor                     | Euclides iterativo            |
| `gcd_r(a, b)`                 | Máximo común divisor                     | Euclides recursivo            |
| `bubble_sort(lista)`          | Ordenamiento burbuja                     | —                             |
| `taylor_exp(x, n)`            | Polinomio de Taylor de e^x hasta grado n | —                             |
| `mean(lista)`                 | Media aritmética                         | —                             |
| `std_dev(lista)`              | Desviación estándar                      | —                             |

### KRYPTOMATRIX

| Función            | Descripción                                       |
| ------------------ | ------------------------------------------------- |
| `mat_add(A, B)`    | Suma                                              |
| `mat_sub(A, B)`    | Resta                                             |
| `mat_mul(A, B)`    | Multiplicación                                    |
| `mat_scalar(A, s)` | Producto por escalar                              |
| `transpose(A)`     | Transpuesta                                       |
| `determinant(A)`   | Determinante — eliminación LU con pivoteo parcial |
| `inverse(A)`       | Inversa — Gauss-Jordan                            |
| `mat_str(A)`       | Representación formateada                         |

### KRYPTOML

| Función                            | Descripción                                 |
| ---------------------------------- | ------------------------------------------- |
| `lin_train(X, y, lr, epochs)`      | Regresión lineal por gradiente descendente  |
| `lin_predict(X, w)`                | Predicción regresión lineal                 |
| `log_train(X, y, lr, epochs)`      | Regresión logística (sigmoide + GD)         |
| `log_predict(X, w)`                | Predicción regresión logística (clases 0/1) |
| `log_proba(X, w)`                  | Probabilidades brutas                       |
| `knn(X_train, y_train, X_test, k)` | K-Vecinos más cercanos                      |
| `kmeans(X, k, max_iter, seed)`     | K-Means con inicialización k-means++        |
| `accuracy(y_true, y_pred)`         | Exactitud                                   |
| `precision(y_true, y_pred)`        | Precisión                                   |
| `recall(y_true, y_pred)`           | Recall                                      |
| `confusion_matrix(y_true, y_pred)` | Matriz de confusión                         |

---

## Ciencia de datos — KRYPTODS

KRYPTODS es la librería de Data Science de KRYPTO. Permite cargar datasets desde CSV o Excel, realizar análisis exploratorio completo y visualizar distribuciones directamente en terminal, sin ninguna dependencia externa.

### Cargar datos

```
// Desde CSV
chain ds = kload("scripts/datos.csv");

// Desde Excel — ver sección "Conversión de Excel a CSV" abajo
```

### Inspección del dataset

```
kprint(kshape(ds));          // [filas, columnas]
kprint(kcolumns(ds));        // lista de nombres de columnas
khead(ds, 5);                // primeras 5 filas en tabla formateada
knulls(ds);                  // conteo de nulos por columna
```

### Estadísticas descriptivas

`kdescribe` calcula sobre todas las variables numéricas: count, mean, std, min, Q1, mediana, Q3, max.

```
kdescribe(ds);
```

Para un subconjunto de columnas:

```
chain sub = kselect(ds, ["col1", "col2", "col3"]);
kdescribe(sub);
```

### Boxplot

```
// Todas las variables numéricas
kboxplot_all(ds);

// Una variable específica
kboxplot(ds, "nombre_columna");
```

Cada boxplot muestra en ASCII: mínimo `|`, Q1–Q3 como bloque `===`, mediana `M`, máximo `|`, con los valores exactos debajo.

### Histograma

```
khistogram(ds, "nombre_columna");        // 10 bins por defecto
khistogram(ds, "nombre_columna", 20);    // bins personalizados
```

### Correlación de Pearson

```
kcorr(ds);
```

Imprime la matriz completa con valores entre -1 y +1. Aplica sobre todas las columnas numéricas del dataset.

### Frecuencias (variables categóricas)

```
kfreq(ds, "nombre_columna");
```

Imprime tabla ordenada por frecuencia descendente con conteo, porcentaje y barra proporcional.

### Selección de columnas

```
chain sub = kselect(ds, ["col_a", "col_b", "col_c"]);
```

Retorna un nuevo dataset con solo las columnas indicadas. Compatible con todas las demás funciones de KRYPTODS.

---

### Conversión de Excel a CSV

KRYPTO lee archivos Excel (`.xlsx`) directamente sin dependencias externas, parseando el formato ZIP+XML del estándar OOXML con la stdlib de Python.

**Listar las hojas disponibles en un Excel:**

```
kexcel_sheets("scripts/datos.xlsx");
```

**Convertir la primera hoja a CSV (mismo nombre, extensión `.csv`):**

```
kexcel_to_csv("scripts/datos.xlsx");
```

**Especificar ruta de salida:**

```
kexcel_to_csv("scripts/datos.xlsx", "scripts/datos.csv");
```

**Convertir una hoja específica por nombre:**

```
kexcel_to_csv("scripts/datos.xlsx", "scripts/datos.csv", "Hoja1");
```

**Convertir una hoja por índice (0 = primera):**

```
kexcel_to_csv("scripts/datos.xlsx", "scripts/datos.csv", 0);
```

**Flujo completo: Excel → CSV → EDA:**

```
kexcel_to_csv("scripts/ventas.xlsx", "scripts/ventas.csv", "Enero");
chain ds = kload("scripts/ventas.csv");
kshape(ds);
kdescribe(ds);
kboxplot_all(ds);
```

El conversor maneja los tres tipos de celda del formato OOXML: cadenas inline (`inlineStr`), cadenas compartidas (`sharedStrings`) y valores numéricos. Las celdas vacías quedan como campo vacío en el CSV. Soporta caracteres especiales y tildes (UTF-8).

### Referencia completa — KRYPTODS

| Función | Parámetros | Descripción |
| --- | --- | --- |
| `kload` | `path` | Carga CSV, retorna dataset |
| `kshape` | `ds` | `[filas, columnas]` |
| `kcolumns` | `ds` | Lista de nombres de columnas |
| `khead` | `ds, n` | Primeras n filas en tabla |
| `knulls` | `ds` | Nulos por columna |
| `kdescribe` | `ds` | Estadísticas descriptivas numéricas |
| `kselect` | `ds, cols` | Subconjunto de columnas |
| `kboxplot` | `ds, col` | Boxplot ASCII de una columna |
| `kboxplot_all` | `ds` | Boxplot ASCII de todas las columnas numéricas |
| `khistogram` | `ds, col [, bins]` | Histograma ASCII |
| `kcorr` | `ds` | Matriz de correlación de Pearson |
| `kfreq` | `ds, col` | Tabla de frecuencias categóricas |
| `kexcel_sheets` | `path` | Lista hojas de un archivo `.xlsx` |
| `kexcel_to_csv` | `path [, csv_path [, sheet]]` | Convierte hoja de Excel a CSV |

---

## Por qué KRYPTO está orientado a IA y Data Science

KRYPTO fue diseñado con ML y análisis de datos como ciudadanos de primera clase, no como módulos externos.

**1. Tipos nativos para álgebra lineal**

`chain` y `grid` son tipos primitivos del lenguaje. Todas las operaciones de matrices están disponibles sin convertir tipos ni importar nada.

```
grid pesos = [[0.1, 0.4], [0.3, 0.2]];
grid entrada = [[1], [0]];
kprint(mat_mul(pesos, entrada));
```

**2. Pipeline de ML completo dentro del lenguaje**

Entrenamiento, predicción y evaluación se escriben íntegramente en KRYPTO:

```
chain X = [[1], [2], [3], [4], [5]];
chain y = [2, 4, 6, 8, 10];

chain w = lin_train(X, y, 0.01, 2000);
chain pred = lin_predict([[6], [7]], w);
kprint(pred);
```

**3. EDA completo desde el lenguaje**

Carga, inspección, estadísticas, correlaciones y visualizaciones se invocan con funciones nativas. No se necesita Python externo ni notebooks:

```
chain ds = kload("datos.csv");
kdescribe(ds);
kboxplot_all(ds);
kcorr(ds);
```

**4. Matemáticas de precisión sin numpy**

Exponencial, logaritmo, trigonometría y raíces implementados con Newton-Raphson, Halley y series de Taylor. Precisión de 15 decimales sin depender de extensiones en C.

**5. Visualización integrada en terminal**

Las gráficas ASCII permiten inspeccionar datos y resultados en cualquier entorno, incluyendo servidores remotos o entornos sin interfaz gráfica.

**6. Perceptrón multicapa implementado desde cero**

El MLP con backpropagation, ReLU, sigmoide, inicialización Xavier y descenso por gradiente está en `KRYPTOML.py` sin ninguna dependencia. Es directamente invocable desde el lenguaje.

---

## Scripts de prueba explicados

### `test_all.kr` — Sintaxis base

```
python3 main.py scripts/test_all.kr
```

Verifica en orden: aritmética, booleanos, `krloop`, `krfor`, funciones, recursión (factorial), funciones matemáticas built-in, listas con `bubble_sort`, operaciones de matrices, y archivos.

Salida esperada (extracto):

```
13        ← 10 + 3
720       ← factorial(6)
4         ← sqrt(16)
[1, 3, 4, 7, 9, 10]   ← bubble_sort([10, 3, 7, 1, 9, 4])
-2        ← determinant([[1,2],[3,4]])
KRYPTO file test
```

### `test_math.kr` — Módulo matemático

```
python3 main.py scripts/test_math.kr
```

Trigonometría, exponencial, logaritmos en distintas bases, potencias, factorial, GCD, Taylor, estadística.

```
2.7182818284590455    ← exp(1) = e
2.0000000000000004    ← log(100, 10)
3628800               ← factorial(10)
[1, 2, 3, 5, 8, 9]   ← bubble_sort
```

### `test_matrices.kr` — Álgebra lineal

```
python3 main.py scripts/test_matrices.kr
```

Suma, resta, multiplicación, escalar, transpuesta, determinante, inversa. El test final calcula `A * inverse(A)` y verifica que sea la identidad. Los valores `~1e-16` son error de punto flotante de 64 bits, matemáticamente equivalentes a 0.

### `test_ml_graf.kr` — Machine Learning y gráficas

```
python3 main.py scripts/test_ml_graf.kr
```

Gráfica ASCII de una parábola. Regresión lineal sobre y = 2x+1 con pesos entrenados prácticamente exactos (`[1.0, 2.0]`). Regresión logística con accuracy=1.0. KNN y K-Means con clusters bien separados.

```
LR weights [bias, slope]:
[0.9999999999999762, 2.0000000000000084]

kmeans labels:
[[[1.33, 1.33], [8.33, 8.33]], [0, 0, 0, 1, 1, 1]]
```

### `test_ds.kr` — Ciencia de datos

```
python3 main.py scripts/test_ds.kr
```

EDA completo sobre un dataset CSV: shape, columnas, head, nulos, estadísticas descriptivas, boxplots de todas las variables, histograma, correlación de Pearson y frecuencias categóricas. Incluye también ejemplo de selección de subconjunto de columnas.

Requiere un CSV en `scripts/`. Para usar el dataset Iris de ejemplo:

```
curl -o scripts/iris.csv https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv
python3 main.py scripts/test_ds.kr
```

---

## Ejemplos de uso cotidiano

### 1. Interés compuesto

```
krfunc interes_compuesto(capital, tasa, anos) {
    yield capital * pow(1 + tasa, anos);
} stop

kprint(interes_compuesto(1000000, 0.08, 10));
```

### 2. Verificador de número primo

```
krfunc es_primo(n) {
    krif (n < 2) { yield nokas; } stop
    num i = 2;
    krloop (i * i <= n) {
        krif (n % i == 0) { yield nokas; } stop
        i = i + 1;
    } stop
    yield sisas;
} stop

krif (es_primo(97)) {
    kprint("Es primo");
} krelse {
    kprint("No es primo");
} stop
```

### 3. Estadísticas de ventas

```
chain ventas = [1200, 980, 1450, 1100, 870, 1600, 1320, 990, 1080, 1410];

kprint(mean(ventas));
kprint(std_dev(ventas));
kprint(bubble_sort(ventas));
```

### 4. Visualizar tendencia de datos

```
chain meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
chain ingresos = [800, 920, 870, 1050, 1200, 1150, 1300, 1280, 1400, 1380, 1500, 1600];

k_title("Ingresos mensuales");
k_xlabel("Mes");
k_ylabel("COP miles");
k_plot(meses, ingresos);
k_show();
```

### 5. Predecir precio con regresión lineal

```
chain metros = [[40], [60], [80], [100], [120], [150]];
chain precios = [120, 180, 240, 300, 360, 450];

chain modelo = lin_train(metros, precios, 0.001, 5000);
kprint(lin_predict([[90]], modelo));
kprint(lin_predict([[200]], modelo));
```

### 6. Clasificar con KNN

```
chain X_train = [[2, 5], [3, 6], [1, 4], [7, 7], [8, 8], [6, 7], [9, 6]];
chain y_train = [0, 0, 0, 1, 1, 1, 1];

chain resultado = knn(X_train, y_train, [[4, 5], [7, 6]], 3);
kprint(resultado);
```

### 7. Agrupar clientes por comportamiento

```
chain clientes = [[1, 50], [2, 60], [1, 45],
                  [10, 500], [12, 480], [9, 510],
                  [5, 200], [6, 220], [5, 190]];

chain grupos = kmeans(clientes, 3, 300, 42);
kprint(grupos[0]);
kprint(grupos[1]);
```

### 8. EDA desde Excel

```
kexcel_to_csv("scripts/reporte.xlsx", "scripts/reporte.csv", "Datos");
chain ds = kload("scripts/reporte.csv");
kdescribe(ds);
kboxplot_all(ds);
kcorr(ds);
```

### 9. Resolver sistema de ecuaciones

```
grid A = [[2, 1], [1, 3]];
grid b = [[5], [10]];

kprint(mat_mul(inverse(A), b));
```

### 10. Fibonacci iterativo vs recursivo

```
krfunc fib_r(n) {
    krif (n <= 1) { yield n; } stop
    yield fib_r(n - 1) + fib_r(n - 2);
} stop

krfunc fib_i(n) {
    krif (n <= 1) { yield n; } stop
    num a = 0;
    num b = 1;
    num i = 2;
    krloop (i <= n) {
        num temp = a + b;
        a = b;
        b = temp;
        i = i + 1;
    } stop
    yield b;
} stop

kprint(fib_r(10));
kprint(fib_i(10));
```

---

## Estructura del proyecto

```
KRYPTO/
├── gramatica/
│   ├── KryptoLexer.g4              # Gramática léxica
│   ├── KryptoParser.g4             # Gramática sintáctica
│   ├── KryptoLexer.py              # Generado por ANTLR4
│   ├── KryptoParser.py             # Generado por ANTLR4
│   └── KryptoParserVisitor.py      # Generado por ANTLR4
├── librerias/
│   ├── KRYPTOMATH.py               # Funciones matemáticas puras
│   ├── KRYPTOMATRIX.py             # Álgebra lineal
│   ├── KRYPTOML.py                 # Machine Learning
│   ├── KRYPTODL.py                 # Deep Learning (MLP)
│   ├── KRYPTODS.py                 # Ciencia de datos y EDA
│   ├── KRYPTOGRAF.py               # Gráficas ASCII (Bresenham)
│   └── KRYPTOarchivos.py           # I/O de archivos
├── scripts/
│   ├── test_all.kr                 # Test de sintaxis completa
│   ├── test_math.kr                # Test KRYPTOMATH
│   ├── test_matrices.kr            # Test KRYPTOMATRIX
│   ├── test_ml_graf.kr             # Test ML y gráficas
│   └── test_ds.kr                  # Test ciencia de datos y EDA
├── interpreter.py                  # Visitor del AST
├── main.py                         # Punto de entrada
├── repl.py                         # Shell interactivo
├── setup.sh                        # Setup automático
└── antlr-4.13.1-complete.jar
```

---

## Palabras clave reservadas

| Token KRYPTO | Equivalente          |
| ------------ | -------------------- |
| `krif`       | `if`                 |
| `krelse`     | `else`               |
| `krloop`     | `while`              |
| `krfor`      | `for`                |
| `krfunc`     | `def` / `function`   |
| `yield`      | `return`             |
| `stop`       | cierre de bloque     |
| `sisas`      | `true`               |
| `nokas`      | `false`              |
| `kprint`     | `print`              |
| `kread`      | lectura de archivo   |
| `kwrite`     | escritura de archivo |
| `num`        | `int`                |
| `dec`        | `float`              |
| `logic`      | `bool`               |
| `text`       | `string`             |
| `chain`      | lista                |
| `grid`       | matriz               |

---

## Comentarios

```
// Comentario de una línea

/* Comentario
   de bloque */
```
