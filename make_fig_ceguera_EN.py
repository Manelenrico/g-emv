import sys; sys.path.insert(0,'.')
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import model as M
from model import State, DEFAULT_CONFIG
cfg=DEFAULT_CONFIG; OUT="figures"
RED="#E0382A"; DARK="#1F1F1F"; GREY="#9C9194"
plt.rcParams.update({'font.size':11,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130})
def mk(half):
    b=M.TEN_BASAL_MIN/2; return State(pF=half,nF=half,pR=b,nR=b,pS=b,nS=b)
def opp(s,d): return State(pF=s.pF+d,nF=s.nF,pR=s.pR,nR=s.nR,pS=s.pS,nS=s.nS)
def dgr(s,d): return State(pF=s.pF,nF=s.nF+d,pR=s.pR,nR=s.nR,pS=s.pS,nS=s.nS)
delta=1.5
sc,st=mk(1.0),mk(3.8)
vals={'opo_c':M.opponent_distance(opp(sc,delta),cfg)-M.opponent_distance(sc,cfg),
      'opo_t':M.opponent_distance(opp(st,delta),cfg)-M.opponent_distance(st,cfg),
      'pel_c':M.opponent_distance(dgr(sc,delta),cfg)-M.opponent_distance(sc,cfg),
      'pel_t':M.opponent_distance(dgr(st,delta),cfg)-M.opponent_distance(st,cfg)}
print("values:",{k:round(v,3) for k,v in vals.items()})
fig,ax=plt.subplots(figsize=(7,4.3))
x=np.arange(2); w=0.36
b1=ax.bar(x-w/2,[vals['opo_c'],vals['pel_c']],w,label='Calm ($\\mathrm{ten}_F = 2.0$)',color=RED)
b2=ax.bar(x+w/2,[vals['opo_t'],vals['pel_t']],w,label='Saturated ($\\mathrm{ten}_F = 7.6$)',color=DARK)
for b in list(b1)+list(b2):
    ax.text(b.get_x()+b.get_width()/2,b.get_height()+0.02,f'{b.get_height():.2f}',ha='center',fontsize=9.5)
ax.set_xticks(x); ax.set_xticklabels(['Opportunity (gain)','Danger (loss)'])
ax.set_ylabel('Homeostatic perturbation Δd'); ax.legend(frameon=False,fontsize=9.5)
ax.set_title('Saturation blindness: to opportunities and to dangers',fontsize=11.5)
ax.annotate('near-total blindness',(0,vals['opo_c']),xytext=(0,vals['opo_c']+0.18),ha='center',fontsize=9,color=GREY,style='italic')
ax.annotate('partial blindness',(1,vals['pel_c']),xytext=(1,vals['pel_c']+0.18),ha='center',fontsize=9,color=GREY,style='italic')
fig.tight_layout(); fig.savefig(f"{OUT}/fig08_saturation_blindness.png",bbox_inches='tight',dpi=300); plt.close()
print("saved -> fig08_saturation_blindness.png")
