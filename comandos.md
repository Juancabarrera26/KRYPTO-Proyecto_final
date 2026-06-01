# Guía de Ejecución EDA y Gráficas - KRYPTO

## Objetivo

Ejecutar el análisis exploratorio de datos (EDA) y las gráficas del dataset para la sustentación.

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

Verificar que aparezca algo similar a:

```text
(.venv) usuario@ubuntu:~/KRYPTO-Proyecto_final$
```

---

# 3. Verificar archivos disponibles

```bash
ls scripts
```

Debe aparecer algo parecido a:

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

# 4. Ejecutar Análisis Exploratorio Completo (EDA)

```bash
python3 main.py scripts/eda_data.kr
```

---

## Salidas esperadas

### Shape

```text
=== SHAPE ===
(10280, 6)
```

Muestra:

* Número de filas
* Número de columnas

---

### Columns

```text
=== COLUMNS ===
```

Variables del dataset:

```text
id
edad
nivel_edu
ingreso_mensual
sex
anios_esc
```

---

### Head

```text
=== HEAD ===
```

Muestra las primeras filas del dataset.

---

### Nulls

```text
=== NULLS ===
```

Permite verificar valores faltantes.

---

### Describe

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

### Frecuencias

```text
=== FRECUENCIAS ===
```

Frecuencia de:

* nivel_edu
* sex

---

### Histogramas

```text
=== HISTOGRAMA ===
```

Variables:

* edad
* ingreso_mensual
* anios_esc

---

### Correlación

```text
=== CORRELACION ===
```

Correlación de Pearson entre variables numéricas.

---

### Subconjunto

```text
=== SUBCONJUNTO ===
```

Variables:

```text
edad
ingreso_mensual
anios_esc
```

---

# 5. Ejecutar gráficas

```bash
python3 main.py scripts/graficas_data.kr
```

---

## Gráficas esperadas

### Distribución de Edad

Debe aparecer una gráfica ASCII de edad.

---

### Distribución de Ingreso

Debe aparecer una gráfica ASCII de ingreso mensual.

---

### Ingreso Promedio por Años de Escolaridad

Debe aparecer una gráfica similar a:

```text
Ingreso Promedio por Años de Escolaridad
```

donde:

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

Si ambos comandos funcionan correctamente, el módulo de análisis exploratorio mostrado en el video quedó validado.

---

# Posibles preguntas del profesor

## Dataset

* ¿Cuántas filas tiene el dataset?
* ¿Cuántas columnas tiene?
* ¿Qué representa cada variable?
* ¿Existen valores nulos?
* ¿Cuál variable tiene mayor dispersión?

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

## Dataset utilizado

Variables observadas:

```text
id
edad
nivel_edu
ingreso_mensual
sex
anios_esc
```

Variables clave para explicar:

```text
edad
ingreso_mensual
anios_esc
```

porque son las que aparecen en histogramas, correlaciones y gráficas.
