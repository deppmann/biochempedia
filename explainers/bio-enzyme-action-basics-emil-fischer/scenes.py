"""Emil Fischer: a scientist profile (Biochemistrypedia, enzyme-action-basics lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time: Fischer's name/dates, timeline markers, "most of a century"
  TEAL   = Fischer's own words and his picture: "lock and key", the quoted phrases, the idea
  BLUE   = the enzyme (and the pure enzyme)
  YELLOW = the substrate / sugars / what the enzyme binds, and the tools that touch them
  GREEN  = the correction: the flexing, closing site, induced fit
  RED    = doubt and harm: distrust, walking it back, the warning, the poison
  GREY   = rigid / de-emphasized things (the "brass lock", the mixture, the lifeforce)
No molecular structure is drawn: enzymes and substrates are schematic puzzle-piece blocks.
"""
import math
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

CROP = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "fischer_crop.png"
CAPTION = "illustration · AI-generated"

INSET_C = np.array([-4.6, 1.3, 0.0])
INSET_H = 2.9
PANEL_C = 1.95          # x center of the right panel (x from -2.2 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(str(CROP)).set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T("Emil Fischer", size=34, font=TITLE_FONT)
    dt = T("1852–1919", size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.2, 0])
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


def xmark(center, color=RED, r=0.22, sw=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color).set_stroke(width=sw) \
        .move_to(center)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)
        self.inset = (img, frame, cap, tag)


# ---- schematic lock-and-key pieces (puzzle blocks; no molecular structure) --------------------
# enzyme block: right face at local x=0, notch carved into it; substrate: left face at local x=0, tab sticks out
E_PTS = [(-1.2, 1.3), (0, 1.3), (0, 0.35), (-0.30, 0.35), (-0.30, 0.0), (-0.55, 0.0), (-0.55, -0.35),
         (0, -0.35), (0, -1.3), (-1.2, -1.3)]
S_PTS = [(0, 0.6), (1.0, 0.6), (1.0, -0.6), (0, -0.6), (0, -0.35), (-0.55, -0.35), (-0.55, 0.0), (-0.30, 0.0),
         (-0.30, 0.35), (0, 0.35)]
S_LEFT = [(0, 0.6), (0.5, 0.6), (0.5, -0.6), (0, -0.6), (0, -0.35), (-0.55, -0.35), (-0.55, 0.0), (-0.30, 0.0),
          (-0.30, 0.35), (0, 0.35)]
S_RIGHT = [(0.5, 0.6), (1.0, 0.6), (1.0, -0.6), (0.5, -0.6)]


def poly(pts, origin, color, fill=0.22, sw=3.5, scale=1.0, flip=False):
    P = [np.array([origin[0] + x * scale, origin[1] + (-y if flip else y) * scale, 0.0]) for x, y in pts]
    return Polygon(*P, color=color, stroke_width=sw, fill_color=color, fill_opacity=fill)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = "Emil Fischer"

    def construct(self):
        img, frame = portrait_pair(4.5)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T("1852–1919", size=38, color=GOLD)
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


# ----------------------------------------------------------------------------- s01 1894: lock and key
class S01Lock(ProfileScene):
    def construct(self):
        self.add_inset()
        EX, EY = 1.9, -0.8
        # --- the most durable metaphor, escaped almost by accident
        meta = lab(["the most durable metaphor", "in enzymology"], TEAL, 32).move_to([PANEL_C, 0.7, 0])
        self.at("The most durable metaphor")
        self.play(pop(meta), run_time=0.7)
        self.play(meta.animate.scale(1.05), run_time=1.3, rate_func=linear)
        self.at("escaped")
        self.play(meta.animate.shift(RIGHT * 0.5), run_time=0.7)
        acc = T("almost by accident", 36, RED).next_to(meta, DOWN, buff=0.55)
        self.at("almost by accident")
        self.play(pop(acc), run_time=0.6)

        # --- 1894 timeline
        ay = 2.2
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([-0.5, ay, 0], radius=0.12, color=GOLD)
        date = T("1894", 40, GOLD, weight=BOLD).next_to(dot, UP, buff=0.2)
        lect = T("closing a lecture", 28, TEXT).next_to(dot, DOWN, buff=0.25)
        self.at("Closing an 1894")
        self.play(FadeOut(meta), FadeOut(acc), run_time=0.4)
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.6)
        self.play(pop(lect), run_time=0.4)
        image = lab("an image", TEAL, 30).move_to([3.4, 1.65, 0])
        self.at("reached for an image")
        self.play(pop(image), run_time=0.5)
        self.at("to explain")
        self.play(Indicate(image, color=TEAL, scale_factor=1.1), run_time=0.7)

        # --- the enzyme, the sugar torn apart, the near-twin ignored
        enz = poly(E_PTS, [EX, EY], BLUE)
        enz_lab = T("enzyme", 30, BLUE).move_to([EX - 0.3, EY + 1.3 + 0.4, 0])
        self.at("an enzyme")
        self.play(FadeIn(enz, shift=RIGHT * 0.3), FadeIn(enz_lab), run_time=0.7)

        s_origin = np.array([EX + 0.03, EY, 0.0])
        sugar = poly(S_PTS, s_origin + RIGHT * 3.4, YELLOW)
        sug_lab = T("one sugar", 28, YELLOW).move_to([EX + 0.5 + 3.4, EY - 1.65, 0])
        grp = VGroup(sugar, sug_lab)
        self.at("would tear")
        self.play(FadeIn(grp), run_time=0.3)
        self.play(grp.animate.shift(LEFT * 3.4), run_time=1.0, rate_func=smooth)
        left = poly(S_LEFT, s_origin, YELLOW)
        right = poly(S_RIGHT, s_origin, YELLOW)
        self.at("apart")
        self.remove(sugar)
        self.add(left, right)
        crack = Flash([EX + 0.5, EY, 0], color=TEXT, flash_radius=0.5, line_length=0.18)
        self.play(FadeOut(sug_lab), right.animate.shift(RIGHT * 0.8 + UP * 0.35).rotate(-0.25),
                  left.animate.shift(LEFT * 0.03), crack, run_time=0.8)

        twin = poly(S_PTS, [EX + 3.5, EY], YELLOW, flip=True)
        twin_lab = T("its near-twin", 28, YELLOW).move_to([EX + 4.0, EY - 1.65, 0])
        tg = VGroup(twin, twin_lab)
        self.at("ignore")
        self.play(FadeOut(left), FadeOut(right), FadeIn(tg), run_time=0.25)
        self.play(tg.animate.shift(LEFT * 3.25), run_time=0.65, rate_func=smooth)     # nub meets the notch wall
        self.at("near twin")
        bump = Flash([EX + 0.0, EY + 0.18, 0], color=RED, flash_radius=0.7, line_length=0.3, num_lines=10)
        hit = xmark([EX - 0.05, EY + 0.55, 0], RED, r=0.2, sw=7)
        self.play(FadeIn(hit, scale=1.6), bump, run_time=0.25)
        self.play(tg.animate.shift(RIGHT * 0.9), FadeOut(hit), run_time=0.45)
        ign = T("ignored", 32, RED).move_to([EX + 2.95, EY - 2.25, 0])
        self.play(pop(ign), run_time=0.3)

        # --- enzyme and substrate must fit
        sub = poly(S_PTS, s_origin + RIGHT * 2.2, YELLOW)
        sub_lab = T("substrate", 28, YELLOW).move_to([EX + 0.5 + 2.2, EY - 1.65, 0])
        sg = VGroup(sub, sub_lab)
        self.at("Enzyme and substrate")
        self.play(FadeOut(tg), FadeOut(ign), FadeIn(sg), run_time=0.3)
        self.play(sg.animate.shift(LEFT * 2.2), run_time=0.9, rate_func=smooth)
        quote = lab("“like lock and key”", TEAL, 32).move_to([3.4, 1.65, 0])
        self.at("like lock and key")
        self.play(ReplacementTransform(image, quote), run_time=0.6)
        self.play(Indicate(enz, color=TEXT, scale_factor=1.04), Indicate(sub, color=TEXT, scale_factor=1.04),
                  run_time=0.7)

        # --- he distrusted it
        dis = lab("distrusted it", RED, 32).move_to([4.75, -0.8, 0])
        self.at("He distrusted")
        self.play(pop(dis), run_time=0.5)
        self.play(Wiggle(quote, scale_value=1.08, rotation_angle=0.03 * TAU), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s02 1898: walking it back
class S02Walkback(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.2
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d94, d98 = Dot([-0.5, ay, 0], radius=0.12, color=GOLD), Dot([3.7, ay, 0], radius=0.12, color=GOLD)
        l94 = T("1894", 34, GOLD, weight=BOLD).next_to(d94, UP, buff=0.2)
        l98 = T("1898", 40, GOLD, weight=BOLD).next_to(d98, UP, buff=0.2)
        lk = lab("“lock and key”", TEAL, 28).next_to(d94, DOWN, buff=0.3)
        self.add(axis, d94, l94, lk)
        self.at("By 1898")
        self.play(FadeIn(d98, scale=2), FadeIn(l98, shift=UP * 0.1), run_time=0.6)

        back = Arrow([3.6, 1.45, 0], [1.4, 1.45, 0], color=RED, stroke_width=5, buff=0,
                     max_tip_length_to_length_ratio=0.2)
        back_lab = T("walking it back", 30, RED).move_to([2.7, 0.95, 0])
        self.at("walking it back")
        self.play(GrowArrow(back), pop(back_lab), lk.animate.set_opacity(0.55), run_time=0.8)

        # the specificity lay in the enzyme molecule's asymmetric structure
        spec = T("the specificity", 32, TEXT).move_to([3.7, 1.0, 0])
        self.at("the specificity")
        self.play(FadeOut(back), FadeOut(back_lab), pop(spec), run_time=0.6)
        quote = lab(["“the asymmetric structure", "of the enzyme molecule”"], TEAL, 28).move_to([3.7, -0.55, 0])
        arrow_q = Arrow(spec.get_bottom() + DOWN * 0.08, quote.get_top() + UP * 0.05, color=GREY, stroke_width=4,
                        buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("lay in")
        self.play(GrowArrow(arrow_q), run_time=0.5)
        self.at("the asymmetric structure")
        self.play(pop(quote), run_time=0.7)
        enz = poly(E_PTS, [0.55, -0.55], BLUE, scale=0.8)
        enz_lab = T("enzyme molecule", 26, BLUE).move_to([0.05, -1.95, 0])
        link = Arrow(quote.get_left() + LEFT * 0.05, [0.72, -0.5, 0], color=GREY, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.3)
        self.at("of the enzyme molecule")
        self.play(FadeIn(enz, shift=RIGHT * 0.2), FadeIn(enz_lab), GrowArrow(link), run_time=0.7)
        self.play(Indicate(enz, color=TEXT, scale_factor=1.06), run_time=0.7)

        # ...and that the lock-and-key picture was only a picture
        pic = lab("“lock and key”", TEAL, 28).move_to([3.7, -2.0, 0])
        self.at("used the picture")
        self.play(FadeOut(spec), FadeOut(arrow_q), pop(pic), run_time=0.5)
        clear = T("only to make the thought clearer", 26, GREY).move_to([3.6, -2.85, 0])
        self.at("only to make the thought clearer")
        self.play(pop(clear), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s03 the warning
class S03Warning(ProfileScene):
    def construct(self):
        self.add_inset()
        warn = lab("the warning", RED, 32).move_to([PANEL_C + 0.2, 2.55, 0])
        self.at("Then the warning")
        self.play(pop(warn), run_time=0.5)
        check = VGroup(Line([-0.22, 0.0, 0], [-0.05, -0.2, 0]), Line([-0.05, -0.2, 0], [0.28, 0.28, 0])) \
            .set_color(GREEN).set_stroke(width=9).next_to(warn, RIGHT, buff=0.35)
        self.at("proves him right")
        self.play(Create(check), run_time=0.5)

        idea = lab("the idea", TEAL, 30).move_to([-0.3, 1.25, 0])
        self.at("the idea")
        self.play(pop(idea), run_time=0.5)
        tested = lab("thoroughly tested", GREEN, 30, fill=0.0).move_to([3.8, 1.25, 0])
        t_box = DashedVMobject(tested[0], num_dashes=30).set_color(GREY)
        link = Arrow(idea.get_right() + RIGHT * 0.1, tested.get_left() + LEFT * 0.1, color=GREY, stroke_width=4,
                     buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("can only be thoroughly tested")
        self.play(GrowArrow(link), Create(t_box), FadeIn(tested[1]), run_time=0.8)
        when = T("only when…", 28, TEXT).move_to([1.7, 0.55, 0])
        self.at("when we are able")
        self.play(pop(when), run_time=0.5)

        # isolate the enzymes in a pure state: a mixture -> a pure vial
        flask = RoundedRectangle(corner_radius=0.2, width=2.2, height=1.5, stroke_color=GREY, stroke_width=3,
                                 fill_opacity=0).move_to([-0.5, -1.35, 0])
        rng = np.random.default_rng(7)
        pts = [[-1.35 + 0.5 * i + rng.uniform(-0.1, 0.1), -1.35 + 0.42 * j + rng.uniform(-0.1, 0.1)]
               for j in (-1, 0, 1) for i in range(4)]
        blue_idx = {0, 3, 6, 9}
        dots = VGroup(*[Dot([p[0] + 0.2, p[1], 0], radius=0.1, color=BLUE if k in blue_idx else GREY)
                        for k, p in enumerate(pts)])
        for d in dots:
            d.set_opacity(0.9)
        enz_lab = T("enzymes", 28, BLUE).next_to(flask, UP, buff=0.2)
        self.at("isolate the enzymes")
        self.play(Create(flask), LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.08), run_time=1.2)
        self.play(pop(enz_lab), run_time=0.4)

        vial = RoundedRectangle(corner_radius=0.2, width=1.1, height=1.8, stroke_color=BLUE, stroke_width=3,
                                fill_opacity=0).move_to([3.0, -1.35, 0])
        pure_lab = T("pure state", 28, BLUE).next_to(vial, DOWN, buff=0.25)
        arr = Arrow([0.8, -1.35, 0], [2.2, -1.35, 0], color=GREY, stroke_width=4, buff=0,
                    max_tip_length_to_length_ratio=0.25)
        blues = [d for k, d in enumerate(dots) if k in blue_idx]
        targets = [[2.75, -1.0], [3.25, -1.0], [2.75, -1.55], [3.25, -1.55]]
        self.at("pure state")
        self.play(GrowArrow(arr), Create(vial), pop(pure_lab),
                  *[d.animate.move_to([t[0], t[1], 0]) for d, t in zip(blues, targets)],
                  *[d.animate.set_opacity(0.3) for k, d in enumerate(dots) if k not in blue_idx],
                  run_time=1.3)

        # investigate their configuration: a lens over the enzyme's shape
        shape = poly(E_PTS, [5.3, -1.35], BLUE, scale=0.7)
        lens_c = np.array([4.95, -1.35, 0.0])
        lens = VGroup(Circle(radius=0.72, color=TEXT, stroke_width=5).move_to(lens_c),
                      Line(lens_c + np.array([0.51, -0.51, 0]), lens_c + np.array([0.95, -0.95, 0]), color=TEXT,
                           stroke_width=8))
        conf = T("configuration", 28, TEAL).move_to([5.0, -0.1, 0])
        self.at("investigate")
        self.play(FadeIn(shape, shift=LEFT * 0.2), Create(lens), run_time=0.7)
        self.at("configuration")
        self.play(pop(conf), run_time=0.5)

        # it took most of a century
        everything = VGroup(warn, check, idea, tested, t_box, link, when, flask, dots, enz_lab, vial, pure_lab, arr, shape,
                            lens, conf)
        self.at("It took most of a century")
        self.play(FadeOut(everything), run_time=0.5)
        bar = Arrow([-1.4, 0.4, 0], [5.8, 0.4, 0], color=GOLD, stroke_width=10, buff=0,
                    max_tip_length_to_length_ratio=0.05)
        ticks = VGroup(*[Line([-1.0 + 0.5 * k, 0.4, 0], [-1.0 + 0.5 * k, 0.4 - (0.32 if k % 5 == 0 else 0.18), 0],
                              color=GOLD, stroke_width=4) for k in range(14)])
        span = T("most of a century", 46, GOLD, font=TITLE_FONT).move_to([2.2, 1.35, 0])
        self.play(pop(span), GrowArrow(bar), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.1), run_time=1.6)
        self.finish()


# ----------------------------------------------------------------------------- s04 the lock flexes
class S04Flex(ProfileScene):
    BX, BY = -0.2, -0.75
    JAW_W = 1.75

    def make_enzyme(self, color):
        px = self.BX + 0.45 - 0.05
        base = RoundedRectangle(corner_radius=0.12, width=0.9, height=2.7, stroke_color=color, stroke_width=3.5,
                                fill_color=color, fill_opacity=0.22).move_to([self.BX, self.BY, 0])
        top = Rectangle(width=self.JAW_W, height=0.45, stroke_color=color, stroke_width=3.5, fill_color=color,
                        fill_opacity=0.22).move_to([px + self.JAW_W / 2, self.BY + 0.62, 0])
        bot = Rectangle(width=self.JAW_W, height=0.45, stroke_color=color, stroke_width=3.5, fill_color=color,
                        fill_opacity=0.22).move_to([px + self.JAW_W / 2, self.BY - 0.62, 0])
        return base, top, bot, np.array([px, self.BY + 0.62, 0.0]), np.array([px, self.BY - 0.62, 0.0])

    def construct(self):
        self.add_inset()
        cryst = lab("crystallographers", TEXT, 30, fill=0.08).move_to([PANEL_C, 2.55, 0])
        self.at("crystallographers")
        self.play(pop(cryst), run_time=0.6)

        base, top, bot, pt, pb = self.make_enzyme(BLUE)
        rest = math.radians(12)
        top.rotate(rest, about_point=pt)
        bot.rotate(-rest, about_point=pb)
        enz = VGroup(base, top, bot)
        enz_lab = T("pure enzyme", 30, BLUE).move_to([self.BX + 0.9, 1.45, 0])
        self.at("a pure enzyme")
        self.play(FadeIn(enz, shift=RIGHT * 0.2), FadeIn(enz_lab), run_time=0.7)

        lens_c = np.array([2.7, 0.55, 0.0])
        lens = VGroup(Circle(radius=0.62, color=TEXT, stroke_width=5).move_to(lens_c),
                      Line(lens_c + np.array([0.44, -0.44, 0]), lens_c + np.array([0.9, -0.9, 0]), color=TEXT,
                           stroke_width=8))
        self.at("and looked")
        self.play(Create(lens), run_time=0.6)
        self.play(lens.animate.shift(LEFT * 1.8 + DOWN * 0.1), run_time=0.6)

        # the brass lock: rigid, grey
        lock_lab = T("the brass lock", 30, GREY).move_to([3.7, 1.0, 0])
        self.at("the brass lock")
        self.play(FadeOut(lens), FadeOut(enz_lab), enz.animate.set_color(GREY), pop(lock_lab), run_time=0.6)

        # ...turned out to flex
        flex_lab = T("flexes", 32, GREEN).move_to([3.7, 1.0, 0])
        self.at("turned out to flex")
        self.play(FadeOut(lock_lab), FadeIn(flex_lab), enz.animate.set_color(BLUE), run_time=0.3)
        wob = math.radians(18)
        self.play(Rotate(top, wob, about_point=pt), Rotate(bot, -wob, about_point=pb), run_time=0.4)
        self.play(Rotate(top, -wob, about_point=pt), Rotate(bot, wob, about_point=pb), run_time=0.4)

        # closing around its substrate
        px = self.BX + 0.4
        sub = RoundedRectangle(corner_radius=0.1, width=0.9, height=0.6, stroke_color=YELLOW, stroke_width=3.5,
                               fill_color=YELLOW, fill_opacity=0.25).move_to([px + 0.8 + 3.2, self.BY, 0])
        sub_lab = T("substrate", 30, YELLOW).move_to([4.2, self.BY, 0])
        sub_arrow = Arrow([2.8, self.BY, 0], [1.7, self.BY, 0], color=YELLOW, stroke_width=4, buff=0,
                          max_tip_length_to_length_ratio=0.3)
        self.at("closing around")
        self.play(FadeOut(flex_lab), FadeIn(sub), run_time=0.15)
        self.play(sub.animate.shift(LEFT * 3.2), Rotate(top, -rest, about_point=pt), Rotate(bot, rest, about_point=pb),
                  run_time=0.65, rate_func=smooth)
        self.at("its substrate")
        self.play(pop(sub_lab), GrowArrow(sub_arrow), enz.animate.set_color(GREEN), run_time=0.35)
        self.play(enz.animate.set_color(BLUE), run_time=0.2)

        # gripping the fleeting transition state tighter still
        ts_lab = VGroup(T("fleeting", 30, YELLOW), T("transition state", 30, YELLOW)).arrange(DOWN, buff=0.1).move_to([4.3, self.BY, 0])
        sub_ts = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=0.9, height=0.6, stroke_color=YELLOW,
                                                 stroke_width=4).move_to(sub.get_center()), num_dashes=22)
        self.at("gripping the fleeting")
        self.play(FadeOut(sub_lab), FadeOut(sub), FadeIn(sub_ts), FadeIn(ts_lab, shift=UP * 0.1), run_time=0.45)
        self.play(sub_ts.animate.set_opacity(0.25), run_time=0.2)
        self.play(sub_ts.animate.set_opacity(1.0), run_time=0.2)
        self.at("tighter still")
        self.play(top.animate.shift(DOWN * 0.1).set_color(GREEN), bot.animate.shift(UP * 0.1).set_color(GREEN),
                  base.animate.set_color(GREEN), Indicate(sub_ts, color=YELLOW, scale_factor=1.15), run_time=0.7)

        # that correction is what Koshland named induced fit
        corr = lab("the correction", GREEN, 30).move_to([4.2, 0.3, 0])
        self.at("That correction")
        self.play(FadeOut(ts_lab), FadeOut(sub_arrow), pop(corr), run_time=0.5)
        kosh = T("Koshland", 34, TEXT, font=TITLE_FONT).move_to([4.2, 0.3, 0])
        self.at("Koshland")
        self.play(FadeOut(corr), FadeIn(kosh, shift=UP * 0.1), run_time=0.5)
        fit_lab = lab("induced fit", GREEN, 40, fill=0.2).move_to([4.2, -0.9, 0])
        self.at("Induced Fit")
        self.play(pop(fit_lab), Indicate(enz, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s05 life, sugars, 1919
class S05Life(ProfileScene):
    def construct(self):
        self.add_inset()
        # --- structure read off behavior
        idea = lab("the lock-and-key idea", TEAL, 30).move_to([PANEL_C + 0.3, 2.35, 0])
        self.at("reached the lock")
        self.play(pop(idea), run_time=0.6)
        structure = lab("structure", TEAL, 34).move_to([3.7, 0.5, 0])
        behavior = lab("behavior", YELLOW, 34).move_to([-0.2, 0.5, 0])
        arrow = Arrow(behavior.get_right() + RIGHT * 0.1, structure.get_left() + LEFT * 0.1, color=TEXT,
                      stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.25)
        read = T("read off", 26, GREY).next_to(arrow, UP, buff=0.12)
        self.at("read structure")
        self.play(pop(structure), run_time=0.5)
        self.at("off behavior")
        self.play(pop(behavior), GrowArrow(arrow), pop(read), run_time=0.7)
        else_ = T("everywhere else", 32, GREY).move_to([PANEL_C, -0.7, 0])
        self.at("everywhere else")
        self.play(pop(else_), run_time=0.6)

        # --- sugars built from glycerol
        stage = VGroup(idea, structure, behavior, arrow, read, else_)
        sugars = lab("sugars", YELLOW, 34).move_to([4.2, 1.5, 0])
        glyc = lab("glycerol", YELLOW, 34).move_to([-0.1, 1.5, 0])
        built = Arrow(glyc.get_right() + RIGHT * 0.1, sugars.get_left() + LEFT * 0.1, color=TEXT, stroke_width=5,
                      buff=0, max_tip_length_to_length_ratio=0.25)
        built_lab = T("built", 28, TEXT).next_to(built, UP, buff=0.12)
        self.at("He built sugars")
        self.play(FadeOut(stage), run_time=0.4)
        self.play(pop(sugars), run_time=0.5)
        self.at("glycerol")
        self.play(pop(glyc), GrowArrow(built), pop(built_lab), run_time=0.7)

        # life held no chemistry beyond the ordinary
        region = RoundedRectangle(corner_radius=0.25, width=6.2, height=2.2, stroke_color=TEAL, stroke_width=3,
                                  fill_color=TEAL, fill_opacity=0.07).move_to([1.4, -1.5, 0])
        life = lab("life", GREEN, 36).move_to([-0.3, -1.65, 0])
        ord_lab = T("ordinary chemistry", 28, TEAL).move_to([region.get_left()[0] + 1.85, -0.78, 0])
        self.at("prove life")
        self.play(pop(life), run_time=0.5)
        self.at("held no chemistry")
        self.play(Create(region), pop(ord_lab), run_time=0.8)
        out = Arrow(life.get_right() + RIGHT * 0.1, [5.9, -1.65, 0], color=RED, stroke_width=5, buff=0,
                    max_tip_length_to_length_ratio=0.2)
        bx = xmark([4.5, -1.65, 0])
        self.at("beyond the ordinary")
        self.play(GrowArrow(out), run_time=0.5)
        self.play(FadeIn(bx, scale=1.5), run_time=0.3)

        # science stripped the lifeforce of its last hiding-place
        stage2 = VGroup(sugars, glyc, built, built_lab, region, life, ord_lab, out, bx)
        science = lab("science", TEAL, 34).move_to([-0.5, 1.2, 0])
        force = lab("“lifeforce”", GREY, 34, fill=0.0).move_to([4.5, 1.2, 0])
        force_box = DashedVMobject(force[0], num_dashes=28).set_color(GREY)
        strip = Arrow(science.get_right() + RIGHT * 0.1, force.get_left() + LEFT * 0.55, color=TEXT, stroke_width=5,
                      buff=0, max_tip_length_to_length_ratio=0.25)
        strip_lab = T("stripped", 28, TEXT).next_to(strip, UP, buff=0.15)
        self.at("declaring that science")
        self.play(FadeOut(stage2), run_time=0.4)
        self.play(pop(science), run_time=0.5)
        self.at("stripped")
        self.play(GrowArrow(strip), pop(strip_lab), run_time=0.5)
        self.at("life force")
        self.play(Create(force_box), FadeIn(force[1]), run_time=0.7)
        hide = RoundedRectangle(corner_radius=0.2, width=force.width + 0.7, height=force.height + 0.7,
                                stroke_color=TEAL, stroke_width=4).move_to(force)
        hide_lab = T("“this last hiding-place”", 30, TEAL).move_to([PANEL_C + 0.2, -0.45, 0])
        self.at("this last hiding place")
        self.play(Create(hide), pop(hide_lab), run_time=0.7)
        gone = VGroup(force_box, force[1])
        self.at("place")
        self.play(FadeOut(gone, shift=DOWN * 0.3), FadeOut(hide), run_time=0.7)

        # --- the phenylhydrazine that fingerprinted those sugars also poisoned him
        stage3 = VGroup(science, strip, strip_lab, hide_lab)
        phz = lab("phenylhydrazine", YELLOW, 32).move_to([-0.3, 2.2, 0])
        sug = lab("sugars", YELLOW, 32).move_to([5.2, 2.2, 0])
        fing = Arrow(phz.get_right() + RIGHT * 0.1, sug.get_left() + LEFT * 0.1, color=TEXT, stroke_width=5, buff=0,
                     max_tip_length_to_length_ratio=0.25)
        fing_lab = T("fingerprinted", 28, TEXT).next_to(fing, UP, buff=0.18)
        self.at("The phenylhydrazine")
        self.play(FadeOut(stage3), run_time=0.4)
        self.play(pop(phz), run_time=0.5)
        self.at("fingerprinted")
        self.play(GrowArrow(fing), pop(fing_lab), pop(sug), run_time=0.7)
        pois_arrow = Arrow(phz.get_bottom() + DOWN * 0.05, [-0.3, 0.55, 0], color=RED, stroke_width=5, buff=0,
                           max_tip_length_to_length_ratio=0.25)
        pois = lab("poisoned him, slowly", RED, 32).move_to([-0.3, 0.0, 0])
        self.at("also slowly")
        self.play(phz.animate.set_color(RED), GrowArrow(pois_arrow), run_time=1.0)
        self.at("poisoned him")
        self.play(pop(pois), run_time=0.5)

        # --- 1919
        ay = -1.35
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([4.6, ay, 0], radius=0.13, color=GOLD)
        date = T("1919", 42, GOLD, weight=BOLD).next_to(dot, UP, buff=0.22)
        self.at("In 1919")
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.8)
        cancer = lab("inoperable cancer", RED, 32).move_to([2.7, -2.55, 0])
        self.at("inoperable cancer")
        self.play(pop(cancer), run_time=0.6)
        img, frame, cap, tag = self.inset
        self.at("took his own life")
        self.play(img.animate.set_opacity(0.55), run_time=1.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“Enzyme and glucoside must fit", "together like a lock and key.”"]
        q = VGroup(*[T(l, 40, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(q, max_w=8.4)
        who = T("— Emil Fischer", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.6).move_to([PANEL_C, 1.0, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        sc = 0.6
        enz = poly(E_PTS, [PANEL_C - 0.5, -1.7], BLUE, scale=sc)
        sub = poly(S_PTS, [PANEL_C - 0.5 + 0.02 + 1.6, -1.7], YELLOW, scale=sc)
        for k, ln in enumerate(q):
            self.play(ln.animate.set_opacity(1.0), run_time=1.0)
            if k == 0:
                self.play(FadeIn(enz), FadeIn(sub), run_time=0.4)
        self.play(sub.animate.shift(LEFT * 1.6), run_time=1.0, rate_func=smooth)
        self.play(Indicate(enz, color=TEXT, scale_factor=1.05), Indicate(sub, color=TEXT, scale_factor=1.05),
                  who.animate.set_opacity(1.0), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Coined the “lock and key” picture of enzyme specificity in 1894."

    def construct(self):
        a = T("Coined the “lock and key” picture", size=42, font=TITLE_FONT)
        b = T("of enzyme specificity in 1894.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
