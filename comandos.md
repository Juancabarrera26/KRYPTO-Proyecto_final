# Guía de Ejecución KRYPTO

```bash
cd KRYPTO-Proyecto_final

python3 -m venv .venv

source .venv/bin/activate

pip install antlr4-python3-runtime==4.13.1

python3 main.py scripts/test_all.kr

python3 main.py scripts/eda_data.kr

python3 main.py scripts/graficas_data.kr
```
---

# 1. Entrar al proyecto

```bash
cd ~/KRYPTO-Proyecto_final
```

---

# 2. Activar entorno virtual

```bash
source .venv/bin/activate
```

Debe aparecer algo similar a:

```text
(.venv) vboxuser@ubuntu:~/KRYPTO-Proyecto_final$
```

---

# 3. Verificar archivos disponibles

```bash
ls scripts
```

Deben existir archivos similares a:

```text
data.csv
data.xlsx
eda_data.kr
graficas_data.kr
output.txt
test_all.kr
test_dl.kr
test_math.kr
test_matrices.kr
test_ml_graf.kr
```

---

# 4. Ejecutar Análisis Exploratorio de Datos (EDA)

```bash
python3 main.py scripts/eda_data.kr
```

---

## Resultados esperados

### SHAPE

```text
=== SHAPE ===
```

Muestra:

* Número de filas
* Número de columnas

---

### COLUMNS

```text
=== COLUMNS ===
```

Variables observadas en el video:

```text
id
edad
nivel_edu
ingreso_mensual
sex
anios_esc
```

---

### HEAD

```text
=== HEAD ===
```

Muestra las primeras filas del dataset.

---

### NULLS

```text
=== NULLS ===
```

Permite identificar valores faltantes.

---

### DESCRIBE

```text
=== DESCRIBE ===
```

Muestra:

* count
* mean
* std
* min
* Q1
* median
* Q3
* max

---

### FRECUENCIAS

```text
=== FRECUENCIAS ===
```

Frecuencias de variables categóricas.

En el video se observan:

```text
nivel_edu
sex
```

---

### HISTOGRAMAS

```text
=== HISTOGRAMA ===
```

Variables observadas:

```text
edad
ingreso_mensual
anios_esc
```

---

### CORRELACIÓN

```text
=== CORRELACION ===
```

Correlación entre variables numéricas.

---

### SUBCONJUNTO

```text
=== SUBCONJUNTO ===
```

Variables observadas:

```text
edad
ingreso_mensual
anios_esc
```

---

### BOXPLOTS

El script genera:

```text
kboxplot_all(...)
```

y boxplots individuales para:

```text
edad
ingreso_mensual
anios_esc
```

Permiten identificar:

* Outliers
* Dispersión
* Rango intercuartílico

---

# 5. Ejecutar Gráficas

```bash
python3 main.py scripts/graficas_data.kr
```

---

## Gráficas esperadas

### Distribución de Edad

Gráfica ASCII de la variable edad.

---

### Distribución de Ingreso

Gráfica ASCII de la variable ingreso mensual.

---

### Ingreso Promedio por Años de Escolaridad

Debe aparecer una gráfica similar a:

```text
Ingreso Promedio por Años de Escolaridad
```

Donde:

* Eje X = años de escolaridad
* Eje Y = ingreso promedio

---

# Verificación rápida antes de la sustentación

Ejecutar:

```bash
cd ~/KRYPTO-Proyecto_final

source .venv/bin/activate

python3 main.py scripts/eda_data.kr

python3 main.py scripts/graficas_data.kr
```

Si ambos comandos ejecutan correctamente y generan resultados similares a los mostrados en el video, el módulo EDA queda validado.

---

# Posibles preguntas del profesor

## Dataset

* ¿Cuántas filas tiene el dataset?
* ¿Cuántas columnas tiene?
* ¿Qué representa cada variable?
* ¿Existen valores nulos?
* ¿Qué variable tiene mayor dispersión?

---

## Estadística

* ¿Qué representa la media?
* ¿Qué representa la mediana?
* ¿Qué representa la desviación estándar?
* ¿Qué información aporta un boxplot?

---

## Correlación

* ¿Qué es una correlación positiva?
* ¿Qué es una correlación negativa?
* ¿Qué significa una correlación cercana a cero?

---

# Variables que deben conocerse

Variables observadas en la demostración:

```text
id
edad
nivel_edu
ingreso_mensual
sex
anios_esc
```

Variables principales para explicar:

```text
edad
ingreso_mensual
anios_esc
```

porque aparecen en:

* Histogramas
* Correlaciones
* Boxplots
* Gráficas finales

---

# Comprobación final

Antes de la sustentación ejecutar:

```bash
cd ~/KRYPTO-Proyecto_final

source .venv/bin/activate

ls scripts

python3 main.py scripts/eda_data.kr

python3 main.py scripts/graficas_data.kr
```

Si estos comandos funcionan correctamente en Ubuntu, estarás reproduciendo el mismo flujo mostrado en la demostración observada.
