import json, statistics as st, math, collections as C
from comun import P7, sal
R=json.load(open(sal("crudo_n1_MC.json")))
J=json.load(open(P7+"/P7_67_analisis.json"))
# check consistency with sealed detalle
D={(c['nivel'],c['serie'],c['dia'],c['brazo'],c['slot']):(c['oportunidad'],c['llegada']) for c in J['criatura_dias_detalle']}
print("discrepancias crudo vs detalle:", sum(D[(c['nivel'],c['serie'],c['dia'],c['brazo'],c['slot'])]!=(c['oportunidad'],c['llegada']) for c in R))
A=set(range(1,11)); B=set(range(11,21))
def frac(cs):
    o=[c for c in cs if c['oportunidad']]; return sum(c['llegada'] for c in o)/len(o), len(o)
def pares(brazo):
    U={}
    for s in range(1,17):
        cs=[c for c in R if c['brazo']==brazo and c['serie']==s]
        a=[c for c in cs if c['dia'] in A]; b=[c for c in cs if c['dia'] in B]
        fa,na=frac(a); fb,nb=frac(b); U[s]=(fb-fa,fa,fb,na,nb)
    return U
def me(x): m=st.mean(x); s=st.stdev(x); return m,s,s/math.sqrt(len(x)),len(x)
M=pares('MIENTE'); K=pares('CONGELADA')
m=me([v[0] for v in M.values()]); k=me([v[0] for v in K.values()])
print("P1 MIENTE B-A: media %.4f sd %.4f ee %.4f n %d  z %.2f"%(m[0],m[1],m[2],m[3],m[0]/m[2]))
print("CONGELADA B-A: media %.4f sd %.4f ee %.4f n %d"%k)
ee2=math.sqrt(m[1]**2/16+k[1]**2/16); d=m[0]-k[0]
print("P2 indep: dif %.4f ee %.4f z %.2f"%(d,ee2,d/ee2))
dd=[M[s][0]-K[s][0] for s in range(1,17)]; p=me(dd)
r=st.correlation([M[s][0] for s in M],[K[s][0] for s in K])
print("P2 emparejado por serie (misma semilla): dif %.4f sd %.4f ee %.4f n %d z %.2f ; corr MIENTE-CONG por serie %.3f"%(p[0],p[1],p[2],p[3],p[0]/p[2],r))
# Welch df
v1=m[1]**2/16; v2=k[1]**2/16; df=(v1+v2)**2/(v1**2/15+v2**2/15); print("Welch df %.1f"%df)
for s in range(1,17): print(s, "M B-A %.3f (A %.3f n%d, B %.3f n%d)"%(M[s][0],M[s][1],M[s][3],M[s][2],M[s][4]), "C B-A %.3f"%K[s][0])
# robustez por criatura: cluster by serie
def criat(brazo):
    U={}
    for s in range(1,17):
        for sl in (10,11):
            cs=[c for c in R if c['brazo']==brazo and c['serie']==s and c['slot']==sl]
            a=[c for c in cs if c['dia'] in A]; b=[c for c in cs if c['dia'] in B]
            dA={c['dia'] for c in a if c['oportunidad']}; dB={c['dia'] for c in b if c['oportunidad']}
            if len(dA)>=3 and len(dB)>=3: U[(s,sl)]=frac(b)[0]-frac(a)[0]
    return U
CM=criat('MIENTE'); CK=criat('CONGELADA')
x=me(list(CM.values())); print("por criatura ingenuo MIENTE: media %.4f ee %.4f n %d"%(x[0],x[2],x[3]))
# cluster-robust ee of mean with clusters = serie
def cl(U):
    vals=list(U.values()); mu=st.mean(vals); G=C.defaultdict(float)
    for (s,sl),v in U.items(): G[s]+=v-mu
    N=len(vals); g=len(G); var=g/(g-1)*sum(e*e for e in G.values())/N**2; return mu, math.sqrt(var), g
a=cl(CM); b=cl(CK); print("por criatura, ee por conglomerados (serie): MIENTE %.4f ee %.4f g %d ; CONG %.4f ee %.4f"%(a[0],a[1],a[2],b[0],b[1]))
print("P2 por criatura cluster indep: dif %.4f ee %.4f z %.2f"%(a[0]-b[0], math.hypot(a[1],b[1]), (a[0]-b[0])/math.hypot(a[1],b[1])))
# 'caida de llegadas' en conteos crudos por bloque
for br in ('MIENTE','CONGELADA'):
    for lo in (1,6,11,16):
        cs=[c for c in R if c['brazo']==br and lo<=c['dia']<lo+5]; print(br,lo,sum(c['llegada'] for c in cs), sum(c['oportunidad'] for c in cs))
