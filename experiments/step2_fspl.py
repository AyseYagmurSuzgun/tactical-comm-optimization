import numpy as np
import matplotlib.pyplot as plt
from sim.propagation import fspl_db

d = np.logspace(1, np.log10(5000), 200)     # 10 m ... 5 km
for f in [900e6, 2.4e9]:
    plt.semilogx(d, fspl_db(d, f), label=f"{f/1e6:.0f} MHz")

plt.xlabel("Mesafe (m)")
plt.ylabel("Yol kaybı (dB)")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.show()

# Doğrulama
print("1 km, 900 MHz:", fspl_db(1000, 900e6))                  # ~91.5 dB olmalı
print("Mesafe 2 katına:", fspl_db(2000, 1e9) - fspl_db(1000, 1e9))   # ~6.02 dB olmalı