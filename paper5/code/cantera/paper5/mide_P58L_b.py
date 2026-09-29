"""[P5-8L·2b] ¿El veto salta porque el armado APARECE? ¿Nacia ya condenada?"""
import collections, glob, json, os, sys, statistics as st
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U
from serie_util import D, DOV
import banco_llaves as B
import curiosidad as C, curiosidad_forma as CFM
from alma import appraisal_zs_v42_exp as V42
def cheb(a,b): return max(abs(a[0]-b[0]),abs(a[1]-b[1]))
OUT=[]
for sonda,pat in (("I","P58I_t1_K_*"),("K","P58K_t0_K_*")):
    for f in sorted(glob.glob(f"paintball/runs/{pat}/*.art.log")):
        recs=list(U.lee(f))
        pc=next((r for r in recs if r.get("k")=="player_config"),None)
        sm=next((r for r in recs if r.get("k")=="static_map"),None)
        cat=next((r for r in recs if r.get("k")=="catalogo"),None)
        if not(pc and sm and cat): continue
        B.pon_v42(B.interruptores(recs))
        mundo=U.mundo_de(pc,list(sm["filas"]),cat["items"]); herm=pc.get("teammate_slot")
        nom=f"{sonda}/{os.path.basename(os.path.dirname(f)).split('_')[3]}/{f.rsplit('_',1)[1][:2]}"
        vivos=[r for r in recs if r.get("k")=="tick" and r.get("phase")=="live"]
        if not vivos: continue
        por_tic={r["tick"]:r for r in vivos}
        prop={r["tick"]:r for r in recs if r.get("k")=="forma_propuesta" and r.get("origen")=="curiosidad"}
        acep={r["id"] for r in recs if r.get("k")=="forma_aceptada"}
        caida={r["id"]:r for r in recs if r.get("k")=="forma_caida"}
        ojo=C.Ojo(mundo,8); mem,blo,ult=V42.Memoria(),D.Bloqueos(),None; cams={}
        for r in [x for x in recs if x.get("k")=="tick"]:
            t=r["tick"]; o=DOV.a_obs(r); o["you"]["attack_ready_in"]=r.get("attack_ready_in") or 0
            mem.observa(o,mundo,t); blo.actualiza(o,mundo,ult,t); ult=r.get("intencion")
            if r.get("phase")!="live": continue
            p=tuple(r.get("pos") or ())
            if p: ojo.mira(p,t)
            if t in prop and p:
                arms=CFM.armados(r,mundo,herm)
                cam,dist,dest=CFM.camino_a_frontera(ojo,mundo,p,arms)
                if dest is None: continue
                # ¿NACE YA CONDENADA? la MISMA regla que la mata, en el tic de nacer
                cond=CFM.abandona_por_peligro(dest,cam,r,mundo,herm)
                cams[prop[t]["id"]]=(cam,dist,dest,t,cond)
        for fid in sorted(acep):
            if fid not in cams: continue
            cam,dist,dest,t0,cond=cams[fid]
            cr=caida.get(fid); mot=str((cr or {}).get("motivo") or "sin fin"); tf=(cr or {}).get("tick")
            fila={"sonda":sonda,"asiento":nom,"id":fid,"dist":dist,"t0":t0,
                  "motivo":mot[:20],"nace_condenada":bool(cond),"vive":(tf-t0) if tf else None}
            if mot.startswith("veto duro") and tf in por_tic:
                r=por_tic[tf]; pos=tuple(r.get("pos") or ())
                try: i=cam.index(pos)
                except ValueError: i=0
                resto=cam[i:] or cam; quien=None
                for a in (r.get("ve_agentes") or []):
                    if a.get("slot")==herm or not a.get("pos"): continue
                    rg=C._alcance(mundo,a.get("hand"))
                    if rg<=0: continue
                    if any(cheb(x,tuple(a["pos"]))<=rg for x in resto): quien=a; break
                if quien:
                    sl=quien["slot"]
                    # ¿desde cuando es visible? y ¿estaba armado antes?
                    visto=[t for t in range(t0,tf+1) if t in por_tic
                           and any(b.get("slot")==sl for b in (por_tic[t].get("ve_agentes") or []))]
                    fila["culpable"]=sl
                    fila["tics_visible_antes"]=len([t for t in visto if t<tf])
                    fila["aparece_en_el_tic"]=(len([t for t in visto if t<tf])==0)
                    fila["visible_al_nacer"]=bool(visto and visto[0]==t0)
            OUT.append(fila)
json.dump(OUT,open("cantera/paper5/P58L_b.json","w"))
V=[x for x in OUT if x.get("culpable") is not None]
print(f"=== ¿NACE YA CONDENADA POR SU PROPIA REGLA DE MUERTE? ===")
for s in ("I","K"):
    S=[x for x in OUT if x["sonda"]==s]
    if not S: continue
    print(f"  P5-8{s}: {sum(1 for x in S if x['nace_condenada'])} de {len(S)} aceptadas nacen con el camino YA cubierto")
print(f"\n=== ¿EL ARMADO APARECE EN EL TIC DEL VETO? ({len(V)} vetos) ===")
ap=sum(1 for x in V if x.get("aparece_en_el_tic"))
vn=sum(1 for x in V if x.get("visible_al_nacer"))
tv=[x["tics_visible_antes"] for x in V]
print(f"  NO se habia visto nunca desde que nacio la forma: {ap}/{len(V)} = {100.0*ap/len(V):.1f}%")
print(f"  ya era visible EN EL TIC DE NACER             : {vn}/{len(V)} = {100.0*vn/len(V):.1f}%")
print(f"  tics visible antes del veto: mediana {st.median(tv)} · max {max(tv)}")
print(f"\n=== cuanto vive una forma que muere por veto duro ===")
vv=[x["vive"] for x in V if x["vive"] is not None]
print(f"  min {min(vv)} · mediana {st.median(vv)} · max {max(vv)} tics")
print(f"  mueren en el PRIMER tic de vida: {sum(1 for x in vv if x<=1)}/{len(vv)}")
