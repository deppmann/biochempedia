"""Glycolysis: spend ATP, balance NAD+, control the gates  (Biochemistrypedia explainer)

Five narrated slide clips from the lesson, one arc: what glycolysis nets (S01) -> the NAD+ bookkeeping that
fermentation fixes (S02) -> why control lives at irreversible steps (S03) -> the three regulated enzymes (S04)
-> what happens to control when fructose enters below the gate (S05).

COLOR MAP (one color per concept, whole video)
  BLUE   = carbon flowing through the pathway (glucose ... pyruvate), glycolysis itself
  YELLOW = ATP (coins, the ledger, ATP chips)
  RED    = brake: ATP spent, inhibition, an irreversible (one-way) step, a stalled step
  GREEN  = gain: ATP earned, activation, a reversible (two-way) step
  TEAL   = NAD+ (oxidized carrier)
  PURPLE = NADH (reduced carrier)
  ORANGE = fructose entering below the gate
  GOLD   = a checkpoint / control point (regulated step, the turnstile, "regulate here")
  TEXT   = electrons, plain words        GREY = structure, axes, de-emphasized
No molecular structures are drawn: steps are numbered nodes, enzymes and metabolites are labelled chips,
water and carbon are dots.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F09A55"
NADP = "NAD⁺"      # NAD+ with a superscript plus
config.disable_caching = True


# ----------------------------------------------------------------------------- helpers
def node(i, color=BLUE, r=0.25, fs=22):
    """Numbered step. Opaque ground under the tint so dots flowing 'through' it pass behind it."""
    under = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1)
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.16)
    return VGroup(under, c, M(str(i), fs, color).move_to(c)).set_z_index(2)


def nad(size=28, color=TEAL):
    """NAD+ with a real superscript plus (the unicode glyph renders too small)."""
    a = T("NAD", size, color, weight=BOLD)
    p = T("+", int(size * 0.8), color, weight=BOLD)
    p.next_to(a, RIGHT, buff=0.02).align_to(a, UP).shift(UP * 0.04)
    return VGroup(a, p)


def electron(size=32):
    e = T("e", size, TEXT, weight=BOLD)
    m = T("\u2212", int(size * 0.8), TEXT, weight=BOLD).next_to(e, RIGHT, buff=0.02).align_to(e, UP).shift(UP * 0.02)
    return VGroup(e, m)


def coin(r=0.36):
    c = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95)
    return VGroup(c, T("ATP", 22, BG, weight=BOLD).move_to(c)).set_z_index(6)


def tag(text, color, size=26):
    return T(text, size, color)


def link(a, b, color=GREY, w=3):
    return Arrow(a, b, buff=0, stroke_width=w, color=color, max_tip_length_to_length_ratio=0.45,
                 tip_length=0.14)


def inhibit(start, end, color=RED, bend=0.5, w=4):
    """Arc ending in a flat bar (the 'blocks' symbol)."""
    arc = ArcBetweenPoints(start, end, angle=bend, stroke_color=color, stroke_width=w)
    p, q = arc.point_from_proportion(0.96), arc.get_end()
    d = q - p
    d = d / np.linalg.norm(d)
    n = np.array([-d[1], d[0], 0])
    bar = Line(q + n * 0.2, q - n * 0.2, color=color, stroke_width=w + 2)
    return VGroup(arc, bar)


def activate(start, end, color=GREEN, bend=0.5, w=4):
    arc = ArcBetweenPoints(start, end, angle=bend, stroke_color=color, stroke_width=w)
    arc.add_tip(tip_length=0.2, tip_width=0.2)
    return arc


class Stream:
    """Dots marching along a polyline. rate scales speed, vis (0..1) thins the stream, dim(x) can fade a part."""

    def __init__(self, pts, n, color, speed=1.6, radius=0.075, rate=1.0, vis=1.0, jitter=0.0):
        self.pts = [np.array(p, dtype=float) for p in pts]
        seg = [np.linalg.norm(self.pts[i + 1] - self.pts[i]) for i in range(len(self.pts) - 1)]
        self.cum = np.concatenate([[0], np.cumsum(seg)])
        self.L = self.cum[-1]
        self.n, self.speed, self.s = n, speed, 0.0
        self.rate, self.vis, self.alpha = ValueTracker(rate), ValueTracker(vis), ValueTracker(1.0)
        self.dots = VGroup(*[Dot(radius=radius, color=color) for _ in range(n)])
        self.dim = None
        rng = np.random.RandomState(7)
        self.jit = (rng.rand(n) - 0.5) * 2 * jitter
        self.dots.add_updater(self._upd)
        self._upd(self.dots, 0)

    def point(self, u, off=0.0):
        d = u * self.L
        i = min(np.searchsorted(self.cum, d, side="right") - 1, len(self.pts) - 2)
        t = (d - self.cum[i]) / max(self.cum[i + 1] - self.cum[i], 1e-9)
        p = self.pts[i] * (1 - t) + self.pts[i + 1] * t
        if off:
            tan = self.pts[i + 1] - self.pts[i]
            tan = tan / max(np.linalg.norm(tan), 1e-9)
            p = p + np.array([-tan[1], tan[0], 0.0]) * off
        return p

    def _upd(self, m, dt):
        self.s = (self.s + dt * self.rate.get_value() * self.speed / self.L) % 1.0
        vis, al = self.vis.get_value(), self.alpha.get_value()
        for k, d in enumerate(self.dots):
            u = (k / self.n + self.s) % 1.0
            p = self.point(u, self.jit[k])
            d.move_to(p)
            op = al if (k + 0.5) / self.n <= vis else 0.0
            if self.dim is not None:
                op *= self.dim(p)
            d.set_opacity(op)


def center_label(mob, target):
    return mob.move_to(target)


# ============================================================================================
class S00Title(TitleCard):
    LESSON = "Glycolysis"
    TITLE = "Spend, balance, control"


# ============================================================================================
class S01Yield(SpokenScene):
    """invest 2 ATP -> earn 4 ATP -> net +2 ATP and 2 NADH -> aerobic respiration adds ~30 more."""

    def construct(self):
        Y0 = 1.0
        glu = T("glucose", 28, BLUE)
        pyr = T("pyruvate", 28, BLUE)
        nodes = [node(i + 1, r=0.27, fs=24) for i in range(10)]
        xs = -3.5 + 0.88 * np.arange(10)
        for n, x in zip(nodes, xs):
            n.move_to([x, Y0, 0])
        glu.next_to(nodes[0], LEFT, buff=0.45)
        pyr.next_to(nodes[9], RIGHT, buff=0.45)
        links = [link(glu.get_right() + RIGHT * 0.05, nodes[0].get_left())]
        links += [link(nodes[i].get_right(), nodes[i + 1].get_left()) for i in range(9)]
        links.append(link(nodes[9].get_right(), pyr.get_left() + LEFT * 0.05))
        strip = VGroup(glu, pyr, *nodes, *links)

        self.play(FadeIn(glu), LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.1),
                  LaggedStart(*[Create(l) for l in links], lag_ratio=0.1), FadeIn(pyr), run_time=1.2)

        # --- two phase brackets (grey until named) ---------------------------------------------------
        def bracket(i0, i1, y):
            x0, x1 = nodes[i0].get_left()[0] - 0.05, nodes[i1].get_right()[0] + 0.05
            return VGroup(Line([x0, y - 0.15, 0], [x0, y, 0]), Line([x0, y, 0], [x1, y, 0]),
                          Line([x1, y, 0], [x1, y - 0.15, 0]))
        YB = Y0 + 1.5
        b1, b2 = bracket(0, 4, YB), bracket(5, 9, YB)
        for b in (b1, b2):
            b.set_stroke(GREY, 4)
        l1 = T("phase 1", 30, GREY).next_to(b1, UP, buff=0.12)
        l2 = T("phase 2", 30, GREY).next_to(b2, UP, buff=0.12)
        self.at("two distinct phases")
        self.play(Create(b1), Create(b2), FadeIn(l1), FadeIn(l2), run_time=0.9)

        # --- ATP ledger ----------------------------------------------------------------------------
        ledger = ValueTracker(0)

        def counter():
            v = int(round(ledger.get_value()))
            s = "0" if v == 0 else f"{v:+d}"
            col = RED if v < 0 else (YELLOW if v > 0 else TEXT)
            g = VGroup(T("net ATP", 36, GREY), M(s, 72, col)).arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
            return g.move_to([0, -1.9, 0])
        ctr = always_redraw(counter)
        HOME = np.array([0, -1.9, 0])

        self.at("investment phase")
        i_l = T("investment", 32, RED).move_to(l1)
        self.play(b1.animate.set_stroke(RED, 5), Transform(l1, i_l), run_time=0.6)

        def spend(k, label, name):
            c = coin().move_to(HOME)
            nm = T(name, 26, GREY).next_to(nodes[k], UP, buff=0.18)
            minus = T("−1", 34, RED, weight=BOLD).next_to(nodes[k], DOWN, buff=0.2)
            self.play(c.animate.move_to(nodes[k].get_center()), FadeIn(nm), run_time=0.8)
            self.play(FadeOut(c, scale=0.4), FadeIn(minus, scale=1.3), run_time=0.3)
            return nm, minus

        self.at("two ATP are consumed")
        self.play(FadeIn(ctr), run_time=0.4)
        n1, m1 = spend(0, None, "hexokinase")
        ledger.set_value(-1)
        self.wait(0.15)
        n3, m3 = spend(2, None, "PFK-1")
        ledger.set_value(-2)

        # --- payoff ----------------------------------------------------------------------------------
        self.at("payoff phase")
        p_l = T("payoff", 32, GREEN).move_to(l2)
        self.play(b2.animate.set_stroke(GREEN, 5), Transform(l2, p_l), run_time=0.6)

        def earn(k, name):
            nm = T(name, 26, GREY).next_to(nodes[k], UP, buff=0.18)
            cs = VGroup(coin(), coin()).arrange(RIGHT, buff=0.12).move_to(nodes[k].get_center() + DOWN * 0.1)
            plus = T("+2", 34, GREEN, weight=BOLD).next_to(nodes[k], DOWN, buff=0.2)
            self.play(FadeIn(nm), FadeIn(cs, scale=0.5), FadeIn(plus), run_time=0.45)
            self.play(cs.animate.move_to(HOME), run_time=0.8)
            self.play(FadeOut(cs, scale=0.4), run_time=0.2)
            return nm, plus

        self.at("Two from phosphoglycerate kinase")
        n7, p7 = earn(6, "PGK")
        ledger.set_value(0)
        self.at("and two from pyruvate kinase")
        n10, p10 = earn(9, "pyruvate kinase")
        ledger.set_value(2)

        # --- subtract ---------------------------------------------------------------------------------
        def term(big, small, color):
            return VGroup(M(big, 50, color), T(small, 26, GREY)).arrange(DOWN, buff=0.14)
        t_pay = term("4 ATP", "payoff", GREEN)
        t_inv = term("2 ATP", "investment", RED)
        t_net = term("+2 ATP", "net yield", YELLOW)
        t_nadh = term("2 NADH", "banked", PURPLE)
        op_minus, op_eq, op_plus = M("−", 50), M("=", 50), M("+", 50)
        eq = VGroup(t_pay, op_minus, t_inv, op_eq, t_net, op_plus, t_nadh).arrange(RIGHT, buff=0.38)
        fit(eq, max_w=12.2)
        eq.move_to([0, -1.9, 0])
        for op in (op_minus, op_eq, op_plus):
            op.set_y(t_pay[0].get_y())

        self.at("Subtract the investment")
        self.play(FadeOut(ctr), run_time=0.3)
        self.at("investment from")
        self.play(FadeIn(t_inv, shift=UP * 0.2), FadeIn(op_minus), run_time=0.5)
        self.at("the payoff and")
        self.play(FadeIn(t_pay, shift=UP * 0.2), run_time=0.5)
        self.at("the net yield")
        self.play(FadeIn(op_eq), FadeIn(t_net, shift=UP * 0.2), run_time=0.6)

        # --- NADH -------------------------------------------------------------------------------------
        self.at("plus two NADH")
        nadh_src = T("2 NADH", 30, PURPLE, weight=BOLD).next_to(nodes[5], DOWN, buff=0.8)
        self.play(nodes[5][1].animate.set_stroke(PURPLE, 5).set_fill(PURPLE, 0.35), FadeIn(nadh_src, scale=0.6),
                  run_time=0.5)
        self.play(FadeIn(op_plus), TransformFromCopy(nadh_src, t_nadh), run_time=0.8)

        # --- the bar chart: glycolysis alone vs with aerobic respiration -------------------------------
        self.at("Aerobic respiration")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        U = 11.0 / 32
        X0, YB2 = -5.5, 0.7
        heading = T("ATP made per glucose", 42, font=TITLE_FONT).move_to([0, 2.5, 0])
        segA = Rectangle(width=2 * U, height=1.2, stroke_color=YELLOW, stroke_width=3,
                         fill_color=YELLOW, fill_opacity=0.95).move_to([X0 + U, YB2, 0])
        segB = Rectangle(width=30 * U, height=1.2, stroke_color=YELLOW, stroke_width=3,
                         fill_color=YELLOW, fill_opacity=0.22).move_to([X0 + 2 * U + 15 * U, YB2, 0])
        lab_a = T("glycolysis alone: 2", 32, YELLOW).next_to(segA, UP, buff=0.4, aligned_edge=LEFT)
        tick_a = Line(segA.get_top(), segA.get_top() + UP * 0.3, color=YELLOW, stroke_width=3)
        lab_b = T("aerobic respiration: ~30 more", 36, YELLOW).move_to(segB)
        self.play(FadeIn(heading), GrowFromEdge(segA, LEFT), FadeIn(lab_a), Create(tick_a), run_time=0.8)
        self.at("extracts roughly 30 more")
        self.play(GrowFromEdge(segB, LEFT), run_time=1.6)
        self.play(FadeIn(lab_b), run_time=0.4)
        self.at("oxygen dependent metabolism")
        brace = Brace(segB, DOWN, color=GREY, buff=0.2)
        need = T("requires oxygen", 34, TEXT).next_to(brace, DOWN, buff=0.15)
        self.play(GrowFromCenter(brace), FadeIn(need), run_time=0.8)
        self.at("so much more efficient")
        self.play(Indicate(segB, color=YELLOW, scale_factor=1.04), run_time=1.0)
        self.finish()


# ============================================================================================
class S02Redox(SpokenScene):
    """NAD+ is a fixed pool: glycolysis turns it into NADH; fermentation hands the electrons to pyruvate
    and gives NAD+ back, so the two cycles keep glycolysis running."""

    def construct(self):
        BAR_W, BAR_H = 6.4, 0.75
        heading = T("A bookkeeping problem", 40, font=TITLE_FONT).move_to([0, 3.3, 0])
        # --- the pool -----------------------------------------------------------------------------
        box = RoundedRectangle(corner_radius=0.2, width=8.4, height=2.0, stroke_color=GREY, stroke_width=3,
                               fill_opacity=0).move_to([0, -1.85, 0])
        bar_c = box.get_center() + UP * 0.3
        f = ValueTracker(0.0)

        def bar():
            fv = f.get_value()
            g = VGroup()
            wn, wh = BAR_W * (1 - fv), BAR_W * fv
            if wn > 0.02:
                g.add(Rectangle(width=wn, height=BAR_H, stroke_width=0, fill_color=TEAL, fill_opacity=0.95)
                      .move_to(bar_c + LEFT * (BAR_W / 2 - wn / 2)))
            if wh > 0.02:
                g.add(Rectangle(width=wh, height=BAR_H, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95)
                      .move_to(bar_c + RIGHT * (BAR_W / 2 - wh / 2)))
            g.add(Rectangle(width=BAR_W, height=BAR_H, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(bar_c))
            return g
        bar_m = always_redraw(bar)
        lab_nad = nad(32).move_to(bar_c + LEFT * (BAR_W / 2 - 0.55) + DOWN * 0.72)
        lab_nadh = T("NADH", 32, PURPLE, weight=BOLD).move_to(bar_c + RIGHT * (BAR_W / 2 - 0.6) + DOWN * 0.72)
        pool_lab = T("NAD pool: a fixed total", 28, GREY).move_to([0, -3.2, 0])

        # --- chips -----------------------------------------------------------------------------------
        gly = chip("glycolysis", BLUE, size=36).move_to([-3.9, 1.95, 0])
        gly_sub = T("glyceraldehyde 3-phosphate step", 24, GREY).move_to([-3.45, 2.8, 0])
        pyr = chip("pyruvate", BLUE, size=34).move_to([1.3, 1.95, 0])
        prod = chip("lactate\nor ethanol", BLUE, size=28).move_to([5.2, 1.95, 0])
        rx_arrow = link(pyr.get_right() + RIGHT * 0.1, prod.get_left() + LEFT * 0.1, color=BLUE, w=5)

        TOP = -0.85
        A0, A1 = np.array([-3.3, TOP, 0]), np.array([-4.4, 1.05, 0])   # pool -> glycolysis (NAD+ out)
        B0, B1 = np.array([-3.4, 1.05, 0]), np.array([-2.5, TOP, 0])   # glycolysis -> pool (NADH back)
        C0, C1 = np.array([2.5, TOP, 0]), np.array([2.75, 1.05, 0])    # pool -> fermentation (NADH out)
        D0, D1 = np.array([3.65, 1.05, 0]), np.array([3.3, TOP, 0])    # fermentation -> pool (NAD+ back)
        arcA = ArcBetweenPoints(A0, A1, angle=-0.35)
        arcB = ArcBetweenPoints(B0, B1, angle=-0.35)
        arcC = ArcBetweenPoints(C0, C1, angle=-0.35)
        arcD = ArcBetweenPoints(D0, D1, angle=-0.35)

        def token(color):
            return Circle(radius=0.21, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.95).set_z_index(4)

        def recolor(tok, color):
            return tok.animate.set_stroke(color).set_fill(color, 0.95)

        # --- build the pool ---------------------------------------------------------------------------
        self.play(FadeIn(heading), run_time=0.6)
        self.at("redox bookkeeping")
        self.play(Create(box), FadeIn(bar_m), FadeIn(lab_nad), FadeIn(lab_nadh), FadeIn(pool_lab), run_time=1.0)

        # --- glycolysis consumes NAD+ and makes NADH ---------------------------------------------------
        self.at("Glycolysis consumes")
        self.play(FadeIn(gly, shift=DOWN * 0.15), run_time=0.5)
        tk = token(TEAL).move_to(A0)
        self.add(tk)
        self.at("consumes NAD")
        self.play(MoveAlongPath(tk, arcA), run_time=0.9)
        self.at("and produces NADH")
        self.play(tk.animate.move_to(B0).set_stroke(PURPLE).set_fill(PURPLE, 0.95), run_time=0.5)
        self.play(MoveAlongPath(tk, arcB), f.animate.set_value(0.1), run_time=0.9)
        self.remove(tk)
        self.at("glyceraldehyde 3 phosphate step")
        self.play(FadeIn(gly_sub), run_time=0.5)

        def left_trip(f_to, rt):
            k = token(TEAL).move_to(A0)
            self.add(k)
            self.play(MoveAlongPath(k, arcA), run_time=rt)
            self.play(k.animate.move_to(B0).set_stroke(PURPLE).set_fill(PURPLE, 0.95), run_time=rt * 0.5)
            self.play(MoveAlongPath(k, arcB), f.animate.set_value(f_to), run_time=rt)
            self.remove(k)

        # --- but the pool is finite: it runs out ------------------------------------------------------
        self.at("But the cell has only")
        self.play(Indicate(box, color=TEAL, scale_factor=1.03), run_time=0.7)
        left_trip(0.4, 0.3)
        left_trip(0.7, 0.3)
        left_trip(1.0, 0.3)
        stall = T("no NAD+ left:\nstalls", 28, RED, line_spacing=0.8).move_to([-5.3, 0.1, 0])
        self.play(gly[0].animate.set_stroke(RED), gly[1].animate.set_color(RED), FadeIn(stall), run_time=0.5)

        # --- fermentation regenerates NAD+ ------------------------------------------------------------
        self.at("Fermentation regenerates")
        self.play(FadeIn(pyr), run_time=0.5)
        self.play(Create(rx_arrow), FadeIn(prod), run_time=0.5)
        self.at("passing electrons from")
        tk = token(PURPLE).move_to(C0)
        self.add(tk)
        self.play(MoveAlongPath(tk, arcC), f.animate.set_value(0.88), run_time=1.0)
        e1 = electron(34).next_to(tk, UP, buff=0.12)
        self.play(FadeIn(e1, scale=0.6), run_time=0.2)
        self.at("onto pyruvate")
        self.play(e1.animate.move_to(pyr.get_center() + DOWN * 0.05).set_opacity(0.0),
                  pyr[0].animate.set_stroke(TEXT), tk.animate.move_to(D0).set_stroke(TEAL).set_fill(TEAL, 0.95),
                  run_time=0.9)
        self.remove(e1)
        self.at("producing either lactate")
        self.play(prod[0].animate.set_fill(BLUE, 0.45), pyr[0].animate.set_stroke(BLUE),
                  MoveAlongPath(tk, arcD), f.animate.set_value(0.8), run_time=1.0)
        self.remove(tk)

        # --- two cycles, coupled -----------------------------------------------------------------------
        self.at("The two cycles")
        arrows = VGroup(*[a.copy().set_stroke(c, 5) for a, c in ((arcA, TEAL), (arcB, PURPLE), (arcC, PURPLE), (arcD, TEAL))])
        for a in arrows:
            a.add_tip(tip_length=0.22, tip_width=0.22)
        self.play(FadeOut(stall), gly[0].animate.set_stroke(BLUE), gly[1].animate.set_color(BLUE),
                  prod[0].animate.set_fill(BLUE, 0.16), run_time=0.5)
        self.play(Create(arrows), run_time=0.8)
        self.at("consume NAD plus here")
        lab_l = T("consumes\nNAD+", 28, TEAL, line_spacing=0.8).move_to([-5.4, 0.0, 0])
        self.play(FadeIn(lab_l), run_time=0.4)
        tk = token(TEAL).move_to(A0)
        self.add(tk)
        self.play(MoveAlongPath(tk, arcA), run_time=0.8)
        self.at("regenerate it there")
        lab_r = T("regenerates\nNAD+", 28, TEAL, line_spacing=0.8).move_to([5.2, 0.0, 0])
        self.play(tk.animate.move_to(B0).set_stroke(PURPLE).set_fill(PURPLE, 0.95), FadeIn(lab_r), run_time=0.4)
        tk2 = token(PURPLE).move_to(C0)
        self.add(tk2)
        self.play(MoveAlongPath(tk, arcB), MoveAlongPath(tk2, arcC), run_time=0.8)
        self.remove(tk)
        self.at("so that glycolysis can keep")
        self.play(tk2.animate.move_to(D0).set_stroke(TEAL).set_fill(TEAL, 0.95), run_time=0.3)
        self.play(MoveAlongPath(tk2, arcD), f.animate.set_value(0.5), run_time=0.8)
        self.remove(tk2)
        self.play(Indicate(gly, color=BLUE, scale_factor=1.08), run_time=0.9)
        self.finish()


# ============================================================================================
class S03Valves(SpokenScene):
    """Plumbing: a reversible step is a valve you can partly close and the levels still equalize; an
    irreversible step is a one-way valve and is where control actually works."""

    def construct(self):
        # flux model: reversible step J = m*k/(k+m) (k = 10*openness, m = 1: huge spare capacity),
        # irreversible step J = 0.909*openness (the step IS the bottleneck). Both read 0.909 when fully open.
        def j_rev(o):
            k = 10.0 * o
            return k / (k + 1.0)

        def j_irr(o):
            return 0.909 * o

        heading = T("Control: a plumbing metaphor", 38, font=TITLE_FONT).to_edge(UP, buff=0.45)
        self.play(FadeIn(heading), run_time=0.6)

        # ---- one pipe: the pathway ---------------------------------------------------------------------
        PY = -0.4
        def pipe(x0, x1, y=PY, w=0.5):
            return VGroup(Line([x0, y + w / 2, 0], [x1, y + w / 2, 0], color=GREY, stroke_width=4),
                          Line([x0, y - w / 2, 0], [x1, y - w / 2, 0], color=GREY, stroke_width=4))
        full_pipe = pipe(-6.0, 6.0)
        full_stream = Stream([[-6.0, PY, 0], [6.0, PY, 0]], 14, BLUE, speed=2.0)
        full_lab = T("a metabolic pathway", 32, BLUE).move_to([0, 0.7, 0])
        self.at("Think of a metabolic pathway")
        self.play(Create(full_pipe), FadeIn(full_lab), run_time=0.8)
        self.add(full_stream.dots)
        self.wait(0.6)

        # ---- left panel: reversible -------------------------------------------------------------------
        LX, RX = -3.2, 3.2
        closeL = ValueTracker(0.0)
        hL, hR = ValueTracker(2.0), ValueTracker(0.45)
        TW, TH, TY = 1.3, 2.5, 0.3
        tankL = Rectangle(width=TW, height=TH, stroke_color=GREY, stroke_width=3).move_to([LX - 2.0, TY, 0])
        tankR = Rectangle(width=TW, height=TH, stroke_color=GREY, stroke_width=3).move_to([LX + 2.0, TY, 0])

        def water(tank, h):
            def mk():
                hv = max(h.get_value(), 0.02)
                return Rectangle(width=TW - 0.08, height=hv, stroke_width=0, fill_color=BLUE, fill_opacity=0.55) \
                    .move_to([tank.get_center()[0], tank.get_bottom()[1] + 0.04 + hv / 2, 0])
            return always_redraw(mk)
        wL, wR = water(tankL, hL), water(tankR, hR)
        pipeL = pipe(LX - 1.35, LX + 1.35, y=PY, w=0.4)
        VX = LX

        def valve_parts(x, color, close_tracker, y=PY):
            body = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
            stem = Line([x, y + 0.34, 0], [x, y + 0.75, 0], color=color, stroke_width=4)

            def handle():
                ang = close_tracker.get_value() * PI / 2
                return Line([x - 0.32, y + 0.75, 0], [x + 0.32, y + 0.75, 0], color=color, stroke_width=6) \
                    .rotate(ang, about_point=[x, y + 0.75, 0])

            def gate():
                c = close_tracker.get_value()
                h = max(0.01, 0.4 * c)
                return Rectangle(width=0.16, height=h, stroke_width=0, fill_color=color, fill_opacity=1) \
                    .move_to([x, y + 0.2 - h / 2, 0])
            return body, stem, always_redraw(handle), always_redraw(gate)
        vL_body, vL_stem, vL_handle, vL_gate = valve_parts(VX, GREEN, closeL)
        titleL = VGroup(T("reversible", 34, GREEN), M("ΔG ≈ 0", 26, GREY)).arrange(DOWN, buff=0.1).move_to([LX, 2.45, 0])
        panelL = VGroup(tankL, pipeL, vL_body, vL_stem)

        self.at("A reversible reaction")
        self.play(FadeOut(full_lab), FadeOut(full_pipe), full_stream.alpha.animate.set_value(0.0), FadeIn(titleL), run_time=0.7)
        full_stream.dots.clear_updaters()
        self.remove(full_stream.dots)
        self.play(Create(tankL), Create(tankR), Create(pipeL), FadeIn(wL), FadeIn(wR), run_time=0.8)
        self.play(FadeIn(vL_body), FadeIn(vL_stem), FadeIn(vL_handle), FadeIn(vL_gate), run_time=0.5)
        self.at("partially close")
        self.play(closeL.animate.set_value(0.5), run_time=1.4)
        self.at("Pressure equilibrates")
        self.play(hL.animate.set_value(1.25), hR.animate.set_value(1.2), run_time=2.0, rate_func=smooth)
        cap_eq = T("levels equalize", 28, GREEN).move_to([LX, -1.45, 0])
        self.play(FadeIn(cap_eq), run_time=0.3)

        # ---- right panel: irreversible ----------------------------------------------------------------
        closeR = ValueTracker(0.0)
        openR = lambda: 1.0 - closeR.get_value()
        pipeR = pipe(RX - 2.9, RX + 2.9, y=PY, w=0.4)
        streamR = Stream([[RX - 2.9, PY, 0], [RX + 2.9, PY, 0]], 12, BLUE, speed=1.8)
        gx = RX

        def dimR(p):
            return 1.0 if p[0] < gx else min(1.0, openR() * 4.0)
        streamR.dim = dimR

        def rate_tick(m, dt):
            streamR.rate.set_value(openR())
        streamR.dots.add_updater(rate_tick)
        vR_body, vR_stem, vR_handle, vR_gate = valve_parts(RX, RED, closeR)
        for part, z in ((vR_body, 3), (vR_stem, 3), (vR_handle, 4), (vR_gate, 4)):
            part.set_z_index(z)
        vR_arrow = Triangle(color=RED, fill_color=RED, fill_opacity=0.9, stroke_width=0).scale(0.15).rotate(-PI / 2).move_to([RX + 0.02, PY - 0.06, 0]).set_z_index(5)
        titleR = VGroup(T("irreversible", 34, RED), M("ΔG ≪ 0", 26, GREY)).arrange(DOWN, buff=0.1).move_to([RX, 2.45, 0])
        divider = DashedLine([0, 2.9, 0], [0, -2.9, 0], color=GREY, stroke_width=2, dash_length=0.12).set_opacity(0.5)

        self.at("An irreversible reaction")
        self.play(FadeIn(titleR), FadeIn(divider), Create(pipeR), run_time=0.7)
        self.play(FadeIn(vR_body), FadeIn(vR_stem), FadeIn(vR_handle), FadeIn(vR_gate), FadeIn(vR_arrow), run_time=0.5)
        self.add(streamR.dots)
        self.at("one way valve")
        self.play(Indicate(vR_body, color=RED, scale_factor=1.25), run_time=0.9)

        # ---- gauges ------------------------------------------------------------------------------------
        def gauge(x, jfun_tracker, label_color=BLUE):
            outline = Rectangle(width=4.2, height=0.32, stroke_color=GREY, stroke_width=2).move_to([x, -2.45, 0])

            def fill():
                w = max(0.01, 4.2 * jfun_tracker())
                return Rectangle(width=w, height=0.32, stroke_width=0, fill_color=BLUE, fill_opacity=0.9) \
                    .align_to(outline, LEFT).align_to(outline, DOWN)
            lab = T("flux", 26, BLUE).next_to(outline, UP, buff=0.12).align_to(outline, LEFT)
            return outline, always_redraw(fill), lab
        gL = gauge(LX, lambda: j_rev(1.0 - closeL.get_value()))
        gR = gauge(RX, lambda: j_irr(openR()))
        self.at("Close it and flow stops")
        self.play(*[FadeIn(m) for m in (*gL, *gR)], run_time=0.5)
        self.play(closeR.animate.set_value(1.0), run_time=1.4)
        stopped = T("flow stops", 28, RED).move_to([RX, 1.05, 0])
        self.play(FadeIn(stopped), run_time=0.3)
        self.wait(0.15)
        self.play(closeR.animate.set_value(0.0), FadeOut(stopped), closeL.animate.set_value(0.0), run_time=0.8)

        # ---- control works at irreversible steps ---------------------------------------------------------
        self.at("Cells regulate")
        ring = Circle(radius=0.62, stroke_color=GOLD, stroke_width=5).move_to([RX, PY, 0])
        reg = T("where cells regulate", 30, GOLD).move_to([RX, 1.35, 0])
        self.play(Create(ring), FadeIn(reg), run_time=0.9)
        self.at("irreversible steps")
        self.play(Indicate(ring, color=GOLD, scale_factor=1.15), run_time=0.9)
        self.at("control actually works")
        banner = T("control works where a step is one-way", 32, GOLD).move_to([0, -3.25, 0])
        self.play(FadeIn(banner), run_time=0.6)

        # ---- the two knobs ------------------------------------------------------------------------------
        self.at("Turn a knob")
        self.play(FadeOut(reg), FadeOut(ring), FadeOut(banner), run_time=0.4)
        self.play(closeL.animate.set_value(0.5), run_time=1.4)
        barely = T("barely changes", 28, GREEN).move_to([LX, -3.0, 0])
        self.play(FadeIn(barely), run_time=0.4)
        self.at("Block an irreversible step")
        self.play(FadeOut(barely), run_time=0.3)
        self.play(closeR.animate.set_value(1.0), run_time=1.4)
        shut = T("the whole line shuts down", 30, RED).move_to([RX, 1.05, 0])
        self.play(FadeIn(shut), run_time=0.5)
        self.finish()


# ============================================================================================
class S04Checkpoints(SpokenScene):
    """The three regulated enzymes and who talks to them."""

    def construct(self):
        SX = 0.0
        ys = 2.8 - 0.6 * np.arange(10)
        nodes = [node(i + 1, r=0.25, fs=22).move_to([SX, ys[i], 0]) for i in range(10)]
        glu = T("glucose", 28, BLUE).move_to([SX, 3.3, 0])
        pyr = T("pyruvate", 28, BLUE).move_to([SX, -3.2, 0])
        links = [link(glu.get_bottom() + DOWN * 0.03, nodes[0].get_top())]
        links += [link(nodes[i].get_bottom(), nodes[i + 1].get_top()) for i in range(9)]
        links.append(link(nodes[9].get_bottom(), pyr.get_top() + UP * 0.03))
        self.play(FadeIn(glu), LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.12),
                  LaggedStart(*[Create(l) for l in links], lag_ratio=0.12), FadeIn(pyr), run_time=2.6)

        def pill(idx, text):
            lab = VGroup(M(str(idx + 1), 24, GREY), T(text, 30, TEXT)).arrange(RIGHT, buff=0.2)
            box = RoundedRectangle(corner_radius=0.16, width=lab.width + 0.55, height=0.62, stroke_color=GOLD,
                                   stroke_width=4, fill_color=GOLD, fill_opacity=0.14).move_to([SX, ys[idx], 0])
            return VGroup(box, lab.move_to(box)).set_z_index(2)
        hk, pfk, pk = pill(0, "hexokinase"), pill(2, "PFK-1"), pill(9, "pyruvate kinase")

        self.at("hexokinase")
        self.play(ReplacementTransform(nodes[0], hk), run_time=0.7)
        self.at("phosphofructokinase 1")
        self.play(ReplacementTransform(nodes[2], pfk), run_time=0.7)
        self.at("and pyruvate kinase")
        self.play(ReplacementTransform(nodes[9], pk), run_time=0.7)
        self.at("Each responds to different")
        self.play(Indicate(hk, color=GOLD), Indicate(pfk, color=GOLD), Indicate(pk, color=GOLD), run_time=1.2)

        # --- hexokinase: product inhibition ------------------------------------------------------------
        g6p = chip("glucose-6-phosphate", GREY, size=28).move_to([-4.0, 2.15, 0])
        inh_g6p = inhibit(g6p.get_right() + RIGHT * 0.05, hk.get_left() + LEFT * 0.14 + DOWN * 0.05, bend=0.5)
        self.at("Hexokinase is inhibited")
        self.play(Indicate(hk, color=RED, scale_factor=1.1), run_time=0.8)
        self.at("its own product")
        self.play(FadeIn(g6p, shift=RIGHT * 0.2), Create(inh_g6p), run_time=0.8)

        # --- PFK-1: the master throttle ----------------------------------------------------------------
        amp = chip("AMP", GREY, size=28).move_to([-3.4, 2.45, 0])
        f26 = chip("fructose-2,6-\nbisphosphate", GREY, size=28).move_to([-3.7, 0.75, 0])
        atp = chip("ATP", YELLOW, size=28).move_to([3.0, 2.4, 0])
        cit = chip("citrate", GREY, size=28).move_to([3.0, 0.8, 0])
        a_amp = activate(amp.get_right() + RIGHT * 0.05, pfk.get_left() + LEFT * 0.04 + UP * 0.05, bend=0.35)
        a_f26 = activate(f26.get_right() + RIGHT * 0.05, pfk.get_left() + LEFT * 0.04 + DOWN * 0.05, bend=-0.35)
        i_atp = inhibit(atp.get_left() + LEFT * 0.05, pfk.get_right() + RIGHT * 0.04 + UP * 0.05, bend=-0.35)
        i_cit = inhibit(cit.get_left() + LEFT * 0.05, pfk.get_right() + RIGHT * 0.04 + DOWN * 0.05, bend=0.35)
        self.at("PFK 1 is the master throttle")
        self.play(FadeOut(g6p), FadeOut(inh_g6p), run_time=0.4)
        self.play(Indicate(pfk, color=GOLD, scale_factor=1.15), run_time=0.9)
        self.at("activated by AMP")
        self.play(FadeIn(amp, shift=RIGHT * 0.2), Create(a_amp), run_time=0.7)
        self.at("and fructose 2 6 bisphosphate")
        self.play(FadeIn(f26, shift=RIGHT * 0.2), Create(a_f26), run_time=0.8)
        self.at("inhibited by ATP")
        self.play(FadeIn(atp, shift=LEFT * 0.2), Create(i_atp), run_time=0.6)
        self.at("and citrate")
        self.play(FadeIn(cit, shift=LEFT * 0.2), Create(i_cit), run_time=0.6)

        # --- pyruvate kinase: feed-forward -------------------------------------------------------------
        # F-1,6-BP is PFK-1's product: it sits on the link between step 3 and step 4, and activates step 10.
        jy = (ys[2] + ys[3]) / 2
        j0 = np.array([SX - 0.12, jy, 0])
        ff = activate(j0, pk.get_left() + LEFT * 0.04, bend=1.6, color=GREEN)
        f16 = chip("fructose-1,6-\nbisphosphate", GREY, size=28)
        f16.move_to([SX - 3.5, jy, 0])
        tie = Line(f16.get_right() + RIGHT * 0.05, j0, color=GREY, stroke_width=3)
        self.at("Pyruvate kinase is activated")
        self.play(Indicate(pk, color=GOLD, scale_factor=1.15), run_time=0.9)
        self.at("feed forward")
        self.play(*[FadeOut(m) for m in (amp, a_amp, f26, a_f26, atp, i_atp, cit, i_cit)], run_time=0.35)
        self.play(Create(ff), run_time=0.75)
        self.at("by fructose 1 6 bisphosphate")
        self.play(FadeIn(f16, shift=RIGHT * 0.2), Create(tie), run_time=0.6)

        # --- together ---------------------------------------------------------------------------------
        self.at("Together these three")
        self.play(FadeOut(ff), FadeOut(f16), FadeOut(tie), run_time=0.6)
        self.at("three checkpoints")
        self.play(Indicate(hk, color=GOLD), Indicate(pfk, color=GOLD), Indicate(pk, color=GOLD), run_time=1.0)
        self.at("match glycolytic flux")
        spine = VGroup(glu, pyr, hk, pfk, pk, *[n for i, n in enumerate(nodes) if i not in (0, 2, 9)], *links)
        lvl = ValueTracker(0.45)
        BASE, HMAX = -2.2, 4.4

        def bar(x, color):
            return always_redraw(lambda: Rectangle(width=1.6, height=max(0.02, HMAX * lvl.get_value()), stroke_width=0,
                                                   fill_color=color, fill_opacity=0.9)
                                 .move_to([x, BASE + max(0.02, HMAX * lvl.get_value()) / 2, 0]))
        bar_f, bar_n = bar(-2.6, BLUE), bar(2.6, YELLOW)
        base = Line([-5.2, BASE, 0], [5.2, BASE, 0], color=GREY, stroke_width=3)
        lab_f = T("glycolytic flux", 32, BLUE).move_to([-2.6, BASE - 0.5, 0])
        lab_n = T("energy needs", 32, YELLOW).move_to([2.6, BASE - 0.5, 0])
        self.play(FadeOut(spine), run_time=0.35)
        self.play(Create(base), FadeIn(bar_f), FadeIn(lab_f), run_time=0.6)
        self.at("energy needs")
        self.play(FadeIn(bar_n), FadeIn(lab_n), run_time=0.4)
        self.play(lvl.animate.set_value(0.9), run_time=0.55)
        self.play(lvl.animate.set_value(0.3), run_time=0.55)
        self.finish()


# ============================================================================================
class S05Gate(SpokenScene):
    """Glucose passes the PFK-1 turnstile at step 3; fructose joins below it, so its flux is not gated."""

    def construct(self):
        PX = 0.8
        ys = 2.75 - 0.6 * np.arange(10)
        pipe_box = RoundedRectangle(corner_radius=0.3, width=0.9, height=6.0, stroke_color=GREY, stroke_width=3,
                                    fill_opacity=0).move_to([PX, 0.025, 0])
        glu = T("glucose", 28, BLUE).move_to([PX, 3.35, 0])
        pyr = T("pyruvate", 28, BLUE).move_to([PX, -3.32, 0])
        ticks = VGroup(*[M(str(i + 1), 22, GREY).move_to([PX + 0.75, ys[i], 0]) for i in range(10)])

        # turnstile at step 3: hub with three rotating arms across the pipe
        rot = ValueTracker(0.0)
        hub_c = np.array([PX, ys[2], 0])

        def turnstile():
            g = VGroup(Circle(radius=0.12, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(hub_c))
            for k in range(3):
                a = rot.get_value() + k * TAU / 3 + PI / 2
                g.add(Line(hub_c, hub_c + 0.42 * np.array([np.cos(a), np.sin(a), 0]), color=GOLD, stroke_width=7))
            g.add(Circle(radius=0.5, stroke_color=GOLD, stroke_width=3).move_to(hub_c))
            return g.set_z_index(3)
        turn = always_redraw(turnstile)

        blue = Stream([[PX, 3.0, 0], [PX, -2.95, 0]], 22, BLUE, speed=2.2, rate=0.0, vis=1.0, jitter=0.2)
        orange = Stream([[-4.05, ys[3], 0], [PX, ys[3], 0], [PX, -2.95, 0]], 26, ORANGE, speed=2.4, rate=0.0, vis=0.0, jitter=0.15)
        blue_rate = ValueTracker(0.0)

        def blue_tick(m, dt):
            blue.rate.set_value(blue_rate.get_value())
            rot.set_value(rot.get_value() + dt * blue_rate.get_value() * 2.4)
        blue.dots.add_updater(blue_tick)

        self.play(Create(pipe_box), FadeIn(glu), FadeIn(pyr), FadeIn(ticks), run_time=0.45)
        self.at("phosphofructokinase 1")
        pfk_lab = T("PFK-1", 34, GOLD, weight=BOLD).move_to([PX + 2.15, ys[2] + 0.17, 0])
        step_lab = T("step 3", 28, GREY).move_to([PX + 2.15, ys[2] - 0.3, 0])
        self.play(FadeIn(turn), FadeIn(pfk_lab), run_time=0.7)
        self.at("as a turnstile")
        self.play(Indicate(turn, color=GOLD, scale_factor=1.2), run_time=0.9)

        # --- glucose must pass, the cell sets the rate ---------------------------------------------------
        self.at("Glucose must pass through")
        self.add(blue.dots)
        self.play(blue_rate.animate.set_value(0.8), run_time=0.6)
        self.at("at step 3")
        self.play(FadeIn(step_lab), run_time=0.4)
        self.at("which means the cell can regulate")
        set_lab = T("the cell sets the rate", 28, GOLD).move_to([PX + 3.5, ys[2] + 1.0, 0])
        self.play(FadeIn(set_lab), run_time=0.4)
        self.at("regulate exactly")
        self.play(blue_rate.animate.set_value(0.25), run_time=1.0)
        self.play(blue_rate.animate.set_value(0.8), run_time=1.0)

        # --- fructose enters below the gate -------------------------------------------------------------
        self.at("Fructose by contrast")
        fru = chip("fructose", ORANGE, size=30).move_to([-5.0, ys[3], 0])
        self.play(FadeOut(set_lab), FadeIn(fru, shift=RIGHT * 0.2), run_time=0.6)
        self.at("sneaks in downstream")
        in_arrow = link(fru.get_right() + RIGHT * 0.05, [PX - 0.47, ys[3], 0], color=ORANGE, w=5)
        self.add(orange.dots)
        self.play(Create(in_arrow), orange.rate.animate.set_value(0.8), orange.vis.animate.set_value(0.3), run_time=0.9)
        self.at("It bypasses the gate")
        nogate = T("no gate here", 30, RED).move_to([PX - 2.0, ys[3] - 0.45, 0])
        self.play(FadeIn(nogate), run_time=0.5)
        self.at("and enters as D chap")
        dhap = chip("DHAP", ORANGE, size=26).move_to([-3.5, ys[3] + 1.0, 0])
        self.play(FadeIn(dhap, shift=DOWN * 0.1), run_time=0.5)
        self.at("and glyceraldehyde 3")
        g3p = chip("glyceraldehyde 3-phosphate", ORANGE, size=26).move_to([-2.6, ys[3] - 0.9, 0])
        self.play(FadeOut(nogate), FadeIn(g3p, shift=UP * 0.1), run_time=0.5)

        # --- the result: unregulated flux below the gate -------------------------------------------------
        GX, GY0, GH = 5.0, -2.65, 3.1
        bx = Rectangle(width=0.7, height=GH, stroke_color=GREY, stroke_width=2).move_to([GX, GY0 + GH / 2, 0])
        LIM = 0.55
        lim = DashedLine([GX - 0.6, GY0 + GH * LIM, 0], [GX + 0.6, GY0 + GH * LIM, 0], color=GOLD, stroke_width=3)
        lim_lab = T("regulated\nlimit", 26, GOLD, line_spacing=0.8).next_to(lim, LEFT, buff=0.1)
        bflux = ValueTracker(0.3)
        oflux = ValueTracker(0.0)

        def fills():
            b, o = bflux.get_value(), oflux.get_value()
            g = VGroup()
            hb = max(0.01, GH * b)
            g.add(Rectangle(width=0.62, height=hb, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([GX, GY0 + hb / 2, 0]))
            if o > 0.005:
                ho = GH * o
                over = (b + o) > LIM
                g.add(Rectangle(width=0.62, height=ho, stroke_width=0, fill_color=RED if over else ORANGE,
                                fill_opacity=0.9).move_to([GX, GY0 + hb + ho / 2, 0]))
            return g
        gfill = always_redraw(fills)
        g_title = T("flux below\nthe gate", 26, TEXT, line_spacing=0.8).move_to([GX - 0.1, GY0 + GH + 0.6, 0])

        self.at("The result is uncontrolled")
        self.play(Create(bx), FadeIn(gfill), FadeIn(g_title), Create(lim), FadeIn(lim_lab), run_time=0.8)
        self.at("carbon flow straight")
        self.play(orange.vis.animate.set_value(1.0), orange.rate.animate.set_value(1.5), oflux.animate.set_value(0.18), run_time=1.0)
        self.at("pyruvate")
        self.play(Indicate(pyr, color=BLUE, scale_factor=1.2), run_time=0.8)
        self.at("which is why excess dietary")
        self.play(oflux.animate.set_value(0.6), orange.rate.animate.set_value(2.2), run_time=1.5)
        self.at("overwhelm normal metabolic")
        over = T("overwhelmed", 32, RED).move_to([GX - 0.3, -3.2, 0])
        self.play(FadeIn(over), run_time=0.5)
        self.finish()


# ============================================================================================
class S06End(EndCard):
    LINE = "Glycolysis: spend ATP, balance NAD+, guard the gates."
