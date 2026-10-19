"""Adaptive immunity: receptors first, antigen chooses  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a lymphocyte and its receptor tip (an unselected cell)
  YELLOW = antigen (the molecule a receptor binds), and the open question
  GREEN  = selected cell and its clone, and the first (primary) response
  PURPLE = V segments        ORANGE = D segments        TEAL = J segments
  GOLD   = junctional variation (nucleotides added or removed), the closing rule
  PINK   = memory cells and the second (secondary) response
  RED    = an idea that was replaced
  GREY   = labels, axes, outlines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#D77AB8"

SIDES = [3, 4, 5, 6, 0]   # tip shapes: triangle, square, pentagon, hexagon, circle
MATCH = 2                 # the pentagon tip is the one the antigen fits


def tip_shape(k, r, color, fill=0.25, sw=4):
    n = SIDES[k]
    if n == 0:
        m = Circle(radius=r * 0.9)
    else:
        m = RegularPolygon(n=n, radius=r)
    m.set_stroke(color, sw).set_fill(color, fill)
    return m


class Cell(VGroup):
    """A lymphocyte as a round body with one stalk and one shaped receptor tip (a schematic, not anatomy)."""

    def __init__(self, x, y, k, s=1.0, color=BLUE):
        super().__init__()
        self.k, self.s = k, s
        self.body = Circle(radius=0.8 * s).set_stroke(color, 4).set_fill(color, 0.18).move_to([x, y, 0])
        self.stalk = Line([x, y + 0.8 * s, 0], [x, y + 1.25 * s, 0], color=color, stroke_width=4)
        self.tip = tip_shape(k, 0.3 * s, color, sw=4).move_to([x, y + 1.55 * s, 0])
        self.add(self.body, self.stalk, self.tip)

    def tipc(self):
        return self.tip.get_center()

    def dimmed(self, o=0.3):
        return [self.body.animate.set_stroke(opacity=o).set_fill(opacity=0.05),
                self.stalk.animate.set_stroke(opacity=o),
                self.tip.animate.set_stroke(opacity=o).set_fill(opacity=0.08)]

    def recolor(self, color):
        return [self.body.animate.set_stroke(color).set_fill(color, 0.2),
                self.stalk.animate.set_stroke(color),
                self.tip.animate.set_stroke(color).set_fill(color, 0.3)]


def antigen(k, s=1.0, at=ORIGIN):
    a = tip_shape(k, 0.36 * s, YELLOW, fill=0.9, sw=3)
    return a.move_to(at)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def row_cells(y, xs=(-4.8, -2.4, 0, 2.4, 4.8), ks=(0, 1, 2, 3, 4), s=1.0):
    return [Cell(x, y, k, s) for x, k in zip(xs, ks)]


class S00Title(TitleCard):
    LESSON = "Adaptive immunity"
    TITLE = "Receptors first, antigen chooses"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        # the unknown: a virus never met
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.6, height=0.95), num_dashes=40)
        box.set_stroke(YELLOW, 4).move_to([-1.6, 2.95, 0])
        q = T("?", 44, YELLOW, weight=BOLD).move_to(box)
        vlab = T("a virus you have never met", 26, YELLOW).next_to(box, RIGHT, buff=0.35)
        self.at("never met")
        self.play(Create(box), FadeIn(q), FadeIn(vlab), run_time=0.9)

        cells = row_cells(0.2)
        self.at("already holds")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.25), run_time=1.6)
        lab = T("lymphocytes: each has receptors of one shape", 26, BLUE).move_to([0, -1.15, 0])
        note = T("a few of millions, not to scale", 22, GREY).next_to(lab, DOWN, buff=0.15)
        self.play(FadeIn(lab), FadeIn(note), run_time=0.6)

        qq = T("Ready for a molecule before it exists in your world?", 32, YELLOW).move_to([0, -2.7, 0])
        self.at("How can a defense")
        self.play(Write(qq), run_time=1.6)
        self.play(*[Indicate(c.tip, color=YELLOW, scale_factor=1.25) for c in cells[:5]], run_time=1.0)
        rule = chip("clonal selection", GREEN, size=36).move_to([0, -2.7, 0])
        self.at("clonal selection")
        self.play(FadeOut(qq), FadeIn(rule, scale=0.9), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Select(SpokenScene):
    def construct(self):
        cells = row_cells(0.9)
        self.at("In vertebrates")
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.15), run_time=1.0)
        head = T("lymphocytes", 28, BLUE).move_to([-5.0, -0.55, 0])
        self.at("white blood cell")
        self.play(FadeIn(head), run_time=0.4)
        self.at("receptors of one specificity")
        self.play(*[Indicate(c.tip, color=BLUE, scale_factor=1.3) for c in cells], run_time=1.0)
        made = T("receptors made first", 28, BLUE).move_to([2.0, -0.55, 0])
        self.at("before it ever meets antigen")
        self.play(FadeOut(head), FadeIn(made), run_time=0.5)

        ag = antigen(MATCH, 1.0, [0, 3.1, 0])
        aglab = T("antigen", 26, YELLOW).next_to(ag, RIGHT, buff=0.25)
        self.at("An antigen is")
        self.play(FadeIn(ag, scale=0.8), FadeIn(aglab), run_time=0.5)
        self.at("When antigen arrives")
        self.play(FadeOut(made), FadeOut(aglab), run_time=0.3)
        self.play(ag.animate.move_to(cells[MATCH].tipc()).scale(0.85), run_time=1.0)
        others = [c for i, c in enumerate(cells) if i != MATCH]
        self.at("only the few")
        self.play(*cells[MATCH].recolor(GREEN), *[a for c in others for a in c.dimmed()], run_time=0.8)
        fit_lab = T("only the cell whose receptor fits", 26, GREEN).move_to([0, -0.55, 0])
        self.play(FadeIn(fit_lab), run_time=0.4)

        # the clone
        self.at("divide into a clone")
        self.play(FadeOut(fit_lab), run_time=0.2)
        parent = cells[MATCH]
        targets = [Cell(x, -2.0, MATCH, 0.55, GREEN) for x in (-4.0, -2.0, 0, 2.0, 4.0)]
        self.play(LaggedStart(*[ReplacementTransform(parent.copy(), t) for t in targets], lag_ratio=0.2), run_time=1.8)
        clab = T("a clone: identical descendants", 28, GREEN).move_to([0, -3.15, 0])
        self.at("identical descendants")
        self.play(FadeIn(clab), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def seg_bar(x, w, y, color, letter):
    bar = RoundedRectangle(corner_radius=0.15, width=w, height=1.5, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.10).move_to([x, y, 0])
    txt = T(f"{letter}   {letter}   {letter}   …", 30, color).set_opacity(0.55).move_to(bar)
    return VGroup(bar, txt)


def seg_block(x, y, color, letter):
    b = RoundedRectangle(corner_radius=0.12, width=1.7, height=1.3, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.35).move_to([x, y, 0])
    return VGroup(b, T(letter, 40, color, weight=BOLD).move_to(b))


class S03Shapes(SpokenScene):
    def construct(self):
        c_gen = chip("about 20,000 protein-coding genes", GREY, size=24).move_to([-3.5, 3.0, 0])
        c_shape = chip("millions of receptor shapes", BLUE, size=24).move_to([4.2, 3.0, 0])
        link = arr(c_gen.get_right() + RIGHT * 0.05, c_shape.get_left() + LEFT * 0.05, YELLOW)
        qm = T("?", 36, YELLOW, weight=BOLD).next_to(link, UP, buff=0.0)
        self.at("millions")
        self.play(FadeIn(c_shape, shift=LEFT * 0.2), run_time=0.5)
        self.at("human genome")
        self.play(FadeIn(c_gen, shift=RIGHT * 0.2), GrowArrow(link), FadeIn(qm), run_time=0.8)

        y = 0.4
        v, d, j = seg_bar(-4.0, 4.2, y, PURPLE, "V"), seg_bar(0.2, 2.8, y, ORANGE, "D"), seg_bar(4.1, 3.0, y, TEAL, "J")
        names = [T("V segments", 26, PURPLE).next_to(v, DOWN, buff=0.2), T("D segments", 26, ORANGE).next_to(d, DOWN, buff=0.2),
                 T("J segments", 26, TEAL).next_to(j, DOWN, buff=0.2)]
        title = T("heavy-chain variable region: gene pieces, not to scale", 26, GREY).move_to([0, 1.85, 0])
        self.at("not encoded as one piece")
        self.play(FadeIn(title), LaggedStart(FadeIn(v), FadeIn(d), FadeIn(j), lag_ratio=0.25), run_time=1.2)
        self.play(*[FadeIn(n) for n in names], run_time=0.5)

        bv, bd, bj = seg_block(-5.0, y, PURPLE, "V"), seg_block(0.9, y, ORANGE, "D"), seg_block(4.0, y, TEAL, "J")
        self.at("joins one V")
        self.play(LaggedStart(FadeIn(bv, scale=1.3), FadeIn(bd, scale=1.3), FadeIn(bj, scale=1.3), lag_ratio=0.3), run_time=1.0)
        self.play(FadeOut(v[0]), FadeOut(v[1]), FadeOut(d[0]), FadeOut(d[1]), FadeOut(j[0]), FadeOut(j[1]),
                  *[FadeOut(n) for n in names], FadeOut(title),
                  bv.animate.move_to([-1.8, y, 0]), bd.animate.move_to([0, y, 0]), bj.animate.move_to([1.8, y, 0]), run_time=1.2)

        rc = chip("somatic recombination", PURPLE, size=28).move_to([0, -2.7, 0])
        self.at("somatic recombination")
        joined = T("one V, one D, one J joined: a heavy-chain variable region", 26, GREY).move_to([0, 1.7, 0])
        self.play(FadeIn(rc), FadeIn(joined), run_time=0.8)

        self.at("added or removed")
        jt = []
        for xj in (-2.1, 2.1):
            m = T("added or\nremoved", 26, GOLD, weight=BOLD, line_spacing=0.8).move_to([xj, y, 0])
            jt.append(m)
        self.play(bv.animate.move_to([-4.2, y, 0]), bj.animate.move_to([4.2, y, 0]), run_time=0.6)
        self.play(*[FadeIn(m, scale=1.4) for m in jt], run_time=0.6)
        jlab = chip("junctional variation", GOLD, size=28).move_to([0, -1.5, 0])
        a1 = arr(jlab.get_top() + LEFT * 0.8, [-2.1, y - 0.55, 0], GOLD, 3, 0.16)
        a2 = arr(jlab.get_top() + RIGHT * 0.8, [2.1, y - 0.55, 0], GOLD, 3, 0.16)
        self.at("junctional variation")
        self.play(FadeIn(jlab), GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def numchip(n, letter, color, size=32):
    return chip(f"{n} {letter}", color, size=size, pad=0.16)


def op(s, size=36):
    return T(s, size, TEXT)


class S04Count(SpokenScene):
    def construct(self):
        x0 = -6.0
        note = T("illustrative human counts, assuming every combination works", 22, GREY).move_to([0, -3.3, 0])
        ask = T("How many receptors can segments make?", 40, YELLOW).move_to([0, 0.3, 0])
        self.at("Count the possibilities")
        self.play(FadeIn(note), Write(ask), run_time=1.4)

        hl = T("heavy chain", 26, GREY).move_to([x0 + 0.9, 3.15, 0])
        hrow = VGroup(numchip(40, "V", PURPLE), op("×"), numchip(23, "D", ORANGE), op("×"), numchip(6, "J", TEAL),
                      op("="), M("5,520", 36)).arrange(RIGHT, buff=0.25)
        hrow.next_to(hl, DOWN, buff=0.2).align_to(hl, LEFT)
        self.at("illustrative human numbers")
        self.play(FadeOut(ask), FadeIn(hl), *[FadeIn(m) for m in hrow[:5]], run_time=1.2)
        self.at("heavy chains")
        self.play(FadeIn(hrow[5]), FadeIn(hrow[6], scale=1.3), run_time=0.6)

        ll = T("light chain", 26, GREY).move_to([x0 + 0.85, 1.35, 0])
        k = VGroup(T("kappa", 28, TEAL), numchip(40, "V", PURPLE), op("×"), numchip(5, "J", TEAL), op("="), M("200", 36)).arrange(RIGHT, buff=0.25)
        lam = VGroup(T("lambda", 28, TEAL), numchip(30, "V", PURPLE), op("×"), numchip(4, "J", TEAL), op("="), M("120", 36)).arrange(RIGHT, buff=0.25)
        k.next_to(ll, DOWN, buff=0.2).align_to(ll, LEFT)
        lam.next_to(k, DOWN, buff=0.25).align_to(k, LEFT)
        self.at("Light chains come")
        self.play(FadeIn(ll), run_time=0.4)
        self.at("Kappa gives")
        self.play(FadeIn(k, shift=RIGHT * 0.2), run_time=0.7)
        self.at("lambda gives")
        self.play(FadeIn(lam, shift=RIGHT * 0.2), run_time=0.7)
        br = Brace(VGroup(k, lam), RIGHT, color=GREY, buff=0.25)
        tot = M("200 + 120 = 320", 32).next_to(br, RIGHT, buff=0.2)
        self.at("That makes")
        self.play(GrowFromCenter(br), FadeIn(tot), run_time=0.8)

        pair = VGroup(M("5,520", 44), op("×", 44), M("320", 44), op("=", 44), M("1,766,400", 44)).arrange(RIGHT, buff=0.3).move_to([0, -1.9, 0])
        plab = T("each B cell pairs one heavy chain with one light chain", 26, GREY).next_to(pair, UP, buff=0.3)
        self.at("pairs one heavy chain")
        self.play(FadeIn(plab), run_time=0.4)
        self.play(*[FadeIn(m) for m in pair[:3]], run_time=0.8)
        self.at("Multiplying")
        self.play(FadeIn(pair[3]), FadeIn(pair[4], scale=1.2), run_time=0.7)
        big = T("about 1.8 million receptors", 44, GREEN, weight=BOLD).move_to([0, -1.9, 0])
        self.at("million")
        self.play(FadeOut(pair), FadeOut(plab), FadeIn(big, scale=0.9), run_time=0.8)
        few = T("from fewer than 150 segments", 28, GREY).move_to([0, -2.75, 0])
        self.at("fewer than")
        self.play(FadeOut(note), FadeIn(few), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Memory(SpokenScene):
    def construct(self):
        ys = 1.95
        xs = (-4.0, -2.0, 0, 2.0, 4.0)
        cells = [Cell(x, ys, k, 0.6) for x, k in zip(xs, (0, 1, 2, 3, 4))]
        sub = T("receptors already made", 26, BLUE).move_to([0, 0.75, 0])
        self.at("No antigen")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.15), FadeIn(sub), run_time=1.3)

        ax = Axes(x_range=[0, 12, 1], y_range=[0, 1.3, 0.5], x_length=10.8, y_length=3.0,
                  axis_config={"color": GREY, "include_ticks": False, "include_numbers": False, "stroke_width": 3},
                  tips=True).move_to([0.5, -1.65, 0])
        xl = T("time", 24, GREY).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
        yl = T("response (relative units)", 24, GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
        sk = T("in this sketch", 24, GREY).move_to(ax.c2p(2.2, 1.12))

        def f(t, t0, a, s):
            u = (t - t0) / s
            return a * u * np.exp(1 - u) if t >= t0 else 0.0

        def y(t):
            return f(t, 0.6, 0.42, 1.7) + f(t, 7.0, 1.0, 0.7)

        prim = ax.plot(y, x_range=[0.6, 7.0], color=GREEN, stroke_width=6)
        sec = ax.plot(y, x_range=[7.0, 11.6], color=PINK, stroke_width=6)
        l1 = T("first response", 24, GREEN).move_to(ax.c2p(3.0, 0.62))
        l2 = T("second response", 24, PINK).move_to(ax.c2p(10.2, 0.95))
        enc2 = DashedLine(ax.c2p(7.0, 0), ax.c2p(7.0, 1.25), color=GREY, stroke_width=3)
        enc1 = DashedLine(ax.c2p(0.6, 0), ax.c2p(0.6, 1.25), color=GREY, stroke_width=3)
        t1 = T("antigen", 22, YELLOW).next_to(enc1, UP, buff=0.05)
        t2 = T("antigen again", 22, YELLOW).next_to(enc2, UP, buff=0.05)

        self.at("After a first response")
        self.play(FadeOut(sub), *[a for i, c in enumerate(cells) if i != MATCH for a in c.dimmed()],
                  *cells[MATCH].recolor(GREEN), run_time=0.5)
        clones = [Cell(x, ys, MATCH, 0.6, GREEN) for x in xs]
        self.play(*[ReplacementTransform(c, t) for c, t in zip(cells, clones)],
                  Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sk), FadeIn(enc1), FadeIn(t1), run_time=0.9)
        self.play(Create(prim), FadeIn(l1), run_time=1.4)
        self.at("most of the expanded")
        keep = (1, 3)
        self.play(*[FadeOut(c) for i, c in enumerate(clones) if i not in keep], run_time=0.9)
        self.at("memory B cells")
        mem = [clones[i] for i in keep]
        self.play(*[m.recolor(PINK)[0] for m in mem], *[m.recolor(PINK)[1] for m in mem], *[m.recolor(PINK)[2] for m in mem], run_time=0.6)
        mlab = T("memory B cells and memory T cells", 26, PINK).move_to([-1.0, 0.9, 0])
        self.play(FadeIn(mlab), run_time=0.5)
        self.at("A second encounter")
        big = [Cell(x, ys, MATCH, 0.6, PINK) for x in np.linspace(-5.25, 5.25, 8)]
        self.play(*[FadeOut(m) for m in mem], LaggedStart(*[FadeIn(c) for c in big], lag_ratio=0.1),
                  mlab.animate.move_to([0, 0.9, 0]), FadeIn(enc2), FadeIn(t2), run_time=1.2)
        self.at("faster and larger")
        self.play(Create(sec), FadeIn(l2), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        # old idea: antigen as template
        y1 = 1.9
        blank = Cell(-4.6, y1, 4, 0.8)
        blab = T("general antibody", 24, GREY).move_to([-4.6, y1 - 0.95, 0])
        ag1 = antigen(MATCH, 0.8, [-2.7, y1 + 0.9, 0])
        ag1lab = T("antigen", 24, YELLOW).next_to(ag1, RIGHT, buff=0.2)
        shaped = Cell(1.6, y1, MATCH, 0.8)
        mid = arr([-1.5, y1 + 0.2, 0], [0.4, y1 + 0.2, 0], GREY)
        tmpl = T("antigen as template", 26, RED).move_to([4.7, y1 + 0.2, 0])
        self.at("Some earlier theories")
        self.play(FadeIn(blank), FadeIn(ag1), FadeIn(ag1lab), FadeIn(blab), run_time=0.8)
        self.at("folding a general antibody")
        self.play(GrowArrow(mid), FadeIn(shaped), ag1.animate.move_to(shaped.tipc()).scale(0.85), FadeOut(ag1lab),
                  FadeIn(tmpl), run_time=1.3)
        xa = VGroup(Line([-6.0, y1 + 1.35, 0], [6.0, y1 - 1.0, 0], color=RED, stroke_width=8),
                    Line([-6.0, y1 - 1.0, 0], [6.0, y1 + 1.35, 0], color=RED, stroke_width=8))
        self.at("Clonal selection replaced")
        self.play(Create(xa), run_time=0.8)
        old = VGroup(blank, ag1, shaped, mid, tmpl, blab)
        self.play(old.animate.set_opacity(0.35), xa.animate.set_opacity(0.6), run_time=0.4)

        # new idea: selection
        y2 = -1.5
        cells = [Cell(x, y2, k, 0.8) for x, k in zip((-5.6, -4.0, -2.4, -0.8), (0, 1, 3, 2))]
        newlab = T("clonal selection", 26, GREEN).move_to([-3.2, y2 - 0.98, 0])
        self.at("Receptors are made first")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.2), FadeIn(newlab), run_time=1.4)
        ag2 = antigen(MATCH, 0.8, [0.8, y2 + 2.0, 0])
        self.at("Antigen finds the cells")
        self.play(FadeIn(ag2, scale=0.8), run_time=0.4)
        self.play(ag2.animate.move_to(cells[3].tipc()).scale(0.85), run_time=0.7)
        self.play(*cells[3].recolor(GREEN), *[a for i, c in enumerate(cells) if i != 3 for a in c.dimmed()], run_time=0.6)
        self.at("become a clone")
        carr = arr([0.0, y2, 0], [1.2, y2, 0], GREEN)
        clones = [Cell(x, y2, MATCH, 0.8, GREEN) for x in (2.0, 3.6, 5.2)]
        self.play(GrowArrow(carr), LaggedStart(*[ReplacementTransform(cells[3].copy(), t) for t in clones], lag_ratio=0.25), run_time=1.4)
        rule = T("The antigen chooses. It does not shape.", 38, GOLD, font=TITLE_FONT).move_to([0, -3.3, 0])
        self.at("Keep this rule")
        self.play(Write(rule), run_time=1.6)
        self.finish()


class S07End(EndCard):
    LINE = "The antigen chooses. It does not shape."
