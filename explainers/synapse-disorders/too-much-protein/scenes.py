"""Too Much Protein (chapter 2 of Disorders of the Synapse: Built, Then Kept).

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film; shared with the other chapters)
  GREY   = synapse, dendrite, neurons, DNA, ribosomes, axes, structure
  GREEN  = working, typical, rescued toward typical
  RED    = symptoms, traits, fragile X mice, the CGG repeat, "no FMRP"
  BLUE   = the FMRP protein (the brake on protein making)
  TEAL   = the FMR1 gene
  GOLD   = methyl tags on DNA, the year / credit highlight
  YELLOW = the question being asked, the drug
  PURPLE = messenger RNA
  PINK   = glutamate and the mGluR5 receptor
  ORANGE = newly made protein, translation blocked
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#E58FC0"
ORANGE = "#F2994A"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ribo(x, y):
    big = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([x, y, 0])
    small = Circle(radius=0.18, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([x + 0.05, y + 0.3, 0])
    return VGroup(small, big)


def wave(x0, x1, y, amp=0.16, cycles=4, color=PURPLE, w=6):
    m = VMobject(color=color, stroke_width=w)
    m.set_points_smoothly([[x, y + amp * np.sin((x - x0) / (x1 - x0) * cycles * 2 * np.pi), 0]
                           for x in np.linspace(x0, x1, 60)])
    return m


def receptor(scale=1.0, color=PINK):
    mem = RoundedRectangle(corner_radius=0.08, width=1.6, height=0.2, stroke_width=0, fill_color=color, fill_opacity=0.9)
    l = Line([-0.32, 0.1, 0], [-0.6, 0.95, 0], color=color, stroke_width=9)
    r = Line([0.32, 0.1, 0], [0.6, 0.95, 0], color=color, stroke_width=9)
    g = VGroup(mem, l, r)
    g.scale(scale)
    return g


class Plot:
    def __init__(s, x0, x1, y0, y1, t0=-20, t1=190, r0=40, r1=110):
        s.x0, s.x1, s.y0, s.y1, s.t0, s.t1, s.r0, s.r1 = x0, x1, y0, y1, t0, t1, r0, r1

    def P(s, t, r):
        return [s.x0 + (t - s.t0) / (s.t1 - s.t0) * (s.x1 - s.x0), s.y0 + (r - s.r0) / (s.r1 - s.r0) * (s.y1 - s.y0), 0]

    def axes(s):
        xa = Line([s.x0, s.y0, 0], [s.x1, s.y0, 0], color=GREY, stroke_width=4)
        ya = Line([s.x0, s.y0, 0], [s.x0, s.y1, 0], color=GREY, stroke_width=4)
        base = DashedLine(s.P(s.t0, 100), s.P(s.t1, 100), color=GREY, stroke_width=2, dash_length=0.14).set_opacity(0.6)
        return VGroup(xa, ya, base)

    def curve(s, f, ta, tb, color, n=140, dashed=False, w=7):
        pts = [s.P(t, f(t)) for t in np.linspace(ta, tb, n)]
        m = VMobject(color=color, stroke_width=w)
        m.set_points_as_corners(pts)
        if dashed:
            return DashedVMobject(m, num_dashes=60)
        return m


def f_typ(t):
    return 100.0 if t < 0 else 100 - 30 * (1 - np.exp(-t / 8))


def f_blk(t):
    return 100.0 if t < 0 else 100 - 26 * (1 - np.exp(-t / 4)) * np.exp(-t / 32)


def f_ko(t):
    return 100.0 if t < 0 else 100 - 52 * (1 - np.exp(-t / 8))


def f_kob(t):
    return 100.0 if t < 0 else 100 - 48 * (1 - np.exp(-t / 9))


def f_wait(t):  # typical, drawn for the "waits for protein" panel: early shallow dip, then the stay-down drop
    if t < 0:
        return 100.0
    return 100 - 14 * (1 - np.exp(-t / 5)) - 16 / (1 + np.exp(-(t - 55) / 6))


BIG = Plot(-5.6, 5.8, -3.0, 2.7)


def big_axes():
    ax = BIG.axes()
    ticks = VGroup()
    for k in (1, 2, 3):
        ticks.add(T(f"{k} h", 26, GREY).move_to(BIG.P(60 * k, 40)[:2] + [0]).shift(DOWN * 0.35))
    yl = T("response (% baseline)", 26, GREY).rotate(PI / 2).move_to([-6.3, -0.1, 0])
    baseline = T("100", 26, GREY).move_to([-5.95, BIG.P(0,100)[1], 0])
    schematic = T("schematic", 26, GREY).move_to([0, -3.65, 0])
    return VGroup(ax, ticks, yl, baseline, schematic)


def dots_in(cx, cy, w, h, n, seed=3, r=0.1):
    rng = np.random.RandomState(seed)
    return VGroup(*[Dot([cx + rng.uniform(-w / 2, w / 2), cy + rng.uniform(-h / 2, h / 2), 0], radius=r, color=ORANGE)
                    for _ in range(n)])


def bar_rect(x0, w, y, color, h=0.5):
    r = Rectangle(width=max(w, 0.05), height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.4)
    return r.move_to([x0, y, 0], aligned_edge=LEFT)


def typ_marker(x, y, h=0.8):
    return Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=GREEN, stroke_width=6)



# Actual post-wait cue times, rather than the pipeline's pre-wait diagnostic.
class TimedSpeech(SpokenScene):
    def at(self, phrase, lead=0.12, nth=0):
        target = self.t_of(phrase, nth)
        rest = target - lead - self.elapsed()
        if rest > 0:
            self.wait(rest)
        with open(Path(os.environ["KX_SCRIPT"]).parent / "sync.log", "a") as log:
            log.write(f"{os.environ['KX_SCENE_ID']} {phrase!r} target={target:.3f} actual={self.elapsed():.3f} delta={self.elapsed()-target:+.3f}\n")


def label(text, x, y, color=TEXT, size=30):
    return T(text, size, color).move_to([x,y,0])


def close_synapse():
    dend = RoundedRectangle(width=12.2, height=3.5, corner_radius=.45, color=GREY,
                            fill_color=GREY, fill_opacity=.09).move_to([0,-1.6,0])
    head = Ellipse(width=5.5,height=2.1,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([0,1.2,0])
    neck = Rectangle(width=1.1,height=.75,stroke_width=0,fill_color=GREY,fill_opacity=.25).move_to([0,.25,0])
    pre = Ellipse(width=5.7,height=.8,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([0,2.95,0])
    labs = VGroup(label("axon ending",-4.5,2.95,GREY),label("spine",4,1.2,GREY),
                  label("dendrite",-4.65,-2.85,GREY))
    rb=VGroup(*[ribo(x,-1.85).scale(1.85) for x in (-2,0,2)])
    labs.add(label("ribosomes",.3,-2.95,GREY))
    # The brake lies inside the dendrite, below and clear of the spine stalk.
    br=RoundedRectangle(width=5.7,height=.4,corner_radius=.1,color=BLUE,fill_color=BLUE,fill_opacity=1).move_to([.4,-.7,0])
    fm=bchip("FMRP brake",BLUE,30).move_to([-4.1,-.7,0])
    return VGroup(dend,neck,head,pre,labs),rb,br,fm


def protein_burst(scene):
    dots=VGroup(*[Dot([x,-1.6,0],radius=.13,color=ORANGE) for x in (-2,0,2)])
    scene.add(dots)
    scene.play(*[d.animate.move_to([x,-2.45,0]) for d,x in zip(dots,(-1.1,1.1,2.9))],run_time=.55)
    return dots


class S00Title(TitleCard):
    LESSON="Disorders of the Synapse: Built, Then Kept"
    TITLE="Too Much Protein"

class S01Q(TimedSpeech):
    def construct(self):
        syn,rb,br,fm=close_synapse()
        self.add(syn,rb,label("Too Much Protein",0,3.65,GOLD,34))
        self.at("when the")
        q=label("?",.4,-.7,YELLOW,40)
        self.play(FadeIn(br),FadeIn(fm),FadeIn(q),run_time=.35)
        self.at("is gone")
        self.play(br.animate.set_opacity(.12),fm.animate.set_opacity(.3),q.animate.set_opacity(.3),run_time=.35)
        protein_burst(self)
        self.finish()

class S02Fx(TimedSpeech):
    def construct(self):
        # One opaque union outline, split across an actual narrow band near the tip.
        pts=[(-.3,.25),(-1.65,2.8),(-1.05,3.1),(0,.85),(1.05,3.1),(1.65,2.8),(.3,.25),
             (1.95,-2.8),(1.35,-3.1),(0,-.75),(-1.35,-3.1),(-1.95,-2.8)]
        x=Polygon(*[[a-3.5,b,0] for a,b in pts],color=GREY,fill_color=GREY,fill_opacity=1)
        gap=Line([-2.18,-2.12,0],[-1.67,-2.4,0],color=BG,stroke_width=24)
        self.add(x,gap,label("fragile X syndrome",2.7,2.55,TEXT,40))
        gaplab=label("gap near the tip",2.5,-2.4,RED,32)
        leader=arr([.4,-2.4,0],[-1.9,-2.25,0],RED)
        self.play(FadeIn(gaplab),GrowArrow(leader),run_time=.5)
        self.at("most common")
        self.play(FadeIn(label("most common\ninherited cause of",2.7,.95,GREY,32)),run_time=.4)
        self.at("intellectual disability")
        self.play(FadeIn(bchip("intellectual disability",RED,30).move_to([2.7,-.65,0])),run_time=.35)
        self.finish()


def gene():
    strip=RoundedRectangle(width=12,height=3,corner_radius=.2,color=TEAL,fill_color=TEAL,fill_opacity=.12).move_to([0,-.5,0])
    chips=VGroup(*[bchip("CGG",RED,48,pad=.32).move_to([-4.75+i*2.375,-.5,0]) for i in range(5)])
    return strip,chips

class S03Cgg(TimedSpeech):
    def construct(self):
        strip,chips=gene()
        self.add(strip,label("FMR1 gene",0,-2.65,TEAL,46))
        self.at("repeat")
        self.play(FadeIn(label("a 3-base repeat",0,2.5,RED,44)),run_time=.4)
        self.at("CGG")
        self.play(LaggedStart(*[FadeIn(c) for c in chips],lag_ratio=.12),run_time=.65)
        self.at("start of the")
        self.play(Create(Brace(chips,UP,color=RED)),run_time=.4)
        self.finish()

class S04Count(TimedSpeech):
    def construct(self):
        title=label("CGG copies",0,3.05,RED,40)
        bands=VGroup()
        for x,w,txt,col in [(-4.5,3,"below 45",GREY),(-1.8,2,"45–54",GREY),(1,3.4,"55–200\npremutation",GOLD),(4.6,2.5,"above ~200",RED)]:
            b=Rectangle(width=w,height=1.3,color=col,fill_color=col,fill_opacity=.15).move_to([x,.8,0])
            bands.add(b,label(txt,x,.8,col,28))
        cnt=ValueTracker(0)
        num=always_redraw(lambda:label(str(int(cnt.get_value())),0,2.1,RED,48))
        control=bchip("FMR1 control region",TEAL,36).move_to([0,-1.2,0])
        self.add(title,bands,num,control)
        self.play(cnt.animate.set_value(45),run_time=.25,rate_func=linear)
        self.play(cnt.animate.set_value(55),run_time=.2,rate_func=linear)
        self.play(cnt.animate.set_value(200),run_time=.35,rate_func=linear)
        self.play(cnt.animate.set_value(236),run_time=.35,rate_func=linear)
        self.at("gene is usually")
        self.play(Transform(control,bchip("FMR1 control region",GREY,36).move_to([0,-1.2,0])),FadeIn(label("methylated",0,-2.1,GREY,32)),
                  FadeIn(label("FMR1 gene: usually silenced",0,-3,GREY,38)),run_time=.35)
        self.finish()

class S05Fmrp(TimedSpeech):
    def construct(self):
        missing=label("FMRP: little or none",0,2.9,BLUE,46)
        band=RoundedRectangle(width=12,height=5.3,corner_radius=.4,color=GREY).move_to([0,-.4,0])
        mr=wave(-5.5,-.1,.5,amp=.22)
        fm=bchip("FMRP",BLUE,36).move_to([.5,1.65,0])
        clamp=Line([.5,1.1,0],[.5,-.9,0],color=BLUE,stroke_width=14)
        rb=VGroup(*[ribo(x,.15).scale(1.8) for x in (1.5,3.7)])
        self.add(missing,band,mr,rb,label("mRNA",-3.5,1.4,PURPLE),label("ribosomes",2.8,-1.5,GREY))
        self.at("It binds")
        self.play(FadeOut(missing),FadeIn(fm),run_time=.35)
        self.at("holds back")
        self.play(Create(clamp),run_time=.25)
        self.at("translation")
        self.play(FadeIn(label("translation held back • idle ribosomes",0,-2.55,BLUE,34)),run_time=.25)
        self.finish()


def stopwatch(c):
    return VGroup(Circle(radius=.65,color=GREY).move_to(c),Line(c,c+UP*.5,color=TEXT,stroke_width=6))

class S06Local(TimedSpeech):
    def construct(self):
        syn,rb,br,fm=close_synapse()
        self.add(syn)
        self.at("their own ribosomes")
        self.play(FadeIn(rb),run_time=.4)
        self.at("synapses can")
        signal=arr([0,2,0],[0,1.25,0],PINK)
        self.play(GrowArrow(signal),run_time=.35)
        self.at("make protein")
        protein_burst(self)
        self.at("within minutes")
        sw=stopwatch(np.array([4.6,-1.65,0]))
        self.add(sw,label("minutes",4.6,-2.65,TEXT,28))
        self.play(Rotate(sw[1],angle=-1.7*PI,about_point=sw[0].get_center()),run_time=1,rate_func=linear)
        self.at("FMRP is a")
        self.play(FadeIn(br),FadeIn(fm),run_time=.4)
        self.finish()

class S07Mglur(TimedSpeech):
    def construct(self):
        syn,rb,br,fm=close_synapse()
        self.add(syn,rb,br,fm)
        self.at("releases the")
        self.play(Indicate(br,scale_factor=1.04),run_time=.4)
        self.at("glutamate")
        gd=VGroup(*[Dot([x,2.4,0],radius=.13,color=PINK) for x in (-.4,0,.4)])
        gl=label("glutamate",4.1,2.15,PINK)
        line=Line([2.8,2.15,0],[.7,2.4,0],color=PINK)
        self.play(FadeIn(gd),FadeIn(gl),Create(line),run_time=.25)
        self.at("receptor")
        rc=receptor(1.65).move_to([0,1.35,0])
        self.play(FadeIn(rc),gd.animate.shift(DOWN*.25),run_time=.4)
        self.at("glue")
        self.play(FadeIn(label("mGluR5",-3.6,.6,PINK,34)),br.animate.set_opacity(0),fm.animate.set_opacity(.25),run_time=.4)
        protein_burst(self)
        self.finish()

class S08Ltd(TimedSpeech):
    def construct(self):
        self.add(big_axes(),BIG.curve(f_typ,-20,0,GREEN))
        self.at("slices")
        self.play(FadeIn(label("hippocampal slices",3.9,3.2,GREY,28)),run_time=.3)
        self.at("activating that")
        self.play(Create(DashedLine(BIG.P(0,40),BIG.P(0,108),color=PINK)),
                  FadeIn(label("receptor activated",-2.5,3.2,PINK,28)),run_time=.4)
        self.at("makes synapses")
        self.play(Create(BIG.curve(f_typ,0,40,GREEN)),run_time=.9)
        self.at("for hours")
        self.play(Create(BIG.curve(f_typ,40,190,GREEN)),run_time=1.1)
        self.at("This long")
        self.play(FadeIn(label("long-term depression",2.5,-.15,GREEN,32)),run_time=.4)
        self.at("normally needs")
        self.play(Create(BIG.curve(f_blk,0,190,ORANGE,dashed=True)),
                  FadeIn(label("new protein blocked",3.3,1.25,ORANGE,28)),run_time=1.3)
        self.finish()


def predict_parts():
    return (big_axes(),BIG.curve(f_typ,-20,190,GREEN).set_stroke(opacity=.5),
            label("Predict.",2.2,3.15,YELLOW,56),bchip("no FMRP",RED,30).move_to([-3,3.15,0]),
            bchip("knockout trace: ?",YELLOW,42).move_to([.9,-2,0]),
            bchip("needs new protein?",YELLOW,36).move_to([2.3,1,0]))

class S09Pred(TimedSpeech):
    def construct(self):
        ax,typ,pred,no,unk,nq=predict_parts()
        self.add(ax,typ,pred)
        self.at("Take the")
        self.play(FadeIn(no),run_time=.4)
        self.at("What happens")
        self.play(FadeIn(unk),run_time=.4)
        self.at("And does it")
        self.play(FadeIn(nq),run_time=.4)
        self.finish()

class S10Pause(NarratedScene):
    def construct(self):
        self.add(*predict_parts())
        self.finish()

class S11Rev(TimedSpeech):
    def construct(self):
        self.add(big_axes(),BIG.curve(f_typ,-20,190,GREEN).set_stroke(opacity=.65),label("typical",4.8,.05,GREEN,30))
        self.at("In fragile")
        self.play(FadeIn(bchip("fragile X mice",RED,30).move_to([-3,3.15,0])),run_time=.35)
        self.at("weakening is")
        self.play(Create(BIG.curve(f_ko,-20,190,RED)),run_time=.6)
        self.at("exaggerated")
        self.play(FadeIn(label("exaggerated",3.8,-2.65,RED,32)),run_time=.35)
        self.at("no longer needs")
        self.play(Create(BIG.curve(f_kob,-20,190,ORANGE,dashed=True,w=9)),
                  FadeIn(label("new protein blocked: still drops",1.6,1.2,ORANGE,30)),run_time=.8)
        self.finish()


def mini(cx,title,col):
    frame=RoundedRectangle(width=6.05,height=7.25,corner_radius=.2,color=GREY).move_to([cx,0,0])
    pl=Plot(cx-1.95,cx+2.55,-2.65,.45)
    response=label("response",cx-2.5,-1.1,GREY,26).rotate(PI/2)
    labs=VGroup(label(title,cx,3.1,col,38),response,
                label("time →",cx+.4,-3.08,GREY,26),label("schematic",cx+.65,-3.43,GREY,26))
    box=RoundedRectangle(width=4.8,height=1,corner_radius=.15,color=GREY).move_to([cx,1.85,0])
    return pl,VGroup(frame,pl.axes(),labs,box)

class S12Why(TimedSpeech):
    def construct(self):
        a,ga=mini(-3.15,"typical",GREEN)
        b,gb=mini(3.15,"no FMRP",RED)
        self.add(ga)
        self.at("weakening waits")
        self.play(Create(a.curve(f_wait,-20,40,GREEN)),run_time=.5)
        self.at("new protein")
        burst=dots_in(-3.15,1.85,4.2,.65,12,r=.12)
        self.play(LaggedStart(*[FadeIn(d,shift=UP*.35) for d in burst],lag_ratio=.03),run_time=.35)
        self.play(FadeIn(label("new protein → sustained drop",-3.15,.94,ORANGE,26)),run_time=.2)
        self.play(Create(a.curve(f_wait,40,190,GREEN)),run_time=1.0)
        self.at("Without the")
        self.play(FadeIn(gb),run_time=.35)
        self.at("usual reading")
        self.play(FadeIn(label("the usual reading",3.15,.94,YELLOW,26)),run_time=.3)
        self.at("protein is already")
        pile=dots_in(3.15,1.85,4.2,.65,32,r=.12)
        self.play(FadeIn(pile),run_time=.3)
        self.play(Create(b.curve(f_ko,-20,190,RED)),run_time=.7)
        self.finish()

class S13Theory(TimedSpeech):
    def construct(self):
        self.add(label("2004",0,2.4,GOLD,100))
        self.at("Huber")
        self.play(FadeIn(label("Bear, Huber and Warren",0,.65,TEXT,46)),run_time=.35)
        self.at("proposed the")
        self.play(FadeIn(bchip("the mGluR theory",PINK,58).move_to([0,-1.7,0])),run_time=.35)
        self.finish()

class S14Theory2(TimedSpeech):
    def construct(self):
        self.add(label("the mGluR theory",0,3.1,PINK,42),bchip("FMRP missing",BLUE,32).move_to([-4.25,1.8,0]))
        self.at("the receptor")
        rc=receptor(1.8).move_to([-4.25,-.3,0])
        self.play(FadeIn(rc),FadeIn(label("mGluR5",-4.25,-2,PINK,34)),run_time=.3)
        self.at("drives")
        a=DashedVMobject(arr([-2.7,-.3,0],[-1.7,-.3,0],PINK),num_dashes=8)
        self.play(FadeIn(a),run_time=.25)
        self.at("too much")
        pile=dots_in(0,-.2,2.4,3.6,40,r=.14)
        self.play(FadeIn(pile),FadeIn(label("excess protein",0,-2.7,ORANGE,30)),run_time=.6)
        self.at("many features")
        a2=DashedVMobject(arr([1.6,-.3,0],[2.7,-.3,0],ORANGE),num_dashes=8)
        traits=VGroup(*[bchip(t,RED,27).move_to([4.5,y,0]) for t,y in [("protein synthesis",1.3),("spine density",-.25),("seizures",-1.8)]])
        self.play(FadeIn(a2),FadeIn(traits),run_time=.45)
        self.finish()


def cross_row(y=0):
    left=bchip("fragile X\nmouse",RED,40)
    right=bchip("one working\nreceptor gene",PINK,40)
    return VGroup(left,label("×",0,0,TEXT,80),right).arrange(RIGHT,buff=.65).move_to([0,y,0])


def predict15_parts():
    return VGroup(label("Predict.",0,3.05,YELLOW,56),label("If excess signalling causes the traits…",0,1.65,TEXT,36),
                  cross_row(-.3),label("What should halving the receptor do?",0,-2.6,YELLOW,38))

class S15Pred(TimedSpeech):
    def construct(self):
        g=predict15_parts()
        self.add(g[0])
        self.at("too much")
        self.play(FadeIn(g[1]),run_time=.4)
        self.at("causes the")
        self.play(FadeIn(g[2]),run_time=.4)
        self.at("what should")
        self.play(FadeIn(g[3]),run_time=.4)
        self.finish()

class S16Pause(NarratedScene):
    def construct(self):
        self.add(predict15_parts())
        self.finish()

class S17Rev(TimedSpeech):
    def construct(self):
        cr=VGroup(bchip("fragile X\nmouse",RED,56,pad=.5),
                  label("×",0,0,TEXT,112),
                  bchip("one working\nreceptor gene",PINK,56,pad=.5)).arrange(RIGHT,buff=.55)
        fit(cr,max_w=12.4)
        cr.move_to(ORIGIN)
        self.add(cr,label("Dölen and Bear, 2007",0,3,GOLD,46))
        self.at("fragile")
        self.play(Indicate(cr[0],color=RED,scale_factor=1.02),run_time=.35)
        self.at("one working")
        self.play(Indicate(cr[2],color=PINK,scale_factor=1.02),run_time=.35)
        self.at("receptor gene")
        self.play(Indicate(cr[2],color=PINK,scale_factor=1.02),run_time=.55)
        self.finish()


def rescue_rows():
    rows=[]
    for i,(name,y,end) in enumerate(zip(["protein synthesis","spine density","sound-triggered seizures"],[1,-.85,-2.7],[.48,.62,.54])):
        title=label(name,-3.6,y+.65,TEXT,28)
        old=bar_rect(-5.6,10.8*.87,y+.15,RED,h=.22)
        new=bar_rect(-5.6,10.8*.87,y-.2,GREEN,h=.22)
        after=bar_rect(-5.6,10.8*end,y-.2,GREEN,h=.22)
        tick=typ_marker(-5.6+10.8*.45,y,h=.75)
        rows.append((VGroup(title,old,new,tick),new,after))
    return rows

class S18Rev2(TimedSpeech):
    def construct(self):
        red_key=VGroup(Line(LEFT*.3,RIGHT*.3,color=RED,stroke_width=7),
                       T("fragile X mouse",28,RED)).arrange(RIGHT,buff=.2)
        green_key=VGroup(Line(LEFT*.3,RIGHT*.3,color=GREEN,stroke_width=7),
                         T("fragile X with half the receptor gene",28,GREEN)).arrange(RIGHT,buff=.2)
        key=VGroup(red_key,green_key).arrange(DOWN,aligned_edge=LEFT,buff=.22).to_corner(UL,buff=.5)
        self.add(key,label("schematic",4.5,3.4,GREY,26),
                 label("typical = green tick",4.3,2.8,GREEN,26))
        rows=rescue_rows()
        for phrase,row in zip(["Protein synthesis","spine density","sound"],rows):
            self.at(phrase)
            self.play(FadeIn(row[0]),run_time=.35)
        self.at("move toward")
        self.play(*[Transform(r[1],r[2]) for r in rows],run_time=.8)
        self.finish()

class S19Bystander(TimedSpeech):
    def construct(self):
        header=label("FMR1 gene  ↔  receptor gene",0,2.95,YELLOW,40)
        self.add(header)
        self.at("interact")
        self.play(FadeIn(label("two genes interact",0,2.05,TEXT,34)),run_time=.35)
        self.at("It may be")
        readings=VGroup()
        for x,heading in [(-3.3,"possible: part of the cause"),(3.3,"possible: offsets the defect")]:
            readings.add(label(heading,x,1.15,TEXT,28),bchip("no FMRP",RED,32).move_to([x,.15,0]),
                         bchip("traits",RED,32).move_to([x,-2.65,0]))
        readings.add(bchip("receptor",PINK,32).move_to([-3.3,-1.2,0]),
                     DashedLine([-3.3,-.3,0],[-3.3,-.75,0],color=GREY),
                     DashedLine([-3.3,-1.65,0],[-3.3,-2.2,0],color=GREY),
                     arr([3.3,-.3,0],[3.3,-2.2,0],RED),
                     bchip("receptor",PINK,28).move_to([5.1,-1.2,0]),
                     arr([4.1,-1.2,0],[3.4,-1.2,0],GREEN))
        self.play(FadeIn(readings),run_time=.5)
        self.finish()


def panel20():
    frame=RoundedRectangle(width=12.4,height=6.8,corner_radius=.25,color=TEAL)
    title=label("adult drug: turns down mGluR5 signalling",0,2.9,TEXT,32)
    mice=bchip("adult fragile X mice",RED,30).move_to([-3.65,1.1,0])
    pill=bchip("receptor blocker",YELLOW,30).move_to([-3.65,-.15,0])
    rec=bchip("mGluR5",PINK,30).move_to([-3.65,-1.4,0])
    arrow=arr([-3.65,-.6,0],[-3.65,-.95,0],YELLOW)
    foot=label("tests whether the circuit can still be adjusted",0,-2.6,YELLOW,28)
    credit=label("Michalon and colleagues, 2012",0,-3.1,GREY,26)
    return frame,title,mice,pill,rec,arrow,foot,credit


def panel_bars():
    rows=[]
    for y,end in zip([1.15,0,-1.15],[.48,.54,.43]):
        a=bar_rect(.3,5.2*.9,y,RED,h=.35)
        b=bar_rect(.3,5.2*end,y,GREEN,h=.35)
        tick=typ_marker(.3+5.2*.45,y,h=.7)
        rows.append((a,b,tick))
    return rows

class S20Late(TimedSpeech):
    def construct(self):
        frame,title,mice,pill,rec,a,foot,credit=panel20()
        rows=panel_bars()
        self.add(frame,title,foot,credit,label("many traits • schematic",2.7,2,GREY,28),
                 label("typical = green ticks",2.7,-1.95,GREEN,26),*[r[2] for r in rows])
        generic=bchip("drug",YELLOW,30).move_to(pill)
        self.at("with a drug")
        self.play(FadeIn(generic),run_time=.35)
        self.at("In adult")
        self.play(FadeIn(mice),run_time=.4)
        self.at("chronic treatment")
        self.play(FadeIn(rec),*[FadeIn(r[0]) for r in rows],run_time=.4)
        self.at("receptor blocker")
        self.play(Transform(generic,pill),GrowArrow(a),run_time=.4)
        self.at("corrected many")
        self.play(*[Transform(r[0],r[1]) for r in rows],run_time=.8)
        self.finish()

class S21Late2(TimedSpeech):
    def construct(self):
        parts=panel20()
        self.add(*parts,label("many traits • schematic",2.7,2,GREY,28),
                 label("typical = green ticks",2.7,-1.95,GREEN,26))
        rows=panel_bars()
        self.add(*[r[1] for r in rows],*[r[2] for r in rows])
        self.at("circuit could")
        self.play(*[Circumscribe(r[1],color=GREEN) for r in rows],run_time=.6)
        self.at("does not put")
        self.play(FadeOut(parts[6]),FadeIn(label("FMRP still missing",0,-2.6,BLUE,32)),run_time=.35)
        self.finish()


def card(name,sub,x):
    box=RoundedRectangle(width=3.9,height=5.5,corner_radius=.2,color=GREY,fill_color=GREY,fill_opacity=.05).move_to([x,.3,0])
    headers=VGroup(box,label(name,x,2.55,YELLOW,27),label(sub,x,1.65,TEXT,28),
                   label("main outcome\nmeasure\n(schematic)",x,.55,GREY,26),
                   label("drug",x-.85,-1.95,YELLOW,26),label("placebo",x+.85,-1.95,GREY,26))
    # Schematic intervals overlap; no numerical or exact-equality claim.
    bars=VGroup()
    for dx,y,col,txt in [(-.85,-.95,YELLOW,"drug"),(.85,-.78,GREY,"placebo")]:
        bars.add(Line([x+dx,y-.5,0],[x+dx,y+.5,0],color=col,stroke_width=4),
                 Line([x+dx-.22,y-.5,0],[x+dx+.22,y-.5,0],color=col),
                 Line([x+dx-.22,y+.5,0],[x+dx+.22,y+.5,0],color=col),
                 Dot([x+dx,y,0],radius=.1,color=col))
    return headers,bars

class S22People(TimedSpeech):
    def construct(self):
        intro=VGroup(receptor(2).move_to([0,0,0]),bchip("drug",YELLOW,36).move_to([0,2,0]))
        self.add(intro)
        self.at("being tested")
        people=label("tested in people",0,-2,TEXT,44)
        self.play(FadeIn(people),run_time=.35)
        self.at("Trials in")
        a,ab=card("mavoglurant, 2016","adolescents\nand adults",-2.3)
        b,bb=card("basimglurant, 2018","adolescents\nand adults",2.3)
        self.play(FadeOut(intro),FadeOut(people),FadeIn(a),FadeIn(b),run_time=.45)
        self.at("no benefit")
        self.play(FadeIn(ab),FadeIn(bb),FadeIn(label("no benefit over placebo on the main measures",0,-3.1,RED,30)),run_time=.4)
        self.finish()

class S23Kids(TimedSpeech):
    def construct(self):
        a,ab=card("mavoglurant, 2016","adolescents\nand adults",-4.1)
        b,bb=card("basimglurant, 2018","adolescents\nand adults",0)
        self.add(a,ab,b,bb)
        self.at("later trial")
        c,cb=card("young children","a later trial",4.1)
        self.play(FadeIn(c),run_time=.35)
        self.at("no benefit")
        self.play(FadeIn(cb),FadeIn(label("young children: no benefit over placebo",0,-3.1,RED,30)),run_time=.4)
        self.finish()

class S24Take(TimedSpeech):
    def construct(self):
        self.add(label("Takeaway",0,2.8,GOLD,42))
        self.at("mouse rescue")
        pair=VGroup(bchip("mouse rescue: yes",GREEN,46).move_to([0,.9,0]),
                    bchip("human trials so far:\nno benefit over placebo",RED,38).move_to([0,-1.2,0]))
        self.play(FadeIn(pair),run_time=.4)
        self.finish()

class S25End(EndCard):
    LINE="A mouse rescue tests a mechanism, not a cure."
