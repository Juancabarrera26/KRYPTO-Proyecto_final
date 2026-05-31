"""
KRYPTOMATRIX - Pure Python matrix operations for KRYPTO language.
Matrices are represented as list-of-lists: M[row][col].
No external imports.
"""


#VALIDATION

def _shape(M):
    rows = len(M)
    cols = len(M[0]) if rows else 0
    return rows, cols


def _check_same_shape(A, B, op):
    rA, cA = _shape(A)
    rB, cB = _shape(B)
    if rA != rB or cA != cB:
        raise ValueError(f"matrix_{op}: incompatible shapes ({rA}x{cA}) vs ({rB}x{cB})")


def _zeros(rows, cols):
    return [[0.0] * cols for _ in range(rows)]


def _identity(n):
    M = _zeros(n, n)
    for i in range(n):
        M[i][i] = 1.0
    return M


def _copy(M):
    return [row[:] for row in M]


#BASIC OPERATIONS

def mat_add(A, B):
    _check_same_shape(A, B, "add")
    rows, cols = _shape(A)
    return [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]


def mat_sub(A, B):
    _check_same_shape(A, B, "sub")
    rows, cols = _shape(A)
    return [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]


def mat_mul(A, B):
    rA, cA = _shape(A)
    rB, cB = _shape(B)
    if cA != rB:
        raise ValueError(f"mat_mul: ({rA}x{cA}) * ({rB}x{cB}) incompatible")
    C = _zeros(rA, cB)
    for i in range(rA):
        for k in range(cA):
            if A[i][k] == 0:
                continue
            for j in range(cB):
                C[i][j] += A[i][k] * B[k][j]
    return C


def mat_scalar(A, s):
    rows, cols = _shape(A)
    return [[A[i][j] * s for j in range(cols)] for i in range(rows)]


def transpose(A):
    rows, cols = _shape(A)
    return [[A[i][j] for i in range(rows)] for j in range(cols)]


#DETERMINANT (LU decomposition, in-place on copy)

def determinant(A):
    n, m = _shape(A)
    if n != m:
        raise ValueError("determinant: matrix must be square")
    M   = _copy(A)
    det = 1.0
    for col in range(n):
        # Partial pivoting
        pivot_row = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[pivot_row][col] == 0:
            return 0.0
        if pivot_row != col:
            M[col], M[pivot_row] = M[pivot_row], M[col]
            det *= -1
        det *= M[col][col]
        for row in range(col + 1, n):
            factor = M[row][col] / M[col][col]
            for k in range(col, n):
                M[row][k] -= factor * M[col][k]
    return det


#INVERSE (Gauss-Jordan elimination with augmented identity)

def inverse(A):
    n, m = _shape(A)
    if n != m:
        raise ValueError("inverse: matrix must be square")
    M   = _copy(A)
    inv = _identity(n)
    for col in range(n):
        # Partial pivoting
        pivot_row = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot_row][col]) < 1e-12:
            raise ValueError("inverse: matrix is singular")
        if pivot_row != col:
            M[col],   M[pivot_row]   = M[pivot_row],   M[col]
            inv[col], inv[pivot_row] = inv[pivot_row], inv[col]
        # Scale pivot row
        pivot = M[col][col]
        for k in range(n):
            M[col][k]   /= pivot
            inv[col][k] /= pivot
        # Eliminate column
        for row in range(n):
            if row == col:
                continue
            factor = M[row][col]
            for k in range(n):
                M[row][k]   -= factor * M[col][k]
                inv[row][k] -= factor * inv[col][k]
    return inv


#DISPLAY

def mat_to_str(M):
    rows, cols = _shape(M)
    lines = []
    for i in range(rows):
        row_str = "  ".join(f"{M[i][j]:8.4f}" for j in range(cols))
        lines.append(f"[ {row_str} ]")
    return "\n".join(lines)


#PUBLIC INTERFACE

FUNCTIONS = {
    "mat_add":   mat_add,
    "mat_sub":   mat_sub,
    "mat_mul":   mat_mul,
    "mat_scalar": mat_scalar,
    "transpose": transpose,
    "determinant": determinant,
    "inverse":   inverse,
    "mat_str":   mat_to_str,
}