"""Yayılım modelleri."""
import numpy as np
from scipy.ndimage import gaussian_filter

C = 299_792_458.0   # ışık hızı (m/s)


def fspl_db(d_m, f_hz):
    """Serbest uzay yol kaybı (dB)."""
    d_m = np.maximum(d_m, 1.0)     # sıfıra bölmeyi önle
    return 20 * np.log10(4 * np.pi * d_m * f_hz / C)

def log_distance_db(d_m, f_hz, n=2.7, d0=1.0):
    """Log-distance yol kaybı. n=2 serbest uzaya eşit, n=2.7-3.5 şehir/engebeli."""
    return fspl_db(d0, f_hz) + 10 * n * np.log10(np.maximum(d_m, d0) / d0)


def shadowing_map_db(shape, sigma_db=4.0, corr_cells=2.0, rng=None):
    """Komşu hücrelerde birbirine benzeyen log-normal gölgeleme haritası (dB)."""
    rng = rng or np.random.default_rng(0)
    f = gaussian_filter(rng.normal(size=shape), corr_cells)
    return sigma_db * f / f.std()