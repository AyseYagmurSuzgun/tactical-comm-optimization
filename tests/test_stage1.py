"""Çalıştır:  python -m tests.test_stage1"""
import numpy as np
from sim.terrain import generate_elevation
from sim.propagation import los_profile_maps, knife_edge_loss_db, path_loss_map_db
from sim.link import evaluate

RES = 50.0
F = 900e6


def test_flat_terrain_has_los():
    elev = np.zeros((100, 100))
    clearance, _ = los_profile_maps(elev, RES, (2500.0, 2500.0), 10, 1.5, F)
    assert np.all(clearance <= 0)          # düz arazide engel yok


def test_wall_blocks_los():
    elev = np.zeros((100, 100)); elev[:, 50] = 80.0      # 80 m'lik duvar
    clearance, v = los_profile_maps(elev, RES, (1000.0, 2500.0), 10, 1.5, F)
    assert clearance[50, 80] > 0           # duvarın arkası: engel var
    assert clearance[50, 20] <= 0          # duvarın önü: açık
    assert knife_edge_loss_db(v[50, 80]) > 15


def test_loss_grows_with_distance():
    elev = np.zeros((100, 100))
    pl = path_loss_map_db(elev, RES, (500.0, 2500.0), 10, 1.5, F, sigma_db=0.0)
    assert pl[50, 80] > pl[50, 20]         # uzak hücre daha çok kayıp


def test_higher_antenna_helps_behind_hill():
    elev = generate_elevation(seed=1)
    lo = path_loss_map_db(elev, RES, (2500.0, 2500.0), 2, 1.5, F).mean()
    hi = path_loss_map_db(elev, RES, (2500.0, 2500.0), 60, 1.5, F).mean()
    assert hi < lo


def test_second_station_increases_coverage():
    elev = generate_elevation(seed=1)
    users = np.random.default_rng(0).uniform(0, 5000, (50, 2))
    one = evaluate(elev, RES, [(1500.0, 2500.0)], users)["coverage_area"]
    two = evaluate(elev, RES, [(1500.0, 2500.0), (3500.0, 2500.0)], users)["coverage_area"]
    assert two > one


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("OK ", name)