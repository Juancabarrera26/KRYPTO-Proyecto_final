"""
KRYPTOarchivos - File I/O for KRYPTO language.
Uses only Python built-in open().
"""


def cargar_fuente_krypto(path):
    #Read a .kr source file and return its content as a string.
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def read_file(path):
    """
    Read a text file and return its content as a single string.
    Called via kread("path") in KRYPTO scripts.
    """
    with open(str(path), 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    """
    Write content to a text file (overwrites if exists).
    Called via kwrite("path", value) in KRYPTO scripts.
    """
    with open(str(path), 'w', encoding='utf-8') as f:
        f.write(str(content))


def append_file(path, content):
    """Append content to a text file."""
    with open(str(path), 'a', encoding='utf-8') as f:
        f.write(str(content))