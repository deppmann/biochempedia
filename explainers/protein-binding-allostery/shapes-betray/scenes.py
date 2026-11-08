"""When the Shapes Betray You  (chapter 6 of "Protein Binding and Allostery")

COLOR MAP (one color per concept, shared with the other chapters of this lesson)
  BLUE   = hemoglobin in the tense (T) state, the weak shape; sickle-hemoglobin molecules
  GREEN  = relaxed (R) state, the tight shape
  YELLOW = O2, the ligand
  RED    = carbon monoxide (CO) and CO-hemoglobin
  TEAL   = 2,3-BPG (recap chip only)
  GOLD   = call-outs, the sticky valine patch and the fibers it builds
  PURPLE = fetal hemoglobin (new in this chapter)
  CELL   = a red blood cell, deep crimson (new in this chapter)
  SKIN   = a hand, normal skin tone (s08 only)
  TEXT   = neutral labels (acid and CO2 chips in the recap);  GREY = axes, secondary labels
NO molecular structures are drawn: hemoglobin is four labelled blocks, a patch is a dot, a pocket is a
notch, a fiber is a row of blocks, a heme is a flat slab. Curves are computed from the Hill equation
Y = x^n / (P50^n + x^n).
"""
import numpy as np

from bp_style import *

CELL = "#D8434F"
PURPLE = "#B79CF0"
SKIN = "#D9A27E"
CHERRY = "#F2475A"

SICKLE_LABELS = ("β", "β", "α", "α")   # sickle scenes: both β on top so Val 6 (β) meets the pocket (β) side by side
DIRS = [UL, UR, DL, DR]                # each subunit's ligand sits on its outer corner, clear of the letter


# ---------------------------------------------------------------- helpers
def hill(x, p50, n):
    return x ** n / (p50 ** n + x ** n)


def badge(text, color, r):
    c = Circle(radius=r, color=color, fill_opacity=1, stroke_width=0)
    t = T(text, max(26, int(80 * r)), BG, weight=BOLD)
    if t.width > 1.45 * r:
        t.scale_to_fit_width(1.45 * r)
    return VGroup(c, t.move_to(c))


def o2(r=0.34):
    return badge("O₂", YELLOW, r)


def co(r=0.34):
    return badge("CO", RED, r)


def sub(label, color, size=1.25, op=0.18, lsize=None):
    r = RoundedRectangle(corner_radius=0.16, width=size, height=size, stroke_color=color, stroke_width=3.5,
                         fill_color=color, fill_opacity=op)
    return VGroup(r, T(label, lsize or int(28 + 12 * size / 1.25), color).move_to(r))


class Tet(VGroup):
    """Hemoglobin cartoon: four labelled blocks plus ligands on the outer corners."""

    def __init__(self, s=1.0, color=BLUE, c=ORIGIN, co_at=(), o2_at=(), labels=("α", "β", "β", "α")):
        size, gap = 1.25 * s, 0.55 * s
        d = (size + gap) / 2
        H = VGroup()
        for (x, y), lab in zip([(-d, d), (d, d), (-d, -d), (d, -d)], labels):
            H.add(sub(lab, color, size).move_to([x, y, 0]))
        H.move_to(c)
        self.r = max(0.3, 0.3 * s)
        super().__init__(H)
        self.H = H
        lig = VGroup()
        for i in co_at:
            lig.add(co(self.r).move_to(self.site(i)))
        for i in o2_at:
            lig.add(o2(self.r).move_to(self.site(i)))
        self.lig = lig
        self.add(lig)

    def site(self, i):
        return self.H[i][0].get_corner(DIRS[i]) - DIRS[i] * self.r * 0.25

    def val_pt(self):
        """Val 6 sits on the right edge of the top-right β."""
        return self.H[1][0].get_right()

    def pocket_pt(self):
        """The hydrophobic pocket is a notch in the left edge of the top-left β."""
        return self.H[0][0].get_left()


def recolor(tet, color):
    anims = []
    for s in tet.H:
        anims.append(s[0].animate.set_stroke(color).set_fill(color, 0.18))
        anims.append(s[1].animate.set_color(color))
    return anims


def popbar(fr, c=ORIGIN, w=6.0, h=0.8):
    """Population bar: fraction fr of molecules in R (green), the rest in T (blue)."""
    wt, wr = max(w * (1 - fr), 0.001), max(w * fr, 0.001)
    x0 = c[0] - w / 2
    t = Rectangle(width=wt, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.85)
    t.move_to([x0 + wt / 2, c[1], 0])
    r = Rectangle(width=wr, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
    r.move_to([x0 + wt + wr / 2, c[1], 0])
    fr_ = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(c)
    return VGroup(t, r, fr_)


def poplabels(c=ORIGIN, w=6.0, h=0.8, size=32):
    a = T("T shape", size, BLUE, weight=BOLD)
    a.move_to([c[0] - w / 2 + a.width / 2, c[1] - h / 2 - 0.4, 0])
    b = T("R shape", size, GREEN, weight=BOLD)
    b.move_to([c[0] + w / 2 - b.width / 2, c[1] - h / 2 - 0.4, 0])
    return VGroup(a, b)


def mini(s=1.0, color=BLUE, patch=True, pocket=True):
    """A small unlabelled hemoglobin: 4 blocks; a gold Val patch on the top-right edge, a pocket notch on the
    top-left edge (open when pocket=True)."""
    b = 0.55 * s
    g = 0.06 * s
    d = (b + g) / 2
    blocks = VGroup()
    for (x, y) in [(-d, d), (d, d), (-d, -d), (d, -d)]:
        blocks.add(RoundedRectangle(corner_radius=0.08, width=b, height=b, stroke_color=color, stroke_width=3,
                                    fill_color=color, fill_opacity=0.28).move_to([x, y, 0]))
    extras = VGroup()
    if pocket:
        extras.add(Circle(radius=0.15 * s, stroke_color=GOLD, stroke_width=3, fill_color=BG,
                          fill_opacity=1).move_to(blocks[0].get_left() + LEFT * 0.1 * s))
    if patch:
        extras.add(Circle(radius=0.12 * s, stroke_width=0, fill_color=GOLD, fill_opacity=1)
                   .move_to(blocks[1].get_right() + RIGHT * 0.1 * s))
    return VGroup(blocks, extras)


def mini_w(s=1.0):
    return 2 * 0.55 * s + 0.06 * s


def pitch(s=1.0):
    """Centre-to-centre spacing of docked molecules: the Val of one sits in the pocket of the next."""
    return mini_w(s) + 0.2 * s


def sickle_shape(R, k, c=ORIGIN):
    """A red cell: k=0 a round disc, k=1 a crescent (a disc with a bite taken from the right)."""
    a = Circle(radius=R).move_to(c)
    off = R * (2.3 - 1.65 * k)
    b = Circle(radius=0.86 * R).move_to(c + RIGHT * off + UP * 0.12 * R * k)
    if k < 0.02:
        a.set_style(fill_color=CELL, fill_opacity=0.6, stroke_color=CELL, stroke_width=5)
        return a
    return Difference(a, b, fill_color=CELL, fill_opacity=0.6, stroke_color=CELL, stroke_width=5)


def red_disc(R=1.2, c=ORIGIN):
    d = Circle(radius=R, fill_color=CELL, fill_opacity=0.6, stroke_color=CELL, stroke_width=5).move_to(c)
    dimple = Circle(radius=R * 0.42, fill_color=CELL, fill_opacity=0.35, stroke_width=0).move_to(c)
    return VGroup(d, dimple)


def lock_icon(c, color=RED, s=1.0):
    body = RoundedRectangle(corner_radius=0.1, width=0.9 * s, height=0.7 * s, stroke_color=color, stroke_width=5,
                            fill_color=BG, fill_opacity=1)
    arc = Arc(radius=0.28 * s, start_angle=0, angle=PI, stroke_color=color, stroke_width=6)
    arc.next_to(body, UP, buff=0)
    return VGroup(arc, body).move_to(c)


def leader(a, b, color=GREY, w=3):
    return Line(a, b, color=color, stroke_width=w)


def shield(c, color=GREEN, s=1.0):
    pts = []
    for t in np.linspace(0, 1, 30):           # right side, top to tip
        y = 0.9 - 2.1 * t
        hw = 0.85 if y > 0.15 else 0.85 * np.sqrt(max(0, 1 - ((0.15 - y) / 1.2) ** 2))
        pts.append([hw, y, 0])
    left = [[-p[0], p[1], 0] for p in reversed(pts)]
    sh = Polygon(*(pts + left), stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.25)
    tick = VMobject(stroke_color=color, stroke_width=7).set_points_as_corners(
        [[-0.38, -0.05, 0], [-0.08, -0.38, 0], [0.42, 0.35, 0]])
    return VGroup(sh, tick).scale(s).move_to(c)


def scissors(c, s=1.0, open_=0.5):
    b1 = Line(LEFT * 0.1, RIGHT * 1.0, color=TEXT, stroke_width=7).rotate(open_ / 2, about_point=ORIGIN)
    b2 = Line(LEFT * 0.1, RIGHT * 1.0, color=TEXT, stroke_width=7).rotate(-open_ / 2, about_point=ORIGIN)
    h1 = Circle(radius=0.22, color=TEXT, stroke_width=6).move_to(LEFT * 0.42 + UP * 0.25)
    h2 = Circle(radius=0.22, color=TEXT, stroke_width=6).move_to(LEFT * 0.42 + DOWN * 0.25)
    l1 = Line(LEFT * 0.1, h1.get_right(), color=TEXT, stroke_width=6)
    l2 = Line(LEFT * 0.1, h2.get_right(), color=TEXT, stroke_width=6)
    g = VGroup(b1, b2, h1, h2, l1, l2).scale(s)
    return g.shift(c - g[0].get_start() * 0)


# ---------------------------------------------------------------- cards
class S00Title(TitleCard):
    LESSON = "Protein Binding and Allostery"
    TITLE = "When the Shapes Betray You"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=24, color=TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), size=28, color=GREY)
        title = T(self.TITLE, size=72, font=TITLE_FONT)
        fit(title, max_w=12.0)
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=5)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.38)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), FadeIn(title, shift=UP * 0.15),
                  GrowFromCenter(rule), run_time=self.beat(0.35))
        self.wait(self.beat(0.4))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


class S22End(EndCard):
    LINE = "Oxygen shifting the T and R mix delivers; locking it, or a sticky T, causes disease."

    def construct(self):
        l1 = T("Oxygen shifting the T and R mix delivers;", size=50, font=TITLE_FONT)
        l2 = T("locking it, or a sticky T, causes disease.", size=50, font=TITLE_FONT)
        lines = VGroup(l1, l2).arrange(DOWN, buff=0.35)
        fit(lines, max_w=12.4)
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=5)
        site = T("biochemistrypedia.com", size=30, color=TEAL)
        g = VGroup(lines, rule, site).arrange(DOWN, buff=0.55)
        self.play(FadeIn(lines, shift=UP * 0.15), GrowFromCenter(rule), run_time=self.beat(0.25))
        self.play(FadeIn(site), run_time=self.beat(0.12))
        self.finish()


# ---------------------------------------------------------------- s01: the question
class S01Q(SpokenScene):
    def construct(self):
        title = T("When the shapes betray you", 54, GOLD, font=TITLE_FONT).move_to(UP * 3.1)
        cobig = badge("CO", RED, 1.45).move_to(LEFT * 3.4 + UP * 0.35)
        co_lab = T("carbon monoxide", 38, RED).next_to(cobig, DOWN, buff=0.45)
        co_warn = T("locks the wrong shape", 34, TEXT).next_to(co_lab, DOWN, buff=0.22)
        cell = sickle_shape(1.55, 1.0, RIGHT * 3.4 + UP * 0.35)
        c_lab = T("sickled red cell", 38, CELL).move_to([3.4, co_lab.get_y(), 0])
        c_warn = T("one shape made dangerous", 34, TEXT).next_to(c_lab, DOWN, buff=0.22)
        self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(cobig, scale=0.6), FadeIn(co_lab),
                  FadeIn(cell, scale=0.6), FadeIn(c_lab), run_time=0.9)
        self.at("holds hemoglobin")
        self.play(FadeIn(co_warn, shift=UP * 0.1), Indicate(cobig, color=RED, scale_factor=1.08), run_time=0.7)
        self.at("makes one shape")
        self.play(FadeIn(c_warn, shift=UP * 0.1), Indicate(cell, color=CELL, scale_factor=1.08), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- s02: CO binds tightly, straight on
def heme_site(c, w=2.6):
    slab = RoundedRectangle(corner_radius=0.08, width=w, height=0.32, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.5).move_to(c)
    return slab


class S02Co(SpokenScene):
    def construct(self):
        blk = RoundedRectangle(corner_radius=0.3, width=11.6, height=4.6, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.14).move_to(UP * 0.55)
        b_lab = T("one hemoglobin subunit", 30, BLUE).next_to(blk.get_corner(UL), DR, buff=0.25)
        hl, hr = LEFT * 2.9 + DOWN * 0.8, RIGHT * 2.9 + DOWN * 0.8
        h1, h2 = heme_site(hl), heme_site(hr)
        hm1 = T("heme", 30, GREY).next_to(h1, DOWN, buff=0.22)
        hm2 = T("heme", 30, GREY).next_to(h2, DOWN, buff=0.22)
        c = co(0.55).move_to(RIGHT * 2.9 + UP * 3.45)
        o = o2(0.55).move_to(LEFT * 2.9 + UP * 3.45)
        self.add(blk, b_lab, h1, h2, hm1, hm2)
        self.play(FadeIn(c, shift=DOWN * 0.3), FadeIn(o, shift=DOWN * 0.3), run_time=0.6)
        self.at("binds the heme")
        stick_c = Line(hr + UP * 0.16, hr + UP * 1.45, color=RED, stroke_width=8)
        tip_o = hl + UP * 0.16 + np.array([np.cos(PI / 3), np.sin(PI / 3), 0]) * 1.45
        stick_o = Line(hl + UP * 0.16, tip_o, color=YELLOW, stroke_width=8)
        self.play(c.animate.move_to(stick_c.get_end() + UP * 0.5), Create(stick_c),
                  o.animate.move_to(tip_o + np.array([np.cos(PI / 3), np.sin(PI / 3), 0]) * 0.5), Create(stick_o),
                  run_time=1.0, rate_func=smooth)
        sl = T("CO: straight on", 32, RED).next_to(c, LEFT, buff=0.4)
        ol = T("O₂: bent", 32, YELLOW).next_to(o, LEFT, buff=0.4)
        self.play(FadeIn(sl), FadeIn(ol), run_time=0.5)
        self.at("250")
        cap = VGroup(T("about 250-fold tighter than", 42, RED), o2(0.42)).arrange(RIGHT, buff=0.3)
        cap.move_to(DOWN * 2.9)
        self.play(FadeIn(cap[0], shift=UP * 0.1), run_time=0.6)
        self.at("than oxygen")
        self.play(FadeIn(cap[1], scale=0.5), Indicate(stick_c, color=RED), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- s03: CO favors R
class S03CoR(SpokenScene):
    def construct(self):
        t = Tet(1.2, BLUE, UP * 1.3)
        bc = DOWN * 2.15
        cap = T("the mix of shapes", 32, TEXT).move_to(bc + UP * 0.85)
        pb = popbar(0.3, bc, 11.6, 0.9)
        pl = poplabels(bc, 11.6, 0.9)
        self.add(t, cap, pb, pl)
        c = co(t.r).move_to(t.site(1) + RIGHT * 2.2 + UP * 0.6)
        self.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.4)
        self.play(c.animate.move_to(t.site(1)), run_time=0.6)
        self.at("favors R")
        fav = T("favors R", 44, GREEN, weight=BOLD).next_to(t, RIGHT, buff=1.2).shift(UP * 0.5)
        arr = Arrow(fav.get_left() + LEFT * 0.05, c.get_right() + RIGHT * 0.1, color=GREEN, buff=0.1, stroke_width=5)
        self.play(FadeIn(fav, shift=LEFT * 0.1), GrowArrow(arr), run_time=0.6)
        self.at("shifts the mix")
        self.play(Transform(pb, popbar(0.85, bc, 11.6, 0.9)), *recolor(t, GREEN), run_time=1.3, rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------- s04: predict
def predict_layout():
    t = Tet(1.5, BLUE, LEFT * 0.9 + UP * 0.2, co_at=(1,), o2_at=(0, 2, 3))
    pred = T("Predict", 44, GOLD, weight=BOLD).move_to(UP * 3.45)
    cl = T("carbon monoxide", 36, RED).next_to(t.lig[0], RIGHT, buff=0.3)
    ol = T("oxygen", 36, YELLOW).next_to(t.lig[1], LEFT, buff=0.3)
    q = T("Held more tightly, or less tightly?", 42, GOLD).move_to(DOWN * 3.2)
    return t, pred, cl, ol, q


class S04Predict(SpokenScene):
    def construct(self):
        t, pred, cl, ol, q = predict_layout()
        self.play(FadeIn(pred), FadeIn(t.H), run_time=0.6)
        self.at("one subunit")
        self.play(FadeIn(t.lig[0], shift=LEFT * 0.6), run_time=0.7)
        self.at("carbon monoxide")
        self.play(FadeIn(cl), run_time=0.4)
        self.at("the oxygen on")
        self.play(LaggedStart(*[FadeIn(o, scale=0.5) for o in t.lig[1:]], lag_ratio=0.25), FadeIn(ol), run_time=0.9)
        self.at("held more")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s05: the pause (question held, countdown)
class S05Pause(NarratedScene):
    def construct(self):
        t, pred, cl, ol, q = predict_layout()
        self.add(pred, t, cl, ol, q)
        qc = RIGHT * 4.6 + DOWN * 0.9
        qm = T("?", 110, GOLD, weight=BOLD).move_to(qc)
        tr = ValueTracker(1.0)
        ring = always_redraw(lambda: Arc(radius=1.0, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.001),
                                         stroke_color=GOLD, stroke_width=8).move_arc_center_to(qc))
        base = Circle(radius=1.0, stroke_color=GREY, stroke_width=3).move_to(qc)
        self.add(base, ring, qm)
        self.play(tr.animate.set_value(0.0),
                  Succession(*[Indicate(qm, color=GOLD, scale_factor=1.15, run_time=1.0) for _ in range(4)]),
                  run_time=4.6, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- s06: reveal
class S06Reveal(SpokenScene):
    def construct(self):
        t, pred, cl, ol, q = predict_layout()
        self.add(pred, t, cl, ol, q)
        a = T("More tightly.", 52, GREEN, weight=BOLD).move_to(q)
        self.play(FadeOut(q), FadeIn(a), FadeOut(pred), run_time=0.5)
        self.at("held in R")
        r_lab = T("held in R", 40, GREEN, weight=BOLD).move_to(RIGHT * 4.3 + DOWN * 0.6)
        self.play(*recolor(t, GREEN), FadeIn(r_lab), run_time=0.8)
        self.at("so its oxygen")
        stay = T("O₂ stays aboard", 36, YELLOW).next_to(r_lab, DOWN, buff=0.3)
        self.play(FadeIn(stay, shift=UP * 0.1),
                  *[Wiggle(o, scale_value=1.15, rotation_angle=0.04 * TAU) for o in t.lig[1:]], run_time=0.8)
        # the curve: plot fills the frame
        ax = Axes(x_range=[0, 100, 10], y_range=[0, 1, 0.5], x_length=9.6, y_length=5.0, tips=False,
                  axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 3})
        ax.move_to(RIGHT * 0.75 + DOWN * 0.15)
        deco = VGroup()
        for v in (0, 50, 100):
            deco.add(M(str(v), 28, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.15))
        for v, s_ in ((0.5, "0.5"), (1, "1")):
            deco.add(M(s_, 28, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.15))
        deco.add(T("pO₂ (torr)", 30, GREY).next_to(ax.x_axis, DOWN, buff=0.62))
        deco.add(T("O₂ sites filled", 30, GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.85))
        normal = ax.plot(lambda x: hill(x, 26, 2.8), x_range=[0, 100, 0.5], color=BLUE, stroke_width=6)
        mus = DashedLine(ax.c2p(20, 0), ax.c2p(20, 1), color=YELLOW, stroke_width=3)
        mus_l = T("muscle", 28, YELLOW).next_to(ax.c2p(20, 0.07), RIGHT, buff=0.12)
        n_lab = T("normal blood", 30, BLUE).next_to(ax.c2p(37, 0.42), RIGHT, buff=0)
        n_ld = leader(n_lab.get_left() + LEFT * 0.05, ax.c2p(31, 0.6), BLUE)
        self.at("released far")
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(26, 0.5), color=GREY, stroke_width=2)
        d_n = Dot(ax.c2p(26, 0.5), radius=0.1, color=BLUE)
        self.play(FadeOut(VGroup(t, cl, ol, a, r_lab, stay)), FadeIn(ax), FadeIn(deco), run_time=0.4)
        self.play(Create(normal), FadeIn(mus), FadeIn(mus_l), run_time=0.8)
        self.play(FadeIn(n_lab), Create(n_ld), Create(half), FadeIn(d_n), run_time=0.4)
        self.at("the curve")
        shifted = ax.plot(lambda x: hill(x, 12, 2.2), x_range=[0, 100, 0.5], color=RED, stroke_width=6)
        moving = normal.copy().set_color(RED)
        d_c = Dot(ax.c2p(12, 0.5), radius=0.1, color=RED)
        sh_arr = Arrow(ax.c2p(25, 0.5), ax.c2p(13, 0.5), color=RED, buff=0.05, stroke_width=5,
                       max_tip_length_to_length_ratio=0.35)
        c_lab = VGroup(T("one CO aboard", 30, RED), T("(O₂ on the other three sites)", 28, RED)) \
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        c_lab.next_to(ax.c2p(1, 1.0), UR, buff=0.15)
        c_ld = leader(c_lab.get_bottom() + LEFT * 0.4 + DOWN * 0.05, ax.c2p(15, 0.66), RED)
        self.play(Transform(moving, shifted), GrowArrow(sh_arr), FadeIn(c_lab), Create(c_ld), run_time=0.9,
                  rate_func=smooth)
        self.play(FadeIn(d_c), run_time=0.2)
        self.wait(1.2)   # let the shifted curve land before the next scene
        self.finish()


# ---------------------------------------------------------------- s07: two harms
class S07Double(SpokenScene):
    def construct(self):
        t = Tet(1.5, GREEN, RIGHT * 0.3 + UP * 0.3, co_at=(1,), o2_at=(0, 2, 3))
        self.add(t)
        self.at("takes sites away")
        box = SurroundingRectangle(VGroup(t.H[1], t.lig[0]), color=RED, buff=0.12, stroke_width=6)
        lab1 = VGroup(T("one site lost", 36, RED), T("to CO", 36, RED)).arrange(DOWN, buff=0.1)
        lab1.next_to(box, RIGHT, buff=0.7).shift(DOWN * 0.3)
        arr1 = Arrow(lab1.get_left() + LEFT * 0.05, box.get_right() + RIGHT * 0.02, color=RED, buff=0.1, stroke_width=5)
        self.play(Create(box), FadeIn(lab1, shift=LEFT * 0.1), GrowArrow(arr1), run_time=0.9)
        self.at("makes the oxygen")
        rings = VGroup(*[Circle(radius=t.r + 0.12, stroke_color=GOLD, stroke_width=6).move_to(t.lig[i]) for i in (1, 2, 3)])
        lab2 = VGroup(T("remaining O₂", 36, YELLOW), T("held tighter", 36, GOLD), T("(all three)", 30, GOLD)) \
            .arrange(DOWN, buff=0.1).move_to(LEFT * 4.8 + UP * 0.2)
        p_ul, p_dl, p_dr = (t.lig[i].get_center() for i in (1, 2, 3))
        a1 = Arrow(lab2.get_corner(UR) + LEFT * 0.2, p_ul + DL * (t.r + 0.1), color=GOLD, buff=0.1, stroke_width=5)
        a2 = Arrow(lab2.get_corner(DR) + LEFT * 0.2, p_dl + UL * (t.r + 0.1) + LEFT * 0.1, color=GOLD, buff=0.1, stroke_width=5)
        a3 = CurvedArrow(lab2.get_bottom() + DOWN * 0.1, p_dr + DOWN * (t.r + 0.18), color=GOLD, stroke_width=5,
                         angle=PI * 0.5)
        self.play(Create(rings), FadeIn(lab2, shift=RIGHT * 0.1), GrowArrow(a1), GrowArrow(a2), Create(a3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- s08: bright red
def vial(c, h=4.4, w=1.7):
    body = Union(Rectangle(width=w, height=h - w / 2).shift(UP * w / 4), Circle(radius=w / 2).shift(DOWN * (h / 2 - w / 2)))
    body.set_style(stroke_color=GREY, stroke_width=5, fill_opacity=0)
    blood = Intersection(body.copy(), Rectangle(width=w * 1.2, height=h * 0.72).shift(DOWN * h * 0.14),
                         fill_color=RED, fill_opacity=0.95, stroke_width=0)
    cap = RoundedRectangle(corner_radius=0.1, width=w + 0.3, height=0.55, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.6).next_to(body, UP, buff=-0.05)
    return VGroup(blood, body, cap).move_to(c)


def hand(c, color=SKIN, s=1.0):
    palm = RoundedRectangle(corner_radius=0.35, width=1.9, height=2.0, fill_color=color, fill_opacity=0.9,
                            stroke_width=0).move_to(UP * 0.3)
    fingers = VGroup()
    for i, (dx, ln) in enumerate([(-0.7, 1.1), (-0.23, 1.35), (0.23, 1.3), (0.68, 1.05)]):
        fingers.add(RoundedRectangle(corner_radius=0.2, width=0.42, height=ln, fill_color=color, fill_opacity=0.9,
                                     stroke_width=0).move_to([dx, 1.3 + ln / 2 - 0.25, 0]))
    thumb = RoundedRectangle(corner_radius=0.2, width=0.45, height=1.2, fill_color=color, fill_opacity=0.9,
                             stroke_width=0).rotate(0.75).move_to([-1.2, 0.35, 0])
    arm = Rectangle(width=1.5, height=2.2, fill_color=color, fill_opacity=0.9, stroke_width=0).move_to(DOWN * 1.65)
    return VGroup(arm, palm, thumb, *fingers).scale(s).move_to(c)


class S08Red(SpokenScene):
    def construct(self):
        v = vial(LEFT * 3.4 + UP * 0.4)
        v_lab = VGroup(T("CO-hemoglobin:", 36, RED), T("bright red", 36, RED)).arrange(DOWN, buff=0.1)
        v_lab.next_to(v, DOWN, buff=0.3)
        self.play(FadeIn(v, scale=0.92), run_time=0.6)
        self.at("bright red")
        self.play(FadeIn(v_lab), Indicate(v[0], color=RED, scale_factor=1.03), run_time=0.6)
        self.at("cherry red skin")
        hd = hand(RIGHT * 3.3 + UP * 0.55, CHERRY, 1.05)
        h_lab = T("cherry-red skin", 36, CHERRY).next_to(hd, DOWN, buff=0.3).align_to(v_lab, UP)
        self.play(FadeIn(hd, shift=UP * 0.2), FadeIn(h_lab), run_time=0.8)
        self.at("rarely seen")
        rare = T("rarely seen in living patients", 34, GOLD).next_to(h_lab, DOWN, buff=0.25)
        self.play(*[m.animate.set_fill(SKIN, 0.9) for m in hd], FadeIn(rare, shift=UP * 0.1), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------- s09: the oximeter
class S09Oxim(SpokenScene):
    def construct(self):
        cA = chip("O₂-Hb", YELLOW, 36).move_to(LEFT * 5.2 + UP * 1.7)
        cB = chip("CO-Hb", RED, 36).move_to(LEFT * 5.2 + DOWN * 0.6)
        body = RoundedRectangle(corner_radius=0.4, width=4.2, height=3.0, stroke_color=GREY, stroke_width=5,
                                fill_color=GREY, fill_opacity=0.14).move_to(LEFT * 0.4 + UP * 0.55)
        finger = RoundedRectangle(corner_radius=0.35, width=2.4, height=0.75, fill_color=SKIN, fill_opacity=0.9,
                                  stroke_width=0).next_to(body, DOWN, buff=-0.45).shift(RIGHT * 1.8)
        scr = T("SpO₂", 44, TEXT).move_to(body.get_center() + UP * 0.35)
        o_lab = T("fingertip pulse oximeter", 32, GREY).next_to(body, DOWN, buff=0.55)
        self.add(body, scr, o_lab, cA, cB)
        self.add_foreground_mobject(body)
        self.at("cannot tell")
        a1 = Arrow(cA.get_right() + RIGHT * 0.1, body.get_left() + UP * 0.5, color=YELLOW, buff=0.08, stroke_width=5)
        a2 = Arrow(cB.get_right() + RIGHT * 0.1, body.get_left() + DOWN * 0.5, color=RED, buff=0.08, stroke_width=5)
        same = T("looks the same to it", 34, GOLD).next_to(o_lab, DOWN, buff=0.3)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.5)
        self.at("reads falsely")
        read = VGroup(T("SpO₂", 44, TEXT), M("98%", 50, GREEN)).arrange(RIGHT, buff=0.3).move_to(scr)
        ex = T("example reading", 28, GREY).move_to(body.get_center() + DOWN * 0.7)
        norm = T("falsely normal", 38, GREEN).move_to(same)
        self.play(Transform(scr, read), FadeIn(ex), FadeOut(same), FadeIn(norm, shift=UP * 0.1), run_time=0.6)
        cells = VGroup(*[RoundedRectangle(corner_radius=0.14, width=1.0, height=1.0, stroke_color=YELLOW,
                                          stroke_width=3, fill_color=YELLOW, fill_opacity=0.85) for _ in range(6)])
        cells.arrange_in_grid(2, 3, buff=0.2).move_to(RIGHT * 4.55 + UP * 0.55)
        cl = T("muscle cells", 34, YELLOW).next_to(cells, UP, buff=0.35)
        self.play(FadeIn(cells), FadeIn(cl), run_time=0.4)
        self.at("tissues suffocate")
        starve = T("starved of O₂", 34, RED).next_to(cells, DOWN, buff=0.35)
        self.play(*[c.animate.set_fill(YELLOW, 0.06).set_stroke(GREY, 3) for c in cells], FadeIn(starve),
                  Indicate(scr[1], color=GREEN, scale_factor=1.1), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------- s10: treat
def mask_icon(c, s=1.0):
    """Oxygen mask: a face, a rounded mask over nose and mouth, a strap around the head, a hose to a tank."""
    MASK = "#9FE3F5"
    head = Circle(radius=1.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([0, 0.35, 0])
    eyes = VGroup(Dot([-0.38, 0.75, 0], radius=0.07, color=GREY), Dot([0.38, 0.75, 0], radius=0.07, color=GREY))
    cup = Ellipse(width=1.5, height=1.15, stroke_color=WHITE, stroke_width=5, fill_color=MASK,
                  fill_opacity=0.85).move_to([0, -0.05, 0])
    vent = Circle(radius=0.17, stroke_color=WHITE, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([0, -0.05, 0])
    strap = VGroup(Line([-0.72, 0.1, 0], [-1.2, 0.5, 0], stroke_color=MASK, stroke_width=8),
                   Line([0.72, 0.1, 0], [1.2, 0.5, 0], stroke_color=MASK, stroke_width=8))
    tube = CubicBezier([0, -0.62, 0], [0, -1.5, 0], [0.5, -2.0, 0], [1.3, -2.0, 0], stroke_color=MASK, stroke_width=9)
    tank = RoundedRectangle(corner_radius=0.2, width=0.6, height=1.2, stroke_color=WHITE, stroke_width=4,
                            fill_color=MASK, fill_opacity=0.6).rotate(PI / 2).move_to([1.9, -2.0, 0])
    return VGroup(head, eyes, strap, tube, tank, cup, vent).scale(s).move_to(c)


class S10Treat(SpokenScene):
    def construct(self):
        t = Tet(1.3, GREEN, RIGHT * 2.9 + DOWN * 0.1, co_at=(1,))
        mk = mask_icon(LEFT * 4.8 + UP * 0.95, 1.0)
        m_lab = T("oxygen mask", 34, YELLOW).next_to(mk, DOWN, buff=0.3)
        self.add(t, mk, m_lab)
        self.at("high concentration")
        hi = T("high-concentration O₂", 40, YELLOW).move_to(UP * 3.35)
        start = np.array([mk[0].get_right()[0] + 0.5, mk[5].get_y(), 0])
        flood = [o2(t.r).move_to(start + RIGHT * 0.5 * i + UP * (0.8 - 0.55 * i)) for i in range(4)]
        self.play(FadeIn(hi, shift=DOWN * 0.1), LaggedStart(*[FadeIn(o, shift=RIGHT * 0.4) for o in flood], lag_ratio=0.2),
                  run_time=0.9)
        self.at("to compete")
        co_badge = t.lig[0]
        # first O2 goes for the CO site and knocks the CO off; the others fill the empty sites
        self.play(flood[0].animate.move_to(t.site(1) + LEFT * 0.9 + UP * 0.2), *[o.animate.move_to(t.site(i))
                  for o, i in zip(flood[1:], (0, 2, 3))], run_time=0.9, rate_func=smooth)
        self.play(flood[0].animate.move_to(t.site(1)), co_badge.animate.shift(RIGHT * 0.9 + UP * 0.9), run_time=0.5)
        self.play(co_badge.animate.shift(RIGHT * 0.9 + UP * 0.9).set_opacity(0), run_time=0.7, rate_func=smooth)
        self.remove(co_badge)
        self.at("back off")
        back = T("CO competed back off", 38, YELLOW).move_to(DOWN * 3.25)
        self.play(FadeIn(back, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s11: sickle, the T shape turns sticky
class S11Sickle(SpokenScene):
    def construct(self):
        title = T("Sickle-cell disease", 48, GOLD, font=TITLE_FONT).move_to(UP * 3.4)
        t = Tet(1.45, BLUE, DOWN * 0.35 + LEFT * 0.6, labels=SICKLE_LABELS)
        self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(t), run_time=0.7)
        self.at("shape itself")
        tl = T("T shape", 44, BLUE, weight=BOLD).next_to(t, LEFT, buff=0.5)
        self.play(FadeIn(tl), run_time=0.4)
        self.at("sticky")
        patch = Circle(radius=0.32, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(t.val_pt())
        sl = T("sticky spot", 42, GOLD).next_to(patch, RIGHT, buff=0.6)
        sld = leader(sl.get_left() + LEFT * 0.05, patch.get_right() + RIGHT * 0.05, GOLD)
        self.play(FadeIn(patch, scale=0.3), FadeIn(sl), Create(sld), run_time=0.5)
        for _ in range(2):
            glow = Circle(radius=0.32, stroke_color=GOLD, stroke_width=6).move_to(patch)
            self.play(glow.animate.scale(2.8).set_stroke(opacity=0), run_time=0.6)
            self.remove(glow)
        self.finish()


# ---------------------------------------------------------------- s12: the mutation
class S12Mut(SpokenScene):
    def construct(self):
        res = ["Val", "His", "Leu", "Thr", "Pro", "Glu", "Glu", "Lys", "Ser", "Ala"]
        w, y = 1.18, -0.45
        boxes = VGroup(*[Rectangle(width=w, height=1.3, stroke_color=GREY, stroke_width=3, fill_opacity=0) for _ in range(10)])
        boxes.arrange(RIGHT, buff=0).move_to(UP * y)
        nums = VGroup(*[M(str(i + 1), 28, GREY).next_to(b, UP, buff=0.15) for i, b in enumerate(boxes)])
        names = VGroup(*[T(r, 30, TEXT).move_to(b) for r, b in zip(res, boxes)])
        bc = T("β chain", 36, BLUE).next_to(boxes, DOWN, buff=0.4).align_to(boxes, LEFT)
        b6 = boxes[5]
        self.add(boxes, nums, names)
        self.at("amino acid changes")
        self.play(b6.animate.set_stroke(GOLD, 7), nums[5].animate.set_color(GOLD), run_time=0.6)
        self.at("glutamate")
        glu = VGroup(chip("Glu", TEXT, 60), T("glutamate", 38, TEXT)).arrange(DOWN, buff=0.15)
        glu.move_to(LEFT * 2.6 + UP * 2.55)
        self.play(FadeIn(glu, shift=DOWN * 0.15), Indicate(names[5], color=GOLD), run_time=0.6)
        self.at("valine")
        val = VGroup(chip("Val", GOLD, 60), T("valine", 38, GOLD)).arrange(DOWN, buff=0.15)
        val.move_to(RIGHT * 2.6 + UP * 2.55)
        arr = Arrow(glu[0].get_right(), val[0].get_left(), color=GOLD, buff=0.3, stroke_width=6)
        new6 = T("Val", 30, GOLD, weight=BOLD).move_to(b6)
        self.play(GrowArrow(arr), FadeIn(val, shift=LEFT * 0.2), Transform(names[5], new6), run_time=0.8)
        self.at("position 6")
        pos = T("position 6", 36, GOLD).next_to(b6, DOWN, buff=0.4)
        self.play(FadeIn(pos, shift=UP * 0.1), run_time=0.4)
        self.at("beta chain")
        self.play(FadeIn(bc), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- s13: the patch meets the pocket
def val_dot(tet):
    return Circle(radius=0.26, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(tet.val_pt())


DOCK = 0.45      # the valine centre sits this far left of the pocket centre: a small gap between the boxes


def pocket_open(tet, r=0.32):
    """A visible notch bitten out of the left edge of the neighbour's top-left box."""
    return Circle(radius=r, stroke_color=GOLD, stroke_width=5, fill_color=BG, fill_opacity=1) \
        .move_to(tet.pocket_pt() + RIGHT * 0.2)


def pocket_closed(tet):
    p = tet.pocket_pt() + RIGHT * 0.12
    return RoundedRectangle(corner_radius=0.05, width=0.14, height=0.6, stroke_width=0, fill_color=GREY,
                            fill_opacity=1).move_to(p)


S13_S = 1.2
S13_A = LEFT * 3.5 + DOWN * 0.15
S13_B = RIGHT * 3.0 + DOWN * 0.15


class S13Patch(SpokenScene):
    def construct(self):
        A = Tet(S13_S, GREEN, S13_A, labels=SICKLE_LABELS)
        B = Tet(S13_S, GREEN, S13_B, labels=SICKLE_LABELS)
        va = val_dot(A)
        pc = pocket_closed(B)
        v_lab = T("Val 6", 34, GOLD).move_to([-1.0, 2.3, 0])
        v_ld = leader(v_lab.get_bottom() + DOWN * 0.05, va.get_top() + UP * 0.04, GOLD)
        pc_lab = T("pocket closed", 32, GREY).move_to([0.55, 3.05, 0])
        pc_ld = leader(pc_lab.get_bottom() + DOWN * 0.05 + RIGHT * 0.4, pc.get_top() + UP * 0.04 + LEFT * 0.05, GREY)
        pc_lab2 = T("pocket opens", 32, GOLD).move_to(pc_lab)
        pc_ld2 = leader(pc_lab2.get_bottom() + DOWN * 0.05 + RIGHT * 0.4, pc.get_top() + UP * 0.04 + LEFT * 0.05, GOLD)
        a_lab = T("R shape", 36, GREEN, weight=BOLD).next_to(A, DOWN, buff=0.35)
        b_lab = T("neighbor, R shape", 36, GREEN, weight=BOLD).next_to(B, DOWN, buff=0.35)
        self.add(A, B, va, pc, a_lab, b_lab)
        self.play(FadeIn(v_lab), Create(v_ld), FadeIn(pc_lab), Create(pc_ld), run_time=0.5)
        self.at("in every state")
        every = T("Val 6 is on the surface in every state", 34, GOLD).move_to(DOWN * 3.35)
        self.play(*recolor(A, BLUE), *recolor(B, BLUE),
                  Transform(a_lab, T("T shape", 36, BLUE, weight=BOLD).move_to(a_lab)),
                  Transform(b_lab, T("neighbor, T shape", 36, BLUE, weight=BOLD).move_to(b_lab)),
                  FadeIn(every), ReplacementTransform(pc_lab, pc_lab2), ReplacementTransform(pc_ld, pc_ld2),
                  Transform(pc, pocket_open(B, 0.2)), run_time=0.9)
        self.play(Indicate(va, color=GOLD, scale_factor=1.4), run_time=0.6)
        self.at("hydrophobic pocket")
        po = pocket_open(B)
        p_lab = VGroup(T("hydrophobic pocket opens", 32, GOLD), T("(Phe 85, Leu 88)", 30, GOLD)) \
            .arrange(DOWN, buff=0.08).move_to([0.45, 3.15, 0])
        p_ld = leader(p_lab.get_bottom() + DOWN * 0.05 + RIGHT * 0.5, po.get_top() + UP * 0.04 + LEFT * 0.05, GOLD)
        self.play(FadeOut(pc), GrowFromCenter(po), FadeOut(pc_lab2), FadeOut(pc_ld2), FadeOut(every),
                  FadeIn(p_lab), Create(p_ld), run_time=0.8)
        self.at("plugs in")
        dx = po.get_center()[0] - DOCK - va.get_center()[0]
        self.play(FadeOut(v_lab), FadeOut(v_ld), VGroup(A, va, a_lab).animate.shift(RIGHT * dx),
                  run_time=1.0, rate_func=smooth)
        self.play(Flash(po, color=GOLD, line_length=0.35, flash_radius=0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- s14: fibers
class S14Fiber(SpokenScene):
    def construct(self):
        # carry over the docked pair from s13, then show it as two small molecules in a row
        A = Tet(S13_S, BLUE, S13_A, labels=SICKLE_LABELS)
        B = Tet(S13_S, BLUE, S13_B, labels=SICKLE_LABELS)
        po = pocket_open(B)
        A.shift(RIGHT * (po.get_center()[0] - DOCK - A.val_pt()[0]))
        pair = VGroup(A, val_dot(A), B, po)
        self.add(pair)
        sc = 1.45
        pw = pitch(sc)
        y = 0.7
        xs = [(i - 2.5) * pw for i in range(6)]

        def place(i):
            return mini(sc).move_to([xs[i], y, 0])

        m2, m3 = place(2), place(3)
        m4 = place(4).shift(RIGHT * 1.5)
        vl = T("Val 6", 36, GOLD).move_to([m3[1][1].get_x() - 0.95, y + 1.75, 0])
        vld = leader(vl.get_bottom() + DOWN * 0.05, m3[1][1].get_top() + UP * 0.04, GOLD)
        pk = T("pocket", 36, GOLD).move_to([m4[1][0].get_x() + 1.25, y + 1.75, 0])
        pkd = leader(pk.get_bottom() + DOWN * 0.05, m4[1][0].get_top() + UP * 0.04, GOLD)
        self.play(FadeOut(pair), run_time=0.3)
        self.play(FadeIn(VGroup(m2, m3)), FadeIn(m4, shift=LEFT * 0.5), run_time=0.4)
        self.play(FadeIn(vl), Create(vld), FadeIn(pk), Create(pkd), run_time=0.4)
        self.at("next")
        self.play(m4.animate.shift(LEFT * 1.5), VGroup(pk, pkd).animate.shift(LEFT * 1.5),
                  run_time=0.8, rate_func=smooth)
        self.at("polymerize")
        extra = [place(1), place(0), place(5)]
        offs = [LEFT * 0.6, LEFT * 0.6, RIGHT * 0.6]
        for m, o in zip(extra, offs):
            m.shift(o)
        self.play(LaggedStart(*[FadeIn(m, shift=-o * 0.6) for m, o in zip(extra, offs)], lag_ratio=0.3),
                  FadeOut(vl), FadeOut(vld), FadeOut(pk), FadeOut(pkd), run_time=0.9)
        self.play(*[m.animate.shift(-o) for m, o in zip(extra, offs)], run_time=0.6, rate_func=smooth)
        chain = VGroup(extra[1], extra[0], m2, m3, m4, extra[2])
        self.at("stiff fibers")
        rod = RoundedRectangle(corner_radius=0.3, width=chain.width + 0.4, height=chain.height + 0.4,
                               stroke_color=GOLD, stroke_width=6).move_to(chain)
        r_lab = T("stiff fiber", 40, GOLD).next_to(rod, UP, buff=0.25)
        self.play(Create(rod), FadeIn(r_lab), run_time=0.6)
        self.at("that deform")
        fib = VGroup(chain, rod)
        cc = DOWN * 1.2 + LEFT * 0.8
        R = 2.55
        k = ValueTracker(0.0)
        cell = always_redraw(lambda: sickle_shape(R, k.get_value(), cc))

        def fibers():
            kk = k.get_value()
            g = VGroup()
            for xo in (-0.42, -0.66):
                p1 = cc + np.array([R * (xo + 0.28 * kk), 0.62 * R, 0])
                p2 = cc + np.array([R * (xo + 0.28 * kk), -0.62 * R, 0])
                g.add(ArcBetweenPoints(p1, p2, angle=1.3 * kk + 0.001, stroke_color=GOLD, stroke_width=6))
            return g

        fl = always_redraw(fibers)
        c_lab = T("red cell", 40, CELL).move_to(RIGHT * 4.6 + DOWN * 1.2)
        f_lab = T("fibers inside", 32, GOLD).move_to(LEFT * 5.6 + DOWN * 1.2)
        r_new = T("stiff fiber", 32, GOLD).move_to(UP * 3.55 + LEFT * 4.6)
        self.play(fib.animate.scale(0.62).move_to(UP * 2.85 + RIGHT * 1.2), Transform(r_lab, r_new), run_time=0.6)
        self.play(FadeIn(cell), FadeIn(fl), FadeIn(c_lab), FadeIn(f_lab), run_time=0.5)
        self.at("into a crescent")
        c2 = T("crescent", 40, CELL).move_to(c_lab)
        self.play(k.animate.set_value(1.0), Transform(c_lab, c2), run_time=1.2, rate_func=smooth)
        self.wait(0.6)
        self.finish()


# ---------------------------------------------------------------- s15: triggers
def runner(c, k=1.5):
    head = Circle(radius=0.3 * k, color=TEXT, stroke_width=6, fill_color=TEXT, fill_opacity=1).move_to(c + (UP * 1.45 + RIGHT * 0.35) * k)
    hip = c + DOWN * 0.3 * k
    neck = c + (UP * 1.1 + RIGHT * 0.25) * k
    body = Line(neck, hip, color=TEXT, stroke_width=7)
    sh = c + (UP * 0.85 + RIGHT * 0.2) * k
    arms = VGroup(Line(sh, sh + (RIGHT * 0.55 + DOWN * 0.1) * k, color=TEXT, stroke_width=7),
                  Line(sh + (RIGHT * 0.55 + DOWN * 0.1) * k, sh + (RIGHT * 0.75 + UP * 0.4) * k, color=TEXT, stroke_width=7),
                  Line(sh, sh + (LEFT * 0.5 + DOWN * 0.35) * k, color=TEXT, stroke_width=7),
                  Line(sh + (LEFT * 0.5 + DOWN * 0.35) * k, sh + (LEFT * 0.85 + DOWN * 0.05) * k, color=TEXT, stroke_width=7))
    legs = VGroup(Line(hip, hip + (RIGHT * 0.6 + DOWN * 0.45) * k, color=TEXT, stroke_width=7),
                  Line(hip + (RIGHT * 0.6 + DOWN * 0.45) * k, hip + (RIGHT * 0.5 + DOWN * 1.1) * k, color=TEXT, stroke_width=7),
                  Line(hip, hip + (LEFT * 0.4 + DOWN * 0.6) * k, color=TEXT, stroke_width=7),
                  Line(hip + (LEFT * 0.4 + DOWN * 0.6) * k, hip + (LEFT * 1.05 + DOWN * 0.5) * k, color=TEXT, stroke_width=7))
    speed = VGroup(*[Line(c + (LEFT * 1.0 + UP * dy) * k, c + (LEFT * 1.6 + UP * dy) * k, color=GREY, stroke_width=4)
                     for dy in (0.9, 0.4, -0.1)])
    return VGroup(head, body, arms, legs, speed)


def snowflake(c, R=1.5):
    g = VGroup()
    for a in np.arange(6) * PI / 3:
        u = np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(c, c + u * R, color=TEXT, stroke_width=6))
        for f in (0.5, 0.78):
            base = c + u * R * f
            for sgn in (1, -1):
                v = np.array([np.cos(a + sgn * PI / 4), np.sin(a + sgn * PI / 4), 0])
                g.add(Line(base, base + v * R * 0.25, color=TEXT, stroke_width=5))
    return g


class S15Trigger(SpokenScene):
    def construct(self):
        t = Tet(1.4, BLUE, DOWN * 0.3, o2_at=(0, 1, 2, 3))
        lab = T("T shape", 40, BLUE, weight=BOLD).next_to(t, LEFT, buff=0.7)
        lose = T("the trigger: losing oxygen", 44, GOLD).move_to(UP * 3.35)
        self.add(lose)
        self.play(FadeIn(t), FadeIn(lab), run_time=0.4)
        self.at("losing oxygen")
        outs = [np.array(v) for v in ([-1.6, 0.6, 0], [1.6, 0.6, 0], [-1.6, -0.6, 0], [1.6, -0.6, 0])]
        # the O2 badges leave the tetramer at full brightness, drifting outward
        self.play(*[o.animate.shift(d) for o, d in zip(t.lig, outs)], run_time=1.2, rate_func=smooth)
        self.at("exertion")
        rc = LEFT * 3.5 + UP * 0.45
        rn = runner(rc, 1.45)
        r_lab = T("exertion", 40, YELLOW).move_to(rc + DOWN * 2.45)
        use = T("more O₂ used", 36, YELLOW).next_to(r_lab, DOWN, buff=0.2)
        t_small = VGroup(t.H, lab)
        self.play(FadeOut(t.lig), t.H.animate.scale(0.5).move_to(UP * 0.7),
                  lab.animate.move_to(UP * 0.7 + DOWN * 1.65), FadeIn(rn, shift=RIGHT * 0.4), FadeIn(r_lab), run_time=0.7)
        self.at("oxygen use")
        self.play(FadeIn(use, shift=UP * 0.1), rn.animate.shift(RIGHT * 0.25), run_time=0.6)
        self.at("cold slows")
        sc_ = RIGHT * 3.6 + UP * 0.45
        fl = snowflake(sc_, 1.6)
        c_lab = T("cold", 40, TEXT).move_to(sc_ + DOWN * 2.45)
        slow = T("slower flow, small vessels", 36, TEXT).next_to(c_lab, DOWN, buff=0.2)
        self.play(FadeIn(fl, scale=0.5), FadeIn(c_lab), run_time=0.6)
        self.at("small vessels")
        self.play(FadeIn(slow, shift=UP * 0.1), Rotate(fl, PI / 6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- s16: more time in T; dehydration
def drop_icon(c, h=3.0):
    ts = np.linspace(0, TAU, 120, endpoint=False)
    pts = [[0.62 * h / 2 * np.sin(t) * np.sin(t / 2) ** 1.1, h / 2 * np.cos(t), 0] for t in ts]
    d = Polygon(*pts, fill_color=TEAL, fill_opacity=0.35, stroke_color=TEAL, stroke_width=4)
    return d.move_to(c)


class S16Trigger2(SpokenScene):
    def construct(self):
        c = UP * 0.5
        cap = T("the mix of shapes", 36, TEXT).move_to(c + UP * 1.25)
        pb = popbar(0.5, c, 11.6, 1.5)
        pl = poplabels(c, 11.6, 1.5, 36)
        self.play(FadeIn(cap), FadeIn(pb), FadeIn(pl), run_time=0.5)
        self.at("leave more hemoglobin")
        self.play(Transform(pb, popbar(0.12, c, 11.6, 1.5)), run_time=1.0, rate_func=smooth)
        held = T("more hemoglobin in T, for longer", 38, BLUE).move_to(c + DOWN * 2.0)
        self.play(FadeIn(held, shift=UP * 0.1), run_time=0.5)
        self.at("dehydration")
        top = UP * 3.0
        bar_grp = VGroup(pb, pl)
        cell = RoundedRectangle(corner_radius=0.5, width=7.6, height=3.6, stroke_color=CELL, stroke_width=5,
                                fill_color=CELL, fill_opacity=0.12).move_to(RIGHT * 2.1 + DOWN * 1.05)
        cell.set_stroke(opacity=1)
        drop = drop_icon(LEFT * 4.6 + DOWN * 1.05, 3.6)
        dl = T("water", 34, TEAL).next_to(drop, DOWN, buff=0.2)
        ms = 0.95
        mols = VGroup(*[mini(ms, BLUE) for _ in range(8)])
        loose = [[2.1 + (i % 4 - 1.5) * 1.75 + (0.15 if i // 4 else -0.15), -0.25 - 1.55 * (i // 4) + (0.12 if i % 2 else -0.1), 0]
                 for i in range(8)]
        for m, p in zip(mols, loose):
            m.move_to(p)
        bar_top = VGroup(popbar(0.12, top, 10.4, 0.75), poplabels(top, 10.4, 0.75, 32))
        self.play(FadeOut(cap), FadeOut(held), run_time=0.3)
        self.play(Transform(bar_grp, bar_top),
                  FadeIn(cell), FadeIn(mols), FadeIn(drop), FadeIn(dl), run_time=0.8)
        self.at("concentrates sickle")
        w = pitch(ms)
        tight = [[2.1 + (i % 4 - 1.5) * w, -0.45 - 1.25 * (i // 4), 0] for i in range(8)]
        self.play(cell.animate.stretch_to_fit_width(5.6).stretch_to_fit_height(3.0).move_to(RIGHT * 2.1 + DOWN * 1.07),
                  *[m.animate.move_to(p) for m, p in zip(mols, tight)], run_time=1.4, rate_func=smooth)
        self.at("fibers form")
        rows = VGroup(*[RoundedRectangle(corner_radius=0.2, width=4 * w + 0.25, height=w + 0.2, stroke_color=GOLD,
                                         stroke_width=5).move_to([2.1, -0.45 - 1.25 * r, 0]) for r in range(2)])
        fl = T("fibers form faster", 38, GOLD).move_to(RIGHT * 2.1 + DOWN * 3.35)
        self.play(Create(rows), FadeIn(fl, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- s17: carriers
def chromosome(c, color, h=4.2):
    rod = RoundedRectangle(corner_radius=0.4, width=0.85, height=h, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.22).move_to(c)
    band = Rectangle(width=0.85, height=0.45, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to(c + UP * 0.6)
    return VGroup(rod, band)


class S17Carriers(SpokenScene):
    def construct(self):
        ca = chromosome(LEFT * 5.0 + DOWN * 0.15, TEXT)
        cb = chromosome(LEFT * 3.1 + DOWN * 0.15, GOLD)
        la = T("normal", 34, TEXT).next_to(ca, UP, buff=0.3)
        lb = T("sickle", 34, GOLD).next_to(cb, UP, buff=0.3)
        gl = VGroup(T("two copies", 32, GREY), T("of the β gene", 32, GREY)).arrange(DOWN, buff=0.08)
        gl.next_to(VGroup(ca, cb), DOWN, buff=0.35)
        self.play(FadeIn(ca), FadeIn(cb), FadeIn(la), FadeIn(lb), FadeIn(gl), run_time=0.8)
        self.at("usually healthy")
        chk = VGroup(Circle(radius=0.55, stroke_color=GREEN, stroke_width=5),
                     VMobject(stroke_color=GREEN, stroke_width=7).set_points_as_corners(
                         [[-0.25, 0.0, 0], [-0.05, -0.22, 0], [0.28, 0.22, 0]]))
        h = T("usually healthy", 44, GREEN, weight=BOLD)
        hg = VGroup(chk, h).arrange(RIGHT, buff=0.4).move_to(RIGHT * 2.2 + UP * 1.75)
        self.play(FadeIn(hg, shift=LEFT * 0.2), run_time=0.7)
        self.at("partly protected")
        pp = VGroup(T("partly protected against", 38, GREEN), T("severe falciparum malaria", 38, GREEN)) \
            .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        sh = shield(ORIGIN, GREEN, 1.05)
        pg = VGroup(sh, pp).arrange(RIGHT, buff=0.45).move_to(RIGHT * 2.25 + DOWN * 1.0)
        self.play(FadeIn(sh, scale=0.6), FadeIn(pp, shift=LEFT * 0.2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- s18: gene editing
def toggle(c, on=False):
    slot = RoundedRectangle(corner_radius=0.35, width=1.9, height=0.7, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.15).move_to(c)
    knob = Circle(radius=0.27, stroke_width=0, fill_color=PURPLE if on else GREY, fill_opacity=1)
    knob.move_to(c + (RIGHT if on else LEFT) * 0.58)
    return VGroup(slot, knob)


class S18Therapy(SpokenScene):
    def construct(self):
        y = 0.3
        enh = chip("enhancer of BCL11A", GREY, 34).move_to(LEFT * 4.25 + UP * y)
        sw = toggle(RIGHT * 0.5 + UP * y)
        off = T("OFF", 30, GREY).next_to(sw, UP, buff=0.2)
        sw_l = VGroup(T("fetal hemoglobin", 30, TEXT), T("switch", 30, TEXT)).arrange(DOWN, buff=0.06).next_to(sw, DOWN, buff=0.3)
        gam = chip("γ-globin gene", PURPLE, 36).move_to(RIGHT * 4.4 + UP * y)
        gam[0].set_stroke(opacity=0.45).set_fill(opacity=0.05)
        gam[1].set_opacity(0.75)
        w1 = Line(enh.get_right(), sw.get_left(), color=GREY, stroke_width=6)
        w2 = Line(sw.get_right(), gam.get_left(), color=GREY, stroke_width=6)
        self.add(enh, w1, sw, off, sw_l, w2, gam)
        self.at("gene editing")
        cut = w1.get_center()
        scs = scissors(ORIGIN, 1.5, 0.7).rotate(-PI / 2)
        scs.shift(cut + UP * 2.6 - scs[0].get_start())
        sc_l = T("gene editing", 36, TEXT).move_to(LEFT * 4.25 + UP * 2.4)
        self.play(FadeIn(scs, shift=DOWN * 0.2), FadeIn(sc_l), run_time=0.4)
        self.play(scs.animate.shift(DOWN * 1.9), run_time=0.4)
        l_a = Line(w1.get_start(), cut + LEFT * 0.3, color=GREY, stroke_width=6)
        l_b = Line(cut + RIGHT * 0.3, w1.get_end(), color=GREY, stroke_width=6)
        self.play(ReplacementTransform(w1, VGroup(l_a, l_b)), scs.animate.scale(0.9), run_time=0.3)
        self.play(l_b.animate.set_opacity(0.0), enh.animate.set_opacity(0.4), l_a.animate.set_opacity(0.4), run_time=0.3)
        self.at("switch fetal")
        sw_on = toggle(sw[0].get_center(), on=True)
        on_t = T("ON", 30, PURPLE, weight=BOLD).move_to(off)
        self.play(FadeOut(scs), FadeOut(sc_l), Transform(sw, sw_on), Transform(off, on_t),
                  w2.animate.set_stroke(PURPLE, 7), gam[0].animate.set_stroke(opacity=1.0).set_fill(PURPLE, 0.3),
                  gam[1].animate.set_opacity(1.0), run_time=0.6)
        self.at("back on")
        on = T("fetal hemoglobin: ON", 44, PURPLE, weight=BOLD).move_to(DOWN * 2.7)
        self.play(FadeIn(on, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- s19: fetal hemoglobin dilutes
class S19Hbf(SpokenScene):
    def construct(self):
        sc = 1.5
        w = pitch(sc)
        y = 0.6
        xs = [(i - 1.5) * w - 1.6 for i in range(4)]
        chain = VGroup(*[mini(sc).move_to([x, y, 0]) for x in xs])
        rod = RoundedRectangle(corner_radius=0.3, width=chain.width + 0.4, height=chain.height + 0.4,
                               stroke_color=GOLD, stroke_width=6).move_to(chain)
        lbl = T("sickle hemoglobin fiber", 36, GOLD).next_to(rod, UP, buff=0.3)
        f1 = mini(sc, PURPLE, patch=False, pocket=False).move_to(RIGHT * 5.1 + UP * y)
        f_l = T("fetal hemoglobin", 34, PURPLE).next_to(f1, DOWN, buff=0.4)
        self.add(chain, rod, lbl)
        self.play(FadeIn(f1, shift=LEFT * 0.4), FadeIn(f_l), run_time=0.6)
        self.at("does not join")
        edge = rod.get_right()[0] + w / 2 + 0.05
        self.play(f1.animate.move_to([edge, y, 0]), f_l.animate.shift(LEFT * (5.1 - edge)), run_time=0.5, rate_func=rush_into)
        self.play(f1.animate.move_to([4.9, y, 0]), f_l.animate.shift(RIGHT * (4.9 - edge)), run_time=0.6, rate_func=rush_from)
        nj = T("no sticky patch: it does not join", 34, PURPLE).move_to(DOWN * 2.0)
        self.play(FadeIn(nj), run_time=0.4)
        self.at("dilutes")
        s2 = 1.15
        grid = [(-4.4 + 2.2 * c, 2.4 - 1.65 * r) for r in range(2) for c in range(5)]
        sick_idx = [0, 6, 2, 8]            # checkerboard, in the chain's left-to-right order
        fet_idx = [4, 1, 3, 5, 7, 9]
        # beat 1: the fibre breaks into separate tetramers (the outline splits into four boxes that pull apart)
        pieces = VGroup(*[RoundedRectangle(corner_radius=0.2, width=mini_w(sc) + 0.3, height=mini_w(sc) + 0.3,
                                           stroke_color=GOLD, stroke_width=5).move_to(ch) for ch in chain])
        self.play(FadeOut(nj), FadeOut(lbl), FadeOut(f_l), ReplacementTransform(rod, pieces), run_time=0.3)
        gaps = [-0.9, -0.3, 0.3, 0.9]
        self.play(*[ch.animate.shift(RIGHT * g) for ch, g in zip(chain, gaps)],
                  *[p.animate.shift(RIGHT * g) for p, g in zip(pieces, gaps)], run_time=0.5, rate_func=smooth)
        # beat 2: they settle into a loose grid, with fetal molecules between them
        anims = []
        for k, ch in zip(sick_idx, chain):
            anims.append(ch.animate.scale(s2 / sc).move_to([grid[k][0], grid[k][1], 0]))
        anims.append(f1.animate.scale(s2 / sc).move_to([grid[fet_idx[0]][0], grid[fet_idx[0]][1], 0]))
        newf = [mini(s2, PURPLE, patch=False, pocket=False).move_to([grid[k][0], grid[k][1], 0]) for k in fet_idx[1:]]
        self.play(FadeOut(pieces), *anims, run_time=0.7, rate_func=smooth)
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in newf], lag_ratio=0.15), run_time=0.4)
        self.at("around it")
        dl = T("fetal hemoglobin dilutes the sickle hemoglobin", 34, PURPLE).move_to(DOWN * 0.55)
        self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.5)
        self.at("far less")
        cell = red_disc(1.35, LEFT * 2.2 + DOWN * 2.4)
        cl = T("cells stay round", 44, TEXT, weight=BOLD).next_to(cell, RIGHT, buff=0.6)
        self.play(FadeIn(cell, scale=0.6), FadeIn(cl), run_time=0.6)
        self.wait(0.8)
        self.finish()


# ---------------------------------------------------------------- s20: recap
def shape_box(letter, color, c):
    b = RoundedRectangle(corner_radius=0.25, width=4.4, height=2.9, stroke_color=color, stroke_width=5,
                         fill_color=color, fill_opacity=0.18).move_to(c)
    l = T(letter, 96, color, weight=BOLD).move_to(b.get_center() + UP * 0.5)
    return VGroup(b, l)


class S20Recap(SpokenScene):
    def construct(self):
        tb = shape_box("T", BLUE, LEFT * 3.5 + UP * 1.85)
        rb = shape_box("R", GREEN, RIGHT * 3.5 + UP * 1.85)
        mix = DoubleArrow(tb.get_right() + RIGHT * 0.2, rb.get_left() + LEFT * 0.2, color=GREY, buff=0, stroke_width=6)
        self.play(FadeIn(tb), FadeIn(rb), GrowArrow(mix), run_time=0.7)
        self.at("in this story")
        specs = [("O₂", YELLOW, "R"), ("BPG", TEAL, "T"), ("CO", RED, "R"),
                 ("acid", TEXT, "T"), ("fetal Hb", PURPLE, "R"), ("CO₂", TEXT, "T")]
        ti = ri = 0
        anims = []
        for n, c, side in specs:
            ch = chip(n, c, 40, fill_opacity=0.3 if c == TEXT else 0.16)
            if c == TEXT:
                ch[0].set_stroke(width=4)
            if side == "T":
                dest = LEFT * 3.5 + DOWN * (0.35 + 1.1 * ti); ti += 1
            else:
                dest = RIGHT * 3.5 + DOWN * (0.35 + 1.1 * ri); ri += 1
            ch.move_to(dest)
            anims.append(FadeIn(ch, shift=UP * 0.3))
        self.play(LaggedStart(*anims, lag_ratio=0.15), run_time=1.4)
        ft = T("favor T", 34, BLUE).move_to(LEFT * 3.5 + DOWN * 3.5)
        fr = T("favor R", 34, GREEN).move_to(RIGHT * 3.5 + DOWN * 3.5)
        self.play(FadeIn(ft), FadeIn(fr), run_time=0.4)
        self.at("a mix of")
        mx = T("a mix", 34, GREY).next_to(mix, UP, buff=0.15)
        self.play(FadeIn(mx), run_time=0.3)
        self.at("weak shape")
        wk = T("weak shape", 36, BLUE).move_to(tb[0].get_center() + DOWN * 0.7)
        self.play(FadeIn(wk), run_time=0.3)
        self.at("tight shape")
        tg = T("tight shape", 36, GREEN).move_to(rb[0].get_center() + DOWN * 0.7)
        self.play(FadeIn(tg), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------- s21: the take-home
class S21Take(SpokenScene):
    def construct(self):
        lc, rc = LEFT * 3.45, RIGHT * 3.45
        div = Line(UP * 3.5, DOWN * 3.5, color=GREY, stroke_width=2)
        hd = T("how blood delivers", 40, GREEN, weight=BOLD).move_to(lc + UP * 3.15)
        hd2 = T("how it fails", 40, RED, weight=BOLD).move_to(rc + UP * 3.15).set_opacity(0.3)
        c1 = lc + DOWN * 0.2
        pb = popbar(0.2, c1, 5.8, 1.1)
        pl = poplabels(c1, 5.8, 1.1, 32)
        ox = o2(0.45).move_to(c1 + UP * 1.55 + LEFT * 1.4)
        ox_l = T("oxygen", 32, YELLOW).next_to(ox, LEFT, buff=0.25)
        self.add(div, hd, hd2, pb, pl, ox, ox_l)
        self.at("that mix")
        self.play(Transform(pb, popbar(0.8, c1, 5.8, 1.1)), VGroup(ox, ox_l).animate.shift(RIGHT * 2.2), run_time=0.9)
        self.play(Transform(pb, popbar(0.2, c1, 5.8, 1.1)), VGroup(ox, ox_l).animate.shift(LEFT * 2.2), run_time=0.9)
        dv = T("shifting the mix", 36, GREEN).move_to(lc + DOWN * 2.2)
        self.play(FadeIn(dv), run_time=0.3)
        self.at("locking the mix")
        c2 = rc + UP * 0.95
        pb2 = popbar(0.85, c2, 5.4, 1.0)
        lk = lock_icon(c2 + UP * 1.4, RED, 0.8)
        l2 = T("locking the mix (CO)", 34, RED).next_to(pb2, DOWN, buff=0.3)
        self.play(hd2.animate.set_opacity(1), FadeIn(pb2), FadeIn(lk, scale=0.5), FadeIn(l2), run_time=0.5)
        self.at("making tea sticky")
        t = Tet(0.8, BLUE, rc + DOWN * 1.85 + LEFT * 1.55, labels=SICKLE_LABELS)
        patch = Circle(radius=0.22, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(t.val_pt())
        sl = VGroup(T("T made sticky", 34, GOLD), T("(sickle cell)", 30, GOLD)).arrange(DOWN, buff=0.08)
        sl.next_to(t, RIGHT, buff=0.5)
        self.play(FadeIn(t), FadeIn(patch, scale=0.3), FadeIn(sl), run_time=0.6)
        self.finish()
