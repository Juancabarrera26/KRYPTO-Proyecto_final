# Instalación y Verificación del Proyecto KRYPTO

---

## 1. Actualizar sistema

```bash
sudo apt update
```

---

## 2. Instalar dependencias base

```bash
sudo apt install -y \
git \
python3 \
python3-pip \
python3-venv \
default-jre
```

Verificar:

```bash
python3 --version
java --version
```

---

## 3. Clonar repositorio

```bash
git clone https://github.com/Juancabarrera26/KRYPTO-Proyecto_final.git
```

Entrar al proyecto:

```bash
cd KRYPTO-Proyecto_final
```

---

## 4. Crear entorno virtual

```bash
python3 -m venv .venv
```

---

## 5. Activar entorno virtual

```bash
source .venv/bin/activate
```

Debe aparecer:

```text
(.venv)
```

al inicio de la terminal.

---

## 6. Instalar ANTLR Runtime

```bash
pip install antlr4-python3-runtime==4.13.1
```

---

## 7. Verificar instalación

Verificar Python:

```bash
python --version
```

Ejemplo:

```text
Python 3.12.3
```

o

```text
Python 3.13.x
```

Verificar ANTLR:

```bash
pip show antlr4-python3-runtime
```

Debe aparecer:

```text
Name: antlr4-python3-runtime
Version: 4.13.1
```

---

# Verificación del Proyecto

## Verificar estructura

```bash
ls
```

Debe existir algo similar a:

```text
gramatica
librerias
scripts
main.py
interprete.py
repl.py
README.md
```

---

## Verificar scripts

```bash
ls scripts
```

Debe aparecer:

```text
data.csv
data.xlsx
eda_data.kr
graficas_data.kr
test_all.kr
test_dl.kr
test_math.kr
test_matrices.kr
test_ml_graf.kr
```

---

# Pruebas Funcionales

## 1. Prueba general del lenguaje

```bash
python3 main.py scripts/test_all.kr
```

Validación:

* Lexer
* Parser
* ANTLR
* Visitor
* Intérprete

Si aparece:

```text
KRYPTO file test
```

la prueba fue exitosa.

---

## 2. Prueba de Matemáticas

```bash
python3 main.py scripts/test_math.kr
```

---

## 3. Prueba de Matrices

```bash
python3 main.py scripts/test_matrices.kr
```

---

## 4. Prueba de Machine Learning

```bash
python3 main.py scripts/test_ml_graf.kr
```

---

## 5. Prueba de Deep Learning

```bash
python3 main.py scripts/test_dl.kr
```

---

## 6. Prueba EDA

```bash
python3 main.py scripts/eda_data.kr
```

Debe mostrar:

* Shape
* Columns
* Head
* Nulls
* Describe
* Frecuencias
* Histogramas
* Correlaciones

---

## 7. Prueba de Gráficas

```bash
python3 main.py scripts/graficas_data.kr
```

Debe generar las gráficas ASCII del dataset.

---

# Probar REPL

Ejecutar:

```bash
python3 repl.py
```

Debe aparecer:

```text
KRYPTO Shell v2.0 | type exit() to quit
```

Salir con:

```text
exit()
```

---

# Comprobación Final

Si funcionan correctamente:

```bash
python3 main.py scripts/test_all.kr

python3 main.py scripts/test_math.kr

python3 main.py scripts/test_matrices.kr

python3 main.py scripts/test_ml_graf.kr

python3 main.py scripts/test_dl.kr

python3 main.py scripts/eda_data.kr

python3 main.py scripts/graficas_data.kr

python3 repl.py
```

entonces el proyecto KRYPTO quedó instalado y validado correctamente.
