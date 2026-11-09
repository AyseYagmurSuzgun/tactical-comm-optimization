import numpy as np
from sim.terrain import generate_elevation
from sim.link import noise_dbm, rx_power_map_dbm, sinr_map_db

RES = 50.0
elev = generate_elevation(n=100, seed=1)
tx = (2500.0, 2500.0)

print(f"Gürültü tabanı: {noise_dbm():.1f} dBm")        # -101.0 dBm çıkmalı

rx = rx_power_map_dbm(elev, RES, tx)
sinr, _ = sinr_map_db([rx])                           # tek verici: girişim yok, SINR = SNR
for name, (x, y) in {"yakın": (2700, 2500), "orta": (3500, 2500), "uzak": (4800, 4800)}.items():
    i, j = int(y / RES), int(x / RES)
    print(f"{name:5s} ({x},{y}): alınan güç = {rx[i, j]:7.1f} dBm | SNR = {sinr[i, j]:6.1f} dB")
    