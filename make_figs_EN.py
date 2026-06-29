#!/usr/bin/env python3
# Versiones EN de Fig 3 (position) y Fig 4 (tension). Misma maqueta, texto en inglés.
# Términos provisionales (a casar con el glosario final, sobre todo "decentering").
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RED  = "#E0382A"   # physical
DARK = "#1F1F1F"   # resources
GREY = "#9C9194"   # social
plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 130, "savefig.dpi": 300})
OUT = "figures"

# Equilibrio verificado del agente
doms = [
    ("resources",        DARK, 1.6013, 2.0, 0.30),  # name, color, rest_pos, target_pos, target_ten
    ("physical",         RED,  0.8209, 1.0, 0.30),
    ("social/relational",GREY, 0.6802, 0.8, 0.15),
]
ys = [2.0, 1.0, 0.0]

# ═══════════════════════ FIG 3 : POSITION (bipolar axis) ═══════════════════════
fig, ax = plt.subplots(figsize=(10.2, 5.4))
XMIN, XMAX = -1.05, 2.55

ax.axvspan(XMIN, 0, color="#000000", alpha=0.035, zorder=0)
ax.axvline(0, color="#666666", lw=1.4, zorder=2)
ax.text(0, 2.86, "neutrality (0)", ha="center", va="bottom", color="#666666",
        fontsize=10.5, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
ax.annotate("", xy=(XMIN+0.08, 2.62), xytext=(-0.45, 2.62),
            arrowprops=dict(arrowstyle="->", color="#999999", lw=1.3))
ax.text(XMIN+0.12, 2.66, "loss", ha="left", va="bottom", color="#999999",
        fontsize=10.5, style="italic")
ax.annotate("", xy=(XMAX-0.12, 2.62), xytext=(0.55, 2.62),
            arrowprops=dict(arrowstyle="->", color="#9a9a9a", lw=1.3))
ax.text(XMAX-0.18, 2.66, "gain", ha="right", va="bottom", color="#8a8a8a",
        fontsize=10.5, style="italic")

for (name, col, pos, obj, _), y in zip(doms, ys):
    ax.plot([XMIN+0.1, XMAX-0.1], [y, y], color="#d9d9d9", lw=1.2, zorder=1)
    ax.annotate("", xy=(pos, y), xytext=(0, y),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=3.6,
                                shrinkA=0, shrinkB=0, mutation_scale=20))
    ax.plot(0, y, "o", color="#444444", ms=6.5, zorder=6,
            markeredgecolor="white", markeredgewidth=1.0)
    ax.text(-0.07, y+0.16, "$f^-=0$", ha="right", va="bottom", color="#b0b0b0", fontsize=8.5)
    ax.plot([pos, obj], [y, y], color=col, lw=2.0, ls=(0,(2,1.8)), zorder=3)
    ax.plot([obj, obj], [y-0.16, y+0.16], color=col, lw=2.4, zorder=4)
    ax.annotate("", xy=(obj, y+0.30), xytext=(pos, y+0.30),
                arrowprops=dict(arrowstyle="<->", color="#444444", lw=1.1))
    ax.text((pos+obj)/2, y+0.36, "gap", ha="center", va="bottom", color="#444444", fontsize=9.5)
    ax.text(XMIN-0.02, y, name, ha="right", va="center", color=col, fontsize=12.5, fontweight="bold")
    ax.text(pos/2, y-0.22, f"$f^+$ = {pos:.2f}  (= rest)", ha="center", va="top", color=col, fontsize=9.6)
    ax.text(obj+0.05, y-0.16, f"target $\\hat p$ = {obj:.1f}", ha="left", va="top", color="#333333", fontsize=9.8)

# Footer legend, centered below the plot (no longer cramped on the left)
fy1, fy2 = -0.92, -1.18
fx0 = 0.30
ax.annotate("", xy=(fx0+0.34, fy1), xytext=(fx0, fy1),
            arrowprops=dict(arrowstyle="-|>", color="#888888", lw=3.0, mutation_scale=15))
ax.text(fx0+0.44, fy1, "gain force ($f^+$): the only one at rest, carries the position to its rest point",
        ha="left", va="center", fontsize=9.4, color="#444444")
ax.plot([fx0, fx0+0.34], [fy2, fy2], color="#888888", lw=2.0, ls=(0,(2,1.8)))
ax.text(fx0+0.44, fy2, "gap: what is left to reach the target",
        ha="left", va="center", fontsize=9.4, color="#444444")

ax.set_xlim(XMIN-0.95, XMAX); ax.set_ylim(-1.40, 3.05)
ax.set_yticks([]); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.set_title("Displacement by domain (position): at rest only the gain force ($f^+$) acts,\nstarting from neutrality and carrying the position to its rest point (displaced, below the target)",
             fontsize=12.2, pad=14)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_esquema_descentramiento_EN.png", bbox_inches="tight")
plt.close(fig)
print("Fig 3 EN (position) generated.")

# ═══════════════════════ FIG 4 : TENSION (rest, with target/excess/basal) ═══════════════════════
rest = [("resources", DARK, 1.60, 0.30), ("physical", RED, 0.82, 0.30), ("social/relational", GREY, 0.68, 0.15)]

fig, ax = plt.subplots(figsize=(10.6, 5.4))
XMIN, XMAX = -1.0, 2.0
BASAL = 0.10
ax.axvspan(XMIN, 0, color="#000000", alpha=0.035, zorder=0)
ax.axvspan(0, BASAL, color="#000000", alpha=0.10, zorder=0)
ax.axvline(0, color="#666666", lw=1.4, zorder=2)
ax.text(0, 2.86, "neutrality (0)", ha="center", va="bottom", color="#666666",
        fontsize=10.5, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
ax.text(BASAL+0.05, 2.48, "basal min. (0.10)", ha="left", va="bottom", color="#999999", fontsize=8.6)
ax.annotate("", xy=(XMIN+0.10, 2.62), xytext=(-0.42, 2.62),
            arrowprops=dict(arrowstyle="->", color="#999999", lw=1.3))
ax.text(XMIN+0.15, 2.66, "loss", ha="left", va="bottom", color="#999999", fontsize=10.5, style="italic")
ax.annotate("", xy=(XMAX-0.10, 2.62), xytext=(0.42, 2.62),
            arrowprops=dict(arrowstyle="->", color="#9a9a9a", lw=1.3))
ax.text(XMAX-0.15, 2.66, "gain", ha="right", va="bottom", color="#8a8a8a", fontsize=10.5, style="italic")

for (name, col, ten, obj), y in zip(rest, ys):
    ax.plot([XMIN+0.08, XMAX-0.08], [y, y], color="#e3e3e3", lw=1.1, zorder=1)
    ax.annotate("", xy=(ten, y), xytext=(0, y),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=3.6, shrinkA=0, shrinkB=0, mutation_scale=20))
    ax.plot(0, y, "o", color="#444444", ms=6.5, zorder=6, markeredgecolor="white", markeredgewidth=1.0)
    ax.text(-0.07, y+0.16, "$f^-=0$", ha="right", va="bottom", color="#b0b0b0", fontsize=8.5)
    ax.plot([obj, obj], [y-0.17, y+0.17], color="#333333", lw=2.2, zorder=5)
    ax.annotate("", xy=(ten, y+0.30), xytext=(obj, y+0.30),
                arrowprops=dict(arrowstyle="<->", color="#444444", lw=1.1))
    ax.text((obj+ten)/2, y+0.35, f"excess = {ten-obj:.2f}", ha="center", va="bottom", color="#444444", fontsize=9.3)
    ax.text(XMIN-0.04, y, name, ha="right", va="center", color=col, fontsize=12.5, fontweight="bold")
    ax.text(ten+0.05, y, f"tension = {ten:.2f}  (= rest)", ha="left", va="center", color=col, fontsize=10)
    ax.text(obj, y-0.20, f"target $\\hat t$ = {obj:.2f}", ha="center", va="top", color="#333333",
            fontsize=9.2, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

ax.text(XMIN-0.95, -0.85, "At rest only the gain force acts ($f^-=0$): tension equals position,",
        ha="left", va="center", fontsize=9.5, color="#444444")
ax.text(XMIN-0.95, -1.08, "and stays well above its (low) target — the excess is the counterpart of the gap.",
        ha="left", va="center", fontsize=9.5, color="#444444")

ax.set_xlim(XMIN-1.30, XMAX); ax.set_ylim(-1.28, 3.05)
ax.set_yticks([]); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.set_title("Tension by domain: at rest, the only active force is the gain force ($f^-=0$),\nand its excess over the (low) target is the counterpart of the position gap",
             fontsize=12.2, pad=14)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_esquema_tension_EN.png", bbox_inches="tight")
plt.close(fig)
print("Fig 4 EN (tension) generated.")
