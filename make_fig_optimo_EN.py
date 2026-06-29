import sys; sys.path.insert(0,'.')
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
import model as M
from model import State, DEFAULT_CONFIG
cfg=DEFAULT_CONFIG; OUT="figures"
RED="#A23B3B"; GREY="#9A9A9A"
plt.rcParams.update({'font.size':11,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130})
def mk(half):
    b=M.TEN_BASAL_MIN/2; return State(pF=half,nF=half,pR=b,nR=b,pS=b,nS=b)
def opp(s,dl): return State(pF=s.pF+dl,nF=s.nF,pR=s.pR,nR=s.nR,pS=s.pS,nS=s.nS)
levels=[2.0,4.0,6.0,7.0,7.5,7.9]; delta=1.5
dd=[M.opponent_distance(opp(mk(t/2),delta),cfg)-M.opponent_distance(mk(t/2),cfg) for t in levels]
fig,ax=plt.subplots(figsize=(7.4,4.6))
ax.set_ylim(-0.2,1.02)
ax.axvspan(6.5,8.0,color=RED,alpha=0.06)
ax.axvline(8.0,ls=':',color=RED,lw=1.2)
ax.text(7.92,0.99,'$V_{\\max} = 8.0$',color=RED,fontsize=9.5,va='top',ha='right')
ax.plot(levels,dd,'-o',color=RED,lw=2,ms=6)
ip=int(np.argmax(dd))
ax.plot(levels[ip],dd[ip],'o',ms=12,mfc='none',mec=RED,mew=2)
ax.annotate(f'Peak: Δd = {dd[ip]:.2f}  ($\\mathrm{{ten}}_F = {levels[ip]:.1f}$)',
            xy=(levels[ip],dd[ip]),xytext=(3.0,0.50),color=RED,fontsize=10,
            arrowprops=dict(arrowstyle='->',color=RED,lw=1.1))
ax.axhline(0,color=GREY,lw=0.8,ls='--')
ax.set_xlabel('Basal physical tension  $\\mathrm{ten}_F$'); ax.set_ylabel('Homeostatic perturbation Δd')
ax.set_title('Activation optimum: opportunity stimulus (δ = 1.5)',fontsize=11.5,pad=12)
fig.tight_layout(); fig.savefig(f"{OUT}/fig5_optimo_activacion_EN.png",bbox_inches='tight'); plt.close()
print(f"saved -> fig5_optimo_activacion_EN.png  peak ten_F={levels[ip]:.1f}, dd={dd[ip]:.3f}")
