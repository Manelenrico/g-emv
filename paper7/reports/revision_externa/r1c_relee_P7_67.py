import sys, json, glob, os, time
from multiprocessing import Pool
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__))); from comun import P7, sal; sys.path.insert(0,P7)
sys.dont_write_bytecode=True
import analiza_P7_67 as A
E=json.load(open(P7+"/P7_67F_estado.json"))["peticiones"]
def una(p):
    car=glob.glob(os.path.join(A.RUNS, f"P767F_n{p['nivel']}_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}"))[0]
    out=[]
    for sl in A.HERMANAS:
        r=A.lee_dia(car,sl); out.append(dict(nivel=p['nivel'],serie=p['serie'],dia=p['dia'],brazo=p['brazo'],slot=sl,oportunidad=r['oportunidad'],llegada=r['llegada'],llegadas=r['llegadas'],carpeta=os.path.basename(car)))
    return out
if __name__=="__main__":
    sel=[p for p in E if p['nivel']=='1' and p['brazo'] in ('MIENTE','CONGELADA')]
    if len(sys.argv)>1: sel=sel[:int(sys.argv[1])]
    t=time.time()
    with Pool(6) as po: R=[x for o in po.map(una,sel,chunksize=4) for x in o]
    json.dump(R,open(sal("crudo_n1_MC.json"),"w")); print(len(R), time.time()-t)
