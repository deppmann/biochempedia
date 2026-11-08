"""Myelination, chapter 1: Why Wrap, and How Much  (Biochemistrypedia chaptered explainer)

COLOR MAP (one color per concept, shared by every chapter)
  BLUE   = the axon
  PURPLE = myelin / the glial membrane wrapped around the axon (and the glial cell)
  YELLOW = the action potential and the current that carries it
  RED    = current leaking out across the membrane
  GREEN  = nodes of Ranvier and their sodium channels
  GREY   = labels, outlines, axes
  TEXT   = ordinary words and numbers
  CHARGE = membrane charge (pink)
  BAND   = observed g-ratio range (slate)
  GOLD   = editorial card accents
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CHARGE = "#EDA4CD"
BAND = "#B1BAC9"
AX_X0, AX_X1 = -6.1, 6.1
NODE_X = [-3.75, -1.25, 1.25, 3.75]


# ------------------------------------------------------------------ helpers
def axon_bar(x0=AX_X0, x1=AX_X1, y=0.0, h=1.4, op=0.22):
    r = Rectangle(width=x1 - x0, height=h, stroke_color=BLUE, stroke_width=3.5,
                  fill_color=BLUE, fill_opacity=op)
    return r.move_to([(x0 + x1) / 2, y, 0])


def leak(x, y0, y1, color=RED, w=5):
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.5)


def harrow(x0, x1, y=0.0, w=7, color=YELLOW, tip=0.26):
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.6)


def wrapped(c, r_ax, n, pitch, op=0.3):
    """Cross-section: axon, glial sheath (filled annulus) and n membrane turns. Returns (sheath, rings, axon)."""
    c = np.array([c[0], c[1], 0.0])
    if n > 0:
        sheath = Annulus(inner_radius=r_ax, outer_radius=r_ax + n * pitch, fill_color=PURPLE,
                         fill_opacity=op, stroke_width=0).move_to(c)
    else:
        sheath = VGroup()
    rings = VGroup(*[Circle(radius=r_ax + k * pitch, stroke_color=PURPLE, stroke_width=2).move_to(c)
                     for k in range(1, n + 1)])
    axon = Circle(radius=r_ax, stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                  fill_opacity=0.4).move_to(c)
    return sheath, rings, axon


def spiral(cx, r_out, pitch, turns=4, width=6):
    return ParametricFunction(
        lambda t: np.array([cx + (r_out - pitch * t / TAU) * np.cos(t),
                            (r_out - pitch * t / TAU) * np.sin(t), 0.0]),
        t_range=[0, TAU * turns, 0.05], color=PURPLE, stroke_width=width)


def channels():
    ch = VGroup()
    for xn in NODE_X:
        for dx in (-0.2, 0.0, 0.2):
            for sgn in (1, -1):
                ch.add(Rectangle(width=0.12, height=0.36, stroke_color=GREEN, stroke_width=2,
                                 fill_color=GREEN, fill_opacity=0.9).move_to([xn + dx, sgn * 0.9, 0]))
    return ch.set_z_index(3)


def node_axon(pitch=2.5):
    axon = axon_bar(h=1.8).set_z_index(2)
    # Longitudinal section: the sheath lies outside the axoplasm.
    sheaths = VGroup(*[VGroup(*[
        Rectangle(width=1.65, height=0.8, stroke_color=PURPLE, stroke_width=3,
                  fill_color=PURPLE, fill_opacity=0.65).move_to([(i-2)*pitch, sign*1.32, 0])
        for sign in (-1, 1)]) for i in range(5)])
    return axon, sheaths


def glow(k, r=0.75):
    return Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=0.75).move_to([NODE_X[k], 0, 0]).set_z_index(4)


def two_lines(a, b, size=26, color=TEXT):
    return VGroup(T(a, size, color), T(b, size, color)).arrange(DOWN, buff=0.16)


# ------------------------------------------------------------------ s00
class S00Title(TitleCard):
    LESSON = "Myelination: Wrapping the Axon So the Signal Jumps"
    TITLE = "Why Wrap, and How Much"
    def construct(self):
        title = T(self.TITLE, 50, TEXT, font=TITLE_FONT)
        rule = Line(LEFT*4.6, RIGHT*4.6, color=GOLD, stroke_width=4)
        brand = T("BIOCHEMISTRYPEDIA", 26, TEAL)
        group = VGroup(brand, title, rule).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.add(brand)
        self.play(Write(title), GrowFromCenter(rule), run_time=1.4)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        sh, rings, ax = wrapped([-3.2, 0], 1.25, 12, 0.1)
        thin = Circle(radius=1.15, color=BLUE, fill_color=BLUE, fill_opacity=0.4).move_to([3.2,0,0])
        q = VGroup(*[T("?",64).move_to([x,3.0,0]) for x in (-3.2,3.2)])
        labels = VGroup(T("wrapped",30,PURPLE).move_to([-3.2,-2.9,0]), T("bare",30,BLUE).move_to([3.2,-2.9,0]))
        self.add(ax,thin,q,labels)
        self.at("wrap an axon")
        self.play(FadeIn(sh), LaggedStart(*[Create(r) for r in rings],lag_ratio=0.06),run_time=1.2)
        self.at("never wrapped")
        self.play(FadeIn(T("never wrapped",26).move_to([3.2,-3.5,0])),run_time=0.4)
        self.finish()


class S02Charge(SpokenScene):
    def construct(self):
        yc = 0.3
        patch = Rectangle(width=4.6, height=4.6, stroke_color=BLUE, stroke_width=3.5,
                          fill_color=BLUE, fill_opacity=0.22).move_to([-1.5, yc, 0])
        plates = VGroup(Line([-3.8, yc + 2.3, 0], [0.8, yc + 2.3, 0], color=BLUE, stroke_width=9),
                        Line([-3.8, yc - 2.3, 0], [0.8, yc - 2.3, 0], color=BLUE, stroke_width=9))
        pl = T("one patch of membrane", 26, BLUE).move_to([-1.5, -2.6, 0])
        active = Rectangle(width=2.6, height=4.6, stroke_color=YELLOW, stroke_width=3.5,
                           fill_color=YELLOW, fill_opacity=0.5).move_to([-5.1, yc, 0])
        al = T("active stretch", 26, YELLOW).move_to([-5.1, -2.6, 0])
        cur = harrow(-4.5, -2.4, yc, 9)
        gframe = Rectangle(width=1.0, height=3.6, stroke_color=GREY, stroke_width=3).move_to([4.6, 0.2, 0])
        gbot = 0.2 - 1.8
        thr_y = gbot + 0.75 * 3.6
        thr = Line([4.0, thr_y, 0], [5.2, thr_y, 0], color=GREY, stroke_width=5)
        tl = T("threshold", 26, GREY).move_to([2.7, thr_y, 0])
        gl = T("charge on the patch", 26, GREY).move_to([4.6, -2.15, 0])
        fill0 = Rectangle(width=0.9, height=0.05, stroke_width=0, fill_color=CHARGE, fill_opacity=0.8).move_to([4.6, gbot + 0.025, 0])
        h1 = 2.95
        fill1 = Rectangle(width=0.9, height=h1, stroke_width=0, fill_color=CHARGE, fill_opacity=0.8).move_to([4.6, gbot + h1 / 2, 0])
        plus = VGroup(*[M("+", 28, CHARGE).move_to([-3.3 + 0.65 * i, yc + 1.9, 0]) for i in range(7)])
        minus = VGroup(*[M("-", 28, CHARGE).move_to([-3.3 + 0.65 * i, yc - 1.9, 0]) for i in range(7)])

        self.at("start with one patch")
        self.play(FadeIn(patch), FadeIn(plates), FadeIn(pl, shift=UP * 0.1), run_time=0.8)
        self.at("current spreads to it")
        self.play(FadeIn(active), run_time=0.35)
        self.play(GrowArrow(cur), run_time=0.45)
        self.at("active stretch behind")
        self.play(FadeIn(al, shift=UP * 0.1), run_time=0.4)
        self.add(Line([0.8,2.2,0],[4.0,1.1,0],color=CHARGE), Line([0.8,-1.6,0],[4.0,-1.6,0],color=CHARGE))
        self.at("before it can fire")
        self.play(FadeIn(gframe), FadeIn(thr), FadeIn(tl), FadeIn(gl), FadeIn(fill0), run_time=0.7)
        self.at("that current must charge it")
        self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in list(plus) + list(minus)], lag_ratio=0.08),
                  Transform(fill0, fill1), run_time=0.9, rate_func=linear)
        self.play(thr.animate.set_color(CHARGE), tl.animate.set_color(CHARGE), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ s03
class S03Leak(SpokenScene):
    def construct(self):
        axon = axon_bar(h=3.0)
        centers = [-5,-3,-1,1,3,5]
        divs = VGroup(*[Line([x,-1.5,0],[x,1.5,0],color=BLUE) for x in (-4,-2,0,2,4)])
        pulse = Rectangle(width=1.8,height=2.9,fill_color=YELLOW,fill_opacity=0.35,stroke_width=0).move_to([-5,0,0])
        self.add(axon,divs,pulse,T("bare axon",30,BLUE).move_to([0,-3.3,0]))
        self.at("current also leaks")
        label=T("current leaks out",30,RED).move_to([0,3.1,0])
        initial=harrow(-5.7,5.7,0,9)
        self.play(FadeIn(label),GrowArrow(initial),run_time=0.4)
        arrows=VGroup()
        for x in centers:
            a=leak(x,1.5,2.5)
            self.play(GrowArrow(a),run_time=0.14)
            arrows.add(a)
        self.at("rebuilt on every patch")
        self.play(FadeOut(initial),run_time=0.15)
        for k in range(1,6):
            current=harrow(centers[k-1],centers[k]-0.2,0,9)
            tick=T(str(k),26,GREY).move_to([centers[k-1],-2.2,0])
            self.play(GrowArrow(current),FadeIn(tick),run_time=0.18)
            self.play(pulse.animate.move_to([centers[k],0,0]),FadeOut(current),run_time=0.2)
        self.at("less current is left")
        long=harrow(-4.9,4.8,0,10)
        short=harrow(-4.9,-2.8,0,3)
        self.play(FadeOut(pulse),GrowArrow(long),run_time=0.4)
        self.play(Transform(long,short),FadeIn(T("slow: rebuild at each patch",28).move_to([0,-2.7,0])),run_time=0.8)
        self.finish()


class S04Wrap(SpokenScene):
    def construct(self):
        ax=Circle(radius=2.0,color=BLUE,fill_color=BLUE,fill_opacity=0.35).move_to([-3,0,0])
        self.add(ax,T("axon",30,BLUE).move_to(ax))
        cells=VGroup()
        for y,name,place in [(1.8,"oligodendrocyte","brain and spinal cord"),(-0.5,"Schwann cell","nerve")]:
            blob=Ellipse(width=0.85,height=0.65,color=PURPLE,fill_color=PURPLE,fill_opacity=0.3).move_to([0.5,y,0])
            mini=VGroup(*wrapped([1.8,y],0.28,3,0.09))
            process=Line([0.9,y,0],[1.25,y,0],color=PURPLE,stroke_width=4)
            label=two_lines(name,place,26,PURPLE).move_to([4.3,y,0])
            cells.add(blob,process,mini,label)
        # A continuous glial sheet is visible from the first membrane cue.
        loose=spiral(-3,2.8,0.20,turns=4,width=5)
        tight=spiral(-3,2.28,0.07,turns=4,width=4)
        self.at("myelin is glial membrane")
        self.play(Create(loose),FadeIn(cells),run_time=0.7)
        self.at("wound many times")
        self.play(ShowPassingFlash(loose.copy().set_color(TEXT),time_width=0.5),run_time=1.0)
        self.at("squeezed tight")
        self.play(Transform(loose,tight),run_time=0.6)
        self.play(FadeIn(two_lines("almost no cytoplasm","between turns",26,PURPLE).move_to([2.8,-2.6,0])),run_time=0.3)
        self.wait(1.5)
        self.finish()


class S05Series(SpokenScene):
    def construct(self):
        axon=axon_bar(-6.1,5.9,-0.1,2.2)
        self.add(axon,T("axon",26,BLUE).move_to([-5.3,-0.6,0]))
        def pair(k):
            return VGroup(*[Line([-3.5,y,0],[2.6,y,0],color=PURPLE,stroke_width=5)
                for y in (1.08+k*0.2,1.17+k*0.2,-1.28-k*0.2,-1.37-k*0.2)])
        layers=[pair(k) for k in range(3)]
        # Fixed left edges and a fourfold change make the two quantities legible.
        c=Rectangle(width=3.0,height=0.3,fill_color=PURPLE,fill_opacity=0.8,stroke_width=0).move_to([-4.5,3.0,0])
        r=Rectangle(width=0.7,height=0.3,fill_color=PURPLE,fill_opacity=0.8,stroke_width=0).move_to([3.25,3.0,0])
        cl=T("capacitance",26,PURPLE).move_to([-4.5,3.5,0]);rl=T("resistance",26,PURPLE).move_to([4.4,3.5,0])
        self.at("each turn adds")
        self.play(FadeIn(layers[0]),FadeIn(c),FadeIn(r),FadeIn(cl),FadeIn(rl),run_time=0.5)
        self.at("two membranes")
        brace=Brace(Line([-3.5,1.85,0],[2.6,1.85,0]),UP,buff=0.04,color=PURPLE)
        caption=T("about 160 membranes; shown: 6",26,PURPLE).move_to([0,2.55,0])
        self.play(GrowFromCenter(brace),FadeIn(caption),run_time=0.5)
        self.add(Arrow([-4.5,2.8,0],[-3.4,1.8,0],color=PURPLE,buff=0.08),Arrow([4.4,2.8,0],[2.7,1.8,0],color=PURPLE,buff=0.08))
        self.at("in series")
        self.play(FadeIn(layers[1]),FadeIn(layers[2]),run_time=0.6)
        self.at("capacitance falls")
        smaller=c.copy().stretch_to_fit_width(0.75).align_to(c,LEFT)
        self.play(Transform(c,smaller),run_time=0.9)
        self.at("resistance rises")
        larger=r.copy().stretch_to_fit_width(2.8).align_to(r,LEFT)
        self.play(Transform(r,larger),run_time=0.9)
        self.at("far more of the current")
        bare=axon_bar(-6.1,5.9,-2.35,0.7)
        gap=Line([4.9,-1.2,0],[4.9,1.0,0],color=GREEN,stroke_width=5)
        gaplabel=T("next gap",26,GREEN).move_to([4.9,1.65,0])
        self.play(FadeIn(bare),FadeIn(T("bare",26,BLUE).move_to([-5.4,-2.95,0])),Create(gap),FadeIn(gaplabel),run_time=0.4)
        a=harrow(-4.7,4.8,-2.35,9); m=harrow(-4.7,4.8,-0.1,9)
        self.play(GrowArrow(a),GrowArrow(m),run_time=0.5)
        self.play(Transform(a,harrow(-4.7,-2.5,-2.35,3)),Transform(m,harrow(-4.7,4.8,-0.1,7)),run_time=0.6)
        note=two_lines("illustrative: 5 µm axon; g = 0.65; about 17 nm per turn", "about 80 turns → about 160 membranes",26,TEXT).move_to([0,-3.25,0])
        self.play(FadeIn(note),run_time=0.4)
        self.finish()


class S06Nodes(SpokenScene):
    def construct(self):
        axon, sheaths = node_axon(2.5)
        chans = channels()
        node_lbl = T("node of Ranvier", 28, GREEN).move_to([-3.75, -2.95, 0])
        node_arr = Arrow([-3.75, -2.55, 0], [-3.75, -1.2, 0], buff=0.05, color=GREEN, stroke_width=5, tip_length=0.2)
        brace = Brace(sheaths[2], UP, color=PURPLE, buff=0.1)
        inter = T("internode", 28, PURPLE).next_to(brace, UP, buff=0.12)
        na_lbl = two_lines("sodium channels", "high channel density", 26, GREEN).move_to([3.7, -2.7, 0])

        self.add(sheaths, axon)
        self.at("those gaps are")
        self.play(FadeIn(node_lbl), GrowArrow(node_arr), run_time=0.6)
        self.play(GrowFromCenter(brace), FadeIn(inter), run_time=0.6)
        self.at("the axon packs")
        self.play(LaggedStart(*[FadeIn(c, scale=1.6) for c in chans], lag_ratio=0.03), run_time=1.0)
        self.at("sodium channels")
        self.play(FadeIn(na_lbl), Create(Line([3.7,-2.1,0],[3.75,-1.2,0],color=GREEN)), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ s07
class S07Jump(SpokenScene):
    def construct(self):
        axon,sheaths=node_axon(); chans=channels()
        self.add(sheaths,axon,chans)
        g=glow(0)
        self.at("the signal is rebuilt")
        self.play(FadeIn(g),run_time=0.3)
        for k in range(3):
            if k==1: self.at("seems to jump")
            current=harrow(NODE_X[k]+0.2,NODE_X[k+1]-0.2,0,8).set_z_index(5)
            nxt=glow(k+1)
            self.play(GrowArrow(current),run_time=0.45)
            self.play(FadeOut(g),FadeIn(nxt),run_time=0.3)
            self.play(Indicate(nxt,color=YELLOW,scale_factor=1.15),run_time=0.3)
            g=nxt
        self.at("saltatory conduction")
        self.play(FadeIn(chip("saltatory conduction",YELLOW,34).move_to([0,-2.9,0])),run_time=0.4)
        self.finish()


class S08Beat(NarratedScene):
    def construct(self):
        axon,sheaths=node_axon()
        self.add(sheaths,axon,channels(),glow(3),chip("saltatory conduction",YELLOW,34).move_to([0,-2.9,0]))
        self.finish()


class S09Rule(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[0, 4.5, 1], y_range=[0, 10, 1], x_length=10.4, y_length=5.4, tips=False,
                  axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 3})
        ax.move_to([0.5, -0.2, 0])
        xl = T("fiber diameter", 26, GREY).next_to(ax.x_axis, DOWN, buff=0.2).align_to(ax.x_axis, RIGHT)
        yl = T("speed", 26, GREY).next_to(ax.y_axis, LEFT, buff=0.2).align_to(ax.y_axis, UP)
        note = T("schematic scaling; near-origin extrapolation", 26, GREY).move_to([0.5, 3.5, 0])
        bare = ax.plot(lambda x: 1.3 * np.sqrt(x), x_range=[0, 4.4], color=BLUE, stroke_width=6)
        bl = T("bare", 30, BLUE).move_to(ax.c2p(3.7, 1.3 * np.sqrt(3.7)) + DOWN * 0.6)
        line = ax.plot(lambda x: 2.2 * x, x_range=[0, 4.4], color=PURPLE, stroke_width=6)
        ml = T("myelinated", 30, PURPLE).move_to(ax.c2p(2.2, 2.2 * 2.2) + UP * 0.9 + LEFT * 0.9)

        self.at("in a bare axon")
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(note), run_time=1.0)
        self.at("square root of diameter")
        self.play(Create(bare), run_time=1.6, rate_func=linear)
        self.play(FadeIn(bl), run_time=0.4)
        self.at("in a myelinated fiber")
        self.play(Create(line), FadeIn(ml), run_time=1.2, rate_func=linear)
        self.at("in proportion to diameter")
        self.wait(2.0)
        self.finish()


# ------------------------------------------------------------------ s10 / s11
def question_frame():
    thin = Circle(radius=0.46, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.4).move_to([-3.3, 0.4, 0])
    thick = Circle(radius=2.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.4).move_to([3.3, 0.4, 0])
    lt = T("2 µm axon", 28, BLUE).move_to([-3.3, -2.25, 0])
    lk = T("10 µm axon", 28, BLUE).move_to([3.3, -2.25, 0])
    q1 = T("?", 72, TEXT, font=TITLE_FONT).move_to([-3.3, 3.2, 0])
    q2 = T("?", 72, TEXT, font=TITLE_FONT).move_to([3.3, 3.2, 0])

    def gbox(x):
        b = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=3.2, height=0.9, stroke_color=GREY, stroke_width=3))
        t = T("gain", 26, GREY)
        return VGroup(b, t).move_to([x, -3.0, 0])
    return thin, thick, lt, lk, q1, q2, gbox(-3.3), gbox(3.3)


class S10Q(SpokenScene):
    def construct(self):
        thin, thick, lt, lk, q1, q2, g1, g2 = question_frame()
        self.add(T("Which gains more?",30).move_to([0,3.25,0]))
        self.at("so which axon")
        self.play(FadeIn(thin, scale=0.8), FadeIn(thick, scale=0.8), FadeIn(lt), FadeIn(lk), run_time=0.7)
        self.at("gains more from a wrap")
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(q1, scale=0.7), FadeIn(q2, scale=0.7), run_time=0.7)
        self.at("a thin one")
        self.play(Indicate(thin, color=BLUE, scale_factor=1.5), run_time=0.6)
        self.at("or a thick one")
        self.play(Indicate(thick, color=BLUE, scale_factor=1.06), run_time=0.6)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        self.add(*question_frame(), T("Which gains more?",30).move_to([0,3.25,0]))
        cue=T("think about it",26,GREY).move_to([0,-0.9,0])
        self.add(cue)
        for i in range(5):
            dot=Dot([0,-1.55,0],color=GREY,radius=0.07)
            self.play(FadeIn(dot),run_time=0.3)
            self.wait(0.4)
            self.play(FadeOut(dot),run_time=0.3)
        self.finish()


# ------------------------------------------------------------------ s12
class S12Reveal(SpokenScene):
    def construct(self):
        rows = [("2 µm axon", 13, 2.1), ("5 µm axon", 21, 0.65), ("10 µm axon", 29, -0.8)]
        x0, k = -2.6, 0.2
        labels, bars, vals = [], [], []
        for name, g, y in rows:
            labels.append(T(name, 30, BLUE).move_to([x0 - 0.3 - 1.1, y, 0]).align_to([x0 - 0.3, y, 0], RIGHT))
            g = 6 * np.sqrt(float(name.split()[0])) / 0.65
            b = Rectangle(width=g * k, height=1.0, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.5)
            b.move_to([x0 + g * k / 2, y, 0])
            bars.append(b)
            vals.append(T(f"about {g:.0f} times", 30, TEXT).next_to(b, RIGHT, buff=0.2))
        head = T("speed gain: times faster than bare", 30, GREY).move_to([0.3, 3.35, 0])
        small = VGroup(T("simple model: g = 0.65, bare speed = square root of d (m/s),", 26, GREY),
                       T("myelinated speed = 6 m/s per µm of fiber diameter", 26, GREY)).arrange(DOWN, buff=0.1).move_to([0, -2.05, 0])
        foot = VGroup(T("Hursh's line is a rule for large fibers,", 26, TEXT),
                      T("so the small row is least reliable.", 26, TEXT)).arrange(DOWN, buff=0.1).move_to([0, -3.0, 0])

        self.at("the thick one")
        self.play(FadeIn(head), run_time=0.2)
        self.play(FadeIn(labels[2]), GrowFromEdge(bars[2], LEFT), FadeIn(vals[2]),run_time=0.5)
        self.at("in a simple model")
        self.play(FadeIn(small), run_time=0.4)
        for i in (0,1):
            self.play(FadeIn(labels[i]),GrowFromEdge(bars[i],LEFT),FadeIn(vals[i]),run_time=0.35)
        self.at("the gain grows")
        self.play(Indicate(bars[2], color=PURPLE, scale_factor=1.04), run_time=0.7)
        self.play(FadeIn(foot), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ s13 / s14
class S13Two(SpokenScene):
    def construct(self):
        c = np.array([0.0, 0.5, 0.0])
        ra, rf = 1.5, 2.5
        axon = Circle(radius=ra, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to(c)
        ring = Annulus(inner_radius=ra, outer_radius=rf, fill_color=PURPLE, fill_opacity=0.35, stroke_color=PURPLE,
                       stroke_width=3).move_to(c)
        inner = VGroup(DoubleArrow(c + LEFT * ra*1.65, c + RIGHT * ra*1.65, buff=0, color=BLUE, stroke_width=5, tip_length=0.2),
                       T("axon  6 µm", 28, BLUE).move_to(c + UP * 0.7))
        yo = c[1] - rf - 0.45
        outer = VGroup(DoubleArrow([-rf, yo, 0], [rf, yo, 0], buff=0, color=PURPLE, stroke_width=5, tip_length=0.2),
                       T("fiber  10 µm  (axon plus myelin)", 26, PURPLE).move_to([0, yo - 0.5, 0]))
        mlbl = T("myelin", 26, PURPLE).move_to(c + RIGHT * (rf + 1.4) + UP * 0.2)
        mline = Line(c + RIGHT * (rf + 0.55) + UP * 0.2, c + RIGHT * 2.0 + UP * 0.2, color=PURPLE, stroke_width=3)

        self.at("the axon diameter")
        axon.scale(1.65)
        self.play(FadeIn(axon), run_time=0.5)
        self.play(GrowFromCenter(inner[0]), FadeIn(inner[1]), run_time=0.6)
        self.at("the fiber diameter")
        self.play(axon.animate.scale(1/1.65), inner[0].animate.scale(1/1.65), FadeIn(ring), run_time=0.6)
        self.play(GrowFromCenter(outer[0]), FadeIn(outer[1]), run_time=0.5)
        self.at("adds the myelin")
        self.play(FadeIn(mlbl, shift=LEFT * 0.1), Create(mline), run_time=0.5)
        self.finish()


class S14G(SpokenScene):
    def construct(self):
        c = np.array([-3.2, 0.0, 0.0])
        ra = 1.5
        rf = ValueTracker(2.5)
        ring = always_redraw(lambda: Annulus(inner_radius=ra, outer_radius=rf.get_value(), fill_color=PURPLE,
                                             fill_opacity=0.35, stroke_color=PURPLE, stroke_width=3).move_to(c))
        axon = Circle(radius=ra, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to(c)
        alb = T("axon", 28, BLUE).move_to(c)
        frac_top = T("axon diameter", 30, BLUE)
        frac_bar = Line(LEFT * 1.6, RIGHT * 1.6, color=GREY, stroke_width=3)
        frac_bot = T("fiber diameter", 30, PURPLE)
        frac = VGroup(frac_top, frac_bar, frac_bot).arrange(DOWN, buff=0.15)
        eq = T("g =", 40, TEXT)
        formula = VGroup(eq, frac).arrange(RIGHT, buff=0.3).move_to([3.0, 1.6, 0])
        readout = always_redraw(lambda: M(f"g = {ra / rf.get_value():.2f}", 60, TEXT).move_to([3.0, -1.2, 0]))
        rlab = T("g ratio", 30, GREY).move_to([3.0, -2.2, 0])

        self.add(ring, axon, alb)
        self.at("their ratio")
        self.play(FadeIn(formula), run_time=0.8)
        self.play(FadeIn(readout), FadeIn(rlab), run_time=0.5)
        self.at("a thinner sheath")
        self.play(rf.animate.set_value(2.0), run_time=2.2, rate_func=smooth)
        self.at("higher g ratio")
        self.play(Indicate(readout, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ s15
class S15Band(SpokenScene):
    def construct(self):
        def v(g):
            return 0.0 if g<=0 or g>=1 else g*np.sqrt(-np.log(g))/np.sqrt(0.5/np.e)
        ax=Axes(x_range=[0,1,0.1],y_range=[0,1.15,0.5],x_length=10.6,y_length=5.7,tips=False,
            axis_config={"include_ticks":False,"color":GREY}).move_to([0.25,-0.05,0])
        curve=ax.plot(v,x_range=[0,1,0.002],color=TEXT,stroke_width=5,use_smoothing=False)
        labels=VGroup(T("relative speed",26).move_to([-4.7,3.1,0]),T("g ratio",28).move_to([0,-3.5,0]))
        ticks=VGroup()
        for x in (0,0.6,0.7,1):
            pt=ax.c2p(x,0)
            ticks.add(Line(pt+UP*0.08,pt+DOWN*0.08,color=GREY),T(f"{x:g}",26).move_to(pt+DOWN*0.35))
        title=T("Rushton model • total fiber diameter fixed",26,GREY).move_to([0,3.5,0])
        x6=ax.c2p(0.6,0)[0]; x7=ax.c2p(0.7,0)[0]
        band=Rectangle(width=x7-x6,height=5.7,fill_color=BAND,fill_opacity=0.24,stroke_width=0).move_to([(x6+x7)/2,ax.get_center()[1],0]).set_z_index(-1)
        bl=two_lines("healthy peripheral","fibers: 0.6–0.7",26,BAND).move_to([1.6,0.2,0])
        leader=Line(bl.get_top()+UP*0.1,ax.c2p(0.65,0.95),color=BAND)
        peak=Dot(ax.c2p(np.exp(-0.5),1),color=TEXT)
        pl=T("fastest, near 0.61",26).move_to([-0.9,2.95,0])
        pline=Line(pl.get_bottom(),peak.get_center()+UP*0.14,color=GREY)
        self.add(ax,labels,ticks,title)
        self.at("healthy peripheral fibers")
        self.play(Create(curve),run_time=1.0)
        self.at("six to zero seven")
        self.play(FadeIn(band),FadeIn(bl),Create(leader),run_time=0.5)
        self.at("close to the fastest")
        self.play(FadeIn(peak),FadeIn(pl),Create(pline),run_time=0.5)
        self.at("the optimum is broad")
        top=ax.plot(v,x_range=[0.5,0.7,0.002],color=TEXT,stroke_width=9)
        flat=DashedLine(ax.c2p(0.42,0.97),ax.c2p(0.78,0.97),color=GREY,stroke_width=2)
        self.play(Create(top),Create(flat),run_time=0.6)
        self.finish()


def schwann_picture():
    cc = np.array([-3.0, 1.2, 0.0])
    body = Ellipse(width=6.2, height=3.6, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.18).move_to(cc)
    axs = VGroup(*[Circle(radius=0.32, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45)
                   .move_to(cc + np.array([dx, dy, 0])) for dx, dy in
                   [(-2.0, -0.55), (-1.0, -0.95), (0.0, -1.05), (1.0, -0.95), (2.0, -0.55)]])
    nm = T("Schwann cell", 26, PURPLE).move_to(cc + UP * 0.75)
    cell = VGroup(body, axs, nm)
    sh, rings, ax = wrapped([4.1, 1.2], 0.8, 9, 0.1)
    big = VGroup(sh, rings, ax)
    lb = T("up to about 1 µm: bare", 26, BLUE).move_to([-3.9, -1.2, 0])
    lk = T("large axon, wrapped", 26, PURPLE).move_to([4.1, -1.2, 0])
    return cell, big, lb, lk


def cutoff_strip():
    axis = Arrow([-6.3, -2.35, 0], [6.4, -2.35, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    al = T("axon diameter (µm)", 26, GREY).move_to([4.65, -2.85, 0])
    t1 = Line([1.4, -2.15, 0], [1.4, -2.55, 0], color=BLUE, stroke_width=5)
    l1 = two_lines("nerve cutoff:", "about 1 µm", 26, BLUE).move_to([1.4, -3.2, 0])
    t2 = Line([-3.6, -2.15, 0], [-3.6, -2.55, 0], color=PURPLE, stroke_width=5)
    l2 = two_lines("central model break-even:", "about 0.2 µm in some models", 26, PURPLE).move_to([-3.6, -3.2, 0])
    qq = T("?", 56, TEXT, font=TITLE_FONT).move_to([-1.1, -1.8, 0])
    return axis, al, t1, l1, t2, l2, qq


class S16Puzzle(SpokenScene):
    def construct(self):
        cell, big, lb, lk = schwann_picture()
        axis, al, t1, l1, t2, l2, qq = cutoff_strip()
        self.add(axis,al,t1,l1)
        self.at("now the puzzle")
        self.play(FadeIn(cell, scale=0.95), FadeIn(big, scale=0.95), run_time=1.0)
        self.play(FadeIn(lk, shift=UP * 0.1), run_time=0.4)
        self.at("up to about one micrometer")
        self.play(FadeIn(lb, shift=UP * 0.1), run_time=0.5)
        self.at("stay bare")
        self.play(Indicate(t1,color=BLUE),run_time=0.5)
        self.at("break even")
        self.play(GrowFromCenter(t2), FadeIn(l2), run_time=0.7)
        self.at("speed alone")
        self.play(FadeIn(qq, scale=0.6), run_time=0.5)
        self.finish()


class S17Decide(SpokenScene):
    def construct(self):
        cell,big,lb,lk=schwann_picture()
        strip=VGroup(*cutoff_strip())
        self.add(cell,big,lb,lk,strip)
        q=T("?",72,TEXT).move_to([-1.0,-1.65,0])
        c1=chip("space",GREY,30).move_to([-3.0,-3.0,0])
        c2=chip("energy cost",GREY,30).move_to([1.0,-3.0,0])
        lines=VGroup(Line(q.get_bottom(),c1.get_top(),color=GREY),Line(q.get_bottom(),c2.get_top(),color=GREY))
        self.at("space and energy")
        self.play(FadeOut(strip),FadeIn(c1),FadeIn(c2),run_time=0.5)
        self.at("something in the tissue")
        self.play(FadeIn(q),FadeIn(lines),run_time=0.6)
        self.play(Indicate(q,color=TEXT,scale_factor=1.2),run_time=1.1)
        self.finish()


class S18Beat(NarratedScene):
    def construct(self):
        cell,big,lb,lk=schwann_picture()
        old=VGroup(cell,big,lb,lk,T("?",72).move_to([-1.0,-1.65,0]))
        self.add(old)
        self.wait(2)
        a1,a2,a3=row_axons()
        self.play(FadeOut(old),FadeIn(a1,shift=RIGHT*0.5),FadeIn(a2,shift=RIGHT*0.5),FadeIn(a3,shift=RIGHT*0.5),run_time=0.8)
        self.finish()


def row_axons():
    _, _, a_bare = wrapped([-4.6, 0.8], 0.3, 0, 0.1)
    return a_bare, VGroup(*wrapped([-1.8, 0.8], 0.6, 3, 0.12)), VGroup(*wrapped([3.0, 0.8], 1.0, 8, 0.1))


class S19Idea(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.3, width=12.6, height=7.0, stroke_color=GOLD, stroke_width=3,
                                fill_color=GOLD, fill_opacity=0.05)
        head = T("THE IDEA TO CARRY", 26, GOLD, weight=BOLD).move_to([0, 3.0, 0])
        a1, a2, a3 = row_axons()
        self.add(a1,a2,a3,two_lines("wrapped,","thinner",26,PURPLE).move_to([-1.8,-1.35,0]))
        card.set_z_index(-2)
        big_lbl = T("largest speed gain", 26, TEXT).move_to([3.0, -1.5, 0])
        small_lbl = VGroup(two_lines("too small, bare", "",26,BLUE).move_to([-4.6,-1.35,0]), Line([-4.6,-0.9,0],[-4.6,0.35,0],color=BLUE))
        line = T("Match the wrap to the axon.", 46, TEXT, font=TITLE_FONT).move_to([0, -2.4, 0])
        how = T("How?", 40, YELLOW, font=TITLE_FONT).move_to([0, -3.15, 0])

        self.at("here is the idea")
        self.play(FadeIn(card), FadeIn(head), run_time=0.8)
        self.at("the speed gain")
        self.play(Indicate(a3,color=PURPLE,scale_factor=1.05),run_time=0.6)
        self.play(FadeIn(big_lbl),FadeIn(small_lbl), run_time=0.5)
        self.at("nerves do match")
        self.play(Write(line), run_time=1.6)
        # The word aligner omitted the final “How?”; hold until the audio ends.
        rest = self.narration_s - self.elapsed()
        if rest > 0:
            self.wait(rest)
        self.play(FadeIn(how, shift=UP * 0.1), run_time=0.3)
        self.wait(1.0)
        self.finish()


class S20Idea2(SpokenScene):
    def construct(self):
        self.add(T("Match the wrap to the axon.",42,TEXT,font=TITLE_FONT).move_to([0,3,0]))
        def row(y,central):
            ax=Circle(radius=0.46,color=BLUE,fill_color=BLUE,fill_opacity=0.35).move_to([-5.3,y,0])
            cell=Ellipse(width=1.25,height=0.85,color=PURPLE,fill_color=PURPLE,fill_opacity=0.3).move_to([-2.7,y,0])
            names=VGroup(T("axon",26,BLUE).move_to([-5.3,y-0.85,0]),T("oligodendrocyte" if central else "Schwann cell",26,PURPLE).move_to([-2.7,y-0.85,0]))
            # No causal arrow: both partners are explicitly named.
            connector=Line([-4.7,y,0],[-3.4,y,0],color=GREY)
            words=two_lines("Brain and spinal cord:" if central else "Nerve: the axon decides", "much of its own program" if central else "how much wrapping",30,TEXT).move_to([2.7,y,0])
            return VGroup(ax,cell,names,connector,words)
        first=row(1,False); second=row(-1.8,True)
        self.at("in nerve")
        self.play(FadeIn(first),run_time=0.6)
        self.at("in the brain and spinal cord")
        self.play(FadeIn(second),run_time=0.6)
        self.at("its own program")
        self.play(Indicate(second[-1][1],color=PURPLE,scale_factor=1.04),run_time=0.5)
        self.finish()


class S21End(EndCard):
    LINE = "In nerve, the axon decides."
    def construct(self):
        line=T(self.LINE,44,TEXT,font=TITLE_FONT).move_to([0,0.4,0])
        pointer=T("Chapter 2 • The Axon Sets the Dose",28,GREY).move_to([0,-0.6,0])
        self.play(FadeIn(line),run_time=0.5)
        self.play(FadeIn(pointer),run_time=0.4)
        self.finish()

