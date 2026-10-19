"""Oxygen transport: hemoglobin loads on the flat part of an S curve and unloads on the steep part.

COLOR MAP (one color per concept, whole video)
  BLUE   = oxygen (O2 chips, oxygen amounts, the dissociation curve)
  RED    = hemoglobin and red blood cells
  GREEN  = lungs: loading, the flat part of the curve, arterial point
  YELLOW = respiring tissue: unloading, the steep part of the curve, venous point
  ORANGE = things that shift the curve right (CO2, low pH, temperature, BPG) and the shifted curve
  GOLD   = the question mark and the "in this sketch" tag
  GREY   = axes, outlines, de-emphasised text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

# plot geometry (scene units)
PX0, PY0 = -5.0, -2.35
PW, PH = 7.2, 4.5
XMAX = 110.0
SX = PW / XMAX
PANEL_X = 4.6          # centre of the right-hand panel


def px(p):
    return PX0 + p * SX


def py(s):
    return PY0 + s * PH


def hill(p, p50, n=3.05):
    """In this sketch only: a Hill-type S curve with the given P50."""
    p = np.asarray(p, float)
    return p ** n / (p ** n + p50 ** n)


P50_BASE, P50_SHIFT = 27.9, 37.5   # shifted value is arbitrary, drawn only as a sketch of a right shift


def curve(p50, color=BLUE, w=6, p_hi=108.0):
    ps = np.linspace(0, p_hi, 140)
    pts = [[px(p), py(float(hill(p, p50))), 0] for p in ps]
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_smoothly(pts)
    return m


def dot(p, p50, color, r=0.13):
    return Dot([px(p), py(float(hill(p, p50))), 0], radius=r, color=color)


def band(lo, hi, color, op=0.13):
    return Rectangle(width=(hi - lo) * SX, height=PH * 1.0, stroke_width=0, fill_color=color,
                     fill_opacity=op).move_to([px((lo + hi) / 2), py(0.5), 0])


def axes(title=True):
    g = VGroup()
    g.add(Line([PX0, PY0, 0], [px(XMAX), PY0, 0], color=GREY, stroke_width=3))
    g.add(Line([PX0, PY0, 0], [PX0, py(1.0) + 0.2, 0], color=GREY, stroke_width=3))
    for p in range(0, 101, 20):
        g.add(Line([px(p), PY0, 0], [px(p), PY0 - 0.1, 0], color=GREY, stroke_width=3))
        g.add(M(str(p), 22, GREY).move_to([px(p), PY0 - 0.38, 0]))
    for s in (0, 50, 100):
        g.add(Line([PX0, py(s / 100), 0], [PX0 - 0.1, py(s / 100), 0], color=GREY, stroke_width=3))
        g.add(M(str(s), 22, GREY).move_to([PX0 - 0.45, py(s / 100), 0]))
    g.add(T("PO2 (mmHg)", 24, GREY).move_to([px(55), PY0 - 0.85, 0]))
    g.add(T("saturation (%)", 24, GREY).rotate(PI / 2).move_to([PX0 - 1.05, py(0.5), 0]))
    return g


def sketch_title(txt="Adult human blood, in this sketch"):
    return T(txt, 26, GOLD).move_to([-2.4, 3.05, 0])


def o2chip(size=22, r=0.24):
    c = Circle(radius=r, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35)
    return VGroup(c, T("O2", size, TEXT).move_to(c))


class S00Title(TitleCard):
    LESSON = "Carrying oxygen and carbon dioxide"
    TITLE = "Hemoglobin loads flat, unloads steep"


# ---------------------------------------------------------------------------------------------
class S01Gap(SpokenScene):
    def construct(self):
        head = T("Oxygen carried by one litre, in an adult human", 30, font=TITLE_FONT).move_to([0, 3.1, 0])
        base = -2.6
        h_blood = 4.2
        h_plasma = h_blood * 3 / 200
        xb, xp = -3.0, 3.0
        base_line = Line([-5.5, base, 0], [5.5, base, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(head), Create(base_line), run_time=0.8)
        self.at("carries about")
        blood = Rectangle(width=1.8, height=h_blood, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                          fill_opacity=0.45).move_to([xb, base + h_blood / 2, 0])
        bl_lbl = T("arterial blood", 26, RED).move_to([xb, base - 0.45, 0])
        bl_val = T("about 200 mL of oxygen", 26, BLUE).move_to([xb, base + h_blood + 0.4, 0])
        self.play(GrowFromEdge(blood, DOWN), FadeIn(bl_lbl), run_time=1.0)
        self.play(FadeIn(bl_val, shift=UP * 0.1), run_time=0.5)
        self.at("plasma alone")
        plasma = Rectangle(width=1.8, height=h_plasma, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                           fill_opacity=0.45).move_to([xp, base + h_plasma / 2, 0])
        pl_lbl = T("plasma alone", 26, GREY).move_to([xp, base - 0.45, 0])
        pl_val = T("about 3 mL of oxygen", 26, BLUE).move_to([xp, base + 0.6, 0])
        self.play(GrowFromEdge(plasma, DOWN), FadeIn(pl_lbl), run_time=0.6)
        self.play(FadeIn(pl_val, shift=UP * 0.1), run_time=0.5)
        self.at("dissolves poorly")
        water = T("oxygen dissolves poorly in water", 28, GREY).move_to([xp, base + 1.7, 0])
        self.play(FadeIn(water), run_time=0.6)
        self.at("make up the difference")
        brace = Line([xb + 1.2, base + h_blood - 0.6, 0], [xp - 1.2, base + h_blood - 0.6, 0], color=GOLD,
                     stroke_width=4)
        qm = T("?", 90, GOLD, weight=BOLD).move_to([0, base + h_blood / 2 + 0.5, 0])
        gap_lbl = T("the gap", 28, GOLD).next_to(qm, UP, buff=0.15)
        self.play(FadeIn(qm, scale=0.5), FadeIn(gap_lbl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Carrier(SpokenScene):
    def construct(self):
        xs = [-3.3, -1.1, 1.1, 3.3]
        cy = -0.2
        cell = RoundedRectangle(corner_radius=0.6, width=11.4, height=5.0, stroke_color=RED, stroke_width=4,
                                fill_color=RED, fill_opacity=0.07).move_to([0, 0.1, 0])
        cell_lbl = T("red blood cell", 28, RED).move_to([-3.9, 2.1, 0])
        chains = VGroup(*[RoundedRectangle(corner_radius=0.2, width=1.9, height=2.0, stroke_color=RED,
                                           stroke_width=3, fill_color=RED, fill_opacity=0.32).move_to([x, cy, 0])
                          for x in xs])
        chain_lbls = VGroup(*[T("chain", 24, TEXT).move_to([x, cy - 0.2, 0]) for x in xs])
        sites = VGroup(*[Circle(radius=0.3, stroke_color=GREY, stroke_width=3).move_to([x, cy + 1.0, 0])
                         for x in xs])
        hb_lbl = T("hemoglobin: one molecule", 28, RED).move_to([0, -1.9, 0])
        self.play(FadeIn(chains, scale=0.9), run_time=0.7)
        self.play(FadeIn(hb_lbl), run_time=0.4)
        self.at("red blood cells")
        self.play(Create(cell), FadeIn(cell_lbl), run_time=1.0)
        self.at("four chains")
        self.play(FadeIn(chain_lbls), run_time=0.6)
        self.at("and four")
        site_lbl = T("4 oxygen-binding sites", 26, GREY).move_to([0, 1.75, 0])
        self.play(Create(sites), FadeIn(site_lbl), run_time=0.8)
        self.at("fraction of those")
        sat = T("saturation = sites holding oxygen", 26, BLUE).move_to([0, -3.1, 0])
        self.play(FadeIn(sat), run_time=0.5)
        o2s = [o2chip().move_to([x, cy + 1.0, 0]) for x in xs]
        self.play(*[FadeIn(o, scale=0.4) for o in o2s[:2]], run_time=0.6)
        two = T("2 of 4", 28, BLUE, weight=BOLD).move_to([5.0, 2.1, 0])
        self.play(FadeIn(two), run_time=0.3)
        self.at("hold oxygen")
        four = T("4 of 4", 28, BLUE, weight=BOLD).move_to(two)
        self.play(*[FadeIn(o, scale=0.4) for o in o2s[2:]], Transform(two, four), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Curve(SpokenScene):
    def construct(self):
        self.at("Plot saturation")
        ax = axes()
        self.play(FadeIn(sketch_title()), Create(ax), run_time=1.4)
        self.at("oxygen dissociation curve")
        c = curve(P50_BASE)
        self.play(Create(c), run_time=2.0)
        self.at("For adult human blood")
        self.play(Indicate(c, color=BLUE, scale_factor=1.03), run_time=0.8)
        self.at("nearly flat")
        gb = band(60, 108, GREEN)
        gl = VGroup(T("flat:", 24, GREEN), T("lungs load", 24, GREEN)).arrange(DOWN, buff=0.08).move_to(
            [px(84), py(0.15), 0])
        self.play(FadeIn(gb), FadeIn(gl), run_time=0.8)
        self.at("Between about")
        yb = band(10, 40, YELLOW)
        yl = VGroup(T("steep:", 24, YELLOW), T("tissues", 24, YELLOW), T("unload", 24, YELLOW)).arrange(
            DOWN, buff=0.08).move_to([px(24), py(0.88), 0])
        self.play(FadeIn(yb), FadeIn(yl), run_time=0.8)
        self.at("cooperative binding")
        chip_c = chip("cooperative binding", RED, size=26).move_to([PANEL_X, 1.5, 0])
        xs = [PANEL_X - 1.3 + 0.87 * i for i in range(4)]
        row = VGroup(*[Circle(radius=0.3, stroke_color=GREY, stroke_width=3).move_to([x, 0.2, 0]) for x in xs])
        cap = T("one molecule, four sites", 24, GREY).move_to([PANEL_X, -0.55, 0])
        self.play(FadeIn(chip_c), Create(row), FadeIn(cap), run_time=0.8)
        self.at("Oxygen at one site")
        o = [o2chip().move_to([x, 0.2, 0]) for x in xs]
        self.play(FadeIn(o[0], scale=0.4), run_time=0.5)
        self.at("bind more readily")
        self.play(LaggedStart(*[FadeIn(oo, scale=0.4) for oo in o[1:]], lag_ratio=0.25), run_time=0.9)
        self.finish()


def static_plot(bands=True, title="Adult human blood, in this sketch"):
    """Rebuild the S03 picture in place for later scenes."""
    items = [sketch_title(title), axes()]
    if bands:
        items += [band(60, 108, GREEN, 0.10), band(10, 40, YELLOW, 0.10)]
    items.append(curve(P50_BASE))
    return VGroup(*items)


# ---------------------------------------------------------------------------------------------
class S04Use(SpokenScene):
    def construct(self):
        self.add(static_plot())
        self.at("illustrative adult human")
        tag = chip("illustrative adult human, at rest", GREY, size=22).move_to([PANEL_X, 2.75, 0])
        self.play(FadeIn(tag), run_time=0.5)
        self.at("Arterial")
        da = dot(100, P50_BASE, GREEN)
        la = VGroup(T("arterial", 24, GREEN), T("100 mmHg, 98%", 24, GREEN)).arrange(DOWN, buff=0.06).move_to(
            [px(88), py(0.62), 0])
        ha = DashedLine([px(100), py(float(hill(100, P50_BASE))), 0], [3.1, py(float(hill(100, P50_BASE))), 0],
                        color=GREEN, stroke_width=3)
        self.play(FadeIn(da, scale=2), FadeIn(la), Create(ha), run_time=0.8)
        self.at("Mixed venous")
        dv = dot(40, P50_BASE, YELLOW)
        lv = VGroup(T("mixed venous", 24, YELLOW), T("40 mmHg, 75%", 24, YELLOW)).arrange(DOWN, buff=0.06).move_to(
            [px(62), py(0.35), 0])
        yv = float(hill(40, P50_BASE))
        hv = DashedLine([px(40), py(yv), 0], [3.1, py(yv), 0], color=YELLOW, stroke_width=3)
        self.play(FadeIn(dv, scale=2), FadeIn(lv), Create(hv), run_time=0.8)
        self.at("of the oxygen offered")
        ya = float(hill(100, P50_BASE))
        arr = DoubleArrow([3.25, py(yv), 0], [3.25, py(ya), 0], color=TEXT, buff=0, stroke_width=4, tip_length=0.15)
        took = VGroup(T("tissues took", 24, TEXT), T("24% of the", 24, TEXT), T("oxygen offered", 24, TEXT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([PANEL_X + 0.9, (py(yv) + py(ya)) / 2 - 0.1, 0])
        self.play(GrowFromCenter(arr), FadeIn(took), run_time=0.8)
        self.at("cardiac output")
        co = chip("cardiac output 5.0 L/min", BLUE, size=24).move_to([PANEL_X, -0.4, 0])
        use = chip("oxygen used 240 mL/min", BLUE, size=24).move_to([PANEL_X, -1.4, 0])
        self.play(FadeIn(co), run_time=0.5)
        self.play(FadeIn(use, shift=DOWN * 0.1), run_time=0.6)
        self.at("comes back unused")
        res = VGroup(T("about three quarters", 24, YELLOW), T("comes back unused", 24, YELLOW)).arrange(
            DOWN, buff=0.06).move_to([PANEL_X, -2.55, 0])
        self.play(FadeIn(res), Indicate(dv, color=YELLOW, scale_factor=2.0), run_time=0.9)
        self.at("steep part")
        self.play(Indicate(curve_between(10, 40), color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.finish()


def curve_between(lo, hi, p50=P50_BASE, color=YELLOW, w=9):
    ps = np.linspace(lo, hi, 40)
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_smoothly([[px(p), py(float(hill(p, p50))), 0] for p in ps])
    return m


# ---------------------------------------------------------------------------------------------
class S05Shift(SpokenScene):
    def construct(self):
        self.add(static_plot(bands=False, title="Blood, in this sketch"))
        base = curve(P50_BASE)
        self.at("In Copenhagen")
        dog = VGroup(T("Bohr, Hasselbalch", 22, GREY), T("and Krogh, 1903:", 22, GREY), T("fresh dog blood", 22, GREY)).arrange(DOWN, buff=0.05).move_to([PANEL_X, 2.6, 0])
        self.play(FadeIn(dog), run_time=0.6)
        self.at("raised the carbon dioxide")
        more = chip("more CO2", ORANGE, size=26).move_to([PANEL_X, 1.5, 0])
        shifted = curve(P50_SHIFT, ORANGE)
        self.play(FadeIn(more, shift=DOWN * 0.1), TransformFromCopy(base, shifted), run_time=1.6)
        self.at("same oxygen pressure")
        p0 = 40
        s1, s2 = float(hill(p0, P50_BASE)), float(hill(p0, P50_SHIFT))
        vl = DashedLine([px(p0), PY0, 0], [px(p0), py(s1), 0], color=GREY, stroke_width=3)
        d1, d2 = dot(p0, P50_BASE, BLUE), dot(p0, P50_SHIFT, ORANGE)
        self.play(Create(vl), FadeIn(d1, scale=2), run_time=0.7)
        self.at("held less oxygen")
        dn = Arrow([px(p0), py(s1) - 0.15, 0], [px(p0), py(s2) + 0.15, 0], color=ORANGE, buff=0, stroke_width=5,
                   tip_length=0.2)
        lab = VGroup(T("same PO2:", 24, TEXT), T("less oxygen held", 24, ORANGE)).arrange(DOWN, buff=0.06).move_to(
            [px(22), py(0.9), 0])
        lead = Line([px(30), py(0.82), 0], [px(p0) - 0.12, (py(s1) + py(s2)) / 2, 0], color=GREY, stroke_width=2)
        self.play(FadeIn(d2, scale=2), GrowArrow(dn), FadeIn(lab), Create(lead), run_time=0.9)
        self.at("Bohr effect names")
        hd = T("Bohr effect", 26, ORANGE, weight=BOLD).move_to([PANEL_X, 0.7, 0])
        c1 = chip("pH falls", ORANGE, size=24).move_to([PANEL_X, 0.0, 0])
        c2 = chip("CO2 rises", ORANGE, size=24).move_to([PANEL_X, -0.8, 0])
        self.play(FadeIn(hd), FadeIn(c1, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.5)
        self.at("shifts right")
        a50 = Arrow([px(P50_BASE) + 0.1, py(0.5), 0], [px(P50_SHIFT) - 0.1, py(0.5), 0], color=TEXT, buff=0,
                    stroke_width=4, tip_length=0.15)
        p1, p2 = dot(P50_BASE, P50_BASE, BLUE, 0.1), dot(P50_SHIFT, P50_SHIFT, ORANGE, 0.1)
        self.play(FadeIn(p1), FadeIn(p2), GrowArrow(a50), run_time=0.7)
        lab50 = T("P50 rises", 24, TEXT).move_to([px(58), py(0.38), 0])
        lead2 = Line([px(49), py(0.4), 0], [px(P50_SHIFT) + 0.05, py(0.5) - 0.12, 0], color=GREY, stroke_width=2)
        self.play(FadeIn(lab50), Create(lead2), run_time=0.6)
        self.at("Higher temperature")
        also = T("also shift it right", 24, GREY).move_to([PANEL_X, -1.65, 0])
        c3 = chip("higher temperature", ORANGE, size=24).move_to([PANEL_X, -2.35, 0])
        c4 = chip("more BPG", ORANGE, size=24).move_to([PANEL_X, -3.15, 0])
        self.play(FadeIn(also), FadeIn(c3, shift=LEFT * 0.2), run_time=0.6)
        self.play(FadeIn(c4, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        base = curve(P50_BASE)
        shifted = curve(P50_SHIFT, ORANGE)
        gb, yb = band(60, 108, GREEN, 0.10), band(10, 40, YELLOW, 0.10)
        self.add(sketch_title(), axes(), gb, yb, base, shifted)
        self.at("In respiring tissue")
        tis = VGroup(T("respiring tissue", 26, YELLOW, weight=BOLD), T("CO2 high", 24, ORANGE),
                     T("PO2 low", 24, BLUE)).arrange(DOWN, buff=0.12).move_to([PANEL_X, 1.9, 0])
        self.play(FadeIn(tis, shift=LEFT * 0.2), run_time=0.8)
        self.at("steep")
        self.play(Indicate(curve_between(10, 40), color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.at("holds less oxygen")
        p0 = 40
        s1, s2 = float(hill(p0, P50_BASE)), float(hill(p0, P50_SHIFT))
        d1 = dot(p0, P50_BASE, BLUE)
        d2 = dot(p0, P50_SHIFT, ORANGE)
        vl = DashedLine([px(p0), PY0, 0], [px(p0), py(s1), 0], color=GREY, stroke_width=3)
        self.play(Create(vl), FadeIn(d1, scale=2), run_time=0.5)
        self.play(TransformFromCopy(d1, d2), run_time=0.8)
        self.at("so the blood has released")
        rel = Brace(Line([px(p0), py(s2), 0], [px(p0), py(s1), 0]), direction=LEFT, color=ORANGE)
        rl = T("released more", 24, ORANGE).move_to([px(22), py(0.9), 0])
        rlead = Line([px(30), py(0.84), 0], [px(p0) - 0.4, (py(s1) + py(s2)) / 2 + 0.05, 0], color=GREY, stroke_width=2)
        self.play(GrowFromCenter(rel), FadeIn(rl), Create(rlead), run_time=0.8)
        self.at("loads on the flat part")
        rule1 = T("loads on the flat part", 24, GREEN, weight=BOLD).move_to([PANEL_X, -0.2, 0])
        self.play(FadeIn(rule1, shift=LEFT * 0.2), Indicate(gb, color=GREEN, scale_factor=1.0),
                  run_time=0.8)
        self.at("unloads on the steep part")
        rule2 = T("unloads on the steep part", 24, YELLOW, weight=BOLD).move_to([PANEL_X, -1.0, 0])
        self.play(FadeIn(rule2, shift=LEFT * 0.2), Indicate(yb, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Hemoglobin loads on the flat part and unloads on the steep part."
