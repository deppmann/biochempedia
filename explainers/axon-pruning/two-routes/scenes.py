"""Axon pruning, chapter 2: Same Knives, Two Routes (Biochemistrypedia chaptered explainer)

COLOR MAP (one color per concept, whole series; taken from scenes.old.py, TEAL added in this chapter)
  BLUE   = the neuron (cell body and axon)
  YELLOW = NGF (the dots)
  VIOLET = caspases (and their scissors icon)
  ORANGE = Apaf-1 and the apoptosome it builds
  RED    = degeneration, death, and a crossed-out item (not needed / lost)
  GREEN  = survival (cell bodies live, axons protected, neurons resist death)
  TEAL   = inhibitors that keep caspases off (XIAP, the proteasome)
  GREY   = chamber, table lines, labels, structure
  GOLD   = a spotlight on a table row (not a concept), and the "unique to one route" glow
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

VIOLET = "#A98BE0"
ORANGE = "#F29E4C"
INHIB = TEAL


def P(x, y):
    return np.array([x, y, 0.0])


# ----------------------------------------------------------------------------------------------
# small helpers
def scissors(scale=1.0, color=VIOLET, sw=5):
    """Two blades (each a line plus its handle ring) on a pivot dot: g[0], g[1] are the blades, g[2] the pivot."""
    a = VGroup(Line(P(-0.55, 0.3), P(0.95, -0.3), color=color, stroke_width=sw),
               Circle(radius=0.19, color=color, stroke_width=sw).move_to(P(-0.74, 0.32)))
    b = VGroup(Line(P(-0.55, -0.3), P(0.95, 0.3), color=color, stroke_width=sw),
               Circle(radius=0.19, color=color, stroke_width=sw).move_to(P(-0.74, -0.32)))
    pv = Dot(P(0.2, 0.0), radius=0.06, color=color)
    g = VGroup(a, b, pv)
    g.move_to(ORIGIN)
    return g.scale(scale)


def snip(g, n=2, rt=0.13, ang=0.4):
    pv = g[2].get_center()
    seq = []
    for _ in range(n):
        seq.append(AnimationGroup(Rotate(g[0], ang, about_point=pv), Rotate(g[1], -ang, about_point=pv), run_time=rt))
        seq.append(AnimationGroup(Rotate(g[0], -ang, about_point=pv), Rotate(g[1], ang, about_point=pv), run_time=rt))
    return Succession(*seq)


def cross(mob, color=RED, w=6, pad=0.06):
    l, r, t, b = mob.get_left(), mob.get_right(), mob.get_top(), mob.get_bottom()
    return VGroup(Line(P(l[0] - pad, t[1] + pad), P(r[0] + pad, b[1] - pad), color=color, stroke_width=w),
                  Line(P(l[0] - pad, b[1] - pad), P(r[0] + pad, t[1] + pad), color=color, stroke_width=w))


def inhib(start, end, color=INHIB, w=7):
    s, e = np.array(start, dtype=float), np.array(end, dtype=float)
    d = (e - s) / np.linalg.norm(e - s)
    n = np.array([-d[1], d[0], 0.0])
    return VGroup(Line(s, e, color=color, stroke_width=w), Line(e + n * 0.3, e - n * 0.3, color=color, stroke_width=w + 2))


def snap(group):
    return [(m, m.get_fill_opacity(), m.get_stroke_opacity()) for m in group.family_members_with_points()]


def scale_op(sn, f):
    """Animations that set every part to fraction f of its snapshot opacity."""
    return [m.animate.set_fill(opacity=a * f).set_stroke(opacity=b * f) for m, a, b in sn]


def set_op(sn, f):
    for m, a, b in sn:
        m.set_fill(opacity=a * f)
        m.set_stroke(opacity=b * f)


def dim_to(group, f):
    return scale_op(snap(group), f)


def chip_style(c, color, fill=0.16, stroke=1.0):
    return AnimationGroup(c[0].animate.set_stroke(color, opacity=stroke).set_fill(color, fill),
                          c[1].animate.set_color(color).set_opacity(1.0))


def dim_chip(c, f=0.4):
    c[0].set_stroke(opacity=f).set_fill(opacity=0.04)
    c[1].set_opacity(f)
    return c


def qmark(size=80, color=TEXT):
    return T("?", size, color, weight=BOLD)


def lines(txts, size, color=TEXT, buff=0.08, **kw):
    """Several single-line texts stacked and centred on each other (multi-line Text is not centred)."""
    return VGroup(*[T(t, size, color, **kw) for t in txts]).arrange(DOWN, buff=buff)


def idle(scene, items, until=None, scale=1.15, rt=0.8):
    """Keep the picture alive: pulse the given items in turn until the scene's end."""
    until = scene.narration_s if until is None else until
    i = 0
    while scene.elapsed() + rt + 0.1 < until:
        scene.play(Indicate(items[i % len(items)], color=TEXT, scale_factor=scale), run_time=rt)
        i += 1
    rest = until - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


# ----------------------------------------------------------------------------------------------
# the microfluidic chamber (centred on the origin; place(y) moves it)
AX_END = 5.6
GX0, GX1 = -0.9, 0.9


def dot_pts(side, ay, ch, xs):
    ys = [(ch + ay[0]) / 2] + [(ay[i] + ay[i + 1]) / 2 for i in range(len(ay) - 1)] + [(ay[-1] - ch) / 2]
    out = []
    for i, y in enumerate(ys):
        off = 0.0 if i % 2 == 0 else (0.8 if side == "l" else 0.8)
        out += [(x + off, y) for x in xs]
    return out


class Chamber:
    def __init__(self, ch=2.8, ay=(1.6, 0.0, -1.6), br=0.5, bx=-4.6, dot_r=0.2, sw=6, tip_r=0.11, bw=4,
                 xs_l=(-5.7, -4.1, -2.5), xs_r=(1.7, 3.3, 4.9), labels=True):
        self.ch, self.ay = ch, list(ay)

        def comp(x0, x1):
            return RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=2 * ch, stroke_color=GREY,
                                    stroke_width=3, fill_opacity=0).move_to(P((x0 + x1) / 2, 0))
        self.cl, self.cr = comp(-6.2, GX0), comp(GX1, 6.2)
        ys = [ch] + [v for y in ay for v in (y + 0.1, y - 0.1)] + [-ch]
        bar = VGroup()
        for i in range(0, len(ys), 2):
            top, bot = ys[i], ys[i + 1]
            bar.add(Rectangle(width=GX1 - GX0, height=top - bot, stroke_width=0, fill_color=GREY,
                              fill_opacity=0.35).move_to(P(0, (top + bot) / 2)))
        self.bar = bar
        self.bodies = VGroup(*[Circle(radius=br, stroke_color=BLUE, stroke_width=bw, fill_color=BLUE,
                                      fill_opacity=0.35).move_to(P(bx, y)) for y in ay])
        self.ax_in = VGroup(*[Line(P(bx + br, y), P(GX1, y), color=BLUE, stroke_width=sw) for y in ay])
        xs = np.linspace(GX1, AX_END, 9)
        self.ax_out = [[Line(P(xs[i], y), P(xs[i + 1], y), color=BLUE, stroke_width=sw) for i in range(8)] for y in ay]
        self.tips = VGroup(*[Dot(P(AX_END, y), radius=tip_r, color=BLUE) for y in ay])
        self.axons_out = VGroup(*[s for row in self.ax_out for s in row], self.tips)
        self.dl = VGroup(*[Dot(P(*p), radius=dot_r, color=YELLOW) for p in dot_pts("l", ay, ch, xs_l)])
        self.dr = VGroup(*[Dot(P(*p), radius=dot_r, color=YELLOW) for p in dot_pts("r", ay, ch, xs_r)])
        self.lab_l = T("cell bodies", 26, GREY).move_to(P(-3.55, ch + 0.4)) if labels else None
        self.lab_r = T("axons", 26, GREY).move_to(P(3.55, ch + 0.4)) if labels else None

    def parts(self):
        return [self.cl, self.cr, self.bar, self.bodies, self.ax_in, self.axons_out, self.dl, self.dr]

    def place(self, y):
        for g in self.parts() + [m for m in (self.lab_l, self.lab_r) if m is not None]:
            g.shift(UP * y)
        return self

    def core(self, dl=True, dr=True, ax_in=True, axons_out=True, bodies=True):
        g = VGroup(self.cl, self.cr, self.bar)
        if bodies:
            g.add(self.bodies)
        if ax_in:
            g.add(self.ax_in)
        if axons_out:
            g.add(self.axons_out)
        if dl:
            g.add(self.dl)
        if dr:
            g.add(self.dr)
        return g

    def everything(self):
        return VGroup(*self.parts())


def legend(x=-5.6, y=-3.3):
    return VGroup(Dot(P(x, y), radius=0.15, color=YELLOW), T("NGF", 26, YELLOW).move_to(P(x + 0.65, y)))


def drain(group, rt=1.0, up=0.35):
    return LaggedStart(*[d.animate.shift(UP * up).set_opacity(0) for d in group], lag_ratio=0.12, run_time=rt)


def fragment(scene, rows, extra=(), rt=1.6, amp=0.14, seed=4):
    """Axon pieces break into beads (short red dashes with gaps), hold, then clear."""
    rng = random.Random(seed)
    segs = [s for row in rows for s in row]
    scene.play(*[s.animate.set_color(RED).shift(P(rng.uniform(-0.04, 0.04), rng.uniform(-amp, amp))).scale(0.42)
                 for s in segs], *[e.animate.set_color(RED) for e in extra], run_time=rt * 0.5)
    scene.wait(rt * 0.2)
    scene.play(*[FadeOut(s) for s in segs], *[FadeOut(e) for e in extra], run_time=rt * 0.3)


# ----------------------------------------------------------------------------------------------
# the stacked pair of full-width chambers (local on top, global below), scenes 6 to 10
ROWY = [1.85, -1.8]
HDRY = [3.5, 0.02]
LEGP = (-6.2, -3.5)


class Stack:
    def __init__(self):
        self.C = []
        for y in ROWY:
            C = Chamber(ch=1.3, ay=(0.8, 0.0, -0.8), br=0.3, bx=-5.3, dot_r=0.12, sw=4, tip_r=0.08, bw=3,
                        xs_l=(-4.3, -3.1, -1.9), xs_r=(1.7, 3.3, 4.9), labels=False).place(y)
            self.C.append(C)
        self.lab = [T("local deprivation", 30).move_to(P(0, HDRY[0])),
                    T("global deprivation", 30).move_to(P(0, HDRY[1]))]
        self.leg = legend(*LEGP)
        self.q = [qmark(52).move_to(P(x, HDRY[r])) for r in range(2) for x in (-4.4, 4.4)]
        self.ques = T("In normal neurons, what happens in each experiment?", 26).move_to(P(1.0, -3.5))

    def chip_at(self, row, side, text, color):
        """side 0 = above the cell-body compartment, side 1 = above the axon compartment."""
        return chip(text, color, size=26, pad=0.16).move_to(P(-4.4 if side == 0 else 4.4, HDRY[row]))

    def add_neutral(self, scene, row1=True, row2=True):
        C1, C2 = self.C
        if row1:
            scene.add(C1.core(dr=False), self.lab[0])
        if row2:
            scene.add(C2.core(dl=False, dr=False), self.lab[1])
        scene.add(self.leg)


def pr_label():
    return T("pruning, in a dish", 30, TEXT, weight=BOLD).move_to(P(0, HDRY[0]))


def dc_label():
    return lines(["developmental cell death", "in a dish"], 26, TEXT, buff=0.04).set_color(TEXT).move_to(P(0, HDRY[1]))


# ----------------------------------------------------------------------------------------------
# the results table (scenes 11 to 23); rows share edges so highlights line up
RHX, C1X, C2X = -5.0, -1.1, 3.7
RW, CW = 3.0, 4.8
HY = 2.65
RY = [1.2, -0.25, -1.7]
RH = 1.45
TL, TR = RHX - RW / 2, C2X + CW / 2

CELLS = {
    (0, 0): [("axons degenerate", RED), ("cell bodies live", GREEN)],
    (0, 1): [("neurons die", RED), ("axons go with them", RED)],
    (1, 0): [("axons protected", GREEN)],
    (1, 1): [("neurons die", RED), ("axons degenerate", RED)],
    (2, 0): [("axons degenerate", RED), ("cell bodies live", GREEN)],
    (2, 1): [("neurons resist death", GREEN)],
}


class Tbl:
    def __init__(self):
        h1 = lines(["NGF removed from", "axons only"], 26, t2c={"NGF": YELLOW}).move_to(P(C1X, HY))
        h2 = lines(["NGF removed", "everywhere"], 26, t2c={"NGF": YELLOW}).move_to(P(C2X, HY))
        self.heads = VGroup(h1, h2)
        names = [(["normal"], TEXT), (["lacking", "caspase-6"], VIOLET), (["lacking", "Apaf-1"], ORANGE)]
        self.rh = [lines(n, 28, c, buff=0.06).move_to(P(RHX, y)) for (n, c), y in zip(names, RY)]
        self.rect = [[Rectangle(width=CW, height=RH, stroke_color=GREY, stroke_width=2.5,
                                fill_opacity=0).move_to(P(x, y)) for x in (C1X, C2X)] for y in RY]
        self.rrect = [Rectangle(width=RW, height=RH, stroke_color=GREY, stroke_width=2.5,
                                fill_opacity=0).move_to(P(RHX, y)) for y in RY]
        self.fill = {}
        for (r, c), ls in CELLS.items():
            g = VGroup(*[T(t, 26, col) for t, col in ls]).arrange(DOWN, buff=0.12)
            g.move_to(self.rect[r][c].get_center())
            self.fill[(r, c)] = g
        self.qm = {(r, c): T("?", 54, TEXT, weight=BOLD).move_to(self.rect[r][c].get_center())
                   for r in range(3) for c in range(2)}

    def set_dim(self, r, f):
        for m in (self.rect[r][0], self.rect[r][1], self.rrect[r]):
            m.set_stroke(opacity=f)
        self.rh[r].set_opacity(f)

    def grid(self, rows=(0, 1, 2)):
        return VGroup(*[self.rect[r][c] for r in rows for c in (0, 1)], *[self.rrect[r] for r in rows])

    def hl(self, row, color=GOLD):
        return Rectangle(width=TR - TL, height=RH, stroke_color=color, stroke_width=6,
                         fill_opacity=0).move_to(P((TR + TL) / 2, RY[row]))

    def base(self, scene, filled=(), q=(), dim=()):
        scene.add(self.heads, self.grid(), *self.rh)
        for k in filled:
            scene.add(self.fill[k])
        for k in q:
            scene.add(self.qm[k])
        for r in dim:
            self.set_dim(r, 0.3)

    def swap(self, scene, key, rt=0.7):
        """Fade the ? out first, then the answer in (never both at once)."""
        scene.play(FadeOut(self.qm[key]), run_time=0.25)
        scene.play(FadeIn(self.fill[key], shift=UP * 0.1), run_time=rt - 0.25)


def question_line(text):
    return T(text, 26).move_to(P(0, -3.2))


# ==============================================================================================
class S00Title(TitleCard):
    LESSON = "Pruning Without Dying: Axons That Cut Themselves Back"
    TITLE = "Same Knives, Two Routes"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = fit(T(self.TITLE, size=54, font=TITLE_FONT), max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        sub = T("the knives are caspases", 28, VIOLET)
        g = VGroup(brand, lesson, title, rule, sub).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=0.35)
        self.play(Write(title), GrowFromCenter(rule), run_time=0.8)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
Y0 = 0.4
BODYC = P(-4.6, Y0)


def neuron():
    body = Circle(radius=1.7, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.35).move_to(BODYC)
    axon = Line(P(-2.9, Y0), P(3.4, Y0), color=BLUE, stroke_width=14)
    branches = VGroup(Line(P(3.4, Y0), P(6.2, Y0 + 2.1), color=BLUE, stroke_width=9),
                      Line(P(3.4, Y0), P(6.5, Y0), color=BLUE, stroke_width=9),
                      Line(P(3.4, Y0), P(6.2, Y0 - 2.1), color=BLUE, stroke_width=9))
    return body, VGroup(axon, branches)


def axon_icon():
    return VGroup(Circle(radius=0.7, stroke_width=0, fill_color=VIOLET, fill_opacity=0.22),
                  scissors(0.7)).move_to(P(0.7, Y0 + 1.5))


class S01Q(SpokenScene):
    def construct(self):
        body, axon = neuron()
        lab_b = T("cell body", 28, GREY).move_to(P(-4.6, Y0 - 2.05))
        lab_a = T("axon", 28, GREY).move_to(P(-1.2, Y0 + 0.65))
        sb = scissors(1.0, sw=6).move_to(P(-4.6, Y0 + 0.5))
        cb = T("caspases", 28, VIOLET).move_to(P(-4.6, Y0 - 0.5))
        sa = axon_icon()
        ca = T("caspases", 28, VIOLET).move_to(P(2.6, Y0 + 1.5))
        qb = qmark(96).move_to(P(-4.6, 3.05))
        qa = qmark(96).move_to(P(0.7, 3.05))
        self.at("cell body")
        self.play(FadeIn(body, scale=0.8), FadeIn(lab_b, shift=UP * 0.1), run_time=0.7)
        self.at("its axon")
        self.play(Create(axon), FadeIn(lab_a, shift=UP * 0.1), run_time=0.9)
        self.at("share one cytoplasm")
        br = Brace(Line(P(-6.3, -2.35), P(6.5, -2.35)), DOWN, color=GREY)
        one = T("one cytoplasm", 30, GREY).move_to(P(0.1, -3.4))
        self.play(GrowFromCenter(br), FadeIn(one, shift=DOWN * 0.1), run_time=0.8)
        self.at("both contain caspases")
        self.play(FadeIn(sb, scale=0.5), FadeIn(cb, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(sa, scale=0.5), FadeIn(ca, shift=UP * 0.1), run_time=0.5)
        self.at("so how can")
        self.play(FadeIn(qb, scale=0.6), FadeIn(qa, scale=0.6), run_time=0.5)
        self.at("in one")
        self.play(Indicate(sb, color=VIOLET, scale_factor=1.3), Indicate(qb, color=TEXT, scale_factor=1.2), run_time=0.8)
        self.at("not the other")
        self.play(Indicate(sa, color=VIOLET, scale_factor=1.3), Indicate(qa, color=TEXT, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Define(SpokenScene):
    def construct(self):
        cx, cy = 3.0, 0.9
        sc = scissors(3.12, sw=6).move_to(P(-3.5, cy))
        name = T("caspases", 44, VIOLET).move_to(P(-3.5, cy - 2.15))
        sub = T("proteases", 32, GREY).move_to(P(-3.5, cy - 2.9))
        pcs = VGroup(*[Circle(radius=0.62, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35)
                       .move_to(P(cx, cy) + (P(0, 0) if k < 0 else 1.15 * P(np.cos(a), np.sin(a))))
                       for k, a in [(-1, 0)] + [(i, i * PI / 3) for i in range(6)]]).scale(1.3, about_point=P(cx, cy))
        self.at("caspases are proteases")
        self.play(FadeIn(sc, scale=0.5), FadeIn(name, shift=UP * 0.1), run_time=0.7)
        self.at("proteases that")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.at("that dismantle")
        self.play(FadeIn(pcs, scale=0.8), run_time=0.5)
        self.at("dismantle")
        self.play(sc.animate.shift(RIGHT * 1.6), name.animate.shift(RIGHT * 1.6), sub.animate.shift(RIGHT * 1.6), run_time=0.4)
        self.play(snip(sc, 2, rt=0.1), run_time=0.4)
        self.play(*[p.animate.set_color(RED).set_fill(RED, 0.5).shift(0.9 * (p.get_center() - P(cx, cy))
                                                                   / max(np.linalg.norm(p.get_center() - P(cx, cy)), 0.4))
                    for p in pcs], run_time=0.5)
        self.at("apoptosis")
        apo = chip("apoptosis", RED, size=52).move_to(P(cx, -2.65))
        self.play(FadeIn(apo, shift=UP * 0.2), run_time=0.5)
        self.at("built in")
        prog = T("a built-in program of cell death", 26, GREY).move_to(P(cx, -3.55))
        self.play(FadeIn(prog, shift=UP * 0.1), run_time=0.6)
        self.at("cell death")
        self.play(Indicate(apo, color=RED, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Logic(SpokenScene):
    def construct(self):
        body, axon = neuron()
        lab_b = T("cell body", 28, GREY).move_to(P(-4.6, Y0 - 2.05))
        lab_a = T("axon", 28, GREY).move_to(P(-1.2, Y0 + 0.65))
        sb = scissors(1.0, sw=6).move_to(P(-4.6, Y0 + 0.2))
        sa = axon_icon()
        self.add(body, axon, lab_b, lab_a, sb, sa)
        self.at("to find out")
        dash = DashedLine(P(-2.65, 3.4), P(-2.65, -3.4), color=TEXT, stroke_width=4, dash_length=0.2)
        self.play(Create(dash), run_time=0.6)
        self.at("deprive one place")
        self.play(Indicate(body, color=BLUE, scale_factor=1.12), run_time=0.7)
        self.at("and not the other")
        self.play(Indicate(axon, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def micro_label():
    return T("microfluidic chamber", 28, GREY).move_to(P(0, -3.3))


class S04Who(SpokenScene):
    def construct(self):
        yr = T("2013", 72, GOLD, font=TITLE_FONT).move_to(P(0, 1.3))
        nm = T("Cusack, Deshmukh and colleagues", 42).move_to(P(0, 0.0))
        mn = T("mouse sympathetic neurons", 36, GREY).move_to(P(0, -1.1))
        self.at("in 2013")
        self.play(FadeIn(yr, shift=UP * 0.15), run_time=0.6)
        self.at("corey cusack")
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.7)
        self.at("grew mouse sympathetic")
        self.play(FadeIn(mn, shift=UP * 0.1), run_time=0.6)
        self.at("microfluidic chamber")
        C = Chamber(labels=False)
        lab = micro_label()
        self.play(FadeOut(yr), FadeOut(nm), FadeOut(mn), FadeIn(C.cl), FadeIn(C.cr), FadeIn(C.bar),
                  FadeIn(lab, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Chamber(SpokenScene):
    def construct(self):
        C = Chamber()
        lab = micro_label()
        self.add(C.cl, C.cr, C.bar, lab)
        lg = legend()
        grooves = T("narrow grooves", 26, GREY).move_to(P(0, -3.3))
        leader = Line(P(0, -3.05), P(0, -ch_bottom()), color=GREY, stroke_width=3)
        self.at("the cell bodies")
        self.play(FadeOut(lab), FadeIn(C.lab_l, shift=DOWN * 0.1), FadeIn(C.bodies, scale=0.6), run_time=0.7)
        self.at("one compartment")
        cbc = T("cell-body compartment", 26, GREY).move_to(C.lab_l.get_center())
        self.play(Indicate(C.cl, color=TEXT, scale_factor=1.02), Transform(C.lab_l, cbc), run_time=0.8)
        self.at("their axons grew")
        self.play(AnimationGroup(*[Create(l) for l in C.ax_in], FadeIn(C.lab_r),
                                 LaggedStart(*[Create(s) for row in C.ax_out for s in row], lag_ratio=0.03, run_time=1.2),
                                 FadeIn(C.tips)), run_time=1.4)
        self.at("narrow grooves")
        self.play(FadeIn(grooves, shift=DOWN * 0.1), Create(leader), Indicate(C.bar, color=TEXT, scale_factor=1.0), run_time=0.8)
        self.at("into a second")
        axc = T("axon compartment", 26, GREY).move_to(C.lab_r.get_center())
        self.play(Indicate(C.cr, color=TEXT, scale_factor=1.02), Transform(C.lab_r, axc), run_time=0.8)
        self.at("the fluid stayed apart")
        self.play(FadeIn(lg, shift=DOWN * 0.1), LaggedStart(*[FadeIn(d, scale=0.3) for d in C.dl], lag_ratio=0.03),
                  LaggedStart(*[FadeIn(d, scale=0.3) for d in C.dr], lag_ratio=0.03), run_time=0.9)
        self.finish()


def ch_bottom():
    return 2.8


# ---------------------------------------------------------------------------------------------
class S06Two(SpokenScene):
    def construct(self):
        Cb = Chamber()
        lgb = legend()
        cbc = T("cell-body compartment", 26, GREY).move_to(Cb.lab_l.get_center())
        axc = T("axon compartment", 26, GREY).move_to(Cb.lab_r.get_center())
        grooves = T("narrow grooves", 26, GREY).move_to(P(0, -3.3))
        old = VGroup(Cb.everything(), cbc, axc, grooves, lgb)
        self.add(old)
        st = Stack()
        C1, C2 = st.C
        row2 = VGroup(C2.everything())
        sn2 = snap(row2)
        set_op(sn2, 0.3)
        self.at("local deprivation")
        self.play(FadeOut(old), FadeIn(C1.everything()), FadeIn(row2), FadeIn(st.lab[0], shift=DOWN * 0.1),
                  FadeIn(st.leg), run_time=0.9)
        self.at("ngf")
        self.play(Indicate(st.leg, color=YELLOW, scale_factor=1.2), run_time=0.7)
        self.at("from the axon compartment")
        self.play(drain(C1.dr, 1.0, up=0.25), run_time=1.0)
        self.at("global deprivation")
        self.play(*scale_op(sn2, 1.0), FadeIn(st.lab[1], shift=DOWN * 0.1), run_time=0.8)
        self.at("from both")
        self.play(drain(C2.dl, 0.9, up=0.25), drain(C2.dr, 0.9, up=0.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Q1(SpokenScene):
    def construct(self):
        st = Stack()
        st.add_neutral(self)
        self.at("in normal neurons")
        self.play(FadeIn(st.ques, shift=DOWN * 0.1), run_time=0.5)
        self.at("what happens")
        self.play(*[FadeIn(q, scale=0.6) for q in st.q], run_time=0.5)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        st = Stack()
        st.add_neutral(self)
        self.add(st.ques, *st.q)
        idle(self, [VGroup(st.q[0], st.q[1]), VGroup(st.q[2], st.q[3])])


# ---------------------------------------------------------------------------------------------
class S09R1(SpokenScene):
    def construct(self):
        st = Stack()
        st.add_neutral(self)
        self.add(st.ques, *st.q)
        C1, C2 = st.C
        dim2 = VGroup(C2.core(dl=False, dr=False), st.lab[1])
        self.at("local deprivation")
        self.play(FadeOut(st.ques), *[FadeOut(q) for q in st.q], *dim_to(dim2, 0.3),
                  Indicate(st.lab[0], color=TEXT), run_time=0.8)
        self.at("the axons degenerate")
        fragment(self, C1.ax_out, extra=[C1.tips], rt=1.2)
        ca = st.chip_at(0, 1, "axons degenerate", RED)
        self.play(FadeIn(ca, shift=UP * 0.1), run_time=0.4)
        self.at("cell bodies live")
        cb = st.chip_at(0, 0, "cell bodies live", GREEN)
        self.play(FadeIn(cb, shift=UP * 0.1), C1.bodies.animate.set_stroke(GREEN).set_fill(GREEN, 0.4), run_time=0.4)
        self.play(Indicate(C1.bodies, color=GREEN, scale_factor=1.3), run_time=0.5)
        self.at("that is pruning")
        pr = pr_label()
        self.play(ReplacementTransform(st.lab[0], pr), run_time=0.6)
        self.finish()


class S10R1b(SpokenScene):
    def construct(self):
        st = Stack()
        C1, C2 = st.C
        C1.bodies.set_stroke(GREEN).set_fill(GREEN, 0.4)
        pr = pr_label()
        ca = st.chip_at(0, 1, "axons degenerate", RED)
        cb = st.chip_at(0, 0, "cell bodies live", GREEN)
        row1 = VGroup(C1.core(dr=False, axons_out=False), pr)
        self.add(row1, ca, cb, C2.core(dl=False, dr=False), st.lab[1], st.leg)
        self.at("global deprivation")
        self.play(*dim_to(row1, 0.3), Indicate(st.lab[1], color=TEXT), run_time=0.8)
        self.at("the neurons die")
        nd = st.chip_at(1, 0, "neurons die", RED)
        self.play(C2.bodies.animate.set_stroke(RED).set_fill(RED, 0.5).scale(0.75), C2.ax_in.animate.set_color(RED),
                  FadeIn(nd, shift=UP * 0.1), run_time=0.7)
        self.at("their axons go")
        fragment(self, C2.ax_out, extra=[C2.tips], rt=0.75)
        ag = st.chip_at(1, 1, "axons go with them", RED)
        self.at("with them")
        self.play(FadeIn(ag, shift=UP * 0.1), FadeOut(C2.bodies), FadeOut(C2.ax_in), run_time=0.6)
        self.at("that is developmental")
        dc = dc_label()
        self.play(ReplacementTransform(st.lab[1], dc), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11Table(SpokenScene):
    def construct(self):
        st = Stack()
        C1, C2 = st.C
        C1.bodies.set_stroke(GREEN).set_fill(GREEN, 0.4)
        pr, dc = pr_label(), dc_label()
        ca = st.chip_at(0, 1, "axons degenerate", RED)
        cb = st.chip_at(0, 0, "cell bodies live", GREEN)
        nd = st.chip_at(1, 0, "neurons die", RED)
        ag = st.chip_at(1, 1, "axons go with them", RED)
        scene_old = VGroup(C1.core(dr=False, axons_out=False), pr,
                           C2.core(dl=False, dr=False, bodies=False, ax_in=False, axons_out=False), dc, st.leg)
        set_op(snap(VGroup(C1.core(dr=False, axons_out=False), pr)), 0.3)
        self.add(scene_old, ca, cb, nd, ag)
        tb = Tbl()
        self.at("fill in a table")
        moves = [(ca[1], tb.fill[(0, 0)][0]), (cb[1], tb.fill[(0, 0)][1]), (nd[1], tb.fill[(0, 1)][0]),
                 (ag[1], tb.fill[(0, 1)][1])]
        self.play(FadeOut(scene_old), FadeIn(tb.heads), FadeIn(tb.grid()), *[FadeOut(c[0]) for c in (ca, cb, nd, ag)],
                  *[ReplacementTransform(a, b) for a, b in moves], run_time=1.0)
        self.at("one genotype per row")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in tb.rh], lag_ratio=0.25, run_time=0.8))
        self.finish()


# ---------------------------------------------------------------------------------------------
Q2 = "Does axon breakdown need caspase-6 in both experiments?"
Q3 = "Does local pruning need Apaf-1 too?"


class S12Q2(SpokenScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1)])
        ql = question_line(Q2)
        self.at("does axon breakdown")
        hl = tb.hl(1)
        self.play(Create(hl), FadeIn(ql, shift=UP * 0.1), run_time=0.8)
        self.at("in both experiments")
        self.play(Indicate(tb.rect[1][0], color=GOLD, scale_factor=1.04), Indicate(tb.rect[1][1], color=GOLD, scale_factor=1.04), run_time=0.9)
        self.at("delete it")
        self.play(Indicate(tb.rh[1], color=VIOLET, scale_factor=1.2), run_time=0.5)
        self.at("predict each one")
        self.play(FadeIn(tb.qm[(1, 0)], scale=0.6), FadeIn(tb.qm[(1, 1)], scale=0.6), run_time=0.5)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1)], q=[(1, 0), (1, 1)])
        self.add(tb.hl(1), question_line(Q2))
        idle(self, [tb.qm[(1, 0)], tb.qm[(1, 1)]])


# ---------------------------------------------------------------------------------------------
class S14R2(SpokenScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1)], q=[(1, 0), (1, 1)])
        ql = question_line(Q2)
        self.add(tb.hl(1), ql)
        self.at("without")
        self.play(Indicate(tb.rh[1], color=VIOLET, scale_factor=1.2), run_time=0.7)
        self.at("locally deprived axons")
        self.play(Indicate(tb.rect[1][0], color=GOLD, scale_factor=1.04), FadeOut(ql), run_time=0.8)
        self.at("were protected")
        tb.swap(self, (1, 0))
        self.finish()


class S15R2b(SpokenScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1), (1, 0)], q=[(1, 1)])
        self.add(tb.hl(1))
        self.at("after global")
        self.play(Indicate(tb.rect[1][1], color=GOLD, scale_factor=1.04), run_time=0.8)
        g = tb.fill[(1, 1)]
        self.at("axons still degenerated")
        self.play(FadeOut(tb.qm[(1, 1)]), run_time=0.2)
        self.play(FadeIn(g[1], shift=UP * 0.1), run_time=0.5)
        self.at("as the neurons died")
        self.play(FadeIn(g[0], shift=UP * 0.1), run_time=0.5)
        self.finish()


class S15bBridge(SpokenScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1), (1, 0), (1, 1)], dim=[2])
        self.add(tb.hl(1))
        self.at("different needs")
        self.play(Indicate(tb.fill[(1, 0)], color=GREEN, scale_factor=1.1), Indicate(tb.fill[(1, 1)], color=RED, scale_factor=1.1), run_time=0.9)
        self.at("a second mutant")
        self.play(Indicate(tb.rh[2], color=ORANGE, scale_factor=1.25), run_time=0.9)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1), (1, 0), (1, 1)], dim=[2])
        self.add(tb.hl(1))
        idle(self, [tb.rh[2], tb.fill[(1, 0)]], rt=0.9)


# ---------------------------------------------------------------------------------------------
WC = P(0, -0.1)
WR = 2.3
SCAT = [(-5.4, 0.8), (-3.9, -2.2), (-3.0, 1.2), (3.6, 2.2), (5.3, 0.3), (4.0, -2.0)]
NBLK = 6


def block(pos, theta=0.0):
    b = RoundedRectangle(corner_radius=0.14, width=0.9, height=1.4, stroke_color=ORANGE, stroke_width=4,
                         fill_color=ORANGE, fill_opacity=0.4)
    return b.rotate(theta).move_to(pos)


def ring_blocks(center=WC):
    return VGroup(*[block(center + WR * P(np.cos(k * 2 * PI / NBLK), np.sin(k * 2 * PI / NBLK)),
                          k * 2 * PI / NBLK - PI / 2) for k in range(NBLK)])


def apo_tag():
    return chip("apoptosis", RED, size=34).move_to(P(5.2, 3.15))


class S17Apaf(SpokenScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1), (1, 0), (1, 1)], dim=[2])
        self.add(tb.hl(1))
        rng = random.Random(3)
        scat = VGroup(*[block(P(*p), rng.uniform(-PI, PI)) for p in SCAT])
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        self.at("other end")
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in scat], lag_ratio=0.12, run_time=1.0))
        self.at("during apoptosis")
        apo = apo_tag()
        self.play(FadeIn(apo, shift=DOWN * 0.1), run_time=0.5)
        self.at("apaf1")
        lab = T("Apaf-1 proteins", 38, ORANGE).move_to(P(0, 3.3))
        a1 = Arrow(P(-1.0, 3.0), scat[0].get_top() + UP * 0.08, buff=0, color=ORANGE, stroke_width=5, tip_length=0.2)
        a2 = Arrow(P(0.0, 3.0), scat[2].get_top() + UP * 0.08, buff=0, color=ORANGE, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(lab, shift=DOWN * 0.1), GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.at("builds", lead=0.5)
        ring = ring_blocks()
        self.play(FadeOut(a1), FadeOut(a2), *[ReplacementTransform(s, t) for s, t in zip(scat, ring)], run_time=0.7)
        self.at("apoptosome")
        name = T("apoptosome", 32, ORANGE).move_to(WC)
        self.play(FadeIn(name, scale=0.7), run_time=0.5)
        self.finish()


class S18Apaf2(SpokenScene):
    def construct(self):
        ring = ring_blocks()
        name = T("apoptosome", 32, ORANGE).move_to(WC)
        apo = apo_tag()
        lab = T("Apaf-1 proteins", 38, ORANGE).move_to(P(0, 3.3))
        self.add(ring, name, apo, lab)
        self.at("the apoptosome")
        wheel = VGroup(ring, name)
        self.play(FadeOut(lab), wheel.animate.shift(LEFT * 3.7), run_time=0.9)
        c9 = dim_chip(chip("caspase-9", VIOLET, size=50)).move_to(P(3.3, 1.6))
        c3 = dim_chip(chip("caspase-3", VIOLET, size=50)).move_to(P(3.3, -1.7))
        a1 = Arrow(P(-0.65, 0.5), c9.get_left() + LEFT * 0.1, buff=0, color=ORANGE, stroke_width=7, tip_length=0.28)
        a2 = Arrow(c9.get_bottom() + DOWN * 0.1, c3.get_top() + UP * 0.1, buff=0, color=VIOLET, stroke_width=7, tip_length=0.28)
        self.at("switches on")
        self.play(FadeIn(c9), GrowArrow(a1), run_time=0.5)
        self.at("caspase 9")
        self.play(chip_style(c9, VIOLET, 0.55), run_time=0.35)
        self.play(Indicate(c9, color=VIOLET, scale_factor=1.12), run_time=0.4)
        self.at("then switches on")
        self.play(FadeIn(c3), GrowArrow(a2), run_time=0.5)
        self.at("caspase 3")
        self.play(chip_style(c3, VIOLET, 0.55), run_time=0.35)
        self.play(Indicate(c3, color=VIOLET, scale_factor=1.12), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19Q3(SpokenScene):
    def construct(self):
        self.at("local pruning needed")
        head = T("local pruning needed", 44).move_to(P(0, 1.9))
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        names = ["caspase-9", "caspase-3", "caspase-6"]
        xs = [-4.3, 0.0, 4.3]
        chips = [chip(n, VIOLET, size=46).move_to(P(x, -0.2)) for n, x in zip(names, xs)]
        self.at("9")
        self.play(FadeIn(chips[0], scale=0.7), run_time=0.4)
        self.at("3")
        self.play(FadeIn(chips[1], scale=0.7), run_time=0.4)
        self.at("6")
        self.play(FadeIn(chips[2], scale=0.7), run_time=0.4)
        self.at("does it need")
        tb = Tbl()
        ql = question_line(Q3)
        pieces = VGroup(tb.heads, tb.grid(), *tb.rh, *[tb.fill[k] for k in [(0, 0), (0, 1), (1, 0), (1, 1)]],
                        tb.qm[(2, 0)], tb.qm[(2, 1)])
        self.play(FadeOut(head), *[FadeOut(c) for c in chips], run_time=0.4)
        self.play(FadeIn(pieces), Create(tb.hl(2)), FadeIn(ql, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S20Pause(NarratedScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1), (1, 0), (1, 1)], q=[(2, 0), (2, 1)])
        self.add(tb.hl(2), question_line(Q3))
        idle(self, [tb.qm[(2, 0)], tb.qm[(2, 1)]])


# ---------------------------------------------------------------------------------------------
class S21R3(SpokenScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1), (1, 0), (1, 1)], q=[(2, 0), (2, 1)])
        ql = question_line(Q3)
        self.add(tb.hl(2), ql)
        g = tb.fill[(2, 0)]
        self.at("without")
        self.play(Indicate(tb.rh[2], color=ORANGE, scale_factor=1.2), run_time=0.7)
        self.at("locally deprived axons")
        self.play(Indicate(tb.rect[2][0], color=GOLD, scale_factor=1.04), FadeOut(tb.qm[(2, 0)]), FadeOut(ql), run_time=0.8)
        self.at("still degenerated")
        self.play(FadeIn(g[0], shift=UP * 0.1), run_time=0.5)
        self.at("cell bodies lived")
        self.play(FadeIn(g[1], shift=UP * 0.1), run_time=0.5)
        self.finish()


class S22R3b(SpokenScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=[(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], q=[(2, 1)])
        self.add(tb.hl(2))
        self.at("after global")
        self.play(Indicate(tb.rect[2][1], color=GOLD, scale_factor=1.04), run_time=0.8)
        self.at("resisted death")
        tb.swap(self, (2, 1))
        self.at("death of the whole")
        self.play(Indicate(tb.rh[2], color=ORANGE, scale_factor=1.2), Indicate(tb.fill[(2, 1)], color=GREEN, scale_factor=1.08), run_time=1.0)
        self.finish()


class S23Beat(NarratedScene):
    def construct(self):
        tb = Tbl()
        tb.base(self, filled=list(CELLS.keys()))
        self.add(tb.hl(2))
        idle(self, [tb.fill[(2, 0)], tb.fill[(2, 1)]], scale=1.08, rt=0.9)


# ---------------------------------------------------------------------------------------------
LX, RX = -3.4, 3.4
LROW = [1.6, 0.35, -0.9, -2.15]
HEADY = 3.0


class Lists:
    def __init__(self):
        self.tl = T("local route", 40).move_to(P(LX, HEADY))
        self.tr = T("global route", 40).move_to(P(RX, HEADY))
        self.tr.align_to(self.tl, UP)
        self.div = Line(P(0, 3.5), P(0, -2.9), color=GREY, stroke_width=3)
        sz = 38
        # slot 0 is the top: Apaf-1 acts first in the cascade, so it heads both lists
        self.la = dim_chip(chip("Apaf-1", ORANGE, size=sz), 0.35).move_to(P(LX, LROW[0]))
        self.lx = cross(self.la, w=6, pad=0.0).scale(0.55).next_to(self.la, RIGHT, buff=0.25)
        self.l9 = chip("caspase-9", VIOLET, size=sz).move_to(P(LX, LROW[1]))
        self.l3 = chip("caspase-3", VIOLET, size=sz).move_to(P(LX, LROW[2]))
        self.l6 = chip("caspase-6", VIOLET, size=sz).move_to(P(LX, LROW[3]))
        self.ra = chip("Apaf-1 (apoptosome)", ORANGE, size=34).move_to(P(RX, LROW[0]))
        self.r9 = chip("caspase-9", VIOLET, size=sz).move_to(P(RX, LROW[1]))
        self.r3 = chip("caspase-3", VIOLET, size=sz).move_to(P(RX, LROW[2]))

    def all(self):
        return VGroup(self.tl, self.tr, self.div, self.la, self.lx, self.l9, self.l3, self.l6, self.ra, self.r9, self.r3)


def glow(mob, color, w=6):
    return SurroundingRectangle(mob, color=color, buff=0.1, stroke_width=w, corner_radius=0.18)


class S24Concl(SpokenScene):
    def construct(self):
        L = Lists()
        self.at("in this study")
        self.play(FadeIn(L.tl, shift=DOWN * 0.1), FadeIn(L.tr, shift=DOWN * 0.1), Create(L.div),
                  *[FadeIn(m, shift=UP * 0.1) for m in (L.l9, L.l3, L.r9, L.r3)], run_time=0.8)
        self.at("caspase 6", lead=0)
        g6 = glow(L.l6, VIOLET)
        self.play(FadeIn(L.l6, scale=0.7), Create(g6), run_time=0.5)
        self.at("for the local route")
        self.play(Indicate(L.l6, color=VIOLET, scale_factor=1.12), FadeIn(L.la), run_time=0.6)
        self.play(Create(L.lx), run_time=0.4)
        self.at("mattered only", nth=1)
        self.play(FadeOut(g6), FadeIn(L.ra, scale=0.7), run_time=0.5)
        self.at("global route", lead=0)
        gr = glow(L.ra, ORANGE)
        self.play(Indicate(L.ra, color=ORANGE, scale_factor=1.08), Create(gr), run_time=0.8)
        self.finish()


class S25Concl2(SpokenScene):
    def construct(self):
        L = Lists()
        self.add(L.all())
        self.at("something the other does not")
        g6, gr = glow(L.l6, GOLD), glow(L.ra, GOLD)
        self.play(Create(g6), Create(gr), run_time=0.7)
        self.at("they share enzymes")
        j9 = Line(L.l9.get_right() + RIGHT * 0.12, L.r9.get_left() + LEFT * 0.12, color=VIOLET, stroke_width=6)
        j3 = Line(L.l3.get_right() + RIGHT * 0.12, L.r3.get_left() + LEFT * 0.12, color=VIOLET, stroke_width=6)
        gs = [glow(m, VIOLET) for m in (L.l9, L.l3, L.r9, L.r3)]
        self.play(*[Create(g) for g in gs], Create(j9), Create(j3), run_time=0.8)
        self.at("wired differently")
        line = T("two differently wired routes", 38).move_to(P(0, -3.35))
        self.play(FadeIn(line, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def deprived_chamber():
    C = Chamber()
    sc = VGroup(*[VGroup(Circle(radius=0.7, stroke_width=0, fill_color=VIOLET, fill_opacity=0.25),
                         scissors(0.65)).move_to(P(3.0, y)) for y in C.ay])
    act = T("active caspases", 28, VIOLET).move_to(P(3.55, -3.3))
    banner = T("local deprivation", 30).move_to(P(0, 3.2))
    return C, sc, act, banner


class S26Q4(SpokenScene):
    def construct(self):
        C, sc, act, banner = deprived_chamber()
        lg = legend()
        C.lab_l.move_to(P(-5.0, 3.2))
        self.add(C.core(dr=False), C.lab_l, C.lab_r, lg, banner)
        self.at("caspases become active")
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in sc], lag_ratio=0.2, run_time=0.9), FadeIn(act, shift=UP * 0.1))
        self.at("deprived axon")
        self.play(Indicate(sc, color=VIOLET, scale_factor=1.1), run_time=0.8)
        self.at("what keeps")
        q = qmark(90).move_to(P(-3.0, 3.3))
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.at("cell body")
        self.play(Indicate(C.bodies, color=BLUE, scale_factor=1.3), Indicate(q, color=TEXT, scale_factor=1.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
BC = P(-3.0, 0.0)


def big_body():
    return Circle(radius=3.3, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.28).move_to(BC)


def zoom_parts():
    lab = T("cell body", 28, GREY).move_to(P(-3.0, 2.7))
    c9 = chip("caspase-9", VIOLET, size=34).move_to(P(-1.5, 1.3))
    c3 = chip("caspase-3", VIOLET, size=34).move_to(P(-1.5, -1.3))
    xi = chip("XIAP", INHIB, size=40).move_to(P(-4.7, 0.0))
    b9 = inhib(P(-3.7, 0.25), P(-2.95, 1.05))
    b3 = inhib(P(-3.7, -0.25), P(-2.95, -1.05))
    note = lines(["XIAP binds and blocks", "active caspase-9 and -3"], 30, INHIB).move_to(P(3.7, 0.5))
    return lab, c9, c3, xi, b9, b3, note


def off(c):
    c[0].set_stroke(GREY, opacity=0.7).set_fill(GREY, 0.12)
    c[1].set_color(GREY)
    return c


def proteasome():
    cap1 = RoundedRectangle(corner_radius=0.08, width=0.28, height=1.0, stroke_color=INHIB, stroke_width=4, fill_color=INHIB, fill_opacity=0.5)
    core = RoundedRectangle(corner_radius=0.08, width=1.0, height=0.8, stroke_color=INHIB, stroke_width=4, fill_color=INHIB, fill_opacity=0.2)
    g = VGroup(cap1, core, cap1.copy()).arrange(RIGHT, buff=0.05).scale(1.15)
    return g.move_to(P(-4.0, -1.95))


def prot_parts():
    pr = proteasome()
    # Route below the caspase-3 chip, with the barrel wholly inside the soma.
    leader = VMobject(color=INHIB, stroke_width=3).set_points_as_corners([
        pr.get_bottom() + DOWN * 0.08, P(-4.0, -2.85), P(1.4, -2.85)])
    pl = lines(["proteasome keeps", "caspases off"], 28, INHIB).move_to(P(3.9, -2.85))
    return pr, leader, pl


BUILD_PTS = [(-4.8, 1.5), (-3.6, 1.0), (-2.2, 0.0), (-0.8, 0.1), (-4.0, -0.95), (-1.9, -2.35)]
COND = "after local deprivation"


class S27Xiap(SpokenScene):
    def construct(self):
        C, sc, act, banner = deprived_chamber()
        lg = legend()
        q = qmark(90).move_to(P(-3.0, 3.3))
        C.lab_l.move_to(P(-5.0, 3.2))
        others = VGroup(C.core(dr=False, bodies=False), C.lab_l, C.lab_r, lg, sc, q, act, banner)
        body = C.bodies[1]
        self.add(others, C.bodies)
        lab, c9, c3, xi, b9, b3, note = zoom_parts()
        big = big_body()
        self.at("the same study")
        self.play(FadeOut(others), FadeOut(C.bodies[0]), FadeOut(C.bodies[2]), run_time=0.5)
        self.play(ReplacementTransform(body, big), run_time=0.8)
        self.play(FadeIn(lab), run_time=0.3)
        self.at("keep caspases off")
        self.play(FadeIn(c9, scale=0.7), FadeIn(c3, scale=0.7), run_time=0.6)
        self.at("one is")
        self.play(FadeIn(xi, scale=0.7), run_time=0.5)
        self.at("which blocks")
        self.play(Create(b9), Create(b3), FadeIn(note, shift=LEFT * 0.1), run_time=0.7)
        self.at("caspase 9")
        self.play(chip_style(c9, GREY, 0.12, 0.7), run_time=0.5)
        self.at("and caspase 3")
        self.play(chip_style(c3, GREY, 0.12, 0.7), run_time=0.5)
        self.finish()


class S28Prot(SpokenScene):
    def construct(self):
        big = big_body()
        lab, c9, c3, xi, b9, b3, note = zoom_parts()
        off(c9), off(c3)
        self.add(big, lab, c9, c3, xi, b9, b3, note)
        pr, leader, pl = prot_parts()
        self.at("the proteasome")
        self.play(FadeIn(pr, scale=0.6), run_time=0.5)
        self.play(Create(leader), FadeIn(pl, shift=LEFT * 0.1), run_time=0.6)
        self.finish()


def xko_start(scene):
    big = big_body()
    lab, c9, c3, xi, b9, b3, note = zoom_parts()
    off(c9), off(c3)
    pr, leader, pl = prot_parts()
    scene.add(big, lab, c9, c3, xi, b9, b3, note, pr, leader, pl)
    return big, lab, c9, c3, xi, b9, b3, note, pr, leader, pl


class S29Xko(SpokenScene):
    def construct(self):
        big, lab, c9, c3, xi, b9, b3, note, pr, leader, pl = xko_start(self)
        cond = T(COND, 28, GREY).move_to(P(3.7, 3.0))
        self.play(FadeOut(note), FadeIn(cond, shift=DOWN * 0.1), run_time=0.5)
        self.at("lacking")
        x = cross(xi, w=7)
        self.play(xi.animate.set_opacity(0.35), FadeOut(b9), FadeOut(b3), Create(x), run_time=0.7)
        self.at("built up", lead=0)
        sc = VGroup(*[scissors(0.6).move_to(P(*p)) for p in BUILD_PTS])
        t = lines(["active caspase-3", "builds up"], 32, VIOLET).move_to(P(3.7, 0.5))
        self.play(chip_style(c3, VIOLET, 0.45, 1.0).set_run_time(0.2),
                  FadeIn(t, shift=LEFT * 0.1, run_time=0.2),
                  LaggedStart(*[FadeIn(s, scale=0.3) for s in sc], lag_ratio=0.2, run_time=1.1))
        self.at("in their cell bodies")
        self.play(Indicate(big, color=BLUE, scale_factor=1.02), run_time=0.8)
        self.finish()


class S29Beat(NarratedScene):
    def construct(self):
        big, lab, c9, c3, xi, b9, b3, note, pr, leader, pl = xko_start(self)
        self.remove(note, b9, b3)
        cond = T(COND, 28, GREY).move_to(P(3.7, 3.0))
        x = cross(xi, w=7)
        xi.set_opacity(0.35)
        sc = VGroup(*[scissors(0.6).move_to(P(*p)) for p in BUILD_PTS])
        t = lines(["active caspase-3", "builds up"], 32, VIOLET).move_to(P(3.7, 0.5))
        c3[0].set_stroke(VIOLET, opacity=1.0).set_fill(VIOLET, 0.45)
        c3[1].set_color(VIOLET)
        self.add(cond, x, sc, t)
        # the free scissors keep snipping while the sentence lands
        t0 = 0
        while self.elapsed() + 0.9 < self.narration_s:
            self.play(*[snip(s, 1, rt=0.12) for s in sc[:3]] if (t0 % 2 == 0) else [snip(s, 1, rt=0.12) for s in sc[3:]], run_time=0.3)
            self.wait(0.4)
            t0 += 1
        rest = self.narration_s - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


# ---------------------------------------------------------------------------------------------
class S30Take(SpokenScene):
    def construct(self):
        sz = 28
        slots = [1.55, 0.3, -0.95, -2.2]
        # panel 1: same enzymes
        p1x, lx, gx, p3x = -5.4, -2.5, 0.6, 4.6
        h1 = T("same enzymes", 30, VIOLET).move_to(P(p1x, 3.0))
        s1 = scissors(1.4, sw=6).move_to(P(p1x, slots[0] + 0.1))
        k9 = chip("caspase-9", VIOLET, size=sz).move_to(P(p1x, slots[1]))
        k3 = chip("caspase-3", VIOLET, size=sz).move_to(P(p1x, slots[2]))
        # panel 2: two wirings
        h2 = T("two wirings", 30).move_to(P(-0.95, 3.0))
        tl = T("local", 26, GREY).move_to(P(lx, 2.25))
        tg = T("global", 26, GREY).move_to(P(gx, 2.25))
        la = dim_chip(chip("Apaf-1", ORANGE, size=sz), 0.35).move_to(P(lx, slots[0]))
        lxx = cross(la, w=5, pad=0.0).scale(0.55).next_to(la, RIGHT, buff=0.15)
        l9 = chip("caspase-9", VIOLET, size=sz).move_to(P(lx, slots[1]))
        l3 = chip("caspase-3", VIOLET, size=sz).move_to(P(lx, slots[2]))
        l6 = chip("caspase-6", VIOLET, size=sz).move_to(P(lx, slots[3]))
        ga = chip("Apaf-1", ORANGE, size=sz).move_to(P(gx, slots[0]))
        g9 = chip("caspase-9", VIOLET, size=sz).move_to(P(gx, slots[1]))
        g3 = chip("caspase-3", VIOLET, size=sz).move_to(P(gx, slots[2]))
        j9 = Line(l9.get_right() + RIGHT * 0.08, g9.get_left() + LEFT * 0.08, color=VIOLET, stroke_width=5)
        j3 = Line(l3.get_right() + RIGHT * 0.08, g3.get_left() + LEFT * 0.08, color=VIOLET, stroke_width=5)
        # panel 3: the inhibitor guards the cell body
        h3 = lines(["an inhibitor guards", "the cell body"], 28, INHIB).move_to(P(p3x, 3.0))
        body = Circle(radius=1.15, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.35).move_to(P(p3x, 0.8))
        bl = T("cell body", 26, GREY).move_to(P(p3x, 0.8))
        shield = Arc(radius=1.65, start_angle=PI * 0.6, angle=PI * 0.8, color=INHIB, stroke_width=14).move_arc_center_to(P(p3x, 0.8))
        xi = chip("XIAP", INHIB, size=sz).move_to(P(p3x, -1.2))
        pc = chip("proteasome", INHIB, size=sz).move_to(P(p3x, -2.2))
        self.at("same enzymes")
        self.play(FadeIn(h1, shift=UP * 0.1), FadeIn(s1, scale=0.6), FadeIn(k9), FadeIn(k3), run_time=0.8)
        self.at("two")
        self.play(FadeIn(h2, shift=UP * 0.1), FadeIn(tl), FadeIn(tg), FadeIn(la), FadeIn(l9), FadeIn(l3), FadeIn(l6),
                  FadeIn(ga), FadeIn(g9), FadeIn(g3), run_time=0.8)
        self.play(Create(lxx), Create(j9), Create(j3), run_time=0.5)
        self.at("and an inhibitor")
        self.play(FadeIn(h3, shift=UP * 0.1), FadeIn(body, scale=0.6), FadeIn(bl), run_time=0.6)
        self.play(Create(shield), FadeIn(xi), FadeIn(pc), run_time=0.7)
        self.finish()


class S31End(EndCard):
    LINE = "Same enzymes, two wirings, an inhibitor\nguarding the part that must live."
