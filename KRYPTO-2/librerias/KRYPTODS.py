# KRYPTODS.py — Data Science library for KRYPTO
# Pure Python, zero external dependencies.
# All datasets are represented as dict[str, list] (column-oriented).

import csv as _csv
import os as _os


# ── Internal helpers ──────────────────────────────────────────────────────────

def _is_numeric(col):
    """Return True if every non-None value in col can be parsed as float."""
    for v in col:
        if v is None:
            continue
        try:
            float(v)
        except (ValueError, TypeError):
            return False
    return True


def _to_float(col):
    """Convert column values to float, None stays None."""
    result = []
    for v in col:
        if v is None or (isinstance(v, str) and v.strip() == ''):
            result.append(None)
        else:
            result.append(float(v))
    return result


def _numeric_values(col):
    """Return list of floats, skipping None."""
    return [v for v in _to_float(col) if v is not None]


def _mean(vals):
    return sum(vals) / len(vals) if vals else 0.0


def _std(vals):
    if len(vals) < 2:
        return 0.0
    m = _mean(vals)
    return (sum((x - m) ** 2 for x in vals) / len(vals)) ** 0.5


def _median(vals):
    if not vals:
        return 0.0
    s = sorted(vals)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2


def _percentile(vals, p):
    """Return p-th percentile (0-100) via linear interpolation."""
    if not vals:
        return 0.0
    s = sorted(vals)
    n = len(s)
    idx = (p / 100) * (n - 1)
    lo = int(idx)
    hi = lo + 1
    frac = idx - lo
    if hi >= n:
        return s[-1]
    return s[lo] + frac * (s[hi] - s[lo])


def _pad(s, width):
    return str(s)[:width].ljust(width)


def _rpad(s, width):
    return str(s)[:width].rjust(width)


# ── I/O ───────────────────────────────────────────────────────────────────────

def kload(path):
    """Load a CSV file and return a column-oriented dataset dict[str, list]."""
    if not _os.path.exists(path):
        raise FileNotFoundError(f"KRYPTO: archivo '{path}' no encontrado")
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = _csv.DictReader(f)
        columns = reader.fieldnames
        if not columns:
            raise ValueError("KRYPTO: CSV vacío o sin encabezado")
        ds = {col: [] for col in columns}
        for row in reader:
            for col in columns:
                raw = row[col].strip() if row[col] is not None else None
                ds[col].append(None if raw == '' else raw)
    return ds


# ── Dataset metadata ──────────────────────────────────────────────────────────

def kcolumns(ds):
    """Return list of column names."""
    return list(ds.keys())


def kshape(ds):
    """Return [n_rows, n_cols]."""
    cols = list(ds.keys())
    n_rows = len(ds[cols[0]]) if cols else 0
    return [n_rows, len(cols)]


def khead(ds, n=5):
    """Return first n rows as list of dicts."""
    n = int(n)
    cols = list(ds.keys())
    rows = []
    for i in range(min(n, len(ds[cols[0]]))):
        rows.append({col: ds[col][i] for col in cols})
    # Print formatted table
    header = ' | '.join(_pad(c, 14) for c in cols)
    sep    = '-+-'.join('-' * 14 for _ in cols)
    print(header)
    print(sep)
    for row in rows:
        print(' | '.join(_pad(row[c], 14) for c in cols))
    return rows


def knulls(ds):
    """Return dict col -> null_count."""
    result = {}
    for col, vals in ds.items():
        result[col] = sum(1 for v in vals if v is None)
    # Print summary
    print(f"\n{'COLUMNA':<25}  {'NULOS':>7}")
    print('-' * 35)
    for col, cnt in result.items():
        print(f"{_pad(col, 25)}  {cnt:>7}")
    return result


def kselect(ds, cols):
    """Return a new dataset with only the specified columns (list of strings)."""
    if not isinstance(cols, list):
        cols = [cols]
    return {col: ds[col] for col in cols if col in ds}


# ── Descriptive statistics ────────────────────────────────────────────────────

def kdescribe(ds):
    """
    Print and return descriptive stats for all numeric columns.
    Stats: count, mean, std, min, Q1, median, Q3, max.
    """
    stats = {}
    num_cols = [col for col in ds if _is_numeric(ds[col])]

    col_w = 14
    header_cols = ['count', 'mean', 'std', 'min', 'Q1', 'median', 'Q3', 'max']
    header = _pad('column', col_w) + '  ' + '  '.join(_rpad(h, 10) for h in header_cols)
    print('\n' + header)
    print('-' * (col_w + 2 + 11 * len(header_cols)))

    for col in num_cols:
        vals = _numeric_values(ds[col])
        if not vals:
            continue
        n     = len(vals)
        m     = _mean(vals)
        sd    = _std(vals)
        mn    = min(vals)
        q1    = _percentile(vals, 25)
        med   = _median(vals)
        q3    = _percentile(vals, 75)
        mx    = max(vals)

        stats[col] = {
            'count': n, 'mean': round(m, 4), 'std': round(sd, 4),
            'min': round(mn, 4), 'Q1': round(q1, 4),
            'median': round(med, 4), 'Q3': round(q3, 4), 'max': round(mx, 4)
        }

        row_vals = [n, round(m,4), round(sd,4), round(mn,4),
                    round(q1,4), round(med,4), round(q3,4), round(mx,4)]
        row = _pad(col, col_w) + '  ' + '  '.join(_rpad(str(v), 10) for v in row_vals)
        print(row)

    return stats


# ── Boxplot ASCII ─────────────────────────────────────────────────────────────

def _boxplot_ascii(col_name, vals, width=60):
    """Render a single horizontal boxplot to stdout."""
    if not vals:
        print(f"{col_name}: sin datos numéricos")
        return
    mn  = min(vals)
    mx  = max(vals)
    q1  = _percentile(vals, 25)
    med = _median(vals)
    q3  = _percentile(vals, 75)

    def scale(v):
        if mx == mn:
            return 0
        return int((v - mn) / (mx - mn) * (width - 1))

    pos_mn  = scale(mn)
    pos_q1  = scale(q1)
    pos_med = scale(med)
    pos_q3  = scale(q3)
    pos_mx  = scale(mx)

    line = [' '] * width

    # whiskers
    for i in range(pos_mn, pos_q1):
        line[i] = '-'
    for i in range(pos_q3 + 1, pos_mx + 1):
        line[i] = '-'

    # box
    for i in range(pos_q1, pos_q3 + 1):
        line[i] = '='

    # special markers
    line[pos_mn]  = '|'
    line[pos_mx]  = '|'
    line[pos_med] = 'M'

    label = f"{col_name:<18}"
    print(f"\n{label} {''.join(line)}")
    print(f"{'':18}  min={round(mn,3):<10} Q1={round(q1,3):<10} "
          f"med={round(med,3):<10} Q3={round(q3,3):<10} max={round(mx,3)}")


def kboxplot(ds, col):
    """Render boxplot ASCII for a single column."""
    if col not in ds:
        raise KeyError(f"KRYPTO: columna '{col}' no existe")
    vals = _numeric_values(ds[col])
    _boxplot_ascii(col, vals)
    return None


def kboxplot_all(ds):
    """Render boxplot ASCII for every numeric column."""
    num_cols = [col for col in ds if _is_numeric(ds[col])]
    if not num_cols:
        print("KRYPTO: no hay columnas numéricas en el dataset")
        return None
    print("\n=== BOXPLOT — todas las variables numéricas ===")
    for col in num_cols:
        vals = _numeric_values(ds[col])
        _boxplot_ascii(col, vals)
    return None


# ── Histogram ASCII ───────────────────────────────────────────────────────────

def khistogram(ds, col, bins=10):
    """Render vertical histogram ASCII for a numeric column."""
    bins = int(bins)
    if col not in ds:
        raise KeyError(f"KRYPTO: columna '{col}' no existe")
    vals = _numeric_values(ds[col])
    if not vals:
        print(f"KRYPTO: columna '{col}' sin datos")
        return None

    mn, mx = min(vals), max(vals)
    if mx == mn:
        print(f"KRYPTO: todos los valores de '{col}' son iguales ({mn})")
        return None

    width = (mx - mn) / bins
    counts = [0] * bins
    for v in vals:
        idx = int((v - mn) / (mx - mn) * bins)
        if idx == bins:
            idx = bins - 1
        counts[idx] += 1

    max_count = max(counts)
    bar_height = 20
    print(f"\n=== HISTOGRAMA: {col} ===")
    for row in range(bar_height, 0, -1):
        threshold = row / bar_height * max_count
        line = ''
        for c in counts:
            line += '##  ' if c >= threshold else '    '
        print(f"{int(threshold):>4} | {line}")

    print('     +' + '----' * bins)
    edge_labels = [f"{mn + i * width:.2f}" for i in range(0, bins + 1, max(1, bins // 5))]
    print('      ' + '    '.join(f"{l:<6}" for l in edge_labels))
    return None


# ── Correlation matrix ────────────────────────────────────────────────────────

def kcorr(ds):
    """Compute and print Pearson correlation matrix for all numeric columns."""
    num_cols = [col for col in ds if _is_numeric(ds[col])]
    if len(num_cols) < 2:
        print("KRYPTO: se necesitan al menos 2 columnas numéricas")
        return {}

    # Align lengths
    n = min(len(ds[col]) for col in num_cols)
    data = {col: _to_float(ds[col])[:n] for col in num_cols}

    def pearson(a, b):
        pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
        if not pairs:
            return 0.0
        xs, ys = zip(*pairs)
        mx, my = _mean(xs), _mean(ys)
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        dx  = sum((x - mx) ** 2 for x in xs) ** 0.5
        dy  = sum((y - my) ** 2 for y in ys) ** 0.5
        if dx == 0 or dy == 0:
            return 0.0
        return num / (dx * dy)

    matrix = {}
    col_w = 12
    header = _pad('', col_w) + '  ' + '  '.join(_pad(c, col_w) for c in num_cols)
    print('\n=== CORRELACIÓN DE PEARSON ===')
    print(header)
    print('-' * len(header))

    for c1 in num_cols:
        matrix[c1] = {}
        row = _pad(c1, col_w) + '  '
        for c2 in num_cols:
            r = pearson(data[c1], data[c2])
            matrix[c1][c2] = round(r, 4)
            row += _pad(f"{r:+.3f}", col_w) + '  '
        print(row)

    return matrix


# ── Frequency table ───────────────────────────────────────────────────────────

def kfreq(ds, col):
    """Print frequency table for a categorical column."""
    if col not in ds:
        raise KeyError(f"KRYPTO: columna '{col}' no existe")
    vals = [v for v in ds[col] if v is not None]
    n = len(vals)
    freq = {}
    for v in vals:
        freq[v] = freq.get(v, 0) + 1
    freq_sorted = sorted(freq.items(), key=lambda x: -x[1])

    print(f"\n=== FRECUENCIAS: {col} (n={n}) ===")
    print(f"{'VALOR':<25}  {'CONTEO':>8}  {'%':>8}")
    print('-' * 46)
    for val, count in freq_sorted:
        pct = count / n * 100
        bar = '#' * int(pct / 2)
        print(f"{_pad(str(val), 25)}  {count:>8}  {pct:>7.2f}%  {bar}")

    return [[v, c] for v, c in freq_sorted]


# ── Excel → CSV conversion ────────────────────────────────────────────────────

import zipfile as _zipfile

_NS_SS  = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
_NS_REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def _xlsx_shared_strings(zf):
    try:
        with zf.open('xl/sharedStrings.xml') as f:
            tree = _ET.parse(f)
    except KeyError:
        return []
    strings = []
    for si in tree.getroot().findall(f'{{{_NS_SS}}}si'):
        strings.append(''.join(t.text or '' for t in si.iter(f'{{{_NS_SS}}}t')))
    return strings


def _xlsx_normalize_path(target):
    return target.lstrip('/') if target.startswith('/') else 'xl/' + target


def _xlsx_sheet_names(zf):
    with zf.open('xl/workbook.xml') as f:
        tree = _ET.parse(f)
    with zf.open('xl/_rels/workbook.xml.rels') as f:
        rel_tree = _ET.parse(f)
    rels = {r.attrib['Id']: r.attrib['Target'] for r in rel_tree.getroot()}
    sheets = []
    for sheet in tree.getroot().findall(f'.//{{{_NS_SS}}}sheet'):
        name = sheet.attrib['name']
        rid  = sheet.attrib.get(f'{{{_NS_REL}}}id') or sheet.attrib.get('r:id', '')
        sheets.append((name, _xlsx_normalize_path(rels.get(rid, ''))))
    return sheets


def _xlsx_col_index(col_str):
    idx = 0
    for ch in col_str:
        idx = idx * 26 + (ord(ch.upper()) - ord('A') + 1)
    return idx - 1


def _xlsx_parse_ref(ref):
    i = 0
    while i < len(ref) and ref[i].isalpha():
        i += 1
    return ref[:i], int(ref[i:]) if ref[i:] else 1


def _xlsx_read_sheet(zf, path, shared):
    with zf.open(path) as f:
        tree = _ET.parse(f)
    root    = tree.getroot()
    rows_d  = {}
    max_col = 0

    for row_el in root.iter(f'{{{_NS_SS}}}row'):
        r_idx = int(row_el.attrib.get('r', 0))
        cells = {}
        for c_el in row_el:
            ref   = c_el.attrib.get('r', '')
            ctype = c_el.attrib.get('t', '')
            col_str, _ = _xlsx_parse_ref(ref) if ref else ('A', r_idx)
            col_idx    = _xlsx_col_index(col_str)
            max_col    = max(max_col, col_idx)

            val = ''
            if ctype == 'inlineStr':
                is_el = c_el.find(f'{{{_NS_SS}}}is')
                if is_el is not None:
                    val = ''.join(t.text or '' for t in is_el.iter(f'{{{_NS_SS}}}t'))
            elif ctype == 's':
                v_el = c_el.find(f'{{{_NS_SS}}}v')
                if v_el is not None and v_el.text is not None:
                    val = shared[int(v_el.text)]
            elif ctype == 'b':
                v_el = c_el.find(f'{{{_NS_SS}}}v')
                val  = 'TRUE' if (v_el is not None and v_el.text == '1') else 'FALSE'
            else:
                v_el = c_el.find(f'{{{_NS_SS}}}v')
                if v_el is not None and v_el.text is not None:
                    val = v_el.text

            cells[col_idx] = val
        rows_d[r_idx] = cells

    if not rows_d:
        return []
    min_r, max_r = min(rows_d), max(rows_d)
    return [[rows_d.get(r, {}).get(c, '') for c in range(max_col + 1)]
            for r in range(min_r, max_r + 1)]


import xml.etree.ElementTree as _ET


def kexcel_to_csv(xlsx_path, csv_path=None, sheet=None):
    """
    Convert an Excel .xlsx file to CSV.

    Parameters
    ----------
    xlsx_path : str   Path to the .xlsx file.
    csv_path  : str   Output CSV path. Defaults to same name with .csv extension.
    sheet     : str|int  Sheet name or 0-based index. Defaults to first sheet.

    Returns the output CSV path as a string.
    """
    if not _os.path.exists(xlsx_path):
        raise FileNotFoundError(f"KRYPTO: archivo '{xlsx_path}' no encontrado")

    with _zipfile.ZipFile(xlsx_path, 'r') as zf:
        shared = _xlsx_shared_strings(zf)
        sheets = _xlsx_sheet_names(zf)
        if not sheets:
            raise ValueError("KRYPTO: el archivo no contiene hojas")

        if sheet is None:
            _, path = sheets[0]
        elif isinstance(sheet, (int, float)):
            _, path = sheets[int(sheet)]
        else:
            match = [(n, p) for n, p in sheets if n == str(sheet)]
            if not match:
                available = [n for n, _ in sheets]
                raise ValueError(f"KRYPTO: hoja '{sheet}' no encontrada. Disponibles: {available}")
            _, path = match[0]

        rows = _xlsx_read_sheet(zf, path, shared)

    if csv_path is None:
        csv_path = _os.path.splitext(xlsx_path)[0] + '.csv'

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        _csv.writer(f).writerows(rows)

    print(f"KRYPTO: Excel convertido → {csv_path}  ({len(rows)} filas)")
    return csv_path


def kexcel_sheets(xlsx_path):
    """Return list of sheet names in an .xlsx file."""
    if not _os.path.exists(xlsx_path):
        raise FileNotFoundError(f"KRYPTO: archivo '{xlsx_path}' no encontrado")
    with _zipfile.ZipFile(xlsx_path, 'r') as zf:
        sheets = _xlsx_sheet_names(zf)
    names = [n for n, _ in sheets]
    print(f"KRYPTO: hojas en '{xlsx_path}': {names}")
    return names


# ── Function registry (imported by interpreter) ───────────────────────────────

FUNCTIONS = {
    'kload':           kload,
    'kcolumns':        kcolumns,
    'kshape':          kshape,
    'khead':           khead,
    'knulls':          knulls,
    'kselect':         kselect,
    'kdescribe':       kdescribe,
    'kboxplot':        kboxplot,
    'kboxplot_all':    kboxplot_all,
    'khistogram':      khistogram,
    'kcorr':           kcorr,
    'kfreq':           kfreq,
    'kexcel_to_csv':   kexcel_to_csv,
    'kexcel_sheets':   kexcel_sheets,
}


def kget_col(ds, col):
    """Return a numeric column as a plain list of floats, skipping None."""
    if col not in ds:
        raise KeyError(f"KRYPTO: columna '{col}' no existe")
    return _numeric_values(ds[col])


FUNCTIONS['kget_col'] = kget_col