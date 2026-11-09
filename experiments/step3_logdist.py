import numpy as np
import matplotlib.pyplot as plt
from sim.propagation import fspl_db, log_distance_db, shadowing_map_db

d = np.logspace(1, np.log10(5000), 200)
f = 900e6
plt.semilogx(d, fspl_db(d, f), label="Serbest uzay (n=2)")
for n in [2.7, 3.5]:
    plt.semilogx(d, log_distance_db(d, f, n), label=f"Log-distance n={n}")
plt.xlabel("Mesafe (m)"); plt.ylabel("Yol kaybı (dB)")
plt.legend(); plt.grid(True, which="both", alpha=0.3)
# yol kaybı eğrileri
plt.savefig("report/figures/step3_logdist.png", dpi=150, bbox_inches="tight")


plt.show()

# Gölgeleme haritası
sh = shadowing_map_db((100, 100), sigma_db=4.0)
plt.imshow(sh, origin="lower", cmap="coolwarm")
plt.colorbar(label="Gölgeleme (dB)")
plt.title("Gölgeleme haritası")
# gölgeleme haritası
plt.savefig("report/figures/step3_shadowing.png", dpi=150, bbox_inches="tight")
plt.show()
print("Std:", sh.std())   # 4.0 çıkmalı