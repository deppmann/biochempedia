"""The wiring problem: rules wire a brain, not lists  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = genes and the on/off label code they make
  YELLOW = neurons, axons, growth cones, terminals
  GREY   = synapse count, target cells, axes, de-emphasized
  ORANGE = the receptor gradient (retina side)
  PURPLE = the cue gradient (target side)
  TEAL   = a rule (the compressed answer)
  GREEN  = activity, firing together, a branch that is kept
  RED    = the unknown, a branch that is removed, activity blocked
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def toggle(on=False, color=BLUE, scale=1.0):
    c = color if on else GREY
    body = RoundedRectangle(corner_radius=0.5, width=2.0, height=1.0, stroke_color=c, stroke_width=5,
                            fill_color=c, fill_opacity=0.25)
    knob = Circle(radius=0.36, stroke_width=0, fill_color=TEXT, fill_opacity=1)
    knob.move_to(body.get_center() + RIGHT * (0.5 if on else -0.5))
    g = VGroup(body, knob)
    g.body, g.knob = body, knob
    g.scale(scale)
    return g


def flip(sw, on, color=BLUE):
    off = sw.body.width * 0.25
    c = color if on else GREY
    tgt = sw.body.get_center() + RIGHT * (off if on else -off)
    return [sw.knob.animate.move_to(tgt), sw.body.animate.set_stroke(c).set_fill(c, 0.25)]


def cell(r=0.3, color=YELLOW):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3)


def strip(bits, side=0.22, color=BLUE):
    """a label code: a row of squares, filled where the gene is on."""
    sq = VGroup()
    for b in bits:
        s = Square(side_length=side, stroke_color=color if b else GREY, stroke_width=2,
                   fill_color=color, fill_opacity=0.9 if b else 0.0)
        sq.add(s)
    return sq.arrange(RIGHT, buff=0.04)


def labelled_cell(bits, r=0.3, side=0.22):
    c = cell(r)
    s = strip(bits, side=side).next_to(c, DOWN, buff=0.12)
    return VGroup(c, s)


def pw(n, size=24, color=GREY):
    """10 to the power n, drawn as plain text with a raised, smaller exponent."""
    base = M("10", size, color)
    e = M(str(n), int(size * 0.65), color).next_to(base, UR, buff=0.02).shift(DOWN * 0.12)
    return VGroup(base, e)


def sup(n):
    return "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(d)] for d in str(n))


class S00Title(TitleCard):
    LESSON = "The wiring problem"
    TITLE = "Rules wire a brain, not lists"


# ---------------------------------------------------------------------------------------------
class S01Numbers(SpokenScene):
    """three bars on a powers-of-ten axis: neurons, genes, synapses; then the question."""

    def construct(self):
        X0, K = -6.0, 0.95
        X = lambda v: X0 + (v - 3) * K
        ax_y = -2.35
        axis = Line([X0, ax_y, 0], [X(15.3), ax_y, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for v in (4, 8, 12):
            ticks.add(Line([X(v), ax_y + 0.1, 0], [X(v), ax_y - 0.1, 0], color=GREY, stroke_width=3))
            ticks.add(pw(v, 24, GREY).move_to([X(v), ax_y - 0.42, 0]))
        scale_lbl = T("a scale in powers of ten", 22, GREY).move_to([0, -3.3, 0])
        self.play(Create(axis), FadeIn(ticks), FadeIn(scale_lbl), run_time=0.45)

        def row(y, v, color, label, lcolor):
            w = X(v) - X0
            bar = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=color, fill_opacity=0.85)
            bar.move_to([X0 + w / 2, y, 0])
            lab = T(label, 26, lcolor).move_to([X0, y + 0.55, 0], aligned_edge=LEFT)
            return bar, lab

        n_bar, n_lab = row(1.9, 10.93, YELLOW, "neurons · about 86 billion", YELLOW)
        g_bar, g_lab = row(0.25, 4.3, BLUE, "genes · about 20,000", BLUE)
        s_bar, s_lab = row(-1.4, 14.0, GREY, "synapses · on the order of 100 trillion", TEXT)

        self.at("human brain")
        self.play(FadeIn(n_lab), GrowFromEdge(n_bar, LEFT), run_time=1.6)
        self.at("genome that builds")
        self.play(FadeIn(g_lab), GrowFromEdge(g_bar, LEFT), run_time=1.2)
        self.at("on the order")
        self.play(FadeIn(s_lab), GrowFromEdge(s_bar, LEFT), run_time=1.6)

        mill = T("× millions", 24, YELLOW).move_to([X(10.93) + 1.1, 1.9, 0])
        bill = T("× billions", 24, TEXT).move_to([5.4, -1.4, 0])
        self.at("fewer than the neurons")
        self.play(Indicate(g_bar, color=BLUE, scale_factor=1.0), FadeIn(mill), run_time=0.8)
        self.at("fewer than the synapses")
        self.play(Indicate(g_bar, color=BLUE, scale_factor=1.0), FadeIn(bill), run_time=0.8)

        gy = 0.25
        d1 = DashedLine([X(4.3) + 0.2, gy, 0], [X(14.0), gy, 0], color=RED, stroke_width=4)
        d2 = DashedLine([X(10.93), 1.65, 0], [X(10.93), gy, 0], color=RED, stroke_width=4)
        d3 = DashedLine([X(14.0), -1.15, 0], [X(14.0), gy, 0], color=RED, stroke_width=4)
        self.at("How does the smaller")
        self.play(Create(d1), Create(d2), Create(d3), run_time=1.2)
        q = bchip("?", RED, 40).move_to([-0.6, gy, 0])
        self.at("wire the larger")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.play(Indicate(q, color=RED, scale_factor=1.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Labels(SpokenScene):
    """a row of on/off genes; each added gene doubles the labels; 72 genes give 4.7e21."""

    def construct(self):
        # --- one neuron with a label code ------------------------------------------------
        one = labelled_cell([1, 0, 1], r=0.55, side=0.4).move_to([0, -0.2, 0])
        tag = T("a label", 32, BLUE).next_to(one, DOWN, buff=0.35)
        self.at("Labels are cheap")
        self.play(FadeIn(one, scale=0.8), FadeIn(tag), run_time=0.8)

        # --- seventy-two genes, each on or off --------------------------------------------
        sws = VGroup(*[toggle(False, scale=0.4) for _ in range(8)]).arrange(RIGHT, buff=0.2)
        sws.scale(1.25).move_to([-0.5, 2.3, 0])
        dots = T("…", 40, GREY).next_to(sws, RIGHT, buff=0.25)
        glab = T("72 genes, each on or off", 30, BLUE).move_to([-0.5, 3.15, 0])
        self.at("let each one")
        self.play(FadeIn(glab), FadeIn(sws, lag_ratio=0.1), FadeIn(dots), run_time=1.0)
        self.at("on or off")
        pattern = [1, 0, 1, 1, 0, 1, 0, 0]
        self.play(*[a for sw, on in zip(sws, pattern) if on for a in flip(sw, True)], run_time=0.8)

        # --- each extra gene doubles the labels ---------------------------------------------
        def family(n):
            cells = VGroup()
            count = 2 ** n
            sp = 9.0 / count if count > 2 else 3.2
            xs = [(-4.5 + i * sp + sp / 2) if count > 2 else (-1.6 + i * 3.2) for i in range(count)]
            if count == 2:
                xs = [-1.6, 1.6]
            for i, x in enumerate(xs):
                bits = [(i >> (n - 1 - j)) & 1 for j in range(n)]
                rr, sd = {1: (0.55, 0.4), 2: (0.5, 0.34), 3: (0.42, 0.27)}[n]
                cells.add(labelled_cell(bits, r=rr, side=sd).move_to([x, -0.2, 0]))
            return cells

        def readout(n):
            return VGroup(T(f"{n} gene" + ("s" if n > 1 else ""), 34, BLUE),
                          M(f"→ {2 ** n} labels", 38, TEXT)).arrange(RIGHT, buff=0.35).move_to([0, -2.4, 0])

        fam = [family(n) for n in (1, 2, 3)]
        ro = [readout(n) for n in (1, 2, 3)]
        self.at("Every extra gene")
        self.play(FadeOut(one), FadeOut(tag), FadeIn(fam[0]), FadeIn(ro[0]), run_time=0.7)
        self.at("doubles the number")
        self.play(ReplacementTransform(fam[0], fam[1]), ReplacementTransform(ro[0], ro[1]), run_time=0.8)
        self.at("combinations")
        self.play(ReplacementTransform(fam[1], fam[2]), ReplacementTransform(ro[1], ro[2]), run_time=0.8)

        # --- 72 genes -----------------------------------------------------------------------
        big = M("2" + sup(72) + " ≈ 4.7 × 10" + sup(21) + " labels", 44, BLUE).move_to([0, 0.5, 0])
        self.at("give about")
        self.play(FadeOut(fam[2]), FadeOut(ro[2]), FadeIn(big, scale=0.9), run_time=0.9)
        neu = M("neurons ≈ 8.6 × 10" + sup(10), 40, YELLOW).move_to([0, -0.9, 0])
        self.at("That is more than")
        self.play(FadeIn(neu, shift=UP * 0.15), run_time=0.6)
        more = T("more than 10" + sup(10) + " times as many labels as neurons", 34).move_to([0, -2.4, 0])
        self.at("billion times")
        self.play(FadeIn(more, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Partner(SpokenScene):
    """a tag says who a cell is, not whom it should meet; the long list folds into rules."""

    def construct(self):
        me = labelled_cell([1, 0, 1], r=0.6, side=0.3).move_to([-4.6, 0.2, 0])
        tag = T("tag", 32, BLUE).next_to(me, DOWN, buff=0.3)
        self.at("But a label")
        self.play(FadeIn(me, scale=0.8), run_time=0.7)
        self.at("A tag says")
        self.play(FadeIn(tag), run_time=0.5)

        # the field of other cells
        field = VGroup()
        cols, rows_ = 8, 6
        for i in range(cols):
            for j in range(rows_):
                field.add(Circle(radius=0.2, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35)
                          .move_to([-1.6 + i * 0.95, 2.4 - j * 0.9, 0]))
        self.at("nothing about")
        self.play(FadeIn(field, lag_ratio=0.02), run_time=1.6)

        picks = [3, 9, 20, 28, 37, 44]
        lines, qs = VGroup(), VGroup()
        for k in picks:
            tgt = field[k].get_center()
            lines.add(DashedLine(me.get_center() + RIGHT * 0.55, tgt + LEFT * 0.22, color=RED, stroke_width=2.5))
            qs.add(T("?", 28, RED, weight=BOLD).move_to(tgt))
        self.at("should connect")
        self.play(Create(lines, lag_ratio=0.15), FadeIn(qs, lag_ratio=0.15), run_time=1.6)

        # --- the long list versus the short list ------------------------------------------------
        self.at("A list with")
        self.play(FadeOut(field), FadeOut(lines), FadeOut(qs), FadeOut(me), FadeOut(tag), run_time=0.6)
        col = VGroup(*[Rectangle(width=3.0, height=0.17, stroke_width=0, fill_color=GREY, fill_opacity=0.7)
                       for _ in range(24)]).arrange(DOWN, buff=0.05).move_to([3.0, -0.2, 0])
        col_lbl = T("one instruction for each synapse", 26, GREY).next_to(col, UP, buff=0.2)
        col_lbl.move_to([3.0, col.get_top()[1] + 0.35, 0])
        self.play(FadeIn(col_lbl), FadeIn(col, lag_ratio=0.05), run_time=2.0)
        genes = VGroup(*[Rectangle(width=3.0, height=0.17, stroke_width=0, fill_color=BLUE, fill_opacity=0.85)
                         for _ in range(2)]).arrange(DOWN, buff=0.05).move_to([-3.2, -0.2, 0])
        g_lbl = T("list of genes", 28, BLUE).move_to([-3.2, 0.4, 0])
        self.at("list of genes")
        self.play(FadeIn(genes), FadeIn(g_lbl), run_time=0.6)
        scale_note = T("not to scale", 22, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(scale_note), run_time=0.4)

        rules = bchip("rules", TEAL, 44).move_to([3.0, -0.2, 0])
        self.at("compressed into rules")
        self.play(ReplacementTransform(col, rules), FadeOut(col_lbl), FadeOut(scale_note), run_time=1.2)
        spots = [(-0.2, 2.4), (2.4, 2.6), (5.0, 2.4), (-0.2, -2.7), (2.4, -2.7), (5.0, -2.7)]
        copies = [bchip("rule", TEAL, 26).move_to([x, y, 0]) for x, y in spots]
        self.at("apply in many")
        self.play(*[TransformFromCopy(rules, c) for c in copies], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gradient(SpokenScene):
    """receptor gradient in the retina, cue gradient in the target; growth cones stop at their level."""

    def construct(self):
        N = 24
        top, bot = 2.4, -2.4
        slice_h = (top - bot) / N

        # target: horizontal band, amount rises left to right
        tx0, tx1 = -1.0, 6.0
        sw = (tx1 - tx0) / N
        t_slices = VGroup(*[Rectangle(width=sw, height=top - bot, stroke_width=0, fill_color=GREY,
                                      fill_opacity=0.08 + 0.55 * i / (N - 1)).move_to([tx0 + sw * (i + .5), 0, 0])
                            for i in range(N)])
        t_frame = Rectangle(width=tx1 - tx0, height=top - bot, stroke_color=GREY, stroke_width=2).move_to([(tx0 + tx1) / 2, 0, 0])
        rule = bchip("Rule 1: a gradient", TEAL, 28).move_to([-0.2, 3.1, 0])
        self.at("first rule")
        self.play(FadeIn(rule, shift=DOWN * 0.15), run_time=0.5)
        self.at("rises smoothly")
        self.play(FadeIn(t_frame), FadeIn(t_slices, lag_ratio=0.06), run_time=1.6)

        # retina: vertical bar, receptor high at the top
        rx = -5.7
        r_slices = VGroup(*[Rectangle(width=0.4, height=slice_h, stroke_width=0, fill_color=ORANGE,
                                      fill_opacity=0.08 + 0.8 * i / (N - 1)).move_to([rx, bot + slice_h * (i + .5), 0])
                            for i in range(N)])
        r_frame = Rectangle(width=0.4, height=top - bot, stroke_color=GREY, stroke_width=2).move_to([rx, 0, 0])
        r_lbl = T("retina: receptor", 24, ORANGE).move_to([rx + 0.9, bot - 0.5, 0])
        ys = [1.8, 0.9, 0.0, -0.9, -1.8]
        dots = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([rx + 0.55, y, 0]) for y in ys])
        self.at("Picture a receptor")
        self.play(FadeIn(r_frame), FadeIn(r_slices, lag_ratio=0.05), FadeIn(r_lbl), run_time=1.4)
        self.play(FadeIn(dots, lag_ratio=0.1), run_time=0.8)

        t_lbl = T("target: cue", 24, PURPLE).move_to([2.5, bot - 0.5, 0])
        self.at("target holds")
        self.play(*[s.animate.set_fill(PURPLE, opacity=0.08 + 0.7 * i / (N - 1)) for i, s in enumerate(t_slices)],
                  FadeIn(t_lbl), run_time=1.4)

        # growth cones stop where the signal reaches a set level
        rec = [1.0, 0.8, 0.6, 0.45, 0.3]
        stops = []
        for r in rec:
            c_needed = 0.3 / r
            stops.append(tx0 + (c_needed - 0.15) / 0.85 * (tx1 - tx0) - 0.0)
        stops = [min(s, 5.8) for s in stops]
        cones, axons = [], []
        for y, sx in zip(ys, stops):
            start = np.array([rx + 0.72, y, 0])
            end = np.array([sx, y, 0])
            ax = Line(start, end, color=YELLOW, stroke_width=4)
            cone = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.26).rotate(-PI / 2).move_to(start)
            axons.append(ax)
            cones.append(cone)
        for cone in cones:
            cone.set_opacity(0)
            self.add(cone)
        self.at("Each growth cone")
        anims = []
        for ax, cone, sx in zip(axons, cones, stops):
            rt = max(0.8, 5.0 * (sx - (rx + 0.72)) / (5.8 - (rx + 0.72)))
            anims.append(AnimationGroup(Create(ax, rate_func=linear, run_time=rt),
                                        cone.animate(rate_func=linear, run_time=rt).set_opacity(1).move_to(ax.get_end())))
        self.play(*anims)
        self.at("set level")
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.8) for c in cones], run_time=0.8)

        order = DashedLine(cones[0].get_center(), cones[-1].get_center(), color=TEXT, stroke_width=2)
        g1 = bchip("1 receptor gene", ORANGE, 24).move_to([-4.2, 3.1, 0])
        g2 = bchip("1 cue gene", PURPLE, 24).move_to([4.4, 3.1, 0])
        self.at("One receptor gene")
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.6)
        self.at("in order")
        self.play(Create(order), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Select(SpokenScene):
    """two neighbours branch widely, fire together, keep matched branches, lose the rest."""

    def construct(self):
        ca, cb = np.array([-5.0, 0.9, 0]), np.array([-5.0, -0.9, 0])
        bpa, bpb = np.array([-0.8, 0.9, 0]), np.array([-0.8, -0.9, 0])
        tys = [2.8, 2.0, 1.2, 0.4, -0.4, -1.2, -2.0, -2.8]
        tx = 4.6
        rule = bchip("Rule 2: overproduce, then select", TEAL, 28).move_to([-0.6, 3.1, 0])
        self.at("second rule")
        self.play(FadeIn(rule, shift=DOWN * 0.15), run_time=0.5)

        a = cell(0.35).move_to(ca)
        b = cell(0.35).move_to(cb)
        ta = Line(ca + RIGHT * 0.35, bpa, color=YELLOW, stroke_width=4)
        tb = Line(cb + RIGHT * 0.35, bpb, color=YELLOW, stroke_width=4)
        spots = VGroup(*[Circle(radius=0.22, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35).move_to([tx, y, 0]) for y in tys])
        t_lbl = T("target", 24, GREY).move_to([tx, -3.3, 0])
        self.at("overproduce")
        self.play(FadeIn(a), FadeIn(b), Create(ta), Create(tb), FadeIn(spots, lag_ratio=0.05), FadeIn(t_lbl), run_time=1.6)

        ia = list(range(0, 6))
        ib = list(range(2, 8))
        la = {i: Line(bpa, [tx - 0.25, tys[i], 0], color=YELLOW, stroke_width=3) for i in ia}
        lb = {i: Line(bpb, [tx - 0.25, tys[i], 0], color=YELLOW, stroke_width=3) for i in ib}
        self.at("Let each axon")
        self.play(*[Create(l) for l in list(la.values()) + list(lb.values())], run_time=2.0)

        brace_lbl = T("neighbours", 24, GREY).move_to([-5.0, 0.0, 0])
        self.at("retinal cells")
        self.play(FadeIn(brace_lbl), run_time=0.5)
        self.at("fire")
        for _ in range(2):
            self.play(a.animate.set_stroke(GREEN).set_fill(GREEN, 0.7), b.animate.set_stroke(GREEN).set_fill(GREEN, 0.7),
                      ta.animate.set_color(GREEN), tb.animate.set_color(GREEN), run_time=0.25)
            self.play(a.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.3), b.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.3),
                      ta.animate.set_color(YELLOW), tb.animate.set_color(YELLOW), run_time=0.25)

        keep_a = [i for i in ia if i in ib]
        gone_a = [i for i in ia if i not in ib]
        gone_b = [i for i in ib if i not in ia]
        self.at("So keep the branches")
        self.play(*[la[i].animate.set_color(GREEN).set_stroke(width=4) for i in keep_a],
                  *[lb[i].animate.set_color(GREEN).set_stroke(width=4) for i in keep_a],
                  *[la[i].animate.set_color(RED) for i in gone_a],
                  *[lb[i].animate.set_color(RED) for i in gone_b], run_time=0.9)
        self.at("remove the rest")
        self.play(*[FadeOut(la[i]) for i in gone_a], *[FadeOut(lb[i]) for i in gone_b], run_time=1.0)

        meas = T("measured by the tissue, after the connections form", 24, GREEN).move_to([-1.0, -3.0, 0])
        self.at("The tissue measures")
        self.play(FadeIn(meas), run_time=0.6)
        gen = bchip("genome", BLUE, 30).move_to([-3.4, -2.0, 0])
        cross = T("✕", 44, RED, weight=BOLD).next_to(gen, RIGHT, buff=0.3)
        self.at("genome never")
        self.play(FadeIn(gen), run_time=0.4)
        self.play(FadeIn(cross, scale=1.5), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """activity blocked: coarse order stays, fine precision is lost."""

    def construct(self):
        ys = [1.6, 0.0, -1.6]
        sy = [2.3 - 0.46 * i for i in range(11)]
        tight = [(1, 2), (4, 5, 6), (8, 9)]
        wide = [(0, 1, 2, 3, 4), (3, 4, 5, 6, 7), (6, 7, 8, 9, 10)]

        def panel(left, title, tcolor):
            ttl = bchip(title, tcolor, 26).move_to([left + 2.9, 3.1, 0])
            cells = VGroup(*[cell(0.28).move_to([left + 0.3, y, 0]) for y in ys])
            xt, xs = left + 3.1, left + 5.2
            trunks = [Line([left + 0.58, y, 0], [xt, y, 0], color=YELLOW, stroke_width=5) for y in ys]
            spots = VGroup(*[Circle(radius=0.14, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35)
                             .move_to([xs, y, 0]) for y in sy])
            return ttl, cells, trunks, spots, xt, xs

        L = panel(-6.1, "with activity", GREEN)
        R = panel(0.4, "activity blocked", RED)

        self.play(FadeIn(L[1]), FadeIn(R[1]), FadeIn(L[3]), FadeIn(R[3]), run_time=0.7)
        self.at("block activity")
        self.play(FadeIn(R[0]), FadeIn(L[0]), run_time=0.8)

        self.at("coarse order")
        self.play(*[Create(t) for t in L[2] + R[2]], run_time=1.2)

        def fans(p, groups, w):
            out = []
            xt, xs = p[4], p[5]
            for y, g in zip(ys, groups):
                for i in g:
                    out.append(Line([xt, y, 0], [xs - 0.15, sy[i], 0], color=YELLOW, stroke_width=w))
            return out

        fl = fans(L, tight, 4)
        fr = fans(R, wide, 4)
        self.at("fine precision")
        self.play(*[Create(f) for f in fl + fr], run_time=1.4)

        c1 = bchip("gradients: rough place", PURPLE, 26).move_to([-3.4, -3.15, 0])
        c2 = bchip("activity: sharpens", GREEN, 26).move_to([3.4, -3.15, 0])
        self.at("So gradients place")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at("activity sharpens")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.6)

        done = bchip("the genome stores rules", TEAL, 30).move_to([-3.4, -3.15, 0])
        done2 = bchip("the tissue measures the rest", GREEN, 30).move_to([3.0, -3.15, 0])
        self.at("The genome stores")
        self.play(ReplacementTransform(c1, done), run_time=0.7)
        self.at("tissue measures")
        self.play(ReplacementTransform(c2, done2), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "The genome stores rules, and the tissue measures the rest."
