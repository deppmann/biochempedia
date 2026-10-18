"""Why a cell is the size it is: the surface feeds the volume  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the surface: membrane, area, supply (uptake across the surface)
  ORANGE = the volume: cytoplasm, volume, demand (use spread through the cell)
  YELLOW = the ratio, the highlighted number, the question
  TEAL   = the plant vacuole
  GREEN  = supply just meets demand
  RED    = demand exceeds supply
  GREY   = labels, guides, axes, not-the-subject
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

J, Q = 20.0, 6.0


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def cell(center, r, width=6):
    return Circle(radius=r, stroke_color=BLUE, stroke_width=width, fill_color=ORANGE, fill_opacity=0.14).move_to(center)


def dots(center, r, step=0.46, size=0.07):
    c = np.array(center, float)
    out = VGroup()
    n = int(r / step) + 1
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            p = np.array([i * step + (j % 2) * step / 2, j * step * 0.87, 0.0])
            if np.linalg.norm(p) < r - 0.28:
                out.add(Dot(c + p, radius=size, color=ORANGE))
    return out


def in_arrows(center, r, n=12, color=BLUE, out=0.85, gap=0.12):
    c = np.array(center, float)
    g = VGroup()
    for k in range(n):
        a = 2 * math.pi * k / n + 0.2
        d = np.array([math.cos(a), math.sin(a), 0.0])
        g.add(Arrow(c + d * (r + out), c + d * (r + gap), buff=0, color=color, stroke_width=5, tip_length=0.2,
                    max_tip_length_to_length_ratio=0.5))
    return g


def card(lines, color, w=5.6, sizes=None, mono=None):
    sizes = sizes or [24] * len(lines)
    mono = mono or [False] * len(lines)
    ts = VGroup(*[(M if m else T)(t, s, color if i else GREY) for i, (t, s, m) in enumerate(zip(lines, sizes, mono))])
    ts.arrange(DOWN, buff=0.16)
    box = RoundedRectangle(corner_radius=0.14, width=max(w, ts.width + 0.5), height=ts.height + 0.45, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=0.12).move_to(ts)
    return VGroup(box, ts)


def bar(x0, y, w, color, h=0.42):
    return Rectangle(width=max(w, 0.01), height=h, stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=0.55).move_to([x0 + max(w, 0.01) / 2, y, 0])


class Plot:
    """Tiny axes with no LaTeX: maps data (x, y) onto the frame."""

    def __init__(self, origin, w, h, xmax, ymax):
        self.o = np.array([origin[0], origin[1], 0.0]); self.w, self.h, self.xm, self.ym = w, h, xmax, ymax

    def p(self, x, y):
        return self.o + np.array([x / self.xm * self.w, y / self.ym * self.h, 0.0])

    def axes(self):
        xa = Line(self.o, self.o + RIGHT * self.w, color=GREY, stroke_width=3)
        ya = Line(self.o, self.o + UP * self.h, color=GREY, stroke_width=3)
        return VGroup(xa, ya)

    def curve(self, f, x0, x1, color, n=120, width=6):
        pts = [self.p(x, f(x)) for x in np.linspace(x0, x1, n)]
        m = VMobject(color=color, stroke_width=width)
        m.set_points_smoothly(pts)
        return m

    def xtick(self, x, label, size=24):
        t = T(label, size, GREY).next_to(self.p(x, 0), DOWN, buff=0.12)
        k = Line(self.p(x, 0), self.p(x, 0) + DOWN * 0.1, color=GREY, stroke_width=3)
        return VGroup(k, t)

    def ytick(self, y, label, size=22):
        t = M(label, size, GREY).next_to(self.p(0, y), LEFT, buff=0.14)
        k = Line(self.p(0, y), self.p(0, y) + LEFT * 0.1, color=GREY, stroke_width=3)
        return VGroup(k, t)


def arr_to(a, b, color):
    return Arrow(a, b, buff=0, color=color, stroke_width=4, tip_length=0.2, max_tip_length_to_length_ratio=0.5)


class S00Title(TitleCard):
    LESSON = "A measured eukaryotic cell"
    TITLE = "The surface feeds the volume"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """the puzzle: what happens when a cell grows? surface in, volume used."""

    def construct(self):
        C = np.array([0.0, -0.45, 0.0])
        head = T("Why is a cell the size it is?", 40, font=TITLE_FONT).to_edge(UP, buff=0.45)
        body = cell(C, 2.2)
        self.at("Why is a cell")
        self.play(Write(head), run_time=1.2)
        self.play(FadeIn(body, scale=0.9), run_time=0.7)

        arrows = in_arrows(C, 2.2, 12)
        surf = T("surface", 30, BLUE, weight=BOLD).move_to([-5.2, -0.45, 0])
        self.at("takes in")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06), FadeIn(surf), run_time=1.2)
        self.play(body.animate.set_stroke(YELLOW, width=9), run_time=0.3)
        self.play(body.animate.set_stroke(BLUE, width=6), run_time=0.3)

        d = dots(C, 2.2)
        vol = T("volume", 30, ORANGE, weight=BOLD).move_to([5.0, -0.45, 0])
        self.at("spread through")
        self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in d], lag_ratio=0.01), FadeIn(vol), run_time=1.6)

        q = T("?", 120, YELLOW, weight=BOLD).move_to([4.6, -0.45, 0])
        self.at("what happens")
        self.play(FadeOut(arrows), FadeOut(surf), FadeOut(vol), FadeIn(q, scale=0.5), run_time=0.5)
        self.at("as a cell")
        self.play(VGroup(body, d).animate.scale(1.28).move_to(C), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Double(SpokenScene):
    """radius 5 -> 10: area x4, volume x8, ratio halves."""

    def construct(self):
        C = np.array([-3.5, 0.1, 0.0])
        small = cell(C, 1.4)
        d_small = dots(C, 1.4, 0.42)
        lab = T("r = 5 µm", 30, YELLOW).move_to([-3.5, -3.2, 0])
        self.at("Take a hypothetical")
        self.play(FadeIn(small, scale=0.9), FadeIn(d_small), run_time=0.8)
        self.play(FadeIn(lab), run_time=0.3)

        # right panel: area and volume bars
        X0, u = 1.0, 0.55
        a_head = T("area", 28, BLUE, weight=BOLD).move_to([X0 + 0.5, 2.55, 0])
        a_base = bar(X0, 1.95, u, BLUE)
        v_head = T("volume", 28, ORANGE, weight=BOLD).move_to([X0 + 0.7, 0.55, 0])
        v_base = bar(X0, -0.05, u, ORANGE)
        ghost = DashedVMobject(Circle(radius=1.4, stroke_color=YELLOW, stroke_width=3).move_to(C), num_dashes=28)
        big = cell(C, 2.8)
        d_big = dots(C, 2.8, 0.46)
        lab10 = T("r = 10 µm", 30, YELLOW).move_to([-3.5, -3.2, 0])
        self.at("to 10")
        self.play(ReplacementTransform(small, big), ReplacementTransform(d_small, d_big), FadeIn(ghost),
                  Transform(lab, lab10), run_time=0.8)

        a_big = bar(X0, 1.95, u * 4, BLUE)
        a_num = M("314.2 → 1256.6 µm²", 24, BLUE).move_to([X0 + 2.15, 1.33, 0])
        a_x = M("×4", 32, YELLOW, weight=BOLD).move_to([X0 + u * 4 + 0.55, 1.95, 0])
        self.at("The area rises")
        self.play(FadeIn(a_head), FadeIn(a_base), run_time=0.4)
        self.play(Transform(a_base, a_big), FadeIn(a_num), FadeIn(a_x), run_time=0.8)

        v_big = bar(X0, -0.05, u * 8, ORANGE)
        v_num = M("523.6 → 4188.8 µm³", 24, ORANGE).move_to([X0 + 2.15, -0.67, 0])
        v_x = M("×8", 32, YELLOW, weight=BOLD).move_to([X0 + u * 8 + 0.55, -0.05, 0])
        self.at("The volume rises")
        self.play(FadeIn(v_head), FadeIn(v_base), run_time=0.4)
        self.play(Transform(v_base, v_big), FadeIn(v_num), FadeIn(v_x), run_time=0.8)

        f_a = M("A = 4πr²", 28, BLUE).move_to([X0 + 1.25, -1.7, 0])
        f_v = M("V = 4πr³/3", 28, ORANGE).move_to([X0 + 4.05, -1.7, 0])
        self.at("Area is 4")
        self.play(FadeIn(f_a), run_time=0.5)
        self.at("Volume is 4")
        self.play(FadeIn(f_v), run_time=0.5)

        ratio = M("A / V = 3 / r", 30, YELLOW).move_to([X0 + 2.4, -2.55, 0])
        self.at("the ratio of area")
        self.play(FadeIn(ratio, shift=UP * 0.15), run_time=0.6)
        res1 = M("0.6 µm⁻¹ at 5 µm", 26, YELLOW).move_to([X0 + 2.4, -3.2, 0])
        self.at("So the ratio halves")
        self.play(FadeIn(res1), run_time=0.5)
        res2 = M("0.3 µm⁻¹ at 10 µm", 26, YELLOW).move_to([X0 + 2.4, -3.2, 0])
        self.at("0 .3")
        self.play(Transform(res1, res2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rates(SpokenScene):
    """two made-up rates: uptake per area, use per volume."""

    def construct(self):
        C = np.array([-3.3, -0.1, 0.0])
        body = cell(C, 2.1)
        d = dots(C, 2.1, 0.44)
        self.at("Now invent two rates")
        self.play(FadeIn(body, scale=0.9), FadeIn(d), run_time=0.8)

        tag = T("made-up inputs, not measurements", 26, GREY).move_to([2.9, 2.9, 0])
        self.at("inputs, not measurements")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.6)

        arrows = in_arrows(C, 2.1, 12, out=0.75)
        cj = card(["membrane uptake, at most", "J = 20 molecules / µm² / s"], BLUE, w=5.6, sizes=[24, 26], mono=[False, True])
        cj.move_to([2.9, 1.5, 0])
        self.at("take up a nutrient")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), FadeIn(cj, shift=LEFT * 0.2), run_time=1.3)

        cq = card(["use, evenly through the volume", "q = 6 molecules / µm³ / s"], ORANGE, w=5.6, sizes=[24, 26], mono=[False, True])
        cq.move_to([2.9, -0.3, 0])
        self.at("the cell uses")
        self.play(FadeIn(cq, shift=LEFT * 0.2), LaggedStart(*[Indicate(x, color=YELLOW, scale_factor=1.6) for x in d],
                                                            lag_ratio=0.02), run_time=1.6)

        note = card(["assumed", "whole surface takes up nutrient", "nothing else limits the cell"], GREY, w=5.6, sizes=[22, 24, 24])
        note.move_to([2.9, -2.3, 0])
        self.at("Assume the whole surface")
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Balance(SpokenScene):
    """supply J*4*pi*r^2 against demand q*4*pi*r^3/3; compare at 5 and 10 micrometres."""

    def construct(self):
        P = Plot([-4.7, -2.75], 7.6, 5.4, 11.0, 32000.0)
        sup = lambda r: J * 4 * math.pi * r ** 2
        dem = lambda r: Q * 4 * math.pi * r ** 3 / 3
        ax = P.axes()
        ticks = VGroup(P.xtick(5, "5"), P.xtick(10, "10"), P.ytick(10000, "10,000"), P.ytick(20000, "20,000"),
                       P.ytick(30000, "30,000"))
        xl = T("radius (µm)", 24, GREY).move_to([P.p(11, 0)[0] - 0.2, -3.35, 0])
        yl = T("molecules per second", 24, GREY).move_to([P.p(0, 32000)[0] + 1.6, 2.95, 0])
        cs = P.curve(sup, 0, 10.8, BLUE)
        cd = P.curve(dem, 0, 10.8, ORANGE)
        leg_s = T("supply = J × area", 26, BLUE).move_to([-4.2, 2.0, 0], aligned_edge=LEFT)
        leg_d = T("demand = q × volume", 26, ORANGE).move_to([-4.2, 1.45, 0], aligned_edge=LEFT)

        self.at("Now compare supply")
        self.play(Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), run_time=0.6)
        self.play(Create(cs), FadeIn(leg_s), run_time=0.6)
        self.play(Create(cd), FadeIn(leg_d), run_time=0.6)

        def mark(r, col):
            line = DashedLine(P.p(r, 0), P.p(r, sup(r) + 3500), color=col, stroke_width=3)
            ds = Dot(P.p(r, sup(r)), radius=0.11, color=BLUE)
            dd = Dot(P.p(r, dem(r)), radius=0.11, color=ORANGE)
            return VGroup(line, ds, dd)

        PX = 4.75
        m5 = mark(5, YELLOW)
        head5 = M("r = 5 µm", 26, YELLOW).move_to([PX, 2.2, 0])
        s5 = M("supply 6,283", 22, BLUE).move_to([PX, 1.35, 0])
        d5 = M("demand 3,142", 22, ORANGE).move_to([PX, 0.7, 0])
        r5 = M("ratio 2", 30, YELLOW, weight=BOLD).move_to([PX, -0.3, 0])
        self.at("At 5 micrometers")
        self.play(Create(m5), FadeIn(head5), run_time=0.8)
        self.at("supply is 6")
        self.play(FadeIn(s5, shift=LEFT * 0.1), Indicate(m5[1], color=YELLOW, scale_factor=1.8), run_time=0.7)
        self.at("Demand is 3")
        self.play(FadeIn(d5, shift=LEFT * 0.1), Indicate(m5[2], color=YELLOW, scale_factor=1.8), run_time=0.7)
        self.at("supply is twice")
        self.play(FadeIn(r5, scale=0.8), run_time=0.6)

        m10 = mark(10, GREEN)
        head10 = M("r = 10 µm", 26, YELLOW).move_to([PX, 2.2, 0])
        eq10 = M("supply = demand", 22, GREEN).move_to([PX, 1.0, 0])
        r10 = M("ratio 1", 30, GREEN, weight=BOLD).move_to([PX, -0.3, 0])
        self.at("At 10 micrometers")
        self.play(ReplacementTransform(m5, m10), ReplacementTransform(head5, head10), FadeOut(s5), FadeOut(d5),
                  FadeOut(r5), run_time=0.9)
        self.at("only just meets")
        self.play(FadeIn(eq10, shift=LEFT * 0.1), run_time=0.5)
        self.at("exactly 1")
        self.play(FadeIn(r10, scale=0.8), run_time=0.5)

        rm = M("r = 3J / q", 26, YELLOW).move_to([PX, -1.3, 0])
        rm2 = M("3 × 20 / 6", 26, YELLOW).move_to([PX, -1.9, 0])
        rm3 = M("= 10 µm", 26, YELLOW).move_to([PX, -2.5, 0])
        self.at("keeps up")
        self.play(FadeIn(rm, shift=UP * 0.1), run_time=0.5)
        self.at("3 times 20")
        self.play(FadeIn(rm2), run_time=0.5)
        self.at("that is 10")
        self.play(FadeIn(rm3), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def rootcell(w, h, d, center, f_color=TEAL):
    outer = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=5, fill_color=ORANGE, fill_opacity=0.28).move_to(center)
    vac = Rectangle(width=w - 2 * d, height=h - 2 * d, stroke_color=f_color, stroke_width=3, fill_color=f_color,
                    fill_opacity=0.5).move_to(center)
    return outer, vac


class S05Leaves(SpokenScene):
    """what the arithmetic leaves out: shape, and the vacuole."""

    def construct(self):
        yc = 0.35
        sph = Circle(radius=1.7, stroke_color=BLUE, stroke_width=6, fill_color=ORANGE, fill_opacity=0.14).move_to([-4.7, yc, 0])
        flat = Ellipse(width=4.0, height=1.2, stroke_color=BLUE, stroke_width=6, fill_color=ORANGE, fill_opacity=0.14).move_to([-0.1, yc, 0])
        thin = RoundedRectangle(corner_radius=0.4, width=1.0, height=5.2, stroke_color=BLUE, stroke_width=6,
                                fill_color=ORANGE, fill_opacity=0.14).move_to([4.9, yc, 0])
        l1 = T("sphere", 30, GREY).move_to([-4.7, -3.1, 0])
        l2 = T("flat", 30, GREY).move_to([-0.1, -3.1, 0])
        l3 = T("long and thin", 30, GREY).move_to([4.5, -3.1, 0])
        self.at("The arithmetic leaves")
        self.play(FadeIn(sph, scale=0.9), FadeIn(l1), run_time=0.8)
        self.at("flat or long thin")
        self.play(FadeIn(flat, shift=LEFT * 0.3), FadeIn(thin, shift=LEFT * 0.3), FadeIn(l2), FadeIn(l3), run_time=1.0)
        self.at("much more surface")
        self.play(flat.animate.set_stroke(YELLOW, width=9), thin.animate.set_stroke(YELLOW, width=9), run_time=0.5)
        self.play(flat.animate.set_stroke(BLUE, width=6), thin.animate.set_stroke(BLUE, width=6), run_time=0.5)

        # phase B: the plant root cell
        CX = -3.8
        o0, v0 = rootcell(1.2, 1.2, 0.25, [CX, 0, 0])
        o1, v1 = rootcell(2.2, 5.6, 0.2, [CX, 0, 0])
        cap = T("root cell", 28, GREY).move_to([CX, -3.3, 0])
        note = T("schematic, not to scale", 22, GREY).move_to([3.4, -3.3, 0])
        vlab = T("vacuole", 30, TEAL, weight=BOLD).move_to([CX + 2.8, 0.7, 0])
        varr = arr_to([CX + 1.75, 0.7, 0], [CX + 0.35, 0.3, 0], TEAL)
        self.at("A plant vacuole")
        self.play(FadeOut(VGroup(sph, flat, thin, l1, l2, l3)), run_time=0.5)
        self.play(FadeIn(o0), FadeIn(v0), FadeIn(cap), FadeIn(note), run_time=0.8)
        self.play(FadeIn(vlab), GrowArrow(varr), run_time=0.4)
        self.at("adds volume")
        self.play(Transform(o0, o1), Transform(v0, v1), run_time=1.6)
        cyt = T("cytoplasm", 30, ORANGE, weight=BOLD).move_to([CX + 2.9, -1.0, 0])
        carr = arr_to([CX + 1.75, -1.0, 0], [CX + 1.0, -0.6, 0], ORANGE)
        self.at("cytoplasm grows")
        self.play(FadeIn(cyt), GrowArrow(carr), run_time=0.8)

        PX = 3.0
        hd = T("Arabidopsis root epidermis", 28, GREY).move_to([PX + 0.6, 2.9, 0])
        t1 = card(["whole cell volume", "about 14-fold"], YELLOW, w=4.4, sizes=[24, 30])
        t1.move_to([PX + 0.6, 1.2, 0])
        t2 = card(["space between vacuole", "and cell boundary", "about 2 to 3-fold"], ORANGE, w=4.4, sizes=[24, 24, 30])
        t2.move_to([PX + 0.6, -1.0, 0])
        self.at("In Arabidopsis")
        self.play(FadeIn(hd), run_time=0.5)
        self.at("cells grew")
        self.play(FadeIn(t1, shift=LEFT * 0.1), run_time=0.6)
        self.at("space between")
        self.play(FadeIn(t2, shift=LEFT * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """capacity to demand = 10 / r falls through 1 at 10 micrometres."""

    def construct(self):
        P = Plot([-5.6, -2.8], 11.2, 5.0, 14.0, 4.0)
        f = lambda r: 10.0 / r
        ax = P.axes()
        ticks = VGroup(P.xtick(5, "5"), P.xtick(10, "10"), P.ytick(1, "1"), P.ytick(2, "2"), P.ytick(3, "3"))
        xl = T("radius (µm)", 24, GREY).move_to([P.p(14, 0)[0] - 0.5, -3.4, 0])
        yl = T("capacity ÷ demand", 24, GREY).move_to([P.p(0, 4)[0] + 1.45, 2.45, 0])
        curve = P.curve(f, 2.6, 14, YELLOW)
        one = DashedLine(P.p(0, 1), P.p(14, 1), color=GREEN, stroke_width=3)
        short = Rectangle(width=P.p(14, 0)[0] - P.p(10, 0)[0], height=P.p(0, 1)[1] - P.p(0, 0)[1], stroke_width=0,
                          fill_color=RED, fill_opacity=0.22).move_to((P.p(10, 0) + P.p(14, 1)) / 2)
        sl = T("demand exceeds supply (in this model)", 24, RED).move_to([P.p(12, 0.5)[0] - 0.3, P.p(0, 1.9)[1], 0])
        head = T("A scaling penalty, not a universal maximum", 34, font=TITLE_FONT).to_edge(UP, buff=0.4)

        self.at("Keep the rule")
        self.play(Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), run_time=0.9)
        self.at("Supply comes in")
        s = bar(0, 0, 0.1, BLUE)  # placeholder, not shown
        sup_t = T("supply: through the surface", 28, BLUE).move_to([0.5, 1.9, 0])
        self.play(FadeIn(sup_t, shift=RIGHT * 0.2), run_time=0.6)
        dem_t = T("demand: through the volume", 28, ORANGE).move_to([0.6, 1.2, 0])
        self.at("Demand is spread")
        self.play(FadeIn(dem_t, shift=RIGHT * 0.2), run_time=0.6)
        self.at("As the radius grows")
        self.play(FadeOut(sup_t), FadeOut(dem_t), Create(curve), run_time=1.6)
        self.play(Create(one), run_time=0.5)
        self.play(FadeIn(short), FadeIn(sl), run_time=0.5)
        fm = M("10 / r", 34, YELLOW, weight=BOLD).move_to([P.p(6.5, 3.2)])
        self.at("In this model")
        self.play(FadeIn(fm, shift=DOWN * 0.1), run_time=0.6)
        self.at("scaling penalty")
        self.play(Write(head), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "A scaling penalty, not a universal maximum."
