# Guía de Pruebas y Preparación para la Sustentación - KRYPTO

## 1. Ingresar al proyecto

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

## 3. Verificar Python

```bash
python3 --version
```

---

## 4. Instalar dependencias

```bash
pip install antlr4-python3-runtime==4.13.1
pip install numpy pandas matplotlib scikit-learn seaborn
```

---

# PRUEBAS DEL LENGUAJE KRYPTO

## 5. Test General

Ejecuta:

```bash
python3 main.py scripts/test_all.kr
```

Debe validar:

* Variables
* Funciones
* Recursión
* Listas
* Ordenamiento
* Matrices
* Manejo de archivos

Resultados esperados:

```text
720
2.718281828...
[1, 3, 4, 7, 9, 10]
[[19, 22], [43, 50]]
KRYPTO file test
```

---

## 6. Pruebas Matemáticas

```bash
python3 main.py scripts/test_math.kr
```

Repasar:

* Factorial
* Potencias
* Logaritmos
* Exponenciales
* Aproximaciones numéricas

---

## 7. Pruebas de Matrices

```bash
python3 main.py scripts/test_matrices.kr
```

Repasar:

* Suma de matrices
* Multiplicación de matrices
* Determinantes
* Transpuestas

---

## 8. Pruebas de Machine Learning

```bash
python3 main.py scripts/test_ml_graf.kr
```

Debe probar:

### Regresión Lineal

Conceptos:

* Pendiente
* Intercepto
* Predicción
* Error

---

### Regresión Logística

Conceptos:

* Clasificación binaria
* Función sigmoide
* Accuracy

---

### KNN

Conceptos:

* Distancia euclidiana
* Vecinos cercanos
* Clasificación

---

### KMeans

Conceptos:

* Clustering
* Centroides
* Agrupamiento

---

## 9. Pruebas de Deep Learning

```bash
python3 main.py scripts/test_dl.kr
```

Repasar:

* Neuronas
* Pesos
* Bias
* Forward propagation
* Backpropagation
* Entrenamiento

---

## 10. REPL Interactivo

Iniciar:

```bash
python3 repl.py
```

Pruebas:

```krypto
num x = 10;

kprint(x);

kprint(x * 5);
```

Salir:

```krypto
exit();
```

---

# ARQUITECTURA DEL PROYECTO

## Flujo de ejecución

```text
Código KRYPTO (.kr)
        │
        ▼
Lexer (KryptoLexer.g4)
        │
        ▼
Tokens
        │
        ▼
Parser (KryptoParser.g4)
        │
        ▼
Parse Tree
        │
        ▼
Visitor
        │
        ▼
Interpreter
        │
        ▼
Resultado
```

---

## Componentes importantes

### Lexer

Archivo:

```text
gramatica/KryptoLexer.g4
```

Responsabilidad:

* Reconocer tokens
* Identificadores
* Números
* Operadores
* Palabras reservadas

---

### Parser

Archivo:

```text
gramatica/KryptoParser.g4
```

Responsabilidad:

* Validar sintaxis
* Construir árbol sintáctico

---

### Visitor

Archivo generado por ANTLR:

```text
KryptoParserVisitor.py
```

Responsabilidad:

* Recorrer el árbol sintáctico

---

### Intérprete

Archivo:

```text
interpreter.py
```

Responsabilidad:

* Ejecutar instrucciones
* Manejar variables
* Manejar funciones
* Ejecutar operaciones matemáticas
* Ejecutar ML y DL

---

# PREGUNTAS PROBABLES DEL PROFESOR

## Compiladores e Intérpretes

* ¿Qué es ANTLR?
* ¿Qué es un Lexer?
* ¿Qué es un Parser?
* ¿Qué es un Token?
* ¿Qué es un Parse Tree?
* ¿Qué es el patrón Visitor?
* ¿Qué diferencia hay entre compilador e intérprete?

---

## Lenguaje KRYPTO

* ¿Cómo se declara una variable?
* ¿Cómo funcionan las funciones?
* ¿Cómo funciona el scope?
* ¿Cómo se manejan los tipos?
* ¿Cómo se ejecuta una sentencia?

---

## Matemáticas

* ¿Cómo se calcula un factorial?
* ¿Cómo funciona una aproximación numérica?
* ¿Qué es convergencia?
* ¿Qué es error numérico?

---

## Matrices

* ¿Cómo se multiplican matrices?
* ¿Qué es un determinante?
* ¿Qué es una matriz transpuesta?

---

## Machine Learning

### Regresión Lineal

* ¿Qué predice?
* ¿Cómo aprende?
* ¿Qué representa la pendiente?

### Regresión Logística

* ¿Qué es clasificación binaria?
* ¿Qué es la función sigmoide?

### KNN

* ¿Qué representa K?
* ¿Cómo se calculan vecinos?

### KMeans

* ¿Qué es un centroide?
* ¿Cómo se forman los clusters?

---

## Deep Learning

* ¿Qué es una neurona artificial?
* ¿Qué son pesos y bias?
* ¿Qué es forward propagation?
* ¿Qué es backpropagation?
* ¿Qué es una función de activación?

---

# ANÁLISIS EXPLORATORIO DE DATOS (EDA)

## Cargar dataset

```python
import pandas as pd

df = pd.read_csv("scripts/data.csv")
```

---

## Información general

```python
print(df.shape)
print(df.info())
print(df.describe())
```

---

## Valores nulos

```python
print(df.isnull().sum())
```

---

## Variables del dataset

```python
print(df.columns)
```

---

## Histogramas

```python
df.hist(figsize=(15,10))
```

---

## Correlaciones

```python
corr = df.corr(numeric_only=True)

print(corr)
```

---

## Heatmap

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(corr, annot=True)

plt.show()
```

---

## Boxplots de todas las variables

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("scripts/data.csv")

for col in df.select_dtypes(include='number').columns:
    plt.figure(figsize=(6,3))
    sns.boxplot(x=df[col])
    plt.title(col)
    plt.show()
```

---

# Checklist final antes de la sustentación

* [ ] test_all.kr ejecuta correctamente
* [ ] test_math.kr ejecuta correctamente
* [ ] test_matrices.kr ejecuta correctamente
* [ ] test_ml_graf.kr ejecuta correctamente
* [ ] test_dl.kr ejecuta correctamente
* [ ] REPL funciona
* [ ] Entiendo Lexer
* [ ] Entiendo Parser
* [ ] Entiendo Visitor
* [ ] Entiendo Interpreter
* [ ] Entiendo Regresión Lineal
* [ ] Entiendo Regresión Logística
* [ ] Entiendo KNN
* [ ] Entiendo KMeans
* [ ] Entiendo Redes Neuronales
* [ ] Conozco todas las variables del dataset
* [ ] Tengo boxplots de todas las variables
* [ ] Tengo análisis exploratorio completo

```
```
