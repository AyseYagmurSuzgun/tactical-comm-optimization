import numpy as np
from scipy.ndimage import gaussian_filter
from sim.terrain import sample_height 

C = 299_792_458.0   # ışık hızı (m/s)


def fspl_db(d_m, f_hz):
    """Serbest uzay yol kaybı (dB)."""
    d_m = np.maximum(d_m, 1.0)    
    return 20 * np.log10(4 * np.pi * d_m * f_hz / C)

def log_distance_db(d_m, f_hz, n=2.7, d0=1.0):
    """Log-distance yol kaybı. n=2 serbest uzaya eşit, n=2.7-3.5 şehir/engebeli."""
    return fspl_db(d0, f_hz) + 10 * n * np.log10(np.maximum(d_m, d0) / d0)


def shadowing_map_db(shape, sigma_db=4.0, corr_cells=2.0, rng=None):
    """Komşu hücrelerde birbirine benzeyen log-normal gölgeleme haritası (dB)."""
    rng = rng or np.random.default_rng(0)
    f = gaussian_filter(rng.normal(size=shape), corr_cells)
    return sigma_db * f / f.std()
    
# ---------------- ADIM 4: görüş hattı (LOS) ----------------

def los_profile_maps(elev, res, tx_xy, h_tx, h_rx, f_hz, n_samples=64):
    """Vericiden haritadaki HER hücreye giden doğru boyunca araziyi tarar.
    Döndürür (iki harita, boyutları elev ile aynı):
      clearance : doğru boyunca arazinin görüş hattının ne kadar ÜSTÜNE çıktığı (m).
                  > 0 ise engel var (LOS yok), <= 0 ise görüş hattı açık.
      v         : Fresnel-Kirchhoff parametresi (difraksiyon için, Adım 5'te kullanılacak)."""
    lam = C / f_hz
    H, W = elev.shape
    xs = (np.arange(W) + 0.5) * res
    ys = (np.arange(H) + 0.5) * res
    X, Y = np.meshgrid(xs, ys)
    rx, ry = X.ravel(), Y.ravel()                 # tüm alıcı hücreler (N,)
    tx, ty = tx_xy

    d = np.maximum(np.hypot(rx - tx, ry - ty), 1.0)           # yatay mesafe (N,)
    t = np.linspace(0, 1, n_samples)[1:-1][None, :]           # doğru üzerindeki oranlar (1, S)

    px = tx + t * (rx - tx)[:, None]                          # örnek noktaların x'i (N, S)
    py = ty + t * (ry - ty)[:, None]
    ground = sample_height(elev, res, px, py)                 # o noktalardaki arazi yüksekliği

    h_tx_abs = sample_height(elev, res, tx, ty) + h_tx        # verici anteni (deniz seviyesinden)
    h_rx_abs = sample_height(elev, res, rx, ry) + h_rx        # alıcı anteni (N,)
    h_line = h_tx_abs + t * (h_rx_abs[:, None] - h_tx_abs)    # görüş hattının yüksekliği (N, S)

    clearance = (ground - h_line).max(axis=1)                 # en kötü nokta

    d1, d2 = t * d[:, None], (1 - t) * d[:, None]
    v = ((ground - h_line) * np.sqrt(2 * (d1 + d2) / (lam * d1 * d2))).max(axis=1)
    return clearance.reshape(H, W), v.reshape(H, W)

# ---------------- ADIM 5: difraksiyon kaybı ----------------

def knife_edge_loss_db(v):
    """Bıçak sırtı difraksiyon kaybı (ITU-R P.526 yaklaşımı). v <= -0.78 ise kayıp 0."""
    v = np.asarray(v, dtype=float)
    loss = 6.9 + 20 * np.log10(np.sqrt((v - 0.1) ** 2 + 1) + v - 0.1)
    return np.where(v > -0.78, loss, 0.0)


def path_loss_map_db(elev, res, tx_xy, h_tx, h_rx, f_hz, n=2.7, sigma_db=4.0, seed=0):
    """Toplam yol kaybı haritası (dB) = log-distance + gölgeleme + difraksiyon."""
    H, W = elev.shape
    xs = (np.arange(W) + 0.5) * res
    ys = (np.arange(H) + 0.5) * res
    X, Y = np.meshgrid(xs, ys)
    dz = (sample_height(elev, res, *tx_xy) + h_tx) - (elev + h_rx)
    d3 = np.sqrt((X - tx_xy[0]) ** 2 + (Y - tx_xy[1]) ** 2 + dz ** 2)   # 3B mesafe

    _, v = los_profile_maps(elev, res, tx_xy, h_tx, h_rx, f_hz)
    pl = log_distance_db(d3, f_hz, n)
    pl = pl + shadowing_map_db((H, W), sigma_db, rng=np.random.default_rng(seed))
    pl = pl + knife_edge_loss_db(v)
    return pl
