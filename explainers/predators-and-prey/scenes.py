"""Predators and prey: predators and prey change each other's numbers  (Biochemistrypedia explainer, grade 7 Life Science)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  RED    = wolves / the predator population
  BLUE   = moose / the prey population
  GREEN  = balsam fir (the moose's plant food)
  YELLOW = energy that passes from moose to wolf
  GREY   = island, water, outlines, other causes, notes
Dots are schematic animals ("a sketch, not real counts"). Real numbers on screen: 2 wolves (counted)
and 1,300 moose (estimated), Isle Royale, winter 2016.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

WOLF = RED
MOOSE = BLUE
FIR = GREEN


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dot(color, r=0.17):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.6)


def slots(cx, cy, w, h, n, seed, gap=0.5):
    """n non-overlapping positions inside an ellipse of width w, height h."""
    rng = np.random.default_rng(seed)
    out = []
    tries = 0
    while len(out) < n and tries < 20000:
        tries += 1
        p = rng.uniform(-1, 1, 2)
        if p[0] ** 2 + p[1] ** 2 > 0.78:
            continue
        q = np.array([cx + p[0] * w / 2, cy + p[1] * h / 2])
        if all(np.hypot(*(q - o)) > gap for o in out):
            out.append(q)
    return out


class Island:
    """An island outline with wolf dots and moose dots whose counts can change (schematic)."""
    def __init__(self, scene, cx, cy, w, h, seed=3, wolves=0, moose=0, show_outline=True):
        self.s = scene
        pos = slots(cx, cy, w, h, 6 + 16, seed, gap=0.52)
        self.wpos, self.mpos = pos[:6], pos[6:]
        self.outline = Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                               fill_opacity=0.10).move_to([cx, cy, 0])
        self.wd = [dot(WOLF, 0.21).move_to([*p, 0]) for p in self.wpos]
        self.md = [dot(MOOSE, 0.15).move_to([*p, 0]) for p in self.mpos]
        self.nw, self.nm = wolves, moose
        self.group = VGroup(self.outline, *self.wd[:wolves], *self.md[:moose]) if show_outline else VGroup(*self.wd[:wolves], *self.md[:moose])

    def set(self, wolves=None, moose=None):
        anims = []
        if wolves is not None:
            if wolves > self.nw:
                anims += [FadeIn(d, scale=0.5) for d in self.wd[self.nw:wolves]]
            elif wolves < self.nw:
                anims += [FadeOut(d) for d in self.wd[wolves:self.nw]]
            self.nw = wolves
        if moose is not None:
            if moose > self.nm:
                anims += [FadeIn(d, scale=0.5) for d in self.md[self.nm:moose]]
            elif moose < self.nm:
                anims += [FadeOut(d) for d in self.md[moose:self.nm]]
            self.nm = moose
        return anims

    def add(self):
        self.s.add(self.outline, *self.wd[:self.nw], *self.md[:self.nm])

    def wolves_group(self):
        return VGroup(*self.wd[:self.nw])

    def moose_group(self):
        return VGroup(*self.md[:self.nm])


def legend(x, y):
    a = dot(WOLF, 0.17).move_to([x - 2.2, y, 0])
    la = T("wolf", 26, WOLF).next_to(a, RIGHT, buff=0.18)
    b = dot(MOOSE, 0.13).move_to([x + 0.1, y, 0])
    lb = T("moose", 26, MOOSE).next_to(b, RIGHT, buff=0.18)
    note = T("a sketch, not real counts", 22, GREY).move_to([x, y - 0.5, 0])
    return VGroup(a, la, b, lb, note)


NODE = {}


def loop_nodes(cx=2.95):
    nodes = {
        1: chip("many moose", MOOSE, size=27).move_to([cx, 2.55, 0]),
        2: chip("more wolves", WOLF, size=27).move_to([cx + 2.15, 0.1, 0]),
        3: chip("fewer moose", MOOSE, size=27).move_to([cx, -2.35, 0]),
        4: chip("fewer wolves", WOLF, size=27).move_to([cx - 2.15, 0.1, 0]),
    }
    arrows = {
        1: arr(nodes[1].get_right() + DOWN * 0.1, nodes[2].get_top() + UP * 0.02, GREY),
        2: arr(nodes[2].get_bottom() + DOWN * 0.02, nodes[3].get_right() + UP * 0.1, GREY),
        3: arr(nodes[3].get_left() + UP * 0.1, nodes[4].get_bottom() + DOWN * 0.02, GREY),
        4: arr(nodes[4].get_top() + UP * 0.02, nodes[1].get_left() + DOWN * 0.1, GREY),
    }
    return nodes, arrows


class S00Title(TitleCard):
    LESSON = "Predators and prey"
    TITLE = "Predators and Prey Change Each Other's Numbers"


# ---------------------------------------------------------------------------------------------
class S01Island(SpokenScene):
    def construct(self):
        water = Rectangle(width=12.6, height=5.6, stroke_color=GREY, stroke_width=2, fill_color=BLUE,
                          fill_opacity=0.05).move_to([0, -0.55, 0])
        lake = T("Lake Superior", 26, GREY).move_to([-4.6, -2.95, 0])
        isl = Island(self, -2.9, -0.45, 6.6, 4.3, seed=3, wolves=0, moose=0)
        ilabel = T("Isle Royale", 38, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.at("Isle Royale is")
        self.play(FadeIn(water), FadeIn(isl.outline), Write(ilabel), FadeIn(lake), run_time=1.2)
        self.at("Wolves hunt moose")
        self.play(*isl.set(wolves=2, moose=16), run_time=1.2)
        k1 = VGroup(T("2 wolves", 46, WOLF, weight=BOLD), T("counted, winter 2016", 26, GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        k2 = VGroup(T("1,300 moose", 46, MOOSE, weight=BOLD), T("estimated, winter 2016", 26, GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        k = VGroup(k1, k2).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.4, 0.0, 0])
        self.at("scientists counted")
        self.play(FadeIn(k1, shift=LEFT * 0.2), Indicate(isl.wolves_group(), color=WOLF), run_time=1.0)
        self.at("They estimated")
        self.play(FadeIn(k2, shift=LEFT * 0.2), Indicate(isl.moose_group(), color=MOOSE, scale_factor=1.05), run_time=1.0)
        note = T("dots are not to scale", 22, GREY).move_to([3.4, -2.6, 0])
        self.play(FadeIn(note), run_time=0.3)
        q = T("If wolves eat moose, why don't they\neat every last moose?", 40, TEXT, font=TITLE_FONT, line_spacing=0.8)
        fit(q, max_w=11.6, max_h=1.6)
        q.move_to([0, 0, 0])
        self.at("So here is the question")
        self.play(FadeOut(k), FadeOut(note), FadeOut(ilabel), FadeOut(water), FadeOut(lake),
                  FadeOut(isl.outline), FadeOut(isl.wolves_group()), FadeOut(isl.moose_group()), run_time=0.7)
        self.play(Write(q), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Terms(SpokenScene):
    def construct(self):
        isl = Island(self, 0, -0.3, 8.2, 4.8, seed=5, wolves=0, moose=16)
        self.at("A population is")
        self.play(FadeIn(isl.outline), FadeIn(isl.moose_group(), lag_ratio=0.05), run_time=1.0)
        t1 = T("one species, in one place", 36, TEXT).move_to([0, 3.0, 0])
        self.play(FadeIn(t1, shift=DOWN * 0.1), run_time=0.6)
        ring = Ellipse(width=7.2, height=4.0, stroke_color=MOOSE, stroke_width=4).move_to([0, -0.3, 0])
        ring.set_stroke(opacity=0.9)
        tag = chip("population: all the moose", MOOSE, size=32).move_to([0, -3.45, 0])
        self.at("All the moose")
        self.play(Create(ring), FadeIn(tag, shift=UP * 0.1), run_time=1.0)
        self.at("A predator is")
        self.play(FadeOut(isl.outline), FadeOut(isl.moose_group()), FadeOut(ring), FadeOut(tag), FadeOut(t1), run_time=0.6)
        wolf = chip("wolf", WOLF, size=54).move_to([-3.7, 0.7, 0])
        moose = chip("moose", MOOSE, size=54).move_to([3.7, 0.7, 0])
        self.play(FadeIn(wolf, scale=0.9), run_time=0.5)
        pred = T("predator", 44, WOLF, weight=BOLD).next_to(wolf, DOWN, buff=0.45)
        self.play(FadeIn(pred, shift=UP * 0.1), run_time=0.5)
        self.at("catches and eats")
        eats = T("catches and eats", 32, GREY).move_to([0, 0.7, 0])
        self.play(FadeIn(moose, scale=0.9), FadeIn(eats), run_time=0.8)
        prey = T("prey", 44, MOOSE, weight=BOLD).next_to(moose, DOWN, buff=0.45)
        self.at("its prey")
        self.play(FadeIn(prey, shift=UP * 0.1), run_time=0.6)
        note = T("main prey of the island's wolves", 32, GREY).move_to([0, -2.6, 0])
        self.at("main prey")
        self.play(FadeIn(note, shift=UP * 0.1), Indicate(moose, color=MOOSE), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Web(SpokenScene):
    def construct(self):
        fir = chip("balsam fir", FIR, size=44).move_to([-4.5, 1.0, 0])
        moose = chip("moose", MOOSE, size=44).move_to([0, 1.0, 0])
        wolf = chip("wolf", WOLF, size=44).move_to([4.5, 1.0, 0])
        ttl = T("food web", 44, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("A food web")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), *[FadeIn(c, scale=0.9) for c in (fir, moose, wolf)], lag_ratio=0.15, run_time=1.2)
        a1 = arr(fir.get_right(), moose.get_left(), GREY, w=7)
        a2 = arr(moose.get_right(), wolf.get_left(), GREY, w=7)
        self.at("Each arrow points")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        food = T("food", 30, GREY).next_to(fir, DOWN, buff=0.25)
        eater = T("eater", 30, GREY).next_to(moose, DOWN, buff=0.25)
        self.at("from the food")
        self.play(FadeIn(food, shift=UP * 0.1), run_time=0.4)
        self.at("to the eater")
        self.play(FadeIn(eater, shift=UP * 0.1), run_time=0.4)
        self.at("Moose eat fir trees")
        self.play(Indicate(a1, color=FIR, scale_factor=1.15), run_time=0.9)
        self.play(FadeOut(food), FadeOut(eater), run_time=0.3)
        self.at("When a wolf eats")
        self.play(Indicate(a2, color=WOLF, scale_factor=1.15), run_time=0.7)
        en = T("some of the energy", 30, YELLOW).move_to([2.25, 2.0, 0])
        ball = Circle(radius=0.17, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.8).move_to(moose.get_right() + RIGHT * 0.35)
        self.at("some of the energy")
        self.play(FadeIn(en, shift=DOWN * 0.1), FadeIn(ball, scale=0.5), run_time=0.6)
        self.at("passes to the wolf")
        self.play(ball.animate.move_to(wolf.get_left() + LEFT * 0.3), run_time=0.9)
        self.play(FadeOut(ball), FadeOut(en), run_time=0.4)
        pack = VGroup(*[dot(WOLF, 0.21).move_to([4.5 + dx, -1.35 + dy, 0]) for dx, dy in ((-0.5, 0.25), (0.45, 0.35), (-0.15, -0.4), (0.6, -0.3))])
        self.at("Wolves often hunt")
        self.play(FadeIn(pack, lag_ratio=0.2, shift=UP * 0.1), run_time=1.0)
        ring = Ellipse(width=2.4, height=1.7, stroke_color=WOLF, stroke_width=3).move_to([4.5, -1.35, 0])
        plab = T("pack", 40, WOLF, weight=BOLD).move_to([4.5, -2.75, 0])
        defn = T("a group of predators that\nlive and hunt together", 32, TEXT, line_spacing=0.8).move_to([-1.0, -1.7, 0])
        self.at("A pack is")
        self.play(Create(ring), FadeIn(plab), run_time=0.8)
        self.at("group of predators")
        self.play(FadeIn(defn, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def build_stage(scene, wolves, moose, nodes_on=(), arrows_on=(), seed=7):
    isl = Island(scene, -3.7, -0.15, 5.4, 5.0, seed=seed, wolves=wolves, moose=moose)
    nodes, arrows = loop_nodes()
    leg = legend(-3.7, -3.0)
    scene.add(isl.outline, *isl.wd[:wolves], *isl.md[:moose], leg)
    for i in nodes_on:
        scene.add(nodes[i])
    for i in arrows_on:
        scene.add(arrows[i])
    return isl, nodes, arrows, leg


class S04Rise(SpokenScene):
    def construct(self):
        isl = Island(self, -3.7, -0.15, 5.4, 5.0, seed=7, wolves=2, moose=16)
        nodes, arrows = loop_nodes()
        leg = legend(-3.7, -3.0)
        self.at("Here is a pattern")
        self.play(FadeIn(isl.outline), FadeIn(isl.wolves_group()), FadeIn(isl.moose_group()), FadeIn(leg), run_time=1.0)
        self.at("prey are plentiful")
        self.play(FadeIn(nodes[1], scale=0.9), Indicate(isl.moose_group(), color=MOOSE, scale_factor=1.05), run_time=1.0)
        self.at("More predators survive")
        self.play(GrowArrow(arrows[1]), FadeIn(nodes[2], scale=0.9), *isl.set(wolves=5), run_time=1.3)
        self.at("population grows")
        self.play(Indicate(nodes[2], color=WOLF), Indicate(isl.wolves_group(), color=WOLF, scale_factor=1.1), run_time=1.0)
        self.at("catch more prey")
        self.play(GrowArrow(arrows[2]), FadeIn(nodes[3], scale=0.9), run_time=0.8)
        self.at("population falls")
        self.play(*isl.set(moose=8), run_time=1.2)
        self.finish()


class S05Fall(SpokenScene):
    def construct(self):
        isl, nodes, arrows, leg = build_stage(self, 5, 8, nodes_on=(1, 2, 3), arrows_on=(1, 2), seed=7)
        self.at("run short of food")
        self.play(GrowArrow(arrows[3]), FadeIn(nodes[4], scale=0.9), run_time=0.9)
        self.at("Fewer of them survive")
        self.play(*isl.set(wolves=3), run_time=1.2)
        self.at("fewer predators hunting")
        self.play(Indicate(isl.wolves_group(), color=WOLF, scale_factor=1.1), run_time=0.8)
        self.at("more prey survive")
        self.play(GrowArrow(arrows[4]), *isl.set(moose=16), run_time=1.3)
        self.at("grows again")
        self.play(Indicate(nodes[1], color=MOOSE), run_time=0.9)
        # the sketch of two lagging curves
        self.at("So predator numbers")
        self.play(*[FadeOut(m) for m in (isl.outline, *isl.wd[:isl.nw], *isl.md[:isl.nm], leg,
                                          *nodes.values(), *arrows.values())], run_time=0.4)
        ax = Axes(x_range=[0, 12.5, 1], y_range=[0, 10, 1], x_length=9.6, y_length=4.4, tips=False,
                  axis_config={"color": GREY, "include_ticks": False, "include_numbers": False, "stroke_width": 3}
                  ).move_to([-0.8, -0.3, 0])
        xl = T("time", 26, GREY).next_to(ax, DOWN, buff=0.2).align_to(ax, RIGHT)
        yl = T("number of animals", 26, GREY).rotate(PI / 2).next_to(ax, LEFT, buff=0.2)
        sk = T("a sketch: real counts are messier", 30, TEXT).move_to([0, 3.15, 0])
        fm = ax.plot(lambda x: 5.2 + 3.2 * np.sin(x * 0.95 - np.pi / 2), x_range=[0, 12.5], color=MOOSE, stroke_width=6)
        fw = ax.plot(lambda x: 5.2 + 2.4 * np.sin((x - 1.15) * 0.95 - np.pi / 2), x_range=[0, 12.5], color=WOLF, stroke_width=6)
        lm = T("moose", 32, MOOSE, weight=BOLD).move_to([5.3, 1.1, 0])
        lw = T("wolves", 32, WOLF, weight=BOLD).move_to([5.3, 0.4, 0])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sk), run_time=0.5)
        self.play(Create(fm), FadeIn(lm), run_time=0.7)
        self.play(Create(fw), FadeIn(lw), run_time=0.7)
        px = np.pi / 0.95
        wx = px + 1.15
        d1 = DashedLine(ax.c2p(px, 0), ax.c2p(px, 9.6), color=MOOSE, stroke_width=3)
        d2 = DashedLine(ax.c2p(wx, 0), ax.c2p(wx, 9.6), color=WOLF, stroke_width=3)
        gap = DoubleArrow(ax.c2p(px, 9.6), ax.c2p(wx, 9.6), buff=0, color=TEXT, stroke_width=4, tip_length=0.18)
        gl = T("a little after", 28, TEXT).next_to(gap, UP, buff=0.12)
        self.at("a little after")
        self.play(Create(d1), Create(d2), run_time=0.7)
        self.play(GrowFromCenter(gap), FadeIn(gl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        box = chip("wolf and moose counts", TEXT, size=34).move_to([0, 0.35, 0])
        box[0].set_stroke(GREY)
        self.at("Real populations are messier")
        self.play(FadeIn(box, scale=0.9), run_time=0.8)
        others = VGroup(*[chip(n, GREY, size=26) for n in ("harsh winters", "ticks", "disease", "the moose's plant food")]).arrange(RIGHT, buff=0.3)
        fit(others, max_w=12.2)
        others.move_to([0, 2.7, 0])
        ars = [arr(c.get_bottom(), box.get_top() + RIGHT * (c.get_center()[0] * 0.25), GREY, w=4, tip=0.18) for c in others]
        self.at("harsh winters")
        self.play(FadeIn(others[0], shift=DOWN * 0.1), GrowArrow(ars[0]), run_time=0.5)
        self.at("ticks")
        self.play(FadeIn(others[1], shift=DOWN * 0.1), GrowArrow(ars[1]), run_time=0.4)
        self.at("disease")
        self.play(FadeIn(others[2], shift=DOWN * 0.1), GrowArrow(ars[2]), run_time=0.4)
        self.at("plant food")
        self.play(FadeIn(others[3], shift=DOWN * 0.1), GrowArrow(ars[3]), run_time=0.5)
        pred = chip("predators", WOLF, size=30).move_to([0, -2.3, 0])
        pa = arr(pred.get_top(), box.get_bottom(), WOLF, w=6)
        self.at("Predators are one cause")
        self.play(FadeIn(pred, shift=UP * 0.1), GrowArrow(pa), run_time=0.8)
        note = T("one cause, not the only one", 28, GREY).next_to(pred, RIGHT, buff=0.4)
        self.at("not the only one")
        self.play(FadeIn(note, shift=LEFT * 0.1), run_time=0.6)
        # the answer on the island
        isl = Island(self, -3.7, 0.0, 5.4, 5.0, seed=11, wolves=4, moose=4)
        leg = legend(-3.7, -3.0)
        self.at("run short of food")
        t1 = T("wolves usually short of food", 34, WOLF).move_to([3.0, 1.8, 0])
        self.play(*[FadeOut(m) for m in (box, *others, *ars, pred, pa, note)], run_time=0.4)
        self.play(FadeIn(isl.outline), FadeIn(isl.wolves_group()),
                  FadeIn(isl.moose_group()), FadeIn(leg), FadeIn(t1, shift=LEFT * 0.1), run_time=0.7)
        self.play(Indicate(isl.wolves_group(), color=WOLF, scale_factor=1.1), run_time=0.6)
        t2 = T("some moose still there", 34, MOOSE).move_to([3.0, 0.6, 0])
        self.at("last prey animal")
        self.play(FadeIn(t2, shift=LEFT * 0.1), Indicate(isl.moose_group(), color=MOOSE, scale_factor=1.15), run_time=0.8)
        t3 = T("fewer wolves survive", 34, WOLF).move_to([3.0, -0.6, 0])
        self.at("fewer wolves survive")
        self.play(FadeIn(t3, shift=LEFT * 0.1), *isl.set(wolves=2), run_time=1.0)
        t4 = T("the moose can recover", 34, MOOSE).move_to([3.0, -1.8, 0])
        self.at("moose can recover")
        self.play(FadeIn(t4, shift=LEFT * 0.1), *isl.set(moose=12), run_time=1.2)
        final = T("Wolves do not eat\nevery last moose.", 44, TEXT, font=TITLE_FONT, line_spacing=0.8).move_to([3.0, 0, 0])
        fit(final, max_w=5.6)
        self.at("That is why")
        self.play(*[FadeOut(m) for m in (t1, t2, t3, t4)], run_time=0.5)
        self.play(Write(final), run_time=1.5)
        self.finish()


class S07End(EndCard):
    LINE = "Usually predators run short of food before the last prey is caught."
