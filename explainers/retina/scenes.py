"""One Cell Counts. Narration/audio are authoritative.
COLOR MAP: YELLOW light; BLUE receptors/cations; TEAL glutamate;
PURPLE cGMP; ORANGE rhodopsin/transducin/PDE6; GREY structure.
Models: V = -80/(1+gCNG), gK=1. Illustrative normalized exponential
flash responses; seeded 0/1-pA mixture histogram; Govardovskii A1 template
as specified in lesson.mdx. Abstract retinal state icon, no molecular structure.
"""
import numpy as np
from bp_style import *
PURPLE='#B58AE8'
ORANGE='#F2A65A'
GLU=TEAL


def label(s,x=0,y=3.1,color=TEXT,size=30):
    return T(s,size=size,color=color).move_to([x,y,0])


def potassium_label(s,x,y,color=TEXT,size=28):
    # The house font has no Unicode subscript k; position a real K as a subscript.
    before,after=s.split('Eₖ')
    parts=VGroup()
    if before:parts.add(T(before,size=size,color=color))
    e=T('E',size=size,color=color);k=T('K',size=26,color=color)
    ek=VGroup(e,k.next_to(e,RIGHT,buff=.02).shift(DOWN*.15));parts.add(ek)
    if after:parts.add(T(after,size=size,color=color))
    parts.arrange(RIGHT,buff=.19,aligned_edge=UP)
    return parts.move_to([x,y,0])


def arrow(a,b,c=BLUE):
    return Arrow(a,b,buff=.06,color=c,stroke_width=5,tip_length=.18)


def rod(x=-4.8):
    """Fixed 5.6-unit silhouette, OS above; shared across all rod scenes."""
    outer=RoundedRectangle(width=1.35,height=2.65,corner_radius=.2,color=BLUE,fill_opacity=.22).move_to([x,1.25,0])
    discs=VGroup(*[Line([x-.5,y,0],[x+.5,y,0],color=BLUE,stroke_opacity=.65) for y in np.linspace(.15,2.35,8)])
    inner=RoundedRectangle(width=1.55,height=1.65,corner_radius=.35,color=BLUE,fill_opacity=.18).move_to([x,-1.05,0])
    neck=Line([x,-1.88,0],[x,-2.2,0],color=BLUE,stroke_width=6)
    terminal=RoundedRectangle(width=1.85,height=.65,corner_radius=.2,color=BLUE,fill_opacity=.25).move_to([x,-2.48,0])
    r=VGroup(outer,discs,inner,neck,terminal)
    r.os_,r.inner,r.term=outer,inner,terminal
    return r


class Gate(VGroup):
    """Pore in a vertical outer-segment wall; tracker controls its opening."""
    def __init__(self,x,y,gap):
        super().__init__()
        self.gap=gap
        self.cover=Rectangle(width=.36,height=.56,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,y,0])
        self.a=Rectangle(width=.3,height=.18,color=BLUE,fill_opacity=1)
        self.b=self.a.copy()
        self.add(self.cover,self.a,self.b)
        def update(m):
            g=gap.get_value()
            m.a.move_to([x,y+.09+g/2,0]);m.b.move_to([x,y-.09-g/2,0])
            m.a.set_color(BLUE if g>.05 else GREY);m.b.set_color(BLUE if g>.05 else GREY)
        self.add_updater(update);update(self)


class Stream(VGroup):
    def __init__(self,a,b,n=4,color=BLUE,speed=.6,fade=True):
        super().__init__(*[Dot(radius=.085,color=color) for _ in range(n)])
        self.phase=0.; self.speed=speed; self.activity=ValueTracker(1)
        a,b=np.array(a),np.array(b)
        def flow(m,dt):
            m.phase+=dt*m.speed
            for i,d in enumerate(m):
                t=(m.phase+i/n)%1
                d.move_to(a+(b-a)*t).set_opacity((min(1,t*8,(1-t)*8) if fade else 1) if i < max(1,round(n*m.activity.get_value())) else 0)
        self.add_updater(flow);flow(self,0)


def channels(r,opened=.34):
    x=r.os_.get_right()[0]
    gaps=[ValueTracker(opened) for _ in range(3)]
    gates=VGroup(*[Gate(x,y,g) for y,g in zip((.45,1.25,2.05),gaps)])
    dots=VGroup(*[Dot([x-.35,y,0],radius=.11,color=PURPLE) for y in (.45,1.25,2.05)])
    return gates,dots,gaps


def scale(g=1):
    x=4.55
    def pos(v):return np.array([x,-2.25+(v+80)/80*4.7,0])
    axis=VGroup(Line(pos(-80),pos(0),color=GREY,stroke_width=5))
    for v,txt in [(-80,'Eₖ ≈ −80 mV'),(-40,'−40 mV'),(0,'0 mV')]:
        p=pos(v)
        axis.add(Line(p+LEFT*.16,p+RIGHT*.16,color=TEXT),potassium_label(txt,x-1.65,p[1]) if 'Eₖ' in txt else label(txt,x-1.65,p[1],TEXT,28))
    marker=Dot(pos(-80/(1+g)),radius=.2,color=BLUE)
    return axis,marker,pos


def rope(start,end,c=BLUE,slack=0):
    a,b=np.array(start),np.array(end)
    # Straightening cord, a visible grip, and a directional pull at the anchor.
    ts=np.linspace(0,1,40)
    length=np.linalg.norm(b-a)
    wave=.07/max(length,.7)
    pts=[a+(b-a)*t+RIGHT*wave*np.sin(12*PI*t) for t in ts]
    cord=VMobject(color=c,stroke_width=6).set_points_as_corners(pts)
    grip=Circle(radius=.14,color=c,stroke_width=5).move_to(b)
    pull=arrow(a+(b-a)*.27,a,c)
    return VGroup(cord,grip,pull)


def tug(g=1):
    r=rod();ax,m,pos=scale(g)
    low=rope(pos(-80)+RIGHT*1.15,m.get_center())
    high=rope(m.get_center(),pos(0)+RIGHT*1.15)
    low.add_updater(lambda mob:mob.become(rope(pos(-80)+RIGHT*1.15,m.get_center())))
    high.strength=ValueTracker(1)
    high.add_updater(lambda mob:mob.become(rope(m.get_center(),pos(0)+RIGHT*1.15)).set_opacity(mob.strength.get_value()))
    labs=VGroup(VGroup(label('K⁺ channels',.4,-1.75,BLUE,30),Line([1.9,-1.75,0],[5.2,-1.75,0],color=BLUE,stroke_width=2)),VGroup(label('CNG channels',.4,1.85,BLUE,30),Line([2.1,1.85,0],[5.2,1.85,0],color=BLUE,stroke_width=2)),label('two-conductance model',1,-3.15,TEXT,28))
    return r,ax,m,low,high,labs,pos


def flash_kernel(t):
    u=np.maximum(np.asarray(t)-.18,0)
    v=(1-np.exp(-u/.13))*np.exp(-u/.3)
    z=np.maximum(np.linspace(0,1,1001)-.18,0)
    return v/np.max((1-np.exp(-z/.13))*np.exp(-z/.3))


def trace(x0,x1,y,amp=1,h=1,color=BLUE):
    ts=np.linspace(0,1,200)
    return VMobject(color=color,stroke_width=4).set_points_as_corners([[x0+(x1-x0)*t,y-h*amp*k,0] for t,k in zip(ts,flash_kernel(ts))])


def pathway():
    # Two rows keep every name readable at 26 pt.
    names=['photon','rhodopsin','transducin','PDE6','cGMP','CNG channels']
    nodes=VGroup(*[chip(n,c,size=30,pad=.18) for n,c in zip(names,[YELLOW,ORANGE,ORANGE,ORANGE,PURPLE,BLUE])])
    VGroup(*nodes[:3]).arrange(RIGHT,buff=.35).move_to([0,-2.35,0])
    VGroup(*nodes[3:]).arrange(RIGHT,buff=.35).move_to([0,-3.35,0])
    return nodes


def light_stage(node):
    # Restore readable text without making the chip fill opaque.
    return AnimationGroup(node[0].animate.set_opacity(1).set_fill(opacity=.3),
                          node[1].animate.set_opacity(1))


def spectrum(w):
    p=560.;x=p/np.asarray(w);a=.8795+.0459*np.exp(-(p-300)**2/11940)
    return 1/(np.exp(69.7*(a-x))+np.exp(28*(.922-x))+np.exp(-14.9*(1.104-x))+.674)+.26*np.exp(-((np.asarray(w)-(189+.315*p))/(-40.5+.195*p))**2)


def cone(x,y=0):
    outer=Polygon([x,2+y,0],[x-.65,.1+y,0],[x+.65,.1+y,0],color=BLUE,fill_opacity=.3)
    inner=Ellipse(width=1.15,height=1.35,color=BLUE,fill_opacity=.2).move_to([x,-.7+y,0])
    stem=Line([x,-1.35+y,0],[x,-2+y,0],color=BLUE,stroke_width=5)
    term=Ellipse(width=1.4,height=.55,color=BLUE,fill_opacity=.3).move_to([x,-2.2+y,0])
    discs=VGroup(*[Line([x-w,h+y,0],[x+w,h+y,0],color=BLUE) for h,w in [(1.35,.17),(.95,.3),(.55,.44)]])
    return VGroup(outer,inner,stem,term,discs)


def prediction():
    ax=Axes(x_range=[400,700,100],y_range=[0,1.1,.5],x_length=7.8,y_length=4.6,tips=False,axis_config={'color':GREY,'include_ticks':True}).move_to([1.55,.15,0])
    ws=np.linspace(400,700,240)
    curve=VMobject(color=BLUE,stroke_width=5).set_points_as_corners([ax.c2p(w,spectrum(w)) for w in ws])
    labs=VGroup(label('sensitivity',-3.5,.7,TEXT,28).rotate(PI/2),label('wavelength (nm)',1.5,-2.9,TEXT,28),label('schematic pigment sensitivity',1.7,3.2,TEXT,28))
    for w in (400,500,600,700):labs.add(label(str(w),ax.c2p(w,0)[0],-2.5,TEXT,26))
    for v in (0,.5,1):labs.add(label(str(v),ax.c2p(400,v)[0]-.4,ax.c2p(400,v)[1],TEXT,26))
    c=cone(-5.1)
    base=VGroup(ax,curve,c,labs,label('one cone',-5.1,-2.95,BLUE,28))
    p=ax.c2p(560,spectrum(560));q=ax.c2p(620,spectrum(620))
    dim=VGroup(Dot(p,radius=.13,color=YELLOW),label('dim · at peak',.1,2.6,YELLOW,28),Line([.65,2.35,0],p+UP*.12,color=YELLOW),arrow([-5.5,3.3,0],[-5.2,2,0],YELLOW))
    bright=VGroup(Dot(q,radius=.22,color=YELLOW),label('brighter · off peak',4.35,2.65,YELLOW,28),Line([4.35,2.35,0],q+UP*.2,color=YELLOW),arrow([-4.2,3.3,0],[-4.95,1.9,0],YELLOW).set_stroke(width=11))
    question=label('Can the cone tell them apart?',0,-3.5,TEXT,36)
    return base,dim,bright,question


def matched_graph():
    """Stacked mean/trial panels; y units deliberately relative, not measured."""
    g=VGroup()
    for y,name in [(1.75,'dim · near peak'),(-.45,'brighter · off peak')]:
        g.add(label(name,-3.8,y-.45,YELLOW,28))
        g.add(Line([-1.4,y+.25,0],[-1.4,y-1.65,0],color=GREY),Line([-1.4,y-1.65,0],[5.8,y-1.65,0],color=GREY))
        for a in (.69,.83,1.18,1.32):g.add(trace(-1.2,5.7,y,a,1.05).set_stroke(width=2,opacity=.5))
        g.add(trace(-1.2,5.7,y,1,1.05).set_stroke(width=7))
    g.add(label('response (relative units)',-6.1,-.15,TEXT,26).rotate(PI/2),label('time →',3,-2.5,TEXT,28))
    return g


class S00Title(TitleCard):
    LESSON='The Retina'
    TITLE='One Cell Counts'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,1.5,TEAL,28),label('THE RETINA',0,.75,TEXT,28),label(self.TITLE,0,-.2,TEXT,56),Line([-1.3,-1.15,0],[1.3,-1.15,0],color=GOLD,stroke_width=4))
        self.wait(self.narration_s)


class S01Question(SpokenScene):
    def construct(self):
        hair=VGroup(RoundedRectangle(width=1.3,height=3,corner_radius=.5,color=BLUE,fill_opacity=.18).move_to([-4.5,-.2,0]),*[Line([-4.9+i*.4,1.3,0],[-4.75+i*.4,2.2,0],color=BLUE,stroke_width=6) for i in range(3)])
        touch=VGroup(Ellipse(width=2,height=3.2,color=BLUE,fill_opacity=.18).move_to([0,.2,0]),Line([0,-1.4,0],[0,-2.6,0],color=BLUE,stroke_width=6))
        r=rod(4.5)
        self.add(hair,touch,r,label('hair cell',-4.5,-3.15,BLUE,30),label('touch ending',0,-3.15,BLUE,30),label('rod',4.5,-3.15,BLUE,30))
        self.at('Most sensory receptors')
        sound=VGroup(*[Arc(radius=.28+i*.2,start_angle=-PI/3,angle=2*PI/3,color=YELLOW).move_to([-6,1.65,0]) for i in range(3)])
        pressure=arrow([1.6,2.8,0],[.5,1.2,0],YELLOW)
        self.at('excited by their stimulus')
        self.play(Create(sound),GrowArrow(pressure),hair.animate.set_fill(BLUE,.8),touch.animate.set_fill(BLUE,.8),run_time=.7)
        self.at('Rods and cones');self.play(r.animate.set_fill(BLUE,.85),run_time=.3)
        self.at('turned down')
        light=arrow([6.2,3.2,0],[4.7,1.9,0],YELLOW)
        self.play(GrowArrow(light),r.animate.set_opacity(.25),run_time=.65)
        self.at('How does quieting')
        self.play(FadeIn(label('How does quieting a cell let you see?',0,3.35,TEXT,36)),run_time=.35)
        self.finish()


class S02Dark(SpokenScene):
    def construct(self):
        r=rod();ch,dots,gaps=channels(r)
        self.add(r,ch,dots,label('DARK',-4.8,3.15,TEXT,32))
        self.at('Start with a rod')
        labs=VGroup(label('outer segment',-1.2,1.9,BLUE,28),label('inner segment',-1.2,-1.05,BLUE,28),label('terminal',-1.2,-2.5,BLUE,28))
        leaders=VGroup(*[Line([r.get_center()[0]+.85,y,0],[-2.7,y,0],color=BLUE) for y in (1.9,-1.05,-2.5)])
        self.play(FadeIn(labs),FadeIn(leaders),run_time=.5)
        self.at('cyclic GMP')
        self.play(FadeIn(label('cGMP',3.6,1.7,PURPLE,34)),Create(Line([2.8,1.5,0],[-4.3,1.25,0],color=PURPLE,stroke_width=2)),Indicate(dots,color=PURPLE),run_time=.5)
        self.at('holds channels open')
        self.play(FadeIn(label('cyclic-nucleotide-gated',3,.55,BLUE,28)),FadeIn(label('(CNG) channels',3,-.1,BLUE,30)),FadeIn(label('held open by cGMP',3,-1.3,PURPLE,30)),FadeIn(Line([.1,.4,0],[-4.125,.45,0],color=BLUE,stroke_width=2)),Indicate(ch,color=BLUE),run_time=.6)
        self.finish()


class S03Current(SpokenScene):
    def construct(self):
        r=rod();ch,dots,gaps=channels(r);self.add(r,ch,dots)
        self.at('Sodium and calcium')
        flows=VGroup(*[Stream([-2.8,y,0],[-4.6,y,0],n=3,fade=False) for y in (.45,1.25,2.05)])
        self.add(flows,label('Na⁺ + Ca²⁺ in',.8,1.8,BLUE,34))
        self.at('steady dark current')
        # Continuous circulation: OS inward, down cell, IS outward, outside up.
        pts=[[-3.1,2.45,0],[-4.125,2.45,0],[-4.125,-1.05,0],[-2.45,-1.05,0],[-2.45,2.45,0],[-3.1,2.45,0]]
        loop=VGroup(*[arrow(a,b) for a,b in zip(pts[:-1],pts[1:])])
        self.play(Create(loop),FadeIn(label('dark current',1,-.1,BLUE,40)),FadeIn(label('K⁺ out',-.8,-1.05,BLUE,30)),run_time=.6)
        self.at('keeps the rod depolarized')
        self.play(FadeIn(label('depolarized',1,-1.9,BLUE,32)),run_time=.35)
        self.at('releasing glutamate')
        glu=Stream([-4.8,-2.8,0],[-4.8,-3.65,0],n=5,color=GLU,speed=.8)
        self.add(glu);self.play(FadeIn(label('steady glutamate release',.7,-3.15,GLU,30)),run_time=.4)
        self.finish()


class S04Tug(SpokenScene):
    def construct(self):
        r,ax,m,l,h,labs,pos=tug(0)
        self.add(r,ax,m,labs[2])
        self.at('Potassium channels')
        l=rope(pos(-80)+RIGHT*1.15,m.get_center())
        l.add_updater(lambda mob:mob.become(rope(pos(-80)+RIGHT*1.15,m.get_center())))
        self.play(Create(l),FadeIn(labs[0]),run_time=.7)
        self.at('pull the other way')
        h=rope(m.get_center(),pos(0)+RIGHT*1.15)
        h.add_updater(lambda mob:mob.become(rope(m.get_center(),pos(0)+RIGHT*1.15)))
        self.play(Create(h),FadeIn(labs[1]),run_time=.5)
        # Keep pulling through the end of the sentence, then continue in s05.
        self.play(m.animate.move_to(pos(-46)),run_time=max(.5,self.narration_s-self.elapsed()-.1),rate_func=linear)
        self.finish()


class S05Balance(SpokenScene):
    def construct(self):
        r,ax,m,l,h,labs,pos=tug();m.move_to(pos(-46));self.add(r,ax,m,l,h,labs)
        self.at('With the two')
        # Model equilibrium gK=gCNG. Damped approach is only the visual easing.
        self.play(m.animate.move_to(pos(-40)),run_time=max(1.05,self.t_of('near minus forty')-.3),rate_func=smooth)
        self.play(FadeIn(label('dark potential ≈ −40 mV',.5,3.2,BLUE,34)),run_time=.3)
        self.at('near minus forty');self.play(Flash(m,color=BLUE),run_time=.4)
        self.finish()


class S06Photon(SpokenScene):
    def construct(self):
        r=rod();self.add(r,label('outer-segment disc',-3.4,-3.2,BLUE,28))
        disc=Line([-5.3,1.25,0],[-4.3,1.25,0],color=ORANGE,stroke_width=8)
        rho=RoundedRectangle(width=5.3,height=3.2,corner_radius=.4,color=ORANGE,fill_opacity=.13).move_to([2,.6,0])
        connector=VGroup(Line([-4.1,1.25,0],[-.7,1.9,0],color=ORANGE),Line([-4.1,1.25,0],[-.7,-.8,0],color=ORANGE))
        bent=VMobject(color=ORANGE,stroke_width=12).set_points_as_corners([[.5,.4,0],[1.8,1.15,0],[3.4,.4,0]])
        state=label('11-cis retinal',2,-1.65,ORANGE,32)
        self.add(disc,rho,connector,bent,state,label('rhodopsin',2,2.75,ORANGE,36),label('abstract state icon',2,-2.5,TEXT,26))
        self.at('Now a photon arrives')
        photon=Dot([-6,3.2,0],radius=.2,color=YELLOW)
        ray=arrow([-6,3.2,0],[-4.8,1.25,0],YELLOW)
        self.add(photon,label('photon',-4.8,3.3,YELLOW,30))
        self.play(GrowArrow(ray),photon.animate.move_to([-4.8,1.25,0]),run_time=.9)
        self.play(Flash(disc,color=YELLOW),run_time=.4)
        self.at('It straightens the retinal')
        straight=Line([.5,.65,0],[3.4,.65,0],color=ORANGE,stroke_width=12)
        self.play(Transform(bent,straight),FadeOut(photon),run_time=.85)
        self.remove(state);self.add(label('all-trans retinal',2,-1.65,ORANGE,32))
        self.at('the pigment becomes active')
        self.play(rho.animate.set_fill(ORANGE,.45),FadeIn(label('ACTIVE',2,-.4,YELLOW,38)),run_time=.6)
        self.finish()


class S07Gain(SpokenScene):
    def construct(self):
        rho=chip('one active rhodopsin',ORANGE,30).move_to([-3.7,.7,0])
        chain=pathway();td=VGroup(*[chip('transducin',ORANGE,28).move_to([2.9,y,0]) for y in (2.3,1.45,.6,-.25,-1.1)])
        chain.set_opacity(.4)
        self.add(rho,chain,label('one input → many outputs',0,3.3,ORANGE,36))
        self.at('One active rhodopsin');self.play(light_stage(chain[0]),light_stage(chain[1]),rho[0].animate.set_fill(ORANGE,.45),run_time=.4)
        self.at('switches on many')
        arrows=VGroup(*[arrow(rho.get_right(),t.get_left(),ORANGE) for t in td])
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a),FadeIn(t)) for a,t in zip(arrows,td)],lag_ratio=.2),run_time=1)
        self.play(FadeIn(label('many more',3,-1.7,ORANGE,30)),run_time=.35)
        self.at('the gain');self.play(FadeIn(label('gain = amplification',-2,-1.3,ORANGE,34)),light_stage(chain[2]),run_time=.5)
        self.finish()


class S08Enzyme(SpokenScene):
    def construct(self):
        chain=pathway();td=chip('transducin',ORANGE,30).move_to([-4.5,2.5,0]);pde=chip('PDE6',ORANGE,34).move_to([-4.5,.6,0])
        dots=VGroup(*[Dot([x,.6,0],radius=.17,color=PURPLE) for x in (-1.5,-.5,.5,1.5)])
        gaps=[ValueTracker(.4) for _ in range(3)]
        gates=VGroup(*[Gate(4.6,y,g) for y,g in zip((-.9,.4,1.7),gaps)])
        wall=Line([4.6,-1.6,0],[4.6,2.5,0],color=BLUE,stroke_width=5)
        chain.set_opacity(.4);chain[2].set_opacity(1);chain[2][0].set_fill(opacity=.3)
        self.add(chain,td,dots,wall,gates,label('cGMP',0,1.8,PURPLE,32),label('CNG channels',4.5,3.2,BLUE,30))
        self.at('turns on an enzyme')
        self.play(GrowArrow(arrow(td.get_bottom(),pde.get_top(),ORANGE)),FadeIn(pde),light_stage(chain[3]),run_time=.6)
        self.at('destroys the messenger')
        self.play(GrowArrow(arrow(pde.get_right(),[-1.8,.6,0],ORANGE)),FadeIn(label('cGMP falls',0,-.55,PURPLE,32)),run_time=.4)
        self.play(LaggedStart(*[FadeOut(d,scale=.05) for d in dots],lag_ratio=.45),run_time=1.1)
        self.at('The messenger falls');self.play(light_stage(chain[4]),run_time=.35)
        self.at('the channels close')
        self.play(LaggedStart(*[g.animate.set_value(0) for g in gaps],lag_ratio=.3),FadeIn(label('CNG channels close',1.1,-1.65,BLUE,32)),light_stage(chain[5]),run_time=.9)
        self.finish()


class S09Slide(SpokenScene):
    def construct(self):
        r,ax,m,l,h,labs,pos=tug();self.add(r,ax,m,l,h,labs)
        self.at('With fewer cation channels')
        toward=potassium_label('toward Eₖ',2.0,.25,BLUE,32)
        toward.add_updater(lambda lab:lab.set_y(m.get_y()-.5))
        self.add(toward)
        self.play(h.strength.animate.set_value(.55),m.animate.move_to(pos(-46)),run_time=1.3)
        self.at('potassium wins');self.play(Indicate(l),m.animate.move_to(pos(-49)),run_time=.9)
        self.at('The balance point slides')
        self.play(m.animate.move_to(pos(-52)),run_time=.9)
        self.finish()


class S10Graded(SpokenScene):
    def construct(self):
        r,ax,m,l,h,labs,pos=tug(80/52-1);h.strength.set_value(.55);self.add(r,ax,m,l,h,labs[2])
        ch,dots,gaps=channels(r,.2);self.add(ch)
        glu=Stream([-4.8,-2.8,0],[-4.8,-3.65,0],n=4,color=GLU,speed=1,fade=False)
        self.add(glu,label('dim flash',-4.8,3.25,YELLOW,30),label('illustrative voltage',.5,2.6,TEXT,28))
        self.at('The rod hyperpolarizes');self.play(FadeIn(label('hyperpolarizes',.2,1.65,BLUE,32)),m.animate.move_to(pos(-58)),run_time=.65)
        self.at('its glutamate release falls')
        self.play(glu.activity.animate.set_value(.5),FadeIn(label('less glutamate',-2.1,-2.45,GLU,32)),run_time=.4);glu.speed=.3
        self.at('Brighter light')
        self.play(FadeIn(label('brighter',-2.8,2.7,YELLOW,30)),GrowArrow(arrow([-2.7,2.3,0],[-4.2,1.5,0],YELLOW)),m.animate.move_to(pos(-72)),gaps[0].animate.set_value(0),gaps[1].animate.set_value(.1),h.strength.animate.set_value(.25),run_time=.9)
        glu.speed=.12;glu.activity.set_value(.25)
        self.at('The response is graded');self.play(FadeIn(label('graded · not all or none',1,-1.25,BLUE,32)),run_time=.4)
        self.finish()


class S11Calcium(SpokenScene):
    def construct(self):
        r=rod();ch,dots,gaps=channels(r,.04)
        ca=VGroup(*[Dot([x,y,0],radius=.12,color=BLUE) for x,y in [(-5.1,.4),(-4.65,.7),(-5.05,1.1),(-4.55,1.5),(-5,1.9)]])
        ca_title=label('Ca²⁺ falls',.4,3.2,BLUE,36)
        level=Rectangle(width=1.1,height=2.3,color=BLUE,fill_opacity=.6).move_to([2.3,-1.3,0])
        level_frame=Rectangle(width=1.1,height=2.3,color=GREY).move_to(level)
        level_lab=label('outer-segment Ca²⁺',2.3,-3,BLUE,30)
        self.add(r,ch,ca,ca_title,level,level_frame,level_lab)
        self.at('Calcium falls too')
        self.at('fewer open channels')
        incoming=arrow([-2.9,2.05,0],[-4,2.05,0]).set_opacity(.4)
        inlab=label('less Ca²⁺ in',-.7,2,BLUE,30)
        self.play(GrowArrow(incoming),FadeIn(inlab),run_time=.4)
        self.at('while the rod keeps removing it')
        out=arrow([-4.5,.3,0],[-2.9,.3,0]);outlab=label('pumped out',-.6,.3,BLUE,30)
        self.play(GrowArrow(out),FadeIn(outlab),level.animate.stretch_to_fit_height(.25).move_to([2.3,-2.325,0]),LaggedStart(*[FadeOut(d,shift=RIGHT*1.7) for d in ca],lag_ratio=.18),run_time=1)
        self.at('Low calcium speeds')
        self.play(FadeOut(incoming),FadeOut(inlab),FadeOut(out),FadeOut(outlab),FadeOut(level),FadeOut(level_frame),FadeOut(level_lab),FadeIn(label('Ca²⁺ low',-2.4,1.25,BLUE,30)),run_time=.3)
        gc=chip('GCAPs',PURPLE,30).move_to([.1,1.25,0]);cyc=chip('cyclase',PURPLE,30).move_to([3.9,1.25,0])
        self.play(FadeIn(gc),GrowArrow(arrow([-1.4,1.25,0],gc.get_left(),PURPLE)),FadeIn(cyc),GrowArrow(arrow(gc.get_right(),cyc.get_left(),PURPLE)),run_time=.65)
        self.at('the remaking of the messenger')
        produced=VGroup(*[Dot([x,-.25,0],radius=.14,color=PURPLE) for x in (2.8,3.5,4.2,4.9)])
        self.play(GrowArrow(arrow(cyc.get_bottom(),[3.9,.1,0],PURPLE)),LaggedStart(*[FadeIn(d,scale=.1) for d in produced],lag_ratio=.2),FadeIn(label('cGMP remade',3.8,-1.1,PURPLE,30)),run_time=.7)
        self.at('The rod recovers')
        # Reuse the same voltage scale and position mapping as the tug scenes.
        self.play(*[FadeOut(obj) for obj in (gc,cyc,produced,ca_title)],
                  *[FadeOut(obj) for obj in list(self.mobjects)
                    if obj not in (r,ch,gc,cyc,produced,ca_title)],run_time=.25)
        ax,mark,pos=scale(80/72-1)
        self.add(ax,mark,label('recovery',.3,2.8,BLUE,38))
        self.play(*[g.animate.set_value(.24) for g in gaps],
                  mark.animate.move_to(pos(-80/1.7)),run_time=1.1)
        self.at('turns its gain down')
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not r and m is not ch],run_time=.3)
        self.add(label('light adaptation: gain turned down',.6,3.2,BLUE,32),label('same flash',1.6,2.2,YELLOW,30),label('brighter background',-4.8,-3.25,YELLOW,27),Rectangle(width=1.9,height=4.7,stroke_width=0,fill_color=YELLOW,fill_opacity=.12).move_to([-4.8,.1,0]),*[arrow([x,2.75,0],[x,2.2,0],YELLOW) for x in (-5.3,-4.8,-4.3)])
        small=trace(-1.7,5.8,-1.4,.45,1.3)
        self.add(label('before',-.5,1.4,BLUE,28),label('after adaptation',2.5,-2.65,BLUE,28))
        self.play(GrowArrow(arrow([1.6,1.8,0],[1.6,1.2,0],YELLOW)),Create(trace(-1.7,5.8,.8,1,1.3)),Create(small),run_time=.65)
        self.finish()


class S12Baylor(SpokenScene):
    def construct(self):
        r=rod();self.add(r,label('toad rod',-4.8,-3.25,BLUE,30))
        self.at('How small can the signal be');self.play(FadeIn(label('How small can the signal be?',.6,3.3,TEXT,34)),run_time=.4)
        # Hollow tapered glass walls narrow into a snug cuff around the OS.
        pip=VGroup(*[VMobject(color=TEXT,stroke_width=4).set_points_as_corners(pts) for pts in [[[-6,3.0,0],[-6,2.6,0],[-5.55,1.65,0],[-5.55,.45,0]],[[-3.6,3,0],[-3.6,2.6,0],[-4.05,1.65,0],[-4.05,.45,0]]]])
        self.at('drew the outer segment');self.play(Create(pip),run_time=.8)
        self.at('into a glass pipette')
        self.play(FadeIn(label('suction electrode',-1.25,2, TEXT,28)),Create(Line([-2.8,2,0],[-4.05,1.5,0],color=TEXT)),run_time=.5)
        axes=VGroup(Line([-1.7,1,0],[-1.7,-1.7,0],color=GREY),Line([-1.7,-1.7,0],[5.8,-1.7,0],color=GREY),label('current',-.7,.9,TEXT,28),label('time →',4.4,-2.25,TEXT,28),label('dark current',2.3,.1,BLUE,30))
        self.play(FadeIn(axes),Create(trace(-1.6,5.8,-.55,0)),FadeIn(label('Baylor, Lamb & Yau · 1979',1.8,-3.15,TEXT,28)),run_time=.6)
        self.finish()


class S13Flashes(SpokenScene):
    def construct(self):
        self.add(label('Repeated dim flashes',0,3.3,YELLOW,36),label('current',-5.3,2.7,TEXT,28),Line([-5.6,2.3,0],[-5.6,-2.55,0],color=GREY),Line([-5.6,-2.55,0],[5.6,-2.55,0],color=GREY),label('time →',4.8,-3.2,TEXT,28),label('illustrative traces',-1.5,-3.2,TEXT,28))
        ys=[2, .75,-.7]; amps=[0,.9,1.1]
        self.at('They repeated a very dim flash')
        # First no-response trial, then one dip and another; each gets its own flash.
        def trial(i,a):
            tick=arrow([-3.6,ys[i]+.5,0],[-3.6,ys[i]+.05,0],YELLOW)
            self.play(GrowArrow(tick),run_time=.2)
            self.play(Create(trace(-5.3,5.5,ys[i],a,.95)),run_time=.65)
        trial(0,0)
        self.at('Some flashes gave nothing');self.play(FadeIn(label('no response',3.6,2.4,TEXT,28)),run_time=.3)
        self.at('Many gave a dip');trial(1,.9);trial(2,1.1)
        self.at('near one')
        bar=VGroup(Line([5.8,.75,0],[5.8,-.2,0],color=TEXT,stroke_width=4),Line([5.65,.75,0],[5.95,.75,0],color=TEXT),Line([5.65,-.2,0],[5.95,-.2,0],color=TEXT),label('1 pA',5.75,1.2,TEXT,28))
        self.play(FadeIn(bar),run_time=.35);self.finish()


class S14Quantal(SpokenScene):
    def construct(self):
        rng=np.random.default_rng(1979);samples=np.r_[rng.normal(0,.065,70),rng.normal(1,.09,100)]
        bins=np.linspace(-.2,1.3,25);counts,_=np.histogram(samples,bins)
        ax=Axes(x_range=[-.2,1.35,.5],y_range=[0,32,10],x_length=9.5,y_length=4.7,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.7,.1,0])
        bars=VGroup(*[Rectangle(width=9.5/1.55*(bins[i+1]-bins[i])*.9,height=max(.015,4.7*c/32),color=BLUE,fill_opacity=.7).move_to(ax.c2p((bins[i]+bins[i+1])/2,c/2)) for i,c in enumerate(counts)])
        labs=VGroup(label('number of flashes',-5.5,0,TEXT,28).rotate(PI/2),label('response size (pA)',.7,-3.05,TEXT,28),label('model histogram',.7,3.35,TEXT,28))
        for v in (0,10,20,30):
            p=ax.c2p(-.2,v);labs.add(Line(p+LEFT*.08,p+RIGHT*.08,color=TEXT),label(str(v),p[0]-.5,p[1],TEXT,26))
        for v in (0,.5,1):
            p=ax.c2p(v,0);labs.add(Line(p+UP*.08,p+DOWN*.08,color=TEXT),label(str(v),p[0],p[1]-.35,TEXT,26))
        ax.y_axis.set_opacity(0)
        self.add(ax,labs,Line(ax.c2p(-.2,0),ax.c2p(-.2,32),color=GREY))
        self.at('The sizes did not vary smoothly')
        # Trace fragments physically fall to the appropriate response bins.
        fragments=VGroup(trace(-4,-2,2.4,0,.5),trace(1,3,2.4,.9,.5),trace(3.2,5.2,2.4,1.1,.5))
        self.add(fragments)
        targets=[ax.c2p(0,0),ax.c2p(.9,0),ax.c2p(1.1,0)]
        self.play(*[m.animate.scale(.15).move_to(p) for m,p in zip(fragments,targets)],run_time=.7)
        self.play(FadeOut(fragments),LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.03),run_time=1.1)
        zero=label('no photon',-2.9,2.6,YELLOW,28);one=label('one photoisomerization',2.7,2.65,ORANGE,28)
        self.play(FadeIn(zero),Indicate(VGroup(*bars[:7])),run_time=.5)
        self.at('Each event was one pigment molecule')
        self.play(FadeIn(one),Indicate(VGroup(*bars[15:])),run_time=.6)
        self.at('activated by one photon');self.play(Indicate(one),run_time=.5)
        self.at('In dim light')
        labs[2].set_opacity(0)
        self.play(FadeIn(label('A rod counts photons',.4,3.35,TEXT,38)),run_time=.4)
        self.finish()


class S15Predict(SpokenScene):
    def construct(self):
        base,dim,bright,q=prediction();self.add(base)
        self.at('Two lights fall on one cone')
        self.at('One is dim');self.play(FadeIn(dim),run_time=.5)
        self.at('One is brighter');self.play(FadeIn(bright),run_time=.5)
        self.at('Can the cone tell them apart');self.play(FadeIn(q),run_time=.4)
        self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(*prediction());self.wait(5)


class S17Reveal(SpokenScene):
    def construct(self):
        c=cone(0).scale(1.25).move_to([0,-.05,0])
        catch_title=label('same mean photon catch',0,3.35,YELLOW,34)
        self.add(c,catch_title)
        lights=VGroup(label('dim · near peak',-2,2.6,YELLOW,30),label('brighter · off peak',2,2.6,YELLOW,30))
        # Each label stays directly above its own separated catch column.
        self.add(lights)
        self.at('Not if the two')
        catches=VGroup(*[Dot([side*2,1.85-.4*i,0],radius=.13,color=YELLOW)
                        for side in (-1,1) for i in range(5)])
        self.add(catches)
        self.at('the same photon catch')
        self.play(*[d.animate.move_to([(-.3 if i<5 else .3),.55+.25*(i%5),0]) for i,d in enumerate(catches)],run_time=.8)
        # Leaders preserve the link after absorption into the enlarged cone.
        links=VGroup(Line([-2,2.25,0],[-.3,1.85,0],color=YELLOW),Line([2,2.25,0],[.3,1.85,0],color=YELLOW))
        self.play(FadeIn(links),run_time=.2)
        count=label('matched mean catch',0,-3,YELLOW,30);self.play(FadeIn(count),run_time=.3)
        self.at('with the same timing');timing=label('same timing',-3.3,-3.5,BLUE,32);self.play(FadeIn(timing),run_time=.3)
        self.at('under the same adaptation');adapt=label('same adaptation',3.1,-3.5,BLUE,32);self.play(FadeIn(adapt),run_time=.3)
        self.at('Once absorbed')
        self.play(FadeOut(c),FadeOut(catches),FadeOut(links),FadeOut(lights),FadeOut(count),FadeOut(catch_title),FadeIn(matched_graph()),run_time=.6)
        self.add(label('bold: mean · thin: single trials',0,3.3,TEXT,28))
        self.at('the same effect');self.play(FadeIn(label('univariance',0,2.55,BLUE,38)),run_time=.4)
        self.finish()


class S18Takeaway(SpokenScene):
    def construct(self):
        graph=matched_graph().shift(UP*.55)
        self.add(graph,label('same average response',0,3.35,TEXT,34))
        self.at('one photoreceptor cannot separate')
        self.play(FadeIn(label('univariance: wavelength and intensity',0,-2.65,BLUE,30)),FadeIn(label('cannot be told apart',0,-3.25,BLUE,30)),run_time=.4)
        self.at('The takeaway')
        self.clear()
        self.add(label('One receptor is univariant;',0,.5,BLUE,40),label('the circuit compares.',0,-.6,TEXT,40))
        self.at('the circuit compares');self.finish()


class S19End(EndCard):
    LINE='One receptor is univariant; the circuit compares.'
    def construct(self):
        self.clear()
        self.add(label('One receptor is univariant;',0,.45,TEXT,40),label('the circuit compares.',0,-.5,TEXT,40))
        self.wait(self.narration_s)
