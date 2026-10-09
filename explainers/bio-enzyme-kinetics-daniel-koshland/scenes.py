"""Daniel Koshland: a scientist profile (Biochemistrypedia, enzyme-kinetics lesson).

Narration is the lesson entry's `story`, verbatim (this entry's story: the water argument for induced fit).
Everything on screen comes from that entry (name, dates, contribution, story, quote). The portrait is an
AI-generated engraving-style illustration from The Molecule Hunters; it is captioned
"illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Koshland and his idea: name/dates, "induced fit", the portrait frame, "proved him right"
  BLUE   = the enzyme and its active site (a schematic block with two movable jaws, no structure)
  GREEN  = the real substrate (the "hand")
  WATER  = water (small dots; orange so it never reads as the blue enzyme)
  RED    = what stood in the way / went wrong: "chaos", "blocked", the dogma, the reviewer's verdict
  YELLOW = dates and tools: 1950s, 1958, X-ray crystallography
  PLACE (lavender) = journals, PNAS
  GREY   = textbook frame, static (rigid) things, labels
No molecular structure is drawn: the enzyme is two jaws on a base, the substrate a plain block, water small dots.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

PORTRAIT = "/Users/deppmann/mission-control/work/explainers/2026-10-09-biochempedia/bio-enzyme-kinetics-daniel-koshland/portrait.png"
CAPTION = "illustration · AI-generated"
NAME = "Daniel Koshland"
DATES = "1920–2007"
PLACE = "#B39DDB"
WATER = "#F4A261"
K = 1.2                                       # schematic scale for the main enzyme

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95

JAW_W, JAW_H, BASE_H = 0.9, 1.5, 0.6
OPEN_GAP, LOCK_GAP, SUB = 1.5, 0.9, 0.9      # open cleft, rigid lock-and-key cleft, substrate block size


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


# ----------------------------------------------------------------------------- the schematic enzyme
class Enz:
    """An enzyme as a schematic: a base and two movable jaws around a cleft (the 'active site').
    Nothing here is a molecular structure; it is a diagram of a site that is rigid or can close."""

    def __init__(self, gap=OPEN_GAP, color=BLUE, cx=PANEL_C, cy=-1.4, scale=K, opacity=0.28):
        self.color = color
        W = gap + 2 * JAW_W
        mk = lambda w, h: RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color,
                                           stroke_width=3.5, fill_color=color, fill_opacity=opacity)
        self.base = mk(W, BASE_H)
        self.jl = mk(JAW_W, JAW_H)
        self.jr = mk(JAW_W, JAW_H)
        self.base.move_to([0, 0, 0])
        jy = BASE_H / 2 + JAW_H / 2 - 0.05
        self.jl.move_to([-(gap / 2 + JAW_W / 2), jy, 0])
        self.jr.move_to([(gap / 2 + JAW_W / 2), jy, 0])
        self.grp = VGroup(self.base, self.jl, self.jr)
        self.grp.scale(scale)
        self.grp.shift(np.array([cx, cy, 0]) - self.base.get_center())

    @property
    def k(self):
        return self.jl.width / JAW_W

    def cleft_c(self):
        """Centre of the cleft floor (where a block of height SUB rests)."""
        k = self.k
        return np.array([self.base.get_center()[0], self.base.get_top()[1] + 0.0, 0.0])

    def cleft_x(self):
        return self.base.get_center()[0]

    def floor_y(self):
        return self.base.get_top()[1] - 0.05 * self.k

    def clamp(self, d=0.3):
        k = self.k
        return [self.jl.animate.shift(RIGHT * d * k), self.jr.animate.shift(LEFT * d * k)]

    def unclamp(self, d=0.3):
        k = self.k
        return [self.jl.animate.shift(LEFT * d * k), self.jr.animate.shift(RIGHT * d * k)]


def substrate(color=GREEN, size=SUB, k=K):
    s = size * k
    return RoundedRectangle(corner_radius=0.1 * k, width=s, height=s, stroke_color=color, stroke_width=3.5 * max(k, 0.6),
                            fill_color=color, fill_opacity=0.45)


def water_dot(x, y, r=0.13):
    return Circle(radius=r, stroke_color=WATER, stroke_width=2.5, fill_color=WATER, fill_opacity=0.8).move_to([x, y, 0])


def checkmark(color=GOLD, size=0.5):
    pts = [[-0.5, 0.0, 0], [-0.15, -0.4, 0], [0.55, 0.5, 0]]
    m = VMobject(stroke_color=color, stroke_width=8).set_points_as_corners(pts)
    return m.scale(size / 0.5 * 0.6)


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


# ----------------------------------------------------------------------------- s01 the lock-and-key picture
class S01Lock(ProfileScene):
    def construct(self):
        self.add_inset()
        yr = M("1950s", 44, YELLOW).move_to([PANEL_C - 2.6, 3.05, 0])
        ul = Line(yr.get_corner(DL) + DOWN * 0.1, yr.get_corner(DR) + DOWN * 0.1, color=YELLOW, stroke_width=3)
        self.at("1950s")
        self.play(Write(yr), Create(ul), run_time=0.6)

        # the rigid lock-and-key schematic: a cleft cut to exactly fit its key
        lock = Enz(gap=LOCK_GAP, cx=PANEL_C, cy=-1.45)
        key = substrate(GREEN)
        key.move_to([PANEL_C, 1.4, 0])
        tag = T("lock-and-key", 32, GREY, font=TITLE_FONT).move_to([PANEL_C + 2.15, 0.9, 0])
        self.at("lock and key")
        self.play(FadeIn(lock.grp, shift=UP * 0.1), FadeIn(key, shift=DOWN * 0.1), pop(tag), run_time=0.7)
        self.at("picture", lead=0.1)
        rest_y = lock.floor_y() + SUB * K / 2
        self.play(key.animate.move_to([PANEL_C, rest_y, 0]), run_time=0.8)

        frame = Rectangle(width=7.8, height=4.5, stroke_color=GREY, stroke_width=3).move_to([PANEL_C, 0.2, 0])
        fl = T("every textbook", 28, GREY).move_to([PANEL_C - 2.5, 1.85, 0])
        self.at("every textbook")
        self.play(Create(frame), FadeIn(fl, shift=DOWN * 0.1), run_time=0.8)

        self.at("Daniel Koshland")
        self.play(Indicate(self.portrait_frame, color=GOLD, scale_factor=1.04), run_time=0.9)
        self.at("incomplete")
        inc = T("incomplete", 42, RED, font=TITLE_FONT).move_to([PANEL_C - 2.0, -2.75, 0])
        self.play(FadeIn(inc, shift=UP * 0.1), frame.animate.set_stroke(RED, 3),
                  VGroup(lock.grp, key, tag, fl).animate.set_opacity(0.55), run_time=0.7)
        self.at("because of water", lead=0.1)
        w = chip("water", WATER, 32).move_to([PANEL_C + 2.3, -2.75, 0])
        dots = VGroup(*[water_dot(PANEL_C + 3.75 + 0.3 * i, -2.75 + (0.12 if i % 2 else -0.1)) for i in range(3)])
        self.play(pop(w), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.25), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s02 water
class S02Water(ProfileScene):
    def construct(self):
        self.add_inset()
        en = Enz(gap=OPEN_GAP, cx=PANEL_C, cy=-1.55)
        f = en.floor_y()
        self.at("active site")
        site = T("active site", 30, BLUE).move_to([PANEL_C, f + 2.5, 0])
        ptr = Arrow(site.get_bottom() + DOWN * 0.08, [PANEL_C, f + 0.75, 0], buff=0, color=BLUE, stroke_width=4,
                    max_tip_length_to_length_ratio=0.25)
        self.play(FadeIn(en.grp, shift=UP * 0.1), pop(site), GrowArrow(ptr), run_time=0.8)
        self.at("permanently open")
        po = T("permanently open", 32, BLUE).move_to([PANEL_C, -2.85, 0])
        self.play(pop(po), run_time=0.5)
        self.at("and waiting", lead=0.1)
        po2 = T("permanently open and waiting", 32, BLUE).move_to([PANEL_C, -2.85, 0])
        self.play(ReplacementTransform(po, po2), run_time=0.4)

        # water molecules, then the comparison with a substrate
        self.play(FadeOut(VGroup(site, ptr)), run_time=0.25)
        self.at("water molecules")
        xs = [PANEL_C - 1.5 + 0.55 * i for i in range(6)]
        wd = VGroup(*[water_dot(x, 2.0) for x in xs])
        wl = T("water molecules", 30, WATER).move_to([PANEL_C - 0.6, 2.95, 0])
        self.play(pop(wl), LaggedStart(*[FadeIn(d, scale=0.5) for d in wd], lag_ratio=0.12), run_time=0.9)
        self.at("smaller than")
        sub = substrate(GREEN).move_to([PANEL_C + 3.55, 1.95, 0])
        subl = T("substrate", 28, GREEN).next_to(sub, DOWN, buff=0.18)
        lt = T("<", 44, WATER, weight=BOLD).move_to([PANEL_C + 2.2, 2.0, 0])
        self.play(pop(sub), pop(subl), FadeIn(lt), run_time=0.7)

        self.at("slip in")
        # water slips into the open cleft
        targets = [(-0.45, f + 0.5), (0.0, f + 0.85), (0.45, f + 0.5)]
        slips = [d.animate.move_to([PANEL_C + dx, dy, 0]) for d, (dx, dy) in zip(list(wd)[1:4], targets)]
        self.play(AnimationGroup(*slips, lag_ratio=0.2), FadeOut(VGroup(lt, sub, subl, wl)), run_time=0.7)
        self.at("constantly")
        more = [d.animate.move_to([PANEL_C + dx, dy, 0])
                for d, (dx, dy) in zip([wd[0], wd[4], wd[5]], [(-0.5, f + 0.2), (0.5, f + 0.2), (0.0, f + 1.25)])]
        self.play(AnimationGroup(*more, lag_ratio=0.2), run_time=0.9)
        self.at("chaos")
        chaos = T("chaos", 48, RED, font=TITLE_FONT).move_to([PANEL_C + 3.1, f + 0.9, 0])
        cc = np.array([PANEL_C, f + 1.2, 0])
        angs = np.linspace(np.pi / 2 - 0.7, np.pi / 2 + 0.7, 5)
        sparks = VGroup(*[Line(cc + 0.85 * np.array([np.cos(a), np.sin(a), 0]), cc + 1.4 * np.array([np.cos(a), np.sin(a), 0]),
                               color=RED, stroke_width=4) for a in angs])
        jit = [d.animate.shift(RIGHT * np.random.uniform(-0.1, 0.1) + UP * np.random.uniform(-0.06, 0.06)) for d in wd]
        self.play(pop(chaos), LaggedStart(*[Create(sp) for sp in sparks], lag_ratio=0.1),
                  AnimationGroup(*jit), run_time=0.8)
        self.at("They don't")
        strike = Line(chaos.get_left() + LEFT * 0.1, chaos.get_right() + RIGHT * 0.1, color=GOLD, stroke_width=6)
        dont = T("They don't.", 44, GOLD, font=TITLE_FONT).move_to([PANEL_C + 3.1, f + 2.55, 0])
        back = [d.animate.move_to([PANEL_C - 1.5 + 0.55 * i, 2.2, 0]).set_opacity(0.0) for i, d in enumerate(wd)]
        self.play(Create(strike), pop(dont), FadeOut(sparks), AnimationGroup(*back), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s03 induced fit
class S03Fit(ProfileScene):
    def construct(self):
        self.add_inset()
        en = Enz(gap=OPEN_GAP, cx=PANEL_C, cy=-1.55)
        self.add(en.grp)
        top = T("something must change", 36, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.95, 0])
        self.at("something must change")
        self.play(pop(top), run_time=0.6)

        self.at("real substrate")
        sub = substrate(GREEN).move_to([PANEL_C, 1.55, 0])
        sl = T("real substrate", 28, GREEN).move_to([PANEL_C + 2.9, 1.55, 0])
        self.play(pop(sub), pop(sl), run_time=0.5)
        self.at("arrives")
        self.play(sub.animate.move_to([PANEL_C, 0.55, 0]), sl.animate.move_to([PANEL_C + 2.9, 0.55, 0]), run_time=0.8)

        self.at("The hand")
        hand = T("hand", 32, GREEN).move_to([PANEL_C + 2.9, 0.55, 0])
        self.play(ReplacementTransform(sl, hand), run_time=0.4)
        self.at("slide into")
        rest_y = en.floor_y() + SUB * K / 2
        self.play(sub.animate.move_to([PANEL_C, rest_y, 0]), hand.animate.move_to([PANEL_C + 2.9, rest_y + 0.1, 0]), run_time=0.9)
        self.at("preformed glove")
        glove = T("a pre-formed glove", 32, BLUE).move_to([PANEL_C, -2.85, 0])
        self.play(pop(glove), run_time=0.5)

        self.at("the glove changes")
        glove2 = T("the glove changes shape around the hand", 32, BLUE).move_to([PANEL_C, -2.85, 0])
        self.play(ReplacementTransform(glove, glove2), *en.clamp(0.3), run_time=1.5)
        self.play(Indicate(sub, color=GREEN, scale_factor=1.06), run_time=0.5)

        self.at("Binding induces")
        top2 = T("binding induces a conformational change", 32, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.95, 0])
        self.play(ReplacementTransform(top, top2), run_time=0.6)
        self.at("induced fit")
        fit_t = T("induced fit", 60, GOLD, font=TITLE_FONT).move_to([PANEL_C, 1.7, 0])
        rule = Line(fit_t.get_corner(DL) + DOWN * 0.1, fit_t.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=4)
        self.play(Write(fit_t, run_time=0.9), Create(rule), run_time=0.9)

        # water is too small to force it: reopen, then water nudges the open site and nothing closes
        self.at("water is", lead=0.3)
        wcap = T("too small to force it", 32, WATER).move_to([PANEL_C, -2.85, 0])
        wd = water_dot(PANEL_C - 1.8, 0.4)
        self.play(FadeOut(sub), FadeOut(hand), ReplacementTransform(glove2, wcap), FadeIn(wd, scale=0.5), *en.unclamp(0.3), run_time=0.6)
        self.at("small", lead=0.15)
        self.play(wd.animate.move_to([PANEL_C - 0.4, en.floor_y() + 0.5, 0]), run_time=0.45)
        self.at("force")
        self.play(wd.animate.shift(RIGHT * 0.2), run_time=0.2)
        self.play(wd.animate.shift(LEFT * 0.15), run_time=0.2)
        self.finish()


# ----------------------------------------------------------------------------- s04 journals and PNAS
class S04Journals(ProfileScene):
    def construct(self):
        self.add_inset()
        wall_x = 2.1
        idea = lab("induced fit", GOLD, 32)
        idea.move_to([-0.55, 0.1, 0])
        self.at("The idea", lead=0.0)
        self.play(pop(idea), run_time=0.5)

        self.at("against the dogma")
        dog = lab("the dogma", RED, 28).move_to([-0.55, 1.75, 0])
        self.play(pop(dog), run_time=0.5)
        # the idea pushes up against the dogma (an arrow, so the word "dogma" stays readable)
        cut = Arrow(idea.get_top() + UP * 0.05, dog.get_bottom() + DOWN * 0.02, buff=0, color=GOLD, stroke_width=5,
                    max_tip_length_to_length_ratio=0.35)
        self.at("dogma", lead=0.1)
        self.play(GrowArrow(cut), run_time=0.3)
        self.play(Wiggle(dog, scale_value=1.06, rotation_angle=0.03 * TAU), run_time=0.5)

        # the wall of standard journals (three pieces; the middle one is the loophole)
        top_p = Rectangle(width=0.7, height=1.9, stroke_color=PLACE, stroke_width=3, fill_color=PLACE, fill_opacity=0.3)
        mid_p = Rectangle(width=0.7, height=1.0, stroke_color=PLACE, stroke_width=3, fill_color=PLACE, fill_opacity=0.3)
        bot_p = Rectangle(width=0.7, height=2.2, stroke_color=PLACE, stroke_width=3, fill_color=PLACE, fill_opacity=0.3)
        top_p.move_to([wall_x, 1.65, 0]); mid_p.move_to([wall_x, 0.1, 0]); bot_p.move_to([wall_x, -1.6, 0])
        wl = T("standard journals", 28, PLACE).move_to([wall_x + 0.6, 2.95, 0])
        self.at("standard journals")
        self.play(FadeIn(VGroup(top_p, mid_p, bot_p), shift=LEFT * 0.2), pop(wl), FadeOut(cut), run_time=0.6)
        self.at("blocked")
        blocked = T("blocked", 34, RED, font=TITLE_FONT).move_to([wall_x - 1.3, -0.75, 0])
        self.play(idea.animate.shift(RIGHT * 1.1), run_time=0.35, rate_func=rush_into)
        self.play(idea.animate.shift(LEFT * 0.5), pop(blocked), Flash(mid_p.get_left(), color=RED, line_length=0.2, flash_radius=0.4),
                  run_time=0.4)

        self.at("one reviewer's")
        rev = lab(["one reviewer's", "verdict"], RED, 26).move_to([-1.0, -2.3, 0])
        rev.shift(RIGHT * 0.0)
        self.play(pop(rev), run_time=0.5)
        self.at("famous")
        self.play(Indicate(rev, color=RED, scale_factor=1.08), run_time=0.7)

        self.at("slipped it")
        # the middle piece slides away: a loophole opens at the height of the idea
        idea_home = [-0.55, 0.1, 0]
        self.play(FadeOut(VGroup(dog, blocked)), idea.animate.move_to(idea_home), mid_p.animate.shift(UP * 0.0).set_opacity(0.0),
                  run_time=0.5)
        pnas = lab("PNAS", PLACE, 34).move_to([5.45, 0.1, 0])
        self.at("PNAS")
        yr = M("1958", 40, YELLOW).move_to([5.45, 1.2, 0])
        self.play(pop(pnas), idea.animate.move_to([pnas.get_left()[0] - 1.15, 0.1, 0]).scale(0.75), run_time=0.8)
        self.at("1958")
        self.play(Write(yr), run_time=0.5)
        self.at("loophole")
        lp = T("a loophole", 32, GOLD, font=TITLE_FONT).move_to([wall_x + 1.9, -1.0, 0])
        arrow = Arrow(lp.get_left() + LEFT * 0.08 + UP * 0.1, [wall_x + 0.32, -0.25, 0], buff=0, color=GOLD, stroke_width=4,
                      max_tip_length_to_length_ratio=0.3)
        self.play(pop(lp), GrowArrow(arrow), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s05 proof and the moving machines
class S05Proof(ProfileScene):
    def construct(self):
        self.add_inset()
        xr = lab("X-ray crystallography", YELLOW, 30).move_to([PANEL_C, 2.95, 0])
        en = Enz(gap=OPEN_GAP, cx=PANEL_C, cy=-1.55)
        self.at("X ray", lead=0.1)
        self.play(pop(xr), FadeIn(en.grp, shift=UP * 0.1), run_time=0.7)
        self.at("proved him right")
        ck = checkmark(GOLD, 0.5).move_to([PANEL_C - 2.3, 1.6, 0])
        pr = T("proved him right", 40, GOLD, font=TITLE_FONT).move_to([PANEL_C + 0.45, 1.6, 0])
        self.play(Create(ck), pop(pr), run_time=0.8)

        self.at("flex")
        fl = T("flex", 36, BLUE, font=TITLE_FONT).move_to([PANEL_C - 2.3, -2.75, 0])
        self.play(pop(fl), Rotate(en.jl, angle=0.22, about_point=en.jl.get_bottom()),
                  Rotate(en.jr, angle=-0.22, about_point=en.jr.get_bottom()), run_time=0.45)
        self.play(Rotate(en.jl, angle=-0.22, about_point=en.jl.get_bottom()),
                  Rotate(en.jr, angle=0.22, about_point=en.jr.get_bottom()), run_time=0.3)
        self.at("shift")
        sh = T("shift", 36, BLUE, font=TITLE_FONT).move_to([PANEL_C, -2.75, 0])
        self.play(pop(sh), en.jl.animate.shift(RIGHT * 0.35), en.jr.animate.shift(RIGHT * 0.35), run_time=0.4)
        self.play(en.jl.animate.shift(LEFT * 0.35), en.jr.animate.shift(LEFT * 0.35), run_time=0.2)
        self.at("clamp")
        cl = T("clamp down", 36, BLUE, font=TITLE_FONT).move_to([PANEL_C + 2.3, -2.75, 0])
        sub = substrate(GREEN).move_to([PANEL_C, 0.7, 0])
        self.play(pop(cl), FadeIn(sub, shift=DOWN * 0.1), run_time=0.3)
        self.play(sub.animate.move_to([PANEL_C, en.floor_y() + SUB * K / 2, 0]), *en.clamp(0.3), run_time=0.6)

        # He had moved biochemistry from static structures to moving machines
        self.at("He had moved", lead=0.3)
        unit = VGroup(en.grp, sub)
        right_c = [PANEL_C + 2.1, -0.9, 0]
        self.play(FadeOut(VGroup(xr, ck, pr, fl, sh, cl)), unit.animate.scale(0.8).move_to(right_c), run_time=0.7)
        self.at("static structures")
        by = en.base.get_center()[1]
        st = Enz(gap=OPEN_GAP, color=GREY, cx=PANEL_C - 2.1, cy=by, scale=0.8 * K)
        stl = T("static structures", 30, GREY).move_to([PANEL_C - 2.1, by - 0.95, 0])
        self.play(FadeIn(st.grp, shift=UP * 0.1), pop(stl), run_time=0.6)
        self.at("to one of", lead=0.0)
        arr = Arrow([PANEL_C - 0.4, by + 0.5, 0], [PANEL_C + 0.4, by + 0.5, 0], buff=0, color=GOLD, stroke_width=6,
                    max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(arr), run_time=0.4)
        self.at("moving machines")
        mm = T("moving machines", 30, BLUE).move_to([PANEL_C + 2.1, by - 0.95, 0])
        self.play(pop(mm), run_time=0.4)
        # sequential plays: each .animate target must be built from the jaws' current position
        for mv in (en.unclamp, en.clamp, en.unclamp, en.clamp):
            self.play(*mv(0.3), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------- s06 quote (silent)
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“What is new is not true,", "and what is true is not new.”"]
        q = VGroup(*[T(l, 40, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(q, max_w=8.4)
        a1 = T("— an anonymous reviewer's dismissal of", 28, GOLD)
        a2 = T("Koshland's induced-fit paper", 28, GOLD)
        a3 = T("as recounted in The Molecule Hunters", 24, GREY)
        who = VGroup(a1, a2, a3).arrange(DOWN, aligned_edge=RIGHT, buff=0.12)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
        fit(g, max_w=8.5)
        g.move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.9)
        self.wait(0.5)
        self.play(who.animate.set_opacity(1.0), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Replaced Fischer's rigid lock with “induced fit”: enzymes reshape around substrates."

    def construct(self):
        a = T("Replaced Fischer's rigid lock with “induced fit”:", size=42, font=TITLE_FONT)
        b = T("enzymes reshape around substrates.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        fit(line, max_w=12.0)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
