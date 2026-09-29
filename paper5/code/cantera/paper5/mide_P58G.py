"""[P5-8G] Por que pierde la forma · el compromiso simulado · P5-6C F y T."""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0,"cantera/paper4"); sys.path.insert(0,"cantera/paper5")
import serie_util as U, curiosidad as C, curiosidad_forma as CF

def cheb(a,b): return max(abs(a[0]-b[0]),abs(a[1]-b[1]))
def dd(c):  # candidatos: {nombre: d} o {nombre: {"d":..}}
    return {k:(v["d"] if isinstance(v,dict) else v) for k,v in (c or {}).items()}

def analiza(pats, etiqueta, con_compromiso=False, tope=None):
    R={"tics":0,"gana":0,"sin_FM":0,"pierde":0,"dif":[],"contra":collections.Counter(),
       "mueve":0,"acerca":0,"d_nace":[],"d_fin":[],"formas":0,
       "rompe":collections.Counter(),"obedece":0,"coste":[],"llegarian":0,
       "cumple_y_anda":collections.Counter()}
    n=0
    for pat in pats:
        for f in sorted(glob.glob(f"paintball/runs/{pat}/*.art.log")):
            n+=1
            if tope and n>tope: break
            recs=list(U.lee(f))
            pc=next((r for r in recs if r.get("k")=="player_config"),None)
            sm=next((r for r in recs if r.get("k")=="static_map"),None)
            cat=next((r for r in recs if r.get("k")=="catalogo"),None)
            if not(pc and sm and cat): continue
            mundo=U.mundo_de(pc,list(sm["filas"]),cat["items"])
            herm=pc.get("teammate_slot")
            vivos=[r for r in recs if r.get("k")=="tick" and r.get("phase")=="live"]
            por={r["tick"]:r for r in vivos}
            acep={r["id"]:r for r in recs if r.get("k")=="forma_aceptada"}
            fin={r["id"]:r["tick"] for r in recs if r.get("k")=="forma_caida"}
            # los tics con forma activa: de forma_tic o cur_forma_tic
            act=collections.defaultdict(list)
            for r in recs:
                if r.get("k")=="cur_forma_tic" and r.get("activa"):
                    act[r["activa"]].append(r["tick"])
                elif r.get("k")=="forma_tic":
                    for i in (r.get("respaldo") or [])+(r.get("nuevos") or []):
                        act[i].append(r["tick"])
            # cumple proyeccion, por forma (P5-6C)
            cum=collections.defaultdict(lambda:[0,0])
            for r in recs:
                if r.get("k")=="confianza" and r.get("d_real") is not None:
                    c=cum[r.get("id")]; c[1]+=1
                    c[0]+= (r["d_real"]<=r["d_proyectada"]+0.05)
            for fid,a in acep.items():
                tics=sorted(act.get(fid) or [])
                if not tics: continue
                R["formas"]+=1
                tr=(a.get("tramos") or [{}])[0]
                dest=tuple(tr.get("destino") or ()) or None
                p0=tuple((por.get(tics[0]) or {}).get("pos") or ())
                pl=tuple((por.get(tics[-1]) or {}).get("pos") or ())
                if dest and p0: R["d_nace"].append(cheb(p0,dest))
                if dest and pl: R["d_fin"].append(cheb(pl,dest))
                if dest and p0 and cheb(p0,dest)*11 <= (tics[-1]-tics[0]):
                    R["llegarian"]+=1
                prev=p0; dano=[]
                for t in tics:
                    r=por.get(t)
                    if not r: continue
                    R["tics"]+=1
                    ra=r.get("RADIOGRAFIA") or {}
                    cands=dd(ra.get("candidatos"))
                    el=ra.get("elegido")
                    fm=next((k for k in cands if k.startswith("_FM_")),None)
                    p=tuple(r.get("pos") or ())
                    if p and prev and p!=prev: R["mueve"]+=1
                    if p and prev and dest and cheb(p,dest)<cheb(prev,dest):
                        R["acerca"]+=1
                    if fm is None:
                        R["sin_FM"]+=1
                    elif el==fm:
                        R["gana"]+=1
                    else:
                        R["pierde"]+=1
                        R["contra"][str(el)]+=1
                        if el in cands:
                            R["dif"].append(cands[fm]-cands[el])
                    if con_compromiso and fm is not None:
                        # las condiciones de ruptura
                        dt=sum(float(x.get("amount") or 0) if isinstance(x,dict) else 0.0
                               for x in (r.get("damage_taken") or []))
                        arms=CF.armados(r,mundo,herm)
                        a_tiro=p and any(cheb(p,q)<=rg for q,rg in arms)
                        veto_d=dest and CF.abandona_por_peligro(dest,[p] if p else [],r,mundo,herm)
                        hp=float(r.get("hp") or 100)
                        cerca=False
                        for ag in (r.get("ve_agentes") or []):
                            if ag.get("slot")!=herm and ag.get("pos") and p:
                                if cheb(p,tuple(ag["pos"]))<6: cerca=True
                        rota=None
                        if a_tiro: rota="a) veto vital"
                        elif veto_d: rota="b) veto duro"
                        elif dt>0: rota="c) dano recibido"
                        elif hp<15: rota="d) vida < 15"
                        elif cerca: rota="e) rival a menos de 6"
                        if rota: R["rompe"][rota]+=1
                        else:
                            R["obedece"]+=1
                            if el!=fm and el in cands:
                                R["coste"].append(cands[fm]-cands[el])
                    prev=p
                if fid in cum and cum[fid][1]:
                    ok = cum[fid][0]==cum[fid][1]
                    anda = bool(dest and p0 and pl and cheb(pl,dest)<cheb(p0,dest))
                    R["cumple_y_anda"][(ok,anda)]+=1
    return R

def q(v):
    if not v: return "—"
    s=sorted(v); n=len(s)
    return f"mediana {st.median(s):+.5f} · Q1 {s[n//4]:+.5f} · Q3 {s[3*n//4]:+.5f}"

if __name__=="__main__":
    que=sys.argv[1] if len(sys.argv)>1 else "K"
    if que=="K":
        R=analiza(["P58B_t1_K_*","P58D_t1_K_*","P58E_t1_K_*"],"K",con_compromiso=True)
    else:
        R=analiza([f"P56C_t{t}_{que}_*" for t in (1,2)],que,tope=24)
    json.dump({k:({str(a):b for a,b in v.items()}
                  if isinstance(v,(dict,collections.Counter)) else v)
               for k,v in R.items()},
              open(f"cantera/paper5/P58G_{que}.json","w"),default=str)
    print(f"=== {que}: {R['formas']} formas · {R['tics']:,} tics con forma activa ===")
    print(f"  gana la forma {R['gana']} = {100*R['gana']/max(1,R['tics']):.2f} % · "
          f"pierde {R['pierde']} · el candidato NO ESTA (veto) {R['sin_FM']} = "
          f"{100*R['sin_FM']/max(1,R['tics']):.2f} %")
    print(f"  d(forma) - d(ganador) en las derrotas: {q(R['dif'])}  (positivo = la forma es PEOR)")
    print(f"  pierde contra: {dict(R['contra'].most_common(6))}")
    print(f"  se mueve {100*R['mueve']/max(1,R['tics']):.2f} % · acerca "
          f"{100*R['acerca']/max(1,R['tics']):.2f} % · d {st.median(R['d_nace']) if R['d_nace'] else '—'}"
          f" -> {st.median(R['d_fin']) if R['d_fin'] else '—'}")
    if R["cumple_y_anda"]:
        print(f"  (cumple proyeccion, anduvo): {dict(R['cumple_y_anda'])}")
    if R["rompe"] or R["obedece"]:
        tot=sum(R["rompe"].values())+R["obedece"]
        print(f"\n  == EL COMPROMISO ==")
        print(f"  obedeceria la forma en {R['obedece']}/{tot} = {100*R['obedece']/max(1,tot):.2f} % de los tics")
        for k,v in R["rompe"].most_common():
            print(f"     rompe {k:24s} {v:6d} = {100*v/max(1,tot):5.2f} %")
        print(f"  llegarian al destino (11 tics/casilla, sin rupturas): {R['llegarian']}/{R['formas']}")
        cs=R["coste"]
        print(f"  COSTE del compromiso (suma de d_forma - d_ganador en lo desobedecido): "
              f"{sum(cs):+.3f} en {len(cs)} tics · por tic {st.mean(cs) if cs else 0:+.5f}")
