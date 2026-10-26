"""What do plants need? How to run a fair test with your child  (Biology Together, Unit 3)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Everything is drawn as simple schematic shapes: cups, a sprout, a sun, a drop, a cupboard.

COLOR MAP (one color per concept, whole video)
  YELLOW = light (the sun)
  BLUE   = water (the drop)
  GREEN  = a green, healthy seedling
  PALE   = a pale seedling (the one grown in the dark)
  SOIL   = the soil in the cups
  GREY   = cups, cupboard, windowsill, outlines, de-emphasized labels
  ORANGE = a guess, a prediction, a question
  GOLD   = the one thing that is different / the thing we are looking at
  TEAL   = what stays the same
  PINK   = food stored in the seed
  RED    = a surprise (the "!" in the last list)
  TEXT   = plain labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PALE = "#CDD6A0"
SOIL = "#8B6B4B"
ORANGE = "#F29E4C"
PINK = "#E49BC1"

# sprout states: stem height h, stem width w, leaf length lw, colour, droop 0..1
ST = {
    "start": dict(h=0.8, w=7, lw=0.5, col=GREEN, droop=0.0),
    "sturdy": dict(h=1.0, w=10, lw=0.62, col=GREEN, droop=0.0),
    "tall": dict(h=2.3, w=7, lw=0.5, col=GREEN, droop=0.0),
    "tallthin": dict(h=2.3, w=3.5, lw=0.34, col=GREEN, droop=0.0),
    "tallpale": dict(h=2.3, w=3.5, lw=0.34, col=PALE, droop=0.0),
    "droop": dict(h=0.8, w=7, lw=0.5, col=GREEN, droop=1.0),
    "flop": dict(h=2.3, w=3.5, lw=0.34, col=PALE, droop=0.45),
}
RIM = -0.8                      # soil line of the full-size cups
K = 1.2                         # scale of the full-size cups
SPREAD = [-4.65, -1.55, 1.55, 4.65]
FINAL = [-5.0, -2.2, 2.2, 5.0]
LABELS = ["light + water", "light, no water", "dark + water", "dark, no water"]


# ---------------------------------------------------------------------------------------------
# helpers (all shapes are local to a cup whose soil line is at the origin, then scaled and placed)
# ---------------------------------------------------------------------------------------------
def place(m, x, rim, k):
    return m.scale(k, about_point=ORIGIN).shift([x, rim, 0])


def sprout_local(h, w, col, droop, lw):
    top = np.array([0.55 * h * droop, h * (1 - 0.45 * droop), 0.0])
    stem = CubicBezier(ORIGIN, np.array([0, 0.55 * h, 0.0]), np.array([0.3 * h * droop, h, 0.0]), top,
                       stroke_color=col, stroke_width=w)
    a = np.radians(25 - 80 * droop)
    leaves = []
    for ang in (np.pi - a, a):
        d = np.array([np.cos(ang), np.sin(ang), 0.0])
        e = Ellipse(width=lw, height=lw * 0.5, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.92)
        e.rotate(ang).move_to(top + d * lw * 0.5)
        leaves.append(e)
    return VGroup(stem, *leaves)


def cup_local():
    return Polygon([-0.85, 0, 0], [0.85, 0, 0], [0.65, -1.5, 0], [-0.65, -1.5, 0], stroke_color=GREY,
                   stroke_width=3.5, fill_color=SOIL, fill_opacity=0.55)


def drop_shape(cx, cy, s=1.0):
    c = Circle(radius=0.16 * s, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to([cx, cy, 0])
    t = Polygon([cx - 0.145 * s, cy + 0.06 * s, 0], [cx + 0.145 * s, cy + 0.06 * s, 0], [cx, cy + 0.42 * s, 0],
                stroke_width=0, fill_color=BLUE, fill_opacity=1)
    return VGroup(c, t)


class Unit:
    """One cup with its sprout and (optionally) its water drop."""

    def __init__(self, x, rim=RIM, k=K, st="start", water=True):
        self.x, self.rim, self.k, self.st = x, rim, k, st
        self.cup = place(cup_local(), x, rim, k).set_z_index(2)
        self.sprout = place(sprout_local(**ST[st]), x, rim, k).set_z_index(1)
        self.drop = place(drop_shape(0, -0.75), x, rim, k).set_z_index(3) if water else None

    def parts(self):
        return [m for m in (self.sprout, self.cup, self.drop) if m is not None]

    def go(self, st):
        tgt = place(sprout_local(**ST[st]), self.x, self.rim, self.k)
        self.st = st
        return Transform(self.sprout, tgt)

    def move(self, x, rim=None):
        rim = self.rim if rim is None else rim
        dx, dy = x - self.x, rim - self.rim
        self.x, self.rim = x, rim
        return [m.animate.shift([dx, dy, 0]) for m in self.parts()]

    def label(self, text, size=22):
        return T(text, size, TEXT).move_to([self.x, self.rim - 1.5 * self.k - 0.42, 0])

    def ring(self, color=GOLD):
        return RoundedRectangle(corner_radius=0.18, width=1.9 * self.k, height=1.5 * self.k + 0.2, stroke_color=color,
                                stroke_width=5).move_to([self.x, self.rim - 0.75 * self.k - 0.0, 0])


def sun(x, y, r=0.38):
    body = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95)
    rays = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * r * 1.4, np.array([np.cos(a), np.sin(a), 0]) * r * 1.95,
                         color=YELLOW, stroke_width=5) for a in np.linspace(0, TAU, 8, endpoint=False)])
    return VGroup(body, rays).move_to([x, y, 0])


def sill(x0, x1, y=-2.7):
    return Rectangle(width=x1 - x0, height=0.16, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                     fill_opacity=0.5).move_to([(x0 + x1) / 2, y, 0]).set_z_index(-1)


def cupboard_box(x0, x1, top=2.4, bot=-2.68):
    return RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=top - bot, stroke_color=GREY, stroke_width=4,
                            fill_color="#05060a", fill_opacity=0.9).move_to([(x0 + x1) / 2, (top + bot) / 2, 0]).set_z_index(-2)


def banner(text, color, y=3.2, x=3.5, size=28):
    return T(text, size, color, weight=BOLD).move_to([x, y, 0])


def four_cups(states=("start",) * 4, water=(True,) * 4, xs=SPREAD):
    return [Unit(x, st=s, water=w) for x, s, w in zip(xs, states, water)]


def bchip(text, color, size=28):
    """chip with an opaque backing so a line drawn behind it does not show through."""
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def sheet(x, y, c=ORANGE):
    r = RoundedRectangle(corner_radius=0.08, width=0.85, height=1.05, stroke_color=c, stroke_width=3,
                         fill_color=c, fill_opacity=0.18)
    lines = VGroup(*[Line([-0.26, dy, 0], [0.26, dy, 0], color=c, stroke_width=3) for dy in (0.25, 0.0, -0.25)])
    return VGroup(r, lines).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "What do plants need?"
    TITLE = "Run a fair test with your child"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """A question you can see (sun ? cup, water), then two identical cups where one thing changes, then four cups."""

    def construct(self):
        u = Unit(0, rim=-0.45, k=1.7, st="start", water=False)
        self.at("Does a plant")
        self.play(FadeIn(u.cup), FadeIn(u.sprout), run_time=0.6)
        s = sun(3.9, 1.75, 0.5)
        dash = DashedLine([3.0, 1.15, 0], [0.8, 0.5, 0], color=GREY, stroke_width=5)
        q = bchip("?", ORANGE, size=44).move_to([1.95, 0.83, 0])
        self.at("sunlight")
        self.play(FadeIn(s, scale=0.8), Create(dash), FadeIn(q, scale=0.7), run_time=0.8)
        d = drop_shape(-3.7, 0.35, 2.2)
        arrow = Arrow([-3.0, 0.1, 0], [-1.6, -0.6, 0], buff=0, color=BLUE, stroke_width=6, tip_length=0.28)
        self.at("already has water")
        self.play(FadeIn(d, shift=DOWN * 0.3), GrowArrow(arrow), run_time=0.8)
        guess = chip("my guess", ORANGE, size=32).move_to([0, 2.6, 0])
        self.at("for a guess")
        self.play(FadeIn(guess, shift=DOWN * 0.2), run_time=0.5)

        # --- a fair test: two identical cups, one thing changes ----------------------------
        self.at("fair test")
        self.play(*[FadeOut(m) for m in (u.cup, u.sprout, s, dash, q, d, arrow, guess)], run_time=0.5)
        a = Unit(-3.0, rim=-0.9, k=1.2)
        b = Unit(3.0, rim=-0.9, k=1.2)
        sa, sb = sun(-3.0, 2.2, 0.42), sun(3.0, 2.2, 0.42)
        self.play(*[FadeIn(m) for m in a.parts() + b.parts()], FadeIn(sa), FadeIn(sb), run_time=0.7)
        self.at("only one thing changes")
        ring = Circle(radius=0.9, stroke_color=GOLD, stroke_width=6).move_to(sb)
        self.play(Create(ring), sb.animate.set_opacity(0.18), run_time=0.8)
        same = DoubleArrow([-1.7, -1.9, 0], [1.7, -1.9, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.22)
        same_t = T("everything else the same", 26, TEAL).move_to([0, -3.15, 0])
        self.at("everything else stays the same")
        self.play(GrowArrow(same), FadeIn(same_t), run_time=0.7)

        # --- four cups on a windowsill ------------------------------------------------------
        self.at("Four cups")
        us = four_cups()
        s4 = sun(0, 2.7, 0.38)
        sl = sill(-6.2, 6.2)
        old = [*a.parts(), *b.parts(), sa, sb, ring, same, same_t]
        self.play(*[FadeOut(m) for m in old], run_time=0.4)
        self.play(LaggedStart(*[FadeIn(m) for u_ in us for m in u_.parts()], lag_ratio=0.05), FadeIn(s4), FadeIn(sl),
                  run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Predict(SpokenScene):
    """Grow all four the same way, then predict before anything changes."""

    def construct(self):
        us = four_cups()
        s4 = sun(0, 2.7, 0.38)
        sl = sill(-6.2, 6.2)
        self.add(sl, s4, *[m for u in us for m in u.parts()])
        chips = VGroup(*[chip(t, TEAL, size=26) for t in ("same soil", "same cups", "same seeds", "same water")])
        chips.arrange(RIGHT, buff=0.35).move_to([0, 1.3, 0])
        sill_t = T("windowsill", 24, GREY).move_to([0, -3.1, 0])

        self.at("all four cups")
        self.play(LaggedStart(*[ApplyMethod(VGroup(*u.parts()).shift, UP * 0.15, rate_func=there_and_back) for u in us], lag_ratio=0.25), run_time=1.0)
        self.at("Same soil")
        self.play(FadeIn(chips[0], shift=DOWN * 0.15), Indicate(VGroup(*[u.cup for u in us]), color=SOIL, scale_factor=1.05),
                  run_time=0.7)
        self.at("same cups")
        self.play(FadeIn(chips[1], shift=DOWN * 0.15), run_time=0.5)
        self.at("same seeds")
        self.play(FadeIn(chips[2], shift=DOWN * 0.15), Indicate(VGroup(*[u.sprout for u in us]), color=GREEN, scale_factor=1.1),
                  run_time=0.7)
        self.at("same amount of water")
        self.play(FadeIn(chips[3], shift=DOWN * 0.15), *[Indicate(u.drop, color=BLUE, scale_factor=1.3) for u in us],
                  run_time=0.7)
        self.at("sunny window")
        self.play(Indicate(s4, color=YELLOW, scale_factor=1.2), FadeIn(sill_t), run_time=0.7)
        hh = ST["start"]["h"] * K
        br = VGroup(Line([-3.3, RIM, 0], [-3.3, RIM + hh, 0], color=GOLD, stroke_width=4),
                    Line([-3.42, RIM, 0], [-3.18, RIM, 0], color=GOLD, stroke_width=4),
                    Line([-3.42, RIM + hh, 0], [-3.18, RIM + hh, 0], color=GOLD, stroke_width=4))
        br_t = M("2 cm", 22, GOLD).move_to([-2.8, RIM + hh / 2, 0])
        self.at("about two")
        self.play(Create(br), FadeIn(br_t), run_time=0.7)

        # --- predict ---------------------------------------------------------------------------------
        self.at("Before you change anything")
        self.play(FadeOut(chips), FadeOut(br), FadeOut(br_t), FadeOut(sill_t), run_time=0.5)
        qs = VGroup(*[chip("?", ORANGE, size=40).move_to([u.x, 1.3, 0]) for u in us])
        self.at("what will happen")
        self.play(LaggedStart(*[FadeIn(q, scale=0.7) for q in qs], lag_ratio=0.2), run_time=1.0)
        sheets = VGroup(*[sheet(u.x, 1.4) for u in us])
        self.at("Write or draw")
        self.play(*[ReplacementTransform(q, sh) for q, sh in zip(qs, sheets)], run_time=0.8)
        safe = chip("Safety notes: on the page", GREY, size=24).move_to([0, -3.15, 0])
        self.at("safety notes")
        self.play(FadeIn(safe, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Change(SpokenScene):
    """Two cups into the cupboard, two lose their water; compare against the light + water cup."""

    def construct(self):
        us = four_cups()
        s4 = sun(0, 2.7, 0.38)
        sl = sill(-6.2, 6.2)
        sheets = VGroup(*[sheet(u.x, 1.4) for u in us])
        safe = chip("Safety notes: on the page", GREY, size=24).move_to([0, -3.15, 0])
        self.add(sl, s4, *[m for u in us for m in u.parts()], sheets, safe)

        self.at("Now change things")
        self.play(FadeOut(sheets), FadeOut(safe), run_time=0.5)
        box = cupboard_box(0.7, 6.3)
        box_t = T("cupboard", 24, GREY).move_to([3.5, 2.7, 0])
        sl2 = sill(-6.2, -0.9)
        self.at("Move two cups")
        anims = []
        for u, x in zip(us, FINAL):
            anims += u.move(x)
        self.play(*anims, s4.animate.move_to([-3.6, 2.7, 0]), Transform(sl, sl2), FadeIn(box), run_time=1.3)
        labels = [u.label(t) for u, t in zip(us, LABELS)]
        self.at("where it is dark")
        self.play(FadeIn(box_t), *[FadeIn(l) for l in labels], run_time=0.7)
        self.at("keep their water")
        self.play(Indicate(us[0].drop, color=BLUE, scale_factor=1.4), Indicate(us[2].drop, color=BLUE, scale_factor=1.4), run_time=0.8)
        self.at("nothing more")
        self.play(FadeOut(us[1].drop, scale=0.3), FadeOut(us[3].drop, scale=0.3), run_time=0.5)
        b1 = banner("everything else the same", TEAL, y=1.0, x=-3.6)
        self.at("nothing else")
        self.play(FadeIn(b1, shift=DOWN * 0.15), run_time=0.5)

        r1 = us[0].ring()
        r3 = us[2].ring()
        self.at("light and water cup")
        self.play(FadeOut(b1), Create(r1), run_time=0.5)
        b2 = banner("only light is different", GOLD, y=1.0, x=-3.6)
        self.at("dark and water cup")
        self.play(Create(r3), run_time=0.4)
        self.at("only in light")
        self.play(FadeIn(b2, shift=DOWN * 0.15), run_time=0.5)
        r2 = us[1].ring()
        b3 = banner("only water is different", GOLD, y=1.0, x=-3.6)
        self.at("light no water cup")
        self.play(Transform(r3, r2), FadeOut(b2), run_time=0.6)
        self.at("only in water")
        self.play(FadeIn(b3, shift=DOWN * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def final_rig(scene, states):
    """The test as set up at the end of scene 3: windowsill left, cupboard right, four labelled cups."""
    us = [Unit(x, st=s, water=w) for x, s, w in zip(FINAL, states, (True, False, True, False))]
    s4 = sun(-3.6, 2.7, 0.38)
    sl = sill(-6.2, -0.9)
    box = cupboard_box(0.7, 6.3)
    box_t = T("cupboard", 24, GREY).move_to([3.5, 2.7, 0])
    labels = [u.label(t) for u, t in zip(us, LABELS)]
    scene.add(sl, box, box_t, s4, *[m for u in us for m in u.parts()], *labels)
    return us, s4, sl, box, box_t, labels


class S04Look(SpokenScene):
    """Time passes: dry cups droop; the dark watered sprouts stretch, thin and pale; the lit one stays sturdy."""

    def construct(self):
        us, s4, sl, box, box_t, labels = final_rig(self, ("start",) * 4)
        b1 = banner("check every day or two", TEXT)
        self.at("Check every day")
        self.play(FadeIn(b1, shift=DOWN * 0.15), run_time=0.5)
        frame = RoundedRectangle(corner_radius=0.15, width=2.3, height=3.3, stroke_color=TEXT, stroke_width=4).move_to([-5.0, -1.15, 0])
        self.at("draw each cup")
        self.play(Create(frame), run_time=0.3)
        for u in us[1:]:
            self.play(frame.animate.move_to([u.x, -1.15, 0]), run_time=0.45)
        self.play(FadeOut(frame), run_time=0.2)
        b2 = banner("2 to 5 days", TEXT)
        self.at("with no water")
        self.play(ReplacementTransform(b1, b2), run_time=0.4)
        self.at("droop")
        self.play(us[1].go("droop"), us[3].go("droop"), run_time=1.0)
        b3 = banner("about a week", TEXT)
        self.at("Within about a week")
        self.play(ReplacementTransform(b2, b3), run_time=0.4)
        r3 = us[2].ring()
        self.at("watered seedlings in the dark")
        self.play(Create(r3), run_time=0.5)
        self.at("taller")
        self.play(us[2].go("tall"), run_time=0.7)
        self.at("thinner")
        self.play(us[2].go("tallthin"), run_time=0.5)
        self.at("paler")
        self.play(us[2].go("tallpale"), FadeOut(r3), run_time=0.6)
        self.at("stays green and upright")
        self.play(us[0].go("sturdy"), Indicate(us[0].sprout, color=GREEN, scale_factor=1.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Surprise(SpokenScene):
    """The tallest is not the best: look at colour and strength; stored food runs out; the result stands."""

    def construct(self):
        us, s4, sl, box, box_t, labels = final_rig(self, ("sturdy", "droop", "tallpale", "droop"))
        u1, u3 = us[0], us[2]
        self.at("Look again")
        box2 = cupboard_box(-2.7, 0.3)
        box_t2 = T("cupboard", 24, GREY).move_to([-1.2, 2.7, 0])
        sl2 = sill(-6.2, -2.8)
        gone = [m for m in us[1].parts() + us[3].parts()] + [labels[1], labels[3], s4]
        self.play(*[FadeOut(m) for m in gone], Transform(box, box2), Transform(box_t, box_t2), Transform(sl, sl2),
                  *u1.move(-4.6), *u3.move(-1.2), labels[0].animate.move_to([-4.6, labels[0].get_y(), 0]),
                  labels[2].animate.move_to([-1.2, labels[2].get_y(), 0]), run_time=1.2)

        top = RIM + ST["tallpale"]["h"] * K + 0.05
        line = DashedLine([-5.7, top, 0], [-0.3, top, 0], color=GOLD, stroke_width=4)
        bar = DoubleArrow([-2.15, RIM, 0], [-2.15, top, 0], buff=0, color=GOLD, stroke_width=5, tip_length=0.2)
        tall_t = T("tallest", 26, GOLD).move_to([-3.6, top + 0.35, 0])
        self.at("the tallest")
        self.play(Create(line), GrowArrow(bar), FadeIn(tall_t), run_time=0.9)
        best = chip("the best?", ORANGE, size=32).move_to([3.75, 2.65, 0])
        self.at("the best")
        self.play(FadeIn(best, shift=DOWN * 0.15), run_time=0.5)
        c_col = chip("ask about", TEXT, size=30).move_to([3.75, 1.5, 0])
        c_str = chip("strength", TEXT, size=30).move_to([3.75, 0.5, 0])
        c_hei = chip("height", GOLD, size=30).move_to([3.75, -0.5, 0])
        self.at("ask about")
        self.play(FadeIn(c_col, shift=LEFT * 0.2), Indicate(VGroup(u1.sprout, u3.sprout), scale_factor=1.12), run_time=0.7)
        self.at("strength")
        self.play(FadeIn(c_str, shift=LEFT * 0.2), run_time=0.5)
        self.at("only height")
        self.play(FadeIn(c_hei, shift=LEFT * 0.2), Indicate(bar, color=GOLD), run_time=0.6)

        # --- stored food -----------------------------------------------------------------------------
        gx, gy, gh = 3.75, -0.45, 2.4
        outline = Ellipse(width=1.7, height=gh, stroke_color=SOIL, stroke_width=6, fill_color=SOIL, fill_opacity=0.25).move_to([gx, gy, 0])
        fill = Ellipse(width=1.25, height=gh - 0.45, stroke_width=0, fill_color=PINK, fill_opacity=0.85).move_to([gx, gy, 0])
        g_t = T("food stored in the seed", 24, PINK).move_to([gx, gy + gh / 2 + 0.4, 0])
        fl = Arrow([gx - 0.9, 0.2, 0], [-0.55, 0.2, 0], buff=0, color=PINK, stroke_width=6, tip_length=0.25)
        self.at("stretches on food")
        self.play(FadeOut(VGroup(c_col, c_str, c_hei, best)), run_time=0.4)
        self.play(FadeIn(outline), FadeIn(fill), FadeIn(g_t), GrowArrow(fl), run_time=0.8)
        empty = Ellipse(width=0.06, height=0.06, stroke_width=0, fill_color=PINK, fill_opacity=0.0).move_to([gx, gy, 0])
        self.at("food runs out")
        self.play(Transform(fill, empty), FadeOut(fl), run_time=1.2)
        self.at("grows weaker")
        self.play(u3.go("flop"), run_time=1.0)
        real = chip("a real result", GOLD, size=32).move_to([3.75, -2.65, 0])
        self.at("still real")
        self.play(FadeIn(real, shift=UP * 0.15), run_time=0.5)
        self.at("throw it out")
        self.play(Indicate(real, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def icon(sym, color, size=34):
    c = Circle(radius=0.38, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.16)
    return VGroup(c, T(sym, size, color, weight=BOLD).move_to(c))


class S06Rule(SpokenScene):
    """An extra cup for the new idea keeps the first test fair; then the five steps."""

    def construct(self):
        k, rim = 1.0, -0.75
        xs = [-5.0, -2.5, 0.0, 2.5, 5.0]
        sts = ["sturdy", "droop", "tallpale", "droop"]
        us = [Unit(x, rim=rim, k=k, st=s, water=w) for x, s, w in zip(xs, sts, (True, False, True, False))]
        self.add(*[m for u in us for m in u.parts()])
        ask = chip("extra water?", ORANGE, size=28).move_to([-5.0, 2.85, 0])
        self.at("extra water for one cup")
        self.play(FadeIn(ask, shift=DOWN * 0.15), run_time=0.6)
        r1 = us[0].ring()
        self.at("do not change that cup")
        self.play(Create(r1), run_time=0.6)
        x5 = Unit(5.0, rim=rim, k=k, st="start", water=True)
        extra_drop = place(drop_shape(0.0, -0.75), 5.0, rim, k)
        x5.drop.shift(LEFT * 0.25 * k)
        extra_drop.shift(RIGHT * 0.25 * k).set_z_index(3)
        lab5 = T("extra cup", 24, ORANGE).move_to([5.0, rim - 1.5 * k - 0.42, 0])
        self.at("extra cup")
        self.play(*[FadeIn(m) for m in x5.parts()], FadeIn(extra_drop), FadeIn(lab5),
                  ask.animate.move_to([5.0, 2.85, 0]), FadeOut(r1), run_time=1.2)
        fair = RoundedRectangle(corner_radius=0.18, width=9.6, height=4.5, stroke_color=TEAL, stroke_width=5).move_to([-1.25, -0.0, 0])
        fair_t = T("the first test stays fair", 26, TEAL).move_to([-1.25, -2.6, 0])
        self.at("first test stays fair")
        self.play(Create(fair), FadeIn(fair_t), run_time=0.8)

        # --- the five steps ------------------------------------------------------------------------------
        self.at("short version")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        head = T("A fair test, in short", 34, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(FadeIn(head), run_time=0.4)
        rows = [("?", ORANGE, "Predict first", "Predict first"),
                ("1", GOLD, "Change one thing at a time", "Change one thing"),
                ("=", TEAL, "Keep everything else the same", "everything else the same"),
                ("", TEXT, "Look and compare", "Look and compare"),
                ("!", RED, "Keep every real result", "Keep every real result")]
        for n, (sym, col, text, cue) in enumerate(rows):
            y = 1.85 - n * 1.15
            if sym:
                ic = icon(sym, col)
            else:
                lens = Circle(radius=0.17, stroke_color=col, stroke_width=4).move_to([-0.07, 0.07, 0])
                hand = Line([0.06, -0.06, 0], [0.26, -0.26, 0], color=col, stroke_width=5)
                ring = Circle(radius=0.38, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.16)
                ic = VGroup(ring, lens, hand)
            ic.move_to([-3.6, y, 0])
            tx = T(text, 40, TEXT).move_to([-2.85, y, 0], aligned_edge=LEFT)
            self.at(cue)
            self.play(FadeIn(ic, scale=0.7), FadeIn(tx, shift=RIGHT * 0.3), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Predict. Change one thing at a time. Keep every real result."
