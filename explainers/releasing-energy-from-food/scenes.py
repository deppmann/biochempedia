"""Releasing energy from food: cells release the energy stored in sugar  (Biochemistrypedia explainer, grade 7)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = sugar (glucose) and the energy stored in it
  BLUE   = oxygen
  PURPLE = carbon dioxide
  TEAL   = water
  GOLD   = released energy used for cell work
  ORANGE = thermal energy / warmth (thermometer liquid, moving particles)
  GREEN  = living cells, mitochondria, "alive", cellular respiration
  RED    = dead / boiled (no respiration)
  GREY   = outlines (thermos, cells), breathing, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TEAL_W = "#4FC3C9"   # water

SUGAR, OXY, CO2, WATER, WORK, HEAT, LIVE, DEAD = YELLOW, BLUE, PURPLE, TEAL_W, GOLD, ORANGE, GREEN, RED


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def two(a, b, size, color, weight=NORMAL, gap=0.12):
    """two centred lines of text (Text with a newline left-aligns)."""
    return VGroup(T(a, size, color, weight=weight), T(b, size, color, weight=weight)).arrange(DOWN, buff=gap)


def bchip2(a, b, color, size=26):
    t = two(a, b, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.44, height=t.height + 0.44, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height, stroke_width=0,
                            fill_color=BG, fill_opacity=1)
    return VGroup(back, box, t)


# ---------------------------------------------------------------------------------------------
# the two thermos rigs (scenes 1 and 6 build them in the same place)
# ---------------------------------------------------------------------------------------------
XL, XR = -4.4, 4.4          # thermos centres
TL, TR = -2.2, 2.2          # thermometer centres
BASE, ROOM = -1.8, -0.3     # bottom of tube, room-temperature level
WARM = 0.9                  # the warmer reading in the sprouting-pea thermos (a sketch, no scale)


def thermos_body(x):
    body = RoundedRectangle(corner_radius=0.25, width=2.6, height=3.9, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.08).move_to([x, 0, 0])
    neck = RoundedRectangle(corner_radius=0.08, width=1.3, height=0.35, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.3).move_to([x, 2.12, 0])
    return VGroup(body, neck)


def peas(x, color, fill=0.85):
    ps = VGroup()
    for r, y in enumerate([-1.65, -1.25, -0.85, -0.45]):
        n = 5 if r % 2 == 0 else 4
        for c in range(n):
            px = x + (c - (n - 1) / 2) * 0.44
            ps.add(Circle(radius=0.17, stroke_color=color, stroke_width=2, fill_color=color,
                          fill_opacity=fill).move_to([px, y, 0]))
    return ps


def thermometer(x, level):
    tube = RoundedRectangle(corner_radius=0.12, width=0.3, height=3.6, stroke_color=GREY, stroke_width=3).move_to([x, 0, 0])
    bulb = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=HEAT, fill_opacity=0.9).move_to([x, BASE - 0.05, 0])
    fluid = always_redraw(lambda: Rectangle(width=0.14, height=max(0.02, level.get_value() - BASE),
                                            stroke_width=0, fill_color=HEAT, fill_opacity=0.95)
                          .move_to([x, (BASE + level.get_value()) / 2, 0]))
    return VGroup(tube, bulb), fluid


def room_line():
    ln = DashedLine([TL + 0.25, ROOM, 0], [TR - 0.25, ROOM, 0], color=GREY, stroke_width=3, dash_length=0.16)
    lb = T("room temperature", 24, GREY).move_to([0, ROOM - 0.4, 0])
    return VGroup(ln, lb)


class S00Title(TitleCard):
    LESSON = "Releasing energy from food"
    TITLE = "Cells release energy stored in sugar"


# ---------------------------------------------------------------------------------------------
class S01Peas(SpokenScene):
    """sprouting vs boiled peas in thermoses; the sprouting thermometer rises; where does the warmth come from?"""

    def construct(self):
        L, R = ValueTracker(ROOM + 0.04), ValueTracker(ROOM + 0.04)
        bodyL, bodyR = thermos_body(XL), thermos_body(XR)
        pL, pR = peas(XL, LIVE), peas(XR, GREY, 0.55)
        thL, flL = thermometer(TL, L)
        thR, flR = thermometer(TR, R)
        labL = T("sprouting peas", 30, LIVE, weight=BOLD).move_to([XL, 2.95, 0])
        labR = T("boiled peas", 30, GREY, weight=BOLD).move_to([XR, 2.95, 0])
        room = room_line()

        self.at("sprouting peas")
        self.play(FadeIn(bodyL), FadeIn(labL), run_time=0.5)
        self.play(FadeIn(pL, shift=DOWN * 0.6, lag_ratio=0.03), run_time=0.9)
        self.play(FadeIn(thL), FadeIn(flL), FadeIn(room), run_time=0.7)

        self.at("climb above")
        self.play(L.animate.set_value(WARM), run_time=2.2, rate_func=smooth)

        self.at("boiled peas")
        self.play(FadeIn(bodyR), FadeIn(labR), run_time=0.5)
        self.play(FadeIn(pR, shift=DOWN * 0.6, lag_ratio=0.03), FadeIn(thR), FadeIn(flR), run_time=0.9)

        self.at("peas have no muscles")
        q = T("Where does the warmth come from?", 40, TEXT, weight=BOLD).move_to([0, -3.0, 0])
        self.at("where does the warmth")
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.play(Indicate(thL[1], color=HEAT, scale_factor=1.25), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fuel(SpokenScene):
    """a seed holds stored energy in sugar; glucose; photosynthesis makes it; cells break it down."""

    def construct(self):
        seed = RoundedRectangle(corner_radius=0.9, width=4.6, height=3.7, stroke_color=LIVE, stroke_width=5,
                                fill_color=LIVE, fill_opacity=0.12).move_to([-3.4, 0.3, 0])
        seed_lbl = T("pea seed", 32, LIVE, weight=BOLD).move_to([-3.4, 2.65, 0])
        dots = VGroup(*[Circle(radius=0.15, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.85)
                        .move_to([-3.4 + (c - 1.5) * 0.8, 0.3 + (r - 1) * 0.8, 0]) for r in range(3) for c in range(4)])
        self.at("pea seed")
        self.play(FadeIn(seed), FadeIn(seed_lbl), run_time=0.7)

        self.at("stores energy")
        self.play(FadeIn(dots, scale=0.6, lag_ratio=0.05), run_time=0.9)
        stored = T("stored energy", 28, TEXT).move_to([-3.4, -2.1, 0])
        self.play(FadeIn(stored), Indicate(dots, color=WORK, scale_factor=1.15), run_time=0.9)

        self.at("glucose")
        gl = bchip("glucose", SUGAR, 32).move_to([3.2, 1.2, 0])
        sub = T("the main fuel: a sugar", 24, SUGAR).next_to(gl, DOWN, buff=0.18)
        self.play(FadeIn(gl, shift=LEFT * 0.3), run_time=0.7)
        self.play(FadeIn(sub), run_time=0.4)

        self.at("photosynthesis")
        ph = bchip("photosynthesis", LIVE, 28).move_to([3.2, 2.85, 0])
        a2 = arr(ph.get_bottom(), gl.get_top(), LIVE)
        self.play(FadeIn(ph, shift=DOWN * 0.3), run_time=0.5)
        self.play(Create(a2), run_time=0.5)

        self.at("break food down")
        cell = bchip("cell breaks it down", GREY, 26).move_to([3.2, -0.65, 0])
        a3 = arr(sub.get_bottom() + DOWN * 0.02, cell.get_top(), SUGAR)
        self.play(FadeIn(cell, shift=UP * 0.2), Create(a3), run_time=0.7)

        self.at("use its energy")
        en = bchip("energy to use", WORK, 28).move_to([3.2, -2.35, 0])
        a4 = arr(cell.get_bottom(), en.get_top(), WORK)
        self.play(Create(a4), FadeIn(en, shift=UP * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Respire(SpokenScene):
    """sugar + oxygen -> [cellular respiration] -> carbon dioxide + water + released energy."""

    def construct(self):
        box = RoundedRectangle(corner_radius=0.3, width=3.2, height=3.6, stroke_color=LIVE, stroke_width=5,
                               fill_color=LIVE, fill_opacity=0.12).move_to([-0.3, 0, 0])
        bl = two("cellular", "respiration", 32, LIVE, BOLD).move_to(box)
        self.at("cellular respiration")
        self.play(FadeIn(box, scale=0.9), Write(bl), run_time=1.0)

        self.at("break down sugar")
        sg = bchip("sugar (glucose)", SUGAR, 26).move_to([-4.6, 1.2, 0])
        self.play(FadeIn(sg, shift=RIGHT * 0.3), run_time=0.5)
        self.at("with oxygen")
        ox = bchip("oxygen", OXY, 28).move_to([-4.6, -1.2, 0])
        self.play(FadeIn(ox, shift=RIGHT * 0.3), run_time=0.5)

        self.at("go in")
        a_in1 = arr(sg.get_right(), [-1.9, 0.7, 0], SUGAR)
        a_in2 = arr(ox.get_right(), [-1.9, -0.7, 0], OXY)
        d1 = Dot(sg.get_right(), radius=0.14, color=SUGAR)
        d2 = Dot(ox.get_right(), radius=0.14, color=OXY)
        self.play(Create(a_in1), Create(a_in2), run_time=0.3)
        self.play(d1.animate.move_to([-0.9, 0.6, 0]).set_opacity(0), d2.animate.move_to([-0.9, -0.6, 0]).set_opacity(0),
                  Indicate(box, color=LIVE, scale_factor=1.04), run_time=0.7)

        self.at("carbon dioxide and water")
        co = bchip("carbon dioxide", CO2, 28).move_to([4.7, 1.7, 0])
        wa = bchip("water", WATER, 28).move_to([4.7, 0.1, 0])
        a_o1 = arr([1.3, 0.8, 0], co.get_left(), CO2)
        a_o2 = arr([1.3, 0.1, 0], wa.get_left(), WATER)
        self.play(Create(a_o1), Create(a_o2), run_time=0.4)
        self.play(FadeIn(co, shift=RIGHT * 0.4), FadeIn(wa, shift=RIGHT * 0.4), run_time=0.7)

        self.at("released energy")
        en = bchip("released energy", WORK, 26).move_to([4.7, -1.6, 0])
        a_o3 = arr([1.3, -0.7, 0], en.get_left(), WORK)
        self.play(Create(a_o3), FadeIn(en, shift=RIGHT * 0.4), run_time=0.7)

        self.at("oxygen is a gas")
        og = T("a gas in the air", 24, OXY).next_to(ox, DOWN, buff=0.2)
        self.play(Indicate(ox, color=OXY, scale_factor=1.15), FadeIn(og), run_time=0.8)
        self.at("carbon dioxide is a gas")
        cg = T("a gas given off", 24, CO2).next_to(co, DOWN, buff=0.2)
        self.play(Indicate(co, color=CO2, scale_factor=1.15), FadeIn(cg), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mito(pos, angle=0.0, scale=1.0):
    o = Ellipse(width=0.95 * scale, height=0.5 * scale, stroke_color=LIVE, stroke_width=3,
                fill_color=LIVE, fill_opacity=0.55).move_to(pos)
    return o.rotate(angle)


class S04Mito(SpokenScene):
    """mitochondria inside an animal cell, then a plant cell: both have them."""

    def construct(self):
        line1 = T("mitochondria", 42, LIVE, weight=BOLD).move_to([0, 3.15, 0])
        cy = -0.75
        acell = Ellipse(width=5.4, height=3.6, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                        fill_opacity=0.08).move_to([-3.3, cy, 0])
        pcell = RoundedRectangle(corner_radius=0.15, width=5.0, height=3.6, stroke_color=GREY, stroke_width=7,
                                 fill_color=GREY, fill_opacity=0.08).move_to([3.3, cy, 0])
        am = VGroup(mito([-4.2, cy + 0.5, 0], 0.4), mito([-2.4, cy + 0.2, 0], -0.5), mito([-3.5, cy - 0.8, 0], 0.15))
        pm = VGroup(mito([2.4, cy + 0.6, 0], -0.3), mito([4.2, cy - 0.1, 0], 0.5), mito([3.0, cy - 0.9, 0], 0.1))
        alab = T("animal cell", 28, TEXT).move_to([-3.3, cy + 2.2, 0])
        plab = T("plant cell", 28, TEXT).move_to([3.3, cy + 2.2, 0])

        ag = VGroup(acell, am)
        ag.shift(RIGHT * 3.3)
        alab.shift(RIGHT * 3.3)
        self.at("most of this")
        self.play(FadeIn(acell), run_time=0.6)
        self.at("small parts")
        self.play(FadeIn(am, scale=0.5, lag_ratio=0.25), run_time=1.0)
        self.at("called mitochondria")
        self.play(Write(line1), run_time=1.0)

        self.at("one is a mitochondrion")
        one = T("one is a mitochondrion", 42, LIVE, weight=BOLD).move_to(line1)
        self.play(Transform(line1, one), Indicate(am[1], color=YELLOW, scale_factor=1.5), run_time=1.0)

        self.at("organelle")
        line2 = T("an organelle where cells release energy from food", 26, TEXT).move_to([0, 2.4, 0])
        self.play(FadeIn(line2, shift=UP * 0.15), run_time=0.6)

        self.at("plant cells and")
        self.play(ag.animate.shift(LEFT * 3.3), alab.animate.shift(LEFT * 3.3), run_time=0.6)
        self.play(FadeIn(pcell), FadeIn(pm, scale=0.5, lag_ratio=0.25), FadeIn(plab), FadeIn(alab), run_time=0.8)

        self.at("almost all")
        al = T("almost all plant, animal and fungus cells", 28, LIVE).move_to([0, -3.25, 0])
        self.play(FadeIn(al, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Energy(SpokenScene):
    """energy stored in sugar -> cell work + thermal energy (moving particles = warmth)."""

    def construct(self):
        src = bchip2("energy stored", "in sugar", SUGAR, 28).move_to([-4.2, 0.9, 0])
        self.play(FadeIn(src), run_time=0.5)

        self.at("released energy")
        self.play(Indicate(src, color=WORK, scale_factor=1.1), run_time=0.8)
        self.at("on work")
        work = bchip("cell work", WORK, 30).move_to([2.7, 2.4, 0])
        a_w = arr([-2.8, 1.3, 0], work.get_left(), WORK)
        self.play(Create(a_w), FadeIn(work, shift=RIGHT * 0.3), run_time=0.8)
        self.at("building new cell parts")
        bn = T("building new cell parts", 26, WORK).next_to(work, DOWN, buff=0.2)
        self.play(FadeIn(bn, shift=UP * 0.1), run_time=0.6)

        self.at("some energy always leaves")
        heat = bchip("thermal energy", HEAT, 30).move_to([2.7, -0.2, 0])
        a_h = arr([-2.8, 0.5, 0], heat.get_left(), HEAT)
        self.play(Create(a_h), FadeIn(heat, shift=RIGHT * 0.3), run_time=0.8)

        self.at("moving particles")
        box = RoundedRectangle(corner_radius=0.2, width=3.6, height=1.15, stroke_color=HEAT, stroke_width=3,
                               fill_color=HEAT, fill_opacity=0.08).move_to([2.7, -1.55, 0])
        bases = [np.array([2.7 + (c - 2.5) * 0.52, -1.55 + (r - 0.5) * 0.45, 0]) for r in range(2) for c in range(6)]
        dots = VGroup(*[Dot(b, radius=0.09, color=HEAT) for b in bases])
        clock = [0.0]

        def jig(m, dt):
            clock[0] += dt
            t = clock[0]
            for i, (d, b) in enumerate(zip(dots, bases)):
                d.move_to(b + 0.13 * np.array([np.sin(6 * t + 1.7 * i), np.cos(7.3 * t + 2.3 * i), 0]))
        dots.add_updater(jig)
        self.play(FadeIn(box), FadeIn(dots), run_time=0.6)

        self.at("feel as warmth")
        wm = T("you feel it as warmth", 26, HEAT).move_to([2.7, -2.5, 0])
        self.play(FadeIn(wm, shift=UP * 0.1), run_time=0.6)

        self.at("already stored in the sugar")
        self.play(Indicate(src, color=SUGAR, scale_factor=1.12), run_time=0.8)
        self.at("changes its form")
        ban = T("the energy changes form", 34, TEXT, weight=BOLD).move_to([-3.6, -2.9, 0])
        self.play(FadeIn(ban, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """thermoses explained; plants, fungi and animals all respire; breathing vs respiration; the answer."""

    def construct(self):
        L, R = ValueTracker(WARM), ValueTracker(ROOM + 0.04)
        bodyL, bodyR = thermos_body(XL), thermos_body(XR)
        pL, pR = peas(XL, LIVE), peas(XR, GREY, 0.55)
        thL, flL = thermometer(TL, L)
        thR, flR = thermometer(TR, R)
        labL = T("sprouting peas", 30, LIVE, weight=BOLD).move_to([XL, 2.95, 0])
        labR = T("boiled peas", 30, GREY, weight=BOLD).move_to([XR, 2.95, 0])
        room = room_line()
        rig = VGroup(bodyL, bodyR, pL, pR, thL, thR, labL, labR, room)

        self.at("the two thermoses")
        self.play(FadeIn(rig), FadeIn(flL), FadeIn(flR), run_time=0.9)

        self.at("peas are alive")
        al = T("alive: cells respire", 26, LIVE, weight=BOLD).move_to([XL, -2.65, 0])
        self.play(FadeIn(al, shift=UP * 0.1), Indicate(pL, color=LIVE, scale_factor=1.06), run_time=0.8)

        self.at("thermal energy")
        ups = VGroup(*[arr([XL + dx, -0.15, 0], [XL + dx, 0.85, 0], HEAT, w=6, tip=0.18) for dx in (-0.7, 0, 0.7)])
        self.play(LaggedStart(*[GrowArrow(u) for u in ups], lag_ratio=0.25), run_time=1.0)
        tl = two("thermal energy", "from the peas", 22, HEAT).move_to([XL, 1.45, 0])
        self.play(FadeIn(tl), run_time=0.4)
        self.at("holds it in")
        self.play(bodyL[0].animate.set_stroke(HEAT, width=7), run_time=0.7)

        self.at("peas are dead")
        de = T("dead: no respiration", 26, DEAD, weight=BOLD).move_to([XR, -2.65, 0])
        self.play(FadeIn(de, shift=UP * 0.1), run_time=0.7)

        self.at("plants fungi and animals")
        self.play(FadeOut(rig), FadeOut(flL), FadeOut(flR), FadeOut(ups), FadeOut(tl), FadeOut(al), FadeOut(de), run_time=0.7)
        cs = VGroup(*[bchip(n, LIVE, 36) for n in ("plants", "fungi", "animals")]).arrange(RIGHT, buff=0.6).move_to([0, 0.8, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cs], lag_ratio=0.35), run_time=1.0)
        self.at("all respire")
        rs = T("all respire", 42, LIVE, weight=BOLD).move_to([0, -1.0, 0])
        self.play(FadeIn(rs, shift=UP * 0.15), run_time=0.6)

        self.at("breathing is moving")
        self.play(FadeOut(cs), FadeOut(rs), run_time=0.5)
        bk = RoundedRectangle(corner_radius=0.25, width=5.4, height=2.6, stroke_color=GREY, stroke_width=4,
                              fill_color=GREY, fill_opacity=0.1).move_to([-3.3, 0.2, 0])
        bt = T("breathing", 38, TEXT, weight=BOLD).move_to([-3.3, 0.85, 0])
        bs = two("air in and out", "of your lungs", 28, TEXT).move_to([-3.3, -0.3, 0])
        self.play(FadeIn(bk), FadeIn(bt), FadeIn(bs), run_time=0.8)
        ne = T("not the same thing", 28, GREY).move_to([0, -2.1, 0])
        self.at("not the same")
        self.play(FadeIn(ne), run_time=0.5)
        self.at("respiration happens")
        rk = RoundedRectangle(corner_radius=0.25, width=5.4, height=2.6, stroke_color=LIVE, stroke_width=4,
                              fill_color=LIVE, fill_opacity=0.12).move_to([3.3, 0.2, 0])
        rt = T("cellular respiration", 34, LIVE, weight=BOLD).move_to([3.3, 0.85, 0])
        rsub = T("inside cells", 30, TEXT).move_to([3.3, -0.3, 0])
        self.play(FadeIn(rk), FadeIn(rt), FadeIn(rsub), run_time=0.8)

        self.at("your cells use oxygen")
        self.play(*[FadeOut(m) for m in (bk, bt, bs, rk, rt, rsub, ne)], run_time=0.6)
        fin = VGroup(T("Your cells use oxygen to release", 42, TEXT, weight=BOLD),
                     T("the energy stored in sugar.", 42, SUGAR, weight=BOLD)).arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        self.play(FadeIn(fin, shift=UP * 0.2), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Cells release energy stored in sugar, using oxygen."
