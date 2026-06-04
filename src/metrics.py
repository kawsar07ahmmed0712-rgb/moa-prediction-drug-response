import numpy as np
from sklearn.metrics import log_loss

def mean_columnwise_log_loss(y_true, y_pred, eps=1e-15):
    """
    Mean column-wise log loss for multi-label classification.
    """
    y_pred = np.clip(y_pred, eps, 1 - eps)
    losses = []

    for i in range(y_true.shape[1]):
        losses.append(log_loss(y_true[:, i], y_pred[:, i], labels=[0, 1]))

    return np.mean(losses)
