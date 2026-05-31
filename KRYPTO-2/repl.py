"""
KRYPTO REPL - Interactive shell.
Usage: python3 repl.py
"""

from antlr4 import InputStream, CommonTokenStream

from gramatica.KryptoLexer  import KryptoLexer
from gramatica.KryptoParser import KryptoParser
from interpreter            import KryptoInterpreter


def main():
    print("KRYPTO Shell v2.0  |  type exit() to quit")
    interpreter = KryptoInterpreter()

    while True:
        try:
            line = input("krypto> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if line.lower() in ('exit()', 'quit', 'salir'):
            break
        if not line:
            continue

        try:
            stream = InputStream(line)
            lexer  = KryptoLexer(stream)
            tokens = CommonTokenStream(lexer)
            parser = KryptoParser(tokens)
            tree   = parser.program()
            if parser.getNumberOfSyntaxErrors() == 0:
                interpreter.visit(tree)
            else:
                print("[KRYPTO] Syntax error.")
        except Exception as e:
            print(f"[KRYPTO Error] {e}")


if __name__ == '__main__':
    main()