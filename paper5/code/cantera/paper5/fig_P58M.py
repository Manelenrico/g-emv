"""[P5-8M] Las dos figuras del cierre, de los datos crudos con matplotlib.

  F1 · ignorancia por tic, A contra K (todas las semillas emparejadas)
  F2 · una vida de K con sus formas

Nada de MettaScope: se reconstruye el `Ojo` de los diarios, como el banco.
"""
import glob, json, os, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import serie_util as U, curiosidad as C

PASO = 200                      # se muestrea la curva cada 200 tics


def curva(f):
    """(tics, ignorancia) reconstruyendo el Ojo del diario."""
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        return None, None, None
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    ojo = C.Ojo(mundo, 8)
    xs, ys = [], []
    vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
    for i, r in enumerate(vivos):
        p = tuple(r.get("pos") or ())
        if p:
            ojo.mira(p, r["tick"])
        if i % PASO == 0:
            xs.append(r["tick"]); ys.append(ojo.ignorancia_global())
    if vivos:
        xs.append(vivos[-1]["tick"]); ys.append(ojo.ignorancia_global())
    return xs, ys, recs


# ── F1 · ignorancia por tic, A contra K ──
fig, ax = plt.subplots(figsize=(9, 5.2))
nK = nA = 0
import statistics as _st
MED = {}
for brazo, col, lab in (("A", "#9aa0a6", "A · cuerpo solo"),
                        ("K", "#1a73e8", "K · curiosidad como forma")):
    todas = []
    for f in sorted(glob.glob(f"paintball/runs/P58M_t*_{brazo}_*/*.art.log")):
        xs, ys, _ = curva(f)
        if not xs:
            continue
        ax.plot(xs, ys, color=col, alpha=0.18, linewidth=0.8,
                label=(lab if (brazo == "A" and nA == 0) or
                       (brazo == "K" and nK == 0) else None))
        todas.append((xs, ys))
        if brazo == "A": nA += 1
        else: nK += 1
    # LA MEDIANA por tic, sobre los asientos QUE SIGUEN VIVOS en ese tic.
    # Se declara: a partir del tic en que quedan menos de cinco, no se dibuja.
    rej = list(range(0, 15001, PASO))
    mx, my = [], []
    for t in rej:
        v = []
        for xs, ys in todas:
            if xs[0] <= t <= xs[-1]:
                i = min(range(len(xs)), key=lambda j: abs(xs[j] - t))
                v.append(ys[i])
        if len(v) >= 5:
            mx.append(t); my.append(_st.median(v))
    MED[brazo] = (mx, my)
    ax.plot(mx, my, color=col, linewidth=2.8,
            label=f"{brazo} · mediana (≥5 asientos vivos)")
ax.set_xlabel("tic")
ax.set_ylabel("ignorancia global  (fracción de arena sin ver)")
ax.set_title(f"P5-8M · la ignorancia a lo largo de una vida\n"
             f"{nK} asientos de K contra {nA} de A · cuarenta partidas",
             fontsize=11)
ax.grid(alpha=0.25, linewidth=0.5)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="upper right")
fig.tight_layout()
fig.savefig("cantera/paper5/F1_P58M_ignorancia.png", dpi=150)
print(f"F1 escrita · {nK} curvas de K · {nA} de A")

# ── F2 · una vida de K con sus formas ──
# se elige el asiento de K con mas formas aceptadas
mejor, n_mejor = None, -1
for f in sorted(glob.glob("paintball/runs/P58M_t*_K_*/*.art.log")):
    n = sum(1 for l in open(f) if '"forma_aceptada"' in l)
    if n > n_mejor:
        mejor, n_mejor = f, n
PASO = 25                      # la vida suelta se muestrea fina
xs, ys, recs = curva(mejor)
acep = [json.loads(l) for l in open(mejor) if '"forma_aceptada"' in l]
caid = [json.loads(l) for l in open(mejor) if '"forma_caida"' in l]
fin_de = {r["id"]: (r["tick"], str(r.get("motivo") or "")) for r in caid}
COL = {"completada": "#137333", "atasco": "#b06000",
       "sin rodeo": "#9334e6", "veto duro": "#c5221f"}
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.plot(xs, ys, color="#1a73e8", linewidth=1.6, label="ignorancia global")
vistos = set()
for a in acep:
    t0 = a["tick"]; t1, mot = fin_de.get(a.get("id"), (t0, "sin fin"))
    cl = next((v for k, v in COL.items() if k in mot), "#5f6368")
    et = next((k for k in COL if k in mot), "sin fin")
    ax.axvspan(t0, max(t1, t0 + 1), color=cl, alpha=0.30,
               label=(et if et not in vistos else None))
    vistos.add(et)
nom = os.path.basename(os.path.dirname(mejor))
ax.set_xlabel("tic")
ax.set_ylabel("ignorancia global")
ax.set_title(f"P5-8M · una vida de K con sus formas\n"
             f"{nom} asiento {mejor.rsplit('_',1)[1][:2]} · "
             f"{len(acep)} formas aceptadas, coloreadas por causa de fin",
             fontsize=11)
ax.grid(alpha=0.25, linewidth=0.5)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig("cantera/paper5/F2_P58M_una_vida.png", dpi=150)
print(f"F2 escrita · {nom} · {len(acep)} formas")
