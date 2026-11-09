import numpy as np
import matplotlib.pyplot as plt
from sim.terrain import generate_elevation
from sim.propagation import los_profile_maps, knife_edge_loss_db

RES, F = 50.0, 900e6
elev = generate_elevation(n=100, seed=1)
tx = (2500.0, 2500.0)

_, v = los_profile_maps(elev, RES, tx, 10, 1.5, F)
loss = knife_edge_loss_db(v)
print(f"Ortalama difraksiyon kaybı: {loss.mean():.1f} dB, en yüksek: {loss.max():.1f} dB")

plt.imshow(loss, origin="lower", extent=[0, 5000, 0, 5000], cmap="magma")
plt.colorbar(label="Difraksiyon kaybı (dB)")
plt.plot(*tx, "c^", markersize=14, markeredgecolor="w")
plt.title("Arazi kaynaklı difraksiyon kaybı")
plt.xlabel("x (m)"); plt.ylabel("y (m)")
plt.savefig("report/figures/step5_diffraction.png", dpi=150, bbox_inches="tight")
plt.show()