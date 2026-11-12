"""Two Whites Make Purple (chapter 2 of Extending Mendel). One world: a 4x4 grid of equal boxes (rows = one
parent's gametes AB, Ab, aB, ab; columns = the other's). Same colour map as chapter 1:
PURPLE purple flower, PALE white flower, FRED red flower, PINK pink flower; boxes and genotypes are WHITE
(the fixed deal); lock = GOLD. Gene A steps/letters BLUE, gene B steps/letters GREEN. RED = broken/missing."""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08CB0"
FRED = "#E04656"
PALE = "#D9DCE3"
BLACKC = "#262A34"

BS = 1.5
GC = np.array([-1.0, -0.35, 0.0])
RX = 4.6
GAM = ["AB", "Ab", "aB", "ab"]


def bcell(r, c):
    return GC + np.array([(c - 1.5) * BS, (1.5 - r) * BS, 0])


def geno(r, c):
    g1, g2 = GAM[r], GAM[c]
    a = "".join(sorted([g1[0], g2[0]], key=lambda x: x != "A"))
    b = "".join(sorted([g1[1], g2[1]], key=lambda x: x != "B"))
    return a + b


def colored(r, c):
    g = geno(r, c)
    return "A" in g[:2] and "B" in g[2:]


def pulse(m, f=1.08):
    return m.animate(rate_func=there_and_back).scale(f)


def bob(m, amp=0.05, f=0.5, ph=0.0):
    m._bt = ph

    def up(mm, dt):
        old = np.sin(2 * np.pi * f * mm._bt) * amp
        mm._bt += dt
        mm.shift(UP * (np.sin(2 * np.pi * f * mm._bt) * amp - old))
    m.add_updater(up)
    return m


class W(SpokenScene):
    """SpokenScene plus a few faint drifting motes so the world never sits dead (as in chapter 1)."""

    def setup(self):
        super().setup()
        import random
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        motes = VGroup()
        for _ in range(16):
            d = Dot(radius=rng.uniform(0.03, 0.06), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.15, 0.3))
            d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
            d.v = (rng.uniform(-0.15, 0.15), rng.uniform(0.1, 0.3))

            def drift(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 4.0:
                    m.shift(DOWN * 8.0)
                if abs(m.get_x()) > 7.2:
                    m.shift(LEFT * 14.4 * np.sign(m.get_x()))
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)


def flower(color, s=1.0):
    petals = VGroup()
    for k in range(5):
        a = np.pi / 2 + k * 2 * np.pi / 5
        p = Circle(radius=0.28 * s, stroke_width=2, stroke_color=color, fill_color=color, fill_opacity=0.95)
        p.move_to(0.31 * s * np.array([np.cos(a), np.sin(a), 0]))
        petals.add(p)
    return VGroup(petals, Circle(radius=0.14 * s, stroke_width=0, fill_color=BG, fill_opacity=1))


def plant(color, s=1.0):
    stem = Line([0, -1.0 * s, 0], [0, 0.35 * s, 0], stroke_color=GREEN, stroke_width=5)
    l1 = Ellipse(width=0.5 * s, height=0.22 * s, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.5).rotate(0.5).move_to([-0.28 * s, -0.45 * s, 0])
    l2 = Ellipse(width=0.5 * s, height=0.22 * s, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.5).rotate(-0.5).move_to([0.28 * s, -0.7 * s, 0])
    fl = flower(color, s).move_to([0, 0.6 * s, 0])
    g = VGroup(stem, l1, l2, fl)
    g.fl = fl
    return g


def lock():
    body = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.85, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.3)
    sh = Arc(radius=0.33, start_angle=0, angle=PI, stroke_color=GOLD, stroke_width=7).next_to(body, UP, buff=-0.02)
    return VGroup(sh, body)


def lock_group(y=2.35):
    lk = lock().move_to([RX, y, 0])
    lt = T("deal: fixed", 28, GOLD).move_to([RX, y - 0.95, 0])
    return VGroup(lk, lt)


def token(letter, color, r=0.4, size=30):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3)
    return VGroup(c, T(letter, size, TEXT, weight=BOLD).move_to(c))


def xmark(center, s=0.3, w=7):
    c = np.array(center, dtype=float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], stroke_color=RED, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], stroke_color=RED, stroke_width=w))


# ---------------------------------------------------------------- the 4x4 grid
def chip_colors(state):
    out = []
    for r in range(4):
        for c in range(4):
            g = geno(r, c)
            if state == "97":
                out.append(PURPLE if colored(r, c) else PALE)
            elif state == "151":
                out.append(PALE if g == "aabb" else PURPLE)
            elif state == "121":
                out.append(TEAL if "A" in g[:2] else (GOLD if "B" in g[2:] else PALE))
            else:
                out.append(None)
    return out


def mark_text(r, c):
    g = geno(r, c)
    if colored(r, c):
        return None
    if g == "aabb":
        return "no steps"
    return "no step 1" if g[:2] == "aa" else "no step 2"


class Grid4:
    def __init__(self, state=None, marks=False, tops=True, genos=True):
        self.boxes = VGroup(*[Square(BS, stroke_color=TEXT, stroke_width=2.5).move_to(bcell(r, c)) for r in range(4) for c in range(4)])
        self.tints = VGroup(*[Square(BS - 0.04, stroke_width=0, fill_color=TEXT, fill_opacity=0.0).move_to(bcell(r, c)) for r in range(4) for c in range(4)])
        self.chips = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.15, height=0.34, stroke_width=0, fill_color=TEXT, fill_opacity=0.0).move_to(bcell(r, c) + DOWN * 0.08)
                              for r in range(4) for c in range(4)])
        self.tops = VGroup(*[T(GAM[c], 30).move_to([bcell(0, c)[0], GC[1] + 2 * BS + 0.42, 0]) for c in range(4)])
        self.sides = VGroup(*[T(GAM[r], 30).move_to([GC[0] - 2 * BS - 0.6, bcell(r, 0)[1], 0]) for r in range(4)])
        self.genos = VGroup(*[T(geno(r, c), 26).move_to(bcell(r, c) + UP * 0.42) for r in range(4) for c in range(4)])
        self.marks = VGroup()
        for r in range(4):
            for c in range(4):
                s = mark_text(r, c)
                if s:
                    m = T(s, 22, RED).move_to(bcell(r, c) + DOWN * 0.56)
                    m.idx = r * 4 + c
                    self.marks.add(m)
        self.set_state(state)
        parts = [self.tints, self.boxes, self.chips]
        if tops:
            parts += [self.tops, self.sides]
        if genos:
            parts += [self.genos]
        if marks:
            parts += [self.marks]
        self.all = VGroup(*parts)
        self.motion()

    def set_state(self, state):
        for i, col in enumerate(chip_colors(state)):
            if col is None:
                self.chips[i].set_fill(TEXT, opacity=0.0)
                self.tints[i].set_fill(TEXT, opacity=0.0)
            else:
                self.chips[i].set_fill(col, opacity=0.95)
                self.tints[i].set_fill(col, opacity=0.2)

    def motion(self):
        for k, m in enumerate(list(self.genos) + list(self.tops) + list(self.sides) + list(self.marks)):
            bob(m, 0.04, 0.4, k * 0.37)


def bring_grid(sc, state=None, marks=False):
    G = Grid4(state, marks)
    sc.add(G.all)
    return G


def light(G, i, col, marks=None):
    return [G.chips[i].animate.set_fill(col, opacity=0.95), G.tints[i].animate.set_fill(col, opacity=0.2)]


class Counter(VGroup):
    def __init__(self, label, color, pos, size=40):
        super().__init__()
        self.tr = ValueTracker(0)
        self.label, self.color, self.pos, self.size = label, color, pos, size
        self.m = T(f"{label}: 0", size, color).move_to(pos)
        self.add(self.m)
        self.add_updater(self._up)

    def _up(self, g):
        n = int(round(self.tr.get_value()))
        new = T(f"{self.label}: {n}", self.size, self.color).move_to(self.pos)
        self.m.become(new)


# ---------------------------------------------------------------- pathway
NX = [-4.7, 0.0, 4.7]


def node(x, y, kind, r=0.9):
    if kind == "purple":
        return Circle(radius=r, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.0).move_to([x, y, 0])
    return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to([x, y, 0])


def flow_dots(p0, p1, color, n=3, speed=0.22, stop=None):
    """Dots drifting from p0 to p1 (a pathway step); with `stop` (0..1) they vanish at that fraction."""
    ds = VGroup()
    for k in range(n):
        d = Dot(radius=0.11, color=color)
        d._ph = k / n
        d._t = 0.0
        d.p0, d.p1, d.stop = np.array(p0, float), np.array(p1, float), stop

        def up(m, dt):
            m._t += dt * speed
            u = (m._t + m._ph) % 1.0
            lim = 1.0 if m.stop is None else m.stop
            m.move_to(m.p0 + (m.p1 - m.p0) * u * lim)
            m.set_opacity(min(1.0, u * 6, (1 - u) * 6))
        d.add_updater(up)
        ds.add(d)
    return ds


class Path:
    """colourless -> step 1 (gene A) -> colourless -> step 2 (gene B) -> purple pigment, centred on y."""

    def __init__(self, y, size=36, r=0.9):
        self.y, self.r = y, r
        self.n = [node(NX[0], y, "grey", r), node(NX[1], y, "grey", r), node(NX[2], y, "purple", r)]
        self.a1 = Arrow([NX[0] + r + 0.1, y, 0], [NX[1] - r - 0.1, y, 0], buff=0, color=BLUE, stroke_width=9, max_tip_length_to_length_ratio=0.12)
        self.a2 = Arrow([NX[1] + r + 0.1, y, 0], [NX[2] - r - 0.1, y, 0], buff=0, color=GREEN, stroke_width=9, max_tip_length_to_length_ratio=0.12)
        up = r + 0.35
        self.l1 = T("step 1 (gene A)", size, BLUE).move_to([(NX[0] + NX[1]) / 2, y + up, 0])
        self.l2 = T("step 2 (gene B)", size, GREEN).move_to([(NX[1] + NX[2]) / 2, y + up, 0])
        dn = r + 0.4
        self.nl = [T("colorless", size - 2, GREY).move_to([NX[0], y - dn, 0]),
                   T("colorless", size - 2, GREY).move_to([NX[1], y - dn, 0]),
                   T("purple", size - 2, PURPLE).move_to([NX[2], y - dn, 0])]
        self.first = VGroup(self.n[0], self.nl[0])
        self.step1 = VGroup(self.a1, self.l1)
        self.mid = VGroup(self.n[1], self.nl[1])
        self.step2 = VGroup(self.a2, self.l2)
        self.last = VGroup(self.n[2], self.nl[2])
        self.all = VGroup(self.first, self.step1, self.mid, self.step2, self.last)

    def p(self, i, side):
        return np.array([NX[i] + (self.r + 0.15 if side > 0 else -self.r - 0.15), self.y, 0])


def shifted_path(path, dy):
    path.all.shift(UP * dy)
    path.y += dy


# ---------------------------------------------------------------- the cross world (s01-s04)
PL, PR = -4.5, 4.5
PY = 0.4
PS = 1.8
HX = [-2.6, -1.3, 0.0, 1.3, 2.6]
HY = -2.35


def parents():
    p1 = plant(PALE, PS).move_to([PL, PY, 0])
    p2 = plant(PALE, PS).move_to([PR, PY, 0])
    bob(p1, 0.05, 0.4, 0)
    bob(p2, 0.05, 0.4, 1)
    return p1, p2


def hybrids():
    hs = VGroup(*[plant(PURPLE, 0.95).move_to([x, HY, 0]) for x in HX])
    for i, h in enumerate(hs):
        bob(h, 0.04, 0.45, i * 0.6)
    return hs


def cross_arrow():
    return Arrow([0, 0.1, 0], [0, -1.25, 0], buff=0, color=GREY, stroke_width=6)


def cross_world(sc, with_cross=False, with_hyb=True, with_card=False, with_labels=True):
    p1, p2 = parents()
    sc.add(p1, p2)
    out = {"p1": p1, "p2": p2}
    if with_hyb:
        hs = hybrids()
        ar = cross_arrow()
        lab = T("every hybrid:\npurple", 28, PURPLE).move_to([5.5, HY, 0])
        sc.add(hs, ar, lab)
        out.update(hs=hs, ar=ar, lab=lab)
    if with_labels:
        t1 = T("white, bred true", 26, GREY).move_to([PL, 3.2, 0])
        t2 = T("white, bred true", 26, GREY).move_to([PR, 3.2, 0])
        sc.add(t1, t2)
    if with_cross:
        x = T("×", 64, GREY).move_to([0, 0.9, 0])
        sc.add(x)
        out["x"] = x
    if with_card:
        out["card"] = card()
        sc.add(out["card"])
    return out


def card():
    box = RoundedRectangle(corner_radius=0.2, width=5.0, height=1.5, stroke_color=GOLD, stroke_width=3, fill_color=BG, fill_opacity=0.95)
    t = T("White × white\ngives purple. How?", 32, TEXT)
    t.move_to(box)
    return VGroup(box, t).move_to([0, 0.9, 0])


# ================================================================ scenes
class S00Title(TitleCard):
    TITLE = "Two Whites Make Purple"
    LESSON = "Extending Mendel"


class S01Hook(W):
    def construct(self):
        p1, p2 = parents()
        self.play(FadeIn(p1, shift=UP * 0.3), FadeIn(p2, shift=UP * 0.3), run_time=1.5)
        q = T("?", 140, PURPLE, weight=BOLD).move_to([0, 0.4, 0])
        self.at("purple child")
        self.play(FadeIn(q, scale=0.6), run_time=0.9)
        self.at("Over a century ago")
        self.play(FadeOut(q), run_time=0.8)
        tag = T("Bateson, Saunders and Punnett,\nsweet peas, early 1900s", 30, GREY).move_to([0, 3.2, 0])
        self.at("William Bateson")
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=1.2)
        self.at("bred sweet peas")
        self.play(Indicate(p1.fl, scale_factor=1.25, color=PALE), Indicate(p2.fl, scale_factor=1.25, color=PALE), run_time=1.4)
        self.at("Mendel's rules")
        self.play(Indicate(tag, scale_factor=1.05, color=TEXT), run_time=1.0)
        self.finish()


class S02Cross(W):
    def construct(self):
        p1, p2 = parents()
        self.add(p1, p2)
        x = T("×", 64, GREY).move_to([0, 0.9, 0])
        self.at("They crossed")
        self.play(FadeIn(x, scale=0.5), run_time=1.0)
        t1 = T("white, bred true", 26, GREY).move_to([PL, 3.2, 0])
        t2 = T("white, bred true", 26, GREY).move_to([PR, 3.2, 0])
        self.at("Each strain bred true")
        self.play(FadeIn(t1, shift=DOWN * 0.15), FadeIn(t2, shift=DOWN * 0.15), run_time=1.2)
        self.at("giving only white flowers")
        self.play(Indicate(p1.fl, scale_factor=1.25, color=PALE), Indicate(p2.fl, scale_factor=1.25, color=PALE), run_time=1.4)
        ar = cross_arrow()
        hs = hybrids()
        self.at("Yet every hybrid")
        self.play(Create(ar), LaggedStart(*[FadeIn(h, shift=UP * 0.5) for h in hs], lag_ratio=0.15), run_time=1.2)
        lab = T("every hybrid:\npurple", 28, PURPLE).move_to([5.5, HY, 0])
        self.at("purple flowers")
        self.play(FadeIn(lab, shift=LEFT * 0.2), *[Indicate(h.fl, scale_factor=1.3, color=PURPLE) for h in hs], run_time=1.5)
        self.finish()


class S03Predict(W):
    def construct(self):
        cross_world(self)
        cd = card()
        self.at("How can two white parents")
        self.play(FadeIn(cd, scale=0.85), run_time=1.0)
        self.play(Indicate(cd[1], scale_factor=1.06, color=GOLD), run_time=1.2)
        self.finish()


class S04Pause(W):
    def construct(self):
        cross_world(self)
        self.add(card())
        ring = Circle(radius=0.4, stroke_color=GOLD, stroke_width=7).move_to([6.0, -3.1, 0])
        self.add(ring)
        self.play(Uncreate(ring), run_time=4.7, rate_func=linear)
        self.finish()


class S05Model(W):
    def construct(self):
        old = cross_world(self, with_card=True)
        pa = Path(0.2)
        tag = chip("model", GOLD, 32).move_to([0, 3.0, 0])
        self.at("Here is the simplest model")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if not isinstance(m, Dot)], run_time=1.0)
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.8)
        self.at("Suppose color is made")
        self.play(FadeIn(pa.first, scale=0.8), run_time=0.5)
        self.play(GrowArrow(pa.a1), FadeIn(pa.l1), run_time=0.7)
        self.play(FadeIn(pa.mid, scale=0.8), run_time=0.4)
        self.play(GrowArrow(pa.a2), FadeIn(pa.l2), run_time=0.7)
        self.play(FadeIn(pa.last, scale=0.8), run_time=0.5)
        d1 = flow_dots(pa.p(0, 1), pa.p(1, -1), TEXT)
        d2 = flow_dots(pa.p(1, 1), pa.p(2, -1), PURPLE)
        self.add(d1, d2)
        self.at("Each step needs")
        self.play(Indicate(pa.a1, color=BLUE, scale_factor=1.15), Indicate(pa.a2, color=GREEN, scale_factor=1.15), run_time=1.4)
        self.at("a different gene")
        self.play(Indicate(pa.l1, color=BLUE, scale_factor=1.12), Indicate(pa.l2, color=GREEN, scale_factor=1.12), run_time=1.4)
        self.finish()


def two_rows(sc, ytop=1.5, ybot=-1.5):
    """Left-parent row and right-parent row of the pathway, no steps broken yet."""
    rows = []
    for y, px in ((ytop, -6.35), (ybot, -6.35)):
        pa = Path(y, size=24)
        pl = plant(PALE, 0.5).move_to([px, y + 0.1, 0])
        rows.append((pa, pl))
    return rows


class S06Blocks(W):
    def construct(self):
        pa = Path(0.2)
        tag = chip("model", GOLD, 32).move_to([0, 3.0, 0])
        self.add(tag, pa.all)
        d1 = flow_dots(pa.p(0, 1), pa.p(1, -1), TEXT)
        d2 = flow_dots(pa.p(1, 1), pa.p(2, -1), PURPLE)
        self.add(d1, d2)
        yt, yb = 1.55, -1.65
        top = Path(yt, size=28, r=0.65)
        bot = Path(yb, size=28, r=0.65)
        pl1 = plant(PALE, 0.75).move_to([-6.3, yt + 0.05, 0])
        pl2 = plant(PALE, 0.75).move_to([-6.3, yb + 0.05, 0])
        self.at("One white strain")
        self.play(FadeOut(tag), FadeOut(pa.all), FadeOut(d1), FadeOut(d2), run_time=0.6)
        self.play(FadeIn(top.all), FadeIn(pl1), run_time=0.8)
        t1 = flow_dots(top.p(0, 1), top.p(1, -1), TEXT, stop=0.5)
        self.add(t1)
        mx1 = (NX[0] + NX[1]) / 2
        mx2 = (NX[1] + NX[2]) / 2
        x1 = xmark([mx1, yt, 0], 0.35)
        aa = T("aa", 32, RED, weight=BOLD).move_to([mx1, yt - 0.55, 0])
        self.at("broken at step one")
        self.play(Create(x1), FadeIn(aa, shift=UP * 0.1), run_time=0.8)
        self.at("The other is broken")
        self.play(FadeIn(bot.all), FadeIn(pl2), run_time=0.8)
        b1 = flow_dots(bot.p(0, 1), bot.p(1, -1), TEXT)
        b2 = flow_dots(bot.p(1, 1), bot.p(2, -1), PURPLE, stop=0.5)
        self.add(b1, b2)
        x2 = xmark([mx2, yb, 0], 0.35)
        bb = T("bb", 32, RED, weight=BOLD).move_to([mx2, yb - 0.55, 0])
        self.at("broken at step two")
        self.play(Create(x2), FadeIn(bb, shift=UP * 0.1), run_time=0.8)
        self.at("Neither can finish")
        nl1 = T("no pigment", 26, RED).move_to(top.nl[2].get_center())
        nl2 = T("no pigment", 26, RED).move_to(bot.nl[2].get_center())
        self.play(Indicate(top.n[2], color=RED, scale_factor=1.25), Indicate(bot.n[2], color=RED, scale_factor=1.25), run_time=1.4)
        self.at("pigment on its own")
        self.play(FadeTransform(top.nl[2], nl1), FadeTransform(bot.nl[2], nl2), run_time=1.0)
        self.finish()


class S07Hybrid(W):
    def construct(self):
        pa = Path(0.2)
        pl = plant(PALE, 0.8).move_to([-6.3, 0.2, 0])
        self.add(pa.all, pl)
        d1 = flow_dots(pa.p(0, 1), pa.p(1, -1), TEXT)
        d2 = flow_dots(pa.p(1, 1), pa.p(2, -1), PURPLE)
        self.add(d1, d2)
        self.at("The hybrid gets")
        gt = T("AaBb", 56, TEXT).move_to([0, 2.9, 0])
        self.play(FadeIn(gt, shift=DOWN * 0.2), run_time=1.0)
        ta = token("A", BLUE, 0.5, 36).move_to([(NX[0] + NX[1]) / 2, -1.5, 0])
        tb = token("B", GREEN, 0.5, 36).move_to([(NX[1] + NX[2]) / 2, -1.5, 0])
        ca = T("from right parent", 26, GREY).move_to([ta.get_x(), -2.45, 0])
        cb = T("from left parent", 26, GREY).move_to([tb.get_x(), -2.45, 0])
        self.at("one working copy of each step")
        self.play(FadeIn(ta, shift=UP * 0.3), FadeIn(tb, shift=UP * 0.3), run_time=1.2)
        self.at("one from each parent")
        self.play(FadeIn(ca, shift=UP * 0.1), FadeIn(cb, shift=UP * 0.1), run_time=1.0)
        self.at("One copy of each is enough")
        self.play(pa.a1.animate.set_stroke(width=14), pa.a2.animate.set_stroke(width=14), Indicate(ta, scale_factor=1.2), Indicate(tb, scale_factor=1.2), run_time=1.6)
        self.at("so the hybrid makes color")
        self.play(pa.n[2].animate.set_fill(PURPLE, opacity=0.9), pl.fl.animate.set_color(PURPLE), run_time=1.8)
        self.at("Each parent brings")
        self.play(Indicate(ca, color=TEXT, scale_factor=1.1), Indicate(cb, color=TEXT, scale_factor=1.1), run_time=1.3)
        self.at("the other one lacks")
        self.play(Indicate(ta, scale_factor=1.25), Indicate(tb, scale_factor=1.25), run_time=1.2)
        self.finish()


GX = [-1.6, 0.8, 3.2, 5.6]


def gamete_row(y=0.2, with_frac=True):
    toks = VGroup(*[token(g, TEAL, 0.7, 34).move_to([x, y, 0]) for g, x in zip(GAM, GX)])
    fr = VGroup(*[T("1/4", 32, GOLD).move_to([x, y - 1.2, 0]) for x in GX]) if with_frac else VGroup()
    return toks, fr


class S08Self(W):
    def construct(self):
        hp = plant(PURPLE, 1.9).move_to([-5.0, 0.0, 0])
        bob(hp, 0.05, 0.4)
        self.add(hp)
        sa = CurvedArrow(hp.get_top() + LEFT * 0.8 + UP * 0.1, hp.get_top() + RIGHT * 0.8 + UP * 0.1, angle=-PI * 0.9, color=PINK)
        self.at("pollinate themselves")
        self.play(Create(sa), run_time=1.6)
        toks, fr = gamete_row()
        t1 = T("the deal: now two genes", 32, GOLD).move_to([2.2, 2.9, 0])
        self.at("Now the deal covers")
        self.play(FadeIn(t1, shift=DOWN * 0.2), run_time=1.0)
        t2 = T("unlinked", 32, TEAL).move_to([2.2, 2.15, 0])
        self.at("The genes are unlinked")
        self.play(FadeIn(t2, shift=DOWN * 0.2), run_time=0.9)
        for t in toks:
            t.save = t.get_center().copy()
            t.move_to(hp.get_center() + RIGHT * 1.2)
            t.set_opacity(0)
        self.at("each hybrid makes four")
        self.play(LaggedStart(*[t.animate.move_to(t.save).set_opacity(1) for t in toks], lag_ratio=0.3), run_time=2.4)
        self.at("equally often")
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in fr], lag_ratio=0.2), run_time=1.4)
        self.finish()


class S09Grid(W):
    def construct(self):
        hp = plant(PURPLE, 1.9).move_to([-5.0, 0.0, 0])
        toks, fr = gamete_row()
        self.add(hp, toks, fr)
        G = Grid4(None, genos=False)
        self.at("Pair them")
        self.play(FadeOut(hp), FadeOut(fr), FadeIn(G.boxes), *[toks[i].animate.move_to(G.tops[i].get_center()) for i in range(4)], run_time=1.1)
        self.play(FadeOut(toks), FadeIn(G.tops), FadeIn(G.sides), run_time=0.4)
        self.at("16 equally likely boxes")
        self.play(LaggedStart(*[FadeIn(g, scale=1.2) for g in G.genos], lag_ratio=0.1), run_time=1.8)
        for k, m in enumerate(list(G.genos)):
            bob(m, 0.04, 0.4, k * 0.37)
        lk = lock_group()
        self.at("Nothing about the deal")
        self.play(FadeIn(lk, scale=0.6), run_time=1.1)
        self.finish()


class S10Glow(W):
    def construct(self):
        G = bring_grid(self)
        lk = lock_group()
        self.add(lk)
        ct = Counter("colored", PURPLE, [RX, 0.3, 0])
        self.add(ct)
        self.at("Light up every box")
        idx = [r * 4 + c for r in range(4) for c in range(4) if colored(r, c)]
        tag = T("an A and a B", 28, GOLD).move_to([RX, -0.6, 0])
        anims = []
        for k, i in enumerate(idx):
            self.play(*light(G, i, PURPLE), ct.tr.animate.set_value(k + 1), run_time=0.45)
            if k == 2:
                pass
        self.at("Those boxes glow")
        self.play(pulse(G.chips, 1.12), FadeIn(tag), run_time=1.4)
        self.finish()


class S11White(W):
    def construct(self):
        G = bring_grid(self, "97")
        for i in range(16):
            r, c = divmod(i, 4)
            if not colored(r, c):
                G.chips[i].set_fill(TEXT, opacity=0.0)
                G.tints[i].set_fill(TEXT, opacity=0.0)
        lk = lock_group()
        ct = Counter("colored", PURPLE, [RX, 0.3, 0])
        ct.tr.set_value(9)
        ct2 = Counter("white", PALE, [RX, -0.6, 0])
        self.add(lk, ct, ct2)
        idx = [r * 4 + c for r in range(4) for c in range(4) if not colored(r, c)]
        self.at("Each of the other boxes")
        self.play(*[Indicate(G.boxes[i], color=RED, scale_factor=1.0) for i in idx], run_time=1.4)
        self.at("lacks a working copy")
        marks = {m.idx: m for m in G.marks}
        self.play(LaggedStart(*[FadeIn(marks[i], scale=1.2) for i in idx], lag_ratio=0.15), run_time=2.6)
        self.at("Those boxes are white")
        for k, i in enumerate(idx):
            self.play(*light(G, i, PALE), ct2.tr.animate.set_value(k + 1), run_time=0.14)
        self.finish()


def lit_marks_grid(sc):
    G = Grid4("97", marks=True)
    sc.add(G.all)
    return G


class S12Counts(W):
    def construct(self):
        G = bring_grid(self, "97", marks=True)
        ct = Counter("colored", PURPLE, [RX, 0.3, 0])
        ct.tr.set_value(9)
        ct2 = Counter("white", PALE, [RX, -0.6, 0])
        ct2.tr.set_value(7)
        self.add(ct, ct2)
        ratio = M("9 : 7", 64, GOLD).move_to([RX, 2.4, 0])
        rl = T("colored : white", 28, GREY).move_to([RX, 1.6, 0])
        self.at("Their real flowers")
        self.play(FadeOut(ct), FadeOut(ct2), *[FadeOut(m) for m in G.marks], run_time=1.0)
        self.play(FadeIn(ratio, scale=0.8), FadeIn(rl), run_time=1.2)
        rep = VGroup(T("Report III, 1906:", 26, GOLD), T("two genes, each", 26, TEXT), T("needs a dominant", 26, TEXT),
                     T("allele for color", 26, TEXT)).arrange(DOWN, buff=0.14).move_to([RX, 0.3, 0])
        self.at("Their third report")
        self.play(FadeIn(rep[0], shift=RIGHT * 0.2), run_time=0.8)
        self.at("two genes that both need")
        self.play(FadeIn(rep[1], shift=RIGHT * 0.2), FadeIn(rep[2], shift=RIGHT * 0.2), FadeIn(rep[3], shift=RIGHT * 0.2), run_time=1.6)
        rf = flower(FRED, 0.9).move_to([RX, -1.35, 0])
        bob(rf, 0.05, 0.5)
        note = T("some colored\nplants were red:\na further gene,\nnot in this model", 26, FRED).move_to([RX, -2.85, 0])
        self.at("Some colored plants were red")
        self.play(FadeIn(rf, scale=0.6), run_time=1.0)
        self.at("That took a further gene")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=1.4)
        self.finish()


# -------- the mini grid used beside the chickens and the clue tags
MINI_C = np.array([-5.0, 0.5, 0.0])


def mini_target(G):
    return VGroup(G.tints, G.boxes, G.chips)


def mini_grid():
    G = Grid4("97", tops=False, genos=False)
    g = VGroup(G.tints, G.boxes, G.chips)
    g.scale(3.0 / (4 * BS)).move_to(MINI_C)
    return g


def chicken(comb, s=1.0):
    head = Circle(radius=0.5 * s, stroke_color=PALE, stroke_width=3, fill_color=PALE, fill_opacity=0.15)
    beak = Polygon([0.45 * s, 0.08 * s, 0], [0.85 * s, -0.04 * s, 0], [0.45 * s, -0.2 * s, 0], stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.7)
    eye = Dot([0.15 * s, 0.12 * s, 0], radius=0.06 * s, color=TEXT)
    kw = dict(stroke_color=FRED, stroke_width=3, fill_color=FRED, fill_opacity=0.35)
    if comb == "rose":
        cb = VGroup(*[Circle(radius=0.1 * s, **kw).move_to([(-0.3 + 0.15 * k) * s, (0.58 - 0.04 * abs(k - 2)) * s, 0]) for k in range(5)])
    elif comb == "pea":
        cb = VGroup(*[RoundedRectangle(corner_radius=0.03 * s, width=0.09 * s, height=0.3 * s, **kw).move_to([(-0.2 + 0.2 * k) * s, 0.58 * s, 0]) for k in range(3)])
    elif comb == "walnut":
        cb = VGroup(Ellipse(width=0.8 * s, height=0.4 * s, **kw).move_to([0, 0.6 * s, 0]),
                    Line([-0.15 * s, 0.52 * s, 0], [-0.1 * s, 0.7 * s, 0], stroke_color=FRED, stroke_width=3),
                    Line([0.12 * s, 0.52 * s, 0], [0.17 * s, 0.7 * s, 0], stroke_color=FRED, stroke_width=3))
    else:
        cb = Polygon([-0.3 * s, 0.46 * s, 0], [-0.26 * s, 0.9 * s, 0], [-0.12 * s, 0.62 * s, 0], [0, 0.98 * s, 0], [0.12 * s, 0.62 * s, 0],
                     [0.26 * s, 0.9 * s, 0], [0.3 * s, 0.46 * s, 0], **kw)
    return VGroup(cb, head, beak, eye)


class S13Combs(W):
    def construct(self):
        G = bring_grid(self, "97")
        mg = VGroup(G.tints, G.boxes, G.chips)
        sp = T("sweet peas", 28, GREY).move_to([MINI_C[0], MINI_C[1] - 1.95, 0])
        self.at("They found the same")
        self.play(FadeOut(G.tops), FadeOut(G.sides), FadeOut(G.genos), FadeIn(sp),
                  mg.animate.scale(3.0 / (4 * BS)).move_to(MINI_C), run_time=1.0)
        hd = T("chickens", 40, TEAL).move_to([1.9, 3.1, 0])
        self.at("in chickens")
        self.play(FadeIn(hd, shift=DOWN * 0.2), run_time=0.9)
        h1 = chicken("rose", 1.25).move_to([-1.1, 1.9, 0])
        h2 = chicken("pea", 1.25).move_to([1.5, 1.9, 0])
        xs = T("×", 48, GREY).move_to([0.2, 1.9, 0])
        self.at("Two comb shapes crossed")
        self.play(FadeIn(h1, shift=RIGHT * 0.3), FadeIn(h2, shift=LEFT * 0.3), FadeIn(xs), run_time=1.2)
        ar = Arrow([2.75, 1.9, 0], [3.5, 1.9, 0], buff=0, color=GREY)
        h3 = chicken("walnut", 1.25).move_to([4.6, 1.9, 0])
        self.at("gave a third")
        self.play(GrowArrow(ar), FadeIn(h3, scale=0.7), run_time=1.1)
        row = VGroup(*[chicken(k, 1.1).move_to([x, -0.6, 0]) for k, x in zip(["walnut", "rose", "pea", "single"], [-1.2, 0.9, 3.0, 5.1])])
        self.at("the next generation held four kinds")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in row], lag_ratio=0.25), run_time=1.6)
        rt = M("9 : 3 : 3 : 1", 52, GOLD).move_to([1.95, -2.0, 0])
        self.at("of comb")
        self.play(FadeIn(rt, shift=UP * 0.2), run_time=1.0)
        one = T("one character, two genes", 36, TEAL).move_to([0.2, -3.2, 0])
        self.at("One character can depend")
        self.play(FadeIn(one, shift=UP * 0.2), run_time=1.2)
        self.at("two genes at once")
        self.play(Indicate(one, scale_factor=1.06, color=TEAL), pulse(mg, 1.05), run_time=1.2)
        self.finish()


class S14General(W):
    def construct(self):
        G = bring_grid(self, "97")
        self.at("These are the ordinary")
        ops = chip_colors("97")
        self.play(G.chips.animate.set_opacity(0.12), *[t.animate.set_fill(TEXT, opacity=0.0) for t in G.tints], run_time=1.6)
        lk = lock_group()
        self.at("The pathway never touched")
        self.play(FadeIn(lk, scale=0.6), Indicate(G.boxes, color=GOLD, scale_factor=1.02), run_time=1.6)
        txt = T("same boxes,\nnew labels", 44, TEAL).move_to([RX, -1.0, 0])
        self.at("How the genes act")
        self.play(G.chips.animate.set_opacity(1.0), *[G.tints[i].animate.set_fill(ops[i], opacity=0.2) for i in range(16)], FadeIn(txt, shift=UP * 0.2), run_time=1.8)
        self.at("share a label")
        self.play(pulse(G.chips, 1.1), run_time=1.2)
        self.finish()


class S15Regroup(W):
    def construct(self):
        G = bring_grid(self, "97")
        regroup = lambda st: [anim for i, col in enumerate(chip_colors(st)) for anim in (G.chips[i].animate.set_fill(col, opacity=0.95), G.tints[i].animate.set_fill(col, opacity=0.2))]
        self.at("Change how the genes act")
        self.play(G.chips.animate.shift(UP * 0.15).set_opacity(0.4), run_time=0.8)
        self.at("the same grid regroups")
        self.play(*regroup("121"), G.chips.animate.shift(DOWN * 0.15).set_opacity(1.0), run_time=1.0)
        r121 = M("12 : 3 : 1", 52, GOLD).move_to([RX, 0.9, 0])
        self.play(FadeIn(r121, shift=LEFT * 0.2), run_time=0.8)
        self.wait(0.5)
        self.at("If a dominant allele")
        r151 = M("15 : 1", 64, GOLD).move_to([RX, 0.9, 0])
        self.play(*regroup("151"), FadeTransform(r121, r151), run_time=1.4)
        self.at("only the box with none")
        i0 = 15
        self.play(Indicate(G.boxes[i0], color=GOLD, scale_factor=1.15), Indicate(G.chips[i0], scale_factor=1.3, color=PALE), run_time=1.4)
        self.finish()


class S16Epistatic(W):
    def construct(self):
        G = bring_grid(self, "97")
        w = T("epistatic", 56, TEXT, font=TITLE_FONT).move_to([RX, 1.5, 0])
        fit(w, max_w=3.4)
        gl = T("a gene that\nhides the effect\nof another", 26, GREY).move_to([RX, 0.1, 0])
        self.at("epistatic")
        self.play(Write(w), run_time=1.4)
        self.at("a gene that hides")
        self.play(FadeIn(gl, shift=UP * 0.2), run_time=1.4)
        self.at("the effect of another")
        self.play(pulse(G.chips, 1.1), run_time=1.4)
        self.finish()


class S17Close(W):
    def construct(self):
        mg = mini_grid()
        sp = T("sweet peas", 28, GREY).move_to([MINI_C[0], MINI_C[1] - 1.95, 0])
        self.add(mg, sp)
        self.at("Look at the second generation")
        self.play(pulse(mg, 1.06), run_time=1.4)
        self.at("like this one")
        self.play(pulse(mg, 1.06), run_time=1.2)
        tags = [("9 : 7", -2.2), ("15 : 1", 0.85), ("12 : 3 : 1", 4.3)]
        mobs = []
        self.at("There, a ratio")
        for s_, x in tags:
            m = T(s_, 52, GOLD).move_to([x, 0.9, 0])
            sub = T("/16", 32, GREY).move_to([x, 0.15, 0])
            mobs.append(VGroup(m, sub))
            self.play(FadeIn(m, shift=UP * 0.2), FadeIn(sub), run_time=0.5)
        row = VGroup(*mobs)
        br = Brace(row, DOWN, color=TEAL, buff=0.2)
        self.at("with fewer than four classes")
        self.play(Indicate(row, scale_factor=1.05, color=GOLD), run_time=1.3)
        cl = T("clue: two unlinked genes, one trait", 38, TEAL).next_to(br, DOWN, buff=0.3)
        cl.set_x(row.get_center()[0])
        self.at("is a clue")
        self.play(GrowFromCenter(br), run_time=0.9)
        self.at("Two unlinked genes")
        self.play(FadeIn(cl, shift=UP * 0.2), run_time=1.4)
        self.finish()


class S18End(EndCard):
    LINE = "Same sixteen boxes; how the genes act decides the labels."
