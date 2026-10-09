"""Jan Baptist van Helmont: scientist profile video (Biochemistrypedia, intro-biochemistry-cell-biology lesson)

The portrait (public/scientists/jan-van-helmont.png, an AI-generated engraving-style illustration from
The Molecule Hunters, cropped to the figure as helmont_crop.png) opens the video with a slow push-in, then
stays as a framed inset on the left while the right side animates the story's beats as the narrator reaches
them. Every cue is a self.at("spoken words") lookup in audio/words.json (word timestamps of the real audio).
Nothing on screen adds a fact that is not in the lesson entry (name, dates, contribution, story, quote).

COLOR MAP (one color per concept, whole video)
  GOLD   = van Helmont, the portrait frame, the principle (a measurable mark), "the bet"
  YELLOW = years
  GREEN  = the willow and its growth (the +164 pounds)
  AMBER  = soil / the dirt (the -2 ounces)
  BLUE   = water
  PURPLE = the invisible: the "something in the air", the vapor, Gas
  ROSE   = fermenting wine
  TEAL   = the chapter you are starting (Biochemistrypedia's cue color)
  RED    = what is ruled out (the dirt as the source, "the story")
  GREY   = structure, labels, the balance
No molecular structure is drawn anywhere (pot, sapling, balance, ruler, jar: schematic apparatus only).
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

AMBER = "#C98B5B"
PURPLE = "#B58CD9"
ROSE = "#C4546F"
CX = 1.7                  # centre of the content area to the right of the portrait column
PORT_X = -4.8
PORT_H = 3.7
PORT_Y = 1.3
CROP_AR = 730 / 930.0     # helmont_crop.png
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "helmont_crop.png"
CAPTION = "illustration · AI-generated"
NAME = "Jan Baptist van Helmont"
DATES = "1580–1644"
QUOTE = ("For want of a name, I have called that vapour Gas, being not far severed from the chaos "
         "of the ancients.")


def portrait(height=PORT_H, center=(PORT_X, PORT_Y)):
    img = ImageMobject(str(IMG))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height).move_to([center[0], center[1], 0]).set_z_index(0)
    border = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    border.move_to(img).set_z_index(3)
    return img, border


def column_labels():
    y = PORT_Y - PORT_H / 2
    cap = T(CAPTION, 22, GREY).move_to([PORT_X, y - 0.32, 0])
    nm = VGroup(T("Jan Baptist", 26, TEXT, font=TITLE_FONT), T("van Helmont", 26, TEXT, font=TITLE_FONT),
                T(DATES, 24, GOLD)).arrange(DOWN, buff=0.1).move_to([PORT_X, y - 1.55, 0])
    return cap, nm


# ---- schematic pieces -------------------------------------------------------------------------
def pot(cx, cy, w=2.0):
    """A flowerpot filled with soil (schematic): trapezoid + rim."""
    h = 1.0
    body = Polygon([cx - w / 2, cy + h / 2, 0], [cx + w / 2, cy + h / 2, 0],
                   [cx + w * 0.38, cy - h / 2, 0], [cx - w * 0.38, cy - h / 2, 0],
                   stroke_color=GREY, stroke_width=4, fill_color=AMBER, fill_opacity=0.55)
    rim = RoundedRectangle(corner_radius=0.05, width=w + 0.3, height=0.2, stroke_width=0,
                           fill_color=GREY, fill_opacity=0.9).move_to([cx, cy + h / 2 + 0.05, 0])
    return VGroup(body, rim)


def sapling(cx, base_y, h=1.9, leaves=4):
    """A stem with ellipse leaves (GREEN)."""
    stem = Line([cx, base_y, 0], [cx, base_y + h, 0], color=GREEN, stroke_width=6)
    lv = VGroup()
    for i in range(leaves):
        y = base_y + h * (0.35 + 0.65 * i / max(1, leaves - 1))
        side = -1 if i % 2 == 0 else 1
        lf = Ellipse(width=0.75, height=0.24, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
        lf.rotate(side * 0.5).move_to([cx + side * 0.36, y, 0])
        lv.add(lf)
    top = Ellipse(width=0.24, height=0.6, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to([cx, base_y + h + 0.2, 0])
    return VGroup(stem, lv, top)


def willow_icon(cx, cy, tall=1.9, leaves=4):
    """Pot + sapling as one group, pot centre at (cx, cy)."""
    p = pot(cx, cy)
    s = sapling(cx, cy + 0.6, tall, leaves)
    return VGroup(p, s)


def cross(mob, color=RED, pad=0.1, w=5):
    return VGroup(Line(mob.get_corner(UL) + [-pad, pad, 0], mob.get_corner(DR) + [pad, -pad, 0], color=color, stroke_width=w),
                  Line(mob.get_corner(DL) + [-pad, -pad, 0], mob.get_corner(UR) + [pad, pad, 0], color=color, stroke_width=w))


def dashed(mob, color, n=40, ratio=0.55):
    return DashedVMobject(mob, num_dashes=n, dashed_ratio=ratio).set_color(color)


def ghost_circle(center, r=0.55, solid=False, color=PURPLE):
    c = Circle(radius=r).move_to(center)
    if solid:
        return c.set_stroke(color, 5).set_fill(color, 0.25)
    return dashed(c, color, 28)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.25)


def chip_at(text, color, x, y, size=28, **kw):
    return chip(text, color, size, **kw).move_to([x, y, 0])


def dashed_chip(text, color, x, y, size=28):
    c = chip(text, color, size).move_to([x, y, 0])
    return VGroup(dashed(c[0], color, 44), c[1])


class BioScene(SpokenScene):
    def add_column(self):
        img, border = portrait()
        cap, nm = column_labels()
        self.add(img, border, cap, nm)


# ======================================================================================================
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
        fit(name, max_w=11.5)
        name.move_to([0, -2.5, 0])
        dates = T(DATES, 28, GOLD).move_to([0, -3.2, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -2.9, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.4)
        self.play(img.animate.scale(1.05), border.animate.scale(1.05), Write(name, run_time=1.0),
                  run_time=1.5, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.35)
        cap2, nm = column_labels()
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       FadeIn(nm)),
            run_time=0.8))
        self.finish()


# ======================================================================================================
class S01Planting(BioScene):
    """He planted a willow sapling in a measured pot of soil and watered it for five years."""

    def construct(self):
        self.add_column()
        px, py = -0.3, -1.0
        p = pot(px, py)
        self.play(FadeIn(p, shift=UP * 0.15), run_time=0.4)

        self.at("willow sapling")
        s = sapling(px, py + 0.6, 1.9, 4)
        lab_w = T("willow sapling", 28, GREEN).move_to([3.0, 0.7, 0])
        self.play(GrowFromPoint(s, [px, py + 0.6, 0]), FadeIn(lab_w, shift=LEFT * 0.2), run_time=0.7)

        self.at("measured pot of soil")
        lab_p = T("measured pot of soil", 28, AMBER).move_to([px, py - 1.1, 0])
        self.play(FadeIn(lab_p, shift=UP * 0.1), run_time=0.5)

        self.at("watered")
        wchip = chip_at("water", BLUE, 3.0, 2.3, 28)
        drops = VGroup(*[Dot(radius=0.08, color=BLUE).move_to([px + 1.15 + 0.3 * i, 2.3 - 0.15 * (i % 2), 0]) for i in range(3)])
        self.play(FadeIn(wchip), FadeIn(drops), run_time=0.2)
        self.play(*[d.animate.move_to([px + 0.55 + 0.35 * i, py + 0.55, 0]).set_opacity(0) for i, d in enumerate(drops)],
                  run_time=0.4, rate_func=rush_into)

        self.at("for five")
        sq = VGroup(*[Square(0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9) for _ in range(5)])
        sq.arrange(RIGHT, buff=0.18).move_to([3.7, -1.0, 0])
        yrs = T("five years", 30, YELLOW).move_to([3.7, -1.75, 0])
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in sq], lag_ratio=0.25), FadeIn(yrs), run_time=0.8)
        self.finish()


# ======================================================================================================
class S02Weighing(BioScene):
    """The tree gained 164 pounds, the soil lost 2 ounces. Where had the mass come from?"""

    def construct(self):
        self.add_column()
        base_y = -0.7
        tx, sx = 0.6, 4.0
        line = Line([-1.5, base_y, 0], [5.8, base_y, 0], color=GREY, stroke_width=3)
        c_tree = chip_at("the tree", GREEN, tx, 3.05, 30)
        c_soil = chip_at("the soil", AMBER, sx, 3.05, 30)
        self.play(Create(line), FadeIn(c_tree, shift=DOWN * 0.1), FadeIn(c_soil, shift=DOWN * 0.1), run_time=0.45)

        self.at("164")
        bar = Rectangle(width=1.3, height=2.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
        bar.move_to([tx, base_y + 1.25, 0])
        self.play(GrowFromEdge(bar, DOWN), run_time=0.9)
        lab_t = VGroup(T("gained", 26, GREY), M("164", 34, GREEN), T("pounds", 26, GREY)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        lab_t.move_to([tx, base_y + 2.5 + 0.38, 0])
        self.play(FadeIn(lab_t, shift=UP * 0.1), run_time=0.4)

        self.at("lost")
        sliver = Rectangle(width=1.3, height=0.05, stroke_width=0, fill_color=AMBER, fill_opacity=0.95)
        sliver.move_to([sx, base_y - 0.03, 0])
        self.play(GrowFromEdge(sliver, LEFT), run_time=0.4)
        lab_s = VGroup(T("lost", 26, GREY), M("2", 34, AMBER), T("ounces", 26, GREY)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        lab_s.move_to([sx, base_y - 0.7, 0])
        self.play(FadeIn(lab_s, shift=DOWN * 0.1), run_time=0.4)

        self.at("Where had")
        q = T("?", 120, GOLD, font=TITLE_FONT).move_to([2.3, base_y + 1.5, 0])
        ask = T("Where had the mass come from?", 34, GOLD, font=TITLE_FONT).move_to([CX, -2.6, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ======================================================================================================
class S03Source(BioScene):
    """Not the dirt (barely moved) -- from water, and from something in the air he could not see, weigh, or hold."""

    def construct(self):
        self.add_column()
        target = chip_at("the tree: +164 pounds", GREEN, 4.3, 0.3, 24)
        tl = target.get_left()[0] - 0.12
        XR = 1.0   # right edge of the three source chips
        self.at("not the dirt")
        dirt = chip("the dirt", AMBER, 30).move_to([0, 1.9, 0]); dirt.shift(RIGHT * (XR - dirt.get_right()[0]))
        a1 = arrow(dirt.get_right() + RIGHT * 0.12, [tl, 0.62, 0], AMBER)
        self.play(FadeIn(target, shift=LEFT * 0.2), FadeIn(dirt, shift=RIGHT * 0.2), GrowArrow(a1), run_time=0.6)

        self.at("barely moved")
        bm = T("barely moved", 26, GREY).next_to(dirt, DOWN, buff=0.28).align_to(dirt, RIGHT)
        mid = a1.get_center()
        x = VGroup(Line(mid + [-0.25, 0.25, 0], mid + [0.25, -0.25, 0], color=RED, stroke_width=6),
                   Line(mid + [-0.25, -0.25, 0], mid + [0.25, 0.25, 0], color=RED, stroke_width=6))
        self.play(FadeIn(bm, shift=UP * 0.1), Create(x), dirt.animate.set_opacity(0.55),
                  a1.animate.set_stroke(opacity=0.35), run_time=0.6)

        self.at("water")
        water = chip("water", BLUE, 30).move_to([0, 0.2, 0]); water.shift(RIGHT * (XR - water.get_right()[0]))
        a2 = arrow(water.get_right() + RIGHT * 0.12, [tl, 0.3, 0], BLUE)
        self.play(FadeIn(water, shift=RIGHT * 0.2), GrowArrow(a2), run_time=0.6)

        self.at("something in the air")
        air = dashed_chip("something in the air", PURPLE, 0, -1.3, 26)
        air.shift(RIGHT * (XR - air.get_right()[0]))
        a3 = arrow(air.get_right() + RIGHT * 0.12, [tl, -0.02, 0], PURPLE).set_stroke(opacity=0.7)
        self.play(FadeIn(air, shift=RIGHT * 0.2), GrowArrow(a3), run_time=0.7)

        self.at("could not see")
        n1 = T("could not see", 26, PURPLE).move_to([-0.9, -2.6, 0])
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.4)
        self.at("weigh")
        n2 = T("weigh", 26, PURPLE).move_to([1.6, -2.6, 0])
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.4)
        self.at("hold")
        n3 = T("or hold", 26, PURPLE).move_to([4.1, -2.6, 0])
        self.play(FadeIn(n3, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ======================================================================================================
def ruler(x0, x1, y, n=9, color=GREY):
    base = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4)
    ticks = VGroup(*[Line([x0 + (x1 - x0) * i / (n - 1), y, 0], [x0 + (x1 - x0) * i / (n - 1), y + 0.2, 0], color=color,
                          stroke_width=3) for i in range(n)])
    return VGroup(base, ticks)


def wisp(x, y0, h=1.5, phase=0.0, color=PURPLE):
    f = ParametricFunction(lambda t: np.array([x + 0.14 * np.sin(5 * t + phase), y0 + h * t, 0]), t_range=[0, 1],
                           color=color, stroke_width=5)
    return f


class S04Gas(BioScene):
    """That same instinct ... the vapor that boils off fermenting wine ... Gas ... chaos."""

    def construct(self):
        self.add_column()
        # --- stage A: the invisible leaves a measurable mark
        self.at("same instinct", lead=0.0)
        head = T("that same instinct", 32, GOLD, font=TITLE_FONT).move_to([CX, 3.0, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        self.at("invisible")
        gh = ghost_circle([-0.4, 0.9, 0], 0.8)
        gl = T("the invisible", 28, PURPLE).move_to([-0.4, -0.3, 0])
        self.play(Create(gh), FadeIn(gl), run_time=0.6)
        self.at("could be real")
        gh2 = ghost_circle([-0.4, 0.9, 0], 0.8, solid=True)
        gl2 = T("could be real", 28, PURPLE).move_to([-0.4, -0.85, 0])
        self.play(FadeOut(gh), FadeIn(gh2), FadeIn(gl2, shift=UP * 0.1), run_time=0.5)
        self.at("left a")
        rl = ruler(2.0, 5.8, 0.6, 9)
        a = arrow([0.6, 0.9, 0], [1.8, 0.9, 0], GOLD)
        self.play(GrowArrow(a), Create(rl), run_time=0.5)
        self.at("measurable mark")
        mark = Line([4.1, 0.6, 0], [4.1, 1.45, 0], color=GOLD, stroke_width=8)
        ml = T("a measurable mark", 30, GOLD).move_to([4.0, -0.3, 0])
        self.play(Create(mark), FadeIn(ml, shift=UP * 0.1), run_time=0.6)

        # --- stage B: the vapor off fermenting wine
        self.at("led him to", lead=0.3)
        self.play(FadeOut(VGroup(head, gh2, gl, gl2, a, rl, mark, ml)), run_time=0.3)
        jx, jy = -0.8, 0.0
        jar = RoundedRectangle(corner_radius=0.2, width=1.5, height=1.7, stroke_color=GREY, stroke_width=4).move_to([jx, jy, 0])
        wine = Rectangle(width=1.38, height=1.0, stroke_width=0, fill_color=ROSE, fill_opacity=0.65).move_to([jx, jy - 0.34, 0])
        jarg = VGroup(wine, jar)
        self.play(FadeIn(jarg, shift=UP * 0.1), run_time=0.4)
        self.at("vapor")
        ws = VGroup(wisp(jx - 0.35, jy + 0.95, 1.6, 0.0), wisp(jx, jy + 0.95, 1.8, 1.7), wisp(jx + 0.35, jy + 0.95, 1.5, 3.2))
        vl = T("vapor", 28, PURPLE).move_to([1.0, 2.45, 0])
        self.play(LaggedStart(*[Create(w) for w in ws], lag_ratio=0.25), FadeIn(vl), run_time=0.8)
        self.at("boils off")
        bubs = VGroup()
        for i in range(3):
            d = Dot(radius=0.07, color=TEXT)
            d.phase = i / 3.0
            d.bx = jx - 0.4 + 0.4 * i

            def upd(m, dt):
                m.phase = (m.phase + dt * 0.7) % 1.0
                m.move_to([m.bx, jy - 0.7 + 0.85 * m.phase, 0])
                m.set_opacity(0.85 * (1 - m.phase))
            d.add_updater(upd)
            bubs.add(d)
        self.add(bubs)
        self.wait(0.3)
        self.at("fermenting wine")
        fw = T("fermenting wine", 26, ROSE).move_to([jx, jy - 1.2, 0])
        self.play(FadeIn(fw, shift=UP * 0.1), run_time=0.5)

        # --- the word
        self.at("coined a word")
        box = RoundedRectangle(corner_radius=0.15, width=2.9, height=1.1, stroke_color=GOLD, stroke_width=3).move_to([3.7, 1.5, 0])
        dbox = dashed(box, GOLD, 40)
        arr = arrow([0.55, 1.5, 0], [2.1, 1.5, 0], PURPLE)
        self.play(Create(dbox), GrowArrow(arr), run_time=0.7)
        self.at("Greek")
        gk = T("from the Greek", 26, GREY).move_to([3.7, 2.45, 0])
        self.play(FadeIn(gk, shift=DOWN * 0.1), run_time=0.4)
        self.at("chaos")
        chaos = T("chaos", 44, GOLD, font=TITLE_FONT).move_to([3.7, 1.5, 0])
        self.play(Write(chaos), run_time=0.7)

        # --- the quote, as it is spoken
        self.at("For want of a name")
        q1 = T("“For want of a name, I have called", 30, TEXT, font=TITLE_FONT)
        q2 = T("that vapour Gas, being not far severed", 30, TEXT, font=TITLE_FONT, t2c={"Gas": PURPLE})
        q3 = T("from the chaos of the ancients.”", 30, TEXT, font=TITLE_FONT, t2c={"chaos": GOLD})
        qg = VGroup(q1, q2, q3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fit(qg, max_w=8.4)
        qg.move_to([CX + 0.4, -2.55, 0])
        for ql in (q2, q3):
            ql.align_to(q1, LEFT)
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.8)
        self.at("that vapor")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.6)
        self.at("gas", lead=0.15)
        gas = T("Gas", 52, PURPLE, font=TITLE_FONT).move_to([3.7, 1.5, 0])
        gk2 = T("coined from chaos", 26, GREY).move_to([3.7, 2.45, 0])
        self.play(ReplacementTransform(chaos, gas), ReplacementTransform(gk, gk2), dbox.animate.set_color(PURPLE), arr.animate.set_color(PURPLE),
                  ws.animate.set_stroke(width=8), run_time=0.8)
        self.at("from the chaos")
        self.play(FadeIn(q3, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ======================================================================================================
PY = 0.7   # pivot height of the balance


def balance(cx, cy, tracker):
    """Schematic balance. tracker.get_value() > 0 tips the LEFT pan down. Returns (static post + dial, redrawn beam)."""
    L = 2.0

    def build():
        a = tracker.get_value()
        le = np.array([cx - L * np.cos(a), cy - L * np.sin(a), 0])
        re = np.array([cx + L * np.cos(a), cy + L * np.sin(a), 0])
        g = VGroup(Line(le, re, color=TEXT, stroke_width=6))
        for e in (le, re):
            pan_c = e + DOWN * 1.0
            g.add(Line(e, pan_c + LEFT * 0.7, color=GREY, stroke_width=3), Line(e, pan_c + RIGHT * 0.7, color=GREY, stroke_width=3),
                  Line(pan_c + LEFT * 0.7, pan_c + RIGHT * 0.7, color=GREY, stroke_width=7))
        tip = np.array([cx - 1.0 * np.sin(a), cy + 1.0 * np.cos(a), 0])
        g.add(Line([cx, cy, 0], tip, color=YELLOW, stroke_width=5), Dot([cx, cy, 0], radius=0.09, color=TEXT))
        return g

    post = VGroup(Line([cx, cy, 0], [cx, cy - 2.2, 0], color=GREY, stroke_width=6),
                  Line([cx - 0.8, cy - 2.2, 0], [cx + 0.8, cy - 2.2, 0], color=GREY, stroke_width=8))
    # the dial the pointer sweeps over: ticks every 0.1 rad from -0.3 to +0.3 at radius 1.1
    for k in range(-3, 4):
        ang = 0.1 * k
        post.add(Line([cx - 1.1 * np.sin(ang), cy + 1.1 * np.cos(ang), 0], [cx - 1.25 * np.sin(ang), cy + 1.25 * np.cos(ang), 0],
                      color=GREY, stroke_width=3))
    return post, always_redraw(build)


class S05Bet(BioScene):
    """The willow experiment is the whole of biochemistry in miniature ... that bet."""

    def construct(self):
        self.add_column()
        icon = willow_icon(CX, -1.0, 1.6, 4)
        self.play(FadeIn(icon, shift=UP * 0.15), run_time=0.4)

        self.at("whole of biochemistry")
        frame = RoundedRectangle(corner_radius=0.25, width=7.8, height=5.4, stroke_color=GOLD, stroke_width=4).move_to([CX, 0.2, 0])
        fl = T("biochemistry", 32, GOLD, font=TITLE_FONT).move_to([CX, 2.35, 0])
        self.play(Create(frame), FadeIn(fl), run_time=1.0)
        self.at("miniature")
        self.play(icon.animate.scale(0.6).move_to([CX, -0.4, 0]), run_time=0.8)

        self.at("a living thing")
        self.play(FadeOut(fl), run_time=0.2)
        gl = T("a living thing grows", 32, GREEN).move_to([CX, 2.2, 0])
        up = Arrow([CX + 1.9, -1.5, 0], [CX + 1.9, 0.9, 0], buff=0, color=GREEN, stroke_width=6, max_tip_length_to_length_ratio=0.2)
        self.play(icon.animate.scale(1.6).move_to([CX - 0.4, -0.7, 0]), GrowArrow(up), FadeIn(gl, shift=DOWN * 0.1), run_time=1.1)

        # --- the balance
        self.at("trust")
        self.play(FadeOut(VGroup(frame, icon, gl, up)), run_time=0.3)
        tilt = ValueTracker(0.0)
        post, beam = balance(CX, PY, tilt)
        self.add(post, beam)
        self.play(FadeIn(post), run_time=0.5)
        bl = T("the balance", 32, GOLD, font=TITLE_FONT).move_to([CX, -2.65, 0])
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=0.3)
        self.at("not the story")
        st = chip_at("the story", GREY, 5.1, 1.9, 28)
        stx = Line(st.get_left() + LEFT * 0.1, st.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        self.play(FadeIn(st, shift=LEFT * 0.2), run_time=0.3)
        self.play(Create(stx), run_time=0.3)

        # --- if the invisible leaves a mark you can measure, it is real
        self.at("if the invisible")
        lx = CX - 2.0
        gh = always_redraw(lambda: ghost_circle(
            [CX - 2.0 * np.cos(tilt.get_value()), PY - 2.0 * np.sin(tilt.get_value()) - 1.0 + 0.48, 0], 0.4))
        gtxt = T("the invisible", 26, PURPLE).move_to([lx - 0.2, -1.75, 0])
        self.add(gh)
        self.play(FadeIn(gtxt, shift=UP * 0.1), run_time=0.5)
        self.at("leaves a mark")
        a_end = 0.17
        mk = Line([CX - 1.1 * np.sin(a_end), PY + 1.1 * np.cos(a_end), 0], [CX - 1.45 * np.sin(a_end), PY + 1.45 * np.cos(a_end), 0],
                  color=GOLD, stroke_width=9)
        mtxt = T("a mark", 28, GOLD).move_to([CX - 1.75 * np.sin(a_end) - 0.5, PY + 1.95, 0])
        self.play(tilt.animate.set_value(a_end), run_time=0.6)
        self.play(Create(mk), FadeIn(mtxt, shift=DOWN * 0.1), run_time=0.2)
        self.at("you can measure")
        self.play(Indicate(mk, color=GOLD, scale_factor=1.8), run_time=0.7)
        self.at("it is real")
        real = T("it is real", 28, GOLD).move_to([lx - 0.2, -1.75, 0])
        self.play(FadeOut(gtxt), run_time=0.2)
        self.play(FadeIn(real, shift=UP * 0.1), run_time=0.4)

        # --- the chapter rests on the bet
        self.at("The chapter")
        self.play(FadeOut(VGroup(post, beam, gh, real, mk, mtxt, bl, st, stx)), run_time=0.3)
        self.remove(post, beam, gh)
        chap = chip_at("the chapter you are starting", TEAL, CX, 2.0, 30)
        self.play(FadeIn(chap, shift=DOWN * 0.15), run_time=0.5)
        self.at("rests on")
        slab = Rectangle(width=5.4, height=0.8, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.2).move_to([CX, -0.6, 0])
        legs = VGroup(Line([CX - 2.2, -1.0, 0], [CX - 2.2, -2.3, 0], color=GREY, stroke_width=6),
                      Line([CX + 2.2, -1.0, 0], [CX + 2.2, -2.3, 0], color=GREY, stroke_width=6))
        self.play(GrowFromEdge(slab, DOWN), Create(legs), chap.animate.move_to([CX, 0.25, 0]), run_time=0.8)
        self.at("that bet")
        bet = T("that bet", 36, GOLD, font=TITLE_FONT).move_to(slab)
        self.play(FadeIn(bet), Indicate(slab, color=GOLD, scale_factor=1.04), run_time=0.7)
        self.finish()


# ======================================================================================================
class S06Quote(BioScene):
    def construct(self):
        self.add_column()
        lines = [T("For want of a name, I have called", 36, TEXT, font=TITLE_FONT),
                 T("that vapour Gas, being not far severed", 36, TEXT, font=TITLE_FONT),
                 T("from the chaos of the ancients.", 36, TEXT, font=TITLE_FONT)]
        qg = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        fit(qg, max_w=8.0)
        qg.move_to([CX + 0.1, 0.5, 0])
        mark = T("“", 120, GOLD, font=TITLE_FONT).scale(0.7).next_to(lines[0], LEFT, buff=0.12).align_to(lines[0], UP).shift(UP * 0.12)
        endq = T("”", 80, GOLD, font=TITLE_FONT).scale(0.7).next_to(lines[2], RIGHT, buff=0.1).shift(UP * 0.1)
        att = T("Jan Baptist van Helmont", 30, GOLD).next_to(qg, DOWN, buff=0.7).align_to(qg, RIGHT)
        self.play(FadeIn(mark, shift=DOWN * 0.1), run_time=0.5)
        for ln in lines:
            self.play(FadeIn(ln, shift=UP * 0.1), run_time=1.0)
            self.wait(0.4)
        self.play(FadeIn(endq), FadeIn(att, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(BioScene):
    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.0))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.0 - 1.15 - 0.3, 0])
        l1 = T("Proved living growth runs on measurable inputs;", 38, font=TITLE_FONT)
        l2 = T("named a vapor Gas.", 38, font=TITLE_FONT)
        lg = VGroup(l1, l2).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · van Helmont profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
