"""[P7-14b] EL BANCO DEL ARREGLO "en un empate no se da ni se suelta nada" (un subproceso por vida; sin partidas ni llamadas):
  (1) los 24 regalos del brazo SUELO en P7-10 (los empates de P7-11): se replican sus vidas con el brazo ESPERANZA tal como se jugaron (pedir
      apagado) y el arreglo, y en cada tic en que el campo regalo se mira que elige la replica;
  (2) el F2 de P7-13 otra vez (`banco_P7_13.py --f2`: los 171 regalos de APRENDE en P7-10 con pedir), ahora con el arreglo.
-> P7_14b_banco.json y P7_14b_F2.json"""
import collections, glob, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import banco_P7_13 as B13
if __name__ == "__main__":
    os.makedirs(B13.SAL, exist_ok=True); V = json.load(open(os.path.join(AQUI, "P7_11_vidas.json"))); SU = {k: v for k, v in V.items() if v["brazo"] == "SUELO" and v["regala"]}
    def una(k):
        v = SU[k]; carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P710_s{v['serie']}_d{v['dia']}_SUELO_*"))[0])
        cu = os.path.join(B13.SAL, "cuad_14b_" + k); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
        tf = os.path.join(B13.SAL, f"14b_tics_{k}.json"); json.dump(sorted({g["t_dec"] for g in v["regala"]}), open(tf, "w"))
        return k, B13.lanza(carp, v["slot"], "ESPERANZA", cu, 0, os.path.join(B13.SAL, f"14b_suelo_{k}.json"), tics=tf)
    with ThreadPoolExecutor(8) as ex: R = dict(ex.map(una, list(SU)))
    err = [k for k, r in R.items() if r.get("error")]
    if err: sys.exit("ERROR " + err[0] + " " + R[err[0]]["error"][-400:])
    regalos = []; fid = collections.Counter()
    for k, r in R.items():
        fid.update(r["fidelidad"])
        for g in SU[k]["regala"]:
            e = r["en_tics"].get(str(g["t_dec"])) or {}; d = e.get("d") or {}
            regalos.append({"vida": k, "t": g["t_dec"], "elegido_replica": e.get("elegido"), "sigue_regalando": str(e.get("elegido")).startswith("soltar_"), "d_soltar": d.get("soltar_first_aid"), "d_noop": d.get("noop"),
                            "era_empate": (d.get("soltar_first_aid") is not None and d.get("noop") is not None and abs(d["soltar_first_aid"] - d["noop"]) < 1e-9)})
    S1 = {"vidas": len(R), "regalos_del_campo": len(regalos), "eran_empate_con_noop": sum(1 for g in regalos if g["era_empate"]), "la_replica_sigue_regalando": sum(1 for g in regalos if g["sigue_regalando"]),
          "elige": dict(collections.Counter(g["elegido_replica"] for g in regalos)), "fidelidad": dict(fid), "regalos": regalos}
    print("SUELO:", {k: v for k, v in S1.items() if k != "regalos"}, flush=True)
    r = subprocess.run([sys.executable, os.path.join(AQUI, "banco_P7_13.py"), "--f2"], capture_output=True, text=True); print(r.stdout[-600:], r.stderr[-300:])
    shutil.copy(os.path.join(AQUI, "P7_13_F2.json"), os.path.join(AQUI, "P7_14b_F2.json")); subprocess.run(["git", "-C", AQUI, "checkout", "P7_13_F2.json"])
    F2 = json.load(open(os.path.join(AQUI, "P7_14b_F2.json"))); G = F2["regalos"]
    json.dump({"suelo": S1, "F2": {**F2["resumen"], "con_pedido_y_sigue": sum(1 for g in G if g["hermano_pide"] and g["sigue_regalando"]), "sin_pedido_y_sigue": sum(1 for g in G if not g["hermano_pide"] and g["sigue_regalando"]), "fidelidad_pase2": F2["fidelidad_pase2"]}}, open(os.path.join(AQUI, "P7_14b_banco.json"), "w"), ensure_ascii=False, indent=1)
    print("F2:", json.load(open(os.path.join(AQUI, "P7_14b_banco.json")))["F2"])
