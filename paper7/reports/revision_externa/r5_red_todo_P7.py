# solo lectura: todas las carpetas P7* de paintball/runs; cuenta red en mano, ataques con red en mano, rivales enredados, huellas de red
import glob, json, os, re, zipfile, collections as C
from comun import RUNS
R=C.defaultdict(C.Counter); ej=[]
def lineas(f):
    if f.endswith(".zip"):
        with zipfile.ZipFile(f) as Z:
            for n in Z.namelist():
                with Z.open(n) as fh:
                    for raw in fh: yield raw.decode("utf-8","replace")
    else:
        with open(f,errors="replace") as fh:
            for l in fh: yield l
for d in sorted(glob.glob(RUNS+"/P7*")):
    camp=os.path.basename(d).split("_")[0]
    fs=[f for f in glob.glob(d+"/*") if re.search(r'policy_agent_\d+\.(zip|art\.log)$',f)]
    for f in fs:
        R[camp]["diarios"]+=1
        for l in lineas(f):
            if l.startswith('{"k":"tick"'):
                R[camp]["ticks"]+=1
                if l.startswith('{"k":"tick"') and '"hand":{"id":"net"' in l[:400]:
                    R[camp]["ticks_red_en_mano"]+=1
                    if '"intencion":{"type":"action","do":"attack"' in l:
                        R[camp]["ATAQUE_con_red"]+=1
                        if len(ej)<20: ej.append((d,f,l[:200]))
                if '"netted":true' in l: R[camp]["ticks_con_agente_visto_enredado"]+=1
            elif l.startswith('{"k":"P7_huella"') and '"objeto":"net"' in l: R[camp]["huellas_red"]+=1
            elif l.startswith('{"k":"P7_33_prueba"') and '"objeto":"net"' in l and '"abre"' in l: R[camp]["abre_red"]+=1
json.dump({"por_campo":R,"ejemplos":ej},open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"escaneo_todo.json"),"w"),indent=1)
print("ok")
