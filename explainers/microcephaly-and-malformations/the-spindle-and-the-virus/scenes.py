"""Too Few: the Spindle and a Virus  (chapter 2 of "When Building Goes Wrong", Biochemistrypedia)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film series; taken from scenes.old.py)
  BLUE    = progenitors (radial glia) and their fibers
  YELLOW  = neurons
  RED     = what goes wrong: the virus, p53 death, "cannot show", the failure labels
  ORANGE  = spindle pole (centrosome)
  TEAL    = microtubules (the spindle fibres)
  MAGENTA = the apical patch at the ventricle (new in chapter 2)
  GOLD    = the switch from making progenitors to making neurons (unused here)
  GREY    = tissue outlines, ventricle, labels, de-emphasized
  WHITE (TEXT) = nucleus, cleavage plane, lit-up outlines
(green = the normal X and purple = doublecortin belong to chapter 3 and are not used here)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
MAGENTA = "#E27BB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def lab_right(text, color, x, y, tip, size=26):
    """text whose left edge sits at x, with an arrow from it to `tip`."""
    t = T(text, size, color)
    t.move_to([x + t.width / 2, y, 0])
    a = arr([x - 0.12, y, 0], tip, color)
    return VGroup(t, a)


def lab_left(text, color, x, y, tip, size=26):
    """text whose right edge sits at x, with an arrow from it to `tip`."""
    t = T(text, size, color)
    t.move_to([x - t.width / 2, y, 0])
    a = arr([x + 0.12, y, 0], tip, color)
    return VGroup(t, a)


def wrap(text, size, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and T(t, size).width > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    return "\n".join(lines)


def para(text, size=22, color=TEXT, max_w=3.6, weight=NORMAL):
    return T(wrap(text, size, max_w), size, color, weight=weight, line_spacing=0.8)


def chipw(text, color=BLUE, size=24, max_w=None, pad=0.2, fill=0.16):
    label = T(wrap(text, size, max_w) if max_w else text, size, color, line_spacing=0.85)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, label.move_to(box))


def dline(a, b, color=TEXT, w=3):
    return DashedLine(a, b, color=color, stroke_width=w, dash_length=0.13)


def spindle_parts(c, half, spread=1.0):
    """horizontal spindle centred on c: teal fibre arcs and two orange poles."""
    c = np.array([c[0], c[1], 0.0], dtype=float)
    pl, pr = c + LEFT * half, c + RIGHT * half
    fibs = VGroup(*[ArcBetweenPoints(pl, pr, angle=a * spread, color=TEAL, stroke_width=3)
                    for a in (-1.2, -0.6, 0, 0.6, 1.2)])
    poles = VGroup(Dot(pl, radius=0.16, color=ORANGE), Dot(pr, radius=0.16, color=ORANGE))
    return fibs, poles


def zika(x, y, r):
    body = Circle(radius=r, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.3)
    ring = VGroup(*[Dot([r * 1.2 * np.cos(a), r * 1.2 * np.sin(a), 0], radius=max(0.05, r * 0.13), color=RED)
                    for a in np.linspace(0, 2 * np.pi, 11)[:-1]])
    return VGroup(body, ring).move_to([x, y, 0])


def vdot(x, y, r=0.07):
    return Dot([x, y, 0], radius=r, color=RED)


def cross(x, y, s=0.22, color=RED, w=5):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


# All tissue and cell cartoons are schematic; plotted values are computed below.
# Timed beats are deliberately short so results settle before the next sentence.

def heading(text, color=TEXT, y=3.15, size=34):
    return T(text, size, color, weight=BOLD).move_to([0,y,0])


def slab_shape(cx,y0,w,h,color=GREY,fill=0.14):
    return RoundedRectangle(corner_radius=0.15,width=w,height=h,stroke_color=color,
        stroke_width=3,fill_color=color,fill_opacity=fill).move_to([cx,y0+h/2,0])


def bands_in(cx,y0,w,h,n=5):
    bh=(h-0.35)/n
    return VGroup(*[Rectangle(width=w-0.24,height=bh-0.05,stroke_width=0,
        fill_color=YELLOW,fill_opacity=0.65 if i%2==0 else 0.3).move_to(
        [cx,y0+0.175+bh*(i+0.5),0]) for i in range(n)])


def ghost_of(shape,n=60):
    return DashedVMobject(shape.copy().set_fill(opacity=0).set_stroke(GREY,2.5),num_dashes=n)


def wavy_shape(cx,y0,w,h,color=GREY,fill=0.14,amp=0.18,n=3):
    xs=np.linspace(cx+w/2,cx-w/2,90)
    pts=[[cx-w/2,y0,0],[cx+w/2,y0,0]]+[[x,y0+h+amp*np.sin(2*PI*n*(x-cx)/w),0] for x in xs]
    return Polygon(*pts,stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=fill)


class S00Title(TitleCard):
    LESSON="When Building Goes Wrong: Microcephaly, Zika and Lissencephaly"
    TITLE="Too Few: the Spindle and a Virus"
    def construct(self):
        brand=heading("BIOCHEMISTRYPEDIA",TEAL,2.4,28)
        title=T("Too Few: the Spindle\nand a Virus",52,TEXT,font=TITLE_FONT,line_spacing=1.1)
        rule=Line(LEFT*2,RIGHT*2,color=GOLD).shift(DOWN*1.6)
        self.add(brand,title,rule)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        q=heading("Why does spindle failure shrink the brain?",size=34)
        cell=Circle(radius=2.65,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.12).move_to([-2.3,-.35,0])
        fib,pol=spindle_parts([-2.3,-.35],1.8)
        labels=VGroup(T("spindle",30,TEAL).move_to([-2.3,-1.5,0]),
            T("pole",28,ORANGE).move_to([-4.1,.25,0]),T("pole",28,ORANGE).move_to([-.5,.25,0]))
        brain=VGroup(Ellipse(width=2.6,height=2.1,color=YELLOW,fill_opacity=.15),
            Arc(radius=.75,angle=PI,color=YELLOW),Line([0,-.8,0],[0,.8,0],color=YELLOW)).move_to([3.7,.5,0])
        self.add(q,cell,fib,pol,labels)
        self.at("shrink the brain")
        self.play(FadeIn(brain),FadeIn(T("brain",32,YELLOW).move_to([3.7,-1.1,0])),run_time=.45)
        self.at("other organs")
        self.play(FadeIn(T("more than other organs?",28,GREY).move_to([3.7,-2.1,0])),run_time=.35)
        self.finish()


class S02Mcph(SpokenScene):
    def construct(self):
        title=heading("Primary microcephaly · recessive",RED,size=36)
        normal=VGroup(slab_shape(-3.2,-2.8,4.5,5.15),bands_in(-3.2,-2.8,4.5,5.15))
        small=VGroup(slab_shape(3.2,-2.8,3.2,3.65),bands_in(3.2,-2.8,3.2,3.65))
        self.add(title,normal,small,T("normal cortex",30,GREY).move_to([-3.2,-3.35,0]))
        self.at("The brain is small")
        self.play(FadeIn(T("small, layers in order",30,YELLOW).move_to([3.2,1.55,0])),run_time=.4)
        self.at("layers")
        self.play(Indicate(small[1],color=YELLOW,scale_factor=1.03),run_time=.6)
        self.finish()


class S03Genes(SpokenScene):
    def construct(self):
        cell=Circle(radius=3.12,stroke_color=GREY,fill_color=BLUE,fill_opacity=.08).move_to([0,-.2,0])
        fib,pol=spindle_parts([0,-.2],2.1)
        a=lab_left("ASPM",ORANGE,-3.4,1.3,[-2.1,-.05,0],32)
        b=lab_right("CDK5RAP2",ORANGE,3.4,1.3,[2.1,-.05,0],30)
        c=lab_right("WDR62",ORANGE,3.4,-1.6,[2.1,-.35,0],30)
        cen=VGroup(T("centrosome",30,ORANGE).move_to([0,-1.7,0]),
            T("main microtubule-organizing center",28,ORANGE).move_to([0,-3.6,0]))
        leader=Line([-1.3,-1.4,0],[-2.1,-.55,0],color=ORANGE)
        self.add(cell,fib,pol,a,b,c,cen,leader)
        self.at("such as")
        self.play(Indicate(a,color=ORANGE),run_time=.5)
        self.at("spindle pole")
        self.play(Indicate(pol,color=ORANGE,scale_factor=1.5),run_time=.5)
        self.finish()


# Continuous radial-glia stage. Tall bodies retain the same silhouette across cuts.
SX=-2.5
BASE=-2.95

def pill(x,y,w,h):
    return slab_shape(x,y,w,h,BLUE,.22)


def patch_at(x,w=.8,y=BASE):
    return Rectangle(width=w,height=.16,stroke_width=0,fill_color=MAGENTA,fill_opacity=1).move_to([x,y,0])


def vent_stage():
    return VGroup(Line([-6.1,BASE-.15,0],[6.1,BASE-.15,0],color=GREY,stroke_width=6),
        T("ventricle / apical surface",28,GREY).move_to([3.3,-3.48,0]))


def tall_cell():
    return VGroup(pill(SX,BASE,1.8,5.8),patch_at(SX),
        Circle(radius=.35,color=TEXT,fill_opacity=.7).move_to([SX,.8,0]))


def stacked():
    # The attached daughter retains the original tall radial-glial silhouette.
    lo=VGroup(pill(SX,BASE,1.8,5.8),patch_at(SX),
        Circle(radius=.35,color=TEXT,fill_opacity=.7).move_to([SX,.8,0]))
    up=pill(-.3,-.4,1.35,2.7)
    return lo,up


def patch_closeup(split=False):
    """Magnified ventricle end, carried across the patch/split cut."""
    x=2.7; y=-2.15
    if split:
        bodies=VGroup(pill(x-.85,y,1.45,3.7),pill(x+.85,y,1.45,3.7))
        patches=VGroup(patch_at(x-.85,1.05,y),patch_at(x+.85,1.05,y))
    else:
        bodies=VGroup(pill(x,y,3.2,3.7))
        patches=VGroup(patch_at(x,2.4,y))
    return VGroup(bodies,patches)


class S04Patch(SpokenScene):
    def construct(self):
        cell=tall_cell(); close=patch_closeup()
        self.add(vent_stage(),cell,heading("Radial glial progenitor",BLUE),close,
            T("ventricle end · enlarged",28,GREY).move_to([2.7,2.25,0]),
            T("apical patch",34,MAGENTA).move_to([2.7,-2.75,0]),
            dline([SX+.9,BASE+.2,0],[1.1,-2.15,0],GREY,2))
        self.at("tall and thin")
        self.play(Indicate(cell[0],color=BLUE,scale_factor=1.02),run_time=.4)
        self.at("a small patch")
        self.play(Indicate(close[1],color=MAGENTA,scale_factor=1.15),run_time=.5)
        self.finish()


class S05Split(SpokenScene):
    def construct(self):
        cell=tall_cell(); close=patch_closeup()
        plane=dline([2.7,1.65,0],[2.7,-2.4,0])
        self.add(vent_stage(),cell,close,plane,
            heading("A cleavage plane shares the apical patch"),
            T("ventricle end · enlarged",28,GREY).move_to([2.7,2.25,0]))
        self.at("cleavage plane")
        self.play(Indicate(plane,color=TEXT,scale_factor=1.02),run_time=.4)
        dl=VGroup(pill(SX-.55,BASE,.8,5.8),patch_at(SX-.55,.4))
        dr=VGroup(pill(SX+.55,BASE,.8,5.8),patch_at(SX+.55,.4))
        self.at("affects")
        self.play(ReplacementTransform(cell,VGroup(dl,dr)),
            Transform(close,patch_closeup(True)),run_time=.55)
        self.at("patch is shared")
        self.play(FadeOut(plane),FadeIn(T("Both daughters keep a piece",30,MAGENTA)
            .move_to([2.7,-2.75,0])),run_time=.3)
        self.finish()


class S06Tilt(SpokenScene):
    def construct(self):
        cell=tall_cell(); fib,pol=spindle_parts([SX,.05],.65)
        plane=dline([SX,-1.9,0],[SX,2,0]); rot=VGroup(fib,pol,plane)
        rot.rotate(PI/3,about_point=[SX,.05,0])
        tilt_label=T("tilted spindle + plane",30,TEAL).move_to([2.8,2.1,0])
        self.add(vent_stage(),cell,rot,heading("Tilt changes patch inheritance"),tilt_label)
        self.at("Tilt the spindle")
        self.play(Indicate(pol,color=ORANGE,scale_factor=1.15),run_time=.5)
        self.wait(max(.01,3-self.elapsed()))
        lo,up=stacked()
        self.play(ReplacementTransform(cell,VGroup(lo,up)),FadeOut(rot),FadeOut(tilt_label),
            FadeIn(lab_right("all of the patch",MAGENTA,.2,-2.1,[SX+.4,BASE+.1,0],30)),run_time=.5)
        poss=VGroup(T("Possible outcomes",30,GREY,weight=BOLD),
            T("stays a progenitor?",32,BLUE),T("becomes a neuron?",32,YELLOW)).arrange(DOWN,buff=.4).move_to([3.2,.2,0])
        self.at("can change")
        self.play(FadeIn(poss),run_time=.45)
        self.finish()


class S06bBasal(SpokenScene):
    def construct(self):
        lo,up=stacked()
        note=T("The patch alone\ndoes not decide fate",34,MAGENTA,
            weight=BOLD,line_spacing=1).move_to([3.7,1.2,0])
        self.add(vent_stage(),lo,up,note)
        self.at("without the patch")
        self.play(up.animate.shift(UP*1.35+RIGHT*.35),run_time=.8)
        self.at("still divide")
        ca=pill(-.6,.95,.75,2.7); cb=pill(.65,.95,.75,2.7)
        self.play(ReplacementTransform(up,VGroup(ca,cb)),run_time=.65)
        self.at("progenitor away")
        self.play(FadeIn(T("still dividing\naway from the ventricle",30,BLUE,line_spacing=1)
            .move_to([3.5,-1.3,0])),run_time=.4)
        self.finish()


class S07Fish(SpokenScene):
    def construct(self):
        credit=heading("Fish and colleagues, 2006 · mouse embryos",GREY,y=3.45,size=30)
        cells=[]; planes=[]
        for x,label in [(-3.3,"control"),(3.3,"Aspm knocked down")]:
            c=pill(x,-2.2,3.6,4.4)
            pl=dline([x,-2.2,0],[x,2.2,0])
            cells.append(c); planes.append(pl)
            self.add(c,pl,patch_at(x,1.6,-2.2),
                T(label,30,BLUE if x<0 else RED).move_to([x,2.65,0]))
        ap=VGroup(Line([-6,-2.35,0],[6,-2.35,0],color=GREY,stroke_width=5),
            T("apical surface / ventricle",28,GREY).move_to([0,-2.75,0]))
        self.add(credit,ap,T("schematic comparison, not measured counts",26,GREY).move_to([0,-3.45,0]))
        self.at("knocking down")
        self.play(Indicate(cells[1],color=RED,scale_factor=1.02),run_time=.45)
        self.at("tilted the division")
        self.play(Rotate(planes[1],-PI/3,about_point=[3.3,0,0]),run_time=.7)
        self.at("shifted divisions")
        result=T("Fewer symmetric,\nprogenitor-making\ndivisions",30,BLUE,weight=BOLD,line_spacing=1).move_to([3.3,.1,0])
        self.play(FadeOut(planes[1]),FadeIn(result),cells[1].animate.set_fill(opacity=.08),run_time=.5)
        self.finish()


class S08P53(SpokenScene):
    def construct(self):
        cc=[-3.1,.65,0]
        cell=Circle(radius=2.1,color=BLUE,fill_opacity=.15).move_to(cc)
        fib,pol=spindle_parts(cc,1.4)
        self.add(cell,fib,pol,T("mouse progenitor",32,BLUE).move_to([-3.1,3.05,0]))
        frame=Rectangle(width=10.8,height=.45,color=GREY).move_to([0,-2.3,0])
        tick=Line([-1.5,-2.7,0],[-1.5,-1.9,0],color=TEXT)
        self.add(frame,tick,T("usual time",28,GREY).move_to([-1.5,-3.05,0]),
            T("time in mitosis · not to scale",28,GREY).move_to([0,-1.65,0]))
        bar=Rectangle(width=.05,height=.4,stroke_width=0,fill_color=BLUE,fill_opacity=.8).move_to([-5.35,-2.3,0])
        self.add(bar)
        self.at("delayed mitosis")
        longer=Rectangle(width=9.5,height=.4,stroke_width=0,fill_color=BLUE,fill_opacity=.8).move_to([-.65,-2.3,0])
        self.play(Transform(bar,longer),FadeIn(T("longer than usual",32,RED).move_to([3.2,2.3,0])),run_time=1)
        self.at("P53")
        p=chipw("p53",RED,44).move_to([3.2,.8,0])
        self.play(FadeIn(p),run_time=.35)
        self.at("a sensor")
        self.play(FadeIn(T("cell-stress sensor",30,GREY).move_to([3.2,-.2,0])),run_time=.35)
        self.wait(.35)
        self.play(FadeOut(fib),FadeOut(pol),cell.animate.set_opacity(.12),
            FadeIn(cross(*cc[:2],.7,RED,7)),run_time=.75)
        self.finish()


class S09Compound(SpokenScene):
    def construct(self):
        # The same illustrative one-in-ten model: E[P_n]/2^n = (1-.1/2)^n.
        xs=[-5.8,-4.3,-2.8,-1.3]
        ys=[[0],[-1.2,1.2],[-1.8,-.6,.6,1.8],list(np.linspace(-2.1,2.1,8))]
        tree=VGroup(*[Line([xs[k-1],ys[k-1][i//2],0],[xs[k],y,0],color=GREY)
            for k in range(1,4) for i,y in enumerate(ys[k])])
        dots=VGroup(*[Dot([xs[k],y,0],radius=.12,color=BLUE) for k in range(4) for y in ys[k]])
        self.add(tree,dots,heading("A fault in this round",RED,size=32))
        def bar(n):
            h=4.8*.95**n
            return Rectangle(width=1.4,height=h,stroke_width=0,fill_color=BLUE,fill_opacity=.7).move_to([2,-2.4+h/2,0])
        pool=bar(0); self.add(pool,ghost_of(bar(0)),T("expected pool",30,BLUE).move_to([3.7,2.8,0]),
            T("illustrative model",26,GREY).move_to([0,-3.25,0]))
        self.at("a fault recurs")
        for k in range(3):
            ring=Circle(radius=.28,color=RED,stroke_width=5).move_to([xs[k],ys[k][-1],0])
            self.play(Create(ring),Transform(pool,bar(k+1)),run_time=.22)
        self.at("round after round")
        word=T("compounds",38,TEXT,weight=BOLD).move_to([4.55,0,0])
        self.play(FadeIn(word),run_time=.2)
        self.wait(1.5)
        self.finish()


# Matched species cartoons, with normal references. Dimensions are schematic.
def species(x,kind="mouse",ratio=.9):
    normal=slab_shape(x,-2.4,3.8,3.9) if kind!="ferret" else wavy_shape(x,-2.4,3.8,3.9)
    shape=slab_shape(x,-2.4,3.8*ratio,3.9*ratio) if kind!="ferret" else wavy_shape(x,-2.4,3.8*ratio,3.9*ratio)
    return VGroup(ghost_of(normal),shape,T("normal",28,GREY).move_to([x,1.95,0]))


def ferret_question():
    fer=species(-3,"ferret",1)
    label=T("ferret, ASPM knocked out",30,RED).move_to([-3,2.8,0])
    q=VGroup(T("Less, the same, or more?",32,TEXT,weight=BOLD),
        chipw("less shrinkage",TEXT,30),chipw("the same",TEXT,30),chipw("more shrinkage",TEXT,30)).arrange(DOWN,buff=.4).move_to([3.1,.25,0])
    return VGroup(fer,label,q,T("schematic · not to scale",26,GREY).move_to([0,-3.2,0]))


class S10Pred(SpokenScene):
    def construct(self):
        tag=heading("Predict",size=36); self.add(tag)
        child=species(-3.2,"child",.52); mouse=species(3.2)
        self.at("A child")
        self.play(FadeIn(child),FadeIn(T("child, no working ASPM",30,GREY).move_to([-3.2,-3,0])),run_time=.4)
        self.at("markedly small")
        cnote=T("markedly small",32,RED).move_to([-3.2,2.6,0]); self.play(FadeIn(cnote),run_time=.3)
        self.at("but mice lacking")
        self.play(FadeIn(mouse),FadeIn(T("mouse, gene lost: mild",30,RED).move_to([3.2,-3,0])),run_time=.4)
        self.at("mild reduction")
        self.play(Indicate(mouse[1],color=RED),run_time=.4)
        self.at("Ferrets have")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.2)
        mo=species(-3.2); fer=species(3.2,"ferret",1)
        self.add(mo,fer,heading("Species comparison · not to scale",GREY,size=30),
            T("mouse, gene lost: mild",28,RED).move_to([-3.2,-3.1,0]),T("ferret cortex, folded",30,GREY).move_to([3.2,-3.1,0]))
        self.at("outer radial glia")
        dots=VGroup(*[Dot([3.2+x,-1.3,0],radius=.17,color=BLUE) for x in (-.9,0,.9)])
        lab=T("outer radial glia",30,BLUE).move_to([3.2,.7,0])
        self.play(FadeIn(dots),FadeIn(lab),run_time=.4)
        self.at("left the ventricle")
        self.play(dots.animate.shift(UP*.9),run_time=.65)
        self.at("keep dividing")
        kids=VGroup(*[Dot([3.2+x,-.65,0],radius=.12,color=BLUE) for x in (-1.1,-.7,-.2,.2,.7,1.1)])
        self.play(ReplacementTransform(dots,kids),run_time=.5)
        self.at("Knock the gene out")
        self.play(FadeOut(Group(*self.mobjects)),FadeIn(ferret_question()),run_time=.5)
        self.at("Less shrinkage")
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        self.add(ferret_question(),T("Think · compare the dividing pools",28,TEAL).move_to([0,3.4,0]))
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        fer=species(-3,"ferret",.52); mouse=species(3)
        self.add(fer,mouse,heading("Ferret: much more        Mouse: mild",RED,size=32),
            T("Johnson and colleagues, 2018 · schematic sizes",26,GREY).move_to([0,-3.2,0]))
        rg=VGroup(*[Dot([-3+x,-2,0],radius=.14,color=BLUE) for x in (-.5,0,.5)])
        self.at("radial glia")
        self.play(FadeIn(rg),run_time=.2)
        self.at("leaving the ventricle")
        self.play(rg.animate.shift(UP*1.2),FadeIn(T("displaced too early",30,BLUE).move_to([0,2.35,0])),run_time=.65)
        self.at("A second reading")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.2)
        ax=Axes(x_range=[0,15,5],y_range=[0,100,25],x_length=10.5,y_length=5.15,tips=False,
            axis_config={"stroke_color":GREY,"include_numbers":False,"tick_size":.07}).move_to([.5,-.2,0])
        xt=VGroup(*[T(str(n),28,GREY).move_to(ax.c2p(n,0)+DOWN*.35) for n in (0,5,10,15)])
        yt=VGroup(*[T(str(n),28,GREY).move_to(ax.c2p(0,n)+LEFT*.45) for n in (0,50,100)])
        title=heading("Illustrative model · still a hypothesis",RED,y=3.25,size=32)
        xl=T("rounds of division",26,GREY).move_to([.5,-3.65,0])
        yl=T("pool (% of normal)",28,GREY).rotate(PI/2).move_to([-6.1,-.2,0])
        curve=ax.plot(lambda n:100*.95**n,x_range=[0,15,.05],color=BLUE,stroke_width=5)
        labels=VGroup()
        for n in (5,10,15):
            point=ax.c2p(n,100*.95**n)
            text=T(f"{100*.95**n:.0f}%",32,BLUE,weight=BOLD).move_to(point+UP*.55+LEFT*.25)
            labels.add(Dot(point,color=BLUE,radius=.1),text,
                DashedLine(ax.c2p(n,0),point,color=BLUE,stroke_opacity=.5))
        self.add(ax,xt,yt,title,xl,yl)
        self.play(Create(curve),FadeIn(labels),run_time=.7)
        note=T("1 in 10 neurogenic rounds · not measured in mice or ferrets",26,GREY).move_to([.4,2.65,0])
        self.add(note)
        self.at("more rounds")
        self.play(Indicate(curve,color=BLUE,scale_factor=1.01),run_time=.5)
        # Hold all three percentages for >=3 seconds before the cut.
        self.wait(max(.1,3.2-(self.elapsed()-(self.t_of("A second reading")+.7))))
        self.finish()


# Compact evidence summaries. Each active study also gets an enlarged teaching panel.
COLX=[-4.35,0,4.35]
HEADS=["epidemiology","pathology","laboratory"]
SHOWS=["Shows: association in\ntime and place","Shows: virus in\na damaged brain","Shows: progenitors\nkilled or slowed"]
CANNOT=["Cannot show: cause\nor mechanism alone","Cannot show: cause\nor frequency alone","Cannot show: risk\nin a pregnancy"]
SRC=["Brazil, 2015\nFrench Polynesia","Mlakar et al., 2016","Stem-cell progenitors\nMarch 2016; organoids"]

def board_card(i,later=False):
    x=COLX[i]
    box=RoundedRectangle(width=4.08,height=5.9,corner_radius=.15,color=GREY,fill_opacity=.04).move_to([x,-.25,0])
    hd=T(HEADS[i],30,TEXT,weight=BOLD).move_to([x,2.25,0])
    src=T(SRC[i],26,GREY,line_spacing=.85).move_to([x,1.15,0])
    # Short phrases leave comfortable line spacing and an internal bottom margin.
    bs=["Shows:\ntime + place\nassociation","Shows:\nvirus in\ndamaged brain","Shows:\nprogenitors\nkilled / slowed"]
    bc=["Cannot show:\ncause / mechanism","Cannot show:\ncause / frequency","Cannot show:\npregnancy risk"]
    shows=T(bs[i],32,TEXT,line_spacing=1).move_to([x,-.8,0])
    cant=T(bc[i],29,RED,line_spacing=1).move_to([x,-2.3,0])
    src.move_to([x,1.4,0])
    if i==0:
        graphic=VGroup(arr([x-1.4,.55,0],[x+1.4,.55,0]),Dot([x-.8,.55,0],color=RED,radius=.13),
            arr([x+.8,.55,0],[x+.8,.9,0],RED),T("time",26,GREY).move_to([x,.1,0]))
    elif i==1:
        graphic=VGroup(slab_shape(x,.05,2.8,.75),Dot([x-.7,.4,0],color=RED),cross(x+.6,.4,.15))
    else:
        graphic=VGroup(Circle(radius=.4,color=GREY).move_to([x,.4,0]),Dot([x-.15,.4,0],color=BLUE),
            cross(x+.15,.5,.1),T("Ⅱ",26,BLUE).move_to([x+.1,.25,0]))
    if later and i==2:
        src=T("Epidemic strains\nagree",28,BLUE,line_spacing=1).move_to([x,1.4,0])
        graphic=T("organoids +\npregnant mice",28,TEXT,line_spacing=.9).move_to([x,.4,0])
    graphic.scale(.75).shift(UP*.2)
    return VGroup(box,hd,src,graphic,shows,cant)


def board(later=False):
    return VGroup(*[board_card(i,later) for i in range(3)])


def study_panel(i):
    # Large drawing at left, study interpretation at right; summary cards follow.
    title=heading(HEADS[i].capitalize(),size=36)
    source=T(SRC[i],29,GREY,line_spacing=.95).move_to([3.6,2,0])
    shows=T(SHOWS[i],34,TEXT,line_spacing=1).move_to([3.6,.25,0])
    cannot=T(CANNOT[i],32,RED,line_spacing=1).move_to([3.6,-2,0])
    return title,source,shows,cannot


class S13ZikaQ(SpokenScene):
    def construct(self):
        virus=zika(-3.6,0,2.2)
        q=T("How do you show a virus\ncauses a birth defect?",36,TEXT,weight=BOLD,line_spacing=1).move_to([2.5,1,0])
        caveat=T("Without testing it\nin pregnant women",32,GREY,line_spacing=1).move_to([2.5,-1.3,0])
        self.add(virus,heading("Zika virus",RED),q,caveat)
        self.at("pregnant women")
        self.play(FadeOut(Group(*self.mobjects)),FadeIn(VGroup(*[VGroup(board_card(i)[0],board_card(i)[1]) for i in range(3)])),run_time=.5)
        self.add(heading("Three kinds of evidence",size=34))
        self.finish()


class S14Epi(SpokenScene):
    def construct(self):
        title,src,shows,cannot=study_panel(0)
        axis=arr([-5.8,-.5,0],[-.6,-.5,0],GREY)
        time=T("time →",30,GREY).move_to([-3.2,-1.2,0])
        event=VGroup(Dot([-4.8,-.5,0],color=RED,radius=.23),T("virus",32,RED).move_to([-4.8,.3,0]))
        rise=VGroup(arr([-1.6,-.5,0],[-1.6,1.8,0],RED,7),T("microcephaly\nrises later",30,RED,line_spacing=.9).move_to([-2,2.4,0]))
        note=T("sequence only · not to scale",28,GREY).move_to([-3.2,-2.3,0])
        self.add(title,src,axis,time,event,note)
        self.at("Microcephaly rose")
        self.play(GrowArrow(rise[0]),FadeIn(rise[1]),run_time=.6)
        self.at("shows association")
        self.play(FadeIn(shows),run_time=.4)
        self.at("not cause")
        self.play(FadeIn(cannot),run_time=.4)
        self.finish()


class S15Path(SpokenScene):
    def construct(self):
        title,src,shows,cannot=study_panel(1)
        tissue=slab_shape(-3.3,-2.5,5.1,4.9)
        dots=VGroup(*[Dot([x,y,0],color=RED,radius=.18) for x,y in [(-4.8,1),(-3.8,-.5),(-2.2,1.4),(-1.7,-1)]])
        damage=VGroup(*[cross(x,y,.3,RED,5) for x,y in [(-4.5,-1.5),(-3,.6),(-2.8,-1.3)]])
        legend=VGroup(Dot(radius=.13,color=RED),T("virus",28,RED),cross(0,0,.12),T("damage",28,GREY)).arrange(RIGHT,buff=.15).move_to([-3.3,-3.1,0])
        self.add(title,src,tissue,legend)
        self.at("Virus was found")
        self.play(FadeIn(dots),run_time=.5)
        self.at("damaged fetal brain")
        self.play(FadeIn(damage),FadeIn(shows),run_time=.4)
        self.at("that cannot show")
        self.play(FadeIn(cannot),run_time=.4)
        self.finish()


class S16Lab(SpokenScene):
    def construct(self):
        title,src,shows,cannot=study_panel(2)
        dish=Circle(radius=2.5,color=GREY,fill_opacity=.05).move_to([-3.3,-.1,0])
        cells=VGroup(*[Circle(radius=.4,color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([x,y,0])
            for x,y in [(-4.3,.8),(-2.5,.8),(-4.3,-1),(-2.5,-1)]])
        self.add(title,src,dish,cells,T("human cortical progenitors",28,BLUE).move_to([-3.3,-3.1,0]))
        self.at("infected")
        self.play(cells.animate.set_stroke(RED,5),run_time=.5)
        self.at("killing some")
        dead=VGroup(cross(-4.3,.8,.3),cross(-2.5,-1,.3))
        self.play(cells[0].animate.set_opacity(.2),cells[3].animate.set_opacity(.2),FadeIn(dead),run_time=.5)
        self.at("slowing the rest")
        pause=VGroup(T("Ⅱ",40,BLUE).move_to([-2.5,.8,0]),T("Ⅱ",40,BLUE).move_to([-4.3,-1,0]))
        self.play(FadeIn(pause),FadeIn(shows),run_time=.4)
        self.add(T("× killed    Ⅱ slowed · schematic",26,GREY).move_to([-3.3,2.75,0]))
        self.at("A dish cannot show")
        self.play(FadeIn(cannot),run_time=.4)
        self.finish()


def skeptic_state():
    return VGroup(heading("Predict · what would a skeptic say?",size=36),
        chipw("The first study",TEXT,34).move_to([-2.8,1.75,0]),
        chipw("MR766 · old Ugandan strain",BLUE,32).move_to([-2.8,.25,0]),
        chipw("Decades in the laboratory",GREY,32).move_to([-2.8,-1.25,0]),
        board_card(2),T("Does this represent the epidemic virus?",30,TEAL).move_to([0,-3.45,0]))


class S17Pred2(SpokenScene):
    def construct(self):
        state=skeptic_state(); self.add(state[0],state[4])
        self.at("The first study")
        self.play(FadeIn(state[1]),run_time=.35)
        self.at("old Ugandan strain")
        self.play(FadeIn(state[2]),run_time=.35)
        self.at("kept for decades")
        self.play(FadeIn(state[3]),run_time=.35)
        self.at("What would a skeptic")
        self.play(FadeIn(state[5]),run_time=.35)
        self.finish()


class S18Pause(NarratedScene):
    def construct(self):
        self.add(skeptic_state(),T("Think",30,TEAL).move_to([-2.8,-2.4,0]))
        self.finish()


class S19Reveal2(SpokenScene):
    def construct(self):
        state=skeptic_state(); self.add(state)
        ans=T("It might not act like\nthe epidemic virus.",36,TEXT,weight=BOLD,line_spacing=1).move_to([-2.8,-1.5,0])
        self.play(FadeOut(state[5]),FadeOut(state[3]),FadeIn(ans),run_time=.35)
        self.at("Later work")
        self.play(FadeOut(Group(*self.mobjects)),FadeIn(board(later=True)),run_time=.4)
        self.add(heading("Later work: epidemic strains",BLUE,size=32))
        self.at("agreed")
        self.play(Indicate(self.mobjects[0][2],color=BLUE,scale_factor=1.02),run_time=.5)
        self.finish()


class S20Concl(SpokenScene):
    def construct(self):
        cards=board(later=True); self.add(cards)
        self.add(heading("Rasmussen and colleagues, 2016",GREY,size=28))
        self.at("formal criteria")
        self.play(*[c[0].animate.set_stroke(TEXT,4) for c in cards],run_time=.6)
        self.at("Zika causes microcephaly")
        banner=T("Zika causes microcephaly",36,TEXT,weight=BOLD).move_to([0,3.2,0])
        self.play(ReplacementTransform(self.mobjects[1],banner),run_time=.4)
        self.finish()


def caution_state():
    cards=VGroup(*[RoundedRectangle(width=6.05,height=6.6,corner_radius=.18,color=GREY).move_to([x,-.1,0]) for x in (-3.3,3.3)])
    h1=T("Infection in pregnancy",32,RED,weight=BOLD).move_to([-3.3,2.5,0])
    source=chipw("infection",RED,30).move_to([-3.3,1.25,0])
    # Widths encode the narrated qualitative most/some distinction, not a measured risk.
    most=VGroup(arr([-3.7,.8,0],[-4.7,-1,0],GREY,16,.36),T("most",30,GREY).move_to([-5.1,.0,0]),
        T("no\nmicrocephaly",28,TEXT,line_spacing=.9).move_to([-4.7,-1.7,0]))
    some=VGroup(arr([-2.9,.8,0],[-1.8,-1,0],RED,3,.18),T("some",28,RED).move_to([-1.7,.0,0]),
        T("microcephaly",27,RED).move_to([-1.8,-1.7,0]))
    qual=T("qualitative · not a risk estimate",26,GREY).move_to([-3.3,-2.9,0])
    h2=T("Tissue already built",32,YELLOW,weight=BOLD).move_to([3.3,2.5,0])
    neurons=VGroup(*[Dot([x,y,0],radius=.27,color=YELLOW) for x,y in [(1.7,.7),(3.3,.7),(4.9,.7),(1.7,-.7),(3.3,-.7),(4.9,-.7)]])
    lab=T("built neurons · schematic",28,YELLOW).move_to([3.3,1.6,0])
    damage=VGroup(*[cross(*neurons[k].get_center()[:2],.36) for k in (1,3,5)])
    note=T("destruction as well as\ntoo few made",30,TEXT,line_spacing=.9).move_to([3.3,-2.3,0])
    return cards,h1,source,most,some,qual,h2,neurons,lab,damage,note


class S21Caution(SpokenScene):
    def construct(self):
        c,h1,src,most,some,qual,h2,ns,lab,damage,note=caution_state()
        self.add(c,h1,h2,heading("Two cautions",y=3.55,size=30))
        self.at("Most infections")
        self.play(FadeIn(src),run_time=.4)
        self.at("do not produce")
        self.play(FadeIn(most),FadeIn(some),FadeIn(qual),run_time=.5)
        self.at("the virus also damages")
        self.play(FadeIn(ns),FadeIn(lab),run_time=.4)
        self.at("tissue already built")
        self.play(*[ns[k].animate.set_opacity(.18) for k in (1,3,5)],FadeIn(damage),FadeIn(note),run_time=.7)
        self.finish()


class S22Beat(NarratedScene):
    def construct(self):
        parts=caution_state()
        for k in (1,3,5): parts[7][k].set_opacity(.18)
        self.add(*parts,heading("Two cautions",y=3.55,size=30)); self.finish()


class S23Take(SpokenScene):
    def construct(self):
        cell=Circle(radius=1.65,color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to([0,.8,0])
        fib,pol=spindle_parts([0,.8],1.15)
        output=VGroup(arr([0,-.9,0],[0,-1.75,0],BLUE,6),
            T("Can leave too few neurons",44,YELLOW,weight=BOLD).move_to([0,-2.25,0]),
            VGroup(*[Dot([x,-3.05,0],radius=.16,color=YELLOW) for x in (-.65,0,.65)]))
        self.add(cell,fib,pol,heading("Dividing progenitor",BLUE,size=32),output)
        gene=chipw("spindle-pole\ngene",ORANGE,32).move_to([-4.8,.8,0])
        ga=arr([-3.5,.8,0],[-1.25,.8,0],ORANGE,5)
        virus=zika(4.8,.8,.85); va=arr([3.6,.8,0],[1.75,.8,0],RED,5)
        self.at("spindlepole gene")
        self.play(FadeIn(gene),GrowArrow(ga),run_time=.35)
        self.at("a virus")
        self.play(FadeIn(virus),GrowArrow(va),run_time=.35)
        self.at("the same cells")
        self.play(FadeIn(T("finds the same cells",28,RED).move_to([4.6,-.65,0])),run_time=.3)
        self.at("too few neurons")
        self.play(Indicate(output[1],color=YELLOW,scale_factor=1.03),run_time=.5)
        self.finish()


class S24End(EndCard):
    LINE="A virus that finds the same cells can leave too few neurons."
    def construct(self):
        line=T("A virus that finds the same cells\ncan leave too few neurons.",44,TEXT,font=TITLE_FONT,line_spacing=1.1)
        self.add(line,T("Zika can also destroy tissue already built",30,GREY).move_to([0,-1.8,0]),
            T("biochemistrypedia.com",28,TEAL).move_to([0,-3,0]))
        self.finish()
