import json, statistics as st, math
from comun import P7, sal; import os
R=json.load(open(sal("crudo_n1_MC.json"))); Dz=json.load(open(os.path.join(P7,"P7_67F_diseno.json")))
def fd(br,d):
    cs=[c for c in R if c['brazo']==br and c['dia']==d]; o=[c for c in cs if c['oportunidad']]
    return (sum(c['llegada'] for c in o)/len(o) if o else None), sum(c['llegada'] for c in o), len(o), len({c['serie'] for c in cs if c['llegada']})
F={}
for d in range(1,21):
    m=fd('MIENTE',d); k=fd('CONGELADA',d); F[d]=(m[0],k[0]); print(d,"MIENTE %s/%d (series con llegada %d)"%(m[1],m[2],m[3]),"CONG %s/%d"%(k[1],k[2]))
def t2(a,b):
    ma,mb=st.mean(a),st.mean(b); ee=math.sqrt(st.variance(a)/len(a)+st.variance(b)/len(b)); return mb-ma, ee, (mb-ma)/ee, len(a), len(b)
A=[F[d][0] for d in range(1,11) if F[d][0] is not None]; B=[F[d][0] for d in range(11,21) if F[d][0] is not None]
print("P1 dia como unidad (frac MIENTE por dia; B - A):", "dif %.4f ee %.4f z %.2f nA %d nB %d"%t2(A,B))
dA=[F[d][0]-F[d][1] for d in range(1,11) if F[d][0] is not None]; dB=[F[d][0]-F[d][1] for d in range(11,21) if F[d][0] is not None]
print("P2 dia como unidad (M-C por dia; B - A):", "dif %.4f ee %.4f z %.2f nA %d nB %d"%t2(dA,dB))
print(Dz.keys() if isinstance(Dz,dict) else type(Dz))
