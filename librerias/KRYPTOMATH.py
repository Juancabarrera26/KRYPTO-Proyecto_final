"""
KRYPTOMATH - Pure Python math library for KRYPTO language.
No external imports. All algorithms implemented from scratch.
"""

#Constants
_PI  = 3.141592653589793
_E   = 2.718281828459045
_INF = float('inf')


#INTERNAL HELPERS

def _normalize_angle(x):
    """Reduce x to [-pi, pi] using period 2*pi."""
    tau = 2 * _PI
    x = x % tau
    if x > _PI:
        x -= tau
    return x


def _int_pow(base, exp):
    """Integer exponentiation via repeated squaring."""
    if exp < 0:
        raise ValueError("_int_pow: negative exponent")
    result = 1
    while exp:
        if exp & 1:
            result *= base
        base *= base
        exp >>= 1
    return result


#ARITHMETIC

def abs_val(x):
    return x if x >= 0 else -x


def power(base, exp):
    """
    General power: base^exp for real exp.
    Uses exp(exp * ln(base)) for non-integer exponents.
    """
    if exp == 0:
        return 1
    if isinstance(exp, int) or (isinstance(exp, float) and exp == int(exp)):
        n = int(exp)
        if n >= 0:
            return _int_pow(base, n)
        return 1.0 / _int_pow(base, -n)
    #Real exponent: base^exp = e^(exp * ln(base))
    if base < 0:
        raise ValueError("power: negative base with non-integer exponent")
    if base == 0:
        return 0
    return exp_func(exp * ln(base))


def sqrt(x):
    """Newton-Raphson square root."""
    if x < 0:
        raise ValueError("sqrt: negative argument")
    if x == 0:
        return 0.0
    guess = x if x < 1 else x / 2.0
    for _ in range(60):
        next_g = 0.5 * (guess + x / guess)
        if abs_val(next_g - guess) < 1e-15:
            break
        guess = next_g
    return next_g


def factorial(n):
    """Recursive factorial for non-negative integers."""
    if not isinstance(n, (int, float)) or n < 0:
        raise ValueError("factorial: requires non-negative integer")
    n = int(n)
    if n == 0:
        return 1
    return n * factorial(n - 1)


def gcd_recursive(a, b):
    """Euclidean GCD - recursive."""
    a, b = int(abs_val(a)), int(abs_val(b))
    if b == 0:
        return a
    return gcd_recursive(b, a % b)


def gcd_iterative(a, b):
    """Euclidean GCD - iterative."""
    a, b = int(abs_val(a)), int(abs_val(b))
    while b:
        a, b = b, a % b
    return a


#EXPONENTIAL & LOGARITHM  (Taylor series)

def exp_func(x):
    """
    e^x via Taylor: sum_{k=0}^{inf} x^k / k!
    Range reduction: e^x = (e^(x/2))^2 for large |x|.
    """
    #Range reduction to avoid slow convergence
    if x > 20:
        half = exp_func(x / 2)
        return half * half
    if x < -20:
        return 1.0 / exp_func(-x)
    total = 1.0
    term  = 1.0
    for k in range(1, 200):
        term *= x / k
        total += term
        if abs_val(term) < 1e-16 * abs_val(total):
            break
    return total


def ln(x):
    """
    Natural log via Halley's method: iteratively solve e^y = x.
    Initial guess via bit-length of integer part.
    """
    if x <= 0:
        raise ValueError("ln: argument must be positive")
    if x == 1:
        return 0.0
    #Initial guess
    guess = 0.0
    t = x
    while t >= _E:
        t /= _E
        guess += 1
    while t < 1:
        t *= _E
        guess -= 1
    #Halley refinement
    for _ in range(100):
        e_y = exp_func(guess)
        delta = 2 * (x - e_y) / (x + e_y)   #Halley step
        guess += delta
        if abs_val(delta) < 1e-15:
            break
    return guess


def log(x, base=10):
    """Logarithm base `base` of x."""
    return ln(x) / ln(base)


#TRIGONOMETRY  (Taylor series + range reduction)

def sin(x):
    """
    sin(x) via Taylor: sum_{k=0}^{inf} (-1)^k * x^(2k+1) / (2k+1)!
    """
    x = _normalize_angle(x)
    total = 0.0
    term  = x
    for k in range(1, 100):
        total += term
        term  *= -x * x / ((2 * k) * (2 * k + 1))
        if abs_val(term) < 1e-16:
            break
    return total


def cos(x):
    """
    cos(x) via Taylor: sum_{k=0}^{inf} (-1)^k * x^(2k) / (2k)!
    """
    x = _normalize_angle(x)
    total = 0.0
    term  = 1.0
    for k in range(1, 100):
        total += term
        term  *= -x * x / ((2 * k - 1) * (2 * k))
        if abs_val(term) < 1e-16:
            break
    return total


def tan(x):
    c = cos(x)
    if abs_val(c) < 1e-15:
        raise ValueError("tan: undefined (cos = 0)")
    return sin(x) / c


def asin(x):
    """arcsin via Newton's method."""
    if abs_val(x) > 1:
        raise ValueError("asin: argument out of [-1, 1]")
    if x == 1:
        return _PI / 2
    if x == -1:
        return -_PI / 2
    guess = x
    for _ in range(100):
        delta = (sin(guess) - x) / cos(guess)
        guess -= delta
        if abs_val(delta) < 1e-15:
            break
    return guess


def acos(x):
    return _PI / 2 - asin(x)


def atan(x):
    """arctan via identity and Taylor series."""
    if abs_val(x) > 1:
        sign = 1 if x > 0 else -1
        return sign * (_PI / 2 - atan(1 / abs_val(x)))
    total = 0.0
    term  = x
    x2    = x * x
    for k in range(200):
        total += term / (2 * k + 1)
        term  *= -x2
        if abs_val(term) < 1e-16:
            break
    return total


#TAYLOR POLYNOMIAL FOR e^x  (finite, order n)

def taylor_exp(x, n=15):
    """
    Partial Taylor polynomial of e^x up to degree n:
    P_n(x) = sum_{k=0}^{n} x^k / k!
    """
    total = 0.0
    term  = 1.0
    for k in range(1, n + 1):
        total += term
        term  *= x / k
    total += term
    return total


#SORT ALGORITHM

def bubble_sort(lst):
    """
    Bubble sort on a copy of lst.
    Returns a new sorted list; original unchanged (functional style).
    """
    arr = lst[:]
    n   = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


#STATISTICS HELPERS (used by ML library)

def mean(lst):
    if not lst:
        raise ValueError("mean: empty list")
    return sum(lst) / len(lst)


def variance(lst):
    mu = mean(lst)
    return sum((x - mu) ** 2 for x in lst) / len(lst)


def std_dev(lst):
    return sqrt(variance(lst))


#PUBLIC INTERFACE  (called by interpreter via name lookup)

FUNCTIONS = {
    "factorial":    factorial,
    "sin":          sin,
    "cos":          cos,
    "tan":          tan,
    "asin":         asin,
    "acos":         acos,
    "atan":         atan,
    "sqrt":         sqrt,
    "log":          log,
    "ln":           ln,
    "exp":          exp_func,
    "abs":          abs_val,
    "pow":          power,
    "gcd":          gcd_iterative,
    "gcd_r":        gcd_recursive,
    "bubble_sort":  bubble_sort,
    "taylor_exp":   taylor_exp,
    "mean":         mean,
    "std_dev":      std_dev,
}