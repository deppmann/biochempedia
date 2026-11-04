"""Sensitive periods in behavior, chapter 2: Who Closes the Window?  (Biochemistrypedia chapter film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole chapter; the first seven are the lesson's map from scenes.old.py)
  TEAL   = the window (how open the young nervous system is to experience) and the age clock that would set it
  YELLOW = experience that arrives: a tutor, the song heard, glutamate released onto the receiving cell
  PURPLE = the memory of the tutor song (not used in this chapter: where the memory is stored is not shown)
  BLUE   = the young bird, its own song, the motor pathway
  GREEN  = a normal or good outcome, "yes, copies", ions flowing
  RED    = an impaired outcome, something crossed out or blocked (AP5, magnesium plug, lesion)
  GREY   = structure, axes, membranes, de-emphasized things
  ORANGE = the anterior forebrain loop (HVC, area X, thalamus, LMAN) and its region        (new in this chapter)
  PINK   = the helper molecule, the co-agonist (glycine or D-serine)                         (new in this chapter)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#E8985E"
PINK = "#E58FB8"
RECEPTOR = "#9FB3C8"


# ---------------------------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------------------------
def bird(scale=1.0, color=BLUE, flip=False):
    """A finch from simple shapes, facing right (flip=True faces left)."""
    body = Ellipse(width=1.5, height=0.95, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to([0.62, 0.42, 0])
    beak = Polygon([0.93, 0.5, 0], [1.28, 0.4, 0], [0.93, 0.32, 0], stroke_color=YELLOW, stroke_width=3,
                   fill_color=YELLOW, fill_opacity=0.9)
    tail = Polygon([-0.65, 0.1, 0], [-1.4, 0.35, 0], [-1.3, -0.05, 0], stroke_color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.28)
    eye = Dot([0.72, 0.48, 0], radius=0.05, color=TEXT)
    legs = VGroup(Line([-0.1, -0.45, 0], [-0.1, -0.8, 0], color=color, stroke_width=4),
                  Line([0.2, -0.45, 0], [0.2, -0.8, 0], color=color, stroke_width=4))
    g = VGroup(tail, body, head, beak, eye, legs).scale(scale)
    if flip:
        g.flip(UP)
    return g


def sing(g, left=False, color=YELLOW, scale=1.0, n=3):
    """Sound arcs in front of the beak of bird g."""
    beak = g[3].get_left() if left else g[3].get_right()
    base = PI if left else 0
    return VGroup(*[Arc(radius=(0.3 + 0.27 * i) * scale, start_angle=base - 0.6, angle=1.2, arc_center=beak,
                        color=color, stroke_width=4) for i in range(n)])


def wave(x0, y, L, fn, color, amp=0.4, w=4):
    return ParametricFunction(lambda t: np.array([x0 + t, y + amp * fn(t), 0]), t_range=[0, L, 0.03],
                              color=color, stroke_width=w)


def rich(t):
    return (0.55 + 0.45 * np.sin(2.1 * t)) * np.sin(9.0 * t) + 0.25 * np.sin(23 * t + 1)


def simple(t):
    return 0.55 * np.sin(7.0 * t)


def rambling(t):
    return 0.8 * np.sin(5.0 * t + 0.8) * np.cos(17 * t) + 0.35 * np.sin(31 * t + 2) + 0.2 * np.sin(2.3 * t)


def canary(t):
    return 0.7 * np.sin(15 * t) * np.sin(2.4 * t) + 0.2 * np.sin(33 * t)


def check(at, color=GREEN, s=0.2, w=7):
    c = VMobject(stroke_color=color, stroke_width=w)
    c.set_points_as_corners([[-s, 0, 0], [-s * 0.3, -s * 0.75, 0], [s * 1.1, s * 0.9, 0]])
    return c.move_to(at)


def cross(at, color=RED, s=0.2, w=7):
    return VGroup(Line([-s, -s, 0], [s, s, 0], color=color, stroke_width=w),
                  Line([-s, s, 0], [s, -s, 0], color=color, stroke_width=w)).move_to(at)


def lines(*txt, size=22, color=TEXT, align=ORIGIN, buff=0.1, font=FONT):
    """Several short lines of text stacked (centered by default, or aligned LEFT)."""
    return VGroup(*[T(t, size, color, font=font) for t in txt]).arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, buff=0.05, w=4):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=buff, color=color, stroke_width=w, tip_length=0.2)


def clock(r=1.0, color=TEAL):
    """Clock face; parts: [0] face, [1] ticks, [2] minute hand, [3] hour hand."""
    face = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.14)
    ticks = VGroup(*[Line(UP * r * 0.82, UP * r * 0.95, stroke_width=3, color=GREY).rotate(-k * PI / 6, about_point=ORIGIN)
                     for k in range(12)])
    hm = Line(ORIGIN, UP * r * 0.7, color=color, stroke_width=5)
    hh = Line(ORIGIN, UP * r * 0.45, color=color, stroke_width=6).rotate(-PI / 3, about_point=ORIGIN)
    return VGroup(face, ticks, hm, hh)


def sweep(clk, turns=1.0, t=1.0):
    return Rotate(clk[2], angle=-turns * TAU, about_point=clk[0].get_center(), rate_func=linear, run_time=t)


# ---------------------------------------------------------------------------------------------
# cards
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Sensitive Periods in Behavior: Song, Language and Sight"
    TITLE = "Who Closes the Window?"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32).move_to(ORIGIN)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        title = T("Who closes the window?", 42, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
        adult = bird(1.0, YELLOW).stretch_to_fit_height(4.8).stretch_to_fit_width(6.3).move_to([-3.55, -0.2, 0])
        clk = clock(2.4).move_to([4.2, -0.2, 0])
        clk_label = T("age clock", 30, TEAL).move_to([4.2, -3.15, 0])
        exp_label = T("experience", 30, YELLOW).move_to([-3.55, -3.15, 0])
        song = sing(adult, False, YELLOW, 0.75)
        q = T("?", 100, TEXT).move_to([0.9, -0.5, 0])
        self.play(FadeIn(title), FadeIn(adult), FadeIn(song), FadeIn(clk), FadeIn(clk_label), GrowFromCenter(q), run_time=0.7)
        self.at("like a clock")
        self.play(sweep(clk, 1.5, 1.4))
        self.at("Or does experience")
        self.play(Indicate(song, color=YELLOW), FadeIn(exp_label), run_time=0.7)
        self.at("help close it")
        self.play(Indicate(q, color=TEXT, scale_factor=1.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the zebra finch timeline (days after hatching)
# ---------------------------------------------------------------------------------------------
XD0, XSC = -6.2, 0.105


def xday(d):
    return XD0 + d * XSC


AX_Y = -1.75
BAND_H = 1.0


def day_tick(d, ay=AX_Y, color=GREY, size=26):
    ln = Line([xday(d), ay - 0.12, 0], [xday(d), ay + 0.12, 0], color=color, stroke_width=3)
    lab = T(str(d), size, color).move_to([xday(d), ay - 0.5, 0])
    return VGroup(ln, lab)


def band_rect(d0, d1, color, ay=AX_Y, h=BAND_H, solid=False):
    w = xday(d1) - xday(d0)
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=0.9 if solid else 0.3).move_to([xday(d0) + w / 2, ay + h / 2, 0])


def axis_line(end_day, ay=AX_Y):
    return Line([xday(0), ay, 0], [xday(end_day), ay, 0], color=GREY, stroke_width=4)


def axis_title(ay=AX_Y):
    return T("days after hatching", 26, GREY).move_to([-0.3, ay - 1.2, 0])


YOUNG_AT = [-4.3, 1.9, 0]
TUTOR_AT = [4.3, 1.9, 0]


def finch_cast(tutor_arcs=True):
    young = bird(1.6, BLUE).move_to(YOUNG_AT)
    young_l = T("young male zebra finch", 26, BLUE).move_to([-4.3, 0.2, 0])
    adult = bird(1.6, YELLOW, flip=True).move_to(TUTOR_AT)
    adult_l = T("tutor, usually his father", 26, YELLOW).move_to([4.3, 0.2, 0])
    arcs = sing(adult, True, YELLOW, 1.0)
    return young, young_l, adult, adult_l, arcs


class S07Finch(SpokenScene):
    def construct(self):
        young, young_l, adult, adult_l, arcs = finch_cast()
        axis, atitle = axis_line(75), axis_title()
        t25, t65 = day_tick(25), day_tick(65)
        band = band_rect(25, 65, TEAL)
        band_l = T("memorize", 28, TEAL).move_to([xday(45), AX_Y + BAND_H + 0.3, 0])
        self.play(FadeIn(young), run_time=0.7)
        self.at("zebra finch")
        self.play(FadeIn(young_l), Create(axis), FadeIn(atitle), run_time=0.9)
        self.at("his tutor")
        self.play(FadeIn(adult), Create(arcs), run_time=0.8)
        self.at("usually his father")
        self.play(FadeIn(adult_l), run_time=0.5)
        self.at("day 25")
        self.play(FadeIn(t25), GrowFromEdge(band, LEFT), run_time=1.1)
        self.at("and 65")
        self.play(FadeIn(t65), FadeIn(band_l), run_time=0.5)
        self.finish()


class S08Cryst(SpokenScene):
    def construct(self):
        young, young_l, adult, adult_l, arcs = finch_cast()
        axis, atitle = axis_line(75), axis_title()
        t25, t65 = day_tick(25), day_tick(65)
        band = band_rect(25, 65, TEAL)
        band_l = T("memorize", 28, TEAL).move_to([xday(45), AX_Y + BAND_H + 0.3, 0])
        self.add(young, young_l, adult, adult_l, arcs, axis, atitle, t25, t65, band, band_l)
        own = sing(young, False, BLUE, 1.0)
        t90 = day_tick(90)
        band2 = band_rect(90, 122, BLUE, solid=True)
        band2_l = T("crystallized song", 28, BLUE).move_to([xday(106), AX_Y + BAND_H + 0.3, 0])
        self.at("fixed")
        self.play(arcs.animate.set_opacity(0.25), Create(own), run_time=0.8)
        self.at("by about three months")
        self.play(Transform(axis, axis_line(124)), FadeIn(t90), run_time=0.5)
        self.play(GrowFromEdge(band2, LEFT), run_time=0.6)
        self.play(FadeIn(band2_l), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the two-group table (carried s10 -> s14)
# ---------------------------------------------------------------------------------------------
FX = dict(AI=-5.65, AT=-3.1, B=-0.6, C=1.7, D=3.95, E=6.35)
FROW = [0.75, -1.65]
FMID = -0.45
FRULE = [1.85, FMID, -2.85]


def finch_parts():
    P = {}
    hdr = lambda txt, x: lines(*txt, size=26, color=GREY).move_to([x, 2.55, 0])
    P["hB"] = hdr(["early", "experience"], FX["B"])
    P["hC"] = hdr(["new tutor,", "same late age"], FX["C"])
    P["hD"] = hdr(["copies new", "song?"], FX["D"])
    P["rules"] = VGroup(*[Line([-6.8, y, 0], [5.4, y, 0], color=GREY, stroke_width=2) for y in FRULE]).set_opacity(0.5)
    P["A"], P["B"], P["yes"], P["q"] = [], [], [], []
    for i, y in enumerate(FROW):
        yb = bird(0.75, BLUE).move_to([FX["AI"], y, 0])
        lab = lines(*(["socially", "reared"] if i == 0 else ["reared without", "adult males"]),
                    size=28, color=TEXT).move_to([FX["AT"], y, 0])
        P["A"].append(VGroup(yb, lab))
        dad = bird(0.55, YELLOW if i == 0 else GREY, flip=True).move_to([FX["B"] + 0.35, y + 0.5, 0])
        if i == 0:
            parts = [dad, sing(dad, True, YELLOW, 0.55)]
            txt = lines("hears his", "father sing", size=26, color=TEXT).move_to([FX["B"], y - 0.5, 0])
        else:
            dad.set_opacity(0.45)
            parts = [dad, cross(dad.get_center(), RED, 0.35, 6)]
            txt = lines("hears no", "male song", size=26, color=TEXT).move_to([FX["B"], y - 0.5, 0])
        P["B"].append(VGroup(*parts, txt))
        P["yes"].append(VGroup(check([FX["C"], y + 0.3, 0], YELLOW, 0.3, 8), T("tutor given", 26, YELLOW).move_to([FX["C"], y - 0.45, 0])))
        P["q"].append(T("?", 72, TEXT).move_to([FX["D"], y, 0]))
    clk = clock(0.45).move_to([FX["E"], FMID + 0.3, 0])
    brk = VMobject(stroke_color=GREY, stroke_width=3).set_points_as_corners(
        [[5.4, FROW[0], 0], [5.6, FROW[0], 0], [5.6, FROW[1], 0], [5.4, FROW[1], 0]])
    link = Line([5.6, FMID + 0.3, 0], [FX["E"] - 0.45, FMID + 0.3, 0], color=GREY, stroke_width=3)
    P["clock"] = VGroup(clk, brk, link)
    P["clk"] = clk
    P["clock_l"] = lines("age", "clock", size=26, color=TEAL).move_to([FX["E"], FMID - 0.65, 0])
    P["qtop"] = T("Which group copies the new tutor?", 32, TEXT).move_to([0, 3.5, 0])
    P["qbot"] = T("What would a clock set by age predict?", 28, TEAL).move_to([0, -3.4, 0])
    return P


class S10Groups(SpokenScene):
    def construct(self):
        P = finch_parts()
        self.play(FadeIn(P["rules"]), FadeIn(P["hB"]), FadeIn(P["A"][0]), FadeIn(P["A"][1]), run_time=0.6)
        self.at("hears its father sing")
        self.play(FadeIn(P["B"][0]), run_time=0.7)
        self.at("other is raised")
        self.play(Indicate(P["A"][1], color=TEXT, scale_factor=1.04), run_time=0.6)
        self.at("without adult males")
        self.play(FadeIn(P["B"][1]), run_time=0.7)
        self.finish()


class S11Tutor(SpokenScene):
    def construct(self):
        P = finch_parts()
        self.add(P["rules"], P["hB"], *P["A"], *P["B"])
        note = T("past the age when normally reared males stop copying", 28, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(P["hC"]), FadeIn(P["yes"][0]), FadeIn(P["yes"][1]), run_time=0.8)
        self.at("same late age")
        self.play(Indicate(P["yes"][0], color=YELLOW, scale_factor=1.2), Indicate(P["yes"][1], color=YELLOW, scale_factor=1.2),
                  run_time=0.6)
        self.at("By then")
        self.play(FadeIn(note), run_time=0.6)
        self.at("stopped copying")
        self.play(FadeIn(P["hD"]), FadeIn(P["q"][0]), FadeIn(P["q"][1]), run_time=0.7)
        self.finish()


def add_finch_static(sc, P, clock_on=False, qs=True):
    sc.add(P["rules"], P["hB"], P["hC"], P["hD"], *P["A"], *P["B"], *P["yes"])
    if qs:
        sc.add(*P["q"])
    if clock_on:
        sc.add(P["clock"], P["clock_l"])


class S12Pq(SpokenScene):
    def construct(self):
        P = finch_parts()
        add_finch_static(self, P)
        predict = T("Predict.", 44, TEXT, font=TITLE_FONT).move_to([0, 3.5, 0])
        self.play(FadeIn(predict), run_time=0.5)
        self.at("Which group")
        self.play(ReplacementTransform(predict, P["qtop"]), run_time=0.5)
        self.play(Indicate(P["q"][0], color=YELLOW, scale_factor=1.3), Indicate(P["q"][1], color=YELLOW, scale_factor=1.3),
                  run_time=0.8)
        self.at("What would a clock")
        self.play(FadeIn(P["clock"]), FadeIn(P["clock_l"]), FadeIn(P["qbot"]), run_time=0.7)
        self.at("age predict")
        self.play(sweep(P["clk"], 1.0, 1.0))
        self.finish()


class S13Pause(SpokenScene):
    def construct(self):
        P = finch_parts()
        add_finch_static(self, P, clock_on=True)
        self.add(P["qtop"], P["qbot"])
        self.finish()


class S14Rev(SpokenScene):
    def construct(self):
        P = finch_parts()
        add_finch_static(self, P, clock_on=True, qs=False)
        self.add(P["qtop"], P["qbot"])

        def ghost(y):
            return VGroup(T("no", 48, TEAL), T("clock predicts", 26, TEAL)).arrange(DOWN, buff=0.12).move_to([FX["D"], y, 0]).set_opacity(0.8)
        gh = [ghost(y) for y in FROW]
        self.add(*P["q"])
        self.at("A clock predicts")
        self.play(Indicate(P["clk"], color=TEAL, scale_factor=1.25), run_time=0.7)
        self.at("neither copies")
        self.play(ReplacementTransform(P["q"][0], gh[0]), ReplacementTransform(P["q"][1], gh[1]), run_time=0.6)
        self.at("raised without adult males")
        self.play(Indicate(P["A"][1], color=TEXT, scale_factor=1.05), run_time=0.7)
        self.at("males copied")
        real1 = VGroup(T("no", 52, TEXT), T("result", 26, GREY)).arrange(DOWN, buff=0.12).move_to([FX["D"], FROW[0], 0])
        real2 = VGroup(T("yes", 52, GREEN), T("result", 26, GREY)).arrange(DOWN, buff=0.12).move_to([FX["D"], FROW[1], 0])
        slash = cross(P["clk"].get_center(), RED, 0.5, 8)
        self.play(ReplacementTransform(gh[0], real1), ReplacementTransform(gh[1], real2), Create(slash), run_time=0.8)
        self.finish()


class S15Eales(SpokenScene):
    def construct(self):
        card = VGroup(RoundedRectangle(corner_radius=0.3, width=12.2, height=3.1, stroke_color=GREY, stroke_width=3,
                                       fill_color=GREY, fill_opacity=0.08),
                      T("Lucy Eales, 1985", 58, TEXT, font=TITLE_FONT).shift(UP * 0.7),
                      lines("reported: only birds raised without adult males", "copied the late tutor", size=30,
                            color=YELLOW, buff=0.12).shift(DOWN * 0.45)
                      ).move_to([0, 1.2, 0])
        card2 = VGroup(RoundedRectangle(corner_radius=0.3, width=12.2, height=1.9, stroke_color=GREY, stroke_width=3,
                                        stroke_opacity=0.7),
                       T("Later studies: mixed results", 48, TEXT, font=TITLE_FONT)).move_to([0, -0.55, 0])
        banner = VGroup(RoundedRectangle(corner_radius=0.25, width=12.2, height=1.2, stroke_color=TEAL, stroke_width=3,
                                         fill_color=TEAL, fill_opacity=0.14),
                        T("same age, different history, different outcome", 34, TEXT)).move_to([0, -2.1, 0])
        self.play(FadeIn(card, shift=UP * 0.15), FadeIn(banner, shift=UP * 0.1), run_time=0.8)
        self.at("Later studies")
        self.play(card.animate.move_to([0, 2.15, 0]), banner.animate.move_to([0, -3.05, 0]), FadeIn(card2, shift=UP * 0.15),
                  run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the two timelines (s16, s17, s18)
# ---------------------------------------------------------------------------------------------
RY = [1.85, -0.25]
BH = 0.8
TW_AX = -1.35
LATE_D = 80


def twin_bar(y, d0, d1, color, solid=False):
    w = xday(d1) - xday(d0)
    return Rectangle(width=w, height=BH, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=0.9 if solid else 0.3).move_to([xday(d0) + w / 2, y, 0])


def twin_parts():
    P = {}
    P["axis"] = axis_line(124, TW_AX)
    P["atitle"] = axis_title(TW_AX)
    P["ticks"] = VGroup(day_tick(25, TW_AX), day_tick(65, TW_AX), day_tick(LATE_D, TW_AX, YELLOW), day_tick(90, TW_AX))
    P["labels"] = [T("socially reared", 30, BLUE), T("reared without adult males", 30, BLUE)]
    for lab, y in zip(P["labels"], RY):
        lab.move_to([0, y + BH / 2 + 0.38, 0]).align_to([xday(25), 0, 0], LEFT)
    icons = []
    for i, y in enumerate(RY):
        yb = bird(0.5, BLUE).move_to([-6.0, y, 0])
        dad = bird(0.45, YELLOW if i == 0 else GREY, flip=True).move_to([-4.4, y, 0])
        if i == 0:
            icons.append(VGroup(yb, dad, sing(dad, True, YELLOW, 0.45, 2)))
        else:
            dad.set_opacity(0.45)
            icons.append(VGroup(yb, dad, cross(dad.get_center(), RED, 0.3, 6)))
    P["icons"] = icons
    P["late"] = VGroup(DashedLine([xday(LATE_D), 3.0, 0], [xday(LATE_D), TW_AX, 0], color=YELLOW, stroke_width=4),
                       T("same late age (schematic)", 28, YELLOW).move_to([xday(LATE_D) + 0.4, 3.4, 0]))
    P["b1"], P["b2"] = twin_bar(RY[0], 25, 65, TEAL), twin_bar(RY[1], 25, 95, TEAL)
    P["w1"] = T("window", 28, TEAL).move_to(P["b1"])
    P["w2"] = T("window", 28, TEAL).move_to(P["b2"]).shift(LEFT * 1.0)
    P["c1"] = twin_bar(RY[0], 90, 122, BLUE, True)
    P["c1l"] = T("crystallized song", 26, BG).move_to(P["c1"])
    return P


class S16Close(SpokenScene):
    def construct(self):
        P = twin_parts()
        card = VGroup(RoundedRectangle(corner_radius=0.25, width=10.0, height=0.9, stroke_color=TEAL, stroke_width=3,
                                       fill_color=TEAL, fill_opacity=0.12),
                      T("hearing a tutor helps close the window", 34, TEXT)).move_to([0, -3.3, 0])
        self.play(Create(P["axis"]), FadeIn(P["atitle"]), FadeIn(P["ticks"]), Create(P["late"]), FadeIn(P["labels"][0]),
                  FadeIn(P["labels"][1]), run_time=0.8)
        self.at("different history")
        self.play(FadeIn(P["icons"][0]), FadeIn(P["icons"][1]), run_time=0.8)
        self.at("so age alone")
        self.play(GrowFromEdge(P["b1"], LEFT), GrowFromEdge(P["b2"], LEFT), run_time=1.0)
        self.play(FadeIn(P["w1"]), FadeIn(P["w2"]), GrowFromEdge(P["c1"], LEFT), FadeIn(P["c1l"]), run_time=0.5)
        self.at("Hearing a tutor")
        self.play(FadeIn(card), run_time=0.6)
        self.at("help close it")
        self.play(Indicate(P["b1"], color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.finish()


def twin_static(sc, P):
    sc.add(P["axis"], P["atitle"], P["ticks"], *P["labels"], *P["icons"], P["late"], P["b1"], P["b2"], P["w1"], P["w2"],
           P["c1"], P["c1l"])


def isolate_extras():
    y = RY[1]
    ext = twin_bar(y, 95, 110, TEAL)
    dy = (y - BH / 2 + TW_AX) / 2
    guide = VGroup(Line([xday(65), y - BH / 2, 0], [xday(65), dy - 0.15, 0], color=TEAL, stroke_width=3),
                   Line([xday(110), y - BH / 2, 0], [xday(110), dy - 0.15, 0], color=TEAL, stroke_width=3))
    dbl = DoubleArrow([xday(65), dy, 0], [xday(110), dy, 0], buff=0, color=TEAL, stroke_width=4, tip_length=0.2)
    lab = T("delayed, not abolished", 36, TEAL).move_to([0, -3.35, 0])
    cry = twin_bar(y, 110, 122, BLUE, True)
    cry_l = lines("crystallized song", "of its own", size=28, color=TEXT).move_to([5.1, y + 1.0, 0])
    return ext, guide, dbl, lab, cry, cry_l


class S17Limit(SpokenScene):
    def construct(self):
        P = twin_parts()
        twin_static(self, P)
        ext, guide, dbl, lab, cry, cry_l = isolate_extras()
        self.at("delays the closing")
        self.play(GrowFromEdge(ext, LEFT), Create(guide), run_time=0.7)
        self.play(GrowArrow(dbl), run_time=0.5)
        self.at("does not abolish")
        self.play(FadeIn(lab), run_time=0.6)
        self.at("eventually crystallize")
        self.play(GrowFromEdge(cry, LEFT), run_time=0.7)
        self.at("song of their own")
        self.add(cry_l)
        self.wait(0.5)
        self.finish()


class S18Beat(SpokenScene):
    def construct(self):
        P = twin_parts()
        twin_static(self, P)
        ext, guide, dbl, lab, cry, cry_l = isolate_extras()
        self.add(ext, guide, dbl, lab, cry, cry_l)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the song circuit (s19 -> s22)
# ---------------------------------------------------------------------------------------------
POS = {"HVC": [-4.3, 1.4, 0], "RA": [-1.4, 1.4, 0], "BS": [1.5, 1.4, 0],
       "X": [-4.3, -1.4, 0], "TH": [-1.4, -1.4, 0], "LMAN": [1.5, -1.4, 0]}
NAMES = {"HVC": "HVC", "RA": "RA", "BS": ["brainstem", "motor neurons"], "X": "area X", "TH": "thalamus", "LMAN": "LMAN"}
PW = {"HVC": 2.0, "RA": 1.8, "BS": 2.7, "X": 2.0, "TH": 2.0, "LMAN": 2.0}
PH = {"BS": 1.25}
SK_C = np.array([-1.2, 0.1, 0.0])   # centre of the head ellipse


def skull():
    """Schematic songbird head: an ellipse (the brain region) plus a small beak. Beak points left."""
    head = Ellipse(width=9.8, height=6.4, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.05).move_to(SK_C)
    beak = Polygon([-6.0, 0.45, 0], [-6.75, 0.0, 0], [-6.0, -0.45, 0], stroke_color=YELLOW, stroke_width=3,
                   fill_color=YELLOW, fill_opacity=0.45)
    return VGroup(head, beak)


def brain_outline():
    return skull()


def brain_label():
    return T("songbird brain (schematic)", 26, GREY).move_to([-1.2, 3.62, 0])


def empty_circle(k):
    return Circle(radius=0.5, stroke_color=GREY, stroke_width=3).move_to(POS[k])


def pill_box(k, color):
    return RoundedRectangle(corner_radius=0.45, width=PW[k], height=PH.get(k, 1.0), stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.18).move_to(POS[k])


def pill_label(k, color):
    nm = NAMES[k]
    t = lines(*nm, size=26, color=color, buff=0.06) if isinstance(nm, list) else T(nm, 26, color)
    return t.move_to(POS[k])


def P_(k, dx=0, dy=0):
    return np.array([POS[k][0] + dx, POS[k][1] + dy, 0])


def motor_arrows(syr):
    return [arr(P_("HVC", PW["HVC"] / 2), P_("RA", -PW["RA"] / 2), BLUE),
            arr(P_("RA", PW["RA"] / 2), P_("BS", -PW["BS"] / 2), BLUE),
            arr(P_("BS", PW["BS"] / 2), syr.get_left(), BLUE)]


def make_syrinx():
    t = lines("syrinx", "(vocal organ)", size=26, color=BLUE, buff=0.06)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.3, height=t.height + 0.3, stroke_color=BLUE,
                           stroke_width=2.5, fill_color=BLUE, fill_opacity=0.16)
    return VGroup(box, t.move_to(box)).move_to([5.45, POS["BS"][1], 0])


def afp_arrows():
    a1 = arr(P_("HVC", 0, -0.5), P_("X", 0, 0.5), ORANGE)
    a2 = arr(P_("X", PW["X"] / 2), P_("TH", -PW["TH"] / 2), ORANGE)
    a3 = arr(P_("TH", PW["TH"] / 2), P_("LMAN", -PW["LMAN"] / 2), ORANGE)
    p0, p1, p2 = P_("LMAN", 0, 0.5), np.array([POS["LMAN"][0], 0.0, 0]), np.array([POS["RA"][0], 0.0, 0])
    ret = VGroup(Line(p0, p1, color=ORANGE, stroke_width=4), Line(p1, p2, color=ORANGE, stroke_width=4),
                 arr(p2, P_("RA", 0, -0.5), ORANGE, buff=0))
    return a1, a2, a3, ret


def motor_label():
    return T("motor pathway", 28, BLUE).move_to([-1.4, 2.55, 0])


def afp_label():
    return T("anterior forebrain pathway", 28, ORANGE).move_to([-1.2, -3.55, 0])


class S19Circuit(SpokenScene):
    def construct(self):
        exp = chip("experience", YELLOW, 60).move_to([-4.1, 0.0, 0])
        ar = Arrow([-1.2, 0.0, 0], [1.2, 0.0, 0], buff=0, color=TEAL, stroke_width=10, tip_length=0.35)
        helps = T("helps set", 44, TEAL).move_to([0.0, 0.8, 0])
        band = Rectangle(width=4.4, height=2.6, stroke_color=TEAL, stroke_width=4, fill_color=TEAL,
                         fill_opacity=0.35).move_to([4.3, 0.0, 0])
        wl = T("window", 60, TEAL).move_to([4.3, 0.0, 0])
        self.play(FadeIn(exp), run_time=0.5)
        self.at("help set")
        self.add(helps)
        self.play(GrowArrow(ar), GrowFromEdge(band, LEFT), run_time=0.5)
        self.at("window")
        self.play(FadeIn(wl), run_time=0.4)
        self.at("which part")
        outline, bl = brain_outline(), brain_label()
        self.play(FadeOut(VGroup(exp, ar, helps, band, wl)), Create(outline), run_time=0.7)
        self.play(FadeIn(bl), run_time=0.3)
        self.finish()


def circuit_base(sc):
    outline, bl = brain_outline(), brain_label()
    circles = {k: empty_circle(k) for k in POS}
    sc.add(outline, bl)
    return outline, bl, circles


class S20Motor(SpokenScene):
    def construct(self):
        outline, bl, circles = circuit_base(self)
        syr = make_syrinx()
        a1, a2, a3 = motor_arrows(syr)
        lab = motor_label()
        boxes = {k: pill_box(k, BLUE) for k in ("HVC", "RA", "BS")}
        labs = {k: pill_label(k, BLUE) for k in ("HVC", "RA", "BS")}
        self.at("motor pathway")
        self.play(FadeIn(lab), run_time=0.5)
        self.at("from HVC")
        self.play(FadeIn(boxes["HVC"]), run_time=0.5)
        self.play(FadeIn(labs["HVC"]), run_time=0.3)
        self.at("to RA")
        self.play(GrowArrow(a1), run_time=0.5)
        self.at("RA")
        self.play(FadeIn(boxes["RA"]), run_time=0.4)
        self.play(FadeIn(labs["RA"]), run_time=0.3)
        self.at("to brainstem")
        self.play(GrowArrow(a2), run_time=0.5)
        self.at("brainstem")
        self.play(FadeIn(boxes["BS"]), run_time=0.4)
        self.play(FadeIn(labs["BS"]), run_time=0.3)
        self.at("the vocal organ")
        self.play(GrowArrow(a3), FadeIn(syr), run_time=0.8)
        self.finish()


def motor_done(sc):
    syr = make_syrinx()
    a1, a2, a3 = motor_arrows(syr)
    boxes = {k: pill_box(k, BLUE) for k in ("HVC", "RA", "BS")}
    labs = {k: pill_label(k, BLUE) for k in ("HVC", "RA", "BS")}
    lab = motor_label()
    sc.add(*boxes.values(), *labs.values(), a1, a2, a3, syr, lab)
    return boxes, labs, syr


class S21Afp(SpokenScene):
    def construct(self):
        outline, bl = brain_outline(), brain_label()
        circles = {k: empty_circle(k).set_stroke(opacity=0.3) for k in ("X", "TH", "LMAN")}
        self.add(outline, bl)
        motor_done(self)
        a1, a2, a3, ret = afp_arrows()
        boxes = {k: pill_box(k, ORANGE) for k in ("X", "TH", "LMAN")}
        labs = {k: pill_label(k, ORANGE) for k in ("X", "TH", "LMAN")}
        self.at("leaves HVC")
        self.play(GrowArrow(a1), run_time=0.7)
        self.at("area X")
        self.play(FadeIn(boxes["X"]), run_time=0.4)
        self.play(FadeIn(labs["X"]), run_time=0.3)
        self.at("the thalamus")
        self.play(GrowArrow(a2), FadeIn(boxes["TH"]), FadeIn(labs["TH"]), run_time=0.6)
        self.at("to L man")
        self.play(GrowArrow(a3), FadeIn(boxes["LMAN"]), FadeIn(labs["LMAN"]), run_time=0.6)
        self.at("then back to RA")
        self.play(Create(ret), run_time=0.7)
        self.at("RA")
        lab = afp_label()
        self.play(FadeIn(lab), *[Indicate(b, color=ORANGE, scale_factor=1.06) for b in boxes.values()], run_time=0.7)
        self.finish()


def afp_done(sc):
    outline, bl = brain_outline(), brain_label()
    sc.add(outline, bl)
    motor_done(sc)
    a1, a2, a3, ret = afp_arrows()
    boxes = {k: pill_box(k, ORANGE) for k in ("X", "TH", "LMAN")}
    labs = {k: pill_label(k, ORANGE) for k in ("X", "TH", "LMAN")}
    sc.add(a1, a2, a3, ret, *boxes.values(), *labs.values(), afp_label())


def small_skull(scale, at, lesion=False):
    """The same head, small, with the LMAN site marked (and crossed out when lesioned)."""
    sk = skull()
    head = sk[0]
    c0 = head.get_center().copy()
    lman = c0 + np.array([POS["LMAN"][0] - SK_C[0], -1.4 - SK_C[1], 0.0])
    dot = Circle(radius=0.55, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.3).move_to(lman)
    g = VGroup(sk, dot)
    if lesion:
        g.add(cross(dot.get_center(), RED, 0.4, 10))
    g.scale(scale)
    g.move_to(at)
    return g


def irregular(t):
    """Developing, disordered song: no repeating pattern (random envelope, drifting pitch)."""
    rng = np.random.RandomState(11)
    ct = np.linspace(0, 6, 36)
    ca = rng.uniform(0.15, 1.0, 36)
    env = np.interp(t, ct, ca)
    return env * np.sin(13 * t + 3.5 * np.sin(1.7 * t) + 2.0 * np.sin(4.3 * t + 1))


def motif_song(t, period=1.9):
    """Stable adult song: the same motif of three syllables, repeated exactly."""
    u = np.mod(t, period)
    env = (np.exp(-((u - 0.35) / 0.14) ** 2) + 0.8 * np.exp(-((u - 0.9) / 0.17) ** 2)
           + 0.9 * np.exp(-((u - 1.5) / 0.12) ** 2))
    return env * np.sin(24 * u)


class S22Lesion(SpokenScene):
    def construct(self):
        def panel(x, title, lesion_label):
            fr = RoundedRectangle(corner_radius=0.3, width=6.5, height=6.0, stroke_color=GREY, stroke_width=3
                                  ).move_to([x, 0.0, 0])
            ti = T(title, 32, BLUE).move_to([x, 2.5, 0])
            sk = small_skull(0.3, [x - 1.4, 1.15, 0], lesion=True)
            ll = T(lesion_label, 26, ORANGE).move_to([x + 2.05, 1.15, 0])
            spot = sk[1].get_center()
            ln = Line([x + 0.95, 1.15, 0], spot + np.array([0.2, 0, 0]), color=ORANGE, stroke_width=2)
            return fr, ti, sk, ll, ln
        L = panel(-3.55, "young finch", "LMAN lesion")
        R = panel(3.55, "adult finch", "LMAN lesion")
        def trace(x, fn, color):
            w = ParametricFunction(lambda t: np.array([x - 2.7 + t, -0.75 + 0.6 * fn(t), 0]), t_range=[0, 5.4, 0.015],
                                   color=color, stroke_width=5)
            ax = Arrow([x - 2.8, -1.65, 0], [x + 2.8, -1.65, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.15)
            tl = T("time", 26, GREY).move_to([x, -2.05, 0])
            return w, VGroup(ax, tl)
        w_l, ax_l = trace(-3.55, irregular, RED)
        w_r, ax_r = trace(3.55, motif_song, GREEN)
        c_l = T("song development disrupted", 28, RED).move_to([-3.55, -2.6, 0])
        c_r = T("stable adult song intact", 28, GREEN).move_to([3.55, -2.6, 0])
        credit = T("Bottjer, Miesner and Arnold, 1984", 26, GREY).move_to([0, 3.65, 0])
        schematic = brain_label().move_to([0, 3.15, 0])
        take = T("this loop matters while song is learned", 32, ORANGE).move_to([0, -3.45, 0])
        self.play(FadeIn(VGroup(*L)), FadeIn(credit), FadeIn(schematic), run_time=0.8)
        self.at("disrupted song development")
        self.play(Create(w_l), FadeIn(ax_l), FadeIn(c_l), run_time=1.0)
        self.at("but left stable adult song")
        self.play(FadeIn(VGroup(*R)), run_time=0.7)
        self.at("stable adult song")
        self.play(Create(w_r), FadeIn(ax_r), FadeIn(c_r), run_time=1.0)
        self.at("This loop matters")
        self.play(FadeIn(take), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the NMDA receptor (s24 -> s25): a labelled schematic, not a structure
# ---------------------------------------------------------------------------------------------
MY = -0.6   # membrane centre line


def nmda_parts():
    def blk(w, h, x, y):
        return RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=RECEPTOR, stroke_width=3,
                                fill_color=RECEPTOR, fill_opacity=0.25).move_to([x, y, 0])
    def memb(x):
        return Rectangle(width=5.4, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.35).move_to([x, MY, 0])
    P = {}
    P["memL"], P["memR"] = memb(-4.1), memb(4.1)
    P["wallL"], P["wallR"] = blk(0.9, 2.2, -0.95, MY), blk(0.9, 2.2, 0.95, MY)
    P["headL"], P["headR"] = blk(2.2, 1.8, -1.6, 1.45), blk(2.2, 1.8, 1.6, 1.45)
    for s, nm in ((-1, "pockL"), (1, "pockR")):
        P[nm] = RoundedRectangle(corner_radius=0.12, width=0.75, height=0.75, stroke_color=TEXT, stroke_width=2,
                                 fill_color=BG, fill_opacity=1).move_to([1.65 * s, 1.55, 0])
    P["body"] = VGroup(P["wallL"], P["wallR"], P["headL"], P["headR"])
    P["mem"] = VGroup(P["memL"], P["memR"])
    P["pore_glow"] = Rectangle(width=1.0, height=4.05, stroke_width=0, fill_color=GREEN, fill_opacity=0.28
                               ).move_to([0, 0.325, 0])
    P["label"] = T("NMDA receptor", 26, RECEPTOR).move_to([4.7, 0.4, 0])
    P["label_ln"] = Line([3.15, 0.55, 0], [2.7, 0.9, 0], color=RECEPTOR, stroke_width=2)
    # sides of the membrane, the membrane itself and the pore
    P["outside"] = T("outside the cell", 26, GREY).move_to([-4.4, 0.6, 0])
    P["membrane"] = T("membrane", 26, TEXT).move_to([-4.1, MY, 0])
    P["inside"] = T("inside the receiving cell", 26, GREY).move_to([-4.85, -2.2, 0])
    P["pore"] = VGroup(T("pore", 28, TEXT).move_to([-1.9, -2.7, 0]),
                       Arrow([-1.45, -2.5, 0], [-0.3, -1.78, 0], buff=0.0, color=TEXT, stroke_width=3, tip_length=0.15))
    P["static"] = VGroup(P["outside"], P["membrane"], P["inside"], P["pore"])
    return P


def pocket_lit(p, color):
    return p.animate.set_fill(color, opacity=0.55).set_stroke(color)


def sign_row(char, color):
    return VGroup(*[T(char, 38, color).move_to([x, -1.55, 0]) for x in (-6.2, -5.2, -4.2, -3.2, -2.2, 2.2, 3.2, 4.2, 5.2, 6.2)])


class S24Nmda(SpokenScene):
    def construct(self):
        afp_done(self)
        brain_stuff = VGroup(*self.mobjects)
        P = nmda_parts()
        glu = Dot(radius=0.22, color=YELLOW).move_to([-1.65, 3.35, 0])
        glu_l = T("glutamate", 28, YELLOW).move_to([-4.3, 1.55, 0])
        glu_ln = Line([-3.3, 1.55, 0], [-2.1, 1.55, 0], color=YELLOW, stroke_width=2)
        co = Dot(radius=0.22, color=PINK).move_to([1.65, 3.35, 0])
        co_l = lines("co-agonist", "(glycine or D-serine)", size=26, color=PINK, buff=0.06).move_to([4.75, 1.75, 0])
        co_ln = Line([3.1, 1.6, 0], [2.1, 1.55, 0], color=PINK, stroke_width=2)
        act = T("these open the channel", 32, TEXT).move_to([0, 3.25, 0])
        self.at("NMDA receptors")
        self.play(FadeOut(brain_stuff), run_time=0.3)
        self.play(FadeIn(P["mem"]), FadeIn(P["body"]), FadeIn(P["pockL"]), FadeIn(P["pockR"]), run_time=0.6)
        self.play(FadeIn(P["label"]), FadeIn(P["label_ln"]), FadeIn(P["static"]), run_time=0.3)
        self.at("natural suspect")
        self.play(Indicate(P["body"], color=TEXT, scale_factor=1.03), run_time=0.7)
        self.at("Glutamate")
        self.play(FadeIn(glu), FadeIn(glu_l), run_time=0.2)
        self.play(glu.animate.move_to(P["pockL"].get_center()), FadeIn(glu_ln), pocket_lit(P["pockL"], YELLOW), run_time=0.7)
        self.at("helper molecule")
        self.play(FadeIn(co), FadeIn(co_l[0]), run_time=0.2)
        self.play(co.animate.move_to(P["pockR"].get_center()), FadeIn(co_ln), pocket_lit(P["pockR"], PINK), run_time=0.7)
        self.at("co agonist")
        self.play(FadeIn(co_l[1]), run_time=0.5)
        self.at("activate them")
        self.add(act)  # Full contrast at the cue; retain through the final hold.
        self.play(P["body"].animate.set_stroke(TEXT), Indicate(P["pockL"], color=YELLOW),
                  Indicate(P["pockR"], color=PINK), run_time=0.8)
        self.finish()


def mg(at, r=0.38):
    return VGroup(Circle(radius=r, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.55),
                  T("Mg", 24, TEXT)).move_to(at)


def ion_flow(x=0.0):
    """Ions moving down through the open pore: a row of dots, staggered."""
    dots = [Dot(radius=0.14, color=GREEN).move_to([x + dx, 2.9 - 0.0, 0]) for dx in (-0.2, 0.2, 0.0, -0.2, 0.2)]
    return dots


def flow_anim(dots, y_end=-2.0, rt=1.6):
    return LaggedStart(*[d.animate.move_to([d.get_center()[0], y_end, 0]) for d in dots], lag_ratio=0.18, run_time=rt)


def open_pore(P):
    """The pore visibly opens: the two walls move apart a little, and the channel fills green."""
    return [P["wallL"].animate.shift(LEFT * 0.12), P["wallR"].animate.shift(RIGHT * 0.12), FadeIn(P["pore_glow"])]


def flow_arrows():
    a = VGroup(Arrow([-0.2, 2.9, 0], [-0.2, -1.95, 0], buff=0, color=GREEN, stroke_width=7, tip_length=0.28),
               Arrow([0.2, 2.9, 0], [0.2, -1.95, 0], buff=0, color=GREEN, stroke_width=7, tip_length=0.28))
    l = T("ions flow in", 28, GREEN).move_to([4.2, -2.2, 0])
    return a, l


class S24bMg(SpokenScene):
    def construct(self):
        P = nmda_parts()
        P["pockL"].set_fill(YELLOW, opacity=0.55).set_stroke(YELLOW)
        P["pockR"].set_fill(PINK, opacity=0.55).set_stroke(PINK)
        P["body"].set_stroke(TEXT)
        glu = Dot(radius=0.22, color=YELLOW).move_to(P["pockL"].get_center())
        co = Dot(radius=0.22, color=PINK).move_to(P["pockR"].get_center())
        self.add(P["mem"], P["body"], P["pockL"], P["pockR"], glu, co, P["label"], P["label_ln"], P["static"])
        m1, m3 = mg([-3.0, 3.1, 0]), mg([3.0, 3.1, 0])
        m2 = mg([0.0, 3.1, 0])
        m_l = T("magnesium", 28, RED).move_to([5.0, 3.1, 0])
        state = T("at rest", 28, GREY).move_to([-5.55, -3.1, 0])
        state_dep = T("depolarized", 28, YELLOW).move_to([-5.55, -3.1, 0])
        minus = sign_row("\u2212", GREY)
        plus = sign_row("+", YELLOW)
        final = T("depolarization relieves the magnesium block", 30, TEXT).move_to([0.6, -3.5, 0])
        arrs, flow_l = flow_arrows()
        dots = ion_flow()
        self.at("magnesium levels")
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(m3), FadeIn(m_l), run_time=0.6)
        self.at("magnesium plugs")
        self.play(m2.animate.move_to([0, MY, 0]), run_time=1.0)
        self.at("receiving cell")
        self.play(FadeIn(minus), FadeIn(state), run_time=0.5)
        self.at("depolarized")
        self.play(ReplacementTransform(minus, plus), ReplacementTransform(state, state_dep), run_time=0.6)
        self.play(m2.animate.move_to([1.7, -2.8, 0]), *open_pore(P), FadeIn(final), run_time=0.8)
        self.add(*dots)
        self.play(GrowArrow(arrs[0]), GrowArrow(arrs[1]), FadeIn(flow_l), flow_anim(dots, -2.0, 1.4))
        self.play(FadeOut(VGroup(*dots)), run_time=0.2)
        self.finish()


class S25Nmda2(SpokenScene):
    def construct(self):
        P = nmda_parts()
        P["pockR"].set_fill(PINK, opacity=0.55).set_stroke(PINK)
        co = Dot(radius=0.22, color=PINK).move_to(P["pockR"].get_center())
        term = RoundedRectangle(corner_radius=0.3, width=5.4, height=0.8, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.12).move_to([0, 3.4, 0])
        term_l = T("sending cell", 26, GREY).move_to([-4.9, 3.4, 0])
        ves = [Dot(radius=0.16, color=YELLOW).move_to([x, 3.4, 0]) for x in (-2.1, -1.65, -1.2)]
        plug = mg([0, MY, 0])
        state = T("at rest", 28, GREY).move_to([-5.55, -3.1, 0])
        state_dep = T("depolarized", 28, YELLOW).move_to([-5.55, -3.1, 0])
        minus = sign_row("\u2212", GREY)
        plus = sign_row("+", YELLOW)
        rel_l = T("glutamate released", 28, YELLOW).move_to([4.7, 3.4, 0])
        coin = lines("coincidence", "detector", size=34, color=TEXT, buff=0.08).move_to([4.8, 0.95, 0])
        thin = Rectangle(width=1.2, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, 2.65, 0])
        thick = Rectangle(width=4.6, height=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.7).move_to([0, 2.65, 0])
        strong = T("stronger synapse", 32, YELLOW).move_to([4.7, 2.25, 0])
        hedge = T("(in many brain regions)", 26, YELLOW).move_to([4.7, 1.75, 0])
        arrs, flow_l = flow_arrows()
        dots = ion_flow()
        self.add(P["mem"], P["body"], P["pockL"], P["pockR"], co, term, term_l, *ves, plug, P["static"], thin, minus, state)
        self.at("glutamate is released")
        self.play(FadeIn(rel_l), *[v.animate.move_to([-1.65 + 0.2 * (i - 1), 2.7, 0]) for i, v in enumerate(ves)], run_time=0.6)
        self.play(*[v.animate.move_to(P["pockL"].get_center() + [0.18 * (i - 1), 0.12 * (1 - abs(i - 1)), 0]) for i, v in enumerate(ves)],
                  pocket_lit(P["pockL"], YELLOW), run_time=0.6)
        self.at("receiving cell is depolarized")
        self.play(ReplacementTransform(minus, plus), ReplacementTransform(state, state_dep), run_time=0.6)
        self.play(plug.animate.move_to([1.7, -2.8, 0]), *open_pore(P), P["body"].animate.set_stroke(TEXT), run_time=0.8)
        self.add(*dots)
        self.play(GrowArrow(arrs[0]), GrowArrow(arrs[1]), FadeIn(flow_l), flow_anim(dots, -2.0, 1.4))
        self.play(FadeOut(VGroup(*dots)), run_time=0.2)
        self.at("same time")
        self.play(FadeIn(coin), Indicate(plus, color=TEXT, scale_factor=1.1), Indicate(P["pockL"], color=YELLOW),
                  run_time=0.8)
        self.at("strengthens the active synapse")
        self.play(Transform(thin, thick), FadeIn(strong), run_time=0.9)
        self.play(FadeIn(hedge), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# AP5 (s26 -> s32)
# ---------------------------------------------------------------------------------------------
def ap5_picture():
    sk = skull().scale(0.9).move_to([-0.2, -0.45, 0])
    head = sk[0]
    c0 = head.get_center()
    region = Ellipse(width=4.8, height=3.6, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                     fill_opacity=0.22).move_to(c0 + np.array([-1.5, -0.1, 0]))
    ry = region.get_center()[1]
    cx = region.get_center()[0]
    region_l = T("anterior forebrain", 30, ORANGE).move_to([cx, ry - 1.0, 0])
    cannula = VGroup(Line([cx, 2.35, 0], [cx, ry + 1.1, 0], color=TEXT, stroke_width=8),
                     Rectangle(width=0.7, height=0.32, stroke_color=TEXT, stroke_width=3, fill_color=GREY,
                               fill_opacity=0.8).move_to([cx, 2.5, 0]))
    cannula_l = T("cannula", 28, TEXT).move_to([cx - 1.6, 2.5, 0])
    cannula_ln = Line([cx - 0.95, 2.5, 0], [cx - 0.4, 2.5, 0], color=TEXT, stroke_width=2)
    drops = VGroup(*[Dot(radius=0.13, color=RED).move_to([cx + dx, ry + dy, 0])
                     for dx, dy in [(-0.55, 0.5), (0.4, 0.7), (0.0, 0.2), (-0.5, -0.1), (0.5, 0.1), (0.1, 0.75)]])
    ap5 = T("AP5 (blocker)", 30, RED).move_to([cx + 3.6, ry + 1.2, 0])
    ap5_ln = Line([cx + 2.15, ry + 1.2, 0], [cx + 0.7, ry + 0.75, 0], color=RED, stroke_width=2)
    return sk, region, region_l, cannula, VGroup(cannula_l, cannula_ln), drops, VGroup(ap5, ap5_ln)


class S26Ap5(SpokenScene):
    def construct(self):
        credit = VGroup(RoundedRectangle(corner_radius=0.25, width=7.3, height=0.95, stroke_color=GREY, stroke_width=3,
                                         fill_color=GREY, fill_opacity=0.1),
                        T("Basham, Nordeen and Nordeen, 1996", 28, TEXT, font=TITLE_FONT)).move_to([3.1, 3.4, 0])
        sk, region, region_l, cannula, can_l, drops, ap5 = ap5_picture()
        schematic = brain_label().move_to([0, -3.65, 0])
        self.play(FadeIn(credit, shift=DOWN * 0.1), Create(sk[0]), FadeIn(sk[1]), FadeIn(schematic), run_time=0.8)
        self.at("and colleagues")
        self.play(FadeIn(region), FadeIn(region_l), run_time=0.6)
        self.at("infused")
        self.play(Create(cannula), FadeIn(can_l), run_time=0.5)
        self.at("a blocker")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in drops], lag_ratio=0.2, run_time=0.7))
        self.at("P5")
        self.play(FadeIn(ap5), run_time=0.4)
        self.finish()


ARY = [1.55, -0.35, -2.25]
ARULE = [2.4, 0.6, -1.3, -3.2]
CX = dict(icon=-6.15, text=-4.85, res=1.9, ann=5.0)


def brain_icon(posterior=False):
    sk = skull()
    head = sk[0]
    c0 = head.get_center()
    spot = Circle(radius=0.8, stroke_color=GREY if posterior else ORANGE, stroke_width=3, fill_color=GREY if posterior else ORANGE,
                  fill_opacity=0.35).move_to(c0 + (np.array([2.7, -1.7, 0]) if posterior else np.array([-2.3, -0.2, 0])))
    dot = Dot(spot.get_center(), radius=0.38, color=RED)
    g = VGroup(sk, spot, dot)
    return g.scale(0.13)


def ap5_parts():
    P = {}
    texts = [["AP5 in the anterior forebrain", "before each of ten", "tutoring sessions"],
             ["AP5 in the anterior forebrain", "on non-tutoring days only"],
             ["AP5 into the cerebellum"]]
    P["hdr"] = VGroup(T("copied?", 26, GREY).move_to([CX["res"], 2.8, 0]),
                      T("what it tells us", 26, GREY).move_to([CX["ann"], 2.8, 0]))
    P["rules"] = VGroup(*[Line([-6.8, y, 0], [6.8, y, 0], color=GREY, stroke_width=2) for y in ARULE]).set_opacity(0.5)
    P["rows"], P["q"] = [], []
    for i, y in enumerate(ARY):
        icon = brain_icon(i == 2).move_to([CX["icon"], y, 0])
        txt = lines(*texts[i], size=26, color=TEXT, align=LEFT).move_to([0, y, 0])
        txt.align_to([CX["text"], 0, 0], LEFT)
        P["rows"].append(VGroup(icon, txt))
        P["q"].append(T("?", 72, TEXT).move_to([CX["res"], y, 0]))
    P["title"] = T("Which birds copy poorly?", 32, TEXT).move_to([0, 3.5, 0])
    P["key"] = T("red dot: where AP5 goes", 26, GREY).move_to([-4.3, -3.55, 0])
    P["res"] = [lines("copied", "significantly less", size=26, color=RED).move_to([CX["res"], ARY[0], 0]),
                lines("copied", "normally", size=26, color=GREEN).move_to([CX["res"], ARY[1], 0]),
                lines("copied", "normally", size=26, color=GREEN).move_to([CX["res"], ARY[2], 0])]
    P["impl"] = [None,
                 lines("counts against", "lost practice alone", "(not fully excluded)", size=26,
                       color=TEXT, buff=0.08).move_to([CX["ann"], ARY[1], 0]),
                 lines("argues against an", "effect of the drug", "wherever infused", size=26, color=TEXT,
                       buff=0.08).move_to([CX["ann"], ARY[2], 0])]
    return P


class S27Pq(SpokenScene):
    def construct(self):
        P = ap5_parts()
        pic = VGroup(*ap5_picture())
        self.add(pic)
        predict = T("Predict.", 44, TEXT, font=TITLE_FONT).move_to([-3.4, 3.5, 0])
        self.play(FadeOut(pic), FadeIn(predict), FadeIn(P["rules"]), FadeIn(P["hdr"][0]), *[FadeIn(row) for row in P["rows"]], FadeIn(P["key"]), run_time=0.6)
        self.at("Which birds")
        self.play(ReplacementTransform(predict, P["title"]), FadeIn(P["q"][0]), FadeIn(P["q"][1]), FadeIn(P["q"][2]), FadeIn(P["hdr"][1]), run_time=0.6)
        self.at("Blocker in the anterior forebrain")
        self.play(Indicate(P["rows"][0], color=YELLOW, scale_factor=1.02), run_time=0.7)
        self.at("before tutoring")
        self.play(Indicate(P["rows"][0][1], color=YELLOW, scale_factor=1.03), run_time=0.7)
        self.at("on other days only")
        self.play(Indicate(P["rows"][1], color=YELLOW, scale_factor=1.02), run_time=0.7)
        self.at("in the cerebellum")
        self.play(Indicate(P["rows"][2], color=YELLOW, scale_factor=1.02), run_time=0.7)
        self.finish()


def ap5_static(sc, P, results=False, upto_impl=(), key=True):
    sc.add(P["title"], P["hdr"], P["rules"], *P["rows"])
    if key:
        sc.add(P["key"])
    if results:
        sc.add(*P["res"])
    else:
        sc.add(*P["q"])
    for i in upto_impl:
        sc.add(P["impl"][i])


class S28Pause(SpokenScene):
    def construct(self):
        P = ap5_parts()
        ap5_static(self, P)
        self.finish()


class S29Rev(SpokenScene):
    def construct(self):
        P = ap5_parts()
        ap5_static(self, P)
        self.at("first group")
        self.play(Indicate(P["rows"][0], color=RED, scale_factor=1.03), run_time=0.5)
        self.at("copied less")
        self.play(ReplacementTransform(P["q"][0], P["res"][0]), run_time=0.5)
        self.play(ReplacementTransform(P["q"][1], P["res"][1]), ReplacementTransform(P["q"][2], P["res"][2]), run_time=0.5)
        self.finish()


class S30Ctrl1(SpokenScene):
    def construct(self):
        P = ap5_parts()
        ap5_static(self, P, results=True)
        dim1 = VGroup(P["rows"][0], P["res"][0])
        dim3 = VGroup(P["rows"][2], P["res"][2])
        note = T("birds could catch up between infusions", 30, TEXT).move_to([0.8, -3.55, 0])
        self.play(dim1.animate.set_opacity(0.6), dim3.animate.set_opacity(0.6), FadeOut(P["key"]), run_time=0.5)
        self.at("copied normally")
        self.play(Indicate(P["res"][1], color=GREEN, scale_factor=1.12), run_time=0.7)
        self.at("That counts against")
        self.play(FadeIn(P["impl"][1]), run_time=0.7)
        self.at("though birds could catch up")
        self.play(FadeIn(note), run_time=0.7)
        self.finish()


def finch_song(t):
    """Zebra finch: short repeated buzzes with gaps."""
    gate = np.clip(np.sin(2 * PI * t / 0.9), 0, None) ** 0.5
    return gate * np.sin(26 * t)


def canary_song(t):
    """Canary: a continuous, fast, pitch-swept warble."""
    return 0.9 * np.sin(55 * t + 7 * np.sin(2.2 * t)) * (0.55 + 0.45 * np.sin(1.1 * t))


class S31Ctrl2(SpokenScene):
    def construct(self):
        P = ap5_parts()
        ap5_static(self, P, results=True, upto_impl=(1,), key=False)
        for m in (P["rows"][0], P["res"][0], P["rows"][1], P["res"][1], P["impl"][1]):
            m.set_opacity(0.6)
        row3 = VGroup(P["rows"][2], P["res"][2])
        self.at("Cerebellum infusions")
        self.play(Indicate(P["rows"][2], color=TEXT, scale_factor=1.04), run_time=0.7)
        self.at("learning normal")
        self.play(FadeIn(P["impl"][2]), Indicate(P["res"][2], color=GREEN, scale_factor=1.12), run_time=0.8)
        self.at("And the")
        keep_hdr = P["hdr"][0]
        gone = VGroup(P["rows"][0], P["res"][0], P["rows"][1], P["res"][1], P["impl"][1], P["impl"][2], P["title"], P["hdr"][1],
                      P["rules"])
        sep = Line([-6.8, 1.85, 0], [6.8, 1.85, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        treated = chip("AP5-treated birds", BLUE, 30).move_to([0, 1.3, 0])
        card_l = RoundedRectangle(corner_radius=0.25, width=6.0, height=3.7, stroke_color=GREY, stroke_width=3).move_to([-3.5, -1.15, 0])
        card_r = RoundedRectangle(corner_radius=0.25, width=6.0, height=3.7, stroke_color=GREY, stroke_width=3).move_to([3.5, -1.15, 0])
        lab_l = T("zebra finch song", 30, YELLOW).move_to([-3.5, 0.15, 0])
        lab_r = T("canary song", 30, YELLOW).move_to([3.5, 0.15, 0])
        def sw(x, fn):
            return ParametricFunction(lambda t: np.array([x - 2.6 + t, -1.45 + 0.75 * fn(t), 0]), t_range=[0, 5.2, 0.012],
                                      color=YELLOW, stroke_width=5)
        wv_l, wv_r = sw(-3.5, finch_song), sw(3.5, canary_song)
        told = DoubleArrow([-0.45, -1.45, 0], [0.45, -1.45, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.2)
        deaf = T("told apart: not simply deaf", 38, GREEN).move_to([0, -3.52, 0])
        self.play(FadeOut(gone), row3.animate.shift(UP * 4.65), keep_hdr.animate.move_to([CX["res"], 3.45, 0]),
                  FadeIn(sep), run_time=0.8)
        self.at("treated birds")
        self.play(FadeIn(treated), run_time=0.4)
        self.at("still tell")
        self.play(FadeIn(card_l), FadeIn(card_r), run_time=0.5)
        self.at("finch song")
        self.play(FadeIn(lab_l), Create(wv_l), run_time=0.7)
        self.at("canary song")
        self.play(FadeIn(lab_r), Create(wv_r), run_time=0.7)
        self.at("so they were")
        self.play(FadeIn(told), run_time=0.5)
        self.at("not simply deaf")
        self.play(FadeIn(deaf), run_time=0.6)
        self.finish()


class S32Take(SpokenScene):
    def construct(self):
        l1 = T("NMDA receptors in the", 50, TEXT, font=TITLE_FONT)
        l2 = T("anterior forebrain are needed", 50, TEXT, font=TITLE_FONT)
        l3 = T("during tutoring", 50, TEXT, font=TITLE_FONT)
        txt = VGroup(l1, l2, l3).arrange(DOWN, buff=0.25)
        card = RoundedRectangle(corner_radius=0.35, width=txt.width + 1.4, height=txt.height + 1.0, stroke_color=ORANGE,
                                stroke_width=3, fill_color=ORANGE, fill_opacity=0.1)
        main = VGroup(card, txt).move_to([0, 0.2, 0])
        dash = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=11.0, height=2.5, stroke_color=GREY, stroke_width=3),
                              num_dashes=80).move_to([0, -2.4, 0])
        notshown = VGroup(T("Where the memory is stored:", 38, GREY), T("not shown", 44, TEXT)).arrange(DOWN, buff=0.2).move_to([0, -2.4, 0])
        self.at("NMDA receptors")
        self.play(FadeIn(main, shift=UP * 0.1), run_time=0.9)
        self.at("needed while the song")
        self.play(l3.animate.set_color(YELLOW), run_time=0.6)
        self.at("Where the memory")
        self.play(main.animate.move_to([0, 1.2, 0]), FadeIn(dash), FadeIn(notshown), run_time=0.9)
        self.finish()


class S33End(EndCard):
    LINE = "Experience seems to help close the window, and the song-learning loop needs NMDA receptors while a tutor is heard."

    def construct(self):
        a = T("Experience seems to help close the window,", 38, TEXT, font=TITLE_FONT)
        b = T("and the song-learning loop needs", 38, TEXT, font=TITLE_FONT)
        c = T("NMDA receptors while a tutor is heard.", 38, TEXT, font=TITLE_FONT)
        line = VGroup(a, b, c).arrange(DOWN, buff=0.25)
        sub = T("biochemistrypedia.com", 26, TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.55)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
