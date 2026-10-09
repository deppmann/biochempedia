"""David Phillips: a scientist profile  (Biochemistrypedia, enzyme-kinetics lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quote). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters (cropped to the figure); it is captioned
"illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Phillips himself: his name/dates, 1965, his reasoning (mechanism), the leap, "the good"
  BLUE   = the enzyme (lysozyme blob, its deep cleft, the folded model)
  GREEN  = Koshland and his motion (enzymes must move)
  PURPLE = sugar (the cell-wall chain)
  RED    = strain, stress, the snap, "enemy"
  YELLOW = signals and the camera (the photograph, radar pulses and echoes)
  TEAL   = the lesson rail viewer (the interactive cue)
  GREY   = axes, structure, de-emphasized things
No molecular structure is drawn: the enzyme is a schematic blob with a notch, the sugar chain is a row of
tiles joined by lines, the 129 amino acids are 129 plain dots, and the radar is pulses and a dashed outline.
"""
import math
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

HERE = Path(__file__).resolve().parent
PORTRAIT = str(HERE / "assets" / "portrait_crop.png")     # David Phillips engraving, cropped to the figure
CAPTION = "illustration · AI-generated"
PURPLE = "#B58CD9"
IMG_AR = 800 / 690.0

INSET_C = np.array([-4.5, 1.2, 0.0])
INSET_H = 3.0
PANEL_C = 1.95          # x center of the right panel (x from -2.3 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T("David Phillips", size=34, font=TITLE_FONT)
    dt = T("1924–1999", size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.25, 0])
    return g


def inset_group():
    img, frame = portrait_pair(INSET_H)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = caption_under(frame)
    tag = name_tag(frame)
    rule = Line([-2.5, -3.2, 0], [-2.5, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16):
    """Chip with one or more centered lines of text."""
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
    """SpokenScene that starts with the inset (portrait + name) already on screen."""

    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


def enzyme(r=1.55, color=BLUE, fill=0.28, nw=0.36, nh=1.3):
    """Schematic enzyme: a blob with a deep notch (the cleft) cut into the top. Centered on the origin."""
    body = Circle(radius=r)
    notch = Ellipse(width=nw * r, height=nh * r).move_to(UP * r)
    shape = Difference(body, notch, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill)
    return shape.move_to(ORIGIN)


def person(color=TEXT, s=1.0):
    head = Circle(radius=0.13 * s, stroke_width=0, fill_color=color, fill_opacity=1).shift(UP * 0.2 * s)
    body = RoundedRectangle(corner_radius=0.17 * s, width=0.46 * s, height=0.3 * s, stroke_width=0,
                            fill_color=color, fill_opacity=1).shift(DOWN * 0.1 * s)
    return VGroup(head, body)


def gear(r=0.5, color=GOLD):
    teeth = Star(n=8, outer_radius=r, inner_radius=r * 0.78, stroke_color=color, stroke_width=3,
                 fill_color=color, fill_opacity=0.25)
    hole = Circle(radius=r * 0.3, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(teeth, hole)


def book(s=1.0, color=GREY):
    cover = RoundedRectangle(corner_radius=0.08 * s, width=2.0 * s, height=2.6 * s, stroke_color=color,
                             stroke_width=3, fill_color=color, fill_opacity=0.12)
    spine = Line(cover.get_left() + RIGHT * 0.22 * s + UP * 1.3 * s, cover.get_left() + RIGHT * 0.22 * s + DOWN * 1.3 * s,
                 color=color, stroke_width=3)
    return VGroup(cover, spine)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = "David Phillips"

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T("1924–1999", size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.1, 0.2, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(
            ScaleInPlace(grp, 1.07, run_time=2.0, rate_func=linear),
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


# ----------------------------------------------------------------------------- s01 hold still
class S01HoldStill(ProfileScene):
    def construct(self):
        self.add_inset()
        C = np.array([PANEL_C, -0.45, 0.0])
        base = enzyme(1.25, nw=0.42, nh=1.5)
        clock = ValueTracker(0.0)
        amp = ValueTracker(1.0)

        def wob():
            t, a = clock.get_value(), amp.get_value()
            m = base.copy()
            m.rotate(0.24 * a * math.sin(t * 8.5))
            m.stretch(1 + 0.09 * a * math.sin(t * 13.0 + 1.0), 0)
            m.stretch(1 - 0.09 * a * math.sin(t * 13.0 + 1.0), 1)
            return m.move_to(C)

        blob = always_redraw(wob)

        kosh = lab("Koshland", GREEN, 32).move_to([-0.2, 2.5, 0])
        self.at("Koshland")
        self.play(pop(kosh), run_time=0.45)

        # motion arrows (his claim: enzymes must move)
        arrows = VGroup(*[
            Arc(radius=1.75, start_angle=a0, angle=0.55, arc_center=C, color=GREEN, stroke_width=5)
            .add_tip(tip_length=0.2) for a0 in (0.35, 0.35 + math.pi * 2 / 3, 0.35 + math.pi * 4 / 3)])
        self.at("enzymes")
        self.add(blob)
        self.play(FadeIn(blob), run_time=0.4)
        self.at("must move")
        self.play(clock.animate.set_value(3.6), FadeIn(arrows), run_time=1.4, rate_func=linear)

        phil = lab("David Phillips", GOLD, 32).move_to([4.2, 2.5, 0])
        self.at("David Phillips")
        self.play(pop(phil), run_time=0.45)

        self.at("hold still", lead=0.3)
        self.play(amp.animate.set_value(0.0), clock.animate.set_value(4.6), FadeOut(arrows), run_time=0.9,
                  rate_func=smooth)
        blob.clear_updaters()

        # the camera: viewfinder corners close in on the still enzyme
        w, h, k = 1.95, 1.95, 0.5
        corners = VGroup()
        for sx, sy in ((-1, 1), (1, 1), (1, -1), (-1, -1)):
            p = C + np.array([sx * w, sy * h, 0.0])
            corners.add(VGroup(Line(p, p - np.array([sx * k, 0, 0]), color=YELLOW, stroke_width=6),
                               Line(p, p - np.array([0, sy * k, 0]), color=YELLOW, stroke_width=6)))
        self.at("long enough")
        self.play(FadeIn(corners, scale=1.2), run_time=0.5)
        self.at("photograph", lead=0.1)
        flash = Rectangle(width=2 * w, height=2 * h, stroke_width=0, fill_color=WHITE, fill_opacity=0.9).move_to(C)
        self.play(FadeIn(flash, run_time=0.08))
        self.play(FadeOut(flash), corners.animate.scale(0.88, about_point=C), run_time=0.45)
        self.finish()


# ----------------------------------------------------------------------------- s02 lysozyme, 1965
class S02Lysozyme(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.55
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([-0.7, ay, 0], radius=0.13, color=GOLD)
        date = T("1965", 40, GOLD, weight=BOLD).move_to([-0.7, ay + 0.55, 0])
        self.at("1965")
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.7)

        self.play(Indicate(date, color=GOLD, scale_factor=1.12), run_time=0.7)
        first = lab(["the first atom-by-atom", "structure of an enzyme"], BLUE, 30).move_to([PANEL_C, 1.4, 0])
        line2 = first[1][1]
        line2.set_opacity(0)
        self.at("first atom by atom", lead=0.3)
        self.play(FadeIn(first[0]), FadeIn(first[1][0], shift=UP * 0.1), run_time=0.6)
        self.at("structure of an enzyme", lead=0.2)
        self.play(line2.animate.set_opacity(1), run_time=0.5)

        lyso = lab("hen egg-white lysozyme", BLUE, 32).move_to([PANEL_C, -0.45, 0])
        link = Arrow(first.get_bottom(), lyso.get_top(), color=BLUE, stroke_width=4, buff=0.08,
                     max_tip_length_to_length_ratio=0.35)
        self.at("Hen egg white lysozyme", lead=0.1)
        self.play(GrowArrow(link), pop(lyso), run_time=0.6)

        # the viewer on the lesson rail: open it and rotate it
        win = RoundedRectangle(corner_radius=0.12, width=5.6, height=2.2, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.08).move_to([PANEL_C, -2.15, 0])
        bar = Line(win.get_corner(UL) + DOWN * 0.55 + RIGHT * 0.03, win.get_corner(UR) + DOWN * 0.55 + LEFT * 0.03,
                   color=TEAL, stroke_width=2)
        rail = T("the rail", 24, TEAL).move_to(win.get_corner(UL) + DOWN * 0.29 + RIGHT * 0.8)
        mini = enzyme(0.38, nw=0.42, nh=1.5).move_to(win.get_center() + DOWN * 0.3 + LEFT * 1.6)
        ring = Arc(radius=0.62, start_angle=0.5, angle=4.6, arc_center=mini.get_center(), color=TEAL, stroke_width=4) \
            .add_tip(tip_length=0.18)
        verbs = T("open and rotate", 28, TEAL).move_to(win.get_center() + DOWN * 0.3 + RIGHT * 0.7)
        self.at("the very structure", lead=0.2)
        self.play(FadeIn(win), FadeIn(bar), FadeIn(rail), FadeIn(mini), run_time=0.6)
        self.at("open and rotate", lead=0.2)
        self.play(FadeIn(verbs, shift=LEFT * 0.1), Create(ring), run_time=0.6)
        self.play(Rotate(mini, angle=-2 * PI, about_point=mini.get_center()), run_time=1.3, rate_func=smooth)
        self.finish()


# ----------------------------------------------------------------------------- s03 the mechanism
class S03Mechanism(ProfileScene):
    def construct(self):
        self.add_inset()

        # --- three days of reasoning: the fold, but above all the mechanism
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.6, height=0.6, stroke_color=GOLD, stroke_width=3,
                                          fill_color=GOLD, fill_opacity=0.0) for _ in range(3)]).arrange(RIGHT, buff=0.18)
        boxes.move_to([-0.55, 2.55, 0])
        days = T("three days of reasoning", 32, GOLD).next_to(boxes, RIGHT, buff=0.4)
        self.at("three day burst")
        self.add(boxes)
        self.play(LaggedStart(*[b.animate.set_fill(GOLD, opacity=0.85) for b in boxes], lag_ratio=0.5),
                  FadeIn(days, shift=RIGHT * 0.1), run_time=1.5)
        self.play(Indicate(days, color=GOLD, scale_factor=1.08), run_time=0.6)

        fold = lab("the fold", GREY, 32).move_to([0.6, 0.7, 0])
        self.at("the fold")
        self.play(pop(fold), run_time=0.45)
        mech = lab("the mechanism", GOLD, 38, fill=0.22).move_to([4.2, 0.7, 0])
        arrow = Arrow(fold.get_right() + RIGHT * 0.1, mech.get_left() + LEFT * 0.1, color=GOLD, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.3)
        self.at("but the mechanism", lead=0.3)
        self.play(GrowArrow(arrow), pop(mech), fold.animate.set_opacity(0.5), run_time=0.6)
        self.play(Indicate(mech, color=GOLD, scale_factor=1.08), run_time=0.7)

        # --- the enzyme and its cleft
        stage1 = VGroup(boxes, days, fold, arrow, mech)
        R = 1.55
        BC = np.array([PANEL_C, -1.35, 0.0])
        blob = enzyme(R, nw=0.42, nh=1.5).move_to(BC)
        self.at("enzyme's", lead=0.5)
        self.play(FadeOut(stage1), run_time=0.4)
        self.play(FadeIn(blob), run_time=0.5)
        cleft_lab = T("deep cleft", 30, BLUE).move_to([-0.75, -0.85, 0])
        cleft_ptr = Arrow(cleft_lab.get_right() + RIGHT * 0.05, [PANEL_C - 0.12, -0.55, 0], color=BLUE, stroke_width=4,
                          buff=0.05, max_tip_length_to_length_ratio=0.3)
        self.at("deep cleft")
        self.play(FadeIn(cleft_lab, shift=RIGHT * 0.1), GrowArrow(cleft_ptr), run_time=0.5)

        # grip arrows at the two lips of the cleft
        lip_y = BC[1] + R - 0.05
        grip = VGroup(
            Arrow([PANEL_C - 1.3, lip_y - 0.05, 0], [PANEL_C - 0.5, lip_y + 0.0, 0], color=BLUE, stroke_width=6, buff=0,
                  max_tip_length_to_length_ratio=0.3),
            Arrow([PANEL_C + 1.3, lip_y - 0.05, 0], [PANEL_C + 0.5, lip_y + 0.0, 0], color=BLUE, stroke_width=6, buff=0,
                  max_tip_length_to_length_ratio=0.3))
        self.at("grips")
        self.play(FadeIn(grip, scale=1.2), run_time=0.4)

        # --- the sugar chain, inside the bacterial cell wall
        cy = 0.85
        xs = [PANEL_C + (i - 3) * 0.88 for i in range(7)]
        tiles = []
        for x in xs:
            sq = RoundedRectangle(corner_radius=0.09, width=0.72, height=0.72, stroke_color=PURPLE, stroke_width=3,
                                  fill_color=PURPLE, fill_opacity=0.25).move_to([x, cy, 0])
            tiles.append(sq)
        stress = ValueTracker(0.0)

        def link(i):
            def make():
                a, b = tiles[i].get_center(), tiles[i + 1].get_center()
                d = (b - a) / np.linalg.norm(b - a)
                col = PURPLE
                wd = 4
                if i == 3:
                    col = interpolate_color(ManimColor(PURPLE), ManimColor(RED), stress.get_value())
                    wd = 4 + 2 * stress.get_value()
                return Line(a + d * 0.36, b - d * 0.36, color=col, stroke_width=wd).set_z_index(1)
            return always_redraw(make)

        links = VGroup(*[link(i) for i in range(6)])
        sugar_lab = T("sugar chain", 30, PURPLE).move_to([-0.1, 2.15, 0])
        self.at("sugar chain")
        self.add(links)
        self.play(FadeIn(sugar_lab, shift=DOWN * 0.1),
                  LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tiles], lag_ratio=0.12), run_time=1.0)

        wall = RoundedRectangle(corner_radius=0.2, width=7.8, height=1.25, stroke_color=GREY, stroke_width=2.5,
                                fill_color=GREY, fill_opacity=0.08).move_to([PANEL_C + 0.2, cy + 0.03, 0]).set_z_index(-1)
        wall_lab = T("bacterial cell wall", 28, GREY).move_to([4.2, 2.15, 0])
        self.at("bacterial cell wall")
        self.play(Create(wall), FadeIn(wall_lab, shift=DOWN * 0.1), run_time=0.8)

        # --- the sugar can't fit
        mid = tiles[3]
        self.at("the sugar", nth=1, lead=0.1)
        self.play(Indicate(mid, color=PURPLE, scale_factor=1.2), run_time=0.4)
        self.at("can't fit", lead=0.3)
        push = Arrow([PANEL_C, cy + 1.2, 0], [PANEL_C, cy + 0.45, 0], color=RED, stroke_width=5, buff=0,
                     max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(push), mid.animate.shift(DOWN * 0.18), run_time=0.3)
        bump = VGroup(Line([-0.2, -0.2, 0], [0.2, 0.2, 0]), Line([-0.2, 0.2, 0], [0.2, -0.2, 0])) \
            .set_color(RED).set_stroke(width=7).move_to([PANEL_C + 0.8, cy - 0.45, 0])
        self.play(FadeIn(bump, scale=1.5), mid.animate.set_color(RED), run_time=0.2)
        self.play(FadeOut(push), FadeOut(bump), mid.animate.shift(UP * 0.18).set_color(PURPLE), run_time=0.2)

        # --- it must bend: the tile kinks and dips into the cleft
        kinked = Polygon([-0.25, 0.36, 0], [0.0, 0.1, 0], [0.25, 0.36, 0], [0.25, -0.36, 0], [-0.25, -0.36, 0],
                         stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.3)
        kinked.move_to([PANEL_C, cy - 1.05, 0])
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.09, width=0.72, height=0.72, stroke_color=RED,
                                                stroke_width=3).move_to([PANEL_C, cy - 1.05, 0]), num_dashes=20)
        self.at("without bending")
        self.play(FadeOut(grip), FadeOut(cleft_ptr), Transform(mid, kinked), run_time=0.9, rate_func=smooth)
        self.add(ghost)
        half = T("“half-chair”", 30, RED).move_to([5.1, -0.35, 0])
        half_ptr = DashedLine(half.get_left() + LEFT * 0.05, [PANEL_C + 0.35, cy - 1.05, 0], color=RED, stroke_width=3,
                              dash_length=0.1)
        self.at("strained")
        self.play(Indicate(mid, color=RED, scale_factor=1.15), run_time=0.7)
        self.at("half chair", lead=0.1)
        self.play(FadeIn(half, shift=LEFT * 0.1), Create(half_ptr), run_time=0.5)

        # --- wrenched out of true
        self.at("wrenched")
        self.play(Rotate(mid, angle=-0.55, about_point=mid.get_center()), run_time=0.9)
        arc = Arc(radius=0.55, start_angle=PI / 2 + 0.55 - 0.55, angle=-0.55, arc_center=mid.get_center(), color=RED, stroke_width=4)
        self.play(Create(arc), run_time=0.4)

        # --- bonds primed to snap
        self.at("primed to snap", lead=0.9)
        self.play(stress.animate.set_value(1.0),
                  *[t.animate.shift(RIGHT * 0.22) for t in tiles[4:]], run_time=1.1, rate_func=smooth)
        self.at("snap", lead=0.15)
        a, b = tiles[3].get_center(), tiles[4].get_center()
        links[3].clear_updaters()
        mid_pt = (a + b) / 2
        stub_l = Line(a + (b - a) / np.linalg.norm(b - a) * 0.36, mid_pt, color=RED, stroke_width=6)
        stub_r = Line(mid_pt, b - (b - a) / np.linalg.norm(b - a) * 0.36, color=RED, stroke_width=6)
        self.remove(links[3])
        self.add(stub_l, stub_r)
        self.play(Flash(mid_pt, color=RED, flash_radius=0.45, line_length=0.18),
                  stub_l.animate.shift(LEFT * 0.12 + DOWN * 0.08), stub_r.animate.shift(RIGHT * 0.12 + UP * 0.05),
                  *[t.animate.shift(RIGHT * 0.12) for t in tiles[4:]], run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s04 radar and a leap
class S04Radar(ProfileScene):
    def construct(self):
        self.add_inset()

        # --- catalysis becomes engineering
        cat = lab("catalysis", BLUE, 34).move_to([-0.3, 0.9, 0])
        self.at("Catalysis")
        self.play(pop(cat), run_time=0.45)
        eng = lab(["a problem", "in engineering"], GOLD, 34).move_to([3.3, 0.9, 0])
        gr = gear(0.5).move_to([5.7, 0.9, 0])
        arr = Arrow(cat.get_right() + RIGHT * 0.1, eng.get_left() + LEFT * 0.1, color=GOLD, stroke_width=4, buff=0,
                    max_tip_length_to_length_ratio=0.25)
        self.at("problem in engineering", lead=0.3)
        self.play(GrowArrow(arr), pop(eng), FadeIn(gr, scale=0.7), run_time=0.7)
        self.play(Rotate(gr, angle=PI / 4, about_point=gr.get_center()), run_time=0.8)

        # --- wartime radar officer: a dish, pulses out, echoes back from an unseen object
        sy = 0.3
        SX, OX = -0.9, 4.5
        stage_a = VGroup(cat, arr, eng, gr)
        dish = Arc(radius=0.75, start_angle=2 * PI / 3, angle=2 * PI / 3, arc_center=[SX + 0.75, sy, 0], color=TEXT,
                   stroke_width=7)
        mount = Line([SX, sy, 0], [SX, sy - 1.1, 0], color=TEXT, stroke_width=7)
        feed = Dot([SX + 0.2, sy, 0], radius=0.09, color=YELLOW)
        station = VGroup(dish, mount, feed)
        officer = T("wartime radar officer", 30, TEXT).move_to([SX + 1.3, sy - 2.2, 0])
        self.at("A wartime radar officer")
        self.play(FadeOut(stage_a), run_time=0.4)
        self.play(FadeIn(station), FadeIn(officer, shift=UP * 0.1), run_time=0.6)

        # unseen object (dashed outline)
        obj = RoundedRectangle(corner_radius=0.22, width=1.7, height=1.7, stroke_color=GREY, stroke_width=3,
                               fill_opacity=0).move_to([OX, sy, 0])
        obj_d = DashedVMobject(obj, num_dashes=24).set_color(GREY)
        q = T("?", 64, GREY).move_to(obj.get_center())

        tt = ValueTracker(0.0)          # seconds since the first pulse left the dish
        SPEED = 2.8
        r_max = OX - 0.85 - (SX + 0.2)
        t_hit = r_max / SPEED

        def pulses():
            g = VGroup()
            for k in range(3):
                r = SPEED * tt.get_value() - 0.8 * k
                if 0.3 < r < r_max:
                    g.add(Arc(radius=r, start_angle=-0.32, angle=0.64, arc_center=[SX + 0.2, sy, 0], color=YELLOW,
                              stroke_width=6))
            return g

        def echoes():
            g = VGroup()
            for k in range(3):
                r = SPEED * (tt.get_value() - t_hit) - 0.8 * k
                if 0.3 < r < r_max + 0.1:
                    g.add(Arc(radius=r, start_angle=PI - 0.32, angle=0.64, arc_center=[OX - 0.85, sy, 0], color=YELLOW,
                              stroke_width=5).set_stroke(opacity=0.6))
            return g

        pul, ech = always_redraw(pulses), always_redraw(echoes)
        self.add(pul, ech)

        sig = T("invisible signals", 30, YELLOW).move_to([PANEL_C + 0.6, 2.6, 0])
        never = T("never seen", 28, GREY).move_to([OX, sy - 1.3, 0])
        self.at("reading", lead=0.2)
        self.play(
            tt.animate.set_value(3.4),
            FadeIn(obj_d, run_time=0.5),
            Succession(Wait(0.45), FadeIn(sig, shift=DOWN * 0.1, run_time=0.4)),
            Succession(Wait(2.4), AnimationGroup(FadeIn(q), FadeIn(never, shift=UP * 0.1), run_time=0.4)),
            run_time=3.4, rate_func=linear)

        # --- the leap: from echoes to the object
        self.at("trusted that kind of", lead=0.1)
        leap = CurvedArrow([SX + 1.4, sy + 1.2, 0], [OX - 0.5, sy + 1.25, 0], angle=-1.1, color=GOLD, stroke_width=6,
                           tip_length=0.28)
        leap_lab = T("leap", 40, GOLD, weight=BOLD).move_to([PANEL_C + 0.8, sy + 2.35, 0])
        self.play(FadeOut(sig), run_time=0.2)
        self.play(Create(leap), FadeIn(leap_lab, shift=DOWN * 0.1), run_time=0.7)
        self.play(obj.animate.set_fill(GOLD, opacity=0.35).set_stroke(GOLD), FadeOut(obj_d),
                  FadeOut(never), q.animate.set_color(GOLD), FadeIn(obj), run_time=0.6)

        # --- pragmatism, pressed on students
        stage_b = VGroup(station, officer, obj, q, leap, leap_lab, pul, ech)
        self.at("pressed", lead=0.2)
        phil = person(GOLD, 1.6).move_to([-1.3, 1.9, 0])
        arr2 = Arrow([-0.6, 1.9, 0], [2.7, 1.9, 0], color=GOLD, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.2)
        prag = lab("pragmatism", GOLD, 30).move_to([1.05, 2.55, 0])
        self.play(FadeOut(stage_b), FadeIn(phil, scale=0.8), run_time=0.4)
        self.at("pragmatism", lead=0.1)
        self.play(GrowArrow(arr2), pop(prag), run_time=0.6)
        studs = VGroup(*[person(TEXT, 1.0) for _ in range(4)]).arrange(RIGHT, buff=0.22).move_to([4.6, 1.9, 0])
        stud_lab = T("students", 28, TEXT).next_to(studs, DOWN, buff=0.18)
        self.at("students", lead=0.1)
        self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.15) for s in studs], lag_ratio=0.2), FadeIn(stud_lab), run_time=0.8)

        # --- the best is the enemy of the good
        best = lab("the best", GREY, 34).move_to([-0.2, -0.9, 0])
        good = lab("the good", GOLD, 34, fill=0.22).move_to([4.8, -0.9, 0])
        enemy_arr = Arrow(best.get_right() + RIGHT * 0.1, good.get_left() + LEFT * 0.1, color=RED, stroke_width=5, buff=0,
                          max_tip_length_to_length_ratio=0.2)
        enemy = T("enemy of", 32, RED).next_to(enemy_arr, UP, buff=0.15)
        self.at("the best", lead=0.1)
        self.play(pop(best), run_time=0.45)
        self.at("enemy", lead=0.1)
        self.play(GrowArrow(enemy_arr), FadeIn(enemy, shift=DOWN * 0.1), run_time=0.6)
        self.at("the good", lead=0.2)
        self.play(pop(good), run_time=0.45)
        self.finish()


# ----------------------------------------------------------------------------- s05 the skeletal model
class S05Model(ProfileScene):
    def construct(self):
        self.add_inset()
        cols_w = 32 * 0.2
        model = lab("skeletal model", GOLD, 44, fill=0.2).move_to([PANEL_C, 0.3, 0])
        self.at("skeletal model")
        self.play(pop(model), run_time=0.5)
        self.at("he built", lead=0.1)
        tray = DashedVMobject(Rectangle(width=cols_w + 0.5, height=1.2 + 0.3, stroke_color=GREY, stroke_width=2),
                              num_dashes=60).set_stroke(opacity=0.6).move_to([PANEL_C, 0.45, 0])
        self.play(model.animate.scale(0.7).move_to([PANEL_C, 3.0, 0]), Create(tray, run_time=1.2), run_time=1.3,
                  rate_func=smooth)

        # 129 dots, one per amino acid, in a flat strip of 4 rows
        N = 129
        cols = 33
        pitch = 0.2
        x0 = PANEL_C - (cols - 1) * pitch / 2
        dots = VGroup(*[Dot([x0 + (i % cols) * pitch, 1.05 - (i // cols) * 0.3, 0], radius=0.07, color=BLUE)
                        for i in range(N)])
        count = ValueTracker(0)
        num = always_redraw(lambda: M(f"{int(round(count.get_value()))}", 56, BLUE, weight=BOLD)
                            .move_to([PANEL_C - 1.1, 2.05, 0]).set_z_index(3))
        aa = T("amino acids", 32, BLUE).move_to([PANEL_C + 0.9, 2.05, 0])
        self.at("129", lead=0.25)
        self.add(num)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.006),
                  count.animate.set_value(N), FadeIn(aa), run_time=0.85, rate_func=linear)

        # fold: dots collapse into a compact blob
        BCX, BCY = 4.0, -0.6
        golden = math.pi * (3 - math.sqrt(5))
        folded = []
        for i in range(N):
            r = 1.2 * math.sqrt((i + 0.5) / N)
            folded.append(np.array([BCX + r * math.cos(i * golden), BCY + r * math.sin(i * golden), 0.0]))
        self.at("folded", lead=0.15)
        self.play(*[d.animate.move_to(p) for d, p in zip(dots, folded)], FadeOut(tray), run_time=0.7,
                  rate_func=smooth)

        # life size vs a hundred million times
        speck = Dot([-1.2, BCY, 0], radius=0.025, color=BLUE)
        life = T("life size", 28, GREY).move_to([-1.2, BCY - 0.55, 0])
        times = T("× 100 million", 34, GOLD, weight=BOLD).move_to([0.75, BCY + 0.65, 0])
        grow = Arrow([-0.6, BCY, 0], [2.4, BCY, 0], color=GOLD, stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.2)
        self.at("100 million times", lead=0.1)
        self.play(GrowArrow(grow), FadeIn(times, shift=DOWN * 0.1), FadeIn(speck, scale=3), run_time=0.7)
        self.at("life size", lead=0.2)
        self.play(FadeIn(life, shift=UP * 0.1), Indicate(speck, color=BLUE, scale_factor=3), run_time=0.6)

        # the picture of an enzyme: onto the cover of a book
        bk = book(1.0).move_to([PANEL_C, -0.2, 0])
        self.at("became the picture")
        blob_all = VGroup(*dots)
        self.play(FadeOut(speck), FadeOut(life), FadeOut(times), FadeOut(grow), FadeOut(model), FadeOut(num), FadeOut(aa),
                  run_time=0.4)
        self.play(FadeIn(bk), blob_all.animate.scale(0.5).move_to(bk.get_center() + RIGHT * 0.1), run_time=0.8)
        pic = VGroup(bk, blob_all)

        # ... in every textbook that followed
        self.at("every textbook")
        xs = [-0.2, 1.65, 3.5, 5.35]
        copies = [pic.copy().scale(0.7).move_to([x, 0.3, 0]) for x in xs]
        self.play(Transform(pic, copies[0]), run_time=0.5)
        extra = [c for c in copies[1:]]
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in extra], lag_ratio=0.3), run_time=1.0)
        every = T("every textbook that followed", 32, TEXT).move_to([PANEL_C + 0.2, -1.9, 0])
        self.play(FadeIn(every, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“Don't let the best be the", "enemy of the good.”"]
        q = VGroup(*[T(l, 44, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(q, max_w=8.4)
        who = T("— David Phillips", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.9)
        self.wait(0.6)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "First atom-by-atom enzyme structure — lysozyme — caught bending its sugar substrate."

    def construct(self):
        a = T("First atom-by-atom enzyme structure — lysozyme —", size=36, font=TITLE_FONT)
        b = T("caught bending its sugar substrate.", size=36, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
