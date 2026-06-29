import sys; sys.path.insert(0,'.')
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
import model as M
from model import State, DEFAULT_CONFIG, ModelConfig
cfg=DEFAULT_CONFIG; OUT="figures"
RED="#E0382A"; DARK="#1F1F1F"; GREY="#9C9194"; BLUE="#1F1F1F"
plt.rcParams.update({'font.size':11,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130})

ETA=0.05
def gstep(s,c):
    dF=s.pos_F-c.f_pos_target;dR=s.pos_R-c.r_pos_target;dS=s.pos_S-c.s_pos_target
    tF=s.ten_F-c.f_ten_target;tR=s.ten_R-c.r_ten_target;tS=s.ten_S-c.s_ten_target
    C_F=c.sens_F*(dR**2+dS**2);C_R=c.sens_R*(dF**2+dS**2);C_S=c.sens_S*(dF**2+dR**2)
    W_F=c.sens_R*s.ten_R+c.sens_S*s.ten_S;W_R=c.sens_F*s.ten_F+c.sens_S*s.ten_S;W_S=c.sens_F*s.ten_F+c.sens_R*s.ten_R
    GpF=2*(c.w_f_pos+W_F)*dF+2*c.w_f_ten*tF+C_F;GnF=-2*(c.w_f_pos+W_F)*dF+2*c.w_f_ten*tF+C_F
    GpR=2*(c.w_r_pos+W_R)*dR+2*c.w_r_ten*tR+C_R;GnR=-2*(c.w_r_pos+W_R)*dR+2*c.w_r_ten*tR+C_R
    GpS=2*(c.w_s_pos+W_S)*dS+2*c.w_s_ten*tS+C_S;GnS=-2*(c.w_s_pos+W_S)*dS+2*c.w_s_ten*tS+C_S
    return State(pF=max(0,s.pF-ETA*GpF),nF=max(0,s.nF-ETA*GnF),pR=max(0,s.pR-ETA*GpR),
                 nR=max(0,s.nR-ETA*GnR),pS=max(0,s.pS-ETA*GpS),nS=max(0,s.nS-ETA*GnS))
def d2(s,c): d=M.opponent_distance(s,c); return d*d
def gain(s,a,dl):
    k={'F':'pF','R':'pR','S':'pS'}[a];kw=dict(pF=s.pF,nF=s.nF,pR=s.pR,nR=s.nR,pS=s.pS,nS=s.nS);kw[k]+=dl;return State(**kw)
def loss(s,a,dl):
    k={'F':'nF','R':'nR','S':'nS'}[a];kw=dict(pF=s.pF,nF=s.nF,pR=s.pR,nR=s.nR,pS=s.pS,nS=s.nS);kw[k]+=dl;return State(**kw)
lambdas=np.linspace(0,1.3,27); base=dict(f_ten_target=cfg.f_ten_target,r_ten_target=cfg.r_ten_target,s_ten_target=cfg.s_ten_target,
    sens_F=cfg.sens_F,sens_R=cfg.sens_R,sens_S=cfg.sens_S,w_f_pos=cfg.w_f_pos,w_r_pos=cfg.w_r_pos,w_s_pos=cfg.w_s_pos,
    w_f_ten=cfg.w_f_ten,w_r_ten=cfg.w_r_ten,w_s_ten=cfg.w_s_ten)
tgt={'F':1.0,'R':2.0,'S':0.8}; res={'F':([],[]),'R':([],[]),'S':([],[])}
for lam in lambdas:
    c=ModelConfig(f_pos_target=tgt['F']*lam,r_pos_target=tgt['R']*lam,s_pos_target=tgt['S']*lam,**base)
    s=State(pF=.4,nF=.4,pR=.4,nR=.4,pS=.4,nS=.4)
    for _ in range(6000): s=gstep(s,c)
    pos={'F':s.pos_F,'R':s.pos_R,'S':s.pos_S}
    for a in ('F','R','S'):
        res[a][0].append(tgt[a]*lam-pos[a]); res[a][1].append(d2(loss(s,a,1.0),c)-d2(gain(s,a,1.0),c))
fig,ax=plt.subplots(figsize=(7,4.3)); cols={'F':RED,'R':BLUE,'S':GREY}; names={'F':'physical','R':'resources','S':'social'}
for a in ('R','F','S'):
    g=np.array(res[a][0]); b=np.array(res[a][1]); o=np.argsort(g); ax.plot(g[o],b[o],'-',color=cols[a],lw=2,label=f'{names[a]} axis')
ax.axhline(0,color='#cccccc',lw=0.8); ax.axvline(0,color='#cccccc',lw=0.8)
ax.plot(0,0,'o',color='k',ms=7,zorder=5)
ax.annotate('No displacement (gap = 0):\nthe bias is null',xy=(0,0),xytext=(0.265,0.28),fontsize=9.5,color=DARK,
            ha='left',bbox=dict(boxstyle='round,pad=0.4',fc='#f3f3f3',ec='#888',lw=0.8),
            arrowprops=dict(arrowstyle='->',color='#555',lw=1.0))
ax.set_xlabel('Displacement of the equilibrium (gap)'); ax.set_ylabel('Bias  d²(loss) − d²(gain)')
ax.set_title('The negativity bias follows from the displacement',fontsize=11.5)
ax.legend(frameon=False,fontsize=9.5,loc='upper left')
fig.tight_layout(); fig.savefig(f"{OUT}/fig_sesgo_negatividad_EN.png",bbox_inches='tight'); plt.close()
print("saved -> fig_sesgo_negatividad_EN.png")
