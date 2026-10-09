"""Daniel Koshland: a scientist profile (Biochemistrypedia, enzyme-action-basics lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quote). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Koshland, the portrait frame, the idea (induced fit), "proved him right"
  BLUE   = the enzyme (the lock, the jaws)
  GREEN  = the substrate and its grip
  AMBER  = the strained transition state and its grip
  TEAL   = water
  YELLOW = dates (1950s, 1958)
  RED    = what went wrong or stood in the way (chaos, the dogma, rejection, "not true")
  PLACE  (lavender) = institutions: the standard journals, PNAS
  GREY   = structure, labels, the textbook page, apparatus
No molecular structure is drawn: the enzyme is a schematic block with a slot (lock-and-key) or a
base with two hinged jaws (induced fit); the substrate is a plain block; water is small dots.
"""
from math import radians

import numpy as np
from bp_style import *  # noqa: F401,F403
from pathlib import Path
import os

PORTRAIT = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "koshland.png")
CAPTION = "illustration · AI-generated"
NAME = "Daniel Koshland"
DATES = "1920–2007"
PLACE = "#B39DDB"
AMBER = "#E0A458"

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95          # x centre of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T(NAME, size=34, font=TITLE_FONT)
    dt = T(DATES, size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.3, 0])
    return g


def inset_group():
    img, frame = portrait_pair(INSET_H)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = caption_under(frame)
    tag = name_tag(frame)
    rule = Line([-2.7, -3.2, 0], [-2.7, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def solid(color, k=0.22):
    return ManimColor(BG).interpolate(ManimColor(color), k)


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16):
    """Chip with one or more centred lines of text."""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.frame = frame
        self.add(img, frame, cap, tag, rule)


def lock_enzyme(cx, cy, s=1.0, color=BLUE):
    """The rigid enzyme of lock-and-key: a block with a fixed slot. cy = centre of the body.
    Slot: x in cx +- 0.65 s, floor at cy - 0.05 s, rim at cy + 0.85 s."""
    pts = [(-2, 0.85), (-0.65, 0.85), (-0.65, -0.05), (0.65, -0.05), (0.65, 0.85), (2, 0.85), (2, -0.85), (-2, -0.85)]
    poly = Polygon(*[[cx + x * s, cy + y * s, 0] for x, y in pts], stroke_color=color, stroke_width=3,
                   fill_color=solid(color), fill_opacity=1)
    poly.round_corners(0.07 * s)
    return poly


def sub_block(w=1.2, h=0.8, color=GREEN, corner=0.1):
    return RoundedRectangle(corner_radius=corner, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=solid(color, 0.35), fill_opacity=1)


def water_dots(n, color=TEAL, r=0.1):
    return [Dot(radius=r, color=color) for _ in range(n)]


class Jaws:
    """The flexible enzyme of induced fit: a base with two hinged jaws.
    a = jaw angle in degrees from vertical (0 = upright, + = splayed open)."""

    def __init__(self, cx, cy, a=30, s=1.0, color=BLUE):
        self.s, self.a = s, a
        self.color = color
        bw, bh = 3.1 * s, 0.9 * s
        self.px, self.jw, self.jh = 0.95 * s, 0.75 * s, 1.9 * s
        self.base = RoundedRectangle(corner_radius=0.18 * s, width=bw, height=bh, stroke_color=color, stroke_width=3,
                                     fill_color=solid(color), fill_opacity=1).move_to([cx, cy, 0])
        self.top = cy + bh / 2
        py = self.top - 0.1 * s
        self.pl = np.array([cx - self.px, py, 0.0])
        self.pr = np.array([cx + self.px, py, 0.0])
        mk = lambda p: RoundedRectangle(corner_radius=0.2 * s, width=self.jw, height=self.jh, stroke_color=color,
                                        stroke_width=3, fill_color=solid(color), fill_opacity=1).move_to(
            [p[0], p[1] + self.jh / 2, 0])
        self.left, self.right = mk(self.pl), mk(self.pr)
        self.left.rotate(radians(a), about_point=self.pl)
        self.right.rotate(radians(-a), about_point=self.pr)
        self.cx, self.cy = cx, cy
        self.group = VGroup(self.base, self.left, self.right)

    def to(self, a, run_time=0.9, rate_func=smooth):
        """Animations that move the jaws to angle a."""
        d = radians(self.a - a)
        self.a = a
        return [Rotate(self.left, -d, about_point=self.pl, run_time=run_time, rate_func=rate_func),
                Rotate(self.right, d, about_point=self.pr, run_time=run_time, rate_func=rate_func)]

    def move(self, dx):
        self.pl = self.pl + np.array([dx, 0, 0])
        self.pr = self.pr + np.array([dx, 0, 0])
        self.cx += dx
        return self.group.animate.shift(RIGHT * dx)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = NAME

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T(DATES, size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.1, 0.2, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(
            ScaleInPlace(grp, 1.07, run_time=1.8, rate_func=linear),
            Succession(
                FadeIn(VGroup(brand, lesson), shift=UP * 0.1, run_time=0.4),
                Write(name, run_time=0.7),
                FadeIn(dates, shift=UP * 0.1, run_time=0.4),
                GrowFromCenter(rule, run_time=0.3),
            ),
        )
        i_img, i_frame, i_cap, i_tag, i_rule = inset_group()
        self.play(
            FadeOut(txt), FadeOut(cap),
            img.animate.set_height(INSET_H).move_to(INSET_C), frame.animate.become(i_frame),
            run_time=0.7,
        )
        self.play(FadeIn(i_cap), FadeIn(i_tag), FadeIn(i_rule), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------- s01 lock-and-key, 1950s
class S01Lock(ProfileScene):
    def construct(self):
        self.add_inset()
        FX, S = 0.9, 1.2
        enz = lock_enzyme(FX, -0.85, S)                   # slot rim y=0.17, floor y=-0.91
        home = [FX, -0.91 + 0.48 + 0.03, 0]
        sub = sub_block(1.44, 0.96).move_to([FX, 1.3, 0])
        yr = M("1950s", 56, YELLOW).move_to([FX, 2.85, 0])
        cap1 = T("lock-and-key", 32, BLUE).move_to([FX, -2.6, 0])
        cap2 = T("every textbook", 30, GREY).move_to([FX, -3.15, 0])
        page = RoundedRectangle(corner_radius=0.18, width=5.9, height=4.2, stroke_color=GREY, stroke_width=4).move_to([FX, 0.0, 0])

        self.at("1950s")
        self.play(Write(yr), run_time=0.5)
        self.at("lock and key")
        self.play(FadeIn(enz), FadeIn(sub), run_time=0.4)
        self.play(sub.animate.move_to(home), FadeIn(cap1, shift=UP * 0.1), run_time=0.7)
        self.at("decorated every")
        self.play(Create(page), run_time=0.7)
        self.at("textbook", lead=0.35)
        self.play(FadeIn(cap2, shift=UP * 0.1), run_time=0.4)

        self.at("Daniel Koshland")
        self.play(Indicate(self.frame, color=TEXT, scale_factor=1.06), run_time=0.8)
        self.at("incomplete", lead=0.3)
        inc = T("incomplete", 32, RED).move_to(cap2)
        self.play(page.animate.set_color(RED), ReplacementTransform(cap2, inc), run_time=0.6)

        self.at("water")
        wchip = lab("water", TEAL, 32).move_to([5.45, 0.9, 0])
        dots = VGroup(*water_dots(4, r=0.13)).arrange(RIGHT, buff=0.3).next_to(wchip, DOWN, buff=0.4)
        self.play(pop(wchip), LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.2), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s02 water
class S02Water(ProfileScene):
    def construct(self):
        self.add_inset()
        EX, EY, S = 1.0, -1.0, 1.4          # slot x in EX+-0.91, rim y=EY+1.19, floor y=EY-0.07
        enz = lock_enzyme(EX, EY, S)
        self.play(FadeIn(enz), run_time=0.3)

        self.at("active site")
        lbl = T("active site", 30, BLUE).move_to([5.0, 0.7, 0])
        arr = Arrow(lbl.get_left() + LEFT * 0.1, [EX + 0.95, EY + 1.2, 0], buff=0, color=BLUE, stroke_width=4,
                    max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(lbl), GrowArrow(arr), run_time=0.5)

        self.at("permanently open")
        tint = Rectangle(width=1.82, height=1.26, stroke_width=0, fill_color=GREY, fill_opacity=0.0).move_to([EX, EY + 0.56, 0])
        open_t = T("permanently open, waiting", 32, GREY).move_to([EX, -2.75, 0])
        self.play(FadeIn(open_t, shift=UP * 0.1), tint.animate.set_fill(GREY, 0.3), run_time=0.6)

        self.at("water", lead=0.55)
        xs = [0.45, 0.75, 1.0, 1.3, 1.5]
        ys = [2.0, 2.4, 2.05, 2.4, 2.0]
        dots = VGroup(*[d.move_to([x, y, 0]) for d, x, y in zip(water_dots(5, r=0.14), xs, ys)])
        wl = T("water", 32, TEAL).move_to([3.4, 2.5, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.1), FadeIn(wl), run_time=0.55)

        self.at("smaller than any")
        sb = sub_block(1.6, 1.05).move_to([-0.95, 2.3, 0])
        sl = T("substrate", 30, GREEN).next_to(sb, DOWN, buff=0.2)
        self.play(pop(sb), FadeIn(sl), Indicate(dots, color=TEAL, scale_factor=1.5), run_time=0.9)

        self.at("slip in")
        tx = [0.45, 0.75, 1.05, 1.35, 0.6]
        ty = [-0.82, -0.82, -0.82, -0.82, -0.52]
        self.play(FadeOut(open_t), FadeOut(Group(sb, sl)),
                  LaggedStart(*[d.animate.move_to([x, y, 0]) for d, x, y in zip(dots, tx, ty)], lag_ratio=0.18),
                  run_time=1.4)
        self.at("trigger chaos", lead=0.1)
        chaos = T("chaos", 48, RED, font=TITLE_FONT).move_to([5.0, -0.6, 0])
        self.play(tint.animate.set_fill(RED, 0.45), FadeIn(chaos, shift=LEFT * 0.2), run_time=0.5)
        rng = np.random.default_rng(3)
        for _ in range(4):
            self.play(*[d.animate.shift([rng.uniform(-0.12, 0.12), rng.uniform(-0.1, 0.1), 0]) for d in dots],
                      run_time=0.14, rate_func=linear)
        self.at("It doesn't", lead=0.1)
        strike = Line(chaos.get_left() + LEFT * 0.1, chaos.get_right() + RIGHT * 0.1, color=GOLD, stroke_width=6)
        no = T("It doesn't.", 50, GOLD, font=TITLE_FONT).move_to([PANEL_C, -2.75, 0])
        self.play(FadeOut(dots), FadeOut(wl), tint.animate.set_fill(RED, 0.0), Create(strike), run_time=0.5)
        self.play(FadeIn(no, shift=UP * 0.12), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s03 induced fit
class S03Fit(ProfileScene):
    def settop(self, txt, color=GOLD, size=40):
        new = T(txt, size, color, font=TITLE_FONT).move_to([PANEL_C, 2.65, 0])
        old = getattr(self, "top", None)
        self.top = new
        if old is None:
            return [FadeIn(new, shift=UP * 0.1)]
        return [Succession(FadeOut(old, shift=UP * 0.1, run_time=0.35), FadeIn(new, shift=UP * 0.1, run_time=0.65))]

    def construct(self):
        self.add_inset()
        cx, cy, S = 0.2, -1.7, 1.15
        J = Jaws(cx, cy, a=28, s=S)
        sub = sub_block(1.27, 1.27).move_to([cx, 1.75, 0])
        rest_y = J.top + 0.64
        leg_e = T("enzyme", 30, BLUE).move_to([-1.5, -2.7, 0])
        leg_s = T("substrate", 30, GREEN).move_to([1.0, -2.7, 0])

        self.play(FadeIn(J.group), FadeIn(leg_e), run_time=0.25)
        self.at("something must change")
        self.play(*self.settop("something must change"), run_time=0.5)
        self.at("real substrate")
        self.play(FadeIn(sub), run_time=0.2)
        self.play(sub.animate.move_to([cx, rest_y, 0]), FadeIn(leg_s), run_time=1.0)
        self.at("closes around it", lead=0.3)
        self.play(*self.settop("the site closes around it"), *J.to(0, 0.9), run_time=0.9)

        self.at("complementarity", lead=0.3)
        halo = SurroundingRectangle(sub, color=GOLD, buff=0.07, corner_radius=0.12, stroke_width=4)
        self.play(*self.settop("complementarity"), Create(halo), run_time=0.6)
        self.play(Indicate(halo, color=GOLD, scale_factor=1.12), run_time=0.7)

        # grip comparison (heights are qualitative: the entry gives no numbers)
        self.at("resting substrate", lead=0.5)
        base_y = -1.6
        axis = Line([3.2, base_y, 0], [6.3, base_y, 0], color=GREY, stroke_width=3)
        grip = T("grip", 34, GOLD).move_to([4.8, 1.45, 0])
        b1 = Rectangle(width=1.0, height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
        b1.move_to([3.95, base_y + 0.4, 0])
        l1 = VGroup(T("resting", 26, GREEN), T("substrate", 26, GREEN)).arrange(DOWN, buff=0.06).move_to([3.95, -2.35, 0])
        self.play(Create(axis), FadeIn(grip), GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.8)

        self.at("strained transition", lead=0.35)
        ts = RoundedRectangle(corner_radius=0.1, width=0.98, height=1.5, stroke_color=AMBER, stroke_width=3,
                              fill_color=solid(AMBER, 0.4), fill_opacity=1).move_to([cx, J.top + 0.75, 0])
        b2 = Rectangle(width=1.0, height=2.4, stroke_width=0, fill_color=AMBER, fill_opacity=0.9)
        b2.move_to([5.65, base_y + 1.2, 0])
        l2 = VGroup(T("strained", 26, AMBER), T("transition", 26, AMBER), T("state", 26, AMBER)).arrange(DOWN, buff=0.06).move_to([5.65, -2.5, 0])
        leg_t = T("transition state", 30, AMBER).move_to([1.3, -2.7, 0])
        halo2 = SurroundingRectangle(ts, color=GOLD, buff=0.07, corner_radius=0.12, stroke_width=4)
        self.play(ReplacementTransform(sub, ts), ReplacementTransform(halo, halo2), *J.to(-6, 0.9), GrowFromEdge(b2, DOWN),
                  FadeIn(l2), Transform(leg_s, leg_t), run_time=1.0)

        self.at("Binding induces", lead=0.3)
        self.play(*self.settop("Binding induces the fit"), run_time=0.5)
        self.at("and water", lead=0.35)
        ghost = Jaws(4.2, -1.5, a=30, s=0.6)
        wchip = lab("water", TEAL, 30).move_to([4.2, 1.3, 0])
        dots = VGroup(*[d.move_to([4.2 + dx, 0.55, 0]) for d, dx in zip(water_dots(3, r=0.13), (-0.3, 0.0, 0.3))])
        self.play(FadeOut(Group(axis, grip, b1, l1, b2, l2, leg_e, leg_s, halo2)), FadeIn(ghost.group), pop(wchip), FadeIn(dots), run_time=0.6)
        self.at("too small", lead=0.3)
        too = T("too small to force it", 32, TEAL).move_to([4.0, -2.6, 0])
        inside = [(4.05, -1.0), (4.35, -1.0), (4.2, -0.72)]
        self.play(FadeIn(too), *[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dots, inside)], run_time=0.8)
        self.play(Indicate(ghost.group, color=BLUE, scale_factor=1.04), run_time=0.5)
        self.play(*[d.animate.shift(UP * 1.4) for d in dots], run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s04 the reviewers
class S04Review(ProfileScene):
    def construct(self):
        self.add_inset()
        # the idea cuts against the dogma
        idea = lab("induced fit", GOLD, 38).move_to([-0.55, 0.3, 0])
        dogma = RoundedRectangle(corner_radius=0.2, width=3.6, height=2.4, stroke_color=RED, stroke_width=3,
                                 fill_color=solid(RED, 0.2), fill_opacity=1).move_to([4.3, 0.3, 0])
        dl = T("the dogma", 44, RED, font=TITLE_FONT).move_to(dogma)
        self.play(pop(idea), run_time=0.4)
        self.at("cut so hard")
        self.play(FadeIn(dogma), FadeIn(dl), run_time=0.4)
        ar = Arrow([1.1, 0.3, 0], [2.4, 0.3, 0], buff=0, color=GOLD, stroke_width=7, max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(ar), run_time=0.5)
        self.play(Wiggle(dogma, scale_value=1.04, rotation_angle=0.03 * TAU, run_time=0.5))

        # the standard journals turn it away
        self.at("standard journals", lead=0.7)
        self.play(FadeOut(Group(idea, dogma, dl, ar)), run_time=0.35)
        paper = lab("the paper", GOLD, 34).move_to([-0.6, 0.3, 0])
        js = VGroup(*[lab("journal", PLACE, 34) for _ in range(3)]).arrange(DOWN, buff=0.4).move_to([4.5, 0.1, 0])
        jl = T("the standard journals", 32, PLACE).move_to([4.2, 2.55, 0])
        self.play(pop(paper), FadeIn(jl), LaggedStart(*[pop(j) for j in js], lag_ratio=0.2), run_time=0.8)
        self.at("turned it away", lead=0.2)
        target = js[1].get_left() + LEFT * 0.1
        self.play(paper.animate.move_to([target[0] - paper.width / 2, 0.1, 0]), run_time=0.45, rate_func=rush_into)
        bounce = paper.animate.move_to([-0.6, 0.1, 0])
        bar = Line(js[1].get_left() + LEFT * 0.12 + UP * 1.0, js[1].get_left() + LEFT * 0.12 + DOWN * 1.0, color=RED, stroke_width=6)
        self.play(bounce, Create(bar), run_time=0.5, rate_func=rush_from)
        away = T("turned away", 44, RED, font=TITLE_FONT).move_to([0.1, -1.5, 0])
        self.play(FadeIn(away, shift=UP * 0.1), run_time=0.4)

        # the reviewer's verdict
        self.at("One reviewer's verdict", lead=0.3)
        self.play(FadeOut(Group(paper, js, jl, bar, away)), run_time=0.35)
        rv = lab("one reviewer's verdict", GREY, 36).move_to([PANEL_C, 2.5, 0])
        self.play(pop(rv), run_time=0.4)
        self.at("became famous", lead=0.1)
        fam = T("famous", 52, GOLD, font=TITLE_FONT).move_to([PANEL_C, 1.2, 0])
        self.play(FadeIn(fam, shift=UP * 0.1), run_time=0.4)
        self.play(Create(Line(fam.get_corner(DL) + DOWN * 0.1, fam.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=4)), run_time=0.6)

        # the verdict, as two pairs
        self.at("What is new")
        new = T("new", 56, TEXT, font=TITLE_FONT).move_to([0.2, 0.5, 0])
        a1 = Arrow([1.1, 0.5, 0], [2.5, 0.5, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        self.play(FadeOut(fam), FadeIn(new, shift=UP * 0.1), run_time=0.4)
        self.at("is not true", lead=0.15)
        nt = T("not true", 56, RED, font=TITLE_FONT).move_to([4.5, 0.5, 0])
        self.play(GrowArrow(a1), FadeIn(nt, shift=LEFT * 0.15), run_time=0.5)
        self.at("and what is true")
        tr = T("true", 56, TEXT, font=TITLE_FONT).move_to([0.2, -1.4, 0])
        a2 = Arrow([1.1, -1.4, 0], [2.5, -1.4, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(tr, shift=UP * 0.1), run_time=0.4)
        self.at("is not new", lead=0.15)
        nn = T("not new", 56, RED, font=TITLE_FONT).move_to([4.5, -1.4, 0])
        self.play(GrowArrow(a2), FadeIn(nn, shift=LEFT * 0.15), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s05 proof
class S05Proof(ProfileScene):
    def construct(self):
        self.add_inset()
        # --- the paper slips through a loophole into PNAS in 1958
        mkw = lambda h, y: Rectangle(width=0.45, height=h, stroke_width=0, fill_color=PLACE, fill_opacity=0.5).move_to([1.6, y, 0])
        wall_t = mkw(1.05, 2.78)
        wall_b = mkw(2.55, -0.125)
        wl = T("standard journals", 28, PLACE).move_to([1.6, -1.85, 0])
        paper = lab("the paper", GOLD, 32).move_to([-0.8, 1.7, 0])
        self.play(pop(paper), FadeIn(wall_t), FadeIn(wall_b), FadeIn(wl), run_time=0.4)
        self.at("slipped")
        self.play(paper.animate.move_to([0.1, 1.7, 0]), run_time=0.7)
        self.at("PNAS", lead=0.3)
        pnas = lab("PNAS", PLACE, 38).move_to([5.4, 1.7, 0])
        self.play(pop(pnas), run_time=0.4)
        self.at("1958", lead=0.25)
        yr = M("1958", 52, YELLOW).move_to([5.4, 2.85, 0])
        self.play(Write(yr), run_time=0.5)
        self.at("through a loophole", lead=0.3)
        ll = T("loophole", 32, GOLD).move_to([-0.2, 2.85, 0])
        la = Arrow(ll.get_right() + RIGHT * 0.1, [1.38, 2.1, 0], buff=0, color=GOLD, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(ll), GrowArrow(la), paper.animate.move_to([3.05, 1.7, 0]), run_time=1.0)

        # --- X-ray crystallography proves him right
        self.at("and X ray", lead=0.4)
        self.play(FadeOut(Group(wall_t, wall_b, wl, paper, pnas, yr, ll, la)), run_time=0.3)
        src = lab("X-rays", GREY, 30).move_to([-0.6, 0.9, 0])
        crystal = RoundedRectangle(corner_radius=0.12, width=1.4, height=1.4, stroke_color=GREY, stroke_width=3,
                                   fill_color=solid(GREY, 0.3), fill_opacity=1).move_to([2.3, 0.9, 0])
        cl = T("crystal", 28, GREY).next_to(crystal, DOWN, buff=0.2)
        plate = Rectangle(width=0.45, height=3.2, stroke_color=GREY, stroke_width=3, fill_color=solid(GREY, 0.15),
                          fill_opacity=1).move_to([5.7, 0.9, 0])
        beam1 = Arrow(src.get_right() + RIGHT * 0.05, crystal.get_left() + LEFT * 0.05, buff=0, color=TEXT, stroke_width=5,
                      max_tip_length_to_length_ratio=0.25)
        self.play(pop(src), FadeIn(crystal), FadeIn(cl), run_time=0.35)
        self.play(GrowArrow(beam1), run_time=0.3)
        spots = VGroup()
        for dy in (0, 0.55, -0.55, 1.1, -1.1, 0.28, -0.28, 1.4, -1.4):
            spots.add(Dot([5.7, 0.9 + dy, 0], radius=0.07 + 0.06 * (1 - abs(dy) / 1.6), color=TEXT))
        rays = VGroup(*[Line(crystal.get_right(), [5.45, 0.9 + dy, 0], color=TEXT, stroke_width=2).set_opacity(0.55)
                        for dy in (0, 0.55, -0.55, 1.1, -1.1)])
        cap = T("X-ray crystallography", 34, GREY).move_to([PANEL_C, -1.2, 0])
        self.play(FadeIn(plate), Create(rays), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(sp, scale=0.3) for sp in spots], lag_ratio=0.08), FadeIn(cap), run_time=0.5)
        self.at("proved him right", lead=0.1)
        right = T("proved him right", 46, GOLD, font=TITLE_FONT).move_to([PANEL_C + 0.6, -2.4, 0])
        chk = VGroup(Line([-0.0, 0.0, 0], [0.22, -0.28, 0]), Line([0.22, -0.28, 0], [0.7, 0.4, 0])).set_color(GOLD).set_stroke(width=8)
        chk.next_to(right, LEFT, buff=0.3)
        self.play(FadeIn(right, shift=UP * 0.12), Create(chk), run_time=0.7)

        # --- enzymes flex, shift, and clamp down
        self.at("Enzymes", lead=0.5)
        self.play(FadeOut(Group(src, crystal, cl, plate, beam1, spots, rays, cap, right, chk)), run_time=0.35)
        cx, cy = PANEL_C, -1.5
        J = Jaws(cx, cy, a=24, s=1.15)
        sub = sub_block(1.27, 1.27).move_to([cx, J.top + 0.64, 0])
        self.play(FadeIn(J.group), FadeIn(sub), run_time=0.3)
        self.at("flex", lead=0.3)
        w1 = T("flex", 54, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.7, 0])
        self.play(FadeIn(w1, shift=UP * 0.1), *J.to(36, 0.35), run_time=0.35)
        self.play(*J.to(14, 0.35), run_time=0.35)
        self.play(*J.to(24, 0.25), run_time=0.25)
        self.at("shift", lead=0.3)
        w2 = T("shift", 54, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.7, 0])
        lean = radians(14)
        self.play(Succession(FadeOut(w1, run_time=0.15), FadeIn(w2, shift=UP * 0.1, run_time=0.2)),
                  Rotate(J.left, -lean, about_point=J.pl), Rotate(J.right, -lean, about_point=J.pr), run_time=0.35)
        self.play(Rotate(J.left, 2 * lean, about_point=J.pl), Rotate(J.right, 2 * lean, about_point=J.pr), run_time=0.35)
        self.play(Rotate(J.left, -lean, about_point=J.pl), Rotate(J.right, -lean, about_point=J.pr), run_time=0.2)
        self.at("clamp down", lead=0.2)
        w3 = T("clamp down", 54, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.7, 0])
        self.play(Succession(FadeOut(w2, run_time=0.15), FadeIn(w3, shift=UP * 0.1, run_time=0.35)), *J.to(0, 0.5), run_time=0.5)

        # --- from static shapes to moving machines
        self.at("He had moved", lead=0.2)
        self.play(FadeOut(Group(J.group, sub, w3)), run_time=0.35)
        bio = lab("biochemistry", GREY, 36).move_to([PANEL_C, 2.6, 0])
        self.play(pop(bio), run_time=0.4)
        self.at("biochemistry")
        self.play(Indicate(bio, color=TEXT, scale_factor=1.1), run_time=0.6)
        self.at("from a science", lead=0.2)
        lock = lock_enzyme(-0.4, -0.3, s=0.8)
        key = sub_block(1.2 * 0.8, 0.8 * 0.8, corner=0.07).move_to([-0.4, -0.3 - 0.05 * 0.8 + 0.4 * 0.8 + 0.02, 0])
        sl = T("static shapes", 32, GREY).move_to([-0.4, -1.9, 0])
        self.play(FadeIn(lock), FadeIn(key), run_time=0.5)
        self.at("static shapes", lead=0.2)
        self.play(FadeIn(sl, shift=UP * 0.1), run_time=0.4)
        self.at("to one of", lead=0.2)
        arr = Arrow([1.5, -0.3, 0], [2.7, -0.3, 0], buff=0, color=GOLD, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(arr), run_time=0.4)
        self.at("moving machines", lead=0.2)
        J2 = Jaws(4.55, -1.1, a=26, s=0.75)
        s2 = sub_block(0.95, 0.95, corner=0.08).move_to([4.55, J2.top + 0.48, 0])
        ml = T("moving machines", 32, GOLD).move_to([4.55, -1.9, 0])
        self.play(FadeIn(J2.group), FadeIn(s2), FadeIn(ml, shift=UP * 0.1), run_time=0.5)
        self.play(*J2.to(8, 0.6), run_time=0.6)
        self.play(*J2.to(26, 0.6), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 quote (silent)
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“What is new is not true,", "and what is true is not new.”"]
        q = VGroup(*[T(l, 44, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(q, max_w=8.4)
        who = VGroup(T("— an anonymous reviewer’s dismissal of", 28, GOLD),
                     T("Koshland’s induced-fit paper,", 28, GOLD),
                     T("as recounted in The Molecule Hunters", 24, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([PANEL_C, 0.0, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.9)
        self.wait(0.7)
        self.play(who.animate.set_opacity(1.0), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Induced fit (1958): the enzyme reshapes itself around what it binds."

    def construct(self):
        img, frame = portrait_pair(2.3)
        grp = Group(img, frame).move_to([0, 2.0, 0])
        cap = T(CAPTION, 22, GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.15)
        a = T("Induced fit (1958): the enzyme reshapes", 40, font=TITLE_FONT)
        b = T("itself around what it binds.", 40, font=TITLE_FONT)
        lg = VGroup(a, b).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · Daniel Koshland profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
