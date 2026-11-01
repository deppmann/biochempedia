"""Cells hold their size  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the surface: membrane, area, supply (uptake across the surface)
  ORANGE = the volume: cytoplasm, volume, demand (use spread through the cell)
  YELLOW = the ratio, the highlighted number, the question
  TEAL   = the plant vacuole
  GREEN  = supply just meets demand
  RED    = demand exceeds supply
  PURPLE = nucleus
  RED    = also the Whi5 division brake
  GREEN  = also commitment to division
  GREY   = labels, guides, axes, not-the-subject
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

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
    TITLE = "Cells Hold Their Size"


def rootcell(w, h, d, center, f_color=TEAL):
    outer = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=5, fill_color=ORANGE, fill_opacity=0.28).move_to(center)
    vac = Rectangle(width=w - 2 * d, height=h - 2 * d, stroke_color=f_color, stroke_width=3, fill_color=f_color,
                    fill_opacity=0.5).move_to(center)
    return outer, vac


def rod(center, w, h=1.05):
    """End-growing fission yeast, with a schematic proportional nucleus."""
    body = RoundedRectangle(corner_radius=h / 2, width=w, height=h,
                            stroke_color=BLUE, stroke_width=5,
                            fill_color=ORANGE, fill_opacity=0.14).move_to(center)
    nuc = Ellipse(width=w * 0.24, height=h * 0.48, color=PURPLE,
                  fill_color=PURPLE, fill_opacity=0.5).move_to(center)
    return VGroup(body, nuc)


def brake_dots(center, r):
    c = np.array(center)
    return VGroup(*[Dot(c + r * np.array([x, y, 0]), radius=0.095, color=RED)
                    for x, y in [(-.45, .25), (0, .48), (.45, .25),
                                 (-.45, -.25), (0, -.48), (.45, -.25)]])


class S01Lead(SpokenScene):
    def construct(self):
        head = T("How does a cell know its size?", 38, YELLOW, font=TITLE_FONT).move_to([0, 3, 0])
        a, b = rod([0, 1.25, 0], 2.1), rod([0, -1.15, 0], 3.7)
        tags = VGroup(T("born small", 28, GREY).move_to([-4.7, 1.25, 0]),
                      T("born large", 28, GREY).move_to([-4.7, -1.15, 0]))
        self.at("Cells do not")
        self.play(FadeIn(head), FadeIn(a), FadeIn(b), run_time=.7)
        link = T("growth → division", 30, TEXT).move_to([0, -3.0, 0])
        self.at("linking growth to division")
        self.play(FadeIn(link), run_time=.6)
        guides = VGroup(*[DashedLine([x, -2, 0], [x, 2.1, 0], color=YELLOW, stroke_width=2)
                         for x in [-2.4, 2.4]])
        self.at("reaches a set size")
        self.play(Create(guides), run_time=.5)
        self.at("Born small")
        self.play(FadeIn(tags[0]), Transform(a, rod([0, 1.25, 0], 4.8)), run_time=1.3)
        self.at("Born large")
        self.play(FadeIn(tags[1]), Transform(b, rod([0, -1.15, 0], 4.8)), run_time=1.0)
        # Divide the two cells at their midpoints, keeping total length approximately constant.
        daughters = [VGroup(rod([-1.3, y, 0], 2.35), rod([1.3, y, 0], 2.35)) for y in [1.25, -1.15]]
        self.play(Transform(a, daughters[0]), Transform(b, daughters[1]), FadeOut(guides), run_time=.9)
        self.at("size sets how much")
        self.play(Indicate(link, color=YELLOW, scale_factor=1.08), run_time=.7)
        self.at("The nucleus")
        self.play(FadeOut(tags), FadeOut(a), FadeOut(b), FadeOut(link), run_time=.4)
        c = rod([0, -.1, 0], 3.0, 1.35)
        nl = T("nucleus", 30, PURPLE).move_to([0, -2, 0])
        self.play(FadeIn(c), FadeIn(nl), run_time=.4)
        self.at("grows with the cell")
        self.play(Transform(c, rod([0, -.1, 0], 5.7, 1.8)), run_time=1.1)
        self.at("So how does")
        self.play(Indicate(head, color=YELLOW, scale_factor=1.03), run_time=.6)
        self.finish()


class S02Sense(SpokenScene):
    def construct(self):
        centers = [[-3.1, -.2, 0], [3.1, -.2, 0]]
        bodies = [cell(centers[0], .85), cell(centers[1], 1.25)]
        brakes = [brake_dots(centers[0], .85), brake_dots(centers[1], 1.25)]
        head = T("Dilution", 40, YELLOW, font=TITLE_FONT).move_to([0, 3.1, 0])
        labels = VGroup(T("born small", 28, GREY).move_to([-3.1, 2.1, 0]),
                        T("born large", 28, GREY).move_to([3.1, 2.1, 0]))
        self.at("One way is dilution")
        self.play(FadeIn(head), run_time=.5)
        self.at("In budding yeast")
        self.play(*[FadeIn(b) for b in bodies], FadeIn(labels), run_time=.6)
        same = T("same amount of division brake", 28, RED).move_to([0, -2.65, 0])
        self.at("the same amount")
        self.play(*[FadeIn(d) for d in brakes], FadeIn(same), run_time=.6)
        self.at("a protein called")
        self.play(Transform(same, T("Whi5 · division brake", 30, RED).move_to(same)), run_time=.6)
        self.at("As the cell grows")
        self.play(*[Transform(b, cell(c, r)) for b, c, r in zip(bodies, centers, [1.2, 1.85])],
                  *[Transform(d, brake_dots(c, r)) for d, c, r in zip(brakes, centers, [1.2, 1.85])], run_time=1.3)
        light = chip("commit", GREEN, 28).move_to([3.1, -2.7, 0])
        self.at("dilutes it sooner")
        self.play(Indicate(brakes[1], color=RED, scale_factor=1.15), run_time=.6)
        self.at("commit to dividing")
        self.play(FadeOut(same), FadeIn(light), bodies[1].animate.set_stroke(GREEN), run_time=.6)
        wait = T("waits → more growth", 26, YELLOW).move_to([-3.1, -2.7, 0])
        self.at("A cell born small waits")
        self.play(FadeIn(wait), run_time=.5)
        self.at("and grows more first")
        self.play(Transform(bodies[0], cell(centers[0], 1.55)),
                  Transform(brakes[0], brake_dots(centers[0], 1.55)), run_time=.9)
        self.finish()


class S03Make(SpokenScene):
    def construct(self):
        c = [-2.9, -.2, 0]
        body, content = cell(c, 1.1), dots(c, 1.1, .48)
        head = T("Making enough for the volume", 38, font=TITLE_FONT).move_to([0, 3.1, 0])
        self.at("Size also sets")
        self.play(FadeIn(head), FadeIn(body), FadeIn(content), run_time=.7)
        label = card(["RNA + protein", "same concentration"], ORANGE, w=4.8, sizes=[28, 28]).move_to([3.5, .9, 0])
        self.at("the same concentration")
        self.play(FadeIn(label), run_time=.6)
        self.at("must make more")
        self.play(Transform(body, cell(c, 1.8)), Transform(content, dots(c, 1.8, .48)), run_time=1.2)
        self.at("in step with volume")
        self.play(Indicate(content, color=ORANGE, scale_factor=1.05), run_time=.6)
        limit = T("Growth without division", 30, YELLOW).move_to([3.5, -1.1, 0])
        self.at("That has a limit")
        self.play(FadeOut(label), run_time=.5)
        self.at("grow without dividing")
        self.play(FadeIn(limit), run_time=.5)
        self.at("get many times bigger")
        spread = VGroup(*[Dot(np.array(c) + (d.get_center() - np.array(c)) * (2.65 / 1.8),
                              radius=.07, color=ORANGE) for d in content])
        self.play(Transform(body, cell(c, 2.65)), Transform(content, spread), run_time=1.3)
        self.at("synthesis falls behind")
        lag = T("synthesis falls behind", 28, ORANGE).move_to([3.5, -.1, 0])
        self.play(FadeIn(lag), run_time=.6)
        self.at("Their cytoplasm becomes diluted")
        diluted = T("diluted", 36, YELLOW).move_to([3.5, -2.3, 0])
        self.play(FadeIn(diluted), run_time=.7)
        self.finish()


class S04Parts(SpokenScene):
    def construct(self):
        head = T("Different cells, different shares", 38, font=TITLE_FONT).move_to([0, 3.1, 0])
        key = T("nucleus", 28, PURPLE).move_to([4.9, 2.25, 0])
        def share(y, fraction, name, text):
            left, width = -1.7, 6.5
            parts = VGroup(bar(left, y, width * fraction, PURPLE, .65),
                           bar(left + width * fraction, y, width * (1-fraction), ORANGE, .65))
            return VGroup(parts, T(name, 26, GREY).move_to([-4.2, y, 0]),
                          T(text, 26, PURPLE).move_to([1.55, y-.65, 0]))
        h = share(1.1, .27, "V79 hamster", "a little over one quarter")
        f = share(-.8, .08, "fission yeast", "under one tenth")
        self.at("The parts scale too")
        self.play(FadeIn(head), run_time=.6)
        self.at("A little more than a quarter")
        self.play(FadeIn(h), FadeIn(key), run_time=.7)
        self.at("In fission")
        self.play(FadeIn(f), run_time=.7)
        row = VGroup(rod([-4.2, 0, 0], 1.0, .5), rod([-1.1, 0, 0], 2.1, 1.05),
                     rod([3.5, 0, 0], 3.27, 1.635))
        self.at("There the nucleus grows")
        self.play(FadeOut(h), FadeOut(f), FadeOut(key), FadeIn(row), run_time=.8)
        range_label = T("35-fold range of cell volumes", 30, YELLOW).move_to([0, -1.8, 0])
        self.at("across a 35")
        self.play(FadeIn(range_label), run_time=.6)
        dna = card(["16-fold change in DNA", "nucleus / cell ratio unchanged"], PURPLE,
                   w=7, sizes=[28, 28]).move_to([0, -2.9, 0])
        self.at("and a 16")
        self.play(FadeOut(range_label), FadeIn(dna), run_time=.6)
        self.at("leaves the ratio unchanged")
        self.play(*[Indicate(r[1], color=PURPLE, scale_factor=1.1) for r in row], run_time=.6)
        self.finish()


class S05Vacuole(SpokenScene):
    def construct(self):
        outer, vac = rootcell(1.2, 1.2, .25, [-3.8, 0, 0])
        head = T("Arabidopsis root epidermis", 34, font=TITLE_FONT).move_to([0, 3.15, 0])
        note = T("schematic · not to scale", 22, GREY).move_to([-3.8, -3.2, 0])
        self.at("Plant cells")
        self.play(FadeIn(outer), FadeIn(vac), FadeIn(note), run_time=.6)
        self.at("In Arabidopsis root epidermis")
        self.play(FadeIn(head), run_time=.6)
        whole = card(["whole cell volume", "about 14-fold"], YELLOW, w=4.9, sizes=[26, 32]).move_to([3.2, 1.6, 0])
        self.at("cells grew about 14")
        big_o, big_v = rootcell(2.3, 5.4, .2, [-3.8, 0, 0])
        self.play(Transform(outer, big_o), Transform(vac, big_v), FadeIn(whole), run_time=1.2)
        outside = card(["space outside vacuole", "about 2 to 3-fold"], ORANGE, w=4.9, sizes=[26, 30]).move_to([3.2, -.25, 0])
        self.at("but the space between")
        self.play(FadeIn(outside), run_time=.6)
        vl = T("vacuole", 28, TEAL).move_to([-3.8, 0, 0])
        self.at("Most new volume is vacuole")
        self.play(FadeIn(vl), Indicate(vac, color=TEAL, scale_factor=1.02), run_time=.8)
        wall = T("wall loosens → cell stretches", 26, GREY).move_to([3.2, -2.5, 0])
        self.at("the wall has to loosen")
        self.play(FadeIn(wall), outer.animate.set_stroke(width=3), run_time=.6)
        self.at("to let the cells stretch")
        end_o, end_v = rootcell(2.4, 5.7, .2, [-3.8, 0, 0])
        self.play(Transform(outer, end_o), Transform(vac, end_v), run_time=.7)
        self.finish()


class S06Surface(SpokenScene):
    def construct(self):
        c = [-3.5, -.1, 0]
        body = cell(c, 1.1)
        content = dots(c, 1.1, .48)
        head = T("Geometry adds a cost", 38, font=TITLE_FONT).move_to([0, 3.1, 0])
        self.at("Geometry adds a cost")
        self.play(FadeIn(head), FadeIn(body), run_time=.6)
        arrows = in_arrows(c, 1.1, 6, out=.5)
        surface = T("supply through surface", 28, BLUE).move_to([3, 1.8, 0])
        self.at("crosses its surface")
        self.play(FadeIn(arrows), FadeIn(surface), run_time=.6)
        volume = T("use through volume", 28, ORANGE).move_to([3, -.1, 0])
        self.at("spread through its volume")
        self.play(FadeIn(content), FadeIn(volume), run_time=.6)
        radius = T("radius: 5 → 10 µm", 28, YELLOW).move_to([-3.5, -2.8, 0])
        self.at("Double a sphere's radius")
        self.play(FadeOut(arrows), Transform(body, cell(c, 2.2)),
                  Transform(content, dots(c, 2.2, .48)), FadeIn(radius),
                  FadeOut(surface), FadeOut(volume), run_time=.9)
        a = bar(.5, 1.4, .5, BLUE)
        al = T("area ×4", 28, BLUE).move_to([3, 2.05, 0])
        self.at("its area rises fourfold")
        self.play(FadeIn(a), FadeIn(al), run_time=.25)
        self.play(Transform(a, bar(.5, 1.4, 2, BLUE)), run_time=.6)
        v = bar(.5, -.3, .5, ORANGE)
        vl = T("volume ×8", 28, ORANGE).move_to([3, .35, 0])
        self.at("its volume rises eightfold")
        self.play(FadeIn(v), FadeIn(vl), run_time=.25)
        self.play(Transform(v, bar(.5, -.3, 4, ORANGE)), run_time=.6)
        # Qualitative model with fixed coefficients: no measured threshold is implied.
        P = Plot([-4.8, -2.5], 9.6, 4.6, 1, 1)
        ax = P.axes()
        supply = P.curve(lambda r: .55*r*r, 0, 1, BLUE)
        demand = P.curve(lambda r: .85*r*r*r, 0, 1, ORANGE)
        labs = VGroup(T("radius →", 24, GREY).move_to([4, -3.05, 0]),
                      T("relative rate", 24, GREY).move_to([-4, 2.45, 0]),
                      T("fixed uptake / area", 26, BLUE).move_to([-1.8, 1.6, 0]),
                      T("fixed demand / volume", 26, ORANGE).move_to([-1.5, .9, 0]))
        self.at("With fixed uptake per area")
        self.play(*[FadeOut(m) for m in [body, content, radius, a, al, v, vl]],
                  Create(ax), FadeIn(VGroup(*labs[:3])), run_time=.6)
        self.play(Create(supply), run_time=.6)
        self.at("and fixed demand per volume")
        self.play(FadeIn(labs[3]), Create(demand), run_time=.7)
        cross_r = .55/.85
        cross = Dot(P.p(cross_r, .55*cross_r**2), color=YELLOW, radius=.1)
        self.at("supply falls behind")
        self.play(FadeIn(cross), Indicate(demand, color=ORANGE, scale_factor=1.01), run_time=.7)
        self.finish()


class S07Rule(SpokenScene):
    def construct(self):
        cards = [card(["1 · growth linked to division"], BLUE, w=9.5, sizes=[32]).move_to([0, 2, 0]),
                 card(["2 · size sets synthesis and parts"], ORANGE, w=9.5, sizes=[32]).move_to([0, 0, 0]),
                 card(["3 · surface adds a cost"], YELLOW, w=9.5, sizes=[32]).move_to([0, -2, 0])]
        head = T("Keep the order", 36, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.at("Keep the order")
        self.play(FadeIn(head), run_time=.5)
        self.at("linking growth to division")
        self.play(FadeIn(cards[0], shift=DOWN*.15), run_time=.6)
        self.at("Size then sets")
        self.play(FadeIn(cards[1], shift=DOWN*.15), run_time=.6)
        self.at("Surface and volume")
        self.play(FadeIn(cards[2], shift=DOWN*.15), run_time=.6)
        note = T("not a universal maximum", 28, GREY).move_to([0, -3.2, 0])
        self.at("not a universal maximum")
        self.play(FadeIn(note), run_time=.6)
        self.finish()


class S08End(EndCard):
    LINE = "Cells hold their size by linking growth to division."
