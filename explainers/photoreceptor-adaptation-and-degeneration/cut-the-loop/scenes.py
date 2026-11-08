"""Cut the Loop — word-timed chapter animation.
COLOR MAP (shared with scenes.old.py): YELLOW light; ORANGE calcium;
PURPLE sensors / GRK1; TEAL membrane proteins; GREEN cGMP / adaptation;
PINK active pigment; BLUE control photoreceptors; RED deficient / off;
GREY membranes / unknowns. Kept here because chapter metadata is read-only.
All curves use the earlier film's explicit illustrative response equations or
S/Sdark = 1 / (1 + (I/I0)**n), with its published fit parameters.
"""
import numpy as np
from bp_style import *
PURPLE, ORANGE, PINK = '#B58CD9', '#F29E4C', '#E58FB0'
CTRL = dict(I0=48800, n=1.0)
KO = dict(I0=12100, n=1.5)
SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')


def label(s, x=0, y=0, size=28, color=TEXT):
    return T(s, size, color).move_to([x,y,0])


def head(s, color=TEXT):
    return label(s, 0, 3.15, 34, color)


def box(s, x, y, color=BLUE, size=28):
    return chip(s, color, size).move_to([x,y,0])


def arrow(a,b,color=GREY):
    return Arrow(a,b,buff=.14,color=color,stroke_width=5)


def rod():
    body=RoundedRectangle(width=1.5,height=4.2,corner_radius=.3,color=BLUE,fill_color=BLUE,fill_opacity=.13)
    disks=VGroup(*[Line([-.5,y,0],[.5,y,0],color=BLUE,stroke_opacity=.5) for y in np.linspace(-1.7,1.7,10)])
    return VGroup(body,disks)


def loop_picture():
    r=rod().move_to([-2.5,-.1,0])
    loop=Circle(radius=2.55,color=ORANGE,stroke_width=7).move_to([-2.5,-.1,0])
    return VGroup(r,loop)


def scissors():
    return VGroup(Circle(.17,color=TEXT).move_to([0,-.18,0]),Circle(.17,color=TEXT).move_to([.4,-.18,0]),Line([0,0,0],[.65,.8,0],color=TEXT),Line([.4,0,0],[-.25,.8,0],color=TEXT))


def channel(opened=True, gap_open=.3):
    # Two protein jaws: widening the gap is the visible opening action.
    gap=gap_open if opened else .03
    return VGroup(*[RoundedRectangle(width=.25,height=.75,corner_radius=.07,color=TEAL,fill_color=TEAL,fill_opacity=.7).move_to([s*(gap+.125),0,0]) for s in (-1,1)])


def membrane(closed=False, question=False, low=False):
    wall=RoundedRectangle(width=7.3,height=3.6,corner_radius=.25,color=GREY,fill_color=GREY,fill_opacity=.05).move_to([-1.8,-.1,0])
    ch=channel(not closed).scale(1.4).move_to([-3.5,1.7,0])
    pump=box('NCKX',.3,-1.9,TEAL,30)
    pump[0].set_fill(BG,opacity=1); pump.set_z_index(3)
    names=VGroup(label('outer segment',-2,-.6,28,GREY),label('channel',-1.9,2.4,28,TEAL),label('exchanger',2.1,-2.3,28,TEAL))
    gauge=Rectangle(width=.85,height=3.25,color=ORANGE).move_to([4.6,-.1,0])
    fill=Rectangle(width=.69,height=.5 if low else 2.95,stroke_width=0,fill_color=ORANGE,fill_opacity=.85).align_to(gauge,DOWN).shift(UP*.1).set_x(4.6)
    gtext=label('calcium\ninside',4.6,2.25,28,ORANGE)
    mark=label('?',4.6,-.1,48) if question else VGroup()
    inside=VGroup(*[Dot([x,y,0],radius=.1,color=ORANGE) for x,y in [(-4,.5),(-2.8,.9),(-1.4,.5),(-.1,.7),(-3.7,-1.1),(-1.2,-1.2)]])
    return VGroup(wall,ch,pump,names,gauge,fill,gtext,mark,inside)


def flow(scene,x,y0,y1):
    dots=VGroup(*[Dot([x+dx,y0,0],radius=.10,color=ORANGE) for dx in (-.12,.12)])
    scene.add(dots)
    scene.play(dots.animate.shift(UP*(y1-y0)),run_time=.65)
    scene.remove(dots)


def predict1():
    g=membrane(closed=True,question=True)
    q=head('Which way does calcium move?')
    light=label('light flash',-4.8,3.05,28,YELLOW)
    out=arrow([.3,-1.1,0],[.3,-3.15,0],ORANGE).set_z_index(2)
    choices=VGroup(*[box(t,x,-3.35,ORANGE,28) for t,x in [('rises',-4.8),('falls',-2.8),('stays',-.8)]])
    return VGroup(g,q,light,out,choices)


def predict2():
    return VGroup(head('Rods lacking GCAP1 + GCAP2',RED),box('(a) Darkness: one photon',0,1.8,YELLOW,30),label('Bigger or smaller?',0,.7,36),box('(b) On a background',0,-.8,YELLOW,30),label('Is adaptation better or worse?',0,-2,32),label('Pause and predict',0,-3.2,28,TEAL))


def response(ax, tau, amplitude, color, dip=False, end=8):
    # Explicit illustrative impulse model, not a measured trace.
    return ax.plot(lambda t: (-1 if dip else 1)*amplitude*(t/tau)*np.exp(1-t/tau),x_range=[0,end,.025],color=color,stroke_width=6,use_smoothing=False)


def flash_plot():
    ax=Axes(x_range=[0,8,2],y_range=[-1.1,.1,.5],x_length=10.5,y_length=4.6,axis_config={'include_tip':False,'include_ticks':False,'color':GREY}).move_to([0,-.1,0])
    return ax,VGroup(ax,label('current',-5.5,2.7,28,BLUE),label('time after flash (s)',0,-2.9,28,GREY),label('illustrative response model',0,-3.5,26,GREY))


def logS(x,I0,n):
    return -np.log10(1+10**(n*(x-np.log10(I0))))


def cone_plot():
    ax=Axes(x_range=[2,6,1],y_range=[-3,0,1],x_length=8.1,y_length=4.6,axis_config={'include_tip':False,'include_ticks':False,'color':GREY},tips=False).move_to([-1.2,-.05,0])
    # Manim places the horizontal axis at y=0; draw a genuine bottom axis.
    ax.x_axis.set_opacity(0)
    bottom=Line(ax.c2p(2,-3),ax.c2p(6,-3),color=GREY)
    ticks=VGroup(*[VGroup(Line(ax.c2p(k,-3),ax.c2p(k,-3)+DOWN*.12,color=GREY),T('10'+str(k).translate(SUP),26,GREY).next_to(ax.c2p(k,-3),DOWN,buff=.17)) for k in range(2,7)],*[T(v,26,GREY).next_to(ax.c2p(2,y),LEFT,buff=.15) for y,v in [(0,'1'),(-1,'0.1'),(-2,'0.01'),(-3,'0.001')]])
    base=VGroup(ax,bottom,ticks,head('Cone sensitivity fits'),label('background (photons per µm² per s)',-1,-3.05,26,GREY),label('S / Sdark',-4.5,2.7,28,TEXT),label('Vinberg & Kefalov 2018',-4.3,-3.65,26,GREY))
    split=np.log10(400000)
    curves=VGroup(*[VGroup(ax.plot(lambda x,p=p:logS(x,**p),x_range=[2,split,.02],color=c,stroke_width=6,use_smoothing=False),DashedVMobject(ax.plot(lambda x,p=p:logS(x,**p),x_range=[split,6,.01],color=c,stroke_width=6,use_smoothing=False),num_dashes=10)) for p,c in [(CTRL,BLUE),(KO,RED)]])
    legend=VGroup(label('control',4.6,2.2,28,BLUE),label('GCAPs +',4.6,1.45,26,RED),label('recoverin',4.6,.95,26,RED),label('absent',4.6,.45,26,RED),label('Dotted: beyond\ntested range\n(≈ 400,000)',4.6,-1.7,26,GREY))
    return ax,base,curves,legend


def half_marks(ax):
    return VGroup(*[VGroup(DashedLine(ax.c2p(np.log10(p['I0']),-3),ax.c2p(np.log10(p['I0']),np.log10(.5)),color=c),Dot(ax.c2p(np.log10(p['I0']),np.log10(.5)),color=c,radius=.09)) for p,c in [(CTRL,BLUE),(KO,RED)]])


def summary():
    # Fixed-width, equal-type cells: no sentence crosses a column boundary.
    headers=VGroup(head('Removing calcium feedback'),label('Cell / intervention',-4.2,2.3,26,GREY),label('Darkness',-.6,2.3,28,GREY),label('Background',3.7,2.3,28,GREY),Line([-6.4,1.9,0],[6.4,1.9,0],color=GREY))
    rods=VGroup(label('Rods\nGCAPs absent',-4.2,1.1,26,RED),label('≈ 5× larger\nslow recovery',-.6,1.1,26,RED),label('Adaptation\ncompromised',3.7,1.1,26,RED))
    cones=VGroup(label('Cones\nGCAPs +\nrecoverin absent',-4.2,-.45,26,RED),label('Slower peak\n142 vs 56 ms',-.6,-.45,26,RED),label('Steeper fitted\nsensitivity decline',3.7,-.45,26,RED))
    normal=VGroup(label('Normal',-4.2,-2,26,BLUE),label('smaller, brief',-.6,-2,26,BLUE),label('Weber-like over a range\nof bright backgrounds\n(some current in reserve)',3.7,-2,26,BLUE))
    return VGroup(headers,rods,cones,normal)


def product_plot(knockout=False):
    p,c=(KO,RED) if knockout else (CTRL,BLUE)
    # Identical y scale across genotypes preserves the magnitude comparison.
    ax=Axes(x_range=[4.5,7,.5],y_range=[0,50000,25000],x_length=6.5,y_length=4.7,axis_config={'include_tip':False,'include_ticks':False,'color':GREY}).move_to([-2,-.1,0])
    fn=lambda x:10**x/(1+(10**x/p['I0'])**p['n'])
    split=np.log10(400000)
    curve=ax.plot(fn,x_range=[4.5,split,.02],color=c,stroke_width=6,use_smoothing=False)
    extra=DashedVMobject(ax.plot(fn,x_range=[split,7,.02],color=c,stroke_width=6,use_smoothing=False),num_dashes=35)
    ticks=VGroup(*[T('10'+str(k).translate(SUP),26,GREY).next_to(ax.c2p(k,0),DOWN,buff=.15) for k in range(5,8)],*[T(f'{v:,}',26,GREY).next_to(ax.c2p(4.5,v),LEFT,buff=.14) for v in [0,25000,50000]])
    rows=['48,800 → '+('≈ 5,400' if knockout else '24,400'),'10⁶ → '+('1,330 *' if knockout else '46,500 *'),'10⁷ → '+('420 *' if knockout else '48,600 *')]
    table=VGroup(*[label(v,3.8,1.1-i*.7,28,c) for i,v in enumerate(rows)])
    base=VGroup(head('Illustrative fit calculations'),ax,ticks,label('(S / Sdark) × I',-3.7,2.7,28,c),label('photons per µm² per s',-1.7,-3.3,26,GREY),label('control cones' if not knockout else 'GCAPs + recoverin\nabsent',3.8,2.55,26,c),label('background → product',3.8,1.75,26,GREY),table,label('* Beyond tested range (up to ≈ 400,000)',0,-3.65,26,GREY))
    dot=Dot(ax.c2p(np.log10(48800),fn(np.log10(48800))),radius=.1,color=c)
    samples=VGroup(*[Dot(ax.c2p(x,fn(x)),radius=.09,color=c) for x in (6,7)]) if knockout else VGroup()
    return ax,base,VGroup(curve,VGroup(extra,samples),dot)


def rod_trace(recovered=False):
    ax=Axes(x_range=[0,10,2],y_range=[0,1,.5],x_length=10.5,y_length=4.8,axis_config={'include_tip':False,'include_ticks':False,'color':GREY}).move_to([.2,-.1,0])
    base=VGroup(head('Mouse rod-driven responses'),ax,label('continued exposure →',2.65,-2.95,28,GREY),label('cone-deficient mice • illustrative model',0,-3.55,26,GREY),DashedLine(ax.c2p(2,0),ax.c2p(2,1),color=YELLOW),label('very bright background',-3.55,-2.95,26,YELLOW),label('rod-driven contrast sensitivity',-6.05,.1,28,BLUE).rotate(PI/2))
    before=ax.plot(lambda x:.9,x_range=[0,2,.02],color=BLUE,stroke_width=6,use_smoothing=False)
    # Illustrative smoothstep fall and exponential recovery, not recorded values.
    drop=ax.plot(lambda x:.9-.72*(3*(x-2)**2-2*(x-2)**3),x_range=[2,3,.015],color=BLUE,stroke_width=6,use_smoothing=False)
    recovery=ax.plot(lambda x:.18+.64*(1-np.exp(-((x-3)/2.2)**2)),x_range=[3,10,.03],color=BLUE,stroke_width=6,use_smoothing=False)
    return base,VGroup(before,drop),recovery


class S00Title(TitleCard):
    TITLE='Cut the Loop'
    LESSON='Calcium Feedback Sets Photoreceptor Gain, and When Photoreceptors Die'
    def construct(self):
        # Wrap the full lesson title while preserving readable type.
        brand=label('BIOCHEMISTRYPEDIA',0,2.0,22,TEAL)
        lesson=label('Calcium Feedback Sets Photoreceptor Gain,\nand When Photoreceptors Die',0,.8,26,GREY)
        title=label(self.TITLE,0,-.65,54)
        rule=Line([-1.3,-1.5,0],[1.3,-1.5,0],color=GOLD,stroke_width=4)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.6)
        self.play(Write(title),Create(rule),run_time=.9)
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        g=loop_picture(); self.add(g,head('What happens when calcium feedback is cut?'),label('calcium feedback',-2.5,-3.2,30,ORANGE),label('photoreceptor',2.8,0,32,BLUE))
        self.at('if you cut')
        gap=Arc(radius=2.55,start_angle=.22,angle=TAU-.44,color=ORANGE,stroke_width=7).move_arc_center_to([-2.5,-.1,0])
        self.play(Transform(g[1],gap),FadeIn(scissors().scale(.7).move_to([.05,-.1,0])),run_time=.55)
        self.finish()


class S02Ca(SpokenScene):
    def construct(self):
        g=membrane(); self.add(g)
        entry=arrow([-3.5,2.9,0],[-3.5,.3,0],ORANGE)
        self.at('Calcium enters'); self.add(entry)
        flow(self,-3.5,2.8,.5)
        self.at('an exchanger')
        self.add(arrow([.3,-1,0],[.3,-3.3,0],ORANGE).set_z_index(2))
        flow(self,.3,-1,-3.2)
        self.finish()


class S03Predict1(SpokenScene):
    def construct(self):
        g=membrane(); self.add(g,head('Predict: calcium inside?'))
        self.at('Light closes')
        light=label('light flash',-4.9,3.05,28,YELLOW)
        beam=arrow([-5.1,2.9,0],[-3.9,1.95,0],YELLOW)
        self.play(FadeIn(light),GrowArrow(beam),Transform(g[1],channel(False).scale(1.4).move_to(g[1])),Flash([-3.5,1.7,0],color=YELLOW),run_time=.5)
        self.at('pumping goes on')
        self.add(arrow([.3,-1.1,0],[.3,-3.15,0],ORANGE).set_z_index(2)); flow(self,.3,-1,-3.2)
        self.at('Which way')
        self.add(label('?',4.6,-.1,48))
        self.play(FadeIn(VGroup(*[box(t,x,-3.35,ORANGE,28) for t,x in [('rises',-4.8),('falls',-2.8),('stays',-.8)]])),run_time=.3)
        self.finish()


class S04Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(predict1())
        count=label('Pause and predict: 5',3.7,-3.35,26,TEAL); self.add(count)
        for n in range(5,0,-1):
            count.become(label(f'Pause and predict: {n}',3.7,-3.35,26,TEAL)); self.wait(1)


class S05Falls(SpokenScene):
    def construct(self):
        g=membrane(closed=True); self.add(g,head('Calcium falls',ORANGE))
        self.add(label('entry falls',-3.7,3.3,28,ORANGE),arrow([-4.9,2.85,0],[-4,1.9,0],ORANGE))
        self.add(label('extrusion continues',.2,-3.35,28,TEAL),arrow([.3,-1.1,0],[.3,-3,0],ORANGE).set_z_index(2))
        self.at('Calcium falls'); self.play(Transform(g[5],membrane(closed=True,low=True)[5]),run_time=.9)
        self.at('pumping continues'); flow(self,.3,-1,-3)
        self.finish()


class S06Gcap(SpokenScene):
    def construct(self):
        self.add(head('Ca falls',ORANGE))
        sensors=VGroup(box('GCAP1 + GCAP2',-1.2,1.8,PURPLE,38),box('recoverin',3.8,1.8,PURPLE,32))
        self.add(sensors)
        self.at('Two main calcium sensors'); self.play(Indicate(sensors,color=PURPLE,scale_factor=1.02),run_time=.4)
        self.at('First')
        cyc=box('cyclase',-1.2,-.15,TEAL,38); cg=box('cGMP',2.3,-1.8,GREEN,38)
        self.play(GrowArrow(arrow(sensors[0].get_bottom(),cyc.get_top(),PURPLE)),FadeIn(cyc),FadeOut(sensors[1]),run_time=.5)
        self.at('synthesis'); b=arrow(cyc.get_right(),cg.get_top(),GREEN)
        self.play(GrowArrow(b),FadeIn(cg),run_time=.5)
        self.at('up to about'); self.add(label('up to about 20-fold',-1.2,-2.9,34,GREEN))
        self.play(b.animate.set_stroke(width=12),run_time=.5)
        self.finish()


class S07Reopen(SpokenScene):
    def construct(self):
        g=membrane(closed=True,low=True); g[3][0].set_opacity(0); g[8].set_opacity(0); self.add(g)
        cg=box('more cGMP',-2,-1,GREEN,32); self.add(cg)
        self.at('More CGMP'); self.play(GrowArrow(arrow(cg.get_top(),[-3.5,1.1,0],GREEN)),run_time=.5)
        self.at('reopens channels'); self.play(Transform(g[1],channel(True,gap_open=.58).scale(1.4).move_to(g[1])),run_time=.5)
        self.add(arrow([-3.5,2.9,0],[-3.5,.3,0],ORANGE)); flow(self,-3.5,2.8,.5)
        self.at('This is the strongest'); self.play(FadeIn(head('Strongest calcium feedback',GREEN)),run_time=.4)
        flow(self,-3.5,2.8,.5)
        self.finish()


class S08Recoverin(SpokenScene):
    def construct(self):
        self.add(head('Ca falls',ORANGE))
        pocket=RoundedRectangle(width=4.5,height=2.1,corner_radius=.25,color=PURPLE,stroke_width=5).move_to([-2.7,1,0])
        rec=label('recoverin',-2.7,2.5,32,PURPLE); kinase=box('GRK1',-2.7,1,PURPLE,34)
        self.add(pocket,rec,kinase)
        self.at('lets go')
        cue=label('Ca falls',-3.6,-1.2,30,ORANGE)
        trigger=arrow(cue.get_top(),[-3.6,-.05,0],ORANGE)
        release=arrow([-.3,1,0],[1.65,1,0],PURPLE)
        self.play(FadeIn(cue),GrowArrow(trigger),kinase.animate.move_to([2.5,1,0]),GrowArrow(release),pocket.animate.set_stroke(opacity=.4),rec.animate.set_opacity(.4),run_time=.65)
        self.at('That kinase')
        pig=box('active pigment',.9,-1.4,PINK,34)
        self.play(FadeIn(pig),GrowArrow(arrow([2.5,.5,0],[.9,-.9,0],PURPLE)),run_time=.5)
        self.at('switches off'); self.play(Transform(pig,box('pigment off',.9,-1.4,GREY,34)),run_time=.5)
        self.at('so pigment'); self.play(FadeIn(label('Pigment off sooner',0,-3,36,PINK)),run_time=.4)
        self.finish()


class S09Jobs1(SpokenScene):
    def construct(self):
        self.add(head('Steady background',YELLOW),label('current available',0,2.3,32,BLUE))
        bars=VGroup(*[Rectangle(width=1.6,height=3.8,color=BLUE).move_to([x,-.25,0]) for x in (-3,3)])
        fills=VGroup(*[Rectangle(width=1.4,height=.7,stroke_width=0,fill_color=BLUE,fill_opacity=.85).align_to(b,DOWN).shift(UP*.1).set_x(b.get_x()) for b in bars])
        self.add(bars,fills,label('without feedback',-3,-2.8,28,RED),label('with feedback',3,-2.8,28,GREEN))
        self.at('it reopens channels')
        fill=Rectangle(width=1.4,height=2.7,stroke_width=0,fill_color=BLUE,fill_opacity=.85).align_to(bars[1],DOWN).shift(UP*.1).set_x(3)
        self.play(Transform(fills[1],fill),run_time=.8)
        self.at('keeps current'); self.play(FadeIn(label('Job one: current in reserve',0,-3.5,30,BLUE)),run_time=.4)
        self.finish()


class S10Jobs2(SpokenScene):
    def construct(self):
        ax,base=flash_plot(); self.add(base,head('Test flash',YELLOW))
        old=response(ax,1.5,.95,GREY,True); outline=DashedVMobject(old.copy(),num_dashes=45).set_opacity(.7)
        new=response(ax,.55,.35,BLUE,True)
        self.at('During each new flash'); self.play(Create(old),run_time=.65)
        self.add(label('without feedback',2,-1.65,28,GREY))
        self.at('pushes against the change'); self.add(outline)
        self.play(Transform(old,new),FadeIn(label('lower gain',2,-.35,32,GREEN)),run_time=.8)
        self.at('Each photon'); self.play(FadeIn(label('smaller, briefer dip',2,-1.1,28,BLUE)),run_time=.4)
        self.finish()


class S11Mendez(SpokenScene):
    def construct(self):
        self.add(head('Mouse rods lacking GCAP1 + GCAP2',RED))
        sensor=box('GCAPs absent',-3.2,1.5,RED,36); cg=box('cGMP synthesis',2.8,-1.3,GREEN,36)
        a=arrow(sensor.get_right(),cg.get_top(),PURPLE); self.add(sensor,cg,a)
        self.at('Now cut'); self.play(a.animate.set_opacity(.2),FadeIn(label('×',.5,.9,60,RED)),run_time=.5)
        self.at('Mendez and colleagues'); self.play(FadeIn(label('Mendez and colleagues, 2001',0,-3.1,30,GREY)),run_time=.5)
        self.finish()


class S12Predict2(SpokenScene):
    def construct(self):
        g=predict2(); self.add(g[0],g[1],g[2],g[5])
        self.at('On a background'); self.play(FadeIn(g[3]),FadeIn(g[4]),run_time=.4)
        self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(predict2()); self.wait(5)

class S14Bigger(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,16,4],y_range=[-5.3,.1,1],x_length=10.5,y_length=4.7,axis_config={'include_tip':False,'include_ticks':False,'color':GREY}).move_to([0,-.1,0])
        ctrl=response(ax,.55,1,BLUE,True,end=16); ko=response(ax,1.9,5,RED,True,end=16)
        self.add(ax,head('Single-photon response in darkness'),label('current',-5.4,2.65,28,BLUE),label('time after photon (s)',0,-2.95,28,GREY),label('Illustrative response model',0,-3.55,26,GREY))
        for t in (4,8,12,16): self.add(Line(ax.c2p(t,0),ax.c2p(t,0)+UP*.12,color=GREY),T(str(t),26,GREY).next_to(ax.c2p(t,0),UP,buff=.15))
        self.at('In darkness'); self.play(Create(ctrl),FadeIn(label('control',-3.6,1.1,28,BLUE)),run_time=.5)
        self.at('about five times'); self.play(Create(ko),FadeIn(label('≈ 5× larger',-1.4,-1.5,30,RED)),run_time=.65)
        self.at('Without the'); self.play(FadeIn(label('GCAPs absent',1.8,-.8,28,RED)),run_time=.4)
        self.at('restored more slowly'); self.play(FadeIn(label('cGMP restored slowly',2,-1.7,28,GREEN)),run_time=.4)
        self.at('responses recover'); self.play(Indicate(ko,color=RED,scale_factor=1.01),run_time=.5)
        self.finish()


class S15Worse(SpokenScene):
    def construct(self):
        self.add(head('Background adaptation: worse',RED))
        self.add(label('normal',-3,2.15,30,BLUE),label('GCAPs absent',3,2.15,30,RED))
        for x,h,c in [(-3,2.6,BLUE),(3,.55,RED)]:
            bar=Rectangle(width=2,height=3.8,color=c).move_to([x,-.3,0])
            fill=Rectangle(width=1.8,height=h,stroke_width=0,fill_color=c,fill_opacity=.7).align_to(bar,DOWN).shift(UP*.1).set_x(x)
            self.add(bar,fill)
        self.add(label('current held in reserve • schematic',0,-2.85,28,GREY))
        self.at('adaptation was'); self.play(FadeIn(label('Adaptation severely compromised',0,-3.5,30,RED)),run_time=.5)
        self.finish()


class S16Cones(SpokenScene):
    def construct(self):
        ax,base,curves,legend=cone_plot(); self.add(base,curves[0],legend[0])
        self.at('In cones lacking'); self.play(Create(curves[1]),FadeIn(VGroup(*legend[1:])),run_time=.7)
        self.at('the fitted'); self.play(Create(half_marks(ax)),run_time=.5)
        self.at('sat at about')
        labels=VGroup()
        for p,c,side in [(KO,RED,LEFT),(CTRL,BLUE,RIGHT)]:
            dot=ax.c2p(np.log10(p['I0']),np.log10(.5))
            txt=T(f"{p['I0']:,}",26,c).next_to(dot,side+(UP if p is CTRL else DOWN),buff=.24)
            labels.add(txt,Line(dot,txt.get_bottom() if p is CTRL else txt.get_top(),color=c,stroke_width=2))
        self.play(FadeIn(labels),FadeIn(label('≈ ¼ control',4.6,-.35,26,RED)),run_time=.5)
        self.at('That shift was'); self.play(Transform(base[3],head('Half-sensitivity shift: not significant',TEXT)),run_time=.5)
        self.finish()


class S17Steep(SpokenScene):
    def construct(self):
        ax,base,curves,legend=cone_plot(); self.add(base,curves,legend)
        self.at('their sensitivity fell')
        blue=label('n = 1.0',.1,2.6,28,BLUE); red=label('n = 1.5',.5,-1.9,28,RED)
        leaders=VGroup(Line(blue.get_bottom(),ax.c2p(4.7,logS(4.7,**CTRL)),color=BLUE,stroke_width=2),Line(red.get_top(),ax.c2p(5,logS(5,**KO)),color=RED,stroke_width=2))
        self.play(FadeIn(blue),FadeIn(red),Create(leaders),FadeIn(label('n sets slope at high background',0,-3.65,26,TEXT)),run_time=.5)
        # The definition replaces the credit so the footer never overlaps.
        self.remove(base[-1])
        self.at('and that difference'); self.play(Transform(base[3],head('Slope difference: significant',GREEN)),run_time=.5)
        self.finish()


class S18Paradox(SpokenScene):
    def construct(self):
        g=summary(); self.add(g[0],g[1])
        self.at('removing the feedback'); self.play(FadeIn(g[2]),run_time=.4)
        self.at('adaptation worse'); self.play(FadeIn(g[3]),run_time=.4)
        self.finish()


class S19Resolve(SpokenScene):
    def construct(self):
        g=summary(); self.add(g)
        hi=SurroundingRectangle(VGroup(g[1][1],g[2][1],g[3][1]),color=GREEN,buff=.18)
        tag=label('Darkness: trim each response',0,-3.45,28,GREEN)
        self.at('In darkness'); self.play(Create(hi),FadeIn(tag),run_time=.5)
        self.at('On a background')
        other=SurroundingRectangle(VGroup(g[1][2],g[2][2],g[3][2]),color=GREEN,buff=.18)
        self.play(Transform(hi,other),Transform(tag,label('Background: trim + reserve',0,-3.45,28,GREEN)),run_time=.6)
        self.finish()


class S20Arith(SpokenScene):
    def construct(self):
        self.add(head('Small-flash regime').set_y(3.55))
        pulse=VMobject(color=YELLOW,stroke_width=5).set_points_as_corners([[-5,1,0],[-1.5,1,0],[-1.5,2.35,0],[1.5,2.35,0],[1.5,1,0],[5,1,0]])
        compact=pulse.copy()
        pulse.stretch(1.65,1,about_point=[0,2.35,0])
        background=label('background I',-3.8,-.4,28,YELLOW)
        self.add(pulse,background)
        self.at('Take a small')
        bracket=VGroup(Line([-1.5,2.75,0],[1.5,2.75,0],color=YELLOW),Line([-1.5,2.65,0],[-1.5,2.85,0],color=YELLOW),Line([1.5,2.65,0],[1.5,2.85,0],color=YELLOW))
        self.play(Create(bracket),FadeIn(label('T',0,2.95,28,YELLOW)),run_time=.4)
        self.at('Its extra intensity')
        self.play(Transform(pulse,compact),background.animate.set_y(.55),run_time=.3)
        self.play(FadeIn(label('ΔI = C × I',3.7,1.9,30,YELLOW)),FadeIn(label('C = contrast',-3.8,1.9,26,TEXT)),run_time=.5)
        self.at('its photon count')
        self.play(FadeIn(label('F = C × I × T',-2.8,-.4,32)),FadeIn(label('F = photons in the flash',3,-.4,26,TEXT)),run_time=.5)
        self.at('Its peak response')
        self.play(FadeIn(label('peak ≈ S(I) × C × I × T',0,-1.45,32)),FadeIn(label('peak = maximum response',0,-2.15,26,TEXT)),run_time=.5)
        self.at('sensitivity times')
        self.play(FadeIn(label('S(I) = sensitivity on background I',0,-2.8,26,TEXT)),FadeIn(label('Fixed C and T: peak tracks S(I) × I',0,-3.5,28,GREEN)),run_time=.5)
        self.finish()


class S21Control(SpokenScene):
    def construct(self):
        ax,base,curves=product_plot(); self.add(*base[:7],base[8],base[7][0])
        self.at('Multiply sensitivity'); self.play(Create(curves[0]),FadeIn(curves[2]),run_time=.6)
        self.at('For normal cones'); self.play(Create(curves[1]),FadeIn(VGroup(*base[7][1:])),run_time=.8)
        self.at('the product climbs'); self.play(Create(DashedLine(ax.c2p(4.5,48800),ax.c2p(7,48800),color=BLUE)),FadeIn(label('ceiling 48,800',-.7,1.2,26,BLUE)),run_time=.5)
        self.at('On bright backgrounds'); self.play(FadeIn(label('contrast responses hold',3.8,-1.6,28,GREEN)),run_time=.5)
        self.finish()


class S21Hold(Scene):
    def construct(self):
        self.camera.background_color=BG; ax,base,curves=product_plot()
        self.add(base,curves,DashedLine(ax.c2p(4.5,48800),ax.c2p(7,48800),color=BLUE),label('ceiling 48,800',-.7,1.2,26,BLUE),label('contrast responses hold',3.8,-1.6,28,GREEN)); self.wait(2)


class S22Knockout(SpokenScene):
    def construct(self):
        ax,base,curves=product_plot(True); self.add(*base[:7],base[8],base[7][0])
        self.at('For the knockout'); self.play(Create(curves[0]),FadeIn(curves[2]),run_time=.6)
        self.at('the product falls'); self.play(Create(curves[1]),FadeIn(VGroup(*base[7][1:])),FadeIn(label('10× brighter\n≈ 3× less',3.8,-1.6,30,RED)),run_time=.7)
        self.finish()


class S22Hold(Scene):
    def construct(self):
        self.camera.background_color=BG; ax,base,curves=product_plot(True)
        self.add(base,curves,label('10× brighter\n≈ 3× less',3.8,-1.6,30,RED)); self.wait(2)


class S23Runout(SpokenScene):
    def construct(self):
        ax,base,curves=product_plot(True); self.add(base,curves)
        self.remove(base[0])
        self.add(head('Illustrative fit calculations'),label('Consistent with less\ncurrent in reserve',-1.8,1.05,30,RED))
        self.at('A fall steeper'); self.play(curves.animate.set_stroke(width=10),run_time=.5)
        self.at('But the slope'); self.play(FadeIn(label('Slope is not a\ncurrent measurement',3.8,-1.6,28,TEXT)),run_time=.5)
        self.finish()


class S24Remainder(SpokenScene):
    def construct(self):
        q=DashedVMobject(Rectangle(width=10.5,height=5.6,color=GREY),num_dashes=60)
        self.add(q,head('Some adaptation remains',GREEN),label('?',0,.6,86,TEXT),label('Cause unresolved',0,-1,36,TEXT),label('GCAP1 + GCAP2 + recoverin absent',0,-2.2,28,RED))
        self.at('Some adaptation'); self.play(Indicate(q,color=GREEN,scale_factor=1.01),run_time=.6)
        self.finish()


class S25Rods(SpokenScene):
    def construct(self):
        base,early,recovery=rod_trace(); self.add(base,early[0])
        self.at('On a very bright'); self.play(Indicate(base[4]),run_time=.5)
        self.at('responses dip'); self.play(Create(early[1]),run_time=.6)
        self.finish()


class S26Recover(SpokenScene):
    def construct(self):
        base,early,recovery=rod_trace(); self.add(base,early)
        self.at('Then they recover'); self.play(Create(recovery),run_time=1.4)
        self.at('A model suggests'); self.play(FadeIn(label('Model suggests:',2.5,-.5,28,TEXT)),run_time=.3)
        self.at('gain changes'); a=box('gain changes',1,-1.35,GREEN,28)
        self.play(FadeIn(a),GrowArrow(arrow(a.get_left(),[.2,.1,0],GREEN)),run_time=.4)
        self.at('pigment bleaching'); b=box('bleaching',4,-1.35,PINK,28)
        self.play(FadeIn(b),GrowArrow(arrow(b.get_right(),[4.9,1.35,0],PINK)),Transform(base[3],label('Illustrative • Tikidji-Hamburyan et al., 2017',0,-3.55,26,GREY)),run_time=.4)
        self.finish()


class S27Daylight(SpokenScene):
    def construct(self):
        r=rod().scale(1.2).move_to([-3,-.1,0])
        sun=VGroup(Circle(radius=.65,color=YELLOW,fill_color=YELLOW,fill_opacity=.7),*[Line([.85*np.cos(a),.85*np.sin(a),0],[1.15*np.cos(a),1.15*np.sin(a),0],color=YELLOW) for a in np.linspace(0,TAU,12,endpoint=False)]).move_to([2.5,1.7,0])
        self.add(r,sun)
        self.at('rods do not'); self.add(label('In these mice,\nrods still respond',2,-.8,36,TEXT),label('Mouse retina and thalamus',0,-3.3,30,TEXT))
        self.finish()


class S28Take(SpokenScene):
    def construct(self):
        loop=Circle(radius=1.65,color=ORANGE,stroke_width=7).move_to([-4.3,.9,0])
        self.add(loop,head('Calcium feedback',ORANGE),label('feedback',-4.3,.9,28,ORANGE))
        one=box('Trims each response',1.8,1.9,GREEN,32); two=box('Keeps current in reserve',1.8,.5,BLUE,32)
        a=arrow([-2.65,1.3,0],one.get_left(),GREEN); b=arrow([-2.65,.5,0],two.get_left(),BLUE)
        bar=Rectangle(width=7.3,height=.8,color=BLUE).move_to([.8,-1.6,0])
        fill=Rectangle(width=4.9,height=.65,stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to(bar).align_to(bar,LEFT).shift(RIGHT*.08)
        low=Rectangle(width=1.2,height=.65,stroke_width=0,fill_color=BLUE,fill_opacity=.9).move_to(bar).align_to(bar,LEFT).shift(RIGHT*.08)
        caption=label('current in reserve',.8,-.9,30,BLUE)
        dashed=DashedVMobject(Rectangle(width=5.4,height=.8,color=GREY).move_to([.8,-3,0]),num_dashes=30)
        self.at('trims each response'); self.play(GrowArrow(a),FadeIn(one),run_time=.4)
        self.at('keeps current'); self.play(GrowArrow(b),FadeIn(two),FadeIn(bar),FadeIn(fill),FadeIn(caption),run_time=.4)
        self.at('Cut it')
        gap=Arc(radius=1.65,start_angle=PI/2+.22,angle=TAU-.44,color=ORANGE,stroke_width=7).move_arc_center_to([-4.3,.9,0])
        loop.become(gap)
        caption.become(label('less current in reserve',.8,-.9,30,RED))
        dim_one=one.copy().set_opacity(.4); dim_one[0].set_fill(opacity=.064)
        dim_two=two.copy().set_opacity(.4); dim_two[0].set_fill(opacity=.064)
        self.play(FadeIn(scissors().scale(.6).move_to([-4.3,2.55,0])),Transform(one,dim_one),Transform(two,dim_two),a.animate.set_opacity(.3),b.animate.set_opacity(.3),Transform(fill,low),FadeIn(dashed),FadeIn(label('some adaptation remains',.8,-3,28,TEXT)),run_time=.5)
        self.finish()

class S29End(EndCard):
    LINE='The feedback trims each response\nand keeps current in reserve.'
