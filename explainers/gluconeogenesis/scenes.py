"""Gluconeogenesis: not glycolysis in reverse  (Biochemistrypedia explainer)

Timed to the SPOKEN words: self.at("phrase") waits until the narrator starts that phrase
(word timestamps in audio/words.json, from the real slide audio).

COLOR MAP (one color per concept, whole video)
  BLUE    = glycolysis: the downhill, forward pathway and its enzymes
  ORANGE  = gluconeogenesis: the uphill pathway and its bypass enzymes
  YELLOW  = glucose and the carbon intermediates (the cargo that moves)
  GREEN   = ATP / GTP / NTP: the energy currency that is spent
  PURPLE  = NADH: reducing power
  RED     = barrier / one-way wall / wasted heat
  GREY    = structure, membranes, axes, de-emphasized things
  TEXT    = consumers (brain, red blood cells), neutral labels
No molecular structures are drawn anywhere: only labelled chips, flows and energy diagrams.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

ORANGE = "#F2A154"
PURPLE = "#B58CD9"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def met(text, size=24, color=YELLOW, pad=0.15, min_w=0.0):
    """Metabolite chip: yellow-outlined box with neutral text."""
    lab = T(text, size, TEXT)
    w = max(lab.width + 2 * pad, min_w)
    box = RoundedRectangle(corner_radius=0.12, width=w, height=max(lab.height, 0.3) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.12)
    return VGroup(box, lab.move_to(box))


def arr(a, b, color=GREY, w=5, tip=0.2, buff=0.0):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), color=color, stroke_width=w,
                 buff=buff, tip_length=tip, max_tip_length_to_length_ratio=0.45)


def darr(a, b, color=GREY, w=4, tip=0.16):
    return DoubleArrow(np.array(a, dtype=float), np.array(b, dtype=float), color=color, stroke_width=w,
                       buff=0.0, tip_length=tip, max_tip_length_to_length_ratio=0.4)


def xmark(center, size=0.2, color=RED, w=6):
    c = np.array(center, dtype=float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def numdot(n, color=ORANGE, r=0.2):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
    return VGroup(c, M(str(n), 24, TEXT, weight=BOLD).move_to(c))


def sstep(u):
    return u * u * (3 - 2 * u)


def ramp_pts(xs, ys, xe, ye, n=60):
    return [np.array([xs + (xe - xs) * i / n, ys + (ye - ys) * sstep(i / n), 0.0]) for i in range(n + 1)]


def ramp(xs, ys, xe, ye, color):
    m = VMobject(stroke_color=color, stroke_width=6)
    m.set_points_smoothly(ramp_pts(xs, ys, xe, ye))
    return m


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Gluconeogenesis"
    TITLE = "Not Glycolysis in Reverse"


# =============================================================================================
class S01Fasting(SpokenScene):
    """Fed: glucose is plentiful and burned. Fasted: scarce, so the body makes it from three streams."""

    def construct(self):
        title = T("Two supply chains", 38, font=TITLE_FONT).move_to([0, 3.1, 0])
        self.play(Write(title), run_time=1.2)
        ch_fed = chip("just ate", BLUE, 30).move_to([-2.6, 0.2, 0])
        ch_fast = chip("hours since a meal", ORANGE, 30).move_to([2.6, 0.2, 0])
        self.at("two completely different")
        self.play(FadeIn(ch_fed, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(ch_fast, shift=UP * 0.15), run_time=0.6)
        self.at("whether you have just eaten")
        self.play(Indicate(ch_fed, color=BLUE, scale_factor=1.1), run_time=0.8)

        # ---- fed state ---------------------------------------------------------------------
        self.at("In the fed state")
        fed = T("FED STATE", 34, BLUE, weight=BOLD).move_to([0, 3.1, 0])
        self.play(ReplacementTransform(title, fed), FadeOut(ch_fed), FadeOut(ch_fast), run_time=0.7)

        lv = ValueTracker(0.0)
        tank_o = RoundedRectangle(corner_radius=0.08, width=1.1, height=2.6, stroke_color=GREY,
                                  stroke_width=4).move_to([-5.0, 0.2, 0])

        def fill():
            H = max(0.001, lv.get_value() * 2.48)
            r = Rectangle(width=0.98, height=H, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
            return r.move_to(tank_o.get_bottom() + UP * (0.06 + H / 2))

        tank_f = always_redraw(fill)
        tank_l = T("Blood glucose", 24, TEXT)
        tank_l.add_updater(lambda m: m.next_to(tank_o, DOWN, buff=0.22))
        self.at("blood glucose")
        self.play(FadeIn(tank_o), FadeIn(tank_l), run_time=0.5)
        self.add(tank_f)
        self.play(lv.animate.set_value(0.9), run_time=1.2)

        # cells burn it
        self.at("so cells simply burn it")
        gly = chip("Glycolysis", BLUE, 28).move_to([-1.6, 0.2, 0])
        krebs = chip("Krebs cycle", BLUE, 28).move_to([1.7, 0.2, 0])
        atp = chip("ATP", GREEN, 28).move_to([4.9, 0.2, 0])
        a1 = arr([-4.35, 0.2, 0], [-2.85, 0.2, 0], YELLOW)
        a2 = arr([-0.35, 0.2, 0], [0.45, 0.2, 0], BLUE)
        a3 = arr([3.05, 0.2, 0], [4.1, 0.2, 0], BLUE)
        dots = VGroup(*[Dot([-4.35, 0.2, 0], radius=0.1, color=YELLOW) for _ in range(4)])
        self.add(dots)
        self.play(GrowArrow(a1), LaggedStart(*[d.animate.move_to([-2.85, 0.2, 0]) for d in dots],
                                             lag_ratio=0.25), run_time=1.2)
        self.play(FadeOut(dots), run_time=0.2)
        self.at("Glycolysis feeds")
        self.play(FadeIn(gly, scale=0.9), run_time=0.5)
        self.at("Krebs cycle")
        self.play(GrowArrow(a2), FadeIn(krebs, scale=0.9), run_time=0.7)
        self.at("which makes ATP")
        self.play(GrowArrow(a3), FadeIn(atp, scale=0.9), run_time=0.6)
        self.play(Indicate(atp, color=GREEN, scale_factor=1.15), run_time=0.7)

        # ---- fasted state -----------------------------------------------------------------
        self.at("But hours after a meal")
        fasted = T("FASTED STATE", 34, ORANGE, weight=BOLD).move_to([0, 3.1, 0])
        chain = VGroup(gly, krebs, atp, a1, a2, a3)
        self.play(ReplacementTransform(fed, fasted), FadeOut(chain), tank_o.animate.move_to([1.7, 0.2, 0]),
                  run_time=1.3)
        self.at("glucose runs scarce")
        self.play(lv.animate.set_value(0.1), run_time=1.3)

        self.at("and the brain and red blood cells")
        brain = chip("Brain", TEXT, 26).move_to([4.9, 1.15, 0])
        rbc = chip("Red blood cells", TEXT, 26).move_to([4.9, -0.75, 0])
        brain.align_to(rbc, LEFT)
        d1 = arr([2.45, 0.2, 0], brain.get_left() + LEFT * 0.12, TEXT, 4)
        d2 = arr([2.45, 0.2, 0], rbc.get_left() + LEFT * 0.12, TEXT, 4)
        self.play(FadeIn(brain, shift=LEFT * 0.2), FadeIn(rbc, shift=LEFT * 0.2), run_time=0.8)
        self.at("still demand it")
        self.play(GrowArrow(d1), GrowArrow(d2), run_time=0.6)
        self.play(Indicate(brain, color=TEXT), Indicate(rbc, color=TEXT), run_time=0.8)

        self.at("Now the body switches")
        fac = chip("Gluconeogenesis", ORANGE, 26).move_to([-1.0, 0.2, 0])
        fa = arr([0.65, 0.2, 0], [1.05, 0.2, 0], ORANGE, 5, tip=0.16)
        self.play(FadeIn(fac, scale=0.9), run_time=0.7)
        self.at("manufacturing")
        dots = VGroup(*[Dot([0.7, 0.2, 0], radius=0.1, color=YELLOW) for _ in range(5)])
        self.add(dots)
        self.play(GrowArrow(fa), lv.animate.set_value(0.75),
                  LaggedStart(*[d.animate.move_to([1.55, 0.2, 0]) for d in dots], lag_ratio=0.25), run_time=2.0)
        self.play(FadeOut(dots), run_time=0.2)
        self.play(d1.animate.set_color(YELLOW), d2.animate.set_color(YELLOW), run_time=0.4)

        # three streams
        self.at("Three streams")
        srcs = []
        for (nm, org, y) in [("Lactate", "muscle, red cells", 1.65), ("Alanine", "muscle protein", 0.0),
                             ("Glycerol", "fat breakdown", -1.65)]:
            c = met(nm, 26)
            o = T("from " + org, 24, GREY)
            g = VGroup(c, o).arrange(DOWN, buff=0.1).move_to([-4.8, y + 0.2, 0])
            srcs.append(g)
        arrows_in = [arr([g.get_right()[0] + 0.12, g[0].get_center()[1], 0],
                         [fac.get_left()[0] - 0.1, 0.2 + (g[0].get_center()[1] - 0.2) * 0.35, 0], YELLOW, 4, 0.16)
                     for g in srcs]
        self.play(Indicate(fac, color=ORANGE, scale_factor=1.08), run_time=0.8)
        self.at("Lactate from muscle")
        self.play(FadeIn(srcs[0], shift=RIGHT * 0.2), GrowArrow(arrows_in[0]), run_time=0.8)
        self.at("alanine from muscle protein")
        self.play(FadeIn(srcs[1], shift=RIGHT * 0.2), GrowArrow(arrows_in[1]), run_time=0.8)
        self.at("and glycerol from fat")
        self.play(FadeIn(srcs[2], shift=RIGHT * 0.2), GrowArrow(arrows_in[2]), run_time=0.8)

        # take-home
        self.at("Hold onto this")
        cap = VGroup(T("fed: burn glucose", 30, BLUE, weight=BOLD), T("fasted: make glucose", 30, ORANGE, weight=BOLD)
                     ).arrange(RIGHT, buff=1.0).move_to([0, -3.0, 0])
        self.play(FadeIn(cap[0], shift=UP * 0.15), run_time=0.6)
        self.at("fasted framing")
        self.play(FadeIn(cap[1], shift=UP * 0.15), run_time=0.6)
        self.finish()


# =============================================================================================
class S02Cliffs(SpokenScene):
    """The glycolysis ladder: three one-way cliffs, four bypass enzymes (named in the narration)."""

    def construct(self):
        names = ["Glucose", "G6P", "F6P", "FBP", "PEP", "Pyruvate"]
        ys = [2.8, 1.52, 0.54, -0.74, -1.72, -3.0]
        nodes = [met(n, 24, min_w=1.5).move_to([0, y, 0]) for n, y in zip(names, ys)]
        bot = lambda i: nodes[i].get_bottom()[1]       # bottom edge of node i
        top = lambda i: nodes[i].get_top()[1]          # top edge of node i
        pad = 0.06

        # headers
        hg = VGroup(T("Glycolysis", 30, BLUE, weight=BOLD), T("↓", 34, BLUE, weight=BOLD)
                    ).arrange(RIGHT, buff=0.2).move_to([-4.3, 3.2, 0])
        hn = VGroup(T("Gluconeogenesis", 30, ORANGE, weight=BOLD), T("↑", 34, ORANGE, weight=BOLD)
                    ).arrange(RIGHT, buff=0.2).move_to([4.0, 3.2, 0])

        # connectors, all grey double-headed at first: "it all looks reversible"
        def link(i, j, dashed=False):
            return darr([0, bot(i) - pad, 0], [0, top(j) + pad, 0], GREY, 4)
        links = [link(i, i + 1) for i in range(5)]

        self.at("Most of glycolysis")
        self.play(FadeIn(hg, shift=RIGHT * 0.2), LaggedStart(*[FadeIn(n, shift=DOWN * 0.15) for n in nodes],
                                                              lag_ratio=0.1), run_time=1.0)
        self.play(LaggedStart(*[GrowFromCenter(l) for l in links], lag_ratio=0.1), run_time=0.5)
        shared = T("shared, reversible steps", 24, GREY).move_to([-3.1, -0.9, 0])
        self.at("freely reversible")
        self.play(FadeIn(shared), run_time=0.5)

        self.at("and gluconeogenesis simply runs")
        self.play(FadeIn(hn, shift=LEFT * 0.2), run_time=0.5)
        # an orange marker climbs the column
        dot = Dot(nodes[5].get_top() + DOWN * 0.1, radius=0.13, color=ORANGE)
        self.add(dot)
        self.play(dot.animate.move_to(nodes[0].get_bottom() + UP * 0.1), run_time=1.8, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.15)

        # ---- the three cliffs --------------------------------------------------------------
        self.at("The problem lives in exactly three places")
        cliff_ids = [0, 2, 4]
        lane = 0.45
        blue_arrows = [arr([-lane, bot(i) - pad, 0], [-lane, top(i + 1) + pad, 0], BLUE, 7, 0.2) for i in cliff_ids]
        rings = [Rectangle(width=1.9, height=abs(bot(i) - top(i + 1)) - 0.05, stroke_color=RED, stroke_width=3,
                           stroke_opacity=0.9).move_to([0, (bot(i) + top(i + 1)) / 2, 0]) for i in cliff_ids]
        self.play(LaggedStart(*[AnimationGroup(ReplacementTransform(links[i], ba), Create(rg))
                                for i, ba, rg in zip(cliff_ids, blue_arrows, rings)], lag_ratio=0.25),
                  FadeOut(shared), run_time=1.3)
        self.at("where glycolysis releases so much")
        walls = T("one-way: huge energy drop", 24, RED).move_to([4.2, 0.2, 0])
        self.play(FadeIn(walls, shift=UP * 0.1), run_time=0.5)
        self.at("effectively one way")
        self.play(Indicate(VGroup(*blue_arrows), color=BLUE, scale_factor=1.12), run_time=0.9)
        self.play(FadeOut(walls), run_time=0.3)

        # enzymes + dG values (appear in the order spoken)
        def left_label(name, val, y, delay_val=True):
            n = T(name, 24, BLUE, weight=BOLD)
            v = T(val, 24, GREY)
            v.next_to(n, DOWN, buff=0.08, aligned_edge=RIGHT)
            g = VGroup(n, v).move_to([-1.2, y, 0], aligned_edge=RIGHT)
            return n, v, g
        ymid = [(bot(i) + top(i + 1)) / 2 for i in cliff_ids]
        hk = left_label("Hexokinase", "ΔG°′ = −16.7 kJ/mol", ymid[0] - 0.0)
        pfk = left_label("Phosphofructokinase-1", "ΔG°′ = −14.2 kJ/mol", ymid[1])
        pk = left_label("Pyruvate kinase", "ΔG°′ = −31.4 kJ/mol", ymid[2])
        for n, v, g in (hk, pfk, pk):
            g.shift(LEFT * 0.0)
            v.set_opacity(0)
        # right-align text under each other
        for n, v, g in (hk, pfk, pk):
            v.next_to(n, DOWN, buff=0.08, aligned_edge=RIGHT)
        self.at("Look at the", lead=-0.4)
        self.play(FadeIn(hk[0], shift=RIGHT * 0.15), run_time=0.5)
        self.at("phosphofructokinase")
        self.play(FadeIn(pfk[0], shift=RIGHT * 0.15), run_time=0.6)
        self.at("and pyruvate")
        self.play(FadeIn(pk[0], shift=RIGHT * 0.15), run_time=0.6)
        self.at("large negative delta G")
        self.play(*[v.animate.set_opacity(1) for n, v, g in (hk, pfk, pk)], run_time=0.8)

        # reversing is impossible
        self.at("so reversing them")
        xs = [xmark([lane, ymid[k], 0], 0.17) for k in range(3)]
        ups = [arr([lane, top(i + 1) + pad, 0], [lane, bot(i) - pad, 0], GREY, 4, 0.16).set_opacity(0.6)
               for i in cliff_ids]
        self.play(LaggedStart(*[AnimationGroup(FadeIn(u), Create(x)) for u, x in zip(ups, xs)], lag_ratio=0.2),
                  run_time=1.0)
        self.at("directly is impossible")
        self.play(*[Indicate(x, color=RED, scale_factor=1.4) for x in xs], run_time=0.9)

        # ---- four bypass enzymes -----------------------------------------------------------
        self.at("Gluconeogenesis solves this")
        self.play(FadeOut(VGroup(*xs)), FadeOut(VGroup(*ups)), FadeOut(VGroup(*rings)), run_time=0.8)
        self.at("shown in orange")
        self.play(Indicate(hn, color=ORANGE, scale_factor=1.12), run_time=0.9)

        def right_label(name, y, num):
            t = T(name, 24, ORANGE, weight=BOLD)
            nd = numdot(num)
            g = VGroup(nd, t).arrange(RIGHT, buff=0.15)
            g.move_to([0.9, y, 0], aligned_edge=LEFT)
            return g
        # bypass 1 and 2 at the first two cliffs
        up1 = arr([lane, top(1) + pad, 0], [lane, bot(0) - pad, 0], ORANGE, 7, 0.2)
        up2 = arr([lane, top(3) + pad, 0], [lane, bot(2) - pad, 0], ORANGE, 7, 0.2)
        r1 = right_label("Glucose-6-phosphatase", ymid[0], 1)
        r2 = right_label("Fructose-1,6-bisphosphatase", ymid[1], 2)
        self.at("glucose 6 phosphatase")
        self.play(GrowArrow(up1), FadeIn(r1, shift=RIGHT * 0.15), run_time=0.9)
        self.at("fructose 1 6 bisphosphatase")
        self.play(GrowArrow(up2), FadeIn(r2, shift=RIGHT * 0.15), run_time=0.9)

        # bypass 3 + 4: pyruvate -> OAA -> PEP
        oaa = met("OAA", 24).move_to([2.0, -2.3, 0])
        pa = arr([0.8, -2.95, 0], [oaa.get_left()[0] - 0.05, -2.52, 0], ORANGE, 6, 0.18)
        pb = arr([oaa.get_left()[0] - 0.05, -2.12, 0], [0.8, -1.75, 0], ORANGE, 6, 0.18)
        r3 = right_label("Pyruvate carboxylase", -3.15, 3)
        r4 = right_label("PEP carboxykinase", -1.6, 4)
        r3.move_to([2.55, -3.15, 0], aligned_edge=LEFT)
        r4.move_to([2.55, -1.6, 0], aligned_edge=LEFT)
        self.at("and the pyruvate carboxylase")
        self.play(GrowArrow(pa), FadeIn(oaa, scale=0.9), FadeIn(r3, shift=RIGHT * 0.15), run_time=0.9)
        self.at("plus PEP")
        self.play(GrowArrow(pb), FadeIn(r4, shift=RIGHT * 0.15), run_time=0.9)

        self.at("Notice that pyruvate to PEP")
        self.play(Indicate(oaa, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.at("split into two reactions")
        two = T("pyruvate \u2192 PEP in two steps", 24, ORANGE).move_to([3.5, -0.7, 0])
        self.play(Indicate(pa, color=ORANGE, scale_factor=1.3), Indicate(pb, color=ORANGE, scale_factor=1.3),
                  FadeIn(two, shift=UP * 0.1), run_time=0.9)
        self.at("whose combined energetics")
        self.play(Indicate(r3, color=ORANGE, scale_factor=1.08), Indicate(r4, color=ORANGE, scale_factor=1.08),
                  run_time=1.0)
        self.at("make the climb feasible")
        self.play(Indicate(oaa, color=ORANGE, scale_factor=1.2), run_time=0.9)

        # ---- summary: same map, different roads --------------------------------------------
        self.at("Same map")
        self.play(FadeOut(two), *[a.animate.set_opacity(0.35) for a in blue_arrows],
                  *[v[0].animate.set_opacity(0.35) for v in (hk, pfk, pk)],
                  *[v[1].animate.set_opacity(0.35) for v in (hk, pfk, pk)], run_time=0.8)
        self.at("different roads")
        self.play(LaggedStart(*[Indicate(a, color=ORANGE, scale_factor=1.3) for a in (up1, up2, pa, pb)],
                              lag_ratio=0.2), run_time=1.6)
        self.finish()


# =============================================================================================
class S03Shuttle(SpokenScene):
    """Oxaloacetate is made inside the mitochondrion but needed outside; malate carries the carbon across."""

    def construct(self):
        mito = RoundedRectangle(corner_radius=0.7, width=6.3, height=6.3, stroke_color=GREY, stroke_width=5,
                                fill_color=GREY, fill_opacity=0.06).move_to([-3.0, 0.0, 0])
        matrix = T("Mitochondrial matrix", 26, GREY).move_to([-3.0, 2.8, 0])
        cyto = T("Cytoplasm", 26, GREY).move_to([3.7, 2.8, 0])
        wall_x = mito.get_right()[0]
        pore_y = -1.1
        S = 26

        # --- inside: pyruvate -> OAA via pyruvate carboxylase -------------------------------
        pyr = met("Pyruvate", S).move_to([-4.4, 1.9, 0])
        oaa_in = met("Oxaloacetate", S).move_to([-4.0, 0.3, 0])
        mal_in = met("Malate", S).move_to([-4.0, -1.1, 0])
        pc = T("Pyruvate\ncarboxylase", 24, ORANGE, weight=BOLD, line_spacing=0.6).move_to([-2.2, 1.1, 0])
        a_pc = arr(pyr.get_bottom() + DOWN * 0.06, [pyr.get_center()[0], oaa_in.get_top()[1] + 0.06, 0], ORANGE, 6, 0.2)

        self.at("Here is a logistics problem")
        self.play(Create(mito), run_time=1.2)
        self.play(FadeIn(matrix), FadeIn(cyto), run_time=0.6)
        self.at("Pyruvate carboxylase lives")
        self.play(FadeIn(pyr, shift=DOWN * 0.1), FadeIn(pc, shift=LEFT * 0.1), run_time=0.8)
        self.at("so oxaloacetate is made there")
        self.play(GrowArrow(a_pc), FadeIn(oaa_in, scale=0.9), run_time=0.9)

        # --- outside: PEP carboxykinase -----------------------------------------------------
        pepck = chip("PEP carboxykinase", ORANGE, 24).move_to([4.6, 0.35, 0])
        self.at("But the next enzyme")
        self.play(FadeIn(pepck, shift=DOWN * 0.1), run_time=0.8)
        self.at("needs that oxaloacetate out in")
        want = arr(oaa_in.get_right() + RIGHT * 0.1, [wall_x - 0.1, 0.3, 0], YELLOW, 4, 0.18)
        want2 = DashedLine([wall_x + 0.1, 0.3, 0], [pepck.get_left()[0] - 0.1, 0.3, 0], color=YELLOW, stroke_width=4)
        self.play(GrowArrow(want), Create(want2), run_time=1.2)

        self.at("and the membrane has no")
        no = T("no oxaloacetate transporter", 24, RED).move_to([3.7, 1.6, 0])
        ghost = oaa_in.copy()
        self.add(ghost)
        self.play(ghost.animate.move_to([wall_x - 1.6, 0.3, 0]), run_time=0.9)
        xm = xmark([wall_x, 0.3, 0], 0.22)
        self.play(Create(xm), FadeIn(no, shift=UP * 0.1), run_time=0.5)
        self.play(ghost.animate.move_to(oaa_in.get_center()), run_time=0.6)
        self.remove(ghost)
        self.play(FadeOut(want), FadeOut(want2), run_time=0.3)

        # --- the workaround ----------------------------------------------------------------
        self.at("The workaround is elegant")
        self.play(FadeOut(no), FadeOut(xm), run_time=0.5)
        self.at("Reduce oxaloacetate")
        a_red = arr([oaa_in.get_center()[0], oaa_in.get_bottom()[1] - 0.05, 0],
                    [mal_in.get_center()[0], mal_in.get_top()[1] + 0.05, 0], YELLOW, 6, 0.2)
        nadh_in = T("NADH \u2192 NAD\u207a", 24, PURPLE).next_to(a_red, RIGHT, buff=0.25)
        self.play(GrowArrow(a_red), FadeIn(nadh_in), FadeIn(mal_in, shift=DOWN * 0.1), run_time=1.0)
        self.at("which can cross")
        pore = Ellipse(width=0.5, height=0.9, stroke_color=YELLOW, stroke_width=4, fill_color=BG,
                       fill_opacity=1.0).move_to([wall_x, pore_y, 0])
        mal_out = met("Malate", S).move_to([1.5, pore_y, 0])
        ghost_m = mal_in.copy()
        self.add(ghost_m)
        self.play(FadeIn(pore, scale=0.7), run_time=0.3)
        self.play(ghost_m.animate.move_to(mal_out.get_center()), run_time=1.0)
        self.remove(ghost_m)
        self.add(mal_out)

        self.at("then reoxidize malate")
        oaa_out = met("Oxaloacetate", S).move_to([4.7, pore_y, 0])
        a_ox = arr(mal_out.get_right() + RIGHT * 0.06, oaa_out.get_left() + LEFT * 0.06, YELLOW, 6, 0.2)
        self.play(GrowArrow(a_ox), FadeIn(oaa_out, scale=0.9), run_time=1.0)

        self.at("regenerates cytoplasmic NADH")
        nadh_out = T("NAD\u207a \u2192 NADH", 24, PURPLE).move_to([3.1, pore_y - 0.55, 0])
        self.play(FadeIn(nadh_out, shift=UP * 0.1), run_time=0.7)
        nadh_big = T("NADH", 30, PURPLE, weight=BOLD).move_to([2.7, -2.7, 0])
        self.play(ReplacementTransform(nadh_out, nadh_big), run_time=0.8)
        self.at("which gluconeogenesis later needs")
        down = chip("later steps", ORANGE, 26).move_to([5.0, -2.7, 0])
        a_dn = arr([nadh_big.get_right()[0] + 0.15, -2.7, 0], [down.get_left()[0] - 0.08, -2.7, 0], PURPLE, 5, 0.18)
        self.play(GrowArrow(a_dn), FadeIn(down), run_time=0.8)

        self.at("So one shuttle accomplishes two jobs")
        j1 = VGroup(T("1", 26, YELLOW, weight=BOLD), T("carbon out", 26, YELLOW)).arrange(RIGHT, buff=0.15)
        j2 = VGroup(T("2", 26, PURPLE, weight=BOLD), T("reducing power in place", 26, PURPLE)).arrange(RIGHT, buff=0.15)
        jobs = VGroup(j1, j2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, 1.7, 0])
        self.play(FadeIn(j1, shift=RIGHT * 0.15), run_time=0.6)
        self.at("moving carbon out")
        self.play(Indicate(oaa_out, color=YELLOW), Indicate(mal_out, color=YELLOW), run_time=0.8)
        self.at("and delivering reducing power")
        self.play(FadeIn(j2, shift=RIGHT * 0.15), Indicate(nadh_big, color=PURPLE, scale_factor=1.3), run_time=0.9)
        self.at("where the downstream reactions")
        a_pk = arr([oaa_out.get_center()[0], oaa_out.get_top()[1] + 0.05, 0],
                   [oaa_out.get_center()[0], pepck.get_bottom()[1] - 0.05, 0], YELLOW, 5, 0.18)
        self.play(GrowArrow(a_pk), Indicate(down, color=ORANGE, scale_factor=1.2), run_time=1.0)
        self.finish()


# =============================================================================================
class S04Bargain(SpokenScene):
    """An energy-level picture of the bargain, then the futile cycle it prevents."""

    def construct(self):
        q = T("Why not just reverse glycolysis?", 36, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.play(Write(q), run_time=1.6)
        # the naive idea: one reversible road
        n_glu = met("Glucose", 28).move_to([-3.0, 0.4, 0])
        n_pyr = met("2 Pyruvate", 28).move_to([3.0, 0.4, 0])
        n_arr = darr([-1.85, 0.4, 0], [1.75, 0.4, 0], GREY, 5, 0.2)
        n_q = T("same enzymes, run backward?", 26, GREY).move_to([0, -0.4, 0])
        self.at("instead of just reversing")
        self.play(FadeIn(n_glu), FadeIn(n_pyr), GrowFromCenter(n_arr), run_time=0.8)
        self.play(FadeIn(n_q, shift=UP * 0.1), run_time=0.5)
        self.at("bargain")
        q2 = T("A bargain with thermodynamics", 36, font=TITLE_FONT, color=GOLD).move_to([0, 3.3, 0])
        self.play(ReplacementTransform(q, q2), run_time=0.9)

        # ---- left panel: glycolysis, downhill ----------------------------------------------
        LX0, LX1 = -5.3, -1.0     # level lines
        Y_GLU, Y_PYR = 0.5, -2.1
        gl_head = T("Glycolysis", 30, BLUE, weight=BOLD).move_to([-3.15, 2.65, 0])
        glu_line = Line([LX0, Y_GLU, 0], [LX0 + 1.3, Y_GLU, 0], color=GREY, stroke_width=5)
        pyr_line = Line([LX1 - 1.3, Y_PYR, 0], [LX1 + 0.75, Y_PYR, 0], color=GREY, stroke_width=5)
        glu_lab = T("Glucose", 26, YELLOW).next_to(glu_line, UP, buff=0.12)
        pyr_lab = T("2 Pyruvate", 26, YELLOW).next_to(pyr_line, UP, buff=0.12).align_to(pyr_line, RIGHT)
        ramp_l = ramp(LX0 + 1.3, Y_GLU, LX1 - 1.3, Y_PYR, BLUE)
        ax = arr([-6.1, -2.5, 0], [-6.1, 2.0, 0], GREY, 3, 0.16)
        ax_l = T("Free energy", 24, GREY).rotate(PI / 2).move_to([-6.5, -0.25, 0])

        self.at("with thermodynamics")
        self.play(FadeOut(VGroup(n_glu, n_pyr, n_arr, n_q)), run_time=0.5)
        self.play(Create(ax), FadeIn(ax_l), run_time=0.8)
        self.at("Glycolysis releases energy")
        self.play(FadeIn(gl_head), run_time=0.5)
        self.play(Create(glu_line), FadeIn(glu_lab), Create(pyr_line), FadeIn(pyr_lab), run_time=0.9)
        self.at("about 74 kilojoules")
        drop_val = M("releases \u2248 74 kJ/mol", 24, BLUE).move_to([-3.4, -2.75, 0])
        self.play(Create(ramp_l), run_time=1.0)
        self.play(FadeIn(drop_val, shift=UP * 0.1), run_time=0.6)
        self.at("so it is downhill")
        pts = ramp_pts(LX0 + 1.3, Y_GLU, LX1 - 1.3, Y_PYR)
        ball = Dot(pts[0] + UP * 0.14, radius=0.14, color=YELLOW)
        path = VMobject(); path.set_points_smoothly([p + UP * 0.14 for p in pts])
        self.add(ball)
        self.play(MoveAlongPath(ball, path), run_time=1.3, rate_func=smooth)
        self.at("spontaneous")
        sp = T("spontaneous", 26, BLUE).move_to([-1.45, 0.3, 0])
        self.play(FadeIn(sp, shift=UP * 0.1), run_time=0.5)

        # ---- right panel: gluconeogenesis, uphill -------------------------------------------
        RX0, RX1 = 1.4, 5.7
        start_y = ValueTracker(Y_PYR)   # 2 pyruvate level (mirror of the left panel)
        end_y = ValueTracker(Y_GLU)     # glucose level: it never moves
        gn_head = T("Gluconeogenesis", 30, ORANGE, weight=BOLD).move_to([3.55, 2.65, 0])
        s_line = always_redraw(lambda: Line([RX0, start_y.get_value(), 0], [RX0 + 1.3, start_y.get_value(), 0],
                                            color=GREY, stroke_width=5))
        e_line = always_redraw(lambda: Line([RX1 - 1.3, end_y.get_value(), 0], [RX1, end_y.get_value(), 0],
                                            color=GREY, stroke_width=5))
        s_lab = T("2 Pyruvate", 26, YELLOW)
        e_lab = T("Glucose", 26, YELLOW)
        s_lab.add_updater(lambda m: m.move_to([RX0 + 0.65, start_y.get_value() + 0.4, 0]))
        e_lab.add_updater(lambda m: m.move_to([RX1 - 0.65, end_y.get_value() + 0.4, 0]))
        r_ramp = always_redraw(lambda: ramp(RX0 + 1.3, start_y.get_value(), RX1 - 1.3, end_y.get_value(), ORANGE))

        self.at("Gluconeogenesis consumes energy")
        self.play(FadeIn(gn_head), run_time=0.5)
        self.add(s_line, e_line, r_ramp)
        self.play(FadeIn(s_lab), FadeIn(e_lab), run_time=0.6)
        ballr = Dot([RX0 + 1.3, Y_PYR + 0.14, 0], radius=0.14, color=YELLOW)
        rpts = [p + UP * 0.14 for p in ramp_pts(RX0 + 1.3, Y_PYR, RX1 - 1.3, Y_GLU)]
        half = VMobject(); half.set_points_smoothly(rpts[:34])
        self.add(ballr)
        self.play(MoveAlongPath(ballr, half), run_time=1.1, rate_func=smooth)
        up_lab = T("uphill: needs energy input", 24, RED).move_to([3.55, -2.8, 0])
        self.play(FadeIn(up_lab, shift=UP * 0.1), run_time=0.4)
        back = VMobject(); back.set_points_smoothly(rpts[:34][::-1])
        self.play(MoveAlongPath(ballr, back), run_time=0.8, rate_func=smooth)
        self.play(FadeOut(ballr), run_time=0.15)

        # six NTP pay the bill
        self.at("the six nucleotide triphosphate")
        ntp = VGroup(*[chip("NTP", GREEN, 24, pad=0.1) for _ in range(6)]).arrange_in_grid(2, 3, buff=0.15)
        ntp.move_to([5.0, -1.85, 0])
        lab6 = T("6 NTP equivalents", 24, GREEN).move_to([5.0, -2.85, 0])
        self.play(FadeOut(up_lab), LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in ntp], lag_ratio=0.12),
                  FadeIn(lab6), run_time=1.5)
        self.at("is precisely what tips")
        s_new = T("2 Pyruvate + 6 NTP", 24, YELLOW)
        s_new.add_updater(lambda m: m.move_to([RX0 + 1.1, start_y.get_value() + 0.4, 0]))
        e_new = T("Glucose + 6 NDP + 6 Pi", 24, YELLOW)
        e_new.add_updater(lambda m: m.move_to([RX1 - 1.25, end_y.get_value() - 0.4, 0]))
        self.play(FadeOut(lab6), FadeOut(s_lab), FadeOut(e_lab), run_time=0.3)
        self.play(ntp.animate.scale(0.3).move_to([RX0 + 0.65, Y_GLU + 1.3, 0]).set_opacity(0),
                  start_y.animate.set_value(Y_GLU + 1.3), run_time=1.4)
        self.play(FadeIn(s_new), FadeIn(e_new), run_time=0.4)
        self.at("to also be favorable")
        ball2 = Dot([RX0 + 1.3, Y_GLU + 1.3 + 0.14, 0], radius=0.14, color=YELLOW)
        rpts2 = [p + UP * 0.14 for p in ramp_pts(RX0 + 1.3, Y_GLU + 1.3, RX1 - 1.3, Y_GLU)]
        path2 = VMobject(); path2.set_points_smoothly(rpts2)
        self.add(ball2)
        self.play(MoveAlongPath(ball2, path2), run_time=1.2, rate_func=smooth)
        fav = T("downhill again", 26, ORANGE).move_to([2.1, Y_GLU + 0.2, 0])
        self.play(FadeIn(fav, shift=UP * 0.1), run_time=0.5)

        # ---- the futile cycle --------------------------------------------------------------
        self.at("If synthesis were free")
        self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, VMobject)], run_time=0.5)
        self.clear()
        cell = RoundedRectangle(corner_radius=0.9, width=10.4, height=5.4, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.06).move_to([0, -0.1, 0])
        glu = met("Glucose", 26).move_to([0, 1.75, 0])
        pyr = met("Pyruvate", 26).move_to([0, -1.95, 0])
        free_t = T("Suppose the climb were free", 36, font=TITLE_FONT, color=GOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(free_t), Create(cell), run_time=0.7)
        self.play(FadeIn(glu), FadeIn(pyr), run_time=0.4)

        self.at("both pathways would run simultaneously")
        ang = PI * 0.85
        a_gly = CurvedArrow([-0.55, 1.3, 0], [-0.55, -1.5, 0], angle=ang, color=BLUE, stroke_width=7)
        a_gn = CurvedArrow([0.55, -1.5, 0], [0.55, 1.3, 0], angle=ang, color=ORANGE, stroke_width=7)
        lg = T("glycolysis", 26, BLUE).move_to([-3.7, -0.1, 0])
        ln = T("gluconeogenesis", 26, ORANGE).move_to([3.5, -0.1, 0])
        self.play(Create(a_gly), FadeIn(lg), run_time=0.7)
        self.play(Create(a_gn), FadeIn(ln), run_time=0.7)
        self.at("in the same cell")
        self.play(Indicate(cell, color=GREY, scale_factor=1.02), run_time=0.8)

        self.at("creating a futile cycle")
        fut = T("futile cycle", 32, RED, weight=BOLD).move_to([0, -0.1, 0])
        self.play(FadeIn(fut, scale=0.8), run_time=0.5)
        loop_d = Dot([-0.55, 1.3, 0], radius=0.13, color=YELLOW)
        self.add(loop_d)
        gly_path = a_gly.copy(); gn_path = a_gn.copy()
        self.play(MoveAlongPath(loop_d, gly_path), run_time=0.8, rate_func=linear)

        self.at("that burns ATP")
        atp1 = chip("ATP", GREEN, 24, pad=0.1).move_to([3.4, 0.9, 0])
        self.play(FadeIn(atp1, scale=0.8), MoveAlongPath(loop_d, gn_path), run_time=0.9, rate_func=linear)
        self.at("and dumps it as heat")
        heat = VGroup(*[Line([3.4 + dx, 1.3, 0], [3.4 + dx, 1.8, 0], color=RED, stroke_width=4)
                        for dx in (-0.2, 0.0, 0.2)])
        heat_t = T("heat", 26, RED).move_to([3.4, 2.15, 0])
        self.play(atp1.animate.shift(UP * 0.4).set_opacity(0.0), FadeIn(heat, shift=UP * 0.3), FadeIn(heat_t), run_time=1.0)

        self.at("with no net product")
        net = VGroup(T("net glucose made:", 28), M("0", 34, RED, weight=BOLD)).arrange(RIGHT, buff=0.25)
        net.move_to([0, -3.35, 0])
        self.play(FadeIn(net, shift=UP * 0.1), run_time=0.7)

        # ---- the price of directional control ----------------------------------------------
        self.at("The energy cost is not waste")
        self.play(FadeOut(VGroup(cell, glu, pyr, a_gly, a_gn, lg, ln, fut, loop_d, heat, heat_t, net, free_t,
                                 atp1)), run_time=0.6)
        l1 = T("The energy cost is not waste.", 40, font=TITLE_FONT).move_to([0, 2.1, 0])
        self.play(Write(l1), run_time=1.3)
        self.at("price of directional control")
        l2 = T("It is the price of directional control.", 40, font=TITLE_FONT, color=GOLD).move_to([0, 1.0, 0])
        pyr2 = met("2 Pyruvate", 26).move_to([-4.6, -1.3, 0])
        glu2 = met("Glucose", 26).move_to([4.6, -1.3, 0])
        one_way = arr([-3.5, -1.3, 0], [3.5, -1.3, 0], ORANGE, 10, 0.4)
        pay = T("6 NTP equivalents spent", 26, GREEN).move_to([0, -0.65, 0])
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(pyr2), FadeIn(glu2), GrowArrow(one_way), FadeIn(pay, shift=DOWN * 0.1), run_time=1.0)
        self.finish()


# =============================================================================================
class S05End(EndCard):
    LINE = "Gluconeogenesis spends energy to climb its own road."
