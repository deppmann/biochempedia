"""DNA is the genetic material: heredity travels with DNA  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = DNA (every strand of DNA; the old, parental strand; phosphorus-32, the DNA label)
  GREEN  = newly made DNA (the new partner strand, light nitrogen DNA)
  PURPLE = protein (trypsin target, the phage coat, sulfur-35, the protein label)
  PINK   = RNA (ribonuclease target)
  ORANGE = bacterial type III (the dead donor's type)
  YELLOW = the unknown agent / the measured activity
  RED    = activity destroyed (0%)
  GREY   = outlines, living recipient cells, tubes, structure, de-emphasized
  TEXT   = base letters not under comparison, label dots
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
TEAL_RNA = "#E88BC4"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell(color, capsule, w=2.5, h=1.15, dashed=False, op=0.25):
    body = RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op)
    parts = []
    if capsule:
        parts.append(RoundedRectangle(corner_radius=0.62, width=w + 0.3, height=h + 0.3, stroke_color=color,
                                      stroke_width=7, fill_opacity=0))
    parts.append(body)
    return VGroup(*parts)


def letters(seq, color, size=48, dx=1.0):
    n = len(seq)
    return VGroup(*[M(ch, size, color, weight=BOLD).move_to([(i - (n - 1) / 2) * dx, 0, 0]) for i, ch in enumerate(seq)])


def strand(seq, color, y, left, right, size=48, dx=1.0):
    """letters plus the two end labels, as one group at height y."""
    L = letters(seq, color, size, dx).move_to([0, y, 0])
    ln = T(left, 26, GREY).move_to([-(len(seq) - 1) / 2 * dx - 0.85, y, 0])
    rn = T(right, 26, GREY).move_to([(len(seq) - 1) / 2 * dx + 0.85, y, 0])
    g = VGroup(L, ln, rn)
    g.L, g.ends = L, VGroup(ln, rn)
    return g


def ticks(y_top, y_bot, n=6, dx=1.0, color=GREY):
    return VGroup(*[Line([(i - (n - 1) / 2) * dx, y_top, 0], [(i - (n - 1) / 2) * dx, y_bot, 0],
                         color=color, stroke_width=3) for i in range(n)])


def bar(x, h, color, base, w=1.2, op=0.85):
    h = max(h, 0.04)
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)
    r.move_to([x, base + h / 2, 0])
    return r


class S00Title(TitleCard):
    LESSON = "DNA is the genetic material"
    TITLE = "Heredity travels with DNA"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """dead type III cells + living harmless cells + a question; mixed; the living cells take the dead cells' type."""

    def construct(self):
        ys = [2.0, 0.0, -2.0]
        dead = VGroup(*[cell(ORANGE, True, op=0.12).move_to([-4.6, y, 0]) for y in ys])
        dead_l = T("heat-killed, type III", 24, ORANGE).move_to([-4.6, 3.1, 0])
        live = VGroup(*[cell(GREY, False).move_to([4.6, y, 0]) for y in ys])
        live_l = T("living, harmless", 24, GREY).move_to([4.6, 3.1, 0])
        self.at("Dead bacteria")
        self.play(FadeIn(dead), FadeIn(dead_l), run_time=0.8)
        self.at("living ones")
        self.play(FadeIn(live), FadeIn(live_l), run_time=0.8)
        q = chip("?", YELLOW, size=64, pad=0.35)
        a1 = arr([-2.8, 0, 0], [q.get_left()[0] - 0.05, 0, 0], GREY)
        a2 = arr([q.get_right()[0] + 0.05, 0, 0], [2.8, 0, 0], GREY)
        self.at("passed across")
        self.play(GrowArrow(a1), FadeIn(q, scale=0.8), GrowArrow(a2), run_time=0.8)
        inj = chip("injected into mice", GREY, size=26)
        b1 = arr([-2.8, 0, 0], [inj.get_left()[0] - 0.05, 0, 0], GREY)
        b2 = arr([inj.get_right()[0] + 0.05, 0, 0], [2.8, 0, 0], GREY)
        self.at("In 1928")
        self.play(ReplacementTransform(q, inj), ReplacementTransform(a1, b1), ReplacementTransform(a2, b2), run_time=0.9)
        live2 = VGroup(*[cell(ORANGE, True).move_to([4.6, y, 0]) for y in ys])
        live2_l = T("living, type III", 24, ORANGE).move_to([4.6, 3.1, 0])
        self.at("came living bacteria")
        self.play(ReplacementTransform(live, live2), ReplacementTransform(live_l, live2_l), run_time=1.0)
        desc = T("passed to descendants", 24, ORANGE).move_to([4.6, -3.2, 0])
        self.at("bred true")
        self.play(FadeIn(desc), Indicate(live2, color=ORANGE, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Enzymes(SpokenScene):
    """three enzyme treatments of the purified fraction; activity bars; only the DNA enzyme removes it."""

    def construct(self):
        head = T("activity left after each enzyme", 30, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(Write(head), run_time=0.5)
        frac = chip("purified active fraction", YELLOW, size=30).move_to([-3.2, 0.2, 0])
        names = T("Avery, MacLeod and McCarty", 26, GREY).next_to(frac, UP, buff=0.5)
        self.at("Later")
        self.play(FadeIn(names), FadeIn(frac), run_time=0.8)
        ech = VGroup(chip("trypsin, chymotrypsin", PURPLE, size=24), chip("ribonuclease", TEAL_RNA, size=24),
                     chip("DNA-digesting enzymes", BLUE, size=24)).arrange(DOWN, buff=0.45).move_to([3.4, 0.2, 0])
        arrs = VGroup(*[arr(frac.get_right() + RIGHT * 0.05, e.get_left() + LEFT * 0.05, GREY, w=4) for e in ech])
        self.at("tried enzymes", lead=0.8)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a_), FadeIn(e)) for a_, e in zip(arrs, ech)], lag_ratio=0.15), run_time=0.7)
        self.at("break down protein")
        self.play(FadeOut(VGroup(frac, names, ech, arrs)), run_time=0.3)
        sub = T("illustrative values, not Avery's measurements", 24, GREY).move_to([0, 2.5, 0])
        self.play(FadeIn(sub), run_time=0.4)
        x0, wbar = 0.3, 4.4
        rows = [(1.7, "protein", PURPLE, "trypsin, chymotrypsin"),
                (0.4, "RNA", TEAL_RNA, "ribonuclease"),
                (-0.9, "DNA", BLUE, "DNA-digesting enzymes")]

        def row_labels(y, tgt, col, enz):
            c = chip(tgt, col, size=24).move_to([-5.3, y, 0])
            c.align_to([-6.2, 0, 0], LEFT)
            t = T(enz, 24, TEXT).next_to(c, RIGHT, buff=0.3)
            track = Rectangle(width=wbar, height=0.7, stroke_color=GREY, stroke_width=2).move_to([x0 + wbar / 2, y, 0])
            return VGroup(c, t), track

        def full(y):
            return Rectangle(width=wbar, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85).move_to(
                [x0 + wbar / 2, y, 0])

        pct = lambda s, y, col=YELLOW: M(s, 26, col).move_to([5.45, y, 0])

        l1, t1 = row_labels(*rows[0][:1], *rows[0][1:])
        l2, t2 = row_labels(*rows[1][:1], *rows[1][1:])
        l3, t3 = row_labels(*rows[2][:1], *rows[2][1:])
        self.at("break down protein")
        self.play(FadeIn(l1), Create(t1), run_time=0.8)
        f1 = full(rows[0][0])
        self.at("Activity")
        self.play(GrowFromEdge(f1, LEFT), FadeIn(pct("100%", rows[0][0])), run_time=0.8)
        self.at("Ribonuclease")
        self.play(FadeIn(l2), Create(t2), run_time=0.8)
        f2 = full(rows[1][0])
        self.at("Activity", nth=1)
        self.play(GrowFromEdge(f2, LEFT), FadeIn(pct("100%", rows[1][0])), run_time=0.8)
        self.at("An enzyme preparation")
        self.play(FadeIn(l3), Create(t3), run_time=0.8)
        f3 = full(rows[2][0])
        p3 = pct("100%", rows[2][0])
        self.play(GrowFromEdge(f3, LEFT), FadeIn(p3), run_time=0.5)
        z = pct("0%", rows[2][0], RED)
        thin = Rectangle(width=0.04, height=0.7, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([x0 + 0.02, rows[2][0], 0])
        self.at("destroyed it")
        self.play(ReplacementTransform(f3, thin), ReplacementTransform(p3, z), run_time=0.8)
        quote = T("principally, if not solely, DNA", 30, BLUE, font=TITLE_FONT).move_to([0, -2.2, 0])
        self.at("principally")
        self.play(FadeIn(quote, shift=UP * 0.1), run_time=0.8)
        note = T("a protein below the detection limit is not excluded", 24, PURPLE).move_to([0, -3.1, 0])
        self.at("detection limit")
        self.play(FadeIn(note), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def phage():
    """coat (head, tail, legs) and DNA squiggle; head centre at the origin."""
    head = RegularPolygon(6, radius=0.85, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.25).rotate(PI / 6)
    tail = Rectangle(width=0.26, height=1.0, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.25)
    tail.move_to([0, -0.85 - 0.5 + 0.02, 0])
    legs = VGroup(Line([0, -1.85, 0], [-0.45, -2.15, 0], color=PURPLE, stroke_width=4),
                  Line([0, -1.85, 0], [0.45, -2.15, 0], color=PURPLE, stroke_width=4))
    coat = VGroup(head, tail, legs)
    dna = ParametricFunction(lambda t: np.array([0.38 * np.sin(6 * PI * t), (t - 0.5) * 1.1, 0]), t_range=[0, 1],
                             color=BLUE, stroke_width=5)
    coat.scale(1.25, about_point=ORIGIN)
    dna.scale(1.25, about_point=ORIGIN)
    return coat, dna


def dots(points, color):
    return VGroup(*[Circle(radius=0.085, stroke_color=color, stroke_width=3, fill_color=TEXT, fill_opacity=1).move_to(p) for p in points])


class S03Labels(SpokenScene):
    """phage coat vs DNA, tracers, blender, bars for the fluid and for the progeny."""

    def construct(self):
        coat, dna = phage()
        hc = np.array([-4.2, 2.0, 0])
        coat.move_to(coat.get_center() + hc)
        dna.move_to(hc)
        # coat dots: five on the hexagon outline, one on the tail
        head = coat[0]
        cdots = dots([head.get_vertices()[i] + hc * 0 for i in (0, 1, 2, 3, 5)] + [coat[1].get_center()], PURPLE)
        ddots = dots([dna.point_from_proportion(p) for p in (0.1, 0.35, 0.6, 0.85)], BLUE)
        lab_coat = T("protein coat", 24, PURPLE).move_to([-1.4, 2.7, 0])
        chip_s = chip("sulfur-35", PURPLE, size=24).move_to([-1.4, 2.0, 0])
        lab_dna = T("DNA", 24, BLUE).move_to([-1.4, 1.0, 0])
        chip_p = chip("phosphorus-32", BLUE, size=24).move_to([-1.4, 0.3, 0])
        self.at("protein coat")
        self.play(FadeIn(coat), FadeIn(dna), FadeIn(lab_coat), FadeIn(lab_dna), run_time=1.0)
        self.at("the protein with")
        self.play(FadeIn(chip_s), FadeIn(cdots), run_time=0.7)
        self.at("mostly the DNA")
        self.play(FadeIn(chip_p), FadeIn(ddots), run_time=0.7)
        bact = RoundedRectangle(corner_radius=0.6, width=3.6, height=1.3, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.2).move_to([-4.2, -2.1, 0])
        bl = T("E. coli", 24, GREY).move_to([-4.2, -3.2, 0])
        phg = VGroup(coat, dna, cdots, ddots)
        self.at("attach to")
        self.play(FadeIn(bact), FadeIn(bl), run_time=0.6)
        self.play(phg.animate.shift(DOWN * 0.75), run_time=0.7)
        # blender: the coat is sheared off, the DNA stays with the cell
        title = T("in the fluid after blending", 24, GREY).move_to([3.5, 2.7, 0])
        base = -2.4
        axis = Line([1.2, base, 0], [6.0, base, 0], color=GREY, stroke_width=3)
        xs, xp = 2.1, 4.7
        ls = T("sulfur-35", 22, PURPLE).move_to([xs, base - 0.4, 0])
        lp = T("phosphorus-32", 22, BLUE).move_to([xp, base - 0.4, 0])
        stub = ParametricFunction(lambda t: np.array([0.38 * np.sin(6 * PI * t), (t - 0.5) * 1.1, 0]), t_range=[0, 1],
                                  color=BLUE, stroke_width=4).scale(0.3).move_to([-4.2, 1.25, 0])
        stub_dot = dots([stub.point_from_proportion(0.5)], BLUE)
        left_s = dots([[-5.0, -1.45, 0], [-3.4, -1.45, 0]], PURPLE)
        coat_g = VGroup(coat, cdots, stub, stub_dot)
        self.at("in a blender")
        self.add(stub, stub_dot)
        self.play(FadeIn(left_s), coat_g.animate.shift(UP * 0.5 + LEFT * 0.9), dna.animate.move_to([-4.2, -2.1, 0]).rotate(PI / 2),
                  ddots.animate.move_to([-4.2, -2.1, 0]).rotate(PI / 2),
                  FadeIn(title), Create(axis), FadeIn(ls), FadeIn(lp), run_time=1.2)
        bs = bar(xs, 3.0, PURPLE, base)
        vs = M("75%", 26, PURPLE).next_to(bs, UP, buff=0.12)
        self.at("of the sulfur came off")
        self.play(GrowFromEdge(bs, DOWN), FadeIn(vs), run_time=0.8)
        bp = bar(xp, 0.6, BLUE, base)
        vp = M("15%", 26, BLUE).next_to(bp, UP, buff=0.12)
        self.at("of the phosphorus did")
        self.play(GrowFromEdge(bp, DOWN), FadeIn(vp), run_time=0.8)
        # progeny: reset both bars to nothing, new label, then reveal on the words
        title2 = T("progeny: share of parental label", 24, GREY).move_to([3.5, 2.7, 0])
        bs2 = bar(xs, 0.04, PURPLE, base)
        bp2 = bar(xp, 0.04, BLUE, base)
        self.at("still made phage")
        self.play(ReplacementTransform(title, title2), ReplacementTransform(bs, bs2), ReplacementTransform(bp, bp2),
                  FadeOut(vs), FadeOut(vp), run_time=0.8)
        vs2 = M("<1%", 26, PURPLE).next_to(bs2, UP, buff=0.12)
        self.at("less than")
        self.play(FadeIn(vs2), run_time=0.5)
        bp3 = bar(xp, 1.2, BLUE, base)
        vp3 = M("≥30%", 26, BLUE).next_to(bp3, UP, buff=0.12)
        self.at("or more of the")
        self.play(ReplacementTransform(bp2, bp3), FadeIn(vp3), run_time=0.8)
        note = T("not proof that no protein entered", 24, GREY).move_to([3.5, -3.3, 0])
        self.at("did not prove")
        self.play(FadeIn(note), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
TOP, BOT = "ATGCCA", "TACGGT"


class S04Pairing(SpokenScene):
    """a letter duplex, pairs lit in turn, then the 22 percent worked problem."""

    def construct(self):
        top = strand(TOP, BLUE, 0.7, "5'", "3'")
        bot = strand(BOT, BLUE, -0.7, "3'", "5'")
        tk = ticks(0.35, -0.35)
        self.at("Two chains")
        self.play(FadeIn(top, shift=DOWN * 0.2), FadeIn(bot, shift=UP * 0.2), Create(tk), run_time=1.0)
        a_top = arr([-2.8, 1.55, 0], [2.8, 1.55, 0], GREY, w=4)
        a_bot = arr([2.8, -1.55, 0], [-2.8, -1.55, 0], GREY, w=4)
        self.at("opposite directions")
        self.play(GrowArrow(a_top), GrowArrow(a_bot), run_time=0.8)

        def col_box(idx):
            return VGroup(*[SurroundingRectangle(VGroup(top.L[i], bot.L[i]), color=TEXT, buff=0.12, stroke_width=3)
                            for i in idx])

        at_box = col_box((0, 1, 5))
        gc_box = col_box((2, 3, 4))
        self.at("Adenine pairs")
        self.play(Create(at_box), run_time=0.7)
        self.at("Guanine pairs")
        self.play(FadeOut(at_box), Create(gc_box), run_time=0.7)
        duplex = VGroup(top.L, bot.L, tk)
        self.at("amounts match")
        self.play(FadeOut(gc_box), FadeOut(a_top), FadeOut(a_bot), FadeOut(top.ends), FadeOut(bot.ends), run_time=0.5)
        self.play(duplex.animate.scale(0.65).move_to([0, 2.55, 0]), run_time=0.8)
        base = -3.0
        xs = [-2.7, -0.9, 0.9, 2.7]
        names = ["A", "T", "G", "C"]
        labs = [M(n, 30, BLUE, weight=BOLD).move_to([x, base - 0.4, 0]) for n, x in zip(names, xs)]
        axis = Line([-3.6, base, 0], [3.6, base, 0], color=GREY, stroke_width=3)
        k = 0.12
        bA = bar(xs[0], 22 * k, BLUE, base)
        vA = M("22%", 26, BLUE).next_to(bA, UP, buff=0.12)
        self.play(Create(axis), FadeIn(VGroup(*labs)), run_time=0.5)
        self.at("a sample is")
        self.play(GrowFromEdge(bA, DOWN), FadeIn(vA), run_time=0.7)
        bT = bar(xs[1], 22 * k, BLUE, base)
        vT = M("22%", 26, BLUE).next_to(bT, UP, buff=0.12)
        self.at("thymine is also")
        self.play(GrowFromEdge(bT, DOWN), FadeIn(vT), run_time=0.7)
        gc = M("G + C = 56%", 30, TEXT).move_to([1.8, 1.4, 0])
        self.at("that leaves")
        self.play(FadeIn(gc, shift=UP * 0.1), run_time=0.7)
        bG = bar(xs[2], 28 * k, BLUE, base)
        bC = bar(xs[3], 28 * k, BLUE, base)
        vG = M("28%", 26, BLUE).next_to(bG, UP, buff=0.12)
        vC = M("28%", 26, BLUE).next_to(bC, UP, buff=0.12)
        self.at("so each is")
        self.play(GrowFromEdge(bG, DOWN), GrowFromEdge(bC, DOWN), FadeIn(vG), FadeIn(vC), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Template(SpokenScene):
    """the duplex separates and each old strand templates a new green partner."""

    def construct(self):
        top = strand(TOP, BLUE, 0.7, "5'", "3'")
        bot = strand(BOT, BLUE, -0.7, "3'", "5'")
        tk = ticks(0.35, -0.35)
        self.play(FadeIn(top), FadeIn(bot), FadeIn(tk), run_time=0.6)
        self.at("one strand fixes")
        self.play(Indicate(top.L, color=BLUE, scale_factor=1.08), run_time=0.8)
        self.at("separate")
        self.play(FadeOut(tk), top.animate.shift(UP * 1.7), bot.animate.shift(DOWN * 1.7), run_time=1.2)
        new_top = strand(BOT, GREEN, 1.3, "3'", "5'")
        new_bot = strand(TOP, GREEN, -1.3, "5'", "3'")
        tk_t = ticks(1.7 - 0.0, 1.95 - 0.0)
        old_lab = T("old strand", 26, BLUE).move_to([5.1, 2.4, 0])
        new_lab = T("new strand", 26, GREEN).move_to([5.1, 1.3, 0])
        old_lab2 = T("old strand", 26, BLUE).move_to([5.1, -2.4, 0])
        new_lab2 = T("new strand", 26, GREEN).move_to([5.1, -1.3, 0])
        self.at("template")
        self.play(FadeIn(old_lab), FadeIn(old_lab2), run_time=0.5)
        self.at("new partner")
        self.play(LaggedStart(*[FadeIn(new_top.L[i], shift=DOWN * 0.3) for i in range(6)],
                              *[FadeIn(new_bot.L[i], shift=UP * 0.3) for i in range(6)], lag_ratio=0.08),
                  FadeIn(new_top.ends), FadeIn(new_bot.ends), FadeIn(new_lab), FadeIn(new_lab2), run_time=1.5)
        t1 = ticks(1.7, 2.0)
        t2 = ticks(-1.7, -2.0)
        self.play(Create(t1), Create(t2), run_time=0.5)
        self.at("photographic negative")
        self.play(Indicate(VGroup(top.L, new_top.L), color=TEXT, scale_factor=1.04), run_time=0.9)
        c1 = T("copy 1", 26, TEXT).move_to([-5.5, 1.85, 0])
        c2 = T("copy 2", 26, TEXT).move_to([-5.5, -1.85, 0])
        self.at("two copies")
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Density(SpokenScene):
    """three tubes: heavy, hybrid, then equal hybrid and light."""

    def construct(self):
        xs = [-2.6, 1.0, 4.6]
        cy = -0.3
        tubes = [RoundedRectangle(corner_radius=0.3, width=1.8, height=4.4, stroke_color=GREY, stroke_width=3).move_to([x, cy, 0])
                 for x in xs]
        ylev = {"light": cy + 0.75, "hybrid": cy - 0.2, "heavy": cy - 1.15}

        def band(x, kind, thick=0.4):
            if kind == "heavy":
                return VGroup(Rectangle(width=1.5, height=thick, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
                              .move_to([x, ylev["heavy"], 0]))
            if kind == "light":
                return VGroup(Rectangle(width=1.5, height=thick, stroke_width=0, fill_color=GREEN, fill_opacity=0.9)
                              .move_to([x, ylev["light"], 0]))
            h = thick / 2
            return VGroup(Rectangle(width=1.5, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).move_to([x, ylev["hybrid"] + h / 2, 0]),
                          Rectangle(width=1.5, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([x, ylev["hybrid"] - h / 2, 0]))

        prop = T("a proposal, not a test", 40, TEXT, font=TITLE_FONT).move_to([0, 0.2, 0])
        self.play(FadeIn(prop), run_time=0.8)
        ecoli = chip("E. coli", GREY, size=30).move_to([-5.0, 0.2, 0])
        hv = chip("heavy nitrogen", BLUE, size=28).move_to([-0.8, 0.2, 0])
        lt = chip("light nitrogen", GREEN, size=28).move_to([4.2, 0.2, 0])
        ar1 = arr(ecoli.get_right() + RIGHT * 0.05, hv.get_left() + LEFT * 0.05, GREY)
        ar2 = arr(hv.get_right() + RIGHT * 0.05, lt.get_left() + LEFT * 0.05, GREY)
        self.at("grew")
        self.play(FadeOut(prop), FadeIn(ecoli), GrowArrow(ar1), FadeIn(hv), run_time=0.8)
        self.at("light nitrogen")
        self.play(GrowArrow(ar2), FadeIn(lt), run_time=0.7)
        tl = [T(s, 24, TEXT).move_to([x, 2.7, 0]) for s, x in zip(["heavy nitrogen", "one generation", "two generations"], xs)]
        self.at("by density")
        self.play(FadeOut(VGroup(ecoli, hv, lt, ar1, ar2)), FadeIn(tubes[0]), FadeIn(tl[0]), FadeIn(band(xs[0], "heavy")), run_time=0.9)
        legend = VGroup(*[T(k, 24, GREY).move_to([-5.55, y, 0]) for k, y in ylev.items()])
        self.play(FadeIn(legend), run_time=0.7)
        key = VGroup(chip("old strand", BLUE, size=22), chip("new strand", GREEN, size=22)).arrange(RIGHT, buff=0.5).move_to([0, -3.15, 0])
        self.at("After one generation")
        self.play(FadeIn(tubes[1]), FadeIn(tl[1]), run_time=0.7)
        self.at("all the DNA")
        self.play(FadeIn(band(xs[1], "hybrid")), FadeIn(key), run_time=0.8)
        self.at("After two")
        self.play(FadeIn(tubes[2]), FadeIn(tl[2]), run_time=0.7)
        self.at("hybrid and light")
        self.play(FadeIn(band(xs[2], "hybrid")), FadeIn(band(xs[2], "light")), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "When strands pair by rule, one strand tells you the other."
