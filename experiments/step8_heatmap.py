import time
import numpy as np
import matplotlib.pyplot as plt
from sim.terrain import generate_elevation
from sim.link import evaluate, SINR_THRESHOLD_DB

RES = 50.0
elev = generate_elevation(n=100, seed=1)
users = np.random.default_rng(0).uniform(0, 5000, (50, 2))   # 50 rastgele kullanıcı


def plot(tx_positions, title, path):
    t0 = time.time()
    r = evaluate(elev, RES, tx_positions, users)
    print(f"{title}: {time.time()-t0:.2f} s | "
          f"kapsama(alan)={r['coverage_area']:.1%}  kapsama(kullanıcı)={r['coverage_users']:.1%}  "
          f"toplam={r['total_throughput_mbps']:.1f} Mbps  min={r['min_user_throughput_mbps']:.2f} Mbps")

    fig, ax = plt.subplots(1, 2, figsize=(13, 5.5))
    im0 = ax[0].imshow(elev, origin="lower", extent=[0, 5000, 0, 5000], cmap="terrain")
    plt.colorbar(im0, ax=ax[0], label="Yükseklik (m)")
    ax[0].set_title("Arazi")

    im1 = ax[1].imshow(r["sinr_map"], origin="lower", extent=[0, 5000, 0, 5000],
                       cmap="RdYlGn", vmin=-10, vmax=30)
    plt.colorbar(im1, ax=ax[1], label="SINR (dB)")
    xs = (np.arange(100) + 0.5) * RES
    ax[1].contour(xs, xs, r["sinr_map"], levels=[SINR_THRESHOLD_DB], colors="k", linewidths=1)
    tx = np.array(tx_positions)
    ax[1].scatter(tx[:, 0], tx[:, 1], marker="^", s=160, c="blue", edgecolors="w", label="Verici")
    ax[1].scatter(users[:, 0], users[:, 1], s=14, c="k", label="Kullanıcı")
    ax[1].legend(loc="upper right")
    ax[1].set_title(f"{title}\nkapsama(alan)={r['coverage_area']:.0%}  "
                    f"toplam={r['total_throughput_mbps']:.1f} Mbps", fontsize=10)
    for a in ax:
        a.set_xlabel("x (m)"); a.set_ylabel("y (m)")
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()


plot([(2500.0, 2500.0)], "Tek verici (merkez)", "report/figures/step8_single.png")
plot([(1200.0, 1200.0), (3800.0, 1500.0), (2500.0, 3900.0)],
     "3 verici (elle yerleşim)", "report/figures/step8_three.png")