import matplotlib.pyplot as plt
from sim.terrain import generate_elevation

RES = 50.0   # hücre boyutu (m)
elev = generate_elevation(n=100, seed=1)

plt.imshow(elev, origin="lower", extent=[0, 100 * RES, 0, 100 * RES], cmap="terrain")
plt.colorbar(label="Yükseklik (m)")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Sentetik arazi")
plt.savefig("report/figures/step1_terrain.png", dpi=150, bbox_inches="tight")
plt.show()