"""
KRYPTODL - Deep Learning module for the KRYPTO language.
Implemented from scratch. No external imports.
Depends only on KRYPTOMATH (internal).
"""

from librerias.KRYPTOMATH import exp_func, sqrt


#Math primitives

def _dot(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))


def _mat_vec_mul(M, v):
    return [_dot(row, v) for row in M]


def _transpose_mat(M):
    rows, cols = len(M), len(M[0])
    return [[M[r][c] for r in range(rows)] for c in range(cols)]


def _sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + exp_func(-z))
    e = exp_func(z)
    return e / (1.0 + e)


def _sigmoid_d(z):
    s = _sigmoid(z)
    return s * (1.0 - s)


def _relu(x):
    return x if x > 0 else 0.0


def _relu_d(x):
    return 1.0 if x > 0 else 0.0


def _tanh(x):
    ep = exp_func(x)
    em = exp_func(-x)
    return (ep - em) / (ep + em)


def _tanh_d(x):
    t = _tanh(x)
    return 1.0 - t * t


def _softmax(v):
    max_v = max(v)
    exps = [exp_func(x - max_v) for x in v]
    s = sum(exps)
    return [e / s for e in exps]


#Linear congruential generator (deterministic pseudo-random)

def _lcg_uniform(n, lo, hi, seed=42):
    a, c, m = 1664525, 1013904223, 2 ** 32
    state = seed
    out = []
    for _ in range(n):
        state = (a * state + c) % m
        out.append(lo + (state / m) * (hi - lo))
    return out


#Model registry — maps integer handle -> MLP instance

_MODEL_REGISTRY: dict = {}
_next_id: list = [0]


def _register(model) -> int:
    mid = _next_id[0]
    _MODEL_REGISTRY[mid] = model
    _next_id[0] += 1
    return mid


def _get_model(model_id):
    mid = int(model_id)
    if mid not in _MODEL_REGISTRY:
        raise KeyError(f"KRYPTODL: no model with id={mid}")
    return _MODEL_REGISTRY[mid]


#MLP — feedforward neural network

_ACTIVATIONS = {
    "relu":    (_relu,    _relu_d),
    "sigmoid": (_sigmoid, _sigmoid_d),
    "tanh":    (_tanh,    _tanh_d),
}


class _MLP:
    """
    Fully-connected feedforward network.
    Hidden layers: configurable activation (default ReLU).
    Output layer:  sigmoid (single output) or softmax (multiple outputs).
    Training:      mini-batch SGD with backpropagation.
    Init:          Xavier uniform.
    """

    def __init__(self, layer_sizes, lr=0.01, epochs=500,
                 activation="relu", batch_size=1):
        self.layer_sizes = [int(x) for x in layer_sizes]
        self.lr = float(lr)
        self.epochs = int(epochs)
        self.batch_size = int(batch_size)
        if activation not in _ACTIVATIONS:
            activation = "relu"
        self.act, self.act_d = _ACTIVATIONS[activation]
        self.weights = []
        self.biases = []
        self._init_weights()
        #Training history
        self.loss_history = []

    def _init_weights(self):
        self.weights = []
        self.biases = []
        for i in range(len(self.layer_sizes) - 1):
            fan_in = self.layer_sizes[i]
            fan_out = self.layer_sizes[i + 1]
            limit = sqrt(6.0 / (fan_in + fan_out))
            w_flat = _lcg_uniform(fan_in * fan_out, -limit, limit, seed=i * 1337 + 7)
            W = [[w_flat[r * fan_in + c] for c in range(fan_in)]
                 for r in range(fan_out)]
            b = [0.0] * fan_out
            self.weights.append(W)
            self.biases.append(b)

    def _forward(self, x):
        """Returns list of (z, a) tuples per layer."""
        activations = []
        a = list(x)
        n_layers = len(self.weights)
        for l, (W, b) in enumerate(zip(self.weights, self.biases)):
            z = [_dot(W[j], a) + b[j] for j in range(len(b))]
            if l < n_layers - 1:
                #Hidden layer
                a = [self.act(zj) for zj in z]
            else:
                #Output layer
                if len(z) == 1:
                    a = [_sigmoid(z[0])]
                else:
                    a = _softmax(z)
            activations.append((z, a))
        return activations

    def _backward(self, x, y_true, activations):
        """Returns (dW, db) gradient lists."""
        n_layers = len(self.weights)
        dW = [None] * n_layers
        db = [None] * n_layers

        #Output delta
        _, a_out = activations[-1]
        if isinstance(y_true, (int, float)):
            y_vec = [float(y_true)]
        else:
            y_vec = [float(v) for v in y_true]

        delta = [a_out[j] - y_vec[j] for j in range(len(a_out))]

        for l in range(n_layers - 1, -1, -1):
            a_prev = activations[l - 1][1] if l > 0 else list(x)
            dW[l] = [[delta[j] * a_prev[k] for k in range(len(a_prev))]
                     for j in range(len(delta))]
            db[l] = delta[:]

            if l > 0:
                z_prev = activations[l - 1][0]
                W_T = _transpose_mat(self.weights[l])
                delta = [self.act_d(z_prev[k]) * _dot(W_T[k], delta)
                         for k in range(len(z_prev))]

        return dW, db

    def _accumulate_gradients(self, batch_X, batch_y):
        """Average gradients over a mini-batch."""
        n = len(batch_X)
        cum_dW = None
        cum_db = None
        for xi, yi in zip(batch_X, batch_y):
            acts = self._forward(xi)
            dW, db = self._backward(xi, yi, acts)
            if cum_dW is None:
                cum_dW = dW
                cum_db = db
            else:
                for l in range(len(dW)):
                    for j in range(len(dW[l])):
                        for k in range(len(dW[l][j])):
                            cum_dW[l][j][k] += dW[l][j][k]
                        cum_db[l][j] += db[l][j]
        #Divide by batch size
        for l in range(len(cum_dW)):
            for j in range(len(cum_dW[l])):
                for k in range(len(cum_dW[l][j])):
                    cum_dW[l][j][k] /= n
                cum_db[l][j] /= n
        return cum_dW, cum_db

    def _apply_gradients(self, dW, db):
        for l in range(len(self.weights)):
            for j in range(len(self.weights[l])):
                for k in range(len(self.weights[l][j])):
                    self.weights[l][j][k] -= self.lr * dW[l][j][k]
                self.biases[l][j] -= self.lr * db[l][j]

    def train(self, X, y):
        n = len(X)
        bs = self.batch_size if self.batch_size > 0 else n
        self.loss_history = []
        for epoch in range(self.epochs):
            #Deterministic shuffle via LCG
            order = list(range(n))
            rvals = _lcg_uniform(n, 0, 1, seed=epoch * 31 + 17)
            order.sort(key=lambda i: rvals[i])
            X_s = [X[i] for i in order]
            y_s = [y[i] for i in order]

            for start in range(0, n, bs):
                batch_X = X_s[start:start + bs]
                batch_y = y_s[start:start + bs]
                dW, db = self._accumulate_gradients(batch_X, batch_y)
                self._apply_gradients(dW, db)

            #Record loss every 10% of epochs
            if epoch % max(1, self.epochs // 10) == 0:
                self.loss_history.append(self._compute_loss(X, y))

    def _compute_loss(self, X, y):
        """Binary cross-entropy for single output; MSE otherwise."""
        total = 0.0
        n = len(X)
        for xi, yi in zip(X, y):
            acts = self._forward(xi)
            a_out = acts[-1][1]
            if isinstance(yi, (int, float)):
                y_val = float(yi)
                p = a_out[0]
                #Binary cross-entropy
                p = max(1e-15, min(1 - 1e-15, p))
                total += -(y_val * (ln_approx(p)) + (1 - y_val) * ln_approx(1 - p))
            else:
                #MSE for multi-output
                for j in range(len(yi)):
                    diff = a_out[j] - float(yi[j])
                    total += diff * diff
                total /= len(yi)
        return total / n

    def predict(self, X):
        results = []
        for xi in X:
            a_out = self._forward(xi)[-1][1]
            if len(a_out) == 1:
                results.append(1 if a_out[0] >= 0.5 else 0)
            else:
                results.append(a_out.index(max(a_out)))
        return results

    def predict_proba(self, X):
        return [self._forward(xi)[-1][1] for xi in X]

    def summary(self):
        print("KRYPTODL Model Summary")
        total_params = 0
        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            n_w = len(W) * len(W[0])
            n_b = len(b)
            layer_params = n_w + n_b
            total_params += layer_params
            in_dim = self.layer_sizes[i]
            out_dim = self.layer_sizes[i + 1]
            print(f"  Layer {i + 1}: {in_dim} -> {out_dim}  "
                  f"| params: {layer_params}  "
                  f"| act: {'output(sigmoid/softmax)' if i == len(self.weights)-1 else 'relu'}")
        print(f"  Total parameters: {total_params}")
        print(f"  lr={self.lr}  epochs={self.epochs}  batch_size={self.batch_size}")


#Natural log approximation (avoid circular import of ln from KRYPTOMATH)
def ln_approx(x):
    """ln(x) via imported KRYPTOMATH.ln if available, else fallback series."""
    try:
        from librerias.KRYPTOMATH import ln
        return ln(x)
    except Exception:
        # Fallback: Padé-like approximation for x near 1
        t = (x - 1) / (x + 1)
        result = 0.0
        t2 = t * t
        term = t
        for k in range(1, 50):
            result += term / (2 * k - 1)
            term *= t2
        return 2.0 * result


#Public API functions (called from .kr via interpreter dispatch)

def dl_create(layer_sizes, lr=0.01, epochs=500):
    """
    Create and register a new MLP model.
    layer_sizes: list like [2, 8, 4, 1] -> input=2, hidden=[8,4], output=1.
    Returns model_id (int).
    """
    if not isinstance(layer_sizes, list) or len(layer_sizes) < 2:
        raise ValueError("dl_create: layer_sizes must be a list with >= 2 elements")
    model = _MLP(layer_sizes, lr=float(lr), epochs=int(epochs))
    return _register(model)


def dl_create_full(layer_sizes, lr=0.01, epochs=500,
                   activation="relu", batch_size=1):
    """
    Create MLP with explicit activation and batch_size.
    activation: 'relu', 'sigmoid', or 'tanh'.
    """
    model = _MLP(layer_sizes, lr=float(lr), epochs=int(epochs),
                 activation=str(activation), batch_size=int(batch_size))
    return _register(model)


def dl_train(model_id, X, y):
    """
    Train model in-place.
    X: list of feature vectors.
    y: list of labels (float for binary, list for multi-class one-hot).
    Returns model_id.
    """
    model = _get_model(model_id)
    model.train(X, y)
    return int(model_id)


def dl_predict(model_id, X):
    """
    Predict class labels.
    Returns list of int predictions.
    """
    return _get_model(model_id).predict(X)


def dl_proba(model_id, X):
    """
    Predict raw output probabilities.
    Returns list of probability vectors.
    """
    return _get_model(model_id).predict_proba(X)


def dl_evaluate(model_id, X, y):
    """
    Compute accuracy on (X, y).
    Returns float in [0, 1].
    """
    preds = _get_model(model_id).predict(X)
    if isinstance(y[0], list):
        y_labels = [v.index(max(v)) for v in y]
    else:
        y_labels = [int(v) for v in y]
    correct = sum(1 for a, b in zip(y_labels, preds) if a == b)
    return correct / len(y_labels)


def dl_loss(model_id, X, y):
    """
    Compute loss on (X, y).
    Returns float.
    """
    return _get_model(model_id)._compute_loss(X, y)


def dl_loss_history(model_id):
    """
    Return recorded loss values during last training run.
    """
    return _get_model(model_id).loss_history[:]


def dl_summary(model_id):
    """
    Print model architecture to stdout.
    Returns None.
    """
    _get_model(model_id).summary()
    return None


def dl_save_weights(model_id):
    """
    Export weights and biases as a flat list.
    Format: [n_layers, l0_rows, l0_cols, ...weights..., ...biases..., ...]
    Returns list.
    """
    model = _get_model(model_id)
    data = [float(len(model.weights))]
    for W, b in zip(model.weights, model.biases):
        rows, cols = len(W), len(W[0])
        data.append(float(rows))
        data.append(float(cols))
        for row in W:
            data.extend(row)
        data.extend(b)
    return data


def dl_load_weights(layer_sizes, data):
    """
    Reconstruct a model from saved weight data.
    layer_sizes: same list used in dl_create.
    data: list returned by dl_save_weights.
    Returns model_id.
    """
    model = _MLP(layer_sizes)
    idx = 1  # skip n_layers
    for l in range(len(model.weights)):
        rows = int(data[idx]); idx += 1
        cols = int(data[idx]); idx += 1
        W = []
        for r in range(rows):
            W.append(data[idx:idx + cols])
            idx += cols
        b = data[idx:idx + rows]
        idx += rows
        model.weights[l] = W
        model.biases[l] = b
    return _register(model)


#Public function table (consumed by interpreter._BUILTINS)

FUNCTIONS = {
    "dl_create":       dl_create,
    "dl_create_full":  dl_create_full,
    "dl_train":        dl_train,
    "dl_predict":      dl_predict,
    "dl_proba":        dl_proba,
    "dl_evaluate":     dl_evaluate,
    "dl_loss":         dl_loss,
    "dl_loss_history": dl_loss_history,
    "dl_summary":      dl_summary,
    "dl_save_weights": dl_save_weights,
    "dl_load_weights": dl_load_weights,
}