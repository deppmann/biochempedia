"""Two Copies, One Coin Toss  (Mendel's peas, film 1)

COLOUR MAP (whole film)
  GOLD   = round copy / round seeds        BROWN  = wrinkled copy / wrinkled seeds
  SILVER = the coin                        WHITE outline = gametes (egg circle, pollen hexagon)
  YEL    = highlight / counts              GREEN  = plants
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

GOLDC = "#E8B830"
BROWN = "#B9794A"
YEL = "#FFF066"
SILVER = "#C8CCD2"
WHITE = "#FFFFFF"
PETAL = "#CDBDEB"


def col(ch):
    return GOLDC if ch == "R" else (BROWN if ch == "r" else TEXT)


def seed(kind="round", r=0.3, op=0.85):
    c = GOLDC if kind == "round" else BROWN
    if kind == "round":
        return Circle(radius=r, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=op)
    s = ParametricFunction(lambda t: np.array([r * (1 + 0.16 * np.sin(7 * t)) * np.cos(t),
                                               r * (1 + 0.16 * np.sin(7 * t)) * np.sin(t), 0]),
                           t_range=[0, TAU], color=c, stroke_width=3)
    s.set_fill(c, op)
    return s


def card(ch="?", w=0.8, h=1.1, size=40):
    c = col(ch)
    b = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=c, stroke_width=4,
                         fill_color=c, fill_opacity=0.45)
    g = VGroup(b)
    if ch != "?":
        g.add(M(ch, size, c, weight=BOLD).move_to(b))
    return g


def pair(a, b, gap=0.2, **kw):
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


def lab(text, size=30, color=TEXT, pos=ORIGIN, **kw):
    return T(text, size, color, **kw).move_to(pos)


def pod_shape(w, h=0.9):
    return RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.3)


def pod_with(kinds, center, r=0.3, gap=0.65, h=0.9):
    center = np.array(center, dtype=float)
    n = len(kinds)
    p = pod_shape(n * gap + 0.5, h).move_to(center)
    ss = VGroup(*[seed(k, r).move_to(center + [(i - (n - 1) / 2) * gap, 0, 0]) for i, k in enumerate(kinds)])
    return p, ss


def pea_plant(x, kind, name):
    c = GOLDC if kind == "round" else BROWN
    p, ss = pod_with([kind] * 4, [x, 1.2, 0], 0.4, 0.85, 1.1)
    stem = plant_at(x, -2.0, 2.7, 1.8)
    label = lab(name, 28, c, [x, 2.45, 0])
    return stem, p, ss, label


# ---------------- coin ----------------
def coin_mob(theta, pos, r=0.9):
    c = math.cos(theta)
    h = max(abs(c), 0.04) * 2 * r
    e = Ellipse(width=2 * r, height=h, stroke_color=SILVER, stroke_width=4, fill_color=SILVER, fill_opacity=0.9)
    g = VGroup(e)
    if abs(c) > 0.5:
        g.add(T("H" if c > 0 else "T", int(40 * r / 0.9), BG, weight=BOLD).move_to(e))
    return g.move_to(pos)


# ---------------- gametes and trays ----------------
def gam(kind, ch, r=0.3, size=26):
    c = col(ch)
    s = Circle(radius=r) if kind == "egg" else RegularPolygon(n=6, radius=r * 1.1)
    s.set_stroke(WHITE, 3).set_fill(c, 0.85)
    return VGroup(s, M(ch, size, WHITE, weight=BOLD).move_to(s))


EGG_CX, POL_CX = -1.2, 4.3


def tray_box(cx):
    return RoundedRectangle(corner_radius=0.2, width=4.8, height=2.4, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.24).move_to([cx, -1.65, 0])


def slot(cx, idx):
    return np.array([cx + [-1.65, -0.55, 0.55, 1.65][idx % 4], [-1.1, -2.2][idx // 4], 0])


def tray_gamete(kind, ch, cx, idx):
    return gam(kind, ch, 0.38, 28).move_to(slot(cx, idx))


def hybrid_plant(x, ybot=-1.5, with_label=None):
    pl = plant_at(x, ybot, 1.9, 1.25)
    cp = pair("R", "r").move_to([x, 1.2, 0])
    g = VGroup(pl, cp)
    return g, cp


# ---------------- the 2x2 grid ----------------
GX, GY, CW = 0.4, 0.0, 2.2
LET = ["R", "r"]


def ccen(i, j):
    return np.array([GX + (j - 0.5) * CW, GY + (0.5 - i) * CW, 0])


def geno_txt(a, b, size=34):
    s = "".join(sorted([a, b]))
    return VGroup(*[M(ch, size, col(ch), weight=BOLD) for ch in s]).arrange(RIGHT, buff=0.03)


def cell_pieces(i, j):
    c = ccen(i, j)
    a, b = LET[i], LET[j]
    rect = Square(CW, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.24).move_to(c)
    e = gam("egg", a).move_to(c + np.array([-0.5, 0.55, 0]))
    p = gam("pollen", b).move_to(c + np.array([0.5, 0.55, 0]))
    g = geno_txt(a, b).move_to(c + np.array([0, -0.15, 0]))
    return rect, e, p, g


def headers():
    eggs = VGroup(*[gam("egg", LET[i], 0.35, 28).move_to([-2.2, ccen(i, 0)[1], 0]) for i in range(2)])
    pol = VGroup(*[gam("pollen", LET[j], 0.35, 28).move_to([ccen(0, j)[0], 2.65, 0]) for j in range(2)])
    l1 = lab("eggs", 30, TEXT, [-3.4, 0, 0])
    l2 = lab("pollen", 30, TEXT, [GX, 3.45, 0])
    return eggs, pol, l1, l2


def seed_at(i, j, r=0.3):
    k = "wrinkled" if (i == 1 and j == 1) else "round"
    return seed(k, r).move_to(ccen(i, j) + np.array([0, -0.75, 0]))


def build_grid(seeds=False):
    """The finished grid (headers, four filled cells); returns (VGroup, cells dict, seeds dict)."""
    eggs, pol, l1, l2 = headers()
    cells, seedd = {}, {}
    allm = [eggs, pol, l1, l2]
    for i in range(2):
        for j in range(2):
            r_, e, p, g = cell_pieces(i, j)
            cells[(i, j)] = VGroup(r_, e, p, g)
            allm.append(cells[(i, j)])
            if seeds:
                s = alive(seed_at(i, j), 0.04, i + 2 * j)
                seedd[(i, j)] = s
                allm.append(s)
    return VGroup(*allm), cells, seedd


def question_card():
    return VGroup(T("Which boxes", 36, YEL), T("look round?", 36, YEL)).arrange(DOWN, buff=0.15).move_to([5.0, 0.4, 0])


def hl(cell_group, color=YEL):
    return SurroundingRectangle(cell_group[0], color=color, buff=-0.02, stroke_width=6)


# =====================================================================================
class S00Title(TitleCard):
    LESSON = "Mendel's peas"
    TITLE = "Two Copies, One Coin Toss"


class S01Hook(SpokenScene):
    def construct(self):
        items = []
        for x, k, nm in [(-3.4, "round", "true-breeding round"), (3.4, "wrinkled", "true-breeding wrinkled")]:
            stem, p, ss, label = pea_plant(x, k, nm)
            for i, s in enumerate(ss):
                alive(s, 0.05, i)
            loop = Arc(radius=0.45, start_angle=PI * 0.3, angle=PI * 1.5, color=TEXT, stroke_width=5).add_tip(tip_length=0.2)
            loop.move_to([x + 1.4, -0.7, 0])
            cap = lab("selfed: same every generation", 26, TEXT, [x, -2.75, 0])
            items.append((stem, p, ss, label, loop, cap))
        self.play(*[Create(it[0]) for it in items], run_time=1.5)
        self.play(*[FadeIn(it[1]) for it in items], *[LaggedStart(*[GrowFromCenter(s) for s in it[2]], lag_ratio=0.2) for it in items], run_time=1.5)
        self.at("Mendel asked")
        self.play(*[FadeIn(it[3], shift=DOWN * 0.1) for it in items], run_time=0.8)
        self.at("garden peas")
        self.play(*[Create(it[4]) for it in items], *[FadeIn(it[5]) for it in items], run_time=1.0)
        self.finish()


class S02Lines(SpokenScene):
    def construct(self):
        ys = [1.6, 0.2, -1.2]
        cols = {}
        for x, k in [(-3.4, "round"), (3.4, "wrinkled")]:
            rows = []
            for y in ys:
                row = VGroup(*[alive(seed(k, 0.46), 0.04, y + i + x) for i in range(4)]).arrange(RIGHT, buff=0.3).move_to([x, y, 0])
                rows.append(row)
            arrows = [Arrow([x, ys[i] - 0.5, 0], [x, ys[i + 1] + 0.5, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.2) for i in range(2)]
            cols[k] = (rows, arrows)
        self.play(*[FadeIn(cols[k][0][0]) for k in cols], run_time=0.8)
        self.at("always bred")
        self.play(*[GrowArrow(cols[k][1][0]) for k in cols], *[FadeIn(cols[k][0][1]) for k in cols], run_time=0.7)
        self.at("bred true")
        self.play(*[GrowArrow(cols[k][1][1]) for k in cols], *[FadeIn(cols[k][0][2]) for k in cols], run_time=1.0)
        self.at("One line")
        l1 = lab("round line", 32, GOLDC, [-3.4, 2.75, 0])
        self.play(FadeIn(l1, shift=DOWN * 0.1), *[Indicate(r, color=GOLDC, scale_factor=1.08) for r in cols["round"][0]], run_time=1.2)
        self.at("The other")
        l2 = lab("wrinkled line", 32, BROWN, [3.4, 2.75, 0])
        self.play(FadeIn(l2, shift=DOWN * 0.1), *[Indicate(r, color=BROWN, scale_factor=1.08) for r in cols["wrinkled"][0]], run_time=1.2)
        self.finish()


class S03Cross(SpokenScene):
    def construct(self):
        base = np.array([-1.5, -2.6, 0])
        title = lab("cross by hand", 34, TEXT, [0, 3.3, 0])
        closed = [-6, -3, 0, 3, 6]
        opn = [-62, -31, 0, 31, 62]
        petals = VGroup(*[Ellipse(width=1.1, height=2.8, stroke_color=PETAL, stroke_width=3, fill_color=PETAL,
                                  fill_opacity=0.35).move_to(base + UP * 1.4).rotate(a * DEGREES, about_point=base) for a in closed])
        fstem = Line(base + DOWN * 0.5, base, color=GREEN, stroke_width=7)
        pistil = VGroup(Line(base + UP * 0.3, base + UP * 1.6, color=GREEN, stroke_width=8), Dot(base + UP * 1.6, radius=0.13, color=GREEN))
        stamens = VGroup(*[VGroup(Line(base + UP * 0.3, base + UP * 1.3 + RIGHT * dx, color=GREY, stroke_width=4),
                                  Dot(base + UP * 1.3 + RIGHT * dx, radius=0.11, color=YELLOW)) for dx in [-0.7, -0.3, 0.3, 0.7]])
        wl = lab("wrinkled line", 28, BROWN, [-1.5, -3.45, 0])
        dp, dss = pod_with(["round"] * 3, [4.6, 1.6, 0], 0.28, 0.65, 0.9)
        dl = lab("round line", 28, GOLDC, [4.6, 2.5, 0])
        for i, s in enumerate(dss):
            alive(s, 0.04, i)
        self.play(FadeIn(title), FadeIn(fstem), FadeIn(petals), FadeIn(wl), run_time=1.2)
        self.play(FadeIn(dp), FadeIn(dss), FadeIn(dl), run_time=1.0)
        self.at("He opened")
        self.play(*[p.animate.rotate((o - c) * DEGREES, about_point=base) for p, o, c in zip(petals, opn, closed)],
                  FadeIn(pistil), FadeIn(stamens), run_time=1.4)
        self.at("removed its")
        tip = base + UP * 1.3
        tw = VGroup(Line(tip, tip + np.array([0.45, 1.5, 0]), color=SILVER, stroke_width=6),
                    Line(tip, tip + np.array([0.95, 1.25, 0]), color=SILVER, stroke_width=6))
        tw.shift(RIGHT * 2.2)
        self.play(FadeIn(tw), tw.animate.shift(LEFT * 2.2), run_time=0.9)
        target = np.array([-5.6, 1.5, 0])
        delta = target - stamens.get_center()
        self.play(stamens.animate.shift(delta), tw.animate.shift(delta), run_time=0.9)
        self.at("which make pollen")
        sl = VGroup(T("stamens", 28, TEXT), T("make pollen", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([-5.6, 0.35, 0])
        self.play(FadeOut(tw), FadeIn(sl), run_time=0.7)
        self.at("brushed on")
        stig = base + UP * 1.6
        tuft0 = np.array([4.0, 0.9, 0])
        tuft = Ellipse(width=0.55, height=0.3, stroke_color="#D9C7A0", fill_color="#D9C7A0", fill_opacity=0.9).move_to(tuft0)
        handle = Line(tuft0, tuft0 + np.array([1.5, 1.1, 0]), color=SILVER, stroke_width=6)
        dots = VGroup(*[Dot(tuft0 + np.array([dx, dy, 0]), radius=0.08, color=GOLDC) for dx, dy in [(-0.15, 0.1), (0.1, 0.12), (0, -0.05), (0.18, -0.02)]])
        brush = VGroup(tuft, handle, dots)
        self.play(FadeIn(brush), run_time=0.4)
        d = stig + np.array([0, 0.15, 0]) - tuft0
        self.play(brush.animate.shift(d), run_time=1.6)
        self.play(FadeOut(tuft), FadeOut(handle), dots.animate.arrange(RIGHT, buff=0.05).move_to(stig + UP * 0.28), run_time=0.8)
        self.finish()


class S04Hybrids(SpokenScene):
    def construct(self):
        p, ss = pod_with(["round"] * 5, [0, 0.3, 0], 0.7, 1.7, 2.2)
        for i, s in enumerate(ss):
            alive(s, 0.06, i)
        label = lab("hybrid seeds (F1)", 36, TEXT, [0, 2.4, 0])
        self.play(FadeIn(p), run_time=0.6)
        self.play(LaggedStart(*[GrowFromCenter(s) for s in ss], lag_ratio=0.25), FadeIn(label), run_time=1.6)
        self.at("like the round parent")
        self.play(Indicate(ss, color=GOLDC, scale_factor=1.12), run_time=1.2)
        self.at("Not halfway")
        self.play(Indicate(ss, color=YEL, scale_factor=1.12), run_time=1.2)
        self.at("Wrinkled seemed")
        ghost = DashedVMobject(seed("wrinkled", 0.55, 0).set_stroke(BROWN, 4), num_dashes=28).move_to([5.7, 0.3, 0])
        q = lab("?", 64, BROWN, [5.7, 0.3, 0], weight=BOLD)
        self.play(FadeIn(ghost), FadeIn(q), run_time=1.0)
        self.play(ghost.animate.set_opacity(0.25), q.animate.set_opacity(0.4), run_time=1.5)
        self.finish()


class S05Return(SpokenScene):
    def construct(self):
        px = -4.8
        ground = Line([-6.6, -3.2, 0], [-3.0, -3.2, 0], color=GREY, stroke_width=5)
        s0 = seed("round", 0.33).move_to([px, -2.2, 0])
        self.play(FadeIn(ground), FadeIn(s0), run_time=0.8)
        self.play(s0.animate.move_to([px, -3.0, 0]), run_time=1.0)
        self.at("let each plant")
        pl = plant_at(px, -3.2, 3.6, 1.2)
        self.play(FadeOut(s0), Create(pl), run_time=1.6)
        fl = lab("F1 plant", 30, TEXT, [px, 1.0, 0])
        loop = Arc(radius=0.45, start_angle=PI * 0.3, angle=PI * 1.5, color=TEXT, stroke_width=5).add_tip(tip_length=0.2).move_to([px + 1.5, -1.0, 0])
        self.play(FadeIn(fl), Create(loop), run_time=1.0)
        self.at("Their pods")
        p, ss = pod_with(["round", "round", "wrinkled", "round"], [1.8, 0.4, 0], 0.5, 1.6, 1.5)
        self.play(FadeIn(p), run_time=0.8)
        self.at("held round")
        self.play(*[GrowFromCenter(ss[i]) for i in (0, 1)], run_time=0.8)
        self.at("wrinkled peas")
        self.play(GrowFromCenter(ss[2]), run_time=0.7)
        self.play(GrowFromCenter(ss[3]), run_time=0.5)
        for i, s in enumerate(ss):
            alive(s, 0.05, i)
        self.at("side by side")
        cap = lab("F2 seeds (in the F1 plant's pods)", 28, TEXT, [1.8, 2.0, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.8)
        self.at("Wrinkled was back")
        self.play(Indicate(ss[2], color=YEL, scale_factor=1.4), run_time=1.5)
        self.finish()


BX_G, BX_B, BASE_Y, SC = -4.2, -1.9, -2.8, 0.00085


def blab(n, w, c, pos):
    return VGroup(T(n, 30, c, weight=BOLD), T(w, 28, c)).arrange(DOWN, buff=0.05).move_to(pos)


def bars_static():
    g = Rectangle(width=1.8, height=5474 * SC, stroke_color=GOLDC, fill_color=GOLDC, fill_opacity=0.8).move_to([BX_G, BASE_Y + 5474 * SC / 2, 0])
    b = Rectangle(width=1.8, height=1850 * SC, stroke_color=BROWN, fill_color=BROWN, fill_opacity=0.8).move_to([BX_B, BASE_Y + 1850 * SC / 2, 0])
    gl = blab("5,474", "round", GOLDC, [BX_G, BASE_Y + 5474 * SC + 0.55, 0])
    bl = blab("1,850", "wrinkled", BROWN, [BX_B, BASE_Y + 1850 * SC + 0.55, 0])
    ln = Line([-5.8, BASE_Y, 0], [-0.4, BASE_Y, 0], color=GREY, stroke_width=4)
    return g, b, gl, bl, ln


class S06Count(SpokenScene):
    def construct(self):
        k = ValueTracker(0)
        ln = Line([-5.8, BASE_Y, 0], [-0.4, BASE_Y, 0], color=GREY, stroke_width=4)
        gbar = always_redraw(lambda: Rectangle(width=1.8, height=max(k.get_value() * 5474 * SC, 0.02), stroke_color=GOLDC, fill_color=GOLDC, fill_opacity=0.8).move_to([BX_G, BASE_Y + max(k.get_value() * 5474 * SC, 0.02) / 2, 0]))
        bbar = always_redraw(lambda: Rectangle(width=1.8, height=max(k.get_value() * 1850 * SC, 0.02), stroke_color=BROWN, fill_color=BROWN, fill_opacity=0.8).move_to([BX_B, BASE_Y + max(k.get_value() * 1850 * SC, 0.02) / 2, 0]))
        gl = always_redraw(lambda: blab(f"{int(k.get_value() * 5474):,}", "round", GOLDC, [BX_G, BASE_Y + max(k.get_value() * 5474 * SC, 0.02) + 0.55, 0]))
        bl = always_redraw(lambda: blab(f"{int(k.get_value() * 1850):,}", "wrinkled", BROWN, [BX_B, BASE_Y + max(k.get_value() * 1850 * SC, 0.02) + 0.55, 0]))
        self.add(ln, gbar, bbar, gl, bl)
        self.play(k.animate.set_value(1), run_time=3.0, rate_func=smooth)
        self.at("by about")
        ratio = lab("2.96 : 1", 56, TEXT, [3.9, 0.9, 0], weight=BOLD)
        rl = lab("round : wrinkled", 28, TEXT, [3.9, 0.15, 0])
        self.play(FadeIn(ratio, shift=UP * 0.15), FadeIn(rl), run_time=0.9)
        self.at("where was wrinkled")
        q = lab("?", 90, BROWN, [BX_B, 0.3, 0], weight=BOLD)
        self.play(FadeIn(q, scale=1.3), run_time=0.8)
        self.at("why one in four")
        self.play(Indicate(q, color=YEL, scale_factor=1.3), run_time=1.2)
        self.finish()


class S07TwoCopies(SpokenScene):
    def construct(self):
        pl = plant_at(0, -3.3, 3.5, 3.0)
        for m in pl[1:]:
            alive(m, 0.04, 0.5)
        self.play(Create(pl), run_time=2.0)
        self.at("Each pea plant")
        title = lab("two copies of the seed-shape gene", 30, TEXT, [0, 3.35, 0])
        slots = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.1, width=1.0, height=1.4, stroke_color=TEXT, stroke_width=3), num_dashes=24).move_to([sx, 1.4, 0]) for sx in (-0.65, 0.65)])
        self.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(slots), run_time=1.0)
        self.at("two copies")
        self.play(Indicate(slots, color=YEL, scale_factor=1.12), run_time=1.0)
        self.at("One copy came")
        mp = plant_at(-5.2, -2.2, 2.2, 0.9)
        fp = plant_at(5.2, -2.2, 2.2, 0.9)
        mc = card("?").move_to([-5.2, 0.9, 0])
        fc = card("?").move_to([5.2, 0.9, 0])
        ml = lab("mother", 28, TEXT, [-5.2, -2.85, 0])
        fl = lab("father", 28, TEXT, [5.2, -2.85, 0])
        self.play(FadeIn(mp), FadeIn(fp), FadeIn(mc), FadeIn(fc), FadeIn(ml), FadeIn(fl), run_time=1.0)
        self.at("came from each parent")
        self.play(mc.animate.move_to([-0.65, 1.4, 0]), fc.animate.move_to([0.65, 1.4, 0]), FadeOut(slots), run_time=1.6)
        self.finish()


class S08Cards(SpokenScene):
    def construct(self):
        xs = [-4.6, 0, 4.6]
        plants = [plant_at(x, -2.4, 2.3, 1.6) for x in xs]
        pairs = [pair("?", "?").move_to([x, 1.0, 0]) for x in xs]
        self.play(*[FadeIn(p) for p in plants], run_time=1.0)
        self.at("as cards")
        self.play(*[FadeIn(c) for c in pairs], run_time=0.8)
        specs = [("R", "R", "round line", GOLDC, "RR"), ("r", "r", "wrinkled line", BROWN, "rr"), ("R", "r", "hybrid", TEXT, "Rr")]
        times = ["a round line", "a wrinkled line", "the hybrid holds"]
        news = []
        for i, (a, b, nm, c, g) in enumerate(specs):
            self.at(times[i])
            newp = pair(a, b).move_to([xs[i], 1.0, 0])
            nl = lab(nm, 30, c, [xs[i], 2.55, 0])
            gt = geno_txt(a, b, 40).move_to([xs[i], -3.1, 0])
            self.play(ReplacementTransform(pairs[i], newp), FadeIn(nl, shift=DOWN * 0.1), FadeIn(gt), run_time=1.0)
            news.append(newp)
        glow = SurroundingRectangle(news[2], color=YEL, buff=0.15, stroke_width=6)
        self.play(Create(glow), run_time=0.8)
        self.play(Indicate(news[2], color=YEL, scale_factor=1.1), run_time=0.8)
        self.finish()


class S09Coin(SpokenScene):
    def construct(self):
        hp, cp = hybrid_plant(-5.2)
        hl_ = lab("hybrid", 28, TEXT, [-5.2, -2.0, 0])
        self.play(FadeIn(hp), FadeIn(hl_), run_time=1.0)
        self.at("an egg")
        et, pt = tray_box(EGG_CX), tray_box(POL_CX)
        el, pl_ = lab("eggs", 28, TEXT, [EGG_CX, -0.1, 0]), lab("pollen", 28, TEXT, [POL_CX, -0.1, 0])
        self.play(FadeIn(et), FadeIn(el), run_time=0.7)
        self.at("pollen grain")
        self.play(FadeIn(pt), FadeIn(pl_), run_time=0.7)
        self.at("it puts in")
        self.fly(cp[0], "egg", "R", EGG_CX, 0)
        self.at("which card")
        th = ValueTracker(0)
        cpos = np.array([0.5, 1.9, 0])
        coin = always_redraw(lambda: coin_mob(th.get_value(), cpos))
        self.add(coin)
        self.wait(0.3)
        plan = [("egg", "r", EGG_CX, 1, 3 * PI), ("pollen", "R", POL_CX, 0, 4 * PI), ("pollen", "r", POL_CX, 1, 7 * PI),
                ("egg", "R", EGG_CX, 2, 8 * PI)]
        for kind, ch, cx, idx, target in plan:
            src = cp[0] if ch == "R" else cp[1]
            c2 = src.copy()
            g = tray_gamete(kind, ch, cx, idx)
            self.play(th.animate.set_value(target), Transform(c2, g), run_time=0.7, rate_func=smooth)
        self.finish()

    def fly(self, src, kind, ch, cx, idx):
        c2 = src.copy()
        self.play(Transform(c2, tray_gamete(kind, ch, cx, idx)), run_time=0.8)


class S10Half(SpokenScene):
    def construct(self):
        hp, cp = hybrid_plant(-5.2)
        hl_ = lab("hybrid", 28, TEXT, [-5.2, -2.0, 0])
        et, pt = tray_box(EGG_CX), tray_box(POL_CX)
        el, pl_ = lab("eggs", 28, TEXT, [EGG_CX, -0.1, 0]), lab("pollen", 28, TEXT, [POL_CX, -0.1, 0])
        th = ValueTracker(0)
        cpos = np.array([0.5, 1.9, 0])
        coin = always_redraw(lambda: coin_mob(th.get_value(), cpos))
        th.add_updater(lambda m, dt: m.increment_value(dt * 6))
        self.add(hp, hl_, et, pt, el, pl_, coin, th)

        def row(kind, cx, ch, r0):
            return [tray_gamete(kind, ch, cx, r0 * 4 + i) for i in range(4)]
        eg, eb = row("egg", EGG_CX, "R", 0), row("egg", EGG_CX, "r", 1)
        pg, pb = row("pollen", POL_CX, "R", 0), row("pollen", POL_CX, "r", 1)

        def half_lab(cx):
            return VGroup(T("1/2", 30), T("R", 30, GOLDC, weight=BOLD), T(",", 30), T("1/2", 30), T("r", 30, BROWN, weight=BOLD)).arrange(RIGHT, buff=0.14).move_to([cx, -3.4, 0])
        self.play(LaggedStart(*[GrowFromCenter(x) for x in eg], lag_ratio=0.3), run_time=1.8)
        self.at("and half carry")
        self.play(LaggedStart(*[GrowFromCenter(x) for x in eb], lag_ratio=0.3), run_time=1.8)
        self.play(FadeIn(half_lab(EGG_CX)), run_time=0.6)
        self.at("the same is true")
        self.play(LaggedStart(*[GrowFromCenter(x) for x in pg + pb], lag_ratio=0.18), run_time=2.0)
        self.play(FadeIn(half_lab(POL_CX)), run_time=0.6)
        self.finish()


class S11Grid(SpokenScene):
    def construct(self):
        px = -5.4
        hp, cp = hybrid_plant(px)
        hl_ = lab("hybrid", 28, TEXT, [px, -2.0, 0])
        self.play(FadeIn(hp), FadeIn(hl_), run_time=1.0)
        self.at("pollinates itself")
        loop = Arc(radius=0.45, start_angle=PI * 0.3, angle=PI * 1.5, color=TEXT, stroke_width=5).add_tip(tip_length=0.2).move_to([px, 2.75, 0])
        self.play(Create(loop), run_time=1.2)
        self.at("eggs meet")
        eggs, pol, l1, l2 = headers()
        self.play(FadeIn(eggs), FadeIn(l1), FadeIn(pol), FadeIn(l2), run_time=0.9)
        rects = [cell_pieces(i, j)[0] for i in range(2) for j in range(2)]
        self.play(*[FadeIn(r) for r in rects], run_time=0.8)
        self.at("so four unions")
        cells = {}
        order = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for n, (i, j) in enumerate(order):
            r_, e, p, g = cell_pieces(i, j)
            ec, pc = eggs[i].copy(), pol[j].copy()
            self.play(Transform(ec, e), Transform(pc, p), run_time=0.6)
            self.play(FadeIn(g), run_time=0.2)
            cells[(i, j)] = VGroup(r_, ec, pc, g)
        self.at("one box gets")
        h = hl(cells[(0, 0)])
        self.play(Create(h), run_time=0.6)
        self.at("two get")
        h2 = VGroup(hl(cells[(0, 1)]), hl(cells[(1, 0)]))
        self.play(FadeOut(h), Create(h2), run_time=0.6)
        self.at("one gets two wrinkled")
        h3 = hl(cells[(1, 1)], BROWN)
        self.play(FadeOut(h2), Create(h3), run_time=0.6)
        ratio = lab("1 : 2 : 1", 48, TEXT, [GX, -3.1, 0], weight=BOLD)
        self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.8)
        self.finish()


def predict_world(self_):
    """The frame shared by s12 and s13: plant, round seed, grid, question card."""
    px = -5.4
    hp, cp = hybrid_plant(px)
    hl_ = lab("hybrid", 28, TEXT, [px, -2.0, 0])
    sd = alive(seed("round", 0.4).move_to([px, -3.1, 0]), 0.04)
    grid, cells, _ = build_grid()
    q = question_card()
    return hp, hl_, sd, grid, cells, q, cp


class S12Predict(SpokenScene):
    def construct(self):
        hp, hl_, sd, grid, cells, q, cp = predict_world(self)
        self.add(hp, hl_, grid)
        self.wait(0.5)
        self.at("every hybrid seed")
        self.play(GrowFromCenter(sd), run_time=0.8)
        self.at("with one copy")
        self.play(Indicate(cp, color=YEL, scale_factor=1.15), run_time=1.2)
        self.at("so which")
        self.play(FadeIn(q, shift=LEFT * 0.2), run_time=0.8)
        for k in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            h = hl(cells[k])
            self.play(Create(h), run_time=0.25)
            self.play(FadeOut(h), run_time=0.2)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        hp, hl_, sd, grid, cells, q, cp = predict_world(self)
        self.add(hp, hl_, sd, grid, q)
        k = ValueTracker(1)
        ring = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=TAU * max(k.get_value(), 0.001), color=YEL, stroke_width=8).move_to([5.6, -2.7, 0]))
        back = Circle(radius=0.55, color=GREY, stroke_width=3).move_to([5.6, -2.7, 0])
        self.add(back, ring)
        self.play(k.animate.set_value(0), run_time=4.9, rate_func=linear)
        self.finish()


class S14Reveal(SpokenScene):
    def construct(self):
        grid, cells, _ = build_grid()
        self.add(grid)
        self.wait(0.1)
        seeds = {}
        for (i, j) in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            seeds[(i, j)] = alive(seed_at(i, j), 0.04, i + 2 * j)
        self.play(LaggedStart(*[GrowFromCenter(seeds[k]) for k in [(0, 0), (0, 1), (1, 0)]], lag_ratio=0.25), run_time=1.4)
        self.play(GrowFromCenter(seeds[(1, 1)]), run_time=0.6)
        self.at("one round copy")
        self.play(Indicate(VGroup(cells[(0, 1)][1], cells[(1, 0)][2]), color=YEL, scale_factor=1.3), run_time=1.2)
        self.at("mendel called")
        head = lab("dominant:", 34, GOLDC, [5.0, 1.0, 0], weight=BOLD)
        body = VGroup(T("the form", 30), T("the hybrid", 30), T("shows", 30)).arrange(DOWN, buff=0.12).move_to([5.0, -0.4, 0])
        self.play(FadeIn(head), run_time=0.7)
        self.play(FadeIn(body), run_time=0.8)
        self.at("the one the hybrid")
        self.play(Indicate(body, color=YEL, scale_factor=1.08), run_time=1.2)
        self.finish()


class S15Recessive(SpokenScene):
    def construct(self):
        grid, cells, _ = build_grid()
        self.add(grid)
        seeds = {}
        for (i, j) in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            seeds[(i, j)] = alive(seed_at(i, j), 0.04, i + 2 * j)
            self.add(seeds[(i, j)])
        self.wait(0.5)
        self.at("the recessive")
        head = lab("recessive:", 34, BROWN, [5.0, 1.1, 0], weight=BOLD)
        body = VGroup(T("hidden in", 28), T("the hybrid;", 28), T("shows with", 28), T("two copies", 28)).arrange(DOWN, buff=0.1).move_to([5.0, -0.4, 0])
        h = hl(cells[(1, 1)], BROWN)
        self.play(FadeIn(head), Create(h), run_time=0.9)
        self.play(FadeIn(body), run_time=0.7)
        self.at("it hides")
        ghosts = VGroup(*[card("r", 0.5, 0.7, 26).move_to(ccen(*k) + np.array([0.72, -0.72, 0])).set_opacity(0.4) for k in [(0, 1), (1, 0)]])
        for g in ghosts:
            g.set_z_index(-1)
        self.play(FadeIn(ghosts), run_time=1.0)
        self.at("shows only")
        self.play(Indicate(cells[(1, 1)], color=BROWN, scale_factor=1.08), Indicate(seeds[(1, 1)], color=YEL, scale_factor=1.4), run_time=1.5)
        self.finish()


class S16Ratio(SpokenScene):
    def construct(self):
        grid, cells, _ = build_grid()
        self.add(grid)
        seeds = {}
        for (i, j) in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            seeds[(i, j)] = alive(seed_at(i, j), 0.04, i + 2 * j)
            self.add(seeds[(i, j)])
        self.wait(0.3)
        self.at("the hidden mix")
        g1 = VGroup(T("genotypes", 30), T("1", 30), T("RR", 30, GOLDC, weight=BOLD), T(":", 30), T("2", 30), T("Rr", 30, GOLDC, weight=BOLD), T(":", 30), T("1", 30), T("rr", 30, BROWN, weight=BOLD)).arrange(RIGHT, buff=0.14).move_to([GX, -2.75, 0])
        self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.9)
        self.at("what you see")
        g2 = VGroup(T("phenotypes", 30), T("3 round", 30, GOLDC), T(":", 30), T("1 wrinkled", 30, BROWN)).arrange(RIGHT, buff=0.14).move_to([GX, -3.4, 0])
        self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.9)
        self.at("three round")
        hs = VGroup(*[hl(cells[k], GOLDC) for k in [(0, 0), (0, 1), (1, 0)]])
        self.play(Create(hs), run_time=0.8)
        self.at("to one wrinkled")
        h3 = hl(cells[(1, 1)], BROWN)
        self.play(Create(h3), run_time=0.8)
        self.finish()


class S17Scatter(SpokenScene):
    def construct(self):
        g, b, gl, bl, ln = bars_static()
        gt = g.copy().scale([1, 0.02, 1], about_point=g.get_bottom())
        bt = b.copy().scale([1, 0.02, 1], about_point=b.get_bottom())
        self.add(ln, gt, bt)
        self.play(Transform(gt, g), Transform(bt, b), run_time=1.0)
        self.play(FadeIn(gl), FadeIn(bl), run_time=0.6)
        self.at("it came close")
        ey_g = BASE_Y + 5493 * SC
        ey_b = BASE_Y + 1831 * SC
        dg = DashedLine([BX_G - 1.1, ey_g, 0], [BX_G + 1.1, ey_g, 0], color=WHITE, stroke_width=4)
        db = DashedLine([BX_B - 1.1, ey_b, 0], [BX_B + 1.1, ey_b, 0], color=WHITE, stroke_width=4)
        t1 = lab("expected 3 : 1", 32, WHITE, [4.5, 2.9, 0])
        self.play(Create(dg), Create(db), FadeIn(t1), run_time=1.2)
        self.at("but not exactly")
        t2 = lab("counted 2.96 : 1", 32, YEL, [4.5, 2.2, 0])
        self.play(FadeIn(t2), run_time=0.8)
        self.at("real counts")
        box = RoundedRectangle(corner_radius=0.15, width=3.2, height=2.2, stroke_color=GREY, stroke_width=3).move_to([4.5, 0.2, 0])
        dl = DashedLine([2.95, 0.2, 0], [6.05, 0.2, 0], color=WHITE, stroke_width=4)
        top = 0.2 + 19 * SC * 30
        bb = Rectangle(width=1.6, height=top - (0.2 - 1.1), stroke_color=BROWN, fill_color=BROWN, fill_opacity=0.8).move_to([4.5, (top + 0.2 - 1.1) / 2, 0])
        zl = lab("zoomed in", 26, GREY, [4.5, -1.3, 0])
        self.play(FadeIn(box), FadeIn(bb), Create(dl), FadeIn(zl), run_time=1.0)
        e1 = lab("expected 1,831", 28, WHITE, [4.5, -2.0, 0])
        e2 = lab("counted 1,850", 28, BROWN, [4.5, -2.6, 0])
        self.play(FadeIn(e1), run_time=0.5)
        self.play(FadeIn(e2), run_time=0.5)
        self.finish()


class S18Idea(SpokenScene):
    def construct(self):
        # column 1: plant with two copies
        pl = plant_at(-4.6, -1.2, 1.6, 1.5)
        cp = pair("R", "r").move_to([-4.6, 0.9, 0])
        # column 2: coin and gametes
        th = ValueTracker(0)
        th.add_updater(lambda m, dt: m.increment_value(dt * 5))
        coin = always_redraw(lambda: coin_mob(th.get_value(), np.array([0, 1.4, 0]), 0.8))
        e = gam("egg", "R", 0.38, 28).move_to([-0.7, -0.4, 0])
        p = gam("pollen", "r", 0.38, 28).move_to([0.7, -0.4, 0])
        # column 3: two copies -> round seed
        c3 = pair("R", "r").move_to([3.7, 0.9, 0])
        arr = Arrow([4.65, 0.9, 0], [5.25, 0.9, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.2)
        sd = alive(seed("round", 0.6).move_to([6.0, 0.9, 0]), 0.05)
        self.add(th)
        self.play(FadeIn(pl), FadeIn(cp), FadeIn(coin), FadeIn(e), FadeIn(p), FadeIn(c3), GrowArrow(arr), GrowFromCenter(sd), run_time=1.6)
        self.at("every pea plant")
        t1 = VGroup(T("Every plant has", 30), T("two copies", 30)).arrange(DOWN, buff=0.1).move_to([-4.6, -2.6, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), Indicate(cp, color=YEL, scale_factor=1.1), run_time=1.0)
        self.at("every egg")
        t2 = VGroup(T("Each egg and pollen", 30), T("grain gets one,", 30), T("by a coin toss", 30)).arrange(DOWN, buff=0.1).move_to([0, -2.6, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=1.0)
        self.at("one round copy")
        t3 = VGroup(T("One round copy", 30), T("is enough to", 30), T("look round", 30)).arrange(DOWN, buff=0.1).move_to([4.6, -2.6, 0])
        self.play(FadeIn(t3, shift=UP * 0.1), Indicate(sd, color=YEL, scale_factor=1.2), run_time=1.0)
        self.finish()


class S19Handoff(SpokenScene):
    def construct(self):
        xs = [-4.0, 0, 4.0]
        seeds = [alive(seed("round", 1.2).move_to([x, 0.2, 0]), 0.06, i) for i, x in enumerate(xs)]
        self.play(LaggedStart(*[GrowFromCenter(s) for s in seeds], lag_ratio=0.3), run_time=1.6)
        self.at("not all")
        self.play(*[Indicate(s, color=YEL, scale_factor=1.08) for s in seeds], run_time=1.2)
        self.at("some hide")
        gh = []
        for n, i in enumerate([0, 2]):
            c = card("r", 0.7, 1.0, 30).move_to([xs[i] + 0.45, -0.35, 0])
            c.set_z_index(-1)
            c._t = n
            c.add_updater(lambda m, dt: (setattr(m, "_t", m._t + dt), m.set_opacity(0.35 + 0.3 * math.sin(3 * m._t))))
            gh.append(c)
        self.play(*[FadeIn(c) for c in gh], run_time=1.0)
        self.at("how could you")
        q = lab("?", 100, YEL, [0, 2.9, 0], weight=BOLD)
        self.play(FadeIn(q, scale=1.3), run_time=0.8)
        self.finish()


class S20End(EndCard):
    LINE = "Pea plants carry two copies; each gamete gets one, by coin toss."
