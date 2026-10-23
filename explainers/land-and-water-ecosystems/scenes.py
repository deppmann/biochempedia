"""Nonliving things help decide who lives where  (Biochemistrypedia explainer, grade 7 Life Science)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = biotic factors (living things)
  YELLOW = abiotic factors (sunlight, water, soil, air) and sunlight
  BLUE   = fresh water
  PURPLE = salt / salty water (salinity)
  ORANGE = oysters
  RED    = "oysters can die", very low salt, poor habitat
  TEAL   = names of kinds of ecosystem (ecosystem, estuary, brackish)
  GREY   = outlines, ground, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
RX0, RX1 = -5.8, 5.8   # river bar x range


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def river(y=0.3, h=1.5, n=28):
    """side map of the river: fresh (blue) on the left, salty (purple) on the right. Not to scale."""
    w = (RX1 - RX0) / n
    bands = VGroup(*[Rectangle(width=w + 0.01, height=h, stroke_width=0, fill_color=interpolate_color(
        ManimColor(BLUE), ManimColor(PURPLE), i / (n - 1)), fill_opacity=0.55).move_to([RX0 + w * (i + 0.5), y, 0])
        for i in range(n)])
    edge = Rectangle(width=RX1 - RX0, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([0, y, 0])
    return VGroup(bands, edge)


def reef(x, y, s=1.0):
    return VGroup(*[Ellipse(width=0.62 * s, height=0.4 * s, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                            fill_opacity=0.6).move_to([x + dx * s, y + dy * s, 0])
                    for dx, dy in ((-0.7, -0.1), (-0.05, 0.22), (0.62, -0.1), (-0.05, -0.28))])


def cross(x, y, r=0.22, color=RED):
    return VGroup(Line([x - r, y - r, 0], [x + r, y + r, 0], color=color, stroke_width=7),
                  Line([x - r, y + r, 0], [x + r, y - r, 0], color=color, stroke_width=7))


def salt_dots(cx, cy, w, h, n, seed):
    rng = np.random.default_rng(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 4000:
        tries += 1
        p = (rng.uniform(-w / 2, w / 2), rng.uniform(-h / 2, h / 2))
        if all(np.hypot(p[0] - q[0], p[1] - q[1]) > 0.38 for q in pts):
            pts.append(p)
    return VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to([cx + p[0], cy + p[1], 0])
                    for p in pts])


def plant(x, y, s=1.0):
    stem = Line([x, y, 0], [x, y + 0.45 * s, 0], color=GREEN, stroke_width=5)
    l1 = Ellipse(width=0.4 * s, height=0.2 * s, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                 fill_opacity=0.6).move_to([x - 0.22 * s, y + 0.5 * s, 0]).rotate(0.4)
    l2 = Ellipse(width=0.4 * s, height=0.2 * s, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                 fill_opacity=0.6).move_to([x + 0.22 * s, y + 0.5 * s, 0]).rotate(-0.4)
    return VGroup(stem, l1, l2)


def tree(x, y, s=1.0):
    trunk = Rectangle(width=0.22 * s, height=0.6 * s, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([x, y + 0.3 * s, 0])
    crown = Ellipse(width=1.0 * s, height=1.0 * s, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                    fill_opacity=0.5).move_to([x, y + 1.0 * s, 0])
    return VGroup(trunk, crown)


class S00Title(TitleCard):
    LESSON = "Land and water ecosystems"
    TITLE = "Nonliving things help decide who lives where"


# ---------------------------------------------------------------------------------------------
class S01River(SpokenScene):
    def construct(self):
        rv = river(-0.4, 2.0)
        mt = VGroup(*[Polygon([x - 0.9 * s, 0.6, 0], [x, 0.6 + 1.3 * s, 0], [x + 0.9 * s, 0.6, 0], stroke_color=GREY,
                              stroke_width=3, fill_color=GREY, fill_opacity=0.25)
                      for x, s in ((-5.2, 1.0), (-4.3, 0.7))])
        l_mt = T("mountains: fresh water", 30, BLUE).move_to([-3.9, -1.85, 0])
        l_bay = T("Bay mouth: salty", 30, PURPLE).move_to([4.3, -1.85, 0])
        note = T("James River, not to scale", 22, GREY).move_to([0, -3.2, 0])
        self.at("starts as fresh water")
        self.play(FadeIn(mt), LaggedStart(*[FadeIn(b) for b in rv[0]], lag_ratio=0.03), FadeIn(rv[1]), FadeIn(l_mt),
                  run_time=2.2)
        self.at("ends in the salty")
        self.play(FadeIn(l_bay, shift=LEFT * 0.2), FadeIn(note), run_time=0.7)
        rf = reef(3.0, -0.4, 1.3)
        rf_l = T("oyster reefs", 30, ORANGE).move_to([3.0, 1.2, 0])
        self.at("Wild oyster reefs")
        self.play(FadeIn(rf, scale=0.8), FadeIn(rf_l, shift=DOWN * 0.15), run_time=0.8)
        tick = Line([-2.2, -1.4, 0], [-2.2, -0.4, 0], color=GREY, stroke_width=3)
        rich = T("Richmond", 30, TEXT).move_to([-2.2, 1.1, 0])
        self.at("the water is fresh")
        self.play(FadeIn(rich, shift=DOWN * 0.15), Create(tick), run_time=0.6)
        die = chip("oysters can die", RED, size=30).move_to([-2.2, 2.1, 0])
        x_ = cross(-2.2, -0.4, 0.3)
        self.at("oysters can die")
        self.play(FadeIn(die, shift=DOWN * 0.15), Create(x_), run_time=0.7)
        q = T("Why do different living things live in\na mountain stream, a forest and the salty Bay?", 36,
              font=TITLE_FONT, line_spacing=0.9)
        fit(q, max_w=11.8)
        q.move_to([0, 2.85, 0])
        self.at("So why do")
        self.play(FadeOut(VGroup(die, rich, tick, x_, rf_l, note)), run_time=0.4)
        self.play(Write(q), run_time=2.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Living(SpokenScene):
    def construct(self):
        box = RoundedRectangle(corner_radius=0.3, width=12.2, height=5.5, stroke_color=TEAL, stroke_width=4).move_to([0, -0.5, 0])
        lab = T("ecosystem", 38, TEAL, weight=BOLD).move_to([0, 3.0, 0])
        self.at("Every place has")
        self.play(Create(box), FadeIn(lab, shift=DOWN * 0.15), run_time=1.0)
        left = Rectangle(width=6.0, height=5.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.12).move_to([-3.1, -0.5, 0])
        right = Rectangle(width=6.0, height=5.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.12).move_to([3.1, -0.5, 0])
        mid = Line([0, -3.15, 0], [0, 2.15, 0], color=GREY, stroke_width=2)
        self.at("all the living things")
        self.play(FadeIn(left), run_time=0.7)
        self.at("surroundings")
        self.play(FadeIn(right), Create(mid), run_time=0.7)
        h_b = T("biotic factors", 36, GREEN, weight=BOLD).move_to([-3.1, 1.5, 0])
        s_b = T("living things and\nhow they interact", 28, GREEN).move_to([-3.1, 0.55, 0])
        self.at("biotic factors")
        self.play(FadeIn(h_b, shift=DOWN * 0.15), FadeIn(s_b), run_time=0.7)
        ac = chip("acorns", GREEN, size=34).move_to([-4.5, -1.2, 0])
        dr = chip("deer", GREEN, size=34).move_to([-1.6, -1.2, 0])
        ar = arr(ac.get_right(), dr.get_left(), GREEN)
        self.at("A deer eating acorns")
        self.play(FadeIn(ac), FadeIn(dr), GrowArrow(ar), run_time=0.9)
        tg = T("biotic", 30, GREEN).move_to([-3.1, -2.4, 0])
        self.play(FadeIn(tg), run_time=0.3)
        h_a = T("abiotic factors", 36, YELLOW, weight=BOLD).move_to([3.1, 1.5, 0])
        s_a = T("nonliving parts", 28, YELLOW).move_to([3.1, 0.7, 0])
        self.at("parts are abiotic")
        self.play(FadeIn(h_a, shift=DOWN * 0.15), FadeIn(s_a), run_time=0.7)
        items = {"sunlight": (1.8, -0.5), "water": (4.4, -0.5), "soil": (1.8, -1.8), "air": (4.4, -1.8)}
        cs = {}
        for name, (x, y) in items.items():
            cs[name] = chip(name, YELLOW, size=34).move_to([x, y, 0])
        for name in ("sunlight", "water", "soil", "air"):
            self.at(name if name != "sunlight" else "Sunlight")
            self.play(FadeIn(cs[name], shift=UP * 0.15), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Decide(SpokenScene):
    def construct(self):
        top = chip("abiotic factor: sunlight", YELLOW, size=30).move_to([0, 3.0, 0])
        self.at("Abiotic factors help")
        self.play(FadeIn(top, shift=DOWN * 0.15), run_time=0.7)
        # left panel: forest floor
        pl = RoundedRectangle(corner_radius=0.2, width=5.9, height=5.4, stroke_color=GREY, stroke_width=2.5).move_to([-3.2, -0.3, 0])
        tl = T("forest floor", 30, TEXT).move_to([-3.2, 1.95, 0])
        sun_l = Circle(radius=0.28, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([-3.2, 1.4, 0])
        rays_l = VGroup(*[arr([x, 1.0, 0], [x, 0.45, 0], YELLOW, w=6, tip=0.2) for x in (-5.0, -4.2, -3.4, -2.6)])
        canopy = RoundedRectangle(corner_radius=0.1, width=3.9, height=0.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                                  fill_opacity=0.5).move_to([-3.95, 0.15, 0])
        cl = T("tree leaves", 22, TEXT).move_to(canopy)
        gap_ray = arr([-1.4, 0.7, 0], [-1.4, -0.9, 0], YELLOW, w=3, tip=0.16)
        ground_l = Rectangle(width=5.5, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([-3.2, -2.75, 0])
        self.at("Few plants can grow")
        self.play(FadeIn(pl), FadeIn(tl), FadeIn(sun_l), FadeIn(ground_l), FadeIn(canopy), FadeIn(cl), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(r) for r in rays_l], lag_ratio=0.15), run_time=0.8)
        self.at("little sunlight")
        self.play(GrowArrow(gap_ray), run_time=0.4)
        ls = T("little sunlight", 26, YELLOW).move_to([-4.0, -0.75, 0])
        p1 = plant(-4.0, -2.6)
        fp = T("few plants", 26, GREEN).move_to([-4.0, -1.55, 0])
        self.play(FadeIn(ls), FadeIn(p1), FadeIn(fp), run_time=0.7)
        # right panel: deep or muddy water
        pr = RoundedRectangle(corner_radius=0.2, width=5.9, height=5.4, stroke_color=GREY, stroke_width=2.5).move_to([3.2, -0.3, 0])
        tr = T("deep or muddy water", 30, TEXT).move_to([3.2, 1.95, 0])
        sun_r = Circle(radius=0.28, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([3.2, 1.4, 0])
        water = Rectangle(width=5.5, height=3.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.22).move_to([3.2, -1.1, 0])
        wl = T("water and floating mud", 22, TEXT)
        mud = RoundedRectangle(corner_radius=0.1, width=wl.width + 0.5, height=0.5, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.5).move_to([3.2, -0.15, 0])
        wl.move_to(mud)
        rays_r = VGroup(*[arr([x, 0.95, 0], [x, 0.2, 0], YELLOW, w=6, tip=0.2) for x in (1.5, 2.5, 3.5, 4.5)])
        ground_r = Rectangle(width=5.5, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([3.2, -2.75, 0])
        self.at("Water and floating mud")
        self.play(FadeIn(pr), FadeIn(tr), FadeIn(sun_r), FadeIn(water), FadeIn(ground_r), run_time=0.8)
        self.play(FadeIn(mud), FadeIn(wl), run_time=0.4)
        self.at("block light")
        self.play(LaggedStart(*[GrowArrow(r) for r in rays_r], lag_ratio=0.12), run_time=0.9)
        lr = T("little light", 26, YELLOW).move_to([3.2, -0.75, 0])
        self.play(FadeIn(lr), run_time=0.4)
        p2 = plant(3.2, -2.6)
        fp2 = T("few plants", 26, GREEN).move_to([3.2, -1.55, 0])
        self.at("few plants grow on the floor")
        self.play(FadeIn(p2), FadeIn(fp2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Three(SpokenScene):
    def construct(self):
        xs = [-4.3, 0.0, 4.3]
        names = ["terrestrial\necosystem", "freshwater\necosystem", "marine\necosystem"]
        panels = [RoundedRectangle(corner_radius=0.2, width=4.0, height=4.2, stroke_color=GREY, stroke_width=2.5)
                  .move_to([x, -0.35, 0]) for x in xs]
        heads = [chip(n, TEAL, size=28).move_to([x, 2.45, 0]) for n, x in zip(names, xs)]
        self.at("three broad groups")
        self.play(*[FadeIn(p) for p in panels], run_time=0.8)
        # terrestrial
        trees = VGroup(tree(-5.1, -1.8, 1.0), tree(-3.5, -1.8, 1.0))
        gl = Rectangle(width=3.6, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([-4.3, -2.0, 0])
        lt = T("forest", 28, TEXT).move_to([-4.3, -1.1 + 1.0, 0])
        lt.move_to([-4.3, 1.25, 0])
        self.at("terrestrial ecosystem")
        self.play(FadeIn(heads[0], shift=DOWN * 0.15), FadeIn(gl), FadeIn(trees), run_time=0.8)
        self.at("on land")
        self.play(FadeIn(lt), run_time=0.4)
        # freshwater
        w1 = Rectangle(width=3.6, height=2.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.3).move_to([0, -0.7, 0])
        d1 = salt_dots(0, -0.7, 3.2, 2.5, 2, 3)
        l1 = T("mountain stream", 28, TEXT).move_to([0, 1.25, 0])
        self.at("freshwater ecosystem")
        self.play(FadeIn(heads[1], shift=DOWN * 0.15), FadeIn(w1), run_time=0.7)
        self.at("very little salt")
        self.play(FadeIn(d1), FadeIn(l1), run_time=0.6)
        # marine
        w2 = Rectangle(width=3.6, height=2.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.3).move_to([4.3, -0.7, 0])
        d2 = salt_dots(4.3, -0.7, 3.2, 2.5, 16, 5)
        l2 = T("ocean", 28, TEXT).move_to([4.3, 1.25, 0])
        self.at("marine ecosystem")
        self.play(FadeIn(heads[2], shift=DOWN * 0.15), FadeIn(w2), run_time=0.7)
        self.at("salty ocean water")
        self.play(FadeIn(d2, lag_ratio=0.05), FadeIn(l2), run_time=0.9)
        key = VGroup(Circle(radius=0.09, stroke_width=0, fill_color=PURPLE, fill_opacity=1),
                     T("= salt (schematic, not to scale)", 24, PURPLE)).arrange(RIGHT, buff=0.15).move_to([0, -3.15, 0])
        self.at("Salinity")
        self.play(FadeIn(key), run_time=0.5)
        sal = T("salinity: the amount of salt dissolved in water", 30, PURPLE)
        fit(sal, max_w=11.8)
        sal.move_to([0, -3.15, 0])
        self.at("amount of salt")
        self.play(FadeOut(key), FadeIn(sal), Indicate(d2, color=PURPLE, scale_factor=1.05), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Estuary(SpokenScene):
    def construct(self):
        rv = river(0.1, 2.0)
        nts = T("James River, not to scale", 22, GREY).move_to([-3.4, -3.3, 0])
        self.add(nts)
        self.at("Now follow")
        self.add(rv)
        self.play(ShowPassingFlash(Line([RX0, 1.1, 0], [RX1, 1.1, 0], color=TEXT, stroke_width=8), time_width=0.5),
                  run_time=2.0)
        br = VGroup(Line([0.2, -1.25, 0], [5.8, -1.25, 0], color=TEAL, stroke_width=5),
                    Line([0.2, -1.25, 0], [0.2, -1.0, 0], color=TEAL, stroke_width=5),
                    Line([5.8, -1.25, 0], [5.8, -1.0, 0], color=TEAL, stroke_width=5))
        est = T("estuary: fresh and salty water mix", 30, TEAL, weight=BOLD).move_to([3.0, -1.8, 0])
        self.at("An estuary")
        self.play(Create(br), FadeIn(est, shift=UP * 0.15), run_time=1.0)
        fa = arr([-5.6, 2.2, 0], [-0.6, 2.2, 0], BLUE, w=7)
        fl = T("fresh river water", 28, BLUE).move_to([-3.1, 2.85, 0])
        sa = arr([5.6, 2.2, 0], [0.6, 2.2, 0], PURPLE, w=7)
        sl = T("salty ocean water", 28, PURPLE).move_to([3.1, 2.85, 0])
        self.at("fresh river water")
        self.play(GrowArrow(fa), FadeIn(fl), run_time=0.7)
        self.at("salty ocean water")
        self.play(GrowArrow(sa), FadeIn(sl), run_time=0.7)
        bay = T("Chesapeake Bay", 30, TEXT).move_to([3.0, -2.4, 0])
        self.at("The Chesapeake Bay is")
        self.play(FadeIn(bay, shift=UP * 0.15), run_time=0.6)
        mt_ = T("salinity in between fresh and salty", 26, TEAL)
        mback = RoundedRectangle(corner_radius=0.1, width=mt_.width + 0.4, height=mt_.height + 0.3, stroke_width=0,
                                 fill_color=BG, fill_opacity=0.9).move_to([3.0, 0.1, 0])
        mix = VGroup(mback, mt_.move_to(mback))
        self.at("Its salinity is in between")
        self.play(FadeIn(mix), run_time=0.5)
        sh = VGroup(arr([2.2, -2.75, 0], [0.4, -2.75, 0], GREY, w=4, tip=0.18), arr([3.8, -2.75, 0], [5.6, -2.75, 0], GREY, w=4, tip=0.18))
        shl = T("shifts with rain and season", 26, GREY).move_to([3.0, -3.05, 0])
        sh_all = VGroup(shl)
        self.at("shifts with rain")
        self.play(FadeOut(mix), FadeIn(shl), run_time=0.5)
        self.play(br.animate.shift(LEFT * 0.5), run_time=0.6)
        self.play(br.animate.shift(RIGHT * 0.5), run_time=0.6)
        self.play(br.animate.shift(RIGHT * 0.0), run_time=0.01)
        g = arr([-5.4, -1.6, 0], [-0.9, -1.6, 0], PURPLE, w=8)
        gl = T("salinity rises", 30, PURPLE, weight=BOLD).move_to([-3.2, -2.3, 0])
        self.at("salinity rises")
        self.play(GrowArrow(g), FadeIn(gl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        rv = river(0.7, 2.0)
        nts = T("James River, not to scale", 22, GREY).move_to([3.5, -3.3, 0])
        self.add(nts)
        self.add(rv)
        self.at("Now think about the oysters")
        die = chip("oysters can die if salt stays\nvery low for a long time", RED, size=26).move_to([-3.4, 2.7, 0])
        self.at("can die")
        self.play(FadeIn(die, shift=DOWN * 0.15), run_time=0.5)
        r_seg = Line([RX0, -0.45, 0], [-2.0, -0.45, 0], color=RED, stroke_width=8)
        r_lab = T("fresh water:\nvery low in salt", 28, RED, line_spacing=0.9).move_to([-3.9, -1.25, 0])
        self.at("very low in salt")
        self.play(Create(r_seg), FadeIn(r_lab), run_time=0.8)
        b_seg = Line([-0.2, -0.45, 0], [5.8, -0.45, 0], color=TEAL, stroke_width=8)
        b_lab = T("brackish: in between\nfresh and salty", 28, TEAL, line_spacing=0.9).move_to([2.8, -1.25, 0])
        self.at("Brackish water is in between")
        self.play(Create(b_seg), FadeIn(b_lab), run_time=0.8)
        rf = reef(3.0, 0.7, 1.3)
        rf_l = T("oyster reefs", 30, ORANGE).move_to([3.0, 2.6, 0])
        self.at("Oyster reefs grow")
        self.play(FadeIn(rf, scale=0.8), FadeIn(rf_l, shift=DOWN * 0.15), run_time=0.8)
        rich = T("fresh water near Richmond:\npoor oyster habitat", 28, RED, line_spacing=0.9).move_to([-3.4, -2.55, 0])
        x_ = cross(-3.9, 0.7, 0.3)
        self.at("near Richmond")
        self.play(FadeIn(rich), Create(x_), run_time=0.7)
        # the answer
        q = T("Why do different living things live in different places?", 34, font=TITLE_FONT)
        fit(q, max_w=11.8)
        q.move_to([0, 3.0, 0])
        self.at("So why do")
        self.play(FadeOut(VGroup(rv, nts, r_seg, r_lab, die, b_seg, b_lab, rf, rf_l, rich, x_)), run_time=0.6)
        self.play(Write(q), run_time=1.6)
        ab = chip("abiotic factors\nsuch as salt and sunlight", YELLOW, size=34).move_to([-3.4, 0.3, 0])
        plus = T("+", 56, TEXT).move_to([0.3, 0.3, 0])
        bi = chip("living things", GREEN, size=34).move_to([3.6, 0.3, 0])
        self.at("Abiotic factors such as")
        self.play(FadeIn(ab, shift=RIGHT * 0.2), run_time=0.6)
        self.at("together with the living")
        self.play(FadeIn(plus), FadeIn(bi, shift=LEFT * 0.2), run_time=0.7)
        dn = arr([0, -0.7, 0], [0, -1.7, 0], TEXT, w=7)
        res = chip("decide who lives in each ecosystem", TEAL, size=36).move_to([0, -2.5, 0])
        self.at("decide who lives")
        self.play(GrowArrow(dn), FadeIn(res, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Abiotic factors and living things decide who lives in each ecosystem."
