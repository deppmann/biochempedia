"""The Chesapeake Under Pressure: bacteria, not fertilizer, use the oxygen  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  ORANGE = nutrients (nitrogen, phosphorus, fertilizer)
  GREEN  = living algae and the algal bloom
  GREY   = water layers, land, dead algae, structure
  PURPLE = bacteria (decomposers)
  BLUE   = dissolved oxygen
  RED    = low oxygen, harm, "no"
  YELLOW = sunlight
  TEAL   = underwater grass
  LIME   = a fix (forest buffer, cover crops, wastewater upgrade, oyster reef)
  GOLD   = the vocabulary word on screen
  TEXT   = animals (crab, fish)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
LIME = "#B8D83A"
NUT, ALGAE, BACT, OXY, LOW, SUNC, GRASS, FIX = ORANGE, GREEN, PURPLE, BLUE, RED, YELLOW, TEAL, LIME

LX0, LX1 = -6.3, -2.2      # land
BX0, BX1 = -2.2, 6.3       # bay
TOP, SPLIT, BOT = 1.2, -0.55, -3.2


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rect(x0, x1, y0, y1, color=GREY, fo=0.0, sw=3):
    return Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=color, stroke_width=sw,
                     fill_color=color, fill_opacity=fo).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def stage():
    land = rect(LX0, LX1, BOT, TOP, GREY, 0.18)
    fresh = rect(BX0, BX1, SPLIT, TOP, GREY, 0.10)
    salty = rect(BX0, BX1, BOT, SPLIT, GREY, 0.30)
    land_l = T("land", 22, GREY).move_to([(LX0 + LX1) / 2, -2.9, 0])
    note = T("side view, not to scale", 22, GREY).move_to([-4.2, -3.55, 0])
    g = VGroup(land, fresh, salty, land_l, note)
    g.land, g.fresh, g.salty = land, fresh, salty
    return g


def bchip(text, color, size=24):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dots(n, color, x0, x1, y0, y1, seed, r=0.1, fo=1.0):
    rs = np.random.RandomState(seed)
    out = VGroup()
    for _ in range(n):
        out.add(Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fo)
                .move_to([rs.uniform(x0, x1), rs.uniform(y0, y1), 0]))
    return out


def algae(n=24, seed=3):
    return dots(n, ALGAE, BX0 + 0.3, BX1 - 0.3, SPLIT + 0.2, TOP - 0.2, seed, r=0.13, fo=0.85)


def dead(n=24, seed=3):
    rs = np.random.RandomState(seed + 1)
    out = VGroup()
    for _ in range(n):
        out.add(Circle(radius=0.12, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.8)
                .move_to([rs.uniform(BX0 + 0.3, 4.4), rs.uniform(BOT + 0.15, BOT + 0.65), 0]))
    return out


def grass_shelf(lines=9):
    shelf = rect(4.7, BX1, BOT, -2.4, GREY, 0.5)
    gr = VGroup(*[Line([4.85 + i * 0.17, -2.4, 0], [4.85 + i * 0.17, -1.85 + 0.12 * (i % 3), 0],
                       color=GRASS, stroke_width=5) for i in range(lines)])
    return VGroup(shelf, gr)


def sun_group():
    sun = Circle(radius=0.3, stroke_color=SUNC, stroke_width=3, fill_color=SUNC, fill_opacity=0.9).move_to([5.0, 3.05, 0])
    lab = T("sunlight", 22, SUNC).move_to([3.7, 3.05, 0])
    rays = VGroup(*[arr([x, 2.6, 0], [x, 1.3, 0], SUNC, w=4) for x in (4.3, 5.0, 5.7)])
    return sun, lab, rays


class S00Title(TitleCard):
    LESSON = "The Chesapeake Under Pressure"
    TITLE = "Bacteria, Not Fertilizer, Use the Oxygen"


class BayScene(SpokenScene):
    _term = None

    def set_term(self, word, gloss="", rt=0.5):
        new = VGroup(chip(word, GOLD, size=38).move_to([0, 3.0, 0]))
        if gloss:
            new.add(T(gloss, 22, GREY).move_to([0, 2.2, 0]))
        old, self._term = self._term, new
        if old is None:
            self.play(FadeIn(new, shift=DOWN * 0.15), run_time=rt)
        else:
            self.play(FadeOut(old), FadeIn(new, shift=DOWN * 0.15), run_time=rt)

    def clear_term(self, rt=0.4):
        if self._term is not None:
            self.play(FadeOut(self._term), run_time=rt)
            self._term = None


# ---------------------------------------------------------------------------------------------
class S01Question(BayScene):
    def construct(self):
        st = stage()
        self.play(FadeIn(st), run_time=0.8)
        lab = T("deep channel, bottom water", 24, GREY).move_to([1.9, -1.9, 0])
        fish = bchip("fish", TEXT, 24).move_to([0.4, -2.6, 0])
        crab = bchip("crab", TEXT, 24).move_to([3.3, -2.7, 0])
        self.add(lab)
        self.add(fish, crab)
        self.at("too little oxygen")
        o = dots(3, OXY, -1.5, 4.0, -2.9, -1.6, 7, r=0.1)
        low = T("too little oxygen", 30, LOW, weight=BOLD).move_to([1.9, -0.95, 0])
        self.play(st.salty.animate.set_fill(LOW, 0.28), FadeOut(lab), FadeIn(o), FadeIn(low), run_time=0.8)
        self.at("cannot stay")
        self.play(fish.animate.move_to([1.2, 0.3, 0]), crab.animate.move_to([3.6, 0.3, 0]), run_time=1.2)
        self.at("dead zone")
        dz = T("dead zone", 44, LOW, weight=BOLD).move_to([1.9, 2.9, 0])
        self.play(FadeIn(dz, shift=DOWN * 0.15), run_time=0.5)
        self.at("no one pours")
        chem = bchip("chemical that soaks up oxygen", LOW, 24).move_to([1.9, 1.95, 0])
        x1 = Line(chem.get_corner(UL), chem.get_corner(DR), color=LOW, stroke_width=4)
        x2 = Line(chem.get_corner(UR), chem.get_corner(DL), color=LOW, stroke_width=4)
        self.play(FadeIn(chem, shift=DOWN * 0.1), run_time=0.6)
        self.play(Create(x1), Create(x2), run_time=0.4)
        self.at("fertilizer")
        fert = bchip("fertilizer", NUT, 24).move_to([-4.2, 0.6, 0])
        self.play(FadeOut(VGroup(chem, x1, x2, dz)), FadeIn(fert, shift=RIGHT * 0.2), run_time=0.7)
        self.at("James River")
        q = T("?", 64, GOLD, weight=BOLD).move_to([-1.2, 2.1, 0])
        a1 = arr(fert.get_top() + UP * 0.05, q.get_left() + LEFT * 0.05, NUT)
        a2 = arr(q.get_bottom() + DOWN * 0.05, [-0.6, -1.7, 0], NUT)
        self.play(GrowArrow(a1), FadeIn(q), run_time=0.6)
        self.play(GrowArrow(a2), run_time=0.6)
        self.at("fix it")
        fx = T("Can people fix it?", 42, GOLD, weight=BOLD).move_to([2.9, 2.8, 0])
        self.play(FadeIn(fx, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Land(BayScene):
    def construct(self):
        st = stage()
        self.add(st)
        self.at("A watershed")
        self.set_term("watershed", "all the land that drains to the Bay")
        ol = DashedVMobject(rect(LX0, LX1, BOT, TOP, GOLD, 0, 5), num_dashes=40)
        drains = VGroup(*[arr([-3.2, y, 0], [-2.3, y, 0], GOLD, w=5, tip=0.18) for y in (0.6, -0.2, -1.0, -1.8)])
        self.play(Create(ol), run_time=0.7)
        self.at("drains into")
        self.play(LaggedStart(*[GrowArrow(a) for a in drains], lag_ratio=0.2), run_time=0.8)
        self.at("Runoff")
        self.set_term("runoff", "rainwater flowing over the ground")
        rain = VGroup(*[Line([x, 2.15, 0], [x - 0.25, 1.75, 0], color=GREY, stroke_width=4) for x in np.linspace(-6.0, -2.8, 9)])
        runoff = arr([-6.0, 1.5, 0], [-1.4, 1.5, 0], GREY, w=7)
        self.play(FadeOut(VGroup(ol, drains)), run_time=0.4)
        self.at("rainwater")
        self.play(FadeIn(rain, shift=DOWN * 0.2), run_time=0.5)
        self.at("over the ground")
        self.play(GrowArrow(runoff), run_time=0.6)
        self.at("carries what")
        bits = [Square(side_length=0.14, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([-5.8 + 0.3 * i, 1.5, 0]) for i in range(5)]
        self.add(*bits)
        self.play(LaggedStart(*[b.animate.move_to([-1.6 + 0.3 * i, 0.6 - 0.1 * i, 0]) for i, b in enumerate(bits)], lag_ratio=0.15), run_time=1.2)
        self.play(*[b.animate.set_opacity(0) for b in bits], run_time=0.4)
        srcs = [("farms", 0.6), ("lawns", -0.4), ("wastewater plant", -1.4)]
        chips = {}

        def emit(name, n=4):
            c = chips[name]
            ds = [Circle(radius=0.1, stroke_color=NUT, stroke_width=2, fill_color=NUT, fill_opacity=1)
                  .move_to(c.get_right() + RIGHT * 0.1) for _ in range(n)]
            rs = np.random.RandomState(abs(hash(name)) % 1000)
            anims = []
            for d in ds:
                tx, ty = rs.uniform(-1.8, 4.5), rs.uniform(-0.3, 0.95)
                anims.append(Succession(d.animate.move_to([-3.0, 1.5, 0]), d.animate.move_to([tx, ty, 0])))
            return ds, anims
        allds = VGroup()
        self.at("farms")
        for name, y in srcs:
            chips[name] = bchip(name, GREY, 22).move_to([-4.3, y, 0])
        for k, (name, y) in enumerate(srcs):
            self.at(["farms", "lawns", "wastewater plants"][k])
            ds, an = emit(name)
            allds.add(*ds)
            self.play(FadeIn(chips[name], shift=RIGHT * 0.2), FadeIn(VGroup(*ds), run_time=0.1), LaggedStart(*an, lag_ratio=0.1), run_time=0.7)
        self.at("even the air")
        air = bchip("air", GREY, 24).move_to([-4.9, 2.8, 0])
        ds = [Circle(radius=0.1, stroke_color=NUT, stroke_width=2, fill_color=NUT, fill_opacity=1).move_to([-4.2, 2.6, 0]) for _ in range(3)]
        rs = np.random.RandomState(11)
        self.play(FadeIn(air, shift=DOWN * 0.1), run_time=0.3)
        self.add(*ds)
        self.play(LaggedStart(*[d.animate.move_to([rs.uniform(-1.5, 2.5), rs.uniform(-0.3, 0.95), 0]) for d in ds], lag_ratio=0.15), run_time=1.0)
        allds.add(*ds)
        self.at("A nutrient")
        self.set_term("nutrient", "living things need it to grow")
        self.play(Indicate(allds, color=NUT, scale_factor=1.5), run_time=0.8)
        self.at("nitrogen")
        n1 = bchip("nitrogen", NUT, 28).move_to([0.6, 1.7, 0])
        self.play(FadeIn(n1, shift=DOWN * 0.1), FadeOut(self._term[1]), run_time=0.4)
        self.at("phosphorus")
        n2 = bchip("phosphorus", NUT, 28).move_to([3.4, 1.7, 0])
        self.play(FadeIn(n2, shift=DOWN * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def nut_dots(seed=5):
    return dots(14, NUT, BX0 + 0.3, BX1 - 0.3, SPLIT + 0.2, TOP - 0.2, seed, r=0.1)


class S03Bloom(BayScene):
    def construct(self):
        st = stage()
        self.add(st)
        shelf = grass_shelf()
        self.add(shelf)
        nd = nut_dots()
        self.add(nd)
        self.at("Extra nutrients")
        cn = bchip("extra nutrients", NUT, 28).move_to([-1.3, 2.9, 0])
        more = nut_dots(9)
        self.play(FadeIn(cn, shift=DOWN * 0.1), FadeIn(more), run_time=0.6)
        self.at("grow fast")
        al = algae(24)
        self.play(LaggedStart(*[FadeIn(a, scale=0.3) for a in al[:6]], lag_ratio=0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(a, scale=0.3) for a in al[6:]], lag_ratio=0.05), run_time=0.9)
        self.at("algal bloom")
        self.play(FadeOut(cn), run_time=0.2)
        self.set_term("algal bloom", "sudden, thick growth of algae")
        self.play(st.fresh.animate.set_fill(ALGAE, 0.30), run_time=0.7)
        self.at("blocks sunlight")
        sun, sl, rays = sun_group()
        self.play(FadeIn(sun), FadeIn(sl), LaggedStart(*[GrowArrow(r) for r in rays], lag_ratio=0.15), run_time=0.9)
        blocked = VGroup(*[Line([x - 0.2, 1.27, 0], [x + 0.2, 1.27, 0], color=LOW, stroke_width=8) for x in (4.3, 5.0, 5.7)])
        bl = T("light blocked", 22, LOW).move_to([2.7, 1.75, 0])
        self.play(Create(blocked), FadeIn(bl), run_time=0.4)
        self.at("from underwater")
        gl = T("underwater grass", 22, GRASS).move_to([4.95, -1.4, 0])
        self.play(FadeIn(gl), shelf[1].animate.set_opacity(0.3), run_time=0.7)
        self.at("die and sink")
        dd = dead(24)
        self.play(FadeOut(VGroup(sun, sl, rays, blocked, bl)), st.fresh.animate.set_fill(GREY, 0.10), run_time=0.5)
        self.play(*[Transform(a, d) for a, d in zip(al, dd)], run_time=1.6)
        dl = T("dead algae", 22, GREY).move_to([1.7, -3.55, 0])
        self.play(FadeIn(dl), FadeOut(gl), run_time=0.3)
        self.at("A decomposer")
        self.set_term("decomposer", "breaks down dead matter")
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Oxygen(BayScene):
    def construct(self):
        st = stage()
        self.add(st)
        shelf = grass_shelf()
        shelf[1].set_opacity(0.3)
        self.add(shelf)
        dd = dead(24)
        self.add(dd)
        self.add(T("dead algae", 22, GREY).move_to([1.7, -3.55, 0]))
        self.at("Bacteria decompose")
        bs = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.34, height=0.2, stroke_color=BACT, stroke_width=2,
                                       fill_color=BACT, fill_opacity=0.9).move_to([x, BOT + 0.38, 0])
                      for x in (-1.6, -0.3, 1.0, 2.3, 3.6)])
        bl = T("bacteria", 26, BACT, weight=BOLD).move_to([-1.1, -0.95, 0])
        self.play(FadeIn(bs, scale=0.4), FadeIn(bl), run_time=0.7)
        self.play(*[d.animate.scale(0.5) for d in dd[::2]], run_time=0.8)
        self.at("use oxygen")
        xs = dots(9, OXY, -1.8, 4.2, -2.5, -1.4, 21, r=0.1)
        ol = T("oxygen", 26, OXY, weight=BOLD).move_to([3.0, -0.95, 0])
        self.play(FadeIn(xs), FadeIn(ol), run_time=0.5)
        bpos = [b.get_center() for b in bs]
        movers = [x.animate.move_to(bpos[i % 5] + UP * 0.25).set_opacity(0) for i, x in enumerate(xs[:7])]
        self.play(LaggedStart(*movers, lag_ratio=0.1), run_time=1.3)
        self.at("Dissolved oxygen")
        self.play(FadeOut(ol), run_time=0.2)
        self.set_term("dissolved oxygen", "oxygen gas mixed into water")
        self.play(Indicate(xs[7:], color=OXY, scale_factor=2.0), run_time=0.8)
        self.at("Fish and crabs")
        fish = bchip("fish", TEXT, 24).move_to([-1.2, -1.6, 0])
        crab = bchip("crab", TEXT, 24).move_to([3.2, -2.2, 0])
        self.play(FadeIn(fish), FadeIn(crab), run_time=0.5)
        self.at("through their gills")
        g1 = arr(xs[7].get_center(), fish.get_right(), OXY, w=4)
        g2 = arr(xs[8].get_center(), crab.get_left(), OXY, w=4)
        gl = T("gills", 22, OXY).move_to([-1.2, -2.2, 0])
        self.play(GrowArrow(g1), GrowArrow(g2), FadeIn(gl), run_time=0.7)
        self.at("hypoxia")
        self.play(FadeOut(VGroup(g1, g2, gl)), st.salty.animate.set_fill(LOW, 0.28), run_time=0.4)
        self.set_term("hypoxia", "low oxygen in the water")
        self.at("swim away leave")
        lo = T("low oxygen", 28, LOW, weight=BOLD).move_to([1.5, -0.95, 0])
        self.play(FadeIn(lo), fish.animate.move_to([-0.6, 0.2, 0]), run_time=1.2)
        self.at("sicken or die")
        sd = T("may sicken or die", 24, LOW).move_to([4.3, -0.95, 0])
        self.play(crab.animate.set_opacity(0.4), FadeIn(sd), run_time=0.7)
        self.at("never takes oxygen")
        self.play(FadeOut(VGroup(lo, sd)), run_time=0.2)
        self.clear_term(0.3)
        fert = bchip("fertilizer", NUT, 28).move_to([1.2, 2.9, 0])
        ar = arr([1.2, 2.5, 0], [1.2, -1.2, 0], NUT, w=5)
        cross = VGroup(Line([0.9, 0.9, 0], [1.5, 0.2, 0], color=LOW, stroke_width=8),
                       Line([1.5, 0.9, 0], [0.9, 0.2, 0], color=LOW, stroke_width=8))
        self.play(FadeIn(fert, shift=DOWN * 0.1), GrowArrow(ar), run_time=0.6)
        self.play(Create(cross), run_time=0.3)
        self.at("Living things use it")
        self.play(Indicate(bs, color=BACT, scale_factor=1.8), Indicate(bl, color=BACT), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Layers(BayScene):
    def construct(self):
        st = stage()
        self.add(st)
        self.at("Why the deep channel")
        ch = T("deep channel", 28, GREY, weight=BOLD).move_to([1.9, -2.7, 0])
        ar0 = arr([1.9, -2.3, 0], [1.9, -1.8, 0], GREY, w=3, tip=0.14)
        self.play(FadeIn(ch), run_time=0.4)
        self.at("fresh river water")
        fl = T("fresh river water", 28, TEXT).move_to([2.2, 0.325, 0])
        self.play(st.fresh.animate.set_fill(TEAL, 0.0), FadeIn(fl), run_time=0.5)
        fl2 = arr([-1.4, 0.3, 0], [-1.4, 0.6, 0], GREY, w=3, tip=0.1)
        self.at("floats")
        fl_lab = Dot(radius=0.001)
        self.at("saltier, heavier seawater")
        sl = T("saltier, heavier seawater", 28, TEXT).move_to([1.9, -1.5, 0])
        self.play(FadeOut(ch), FadeIn(sl), run_time=0.5)
        self.at("mix poorly")
        line = DashedVMobject(Line([BX0, SPLIT, 0], [BX1, SPLIT, 0], color=GOLD, stroke_width=7), num_dashes=30)
        self.play(Create(line), run_time=0.6)
        self.at("new oxygen")
        air = bchip("air", GREY, 24).move_to([-0.6, 2.4, 0])
        oxa = arr([-0.6, 2.05, 0], [-0.6, SPLIT + 0.12, 0], OXY, w=6)
        stop = Line([-0.95, SPLIT - 0.02, 0], [-0.25, SPLIT - 0.02, 0], color=LOW, stroke_width=8)
        self.play(FadeIn(air), GrowArrow(oxa), run_time=0.8)
        self.play(Create(stop), run_time=0.2)
        self.at("reaches the bottom")
        nb = T("little new oxygen reaches the bottom", 24, OXY).move_to([1.6, -2.4, 0])
        self.play(FadeOut(sl), FadeIn(nb), run_time=0.5)
        self.at("Warm water")
        self.play(FadeOut(VGroup(air, oxa)), run_time=0.3)
        b1 = Rectangle(width=2.8, height=0.4, stroke_color=OXY, stroke_width=3, fill_color=OXY, fill_opacity=0.45).move_to([4.7, 3.0, 0])
        b2 = Rectangle(width=1.6, height=0.4, stroke_color=OXY, stroke_width=3, fill_color=OXY, fill_opacity=0.45)
        b2.move_to([b1.get_left()[0] + 0.8, 2.25, 0])
        l1 = T("cooler water", 24, TEXT).next_to(b1, LEFT, buff=0.2)
        l2 = T("warm water", 24, TEXT).next_to(b1, LEFT, buff=0.2).set_y(2.25)
        cap = T("oxygen the water can hold (a sketch)", 22, OXY).move_to([3.4, 1.5, 0])
        self.play(FadeIn(VGroup(b1, l1)), run_time=0.5)
        self.play(FadeIn(VGroup(b2, l2)), FadeIn(cap), run_time=0.7)
        self.at("enrichment of water")
        newterm = VGroup(chip("eutrophication", GOLD, size=38).move_to([0, 3.0, 0]))
        self._term = newterm
        self.play(FadeOut(VGroup(st, nb, fl, fl_lab, line, stop, b1, b2, l1, l2, cap)), FadeIn(newterm, shift=DOWN * 0.15), run_time=0.6)
        c1 = bchip("extra nutrients", NUT, 38).move_to([-4.4, 0.0, 0])
        c2 = bchip("too much algae", ALGAE, 38).move_to([0.3, 0.0, 0])
        c3 = bchip("oxygen loss", LOW, 38).move_to([4.7, 0.0, 0])
        a1 = arr(c1.get_right(), c2.get_left(), GREY)
        a2 = arr(c2.get_right(), c3.get_left(), GREY)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("too much algae growth")
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.at("oxygen loss")
        self.play(GrowArrow(a2), FadeIn(c3, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Fix(BayScene):
    _msg = None

    def say(self, text, color, size=34, y=2.6, rt=0.5):
        new = T(text, size, color, line_spacing=0.9).move_to([0, y, 0])
        old, self._msg = self._msg, new
        if old is None:
            self.play(FadeIn(new, shift=DOWN * 0.15), run_time=rt)
        else:
            self.play(FadeOut(old), FadeIn(new, shift=DOWN * 0.15), run_time=rt)

    def construct(self):
        st = stage()
        self.add(st)
        self.at("human actions")
        self.say("How do human actions change the Bay?\nWhat can we do?", GOLD)
        self.at("People add")
        farm = bchip("farms", GREY, 22).move_to([-4.3, 0.6, 0])
        rs = np.random.RandomState(4)
        ds = [Circle(radius=0.1, stroke_color=NUT, stroke_width=2, fill_color=NUT, fill_opacity=1).move_to(farm.get_right() + RIGHT * 0.1) for _ in range(10)]
        self.add(*ds)
        self.play(FadeIn(farm), run_time=0.3)
        self.say("people add nutrients", NUT, 34, 2.6, 0.4)
        self.play(LaggedStart(*[Succession(d.animate.move_to([-3.0, 1.5, 0]), d.animate.move_to([rs.uniform(-1.6, 5.0), rs.uniform(-0.3, 0.95), 0])) for d in ds], lag_ratio=0.1), run_time=1.4)
        self.at("cut them")
        self.say("people can cut them", FIX, 34, 2.6, 0.4)
        self.play(*[d.animate.set_opacity(0.0) for d in ds[::2]], run_time=0.6)
        self.at("riparian forest buffer")
        self.play(FadeOut(self._msg), run_time=0.2)
        self._msg = None
        self.set_term("riparian forest buffer", "a strip of trees and shrubs along a stream")
        strip = rect(-3.0, -2.2, BOT, TOP, FIX, 0.45, 3)
        trees = VGroup(*[Triangle(fill_color=FIX, fill_opacity=0.9, stroke_width=0).scale(0.17).move_to([-2.6, y, 0]) for y in np.linspace(-2.9, 0.9, 7)])
        self.play(FadeIn(strip), FadeIn(trees, lag_ratio=0.1), run_time=0.8)
        self.at("catches runoff")
        ds2 = [Circle(radius=0.1, stroke_color=NUT, stroke_width=2, fill_color=NUT, fill_opacity=1).move_to([-3.8, y, 0]) for y in (0.8, 0.4, 0.0, -0.4, -0.8)]
        self.add(*ds2)
        self.play(*[d.animate.move_to([-3.15, d.get_y(), 0]) for d in ds2], run_time=0.9)
        self.play(*[d.animate.set_opacity(0.0) for d in ds2[2:]], *[d.animate.move_to([-1.4, d.get_y(), 0]) for d in ds2[:2]], run_time=0.8)
        much = T("catches much of it", 22, FIX).move_to([-0.2, 1.7, 0])
        self.play(FadeIn(much), run_time=0.3)
        self.at("Cover crops")
        self.play(FadeOut(farm), run_time=0.2)
        cc = bchip("cover crops", FIX, 22).move_to([-4.6, 0.6, 0])
        self.play(FadeIn(cc, shift=RIGHT * 0.2), run_time=0.4)
        self.at("wastewater upgrades")
        wu = bchip("wastewater upgrade", FIX, 22).move_to([-4.6, -0.5, 0])
        self.play(FadeIn(wu, shift=RIGHT * 0.2), run_time=0.4)
        self.at("also cut nutrients")
        mn = T("less nitrogen in", 22, NUT).move_to([-4.6, -1.4, 0])
        self.play(FadeIn(mn), run_time=0.5)
        self.at("Oyster reefs")
        self.set_term("oyster reef", "")
        reef = VGroup(*[Rectangle(width=0.55, height=0.38, stroke_color=FIX, stroke_width=2, fill_color=FIX, fill_opacity=0.6)
                        .move_to([x, BOT + 0.22 + dy, 0]) for x, dy in ((0.1, 0), (0.7, 0), (1.3, 0), (0.4, 0.4), (1.0, 0.4), (0.7, 0.8))])
        self.play(FadeIn(reef, lag_ratio=0.1), run_time=0.8)
        self.at("shelter other animals")
        sh = T("shelter for\nother animals", 22, TEXT, line_spacing=0.85).move_to([0.7, -1.35, 0])
        self.play(FadeIn(sh), run_time=0.4)
        self.at("do not replace")
        nr = T("not a replacement\nfor cutting nutrients", 24, NUT, line_spacing=0.85).move_to([3.6, -1.35, 0])
        self.play(FadeIn(nr), run_time=0.5)
        self.at("Underwater grass")
        self.clear_term()
        shelf = grass_shelf(9)
        shelf[1].set_opacity(0.0)
        self.add(shelf)
        gr = shelf[1]
        gl = T("underwater grass", 22, GRASS).move_to([4.95, -1.4, 0])
        self.play(FadeOut(VGroup(sh, nr)), run_time=0.3)
        self.play(gr[:4].animate.set_opacity(1.0), FadeIn(gl), run_time=0.7)
        self.at("partly returned")
        pb = T("partly back", 22, GRASS).move_to([4.95, -1.0, 0])
        self.play(FadeIn(pb), run_time=0.4)
        self.at("Recovery is real")
        self.say("Recovery is real,\nbut slow and usually partial", GRASS, 34, 3.0, 0.6)
        self.at("results often")
        tl = arr([-1.8, 1.7, 0], [3.4, 1.7, 0], GOLD, w=6)
        f0 = bchip("fix", FIX, 22).move_to([-2.6, 1.7, 0])
        yl = T("years", 28, GOLD, weight=BOLD).move_to([0.8, 2.0, 0])
        f1 = bchip("recovery", GRASS, 22).move_to([4.5, 1.7, 0])
        self.play(FadeIn(f0), GrowArrow(tl), FadeIn(yl), FadeIn(f1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "People add many of those nutrients, so people can cut them."
