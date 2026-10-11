"""Finding a signal: how a bioassay turns an unknown activity into something you can purify
(Biochemistrypedia section film). Timed to the SPOKEN words: every self.at("...") waits for that phrase.

COLOR MAP (one color per concept, whole video)
  YELLOW = the sample / the source of the factor (tumor fragment, tubes of extract)
  BLUE   = the ganglion
  GREEN  = the living response (fibers, the halo) and the activity read from it
  TEAL   = the bioassay itself
  ORANGE = specific activity (activity per milligram of protein)
  GREY   = dish, plasma clot, tube walls, labels, the unknown
  RED    = the slow, messy embryo test that the dish replaces
No molecular structures: a ganglion is a disc, fibers are lines, tubes are rounded bars.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F59E4B"

GX, GY = -1.9, 0.05          # the ganglion in the dish
TX = 3.3                     # the tumor fragment


def bchip(text, color=BLUE, size=24, pad=0.2):
    c = chip(text, color, size=size, pad=pad)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def ganglion(c, r=0.5):
    return Circle(radius=r, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45).move_to([c[0], c[1], 0])


def fibers(c, r=0.5, toward=None, reach=0.45, extra=1.0, w=3.5):
    """a halo of straight lines out of a disc. With `toward` (radians) it is longer and denser that way."""
    cx, cy = c
    angles = list(np.linspace(0, TAU, 20, endpoint=False))
    if toward is not None:
        angles += [toward + d for d in np.linspace(-1.0, 1.0, 9) + 0.0] + [toward + d for d in np.linspace(-0.9, 0.9, 8) + 0.11]
    lines = VGroup()
    for a in angles:
        u = np.array([np.cos(a), np.sin(a), 0])
        ln = r + reach + (extra * max(0.0, np.cos(a - toward)) ** 1.5 if toward is not None else 0.0)
        lines.add(Line([cx, cy, 0] + u * r, [cx, cy, 0] + u * ln, color=GREEN, stroke_width=w))
    return lines


def tube(x, y, alpha=0.55, h=1.3, w=0.7):
    wall = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    liq = RoundedRectangle(corner_radius=0.14, width=w - 0.16, height=h * 0.62, stroke_width=0,
                           fill_color=YELLOW, fill_opacity=alpha).move_to([x, y - h * 0.16, 0])
    return VGroup(wall, liq)


def test_unit(x, y, halo=True, r=0.3, reach=0.35, w=2.5):
    g = VGroup(ganglion((x, y), r))
    f = fibers((x, y), r, reach=reach, w=w)
    if halo:
        g.add(f)
    g.disc, g.halo = g[0], f
    return g


def unread(x, y, r=0.5):
    """a test not yet read: dashed outline and a question mark, no result."""
    ring = DashedVMobject(Circle(radius=r).move_to([x, y, 0]), num_dashes=16).set_color(GREY)
    return VGroup(ring, T("?", 34, TEXT, weight=BOLD).move_to([x, y, 0]))


def dish_parts():
    dish = RoundedRectangle(corner_radius=0.6, width=11.6, height=5.3, stroke_color=GREY, stroke_width=4).move_to([0, 0.15, 0])
    clot = Ellipse(width=5.9, height=4.0, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.22).move_to([GX, GY, 0])
    clot_lbl = T("blood plasma clot", 22, GREY).move_to([GX, 2.45, 0])
    gang = ganglion((GX, GY)).set_z_index(2)
    clot.set_z_index(1)
    g_lbl = T("ganglion", 22, BLUE).move_to([-3.95, GY, 0])
    tum = bchip("tumor fragment", YELLOW, 24).move_to([TX, GY, 0])
    return dish, clot, clot_lbl, gang, g_lbl, tum


class Film(SpokenScene):
    def outro(self, *anims, run_time=0.4):
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Finding a Signal: NGF, EGF and the Bioassay"
    TITLE = "Follow the activity before the molecule"


# ---------------------------------------------------------------------------------------------
class S01Dish(Film):
    """a slow, messy test in an embryo becomes a ganglion in a dish beside a tumor fragment."""

    def construct(self):
        emb = RoundedRectangle(corner_radius=0.8, width=7.0, height=3.6, stroke_color=RED, stroke_width=4,
                               fill_color=RED, fill_opacity=0.08).move_to([0, 0.2, 0])
        etxt = T("embryo", 30, GREY).move_to([-1.4, 0.7, 0])
        etum = bchip("tumor", YELLOW, 26).move_to([1.2, -0.1, 0])
        est = VGroup(emb, etxt, etum)
        self.add(emb)
        self.play(FadeIn(etxt), run_time=0.4)
        self.at("A tumor in an embryo")
        self.play(FadeIn(etum, shift=DOWN * 0.2), run_time=0.5)
        slow = T("slow, messy detector", 32, RED).move_to([0, -2.4, 0])
        self.at("slow, messy")
        self.play(FadeIn(slow, shift=UP * 0.12), run_time=0.5)

        dish, clot, clot_lbl, gang, g_lbl, tum = dish_parts()
        self.at("into a dish")
        self.play(FadeOut(VGroup(etxt, etum, slow)), ReplacementTransform(emb, dish), run_time=0.9)
        dlbl = T("dish", 24, GREY).move_to([-4.9, 2.2, 0])
        self.play(FadeIn(dlbl), run_time=0.3)
        self.at("a chick ganglion")
        self.play(FadeIn(gang, scale=0.6), FadeIn(g_lbl), run_time=0.5)
        self.at("clot of blood plasma")
        self.play(FadeIn(clot), FadeIn(clot_lbl), run_time=0.6)
        self.at("fragment of tumor")
        self.play(FadeIn(tum, shift=LEFT * 0.3), run_time=0.5)
        gap = DoubleArrow([GX + 2.95 + 0.1, GY, 0], [TX - 1.45 - 0.1, GY, 0], buff=0, color=GREY, stroke_width=4,
                          tip_length=0.15)
        nt = T("near, not touching", 22, GREY).move_to([1.2, 0.8, 0])
        self.at("not touching")
        self.play(GrowFromCenter(gap), FadeIn(nt), run_time=0.5)
        self.outro(FadeOut(VGroup(gap, nt, dlbl)))


# ---------------------------------------------------------------------------------------------
class S02Halo(Film):
    """the halo grows, thickest toward the tumor, and is named a bioassay."""

    def construct(self):
        dish, clot, clot_lbl, gang, g_lbl, tum = dish_parts()
        self.add(dish, clot, clot_lbl, gang, g_lbl, tum)
        fib = fibers((GX, GY), toward=0.0).set_z_index(3)
        self.at("Within 24 hours")
        self.wait(0.3)
        self.at("a dense halo")
        self.play(LaggedStart(*[Create(f) for f in fib], lag_ratio=0.02), run_time=1.3)
        hl = T("halo of fibers", 22, GREEN).move_to([GX, GY + 1.45, 0])
        self.play(FadeIn(hl), run_time=0.3)
        right = VGroup(*[f for f in fib if f.get_end()[0] > GX + 1.2])
        self.at("thickest toward the tumor")
        self.play(Indicate(right, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.at("fit in a dish")
        self.play(Indicate(dish, color=TEXT, scale_factor=1.0), run_time=0.7)
        frame = RoundedRectangle(corner_radius=0.3, width=6.3, height=4.3, stroke_color=TEAL, stroke_width=4).move_to([GX, GY, 0])
        bio = T("bioassay", 36, TEAL, weight=BOLD).move_to([-4.2, -3.05, 0])
        self.at("halo is a bioassay")
        self.play(Create(frame), FadeIn(bio, shift=UP * 0.1), run_time=0.6)
        desc = T("a living response is the measuring device", 26, TEXT).next_to(bio, RIGHT, buff=0.35)
        self.at("a living response")
        self.play(FadeIn(desc, shift=RIGHT * 0.12), run_time=0.5)
        q = T("?", 52, TEXT, weight=BOLD).move_to([TX, GY + 0.9, 0])
        unk = T("molecule unknown", 22, GREY).move_to([TX, GY - 0.75, 0])
        self.at("before you know")
        self.play(FadeIn(q, scale=0.6), FadeIn(unk), run_time=0.5)
        self.outro(FadeOut(VGroup(dish, clot, clot_lbl, gang, g_lbl, tum, fib, hl, frame, bio, desc, q, unk)))


# ---------------------------------------------------------------------------------------------
class S03Dilute(Film):
    """a dilution series, each tested; the highest dilution with a halo; activity per milligram."""

    def construct(self):
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        alphas = [0.8, 0.6, 0.42, 0.26, 0.12]
        TY, UY = 1.75, -0.15
        t0 = tube(0, TY, alphas[0])
        u0 = test_unit(0, UY)
        d0 = arr([0, TY - 0.8, 0], [0, UY + 0.75, 0])
        bio = T("bioassay", 28, TEAL, weight=BOLD).move_to([0, -1.5, 0])
        self.add(t0)
        self.at("A bioassay")
        self.play(GrowArrow(d0), FadeIn(u0), FadeIn(bio), run_time=0.6)
        # dilute step by step: the first tube moves left and the others appear
        tubes = [t0] + [tube(x, TY, a) for x, a in zip(xs[1:], alphas[1:])]
        lead = Line([-4.4, 2.85, 0], [-1.3, 2.85, 0], color=GREY, stroke_width=4)
        dl = T("more dilute", 24, GREY).move_to([0, 2.85, 0])
        dar = arr([1.3, 2.85, 0], [4.4, 2.85, 0], w=4)
        self.at("Dilute a sample")
        self.play(FadeOut(bio), t0.animate.move_to([-4.4, TY, 0]), u0.animate.move_to([-4.4, UY, 0]),
                  d0.animate.move_to([-4.4, (TY - 0.8 + UY + 0.75) / 2, 0]), run_time=0.6)
        self.at("step by step")
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tubes[1:]], lag_ratio=0.3),
                  FadeIn(lead), FadeIn(dl), FadeIn(dar), run_time=1.3)
        units, ds = [u0], [d0]
        for i in range(1, 5):
            units.append(test_unit(xs[i], UY, halo=i <= 2))
            ds.append(arr([xs[i], TY - 0.8, 0], [xs[i], UY + 0.75, 0]))
        self.at("The highest dilution")
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(ds[i]), FadeIn(units[i])) for i in range(1, 5)], lag_ratio=0.25),
                  run_time=1.2)
        nh = VGroup(*[T("no halo", 22, GREY).move_to([xs[i], -1.05, 0]) for i in (3, 4)])
        box = Rectangle(width=1.9, height=3.6, stroke_color=GREEN, stroke_width=4).move_to([0, 0.7, 0])
        hi = T("highest dilution that still gives a halo", 24, GREEN).move_to([0, -1.55, 0])
        self.at("still gives a halo")
        self.play(FadeIn(nh), Create(box), FadeIn(hi), run_time=0.7)
        act = bchip("activity", GREEN, 28)
        div = T("÷", 36, TEXT)
        mg = bchip("milligrams of protein", GREY, 28)
        eq = T("=", 36, TEXT)
        spec = bchip("specific activity", ORANGE, 28)
        row = VGroup(act, div, mg, eq, spec).arrange(RIGHT, buff=0.3).move_to([0, -2.4, 0])
        self.at("how much factor")
        self.play(FadeIn(act, shift=DOWN * 0.15), run_time=0.4)
        self.at("Divide by")
        self.play(FadeIn(div), FadeIn(mg, shift=RIGHT * 0.15), run_time=0.5)
        self.at("That gives the specific")
        self.play(FadeIn(eq), FadeIn(spec, shift=RIGHT * 0.15), run_time=0.5)
        per = T("activity per milligram of protein", 24, ORANGE).move_to([0, -3.1, 0])
        self.at("per milligram")
        self.play(FadeIn(per, shift=UP * 0.1), run_time=0.5)
        self.outro(FadeOut(VGroup(*tubes, lead, dl, dar, *units, *ds, nh, box, hi, act, div, mg, eq, spec, per)))


# ---------------------------------------------------------------------------------------------
class S04Follow(Film):
    """the same assay on a sample from each purification step: did activity per milligram go up?"""

    def construct(self):
        xs = [-4.2, 0.0, 4.2]
        TY, UY = 1.6, -0.5
        names = ["crude extract", "after a step", "after the next step"]
        tubes = [tube(x, TY, 0.55) for x in xs]
        labs = [T(n, 22, GREY).move_to([x, 2.75, 0]) for n, x in zip(names, xs)]
        self.play(FadeIn(tubes[0]), FadeIn(labs[0]), run_time=0.5)
        steps = []
        for i in (0, 1):
            a = arr([xs[i] + 0.55, TY, 0], [xs[i + 1] - 0.55, TY, 0], w=4)
            s = T("purification step", 22, TEXT).move_to([(xs[i] + xs[i + 1]) / 2, TY + 0.5, 0])
            steps.append((a, s))
        self.at("a sample from each")
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(steps[i][0]), FadeIn(tubes[i + 1]), FadeIn(labs[i + 1]))
                                for i in (0, 1)], lag_ratio=0.5), run_time=1.0)
        self.at("each purification step")
        self.play(FadeIn(steps[0][1]), FadeIn(steps[1][1]), run_time=0.5)
        units = [unread(x, UY) for x in xs]
        ds = [arr([x, TY - 0.8, 0], [x, UY + 0.75, 0]) for x in xs]
        self.at("the same assay")
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(d), FadeIn(u)) for d, u in zip(ds, units)], lag_ratio=0.3), run_time=1.2)
        line = Line([-5.4, -1.5, 0], [5.4, -1.5, 0], color=TEAL, stroke_width=4)
        bio = T("the same bioassay", 24, TEAL).move_to([0, -1.85, 0])
        self.play(Create(line), FadeIn(bio), run_time=0.5)
        qn = T("Did the activity per milligram go up?", 36, ORANGE, weight=BOLD).move_to([0, -2.75, 0])
        self.at("one question")
        self.play(FadeIn(qn, shift=UP * 0.12), run_time=0.6)
        self.at("follow the factor")
        self.play(LaggedStart(*[Indicate(u, color=TEXT, scale_factor=1.15) for u in units], lag_ratio=0.3), run_time=1.2)
        rule = T("You cannot purify what you cannot detect.", 36, TEXT, weight=BOLD).move_to([0, -2.75, 0])
        self.at("you cannot purify")
        self.play(ReplacementTransform(qn, rule), run_time=0.6)
        self.finish()


class S05End(EndCard):
    LINE = "You cannot purify what you cannot detect."
