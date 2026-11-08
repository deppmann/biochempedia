"""Multiply, Don't Add  (chapter 1 of What Makes the Human Brain Big)

COLOR MAP (one color per concept, shared by every chapter; taken from scenes.old.py)
  BLUE   = progenitors: classical radial glia, the founders, the units (patch + fibre)
  YELLOW = neurons, and the columns they stack into
  GREEN  = area: the number of units, symmetric (doubling) divisions
  PURPLE = thickness: neurons per unit, asymmetric (adding) divisions
  PINK   = outer radial glia (chapter 2)
  ORANGE = a gene or protein that is added, changed or removed (stabilised beta-catenin here)
  RED    = not tested / no contact / missing
  TEAL   = time: cell cycles, how long a step takes (new in this chapter, reuse in chapters 2 and 3)
  GREY   = ventricle, brain surface, labels, de-emphasised things
  GOLD   = the question, the switch, and one highlight at a time
  TEXT   = plain labels and names
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#C9A2F2"
ORANGE = "#F29E4C"
PINK = "#E58BB8"


def P(x, y):
    return np.array([x, y, 0.0])


class S(SpokenScene):
    def til(self, t):
        """Wait until t seconds into the scene (no cue to log)."""
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


# ----------------------------------------------------------------------------------------------
# small shape helpers
def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    g = VGroup(back, t)
    g.set_z_index(6)
    return g


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.04, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def darr(a, b, color=GREY, w=5, tip=0.2):
    return DoubleArrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                       max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cellc(x, y, r=0.9, color=BLUE, op=0.85):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to(P(x, y))
    c.set_z_index(3)
    return c


def small_dot(x, y, color=YELLOW, r=0.24):
    d = Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to(P(x, y))
    d.set_z_index(4)
    return d


def spread(n, sp):
    return [(i - (n - 1) / 2) * sp for i in range(n)]


def fit_w(mob, w):
    if mob.width > w:
        mob.scale(w / mob.width)
    return mob


VEN_Y = -2.6


def ventricle(label=True, x0=-6.4, x1=6.4, y=VEN_Y):
    b = RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=0.22, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.35).move_to(P((x0 + x1) / 2, y))
    g = VGroup(b)
    if label:
        g.add(T("ventricle", 26, GREY).move_to(P(x1 - 1.1, y - 0.55)))
    return g


CR = 0.9
CY = VEN_Y + 0.11 + CR        # a progenitor of radius CR sitting on the ventricle


def counter(label, color, val, x, y=1.0):
    lab = T(label, 34, color).move_to(P(x, y + 0.95))
    num = M(str(val), 80, color).move_to(P(x, y - 0.15))
    return VGroup(lab, num)


def renum(c, val, color):
    return M(str(val), 80, color).move_to(c[1])


# ----------------------------------------------------------------------------------------------
# slabs (s01, s02): unfolded sheets drawn as slabs. top face = area (green), edges = thickness (purple)
def slab(xl, yb, w, d, t):
    dx, dy = 0.8 * d, 0.6 * d
    front = Polygon(P(xl, yb), P(xl + w, yb), P(xl + w, yb + t), P(xl, yb + t), stroke_color=PURPLE,
                    stroke_width=3, fill_color=PURPLE, fill_opacity=0.4)
    side = Polygon(P(xl + w, yb), P(xl + w + dx, yb + dy), P(xl + w + dx, yb + t + dy), P(xl + w, yb + t),
                   stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.25)
    top = Polygon(P(xl, yb + t), P(xl + w, yb + t), P(xl + w + dx, yb + t + dy), P(xl + dx, yb + t + dy),
                  stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35)
    return VGroup(front, side, top)


SB = -1.9   # base of the slabs


def two_slabs():
    mouse = slab(-6.3, SB, 1.56, 1.2, 0.6)
    human = slab(-3.3, SB, 6.0, 4.8, 1.2)
    ml = T("mouse", 28, TEXT).move_to(P(-5.5, SB - 0.45))
    hl = T("human", 28, TEXT).move_to(P(-0.3, SB - 0.45))
    note = T("schematic sheets, not to scale", 26, GREY).move_to(P(3.9, -3.5))
    return mouse, human, ml, hl, note


def thick_marks():
    m = darr(P(-6.55, SB), P(-6.55, SB + 0.6), PURPLE, 4, 0.14)
    h = darr(P(-3.6, SB), P(-3.6, SB + 1.2), PURPLE, 4, 0.18)
    tl = T("thickness: about 2 times", 28, PURPLE).move_to(P(-3.3, -3.0))
    return m, h, tl


class S00Title(TitleCard):
    LESSON = "What Makes the Human Brain Big"
    TITLE = "Multiply, Don't Add"

    def construct(self):
        # the whole title is on screen from the first frames and held for about two seconds
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=26, color=GREY)
        title = T(self.TITLE, size=64, font=TITLE_FONT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.add(g)
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.35)
        self.wait(2.0)
        self.play(FadeOut(g), run_time=0.35)
        self.finish()


# ----------------------------------------------------------------------------------------------
def q_top():
    return T("Why is the surface so much larger?", 36, GOLD).move_to(P(-1.2, 3.4))


def area_lab():
    return T("area: about 1,000 times", 32, GREEN).move_to(P(3.2, 2.8))


class S01Q(S):
    def construct(self):
        mouse, human, ml, hl, note = two_slabs()
        self.at("Your cortex")
        self.play(FadeIn(mouse), FadeIn(human), FadeIn(ml), FadeIn(hl), FadeIn(note), run_time=0.9)
        self.at("twice as thick")
        tm, th, tl = thick_marks()
        self.play(GrowFromCenter(tm), GrowFromCenter(th), FadeIn(tl), run_time=0.7)
        self.at("So why")
        q = q_top()
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.6)
        self.at("its surface")
        self.play(Indicate(VGroup(mouse[2], human[2]), color=GREEN, scale_factor=1.03), run_time=0.8)
        self.at("thousand")
        al = area_lab()
        self.play(FadeIn(al, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


class S02Sideways(S):
    def construct(self):
        mouse, human, ml, hl, note = two_slabs()
        tm, th, tl = thick_marks()
        al = area_lab()
        q = q_top()
        self.add(mouse, human, ml, hl, note, tm, th, tl, al, q)
        self.at("Almost all of the gain")
        # the size factor split on screen as two lines: height x 2, area x 1,000
        h2 = T("height × 2", 36, PURPLE).move_to(P(-4.75, 1.85))
        a2 = T("area × 1,000", 36, GREEN).move_to(P(-4.75, 1.1))
        self.play(FadeOut(q), FadeOut(tl), FadeOut(al), FadeIn(h2, shift=RIGHT * 0.15), run_time=0.5)
        self.play(FadeIn(a2, shift=RIGHT * 0.15), run_time=0.4)
        side_arrow = arr(P(0.3, 2.65), P(6.3, 2.65), GREEN, 8, 0.35)
        sl = T("sideways", 34, GREEN).move_to(P(-1.4, 2.65))
        self.at("sideways")
        self.play(GrowArrow(side_arrow), FadeIn(sl), run_time=0.6)
        self.at("How does a brain build")
        q2 = T("How does a brain build more of the same wall?", 34, GOLD).move_to(P(0, 3.45))
        self.play(FadeIn(q2, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
R1 = 1.15
Y1 = VEN_Y + 0.11 + R1


class S03Two(S):
    def construct(self):
        v = ventricle()
        c = cellc(0, Y1, R1)
        lab = T("progenitor", 32, BLUE).move_to(P(0, Y1 + R1 + 0.5))
        self.play(FadeIn(v), FadeIn(c, scale=0.6), run_time=0.7)
        self.at("division")
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


class S04Sym(S):
    def construct(self):
        v = ventricle()
        c0 = cellc(0, Y1, R1)
        pool = counter("progenitors", BLUE, 1, -4.2)
        self.add(v, c0, pool)
        self.at("symmetric proliferative")
        kind = T("symmetric proliferative division", 36, GREEN).move_to(P(0, 3.3))
        self.play(FadeIn(kind, shift=DOWN * 0.15), run_time=0.6)
        self.at("one progenitor makes two")
        c1 = cellc(0, Y1, R1)
        self.add(c1)
        lab1 = T("one division:\n+1 progenitor", 32, GREEN).move_to(P(4.2, 1.0))
        self.play(c0.animate.move_to(P(-1.25, Y1)), c1.animate.move_to(P(1.25, Y1)),
                  Transform(pool[1], renum(pool, 2, BLUE)), FadeIn(lab1, shift=LEFT * 0.15), run_time=0.6)
        self.at("does this once")
        d0 = cellc(-1.25, Y1, R1)
        d1 = cellc(1.25, Y1, R1)
        self.add(d0, d1)
        self.play(c0.animate.move_to(P(-3.75, Y1)), d1.animate.move_to(P(3.75, Y1)),
                  Transform(pool[1], renum(pool, 4, BLUE)), FadeOut(lab1), run_time=0.6)
        self.at("the pool doubles")
        lab2 = T("a full round:\npool × 2", 32, GREEN).move_to(P(4.2, 1.0))
        self.play(FadeIn(lab2, shift=LEFT * 0.15), Indicate(pool[1], color=BLUE, scale_factor=1.15), run_time=0.7)
        self.finish()


class S05Asym(S):
    def construct(self):
        v = ventricle()
        c0 = cellc(0, Y1, R1)
        pool = counter("progenitors", BLUE, 1, -4.2)
        neu = counter("neurons", YELLOW, 0, 4.2)
        self.add(v, c0, pool, neu)
        self.at("asymmetric neurogenic")
        kind = T("asymmetric neurogenic division", 36, PURPLE).move_to(P(0, 3.3))
        self.play(FadeIn(kind, shift=DOWN * 0.15), run_time=0.5)
        self.at("it makes one progenitor")
        self.play(c0.animate.move_to(P(-1.35, Y1)), run_time=0.5)
        pl = T("progenitor", 28, BLUE).move_to(P(-1.35, Y1 + R1 + 0.4))
        self.play(FadeIn(pl), run_time=0.4)
        self.at("and one neuron")
        n0 = cellc(-1.35, Y1, 0.85, YELLOW, 0.85)
        self.add(n0)
        self.play(n0.animate.move_to(P(1.45, Y1)), run_time=0.8)
        nl = T("neuron", 28, YELLOW).move_to(P(1.45, Y1 + R1 + 0.4))
        self.play(Transform(neu[1], renum(neu, 1, YELLOW)), FadeIn(nl), run_time=0.4)
        self.at("the pool stays")
        un = T("unchanged", 30, BLUE).move_to(P(-4.2, -0.15))
        self.play(Indicate(pool[1], color=BLUE, scale_factor=1.15), FadeIn(un), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
FR = 0.5


def founder_cell(x, r=FR, fibre_top=2.75):
    cy = VEN_Y + 0.11 + r
    fib = Line(P(x, cy + r), P(x, fibre_top), color=BLUE, stroke_width=3).set_opacity(0.55)
    return VGroup(fib, cellc(x, cy, r))


class S06Founders(S):
    def construct(self):
        v = ventricle()
        surf = VGroup(Line(P(-6.4, 2.75), P(6.4, 2.75), color=GREY, stroke_width=3),
                      T("brain surface", 26, GREY).move_to(P(5.2, 3.15)))
        self.add(v, surf)
        xs4 = [-3.3, -1.1, 1.1, 3.3]
        row4 = VGroup(*[founder_cell(x) for x in xs4])
        cy = VEN_Y + 0.11 + FR
        self.play(FadeIn(row4, shift=UP * 0.2), run_time=0.8)
        self.at("radial glia")
        rg = T("radial glia", 28, BLUE).move_to(P(-5.55, 0.5))
        rgl = Line(P(-4.55, 0.5), P(-3.4, 0.5), color=BLUE, stroke_width=2.5)
        self.play(FadeIn(rg), Create(rgl), run_time=0.5)
        self.at("founders")
        fl = T("the founders", 28, BLUE).move_to(P(-5.45, -1.15))
        fll = Line(P(-4.3, -1.3), P(-3.85, -1.75), color=BLUE, stroke_width=2.5)
        self.play(FadeIn(fl), Create(fll), run_time=0.5)
        self.at("divide symmetrically")
        kind = T("divide symmetrically: pool × 2", 34, GREEN).move_to(P(-0.6, 3.5))
        copies = [g.copy() for g in row4]
        self.add(*copies)
        anims = []
        for g, c in zip(row4, copies):
            anims += [g.animate.shift(LEFT * 0.55), c.animate.shift(RIGHT * 0.55)]
        self.play(FadeIn(kind, shift=DOWN * 0.15), FadeOut(rg), FadeOut(rgl), FadeOut(fl), FadeOut(fll),
                  *anims, run_time=0.7)
        cells8 = []
        for g, c in zip(row4, copies):
            cells8 += [g, c]
        self.at("Later")
        kind2 = T("later: switch to making neurons", 34, PURPLE).move_to(P(-0.6, 3.5))
        self.play(FadeOut(kind), run_time=0.3)
        self.play(FadeIn(kind2, shift=DOWN * 0.15), run_time=0.4)
        self.at("making neurons")
        dots = []
        for g in cells8:
            x = g[1].get_center()[0]
            dots.append(small_dot(x, cy + FR - 0.1, YELLOW, 0.24))
        self.add(*dots)
        self.play(LaggedStart(*[d.animate.move_to(P(d.get_center()[0], 0.5)) for d in dots], lag_ratio=0.1),
                  run_time=1.3)
        self.finish()


# ----------------------------------------------------------------------------------------------
SLOTS = [-0.9, -0.25, 0.4, 1.05, 1.7]
COL_B, COL_T = -1.5, 2.1
SURF_Y = 2.75


def unit_parts(x, with_col=True, with_dots=True):
    patch = Ellipse(width=0.9, height=0.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                    fill_opacity=0.6).move_to(P(x, -2.38))
    fibre = Line(P(x, -2.2), P(x, SURF_Y), color=BLUE, stroke_width=3).set_opacity(0.55)
    parts = {"patch": patch, "fibre": fibre}
    if with_col:
        parts["col"] = RoundedRectangle(corner_radius=0.12, width=0.95, height=COL_T - COL_B, stroke_color=YELLOW,
                                        stroke_width=3, fill_color=YELLOW, fill_opacity=0.1
                                        ).move_to(P(x, (COL_B + COL_T) / 2))
    if with_dots:
        parts["dots"] = VGroup(*[small_dot(x, y) for y in SLOTS])
    return parts


# birth-order colours: first-born (deep) is the darkest gold, the youngest is the brightest
BIRTH = ["#A8841A", "#CDA826", "#E8C535", "#F5D547", "#FFF08A"]
S7 = [-1.2, -0.4, 0.4, 1.2, 2.0]


class S07Rakic(S):
    def construct(self):
        v = ventricle(label=False)
        surf = VGroup(Line(P(-6.4, SURF_Y), P(6.4, SURF_Y), color=GREY, stroke_width=3),
                      T("brain surface", 26, GREY).move_to(P(5.2, 3.15)))
        patch = Ellipse(width=1.5, height=0.36, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                        fill_opacity=0.6).move_to(P(0, -2.36))
        fibre = Line(P(0, -2.18), P(0, SURF_Y), color=BLUE, stroke_width=3).set_opacity(0.55)
        self.add(v, surf)
        card = VGroup(T("Pasko Rakic", 40, TEXT, font=TITLE_FONT), T("fetal rhesus monkey", 28, GREY)
                      ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(P(-4.0, 1.9))
        self.play(FadeIn(card, shift=RIGHT * 0.2), FadeIn(patch), Create(fibre), run_time=0.9)
        born = T("born here", 28, BLUE).move_to(P(2.3, -2.0))
        bl = Line(P(1.0, -2.0), P(0.85, -2.3), color=BLUE, stroke_width=2.5)
        self.play(FadeIn(born), Create(bl), run_time=0.4)
        self.at("young neurons")
        dots = [small_dot(0, -2.05, c, 0.34) for c in BIRTH]
        anims = []
        for d, y in zip(dots, S7):
            anims.append(Succession(FadeIn(d, scale=0.3, run_time=0.2),
                                    d.animate.move_to(P(0, y)).set_run_time(0.9)))
        self.play(LaggedStart(*anims, lag_ratio=0.45), run_time=2.9)
        old = T("oldest at the bottom", 30, BIRTH[0]).move_to(P(3.9, -1.2))
        ol = Line(P(1.8, -1.2), P(0.8, -1.2), color=BIRTH[0], stroke_width=2.5)
        yg = T("youngest on top", 30, BIRTH[4]).move_to(P(3.4, 2.0))
        yl = Line(P(1.75, 2.0), P(0.8, 2.0), color=BIRTH[4], stroke_width=2.5)
        self.at("He argued")
        self.play(FadeIn(old), Create(ol), FadeIn(yg), Create(yl), run_time=0.5)
        self.at("stack into columns")
        col = RoundedRectangle(corner_radius=0.14, width=1.25, height=4.0, stroke_color=YELLOW, stroke_width=3,
                               fill_color=YELLOW, fill_opacity=0.08).move_to(P(0, 0.4))
        self.play(FadeIn(col), run_time=0.6)
        self.finish()


UX = [-3.6, -1.8, 0.0, 1.8, 3.6]


class S08Units(S):
    def construct(self):
        v = ventricle(label=False)
        surf = Line(P(-6.4, SURF_Y), P(4.6, SURF_Y), color=GREY, stroke_width=3)
        units = [unit_parts(x) for x in UX]
        mid = units[2]
        self.add(v, surf)
        for k in ("patch", "fibre", "col", "dots"):
            self.add(mid[k])
        self.at("In 1988")
        t1 = T("1988", 42, GOLD, font=TITLE_FONT).move_to(P(0, 3.45))
        self.play(FadeIn(t1, shift=DOWN * 0.15), run_time=0.5)
        self.at("radial unit hypothesis")
        t2 = T("The radial unit hypothesis, 1988", 36, GOLD, font=TITLE_FONT).move_to(P(0, 3.45))
        others = [u for i, u in enumerate(units) if i != 2]
        self.play(ReplacementTransform(t1, t2),
                  *[FadeIn(u[k], shift=UP * 0.1) for u in others for k in ("patch", "fibre", "col", "dots")],
                  run_time=1.0)
        self.at("takes up about the same patch")
        segs = VGroup(*[Rectangle(width=1.74, height=0.22, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                                  fill_opacity=0.4).move_to(P(x, SURF_Y)) for x in UX])
        pl = T("same patch\nper unit", 28, GREEN).move_to(P(5.7, 2.75))
        self.play(LaggedStart(*[FadeIn(s_, scale=0.6) for s_ in segs], lag_ratio=0.25), FadeIn(pl, shift=LEFT * 0.1),
                  run_time=1.6)
        self.at("the number of units")
        area_arrow = darr(P(-4.5, -3.1), P(4.5, -3.1), GREEN, 5, 0.2)
        cap1 = T("number of units: area", 30, GREEN).move_to(P(0, -3.55))
        self.play(GrowFromCenter(area_arrow), FadeIn(cap1, shift=UP * 0.1), run_time=0.8)
        self.at("The neurons per unit")
        thick_arrow = darr(P(-4.5, COL_B), P(-4.5, COL_T), PURPLE, 5, 0.2)
        cap2 = T("neurons\nper unit:\nthickness", 28, PURPLE).move_to(P(-5.65, 0.3))
        self.play(FadeIn(VGroup(thick_arrow, cap2)), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
# s09-s11: the three species, big panels
PX = [-4.5, 0.0, 4.5]
PCY, PW, PH = -0.9, 4.3, 5.5     # panels run from y = -3.65 to 1.85


def panel_frame(i):
    r = RoundedRectangle(corner_radius=0.2, width=PW, height=PH, stroke_color=GREY, stroke_width=2.5,
                         fill_color=GREY, fill_opacity=0.07).move_to(P(PX[i], PCY))
    h = T("Species " + "ABC"[i], 40, TEXT).move_to(P(PX[i], PCY + PH / 2 - 0.45))
    return VGroup(r, h)


def cap_lines(txts, i, color=TEXT, size=30):
    return VGroup(*[T(t, size, color).move_to(P(PX[i], -2.2 - 0.5 * k)) for k, t in enumerate(txts)])


def unit_icon(x):
    patch = Ellipse(width=1.1, height=0.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                    fill_opacity=0.6).move_to(P(x, -1.5))
    col = Rectangle(width=0.95, height=2.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                    fill_opacity=0.2).move_to(P(x, -0.2))
    n = M("100", 28, YELLOW).move_to(col)
    return VGroup(patch, col, n)


def pchip(txt, color, x, y, size=30):
    return chip(txt, color, size, 0.14, 0.2).move_to(P(x, y))


def panel_parts():
    """Each panel as separate pieces so they can arrive as they are named."""
    A = dict(frame=panel_frame(0), unit=unit_icon(PX[0]), cap=cap_lines(["each unit makes", "about 100 neurons"], 0))
    B = dict(frame=panel_frame(1), unit=unit_icon(PX[1] - 1.0),
             chips=VGroup(*[pchip("×2", GREEN, PX[1] + 1.2, y) for y in (0.55, -0.2, -0.95)]),
             cap=cap_lines(["3 extra symmetric", "rounds, before", "the switch"], 1))
    C = dict(frame=panel_frame(2), unit=unit_icon(PX[2] - 1.0),
             chips=VGroup(*[pchip("+1", PURPLE, PX[2] + 1.2, y) for y in (0.55, -0.2, -0.95)]),
             cap=cap_lines(["3 extra asymmetric", "divisions per unit,", "after the switch"], 2))
    return A, B, C


def all_panels(parts):
    out = []
    for p in parts:
        out += [p["frame"], p["unit"], p["cap"]] + ([p["chips"]] if "chips" in p else [])
    return out


def question_lines():
    return VGroup(T("Which species gains more neurons?", 34, GOLD).move_to(P(0, 3.45)),
                  T("And which gains area?", 34, GOLD).move_to(P(0, 2.78)))


class S09Predict(S):
    def construct(self):
        A, B, C = panel_parts()
        head = T("Predict", 48, GOLD, font=TITLE_FONT).move_to(P(0, 2.85))
        self.add(head)
        self.play(FadeIn(A["frame"]), FadeIn(A["unit"]), FadeIn(A["cap"]), run_time=0.6)
        self.at("species")
        self.play(FadeIn(B["frame"]), FadeIn(B["unit"]), run_time=0.5)
        self.at("three extra rounds")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in B["chips"]], lag_ratio=0.35), run_time=1.0)
        self.at("symmetric division")
        self.play(Indicate(B["chips"], color=GREEN, scale_factor=1.06), FadeIn(B["cap"][0]), FadeIn(B["cap"][1]),
                  run_time=0.7)
        self.at("before the switch")
        self.play(FadeIn(B["cap"][2]), run_time=0.5)
        self.at("species c")
        self.play(FadeIn(C["frame"]), FadeIn(C["unit"]), run_time=0.5)
        self.at("three extra asymmetric")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in C["chips"]], lag_ratio=0.35), run_time=1.0)
        self.at("asymmetric divisions per unit")
        self.play(FadeIn(C["cap"][0]), FadeIn(C["cap"][1]), Indicate(C["chips"], color=PURPLE, scale_factor=1.06),
                  run_time=0.6)
        self.at("After it")
        self.play(FadeIn(C["cap"][2]), run_time=0.5)
        self.at("each adding one neuron")
        self.play(Indicate(C["chips"], color=PURPLE, scale_factor=1.12), run_time=0.8)
        self.finish()


class S10Predict2(S):
    def construct(self):
        A, B, C = panel_parts()
        self.add(*all_panels([A, B, C]))
        q = question_lines()
        self.at("Which species gains more neurons")
        self.play(FadeIn(q[0], shift=DOWN * 0.15), run_time=0.6)
        self.at("which one gains area")
        self.play(FadeIn(q[1], shift=DOWN * 0.15), run_time=0.6)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        A, B, C = panel_parts()
        self.add(*all_panels([A, B, C]), question_lines())
        cue = T("pause and predict", 28, TEAL).move_to(P(5.0, 2.78))
        track = Rectangle(width=9.0, height=0.14, stroke_color=TEAL, stroke_width=2, fill_opacity=0
                          ).move_to(P(0, 2.2))

        def barf(w):
            return Rectangle(width=max(w, 0.02), height=0.14, stroke_width=0, fill_color=TEAL, fill_opacity=0.9
                             ).move_to(P(-4.5 + max(w, 0.02) / 2, 2.2))

        bar = barf(9.0)
        self.add(cue, track, bar)
        self.play(UpdateFromAlphaFunc(bar, lambda m, a: m.become(barf(9.0 * (1 - a))), rate_func=linear),
                  run_time=self.narration_s - 0.2)
        self.finish()


# ----------------------------------------------------------------------------------------------
# s12-s15: B on the left, C on the right, nothing moves between them
BCX = -3.4
SPS, WS = 0.72, 0.62
UNIT_BASE = -2.05
COLH = 3.6
VY = -2.55
CXU = 1.7          # species C's column


def one_unit(x, w=WS, sp=SPS, colh=COLH):
    patch = Ellipse(width=w, height=0.28, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                    fill_opacity=0.6).move_to(P(x, -2.26))
    col = Rectangle(width=w, height=colh, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                    fill_opacity=0.22).move_to(P(x, UNIT_BASE + colh / 2))
    seg = Rectangle(width=sp - 0.06, height=0.22, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                    fill_opacity=0.4).move_to(P(x, UNIT_BASE + colh + 0.12))
    return VGroup(patch, col, seg)


def b_row(n):
    return VGroup(*[one_unit(BCX + x) for x in spread(n, SPS)])


def b_name():
    return T("Species B", 36, TEXT).move_to(P(BCX, 3.4))


def b_area():
    arrow = darr(P(BCX - 2.75, 2.2), P(BCX + 2.75, 2.2), GREEN, 5, 0.2)
    lab = T("area × 8", 36, GREEN).move_to(P(BCX, 2.75))
    return arrow, lab


def b_neur():
    return T("neurons × 8", 34, YELLOW).move_to(P(BCX, -3.25))


def eq_text(s):
    return M(s, 44, GREEN).move_to(P(3.4, 2.2))


class S12Reveal(S):
    def construct(self):
        v = ventricle(label=False, y=VY)
        self.add(v)
        name = b_name()
        row = b_row(1)
        head = T("3 rounds of doubling", 34, GREY).move_to(P(3.4, 3.15))
        self.play(FadeIn(name), FadeIn(row), FadeIn(head), run_time=0.6)
        self.at("Doubling")
        cur = row
        eq = eq_text("2")
        for n, s_eq in ((2, "2"), (4, "2 × 2"), (8, "2 × 2 × 2")):
            tgt = b_row(n)
            anims = [TransformFromCopy(cur[i // 2], tgt[i]) for i in range(n)]
            if n == 2:
                anims.append(FadeIn(eq))
            else:
                anims.append(Transform(eq, eq_text(s_eq)))
            self.play(*anims, run_time=0.4)
            self.remove(cur, *list(cur))
            cur = tgt
        self.at("eight times the units")
        eq8 = eq_text("2 × 2 × 2 = 8")
        ul = T("units × 8", 38, GREEN).move_to(P(3.4, 1.2))
        self.play(Transform(eq, eq8), FadeIn(ul, shift=UP * 0.1),
                  *[u[1].animate.set_fill(YELLOW, 0.5) for u in cur], run_time=0.5)
        self.play(*[u[1].animate.set_fill(YELLOW, 0.22) for u in cur], run_time=0.3)
        self.at("so with")
        hl = T("columns: same height", 32, YELLOW).move_to(P(3.4, 0.3))
        self.play(FadeIn(hl, shift=UP * 0.1), run_time=0.5)
        self.at("same patch per unit")
        pl = T("same patch per unit", 32, GREEN).move_to(P(3.4, -0.6))
        self.play(FadeIn(pl, shift=UP * 0.1), *[u[2].animate.set_fill(GREEN, 0.9) for u in cur], run_time=0.4)
        self.play(*[u[2].animate.set_fill(GREEN, 0.4) for u in cur], run_time=0.3)
        self.at("eight times the area")
        arrow, lab = b_area()
        nl = b_neur()
        self.play(GrowFromCenter(arrow), FadeIn(lab, shift=DOWN * 0.1), FadeIn(nl, shift=UP * 0.1), run_time=0.8)
        self.finish()


def c_unit(grown=False):
    cu = one_unit(CXU)
    if grown:
        cu[1].become(Rectangle(width=WS, height=COLH * 1.03, stroke_color=YELLOW, stroke_width=3,
                               fill_color=YELLOW, fill_opacity=0.35).move_to(P(CXU, UNIT_BASE + COLH * 1.03 / 2)))
    return cu


def c_name():
    return T("Species C", 36, TEXT).move_to(P(3.4, 3.4))


def c_area():
    return T("area: no extra", 36, GREEN).move_to(P(3.4, 2.75))


def c_neur():
    return T("neurons +3%", 34, YELLOW).move_to(P(3.4, -3.25))


def c_ghost():
    return DashedLine(P(CXU - 0.45, UNIT_BASE + COLH), P(CXU + 0.45, UNIT_BASE + COLH), color=GREY,
                      stroke_width=3)


def c_cap():
    return Rectangle(width=WS, height=COLH * 0.03, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW,
                     fill_opacity=1.0).move_to(P(CXU, UNIT_BASE + COLH + COLH * 0.015))


def c_read(i):
    items = [T("neurons per unit", 28, GREY).move_to(P(4.7, 2.05)),
             M("100 → 103", 40, YELLOW).move_to(P(4.7, 1.4)),
             T("no extra units", 32, BLUE).move_to(P(4.7, 0.4))]
    return items[i]


def b_state(scene):
    """B exactly as it stands at the end of s12 (the right-hand readouts are removed)."""
    v = ventricle(label=False, y=VY)
    arrow, lab = b_area()
    row = b_row(8)
    nb = b_neur()
    scene.add(v, b_name(), row, arrow, lab, nb)
    return row, nb


class S13Reveal2(S):
    def construct(self):
        v = ventricle(label=False, y=VY)
        arrow, lab = b_area()
        row = b_row(8)
        # the right half still shows B's readouts from the last scene
        eq = eq_text("2 × 2 × 2 = 8")
        ul = T("units × 8", 38, GREEN).move_to(P(3.4, 1.2))
        hl = T("columns: same height", 32, YELLOW).move_to(P(3.4, 0.3))
        pl = T("same patch per unit", 32, GREEN).move_to(P(3.4, -0.6))
        head = T("3 rounds of doubling", 34, GREY).move_to(P(3.4, 3.15))
        old = VGroup(eq, ul, hl, pl, head)
        self.add(v, b_name(), row, arrow, lab, b_neur(), old)
        cu = c_unit()
        self.at("Species")
        self.play(FadeOut(old), FadeIn(c_name()), FadeIn(cu), run_time=0.6)
        self.at("gains about")
        h100 = M("100", 40, GREY).move_to(P(4.7, 1.4))
        self.play(FadeIn(c_read(0)), FadeIn(h100), FadeIn(c_ghost()), run_time=0.3)
        self.at("about 3")
        grown = c_unit(True)
        cap = c_cap()
        self.play(ReplacementTransform(h100, c_read(1)), Transform(cu[1], grown[1]), FadeIn(cap), run_time=0.5)
        self.at("more neurons")
        self.play(FadeIn(c_neur(), shift=UP * 0.1), Indicate(cap, color=YELLOW, scale_factor=1.3), run_time=0.5)
        self.at("no extra units")
        self.play(FadeIn(c_read(2), shift=UP * 0.1), Indicate(cu[0], color=BLUE, scale_factor=1.15), run_time=0.5)
        self.at("so no extra area")
        self.play(FadeIn(c_area(), shift=DOWN * 0.1), Indicate(cu[2], color=GREEN, scale_factor=1.1), run_time=0.5)
        self.finish()


def s13_final(scene):
    row, nb = b_state(scene)
    cu = c_unit(True)
    objs = [c_name(), cu, c_ghost(), c_cap(), c_read(0), c_read(1), c_read(2), c_area(), c_neur()]
    scene.add(*objs)
    return dict(row=row, cu=cu, neur_c=objs[-1], neur_b=nb)


class S14Beat(NarratedScene):
    def construct(self):
        s13_final(self)
        self.finish()


class S15Rule(S):
    def construct(self):
        d = s13_final(self)
        nb = d["neur_b"]
        cap_b = T("Doubling multiplies.", 36, GREEN).move_to(P(BCX, -3.25))
        cap_c = T("Adding only adds.", 36, PURPLE).move_to(P(3.4, -3.25))
        self.at("Doubling")
        self.play(ReplacementTransform(nb, cap_b), Indicate(d["row"], color=GREEN, scale_factor=1.02), run_time=0.9)
        self.at("Adding only adds")
        self.play(ReplacementTransform(d["neur_c"], cap_c), Indicate(d["cu"][1], color=PURPLE, scale_factor=1.06),
                  run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S16Ten(S):
    def construct(self):
        OX, OY = -5.2, -3.3
        u = 6.4 / 32
        kc = ValueTracker(0.0)      # how many doublings so far (continuous while a doubling plays)
        fillv = ValueTracker(0.0)

        def side(j):
            return u * 2 ** (j / 2)

        def fac(k):
            return max(6.5 * 2 ** (-k / 2), 1.0)     # zoom: starts large, settles at true size

        def nvis(k):
            return int(np.ceil(k - 1e-9))

        sqs, labs = [], []
        for j in range(11):
            sq = Square(0.3, stroke_color=GREEN)

            def f(m, j=j):
                k = kc.get_value()
                s = side(j) * fac(k)
                vis = j <= nvis(k)
                new = Square(max(s, 1e-3), stroke_color=GREEN, stroke_width=5 if j == 10 else 3,
                             stroke_opacity=1 if vis else 0, fill_color=GREEN,
                             fill_opacity=fillv.get_value() if (j == 10 and vis) else 0)
                new.move_to(P(OX + s / 2, OY + s / 2))
                m.become(new)

            sq.add_updater(f)
            sq.update()
            sqs.append(sq)
        for j in (1, 3, 6, 9, 10):
            lb = btext(f"× {2 ** j:,}", 26, GREEN)

            def lf(m, j=j):
                k = kc.get_value()
                fc = fac(k)
                s = side(j) * fc
                show = j <= nvis(k)
                if show and j < 10 and (j + 1) <= nvis(k):
                    next_label = next(n for n in (1, 3, 6, 9, 10) if n > j)
                    nxt = side(next_label) * fc
                    show = (next_label > nvis(k) or (nxt - s) >= 0.42) and nxt >= m.width + 0.3
                m.set_opacity(1 if show else 0)
                m.move_to(P(OX + 0.14 + m.width / 2, OY + s + 0.1 + m.height / 2))

            lb.add_updater(lf)
            lb.update()
            labs.append(lb)

        def readout(k):
            return VGroup(T("doublings", 30, GREY).move_to(P(4.1, 2.9)),
                          M(str(k), 80, GREEN).move_to(P(4.1, 1.95)),
                          M(f"area × {2 ** k:,}", 36, GREEN).move_to(P(4.1, 0.95)))

        ml = T("mouse: one unit", 26, GREY).move_to(P(OX + 1.45, OY - 0.32))
        ro = readout(0)
        self.add(*sqs, *labs)
        self.play(FadeIn(ml), FadeIn(ro), run_time=0.4)
        self.at("Ten doublings")
        for k in range(1, 11):
            self.remove(ro)
            ro = readout(k)
            self.add(ro)
            self.play(kc.animate.set_value(k).set_rate_func(linear), run_time=0.15)
        self.at("fold")
        two = M("2", 46, TEXT)
        sup = M("10", 28, TEXT).next_to(two, UR, buff=0.02).shift(DOWN * 0.1)
        rest = M("= 1,024", 46, TEXT).next_to(sup, RIGHT, buff=0.2).align_to(two, DOWN)
        eq = VGroup(two, sup, rest).move_to(P(4.1, -0.3))
        hl = T("human", 30, GREEN).move_to(P(OX + 5.6, OY - 0.32))
        self.play(fillv.animate.set_value(0.18), FadeIn(eq, shift=UP * 0.1), FadeIn(hl), run_time=0.4)
        self.at("with every unit the same size")
        same = T("every unit the same size", 28, GREY).move_to(P(4.1, -1.35))
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.6)
        self.at("ten extra rounds")
        gap = T("ten extra rounds\nclose the gap", 32, GOLD).move_to(P(4.1, -2.5))
        self.play(FadeIn(gap, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
BX = [-4.0, -1.35, 1.35, 4.0]
BASE = -2.45
H1 = 1.25
AXX = -5.55


def bar_(x, f, color, dashed=False):
    r = Rectangle(width=2.0, height=H1 * f, stroke_color=color, stroke_width=3, fill_color=color,
                  fill_opacity=0.0 if dashed else 0.45).move_to(P(x, BASE + H1 * f / 2))
    if dashed:
        r = DashedVMobject(r, num_dashes=40)
    return r


class S17Chimp(S):
    def construct(self):
        ax = Line(P(AXX, BASE), P(6.3, BASE), color=GREY, stroke_width=3)
        yax = Line(P(AXX, BASE), P(AXX, BASE + 4 * H1 + 0.3), color=GREY, stroke_width=3)
        ticks = VGroup()
        for n in (1, 2, 3, 4):
            ticks.add(Line(P(AXX, BASE + n * H1), P(AXX + 0.15, BASE + n * H1), color=GREY, stroke_width=3))
            ticks.add(T(str(n), 26, GREY).move_to(P(AXX - 0.32, BASE + n * H1)))
        self.add(ax, yax, ticks)
        ttl = T("brain size (chimpanzee = 1)", 32, TEXT).move_to(P(0, 3.4))
        self.play(FadeIn(ttl, shift=DOWN * 0.1), run_time=0.4)
        b1 = bar_(BX[0], 1, GREY)
        l1 = T("chimpanzee", 26, TEXT).move_to(P(BX[0], -2.95))
        v1 = T("1", 28, GREY).move_to(P(BX[0], BASE + H1 + 0.3))
        self.play(FadeIn(b1, shift=UP * 0.2), FadeIn(l1), FadeIn(v1), run_time=0.6)
        self.at("three times")
        b3 = bar_(BX[2], 3, GREY)
        l3 = T("human", 26, TEXT).move_to(P(BX[2], -2.95)).align_to(l1, DOWN)
        v3 = T("about 3×", 30, TEXT).move_to(P(BX[2], BASE + 3 * H1 + 0.35))
        self.play(GrowFromEdge(b3, DOWN), FadeIn(l3), run_time=1.0)
        self.play(FadeIn(v3, shift=DOWN * 0.1), run_time=0.3)
        self.at("our cortical area")
        ttl2 = T("CORTICAL AREA, if similar (chimpanzee = 1)", 32, GREEN).move_to(P(0, 3.4))
        self.play(ReplacementTransform(ttl, ttl2), b1.animate.set_stroke(GREEN).set_fill(GREEN, 0.45),
                  b3.animate.set_stroke(GREEN).set_fill(GREEN, 0.45),
                  v3.animate.set_color(GREEN), run_time=0.5)
        self.play(Indicate(ttl2, color=GREEN, scale_factor=1.04), run_time=0.5)
        g2 = bar_(BX[1], 2, GREEN, dashed=True)
        g4 = bar_(BX[3], 4, GREEN, dashed=True)
        l2 = T("one round", 26, GREEN).move_to(P(BX[1], -2.95)).align_to(l1, DOWN)
        l4 = T("two rounds", 26, GREEN).move_to(P(BX[3], -2.95)).align_to(l1, DOWN)
        v2 = T("2×", 30, GREEN).move_to(P(BX[1], BASE + 2 * H1 + 0.3))
        v4 = T("4×", 30, GREEN).move_to(P(BX[3] + 1.2, BASE + 4 * H1 - 0.1))
        self.play(FadeIn(g2), FadeIn(g4), FadeIn(l2), FadeIn(l4), FadeIn(v2), FadeIn(v4), run_time=0.8)
        self.at("the gap is under two rounds")
        gap = T("the gap: under two rounds", 30, GOLD).move_to(P(-1.6, 2.75))
        self.play(FadeIn(gap, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
CX = [-4.9 + 1.5 * i for i in range(7)]
BBASE = -2.5
BSC = 5.0 / 64


def pbar(i):
    h = BSC * 2 ** i
    return Rectangle(width=1.0, height=h, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                     fill_opacity=0.55).move_to(P(CX[i], BBASE + h / 2))


class S181995(S):
    def construct(self):
        card = VGroup(T("Pasko Rakic", 36, TEXT, font=TITLE_FONT), T("1995", 30, GOLD)
                      ).arrange(RIGHT, buff=0.3).move_to(P(-3.2, 3.25))
        base = Line(P(-5.75, BBASE), P(6.3, BBASE), color=GREY, stroke_width=3)
        yax = Line(P(-5.75, BBASE), P(-5.75, 2.9), color=GREY, stroke_width=3)
        fl = T("founder pool", 28, BLUE).move_to(P(-4.55, 2.6))
        xl = T("cell cycles →", 26, GREY).move_to(P(-4.3, -3.0))
        # Start zoomed to the first four cycles; all heights remain proportional.
        bars = [pbar(i) for i in range(7)]
        early = VGroup(*bars[:4])
        for i, b in enumerate(bars[:4]):
            b.stretch_to_fit_height(5.0 * 2 ** i / 8).move_to(P(CX[i], BBASE + 2.5 * 2 ** i / 8))
        sx = (CX[3] + CX[4]) / 2
        ex = CX[6] + 0.75
        mark = DashedLine(P(sx, BBASE), P(sx, 2.9), color=GOLD, stroke_width=4)
        ml = T("switch", 30, GOLD, weight=BOLD).move_to(P(sx, 3.3))
        self.add(card, base, yax, fl, xl, early, mark, ml)
        self.at("Rakic")
        self.at("A delay of")
        self.play(mark.animate.put_start_and_end_on(P(ex, BBASE), P(ex, 2.9)),
                  ml.animate.move_to(P(ex - 0.2, 3.3)), run_time=0.5)
        self.at("a few cell cycles")
        span = darr(P(sx, -3.0), P(ex, -3.0), TEAL, 4, 0.18)
        sl = T("a few cell cycles", 28, TEAL).move_to(P((sx + ex) / 2, -3.5))
        self.play(*[Transform(bars[i], pbar(i)) for i in range(4)],
                  FadeOut(fl), FadeIn(VGroup(span, sl)),
                  LaggedStart(*[GrowFromEdge(bars[i], DOWN) for i in (4, 5, 6)], lag_ratio=0.5), run_time=1.6)
        self.at("greatly enlarge the cortex")
        big = T("a delay could greatly\nenlarge the cortex", 32, GREEN).move_to(P(-2.0, 1.1))
        self.play(FadeIn(big, shift=UP * 0.1), Indicate(bars[6], color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
def blob(a, b, eps, cx=0.0, cy=0.0, color=YELLOW, fill=0.14, sw=4):
    return ParametricFunction(
        lambda th: np.array([cx + a * (1 + eps * np.sin(11 * th)) * np.cos(th),
                             cy + b * (1 + eps * np.sin(11 * th)) * np.sin(th), 0]),
        t_range=[0, TAU, 0.02], stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fill)


MCX, MCY = 0.6, -0.15


def vring(a, b, n, r=0.17):
    g = VGroup()
    for k in range(n):
        th = TAU * (k + 0.5) / n
        g.add(small_dot(MCX + a * np.cos(th), MCY + b * np.sin(th), BLUE, r))
    return g


def mouse_final():
    cortex = blob(5.0, 3.0, 0.06, MCX, MCY)
    vent = blob(2.5, 1.45, 0, MCX, MCY, color=GREY, fill=0.0, sw=3)
    ring = vring(2.5, 1.45, 12, 0.15)
    vl = T("ventricular surface", 26, BLUE).move_to(P(MCX, 1.75))
    cl = T("cortex", 28, YELLOW).move_to(P(MCX, 2.35))
    sch = T("schematic top view", 26, GREY).move_to(P(5.0, -3.55))
    ml = T("mouse cortex", 26, GREY).move_to(P(-5.2, -3.55))
    return cortex, vent, ring, vl, cl, sch, ml


class S19Mice(S):
    def construct(self):
        cortex = blob(3.2, 2.2, 0, MCX, MCY)
        vent = blob(1.3, 0.8, 0, MCX, MCY, color=GREY, fill=0.0, sw=3)
        ring = vring(1.3, 0.8, 6)
        vl = T("ventricular surface", 26, BLUE).move_to(P(MCX, 1.1))
        cl = T("cortex", 28, YELLOW).move_to(P(MCX, 1.7))
        sm = T("smooth", 30, GREY).move_to(P(-4.4, MCY))
        sch = T("schematic top view", 26, GREY).move_to(P(5.0, -3.55))
        ml = T("mouse cortex", 26, GREY).move_to(P(-5.2, -3.55))
        self.at("In mice")
        card = VGroup(T("Chenn and", 34, TEXT, font=TITLE_FONT), T("Walsh", 34, TEXT, font=TITLE_FONT),
                      T("2002", 30, GOLD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(P(-5.4, 2.55))
        self.play(FadeIn(card, shift=RIGHT * 0.2), FadeIn(cortex), FadeIn(vent), FadeIn(ring), FadeIn(sch),
                  FadeIn(ml), FadeIn(vl), FadeIn(cl), FadeIn(sm), run_time=0.9)
        self.at("a stabilized form")
        bc = T("stabilized β-catenin", 32, ORANGE).move_to(P(4.3, 3.25))
        self.play(FadeIn(bc, shift=DOWN * 0.15), run_time=0.6)
        self.at("kept more progenitors")
        ring2 = vring(1.3, 0.8, 12, 0.13)
        self.play(ReplacementTransform(ring, ring2), run_time=0.9)
        self.at("The cortex grew in area")
        cortex2 = blob(5.0, 3.0, 0, MCX, MCY)
        vent2 = blob(2.5, 1.45, 0, MCX, MCY, color=GREY, fill=0.0, sw=3)
        ring3 = vring(2.5, 1.45, 12, 0.15)
        self.play(Transform(cortex, cortex2), Transform(vent, vent2), Transform(ring2, ring3),
                  vl.animate.move_to(P(MCX, 1.75)), cl.animate.move_to(P(MCX, 2.35)), FadeOut(sm), run_time=1.2)
        self.at("buckled into folds")
        cortex3 = blob(5.0, 3.0, 0.06, MCX, MCY)
        bk = T("buckled", 30, YELLOW).move_to(P(-5.75, MCY))
        self.play(Transform(cortex, cortex3), FadeIn(bk), run_time=1.0)
        self.finish()


class S20Mice2(S):
    def construct(self):
        cortex, vent, ring, vl, cl, sch, ml = mouse_final()
        self.add(cortex, vent, ring, vl, cl, sch, ml)
        self.at("That shows extra founder")
        cap = T("extra founder divisions can enlarge the sheet", 34, GREEN).move_to(P(0, 3.45))
        self.play(FadeIn(cap, shift=DOWN * 0.15), run_time=0.7)
        self.at("not how primates did it")
        cap2 = T("not how primates did it", 34, RED).move_to(P(0, -3.55))
        self.play(FadeIn(cap2, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
OXS = [-4.4, 0.0, 4.4]
ORY = 0.95
ORAD = 1.4
TW_ = 3.6
TRY = -1.25


def organoid(x, r=ORAD):
    return Circle(radius=r, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.1).move_to(P(x, ORY))


def track(x0):
    return Rectangle(width=TW_, height=0.4, stroke_color=GREY, stroke_width=2, fill_opacity=0
                     ).move_to(P(x0 + TW_ / 2, TRY))


def fillbar(x0, w):
    return Rectangle(width=max(w, 0.02), height=0.4, stroke_width=0, fill_color=TEAL, fill_opacity=0.9
                     ).move_to(P(x0 + max(w, 0.02) / 2, TRY))


def ne_dot(x, done=False):
    if done:
        return Circle(radius=0.36, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.7
                      ).move_to(P(x, ORY))
    return Circle(radius=0.36, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to(P(x, ORY))


class S21Organoids(S):
    def construct(self):
        orgs = [organoid(x) for x in OXS]
        names = [T(n, 34, TEXT).move_to(P(x, 3.3)) for n, x in zip(("human", "chimpanzee", "gorilla"), OXS)]
        dots = [ne_dot(x) for x in OXS]
        x0 = [x - TW_ / 2 for x in OXS]
        tracks = [track(x) for x in x0]
        tl = T("time to become radial glia", 28, TEAL).move_to(P(0, -1.85))
        legend = VGroup(Circle(radius=0.17, stroke_color=TEXT, stroke_width=3, fill_opacity=0),
                        T("neuroepithelial cell", 26, TEXT),
                        T("→", 30, GREY),
                        Circle(radius=0.17, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.7),
                        T("radial glia", 26, BLUE)).arrange(RIGHT, buff=0.22).move_to(P(0, -2.55))
        self.at("In organoids")
        self.play(*[FadeIn(o) for o in orgs], *[FadeIn(n) for n in names], *[FadeIn(d) for d in dots],
                  FadeIn(legend), run_time=0.8)
        self.at("human cells")
        self.play(*[FadeIn(t) for t in tracks], FadeIn(tl), run_time=0.3)
        bars = [fillbar(x, 0) for x in x0]
        self.add(*bars)

        def grow(i, a_from, a_to, t):
            return UpdateFromAlphaFunc(bars[i], lambda m, a, i=i: m.become(fillbar(x0[i], a_from + (a_to - a_from) * a)),
                                       rate_func=linear, run_time=t)

        # apes finish (2.3 units) while the human bar keeps running (3.6 units)
        self.play(grow(0, 0, 2.3, 1.7), grow(1, 0, 2.3, 1.7), grow(2, 0, 2.3, 1.7))
        self.at("become radial glia")
        self.play(Transform(dots[1], ne_dot(OXS[1], True)), Transform(dots[2], ne_dot(OXS[2], True)),
                  grow(0, 2.3, 3.6, 1.0), run_time=1.0)
        self.play(Transform(dots[0], ne_dot(OXS[0], True)), run_time=0.3)
        self.at("human organoids")
        self.play(orgs[0].animate.scale(1.28), dots[0].animate.scale(1.0), run_time=1.3)
        self.at("Neither test")
        cap = T("neither test was done in a developing human brain", 32, RED).move_to(P(0, -3.4))
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
def idea_card():
    return RoundedRectangle(corner_radius=0.3, width=12.6, height=7.1, stroke_color=GOLD, stroke_width=3,
                            fill_color=GOLD, fill_opacity=0.04).move_to(P(0, 0))


def idea_heading():
    h1 = T("Multiply,", 68, GOLD, font=TITLE_FONT)
    h2 = T("don't add.", 68, GOLD, font=TITLE_FONT)
    return VGroup(h1, h2).arrange(RIGHT, buff=0.35).move_to(P(0, 2.7))


def idea_blocks():
    left = VGroup(*[chip("×2", GREEN, 52, 0.22, 0.2) for _ in range(3)]).arrange(RIGHT, buff=0.25).move_to(P(-3.3, 0.9))
    left_eq = T("units × 8", 50, GREEN).move_to(P(-3.3, -0.7))
    right = VGroup(*[chip("+1", PURPLE, 52, 0.22, 0.2) for _ in range(3)]).arrange(RIGHT, buff=0.25).move_to(P(3.3, 0.9))
    right_eq = T("neurons +3%", 50, PURPLE).move_to(P(3.3, -0.7))
    return VGroup(left, left_eq), VGroup(right, right_eq)


class S22Idea(S):
    def construct(self):
        h = idea_heading()
        L, R = idea_blocks()
        sub = T("Extra rounds of doubling can multiply the neurons a cortex makes.", 38, TEXT).move_to(P(0, -2.4))
        fit_w(sub, 12.0)
        self.add(idea_card())
        self.at("Multiply")
        self.play(FadeIn(h[0], shift=UP * 0.1), FadeIn(L, shift=UP * 0.1), run_time=0.7)
        self.at("don't add")
        self.play(FadeIn(h[1], shift=UP * 0.1), FadeIn(R, shift=UP * 0.1), run_time=0.7)
        self.at("Extra rounds of doubling")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        self.at("multiply the neurons")
        self.play(Indicate(L, color=GREEN, scale_factor=1.1), run_time=0.8)
        self.finish()


class S23Idea2(S):
    def construct(self):
        h = idea_heading()
        self.add(idea_card(), h)
        self.at("That is the leading explanation")
        lead = T("the leading explanation for our big cortex", 46, TEXT, font=TITLE_FONT).move_to(P(0, 1.2))
        fit_w(lead, 12.2)
        small = T("tested in animals and organoids,\nnot in a developing human brain", 32, GREY).move_to(P(0, -2.6))
        self.add(lead, small)
        self.at("nearly all of the gain")
        arrow = arr(P(-4.8, 0.15), P(4.8, 0.15), GREEN, 10, 0.45)
        al = T("nearly all of the gain went into area", 44, GREEN).move_to(P(0, -0.8))
        self.play(FadeIn(VGroup(arrow, al)), run_time=0.3)
        self.finish()


class S24Take(S):
    def construct(self):
        q = T("What does it change?", 64, GOLD, font=TITLE_FONT).move_to(P(0, 2.7))
        a = chip("every cell", BLUE, 50, 0.3).move_to(P(-3.0, 1.0))
        b = chip("every gene", ORANGE, 50, 0.3).move_to(P(3.0, 1.0))
        self.add(idea_card(), q, a, b)
        self.at("for every cell")
        self.play(Indicate(a, color=BLUE, scale_factor=1.04), run_time=0.3)
        self.at("and gene")
        self.play(Indicate(b, color=ORANGE, scale_factor=1.04), run_time=0.3)
        labels = (("more doubling", GREEN), ("more time", TEAL), ("something else?", GREY))
        options = VGroup()
        for text, color in labels:
            box = RoundedRectangle(width=3.75, height=1.0, corner_radius=0.14,
                                   stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
            label = fit_w(T(text, 34, color), 3.35).move_to(box)
            options.add(VGroup(box, label))
        options.arrange(RIGHT, buff=0.3).move_to(P(0, -1.1))
        self.at("follows")
        self.play(FadeIn(options), run_time=0.5)
        self.at("ask what it changes")
        self.play(Indicate(q, color=GOLD, scale_factor=1.03), run_time=0.5)
        self.finish()


class S25End(EndCard):
    LINE = "So for every cell and gene that follows,\nask what it changes."

    def construct(self):
        line = VGroup(*[T(part, size=40, font=TITLE_FONT) for part in self.LINE.split("\n")]).arrange(DOWN, buff=0.18)
        fit_w(line, 11.5)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        VGroup(line, sub).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
