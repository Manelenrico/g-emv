import glob, json, os, re, zipfile, collections
from comun import RUNS, P7
K=(b'{"k":"P7_54_evaluada"',b'{"k":"P7_62_evaluada"',b'{"k":"P7_57_contraste"',b'{"k":"P7_62_contraste"',b'{"k":"P7_63_contraste"')
def fuentes():
    for d in sorted(glob.glob(RUNS+"/P7[56]*")):
        g=os.path.basename(d).split("_")[0]
        for z in glob.glob(d+"/*.zip"):
            zf=zipfile.ZipFile(z)
            for n in zf.namelist():
                if n.endswith(".log"): yield g, (lambda zf=zf,n=n: zf.open(n))
    for d in sorted(glob.glob(P7+"/_P7_*local*")+glob.glob(P7+"/_P7_*humo_local*")):
        if not os.path.isdir(d): continue
        g=os.path.basename(d)
        for f in glob.glob(d+"/**/policy_agent_*.log",recursive=True): yield g, (lambda f=f: open(f,"rb"))
def regla(p,v):
    if abs(p)<1e-9: return 1 if abs(v)<1.0 else 0
    return 1 if (p>0)==(v>0) and abs(v)>=abs(p)/2 else 0
C=collections.defaultdict(lambda: collections.Counter()); EJ=collections.defaultdict(list)
for g,op in fuentes():
    for line in op():
        if not line.startswith(b'{"k":"P7_'): continue
        if not any(line.startswith(k) for k in K): continue
        r=json.loads(line); k=r["k"]; c=C[(g,k)]; c["registros"]+=1
        if k.endswith("evaluada"):
            for dim in ("cuerpo","recursos","vinculo"):
                p=float((r.get("prometido") or {}).get(dim) or 0.0); v=float((r.get("vivido") or {}).get(dim) or 0.0); a=(r.get("acierto") or {}).get(dim)
                s="neg" if p< -1e-9 else ("cero" if abs(p)<1e-9 else "pos")
                c[f"{dim}:{s}"]+=1; c[f"{dim}:{s}:acierto"]+= (a or 0)
                if s=="cero" and abs(v)>=1: c[f"{dim}:cero:vivido>=1(fallo)"]+=1
                if s=="cero" and v>=1: c[f"{dim}:cero:vivido>=+1(ganancia, fallo)"]+=1
                if s=="neg" and len(EJ[(g,k)])<6: EJ[(g,k)].append((r.get("accion"),dim,p,v,a,r.get("fuente")))
                if k=="P7_54_evaluada" and a is not None and a!=regla(p,v): c[f"{dim}:discrepa_regla"]+=1
        else:
            for p in r.get("promesas") or []:
                s="neg" if p< -1e-9 else ("cero" if abs(p)<1e-9 else "pos"); c[f"cuerpo:{s}"]+=1
                if s=="neg" and len(EJ[(g,k)])<6: EJ[(g,k)].append((r.get("acciones"),p,r.get("efecto_contado"),r.get("acierto")))
for key in sorted(C): print(key, dict(sorted(C[key].items())))
print("--- ejemplos negativos")
for key in EJ: print(key, EJ[key])
