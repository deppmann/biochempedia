"""The air's nitrogen must be changed  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = nitrogen gas (the air band, the gas chips and arrows)
  YELLOW = usable nitrogen (chips and arrows)
  GREEN  = plants (corn, soybean), "plants can use"
  ORANGE = bacteria, root nodules, "other bacteria"
  PURPLE = protein and DNA
  TEAL   = sugar
  PINK   = decomposers
  BROWN  = soil and ground
  RED    = blocked / cannot use / no
  TEXT   = lightning, factory, animals, the answer
  GREY   = structure and small notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB4"
BROWN = "#A8825A"
TEAL = "#3FB8C0"
NITRO = BLUE
USABLE = YELLOW


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def ground(y_top, y_bot=-3.5, x0=-6.2, x1=6.2):
    return Rectangle(width=x1 - x0, height=y_top - y_bot, stroke_width=0, fill_color=BROWN,
                     fill_opacity=0.35).move_to([(x0 + x1) / 2, (y_top + y_bot) / 2, 0])


def leaf(x, y, w=1.1, h=0.26, ang=0.45, color=GREEN, op=0.45):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                   fill_opacity=op).rotate(ang).move_to([x, y, 0])


def corn(cx, base, h):
    stem = Line([cx, base, 0], [cx, base + h, 0], color=GREEN, stroke_width=7)
    ls = []
    for i, f in enumerate([0.30, 0.50, 0.70, 0.90]):
        s = 1 if i % 2 == 0 else -1
        ls.append(leaf(cx + s * 0.55, base + h * f + 0.1, ang=s * 0.45))
    return VGroup(stem, *ls)


def soy(cx, base, h):
    stem = Line([cx, base, 0], [cx, base + h, 0], color=GREEN, stroke_width=7)
    top = base + h
    ls = [leaf(cx - 0.45, top - 0.15, 0.8, 0.5, 0.3), leaf(cx + 0.45, top - 0.15, 0.8, 0.5, -0.3),
          leaf(cx, top + 0.3, 0.7, 0.5, 0.0),
          leaf(cx - 0.4, base + h * 0.45, 0.8, 0.5, 0.3), leaf(cx + 0.4, base + h * 0.45, 0.8, 0.5, -0.3)]
    return VGroup(stem, *ls)


def roots(cx, base, spread=0.8, depth=0.75, color=BROWN):
    return VGroup(*[Line([cx, base, 0], [cx + dx, base - depth, 0], color=color, stroke_width=3)
                    for dx in (-spread, 0.0, spread)])


def bact(x, y, ang=0.0, s=1.0):
    return RoundedRectangle(corner_radius=0.1 * s, width=0.42 * s, height=0.2 * s, stroke_color=ORANGE,
                            stroke_width=2, fill_color=ORANGE, fill_opacity=0.5).rotate(ang).move_to([x, y, 0])


def air_band(y=3.0, w=11.0, h=0.9, label="nitrogen gas", size=30):
    box = Rectangle(width=w, height=h, stroke_color=NITRO, stroke_width=3, fill_color=NITRO,
                    fill_opacity=0.16).move_to([0, y, 0])
    return VGroup(box, T(label, size, NITRO, weight=BOLD).move_to([0, y, 0]))


def gas_chip(x, y, size=26):
    return chip("nitrogen gas", NITRO, size=size).move_to([x, y, 0])


def use_chip(x, y, size=26, text="usable nitrogen"):
    return chip(text, USABLE, size=size).move_to([x, y, 0])


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Nitrogen for Life"
    TITLE = "The air's nitrogen must be changed"


# =============================================================================================
class S01Question(SpokenScene):
    def construct(self):
        bx0 = -5.5
        outline = Rectangle(width=11, height=0.85, stroke_color=GREY, stroke_width=3).move_to([0, 3.0, 0])
        fill = Rectangle(width=11 * 0.78, height=0.85, stroke_width=0, fill_color=NITRO, fill_opacity=0.35)
        fill.move_to([bx0 + 11 * 0.78 / 2, 3.0, 0])
        lab = T("about 78 percent nitrogen", 28, NITRO, weight=BOLD).move_to(fill)
        airl = T("air", 26, GREY).move_to([bx0 + 11 * 0.89, 3.0, 0])
        g = ground(-1.7)
        corn_p = corn(-3.2, -1.7, 2.9)
        corn_r = roots(-3.2, -1.7)
        corn_l = T("corn", 28, GREEN, weight=BOLD).move_to([-3.2, 1.65, 0])
        soy_p = soy(3.2, -1.7, 1.9)
        soy_r = roots(3.2, -1.7)
        nods = VGroup(*[Circle(radius=0.11, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE,
                               fill_opacity=0.6).move_to([3.2 + dx, -2.25 + dy, 0])
                        for dx, dy in [(-0.8, 0.0), (0.0, 0.0), (0.8, 0.0)]])
        soy_l = T("soybeans", 28, GREEN, weight=BOLD).move_to([3.2, 0.95, 0])
        added = use_chip(-3.2, -2.9, 24, "added nitrogen")
        rb = chip("root bacteria", ORANGE, size=24).move_to([0.7, -2.15, 0])
        little = chip("little or no added nitrogen", USABLE, size=22).move_to([3.2, -3.0, 0])
        little[0].set_stroke(opacity=0.5)
        self.play(FadeIn(outline), run_time=0.4)
        self.play(FadeIn(fill), FadeIn(lab), FadeIn(airl), run_time=0.8)
        self.at("is about")
        self.wait(0.1)
        self.at("corn farmers")
        self.play(FadeIn(g), FadeIn(corn_p), FadeIn(corn_r), FadeIn(corn_l), run_time=0.8)
        self.at("add nitrogen")
        self.play(FadeIn(added, shift=DOWN * 0.3), run_time=0.7)
        self.at("Soybeans next door")
        self.play(FadeIn(soy_p), FadeIn(soy_r), FadeIn(soy_l), run_time=0.7)
        self.at("root bacteria")
        self.play(FadeIn(nods), FadeIn(rb), run_time=0.6)
        self.at("little or none")
        self.play(FadeIn(little), run_time=0.6)
        self.at("So here is")
        q = VGroup(T("Why give", 34, TEXT, weight=BOLD), T("plants nitrogen?", 34, TEXT, weight=BOLD)).arrange(DOWN, buff=0.15)
        q.move_to([-0.15, 0.5, 0])
        self.at("Why do farmers")
        self.play(FadeIn(q, scale=0.8), run_time=0.6)
        self.finish()


# =============================================================================================
class S02Need(SpokenScene):
    def construct(self):
        plant = VGroup(corn(0.0, -3.4, 3.0))
        ask = chip("nitrogen ?", USABLE, size=32).move_to([3.4, -1.9, 0])
        self.at("Why does a plant")
        self.play(FadeIn(plant), FadeIn(ask), run_time=0.8)
        # protein block
        pr = chip("protein", PURPLE, size=36).move_to([-3.4, 2.7, 0])
        prn = T("builds cells, does much of their work", 22, GREY).move_to([-3.4, 2.0, 0])
        pn = use_chip(-3.4, 1.2, 26, "nitrogen inside")
        dn = chip("DNA", PURPLE, size=36).move_to([3.4, 2.7, 0])
        dnn = T("carries the instructions", 22, GREY).move_to([3.4, 2.0, 0])
        dnn2 = use_chip(3.4, 1.2, 26, "nitrogen inside")
        self.at("A protein")
        self.play(FadeIn(pr, scale=0.8), run_time=0.5)
        self.at("builds cells")
        self.play(FadeIn(prn), run_time=0.5)
        self.at("Proteins contain")
        self.play(FadeIn(pn, shift=UP * 0.2), run_time=0.6)
        self.at("instructions")
        self.play(FadeIn(dn, scale=0.8), FadeIn(dnn), run_time=0.6)
        self.at("contains nitrogen too")
        self.play(FadeIn(dnn2, shift=UP * 0.2), run_time=0.6)
        self.at("new leaves")
        ghost = leaf(0.6, -0.05, 1.2, 0.3, 0.45, RED, 0.0)
        ghost.set_stroke(opacity=0.9)
        gd = DashedVMobject(ghost, num_dashes=14)
        no = VGroup(T("no nitrogen:", 30, RED, weight=BOLD), T("no new leaves", 30, RED, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([3.4, -1.9, 0])
        self.play(Create(gd), ReplacementTransform(ask, no), run_time=0.9)
        self.finish()


# =============================================================================================
class S03Gas(SpokenScene):
    def construct(self):
        air = air_band(2.9)
        g = ground(-2.5)
        plant = corn(0.0, -2.5, 3.0)
        r = roots(0.0, -2.5, 0.8, 0.6)
        self.at("Here is the puzzle")
        self.play(FadeIn(g), FadeIn(plant), FadeIn(r), run_time=0.7)
        self.at("is a gas")
        self.play(FadeIn(air), run_time=0.7)
        self.at("cannot use")
        a = arr([0, 2.25, 0], [0, 0.85, 0], NITRO, w=7, tip=0.28)
        x1 = Line([-0.4, 1.8, 0], [0.4, 1.0, 0], color=RED, stroke_width=9)
        x2 = Line([-0.4, 1.0, 0], [0.4, 1.8, 0], color=RED, stroke_width=9)
        no = VGroup(T("most living things", 26, RED, weight=BOLD), T("cannot use this form", 26, RED, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([3.0, 1.4, 0])
        self.play(GrowArrow(a), run_time=0.5)
        self.play(Create(x1), Create(x2), FadeIn(no), run_time=0.5)
        self.at("Corn can stand")
        cornl = T("corn", 30, GREEN, weight=BOLD).move_to([1.4, -0.6, 0])
        self.play(FadeIn(cornl), run_time=0.4)
        self.at("still run short")
        short = VGroup(T("still runs short of", 28, USABLE), T("usable nitrogen", 28, USABLE)).arrange(DOWN, buff=0.1).move_to([-3.2, 0.1, 0])
        self.play(FadeIn(short), run_time=0.5)
        self.at("must first be changed")
        self.play(*[FadeOut(m) for m in (air, g, plant, r, a, x1, x2, no, short, cornl)], run_time=0.6)
        gc = gas_chip(-4.7, 1.0, 30)
        box = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.5, stroke_color=GREY, stroke_width=3,
                               stroke_opacity=1.0)
        box = DashedVMobject(box, num_dashes=30).move_to([0, 1.0, 0])
        q = T("changed?", 34, TEXT, weight=BOLD).move_to([0, 1.0, 0])
        a1 = arr([-3.3, 1.0, 0], [-1.55, 1.0, 0], GREY, w=6)
        a2 = arr([1.55, 1.0, 0], [2.7, 1.0, 0], GREY, w=6)
        uc = use_chip(4.5, 1.0, 30)
        self.play(FadeIn(gc), FadeIn(box), FadeIn(q), FadeIn(a1), FadeIn(a2), run_time=0.8)
        self.play(FadeIn(uc, shift=RIGHT * 0.3), run_time=0.6)
        self.at("Plants can use")
        pl = T("plants can use this", 26, GREEN, weight=BOLD).move_to([4.5, 0.2, 0])
        cn = VGroup(T("most living things", 26, RED, weight=BOLD), T("cannot use this", 26, RED, weight=BOLD)).arrange(DOWN, buff=0.08).move_to([-4.7, 0.05, 0])
        pa = arr([4.5, -0.2, 0], [4.5, -0.85, 0], USABLE, w=6, tip=0.2)
        pp = corn(4.5, -3.4, 2.4)
        self.play(FadeIn(cn), FadeIn(pl), run_time=0.5)
        self.play(GrowArrow(pa), FadeIn(pp), run_time=0.7)
        self.finish()


# =============================================================================================
class S04Changers(SpokenScene):
    def construct(self):
        air = air_band(3.0, 11.0, 0.8, size=28)
        g = ground(-0.6)
        # bacteria in soil
        bs = VGroup(*[bact(-4.2 + dx, -1.2 + dy, a) for dx, dy, a in
                      [(-0.5, 0.1, 0.4), (0.0, 0.25, -0.3), (0.5, 0.05, 0.2), (-0.2, -0.2, -0.5), (0.3, -0.25, 0.6)]])
        bl = T("bacteria", 26, ORANGE, weight=BOLD).move_to([-4.2, -1.8, 0])
        bu = use_chip(-4.2, -2.85, 24)
        ba1 = arr([-4.2, 2.55, 0], [-4.2, -0.85, 0], NITRO, w=6, tip=0.25)
        ba2 = arr([-4.2, -2.05, 0], [-4.2, -2.52, 0], USABLE, w=6, tip=0.18)
        # lightning
        bolt = Polygon([0.15, 2.5, 0], [-0.35, 1.6, 0], [-0.02, 1.6, 0], [-0.3, 0.75, 0], [0.4, 1.85, 0],
                       [0.05, 1.85, 0], stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.5)
        ll = T("lightning", 26, TEXT, weight=BOLD).move_to([1.5, 1.6, 0])
        la = arr([0, 0.55, 0], [0, -2.45, 0], USABLE, w=6, tip=0.25)
        lu = use_chip(0.0, -2.85, 24)
        # factory
        body = Rectangle(width=1.5, height=1.0, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                         fill_opacity=0.2).move_to([4.2, -0.1, 0])
        chim = Rectangle(width=0.3, height=0.7, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                         fill_opacity=0.2).move_to([4.7, 0.65, 0])
        fl = T("factory", 26, TEXT, weight=BOLD).move_to([4.2, 1.3, 0])
        fa1 = arr([4.2, 2.55, 0], [4.2, 1.7, 0], NITRO, w=6, tip=0.25)
        fa2 = arr([4.2, -0.6, 0], [4.2, -2.45, 0], USABLE, w=6, tip=0.25)
        fu = use_chip(4.2, -2.85, 24)
        fert = T("fertilizer", 24, USABLE, weight=BOLD)
        fert2 = T("added by farmers", 22, GREY)
        fert2 = VGroup(T("added by", 22, GREY), T("farmers", 22, GREY)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        fg = VGroup(fert, fert2).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([5.3, -1.5, 0])
        fg.align_to([4.5, 0, 0], LEFT)
        self.at("Bacteria, lightning")
        self.play(FadeIn(air), FadeIn(g), run_time=0.7)
        self.at("tiny living things")
        self.play(FadeIn(bs), FadeIn(bl), run_time=0.8)
        self.at("live free in the soil")
        self.play(GrowArrow(ba1), run_time=0.6)
        self.at("usable form")
        self.play(GrowArrow(ba2), FadeIn(bu), run_time=0.7)
        self.at("Lightning changes")
        self.play(FadeIn(bolt, scale=0.7), FadeIn(ll), run_time=0.3)
        self.play(GrowArrow(la), FadeIn(lu), run_time=0.6)
        self.at("factories that make fertilizer")
        self.play(FadeIn(body), FadeIn(chim), FadeIn(fl), GrowArrow(fa1), run_time=0.7)
        self.play(GrowArrow(fa2), FadeIn(fu), run_time=0.6)
        self.at("farmers add")
        self.play(FadeIn(fg), run_time=0.6)
        self.finish()


# =============================================================================================
class S05Partners(SpokenScene):
    def construct(self):
        TOP = -0.2
        g = ground(TOP)
        sp = soy(-3.5, TOP, 2.0)
        sl = T("soybean", 28, GREEN, weight=BOLD).move_to([-3.5, 3.2, 0])
        N1, N2 = np.array([-4.9, -1.75, 0]), np.array([-2.1, -1.75, 0])
        base = np.array([-3.5, TOP, 0])
        def edge(c):
            v = (base - c) / np.linalg.norm(base - c)
            return c + v * 0.6
        r1 = Line(base, edge(N1), color=BROWN, stroke_width=4)
        r2 = Line(base, edge(N2), color=BROWN, stroke_width=4)

        def nodule(c, rad):
            circ = Circle(radius=rad, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                          fill_opacity=0.15).move_to(c)
            ds = VGroup(*[bact(c[0] + dx * rad, c[1] + dy * rad, a, 0.8) for dx, dy, a in
                          [(-0.3, 0.25, 0.3), (0.3, 0.3, -0.4), (0.0, -0.3, 0.5), (-0.35, -0.2, -0.2)]])
            return VGroup(circ, ds)
        n1 = nodule(N1, 0.6)
        n2 = nodule(N2, 0.6)
        nl = T("root nodule", 28, ORANGE, weight=BOLD).move_to([-2.1, -2.85, 0])
        d = (N2 - base) / np.linalg.norm(N2 - base)
        perp = np.array([d[1] * -1, d[0], 0.0])  # points up-right
        perp = perp if perp[1] > 0 else -perp
        L = np.linalg.norm(N2 - base) - 0.6
        p0, p1 = base + d * 0.35, base + d * (L - 0.1)
        sug = arr(p0 - perp * 0.28, p1 - perp * 0.28, TEAL, w=7, tip=0.22)
        usa = arr(p1 + perp * 0.28, p0 + perp * 0.28, USABLE, w=7, tip=0.22)
        sugl = T("sugar", 26, TEAL, weight=BOLD).move_to([-3.75, -1.6, 0])
        usal = T("usable nitrogen", 28, USABLE, weight=BOLD).move_to([-1.0, -0.65, 0])
        # corn
        cp = corn(3.8, TOP, 2.4)
        cr = roots(3.8, TOP, 0.9, 1.2)
        cl = T("corn", 28, GREEN, weight=BOLD).move_to([3.8, 3.2, 0])
        no = T("no root nodules", 28, RED, weight=BOLD).move_to([3.8, 2.75, 0])
        sc = use_chip(3.8, -2.85, 24, "usable nitrogen\nin the soil")
        ca = arr([3.8, -2.3, 0], [3.8, -1.5, 0], USABLE, w=7, tip=0.22)
        self.at("A root nodule")
        self.play(FadeIn(g), FadeIn(sp), FadeIn(sl), Create(r1), Create(r2), run_time=0.8)
        self.play(FadeIn(n2, scale=0.6), FadeIn(n1, scale=0.6), FadeIn(nl), run_time=0.7)
        self.at("Beans, peas")
        self.wait(0.1)
        self.at("Bacteria live inside")
        self.play(Indicate(n2, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.at("sends sugar")
        self.play(GrowArrow(sug), FadeIn(sugl), run_time=0.7)
        self.at("give the plant usable")
        self.play(GrowArrow(usa), FadeIn(usal), run_time=0.7)
        self.play(Indicate(usa, color=USABLE, scale_factor=1.35), run_time=0.8)
        self.play(Indicate(usa, color=USABLE, scale_factor=1.35), run_time=0.8)
        self.at("Corn has no")
        self.play(FadeIn(cp), FadeIn(cr), FadeIn(cl), FadeIn(no), run_time=0.8)
        self.at("already in the soil")
        self.play(FadeIn(sc, shift=UP * 0.2), GrowArrow(ca), run_time=0.7)
        self.finish()


# =============================================================================================
class S06Loop(SpokenScene):
    def construct(self):
        air = gas_chip(-0.3, 2.8, 28)
        soil = chip("usable nitrogen\nin the soil", USABLE, size=22).move_to([4.6, 0.6, 0])
        plants = chip("plants", GREEN, size=28).move_to([3.0, -2.5, 0])
        animals = chip("animals", TEXT, size=28).move_to([-3.0, -2.5, 0])
        dec = chip("decomposers", PINK, size=28).move_to([-4.6, 0.9, 0])
        decl = T("break down dead things and wastes", 22, GREY).move_to([-3.9, 0.15, 0])
        a_air = arr([1.2, 2.4, 0], [3.9, 1.3, 0], TEXT, w=5, tip=0.2)
        a_up = arr([4.3, -0.2, 0], [3.4, -2.05, 0], GREEN, w=6, tip=0.2)
        a_eat = arr([2.1, -2.5, 0], [-2.0, -2.5, 0], TEXT, w=6, tip=0.2)
        eat = T("eating", 24, TEXT).move_to([0, -2.05, 0])
        a_dec = arr([-3.2, 0.9, 0], [3.0, 0.9, 0], PINK, w=6, tip=0.2)
        dl = T("returned to the soil", 24, PINK).move_to([-0.1, 1.35, 0])
        a_back = arr([5.0, 1.05, 0], [1.0, 3.0, 0], ORANGE, w=6, tip=0.2)
        ob = T("other bacteria", 24, ORANGE, weight=BOLD).move_to([4.3, 2.65, 0])
        self.add(air, soil, a_air)
        self.at("Plant roots")
        self.play(FadeIn(plants), GrowArrow(a_up), run_time=0.8)
        self.at("Animals get")
        self.play(FadeIn(animals), GrowArrow(a_eat), FadeIn(eat), run_time=0.8)
        self.at("Decomposers break")
        self.play(FadeIn(dec), FadeIn(decl), run_time=0.7)
        self.at("return the nitrogen")
        self.play(GrowArrow(a_dec), FadeIn(dl), run_time=0.7)
        self.at("Other bacteria")
        self.play(GrowArrow(a_back), FadeIn(ob), run_time=0.8)
        self.at("is the nitrogen cycle")
        cyc = T("the nitrogen cycle", 34, TEXT, weight=BOLD).move_to([0, -1.0, 0])
        self.play(FadeIn(cyc), run_time=0.6)
        self.at("So corn")
        allm = [air, soil, plants, animals, dec, decl, a_air, a_up, a_eat, eat, a_dec, dl, a_back, ob]
        card = VGroup(T("Corn cannot use nitrogen gas.", 28, TEXT, weight=BOLD),
                      T("It depends on usable", 28, USABLE, weight=BOLD),
                      T("nitrogen in the soil.", 28, USABLE, weight=BOLD)).arrange(DOWN, buff=0.15)
        card.move_to([0, -1.0, 0])
        self.play(*[m.animate.set_opacity(0.25) for m in allm], ReplacementTransform(cyc, card), run_time=0.8)
        self.finish()


# =============================================================================================
class S07End(EndCard):
    LINE = "Corn cannot use nitrogen gas. It depends on usable nitrogen in soil."
