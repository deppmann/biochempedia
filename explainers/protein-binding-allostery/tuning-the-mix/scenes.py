"""Tuning the Mix  (Biochemistrypedia: Protein binding & allostery, chapter 5)

COLOR MAP (one color per concept, whole series; taken from scenes.old.py and chapter 1)
  BLUE   = hemoglobin / protein, and the T (tense, weak-grip) shape
  GREEN  = the R (relaxed, tight-grip) shape
  YELLOW = O2, the ligand, and the P50 marker
  RED    = loss (oxygen not loaded); a cross
  TEAL   = 2,3-BPG
  GOLD   = call-outs, salt bridges, titles of effects
  TEXT   = neutral labels;  GREY = axes, secondary labels, ghosts of the old curve
  Added here: ACID (orange) = H+ and low pH;  CO2C (lavender) = carbon dioxide and carbamate;
  FETAL (pink) = fetal hemoglobin;  CELL/LUNGC/MUSC = red cell, lung and muscle pictures (as chapter 1).
Curves are computed: hemoglobin Y = x^n/(P50^n + x^n), P50 = 26.4 torr, n = 2.8 (shifted copies change P50 only:
BPG 35, acid in muscle 36, a very large BPG shift 52, fetal 19 torr). The T/R bar comes from the two-state
(MWC) model, L = 1000, c = 0.01, KR = 5 torr, at 26.4 torr; a T-favouring regulator multiplies L by 3.5.
NO molecular structures are drawn: blocks, chips, balls, bars and curves only.
"""
import numpy as np

from bp_style import *

# ------------------------------------------------------------------ colours and numbers
ACID = "#F28C28"
CO2C = "#B48EDE"
FETAL = "#FF8FB8"
TEAL_ = TEAL
CELL = "#E5566A"
LUNGC = "#E58FB0"
MUSC = "#C9754F"

P50, NH = 26.4, 2.8
KR, LL, CC = 5.0, 1000.0, 0.01
P_MODEST, P_ACID, P_LARGE, P_FETAL = 35.0, 36.0, 52.0, 19.0


def hill(x, p50=P50, n=NH):
    return x ** n / (p50 ** n + x ** n)


def mwc_r(p, L=LL):
    """Fraction of molecules in R at pressure p (two-state model)."""
    a = p / KR
    r = (1 + a) ** 4
    t = L * (1 + CC * a) ** 4
    return r / (r + t)


FR0 = mwc_r(P50)               # about 0.55
FR_T = mwc_r(P50, LL * 3.5)    # tipped toward T, about 0.29


# ------------------------------------------------------------------ pictures and parts
GREEK = "Helvetica Neue"   # a font with real alpha, beta, gamma glyphs (Avenir draws gamma like a Y)


def G(text, size=30, color=TEXT, **kw):
    """Text that contains Greek chain letters."""
    return T(text, size, color, font=GREEK, **kw)


def o2(r=0.27):
    c = Circle(radius=r, color=YELLOW, fill_opacity=1, stroke_width=0)
    return VGroup(c, T("O₂", 22, BG, weight=BOLD).move_to(c))


def ball(label, color, r=0.3, size=22, text_color=BG):
    c = Circle(radius=r, color=color, fill_opacity=1, stroke_width=0)
    return VGroup(c, T(label, size, text_color, weight=BOLD).move_to(c))


def bpg_ball(r=0.45, label=True):
    c = Circle(radius=r, color=TEAL, fill_opacity=0.95, stroke_width=0)
    g = VGroup(c)
    if label:
        g.add(T("BPG", 24, BG, weight=BOLD).move_to(c))
    return g


def lung_pic(x, y=-0.2):
    sh = VGroup()
    for dx in (-1.0, 1.0):
        sh.add(Ellipse(width=1.95, height=3.0, stroke_color=LUNGC, stroke_width=3,
                       fill_color=LUNGC, fill_opacity=0.28).shift(RIGHT * dx))
    sh.add(Line(UP * 1.85, UP * 0.8, color=LUNGC, stroke_width=5))
    sh.add(Line(UP * 0.8, LEFT * 0.9 + UP * 0.3, color=LUNGC, stroke_width=4))
    sh.add(Line(UP * 0.8, RIGHT * 0.9 + UP * 0.3, color=LUNGC, stroke_width=4))
    lab = T("lungs", 28, LUNGC).move_to(DOWN * 1.9)
    return VGroup(sh, lab).move_to([x, y, 0])


def muscle_pic(x, y=-0.2):
    r = RoundedRectangle(corner_radius=0.3, width=4.2, height=3.0, stroke_color=MUSC, stroke_width=3,
                         fill_color=MUSC, fill_opacity=0.28)
    fib = VGroup(*[Line(LEFT * 1.9, RIGHT * 1.9, color=MUSC, stroke_width=2).set_opacity(0.5).shift(UP * yy)
                   for yy in (-0.9, -0.3, 0.3, 0.9)])
    lab = T("muscle", 28, MUSC).move_to(DOWN * 1.9)
    return VGroup(VGroup(r, fib), lab).move_to([x, y, 0])


def cell_pic(r=0.62, color=CELL):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.55)
    d = Circle(radius=r * 0.42, stroke_width=0, fill_color=BG, fill_opacity=0.35)
    return VGroup(c, d)


def cell_dots(center, n=4, r=0.62, dr=0.11):
    out = VGroup()
    for k in range(n):
        ang = PI / 4 + k * PI / 2
        out.add(Circle(radius=dr, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
                .move_to(center + np.array([np.cos(ang), np.sin(ang), 0]) * r * 0.78))
    return out


def pulse_fibres(ph, half, ys, w0=5, color=MUSC, shrink=0.12, thick=4):
    """Muscle fibres that shorten and thicken as the tracker ph runs (a contraction every 2 s)."""
    s = 0.5 - 0.5 * np.cos(ph.get_value() * TAU)
    h = half * (1 - shrink * s)
    return VGroup(*[Line([-h, y, 0], [h, y, 0], color=color, stroke_width=w0 + thick * s).set_opacity(0.65) for y in ys])


def start_pulse(scene, rate=0.5):
    ph = ValueTracker(0)
    ph.add_updater(lambda m, dt: m.increment_value(dt * rate))
    scene.add(ph)
    return ph


def hbcart(cx, cy, size=1.3, g=0.3, color=BLUE, labels=("α", "β", "β", "α"), op=0.22, lsize=30,
           colors=None):
    """Four labelled blocks round a central gap (a cartoon, not a structure). Beta chains sit on the diagonal."""
    d = (size + g) / 2
    out = VGroup()
    for i, ((x, y), lab) in enumerate(zip([(-d, d), (d, d), (-d, -d), (d, -d)], labels)):
        col = colors[i] if colors else color
        r = RoundedRectangle(corner_radius=0.14, width=size, height=size, stroke_color=col, stroke_width=3,
                             fill_color=col, fill_opacity=op)
        out.add(VGroup(r, G(lab, lsize, col).move_to(r)).move_to([cx + x, cy + y, 0]))
    return out


def pocket_cart(cx, cy, size, g, e, color=BLUE, lsize=32, op=0.22):
    """Tetramer cartoon whose beta blocks (top right, bottom left) sit e further out along the diagonal,
    so the central pocket reads as lying between the two beta chains."""
    d = (size + g) / 2
    pos = [(-d, d), (d + e, d + e), (-d - e, -d - e), (d, -d)]
    out = VGroup()
    for (x, y), lab in zip(pos, ("α", "β", "β", "α")):
        r = RoundedRectangle(corner_radius=0.14, width=size, height=size, stroke_color=color, stroke_width=3,
                             fill_color=color, fill_opacity=op)
        out.add(VGroup(r, G(lab, lsize, color).move_to(r)).move_to([cx + x, cy + y, 0]))
    return out


def bpg_pill(cx, cy, length, thick=0.62):
    p = RoundedRectangle(corner_radius=thick / 2, width=length, height=thick, stroke_width=0,
                         fill_color=TEAL, fill_opacity=0.95)
    p.rotate(PI / 4).move_to([cx, cy, 0])
    return p


def popbar(fr, cx, cy, w, h):
    """T (blue) on the left, R (green) on the right, R share = fr."""
    g = VGroup()
    wt, wr = w * (1 - fr), w * fr
    left = cx - w / 2
    if wt > 0.01:
        g.add(Rectangle(width=wt, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.85)
              .move_to([left + wt / 2, cy, 0]))
        if wt > 0.8:
            g.add(T("T", 34, BG, weight=BOLD).move_to([left + wt / 2, cy, 0]))
    if wr > 0.01:
        g.add(Rectangle(width=wr, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
              .move_to([left + wt + wr / 2, cy, 0]))
        if wr > 0.8:
            g.add(T("R", 34, BG, weight=BOLD).move_to([left + wt + wr / 2, cy, 0]))
    return g


BAR_X, BAR_Y, BAR_W, BAR_H = 0.0, -2.1, 10.4, 0.9


def mix_cap(y=BAR_Y):
    return T("the mix of shapes", 26, GREY).move_to([BAR_X, y + BAR_H / 2 + 0.38, 0])


def mix_bar(scene, fr, y=BAR_Y, fade=True, w=BAR_W):
    """Add the T/R bar to the scene driven by a tracker; returns the tracker."""
    tr = ValueTracker(fr)
    if fade:
        st = popbar(fr, BAR_X, y, w, BAR_H)
        scene.play(FadeIn(st), run_time=0.5)
        scene.remove(st)
    bar = always_redraw(lambda: popbar(tr.get_value(), BAR_X, y, w, BAR_H))
    scene.add(bar)
    return tr, bar


def mk_axes(w, h, center, xt=((50, "50"), (100, "100")), yt=((0.5, "0.5"), (1, "1")),
            xlab="oxygen pressure (torr)", ylab="fraction bound"):
    ax = Axes(x_range=[0, 100, 100], y_range=[0, 1, 1], x_length=w, y_length=h, tips=False,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 3})
    ax.move_to(center)
    deco = VGroup()
    for v, lab in xt:
        deco.add(M(lab, 26, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.15))
    for v, lab in yt:
        deco.add(M(lab, 26, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.15))
    deco.add(M("0", 26, GREY).next_to(ax.c2p(0, 0), DL, buff=0.1))
    deco.add(T(xlab, 26, GREY).next_to(ax.x_axis, DOWN, buff=0.68))
    deco.add(T(ylab, 26, GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=1.0))
    return ax, deco


def axes_c():
    return mk_axes(8.2, 4.8, [-0.6, 0.1, 0])


def axes_l():
    return mk_axes(6.2, 4.8, [-2.0, 0.1, 0])


def axes_r():
    return mk_axes(5.8, 4.8, [3.3, 0.0, 0])


def cv(ax, p50, color, n=NH, w=5):
    return ax.plot(lambda x: hill(x, p50, n), x_range=[0, 100, 0.5], color=color, stroke_width=w)


def p50_marker(ax, p50, color=YELLOW):
    y = 0.5
    return VGroup(DashedLine(ax.c2p(0, y), ax.c2p(p50, y), color=color, stroke_width=3),
                  DashedLine(ax.c2p(p50, 0), ax.c2p(p50, y), color=color, stroke_width=3),
                  Dot(ax.c2p(p50, y), color=color, radius=0.13))


def dotat(ax, x, p50, color, r=0.11):
    return Dot(ax.c2p(x, hill(x, p50)), color=color, radius=r)


def plus_badge(label, pos, color=GOLD):
    c = Circle(radius=0.22, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(c, T(label, 28, color, weight=BOLD).move_to(c)).move_to(pos)


# ---- the cartoon with its attached groups (scenes 10, 11, 13)
CX, CY, CSZ, CGAP = -2.3, 0.8, 2.15, 0.3
CD = (CSZ + CGAP) / 2


def main_cart(color=BLUE):
    return hbcart(CX, CY, CSZ, CGAP, color=color, lsize=34)


def blk_pos(i):
    return np.array([[CX - CD, CY + CD, 0], [CX + CD, CY + CD, 0], [CX - CD, CY - CD, 0], [CX + CD, CY - CD, 0]][i])


class Sc(SpokenScene):
    pass


# ---------------------------------------------------------------- cards
class S00Title(TitleCard):
    LESSON = "Protein Binding and Allostery: How Hemoglobin Loads and Delivers Oxygen"
    TITLE = "Tuning the Mix"


class S24End(EndCard):
    LINE = "Acid, CO₂ and BPG favor T, so they shift the mix where oxygen must let go."

    def construct(self):
        a = MarkupText("Acid, CO<sub>2</sub> and BPG favor T, so they shift", font=TITLE_FONT, font_size=38)
        b = T("the mix where oxygen must let go.", 38, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.28)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=24, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.55)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()


# ---------------------------------------------------------------- 1: the question
class S01Q(Sc):
    def construct(self):
        ph = start_pulse(self, 0.5)
        vessel = RoundedRectangle(corner_radius=0.9, width=12.4, height=2.8, stroke_color=CELL, stroke_width=3,
                                  fill_color=CELL, fill_opacity=0.10).move_to([0, -2.45, 0])
        mbox = RoundedRectangle(corner_radius=0.35, width=11.6, height=2.8, stroke_color=MUSC, stroke_width=3,
                                fill_color=MUSC, fill_opacity=0.26).move_to([0, 1.1, 0])
        fibs = always_redraw(lambda: pulse_fibres(ph, 5.3, (0.2, 0.65, 1.1, 1.55), w0=4, shrink=0.3, thick=9))
        mlab = T("working muscle", 30, MUSC).move_to([-4.0, 2.15, 0])
        q = T("How does the blood know?", 48, YELLOW).move_to([0, 3.25, 0])
        cell = cell_pic(1.3).move_to([-4.8, -2.45, 0])
        dots = cell_dots(cell.get_center(), 4, 1.3, 0.22)
        cg = VGroup(cell, dots)
        self.add(fibs)
        self.play(FadeIn(vessel), FadeIn(mbox), FadeIn(mlab), FadeIn(q), FadeIn(cg), run_time=0.6)
        self.play(cg.animate.move_to([-1.3, -2.45, 0]), run_time=3.4, rate_func=linear)
        self.at("let go of")
        out = VGroup(*[o2().move_to(d.get_center()) for d in dots])
        self.play(FadeOut(dots), FadeIn(out), run_time=0.15)
        spots = [(-2.9, 0.1), (-1.7, 0.55), (-0.5, 0.1), (0.7, 0.55)]
        self.play(*[o.animate.move_to([x, y, 0]) for o, (x, y) in zip(out, spots)], run_time=1.1)
        self.finish()


# ---------------------------------------------------------------- 2: the rule
def tcart(cx, cy, g=0.95, size=1.25):
    return hbcart(cx, cy, size, g, color=BLUE, lsize=28)


def rcart(cx, cy, g=0.1, size=1.25):
    return hbcart(cx, cy, size, g, color=GREEN, lsize=28)


class S02Rule(Sc):
    def construct(self):
        tc, rc = tcart(-3.6, 1.05), rcart(3.6, 1.05)
        tl = T("T shape", 32, BLUE).move_to([-3.6, -1.15, 0])
        rl = T("R shape", 32, GREEN).move_to([3.6, -1.15, 0])
        cap = mix_cap()
        st = popbar(FR0, BAR_X, BAR_Y, BAR_W, BAR_H)
        self.play(FadeIn(tc), FadeIn(rc), FadeIn(tl), FadeIn(rl), FadeIn(st), FadeIn(cap), run_time=0.7)
        self.remove(st)
        tr = ValueTracker(FR0)
        bar = always_redraw(lambda: popbar(tr.get_value(), BAR_X, BAR_Y, BAR_W, BAR_H))
        self.add(bar)
        self.at("anything that binds")
        rule = T("binds T better, so the mix shifts toward T", 32, GOLD).move_to([0, 3.35, 0])
        q = ball("?", GREY, 0.42, 40).move_to([0, 1.05, 0])
        self.play(FadeIn(q, scale=0.6), FadeIn(rule, shift=DOWN * 0.1), run_time=0.5)
        self.at("one shape")
        self.play(q.animate.move_to([-3.6, 1.05, 0]), run_time=0.9)
        self.play(q[0].animate.set_fill(TEAL), run_time=0.2)
        self.at("shifts the mix")
        self.play(tr.animate.set_value(FR_T), run_time=2.2)
        self.finish()


# ---------------------------------------------------------------- 3: three regulators
REG_X = [-4.3, -1.8, 0.4]
REG_BY = -1.7


def reg_arrows(chips, sw):
    return [Arrow([x, 0.75, 0], [x, REG_BY + BAR_H / 2 + 0.03, 0], color=c[0].get_color(), buff=0, stroke_width=sw)
            for x, c in zip(REG_X, chips)]


class S03Three(Sc):
    def construct(self):
        tr, bar = mix_bar(self, FR0, y=REG_BY, fade=True)
        cap = T("the mix of shapes", 26, GREY).move_to([0, REG_BY - 0.85, 0])
        self.add(cap)
        head = VGroup(T("Three regulators prefer", 46), T("T", 46, BLUE)).arrange(RIGHT, buff=0.2).move_to([0, 3.05, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        chips = [chip("acid (H⁺)", ACID, 40), chip("CO₂", CO2C, 40), chip("BPG", TEAL, 40)]
        for c, x in zip(chips, REG_X):
            c.move_to([x, 1.4, 0])
        arrows = reg_arrows(chips, 7)
        levels = [FR0, FR0 - (FR0 - FR_T) / 3, FR0 - 2 * (FR0 - FR_T) / 3, FR_T]
        for i, nm in enumerate(["acid", "carbon dioxide", "bpg"]):
            self.at(nm)
            self.play(FadeIn(chips[i], shift=DOWN * 0.3), GrowArrow(arrows[i]), run_time=0.6)
            self.play(tr.animate.set_value(levels[i + 1]), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- 4: BPG
class S04Bpg(Sc):
    def construct(self):
        name = T("2,3-bisphosphoglycerate", 48, TEAL).move_to([0, 3.15, 0])
        b = bpg_ball(1.25).move_to([0, 0.1, 0])
        b[1].scale(1.7)
        self.play(Write(name, run_time=1.9), FadeIn(b, scale=0.6, run_time=0.6))
        self.at("small anion")
        ln = Line([1.45, 0.1, 0], [3.0, 0.1, 0], color=TEAL, stroke_width=4)
        sm = T("small anion", 42, TEAL).move_to([4.6, 0.1, 0])
        self.play(FadeIn(sm, shift=LEFT * 0.2), Create(ln), run_time=0.5)
        self.at("about")
        angs = [90, 18, -54, -126, 162]
        chg = VGroup(*[plus_badge("−", [1.95 * np.cos(a * DEGREES), 0.1 + 1.95 * np.sin(a * DEGREES), 0], TEAL)
                       for a in angs])
        for c in chg:
            c.scale(1.25)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in chg], lag_ratio=0.3), run_time=1.1)
        self.at("negative charges")
        lab = T("about 4 to 5 negative charges", 38, TEAL).move_to([0, -3.0, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- 5: one per hemoglobin
def mini_hb(color=BLUE, s=0.34):
    return hbcart(0, 0, s, 0.08, color=color, labels=("", "", "", ""), op=0.35, lsize=10).scale(1.0)


class S05Amount(Sc):
    def construct(self):
        cc = np.array([-1.6, -0.1, 0])
        cell = Circle(radius=3.1, stroke_color=CELL, stroke_width=4, fill_color=CELL, fill_opacity=0.16).move_to(cc)
        self.at("red cells")
        self.play(FadeIn(cell, scale=0.8), run_time=0.7)
        rows = [1.5, 0.0, -1.5]
        cols = [-1.0, 1.0]
        pairs = [(cc[0] + dx * 1.0 + (0.0), cc[1] + dy) for dy in rows for dx in cols]
        bp = VGroup(*[Circle(radius=0.26, stroke_width=0, fill_color=TEAL, fill_opacity=0.95).move_to([x - 0.5, y, 0])
                      for x, y in pairs])
        hb = VGroup(*[mini_hb().move_to([x + 0.5, y, 0]) for x, y in pairs])
        legb = VGroup(Circle(radius=0.26, stroke_width=0, fill_color=TEAL, fill_opacity=0.95), T("BPG", 32, TEAL)).arrange(RIGHT, buff=0.3).move_to([4.4, 1.3, 0])
        legb.align_to([2.3, 0, 0], LEFT)
        legh = VGroup(mini_hb(), T("hemoglobin", 32, BLUE)).arrange(RIGHT, buff=0.3).move_to([4.4, 0.1, 0])
        legh.align_to(legb, LEFT)
        self.at("one bpg")
        self.play(LaggedStart(*[FadeIn(b, scale=0.3) for b in bp], lag_ratio=0.12), FadeIn(legb), run_time=1.0)
        self.at("every hemoglobin")
        self.play(LaggedStart(*[FadeIn(h, scale=0.3) for h in hb], lag_ratio=0.12), FadeIn(legh), run_time=1.0)
        ratio = M("nearly 1 : 1", 36, GOLD).move_to([4.2, -1.6, 0])
        self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- 6: the pocket
P_SZ, P_GT, P_ET = 1.9, 0.8, 0.5     # T state: block size, gap, extra outward shift of the beta blocks
P_X, P_Y = -2.1, -0.1


class S06Pocket(Sc):
    def construct(self):
        tcr = pocket_cart(P_X, P_Y, P_SZ, P_GT, P_ET, color=BLUE, lsize=36)
        state = T("T shape", 36, BLUE).move_to([4.3, 2.3, 0])
        ball_ = bpg_ball(0.4).move_to([P_X + 0.25, P_Y + 3.35, 0])
        self.play(FadeIn(tcr), FadeIn(state), FadeIn(ball_), run_time=0.4)
        self.play(ball_.animate.move_to([P_X, P_Y, 0]), run_time=0.5)
        pill = bpg_pill(P_X, P_Y, 2.45)
        self.play(ReplacementTransform(ball_[0], pill), run_time=0.4)
        self.at("central pocket")
        lab = T("central pocket", 34, TEAL).move_to([4.3, 1.0, 0])
        ar = Arrow(lab.get_left() + LEFT * 0.1, [P_X + 0.55, P_Y - 0.05, 0], color=TEAL, buff=0.05, stroke_width=5)
        self.play(FadeIn(lab, shift=LEFT * 0.15), GrowArrow(ar), run_time=0.6)
        self.at("beta chains")
        self.play(Indicate(tcr[1], color=BLUE, scale_factor=1.06), Indicate(tcr[2], color=BLUE, scale_factor=1.06),
                  run_time=1.0)
        self.at("that pocket")
        wide = T("wide open", 36, BLUE).move_to([4.3, -0.4, 0])
        self.play(FadeIn(wide, shift=UP * 0.1), run_time=0.4)
        self.at("only in")
        # the pocket closes: BPG leaves up the open channel first, then the four blocks squeeze together
        rcr = pocket_cart(P_X, P_Y, P_SZ, 0.1, 0.0, color=GREEN, lsize=36)
        rstate = T("R shape", 36, GREEN).move_to([4.3, 2.3, 0])
        narrow = T("R: pocket narrows", 36, GREEN).move_to([4.3, -0.4, 0])
        exit_ball = bpg_ball(0.4, label=False).move_to([P_X + 0.25, P_Y + 3.3, 0])
        self.play(FadeOut(ar), FadeOut(lab), Transform(pill, exit_ball), ball_[1].animate.move_to([P_X + 0.25, P_Y + 3.3, 0]),
                  run_time=0.6)
        out = VGroup(pill, ball_[1])
        pushes = VGroup()
        for sx, sy, i in [(-1, 1, 0), (1, 1, 1), (-1, -1, 2), (1, -1, 3)]:
            c = rcr[i].get_center()
            p0 = c + np.array([sx, sy, 0]) * 1.65
            p1 = c + np.array([sx, sy, 0]) * 1.25
            pushes.add(Arrow(p0, p1, color=GREEN, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.5))
        self.play(ReplacementTransform(tcr, rcr), ReplacementTransform(state, rstate),
                  ReplacementTransform(wide, narrow), FadeIn(pushes), run_time=0.9)
        sq = T("BPG pushed out", 30, TEAL).next_to(out, RIGHT, buff=0.3)
        self.play(FadeIn(sq), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------- 7 and 8: the question
PLBL = np.array([31, 0.33])


def predict_mobs():
    ax, deco = axes_l()
    curve = cv(ax, P50, BLUE)
    mk = p50_marker(ax, P50)
    mk_lab = T("P50 = 26 torr", 26, YELLOW).move_to(ax.c2p(32, 0.3), aligned_edge=LEFT)
    tag = chip("PREDICT", GOLD, 30).move_to([4.3, 3.0, 0])
    add = chip("Add BPG", TEAL, 42).move_to([4.3, 1.4, 0])
    q = VGroup(T("Which way", 42), T("does P50 move?", 42)).arrange(DOWN, buff=0.2).move_to([4.3, -0.5, 0])
    return ax, deco, curve, mk, mk_lab, tag, add, q


class S07Predict(Sc):
    def construct(self):
        ax, deco, curve, mk, mk_lab, tag, add, q = predict_mobs()
        self.play(FadeIn(tag, shift=DOWN * 0.2), Create(ax), FadeIn(deco), run_time=0.6)
        self.play(Create(curve), run_time=0.6)
        self.play(FadeIn(mk), FadeIn(mk_lab), run_time=0.4)
        self.at("add bpg")
        self.play(FadeIn(add, shift=DOWN * 0.2), run_time=0.5)
        self.at("which way")
        self.play(Write(q), run_time=1.4)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        ax, deco, curve, mk, mk_lab, tag, add, q = predict_mobs()
        self.add(ax, deco, curve, mk, mk_lab, tag, add, q)
        self.finish()


# ---------------------------------------------------------------- 9: the answer
class S09Reveal(Sc):
    def construct(self):
        ax, deco, curve, mk, mk_lab, tag, add, q = predict_mobs()
        self.add(ax, deco, curve, mk, mk_lab, tag, add, q)
        ans = T("P50 goes up", 46, TEAL).move_to([4.3, 3.4, 0])
        self.play(FadeOut(tag), FadeOut(add), FadeOut(q), FadeIn(ans, shift=DOWN * 0.15), run_time=0.6)
        ccx, ccy, s, g, e = 4.3, 0.2, 1.3, 0.6, 0.35
        cart = pocket_cart(ccx, ccy, s, g, e, color=BLUE, lsize=28)
        tlab = T("T shape", 32, BLUE).move_to([ccx, ccy - 2.3, 0])
        self.play(FadeIn(cart), FadeIn(tlab), run_time=0.6)
        bp = bpg_ball(0.3, label=False).move_to([ccx + 0.1, ccy + 2.2, 0])
        self.at("bpg")
        self.play(FadeIn(bp, scale=0.5), run_time=0.3)
        pill = bpg_pill(ccx, ccy, 1.8, 0.45)
        self.play(bp.animate.move_to([ccx, ccy, 0]), run_time=0.5)
        self.play(ReplacementTransform(bp, pill), run_time=0.2)
        bl = T("BPG", 30, TEAL).move_to([ccx + 0.2, ccy + 2.45, 0])
        bar_ = Arrow(bl.get_bottom() + DOWN * 0.05, [ccx + 0.1, ccy + 0.35, 0], color=TEAL, buff=0.05, stroke_width=5)
        self.play(FadeIn(bl), GrowArrow(bar_), run_time=0.4)
        self.at("like a doorstop")
        pushes = VGroup()
        for sx, sy, i in [(-1, 1, 0), (1, 1, 1), (-1, -1, 2), (1, -1, 3)]:
            c = cart[i].get_center()
            p0 = c + np.array([sx, sy, 0]) * 1.2
            p1 = c + np.array([sx, sy, 0]) * 0.85
            pushes.add(Arrow(p0, p1, color=GREEN, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.5))
        stop = T("a doorstop", 34, TEAL).move_to([ccx, ccy - 2.3, 0])
        self.play(FadeIn(pushes), FadeIn(stop), FadeOut(tlab), run_time=0.7)
        self.at("it takes more oxygen")
        more = T("more O₂ to tip the mix", 30, YELLOW).move_to([ccx, ccy - 2.95, 0])
        self.play(FadeIn(more, shift=UP * 0.1), run_time=0.5)
        self.at("so the curve shifts")
        ghost = cv(ax, P50, GREY, w=3).set_stroke(opacity=0.7).set_fill(opacity=0)
        self.add(ghost)
        new = cv(ax, P_MODEST, TEAL)
        newmk = p50_marker(ax, P_MODEST)
        newlab = VGroup(T("P50 moves up:", 26, YELLOW), T("26 → about 35 torr", 26, YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        newlab.move_to(ax.c2p(41, 0.3), aligned_edge=LEFT)
        self.play(FadeOut(mk_lab), run_time=0.3)
        self.play(Transform(curve, new), Transform(mk, newmk), run_time=1.3)
        self.play(FadeIn(newlab), run_time=0.4)
        gl = T("without BPG", 26, GREY).move_to(ax.c2p(78, 0.16))
        self.play(FadeIn(gl), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------- 10: the Bohr effect
HIS_TR = np.array([CX + CD + CSZ / 2 + 0.15 + 0.55, CY + CD, 0])     # right of the top-right beta block
HIS_BL = np.array([CX - CD - CSZ / 2 - 0.15 - 0.55, CY - CD, 0])     # left of the bottom-left beta block
BAR13_Y = -2.65


def his_chip(label="His", color=GREY):
    return chip(label, color, 26, pad=0.16)


class S10Bohr(Sc):
    def construct(self):
        sz, gp, cx, cy = 2.7, 0.38, 0.0, -0.1
        dd = (sz + gp) / 2
        cart = hbcart(cx, cy, sz, gp, color=BLUE, lsize=42)
        tr_pos = np.array([cx + dd + sz / 2 + 0.7, cy + dd, 0])
        bl_pos = np.array([cx - dd - sz / 2 - 0.7, cy - dd, 0])
        h1 = his_chip().move_to(tr_pos)
        h2 = his_chip().move_to(bl_pos)
        cl = VGroup(*[ball("H⁺", ACID, 0.36, 28) for _ in range(4)])
        pos = [(5.0, -0.6), (6.2, -1.3), (4.9, -2.0), (6.2, -2.8)]
        for b, p in zip(cl, pos):
            b.move_to([p[0], p[1], 0])
        acid = T("acid: H⁺ ions", 32, ACID).move_to([5.6, 0.3, 0])
        self.play(FadeIn(cart), FadeIn(h1), FadeIn(h2), FadeIn(cl, scale=0.5), FadeIn(acid), run_time=0.6)
        bohr = T("the Bohr effect", 40, GOLD).move_to([-4.2, 3.4, 0])
        self.at("bohr effect")
        self.play(FadeIn(bohr, shift=UP * 0.1), run_time=0.5)
        self.at("protons add")
        p1, p2 = cl[0], cl[3]
        self.play(p1.animate.move_to(h1.get_center()).scale(0.8), run_time=0.8)
        k1 = his_chip("His⁺", ACID).move_to(tr_pos)
        self.play(ReplacementTransform(h1, k1), FadeOut(p1), run_time=0.4)
        path2 = VMobject().set_points_smoothly([p2.get_center(), np.array([3.0, -3.3, 0]), np.array([-1.5, -3.5, 0]),
                                                 np.array([-5.2, -3.0, 0]), bl_pos + DOWN * 0.1])
        self.play(MoveAlongPath(p2, path2), run_time=1.1)
        k2 = his_chip("His⁺", ACID).move_to(bl_pos)
        self.play(ReplacementTransform(h2, k2), FadeOut(p2), run_time=0.4)
        self.at("histidine")
        hl = VGroup(G("histidine near", 28, ACID), G("each β chain end", 28, ACID)).arrange(DOWN, buff=0.1).move_to([5.2, 2.9, 0])
        la = Arrow(hl.get_bottom() + DOWN * 0.05, k1.get_top() + UP * 0.05 + RIGHT * 0.2, color=ACID, buff=0.05, stroke_width=4)
        self.play(FadeIn(hl, shift=DOWN * 0.1), GrowArrow(la), run_time=0.5)
        self.at("end of each")
        self.play(Indicate(cart[1], color=BLUE, scale_factor=1.05), Indicate(cart[2], color=BLUE, scale_factor=1.05),
                  run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- 11: salt bridges
class S11Bohr2(Sc):
    def construct(self):
        cart = main_cart()
        k1 = his_chip("His⁺", ACID).move_to(HIS_TR)
        k2 = his_chip("His⁺", ACID).move_to(HIS_BL)
        cap = mix_cap(BAR13_Y)
        self.add(cart, k1, k2, cap)
        tr, bar = mix_bar(self, FR0, y=BAR13_Y, fade=False)
        a1 = chip("Asp −", GOLD, 22, pad=0.12).move_to(blk_pos(1) + np.array([-0.3, -0.62, 0]))
        a2 = chip("Asp −", GOLD, 22, pad=0.12).move_to(blk_pos(2) + np.array([0.0, -0.66, 0]))
        l1 = DashedLine(k1.get_left() + DOWN * 0.15, a1.get_right(), color=GOLD, stroke_width=4)
        l2 = DashedLine(k2.get_right() + DOWN * 0.15, a2.get_left(), color=GOLD, stroke_width=4)
        self.at("salt bridges")
        sb = T("salt bridges", 36, GOLD).move_to([4.3, 0.8, 0])
        self.play(FadeIn(a1), FadeIn(a2), Create(l1), Create(l2), FadeIn(sb), run_time=0.9)
        self.at("steady")
        self.play(Indicate(cart, color=BLUE, scale_factor=1.03), tr.animate.set_value(0.4), run_time=0.9)
        lab = VGroup(T("low pH", 40, ACID), T("lower O₂ affinity", 40)).arrange(DOWN, buff=0.12).move_to([4.3, 2.4, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), tr.animate.set_value(FR_T), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------- 12: working muscle
def gauge(x, level, color, name, val):
    fr = Rectangle(width=0.9, height=3.6, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([x, -0.1, 0])
    fill = Rectangle(width=0.9, height=3.6 * level, stroke_width=0, fill_color=color, fill_opacity=0.9)
    fill.align_to(fr, DOWN).align_to(fr, LEFT)
    nm = T(name, 30, color).move_to([x, -2.35, 0])
    v = M(val, 30, color).move_to([x, 2.3, 0])
    return fr, fill, nm, v


class S12Muscle(Sc):
    def construct(self):
        ax, deco = mk_axes(6.0, 4.6, [3.2, -0.3, 0])
        curve = cv(ax, P50, BLUE)
        fr1, fl1, nm1, v1 = gauge(-5.6, 0.62, BLUE, "lungs", "pH 7.4")
        fr2, fl2, nm2, v2 = gauge(-3.3, 0.62, MUSC, "muscle", "pH 7.4")
        sw1 = Line([0.0, 3.5, 0], [0.55, 3.5, 0], color=BLUE, stroke_width=6)
        lg1 = T("lung blood (pH 7.4)", 26, BLUE).next_to(sw1, RIGHT, buff=0.2)
        sw2 = Line([0.0, 3.0, 0], [0.55, 3.0, 0], color=ACID, stroke_width=6)
        lg2 = T("working-muscle blood (lower pH)", 26, ACID).next_to(sw2, RIGHT, buff=0.2)
        self.play(FadeIn(fr1), FadeIn(fl1), FadeIn(nm1), FadeIn(v1), FadeIn(fr2), FadeIn(fl2), FadeIn(nm2), FadeIn(v2),
                  Create(ax), FadeIn(deco), run_time=0.6)
        self.play(Create(curve), FadeIn(sw1), FadeIn(lg1), run_time=0.5)
        self.at("makes acid")
        v2b = M("pH lower", 28, ACID).move_to([-3.3, 2.3, 0])
        fl2b = fl2.copy().stretch_to_fit_height(3.6 * 0.38, about_edge=DOWN).set_fill(ACID, 0.9)
        fl2b.align_to(fr2, DOWN).align_to(fr2, LEFT)
        self.play(Transform(fl2, fl2b), ReplacementTransform(v2, v2b), nm2.animate.set_color(ACID), run_time=1.2)
        self.at("acid tips")
        new = cv(ax, P_ACID, ACID)
        self.play(TransformFromCopy(curve, new), FadeIn(sw2), FadeIn(lg2), run_time=1.3)
        self.at("where")
        vl = DashedLine(ax.c2p(20, 0), ax.c2p(20, 1), color=MUSC, stroke_width=3)
        dm = dotat(ax, 20, P50, BLUE, 0.14)
        da = dotat(ax, 20, P_ACID, ACID, 0.14)
        self.play(Create(vl), FadeIn(dm), FadeIn(da), run_time=0.8)
        self.at("straining muscle")
        ml = T("muscle", 28, MUSC).move_to(ax.c2p(20, 1.0) + UP * 0.4)
        self.play(FadeIn(ml), run_time=0.4)
        self.at("needs the oxygen")
        gap = Line(dm.get_center(), da.get_center(), color=YELLOW, stroke_width=8)
        more = T("more O₂ let go", 28, YELLOW).move_to(ax.c2p(60, 0.09))
        la = Arrow(da.get_center() + RIGHT * 0.2 + DOWN * 0.04, more.get_left() + LEFT * 0.1, color=YELLOW, buff=0.0, stroke_width=4)
        self.play(Create(gap), FadeIn(more), GrowArrow(la), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- 13: carbon dioxide
C13X, C13Y, C13S, C13G = 0.3, 0.7, 1.9, 0.3
C13D = (C13S + C13G) / 2


def cart13():
    return hbcart(C13X, C13Y, C13S, C13G, color=BLUE, lsize=34)


def b13(i):
    return np.array([[C13X - C13D, C13Y + C13D, 0], [C13X + C13D, C13Y + C13D, 0],
                     [C13X - C13D, C13Y - C13D, 0], [C13X + C13D, C13Y - C13D, 0]][i])


class S13Co2(Sc):
    def construct(self):
        cart = cart13()
        y13 = -2.6
        cap = mix_cap(y13)
        self.add(cart, cap)
        tr, bar = mix_bar(self, FR0, y=y13, fade=False)
        ya, yb = b13(0)[1] + 0.45, b13(2)[1] - 0.45
        ce1 = chip("chain end", GREY, 24, pad=0.16).move_to([-2.85, ya, 0])
        ce2 = chip("chain end", GREY, 24, pad=0.16).move_to([-2.85, yb, 0])
        cl = VGroup(*[ball("CO₂", CO2C, 0.42, 22) for _ in range(3)])
        for b, p in zip(cl, [(4.0, 2.4), (5.6, 1.2), (4.1, -0.2)]):
            b.move_to([p[0], p[1], 0])
        self.play(FadeIn(ce1), FadeIn(ce2), FadeIn(cl, scale=0.5), run_time=0.6)
        self.at("binds")
        k1p, k2p = np.array([-5.4, ya, 0]), np.array([-5.4, yb, 0])
        pa = VMobject().set_points_smoothly([cl[0].get_center(), np.array([3.0, 3.3, 0]), np.array([-2.0, 3.45, 0]),
                                             np.array([-5.0, 3.3, 0]), k1p + UP * 0.05])
        pb = VMobject().set_points_smoothly([cl[2].get_center(), np.array([3.4, 3.0, 0]), np.array([-3.0, 3.1, 0]),
                                             np.array([-6.3, 2.5, 0]), np.array([-6.3, 0.4, 0]), k2p + UP * 0.05])
        self.play(MoveAlongPath(cl[0], pa), FadeOut(cl[1]), run_time=1.0)
        self.play(MoveAlongPath(cl[2], pb), run_time=1.1)
        self.at("as carbamate", lead=0.7)
        k1 = chip("carbamate", CO2C, 24, pad=0.16).move_to(k1p)
        k2 = chip("carbamate", CO2C, 24, pad=0.16).move_to(k2p)
        ar1 = Arrow(ce1.get_left() + LEFT * 0.03, k1.get_right() + RIGHT * 0.03, color=CO2C, buff=0.0, stroke_width=4)
        ar2 = Arrow(ce2.get_left() + LEFT * 0.03, k2.get_right() + RIGHT * 0.03, color=CO2C, buff=0.0, stroke_width=4)
        self.play(ReplacementTransform(cl[0], k1), ReplacementTransform(cl[2], k2), GrowArrow(ar1), GrowArrow(ar2),
                  run_time=0.7)
        self.at("their own salt bridges", lead=0.8)
        m1 = plus_badge("+", b13(0) + np.array([-C13S / 2, -0.55, 0]))
        m2 = plus_badge("+", b13(2) + np.array([-C13S / 2, 0.5, 0]))
        l1 = DashedLine(k1.get_bottom() + RIGHT * 0.3, m1.get_left(), color=GOLD, stroke_width=7)
        l2 = DashedLine(k2.get_top() + RIGHT * 0.3, m2.get_left(), color=GOLD, stroke_width=7)
        sb = T("salt bridges", 42, GOLD, weight=BOLD).move_to([4.6, 1.0, 0])
        self.play(FadeIn(m1), FadeIn(m2), Create(l1), Create(l2), FadeIn(sb), tr.animate.set_value(0.38), run_time=1.0)
        self.at("favor", lead=0.6)
        tl = T("favor T", 44, BLUE, weight=BOLD).move_to([4.6, 2.3, 0])
        self.play(FadeIn(tl, shift=DOWN * 0.1), tr.animate.set_value(FR_T * 0.95), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- 14: three signals
class S14Signals(Sc):
    def construct(self):
        ph = start_pulse(self, 0.5)
        mus = RoundedRectangle(corner_radius=0.35, width=11.8, height=2.6, stroke_color=MUSC, stroke_width=3,
                               fill_color=MUSC, fill_opacity=0.26).move_to([0, -2.0, 0])
        fib = always_redraw(lambda: pulse_fibres(ph, 5.4, (-2.1, -2.55, -3.0)))
        lab = T("exercising muscle", 30, MUSC).move_to([-3.9, -1.25, 0])
        self.add(fib)
        self.play(FadeIn(mus), FadeIn(lab), run_time=0.6)
        xs = [-4.3, 0.0, 4.3]
        specs = [("falling oxygen", YELLOW, "O₂", DOWN, "oxygen", "pO₂ falls"),
                 ("falling pH", ACID, "H⁺", DOWN, "pH", "pH falls"),
                 ("rising carbon", CO2C, "CO₂", UP, "carbon dioxide", "CO₂ rises")]
        balls = [ball(sym, col, 0.78, 40) for _, col, sym, _, _, _ in specs]
        names = [T(nm, 34, col) for (_, col, _, _, nm, _) in specs]
        for b, n, x in zip(balls, names, xs):
            b.move_to([x, 1.45, 0])
            n.move_to([x, 3.15, 0])
        self.at("exercising muscle")
        self.play(FadeIn(VGroup(*balls), scale=0.5), FadeIn(VGroup(*names), shift=DOWN * 0.1), run_time=0.7)
        self.at("three fast")
        self.play(Indicate(VGroup(*balls), color=GOLD, scale_factor=1.06), run_time=0.6)
        for i, (cue, col, sym, dr, nm, txt) in enumerate(specs):
            self.at(cue)
            ax_ = xs[i] + 1.35
            if dr is DOWN:
                a = Arrow([ax_, 2.5, 0], [ax_, 0.4, 0], color=col, buff=0, stroke_width=10)
            else:
                a = Arrow([ax_, 0.4, 0], [ax_, 2.5, 0], color=col, buff=0, stroke_width=10)
            t_ = T(txt, 38, col).move_to([xs[i], 3.15, 0])
            self.play(GrowArrow(a), FadeOut(names[i]), run_time=0.8)
            self.play(FadeIn(t_), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------- 15: the lungs
LX, MX = -3.9, 3.9


class S15Lungs(Sc):
    def construct(self):
        lung, mus = lung_pic(LX, -0.7).scale(1.3), muscle_pic(MX, -0.7).scale(1.3)
        lung.move_to([LX, -0.8, 0]), mus.move_to([MX, -0.8, 0])
        q = VGroup(T("Does a right shift", 44), T("spoil loading in the lungs?", 44)).arrange(DOWN, buff=0.15).move_to([0, 3.15, 0])
        self.play(FadeIn(lung), FadeIn(mus), FadeIn(q), run_time=0.7)
        self.at("acid and")
        balls = VGroup()
        pts = [(-1.5, 0.7, "H⁺", ACID), (0.1, 0.6, "CO₂", CO2C), (1.5, 0.8, "H⁺", ACID), (-0.9, -0.2, "CO₂", CO2C),
               (0.6, -0.1, "H⁺", ACID), (1.6, -0.5, "CO₂", CO2C), (-1.6, -0.5, "H⁺", ACID), (0.0, -0.9, "H⁺", ACID)]
        for dx, dy, s, c in pts:
            balls.add(ball(s, c, 0.36, 22).move_to([MX + dx * 1.2, -0.3 + dy * 1.2, 0]))
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in balls], lag_ratio=0.08), run_time=1.0)
        self.at("high in tissue")
        hi = T("high in the working muscle", 28, ACID).move_to([MX, 1.8, 0])
        self.play(FadeIn(hi, shift=DOWN * 0.1), run_time=0.5)
        self.at("not in the")
        lo = T("acid and CO₂ low in the lungs", 28, GREEN).move_to([LX, 1.8, 0])
        self.play(FadeIn(lo, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- 16: where the shift happens
def lung_line(ax, label_color=GREY):
    vl = DashedLine(ax.c2p(100, 0), ax.c2p(100, 1.0), color=GREY, stroke_width=3)
    lab = T("100 torr = lungs", 26, BLUE).move_to([ax.c2p(100, 1.0)[0] + 0.3, ax.c2p(100, 1.0)[1] + 0.5, 0], aligned_edge=RIGHT)
    lab.move_to([ax.c2p(100, 1.0)[0] + 0.9 - lab.width / 2, ax.c2p(100, 1.0)[1] + 0.5, 0])
    return vl, lab


class S16Where(Sc):
    def construct(self):
        ax, deco = axes_c()
        blue = cv(ax, P50, BLUE)
        org = cv(ax, P_ACID, ACID)
        dl = dotat(ax, 100, P50, BLUE, 0.14)
        dm = dotat(ax, 20, P_ACID, ACID, 0.14)
        vl, ll = lung_line(ax)
        ll2 = T("lung blood", 28, BLUE).move_to(ax.c2p(80, 0.7))
        ml = T("muscle blood", 28, ACID).move_to(ax.c2p(62, 0.2))
        self.play(Create(ax), FadeIn(deco), Create(blue), run_time=0.9)
        self.play(Create(vl), FadeIn(dl), FadeIn(ll), FadeIn(ll2), run_time=0.4)
        self.at("where")
        ma = Arrow(ml.get_left() + LEFT * 0.05, dm.get_center() + RIGHT * 0.2 + DOWN * 0.05, color=ACID, buff=0.05, stroke_width=4)
        self.play(Create(org), FadeIn(dm), FadeIn(ml), GrowArrow(ma), run_time=0.9)
        cap = T("the shift applies where acid and CO₂ are high", 30, GOLD).move_to([0, 3.5, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- 17 and 18: BPG shifts the curve everywhere
def at100(ax, p_new, color_new):
    """Two markers at 100 torr: a ring for the unshifted curve, a dot for the shifted one."""
    d1 = Circle(radius=0.26, stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to(ax.c2p(100, hill(100, P50)))
    d2 = Dot(ax.c2p(100, hill(100, p_new)), color=color_new, radius=0.2)
    return d1, d2


class S17Flat(Sc):
    def construct(self):
        ax, deco = axes_c()
        blue = cv(ax, P50, GREY)
        vl, ll = lung_line(ax)
        self.add(ax, deco, blue, vl, ll)
        bl = T("without extra BPG", 26, GREY).move_to(ax.c2p(76, 0.28))
        teal = cv(ax, P_MODEST, TEAL)
        tl = T("with BPG", 26, TEAL).move_to(ax.c2p(76, 0.14))
        tl.align_to(bl, LEFT)
        sh = Arrow(ax.c2p(P50, 0.5), ax.c2p(P_MODEST, 0.5), color=TEAL, buff=0, stroke_width=7)
        self.at("bpg")
        self.play(TransformFromCopy(blue, teal), GrowArrow(sh), FadeIn(tl), FadeIn(bl), run_time=1.1)
        self.at("everywhere")
        self.play(Indicate(teal, color=TEAL, scale_factor=1.0), run_time=0.8)
        self.at("sits on the flat top")
        flat1 = ax.plot(lambda x: hill(x, P50), x_range=[70, 100, 0.5], color=GOLD, stroke_width=10)
        flat2 = ax.plot(lambda x: hill(x, P_MODEST), x_range=[70, 100, 0.5], color=GOLD, stroke_width=10)
        ft = T("flat top", 30, GOLD).move_to(ax.c2p(58, 1.0) + UP * 0.45)
        self.play(Create(flat1), Create(flat2), FadeIn(ft), run_time=1.0)
        self.at("modest shift")
        d1, d2 = at100(ax, P_MODEST, TEAL)
        lost = VGroup(T("only a", 30, RED), T("little lost", 30, RED)).arrange(DOWN, buff=0.08)
        lost.move_to([5.5, d1.get_center()[1] - 0.25, 0])
        la = Arrow(lost.get_left() + LEFT * 0.1, d1.get_right() + RIGHT * 0.12, color=RED, buff=0.0, stroke_width=5,
                   max_tip_length_to_length_ratio=0.35)
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.5)
        self.at("costs little")
        self.play(FadeIn(lost), GrowArrow(la), run_time=0.6)
        self.finish()


class S18Large(Sc):
    def construct(self):
        ax, deco = axes_c()
        blue = cv(ax, P50, GREY)
        teal = cv(ax, P_MODEST, TEAL)
        vl, ll = lung_line(ax)
        d1, d2 = at100(ax, P_MODEST, TEAL)
        self.add(ax, deco, blue, teal, vl, ll, d1, d2)
        big = cv(ax, P_LARGE, TEAL)
        d2b = Dot(ax.c2p(100, hill(100, P_LARGE)), color=TEAL, radius=0.09)
        self.at("very large shift")
        self.play(Transform(teal, big), Transform(d2, d2b), run_time=1.5)
        self.at("cost loading")
        br = Brace(Line(d2b.get_center(), ax.c2p(100, hill(100, P50))), direction=RIGHT, color=RED, buff=0.3)
        lost = VGroup(T("too far costs", 28, RED), T("loading", 28, RED)).arrange(DOWN, buff=0.08)
        lost.next_to(br, RIGHT, buff=0.2)
        self.play(GrowFromCenter(br), FadeIn(lost), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- 19: the slower dial
class S19Slow(Sc):
    def construct(self):
        pv = np.array([4.4, -0.7, 0])
        arc = Arc(radius=2.3, start_angle=0, angle=PI, color=GREY, stroke_width=6, arc_center=pv)
        base = Line(pv + LEFT * 2.3, pv + RIGHT * 2.3, color=GREY, stroke_width=4)
        lo, hi = T("low", 28, GREY).move_to(pv + LEFT * 1.7 + DOWN * 0.4), T("high", 28, GREY).move_to(pv + RIGHT * 1.7 + DOWN * 0.4)
        prog = ValueTracker(0)
        a0, a1 = 165 * DEGREES, 15 * DEGREES

        def needle():
            a = a0 + (a1 - a0) * prog.get_value()
            return VGroup(Line(pv, pv + 2.0 * np.array([np.cos(a), np.sin(a), 0]), color=TEAL, stroke_width=8),
                          Dot(pv, color=TEAL, radius=0.16))

        nd = always_redraw(needle)
        title = T("BPG: the slower dial", 44, TEAL).move_to([0, 3.2, 0])
        dl = T("BPG in red cells", 32, TEAL).move_to([4.4, -2.3, 0])
        dial = VGroup(arc, base, lo, hi)
        cc = np.array([-4.4, 0.1, 0])
        face = Circle(radius=1.95, color=GREY, stroke_width=5).move_to(cc)
        ticks = VGroup(*[Line(cc + 1.68 * np.array([np.cos(k * TAU / 12), np.sin(k * TAU / 12), 0]),
                              cc + 1.9 * np.array([np.cos(k * TAU / 12), np.sin(k * TAU / 12), 0]),
                              color=GREY, stroke_width=3) for k in range(12)])

        def hands():
            t = prog.get_value()
            ang = lambda turns: PI / 2 - TAU * turns
            return VGroup(Line(cc, cc + 1.5 * np.array([np.cos(ang(t * 6)), np.sin(ang(t * 6)), 0]), color=TEXT, stroke_width=6),
                          Line(cc, cc + 1.0 * np.array([np.cos(ang(t * 0.5)), np.sin(ang(t * 0.5)), 0]), color=TEXT, stroke_width=8),
                          Dot(cc, color=TEXT, radius=0.1))

        hd = always_redraw(hands)
        clock = VGroup(face, ticks)
        mt = Polygon([-2.3, -1.9, 0], [0.0, 2.0, 0], [2.3, -1.9, 0], color=GREY, stroke_width=5, fill_color=GREY,
                     fill_opacity=0.25)
        cap_ = Polygon([-0.72, 0.8, 0], [0.0, 2.0, 0], [0.72, 0.8, 0], stroke_width=0, fill_color=TEXT, fill_opacity=0.85)
        mtn = VGroup(mt, cap_).move_to([0.0, 0.1, 0])
        self.play(FadeIn(title), FadeIn(dial), FadeIn(dl), FadeIn(clock), FadeIn(mtn), run_time=0.7)
        self.add(nd, hd)
        self.at("it rises")
        self.play(prog.animate.set_value(0.4), run_time=1.3, rate_func=linear)
        cl = T("hours to days", 34, TEXT).move_to([-4.4, -2.3, 0])
        self.at("hours to days")
        self.play(FadeIn(cl), prog.animate.set_value(0.6), run_time=1.0, rate_func=linear)
        self.at("high altitude")
        ml = T("high altitude", 34, TEXT).move_to([0.0, -2.3, 0])
        self.play(FadeIn(ml), Indicate(mtn, color=TEXT, scale_factor=1.05), prog.animate.set_value(0.85), run_time=1.0, rate_func=linear)
        self.at("how you acclimatize")
        acc = T("you acclimatize", 40, GOLD).move_to([0.0, -3.3, 0])
        self.play(FadeIn(acc, shift=DOWN * 0.1), prog.animate.set_value(1.0), run_time=0.9, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- 20: fetal hemoglobin
FX_A, FX_F, FY, FS, FG = -3.6, 3.6, -0.15, 1.9, 0.3
FD = (FS + FG) / 2


class S20Fetal(Sc):
    def construct(self):
        adult = hbcart(FX_A, FY, FS, FG, color=BLUE, lsize=38)
        fetal = hbcart(FX_F, FY, FS, FG, labels=("α", "γ", "γ", "α"), colors=[BLUE, FETAL, FETAL, BLUE], lsize=38)
        al = G("adult α₂β₂", 34, BLUE).move_to([FX_A, FY - 2.55, 0])
        fl = G("fetal α₂γ₂", 34, FETAL).move_to([FX_F, FY - 2.55, 0])
        self.play(FadeIn(adult), FadeIn(al), FadeIn(fetal), FadeIn(fl), run_time=0.5)
        self.at("two gamma")
        self.play(Indicate(fetal[1], color=FETAL, scale_factor=1.08), Indicate(fetal[2], color=FETAL, scale_factor=1.08),
                  run_time=1.0)
        self.at("beta chains")
        self.play(Indicate(adult[1], color=BLUE, scale_factor=1.08), Indicate(adult[2], color=BLUE, scale_factor=1.08),
                  run_time=1.0)
        self.at("position 143")
        ca = chip("143", GOLD, 30, pad=0.16).move_to([FX_A + FD + 0.9, 3.0, 0])
        cf = chip("143", GOLD, 30, pad=0.16).move_to([FX_F + FD + 0.9, 3.0, 0])
        tip = lambda fx: np.array([fx + FD, FY + FD + FS / 2 - 0.35, 0])
        la = Line(ca.get_bottom(), tip(FX_A), color=GOLD, stroke_width=3)
        lf = Line(cf.get_bottom(), tip(FX_F), color=GOLD, stroke_width=3)
        da = Dot(tip(FX_A), color=GOLD, radius=0.1)
        df = Dot(tip(FX_F), color=GOLD, radius=0.1)
        self.play(FadeIn(ca), FadeIn(cf), Create(la), Create(lf), FadeIn(da), FadeIn(df), run_time=0.8)
        self.at("serine")
        cf2 = chip("Ser 143", FETAL, 30, pad=0.16).move_to(cf)
        self.play(ReplacementTransform(cf, cf2), run_time=0.6)
        self.at("histidine")
        ca2 = chip("His 143", BLUE, 30, pad=0.16).move_to(ca)
        self.play(ReplacementTransform(ca, ca2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- 21: fetal binds BPG weakly
class S21Fetal2(Sc):
    def construct(self):
        ax, deco = axes_r()
        mother = cv(ax, P50, BLUE)
        fcart = hbcart(-4.0, 0.6, 1.5, 0.3, labels=("α", "γ", "γ", "α"), colors=[BLUE, FETAL, FETAL, BLUE], lsize=32)
        fl = G("fetal α₂γ₂", 30, FETAL).move_to([-4.0, -1.55, 0])
        self.play(Create(ax), FadeIn(deco), Create(mother), FadeIn(fcart), FadeIn(fl), run_time=0.6)
        bp = bpg_ball(0.32, label=False).move_to([-4.0, 3.2, 0]).set_opacity(0.35)
        bpl = T("BPG", 30, TEAL).next_to(bp, RIGHT, buff=0.25)
        self.at("binds bpg")
        self.play(FadeIn(bp), FadeIn(bpl), run_time=0.4)
        self.play(bp.animate.move_to([-4.0, 2.55, 0]), run_time=0.4)
        self.play(bp.animate.move_to([-4.0, 3.2, 0]), run_time=0.4)
        weak = T("binds BPG weakly", 32, TEAL).move_to([-4.0, -2.35, 0])
        self.play(FadeIn(weak, shift=UP * 0.1), run_time=0.4)
        self.at("higher oxygen")
        fet = cv(ax, P_FETAL, FETAL)
        sh = Arrow(ax.c2p(P50, 0.5), ax.c2p(P_FETAL, 0.5), color=FETAL, buff=0, stroke_width=7)
        self.play(Create(fet), GrowArrow(sh), run_time=1.3)
        self.at("mother's hemoglobin")
        ml = T("mother's hemoglobin", 28, BLUE).move_to(ax.c2p(66, 0.28))
        fl_ = T("fetal hemoglobin", 28, FETAL).move_to(ax.c2p(66, 0.12))
        fl_.align_to(ml, LEFT)
        self.play(FadeIn(ml), FadeIn(fl_), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- 22: across the placenta
class S22Placenta(Sc):
    def construct(self):
        mc = cell_pic(1.6, CELL).move_to([-4.0, 0.3, 0])
        fc = cell_pic(1.6, FETAL).move_to([4.0, 0.3, 0])
        angs = (PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4, 0, PI)
        md = VGroup(*[o2(0.3).move_to(mc.get_center() + np.array([np.cos(a), np.sin(a), 0]) * 0.95) for a in angs])
        wall = RoundedRectangle(corner_radius=0.3, width=0.9, height=5.6, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.25).move_to([0, 0.3, 0])
        pl = T("placenta", 34, GREY).move_to([0, 3.5, 0])
        ml = T("mother's blood", 32, CELL).move_to([-4.0, -2.0, 0])
        fl = T("fetal blood", 32, FETAL).move_to([4.0, -2.0, 0])
        ha = T("higher affinity", 32, FETAL).move_to([4.0, -2.65, 0])
        self.play(FadeIn(mc), FadeIn(md), FadeIn(fc), FadeIn(wall), FadeIn(pl), FadeIn(ml), FadeIn(fl), FadeIn(ha),
                  run_time=0.8)
        self.at("pull oxygen")
        tgt = [fc.get_center() + np.array([np.cos(a), np.sin(a), 0]) * 0.95 for a in (PI / 4, 3 * PI / 4, 5 * PI / 4)]
        moving = [md[0], md[1], md[2]]
        self.play(LaggedStart(*[d.animate.move_to(t) for d, t in zip(moving, tgt)], lag_ratio=0.2), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------- 23: take-home
class S23Take(Sc):
    def construct(self):
        tr, bar = mix_bar(self, FR0, y=REG_BY, fade=False)
        cap = T("the mix of shapes", 26, GREY).move_to([0, REG_BY - 0.85, 0])
        self.add(cap)
        chips = [chip("acid", ACID, 42), chip("CO₂", CO2C, 42), chip("BPG", TEAL, 42)]
        for c, x in zip(chips, REG_X):
            c.move_to([x, 1.4, 0])
        arrows = reg_arrows(chips, 8)
        for nm, c, a in zip(["acid", "carbon dioxide", "bpg"], chips, arrows):
            self.at(nm)
            self.play(FadeIn(c, shift=DOWN * 0.2), GrowArrow(a), run_time=0.6)
        self.at("all favor")
        fav = T("all favor T", 46, BLUE).move_to([0, 3.0, 0])
        self.play(FadeIn(fav, shift=DOWN * 0.1), run_time=0.5)
        self.at("shift the mix")
        self.play(tr.animate.set_value(FR_T - 0.08), run_time=1.3)
        self.at("where oxygen must")
        wh = T("where oxygen must let go", 38, YELLOW).move_to([0, REG_BY - 1.6, 0])
        self.play(FadeIn(wh, shift=UP * 0.1), run_time=0.6)
        self.finish()
