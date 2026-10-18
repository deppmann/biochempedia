"""History of life: a fossil date is a floor  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = fossils and traces of life (mounds, fossil bed, fossil dots)
  YELLOW = a measured date, the minimum age, the bracket
  ORANGE = parent atoms (uranium)
  GREEN  = daughter atoms (lead)
  PURPLE = rock and ash (zircon crystal, ash beds)
  TEAL   = one species / lineage drawn as a line
  RED    = where the truth could lie (older), unknown, gone
  GREY   = axes, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
AX_Y = -0.4          # y of the Dresser timeline (s01 and s06)
PIN_X = 2.2          # x of the 3.48 Ga pin


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def mounds(cx, base_y, scale=1.0):
    """three layered mounds side by side (simple half-ellipse outlines, nothing molecular)."""
    specs = [(1.3, 1.25), (1.6, 1.9), (1.1, 1.0)]    # (half width, height)
    gap = 0.18
    total = sum(2 * a for a, _ in specs) + gap * 2
    x = -total / 2
    parts = []
    for a, h in specs:
        xc = x + a
        for k, f in enumerate([1.0, 0.72, 0.45]):
            t = np.linspace(0, np.pi, 40)
            pts = [[xc + a * f * np.cos(u), base_y_local + h * f * np.sin(u), 0] for u in t] if False else None
            pts = [[xc + a * f * np.cos(u), h * f * np.sin(u), 0] for u in t]
            poly = Polygon(*pts, stroke_color=BLUE, stroke_width=3.5 if k == 0 else 2.5,
                           fill_color=BLUE, fill_opacity=0.28 if k == 0 else 0.0)
            parts.append(poly)
        x += 2 * a + gap
    base = Line([-total / 2 - 0.2, 0, 0], [total / 2 + 0.2, 0, 0], color=GREY, stroke_width=5)
    g = VGroup(*parts, base)
    g.scale(scale)
    g.move_to([cx, base_y, 0], aligned_edge=DOWN)
    return g


def dresser_timeline():
    """axis, zone and pin positions shared by s01 and s06."""
    axis = Arrow([5.9, AX_Y, 0], [-6.2, AX_Y, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
    older = T("older", 24, GREY).move_to([-5.5, AX_Y + 0.4, 0])
    younger = T("younger", 24, GREY).move_to([5.0, AX_Y + 0.4, 0])
    pin = Line([PIN_X, AX_Y, 0], [PIN_X, 0.75, 0], color=YELLOW, stroke_width=4)
    tick = Dot([PIN_X, AX_Y, 0], radius=0.12, color=YELLOW)
    lab = T("3.48 Ga", 30, YELLOW, weight=BOLD).move_to([PIN_X + 1.0, AX_Y - 0.5, 0])
    zone = DashedVMobject(Rectangle(width=7.9, height=1.75, stroke_color=RED, stroke_width=3.5,
                                    fill_color=RED, fill_opacity=0.08).move_to([-2.25, -1.17, 0]), num_dashes=60)
    qs = VGroup(*[T("?", 44, RED, weight=BOLD).move_to([x, -1.25, 0]) for x in (-5.2, -3.6, -2.0, -0.4)])
    return axis, older, younger, pin, tick, lab, zone, qs


class S00Title(TitleCard):
    LESSON = "History of Life and Macroevolution"
    TITLE = "A Fossil Date Is a Floor"


# ---------------------------------------------------------------------------------------------
class S01Dresser(SpokenScene):
    def construct(self):
        m = mounds(0, 0.25, 1.15)
        lab1 = T("Dresser Formation, Western Australia", 32).move_to([0, -0.45, 0])
        lab2 = T("about 3.48 billion years old", 28, YELLOW).move_to([0, -1.0, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in m[:-1]], lag_ratio=0.12), Create(m[-1]), run_time=1.2)
        self.at("Dresser Formation")
        self.play(FadeIn(lab1), FadeIn(lab2), run_time=0.7)
        read = chip("2017 study: traces of life in hot springs", BLUE, size=28).move_to([0, -2.1, 0])
        self.at("traces of life")
        self.play(FadeIn(read, shift=UP * 0.15), run_time=0.6)
        q = T("When did life begin?", 46, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("when did life begin")
        self.play(Write(q), run_time=0.9)
        self.at("These rocks")
        self.play(q.animate.set_color(RED), run_time=0.3)
        axis, older, younger, pin, tick, lab, zone, qs = dresser_timeline()
        self.at("that life existed")
        small = mounds(PIN_X, 1.05, 0.6)
        self.play(FadeOut(lab1), FadeOut(lab2), FadeOut(read), FadeOut(q),
                  Transform(m, small), Create(axis), FadeIn(older), FadeIn(younger), run_time=0.9)
        self.play(Create(pin), FadeIn(tick), FadeIn(lab), run_time=0.5)
        self.at("older traces")
        self.play(FadeIn(zone), LaggedStart(*[FadeIn(x, scale=1.4) for x in qs], lag_ratio=0.15), run_time=0.9)
        reasons = [chip("destroyed", RED, 26), chip("never formed", RED, 26), chip("not yet found", RED, 26)]
        row = VGroup(*reasons).arrange(RIGHT, buff=0.25).move_to([-2.25, -2.95, 0])
        for r, ph in zip(reasons, ["destroyed", "never formed", "not yet found"]):
            self.at(ph)
            self.play(FadeIn(r, shift=UP * 0.12), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def atom(color, r=0.38):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)


GRID = [(-1, 1), (1, 1), (-1, -1), (1, -1)]


def crystal(center, w, h, states, d, r):
    """states: 'U' uranium or 'P' lead for the four grid slots."""
    box = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=PURPLE, stroke_width=4,
                           fill_color=PURPLE, fill_opacity=0.14).move_to(center)
    dots = VGroup()
    for (gx, gy), s in zip(GRID, states):
        dots.add(atom(ORANGE if s == "U" else GREEN, r).move_to(np.array(center) + np.array([gx * d, gy * d, 0])))
    return box, dots


def hourglass(cx, cy):
    top = Polygon([cx - 1, cy + 1.7, 0], [cx + 1, cy + 1.7, 0], [cx, cy, 0], stroke_color=GREY, stroke_width=4)
    bot = Polygon([cx, cy, 0], [cx + 1, cy - 1.7, 0], [cx - 1, cy - 1.7, 0], stroke_color=GREY, stroke_width=4)
    return VGroup(top, bot)


def sand_top(cx, cy, f):
    L = 1.7 * np.sqrt(0.78 * max(f, 0.001))
    hw = L / 1.7
    return Polygon([cx - hw, cy + L, 0], [cx + hw, cy + L, 0], [cx, cy, 0], stroke_width=0,
                   fill_color=ORANGE, fill_opacity=0.85)


def sand_bot(cx, cy, f):
    L = 1.7 * (1 - np.sqrt(1 - 0.78 * max(f, 0.001)))
    hw_floor = 0.95
    hw_top = 0.95 * (1 - L / 1.7)
    return Polygon([cx - hw_floor, cy - 1.65, 0], [cx + hw_floor, cy - 1.65, 0],
                   [cx + hw_top, cy - 1.65 + L, 0], [cx - hw_top, cy - 1.65 + L, 0],
                   stroke_width=0, fill_color=GREEN, fill_opacity=0.85)


class S02Clock(SpokenScene):
    def construct(self):
        cc = np.array([-4.0, 0.3, 0])
        box, dots = crystal(cc, 3.7, 3.7, "UUUU", 0.85, 0.4)
        name = T("hypothetical zircon", 26, PURPLE).move_to([-4.0, -2.0, 0])
        rock = Rectangle(width=3.7, height=3.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.15).move_to(cc)
        fossil = Ellipse(width=1.6, height=0.8, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.7).move_to(cc)
        fl = T("fossil", 26, BLUE).next_to(fossil, DOWN, buff=0.15)
        self.play(FadeIn(rock), FadeIn(fossil, scale=0.5), FadeIn(fl), run_time=0.8)
        self.at("Minerals in the rocks")
        halo = [Circle(radius=0.14, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.8).move_to(cc + np.array(p + (0,)))
                for p in [(-1.4, 1.4), (1.4, 1.4), (-1.4, -1.4), (1.4, -1.4), (0, 1.5), (0, -1.5)]]
        ml = T("minerals around it", 26, PURPLE).move_to([-4.0, -2.0, 0])
        self.play(LaggedStart(*[FadeIn(h, scale=0.3) for h in halo], lag_ratio=0.1), FadeIn(ml), run_time=1.0)
        self.at("hypothetical zircon")
        self.play(FadeOut(fossil), FadeOut(fl), FadeOut(VGroup(*halo)), FadeOut(ml), ReplacementTransform(rock, box), FadeIn(name), run_time=0.8)
        self.at("took up uranium")
        leg_u = VGroup(atom(ORANGE, 0.22), T("uranium (parent)", 26, ORANGE)).arrange(RIGHT, buff=0.2)
        leg_u.move_to([4.2, 1.4, 0]).align_to([2.5, 0, 0], LEFT)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.15), FadeIn(leg_u), run_time=1.0)
        self.at("almost no lead")
        leg_p = VGroup(atom(GREEN, 0.22), T("lead (daughter)", 26, GREEN)).arrange(RIGHT, buff=0.2)
        leg_p.move_to([4.2, -0.2, 0]).align_to([2.5, 0, 0], LEFT)
        none = T("almost none at first", 22, GREY).next_to(leg_p, DOWN, buff=0.15).align_to(leg_p, LEFT)
        self.play(FadeIn(leg_p), FadeIn(none), run_time=0.6)
        self.at("later decay")
        dk = arr([2.7, 1.0, 0], [2.7, 0.25, 0], GREY)
        dkl = T("decay", 24, GREY).next_to(dk, RIGHT, buff=0.15)
        dk2 = VGroup(dk, dkl)
        dk2.shift(RIGHT * 0.0)
        self.play(GrowArrow(dk), FadeIn(dkl), run_time=0.5)
        self.at("hourglass")
        hg = hourglass(0.0, 0.5)
        st = sand_top(0.0, 0.5, 1.0)
        sb = sand_bot(0.0, 0.5, 0.0)
        # keep hourglass between crystal and legend
        self.play(FadeOut(dk), FadeOut(dkl), Create(hg), FadeIn(st), run_time=0.8)
        self.at("bottom bulb")
        sb2 = sand_bot(0.0, 0.5, 0.1)
        self.play(Transform(sb, sb2), run_time=0.4)
        self.add(sb)
        self.at("the time for half")
        hl = T("half-life", 36, YELLOW, weight=BOLD).move_to([0.0, -2.7, 0])
        self.play(FadeIn(hl, shift=UP * 0.1), run_time=0.5)
        self.at("Here it is")
        hl2 = T("half-life = 704 million years", 36, YELLOW, weight=BOLD).move_to([0.0, -2.7, 0])
        self.play(ReplacementTransform(hl, hl2),
                  dots[2].animate.set_color(GREEN).set_fill(GREEN, 0.9),
                  dots[3].animate.set_color(GREEN).set_fill(GREEN, 0.9),
                  Transform(st, sand_top(0.0, 0.5, 0.5)),
                  Transform(sb, sand_bot(0.0, 0.5, 0.5)), run_time=1.6)
        self.finish()


class S03Ratio(SpokenScene):
    def construct(self):
        d = 0.7
        xs = [-4.5, 0.0, 4.5]
        cy = np.array([0, 0.7, 0])
        W, H, R = 3.0, 2.9, 0.33
        # C first (the measured crystal), then A and B
        boxC, dotsC = crystal(cy + np.array([xs[2], 0, 0]), W, H, "UPPP", d, R)
        boxA, dotsA = crystal(cy + np.array([xs[0], 0, 0]), W, H, "UUUU", d, R)
        boxB, dotsB = crystal(cy + np.array([xs[1], 0, 0]), W, H, "UUPP", d, R)
        labC = VGroup(T("measured now", 26, TEXT), M("lead / uranium = 3", 22, YELLOW)).arrange(DOWN, buff=0.1).move_to([xs[2], -1.25, 0])
        labA = VGroup(T("at the start", 26, TEXT), T("4 uranium", 24, ORANGE)).arrange(DOWN, buff=0.1).move_to([xs[0], -1.25, 0])
        labB = VGroup(T("after one half-life", 26, TEXT), T("2 uranium, 2 lead", 24, GREY)).arrange(DOWN, buff=0.1).move_to([xs[1], -1.25, 0])
        self.play(FadeIn(boxC), FadeIn(labC[0]), run_time=0.5)
        self.at("three lead atoms")
        self.play(LaggedStart(*[FadeIn(x, scale=0.4) for x in dotsC], lag_ratio=0.15), FadeIn(labC[1]), run_time=1.0)
        self.at("once a uranium atom")
        ghosts = VGroup(*[Circle(radius=R + 0.07, stroke_color=ORANGE, stroke_width=4).move_to(x) for x in dotsC[1:]])
        self.play(Create(ghosts), run_time=0.6)
        self.at("started with four")
        self.play(FadeIn(boxA), LaggedStart(*[FadeIn(x, scale=0.4) for x in dotsA], lag_ratio=0.12), FadeIn(labA), run_time=1.0)
        self.play(FadeOut(ghosts), run_time=0.3)
        self.at("One quarter is left")
        q = T("1 of 4 left: one quarter", 24, YELLOW).move_to([xs[2], -2.05, 0])
        self.play(Indicate(dotsC[0], color=YELLOW, scale_factor=1.25), FadeIn(q), run_time=0.8)
        self.at("That is two")
        a1 = CurvedArrow(boxA.get_top() + UP * 0.05, boxB.get_top() + UP * 0.05, angle=-TAU / 6, color=YELLOW, stroke_width=5)
        t1 = T("704 million years", 24, YELLOW).next_to(a1, UP, buff=0.05)
        self.play(FadeIn(boxB), FadeIn(labB), Create(a1), FadeIn(t1), *[FadeIn(x, scale=0.4) for x in dotsB], run_time=0.8)
        a2 = CurvedArrow(boxB.get_top() + UP * 0.05, boxC.get_top() + UP * 0.05, angle=-TAU / 6, color=YELLOW, stroke_width=5)
        t2 = T("704 million years", 24, YELLOW).next_to(a2, UP, buff=0.05)
        self.play(Create(a2), FadeIn(t2), run_time=0.5)
        self.at("Two times")
        res = T("2 × 704 = 1,408 million years", 40, YELLOW, weight=BOLD).move_to([0, -2.95, 0])
        self.play(FadeIn(res, shift=UP * 0.15), run_time=0.7)
        self.at("a model")
        ass = T("a model, only as good as its assumptions", 24, GREY).move_to([0, -3.5 + 0.0, 0])
        self.play(FadeIn(ass), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Bracket(SpokenScene):
    def construct(self):
        cx, w = -4.1, 4.0
        bed = Rectangle(width=w, height=2.0, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.12).move_to([cx, 0.45, 0])
        fos = VGroup(*[Ellipse(width=0.55, height=0.28, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.7).move_to([cx + dx, 0.45 + dy, 0])
                       for dx, dy in [(-1.2, 0.55), (0.0, 0.7), (1.1, 0.5), (-0.6, 0.0), (0.6, -0.05)]])
        bedlab = T("fossil bed", 28, BLUE).move_to([cx, -0.3, 0])
        # put label inside lower part of bed
        bedlab.move_to([cx, 0.45 - 0.78, 0])
        top = Rectangle(width=w, height=0.8, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3).move_to([cx, 1.9, 0])
        toplab = T("ash", 28, PURPLE).move_to(top)
        bot = Rectangle(width=w, height=0.8, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3).move_to([cx, -1.0, 0])
        botlab = T("ash", 28, PURPLE).move_to(bot)
        tag = T("worked example (hypothetical)", 26, GREY).move_to([2.0, 3.3, 0])
        self.at("date a fossil")
        self.play(FadeIn(tag), run_time=0.4)
        self.play(FadeIn(bed), LaggedStart(*[FadeIn(f, scale=0.3) for f in fos], lag_ratio=0.12), FadeIn(bedlab), run_time=1.0)
        # age axis
        ax_y = -2.45
        x_old, x_young = 0.9, 4.7
        axis = Arrow([-0.7, ax_y, 0], [6.2, ax_y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        axl = T("older", 22, GREY).move_to([-0.3, ax_y - 0.4, 0])
        ayl = T("younger", 22, GREY).move_to([5.7, ax_y - 0.4, 0])
        self.at("ash lies above")
        self.play(FadeIn(top), FadeIn(toplab), run_time=0.6)
        d1 = DashedLine([cx + w / 2, 1.9, 0], [x_young, 1.9, 0], color=PURPLE, stroke_width=3)
        d1v = DashedLine([x_young, 1.9, 0], [x_young, ax_y, 0], color=PURPLE, stroke_width=3)
        l1 = T("ash above: 1,408 million years", 26, YELLOW).move_to([2.25, 2.35, 0])
        self.play(Create(d1), Create(d1v), Create(axis), FadeIn(axl), FadeIn(ayl), FadeIn(l1), run_time=1.0)
        self.at("second ash")
        self.play(FadeIn(bot), FadeIn(botlab), run_time=0.6)
        d2 = DashedLine([cx + w / 2, -1.0, 0], [x_old, -1.0, 0], color=PURPLE, stroke_width=3)
        d2v = DashedLine([x_old, -1.0, 0], [x_old, ax_y, 0], color=PURPLE, stroke_width=3)
        l2 = T("ash below: 1,450 million years", 26, YELLOW).move_to([1.9, -0.6, 0])
        self.play(Create(d2), Create(d2v), FadeIn(l2), run_time=1.0)
        self.at("younger than")
        s1 = T("older than 1,408", 28, TEXT)
        s2 = T("younger than 1,450", 28, TEXT)
        st = VGroup(s2, s1).arrange(DOWN, buff=0.12).move_to([2.8, 0.65, 0])
        self.play(FadeIn(st, shift=UP * 0.1), run_time=0.7)
        self.at("a bracket")
        br = Line([x_old, ax_y, 0], [x_young, ax_y, 0], color=YELLOW, stroke_width=10)
        brl = T("the fossils fall here", 26, YELLOW).move_to([2.8, ax_y + 0.45, 0])
        self.play(Create(br), FadeIn(brl), run_time=0.8)
        self.at("not a point")
        self.play(Indicate(br, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Floor(SpokenScene):
    def construct(self):
        ly = 0.3
        xs = [-4.1, -2.3, 0.6, 2.2]
        x_van = 4.9
        head = T("one lineage through time", 32, GREY).move_to([0, 3.1, 0])
        rows = [("3.48 Ga", "Dresser Formation, Western Australia"), ("2,460 to 2,426 Ma", "onset of the Great Oxidation Event"),
                ("1.047 Ga", "Bangiomorpha, a red alga"), ("571 to 541 Ma", "Ediacaran, Dickinsonia"),
                ("473 to 471 Ma", "cryptospores of early land plants")]
        lst = VGroup()
        for i, (da, db) in enumerate(rows):
            d_ = T(da, 28, YELLOW); t_ = T(db, 28, TEXT)
            y_ = 1.2 - i * 0.7
            d_.move_to([-1.4 - d_.width / 2, y_, 0]); t_.move_to([-1.0 + t_.width / 2, y_, 0])
            lst.add(VGroup(d_, t_))
        lead = T("firsts in the record", 30, GREY).move_to([0, 2.75, 0])
        self.play(FadeIn(lead), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in lst], lag_ratio=0.25), run_time=1.6)
        line = Line([xs[0], ly, 0], [x_van, ly, 0], color=TEAL, stroke_width=7)
        fos = [Dot([x, ly, 0], radius=0.38, color=BLUE) for x in xs]
        tl = Arrow([6.2, -3.25, 0], [-6.2, -3.25, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        tll = T("older", 22, GREY).move_to([-5.5, -2.85, 0])
        tly = T("younger", 22, GREY).move_to([5.4, -2.85, 0])
        self.at("minimum age")
        self.play(FadeOut(lst), FadeOut(lead), run_time=0.4)
        self.play(FadeIn(head), Create(tl), FadeIn(tll), FadeIn(tly), run_time=0.5)
        self.play(Create(line), LaggedStart(*[FadeIn(f, scale=0.3) for f in fos], lag_ratio=0.1), run_time=0.8)
        self.at("oldest fossil")
        floor = Line([xs[0], ly - 1.0, 0], [xs[0], ly + 1.0, 0], color=YELLOW, stroke_width=7)
        fl = VGroup(T("oldest fossil:", 28, YELLOW), T("a floor", 28, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([xs[0], ly + 1.75, 0])
        self.play(Create(floor), FadeIn(fl), run_time=0.7)
        self.at("may be older")
        dash = DashedLine([xs[0], ly, 0], [-6.2, ly, 0], color=RED, stroke_width=7)
        ol = VGroup(T("lineage may", 26, RED), T("be older", 26, RED)).arrange(DOWN, buff=0.05).move_to([-5.3, ly - 0.95, 0])
        self.play(Create(dash), FadeIn(ol), run_time=0.8)
        self.at("uneven")
        gx0, gx1 = xs[1], xs[2]
        brk = VGroup(Line([gx0, ly - 0.55, 0], [gx1, ly - 0.55, 0], color=GREY, stroke_width=4),
                     Line([gx0, ly - 0.45, 0], [gx0, ly - 0.65, 0], color=GREY, stroke_width=4),
                     Line([gx1, ly - 0.45, 0], [gx1, ly - 0.65, 0], color=GREY, stroke_width=4))
        gl = T("gap in the record", 26, GREY).move_to([(gx0 + gx1) / 2, ly - 1.05, 0])
        self.play(Create(brk), FadeIn(gl), run_time=0.7)
        self.at("not a gap in life")
        gl2 = T("not a gap in life", 26, TEAL).move_to([(gx0 + gx1) / 2, ly - 1.65, 0])
        self.play(Indicate(line, color=TEAL, scale_factor=1.0), FadeIn(gl2), run_time=0.8)
        self.at("other end")
        lf = T("last fossil", 28, BLUE).move_to([xs[3], ly + 0.95, 0])
        self.play(FadeIn(lf), Indicate(fos[3], color=BLUE, scale_factor=1.4), run_time=0.7)
        self.at("actually vanished")
        xm = VGroup(Line([-0.28, -0.28, 0], [0.28, 0.28, 0]), Line([-0.28, 0.28, 0], [0.28, -0.28, 0])).set_color(RED).set_stroke(width=8).move_to([x_van, ly, 0])
        vl = T("vanished", 28, RED).move_to([x_van, ly + 0.95, 0])
        gap = DoubleArrow([xs[3] + 0.4, ly - 0.55, 0], [x_van - 0.1, ly - 0.55, 0], buff=0, color=RED, stroke_width=4, tip_length=0.2)
        self.play(Create(xm), FadeIn(vl), GrowFromCenter(gap), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        names = [("measured age", YELLOW), ("a method", GREY), ("an uncertainty", GREY), ("a direction the truth could lie", RED)]
        chips = [chip(t, c, size=24, pad=0.14) for t, c in names]
        col = VGroup(*chips).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        col.move_to([0, 0, 0]).to_corner(UL, buff=0.5)
        axis, older, younger, pin, tick, lab, zone, qs = dresser_timeline()
        self.at("measured age")
        self.play(FadeIn(chips[0], shift=RIGHT * 0.2), run_time=0.5)
        self.at("a method")
        self.play(FadeIn(chips[1], shift=RIGHT * 0.2), run_time=0.5)
        self.at("an uncertainty")
        self.play(FadeIn(chips[2], shift=RIGHT * 0.2), run_time=0.5)
        self.at("direction in which")
        self.play(FadeIn(chips[3], shift=RIGHT * 0.2), run_time=0.5)
        small = mounds(PIN_X, 1.05, 0.6)
        self.at("Dresser rocks")
        self.play(FadeIn(small), Create(axis), FadeIn(older), FadeIn(younger), run_time=0.8)
        self.at("life existed by")
        self.play(Create(pin), FadeIn(tick), FadeIn(lab), run_time=0.6)
        self.play(FadeIn(zone), LaggedStart(*[FadeIn(x, scale=1.4) for x in qs], lag_ratio=0.12), run_time=0.8)
        self.at("never when it began")
        final = VGroup(T("The oldest fossil tells you when life existed by,", 32, TEXT, font=TITLE_FONT),
                       T("never when it began.", 36, YELLOW, font=TITLE_FONT)).arrange(DOWN, buff=0.15).move_to([0, -2.85, 0])
        self.play(FadeIn(final, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Oldest fossil: when life existed by, never when it began."
