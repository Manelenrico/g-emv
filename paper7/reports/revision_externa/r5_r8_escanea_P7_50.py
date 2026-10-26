# solo lectura: recorre los zips de P750 sin extraer a disco
import glob, json, os, re, zipfile, collections as C
from comun import RUNS
OUT={}
do_c=C.Counter(); hand_c=C.Counter(); do_net=C.Counter(); hu=C.Counter(); hu_motivo=C.Counter(); abre=C.Counter(); netted_rival=0; ev_c=C.Counter()
REC=[]; VIS=[]; HNET=[]
rdo=re.compile(r'"intencion":(\{[^{}]*\})'); rhand=re.compile(r'"hand":\{"id":"([^"]*)"')
for d in sorted(glob.glob(RUNS+"/P750_s*")):
    tag=os.path.basename(d)
    for z in glob.glob(d+"/*.zip"):
        sl=re.search(r'agent_(\d+)',z).group(1)
        with zipfile.ZipFile(z) as Z:
            for name in Z.namelist():
                with Z.open(name) as fh:
                    for raw in fh:
                        line=raw.decode("utf-8","replace")
                        if line.startswith('{"k":"tick"'):
                            m=rhand.search(line); h=m.group(1) if m else "?"; hand_c[h]+=1
                            m=rdo.search(line)
                            if m:
                                try: it=json.loads(m.group(1))
                                except Exception: it={"do":"?"}
                                k=(it.get("type"),it.get("do")); do_c[k]+=1
                                if h=="net": do_net[k]+=1
                                if "net" in m.group(1): do_net[("menciona_net",m.group(1)[:80])]+=1
                        elif line.startswith('{"k":"P7_huella"'):
                            r=json.loads(line); o=r.get("objeto") or "first_aid"; hu[(tag.split("_")[3],o)]+=1
                            if o=="net": hu_motivo[(r.get("motivo_cierre"),r.get("completa"))]+=1; HNET.append((tag,sl,r.get("efecto"),r.get("duracion"),r.get("motivo_cierre")))
                        elif line.startswith('{"k":"P7_33_prueba"'):
                            r=json.loads(line); abre[r.get("objeto")]+=1
                        elif line.startswith('{"k":"P7_48_contado"'):
                            r=json.loads(line); r["_tag"]=tag; r["_sl"]=sl; REC.append(r)
                        elif line.startswith('{"k":"P7_48_visto"'):
                            r=json.loads(line)
                            if r.get("estado")=="apuntado": r["_tag"]=tag; r["_sl"]=sl; VIS.append(r)
json.dump({"do":[[list(k),v] for k,v in do_c.most_common()],"hand":hand_c.most_common(),"do_con_red_en_mano":[[list(k),v] for k,v in do_net.most_common(40)],
 "huellas":[[list(k),v] for k,v in hu.items()],"net_motivo":[[list(k),v] for k,v in hu_motivo.items()],"abre":abre,"HNET":HNET,"REC":REC,"VIS":VIS},open(os.path.join(os.path.dirname(__file__),"escaneo.json"),"w"),ensure_ascii=False,indent=0,default=str)
print("ok", len(REC), len(VIS))
