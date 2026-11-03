"""Two Inputs, One Exit — revised chapter animation.
COLOR MAP: BLUE rod/cone relay and potassium; GREEN melanopsin/cation pathway;
GOLD ipRGC cell bodies; YELLOW light and voltage marker; PURPLE brain targets;
RED removal; GREY scaffolds. No molecular structures.
All traces are computed from first-order passive/conductance models, never data.
V∞=(gₖ Eₖ+gcat Ecat)/(gₖ+gcat); dV/dt=(V∞−V)/tau.
"""
import numpy as np
import re
from bp_style import *
PURPLE = '#B58CD9'

def label(s,x=0,y=0,size=40,color=TEXT):
    # Build real subscripts from baseline-aligned text; the house font lacks
    # Unicode subscript K/c glyphs, so these must not be passed to Pango.
    tokens=re.split(r'([Eg](?:ₖ|꜀ₐₜ))',s)
    if len(tokens)==1:
        return (VGroup(*[T(line,size,color) for line in s.split('\n')]).arrange(DOWN,buff=.14) if '\n' in s else T(s,size,color)).move_to([x,y,0])
    parts=VGroup(); cursor=0
    for token in tokens:
        if not token: continue
        if re.fullmatch(r'[Eg](?:ₖ|꜀ₐₜ)',token):
            main=T(token[0],size,color)
            sub=T('K' if token[1:]=='ₖ' else 'cat',size*.64,color)
            sub.next_to(main,RIGHT,buff=.015).shift(DOWN*.17)
            part=VGroup(main,sub)
        else: part=T(token,size,color)
        part.shift(RIGHT*(cursor-part.get_left()[0]))
        parts.add(part); cursor+=part.width+.025
    return parts.move_to([x,y,0])
def heading(s): return label(s,0,3.22,44)
def note(s): return label(s,0,-3.28,30,GREY)
def arr(a,b,c=GREEN,w=6):
    return Arrow(a,b,buff=.08,color=c,stroke_width=w,tip_length=.22,
                 max_tip_length_to_length_ratio=.35)
def box(s,x,y,c=GREEN,w=3.4,h=1.05,size=38):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.17,
        stroke_color=c,stroke_width=3,fill_color=BG,fill_opacity=1).move_to([x,y,0]),label(s,x,y,size,c))
def body(x,y,w=2.25,h=1.25):
    return VGroup(Ellipse(width=w,height=h,color=GOLD,stroke_width=4,fill_color=GOLD,fill_opacity=.12).move_to([x,y,0]),label('ipRGC',x,y,38,GOLD))
def cross(x,y,s=.22):
    return VGroup(Line([x-s,y-s,0],[x+s,y+s,0],color=RED,stroke_width=4),Line([x-s,y+s,0],[x+s,y-s,0],color=RED,stroke_width=4))
def scissors(x,y):
    return VGroup(Circle(.14,color=RED).move_to([x-.32,y-.23,0]),Circle(.14,color=RED).move_to([x-.32,y+.23,0]),
        Line([x-.2,y-.17,0],[x+.38,y+.32,0],color=RED,stroke_width=5),Line([x-.2,y+.17,0],[x+.38,y-.32,0],color=RED,stroke_width=5))

# The same voltage-to-position map is used in every balance-point scene.
def voltage(gk,gcat): return -90*gk/(gk+gcat)
def voltage_x(v): return -5.3+10.6*(v+90)/90
def vx(gk,gcat): return voltage_x(voltage(gk,gcat))
def response(t,kind,common=False,residual=1):
    base,target,tau=(-45,-75,.24) if kind=='rod' else (-75,-45,.85)
    if common: base,target=-60,(-80 if kind=='rod' else -40)
    return base if t<1 else base+residual*(target-base)*(1-np.exp(-(t-1)/tau))

def trace(x,y,kind,w=4.5,h=3.8,common=False,residual=1):
    color=BLUE if kind=='rod' else GREEN
    ax=Axes(x_range=[0,6,2],y_range=[-90,-30,30],x_length=w,y_length=h,tips=False,
        axis_config={'include_ticks':False,'stroke_color':GREY,'stroke_width':2}).move_to([x,y,0])
    base=-60 if common else (-45 if kind=='rod' else -75)
    curve=ax.plot(lambda t:response(t,kind,common,residual),x_range=[0,6,.025],color=color,stroke_width=5)
    rest=DashedLine(ax.c2p(0,base),ax.c2p(6,base),color=GREY,stroke_width=2,dash_length=.12)
    ticks=VGroup(*[label(str(v),ax.c2p(0,v)[0]-.43,ax.c2p(0,v)[1],30,GREY) for v in [-90,-60,-30]])
    light=VGroup(Line(ax.c2p(1,-30)+UP*.22,ax.c2p(6,-30)+UP*.22,color=YELLOW,stroke_width=7),
        label('light on',x+.35,y+h/2+.55,32,YELLOW))
    time=label('time →',x,y-h/2-.42,34,GREY)
    return VGroup(ax,curve,rest,ticks,light,time)
def paired(compact=False):
    y,h=(1.25,1.8) if compact else (-.35,3.7)
    a=trace(-3.0,y,'rod',4.5,h,True); b=trace(3.25,y,'m1',4.5,h,True)
    title=label('Membrane voltage (mV)',0,3.22,38)
    names=VGroup(label('rod',-3,2.62 if not compact else 2.83,40,BLUE),label('M1 cell',3.25,2.62 if not compact else 2.83,40,GREEN))
    if compact:
        # Keep the bar labels below the names in the short summary panels.
        for t in (a,b): t[4][1].set_opacity(0)
        title=label('Membrane voltage (mV) • light on',0,3.5,32)
    return VGroup(a,b,names,title)

def wiring():
    layers=VGroup(*[RoundedRectangle(width=12,height=1.35,corner_radius=.16,stroke_color=GREY,stroke_opacity=.25,
        fill_color=GREY,fill_opacity=.035).move_to([0,y,0]) for y in [2.1,.05,-2.15]])
    rc=VGroup(box('rods',-2.8,2.1,BLUE,3.3),box('cones',2.8,2.1,BLUE,3.3))
    bp=VGroup(box('bipolar',-2.8,.05,BLUE,3.3),box('bipolar',2.8,.05,BLUE,3.3))
    upper=VGroup(*[arr([x,1.55,0],[x,.65,0],BLUE) for x in [-2.8,2.8]])
    dend=VGroup(Line([-4.1,-1.2,0],[4.1,-1.2,0],color=GOLD,stroke_width=5),Line([0,-1.2,0],[0,-1.55,0],color=GOLD,stroke_width=5))
    lower=VGroup(*[arr([x,-.52,0],[x,-1.2,0],BLUE) for x in [-2.8,2.8]])
    ip=body(0,-2.2,2.7,1.25)
    dl=label('dendrites',3.9,-2.15,36,GOLD)
    leader=Line([3.9,-1.85,0],[3.9,-1.27,0],color=GOLD,stroke_width=2)
    return VGroup(layers,rc,bp,upper,dend,lower,ip,dl,leader)

def pool(y=-.25):
    ip=body(-.1,y,2.65,1.5)
    r=arr([-5, y+1.45,0],[-1.5,y+.4,0],BLUE,8)
    m=arr([-5,y-1.45,0],[-1.5,y-.4,0],GREEN,8)
    out=arr([1.3,y,0],[3.05,y,0],GOLD,9)
    targets=VGroup(box('clock\n(SCN)',4.7,y+1.55,PURPLE,2.5,1.4,36),box('pupil\n(OPN)',4.7,y-1.55,PURPLE,2.5,1.4,36))
    branches=VGroup(arr([3.05,y,0],[3.6,y+1.1,0],GOLD),arr([2.95,y-1.55,0],[3.4,y-1.55,0],GOLD))
    others=VGroup(body(1.8,y-1.55,2.1,1.1),arr([-.15,y-1.1,0],[.68,y-1.3,0],BLUE),arr([-.15,y-2.0,0],[.68,y-1.8,0],GREEN),label('across cells',1.8,y-2.45,30,GREY))
    texts=VGroup(label('rod + cone relay',-3.7,y+2.05,36,BLUE),label('melanopsin',-3.7,y-2.05,38,GREEN),label('one axon',2.25,y+.65,34,GOLD))
    return VGroup(ip,r,m,out,targets,branches,texts,others)

def gate(x,y,opened,c=GREEN,name='cation channel',width=3.7):
    gap=.62 if opened else .18
    mask=Rectangle(width=width+.1,height=.22,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,y,0])
    bars=VGroup(mask,Line([x-width/2,y,0],[x-gap,y,0],color=c,stroke_width=13),Line([x+gap,y,0],[x+width/2,y,0],color=c,stroke_width=13))
    sides=VGroup(Line([x-gap,y-.43,0],[x-gap,y+.43,0],color=c,stroke_width=5),Line([x+gap,y-.43,0],[x+gap,y+.43,0],color=c,stroke_width=5))
    shut=Line([x-gap,y,0],[x+gap,y,0],color=c,stroke_width=9).set_opacity(0 if opened else 1)
    return VGroup(bars,sides,shut,label(name,x,y-.91,36,c))
def charges(x,y,c=GREEN):
    return VGroup(*[label('+',x+dx,y+dy,38,c) for dx,dy in [(-.28,.65),(.28,.9),(-.24,1.15),(.24,1.4)]])

def pulse(mob):
    # Scale only: preserve every label's colour and every box's dark fill.
    return Indicate(mob,color=None,scale_factor=1.045)

def flow(scene,x,y,c=GREEN,duration=1.2):
    ions=VGroup(*[label('+',x+dx,y+dy,34,c) for dx,dy in [(-.42,.35),(-.14,.35),(.14,.35),(.42,.35)]])
    scene.add(ions)
    scene.play(ions.animate.shift(DOWN*1.55),run_time=duration,rate_func=linear)
    # Hold the entered charges in the cell so sparse draft samples show entry.
    return ions

def cascade():
    mem=VGroup(Line([-6.1,1.05,0],[6.1,1.05,0],color=GOLD,stroke_width=12),label('M1 membrane',0,3.22,42,GOLD))
    mel=box('melanopsin',-4.75,1.05,GREEN,2.7,1.2,30)
    g=box('Gq family\n(inferred)',-1.5,1.05,GREEN,2.4,1.4,32)
    plc=box('PLCB4',1.5,1.05,GREEN,2.15,1.2,34)
    a=arr([-3.35,1.05,0],[-2.75,1.05,0],GREEN)
    b=arr([-.25,1.05,0],[.37,1.05,0],GREEN)
    expanded=label('phospholipase\nC beta 4',1.5,-1.05,36,GREEN)
    link=Line([1.5,.4,0],[1.5,-.35,0],color=GREEN,stroke_width=3)
    light=VGroup(arr([-4.75,2.8,0],[-4.75,1.75,0],YELLOW),label('light',-5.65,2.5,32,YELLOW))
    channel=gate(4.65,1.05,False,GREEN,'TRPC6/7: closed',2.7)
    channel[3].move_to([4.65,2.2,0]).scale(.85)
    output=arr([2.62,1.05,0],[3.23,1.05,0],GREEN)
    return VGroup(mem,mel,g,plc,a,b,expanded,link,light,channel,output)

def scale(v=-85,y=0,title='The balance-point rule'):
    line=Line([-5.3,y,0],[5.3,y,0],color=GREY,stroke_width=9)
    ticks=VGroup(*[Line([voltage_x(n),y-.16,0],[voltage_x(n),y+.16,0],color=GREY,stroke_width=3) for n in [-90,-75,-60,-45,-30,-15,0]])
    ends=VGroup(label('Eₖ ≈ −90 mV',-4.5,y-.75,38,BLUE),label('E꜀ₐₜ ≈ 0 mV',4.4,y-.75,38,GREEN))
    mark=VGroup(Dot([voltage_x(v),y,0],radius=.17,color=YELLOW),Line([voltage_x(v),y+.18,0],[voltage_x(v),y+.8,0],color=YELLOW,stroke_width=4))
    return VGroup(line,ticks,ends,mark,heading(title))
def marker_label(v,y=1.3): return label(f'membrane voltage: {v:g} mV',0,y,38,YELLOW)
def formula(y=-2.15):
    # The label helper draws baseline-shifted subscripts without LaTeX.
    return label('V = (gₖ Eₖ + g꜀ₐₜ E꜀ₐₜ) / (gₖ + g꜀ₐₜ)',0,y,39)

def m4(final=False,hcn=False):
    a=gate(-4.0,1.65,not final,BLUE,'K leak: closed' if final else 'K leak: open',3.45)
    b=gate(0,1.65,final,GREEN,'TRPC: open' if final else 'TRPC: closed',3.45)
    a[3].move_to([-4,-.1,0]); b[3].move_to([0,-.1,0])
    mem=Line([-6,1.65,0],[6,1.65,0],color=GOLD,stroke_width=5).set_opacity(.4)
    g=VGroup(mem,a,b,heading('M4 • a reported pathway').move_to([0,3.45,0]))
    if hcn:
        h=gate(4,1.65,True,GREY,'HCN ?\ndisputed',3.45)
        h[3].move_to([4,-.1,0])
        dashed=VGroup(*[DashedVMobject(line,num_dashes=9) for group in [VGroup(*h[0][1:]),h[1]] for line in group]).set_opacity(.5)
        g.add(VGroup(h[0][0],dashed,h[3].set_opacity(.65)))
    s=scale(-60 if final else -85,-1.25); s.remove(s[4])
    val=label('illustrative: −60 mV' if final else 'near rest: −85 mV',0,-2.72,36,YELLOW)
    # gcat=.0588 puts rest at -85; halving K and opening TRPC to .25 gives -60.
    return g,s,val,a,b

class S00Title(TitleCard):
    LESSON='Melanopsin Cells: Light for the Clock and the Pupil'
    TITLE='Two Inputs, One Exit'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.5,30,TEAL),label(self.TITLE,0,1.0,58))
        subtitle=VGroup(label('Melanopsin Cells:',0,-.5,38,GREY),label('Light for the Clock and the Pupil',0,-1.4,38,GREY))
        self.play(FadeIn(subtitle),Create(Line([-3,-2.3,0],[3,-2.3,0],color=GOLD)),run_time=.6); self.finish()

class S01Q(SpokenScene):
    def construct(self):
        p=paired(); self.add(p[2],p[3])
        for t in p[:2]: self.add(t[0],t[2],t[3],t[4],t[5])
        self.at('Light hyperpolarizes'); self.play(Create(p[0][1]),run_time=.6)
        self.at('Yet light',lead=.5); self.play(Create(p[1][1]),run_time=.6)
        self.at('How can',lead=.5); self.play(FadeIn(label('Same light, opposite signs?',0,-3.2,40,YELLOW)),run_time=.4)
        self.finish()

class S02Wiring(SpokenScene):
    def construct(self):
        w=wiring(); self.add(w[0],w[1],w[2],w[4],w[6],w[7],w[8],heading('Retina: the relay route'))
        self.at('Start with'); self.play(Indicate(w[1]),run_time=.4)
        self.at('Rods and cones',lead=.5); self.play(Create(w[3]),run_time=.4)
        self.at('Bipolar cells signal',lead=.5); self.play(Create(w[5]),run_time=.4)
        self.at('dendrites',lead=.5); self.play(Indicate(w[4]),Indicate(w[7]),run_time=.5)
        self.finish()

class S03Own(SpokenScene):
    def construct(self):
        w=wiring(); self.add(w,heading('Two routes for light'))
        dots=VGroup(*[Dot([x,-2.75,0],radius=.12,color=GREEN) for x in [-.55,0,.55]])
        name=label('melanopsin',-3.9,-3.12,36,GREEN)
        leader=Line([-2.5,-3.05,0],[-.6,-2.8,0],color=GREEN,stroke_width=2)
        self.add(dots,name,leader)
        self.at('Melanopsin sits'); self.play(Indicate(dots,color=GREEN),run_time=.5)
        self.at('So light',lead=.5)
        lights=VGroup(arr([-5.55,3.02,0],[-4.55,2.57,0],YELLOW),arr([.05,3.02,0],[1.05,2.57,0],YELLOW),arr([1.55,-3.2,0],[.55,-2.75,0],YELLOW))
        self.play(Create(lights),run_time=.4); self.finish()

class S04Exit(SpokenScene):
    def construct(self):
        cells=VGroup(*[body(-4.7,y,2.4,1.35) for y in [2.05,0,-2.05]])
        targets=VGroup(box('clock (SCN)',4.1,1.45,PURPLE,3.65,1.5,38),box('pupil (OPN)',4.1,-1.45,PURPLE,3.65,1.5,38))
        ax=VGroup(arr([-3.45,2.05,0],[2.2,1.45,0],GOLD,8),arr([-3.45,0,0],[2.2,1.45,0],GOLD,8),arr([-3.45,-2.05,0],[2.2,-1.45,0],GOLD,8))
        self.add(cells,heading('One exit per cell'),note('Across the population'))
        self.at('each cell',lead=.4); self.play(Create(ax),run_time=.4)
        self.at('those exits reach',lead=.5); self.play(FadeIn(targets),run_time=.4)
        self.at('clock and'); self.play(pulse(targets[0]),run_time=.35)
        self.at('pupil'); self.play(pulse(targets[1]),run_time=.35); self.finish()

class S05Idea(SpokenScene):
    def construct(self):
        call=box('An ipRGC pools two light signals into one output.',0,2.18,GOLD,12,1.0,35)
        cell=body(0,-.8,2.9,1.65)
        r=arr([-5.4,.5,0],[-1.55,-.35,0],BLUE,8)
        m=arr([-5.4,-2.1,0],[-1.55,-1.25,0],GREEN,8)
        out=arr([1.55,-.8,0],[4.0,-.8,0],GOLD,9)
        names=VGroup(label('rod + cone relay',-4,.98,34,BLUE),label('melanopsin',-4,-2.65,36,GREEN),label('one output',4.6,-1.5,36,GOLD))
        self.add(heading('The one idea').shift(UP*.2),call,cell)
        self.at('one idea'); self.play(pulse(call),run_time=.4)
        self.at('two light signals',lead=.4)
        self.play(Create(r),FadeIn(names[0]),run_time=.45)
        self.play(Create(m),FadeIn(names[1]),run_time=.45)
        self.at('one output',lead=.2); self.play(Create(out),FadeIn(names[2]),run_time=.45); self.finish()

class S06Inputs(SpokenScene):
    def construct(self):
        self.add(heading('Two signals, different sensitivities'))
        def signal(y,slow):
            ax=Axes(x_range=[0,8,2],y_range=[0,1.3,.5],x_length=6.4,y_length=1.55,tips=False,axis_config={'include_ticks':False,'stroke_color':GREY}).move_to([-2.4,y,0])
            tau=1.2 if slow else .15
            f=lambda t:(1-np.exp(-t/tau))*(.65+.55*np.exp(-t/2.5))
            color=GREEN if slow else BLUE
            strong=ax.plot(f,x_range=[0,8,.04],color=color,stroke_width=5)
            # Hill sensitivity to dim intensity: same light, different K (illustrative).
            dim=.12**2/(.12**2+(.8 if slow else .1)**2)
            weak=ax.plot(lambda t:dim*f(t),x_range=[0,8,.04],color=color,stroke_width=3)
            return VGroup(ax,strong,DashedVMobject(weak,num_dashes=35),label('time →',-2.4,y-1.02,32,GREY),
                label('melanopsin • slower' if slow else 'relay • faster',-2.3,y+1.05,38,color),
                arr([1.1,y,0],[3.55,y*.3,0],color))
        a=signal(1.25,False); b=signal(-1.75,True)
        self.add(a,body(4.85,-.25,2.4,1.5),label('signal',-6.05,-.2,32,GREY).rotate(PI/2),label('solid: brighter light    dashed: same dim light',0,-3.35,30,YELLOW))
        self.at('One input'); self.play(Create(a[1]),run_time=.4)
        self.at('usually faster'); self.play(Indicate(a[2]),run_time=.4)
        self.at('The other',lead=.5); self.play(FadeIn(b),run_time=.4)
        self.at('usually slower'); self.play(Indicate(b[2]),run_time=.4)
        self.at('Both can'); self.play(Indicate(a[1]),Indicate(b[1]),run_time=.5); self.finish()

class S07Route(SpokenScene):
    def construct(self):
        p=pool(); self.add(p,heading('Main route, in mice'),note('Different cells reach different targets'))
        self.at('In mice'); self.play(p[3].animate.set_stroke(width=14),p[5].animate.set_stroke(width=10),run_time=.5)
        self.at('either signal',lead=.4); self.play(Indicate(p[1],color=BLUE),Indicate(p[2],color=GREEN),run_time=.4)
        self.at('reaches the clock',lead=.4); self.play(ShowPassingFlash(p[3].copy().set_color(YELLOW)),Indicate(p[4]),run_time=.6); self.finish()

class S08Predictions(SpokenScene):
    def construct(self):
        p=pool(); self.add(p,heading('Remove one part at a time'))
        result=label('rod + cone relay alone',0,-3.25,40,BLUE)
        cut=scissors(-3.1,-.95)
        self.at('removing the pigment',lead=.4); self.play(FadeIn(cut),p[2].animate.set_opacity(.12),p[7][2].animate.set_opacity(.12),FadeIn(result),run_time=.35)
        self.at('or the rods',lead=.4); self.play(cut.animate.move_to([-3.1,.65,0]),p[2].animate.set_opacity(1),p[1].animate.set_opacity(.12),p[7][2].animate.set_opacity(1),p[7][1].animate.set_opacity(.12),Transform(result,label('melanopsin alone',0,-3.25,40,GREEN)),run_time=.35)
        self.at('other input'); self.play(p[2].animate.set_opacity(1),run_time=.4)
        self.at('Removing the cell',lead=.4); self.play(cut.animate.move_to([.1,-1.25,0]),p[0].animate.set_opacity(.15),p[1].animate.set_opacity(.12),p[2].animate.set_opacity(.12),p[3].animate.set_opacity(.12),p[5].animate.set_opacity(.12),p[7].animate.set_opacity(.12),Transform(result,label('neither input reaches the targets',0,-3.25,38,RED)),run_time=.4); self.finish()

class S09Rod(SpokenScene):
    def construct(self):
        g=gate(-3.7,.4,True,BLUE,'cation channel',4.0); tr=trace(3.4,-.4,'rod',4.1,3.5,True)
        sensor=box('rhodopsin /\ncGMP cascade',-3.7,2.12,BLUE,4.1,1.2,34)
        self.add(heading('Rod • membrane voltage (mV)'),g,sensor,tr[0],tr[2],tr[3],tr[4],tr[5],note('Illustrative passive response'))
        link=arr([-3.7,1.48,0],[-3.7,.88,0],BLUE); self.add(link)
        plus=charges(-3.7,.4,BLUE); self.add(plus)
        self.at('Now the polarity'); self.play(plus.animate.shift(DOWN*1.05),run_time=.7)
        self.at('light closes',lead=.45); self.play(Create(arr([-6,2.7,0],[-5.8,2.2,0],YELLOW)),g[2].animate.set_opacity(1),FadeOut(plus),run_time=.4)
        self.at('Less positive'); self.play(Indicate(g[2]),run_time=.4)
        self.at('rod hyperpolarizes',lead=.5); self.play(Create(tr[1]),run_time=.65); self.finish()

class S10M1(SpokenScene):
    def construct(self):
        p=paired(compact=True)
        # Move compact voltage plots below the channel comparison.
        for t in p[:2]: t.shift(DOWN*2.6)
        rod=gate(-3.3,1.25,False,BLUE,'rod: closed',4.7); m=gate(3.2,1.25,False,GREEN,'M1: channel closed',4.7)
        self.add(heading('Membrane voltage (mV)').move_to([0,3.47,0]),rod,m,p[0],p[1][0],p[1][2],p[1][3],p[1][4],p[1][5])
        sensor=box('melanopsin cascade',3.2,2.75,GREEN,4.8,.8,34); self.add(sensor)
        rod[3].move_to([-3.3,1.95,0]); m[3].move_to([3.2,1.95,0])
        light=arr([.25,2.75,0],[.73,2.75,0],YELLOW)
        p[0][4][1].set_opacity(0); p[1][4][1].set_opacity(0)
        self.add(label('light on',0,-.05,30,YELLOW))
        self.at('In an'); self.play(Create(light),run_time=.3)
        self.at('light opens',lead=.2)
        opened=gate(3.2,1.25,True,GREEN,'M1: channel open',4.7)
        opened[3].move_to([3.2,1.95,0])
        self.play(Transform(m,opened),Create(p[1][1]),run_time=.4)
        flow(self,3.2,1.25,duration=.9); self.finish()

class S11Opsin(SpokenScene):
    def construct(self):
        root=box('opsins',0,2.35,GREY,3,1.1,44)
        trunk=VGroup(Line([0,1.8,0],[0,.85,0],color=GREY,stroke_width=4),Line([-3,.85,0],[3,.85,0],color=GREY,stroke_width=4),Line([-3,.85,0],[-3,-.1,0],color=GREEN,stroke_width=4),Line([3,.85,0],[3,-.1,0],color=BLUE,stroke_width=4))
        left=box('insect-type',-3,-.4,GREEN,5,1.05,40); right=box('vertebrate rod\nand cone type',3,-.4,BLUE,5,1.05,36)
        leaves=VGroup(box('melanopsin',-4.65,-2.45,GREEN,3,1,34),box('insect visual\nopsins',-1.35,-2.45,GREEN,3,1,34),box('rod + cone\nopsins',3,-2.45,BLUE,4.2,1,38))
        links=VGroup(Line([-3,-.95,0],[-4.65,-1.9,0],color=GREEN,stroke_width=3),Line([-3,-.95,0],[-1.35,-1.9,0],color=GREEN,stroke_width=3),Line([3,-.95,0],[3,-1.9,0],color=BLUE,stroke_width=3))
        tree=VGroup(root,trunk,left,right,links,leaves).shift(DOWN*.35)
        self.add(heading('An opsin family tree').shift(UP*.15),tree)
        self.at('Melanopsin is'); self.play(pulse(leaves[0]),run_time=.4)
        self.at('but it is closer',lead=.4); self.play(pulse(VGroup(left,leaves[0],leaves[1])),run_time=.5)
        self.at('rod and cone',lead=.4); self.play(pulse(leaves[2]),run_time=.4); self.finish()

class S12Gq(SpokenScene):
    def construct(self):
        c=cascade(); self.add(c[0],c[1],c[8],note('Light → opsin → G protein → enzyme'))
        self.at('It activates'); self.play(Create(c[4]),run_time=.35)
        self.at('a G protein',lead=.4); self.play(FadeIn(c[2]),run_time=.35)
        self.at('inferred to be',lead=.4); self.play(Indicate(c[2]),run_time=.45)
        self.at('That activates',lead=.2); self.play(Create(c[5]),FadeIn(c[3]),run_time=.45)
        self.at('phospholipase C',lead=.2); self.play(FadeIn(c[6]),Create(c[7]),run_time=.35); self.finish()

class S13Trpc(SpokenScene):
    def construct(self):
        c=cascade(); self.add(*c[:9],c[9],c[10])
        self.at('Then'); self.play(Indicate(c[9][3]),run_time=.4)
        self.at('channels open',lead=.2)
        opened=gate(4.65,1.05,True,GREEN,'TRPC6/7: open',2.7)
        opened[3].move_to([4.65,2.2,0]).scale(.85)
        self.play(Transform(c[9],opened),run_time=.4)
        flow(self,4.65,1.05,duration=1.1); self.finish()

class S14Ko(SpokenScene):
    def construct(self):
        # Compact membrane chain above a large, labelled voltage panel.
        chain=VGroup(box('melanopsin',-4.5,2.15,GREEN,2.8,.9,32),box('Gq\n(inferred)',-.9,2.15,GREEN,2.8,1.15,32),box('PLCB4',3.1,2.15,GREEN,2.7,.9,38),arr([-3,2.15,0],[-2.4,2.15,0]),arr([.6,2.15,0],[1.65,2.15,0]))
        tr=trace(.45,-.9,'m1',10.0,2.8,common=True)
        ref=label('intact reference',1.5,-1.65,36,GREY)
        self.add(heading('M1 membrane • voltage (mV)'),chain,tr,ref,note('Xue and colleagues, 2011 • illustrative response'))
        self.at('Without'); self.wait(.25)
        self.at('phospholipase C',lead=0); self.play(chain[2].animate.set_opacity(.5),FadeIn(cross(5.0,2.15)),run_time=.35)
        self.at('essentially disappeared',lead=.4)
        residual=tr[0].plot(lambda t:response(t,'m1',common=True,residual=.008),x_range=[0,6,.025],color=GREEN,stroke_width=5)
        self.play(Transform(tr[1],residual),Transform(ref,label('essentially none • ≤1% residual',1.5,-1.65,34,RED)),run_time=.4); self.finish()

class S15Fly(SpokenScene):
    def construct(self):
        self.add(heading('Same pieces in a fly eye'))
        def row(y,fly):
            return VGroup(label('fly eye' if fly else 'M1 cell',-4.65,y+1,40,GREEN),box('Gq',-2.65,y,GREEN,2,1.3,40),box('PLC' if fly else 'PLCB4',.5,y,GREEN,2.5,1.3,38),box('TRP' if fly else 'TRPC6/7',4.1,y,GREEN,3.0,1.3,36),arr([-1.55,y,0],[-.85,y,0]),arr([1.85,y,0],[2.5,y,0]))
        m=row(1.15,False); f=row(-1.8,True)
        f[0].shift(UP*.45)
        eye=VGroup(Ellipse(width=1.4,height=1.8,color=GREY,fill_color=GREY,fill_opacity=.15),*[Circle(.12,color=YELLOW).move_to([x,y,0]) for x,y in [(-.3,.35),(.15,.45),(.35,.05),(-.25,-.2),(.15,-.45)]]).move_to([-4.8,-1.8,0])
        self.add(m,f[0],eye)
        self.at('A fly'); self.play(pulse(eye),FadeIn(f[1]),Create(f[4]),FadeIn(f[2]),Create(f[5]),FadeIn(f[3]),run_time=.5)
        self.at('with',lead=.4); self.play(pulse(f[1]),run_time=.35)
        self.at('phospholipase',lead=.4); self.play(pulse(f[2]),run_time=.35)
        self.at('and TRP',lead=.4); self.play(pulse(f[3]),run_time=.35); self.finish()

class S16Predict(SpokenScene):
    def construct(self):
        s=scale(title='Which way when TRPC opens?'); self.add(s,marker_label(-85),label('TRPC: cations • reversal near 0 mV',0,2.25,38,GREEN),label('← more negative        more positive →',0,-1.8,38,GREY),label('Pause and predict: which direction?',0,-2.8,38,YELLOW))
        self.at('Predict'); self.play(Indicate(s[3]),run_time=.4)
        self.at('reverses near',lead=.4); self.play(Indicate(s[2][1]),run_time=.45)
        self.at('Opening them',lead=.4); self.play(Indicate(s[4]),run_time=.45); self.finish()

class S17Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(scale(title='Which way when TRPC opens?'),marker_label(-85),label('TRPC: cations • reversal near 0 mV',0,2.25,38,GREEN),label('← more negative        more positive →',0,-1.8,38,GREY),label('Pause and predict: which direction?',0,-2.8,38,YELLOW))
        self.wait(5)

class S18Rule(SpokenScene):
    def construct(self):
        s=scale(); val=marker_label(-85)
        self.add(s,val,formula(),label('Conductance sets the pull',0,-3.15,38,GREEN))
        cond=label('steady state • no injected current',0,2.28,38,GREY)
        tracker=ValueTracker(90/85-1)
        def cat_rope():
            return arr([vx(1,tracker.get_value()),.48,0],[5.2,.48,0],GREEN,3+60*tracker.get_value()).set_stroke(width=3+60*tracker.get_value(),family=False)
        def k_rope():
            return arr([vx(1,tracker.get_value()),-.3,0],[-5.3,-.3,0],BLUE,12).set_stroke(width=12,family=False)
        rope=always_redraw(cat_rope); k=always_redraw(k_rope)
        self.add(rope,k,label('gₖ = 1',-4.5,-1.4,32,BLUE),label('g꜀ₐₜ rises',4.3,-1.45,32,GREEN))
        self.at('Recall the'); self.play(pulse(s[0]),run_time=.45)
        self.at('When the voltage',lead=.4); self.play(FadeIn(cond),run_time=.35)
        self.at('weighted average',lead=.4); self.play(pulse(self.mobjects[2]),run_time=.4)
        self.at('The weights',lead=.2)
        s[3].add_updater(lambda m:m.shift(RIGHT*(vx(1,tracker.get_value())-m[0].get_x())))
        self.play(tracker.animate.set_value(.2),FadeOut(val),run_time=1.3)
        s[3].clear_updaters()
        self.add(marker_label(-75)); self.finish()

class S19Reveal(SpokenScene):
    def construct(self):
        s=scale(-75); val=label('g꜀ₐₜ = 0.2   →   V = −75 mV',0,1.2,42,YELLOW)
        self.add(s,val,label('gₖ = 1 • Eₖ = −90 mV • E꜀ₐₜ = 0 mV',0,2.25,36),formula(-2),note('Illustrative passive model, not ipRGC measurements'))
        self.at('Here that'); self.play(Indicate(s[2][1]),run_time=.4)
        self.at('voltage moves up',lead=.4)
        self.play(s[3].animate.shift(RIGHT*(voltage_x(-45)-voltage_x(-75))),Transform(val,label('g꜀ₐₜ = 1   →   V = −45 mV',0,1.2,42,YELLOW)),run_time=1.0)
        self.at('cell depolarizes',lead=.4); self.play(Transform(s[4],heading('The cell depolarizes')),run_time=.35); self.finish()

class S20M4(SpokenScene):
    def construct(self):
        g,s,val,a,b=m4()
        values=VGroup(label('gₖ: 1 → 0.5',size=28,color=GREY),label('g꜀ₐₜ: 0.059 → 0.25',size=28,color=GREY)).arrange(RIGHT,buff=.7).move_to([0,-3.55,0])
        foot=VGroup(label('Illustrative model',0,-3.12,28,GREY),values)
        self.add(g,s,val,label('K leak closure reported\n(Sonoda and colleagues, 2018)',0,2.65,30,BLUE),foot)
        self.at('another subtype'); self.play(pulse(g[3]),run_time=.4)
        self.at('close potassium',lead=.15)
        closed=gate(-4,1.65,False,BLUE,'K leak: closed',3.45); closed[3].move_to([-4,-.1,0])
        self.play(Transform(a,closed),run_time=.55)
        self.at('alongside',lead=.15)
        opened=gate(0,1.65,True,GREEN,'TRPC: open',3.45); opened[3].move_to([0,-.1,0])
        self.play(Transform(b,opened),run_time=.55)
        flow(self,0,1.65,duration=1.1)
        self.at('Closing them',lead=.2)
        newval=label('illustrative: −60 mV',0,-2.72,36,YELLOW)
        self.play(s[3].animate.shift(RIGHT*(voltage_x(-60)-voltage_x(-85))),FadeOut(val),run_time=.8)
        self.play(FadeIn(newval),run_time=.3)
        self.at('same rule',lead=.2); self.play(pulse(s[3]),run_time=.4); self.finish()

class S21Dispute(SpokenScene):
    def construct(self):
        g,s,val,a,b=m4(True,True); self.add(g,s,val,label('HCN: disputed between labs',0,2.65,38,GREY),note('Scale retained • illustrative passive model'))
        self.at('Whether'); self.play(pulse(g[4]),run_time=.4)
        self.at('still disputed',lead=.4); self.play(Indicate(self.mobjects[3]),run_time=.4); self.finish()

class S22Take(SpokenScene):
    def construct(self):
        p=paired(True); self.add(p)
        # Two named inputs converge on one cell; its single axon reaches targets.
        cell=body(.15,-1.75,2.4,1.45)
        r=arr([-4.8,-1,0],[-1.15,-1.35,0],BLUE,8); m=arr([-4.8,-2.6,0],[-1.15,-2.12,0],GREEN,8)
        out=arr([1.4,-1.75,0],[3.7,-1.75,0],GOLD,9)
        labels=VGroup(label('relay',-4,-.65,36,BLUE),label('melanopsin',-4,-3,36,GREEN),label('one axon',2.55,-1.05,36,GOLD),label('clock /\npupil',5,-1.75,38,PURPLE))
        self.add(cell,r,m,out,labels)
        self.at('Light hyperpolarizes'); self.play(Indicate(p[0][1],color=BLUE),run_time=.4)
        self.at('depolarizes an',lead=.4); self.play(Indicate(p[1][1],color=GREEN),run_time=.4)
        self.at('both of',lead=.4); self.play(ShowPassingFlash(r.copy()),ShowPassingFlash(m.copy()),run_time=.45)
        self.at('one exit',lead=.4); self.play(ShowPassingFlash(out.copy().set_color(YELLOW)),run_time=.5); self.finish()

class S23End(EndCard):
    LINE="Light hyperpolarizes a rod, depolarizes an M1 cell,\nand both of the cell’s inputs leave by one exit."
    def construct(self):
        self.clear()
        self.add(label('Two Inputs, One Exit',0,2.4,48,GOLD),T(self.LINE,40,should_center=True,line_spacing=1.4).move_to([0,.15,0]),label('biochemistrypedia.com',0,-2.5,34,TEAL))
        self.finish()
