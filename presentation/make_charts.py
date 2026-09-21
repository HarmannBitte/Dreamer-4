"""Charts for the Dreamer 4 deck (numbers from the paper's tables; see dreamer4_research_report.md)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
A="assets/"
NAVY="#14213D"; BLUE="#2F5BEA"; TEAL="#1FB5A6"; PURPLE="#8B5CF6"; RED="#EF5350"; GREY="#8A94A6"; ORANGE="#F59E0B"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":12,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#444","axes.titleweight":"bold"})

# 1. Hard milestones, Table 7 (success %, 1000 episodes)
items=["Stone\npickaxe","Iron\nore","Furnace","Iron\ningot","Iron\npickaxe","Diamond"]
data={"BC":[53.8,26.5,16.2,4.3,0.6,0.0],"VLA (Gemma 3)":[76.7,46.3,42.4,22.5,11.2,0.0],"WM + BC":[89.4,62.9,51.1,27.8,16.9,0.0],"Dreamer 4":[90.1,66.7,58.1,39.5,29.0,0.7]}
cols=[PURPLE,TEAL,GREY,BLUE]
fig,ax=plt.subplots(figsize=(10,4.6),dpi=200); x=np.arange(len(items)); w=0.2
for i,(k,v) in enumerate(data.items()):
    b=ax.bar(x+(i-1.5)*w,v,w,label=k,color=cols[i])
    for r,val in zip(b,v): ax.text(r.get_x()+r.get_width()/2,val+1,f"{val:g}",ha="center",va="bottom",fontsize=8.5,color=cols[i],fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(items); ax.set_ylabel("Success rate (%)"); ax.set_ylim(0,100)
ax.set_title("Hard milestones of the offline diamond challenge (Table 7, 1,000 episodes × 60 min)",fontsize=12)
ax.legend(frameon=False,ncol=4,loc="upper right"); ax.grid(axis="y",alpha=.25)
fig.tight_layout(); fig.savefig(A+"chart_table7_hard.png"); plt.close(fig)

# 2. Design cascade, Table 2 (FVD lower is better; FPS where reported)
rows=[("Diffusion-forcing transformer, K = 64 steps",306,0.8),("K = 4 sampling steps",875,9.1),("+ shortcut objective  → shortcut forcing",329,None),("+ x-prediction",326,None),("+ loss in x-space (scaled)",151,None),("+ ramp loss weight",102,None),("+ alternating batch lengths",80,None),("+ long-context (time) attention only every 4th layer",70,18.9),("+ grouped-query attention",71,23.2),("+ time-factorized long context",91,30.1),("+ register tokens",91,None),("+ N_z 128 → 256 latent tokens  (final)",57,21.4)]
fig,ax=plt.subplots(figsize=(11,5.6),dpi=200)
y=np.arange(len(rows))[::-1]; vals=[r[1] for r in rows]
colors=[GREY]*len(rows); colors[0]=RED; colors[1]=RED; colors[-1]=BLUE
ax.barh(y,vals,color=colors,height=0.62)
for yi,(name,fvd,fps) in zip(y,rows):
    ax.text(fvd+8,yi,f"FVD {fvd}"+(f"   ·   {fps} FPS" if fps else ""),va="center",fontsize=10,color="#222")
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=10.5); ax.set_xlabel("FVD on 384-frame generations (lower is better)"); ax.set_xlim(0,1000)
ax.set_title("Cascade of design choices — Table 2 (each row adds to the previous; 48 h runs)",fontsize=11,loc="left")
ax.grid(axis="x",alpha=.25); fig.tight_layout(); fig.savefig(A+"chart_ablation_cascade.png"); plt.close(fig)

# 3. Time to milestone, Table 8 (minutes, successful episodes)
ms=["Crafting table","Stone pickaxe","Iron pickaxe","Diamond"]; d4=[4.4,6.7,13.3,20.7]; vla=[7.2,14.5,31.1,None]
fig,ax=plt.subplots(figsize=(6.4,4.2),dpi=200); x=np.arange(4); w=0.36
ax.bar(x-w/2,d4,w,color=BLUE,label="Dreamer 4"); ax.bar(x+w/2,[v or 0 for v in vla],w,color=TEAL,label="VLA (Gemma 3)")
for i,v in enumerate(d4): ax.text(i-w/2,v+0.5,f"{v}",ha="center",fontsize=10,color=BLUE,fontweight="bold")
for i,v in enumerate(vla):
    if v: ax.text(i+w/2,v+0.5,f"{v}",ha="center",fontsize=10,color=TEAL,fontweight="bold")
    else: ax.text(i+w/2,1,"never",ha="center",fontsize=9,color=TEAL,rotation=90,va="bottom")
ax.set_xticks(x); ax.set_xticklabels(ms); ax.set_ylabel("Minutes until item obtained"); ax.set_ylim(0,36)
ax.set_title("Time to milestone (Table 8)",fontsize=12); ax.legend(frameon=False); ax.grid(axis="y",alpha=.25)
fig.tight_layout(); fig.savefig(A+"chart_time_to_milestone.png"); plt.close(fig)

# 4. Speed/fidelity landscape (qualitative positions from paper + TalkRL)
plt.rcParams.update({"font.size":13})
fig,ax=plt.subplots(figsize=(6.6,4.4),dpi=200)
pts=[("Dreamer 3 RSSM\n(64×64, fast)",1000,1,NAVY),("Diffusion-forcing\ntransformer, K=64",0.8,5,RED),("Dreamer 4\n(shortcut forcing, K=4)",21,5,BLUE)]
for n,fps,q,c in pts: ax.scatter(fps,q,s=260,color=c,zorder=3); ax.annotate(n,(fps,q),textcoords="offset points",xytext=(0,14),ha="center",fontsize=11,color=c)
ax.set_xscale("log"); ax.set_xlim(0.3,4000); ax.set_ylim(0,7); ax.set_yticks([1,5]); ax.set_yticklabels(["low","high"]); ax.set_ylabel("Fidelity / interaction accuracy")
ax.set_xlabel("Generation speed (FPS, log scale)"); ax.set_title("Speed vs. fidelity: ~30× faster than diffusion forcing,\n~40× slower than Dreamer 3's RSSM (Hafner, TalkRL)",fontsize=10.5)
ax.axvspan(15,40,color=BLUE,alpha=.06); ax.text(22,0.4,"real-time\n(≥ 20 FPS)",ha="center",fontsize=9,color=BLUE)
ax.grid(alpha=.25,which="both"); fig.tight_layout(); fig.savefig(A+"chart_speed_fidelity.png"); plt.close(fig)
print("charts done")
