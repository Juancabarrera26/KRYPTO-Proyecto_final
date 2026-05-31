"""
KRYPTOML - Machine Learning algorithms for KRYPTO language.
All implemented from scratch. No external imports.
Depends only on KRYPTOMATH (internal).
"""
from librerias import KRYPTODL
from librerias.KRYPTOMATH import (
    exp_func, sqrt, abs_val, ln
)

#INTERNAL HELPERS

def _dot(a, b):
    """Dot product of two equal-length lists."""
    return sum(a[i] * b[i] for i in range(len(a)))


def _vec_add(a, b):
    return [a[i] + b[i] for i in range(len(a))]


def _vec_scale(v, s):
    return [x * s for x in v]


def _mat_vec_mul(M, v):
    """Matrix (list-of-rows) times column vector (list)."""
    return [_dot(row, v) for row in M]


def _transpose_mat(M):
    rows = len(M)
    cols = len(M[0])
    return [[M[r][c] for r in range(rows)] for c in range(cols)]


def _zeros(n):
    return [0.0] * n


def _mean_list(lst):
    return sum(lst) / len(lst)


def _euclidean(a, b):
    return sqrt(sum((a[i] - b[i]) ** 2 for i in range(len(a))))


#GRADIENT DESCENT OPTIMIZER (shared)

def _gradient_descent(X, y, weights, grad_fn, lr, epochs):
    """
    Generic gradient descent loop.
    grad_fn(X, y, weights) -> gradient vector same shape as weights.
    """
    w = weights[:]
    n = len(y)
    for _ in range(epochs):
        grad = grad_fn(X, y, w)
        w = [w[i] - lr * grad[i] for i in range(len(w))]
    return w


#LINEAR REGRESSION

def _lin_predict(X, w):
    """Predict y-hat for each sample (list of feature lists)."""
    return [_dot(x, w) for x in X]


def _lin_grad(X, y, w):
    """MSE gradient: (1/n) X^T (X w - y)."""
    n     = len(y)
    y_hat = _lin_predict(X, w)
    errors = [y_hat[i] - y[i] for i in range(n)]
    XT    = _transpose_mat(X)
    grad  = [_dot(XT[j], errors) / n for j in range(len(w))]
    return grad


def linear_regression_train(X, y, lr=0.01, epochs=1000):
    """
    Train linear regression via gradient descent.
    X: list of feature lists (bias NOT prepended automatically).
    y: list of target values.
    Returns weight vector w such that y_hat = X * w.
    """
    if not X or not y:
        raise ValueError("linear_regression: empty dataset")
    # Prepend bias column of 1s
    Xb = [[1.0] + row for row in X]
    w  = _zeros(len(Xb[0]))
    w  = _gradient_descent(Xb, y, w, _lin_grad, lr, epochs)
    return w


def linear_regression_predict(X, w):
    """Predict using trained weights (bias prepended automatically)."""
    Xb = [[1.0] + row for row in X]
    return _lin_predict(Xb, w)


#LOGISTIC REGRESSION

def _sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + exp_func(-z))
    e = exp_func(z)
    return e / (1.0 + e)


def _log_predict_proba(X, w):
    return [_sigmoid(_dot(x, w)) for x in X]


def _log_grad(X, y, w):
    """Binary cross-entropy gradient: (1/n) X^T (sigmoid(Xw) - y)."""
    n      = len(y)
    y_hat  = _log_predict_proba(X, w)
    errors = [y_hat[i] - y[i] for i in range(n)]
    XT     = _transpose_mat(X)
    return [_dot(XT[j], errors) / n for j in range(len(w))]


def logistic_regression_train(X, y, lr=0.1, epochs=1000):
    """
    Binary logistic regression via gradient descent.
    y must be 0/1 labels.
    Returns weight vector w.
    """
    Xb = [[1.0] + row for row in X]
    w  = _zeros(len(Xb[0]))
    w  = _gradient_descent(Xb, y, w, _log_grad, lr, epochs)
    return w


def logistic_regression_predict(X, w, threshold=0.5):
    """Returns list of 0/1 class predictions."""
    Xb    = [[1.0] + row for row in X]
    proba = _log_predict_proba(Xb, w)
    return [1 if p >= threshold else 0 for p in proba]


def logistic_regression_proba(X, w):
    """Returns raw probabilities."""
    Xb = [[1.0] + row for row in X]
    return _log_predict_proba(Xb, w)


#MULTILAYER PERCEPTRON  (MLP)

def _relu(x):
    return x if x > 0 else 0.0


def _relu_d(x):
    return 1.0 if x > 0 else 0.0


def _softmax(v):
    max_v = max(v)
    exps  = [exp_func(x - max_v) for x in v]
    s     = sum(exps)
    return [e / s for e in exps]


class MLP:
    """
    Feedforward neural network with configurable hidden layers.
    Activation: ReLU (hidden), sigmoid (binary) or softmax (multi-class).
    Training: backpropagation + gradient descent.
    """

    def __init__(self, layer_sizes, lr=0.01, epochs=500):
        """
        layer_sizes: [input_dim, hidden1, hidden2, ..., output_dim]
        """
        self.layer_sizes = layer_sizes
        self.lr          = lr
        self.epochs      = epochs
        self.weights     = []   #W[l]: matrix (out x in)
        self.biases      = []   #b[l]: vector
        self._init_weights()

    def _init_weights(self):
        """Xavier initialization using simple formula."""
        self.weights = []
        self.biases  = []
        for i in range(len(self.layer_sizes) - 1):
            fan_in  = self.layer_sizes[i]
            fan_out = self.layer_sizes[i + 1]
            limit   = sqrt(6.0 / (fan_in + fan_out))
            # Deterministic pseudo-random using linear congruential generator
            w_flat  = _lcg_uniform(fan_in * fan_out, -limit, limit, seed=i * 1337)
            W = [[w_flat[r * fan_in + c] for c in range(fan_in)] for r in range(fan_out)]
            b = [0.0] * fan_out
            self.weights.append(W)
            self.biases.append(b)

    def _forward(self, x):
        """Returns list of (pre-activation, activation) per layer."""
        activations = []
        a = x[:]
        for l, (W, b) in enumerate(zip(self.weights, self.biases)):
            z = [_dot(W[j], a) + b[j] for j in range(len(b))]
            if l < len(self.weights) - 1:
                a = [_relu(zj) for zj in z]
            else:
                #Output layer: sigmoid for single output, softmax for multi
                if len(z) == 1:
                    a = [_sigmoid(z[0])]
                else:
                    a = _softmax(z)
            activations.append((z, a))
        return activations

    def _backward(self, x, y_true, activations):
        """
        Backprop. y_true: float (binary) or list (multi-class one-hot).
        Returns (dW list, db list).
        """
        n_layers = len(self.weights)
        dW = [None] * n_layers
        db = [None] * n_layers

        #Output delta
        z_out, a_out = activations[-1]
        if isinstance(y_true, (int, float)):
            y_vec = [float(y_true)]
        else:
            y_vec = [float(v) for v in y_true]

        delta = [a_out[j] - y_vec[j] for j in range(len(a_out))]

        for l in range(n_layers - 1, -1, -1):
            a_prev = activations[l - 1][1] if l > 0 else x
            dW[l]  = [[delta[j] * a_prev[k] for k in range(len(a_prev))]
                      for j in range(len(delta))]
            db[l]  = delta[:]

            if l > 0:
                z_prev = activations[l - 1][0]
                W_T    = _transpose_mat(self.weights[l])
                delta  = [_relu_d(z_prev[k]) * _dot(W_T[k], delta)
                          for k in range(len(z_prev))]
        return dW, db

    def train(self, X, y):
        """
        X: list of feature vectors.
        y: list of labels (float for binary, list for multi-class).
        """
        for _ in range(self.epochs):
            for xi, yi in zip(X, y):
                acts      = self._forward(xi)
                dW, db    = self._backward(xi, yi, acts)
                for l in range(len(self.weights)):
                    for j in range(len(self.weights[l])):
                        for k in range(len(self.weights[l][j])):
                            self.weights[l][j][k] -= self.lr * dW[l][j][k]
                        self.biases[l][j] -= self.lr * db[l][j]

    def predict(self, X):
        results = []
        for xi in X:
            acts = self._forward(xi)
            a_out = acts[-1][1]
            if len(a_out) == 1:
                results.append(1 if a_out[0] >= 0.5 else 0)
            else:
                results.append(a_out.index(max(a_out)))
        return results

    def predict_proba(self, X):
        return [self._forward(xi)[-1][1] for xi in X]


#K-NEAREST NEIGHBORS

def knn_predict(X_train, y_train, X_test, k=3):
    """
    K-Nearest Neighbors classifier.
    X_train/X_test: list of feature vectors.
    y_train: list of labels (any type).
    Returns list of predictions.
    """
    predictions = []
    for x in X_test:
        distances = [(_euclidean(x, xt), yt) for xt, yt in zip(X_train, y_train)]
        distances.sort(key=lambda d: d[0])
        neighbors = [yt for _, yt in distances[:k]]
        #Majority vote
        counts = {}
        for label in neighbors:
            counts[label] = counts.get(label, 0) + 1
        predictions.append(max(counts, key=counts.get))
    return predictions


#K-MEANS CLUSTERING

def _lcg_uniform(n, lo, hi, seed=42):
    """Linear congruential generator to produce n floats in [lo, hi]."""
    a, c, m = 1664525, 1013904223, 2 ** 32
    state   = seed
    out     = []
    for _ in range(n):
        state = (a * state + c) % m
        out.append(lo + (state / m) * (hi - lo))
    return out


def kmeans(X, k, max_iter=300, seed=0):
    """
    K-Means clustering.
    X: list of feature vectors.
    k: number of clusters.
    Returns (centroids, labels).
    """
    n      = len(X)
    dim    = len(X[0])
    #K-Means++ style init: first centroid random, rest chosen as farthest point
    rng     = _lcg_uniform(1, 0, 1, seed=seed)
    first   = int(rng[0] * (n - 1))
    centroids = [X[first][:]]
    for _ in range(1, k):
        dists = [min(_euclidean(x, c) for c in centroids) for x in X]
        centroids.append(X[dists.index(max(dists))][:])

    labels = [0] * n
    for _ in range(max_iter):
        #Assignment step
        new_labels = []
        for x in X:
            dists      = [_euclidean(x, c) for c in centroids]
            new_labels.append(dists.index(min(dists)))

        #Check convergence
        if new_labels == labels:
            break
        labels = new_labels

        #Update step
        new_centroids = [[0.0] * dim for _ in range(k)]
        counts        = [0] * k
        for i, x in enumerate(X):
            cl = labels[i]
            for d in range(dim):
                new_centroids[cl][d] += x[d]
            counts[cl] += 1
        for cl in range(k):
            if counts[cl] > 0:
                for d in range(dim):
                    new_centroids[cl][d] /= counts[cl]
            else:
                new_centroids[cl] = centroids[cl][:]  #keep old if empty
        centroids = new_centroids

    return [centroids, labels]


#METRICS

def accuracy(y_true, y_pred):
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return correct / len(y_true)


def confusion_matrix(y_true, y_pred):
    """Returns confusion matrix as list-of-lists for binary classification."""
    classes = sorted(set(y_true) | set(y_pred))
    n       = len(classes)
    idx     = {c: i for i, c in enumerate(classes)}
    cm      = [[0] * n for _ in range(n)]
    for t, p in zip(y_true, y_pred):
        cm[idx[t]][idx[p]] += 1
    return cm


def precision(y_true, y_pred, pos_label=1):
    tp = sum(1 for t, p in zip(y_true, y_pred) if p == pos_label and t == pos_label)
    fp = sum(1 for t, p in zip(y_true, y_pred) if p == pos_label and t != pos_label)
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0


def recall(y_true, y_pred, pos_label=1):
    tp = sum(1 for t, p in zip(y_true, y_pred) if p == pos_label and t == pos_label)
    fn = sum(1 for t, p in zip(y_true, y_pred) if p != pos_label and t == pos_label)
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0


#PUBLIC INTERFACE

FUNCTIONS = {
    "lin_train":       linear_regression_train,
    "lin_predict":     linear_regression_predict,
    "log_train":       logistic_regression_train,
    "log_predict":     logistic_regression_predict,
    "log_proba":       logistic_regression_proba,
    "knn":             knn_predict,
    "kmeans":          kmeans,
    "accuracy":        accuracy,
    "confusion_matrix": confusion_matrix,
    "precision":       precision,
    "recall":          recall,
}