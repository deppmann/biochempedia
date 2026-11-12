"""Two Genes, Two Coins  (Mendel's peas, film 2)

Same world as film 1 (../scenes.py).  COLOUR MAP (both films)
  GOLD   = round copy / round seeds       BROWN = wrinkled copy / wrinkled seeds
  YELC   = yellow copy / yellow seeds     GREENC = green copy / green seeds
  SILVER = the coin                       WHITE outline = gametes
  TEAL   = highlight / question           PETAL = pollen series
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

GOLDC = "#E8B830"
BROWN = "#B9794A"
YELC = "#FFEB3B"
GREENC = "#4CD964"
SILVER = "#C8CCD2"
WHITE = "#FFFFFF"
PETAL = "#CDBDEB"
HL = TEAL
LC = {"R": GOLDC, "r": BROWN, "Y": YELC, "y": GREENC}
KINDS = [("round", "yellow", "RY"), ("round", "green", "Ry"), ("wrinkled", "yellow", "rY"), ("wrinkled", "green", "ry")]


def blend(a, b):
    return interpolate_color(ManimColor(a), ManimColor(b), 0.5)


def seed2(shape="round", colour="yellow", r=0.3, op=0.9):
    sc = GOLDC if shape == "round" else BROWN
    fc = YELC if colour == "yellow" else GREENC
    if shape == "round":
        return Circle(radius=r, stroke_color=sc, stroke_width=5, fill_color=fc, fill_opacity=op)
    s = ParametricFunction(lambda t: np.array([r * (1 + 0.16 * np.sin(7 * t)) * np.cos(t),
                                               r * (1 + 0.16 * np.sin(7 * t)) * np.sin(t), 0]),
                           t_range=[0, TAU], color=sc, stroke_width=5)
    s.set_fill(fc, op)
    return s


def card(ch="?", w=1.1, h=1.5, size=56, color=None):
    c = color or LC.get(ch, TEXT)
    b = RoundedRectangle(corner_radius=0.1 * w / 0.8, width=w, height=h, stroke_color=c, stroke_width=4,
                         fill_color=c, fill_opacity=0.45)
    g = VGroup(b)
    if ch != "?":
        g.add(M(ch, size, c, weight=BOLD).move_to(b))
    return g


def pair(a, b, gap=0.25, **kw):
    return VGroup(card(a, **kw), card(b, **kw)).arrange(RIGHT, buff=gap)


def plant_at(x, ybot, h=2.6, s=1.0):
    stem = Line(ORIGIN, UP * h, color=GREEN, stroke_width=7)
    parts = [stem]
    for sx, yy in [(-1, 0.35), (1, 0.35), (-1, 0.68), (1, 0.68)]:
        l = Ellipse(width=0.9 * s, height=0.38 * s, stroke_color=GREEN, stroke_width=2,
                    fill_color=GREEN, fill_opacity=0.8)
        l.rotate(sx * -0.5).move_to([sx * 0.5 * s, h * yy, 0])
        parts.append(l)
    return VGroup(*parts).shift([x, ybot, 0])


def alive(m, amp=0.05, ph=0.0, w=2.0):
    m._t = ph
    m._o = 0.0

    def up(mm, dt):
        mm._t += dt
        n = amp * math.sin(w * mm._t)
        mm.shift(UP * (n - mm._o))
        mm._o = n
    m.add_updater(up)
    return m


def lab(text, size=30, color=TEXT, pos=ORIGIN, max_w=None, **kw):
    t = T(text, size, color, **kw)
    if max_w and t.width > max_w:
        t.scale(max_w / t.width)
    return t.move_to(pos)


def pod_shape(w, h=0.9):
    return RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.3)


def coin_mob(theta, pos, r=0.9):
    c = math.cos(theta)
    h = max(abs(c), 0.04) * 2 * r
    e = Ellipse(width=2 * r, height=h, stroke_color=SILVER, stroke_width=4, fill_color=SILVER, fill_opacity=0.9)
    g = VGroup(e)
    if abs(c) > 0.5:
        g.add(T("H" if c > 0 else "T", max(int(40 * r / 0.9), 24), BG, weight=BOLD).move_to(e))
    return g.move_to(pos)


def live_coin(pos, r=0.9, th0=0.0):
    th = ValueTracker(th0)
    m = always_redraw(lambda: coin_mob(th.get_value(), pos, r))
    return m, th


def letters(code, size, extra=None):
    g = VGroup(*[M(ch, size, LC[ch], weight=BOLD) for ch in code]).arrange(RIGHT, buff=0.02)
    if extra:
        g = VGroup(g, M(extra, size, TEXT)).arrange(RIGHT, buff=0.18)
    return g


def gam2(code, r=0.5, size=32):
    c = Circle(radius=r, stroke_color=WHITE, stroke_width=3, fill_color=WHITE, fill_opacity=0.12)
    return VGroup(c, letters(code, size).move_to(c))


def hybrid(x, ybot=-3.5, h=3.0, s=1.5):
    return plant_at(x, ybot, h, s)


SH_X, CO_X, CARD_Y = -1.8, 1.8, 0.6


def hybrid_world():
    pl = hybrid(0)
    sp = pair("R", "r").move_to([SH_X, CARD_Y, 0])
    cp = pair("Y", "y").move_to([CO_X, CARD_Y, 0])
    return pl, sp, cp


# ---------------------------------------------------------------- panels A (glued) and B (separate coins)
def panel(kind, cx, cy, s, animated=True):
    """Hypothesis panel built in absolute coordinates (centre cx, cy; scale s). Returns a dict of pieces."""
    P = lambda x, y: np.array([cx + s * x, cy + s * y, 0.0])
    d = {"P": P, "s": s}
    d["title"] = T("glued together" if kind == "A" else "separate coins", 40 * s, TEXT, weight=BOLD).move_to(P(0, 3.0))
    cw, ch_, cs = 0.8 * s, 1.1 * s, 44 * s
    if kind == "A":
        b1 = pair("R", "Y", gap=0.2 * s, w=cw, h=ch_, size=cs).move_to(P(-2.2, 1.7))
        b2 = pair("r", "y", gap=0.2 * s, w=cw, h=ch_, size=cs).move_to(P(2.2, 1.7))
        d["pairs"] = [b1, b2]
        d["clips"] = [RoundedRectangle(corner_radius=0.25 * s, width=2.25 * s, height=1.6 * s, stroke_color=WHITE,
                                       stroke_width=7 * s).move_to(P(x, 1.7)) for x in (-2.2, 2.2)]
        cpos = [P(0, 0.3)]
    else:
        b1 = pair("R", "r", gap=0.2 * s, w=cw, h=ch_, size=cs).move_to(P(-2.3, 1.7))
        b2 = pair("Y", "y", gap=0.2 * s, w=cw, h=ch_, size=cs).move_to(P(2.3, 1.7))
        d["pairs"] = [b1, b2]
        d["clips"] = []
        cpos = [P(-2.3, 0.3), P(2.3, 0.3)]
    d["cpos"] = cpos
    d["coins"] = []
    for p in cpos:
        if animated:
            d["coins"].append(live_coin(p, 0.55 * s))
        else:
            d["coins"].append((coin_mob(0, p, 0.55 * s), None))
    d["tray"] = RoundedRectangle(corner_radius=0.2 * s, width=7 * s, height=1.5 * s, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.24).move_to(P(0, -1.65))
    d["slots"] = [P(x, -1.65) for x in (-2.55, -0.85, 0.85, 2.55)]
    if kind == "A":
        codes = ["RY", "RY", "ry", "ry"]
        d["order"] = [0, 2, 1, 3]            # arrival order: RY, ry, RY, ry
        d["labels"] = [letters("RY", 30 * s, "1/2").move_to(P(-1.7, -3.0)), letters("ry", 30 * s, "1/2").move_to(P(1.7, -3.0))]
    else:
        codes = ["RY", "Ry", "rY", "ry"]
        d["order"] = [0, 1, 2, 3]
        d["labels"] = [M("1/4", 30 * s, TEXT).move_to(P(x, -3.0)) for x in (-2.55, -0.85, 0.85, 2.55)]
    d["codes"] = codes
    d["gams"] = [gam2(c, 0.5 * s, 30 * s).move_to(sl) for c, sl in zip(codes, d["slots"])]
    return d


def panel_all(d):
    return VGroup(d["title"], *d["pairs"], *d["clips"], *[c[0] for c in d["coins"]], d["tray"], *d["gams"], *d["labels"])


def panel_static(kind, cx, cy, s):
    return panel_all(panel(kind, cx, cy, s, animated=False))


# ---------------------------------------------------------------- bar chart (eggs / pollen)
KX = [-4.05, -1.35, 1.35, 4.05]
BASEY, BSC = -2.2, 0.125
EGG = [31, 26, 27, 26]
POL = [24, 25, 22, 27]
EGGC = TEAL


def egg_x(i):
    return KX[i] - 0.47


def pol_x(i):
    return KX[i] + 0.47


def bar_rect(x, v, c, k=1.0):
    h = max(v * BSC * k, 0.02)
    return Rectangle(width=0.85, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.85).move_to([x, BASEY + h / 2, 0])


def num_lab(x, v, c, k=1.0, size=36):
    return M(f"{int(round(v * k))}", size, c, weight=BOLD).set_stroke(BG, 8, background=True).move_to([x, BASEY + max(v * BSC * k, 0.02) + 0.35, 0])


def kind_labels():
    g = VGroup()
    for i, (sh, co, _) in enumerate(KINDS):
        g.add(seed2(sh, co, 0.3).move_to([KX[i], -2.75, 0]))
        g.add(lab(f"{sh} {co}", 24, TEXT, [KX[i], -3.4, 0]))
    return g


def dash_line(v, side):
    y = BASEY + v * BSC
    ln = DashedLine([-5.2, y, 0], [5.2, y, 0], color=WHITE, stroke_width=3, dash_length=0.18).set_z_index(-1)
    t = M(f"{v}", 26, WHITE).move_to([-6.0 if side == "L" else 6.0, y, 0])
    return VGroup(ln, t)


def static_bars(egg=True, pol=True):
    g = VGroup()
    for i in range(4):
        if egg:
            g.add(bar_rect(egg_x(i), EGG[i], EGGC), num_lab(egg_x(i), EGG[i], EGGC))
        if pol:
            g.add(bar_rect(pol_x(i), POL[i], PETAL), num_lab(pol_x(i), POL[i], PETAL))
    return g


EGG_LEG = lambda: lab("hybrid as seed parent (eggs), 110 seeds", 28, EGGC, [0, 3.35, 0])
POL_LEG = lambda: lab("hybrid as pollen parent, 98 seeds", 28, PETAL, [0, 2.8, 0])
BASE_LINE = lambda: Line([-5.3, BASEY, 0], [5.3, BASEY, 0], color=GREY, stroke_width=4)


# ---------------------------------------------------------------- the square (s14-s17)
SQX0, SQW, SQT, SQH = -6.4, 5.6, 2.8, 5.6
VS = SQX0 + SQW * 0.75          # x of the shape cut
HS = SQT - SQH * 0.75           # y of the colour cut
CELLS = {  # key: (x0, x1, y0(top), y1(bottom), shape, colour)
    "RY": (SQX0, VS, SQT, HS, "round", "yellow"),
    "RG": (SQX0, VS, HS, SQT - SQH, "round", "green"),
    "WY": (VS, SQX0 + SQW, SQT, HS, "wrinkled", "yellow"),
    "WG": (VS, SQX0 + SQW, HS, SQT - SQH, "wrinkled", "green"),
}


def cell_rect(k, fill=True):
    x0, x1, y0, y1, sh, co = CELLS[k]
    c = blend(GOLDC if sh == "round" else BROWN, YELC if co == "yellow" else GREENC)
    r = Rectangle(width=x1 - x0, height=y0 - y1, stroke_color=WHITE, stroke_width=3, fill_color=c, fill_opacity=0.45 if fill else 0)
    return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def cell_center(k):
    x0, x1, y0, y1, _, _ = CELLS[k]
    return np.array([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def square_cells():
    return VGroup(*[cell_rect(k) for k in CELLS])


def cut_labels():
    top = [lab("round 3/4", 30, GOLDC, [(SQX0 + VS) / 2, 3.35, 0]), lab("wrinkled 1/4", 30, BROWN, [(VS + SQX0 + SQW) / 2 + 0.2, 3.35, 0], max_w=2.6)]
    side = [lab("yellow 3/4", 30, YELC, [1.1, (SQT + HS) / 2, 0]), lab("green 1/4", 30, GREENC, [1.1, (HS + SQT - SQH) / 2, 0])]
    return top, side


FRAC = {"RY": "9/16", "RG": "3/16", "WY": "3/16", "WG": "1/16"}


def cell_fracs(seeds=True):
    g = VGroup()
    for k, f in FRAC.items():
        c = cell_center(k)
        _, _, _, _, sh, co = CELLS[k]
        if k == "RY":
            g.add(seed2(sh, co, 0.55).move_to(c + UP * 0.9), M(f, 56, TEXT, weight=BOLD).move_to(c + DOWN * 0.1),
                  lab("round yellow", 30, TEXT, c + DOWN * 1.0))
        elif k == "RG":
            g.add(seed2(sh, co, 0.3).move_to(c + LEFT * 1.6), M(f, 38, TEXT, weight=BOLD).move_to(c + RIGHT * 0.2))
        elif k == "WY":
            g.add(seed2(sh, co, 0.3).move_to(c + UP * 1.2), M(f, 28, TEXT, weight=BOLD).move_to(c + UP * 0.3))
        else:
            g.add(seed2(sh, co, 0.26).move_to(c + UP * 0.32), M(f, 28, TEXT, weight=BOLD).move_to(c + DOWN * 0.3))
    return g


# =====================================================================================
class S00Title(TitleCard):
    LESSON = "Mendel's peas"
    TITLE = "Two Genes, Two Coins"


class S01Hook(SpokenScene):
    def construct(self):
        pl = hybrid(0)
        sp = pair("R", "r").move_to([0, CARD_Y, 0])
        alive(sp, 0.05, 0.2)
        self.play(Create(pl), FadeIn(sp, shift=UP * 0.15), run_time=1.0)
        self.at("one at a time")
        a = VGroup(card("R", 0.8, 1.1, 40), T("one at a time?", 36, TEXT)).arrange(DOWN, buff=0.2).move_to([-4.6, 1.2, 0])
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.8)
        self.at("in bundles")
        bcs = VGroup(card("R", 0.8, 1.1, 40), card("Y", 0.8, 1.1, 40)).arrange(RIGHT, buff=0.15)
        clip = RoundedRectangle(corner_radius=0.2, width=bcs.width + 0.35, height=1.45, stroke_color=WHITE, stroke_width=6).move_to(bcs)
        b = VGroup(VGroup(bcs, clip), T("in bundles?", 36, TEXT)).arrange(DOWN, buff=0.2).move_to([4.6, 1.2, 0])
        self.play(FadeIn(b, shift=LEFT * 0.2), run_time=0.8)
        self.at("chapter one")
        sl = lab("seed shape", 38, GOLDC, [0, 2.0, 0])
        self.play(FadeOut(a), FadeOut(b), FadeIn(sl, shift=DOWN * 0.1), Indicate(sp, color=HL, scale_factor=1.1), run_time=1.3)
        self.at("now add a second")
        cp = pair("Y", "y").move_to([5.5, CARD_Y, 0])
        alive(cp, 0.05, 1.0)
        self.play(sp.animate.move_to([SH_X, CARD_Y, 0]), cp.animate.move_to([CO_X, CARD_Y, 0]), sl.animate.move_to([SH_X, 2.0, 0]), run_time=1.6)
        cl = lab("seed color", 38, YELC, [CO_X, 2.0, 0])
        self.play(FadeIn(cl, shift=DOWN * 0.1), Indicate(cp, color=HL, scale_factor=1.1), run_time=1.2)
        self.finish()


class S02Cross(SpokenScene):
    def construct(self):
        def parent(x, shape, colour, name):
            pl = plant_at(x, -3.2, 2.2, 1.3)
            p = pod_shape(3.2, 1.1).move_to([x, -0.2, 0])
            ss = VGroup(*[alive(seed2(shape, colour, 0.4), 0.04, i + x) for i in range(3)]).arrange(RIGHT, buff=0.3).move_to(p)
            lb = lab(name, 34, TEXT, [x, 1.1, 0])
            return pl, p, ss, lb
        L = parent(-4.5, "round", "yellow", "round yellow")
        R = parent(4.5, "wrinkled", "green", "wrinkled green")
        self.play(Create(L[0]), FadeIn(L[1]), run_time=1.0)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in L[2]], lag_ratio=0.2), FadeIn(L[3]), run_time=1.0)
        self.at("wrinkled green")
        self.play(Create(R[0]), FadeIn(R[1]), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in R[2]], lag_ratio=0.2), FadeIn(R[3]), run_time=1.0)
        self.at("every hybrid seed")
        a1 = Arrow([-2.6, 0.2, 0], [-0.6, -1.0, 0], buff=0, color=GREY, stroke_width=7)
        a2 = Arrow([2.6, 0.2, 0], [0.6, -1.0, 0], buff=0, color=GREY, stroke_width=7)
        hp = pod_shape(4.2, 1.3).move_to([0, -1.9, 0])
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(hp), run_time=1.2)
        self.at("round and yellow")
        hs = VGroup(*[alive(seed2("round", "yellow", 0.45), 0.04, i) for i in range(4)]).arrange(RIGHT, buff=0.25).move_to(hp)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in hs], lag_ratio=0.2), run_time=1.2)
        gl = M("RrYy", 44, TEXT, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S03Pairs(SpokenScene):
    def construct(self):
        pl, sp, cp = hybrid_world()
        alive(sp, 0.04, 0.2)
        alive(cp, 0.04, 1.0)
        self.play(Create(pl), run_time=1.0)
        self.at("two pairs of cards")
        self.play(FadeIn(sp, shift=UP * 0.1), FadeIn(cp, shift=UP * 0.1), run_time=1.2)
        self.at("a shape pair")
        t1 = lab("shape", 38, GOLDC, [SH_X, 2.0, 0])
        n1 = VGroup(lab("round", 26, GOLDC, [SH_X - 0.67, -0.4, 0]), lab("wrinkled", 26, BROWN, [SH_X + 0.67, -0.4, 0]))
        self.play(FadeIn(t1, shift=DOWN * 0.1), Indicate(sp, color=HL, scale_factor=1.12), run_time=1.0)
        self.play(FadeIn(n1), run_time=0.7)
        self.at("a color pair")
        t2 = lab("color", 38, YELC, [CO_X, 2.0, 0])
        n2 = VGroup(lab("yellow", 26, YELC, [CO_X - 0.67, -0.4, 0]), lab("green", 26, GREENC, [CO_X + 0.67, -0.4, 0]))
        self.play(FadeIn(t2, shift=DOWN * 0.1), Indicate(cp, color=HL, scale_factor=1.12), run_time=1.0)
        self.play(FadeIn(n2), run_time=0.7)
        self.finish()


class S04Question(SpokenScene):
    def construct(self):
        pl, sp, cp = hybrid_world()
        alive(sp, 0.04, 0.2)
        alive(cp, 0.04, 1.0)
        self.add(pl, sp, cp)
        c1, th1 = live_coin(np.array([SH_X, 2.7, 0]), 0.75)
        c2, th2 = live_coin(np.array([CO_X, 2.7, 0]), 0.75)
        q = lab("?", 90, HL, [0, 2.7, 0], weight=BOLD)
        self.add(c1, c2)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(q, scale=1.3), run_time=0.8)
        self.at("toss the two pairs together")
        self.play(th1.animate.set_value(4 * PI), th2.animate.set_value(4 * PI), run_time=1.5)
        self.at("or separately")
        self.play(th1.animate.set_value(7 * PI), th2.animate.set_value(10 * PI), run_time=1.6, rate_func=linear)
        self.finish()


class S05Glued(SpokenScene):
    def construct(self):
        A = panel("A", 0, 0, 1.0)
        cm, th = A["coins"][0]
        self.add(cm)
        self.play(FadeIn(A["title"]), FadeIn(A["pairs"][0]), FadeIn(A["pairs"][1]), FadeIn(A["tray"]), FadeIn(cm), run_time=0.8)
        self.at("glued together")
        self.play(*[GrowFromCenter(c) for c in A["clips"]], run_time=1.0)
        self.at("round and yellow")
        self.play(Indicate(A["pairs"][0], color=HL, scale_factor=1.12), run_time=1.2)
        self.at("so they would leave together")
        # four tosses: heads = glued RY, tails = glued ry
        tgt = [2 * PI, 5 * PI, 8 * PI, 11 * PI]
        grp = [0, 1, 0, 1]
        for n in range(4):
            slot = A["slots"][A["order"][n]]
            src = A["pairs"][grp[n]]
            c2 = VGroup(*[m.copy() for m in src])
            g = gam2("RY" if grp[n] == 0 else "ry", 0.5, 32).move_to(slot)
            self.play(th.animate.set_value(tgt[n]), Transform(c2, g), run_time=0.8)
        self.at("only two kinds")
        self.play(*[FadeIn(l, shift=UP * 0.1) for l in A["labels"]], run_time=1.0)
        self.finish()


class S06Separate(SpokenScene):
    def construct(self):
        A = panel_static("A", 0, 0, 1.0)
        self.add(A)
        B = panel("B", 3.3, 0, 0.8)
        (c1, th1), (c2, th2) = B["coins"]
        self.play(A.animate.scale(0.8, about_point=ORIGIN).shift(LEFT * 3.3), FadeIn(B["title"]), FadeIn(B["tray"]), run_time=1.0)
        self.at("each pair has its own coin")
        self.add(c1, c2)
        self.play(FadeIn(B["pairs"][0]), FadeIn(B["pairs"][1]), FadeIn(c1), FadeIn(c2), run_time=1.0)
        self.at("any shape card")
        sa, sb = B["pairs"]
        lines = VGroup(*[Line(sa[i].get_bottom() + DOWN * 0.02, sb[j].get_bottom() + DOWN * 0.02, color=WHITE, stroke_width=3).set_opacity(0.55)
                         for i in range(2) for j in range(2)])
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2), run_time=1.0)
        self.play(FadeOut(lines), run_time=0.3)
        self.at("four kinds")
        faces = [(0, 0), (0, 1), (1, 0), (1, 1)]
        cur = [0.0, 0.0]
        curf = [0, 0]
        for n, (f1, f2) in enumerate(faces):
            tg = []
            for ci, f in enumerate((f1, f2)):
                prev, pf = cur[ci], curf[ci]
                t = prev + (2 * PI if f == pf else 3 * PI)
                tg.append(t)
                cur[ci], curf[ci] = t, f
            ca = sa[f1].copy()
            cb = sb[f2].copy()
            c3 = VGroup(ca, cb)
            g = B["gams"][n].copy()
            self.play(th1.animate.set_value(tg[0]), th2.animate.set_value(tg[1]), Transform(c3, g), run_time=0.55)
        self.at("a quarter each")
        self.play(*[FadeIn(l, shift=UP * 0.1) for l in B["labels"]], run_time=1.0)
        self.finish()


def s07_pieces():
    A = panel_static("A", -3.3, 0, 0.8)
    B = panel_static("B", 3.3, 0, 0.8)
    A.remove(A[0])
    B.remove(B[0])
    A.set_opacity(0.14)
    B.set_opacity(0.14)
    sp = pair("R", "r", w=0.8, h=1.1, size=42).move_to([-2.7, -0.7, 0]).set_opacity(0.35)
    cp = pair("Y", "y", w=0.8, h=1.1, size=42).move_to([2.7, -0.7, 0]).set_opacity(0.35)
    sd = seed2("round", "yellow", 0.95).move_to([0, -0.7, 0])
    q = VGroup(T("How could you read", 40, HL), T("the hybrid's gametes?", 40, HL)).arrange(DOWN, buff=0.15).move_to([0, 3.1, 0])
    return A, B, sp, cp, sd, q


class S07Predict(SpokenScene):
    def construct(self):
        A, B, sp, cp, sd, q = s07_pieces()
        self.add(A, B)
        self.at("a selfed seed")
        g1 = gam2("RY", 0.5, 32).move_to([-4.2, -0.7, 0])
        g2 = gam2("ry", 0.5, 32).move_to([4.2, -0.7, 0])
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.7)
        self.at("mixes two")
        mid = VGroup(g1, g2)
        self.play(g1.animate.move_to([-0.5, -0.7, 0]), g2.animate.move_to([0.5, -0.7, 0]), run_time=1.2)
        self.play(Transform(mid, sd), run_time=0.8)
        alive(mid, 0.05, 0.4)
        self.at("dominance hides")
        self.play(FadeIn(sp), FadeIn(cp), run_time=1.0)
        self.play(Indicate(mid, color=HL, scale_factor=1.08), run_time=0.9)
        self.at("so how could you read")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.9)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        A, B, sp, cp, sd, q = s07_pieces()
        alive(sd, 0.05, 0.4)
        self.add(A, B, sp, cp, sd, q)
        k = ValueTracker(1)
        ring = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=TAU * max(k.get_value(), 0.001), color=HL, stroke_width=8).move_to([6.0, 3.2, 0]))
        back = Circle(radius=0.55, color=GREY, stroke_width=3).move_to([6.0, 3.2, 0])
        self.add(back, ring)
        self.play(k.animate.set_value(0), run_time=4.9, rate_func=linear)
        self.finish()


class S09Tester(SpokenScene):
    def construct(self):
        hp = plant_at(-5.0, -3.1, 2.4, 1.1)
        hc = VGroup(pair("R", "r", w=0.8, h=1.1, size=42).move_to([-5.0, 1.9, 0]), pair("Y", "y", w=0.8, h=1.1, size=42).move_to([-5.0, 0.5, 0]))
        hl_ = lab("hybrid", 32, TEXT, [-5.0, -3.5, 0])
        tp = plant_at(5.0, -3.1, 2.4, 1.1)
        tc = VGroup(pair("r", "r", w=0.8, h=1.1, size=42).move_to([5.0, 1.9, 0]), pair("y", "y", w=0.8, h=1.1, size=42).move_to([5.0, 0.5, 0]))
        tl = M("tester rryy", 30, TEXT).move_to([5.0, -3.5, 0])
        alive(hc, 0.04, 0.0)
        self.play(Create(hp), FadeIn(hc), FadeIn(hl_), run_time=1.3)
        self.at("wrinkled green plant")
        self.play(Create(tp), FadeIn(tc), FadeIn(tl), run_time=1.3)
        alive(tc, 0.04, 1.0)
        self.at("that tester")
        tg = gam2("ry", 0.5, 32).move_to([1.6, 3.0, 0])
        tt = lab("tester gives only", 30, TEXT, [-0.8, 3.0, 0])
        self.play(FadeIn(tt), FadeIn(tg), Indicate(tc, color=HL, scale_factor=1.1), run_time=1.4)
        self.at("so each seed shows")
        xs = [-2.7, -0.9, 0.9, 2.7]
        gs = VGroup(*[gam2(c, 0.5, 32).move_to([x, 1.2, 0]) for x, (_, _, c) in zip(xs, KINDS)])
        self.play(LaggedStart(*[GrowFromCenter(g) for g in gs], lag_ratio=0.25), run_time=1.4)
        arrows = VGroup(*[Arrow([x, 0.55, 0], [x, -0.55, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.2) for x in xs])
        sds = VGroup(*[alive(seed2(sh, co, 0.5).move_to([x, -1.3, 0]), 0.04, x) for x, (sh, co, _) in zip(xs, KINDS)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.0)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sds], lag_ratio=0.2), run_time=1.2)
        cap = lab("each seed reads one hybrid gamete", 32, HL, [0, -2.8, 0], max_w=7.6)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S10Eggs(SpokenScene):
    def construct(self):
        base = BASE_LINE()
        kl = kind_labels()
        leg = EGG_LEG()
        self.play(Create(base), FadeIn(kl), FadeIn(leg), run_time=1.2)
        self.at("four kinds")
        rain = VGroup()
        for i, (sh, co, _) in enumerate(KINDS):
            for j in range(5):
                rain.add(seed2(sh, co, 0.17).move_to([egg_x(i) + (j - 2) * 0.17, 1.5 + 0.3 * j, 0]))
        self.play(LaggedStart(*[m.animate.shift(DOWN * 4.0).set_opacity(0) for m in rain], lag_ratio=0.04), run_time=1.6)
        self.remove(rain)
        self.at("roughly equal")
        k = ValueTracker(0)
        bars = always_redraw(lambda: VGroup(*[bar_rect(egg_x(i), EGG[i], EGGC, k.get_value()) for i in range(4)]))
        nums = always_redraw(lambda: VGroup(*[num_lab(egg_x(i), EGG[i], EGGC, k.get_value()) for i in range(4)]))
        self.add(bars, nums)
        self.play(k.animate.set_value(1), run_time=2.6, rate_func=smooth)
        dl = dash_line(27.5, "L")
        self.play(Create(dl[0]), FadeIn(dl[1]), run_time=1.0)
        self.finish()


class S11Pollen(SpokenScene):
    def construct(self):
        base = BASE_LINE()
        kl = kind_labels()
        leg = EGG_LEG()
        eg = static_bars(True, False)
        dl = dash_line(27.5, "L")
        self.add(base, kl, leg, eg, dl)
        self.wait(0.5)
        self.at("the other way")
        pl_ = POL_LEG()
        self.play(FadeIn(pl_, shift=DOWN * 0.1), run_time=0.8)
        self.at("again four kinds")
        k = ValueTracker(0)
        bars = always_redraw(lambda: VGroup(*[bar_rect(pol_x(i), POL[i], PETAL, k.get_value()) for i in range(4)]))
        nums = always_redraw(lambda: VGroup(*[num_lab(pol_x(i), POL[i], PETAL, k.get_value()) for i in range(4)]))
        self.add(bars, nums)
        self.play(k.animate.set_value(1), run_time=2.0, rate_func=smooth)
        self.at("roughly equal")
        dl2 = dash_line(24.5, "R")
        self.play(Create(dl2[0]), FadeIn(dl2[1]), run_time=1.0)
        self.finish()


class S12Verdict(SpokenScene):
    def construct(self):
        base = BASE_LINE()
        kl = kind_labels()
        leg = VGroup(EGG_LEG(), POL_LEG())
        bars = static_bars(True, True)
        d1, d2 = dash_line(27.5, "L"), dash_line(24.5, "R")
        chart = VGroup(base, bars, d1[0], d2[0])
        self.add(chart, d1[1], d2[1], kl, leg)
        self.play(FadeOut(kl), FadeOut(leg), FadeOut(d1[1]), FadeOut(d2[1]), run_time=0.5)
        self.play(chart.animate.scale(0.65).move_to([-3.0, 0.3, 0]), run_time=1.2)
        # mini hypothesis panels
        boxA = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([3.7, 2.0, 0])
        ta = lab("glued: 2 kinds", 32, TEXT, [3.7, 2.7, 0])
        ga = VGroup(gam2("RY", 0.45, 28), gam2("ry", 0.45, 28)).arrange(RIGHT, buff=0.9).move_to([3.7, 1.7, 0])
        A = VGroup(boxA, ta, ga)
        boxB = RoundedRectangle(corner_radius=0.2, width=5.6, height=2.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([3.7, -0.7, 0])
        tb = lab("separate coins: 4 kinds", 32, TEXT, [3.7, 0.0, 0], max_w=5.3)
        gb = VGroup(*[gam2(c, 0.45, 28) for _, _, c in KINDS]).arrange(RIGHT, buff=0.2).move_to([3.7, -1.0, 0])
        B = VGroup(boxB, tb, gb)
        self.at("fully glued pairs")
        self.play(FadeIn(A), FadeIn(B), run_time=1.0)
        cross = VGroup(Line([1.2, 2.9, 0], [6.2, 1.1, 0], color=RED, stroke_width=8), Line([1.2, 1.1, 0], [6.2, 2.9, 0], color=RED, stroke_width=8)).set_opacity(0.8)
        self.play(Create(cross), A.animate.set_opacity(0.35), run_time=1.0)
        self.at("two separate coins")
        ring = SurroundingRectangle(boxB, color=HL, buff=0.08, stroke_width=6)
        self.play(Create(ring), B.animate.set_opacity(1.0), run_time=1.0)
        cap = lab("four kinds, about equal, eggs and pollen alike", 30, TEXT, [0, -3.35, 0], max_w=12)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.8)
        self.finish()


def heap_seeds():
    rng = random.Random(7)
    kinds = ["RY"] * 23 + ["Ry"] * 8 + ["rY"] * 7 + ["ry"] * 2
    rng.shuffle(kinds)
    out, n = [], 0
    for row, cnt in enumerate([9, 8, 7, 6, 5, 4]):
        for j in range(cnt):
            k = kinds[n]
            n += 1
            sh = "round" if k[0] == "R" else "wrinkled"
            co = "yellow" if k[1] == "Y" else "green"
            x = 2.0 + (j - (cnt - 1) / 2) * 0.72
            y = -3.0 + row * 0.62
            out.append(seed2(sh, co, 0.28).move_to([x, y, 0]))
    return out


class S13Self(SpokenScene):
    def construct(self):
        hp = plant_at(-4.7, -3.1, 2.4, 1.1)
        hc = VGroup(pair("R", "r", w=0.8, h=1.1, size=42).move_to([-4.7, 1.9, 0]), pair("Y", "y", w=0.8, h=1.1, size=42).move_to([-4.7, 0.5, 0]))
        hl_ = lab("double hybrid", 32, TEXT, [-4.7, -3.5, 0])
        alive(hc, 0.04, 0.3)
        self.play(Create(hp), FadeIn(hc), FadeIn(hl_), run_time=1.2)
        self.at("pollinate itself")
        loop = Arc(radius=0.6, start_angle=PI * 0.3, angle=PI * 1.5, color=TEXT, stroke_width=6).add_tip(tip_length=0.25).move_to([-3.0, 1.2, 0])
        self.play(Create(loop), run_time=1.0)
        self.at("as mendel did")
        seeds = heap_seeds()
        for i, s in enumerate(seeds):
            alive(s, 0.02, i)
        tl = lab("556 seeds from 15 F1 plants", 32, TEXT, [1.9, 3.3, 0], max_w=7.4)
        self.play(FadeIn(tl, shift=DOWN * 0.1), LaggedStart(*[GrowFromCenter(s) for s in seeds], lag_ratio=0.04), run_time=2.4)
        self.at("separate coins predict")
        q = lab("predicted split?", 36, HL, [1.9, 1.6, 0], weight=BOLD)
        self.play(FadeIn(q, scale=1.2), run_time=0.8)
        self.finish()


def square_outline():
    return Rectangle(width=SQW, height=SQH, stroke_color=WHITE, stroke_width=4).move_to([SQX0 + SQW / 2, SQT - SQH / 2, 0])


class S14Square(SpokenScene):
    def construct(self):
        sq = square_outline()
        al = lab("all the seeds", 32, TEXT, [SQX0 + SQW / 2, 0, 0])
        self.at("draw a square")
        self.play(Create(sq), FadeIn(al), run_time=1.4)
        top, side = cut_labels()
        self.at("shape cuts it")
        vline = Line([VS, SQT, 0], [VS, SQT - SQH, 0], color=WHITE, stroke_width=5)
        fl = Rectangle(width=VS - SQX0, height=SQH, stroke_width=0, fill_color=GOLDC, fill_opacity=0.35).move_to([(SQX0 + VS) / 2, SQT - SQH / 2, 0])
        fr = Rectangle(width=SQX0 + SQW - VS, height=SQH, stroke_width=0, fill_color=BROWN, fill_opacity=0.35).move_to([(VS + SQX0 + SQW) / 2, SQT - SQH / 2, 0])
        self.play(FadeOut(al), Create(vline), FadeIn(fl), FadeIn(fr), run_time=1.4)
        self.play(FadeIn(top[0], shift=DOWN * 0.1), FadeIn(top[1], shift=DOWN * 0.1), run_time=1.0)
        self.at("color cuts it")
        hline = Line([SQX0, HS, 0], [SQX0 + SQW, HS, 0], color=WHITE, stroke_width=5)
        cells = square_cells()
        self.play(Create(hline), run_time=1.0)
        self.play(FadeOut(fl), FadeOut(fr), FadeIn(cells), run_time=1.0)
        self.play(FadeIn(side[0], shift=LEFT * 0.1), FadeIn(side[1], shift=LEFT * 0.1), run_time=1.0)
        self.finish()


def s14_end():
    top, side = cut_labels()
    return square_cells(), VGroup(*top), VGroup(*side)


class S15Multiply(SpokenScene):
    def construct(self):
        cells, top, side = s14_end()
        self.add(cells, top, side)
        fr = cell_fracs()
        self.wait(0.3)
        self.at("separate coins multiply")
        eq = M("3/4 x 3/4 = 9/16", 40, TEXT, weight=BOLD).move_to([3.8, 1.9, 0])
        self.play(FadeIn(eq, shift=LEFT * 0.2), run_time=1.0)
        self.at("so each box's share")
        self.play(LaggedStart(*[FadeIn(m) for m in fr], lag_ratio=0.1), run_time=1.6)
        self.at("round yellow corner")
        ring = SurroundingRectangle(cells[0], color=HL, buff=-0.04, stroke_width=8)
        self.play(Create(ring), run_time=0.8)
        self.at("wrinkled green corner")
        eq2 = M("1/4 x 1/4 = 1/16", 40, TEXT, weight=BOLD).move_to([3.8, -0.7, 0])
        ring2 = SurroundingRectangle(cells[3], color=HL, buff=-0.04, stroke_width=8)
        self.play(FadeOut(ring), Create(ring2), FadeIn(eq2, shift=LEFT * 0.2), run_time=1.0)
        self.finish()


COUNTS = [315, 108, 101, 32]
EXPECT = [312.75, 104.25, 104.25, 34.75]
GX = [1.7, 3.15, 4.6, 6.05]
B2Y, B2S = -1.7, 0.0125


def sq_bars(k=1.0):
    g = VGroup()
    for i, key in enumerate(["RY", "RG", "WY", "WG"]):
        c = blend(GOLDC if key[0] == "R" else BROWN, YELC if key[1] == "Y" else GREENC)
        h = max(COUNTS[i] * B2S * k, 0.02)
        g.add(Rectangle(width=0.45, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.9).move_to([GX[i] - 0.25, B2Y + h / 2, 0]))
    return g


class S16Fit(SpokenScene):
    def construct(self):
        cells = square_cells()
        fr = cell_fracs()
        rl = lab("9 : 3 : 3 : 1", 44, TEXT, [SQX0 + SQW / 2, 3.35, 0], weight=BOLD)
        self.add(cells, fr, rl)
        base = Line([1.0, B2Y, 0], [6.6, B2Y, 0], color=GREY, stroke_width=4)
        icons = VGroup(*[seed2(sh, co, 0.22).move_to([GX[i], -2.2, 0]) for i, (sh, co, _) in enumerate(KINDS)])
        self.add(base)
        self.at("mendel's counts")
        k = ValueTracker(0)
        bars = always_redraw(lambda: sq_bars(k.get_value()))
        nums = always_redraw(lambda: VGroup(*[M(f"{int(COUNTS[i] * k.get_value())}", 24, TEXT).move_to([GX[i] - 0.25, B2Y + max(COUNTS[i] * B2S * k.get_value(), 0.02) + 0.3, 0]) for i in range(4)]))
        self.add(bars, nums)
        self.play(FadeIn(icons), k.animate.set_value(1), run_time=2.6, rate_func=smooth)
        self.at("close but not exact")
        ex = VGroup()
        for i in range(4):
            h = EXPECT[i] * B2S
            r = Rectangle(width=0.45, height=h, stroke_color=WHITE, stroke_width=3).move_to([GX[i] + 0.25, B2Y + h / 2, 0])
            ex.add(DashedVMobject(r, num_dashes=40))
        leg = VGroup(T("counted", 26, TEXT), T("expected", 26, WHITE)).arrange(RIGHT, buff=0.6).move_to([3.8, 3.2, 0])
        self.play(FadeIn(ex), FadeIn(leg), run_time=1.2)
        etxt = VGroup(*[M(f"{EXPECT[i]:g}", 22, WHITE).move_to([GX[i], -2.75, 0]) for i in range(4)])
        self.play(FadeIn(etxt, shift=UP * 0.1), run_time=1.0)
        self.finish()


class S17Scope(SpokenScene):
    def construct(self):
        cells = square_cells()
        fr = cell_fracs()
        rl = lab("9 : 3 : 3 : 1", 44, TEXT, [SQX0 + SQW / 2, 3.35, 0], weight=BOLD)
        sqg = VGroup(cells, fr, rl)
        self.add(sqg)
        self.wait(0.3)
        self.at("this held for")
        cap = lab("seed shape and seed color", 32, TEXT, [-1.7, 2.7, 0], max_w=5)
        self.play(FadeOut(fr), FadeOut(rl), cells.animate.scale(0.3, about_point=ORIGIN).move_to([-5.5, 2.7, 0]), run_time=1.4)
        self.play(FadeIn(cap), run_time=0.6)
        self.at("it does not hold")
        pa = pair("A", "a", color=TEAL, w=1.1, h=1.5, size=56).move_to([-2.4, 0.3, 0])
        pb = pair("B", "b", color=PETAL, w=1.1, h=1.5, size=56).move_to([2.4, 0.3, 0])
        alive(pa, 0.04, 0.2)
        alive(pb, 0.04, 1.1)
        self.play(FadeOut(cap), FadeIn(pa, shift=RIGHT * 0.3), FadeIn(pb, shift=LEFT * 0.3), run_time=1.2)
        self.at("why not comes")
        links = VGroup(*[DashedLine([-0.9, 0.3 + dy, 0], [0.9, 0.3 + dy, 0], color=WHITE, stroke_width=5, dash_length=0.15) for dy in (-0.3, 0.3)]).set_opacity(0.6)
        self.play(Create(links), run_time=0.9)
        q = lab("not every pair: later lesson", 38, HL, [0, -1.9, 0], max_w=11)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S18Idea(SpokenScene):
    def construct(self):
        sp = pair("R", "r", w=1.1, h=1.5, size=56).move_to([-5.0, 1.4, 0])
        cp = pair("Y", "y", w=1.1, h=1.5, size=56).move_to([-5.0, -1.4, 0])
        c1, th1 = live_coin(np.array([-2.7, 1.4, 0]), 0.7)
        c2, th2 = live_coin(np.array([-2.7, -1.4, 0]), 0.7)
        alive(sp, 0.04, 0.0)
        alive(cp, 0.04, 1.0)
        self.add(c1, c2)
        self.play(FadeIn(sp), FadeIn(cp), FadeIn(c1), FadeIn(c2), run_time=0.6)
        self.at("so here is the whole idea")
        l0 = lab("The whole idea", 34, HL, [2.4, 2.9, 0], weight=BOLD)
        self.play(FadeIn(l0, shift=DOWN * 0.1), th1.animate.set_value(3 * PI), th2.animate.set_value(4 * PI), run_time=1.2)
        self.at("two copies of each gene")
        s1 = lab("Two copies of each gene.", 36, TEXT, [2.4, 1.8, 0], max_w=7.8)
        self.play(FadeIn(s1, shift=LEFT * 0.2), Indicate(sp, color=HL, scale_factor=1.08), run_time=1.0)
        self.at("one goes to each gamete")
        s2 = VGroup(T("One goes to each gamete,", 36, TEXT), T("by a coin toss.", 36, TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s2.move_to([2.4, 0.3, 0])
        self.play(FadeIn(s2, shift=LEFT * 0.2), th1.animate.set_value(7 * PI), th2.animate.set_value(9 * PI), run_time=1.6)
        self.at("genes that assort")
        s3 = VGroup(T("Genes that assort independently", 36, TEXT), T("are separate coins.", 36, TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s3.move_to([2.4, -1.7, 0])
        self.play(FadeIn(s3, shift=LEFT * 0.2), Indicate(c2, color=HL, scale_factor=1.1), run_time=1.6)
        self.at("like seed shape")
        self.play(Indicate(sp, color=GOLDC, scale_factor=1.08), Indicate(cp, color=YELC, scale_factor=1.08), th1.animate.set_value(11 * PI), th2.animate.set_value(12 * PI), run_time=1.6)
        self.finish()


class S19End(EndCard):
    LINE = "Genes that assort independently are separate coins: their chances multiply."
