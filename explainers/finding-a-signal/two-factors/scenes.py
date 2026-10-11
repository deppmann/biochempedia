"""Finding a signal: one crude extract, two hidden factors  (section film, Biochemistrypedia)

COLOR MAP (one color per concept, whole film)
  YELLOW = the crude extract (the mixture that is injected)
  BLUE   = nerve growth factor and its effect, the enlarged ganglia
  PURPLE = the second protein (epidermal growth factor) and its effects: eyelids, teeth, skin
  RED    = not seen / did not happen / not expected
  GREY   = the mouse, axes, labels, things that did not occur (dashed)
  TEXT   = plain labels
  GOLD   = the closing rule

The mouse is a simple shape (body, head, ear, tail). The ganglia are three blue dots inside it.
An eyelid is a short arc when closed and a ring with a dot when open. Teeth are two white blocks.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
BODY_C = np.array([-2.5, -0.5, 0])


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ghost(text, size=24, color=GREY):
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.34)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(color), t)


class Mouse:
    """A newborn mouse in simple shapes. Parts are kept so scenes can change them."""

    def __init__(self, B=BODY_C, k=1.25):
        self.B, self.k = np.array(B, float), k
        H = self.B + np.array([-1.9, 0.15, 0]) * k
        self.H = H
        self.body = Ellipse(width=3.4 * k, height=2.0 * k, stroke_color=GREY, stroke_width=3,
                            fill_color="#232733", fill_opacity=1).move_to(self.B)
        self.head = Circle(radius=0.9 * k, stroke_color=GREY, stroke_width=3,
                           fill_color="#232733", fill_opacity=1).move_to(H)
        self.ear = Circle(radius=0.3 * k, stroke_color=GREY, stroke_width=3,
                          fill_color="#232733", fill_opacity=1).move_to(H + np.array([0.55, 0.7, 0]) * k)
        p0 = self.B + np.array([1.7, 0.1, 0]) * k
        self.tail = CubicBezier(p0, p0 + np.array([0.5, 0.4, 0]) * k, p0 + np.array([0.6, -0.2, 0]) * k,
                                p0 + np.array([0.85, 0.3, 0]) * k, stroke_color=GREY, stroke_width=4)
        self.base = VGroup(self.tail, self.body, self.head, self.ear)
        self.eye_pos = H + np.array([-0.38, 0.25, 0]) * k
        self.ganglia_r = 0.13 * k
        self.ganglia_pos = [self.B + np.array([dx, 0.15, 0]) * k for dx in (-0.7, 0.0, 0.7)]

    def eye_closed(self):
        return Arc(radius=0.2 * self.k, start_angle=PI * 1.15, angle=PI * 0.7,
                   arc_center=self.eye_pos + np.array([0, 0.15 * self.k, 0]),
                   stroke_color=TEXT, stroke_width=5)

    def eye_open(self):
        ring = Circle(radius=0.17 * self.k, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9)
        dot = Dot(self.eye_pos, radius=0.08 * self.k, color=BG)
        return VGroup(ring.move_to(self.eye_pos), dot)

    def teeth(self):
        k = self.k
        a = Rectangle(width=0.13 * k, height=0.26 * k, stroke_width=0, fill_color=TEXT, fill_opacity=1)
        b = a.copy()
        a.move_to(self.H + np.array([-0.62, -0.78, 0]) * k)
        b.move_to(self.H + np.array([-0.42, -0.84, 0]) * k)
        return VGroup(a, b)

    def ganglia(self, scale=1.0, dashed=False):
        out = VGroup()
        for p in self.ganglia_pos:
            c = Circle(radius=self.ganglia_r * scale, stroke_color=BLUE, stroke_width=3,
                       fill_color=BLUE, fill_opacity=0 if dashed else 0.85).move_to(p)
            if dashed:
                c = DashedVMobject(c, num_dashes=14).set_color(BLUE)
            out.add(c)
        return out


def leader(a, b, color=GREY):
    return Line(a, b, color=color, stroke_width=3)


class S00Title(TitleCard):
    LESSON = "Finding a Signal: NGF, EGF and the Bioassay"
    TITLE = "One Extract, Two Hidden Factors"


class S01Inject(SpokenScene):
    def construct(self):
        m = Mouse()
        self.at("injected newborn")
        self.play(FadeIn(m.base), run_time=0.8)
        nb = T("newborn mouse", 24, GREY).move_to(m.B + [0, -1.55, 0])
        self.play(FadeIn(nb), run_time=0.4)
        top = m.B[1] + 1.25
        needle = Line([-2.3, top, 0], [-2.3, top + 0.55, 0], color=GREY, stroke_width=3)
        barrel = Rectangle(width=0.55, height=1.3, stroke_color=GREY, stroke_width=3,
                           fill_color=YELLOW, fill_opacity=0.5).move_to([-2.3, top + 0.55 + 0.65, 0])
        plunger = VGroup(Line([-2.3, top + 1.85, 0], [-2.3, top + 2.4, 0], color=GREY, stroke_width=4),
                         Line([-2.65, top + 2.4, 0], [-1.95, top + 2.4, 0], color=GREY, stroke_width=5))
        syr = VGroup(needle, barrel, plunger)
        self.at("every day")
        self.play(FadeIn(syr), run_time=0.3)
        ed = T("every day", 26, YELLOW).move_to([0.2, top + 1.2, 0])
        self.play(FadeIn(ed), run_time=0.2)
        for _ in range(1):
            dot = Dot([-2.3, top - 0.05, 0], radius=0.09, color=YELLOW)
            self.play(syr.animate.shift(DOWN * 0.18), FadeIn(dot), run_time=0.25)
            self.play(syr.animate.shift(UP * 0.18), dot.animate.shift(DOWN * 0.5).set_opacity(0), run_time=0.3)
        self.at("crude extract of")
        vial = RoundedRectangle(corner_radius=0.15, width=1.5, height=2.1, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.25).move_to([3.7, 1.0, 0])
        rng = np.random.RandomState(4)
        specks = VGroup(*[Dot(vial.get_center() + [rng.uniform(-0.5, 0.5), rng.uniform(-0.8, 0.8), 0],
                              radius=rng.uniform(0.05, 0.12), color=YELLOW) for _ in range(11)])
        vl = T("crude extract", 26, YELLOW).move_to([3.7, -0.5, 0])
        vl2 = T("male mouse salivary gland", 22, GREY).move_to([3.7, -1.0, 0])
        self.play(FadeIn(vial), FadeIn(specks), run_time=0.6)
        self.play(FadeIn(vl), FadeIn(vl2), run_time=0.4)
        self.at("mixture")
        box = SurroundingRectangle(specks, color=YELLOW, buff=0.1, stroke_width=3)
        mix = T("a mixture", 28, YELLOW).move_to([3.7, 2.55, 0])
        self.play(Create(box), FadeIn(mix), run_time=0.6)
        self.at("sympathetic ganglia")
        g = m.ganglia(1.0)
        gl = T("sympathetic ganglia", 26, BLUE).move_to([-2.5, -2.45, 0])
        ln = leader([-2.5, -2.15, 0], [-2.5, -1.45, 0], BLUE)
        self.play(FadeIn(g), FadeIn(gl), Create(ln), FadeOut(nb), run_time=0.6)
        self.at("should be enlarged")
        gh = m.ganglia(1.9, dashed=True)
        ex = T("expected: enlarged", 22, BLUE).move_to([-1.95, -1.05, 0])
        self.play(Create(gh), FadeIn(ex), run_time=0.8)
        self.at("and they were")
        gbig = m.ganglia(1.9)
        self.play(Transform(g, gbig), run_time=0.7)
        self.play(FadeOut(gh), FadeOut(ex), FadeOut(ln), FadeOut(box), run_time=0.4)
        self.play(Transform(gl, T("sympathetic ganglia: enlarged", 26, BLUE).move_to([-2.5, -2.45, 0])), run_time=0.4)
        self.finish()


def pup_with_ganglia():
    m = Mouse()
    g = m.ganglia(1.9)
    gl = T("sympathetic ganglia: enlarged", 26, BLUE).move_to([-2.5, -2.45, 0])
    return m, g, gl


class S02Surprise(SpokenScene):
    def construct(self):
        m, g, gl = pup_with_ganglia()
        eye = m.eye_closed()
        self.add(m.base, g, gl, eye)
        self.at("something else")
        q = T("?", 64, YELLOW).move_to(m.H + [0.2, 1.75, 0])
        self.play(FadeIn(q, scale=0.5), gl.animate.set_opacity(0.45), g.animate.set_opacity(0.5), run_time=0.5)
        x0, scale = 1.5, 0.3
        X = lambda d: x0 + d * scale
        axis = Line([X(0), 0.4, 0], [X(16), 0.4, 0], color=GREY, stroke_width=4)
        t0 = Line([X(0), 0.3, 0], [X(0), 0.5, 0], color=GREY, stroke_width=4)
        l0 = T("birth", 22, GREY).move_to([X(0), 0.0, 0])
        ad = T("days after birth", 22, GREY).move_to([X(8), -0.7, 0])
        self.at("eyelids")
        self.play(Indicate(eye, color=PURPLE, scale_factor=1.6), FadeOut(q), run_time=0.7)
        self.at("about seven days")
        self.play(Create(axis), Create(t0), FadeIn(l0), FadeIn(ad), run_time=0.6)
        mark = Dot([X(7), 0.4, 0], radius=0.17, color=PURPLE)
        ml = T("eyelids open: about 7", 24, PURPLE).move_to([X(5.0), 1.5, 0])
        mt = Line([X(7), 0.55, 0], [X(7), 1.15, 0], color=PURPLE, stroke_width=3)
        self.play(FadeIn(mark, scale=0.4), Create(mt), FadeIn(ml), Transform(eye, m.eye_open()), run_time=0.7)
        self.at("usual age")
        band = Rectangle(width=2 * scale, height=0.36, stroke_width=0, fill_color=GREY,
                         fill_opacity=0.7).move_to([X(13), 0.4, 0])
        bl = T("usual: 12 to 14", 22, GREY).move_to([X(13) - 0.1, 1.05, 0])
        self.play(FadeIn(band), FadeIn(bl), run_time=0.6)
        self.at("teeth also")
        te = m.teeth()
        tl = T("teeth through early", 24, PURPLE).move_to([X(8), -1.85, 0])
        tln = leader([X(3.2), -1.85, 0], m.H + [-0.5, -1.2, 0], PURPLE)
        self.play(FadeIn(te, scale=0.4), FadeIn(tl), Create(tln), run_time=0.7)
        self.at("neither of these")
        ne1 = T("not expected", 24, RED).move_to([X(10), -2.55, 0])
        ne2 = T("!", 54, RED, weight=BOLD).move_to([X(13) + 0.4, 1.75, 0])
        self.play(FadeIn(ne1), FadeIn(ne2, scale=0.5), run_time=0.5)
        self.finish()


class S03Second(SpokenScene):
    def construct(self):
        y1 = 2.4
        pn = chip("purified NGF alone", BLUE, size=24).move_to([-4.2, y1, 0])
        a1 = arr([-2.0, y1, 0], [-0.9, y1, 0])
        c1 = ghost("eyelids early", 24).move_to([1.0, y1, 0])
        c2 = ghost("teeth early", 24).move_to([4.2, y1, 0])
        self.at("purified nerve growth factor")
        self.play(FadeIn(pn, shift=RIGHT * 0.2), run_time=0.6)
        self.at("did none")
        self.play(GrowArrow(a1), FadeIn(c1), FadeIn(c2), run_time=0.5)
        self.play(Create(strike(c1)), Create(strike(c2)), run_time=0.5)
        ex = chip("crude extract", YELLOW, size=26).move_to([-4.9, -1.0, 0])
        ng = chip("nerve growth factor", BLUE, size=24).move_to([-0.6, -0.1, 0])
        sp = chip("second protein", PURPLE, size=24).move_to([-0.6, -2.1, 0])
        self.at("crude extract must")
        self.play(FadeIn(ex), run_time=0.5)
        self.play(GrowArrow(arr(ex.get_right() + [0.0, 0.2, 0], ng.get_left())), FadeIn(ng), run_time=0.6)
        self.at("second protein")
        a_sp = arr(ex.get_right() + [0.0, -0.2, 0], sp.get_left(), PURPLE)
        self.play(GrowArrow(a_sp), FadeIn(sp, scale=0.8), run_time=0.7)
        eff1 = chip("ganglia enlarged", BLUE, size=24).move_to([4.7, -0.1, 0])
        eff2 = chip("eyelids, teeth early", PURPLE, size=24).move_to([4.7, -2.1, 0])
        self.at("its own activity")
        a_e2 = arr(sp.get_right(), eff2.get_left(), PURPLE)
        self.play(GrowArrow(arr(ng.get_right(), eff1.get_left(), BLUE)), FadeIn(eff1),
                  GrowArrow(a_e2), FadeIn(eff2), run_time=0.8)
        self.at("acts on skin")
        sk = T("acts on skin", 24, PURPLE).move_to([-0.6, -3.1, 0])
        self.play(FadeIn(sk, shift=UP * 0.1), run_time=0.4)
        self.at("epidermal growth factor")
        egf = chip("epidermal growth factor (EGF)", PURPLE, size=24).move_to([-0.6, -2.1, 0])
        n1 = arr(ex.get_right() + [0.0, -0.2, 0], egf.get_left(), PURPLE)
        n2 = arr(egf.get_right(), eff2.get_left(), PURPLE)
        self.play(Transform(sp, egf), Transform(a_sp, n1), Transform(a_e2, n2), run_time=0.8)
        self.at("two activities")
        self.play(Indicate(eff1, color=BLUE, scale_factor=1.12), Indicate(eff2, color=PURPLE, scale_factor=1.12),
                  run_time=0.9)
        self.finish()


class S04Assay(SpokenScene):
    def construct(self):
        cx, cy = -3.4, 0.5
        title = T("halo assay", 30, BLUE, weight=BOLD).move_to([cx, 2.9, 0])
        gang = Circle(radius=0.45, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.85).move_to([cx, cy, 0])
        fibers = VGroup(*[Line([cx + 0.45 * np.cos(a), cy + 0.45 * np.sin(a), 0],
                               [cx + 1.45 * np.cos(a), cy + 1.45 * np.sin(a), 0], color=BLUE, stroke_width=3)
                          for a in np.linspace(0, TAU, 17)[:-1]])
        self.at("halo assay")
        self.play(FadeIn(title), FadeIn(gang), run_time=0.6)
        self.at("counted nerve fibers")
        cnt = T("counts nerve fibers", 24, BLUE).move_to([cx, 2.4, 0])
        self.play(LaggedStart(*[Create(f) for f in fibers], lag_ratio=0.05), FadeIn(cnt), run_time=1.0)
        self.at("could not show")
        egf = chip("EGF", PURPLE, size=26).move_to([cx, -2.15, 0])
        self.play(FadeIn(egf, shift=UP * 0.2), run_time=0.5)
        self.play(egf.animate.move_to([cx, -1.7, 0]), run_time=0.5)
        self.at("blind to epidermal")
        x = T("no response", 24, RED).move_to([cx, -2.65, 0])
        self.play(Create(strike(egf)), FadeIn(x), run_time=0.6)
        self.at("whole newborn mouse")
        m = Mouse(B=[3.5, -0.2, 0], k=0.95)
        wl = T("whole newborn mouse", 26, GREY).move_to([3.3, 1.9, 0])
        self.play(FadeIn(m.base), FadeIn(wl), run_time=0.7)
        g = m.ganglia(1.9)
        eye = m.eye_open()
        te = m.teeth()
        self.at("responds to everything")
        self.play(FadeIn(g), FadeIn(eye), FadeIn(te), run_time=0.7)
        self.play(Indicate(g, color=BLUE, scale_factor=1.15), Indicate(eye, color=PURPLE, scale_factor=1.4),
                  Indicate(te, color=PURPLE, scale_factor=1.4), run_time=0.9)
        self.at("assay you choose")
        rule = T("the assay decides which molecule you find", 30, GOLD).move_to([0.0, -3.35, 0])
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S05End(EndCard):
    LINE = "The assay you choose decides which molecule you find."
