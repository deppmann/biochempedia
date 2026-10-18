"""Microscopy and quantitative images: why zooming cannot split two dots  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = fluorescent light: the emitters, their blurred images, the intensity curves
  YELLOW = the resolution d and the numbers of the worked sum; the point you aim at
  BLUE   = the lens and its numerical aperture
  RED    = the failure: "one blob", "one merged spot", "empty"
  TEAL   = a measured centre (a located position) in the localization scene
  GREY   = panels, axes, stamp, de-emphasised things
  TEXT   = a sum of two curves (what the detector actually records)
"""
import numpy as np
from scipy.special import j1
from bp_style import *  # noqa: F401,F403

D0 = 226.6       # lesson: lateral resolution at 520 nm, NA 1.40
D1 = 317.2       # lesson: lateral resolution at 520 nm, NA 1.00


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def airy(x, d=D0):
    """Intensity across one point's diffraction pattern; first dark ring at x = d (Rayleigh)."""
    v = 3.8317 * np.abs(np.asarray(x, float)) / d
    v = np.where(v < 1e-6, 1e-6, v)
    return (2 * j1(v) / v) ** 2


def curve(fn, x0, x1, ox, oy, sx, k, color, w=5, n=500, opacity=1.0):
    xs = np.linspace(x0, x1, n)
    pts = [[ox + x * sx, oy + k * float(fn(x)), 0] for x in xs]
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners(pts)
    m.set_stroke(opacity=opacity)
    return m


def glow(center, r, color=GREEN, stretch=1.0):
    """a blurred spot: stacked translucent discs."""
    g = VGroup()
    for f, o in zip([1.0, 0.8, 0.58, 0.36], [0.12, 0.25, 0.45, 0.75]):
        c = Circle(radius=r * f, stroke_width=0, fill_color=color, fill_opacity=o)
        c.stretch(stretch, 0)
        g.add(c)
    return g.move_to(center)


def airy_disc(center, s=1.0):
    """bright disc with faint rings (drawn picture of an Airy pattern, not to scale)."""
    g = VGroup(
        Circle(radius=1.15 * s, stroke_color=GREEN, stroke_width=2, stroke_opacity=0.25),
        Circle(radius=0.82 * s, stroke_color=GREEN, stroke_width=2.5, stroke_opacity=0.4),
        Circle(radius=0.5 * s, stroke_width=0, fill_color=GREEN, fill_opacity=0.85),
    )
    return g.move_to(center)


def bracket(x0, x1, y, color, tick=0.12, w=4):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w),
                  Line([x0, y - tick, 0], [x0, y + tick, 0], color=color, stroke_width=w),
                  Line([x1, y - tick, 0], [x1, y + tick, 0], color=color, stroke_width=w))


def axis(x0, x1, y, color=GREY):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def panel(cx, cy, w, h, color=GREY):
    return RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=3).move_to([cx, cy, 0])


class S00Title(TitleCard):
    LESSON = "Microscopy and Quantitative Images"
    TITLE = "Why Zooming Cannot Split Two Dots"


# ---------------------------------------------------------------------------------------------
class S01Blob(SpokenScene):
    """two vesicles 150 nm apart -> one blob; zoom only enlarges the blob."""

    def construct(self):
        P1, P2, Y = -3.9, 3.9, 0.2
        p1 = panel(P1, Y, 4.8, 4.4)
        p2 = panel(P2, Y, 4.8, 4.4)
        h1 = T("the sample", 24, GREY).move_to([P1, Y + 1.85, 0])
        h2 = T("the image", 24, GREY).move_to([P2, Y + 1.85, 0])
        v1 = Circle(radius=0.45, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.5).move_to([P1 - 0.75, Y, 0])
        v2 = v1.copy().move_to([P1 + 0.75, Y, 0])
        lab = T("two GFP vesicles", 26, GREEN).move_to([P1, Y + 1.05, 0])
        self.play(Create(p1), FadeIn(h1), run_time=0.6)
        self.at("Two vesicles")
        self.play(FadeIn(v1, scale=0.6), FadeIn(v2, scale=0.6), FadeIn(lab), run_time=0.7)
        br = bracket(P1 - 0.75, P1 + 0.75, Y - 0.85, YELLOW)
        d150 = M("150 nm", 28, YELLOW).move_to([P1, Y - 1.4, 0])
        self.at("apart")
        self.play(Create(br), FadeIn(d150), run_time=0.7)

        chipm = chip("light microscope", BLUE, size=22).move_to([0, Y + 0.85, 0])
        a = arr([-1.35, Y, 0], [1.35, Y, 0], BLUE)
        self.at("ordinary light")
        self.play(FadeIn(chipm, shift=DOWN * 0.1), GrowArrow(a), Create(p2), FadeIn(h2), run_time=0.8)
        blob = glow([P2, Y, 0], 1.0, GREEN, stretch=1.2)
        one = T("one blob", 30, RED, weight=BOLD).move_to([P2, Y - 1.72, 0])
        self.at("like one blob")
        self.play(FadeIn(blob, scale=0.8), FadeIn(one), run_time=0.8)

        zoom = chip("zoom in", YELLOW, size=22).move_to([0, Y - 0.85, 0])
        self.at("Zoom in")
        self.play(FadeIn(zoom, shift=UP * 0.1), run_time=0.4)
        self.play(blob.animate.scale(1.5).move_to([P2, Y + 0.15, 0]), run_time=1.2)
        self.at("only gets bigger")
        self.play(Indicate(one, color=RED, scale_factor=1.1), run_time=0.6)

        why = T("Why?", 48, YELLOW, weight=BOLD).move_to([0, Y - 1.95, 0])
        self.at("Why can you not")
        self.play(FadeIn(why, scale=0.8), run_time=0.5)
        prop = T("a property of light", 38, GREEN, font=TITLE_FONT).move_to([0, -3.0, 0])
        self.at("a property of light")
        self.play(Write(prop), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Stamp(SpokenScene):
    """a stamp makes a mark its own size; a lens turns a point into a disc with rings; close marks run together."""

    def construct(self):
        C = np.array([0.0, 0.2, 0])
        face = Circle(radius=1.5, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.25).move_to(C)
        face_l = T("soft, round stamp face", 26, GREY).move_to([0, -1.9, 0])
        self.at("rubber stamp")
        self.play(FadeIn(face, scale=0.9), FadeIn(face_l), run_time=0.8)
        pt = Dot(C, radius=0.09, color=YELLOW)
        pt_l = T("the point you aim at", 26, YELLOW).move_to([4.5, 0.2, 0])
        pt_a = arr([2.65, 0.2, 0], [0.2, 0.2, 0], YELLOW, w=3, tip=0.18)
        self.at("However small the point")
        self.play(FadeIn(pt, scale=3), FadeIn(pt_l), GrowArrow(pt_a), run_time=0.7)
        mark = glow(C, 1.5, GREEN)
        mark_l = T("the mark", 28, GREEN).move_to([-4.3, 0.2, 0])
        self.at("the mark is the size")
        self.play(FadeIn(mark, scale=0.5), FadeIn(mark_l), Indicate(face, color=GREY, scale_factor=1.04), run_time=1.0)
        self.add(pt)

        # the lens does the same
        self.at("A lens does the same")
        self.play(FadeOut(VGroup(face, face_l, mark, mark_l, pt_l, pt_a)), pt.animate.move_to([-5.0, 0.2, 0]), run_time=0.8)
        lens = Ellipse(width=0.7, height=3.2, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.25).move_to([-1.2, 0.2, 0])
        lens_l = T("lens", 28, BLUE).move_to([-1.2, -1.9, 0])
        pt_l2 = T("one point", 26, YELLOW).move_to([-5.0, -0.5, 0])
        a1 = arr([-4.6, 0.2, 0], [-1.75, 0.2, 0], GREY)
        a2 = arr([-0.65, 0.2, 0], [1.6, 0.2, 0], GREEN)
        self.play(FadeIn(lens, scale=0.9), FadeIn(lens_l), FadeIn(pt_l2), GrowArrow(a1), run_time=0.8)
        disc = airy_disc([4.2, 0.2, 0], 1.25)
        disc_l = T("the image of one point", 26, GREEN).move_to([4.2, -1.9, 0])
        self.at("bright")
        self.play(GrowArrow(a2), FadeIn(disc[2], scale=0.4), run_time=0.7)
        self.at("faint rings")
        self.play(FadeIn(disc[1]), FadeIn(disc[0]), run_time=0.7)
        ring_l = T("Airy pattern", 34, GREEN, font=TITLE_FONT).move_to([4.2, 2.3, 0])
        self.at("Airy pattern")
        self.play(FadeIn(ring_l, shift=DOWN * 0.1), FadeIn(disc_l), run_time=0.7)

        # two marks closer than one width
        self.at("Two marks closer")
        self.play(FadeOut(VGroup(lens, lens_l, pt, pt_l2, a1, a2, disc, disc_l, ring_l)), run_time=0.6)
        dA = airy_disc([-2.6, 0.2, 0], 1.25)
        dB = airy_disc([2.6, 0.2, 0], 1.25)
        self.play(FadeIn(dA), FadeIn(dB), run_time=0.5)
        self.play(dA.animate.move_to([-0.55, 0.2, 0]), dB.animate.move_to([0.55, 0.2, 0]), run_time=1.6)
        run = T("run together", 40, RED, weight=BOLD).move_to([0, -2.4, 0])
        self.at("run together")
        self.play(FadeIn(run, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rayleigh(SpokenScene):
    """two patterns add; resolved when one's centre sits on the other's first dark ring; d depends on wavelength and NA."""

    def construct(self):
        SX, OX, BASE, K = 0.0105, 0.0, -2.0, 2.6
        ax = axis(-5.9, 5.9, BASE)
        c = D0 / 2
        A = curve(airy, -550, 550, OX - c * SX, BASE, SX, K, GREEN, w=5)
        # curve centred at -c: shift by evaluating at x + c
        A = curve(lambda x: airy(x + c), -550, 550, OX, BASE, SX, K, GREEN, w=5)
        B = curve(lambda x: airy(x - c), -550, 550, OX, BASE, SX, K, GREEN, w=5)
        S = curve(lambda x: airy(x + c) + airy(x - c), -550, 550, OX, BASE, SX, K, TEXT, w=7)
        la = T("point A", 26, GREEN).move_to([-3.7, BASE + 1.0, 0])
        lb = T("point B", 26, GREEN).move_to([3.7, BASE + 1.0, 0])
        self.at("Two glowing points")
        self.play(Create(ax), run_time=0.5)
        self.play(Create(A), FadeIn(la), run_time=0.8)
        self.play(Create(B), FadeIn(lb), run_time=0.8)
        sumlab = T("what the detector records: the sum", 24, TEXT).move_to([0, BASE - 1.0, 0])
        self.at("their intensities add")
        self.play(A.animate.set_stroke(opacity=0.4), B.animate.set_stroke(opacity=0.4), Create(S), FadeIn(sumlab), run_time=1.4)

        # B's centre sits on A's first dark ring
        xb = c * SX
        ring_dot = Dot([xb, BASE, 0], radius=0.13, color=YELLOW)
        guide = DashedLine([xb, BASE, 0], [xb, BASE + K + 0.15, 0], color=YELLOW, stroke_width=3)
        ring_l = T("A's first dark ring = B's centre", 24, YELLOW).move_to([xb + 0.9, BASE - 0.45, 0])
        self.at("first dark ring")
        self.play(FadeIn(ring_dot, scale=2), Create(guide), FadeIn(ring_l), run_time=0.9)

        by = BASE + K + 0.85
        br = bracket(-c * SX, c * SX, by, YELLOW)
        dl = M("d", 36, YELLOW, weight=BOLD).move_to([0, by + 0.45, 0])
        self.at("That spacing")
        self.play(Create(br), FadeIn(dl), run_time=0.8)
        res = T("= the resolution", 26, YELLOW).next_to(dl, RIGHT, buff=0.2)
        self.at("is the resolution")
        self.play(FadeIn(res), run_time=0.5)

        # the two things d depends on
        wave = FunctionGraph(lambda t: 0.22 * np.sin(t * 6.0), x_range=[0, 2.6], color=GREEN, stroke_width=4).move_to([-4.6, 2.75, 0])
        wl = T("emission wavelength", 24, GREEN).move_to([-4.6, 2.1, 0])
        self.at("emission wavelength")
        self.play(Create(wave), FadeIn(wl), run_time=0.9)
        sp = Dot([3.0, 2.6, 0], radius=0.08, color=YELLOW)
        lens = Ellipse(width=0.4, height=1.4, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to([4.8, 2.6, 0])
        cone = VGroup(Line([3.0, 2.6, 0], [4.8, 3.3, 0], color=BLUE, stroke_width=3),
                      Line([3.0, 2.6, 0], [4.8, 1.9, 0], color=BLUE, stroke_width=3))
        na = T("numerical aperture", 24, BLUE).move_to([4.5, 1.3, 0])
        self.at("numerical aperture")
        self.play(FadeIn(sp), FadeIn(lens), Create(cone), FadeIn(na), run_time=0.9)
        self.at("how wide a cone")
        cone2 = VGroup(Line([3.0, 2.6, 0], [4.8, 3.6, 0], color=BLUE, stroke_width=3),
                       Line([3.0, 2.6, 0], [4.8, 1.6, 0], color=BLUE, stroke_width=3))
        lens2 = Ellipse(width=0.4, height=2.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to([4.8, 2.6, 0])
        self.play(Transform(cone, cone2), Transform(lens, lens2), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Numbers(SpokenScene):
    """d = 0.61 x 520 / 1.40 = 226.6 nm; NA 1.00 gives 317.2 nm."""

    def construct(self):
        LX = -6.1
        eq = M("d = 0.61 × wavelength / NA", 26, TEXT)
        eq.move_to([LX, 3.0, 0], aligned_edge=LEFT)
        eq.align_to([LX, 0, 0], LEFT)
        l1 = M("wavelength = 520 nm", 26, GREEN).align_to([LX, 0, 0], LEFT).set_y(2.15)
        l2 = M("NA = 1.40", 26, BLUE).align_to([LX, 0, 0], LEFT).set_y(1.45)
        l3 = M("d = 0.61 × 520 / 1.40", 26, TEXT).align_to([LX, 0, 0], LEFT).set_y(0.55)
        l4 = M("d = 317.2 / 1.40", 26, TEXT).align_to([LX, 0, 0], LEFT).set_y(-0.15)
        l5 = M("d = 226.6 nm", 38, YELLOW, weight=BOLD).align_to([LX, 0, 0], LEFT).set_y(-1.0)
        w1 = M("NA = 1.00", 26, BLUE).align_to([LX, 0, 0], LEFT).set_y(-2.0)
        w2 = M("d = 317.2 / 1.00 = 317.2 nm", 26, YELLOW).align_to([LX, 0, 0], LEFT).set_y(-2.7)
        w3 = T("about 90 nm lost", 28, RED).align_to([LX, 0, 0], LEFT).set_y(-3.3)

        CX, SX, BASE, K = 3.45, 0.0075, -1.5, 3.0
        ax = axis(CX - 2.85, CX + 2.85, BASE)
        c1 = curve(lambda x: airy(x, D0), -380, 380, CX, BASE, SX, K, GREEN, w=6)
        chip1 = chip("NA 1.40", BLUE, size=26).move_to([CX, 2.55, 0])

        self.at("Take light")
        self.play(FadeIn(eq, shift=RIGHT * 0.2), FadeIn(l1), run_time=0.8)
        self.at("oil lens")
        self.play(FadeIn(l2), FadeIn(chip1), Create(ax), run_time=0.8)
        self.at("The resolution is")
        self.play(FadeIn(l3, shift=RIGHT * 0.2), Create(c1), run_time=1.4)
        self.play(FadeIn(l4, shift=RIGHT * 0.2), run_time=0.7)

        zero_dot = Dot([CX + D0 * SX, BASE, 0], radius=0.12, color=YELLOW)
        br = bracket(CX, CX + D0 * SX, BASE - 0.45, YELLOW)
        bl = M("226.6 nm", 24, YELLOW).move_to([CX + D0 * SX / 2, BASE - 0.88, 0])
        ringl = T("to the first dark ring", 22, YELLOW).move_to([CX + 1.1, BASE - 1.3, 0])
        self.at("That is")
        self.play(FadeIn(l5, scale=0.9), FadeIn(zero_dot, scale=2), Create(br), FadeIn(bl), FadeIn(ringl), run_time=1.0)

        # weaker lens
        ghost = c1.copy().set_stroke(GREY, opacity=0.6, width=3)
        c2 = curve(lambda x: airy(x, D1), -380, 380, CX, BASE, SX, K, GREEN, w=6)
        chip2 = chip("NA 1.00", BLUE, size=26).move_to([CX, 2.55, 0])
        self.at("weaker lens")
        self.add(ghost)
        self.play(FadeIn(w1), ReplacementTransform(chip1, chip2), Transform(c1, c2), run_time=1.2)
        br2 = bracket(CX, CX + D1 * SX, BASE - 0.45, YELLOW)
        bl2 = M("317.2 nm", 24, YELLOW).move_to([CX + D1 * SX / 2, BASE - 0.9, 0])
        self.play(Transform(zero_dot, Dot([CX + D1 * SX, BASE, 0], radius=0.12, color=YELLOW)),
                  Transform(br, br2), Transform(bl, bl2), FadeIn(w2), run_time=1.0)
        self.at("Losing a little aperture")
        self.play(FadeIn(w3, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Merged(SpokenScene):
    """150 nm < 226.6 nm: two blurs add into one hump; enlarging only spreads it over more pixels."""

    def construct(self):
        SX, BASE, K = 0.0095, -1.3, 1.8
        ax = axis(-5.9, 5.9, BASE)
        nm = T("nm", 22, GREY).move_to([5.5, BASE - 0.32, 0])
        h = 75
        A = curve(lambda x: airy(x + h), -550, 550, 0, BASE, SX, K, GREEN, w=5, opacity=0.85)
        B = curve(lambda x: airy(x - h), -550, 550, 0, BASE, SX, K, GREEN, w=5, opacity=0.85)
        S = curve(lambda x: airy(x + h) + airy(x - h), -550, 550, 0, BASE, SX, K, TEXT, w=7)
        va = Circle(radius=0.14, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([-h * SX, BASE, 0])
        vb = va.copy().move_to([h * SX, BASE, 0])

        self.at("put the vesicles back")
        self.play(Create(ax), FadeIn(nm), FadeIn(va), FadeIn(vb), run_time=0.6)
        self.play(Create(A), Create(B), run_time=1.0)

        b150 = bracket(-h * SX, h * SX, 2.4, GREEN)
        l150 = M("vesicles 150 nm apart", 24, GREEN).move_to([h * SX + 2.7, 2.4, 0])
        self.at("apart")
        self.play(Create(b150), FadeIn(l150), run_time=0.7)
        c = D0 / 2
        b226 = bracket(-c * SX, c * SX, 3.05, YELLOW)
        l226 = M("resolution 226.6 nm", 24, YELLOW).move_to([c * SX + 2.7, 3.05, 0])
        self.at("closer than")
        self.play(Create(b226), FadeIn(l226), run_time=0.7)

        one = T("one spot", 32, RED, weight=BOLD).move_to([-3.6, 0.9, 0])
        self.at("overlap")
        self.play(A.animate.set_stroke(opacity=0.35), B.animate.set_stroke(opacity=0.35), Create(S), run_time=1.3)
        self.at("into one spot")
        self.play(FadeIn(one), Indicate(S, color=RED, scale_factor=1.04), run_time=0.7)

        # what the camera records: a row of pixels
        pit = 100
        pxs = [-300 + pit * i for i in range(7)]
        vals = [float(airy(x + h) + airy(x - h)) for x in pxs]
        vmax = max(vals)
        row_y, sq = -2.65, pit * SX
        row = VGroup(*[Rectangle(width=sq, height=0.8, stroke_color=GREY, stroke_width=2, fill_color=GREEN,
                                 fill_opacity=0.08 + 0.9 * v / vmax).move_to([x * SX, row_y, 0]) for x, v in zip(pxs, vals)])
        rl = T("camera pixels", 24, GREY).move_to([0, -3.35, 0])
        self.at("camera records")
        self.play(FadeIn(row), FadeIn(rl), run_time=0.8)

        # enlarge: the same spot over more, bigger-on-screen pixels
        fine = 21
        fx = np.linspace(-300 - pit / 2, 300 + pit / 2, fine + 1)
        fc = (fx[:-1] + fx[1:]) / 2
        fvals = np.interp(fc, pxs, vals)
        frow = VGroup(*[Rectangle(width=(fx[1] - fx[0]) * SX, height=0.8, stroke_color=GREY, stroke_width=1.5, fill_color=GREEN,
                                  fill_opacity=0.08 + 0.9 * v / vmax).move_to([x * SX, row_y, 0]) for x, v in zip(fc, fvals)])
        frow.stretch(1.65, 0).move_to([0, row_y, 0])
        rl2 = T("enlarged: more pixels, same spot", 24, YELLOW).move_to([0, -3.35, 0])
        self.at("Enlarge the picture")
        self.play(ReplacementTransform(row, frow), ReplacementTransform(rl, rl2), run_time=1.5)
        none = T("no new information", 30, RED, weight=BOLD).move_to([-3.9, 0.9, 0])
        self.at("no new information")
        self.play(ReplacementTransform(one, none), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Switch(SpokenScene):
    """switch on a sparse few at a time, find each blur's centre, plot the positions."""

    def construct(self):
        PX = [-4.2, 0.0, 4.2]
        PY, PW, PH = 1.75, 3.9, 2.8
        RY, RH = -1.95, 2.9
        mol = {"A": (-1.2, 0.1), "B": (-0.85, 0.1), "C": (0.2, 0.5), "D": (0.8, -0.5), "E": (1.3, 0.3), "F": (-0.2, -0.6)}
        cycles = [("A", "E"), ("B", "F"), ("C", "D")]
        cues = ["Switch on a sparse", "so that no two", "glow together"]

        panels = [panel(x, PY, PW, PH) for x in PX]
        ctitle = [T(f"cycle {i + 1}", 22, GREY).move_to([x - 1.2, PY + 1.15, 0]) for i, x in enumerate(PX)]
        offs = []
        for x in PX:
            offs.append({k: Dot([x + p[0], PY + p[1] - 0.15, 0], radius=0.07, color=GREY) for k, p in mol.items()})
        res = panel(0, RY, 12.4, RH)
        res_l = T("positions found", 22, TEAL).move_to([-4.85, RY + 1.15, 0])

        self.play(*[Create(p) for p in panels], run_time=0.7)
        self.play(*[FadeIn(t) for t in ctitle], *[FadeIn(d) for o in offs for d in o.values()], run_time=0.6)
        self.at("controlling which molecules")
        self.play(*[Indicate(d, color=GREEN, scale_factor=1.6) for o in offs for d in o.values()], run_time=1.0)

        allcr, allbl = [], []
        for i, (x, grp, cue) in enumerate(zip(PX, cycles, cues)):
            self.at(cue)
            blurs = [glow([x + mol[k][0], PY + mol[k][1] - 0.15, 0], 0.36, GREEN) for k in grp]
            self.play(*[FadeIn(b, scale=0.5) for b in blurs], run_time=0.5)
            for k, b in zip(grp, blurs):
                allbl.append((k, b))
        self.at("each blur")
        crs = {}
        for k, b in allbl:
            p = b.get_center()
            crs[k] = VGroup(Line(p + [-0.15, 0, 0], p + [0.15, 0, 0], color=TEAL, stroke_width=4),
                            Line(p + [0, -0.15, 0], p + [0, 0.15, 0], color=TEAL, stroke_width=4))
        self.play(*[Create(c) for c in crs.values()], run_time=0.5)
        a_x, b_x = mol["A"][0] * 2.2, mol["B"][0] * 2.2
        merged = VGroup(glow([a_x, RY - 0.1 + 0.15, 0], 0.7, GREEN), glow([b_x, RY - 0.1 + 0.15, 0], 0.7, GREEN))
        merged_l = T("wide blur, neighbours merged", 22, RED).move_to([a_x - 0.2, RY - 0.85, 0])
        self.play(FadeIn(res), FadeIn(res_l), FadeIn(merged), FadeIn(merged_l), run_time=0.5)
        found = {}
        moves = []
        for k, b in allbl:
            tx = mol[k][0] * 2.2
            ty = RY - 0.1 + mol[k][1] * 1.5
            found[k] = Dot([tx, ty, 0], radius=0.11, color=TEAL)
            moves.append(Transform(crs[k], found[k]))
        self.at("far more precisely")
        self.play(*moves, *[FadeOut(b) for _, b in allbl], run_time=1.2)
        self.remove(*crs.values())
        self.add(*found.values())
        self.at("Plot the positions")
        self.play(*[Indicate(f, color=TEAL, scale_factor=1.4) for f in found.values()], run_time=0.8)
        ga = bracket(found["A"].get_center()[0], found["B"].get_center()[0], RY - 0.5, TEAL)
        gl = T("close neighbours, apart", 24, TEAL).move_to([-3.0, RY - 0.95, 0])
        self.at("told apart")
        self.play(FadeOut(merged), FadeOut(merged_l), run_time=0.5)
        self.play(Create(ga), FadeIn(gl), run_time=0.8)
        self.at("Magnification without resolution")
        self.play(FadeOut(VGroup(*panels, *ctitle, *[d for o in offs for d in o.values()])), run_time=0.8)
        e = T("empty magnification", 44, RED, font=TITLE_FONT, weight=BOLD).move_to([0, 1.5, 0])
        self.play(FadeIn(e, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Magnification without resolution is empty magnification."
