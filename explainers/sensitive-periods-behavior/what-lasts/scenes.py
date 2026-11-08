"""Chapter 3 of 3, "What Lasts Is Not What Can Be Learned"  (Sensitive Periods in Behavior)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept; shared with chapters 1 and 2 and with scenes.old.py)
  TEAL   = the window: how open the young nervous system is = ABILITY to learn (curves, window shapes, "full speed" years)
  YELLOW = experience that arrives: sign, patterned light, the age at which input first comes, "arrives at 12"
  BLUE   = the learner and what LASTS: people, adult scores, the outcome curve, the outcome gauge
  GREEN  = native-like / normal outcome (native level lines, early-arrival points)
  RED    = impaired or short of the need (affected proficiency, deficit, shortfall)
  GREY   = structure: axes, ticks, labels, de-emphasised things
  PURPLE = (the memory of the tutor song: chapter 1 and 2 only, unused here)

Curves and bars are computed: the outcome curve from the pattern the lesson reports for Johnson and Newport
(native-like to about age 7, a steady fall to about puberty, then lower and variable); the learning-ability
curve from the toy model (full speed to 17, then much slower); the toy bars from 17 minus the starting age.
The 46 points of the study are an ILLUSTRATION of that reported pattern (the lesson gives no individual scores).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
LG = "#B9C1CE"      # light grey for text labels (axes stay GREY)
LBLUE = "#A8DCEC"   # lifted BLUE for small text on dark
PUB = 15          # "about puberty", where the early-arrival fall ends
RATE_AFTER = 0.2  # toy: learning runs at this fraction of full speed after 17


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bird(scale=1.0, color=BLUE):
    body = Ellipse(width=1.5, height=0.95, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to([0.62, 0.42, 0])
    beak = Polygon([0.93, 0.5, 0], [1.28, 0.4, 0], [0.93, 0.32, 0], stroke_color=YELLOW, stroke_width=3,
                   fill_color=YELLOW, fill_opacity=0.9)
    tail = Polygon([-0.65, 0.1, 0], [-1.4, 0.35, 0], [-1.3, -0.05, 0], stroke_color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.28)
    eye = Dot([0.72, 0.48, 0], radius=0.05, color=TEXT)
    legs = VGroup(Line([-0.1, -0.45, 0], [-0.1, -0.8, 0], color=color, stroke_width=4),
                  Line([0.2, -0.45, 0], [0.2, -0.8, 0], color=color, stroke_width=4))
    return VGroup(tail, body, head, beak, eye, legs).scale(scale)


def person(h=2.0, color=BLUE, arms="down", fill=0.3):
    """A simple person, feet on y=0, centred on x=0. arms: 'down' or 'sign' (hands raised, yellow)."""
    hr = 0.16 * h
    body = RoundedRectangle(corner_radius=0.12 * h, width=0.46 * h, height=0.62 * h, stroke_color=color,
                            stroke_width=4, fill_color=color, fill_opacity=fill).move_to([0, 0.31 * h, 0])
    head = Circle(radius=hr, stroke_color=color, stroke_width=4, fill_color=color,
                  fill_opacity=fill).move_to([0, 0.66 * h + hr, 0])
    parts = [body, head]
    for sx in (-1, 1):
        if arms == "down":
            parts.append(Line([sx * 0.23 * h, 0.54 * h, 0], [sx * 0.32 * h, 0.24 * h, 0], color=color, stroke_width=4))
        else:
            parts.append(Line([sx * 0.23 * h, 0.54 * h, 0], [sx * 0.42 * h, 0.84 * h, 0], color=color, stroke_width=4))
            parts.append(Dot([sx * 0.42 * h, 0.84 * h, 0], radius=0.045 * h, color=YELLOW))
    return VGroup(*parts)


def signs(at, flip=1, n=3, color=YELLOW):
    """Arcs radiating from a signing hand (flip=1 radiates to the left, -1 to the right)."""
    arcs = VGroup()
    for i in range(n):
        r = 0.28 + 0.24 * i
        a = Arc(radius=r, start_angle=(3 * PI / 4 if flip == 1 else -PI / 4), angle=PI / 2, color=color, stroke_width=4)
        arcs.add(a.move_arc_center_to(at))
    return arcs


def face(d, r=1.5, color=GREY):
    """A face: eyes fixed, the mouth a distance d below the eye line. Returns (face, eye_y, mouth_y)."""
    k = r / 1.15
    head = Circle(radius=r, stroke_color=color, stroke_width=4)
    ey = 0.35 * k
    eyes = VGroup(Dot([-0.4 * k, ey, 0], radius=0.11, color=TEXT), Dot([0.4 * k, ey, 0], radius=0.11, color=TEXT))
    mouth = Line([-0.3 * k, ey - d, 0], [0.3 * k, ey - d, 0], color=TEXT, stroke_width=5)
    return VGroup(head, eyes, mouth), ey, ey - d


def L(text, x, y, size=24, color=GREY, **kw):
    """Left-aligned label whose left edge sits at x."""
    return T(text, size, color, **kw).move_to([x, y, 0], aligned_edge=LEFT)


def credit(text, y=3.4, x=0.0, size=24):
    return chip(text, GREY, size, pad=0.16, fill_opacity=0.10).move_to([x, y, 0])


def clear(scene, t=0.35):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=t)


def poly(pts, color, sw=6):
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners([[x, y, 0] for x, y in pts])


# ---- the curves ------------------------------------------------------------------------------
def outcome(a):
    """What lasts: adult grammar score by age of arrival (the pattern the lesson reports), 0..1."""
    a = np.asarray(a, dtype=float)
    return np.where(a <= 7, 0.96, np.where(a >= PUB, 0.66, 0.96 - 0.30 * (a - 7) / (PUB - 7)))


def outcome_smooth(a):
    ag = np.linspace(2, 40, 400)
    og = outcome(ag)
    k = np.ones(25) / 25.0
    pad = np.pad(og, 12, mode="edge")
    sm = np.convolve(pad, k, mode="valid")
    return float(np.interp(a, ag, sm))


def ability(a):
    """Learning ability (toy): full speed to 17, then falling toward RATE_AFTER by about 30."""
    s = min(max((a - 17.0) / 13.0, 0.0), 1.0)
    return 1.0 - (1.0 - RATE_AFTER) * (3 * s * s - 2 * s ** 3)


def sample_age_curve(a):
    """A generic 'age curve' for the opening question: high, then falling (shape only)."""
    return 0.08 + 0.88 / (1.0 + np.exp((a - 17.0) / 5.5))


DOOR_HI, DOOR_LO, TIDE_LO = 0.96, 0.74, 0.60


def tide_f(a):
    return max(TIDE_LO, 0.96 - (0.96 - TIDE_LO) * (a - 3) / 21.0)


class Plot:
    """Age-of-arrival plot. X maps age 3..39, Y maps 0..1 onto the screen box."""

    def __init__(self, xl, xr, yb, yt):
        self.xl, self.xr, self.yb, self.yt = xl, xr, yb, yt

    def X(self, a):
        return self.xl + (a - 3) / 36.0 * (self.xr - self.xl)

    def Y(self, v):
        return self.yb + v * (self.yt - self.yb)

    def axes(self):
        return VGroup(Arrow([self.xl, self.yb, 0], [self.xr + 0.3, self.yb, 0], buff=0, color=GREY, stroke_width=3,
                            tip_length=0.2),
                      Arrow([self.xl, self.yb, 0], [self.xl, self.yt + 0.25, 0], buff=0, color=GREY, stroke_width=3,
                            tip_length=0.2))

    def ticks(self, ages=(3, 10, 17, 25, 39), hl=None):
        g = VGroup()
        for a in ages:
            c = TEAL if a == hl else LG
            g.add(Line([self.X(a), self.yb - 0.08, 0], [self.X(a), self.yb + 0.08, 0], color=GREY, stroke_width=3))
            g.add(M(str(a), 26, c).move_to([self.X(a), self.yb - 0.42, 0]))
        return g

    def xlab(self, text="age of arrival (years)"):
        return T(text, 26, LG).move_to([(self.xl + self.xr) / 2, self.yb - 1.0, 0])

    def ylab(self, text, color=LBLUE):
        return T(text, 26, color).rotate(PI / 2).move_to([self.xl - 0.72, (self.yb + self.yt) / 2, 0])

    def curve(self, f, color, sw=6, a0=3, a1=39, dashed=False):
        ages = np.arange(a0, a1 + 0.01, 0.25)
        m = poly([(self.X(a), self.Y(f(a))) for a in ages], color, sw)
        return DashedVMobject(m, num_dashes=max(8, int((a1 - a0) * 1.4))) if dashed else m


FULL = Plot(-5.4, 6.0, -2.45, 2.8)    # the one plot geometry for every age-of-arrival scene (s09 to s16)


def points46():
    """46 illustrative arrivals: 23 early (3-15), 23 late (17-39), following the reported pattern."""
    rs = np.random.RandomState(11)
    early = [3, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7, 7, 8, 9, 9, 10, 10, 11, 12, 12, 13, 14, 15]
    late = list(range(17, 40))
    pts = []
    for a in early:
        j = 0.012 if a <= 7 else 0.03
        pts.append((a, float(outcome(a)) + rs.uniform(-j, j)))
    for a in late:
        pts.append((a, float(np.clip(0.66 + rs.normal(0, 0.12), 0.32, 0.88))))
    return pts


def dots(P, pts, lo, hi):
    g = VGroup()
    for a, s in pts:
        if lo <= a <= hi:
            g.add(Dot([P.X(a), P.Y(s), 0], radius=0.1, color=GREEN if a <= 7 else BLUE))
    return g


class S00Title(NarratedScene):
    LESSON = "Sensitive Periods in Behavior: Song, Language and Sight"
    TITLE = "What Lasts Is Not What Can Be Learned"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32).move_to(ORIGIN)
        for m in g:
            m.set_x(0)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=0.6)
        self.wait(1.3)
        self.play(FadeOut(g), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
# Opening question and Lenneberg
# ---------------------------------------------------------------------------------------------
def window_bracket(cx, y, w, color=TEAL, dashed=False):
    pts = [(cx - w / 2, y - 0.3), (cx - w / 2, y), (cx + w / 2, y), (cx + w / 2, y - 0.3)]
    m = poly(pts, color, 8)
    return DashedVMobject(m, num_dashes=16) if dashed else m


class S01Q(SpokenScene):
    def construct(self):
        child = person(3.6, BLUE).move_to([-3.4, -2.4, 0], aligned_edge=DOWN)
        clab = T("people", 32, BLUE).move_to([-3.4, -3.0, 0])
        child.shift(UP * 0.05)
        b = bird(1.7).move_to([3.5, -0.75, 0])
        blab = T("songbird", 32, BLUE).move_to([3.5, -3.0, 0])
        bc = window_bracket(-3.4, 1.85, 2.4, TEAL, dashed=True)
        bb = window_bracket(3.5, 1.45, 3.4, TEAL)
        cw = T("window?", 34, TEAL).move_to([-3.4, 2.5, 0])
        bw = T("window", 34, TEAL).move_to([3.5, 2.1, 0])
        self.at("do people")
        self.play(FadeIn(child, shift=UP * 0.2), FadeIn(clab), run_time=0.6)
        self.at("have windows")
        self.play(Create(bc), FadeIn(cw), run_time=0.7)
        self.at("like a")
        self.play(FadeIn(b, shift=UP * 0.2), FadeIn(blab), Create(bb), FadeIn(bw), run_time=0.9)
        self.at("and what does", lead=0.6)
        clear(self, 0.2)
        ax = FULL
        axes = ax.axes()
        xl = T("age", 28, LG).move_to([(ax.xl + ax.xr) / 2, ax.yb - 0.7, 0])
        yl = ax.ylab("what lasts")
        crv = ax.curve(sample_age_curve, BLUE, 7, 3, 39)
        sch = T("an example shape", 26, LG).move_to([ax.X(30), ax.Y(0.62), 0])
        self.play(Create(axes), FadeIn(xl), FadeIn(yl), run_time=0.35)
        self.at("an age curve")
        self.play(Create(crv), FadeIn(sch), run_time=0.65)
        self.finish()


LA, LB = -4.4, 2.2      # Lenneberg window edges, big layout (age axis at y=-2.4)


def lenn_big():
    axis = Arrow([-6.2, -2.4, 0], [6.5, -2.4, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    rect = Rectangle(width=LB - LA, height=4.4, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                     fill_opacity=0.22).move_to([(LA + LB) / 2, -0.2, 0])
    l1 = T("early childhood", 28, TEAL).move_to([LA, -2.95, 0])
    l2 = T("puberty", 28, TEAL).move_to([LB, -2.95, 0])
    age = T("age", 28, LG).move_to([6.1, -2.95, 0])
    return axis, rect, l1, l2, age


def lenn_compact():
    axis = Arrow([-6.2, -3.05, 0], [6.5, -3.05, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    rect = Rectangle(width=LB - LA, height=0.5, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                     fill_opacity=0.22).move_to([(LA + LB) / 2, -2.8, 0])
    l1 = T("early childhood", 28, TEAL).move_to([LA, -3.55, 0])
    l2 = T("puberty", 28, TEAL).move_to([LB, -3.55, 0])
    age = T("age", 28, LG).move_to([6.1, -3.55, 0])
    return axis, rect, l1, l2, age


def lenn_cp():
    return T("critical period\nfor language", 40, TEAL).move_to([(LA + LB) / 2, 0.3, 0]).set_z_index(3)


class S02Lenneberg(SpokenScene):
    def construct(self):
        name = T("Eric Lenneberg,", 40, TEXT, font=TITLE_FONT)
        year = M("1967", 40, YELLOW)
        card = VGroup(name, year).arrange(RIGHT, buff=0.3).move_to([0, 3.3, 0])
        axis, rect, l1, l2, age = lenn_big()
        cp = lenn_cp()
        box = DashedVMobject(Rectangle(width=LB - LA, height=4.4, stroke_color=TEAL, stroke_width=3)
                             .move_to([(LA + LB) / 2, -0.2, 0]), num_dashes=40)
        edgeL = DashedLine([LA, -2.4, 0], [LA, 2.0, 0], color=TEAL, stroke_width=4)
        edgeR = DashedLine([LB, -2.4, 0], [LB, 2.0, 0], color=TEAL, stroke_width=4)
        self.at("1967")
        self.play(FadeIn(year, shift=UP * 0.1), Create(axis), FadeIn(age), run_time=0.8)
        self.at("eric lennyberg")
        self.play(FadeIn(name, shift=UP * 0.1), run_time=0.5)
        self.at("critical period for language")
        self.play(Create(box), FadeIn(cp), run_time=0.8)
        self.at("early childhood")
        self.play(Create(edgeL), FadeIn(l1), GrowFromEdge(rect, LEFT), run_time=0.9)
        self.at("to puberty")
        self.play(Create(edgeR), FadeIn(l2), run_time=0.6)
        self.remove(box)
        self.finish()


class S04Signers(SpokenScene):
    def construct(self):
        big = lenn_big()
        cp = lenn_cp()
        edges = VGroup(DashedLine([LA, -2.4, 0], [LA, 2.0, 0], color=TEAL, stroke_width=4),
                       DashedLine([LB, -2.4, 0], [LB, 2.0, 0], color=TEAL, stroke_width=4))
        self.add(*big, cp, edges)
        small = lenn_compact()
        self.play(*[Transform(b, c) for b, c in zip(big, small)], FadeOut(cp), FadeOut(edges), run_time=0.9)
        child = person(2.6, BLUE, "sign").move_to([-1.3, -1.75, 0], aligned_edge=DOWN)
        clab = T("deaf child", 30, BLUE).move_to([-1.3, 1.45, 0])
        pa = person(3.4, GREY).move_to([-5.6, -1.75, 0], aligned_edge=DOWN)
        pb = person(3.4, GREY).move_to([-4.0, -1.75, 0], aligned_edge=DOWN)
        plab = T("hearing parents", 30, LG).move_to([-4.8, 2.1, 0])
        teacher = person(3.4, GREEN, "sign").move_to([3.4, -1.75, 0], aligned_edge=DOWN)
        arcs = signs([3.4 - 0.42 * 3.4, -1.75 + 0.84 * 3.4, 0], flip=1)
        slab = T("signed language", 30, YELLOW).move_to([3.4, 2.3, 0])
        dots_ = VGroup(*[Dot([x, -3.05, 0], radius=0.15, color=YELLOW).set_z_index(5) for x in (-1.3, 0.7, 3.0, 5.2)])
        mlab = T("first sign exposure: late (varies)", 28, YELLOW).move_to([0.4, -2.3, 0])
        self.at("deaf children")
        self.play(FadeIn(child, shift=UP * 0.2), FadeIn(clab), run_time=0.6)
        self.at("of hearing parents")
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(plab), run_time=0.6)
        self.at("first meet a signed language")
        self.play(FadeIn(teacher, shift=UP * 0.2), FadeIn(slab), run_time=0.5)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), run_time=0.7)
        self.at("language late")
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots_], lag_ratio=0.15), FadeIn(mlab), run_time=0.8)
        self.finish()


class S05Access(SpokenScene):
    def construct(self):
        c1 = chip("delayed access to sign", YELLOW, 58, pad=0.34).move_to([0, 2.15, 0])
        arr = Arrow([0, 1.15, 0], [0, -0.05, 0], buff=0, color=RED, stroke_width=9, tip_length=0.38)
        c2 = chip("lower proficiency\nin adulthood", RED, 58, pad=0.34).move_to([0, -1.55, 0])
        c2[1].set_color("#FFAAA2")
        cr = credit("Newport, 1990", y=-3.35, size=42)
        cr[1].set_color(LG)
        self.play(FadeIn(c1, shift=UP * 0.15), FadeIn(cr), run_time=0.5)
        self.at("does affect")
        self.play(GrowArrow(arr), FadeIn(c2, shift=UP * 0.15), run_time=0.5)
        self.at("later proficiency")
        self.play(Indicate(c2[1], color="#FFAAA2", scale_factor=1.03), run_time=0.6)
        self.finish()


# ---- Mayberry: two timelines on the left, the bars on the right -----------------------------
XA, XR, XS = -6.4, 2.3, -0.2          # row start, row end, the age at which both learned sign
YA, YB = 1.5, -1.6                    # the two timeline axes
XE, XL_A = XA + 3.7, XA + 1.0         # English ends (row B), hearing lost early (row A)
BASEY = -1.2                          # baseline of the bars


def mayberry():
    d = {}
    d["axA"] = Arrow([XA, YA, 0], [XR, YA, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    d["axB"] = Arrow([XA, YB, 0], [XR, YB, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    d["tk"] = VGroup(*[T(s, 26, LG).move_to([x, y - 0.4, 0], aligned_edge=LEFT if s == "birth" else RIGHT)
                       for s, x, y in (("birth", XA, YA), ("age", XR, YA), ("birth", XA, YB), ("age", XR, YB))])
    d["hA"] = T("sign as first language", 30, TEXT).move_to([XA, 2.85, 0], aligned_edge=LEFT)
    d["hB"] = T("sign as second language", 30, TEXT).move_to([XA, -0.35, 0], aligned_edge=LEFT)
    d["noA"] = VGroup(DashedVMobject(Rectangle(width=XS - XA, height=0.7, stroke_color=LG, stroke_width=3)
                                     .move_to([(XA + XS) / 2, YA + 0.4, 0]), num_dashes=44),
                      T("no accessible language", 26, LG).move_to([(XA + XS) / 2, YA + 0.4, 0]))
    d["enB"] = VGroup(Rectangle(width=XE - XA, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                                fill_opacity=0.35).move_to([(XA + XE) / 2, YB + 0.4, 0]),
                      T("English", 26, LBLUE).move_to([(XA + XE) / 2, YB + 0.4, 0]))
    d["mk"] = VGroup(Dot([XS, YA, 0], radius=0.16, color=YELLOW), Dot([XS, YB, 0], radius=0.16, color=YELLOW))
    d["same"] = VGroup(DashedLine([XS, YA - 0.15, 0], [XS, YB + 0.15, 0], color=YELLOW, stroke_width=3),
                       T("learned sign at the same age", 28, YELLOW).move_to([XS + 0.2, 0.35, 0], aligned_edge=LEFT))
    d["lostB"] = VGroup(Line([XE, YB - 0.12, 0], [XE, YB + 0.85, 0], color=RED, stroke_width=6),
                        T("lost hearing", 26, RED).move_to([XE + 0.12, YB - 0.4, 0], aligned_edge=LEFT))
    d["lostA"] = VGroup(Line([XL_A, YA - 0.12, 0], [XL_A, YA + 0.85, 0], color=RED, stroke_width=6),
                        T("lost hearing", 26, RED).move_to([XL_A + 0.12, YA - 0.4, 0], aligned_edge=LEFT))
    d["cr"] = credit("Mayberry, 1993", y=3.3, x=4.5, size=28)
    return d


class S06Mayberry(SpokenScene):
    def construct(self):
        d = mayberry()
        self.at("mayberry")
        self.play(FadeIn(d["cr"]), Create(d["axA"]), Create(d["axB"]), FadeIn(d["tk"]), run_time=0.8)
        self.at("adults")
        self.play(FadeIn(d["hA"]), FadeIn(d["hB"]), run_time=0.6)
        self.at("learned sign")
        self.play(FadeIn(d["mk"], scale=2), run_time=0.5)
        self.at("same age")
        self.play(Create(d["same"]), run_time=0.8)
        self.at("some already had english")
        self.play(FadeIn(d["noA"]), FadeIn(d["enB"]), run_time=0.9)
        self.at("before losing")
        self.play(FadeIn(d["lostB"], shift=UP * 0.1), run_time=0.6)
        self.finish()


def mayberry_bars():
    bA = Rectangle(width=1.2, height=1.9, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.5)
    bB = Rectangle(width=1.2, height=3.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5)
    bA.move_to([3.95, BASEY + 0.95, 0])
    bB.move_to([5.85, BASEY + 1.75, 0])
    labs = VGroup(T("sign as\nfirst\nlanguage", 26, TEXT).move_to([3.95, BASEY - 0.95, 0]),
                  T("sign as\nsecond\nlanguage", 26, TEXT).move_to([5.85, BASEY - 0.95, 0]))
    ttl = VGroup(T("sign proficiency", 26, LG).move_to([4.95, 3.4, 0]), T("(schematic)", 26, LG).move_to([4.95, 2.95, 0]))
    ax = VGroup(Line([3.1, BASEY, 0], [6.6, BASEY, 0], color=GREY, stroke_width=3),
                Arrow([3.1, BASEY, 0], [3.1, 2.7, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2))
    return bA, bB, labs, ttl, ax


def card_missing():
    return T("missing early language, not only age", 36, TEXT, font=TITLE_FONT).move_to([0, -3.35, 0])


def ctrl_note():
    return T("not a perfect control", 30, GOLD).move_to([-3.2, -2.95, 0])


class S07Mayberry2(SpokenScene):
    def construct(self):
        d = mayberry()
        for k in ("axA", "axB", "tk", "hA", "hB", "noA", "enB", "mk", "same", "lostB", "cr"):
            self.add(d[k])
        bA, bB, labs, ttl, ax = mayberry_bars()
        ctrl = ctrl_note()
        card = card_missing()
        self.at("those with no accessible language")
        self.play(Indicate(d["noA"], color=TEXT, scale_factor=1.03), run_time=0.9)
        self.at("did worse")
        self.play(FadeOut(d["cr"]), FadeOut(d["same"]), FadeIn(ttl), Create(ax), run_time=0.5)
        self.play(GrowFromEdge(bA, DOWN), GrowFromEdge(bB, DOWN), FadeIn(labs), run_time=0.9)
        self.at("differed in when")
        self.play(FadeIn(d["lostA"], shift=UP * 0.1), run_time=0.7)
        self.at("not a perfect control")
        self.play(FadeIn(ctrl), run_time=0.6)
        self.at("missing early language")
        self.play(FadeOut(ctrl), run_time=0.3)
        self.play(FadeIn(card, shift=UP * 0.1), run_time=0.7)
        self.at("leaves a lasting mark")
        self.play(Indicate(bA, color=RED, scale_factor=1.06), run_time=0.9)
        self.finish()


class S08Beat(NarratedScene):
    def construct(self):
        d = mayberry()
        for k in ("axA", "axB", "tk", "hA", "hB", "noA", "enB", "mk", "lostB", "lostA"):
            self.add(d[k])
        bA, bB, labs, ttl, ax = mayberry_bars()
        self.add(bA, bB, labs, ttl, ax, card_missing())
        self.wait(1.6)
        clear(self, 0.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
# Johnson and Newport
# ---------------------------------------------------------------------------------------------
def fullplot_base(P=FULL, ylab="adult grammar score"):
    return P.axes(), P.ticks(), P.xlab(), P.ylab(ylab)


class S09Jn(SpokenScene):
    def construct(self):
        P = FULL
        axes, ticks, xl, yl = fullplot_base()
        cr = credit("Johnson and Newport, 1989", y=3.35, size=34)
        info = VGroup(T("46 adults", 52, BLUE, weight=BOLD),
                      T("first language Korean or Chinese", 32, TEXT)).arrange(DOWN, buff=0.25).move_to([0.4, 0.2, 0])
        self.play(FadeIn(cr, shift=DOWN * 0.1), Create(axes), run_time=0.7)
        self.at("english grammar")
        self.play(FadeIn(yl), run_time=0.6)
        self.at("adults who")
        self.play(FadeIn(info, shift=UP * 0.1), run_time=0.7)
        self.at("in the united")
        self.play(FadeIn(xl), run_time=0.5)
        self.at("ages 3 to 39")
        self.play(FadeIn(ticks, lag_ratio=0.15), run_time=1.0)
        self.finish()


def ghost_state(P=FULL):
    door = VGroup(P.curve(lambda a: DOOR_HI, BLUE, 5, 3, PUB, True),
                  DashedLine([P.X(PUB), P.Y(DOOR_HI), 0], [P.X(PUB), P.Y(DOOR_LO), 0], color=BLUE, stroke_width=5),
                  P.curve(lambda a: DOOR_LO, BLUE, 5, PUB, 39, True))
    tide = P.curve(tide_f, BLUE, 5, 3, 39, True)
    pub = VGroup(DashedLine([P.X(PUB), P.yb, 0], [P.X(PUB), P.Y(1.0) + 0.15, 0], color=GREY, stroke_width=2),
                 L("puberty", P.X(PUB) + 0.12, P.yb + 0.5, 26, LG))
    labs = VGroup(T("hold, then drop", 26, LBLUE).move_to([P.X(31), P.Y(DOOR_LO) + 0.4, 0]),
                  T("fall earlier", 26, LBLUE).move_to([P.X(31), P.Y(TIDE_LO) - 0.4, 0]))
    poss = VGroup(T("possible adult scores (an outcome, not learning ability)", 28, TEXT).move_to([0.3, 3.45, 0]),
                  )
    guess = T("dashed curves are guesses", 26, LG).move_to([0.3, 3.0, 0])
    q = T("?", 64, GOLD, weight=BOLD).move_to([P.X(36.5), (P.Y(DOOR_LO) + P.Y(TIDE_LO)) / 2 + 0.03, 0])
    return door, tide, pub, labs, VGroup(poss, guess), q


class S10Pq(SpokenScene):
    def construct(self):
        P = FULL
        axes, ticks, xl, yl = fullplot_base()
        self.add(axes, ticks, xl, yl)
        door, tide, pub, labs, poss, q = ghost_state()
        pr = T("Predict", 48, GOLD, font=TITLE_FONT).move_to([0.3, 3.4, 0])
        self.at("predict")
        self.play(FadeIn(pr, shift=UP * 0.1), run_time=0.5)
        self.at("plot adult grammar scores")
        self.play(Indicate(yl, color=TEXT, scale_factor=1.08), Indicate(xl, color=TEXT, scale_factor=1.08),
                  FadeOut(pr), run_time=0.9)
        self.play(FadeIn(poss), run_time=0.6)
        self.at("scores hold")
        self.play(Create(door[0]), run_time=0.9)
        self.at("until puberty")
        self.play(Create(pub), run_time=0.6)
        self.at("then drop")
        self.play(Create(door[1]), Create(door[2]), FadeIn(labs[0]), run_time=1.0)
        self.at("or fall earlier")
        self.play(Create(tide), run_time=1.0)
        self.play(FadeIn(labs[1]), FadeIn(q, scale=0.7), run_time=0.5)
        self.finish()


def countdown(scene, n=5, lab_at=(0.0, -1.0), num_at=(2.5, -1.0), label="pause and predict"):
    """One visible number per second, so the pause reads as a pause."""
    lab = T(label, 30, GOLD).move_to([lab_at[0], lab_at[1], 0])
    scene.play(FadeIn(lab), run_time=0.01)
    for i in range(n, 0, -1):
        num = M(str(i), 64, GOLD, weight=BOLD).move_to([num_at[0], num_at[1], 0])
        scene.play(FadeIn(num, scale=1.3), run_time=0.2)
        scene.wait(0.6)
        scene.play(FadeOut(num), run_time=0.2)


class S11Pause(NarratedScene):
    def construct(self):
        axes, ticks, xl, yl = fullplot_base()
        door, tide, pub, labs, poss, q = ghost_state()
        self.add(axes, ticks, xl, yl, door, tide, pub, labs, q)
        qt = T("Do scores hold until puberty, then drop? Or fall earlier?", 32, TEXT, font=TITLE_FONT).move_to([0.3, 3.4, 0])
        fit(qt, max_w=12.2)
        self.play(FadeIn(qt, shift=DOWN * 0.1), run_time=0.4)
        countdown(self, 5, lab_at=(1.4, -0.9), num_at=(4.3, -0.9))
        self.finish()


def jn_static(P=FULL):
    axes, ticks, xl, yl = fullplot_base()
    pts = points46()
    nat = VGroup(DashedLine([P.xl, P.Y(0.96), 0], [P.xr, P.Y(0.96), 0], color=GREEN, stroke_width=3),
                 T("native speakers", 26, GREEN).move_to([P.xr - 1.5, P.Y(0.96) + 0.34, 0]))
    pub = VGroup(DashedLine([P.X(PUB), P.yb, 0], [P.X(PUB), P.Y(1.0) + 0.15, 0], color=GREY, stroke_width=2),
                 T("about puberty", 26, LG).move_to([P.X(PUB), P.Y(1.0) + 0.52, 0]))
    sch = T("schematic, not the study's data", 26, GOLD).move_to([6.5, 3.62, 0], aligned_edge=RIGHT)
    return axes, ticks, xl, yl, pts, nat, pub, sch


class S12Rev(SpokenScene):
    def construct(self):
        P = FULL
        axes, ticks, xl, yl, pts, nat, pub, sch = jn_static()
        self.add(axes, ticks, xl, yl, sch)
        early, mid = dots(P, pts, 3, 7), dots(P, pts, 8, 15)
        hl = RoundedRectangle(corner_radius=0.2, width=P.X(7) - P.X(3) + 0.8, height=0.7, stroke_color=GREEN,
                              stroke_width=3).move_to([(P.X(3) + P.X(7)) / 2, P.Y(0.96), 0])
        hl_lab = T("arrived at 3 to 7", 26, GREEN).move_to([(P.X(3) + P.X(7)) / 2 + 1.0, P.Y(0.96) - 0.72, 0])
        self.at("early arrivals")
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in early], lag_ratio=0.12), Create(hl), FadeIn(hl_lab),
                  run_time=1.3)
        self.at("like native speakers")
        self.play(Create(nat), run_time=0.9)
        self.at("then scores fell")
        self.play(FadeOut(hl), FadeOut(hl_lab), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in mid], lag_ratio=0.2), run_time=2.4)
        self.at("up to about puberty")
        self.play(Create(pub), run_time=0.8)
        self.finish()


def legend_rows(P=FULL):
    y1, y2 = P.Y(0.2), P.Y(0.07)
    x0 = P.X(17) + 0.2
    r1 = VGroup(DashedLine([x0, y1, 0], [x0 + 0.8, y1, 0], color=BLUE, stroke_width=5),
                L("hold, then drop (a guess)", x0 + 1.0, y1, 26, LBLUE))
    r2 = VGroup(DashedLine([x0, y2, 0], [x0 + 0.8, y2, 0], color=BLUE, stroke_width=5),
                L("fall from childhood (a guess)", x0 + 1.0, y2, 26, LBLUE))
    return r1, r2


class S13Rev2(SpokenScene):
    def construct(self):
        P = FULL
        axes, ticks, xl, yl, pts, nat, pub, sch = jn_static()
        self.add(axes, ticks, xl, yl, nat, pub, dots(P, pts, 3, 15), sch)
        late = dots(P, pts, 17, 39)
        ys = [P.Y(s) for a, s in pts if a >= 17]
        band = RoundedRectangle(corner_radius=0.25, width=P.X(39) - P.X(17) + 0.7, height=max(ys) - min(ys) + 0.3,
                                stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.16)
        band.move_to([(P.X(17) + P.X(39)) / 2, (max(ys) + min(ys)) / 2, 0])
        vw = T("varied widely", 32, TEXT, weight=BOLD).move_to([P.X(30), P.Y(0.2), 0])
        door, tide, _, _, _, _ = ghost_state()
        door.set_stroke(color=LBLUE, opacity=0.65)
        tide.set_stroke(opacity=0.5)
        r1, r2 = legend_rows()
        fit_curve = P.curve(outcome_smooth, BLUE, 7, 3, 39)
        lab = T("what lasts,\nnot learning\nability", 28, LBLUE).move_to([P.X(8.5), P.Y(0.27), 0])
        self.at("later arrivals")
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in late], lag_ratio=0.08), run_time=2.0)
        self.at("varied widely")
        self.add(vw)  # Full contrast as soon as the variability box starts appearing.
        self.play(FadeIn(band), run_time=0.6)
        self.at("outcome curve")
        self.play(FadeOut(band), FadeOut(vw), FadeIn(door), FadeIn(tide), FadeIn(r1), FadeIn(r2), run_time=0.9)
        self.at("falling from childhood")
        self.play(Transform(tide, fit_curve), door.animate.set_stroke(opacity=0.4), r1.animate.set_opacity(0.65),
                  r2[1].animate.set_color(TEXT), FadeIn(lab), run_time=1.3)
        self.finish()


class S14Beat(NarratedScene):
    def construct(self):
        P = FULL
        axes, ticks, xl, yl, pts, nat, pub, sch = jn_static()
        allp = dots(P, pts, 3, 39)
        curve = P.curve(outcome_smooth, BLUE, 7, 3, 39)
        lab = T("what lasts,\nnot learning\nability", 28, LBLUE).move_to([P.X(8.5), P.Y(0.27), 0])
        door, tide, _, _, _, _ = ghost_state()
        door.set_stroke(color=LBLUE, opacity=0.4)
        r1, r2 = legend_rows()
        r1.set_opacity(0.65)
        r2[1].set_color(TEXT)
        self.add(axes, ticks, xl, yl, nat, pub, allp, door, curve, lab, sch, r1, r2)
        self.wait(2.0)
        clear(self, 0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# Hartshorne and the toy
# ---------------------------------------------------------------------------------------------
ABIL_LAB = "grammar-learning ability"


def hart_base():
    P = FULL
    return P.axes(), P.ticks(hl=17), P.xlab("age (years)"), P.ylab(ABIL_LAB, TEAL)


def ability_curve_parts(P, label=True):
    flat = P.curve(ability, TEAL, 7, 3, 17)
    drop = P.curve(ability, TEAL, 7, 17, 39)
    mark = VGroup(DashedLine([P.X(17), P.yb, 0], [P.X(17), P.Y(1.0), 0], color=TEAL, stroke_width=2))
    if label:
        mark.add(T("about 17", 26, TEAL).move_to([P.X(17), P.Y(1.0) + 0.38, 0]))
    return flat, drop, mark


def people_block(P):
    return VGroup(T("about", 28, LG), M("670,000", 52, LBLUE), T("people", 34, TEXT)).arrange(DOWN, buff=0.12) \
        .move_to([P.X(9.2), P.Y(0.34), 0])


class S15Hart(SpokenScene):
    def construct(self):
        P = FULL
        axes, ticks, xl, yl = hart_base()
        flat, drop, mark = ability_curve_parts(P)
        cr = chip("Hartshorne, Tenenbaum\nand Pinker, 2018", LG, 28, pad=0.2, fill_opacity=0.10).move_to([4.0, 3.2, 0])
        people = people_block(P)
        sch = T("curve after 17: schematic", 26, LG).move_to([P.xr - 0.1 - 2.4, P.Y(0.07), 0])
        self.play(FadeIn(cr), Create(axes), FadeIn(ticks), FadeIn(xl), FadeIn(yl),
                  FadeIn(people, shift=UP * 0.1), run_time=0.5)
        self.at("grammar learning ability")
        self.play(Create(flat), run_time=0.9)
        self.at("stays high")
        self.play(Indicate(flat, color=TEAL, scale_factor=1.0), run_time=0.5)
        self.at("until about")
        self.play(Create(mark), run_time=0.5)
        self.at("17")
        self.play(Create(drop), FadeIn(sch), Indicate(ticks[5], color=TEAL, scale_factor=1.4), run_time=0.9)
        self.finish()


def child_state(P):
    ch = person(2.2, YELLOW).move_to([P.X(12), P.yb + 0.03, 0], aligned_edge=DOWN)
    up = DashedLine([P.X(12), P.yb + 2.35, 0], [P.X(12), P.Y(ability(12)) - 0.05, 0], color=YELLOW, stroke_width=3)
    cl = T("arrives\nat 12", 28, YELLOW).move_to([P.X(12) - 1.55, P.yb + 1.3, 0])
    return ch, up, cl


def gauge_state(P=FULL):
    cx = P.X(36.3)
    ytop, ybot = P.Y(1.0) - 0.15, P.Y(0.40)
    track = RoundedRectangle(corner_radius=0.2, width=1.0, height=ytop - ybot, stroke_color=BLUE, stroke_width=3) \
        .move_to([cx, (ytop + ybot) / 2, 0])
    nat = VGroup(DashedLine([cx - 0.75, ytop - 0.2, 0], [cx + 0.75, ytop - 0.2, 0], color=GREEN, stroke_width=4),
                 T("native level", 26, GREEN).move_to([cx - 2.1, ytop - 0.2, 0]))
    qm = T("?", 80, BLUE, weight=BOLD).move_to([cx, (ytop + ybot) / 2 - 0.2, 0])
    ttl = T("final grammar\nscore", 26, LBLUE).move_to([cx - 1.95, (ytop + ybot) / 2 - 0.55, 0])
    return track, nat, qm, ttl


class S16Pq(SpokenScene):
    def construct(self):
        P = FULL
        axes, ticks, xl, yl = hart_base()
        flat, drop, mark = ability_curve_parts(P)
        cr = chip("Hartshorne, Tenenbaum\nand Pinker, 2018", LG, 28, pad=0.2, fill_opacity=0.10).move_to([4.0, 3.2, 0])
        people = people_block(P)
        sch = T("curve after 17: schematic", 26, LG).move_to([P.xr - 0.1 - 2.4, P.Y(0.07), 0])
        self.add(axes, ticks, xl, yl, flat, drop, mark, cr, people, sch)
        ch, up, cl = child_state(P)
        track, nat, qm, ttl = gauge_state(P)
        fl = T("full learning\nability", 28, TEAL).move_to([P.X(12) - 1.5, P.Y(0.80), 0])
        self.play(FadeOut(cr), FadeOut(people), FadeOut(sch), run_time=0.3)
        self.at("12 year old")
        self.play(FadeIn(ch, shift=UP * 0.2), run_time=0.6)
        self.at("arrive with")
        self.play(Create(up), FadeIn(cl), run_time=0.7)
        self.at("full learning ability")
        self.play(FadeIn(fl), Indicate(flat, color=TEAL, scale_factor=1.0), run_time=0.8)
        self.at("end below")
        self.play(Create(track), FadeIn(ttl), FadeIn(qm, scale=0.7), run_time=0.8)
        self.at("native level")
        self.play(Create(nat[0]), FadeIn(nat[1]), run_time=0.6)
        self.finish()


class S17Pause(NarratedScene):
    def construct(self):
        P = FULL
        axes, ticks, xl, yl = hart_base()
        flat, drop, mark = ability_curve_parts(P, label=False)
        ch, up, cl = child_state(P)
        track, nat, qm, ttl = gauge_state(P)
        fl = T("full learning\nability", 28, TEAL).move_to([P.X(12) - 1.5, P.Y(0.80), 0])
        self.add(axes, ticks, xl, yl, flat, drop, mark, ch, up, cl, track, nat, qm, ttl, fl)
        qt = T("How can a 12-year-old arrive with full learning ability,\nyet end below native level?", 30, TEXT,
               font=TITLE_FONT).move_to([-0.6, 3.45, 0])
        self.play(FadeIn(qt, shift=DOWN * 0.1), run_time=0.4)
        countdown(self, 5, lab_at=(1.3, -2.0), num_at=(4.0, -2.0))
        self.finish()


# ---- the toy bars ----------------------------------------------------------------------------
BARX = [-4.4, -2.2, 0.0, 2.2, 4.4]
STARTS = [5, 10, 12, 14, 25]
BASE = -1.9
UNIT = 0.36
DIM_FILL, DIM_STROKE, DIM_TXT = 0.2, 0.4, 0.4
TOY_CAP = "toy: does not reproduce the early decline or the spread"


def full_years(s):
    return max(0, 17 - s)


def bar_rect(i, years, opacity=0.5):
    h = max(years, 0.001) * UNIT
    return Rectangle(width=1.3, height=h, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                     fill_opacity=opacity).move_to([BARX[i], BASE + h / 2, 0])


def bar_labels():
    return VGroup(*[T(f"starts\nat {s}", 26, LG).move_to([BARX[i], BASE - 0.6, 0]) for i, s in enumerate(STARTS)])


def bar_numbers():
    return VGroup(*[M(str(full_years(s)), 32, TEXT).move_to([BARX[i], BASE + (full_years(s) * UNIT - 0.34 if full_years(s) else 0.34), 0])
                    for i, s in enumerate(STARTS)])


def toy_note():
    return T("a toy calculation, not data", 26, LG).move_to([6.5, 3.45, 0], aligned_edge=RIGHT)


def toy_heading():
    return VGroup(L("full-speed years before 17", -6.5, 3.45, 32, TEAL),
                  L("(ability stays at full speed until 17)", -6.5, 2.95, 26, TEAL))


def toy_axis():
    return Line([-5.6, BASE, 0], [5.6, BASE, 0], color=GREY, stroke_width=3)


def seven_line():
    y = BASE + 7 * UNIT
    return VGroup(DashedLine([-5.6, y, 0], [5.6, y, 0], color=YELLOW, stroke_width=4),
                  T("7 years needed (toy)", 26, YELLOW).move_to([4.5, y + 0.36, 0]))


def toy_cap():
    return T(TOY_CAP, 26, LG).move_to([0, -3.5, 0])


class S18Rev(SpokenScene):
    def construct(self):
        ax = toy_axis()
        labs = bar_labels()
        nums = bar_numbers()
        bars = [bar_rect(i, full_years(s)) for i, s in enumerate(STARTS)]
        h = toy_heading()
        note = toy_note()
        line = seven_line()
        self.add(ax)
        self.play(FadeIn(h), FadeIn(note), run_time=0.01)
        self.at("grammar takes years")
        self.play(FadeIn(labs[0]), GrowFromEdge(bars[0], DOWN), run_time=1.6)
        self.play(FadeIn(nums[0]), run_time=0.3)
        self.at("a later starter")
        self.play(FadeIn(labs[1:]), run_time=0.7)
        self.at("fewer full speed")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1:4]], lag_ratio=0.35), run_time=1.1)
        self.play(FadeIn(nums[1:]), run_time=0.3)
        self.at("before the slowdown")
        self.play(Create(line), run_time=0.9)
        self.finish()


def toy_state():
    ax = toy_axis()
    labs, nums = bar_labels(), bar_numbers()
    bars = [bar_rect(i, full_years(s)) for i, s in enumerate(STARTS)]
    return ax, labs, nums, bars, toy_heading(), toy_note(), seven_line()


def dim_others(bars, nums, labs, keep=2):
    for i in range(len(bars)):
        if i != keep:
            bars[i].set_stroke(opacity=DIM_STROKE).set_fill(opacity=DIM_FILL)
            nums[i].set_opacity(DIM_TXT)
            labs[i].set_opacity(DIM_TXT)
    bars[keep].set_fill(opacity=0.9)


def short_arrow(y_lo, y_hi, label, x=1.05, sw=7, size=28, ly=None):
    return VGroup(DoubleArrow([x, y_lo, 0], [x, y_hi, 0], buff=0, color=RED, stroke_width=sw, tip_length=0.23, max_tip_length_to_length_ratio=0.4,
                             max_stroke_width_to_length_ratio=30),
                  T(label, size, RED).move_to([x + 0.3, ly if ly is not None else (y_lo + y_hi) / 2 + 0.02, 0], aligned_edge=LEFT))


class S18bToy(SpokenScene):
    def construct(self):
        ax, labs, nums, bars, h, note, line = toy_state()
        self.add(ax, labs, nums, *bars, h, note, line)
        y7, y5 = BASE + 7 * UNIT, BASE + 5 * UNIT
        brace = short_arrow(y5, y7, "2 years short")
        cap = toy_cap()
        self.at("as a toy")
        self.play(FadeIn(cap), run_time=0.5)
        self.at("seven full speed years")
        self.play(Indicate(line[0], color=TEXT, scale_factor=1.0), Indicate(line[1], color=TEXT, scale_factor=1.15), run_time=0.9)
        self.at("a 12 year old")
        self.play(*[b.animate.set_stroke(opacity=DIM_STROKE).set_fill(opacity=DIM_FILL) for i, b in enumerate(bars) if i != 2],
                  *[n.animate.set_opacity(DIM_TXT) for i, n in enumerate(nums) if i != 2],
                  *[l.animate.set_opacity(DIM_TXT) for i, l in enumerate(labs) if i != 2],
                  bars[2].animate.set_fill(opacity=0.9), run_time=0.7)
        self.at("gets only")
        self.play(Indicate(nums[2], color=TEAL, scale_factor=1.5), run_time=0.7)
        self.play(Create(brace), run_time=0.7)
        self.finish()


class S18cLasts(SpokenScene):
    def construct(self):
        ax, labs, nums, bars, h, note, line = toy_state()
        dim_others(bars, nums, labs)
        y5, y6, y7 = BASE + 5 * UNIT, BASE + 6 * UNIT, BASE + 7 * UNIT
        brace = short_arrow(y5, y7, "2 years short")
        cap = toy_cap()
        self.add(ax, labs, nums, *bars, h, note, line, brace, cap)
        ext = Rectangle(width=1.3, height=UNIT, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                        fill_opacity=0.9).move_to([0, y5 + UNIT / 2, 0])
        ext.set_fill(color=interpolate_color(ManimColor(TEAL), ManimColor("#FFFFFF"), 0.35), opacity=0.95)
        slow = VGroup(T("17 on: slow", 30, TEAL).move_to([-1.15, y5 - 0.6, 0], aligned_edge=RIGHT),
                      Line([-1.1, y5 - 0.4, 0], [-0.7, y5 + UNIT / 2, 0], color=TEAL, stroke_width=4))
        short2 = short_arrow(y6, y7, "still short", x=1.0, sw=10, size=32, ly=y7 + 1.0)
        short2.add(Line([1.0, y7, 0], [1.0, y7 + 0.78, 0], color=RED, stroke_width=4))
        self.at("later learning is slow")
        self.play(FadeOut(brace), GrowFromEdge(ext, DOWN), FadeIn(slow), run_time=1.1)
        self.at("that shortfall lasts")
        self.play(Create(short2), run_time=0.5)
        self.play(Indicate(short2[1], color=RED, scale_factor=1.15), run_time=0.6)
        self.finish()


# ---- what lasts and ability on stacked, aligned panels ---------------------------------------
PT = Plot(-5.4, 6.0, 0.75, 3.0)     # top panel: what lasts
PB = Plot(-5.4, 6.0, -2.25, -0.2)   # bottom panel: ability to learn


def stack_base():
    axT = PT.axes()
    axB = PB.axes()
    ticks = PB.ticks(hl=17)
    xl = PB.xlab("age of arrival (years)")
    xl.move_to([(PB.xl + PB.xr) / 2, PB.yb - 1.0, 0])
    mark = DashedLine([PB.X(17), PB.yb, 0], [PT.Y(1.0) + 0.1, PT.Y(1.0) + 0.1, 0], color=TEAL, stroke_width=2)
    mark = DashedLine([PB.X(17), PB.yb, 0], [PB.X(17), PT.Y(1.0) + 0.1, 0], color=TEAL, stroke_width=2)
    labT = PT.ylab("adult grammar score", LBLUE)
    labB = PB.ylab("learning ability", TEAL)
    sch = T("all shapes schematic", 26, GOLD).move_to([6.5, 3.45, 0], aligned_edge=RIGHT)
    return axT, axB, ticks, xl, mark, labT, labB, sch


def stack_curves():
    ou = PT.curve(outcome_smooth, BLUE, 7, 3, 39)
    ab = PB.curve(ability, TEAL, 7, 3, 39)
    dot7 = Dot([PT.X(7), PT.Y(0.96), 0], radius=0.14, color=BLUE)
    fall = VGroup(T("starts to fall", 28, LBLUE).move_to([PT.X(9.3), PT.Y(0.52), 0]),
                  Arrow([PT.X(8.0), PT.Y(0.65), 0], [PT.X(7.2), PT.Y(0.9), 0], buff=0, color=LBLUE, stroke_width=3, tip_length=0.15))
    return ou, ab, dot7, fall


class S19Rev2(SpokenScene):
    def construct(self):
        axT, axB, ticks, xl, mark, labT, labB, sch = stack_base()
        ou, ab, dot7, fall = stack_curves()
        self.play(Create(axT), Create(axB), FadeIn(ticks), FadeIn(xl), FadeIn(sch), run_time=0.45)
        self.at("what lasts")
        self.play(Create(ou), FadeIn(labT), run_time=0.7)
        self.at("start to fall")
        self.play(FadeIn(dot7, scale=2), FadeIn(fall), run_time=0.5)
        self.at("ability to learn")
        self.play(Create(ab), Create(mark), FadeIn(labB), run_time=1.0)
        self.finish()


class S20Point(SpokenScene):
    def construct(self):
        axT, axB, ticks, xl, mark, labT, labB, sch = stack_base()
        ou, ab, dot7, fall = stack_curves()
        self.add(axT, axB, ticks, xl, mark, labT, labB, ou, ab, dot7, fall)
        card = T("A curve of what lasts is not a curve of learning ability", 32, TEXT, font=TITLE_FONT).move_to([0, 3.5, 0])
        fit(card, max_w=12.2)
        self.at("a curve of what lasts", lead=0)
        self.wait(0.2)  # Title begins strictly inside s20, after the scene boundary.
        self.play(FadeIn(card, shift=DOWN * 0.1), ab.animate.set_stroke(opacity=0.3), labB.animate.set_opacity(0.3),
                  Indicate(ou, color=BLUE, scale_factor=1.0), run_time=0.9)
        self.at("a curve of learning ability")
        self.play(ab.animate.set_stroke(opacity=1), labB.animate.set_opacity(1), ou.animate.set_stroke(opacity=0.3),
                  labT.animate.set_opacity(0.3), run_time=0.8)
        self.at("why learning slows")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not card], run_time=0.3)
        sub = T("possible reasons", 30, LG).move_to([0, 2.15, 0])
        c1 = chip("changes in plasticity", TEAL, 38, pad=0.25).move_to([0, 0.95, 0])
        c2 = chip("an entrenched first language", BLUE, 38, pad=0.25).move_to([0, -0.45, 0])
        c3 = chip("differences in input", YELLOW, 38, pad=0.25).move_to([0, -1.85, 0])
        self.play(FadeIn(sub), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in (c1, c2, c3)], lag_ratio=0.3), run_time=0.7)
        self.at("still debated")
        deb = T("still debated", 36, GOLD, font=TITLE_FONT).move_to([0, -3.2, 0])
        self.play(FadeIn(deb, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# Sight
# ---------------------------------------------------------------------------------------------
def eye_parts(c, r=1.4, dense=False):
    """A schematic eye (light comes from the left): outline, cornea, lens, retina."""
    cx, cy = c
    ball = Arc(radius=r, start_angle=-PI + 0.6, angle=2 * PI - 1.2,
                   color=LG, stroke_width=4).move_arc_center_to([cx, cy, 0])
    cornea = VMobject(stroke_color=TEXT, stroke_width=6)
    cornea.start_new_path(np.array([cx - r * np.cos(0.6), cy + r * np.sin(0.6), 0]))
    cornea.add_cubic_bezier_curve_to([cx - r * 1.3, cy + r * 0.45, 0],
                                     [cx - r * 1.3, cy - r * 0.45, 0],
                                     [cx - r * np.cos(0.6), cy - r * np.sin(0.6), 0])
    retina = Arc(radius=r, start_angle=-PI / 3, angle=2 * PI / 3, color=RED, stroke_width=11).move_arc_center_to([cx, cy, 0])
    lens = Ellipse(width=0.42 * r, height=0.95 * r, stroke_color=LG, stroke_width=4, fill_color=LG, fill_opacity=0.95 if dense else 0.0) \
        .move_to([cx - r * 0.5, cy, 0])
    return VGroup(ball, cornea, retina, lens)


class S21Sight(SpokenScene):
    def construct(self):
        cr = credit("Maurer, Lewis, Brent and Levin, 1999", y=3.4, size=30)
        r = 1.55
        e1 = (-4.95, 0.2)
        e2 = (-1.4, 0.2)
        g1 = eye_parts(e1, r, dense=True)
        g2 = eye_parts(e2, r, dense=False)
        lab_cornea = T("cornea", 26, TEXT).move_to([e1[0] - 1.25, 2.55, 0])
        lab_lens = T("lens", 26, LG).move_to([e1[0] + 0.05, 2.55, 0])
        lab_ret = T("retina", 26, RED).move_to([e1[0] + 1.6, 2.55, 0])
        ld1 = Line([e1[0] - 1.3, 2.3, 0], [e1[0] - r * 0.93, e1[1] + 0.55, 0], color=TEXT, stroke_width=2)
        ld2 = Line([e1[0] + 0.0, 2.3, 0], [e1[0] - r * 0.5, e1[1] + 0.6, 0], color=LG, stroke_width=2)
        ld3 = Line([e1[0] + 1.5, 2.3, 0], [e1[0] + r * 0.87, e1[1] + 0.7, 0], color=RED, stroke_width=2)
        parts = VGroup(lab_cornea, lab_lens, lab_ret, ld1, ld2, ld3)
        st1 = T("before:\ndense cataract", 28, LG).move_to([e1[0], -2.0, 0])
        bars = VGroup(*[Rectangle(width=0.15, height=1.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95)
                        .move_to([e2[0] + 0.15 + i * 0.36, e2[1], 0]) for i in range(3)])
        st2 = T("after treatment:\npatterned light\nreaches the retina", 28, YELLOW).move_to([e2[0] + 0.1, -2.3, 0])
        P = Plot(1.6, 6.4, -2.4, 2.4)
        axes = P.axes()
        base_y = -0.55
        nl = VGroup(DashedLine([1.6, base_y, 0], [6.4, base_y, 0], color=LG, stroke_width=3),
                    T("newborn level", 26, LG).move_to([5.0, base_y - 0.38, 0]))
        ylab = T("acuity (schematic)", 26, TEAL).rotate(PI / 2).move_to([0.85, 0.0, 0])
        t0 = T("treatment", 26, LG).move_to([2.4, -2.95, 0])
        t1 = T("1 hour", 26, YELLOW).move_to([5.7, -2.95, 0])
        start = Dot([2.0, base_y, 0], radius=0.14, color=TEAL)
        rise = poly([(2.0 + 3.7 * t, base_y + 1.0 * (1 - np.exp(-3 * t))) for t in np.linspace(0, 1, 40)], TEAL, 7)
        rl = T("some improvement", 28, TEAL).move_to([4.0, 1.55, 0])
        self.play(FadeIn(cr), run_time=0.5)
        self.at("infants treated")
        big_eye = g1.copy().scale(1.45).move_to([0, 0, 0])
        big_parts = parts.copy().shift(RIGHT * 4.95)
        big_parts[3].put_start_and_end_on([-1.3, 2.3, 0], big_eye[1].point_from_proportion(0.3))
        big_parts[4].put_start_and_end_on([0.0, 2.3, 0], big_eye[3].get_top())
        big_parts[5].put_start_and_end_on([1.5, 2.3, 0], big_eye[2].point_from_proportion(0.7))
        self.play(Create(big_eye), FadeIn(big_parts), run_time=0.7)
        self.at("dense cataracts")
        big_st1 = st1.copy().move_to([0, -2.8, 0])
        self.play(FadeIn(big_st1), run_time=0.4)
        self.at("showed some improvement")
        g1.set_stroke(opacity=0.4)
        g1[3].set_fill(opacity=0.4)
        st1.set_opacity(0.55)
        self.play(Transform(big_eye, g1), FadeOut(big_parts), FadeOut(big_st1), FadeIn(st1),
                  Create(g2), FadeIn(bars), FadeIn(st2), run_time=0.9)
        self.remove(big_eye)
        self.add(g1)
        self.at("in acuity")
        self.play(Create(axes), FadeIn(ylab), FadeIn(nl), FadeIn(start, scale=2), FadeIn(t0), run_time=0.8)
        self.at("after as little as")
        self.play(FadeIn(t1), run_time=0.3)
        self.play(Create(rise), run_time=1.0)
        self.play(FadeIn(rl), run_time=0.4)
        self.finish()


def windows_state():
    AX0, AX1 = -4.3, 6.4
    y_ax = -2.75
    ax = Arrow([AX0, y_ax, 0], [AX1, y_ax, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    xl = T("developmental age", 26, LG).move_to([(AX0 + AX1) / 2, -3.4, 0])
    yl = T("sensitivity to deprivation", 26, TEAL).rotate(PI / 2).move_to([-4.95, -0.2, 0])
    yarrow = Arrow([AX0, y_ax, 0], [AX0, 2.6, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    base1 = DashedLine([AX0, -0.05, 0], [AX1 - 0.3, -0.05, 0], color=GREY, stroke_width=2)
    g = lambda t, c, s: float(np.exp(-((t - c) / s) ** 2))

    def bell(y0, c, s, amp):
        pts = [(AX0 + 0.2 + 10.4 * i / 100, y0 + amp * g(i / 100, c, s)) for i in range(101)]
        return poly(pts, TEAL, 7)

    w1 = bell(-0.05, 0.2, 0.11, 2.4)
    w2 = bell(y_ax, 0.55, 0.2, 2.4)
    l1 = T("acuity", 32, TEAL).move_to([AX0 + 0.2 + 10.4 * 0.2 + 1.75, 1.9, 0])
    l2 = T("facial-feature spacing", 32, TEAL).move_to([-2.0, -0.75, 0])
    sch = T("shapes and timing are schematic", 26, GOLD).move_to([0.8, 3.35, 0])
    return ax, xl, yl, yarrow, base1, w1, w2, l1, l2, sch


class S22Sight2(SpokenScene):
    def construct(self):
        fa, eya, mya = face(1.0, r=2.1)
        fb, eyb, myb = face(1.7, r=2.1)
        fy = 0.5
        fa.move_to([-4.55, fy, 0])
        fb.move_to([-0.15, fy, 0])
        arrs = VGroup(*[DoubleArrow([x, fy + e, 0], [x, fy + m, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.14)
                        for x, e, m in ((-4.55, eya, mya), (-0.15, eyb, myb))])
        cap = T("same features, different spacing", 30, LG).move_to([-2.35, -2.6, 0])
        early = chip("early deprivation", YELLOW, 30, pad=0.22).move_to([4.65, 2.5, 0])
        arr = Arrow([4.65, 1.8, 0], [4.65, 0.75, 0], buff=0, color=LG, stroke_width=5, tip_length=0.25)
        yl_ = T("years later", 28, LG).move_to([4.9, 1.3, 0], aligned_edge=LEFT)
        imp = VGroup(chip("face-spacing\nprocessing:\nstill impaired", RED, 30, pad=0.26).move_to([4.65, -0.35, 0]),
                     T("(some functions)", 26, LG).move_to([4.65, -2.0, 0]))
        ax, xl, yl, yarrow, base1, w1, w2, l1, l2, sch = windows_state()
        head = T("separate windows", 42, TEXT, font=TITLE_FONT).move_to([0.8, 3.45, 0])
        sch.move_to([0.8, 2.85, 0])
        self.play(FadeIn(fa), FadeIn(fb), FadeIn(early), run_time=0.5)
        self.at("processing of the spacing")
        self.play(Create(arrs), FadeIn(cap), run_time=0.8)
        self.at("stayed impaired")
        self.play(GrowArrow(arr), FadeIn(imp, shift=UP * 0.1), run_time=0.6)
        self.at("impaired years later")
        self.play(FadeIn(yl_), run_time=0.5)
        self.at("separate abilities")
        clear(self, 0.3)
        self.play(Create(ax), Create(yarrow), FadeIn(xl), FadeIn(yl), Create(base1), Create(w1), FadeIn(l1),
                  Create(w2), FadeIn(l2), run_time=0.8)
        self.at("separate windows")
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(sch), run_time=0.6)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        rows = []
        for y, txt, col in [(1.6, "What input arrives?", YELLOW), (0.0, "At what age?", TEAL), (-1.6, "What lasts?", BLUE)]:
            dot = Dot([-4.6, y, 0], radius=0.28, color=col)
            t = T(txt, 50, TEXT, font=TITLE_FONT).move_to([-3.9, y, 0], aligned_edge=LEFT)
            rows.append(VGroup(dot, t))
        self.at("what input arrives")
        self.play(FadeIn(rows[0], shift=RIGHT * 0.3), run_time=0.6)
        self.at("at what age")
        self.play(FadeIn(rows[1], shift=RIGHT * 0.3), run_time=0.6)
        self.at("and what lasts")
        self.play(FadeIn(rows[2], shift=RIGHT * 0.3), run_time=0.6)
        self.finish()


class S24End(EndCard):
    LINE = "Ask what input arrives, at what age, and what lasts."
