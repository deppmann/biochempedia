"""Photoreceptor adaptation and degeneration: animation for the revised narration  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = light (background light, the flash)
  ORANGE = calcium (dots, gauge, bath tag, the calcium-dependent mechanism)
  PURPLE = the two calcium sensors, GCAPs and recoverin (and their kinase partner chip)
  TEAL   = membrane proteins (CNG channels, the pump)
  GREEN  = cGMP, adaptation / gain control, the dark state, supportive / therapeutic effects
  PINK   = activated visual pigment
  BLUE   = intact / control photoreceptors (cells, curves, labels, bars)
  RED    = removed / lacking / off (crossed-out sensors, knockout cones, the off T-bar, "not clamped")
  GREY   = membranes, outlines, unknowns (dashed question-mark boxes)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=22, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color, op=0.16):
    return [c[1].animate.set_stroke(color).set_fill(color, op), c[2].animate.set_color(color)]


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.05
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def cone_cell(color=GREY, s=1.0):
    """A simple cone cell: tapered outer segment on top, rounded cell body, a stub of axon."""
    outer = Polygon([-0.55, 0, 0], [0.55, 0, 0], [0.14, 1.7, 0], [-0.14, 1.7, 0], stroke_color=color, stroke_width=4,
                    fill_color=color, fill_opacity=0.18)
    body = RoundedRectangle(corner_radius=0.4, width=1.4, height=1.1, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.18).move_to([0, -0.55, 0])
    stub = Line([0, -1.1, 0], [0, -1.6, 0], color=color, stroke_width=4)
    g = VGroup(outer, body, stub).scale(s)
    g.outer, g.body = outer, body
    return g


def cross(mob, color=RED, w=6):
    r = mob.get_right()[0] - 0.12
    l = mob.get_left()[0] + 0.12
    t = mob.get_top()[1] - 0.05
    b = mob.get_bottom()[1] + 0.05
    return VGroup(Line([l, t, 0], [r, b, 0], color=color, stroke_width=w), Line([l, b, 0], [r, t, 0], color=color, stroke_width=w))


def bar(left, y, w, color, h=0.4):
    return Rectangle(width=max(w, 0.05), height=h, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([left + max(w, 0.05) / 2, y, 0])


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def make_plot(dim_axes=False):
    """Log-log plot of relative sensitivity S/Sdark against background I, computed from the lesson's fit values."""
    ax = Axes(x_range=[2, 6, 1], y_range=[-3, 0, 1], x_length=8.2, y_length=4.5,
              axis_config={"color": GREY, "stroke_width": 3, "include_ticks": True, "include_tip": False},
              ).move_to([-1.9, -0.25, 0])
    grid = VGroup(*[Line(ax.c2p(2, y), ax.c2p(6, y), color=GREY, stroke_width=1, stroke_opacity=0.25) for y in (-1, -2, -3)])
    xl = VGroup(*[T("10" + str(k).translate(SUP), 22, GREY).next_to(ax.c2p(k, -3), DOWN, buff=0.15) for k in range(2, 7)])
    yl = VGroup(*[T(s, 22, GREY).next_to(ax.c2p(2, y), LEFT, buff=0.15)
                  for y, s in ((0, "1"), (-1, "0.1"), (-2, "0.01"), (-3, "0.001"))])
    xt = T("background light (photons per µm² per s)", 22, GREY).next_to(xl, DOWN, buff=0.12)
    yt = T("relative sensitivity, S / Sdark", 22, GREY).move_to([-1.9, 2.55, 0])
    base = VGroup(grid, ax, xl, yl, xt, yt)
    return ax, base


def logS(x, I0, n):
    return -np.log10(1 + 10 ** (n * (x - np.log10(I0))))


CTRL = dict(I0=48800, n=1.0)
KO = dict(I0=12100, n=1.5)


def fit_curve(ax, p, color):
    return ax.plot(lambda x: logS(x, p["I0"], p["n"]), x_range=[2, 6, 0.02], color=color, stroke_width=6, use_smoothing=False)


# Additional schematic helpers use the same outlines and chip vocabulary.
def rod_cell(color=BLUE, s=1.0):
    outer = RoundedRectangle(corner_radius=0.15, width=0.7, height=1.7,
                             stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18).move_to([0, 0.85, 0])
    body = RoundedRectangle(corner_radius=0.4, width=1.1, height=1.1,
                            stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18).move_to([0, -0.55, 0])
    return VGroup(outer, body, Line([0, -1.1, 0], [0, -1.6, 0], color=color, stroke_width=4)).scale(s)


def response(left, bottom, width, height, tau, color):
    # Illustrative impulse response, normalized to its stated peak.
    ts = np.linspace(0, 8, 160)
    vals = (ts / tau) * np.exp(1 - ts / tau)
    return VMobject(color=color, stroke_width=5).set_points_as_corners(
        [[left + width*t/8, bottom + height*v, 0] for t, v in zip(ts, vals)])


def question(text, pos, width=3.4):
    box = DashedVMobject(RoundedRectangle(width=width, height=1.0, corner_radius=0.15,
                                        stroke_color=GREY), num_dashes=26).move_to(pos)
    return VGroup(box, T(text, 22, GREY).move_to(box))


class S00Title(TitleCard):
    LESSON = "Photoreceptors across a billion-fold range, and when they fail"
    TITLE = "Calcium Turns Down the Gain"



class S01Gain(SpokenScene):
    def construct(self):
        cell = cone_cell(BLUE, 1.25).move_to([-4.5, -0.25, 0])
        light = VGroup(T("background light", 26, YELLOW).move_to([0, 3.1, 0]), bar(-5.6, 2.55, 0.5, YELLOW))
        self.at("Your eyes work")
        self.play(FadeIn(cell), FadeIn(light), run_time=0.7)
        dial = VGroup(Arc(radius=0.75, start_angle=0, angle=PI, color=GREEN).move_to([3.7, 1.5, 0]),
                      T("gain", 26, GREEN).move_to([3.7, 0.6, 0]))
        needle = Line([3.7, 1.1, 0], [4.3, 1.7, 0], color=GREEN, stroke_width=6)
        self.at("turning its own")
        self.play(FadeIn(dial), Create(needle), run_time=0.5)
        self.at("background brightens")
        self.play(Transform(light[1], bar(-5.6, 2.55, 11.2, YELLOW)),
                  Transform(needle, Line([3.7, 1.1, 0], [3.1, 1.5, 0], color=GREEN, stroke_width=6)), run_time=0.9)
        gauge = VGroup(Rectangle(width=0.35, height=1.55, color=ORANGE).move_to([-4.5, 0.9, 0]),
                       bar(-4.675, 0.9, 0.35, ORANGE, 1.5),
                       T("calcium", 24, ORANGE).move_to([-1.9, 1.55, 0]),
                       T("outer segment", 22, GREY).move_to([-1.9, 0.95, 0]))
        self.at("Calcium is the signal")
        self.play(FadeIn(gauge), run_time=0.5)
        self.at("Light lowers calcium")
        self.play(Transform(gauge[1], bar(-4.675, 0.3, 0.35, ORANGE, 0.3)), run_time=1.0)
        cg = bchip("cGMP synthesis ↑", GREEN, 24).move_to([-0.8, -0.15, 0])
        self.at("Falling calcium speeds")
        self.play(FadeIn(cg), run_time=0.6)
        pig = bchip("pigment off sooner", PINK, 24).move_to([-0.8, -1.1, 0])
        self.at("active pigment")
        self.play(FadeIn(pig), run_time=0.6)
        traces = VGroup(T("background + flashes", 22, YELLOW).move_to([0.4, -1.45, 0]),
                        Line([-2.3, -2.2, 0], [4.8, -2.2, 0], color=YELLOW, stroke_width=2),
                        T("responses", 22, BLUE).move_to([-3.9, -3.0, 0]))
        for x in (-2.3, 0, 2.3):
            traces.add(Line([x, -2.2, 0], [x, -1.8, 0], color=YELLOW, stroke_width=5),
                       response(x, -3.2, 2, 0.65, 0.6, BLUE))
        self.at("That feedback keeps")
        self.play(FadeOut(cg), FadeOut(pig), run_time=0.3)
        self.play(FadeIn(traces), run_time=0.6)
        self.finish()


class S02Loop(SpokenScene):
    def construct(self):
        cap = RoundedRectangle(corner_radius=0.6, width=8.4, height=4.0, stroke_color=GREY,
                               stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([-2.3, -0.4, 0])
        chans = VGroup(*[bchip("CNG", TEAL, 22).move_to([x, 1.6, 0]) for x in (-5, -3.2, -1.4)])
        outline = VGroup(cap, T("outer segment", 22, GREY).move_to([-4.9, -1.95, 0]))
        dots = VGroup(*[Dot([x, 2.2, 0], radius=0.1, color=ORANGE) for x in (-5, -3.2, -1.4)])
        light = VGroup(T("light", 26, YELLOW).move_to([-0.2, 2.8, 0]), arr([-1.4, 3.1, 0], [-1.4, 2, 0], YELLOW))
        self.add(outline, chans, dots)
        self.at("Light closes channels")
        self.play(FadeIn(light), *[a for c in chans for a in recolor(c, GREY, 0.05)], run_time=0.8)
        self.at("entry falls")
        self.play(FadeOut(dots), run_time=0.5)
        pump = bchip("pump", TEAL, 22).move_to([-3.0, -2.4, 0])
        calcium = Dot([-3, -1.6, 0], color=ORANGE, radius=0.12)
        self.at("pump keeps removing")
        self.play(FadeIn(pump), FadeIn(calcium), run_time=0.3)
        self.play(calcium.animate.move_to([-3, -3.1, 0]), run_time=0.8)
        self.play(FadeOut(calcium), run_time=0.2)
        gcap = bchip("GCAPs", PURPLE, 22).move_to([-5, 0.35, 0])
        cg = bchip("cGMP", GREEN, 22).move_to([-2.6, 0.35, 0])
        thick = arr(gcap.get_right(), cg.get_left(), PURPLE, 9)
        self.at("At low calcium")
        self.play(FadeIn(gcap), run_time=0.5)
        self.at("speeds see GMP")
        self.play(GrowArrow(thick), FadeIn(cg), run_time=0.7)
        self.at("which reopens channels")
        up = arr(cg.get_top(), [-2.6, 1.3, 0], GREEN, 4)
        self.play(GrowArrow(up), *[a for c in chans for a in recolor(c, TEAL)], run_time=0.7)
        rec = bchip("recoverin", PURPLE, 22).move_to([-4.9, -0.8, 0])
        grk = bchip("GRK1", PURPLE, 22).next_to(rec, RIGHT, buff=0.05)
        self.at("Recover in")
        self.play(FadeIn(rec), FadeIn(grk), run_time=0.4)
        self.at("Let's Go")
        self.play(grk.animate.move_to([-2.4, -0.8, 0]), run_time=0.7)
        pig = bchip("activated pigment", PINK, 22).move_to([0, -0.8, 0])
        tb = inhib([-1.75, -0.8, 0], [pig.get_left()[0] - 0.05, -0.8, 0])
        self.at("switches off activated pigment")
        self.play(FadeIn(pig), Create(tb), run_time=0.5)
        self.play(*recolor(pig, GREY, 0.05), run_time=0.5)
        back = bchip("toward dark state", GREEN, 24).move_to([4.4, 0.4, 0])
        self.at("Both push the cell back")
        # Clear the detailed branches before zooming out to the feedback loop.
        detail = VGroup(gcap, cg, thick, up, rec, grk, pig, tb, pump)
        self.play(FadeOut(detail), FadeIn(back), run_time=0.7)
        loop = CurvedArrow([4.2, -0.4, 0], [-0.9, 1.5, 0], angle=-PI/2, color=GREEN, stroke_width=5)
        label = T("gain control", 30, GREEN, weight=BOLD).move_to([4.3, -2, 0])
        self.at("gain control")
        self.play(Create(loop), FadeIn(label), run_time=0.7)
        self.finish()


class S03Cut(SpokenScene):
    def construct(self):
        heads = VGroup(T("control rod", 26, BLUE).move_to([-3.4, 3.0, 0]),
                       T("GCAP knockout rod", 26, RED).move_to([3.2, 3.0, 0]))
        cells = VGroup(rod_cell(BLUE, 0.55).move_to([-5.6, 0.9, 0]), rod_cell(RED, 0.55).move_to([0.8, 0.9, 0]))
        self.at("To test a loop")
        self.play(FadeIn(heads), FadeIn(cells), run_time=0.7)
        chips = VGroup(*[bchip(n, PURPLE, 22).move_to([x, 2.1, 0]) for n,x in (("GCAP1",2.2),("GCAP2",4.3))])
        self.at("cut it")
        self.play(FadeIn(chips), run_time=0.3)
        self.at("mouse rods lacking both")
        cuts = VGroup(*[cross(c) for c in chips])
        self.play(Create(cuts), run_time=0.6)
        baselines = VGroup(Line([-4.6,-0.4,0],[-0.8,-0.4,0],color=GREY), Line([1.5,-0.4,0],[5.8,-0.4,0],color=GREY))
        ctrl = response(-4.6,-0.4,3.8,0.35,0.55,BLUE)
        ko = response(1.5,-0.4,4.3,0.35,1.9,RED)
        self.at("responses recover slowly")
        self.play(Create(baselines), Create(ctrl), Create(ko), run_time=0.8)
        photons = VGroup(*[Dot([x,1.1,0],radius=0.1,color=YELLOW) for x in (-4.4,1.7)])
        self.at("single photon responses grow")
        self.play(FadeIn(photons), run_time=0.3)
        self.at("about five times larger")
        five = T("≈ 5×",26,RED).move_to([5.4,1.65,0])
        self.play(Transform(ko,response(1.5,-0.4,4.3,1.75,1.9,RED)),FadeIn(five),run_time=0.8)
        impaired = T("background adaptation impaired",24,RED).move_to([0,-1.15,0])
        self.at("adaptation to background light")
        self.play(FadeOut(photons), FadeOut(chips), FadeOut(cuts), FadeIn(impaired),run_time=0.6)
        cones = VGroup(cone_cell(BLUE,0.3).move_to([-5.5,-2.35,0]), cone_cell(RED,0.3).move_to([0.8,-2.35,0]),
                       response(-4.6,-2.9,3.8,0.17,0.45,BLUE), response(1.5,-2.9,4.3,0.85,1.3,RED),
                       T("cones",22,GREY).move_to([-5.5,-3.2,0]))
        self.at("Cones without")
        self.play(FadeIn(cones),run_time=0.8)
        self.at("normally curb")
        self.play(Indicate(ctrl,color=BLUE,scale_factor=1.05),Indicate(ko,color=RED,scale_factor=1.05),run_time=0.7)
        tag = bchip("GCAP1 mutations: inherited blinding disease",RED,26).move_to([0,-2.2,0])
        self.at("In people")
        self.play(FadeOut(cones),FadeOut(impaired),run_time=0.4)
        self.at("mutations are linked")
        self.play(FadeIn(tag),run_time=0.7)
        self.finish()


def n_asym(x, p):
    return p["n"] * (x - np.log10(p["I0"]))


class S04Curve(SpokenScene):
    def construct(self):
        ax, base = make_plot()
        ctrl, ko = fit_curve(ax,CTRL,BLUE), fit_curve(ax,KO,RED)
        self.at("Sensitivity falls")
        self.play(FadeIn(base), Create(ctrl),run_time=1.2)
        x0,x1 = np.log10(CTRL["I0"]),np.log10(KO["I0"])
        halfy = np.log10(0.5)
        dots = VGroup(Dot(ax.c2p(x0,halfy),color=BLUE,radius=0.1),Dot(ax.c2p(x1,halfy),color=RED,radius=0.1))
        marks = VGroup(DashedLine(ax.c2p(2,halfy),ax.c2p(x0,halfy),color=GREY),
                       DashedLine(ax.c2p(x0,halfy),ax.c2p(x0,-3),color=BLUE),
                       T("½",24,GREY).next_to(ax.c2p(2,halfy),LEFT,buff=0.18),
                       T("I0",24,BLUE).next_to(ax.c2p(x0,-3),UP,buff=0.15))
        self.at("is the background")
        self.play(Create(marks),FadeIn(dots[0]),run_time=0.8)
        slope = T("n sets slope",24,BLUE).move_to([4.5,2.1,0])
        self.at("sets the slope")
        self.play(FadeIn(slope),run_time=0.6)
        legend = VGroup(T("control",26,BLUE), T("without GCAPs",24,RED),T("and recoverin",24,RED)).arrange(DOWN,buff=0.18).move_to([4.5,0.7,0])
        self.at("Mouse cones lacking")
        self.play(Create(ko),FadeIn(legend),run_time=0.9)
        mark2=VGroup(DashedLine(ax.c2p(x1,halfy),ax.c2p(x1,-3),color=RED),T("I0",24,RED).next_to(ax.c2p(x1,-3),UP,buff=0.15))
        self.at("reach half sensitivity")
        self.play(Create(mark2),FadeIn(dots[1]),run_time=0.7)
        ratio=T("I0 ≈ ¼ control",24,RED).move_to([4.5,-0.7,0])
        self.at("about a quarter")
        self.play(FadeIn(ratio),run_time=0.5)
        steep=T("steeper fall",24,RED).move_to([4.5,-1.4,0])
        self.at("fall more steeply")
        self.play(FadeIn(steep),run_time=0.5)
        q=question("remaining adaptation?",[4.5,-2.65,0],3.8)
        self.at("Some adaptation remains")
        self.play(FadeIn(q),run_time=0.7)
        self.finish()


class S05RodsCones(SpokenScene):
    def construct(self):
        axis=VGroup(arr([-5.8,1.8,0],[5.8,1.8,0],GREY,3),T("dim",24,GREY).move_to([-5.7,2.4,0]),T("bright",24,YELLOW).move_to([5.4,2.4,0]),T("light level",26,GREY).move_to([0,3.1,0]))
        rods=VGroup(bar(-5.7,1.1,6.7,BLUE),T("rods",26,BLUE).move_to([-3.2,0.5,0]))
        cones=VGroup(bar(-0.7,-0.2,6.4,BLUE),T("cones",26,BLUE).move_to([3.3,-0.8,0]))
        self.at("Rods and cones split")
        self.play(FadeIn(axis),FadeIn(rods),FadeIn(cones),run_time=0.8)
        rtrace=VGroup(T("single photon",22,YELLOW).move_to([-3.3,-1.4,0]),response(-5.5,-2.8,4.3,0.95,1.0,BLUE))
        self.at("A rod can respond")
        self.play(FadeIn(rtrace),run_time=0.7)
        ctrace=response(1,-2.8,4.3,0.5,0.4,BLUE)
        self.at("Cones are less sensitive")
        self.play(Create(ctrace),run_time=0.7)
        self.at("end each response faster")
        self.play(Indicate(ctrace,color=BLUE,scale_factor=1.05),run_time=0.7)
        mouse=bchip("mouse recordings",GREY,26).move_to([0,3,0])
        self.at("Mouse recordings")
        self.play(FadeOut(axis),FadeOut(rods),FadeOut(cones),FadeOut(rtrace),FadeOut(ctrace),run_time=0.3)
        self.play(FadeIn(mouse),run_time=0.4)
        ax=Axes(x_range=[0,10,2],y_range=[0,1,0.5],x_length=9.5,y_length=3.8,axis_config={"include_tip":False,"include_ticks":False,"color":GREY}).move_to([0,-0.1,0])
        labels=VGroup(T("rod-driven contrast sensitivity",26,BLUE).move_to([0,2.0,0]),T("continued exposure →",24,GREY).move_to([1,-2.7,0]),T("schematic",22,GREY).move_to([4.6,-3.3,0]))
        start=VGroup(DashedLine(ax.c2p(2,0),ax.c2p(2,1),color=YELLOW),T("bright background starts",22,YELLOW).move_to([-2.5,-3.3,0]))
        before=ax.plot(lambda x:0.9,x_range=[0,2],color=BLUE,stroke_width=5)
        drop=ax.plot(lambda x:0.9-0.72*(x-2),x_range=[2,3],color=BLUE,stroke_width=5)
        recover=ax.plot(lambda x:0.18+0.64*(1-np.exp(-(x-3)/2.2)),x_range=[3,10],color=BLUE,stroke_width=5)
        self.at("On a bright background")
        self.play(FadeIn(ax),FadeIn(labels),FadeIn(start),Create(before),run_time=0.7)
        self.at("responses dip")
        self.play(Create(drop),run_time=0.7)
        self.at("then recover")
        self.play(Create(recover),run_time=1.3)
        self.at("in these mice")
        self.play(Indicate(recover,color=BLUE,scale_factor=1.02),run_time=0.7)
        self.finish()


class S06Degeneration(SpokenScene):
    def construct(self):
        rods=VGroup(*[rod_cell(BLUE,0.65).move_to([x,0.8,0]) for x in (-4.5,-1.5,1.5)])
        cones=VGroup(*[cone_cell(BLUE,0.65).move_to([x,0.8,0]) for x in (-3,0,3)])
        head=T("photoreceptor loss",30,TEXT).move_to([0,3.1,0])
        self.at("When photoreceptors die")
        self.play(FadeIn(rods),FadeIn(cones),FadeIn(head),run_time=0.7)
        rp=T("typical retinitis pigmentosa",30,TEXT).move_to(head)
        self.at("typical retinitis pigmentosa")
        self.play(Transform(head,rp),run_time=0.7)
        self.at("rods die first")
        self.play(rods.animate.set_opacity(0.08),run_time=0.7)
        self.at("cones die after")
        self.play(cones.animate.set_opacity(0.08),run_time=0.7)
        vision=T("daylight + central vision",30,BLUE).move_to([0,-2.2,0])
        self.at("Losing cones costs")
        self.play(FadeIn(vision),run_time=0.7)
        rod=rod_cell(BLUE,0.95).move_to([-4.7,0.6,0])
        cone=cone_cell(BLUE,0.95).move_to([4.8,0.6,0])
        candidate=T("candidate: rod support",28,GREY).move_to([0,3.1,0])
        self.at("One candidate reason")
        self.play(FadeOut(rods),FadeOut(cones),FadeOut(vision),Transform(head,candidate),FadeIn(rod),FadeIn(cone),run_time=0.7)
        factor=bchip("RdCVF",GREEN,24).move_to([-3,1.3,0])
        support=arr([-3.9,1.3,0],factor.get_left(),GREEN,4)
        dock=VGroup(bchip("basigin-1",TEAL,22),bchip("GLUT1",TEAL,22)).arrange(DOWN,buff=0.35,aligned_edge=RIGHT)
        dock.move_to([0,1.0,0]).shift(RIGHT*(cone.body.get_left()[0]-0.3-dock.get_right()[0]))
        docked_factor=factor.copy().next_to(dock[0],LEFT,buff=0.4)
        self.at("rod derived factor")
        self.play(GrowArrow(support),FadeIn(factor),run_time=0.5)
        self.at("RDCVF")
        self.play(FadeIn(dock),factor.animate.move_to(docked_factor),
                  Transform(support,arr([-3.9,1.3,0],docked_factor.get_left(),GREEN,4)),run_time=0.8)
        glucose=VGroup(T("glucose",24,GREEN).move_to([0,-0.8,0]),arr([0.8,-1.0,0],cone.body.get_center()+RIGHT*0.15,GREEN,7),T("experimental models",22,GREY).move_to([0,-3.1,0]))
        self.at("raises cone glucose uptake")
        self.play(FadeIn(glucose),run_time=0.7)
        # Loss of the donor removes the support arrow; both explanations remain candidates.
        damage=question("oxidative damage?",[-2.5,-1.8,0],4.2)
        self.at("Oxidative damage")
        self.play(rod.animate.set_opacity(0.08),FadeOut(support),FadeOut(factor),FadeOut(glucose),FadeIn(damage),run_time=0.7)
        unsettled=T("no single cause settled",28,GREY).move_to([0,-3.1,0])
        self.at("no single cause")
        self.play(FadeIn(unsettled),run_time=0.6)
        self.finish()


class S07Rescue(SpokenScene):
    def construct(self):
        title=T("gene therapy",36,GREEN).move_to([0,3.1,0])
        self.at("Gene therapy")
        self.play(FadeIn(title),run_time=0.7)
        left=RoundedRectangle(width=6.1,height=5.3,corner_radius=0.2,color=GREY).move_to([-3.3,-0.3,0])
        lh=VGroup(T("randomized trial",28,TEXT),T("RPE65 augmentation",26,GREEN)).arrange(DOWN,buff=0.2).move_to([-3.3,1.7,0])
        self.at("randomized trial")
        self.play(Create(left),FadeIn(lh),run_time=0.7)
        course=VGroup(*[Line([-5.8,y,0],[-0.8,y,0],color=GREY,stroke_width=2) for y in (0.2,-1.1)],
                      *[Rectangle(width=0.25,height=0.4,color=YELLOW).move_to([x,y+0.2,0]) for y in (0.2,-1.1) for x in (-3.5,-1.7)])
        treated=Dot([-5.7,0.5,0],color=GREEN,radius=0.13)
        control=Dot([-5.7,-0.8,0],color=BLUE,radius=0.13)
        rows=VGroup(T("treated",22,GREEN).move_to([-5.3,0.95,0]),T("control",22,BLUE).move_to([-5.3,-0.35,0]),T("low-light navigation · 1 year",22,GREY).move_to([-3.3,-2.4,0]))
        levels = VGroup(T("light levels",22,GREY).move_to([-4.9,-1.85,0]),
                        *[bar(-3.6+i*0.65,-1.85,0.45,YELLOW,0.12+0.08*i) for i in range(4)])
        course.add(levels)
        self.at("improved navigation")
        self.play(FadeIn(course),FadeIn(rows),FadeIn(treated),FadeIn(control),run_time=0.6)
        self.play(treated.animate.move_to([-1.0,0.5,0]),control.animate.move_to([-3.9,-0.8,0]),run_time=1.0)
        right=RoundedRectangle(width=6.1,height=5.3,corner_radius=0.2,color=GREY).move_to([3.3,-0.3,0])
        rh=VGroup(T("early editing study",28,TEXT),T("CEP290",26,GREEN)).arrange(DOWN,buff=0.2).move_to([3.3,1.7,0])
        eyes=VGroup(VGroup(Ellipse(width=1.3,height=0.7,color=GREEN),Dot(color=GREEN,radius=0.16)).move_to([2,0.3,0]),
                    VGroup(Ellipse(width=1.3,height=0.7,color=GREY),Dot(color=GREY,radius=0.16)).move_to([4.6,0.3,0]),
                    T("treated eye",22,GREEN).move_to([2,-0.4,0]),T("fellow eye\nuntreated",22,GREY,line_spacing=0.8).move_to([4.6,-0.5,0]))
        self.at("An early editing study")
        self.play(Create(right),FadeIn(rh),FadeIn(eyes),run_time=0.7)
        possible=T("safety + possible benefit",24,GREEN).move_to([3.3,-1.4,0])
        self.at("reported safety")
        self.play(FadeIn(possible),run_time=0.7)
        no=T("no control group",26,RED).move_to([3.3,-2.3,0])
        self.at("without a control group")
        self.play(FadeIn(no),run_time=0.6)
        close=T("design sets the claim",32,TEXT).move_to([0,3.1,0])
        self.at("The design decides")
        self.play(Transform(title,close),run_time=0.7)
        self.finish()


class S08End(EndCard):
    LINE = "Falling calcium turns down photoreceptor gain as background light rises."
