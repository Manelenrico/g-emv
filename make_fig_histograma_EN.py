#!/usr/bin/env python3
# Genera el panel del histograma de la Fig 10 del paper.
# La figura publicada (fig10_concentration.png) es un montaje: un render 3D de la esfera
# arriba mas este histograma abajo, ensamblado por el autor. Este script guarda solo
# el panel del histograma como fig10_histogram_panel.png.
import sys; sys.path.insert(0,'.')
import os; os.chdir('.')
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
RED="#E0382A"; DARK="#1F1F1F"; GREY="#9C9194"
plt.rcParams.update({'font.size':11,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130})
OUT="figures"

d=json.load(open('attractor_signatures.json'))
sig=d['signatures']
def arr(types):
    v=np.array([[s['sig_F'],s['sig_R'],s['sig_S']] for s in sig if s['type'] in types])
    return v/np.linalg.norm(v,axis=1,keepdims=True)
mixed=arr({'mix2','mix3'})
ang_mixed=np.degrees(np.arccos(np.clip(np.max(np.abs(mixed),axis=1),-1,1)))
frac30=np.mean(ang_mixed<30)
rng=np.random.default_rng(0); u=rng.normal(size=(3_000_000,3)); u/=np.linalg.norm(u,axis=1,keepdims=True)
ang_base=np.degrees(np.arccos(np.clip(np.max(np.abs(u),axis=1),-1,1)))
base30=np.mean(ang_base<30)
print(f"mixtures <30deg: {frac30:.4f}  | uniform baseline <30deg: {base30:.4f}  | enrichment {frac30/base30:.3f}x")

fig,ax=plt.subplots(figsize=(7.8,3.5))
bins=np.linspace(0,90,31)
wm=np.ones_like(ang_mixed)/len(ang_mixed)
ax.hist(ang_mixed,bins=bins,weights=wm,color=RED,alpha=0.85,label='Responses to mixtures (observed)')
hb,_=np.histogram(ang_base,bins=bins); hb=hb/hb.sum()
ax.plot((bins[:-1]+bins[1:])/2,hb,'--',color=DARK,lw=1.8,label='Uniform distribution (chance)')
ax.set_ylim(0, 0.155)
ax.axvline(30,color=GREY,lw=1.2,ls=':')
ax.text(30,0.142,' 30°',color=GREY,fontsize=9)
ax.text(1.5,0.150,f'Within 30° of a pole:\n{frac30*100:.1f}% observed  vs  {base30*100:.1f}% chance\n(enrichment {frac30/base30:.2f}×)',
        ha='left',va='top',fontsize=9.5,color=DARK,
        bbox=dict(boxstyle='round,pad=0.4',fc='white',ec='#9C9194',lw=0.9))
ax.set_xlabel('Angular distance to nearest pole (degrees)'); ax.set_ylabel('Fraction of responses')
ax.set_title('Concentration of responses at the poles (mixtures of two or three domains)',fontsize=11.5)
ax.legend(frameon=False,fontsize=9.5,loc='upper right')
fig.tight_layout(); fig.savefig(f"{OUT}/fig10_histogram_panel.png",bbox_inches="tight",dpi=300); plt.close()
print("saved -> fig10_histogram_panel.png")
