"""Linus Pauling: a scientist profile (Biochemistrypedia, protein-3d-structure lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time: Pauling's name/dates, timeline markers and date labels
  TEAL   = Pauling's chemistry: the chain/strip, the coil, "from the bonds alone", the 5.4 he calculated
  YELLOW = tools and data: paper, slide rule, the 5.1 measured for keratin, the DNA photographs
  RED    = what went wrong or stood in the way: the infection, the discrepancy, the passport, "missed"
  PLACE (lavender) = places and institutions: Oxford, London, the State Department
           (not BLUE: BLUE #58C4DD is too close to TEAL to read as a different concept)
  GREEN  = hydrogen bonds (NH to CO)
  GREY   = axes, rulers, de-emphasized things (the mystery novels)
No molecular structure is drawn: the chain is a strip of numbered residue tiles, the coil is an
end-on arrangement of those tiles, and the numbers are plotted as plain bars.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = "/Users/deppmann/biochempedia/public/scientists/linus-pauling.png"
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"       # places and institutions

# left column (portrait inset + name), right panel (the story animates here)
INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    """(image, frame) at the given height, centered on the origin."""
    img = ImageMobject(PORTRAIT).set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T("Linus Pauling", size=34, font=TITLE_FONT)
    dt = T("1901–1994", size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.3, 0])
    return g


def inset_group():
    """Left column used by every content scene: framed portrait, caption, name and dates."""
    img, frame = portrait_pair(INSET_H)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = caption_under(frame)
    tag = name_tag(frame)
    rule = Line([-2.7, -3.2, 0], [-2.7, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16):
    """Chip with one or more centered lines of text."""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1   # same box height whatever the letters
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


def tile(n, color=TEAL, size=0.62, fs=26):
    sq = RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color, stroke_width=3,
                          fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.2), fill_opacity=1)
    return VGroup(sq, M(str(n), fs, color).move_to(sq))


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = "Linus Pauling"

    def construct(self):
        # portrait first, slow push-in; name and dates appear beside it
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T("1901–1994", size=38, color=GOLD)
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
        # glide to the inset position the content scenes start from
        i_img, i_frame, i_cap, i_tag, i_rule = inset_group()
        self.play(
            FadeOut(txt), FadeOut(cap),
            img.animate.set_height(INSET_H).move_to(INSET_C), frame.animate.become(i_frame),
            run_time=0.7,
        )
        self.play(FadeIn(i_cap), FadeIn(i_tag), FadeIn(i_rule), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------- s01 Oxford, 1948
class S01Oxford(ProfileScene):
    def construct(self):
        self.add_inset()
        axis_y = 2.3
        axis = Arrow([-2.2, axis_y, 0], [6.1, axis_y, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([-1.2, axis_y, 0], radius=0.12, color=GOLD)
        date = T("March 1948", 36, GOLD, weight=BOLD).next_to(dot, UP, buff=0.22, aligned_edge=LEFT).shift(LEFT * 0.3)
        self.at("March 1948")
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.6)

        oxford = lab("Oxford", PLACE, 30)
        oxford.next_to(date, RIGHT, buff=0.7).align_to(date, DOWN).shift(DOWN * 0.04)
        self.at("Oxford")
        self.play(pop(oxford), run_time=0.45)

        sinus = lab("sinus infection", RED, 30).move_to([0.0, 0.6, 0])
        self.at("sinus infection")
        self.play(pop(sinus), run_time=0.45)

        novels = lab("mystery novels", GREY, 30).move_to([4.0, 0.6, 0])
        self.at("reading mystery novels")
        self.play(pop(novels), run_time=0.45)
        strike = Line(novels.get_left() + RIGHT * 0.05, novels.get_right() - RIGHT * 0.05, color=GREY, stroke_width=5)
        self.at("bored him")
        self.play(Create(strike), novels.animate.set_opacity(0.55), run_time=0.45)

        wife = lab("his wife", TEXT, 30).move_to([-0.1, -1.2, 0])
        self.at("asked his wife")
        self.play(pop(wife), run_time=0.45)
        arrow = Arrow(wife.get_right() + RIGHT * 0.1, [1.75, -1.2, 0], color=TEXT, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.3)
        paper = lab("paper", YELLOW, 30).move_to([3.0, -1.2, 0])
        rule_chip = lab("slide rule", YELLOW, 30).move_to([5.15, -1.2, 0])
        self.at("bring him")
        self.play(GrowArrow(arrow), run_time=0.4)
        self.at("paper")
        self.play(pop(paper), run_time=0.4)
        self.at("slide rule")
        self.play(pop(rule_chip), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s02 the coil
class S02Coil(ProfileScene):
    N = 8
    CENTER = np.array([4.0, 0.15, 0.0])

    def wheel_pos(self, n):
        """Position/scale of residue n (1-based) seen end-on: 100 deg per residue = 3.6 per turn,
        clockwise, spiralling inward = the chain running away from the viewer (a right-handed coil)."""
        ang = math.radians(90 - 360 / 3.6 * (n - 1))
        r = 1.85 - 0.08 * (n - 1)
        return self.CENTER + np.array([r * math.cos(ang), r * math.sin(ang), 0.0]), 1.0 - 0.012 * (n - 1)

    def construct(self):
        self.add_inset()
        N = self.N
        row_y = 0.55
        xs = [-1.9 + 0.95 * i for i in range(N)]
        tiles = [tile(i + 1) for i in range(N)]
        for t, x in zip(tiles, xs):
            t.move_to([x, row_y, 0]).set_z_index(3)
        w = ValueTracker(3.0)
        links = VGroup(*[
            always_redraw(lambda a=tiles[i], b=tiles[i + 1]: Line(
                a.get_center(), b.get_center(), color=TEAL, stroke_width=w.get_value()).set_z_index(1))
            for i in range(N - 1)
        ])

        chain_lab = T("polypeptide chain", 32, TEAL).move_to([PANEL_C - 0.2, 1.65, 0])
        self.at("polypeptide chain")
        self.add(links)
        self.play(FadeIn(chain_lab, shift=UP * 0.1),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=1.3)

        # ruler: "at the right scale"
        ticks = VGroup(*[Line([-2.0 + 0.4 * k, -0.35, 0], [-2.0 + 0.4 * k, -0.35 + (0.22 if k % 5 == 0 else 0.12), 0],
                              color=GREY, stroke_width=2) for k in range(21)])
        base = Line([-2.0, -0.35, 0], [6.0, -0.35, 0], color=GREY, stroke_width=3)
        ruler = VGroup(base, ticks)
        scale_lab = T("drawn to scale", 26, GREY).move_to([PANEL_C - 0.2, -0.95, 0])
        self.at("right scale")
        self.play(Create(base), FadeIn(ticks), FadeIn(scale_lab), run_time=0.7)

        # flat peptide bonds
        flat = lab(["every peptide bond", "kept flat"], TEAL, 28).move_to([PANEL_C - 0.2, -1.2, 0])
        self.at("peptide bond flat")
        self.play(FadeOut(ruler), FadeOut(scale_lab), run_time=0.4)
        self.play(w.animate.set_value(10), pop(flat), run_time=0.7)
        self.play(LaggedStart(*[Flash((tiles[i].get_center() + tiles[i + 1].get_center()) / 2, color=TEXT,
                                      flash_radius=0.3, line_length=0.12) for i in range(N - 1)], lag_ratio=0.2),
                  run_time=1.0)

        # fold: the strip winds up into an end-on coil
        targets = []
        for i, t in enumerate(tiles):
            pos, sc = self.wheel_pos(i + 1)
            t2 = t.copy().scale(sc).move_to(pos)
            targets.append(Transform(t, t2, path_arc=-1.4))
        spiral = ParametricFunction(
            lambda s: self.CENTER + np.array([
                (1.85 - 0.08 * (s - 1)) * math.cos(math.radians(90 - 100 * (s - 1))),
                (1.85 - 0.08 * (s - 1)) * math.sin(math.radians(90 - 100 * (s - 1))), 0]),
            t_range=[1, N, 0.02], color=TEAL, stroke_width=4).set_z_index(1).set_fill(opacity=0).set_stroke(opacity=0.6)
        self.at("folded the strip")
        self.play(FadeOut(flat), FadeOut(chain_lab), run_time=0.4)
        self.play(LaggedStart(*targets, lag_ratio=0.12), w.animate.set_value(4), run_time=2.4)
        for l in links:
            l.clear_updaters()
        endon = T("seen end-on, down the coil", 24, GREY).move_to(self.CENTER + DOWN * 2.45)
        self.play(FadeOut(links), FadeIn(spiral), FadeIn(endon), run_time=0.5)

        # right-handed coil: a clockwise arrow in the middle
        coil = lab(["right-handed", "coil"], TEAL, 30).move_to([-0.8, 1.55, 0])
        turn_arrow = Arc(radius=0.7, start_angle=math.radians(90), angle=-math.radians(260), color=TEAL,
                         stroke_width=5).add_tip(tip_length=0.22).move_arc_center_to(self.CENTER)
        self.at("handed coil")
        self.play(pop(coil), Create(turn_arrow), run_time=0.8)

        # 3.6 residues per turn: ring + counter
        # 3.6 residues per turn: a hand sweeps one full turn (360 deg) from residue 1; the counter reads
        # residues advanced (angle / 100 deg), so one turn ends 60% of the way from residue 4 to residue 5
        per_turn = lab(["3.6 residues", "per turn"], TEAL, 30).move_to([-0.8, 0.0, 0])
        v = ValueTracker(0.0)          # degrees swept, clockwise from residue 1

        def sweep():
            a = v.get_value()
            arc = Arc(radius=0.92, start_angle=math.radians(90), angle=-math.radians(max(a, 0.01)),
                      arc_center=self.CENTER, color=TEXT, stroke_width=4)
            ang = math.radians(90 - a)
            u = np.array([math.cos(ang), math.sin(ang), 0.0])
            hand = Line(self.CENTER + u * 0.8, self.CENTER + u * 1.04, color=TEXT, stroke_width=5)
            return VGroup(arc, hand)

        dial = always_redraw(sweep)
        counter = always_redraw(lambda: M(f"{v.get_value() / 100:.1f}", 44, TEAL).move_to(self.CENTER))
        self.at("3 6 residues")
        self.play(FadeOut(turn_arrow), pop(per_turn), run_time=0.4)
        self.add(dial, counter)
        self.play(v.animate.set_value(360), run_time=1.6, rate_func=smooth)
        dial.clear_updaters()
        counter.clear_updaters()

        # NH hydrogen-bonded to CO four residues back
        hb = lab(["NH → CO,", "four residues back"], GREEN, 26).move_to([-0.7, -1.5, 0])
        self.at("backbone NH")
        self.play(pop(hb), FadeOut(dial), run_time=0.5)

        def edge(n, d=0.36):
            p, _ = self.wheel_pos(n)
            u = (p - self.CENTER) / np.linalg.norm(p - self.CENTER)
            return p + u * d

        def around(n, deg, r):
            ang = math.radians(90 - 100 * (n - 1) + deg)
            return self.CENTER + r * np.array([math.cos(ang), math.sin(ang), 0.0])

        nh = T("NH", 26, GREEN, weight=BOLD).move_to(around(5, -28, 2.2))
        co = T("CO", 26, GREEN, weight=BOLD).move_to(around(1, 22, 2.4))
        self.at("NH")
        self.play(FadeIn(nh, scale=1.4), Indicate(tiles[4], color=GREEN, scale_factor=1.12), run_time=0.6)
        # residue n+4 sits 40 deg clockwise of residue n; the arrow runs back to n, bulging outward
        dashes = [CurvedArrow(edge(n + 4), edge(n), angle=0.9, color=GREEN, stroke_width=5,
                              tip_length=0.18).set_z_index(2) for n in range(1, 5)]
        self.at("hydrogen bonded")
        self.play(Create(dashes[0]), run_time=0.6)
        self.at("CO4")
        self.play(FadeIn(co, scale=1.4), Indicate(tiles[0], color=GREEN), run_time=0.5)
        self.at("residues back")
        self.play(LaggedStart(*[Create(d) for d in dashes[1:]], lag_ratio=0.35), run_time=1.1)
        self.finish()


# ----------------------------------------------------------------------------- s03 5.4 vs 5.1
class S03Rise(ProfileScene):
    def construct(self):
        self.add_inset()
        x0, k = -2.0, 1.3          # x of 0 angstrom, units per angstrom
        y1, y2, h = 1.35, -0.85, 0.8
        ax_y = -2.1
        axis = VGroup(
            Line([x0, ax_y, 0], [x0 + 6.0 * k + 0.2, ax_y, 0], color=GREY, stroke_width=3),
            *[Line([x0 + k * v, ax_y, 0], [x0 + k * v, ax_y - 0.12, 0], color=GREY, stroke_width=3) for v in range(7)],
            *[T(str(v), 24, GREY).move_to([x0 + k * v, ax_y - 0.38, 0]) for v in range(7)],
        )
        zero = Line([x0, ax_y, 0], [x0, y1 + 0.75, 0], color=GREY, stroke_width=3)
        ax_title = T("rise per turn (Å)", 28, TEXT).move_to([x0 + 3.0 * k, ax_y - 0.95, 0])

        t1, t2 = ValueTracker(0.0), ValueTracker(0.0)
        bad = ValueTracker(0.0)

        def bar(tr, y, color, tint=None):
            def make():
                wd = max(0.001, k * tr.get_value())
                col = interpolate_color(ManimColor(color), ManimColor(RED), bad.get_value()) if tint else color
                return Rectangle(width=wd, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9) \
                    .move_to([x0 + wd / 2, y, 0])
            return always_redraw(make)

        def val(tr, y):
            def make():
                s = tr.get_value()
                m = M(f"{s:.1f} Å", 30, BG, weight=BOLD)
                m.move_to([x0 + k * s - m.width / 2 - 0.2, y, 0])
                m.set_opacity(1.0 if s > 1.5 else 0.0)
                return m
            return always_redraw(make)

        bar1, bar2 = bar(t1, y1, TEAL, tint=True), bar(t2, y2, YELLOW)
        v1, v2 = val(t1, y1), val(t2, y2)
        lab1 = T("Pauling's coil", 30, TEAL).move_to([x0, y1 + h / 2 + 0.38, 0], aligned_edge=LEFT)
        lab2 = T("keratin, measured", 30, YELLOW).move_to([x0, y2 + h / 2 + 0.38, 0], aligned_edge=LEFT)
        lab1.move_to([x0 + 0.15 + lab1.width / 2, y1 + h / 2 + 0.38, 0])
        lab2.move_to([x0 + 0.15 + lab2.width / 2, y2 + h / 2 + 0.38, 0])

        self.at("rise per turn")
        self.play(Create(zero), FadeIn(axis), FadeIn(ax_title), run_time=0.9)
        self.add(bar1, v1)
        self.at("5 4 angstroms")
        self.play(FadeIn(lab1, shift=RIGHT * 0.1), t1.animate.set_value(5.4), run_time=1.1, rate_func=smooth)
        self.add(bar2, v2)
        self.at("5 1")
        self.play(t2.animate.set_value(5.1), run_time=1.0, rate_func=smooth)
        self.at("keratin")
        self.play(FadeIn(lab2, shift=RIGHT * 0.1), run_time=0.5)

        # the gap between the two ends
        xa, xb = x0 + k * 5.4, x0 + k * 5.1
        gy = 0.2
        guides = VGroup(DashedLine([xa, y1 - h / 2, 0], [xa, y2 + h / 2, 0], color=RED, stroke_width=3, dash_length=0.1),
                        DashedLine([xb, y1 - h / 2, 0], [xb, y2 + h / 2, 0], color=RED, stroke_width=3, dash_length=0.1))
        band = Rectangle(width=xa - xb, height=(y1 - h / 2) - (y2 - h / 2), stroke_width=0, fill_color=RED,
                         fill_opacity=0.3).move_to([(xa + xb) / 2, (y1 - h / 2 + y2 - h / 2) / 2, 0])
        gap = DoubleArrow([xb, gy, 0], [xa, gy, 0], color=RED, stroke_width=5, buff=0, tip_length=0.12)
        gap_lab = T("discrepancy", 30, RED, weight=BOLD)
        gap_lab.move_to([xb - 0.25 - gap_lab.width / 2, gy, 0])
        self.at("and let")
        self.play(Create(guides), FadeIn(band), run_time=0.4)
        self.at("discrepancy")
        self.play(GrowFromCenter(gap), FadeIn(gap_lab, shift=LEFT * 0.1), run_time=0.6)
        self.at("stand")
        self.play(Indicate(gap_lab, color=RED, scale_factor=1.12), run_time=0.7)

        # what he did not do: bend the chemistry to fit
        cross = VGroup(Line([-0.3, -0.3, 0], [0.3, 0.3, 0]), Line([-0.3, 0.3, 0], [0.3, -0.3, 0])) \
            .set_color(RED).set_stroke(width=8).move_to([x0 + k * 5.1 + 0.75, y1, 0])
        self.at("bend the chemistry")
        self.play(t1.animate.set_value(5.1), bad.animate.set_value(1.0), FadeOut(gap), FadeOut(gap_lab),
                  FadeOut(guides), FadeOut(band), run_time=0.6)
        self.at("to fit")
        self.play(FadeIn(cross, scale=1.4), run_time=0.3)
        self.at("it", lead=-0.2)      # hold the rejected fit until the sentence ends, then restore
        self.play(FadeOut(cross), t1.animate.set_value(5.4), bad.animate.set_value(0.0),
                  Create(guides), FadeIn(band), GrowFromCenter(gap), FadeIn(gap_lab), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s04 the passport
class S04Passport(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.4
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d1, d2 = Dot([-1.2, ay, 0], radius=0.12, color=GOLD), Dot([3.6, ay, 0], radius=0.12, color=GOLD)
        l1 = T("March 1948", 30, GOLD, weight=BOLD)
        l1.move_to([-2.0 + l1.width / 2, ay + 0.5, 0])
        l2 = T("four years later", 30, GOLD, weight=BOLD).move_to([3.6, ay + 0.5, 0])
        self.add(axis, d1, l1)

        deduce = lab(["deduce a structure", "from the bonds alone"], TEAL, 26).move_to([-0.4, 0.9, 0])
        self.at("deduce a structure")
        self.play(pop(deduce), run_time=0.6)

        self.at("four years later")
        self.play(FadeIn(d2, scale=2), FadeIn(l2, shift=UP * 0.1), run_time=0.6)
        state = lab("State Department", PLACE, 28).move_to([3.6, 1.3, 0])
        self.at("State Department")
        self.play(pop(state), run_time=0.45)
        passport = lab("passport not renewed", RED, 28).move_to([3.6, -0.3, 0])
        link = Arrow(state.get_bottom(), passport.get_top(), color=RED, stroke_width=4, buff=0.08,
                     max_tip_length_to_length_ratio=0.35)
        self.at("refused to renew")
        self.play(GrowArrow(link), pop(passport), run_time=0.6)

        # London as a place (a lavender region); the DNA photographs wait inside it
        city = RoundedRectangle(corner_radius=0.2, width=7.2, height=1.25, stroke_color=PLACE, stroke_width=2.5,
                                fill_color=PLACE, fill_opacity=0.08).move_to([2.2, -2.15, 0])
        city_lab = T("London", 30, PLACE).move_to(city.get_left() + RIGHT * 0.95)
        london = VGroup(city, city_lab)
        blocked = DashedLine(passport.get_bottom() + DOWN * 0.05, [3.6, city.get_top()[1] + 0.05, 0],
                             color=RED, stroke_width=4, dash_length=0.12)
        bx = blocked.get_center()
        xmark = VGroup(Line([-0.22, -0.22, 0], [0.22, 0.22, 0]), Line([-0.22, 0.22, 0], [0.22, -0.22, 0])) \
            .set_color(RED).set_stroke(width=8).move_to(bx)
        self.at("keeping him out of London")
        self.play(FadeIn(london), Create(blocked), run_time=0.6)
        self.play(FadeIn(xmark, scale=1.5), run_time=0.3)

        dna = lab("DNA photographs", YELLOW, 28).move_to([3.9, city.get_center()[1], 0])
        self.at("DNA photographs")
        self.play(pop(dna), run_time=0.5)
        self.play(Indicate(dna, color=YELLOW, scale_factor=1.06), run_time=0.8)

        # clear the stage for the last sentence
        stage = VGroup(axis, d1, l1, d2, l2, deduce, state, passport, link, london, blocked, xmark, dna)
        first = lab(["read structure", "from first principles"], TEAL, 32).move_to([-0.1, 0.3, 0])
        gene = lab(["the structure", "of the gene"], RED, 32, fill=0.0).move_to([4.2, 0.3, 0])
        gene_box = DashedVMobject(gene[0], num_dashes=28)
        gene_box.set_color(RED)
        arrow = Arrow(first.get_right() + RIGHT * 0.1, gene.get_left() + LEFT * 0.1, color=GREY, stroke_width=4,
                      buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("The man who could read structure")
        self.play(FadeOut(stage), run_time=0.6)
        self.play(pop(first), run_time=0.6)
        missed = T("missed", 36, RED, weight=BOLD).next_to(gene, DOWN, buff=0.35)
        self.at("missed")
        self.play(GrowArrow(arrow), FadeIn(missed, shift=UP * 0.1), run_time=0.6)
        self.at("structure of the gene")
        self.play(Create(gene_box), FadeIn(gene[1]), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s05 the quote
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“I was so pleased with this", "structure that I stayed up until", "late in the night, pondering", "about it.”"]
        q = VGroup(*[T(l, 38, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        fit(q, max_w=8.4)
        who = T("— Linus Pauling", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.8)
        self.wait(0.5)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Predicted the alpha helix and beta sheet from first principles, years before confirmation."

    def construct(self):
        a = T("Predicted the alpha helix and beta sheet", size=42, font=TITLE_FONT)
        b = T("from first principles, years before confirmation.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
