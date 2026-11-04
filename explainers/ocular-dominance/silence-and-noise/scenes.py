"""Ocular dominance, chapter 5: Silence Is Not Noise  (Biochemistrypedia chaptered explainer)

COLOR MAP (one colour per concept, shared by every chapter; the lesson's convention is that the left
hemisphere is recorded, so the right eye is contralateral and the left eye ipsilateral)
  ORANGE = the right (contralateral) eye, group 1 of the histogram; in this chapter it is also the eye that
           is sutured or silenced (the closed eye)
  BLUE   = the left (ipsilateral) eye, group 7; here the open, active eye
  PURPLE = a cortical cell that both eyes can drive, and that cell's response
  RED    = tetrodotoxin and anything crossed out
  GOLD   = credits, the question mark, the threshold line, "predicted" tags
  GREEN  = sodium ions only
  GREY   = outlines and neutral things (small labels use the lighter LGREY)
Histogram bars run from orange (group 1) through purple (group 4) to blue (group 7).
"""
import numpy as np

ORANGE = "#F2994A"
PURPLE = "#B58CD9"
from bp_style import *  # noqa: F401,F403

DARK_PUPIL = "#454b58"
LGREY = "#C3C9D6"       # small labels: lighter than GREY so they read on the dark ground

# ------------------------------------------------------------------ spike data (arbitrary time units, 0 to 10)
BURSTS = [1.0, 3.4, 6.0, 8.4]                                   # moments the open eye drives the cell
OPEN_T = [c + 0.2 * k for c in BURSTS for k in range(5)]        # open eye: bursts of five spikes
CELL_T = [c + 0.12 + 0.25 * k for c in BURSTS for k in range(3)]  # the cell follows the open eye
SUT_T = [0.35, 2.0, 2.5, 4.7, 5.2, 7.1, 7.6, 9.7]               # sutured eye: scattered, unpatterned (all in the gaps)
SUT_F, SIL_F = 0.45, 0.80                                       # schematic bar heights, same in s14, s15 and s24


def resp(times, wgt, tt, tau=0.45):
    """Leaky integrator of a spike train: each spike adds wgt, decaying with time constant tau."""
    r = np.zeros_like(tt)
    for s in times:
        m = tt >= s
        r[m] += wgt * np.exp(-(tt[m] - s) / tau)
    return r


# ------------------------------------------------------------------ helpers
def arr(a, b, color=GREY, w=6, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def make_eye(color=ORANGE, scale=1.0, state="open"):
    """VGroup(outline, pupil, glint, stitches). state: open, dark (silenced) or sutured (closed, stitched)."""
    w = 2.0 * scale
    ell = Ellipse(width=w, height=1.1 * scale, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15)
    pup = Circle(radius=0.3 * scale, stroke_width=0, fill_color=color, fill_opacity=1)
    glint = Circle(radius=0.08 * scale, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pup.get_center() + UR * 0.1 * scale)
    st = VGroup(*[Line([x * scale, -0.36 * scale, 0], [x * scale, 0.36 * scale, 0], stroke_width=4.5, color=color)
                  for x in (-0.7, -0.35, 0, 0.35, 0.7)])
    st.set_opacity(0)
    g = VGroup(ell, pup, glint, st)
    if state == "dark":
        pup.set_fill(DARK_PUPIL, 1)
        glint.set_opacity(0)
        ell.set_fill(color, 0.04)
    elif state == "sutured":
        ell.stretch_to_fit_height(w * 0.17)
        ell.set_fill(color, 0.3)
        pup.set_opacity(0)
        glint.set_opacity(0)
        st.set_opacity(1)
    return g


def sew(g):
    return [g[0].animate.stretch_to_fit_height(g[0].width * 0.17).set_fill(g[0].get_color(), 0.3), g[1].animate.set_opacity(0),
            g[2].animate.set_opacity(0), g[3].animate.set_opacity(1)]


def darken(g):
    return [g[1].animate.set_fill(DARK_PUPIL, 1), g[2].animate.set_opacity(0), g[0].animate.set_fill(g[0].get_color(), 0.04)]


def spikes(times, x0, x1, y, h=0.55, color=ORANGE, T0=10.0, w=0.06, sw=4):
    """A spike train drawn as a polyline, one tick per spike time (times run 0..T0 across x0..x1)."""
    pts = [[x0, y, 0]]
    for t in sorted(times):
        x = x0 + (x1 - x0) * t / T0
        pts += [[x - w, y, 0], [x, y + h, 0], [x + w, y, 0]]
    pts.append([x1, y, 0])
    m = VMobject()
    m.set_points_as_corners(pts)
    m.set_stroke(color, sw)
    return m


def kind_card(kind, big, cx):
    """VGroup(card, title, eye, trace) for a sutured or a silenced eye; same structure at both sizes."""
    sut = kind == "sutured"
    if big:
        cy, w, h, ts, es = 0.0, 6.4, 6.2, 36, 2.6
        title_pos, eye_pos = [cx + 0.3, cy + 2.5, 0], [cx, cy + 0.7, 0]
        x0, x1, ty, th = cx - 2.7, cx + 2.7, cy - 2.0, 1.0
    else:
        cy, w, h, ts, es = 2.1, 6.4, 3.3, 30, 1.3
        title_pos, eye_pos = [cx, cy + 1.25, 0], [cx - 1.7, cy - 0.3, 0]
        x0, x1, ty, th = cx - 0.1, cx + 2.9, cy - 0.35, 0.7
    card = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.06).move_to([cx, cy, 0])
    title = T("sutured eye" if sut else "silenced eye", ts, ORANGE).move_to(title_pos)
    eye = make_eye(ORANGE, es, "sutured" if sut else "dark").move_to(eye_pos)
    tr = spikes(SUT_T, x0, x1, ty, h=(th if sut else 0.0), color=ORANGE)   # same structure; flat when silenced
    return VGroup(card, title, eye, tr)


# histogram ------------------------------------------------------------------------------------
HX = [(i - 3) * 1.5 for i in range(7)]
BASE = -2.7
H_NORMAL = [3, 6, 10, 12, 9, 5, 2]
H_SHIFT = [0.5, 1, 2, 3, 6, 10, 13]
INSET = 0.02     # bars sit just above the axis line so their outlines never dip below it


def gcol(i):
    A, P, B = ManimColor(ORANGE), ManimColor(PURPLE), ManimColor(BLUE)
    return interpolate_color(A, P, i / 3) if i <= 3 else interpolate_color(P, B, (i - 3) / 3)


def hbars(h, hx=HX, base=BASE, unit=0.38, bw=1.2):
    out = VGroup()
    for i, v in enumerate(h):
        hh = max(v * unit, 0.05)
        out.add(Rectangle(width=bw, height=hh, stroke_color=gcol(i), stroke_width=2, fill_color=gcol(i),
                          fill_opacity=0.6).move_to([hx[i], base + INSET + hh / 2, 0]))
    return out


def hnums(hx=HX, base=BASE, size=26, dy=0.4):
    return VGroup(*[T(str(i + 1), size, TEXT).move_to([hx[i], base - dy, 0]) for i in range(7)])


def hline(hx=HX, base=BASE, pad=0.9):
    return Line([hx[0] - pad, base, 0], [hx[-1] + pad, base, 0], color=GREY, stroke_width=3)


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
    with open(Path(os.environ["KX_SCRIPT"]).parent / "scratch" / "audit.log", "a") as f:
        f.write(f"{sid}: {'ok' if not out else '; '.join(out)}\n")


class Sc(SpokenScene):
    def finish(self):
        import os
        if os.environ.get("KX_AUDIT"):
            _audit(self)
        super().finish()


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Ocular dominance and the critical period"
    TITLE = "Silence Is Not Noise"


class S01(Sc):
    def construct(self):
        q = T("Which loses more of the cortex?", 38).move_to([0, 3.15, 0])
        eL = make_eye(ORANGE, 2.5, "dark").move_to([-3.3, 1.3, 0])
        eR = make_eye(ORANGE, 2.5, "sutured").move_to([3.3, 1.3, 0])
        self.add(q, eL, eR)
        flat = spikes([], -5.7, -0.9, -0.9, color=ORANGE)
        noisy = spikes(SUT_T, 0.9, 5.7, -0.9, h=1.3, color=ORANGE)
        l1 = T("sends nothing", 32, ORANGE).move_to([-3.3, -2.3, 0])
        l2 = T("sends noise", 32, ORANGE).move_to([3.3, -2.3, 0])
        self.at("an eye that sends nothing")
        self.play(Create(flat), FadeIn(l1, shift=UP * 0.1), run_time=1.0)
        self.at("or an eye that sends noise")
        self.play(Create(noisy), FadeIn(l2, shift=UP * 0.1), run_time=1.4)
        self.finish()


class S02(Sc):
    def construct(self):
        eye = make_eye(ORANGE, 2.6).move_to([0, 1.8, 0])
        bar = Rectangle(width=0.2, height=1.9, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([-5.6, 1.8, 0])
        a1 = arr([-4.9, 1.8, 0], [-2.8, 1.8, 0], GREY, 6)
        l_img = T("image", 26, LGREY).move_to([-5.6, 0.5, 0])
        self.add(eye, bar, a1, l_img)
        self.at("lid suture", lead=0.0)
        self.play(*sew(eye), run_time=0.6)
        a2 = arr([2.8, 1.8, 0], [3.9, 1.8, 0], GREY, 6)
        glow = VGroup(*[Rectangle(width=0.2 + 0.24 * i, height=1.9 + 0.12 * i, stroke_width=0, fill_color=TEXT,
                                  fill_opacity=0.16).move_to([5.0, 1.8, 0]) for i in range(5)])
        l_bl = T("blurred", 26, LGREY).move_to([5.0, 0.4, 0])
        self.at("blurs")
        self.play(GrowArrow(a2), FadeIn(glow), FadeIn(l_bl), run_time=0.9)
        chipr = chip("retina", ORANGE, size=28).move_to([-5.2, -1.7, 0])
        tr = spikes([0.4, 1.3, 1.8, 3.0, 3.4, 4.6, 5.9, 6.3, 7.5, 8.8, 9.3], -3.6, 5.6, -1.7, h=1.5, color=ORANGE)
        self.at("its retina")
        self.play(FadeIn(chipr, shift=RIGHT * 0.1), run_time=0.4)
        self.at("keeps firing")
        self.play(Create(tr), run_time=1.6)
        self.finish()


class S03(Sc):
    def construct(self):
        eye = make_eye(ORANGE, 2.6).move_to([0, 0.95, 0])
        y86 = T("1986", 64, GOLD, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.play(FadeIn(eye), FadeIn(y86, shift=DOWN * 0.1), run_time=0.5)
        full = VGroup(T("Stryker laboratory, 1986", 48, GOLD, font=TITLE_FONT),
                      T("Chapman and colleagues", 28, LGREY)).arrange(DOWN, buff=0.12).move_to([0, 3.05, 0])
        self.at("Michael")
        self.play(ReplacementTransform(y86, full), run_time=0.8)
        tr = spikes([0.3, 0.9, 1.2, 2.1, 2.6, 2.9, 3.8, 4.2, 4.9, 5.3, 5.5, 6.6, 7.0, 7.7, 8.3, 8.6, 9.5], -4.7, 5.6, -1.95, h=1.2, color=ORANGE)
        rl = chip("retina", ORANGE, size=28).move_to([-5.9, -1.5, 0])
        lab = T("electrical activity", 40, TEXT).move_to([0, -3.1, 0])
        self.at("whether")
        self.play(Create(tr), FadeIn(rl, shift=RIGHT * 0.1), run_time=1.0)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        q = T("?", 90, GOLD, weight=BOLD).move_to([3.3, -3.0, 0])
        self.at("itself")
        self.play(FadeIn(q, scale=1.4), run_time=0.6)
        self.finish()


class S04(Sc):
    def construct(self):
        eye = make_eye(ORANGE, 2.3).move_to([-2.9, 1.3, 0])
        d = np.array([np.cos(np.radians(45)), np.sin(np.radians(45)), 0])
        tip = np.array([-2.8, -0.02, 0])
        k = 1.3
        barrel = RoundedRectangle(corner_radius=0.08, width=1.8, height=0.55, stroke_color=GREY, stroke_width=3,
                                  fill_color=RED, fill_opacity=0.45)
        needle = Line([0.9, 0, 0], [1.6, 0, 0], color=TEXT, stroke_width=4)
        rod = Line([-0.9, 0, 0], [-1.5, 0, 0], color=GREY, stroke_width=4)
        thumb = Rectangle(width=0.12, height=0.8, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([-1.5, 0, 0])
        syr = VGroup(barrel, needle, rod, thumb).scale(k)
        syr.rotate(np.radians(45))
        syr.shift(tip - needle.get_end())
        syr.shift(-d * 0.4)   # held back from the eye, ready to inject
        lab = T("tetrodotoxin", 34, RED).move_to([-1.7, -2.6, 0])
        SH = RIGHT * 2.9
        eye.shift(SH)
        syr.shift(SH)
        lab.shift(SH)
        self.add(eye, syr)
        self.at("silenced")
        self.play(syr.animate.shift(d * 0.4), run_time=0.6)
        self.at("tetrodotoxin")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        # close-up of the membrane with two sodium channels
        mem = RoundedRectangle(corner_radius=0.1, width=5.8, height=0.9, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([3.7, 0.0, 0])
        slots = [2.4, 5.0]
        chans = VGroup()
        for cx in slots:
            body = RoundedRectangle(corner_radius=0.12, width=1.7, height=3.0, stroke_color=TEAL, stroke_width=3,
                                    fill_color=TEAL, fill_opacity=0.5).move_to([cx, 0, 0])
            slot = Rectangle(width=0.5, height=3.0, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([cx, 0, 0])
            chans.add(VGroup(body, slot))

        def ion(x, y):
            return VGroup(Circle(radius=0.4, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5),
                          T("Na+", 26, TEXT)).move_to([x, y, 0])
        ions = VGroup(*[ion(x, 3.1) for x in slots])
        self.at("a toxin that")
        self.play(FadeIn(mem), FadeIn(chans), FadeIn(ions), VGroup(eye, syr, lab).animate.shift(-SH), run_time=0.4)
        self.play(ions.animate.shift(DOWN * 6.2), run_time=0.55, rate_func=linear)
        plugs = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.5, height=1.1, stroke_width=0, fill_color=RED, fill_opacity=1)
                         .move_to([x, 0.95, 0]) for x in slots])
        ions2 = VGroup(*[ion(x, 2.95) for x in slots])
        arrows = VGroup(*[arr([x, 2.5, 0], [x, 1.62, 0], GREEN, 6, 0.2) for x in slots])
        self.at("blocks")
        self.play(FadeOut(ions), FadeIn(ions2), FadeIn(plugs, shift=DOWN * 0.8), run_time=0.4)
        cl = T("sodium channels", 32, TEAL).move_to([3.7, -2.2, 0])
        self.at("sodium channels")
        self.play(FadeIn(cl, shift=UP * 0.1), *[GrowArrow(a) for a in arrows], run_time=0.5)
        # hand-over to the next scene: the eye's output cells, still lit and firing
        cells, rings, axons, trunk, nerve = s05_lit()
        rings.add_updater(lambda m: m.set_stroke(opacity=0.45 + 0.4 * np.sin(self.renderer.time * 16)))
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(axons), FadeIn(cells), FadeIn(rings), FadeIn(trunk), FadeIn(nerve),
                  run_time=0.5)
        self.finish()


TT5 = [0.4, 1.0, 1.5, 2.2, 2.7, 3.4, 3.9, 4.6, 5.2, 5.7, 6.5, 7.0, 7.8, 8.3, 9.0, 9.6]
YS5 = [2.4, 1.2, 0.0, -1.2, -2.4]
J5 = np.array([-0.8, 0.0, 0.0])


def s05_lit():
    """The lit, spiking retinal ganglion cells: cells, rings, axons, optic-nerve trace, nerve label."""
    cells = VGroup(*[Circle(radius=0.5, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.6)
                     .move_to([-5.4, y, 0]) for y in YS5])
    rings = VGroup(*[Circle(radius=0.68, stroke_color=ORANGE, stroke_width=3, fill_opacity=0).move_to([-5.4, y, 0]) for y in YS5])
    axons = VGroup(*[Line([-4.9, y, 0], J5, color=ORANGE, stroke_width=5) for y in YS5])
    trunk = spikes(TT5, J5[0], 6.3, 0.0, h=0.6, color=ORANGE, sw=5)
    nerve = T("optic nerve", 32, LGREY).move_to([3.5, -0.8, 0])
    return cells, rings, axons, trunk, nerve


class S05(Sc):
    def construct(self):
        cells, rings, axons, trunk, nerve = s05_lit()
        self.add(axons, cells, rings, trunk, nerve)
        rings.add_updater(lambda m: m.set_stroke(opacity=0.45 + 0.4 * np.sin(self.renderer.time * 16)))
        flat = spikes(TT5, J5[0], 6.3, 0.0, h=0.0, color=DARK_PUPIL, sw=5)
        self.at("silences", lead=0.0)
        rings.clear_updaters()
        self.play(*[c.animate.set_stroke(GREY, 4).set_fill(DARK_PUPIL, 0.9) for c in cells], FadeOut(rings),
                  *[a.animate.set_stroke(DARK_PUPIL, 5) for a in axons], Transform(trunk, flat), run_time=0.78)
        lab = T("retinal ganglion cells", 34, TEXT)
        lab.move_to([-4.2 + lab.width / 2, 3.45, 0])
        self.at("retinal ganglion cells")
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        out = T("the eye's output neurons", 30, TEXT)
        out.move_to([-4.2 + out.width / 2, 2.85, 0])
        self.at("output neurons")
        self.play(FadeIn(out, shift=UP * 0.1), Indicate(cells, color=ORANGE, scale_factor=1.1), run_time=0.8)
        self.finish()


class S06(Sc):
    def construct(self):
        ax, nums = hline(HX, BASE), hnums(HX, BASE, 26, 0.38)
        yl = T("number of cells", 26, LGREY).rotate(PI / 2).move_to([-6.45, -0.3, 0])
        bars = hbars(H_NORMAL)
        ca = make_eye(ORANGE, 0.45, "dark").move_to([-6.35, -3.55, 0])
        cb = make_eye(BLUE, 0.45).move_to([6.1, -3.55, 0])
        ta = T("silenced eye only", 26, ORANGE).move_to([-4.1, -3.55, 0])
        tb = T("active eye only", 26, BLUE).move_to([4.2, -3.55, 0])
        sch = T("schematic", 26, LGREY).move_to([5.8, 3.5, 0])
        leg = VGroup(T("recording: left hemisphere", 26, TEXT),
                     T("orange = right (contralateral) eye", 26, ORANGE),
                     T("blue = left (ipsilateral) eye", 26, BLUE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        leg.move_to([-6.6 + leg.width / 2, 3.05, 0])
        self.play(FadeIn(VGroup(ax, nums, yl, ca, cb, ta, tb, sch, leg)), FadeIn(bars), run_time=0.6)
        self.at("shifted")
        self.play(Transform(bars, hbars(H_SHIFT)), run_time=0.9)
        move = arr([0.8, 3.3, 0], [3.9, 3.3, 0], TEXT, 6)
        self.at("toward the eye")
        self.play(GrowArrow(move), run_time=0.6)
        self.at("kept firing")
        self.play(Indicate(cb, color=BLUE, scale_factor=1.3), Indicate(tb, color=BLUE, scale_factor=1.1), run_time=0.9)
        self.finish()


class S07(Sc):
    def construct(self):
        hx = [3.4 + (i - 3) * 0.85 for i in range(7)]
        base = -2.2
        bars = hbars(H_SHIFT, hx, base, 0.34, 0.66)
        ax, nums = hline(hx, base, pad=0.5), hnums(hx, base, 26, 0.38)
        el1 = make_eye(ORANGE, 0.9, "dark").move_to([-5.7, 1.15, 0])
        el2 = make_eye(BLUE, 0.9).move_to([-5.7, -1.3, 0])
        t1 = spikes([], -4.3, -0.9, 1.0, color=ORANGE)
        t2 = spikes([0.5, 1.1, 1.4, 2.6, 3.1, 3.5, 4.8, 5.2, 6.3, 6.6, 7.9, 8.4, 8.8, 9.5], -4.3, -0.9, -1.4, h=0.9, color=BLUE)
        n1 = T("silenced eye", 26, ORANGE).move_to([-5.7, 0.4, 0])
        n2 = T("active eye", 26, BLUE).move_to([-5.7, -2.05, 0])
        self.play(FadeIn(VGroup(ax, nums, bars, el1, el2, n1, n2)), Create(t1), Create(t2), run_time=0.4)
        lab = T("an imbalance of electrical activity is enough", 36, TEXT).move_to([0, 3.2, 0])
        self.at("imbalance")
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.8)
        self.at("enough to cause")
        sh = arr([-0.7, -1.0, 0], [4.62, 1.1, 0], GOLD, 7)
        self.play(GrowArrow(sh), run_time=0.8)
        self.at("shift")
        self.play(Indicate(bars[5:], color=BLUE, scale_factor=1.08), run_time=0.9)
        self.finish()


class S08(Sc):
    def construct(self):
        eA = make_eye(ORANGE, 2.7).move_to([-3.4, 1.2, 0])
        eB = make_eye(BLUE, 2.7).move_to([3.4, 1.2, 0])
        ts = [0.5, 1.2, 1.5, 2.6, 3.1, 3.7, 4.8, 5.2, 6.3, 6.7, 7.9, 8.4, 9.3]
        tA = spikes(ts, -6.0, -0.8, -1.3, h=1.0, color=ORANGE)
        tB = spikes([t + 0.3 for t in ts[::-1]], 0.8, 6.0, -1.3, h=1.0, color=BLUE)
        self.add(eA, eB)
        self.play(Create(tA), Create(tB), run_time=0.9)
        cred = T("Stryker and Harris, 1986", 36, GOLD).move_to([0, 3.4, 0])
        self.at("Stryker")
        self.play(FadeIn(cred, shift=DOWN * 0.1), run_time=0.5)
        flA = spikes(ts, -6.0, -0.8, -1.3, h=0.0, color=ORANGE)
        flB = spikes([t + 0.3 for t in ts[::-1]], 0.8, 6.0, -1.3, h=0.0, color=BLUE)
        self.at("silenced both eyes", lead=0.1)
        self.play(*darken(eA), *darken(eB), Transform(tA, flA), Transform(tB, flB), run_time=0.6)
        dev = chip("during development", GOLD, size=32).move_to([0, -2.6, 0])
        self.at("during development")
        self.play(FadeIn(dev, shift=UP * 0.1), run_time=0.5)
        self.finish()


def s09_ends(colors, ys, xs):
    ends = VGroup()
    for x, col, y_end in zip(xs, colors, ys):
        c = ORANGE if col == 0 else BLUE
        ln = Line([x, 2.85, 0], [x, y_end, 0], color=c, stroke_width=4)
        dot = Circle(radius=0.17, stroke_width=0, fill_color=c, fill_opacity=0.95).move_to([x, y_end, 0])
        ends.add(VGroup(ln, dot))
    return ends


class S09(Sc):
    def construct(self):
        rng = np.random.default_rng(5)
        band = Rectangle(width=12.4, height=3.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to([0, -1.2, 0])
        centres = [-5.1 + 2.04 * i for i in range(6)]
        stripes = VGroup(*[Rectangle(width=2.0, height=3.5, stroke_width=0, fill_color=(ORANGE if i % 2 == 0 else BLUE),
                                     fill_opacity=0.13).move_to([c, -1.2, 0]) for i, c in enumerate(centres)])
        lab = T("layer 4", 32, TEXT).move_to([-5.2, -3.45, 0])
        ca = make_eye(ORANGE, 0.6).move_to([-6.0, 3.3, 0])
        cb = make_eye(BLUE, 0.6).move_to([6.0, 3.3, 0])
        xs = [c + o for c in centres for o in (-0.65, -0.22, 0.22, 0.65)]
        colors_n = [i // 4 % 2 for i in range(24)]
        ys_n = list(rng.uniform(-2.6, -0.4, size=24))
        colors_m = list(rng.integers(0, 2, size=24))
        colors_m[:6] = [0, 1, 0, 1, 1, 0]
        ys_m = list(rng.uniform(-2.6, -0.4, size=24))
        ends = s09_ends(colors_n, ys_n, xs)
        mixed = s09_ends(colors_m, ys_m, xs)
        self.play(FadeIn(VGroup(band, stripes, lab, ca, cb)), run_time=0.4)
        self.play(LaggedStart(*[Create(e) for e in ends], lag_ratio=0.04), run_time=0.8)
        nl = T("normal", 34, TEXT).move_to([4.6, -3.45, 0])
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.3)
        fl = T("failed to separate", 34, TEXT).move_to([4.2, -3.45, 0])
        self.at("failed", lead=0.1)
        self.play(Transform(ends, mixed), FadeOut(stripes), ReplacementTransform(nl, fl), *darken(ca), *darken(cb), run_time=1.0)
        bounds = VGroup(*[DashedLine([-6.2 + 2.04 * i, 0.55, 0], [-6.2 + 2.04 * i, -2.95, 0], color=GREY, stroke_width=2, dash_length=0.12)
                          for i in range(1, 6)])
        self.at("stripes")
        self.play(FadeIn(bounds), run_time=0.5)
        self.finish()


def cards_big():
    c1 = kind_card("sutured", True, -3.5)
    c2 = kind_card("silenced", True, 3.5)
    n1 = T("1", 56, GOLD, font=TITLE_FONT).move_to([-6.2, 2.45, 0])
    n2 = T("2", 56, GOLD, font=TITLE_FONT).move_to([0.8, 2.45, 0])
    return c1, c2, n1, n2


BIG_EYE = 3.0 / 2.6      # in s10 the eyes sit larger, at the card's centre; s11 moves them up as the titles arrive


def centre_eyes(c1, c2):
    for c, cx in ((c1, -3.5), (c2, 3.5)):
        c[2].scale(BIG_EYE).move_to([cx, 0.0, 0])


class S10(Sc):
    def construct(self):
        c1, c2, n1, n2 = cards_big()
        centre_eyes(c1, c2)
        self.play(FadeIn(c1[0]), FadeIn(c2[0]), FadeIn(c1[2], scale=0.9), FadeIn(c2[2], scale=0.9), run_time=0.6)
        self.at("two ways")
        self.play(FadeIn(n1, scale=1.3), FadeIn(n2, scale=1.3), run_time=0.6)
        self.finish()


class S11(Sc):
    def construct(self):
        c1, c2, n1, n2 = cards_big()
        e1_to, e2_to = c1[2].get_center(), c2[2].get_center()
        centre_eyes(c1, c2)
        self.add(c1[0], c1[2], c2[0], c2[2], n1, n2)
        self.at("sutured eye")
        self.play(FadeIn(c1[1], shift=DOWN * 0.1), c1[2].animate.scale(1 / BIG_EYE).move_to(e1_to), run_time=0.5)
        self.at("still fires")
        self.play(Create(c1[3]), run_time=1.2)
        self.at("silenced eye")
        self.play(FadeIn(c2[1], shift=DOWN * 0.1), c2[2].animate.scale(1 / BIG_EYE).move_to(e2_to), run_time=0.5)
        self.at("sends nothing")
        self.play(Create(c2[3]), run_time=1.0)
        self.finish()


def s12_frame():
    c1 = kind_card("sutured", False, -3.5)
    c2 = kind_card("silenced", False, 3.5)
    q = T("which closed eye loses more?", 40, GOLD).move_to([0, -0.05, 0])
    ra = chip("the more active eye wins", LGREY, size=34, pad=0.26).move_to([0, -1.4, 0])
    rb = chip("the cell keeps the eye that helps it fire", PURPLE, size=34, pad=0.26).move_to([0, -2.8, 0])
    return c1, c2, q, ra, rb


class S12(Sc):
    def construct(self):
        c1, c2, n1, n2 = cards_big()
        self.add(*c1, *c2)
        s1, s2, q, ra, rb = s12_frame()
        self.play(Transform(c1, s1), Transform(c2, s2), run_time=0.9)
        self.at("the more active eye")
        self.play(FadeIn(ra, shift=UP * 0.1), run_time=0.6)
        self.at("which closed eye")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.at("our rule")
        self.play(FadeIn(rb, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        c1, c2, q, ra, rb = s12_frame()
        self.add(*c1, *c2, q, ra, rb)
        tr = ValueTracker(0)
        R, C = 0.42, np.array([2.75, -0.05, 0])
        track = Circle(radius=R, stroke_color=GREY, stroke_width=5).move_to(C)
        arc = always_redraw(lambda: Arc(radius=R, start_angle=PI / 2, angle=-TAU * max(1 - tr.get_value(), 0.003),
                                        arc_center=C, stroke_color=GOLD, stroke_width=7))
        lab = T("pause and predict", 28, GOLD).move_to([5.0, -0.05, 0])
        self.play(q.animate.shift(LEFT * 1.6), FadeIn(track), FadeIn(lab), run_time=0.5)
        self.add(arc)
        self.play(tr.animate.set_value(1), run_time=4.3, rate_func=linear)
        self.finish()


BASE_Y = -3.0
BAR_H = 4.6
BAR_X = (-3.0, 3.0)


def bar(x, frac, color=ORANGE):
    h = max(frac * BAR_H, 0.05)
    return Rectangle(width=2.2, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5).move_to([x, BASE_Y + INSET + h / 2, 0])


def bar_frame(sil_label="silenced", credit=False):
    ax = Line([-5.4, BASE_Y, 0], [5.4, BASE_Y, 0], color=GREY, stroke_width=3)
    yl = T("cortical responses to that eye", 26, LGREY).rotate(PI / 2).move_to([-6.6, -0.7, 0])
    l1 = T("sutured", 28, ORANGE).move_to([BAR_X[0], -3.5, 0])
    l2 = T(sil_label, 28, ORANGE).move_to([BAR_X[1], -3.5, 0])
    ey = 2.55 if credit else 2.7
    e1 = make_eye(ORANGE, 0.85, "sutured").move_to([BAR_X[0], ey, 0])
    e2 = make_eye(ORANGE, 0.85, "dark").move_to([BAR_X[1], ey, 0])
    sch = T("schematic", 26, LGREY).move_to([5.7, 3.5, 0])
    return VGroup(ax, yl, l1, l2, e1, e2, sch), l2


def yb(f):
    return BASE_Y + f * BAR_H


class S14(Sc):
    def construct(self):
        fr, _ = bar_frame()
        b1, b2 = bar(BAR_X[0], 1.0), bar(BAR_X[1], 1.0)
        normal = DashedLine([-4.4, yb(1.0), 0], [4.4, yb(1.0), 0], color=LGREY, stroke_width=3, dash_length=0.14)
        nl = T("normal", 26, LGREY).move_to([5.55, yb(1.0), 0])
        self.play(FadeIn(fr), FadeIn(b1), FadeIn(b2), FadeIn(normal), FadeIn(nl), run_time=0.7)
        self.at("silenced eye is quieter")
        self.play(Indicate(fr[3], color=ORANGE, scale_factor=1.2), run_time=0.8)
        pl1 = DashedLine([-4.4, yb(0.7), 0], [-1.7, yb(0.7), 0], color=GOLD, stroke_width=5, dash_length=0.14)
        pl2 = DashedLine([1.7, yb(0.35), 0], [4.4, yb(0.35), 0], color=GOLD, stroke_width=5, dash_length=0.14)
        pt1 = T("predicted", 26, GOLD).move_to([-5.55, yb(0.7), 0])
        pt2 = T("predicted", 26, GOLD).move_to([5.55, yb(0.35), 0])
        self.at("so it should lose more")
        self.play(Create(pl1), Create(pl2), FadeIn(pt1), FadeIn(pt2), run_time=0.9)
        self.at("it loses less")
        self.play(Transform(b2, bar(BAR_X[1], SIL_F)), Transform(b1, bar(BAR_X[0], SUT_F)), run_time=0.8)
        self.finish()


def s15_frame():
    fr, l2 = bar_frame("silenced with tetrodotoxin", credit=True)
    return fr, l2, bar(BAR_X[0], SUT_F), bar(BAR_X[1], SIL_F)


def s15_marks():
    y1, y2 = yb(SUT_F), yb(SIL_F)
    d1 = DashedLine([-1.9, y1, 0], [0.3, y1, 0], color=GOLD, stroke_width=3, dash_length=0.12)
    d2 = DashedLine([1.9, y2, 0], [-0.3, y2, 0], color=GOLD, stroke_width=3, dash_length=0.12)
    gap = DoubleArrow([0.0, y1, 0], [0.0, y2, 0], buff=0.0, color=GOLD, stroke_width=5, tip_length=0.2)
    lab = T("suture weakens more", 28, GOLD).move_to([0, y2 + 0.5, 0])
    return d1, d2, gap, lab


class S15(Sc):
    def construct(self):
        fr, l2, b1, b2 = s15_frame()
        self.add(fr, b1, b2)
        cred = T("Rittenhouse and colleagues, 1999", 28, GOLD).move_to([0, 3.5, 0])
        self.at("in kittens")
        self.play(FadeIn(cred), run_time=0.5)
        self.at("lid suture weakens")
        self.play(Indicate(b1, color=ORANGE, scale_factor=1.06), run_time=0.9)
        d1, d2, gap, lab = s15_marks()
        self.at("more than tetrodotoxin")
        self.play(Create(d1), Create(d2), GrowFromCenter(gap), FadeIn(lab, shift=DOWN * 0.1), run_time=0.9)
        self.play(Indicate(l2, color=ORANGE, scale_factor=1.1), run_time=0.7)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        fr, l2, b1, b2 = s15_frame()
        d1, d2, gap, lab = s15_marks()
        cred = T("Rittenhouse and colleagues, 1999", 28, GOLD).move_to([0, 3.5, 0])
        self.add(fr, b1, b2, d1, d2, gap, lab, cred)
        self.finish()


class S17(Sc):
    def construct(self):
        eye = make_eye(ORANGE, 4.2, "sutured").move_to([1.0, 1.8, 0])
        q = T("Why?", 80, GOLD, font=TITLE_FONT).move_to([-5.1, 1.8, 0])
        self.add(eye)
        self.play(FadeIn(q, shift=RIGHT * 0.1), run_time=0.4)
        chipr = chip("retina", ORANGE, size=30).move_to([-5.6, -1.5, 0])
        tr = spikes([0.4, 1.3, 1.8, 3.0, 3.4, 4.6, 5.9, 6.3, 7.5, 8.8, 9.3], -3.8, 6.2, -2.4, h=2.2, color=ORANGE)
        self.at("retina")
        self.play(FadeOut(q), FadeIn(chipr, shift=RIGHT * 0.1), run_time=0.4)
        self.play(Create(tr), run_time=1.3)
        self.at("under the lid")
        self.play(Indicate(eye, color=ORANGE, scale_factor=1.05), run_time=0.8)
        self.finish()


class S18(Sc):
    def construct(self):
        XL, XR = -3.6, 6.2
        yo, yc, ys = 2.3, 0.2, -1.9

        def px(t):
            return XL + (XR - XL) * t / 10.0
        bands = VGroup(*[Rectangle(width=px(c + 0.9) - px(c - 0.1), height=6.0, stroke_width=0, fill_color=PURPLE, fill_opacity=0.14)
                         .move_to([(px(c + 0.9) + px(c - 0.1)) / 2, 0.15, 0]) for c in BURSTS])
        lab_s = T("sutured eye", 28, ORANGE).move_to([-5.15, ys + 0.3, 0])
        lab_o = T("open eye", 28, BLUE).move_to([-5.15, yo + 0.3, 0])
        lab_c = T("cortical cell", 28, PURPLE).move_to([-5.15, yc + 0.3, 0])
        tr_s = spikes(SUT_T, XL, XR, ys, h=0.9, color=ORANGE)
        tr_o = spikes(OPEN_T, XL, XR, yo, h=0.9, color=BLUE)
        tr_c = spikes(CELL_T, XL, XR, yc, h=0.9, color=PURPLE)
        dim = VGroup(lab_o, lab_c)
        dim.set_opacity(0.3)
        tr_o.set_stroke(opacity=0.3)
        tr_c.set_stroke(opacity=0.3)
        self.add(lab_s, tr_s, lab_o, lab_c, tr_o, tr_c)
        self.at("unpatterned")
        self.play(Indicate(tr_s, color=ORANGE, scale_factor=1.0), Indicate(lab_s, color=ORANGE, scale_factor=1.15), run_time=1.0)
        bl = T("the cell follows the open eye", 30, PURPLE).move_to([1.3, -3.4, 0])
        self.at("out of step")
        self.play(lab_o.animate.set_opacity(1), lab_c.animate.set_opacity(1), tr_o.animate.set_stroke(opacity=1),
                  tr_c.animate.set_stroke(opacity=1), FadeIn(bands), FadeIn(bl, shift=UP * 0.1), run_time=0.7)
        crosses = VGroup()
        for t in SUT_T:
            x, y = px(t), ys + 1.25
            crosses.add(VGroup(Line([x - 0.13, y - 0.13, 0], [x + 0.13, y + 0.13, 0], color=RED, stroke_width=5),
                               Line([x - 0.13, y + 0.13, 0], [x + 0.13, y - 0.13, 0], color=RED, stroke_width=5)))
        self.at("the cells it drives")
        self.play(LaggedStart(*[FadeIn(c, scale=1.5) for c in crosses], lag_ratio=0.1), run_time=0.9)
        self.finish()


CELL_C = np.array([3.6, 0.0, 0])
CELL_R = 2.4


def bundle(y0, w, bs, angles, color=ORANGE, op=1.0):
    parts = [Line([-4.2, y0, 0], [-1.0, y0, 0], color=color, stroke_width=w).set_stroke(opacity=op)]
    pts = [CELL_C + CELL_R * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) for a in angles]
    for p in pts:
        parts.append(Line([-1.0, y0, 0], p, color=color, stroke_width=w).set_stroke(opacity=op))
    for p in pts:
        parts.append(Circle(radius=0.34 * bs, stroke_width=0, fill_color=color, fill_opacity=0.95 * op).move_to(p))
    return VGroup(*parts)


A0 = [150, 180, 210]
A_UP = [115, 140, 165]
A_DN = [195, 220, 245]


def cell_big():
    return VGroup(Circle(radius=CELL_R, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.25).move_to(CELL_C),
                  T("cortical cell", 30, PURPLE).move_to(CELL_C + RIGHT * 0.7))


def ghost(y0, angles):
    return bundle(y0, 9, 1.0, angles, LGREY, 0.5)


def before_note():
    return T("faint grey: before", 26, LGREY).move_to([4.7, 3.45, 0])


class S19(Sc):
    def construct(self):
        cell = cell_big()
        eye = make_eye(ORANGE, 0.55, "sutured").move_to([-5.6, 0.0, 0])
        l1 = T("sutured", 26, ORANGE).move_to([-5.6, -0.75, 0])
        g = ghost(0.0, A0)
        b = bundle(0.0, 9, 1.0, A0)
        self.play(FadeIn(cell), FadeIn(eye), FadeIn(l1), FadeIn(g), FadeIn(b), run_time=0.5)
        hedge = T("seems to weaken", 34, TEXT).move_to([-2.2, 1.5, 0])
        self.at("seems")
        self.play(FadeIn(hedge, shift=DOWN * 0.1), run_time=0.4)
        self.at("weaken")
        self.play(Transform(b, bundle(0.0, 2.5, 0.4, A0)), FadeIn(before_note()), run_time=1.0)
        lab = T("synapses", 30, TEXT).move_to([0.1, -1.75, 0])
        self.at("synapses")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        self.finish()


def s20_pic(final):
    cell = cell_big()
    eye1 = make_eye(ORANGE, 0.55, "sutured").move_to([-5.6, 1.9, 0])
    l1 = T("sutured", 26, ORANGE).move_to([-5.6, 1.15, 0])
    g1, b1 = ghost(1.9, A_UP), bundle(1.9, 2.5, 0.4, A_UP)
    eye2 = make_eye(ORANGE, 0.55, "dark").move_to([-5.6, -1.9, 0])
    l2 = T("silenced", 26, ORANGE).move_to([-5.6, -2.65, 0])
    g2 = ghost(-1.9, A_DN)
    b2 = bundle(-1.9, 7, 0.85, A_DN) if final else bundle(-1.9, 9, 1.0, A_DN)
    return cell, eye1, l1, g1, b1, eye2, l2, g2, b2


class S20(Sc):
    def construct(self):
        cell = cell_big()
        eye = make_eye(ORANGE, 0.55, "sutured").move_to([-5.6, 0.0, 0])
        l1 = T("sutured", 26, ORANGE).move_to([-5.6, -0.75, 0])
        g = ghost(0.0, A0)
        b = bundle(0.0, 2.5, 0.4, A0)
        note = before_note()
        self.add(cell, eye, l1, g, b, note)
        _, eye1, l1n, g1, b1, eye2, l2, g2, b2 = s20_pic(False)
        self.play(Transform(b, b1), Transform(g, g1), eye.animate.move_to([-5.6, 1.9, 0]), l1.animate.move_to([-5.6, 1.15, 0]),
                  FadeIn(eye2), FadeIn(l2), FadeIn(g2), FadeIn(b2), run_time=0.9)
        self.at("never active")
        self.play(Indicate(l2, color=ORANGE, scale_factor=1.25), run_time=0.8)
        self.at("so it loses less")
        self.play(Transform(b2, bundle(-1.9, 7, 0.85, A_DN)), run_time=1.2)
        self.finish()


class S21(Sc):
    def construct(self):
        pic = VGroup(*s20_pic(True), before_note())
        self.add(pic)
        ca = chip("the more active eye wins", LGREY, size=42, pad=0.5).move_to([0, 1.25, 0])
        cb = chip("disuse: the eye used least loses most", LGREY, size=42, pad=0.5).move_to([0, -1.25, 0])
        self.at("more active eye wins")
        self.play(FadeOut(pic), FadeIn(ca, shift=UP * 0.1), run_time=0.7)
        xa = Line(ca.get_left() + RIGHT * 0.15, ca.get_right() + LEFT * 0.15, color=RED, stroke_width=10)
        self.at("fails this test")
        self.play(Create(xa), run_time=0.8)
        self.at("so does")
        self.play(FadeIn(cb, shift=UP * 0.1), run_time=0.6)
        xb = Line(cb.get_left() + RIGHT * 0.15, cb.get_right() + LEFT * 0.15, color=RED, stroke_width=10)
        self.at("disuse")
        self.play(Create(xb), run_time=0.7)
        self.finish()


class S22(Sc):
    def construct(self):
        title = T("the cell keeps the eye that helps it fire", 40, PURPLE).move_to([0, 3.25, 0])
        RX, RW, RH = 1.65, 9.9, 1.85

        def row(y, txt, col, size=30):
            r = RoundedRectangle(corner_radius=0.2, width=RW, height=RH, stroke_color=col, stroke_width=3,
                                 fill_color=col, fill_opacity=0.12).move_to([RX, y, 0])
            t = T(txt, size, TEXT)
            t.move_to([RX - RW / 2 + 0.3 + t.width / 2, y, 0])
            return VGroup(r, t)
        y1, y2, y3 = 1.55, -0.4, -2.35
        r1 = row(y1, "active with a strong response:\nstrengthened", GREEN)
        r2 = row(y2, "active with a weak response:\nweakened", ORANGE)
        r3 = row(y3, "silent: changes little", GREY)
        tag1 = T("strengthening half", 26, GREEN).move_to([-5.3, y1, 0])
        tag2 = T("weakening half", 26, ORANGE).move_to([-5.3, y2 + 0.2, 0])
        # a copy of the next scene's sutured traces, to the right of the row text, so the row carries its reason
        tt = np.arange(0, 10.001, 0.05)
        rs = resp(SUT_T, 0.12, tt)
        X0, X1 = 2.75, 6.25
        base, hs = y2 - 0.78, 1.2
        spk = spikes(SUT_T, X0, X1, y2 + 0.42, h=0.34, color=ORANGE, sw=3, w=0.03)
        cur = VMobject(color=ORANGE, stroke_width=4).set_points_as_corners(
            [np.array([X0 + (X1 - X0) * t / 10, base + hs * v, 0]) for t, v in zip(tt, rs)])
        thr = DashedLine([X0, base + hs * 0.55, 0], [X1, base + hs * 0.55, 0], color=GOLD, stroke_width=2.5, dash_length=0.1)
        thumb = VGroup(spk, thr, cur)
        e1 = make_eye(ORANGE, 0.5, "sutured").move_to([-5.3, y2 - 0.45, 0])
        e2 = make_eye(ORANGE, 0.5, "dark").move_to([-5.3, y3, 0])
        self.at("the rule in the box")
        self.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(r1, shift=UP * 0.1), FadeIn(r2, shift=UP * 0.1), FadeIn(tag1), run_time=0.9)
        self.at("the sutured eye's input")
        self.play(FadeIn(e1), FadeIn(thumb), run_time=0.7)
        self.at("weakening half")
        self.play(FadeIn(tag2), r2[0].animate.set_fill(ORANGE, 0.3).set_stroke(ORANGE, 6), run_time=0.7)
        self.at("a silent input")
        self.play(FadeIn(r3, shift=UP * 0.1), FadeIn(e2), run_time=0.7)
        self.at("left nearly alone")
        self.play(r3[0].animate.set_stroke(TEXT, 5), run_time=0.6)
        self.finish()


class S23(Sc):
    def construct(self):
        XL, XR = -3.6, 6.2

        def px(t):
            return XL + (XR - XL) * t / 10.0
        Y0, H, THR = -2.8, 3.4, 0.55
        tt = np.arange(0, 10.001, 0.05)

        def curve(r, color):
            pts = [np.array([px(t), Y0 + H * min(v, 1.1), 0]) for t, v in zip(tt, r)]
            return VMobject(color=color, stroke_width=5).set_points_as_corners(pts)

        r_open = resp(OPEN_T, 0.30, tt)
        r_sut = resp(SUT_T, 0.12, tt)
        lab_o = T("open eye", 28, BLUE).move_to([-5.2, 2.95, 0])
        tr_o = spikes(OPEN_T, XL, XR, 2.65, h=0.7, color=BLUE)
        axes = VGroup(Line([XL, Y0, 0], [XR, Y0, 0], color=GREY, stroke_width=3), Line([XL, Y0, 0], [XL, Y0 + H + 0.2, 0], color=GREY, stroke_width=3))
        ythr = Y0 + H * THR
        thr = DashedLine([XL, ythr, 0], [XR, ythr, 0], color=GOLD, stroke_width=3, dash_length=0.18)
        lab_t = T("threshold", 26, GOLD).move_to([-5.2, ythr, 0])
        lab_r = T("cell's response", 26, PURPLE).move_to([-5.15, -2.2, 0])
        tarrow = arr([XL + 0.35, -3.65, 0], [5.8, -3.65, 0], LGREY, 4, 0.2)
        tlab = T("time", 26, LGREY).move_to([-4.6, -3.65, 0])
        cur_o = curve(r_open, PURPLE)
        shade = VGroup()
        above = r_open > THR
        i = 0
        while i < len(tt):
            if above[i]:
                j = i
                while j + 1 < len(tt) and above[j + 1]:
                    j += 1
                pts = [np.array([px(tt[k]), Y0 + H * r_open[k], 0]) for k in range(i, j + 1)]
                pts += [np.array([px(tt[j]), ythr, 0]), np.array([px(tt[i]), ythr, 0])]
                shade.add(Polygon(*pts, stroke_width=0, fill_color=PURPLE, fill_opacity=0.4))
                i = j + 1
            else:
                i += 1
        strong = VGroup()
        for c in BURSTS:
            m = (tt >= c) & (tt <= c + 1.6)
            k = np.where(m)[0][np.argmax(r_open[m])]
            strong.add(T("strong", 26, PURPLE).move_to([px(tt[k]), Y0 + H * r_open[k] + 0.4, 0]))
        weak = VGroup()
        for t in (0.35, 2.25, 4.95, 7.35, 9.7):
            w = T("weak", 26, ORANGE)
            w.move_to([max(px(t) + 0.12, XL + 0.2 + w.width / 2), Y0 - 0.36, 0])
            weak.add(w)
        self.play(FadeIn(lab_o), Create(tr_o), FadeIn(axes), FadeIn(thr), FadeIn(lab_t), FadeIn(lab_r), FadeIn(tarrow), FadeIn(tlab), run_time=0.9)
        self.at("cell's strong responses")
        self.play(Create(cur_o, rate_func=linear), run_time=1.7)
        self.play(FadeIn(shade), FadeIn(strong), run_time=0.3)
        lab_s = T("sutured eye", 28, ORANGE).move_to([-5.2, 1.35, 0])
        tr_s = spikes(SUT_T, XL, XR, 1.1, h=0.6, color=ORANGE)
        self.at("on its own")
        self.play(FadeIn(lab_s), Create(tr_s), run_time=0.8)
        cur_s = curve(r_sut, ORANGE)
        self.at("evokes only weak ones")
        self.play(Create(cur_s, rate_func=linear), run_time=1.3)
        self.play(FadeIn(weak), run_time=0.4)
        self.finish()


class S24(Sc):
    def construct(self):
        tk = T("TAKEAWAY", 28, GOLD, weight=BOLD).move_to([0, 3.62, 0])
        title = T("Silence is not noise", 48, TEXT, font=TITLE_FONT).move_to([0, 2.95, 0])
        e1 = make_eye(ORANGE, 1.7, "sutured").move_to([-3.3, 1.35, 0])
        e2 = make_eye(ORANGE, 1.7, "dark").move_to([3.3, 1.35, 0])
        t1 = spikes(SUT_T, -5.6, -1.0, -0.3, h=0.8, color=ORANGE)
        t2 = spikes(SUT_T, 1.0, 5.6, -0.3, h=0.0, color=ORANGE)
        n1 = T("out of step with the cell", 28, ORANGE).move_to([-3.3, -1.05, 0])
        n2 = T("simply silent", 28, ORANGE).move_to([3.3, -1.05, 0])
        base = Line([-5.6, -3.2, 0], [5.6, -3.2, 0], color=GREY, stroke_width=3)
        yl = T("responses to that eye, in kittens", 26, LGREY).move_to([0, -3.58, 0])

        def b(x, f):
            h = max(2.0 * f, 0.05)
            return Rectangle(width=1.8, height=h, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.5).move_to([x, -3.2 + INSET + h / 2, 0])
        t1.set_stroke(opacity=0.3)
        t2.set_stroke(opacity=0.3)
        self.add(tk, e1, e2, base, yl, t1, t2)
        self.at("Take", lead=0.0)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.8)
        self.at("silence is not")
        self.play(t2.animate.set_stroke(opacity=1), FadeIn(n2), run_time=0.8)
        self.at("noise")
        self.play(t1.animate.set_stroke(opacity=1), run_time=0.9)
        self.at("out of step")
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.5)
        self.at("loses more")
        self.play(GrowFromEdge(b(-3.3, SUT_F), DOWN), run_time=0.7)
        self.at("simply silent")
        self.play(GrowFromEdge(b(3.3, SIL_F), DOWN), run_time=0.7)
        self.finish()


def make_cat(scale, color, head_r, body_w, body_h):
    def solid(m, op):
        under = m.copy().set_fill(BG, 1).set_stroke(width=0)
        m.set_fill(color, op)
        return VGroup(under, m)
    r = head_r
    body_c = np.array([0, -r - body_h * 0.35, 0])
    body = Ellipse(width=body_w, height=body_h, stroke_color=color, stroke_width=4).move_to(body_c)
    tail_a = body_c + np.array([body_w * 0.2, -body_h * 0.1, 0])
    tail_b = body_c + np.array([body_w * 0.78, body_h * 0.75, 0])
    tail = ArcBetweenPoints(tail_a, tail_b, angle=PI / 2, stroke_color=color, stroke_width=7)
    ears = VGroup(
        Polygon([-r * 0.95, r * 0.35, 0], [-r * 0.75, r * 1.45, 0], [-r * 0.1, r * 0.95, 0], stroke_color=color, stroke_width=4),
        Polygon([r * 0.95, r * 0.35, 0], [r * 0.75, r * 1.45, 0], [r * 0.1, r * 0.95, 0], stroke_color=color, stroke_width=4))
    head = Circle(radius=r, stroke_color=color, stroke_width=4)
    face = VGroup(Dot([-r * 0.38, r * 0.15, 0], radius=r * 0.09, color=TEXT), Dot([r * 0.38, r * 0.15, 0], radius=r * 0.09, color=TEXT),
                  Triangle(stroke_width=0, fill_color=color, fill_opacity=1).scale(r * 0.1).rotate(PI).move_to([0, -r * 0.2, 0]))
    wh = VGroup(*[Line([s * r * 0.25, -r * 0.3 + k * 0.05 * r, 0], [s * r * 1.15, -r * 0.4 + k * 0.2 * r, 0], color=color, stroke_width=2.5)
                  for s in (-1, 1) for k in (-1, 0, 1)])
    parts = VGroup(tail, solid(ears[0], 0.18), solid(ears[1], 0.18), solid(body, 0.14), solid(head, 0.2), face, wh)
    return parts.scale(scale)


class S25(Sc):
    def construct(self):
        kit = make_cat(1.8, GOLD, 0.75, 1.5, 1.0).move_to([-3.6, 0.35, 0])
        cat = make_cat(1.6, LGREY, 0.85, 3.0, 1.7).move_to([3.1, 0.45, 0])
        lk = T("kitten", 32, GOLD).move_to([-3.6, -3.4, 0])
        lc = T("adult cat", 32, LGREY).move_to([3.1, -3.4, 0])
        self.add(kit, cat, lk, lc)
        q = T("?", 140, GOLD, weight=BOLD).move_to([-0.25, 0.5, 0])
        self.at("Why")
        self.play(FadeIn(q, scale=1.4), run_time=0.6)
        self.at("mainly in the young")
        self.play(Indicate(kit, color=GOLD, scale_factor=1.1), Indicate(lk, color=GOLD, scale_factor=1.15), run_time=1.0)
        self.finish()


class S26End(EndCard):
    LINE = "In kittens, an out-of-step eye loses more than a silent one."

    def construct(self):
        line = T(self.LINE, 40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", 26, TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.4)
        self.play(FadeIn(line, shift=UP * 0.15), FadeIn(sub), run_time=0.4)
        self.finish()
