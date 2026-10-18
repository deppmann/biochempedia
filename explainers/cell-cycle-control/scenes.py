"""Cell-cycle states and control logic: a kinase whose partner rises and falls  (Biochemistrypedia explainer, Cell Biology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = CDK (CDK1 / Cdc2), the kinase
  ORANGE = cyclin, and the cyclin level
  YELLOW = the transferable activity (the unknown "copy now" signal, MPF)
  TEAL   = DNA copying
  GREEN  = on / active / matured / mitosis
  RED    = refuses / off / destroyed
  PURPLE = Wee1 and Cdc25
  PINK   = the hormone progesterone
  GOLD   = a phosphate badge
  GREY   = cells, nuclei, axes, interphase and resting states
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar_t(a, b, color=RED, w=5):
    """inhibition: line ending in a T bar."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.25, b - perp * 0.25, color=color, stroke_width=w + 1))


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cross_mark(center, s=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def cell_shape(cx, cy, w, h, color=GREY, op=0.07):
    return RoundedRectangle(corner_radius=0.9, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=op).move_to([cx, cy, 0])


def nucleus(cx, cy, r=0.62, color=GREY, fill=0.1):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill).move_to([cx, cy, 0])


def pbadge(size=0.22):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def sawtooth(xs, ys, x0, x1, y0, y1, teeth_end, color=ORANGE, w=6, power=1.6, n=60, last_frac=1.0):
    """Polyline: level rises through each cycle and drops at each division. teeth_end = division times."""
    pts = []
    t_prev = 0.0
    for k, te in enumerate(teeth_end):
        frac_end = last_frac if k == len(teeth_end) - 1 else 1.0
        for i in range(n + 1):
            u = (i / n) * frac_end
            t = t_prev + u * (te - t_prev)
            lvl = 0.06 + 0.88 * (u ** power)
            pts.append([xs(t), ys(lvl), 0])
        if frac_end >= 1.0 and k < len(teeth_end) - 1:
            pts.append([xs(te), ys(0.06), 0])
        t_prev = te
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners(pts)
    return m


class Plot:
    """A bare plot frame: x from X0..X1 (screen), y from Y0..Y1 (screen); time 0..tmax; level 0..1."""

    def __init__(self, X0, X1, Y0, Y1, tmax, xlab="time", ylab="level"):
        self.X0, self.X1, self.Y0, self.Y1, self.tmax = X0, X1, Y0, Y1, tmax
        self.xaxis = Arrow([X0, Y0, 0], [X1, Y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        self.yaxis = Arrow([X0, Y0, 0], [X0, Y1, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        self.xl = T(xlab, 22, GREY).next_to(self.xaxis, DOWN, buff=0.1).align_to(self.xaxis, RIGHT)
        self.yl = T(ylab, 22, GREY).next_to(self.yaxis, UP, buff=0.12).align_to(self.yaxis, LEFT)
        self.group = VGroup(self.xaxis, self.yaxis, self.xl, self.yl)

    def xs(self, t):
        return self.X0 + (self.X1 - self.X0 - 0.3) * t / self.tmax

    def ys(self, v):
        return self.Y0 + (self.Y1 - self.Y0 - 0.3) * v


def until(scene, phrase, extra=0.0, floor=0.5, nth=0):
    """seconds from now until just before the narrator says `phrase` (for draws that should end on a cue)."""
    return max(floor, scene.t_of(phrase, nth) - 0.2 - scene.elapsed() + extra)


class S00Title(TitleCard):
    LESSON = "Cell-cycle states and control logic"
    TITLE = "A kinase whose partner rises and falls"


# ---------------------------------------------------------------------------------------------
class S01Fusion(SpokenScene):
    """Two fusions share one cytoplasm: the unstarted nucleus copies early, the finished one refuses."""

    def construct(self):
        rng = random.Random(4)
        LX, RX = -4.2, 0.2

        def make_row(y, right_label):
            cl, cr = cell_shape(LX, y, 3.9, 2.7), cell_shape(RX, y, 3.9, 2.7)
            nl, nr = nucleus(LX, y + 0.25), nucleus(RX, y + 0.25)
            ll = T("S phase", 24, GREY).move_to([LX, y - 0.92, 0])
            lr = T(right_label, 24, GREY).move_to([RX, y - 0.92, 0])
            return cl, cr, nl, nr, ll, lr

        def dots(y):
            out = VGroup()
            for _ in range(13):
                while True:
                    x = rng.uniform(-5.9, 1.9)
                    yy = y + rng.uniform(-1.1, 1.1)
                    if ((x - LX) ** 2 + (yy - (y + 0.25)) ** 2 > 0.95 ** 2 and
                            (x - RX) ** 2 + (yy - (y + 0.25)) ** 2 > 0.95 ** 2 and abs(yy - (y - 0.92)) > 0.0 and yy > y - 0.55 + 0.0 - 0.0):
                        break
                out.add(Dot([x, yy, 0], radius=0.07, color=YELLOW))
            return out

        YA, YB = 1.75, -1.75
        # ---- row A: a copying cell and one that has not started ---------------------------------
        cl, cr, nl, nr, ll, lr = make_row(YA, "")
        self.play(FadeIn(cl), FadeIn(cr), FadeIn(nl), FadeIn(nr), run_time=0.6)
        self.at("copying its DNA")
        ll = T("copying", 24, TEAL).move_to([LX, YA - 0.92, 0])
        self.play(nl.animate.set_stroke(TEAL).set_fill(TEAL, 0.45), FadeIn(ll), run_time=0.5)
        self.at("has not started")
        lr = T("not started", 24, GREY).move_to([RX, YA - 0.92, 0])
        self.play(FadeIn(lr), run_time=0.4)
        self.at("The second nucleus")
        merged = cell_shape(-2.0, YA, 8.6, 2.7)
        self.play(ReplacementTransform(VGroup(cl, cr), merged), run_time=0.8)
        self.at("begins copying")
        lr2 = T("copying early", 24, TEAL).move_to([RX, YA - 0.92, 0])
        self.play(nr.animate.set_stroke(TEAL).set_fill(TEAL, 0.45), ReplacementTransform(lr, lr2), run_time=0.6)
        # ---- row B: the same copying cell and a finished one ---------------------------------
        self.at("Fuse it with")
        cl_b, cr_b, nl_b, nr_b, _, _ = make_row(YB, "")
        nl_b.set_stroke(TEAL).set_fill(TEAL, 0.45)
        ll_b = T("copying", 24, TEAL).move_to([LX, YB - 0.92, 0])
        self.play(FadeIn(cl_b), FadeIn(cr_b), FadeIn(nl_b), FadeIn(nr_b), FadeIn(ll_b), run_time=0.6)
        self.at("has finished")
        lr_b = T("finished", 24, GREY).move_to([RX, YB - 0.92, 0])
        self.play(FadeIn(lr_b), run_time=0.4)
        self.at("and that nucleus")
        merged_b = cell_shape(-2.0, YB, 8.6, 2.7)
        self.play(ReplacementTransform(VGroup(cl_b, cr_b), merged_b), run_time=0.8)
        self.at("refuses")
        lr_b2 = T("refuses", 24, RED).move_to([RX, YB - 0.92, 0])
        self.play(nr_b.animate.set_stroke(RED), ReplacementTransform(lr_b, lr_b2),
                  FadeIn(cross_mark([RX, YB + 0.25, 0], 0.32)), run_time=0.5)
        # ---- the cytoplasm ----------------------------------------------------------------------
        self.at("Something in the cytoplasm")
        da, db = dots(YA), dots(YB)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in list(da) + list(db)], lag_ratio=0.04), run_time=1.0)
        self.at("What is it")
        q = T("?", 170, YELLOW, weight=BOLD).move_to([4.9, 0.55, 0])
        ql = T("in the cytoplasm", 24, YELLOW).move_to([4.9, -1.35, 0])
        self.play(FadeIn(q, scale=0.6), FadeIn(ql), run_time=0.6)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Frog(SpokenScene):
    """Cytoplasm from a treated frog oocyte matures an untreated one: an activity, MPF."""

    def construct(self):
        DX, RX, Y = -4.0, 3.4, 0.3
        R = 1.6

        def oocyte(cx):
            body = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([cx, Y, 0])
            nuc = Circle(radius=0.55, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([cx - 0.15, Y + 0.3, 0])
            return body, nuc

        rng = random.Random(9)

        def activity_dots(cx, n=9):
            out = VGroup()
            pts = []
            while len(pts) < n:
                a, r = rng.uniform(0, 6.28), rng.uniform(0.85, 1.3)
                p = (cx + r * np.cos(a), Y + r * np.sin(a))
                if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 0.3 for q in pts):
                    pts.append(p)
            for p in pts:
                out.add(Dot([p[0], p[1], 0], radius=0.09, color=YELLOW))
            return out

        d_body, d_nuc = oocyte(DX)
        r_body, r_nuc = oocyte(RX)
        d_lab = T("oocyte", 26, GREY).move_to([DX, -1.65, 0])
        r_lab = T("oocyte", 26, GREY).move_to([RX, -1.65, 0])
        self.at("Frogs gave")
        self.at("oocyte waits")
        self.play(FadeIn(d_body), FadeIn(d_nuc), FadeIn(r_body), FadeIn(r_nuc), FadeIn(d_lab), FadeIn(r_lab), run_time=0.7)
        r_lab2 = T("untreated, waiting", 26, GREY).move_to([RX, -1.65, 0])
        self.play(ReplacementTransform(r_lab, r_lab2), run_time=0.4)
        self.at("progesterone")
        hormone = bchip("progesterone", PINK, 26).move_to([DX, 3.05, 0])
        ha = arr([DX, 2.7, 0], [DX, 1.98, 0], PINK)
        self.play(FadeIn(hormone, shift=DOWN * 0.15), GrowArrow(ha), run_time=0.6)
        d_dots = activity_dots(DX)
        d_lab2 = T("treated", 26, PINK).move_to([DX, -1.65, 0])
        self.play(ReplacementTransform(d_lab, d_lab2), FadeIn(d_dots, lag_ratio=0.1), d_body.animate.set_stroke(PINK), run_time=0.8)
        # ---- transfer ----------------------------------------------------------------------------
        self.at("Take cytoplasm")
        inj_arrow = arr([DX + R + 0.15, Y, 0], [RX - R - 0.15, Y, 0], YELLOW, 6)
        inj_lab = T("cytoplasm", 24, YELLOW).next_to(inj_arrow, UP, buff=0.1)
        self.play(GrowArrow(inj_arrow), FadeIn(inj_lab), run_time=0.5)
        self.at("inject it")
        movers = [Dot([DX + R + 0.3 + 0.5 * i, Y, 0], radius=0.09, color=YELLOW) for i in range(4)]
        for m in movers:
            m.move_to([DX + R - 0.3, Y + 0.0, 0])
        self.add(*movers)
        r_dots = activity_dots(RX, 7)
        self.play(LaggedStart(*[m.animate.move_to(r_dots[i].get_center()) for i, m in enumerate(movers)], lag_ratio=0.15),
                  run_time=1.2)
        self.remove(*movers)
        self.add(*r_dots[:4])
        self.play(FadeIn(r_dots[4:]), run_time=0.3)
        self.at("recipient matures")
        r_lab3 = T("matures", 26, GREEN).move_to([RX, -1.65, 0])
        self.play(ReplacementTransform(r_lab2, r_lab3), r_body.animate.set_stroke(GREEN).set_fill(GREEN, 0.12), run_time=0.6)
        # ---- donor nucleus removed: reset the recipient, then repeat ---------------------------------
        self.at("Removing the")
        r_lab4 = T("untreated, waiting", 26, GREY).move_to([RX, -1.65, 0])
        x1 = cross_mark(d_nuc.get_center(), 0.3)
        self.play(FadeOut(r_dots), ReplacementTransform(r_lab3, r_lab4),
                  r_body.animate.set_stroke(GREY).set_fill(GREY, 0.08), run_time=0.6)
        self.play(FadeIn(x1), run_time=0.3)
        self.play(FadeOut(d_nuc), FadeOut(x1), run_time=0.4)
        self.at("stop this")
        movers = [Dot([DX + R - 0.3, Y, 0], radius=0.09, color=YELLOW) for i in range(4)]
        self.add(*movers)
        r_dots2 = activity_dots(RX, 7)
        self.play(LaggedStart(*[m.animate.move_to(r_dots2[i].get_center()) for i, m in enumerate(movers)], lag_ratio=0.15),
                  run_time=1.0)
        self.remove(*movers)
        self.add(*r_dots2[:4])
        r_lab5 = T("matures", 26, GREEN).move_to([RX, -1.65, 0])
        self.play(FadeIn(r_dots2[4:]), ReplacementTransform(r_lab4, r_lab5),
                  r_body.animate.set_stroke(GREEN).set_fill(GREEN, 0.12), run_time=0.6)
        # ---- MPF is an activity, not a molecule -------------------------------------------------------
        self.at("named")
        mpf = bchip("MPF", YELLOW, 32).move_to([-0.3, 2.6, 0])
        mpf_sub = T("maturation-promoting factor", 22, YELLOW).next_to(mpf, DOWN, buff=0.1)
        self.play(FadeIn(mpf, scale=0.8), FadeIn(mpf_sub), run_time=0.6)
        self.at("not a molecule")
        c1 = bchip("an activity", YELLOW, 30).move_to([-2.2, -2.85, 0])
        c2 = bchip("a molecule ?", GREY, 30).move_to([2.2, -2.85, 0])
        self.play(FadeIn(c1, shift=UP * 0.15), FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Urchin(SpokenScene):
    """A protein builds up through each cycle and vanishes at each division: correlation, not yet cause."""

    def construct(self):
        P = Plot(-5.6, 6.0, -3.0, 0.9, 3.0, "time", "protein level")
        # embryo row
        def circ(x, y, r):
            return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to([x, y, 0])
        EY = 2.5
        st1 = VGroup(circ(-2.2, EY, 0.6))
        st2 = VGroup(circ(0.6 - 0.48, EY, 0.45), circ(0.6 + 0.48, EY, 0.45))
        st4 = VGroup(*[circ(3.6 + dx, EY + dy, 0.34) for dx in (-0.38, 0.38) for dy in (-0.38, 0.38)])
        a1 = arr([-1.35, EY, 0], [-0.35, EY, 0], GREY, 4)
        a2 = arr([1.45, EY, 0], [2.45, EY, 0], GREY, 4)
        elab = T("sea urchin\nembryo", 24, GREY, line_spacing=0.8).move_to([-5.3, EY, 0])
        self.at("Researchers")
        self.play(FadeIn(st1), run_time=0.5)
        self.at("sea urchin embryos")
        self.play(FadeIn(elab), run_time=0.4)
        self.at("first divisions")
        self.play(FadeIn(a1), FadeIn(st2), run_time=0.5)
        self.play(FadeIn(a2), FadeIn(st4), run_time=0.5)
        # plot
        self.at("One protein built up")
        self.play(FadeIn(P.group), run_time=0.5)
        ends = [1.0, 2.0, 3.0]
        trace = sawtooth(P.xs, P.ys, 0, 0, 0, 0, ends, color=TEXT, w=6, last_frac=0.55)
        dl1 = DashedLine([P.xs(1.0), P.Y0, 0], [P.xs(1.0), P.Y1 - 0.1, 0], color=GREY, stroke_width=3)
        dl2 = DashedLine([P.xs(2.0), P.Y0, 0], [P.xs(2.0), P.Y1 - 0.1, 0], color=GREY, stroke_width=3)
        dv1 = T("division", 22, GREY).next_to(dl1, UP, buff=0.05)
        dv2 = T("division", 22, GREY).next_to(dl2, UP, buff=0.05)
        plab = T("one protein", 24, TEXT).move_to([P.xs(0.5), P.ys(0.25) , 0])
        self.play(Create(trace), run_time=until(self, "vanished at each", 0.3), rate_func=linear)
        self.at("vanished at each")
        self.play(FadeIn(dl1), FadeIn(dl2), FadeIn(dv1), FadeIn(dv2), run_time=0.4)
        self.at("named cyclin")
        trace_o = sawtooth(P.xs, P.ys, 0, 0, 0, 0, ends, color=ORANGE, w=7, last_frac=0.55)
        cyc_lab = T("cyclin", 30, ORANGE, weight=BOLD).move_to([P.xs(2.62), P.ys(0.88), 0])
        self.play(ReplacementTransform(trace, trace_o), FadeIn(cyc_lab), run_time=0.7)
        self.at("only a correlation")
        # fade the embryo row, show the two readings
        corr = T("correlation", 30, YELLOW, weight=BOLD).move_to([0, 2.6, 0])
        self.play(FadeOut(VGroup(st1, st2, st4, a1, a2, elab)), run_time=0.4)
        self.play(FadeIn(corr, shift=DOWN * 0.1), Indicate(trace_o, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("could be a result")
        self.play(FadeOut(corr), run_time=0.3)
        r1a, r1b = bchip("division", GREY, 26), bchip("protein falls", ORANGE, 26)
        row1 = VGroup(r1a, arr([0, 0, 0], [0.9, 0, 0], GREY, 4), r1b).arrange(RIGHT, buff=0.15)
        tag1 = T("a result?", 26, YELLOW)
        g1 = VGroup(row1, tag1).arrange(RIGHT, buff=0.55).move_to([0, 3.0, 0])
        self.play(FadeIn(g1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("not a cause")
        r2a, r2b = bchip("protein falls", ORANGE, 26), bchip("division", GREY, 26)
        row2 = VGroup(r2a, arr([0, 0, 0], [0.9, 0, 0], GREY, 4), r2b).arrange(RIGHT, buff=0.15)
        tag2 = T("a cause?", 26, YELLOW)
        g2 = VGroup(row2, tag2).arrange(RIGHT, buff=0.55)
        g2.move_to([0, 1.95, 0]).align_to(g1, LEFT)
        self.play(FadeIn(g2, shift=RIGHT * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Extract(SpokenScene):
    """Egg extract in a tube: no mRNA stops it in interphase, mRNA back restores cycles, stable cyclin holds mitosis."""

    def construct(self):
        P = Plot(-2.3, 6.1, -2.6, 1.8, 3.0, "time", "cyclin level")
        # tube
        TX, TY = -4.7, -0.3
        tube = RoundedRectangle(corner_radius=0.5, width=1.5, height=3.4, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.15).move_to([TX, TY, 0])
        cap = Rectangle(width=1.5, height=0.5, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([TX, TY + 1.9, 0])
        tube_lab = T("egg extract", 24, GREY).move_to([TX, TY + 2.2, 0])
        self.at("Tests came next")
        self.play(FadeIn(tube), FadeIn(tube_lab), run_time=0.6)
        self.at("cycle in a tube")
        case0 = T("an extract that cycles in a tube", 30, TEXT).move_to([1.7, 3.05, 0])
        tr0 = sawtooth(P.xs, P.ys, 0, 0, 0, 0, [1.0, 2.0, 3.0], color=ORANGE, w=7)
        st0 = bchip("cycling", GREEN, 26).move_to([3.9, 2.35, 0])
        self.play(FadeIn(P.group), FadeIn(case0), run_time=0.5)
        self.play(Create(tr0), FadeIn(st0), run_time=until(self, "Destroy the", 0.2, 1.0), rate_func=linear)

        # ---- case 1: destroy the extract's own mRNA ----------------------------------------------
        self.at("Destroy the")
        case1 = T("destroy the extract's own messenger RNA", 30, RED).move_to([1.7, 3.05, 0])
        mrna = bchip("messenger RNA", TEXT, 24).move_to([TX, -2.9, 0])
        flat = Line([P.xs(0), P.ys(0.06), 0], [P.xs(3.0), P.ys(0.06), 0], color=ORANGE, stroke_width=7)
        self.play(ReplacementTransform(case0, case1), FadeOut(tr0), FadeOut(st0), FadeIn(mrna), run_time=0.5)
        xm = cross_mark([TX + 1.9, -2.9, 0], 0.26, RED, 8)
        self.play(FadeIn(xm), run_time=0.3)
        self.at("cycles stop")
        st1 = bchip("stuck in interphase", GREY, 26).move_to([3.0, 2.35, 0])
        self.play(Create(flat), FadeIn(st1), run_time=until(self, "Add cyclin", 0.0, 0.8), rate_func=linear)

        # ---- case 2: cyclin mRNA added back --------------------------------------------------------
        self.at("Add cyclin")
        case2 = T("add cyclin messenger RNA back", 30, GREEN).move_to([1.7, 3.05, 0])
        cm = bchip("cyclin mRNA", ORANGE, 24).move_to([TX, -2.9, 0])
        up = arr([TX, -2.5, 0], [TX, -1.85, 0], ORANGE, 5)
        self.play(ReplacementTransform(case1, case2), FadeOut(flat), FadeOut(st1), FadeOut(xm), run_time=0.5)
        self.play(FadeOut(mrna), FadeIn(cm), GrowArrow(up), run_time=0.4)
        self.at("cycles return")
        tr2 = sawtooth(P.xs, P.ys, 0, 0, 0, 0, [1.0, 2.0, 3.0], color=ORANGE, w=7)
        st2 = bchip("cycles return", GREEN, 26).move_to([3.4, 2.35, 0])
        self.play(Create(tr2), FadeIn(st2), run_time=until(self, "cannot be destroyed", 0.0, 1.0), rate_func=linear)

        # ---- case 3: a cyclin that cannot be destroyed -----------------------------------------------
        self.at("cannot be destroyed")
        case3 = T("a cyclin that cannot be destroyed", 30, ORANGE).move_to([1.7, 3.05, 0])
        sc = chip("cyclin", ORANGE, size=24).move_to([TX, -2.9, 0])
        tt = np.linspace(0, 3.0, 80)
        pts = [[P.xs(t), P.ys(0.06 + 0.88 * (1 - np.exp(-2.6 * t / 3.0 * 1.6))), 0] for t in tt]
        tr3 = VMobject(stroke_color=ORANGE, stroke_width=7)
        tr3.set_points_as_corners(pts)
        self.play(ReplacementTransform(case2, case3), FadeOut(tr2), FadeOut(st2), FadeOut(cm), FadeOut(up),
                  FadeIn(sc), run_time=0.5)
        self.at("holds the extract")
        st3 = bchip("held in mitosis", GREEN, 26).move_to([3.0, 2.35, 0])
        self.play(Create(tr3), FadeIn(st3), run_time=max(1.0, self.narration_s - self.elapsed() - 0.4), rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
CDK_W, CDK_H = 3.0, 2.5
CYC_W = 1.9


def cdk_blob(label="CDK1"):
    """CDK: a blue body with a pocket (the catalytic site). A red bar blocks the pocket when it is off.
    VGroup(body, pocket, flap, lab) with those attributes."""
    body = RoundedRectangle(corner_radius=0.4, width=CDK_W, height=CDK_H, stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.28)
    pocket = RoundedRectangle(corner_radius=0.14, width=1.0, height=0.7, stroke_color=BLUE, stroke_width=3,
                              fill_color=BG, fill_opacity=1).move_to(body.get_top() + DOWN * 0.7 + LEFT * 0.6)
    flap = Rectangle(width=1.2, height=0.14, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(pocket.get_center())
    lab = T(label, 32, BLUE, weight=BOLD).move_to(body.get_center() + DOWN * 0.45)
    g = VGroup(body, pocket, flap, lab)
    g.body, g.pocket, g.flap, g.lab = body, pocket, flap, lab
    return g


def cyclin_blob(label="cyclin B"):
    r = RoundedRectangle(corner_radius=0.35, width=CYC_W, height=CDK_H, stroke_color=ORANGE, stroke_width=4,
                         fill_color=ORANGE, fill_opacity=0.3)
    return VGroup(r, T(label, 26, ORANGE, weight=BOLD).move_to(r))


def set_off(cdk):
    return [cdk.flap.animate.set_opacity(1), cdk.pocket.animate.set_stroke(BLUE).set_fill(BG, 1)]


def set_on(cdk):
    return [cdk.flap.animate.set_opacity(0), cdk.pocket.animate.set_stroke(GREEN).set_fill(GREEN, 0.3)]


class S05Engine(SpokenScene):
    """MPF is CDK1 bound to cyclin B: CDK inactive alone, cyclin switches it on; cyclin rises and falls, CDK stays even."""

    def construct(self):
        cx, cy = -1.0, 0.2
        mpf = bchip("MPF", YELLOW, 44).move_to([cx, cy, 0])
        self.at("MPF turned")
        self.play(FadeIn(mpf, scale=0.8), run_time=0.4)
        self.at("turned out")
        cdk = cdk_blob("Cdc2").move_to([cx, cy, 0])
        self.play(ReplacementTransform(mpf, cdk), run_time=0.8)
        self.at("now called")
        new_lab = T("CDK1", 32, BLUE, weight=BOLD).move_to(cdk.lab.get_center())
        self.play(ReplacementTransform(cdk.lab, new_lab), run_time=0.5)
        cdk.lab = new_lab
        # cyclin comes in
        dock = np.array([cdk.body.get_right()[0] + CYC_W / 2 + 0.06, cy, 0])
        away = dock + RIGHT * 2.6
        cycg = cyclin_blob().move_to(away)
        self.at("bound to cyclin")
        self.play(FadeIn(cycg), run_time=0.3)
        self.play(cycg.animate.move_to(dock), run_time=0.7)
        self.play(*set_on(cdk), run_time=0.5)
        self.at("catalytic site")
        site = T("catalytic site", 26, GREEN).next_to(cdk.body, UP, buff=0.25).align_to(cdk.body, LEFT)
        self.play(FadeIn(site), Indicate(cdk.pocket, color=GREEN, scale_factor=1.15), run_time=0.6)
        self.at("inactive alone")
        alone = T("inactive alone", 28, RED).next_to(cdk.body, DOWN, buff=0.3)
        self.play(cycg.animate.move_to(away), *set_off(cdk), FadeOut(site), FadeIn(alone), run_time=0.8)
        self.at("switches it on")
        on = T("active", 28, GREEN).next_to(cdk.body, DOWN, buff=0.3)
        self.play(cycg.animate.move_to(dock), run_time=0.6)
        self.play(*set_on(cdk), ReplacementTransform(alone, on), run_time=0.5)
        # ---- the traces ------------------------------------------------------------------------------
        self.at("Cyclin levels rise")
        cartoon = VGroup(cdk, cycg, on)
        P = Plot(0.9, 6.2, -2.6, 1.6, 3.0, "time", "level")
        self.play(cartoon.animate.shift(LEFT * 2.6 + UP * 0.0), run_time=0.7)
        self.play(FadeIn(P.group), run_time=0.4)
        tr = sawtooth(P.xs, P.ys, 0, 0, 0, 0, [1.0, 2.0, 3.0], color=ORANGE, w=7)
        cl = T("cyclin", 28, ORANGE, weight=BOLD).move_to([P.xs(0.5) + 1.0, P.ys(1.0) + 0.4, 0])
        self.play(Create(tr), FadeIn(cl), run_time=until(self, "stay fairly even", 0.0, 1.0), rate_func=linear)
        self.at("stay fairly even")
        flat = Line([P.xs(0), P.ys(0.55), 0], [P.xs(3.0), P.ys(0.55), 0], color=BLUE, stroke_width=7)
        kl = T("CDK", 28, BLUE, weight=BOLD).move_to([P.xs(2.0) + 0.0, P.ys(0.55) + 0.55, 0])
        self.play(Create(flat), FadeIn(kl), run_time=max(1.0, self.narration_s - self.elapsed() - 0.4), rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
def ymap(nm):
    return -2.6 + nm * 0.115


class S06Switch(SpokenScene):
    """Wee1 and Cdc25 tune CDK1; feedback makes entry a switch; the cyclin B thresholds differ for entry and exit."""

    def construct(self):
        # ---- part 1: the two enzymes and the feedback ------------------------------------------------
        GY = -0.55
        cdk = cdk_blob("CDK1").move_to([-0.8, GY, 0])
        cyc = cyclin_blob().move_to([cdk.body.get_right()[0] + CYC_W / 2 + 0.06, GY, 0])
        group = VGroup(cdk, cyc)
        wee = bchip("Wee1", PURPLE, 32).move_to([-4.6, 2.5, 0])
        c25 = bchip("Cdc25", PURPLE, 32).move_to([4.4, 2.5, 0])
        cdk.flap.set_opacity(0)
        cdk.pocket.set_stroke(GREEN).set_fill(GREEN, 0.3)
        self.at("Two enzymes")
        self.play(FadeIn(group), run_time=0.6)
        self.play(FadeIn(wee), FadeIn(c25), run_time=0.5)
        self.at("inhibitory phosphate")
        pb = pbadge(0.26).move_to(wee.get_right() + RIGHT * 0.5)
        target = cdk.pocket.get_top() + UP * 0.4
        self.play(FadeIn(pb), run_time=0.2)
        self.play(pb.animate.move_to(target), run_time=0.7)
        st_off = T("off", 30, RED, weight=BOLD).move_to([-0.8, GY - 1.75, 0])
        self.play(*set_off(cdk), FadeIn(st_off), run_time=0.4)
        self.at("removes it")
        self.play(pb.animate.move_to(c25.get_left() + LEFT * 0.4), run_time=0.7)
        st_on = T("on", 30, GREEN, weight=BOLD).move_to([-0.8, GY - 1.75, 0])
        self.play(FadeOut(pb), *set_on(cdk), ReplacementTransform(st_off, st_on), run_time=0.5)
        self.at("also switches on")
        on_arrow = arr([cdk.body.get_top()[0] + 0.9, cdk.body.get_top()[1] + 0.12, 0],
                       [c25.get_bottom()[0] - 0.1, c25.get_bottom()[1] - 0.08, 0], GREEN, 6)
        plus = T("+", 36, GREEN, weight=BOLD).move_to([2.9, 1.4, 0])
        self.play(GrowArrow(on_arrow), FadeIn(plus), run_time=0.6)
        self.at("switches off")
        off_bar = bar_t([cdk.body.get_top()[0] - 0.9, cdk.body.get_top()[1] + 0.12, 0],
                        [wee.get_bottom()[0] + 0.1, wee.get_bottom()[1] - 0.1, 0], RED, 6)
        self.play(Create(off_bar), run_time=0.6)
        self.at("mitotic entry is")
        sw = T("mitotic entry is a switch", 32, YELLOW, weight=BOLD).move_to([0, -3.15, 0])
        self.play(FadeIn(sw, shift=UP * 0.1), FadeOut(st_on), run_time=0.6)

        # ---- part 2: entry and exit thresholds -------------------------------------------------------
        self.at("entry needed")
        part1 = VGroup(group, wee, c25, on_arrow, plus, off_bar, sw)
        self.play(FadeOut(part1), run_time=0.5)
        AX = -5.0
        yaxis = Arrow([AX, ymap(0), 0], [AX, ymap(0) + 5.35, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        ylab = T("cyclin B (nM)", 24, GREY).next_to(yaxis, UP, buff=0.12).align_to(yaxis, LEFT).shift(LEFT * 0.4)
        ticks = VGroup()
        for v in (16, 24, 32, 40):
            ticks.add(Line([AX - 0.1, ymap(v), 0], [AX + 0.1, ymap(v), 0], color=GREY, stroke_width=3))
            ticks.add(M(str(v), 24, GREY).move_to([AX - 0.5, ymap(v), 0]))
        ticks.add(M("0", 24, GREY).move_to([AX - 0.5, ymap(0), 0]))
        self.play(FadeIn(yaxis), FadeIn(ylab), FadeIn(ticks), run_time=0.5)
        BX1, BX2, BW = -3.0, 0.1, 1.2
        TOP = 44

        def band(x, lo, hi, c_lo, c_hi):
            r = Rectangle(width=BW, height=ymap(hi) - ymap(lo), stroke_width=0)
            r.set_fill(color=[c_hi, c_lo], opacity=0.7)
            return r.move_to([x, (ymap(lo) + ymap(hi)) / 2, 0])

        def solid(x, lo, hi, c):
            return Rectangle(width=BW, height=ymap(hi) - ymap(lo), stroke_width=0, fill_color=c,
                             fill_opacity=0.7).move_to([x, (ymap(lo) + ymap(hi)) / 2, 0])

        guides = VGroup()
        for v, c in ((32, GREEN), (40, GREEN), (16, RED), (24, RED)):
            guides.add(DashedLine([AX, ymap(v), 0], [BX2 + BW / 2 + 0.2, ymap(v), 0], color=c, stroke_width=2).set_opacity(0.55))
        ltitle = T("adding cyclin B", 26, ORANGE).move_to([BX1, ymap(0) - 0.45, 0])
        rtitle = T("lowering cyclin B", 26, ORANGE).move_to([BX2, ymap(0) - 0.45, 0])
        dot = Dot([BX1, ymap(1), 0], radius=0.2, color=TEXT)
        state = T("interphase", 26, GREY, weight=BOLD).set_stroke(BG, 7, background=True)
        state.add_updater(lambda m: m.next_to(dot, RIGHT, buff=0.3))
        self.add(state)
        self.play(FadeIn(guides), FadeIn(ltitle), FadeIn(dot), run_time=0.4)
        seg1 = solid(BX1, 0, 32, GREY)
        seg2 = band(BX1, 32, 40, GREY, GREEN)
        seg3 = solid(BX1, 40, TOP, GREEN)
        self.play(FadeIn(seg1), dot.animate.move_to([BX1, ymap(32), 0]), run_time=0.8, rate_func=linear)
        self.play(FadeIn(seg2), dot.animate.move_to([BX1, ymap(40), 0]), run_time=0.7, rate_func=linear)
        st_m = T("mitosis", 26, GREEN, weight=BOLD).set_stroke(BG, 7, background=True)
        st_m.add_updater(lambda m: m.next_to(dot, RIGHT, buff=0.3))
        state.clear_updaters()
        self.play(FadeIn(seg3), dot.animate.move_to([BX1, ymap(TOP - 1), 0]).set_color(GREEN),
                  ReplacementTransform(state, st_m), run_time=0.7, rate_func=linear)
        self.bring_to_front(guides, dot, st_m)
        # ---- exit ------------------------------------------------------------------------------------
        self.at("already in mitosis")
        dot2 = Dot([BX2, ymap(TOP - 1), 0], radius=0.2, color=GREEN)
        st_m2 = T("mitosis", 26, GREEN, weight=BOLD).set_stroke(BG, 7, background=True)
        st_m2.add_updater(lambda m: m.next_to(dot2, RIGHT, buff=0.3))
        seg4 = solid(BX2, 24, TOP, GREEN)
        seg5 = band(BX2, 16, 24, GREY, GREEN)
        seg6 = solid(BX2, 0, 16, GREY)
        self.add(st_m2)
        self.play(FadeIn(rtitle), FadeIn(seg4), FadeIn(dot2), run_time=0.5)
        self.bring_to_front(guides, dot2, st_m2)
        self.at("down to about")
        self.play(dot2.animate.move_to([BX2, ymap(24), 0]), FadeIn(seg5), run_time=0.9, rate_func=linear)
        self.play(dot2.animate.move_to([BX2, ymap(16), 0]), run_time=0.6, rate_func=linear)
        st_i2 = T("interphase", 26, GREY, weight=BOLD).set_stroke(BG, 7, background=True)
        st_m2.clear_updaters()
        st_i2.add_updater(lambda m: m.next_to(dot2, RIGHT, buff=0.3))
        self.play(FadeIn(seg6), dot2.animate.move_to([BX2, ymap(1), 0]).set_color(GREY),
                  ReplacementTransform(st_m2, st_i2), run_time=0.7, rate_func=linear)
        self.bring_to_front(guides, dot2, st_i2)
        # ---- the rule ----------------------------------------------------------------------------------
        self.at("Making cyclin")
        up = arr([3.4, ymap(2), 0], [3.4, ymap(40), 0], ORANGE, 8)
        up_l = T("making cyclin: entry", 24, ORANGE).move_to([4.6, 2.65, 0])
        self.play(GrowArrow(up), FadeIn(up_l), run_time=0.7)
        self.at("Destroying it")
        dn = arr([4.1, ymap(40), 0], [4.1, ymap(2), 0], RED, 8)
        dn_l = T("destroying it: exit", 24, RED).move_to([4.6, -3.1, 0])
        self.play(GrowArrow(dn), FadeIn(dn_l), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Making cyclin drives entry. Destroying it permits exit."
