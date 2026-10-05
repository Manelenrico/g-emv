"""[P6-5 · 5b] LA SORDERA DE A1: el parte del hermano no se leyo. SOLO LECTURA.

Sale de investigar el punto 5. El cuerpo del cinco lee el parte del hermano en
UN solo sitio, con un parser ESTRICTO:

    appraisal_zs_v42_exp.py:578     p = PARTE.parsea(m.get("text") or "")
    parte.py:48                     r"^E1 P(\\d+) t(\\d+) ..."

`policy_pareja` cambia la emision a E2 (`parte2.MARCA = "E2"`), y `AlmaPareja.
_oye_e2` parsea el E2 para SU uso (inyectar lo contado), pero NADIE vuelve a
poner la cabeza del parte donde el cuerpo del cinco la busca. El parser del
cinco ve la marca `E2` y devuelve None. Resultado: en el brazo A1, `mem.parte`
es None SIEMPRE y `mem.parte_fresco(tick)` tambien.

Esto apaga, en cascada, todo lo que el cinco sabia de su hermano por el canal:
  `_hermana_b0`            -> False siempre  (S-PROVISION y el don por provision)
  `_provision_calma`       -> False siempre
  `agresor_de_la_hermana`  -> None siempre   (la manada no caza por parte)
  `pareja_hp_est`          -> BANDA_EST (healthy = 83, no 100) en vez del hp exacto

QUE MIDE, por brazo (A0 = E1, A1 = E2):
  1. partes del hermano recibidos, y cuantos pasan el parser ESTRICTO del cinco.
  2. censo de filas de la tabla (que se enciende y que se apaga).
  3. disponibilidad del candidato `soltar_*` y quien le gana.
  4. familias de elegido.
  5. la puerta de la herida (hermano visible y herido, con consumible en mano).

Uso:
  python3 mide_sordera_P6_5.py A0=paintball/runs/P64_t[13]_A0_* A1=paintball/runs/P64_t[24]_A1_*
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
import serie_util as U
from alma import parte as PARTE          # el parser ESTRICTO del cinco, tal cual

NUESTROS = (10, 11)
CONSUMIBLES = ("first_aid", "rations")


def fam(e):
    e = str(e or "")
    for p in ("soltar_", "usar_", "ir_", "move_", "paso_", "atacar", "coger",
              "noop", "empunar", "ponerse_"):
        if e.startswith(p):
            return p.rstrip("_")
    return e or "otro"


def mide(pat):
    C, FILAS, ELEG, GANA = collections.Counter(), collections.Counter(), \
        collections.Counter(), collections.Counter()
    vistos = set()
    for f in sorted(glob.glob(os.path.join(pat, "*policy_agent_1*.art.log"))):
        sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
        if sl not in NUESTROS:
            continue
        par = 11 if sl == 10 else 10
        C["asientos"] += 1
        for r in U.lee(f):
            if r.get("k") != "tick" or r.get("phase") != "live":
                continue
            C["tics"] += 1
            ra = r.get("RADIOGRAFIA") or {}
            ELEG[fam(ra.get("elegido"))] += 1
            # 1 · el parte del hermano, por el parser DEL CINCO
            for m in (r.get("chat") or []):
                if m.get("from") != par or m.get("channel") != "team":
                    continue
                k = (f, m.get("tick"))
                if k in vistos:
                    continue
                vistos.add(k)
                C["partes del hermano"] += 1
                p = PARTE.parsea(m.get("text") or "")
                if p is None:
                    C["  NO los lee el cinco (parser estricto)"] += 1
                else:
                    C["  los LEE el cinco"] += 1
                    C["    b=0" if int(p.get("botiquin") or 0) == 0
                      else "    b>=1"] += 1
            # 2 · censo de filas
            fl = (ra.get("ahora") or {}).get("filas") or {}
            if fl:
                C["tics con tabla"] += 1
                for k in fl:
                    FILAS[k] += 1
            # 3 · disponibilidad de `soltar_*`
            cd = ra.get("candidatos") or {}
            if any(k.startswith("soltar_") for k in cd):
                C["`soltar_*` DISPONIBLE"] += 1
                if not str(ra.get("elegido") or "").startswith("soltar_"):
                    GANA[fam(ra.get("elegido"))] += 1
            # 5 · la puerta de la herida
            cons = sum(int((s or {}).get("n") or 1) for s in (r.get("pack") or [])
                       if s and s.get("id") in CONSUMIBLES)
            if cons:
                C["con consumible en la mochila"] += 1
            p = next((a for a in (r.get("ve_agentes") or [])
                      if a.get("slot") == par and not a.get("_contado")), None)
            if p is not None and (p.get("hp_band") or "healthy") != "healthy":
                C["hermano visible y HERIDO"] += 1
                if cons:
                    C["  ...y yo con consumible (PUERTA DE LA HERIDA)"] += 1
    return C, FILAS, ELEG, GANA


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    C, FILAS, ELEG, GANA = mide(os.path.join(RAIZ, pat))
    n = C["tics"] or 1
    OUT[etiq] = {"recuento": dict(C), "filas": dict(FILAS),
                 "elegido": dict(ELEG), "gana_a_soltar": dict(GANA)}
    print(f"### {etiq}  ({C['asientos']} asientos · {C['tics']} tics)")
    for k in ("partes del hermano", "  los LEE el cinco",
              "  NO los lee el cinco (parser estricto)", "    b=0", "    b>=1",
              "`soltar_*` DISPONIBLE", "hermano visible y HERIDO",
              "  ...y yo con consumible (PUERTA DE LA HERIDA)",
              "con consumible en la mochila"):
        if k in C:
            print(f"   {k:46s} {C[k]:8d}")
    print("   -- filas --")
    for k, v in FILAS.most_common():
        print(f"      {k:22s} {v:8d}  {100 * v / (C['tics con tabla'] or 1):6.2f} %")
    print("   -- elegido --")
    for k, v in ELEG.most_common():
        print(f"      {k:10s} {v:8d}  {100 * v / n:6.2f} %")
    if GANA:
        print("   -- gana a `soltar_*` cuando esta disponible --")
        for k, v in GANA.most_common():
            print(f"      {k:10s} {v:8d}")
if len(OUT) == 2:
    (a, A), (b, B) = OUT.items()
    na = A["recuento"].get("tics con tabla") or 1
    nb = B["recuento"].get("tics con tabla") or 1
    print(f"\n### {b} - {a}, filas, en puntos porcentuales")
    for k in sorted(set(A["filas"]) | set(B["filas"]),
                    key=lambda x: 100 * B["filas"].get(x, 0) / nb
                    - 100 * A["filas"].get(x, 0) / na):
        pa, pb = 100 * A["filas"].get(k, 0) / na, 100 * B["filas"].get(k, 0) / nb
        print(f"   {k:22s} {a} {pa:6.2f} %  {b} {pb:6.2f} %  d {pb - pa:+7.2f}")
json.dump(OUT, open(os.path.join(AQUI, "P6_5_sordera.json"), "w"),
          ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_5_sordera.json")
