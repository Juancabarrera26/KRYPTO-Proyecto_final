"""
KRYPTO Engine - main entry point.
Usage: python3 main.py [script.kr]
       python3 main.py          (prompts for filename)
"""

import sys
import os

from antlr4 import InputStream, CommonTokenStream

from gramatica.KryptoLexer   import KryptoLexer
from gramatica.KryptoParser  import KryptoParser
from interpreter             import KryptoInterpreter
from librerias.KRYPTOarchivos import cargar_fuente_krypto


def run(path):
    if not os.path.exists(path):
        print(f"[KRYPTO] File not found: '{path}'")
        sys.exit(1)

    source       = cargar_fuente_krypto(path)
    input_stream = InputStream(source)
    lexer        = KryptoLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser       = KryptoParser(token_stream)
    tree         = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"[KRYPTO] Syntax errors found. Aborting.")
        sys.exit(1)

    engine = KryptoInterpreter()
    engine.visit(tree)


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Script (.kr): ").strip()
        if not filename.endswith('.kr'):
            filename += '.kr'
        filename = os.path.join('scripts', filename)

    run(filename)


if __name__ == '__main__':
    main()