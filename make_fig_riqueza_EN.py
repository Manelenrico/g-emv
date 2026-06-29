#!/usr/bin/env python3
# Figure 9 (EN): recovery of orientation richness + redistribution of tensions.
import importlib.util, sys, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = "."
sys.path.insert(0, REPO)
os.chdir(REPO)

spec = importlib.util.spec_from_file_location("riq", os.path.join(REPO, "experimentos_riqueza_orientacion.py"))
riq = importlib.util.module_from_spec(spec); sys.modules["riq"] = riq; spec.loader.exec_module(riq)
import model as M
from model import State, DEFAULT_CONFIG
cfg = DEFAULT_CONFIG

half_b = M.TEN_BASAL_MIN / 2
N = 80
init = State(pF=3.8, nF=3.8, pR=half_b, nR=half_b, pS=half_b, nS=half_b)
traj = riq.run_trajectory(init, N, cfg)

steps = np.arange(len(traj))
Rs = np.array([riq.richness(s)[0] for s in traj])
tenF = np.array([s.ten_F for s in traj])
tenR = np.array([s.ten_R for s in traj])
tenS = np.array([s.ten_S for s in traj])

RED  = "#E0382A"  # physical
DARK = "#1F1F1F"  # resources
GREY = "#9C9194"  # social
RICH = "#2C6E9C"  # richness (blue)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.size"] = 11
plt.rcParams["axes.linewidth"] = 0.8

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 5.6), sharex=True,
                               gridspec_kw={"height_ratios": [1, 1], "hspace": 0.14})

ax1.plot(steps, Rs, color=RICH, lw=2.4, zorder=3)
plat = Rs[-1]
ax1.axhline(plat, color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax1.text(N*0.99, plat - 0.085, f"plateau $R \\approx {plat:.2f}$", ha="right", va="top",
         fontsize=10, color="#444444")
ax1.axvline(20, color=GREY, lw=0.8, ls=":", zorder=1)
ax1.text(20, 0.06, "~20 steps", ha="center", va="bottom", fontsize=9.5, color="#555555",
         bbox=dict(fc="white", ec="none", pad=0.6))
ax1.set_ylim(0, 1.02)
ax1.set_ylabel("richness $R$")
ax1.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.spines[["top", "right"]].set_visible(False)

ax2.plot(steps, tenF, color=RED,  lw=2.2, label="physical (F)", zorder=3)
ax2.plot(steps, tenR, color=DARK, lw=2.2, label="resources (R)", zorder=3)
ax2.plot(steps, tenS, color=GREY, lw=2.2, label="social (S)", zorder=3)
ax2.set_ylim(0, max(tenF)*1.06)
ax2.set_ylabel("tension per axis")
ax2.set_xlabel("step")
ax2.set_xlim(0, N)
ax2.spines[["top", "right"]].set_visible(False)
ax2.legend(frameon=False, fontsize=10, loc="upper right", handlelength=1.6)

fig.savefig("figures/fig09_richness_recovery.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("OK -> fig09_richness_recovery.png  R(80)=%.4f" % Rs[-1])
