"""Marked in the Yolk Sac  (chapter 2 of "Where Glia Come From", Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole series; taken from scenes.old.py, with two additions marked NEW)
  BLUE   = neural tube, brain, radial glia (the CNS stem cell lineage)
  GREEN  = astrocytes, GFAP "on"
  TEAL   = oligodendrocyte lineage (precursors)
  ORANGE = yolk sac and microglia / yolk-sac macrophages
  PURPLE = neural crest, Schwann cells, satellite glia
  TEXT   = neurons, body outlines and the emphasised word "most" (white)
  PINK   = named proteins: relay proteins (JAK, STAT3), Cre, the CSF1R receptor
  YELLOW = a signal or a mark that is passed on: here the Cre mark / reporter glow, tamoxifen, marked cells
  RED    = the question, a block, a loss (STOP block, no heartbeat, missing cells)
  GREY   = outlines, labels, de-emphasized, unmarked cells
  SITE   = NEW  loxP sites (periwinkle)
  BLOOD  = NEW  blood-making cells, monocytes, blood vessels (magenta-rose)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E58FB4"
SITE = "#9FA8FF"
BLOOD = "#D9508F"


# Finish on the audio clock; otherwise 25 scene tails add ten seconds of drift.
def audio_finish(self):
    remaining = self.narration_s - self.elapsed()
    if remaining > 0:
        self.wait(remaining)

class SpokenScene(SpokenScene):
    finish = audio_finish

class NarratedScene(NarratedScene):
    finish = audio_finish

class TitleCard(TitleCard):
    finish = audio_finish

class EndCard(EndCard):
    finish = audio_finish

# ---------------------------------------------------------------- helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def P(x, y):
    return np.array([x, y, 0.0])


def lab(text, x, y, size=26, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def micro(pos=ORIGIN, s=1.0, color=ORANGE, angles=None):
    """Ramified microglia: body plus branched processes; total radius is about 0.7 * s."""
    pos = np.array(pos, dtype=float)
    lens = [1.0, 0.85, 1.1, 0.9, 1.05, 0.8]
    sw = max(2.5, 3.4 * s ** 0.6)
    parts = []
    angs = list(range(15, 360, 60)) if angles is None else angles
    for k, a0 in enumerate(angs):
        L = 0.4 * lens[k % 6] * s
        a = np.deg2rad(a0)
        d = np.array([np.cos(a), np.sin(a), 0])
        n = np.array([-np.sin(a), np.cos(a), 0])
        p1 = d * L + n * 0.05 * s * (1 if k % 2 else -1)
        arm = VMobject().set_points_as_corners([ORIGIN, p1 * 0.5 + n * 0.04 * s, p1]).set_stroke(color, sw).set_fill(opacity=0)
        parts.append(arm)
        for sgn in (-1, 1):
            ang = a + sgn * np.deg2rad(38)
            e = np.array([np.cos(ang), np.sin(ang), 0])
            parts.append(Line(p1, p1 + e * 0.3 * s * lens[k % 6], color=color, stroke_width=sw * 0.65))
        parts.append(Line(p1, p1 + d * 0.28 * s, color=color, stroke_width=sw * 0.65))
    body = Circle(radius=0.17 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    return VGroup(*parts, body).shift(pos)


def cell(pos, r=0.3, ident=GREY, marked=False, fill=0.3):
    """A simple round cell. Marked cells are filled yellow with a glow ring."""
    pos = np.array(pos, dtype=float)
    if marked:
        glow = Circle(radius=r * 1.45, stroke_width=0, fill_color=YELLOW, fill_opacity=0.22)
        body = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
        return VGroup(glow, body).move_to(pos)
    glow = Circle(radius=r * 1.45, stroke_width=0, fill_color=YELLOW, fill_opacity=0.0)
    body = Circle(radius=r, stroke_color=ident, stroke_width=3, fill_color=ident, fill_opacity=fill)
    return VGroup(glow, body).move_to(pos)


def mark_it(c):
    """Animation list that turns a cell() yellow-marked."""
    return [c[0].animate.set_fill(YELLOW, 0.22), c[1].animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW)]


def drop(pos, s=1.0):
    body = Circle(radius=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(ORIGIN)
    tip = Triangle(stroke_width=0, fill_color=YELLOW, fill_opacity=1).scale(0.2).move_to([0, 0.27, 0])
    return VGroup(body, tip).scale(s).move_to(pos)


def mouse(pos, s=1.0):
    body = Ellipse(width=2.8, height=1.6, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
    head = Ellipse(width=1.3, height=1.1, stroke_color=TEXT, stroke_width=3, fill_color=GREY,
                   fill_opacity=0.25).move_to([1.6, 0.15, 0])
    ear = Circle(radius=0.26, stroke_color=TEXT, stroke_width=3, fill_color=PINK, fill_opacity=0.35).move_to([1.5, 0.92, 0])
    ear.set_z_index(-1)
    eye = Dot([1.85, 0.3, 0], radius=0.07, color=TEXT)
    nose = Dot([2.25, 0.15, 0], radius=0.09, color=PINK)
    tail = ArcBetweenPoints([-1.4, -0.1, 0], [-2.9, 0.7, 0], angle=PI / 2.2, color=TEXT, stroke_width=3)
    feet = [Ellipse(width=0.5, height=0.28, stroke_color=TEXT, stroke_width=2, fill_color=GREY,
                    fill_opacity=0.3).move_to([x, -0.85, 0]) for x in (-0.8, 0.8)]
    return VGroup(tail, body, head, ear, eye, nose, *feet).scale(s).move_to(pos)


# ---------------------------------------------------------------- the DNA cassette (scenes 3, 4)
SY = -0.3                      # strand height
T1X, T2X = -4.5, -0.5          # loxP sites (flat layout)
TRI_S = 1.12                   # triangle scale; horizontal extent 1.68
TRI_HALF = 0.84
STOP_X, STOP_W = -2.5, 1.9
REP_X, REP_W = 3.3, 4.2
BLK_H = 2.0
SHIFT = -2.27                  # how far everything right of site 2 moves when the loop closes
T2L = T2X + SHIFT              # site 2 once the sites meet
XM = (T1X + T2L) / 2           # junction


def tri(x):
    return Triangle(stroke_color=SITE, stroke_width=3, fill_color=SITE, fill_opacity=0.75).scale(TRI_S).rotate(-PI / 2) \
        .move_to([x, SY, 0])


def block(w, h, color, fill, pos, z=2):
    """a rectangle with an opaque dark underlay so the DNA line does not run through its text"""
    under = Rectangle(width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pos)
    over = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill).move_to(pos)
    g = VGroup(under, over)
    g.set_z_index(z)
    return g


def cre_chip(pos, s=1.0):
    body = Ellipse(width=2.4, height=1.15, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.35)
    return VGroup(body, T("Cre", 44, PINK).move_to(body)).scale(s).move_to(pos)


def cassette():
    """The flat s03 layout."""
    d = {}
    d["strandA"] = Line([-6.6, SY, 0], [T1X, SY, 0], color=GREY, stroke_width=10)
    d["strandB"] = Line([T1X, SY, 0], [T2X, SY, 0], color=GREY, stroke_width=10)
    d["strandC"] = Line([T2X, SY, 0], [6.4, SY, 0], color=GREY, stroke_width=10)
    d["stop"] = block(STOP_W, BLK_H, RED, 0.3, [STOP_X, SY, 0])
    d["stop_t"] = T("STOP", 38, RED).move_to([STOP_X, SY, 0]).set_z_index(3)
    d["rep"] = block(REP_W, BLK_H, GREY, 0.12, [REP_X, SY, 0])
    d["rep_t"] = T("reporter gene", 36, GREY).move_to([REP_X, SY, 0]).set_z_index(3)
    d["tri1"] = tri(T1X).set_z_index(2)
    d["tri2"] = tri(T2X).set_z_index(2)
    d["lox1"] = lab("loxP", T1X, SY - 1.45, 30, SITE)
    d["lox2"] = lab("loxP", T2X, SY - 1.45, 30, SITE)
    d["dna"] = lab("DNA", -6.0, SY + 0.7, 28, GREY)
    return d


def loop_curve():
    p0 = P(T1X + 0.3, SY + 0.6)
    p3 = P(T2L - 0.3, SY + 0.6)
    return CubicBezier(p0, p0 + P(-0.8, 2.2), p3 + P(0.8, 2.2), p3).set_stroke(GREY, 10)


def loop_state():
    """The looped layout at the end of s03: the sites sit side by side, the STOP rides the loop."""
    d = cassette()
    d["strandB"] = loop_curve()
    d["stop"] = block(1.5, 0.85, RED, 0.3, [XM, SY + 2.0, 0])
    d["stop_t"] = T("STOP", 30, RED).move_to([XM, SY + 2.0, 0]).set_z_index(3)
    for k in ("tri2", "lox2", "strandC", "rep", "rep_t"):
        d[k].shift(RIGHT * SHIFT)
    return d


# ---------------------------------------------------------------- the prediction chart (scenes 9-14)
BASE, K, CW = -1.8, 0.125, 1.6
PX = [-4.0, -1.9, 0.2]
PRED = [30 * f + 2 * (1 - f) for f in (1.0, 0.5, 0.0)]
PLAB = ["all yolk\nsac", "half and\nhalf", "all\nblood"]
PFRAC = [1.0, 0.5, 0.0]
AXX = -5.6
TOP = BASE + 40 * K


def axis_group():
    parts = [Line([AXX, BASE, 0], [AXX, TOP, 0], color=GREY, stroke_width=2)]
    for v in (0, 10, 20, 30, 40):
        y = BASE + v * K
        parts.append(Line([AXX - 0.1, y, 0], [AXX + 0.1, y, 0], color=GREY, stroke_width=2))
        parts.append(T(f"{v}%", 26, GREY).move_to([AXX - 0.75, y, 0]))
    parts.append(T("marked", 26, YELLOW).move_to([-5.9, TOP + 0.42, 0]))
    return VGroup(*parts)


def outline_col(x):
    return Rectangle(width=CW, height=40 * K, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(
        [x, BASE + 20 * K, 0])


def fill_col(x, pct, op=0.4, solid=False):
    h = max(pct * K, 0.04)
    r = Rectangle(width=CW, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9 if solid else op)
    return r.move_to([x, BASE + h / 2, 0])


def mix_icon(x, frac):
    w, h = 1.0, 0.42
    y = -3.25
    parts = []
    if frac > 0:
        a = Rectangle(width=w * frac, height=h, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9)
        a.move_to([x - w / 2 + w * frac / 2, y, 0])
        parts.append(a)
    if frac < 1:
        b = Rectangle(width=w * (1 - frac), height=h, stroke_width=0, fill_color=BLOOD, fill_opacity=0.9)
        b.move_to([x + w / 2 - w * (1 - frac) / 2, y, 0])
        parts.append(b)
    parts.append(Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([x, y, 0]))
    return VGroup(*parts)


def pred_base():
    """empty prediction columns with labels and mix icons -> list of VGroups (one per column)"""
    cols = []
    for x, lb, f in zip(PX, PLAB, PFRAC):
        cols.append(VGroup(outline_col(x), T(lb, 26, TEXT, line_spacing=0.8).move_to([x, -2.5, 0]), mix_icon(x, f)))
    return cols


def val_lab(x, p):
    return T(f"{p:g}%", 30, YELLOW).move_to([x, BASE + p * K + 0.35, 0])


RX = 2.5   # left edge of the right-hand text panel


def left_at(mob, x, y):
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def right_q():
    return left_at(T("What share of adult\nmicroglia should be\nmarked?", 30, TEXT), RX, 2.2)


def right_src():
    g = VGroup(T("yolk sac: 30% marked", 26, ORANGE), T("blood: 2% marked", 26, BLOOD),
               T("both assumed for\nthis exercise", 26, TEXT)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    return left_at(g, RX, -0.1)


def right_pp():
    return left_at(T("pause and predict", 32, YELLOW), RX, -2.5)


def right_note():
    return left_at(T("assumed: all sources\nexpand alike, no\nthird source", 28, TEXT), RX, 2.1)


def right_work():
    g = VGroup(T("average of\n30% and 2%", 28, TEXT), M("= 16%", 34, YELLOW)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    return left_at(g, RX, -2.3)


OBS_X = [2.6, 4.6]


def obs_pair():
    mg = fill_col(OBS_X[0], 100 / 3, solid=True)
    bl = fill_col(OBS_X[1], 2, solid=True)
    lmg = T("adult\nmicroglia", 26, TEXT, line_spacing=0.8).move_to([OBS_X[0], -2.5, 0])
    lbl = T("blood\ncells", 26, TEXT, line_spacing=0.8).move_to([OBS_X[1], -2.5, 0])
    vmg = T("about a third", 26, YELLOW).move_to([OBS_X[0], BASE + (100 / 3) * K + 0.4, 0])
    vbl = T("very few", 26, YELLOW).move_to([OBS_X[1], BASE + 2 * K + 0.5, 0])
    return mg, bl, lmg, lbl, vmg, vbl


X13 = -0.9    # the observed bar moves here, beside bar 1


def inset_parts():
    frame = RoundedRectangle(corner_radius=0.2, width=4.8, height=6.7, stroke_color=GREY, stroke_width=2,
                             fill_opacity=0).move_to([3.8, 0.0, 0])
    ttl = T("later pulse", 30, TEXT).move_to([3.8, 2.85, 0])
    base_y = -1.55
    baseline = Line([1.9, base_y, 0], [5.7, base_y, 0], color=GREY, stroke_width=3)
    blood = Rectangle(width=1.2, height=3.0, stroke_color=BLOOD, stroke_width=0, fill_color=YELLOW,
                      fill_opacity=0.9).move_to([2.9, base_y + 1.5, 0])
    mg = Rectangle(width=1.2, height=0.25, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9) \
        .move_to([4.8, base_y + 0.125, 0])
    vb = T("many marked", 26, YELLOW).move_to([2.95, base_y + 3.0 + 0.4, 0])
    vm = T("few marked", 26, YELLOW).move_to([4.8, base_y + 0.7, 0])
    bl = T("blood", 26, BLOOD).move_to([2.9, base_y - 0.45, 0])
    ml = T("microglia", 26, ORANGE).move_to([4.8, base_y - 0.45, 0])
    ill = T("schematic, not to scale", 26, GREY).move_to([3.8, -2.85, 0])
    return dict(frame=frame, ttl=ttl, base=baseline, blood=blood, mg=mg, vb=vb, vm=vm, bl=bl, ml=ml, ill=ill)


def header(text, x, color=TEXT):
    return T(text, 28, color).move_to([x, 3.55, 0])


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "Where Glia Come From"
    TITLE = "Marked in the Yolk Sac"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), FadeIn(title, scale=0.96),
                  GrowFromCenter(rule), run_time=self.beat(0.3))
        self.wait(self.beat(0.35))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


# --------------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        cc = P(2.3, 0.35)
        mg = micro(cc, 4.2)
        halo = Circle(radius=0.17 * 4.2 * 1.9, stroke_width=0, fill_color=ORANGE, fill_opacity=0.12).move_to(cc)
        stain = T("stained cell", 34, ORANGE).move_to([2.3, -3.05, 0])
        self.add(halo, mg, stain)
        self.at("where a cell was born")
        qc = Circle(radius=1.5, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.08).move_to([-4.6, 0.35, 0])
        q = T("?", 140, RED, weight=BOLD).move_to(qc)
        qt = T("where was it born?", 30, RED).move_to([-4.6, -1.95, 0])
        ln = DashedLine([-3.0, 0.35, 0], [-0.6, 0.35, 0], color=RED, stroke_width=5, dash_length=0.2)
        ln.add_tip(tip_length=0.3)
        self.play(FadeIn(qc), FadeIn(q, scale=0.5), FadeIn(qt), run_time=0.6)
        self.play(Create(ln), run_time=0.7)
        self.at("stain shows only")
        sh = T("shape only", 38, TEXT, weight=BOLD).move_to([2.3, -3.05, 0])
        self.play(ReplacementTransform(stain, sh), Indicate(mg, color=ORANGE, scale_factor=1.04), run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------------------------------
GX = [-4.2, -1.4, 1.4, 4.2]


class S02(SpokenScene):
    def construct(self):
        p0 = cell([GX[0], 0, 0], 0.6)
        pl = lab("progenitor", GX[0], -1.15, 30, GREY)
        self.add(p0)
        self.wait(0.4)
        self.at("progenitor")
        self.play(FadeIn(pl, shift=UP * 0.1), run_time=0.4)
        self.at("progenitor")
        mk = lab("Mark a progenitor", GX[0], 1.25, 30, YELLOW)
        self.play(*mark_it(p0), FadeIn(mk, shift=DOWN * 0.1), pl.animate.set_color(YELLOW), run_time=0.6)
        self.play(Indicate(p0[1], color=YELLOW, scale_factor=1.2), run_time=0.5)
        self.at("later in everything")
        tl = arr([-4.2, -3.5, 0], [4.9, -3.5, 0], GREY, 4)
        later = lab("later", -1.0, -3.1, 28, GREY)
        self.play(GrowArrow(tl), FadeIn(later), run_time=0.3)
        g1 = [cell([GX[1], y, 0], 0.5, marked=True) for y in (1.2, -1.2)]
        l1 = [Line([GX[0] + 0.55, 0, 0], [GX[1] - 0.5, y, 0], color=YELLOW, stroke_width=3).set_opacity(0.7) for y in (1.2, -1.2)]
        self.play(*[FadeIn(c, scale=0.5) for c in g1], *[Create(l) for l in l1], run_time=0.4)
        g2 = [cell([GX[2], y, 0], 0.42, marked=True) for y in (2.0, 0.65, -0.65, -2.0)]
        l2 = []
        for i, c in enumerate(g2):
            par = g1[0] if i < 2 else g1[1]
            l2.append(Line([GX[1] + 0.5, par.get_center()[1], 0], [GX[2] - 0.42, c.get_center()[1], 0],
                           color=YELLOW, stroke_width=3).set_opacity(0.7))
        self.play(*[FadeIn(c, scale=0.5) for c in g2], *[Create(l) for l in l2], run_time=0.4)
        ys = np.linspace(2.95, -2.95, 8)
        g3 = [cell([GX[3], y, 0], 0.3, marked=True) for y in ys]
        l3 = []
        for i, c in enumerate(g3):
            par = g2[i // 2]
            l3.append(Line([GX[2] + 0.42, par.get_center()[1], 0], [GX[3] - 0.3, c.get_center()[1], 0],
                           color=YELLOW, stroke_width=3).set_opacity(0.7))
        self.play(*[FadeIn(c, scale=0.5) for c in g3], *[Create(l) for l in l3], run_time=0.5)
        self.at("fate mapping")
        fm = T("fate mapping", 52, YELLOW, font=TITLE_FONT).move_to([-3.4, 3.0, 0])
        self.play(FadeIn(fm, shift=UP * 0.1), run_time=0.6)
        self.finish()


# --------------------------------------------------------------------------------------------------
class S03(SpokenScene):
    def construct(self):
        d = cassette()
        self.add(*[d[k] for k in ("strandA", "strandB", "strandC", "stop", "stop_t", "rep", "rep_t",
                                   "tri1", "tri2", "lox1", "lox2", "dna")])
        self.at("an enzyme called")
        c = cre_chip([-2.5, 2.9, 0])
        self.play(FadeIn(c, shift=UP * 0.4), run_time=0.6)
        self.at("cuts and rejoins")
        d2 = loop_state()
        self.play(
            Transform(d["strandB"], d2["strandB"]),
            ReplacementTransform(d["stop"], d2["stop"]),
            ReplacementTransform(d["stop_t"], d2["stop_t"]),
            d["tri2"].animate.shift(RIGHT * SHIFT), d["lox2"].animate.shift(RIGHT * SHIFT),
            d["strandC"].animate.shift(RIGHT * SHIFT), d["rep"].animate.shift(RIGHT * SHIFT),
            d["rep_t"].animate.shift(RIGHT * SHIFT),
            c.animate.move_to([XM, -2.95, 0]),
            run_time=1.4)
        grips = VGroup(Line([XM,-2.37,0],[XM,-1.61,0],color=PINK,stroke_width=4))
        self.play(Create(grips),run_time=0.3)
        self.at("short sequences called")
        ring = Ellipse(width=4.2, height=2.6, stroke_color=PINK, stroke_width=4, fill_opacity=0).move_to([XM, SY, 0])
        self.play(Create(ring), run_time=0.6)
        self.at("lox")
        self.play(Indicate(d["lox1"], color=SITE, scale_factor=1.25), Indicate(d["lox2"], color=SITE, scale_factor=1.25),
                  Indicate(d["tri1"], color=SITE, scale_factor=1.15), Indicate(d["tri2"], color=SITE, scale_factor=1.15),
                  run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------------
class S04(SpokenScene):
    def construct(self):
        d = loop_state()
        c = cre_chip([XM, -2.95, 0])
        ring = Ellipse(width=4.2, height=2.6, stroke_color=PINK, stroke_width=4, fill_opacity=0).move_to([XM, SY, 0])
        grips = VGroup(Line([XM,-2.37,0],[XM,-1.61,0],color=PINK,stroke_width=4))
        self.add(*[d[k] for k in d], c, ring, grips)
        rm = lab("reporter mouse", -4.9, 3.35, 32, TEXT)
        self.add(rm)
        self.at("removes a stop")
        loop = VGroup(d["strandB"], d["stop"], d["stop_t"])
        self.play(FadeOut(ring), loop.animate.shift(UP * 1.3).set_opacity(0), d["tri2"].animate.set_opacity(0),
                  d["lox2"].animate.set_opacity(0),
                  Transform(d["strandC"], Line([T1X + TRI_HALF, SY, 0], [4.0, SY, 0], color=GREY, stroke_width=10)),
                  run_time=1.0)
        self.play(FadeOut(c), FadeOut(grips), run_time=0.3)
        self.at("the sites")
        one = lab("one loxP site left", T1X + 0.9, SY - 1.45, 30, TEXT)
        self.play(ReplacementTransform(d["lox1"], one), Indicate(d["tri1"], color=SITE, scale_factor=1.25), run_time=0.7)
        self.at("reporter turns on")
        glow = Rectangle(width=REP_W + 0.5, height=BLK_H + 0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.25) \
            .move_to(d["rep"].get_center()).set_z_index(1)
        ron = chip("reporter on", YELLOW, size=30).move_to([3.8, 3.35, 0])
        self.play(FadeOut(rm), FadeIn(ron), d["rep"][1].animate.set_stroke(YELLOW, 6).set_fill(YELLOW, 0.5),
                  d["rep_t"].animate.set_color(TEXT), FadeIn(glow), run_time=0.7)
        self.play(Indicate(d["rep"], color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.at("and every")
        mother = cell([0, -0.2, 0], 0.95, marked=True)
        keep = VGroup(d["strandA"], d["strandC"], d["rep"], d["rep_t"], d["tri1"], d["dna"], glow)
        self.play(FadeOut(keep), one.animate.move_to([-3.6, -3.1, 0]), FadeIn(mother, scale=0.5), run_time=0.3)
        self.wait(0.18)  # hold the single mother before the first division
        self.at("descendant")
        a1 = cell([0, -0.2, 0], 0.85, marked=True)
        a2 = cell([0, -0.2, 0], 0.85, marked=True)
        self.add(a1, a2)
        self.remove(mother)
        self.play(a1.animate.move_to([-1.7, -0.2, 0]), a2.animate.move_to([1.7, -0.2, 0]), run_time=0.35)
        self.at("inherits it")
        b = [cell([x, -0.2, 0], 0.8, marked=True) for x in (-1.7, -1.7, 1.7, 1.7)]
        self.remove(a1, a2)
        self.add(*b)
        self.play(b[0].animate.move_to([-4.2, -0.2, 0]), b[1].animate.move_to([-1.4, -0.2, 0]),
                  b[2].animate.move_to([1.4, -0.2, 0]), b[3].animate.move_to([4.2, -0.2, 0]), run_time=0.45)
        tx = lab("every daughter glows", 0, -2.3, 40, YELLOW)
        self.play(FadeIn(tx, shift=UP * 0.1), run_time=0.2)
        self.finish()


# --------------------------------------------------------------------------------------------------
class S05(SpokenScene):
    def construct(self):
        SYY = 1.2
        strand = Line([-6.4, SYY, 0], [2.0, SYY, 0], color=GREY, stroke_width=10)
        prom = block(3.0, 1.3, GREY, 0.3, [-3.8, SYY, 0])
        prom_t = T("promoter", 34, TEXT).move_to(prom).set_z_index(3)
        AY = -2.85
        ax = arr([-6.4, AY, 0], [6.5, AY, 0], GREY, 5)
        tt = lab("time", 5.9, AY - 0.5, 28, GREY)
        ca = cell([-0.1, -1.45, 0], 0.55)
        cb = cell([1.9, -1.45, 0], 0.55)
        la = lab("gene on", -0.1, -2.35, 26, TEXT)
        lb = lab("gene off", 1.9, -2.35, 26, TEXT)
        self.add(strand,prom,prom_t,ax,tt,ca,cb,la,lb)
        self.at("from a gene")
        creb = block(2.6, 1.3, PINK, 0.35, [0.4, SYY, 0])
        creb_t = T("Cre", 46, PINK).move_to([0.4, SYY, 0]).set_z_index(3)
        ar = arr([-2.2, SYY, 0], [-1.1, SYY, 0], YELLOW, 6, 0.22)
        self.play(GrowArrow(ar), FadeIn(creb), FadeIn(creb_t), run_time=0.6)
        self.at("the progenitor uses")
        gl = lab("a gene the progenitor uses", -3.8, 2.25, 28, GREY)
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.5)
        self.at("in the line")
        mline = chip("microglia line", ORANGE, size=30).move_to([4.6, 2.4, 0])
        self.play(FadeIn(mline, shift=LEFT * 0.2), run_time=0.6)
        self.at("one dose of tamoxifen")
        dr = drop([-1.6, 0.35, 0], 1.5)
        dl = lab("tamoxifen", -3.55, 0.35, 32, YELLOW)
        self.play(FadeIn(dr, scale=0.5), FadeIn(dl), run_time=0.4)
        self.play(dr.animate.move_to([-1.6, AY + 0.55, 0]), dl.animate.move_to([-3.55, AY + 0.55, 0]), run_time=0.7)
        self.at("lets it act")
        win = Rectangle(width=4.4, height=2.6, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                        fill_opacity=0.12).move_to([0.9, -1.55, 0])
        wl = lab("in the microglia line", 0.9, -0.55, 26, ORANGE)
        self.play(FadeIn(win, shift=RIGHT * 0.3), FadeIn(wl), run_time=0.5)
        self.at("about a day")
        dl2 = lab("about one day", 0.9, AY - 0.5, 32, YELLOW)
        self.play(FadeIn(dl2, shift=UP * 0.1), *mark_it(ca), run_time=0.6)
        self.finish()


# --------------------------------------------------------------------------------------------------
class S06(SpokenScene):
    def construct(self):
        m = mouse([2.9, 0.0, 0], 1.3)
        yr = lab("2010", -3.6, 2.6, 80, YELLOW, font=TITLE_FONT)
        self.add(m, yr)
        self.at("florent")
        self.play(FadeIn(lab("Florent Ginhoux", -3.6, 1.2, 36)), run_time=0.25)
        self.at("miriam")
        self.play(FadeIn(lab("Miriam Merad", -3.6, 0.4, 36)), run_time=0.25)
        self.at("and colleagues")
        self.play(FadeIn(lab("and colleagues", -3.6, -0.4, 32)), run_time=0.25)
        self.at("in mice")
        self.play(FadeIn(lab("mouse", 3.2, -1.7, 32)), run_time=0.25)
        self.at("driven by")
        driver = VGroup(chip("Runx1 promoter", ORANGE, 32),
                        T("→", 42, TEXT), chip("CreER", PINK, 34)).arrange(RIGHT, buff=0.4).move_to([0,-2.5,0])
        self.play(FadeIn(driver), run_time=0.4)
        self.play(FadeIn(lab("Runx1-CreER", 0, 3.25, 48, PINK)), run_time=0.3)
        self.finish()


# --------------------------------------------------------------------------------------------------
def yolk_ellipse(c, w=4.8, h=4.2):
    return Ellipse(width=w, height=h, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                   fill_opacity=0.12).move_to(c)


LC, RC = np.array([-3.5, 0.3, 0]), np.array([3.5, 0.3, 0])
LP = [[-1.2, 0.9], [0, 1.1], [1.2, 0.9], [-1.3, -0.1], [0, 0], [1.3, -0.1], [-1.1, -1.1], [0, -1.2], [1.1, -1.1]]
RP = [[-1.4, 0.8], [0.0, 1.1], [1.3, 0.6], [-0.7, -0.1], [0.7, 0.1], [-1.5, -0.9], [0.0, -1.0], [1.4, -0.8], [0.2, -1.7]]


class S07(SpokenScene):
    def construct(self):
        ly = yolk_ellipse(LC)
        ly_l = lab("yolk sac:\nRunx1+ progenitors", LC[0], -2.85, 26, ORANGE, line_spacing=0.8)
        prog = [cell(LC + P(*p), 0.3, ORANGE, fill=0.5) for p in LP]
        self.add(ly, ly_l, *prog)
        self.at("a pulse at")
        dr = drop([LC[0], 3.1, 0], 1.5)
        tam = lab("tamoxifen", LC[0] + 1.75, 3.1, 30, YELLOW)
        self.play(FadeIn(dr, scale=0.5), FadeIn(tam), run_time=0.3)
        self.at("embryonic day")
        e75 = lab("E7.5", -5.9, 3.1, 36, TEXT)
        self.play(FadeIn(e75), dr.animate.move_to([LC[0], 1.35, 0]), run_time=1.0)
        self.at("marked early progenitors")
        self.play(FadeOut(dr), FadeOut(tam), *mark_it(prog[0]), *mark_it(prog[2]), *mark_it(prog[4]), run_time=0.7)
        self.at("later")
        ar = arr([-0.8, 0.3, 0], [0.8, 0.3, 0], GREY, 6, 0.28)
        ry = yolk_ellipse(RC)
        ry_l = lab("yolk-sac macrophages", RC[0], -2.35, 26, ORANGE)
        lt = lab("later", RC[0], 3.1, 36, TEXT)
        mac = [cell(RC + P(*p), 0.3, ORANGE, marked=i in (1, 4, 7), fill=0.55) for i, p in enumerate(RP)]
        self.play(GrowArrow(ar), FadeIn(ry), FadeIn(ry_l), FadeIn(lt),
                  TransformFromCopy(VGroup(*prog), VGroup(*mac)), run_time=0.45)
        self.at("about a third")
        self.play(*[a for i in (1, 4, 7) for a in mark_it(mac[i])], run_time=0.5)
        self.at("carried the mark")
        third = lab("3 of 9 glowing: about a third", RC[0], -3.05, 28, YELLOW)
        self.play(FadeIn(third, shift=UP * 0.1), *[Indicate(mac[i][1], color=YELLOW, scale_factor=1.25) for i in (1, 4, 7)],
                  run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------------------------------
def source_box(c, color, name):
    box = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.0, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.1).move_to(c)
    dots = []
    for i in range(50):
        r, cc = divmod(i, 10)
        x = c[0] - 2.25 + cc * 0.5
        y = c[1] + 1.0 - r * 0.5
        dots.append(Circle(radius=0.15, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.3)
                    .move_to([x, y, 0]))
    nm = T(name, 34, color).move_to([c[0], c[1] + 2.0, 0])
    return box, VGroup(*dots), nm


class S08(SpokenScene):
    def construct(self):
        cy, cb = P(-3.4, 0.5), P(3.4, 0.5)
        b1, d1, n1 = source_box(cy, ORANGE, "yolk sac")
        self.add(b1, d1, n1)
        self.at("labeling 30")
        p1 = T("30%", 80, YELLOW, weight=BOLD).move_to([cy[0], -1.8, 0])
        t1 = lab("assumed for this exercise", cy[0], -2.95, 28, TEXT)
        self.play(LaggedStart(*[d1[i].animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW) for i in range(15)], lag_ratio=0.05),
                  FadeIn(p1, scale=0.6), FadeIn(t1, shift=UP * 0.1), run_time=1.0)
        self.at("very few blood")
        b2, d2, n2 = source_box(cb, BLOOD, "blood-making cells")
        self.play(FadeIn(b2), FadeIn(d2), FadeIn(n2), run_time=0.8)
        self.at("say")
        p2 = T("2%", 80, YELLOW, weight=BOLD).move_to([cb[0], -1.8, 0])
        t2 = lab("assumed for this exercise", cb[0], -2.95, 28, TEXT)
        self.play(d2[0].animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW), FadeIn(p2, scale=0.6), FadeIn(t2, shift=UP * 0.1),
                  run_time=0.7)
        self.play(Indicate(d2[0], color=YELLOW, scale_factor=1.8), run_time=0.5)
        self.finish()


# --------------------------------------------------------------------------------------------------
class S09(SpokenScene):
    def construct(self):
        ax = axis_group()
        q, src = right_q(), right_src()
        self.add(ax, q, src)
        cols = pred_base()
        self.at("try all from")
        self.play(FadeIn(cols[0], shift=UP * 0.2), run_time=0.6)
        self.at("half")
        self.play(FadeIn(cols[1], shift=UP * 0.2), run_time=0.6)
        self.at("all from blood")
        self.play(FadeIn(cols[2], shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(right_pp(), shift=UP * 0.1), run_time=0.4)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        self.add(axis_group(), *pred_base(), right_q(), right_src(), right_pp())
        self.finish()


class S11(SpokenScene):
    def construct(self):
        cols = pred_base()
        q, src, pp = right_q(), right_src(), right_pp()
        self.add(axis_group(), *cols, q, src, pp)
        self.at("carries the mark")
        c_m = cell([RX + 0.5, 2.5, 0], 0.4, marked=True)
        c_u = cell([RX + 0.5, 1.4, 0], 0.4)
        l_m = left_at(T("marked", 32, YELLOW), RX + 1.2, 2.5)
        l_u = left_at(T("not marked", 32, GREY), RX + 1.2, 1.4)
        self.play(FadeOut(q), FadeOut(pp), run_time=0.3)
        self.play(FadeIn(c_m, scale=0.5), FadeIn(l_m), run_time=0.4)
        self.play(FadeIn(c_u, scale=0.5), FadeIn(l_u), run_time=0.4)
        self.at("if all sources")
        note = right_note()
        self.play(FadeOut(VGroup(c_m, c_u, l_m, l_u)), FadeIn(note, shift=DOWN * 0.1), run_time=0.6)
        self.at("marked share")
        mir = left_at(T("marked share\n= the mix", 32, YELLOW), RX, -2.4)
        self.play(FadeIn(mir, shift=UP * 0.1), *[Indicate(c[2], color=YELLOW, scale_factor=1.15) for c in cols], run_time=1.0)
        self.finish()


class S11b(SpokenScene):
    def construct(self):
        cols = pred_base()
        self.add(axis_group(), *cols, right_note(), right_src())
        fills = [fill_col(x, p) for x, p in zip(PX, PRED)]
        vals = [val_lab(x, p) for x, p in zip(PX, PRED)]
        self.at("all from the yolk sac")
        self.play(GrowFromEdge(fills[0], DOWN), FadeIn(vals[0]), run_time=0.6)
        self.play(Indicate(fills[0], color=YELLOW, scale_factor=1.04), run_time=0.6)
        self.at("half and half")
        self.play(GrowFromEdge(fills[1], DOWN), FadeIn(vals[1]), FadeIn(right_work(), shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(fills[1], color=YELLOW, scale_factor=1.04), run_time=0.6)
        self.at("all blood")
        self.play(GrowFromEdge(fills[2], DOWN), FadeIn(vals[2]), run_time=0.5)
        self.play(Indicate(vals[2], color=YELLOW, scale_factor=1.4), run_time=0.6)
        self.finish()


def pred_filled(scene):
    cols = pred_base()
    fills = [fill_col(x, p) for x, p in zip(PX, PRED)]
    vals = [val_lab(x, p) for x, p in zip(PX, PRED)]
    scene.add(axis_group(), *cols, *fills, *vals)
    return cols, fills, vals


def s12_state(scene):
    cols, fills, vals = pred_filled(scene)
    hp = header("predicted (assumed)", -1.9, GREY)
    ho = header("observed", 3.6, TEXT)
    sep = DashedLine([1.2, 3.3, 0], [1.2, -3.4, 0], color=GREY, stroke_width=2, dash_length=0.15)
    mg, bl, lmg, lbl, vmg, vbl = obs_pair()
    scene.add(hp, ho, sep, mg, bl, lmg, lbl, vmg, vbl)
    return cols, fills, vals, hp, ho, sep, (mg, bl, lmg, lbl, vmg, vbl)


class S12(SpokenScene):
    def construct(self):
        cols, fills, vals = pred_filled(self)
        hp = header("predicted (assumed)", -1.9, GREY)
        ho = header("observed", 3.6, TEXT)
        sep = DashedLine([1.2, 3.3, 0], [1.2, -3.4, 0], color=GREY, stroke_width=2, dash_length=0.15)
        mg, bl, lmg, lbl, vmg, vbl = obs_pair()
        self.play(FadeIn(hp), FadeIn(ho), FadeIn(sep), FadeIn(lmg), FadeIn(lbl), run_time=0.5)
        self.at("about a third")
        self.play(GrowFromEdge(mg, DOWN), run_time=0.8)
        self.play(FadeIn(vmg), run_time=0.3)
        self.at("very few blood")
        self.play(GrowFromEdge(bl, DOWN), FadeIn(vbl), run_time=0.6)
        self.play(Indicate(bl, color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.finish()


def s13_end(scene):
    """the final picture of s13; s14 holds it"""
    cols = pred_base()
    f1 = fill_col(PX[0], 30)
    v1 = val_lab(PX[0], 30)
    hp = header("predicted", PX[0], GREY)
    ho = header("observed", X13, TEXT)
    mg, _bl, lmg, _lbl, vmg, _vbl = obs_pair()
    for m in (mg, lmg, vmg):
        m.shift(RIGHT * (X13 - OBS_X[0]))
    eq = T("≈", 60, TEXT).move_to([(PX[0] + X13) / 2, BASE + 15 * K + 0.1, 0])
    ins = inset_parts()
    scene.add(axis_group(), cols[0], f1, v1, hp, ho, mg, lmg, vmg, eq, *ins.values())


class S13(SpokenScene):
    def construct(self):
        cols, fills, vals, hp, ho, sep, obs = s12_state(self)
        mg, bl, lmg, lbl, vmg, vbl = obs
        ring = SurroundingRectangle(fills[0], color=TEXT, buff=0.12, stroke_width=5, corner_radius=0.1)
        tag = T("the top bar", 30, TEXT).move_to([PX[0], 3.55, 0])
        self.play(Create(ring), ReplacementTransform(hp, tag), run_time=0.25)
        self.at("top bar")
        observed_ring = SurroundingRectangle(mg, color=YELLOW, buff=0.12, stroke_width=5)
        self.play(Create(observed_ring), Indicate(ring, color=YELLOW, scale_factor=1.06), run_time=0.3)
        self.play(FadeOut(VGroup(cols[1], cols[2], fills[1], fills[2], vals[1], vals[2], bl, lbl, vbl, sep)), run_time=0.2)
        self.play(mg.animate.shift(RIGHT * (X13 - OBS_X[0])), lmg.animate.shift(RIGHT * (X13 - OBS_X[0])),
                  vmg.animate.shift(RIGHT * (X13 - OBS_X[0])), ho.animate.move_to([X13, 3.55, 0]),
                  FadeOut(observed_ring), run_time=0.35)
        eq = T("≈", 60, TEXT).move_to([(PX[0] + X13) / 2, BASE + 15 * K + 0.1, 0])
        self.play(FadeIn(eq, scale=0.6), ReplacementTransform(tag, header("predicted", PX[0], GREY)), run_time=0.2)
        ins = inset_parts()
        self.at("later pulses")
        self.play(FadeOut(ring), FadeIn(ins["frame"]), FadeIn(ins["ttl"]), FadeIn(ins["base"]), FadeIn(ins["ill"]), run_time=0.25)
        self.at("marked blood")
        self.play(GrowFromEdge(ins["blood"], DOWN), FadeIn(ins["bl"]), FadeIn(ins["vb"]), run_time=0.45)
        self.at("but few")
        self.play(GrowFromEdge(ins["mg"], DOWN), FadeIn(ins["ml"]), FadeIn(ins["vm"]), run_time=0.5)
        self.finish()


class S14Beat(NarratedScene):
    def construct(self):
        s13_end(self)
        self.finish()


# --------------------------------------------------------------------------------------------------
class S15(SpokenScene):
    def construct(self):
        TW, TH, TY = 5.4, 3.2, 0.6
        LCx, RCx = -3.4, 3.4
        h1 = T("read alone", 38, TEXT).move_to([LCx, 3.3, 0])
        trk1 = Rectangle(width=TW, height=TH, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([LCx, TY, 0])
        fl1 = Rectangle(width=TW / 3, height=TH, stroke_width=0, fill_color=YELLOW,
                        fill_opacity=0.85).move_to([LCx - TW / 2 + TW / 6, TY, 0])
        third = lab("a third", LCx, -1.5, 54, YELLOW)
        self.add(h1, trk1)
        self.play(GrowFromEdge(fl1, LEFT), FadeIn(third), run_time=0.7)
        self.at("sounds like a minority")
        mino = lab("minority", LCx, -2.75, 48, RED)
        self.play(FadeIn(mino, shift=UP * 0.1), run_time=0.6)
        self.at("read against")
        h2 = T("read against the source", 38, TEXT).move_to([RCx, 3.3, 0])
        trk2 = Rectangle(width=TW, height=TH, stroke_color=ORANGE, stroke_width=3, fill_opacity=0).move_to([RCx, TY, 0])
        src = lab("source labeled at a third", RCx, 2.6, 28, ORANGE)
        self.play(FadeIn(h2), FadeIn(trk2), FadeIn(src), run_time=0.6)
        self.at("labeled at a third")
        fl2 = Rectangle(width=TW, height=TH, stroke_width=0, fill_color=YELLOW,
                        fill_opacity=0.85).move_to([RCx, TY, 0])
        tt2 = lab("a third of a third-labeled\nsource = all or nearly all", RCx, -1.85, 30, YELLOW, line_spacing=0.85)
        fl2.set_z_index(1)
        trk2.set_z_index(2)
        self.play(GrowFromEdge(fl2, LEFT), FadeIn(tt2), run_time=0.8)
        self.at("it means most")
        most = lab("most", RCx, -2.85, 64, TEXT, weight=BOLD)
        xx = Cross(trk1, stroke_color=RED, stroke_width=7).set_stroke(opacity=0.55)
        self.play(FadeIn(most, scale=0.7), Create(xx), run_time=0.8)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        BX0, BW, BH = -2.6, 8.8, 1.6
        YA, YB = 1.55, -0.65
        ttl = T("the reading depends on the source", 38, TEXT).move_to([0, 3.1, 0])
        ill = lab("illustration,\nnot a measurement", 4.8, 3.1, 28, GREY, line_spacing=0.8)
        trk_a = Rectangle(width=BW, height=BH, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([BX0 + BW / 2, YA, 0])
        trk_b = Rectangle(width=BW, height=BH, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([BX0 + BW / 2, YB, 0])
        self.add(ttl)
        intro = lab("same adult count\ndifferent source labeling", 0, 0, 48, ORANGE)
        self.add(intro)
        self.at("adult count is 30")
        chipc = chip("adult count: 30%", YELLOW, size=38).move_to([-0.8, 3.1, 0])
        ra_l = lab("source labeled\n30%", -4.6, YA, 26, ORANGE, line_spacing=0.8)
        ra = Rectangle(width=BW, height=BH, stroke_width=0, fill_color=ORANGE, fill_opacity=0.5).move_to([BX0 + BW / 2, YA, 0])
        ra_t = lab("all from the yolk sac", BX0 + BW / 2, YA, 34, TEXT)
        self.play(FadeOut(intro), ReplacementTransform(ttl, chipc), FadeIn(ill), FadeIn(trk_a), FadeIn(ra_l), GrowFromEdge(ra, LEFT), FadeIn(ra_t),
                  run_time=0.8)
        self.at("40", lead=0.1)
        rb_l = lab("precursors, if\nlabeled 40%", -4.6, YB, 28, ORANGE, line_spacing=0.8)
        fr = (30 - 2) / (40 - 2)
        ro = Rectangle(width=BW * fr, height=BH, stroke_width=0, fill_color=ORANGE, fill_opacity=0.5) \
            .move_to([BX0 + BW * fr / 2, YB, 0])
        rbl = Rectangle(width=BW * (1 - fr), height=BH, stroke_width=0, fill_color=BLOOD, fill_opacity=0.5) \
            .move_to([BX0 + BW * fr + BW * (1 - fr) / 2, YB, 0])
        self.play(FadeIn(trk_b), FadeIn(rb_l), GrowFromEdge(ro, LEFT), FadeIn(rbl), run_time=0.5)
        self.at("labeled")
        work = M("(30 − 2) ÷ (40 − 2) = 0.74", 40, YELLOW).move_to([0, -2.25, 0])
        bn = lab("2 = blood labeled 2%", 0, -3.15, 34, BLOOD)
        self.play(FadeIn(work, shift=UP * 0.1), FadeIn(bn), run_time=0.5)
        self.at("three quarters")
        ro_t = lab("about three-quarters", BX0 + BW * fr / 2, YB, 32, TEXT)
        rbl_t = lab("blood", BX0 + BW * fr + BW * (1 - fr) / 2, YB, 28, TEXT)
        self.play(FadeIn(ro_t), FadeIn(rbl_t), run_time=0.4)
        self.at("came from the yolk sac")
        self.play(Indicate(ro, color=ORANGE, scale_factor=1.04), run_time=0.9)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        TX0, TW, TY, TH = -5.2, 10.4, 0.0, 3.2
        track = Rectangle(width=TW, height=TH, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([0, TY, 0])
        t0 = lab("0%", TX0, TY - TH / 2 - 0.4, 28, GREY)
        t1 = lab("100%", TX0 + TW, TY - TH / 2 - 0.4, 28, GREY)
        cap = lab("share from the yolk sac", 0, TY - TH / 2 - 0.4, 32, ORANGE)
        self.add(track, t0, t1, cap)
        self.at("the right word")
        # a gradient that starts faint near the middle and brightens toward 100%; no numeric floor is drawn
        n = 40
        x0, x1 = TX0 + TW * 0.5, TX0 + TW
        sw = (x1 - x0) / n
        strips = VGroup(*[Rectangle(width=sw + 0.01, height=TH, stroke_width=0, fill_color=ORANGE,
                                    fill_opacity=0.04 + 0.62 * (i / (n - 1)) ** 1.3)
                          .move_to([x0 + sw * (i + 0.5), TY, 0]) for i in range(n)])
        most = lab("most", 1.9, TY, 90, TEXT, weight=BOLD)
        self.play(FadeIn(strips), FadeIn(most), run_time=0.45)
        self.at("possibly all")
        mk = Line([TX0 + TW, TY - TH / 2, 0], [TX0 + TW, TY + TH / 2, 0], color=YELLOW, stroke_width=10)
        pa = lab("possibly all", 3.9, TY + TH / 2 + 0.55, 44, YELLOW)
        pl = arr([4.7, TY + TH / 2 + 0.3, 0], [TX0 + TW - 0.05, TY + TH / 2 - 0.15, 0], YELLOW, 5, 0.22)
        self.play(Create(mk), FadeIn(pa, shift=DOWN * 0.1), FadeIn(pl), run_time=0.7)
        self.at("cannot give an exact")
        nx = lab("not an exact number", 0, -3.2, 44, TEXT, weight=BOLD)
        self.play(FadeIn(nx, shift=UP * 0.1), run_time=0.7)
        self.finish()


# --------------------------------------------------------------------------------------------------
def embryo_parts(c, sc=1.0):
    """yolk-sac circle, an embryo (brain, body, heart) and a vessel path from the sac, past the heart, to the brain"""
    c = np.array(c, dtype=float)

    def q(x, y):
        return c + P(x * sc, y * sc)

    yolk = Circle(radius=3.3 * sc, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.12).move_to(c)
    head = Circle(radius=0.8 * sc, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to(q(-0.9, 1.35))
    trunk = Ellipse(width=1.3 * sc, height=2.6 * sc, stroke_color=TEXT, stroke_width=3, fill_color=GREY,
                    fill_opacity=0.2).move_to(q(-0.9, -0.55))
    heart = Circle(radius=0.27 * sc, stroke_color=TEXT, stroke_width=3, fill_color=RED, fill_opacity=0.4).move_to(q(-0.9, 0.05))
    # the vessel path, as two cubic segments: sac -> heart, heart -> brain
    s1 = [q(2.0, -1.4), q(1.2, -0.9), q(0.3, 0.1), q(-0.62, 0.05)]
    s2 = [q(-0.62, 0.05), q(-0.1, 0.3), q(0.2, 0.9), q(-0.9, 1.35)]
    v1 = CubicBezier(*s1).set_stroke(BLOOD, 5)
    v2 = CubicBezier(*s2).set_stroke(BLOOD, 5)
    path = VMobject()
    path.start_new_path(s1[0])
    path.add_cubic_bezier_curve_to(s1[1], s1[2], s1[3])
    path.add_cubic_bezier_curve_to(s2[1], s2[2], s2[3])
    pos = [(1.1, 1.5), (2.2, 0.4), (0.9, -0.1), (2.0, -1.0), (0.5, -2.0), (1.5, 2.0), (1.4, -2.0), (-0.3, -2.6), (2.5, -0.5)]
    macs = VGroup(*[cell(q(*p), 0.26 * sc + 0.02, ORANGE, fill=0.7) for p in pos])
    return dict(yolk=yolk, head=head, trunk=trunk, heart=heart, v1=v1, v2=v2, path=path, macs=macs)


EC = np.array([0.6, -0.2, 0.0])


def leader(a, b, color=GREY):
    return Line(a, b, color=color, stroke_width=3)


class S18(SpokenScene):
    def construct(self):
        e = embryo_parts(EC)
        head, heart = e["head"], e["heart"]
        # labels with leaders
        l_sac = lab("yolk sac", 5.6, 2.6, 30, ORANGE)
        k_sac = leader([4.7, 2.5, 0], EC + P(2.5, 2.1), ORANGE)
        l_brain = lab("brain", -5.6, 1.9, 30, BLUE)
        k_brain = leader([-5.0, 1.9, 0], head.get_left() + P(-0.05, 0), BLUE)
        l_heart = lab("heart", -5.6, 0.0, 30, TEXT)
        k_heart = leader([-5.05, 0.0, 0], heart.get_left() + P(-0.05, 0), TEXT)
        self.add(e["yolk"], head, e["trunk"], heart, l_sac, k_sac,
                 l_brain, k_brain, l_heart, k_heart, e["macs"])
        self.at("lacking")
        title = lab("Ncx1 embryo", -4.5, 3.3, 36, TEXT)
        self.play(FadeIn(title, shift=RIGHT * 0.1), run_time=0.5)
        self.at("the heart needs to beat")
        nh = lab("no heartbeat", -5.6, -0.9, 30, RED)
        flat = Line([-6.4, -1.45, 0], [-3.6, -1.45, 0], color=RED, stroke_width=6)
        self.play(FadeIn(nh), Create(flat), Indicate(heart, color=RED, scale_factor=1.3), run_time=0.7)
        l_ves = lab("blood vessels:\nno flow", -5.1, -2.7, 28, BLOOD, line_spacing=0.8)
        k_ves = leader([-4.5, -2.7, 0], EC + P(1.2, -1.15), BLOOD)
        self.play(Create(e["v1"]), Create(e["v2"]), FadeIn(l_ves), Create(k_ves), run_time=0.7)
        self.at("still made yolk sac")
        ml = lab("yolk-sac\nmacrophages", 5.0, -2.65, 28, ORANGE)
        k_ml = leader([4.2, -2.85, 0], EC + P(2.45, -2.05), ORANGE)
        self.play(FadeIn(ml), Create(k_ml), Indicate(e["macs"], color=ORANGE, scale_factor=1.04),
                  run_time=0.6)
        self.finish()


LC19, RC19, SC = P(-3.35, 0.15), P(3.35, 0.15), 0.80


def comparison_embryo(c, title, no_flow=False):
    e = embryo_parts(c, SC)
    body = VGroup(e["yolk"], e["head"], e["trunk"], e["heart"], e["v1"], e["v2"], e["macs"])
    # All captions sit above or below the sac, with leaders to the organs.
    labels = VGroup(lab(title, c[0], 3.5, 34),
                    lab("brain", c[0]-1.2, 2.95, 30, BLUE),
                    leader(c+P(-1.2,2.6), e["head"].get_top(), BLUE),
                    lab("yolk sac", c[0]+1.15, 2.95, 30, ORANGE),
                    leader(c+P(1.15,2.6), c+P(1.55,2.05), ORANGE),
                    lab("heart", c[0]-1.1, -2.85, 30, TEXT),
                    leader(c+P(-1.1,-2.4), e["heart"].get_bottom(), TEXT),
                    lab("blood vessels", c[0]+1.25, -2.85, 28, BLOOD),
                    leader(c+P(1.25,-2.4), c+P(1.3,-1.0), BLOOD))
    if no_flow:
        labels.add(lab("no beat", c[0]-1.1, -3.18, 28, RED),
                   lab("no flow", c[0]+1.25, -3.18, 28, RED))
    return e, body, labels


class S19(SpokenScene):
    def construct(self):
        L,lb,ll = comparison_embryo(LC19,"Ncx1 embryo",True)
        R,rb,rl = comparison_embryo(RC19,"normal embryo")
        self.add(lb,ll,rb,rl)
        self.at("no brain")
        nb=lab("no brain microglia",LC19[0],-3.65,26,RED)
        self.play(FadeIn(nb),Indicate(L["head"],color=RED,scale_factor=1.1),run_time=0.4)
        self.at("so the progenitors")
        # Move actual orange sac cells along the connected sac-heart-brain vessel.
        movers=[R["macs"][i] for i in (3,4,6)]
        paths=[]
        for m in movers:
            path=VMobject().set_points_as_corners([m.get_center(),R["path"].get_start()])
            path.append_vectorized_mobject(R["path"])
            paths.append(path)
        self.play(LaggedStart(*[MoveAlongPath(m,path) for m,path in zip(movers,paths)],lag_ratio=0.12),run_time=1.6)
        center=R["head"].get_center()
        self.play(*[m.animate.scale(0.75).move_to(center+P((i-1)*0.25,0.1*(i%2))) for i,m in enumerate(movers)],run_time=0.3)
        self.finish()


# --------------------------------------------------------------------------------------------------
class S20(SpokenScene):
    def construct(self):
        cc = P(-3.0, 0.0)
        s = 5.0
        mg = micro(cc, s, angles=[95, 150, 210, 265])
        r_body = 0.17 * s
        rx = cc[0] + r_body
        rec_stalk = Rectangle(width=0.3, height=1.0, stroke_width=0, fill_color=PINK, fill_opacity=0.95).move_to([rx + 0.1, 0, 0])
        rec_head = Circle(radius=0.3, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.95).move_to([rx + 0.65, 0, 0])
        rec = VGroup(rec_stalk, rec_head)
        mem = T("cell membrane", 26, GREY).move_to([rx - 0.2, -1.55, 0])
        self.add(mg)
        self.at("also need the receptor")
        rc = chip("CSF1R receptor", PINK, size=44, pad=0.28).move_to([3.1, 0, 0])
        ln = Line([rx + 0.98, 0, 0], [rc.get_left()[0] - 0.05, 0, 0], color=PINK, stroke_width=4)
        self.play(FadeIn(rec, scale=0.4), run_time=0.4)
        self.play(Create(ln), FadeIn(rc, shift=LEFT * 0.2), run_time=0.6)
        self.at("mice without it")
        mglist = VGroup(mg, rec, ln, rc)
        bl_c, br_c = P(-3.4, -0.2), P(3.4, -0.2)
        bl = Circle(radius=2.75, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.1).move_to(bl_c)
        br = Circle(radius=2.75, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.1).move_to(br_c)
        offs = [(0, 0)] + [(1.5 * np.cos(np.deg2rad(a)), 1.5 * np.sin(np.deg2rad(a))) for a in (90, 162, 234, 306, 18)]
        dots_l = VGroup(*[micro(bl_c + P(*o), 1.15) for o in offs])
        one = micro(br_c + P(0.5, -0.3), 1.0).set_opacity(0.5)
        ll = lab("normal brain", bl_c[0], 3.15, 32, BLUE)
        lr = lab("brain without CSF1R", br_c[0], 3.15, 32, RED)
        self.play(FadeOut(mglist), FadeIn(bl), FadeIn(br), FadeIn(ll), FadeIn(lr), FadeIn(dots_l, scale=0.5), FadeIn(one), run_time=0.4)
        self.at("few or none")
        fn = lab("few or none", br_c[0], -3.35, 34, RED)
        self.play(FadeIn(fn, shift=UP * 0.1), Indicate(br, color=RED, scale_factor=1.03), run_time=0.9)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        tis = RoundedRectangle(corner_radius=0.3, width=7.4, height=6.6, stroke_color=BLUE, stroke_width=3,
                               fill_color=BLUE, fill_opacity=0.07).move_to([-3.3, 0, 0])
        tl = lab("adult brain", -5.3, 2.85, 30, BLUE)
        a = micro([-3.3, 0.0, 0], 3.6)
        vessel = RoundedRectangle(corner_radius=0.5, width=3.9, height=6.6, stroke_color=BLOOD, stroke_width=5,
                                  fill_color=BLOOD, fill_opacity=0.08).move_to([4.3, 0, 0])
        vl = lab("blood vessel", 4.3, 2.85, 28, BLOOD)
        mons = [cell([3.2, y, 0], 0.5, BLOOD, fill=1.0) for y in (1.5, 0.0, -1.5)]
        ml = lab("blood\nmonocytes", 5.2, 0.0, 26, TEXT, line_spacing=0.8)
        self.add(tis, tl, a, vessel, vl, *mons, ml)
        self.at("microglia renew themselves")
        b = a.copy()
        self.add(b)
        sl = lab("microglia renew themselves", -3.3, -2.75, 32, ORANGE)
        self.play(a.animate.scale(0.52).move_to([-5.0, 0.0, 0]), b.animate.scale(0.52).move_to([-1.6, 0.0, 0]),
                  FadeIn(sl, shift=UP * 0.1), run_time=0.75)
        self.play(Indicate(a, color=ORANGE, scale_factor=1.08), Indicate(b, color=ORANGE, scale_factor=1.08), run_time=0.7)
        self.at("blood monocytes")
        self.play(*[Indicate(m[1], color=BLOOD, scale_factor=1.08) for m in mons], run_time=0.4)
        self.at("do not replace them")
        barrier = Line([1.4, -1.2, 0], [1.4, 1.2, 0], color=RED, stroke_width=8)
        stay = lab("monocytes stay\nin the vessel", 4.3, -2.75, 26, TEXT, line_spacing=0.8)
        self.play(Create(barrier), FadeIn(stay), run_time=0.5)
        self.finish()


# --------------------------------------------------------------------------------------------------
class S22Take(SpokenScene):
    def construct(self):
        title = lab("read a fate map against its source", 0, 3.1, 44, TEXT, font=TITLE_FONT)
        yolk = yolk_ellipse(P(-4, 0), 4.1, 3.8)
        brain = Circle(radius=1.85, stroke_color=BLUE, stroke_width=4,
                       fill_color=BLUE, fill_opacity=0.14).move_to([4,0,0])
        labels = VGroup(lab("yolk sac", -4, -2.3, 32, ORANGE), lab("brain", 4, -2.3, 32, BLUE))
        arrow = arr([-1.7,0,0],[1.8,0,0],ORANGE,8,0.3)
        riders = VGroup(*[cell([-4.5+0.55*(i%3),0.4-0.8*(i//3),0],0.22,ORANGE,fill=0.9) for i in range(6)])
        self.add(title,yolk,brain,labels,arrow,riders)
        self.at("against its source")
        echo = lab("source labeled ⅓; adult count ⅓ → most",0,-3.25,30,TEXT)
        self.play(FadeIn(echo), run_time=0.35)
        self.at("in mice")
        self.play(FadeIn(lab("in mice",0,1.9,32,ORANGE)),run_time=0.25)
        self.at("most")
        for i,r in enumerate(riders):
            r.generate_target()
            r.target.move_to([3.4+0.6*(i%3),0.45-0.9*(i//3),0])
        self.play(LaggedStart(*[MoveToTarget(r,path_arc=-0.12) for r in riders],lag_ratio=0.08),run_time=1.4)
        self.finish()


class S23End(EndCard):
    LINE = "In mice, most microglia were born in the yolk sac."

    def construct(self):
        l1 = T("In mice, most microglia", 64, TEXT, font=TITLE_FONT)
        l2 = T("were born in the yolk sac.", 64, ORANGE, font=TITLE_FONT)
        g = VGroup(l1, l2).arrange(DOWN, buff=0.35)
        fit(g, max_w=12.4)
        sub = T("biochemistrypedia.com", size=28, color=TEAL)
        full = VGroup(g, sub).arrange(DOWN, buff=0.7).move_to(ORIGIN)
        self.add(full)
        self.finish()
