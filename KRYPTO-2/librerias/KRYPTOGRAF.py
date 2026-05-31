"""
KRYPTOGRAF - ASCII terminal chart engine for KRYPTO language.
Renders scatter/line plots directly in the terminal.
No external imports.
"""

#Terminal dimensions
_DEFAULT_WIDTH  = 72   #character columns
_DEFAULT_HEIGHT = 20   #character rows


class KryptoChart:
    """
    Accumulates plot commands and renders an ASCII chart on k_show().
    """

    def __init__(self):
        self._reset()

    def _reset(self):
        self._datasets = []   #list of (x_vals, y_vals)
        self._title    = ""
        self._xlabel   = ""
        self._ylabel   = ""

    #COMMAND INTERFACE (called by interpreter)

    def plot(self, x_data, y_data):
        """Register a dataset. x_data and y_data must be lists of numbers."""
        if not isinstance(x_data, list) or not isinstance(y_data, list):
            raise TypeError("k_plot: arguments must be lists")
        if len(x_data) != len(y_data):
            raise ValueError("k_plot: x and y must have the same length")
        self._datasets.append((x_data[:], y_data[:]))

    def set_title(self, title):
        self._title = str(title)

    def set_xlabel(self, label):
        self._xlabel = str(label)

    def set_ylabel(self, label):
        self._ylabel = str(label)

    def show(self):
        if not self._datasets:
            print("[KRYPTOGRAF] No data to display.")
            return
        self._render()
        self._reset()

    #RENDER ENGINE

    def _render(self):
        W = _DEFAULT_WIDTH
        H = _DEFAULT_HEIGHT

        #Collect all data points 
        all_x, all_y = [], []
        for xs, ys in self._datasets:
            all_x.extend(xs)
            all_y.extend(ys)

        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)

        #Avoid degenerate ranges
        if x_max == x_min:
            x_min -= 1; x_max += 1
        if y_max == y_min:
            y_min -= 1; y_max += 1

        #Reserve left margin for y-axis labels (7 chars)
        margin = 7
        plot_w = W - margin
        plot_h = H

        #Build blank canvas
        #canvas[row][col], row 0 = top
        canvas = [[' '] * plot_w for _ in range(plot_h)]

        def to_col(x):
            return int((x - x_min) / (x_max - x_min) * (plot_w - 1))

        def to_row(y):
            return int((y_max - y) / (y_max - y_min) * (plot_h - 1))

        #Plot datasets
        markers = ['*', 'o', '+', 'x', '#']
        for ds_idx, (xs, ys) in enumerate(self._datasets):
            marker = markers[ds_idx % len(markers)]
            sorted_pts = sorted(zip(xs, ys), key=lambda p: p[0])
            prev_col, prev_row = None, None
            for x, y in sorted_pts:
                col = to_col(x)
                row = to_row(y)
                #Draw connecting line (Bresenham)
                if prev_col is not None:
                    for lc, lr in _bresenham(prev_col, prev_row, col, row):
                        if 0 <= lr < plot_h and 0 <= lc < plot_w:
                            if canvas[lr][lc] == ' ':
                                canvas[lr][lc] = '.'
                if 0 <= row < plot_h and 0 <= col < plot_w:
                    canvas[row][col] = marker
                prev_col, prev_row = col, row

        #Print title 
        if self._title:
            total_w = margin + plot_w
            print(self._title.center(total_w))
            print('=' * total_w)

        #Print rows with y-axis labels
        for r in range(plot_h):
            #y value at this row
            y_val = y_max - r * (y_max - y_min) / (plot_h - 1)
            if r == 0 or r == plot_h - 1 or r == plot_h // 2:
                label = f"{y_val:6.2f}|"
            else:
                label = "      |"
            row_str = ''.join(canvas[r])
            print(label + row_str)

        #X axis
        axis_line = ' ' * margin + '-' * plot_w
        print(axis_line)

        #X labels
        x_mid = (x_min + x_max) / 2
        left  = f"{x_min:.2f}"
        mid   = f"{x_mid:.2f}"
        right = f"{x_max:.2f}"
        #Position mid label at center of plot_w
        mid_pos = margin + plot_w // 2 - len(mid) // 2
        label_row  = ' ' * margin + left
        label_row += ' ' * (mid_pos - margin - len(left)) + mid
        remaining  = margin + plot_w - mid_pos - len(mid)
        label_row += ' ' * (remaining - len(right)) + right
        print(label_row)

        #x label
        if self._xlabel:
            total_w = margin + plot_w
            print(self._xlabel.center(total_w))

        #y label (rotated — just print left of chart)
        if self._ylabel:
            print(f"y-axis: {self._ylabel}")

        print()


# BRESENHAM LINE ALGORITHM

def _bresenham(x0, y0, x1, y1):
    """Yield (col, row) integer pairs for line from (x0,y0) to (x1,y1)."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0  += sx
        if e2 < dx:
            err += dx
            y0  += sy
    return points


#SINGLETON INSTANCE (shared across interpreter lifetime)

_chart = KryptoChart()


def get_chart():
    return _chart