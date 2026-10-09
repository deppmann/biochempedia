"""Louis Pasteur: a scientist profile (Biochemistrypedia, vitalism lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story). The entry lists no quotes, so there is no quote scene; the silent
scene before the end card shows the entry's contribution line instead. The portrait is an
AI-generated engraving-style illustration from The Molecule Hunters; it is captioned
"illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and names: Pasteur's name/dates, Buechner in the contribution line
  GREEN  = life: living yeast, the living cell, "proved fermentation was alive", what the data showed
  YELLOW = fermentation and its products: the foam / alcohol, the fermentation bubbles and chip
  JUICE  = grape juice (violet)
  BLUE   = the air (sealed from it / open to it)
  TEAL   = Pasteur's empirical claim
  RED    = what went beyond the evidence or stood in the way: the claim past the data,
           "cannot be separated", the conviction and the forty-year orthodoxy
  GREY   = inert / dead / dismissed things: the inert sealed juice, the vital force, dead yeast
No molecular structure is drawn: flasks are schematic apparatus, yeast cells are plain dots,
the orthodoxy is forty bricks (one per year).
"""
import math
import random

import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = "/Users/deppmann/biochempedia/public/scientists/louis-pasteur.png"
CAPTION = "illustration · AI-generated"
JUICE = "#A78BDB"       # grape juice

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T("Louis Pasteur", size=34, font=TITLE_FONT)
    dt = T("1822–1895", size=28, color=GOLD)
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


def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16):
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)
        self.portrait_frame = frame


def flask(cx, cy, s=1.0, fill=JUICE):
    """Schematic Erlenmeyer-type flask (apparatus, not a molecule): returns (liquid, outline, helpers)."""
    pts = [(-.28, 1.3), (.28, 1.3), (.28, .5), (.95, -1.2), (-.95, -1.2), (-.28, .5)]
    outline = Polygon(*[[cx + x * s, cy + y * s, 0] for x, y in pts], color=TEXT, stroke_width=4)
    outline.round_corners(0.08 * s)
    lv = -0.1

    def hw(y):
        return .28 + (.5 - y) / 1.7 * .67
    liquid = Polygon([cx - hw(lv) * s, cy + lv * s, 0], [cx + hw(lv) * s, cy + lv * s, 0],
                     [cx + .95 * s, cy - 1.2 * s, 0], [cx - .95 * s, cy - 1.2 * s, 0],
                     stroke_width=0, fill_color=fill, fill_opacity=0.55)
    return liquid, outline


def yeast_dot(pos, color=GREEN, r=0.13, op=0.85):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op).move_to(pos)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = "Louis Pasteur"

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T("1822–1895", size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.1, 0.2, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(
            ScaleInPlace(grp, 1.08, run_time=4.2, rate_func=linear),
            Succession(
                Wait(0.4),
                FadeIn(VGroup(brand, lesson), shift=UP * 0.1, run_time=0.5),
                Wait(0.3),
                Write(name, run_time=0.9),
                Wait(0.3),
                FadeIn(dates, shift=UP * 0.1, run_time=0.5),
                GrowFromCenter(rule, run_time=0.4),
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


# ----------------------------------------------------------------------------- s01 sealed vs open
class S01Flasks(ProfileScene):
    def construct(self):
        self.add_inset()
        S = 1.2
        cy = 0.45
        lx, rx = 0.0, 4.2

        # "a real question"
        q = T("?", 150, GOLD, font=TITLE_FONT, weight=BOLD).move_to([PANEL_C, 0.2, 0])
        self.at("Pasteur", lead=0.0)
        self.play(FadeIn(q, scale=0.6), run_time=0.5)

        # grape juice, sealed from the air
        l_liq, l_out = flask(lx, cy, s=S)
        self.at("grape juice")
        self.play(FadeOut(q, scale=0.5), FadeIn(l_liq), Create(l_out), run_time=0.7)
        stopper = Rectangle(width=0.8, height=0.32, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                            fill_opacity=0.8).move_to([lx, cy + 1.3 * S + 0.16 + 0.7, 0])
        stopper.set_opacity(0)
        self.add(stopper)
        self.at("sealed")
        self.play(stopper.animate.set_opacity(1).move_to([lx, cy + 1.3 * S + 0.16, 0]), run_time=0.4)
        sealed_lab = T("sealed from the air", 26, BLUE).move_to([lx, -1.75, 0])
        self.at("from the air")
        self.play(pop(sealed_lab), run_time=0.4)
        inert = lab("inert", GREY, 30).move_to([lx, -2.6, 0])
        self.at("stayed inert")
        self.play(pop(inert), run_time=0.4)

        # open to airborne yeast
        r_liq, r_out = flask(rx, cy, s=S)
        open_lab = T("open to airborne yeast", 26, BLUE).move_to([rx - 0.05, -1.75, 0])
        self.at("while juice")
        self.play(FadeIn(r_liq), Create(r_out), run_time=0.45)
        self.at("open to")
        self.play(pop(open_lab), run_time=0.4)
        # yeast dots drift down into the neck, then into the juice
        starts = [[rx - 1.2 + 0.55 * i, cy + 2.45 - 0.15 * (i % 2), 0] for i in range(5)]
        ends = [[rx - 0.5 + 0.25 * i, cy - 0.7 - 0.22 * (i % 2), 0] for i in range(5)]
        dots = [yeast_dot(p) for p in starts]
        tips = [[rx + (i - 2) * 0.05, cy + 1.3 * S + 0.1, 0] for i in range(5)]
        self.at("airborne yeast")
        self.play(LaggedStart(*[
            Succession(FadeIn(d, scale=0.5, run_time=0.15),
                       d.animate(run_time=0.55).move_to(tips[i]),
                       d.animate(run_time=0.5).move_to(ends[i]))
            for i, d in enumerate(dots)], lag_ratio=0.15), run_time=0.8)

        # foams into alcohol
        fy = cy - 0.1 * S
        foam = VGroup(*[Circle(radius=0.11, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.55)
                        .move_to([rx - 0.55 + 0.275 * i, fy + (0.05 if i % 2 else 0.0), 0]) for i in range(5)])
        bubbles = VGroup(*[Circle(radius=0.07, stroke_color=YELLOW, stroke_width=2, fill_opacity=0)
                           .move_to([rx - 0.6 + 0.24 * i, cy - 0.95 - 0.12 * (i % 3), 0]) for i in range(6)])
        alcohol = lab("alcohol", YELLOW, 30).move_to([rx, -2.6, 0])
        self.at("foamed")
        self.play(r_liq.animate.set_fill(YELLOW, opacity=0.45), FadeIn(bubbles),
                  LaggedStart(*[GrowFromCenter(f) for f in foam], lag_ratio=0.1),
                  *[b.animate.shift(UP * 0.6) for b in bubbles], run_time=0.65)
        self.at("alcohol")
        self.play(pop(alcohol), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s02 biology, then the claim
class S02Claim(ProfileScene):
    def construct(self):
        self.add_inset()

        # ---- A: fermentation = biology; alongside living, multiplying yeast
        ferm = lab("fermentation", YELLOW, 30).move_to([0.1, 2.65, 0])
        eq = T("=", 40, TEXT).move_to([2.05, 2.65, 0])
        bio = lab("biology", GREEN, 30).move_to([3.4, 2.65, 0])
        self.at("Fermentation")
        self.play(pop(ferm), run_time=0.45)
        self.at("biology")
        self.play(FadeIn(eq), pop(bio), run_time=0.45)

        cols = [-0.5, 1.4, 3.3, 5.2]
        counts = [1, 2, 4, 8]
        base_y, cell_y = -2.0, 0.75
        ax_lab = T("fermentation", 26, YELLOW).move_to([2.35, base_y - 0.1, 0])
        row_lab = T("living, multiplying yeast", 26, GREEN).move_to([2.35, 1.9, 0])

        def grid(n, cx):
            if n == 1:
                offs = [(0, 0)]
            elif n == 2:
                offs = [(-.2, 0), (.2, 0)]
            elif n == 4:
                offs = [(-.2, .2), (.2, .2), (-.2, -.2), (.2, -.2)]
            else:
                offs = [(x, y) for y in (.2, -.2) for x in (-.6, -.2, .2, .6)]
            return VGroup(*[yeast_dot([cx + x, cell_y + y, 0], r=0.17) for x, y in offs])

        groups = [grid(n, cx) for n, cx in zip(counts, cols)]

        def foam(n, cx):
            """Fermentation bubbles that appear with each yeast group (no axis, no quantities)."""
            g = grid(n, cx)
            return VGroup(*[Circle(radius=0.12, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW,
                                   fill_opacity=0.5).move_to(d.get_center() + DOWN * 1.75) for d in g])
        foams = [foam(n, cx) for n, cx in zip(counts, cols)]

        self.at("only alongside")
        self.play(pop(ax_lab), run_time=0.5)
        self.at("living")
        self.play(pop(row_lab), FadeIn(groups[0], scale=0.6), FadeIn(foams[0], shift=UP * 0.25), run_time=0.5)
        self.at("multiplying")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(groups[i], scale=0.6), FadeIn(foams[i], shift=UP * 0.25))
                                for i in (1, 2, 3)], lag_ratio=0.28), run_time=1.0)

        partA = VGroup(ax_lab, row_lab, *groups, *foams, ferm, eq, bio)
        # ---- B: no vital force; an empirical claim; stronger than the data
        self.at("invoked", lead=0.7)
        self.play(FadeOut(partA), run_time=0.4)
        vital = lab("vital force", GREY, 30).move_to([-0.1, 2.65, 0])
        self.at("invoked")
        self.play(pop(vital), run_time=0.4)
        strike = Line(vital.get_left() + LEFT * 0.1, vital.get_right() + RIGHT * 0.1, color=RED, stroke_width=4)
        no_lab = T("no", 30, RED, weight=BOLD).next_to(vital, LEFT, buff=0.3)
        self.at("no vital")
        self.play(Create(strike), FadeIn(no_lab), run_time=0.35)
        emp = lab("empirical claim", TEAL, 30).move_to([4.3, 2.65, 0])
        self.at("empirical")
        self.play(pop(emp), run_time=0.45)

        x0, d_len, c_len = -2.0, 4.0, 7.6
        l1 = T("what his data showed", 26, GREEN).move_to([x0 + 1.85, 1.7, 0])
        l2 = T("what he claimed", 26, TEAL).move_to([x0 + 1.35, 0.2, 0])
        bar1 = Rectangle(width=d_len, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.85) \
            .move_to([x0 + d_len / 2, 1.1, 0])
        b2a = Rectangle(width=d_len, height=0.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.85) \
            .move_to([x0 + d_len / 2, -0.5, 0])
        b2b = Rectangle(width=c_len - d_len, height=0.5, stroke_width=0, fill_color=RED, fill_opacity=0.85) \
            .move_to([x0 + d_len + (c_len - d_len) / 2, -0.5, 0])
        bar2 = VGroup(b2a, b2b)
        self.at("stronger")
        self.play(pop(l2), GrowFromEdge(bar2, LEFT), run_time=0.7)
        self.at("than his data")
        self.play(pop(l1), GrowFromEdge(bar1, LEFT), run_time=0.7)
        beyond = DoubleArrow([x0 + d_len + 0.03, -1.15, 0], [x0 + c_len, -1.15, 0], color=RED, stroke_width=4, buff=0,
                             tip_length=0.15)
        beyond_lab = T("beyond the data", 26, RED).move_to([x0 + (d_len + c_len) / 2, -1.65, 0])
        self.at("required")
        self.play(GrowFromCenter(beyond), pop(beyond_lab), run_time=0.5)

        # ---- C: not separable from the living cell
        stage = VGroup(l1, l2, bar1, bar2, beyond, beyond_lab)
        cell_c = np.array([0.9, -0.3, 0.0])
        fchip = lab("fermentation", YELLOW, 26).move_to(cell_c)
        self.at("that fermentation")
        self.play(FadeOut(stage), run_time=0.3)
        self.play(pop(fchip), run_time=0.3)
        out = DashedLine(fchip.get_right() + RIGHT * 0.1, [5.4, -0.3, 0], color=RED, stroke_width=4, dash_length=0.14)
        out.add_tip(tip_length=0.2)
        xmark = VGroup(Line([-0.22, -0.22, 0], [0.22, 0.22, 0]), Line([-0.22, 0.22, 0], [0.22, -0.22, 0])) \
            .set_color(RED).set_stroke(width=8).move_to([3.45, -0.3, 0])
        no_sep = lab(["could not be", "separated"], RED, 26).move_to([4.7, 0.95, 0])
        self.at("could not")
        self.play(Create(out), run_time=0.6)
        self.at("separated")
        self.play(FadeIn(xmark, scale=1.6), pop(no_sep), run_time=0.45)
        membrane = Circle(radius=1.5, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.08) \
            .move_to(cell_c)
        cell_lab = T("the living cell", 28, GREEN).move_to([0.9, -2.3, 0])
        self.at("from the")
        self.play(Create(membrane), run_time=0.7)
        self.at("living cell")
        self.play(pop(cell_lab), Indicate(membrane, color=GREEN, scale_factor=1.04), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s03 forty-year orthodoxy
class S03Orthodoxy(ProfileScene):
    def construct(self):
        self.add_inset()
        self.at("From", lead=0.0)
        self.play(Indicate(self.portrait_frame, color=GOLD, scale_factor=1.05), run_time=0.7)
        proved = lab(["proved fermentation", "was alive"], GREEN, 28).move_to([0.2, 2.35, 0])
        self.at("proved")
        self.play(pop(proved), run_time=0.5)
        conv = lab(["that", "conviction"], RED, 28).move_to([4.9, 2.35, 0])
        arr = Arrow(proved.get_right() + RIGHT * 0.1, conv.get_left() + LEFT * 0.1, color=RED, stroke_width=4, buff=0,
                    max_tip_length_to_length_ratio=0.3)
        self.at("that conviction")
        self.play(GrowArrow(arr), pop(conv), run_time=0.5)

        # forty bricks, one per year
        bw, gap = 0.17, 0.03
        x_start = -2.0
        bricks = VGroup(*[Rectangle(width=bw, height=0.75, stroke_width=0, fill_color=RED, fill_opacity=0.85)
                          .move_to([x_start + bw / 2 + i * (bw + gap), 0.55, 0]) for i in range(40)])
        for i in (9, 19, 29, 39):
            bricks[i].set_fill(RED, opacity=1.0)
        self.at("hardened")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bricks], lag_ratio=0.045), run_time=1.9)
        brace = Brace(bricks, DOWN, color=GREY, buff=0.1)
        orth = T("forty-year orthodoxy", 30, RED, weight=BOLD).next_to(brace, DOWN, buff=0.15)
        self.at("orthodoxy")
        self.play(FadeIn(brace), pop(orth), run_time=0.5)

        # a flask of dead yeast
        liq, out = flask(0.0, -2.2, s=0.6, fill=GREY)
        dead = VGroup(*[yeast_dot([x, y, 0], color=GREY, r=0.07, op=0.7)
                        for x, y in [(-.2, -2.68), (.0, -2.76), (.22, -2.66), (-.08, -2.55), (.12, -2.84)]])
        flask_lab = T("a flask of dead yeast", 28, GREY).move_to([3.1, -2.2, 0])
        self.at("flask")
        self.play(FadeIn(liq), Create(out), FadeIn(dead), run_time=0.5)
        self.at("dead yeast")
        self.play(pop(flask_lab), run_time=0.4)

        random.seed(7)
        self.at("dissolve")
        self.play(
            LaggedStart(*[b.animate.shift([random.uniform(-0.1, 0.1), random.uniform(-0.25, 0.25), 0])
                          .scale(0.3).set_opacity(0) for b in bricks], lag_ratio=0.03),
            FadeOut(brace), orth.animate.set_opacity(0.35),
            Indicate(VGroup(liq, out), color=TEXT, scale_factor=1.08),
            run_time=1.1,
        )
        self.finish()


# ----------------------------------------------------------------------------- s04 the contribution (silent)
class S04Contrib(ProfileScene):
    def construct(self):
        self.add_inset()
        head = T("Contribution", 28, GOLD, weight=BOLD).move_to([PANEL_C - 1.4, 3.0, 0])
        rule = Line([-2.0, 2.6, 0], [6.0, 2.6, 0], color=GOLD, stroke_width=2).set_opacity(0.5)
        self.wait(0.3)
        self.play(FadeIn(head, shift=UP * 0.1), Create(rule), run_time=0.8)

        # 1. proved: living yeast does fermentation
        c1 = lab(["Proved fermentation was the", "work of living yeast"], GREEN, 30).move_to([1.5, 1.35, 0])
        icon1 = VGroup(*[yeast_dot([5.55 + dx, 1.35 + dy, 0], r=0.17) for dx, dy in
                         [(-.2, -.12), (.2, -.12), (0, .24)]])
        self.wait(0.4)
        self.play(Create(c1[0]), run_time=0.7)
        self.play(FadeIn(c1[1]), run_time=0.7)
        self.play(FadeIn(icon1, scale=0.6), run_time=0.5)
        self.play(Indicate(icon1, color=GREEN, scale_factor=1.15), run_time=0.4)
        self.wait(0.8)

        # 2. then held, to the end: inseparable from the intact cell
        link = Arrow([1.5, 0.55, 0], [1.5, -0.35, 0], color=GREY, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.35)
        then = T("then held, to the end,", 28, GREY).move_to([3.7, 0.1, 0]).shift(LEFT * 0.0)
        then.align_to(link, LEFT).shift(RIGHT * 0.35)
        c2 = lab(["the process was inseparable", "from the intact cell"], RED, 30).move_to([1.5, -1.2, 0])
        cell = Circle(radius=0.45, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.08)
        inner = Square(0.26, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.6)
        icon2 = VGroup(cell, inner).move_to([5.6, -1.2, 0])
        self.play(GrowArrow(link), FadeIn(then, shift=RIGHT * 0.1), run_time=0.8)
        self.play(Create(c2[0]), run_time=0.6)
        self.play(FadeIn(c2[1]), run_time=0.6)
        self.play(FadeIn(icon2, scale=0.6), run_time=0.5)
        self.wait(1.2)

        # 3. the last claim Buechner had to overturn
        last = T("the last claim Büchner had to overturn", 30, TEXT, t2c={"Büchner": GOLD}) \
            .move_to([PANEL_C - 0.2, -2.7, 0])
        fit(last, max_w=8.4)
        self.play(FadeIn(last, shift=UP * 0.12), run_time=0.8)
        self.wait(0.5)
        push = Arrow([6.3, -1.95, 0], [5.0, -1.45, 0], color=GOLD, stroke_width=5, buff=0)
        self.play(GrowArrow(push), run_time=0.4)
        self.play(Wiggle(VGroup(c2, icon2), scale_value=1.04, rotation_angle=0.02 * TAU), run_time=0.8)
        strike = VGroup(*[Line(ln.get_left() + LEFT * 0.08, ln.get_right() + RIGHT * 0.08, color=RED, stroke_width=5)
                          for ln in c2[1]])
        self.play(
            c2[1].animate.set_opacity(0.6), c2[0].animate.set_stroke(opacity=0.5), icon2.animate.fade(0.5),
            LaggedStart(*[Create(l) for l in strike], lag_ratio=0.4), FadeOut(push), run_time=0.9,
        )
        self.play(Indicate(c1, color=GREEN, scale_factor=1.05), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s05 end card
class S05End(EndCard):
    LINE = "Proved living yeast ferments; held fermentation inseparable from the intact cell."

    def construct(self):
        a = T("Proved living yeast ferments; held fermentation", size=40, font=TITLE_FONT)
        b = T("inseparable from the intact cell.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        fit(line, max_w=12.0)
        name = T("Louis Pasteur · 1822–1895", size=26, color=GOLD)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(name, line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(name, shift=UP * 0.1), run_time=self.beat(0.15))
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
