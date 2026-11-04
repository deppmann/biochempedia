"""Chapter 2: Who Makes Them, and How Many Are Kept  (adult neurogenesis, level-up chaptered film)

COLOR MAP (one color per concept; shared with chapters 1 and 3, taken from scenes.old.py)
  BLUE   = neurons, young neurons (A cells), new neurons
  GREY   = structure, outlines, other cells (ependymal, C cells, non-GFAP cells), cards
  MAGENTA = the astrocyte-like stem cell (B cell)
  YELLOW = the inherited label / BrdU label / birth marker, and question marks
  GREEN  = neuron identity (stain for a neuron protein)
  PURPLE = the hippocampus (dentate gyrus)
  RED    = the drug, cells lost
  ORANGE = receptors (the virus receptor, NMDA receptors)
  INDIGO = the retrovirus
  LIGHT  = incoming input / activity
  TEXT   = rules, plain labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
INDIGO = "#8E9BFF"
LIGHT = "#BDEBFA"
STEM = "#E0529C"


def _quiet_at(self, phrase, lead=0.2, nth=0):
    rest = self.t_of(phrase, nth) - lead - self.elapsed()
    if rest > 0.02:
        self.wait(rest)

SpokenScene.at = _quiet_at



# ----------------------------------------------------------------- shared shapes
def cell(r=0.8, color=BLUE, nuc=0.4):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)
    n = Circle(radius=r * nuc, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
    return VGroup(body, n)


def neuron(r=0.55, color=BLUE):
    c = cell(r, color)
    br = VGroup()
    for angle in (0.3, 1.2, 2.2, 3.0):
        d = np.array([np.cos(angle), np.sin(angle), 0])
        tip = d * (r + 0.75)
        br.add(Line(d * r, tip, color=color, stroke_width=4))
        br.add(Line(tip, tip + 0.4 * np.array([np.cos(angle + 0.6), np.sin(angle + 0.6), 0]), color=color, stroke_width=3))
    ax = Line(DOWN * r, DOWN * (r + 1.0), color=color, stroke_width=4)
    return VGroup(c, br, ax)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def bcell(s=1.0, color=STEM):
    """Astrocyte-like cell: round body with radiating processes."""
    rays = VGroup(*[Line(0.5 * s * np.array([np.cos(a), np.sin(a), 0]), 1.0 * s * np.array([np.cos(a), np.sin(a), 0]),
                         color=color, stroke_width=5) for a in np.linspace(0, TAU, 7, endpoint=False) + 0.2])
    return VGroup(rays, cell(0.42 * s, color, 0.45))


def epcell():
    sheet = RoundedRectangle(corner_radius=0.1, width=0.98, height=0.5, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.3)
    cil = VGroup(*[Line([dx, 0.27, 0], [dx, 0.68, 0], color=GREY, stroke_width=3) for dx in (-0.27, 0, 0.27)])
    return VGroup(sheet, cil)


def ccell():
    return cell(0.36, GREY, 0.45)


def acell():
    return VGroup(cell(0.28, BLUE, 0.45), Line(LEFT * 0.28, LEFT * 0.62, color=BLUE, stroke_width=4))


def qmark(size=44):
    return T("?", size, YELLOW, weight=BOLD)


def mouse():
    return VGroup(Ellipse(width=1.2, height=0.6, color=GREY, fill_color=GREY, fill_opacity=1),
                  Circle(radius=0.28, color=GREY, fill_color=BG, fill_opacity=1).move_to([0.6, 0.13, 0]),
                  Circle(radius=0.16, color=GREY, fill_color=BG, fill_opacity=1).move_to([0.53, 0.43, 0]),
                  Dot([0.72, 0.18, 0], radius=0.04, color=TEXT),
                  Arc(radius=0.5, start_angle=PI / 2, angle=PI, color=GREY).move_to([-0.95, 0, 0]))


def wheel(r=1.6):
    return VGroup(Circle(radius=r, color=GREY, stroke_width=5),
                  *[Line(ORIGIN, r * np.array([np.cos(a), np.sin(a), 0]), color=GREY, stroke_width=3)
                    for a in np.linspace(0, TAU, 7, endpoint=False)])


def dg_arc(r=1.9, color=PURPLE, n=14, dot_r=0.13, width=26):
    arc = Arc(radius=r, start_angle=-0.2 * PI, angle=1.4 * PI, stroke_color=color, stroke_width=width)
    arc.set_stroke(opacity=0.4)
    dots = VGroup()
    for k in range(n):
        ang = -0.2 * PI + 1.4 * PI * (k + 0.5) / n
        dots.add(Dot(arc.get_arc_center() + r * np.array([np.cos(ang), np.sin(ang), 0]), radius=dot_r, color=BLUE))
    return VGroup(arc, dots)


def virus(r=0.42):
    spikes = VGroup(*[Line(r * np.array([np.cos(a), np.sin(a), 0]), (r + 0.17) * np.array([np.cos(a), np.sin(a), 0]),
                           color=INDIGO, stroke_width=4) for a in np.linspace(0, TAU, 9, endpoint=False)])
    body = Circle(radius=r, stroke_color=INDIGO, stroke_width=4, fill_color=INDIGO, fill_opacity=0.28)
    return VGroup(body, spikes)


# ----------------------------------------------------------------- brain (s01-s04)
VENT = np.array([-1.6, 0.35, 0])
DGC = np.array([2.0, -0.55, 0])
BULB = np.array([-5.15, -0.55, 0])


def brain():
    # Stylized sagittal mouse brain, anterior at left. Smooth silhouette,
    # cortical mantle, posterior cerebellum and ventral brainstem.
    outline = VMobject(color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)
    outline.set_points_smoothly([[-5.8,-0.7,0],[-5.9,0.3,0],[-4.8,1.0,0],[-3.8,1.1,0],
        [-2.6,2.5,0],[0,2.95,0],[2.8,2.3,0],[4.0,0.8,0],[5.5,0.3,0],
        [5.8,-1.1,0],[4.7,-1.8,0],[3.2,-1.5,0],[2.7,-2.7,0],[1.6,-2.9,0],
        [1.8,-1.6,0],[-0.2,-1.8,0],[-2.6,-1.25,0],[-4.2,-0.65,0],[-5.8,-0.7,0]])
    cortex = VMobject(color=GREY, stroke_width=2).set_points_smoothly(
        [[-3.5,1.1,0],[-2.0,1.95,0],[0,2.15,0],[2.3,1.6,0],[3.2,0.65,0]])
    bulb = Ellipse(width=1.6,height=1.25,color=BLUE,stroke_width=3).move_to(BULB)
    folds=VGroup(*[Arc(radius=.55,start_angle=-PI/2,angle=PI,color=GREY,stroke_width=2).move_to([4.2+.35*i,-.55,0]) for i in range(3)])
    hip=VMobject(color=PURPLE,stroke_width=5).set_points_smoothly([[.4,-.6,0],[.7,.45,0],[2.1,.65,0],[2.8,-.1,0],[2,-1.0,0]])
    return VGroup(outline,cortex,bulb,folds,hip).stretch(1.13, 1, about_point=ORIGIN)


def lumen():
    return Ellipse(width=2.4, height=1.243, color=GREY, stroke_width=4).move_to(VENT)


def svz_ring():
    return Ellipse(width=3.1, height=1.9775, color=TEXT, stroke_width=12).set_stroke(opacity=0.55).move_to(VENT)


STREAM = CubicBezier(VENT + [0, .95, 0], [-3.2, 2.25, 0], [-4.1, 1.25, 0], BULB + [0, -.07, 0])


def stream_dots(n=6):
    return VGroup(*[Dot(STREAM.point_from_proportion(0.0), radius=0.13, color=BLUE) for _ in range(n)])


# ----------------------------------------------------------------- ventricle wall (s05-s11)
RY = {"ep": 1.7, "B": 0.3, "C": -1.2, "A": -2.65}
EP_X = [-5.8 + 1.05 * i for i in range(8)]
B_X = [-5.0, -2.8, -0.6, 1.6]
C_X5 = [-5.4, -3.7, -2.0, -0.3, 1.4]
C_X8 = [-5.4 + 0.85 * i for i in range(9)]
A_X6 = [-3.0 + 0.9 * i for i in range(6)]
A_X4 = A_X6[2:]
LX = 3.35


def make_wall(cx, ax):
    ep = VGroup(*[epcell().move_to([x, RY["ep"], 0]) for x in EP_X])
    B = VGroup(*[bcell(0.8).move_to([x, RY["B"], 0]) for x in B_X])
    C = VGroup(*[ccell().move_to([x, RY["C"], 0]) for x in cx])
    A = VGroup(*[acell().move_to([x, RY["A"], 0]) for x in ax])
    return ep, B, C, A


def rowlab(key, text, color, size=26):
    t = T(text, size, color, line_spacing=0.8)
    t.move_to([0, RY[key], 0])
    t.align_to([LX, 0, 0], LEFT)
    return t


def lab_ep(): return rowlab("ep", "ependymal cells", GREY)
def lab_B(): return rowlab("B", "B cells\nastrocyte-like", STEM)
def lab_C(): return rowlab("C", "C cells\nfast-dividing", GREY)
def lab_A(): return rowlab("A", "A cells\nyoung neurons", BLUE)


def shade(key):
    return Rectangle(width=9.6, height=1.5, fill_color=BG, fill_opacity=0.68, stroke_width=0).move_to([-1.7, RY[key], 0])


def ventricle_label():
    return T("ventricle", 26, GREY).move_to([-2.2, 3.1, 0])


def question_frame():
    """The frame held while the question is on screen (s08, s09)."""
    ep, B, C, A = make_wall(C_X8, A_X4)
    labs = VGroup(lab_ep(), lab_B(), lab_C(), lab_A())
    qs = VGroup(*[qmark().move_to([2.85, RY[k], 0]) for k in ("ep", "B", "C", "A")])
    top = T("Which cells survive?", 34, YELLOW).move_to([-1.7, 3.3, 0])
    bot = T("Which one rebuilds the zone?", 34, YELLOW).move_to([-1.7, -3.45, 0])
    return VGroup(ep, B, C, A, labs, qs, top, bot)


def regen_frame():
    """End state of s11 (and the beat that follows)."""
    ep, B, C, A = make_wall(C_X8, A_X4)
    labs = VGroup(lab_ep(), lab_B(), lab_C(), lab_A())
    ars = VGroup(arrow([2.85, 0.05, 0], [2.85, -0.85, 0], STEM), arrow([2.85, -1.45, 0], [2.85, -2.3, 0], BLUE))
    return VGroup(ep, B, C, A, labs, ars)


# ================================================================== SCENES
class S00Title(TitleCard):
    LESSON = "Two Places the Adult Brain Still Makes Neurons"
    TITLE = "Who Makes Them, and How Many Are Kept"

    def construct(self):
        title=T("Who Makes Them,\nand How Many Are Kept",44,font=TITLE_FONT,line_spacing=1.1).move_to([0,.65,0])
        rule=Line([-2.2,-.6,0],[2.2,-.6,0],color=GOLD,stroke_width=4)
        sub=T(self.LESSON,26,GREY).move_to([0,-1.25,0])
        brand=T("BIOCHEMISTRYPEDIA",26,TEAL).move_to([0,2.65,0])
        self.add(title,rule,sub,brand)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        br = brain()
        self.add(br, T("Which cell makes them?", 34, STEM).move_to([0, 2.85, 0]))
        self.at("adult rodents")
        nr = neuron(0.5).move_to([1.5, 0.45, 0])
        self.at("new neurons")
        self.play(FadeIn(nr, scale=0.5), run_time=0.7)
        box = VGroup(RoundedRectangle(corner_radius=0.15, width=1.2, height=1.2, color=STEM, stroke_width=4),
                     qmark(64).move_to([0, 0, 0])).move_to([-1.6, 0.45, 0])
        ar = arrow([-0.9, 0.45, 0], [0.7, 0.45, 0], STEM)
        top = T("Which cell makes them?", 34, STEM).move_to([0, 3.3, 0])
        self.at("which cell makes them")
        self.play(FadeIn(box), GrowArrow(ar), run_time=0.6)
        row = VGroup(*[neuron(0.28).scale(0.8).move_to([-2.3 + 1.0 * i, -1.35, 0]) for i in range(5)])
        bot = T("How many are kept?", 34, YELLOW).move_to([-2, -2.85, 0])
        self.at("how many are kept")
        self.play(FadeIn(row, lag_ratio=0.2), FadeIn(bot), run_time=0.9)
        self.finish()


class S02P1(SpokenScene):
    def construct(self):
        br = brain()
        lu = lumen()
        self.add(br, lu)
        sites = [Circle(radius=0.55, color=TEXT, stroke_width=5).move_to(p) for p in (VENT, DGC)]
        self.at("two places")
        self.play(*[FadeIn(s, scale=1.4) for s in sites], run_time=0.5)
        self.play(*[FadeOut(s) for s in sites], run_time=0.6)
        ring = svz_ring()
        sl = T("subventricular zone", 26, TEXT).move_to([-0.8, 1.9, 0])
        l1 = Line([-1.5, 1.62, 0], [-1.6, 1.12, 0], color=TEXT, stroke_width=3)
        self.at("subventricular zone")
        self.play(Create(ring), FadeIn(sl), Create(l1), run_time=0.9)
        vl = T("lateral ventricle", 26, GREY).move_to([-1.6, -1.25, 0])
        l2 = Line([-1.6, -0.95, 0], [-1.6, -0.2, 0], color=GREY, stroke_width=3)
        self.at("wall of the lateral")
        self.play(FadeIn(vl), Create(l2), Indicate(ring, color=TEXT, scale_factor=1.05), run_time=0.9)
        self.finish()


class S03P2(SpokenScene):
    def construct(self):
        br, lu, ring = brain(), lumen(), svz_ring()
        sl = T("subventricular zone", 26, TEXT).move_to([-0.8, 1.9, 0])
        l1 = Line([-1.5, 1.62, 0], [-1.6, 1.12, 0], color=TEXT, stroke_width=3)
        self.add(br, lu, ring, sl, l1, STREAM.copy().set_stroke(BLUE, 6),
                 T("rostral migratory stream", 26, BLUE).move_to([-3.2, -2.65, 0]))
        dots = stream_dots(6)
        for d in dots:
            d.move_to(STREAM.get_start())
        self.at("its young neurons")
        self.play(FadeIn(dots[0], scale=0.4), run_time=0.4)
        self.at("migrate forward")
        self.add(*dots)
        anims = [MoveAlongPath(d, STREAM.get_subcurve(0, 1 - 0.075 * k), rate_func=linear) for k, d in enumerate(dots)]
        self.play(LaggedStart(*anims, lag_ratio=0.22), run_time=2.2)
        bl = T("olfactory bulb", 26, BLUE).move_to([-5.0, -1.75, 0])
        self.at("olfactory bulb")
        self.play(FadeIn(bl), Indicate(br[2], color=BLUE, scale_factor=1.12), run_time=0.8)
        self.finish()


class S04P3(SpokenScene):
    def construct(self):
        br=brain(); dg=dg_arc(.65,n=8,dot_r=.08).move_to([1.8,-.25,0])
        title=T("dentate gyrus",30,PURPLE).move_to([2,1.35,0])
        hip=T("hippocampus",28,PURPLE).move_to([4,-2.65,0])
        self.add(br)
        self.at("dentate gyrus")
        self.play(FadeIn(dg),FadeIn(title),run_time=.45)
        self.at("hippocampus")
        self.play(FadeIn(hip),Create(Line([3.5,-2.3,0],[2.7,-.8,0],color=PURPLE)),run_time=.35)
        self.at("there the rate")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.clear()
        ax=Axes(x_range=[0,1,.25],y_range=[0,1,.25],x_length=10,y_length=5.0,
            axis_config={"include_tip":False,"include_ticks":False,"stroke_color":GREY}).move_to([.45,-.15,0])
        # Qualitative exponential model, no measured ages or counts implied.
        curve=ax.plot(lambda age:.05+.95*np.exp(-age/.2),x_range=[0,1],color=BLUE,stroke_width=7)
        labels=VGroup(T("new neurons made",30,BLUE).move_to([0,3.1,0]),
            T("age",30).move_to([.45,-3.1,0]),T("schematic · dentate gyrus",26,PURPLE).move_to([2,2.1,0]))
        self.add(ax,labels)
        self.at("falls steeply")
        self.play(Create(curve),run_time=.8)
        self.wait(3.0)
        self.finish()


class S05Cells1(SpokenScene):
    def construct(self):
        ep, B, C, A = make_wall(C_X5, A_X6)
        vent = ventricle_label()
        self.at("four kinds")
        self.play(FadeIn(vent), LaggedStart(*[FadeIn(g, shift=UP * 0.12) for g in (ep, B, C, A)], lag_ratio=0.55), run_time=2.3)
        sB, sC, sA = shade("B"), shade("C"), shade("A")
        le = lab_ep()
        self.at("ependymal cells line")
        self.play(FadeIn(le), FadeIn(sB), FadeIn(sC), FadeIn(sA), run_time=0.6)
        lb = lab_B()
        self.at("astrocyte like")
        self.play(FadeIn(lb), FadeOut(sB), run_time=0.6)
        self.finish()


class S06Cells2(SpokenScene):
    def construct(self):
        ep, B, C, A = make_wall(C_X5, A_X6)
        vent = ventricle_label()
        sC, sA = shade("C"), shade("A")
        self.add(vent, ep, B, C, A, sC, sA, lab_ep(), lab_B())
        br = Brace(Line([2.5, 2.3, 0], [2.5, -0.5, 0]), direction=RIGHT, color=GREY, buff=0.1)
        rare = T("divide rarely", 30, TEXT, weight=BOLD).move_to([4.85, 1.08, 0])
        self.at("rarely")
        self.play(FadeIn(br), FadeIn(rare), run_time=0.6)
        lc = lab_C()
        self.at("fast dividing")
        self.play(FadeOut(br), FadeOut(rare), FadeOut(sC), FadeIn(lc), run_time=0.6)
        new = VGroup(*[ccell().move_to([x, RY["C"], 0]) for x in (-4.55, -2.85, -1.15, 0.55)])
        self.at("multiply")
        self.play(FadeIn(new, scale=0.3), run_time=0.7)
        self.at("young neurons")
        self.play(FadeOut(sA), run_time=0.5)
        la = lab_A()
        self.at("cells migrate")
        self.play(FadeIn(la), run_time=0.4)
        self.at("migrate away")
        gone = VGroup(A[0], A[1])
        self.play(gone.animate.shift(RIGHT * 3.8).set_opacity(0), run_time=1.0)
        self.finish()


class S07Drug(SpokenScene):
    def construct(self):
        ep,B,C,A=make_wall(C_X8,A_X4)
        self.add(ep,B,C,A,lab_ep(),lab_B(),lab_C(),lab_A())
        self.add(T("Doetsch and colleagues, 1999 · adult mouse",26,GREY).move_to([-1.3,3.2,0]))
        wash=VGroup(*[Rectangle(width=9,height=1.05,stroke_width=0,fill_color=RED,
            fill_opacity=op).move_to([-1.8,RY[k],0]) for k,op in [("ep",.04),("B",.04),("C",.33),("A",.33)]])
        streams=VGroup(*[arrow([-6,y,0],[2,y,0],RED,3) for y in [-.8,-1.6,-2.4]])
        self.at("infused adult")
        self.play(FadeIn(wash,shift=RIGHT),LaggedStart(*[GrowArrow(a) for a in streams],lag_ratio=.15),run_time=1)
        tag=T("drug: kills cells copying DNA",28,RED).move_to([0,-3.45,0])
        self.at("kills cells copying")
        self.play(FadeIn(tag),run_time=.3)
        self.at("then stopped")
        self.play(FadeOut(wash,shift=RIGHT),FadeOut(streams,shift=RIGHT),FadeOut(tag),run_time=.35)
        self.add(T("STOP · wash removed",30,RED).move_to([0,-3.45,0]))
        self.finish()


class S08Pred(SpokenScene):
    def construct(self):
        ep, B, C, A = make_wall(C_X8, A_X4)
        labs = VGroup(lab_ep(), lab_B(), lab_C(), lab_A())
        self.add(ep, B, C, A, labs)
        top = T("Pause and predict", 34, YELLOW).move_to([-1.7, 3.3, 0])
        self.at("pause and predict")
        self.play(FadeIn(top), run_time=0.5)
        qs = VGroup(*[qmark().move_to([2.85, RY[k], 0]) for k in ("ep", "B", "C", "A")])
        top2 = T("Which cells survive?", 34, YELLOW).move_to([-1.7, 3.3, 0])
        self.at("which cells survive")
        self.play(ReplacementTransform(top, top2), LaggedStart(*[FadeIn(q, scale=0.4) for q in qs], lag_ratio=0.1), run_time=0.4)
        bot = T("Which one rebuilds the zone?", 34, YELLOW).move_to([-1.7, -3.45, 0])
        self.at("which one rebuilds")
        self.play(FadeIn(bot), run_time=0.6)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        self.add(question_frame())
        self.finish()


class S10Rev1(SpokenScene):
    def construct(self):
        ep, B, C, A = make_wall(C_X8, A_X4)
        labs = [lab_ep(), lab_B(), lab_C(), lab_A()]
        qs = VGroup(*[qmark().move_to([2.85, RY[k], 0]) for k in ("ep", "B", "C", "A")])
        top = T("Which cells survive?", 34, YELLOW).move_to([-1.7, 3.3, 0])
        bot = T("Which one rebuilds the zone?", 34, YELLOW).move_to([-1.7, -3.45, 0])
        self.add(ep, B, C, A, *labs, qs, top, bot)
        self.play(FadeOut(qs), FadeOut(top), FadeOut(bot), run_time=0.4)
        self.at("fast dividers")
        self.play(C.animate.set_color(RED), run_time=0.4)
        self.play(FadeOut(C), FadeOut(labs[2]), run_time=0.5)
        self.at("most neuroblasts")
        dying = VGroup(A[0], A[1], A[2])
        self.play(dying.animate.set_color(RED), run_time=0.3)
        self.play(FadeOut(dying), run_time=0.5)
        self.at("rare dividers")
        checks=VGroup(*[T("✓",36,GREEN).move_to([2.65,RY[k],0]) for k in ("ep","B")])
        tag=T("survived: divide rarely",30,GREEN).move_to([-1.5,3.25,0])
        self.play(FadeIn(checks),FadeIn(tag),run_time=.35)
        self.finish()


class S11Rev2(SpokenScene):
    def construct(self):
        ep,B,C,A=make_wall(C_X8,A_X4)
        self.add(ep,B,A[3],lab_ep(),lab_B(),lab_A())
        tag=T("ependymal cells: did not rebuild the zone",26,GREY).move_to([-1,3.25,0])
        self.add(tag)
        self.at("astrocyte like")
        self.play(*[b[1][1].animate.set_fill(STEM,1) for b in B],
            *[Indicate(b,color=STEM,scale_factor=1.16) for b in B],run_time=.65)
        self.at("divided", lead=.1)
        # A B cell leaves a B daughter in place and produces a C daughter.
        first=C[0]
        split = VGroup(cell(.35,STEM).move_to(B[0].get_center()+[-.24,0,0]),
            cell(.35,GREY).move_to(B[0].get_center()+[.24,0,0]))
        parent=B[0].copy()
        self.play(Transform(B[0],split),run_time=.25)
        self.play(Transform(B[0],parent),TransformFromCopy(split[1],first),run_time=.55)
        self.add(arrow(B[0].get_bottom(),first.get_top(),STEM),
            T("B → B + C",28,STEM).move_to([-1,-3.45,0]))
        self.at("precursors came back")
        self.play(*[TransformFromCopy(B[min(i//2,3)],C[i]) for i in range(1,9)],FadeIn(lab_C()),run_time=.65)
        self.at("then neuroblasts")
        self.play(*[TransformFromCopy(C[2*i+1],A[i]) for i in range(3)],run_time=.6)
        self.at("normal order")
        self.play(GrowArrow(arrow([2.85,.05,0],[2.85,-.85,0],STEM)),
            GrowArrow(arrow([2.85,-1.45,0],[2.85,-2.3,0],BLUE)),run_time=.5)
        self.finish()


class S12Beat(NarratedScene):
    def construct(self):
        self.add(regen_frame())
        self.finish()


class S13Proof(SpokenScene):
    def construct(self):
        # Reuse the preceding chapter's actual card and slot geometry.
        card=RoundedRectangle(corner_radius=.3,width=8.7,height=6.5,stroke_color=GREY,stroke_width=3,
            fill_color=GREY,fill_opacity=.06).move_to([-2.05,.2,0])
        head=T("A neuron counts as new only when",28).move_to([-2.05,2.7,0])
        slots=VGroup(*[RoundedRectangle(corner_radius=.15,width=3.5,height=2.7,color=col,stroke_width=3).move_to([x,.5,0])
            for x,col in [(-4.05,YELLOW),(-.05,GREEN)]])
        self.add(card,head,slots)
        candidate=bcell(1.0).move_to([4.4,.5,0])
        self.at("leading candidate")
        self.play(FadeIn(candidate),FadeIn(T("candidate",28,STEM).move_to([4.4,-1.1,0])),run_time=.4)
        self.at("not yet proof")
        self.add(T("not yet proof",30,YELLOW).move_to([4.4,2.45,0]))
        self.at("inherited label")
        birth=T("birth record\nor inherited label",27,YELLOW).move_to([-4.05,.7,0])
        self.play(FadeIn(birth),run_time=.35)
        self.at("neurons descend")
        self.add(T("from an\nastrocyte-like cell",26,STEM).move_to([-4.05,-.3,0]))
        self.at("same cells")
        self.play(FadeIn(T("in the same cells",30).move_to([-2.05,-1.9,0])),
            FadeIn(T("neuron identity",28,GREEN).move_to([-.05,.7,0])),run_time=.4)
        self.add(Line([-5.9,-1.25,0],[1.8,-1.25,0],color=TEXT,stroke_width=4))
        self.finish()


class S14Virus(SpokenScene):
    def construct(self):
        body=cell(2.75,GREY,.58).move_to([.4,.2,0])
        chrom=RoundedRectangle(width=2.3,height=.38,corner_radius=.1,color=TEXT,fill_color=GREY,fill_opacity=.6).move_to([.4,.2,0])
        v=virus(.65).move_to([-4.7,1.4,0])
        vl=T("retrovirus",28,INDIGO).move_to([-4.7,2.65,0])
        gene=Rectangle(width=.65,height=.38,stroke_width=0,fill_color=YELLOW,fill_opacity=1).move_to(v)
        self.add(body,chrom,v,gene,vl)
        self.at("writes its genes")
        self.play(v.animate.move_to([-.65,.6,0]),gene.animate.move_to([-.65,.6,0]),run_time=.8)
        self.at("chromosome", lead=.25)
        self.play(gene.animate.move_to(chrom),chrom.animate.set_fill(YELLOW,1).set_stroke(YELLOW),
            FadeOut(v),FadeOut(vl),run_time=.45)
        self.add(T("chromosome",30).move_to([4.8,-.85,0]),Line([3.8,-.65,0],[1.6,.2,0],color=TEXT))
        self.at("dividing cell")
        def marked(x,y):
            c=cell(.6,GREY,.5).move_to([x,y,0])
            return VGroup(c,Rectangle(width=.4,height=.15,stroke_width=0,fill_color=YELLOW,fill_opacity=1).move_to(c))
        top=marked(0,2.55); mid=VGroup(*[marked(x,.6) for x in [-2.8,2.8]])
        low=VGroup(*[marked(x,-1.6) for x in [-4.4,-1.5,1.5,4.4]])
        lines=VGroup(*[Line(top.get_bottom(),c.get_top(),color=GREY) for c in mid],
            *[Line(mid[i//2].get_bottom(),c.get_top(),color=GREY) for i,c in enumerate(low)])
        self.play(Transform(body,top),
            *[FadeOut(m) for m in list(self.mobjects) if m is not body],run_time=.25)
        self.remove(body)
        self.add(top)
        self.play(*[TransformFromCopy(top,c) for c in mid],
            Create(VGroup(*lines[:2])),run_time=.5)
        self.at("so every")
        self.at("descendant inherits")
        self.play(Create(VGroup(*lines[2:])),
            *[TransformFromCopy(mid[i//2],c) for i,c in enumerate(low)],run_time=.65)
        self.add(T("gene passed to every descendant",30,YELLOW).move_to([0,-3,0]))
        self.finish()


class S15Virus2(SpokenScene):
    def construct(self):
        xs=[-4.4,0,4.4]
        cells=VGroup(cell(1.45,GREY).move_to([xs[0],-.6,0]),cell(1.45,GREY).move_to([0,-.6,0]),bcell(1.7).move_to([xs[2],-.6,0]))
        labels=VGroup(*[T(t,30,col).move_to([x,-2.7,0]) for x,t,col in zip(xs,["no GFAP","no GFAP","makes GFAP"],[GREY,GREY,STEM])])
        rec=RoundedRectangle(width=.4,height=.5,corner_radius=.06,stroke_width=0,fill_color=ORANGE,fill_opacity=1).move_to([4.4,.65,0])
        v=virus(.6).move_to([-4.4,2.5,0])
        self.add(cells,labels,v)
        self.at("one receptor")
        self.add(rec,T("one receptor",30,ORANGE).move_to([3.8,3.1,0]))
        self.play(v.animate.move_to([-4.4,1.45,0]),run_time=.4)
        self.play(v.animate.move_to([-3.7,2.5,0]),run_time=.25)
        self.at("mice were engineered")
        self.play(v.animate.move_to([0,1.45,0]),run_time=.6)
        self.play(v.animate.move_to([.7,2.5,0]),run_time=.3)
        self.at("only in cells")
        self.play(v.animate.move_to([4.4,1.45,0]),run_time=.65)
        self.play(Indicate(rec,color=ORANGE),run_time=.4)
        self.finish()


# ----------------------------------------------------------------- s16 helpers
S16Y = 0.6
S16X = [-5.0, -1.7, 1.7, 5.0]


def s16_stage2():
    B=bcell(1.3).move_to([-5,.4,0]); nuc=Dot(B[1][1].get_center(),radius=.18,color=YELLOW)
    bulb=Circle(radius=1.65,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.12).move_to([4.6,.35,0])
    bl=T("olfactory bulb",28).move_to([4.6,-2.15,0])
    st=CubicBezier([-.1,.4,0],[1,1.4,0],[2.1,1.4,0],[3.8,.4,0],color=BLUE,stroke_width=5)
    tip=arrow(st.point_from_proportion(.8),st.point_from_proportion(1),BLUE)
    labels=VGroup(T("astrocyte-like B cell",26,STEM).move_to([-4.6,-1.6,0]),
        T("rostral migratory stream",28,BLUE).move_to([.8,2.25,0]),tip)
    C=ccell().scale(1.4).move_to([-2.7,.4,0]); A=acell().scale(1.5).move_to([-.9,.4,0])
    labels.add(C,A,Dot(C[1].get_center(),radius=.16,color=YELLOW),
        Dot(A[0][1].get_center(),radius=.15,color=YELLOW),
        T("C precursor",24,GREY).move_to([-2.7,-.75,0]),
        T("A neuroblast",24,BLUE).move_to([-.65,-.75,0]),
        arrow([-3.7,.4,0],[-3.25,.4,0],STEM),arrow([-2.1,.4,0],[-1.55,.4,0],BLUE))
    return B,nuc,bulb,bl,st,labels


class S16Virus3(SpokenScene):
    def construct(self):
        ep=epcell().scale(2).move_to([-5,.5,0]); B=bcell(1.5).move_to([-1.7,.5,0])
        C=cell(.8,GREY).move_to([1.7,.5,0]); A=acell().scale(2).move_to([5,.5,0])
        labs=VGroup(*[T(t,28,col).move_to([x,-1.5,0]) for x,t,col in zip(S16X,["ependymal","B cell","C cell","A cell"],[GREY,STEM,GREY,BLUE])])
        self.add(ep,B,C,A,labs,T("untreated mice",32).move_to([0,3.2,0]))
        self.at("only astrocyte like")
        self.play(Indicate(B,color=STEM,scale_factor=1.1),run_time=.35)
        marker=Dot(B[1][1].get_center(),radius=.2,color=YELLOW)
        self.at("were infected")
        self.add(marker,T("infected: carries the marker",28,YELLOW).move_to([-1.7,-2.5,0]))
        self.at("later")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.2)
        self.clear()
        B,nuc,bulb,bl,path,labels=s16_stage2()
        self.add(B,nuc,bulb,bl,path,*labels[:3])
        self.play(TransformFromCopy(VGroup(B,nuc),VGroup(*labels[3:7:2])),
            FadeIn(labels[7]),GrowArrow(labels[9]),run_time=.3)
        self.play(TransformFromCopy(VGroup(labels[3],labels[5]),VGroup(labels[4],labels[6])),
            FadeIn(labels[8]),GrowArrow(labels[10]),run_time=.3)
        chain=VGroup(*[VGroup(Dot(radius=.22,color=BLUE),Dot(radius=.1,color=YELLOW)).move_to(path.get_start()) for _ in range(5)])
        self.at("marker turned up")
        self.play(LaggedStart(*[MoveAlongPath(c,path,rate_func=linear) for c in chain],lag_ratio=.14),run_time=1.1)
        self.remove(*chain)
        nn=neuron(.78).move_to([4.6,.5,0]); mk=Dot(nn[0][1].get_center(),radius=.17,color=YELLOW)
        self.add(nn,mk,T("new neuron · carries the marker",30,YELLOW).move_to([0,-3,0]))
        self.finish()


class S17Beat(NarratedScene):
    def construct(self):
        self.add(*s16_stage2())
        nn=neuron(.78).move_to([4.6,.5,0])
        self.add(nn,Dot(nn[0][1].get_center(),radius=.17,color=YELLOW),
            T("new neuron · carries the marker",30,YELLOW).move_to([0,-3,0]))
        self.finish()


class S18Dg(SpokenScene):
    def construct(self):
        div=Line([0,3.4,0],[0,-3.4,0],color=GREY)
        B=bcell(1.4).move_to([-4.8,1.1,0])
        C=cell(.8,GREY).move_to([-2,1.1,0])
        A=neuron(.5).scale(.85).move_to([-2,-1.9,0])
        self.add(div,B,C,A,T("ventricle wall",28).move_to([-3.5,3.3,0]),
            T("astrocyte-like\nB cell",28,STEM).move_to([-4.8,-1.2,0]),
            T("C precursor",26,GREY).move_to([-2,2.4,0]),
            T("A neuroblast",26,BLUE).move_to([-2,-3.4,0]),
            arrow([-3.4,1.1,0],[-2.9,1.1,0],STEM),arrow([-2,.2,0],[-2,-.65,0],BLUE),
            T("dentate gyrus",28,PURPLE).move_to([3.4,3.3,0]))
        dg=dg_arc(2.2,n=13,dot_r=.12,width=32)
        dg.shift(np.array([3.4,-.25,0])-dg[0].get_arc_center())
        self.at("the dentate gyrus")
        self.play(FadeIn(dg),run_time=.5)
        ctr=dg[0].get_arc_center()
        stem=bcell(.85).move_to(ctr+[0,1.2,0])
        radial=Line(ctr+[0,1.5,0],ctr+[0,2.0,0],color=STEM,stroke_width=8)
        self.at("radial")
        self.play(FadeIn(stem),Create(radial),run_time=.4)
        self.add(T("radial,\nastrocyte-like\nstem cell",28,STEM).move_to(ctr+[0,-.4,0]))
        self.at("stem cells")
        self.add(T("granule layer",28,PURPLE).move_to([3.4,-3.0,0]),
            Line([2.3,-2.7,0],[1.7,-1.85,0],color=PURPLE))
        self.wait(3.0)
        self.finish()


# ----------------------------------------------------------------- s19-s20 helpers
GX = [-4.5, -2.7, -0.9, 0.9, 2.7, 4.5]
GY = [2.2, 0.9, -0.4, -1.7]
KEEP = [8, 11, 12, 15, 19, 22]
_rng = np.random.RandomState(3)
_others = [i for i in range(24) if i not in KEEP]
ORDER = list(_rng.permutation(_others))
DEATH = {idx: -3.0 * np.log(1 - (j + 0.5) / 18.0) for j, idx in enumerate(ORDER)}


def gpos(i):
    return np.array([GX[i % 6], GY[i // 6], 0])


AX_Y = -2.85
AX_X0, AX_X1 = -5.0, 5.0


def tx(t):
    return AX_X0 + (AX_X1 - AX_X0) * t / 28.0


def time_axis():
    line = Line([AX_X0, AX_Y, 0], [AX_X1, AX_Y, 0], color=GREY, stroke_width=4)
    brk = Line([tx(7), AX_Y - 0.14, 0], [tx(7), AX_Y + 0.14, 0], color=GREY, stroke_width=3)
    first = Line([tx(0), AX_Y - 0.28, 0], [tx(7), AX_Y - 0.28, 0], color=YELLOW, stroke_width=5)
    l1 = T("first days", 26, YELLOW).move_to([tx(3.5), AX_Y - 0.65, 0])
    l0 = T("birth", 26, GREY).move_to([tx(0) - 0.3, AX_Y + 0.55, 0])
    l2 = T("weeks", 26, GREY).move_to([tx(26), AX_Y - 0.65, 0])
    return VGroup(line, brk, first, l1, l0, l2), l1


class S19Kept(SpokenScene):
    def construct(self):
        sch = T("schematic, not counts or measured fraction", 26, GREY).move_to([0, 3.4, 0])
        dots = VGroup(*[Dot(gpos(i), radius=0.24, color=BLUE) for i in range(24)])
        axg, l1 = time_axis()
        cur = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.18).rotate(PI)
        tr = ValueTracker(0)
        cur.add_updater(lambda m: m.move_to([tx(tr.get_value()), AX_Y + 0.28, 0]))
        cur.move_to([tx(0), AX_Y + 0.28, 0])
        for i, d in enumerate(dots):
            if i in KEEP:
                continue
            td = DEATH[i]

            def upd(m, td=td):
                t = tr.get_value()
                if t < td:
                    return
                f = min(1.0, (t - td) / 1.0)
                m.set_color(RED)
                m.set_opacity(1 - f)
            d.add_updater(upd)
        self.add(sch,dots,axg,cur)
        self.at("how many are kept")
        self.at("many newborn cells")
        self.play(tr.animate.set_value(7), run_time=2.0, rate_func=linear)
        self.at("first days")
        self.add(T("kept",30,BLUE).move_to([0,2.9,0]))
        self.play(Indicate(l1, color=YELLOW, scale_factor=1.15), tr.animate.set_value(28), run_time=.6, rate_func=linear)
        keep = VGroup(*[dots[i] for i in KEEP])
        self.play(Indicate(keep, color=BLUE, scale_factor=1.2), run_time=0.4)
        self.finish()


def kept_neurons():
    return VGroup(*[neuron(0.3).scale(0.85).move_to(gpos(i)) for i in KEEP])


class S20Act(SpokenScene):
    def construct(self):
        positions=[[-4.4,1.5,0],[0,1.5,0],[4.4,1.5,0],[-4.4,-1.1,0],[0,-1.1,0],[4.4,-1.1,0]]
        nrs=VGroup(*[neuron(.48).scale(.95).move_to(p) for p in positions])
        self.add(nrs,T("kept",30,BLUE).move_to([0,-3.35,0]))
        self.at("while they mature")
        self.play(*[Indicate(n,color=BLUE,scale_factor=1.05) for n in nrs],run_time=.5)
        self.at("survival also depends")
        self.add(T("incoming input",30,LIGHT).move_to([0,3.35,0]))
        for n in nrs:
            endpoint=n[1][0].get_end()
            start=endpoint+[-.8,.25,0]
            pulse=Dot(start,radius=.13,color=LIGHT)
            self.add(arrow(start,endpoint,LIGHT,4),pulse)
            self.play(pulse.animate.move_to(endpoint),n[0][1].animate.set_fill(LIGHT,1),run_time=.14)
            self.remove(pulse)
        self.at("their own activity")
        self.play(*[Indicate(n[0][1],color=LIGHT,scale_factor=1.2) for n in nrs],run_time=.5)
        self.finish()


class S20bNmda(SpokenScene):
    def construct(self):
        cred = T("Tashiro and colleagues, 2006 · mouse", 26, GREY).move_to([0, 3.35, 0])
        xs = [-5.3, -2.65, 0.0, 2.65, 5.3]
        YN = 0.6
        nrs = VGroup(*[neuron(0.6).scale(0.85).move_to([x, YN, 0]) for x in xs])

        def rblock(x, a):
            return RoundedRectangle(corner_radius=0.04, width=0.22, height=0.36, stroke_width=0, fill_color=ORANGE,
                                    fill_opacity=1).rotate(a - PI / 2).move_to(np.array([x, YN, 0]) + 0.64 * np.array([np.cos(a), np.sin(a), 0]))
        rec = [VGroup(*[rblock(x, a) for a in (PI / 2, 0.82 * PI, -0.12 * PI, -0.55 * PI)]) for x in xs]
        self.at("young neurons")
        self.play(FadeIn(cred), FadeIn(nrs), *[FadeIn(r) for r in rec], run_time=0.9)
        ll = T("lacks\nreceptors", 26, RED, line_spacing=0.8).move_to([xs[2], -1.55, 0])
        self.at("lacking")
        self.play(FadeOut(rec[2], shift=UP * 0.2), FadeIn(ll), run_time=0.7)
        leg = VGroup(RoundedRectangle(corner_radius=0.04, width=0.22, height=0.36, stroke_width=0, fill_color=ORANGE, fill_opacity=1),
                     T("NMDA receptor", 28, ORANGE)).arrange(RIGHT, buff=0.2).move_to([0, 3.0, 0])
        self.at("a receptor")
        self.play(FadeIn(leg), FadeOut(cred), run_time=0.5)
        keep = [T("keeps\nreceptors", 26, GREY, line_spacing=0.8).move_to([x, -1.55, 0]) for i, x in enumerate(xs) if i != 2]
        self.at("survive less well")
        self.add(*keep)
        self.play(nrs[2].animate.set_color(RED).scale(.75),run_time=.6)
        self.add(T("more likely to die",28,RED).move_to([0,-2.3,0]))
        other = T("other survival signals may help too", 30, TEXT).move_to([0, -2.9, 0])
        self.at("other survival signals")
        self.play(FadeIn(other), run_time=0.7)
        self.finish()


def timeline_row(y):
    ln = Line([-5.8, y, 0], [5.8, y, 0], color=GREY, stroke_width=4)
    xs = [-5.6, -3.2, 3.2]
    dots = VGroup(Dot([xs[0], y, 0], radius=0.15, color=YELLOW), Dot([xs[1], y, 0], radius=0.13, color=TEXT),
                  Dot([xs[2], y, 0], radius=0.13, color=TEXT))
    labs = VGroup(T("one dose", 28, YELLOW).move_to([xs[0] + 0.55, y + 0.45, 0]),
                  T("one day", 28, TEXT).move_to([xs[1], y + 0.45, 0]),
                  T("four weeks", 28, TEXT).move_to([xs[2], y + 0.45, 0]))
    brk = VGroup(Line([0, y - 0.2, 0], [-0.1, y + 0.2, 0], color=GREY, stroke_width=3),
                 Line([0.3, y - 0.2, 0], [0.2, y + 0.2, 0], color=GREY, stroke_width=3))
    return VGroup(ln, brk, dots, labs)


class S21Steps(SpokenScene):
    def construct(self):
        left=VGroup(cell(.8,GREY).move_to([-5,1.2,0]),cell(.55,GREY).move_to([-2.8,1.8,0]),
            cell(.55,GREY).move_to([-2.8,.3,0]),arrow([-4,1.2,0],[-3.5,1.2,0]),
            T("more division",32).move_to([-3.9,-.9,0]))
        right=VGroup(*[neuron(.3).scale(.65).move_to([x,1,0]) for x in [1.8,3.5,5.2]],
            T("more young cells kept",30).move_to([3.5,-.9,0]))
        self.add(T("more new neurons",36,BLUE).move_to([0,3.2,0]),left,right,T("or",36,YELLOW).move_to([0,.6,0]))
        self.at("more division")
        self.play(Indicate(left,color=TEXT,scale_factor=1.05),run_time=.4)
        self.at("more young cells kept")
        self.play(Indicate(right,color=BLUE,scale_factor=1.05),run_time=.4)
        self.at("two time points")
        self.play(FadeIn(timeline_row(-2.7)),run_time=.35)
        self.finish()


def two_boxes():
    tl = timeline_row(3.1)
    bl = RoundedRectangle(corner_radius=0.2, width=6.2, height=5.0, stroke_color=GREY, stroke_width=3).move_to([-3.3, -0.3, 0])
    br = RoundedRectangle(corner_radius=0.2, width=6.2, height=5.0, stroke_color=GREY, stroke_width=3).move_to([3.3, -0.3, 0])
    return tl, bl, br


def lab_cell(x, y, rr=0.42, marked=True, green=False):
    c = cell(rr, GREY, 0.45)
    g = VGroup(c)
    if marked:
        g.add(Dot(c[1].get_center(), radius=rr * 0.28, color=YELLOW))
    if green:
        g.add(Circle(radius=rr * 1.25, color=GREEN, stroke_width=5))
    return g.move_to([x, y, 0])


class S22Tool2(SpokenScene):
    def construct(self):
        tl = timeline_row(3.1)
        self.add(tl)
        bl = RoundedRectangle(corner_radius=0.2, width=6.2, height=5.0, stroke_color=GREY, stroke_width=3).move_to([-3.3, -0.4, 0])
        br = RoundedRectangle(corner_radius=0.2, width=6.2, height=5.0, stroke_color=GREY, stroke_width=3).move_to([3.3, -0.4, 0])

        self.at("after one dose")
        self.play(Indicate(tl[3][0], color=YELLOW, scale_factor=1.15), run_time=0.7)
        h1 = T("one day", 32, TEXT, weight=BOLD).move_to([-3.3, 1.7, 0])
        cl = VGroup(*[lab_cell(-4.9 + 1.6 * (i % 3), 0.55 - 1.4 * (i // 3), 0.55, marked=True) for i in range(5)])
        cap1 = T("index of division", 30, YELLOW).move_to([-3.3, -2.35, 0])
        self.at("one day count")
        self.add(bl,h1,cl,T("mostly dividing cells",26).move_to([-3.3,-1.65,0]))
        self.at("index of division")
        self.play(FadeIn(cap1), run_time=0.6)
        h2 = T("four weeks", 32, TEXT, weight=BOLD).move_to([3.3, 1.7, 0])
        cr = VGroup(*[lab_cell(1.7 + 1.6 * (i % 3), 0.55 - 1.4 * (i // 3), 0.55, marked=True, green=(i != 4)) for i in range(5)])
        self.at("at four weeks")
        self.add(br,h2,cr)
        cap2 = VGroup(T("BrdU + NeuN:", 28, TEXT), T("labelled cells that are neurons", 26, GREEN)).arrange(DOWN, buff=0.12).move_to([3.3, -2.25, 0])
        self.at("label plus")
        self.play(FadeIn(cap2[0]), run_time=0.5)
        self.at("counts labeled cells")
        self.play(FadeIn(cap2[1]), Indicate(VGroup(*[c for i, c in enumerate(cr) if i != 4]), color=GREEN, scale_factor=1.15), run_time=1.0)
        self.finish()


def running_prediction():
    w=wheel(1.65).move_to([-4.4,.3,0])
    m=mouse().scale(.95).move_to([-4.4,-.2,0])
    for part in m: part.set_fill(BG,1)
    m[3].set_fill(TEXT,1)
    return VGroup(T("Suppose running acts only on division",33,YELLOW).move_to([0,3.15,0]),
        w,m,T("running",30).move_to([-4.4,-1.9,0]),
        T("assume: no effect on survival",29,GREY).move_to([0,-3,0]),
        bchip("one day  ?",YELLOW,38).move_to([2.5,1.25,0]),
        bchip("four weeks  ?",YELLOW,38).move_to([2.5,-.8,0]))


class S23Pred2(SpokenScene):
    def construct(self):
        g=running_prediction()
        self.add(g[1],g[2],g[3])
        self.at("running acted only")
        self.add(g[0],g[4])
        self.at("what would you see")
        self.play(FadeIn(g[5]),FadeIn(g[6]),run_time=.35)
        self.finish()


class S24Pause(NarratedScene):
    def construct(self):
        self.add(running_prediction())
        self.finish()


class S25Rev4(SpokenScene):
    def construct(self):
        note=T("predicted pattern · later steps unchanged · not data",26,YELLOW).move_to([0,3.4,0])
        self.add(note,T("made-up numbers",26,GREY).move_to([0,2.85,0]))
        panels=[]
        # Counts and ratios computed from an explicit toy model.
        early=np.array([2000,1000]); survival=.6; late=early*survival
        for x,heading,measure,vals in [(-3.35,"one day","BrdU-labelled cells",early),(3.35,"four weeks","BrdU + NeuN cells",late)]:
            ax=Axes(x_range=[0,3,1],y_range=[0,2200,1000],x_length=4.4,y_length=3.4,
                axis_config={"include_tip":False,"include_ticks":False,"stroke_color":GREY}).move_to([x,.15,0])
            bars=VGroup(); labels=VGroup()
            for i,(v,col) in enumerate(zip(vals,[BLUE,GREY])):
                base=ax.c2p(i+1,0); top=ax.c2p(i+1,float(v))
                b=Rectangle(width=.85,height=top[1]-base[1],stroke_width=0,fill_color=col,fill_opacity=.95).move_to((top+base)/2)
                bars.add(b)
                labels.add(T(str(int(v)),28,col).move_to(top+[0,.25,0]),
                    T(["runners","controls"][i],26,col).move_to(base+[0,-.4,0]))
            ticks=VGroup(*[T(str(v),26,GREY).next_to(ax.c2p(0,v),LEFT,buff=.1) for v in [0,1000,2000]])
            panels.append(VGroup(ax,bars,labels,ticks,T(heading,30).move_to([x,2.35,0]),
                T(measure+" (count)",26).move_to([x,-2.55,0])))
        self.at("more labeled cells")
        self.add(panels[0])
        self.at("more new neurons")
        self.add(panels[1])
        self.at("same proportion")
        ratios=late/early
        self.add(T(f"late ÷ early:  {ratios[0]:.1f} = {ratios[1]:.1f}",36).move_to([0,-3.2,0]))
        self.finish()


def cage():
    box=RoundedRectangle(width=5.8,height=4.4,corner_radius=.1,color=GREY,stroke_width=4)
    bars=VGroup(*[Line([x,-2.1,0],[x,2.1,0],color=GREY,stroke_width=1).set_opacity(.3) for x in np.linspace(-2.6,2.6,9)])
    platform=Line([-.2,.25,0],[2.5,.25,0],color=GREY,stroke_width=6)
    ramp=Line([-2.3,-1.9,0],[-.2,.25,0],color=ORANGE,stroke_width=7)
    rungs=VGroup(*[Line([-2.2+.3*i,-1.8+.3*i,0],[-1.9+.3*i,-1.8+.3*i,0],color=ORANGE,stroke_width=4) for i in range(6)])
    ball=Circle(radius=.4,color=YELLOW,fill_color=YELLOW,fill_opacity=.5).move_to([1.9,-1.65,0])
    tunnel=Arc(radius=.7,start_angle=0,angle=PI,color=BLUE,stroke_width=9).move_to([-.4,-1.6,0])
    mice=VGroup(mouse().scale(.72).move_to([1.2,.65,0]),mouse().scale(.72).move_to([-1.7,1.35,0]),mouse().scale(.65).move_to([-.4,-1.75,0]))
    return VGroup(box,bars,platform,ramp,rungs,ball,tunnel,mice)


def s26_state():
    w = wheel(1.95).move_to([-4.0, 0.6, 0])
    m = mouse().scale(1.25).move_to([-4.0, 0.2, 0])
    mask=Ellipse(width=2.8,height=1.35,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([-4,.3,0])
    m=VGroup(mask,m).set_z_index(2)
    return w, m


class S26Rev5(SpokenScene):
    def construct(self):
        head = T("in these mouse studies", 28, GREY).move_to([0, 3.4, 0])
        w, m = s26_state()
        self.at("in those mouse")
        cg = cage().move_to([3.0, 0.3, 0])
        self.play(FadeIn(head), FadeIn(w), FadeIn(m), FadeIn(cg), run_time=0.6)
        rl = T("running", 30, TEXT).move_to([-4.0, -1.8, 0])
        dv = T("division", 34, TEXT, weight=BOLD).move_to([-4.0, -2.6, 0])
        self.at("running mainly raised")
        self.play(FadeIn(rl), run_time=0.4)
        self.play(Rotate(w, PI / 3), FadeIn(dv), run_time=0.7)
        el = T("enriched housing", 30, TEXT).move_to([3.0, -2.3, 0])
        self.at("enriched housing")
        self.play(Indicate(cg,color=GREY,scale_factor=1.02), FadeIn(el), run_time=0.35)
        sv = T("survival", 34, BLUE, weight=BOLD).move_to([3.0, -3.15, 0])
        self.at("raised survival")
        self.play(FadeIn(sv), run_time=0.6)
        self.finish()


class S27Beat(NarratedScene):
    def construct(self):
        head = T("in these mouse studies", 28, GREY).move_to([0, 3.4, 0])
        w, m = s26_state()
        w.rotate(PI / 3)
        rl = T("running", 30, TEXT).move_to([-4.0, -1.8, 0])
        dv = T("division", 34, TEXT, weight=BOLD).move_to([-4.0, -2.6, 0])
        cg = cage().move_to([3.0, 0.3, 0])
        el = T("enriched housing", 30, TEXT).move_to([3.0, -2.3, 0])
        sv = T("survival", 34, BLUE, weight=BOLD).move_to([3.0, -3.15, 0])
        self.add(head, w, m, rl, dv, cg, el, sv)
        self.finish()


class S28Take(SpokenScene):
    def construct(self):
        B=bcell(2.1).move_to([0,.65,0])
        label=T("the stem cell\nlooks glial",38,STEM).move_to([0,-2.3,0])
        self.add(B,label)
        born=VGroup(*[Dot([.8+.9*i,1.2,0],radius=.28,color=BLUE) for i in range(6)])
        self.at("born is not",lead=.4)
        self.play(B.animate.shift(LEFT*3.8),label.animate.shift(LEFT*3.8),run_time=.4)
        self.add(T("born",34).move_to([2.9,2.25,0]),born,T("schematic",26,GREY).move_to([3,-2.8,0]))
        self.at("same as kept")
        self.add(T("kept",34).move_to([2.9,-1.8,0]))
        self.play(*[TransformFromCopy(born[i],Dot([.8+.9*i,-.7,0],radius=.28,color=BLUE)) for i in [1,4]],run_time=.45)
        self.wait(2.5)
        self.finish()


class S29End(EndCard):
    LINE = "Stem cells look glial; born is not the same as kept."
