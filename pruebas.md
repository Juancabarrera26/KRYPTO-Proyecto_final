# EDA - Ejecución y Validación para la Sustentación

## 1. Entrar al proyecto

```bash
cd ~/KRYPTO-Proyecto_final
```

---

## 2. Activar entorno virtual

```bash
source .venv/bin/activate
```

Si no existe:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Verificar archivos necesarios

```bash
ls scripts
```

Debe existir:

```text
data.csv
data.xlsx
eda_data.kr
```

---

## 4. Ejecutar Análisis Exploratorio Completo

```bash
python3 main.py scripts/eda_data.kr
```

---

# Resultados que deben aparecer

## 1. Shape

```text
SHAPE
```

Permite conocer:

* Número de filas
* Número de columnas

---

## 2. Columns

```text
COLUMNS
```

Permite conocer:

* Variables disponibles
* Nombres de columnas

---

## 3. Head

```text
HEAD
```

Muestra:

* Primeros registros
* Estructura del dataset

---

## 4. Nulls

```text
NULLS
```

Permite identificar:

* Valores faltantes
* Calidad de datos

---

## 5. Describe

```text
DESCRIBE
```

Estadísticas descriptivas:

* Media
* Mediana
* Mínimo
* Máximo
* Desviación estándar

---

## 6. Frecuencias

```text
FRECUENCIAS
```

Permite analizar:

* Variables categóricas
* Distribución de categorías

---

## 7. Histogramas

```text
HISTOGRAMA
```

Permite analizar:

* Distribución de variables
* Concentración de datos
* Posibles sesgos

---

## 8. Correlación

```text
CORRELACION
```

Permite identificar:

* Relaciones entre variables
* Dependencias positivas
* Dependencias negativas

---

## 9. Boxplots

```text
BOXPLOT
```

Permite identificar:

* Outliers
* Dispersión
* Rango intercuartílico

---

# Variables que se deben conocer

Antes de la sustentación revisar:

```text
edad
sexo
ingreso_mensual
anos_esc
```

o las variables reales que aparezcan en:

```text
COLUMNS
```

Debe conocerse:

* Qué representa cada variable
* Tipo de dato
* Rango de valores
* Posibles outliers

---

# Comandos de Validación Adicional

## Machine Learning

```bash
python3 main.py scripts/test_ml_graf.kr
```

Valida:

* Regresión Lineal
* Regresión Logística
* KNN
* KMeans

---

## Deep Learning

```bash
python3 main.py scripts/test_dl.kr
```

Valida:

* Redes neuronales
* Forward Propagation
* Backpropagation

```
```
