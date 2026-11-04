"""Ocular dominance, chapter 6: The Window and the Patch  (Biochemistrypedia chaptered explainer)

COLOR MAP (one colour per concept, shared by every chapter; the lesson's convention is that the left
hemisphere is recorded, so the right eye is contralateral and the left eye ipsilateral)
  ORANGE = the right (contralateral) eye, group 1 of the histogram; here it is the closed eye in the animals
           and the GOOD eye in the child
  BLUE   = the left (ipsilateral) eye, group 7; here it is the open eye in the animals and the WEAK eye in the child
  PURPLE = a cortical cell that both eyes can drive
  RED    = anything crossed out
  GOLD   = the window (sensitive or critical period), credits, "predict" and schematic tags
  GREY   = outlines and neutral things
Histogram bars run from orange (group 1) through purple (group 4) to blue (group 7).
"""
import numpy as np

ORANGE = "#F2994A"
PURPLE = "#B58CD9"
from bp_style import *  # noqa: F401,F403

DARK = "#2a2f3a"

# ------------------------------------------------------------------ helpers
def arr(a, b, color=GREY, w=6, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=24)


def make_eye(color=ORANGE, scale=1.0, state="open"):
    """VGroup(outline, pupil, glint, stitches). state: open or sutured (closed, stitched)."""
    w = 2.0 * scale
    ell = Ellipse(width=w, height=1.1 * scale, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15)
    pup = Circle(radius=0.3 * scale, stroke_width=0, fill_color=color, fill_opacity=1)
    glint = Circle(radius=0.08 * scale, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pup.get_center() + UR * 0.1 * scale)
    st = VGroup(*[Line([x * scale, -0.36 * scale, 0], [x * scale, 0.36 * scale, 0], stroke_width=4.5, color=color)
                  for x in (-0.7, -0.35, 0, 0.35, 0.7)])
    st.set_opacity(0)
    g = VGroup(ell, pup, glint, st)
    if state == "sutured":
        ell.stretch_to_fit_height(w * 0.17)
        ell.set_fill(color, 0.3)
        pup.set_opacity(0)
        glint.set_opacity(0)
        st.set_opacity(1)
    return g


def sew(g):
    return [g[0].animate.stretch_to_fit_height(g[0].width * 0.17).set_fill(g[0].get_color(), 0.3), g[1].animate.set_opacity(0),
            g[2].animate.set_opacity(0), g[3].animate.set_opacity(1)]


def turn_in(g, scale, toward):
    """Static: move the pupil and glint sideways (toward = +1 or -1) so the eye looks turned."""
    g[1].shift(RIGHT * toward * 0.62 * scale)
    g[2].shift(RIGHT * toward * 0.62 * scale)
    return g


def turn_anim(g, scale, toward):
    return [g[1].animate.shift(RIGHT * toward * 0.62 * scale), g[2].animate.shift(RIGHT * toward * 0.62 * scale)]


def make_cat(cx, cy, s=1.0, kitten=False):
    """A front-facing cat head. Returns (group, right_eye, left_eye). The cat's right eye is on our left."""
    es = 0.4 if kitten else 0.34
    head = Circle(radius=1.0 * s, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)
    ears = VGroup(*[Polygon([sx * 0.92 * s, 0.35 * s, 0], [sx * 0.82 * s, 1.3 * s, 0], [sx * 0.18 * s, 0.9 * s, 0],
                            stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2) for sx in (-1, 1)])
    eR = make_eye(ORANGE, es * s, "open").move_to([-0.48 * s, 0.18 * s, 0])
    eL = make_eye(BLUE, es * s, "open").move_to([0.48 * s, 0.18 * s, 0])
    nose = Polygon([-0.1 * s, -0.22 * s, 0], [0.1 * s, -0.22 * s, 0], [0, -0.36 * s, 0], stroke_width=0, fill_color=GREY, fill_opacity=1)
    mouth = VGroup(Line([0, -0.36 * s, 0], [0, -0.5 * s, 0], color=GREY, stroke_width=3),
                   Arc(radius=0.17 * s, start_angle=PI, angle=PI, color=GREY, stroke_width=3).rotate(PI).move_to([-0.17 * s, -0.5 * s, 0]),
                   Arc(radius=0.17 * s, start_angle=PI, angle=PI, color=GREY, stroke_width=3).rotate(PI).move_to([0.17 * s, -0.5 * s, 0]))
    wh = VGroup(*[Line([sx * 0.55 * s, (-0.3 - 0.07 * k) * s, 0], [sx * 1.4 * s, (-0.38 - 0.2 * k + 0.12) * s, 0], color=GREY, stroke_width=2.5)
                  for sx in (-1, 1) for k in (-1, 0, 1)])
    g = VGroup(ears, head, wh, nose, mouth, eR, eL).move_to([cx, cy, 0])
    return g, eR, eL


# histograms -----------------------------------------------------------------------------------
HX = [(i - 3) * 1.5 for i in range(7)]
BASE = -2.0
H_NORMAL = [3, 6, 10, 12, 9, 5, 2]
H_SHIFT = [0.5, 1, 2, 3, 6, 10, 13]          # closing the right (orange) eye moves cells toward the blue group
H_LOST = [13, 10, 6, 3, 2, 1, 0.5]           # the weak (blue) eye has lost the cortex
H_REGAIN = [7, 10, 11, 9, 6, 3.5, 2]         # the weak eye's bars regrow


def gcol(i):
    A, P, B = ManimColor(ORANGE), ManimColor(PURPLE), ManimColor(BLUE)
    return interpolate_color(A, P, i / 3) if i <= 3 else interpolate_color(P, B, (i - 3) / 3)


def hbars(h, hx=HX, base=BASE, unit=0.3, bw=1.2):
    out = VGroup()
    for i, v in enumerate(h):
        hh = max(v * unit, 0.03)
        out.add(Rectangle(width=bw, height=hh, stroke_color=gcol(i), stroke_width=2, fill_color=gcol(i),
                          fill_opacity=0.6).move_to([hx[i], base + hh / 2, 0]))
    return out


def hnums(hx=HX, base=BASE, size=26, dy=0.4):
    return VGroup(*[T(str(i + 1), size, TEXT).move_to([hx[i], base - dy, 0]) for i in range(7)])


def hline(hx=HX, base=BASE, pad=0.9):
    return Line([hx[0] - pad, base, 0], [hx[-1] + pad, base, 0], color=GREY, stroke_width=3)


def hist_frame(hx=HX, base=BASE, size=26, dy=0.4, pad=0.9, ta="right eye", tb="left eye", tsize=24, tdy=1.05):
    ax = hline(hx, base, pad)
    nums = hnums(hx, base, size, dy)
    l1 = T(ta, tsize, ORANGE).move_to([hx[0], base - tdy, 0])
    l7 = T(tb, tsize, BLUE).move_to([hx[6], base - tdy, 0])
    return VGroup(ax, nums, l1, l7)


def corner_eyes(closed_right=True, y=3.35, x=6.0):
    a = make_eye(ORANGE, 0.5, "sutured" if closed_right else "open").move_to([-x, y, 0])
    b = make_eye(BLUE, 0.5).move_to([x, y, 0])
    return a, b


# faces ----------------------------------------------------------------------------------------
class Face:
    """A child's face. eR (orange, the good eye) is on our left, eL (blue, the weak eye) on our right."""

    def __init__(self, cx, cy, r=2.5):
        k = r / 2.2
        self.cx, self.cy, self.r, self.k = cx, cy, r, k
        self.es = 0.55 * k
        self.head = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.10).move_to([cx, cy, 0])
        self.hair = Arc(radius=r + 0.05, start_angle=PI * 0.08, angle=PI * 0.84, color=GREY, stroke_width=14, arc_center=[cx, cy, 0])
        ey = cy + 0.35 * k
        self.ey = ey
        self.eR = make_eye(ORANGE, self.es).move_to([cx - 0.98 * k, ey, 0])
        self.eL = make_eye(BLUE, self.es).move_to([cx + 0.98 * k, ey, 0])
        self.nose = Line([cx, cy - 0.05 * k, 0], [cx - 0.1 * k, cy - 0.5 * k, 0], color=GREY, stroke_width=4)
        self.nose2 = Line([cx - 0.1 * k, cy - 0.5 * k, 0], [cx + 0.1 * k, cy - 0.5 * k, 0], color=GREY, stroke_width=4)
        self.mouth = Arc(radius=0.55 * k, start_angle=PI * 1.2, angle=PI * 0.6, color=GREY, stroke_width=4, arc_center=[cx, cy - 0.6 * k, 0])
        gr = 0.72 * k
        self.glasses = VGroup(Circle(radius=gr, stroke_color=TEXT, stroke_width=4).move_to([cx - 0.98 * k, ey, 0]),
                              Circle(radius=gr, stroke_color=TEXT, stroke_width=4).move_to([cx + 0.98 * k, ey, 0]),
                              Line([cx - 0.98 * k + gr, ey + 0.1, 0], [cx + 0.98 * k - gr, ey + 0.1, 0], color=TEXT, stroke_width=4))
        self.base = VGroup(self.hair, self.head, self.nose, self.nose2, self.mouth, self.eR, self.eL)

    def eye_pos(self, which):
        return np.array([self.cx + (0.98 if which == "L" else -0.98) * self.k, self.ey, 0])


def patch_shape(w=1.5, h=1.15):
    return VGroup(RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=GREY, stroke_width=4,
                                   fill_color=DARK, fill_opacity=1),
                  Line([-w * 0.25, -h * 0.25, 0], [w * 0.25, h * 0.25, 0], color=GREY, stroke_width=3),
                  Line([-w * 0.25, h * 0.25, 0], [w * 0.25, -h * 0.25, 0], color=GREY, stroke_width=3))


# the eye-to-brain diagram (s16 and s22) ----------------------------------------------------
EYE_O = np.array([-4.8, 1.6, 0])
EYE_B = np.array([-4.8, -1.6, 0])
BRAIN_C = np.array([2.7, 0.1, 0])


def brain_parts():
    box = RoundedRectangle(corner_radius=0.3, width=5.6, height=5.0, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.05).move_to(BRAIN_C)
    cells = VGroup(*[Circle(radius=0.38, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35)
                     .move_to(BRAIN_C + np.array([-1.7 + 1.13 * c, 1.45 - 1.45 * r, 0])) for r in range(3) for c in range(4)])
    cap = T("young brain", 28, GREY).move_to([BRAIN_C[0], BRAIN_C[1] + 3.05, 0])
    sc = T("cells shared by both eyes", 26, PURPLE).move_to([BRAIN_C[0], BRAIN_C[1] - 2.95, 0])
    return box, cells, cap, sc


def wire(color, y0, y1, w):
    return arr([-3.55, y0, 0], [-0.35, y1, 0], color, w, tip=0.3)


class SceneAudit:
    pass


# ------------------------------------------------------------------ audit (set KX_AUDIT=1; writes scratch/audit.log)
def _audit(scene):
    import os
    from pathlib import Path
    out = []
    texts = []

    def walk(m):
        if isinstance(m, Text):
            if m.get_fill_opacity() > 0.05:
                texts.append(m)
        else:
            for s in m.submobjects:
                walk(s)
    for m in scene.mobjects:
        walk(m)
        b = [m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1]]
        if b[0] < -6.85 or b[1] > 6.85 or b[2] < -3.85 or b[3] > 3.85:
            out.append(f"OFF-FRAME {type(m).__name__} {['%.2f' % v for v in b]}")
    for i, a in enumerate(texts):
        for c in texts[i + 1:]:
            dx = min(a.get_right()[0], c.get_right()[0]) - max(a.get_left()[0], c.get_left()[0])
            dy = min(a.get_top()[1], c.get_top()[1]) - max(a.get_bottom()[1], c.get_bottom()[1])
            if dx > 0.02 and dy > 0.02:
                out.append(f"TEXT-OVERLAP {a.text!r} / {c.text!r}")
    sid = os.environ.get("KX_SCENE_ID")
    p = Path(os.environ["KX_SCRIPT"]).parent / "scratch"
    p.mkdir(exist_ok=True)
    with open(p / "audit.log", "a") as f:
        f.write(f"{sid}: {'ok' if not out else '; '.join(out)}\n")


class Sc(SpokenScene):
    def finish(self):
        import os
        if os.environ.get("KX_AUDIT"):
            _audit(self)
        super().finish()


# ================================================================== s00 title
class S00Title(TitleCard):
    LESSON = "Ocular dominance and the critical period"
    TITLE = "The Window and the Patch"


# ================================================================== big histogram (s07, s24)
BH_HX = [(i - 3) * 1.5 for i in range(7)]
BH_BASE = -2.2
BH_UNIT = 0.32
BH_BW = 1.28
H_PART = [9.5, 10, 7.5, 4.5, 3, 1.6, 1.0]     # partial recovery: still skewed, but less


def bigbars(h):
    return hbars(h, hx=BH_HX, base=BH_BASE, unit=BH_UNIT, bw=BH_BW)


def big_hist_frame(ta="right eye", tb="left eye"):
    fr = hist_frame(hx=BH_HX, base=BH_BASE, size=26, dy=0.4, pad=0.9, ta=ta, tb=tb, tsize=26, tdy=1.05)
    yl = T("number of cells", 26, GREY).rotate(PI / 2).move_to([-6.1, BH_BASE + 2.2, 0])
    yax = Line([-5.45, BH_BASE, 0], [-5.45, BH_BASE + 4.8, 0], color=GREY, stroke_width=3)
    return VGroup(fr, yl, yax)


def ghost_bars(h):
    out = VGroup()
    for r in bigbars(h):
        out.add(DashedVMobject(Rectangle(width=r.width, height=r.height).move_to(r.get_center()), num_dashes=22).set_stroke(GREY, 3))
    return out


# ================================================================== s01 the question
CAT_K = (-3.4, 1.9)
CAT_A = (3.6, 1.9)
MH_X = [(i - 3) * 0.78 for i in range(7)]
MH_BASE = -2.6
MH_UNIT = 0.17


def mini_parts(cx, heights):
    hx = [x + cx for x in MH_X]
    bars = hbars(heights, hx=hx, base=MH_BASE, unit=MH_UNIT, bw=0.66)
    fr = hist_frame(hx=hx, base=MH_BASE, size=26, dy=0.38, pad=0.5, tsize=26, tdy=0.82)
    return bars, fr


class S01(Sc):
    def construct(self):
        kc, kR, kL = make_cat(*CAT_K, s=1.05, kitten=True)
        ac, aR, aL = make_cat(*CAT_A, s=1.05)
        kname = T("kitten", 32).move_to([CAT_K[0], 3.55, 0])
        aname = T("adult cat", 32).move_to([CAT_A[0], 3.55, 0])
        kb, kf = mini_parts(CAT_K[0], H_NORMAL)
        ab, af = mini_parts(CAT_A[0], H_NORMAL)
        ky = T("number of cells", 26, GREY).rotate(PI / 2).move_to([CAT_K[0] - 3.1, -1.35, 0])
        ay = T("number of cells", 26, GREY).rotate(PI / 2).move_to([CAT_A[0] - 3.1, -1.35, 0])
        rec = T("left hemisphere recorded", 26, GREY).move_to([0.1, 3.55, 0])
        self.add(kc, kname, kf, kb, ky, ac, aname, af, ab, ay, rec)
        self.at("a week")
        wk = chip("one week", GOLD, size=26).move_to([CAT_K[0], 0.3, 0])
        self.play(*sew(kR), FadeIn(wk, shift=UP * 0.1), run_time=0.6)
        self.at("rewire")
        self.play(Transform(kb, hbars(H_SHIFT, hx=[x + CAT_K[0] for x in MH_X], base=MH_BASE, unit=MH_UNIT, bw=0.66)), run_time=1.3)
        self.at("while months")
        mo = chip("months", GOLD, size=26).move_to([CAT_A[0], 0.3, 0])
        self.play(*sew(aR), FadeIn(mo, shift=UP * 0.1), run_time=0.6)
        self.at("nothing visible")
        self.play(Indicate(ab, color=PURPLE, scale_factor=1.04), run_time=0.9)
        self.finish()


# ================================================================== s02 to s05 the two nested boxes
OUT_W, OUT_H, OUT_Y = 11.8, 6.8, 0.0
IN_W, IN_H, IN_Y = 9.0, 3.4, -0.75


def outer_box(fill=0.0, color=GREY):
    return RoundedRectangle(corner_radius=0.3, width=OUT_W, height=OUT_H, stroke_color=color, stroke_width=4,
                            fill_color=GOLD, fill_opacity=fill).move_to([0, OUT_Y, 0])


def inner_box(fill=0.0, color=GREY):
    return RoundedRectangle(corner_radius=0.25, width=IN_W, height=IN_H, stroke_color=color, stroke_width=4,
                            fill_color=GOLD, fill_opacity=fill).move_to([0, IN_Y, 0])


def slot(y, filled=False):
    r = RoundedRectangle(corner_radius=0.15, width=8.2, height=0.78, stroke_color=GOLD if filled else GREY, stroke_width=3,
                         fill_color=GOLD, fill_opacity=0.16 if filled else 0.0).move_to([0, y, 0])
    return r


SLOT_Y = (IN_Y + IN_H / 2 - 1.35, IN_Y + IN_H / 2 - 2.25)


def s_title_texts():
    t1 = T("sensitive period", 42, GOLD).move_to([0, 2.8, 0])
    t2 = T("experience has an unusually strong effect", 30, TEXT).move_to([0, 2.1, 0])
    return t1, t2


def s_inner_texts():
    ti = T("critical period", 38, GOLD).move_to([0, IN_Y + IN_H / 2 - 0.5, 0])
    cred = T("Eric Knudsen's definition", 26, GOLD).move_to([0, -2.95, 0])
    return ti, cred


def s_slot_texts():
    a = T("essential for normal development", 30, TEXT).move_to([0, SLOT_Y[0], 0])
    b = T("effects last", 30, TEXT).move_to([0, SLOT_Y[1], 0])
    return a, b


class S02(Sc):
    def construct(self):
        kc, kR, kL = make_cat(-4.1, 0.35, s=1.5, kitten=True)
        ac, aR, aL = make_cat(4.0, 0.35, s=1.9)
        ax = arr([-1.7, 0.35, 0], [1.2, 0.35, 0], GREY, 8)
        lab = T("age", 60, TEXT).move_to([-0.25, 1.35, 0])
        young = T("young", 40, GREY).move_to([-4.1, -2.55, 0])
        old = T("adult", 40, GREY).move_to([4.0, -2.55, 0])
        self.add(kc, young, ac, old)
        self.play(Create(ax), run_time=0.8)
        self.at("depends on age")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        ob = outer_box()
        ib = inner_box()
        self.at("Two terms")
        self.play(FadeOut(VGroup(ax, lab, kc, ac, young, old)), Create(ob), run_time=0.6)
        self.at("help")
        self.play(Create(ib), run_time=0.6)
        self.finish()


class S03(Sc):
    def construct(self):
        ob, ib = outer_box(), inner_box()
        self.add(ob, ib)
        t1, t2 = s_title_texts()
        self.at("A sensitive period")
        self.play(ob.animate.set_stroke(GOLD).set_fill(GOLD, 0.12), FadeIn(t1, shift=DOWN * 0.1), run_time=0.8)
        self.at("unusually strong effect")
        self.play(FadeIn(t2, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


def nested_base():
    ob = outer_box(0.12, GOLD)
    ib = inner_box()
    t1, t2 = s_title_texts()
    return ob, ib, t1, t2


class S04(Sc):
    def construct(self):
        ob, ib, t1, t2 = nested_base()
        self.add(ob, ib, t1, t2)
        ti, cred = s_inner_texts()
        s1, s2 = slot(SLOT_Y[0]), slot(SLOT_Y[1])
        self.at("A critical period")
        self.play(ib.animate.set_stroke(GOLD).set_fill(GOLD, 0.2), FadeIn(ti, shift=DOWN * 0.1), run_time=0.8)
        self.at("Knudsen's definition")
        self.play(FadeIn(cred, shift=UP * 0.1), run_time=0.6)
        self.at("two extra features")
        self.play(FadeIn(s1), run_time=0.5)
        self.play(FadeIn(s2), run_time=0.5)
        self.finish()


class S05(Sc):
    def construct(self):
        ob, ib, t1, t2 = nested_base()
        ib.set_stroke(GOLD).set_fill(GOLD, 0.2)
        ti, cred = s_inner_texts()
        s1, s2 = slot(SLOT_Y[0]), slot(SLOT_Y[1])
        self.add(ob, ib, t1, t2, ti, cred, s1, s2)
        a, b = s_slot_texts()
        self.at("essential for")
        self.play(s1.animate.set_stroke(GOLD).set_fill(GOLD, 0.16), FadeIn(a), run_time=0.7)
        self.at("effects last")
        self.play(s2.animate.set_stroke(GOLD).set_fill(GOLD, 0.16), FadeIn(b), run_time=0.7)
        self.finish()


# ================================================================== s06 the window is a spectrum, three things that change it
def mini_plot(cx, kind, y0=-2.45, w=1.9, h=2.3, lo=0.3, hi=0.7, mu=0.5, sd=0.19, peak=0.85):
    """A small plot (L-shaped axes) of a window: 'sharp' (box with vertical edges from lo to hi) or 'gradual' (smooth hump at mu)."""
    xl, xr = cx - w / 2, cx + w / 2
    ax = VGroup(Line([xl, y0, 0], [xr, y0, 0], color=GREY, stroke_width=3), Line([xl, y0, 0], [xl, y0 + h, 0], color=GREY, stroke_width=3))
    if kind == "sharp":
        pts = [[xl, y0 + 0.05, 0], [xl + lo * w, y0 + 0.05, 0], [xl + lo * w, y0 + h * peak, 0], [xl + hi * w, y0 + h * peak, 0],
               [xl + hi * w, y0 + 0.05, 0], [xr, y0 + 0.05, 0]]
        cu = VMobject(color=GOLD, stroke_width=6).set_points_as_corners(pts)
    else:
        ts = np.linspace(0, 1, 60)
        cu = VMobject(color=GOLD, stroke_width=6).set_points_smoothly(
            [np.array([xl + t * w, y0 + 0.05 + h * peak * np.exp(-((t - mu) / sd) ** 2 / 2), 0]) for t in ts])
    return VGroup(ax, cu)


# one card per thing that changes how sharp a window looks: (name, detail, sharp shape, gradual shape)
S06_CARDS = [
    ("species", "cat vs mouse", dict(lo=0.3, hi=0.7), dict(mu=0.5, sd=0.19)),
    ("manipulation", "how long the\nclosure lasts", dict(lo=0.15, hi=0.45, peak=0.7), dict(mu=0.5, sd=0.26, peak=0.6)),
    ("measure", "histogram shift vs\nanother readout", dict(lo=0.4, hi=0.6, peak=0.9), dict(mu=0.35, sd=0.14, peak=0.9)),
]
S06_CX = (-4.6, 0.0, 4.6)


class S06(Sc):
    def construct(self):
        ob, ib, t1, t2 = nested_base()
        ib.set_stroke(GOLD).set_fill(GOLD, 0.2)
        ti, cred = s_inner_texts()
        s1, s2 = slot(SLOT_Y[0], True), slot(SLOT_Y[1], True)
        a, b = s_slot_texts()
        self.add(ob, ib, t1, t2, ti, cred, s1, s2, a, b)
        ra = 2.95
        ca = chip("sensitive period", GOLD, size=30).move_to([-4.1, ra, 0])
        cb = chip("critical period", GOLD, size=30).move_to([4.1, ra, 0])
        link = DoubleArrow([-2.3, ra, 0], [2.3, ra, 0], buff=0, color=GREY, stroke_width=7, tip_length=0.3)
        dot = Dot([0, ra, 0], radius=0.24, color=GOLD)
        dl = T("most real windows", 26, GOLD).move_to([0, ra - 0.7, 0])
        # the arrow is at the top from the first frame; the two boxes shrink below it as the picture of the two terms
        boxes = VGroup(ob, ib)
        self.play(FadeOut(VGroup(t1, t2, ti, cred, s1, s2, a, b)),
                  boxes.animate.scale(0.62).move_to([0, -0.55, 0]),
                  FadeIn(ca), FadeIn(cb), GrowFromCenter(link), run_time=0.7)
        self.at("between the two")
        mid = VGroup(dot, dl)
        self.play(FadeIn(mid, scale=1.6), run_time=0.4)
        self.play(mid.animate.shift(LEFT * 0.9), run_time=0.3)
        self.play(mid.animate.shift(RIGHT * 1.6), run_time=0.35)
        self.play(mid.animate.shift(LEFT * 0.7), run_time=0.3)
        # three empty cards, then each is filled as the narrator names it
        cards = []
        for cx in S06_CX:
            cards.append(RoundedRectangle(corner_radius=0.2, width=4.3, height=5.0, stroke_color=GREY, stroke_width=2.5,
                                          fill_color=GREY, fill_opacity=0.06).move_to([cx, -0.95, 0]))
        sch = T("schematic", 26, GOLD).move_to([6.0, -3.65, 0])

        def fill_card(k):
            name, detail, sh, gr = S06_CARDS[k]
            cx = S06_CX[k]
            tt = VGroup(T(name, 34, TEXT), T(detail, 26, GOLD, line_spacing=0.8)).arrange(DOWN, buff=0.12).move_to([cx, 0.85, 0])
            pa, pb = mini_plot(cx - 1.0, "sharp", y0=-2.35, h=2.0, w=1.8, **sh), mini_plot(cx + 1.0, "gradual", y0=-2.35, h=2.0, w=1.8, **gr)
            la = T("sharp", 26, GREY).move_to([cx - 1.0, -2.85, 0])
            lb = T("gradual", 26, GREY).move_to([cx + 1.0, -2.85, 0])
            return tt, pa, pb, la, lb
        self.at("How sharp")
        pieces = [fill_card(k) for k in range(3)]
        self.play(FadeOut(boxes), *[FadeIn(c) for c in cards], FadeIn(sch), run_time=0.5)
        # the first pair is drawn straight away (the sentence is about sharpness); its tag arrives with "species"
        self.play(Create(pieces[0][1][0]), Create(pieces[0][1][1]), Create(pieces[0][2][0]), Create(pieces[0][2][1]),
                  FadeIn(pieces[0][3]), FadeIn(pieces[0][4]), run_time=0.7)
        for k, cue in enumerate(["species", "manipulation", "measure"]):
            self.at(cue)
            tt, pa, pb, la, lb = pieces[k]
            if k == 0:
                self.play(FadeIn(tt, shift=DOWN * 0.1), run_time=0.4)
            else:
                self.play(FadeIn(tt, shift=DOWN * 0.1), Create(pa[0]), Create(pa[1]), Create(pb[0]), Create(pb[1]),
                          FadeIn(la), FadeIn(lb), run_time=0.7)
        self.finish()


# ================================================================== s07 the adult histogram
class S07(Sc):
    def construct(self):
        ca, cb = corner_eyes(closed_right=False)
        fr = big_hist_frame()
        rec = T("recorded: left hemisphere", 26, GREY).move_to([0, -3.3, 0])
        lab = T("adult cat, months of closure: histogram unchanged", 32).move_to([0, 3.45, 0])
        bars = bigbars(H_NORMAL)
        self.add(ca, cb, fr, lab, rec, bars)
        ghost = ghost_bars(H_SHIFT)
        gl = T("dashed: a kitten after one week", 26, TEXT).move_to([4.0, 2.45, 0])
        self.at("may not move")
        self.play(*sew(ca), FadeIn(ghost), FadeIn(gl), run_time=0.7)
        note = T("not the same as no change of any kind", 30, GOLD).move_to([-2.0, 2.8, 0])
        ol = VGroup(*[T(x, 24, TEXT) for x in ("synapses, spines,", "other measures:", "not shown here")]).arrange(DOWN, buff=0.12)
        other = VGroup(RoundedRectangle(corner_radius=0.14, width=ol.width + 0.5, height=ol.height + 0.5, stroke_color=TEXT, stroke_width=2.5,
                                        fill_color=TEXT, fill_opacity=0.12), ol).move_to([-3.8, 1.55, 0])
        self.at("does not mean")
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(other, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ================================================================== s08 to s12 the species timelines
RX0, RL = -3.0, 8.8          # row axis start and length
ROW_Y = (2.2, -0.2, -2.6)
ROW_DEFS = [
    # name, unit, ticks (fraction, label), band (t0, t1, soft_end)
    ("kitten", "weeks", [(w / 14, str(w)) for w in (0, 4, 8, 12)], (3 / 14, 13 / 14, None)),
    ("macaque", "weeks after\nbirth", [(w / 12, str(w)) for w in (0, 4, 8, 12)], (0.0, 0.2, 0.36)),
    ("mouse", "postnatal day", [(d / 120, str(d)) for d in (0, 40, 80, 120)], (20 / 120, 40 / 120, None)),
]


def rx(t):
    return RX0 + RL * t


def row_band(i, op=0.26):
    t0, t1, soft = ROW_DEFS[i][3]
    yb = ROW_Y[i]
    g = VGroup(Rectangle(width=rx(t1) - rx(t0), height=1.25, stroke_width=0, fill_color=GOLD, fill_opacity=op).move_to(
        [(rx(t0) + rx(t1)) / 2, yb + 0.65, 0]))
    if soft:
        n = 6
        for k in range(n):
            a, b = t1 + (soft - t1) * k / n, t1 + (soft - t1) * (k + 1) / n
            g.add(Rectangle(width=rx(b) - rx(a), height=1.25, stroke_width=0, fill_color=GOLD, fill_opacity=op * (1 - (k + 0.5) / n)).move_to(
                [(rx(a) + rx(b)) / 2, yb + 0.65, 0]))
    return g


def row_parts(i):
    name, unit, ticks, band = ROW_DEFS[i]
    yb = ROW_Y[i]
    lab = T(name, 40).move_to([-5.0, yb + 0.95, 0])
    un = T(unit, 26, GREY, line_spacing=0.8).move_to([-5.0, yb + 0.15, 0])
    axis = arr([RX0, yb, 0], [RX0 + RL + 0.4, yb, 0], GREY, 6, tip=0.22)
    tk = VGroup(*[Line([rx(t), yb - 0.1, 0], [rx(t), yb + 0.1, 0], color=GREY, stroke_width=3) for t, _ in ticks])
    nums = VGroup(*[T(s, 26, TEXT).move_to([rx(t), yb - 0.42, 0]) for t, s in ticks])
    return VGroup(lab, un), VGroup(axis, tk, nums)


class S08(Sc):
    def construct(self):
        rows = [row_parts(i) for i in range(3)]
        sch = T("schematic", 26, GOLD).move_to([5.9, 3.5, 0])
        self.add(rows[0][0], rows[0][1], sch)
        for k, cue in enumerate(["Name the", "species", "every number"]):
            if k == 0:
                continue
            self.at(cue)
            self.play(FadeIn(rows[k][0], shift=RIGHT * 0.1), FadeIn(rows[k][1]), run_time=0.3)
        self.at("window differs")
        self.play(*[GrowFromEdge(row_band(k), LEFT) for k in range(3)], run_time=0.9)
        self.finish()


# big single plot ---------------------------------------------------------------------------
BX0, BX1, BYB, BYT = -5.2, 5.9, -2.6, 2.8


def bx(t):
    return BX0 + (BX1 - BX0) * t


def by(v):
    return BYB + (BYT - BYB) * v


def y_axis():
    axy = arr([BX0, BYB, 0], [BX0, BYT + 0.25, 0], GREY, 5, tip=0.2)
    yl = T("susceptibility to closure", 26, GREY).rotate(PI / 2).move_to([-6.35, 0.1, 0])
    return VGroup(axy, yl)


def x_axis(xlabel, ticks, labelled):
    """ticks: fractions along x for small tick marks; labelled: (fraction, text) pairs."""
    axx = arr([BX0, BYB, 0], [BX1 + 0.3, BYB, 0], GREY, 5, tip=0.2)
    tk = VGroup(*[Line([bx(t), BYB - 0.1, 0], [bx(t), BYB + 0.1, 0], color=GREY, stroke_width=3) for t in ticks])
    lb = VGroup(*[T(s, 26, TEXT).move_to([bx(t), BYB - 0.45, 0]) for t, s in labelled])
    xl = T(xlabel, 26, GREY).move_to([(BX0 + BX1) / 2, BYB - 0.98, 0])
    return VGroup(axx, tk, lb, xl)


def curve(f, t0, t1, n=80, color=GOLD, w=7):
    ts = np.linspace(t0, t1, n)
    return VMobject(color=color, stroke_width=w).set_points_smoothly([np.array([bx(t), by(f(t)), 0]) for t in ts])


def vmark(t, color=GOLD, top=None):
    return DashedLine([bx(t), BYB, 0], [bx(t), BYT if top is None else top, 0], color=color, stroke_width=3, dash_length=0.12)


def vband(t0, t1, op=0.2, color=GOLD):
    return Rectangle(width=bx(t1) - bx(t0), height=BYT - BYB, stroke_width=0, fill_color=color, fill_opacity=op).move_to(
        [(bx(t0) + bx(t1)) / 2, (BYT + BYB) / 2, 0])


def soft_vband(t0, t1, t2, op=0.22):
    g = VGroup(vband(t0, t1, op))
    n = 6
    for k in range(n):
        a, b = t1 + (t2 - t1) * k / n, t1 + (t2 - t1) * (k + 1) / n
        g.add(vband(a, b, op * (1 - (k + 0.5) / n)))
    return g


def logi(z):
    return 1 / (1 + np.exp(-z))


def f_kitten(t):
    w = 14 * t
    return logi((w - 3.8) / 0.22) * (1 - 0.9 * logi((w - 10.3) / 1.0))


def f_mac(t):
    return 0.1 + 0.9 * np.exp(-0.5 * (max(0.0, t - 0.1) / 0.27) ** 2)


def f_mouse(t):
    d = 120 * t
    return 0.06 + 0.94 * np.exp(-((d - 28) / 9.0) ** 2 / 2.0)


def kit_x():
    return x_axis("age (weeks)", [w / 14 for w in range(0, 15)], [(w / 14, str(w)) for w in (0, 4, 8, 12)])


def mac_x():
    return x_axis("age after birth (weeks)", [i / 12 for i in range(0, 13)], [(i / 12, str(i)) for i in (0, 4, 8, 12)])


def mouse_x():
    return x_axis("postnatal day", [d / 120 for d in range(0, 121, 10)], [(d / 120, str(d)) for d in (0, 40, 80, 120)])


def schem_tag(y=3.45, text="schematic"):
    t = T(text, 26, GOLD)
    return t.move_to([6.7 - t.width / 2, y, 0])


class S09(Sc):
    def construct(self):
        klab = T("kitten", 46).move_to([-4.2, 1.8, 0])
        ya, xa = y_axis(), kit_x()
        tag = schem_tag()
        self.add(ya, xa, klab, tag)
        s1 = curve(f_kitten, 0, 5 / 14)
        s2 = curve(f_kitten, 5 / 14, 8.4 / 14)
        s3 = curve(f_kitten, 8.4 / 14, 1.0)
        m3 = vmark(3 / 14)
        l3 = T("start of week 4", 26, GOLD).move_to([bx(3 / 14), 3.3, 0])
        b68 = vband(6 / 14, 8 / 14)
        l68 = T("6 to 8 weeks", 26, GOLD).move_to([bx(7 / 14), 3.3, 0])
        b3m = vband(9 / 14, 13 / 14, 0.14)
        l3m = T("third month", 26, GOLD).move_to([bx(11 / 14), 3.3, 0])
        self.at("begins around")
        self.play(Create(s1), run_time=1.1)
        self.at("fourth week")
        self.play(Create(m3), FadeIn(l3, shift=DOWN * 0.1), run_time=0.6)
        self.at("stays high")
        self.play(Create(s2), run_time=1.0)
        self.at("six to eight weeks")
        self.play(FadeIn(b68), FadeIn(l68, shift=DOWN * 0.1), run_time=0.7)
        self.at("declines")
        self.play(Create(s3), run_time=1.1)
        self.at("third month")
        self.play(FadeIn(b3m), FadeIn(l3m, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


def kitten_full():
    ya, xa = y_axis(), kit_x()
    klab = T("kitten", 46).move_to([-4.2, 1.8, 0])
    c = curve(f_kitten, 0, 1.0)
    m3 = vmark(3 / 14)
    l3 = T("start of week 4", 26, GOLD).move_to([bx(3 / 14), 3.3, 0])
    b68 = vband(6 / 14, 8 / 14)
    l68 = T("6 to 8 weeks", 26, GOLD).move_to([bx(7 / 14), 3.3, 0])
    b3m = vband(9 / 14, 13 / 14, 0.14)
    l3m = T("third month", 26, GOLD).move_to([bx(11 / 14), 3.3, 0])
    return ya, xa, klab, c, VGroup(m3, l3, b68, l68, b3m, l3m)


class S10(Sc):
    def construct(self):
        ya = y_axis()
        tag = schem_tag()
        mlab = T("macaque", 46).move_to([4.2, 1.8, 0])
        xa2 = mac_x()
        self.add(ya, tag, xa2, mlab)
        cm = curve(f_mac, 0, 1.0)
        self.at("strongest effect")
        self.play(Create(cm), run_time=1.2)
        band = soft_vband(0, 0.2, 0.36)
        lab = T("first weeks after birth", 26, GOLD).move_to([bx(0.02) + 2.2, 3.3, 0])
        self.at("first weeks")
        self.play(FadeIn(band), FadeIn(lab, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


def mouse_static(with_peak=True):
    lab = T("mouse", 46).move_to([4.2, 1.8, 0])
    cred = T("Gordon and Stryker, 1996", 26, GOLD)
    cred.move_to([6.7 - cred.width / 2, 3.55, 0])
    tag = schem_tag(3.1)
    return lab, cred, tag


class S11(Sc):
    def construct(self):
        ya = y_axis()
        lab, cred, tag3 = mouse_static()
        xa3 = mouse_x()
        self.add(ya, xa3, lab, tag3)
        self.at("Joshua Gordon")
        self.play(FadeIn(cred, shift=DOWN * 0.1), run_time=0.5)
        cu = curve(f_mouse, 0, 1.0, n=160)
        self.at("strongest shifts")
        self.play(Create(cu), run_time=1.5)
        mk = vmark(28 / 120)
        pl = T("peak near day 28", 26, GOLD).move_to([bx(28 / 120) + 1.75, 3.3, 0])
        self.at("day 28")
        self.play(Create(mk), FadeIn(pl, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S12(Sc):
    def construct(self):
        ya, xa3 = y_axis(), mouse_x()
        lab, cred, tag3 = mouse_static()
        cu = curve(f_mouse, 0, 1.0, n=160)
        mk = vmark(28 / 120)
        pl = T("peak near day 28", 26, GOLD).move_to([bx(28 / 120) + 1.75, 3.3, 0])
        self.add(ya, xa3, lab, cred, tag3, cu, mk, pl)
        px = bx(28 / 120)
        few = VGroup(Line([px - 0.55, 3.15, 0], [px + 0.55, 3.15, 0], color=TEXT, stroke_width=6),
                     Line([px - 0.55, 3.0, 0], [px - 0.55, 3.3, 0], color=TEXT, stroke_width=6),
                     Line([px + 0.55, 3.0, 0], [px + 0.55, 3.3, 0], color=TEXT, stroke_width=6))
        fl = T("a few days of closure", 26, TEXT).move_to([px + 0.75 + 1.8, 3.15, 0])
        self.at("same few days")
        self.play(FadeOut(pl), FadeOut(mk), run_time=0.2)
        self.play(FadeIn(few), FadeIn(fl), run_time=0.3)
        ax_x = bx(90 / 120)
        band = vband(60 / 120, 1.0, 0.14, GREY)
        al = T("adult mice", 34, TEXT).move_to([ax_x, 0.9, 0])
        few2 = few.copy().move_to([ax_x, -0.7, 0])
        fl2 = fl.copy().move_to([ax_x, -0.15, 0])
        self.at("adult mice")
        # the bracket and its text clear before the adult panel slides in, then reappear inside it
        self.play(FadeOut(few), FadeOut(fl), run_time=0.2)
        self.play(FadeIn(band), FadeIn(al, shift=DOWN * 0.1), FadeIn(few2), FadeIn(fl2), run_time=0.6)
        self.at("did little")
        flat = curve(f_mouse, 60 / 120, 1.0, n=30, color=GOLD, w=11)
        little = T("little effect", 26, TEXT).move_to([ax_x, -1.55, 0])
        self.play(Create(flat), FadeIn(little), run_time=0.7)
        self.finish()


# ================================================================== s13 mouse cortex
class S13(Sc):
    def construct(self):
        cx, cy = -2.4, 0.1
        cortex = Ellipse(width=7.4, height=5.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.06).move_to([cx, cy, 0])
        zc = np.array([cx + 1.0, cy - 0.3, 0])
        zone = Ellipse(width=3.4, height=2.3, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.08).move_to(zc)
        rng = np.random.RandomState(4)
        dots = VGroup()
        while len(dots) < 24:
            p = rng.uniform(-1, 1, 2)
            if p[0] ** 2 + p[1] ** 2 > 0.8:
                continue
            col = ORANGE if len(dots) % 2 == 0 else BLUE
            dots.add(Circle(radius=0.14, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(zc + np.array([p[0] * 1.4, p[1] * 0.95, 0])))
        zl = T("binocular zone", 30, PURPLE).move_to([zc[0], zc[1] + 1.6, 0])
        cn = T("mouse cortex", 28, GREY).move_to([cx - 2.15, cy + 0.65, 0])
        self.add(cortex, cn, zone, dots, zl)
        # the stripes mice do not have
        sc_ = np.array([4.2, 1.1, 0])
        sw = VGroup(*[Rectangle(width=0.34, height=2.8, stroke_width=0, fill_color=(ORANGE if k % 2 == 0 else BLUE), fill_opacity=0.75)
                      .move_to([sc_[0] + (k - 3) * 0.34, sc_[1], 0]) for k in range(7)])
        cross = VGroup(Line([sc_[0] - 1.5, sc_[1] - 1.7, 0], [sc_[0] + 1.5, sc_[1] + 1.7, 0], color=RED, stroke_width=9),
                       Line([sc_[0] - 1.5, sc_[1] + 1.7, 0], [sc_[0] + 1.5, sc_[1] - 1.7, 0], color=RED, stroke_width=9))
        scol = T("ocular dominance columns", 28, GREY).move_to([sc_[0], -1.05, 0])
        self.at("no ocular")
        self.play(FadeIn(sw), FadeIn(scol), run_time=0.6)
        self.play(Create(cross), run_time=0.5)
        # genetics, then the window it is used to ask about
        gc = chip("genetics", TEXT, size=44).move_to([4.2, 1.4, 0])
        self.at("genetics")
        self.play(FadeOut(VGroup(sw, cross, scol)), run_time=0.3)
        self.play(FadeIn(gc, scale=0.8), run_time=0.5)
        wcx, wcy = 4.2, -1.75
        self.at("what opens")
        wa = arr([4.2, 0.75, 0], [4.2, -0.1, 0], GOLD, 6, tip=0.25)
        win = window(wcx, wcy, 2.6, 0.0)
        self.play(GrowArrow(wa), FadeIn(win), run_time=0.6)
        q = T("?", 80, GOLD).move_to([6.2, wcy, 0])
        self.play(Transform(win, window(wcx, wcy, 2.6, 0.8)), FadeIn(q), run_time=0.9)
        self.finish()


# ================================================================== s14 to s15 amblyopia
def view_frame(cx, cy, color, blurred):
    fr = RoundedRectangle(corner_radius=0.2, width=3.8, height=1.9, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.05).move_to([cx, cy, 0])

    def pic(op, dx=0.0, dy=0.0, w=4):
        sun = Circle(radius=0.28, stroke_color=TEXT, stroke_width=w, fill_opacity=0).move_to([cx - 0.9 + dx, cy + 0.4 + dy, 0])
        hill = Polygon([cx - 1.6 + dx, cy - 0.7 + dy, 0], [cx - 0.3 + dx, cy + 0.15 + dy, 0], [cx + 0.9 + dx, cy - 0.7 + dy, 0],
                       stroke_color=TEXT, stroke_width=w, fill_opacity=0)
        hill2 = Polygon([cx + 0.1 + dx, cy - 0.7 + dy, 0], [cx + 0.9 + dx, cy - 0.1 + dy, 0], [cx + 1.6 + dx, cy - 0.7 + dy, 0],
                        stroke_color=TEXT, stroke_width=w, fill_opacity=0)
        g = VGroup(sun, hill, hill2)
        g.set_stroke(opacity=op)
        return g

    if not blurred:
        g = VGroup(fr, pic(1.0))
    else:
        copies = VGroup(*[pic(0.2, dx, dy, 9) for dx, dy in [(-0.12, 0), (0.12, 0), (0, -0.1), (0, 0.1), (0.08, 0.08), (-0.08, -0.08), (0, 0)]])
        g = VGroup(fr, copies)
    return g.scale(1.25).move_to([cx, cy, 0])


JITTER = [(-0.14, 0), (0.14, 0), (0, -0.1), (0, 0.1), (0.1, 0.08), (-0.1, -0.08), (0, 0)]


def blurred_eye(color, scale, center):
    out = VGroup()
    for dx, dy in JITTER:
        e = make_eye(color, scale).move_to(np.array(center) + np.array([dx * scale, dy * scale, 0]))
        e[0].set_stroke(color, 6, opacity=0.25)
        e[0].set_fill(color, 0.05)
        e[1].set_fill(color, 0.25)
        e[2].set_opacity(0)
        out.add(e)
    return out


class S14(Sc):
    def construct(self):
        f = Face(-3.5, -0.25, 2.8)
        title = T("amblyopia", 46).move_to([-3.5, 3.4, 0])
        self.add(f.base)
        self.at("Amblyopia")
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.5)
        vr = view_frame(3.9, 1.95, ORANGE, False)
        lr = T("right eye's view: sharp", 26, ORANGE).move_to([3.9, 0.5, 0])
        vl = view_frame(3.9, -0.95, BLUE, True)
        ll = T("left eye's view: blurred", 26, BLUE).move_to([3.9, -2.55, 0])
        weak = T("left eye: the weak eye", 26, BLUE).move_to([f.eye_pos("L")[0], -3.45, 0])
        self.at("reduced vision")
        self.play(FadeIn(vr), FadeIn(lr), run_time=0.5)
        self.at("usually in one eye")
        self.play(FadeIn(vl), FadeIn(ll), FadeIn(weak, shift=UP * 0.1), Indicate(f.eL, color=BLUE, scale_factor=1.3), run_time=0.9)
        self.at("glasses do not")
        self.play(FadeIn(f.glasses), run_time=0.6)
        self.play(Indicate(f.glasses, color=TEXT, scale_factor=1.05), run_time=0.9)
        self.finish()


class S15(Sc):
    def construct(self):
        # the weak eye, seen from the side, structurally intact
        c = np.array([-0.5, -0.25, 0])
        R = 2.3
        ball = Circle(radius=R, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.10).move_to(c)
        lens = Ellipse(width=0.8, height=1.85, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to(c + LEFT * 1.15)
        cornea = Arc(radius=R, start_angle=PI * 0.88, angle=PI * 0.24, color=BLUE, stroke_width=12, arc_center=c)
        retina = Arc(radius=R - 0.2, start_angle=-PI * 0.38, angle=PI * 0.76, color=BLUE, stroke_width=12, arc_center=c)
        nerve = RoundedRectangle(corner_radius=0.12, width=1.5, height=0.65, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to(c + RIGHT * (R + 0.55))
        eye = VGroup(ball, lens, cornea, retina, nerve)
        ok = T("the weak eye: structure looks healthy", 34, TEXT).move_to([0, -3.35, 0])
        self.add(eye, ok)
        dis = chip("structural disease", RED, size=34).move_to([-1.0, 3.1, 0])
        no = VGroup(Circle(radius=0.42, stroke_color=RED, stroke_width=7),
                    Line([-0.3, -0.3, 0], [0.3, 0.3, 0], color=RED, stroke_width=7)).move_to([dis.get_right()[0] + 0.75, 3.1, 0])
        self.at("No structural disease")
        self.play(FadeIn(dis, shift=LEFT * 0.1), run_time=0.4)
        self.play(Create(no), run_time=0.4)
        self.at("of the eye")
        self.play(Indicate(eye, color=BLUE, scale_factor=1.03), run_time=0.9)
        self.finish()


# ================================================================== s16 unequal input
def brain_diagram(equal=False, patch=False):
    eo = make_eye(ORANGE, 1.2).move_to(EYE_O)
    eb = make_eye(BLUE, 1.2).move_to(EYE_B)
    lo = T("good eye", 28, ORANGE).move_to(EYE_O + UP * 1.0)
    lb = T("weak eye", 28, BLUE).move_to(EYE_B + DOWN * 1.0)
    box, cells, cap, sc = brain_parts()
    return eo, eb, lo, lb, box, cells, cap, sc


class S16(Sc):
    def construct(self):
        eo, eb, lo, lb, box, cells, cap, sc = brain_diagram()
        self.add(eo, eb, lo, lb, box, cells, cap, sc)
        wo, wb = wire(ORANGE, 1.6, 0.6, 9), wire(BLUE, -1.6, -0.6, 9)
        self.at("give the")
        self.play(GrowArrow(wo), GrowArrow(wb), run_time=0.6)
        self.at("unequal input")
        self.play(Transform(wo, wire(ORANGE, 1.6, 0.6, 24)), Transform(wb, wire(BLUE, -1.6, -0.6, 3)), run_time=1.0)
        self.finish()


# ================================================================== s17 and s18 causes
CARD_X = [-4.5, 0.0, 4.5]
CARD_W, CARD_H, CARD_Y = 4.1, 6.0, 0.0


def card(cx, label):
    r = RoundedRectangle(corner_radius=0.25, width=CARD_W, height=CARD_H, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to([cx, CARD_Y, 0])
    t = T(label, 30, TEXT).move_to([cx, CARD_Y - 2.55, 0])
    return r, t


def icon_strab(cx, cy, s=0.8):
    a = make_eye(ORANGE, s).move_to([cx - 0.5 * s * 2.2, cy, 0])
    b = turn_in(make_eye(BLUE, s).move_to([cx + 0.5 * s * 2.2, cy, 0]), s, -1)
    return VGroup(a, b)


def lens_poly(cx, cy, H, th, color):
    ys = np.linspace(-H / 2, H / 2, 24)
    right = [[cx + th * (1 - (2 * y / H) ** 2), cy + y, 0] for y in ys]
    left = [[cx - th * (1 - (2 * y / H) ** 2), cy + y, 0] for y in ys[::-1]]
    return Polygon(*right, *left, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3)


def lens_row(cx, cy, th, f, color, name):
    H = 1.3
    lens = lens_poly(cx, cy, H, th, color)
    rays = VGroup(*[VMobject(color=color, stroke_width=3).set_points_as_corners(
        [[cx - 1.1, cy + yy, 0], [cx, cy + yy, 0], [cx + f, cy, 0]]) for yy in (-0.42, 0.0, 0.42)])
    focus = Dot([cx + f, cy, 0], radius=0.09, color=TEXT)
    lab = T(name, 26, color).move_to([cx + 0.3, cy + 0.98, 0])
    return VGroup(rays, lens, focus, lab)


def icon_lenses(cx, cy):
    return VGroup(lens_row(cx - 0.8, cy + 1.2, 0.2, 2.2, ORANGE, "weak lens"), lens_row(cx - 0.8, cy - 0.65, 0.45, 1.0, BLUE, "strong lens"))


def icon_blocked(cx, cy, s=1.4):
    e = make_eye(BLUE, s).move_to([cx, cy, 0])
    cloud = Ellipse(width=0.95 * s, height=0.8 * s, stroke_width=0, fill_color=TEXT, fill_opacity=0.75).move_to(e[1].get_center())
    a, b = e[0].width / 2, e[0].height / 2
    pts = [[cx + a * np.cos(th), cy + b * np.sin(th), 0] for th in np.linspace(0.12, PI - 0.12, 30)]
    lid = Polygon(*pts, stroke_color=BLUE, stroke_width=4, fill_color=DARK, fill_opacity=1)
    return VGroup(e, cloud, lid)


def cause_set():
    cards = [card(CARD_X[0], "strabismus"), card(CARD_X[1], "different focus"), card(CARD_X[2], "blocked image")]
    icons = [icon_strab(CARD_X[0], 0.4, 0.8), icon_lenses(CARD_X[1], 0.4), icon_blocked(CARD_X[2], 0.4)]
    return cards, icons


class S17(Sc):
    def construct(self):
        cards, icons = cause_set()
        for k in range(3):
            cards[k][0].set_stroke(opacity=0.35)
            self.add(cards[k][0])
        ca = ["strabismus", "difference in focus", "blocks one eye's image"]
        for k in range(3):
            self.at(ca[k])
            self.play(cards[k][0].animate.set_stroke(GREY, opacity=1.0), FadeIn(icons[k], scale=0.9), FadeIn(cards[k][1], shift=UP * 0.1), run_time=0.8)
        self.finish()


class S18(Sc):
    def construct(self):
        cards, icons = cause_set()
        old = VGroup(*[c[0] for c in cards], *[c[1] for c in cards], *icons)
        self.add(old)
        big = icon_strab(-3.3, 0.9, 1.45)
        bl = T("strabismus", 46, TEXT).move_to([-3.3, -1.2, 0])
        grid = VGroup(*[Circle(radius=0.15, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([3.8 + 0.5 * (c - 4.5), 2.45 - 0.5 * r, 0])
                        for r in range(10) for c in range(10)])
        gl = T("a few percent of children", 32, TEXT).move_to([3.8, -2.85, 0])
        gl2 = T("each dot is a child (schematic)", 26, GREY).move_to([3.8, -3.4, 0])
        self.play(FadeOut(old), FadeIn(big), FadeIn(bl), FadeIn(grid), run_time=0.6)
        self.at("a few percent")
        mark = [23, 57, 81]
        self.play(*[grid[i].animate.set_fill(GOLD, 1).scale(1.9) for i in mark], FadeIn(gl, shift=UP * 0.1), FadeIn(gl2), run_time=0.9)
        self.finish()


# ================================================================== s19 and s20 predict
FACE_C = (-3.4, -0.1)
FACE_R = 2.8


def s19_final():
    f = Face(FACE_C[0], FACE_C[1], FACE_R)
    turn_in(f.eL, f.es, -1)
    pred = chip("Predict", GOLD, size=36).move_to([FACE_C[0], 3.35, 0])
    lr = T("right eye", 26, ORANGE).move_to([f.eye_pos("R")[0], -3.45, 0])
    ll = T("left eye", 26, BLUE).move_to([f.eye_pos("L")[0], -3.45, 0])
    q = VGroup(T("Which eye", 66, TEXT, font=TITLE_FONT), T("do you patch?", 66, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.4).move_to([3.4, 0.3, 0])
    return f, pred, lr, ll, q


class S19(Sc):
    def construct(self):
        # build centred, then slide left when the question arrives
        f = Face(0.0, FACE_C[1], FACE_R)
        pred = chip("Predict", GOLD, size=36).move_to([0, 3.35, 0])
        ll = T("left eye", 26, BLUE).move_to([f.eye_pos("L")[0], -3.45, 0])
        lr_final = T("right eye", 26, ORANGE).move_to([f.eye_pos("R")[0] + FACE_C[0], -3.45, 0])
        q = VGroup(T("Which eye", 66, TEXT, font=TITLE_FONT), T("do you patch?", 66, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.4).move_to([3.4, 0.3, 0])
        self.add(pred, f.base)
        self.at("child's left")
        self.play(FadeIn(ll, shift=UP * 0.1), Indicate(f.eL, color=BLUE, scale_factor=1.3), run_time=0.8)
        self.at("sees poorly")
        self.play(*turn_anim(f.eL, f.es, -1), run_time=0.8)
        self.at("Glasses")
        self.play(FadeIn(f.glasses), run_time=0.7)
        self.at("Which eye")
        mover = VGroup(f.base, f.glasses, ll, pred)
        self.play(mover.animate.shift(RIGHT * FACE_C[0]), FadeIn(lr_final, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(q[0], shift=DOWN * 0.1), run_time=0.5)
        self.play(FadeIn(q[1], shift=DOWN * 0.1), run_time=0.5)
        self.finish()


class S20Pause(NarratedScene):
    def construct(self):
        f, pred, lr, ll, q = s19_final()
        self.add(f.base, f.glasses, pred, lr, ll, q)
        self.finish()


# ================================================================== s21 to s23 the patch
class S21(Sc):
    def construct(self):
        f = Face(FACE_C[0], FACE_C[1], FACE_R)
        turn_in(f.eL, f.es, -1)
        self.add(f.base, f.glasses)
        pe = f.eye_pos("R")
        good = T("the good eye", 32, ORANGE).move_to([-5.45, 3.3, 0])
        ga = arr([-5.1, 2.9, 0], [pe[0] - 0.05, pe[1] + 0.55, 0], ORANGE, 5, tip=0.24)
        self.play(FadeIn(good, shift=DOWN * 0.1), GrowArrow(ga), Indicate(f.eR, color=ORANGE, scale_factor=1.3), run_time=0.8)
        patch = patch_shape(1.9, 1.5).move_to(pe)
        pl = T("patch: part of the day", 30, TEXT).move_to([FACE_C[0], -3.5, 0])
        self.at("A patch covers")
        self.play(FadeIn(patch, scale=1.5), FadeIn(pl, shift=UP * 0.1), run_time=0.7)
        # the alternative, side by side: atropine drops blur the good eye
        card_ = RoundedRectangle(corner_radius=0.25, width=5.6, height=6.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to([3.9, 0.0, 0])
        al = T("atropine drops", 36, TEXT).move_to([3.9, 2.6, 0])
        eo = make_eye(ORANGE, 2.2).move_to([3.9, -0.2, 0])
        self.at("atropine drops")
        self.play(FadeIn(card_), FadeIn(eo), FadeIn(al, shift=UP * 0.1), run_time=0.5)
        drops = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to([3.9 + dx, 2.05, 0]) for dx in (-0.55, 0.0, 0.55)])
        self.play(*[d.animate.move_to([d.get_center()[0], 0.9, 0]).set_opacity(0.0) for d in drops], FadeIn(drops, run_time=0.1), run_time=0.7)
        bl = T("blurred", 40, ORANGE).move_to([3.9, -2.35, 0])
        self.at("blur it")
        self.play(FadeOut(eo), FadeIn(blurred_eye(ORANGE, 2.2, [3.9, -0.2, 0])), FadeIn(bl, shift=UP * 0.1), run_time=0.8)
        self.finish()


def s22_parts(orange_w, blue_w):
    eo, eb, lo, lb, box, cells, cap, sc = brain_diagram()
    patch = patch_shape(2.4, 1.5).move_to(EYE_O)
    lo.become(T("good eye, patched", 28, ORANGE).move_to(EYE_O + UP * 1.15))
    return eo, eb, lo, lb, box, cells, cap, sc, patch, wire(ORANGE, 1.6, 0.6, orange_w), wire(BLUE, -1.6, -0.6, blue_w)


def faint_orange():
    return DashedLine([-3.55, 1.6, 0], [-0.35, 0.6, 0], color=ORANGE, stroke_width=4, dash_length=0.2).set_stroke(opacity=0.4)


def pulse_cells(scene, cells, n, each):
    for _ in range(n):
        scene.play(cells.animate.set_fill(BLUE, 0.85).set_stroke(BLUE), run_time=each)
        scene.play(cells.animate.set_fill(PURPLE, 0.35).set_stroke(PURPLE), run_time=each)


class S22(Sc):
    def construct(self):
        eo, eb, lo, lb, box, cells, cap, sc, patch, wo, wb = s22_parts(24, 3)
        self.add(eo, eb, lo, lb, box, cells, cap, sc, wo, wb, patch)
        self.at("Then")
        self.play(FadeOut(wo), FadeIn(faint_orange()), run_time=0.4)
        self.at("weak eye carries")
        self.play(Transform(wb, wire(BLUE, -1.6, -0.6, 24)), cells.animate.set_fill(BLUE, 0.85).set_stroke(BLUE), run_time=1.0)
        self.play(cells.animate.set_fill(PURPLE, 0.35).set_stroke(PURPLE), run_time=0.4)
        self.finish()


class S23Beat(NarratedScene):
    def construct(self):
        eo, eb, lo, lb, box, cells, cap, sc, patch, wo, wb = s22_parts(3, 24)
        self.add(eo, eb, lo, lb, box, cells, cap, sc, faint_orange(), wb, patch)
        pulse_cells(self, cells, 2, 0.5)
        self.finish()


# ================================================================== s24 the contest tilts
class S24(Sc):
    def construct(self):
        ca, cb = corner_eyes(closed_right=False)
        fr = big_hist_frame(tb="left eye (weak)")
        rule = T("the cell keeps the eye that helps it fire", 30, GOLD).move_to([0, 3.55, 0])
        bars = bigbars(H_LOST)
        ill = T("illustrative counts", 28, GREY).move_to([4.9, 2.7, 0])
        patch = patch_shape(1.1, 0.75).move_to(ca)
        tag = chip("before patching", GOLD, size=28).move_to([-0.3, 2.75, 0])
        self.add(ca, patch, cb, fr, bars, ill, rule, tag)
        self.at("weak eye")
        self.play(Indicate(cb, color=BLUE, scale_factor=1.4), Indicate(VGroup(bars[5], bars[6]), color=BLUE, scale_factor=1.15), run_time=0.9)
        self.at("shared cells")
        self.play(Indicate(VGroup(bars[2], bars[3], bars[4]), color=PURPLE, scale_factor=1.05), run_time=0.9)
        tag2 = chip("after weeks of patching", GOLD, size=28).move_to([-0.3, 2.75, 0])
        self.at("contest tilts")
        self.play(FadeOut(tag), run_time=0.25)
        self.play(Transform(bars, bigbars(H_PART)), FadeIn(tag2), run_time=1.1)
        vary = chip("how far varies", GOLD, size=30).move_to([3.7, 1.0, 0])
        self.play(FadeIn(vary, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ================================================================== s25 thin, present, thickening
class S25(Sc):
    def construct(self):
        cc = np.array([3.3, 0.0, 0])
        R = 2.6
        cell = Circle(radius=R, stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.25).move_to(cc)
        cl = T("cortical cell", 32, PURPLE).move_to(cc)
        junction = np.array([-2.5, 0.0, 0])
        angs = [138, 160, 200, 222]
        ends = [cc + R * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) for a in angs]

        def branch(end, w, color=BLUE):
            c_ = CubicBezier(junction, junction + np.array([1.5, 0, 0]), end + np.array([-1.5, 0, 0]), end)
            c_.set_stroke(color, w)
            return c_

        weye = make_eye(BLUE, 0.6).move_to([-5.9, 0, 0])
        trunk = Line([-5.25, 0, 0], junction, color=BLUE, stroke_width=5)
        tl = T("weak eye's input", 28, BLUE).move_to([-3.9, 0.55, 0])
        brs = VGroup(*[branch(ends[i], 3) for i in range(4)])
        bouts = VGroup(*[Circle(radius=0.15, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to(ends[i]) for i in range(4)])
        # the lost branch stays gone: a short grey stub with a cut end, there from the start
        sd = np.array([0.55, -0.8, 0])
        sp = np.array([0.8, 0.55, 0]) * 0.2
        stub = VGroup(Line(junction, junction + sd, color=GREY, stroke_width=6),
                      Line(junction + sd - sp, junction + sd + sp, color=GREY, stroke_width=6))
        lostl = T("one connection lost", 28, GREY).move_to([-2.9, -1.55, 0])
        self.add(cell, cl, weye, trunk, tl, stub)
        self.at("keeps pathways")
        self.play(*[Create(b) for b in brs], run_time=0.8)
        self.play(FadeIn(bouts, scale=0.5), run_time=0.4)
        self.at("strengthened")
        self.play(*[b.animate.set_stroke(BLUE, 9) for b in brs], trunk.animate.set_stroke(BLUE, 12),
                  *[o.animate.scale(1.7) for o in bouts], run_time=1.5)
        self.at("connections were lost")
        self.play(Indicate(stub, color=GREY, scale_factor=1.15), FadeIn(lostl, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ================================================================== s26 treatment by age
class S26(Sc):
    def construct(self):
        yb = -2.4
        axis = Line([-5.0, yb, 0], [5.4, yb, 0], color=GREY, stroke_width=4)
        yax = arr([-5.0, yb, 0], [-5.0, 3.0, 0], GREY, 5, tip=0.2)
        yl = T("improvement in vision", 26, GREY).rotate(PI / 2).move_to([-5.85, 0.3, 0])
        sch = chip("schematic:\nnot to scale", GOLD, size=26).move_to([5.2, 1.5, 0])
        xs = (-1.9, 2.6)

        def bar(x, h, op=0.55):
            return Rectangle(width=2.6, height=max(h, 0.03), stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.4).move_to([x, yb + max(h, 0.03) / 2, 0])
        t1 = T("young children", 30, TEXT).move_to([xs[0], -2.9, 0])
        t2 = T("older children", 30, TEXT).move_to([xs[1], -2.9, 0])
        xl = T("age at start of treatment", 26, GREY).move_to([0.2, -3.5, 0])
        b1, b2 = bar(xs[0], 4.8), bar(xs[1], 2.6)
        g1, g2 = bar(xs[0], 0), bar(xs[1], 0)
        self.add(axis, yax, yl, sch, xl, g1)
        # the young bar rises as the narrator starts ("Treatment generally works best in young children")
        self.play(Transform(g1, b1), run_time=1.6)
        self.at("young children")
        self.play(FadeIn(t1), run_time=0.4)
        chip_ = chip("consistent with a sensitive period", GOLD, size=26).move_to([-1.2, 3.35, 0])
        self.at("sensitive period")
        self.play(FadeIn(chip_, shift=DOWN * 0.1), run_time=0.6)
        self.at("older children")
        self.add(g2)
        self.play(FadeIn(t2), Transform(g2, b2), run_time=1.0)
        self.at("still improve")
        self.play(Indicate(g2, color=GOLD, scale_factor=1.05), run_time=0.9)
        self.finish()


# ================================================================== s27 cataract
class S27(Sc):
    def construct(self):
        eye = make_eye(BLUE, 3.4).move_to([0, 1.15, 0])
        cloud = Ellipse(width=2.9, height=2.1, stroke_width=0, fill_color=TEXT, fill_opacity=0.8).move_to(eye[1].get_center())
        cl = T("cataract: a clouded lens", 32, TEXT).move_to([0, 3.5, 0])
        cl2 = T("cataract removed", 32, TEXT).move_to([0, 3.5, 0])
        self.add(eye, cloud, cl)
        yb = -2.2
        axis = arr([-5.9, yb, 0], [5.9, yb, 0], GREY, 5, tip=0.2)
        bl = T("birth", 26, TEXT).move_to([-5.45, yb - 0.45, 0])
        age = T("age", 26, GREY).move_to([5.5, yb - 0.45, 0])
        self.at("from birth")
        self.play(Create(axis), FadeIn(bl), FadeIn(age), run_time=0.8)
        mx = -4.1
        mk = Triangle(color=GOLD, fill_opacity=1, stroke_width=0).scale(0.22).rotate(PI).move_to([mx, yb + 0.3, 0])
        ml = chip("early in infancy", GOLD, size=28).move_to([mx + 1.1, -3.2, 0])
        joint = Line([mx, yb - 0.08, 0], [mx, ml.get_top()[1], 0], color=GOLD, stroke_width=4)
        self.at("removed")
        pc = eye[1].get_center()
        dpup = VGroup(Circle(radius=0.5, stroke_width=0, fill_color="#0b0e14", fill_opacity=1).move_to(pc),
                      Circle(radius=0.13, stroke_width=0, fill_color=TEXT, fill_opacity=0.9).move_to(pc + UR * 0.2))
        self.play(FadeOut(cloud), FadeOut(cl), FadeIn(dpup), FadeIn(mk, shift=DOWN * 0.2), run_time=0.35)
        self.play(FadeIn(cl2, shift=DOWN * 0.1), run_time=0.3)
        self.at("early in infancy")
        self.play(Create(joint), FadeIn(ml, shift=UP * 0.1), run_time=0.5)
        band = Rectangle(width=5.4, height=0.8, stroke_width=0, fill_color=GOLD, fill_opacity=0.25).move_to([-3.1, yb + 0.45, 0])
        wl = T("the window", 38, "#F2CF6B", weight=BOLD).move_to([-3.1, yb + 1.2, 0])
        self.at("same reason")
        self.play(FadeIn(band), FadeIn(wl, shift=DOWN * 0.1), Indicate(eye, color=BLUE, scale_factor=1.03), run_time=0.9)
        self.finish()


# ================================================================== s28 to s29 takeaway and window
def window(cx, cy, h, open_frac):
    """A window frame with one sash hinged on the left. open_frac 0 = shut, 1 = wide open."""
    w = h * 0.9
    frame = Rectangle(width=w, height=h, stroke_color=GOLD, stroke_width=7, fill_color=GOLD, fill_opacity=0.06).move_to([cx, cy, 0])
    wid = (w - 0.2) * (1 - 0.8 * open_frac)
    hh = (h - 0.2) * (1 - 0.1 * open_frac)
    x0 = cx - w / 2 + 0.1
    sash = Polygon([x0, cy - (h - 0.2) / 2, 0], [x0, cy + (h - 0.2) / 2, 0], [x0 + wid, cy + hh / 2, 0], [x0 + wid, cy - hh / 2, 0],
                   stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.28)
    bar = Line([x0 + wid / 2, cy - hh / 2 * 0.95, 0], [x0 + wid / 2, cy + hh / 2 * 0.95, 0], color=GOLD, stroke_width=3)
    cross = Line([x0, cy, 0], [x0 + wid, cy, 0], color=GOLD, stroke_width=3)
    return VGroup(frame, sash, bar, cross)


WIN_C = (3.7, 0.25)
WIN_H = 5.4


def rule3():
    return T("the cell keeps\nthe eye that\nhelps it fire", 52, TEXT, font=TITLE_FONT, line_spacing=0.9)


class S28(Sc):
    def construct(self):
        rule = rule3().move_to([0, 0.2, 0])
        self.add(rule)
        w = window(WIN_C[0], WIN_C[1], WIN_H, 0.0)
        self.at("That contest")
        self.play(rule.animate.move_to([-3.3, 0.25, 0]), run_time=0.7)
        self.play(FadeIn(w), run_time=0.6)
        wl = T("while the window is open", 34, GOLD).move_to([WIN_C[0], WIN_C[1] - WIN_H / 2 - 0.55, 0])
        self.at("while the window")
        self.play(Transform(w, window(WIN_C[0], WIN_C[1], WIN_H, 1.0)), FadeIn(wl, shift=UP * 0.1), run_time=1.2)
        self.finish()


class S29(Sc):
    def construct(self):
        rule = rule3().move_to([-3.3, 0.25, 0])
        w = window(WIN_C[0], WIN_C[1], WIN_H, 1.0)
        wl = T("while the window is open", 34, GOLD).move_to([WIN_C[0], WIN_C[1] - WIN_H / 2 - 0.55, 0])
        self.add(rule, w, wl)
        q = T("what opens and closes the window?", 44, TEXT, font=TITLE_FONT).move_to([0, 3.35, 0])
        # clear the text first, then move the window to the centre
        self.play(FadeOut(rule), FadeOut(wl), run_time=0.35)
        self.play(w.animate.move_to([0, -0.15, 0]).scale(4.8 / WIN_H), FadeIn(q, shift=DOWN * 0.1), run_time=0.8)
        self.play(Transform(w, window(0, -0.15, 4.8, 0.45)), run_time=1.0)
        nl = chip("next lesson", GOLD, size=36).move_to([0, -3.2, 0])
        self.at("next lesson's question")
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S30End(NarratedScene):
    LINE = "The contest between the eyes\ncounts most while the window is open."

    def construct(self):
        line = T(self.LINE, size=46, font=TITLE_FONT, line_spacing=0.9)
        fit(line, max_w=12.2)
        sub = T("biochemistrypedia.com", size=32, color="#8FE3E9")
        g = VGroup(line, sub).arrange(DOWN, buff=0.55)
        self.add(g)
        self.finish()
