import sys; sys.path.insert(0,'.')
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
import model as M
from model import State, ModelConfig

OUT="figures"
RED="#E0382A"; DARK="#1F1F1F"; GREY="#9C9194"; GREYL="#C7C0C2"
plt.rcParams.update({'font.size':12.5,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130})

SF,SR,SS = 0.30,0.15,0.10
def cfg_sigma(k): return ModelConfig(sens_F=SF*k, sens_R=SR*k, sens_S=SS*k)
cfg_B = ModelConfig(sens_F=0.0,sens_R=0.0,sens_S=0.0)
base = dict(pF=0.8209,nF=0.0,pR=1.6013,nR=0.0,pS=0.6802,nS=0.0)
DELTA=0.5
def dd(kw,cfg,stim):
    s=State(**kw); s2=State(**{**kw,stim:kw[stim]+DELTA})
    return M.opponent_distance(s2,cfg)-M.opponent_distance(s,cfg)
def cross(kw,stim,k): return dd(kw,cfg_sigma(k),stim)-dd(kw,cfg_B,stim)

defs=np.linspace(0,2.0,41)
tests=[("Social spectator  $\\rightarrow$  physical stimulus","nS","pF","social deficit  $n_S$"),
       ("Resource spectator  $\\rightarrow$  physical stimulus","nR","pF","resource deficit  $n_R$"),
       ("Physical spectator  $\\rightarrow$  resource stimulus","nF","pR","physical deficit  $n_F$")]
sigmas=[(0.5,GREYL,'--',1.7,'$\\sigma$ = 0.5×',2),
        (1.0,RED,'-',2.8,'$\\sigma$ = 1× (nominal)',6),
        (1.5,GREY,'-.',1.8,'$\\sigma$ = 1.5×',2),
        (2.0,DARK,':',1.8,'$\\sigma$ = 2×',2)]

fig,axs=plt.subplots(1,3,figsize=(13.2,4.0))
yc=[cross({**base,'nF':nx},'pR',1.0) for nx in defs]
xc=np.interp(0,yc,defs)
for j,(ax,(title,spec,stim,xlabel)) in enumerate(zip(axs,tests)):
    for k,color,ls,lw,lbl,z in sigmas:
        ys=[cross({**base,spec:nx},stim,k) for nx in defs]
        ax.plot(defs,ys,ls,color=color,lw=lw,label=lbl,zorder=z)
    ax.axhline(0,color=DARK,lw=0.9)
    ax.set_title(title,fontsize=11.5,pad=8)
    ax.set_xlabel(xlabel); ax.set_xlim(0,2.0)
    ax.margins(y=0.12)
    if j==2:
        ax.axvline(xc,color=GREY,lw=1.0,ls=(0,(1,2)))
        yl=ax.get_ylim()
        ax.text(0.15,yl[0]+0.10*(yl[1]-yl[0]),'facilitates',color=GREY,fontsize=10,style='italic')
        ax.text(1.55,yl[1]-0.12*(yl[1]-yl[0]),'penalizes',color=DARK,fontsize=10,style='italic')
axs[0].set_ylabel("coupling contribution\n($\\Delta d_{\\sigma}\\,-\\,\\Delta d_{0}$)")
axs[0].legend(frameon=False,fontsize=9.5,loc='upper left')
fig.suptitle("Cross-modulation of sensitivity: the coupling's contribution to the response, by the deficit of the spectator domain",
             fontsize=12,y=1.04)
fig.tight_layout()
fig.savefig(f"{OUT}/fig11_cross_modulation.png",bbox_inches="tight",dpi=300); plt.close()
print(f"saved -> fig11_cross_modulation.png  Test 3 crossover (in dd): nF = {xc:.2f}")
