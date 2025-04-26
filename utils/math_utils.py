import numpy as np

def normalize_columns_m(M: np.ndarray) -> np.ndarray:
    """
    Normaliza la probabilidad de cada columna de la matriz M para que sea estocastica.

    Arguemento:
        M (np.ndarray): La matriz a normalizar.

    Salida:
        np.ndarray: La matriz normalizada.
    """
    
    col_sum = np.linalg.norm(M, axis=0, keepdims=True)
    return M / col_sum