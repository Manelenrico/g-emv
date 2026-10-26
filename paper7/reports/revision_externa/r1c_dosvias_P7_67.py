import json, numpy as np
from comun import sal
R=json.load(open(sal("crudo_n1_MC.json")))
def cr(X,y,g):
    XtXi=np.linalg.inv(X.T@X); b=XtXi@X.T@y; e=y-X@b; M=np.zeros((X.shape[1],)*2); G=np.unique(g)
    for v in G:
        s=X[g==v].T@e[g==v]; M+=np.outer(s,s)
    G_=len(G); n=len(y); k=X.shape[1]; c=G_/(G_-1)*(n-1)/(n-k)
    return b, XtXi@M@XtXi*c
def run(rows, cols):
    y=np.array([c['llegada'] for c in rows],float)
    X=np.column_stack([np.ones(len(rows))]+[f(rows) for f in cols])
    s=np.array([c['serie'] for c in rows]); d=np.array([c['dia'] for c in rows]); sd=np.array([c['serie']*100+c['dia'] for c in rows])
    b,Vs=cr(X,y,s); _,Vd=cr(X,y,d); _,Vsd=cr(X,y,sd); V2=Vs+Vd-Vsd
    j=X.shape[1]-1
    for nm,V in (("serie",Vs),("dia",Vd),("dos vias",V2)): print("  coef %.4f ee[%s] %.4f z %.2f"%(b[j],nm,np.sqrt(V[j,j]),b[j]/np.sqrt(V[j,j])))
o=[c for c in R if c['oportunidad']]
M=[c for c in o if c['brazo']=='MIENTE']
print("P1 nivel criatura-dia, MIENTE, y=llegada ~ B:"); run(M,[lambda r: np.array([c['dia']>10 for c in r],float)])
print("P2: y ~ MIENTE + B + MIENTE*B (coef interaccion):")
run(o,[lambda r: np.array([c['brazo']=='MIENTE' for c in r],float), lambda r: np.array([c['dia']>10 for c in r],float), lambda r: np.array([(c['brazo']=='MIENTE')*(c['dia']>10) for c in r],float)])
