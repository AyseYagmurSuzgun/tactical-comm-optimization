import numpy as np
import matplotlib.pyplot as plt
from sim.terrain import generate_elevation
from sim.propagation import los_profile_maps

RES, F = 50.0, 900e6
elev = generate_elevation(n=100, seed=1)
tx = (2500.0, 2500.0)

clearance, v = los_profile_maps(elev, RES, tx, h_tx=10, h_rx=1.5, f_hz=F)
blocked = clearance > 0
print(f"Görüş hattı kapalı hücre oranı: {blocked.mean():.1%}")

ext = [0, 5000, 0, 5000]
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].imshow(elev, origin="lower", extent=ext, cmap="terrain")
ax[0].plot(*tx, "b^", markersize=14, markeredgecolor="w")
ax[0].set_title("Arazi ve verici")
ax[1].imshow(blocked, origin="lower", extent=ext, cmap="gray_r")
ax[1].plot(*tx, "b^", markersize=14, markeredgecolor="w")
ax[1].set_title("Görüş hattı haritası (siyah = engelli)")
for a in ax:
    a.set_xlabel("x (m)"); a.set_ylabel("y (m)")
plt.tight_layout()
plt.savefig("report/figures/step4_los.png", dpi=150, bbox_inches="tight")
plt.show()