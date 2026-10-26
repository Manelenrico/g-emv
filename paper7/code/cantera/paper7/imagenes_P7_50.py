"""[P7-50, Manel 12-oct] COMPROBACION DE IMAGENES: con que version/imagen se jugo CADA partida del campo (por serie y brazo) y que todas llevan las mismas piezas.
De P7_50_estado.json: por peticion, la clave de imagen, la etiqueta (gemv-p7-campo:vNNN), el policy_version_id pedido (pvid) y el registrado para esa imagen, los cuadernos
horneados; del diario de cada asiento: las piezas (`P7_49_arranque_campo`), el modo (`P7_48_arranque`), el MIEDO del asiento (`P7_49_arranque`) y las filas escaladas.
Comprueba: pvid de la peticion == pvid de su imagen; piezas identicas en todas; modo == brazo; MIEDO 0,5 en el 10 y 1,5 en el 11; filas de miedo identicas. Ademas, con
`git log`, que ningun archivo que la imagen copia cambio desde la primera subida del campo.  python3 imagenes_P7_50.py -> P7_50_imagenes.json"""
import glob, json, os, re, subprocess
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
E = json.load(open(os.path.join(AQUI, "P7_50_estado.json"))); IM = E["imagenes"]
filas = []; piezas_set = set(); miedo_set = set(); avisos = []
for p in sorted(E["peticiones"], key=lambda p: (p["serie"], p["brazo"], p["dia"])):
    im = IM.get(p["imagen"]) or {}; f = {"serie": p["serie"], "dia": p["dia"], "brazo": p["brazo"], "imagen": p["imagen"], "etiqueta": im.get("etiqueta"), "version": im.get("version"), "pvid_pedido": p.get("pvid"), "pvid_imagen": im.get("policy_version_id"), "pvid_coincide": p.get("pvid") == im.get("policy_version_id"), "cuadernos_horneados": im.get("cuadernos_horneados"), "estado": p["estado"], "asientos": {}}
    for sl in (10, 11):
        fs = glob.glob(os.path.join(RUNS, f"P750_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}", f"*policy_agent_{sl}.art.log")); a = {}
        if fs:
            for line in open(fs[0], errors="replace"):
                if line.startswith('{"k":"P7_49_arranque_campo"'): r = json.loads(line); a["piezas"] = r.get("piezas"); a["brazo_imagen"] = r.get("brazo")
                elif line.startswith('{"k":"P7_48_arranque"'): r = json.loads(line); a["modo"] = r.get("modo"); a["ya_recibidos"] = r.get("ya_recibidos"); a["noche"] = len(r.get("noche") or [])
                elif line.startswith('{"k":"P7_49_arranque"'): r = json.loads(line); a["miedo"] = r.get("miedo"); a["filas"] = r.get("filas"); a["miedo_v"] = r.get("miedo_v"); a["miedo_p"] = r.get("miedo_p")
                elif line.startswith('{"k":"tick"'): break
            if a.get("piezas"): piezas_set.add(tuple(a["piezas"]))
            if a.get("filas"): miedo_set.add((tuple(a["filas"]), a.get("miedo_v"), a.get("miedo_p")))
            if a.get("modo") and a["modo"] != p["brazo"].lower(): avisos.append(f"s{p['serie']} d{p['dia']} {p['brazo']} a{sl}: modo {a['modo']} != brazo")
            if a.get("miedo") is not None and a["miedo"] != (0.5 if sl == 10 else 1.5): avisos.append(f"s{p['serie']} d{p['dia']} {p['brazo']} a{sl}: MIEDO {a['miedo']}")
        f["asientos"][sl] = a
    if not f["pvid_coincide"]: avisos.append(f"s{p['serie']} d{p['dia']} {p['brazo']}: pvid pedido {p.get('pvid')} != imagen {im.get('policy_version_id')}")
    if p["dia"] > 1 and im.get("cuadernos_horneados") is not None and len(im["cuadernos_horneados"]) < 2: avisos.append(f"s{p['serie']} d{p['dia']} {p['brazo']}: cuadernos horneados {im.get('cuadernos_horneados')}")
    filas.append(f)
# los archivos que copia la imagen: ¿cambio alguno desde la primera subida del campo?
copiados = [l.split()[1] for l in open(os.path.join(AQUI, "Dockerfile.pareja_P7_49")) if l.startswith("COPY ") and len(l.split()) >= 3]
primera = min((im.get("subida_a_las") or "9") for im in IM.values())
log = subprocess.run(["git", "log", "--since", primera, "--name-only", "--format=%h %ci %s", "--"] + copiados, capture_output=True, text=True, cwd=RAIZ).stdout.strip()
R = {"partidas": filas, "piezas_distintas": [list(x) for x in piezas_set], "miedo_distintos": [[list(x[0]), x[1], x[2]] for x in miedo_set], "avisos": avisos, "primera_subida": primera, "cambios_en_archivos_copiados_desde_la_primera_subida": log or "ninguno", "versiones": sorted({f["version"] for f in filas if f["version"] is not None})}
json.dump(R, open(os.path.join(AQUI, "P7_50_imagenes.json"), "w"), ensure_ascii=False, indent=1)
print("partidas", len(filas), "piezas distintas", len(piezas_set), "miedo distintos", len(miedo_set), "avisos", avisos, "cambios copiados:", (log or "ninguno")[:300])
