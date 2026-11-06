"""One Site, One Curve  (chapter 2 of "Protein Binding and Allostery")

COLOR MAP (one color per concept, shared with the other chapters of this lesson)
  BLUE   = protein / receptor / myoglobin, and the one-site hyperbola
  YELLOW = ligand, O2, the half-saturation marker and the 'bound' amount on plots
  GREEN  = tighter binding
  GOLD   = Kd / P50 and other call-outs; hemoglobin's curve
  TEAL   = Ka, the reciprocal
  RED    = crossed out (cancelled) terms, wrong readings
  TEXT   = equations, neutral labels;  GREY = axes, secondary labels
NO molecular structures: receptors are labelled blocks with a socket, ligands are dots, and every
curve is computed from  Y = L / (Kd + L)  (hemoglobin's S from the Hill equation, n = 2.8, P50 = 26 torr).
"""
import numpy as np

from bp_style import *


# ---------------------------------------------------------------- motion helpers
def key_pos(keys, t):
    """Position at time t from keyframes [(t, point), ...], smooth between keys, held at the ends."""
    if t <= keys[0][0]:
        return np.array(keys[0][1], dtype=float)
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if t <= t1:
            a = smooth((t - t0) / (t1 - t0)) if t1 > t0 else 1.0
            return np.array(p0, dtype=float) + (np.array(p1, dtype=float) - np.array(p0, dtype=float)) * a
    return np.array(keys[-1][1], dtype=float)


def follow_keys(mob, keys):
    """Move mob along keyframes, timed from the moment it is added to the scene."""
    mob.kt = 0.0
    mob.move_to(key_pos(keys, 0.0))

    def upd(m, dt):
        m.kt += dt
        m.move_to(key_pos(keys, m.kt))
    mob.add_updater(upd)
    return mob


class Rec(VGroup):
    """A receptor: a labelled-cartoon block with a socket on top. Lit = a ligand is bound."""

    def __init__(self, w=1.2, h=1.1, lit=False):
        super().__init__()
        self.blk = RoundedRectangle(corner_radius=0.14 * min(1, w), width=w, height=h, stroke_color=BLUE,
                                    stroke_width=3, fill_color=BLUE, fill_opacity=0.5 if lit else 0.12)
        self.sock = Circle(radius=0.2 * w, stroke_color=BLUE, stroke_width=3, fill_color=BG, fill_opacity=1)
        self.sock.move_to(self.blk.get_top() + DOWN * 0.27 * w)
        self.add(self.blk, self.sock)
        self.w = w

    def sock_pos(self):
        return self.sock.get_center()

    def lit_anim(self, on):
        return self.blk.animate.set_fill(BLUE, 0.5 if on else 0.12)


def lit_by(rec, ligs):
    """Light the receptor whenever one of the ligands sits in its socket."""
    def upd(m, dt):
        on = any(np.linalg.norm(l.get_center() - m.sock_pos()) < 0.1 for l in ligs)
        cur = m.blk.get_fill_opacity()
        tgt = 0.5 if on else 0.12
        m.blk.set_fill(BLUE, cur + (tgt - cur) * min(1.0, dt * 12))
    rec.add_updater(upd)


def lig(r=0.2):
    return Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=1).set_z_index(3)


def bound_pair(w=1.2, h=1.1):
    r = Rec(w, h, lit=True)
    l = lig(0.15 * w).move_to(r.sock_pos())
    return VGroup(r, l), r, l


def kd_eq(size=56):
    num = VGroup(M("[R]", size, BLUE), M("[L]", size, YELLOW)).arrange(RIGHT, buff=0.12)
    den = M("[RL]", size, TEXT)
    bar = Line(LEFT, RIGHT, color=TEXT, stroke_width=4).set_width(num.width + 0.4)
    frac = VGroup(num, bar, den).arrange(DOWN, buff=0.18)
    eq = VGroup(M("Kd =", size, GOLD), frac).arrange(RIGHT, buff=0.3)
    return eq, num, den, frac


# ---------------------------------------------------------------- plot frames
class Frame:
    """A plot frame drawn by hand so the x scale can be broken or morphed. fx maps a data x to 0..1."""

    def __init__(self, x0, w, y0, h, fx):
        self.x0, self.w, self.y0, self.h, self.fx = x0, w, y0, h, fx

    def c2p(self, x, y):
        return np.array([self.x0 + self.w * float(self.fx(x)), self.y0 + self.h * y, 0.0])

    def curve(self, f, xs, color=BLUE, sw=6):
        pts = [self.c2p(x, f(x)) for x in xs]
        return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(pts)

    def lines(self, xmax):
        xl = Line(self.c2p(0, 0), self.c2p(xmax, 0), color=GREY, stroke_width=3)
        yl = Line(self.c2p(0, 0), self.c2p(0, 1.04), color=GREY, stroke_width=3)
        return VGroup(xl, yl)

    def xtick(self, x, lab, color=GREY, size=26):
        p = self.c2p(x, 0)
        mark = Line(p, p + DOWN * 0.1, color=GREY, stroke_width=3)
        t = M(lab, size, color).next_to(p, DOWN, buff=0.17)
        return VGroup(mark, t)

    def yticks(self):
        g = VGroup()
        for v, lab in [(0, "0"), (0.5, "0.5"), (1, "1")]:
            p = self.c2p(0, v)
            g.add(VGroup(Line(p, p + LEFT * 0.1, color=GREY, stroke_width=3),
                         M(lab, 26, GREY).next_to(p, LEFT, buff=0.18)))
        return g

    def ytitle(self, yt):
        t = T("fraction bound", 28, GREY).rotate(PI / 2)
        t.next_to(yt, LEFT, buff=0.22).set_y(self.y0 + self.h * 0.5)
        return t

    def xtitle(self, text, xmax):
        return T(text, 28, GREY).move_to([(self.c2p(0, 0)[0] + self.c2p(xmax, 0)[0]) / 2, self.y0 - 0.95, 0])


# generic one-site chart (s10, s12): x in units where Kd = 2
KD = 2.0
GEN = Frame(-4.3, 10.1, -2.3, 5.3, lambda x: x / 10.0)


def y1(x, kd=KD):
    return x / (kd + x)


def gen_base():
    lines = GEN.lines(10)
    yt = GEN.yticks()
    ytl = GEN.ytitle(yt)
    return lines, yt, ytl


def gen_curve(x1=10.0, color=BLUE, sw=6, x0=0.0):
    return GEN.curve(y1, np.linspace(x0, x1, 300), color, sw)


def gen_kd_marker():
    v = DashedLine(GEN.c2p(KD, 0), GEN.c2p(KD, 0.5), color=YELLOW, stroke_width=3)
    h = DashedLine(GEN.c2p(0, 0.5), GEN.c2p(KD, 0.5), color=YELLOW, stroke_width=3)
    d = Dot(GEN.c2p(KD, 0.5), color=YELLOW, radius=0.11).set_z_index(4)
    return VGroup(v, h, d)


# myoglobin chart (s13-s18): 0..20 torr gets 55% of the width so the rise is visible
BRK = 0.55


def f_broken(p):
    return p / 20 * BRK if p <= 20 else BRK + (p - 20) / 80 * (1 - BRK)


MB_B = (-1.5, 7.9, -2.45, 5.45)
MB_L = (-4.9, 10.6, -2.45, 5.45)


def mb_frame(a=0.0):
    x0, w, y0, h = [b * (1 - a) + l * a for b, l in zip(MB_B, MB_L)]
    return Frame(x0, w, y0, h, lambda p: (1 - a) * f_broken(p) + a * p / 100)


MBF = mb_frame(0.0)
MB_P50 = 2.0


def mb_y(p):
    return p / (MB_P50 + p)


def hb_y(p):
    return p ** 2.8 / (26.0 ** 2.8 + p ** 2.8)


def mb_ps(p0, p1):
    lo = np.linspace(p0, min(p1, 20), 260) if p0 < 20 else np.array([])
    hi = np.linspace(max(p0, 20), p1, 160) if p1 > 20 else np.array([])
    return np.concatenate([lo, hi])


def mb_curve(fr=MBF, p0=0.0, p1=100.0):
    return fr.curve(mb_y, mb_ps(p0, p1), BLUE, 6)


def mb_axes(fr=MBF, broken_op=1.0, lin_op=0.0):
    lines = fr.lines(100)
    yt = fr.yticks()
    ytl = fr.ytitle(yt)
    xtl = fr.xtitle("pO₂  (torr)", 100)
    tb = VGroup(*[fr.xtick(p, str(p)) for p in (0, 2, 5, 10, 20, 40, 60, 80, 100)])
    bp = fr.c2p(20, 0) + RIGHT * 0.2
    brk = VGroup(*[Line(bp + dx + DOWN * 0.13 + LEFT * 0.06, bp + dx + UP * 0.13 + RIGHT * 0.06, color=GREY, stroke_width=3)
                   for dx in (LEFT * 0.06, RIGHT * 0.06)])
    gap = Line(bp + LEFT * 0.06, bp + RIGHT * 0.06, color=BG, stroke_width=6)
    broken = VGroup(tb, gap, brk).set_opacity(broken_op)
    lin = VGroup(*[fr.xtick(p, str(p)) for p in (20, 40, 60, 80, 100)]).set_opacity(lin_op)
    return VGroup(lines, yt, ytl, xtl, broken, lin)


def mb_p50_marker(fr=MBF):
    v = DashedLine(fr.c2p(MB_P50, 0), fr.c2p(MB_P50, 0.5), color=GOLD, stroke_width=3)
    h = DashedLine(fr.c2p(0, 0.5), fr.c2p(MB_P50, 0.5), color=GOLD, stroke_width=3)
    d = Dot(fr.c2p(MB_P50, 0.5), color=GOLD, radius=0.11).set_z_index(4)
    return VGroup(v, h, d)


def mb_p50_label():
    txt = M("P50 ≈ 2 torr", 28, GOLD)
    txt.move_to(MBF.c2p(6, 0.37), aligned_edge=LEFT)
    lead = Arrow(txt.get_left() + LEFT * 0.05, MBF.c2p(MB_P50, 0.5) + RIGHT * 0.1 + DOWN * 0.05, color=GOLD, buff=0.06,
                 stroke_width=3, max_tip_length_to_length_ratio=0.12, tip_length=0.18)
    return VGroup(txt, lead)


def stmt(top, bottom, color=YELLOW):
    g = VGroup(M(top, 26, GREY), M(bottom, 38, color)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    return g


S100_POS = np.array([-6.6, 1.5, 0])
S20_POS = np.array([-6.6, -0.4, 0])


def place(g, pos):
    return g.move_to(pos, aligned_edge=LEFT)


# ---------------------------------------------------------------- cards
class S00Title(TitleCard):
    LESSON = "Protein Binding and Allostery"
    TITLE = "One Site, One Curve"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON, size=30, color=GREY)
        title = T(self.TITLE, size=80, font=TITLE_FONT)
        rule = Line(LEFT * 1.5, RIGHT * 1.5, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.38)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), FadeIn(title, shift=UP * 0.12),
                  GrowFromCenter(rule), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(g), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s01
class S01Q(SpokenScene):
    def construct(self):
        r = Rec(3.6, 3.3).move_to(LEFT * 3.0 + UP * 0.55)
        r_lab = T("receptor protein", 32, BLUE).next_to(r, DOWN, buff=0.3)
        s = r.sock_pos()
        la = follow_keys(lig(0.5), [(0, [3.2, 2.2, 0]), (0.5, [2.2, 2.5, 0]), (1.3, s), (2.5, s), (3.3, [1.0, 2.9, 0]),
                                    (4.5, [0.4, 2.7, 0])])
        lb = follow_keys(lig(0.5), [(0, [4.6, 0.2, 0]), (1.5, [3.9, -0.3, 0]), (3.0, [4.5, -0.9, 0]), (4.5, [4.0, -0.4, 0])])
        lc = follow_keys(lig(0.5), [(0, [2.4, -1.2, 0]), (1.6, [1.7, -0.6, 0]), (3.2, [2.3, -0.2, 0]), (4.5, [1.8, -0.9, 0])])
        l_lab = T("ligand", 32, YELLOW).add_updater(lambda m: m.next_to(lb, UP, buff=0.25))
        lit_by(r, [la])
        self.add(r, la, lb, lc)
        self.play(FadeIn(r), FadeIn(r_lab), FadeIn(l_lab), run_time=0.4)
        self.at("how tightly")
        q = T("How tightly does it hold on?", 46, GOLD).move_to(DOWN * 3.05)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- s02
class S02Stick(SpokenScene):
    def construct(self):
        recs = VGroup(*[Rec(1.9, 1.7) for _ in range(8)]).arrange_in_grid(2, 4, buff=(0.62, 0.55)).move_to(UP * 0.65)
        S = [r.sock_pos() for r in recs]
        U = lambda i: S[i] + UP * 1.0  # a hover point above socket i
        sched = [
            [(0, S[0]), (1.0, S[0]), (1.6, U(0)), (2.4, [-6.0, 1.0, 0])],                       # never permanent
            [(0, S[3]), (2.4, S[3]), (2.9, U(3)), (3.6, [6.0, 2.9, 0])],
            [(0, S[5]), (4.6, S[5]), (5.0, U(5) + RIGHT * 0.4), (5.8, [6.0, -1.6, 0])],        # coming apart
            [(0, S[6]), (6.0, S[6])],
            [(0, [-6.0, 3.1, 0]), (0.9, [-6.0, 3.1, 0]), (1.6, U(1)), (2.1, S[1]), (6.0, S[1])],
            [(0, [6.0, 0.6, 0]), (3.0, [6.0, 0.6, 0]), (3.6, U(2) + UP * 0.05), (4.1, S[2]), (6.0, S[2])],  # joining
            [(0, [-6.0, -1.9, 0]), (4.3, [-6.0, -1.9, 0]), (5.0, S[4] + LEFT * 1.4 + UP * 0.6), (5.6, S[4])],
        ]
        ligs = [follow_keys(lig(0.27), k) for k in sched]
        for r in recs:
            r.blk.set_fill(BLUE, 0.5 if any(np.linalg.norm(l.get_center() - r.sock_pos()) < 0.1 for l in ligs) else 0.12)
            lit_by(r, ligs)
        sw1 = Rec(0.8, 0.72, lit=True)
        sw1.add(lig(0.12).move_to(sw1.sock_pos()))
        t1 = T("bound", 32, TEXT)
        sw2 = Rec(0.8, 0.72, lit=False)
        t2 = T("free", 32, TEXT)
        leg = VGroup(sw1, t1, sw2, t2).arrange(RIGHT, buff=0.3)
        leg[2].shift(RIGHT * 0.9)
        leg[3].shift(RIGHT * 0.9)
        leg.move_to(DOWN * 3.15)
        self.add(recs, *ligs)
        self.play(FadeIn(recs), *[FadeIn(l) for l in ligs], FadeIn(leg), run_time=0.5)
        self.at("never permanent")
        self.wait(0.1)
        self.finish()


# ---------------------------------------------------------------- s03
def harpoons(length=1.3, color=TEXT, sw=5):
    top = Arrow(LEFT * length / 2, RIGHT * length / 2, color=color, buff=0, stroke_width=sw,
                max_tip_length_to_length_ratio=0.25, tip_length=0.22).shift(UP * 0.13)
    bot = Arrow(RIGHT * length / 2, LEFT * length / 2, color=color, buff=0, stroke_width=sw,
                max_tip_length_to_length_ratio=0.25, tip_length=0.22).shift(DOWN * 0.13)
    return VGroup(top, bot)


class S03Write(SpokenScene):
    def construct(self):
        eq = VGroup(M("RL", 66, TEXT), harpoons(1.3), M("R", 66, BLUE), M("+", 66, TEXT), M("L", 66, YELLOW))
        eq.arrange(RIGHT, buff=0.4).move_to(UP * 2.85)
        pair, r, l = bound_pair(3.0, 2.8)
        pair.move_to(LEFT * 4.4 + DOWN * 0.45)
        rl_lab = M("RL", 52, TEXT).next_to(pair, DOWN, buff=0.3)
        self.play(FadeIn(pair), FadeIn(rl_lab), run_time=0.4)
        self.play(Write(eq), run_time=0.8)
        self.at("direction")
        hp = harpoons(1.5, TEXT, 7).move_to(LEFT * 1.6 + DOWN * 0.45)
        self.play(GrowArrow(hp[0]), GrowArrow(hp[1]), Indicate(eq[1], color=GOLD, scale_factor=1.15), run_time=0.7)
        self.play(Indicate(hp[0], color=GOLD, scale_factor=1.15), run_time=0.6)
        self.at("bound complex")
        self.play(Indicate(pair, color=YELLOW, scale_factor=1.05), Indicate(eq[0], color=YELLOW), run_time=0.7)
        self.at("splits")
        fr = Rec(3.0, 2.8).move_to(RIGHT * 1.6 + DOWN * 0.45)
        fl = lig(0.45).move_to(RIGHT * 5.2 + DOWN * 0.45)
        plus = M("+", 60).move_to(RIGHT * 3.75 + DOWN * 0.45)
        rc = r.copy()
        lc = l.copy()
        self.add(rc, lc)
        self.play(lc.animate.shift(UP * 1.1), rc.animate.set_fill(BLUE, 0.12), run_time=0.3)
        self.play(Transform(rc, fr), lc.animate.move_to(fl), FadeIn(plus), run_time=0.45)
        self.at("free receptor")
        R_lab = M("R", 52, BLUE).next_to(fr, DOWN, buff=0.3)
        self.play(FadeIn(R_lab, shift=UP * 0.1), Indicate(eq[2], color=BLUE), run_time=0.5)
        self.at("free ligand")
        L_lab = M("L", 52, YELLOW).move_to([fl.get_x(), R_lab.get_y(), 0])
        self.play(FadeIn(L_lab, shift=UP * 0.1), Indicate(eq[4], color=YELLOW), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s04 / s05
EQ_POS = LEFT * 2.7 + DOWN * 0.1


def s04_parts():
    eq, num, den, frac = kd_eq(80)
    eq.move_to(EQ_POS)
    fr = Rec(1.05, 0.95).move_to([2.6, num.get_y(), 0])
    fl = lig(0.2).move_to([3.75, num.get_y(), 0])
    loose_t = T("loose", 34, TEXT).move_to([5.45, num.get_y(), 0])
    pair, r, l = bound_pair(1.05, 0.95)
    pair.move_to([3.15, den.get_y(), 0])
    bound_t = T("bound", 34, TEXT).move_to([5.45, den.get_y(), 0])
    name = T("dissociation constant", 42, GOLD).move_to(UP * 3.0)
    return eq, num, den, frac, fr, fl, loose_t, pair, bound_t, name


def row_box(row, span):
    """A highlight box around one row of the fraction, as wide as the whole row of terms and icons."""
    b = Rectangle(width=span.width + 0.35, height=row.height + 0.16, color=YELLOW, stroke_width=3)
    return b.move_to([span.get_center()[0], row.get_y(), 0])


class S04Kd(SpokenScene):
    def construct(self):
        eq, num, den, frac, fr, fl, loose_t, pair, bound_t, name = s04_parts()
        self.play(FadeIn(name, shift=DOWN * 0.1), run_time=0.4)
        ghost = frac.copy().set_opacity(0.25)
        self.play(FadeIn(eq[0]), FadeIn(ghost), run_time=0.5)
        self.at("kd")
        self.play(Indicate(eq[0], color=GOLD, scale_factor=1.12), run_time=0.6)
        self.at("ratio")
        self.play(FadeIn(frac), FadeOut(ghost), run_time=0.4)
        self.at("loose")
        g1 = row_box(num, VGroup(num, fr, fl, loose_t, bound_t))
        self.play(FadeIn(fr), FadeIn(fl), FadeIn(loose_t), Create(g1), run_time=0.4)
        self.at("bound")
        g2 = row_box(den, VGroup(num, fr, fl, loose_t, bound_t))
        self.play(FadeIn(pair), FadeIn(bound_t), ReplacementTransform(g1, g2), run_time=0.45)
        self.finish()


class S05Units(SpokenScene):
    def construct(self):
        eq, num, den, frac, fr, fl, loose_t, pair, bound_t, name = s04_parts()
        g2 = row_box(den, VGroup(num, fr, fl, loose_t, bound_t))
        self.add(eq, fr, fl, loose_t, pair, bound_t, name, g2)
        ut = VGroup(M("M", 72), M("×", 72), M("M", 72)).arrange(RIGHT, buff=0.25)
        ub = M("M", 72)
        ubar = Line(LEFT, RIGHT, color=TEXT, stroke_width=5).set_width(ut.width + 0.4)
        ufrac = VGroup(ut, ubar, ub).arrange(DOWN, buff=0.2)
        eqs = VGroup(ufrac, M("=", 72), M("M", 80, GOLD)).arrange(RIGHT, buff=0.4).move_to([3.9, eq.get_y(), 0])
        ufrac.align_to(frac, DOWN).shift(DOWN * 0.05)
        eqs[1].set_y(frac[1].get_y())
        eqs[2].set_y(frac[1].get_y())
        self.play(FadeOut(VGroup(fr, fl, loose_t, pair, bound_t, name, g2)), run_time=0.4)
        self.at("concentrations")
        box1 = SurroundingRectangle(num, color=GOLD, buff=0.1, stroke_width=3)
        self.play(Create(box1), Write(ut), run_time=0.7)
        self.at("one below")
        box2 = SurroundingRectangle(den, color=GOLD, buff=0.1, stroke_width=3)
        self.play(ReplacementTransform(box1, box2), Create(ubar), Write(ub), run_time=0.6)
        self.at("leave one")
        c1 = Line(ut[2].get_corner(DL), ut[2].get_corner(UR), color=RED, stroke_width=7)
        c2 = Line(ub.get_corner(DL), ub.get_corner(UR), color=RED, stroke_width=7)
        self.play(Create(c1), Create(c2), FadeOut(box2), run_time=0.5)
        self.play(FadeIn(eqs[1]), FadeIn(eqs[2], scale=1.3), run_time=0.5)
        self.at("units of")
        lab = T("units of concentration", 48, GOLD).move_to(DOWN * 2.75)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s06
class S06Half(SpokenScene):
    def construct(self):
        recs = VGroup(*[Rec(1.55, 1.4) for _ in range(10)]).arrange_in_grid(2, 5, buff=(0.45, 0.5)).move_to(RIGHT * 0.8 + UP * 0.85)
        self.play(FadeIn(recs), run_time=0.5)
        self.at("ligand level")
        bound_ix = [0, 2, 4, 6, 8]
        starts = [[-5.8, 3.3, 0], [-5.8, 1.8, 0], [-5.8, 0.3, 0], [-5.8, -1.2, 0], [6.3, -1.2, 0]]
        ligs = [lig(0.24).move_to(p) for p in starts]
        self.play(*[FadeIn(l, scale=0.5) for l in ligs], run_time=0.5)
        self.at("half")
        self.play(*[l.animate.move_to(recs[i].sock_pos()) for i, l in zip(bound_ix, ligs)],
                  *[recs[i].lit_anim(True) for i in bound_ix], run_time=1.0)
        self.at("free and")
        # sort: bound receptors to the top row, free ones to the bottom row
        free_ix = [1, 3, 5, 7, 9]
        top_slots = [recs[j].get_center() for j in range(5)]
        bot_slots = [recs[j].get_center() for j in range(5, 10)]
        anims = []
        for k, (i, l) in enumerate(zip(bound_ix, ligs)):
            anims.append(VGroup(recs[i], l).animate.move_to(top_slots[k]))
        for k, i in enumerate(free_ix):
            anims.append(recs[i].animate.move_to(bot_slots[k]))
        self.play(*anims, run_time=0.45)
        rb = M("[R]", 52, BLUE).move_to([-5.6, bot_slots[0][1], 0])
        self.play(FadeIn(rb, shift=RIGHT * 0.1), run_time=0.25)
        self.at("bound receptor")
        rlb = M("[RL]", 52, TEXT).move_to([-5.6, top_slots[0][1], 0])
        self.play(FadeIn(rlb, shift=RIGHT * 0.1), run_time=0.4)
        self.at("equal")
        big = VGroup(M("[R]", 64, BLUE), M("=", 64, GOLD), M("[RL]", 64, TEXT)).arrange(RIGHT, buff=0.35).move_to(DOWN * 2.85)
        self.play(FadeIn(big, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- s07
class S07Cancel(SpokenScene):
    def construct(self):
        top = VGroup(M("[R]", 50, BLUE), M("=", 50, GOLD), M("[RL]", 50, TEXT)).arrange(RIGHT, buff=0.3).move_to(UP * 3.15)
        eq, num, den, frac = kd_eq(66)
        eq.move_to(UP * 1.25)
        self.add(top)
        self.play(FadeIn(eq), run_time=0.4)
        self.at("cancel")
        c1 = Line(num[0].get_corner(DL), num[0].get_corner(UR), color=RED, stroke_width=7)
        c2 = Line(den.get_corner(DL), den.get_corner(UR), color=RED, stroke_width=7)
        self.play(Create(c1), Create(c2), Indicate(top, color=GOLD, scale_factor=1.06), run_time=0.7)
        self.at("so kd")
        res = VGroup(M("Kd =", 88, GOLD), M("[L]", 88, YELLOW)).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.75)
        self.play(TransformFromCopy(eq[0], res[0]), TransformFromCopy(num[1], res[1]), run_time=0.6)
        self.at("free ligand")
        fl = T("free ligand", 38, YELLOW)
        ho = T("at half occupancy", 38, YELLOW)
        cap = VGroup(fl, ho).arrange(RIGHT, buff=0.22).move_to(DOWN * 1.95)
        self.play(FadeIn(fl), run_time=0.4)
        self.at("half")
        self.play(FadeIn(ho), run_time=0.35)
        L = M("L", 60, YELLOW)
        sub = M("½", 48, YELLOW).next_to(L, RIGHT, buff=0.04).align_to(L, DOWN).shift(DOWN * 0.16)
        short = VGroup(T("written", 34, GREY), M("Kd =", 60, GOLD), VGroup(L, sub)).arrange(RIGHT, buff=0.3)
        short[2].shift(DOWN * 0.02)
        short.move_to(DOWN * 3.05)
        self.play(FadeIn(short, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- s08
class S08Flip(SpokenScene):
    def construct(self):
        N = 44
        w = 11.0 / N
        bar = VGroup(*[Rectangle(width=w, height=0.5, stroke_width=0, fill_opacity=1,
                                 fill_color=interpolate_color(ManimColor(GREEN), ManimColor(GREY), i / (N - 1)))
                       for i in range(N)]).arrange(RIGHT, buff=0).move_to(DOWN * 1.6)
        ticks = VGroup()
        for x, lab in [(-5.5, "1 nM"), (0.0, "1 µM"), (5.5, "1 mM")]:
            ticks.add(Line([x, -1.85, 0], [x, -2.0, 0], color=GREY, stroke_width=3),
                      M(lab, 28, GREY).move_to([x, -2.3, 0]))
        ticks[1].shift(RIGHT * 0.02)
        ticks[2].shift(RIGHT * 0.25)
        ticks[-1].shift(LEFT * 0.25)
        ticks[-2].shift(LEFT * 0.02)
        sm = M("small Kd", 32, GOLD).move_to([-4.6, -2.95, 0])
        lg = M("large Kd", 32, GOLD).move_to([4.6, -2.95, 0])
        lgp = VGroup(*[Rec(1.2, 1.05) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.3).move_to([-4.3, 1.6, 0])
        con1 = DashedLine(lgp.get_bottom() + DOWN * 0.1, [-5.3, -1.3, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(bar), FadeIn(ticks), FadeIn(sm), FadeIn(lg), FadeIn(lgp), Create(con1), run_time=0.6)
        self.at("backwards")
        arr = Arrow(RIGHT * 3.0 + DOWN * 0.8, LEFT * 3.0 + DOWN * 0.8, color=GREEN, buff=0, stroke_width=8)
        al = T("tighter binding", 34, GREEN).next_to(arr, UP, buff=0.15)
        self.play(GrowArrow(arr), FadeIn(al), run_time=0.8)
        self.at("small")
        self.play(Indicate(sm, color=GOLD, scale_factor=1.15), run_time=0.6)
        self.at("tight binding")
        self.at("little ligand")
        l1 = lig(0.17).move_to(lgp[0].sock_pos() + UP * 1.4)
        l2 = lig(0.17).move_to(lgp[3].sock_pos() + UP * 2.6)
        lt = T("little ligand", 32, TEXT).move_to([-4.3, 3.6, 0])
        self.add(l1, l2)
        self.play(l1.animate.move_to(lgp[0].sock_pos()), l2.animate.move_to(lgp[3].sock_pos()),
                  lgp[0].lit_anim(True), lgp[3].lit_anim(True), FadeIn(lt), run_time=0.6)
        self.at("half the sites")
        rgp = VGroup(*[Rec(1.2, 1.05) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.3).move_to([4.3, 1.6, 0])
        rgp[1].blk.set_fill(BLUE, 0.5)
        rgp[2].blk.set_fill(BLUE, 0.5)
        bl = [lig(0.17).move_to(rgp[i].sock_pos()) for i in (1, 2)]
        fl = [lig(0.17).move_to(p) for p in ([2.4, 2.6, 0], [2.4, 1.5, 0], [2.4, 0.4, 0], [6.2, 2.6, 0], [6.2, 1.5, 0],
                                             [6.2, 0.4, 0], [3.5, 0.0, 0], [5.0, 3.0, 0], [3.6, 3.0, 0])]
        rt = T("lots of ligand", 32, TEXT).move_to([4.3, 3.6, 0])
        con2 = DashedLine(rgp.get_bottom() + DOWN * 0.1, [5.3, -1.3, 0], color=GREY, stroke_width=3)
        both = T("both half full", 32, YELLOW).move_to([0, 1.6, 0])
        self.play(FadeIn(rgp), *[FadeIn(x) for x in bl + fl], FadeIn(rt), Create(con2), FadeIn(both), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- s09
class S09Error(SpokenScene):
    def panel(self, x, title, col, sym):
        box = RoundedRectangle(corner_radius=0.25, width=6.0, height=5.8, stroke_color=GREY, stroke_width=2.5,
                               fill_color=GREY, fill_opacity=0.06).move_to(RIGHT * x + UP * 0.15)
        ttl = M(title, 56, col).move_to(box.get_top() + DOWN * 0.6)
        lx = x - 1.5
        scale = Line([lx, -1.05, 0], [lx, 1.15, 0], color=GREY, stroke_width=5)
        hi = T("high " + sym, 30, TEXT).next_to(scale.get_end(), RIGHT, buff=0.25)
        lo = T("low " + sym, 30, TEXT).next_to(scale.get_start(), RIGHT, buff=0.25)
        return box, ttl, VGroup(scale, hi, lo)

    def construct(self):
        b1, t1, sc1 = self.panel(-3.35, "Kd", GOLD, "Kd")
        b2, t2, sc2 = self.panel(3.35, "Ka = 1/Kd", TEAL, "Ka")
        a1 = Arrow(sc1[0].get_end() + LEFT * 0.55, sc1[0].get_start() + LEFT * 0.55, color=GREEN, buff=0, stroke_width=8)
        tx1 = T("lower = tighter", 32, GREEN).move_to([-2.35, 0.05, 0])
        ghost = t2.copy().set_opacity(0.3)
        self.play(FadeIn(VGroup(b1, t1, sc1, a1, tx1)), FadeIn(b2), FadeIn(ghost), FadeIn(sc2), run_time=0.5)
        self.at("flipping")
        wrong = T("Kd high = tighter?", 34, RED).move_to([-3.35, -1.85, 0])
        self.play(FadeIn(wrong), run_time=0.35)
        x = Line(wrong.get_left() + LEFT * 0.1, wrong.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        self.play(Create(x), run_time=0.4)
        self.at("reciprocal")
        self.play(FadeIn(t2), FadeOut(ghost), run_time=0.4)
        self.at("association constant")
        nm = T("association constant", 30, TEAL).next_to(t2, DOWN, buff=0.15)
        self.play(FadeIn(nm), run_time=0.4)
        self.at("other way")
        a2 = Arrow(sc2[0].get_start() + LEFT * 0.55, sc2[0].get_end() + LEFT * 0.55, color=GREEN, buff=0, stroke_width=8)
        tx2 = T("higher = tighter", 32, GREEN).move_to([4.35, 0.05, 0])
        self.play(GrowArrow(a2), FadeIn(tx2), run_time=0.6)
        self.at("for kd")
        ban = RoundedRectangle(corner_radius=0.2, width=10.5, height=0.9, stroke_color=GOLD, stroke_width=3,
                               fill_color=GOLD, fill_opacity=0.14).move_to(DOWN * 3.4)
        bt = T("For Kd, lower is tighter", 42, GOLD).move_to(ban)
        self.play(FadeOut(VGroup(wrong, x)), FadeIn(ban), FadeIn(bt), Indicate(tx1, color=GREEN), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- s10 / s12
def gen_xticks(numbers=False):
    if numbers:
        return VGroup(*[GEN.xtick(x, str(int(x))) for x in (0, 2, 4, 6, 8, 10)])
    return VGroup(GEN.xtick(0, "0"))


def kd_tick(lab="Kd", color=GOLD):
    return GEN.xtick(KD, lab, color)


EQ_C = np.array([2.7, -0.35, 0])


class S10Curve(SpokenScene):
    def construct(self):
        lines, yt, ytl = gen_base()
        xtl = GEN.xtitle("free ligand [L]  (M)", 10)
        x0t = gen_xticks()
        self.play(Create(lines), run_time=0.4)
        self.at("fraction bound")
        self.play(FadeIn(ytl), FadeIn(yt), run_time=0.4)
        self.at("free ligand")
        self.play(FadeIn(xtl), FadeIn(x0t), run_time=0.4)
        self.at("you get")
        xv = ValueTracker(0.0)
        cv = always_redraw(lambda: gen_curve(max(xv.get_value(), 0.01)))
        tip = always_redraw(lambda: Dot(GEN.c2p(xv.get_value(), y1(xv.get_value())), color=TEXT, radius=0.09).set_z_index(5))
        self.add(cv, tip)
        self.play(xv.animate.set_value(KD), run_time=0.75, rate_func=linear)
        mk = gen_kd_marker()
        kt = kd_tick()
        self.play(FadeIn(mk), FadeIn(kt), run_time=0.3)
        eqn = M("Y = L / (Kd + L)", 38, TEXT).move_to(EQ_C)
        cav = T("one site, no cooperativity", 30, GREY).next_to(eqn, DOWN, buff=0.3)
        self.play(xv.animate.set_value(10), FadeIn(eqn), FadeIn(cav), run_time=1.0, rate_func=linear)
        self.remove(cv, tip)
        curve = gen_curve()
        self.add(curve)
        self.at("rises")
        seg1 = gen_curve(1.0, YELLOW, 10)
        self.play(Create(seg1), run_time=0.6)
        self.at("bends")
        seg2 = gen_curve(4.0, YELLOW, 10, 1.0)
        self.play(FadeOut(seg1), Create(seg2), run_time=0.6)
        self.at("creeps")
        seg3 = gen_curve(10.0, YELLOW, 10, 4.0)
        self.play(FadeOut(seg2), Create(seg3), run_time=0.45)
        self.at("full")
        full = DashedLine(GEN.c2p(0, 1), GEN.c2p(10, 1), color=GREY, stroke_width=2.5)
        self.play(Create(full), FadeOut(seg3), run_time=0.4)
        self.finish()


class S11Gas(SpokenScene):
    def gauge(self, p):
        c = np.array([0, 1.55, 0])
        R = 0.95
        ang = lambda v: np.deg2rad(210 - 240 * v / 100)
        arc = Arc(radius=R, start_angle=np.deg2rad(-30), angle=np.deg2rad(240), color=GREY, stroke_width=5).move_arc_center_to(c)
        tks = VGroup(*[Line(c + (R - 0.15) * np.array([np.cos(ang(v)), np.sin(ang(v)), 0]),
                            c + R * np.array([np.cos(ang(v)), np.sin(ang(v)), 0]), color=GREY, stroke_width=3)
                       for v in (0, 20, 40, 60, 80, 100)])
        needle = Line(c, c + (R - 0.12) * np.array([np.cos(ang(p)), np.sin(ang(p)), 0]), color=GOLD, stroke_width=6)
        hub = Dot(c, color=GOLD, radius=0.08)
        read = T(f"pO₂ = {int(round(p))} torr", 32, GOLD).move_to(c + DOWN * 1.2)
        return VGroup(arc, tks, needle, hub, read)

    def construct(self):
        rng = np.random.RandomState(4)
        gbox = RoundedRectangle(corner_radius=0.2, width=4.1, height=4.9, stroke_color=GREY, stroke_width=3).move_to(LEFT * 4.35 + UP * 0.25)
        dbox = RoundedRectangle(corner_radius=0.2, width=4.1, height=4.9, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.08).move_to(RIGHT * 4.35 + UP * 0.25)

        def dots(box, n):
            cells = [(i, j) for i in range(3) for j in range(4)]
            rng.shuffle(cells)
            pts = [[-1.25 + 1.25 * i + rng.uniform(-0.3, 0.3), -1.7 + 1.13 * j + rng.uniform(-0.25, 0.25), 0] for i, j in cells[:n]]
            return [lig(0.2).move_to(box.get_center() + np.array(p)) for p in pts]

        g_all = dots(gbox, 12)
        d_all = dots(dbox, 8)
        g_lab = T("oxygen gas", 32, TEXT).next_to(gbox, DOWN, buff=0.25)
        d_lab = T("dissolved O₂", 32, BLUE).next_to(dbox, DOWN, buff=0.25)
        pv = ValueTracker(20)
        gg = always_redraw(lambda: self.gauge(pv.get_value()))
        self.play(FadeIn(gbox), FadeIn(dbox), FadeIn(g_lab), FadeIn(d_lab), *[FadeIn(d) for d in g_all[:3]],
                  *[FadeIn(d) for d in d_all[:2]], FadeIn(gg), run_time=0.25)
        self.at("pressure")
        self.play(Indicate(gg[4], color=GOLD, scale_factor=1.1), run_time=0.6)
        self.at("dissolved concentration")
        self.play(Indicate(d_lab, color=BLUE, scale_factor=1.1), run_time=0.6)
        self.at("proportional")
        link = DoubleArrow(LEFT * 2.0 + DOWN * 0.75, RIGHT * 2.0 + DOWN * 0.75, color=GOLD, buff=0, stroke_width=6)
        prop = T("[O₂] ∝ pO₂", 36, GOLD).move_to(DOWN * 1.6)
        self.play(GrowArrow(link), FadeIn(prop), pv.animate.set_value(40), *[FadeIn(d) for d in g_all[3:6]],
                  *[FadeIn(d) for d in d_all[2:4]], run_time=0.7)
        self.at("partial")
        self.play(pv.animate.set_value(80), *[FadeIn(d) for d in g_all[6:]], *[FadeIn(d) for d in d_all[4:]], run_time=0.6)
        self.finish()


def s10_final(scene):
    lines, yt, ytl = gen_base()
    xtl = GEN.xtitle("free ligand [L]  (M)", 10)
    x0t = gen_xticks()
    curve = gen_curve()
    mk = gen_kd_marker()
    kt = kd_tick()
    full = DashedLine(GEN.c2p(0, 1), GEN.c2p(10, 1), color=GREY, stroke_width=2.5)
    eqn = M("Y = L / (Kd + L)", 38, TEXT).move_to(EQ_C)
    cav = T("one site, no cooperativity", 30, GREY).next_to(eqn, DOWN, buff=0.3)
    scene.add(lines, yt, ytl, xtl, x0t, curve, mk, kt, full, eqn, cav)
    return dict(lines=lines, yt=yt, ytl=ytl, xtl=xtl, x0t=x0t, curve=curve, mk=mk, kt=kt, full=full, eqn=eqn, cav=cav)


class S12P50(SpokenScene):
    def construct(self):
        s = s10_final(self)
        self.at("single site")
        self.play(Indicate(s["cav"], color=BLUE, scale_factor=1.08), FadeOut(s["eqn"]), run_time=0.6)
        self.at("p50")
        p50 = M("P50", 30, GOLD).next_to(GEN.c2p(KD, 0.25), RIGHT, buff=0.2)
        self.play(FadeIn(p50, shift=LEFT * 0.1), run_time=0.4)
        self.at("pressure")
        newx = GEN.xtitle("pO₂  (torr)", 10)
        self.play(FadeOut(s["xtl"]), FadeIn(newx), run_time=0.5)
        self.at("half")
        self.play(Indicate(s["mk"][1], color=YELLOW, scale_factor=1.0), Indicate(s["yt"][1], color=YELLOW), run_time=0.6)
        self.at("kd measured")
        res = M("P50 = Kd", 44, GOLD).move_to(EQ_C)
        self.play(FadeIn(res), run_time=0.4)
        self.at("torr")
        intorr = T("(in torr)", 34, GOLD).next_to(res, RIGHT, buff=0.25)
        nums = gen_xticks(True)
        self.play(FadeIn(intorr), FadeOut(s["kt"]), FadeOut(s["x0t"]), FadeIn(nums), run_time=0.5)
        self.finish()


def s12_final(scene):
    lines, yt, ytl = gen_base()
    newx = GEN.xtitle("pO₂  (torr)", 10)
    nums = gen_xticks(True)
    curve = gen_curve()
    mk = gen_kd_marker()
    full = DashedLine(GEN.c2p(0, 1), GEN.c2p(10, 1), color=GREY, stroke_width=2.5)
    res = M("P50 = Kd", 44, GOLD).move_to(EQ_C)
    intorr = T("(in torr)", 34, GOLD).next_to(res, RIGHT, buff=0.25)
    cav = T("one site, no cooperativity", 30, GREY).next_to(M("Y = L / (Kd + L)", 38).move_to(EQ_C), DOWN, buff=0.3)
    p50 = M("P50", 30, GOLD).next_to(GEN.c2p(KD, 0.25), RIGHT, buff=0.2)
    rest = VGroup(lines, yt, ytl, newx, nums, mk, full, res, intorr, cav, p50)
    scene.add(rest, curve)
    return rest, curve


# ---------------------------------------------------------------- s13
MBX = -5.0


def myoglobin_cartoon():
    blob = Ellipse(width=2.7, height=3.7, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.14)
    blob.move_to([MBX, 0.75, 0])
    ts = np.linspace(0, 1, 200)
    pts = [[MBX + 0.75 * np.sin(5.2 * np.pi * t) * (1 - 0.25 * abs(t - 0.5)), 2.15 - 2.8 * t, 0] for t in ts]
    chain = VMobject(stroke_color=BLUE, stroke_width=5).set_points_smoothly(pts)
    heme = RoundedRectangle(corner_radius=0.1, width=0.75, height=0.75, stroke_color=GOLD, stroke_width=3,
                            fill_color=GOLD, fill_opacity=0.55).move_to([MBX + 0.35, 0.6, 0]).set_z_index(2)
    o2 = lig(0.17).move_to(heme.get_center()).set_z_index(3)
    ttl = T("myoglobin", 36, BLUE).next_to(blob, UP, buff=0.2)
    labs = VGroup(*[T(s, 30, TEXT) for s in ("one chain", "one heme", "one site")]).arrange(DOWN, buff=0.18)
    labs.next_to(blob, DOWN, buff=0.3)
    return blob, chain, heme, o2, ttl, labs


class S13Mb(SpokenScene):
    def construct(self):
        rest, curve12 = s12_final(self)
        ax = mb_axes()
        blob, chain, heme, o2, ttl, labs = myoglobin_cartoon()
        curve = mb_curve(p1=10)
        self.play(FadeOut(rest), FadeIn(ax), ReplacementTransform(curve12, curve), FadeIn(blob), FadeIn(ttl), run_time=0.8)
        self.at("one chain")
        self.play(Create(chain), FadeIn(labs[0]), run_time=0.6)
        self.at("one heme")
        self.play(FadeIn(heme, scale=0.6), FadeIn(labs[1]), run_time=0.4)
        self.at("one site")
        self.play(FadeIn(o2, scale=0.5), FadeIn(labs[2]), run_time=0.4)
        self.at("its p50")
        self.play(FadeIn(mb_p50_marker()), Indicate(curve, color=BLUE, scale_factor=1.0), run_time=0.6)
        self.at("about two")
        self.play(FadeIn(mb_p50_label()), Indicate(ax[4][0][1], color=GOLD, scale_factor=1.3), run_time=0.5)
        self.finish()


class MbBase(SpokenScene):
    """Rebuild the myoglobin chart where s13 left it (curve drawn to 10 torr unless full=True)."""

    def base(self, full=False):
        self.ax = mb_axes()
        self.curve = mb_curve(p1=100 if full else 10)
        self.mk = VGroup(mb_p50_marker(), mb_p50_label())
        self.add(self.ax, self.curve, self.mk)


def pt(p, y=None, color=YELLOW):
    return Dot(MBF.c2p(p, mb_y(p) if y is None else y), color=color, radius=0.12).set_z_index(5)


def q_marker():
    c = Circle(radius=0.32, color=GOLD, stroke_width=4, fill_color=BG, fill_opacity=1)
    q = M("?", 36, GOLD)
    return VGroup(c, q).move_to(MBF.c2p(20, 0.68)).set_z_index(5)


def pred_parts():
    l100 = DashedLine(MBF.c2p(100, 0), MBF.c2p(100, mb_y(100)), color=YELLOW, stroke_width=3)
    d100 = pt(100)
    s100 = place(stmt("100 torr, lungs", "98% full", YELLOW), S100_POS)
    l20 = DashedLine(MBF.c2p(20, 0), MBF.c2p(20, 1.0), color=GOLD, stroke_width=3)
    qm = q_marker()
    s20 = place(stmt("20 torr, muscle", "?", GOLD), S20_POS)
    pred = T("Predict", 40, GOLD).move_to([-4.8, 3.1, 0])
    return l100, d100, s100, l20, qm, s20, pred


# ---------------------------------------------------------------- s14
class S14Predict(MbBase):
    def construct(self):
        self.base()
        blob, chain, heme, o2, ttl, labs = myoglobin_cartoon()
        self.add(blob, chain, heme, o2, ttl, labs)
        l100, d100, s100, l20, qm, s20, pred = pred_parts()
        self.play(FadeOut(VGroup(blob, chain, heme, o2, ttl, labs)), FadeIn(pred, shift=DOWN * 0.1), run_time=0.5)
        self.at("98")
        self.play(Create(l100), FadeIn(d100, scale=0.5), FadeIn(s100), run_time=0.7)
        self.at("how full")
        self.play(Create(l20), FadeIn(qm, scale=0.6), FadeIn(s20), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- s15
class S15Pause(MbBase):
    def construct(self):
        self.base()
        l100, d100, s100, l20, qm, s20, pred = pred_parts()
        self.add(l100, d100, s100, l20, qm, s20, pred)
        c = np.array([-5.75, -2.55, 0])
        bg = Circle(radius=0.45, color=GREY, stroke_width=3, stroke_opacity=0.4).move_to(c)
        tv = ValueTracker(1.0)
        ring = always_redraw(lambda: Arc(radius=0.45, start_angle=PI / 2, angle=TAU * max(tv.get_value(), 0.001),
                                         color=GOLD, stroke_width=6).move_arc_center_to(c))
        think = T("think first", 34, GOLD).next_to(bg, RIGHT, buff=0.3)
        self.play(FadeIn(bg), FadeIn(ring), FadeIn(think), run_time=0.3)
        self.play(tv.animate.set_value(0.0), run_time=4.4, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- s16
class S16Reveal(MbBase):
    def construct(self):
        self.base()
        l100, d100, s100, l20, qm, s20, pred = pred_parts()
        self.add(l100, d100, s100, l20, qm, s20, pred)
        self.play(FadeOut(pred), run_time=0.3)
        self.at("91")
        rest = mb_curve(p0=10, p1=100)
        self.play(Create(rest), FadeOut(qm), FadeOut(s20[1]), run_time=0.4, rate_func=linear)
        d20 = pt(20)
        l20b = DashedLine(MBF.c2p(20, 0), MBF.c2p(20, mb_y(20)), color=GOLD, stroke_width=3)
        h20 = DashedLine(MBF.c2p(0, mb_y(20)), MBF.c2p(20, mb_y(20)), color=YELLOW, stroke_width=3)
        new = place(stmt("20 torr, muscle", "91% full", YELLOW), S20_POS)
        self.play(FadeIn(d20, scale=0.4), ReplacementTransform(l20, l20b), Create(h20), FadeIn(new[1]), run_time=0.6)
        self.at("far above")
        arr = DoubleArrow(MBF.c2p(MB_P50, 0.12), MBF.c2p(20, 0.12), color=GOLD, buff=0, stroke_width=4,
                          max_tip_length_to_length_ratio=0.08, tip_length=0.2)
        far = T("far above P50", 30, GOLD).next_to(MBF.c2p(20, 0.12), RIGHT, buff=0.25)
        self.play(GrowArrow(arr), FadeIn(far), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- s17
SPONGE_C = np.array([-4.85, -0.45, 0])
PORES = [(-1.05, 0.85, 0.22), (-0.1, 0.95, 0.2), (0.95, 0.8, 0.23), (-0.6, 0.3, 0.18), (0.45, 0.25, 0.22),
         (1.15, -0.1, 0.17), (-1.15, -0.25, 0.21), (-0.2, -0.35, 0.2), (0.75, -0.75, 0.21), (-0.75, -0.95, 0.2),
         (0.25, -1.05, 0.17), (1.2, -1.05, 0.15)]
EMPTY_ORDER = [5, 0, 9, 3, 11, 7, 1, 10, 4, 8, 2, 6]


def sponge_body():
    pts = []
    for k in range(48):
        a = TAU * k / 48
        rr = 1.0 + 0.05 * np.sin(5 * a) + 0.035 * np.cos(9 * a)
        pts.append(SPONGE_C + np.array([1.65 * rr * np.cos(a), 1.45 * rr * np.sin(a), 0]))
    body = VMobject(stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).set_points_smoothly(pts + [pts[0]])
    holes = VGroup(*[Circle(radius=r, stroke_color=BLUE, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(
        SPONGE_C + np.array([x, y, 0])) for x, y, r in PORES])
    return body, holes


def sponge_o2(p):
    n = int(round(12 * mb_y(p)))
    gone = set(EMPTY_ORDER[:12 - n])
    return VGroup(*[lig(0.12).move_to(SPONGE_C + np.array([x, y, 0])).set_opacity(0 if i in gone else 1)
                    for i, (x, y, r) in enumerate(PORES)])


class S17Seven(MbBase):
    def construct(self):
        self.base(full=True)
        l100 = DashedLine(MBF.c2p(100, 0), MBF.c2p(100, mb_y(100)), color=YELLOW, stroke_width=3)
        l20 = DashedLine(MBF.c2p(20, 0), MBF.c2p(20, mb_y(20)), color=GOLD, stroke_width=3)
        h20 = DashedLine(MBF.c2p(0, mb_y(20)), MBF.c2p(20, mb_y(20)), color=YELLOW, stroke_width=3)
        d100, d20 = pt(100), pt(20)
        s100 = place(stmt("100 torr, lungs", "98% full", YELLOW), S100_POS)
        s20 = place(stmt("20 torr, muscle", "91% full", YELLOW), S20_POS)
        arr = DoubleArrow(MBF.c2p(MB_P50, 0.12), MBF.c2p(20, 0.12), color=GOLD, buff=0, stroke_width=4,
                          max_tip_length_to_length_ratio=0.08, tip_length=0.2)
        far = T("far above P50", 30, GOLD).next_to(MBF.c2p(20, 0.12), RIGHT, buff=0.25)
        self.add(l100, l20, h20, d100, d20, s100, s20, arr, far)
        self.play(FadeOut(arr), FadeOut(far), run_time=0.3)
        self.at("only about")
        h98 = DashedLine(MBF.c2p(0, mb_y(100)), MBF.c2p(100, mb_y(100)), color=YELLOW, stroke_width=3)
        self.play(Create(h98), run_time=0.5)
        self.at("7")
        da = DoubleArrow(MBF.c2p(15, mb_y(20)), MBF.c2p(15, mb_y(100)), color=TEXT, buff=0, stroke_width=4,
                         max_tip_length_to_length_ratio=0.4, tip_length=0.13)
        dl = T("delivered ≈ 7%", 32, TEXT).move_to(MBF.c2p(15, 1.0) + UP * 0.45)
        lead = Line(dl.get_bottom() + DOWN * 0.04, da.get_top() + UP * 0.03, color=TEXT, stroke_width=2)
        self.play(GrowFromCenter(da), FadeIn(dl), Create(lead), run_time=0.5)
        self.at("sponge")
        c100 = place(M("100 torr: 98%", 28, YELLOW), np.array([-6.6, 3.15, 0]))
        c20 = place(M("20 torr: 91%", 28, YELLOW), np.array([-6.6, 2.6, 0]))
        body, holes = sponge_body()
        pv = ValueTracker(100.0)
        o2s = always_redraw(lambda: sponge_o2(pv.get_value()))
        sp_lab = T("sponge", 34, BLUE).move_to(SPONGE_C + DOWN * 2.0)
        self.play(ReplacementTransform(s100, c100), ReplacementTransform(s20, c20), FadeIn(body), FadeIn(holes),
                  FadeIn(o2s), FadeIn(sp_lab), run_time=0.5)
        self.at("grips")
        mark = always_redraw(lambda: VGroup(
            DashedLine(MBF.c2p(pv.get_value(), 0), MBF.c2p(pv.get_value(), mb_y(pv.get_value())), color=TEXT, stroke_width=3),
            Dot(MBF.c2p(pv.get_value(), mb_y(pv.get_value())), color=TEXT, radius=0.14).set_z_index(6)))
        self.add(mark)
        self.play(pv.animate.set_value(20), run_time=1.1)
        self.at("only when")
        sc = T("truly scarce", 32, GOLD).move_to(MBF.c2p(7, 0.2), aligned_edge=LEFT).set_z_index(8)
        sca = Arrow(sc.get_left() + LEFT * 0.08, MBF.c2p(1.0, 0.04), color=GOLD, buff=0, stroke_width=4,
                    max_tip_length_to_length_ratio=0.25, tip_length=0.2).set_z_index(8)
        self.play(FadeIn(sc), GrowArrow(sca), run_time=0.4)
        self.play(pv.animate.set_value(1.0), run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
        self.finish()


# ---------------------------------------------------------------- s18
class S18Hb(SpokenScene):
    def construct(self):
        # s17's final chart, without the left column and the s17 call-outs
        left = VGroup(place(M("100 torr: 98%", 28, YELLOW), np.array([-6.6, 3.15, 0])),
                      place(M("20 torr: 91%", 28, YELLOW), np.array([-6.6, 2.6, 0])),
                      *sponge_body(), sponge_o2(1.0), T("sponge", 34, BLUE).move_to(SPONGE_C + DOWN * 2.0))
        callouts = VGroup(mb_p50_label(),
                          DashedLine(MBF.c2p(100, 0), MBF.c2p(100, mb_y(100)), color=YELLOW, stroke_width=3),
                          DashedLine(MBF.c2p(20, 0), MBF.c2p(20, mb_y(20)), color=GOLD, stroke_width=3),
                          DashedLine(MBF.c2p(0, mb_y(20)), MBF.c2p(20, mb_y(20)), color=YELLOW, stroke_width=3),
                          DashedLine(MBF.c2p(0, mb_y(100)), MBF.c2p(100, mb_y(100)), color=YELLOW, stroke_width=3),
                          pt(100), pt(20))
        a = ValueTracker(0.0)

        def chart():
            v = a.get_value()
            fr = mb_frame(v)
            return VGroup(mb_axes(fr, max(0.0, 1 - 2 * v), max(0.0, 2 * v - 1)),
                          fr.curve(mb_y, mb_ps(0, 100), BLUE, 6), mb_p50_marker(fr))
        live = always_redraw(chart)
        self.add(left, callouts, live)
        self.play(FadeOut(left), FadeOut(callouts), a.animate.set_value(1.0), run_time=0.6)
        self.remove(live)
        LF = mb_frame(1.0)
        ax = mb_axes(LF, 0.0, 1.0)
        mbc = LF.curve(mb_y, mb_ps(0, 100), BLUE, 6)
        mmk = mb_p50_marker(LF)
        self.add(ax, mbc, mmk)
        mlab = T("myoglobin", 32, BLUE).move_to(LF.c2p(14, 1.0) + UP * 0.42, aligned_edge=LEFT)
        mlead = Line(mlab.get_left() + DOWN * 0.15, LF.c2p(4, mb_y(4)) + UP * 0.12 + RIGHT * 0.05, color=BLUE, stroke_width=2)
        self.at("curve")
        hbc = LF.curve(hb_y, np.linspace(0, 100, 400), GOLD, 6)
        self.play(Create(hbc), FadeIn(mlab), Create(mlead), run_time=1.4, rate_func=linear)
        hlab = T("hemoglobin", 32, GOLD).move_to(LF.c2p(68, 0.80))
        self.play(FadeIn(hlab), run_time=0.35)
        self.at("an s")
        hb_hi = LF.curve(hb_y, np.linspace(0, 100, 400), GOLD, 12)
        sl = T("S-shaped", 34, GOLD).move_to(LF.c2p(55, 0.22))
        self.play(ShowPassingFlash(hb_hi, time_width=0.6), FadeIn(sl), run_time=0.8)
        self.at("next chapter")
        hv = DashedLine(LF.c2p(26, 0), LF.c2p(26, 0.5), color=GOLD, stroke_width=3)
        hh = DashedLine(LF.c2p(MB_P50, 0.5), LF.c2p(26, 0.5), color=GOLD, stroke_width=3)
        hd = Dot(LF.c2p(26, 0.5), color=GOLD, radius=0.11).set_z_index(5)
        hl = M("P50 ≈ 26", 28, GOLD).move_to(LF.c2p(29, 0.40), aligned_edge=LEFT)
        ml = M("P50 ≈ 2", 26, GOLD).move_to(LF.c2p(3.0, 0.41), aligned_edge=LEFT)
        self.play(Create(hv), Create(hh), FadeIn(hd), FadeIn(hl), FadeIn(ml), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- s19 / s20
def end_lines():
    l1 = T("One site gives a hyperbola;", 46, TEXT, font=TITLE_FONT)
    l2 = T("Kd, or P50, sets where it sits.", 46, TEXT, font=TITLE_FONT)
    g = VGroup(l1, l2).arrange(DOWN, buff=0.35).move_to(UP * 0.35)
    return l1, l2


class S19Take(SpokenScene):
    def construct(self):
        LF = mb_frame(1.0)
        old = VGroup(mb_axes(LF, 0.0, 1.0), LF.curve(mb_y, mb_ps(0, 100), BLUE, 6), mb_p50_marker(LF),
                     LF.curve(hb_y, np.linspace(0, 100, 400), GOLD, 6))
        self.add(old)
        l1, l2 = end_lines()
        self.play(FadeOut(old), run_time=0.4)
        self.at("hyperbola")
        self.play(FadeIn(l1, shift=UP * 0.12), run_time=0.45)
        self.at("and kd")
        self.play(FadeIn(l2, shift=UP * 0.12), run_time=0.45)
        self.finish()


class S20End(EndCard):
    LINE = "One site gives a hyperbola; Kd, or P50, sets where it sits."

    def construct(self):
        l1, l2 = end_lines()
        self.add(l1, l2)
        sub = T("biochemistrypedia.com", size=26, color=TEAL).next_to(VGroup(l1, l2), DOWN, buff=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.finish()
