"""Spatial spread in a passive cable.

COLOR MAP: TEAL=current/water only; YELLOW=voltage/current comparison;
GREY=membrane, axes and before-reference; TEXT=labels; BLUE (#4775EF)=K;
ORANGE=Na; GREEN=balance; PURPLE=capacitance / slow time course;
CYAN (BLUE constant)=fast time course.
All traces: exp(-x/lambda), RC steps, or exact held-end cable step solution.
One font family (Avenir Next) for labels, numbers and mathematical notation.
"""
import math
import numpy as np
from bp_style import *

KC, NAC, VC, NETC = "#4775EF", "#F29E4C", YELLOW, GREEN
PURPLE = "#B58CD9"
LESSON_NAME = "The Resting Membrane and Passive Signals"


def label(s, y=3.15, color=TEXT, size=32):
    return T(s, size, color).move_to([0,y,0])


def leader(text, pos, target, color=TEXT, size=28):
    t=T(text,size,color).move_to([*pos,0])
    end=np.array([*target,0])
    dx,dy=target[0]-pos[0],target[1]-pos[1]
    start=(t.get_right() if dx>0 else t.get_left()) if abs(dx)>abs(dy) else (t.get_top() if dy>0 else t.get_bottom())
    return VGroup(Line(start,end,color=color,stroke_width=2,buff=.10),t)


def tube(y=0,height=2.5,width=10.8,holes=True,hose=False):
    # Cutaway: two clearly separated layers of wall, open pores, rounded end caps.
    g=VGroup(RoundedRectangle(width=width,height=height,corner_radius=.3,
        color=GREY,stroke_width=5,fill_color=TEAL if hose else GREY,fill_opacity=.09).move_to([0,y,0]))
    for sign in [-1,1]:
        g.add(Line([-width/2+.3,y+sign*(height/2-.13),0],
            [width/2-.3,y+sign*(height/2-.13),0],color=GREY,stroke_width=2))
        if holes:
            for x in [-3.6,0,3.6]:
                g.add(Rectangle(width=.32,height=.35,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,y+sign*(height/2-.06),0]))
                for dx in [-.20,.20]:
                    g.add(Line([x+dx,y+sign*(height/2-.26),0],[x+dx,y+sign*(height/2+.12),0],color=GREY,stroke_width=4))
    return g


def flow(y=0,lam=5):
    return VGroup(*[Arrow([x,y,0],[x+1.65,y,0],buff=0,color=TEAL,
        stroke_width=13*np.exp(-(x+4.6)/lam),max_tip_length_to_length_ratio=.18)
        for x in [-4.6,-2.2,.2,2.6]])


def spray(height=2.5):
    return VGroup(*[Arrow([x,s*height/2,0],[x+.25,s*(height/2+.8),0],buff=0,
        color=TEAL,stroke_width=5) for x in [-3.6,0,3.6] for s in [-1,1]])


def hose():
    # A broad cutaway joins a curved outlet and a recognisable valve and spout.
    body=tube(hose=True)
    outlet=ArcBetweenPoints([5.05,0,0],[5.8,-1.85,0],angle=-PI/2,
        color=GREY,stroke_width=30)
    water=outlet.copy().set_stroke(color=TEAL,width=19)
    tap=VGroup(
        RoundedRectangle(width=.52,height=1.2,corner_radius=.12,color=GREY,
            fill_color=GREY,fill_opacity=1).move_to([-5.95,.6,0]),
        Line([-5.95,.18,0],[-5.25,.18,0],color=GREY,stroke_width=26),
        Line([-5.25,.18,0],[-5.25,-.18,0],color=GREY,stroke_width=26),
        Line([-5.95,1.2,0],[-5.95,1.55,0],color=GREY,stroke_width=7),
        Line([-6.4,1.55,0],[-5.5,1.55,0],color=GREY,stroke_width=10),
        Dot([-5.95,1.55,0],radius=.12,color=GREY))
    return VGroup(body,outlet,water,tap,
        Arrow([-5.2,-.25,0],[-4.15,-.25,0],buff=0,color=TEAL,stroke_width=10))


def drops():
    # Paired spray fans appear hole by hole, left to right.
    fans=VGroup()
    for x in [-3.6,0,3.6]:
        fan=VGroup()
        for sign in [-1,1]:
            for dx in [-.42,0,.42]:
                end=np.array([x+dx,sign*2.17,0])
                fan.add(Line([x,sign*1.32,0],end,color=TEAL,stroke_width=4),
                    Dot(end,radius=.10,color=TEAL))
        fans.add(fan)
    return fans


def stream(taper=False):
    xs=np.linspace(-4.8,4.8,70)
    widths=.48*np.exp(-(xs+4.8)/3.8) if taper else np.full_like(xs,.48)
    pts=[[x,w,0] for x,w in zip(xs,widths)]+[[x,-w,0] for x,w in zip(xs[::-1],widths[::-1])]
    return Polygon(*pts,stroke_width=0,fill_color=TEAL,fill_opacity=.75)


def subscript(base, sub, color=VC, size=30):
    main=T(base,size,color)
    small=T(sub,26,color).next_to(main,RIGHT,buff=.02).shift(DOWN*.14)
    return VGroup(main,small)


def formula():
    # Explicit 26 pt subscripts and superscript, avoiding unavailable Unicode glyphs.
    parts=[T("ΔV(x) =",30,VC),subscript("ΔV","0"),T("e",30,VC)]
    eq=VGroup(*parts).arrange(RIGHT,buff=.12,aligned_edge=UP)
    power=T("−x/λ",26,VC).next_to(eq[-1],RIGHT,buff=.02).shift(UP*.2)
    eq.add(power)
    lam=VGroup(T("λ = √(",30,VC),subscript("r","m"),T("/",30,VC),subscript("r","i"),T(")",30,VC)).arrange(RIGHT,buff=.06,aligned_edge=UP)
    top=VGroup(eq,lam).arrange(RIGHT,buff=.6).move_to([0,-2.28,0])
    rm=VGroup(subscript("r","m",GREY,26),T(": membrane resistance × length",26,GREY)).arrange(RIGHT,buff=.06)
    ri=VGroup(subscript("r","i",GREY,26),T(": core resistance / length",26,GREY)).arrange(RIGHT,buff=.06)
    defs=VGroup(rm,ri).arrange(RIGHT,buff=.45).move_to([0,-2.75,0])
    return VGroup(top,defs)


def graph(negative=False,reference=False):
    ax=Axes(x_range=[0,4,1],y_range=[-10,0,5] if negative else [0,1,.5],
        x_length=10.4,y_length=4.15 if negative or reference else 3.5,tips=False,
        axis_config={"color":GREY,"stroke_width":2,"include_ticks":False}).move_to([.15,.1 if negative else .45,0])
    labs=VGroup()
    labs.add(T("ΔV (mV)" if negative else "ΔV / ΔV₀",28,VC).rotate(PI/2).move_to([-6.25,.2,0]))
    for x,txt in [(0,"0"),(1,"0.5" if negative else ("0.5" if reference else "λ")),
                  (2,"1.0" if negative or reference else "2λ"),(4,"2.0" if negative or reference else "4λ")]:
        p=ax.c2p(x,0)
        labs.add(Line(p+UP*.07,p+DOWN*.07,color=GREY))
        # Negative plots have their horizontal zero axis above the trace.
        labs.add(T(txt,26,GREY).move_to(p+(UP*.28 if negative else DOWN*.30)))
    for v in ([-10,-5,0] if negative else [0,.5,1]):
        labs.add(T(str(v) if negative else ("0.5" if v==.5 else str(v)),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.16))
    labs.add(T("distance (mm)" if negative or reference else "distance x",27,GREY).move_to([4.3,-2.35 if negative or reference else -1.95,0]))
    return ax,labs


def decay(ax,lam=1,amp=1,color=VC):
    return ax.plot(lambda x:amp*np.exp(-x/lam),x_range=[0,4,.025],color=color,stroke_width=5)


def cable_strip():
    g=VGroup(Line([-5.05,2.55,0],[5.35,2.55,0],color=GREY,stroke_width=9),
        Dot([-5.05,2.55,0],color=TEAL,radius=.08),
        T("held source",26,TEAL).move_to([-3.7,2.9,0]))
    return g


def mark(ax,x=1,lam=1,amp=1,text=None,offset=(.8,.45),color=VC,baseline=0):
    p=ax.c2p(x,amp*np.exp(-x/lam))
    g=VGroup(DashedLine(ax.c2p(x,baseline),p,color=color,stroke_width=2),Dot(p,color=color,radius=.08))
    if text:
        t=T(text,28,color,line_spacing=1.1).move_to(p+np.array([*offset,0]))
        dx,dy=offset
        edge=(t.get_left() if dx>0 else t.get_right()) if abs(dx)>abs(dy) else (t.get_bottom() if dy>0 else t.get_top())
        g.add(Line(p,edge,color=color,buff=.12,stroke_width=2),t)
    return g


def question_marker(ax):
    return VGroup(DashedLine(ax.c2p(1,0),ax.c2p(1,1),color=VC,stroke_width=2),
        T("?",30,VC).move_to(ax.c2p(1,0)+UP*.26))


def prediction():
    ax,labs=graph()
    curve=decay(ax).set_stroke(opacity=.6)
    return VGroup(ax,labs,curve,cable_strip(),formula(),
        label("At x = λ, is the steady signal gone?",3.25,size=32),
        question_marker(ax))


def worked_marks(ax,n=3):
    specs=[(0,"−10 mV",(1,-.05)),(1,"−3.68 mV\n1λ · 37%",(.55,-.85)),
        (2,"−1.35 mV\n2λ · 14%",(.7,-.78))]
    return VGroup(*[mark(ax,x,amp=-10,text=s,offset=off) for x,s,off in specs[:n]])


def slider(y=2.65,kind="leak",value=""):
    left,right=("less leak","more leak") if kind=="leak" else ("wide core","narrow core")
    return VGroup(Line([-1.5,y,0],[3.6,y,0],color=GREY,stroke_width=5),
        Dot([-1.5,y,0],radius=.13,color=TEXT),
        T(left,26).move_to([-3.15,y,0]),T(right,26).move_to([4.8,y,0]),
        T(value,26,VC).move_to([1,y+.5,0]))


def summary_table(n=1,compact=True):
    # Keep the exact same single-line table geometry through all four scenes.
    specs=[("total leak","10 nS","20 nS"),("input R","100 MΩ","50 MΩ"),
        ("ΔV, −100 pA","−10 mV","−5 mV"),("tau","20 ms","10 ms"),
        ("cable λ","0.5 mm","0.354 mm")]
    left=-6.0
    xs=(-2.8,-.8)
    heading=T("Double the leak",32).move_to([-3.2,3.15,0])
    heads=VGroup(T("before",26,GREY).move_to([xs[0],2.35,0]),T("doubled",26,VC).move_to([xs[1],2.35,0]))
    rows=VGroup()
    for i,(name,a,b) in enumerate(specs[:n]):
        y=1.5-i*1.02
        name=T(name,26).move_to([0,y,0]).align_to([left,y,0],LEFT)
        rows.add(VGroup(name,T(a,26,GREY).move_to([xs[0],y,0]),T(b,26,VC).move_to([xs[1],y,0])))
    return VGroup(heading,heads,rows)


def panel(kind="time",cx=3.6,width=4.6,height=4.0,amp_new=-5):
    xmax=80 if kind=="time" else 1.5
    ax=Axes(x_range=[0,xmax,xmax/3],y_range=[-10,0,5],x_length=width,y_length=height,
        tips=False,axis_config={"color":GREY,"include_ticks":False,"stroke_width":2}).move_to([cx,.2,0])
    labels=VGroup(T("ΔV (mV)",26,VC).move_to([cx,2.75,0]),
        T("time (ms)" if kind=="time" else "distance (mm)",26).move_to([cx,-2.65,0]))
    for v in [-10,-5,0]:
        labels.add(T(str(v),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.13))
    for x in ([20,60] if kind=="time" else [.5,1.5]):
        labels.add(T(str(x),26,GREY).move_to(ax.c2p(x,-10)+DOWN*.3))
    old=ax.plot(lambda x:-10*(1-np.exp(-x/20)) if kind=="time" else -10*np.exp(-x/.5),
        x_range=[0,xmax,xmax/200],color=GREY,stroke_width=4)
    new=ax.plot(lambda x:amp_new*(1-np.exp(-x/10)) if kind=="time" else amp_new*np.exp(-x/(.5/math.sqrt(2))),
        x_range=[0,xmax,xmax/200],color=VC,stroke_width=5)
    return ax,labels,old,new


def panel_legend(cx=3.6):
    return VGroup(T("before",26,GREY).move_to([cx-.85,3.28,0]),T("leak doubled",26,VC).move_to([cx+1.05,3.28,0]))


class S00Title(TitleCard):
    LESSON=LESSON_NAME
    TITLE="A Nudge Fades with Distance"
    def construct(self):
        self.add(label("BIOCHEMISTRYPEDIA",2.35, TEXT,26),label(LESSON_NAME,1.55,GREY,26))
        title=VGroup(T("A Nudge Fades",49,font=TITLE_FONT),T("with Distance",49,font=TITLE_FONT)).arrange(DOWN,buff=.2).move_to([0,-.3,0])
        self.play(Write(title),run_time=1.1)
        self.add(Line([-1.2,-2,0],[1.2,-2,0],color=GOLD,stroke_width=4))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(tube(),T("?",70,GREY).move_to([4.55,0,0]))
        self.at("A small")
        self.play(FadeIn(label("How much survives the trip?",3.15,size=38)),run_time=.35)
        e=VGroup(Line([-5.3,2.65,0],[-4.55,.25,0],color=GREY,stroke_width=7),
            Arrow([-4.55,.25,0],[-3.45,.25,0],color=TEAL,buff=0,stroke_width=9))
        self.play(Create(e),FadeIn(T("electrode",28).move_to([-3.5,2.25,0])),run_time=.5)
        self.at("at one point")
        self.play(FadeIn(leader("input point",(-3.7,-2.2),(-4.55,.25),TEAL)),Flash([-4.55,.25,0],color=TEAL),run_time=.5)
        self.finish()


class S02Tube(SpokenScene):
    def construct(self):
        c=tube();self.add(c)
        self.at("A dendrite")
        self.play(Transform(c,tube(height=3.2)),run_time=.55)
        self.at("salty cytoplasm")
        self.play(FadeIn(label("salty core",0,size=36)),run_time=.4)
        self.at("wrapped in")
        self.play(FadeIn(leader("membrane",(-2.9,2.65),(-2.8,1.6))),
            FadeIn(leader("leak channel",(3.4,-2.7),(3.6,-1.6))),run_time=.5)
        self.finish()


class S03Paths(SpokenScene):
    def construct(self):
        self.add(tube())
        self.at("Current injected")
        self.play(GrowArrow(Arrow([-6.2,0,0],[-4.8,0,0],color=TEAL,buff=0,stroke_width=9)),run_time=.4)
        self.at("flow along the core")
        self.play(LaggedStart(*[GrowArrow(a) for a in flow()],lag_ratio=.13),
            FadeIn(leader("core (axial) path",(-1.6,-.65),(-1.6,0),TEAL)),run_time=.65)
        self.at("out through the membrane")
        self.play(LaggedStart(*[GrowArrow(a) for a in spray()],lag_ratio=.1),
            FadeIn(leader("membrane path",(2.9,2.8),(3.8,1.85),TEXT)),run_time=.7)
        self.finish()


class S04Hose(SpokenScene):
    def construct(self):
        c=tube();self.add(c)
        self.at("Think of a garden hose")
        self.play(Transform(c,hose()),FadeIn(label("Garden hose",3.15)),run_time=.65)
        self.at("small holes")
        self.play(FadeIn(leader("small holes",(-2.3,2.5),(0,1.25))),run_time=.4)
        self.at("every hole")
        self.play(LaggedStart(*[FadeIn(d,shift=UP*.12 if d.get_y()>0 else DOWN*.12) for d in drops()],lag_ratio=.12),run_time=.85)
        self.finish()


class S05Hose2(SpokenScene):
    def construct(self):
        water=stream();self.add(hose(),drops(),water,label("Water entering →",3.15,TEAL))
        self.at("farther along")
        self.play(Transform(water,stream(True)),run_time=.8)
        self.at("the less is left")
        self.play(FadeIn(leader("less left",(4,-2.65),(4,.08))),run_time=.4)
        self.finish()


def contest_panel(cx,wide=False):
    w=2.2
    body=VGroup(RoundedRectangle(width=w,height=4.4,corner_radius=.2,color=GREY,
        stroke_width=6,fill_color=GREY,fill_opacity=.09).move_to([cx,-.1,0]))
    # The tight wall has a continuous inner seal with only one tiny pore.
    if not wide:
        for side in [-1,1]:
            body.add(Line([cx+side*(w/2-.12),1.9,0],
                [cx+side*(w/2-.12),-2.1,0],color=GREY,stroke_width=4))
    pores=[.9,-1.1] if wide else [.1]
    for y in pores:
        body.add(Rectangle(width=.3,height=.25 if wide else .09,stroke_width=0,
            fill_color=BG,fill_opacity=1).move_to([cx+w/2-.06,y,0]))
    arrows=VGroup(*[Arrow([cx,y,0],[cx,y-.8,0],color=TEAL,buff=0,stroke_width=9) for y in [1.8,.75,-.3,-1.35]])
    leaks=VGroup(*[Arrow([cx+w/2,y,0],[cx+w/2+(.55 if wide else .23),y,0],
        buff=0,color=TEAL,stroke_width=3 if wide else 2) for y in pores])
    end=VGroup(Line([cx-.65,-2.2,0],[cx+.65,-2.2,0],color=VC,stroke_width=4),
        T("reaches far",26,VC).move_to([cx,-2.5,0]))
    return VGroup(body,arrows,leaks,T("wide core" if wide else "tight wall",30).move_to([cx,2.6,0]),end)


class S06Contest(SpokenScene):
    def construct(self):
        left=contest_panel(-3.25,True);right=contest_panel(3.25)
        self.add(left[0],right[0],label("Which path is easier?",3.35,size=32),Line([0,-2.6,0],[0,2.75,0],color=GREY,stroke_opacity=.4))
        self.at("A wide core")
        self.play(FadeIn(left[3]),LaggedStart(*[GrowArrow(a) for a in left[1]],lag_ratio=.15),Create(left[2]),FadeIn(left[4]),run_time=.75)
        self.at("A tight wall")
        self.play(FadeIn(right[3]),LaggedStart(*[GrowArrow(a) for a in right[1]],lag_ratio=.15),Create(right[2]),FadeIn(right[4]),run_time=.75)
        self.play(FadeIn(label("Both: reaches farther",-2.7,VC,30)),run_time=.4)
        self.finish()


class S07Lambda(SpokenScene):
    def construct(self):
        self.add(contest_panel(-3.25,True).set_opacity(.2),contest_panel(3.25).set_opacity(.2))
        self.at("The length constant")
        self.play(FadeIn(T("λ",116,VC).move_to([0,.5,0])),FadeIn(label("length constant",-1.15,VC,40)),run_time=.65)
        self.finish()


class S08Lambda2(SpokenScene):
    def construct(self):
        self.add(tube(y=1.25,height=1.9,width=11.6))
        hi=Rectangle(width=4,height=1.9,color=VC,fill_color=VC,fill_opacity=.12).move_to([-1,1.25,0])
        span=DoubleArrow([-3,2.65,0],[1,2.65,0],buff=0,color=VC)
        self.at("length of cable")
        self.play(FadeIn(hi),Create(span),FadeIn(T("λ",34,VC).move_to([-1,3.2,0])),run_time=.55)
        core=VGroup(Line([-3,1.25,0],[-3,-.65,0],color=GREY),
            Line([1,1.25,0],[1,-.65,0],color=GREY),
            Line([-3,-.65,0],[1,-.65,0],color=GREY,stroke_width=4),
            Rectangle(width=1.6,height=.8,color=VC,fill_color=BG,fill_opacity=1).move_to([-1,-.65,0]),
            T("core resistance",28).move_to([-1,-1.4,0]))
        mem=VGroup(
            # A bracket gathers the wall of the entire highlighted segment.
            Line([-3,.3,0],[-3,.02,0],color=GREY,stroke_width=3),
            Line([1,.3,0],[1,.02,0],color=GREY,stroke_width=3),
            Line([-3,.02,0],[3,.02,0],color=GREY,stroke_width=3),
            Line([3,.02,0],[3,-.575,0],color=GREY,stroke_width=4),
            Line([3,-1.825,0],[3,-2.1,0],color=GREY,stroke_width=4),
            Rectangle(width=.8,height=1.25,color=GREY,fill_color=BG,fill_opacity=1).move_to([3,-1.2,0]),
            T("membrane\nresistance",28,line_spacing=1.1).next_to([3.4,-1.2,0],RIGHT,buff=.2))
        self.at("core resistance")
        self.play(Create(core),run_time=.45)
        self.at("equals the resistance")
        self.play(Create(mem),FadeIn(T("=",54,VC).move_to([1.5,-1.15,0])),run_time=.6)
        self.finish()


class S09Decay(SpokenScene):
    def construct(self):
        ax,labs=graph();self.add(ax,labs,cable_strip(),label("Long, uniform cable",3.25,size=32))
        self.at("a steady signal")
        self.play(Create(decay(ax)),run_time=.7)
        self.at("falls exponentially")
        self.play(FadeIn(formula()),run_time=.45)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        self.add(prediction())
        self.at("one length constant")
        self.play(Indicate(self.mobjects[0][-1],color=VC),run_time=.65)
        self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        bar=Line([-1.1,3.25,0],[1.1,3.25,0],color=TEXT,stroke_width=8)
        pic=prediction();pic[-2].become(label("Pause · think",3.25,size=30))
        # Countdown is placed alongside the question title, never over the graph.
        bar.put_start_and_end_on([2.5,3.25,0],[5.4,3.25,0])
        self.add(pic,Line([2.5,3.25,0],[5.4,3.25,0],color=GREY,stroke_width=3),bar)
        self.play(bar.animate.put_start_and_end_on([2.5,3.25,0],[2.51,3.25,0]),run_time=5,rate_func=linear)


class S12Reveal(SpokenScene):
    def construct(self):
        ax,labs=graph();q=question_marker(ax)
        self.add(ax,labs,decay(ax),cable_strip(),formula(),q)
        self.at("about 37")
        self.play(Transform(q,mark(ax,text="37% · e⁻¹ ≈ 0.37",offset=(1.9,.52))),
            FadeIn(label("Smaller, not gone",3.25,VC,34)),run_time=.55)
        self.finish()


class S13TwoLambda(SpokenScene):
    def construct(self):
        ax,labs=graph();m=mark(ax,text="37% · e⁻¹ ≈ 0.37",offset=(1.9,.52))
        self.add(ax,labs,decay(ax),cable_strip(),formula(),m)
        self.at("Two length constants")
        self.play(Transform(m,mark(ax,2)),run_time=.5)
        self.at("about fourteen")
        self.play(Transform(m,mark(ax,2,text="14% · e⁻² ≈ 0.135",offset=(1.3,.7))),run_time=.45)
        self.at("never simply stops")
        end=ax.c2p(4,np.exp(-4))
        self.play(FadeIn(leader("still > 0",(4.45,-.6),tuple(end[:2]),VC)),
            Create(Arrow(end,end+RIGHT*.5+DOWN*.015,color=VC,buff=0,stroke_width=3)),run_time=.5)
        self.finish()


class S14Worked(SpokenScene):
    def construct(self):
        ax,labs=graph(True);m=worked_marks(ax)
        self.add(ax,labs,decay(ax,amp=-10),label("λ = 0.5 mm · held source",3.25,VC,32))
        self.at("Here is")
        self.play(FadeIn(m[0]),run_time=.4)
        self.at("Watch the steady signal")
        self.play(FadeIn(m[1]),run_time=.5)
        self.at("constant along the cable")
        self.play(FadeIn(m[2]),run_time=.5)
        self.finish()


class S15Scale(SpokenScene):
    def construct(self):
        ax,labs=graph(True)
        self.add(ax,labs,decay(ax,amp=-10),worked_marks(ax),label("λ = 0.5 mm · held source",3.25,VC,32))
        self.at("sets the scale")
        self.play(FadeIn(T("λ is a scale, not a cutoff",30,VC).move_to([1.5,-1.6,0])),run_time=.45)
        self.at("It is")
        self.play(FadeIn(leader("approaches 0; never reaches it",(2.6,-.4),(4.85,1.9),VC,26)),run_time=.5)
        self.finish()


class S16Leakier(SpokenScene):
    def construct(self):
        ax,labs=graph(reference=True)
        curve=decay(ax,lam=2);m=mark(ax,2,lam=2)
        self.add(ax,labs,decay(ax,lam=2,color=GREY).set_stroke(opacity=.65),mark(ax,2,lam=2,color=GREY).set_opacity(.5),curve,m)
        knob=slider();self.add(knob)
        self.at("A leakier membrane")
        self.play(Transform(curve,decay(ax,lam=math.sqrt(2))),Transform(m,mark(ax,math.sqrt(2),lam=math.sqrt(2))),knob[1].animate.shift(RIGHT*2.5),run_time=.75)
        self.at("a narrower core")
        self.remove(knob);knob=slider(kind="core");self.add(knob)
        self.play(Transform(curve,decay(ax,lam=1)),Transform(m,mark(ax,1,lam=1,text="37%",offset=(.65,.5))),knob[1].animate.shift(RIGHT*2.5),run_time=.75)
        self.add(label("37% point moves toward source",-2.7,VC,30))
        self.finish()


class S17Sim(SpokenScene):
    def construct(self):
        ax,labs=graph(reference=True);g=ValueTracker(1)
        knob=slider(y=2.35,value="leak ×1.0")
        self.add(RoundedRectangle(width=13.2,height=7.3,corner_radius=.2,color=GREY,stroke_width=2),
            label("Cable length constant",3.23,size=32),ax,labs,knob,
            decay(ax,lam=2,color=GREY).set_stroke(opacity=.65),mark(ax,2,lam=2,color=GREY).set_opacity(.5))
        curve=always_redraw(lambda:decay(ax,lam=2/math.sqrt(g.get_value())))
        m=always_redraw(lambda:mark(ax,2/math.sqrt(g.get_value()),lam=2/math.sqrt(g.get_value()),text="37%",offset=(.65,.5)))
        val=always_redraw(lambda:T(f"leak ×{g.get_value():.1f}",26,VC).move_to([1,2.75,0]))
        self.remove(knob[4]);knob.remove(knob[4]);self.add(curve,m,val)
        self.at("Make the membrane leakier")
        self.play(g.animate.set_value(2),knob[1].animate.shift(RIGHT*2.5),run_time=1.3)
        self.at("toward the source")
        self.play(Indicate(m,color=VC),run_time=.55)
        self.finish()


class S18Diameter(SpokenScene):
    def construct(self):
        self.add(label("Same membrane and cytoplasm",3.25,size=32))
        # Diameter is exactly fourfold, lambda exactly twofold. Common horizontal scale.
        small=tube(y=1.85,height=.55,width=10.5,holes=False)
        big=tube(y=-.65,height=2.2,width=10.5,holes=False)
        self.add(small,T("diameter d",28).move_to([-3.4,2.5,0]),
            DoubleArrow([-4.8,1.15,0],[-.8,1.15,0],color=VC,buff=0),T("λ (37% point)",28,VC).move_to([-2.8,.65,0]))
        self.at("the length constant grows")
        self.play(FadeIn(big),FadeIn(T("diameter 4d",28).move_to([-3.4,-.65,0])),
            Create(DoubleArrow([-4.8,-2.2,0],[3.2,-2.2,0],color=VC,buff=0)),run_time=.7)
        self.at("square root")
        self.play(FadeIn(label("2λ (37% point)     λ ∝ √diameter",-2.7,VC,32)),run_time=.5)
        self.finish()


def cable_step(x,t):
    if t<=0:return 1.0 if x==0 else 0.0
    r=math.sqrt(t)
    return .5*(math.exp(-x)*math.erfc(x/(2*r)-r)+math.exp(x)*math.erfc(x/(2*r)+r))


class S19Cap(SpokenScene):
    def construct(self):
        # Fixed steady cable on left; exact held-end solution at x=lambda on right.
        ax=Axes(x_range=[0,4,1],y_range=[0,1,.5],x_length=4.6,y_length=3.8,tips=False,
            axis_config={"color":GREY,"include_ticks":False}).move_to([-3.5,.3,0])
        tm=Axes(x_range=[0,160,40],y_range=[0,.42,.2],x_length=4.6,y_length=3.8,tips=False,
            axis_config={"color":GREY,"include_ticks":False}).move_to([3.5,.3,0])
        steady=ax.plot(lambda x:np.exp(-x),x_range=[0,4,.025],color=VC,stroke_width=5)
        labs=VGroup(label("Same steady shape",3.25,VC,34),
            T("distance x / λ",28).move_to([-3.5,-2.3,0]),T("time (ms)",28).move_to([3.5,-2.3,0]),
            T("ΔV / ΔV₀",26,VC).move_to([-3.5,2.65,0]),T("ΔV / ΔV₀ at x = λ",26).move_to([3.5,2.65,0]))
        for x in [0,2,4]:labs.add(T(str(x),26,GREY).next_to(ax.c2p(x,0),DOWN,buff=.15))
        for x in [0,80,160]:labs.add(T(str(x),26,GREY).next_to(tm.c2p(x,0),DOWN,buff=.15))
        for v in [0,1]:labs.add(T(str(v),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.12))
        for v,txt in [(0,"0"),(.2,"0.2"),(.37,"0.37")]:
            labs.add(T(txt,24,GREY).next_to(tm.c2p(0,v),LEFT,buff=.12))
        self.add(ax,tm,steady,labs,DashedLine(tm.c2p(0,np.exp(-1)),tm.c2p(160,np.exp(-1)),color=GREY),
            T("same level · 37%",26,VC).move_to([3.5,2.15,0]))
        self.at("It only sets")
        fast=tm.plot(lambda ms:cable_step(1,ms/10),x_range=[0,160,.8],color=BLUE,stroke_width=5)
        slow=tm.plot(lambda ms:cable_step(1,ms/20),x_range=[0,160,.8],color=PURPLE,stroke_width=5)
        self.play(Create(fast),Create(slow),FadeIn(label("C sets speed, not shape",-2.7,VC,30)),
            FadeIn(leader("τ = 10 ms",(3.9,.65),tuple(tm.c2p(8,cable_step(1,.8))[:2]),BLUE,26)),FadeIn(leader("2τ = 20 ms",(4.8,-.6),tuple(tm.c2p(55,cable_step(1,55/20))[:2]),PURPLE,26)),run_time=.85)
        self.finish()


class S20Double(SpokenScene):
    def construct(self):
        table=summary_table(1);self.add(table[0],table[1],table[2][0][:2],label("Compact cell · same capacitance and current",-2.3,GREY,28))
        self.at("double the leak")
        self.play(FadeIn(table[2][0][2]),run_time=.5)
        self.finish()


class S21DoubleRin(SpokenScene):
    def construct(self):
        table=summary_table(3);self.add(table[0],table[1],table[2][0],label("Compact cell · same capacitance and current",-2.3,GREY,28))
        self.at("input resistance halves")
        self.play(FadeIn(table[2][1]),run_time=.5)
        self.at("The same current")
        self.play(FadeIn(table[2][2]),run_time=.5)
        self.finish()


class S22DoubleTau(SpokenScene):
    def construct(self):
        table=summary_table(4,True);ax,labs,old,new=panel()
        self.add(table[0],table[1],*table[2][:3],ax,labs,old,panel_legend())
        self.at("The time constant")
        self.play(FadeIn(table[2][3]),run_time=.4)
        self.at("so the voltage")
        dots=VGroup()
        for x,a,tau,c,off in [(20,-10,20,GREY,(2.1,-.3)),(10,-5,10,VC,(1.8,.5))]:
            p=ax.c2p(x,a*(1-np.exp(-x/tau)))
            txt=T(f"{tau} ms · 63%",26,c).move_to(p+np.array([*off,0]))
            edge=txt.get_left() if off[0]>1 else txt.get_top()
            dots.add(Dot(p,color=c),DashedLine(ax.c2p(x,0),p,color=c),Line(p,edge,color=c,buff=.12,stroke_width=2),txt)
        self.play(Create(new),FadeIn(dots),run_time=.65)
        self.finish()


class S23DoubleLambda(SpokenScene):
    def construct(self):
        table=summary_table(5,True);ax,labs,old,new=panel("space",amp_new=-10)
        self.add(table[0],table[1],*table[2][:4],ax,labs,old,panel_legend())
        self.at("the length constant")
        self.play(FadeIn(table[2][4]),run_time=.4)
        self.at("Signals reach less far")
        self.play(Create(new),FadeIn(mark(ax,.5,lam=.5,amp=-10,text="37%\n0.5 mm",offset=(1.6,-.85),color=GREY,baseline=-10)),
            FadeIn(mark(ax,.5/math.sqrt(2),lam=.5/math.sqrt(2),amp=-10,text="37%\n0.354 mm",offset=(-.10,1.0),baseline=-10)),run_time=.65)
        self.finish()


class S24Rest(SpokenScene):
    def construct(self):
        ek,ena,vm=-95,60.6,-71.2
        gna=(vm-ek)/(ena-vm)
        ypos=lambda v:(v+95)/(ena+95)*4.05-1.85
        axis=Line([0,-2.05,0],[0,2.4,0],color=GREY,stroke_width=3)
        dot=Dot([0,ypos(vm),0],radius=.16,color=NETC).set_z_index(5)
        k=Line([0,ypos(ek),0],[0,ypos(vm)-.17,0],color=KC,stroke_width=12)
        na=Line([0,ypos(vm)+.17,0],[0,ypos(ena),0],color=NAC,stroke_width=12*gna)
        title=label("Does the balance point move?",3.3,size=34)
        note=label("Added leak: which reversal potential?",2.75,size=28)
        self.add(axis,k,na,dot,title,
            leader("ENa +60.6 mV",(-2.8,2.12),(0,2.2),NAC),
            leader("EK −95 mV",(-2.7,-1.85),(0,-1.85),KC),
            leader("Vm −71.2 mV",(2.7,ypos(vm)),(0,ypos(vm)),NETC))
        na_name=T("Na leak",28,NAC).move_to([1.1,.7,0])
        k_name=T("K leak",28,KC).move_to([1.1,-1.85,0])
        self.add(na_name,k_name)
        self.at("That depends")
        self.play(FadeIn(note),Indicate(na,color=NAC),run_time=.5)
        self.at("With no applied current")
        self.play(Transform(note,label("If every leak scales in proportion",2.75,size=28)),
            FadeIn(label("no applied current",-2.35,GREY,26)),run_time=.45)
        self.at("pump's own current")
        self.play(FadeIn(label("pump’s direct current omitted",-2.75,GREY,26)),run_time=.4)
        self.at("doubling every leak")
        self.play(k.animate.set_stroke(width=24),na.animate.set_stroke(width=24*gna),
            FadeIn(T("×2",28,KC).next_to(k_name,RIGHT,buff=.16)),
            FadeIn(T("×2",28,NAC).next_to(na_name,RIGHT,buff=.16)),run_time=.9)
        self.at("leaves it unchanged")
        self.play(FadeOut(title),run_time=.15)
        self.play(FadeIn(label("Same balance point",3.3,NETC,34)),run_time=.25)
        self.play(Indicate(dot,color=NETC),run_time=.4)
        self.finish()


class S25Takeaway(SpokenScene):
    def construct(self):
        ax,labs,old,new=panel("time",cx=-3.3,width=4.45,height=4.5)
        sx,sl,so,sn=panel("space",cx=3.6,width=4.45,height=4.5,amp_new=-10)
        self.add(label("More leak",3.35,size=36),
            T("compact cell",26,GREY).move_to([-3.3,3.35,0]),T("held source",26,GREY).move_to([3.6,3.35,0]),ax,labs,old,sx,sl,so,
            T("before",26,GREY).move_to([-1.4,.3,0]),T("before",26,GREY).move_to([5.0,.65,0]))
        self.at("makes a cell faster")
        p=ax.c2p(10,-5*(1-np.exp(-1)))
        self.play(Create(new),FadeIn(leader("faster",(-2.5,1.45),(p[0],p[1]),VC)),run_time=.55)
        self.at("responses are smaller")
        self.play(FadeIn(leader("smaller",(-1.3,-.75),(-1.35,-.05),VC)),run_time=.45)
        self.at("they reach less far")
        self.play(Create(sn),FadeIn(mark(sx,.5,lam=.5,amp=-10,color=GREY)),
            FadeIn(mark(sx,.5/math.sqrt(2),lam=.5/math.sqrt(2),amp=-10,text="37%",offset=(-.45,.7))),
            FadeIn(leader("more local",(4.65,-1.05),(2.43,.54),VC,30)),run_time=.55)
        self.finish()
        self.wait(.6)


class S26End(EndCard):
    LINE="More leak: faster, but smaller and reaching less far."
    def construct(self):
        line=VGroup(T("More leak: faster,",40,font=TITLE_FONT),T("but smaller and reaching less far.",40,font=TITLE_FONT)).arrange(DOWN,buff=.22)
        self.play(FadeIn(line),run_time=.6)
        self.add(label("biochemistrypedia.com",-1.8, TEXT,26))
        self.finish()
