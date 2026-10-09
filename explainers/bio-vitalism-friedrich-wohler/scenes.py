"""Friedrich Wöhler: scientist profile video (Biochemistrypedia, vitalism lesson)

The portrait (public/scientists/friedrich-wohler.png, an AI-generated engraving-style illustration from
The Molecule Hunters, cropped to the figure) is the anchor: the title scene pushes in on it, then it stays
as a framed inset on the left while the right side animates the story's beats as the narrator reaches them.
Every cue is a self.at("spoken words") lookup in audio/words.json (word timestamps of the real audio).
Nothing on screen adds a fact that is not in this lesson entry (name, dates, contribution, story, quotes).
No molecular structure is drawn: the flask is a schematic apparatus, the compounds are labelled chips.

COLOR MAP (one color per concept, whole video)
  GOLD   = Wöhler himself, the portrait frame, the insight (the confession, "structure changes everything")
  YELLOW = dates and ages (February 1828, 27)
  TEAL   = the letter / correspondence, and "structure" (different structures)
  BLUE   = ammonium cyanate, the inorganic salt
  GREEN  = urea, and its natural twin
  AMBER  = heat (warming the flask)
  PLUM   = nitrogen
  KHAKI  = organic chemistry, the primeval forest
  RED    = what he did not claim (struck-through "conquered")
  GREY   = labels, apparatus, Berzelius, the body
"""
import os
import random
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

AMBER = "#E0A458"
PLUM = "#B39DDB"
KHAKI = "#B59A62"
CX = 1.95              # centre of the content panel to the right of the portrait column
PORT_X = -4.8          # portrait column centre
PORT_H = 3.4
PORT_Y = 1.25
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "wohler_crop.png"   # 700x700 crop of the engraving
NAME = "Friedrich Wöhler"
DATES = "1800–1882"
CAPTION = "illustration · AI-generated"


def portrait(height=PORT_H, center=(PORT_X, PORT_Y)):
    img = ImageMobject(str(IMG))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height)
    img.move_to([center[0], center[1], 0])
    img.set_z_index(0)
    border = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    border.move_to(img).set_z_index(3)
    return img, border


def column_labels():
    """Caption under the portrait, then name and dates."""
    y = PORT_Y - PORT_H / 2
    cap = T(CAPTION, 22, GREY).move_to([PORT_X, y - 0.32, 0])
    nm = VGroup(T(NAME, 30, TEXT, font=TITLE_FONT), T(DATES, 26, GOLD)).arrange(DOWN, buff=0.12)
    nm.move_to([PORT_X, y - 1.25, 0])
    return cap, nm


def flask(center, s=1.0):
    """Schematic Erlenmeyer flask (apparatus, not a molecule): outline + liquid polygon."""
    cx, cy = center
    def P(x, y):
        return [cx + x * s, cy + y * s, 0]
    outline = Polygon(P(-0.28, 1.4), P(-0.28, 0.7), P(-1.1, -0.7), P(1.1, -0.7), P(0.28, 0.7), P(0.28, 1.4),
                      stroke_color=GREY, stroke_width=4, fill_opacity=0)
    # liquid fills the lower body up to y = 0.0
    k = 0.85 / 1.4
    xl = 0.28 + (0.7 - 0.0) * k
    liquid = Polygon(P(-1.1, -0.7), P(1.1, -0.7), P(xl, 0.0), P(-xl, 0.0),
                     stroke_width=0, fill_color=BLUE, fill_opacity=0.55)
    rim = Line(P(-0.4, 1.4), P(0.4, 1.4), color=GREY, stroke_width=4)
    return outline, liquid, rim


def heat_waves(cx, y0, n=3, color=AMBER):
    waves = VGroup()
    for i in range(n):
        x0 = cx + (i - (n - 1) / 2) * 0.62
        w = ParametricFunction(lambda t, x0=x0: np.array([x0 + 0.09 * np.sin(2.6 * t + i), y0 + t, 0]),
                               t_range=[0, 0.75], color=color, stroke_width=5)
        waves.add(w)
    return waves


def crystal(center, color=GREEN, r=0.85):
    """A macroscopic crystal icon: hexagon outline with three facet edges (no atoms, no bonds)."""
    cx, cy = center
    pts = [[cx + r * np.cos(np.pi / 6 + k * np.pi / 3), cy + r * np.sin(np.pi / 6 + k * np.pi / 3), 0] for k in range(6)]
    hexa = Polygon(*pts, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.2)
    facets = VGroup(*[Line([cx, cy, 0], pts[k], color=color, stroke_width=3) for k in (1, 3, 5)])
    return VGroup(hexa, facets)


def tree(x, y, h, color=KHAKI):
    w = 0.62 * h
    tri = Polygon([x - w / 2, y + 0.18 * h, 0], [x + w / 2, y + 0.18 * h, 0], [x, y + h, 0],
                  stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.28)
    trunk = Line([x, y, 0], [x, y + 0.2 * h, 0], color=color, stroke_width=3)
    return VGroup(trunk, tri)


class BioScene(SpokenScene):
    def add_column(self):
        img, border = portrait()
        cap, nm = column_labels()
        self.add(img, border, cap, nm)

    def chip_at(self, text, color, x, y, size=28, **kw):
        c = chip(text, color, size, **kw)
        c.move_to([x, y, 0])
        return c


# ----------------------------------------------------------------------------- s00 title
class S00Title(BioScene):
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA  ·  SCIENTIST PROFILE", 22, TEAL, weight=BOLD).move_to([0, 3.4, 0])
        img, border = portrait()
        big_h = 4.0
        k = big_h / PORT_H
        big_c = np.array([0.0, 0.8, 0.0])
        for m in (img, border):
            m.scale(k, about_point=ORIGIN).move_to(big_c)
        cap = T(CAPTION, 22, GREY).move_to([0, 0.8 - big_h / 2 - 0.3, 0])
        name = T(NAME, 52, font=TITLE_FONT)
        name.move_to([0, -2.5, 0])
        dates = T(DATES, 28, GOLD).move_to([0, -3.2, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -2.9, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.6)
        # slow push-in while the name and dates arrive
        self.play(img.animate.scale(1.06), border.animate.scale(1.06),
                  Succession(Wait(0.5), Write(name, run_time=1.1), Wait(0.2), AnimationGroup(GrowFromCenter(rule), FadeIn(dates), run_time=0.4)),
                  run_time=3.6, rate_func=linear)
        self.wait(0.6)
        # hand over to the inset layout used by every later scene
        cap2, nm = column_labels()
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.06)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.06)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       FadeIn(nm)),
            run_time=0.9))
        self.finish()


# ----------------------------------------------------------------------------- s01 the letter
class S01Letter(BioScene):
    def construct(self):
        self.add_column()
        # timeline mark: February 1828
        ty = 2.75
        axis = Arrow([-2.2, ty, 0], [6.1, ty, 0], color=GREY, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.04)
        dot = Dot([-0.9, ty, 0], radius=0.12, color=YELLOW)
        date = T("February 1828", 36, YELLOW, weight=BOLD).next_to(dot, DOWN, buff=0.22, aligned_edge=LEFT).shift(LEFT * 0.3)
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.7)

        # Wöhler (left) and Berzelius (right)
        woh = self.chip_at("Wöhler", GOLD, -0.2, 0.7, 32)
        self.at("Wöhler", lead=0.6)
        self.play(FadeIn(woh, shift=UP * 0.1), run_time=0.4)

        ber_pos = [4.5, 0.7, 0]
        ber = self.chip_at("Berzelius", GREY, *ber_pos[:2], 32)
        arr = Arrow(woh.get_right() + RIGHT * 0.1, ber.get_left() + LEFT * 0.1, buff=0, color=TEAL, stroke_width=5,
                    max_tip_length_to_length_ratio=0.12)
        # the letter: a small envelope drawn from a rectangle and a flap
        env = VGroup(Rectangle(width=0.95, height=0.62, stroke_color=TEAL, stroke_width=3, fill_color=BG, fill_opacity=1),
                     Line([-0.475, 0.31, 0], [0, -0.02, 0], color=TEAL, stroke_width=3),
                     Line([0.475, 0.31, 0], [0, -0.02, 0], color=TEAL, stroke_width=3))
        env.move_to(woh.get_right() + RIGHT * 0.9 + UP * 0.0)
        self.at("wrote to", lead=0.35)
        self.play(GrowArrow(arr), FadeIn(env, shift=RIGHT * 0.2), run_time=0.6)
        self.at("old teacher", lead=0.4)
        self.play(env.animate.move_to([2.05, 0.7, 0]), FadeIn(ber, shift=LEFT * 0.2), run_time=0.9)
        old = T("his old teacher", 26, GREY).next_to(ber, DOWN, buff=0.25)
        self.play(FadeIn(old, shift=UP * 0.1), run_time=0.4)

        # the confession
        self.at("a confession")
        conf = T("a confession", 42, GOLD, font=TITLE_FONT).move_to([CX, -1.15, 0])
        ul = Line(conf.get_corner(DL) + DOWN * 0.1, conf.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=4)
        self.play(env.animate.scale(1.25).set_stroke(GOLD), FadeIn(conf, shift=UP * 0.1), Create(ul), run_time=0.7)
        self.at("he could not keep")
        keep = T("he could not keep it to himself", 30, GREY).move_to([CX, -2.3, 0])
        self.play(FadeIn(keep, shift=UP * 0.1), Wiggle(woh, scale_value=1.1, rotation_angle=0.03 * TAU, run_time=1.0), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------- s02 the experiment
class S02Urea(BioScene):
    def construct(self):
        self.add_column()
        fc = (1.0, -0.15)
        outline, liquid, rim = flask(fc)
        waves = heat_waves(fc[0], -1.65)
        warm = T("warmed", 30, AMBER).move_to([2.95, -1.35, 0])

        # warmed ... ammonium cyanate, an inorganic salt
        self.at("warmed", lead=0.25)
        self.play(Create(outline), Create(rim), Create(waves), FadeIn(warm, shift=LEFT * 0.15), run_time=0.7)
        salt = self.chip_at("ammonium cyanate", BLUE, 1.0, 2.55, 28)
        down = Arrow(salt.get_bottom() + DOWN * 0.05, [1.0, 1.55, 0], buff=0, color=BLUE, stroke_width=4,
                     max_tip_length_to_length_ratio=0.3)
        self.at("ammonium cyanate", lead=0.15)
        self.play(FadeIn(salt, shift=DOWN * 0.1), GrowArrow(down), run_time=0.5)
        self.play(FadeIn(liquid), run_time=0.4)
        self.at("inorganic salt", lead=0.15)
        inorg = T("an inorganic salt", 26, GREY).move_to([4.95, 2.55, 0])
        self.play(FadeIn(inorg, shift=LEFT * 0.15), run_time=0.4)

        # watched it turn into urea
        self.at("watched it turn")
        urea = self.chip_at("urea", GREEN, 5.0, -0.15, 34)
        out = Arrow([2.3, -0.15, 0], urea.get_left() + LEFT * 0.1, buff=0, color=GREEN, stroke_width=5,
                    max_tip_length_to_length_ratio=0.25)
        self.play(liquid.animate.set_fill(GREEN, 0.55), run_time=0.9)
        self.at("urea", lead=0.3)
        self.play(GrowArrow(out), FadeIn(urea, shift=LEFT * 0.2), run_time=0.6)

        # a molecule the body makes to dump nitrogen
        self.at("a molecule", lead=0.5)
        self.play(FadeOut(Group(outline, liquid, rim, waves, warm, salt, down, inorg, out)),
                  urea.animate.move_to([2.3, 0.5, 0]), run_time=0.5)
        body = self.chip_at("the body", GREY, -1.0, 0.5, 30)
        a1 = Arrow(body.get_right() + RIGHT * 0.08, [1.55, 0.5, 0], buff=0, color=GREY, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        mk = T("makes", 24, GREY).next_to(a1, UP, buff=0.12)
        self.at("the body", lead=0.1)
        self.play(FadeIn(body, shift=RIGHT * 0.15), GrowArrow(a1), FadeIn(mk), run_time=0.5)
        nit = self.chip_at("nitrogen", PLUM, 5.5, 0.5, 30)
        a2 = Arrow([3.05, 0.5, 0], nit.get_left() + LEFT * 0.08, buff=0, color=PLUM, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        dump = T("to dump", 24, PLUM).next_to(a2, UP, buff=0.12)
        self.at("dump nitrogen", lead=0.35)
        self.play(GrowArrow(a2), FadeIn(dump), FadeIn(nit, shift=LEFT * 0.15), run_time=0.6)

        # identical to the natural product, down to the crystal
        self.at("identical", lead=0.45)
        # keep the body -> urea -> nitrogen chain on screen as context: lift it to the top band
        chain = VGroup(body, a1, mk, urea, a2, dump, nit)
        self.play(chain.animate.scale(0.92).move_to([CX, 2.7, 0]), run_time=0.35)
        c1 = crystal((-0.2, 0.4), GREEN)
        c2 = crystal((4.1, 0.4), GREEN)
        l1 = T("Wöhler's urea", 28, GREEN).next_to(c1, DOWN, buff=0.3)
        l2 = T("natural product", 28, GREEN).next_to(c2, DOWN, buff=0.3)
        eq = M("=", 64, GOLD).move_to([1.95, 0.4, 0])
        self.play(Create(c1), FadeIn(l1), run_time=0.5)
        self.at("natural product", lead=0.25)
        self.play(Create(c2), FadeIn(l2), FadeIn(eq, scale=1.5), run_time=0.6)
        self.at("down to the crystal", lead=0.1)
        ident = T("identical, down to the crystal", 34, GOLD, font=TITLE_FONT).move_to([CX, -2.2, 0])
        self.play(Write(ident), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------- s03 structure
class S03Structure(BioScene):
    def construct(self):
        self.add_column()
        self.at("twenty", lead=0.05)
        age = M("27", 66, YELLOW).move_to([-0.7, 2.7, 0])
        yo = T("years old", 28, YELLOW).next_to(age, RIGHT, buff=0.3).align_to(age, DOWN).shift(UP * 0.02)
        self.play(Write(age), FadeIn(yo, shift=LEFT * 0.1), run_time=0.7)
        self.at("understood at once", lead=0.1)
        und = T("understood at once", 36, GOLD, font=TITLE_FONT).move_to([4.2, 2.7, 0])
        self.play(FadeIn(und, shift=UP * 0.1), run_time=0.6)

        self.at("what he held", lead=0.2)
        a = self.chip_at("ammonium cyanate", BLUE, 0.0, 0.5, 28)
        u = self.chip_at("urea", GREEN, 4.4, 0.5, 30)
        link = DoubleArrow(a.get_right() + RIGHT * 0.08, u.get_left() + LEFT * 0.08, buff=0, color=GREY, stroke_width=4,
                           max_tip_length_to_length_ratio=0.25)
        self.play(FadeIn(a, shift=RIGHT * 0.15), FadeIn(u, shift=LEFT * 0.15), GrowFromCenter(link), run_time=0.7)

        self.at("same atoms", lead=0.25)
        bt = Brace(Group(a, u), UP, color=GREY, buff=0.15)
        lt = T("same atoms", 32, GREY).next_to(bt, UP, buff=0.12)
        self.play(GrowFromCenter(bt), FadeIn(lt, shift=DOWN * 0.1), run_time=0.7)
        self.at("different structures", lead=0.3)
        bb = Brace(Group(a, u), DOWN, color=TEAL, buff=0.15)
        lb = T("different structures", 32, TEAL).next_to(bb, DOWN, buff=0.12)
        self.play(GrowFromCenter(bb), FadeIn(lb, shift=UP * 0.1), run_time=0.7)

        self.at("structure changes everything", lead=0.3)
        big = T("structure changes everything", 42, GOLD, font=TITLE_FONT).move_to([CX, -2.5, 0])
        fit(big, max_w=8.5)
        self.play(Write(big), run_time=1.3)
        self.play(Indicate(big, color=GOLD, scale_factor=1.04), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s04 the forest
class S04Forest(BioScene):
    def construct(self):
        self.add_column()
        self.at("never claimed", lead=0.1)
        con = self.chip_at("conquered the field he opened", GREY, CX, 2.75, 28)
        self.play(FadeIn(con, shift=DOWN * 0.1), run_time=0.5)
        self.at("conquered", lead=0.05)
        strike = Line(con.get_left() + RIGHT * 0.15, con.get_right() + LEFT * 0.15, color=RED, stroke_width=6)
        nope = T("never claimed", 28, RED).next_to(con, DOWN, buff=0.18)
        self.play(Create(strike), run_time=0.45)
        self.play(FadeIn(nope, shift=UP * 0.1), run_time=0.35)

        self.at("organic chemistry", lead=0.3)
        self.play(FadeOut(nope), run_time=0.15)
        org = self.chip_at("organic chemistry", KHAKI, -0.15, 1.65, 28)
        self.play(FadeIn(org, shift=DOWN * 0.1), run_time=0.5)

        # the forest grows
        rnd = random.Random(7)
        trees = VGroup()
        for row, y in enumerate(np.linspace(-2.15, 0.0, 6)):
            for x in np.arange(-0.9 + 0.3 * (row % 2), 6.25, 0.58):
                trees.add(tree(x + rnd.uniform(-0.12, 0.12), y + rnd.uniform(-0.08, 0.08), rnd.uniform(0.62, 0.95)))
        # draw back rows first so nearer trees overlap them
        for t in trees:
            t.set_z_index(0)
        eq = M("=", 40, KHAKI).next_to(org, RIGHT, buff=0.3)
        prim = T("a primeval forest", 30, KHAKI, font=TITLE_FONT).next_to(eq, RIGHT, buff=0.3)
        # Wöhler waits at the forest's edge (appears with the forest so the label can be read)
        dot = Dot(radius=0.17, color=GOLD).move_to([-1.9, -1.1, 0])
        dot.set_z_index(6)
        wlab = T("Wöhler", 24, GOLD).move_to([-1.85, -0.55, 0])
        self.at("a primeval forest", lead=0.2)
        self.play(FadeIn(eq), FadeIn(prim, shift=LEFT * 0.1), FadeIn(dot), FadeIn(wlab),
                  LaggedStart(*[FadeIn(t, scale=0.6) for t in trees], lag_ratio=0.02), run_time=1.2)

        # Wöhler steps in, but only just
        self.at("only entered", lead=0.5)
        trail = Line([-1.9, -1.1, 0], [-0.1, -1.1, 0], color=GOLD, stroke_width=5)
        trail.set_z_index(5)
        self.play(dot.animate.move_to([-0.1, -1.1, 0]), Create(trail), FadeOut(wlab), run_time=0.9)
        only = T("only entered", 30, GOLD).move_to([-0.1, -3.0, 0])
        ptr = Arrow(only.get_top() + UP * 0.05, [-0.1, -1.35, 0], buff=0, color=GOLD, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        ptr.set_z_index(6)
        self.play(FadeIn(only, shift=UP * 0.1), GrowArrow(ptr), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s05 quote
class S05Quote(BioScene):
    def construct(self):
        self.add_column()
        lines = ["“I can no longer, as it were,", "hold back my chemical urine;", "and I have to let out that",
                 "I can make urea without", "needing a kidney.”"]
        q = VGroup(*[T(l, 36, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        fit(q, max_w=8.4)
        who = T("— Friedrich Wöhler", 30, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.5).move_to([CX, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.7)
        self.wait(0.5)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(BioScene):
    LINE = "Heated an inorganic salt, got urea: first crack between living and dead."

    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.0))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.0 - 1.15 - 0.3, 0])
        l1 = T("Heated an inorganic salt, got urea:", 38, font=TITLE_FONT)
        l2 = T("first crack between living and dead.", 38, font=TITLE_FONT)
        lg = VGroup(l1, l2).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters · Part I, “Vitalism Crumbles: Synthesis Without Life”", 22, GREY).move_to([0, -2.6, 0])
        fit(src, max_w=12.2)
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.5)
        self.finish()
