"""Food webs and energy: less energy at every step  (Biochemistrypedia explainer, grade 7 Life Science)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = sunlight / energy and the "about one tenth passes up" arrows
  GREEN  = producers (phytoplankton)
  TEAL   = first-order consumers (zooplankton)
  INDIGO = second-order consumers (menhaden)
 consumers (osprey)
  RED    = heat (thermal energy) leaving
  GREY   = water, outlines, uneaten food, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

C2 = "#6C8CF0"
C3 = "#E070B8"
TEAL_C = "#3FB8C0"
LEVEL = {"prod": GREEN, "c1": TEAL_C, "c2": C2, "c3": C3}


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def fish(x, y, color=C2, s=1.0):
    body = Ellipse(width=0.95 * s, height=0.45 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    tail = Polygon([0.4 * s, 0, 0], [0.75 * s, 0.25 * s, 0], [0.75 * s, -0.25 * s, 0], stroke_color=color,
                   stroke_width=3, fill_color=color, fill_opacity=0.35)
    return VGroup(body, tail).move_to([x, y, 0])


def dots(cx, cy, n, r, color, seed):
    rng = np.random.default_rng(seed)
    out = []
    while len(out) < n:
        p = rng.uniform(-r, r, 2)
        if np.hypot(*p) <= r and all(np.hypot(p[0] - q[0], p[1] - q[1]) > 0.42 for q in out):
            out.append(p)
    return VGroup(*[Circle(radius=0.16, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.55)
                    .move_to([cx + p[0], cy + p[1], 0]) for p in out])


def tier(x, y, w, color, h=1.05):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([x, y, 0])


TIER_Y = [-1.95, -0.78, 0.39, 1.56]
TIER_W = [6.0, 4.2, 2.6, 1.2]
TIER_C = [GREEN, TEAL_C, C2, C3]
NUMS = ["10,000", "1,000", "100", "10"]


class S00Title(TitleCard):
    LESSON = "Food webs and energy"
    TITLE = "Less energy at every step"


# ---------------------------------------------------------------------------------------------
class S01Osprey(SpokenScene):
    def construct(self):
        water = Rectangle(width=12.6, height=3.2, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                          fill_opacity=0.14).move_to([0, -1.8, 0])
        bay = T("Chesapeake Bay", 26, GREY).move_to([-4.4, -0.55, 0])
        osprey = chip("osprey", C3, size=36).move_to([2.6, 2.2, 0])
        self.at("nest along")
        self.play(FadeIn(water), FadeIn(bay), FadeIn(osprey, shift=DOWN * 0.2), run_time=0.8)
        self.at("plunge")
        self.play(osprey.animate.move_to([2.6, -0.75, 0]), run_time=1.2, rate_func=rush_into)
        school = VGroup(*[fish(1.9 + 1.4 * (i % 3) + 0.4 * (i // 3), -1.75 - 0.7 * (i // 3), C2, 1.35) for i in range(5)])
        flab = T("menhaden", 30, C2).move_to([3.4, -3.0, 0])
        caught = fish(2.6, -1.2, C2, 1.0)
        self.at("catch fish")
        self.play(FadeIn(caught), run_time=0.3)
        self.play(osprey.animate.move_to([2.6, 1.8, 0]), caught.animate.move_to([2.6, 1.05, 0]), run_time=1.2)
        self.at("Atlantic")
        self.play(FadeIn(school, shift=LEFT * 0.3), FadeIn(flab), run_time=0.9)
        pl = dots(-3.0, -1.95, 11, 0.85, GREEN, 4)
        plab = T("plankton", 30, GREEN).move_to([-3.0, -3.0, 0])
        self.at("tiny living things")
        self.play(FadeIn(pl, lag_ratio=0.1), FadeIn(plab), run_time=1.0)
        self.at("So here is the question")
        self.play(*[FadeOut(m) for m in (water, bay, osprey, caught, school, flab, pl, plab)], run_time=0.6)
        row = []
        for name, col, x in (("plankton", GREEN, -4.2), ("menhaden", C2, 0.0), ("osprey", C3, 4.2)):
            row.append(chip(name, col, size=40).move_to([x, 0.6, 0]))
        a1 = arr(row[0].get_right(), row[1].get_left(), GREY)
        a2 = arr(row[1].get_right(), row[2].get_left(), GREY)
        self.play(*[FadeIn(c, scale=0.9) for c in row], GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        q = T("Why does each step up have less energy to live on?", 38, font=TITLE_FONT)
        fit(q, max_w=11.8)
        q.move_to([0, 2.5, 0])
        self.at("Why does each step")
        self.play(Write(q), run_time=1.6)
        self.at("less energy")
        boxes = []
        for c in row:
            b = RoundedRectangle(corner_radius=0.12, width=3.0, height=1.5, stroke_color=YELLOW, stroke_width=3,
                                 fill_color=YELLOW, fill_opacity=0.1).move_to([c.get_center()[0], -1.3, 0])
            boxes.append(VGroup(b, T("energy?", 36, YELLOW).move_to(b)))
        self.play(*[FadeIn(b, shift=UP * 0.15) for b in boxes], lag_ratio=0.2, run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Producer(SpokenScene):
    def construct(self):
        phy = dots(-0.6, 0.7, 13, 1.2, GREEN, 7)
        tag_p = chip("producer", GREEN, size=30).move_to([-0.6, -2.4, 0])
        self.at("starts with a")
        self.play(FadeIn(phy, lag_ratio=0.08), FadeIn(tag_p, shift=UP * 0.15), run_time=1.0)
        sun = Circle(radius=0.6, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.7).move_to([-5.2, 1.4, 0])
        sun_l = T("sunlight", 28, YELLOW).next_to(sun, DOWN, buff=0.25)
        a_sun = arr([-4.4, 1.2, 0], [-2.1, 0.85, 0], YELLOW, w=7)
        en = T("energy", 28, YELLOW).move_to([-3.25, 1.75, 0])
        self.at("from sunlight")
        self.play(FadeIn(sun, scale=0.7), FadeIn(sun_l), run_time=0.5)
        self.play(GrowArrow(a_sun), FadeIn(en), run_time=0.6)
        self.at("stores it")
        self.play(Indicate(phy, color=YELLOW, scale_factor=1.12), run_time=1.0)
        lab_p = T("phytoplankton", 28, GREEN).move_to([-0.6, -1.3, 0])
        self.at("main producers")
        self.play(FadeIn(lab_p, shift=UP * 0.1), run_time=0.5)
        zoo = VGroup(*[Ellipse(width=0.8, height=0.45, stroke_color=TEAL_C, stroke_width=3, fill_color=TEAL_C,
                               fill_opacity=0.45).move_to([4.2 + dx, 0.7 + dy, 0])
                       for dx, dy in ((-0.7, 0.4), (0.5, 0.7), (0.0, -0.1), (-0.5, -0.65), (0.8, -0.4))])
        lab_z = T("zooplankton", 28, TEAL_C).move_to([4.2, -1.3, 0])
        a_pz = arr([1.0, 0.7, 0], [2.7, 0.7, 0], GREEN, w=7)
        self.at("tiny drifting animals")
        self.play(FadeIn(zoo, lag_ratio=0.15), FadeIn(lab_z), GrowArrow(a_pz), run_time=1.0)
        tag_z = chip("first-order consumer", TEAL_C, size=28).move_to([4.2, -2.4, 0])
        self.at("They are")
        self.play(FadeIn(tag_z, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
NODES = [("sunlight", YELLOW), ("phytoplankton", GREEN), ("zooplankton", TEAL_C), ("menhaden", C2), ("osprey", C3)]


def icon(i, cx, cy):
    col = NODES[i][1]
    if i == 0:
        return Circle(radius=0.38, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.7).move_to([cx, cy, 0])
    if i == 1:
        return VGroup(*[Circle(radius=0.13, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.55)
                        .move_to([cx + dx, cy + dy, 0]) for dx, dy in ((-0.3, 0.25), (0.1, 0.35), (0.35, 0.05), (-0.2, -0.2), (0.15, -0.3))])
    if i == 2:
        return VGroup(*[Ellipse(width=0.6, height=0.32, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.45)
                        .move_to([cx + dx, cy + dy, 0]) for dx, dy in ((-0.2, 0.3), (0.2, 0.0), (-0.15, -0.3))])
    if i == 3:
        return fish(cx - 0.1, cy, col, 0.95)
    body = Ellipse(width=0.5, height=0.3, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.4)
    wings = Polygon([-0.55, 0.05, 0], [-0.3, 0.38, 0], [0, 0.1, 0], [0.3, 0.38, 0], [0.55, 0.05, 0], [0, -0.2, 0],
                    stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.4)
    return VGroup(wings, body).move_to([cx, cy, 0])


class S03Chain(SpokenScene):
    def construct(self):
        xs = [-5.4, -2.7, 0.0, 2.7, 5.4]
        cy = 1.0

        def chips_top(i):
            return np.array([xs[i], cy + 0.85, 0])

        cards = [RoundedRectangle(corner_radius=0.14, width=1.5, height=1.5, stroke_color=NODES[i][1], stroke_width=3,
                                  fill_color=NODES[i][1], fill_opacity=0.12).move_to([xs[i], cy, 0]) for i in range(5)]
        icons = [icon(i, xs[i], cy) for i in range(5)]
        names = [T(NODES[i][0], 24, NODES[i][1]).move_to([xs[i], cy - 1.1, 0]) for i in range(5)]
        arrows = [arr([xs[i] + 0.8, cy, 0], [xs[i + 1] - 0.8, cy, 0], GREY, w=6, tip=0.2) for i in range(4)]
        title = T("food chain", 34, font=TITLE_FONT).move_to([-4.6, 3.1, 0])
        self.at("food chain")
        self.play(FadeIn(title), run_time=0.4)
        self.at("line model")
        self.play(*[FadeIn(VGroup(cards[i], icons[i], names[i]), scale=0.9) for i in range(5)], run_time=0.8)
        self.play(*[GrowArrow(a) for a in arrows], lag_ratio=0.2, run_time=1.0)

        def tag(i, text, color):
            return T(text, 26, color).move_to([xs[i], -1.1, 0])

        tags = {1: tag(1, "producer", GREEN), 2: tag(2, "first-order\nconsumer", TEAL_C),
                3: tag(3, "second-order\nconsumer\n(in this chain)", C2), 4: tag(4, "third-order\nconsumer\n(in this chain)", C3)}
        note = T("arrow: from the food to the eater", 30, YELLOW).move_to([0, -2.7, 0])
        self.at("arrows point")
        self.play(FadeIn(tags[1]), FadeIn(tags[2]), FadeIn(note), *[Indicate(a, color=YELLOW, scale_factor=1.2) for a in arrows],
                  run_time=1.2)
        self.at("menhaden eat")
        self.play(Indicate(arrows[2], color=YELLOW, scale_factor=1.4), run_time=0.8)
        self.at("here they")
        self.play(FadeIn(tags[3], shift=UP * 0.1), run_time=0.6)
        self.at("phytoplankton directly")
        alt = CurvedArrow(chips_top(1), chips_top(3), angle=-TAU / 5, color=YELLOW, stroke_width=5)
        self.play(Create(alt), run_time=0.8)
        self.at("Ospreys eat")
        self.play(Indicate(arrows[3], color=YELLOW, scale_factor=1.4), run_time=0.8)
        self.at("consumer eats")
        self.play(FadeIn(tags[4], shift=UP * 0.1), run_time=0.6)
        self.at("osprey is")
        self.play(Indicate(VGroup(cards[4], icons[4]), color=C3, scale_factor=1.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Heat(SpokenScene):
    def construct(self):
        x0, w0 = -4.3, 1.5
        bar = Rectangle(width=w0, height=3.9, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                        fill_opacity=0.35).move_to([x0, 0.15, 0])
        head = T("energy in the plankton\na menhaden eats", 26, YELLOW).move_to([x0, 2.85, 0])
        self.at("A menhaden eats")
        self.play(FadeIn(bar, scale=0.9), FadeIn(head), run_time=0.8)
        # segments, top to bottom: heat 2.0, uneaten 1.1, body 0.8 (not to scale)
        segs = [(2.1, 0.1, RED), (0.1, -1.0, GREY), (-1.0, -1.8, C2)]
        parts = [Rectangle(width=w0, height=a - b, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.4)
                 .move_to([x0, (a + b) / 2, 0]) for a, b, c in segs]
        self.at("Most of that")
        ns = T("not to scale", 22, GREY).move_to([1.2, -3.0, 0])
        self.play(FadeOut(bar), *[FadeIn(p) for p in parts], FadeIn(ns), run_time=0.5)
        lab_body = T("built into the fish's body", 24, C2)
        wide = 4.4
        cx = 1.2
        tx = [cx - 0, cx, cx]
        blocks = []
        for p, (a, b, c) in zip(parts, segs):
            blocks.append(p)
        heat_l = T("heat (thermal energy)", 26, TEXT)
        unea_l = T("passes through\nundigested", 22, TEXT)
        body_l = T("built into the body", 24, TEXT)
        self.at("Much of it")
        self.play(parts[0].animate.stretch_to_fit_width(wide).move_to([cx, 1.1, 0]), run_time=0.8)
        heat_l.move_to(parts[0])
        harr = VGroup(*[arr([cx - 1.4 + 1.4 * i, 2.15, 0], [cx - 1.4 + 1.4 * i, 3.05, 0], RED, w=6) for i in range(3)])
        self.play(FadeIn(heat_l), LaggedStart(*[GrowArrow(a) for a in harr], lag_ratio=0.25), run_time=1.0)
        self.at("passes through")
        self.play(parts[1].animate.stretch_to_fit_width(wide).move_to([cx, -0.45, 0]), run_time=0.7)
        unea_l.move_to(parts[1])
        self.play(FadeIn(unea_l), run_time=0.4)
        self.at("Only the rest")
        self.play(parts[2].animate.stretch_to_fit_width(wide).move_to([cx, -1.4, 0]), run_time=0.7)
        body_l.move_to(parts[2])
        self.play(FadeIn(body_l), run_time=0.4)
        osp = chip("osprey", C3, size=26).move_to([5.3, -1.4, 0])
        a_o = arr([cx + wide / 2, -1.4, 0], osp.get_left(), C2, w=6)
        self.at("where an osprey")
        self.play(GrowArrow(a_o), FadeIn(osp), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pyramid(cx, with_names=False):
    tiers = [tier(cx, TIER_Y[i], TIER_W[i], TIER_C[i]) for i in range(4)]
    nums = [M(NUMS[i], 30, TEXT).move_to(tiers[i]) for i in range(4)]
    return tiers, nums


class S05Pyramid(SpokenScene):
    def construct(self):
        cx = 0.0
        names = ["Producers", "first-order\nconsumers", "second-order\nconsumers", "third-order\nconsumers"]
        tiers = [tier(cx, TIER_Y[i], TIER_W[i], TIER_C[i]) for i in range(4)]
        outlines = [t.copy().set_fill(opacity=0).set_stroke(GREY, opacity=0.6) for t in tiers]
        labs = [T(names[i], 24, TIER_C[i]).move_to([-3.3 - 1.0, TIER_Y[i], 0]) for i in range(4)]
        for l, i in zip(labs, range(4)):
            l.align_to([-3.35, 0, 0], RIGHT)
        self.at("Stack the energy")
        self.play(*[FadeIn(o) for o in outlines], *[FadeIn(l) for l in labs], lag_ratio=0.1, run_time=1.2)
        title = chip("energy pyramid", YELLOW, size=30).move_to([0, 2.95, 0])
        self.at("This stack")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)
        marks = []
        for i in range(3):
            ym = (TIER_Y[i] + TIER_Y[i + 1]) / 2
            a = arr([3.55, TIER_Y[i] - 0.1, 0], [3.55, TIER_Y[i + 1] + 0.1, 0], YELLOW, w=7)
            t = T("about 1/10", 26, YELLOW).move_to([5.2, ym, 0])
            marks.append(VGroup(a, t))
        self.at("rough rule")
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in marks], lag_ratio=0.35), run_time=1.5)
        note = T("made-up numbers: units per square meter per year", 24, GREY).move_to([0, -3.2, 0])
        self.at("Here is a model")
        self.play(FadeIn(note), run_time=0.6)
        shown = [None] * 4
        for i, cue in enumerate(["Producers have", "consumers have", "consumers have", "consumers have"]):
            nth = max(0, i - 1)
            self.at(cue, nth=nth)
            n = M(NUMS[i], 30, TEXT).move_to(tiers[i])
            self.play(ReplacementTransform(outlines[i], tiers[i]), FadeIn(n), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        cx = -1.6
        tiers = [tier(cx, TIER_Y[i], TIER_W[i], TIER_C[i]) for i in range(4)]
        nums = [M(NUMS[i], 30, TEXT).move_to(tiers[i]) for i in range(4)]
        note = T("made-up numbers: units per square meter per year", 24, GREY).move_to([cx, -3.2, 0])
        self.add(*tiers, *nums, note)
        self.at("So here is the answer")
        self.play(Indicate(VGroup(*tiers), color=YELLOW, scale_factor=1.03), run_time=0.8)
        heat = []
        for i in range(4):
            xr = cx + TIER_W[i] / 2
            a = arr([xr + 0.1, TIER_Y[i], 0], [xr + 1.6, TIER_Y[i], 0], RED, w=6)
            t = T("heat", 26, RED).next_to(a, RIGHT, buff=0.15)
            heat.append(VGroup(a, t))
        self.at("At each step")
        self.play(LaggedStart(*[FadeIn(h, shift=RIGHT * 0.2) for h in heat], lag_ratio=0.3), run_time=1.6)
        self.at("changes form")
        self.play(Indicate(VGroup(*heat), color=RED, scale_factor=1.08), run_time=0.9)
        tenth = VGroup(T("roughly 1/10", 28, YELLOW), T("passes up", 28, YELLOW)).arrange(DOWN, buff=0.1).move_to([5.1, 2.2, 0])
        up = arr([5.1, -0.5, 0], [5.1, 1.5, 0], YELLOW, w=8)
        self.at("Only roughly")
        self.play(FadeIn(tenth), GrowArrow(up), run_time=0.8)
        sun = VGroup(arr([-6.2, -1.95, 0], [cx - TIER_W[0] / 2 - 0.1, -1.95, 0], YELLOW, w=7), T("sunlight", 24, YELLOW).move_to([-5.5, -1.45, 0]))
        self.at("in as sunlight")
        self.play(FadeIn(sun, shift=RIGHT * 0.2), run_time=0.7)
        self.at("out as heat")
        self.play(Indicate(VGroup(*heat), color=RED, scale_factor=1.08), run_time=0.9)
        hc = T("An energy pyramid\nis not a head count.", 26, TEXT).move_to([4.9, -3.0, 0])
        self.at("pyramid is not")
        self.play(FadeIn(hc, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "At each step, much of the energy is given off as heat."
