"""Chapter 2 of "Ocular Dominance and the Critical Period": Six Days at Four Weeks (Biochemistrypedia film)

COLOR MAP (one color per concept, shared by all six chapters; ch1's blue/yellow eyes are replaced by the
chapters' own convention: left hemisphere recorded, right eye contralateral, left eye ipsilateral)
  ORANGE = the right eye (contralateral), the one that gets closed here; histogram group 1 end; its stripes and axon
  BLUE   = the left eye (ipsilateral), the open eye here; histogram group 7 end; its stripes
  PURPLE = a cortical cell driven by both eyes (the middle of the histogram)
  GOLD   = time: the sensitive-period curve, "6 days", "1963", credits, small tags
  GREEN  = "still works" ticks
  GREY   = outlines, the cortex, faces, neutral things (LIGHT = brighter grey for axis text)
  TEXT   = bright white-ish: stitches, electrode, headlines
Histogram bars run from orange (group 1) through purple (group 4) to blue (group 7).
Every histogram in the film comes from the one Hist class: x title, three end labels, y label, schematic tag.
"""
import numpy as np

from bp_style import *  # noqa: F401,F403

ORANGE = "#FF9A3C"
PURPLE = "#B58CD9"
FACE_BG = "#171b24"
LIGHT = "#C3CAD6"


# ------------------------------------------------------------------ small helpers
def arr(a, b, color=GREY, w=6, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def make_eye(color, scale=1.0):
    ell = Ellipse(width=2.0, height=1.1, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15)
    pup = Circle(radius=0.3, stroke_width=0, fill_color=color, fill_opacity=1)
    glint = Circle(radius=0.08, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pup.get_center() + UR * 0.1)
    return VGroup(ell, pup, glint).scale(scale)


def eye_close(g):
    return [g[0].animate.stretch_to_fit_height(g[0].width * 0.07), g[1].animate.set_opacity(0), g[2].animate.set_opacity(0)]


def shut(g):
    """Closed from the first frame (no animation)."""
    g[0].stretch_to_fit_height(g[0].width * 0.07)
    g[1].set_opacity(0)
    g[2].set_opacity(0)
    return g


def stitches(g):
    c = g[0].get_center()
    w = g[0].width
    return VGroup(*[Line(c + np.array([k * w, -0.2 * w, 0]), c + np.array([k * w, 0.2 * w, 0]), color=TEXT, stroke_width=3)
                    for k in (-0.28, 0.0, 0.28)])


def tick_mark(c, color=GREEN, s=1.0):
    c = np.array([c[0], c[1], 0.0])
    return VGroup(Line(c + s * np.array([-0.3, 0.0, 0]), c + s * np.array([-0.1, -0.24, 0]), color=color, stroke_width=9),
                  Line(c + s * np.array([-0.1, -0.24, 0]), c + s * np.array([0.34, 0.3, 0]), color=color, stroke_width=9))


class Face:
    """A schematic face (kitten, adult cat or macaque). Right eye (orange) is on the viewer's left."""

    def __init__(self, cx, cy, r, kind="kitten", closed=False, simple=False):
        c = np.array([cx, cy, 0.0])
        self.c, self.r = c, r
        base = VGroup()
        if kind == "macaque":
            for sx in (-1, 1):
                base.add(Circle(radius=0.3 * r, stroke_color=GREY, stroke_width=4, fill_color=FACE_BG, fill_opacity=1)
                         .move_to(c + np.array([sx * 0.98 * r, 0.1 * r, 0])))
        else:
            h = 1.38 if kind == "cat" else 1.2
            for sx in (-1, 1):
                base.add(Polygon(c + np.array([sx * 0.95 * r, 0.4 * r, 0]), c + np.array([sx * 0.85 * r, h * r, 0]),
                                 c + np.array([sx * 0.2 * r, 0.95 * r, 0]), stroke_color=GREY, stroke_width=4,
                                 fill_color=FACE_BG, fill_opacity=1))
        base.add(Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=FACE_BG, fill_opacity=1).move_to(c))
        if kind == "macaque":
            base.add(Ellipse(width=1.15 * r, height=0.85 * r, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                             fill_opacity=0.12).move_to(c + np.array([0, -0.42 * r, 0])))
            for sx in (-1, 1):
                base.add(Dot(c + np.array([sx * 0.12 * r, -0.35 * r, 0]), radius=0.045 * r, color=GREY))
            base.add(Line(c + np.array([-0.25 * r, -0.65 * r, 0]), c + np.array([0.25 * r, -0.65 * r, 0]), color=GREY, stroke_width=3))
        else:
            nose = Triangle(stroke_width=0, fill_color=GREY, fill_opacity=0.9).scale(0.1 * r).rotate(PI).move_to(c + np.array([0, -0.2 * r, 0]))
            base.add(nose)
            if not simple:
                base.add(Line(c + np.array([0, -0.28 * r, 0]), c + np.array([0, -0.42 * r, 0]), color=GREY, stroke_width=3))
                base.add(Line(c + np.array([0, -0.42 * r, 0]), c + np.array([-0.2 * r, -0.5 * r, 0]), color=GREY, stroke_width=3))
                base.add(Line(c + np.array([0, -0.42 * r, 0]), c + np.array([0.2 * r, -0.5 * r, 0]), color=GREY, stroke_width=3))
            for sx in ((-1, 1) if not simple else ()):
                for dy in (0.05, -0.12, -0.3):
                    base.add(Line(c + np.array([sx * 0.4 * r, -0.28 * r, 0]), c + np.array([sx * 1.22 * r, (-0.28 + dy) * r, 0]),
                                  color=GREY, stroke_width=2))
        ey = 0.2 * r
        self.eR = make_eye(ORANGE, 0.3 * r).move_to(c + np.array([-0.5 * r, ey, 0]))
        self.eL = make_eye(BLUE, 0.3 * r).move_to(c + np.array([0.5 * r, ey, 0]))
        self.base = base
        if closed:
            shut(self.eR)
        self.st = stitches(self.eR)
        self.all = VGroup(base, self.eR, self.eL, self.st) if closed else VGroup(base, self.eR, self.eL)

    def add(self, scene):
        scene.add(self.all)
        return self

    def close_right(self):
        return eye_close(self.eR)


def cortex(cx, cy, w, h, sp=1.3, cells_dy=-0.1, r=0.4, color=GREY):
    box = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.05).move_to([cx, cy, 0])
    cs = VGroup()
    for i in range(9):
        rr, c = divmod(i, 3)
        cs.add(Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
               .move_to([cx + (c - 1) * sp, cy + cells_dy + (1 - rr) * sp, 0]))
    return box, cs


# ------------------------------------------------------------------ the histogram (one component for the whole film)
H_NORMAL = [3, 6, 10, 12, 9, 5, 2]
H_DEPRIVED = [0.1, 0.3, 0.6, 1.2, 3, 8, 13]      # about 3 months of closure from birth (schematic)
H_SHIFT = [0.5, 1, 2, 3, 6, 10, 13]              # 6 days at the peak (schematic)
H_FALL = [0.5, 1, 2, 12, 9, 5, 2]                # groups 1 to 3 down to a fraction of normal


def gcol(i):
    O, P, B = ManimColor(ORANGE), ManimColor(PURPLE), ManimColor(BLUE)
    return interpolate_color(O, P, i / 3) if i <= 3 else interpolate_color(P, B, (i - 3) / 3)


class Hist:
    """Seven-group ocular dominance histogram. full: cx 0, spacing 1.5. compact: for side-by-side panels."""

    def __init__(self, cx=0.0, base=-1.5, sp=1.5, unit=0.33, bw=1.2, compact=False):
        self.cx, self.base, self.sp, self.unit, self.bw, self.compact = cx, base, sp, unit, bw, compact
        self.hx = [cx + (i - 3) * sp for i in range(7)]
        self.pad = 0.5 if compact else 0.9

    def bars(self, h):
        out = VGroup()
        for i, v in enumerate(h):
            hh = max(v * self.unit, 0.03)
            out.add(Rectangle(width=self.bw, height=hh, stroke_color=gcol(i), stroke_width=2, fill_color=gcol(i),
                              fill_opacity=0.6).move_to([self.hx[i], self.base + hh / 2, 0]))
        return out

    def ghost(self, h=H_NORMAL, idx=range(7)):
        return VGroup(*[Rectangle(width=self.bw, height=h[i] * self.unit, stroke_color=LIGHT, stroke_width=2.5,
                                  fill_opacity=0).move_to([self.hx[i], self.base + h[i] * self.unit / 2, 0]) for i in idx])

    def axis(self):
        line = Line([self.hx[0] - self.pad, self.base, 0], [self.hx[6] + self.pad, self.base, 0], color=GREY, stroke_width=3)
        nums = VGroup(*[T(str(i + 1), 26, TEXT).move_to([self.hx[i], self.base - 0.38, 0]) for i in range(7)])
        return VGroup(line, nums)

    def tags(self):
        if self.compact:
            a = T("right eye\n(closed)", 26, ORANGE, line_spacing=0.6)
            m = T("both\neyes", 26, PURPLE, line_spacing=0.6)
            b = T("left eye\n(open)", 26, BLUE, line_spacing=0.6)
            y = self.base - 1.2
        else:
            a = T("right eye (closed)", 26, ORANGE)
            m = T("both eyes", 26, PURPLE)
            b = T("left eye (open)", 26, BLUE)
            y = self.base - 1.0
        a.move_to([self.hx[0], y, 0])
        m.move_to([self.hx[3], y, 0])
        b.move_to([self.hx[6], y, 0])
        return VGroup(a, m, b)

    def xtitle(self):
        y = self.base - (1.95 if self.compact else 1.65)
        return T("ocular dominance group" if self.compact else "ocular dominance group, 1 to 7", 26, LIGHT).move_to([self.cx, y, 0])

    def ylab(self):
        x = self.hx[0] - self.pad - 0.38
        return T("number of cells", 26, LIGHT).rotate(PI / 2).move_to([x, self.base + 2.0, 0])

    def frame(self):
        return VGroup(self.axis(), self.tags(), self.xtitle(), self.ylab())

    def normal_label(self):
        return T("normal", 26, LIGHT).move_to([self.hx[1], self.base + H_NORMAL[1] * self.unit + 0.35, 0])


def schem_tag(x=0.0, y=3.45, size=24):
    return chip("schematic", LIGHT, size=size, pad=0.14, fill_opacity=0.08).move_to([x, y, 0])


def corner_eyes(y=3.3, x=5.7, scale=0.55):
    a = shut(make_eye(ORANGE, scale).move_to([-x, y, 0]))
    b = make_eye(BLUE, scale).move_to([x, y, 0])
    return a, b, stitches(a)


# the age plot (sensitivity to closure against age) ---------------------------------------------
PX0, PX1, PYB, PYT = -5.0, 6.4, -2.3, 2.4
SX = (PX1 - PX0) / 14.0


def px(w):
    return PX0 + w * SX


def sens(w):
    s = lambda z: 1 / (1 + np.exp(-z))
    return s((w - 3.6) / 0.35) * (1 - 0.95 * s((w - 10.0) / 1.1))


def py(v):
    return PYB + (PYT - PYB) * v


def curve(a, b, n=90, color=GOLD, width=7):
    ws = np.linspace(a, b, n)
    return VMobject(color=color, stroke_width=width).set_points_smoothly([np.array([px(w), py(sens(w)), 0]) for w in ws])


def age_axes():
    ax = VGroup(Line([PX0, PYB, 0], [PX1, PYB, 0], color=GREY, stroke_width=3),
                Line([PX0, PYB, 0], [PX0, PYT + 0.2, 0], color=GREY, stroke_width=3))
    ticks = VGroup(*[T(str(w), 26, TEXT).move_to([px(w), PYB - 0.4, 0]) for w in range(0, 15, 2)])
    xl = T("age when closure begins (weeks)", 26, LIGHT).move_to([px(7), PYB - 1.0, 0])
    yl = T("effect of closure\n(susceptibility)", 26, LIGHT, line_spacing=0.6).rotate(PI / 2).move_to([PX0 - 0.95, 0.05, 0])
    return VGroup(ax, ticks, xl), yl


def band(w0, w1, color=GOLD, op=0.16):
    return Rectangle(width=px(w1) - px(w0), height=PYT - PYB, stroke_width=0, fill_color=color,
                     fill_opacity=op).move_to([(px(w0) + px(w1)) / 2, (PYT + PYB) / 2, 0])


def hatch_band(w0, w1):
    r = Rectangle(width=px(w1) - px(w0), height=PYT - PYB, stroke_width=0, fill_color=TEXT, fill_opacity=0.07)
    r.move_to([(px(w0) + px(w1)) / 2, (PYT + PYB) / 2, 0])
    d = DashedVMobject(Rectangle(width=px(w1) - px(w0), height=PYT - PYB, stroke_color=LIGHT, stroke_width=2.5, fill_opacity=0)
                       .move_to(r.get_center()), num_dashes=40)
    return VGroup(r, d)


def chip_glyph(text, kind, color=GOLD, size=24):
    lab = T(text, size, color)
    xs = np.linspace(0, 1, 40)
    if kind == "step":
        pts = [np.array([x * 0.9, 0.5 * (1 - 1 / (1 + np.exp(-(x - 0.6) * 18))), 0]) for x in xs]
    else:
        pts = [np.array([x * 0.9, 0.5 * np.exp(-((x - 0.5) / 0.22) ** 2), 0]) for x in xs]
    gl = VMobject(color=color, stroke_width=4).set_points_smoothly(pts)
    gl.move_to(ORIGIN)
    row = VGroup(gl, lab).arrange(RIGHT, buff=0.25)
    box = RoundedRectangle(corner_radius=0.14, width=row.width + 0.4, height=max(row.height, 0.55) + 0.3, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=0.12).move_to(row)
    return VGroup(box, row)


def predict_row():
    pr = T("Predict", 34, GOLD, weight=BOLD)
    ca = chip_glyph("one switch-off point", "step")
    orr = T("or", 26, LIGHT)
    cb = chip_glyph("a rise and a fall", "hump")
    row = VGroup(ca, orr, cb).arrange(RIGHT, buff=0.3)
    row.move_to([1.0, 3.3, 0])
    pr.move_to([row.get_left()[0] - 0.35 - pr.width / 2, 3.3, 0])
    return pr, ca, orr, cb


BRIEF_AGES = (1.0, 4.0, 7.0, 10.0, 12.4)
BRIEF_Y = 0.5


def brief_bars():
    return [Rectangle(width=0.75, height=0.42, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8)
            .move_to([px(a) + 0.375, BRIEF_Y, 0]) for a in BRIEF_AGES]


def brief_ticks():
    return VGroup(*[Line([px(a), PYB, 0], [px(a), PYB + 0.28, 0], color=GOLD, stroke_width=5) for a in BRIEF_AGES])


def brief_label():
    return T("same brief closure, begun at different ages", 26, GOLD).move_to([px(7), BRIEF_Y + 0.75, 0])


# the stripes of layer 4C ------------------------------------------------------------------------
def stripes(cx, cy, total_w, h, orange_share=0.5, pairs=4):
    """Alternating orange and blue stripes inside a box; orange_share is the orange part of each pair."""
    pw = total_w / pairs
    out = VGroup()
    x = cx - total_w / 2
    for _ in range(pairs):
        for share, col in ((orange_share, ORANGE), (1 - orange_share, BLUE)):
            w = pw * share
            out.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=col, fill_opacity=0.55).move_to([x + w / 2, cy, 0]))
            x += w
    return out


def stripes_box(cx, cy, total_w, h):
    return Rectangle(width=total_w, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, cy, 0])


def stripe_legend(xo, xb, y):
    o = VGroup(Rectangle(width=0.4, height=0.4, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8), T("closed eye's stripes", 26, ORANGE))
    o.arrange(RIGHT, buff=0.2).move_to([xo, y, 0])
    b = VGroup(Rectangle(width=0.4, height=0.4, stroke_width=0, fill_color=BLUE, fill_opacity=0.8), T("open eye's stripes", 26, BLUE))
    b.arrange(RIGHT, buff=0.2).move_to([xb, y, 0])
    return o, b


# an axon arbor, built from a rule so the same drawing can be thinned --------------------------------
def arbor(cx, base_y, width, height, seed=7):
    rng = np.random.RandomState(seed)
    segs = []

    def grow(p, ang, L, d):
        q = p + L * np.array([np.sin(ang), np.cos(ang), 0])
        segs.append((p, q, d))
        if d >= 4:
            return
        nxt = 1.0 if d == 0 else L * 0.8
        for da in (-0.32, 0.32):
            grow(q, ang + da + rng.uniform(-0.1, 0.1), nxt, d + 1)

    grow(np.array([0.0, 0.0, 0.0]), 0.0, 2.2, 0)
    pts = np.array([s[1] for s in segs] + [s[0] for s in segs])
    xmin, xmax, ymax = pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].max()
    k = min(width / (xmax - xmin), height / ymax)
    xmid = (xmin + xmax) / 2
    lines, depths = [], []
    for p, q, d in segs:
        a = np.array([cx + (p[0] - xmid) * k, base_y + p[1] * k, 0])
        b = np.array([cx + (q[0] - xmid) * k, base_y + q[1] * k, 0])
        lines.append(Line(a, b, color=ORANGE, stroke_width=max(2.5, 10 - 2.0 * d)))
        depths.append(d)
    return lines, depths


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Ocular Dominance and the Critical Period"
    TITLE = "Six Days at Four Weeks"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), 24, LIGHT)
        title = T(self.TITLE, 60, TEXT, font=TITLE_FONT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.36)
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S01(SpokenScene):
    def construct(self):
        f = Face(3.6, -0.1, 2.4, "kitten")
        box, cells = cortex(-3.8, 0.1, 5.2, 5.2, sp=1.4, cells_dy=0.0)
        lr = T("right eye", 26, ORANGE).move_to([2.4, -3.1, 0])
        ll = T("left eye", 26, BLUE).move_to([4.8, -3.1, 0])
        cl = T("cortical cells", 28, LIGHT).move_to([-3.8, -3.1, 0])
        self.play(FadeIn(f.all), FadeIn(lr), FadeIn(ll), FadeIn(box), FadeIn(cells), FadeIn(cl), run_time=0.4)
        self.at("sew")
        self.play(*f.close_right(), run_time=0.6)
        self.play(FadeIn(f.st), run_time=0.3)
        self.at("cortical cells")
        self.play(Indicate(cells, color=TEXT, scale_factor=1.08), run_time=0.9)
        a = arr([1.7, 0.4, 0], [-1.1, 0.4, 0], ORANGE, 8)
        self.at("used to drive")
        self.play(GrowArrow(a), run_time=0.5)
        q = T("?", 130, GOLD, weight=BOLD).move_to([-3.8, 0.1, 0])
        self.play(cells.animate.set_opacity(0.25), FadeIn(q, scale=1.3), run_time=0.5)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        f = Face(3.6, -0.1, 2.4, "kitten", closed=True).add(self)
        lr = T("right eye", 26, ORANGE).move_to([2.4, -3.1, 0])
        ll = T("left eye", 26, BLUE).move_to([4.8, -3.1, 0])
        box, cells = cortex(-3.8, 0.1, 5.2, 5.2, sp=1.4, cells_dy=0.0)
        a = arr([1.7, 0.4, 0], [-1.1, 0.4, 0], ORANGE, 8)
        q = T("?", 130, GOLD, weight=BOLD).move_to([-3.8, 0.1, 0])
        cl = T("cortical cells", 28, LIGHT).move_to([-3.8, -3.1, 0])
        cells.set_opacity(0.25)
        old = VGroup(box, cells, a, q, cl)
        self.add(lr, ll, old)
        self.play(FadeOut(old), run_time=0.25)
        yr = T("1963", 120, GOLD, font=TITLE_FONT).move_to([-3.3, 0.9, 0])
        self.at("1963")
        self.play(FadeIn(yr, shift=UP * 0.15), run_time=0.7)
        nm = T("Wiesel and Hubel", 48, TEXT).move_to([-3.3, -0.8, 0])
        self.at("Wiesel")
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.6)
        self.at("one eye closed")
        self.play(Indicate(VGroup(f.eR, f.st), color=ORANGE, scale_factor=1.25), run_time=1.0)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        AY, BY, X0, X1 = -1.35, -0.2, -4.6, 4.6
        axis = arr([-6.2, AY, 0], [6.4, AY, 0], GREY, 4, tip=0.25)
        eye = make_eye(ORANGE, 1.5).move_to([X0, 2.1, 0])
        self.play(Create(axis), run_time=0.4)
        self.at("sutured")
        self.play(FadeIn(eye, shift=DOWN * 0.1), run_time=0.3)
        self.at("lids")
        self.play(*eye_close(eye), run_time=0.45)
        st = stitches(eye).move_to(eye[0])
        self.play(FadeIn(st), run_time=0.15)
        tick0 = Line([X0, AY + 0.25, 0], [X0, BY + 0.55, 0], color=TEXT, stroke_width=5)
        l0 = T("birth or\nnear birth", 28, TEXT, line_spacing=0.6).move_to([X0, AY - 0.85, 0])
        self.at("at or near birth")
        self.play(FadeIn(tick0), FadeIn(l0, shift=UP * 0.1), run_time=0.5)
        el = VGroup(Line([6.0, 3.6, 0], [X1 + 0.1, BY + 0.8, 0], stroke_width=7, color=TEXT), Dot([X1 + 0.1, BY + 0.8, 0], radius=0.12, color=TEXT))
        rl = T("recording", 30, TEXT).move_to([2.6, 2.4, 0])
        self.at("recorded")
        self.play(FadeIn(el, shift=DOWN * 0.3), FadeIn(rl), run_time=0.6)
        bar = Rectangle(width=X1 - X0, height=1.0, stroke_width=0, fill_color=ORANGE, fill_opacity=0.55).move_to([(X0 + X1) / 2, BY, 0])
        self.at("after about")
        self.play(GrowFromEdge(bar, LEFT), run_time=0.7)
        tick1 = Line([X1, AY + 0.25, 0], [X1, BY - 0.5, 0], color=GOLD, stroke_width=5)
        l1 = T("about\n3 months", 28, GOLD, line_spacing=0.6).move_to([X1, AY - 0.85, 0])
        self.at("three months")
        self.play(FadeIn(tick1), FadeIn(l1, shift=UP * 0.1), run_time=0.6)
        bl = T("eye closed", 30, TEXT).move_to([(X0 + X1) / 2, BY, 0])
        self.at("of closure")
        self.play(FadeIn(bl), run_time=0.5)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        h = Hist()
        ca, cb, cst = corner_eyes()
        bars = h.bars(H_NORMAL)
        ghost = h.ghost()
        nl = h.normal_label()
        self.play(FadeIn(VGroup(h.frame(), ca, cb, cst, bars, schem_tag(0, 3.45))), run_time=0.6)
        self.at("cortical cells")
        self.play(Indicate(VGroup(bars[0], bars[1], bars[2]), color=ORANGE, scale_factor=1.06), run_time=0.9)
        self.at("could be driven")
        self.add(ghost)
        self.play(Transform(bars, h.bars(H_FALL)), FadeIn(nl), run_time=1.1)
        self.at("closed eye")
        self.play(Indicate(VGroup(ca, cst), color=ORANGE, scale_factor=1.3), run_time=0.8)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        yA, yB = 1.75, -1.55
        eA = shut(make_eye(ORANGE, 1.1).move_to([-5.5, yA, 0]))
        stA = stitches(eA)
        lA = T("closed eye", 28, ORANGE).move_to([-5.5, yA - 0.95, 0])
        eB = make_eye(BLUE, 1.1).move_to([-5.5, yB, 0])
        lB = T("other eye", 28, BLUE).move_to([-5.5, yB - 0.95, 0])
        self.play(FadeIn(VGroup(eA, stA, lA, eB, lB)), run_time=0.4)
        retA = chip("retina", ORANGE, size=32).move_to([-2.9, yA, 0])
        retB = chip("retina", BLUE, size=32).move_to([-2.9, yB, 0])
        a1A = arr([-4.4, yA, 0], [-3.9, yA, 0], ORANGE, 6)
        a1B = arr([-4.4, yB, 0], [-3.9, yB, 0], BLUE, 6)
        self.at("retina")
        self.play(FadeIn(retA, shift=LEFT * 0.1), FadeIn(retB, shift=LEFT * 0.1), GrowArrow(a1A), GrowArrow(a1B), run_time=0.4)
        self.at("still responded")
        self.play(retA[0].animate.set_fill(ORANGE, 0.75), Flash(retA, color=ORANGE, flash_radius=1.3, line_length=0.3), run_time=0.9)
        self.play(retA[0].animate.set_fill(ORANGE, 0.16), run_time=0.4)
        box = RoundedRectangle(corner_radius=0.3, width=6.4, height=7.0, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.05).move_to([3.5, 0.1, 0])
        ttl = T("LGN", 32, TEXT).move_to([3.5, 3.0, 0])
        a2A = arr([-1.85, yA, 0], [0.2, yA, 0], ORANGE, 6)
        a2B = arr([-1.85, yB, 0], [0.2, yB, 0], BLUE, 6)
        rowA = VGroup(*[Circle(radius=0.5, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.12)
                        .move_to([3.5 + (i - 2) * 1.12, yA, 0]) for i in range(5)])
        rowB = VGroup(*[Circle(radius=0.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.12)
                        .move_to([3.5 + (i - 2) * 1.12, yB, 0]) for i in range(5)])
        self.at("LGN")
        self.play(FadeIn(box), FadeIn(ttl), GrowArrow(a2A), GrowArrow(a2B), FadeIn(rowA), FadeIn(rowB), run_time=0.5)
        self.at("cells")
        self.play(*[c.animate.set_fill(ORANGE, 0.85) for c in rowA], Flash(rowA, color=ORANGE, flash_radius=3.0, line_length=0.3),
                  *[c.animate.set_fill(BLUE, 0.55) for c in rowB], run_time=0.9)
        self.at("those serving")
        self.play(Indicate(rowA, color=ORANGE, scale_factor=1.04), run_time=0.8)
        self.at("looked smaller")
        self.play(*[c.animate.scale(0.5).set_fill(ORANGE, 0.55) for c in rowA], run_time=1.1)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        y = 0.2
        eye = shut(make_eye(ORANGE, 0.8).move_to([-5.9, y, 0]))
        st = stitches(eye)
        ret = chip("retina", ORANGE, size=30).move_to([-3.5, y, 0])
        lgn = chip("LGN", ORANGE, size=30).move_to([-0.95, y, 0])
        a1 = arr([-5.0, y, 0], [-4.5, y, 0], ORANGE, 6)
        a2 = arr([-2.5, y, 0], [-1.9, y, 0], ORANGE, 6)
        path = VGroup(eye, st, ret, lgn, a1, a2)
        cap = T("closed eye", 26, ORANGE).move_to([-5.9, y - 0.85, 0])
        self.play(FadeIn(path), FadeIn(cap), run_time=0.5)
        self.at("not broken")
        ticks = VGroup(tick_mark([-5.9, 1.25]), tick_mark([-3.5, 1.25]), tick_mark([-0.95, 1.25]))
        ok = T("eye, retina, LGN still respond", 28, GREEN).move_to([-3.4, -1.85, 0])
        self.play(LaggedStart(*[FadeIn(t, scale=1.6) for t in ticks], lag_ratio=0.25), FadeIn(ok, shift=UP * 0.1), run_time=0.9)
        cbox, ccells = cortex(3.9, 0.1, 5.2, 5.8, sp=1.3, cells_dy=-0.1)
        ctl = T("visual cortex", 30, TEXT).move_to([3.9, 2.45, 0])
        a3 = arr([-0.15, y, 0], [1.2, y, 0], ORANGE, 6)
        trav = arr([-5.9, -1.15, 0], [1.3, -1.15, 0], GOLD, 9, tip=0.3)
        self.at("What changed")
        self.play(FadeIn(cbox), FadeIn(ccells), FadeIn(ctl), GrowArrow(a3), GrowArrow(trav), run_time=0.9)
        lab2 = T("the change is in the brain", 28, GOLD, weight=BOLD).move_to([3.9, -3.3, 0])
        self.at("in the brain")
        self.play(FadeIn(lab2, shift=DOWN * 0.1), cbox.animate.set_stroke(GOLD, 6), run_time=0.8)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        f = Face(-3.9, 0.45, 2.3, "cat")
        al = T("adult cat", 30, TEXT).move_to([-3.9, -2.35, 0])
        h = Hist(cx=3.7, base=-1.0, sp=0.82, unit=0.27, bw=0.7, compact=True)
        bars = h.bars(H_NORMAL)
        hd = T("before closure", 28, LIGHT).move_to([3.7, 2.8, 0])
        self.play(FadeIn(f.all), FadeIn(al), FadeIn(h.frame()), FadeIn(bars), FadeIn(hd), run_time=0.5)
        self.at("closed")
        self.play(*f.close_right(), run_time=0.45)
        self.play(FadeIn(f.st), run_time=0.15)
        mo = chip("for months", GOLD, size=28).move_to([-3.9, -3.2, 0])
        self.at("months")
        self.play(FadeIn(mo, shift=UP * 0.1), run_time=0.35)
        hd2 = T("after months: no change", 28, PURPLE).move_to([3.7, 2.8, 0])
        self.at("showed no")
        self.play(ReplacementTransform(hd, hd2), Indicate(bars, color=PURPLE, scale_factor=1.04), run_time=0.9)
        self.finish()


S08_ROWS = [2.0, 1.0, 0.0, -1.0, -2.0]
S08_SPANS = [(0.5, 6.0), (3.0, 2.0), (4.0, 8.0), (8.0, 1.5), (6.0, 7.0)]
S08_X0, S08_K = -4.4, 0.74


def s08x(w):
    return S08_X0 + S08_K * w


def kitten_eyes(y):
    a = shut(make_eye(ORANGE, 0.34).move_to([-6.1, y, 0]))
    b = make_eye(BLUE, 0.34).move_to([-5.3, y, 0])
    return VGroup(a, stitches(a), b)


class S08(SpokenScene):
    def construct(self):
        cr = T("Hubel and Wiesel, 1970", 36, GOLD).move_to([0, 3.45, 0])
        axis = arr([-4.7, -2.7, 0], [6.4, -2.7, 0], GREY, 4, tip=0.25)
        ticks = VGroup(*[Line([s08x(w), -2.7, 0], [s08x(w), -2.55, 0], color=GREY, stroke_width=3) for w in (0, 4, 8, 12)])
        tl = VGroup(*[T(str(w), 26, TEXT).move_to([s08x(w), -3.05, 0]) for w in (0, 4, 8, 12)])
        at_ = T("age when closure begins (weeks)", 26, LIGHT).move_to([0.9, -3.55, 0])
        icons = [kitten_eyes(y) for y in S08_ROWS]
        khead = T("kitten", 26, LIGHT).move_to([-5.75, 3.0, 0])
        stubs = [Rectangle(width=0.22, height=0.42, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8)
                 .move_to([s08x(s) + 0.11, y, 0]) for y, (s, _) in zip(S08_ROWS, S08_SPANS)]
        self.play(FadeIn(cr, shift=DOWN * 0.1), FadeIn(VGroup(axis, ticks, tl, at_)), FadeIn(icons[0]), FadeIn(khead), FadeIn(stubs[0], scale=0.6), run_time=0.7)
        self.at("asked when")
        self.play(Indicate(at_, color=GOLD, scale_factor=1.08), run_time=0.8)
        self.at("closed one eye")
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.1) for i in icons[1:]], lag_ratio=0.25), run_time=1.2)
        self.at("different ages")
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in stubs[1:]], lag_ratio=0.2), run_time=0.9)
        bars = [Rectangle(width=S08_K * w, height=0.42, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8)
                .move_to([s08x(s) + S08_K * w / 2, y, 0]) for y, (s, w) in zip(S08_ROWS, S08_SPANS)]
        ll = T("length of closure", 26, ORANGE).move_to([s08x(3.2), 2.78, 0])
        self.at("different lengths")
        self.play(*[Transform(s, b) for s, b in zip(stubs, bars)], FadeIn(ll, shift=DOWN * 0.1), run_time=1.3)
        self.finish()


def s09_end(scene, with_label=True):
    ax, yl = age_axes()
    pr, ca, orr, cb = predict_row()
    bars = brief_bars()
    tk = brief_ticks()
    lab = brief_label()
    scene.add(ax, yl, pr, ca, orr, cb, tk, *bars)
    if with_label:
        scene.add(lab)
    return ax, yl, pr, ca, orr, cb, tk, bars, lab


class S09(SpokenScene):
    def construct(self):
        ax, yl = age_axes()
        pr, ca, orr, cb = predict_row()
        self.play(FadeIn(ax), FadeIn(yl), FadeIn(pr), run_time=0.8)
        y1 = 0.5
        start = Dot([px(0), y1, 0], radius=0.14, color=ORANGE)
        arrow = arr([px(0), y1, 0], [px(13), y1, 0], ORANGE, 8, tip=0.3)
        bl = T("closure begins at birth (lasts 3 months)", 26, ORANGE).move_to([px(6.5), y1 + 0.55, 0])
        self.at("closure from birth")
        self.play(FadeIn(start, scale=2.0), GrowArrow(arrow), FadeIn(bl, shift=DOWN * 0.1), run_time=1.3)
        dl = VGroup(*[DashedLine([px(w), y1 - 0.1, 0], [px(w), PYB, 0], color=GOLD, stroke_width=2.5, dash_length=0.1) for w in range(2, 13, 2)])
        self.at("spanned many ages")
        self.play(FadeIn(dl), run_time=0.8)
        bars = brief_bars()
        tk = brief_ticks()
        self.at("Compare brief")
        self.play(FadeOut(dl), FadeOut(bl), FadeOut(arrow), FadeOut(start), FadeIn(bars[0], scale=0.6), FadeIn(tk[0]), run_time=1.0)
        lab = brief_label()
        self.at("different ages")
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in bars[1:]], lag_ratio=0.3), FadeIn(tk[1:]), FadeIn(lab), run_time=1.4)
        self.at("one switch off point")
        self.play(FadeIn(ca, shift=DOWN * 0.1), run_time=0.5)
        self.at("rise and a fall")
        self.play(FadeIn(orr), FadeIn(cb, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        s09_end(self)
        msg = T("Pause and sketch your guess", 36, GOLD, weight=BOLD).move_to([px(7), 2.0, 0])
        track = Line([px(3.0), 1.62, 0], [px(11.0), 1.62, 0], color=GOLD, stroke_width=7)
        self.add(msg, track)
        self.play(Uncreate(track), run_time=self.narration_s - 0.3, rate_func=linear)
        self.finish()


def plot_static(scene, upto=13.7, onset=True, kit=True, note=False):
    ax, yl = age_axes()
    out = [ax, yl]
    scene.add(ax, yl)
    if kit:
        k = T("kitten", 34, GOLD, weight=BOLD).move_to([-5.5, 3.4, 0])
        scene.add(k)
        out.append(k)
    c = curve(0, upto)
    scene.add(c)
    out.append(c)
    if onset:
        out += onset_marker(scene)
    return out


def onset_marker(scene=None):
    p = np.array([px(3.0), py(sens(3.0)), 0])
    dot = Dot(p, radius=0.12, color=GOLD)
    dl = DashedLine(p, [p[0], PYB, 0], color=GOLD, stroke_width=3, dash_length=0.1)
    lab = T("starts in the 4th week\n(age 3 weeks)", 26, GOLD, line_spacing=0.6).move_to([px(3.0) + 2.4, -1.5, 0])
    lead = Line([p[0] + 0.12, p[1] - 0.12, 0], [lab.get_left()[0] - 0.08, -1.5, 0], color=GOLD, stroke_width=2.5)
    if scene is not None:
        scene.add(dot, dl, lab, lead)
    return [dot, dl, lab, lead]


class S11(SpokenScene):
    def construct(self):
        ax, yl, pr, ca, orr, cb, tk, bars, lab = s09_end(self)
        kit = T("kitten", 34, GOLD, weight=BOLD).move_to([-5.5, 3.4, 0])
        c0 = curve(0, 2.7)
        self.play(FadeOut(VGroup(*bars, tk, lab, pr, ca, orr)), Indicate(cb, color=GOLD, scale_factor=1.12), Create(c0, rate_func=linear), run_time=1.4)
        self.at("kittens")
        self.play(FadeOut(cb), FadeIn(kit, shift=DOWN * 0.1), run_time=0.5)
        note = T("susceptibility = size of the effect of closure", 26, GOLD).move_to([1.0, 3.35, 0])
        self.at("susceptibility")
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.5)
        c1 = curve(2.7, 3.7)
        self.at("began")
        self.play(Create(c1, rate_func=linear), run_time=1.0)
        dot, dl, ml, lead = onset_marker()
        self.at("start of the")
        self.play(FadeIn(dot, scale=1.8), Create(dl), FadeIn(ml), Create(lead), run_time=0.6)
        c2 = curve(3.7, 5.5)
        self.play(Create(c2, rate_func=linear), run_time=0.9)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        plot_static(self, 5.5)
        tag = schem_tag(5.2, 3.4)
        self.add(tag)
        c2 = curve(5.5, 7.0)
        self.at("stayed high")
        self.play(Create(c2, rate_func=linear), run_time=1.2)
        b1 = band(6, 8)
        l1 = T("6 to 8 weeks", 26, GOLD).move_to([px(7), 2.85, 0])
        self.at("six and eight")
        self.play(FadeIn(b1), FadeIn(l1, shift=DOWN * 0.1), run_time=0.6)
        c3 = curve(7.0, 13.7)
        self.at("then it declined")
        self.play(Create(c3, rate_func=linear), run_time=1.4)
        b2 = hatch_band(9, 13)
        l2 = T("month 3", 26, LIGHT).move_to([px(11), 2.85, 0])
        self.at("third")
        self.play(FadeIn(b2), FadeIn(l2, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


def overlap_state(scene, bar_label=True, effect=True):
    """The 1963 closure bar over the curve, shaded where it meets the high weeks (3 to 8)."""
    x0, x1 = px(0), px(13)
    bar = Rectangle(width=x1 - x0, height=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.45).move_to([(x0 + x1) / 2, 2.75, 0])
    hi = Rectangle(width=px(8) - px(3), height=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to([(px(3) + px(8)) / 2, 2.75, 0])
    bl = VGroup(T("birth to month 3", 26, TEXT).move_to([(px(8) + x1) / 2, 2.75, 0]),
                T("closure covers ages 0 to 13 weeks", 26, ORANGE).move_to([(x0 + x1) / 2 - 0.4, 3.4, 0]),
                Line([x0, 2.45, 0], [x0, 3.05, 0], color=ORANGE, stroke_width=5),
                Line([x1, 2.45, 0], [x1, 3.05, 0], color=ORANGE, stroke_width=5))
    shade = Rectangle(width=px(8) - px(3), height=2.75 - 0.25 - PYB, stroke_width=0, fill_color=ORANGE, fill_opacity=0.16)
    shade.move_to([(px(3) + px(8)) / 2, (2.5 + PYB) / 2, 0])
    eff = chip("large effect", GOLD, size=28).move_to([px(5.5), 0.55, 0])
    hw = T("the high weeks", 26, LIGHT).move_to([0.3, -1.4, 0])
    return bar, hi, bl, shade, eff, hw


class S12b(SpokenScene):
    def construct(self):
        marks = plot_static(self, 13.7)[-4:]
        self.add(schem_tag(5.2, 3.4))
        b1, l1 = band(6, 8), T("6 to 8 weeks", 26, GOLD).move_to([px(7), 2.85, 0])
        b2, l2 = hatch_band(9, 13), T("month 3", 26, LIGHT).move_to([px(11), 2.85, 0])
        old = VGroup(b1, l1, b2, l2, *marks)
        self.add(old)
        bar, hi, bl, shade, eff, hw = overlap_state(self)
        self.play(FadeOut(old), run_time=0.3)
        self.at("closure from birth")
        self.play(GrowFromEdge(bar, LEFT), run_time=1.4)
        self.at("three months")
        self.play(FadeIn(bl), run_time=0.5)
        self.at("overlaps those weeks")
        self.play(FadeIn(shade), FadeIn(hi), FadeIn(hw), run_time=0.8)
        self.at("large effect")
        self.play(FadeIn(eff, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S13Beat(NarratedScene):
    def construct(self):
        plot_static(self, 13.7, onset=False)
        self.add(schem_tag(5.2, 3.4))
        bar, hi, bl, shade, eff, hw = overlap_state(self)
        self.add(bar, hi, bl, shade, eff, hw)
        sw = T("overlap with the high weeks\nfits the large effect", 26, GOLD, line_spacing=0.6).move_to([0.3, -1.4, 0])
        self.play(ReplacementTransform(hw, sw), Indicate(eff, color=GOLD, scale_factor=1.12), Indicate(shade, color=ORANGE, scale_factor=1.0), run_time=1.2)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        plot_static(self, 13.7, onset=False)
        self.add(schem_tag(5.2, 3.4))
        bar, hi, bl, shade, eff, hw = overlap_state(self)
        sw = T("overlap with the high weeks\nfits the large effect", 26, GOLD, line_spacing=0.6).move_to([0.3, -1.4, 0])
        old = VGroup(bar, hi, bl, shade, eff, sw)
        self.add(old)
        self.play(FadeOut(old), run_time=0.3)
        pk = Dot([px(5.0), py(sens(5.0)), 0], radius=0.14, color=GOLD)
        pkl = T("peak", 28, GOLD, weight=BOLD).move_to([px(5.0), py(sens(5.0)) - 0.6, 0])
        self.at("the peak")
        self.play(FadeIn(pk, scale=2.0), Flash(pk, color=GOLD, flash_radius=0.6, line_length=0.2), FadeIn(pkl), run_time=0.8)
        eye = make_eye(ORANGE, 1.2).move_to([-3.4, 1.3, 0])
        lab = T("right eye", 28, ORANGE).move_to([-3.4, 0.3, 0])
        self.at("some kittens")
        self.play(FadeIn(eye), FadeIn(lab), run_time=0.5)
        self.at("closed")
        self.play(*eye_close(eye), run_time=0.5)
        st = stitches(eye).move_to(eye[0])
        cnt = T("day 0", 32, GOLD, weight=BOLD).move_to([-3.4, -0.45, 0])
        self.play(FadeIn(st), FadeIn(cnt), run_time=0.2)
        d6 = Rectangle(width=6 / 7 * SX, height=0.36, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).move_to([px(4.55), 2.78, 0])
        dl = T("6 days", 28, GOLD, weight=BOLD).next_to(d6, RIGHT, buff=0.15)
        self.at("six days")
        for n in range(1, 7):
            self.remove(cnt)
            cnt = T(f"day {n}", 32, GOLD, weight=BOLD).move_to([-3.4, -0.45, 0])
            self.add(cnt)
            self.wait(0.16)
        self.play(FadeIn(d6, scale=0.5), FadeIn(dl, shift=DOWN * 0.1), run_time=0.5)
        b = band(3, 5, GOLD, 0.2)
        bl2 = T("4th or 5th week: rising to the peak", 26, GOLD).move_to([px(4.0) + 0.9, 3.4, 0])
        self.at("fourth or fifth week")
        self.play(FadeIn(b), FadeIn(bl2, shift=UP * 0.1), run_time=0.7)
        self.finish()


def s15_final(scene):
    """Group-1 scale with the eye icons and callouts (the end of s15)."""
    h = Hist()
    ax, tags, xt = h.axis(), h.tags(), h.xtitle()
    ea = shut(make_eye(ORANGE, 1.2).move_to([h.hx[0], 0.55, 0]))
    sa = stitches(ea)
    eb = make_eye(BLUE, 1.2).move_to([h.hx[6], 0.55, 0])
    arA = arr([h.hx[0], -0.3, 0], [h.hx[0], -1.35, 0], ORANGE, 7)
    arB = arr([h.hx[6], -0.3, 0], [h.hx[6], -1.35, 0], BLUE, 7)
    ring = Circle(radius=0.36, stroke_color=ORANGE, stroke_width=6).move_to([h.hx[0], h.base - 0.38, 0])
    g1 = T("group 1", 44, ORANGE, weight=BOLD).move_to([h.hx[0], 1.95, 0])
    g7 = T("group 7", 44, BLUE, weight=BOLD).move_to([h.hx[6], 1.95, 0])
    mid = T("recorded:\nleft hemisphere", 30, TEXT, line_spacing=0.6).move_to([0, 0.6, 0])
    return h, ax, tags, xt, ea, sa, eb, arA, arB, ring, g1, g7, mid


class S15(SpokenScene):
    def construct(self):
        brain = Ellipse(width=9.6, height=5.0, stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to([0, 1.2, 0])
        LH = Ellipse(width=4.0, height=4.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([2.1, 1.2, 0])
        RH = Ellipse(width=4.0, height=4.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([-2.1, 1.2, 0])
        rl = T("right\nhemisphere", 28, GREY, line_spacing=0.6).move_to([-2.1, 1.2, 0])
        bt = T("top view", 26, LIGHT).move_to([-5.7, 3.4, 0])
        self.play(FadeIn(brain), FadeIn(LH), FadeIn(RH), FadeIn(rl), FadeIn(bt), run_time=0.5)
        el = VGroup(Line([4.5, 3.6, 0], [2.7, 2.3, 0], stroke_width=7, color=TEXT), Dot([2.7, 2.3, 0], radius=0.12, color=TEXT))
        elab = T("electrode", 26, TEXT).move_to([5.6, 3.2, 0])
        self.play(FadeIn(el, shift=DOWN * 0.3), FadeIn(elab), run_time=0.5)
        ll = T("left\nhemisphere", 28, TEXT, line_spacing=0.6).move_to([2.1, 1.5, 0])
        self.at("left hemisphere")
        self.play(LH.animate.set_stroke(TEXT, 6).set_fill(TEXT, 0.14), FadeIn(ll), run_time=0.7)
        ea = shut(make_eye(ORANGE, 1.1).move_to([-2.0, -2.75, 0]))
        sa = stitches(ea)
        eb = make_eye(BLUE, 1.1).move_to([2.0, -2.75, 0])
        la = T("right eye (closed)", 26, ORANGE).move_to([-2.0, -3.55, 0])
        lb = T("left eye (open)", 26, BLUE).move_to([2.0, -3.55, 0])
        aA = arr([-1.5, -2.2, 0], [1.6, 0.35, 0], ORANGE, 8)
        aB = arr([2.5, -2.2, 0], [2.5, -0.35, 0], BLUE, 6)
        cl = T("contralateral", 26, ORANGE).move_to([-3.4, -1.45, 0])
        il = T("ipsilateral", 26, BLUE).move_to([4.3, -1.45, 0])
        self.at("closed right eye")
        self.play(FadeIn(VGroup(ea, sa, eb, la, lb)), GrowArrow(aA), GrowArrow(aB), FadeIn(cl), FadeIn(il), run_time=1.0)
        self.at("group one")
        stage1 = VGroup(brain, bt, LH, RH, rl, el, elab, ll, ea, sa, eb, la, lb, aA, aB, cl, il)
        h, ax, tags, xt, ea2, sa2, eb2, arA, arB, ring, g1, g7, mid = s15_final(self)
        self.play(FadeOut(stage1), run_time=0.25)
        self.play(FadeIn(VGroup(ax, tags, xt, ea2, sa2, eb2, arA, arB, mid)), run_time=0.4)
        self.play(Create(ring), FadeIn(g1, shift=DOWN * 0.1), FadeIn(g7, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        h, ax, tags, xt, ea, sa, eb, arA, arB, ring, g1, g7, mid = s15_final(self)
        self.add(ax, tags, xt, ea, sa, eb, arA, arB, ring, g1, g7, mid)
        ca, cb, cst = corner_eyes()
        yl = h.ylab()
        bars0 = h.bars([0] * 7)
        self.add(bars0)
        self.play(FadeOut(VGroup(arA, arB, ring, g1, g7, mid)), ReplacementTransform(ea, ca), ReplacementTransform(sa, cst),
                  ReplacementTransform(eb, cb), run_time=0.5)
        self.play(FadeIn(yl), Transform(bars0, h.bars(H_NORMAL)), run_time=0.6)
        bars = bars0
        ghost = h.ghost()
        nl = h.normal_label()
        self.at("could drive")
        self.play(Indicate(VGroup(bars[0], bars[1], bars[2]), color=ORANGE, scale_factor=1.08), run_time=0.5)
        self.at("fell")
        self.add(ghost)
        self.play(Transform(bars, h.bars(H_FALL)), FadeIn(nl), run_time=1.0)
        self.at("fraction of normal")
        self.play(Indicate(VGroup(bars[0], bars[1], bars[2]), color=ORANGE, scale_factor=1.08), run_time=0.6)
        move = CurvedArrow([h.hx[1], 1.75, 0], [h.hx[5] + 0.2, 3.3, 0], angle=-TAU / 6, color=TEXT, stroke_width=7)
        self.at("Most of the histogram")
        self.play(Transform(bars, h.bars(H_SHIFT)), Create(move), run_time=1.5)
        self.at("group 7")
        self.play(Indicate(bars[6], color=BLUE, scale_factor=1.06), run_time=0.8)
        self.at("open eye")
        self.play(Indicate(VGroup(cb, tags[2]), color=BLUE, scale_factor=1.15), FadeOut(move), run_time=0.8)
        self.finish()


def hist_state(scene, hvals):
    h = Hist()
    ca, cb, cst = corner_eyes()
    parts = VGroup(h.frame(), ca, cb, cst, h.bars(hvals), h.ghost(), h.normal_label())
    scene.add(parts)
    return h, parts


class S17(SpokenScene):
    def construct(self):
        h, parts = hist_state(self, H_SHIFT)
        cap = T("6 days of unequal vision", 40, GOLD, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.6)
        self.at("enough")
        self.play(Indicate(cap, color=GOLD, scale_factor=1.08), run_time=0.9)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        f = Face(-3.2, -0.2, 2.8, "macaque")
        lab = T("infant macaque", 30, TEXT).move_to([-3.2, -3.45, 0])
        self.add(f.all)
        self.add(lab)
        an = T("anatomy", 44, GOLD, font=TITLE_FONT).move_to([3.4, 2.7, 0])
        self.at("anatomy")
        self.play(FadeIn(an, shift=DOWN * 0.1), run_time=0.5)
        nm1 = T("Hubel", 46, TEXT).move_to([3.4, 1.5, 0])
        nm2 = T("Wiesel", 46, TEXT).move_to([3.4, 0.5, 0])
        nm3 = T("Simon LeVay", 46, TEXT).move_to([3.4, -0.5, 0])
        yrs = T("1977 and 1980", 32, GOLD).move_to([3.4, -1.55, 0])
        self.at("Hubel")
        self.play(FadeIn(nm1, shift=LEFT * 0.15), run_time=0.4)
        self.at("Wiesel")
        self.play(FadeIn(nm2, shift=LEFT * 0.15), run_time=0.4)
        self.at("Simon")
        self.play(FadeIn(nm3, shift=LEFT * 0.15), FadeIn(yrs, shift=UP * 0.1), run_time=0.5)
        self.at("closed one eye")
        self.play(*f.close_right(), run_time=0.6)
        self.play(FadeIn(f.st), run_time=0.3)
        self.at("infant macaque")
        self.play(Indicate(lab, color=TEXT, scale_factor=1.12), run_time=0.7)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        cx, cy, W, H = 0.0, 0.2, 10.4, 4.0
        f = Face(-3.2, -0.2, 2.8, "macaque", closed=True)
        nm = VGroup(T("Hubel", 46, TEXT).move_to([3.4, 1.5, 0]), T("Wiesel", 46, TEXT).move_to([3.4, 0.5, 0]),
                    T("Simon LeVay", 46, TEXT).move_to([3.4, -0.5, 0]), T("anatomy", 44, GOLD, font=TITLE_FONT).move_to([3.4, 2.7, 0]),
                    T("1977 and 1980", 32, GOLD).move_to([3.4, -1.55, 0]))
        lab0 = T("infant macaque", 30, TEXT).move_to([-3.2, -3.45, 0])
        old = VGroup(f.all, nm, lab0)
        self.add(old)
        eq = stripes(cx, cy, W, H, 0.5)
        sb = stripes_box(cx, cy, W, H)
        hdr = T("layer 4C, seen from above", 30, TEXT).move_to([0, 2.8, 0])
        state = T("normal", 30, TEXT).move_to([5.3, 2.8, 0])
        tag = schem_tag(-5.5, 2.8)
        self.play(FadeOut(old), run_time=0.25)
        self.at("traced the stripes")
        self.play(FadeIn(sb), LaggedStart(*[FadeIn(s) for s in eq], lag_ratio=0.1), FadeIn(state), FadeIn(tag), run_time=0.9)
        self.at("layer 4C")
        self.play(FadeIn(hdr, shift=DOWN * 0.1), run_time=0.5)
        lo, lb = stripe_legend(-3.3, 3.3, -2.55)
        self.play(FadeIn(lo), FadeIn(lb), run_time=0.5)
        self.at("open eyes")
        self.play(Indicate(VGroup(*[eq[i] for i in range(1, 8, 2)]), color=BLUE, scale_factor=1.02), run_time=0.8)
        pw = W / 4
        blue_arrows = VGroup(*[DoubleArrow([cx - W / 2 + pw * k + 0.78 + 0.1, cy + 0.9, 0], [cx - W / 2 + pw * (k + 1) - 0.1, cy + 0.9, 0],
                                            color=TEXT, stroke_width=6, buff=0, tip_length=0.2) for k in (1, 2)])
        state2 = T("after closure", 30, GOLD, weight=BOLD).move_to([5.3, 2.8, 0])
        self.at("widened")
        self.play(Transform(eq, stripes(cx, cy, W, H, 0.3)), ReplacementTransform(state, state2), FadeIn(blue_arrows), run_time=1.1)
        self.at("closed eyes")
        self.play(Indicate(VGroup(*[eq[i] for i in range(0, 8, 2)]), color=ORANGE, scale_factor=1.03), run_time=0.7)
        oa = VGroup()
        for k in (1, 2):
            xa = cx - W / 2 + pw * k
            oa.add(arr([xa - 0.7, cy - 0.9, 0], [xa + 0.05, cy - 0.9, 0], TEXT, 6, tip=0.2))
            oa.add(arr([xa + 0.78 + 0.7, cy - 0.9, 0], [xa + 0.73, cy - 0.9, 0], TEXT, 6, tip=0.2))
        self.at("narrowed")
        self.play(FadeIn(oa), run_time=0.6)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        band4 = Rectangle(width=13.2, height=2.5, stroke_width=0, fill_color=GREY, fill_opacity=0.07).move_to([0, 1.55, 0])
        bord = DashedVMobject(Rectangle(width=13.2, height=2.5, stroke_color=LIGHT, stroke_width=2.5, fill_opacity=0).move_to([0, 1.55, 0]), num_dashes=70)
        l4 = T("layer 4", 28, LIGHT).move_to([0, 1.7, 0])
        kit = T("kitten", 34, GOLD, weight=BOLD).move_to([-5.5, 3.4, 0])
        self.play(FadeIn(band4), FadeIn(bord), FadeIn(l4), FadeIn(kit), run_time=0.5)
        L, D = arbor(-3.4, -2.35, 4.6, 4.9)
        self.play(Create(L[0]), run_time=0.6)
        self.at("single thalamic axons")
        self.play(LaggedStart(*[Create(l) for l in L[1:]], lag_ratio=0.05), run_time=1.5)
        lab = T("thalamic axon, closed eye\nday 0", 26, ORANGE, line_spacing=0.6).move_to([-3.4, -3.3, 0])
        self.at("deprived eye")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.6)
        L2, D2 = arbor(3.4, -2.35, 4.6, 4.9)
        right = VGroup(*L2)
        a = arr([-1.0, -0.3, 0], [1.0, -0.3, 0], GOLD, 7)
        wk = T("same axon,\nabout a week later", 26, GOLD, weight=BOLD, line_spacing=0.6).move_to([3.4, -3.3, 0])
        self.at("were later seen")
        self.play(FadeIn(right), GrowArrow(a), FadeIn(wk, shift=UP * 0.1), run_time=0.5)
        gone = [l for l, d, i in zip(L2, D2, range(len(L2))) if d == 4 or (d == 3 and i % 2 == 0)]
        self.at("lose branches")
        self.play(*[Uncreate(l) for l in gone], run_time=1.1)
        self.at("about a week")
        self.play(Indicate(wk, color=GOLD, scale_factor=1.1), run_time=0.6)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        cx = -3.9
        sb = stripes_box(cx, 0.3, 5.0, 4.6)
        st = stripes(cx, 0.3, 5.0, 4.6, 0.3)
        tl = T("territory (anatomy)", 30, TEXT).move_to([cx, 3.05, 0])
        lo, lb = stripe_legend(-5.3, -2.3, -2.55)
        lo.move_to([-3.9, -2.55, 0])
        lb.move_to([-3.9, -3.1, 0])
        h = Hist(cx=3.7, base=-1.2, sp=0.82, unit=0.28, bw=0.7, compact=True)
        bars = h.bars(H_SHIFT)
        rl = T("response (physiology)", 30, TEXT).move_to([3.7, 3.05, 0])
        sch = schem_tag(0.0, 3.5)
        win = T("sensitive\nweeks", 26, GOLD, line_spacing=0.6).move_to([-0.58, 1.05, 0])
        self.play(FadeIn(VGroup(sb, st, tl, lo, lb)), FadeIn(VGroup(h.frame(), bars, rl)), FadeIn(sch), run_time=0.8)
        self.at("window")
        self.play(FadeIn(win, shift=DOWN * 0.1), run_time=0.5)
        self.at("territory")
        self.play(Indicate(st, color=TEXT, scale_factor=1.02), run_time=0.9)
        tie = DoubleArrow([-1.15, 0.3, 0], [-0.1, 0.3, 0], color=GOLD, stroke_width=7, buff=0, tip_length=0.2)
        self.at("axons hold")
        self.play(Create(tie), run_time=0.6)
        self.at("how cells")
        self.play(Indicate(bars, color=TEXT, scale_factor=1.02), run_time=0.9)
        self.finish()


PB, PU, PSP, PBW = -0.95, 0.2, 0.8, 0.7


def panel(cx, kind):
    word, tag = ("young", "a few days of closure") if kind == "kitten" else ("adult", "months of closure")
    sgn = -1 if cx < 0 else 1
    f = Face(cx + sgn * 2.15, 2.6, 0.65, kind, closed=True, simple=True)
    lab = T(word, 36, TEXT, weight=BOLD).move_to([cx - sgn * 0.8, 3.0, 0])
    chp = chip(tag, GOLD, size=26).move_to([cx - sgn * 0.8, 2.15, 0])
    h = Hist(cx=cx, base=PB, sp=PSP, unit=PU, bw=PBW, compact=True)
    return f, lab, chp, h


class S22(SpokenScene):
    def construct(self):
        yf, yl, yc, yh = panel(-3.4, "kitten")
        af, al, ac, ah = panel(3.4, "cat")
        take = T("Takeaway", 30, GOLD, weight=BOLD).move_to([0, 3.5, 0])
        yb = yh.bars(H_NORMAL)
        ab = ah.bars(H_NORMAL)
        self.play(FadeIn(take), FadeIn(yh.frame()), FadeIn(ah.frame()), run_time=0.5)
        self.at("in the young")
        self.play(FadeIn(yf.all), FadeIn(yl), FadeIn(yb), run_time=0.7)
        self.at("few days")
        self.play(FadeIn(yc, shift=UP * 0.1), run_time=0.5)
        self.at("move the balance")
        self.play(Transform(yb, yh.bars(H_SHIFT)), run_time=1.0)
        self.at("the adult")
        self.play(FadeIn(af.all), FadeIn(al), FadeIn(ab), run_time=0.6)
        self.at("months")
        self.play(FadeIn(ac, shift=UP * 0.1), run_time=0.5)
        self.at("do not")
        self.play(Indicate(ab, color=PURPLE, scale_factor=1.04), run_time=0.9)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        # two option cards, shown together
        cardL = RoundedRectangle(corner_radius=0.3, width=5.8, height=6.4, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.05).move_to([-3.5, 0.0, 0])
        cardR = RoundedRectangle(corner_radius=0.3, width=5.8, height=6.4, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.05).move_to([3.5, 0.0, 0])
        eo = shut(make_eye(ORANGE, 1.4).move_to([-3.4, 2.0, 0]))
        es = stitches(eo)
        eb = make_eye(BLUE, 1.4).move_to([3.4, 2.0, 0])
        lo = T("closed eye", 28, ORANGE).move_to([-3.4, 1.05, 0])
        lb = T("other eye", 28, BLUE).move_to([3.4, 1.05, 0])
        cellsL = VGroup(*[Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
                          .move_to([-3.4 + (i - 1) * 1.2, -0.45, 0]) for i in range(3)])
        cellsR = VGroup(*[Circle(radius=0.38, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5)
                          .move_to([3.4 + (i - 1) * 1.2, -0.45, 0]) for i in range(3)])
        arrR = arr([3.4, 0.6, 0], [3.4, 0.0, 0], BLUE, 10)
        cap = T("cortical cells", 26, LIGHT)
        capL = cap.copy().move_to([-3.4, -1.2, 0])
        capR = cap.copy().move_to([3.4, -1.2, 0])
        q = T("?", 90, GOLD, weight=BOLD).move_to([0, 0.2, 0])
        self.play(FadeIn(VGroup(cardL, cardR)), FadeIn(VGroup(eo, es, eb, lo, lb, cellsL, cellsR, capL, capR, arrR)), run_time=0.5)
        self.at("question")
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.at("closed eye")
        self.play(cardL.animate.set_stroke(ORANGE, 5), Indicate(VGroup(eo, es), color=ORANGE, scale_factor=1.15), run_time=0.8)
        c1 = chip("unused?", GREY, size=50).move_to([-3.4, -2.2, 0])
        c1[1].set_color(LIGHT)
        self.at("unused")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        c2 = chip("out-competed?", BLUE, size=50).move_to([3.4, -2.2, 0])
        self.at("other eye")
        self.play(cardR.animate.set_stroke(BLUE, 5), Indicate(eb, color=BLUE, scale_factor=1.15), FadeIn(c2, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S24End(EndCard):
    LINE = "A few days of unequal vision, early in life,\nshift the balance; months in an adult do not."

    def construct(self):
        line = T(self.LINE, 40, TEXT, font=TITLE_FONT, line_spacing=1.0)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", 24, TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
