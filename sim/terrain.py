"""Sentetik arazi üretimi."""
import numpy as np
from scipy.ndimage import gaussian_filter


def generate_elevation(n=100, n_hills=12, max_height=150.0, seed=0):
    """n x n boyutunda yükseklik haritası (metre).
    Rastgele Gauss tepeleri toplanır, ince taneli pürüz eklenir."""
    rng = np.random.default_rng(seed)
    X, Y = np.meshgrid(np.arange(n), np.arange(n))
    elev = np.zeros((n, n))

    for _ in range(n_hills):
        cx, cy = rng.uniform(0, n, 2)          # tepe merkezi
        s = rng.uniform(0.05, 0.15) * n        # tepe genişliği
        a = rng.uniform(0.3, 1.0)              # tepe yüksekliği (göreli)
        elev += a * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * s ** 2))

    elev += 0.75 * gaussian_filter(rng.normal(size=(n, n)), 2)   # pürüz

    # 0 - max_height aralığına ölçekle
    elev = (elev - elev.min()) / (elev.max() - elev.min()) * max_height
    return elev