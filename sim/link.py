"""Link bütçesi, SINR, kapsama ve throughput."""
import numpy as np
from sim.propagation import path_loss_map_db

# ---- Sistem parametreleri (istediğiniz gibi değiştirebilirsiniz) ----
F_HZ = 900e6            # frekans
TX_POWER_DBM = 30.0     # verici gücü
TX_GAIN_DB = 3.0        # verici anten kazancı
RX_GAIN_DB = 0.0        # alıcı anten kazancı
BANDWIDTH_HZ = 5e6      # bant genişliği
NOISE_FIGURE_DB = 6.0   # alıcı gürültü katsayısı
H_TX = 10.0             # verici anten yüksekliği (m)
H_RX = 1.5              # alıcı anten yüksekliği (m)
SINR_THRESHOLD_DB = 5.0 # kapsama eşiği


def noise_dbm(bandwidth_hz=BANDWIDTH_HZ, nf_db=NOISE_FIGURE_DB):
    """Gürültü tabanı (dBm) = -174 + 10 log10(B) + NF"""
    return -174 + 10 * np.log10(bandwidth_hz) + nf_db


def rx_power_map_dbm(elev, res, tx_xy, h_tx=H_TX, seed=0):
    """Alınan güç = Tx gücü + kazançlar - yol kaybı  (dBm)"""
    pl = path_loss_map_db(elev, res, tx_xy, h_tx, H_RX, F_HZ, seed=seed)
    return TX_POWER_DBM + TX_GAIN_DB + RX_GAIN_DB - pl


def sinr_map_db(rx_maps_dbm):
    """rx_maps_dbm: her verici için alınan güç haritası listesi.
    Her hücre en güçlü vericiye bağlanır, diğerleri girişim sayılır.
    Döndürür: (sinr_db haritası, hangi vericiye bağlı haritası)"""
    lin = 10 ** (np.stack(rx_maps_dbm) / 10)           # mW
    serving = lin.argmax(axis=0)
    signal = lin.max(axis=0)
    interference = lin.sum(axis=0) - signal
    noise = 10 ** (noise_dbm() / 10)
    return 10 * np.log10(signal / (interference + noise)), serving


# ---------------- ADIM 7: metrikler ----------------

def coverage_ratio(sinr_db, threshold_db=SINR_THRESHOLD_DB):
    """SINR eşiğin üstünde olan hücrelerin oranı (0-1)."""
    return float(np.mean(sinr_db >= threshold_db))


def shannon_throughput_bps(sinr_db, bandwidth_hz=BANDWIDTH_HZ):
    """Shannon kapasitesi: B * log2(1 + SINR)"""
    return bandwidth_hz * np.log2(1 + 10 ** (sinr_db / 10))


def evaluate(elev, res, tx_positions, users_xy, h_tx=H_TX):
    """Bir yerleşimi değerlendirir. Döndürür: sözlük (metrikler + haritalar)."""
    rx_maps = [rx_power_map_dbm(elev, res, p, h_tx, seed=i) for i, p in enumerate(tx_positions)]
    sinr, serving = sinr_map_db(rx_maps)

    ux, uy = np.asarray(users_xy).T
    j = np.clip((ux / res).astype(int), 0, elev.shape[1] - 1)
    i = np.clip((uy / res).astype(int), 0, elev.shape[0] - 1)
    u_sinr, u_bs = sinr[i, j], serving[i, j]
    covered = u_sinr >= SINR_THRESHOLD_DB

    # Aynı vericiye bağlı kapsanan kullanıcılar bant genişliğini eşit paylaşır
    share = np.array([max(1, np.sum(covered & (u_bs == b))) for b in range(len(tx_positions))])
    per_user = np.where(covered,
                        shannon_throughput_bps(u_sinr, BANDWIDTH_HZ / share[u_bs]), 0.0)
    return {
        "coverage_area": coverage_ratio(sinr),
        "coverage_users": float(covered.mean()),
        "total_throughput_mbps": float(per_user.sum() / 1e6),
        "min_user_throughput_mbps": float(per_user.min() / 1e6),
        "sinr_map": sinr, "serving_map": serving,
    }