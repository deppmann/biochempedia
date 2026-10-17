"""Recombinant DNA and PCR: copies of copies, doubling each cycle  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  GREY   = original template strands, outlines, axes
  YELLOW = primers
  BLUE   = new DNA made by polymerase (copies), and the copy-number curves
  GREEN  = molecules bounded by both primers (exact length), and the steps that are "go"
  RED    = the stop: what a real reaction runs into (plateau line), crossed-out cell
  TEAL / PURPLE = the other two starting amounts in the last scene
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
BAR = 0.16


def bar(x0, x1, y, color, h=BAR, op=0.95):
    r = Rectangle(width=max(x1 - x0, 0.02), height=h, stroke_width=0, fill_color=color, fill_opacity=op)
    return r.move_to([(x0 + x1) / 2, y, 0])


def tip(x, y, d, color, s=0.2):
    """small triangle marking a 3' end; d = +1 points right, -1 points left."""
    t = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(s)
    t.rotate(-PI / 2 if d > 0 else PI / 2)
    return t.move_to([x + d * s * 0.5, y, 0])


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def small_duplex(x, y, w=0.5, color=GREY):
    return VGroup(bar(x - w / 2, x + w / 2, y + 0.06, color, 0.07), bar(x - w / 2, x + w / 2, y - 0.06, color, 0.07))


class S00Title(TitleCard):
    LESSON = "Recombinant DNA, cloning and PCR"
    TITLE = "Copies of copies, doubling each cycle"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        # tube with ten duplexes
        tube = VMobject(color=GREY, stroke_width=5)
        tube.set_points_as_corners([[-6.0, 1.9, 0], [-6.0, -1.9, 0], [-3.4, -1.9, 0], [-3.4, 1.9, 0]])
        rim = Line([-6.2, 1.9, 0], [-3.2, 1.9, 0], color=GREY, stroke_width=5)
        ten = VGroup()
        for i in range(10):
            r, c = divmod(i, 2)
            ten.add(small_duplex(-5.35 + c * 1.1, 1.0 - r * 0.62, 0.7, GREY))
        ten_lbl = T("10 molecules", 28, TEXT).next_to(tube, DOWN, buff=0.3)
        self.at("molecules of DNA")
        self.play(Create(tube), Create(rim), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, ten, lag_ratio=0.12), FadeIn(ten_lbl), run_time=1.2)

        # arrow of thirty rounds
        self.at("rounds of copying")
        ar = Arrow([-2.7, 0, 0], [0.9, 0, 0], buff=0, color=BLUE, stroke_width=8)
        ar_lbl = T("30 rounds of copying", 28, BLUE).next_to(ar, UP, buff=0.25)
        self.play(GrowArrow(ar), FadeIn(ar_lbl), run_time=0.8)

        # dense field
        rng = np.random.default_rng(3)
        field = VGroup()
        for _ in range(170):
            x = rng.uniform(1.6, 6.2)
            y = rng.uniform(-1.7, 1.7)
            field.add(small_duplex(x, y, 0.32, BLUE))
        tube2 = VMobject(color=GREY, stroke_width=5)
        tube2.set_points_as_corners([[1.4, 1.9, 0], [1.4, -1.9, 0], [6.4, -1.9, 0], [6.4, 1.9, 0]])
        rim2 = Line([1.2, 1.9, 0], [6.6, 1.9, 0], color=GREY, stroke_width=5)
        big_lbl = T("about 10 billion", 28, BLUE).next_to(tube2, DOWN, buff=0.3)
        self.at("turn them into")
        self.play(Create(tube2), Create(rim2), run_time=0.4)
        self.play(FadeIn(field, lag_ratio=0.02), FadeIn(big_lbl), run_time=1.4)

        # no living cell
        self.at("No living cell is involved")
        cell = Circle(radius=0.75, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([-0.9, 2.55, 0])
        nuc = Circle(radius=0.25, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(cell)
        cross = VGroup(Line([-1.7, 3.25, 0], [-0.1, 1.85, 0], color=RED, stroke_width=7),
                       Line([-1.7, 1.85, 0], [-0.1, 3.25, 0], color=RED, stroke_width=7))
        cell_lbl = T("living cell", 26, GREY).next_to(cell, RIGHT, buff=0.35)
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(cell_lbl), run_time=0.4)
        self.play(Create(cross), run_time=0.5)

        # the questions
        self.at("How does a tube of DNA do that")
        q1 = T("?", 96, GOLD, weight=BOLD).move_to([-0.9, -1.1, 0])
        self.play(FadeIn(q1, scale=0.6), run_time=0.5)
        self.at("stop short")
        stop = DashedLine([6.55, -2.2, 0], [6.55, 2.2, 0], color=RED, stroke_width=5)
        self.play(Create(stop), FadeOut(q1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
TA, TB = -2.5, 2.5          # primer sites on the template (x coordinates)
TL, TR = -5.8, 5.8          # template ends
YT, YB = 1.05, -1.05       # top and bottom strand heights
PL = 2.0                    # primer length


def template_group():
    top = bar(TL, TR, YT, GREY, 0.4)
    bot = bar(TL, TR, YB, GREY, 0.4)
    labs = VGroup(T("5'", 26, GREY).move_to([TL - 0.4, YT, 0]), T("3'", 26, GREY).move_to([TR + 0.4, YT, 0]),
                  T("3'", 26, GREY).move_to([TL - 0.4, YB, 0]), T("5'", 26, GREY).move_to([TR + 0.4, YB, 0]))
    return VGroup(top, bot), labs


class S02Primers(SpokenScene):
    def construct(self):
        tmpl, labs = template_group()
        head = T("the template", 28, GREY).move_to([0, 2.5, 0])
        self.play(FadeIn(tmpl), FadeIn(labs), FadeIn(head), run_time=0.8)
        # primer 1 on the bottom strand, pointing right; primer 2 on the top strand, pointing left
        PY = 0.38
        p1 = VGroup(bar(TA, TA + PL, YB + PY, YELLOW, 0.34), tip(TA + PL, YB + PY, +1, YELLOW, 0.4))
        p2 = VGroup(bar(TB - PL, TB, YT - PY, YELLOW, 0.34), tip(TB - PL, YT - PY, -1, YELLOW, 0.4))
        l1 = T("primer", 28, YELLOW).move_to([TA + 0.7, YB - 0.65, 0])
        l2 = T("primer", 28, YELLOW).move_to([TB - 0.7, YT + 0.65, 0])
        self.at("two short primers")
        self.play(FadeOut(head), run_time=0.2)
        self.play(FadeIn(p1, shift=UP * 0.3), FadeIn(p2, shift=DOWN * 0.3), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.at("opposite strands")
        brace_top = Line([TA, YT + 0.85, 0], [TA, YT + 0.85, 0])
        hl1 = SurroundingRectangle(bar(TL, TR, YB, GREY, 0.4), color=YELLOW, buff=0.06, stroke_width=3)
        hl2 = SurroundingRectangle(bar(TL, TR, YT, GREY, 0.4), color=YELLOW, buff=0.06, stroke_width=3)
        self.play(Create(hl1), run_time=0.5)
        self.play(Create(hl2), run_time=0.5)
        self.play(FadeOut(hl1), FadeOut(hl2), run_time=0.3)
        # the region between
        self.at("region to copy")
        reg = DoubleArrow([TA, 0, 0], [TB, 0, 0], buff=0, color=GREEN, stroke_width=5, tip_length=0.2)
        reg_t = btext("region to copy", 30, GREEN).move_to([0, 0, 0])
        self.play(GrowFromCenter(reg), FadeIn(reg_t), run_time=0.7)
        # only extends from 3' end
        self.at("Polymerase can only add")
        e1 = Arrow([TA + PL + 0.45, YB + PY, 0], [TA + PL + 1.9, YB + PY, 0], buff=0, color=BLUE, stroke_width=8)
        e2 = Arrow([TB - PL - 0.45, YT - PY, 0], [TB - PL - 1.9, YT - PY, 0], buff=0, color=BLUE, stroke_width=8)
        t1 = T("3'", 30, YELLOW, weight=BOLD).move_to([TA + PL + 0.2, YB - 0.65, 0])
        t2 = T("3'", 30, YELLOW, weight=BOLD).move_to([TB - PL - 0.2, YT + 0.65, 0])
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.4)
        self.at("point toward each other")
        self.play(GrowArrow(e1), GrowArrow(e2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cycle(SpokenScene):
    def construct(self):
        steps = []
        specs = [("1  Denature", "94 to 98 °C"), ("2  Anneal", "a few degrees below\nthe primers' melting temperature"), ("3  Extend", "72 °C for Taq")]
        for name, sub in specs:
            c = chip(name, GREY, 28)
            s = T(sub, 22, GREY, line_spacing=0.8)
            g = VGroup(c, s).arrange(DOWN, buff=0.15)
            steps.append(g)
        row = VGroup(*steps).arrange(RIGHT, buff=0.6).move_to([0, 3.05, 0])
        row.scale_to_fit_width(min(row.width, 12.2)) if row.width > 12.2 else None
        self.play(FadeIn(row), run_time=0.6)

        def lit(i, color):
            return [steps[i][0][0].animate.set_stroke(color).set_fill(color, 0.2),
                    steps[i][0][1].animate.set_color(color), steps[i][1].animate.set_color(color)]

        # template in the middle, reduced to the region and a little flanking
        x0, x1 = -5.2, 5.2
        top = bar(x0, x1, 0.6, GREY, 0.3)
        bot = bar(x0, x1, -0.6, GREY, 0.3)
        tl = T("5'", 24, GREY).move_to([x0 - 0.35, 0.6, 0]); tr = T("3'", 24, GREY).move_to([x1 + 0.35, 0.6, 0])
        bl = T("3'", 24, GREY).move_to([x0 - 0.35, -0.6, 0]); br = T("5'", 24, GREY).move_to([x1 + 0.35, -0.6, 0])
        ends = VGroup(tl, tr, bl, br)
        self.play(FadeIn(top), FadeIn(bot), FadeIn(ends), run_time=0.6)

        # 1 denature
        self.at("heat the tube")
        self.play(*lit(0, RED), run_time=0.3)
        self.play(top.animate.shift(UP * 1.05), bot.animate.shift(DOWN * 1.05),
                  tl.animate.shift(UP * 1.05), tr.animate.shift(UP * 1.05),
                  bl.animate.shift(DOWN * 1.05), br.animate.shift(DOWN * 1.05), run_time=1.2)
        self.at("strands separate")
        # (strands are already apart; the wait lets the sentence land)
        # 2 anneal
        self.at("cool the tube")
        self.play(*lit(0, GREY), *lit(1, YELLOW), run_time=0.3)
        pa = bar(-3.6, -1.2, -1.65 + 0.3, YELLOW, 0.26)   # sits just above the bottom strand
        pb = bar(1.2, 3.6, 1.65 - 0.3, YELLOW, 0.26)      # sits just below the top strand
        pa_t = tip(-1.2, -1.65 + 0.3, +1, YELLOW, 0.3)
        pb_t = tip(1.2, 1.65 - 0.3, -1, YELLOW, 0.3)
        pa_g = VGroup(pa, pa_t); pb_g = VGroup(pb, pb_t)
        self.play(FadeIn(pa_g, shift=UP * 0.8), FadeIn(pb_g, shift=DOWN * 0.8), run_time=0.9)
        self.at("each primer pairs")
        self.play(Indicate(pa_g, color=YELLOW, scale_factor=1.08), Indicate(pb_g, color=YELLOW, scale_factor=1.08), run_time=0.8)
        # 3 extend
        self.at("Third")
        self.play(*lit(1, GREY), *lit(2, GREEN), run_time=0.3)
        self.at("each primer is lengthened")
        ea = bar(-1.2, 4.9, -1.65 + 0.3, BLUE, 0.26)
        eb = bar(-4.9, 1.2, 1.65 - 0.3, BLUE, 0.26)
        self.play(GrowFromEdge(ea, LEFT), GrowFromEdge(eb, RIGHT), run_time=2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Copies(SpokenScene):
    """Rows of duplexes: every strand is a template. Strand identities are tracked so every copy is real."""
    U0, UW = -6.3, 0.9          # template coordinate u in [0, 10] -> x
    A, B = 3.0, 7.0
    RX = 4.9                    # centre of the right-hand text column

    def X(self, u):
        return self.U0 + u * self.UW

    def ys(self, n):
        sp = {1: 0.0, 2: 1.5, 4: 1.0, 8: 0.62}[n]
        return [(n - 1) / 2 * sp - i * sp for i in range(n)]

    def mk(self, u0, u1, y, color):
        return bar(self.X(u0), self.X(u1), y, color, 0.15)

    def construct(self):
        A, B, RX = self.A, self.B, self.RX
        ya = self.ys(1)[0]
        top = {"u0": 0, "u1": 10, "m": self.mk(0, 10, ya + 0.1, GREY)}
        bot = {"u0": 0, "u1": 10, "m": self.mk(0, 10, ya - 0.1, GREY)}
        rows = [(top, bot)]

        da = DashedLine([self.X(A), 2.6, 0], [self.X(A), -2.55, 0], color=YELLOW, stroke_width=2, dash_length=0.12).set_opacity(0.7)
        db = DashedLine([self.X(B), 2.6, 0], [self.X(B), -2.55, 0], color=YELLOW, stroke_width=2, dash_length=0.12).set_opacity(0.7)
        la = T("primer site", 22, YELLOW).move_to([self.X(A), 2.95, 0])
        lb = T("primer site", 22, YELLOW).move_to([self.X(B), 2.95, 0])
        leg = VGroup(VGroup(bar(0, 0.5, 0, GREY, 0.15), T("original", 24, GREY)).arrange(RIGHT, buff=0.15),
                     VGroup(bar(0, 0.5, 0, BLUE, 0.15), T("new copy", 24, BLUE)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6).move_to([self.X(5), -3.3, 0])
        count = T("1 duplex", 32, TEXT).move_to([RX, 1.2, 0])
        self.play(FadeIn(top["m"]), FadeIn(bot["m"]), FadeIn(da), FadeIn(db), FadeIn(la), FadeIn(lb), FadeIn(leg), FadeIn(count), run_time=0.4)

        def do_cycle():
            nonlocal rows
            n = len(rows)
            new_rows, anims, grows, newm = [], [], [], []
            yn = self.ys(2 * n)
            for i, (t, b) in enumerate(rows):
                nb = {"u0": t["u0"], "u1": B, "m": self.mk(t["u0"], B, yn[2 * i] - 0.1, BLUE)}
                nt = {"u0": A, "u1": b["u1"], "m": self.mk(A, b["u1"], yn[2 * i + 1] + 0.1, BLUE)}
                anims += [t["m"].animate.set_y(yn[2 * i] + 0.1), b["m"].animate.set_y(yn[2 * i + 1] - 0.1)]
                grows += [GrowFromEdge(nb["m"], RIGHT), GrowFromEdge(nt["m"], LEFT)]
                newm += [nb, nt]
                new_rows += [(t, nb), (nt, b)]
            rows = new_rows
            return anims, grows, newm

        def step(k, label_old):
            nonlocal count
            an, gr, newm = do_cycle()
            c = T(f"cycle {k}", 32, BLUE).move_to([RX, 2.2, 0])
            nc = T(f"{2 ** k} duplexes", 32, TEXT).move_to([RX, 1.2, 0])
            first = [FadeIn(c)] if label_old is None else [FadeOut(label_old), FadeIn(c)]
            self.play(*first, *an, run_time=0.6)
            self.play(*gr, FadeOut(count), FadeIn(nc), run_time=1.1)
            count = nc
            if k == 2:
                ex0 = T("exact-length\nduplexes: 0", 26, GREY).move_to([RX, 0.2, 0])
                self.add(ex0); self.exz = ex0
            if k == 3:
                self.remove(self.exz)
            return c

        self.at("copies start at a primer")
        c = step(1, None)
        self.at("run past the other site")
        longs = VGroup(rows[0][1]["m"], rows[1][0]["m"])
        self.play(Indicate(longs, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("each new strand contains")
        self.play(Indicate(da, color=YELLOW), Indicate(db, color=YELLOW), run_time=0.8)
        self.at("products of one cycle become templates")
        c = step(2, c)
        self.at("photocopier")
        self.wait(0.1)
        self.at("first appear in cycle")
        c = step(3, c)

        exact = [i for i, (t, b) in enumerate(rows) if t["u0"] == A and t["u1"] == B and b["u0"] == A and b["u1"] == B]
        assert len(exact) == 2, exact
        self.at("two of the eight")
        ex_anims = []
        for i in exact:
            ex_anims += [rows[i][0]["m"].animate.set_color(GREEN), rows[i][1]["m"].animate.set_color(GREEN)]
        ex_lbl = T("exact-length\nduplexes: 2", 26, GREEN).move_to([RX, 0.2, 0])
        self.play(*ex_anims, FadeIn(ex_lbl), run_time=0.8)
        self.at("nearly all of the product")
        end_t = T("by cycle 30:\nnearly all", 30, GREEN).move_to([RX, -1.3, 0])
        self.play(FadeIn(end_t), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Doubling(SpokenScene):
    def construct(self):
        eq = M("N = N0 x 2^n", 40, TEXT).move_to([0, 2.7, 0])
        self.at("Doubling")
        pd = T("perfect doubling", 26, GREY).move_to([0, 2.1, 0])
        self.play(FadeIn(eq, shift=UP * 0.2), FadeIn(pd), run_time=0.6)
        n_tr = ValueTracker(0)
        cyc_t = T("cycle", 34, GREY).move_to([-5.0, 0.95, 0])
        cnt_t = T("copies", 34, GREY).move_to([-5.0, -0.55, 0])
        cyc_n = always_redraw(lambda: M(f"{int(round(n_tr.get_value()))}", 64, BLUE).move_to([0, 0.95, 0]).align_to([-3.4, 0, 0], LEFT))
        cnt_n = always_redraw(lambda: M(f"{10 * 2 ** int(round(n_tr.get_value())):,}", 64, BLUE).move_to([0, -0.55, 0]).align_to([-3.4, 0, 0], LEFT))
        line = Line([-5.5, -2.1, 0], [5.5, -2.1, 0], color=GREY, stroke_width=4)
        dot = always_redraw(lambda: Dot([-5.5 + 11 * n_tr.get_value() / 30, -2.1, 0], radius=0.14, color=BLUE))
        l0 = T("0", 24, GREY).move_to([-5.5, -2.5, 0]); l30 = T("30", 24, GREY).move_to([5.5, -2.5, 0])
        self.play(FadeIn(cyc_t), FadeIn(cyc_n), FadeIn(cnt_t), FadeIn(cnt_n), Create(line), FadeIn(dot), FadeIn(l0), FadeIn(l30), run_time=0.7)
        self.at("multiplies the number of copies")
        self.play(n_tr.animate.set_value(3), run_time=2.0, rate_func=linear)
        self.at("Thirty cycles multiply")
        mult = M("x 2 x 2 x 2 ...", 30, GREY).move_to([0, 1.6, 0])
        self.play(FadeIn(mult), run_time=0.3)
        self.play(n_tr.animate.set_value(30), run_time=3.4, rate_func=rush_into)
        self.at("just over one billion")
        pw = M("2^30 = 1,073,741,824", 34, GREEN).move_to([0, 1.6, 0])
        self.play(FadeOut(mult), run_time=0.2)
        self.play(FadeIn(pw), run_time=0.4)
        self.at("Ten molecules become")
        res = M("10 x 1,073,741,824 = 10,737,418,240", 30, GREEN).move_to([0, -3.15, 0])
        self.play(FadeOut(l0), FadeOut(l30), FadeIn(res), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Plateau(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[0, 30, 10], y_range=[0, 1.1, 0.5], x_length=9.4, y_length=5.0,
                  axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 3}
                  ).move_to([-1.6, -0.3, 0])
        xl = T("cycle", 26, GREY).next_to(ax.x_axis, DOWN, buff=0.2).align_to(ax.x_axis, RIGHT)
        yl = T("DNA", 26, GREY).next_to(ax.y_axis, UP, buff=0.15)
        sch = T("schematic", 22, GREY).move_to([5.2, -3.4, 0])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sch), run_time=0.8)

        def curve(n0):
            def f(c):
                x = n0 * 2.0 ** c
                return x / (1 + x)
            return f
        starts = [(2.0 ** -12, BLUE), (2.0 ** -15, TEAL), (2.0 ** -18, PURPLE)]
        graphs = [ax.plot(curve(n0), x_range=[0, 30], color=col, stroke_width=6, use_smoothing=False) for n0, col in starts]

        self.play(Create(graphs[0]), run_time=3.4, rate_func=linear)
        self.at("exponential only in the early cycles")
        early = T("doubles each cycle", 26, BLUE).move_to(ax.c2p(5.6, 0.55))
        self.play(FadeIn(early), run_time=0.4)
        self.at("reaches a plateau")
        pl = DashedLine(ax.c2p(0, 1.0), ax.c2p(30, 1.0), color=RED, stroke_width=4)
        pl_t = T("plateau", 28, RED).move_to(ax.c2p(4, 1.0) + UP * 0.35)
        self.play(Create(pl), FadeIn(pl_t), FadeOut(early), run_time=0.8)
        self.at("different starting amounts")
        self.play(Create(graphs[1]), Create(graphs[2]), run_time=2.0, rate_func=linear)
        leg = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.5, color=col, stroke_width=6), T(txt, 24, col)).arrange(RIGHT, buff=0.15)
                       for col, txt in [(BLUE, "most template"), (TEAL, "less"), (PURPLE, "least")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        leg.move_to([5.2, 1.4, 0])
        self.play(FadeIn(leg), run_time=0.4)
        self.at("same final level")
        self.play(Indicate(pl, color=RED, scale_factor=1.0), Indicate(pl_t, color=RED), run_time=0.9)
        self.at("bright band at the end")
        note = T("same endpoint,\ndifferent start", 30, GOLD).move_to([5.2, -0.6, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Each cycle doubles the copies, but only early on."
