"""Evidence workshop: wells share one scoop of water  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the water sample (the scoop, the cup)
  YELLOW = the target DNA / the species
  PURPLE = the lab steps (extraction, qPCR wells)
  GREEN  = amplification / detection / a stop-worthy result
  RED    = a miss, an error, DNA absent from the scoop
  ORANGE = the probability that the pond is occupied (prior and posteriors)
  GOLD   = the 5% stop line
  GREY   = outlines, negative wells, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def well(size=0.7):
    box = RoundedRectangle(corner_radius=0.1, width=size, height=size, stroke_color=PURPLE, stroke_width=3,
                           fill_color=PURPLE, fill_opacity=0.12)
    z = M("0", 26, TEXT).move_to(box).set_opacity(0)
    g = VGroup(box, z)
    g.box, g.zero = box, z
    return g


def grid(rows, cols, size, gap, center, row_gaps=None):
    """rows x cols wells; row_gaps = extra space after given row index."""
    row_gaps = row_gaps or {}
    ws, ys, y = [], [], 0.0
    for r in range(rows):
        ys.append(y)
        y -= size + gap + row_gaps.get(r, 0)
    cy = (ys[0] + ys[-1]) / 2
    for r in range(rows):
        row = []
        for c in range(cols):
            w = well(size).move_to([(c - (cols - 1) / 2) * (size + gap) + center[0], ys[r] - cy + center[1], 0])
            row.append(w)
        ws.append(row)
    return ws


def neg(w):
    return [w.box.animate.set_fill(GREY, 0.35).set_stroke(GREY), w.zero.animate.set_opacity(1)]


def cup(scale=1.0, color=BLUE):
    body = Polygon([-0.55, 0.4, 0], [0.55, 0.4, 0], [0.38, -0.4, 0], [-0.38, -0.4, 0], stroke_color=color,
                   stroke_width=4, fill_color=color, fill_opacity=0.25)
    return body.scale(scale)


def pond(w=5.6, h=4.4):
    return Ellipse(width=w, height=h, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.12)


def dots(pts, r=0.13, color=YELLOW):
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([x, y, 0]) for x, y in pts])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S00Title(TitleCard):
    LESSON = "Integrative evidence workshop"
    TITLE = "Wells share one scoop of water"



# ------------------------------------------------------------------------------------------
class S01Pond(SpokenScene):
    def construct(self):
        pd = pond(5.2, 4.8).move_to([-3.5, -0.1, 0])
        pl = T("pond S2", 30, BLUE).move_to([-3.5, -2.9, 0])
        ws = grid(4, 5, 0.9, 0.25, (3.4, -0.1), row_gaps={1: 0.4})
        flat = [w for r in ws for w in r]
        head = T("20 qPCR wells", 30, PURPLE).move_to([3.4, 3.0, 0])
        self.at("Pond S2")
        self.play(FadeIn(pd), FadeIn(pl), run_time=0.7)
        self.at("qPCR wells")
        self.play(FadeIn(head), LaggedStart(*[FadeIn(w, scale=0.8) for w in flat], lag_ratio=0.05), run_time=1.6)
        self.at("Every one is negative")
        self.play(LaggedStart(*[AnimationGroup(*neg(w)) for w in flat], lag_ratio=0.05), run_time=1.6)
        q = T("?", 140, YELLOW, weight=BOLD).move_to(pd)
        self.at("Is the species gone")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("Not yet")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=0.6)
        fn = chip("false negative = a miss", RED, 28).move_to([3.4, -3.3, 0])
        self.at("A false negative is a miss")
        self.play(FadeIn(fn, shift=UP * 0.1), run_time=0.5)
        dna = dots([(-4.7, 0.7), (-3.3, 1.1), (-4.1, -0.6), (-2.7, -0.3), (-2.2, 0.6), (-3.6, 0.1)], r=0.17)
        self.at("The organism or its DNA is present")
        self.play(FadeOut(q), FadeIn(dna, lag_ratio=0.1), run_time=0.8)
        self.at("nothing amplifies")
        self.play(Indicate(VGroup(*flat), color=RED, scale_factor=1.04), run_time=0.8)
        self.at("follow the DNA")
        self.play(GrowArrow(arr([-0.8, 0, 0], [0.4, 0, 0], YELLOW)), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------
class S02Nets(SpokenScene):
    def construct(self):
        ys = [1.9, 0.1, -1.7]
        gaps = [[-4.6, -2.5, -0.4], [-4.6, -0.4], [-0.4]]
        cols = [BLUE, PURPLE, PURPLE]
        labels = [("scoop: DNA in the water", "0.60", "our choice", BLUE),
                  ("extraction: captures it", "0.49", "estimate: wild pig study\n(one species, one region)", PURPLE),
                  ("qPCR run: amplifies it", "0.38", "estimate: wild pig study\n(one species, one region)", PURPLE)]
        nets = []
        for y, gp, col in zip(ys, gaps, cols):
            segs, left = [], -6.0
            for g in gp + [99]:
                right = min(g - 0.45, 0.8)
                if right > left:
                    segs.append(Line([left, y, 0], [right, y, 0], color=col, stroke_width=10))
                left = g + 0.45
            nets.append(VGroup(*segs))
        d = dots([(-4.6, 3.3)], r=0.2)
        chipsR = []
        for (nm, pr, note, col), y in zip(labels, ys):
            c = VGroup(T(nm, 28, col), M(pr, 44, col, weight=BOLD), T(note, 24, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            c.move_to([4.0, y, 0]).align_to([2.1, 0, 0], LEFT)
            chipsR.append(c)
        self.at("three nets")
        self.play(FadeIn(d), run_time=0.4)
        self.at("First, DNA must be in the water")
        self.play(Create(nets[0]), FadeIn(chipsR[0], shift=LEFT * 0.2), run_time=0.8)
        self.play(d[0].animate.move_to([-4.6, 1.9, 0]), run_time=0.6)
        self.at("Second, the extraction must capture it")
        self.play(Create(nets[1]), FadeIn(chipsR[1], shift=LEFT * 0.2), run_time=0.8)
        self.play(d[0].animate.move_to([-4.6, 0.1, 0]), run_time=0.6)
        self.at("Third, a qPCR run must amplify it")
        self.play(Create(nets[2]), FadeIn(chipsR[2], shift=LEFT * 0.2), run_time=0.8)
        self.play(d[0].animate.move_to([-4.6, -1.4, 0]), run_time=0.6)
        self.at("Each net can let the signal slip through")
        self.play(d[0].animate.set_opacity(0.35), Indicate(nets[2], color=RED, scale_factor=1.0), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------
class S03Lab(SpokenScene):
    def construct(self):
        xs = [-0.1 + 1.4 * i for i in range(5)]
        y1, y2 = 1.4, -1.1
        w1 = [well(1.1).move_to([x, y1, 0]) for x in xs]
        w2 = [well(1.1).move_to([x, y2, 0]) for x in xs]
        c = cup(1.4).move_to([-5.55, (y1 + y2) / 2, 0])
        cl = T("one water", 24, BLUE).next_to(c, UP, buff=0.55)
        cl2 = T("sample", 24, BLUE).next_to(cl, DOWN, buff=0.05)
        cll = VGroup(cl, cl2)
        e1 = chip("extraction 1", PURPLE, 26).move_to([-3.2, y1, 0])
        e2 = chip("extraction 2", PURPLE, 26).move_to([-3.2, y2, 0])
        top = [1.9, 2.9]
        self.at("Start with the lab")
        self.play(FadeIn(c), FadeIn(cll), FadeIn(e1), LaggedStart(*[FadeIn(w, scale=0.8) for w in w1], lag_ratio=0.1),
                  run_time=1.0)
        lab1 = M("one run misses: 0.62", 32, RED).move_to([0.9, 2.95, 0])
        self.at("One run misses")
        self.play(*neg(w1[0]), w1[0].box.animate.set_stroke(RED), FadeIn(lab1), run_time=0.6)
        lab5 = M("0.62 x 0.62 x 0.62 x 0.62 x 0.62 = 0.092", 27, RED).move_to([0.9, 2.95, 0])
        self.at("All five runs miss")
        self.play(*[a for w in w1[1:] for a in (neg(w) + [w.box.animate.set_stroke(RED)])], ReplacementTransform(lab1, lab5), run_time=1.0)
        labA = M("5 runs detect captured DNA: 0.908", 32, GREEN).move_to([0.9, 2.95, 0])
        self.at("five runs amplify")
        self.play(*[a for w in w1 for a in (w.box.animate.set_fill(PURPLE, 0.12).set_stroke(GREEN), w.zero.animate.set_opacity(0))],
                  ReplacementTransform(lab5, labA), run_time=0.9)
        cap1 = M("0.49", 28, PURPLE, weight=BOLD).next_to(e1, UP, buff=0.12)
        self.at("Add the capture step")
        self.play(FadeIn(cap1, shift=DOWN * 0.1), Indicate(e1, color=PURPLE), run_time=0.7)
        cap2 = M("0.49", 28, PURPLE, weight=BOLD).next_to(e2, UP, buff=0.12)
        self.at("two extractions")
        self.play(FadeIn(e2), FadeIn(cap2), LaggedStart(*[FadeIn(w, scale=0.8) for w in w2], lag_ratio=0.1), run_time=1.0)
        res = M("lab side detects: 0.692", 38, GREEN, weight=BOLD).move_to([1.5, -2.85, 0])
        self.at("detect with probability")
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------
class S04Ceiling(SpokenScene):
    L = 10.8
    X0 = -5.4

    def px(self, v):
        return self.X0 + self.L * v

    def construct(self):
        y, h = 0.7, 1.7
        ay = y - h / 2 - 0.1
        axis = Line([self.px(0), ay, 0], [self.px(1), ay, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[Line([self.px(v), ay - 0.15, 0], [self.px(v), ay + 0.15, 0], color=GREY) for v in (0, 1)])
        t0 = M("0", 26, GREY).move_to([self.px(0), ay - 0.5, 0])
        t1 = M("1", 26, GREY).move_to([self.px(1), ay - 0.5, 0])
        tl = T("chance of detecting an occupied pond", 26, GREY).move_to([0.0, ay - 2.45, 0])
        tag = T("in this sketch", 24, GREY).to_corner(UR, buff=0.5)
        self.play(FadeIn(axis), FadeIn(ticks), FadeIn(t0), FadeIn(t1), FadeIn(tl), FadeIn(tag), run_time=0.1)

        def bar(a, b, color, op=0.35):
            return Rectangle(width=self.L * (b - a), height=h, stroke_color=color, stroke_width=3, fill_color=color,
                             fill_opacity=op).move_to([self.px((a + b) / 2), y, 0])
        scoop = bar(0, 0.6, BLUE)
        scoopl = M("scoop 0.6", 30, BLUE).move_to([self.px(0.3), y + h / 2 + 0.4, 0])
        self.at("Now the scoop")
        self.play(GrowFromEdge(scoop, LEFT), FadeIn(scoopl), run_time=0.9)
        lab = bar(0, 0.415, PURPLE, 0.55)
        labl = M("one sample 0.415", 30, PURPLE).move_to([self.px(0.415) - 1.9, ay - 1.35, 0])
        self.at("gives")
        self.play(GrowFromEdge(lab, LEFT), run_time=0.9)
        self.at("That is the chance one water sample")
        self.play(FadeIn(labl), run_time=0.5)
        self.at("Could more wells fix it")
        lab2 = bar(0, 0.6, PURPLE, 0.55)
        perf = T("perfect lab work", 30, PURPLE).move_to([self.px(0.3), ay - 1.35, 0])
        self.play(ReplacementTransform(lab, lab2), FadeOut(labl), FadeIn(perf), run_time=1.0)
        ceil = DashedLine([self.px(0.6), y + h / 2 + 0.3, 0], [self.px(0.6), y - h / 2, 0], color=RED, stroke_width=5)
        cl = T("ceiling", 28, RED).move_to([self.px(0.6) + 0.9, y + h / 2 + 0.4, 0])
        self.at("no more than")
        self.play(Create(ceil), FadeIn(cl), run_time=0.7)
        nod = bar(0.6, 1.0, RED, 0.18)
        nodl = T("no DNA in the scoop", 28, RED).move_to([self.px(0.8), y, 0])
        self.at("If the scoop held no DNA")
        self.play(FadeIn(nod), FadeIn(nodl), run_time=0.7)
        self.at("no number of runs")
        self.play(Indicate(nodl, color=RED, scale_factor=1.1), Indicate(nod, color=RED, scale_factor=1.0), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------
class S05Samples(SpokenScene):
    def construct(self):
        bx = [-4.2, -0.9, 2.4]
        base = -1.2
        H = 16.0   # screen units per 100 %

        def hgt(p):
            return p * H
        axis = Line([-5.9, base, 0], [5.9, base, 0], color=GREY, stroke_width=3)
        ytitle = T("chance the pond is still occupied", 26, GREY).to_corner(UL, buff=0.45)
        tagw = T("worked example, in this sketch", 24, GREY).to_corner(UR, buff=0.45)
        ysl = base + hgt(0.05)
        stop = DashedLine([-5.9, ysl, 0], [5.9, ysl, 0], color=GOLD, stroke_width=4)
        stopl = M("stop line 5%", 26, GOLD).move_to([5.0, ysl + 0.3, 0])

        def cups(n, x):
            return VGroup(*[cup(0.7) for _ in range(n)]).arrange(RIGHT, buff=0.2).move_to([x, base - 0.75, 0])
        cups2, cups3 = cups(2, bx[1]), cups(3, bx[2])
        self.play(FadeIn(axis), FadeIn(tagw), run_time=0.1)
        sx = lambda v: -5.4 + 10.8 * v
        s_blue = Rectangle(width=10.8 * 0.6, height=1.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35
                           ).move_to([sx(0.3), 2.0, 0])
        s_red = Rectangle(width=10.8 * 0.4, height=1.3, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.18
                          ).move_to([sx(0.8), 2.0, 0])
        s_bl = M("if occupied: DNA in scoop 0.6", 26, BLUE).move_to(s_blue)
        s_rl = T("40% chance:\nno DNA in the scoop", 26, RED).move_to(s_red)
        strip = VGroup(s_blue, s_red, s_bl, s_rl)
        self.at("Only another independent water sample")
        self.play(FadeIn(strip), FadeIn(cups2[0], scale=0.8), run_time=0.6)
        self.play(FadeIn(cups2[1], scale=0.8), run_time=0.4)
        self.at("that the scoop holds no DNA")
        self.play(Indicate(s_red, color=RED, scale_factor=1.04), run_time=0.8)
        miss = M("0.585 x 0.585 = 0.342", 28, RED).move_to([bx[1], base - 1.8, 0])
        self.at("Two samples both miss")
        self.play(FadeIn(miss, shift=UP * 0.1), FadeOut(strip), run_time=0.6)

        def mkbar(p, x, col=ORANGE):
            return Rectangle(width=1.8, height=hgt(p), stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.4
                             ).move_to([x, base + hgt(p) / 2, 0])
        b0 = mkbar(0.20, bx[0])
        l0 = M("prior 0.2", 30, ORANGE).next_to(b0, UP, buff=0.15)
        self.at("Start from a prior")
        self.play(GrowFromEdge(b0, DOWN), FadeIn(l0), FadeIn(ytitle), run_time=0.9)
        b1 = mkbar(0.079, bx[1])
        l1 = M("7.9%", 32, ORANGE, weight=BOLD).next_to(b1, UP, buff=0.15)
        self.at("rule then gives")
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.9)
        self.at("The team stops only")
        self.play(Create(stop), FadeIn(stopl), run_time=0.8)
        again = T("sample again", 30, RED, weight=BOLD).next_to(l1, UP, buff=0.3)
        self.at("so it samples again")
        self.play(b1.animate.set_stroke(RED).set_fill(RED, 0.4), FadeIn(again), run_time=0.6)
        self.at("A third negative sample")
        self.play(FadeIn(cups3, lag_ratio=0.2), run_time=0.8)
        b2 = mkbar(0.048, bx[2], GREEN)
        l2 = M("4.8%", 32, GREEN, weight=BOLD).next_to(b2, UP, buff=0.15)
        self.at("just under the line")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        base = -2.0
        H = 40.0

        def hgt(p):
            return p * H
        axis = Line([-5.9, base, 0], [5.9, base, 0], color=GREY, stroke_width=3)
        ysl = base + hgt(0.05)
        stop = DashedLine([-5.9, ysl, 0], [5.9, ysl, 0], color=GOLD, stroke_width=4)
        stopl = M("stop line 5%", 26, GOLD).move_to([4.7, ysl + 0.3, 0])
        wells = VGroup(*[well(0.55) for _ in range(20)]).arrange_in_grid(4, 5, buff=0.14).move_to([-3.0, 1.75, 0])
        for w in wells:
            w.zero.set_opacity(0)
            w.box.set_fill(GREY, 0.35).set_stroke(GREY)
        tries = T("20 wells counted as 20 tries", 28, RED).move_to([-3.0, -0.55, 0])
        self.at("Now count the")
        tagw = T("worked example, in this sketch", 24, GREY).move_to([0, -3.4, 0])
        self.play(FadeIn(axis), Create(stop), FadeIn(stopl), FadeIn(wells, lag_ratio=0.03), FadeIn(tagw), run_time=1.2)
        self.play(FadeIn(tries), run_time=0.4)
        ps = chip("pseudoreplication", RED, 32).move_to([3.0, 3.0, 0])
        self.at("That is pseudo replication")
        self.play(FadeIn(ps, shift=DOWN * 0.1), run_time=0.6)
        b = Rectangle(width=1.8, height=hgt(0.023), stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.4
                      ).move_to([2.2, base + hgt(0.023) / 2, 0])
        bl = M("2.3%", 32, RED, weight=BOLD).next_to(b, UP, buff=0.15)
        self.at("and you would stop")
        self.play(GrowFromEdge(b, DOWN), FadeIn(bl), run_time=0.9)
        err = T("an error in the model, not evidence", 28, RED).move_to([3.0, 1.7, 0])
        self.at("an error in the model")
        self.play(FadeIn(err), run_time=0.6)
        self.at("Even the honest numbers")
        self.play(FadeOut(VGroup(axis, stop, stopl, wells, tries, ps, b, bl, err)), run_time=0.6)
        cs = VGroup(chip("0.6 scoop chance", BLUE, 32), chip("prior 0.2", ORANGE, 32), chip("stop line 5%", GOLD, 32)
                    ).arrange(RIGHT, buff=0.5).move_to([0, 0.4, 0])
        ch = T("our choices", 36, TEXT).next_to(cs, UP, buff=0.5)
        self.at("the prior")
        self.play(FadeIn(cs, lag_ratio=0.3), FadeIn(ch), run_time=1.2)
        self.at("Changing them can change")
        self.play(Indicate(cs, color=YELLOW, scale_factor=1.06), run_time=0.8)
        c1 = cup(2.0).move_to([-3.3, 0.9, 0])
        ws = VGroup(*[well(0.5) for _ in range(10)]).arrange_in_grid(2, 5, buff=0.12).move_to([-3.3, -1.9, 0])
        for w in ws:
            w.box.set_fill(GREY, 0.35).set_stroke(GREY)
        lnk = VGroup(*[Line(c1.get_bottom(), w.get_top(), color=GREY, stroke_width=2) for w in ws[:5]])
        shared = T("one sample, one scoop", 30, BLUE).move_to([-3.3, 2.5, 0])
        self.at("Wells from one sample")
        self.play(FadeOut(VGroup(cs, ch, tagw)), run_time=0.3)
        self.play(FadeIn(c1), FadeIn(ws), FadeIn(lnk), FadeIn(shared), run_time=0.8)
        new = VGroup(*[cup(1.5) for _ in range(3)]).arrange(RIGHT, buff=0.4).move_to([3.4, 0.9, 0])
        newl = T("new samples, new tries", 30, GREEN).move_to([3.4, 2.5, 0])
        self.at("Only new water samples")
        self.play(FadeIn(new, lag_ratio=0.25), FadeIn(newl), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Wells share one scoop. Only new water samples are new tries."
