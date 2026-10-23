"""Extra Nutrients, Less Deep Oxygen  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = Bay water, rain
  YELLOW = nutrients (nitrogen, phosphorus, fertilizer, manure, wastewater)
  GREEN  = algae, underwater grasses
  GREY   = dead algae, structure, small notes
  ORANGE = bacteria / decomposers
  TEAL   = dissolved oxygen
  RED    = low oxygen, dead zone, trouble, "does not"
  BROWN  = land
  TEXT   = animals, plain labels
  GOLD   = the word eutrophication
"""
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BROWN = "#A8825A"
NUT, ALG, DEAD, BAC, OXY, BAD = YELLOW, GREEN, GREY, ORANGE, TEAL, RED

WX0, WX1 = -3.0, 6.1
XC = (WX0 + WX1) / 2
COLS = [-0.6 + 0.65 * k for k in range(7)]
SROW, DROWS = -0.55, (-1.3, -1.95)
ALGROWS = (0.75, 0.35, -0.05)
PILE = (-2.55, -2.8, -3.05)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def dot(x, y, color=OXY, r=0.075):
    return Dot([x, y, 0], radius=r, color=color)


def alga(x, y, color=ALG):
    return Ellipse(width=0.5, height=0.22, stroke_color=color, stroke_width=2, fill_color=color,
                   fill_opacity=0.5).move_to([x, y, 0])


def bact(x, y, s=1.0):
    return RoundedRectangle(corner_radius=0.08 * s, width=0.42 * s, height=0.2 * s, stroke_color=BAC,
                            stroke_width=2, fill_color=BAC, fill_opacity=0.55).move_to([x, y, 0])


class Bay:
    """Side view of the Bay: land at left, a surface layer over a deep layer."""

    def __init__(self, labels=True):
        self.land = Rectangle(width=3.3, height=3.5, stroke_width=0, fill_color=BROWN,
                              fill_opacity=0.35).move_to([-4.65, -1.55, 0])
        self.landl = T("land", 22, GREY).move_to([-4.65, -2.9, 0])
        self.surf = Rectangle(width=9.1, height=1.9, stroke_color=BLUE, stroke_width=2, fill_color=BLUE,
                              fill_opacity=0.16).move_to([XC, 0.05, 0])
        self.deep = Rectangle(width=9.1, height=2.4, stroke_color=BLUE, stroke_width=2, fill_color=BLUE,
                              fill_opacity=0.30).move_to([XC, -2.1, 0])
        self.sl = T("surface\nlayer", 22, GREY).move_to([-1.6, -0.35, 0])
        self.dl = T("deep\nlayer", 22, GREY).move_to([-1.6, -2.2, 0])
        self.sdots = [dot(x, SROW) for x in COLS]
        self.ddots = [[dot(x, y) for x in COLS] for y in DROWS]

    def base(self):
        return [self.land, self.landl, self.surf, self.deep, self.sl, self.dl]

    def alldots(self):
        return self.sdots + self.ddots[0] + self.ddots[1]


def show_bay(scene, b, t=0.15):
    scene.play(*[FadeIn(m) for m in b.base()], *[FadeIn(d) for d in b.alldots()], run_time=t)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Big Changes: Dead Zones, Storms and Climate"
    TITLE = "Extra Nutrients, Less Deep Oxygen"


# =============================================================================================
class S01Question(SpokenScene):
    def construct(self):
        b = Bay()
        show_bay(self, b, 0.15)
        self.at("Each summer")
        title = T("Chesapeake Bay in summer", 30, TEXT, weight=BOLD).move_to([XC, 1.55, 0])
        self.play(FadeIn(title), run_time=0.5)
        self.at("deep water")
        hl = Rectangle(width=9.1, height=2.4, stroke_color=TEXT, stroke_width=5).move_to([XC, -2.1, 0])
        self.play(Create(hl), run_time=0.6)
        self.at("very low on oxygen")
        low = T("very low\noxygen", 24, BAD, weight=BOLD).move_to([4.95, -1.4, 0])
        gone = b.ddots[0][3:] + b.ddots[1][3:]
        self.play(LaggedStart(*[FadeOut(d) for d in gone], lag_ratio=0.08), FadeIn(low), run_time=1.4)
        self.at("Fish and crabs")
        fish = chip("fish", TEXT, size=24, pad=0.14).move_to([0.1, -2.7, 0])
        crab = chip("crabs", TEXT, size=24, pad=0.14).move_to([1.6, -2.7, 0])
        self.play(FadeIn(fish), FadeIn(crab), run_time=0.5)
        self.at("swim away")
        self.play(fish.animate.move_to([0.1, 0.35, 0]), crab.animate.move_to([1.6, 0.35, 0]), run_time=1.3)
        self.at("Animals that cannot leave")
        stay = chip("cannot leave", TEXT, size=24, pad=0.14).move_to([3.6, -2.85, 0])
        self.play(FadeIn(stay), run_time=0.5)
        self.at("sick or die")
        die = chip("may get sick or die", BAD, size=24, pad=0.14).move_to([3.6, -2.85, 0])
        self.play(ReplacementTransform(stay, die), run_time=0.6)
        self.at("dead zone")
        dz = chip("dead zone", BAD, size=28, pad=0.14).move_to([4.95, -2.2, 0])
        dzr = Rectangle(width=5.05, height=2.4, stroke_color=BAD, stroke_width=5).move_to([3.575, -2.1, 0])
        self.play(ReplacementTransform(hl, dzr), FadeIn(dz, scale=0.8), run_time=0.7)
        self.at("How can too much")
        q = VGroup(T("How can too much fertilizer", 34, TEXT, weight=BOLD),
                   T("make part of the Bay run out of oxygen?", 34, TEXT, weight=BOLD)).arrange(DOWN, buff=0.15)
        q.move_to([XC, 2.85, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.at("run out of")
        fert = chip("fertilizer", NUT, size=24, pad=0.14).move_to([-4.65, 0.75, 0])
        a = arr([-3.75, 0.75, 0], [-2.7, 0.75, 0], NUT, w=6)
        qm = T("?", 44, TEXT, weight=BOLD).move_to([-2.25, 0.75, 0])
        self.play(FadeIn(fert), GrowArrow(a), FadeIn(qm), run_time=0.8)
        self.finish()


# =============================================================================================
NUTPOS = [(-2.5, 0.6), (-1.8, 0.35), (-1.3, 0.7), (-2.2, 0.05), (-1.5, 0.1), (-2.65, 0.3)]
ALG0 = [(COLS[1], ALGROWS[1]), (COLS[3], ALGROWS[1]), (COLS[5], ALGROWS[1])]


class S02Nutrients(SpokenScene):
    def construct(self):
        b = Bay()
        show_bay(self, b, 0.15)
        self.at("A nutrient")
        defn = VGroup(chip("nutrient", NUT, size=30, pad=0.16),
                      T("a substance living things need to grow", 26, TEXT)).arrange(RIGHT, buff=0.3)
        defn.move_to([0, 3.0, 0])
        self.play(FadeIn(defn, shift=DOWN * 0.15), run_time=0.6)
        self.at("Algae are tiny")
        algs = VGroup(*[alga(x, y) for x, y in ALG0])
        al = T("algae", 26, ALG, weight=BOLD).move_to([COLS[3], 1.45, 0])
        self.play(FadeIn(algs, scale=0.6), FadeIn(al), run_time=0.7)
        self.at("need nitrogen")
        n1 = chip("nitrogen", NUT, size=26, pad=0.14).move_to([-1.2, 2.15, 0])
        n2 = chip("phosphorus", NUT, size=26, pad=0.14).move_to([1.3, 2.15, 0])
        self.play(FadeIn(n1, shift=DOWN * 0.1), FadeIn(n2, shift=DOWN * 0.1), run_time=0.6)
        self.at("Farm fertilizer")
        f = chip("fertilizer", NUT, size=24, pad=0.14).move_to([-4.65, -0.35, 0])
        self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.5)
        self.at("and manure")
        m = chip("manure", NUT, size=24, pad=0.14).move_to([-4.65, -1.2, 0])
        self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.5)
        self.at("So does")
        w = chip("wastewater", NUT, size=24, pad=0.14).move_to([-4.65, -2.05, 0])
        self.play(FadeIn(w, shift=RIGHT * 0.2), run_time=0.5)
        self.at("Rain washes")
        rain = VGroup(*[Line([x, 1.7, 0], [x - 0.3, 1.1, 0], color=BLUE, stroke_width=4) for x in (-5.5, -4.9, -4.3, -3.7)])
        rl = T("rain", 26, BLUE, weight=BOLD).move_to([-4.6, 2.25, 0])
        self.play(FadeIn(rain, shift=DOWN * 0.2), FadeIn(rl), run_time=0.6)
        self.at("fields and lawns")
        nd = [dot(-4.1 + 0.25 * i, 0.5, NUT, 0.09) for i in range(6)]
        self.play(*[FadeIn(d) for d in nd], run_time=0.4)
        self.at("into rivers")
        self.play(*[d.animate.move_to([NUTPOS[i][0], NUTPOS[i][1], 0]) for i, d in enumerate(nd)],
                  run_time=1.6, rate_func=smooth)
        self.finish()


# =============================================================================================
class S03Bloom(SpokenScene):
    def construct(self):
        b = Bay()
        show_bay(self, b, 0.15)
        al3 = [alga(x, y) for x, y in ALG0]
        nd = [dot(x, y, NUT, 0.09) for x, y in NUTPOS]
        self.add(*al3, *nd)
        grid = [(COLS[k], r) for r in ALGROWS for k in range(7)]
        others = [(x, y) for (x, y) in grid if (x, y) not in ALG0]
        extra = [alga(x, y) for x, y in others]
        self.at("In the Bay")
        self.wait(0.1)
        self.at("feed the algae")
        tgt = [al3[0], al3[0], al3[1], al3[1], al3[2], al3[2]]
        self.play(*[d.animate.move_to(tgt[i].get_center()) for i, d in enumerate(nd)], run_time=0.9)
        self.play(*[FadeOut(d) for d in nd], *[Indicate(a, scale_factor=1.3, color=ALG) for a in al3], run_time=0.6)
        self.at("grow very fast")
        self.play(LaggedStart(*[GrowFromCenter(a) for a in extra], lag_ratio=0.07),
                  b.surf.animate.set_fill(ALG, 0.28), run_time=2.0)
        self.at("algae bloom")
        bl = chip("algae bloom", ALG, size=30, pad=0.16).move_to([XC, 1.6, 0])
        bl2 = T("a thick, fast growth of algae", 24, TEXT).move_to([XC, 2.25, 0])
        self.play(FadeIn(bl, scale=0.8), FadeIn(bl2), run_time=0.6)
        self.at("The green water")
        shelf = Rectangle(width=0.7, height=2.4, stroke_width=0, fill_color=BROWN, fill_opacity=0.5).move_to([-2.65, -2.1, 0])
        gr = VGroup(*[Line([x, -0.9, 0], [x + 0.06, -0.45, 0], color=ALG, stroke_width=5) for x in (-2.9, -2.7, -2.5)])
        gl = T("underwater\ngrasses", 22, ALG).move_to([-1.85, 0.55, 0])
        self.play(FadeIn(shelf), FadeIn(gr, shift=UP * 0.1), FadeIn(gl), run_time=0.6)
        self.at("underwater grasses")
        gl2 = T("grasses\nshaded", 22, ALG).move_to([-1.85, 0.55, 0])
        self.play(gr.animate.set_stroke(opacity=0.3), ReplacementTransform(gl, gl2), run_time=0.7)
        self.at("Then the algae")
        allg = al3 + extra
        self.play(*[a.animate.set_stroke(DEAD).set_fill(DEAD, 0.5) for a in allg],
                  b.surf.animate.set_fill(BLUE, 0.16), FadeOut(bl), FadeOut(bl2), run_time=0.8)
        self.at("sink to the bottom")
        moves = []
        for a in allg:
            x, y = a.get_center()[0], a.get_center()[1]
            ny = PILE[ALGROWS.index(min(ALGROWS, key=lambda r: abs(r - y)))]
            moves.append(a.animate.move_to([x, ny, 0]))
        self.play(*moves, run_time=2.2, rate_func=smooth)
        dd = T("dead algae", 24, DEAD, weight=BOLD).move_to([XC - 0.6, -3.55 + 0.0, 0])
        self.finish()


# =============================================================================================
class S04Decomposers(SpokenScene):
    def construct(self):
        b = Bay()
        show_bay(self, b, 0.15)
        pile = [alga(x, y, DEAD) for y in PILE for x in COLS]
        self.add(*pile)
        self.at("A decomposer is")
        dc = chip("decomposer", BAC, size=30, pad=0.16).move_to([-2.6, 2.7, 0])
        dt = T("breaks down dead matter", 24, TEXT).move_to([-2.6, 2.05, 0])
        self.play(FadeIn(dc, scale=0.8), run_time=0.5)
        self.at("dead matter")
        self.play(FadeIn(dt), run_time=0.5)
        self.at("Bacteria decompose")
        bs = [bact(x, -2.28) for x in COLS]
        bl = chip("bacteria", BAC, size=24, pad=0.14).move_to([4.95, -2.8, 0])
        self.play(*[FadeIn(x, scale=0.5) for x in bs], FadeIn(bl), run_time=0.8)
        self.at("They use oxygen")
        low = b.ddots[1]
        self.play(LaggedStart(*[d.animate.move_to([COLS[i], -2.28, 0]) for i, d in enumerate(low)], lag_ratio=0.12),
                  run_time=1.6)
        self.play(*[FadeOut(d) for d in low], run_time=0.3)
        self.at("Dissolved oxygen is")
        lg = VGroup(dot(0, 0), T("dissolved oxygen", 26, OXY, weight=BOLD)).arrange(RIGHT, buff=0.2)
        lg2 = T("oxygen gas mixed into water", 22, TEXT)
        leg = VGroup(lg, lg2).arrange(DOWN, buff=0.15).move_to([3.7, 2.45, 0])
        self.play(FadeIn(leg, shift=DOWN * 0.1), run_time=0.6)
        self.at("The deep water runs")
        gone = b.ddots[0][:5]
        lw = T("low oxygen", 24, BAD, weight=BOLD).move_to([4.95, -1.3, 0])
        self.play(*[d.animate.move_to([COLS[i], -2.28, 0]) for i, d in enumerate(gone)], run_time=1.0)
        self.play(*[FadeOut(d) for d in gone], FadeIn(lw), run_time=0.4)
        self.finish()


# =============================================================================================
class S05Deep(SpokenScene):
    def construct(self):
        # panel A: the gauge
        BX, YB, H = -4.2, -2.8, 4.4
        bar = Rectangle(width=1.2, height=H, stroke_color=GREY, stroke_width=3).move_to([BX, YB + H / 2, 0])
        yt = YB + H * 0.4
        redz = Rectangle(width=1.2, height=H * 0.4, stroke_width=0, fill_color=BAD, fill_opacity=0.18)
        redz.align_to(bar, DOWN).align_to(bar, LEFT)
        fill = Rectangle(width=1.2, height=H * 0.28, stroke_width=0, fill_color=OXY, fill_opacity=0.7)
        fill.align_to(bar, DOWN).align_to(bar, LEFT)
        line = Line([-5.2, yt, 0], [-3.2, yt, 0], color=BAD, stroke_width=5)
        ll = M("2 mg/L", 28, BAD).move_to([-2.2, yt, 0])
        gt = T("dissolved oxygen", 26, OXY, weight=BOLD).move_to([BX, 2.2, 0])
        gn = T("in this sketch, not to scale", 22, GREY).move_to([BX + 0.6, -3.3, 0])
        self.at("In this lesson")
        dz = chip("dead zone", BAD, size=34, pad=0.16).move_to([1.7, 1.5, 0])
        self.play(Create(bar), FadeIn(gt), FadeIn(gn), FadeIn(fill), FadeIn(redz), Create(line), FadeIn(ll),
                  FadeIn(dz, scale=0.8), run_time=0.9)
        self.at("per liter")
        lt = T("less than 2 mg/L", 34, BAD, weight=BOLD).move_to([1.7, 0.7, 0])
        self.play(FadeIn(lt, shift=UP * 0.1), run_time=0.5)
        self.at("It is not empty")
        ne = T("not empty", 36, TEXT, weight=BOLD).move_to([1.7, -0.2, 0])
        self.play(FadeIn(ne), run_time=0.5)
        self.at("Bacteria live there")
        bs = VGroup(*[bact(0.4 + 0.75 * i, -1.05, 1.5) for i in range(4)])
        bt = T("bacteria live here", 28, BAC, weight=BOLD).move_to([1.7, -1.7, 0])
        self.play(FadeIn(bs, scale=0.6), FadeIn(bt), run_time=0.6)
        self.at("little to no")
        lo = T("may hold little to no oxygen", 28, OXY, weight=BOLD).move_to([1.7, -2.6, 0])
        self.play(fill.animate.stretch_to_fit_height(H * 0.05).align_to(bar, DOWN), FadeIn(lo), run_time=1.0)
        # panel B
        self.at("Why the deep")
        self.play(*[FadeOut(m) for m in (bar, redz, fill, line, ll, gt, gn, dz, lt, ne, bs, bt, lo)], run_time=0.5)
        q1 = T("Why the deep water?", 40, TEXT, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(q1), run_time=0.4)
        self.at("why summer")
        q2 = T("Why summer?", 40, TEXT, weight=BOLD).move_to([0, 2.3, 0])
        self.play(FadeIn(q2), run_time=0.4)
        self.at("Warm water")
        cool = Rectangle(width=1.6, height=2.8, stroke_color=OXY, stroke_width=3, fill_color=OXY, fill_opacity=0.45)
        warm = Rectangle(width=1.6, height=1.8, stroke_color=OXY, stroke_width=3, fill_color=OXY, fill_opacity=0.45)
        cool.move_to([-2.2, -2.4 + 1.4, 0])
        warm.move_to([2.2, -2.4 + 0.9, 0])
        cl = T("cool water", 28, TEXT).move_to([-2.2, -2.85, 0])
        wl = T("warm water", 28, TEXT).move_to([2.2, -2.85, 0])
        ht = T("oxygen the water can hold", 26, OXY, weight=BOLD).move_to([0, 1.3, 0])
        note = T("in this sketch, not to scale", 22, GREY).move_to([0, -3.4, 0])
        self.play(GrowFromEdge(cool, DOWN), FadeIn(cl), FadeIn(ht), FadeIn(note), run_time=0.6)
        self.play(GrowFromEdge(warm, DOWN), FadeIn(wl), run_time=0.7)
        # panel C
        self.at("In summer")
        self.play(*[FadeOut(m) for m in (q1, q2, cool, warm, cl, wl, ht, note)], run_time=0.5)
        sf = Rectangle(width=10, height=1.8, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.16).move_to([0, 1.1, 0])
        dp = Rectangle(width=10, height=2.6, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.30).move_to([0, -1.1, 0])
        sm = T("summer", 32, TEXT, weight=BOLD).move_to([0, 2.75, 0])
        sd = [dot(x, 0.75) for x in (0.2, 0.85, 1.5, 3.3, 3.95, 4.6)]
        self.play(FadeIn(sm), FadeIn(sf), FadeIn(dp), *[FadeIn(d) for d in sd], run_time=0.5)
        self.at("fresher river water")
        fl = T("fresher river water", 30, BLUE, weight=BOLD).move_to([-2.2, 1.1, 0])
        self.play(FadeIn(fl), run_time=0.4)
        self.at("saltier Bay water")
        sl = T("saltier Bay water", 30, BLUE, weight=BOLD).move_to([-2.2, -1.2, 0])
        self.play(FadeIn(sl), run_time=0.4)
        self.at("mix poorly")
        mp = chip("mix poorly", GREY, size=26, pad=0.14).move_to([-2.2, 0.2, 0])
        mp[0].set_fill(BG, 1.0)
        bd = VGroup(Line([-5, 0.2, 0], [mp.get_left()[0] - 0.05, 0.2, 0], color=GREY, stroke_width=7),
                    Line([mp.get_right()[0] + 0.05, 0.2, 0], [5, 0.2, 0], color=GREY, stroke_width=7))
        self.play(Create(bd), FadeIn(mp), run_time=0.6)
        self.at("new oxygen")
        ar = DashedLine([2.3, 0.9, 0], [2.3, -1.5, 0], color=OXY, stroke_width=4).add_tip(tip_length=0.2)
        nt = T("new oxygen\narrives slowly", 24, OXY, weight=BOLD).move_to([3.7, -0.8, 0])
        self.play(Create(ar), FadeIn(nt), run_time=1.0)
        self.finish()


# =============================================================================================
class S06Answer(SpokenScene):
    def construct(self):
        self.at("Here is the chain")
        c1 = chip("extra nutrients", NUT, size=26, pad=0.16).move_to([-4.3, 1.2, 0])
        c2 = chip("algae bloom", ALG, size=26, pad=0.16).move_to([0, 1.2, 0])
        c3 = chip("algae die and sink", DEAD, size=26, pad=0.16).move_to([4.3, 1.2, 0])
        c4 = chip("decomposers use oxygen", BAC, size=26, pad=0.16).move_to([-3.0, -0.9, 0])
        c5 = chip("animals leave, or may die", BAD, size=26, pad=0.16).move_to([3.0, -0.9, 0])
        a12 = arr([c1.get_right()[0] + 0.05, 1.2, 0], [c2.get_left()[0] - 0.05, 1.2, 0], GREY)
        a23 = arr([c2.get_right()[0] + 0.05, 1.2, 0], [c3.get_left()[0] - 0.05, 1.2, 0], GREY)
        a45 = arr([c4.get_right()[0] + 0.05, -0.9, 0], [c5.get_left()[0] - 0.05, -0.9, 0], GREY)
        el = VGroup(Line([c3.get_bottom()[0], c3.get_bottom()[1] - 0.05, 0], [c3.get_bottom()[0], 0.0, 0], color=GREY, stroke_width=5),
                    Line([c3.get_bottom()[0], 0.0, 0], [-3.0, 0.0, 0], color=GREY, stroke_width=5),
                    arr([-3.0, 0.0, 0], [-3.0, c4.get_top()[1] + 0.05, 0], GREY))
        self.at("Extra nutrients feed")
        self.play(FadeIn(c1, scale=0.8), run_time=0.5)
        self.play(GrowArrow(a12), FadeIn(c2, scale=0.8), run_time=0.6)
        self.at("The algae die")
        self.play(GrowArrow(a23), FadeIn(c3, scale=0.8), run_time=0.6)
        self.at("Decomposers use")
        self.play(Create(el), FadeIn(c4, scale=0.8), run_time=0.9)
        self.at("Fish and crabs")
        self.play(GrowArrow(a45), FadeIn(c5, scale=0.8), run_time=0.7)
        self.at("Eutrophication is")
        eu = T("eutrophication", 46, GOLD, weight=BOLD, font=TITLE_FONT).move_to([0, 3.0, 0])
        rl = Line([-6.0, 2.35, 0], [6.0, 2.35, 0], color=GOLD, stroke_width=4)
        d1 = T("extra nutrients feeding too much algae growth", 28, TEXT).move_to([0, -2.2, 0])
        self.play(FadeIn(eu, shift=DOWN * 0.1), Create(rl), FadeIn(d1), run_time=0.8)
        self.at("It can lead")
        d2 = T("it can lead to low oxygen", 28, BAD, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(d2), run_time=0.5)
        self.at("So fertilizer")
        self.play(*[FadeOut(m) for m in (c1, c2, c3, c4, c5, a12, a23, a45, el, eu, rl, d1, d2)], run_time=0.5)
        fe = chip("fertilizer", NUT, size=30, pad=0.16).move_to([-3.8, 2.2, 0])
        ox = chip("oxygen", OXY, size=30, pad=0.16).move_to([3.8, 2.2, 0])
        ax = arr([-2.4, 2.2, 0], [2.5, 2.2, 0], GREY)
        x1 = Line([-0.3, 1.9, 0], [0.3, 2.5, 0], color=BAD, stroke_width=9)
        x2 = Line([-0.3, 2.5, 0], [0.3, 1.9, 0], color=BAD, stroke_width=9)
        tk = T("does not take", 28, BAD, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(fe), FadeIn(ox), GrowArrow(ax), run_time=0.6)
        self.play(Create(x1), Create(x2), FadeIn(tk), run_time=0.5)
        self.at("Its nutrients")
        nu = chip("its nutrients", NUT, size=30, pad=0.16).move_to([-3.8, 0.4, 0])
        al = chip("algae", ALG, size=30, pad=0.16).move_to([3.8, 0.4, 0])
        an = arr([-2.1, 0.4, 0], [3.0, 0.4, 0], GREY)
        ft = T("feed", 28, TEXT, weight=BOLD).move_to([0.3, 0.95, 0])
        self.play(FadeIn(nu), GrowArrow(an), FadeIn(ft), FadeIn(al), run_time=0.7)
        self.at("Decomposers use", nth=1)
        de = chip("decomposers", BAC, size=30, pad=0.16).move_to([-3.8, -1.6, 0])
        o2 = chip("the oxygen", OXY, size=30, pad=0.16).move_to([3.8, -1.6, 0])
        ad = arr([-2.1, -1.6, 0], [2.6, -1.6, 0], GREY)
        ut = T("use", 28, TEXT, weight=BOLD).move_to([0.3, -1.05, 0])
        self.play(FadeIn(de), GrowArrow(ad), FadeIn(ut), FadeIn(o2), run_time=0.7)
        self.finish()


# =============================================================================================
class S07End(EndCard):
    LINE = "Extra nutrients feed algae; decomposers then use the deep oxygen."
