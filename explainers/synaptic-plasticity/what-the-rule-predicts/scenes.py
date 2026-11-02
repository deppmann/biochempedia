"""What the Rule Explains — Synaptic Plasticity.
COLOR MAP: yellow glutamate, blue AMPA, purple NMDA, orange Mg2+,
teal Ca2+, pink voltage, green LTP; pathway A lavender, B blue, C grey.
All time courses: illustrative step model 100 + 65 H(t); not measured data.
Voltage = -70/(1+gAMPA/grest); entry = Mg-unblocked fraction × GHK flux.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as _SpokenScene
PURPLE='#B58CD9'; ORANGE='#F29E4C'; PINK='#E58FC0'
PATH=['#A7A5ED','#76B6E8',GREY]

class SpokenScene(_SpokenScene):
    # Exact word onset, with no anticipatory lead. The shared logger records
    # pre-wait times, so avoid using it as a measure of actual cue arrival.
    def at(self, phrase, lead=0, nth=0):
        remaining=self.t_of(phrase,nth)-self.elapsed()
        if remaining>0: self.wait(remaining)


def lab(s,x=0,y=3.15,color=TEXT,size=28):
    return T(s,size,color).move_to([x,y,0])

def heading(s,color=TEXT): return lab(s,color=color,size=34)
def unblocked(v): return 1/(1+np.exp(-.062*v)/3.57)
def voltage(g): return -70/(1+g)
def entry(v):
    u=2*96485.33212*(v/1000)/(8.314462618*308.15)
    inward=2-.0001 if abs(u)<1e-7 else u*(2-.0001*np.exp(u))/np.expm1(u)
    return unblocked(v)*inward

def pore(x,y,k=1):
    return VGroup(*[RoundedRectangle(width=.28*k,height=1.1*k,corner_radius=.06,
        color=PURPLE,fill_color=PURPLE,fill_opacity=.4,stroke_width=3)
        .move_to([x+s*.34*k,y,0]) for s in [-1,1]])

def circuit(names=('input A','input B','input C'),third=True):
    ys=[2,.1,-1.8]
    soma=Circle(.48,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([-1.8,-2.55,0])
    dend=Line([-1.8,-2.1,0],[-1.8,2.5,0],color=GREY,stroke_width=8)
    c=VGroup(soma,dend,lab('CA1 cell',-1.8,-3.3,TEXT,26))
    w=VGroup(); h=VGroup(); l=VGroup()
    for i,y in enumerate(ys[:3 if third else 2]):
        w.add(Line([-6,y,0],[-2.5,y,0],color=PATH[i],stroke_width=7 if i==1 else 3))
        h.add(VGroup(Circle(.23,color=PATH[i],fill_color=BG,fill_opacity=1).move_to([-2.25,y,0]),
            Line([-2,y,0],[-1.8,y,0],color=GREY,stroke_width=4)))
        l.add(lab(names[i],-4.5,y+.45,PATH[i],28))
    return c,w,h,l

def train(scene,w,indices,repeats=3,pulse_time=.20):
    for _ in range(repeats):
        dots=[Dot(w[i].get_start(),radius=.10,color=w[i].get_color()) for i in indices]
        scene.add(*dots)
        scene.play(*[MoveAlongPath(d,w[i]) for d,i in zip(dots,indices)],run_time=pulse_time,rate_func=linear)
        scene.remove(*dots)

def course(x,y,w=3.4,h=3.5):
    return Axes(x_range=[-1,3,1],y_range=[50,200,50],x_length=w,y_length=h,
        axis_config={'include_ticks':False,'include_tip':False,'color':GREY}).move_to([x,y,0])

def trace(ax,up=False,color=TEXT):
    ts=[-1,0,0,3]; vals=100+65*np.array([0,0,int(up),int(up)])
    return VMobject(color=color,stroke_width=4).set_points_as_corners([ax.c2p(t,v) for t,v in zip(ts,vals)])

def plot(x,y,w,h,name,up=None,labels=True):
    ax=course(x,y,w,h)
    base=DashedLine(ax.c2p(-1,100),ax.c2p(3,100),color=GREY,stroke_width=2)
    labels_g=VGroup(lab(name,x,y+h/2+.4,TEXT,28))
    if labels:
        labels_g.add(lab('before → 1 hour',x,y-h/2-.4,TEXT,26))
    result=lab('?',x,y+.35,GOLD,52) if up is None else trace(ax,up,GREEN if up else TEXT)
    return VGroup(ax,base,labels_g,result)

def prediction(states=(None,None,None),title='Each pathway’s slope an hour later?'):
    xs=[-3.9,.35,4.6]
    ps=VGroup(*[plot(x,0,3.35,4.7,n,s) for x,n,s in zip(xs,['Strong','Weak','Third: silent'],states)])
    ylabel=lab('EPSP slope (% of baseline)',-6.65,0,TEXT,26).rotate(PI/2)
    ticks=VGroup(*[lab(str(v),-5.9,ps[0][0].c2p(-1,v)[1],TEXT,26) for v in [100,200]])
    return VGroup(heading(title,GOLD).shift(UP*.25),ps,ylabel,ticks,
        lab('Illustrative step model • dashed line = baseline',.3,-3.4,GREY,26))

def sideplots(states=(None,None,None),names=('A','B','C')):
    ps=VGroup(*[plot(3.65,y,4.4,1.05,n,s,False) for y,n,s in zip([2.05,.05,-1.95],names,states)])
    return VGroup(ps,lab('EPSP slope (% baseline)',3.65,3.5,TEXT,26),
        lab('before → 1 hour',3.65,-3.05,TEXT,26))

def assocplots(states=(None,True)):
    ps=VGroup(*[plot(3.65,y,4.4,1.65,n,s,False) for y,n,s in zip([1.55,-1.25],['Weak','Strong'],states)])
    return VGroup(ps,lab('EPSP slope (% baseline)',3.65,3.25,TEXT,26),
        lab('before → 1 hour',3.65,-2.8,TEXT,26))

def spine(x=0,y=0):
    # Large two-pore cartoon: one may unblock while the other remains blocked.
    membrane=VGroup(Line([x-3,y,0],[x-2.1,y,0],color=GREY,stroke_width=10),
        Line([x-.3,y,0],[x+.3,y,0],color=GREY,stroke_width=10),
        Line([x+2.1,y,0],[x+3,y,0],color=GREY,stroke_width=10))
    membrane.add(VMobject(color=GREY,stroke_width=3).set_points_as_corners([[x-3,y,0],[x-3,y-1.5,0],[x-2.6,y-2,0],[x-.5,y-2,0],[x-.5,y-2.35,0],[x+.5,y-2.35,0],[x+.5,y-2,0],[x+2.6,y-2,0],[x+3,y-1.5,0],[x+3,y,0]]))
    pores=VGroup(pore(x-1.2,y,1.9),pore(x+1.2,y,1.9))
    mg=VGroup(*[Dot([x+i,y,0],radius=.19,color=ORANGE) for i in [-1.2,1.2]])
    names=VGroup(lab('NMDA receptors',x,y-1.65,PURPLE,28),
        lab('Mg²⁺',x,y+.8,ORANGE,28),
        Line([x-.3,y+.55,0],[x-1.05,y+.15,0],color=ORANGE),
        Line([x+.3,y+.55,0],[x+1.05,y+.15,0],color=ORANGE))
    return VGroup(membrane,pores,mg,names)

def glus(x=0,y=0):
    return VGroup(*[Dot([x+i-.92,y+.62,0],radius=.12,color=YELLOW) for i in [-1.2,1.2]])

def bound_glus(x=0,y=0):
    # Glutamate sits on the extracellular end of each outer receptor pillar.
    return VGroup(*[Dot([x+s*1.846,y+1.045,0],radius=.12,color=YELLOW) for s in [-1,1]])

def voltage_panel(g):
    # Marker, pore and graph form one connected explanatory layout.
    ax=Axes(x_range=[-80,20,20],y_range=[0,5,1],x_length=6.4,y_length=4.4,
        axis_config={'include_ticks':False,'include_tip':False,'color':GREY}).move_to([2.6,-.1,0])
    ax.y_axis.set_opacity(0)
    left_axis=Line(ax.c2p(-80,0),ax.c2p(-80,5),color=GREY)
    curve=ax.plot(entry,x_range=[-80,20,.35],use_smoothing=False,color=TEAL,stroke_width=5)
    xt=VGroup(*[lab(str(v).replace('-','−'),ax.c2p(v,0)[0],-2.75,TEXT,26) for v in [-80,-70,-40,0,20]])
    # Stagger the adjacent tick below the axis, clear of the -80 label.
    xt[1].shift(DOWN*.35)
    scale=Line([-5.5,-2.25,0],[-5.5,2.15,0],color=GREY,stroke_width=4)
    def vp(v): return np.array([-5.5,-2.25+(v+70)/70*4.4,0])
    ticks=VGroup(*[lab(str(v).replace('-','−'),-6.1,vp(v)[1],TEXT,26) for v in [-70,-40,0]])
    v=voltage(g); marker=Dot(vp(v),radius=.14,color=PINK)
    point=Dot(ax.c2p(v,entry(v)),radius=.12,color=PINK)
    # Route around the pore, keeping its block and label unobscured.
    connection=VGroup(*[DashedLine(a,b,color=PINK,stroke_width=2) for a,b in zip(
        [marker.get_center(),[-4.65,vp(v)[1],0],[-4.65,1.1,0],[.1,1.1,0]],
        [[-4.65,vp(v)[1],0],[-4.65,1.1,0],[.1,1.1,0],point.get_center()])])
    # Voltage label has a standing place, clear of pore and tick text.
    val=lab(f'≈ {v:.0f} mV'.replace('-','−'),-3.4,1.65,PINK,30)
    rope=Line(vp(v),[-4.6,2.15,0],color=BLUE,stroke_width=3 if g<1 else 10)
    p=VGroup(pore(-3.3,-.55,1.5),Dot([-3.3,-.55,0],radius=.19,color=ORANGE),lab('Mg²⁺',-3.3,-1.9,ORANGE,28))
    fixed=VGroup(ax,left_axis,curve,xt,scale,ticks,lab('local voltage',-5.2,2.75,TEXT,26),
        lab('Ca²⁺ entry (relative)',2.65,2.75,TEAL,28),lab('voltage (mV)',2.6,-3.5,TEXT,26),
        lab('AMPA pull: toward 0 mV',-3.6,3.35,BLUE,26),
        lab('balance point',-4.8,-3.25,PINK,26),
        lab('AMPA conductance:',1.7,3.35,BLUE,26))
    moving=VGroup(connection,rope,marker,point,val,
        lab('0 × resting' if g==0 else ('0.1 × resting' if g<1 else '2 × resting'),4.6,3.35,BLUE,26),
        DashedLine([-4.9,-2.95,0],vp(v),color=PINK,stroke_width=2))
    return fixed,moving,p

class S00Title(TitleCard):
    LESSON='Synaptic Plasticity'; TITLE='What the Rule Explains'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON.upper(),28,GREY),
            T(self.TITLE,48,font=TITLE_FONT),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.45)
        self.add(g); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(); g=VGroup(c,w,h,l).shift(RIGHT*2)
        self.add(g,lab('?',2.8,-2.5,GOLD,70))
        self.at('several inputs'); train(self,w,[0,1,2]); self.finish()

class S02Setup(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(); self.add(c,w,h,l)
        self.at('receiving separate input'); ps=sideplots((False,False,False)); self.play(FadeIn(ps),run_time=.4)
        self.at('stimulate each one');
        stims=VGroup(*[chip('stim',TEXT,26).move_to([-5.6,y,0]) for y in [2,.1,-1.8]])
        for i,stim in enumerate(stims):
            w[i].put_start_and_end_on([stim.get_right()[0],w[i].get_y(),0],w[i].get_end())
            l[i].shift(UP*.18)
        self.add(stims)
        for i in range(3): train(self,w,[i],2)
        self.at('Three properties'); self.remove(stims)
        props=VGroup(lab('Three properties',3.65,2.65,GOLD,30),
            *[lab(name,3.65,y,TEXT,30) for name,y in zip(
                ['Input specificity','Cooperativity','Associativity'],[1.3,-.05,-1.4])])
        self.play(FadeOut(ps),FadeIn(props),run_time=.4)
        self.at('Can the gate'); self.play(Indicate(props,color=GOLD,scale_factor=1.02),run_time=.3)
        self.finish()

class S03SpecQ(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(('trained','bystander','silent')); ps=sideplots((False,False,None),('trained','bystander','silent'))
        self.add(c,w,h,l,ps)
        self.at('during the train')
        self.play(c[0].animate.set_color(PINK),c[1].animate.set_color(PINK),run_time=.2)
        train(self,w,[0],4,pulse_time=.32)
        self.at('Does it change'); self.play(FadeOut(c[2]),FadeIn(lab('Does the silent input change?',-3.3,-3.3,GOLD,28)),run_time=.3); self.finish()

class S04SpecA(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(('trained','bystander','silent'))
        mini=VGroup(c[0],c[1],w,h).scale(.42).move_to([-5,1,0]); self.add(mini,lab('trained',-5.2,2.3,PATH[0],26),lab('silent',-5.2,.55,TEXT,26),lab('CA1',-4.05,-.65,TEXT,26))
        detail=spine(-.4,0)
        detail[3][1].move_to([-.4,1.3,0])
        detail[3][2].put_start_and_end_on([-.75,1.08,0],[-1.45,.15,0])
        detail[3][3].put_start_and_end_on([-.05,1.08,0],[.65,.15,0])
        self.add(detail,heading('Silent input',TEXT))
        self.at('it released no'); self.play(FadeIn(lab('no glutamate',-.4,2.1,YELLOW,30)),run_time=.3)
        self.at('let in no calcium');
        ca=VGroup(lab('Ca²⁺',-2.5,2.65,TEAL,34),Arrow([-2.5,2.45,0],[-2.5,1.2,0],color=TEAL,buff=0,stroke_width=8,max_tip_length_to_length_ratio=.2),Line([-2.9,1.2,0],[-2.1,1.2,0],color=TEXT,stroke_width=6))
        self.play(FadeIn(ca),FadeIn(lab('no entry',-1.6,-2.85,TEAL,36)),run_time=.35)
        self.at('however depolarized'); self.play(c[0].animate.set_color(PINK),c[1].animate.set_color(PINK),detail[0].animate.set_color(PINK),FadeIn(lab('depolarized',-4.9,-1.2,PINK,26)),run_time=.6)
        self.at('does not potentiate'); p=plot(4.4,0,3.2,4.2,'Silent input',False)
        self.play(FadeIn(p),run_time=.45); self.finish()

class S05SpecName(SpokenScene):
    def construct(self):
        left=plot(-3.1,-.15,4.9,4.8,'Silent input',False); self.add(left)
        self.at('input specificity'); self.play(FadeIn(heading('Input specificity')),run_time=.35)
        self.at('first recording'); right=plot(3.1,-.15,4.9,4.8,'Untrained control · chapter 1',False)
        self.play(FadeIn(right,shift=LEFT*.4),Create(DashedLine([-.5,.7,0],[.5,.7,0],color=TEXT)),run_time=.5)
        self.at('stayed flat'); self.play(Indicate(right[3],scale_factor=1.04),run_time=.4); self.finish()

class S06Coop(SpokenScene):
    def construct(self):
        ps=VGroup(plot(-3.2,-.8,4.8,3.5,'Few fibres',None),plot(3.2,-.8,4.8,3.5,'Many fibres',None))
        bundles=[]
        for x,n in [(-3.2,3),(3.2,12)]:
            wires=VGroup(*[Line([x-1.8,2.65+i*.035,0],[x+1.3,2.25+(i-(n-1)/2)*.10,0],color=PATH[0],stroke_width=2) for i in range(n)])
            bundles.append(wires)
            self.add(wires,Circle(.27,color=GREY).move_to([x+1.65,2.25,0]))
        self.add(ps,lab('EPSP slope (% baseline)',0,-3.5,TEXT,26))
        self.at('a train to'); train(self,bundles[0],[0,1,2],3)
        self.at('can fail'); self.play(FadeOut(ps[0][3]),Create(trace(ps[0][0])),run_time=.35)
        self.at('The same train'); train(self,bundles[1],list(range(12)),3)
        self.at('succeeds'); self.play(FadeOut(ps[1][3]),Create(trace(ps[1][0],True,GREEN)),run_time=.4); self.finish()

class S07CoopWhy(SpokenScene):
    def construct(self):
        f,m,p=voltage_panel(0); self.add(f,m,p)
        self.at('balance point shows'); self.play(Indicate(m[2],color=PINK),run_time=.4)
        self.at('few synapses'); _,target,_=voltage_panel(.1); self.play(Transform(m,target),run_time=1)
        self.at('gate barely moves'); self.play(Indicate(p[1],color=ORANGE),run_time=.4); self.finish()

class S08CoopMany(SpokenScene):
    def construct(self):
        f,m,p=voltage_panel(.1); self.add(f,m,p)
        self.at('Many synapses together'); _,target,_=voltage_panel(2); self.play(Transform(m,target),run_time=2)
        self.at('calcium entry is greatest');
        # A second pore retains its block; the displaced Mg remains visible.
        other=VGroup(pore(-1.65,-.55,1.5),Dot([-1.65,-.55,0],radius=.19,color=ORANGE))
        self.play(FadeIn(other),p[1].animate.shift(UP*1.2),p[2].animate.shift(RIGHT*1.65),run_time=.5)
        self.play(FadeIn(lab('Near peak · about half unblocked',2.5,1.95,TEAL,26)),run_time=.3); self.finish()

class S09CoopName(SpokenScene):
    def construct(self):
        self.add(heading('Few and many synapses'))
        for x,g,name in [(-3.2,.1,'Few'),(3.2,2,'Many')]:
            v=voltage(g); ax=course(x,-.15,4.5,4.2)
            # Computed voltage position on identical vertical scales.
            scale=Line([x,-1.8,0],[x,1.8,0],color=GREY,stroke_width=4)
            pos=[x,-1.8+(v+70)/70*3.6,0]
            self.add(scale,Dot(pos,color=PINK,radius=.18),lab(name,x,2.3,TEXT,30),
                lab(f'≈ {v:.0f} mV'.replace('-','−'),x+1.35,pos[1],PINK,30),
                lab('−70',x-1,-1.8,TEXT,26),lab('0 mV',x-1,1.8,TEXT,26))
        self.at('cooperativity'); self.play(Transform(self.mobjects[0],heading('Cooperativity')),run_time=.3)
        self.at('single patch'); self.play(FadeIn(lab('Single-patch numbers • illustrative',0,-2.65,TEXT,30)),run_time=.3)
        self.at('read the direction'); self.play(FadeIn(lab('Real dendrites differ',0,-3.35,PINK,28)),run_time=.3); self.finish()

class S10AssocSetup(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(('weak','strong','silent'),False); ps=assocplots((None,None)); self.add(c,w,h,l,ps)
        self.at('take two pathways'); self.play(Indicate(w,scale_factor=1.02),run_time=.3)
        self.at('one weak'); self.play(Indicate(w[0],color=PATH[0]),run_time=.3)
        self.at('strong one can potentiate'); train(self,w,[1]); self.play(FadeOut(ps[0][1][3]),Create(trace(ps[0][1][0],True,GREEN)),run_time=.4); self.finish()

class S11AssocAlone(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(('weak','strong','silent'),False); ps=assocplots(); self.add(c,w,h,l,ps)
        self.at('Stimulated alone'); train(self,w,[0],4,pulse_time=.35)
        self.play(w[0].animate.set_stroke(width=6),run_time=.15)
        self.at('weak pathway fails'); self.play(FadeOut(ps[0][0][3]),Create(trace(ps[0][0][0])),run_time=.3)
        self.at('spines get glutamate');
        # Zoom the weak pathway's contact, explicitly connected to that wire.
        detail=spine(-3.5,-.6); detail.scale(.78).move_to([-3.6,-.65,0])
        for label in detail[3][:2]: label.scale(1/.78)
        py=detail[1][0].get_y()
        centers=[-5.2,-3.6,-2.0]
        detail.submobjects[1]=VGroup(*[pore(x,py,1.05) for x in centers])
        detail.submobjects[2]=VGroup(*[Dot([x,py,0],radius=.16,color=ORANGE) for x in centers])
        outline=detail[0][-1]
        detail.submobjects[0]=VGroup(*[Line([a,py,0],[b,py,0],color=GREY,stroke_width=7)
            for a,b in [(-5.94,-5.71),(-4.69,-4.11),(-3.09,-2.51),(-1.49,-1.26)]],outline)
        detail[3][1].move_to([-3.6,.95,0])
        origin=detail[3][1].get_center()
        detail[3][2].put_start_and_end_on(origin+LEFT*.25+DOWN*.12,[-5.05,py+.12,0])
        detail[3][3].put_start_and_end_on(origin+RIGHT*.25+DOWN*.12,[-2.15,py+.12,0])
        self.play(FadeOut(c),FadeOut(w[1]),FadeOut(h),FadeOut(l[1]),FadeIn(detail),run_time=.4)
        bound=VGroup(*[Dot(p[0].get_top(),radius=.12,color=YELLOW) for p in detail[1]])
        self.play(FadeIn(bound),FadeIn(VGroup(DashedLine([-2.5,2,0],[-1.1,2,0],color=PATH[0]),DashedLine([-1.1,2,0],[-1.1,-.1,0],color=PATH[0]))),run_time=.3)
        self.at('too little depolarization');
        self.play(FadeIn(lab('local voltage ≈ −65 mV',-3.6,1.3,PINK,26)),
            Create(Line([-6.25,-2,0],[-6.25,1.6,0],color=GREY,stroke_width=4)),
            FadeIn(Dot([-6.25,-2+5/70*3.6,0],color=PINK,radius=.13)),
            FadeIn(lab('0',-6.6,1.6,TEXT,22)),FadeIn(lab('−70',-6.2,-2.35,TEXT,22)),
            FadeIn(lab('block remains in most pores',-3.6,-2.6,ORANGE,26)),run_time=.35); self.finish()

class S12AssocPair(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(('weak','strong','silent'),False); ps=assocplots((None,None)); self.add(c,w,h,l,ps)
        self.at('stimulate the weak pathway'); train(self,w,[0,1],3)
        self.at('during the strong'); self.play(c[1].animate.set_color(PINK),h.animate.set_color(PINK),run_time=.3); train(self,w,[0,1],2)
        self.finish()

class S13AssocThird(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(('weak','strong','silent')); ps=assocplots((None,None)); self.add(c,w[:2],h[:2],l[:2],ps)
        self.at('third pathway'); self.play(Create(w[2]),FadeIn(h[2]),FadeIn(l[2]),run_time=.4); self.finish()

class S14Predict(SpokenScene):
    def construct(self):
        g=prediction(); self.add(g); self.at('Predict each'); self.play(Indicate(g[0],scale_factor=1.01),run_time=.4); self.finish()

class S15Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=prediction(title='Pause and predict'); self.add(g)
        # Countdown lives in the header, leaving the question plots unchanged.
        for n in range(5,0,-1):
            t=lab(str(n),6.25,3.15,GOLD,32); self.add(t); self.wait(1); self.remove(t)

class S16Reveal1(SpokenScene):
    def construct(self):
        g=prediction(); self.add(g); self.at('strong pathway is potentiated')
        self.play(FadeOut(g[1][0][3]),Create(trace(g[1][0][0],True,GREEN)),run_time=.5); self.finish()

class S17Reveal2(SpokenScene):
    def construct(self):
        g=prediction((True,True,None)); self.add(g)
        self.at('weak pathway is potentiated'); self.play(Indicate(g[1][1][3],color=GREEN),run_time=.4)
        self.at('supplied its own glutamate');
        detail=spine(0,.05); glu=bound_glus(0,.05).shift(UP*1.15)
        detail[3][1].move_to([0,1.45,0])
        detail[3][2].put_start_and_end_on([-.3,1.2,0],[-1.05,.2,0])
        detail[3][3].put_start_and_end_on([.3,1.2,0],[1.05,.2,0])
        self.play(FadeOut(g),FadeIn(detail),FadeIn(heading('Weak input’s spine',PATH[0])),FadeIn(glu),run_time=.4)
        self.play(glu.animate.shift(DOWN*1.15),FadeIn(lab('own glutamate binds',0,2,YELLOW,30)),run_time=.5)
        self.at('strong input supplied');
        arrow=Arrow([5.8,-1.9,0],[2.55,.05,0],color=PINK,buff=0,stroke_width=6)
        self.play(GrowArrow(arrow),FadeIn(lab('depolarization from',4.3,1.05,PINK,28)),
            FadeIn(lab('the strong input',4.3,.5,PINK,28)),detail[0].animate.set_color(PINK),run_time=.6)
        self.at('cleared the block');
        self.play(detail[2][0].animate.shift(UP*1.3+LEFT*.9),FadeOut(detail[3][2]),run_time=.4)
        self.play(FadeIn(lab('Partial unblock → Ca²⁺ entry',0,-2.65,TEAL,30)),
            GrowArrow(Arrow([-1.2,-.1,0],[-1.2,-1.25,0],color=TEAL,buff=0)),run_time=.3)
        self.play(FadeIn(lab('Weak pathway ↑ · potentiated',0,-3.2,GREEN,30)),run_time=.3); self.wait(1.4); self.finish()

class S18Reveal3(SpokenScene):
    def construct(self):
        detail=spine(0,.05); detail[0].set_color(PINK); detail[2][0].shift(UP*1.3+LEFT*.9)
        detail[3][1].move_to([0,1.45,0])
        detail[3][2].put_start_and_end_on([-.3,1.2,0],[-1.05,.2,0])
        detail[3][3].put_start_and_end_on([.3,1.2,0],[1.05,.2,0])
        self.add(detail,bound_glus(0,.05),heading('Weak input’s spine',PATH[0]),lab('Weak pathway ↑ · potentiated',0,-3.2,GREEN,30))
        self.at('third pathway stays'); g=prediction((True,True,False))
        self.play(*[FadeOut(o) for o in list(self.mobjects)],FadeIn(g),run_time=.5)
        self.at('released no glutamate'); self.play(Transform(g[4],lab('Third pathway: no glutamate',0,-3.4,YELLOW,28)),run_time=.3); self.finish()

class S19AssocName(SpokenScene):
    def construct(self):
        g=prediction((True,True,False)); self.add(g)
        self.at('associativity'); self.play(Transform(g[0],heading('Associativity')),run_time=.3)
        self.at('a Hebbian rule'); self.play(Transform(g[4],lab('A Hebbian rule in a dish',0,-3.4,TEXT,30)),run_time=.3); self.finish()

class S20Bap(SpokenScene):
    def construct(self):
        soma=Circle(.6,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([-4.7,-2.1,0])
        path=VMobject(color=GREY,stroke_width=9).set_points_as_corners([[-4.7,-2.1,0],[-3.5,-2.1,0],[-2,-2.4,0],[4.7,-2.4,0],[4.7,.3,0],[4.2,.3,0]])
        detail=spine(1.2,.3); glu=glus(1.2,.3)
        wire=VMobject(color=PATH[0],stroke_width=3).set_points_as_corners([[-5.5,2,0],[-.9,2,0],[-.9,1.1,0]])
        self.add(soma,path,detail,glu,wire,lab('weak input',-3.5,2.5,PATH[0],28),
            lab('cell body',-4.7,-3.1,TEXT,28),heading('Backpropagating spike'))
        self.at('spike fired by'); d=Dot([-4.7,-2.1,0],radius=.2,color=PINK)
        self.play(soma.animate.set_color(PINK),FadeIn(d),FadeIn(lab('spike',-4.7,-1,PINK,28)),run_time=.3)
        self.at('spreading back'); self.play(MoveAlongPath(d,path),run_time=1.1)
        self.at('can play'); self.play(detail[0].animate.set_color(PINK),detail[2][0].animate.shift(UP*1.2+LEFT*.8),FadeOut(d),run_time=.5)
        self.play(FadeIn(lab('Glutamate bound · partial unblock',1.3,-2.8,YELLOW,28)),run_time=.3); self.finish()

class S21Cue(SpokenScene):
    def construct(self):
        c,w,h,l=circuit(('weak','strong','silent'),False); ps=assocplots((None,None)); self.add(c,w,h,l,ps)
        self.at('shape an association'); self.play(FadeIn(lab('Associativity',-3.6,-1.3,TEXT,34)),run_time=.3)
        self.at('a cue'); self.play(Transform(l[0],lab('cue',-4.5,2.45,PATH[0],30)),
            Transform(ps[0][0][2][0],lab('Cue',3.65,2.775,TEXT,28)),run_time=.3)
        self.at('gains strength'); train(self,w,[0,1],2)
        self.play(w[0].animate.set_stroke(width=8),h[0].animate.set_color(GREEN),h[1].animate.set_color(PINK),
            FadeOut(ps[0][0][3]),Create(trace(ps[0][0][0],True,GREEN)),run_time=.4)
        self.at('when active with'); train(self,w,[0,1],2)
        self.at('an outcome'); self.play(Transform(l[1],lab('outcome',-4.5,.55,PATH[1],30)),
            Transform(ps[0][1][2][0],lab('Outcome',3.65,-.025,TEXT,28)),
            FadeOut(ps[0][1][3]),Create(trace(ps[0][1][0],True,GREEN)),run_time=.3); self.finish()

class S22Takeaway(SpokenScene):
    def construct(self):
        formula=VGroup(chip('glutamate',YELLOW,30),T('+',32),chip('depolarization',PINK,30)).arrange(RIGHT,buff=.4).move_to([0,2.35,0])
        gate=VGroup(pore(0,.7,1.1),Dot([0,.7,0],radius=.16,color=ORANGE),
            lab('Mg²⁺',-1.25,.7,ORANGE,28),lab('NMDA gate',2.5,.7,PURPLE,30))
        self.add(formula)
        self.at('one gate'); self.play(FadeIn(gate),Create(Line([0,1.9,0],[0,1.4,0],color=TEXT)),run_time=.4)
        self.at('reading two signals'); self.play(gate[1].animate.shift(UP*.55+LEFT*.75),
            FadeIn(lab('→ Ca²⁺ entry → LTP',0,-.45,TEAL,30)),run_time=.4)
        for phrase,name,x in [('input specificity','Input specificity',-4.4),('cooperativity','Cooperativity',0),('associativity','Associativity',4.3)]:
            self.at(phrase); self.play(Create(Line([0,-.8,0],[x,-1.8,0],color=GREY)),FadeIn(lab(name,x,-2.2,TEXT,30)),run_time=.3)
        self.at('right spines enough'); self.play(FadeIn(lab('When inputs depolarize the right spines enough',0,-3.1,PINK,27)),run_time=.35); self.finish()

class S23End(EndCard):
    LINE='One gate explains three properties when inputs depolarize the right spines enough.'
    def construct(self):
        g=VGroup(T('One gate explains three properties',36,font=TITLE_FONT),
            T('when inputs depolarize the right spines enough.',30,PINK),
            T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.6)
        self.add(g); self.finish()
