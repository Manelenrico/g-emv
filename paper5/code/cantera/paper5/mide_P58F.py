"""[P5-8F] Que hace el cuerpo mientras «sigue» una forma. Diagnostico, en seco."""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0,"cantera/paper4"); sys.path.insert(0,"cantera/paper5")
import serie_util as U, curiosidad as C

def cheb(a,b): return max(abs(a[0]-b[0]),abs(a[1]-b[1]))

OUT=[]
for pat in ("P58B_t1_K_*","P58D_t1_K_*","P58E_t1_K_*"):
    for f in sorted(glob.glob(f"paintball/runs/{pat}/*.art.log")):
        recs=list(U.lee(f))
        pc=next((r for r in recs if r.get("k")=="player_config"),None)
        sm=next((r for r in recs if r.get("k")=="static_map"),None)
        cat=next((r for r in recs if r.get("k")=="catalogo"),None)
        if not(pc and sm and cat): continue
        mundo=U.mundo_de(pc,list(sm["filas"]),cat["items"])
        vivos=[r for r in recs if r.get("k")=="tick" and r.get("phase")=="live"]
        por_tic={r["tick"]:r for r in vivos}
        ctic={r["tick"]:r for r in recs if r.get("k")=="cur_forma_tic"}
        prop={r["id"]:r for r in recs if r.get("k")=="forma_propuesta" and r.get("origen")=="curiosidad"}
        acep={r["id"]:r["tick"] for r in recs if r.get("k")=="forma_aceptada"}
        fin={r["id"]:(r["tick"],str(r.get("motivo") or "")) for r in recs if r.get("k")=="forma_caida"}
        # el ojo, reproducido tic a tic (la MISMA clase que usa el BFS)
        ojo=C.Ojo(mundo,8); visto_en={}
        for r in vivos:
            p=tuple(r.get("pos") or ())
            if not p: continue
            for c in ojo.vistas_desde(p):
                visto_en.setdefault(c,r["tick"])
            ojo.mira(p,r["tick"])
        nom=os.path.basename(os.path.dirname(f))+"/"+f.rsplit("_",1)[1][:2]
        for fid,t0 in acep.items():
            p0=prop.get(fid)
            if not p0 or not p0.get("destino"): continue
            dest=tuple(p0["destino"])
            t1,motivo=fin.get(fid,(vivos[-1]["tick"],"sin fin"))
            tics=[t for t in range(t0,t1+1) if t in por_tic]
            if len(tics)<2: continue
            mueve=acerca=0
            gana_forma=0; n_dec=0
            prev=tuple(por_tic[tics[0]].get("pos") or ())
            d_nace=cheb(prev,dest)
            for t in tics[1:]:
                p=tuple(por_tic[t].get("pos") or ())
                if not p: continue
                if p!=prev: mueve+=1
                if cheb(p,dest)<cheb(prev,dest): acerca+=1
                prev=p
                ra=(por_tic[t].get("RADIOGRAFIA") or {})
                if ra.get("elegido"):
                    n_dec+=1
                    if str(ra["elegido"]).startswith("_FM_"): gana_forma+=1
            d_fin=cheb(prev,dest)
            # las casillas «del camino y del destino» no vistas al nacer
            objetivo=set()
            for c in ojo.vistas_desde(dest): objetivo.add(c)
            objetivo={c for c in objetivo if visto_en.get(c,10**9)>=t0}
            antes=sum(1 for c in objetivo if visto_en.get(c,10**9)<t0)
            durante=sum(1 for c in objetivo if t0<=visto_en.get(c,10**9)<=t1)
            despues=sum(1 for c in objetivo if t1<visto_en.get(c,10**9)<=t1+100)
            nunca=len(objetivo)-antes-durante-despues
            OUT.append({"asiento":nom,"id":fid,"motivo":motivo[:26],
                        "vive":t1-t0,"tics":len(tics),
                        "mueve":mueve,"acerca":acerca,"n_dec":n_dec,
                        "gana_forma":gana_forma,
                        "d_nace":d_nace,"d_fin":d_fin,
                        "obj":len(objetivo),"durante":durante,
                        "despues":despues,"nunca":nunca})
json.dump(OUT,open("cantera/paper5/P58F.json","w"))
print(f"{len(OUT)} formas aceptadas analizadas")
