"""Putting the Switch on Trial (evolution of development, film 2), Biochemistrypedia film.

Same look and colour map as film 1 (../scenes.py).
COLOR MAP (both films)
  BLUE   = marine fish and anything marine
  ORANGE = Paxton Lake fish and anything Paxton / pelvic-reduced
  GOLD   = Pitx1 RNA (glows where the gene is used)
  PURPLE = Pitx1 protein (blob)
  GREY-WHITE = DNA, coding block
  TEAL   = enhancer (switch tab)
  GREEN  = reporter marker glow (new in film 2), also tick / on
  RED    = broken / deleted
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
DNA_C = "#B9BFCC"
LARVA = "#C9CED9"
CLK = [0.0]
PEL = (0.1, -0.68)
JAW = (1.4, -0.2)
DNAY = 0.2


def bubbles(sc, n=14, seed=1):
    rng = np.random.RandomState(seed)
    ds = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.03, 0.08), color=TEAL).set_opacity(rng.uniform(0.12, 0.3))
        d.move_to([rng.uniform(-6.9, 6.9), rng.uniform(-4, 4), 0])
        d.v = (rng.uniform(-0.15, 0.15), rng.uniform(0.25, 0.6))

        def up(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 4.2:
                m.shift(DOWN * 8.4)
        d.add_updater(up)
        ds.add(d)
    ds.set_z_index(-10)
    sc.add(ds)


def start(sc):
    CLK[0] = 0.0
    c = Dot(radius=0.01).set_opacity(0)

    def tk(m, dt):
        CLK[0] += dt
    c.add_updater(tk)
    sc.add(c)
    bubbles(sc)


def bob(m, amp=0.08, sp=1.4):
    m._b = 0.0

    def u(mm, dt):
        d = amp * np.sin(sp * CLK[0])
        mm.shift(UP * (d - mm._b))
        mm._b = d
    m.add_updater(u)
    return m


def pulse(m, amp=0.1, sp=3.2):
    m._f = 1.0

    def u(mm, dt):
        f = 1 + amp * np.sin(sp * CLK[0])
        mm.scale(f / mm._f)
        mm._f = f
    m.add_updater(u)
    return m


def fish(color, pos, s=1.0, pelvis="full"):
    st = dict(stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.22)
    body = Ellipse(width=3.6, height=1.4, **st)
    tail = Polygon([-1.7, 0, 0], [-2.6, 0.65, 0], [-2.6, -0.65, 0], **st)
    eye = Dot([1.2, 0.2, 0], radius=0.07, color=TEXT)
    pel = VGroup()
    if pelvis in ("full", "stub"):
        pel.add(RoundedRectangle(corner_radius=0.06, width=0.6, height=0.2, stroke_width=0,
                                 fill_color=TEXT, fill_opacity=0.9).move_to([PEL[0], PEL[1], 0]))
    if pelvis == "full":
        pel.add(Line([-0.05, -0.72, 0], [-0.5, -1.75, 0], color=TEXT, stroke_width=6),
                Line([0.25, -0.72, 0], [0.1, -1.75, 0], color=TEXT, stroke_width=6))
    g = VGroup(tail, body, eye, pel)
    g.scale(s, about_point=ORIGIN).shift(np.array([pos[0], pos[1], 0]))
    g.s, g.o, g.pel = s, np.array([pos[0], pos[1], 0.0]), pel
    return g


def mini(color, pos, s, spine):
    """Juvenile fish with a pelvic spine of relative length `spine` (0 = none; at most a tiny internal vestige)."""
    f = fish(color, pos, s, "none")
    if spine > 0:
        x0, y0, _ = loc(f, (0.1, -0.68))
        L = 1.05 * spine * s
        f.add(Line([x0 - 0.12 * s, y0, 0], [x0 - 0.45 * s * spine, y0 - L, 0], color=TEXT, stroke_width=6),
              Line([x0 + 0.12 * s, y0, 0], [x0 + 0.05 * s * spine, y0 - L, 0], color=TEXT, stroke_width=6))
    return f


def loc(g, p):
    return g.o + np.array([p[0], p[1], 0]) * g.s


def glow(pt, r=0.3, color=GOLD):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(pt)


def ring(pt, r=0.5, color=RED):
    return Circle(radius=r, stroke_color=color, stroke_width=6, fill_opacity=0).move_to(pt)


def dring(pt, r=0.6, color=TEXT, w=5):
    return DashedVMobject(Circle(radius=r, color=color, stroke_width=w)).move_to(pt)


def blob(color, pos, r=0.5):
    g = VGroup()
    for k, o in [(1, (0, 0)), (0.7, (0.7, 0.4)), (0.65, (-0.7, 0.3)), (0.6, (0.2, -0.7))]:
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=color, fill_opacity=0.9)
              .move_to(np.array([pos[0], pos[1], 0]) + np.array([o[0], o[1], 0]) * r))
    return g


def tickm(pos, color=GREEN, k=1.0):
    p = np.array([pos[0], pos[1], 0])
    return VGroup(Line(p + np.array([-0.25, 0.0, 0]) * k, p + np.array([-0.07, -0.22, 0]) * k),
                  Line(p + np.array([-0.07, -0.22, 0]) * k, p + np.array([0.3, 0.26, 0]) * k)).set_stroke(color, 8)


def dna_line(y):
    return Line([-6.5, y, 0], [6.5, y, 0], color=DNA_C, stroke_width=14)


def coding(y, x=3.6, w=4.2):
    blk = RoundedRectangle(corner_radius=0.12, width=w, height=1.3, stroke_color=DNA_C, stroke_width=3,
                           fill_color="#2B2F3A", fill_opacity=1).move_to([x, y, 0])
    return VGroup(blk, T("Pitx1 coding part", 32).move_to(blk))


def tab(label, x, y, w=3.2, color=TEAL, up=True):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=1.0, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.35 if up else 0.1)
    r.move_to([x, y + 0.65, 0])
    return VGroup(r, T(label, 34).move_to(r))


def gap_tab(cx, cy, w, color, a=0.38, b=0.64, h=0.75, gap_color=RED):
    """A switch tab with a deletion: two pieces and a dashed hole between them."""
    x0 = cx - w / 2
    st = dict(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    left = Rectangle(width=w * a, height=h, **st).move_to([x0 + w * a / 2, cy, 0])
    right = Rectangle(width=w * (1 - b), height=h, **st).move_to([x0 + w * b + w * (1 - b) / 2, cy, 0])
    hole = DashedVMobject(Rectangle(width=w * (b - a), height=h, stroke_color=gap_color, stroke_width=3,
                                    fill_opacity=0)).move_to([x0 + w * (a + b) / 2, cy, 0])
    return VGroup(left, hole, right)


def egg(pos, r=0.85):
    e = Ellipse(width=r * 2, height=r * 2.3, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.25)
    n = Circle(radius=r * 0.35, stroke_width=0, fill_color=ORANGE, fill_opacity=0.5)
    g = VGroup(e, n).move_to([pos[0], pos[1], 0])
    return g


def construct_row(sz=34, buff=0.3):
    a = chip("PelA", TEAL, sz)
    b = chip("minimal promoter", TEXT, sz)
    c = chip("marker gene", GREEN, sz)
    return VGroup(a, b, c).arrange(RIGHT, buff=buff)


# ---------- the map (film 2 scenes 9-11) ----------
LAND = [(-6.5, 3.0), (-3.0, 3.1), (-0.8, 2.9), (-0.6, 0.5), (-0.8, -1.8), (-1.5, -3.0), (-4.0, -3.0), (-5.2, -2.5),
        (-4.6, -1.6), (-5.8, -0.9), (-5.0, 0.0), (-6.3, 0.8), (-5.6, 1.8), (-6.5, 2.3)]
PINS = [(-3.9, 2.2), (-2.2, 1.1), (-4.3, 0.0), (-2.4, -1.1), (-3.6, -2.2)]
ROWY = [2.2, 1.1, 0.0, -1.1, -2.2]
GAPS = [(2.6, 4.4), (2.1, 3.9), (3.0, 5.0), (2.8, 3.6), (2.2, 4.6)]
BAR = (0.9, 6.5)


def make_map():
    land = Polygon(*[[x, y, 0] for x, y in LAND], stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.3)
    land.round_corners(0.35)
    pins = VGroup(*[Dot([x, y, 0], radius=0.2, color=ORANGE) for x, y in PINS])
    return land, pins


def make_bar(i):
    y = ROWY[i]
    x0, x1 = BAR
    g0, g1 = GAPS[i]
    st = dict(stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.4)
    left = Rectangle(width=g0 - x0, height=0.55, **st).move_to([(x0 + g0) / 2, y, 0])
    right = Rectangle(width=x1 - g1, height=0.55, **st).move_to([(g1 + x1) / 2, y, 0])
    hole = DashedVMobject(Rectangle(width=g1 - g0, height=0.55, stroke_color=RED, stroke_width=3, fill_opacity=0)).move_to([(g0 + g1) / 2, y, 0])
    return VGroup(left, hole, right)


def fish_icon(color, x, y, k=1.0):
    st = dict(stroke_width=0, fill_color=color, fill_opacity=0.95)
    b = Ellipse(width=0.34 * k, height=0.2 * k, **st)
    t = Polygon([-0.17 * k, 0, 0], [-0.31 * k, 0.1 * k, 0], [-0.31 * k, -0.1 * k, 0], **st)
    return VGroup(t, b).move_to([x, y, 0])


# ====================================================================================
class S00Title(TitleCard):
    LESSON = "Evolution of development"
    TITLE = "Putting the Switch on Trial"


class S01Link(SpokenScene):
    def construct(self):
        start(self)
        nuc = Ellipse(width=12.2, height=5.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to([0, 0.35, 0])
        wavy = lambda y, c: ParametricFunction(lambda t: np.array([t, y + 0.12 * np.sin(4 * t), 0]), t_range=[-5.3, 5.3], stroke_width=10, color=c)
        bl = wavy(1.45, BLUE)
        orr = wavy(-0.65, ORANGE)
        lb = T("marine copy", 36, BLUE).move_to([-2.8, 2.25, 0])
        lo = T("Paxton copy", 36, ORANGE).move_to([-2.8, 0.15, 0])
        self.play(Create(nuc), run_time=0.6)
        self.at("pinned")
        self.play(Create(bl), Create(orr), FadeIn(lb), FadeIn(lo), run_time=0.7)
        pole = Line([3.3, -0.65, 0], [3.3, 0.7, 0], color=RED, stroke_width=7)
        flag = Polygon([3.3, 0.7, 0], [4.4, 0.4, 0], [3.3, 0.1, 0], stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.9)
        fl = VGroup(pole, flag)
        ft = T("fault on this copy (pelvis)", 34, RED).move_to([0.6, -1.7, 0])
        self.at("the fault on")
        self.play(Create(pole), FadeIn(flag, shift=RIGHT * 0.3), FadeIn(ft), run_time=1.2)
        pulse(flag, 0.08)
        # the larva
        self.at("rna is missing")
        self.play(FadeOut(nuc), FadeOut(bl), FadeOut(orr), FadeOut(lb), FadeOut(lo), FadeOut(fl), FadeOut(ft), run_time=0.5)
        f = fish(ORANGE, (0.9, 0.2), 2.4, "none")
        f.shift(RIGHT * 8)
        self.add(f)
        self.play(f.animate.shift(LEFT * 8), run_time=1.0)
        bob(f)
        gj = glow(loc(f, JAW), 0.4)
        bob(gj)
        self.play(FadeIn(gj, scale=0.3), run_time=0.4)
        self.at("where the pelvis")
        rg = dring(loc(f, PEL), 0.9, TEXT)
        bob(rg)
        self.play(Create(rg), run_time=1.0)
        self.at("so which stretch")
        q = T("?", 130, YELLOW).move_to(loc(f, PEL) + UP * 0.02)
        bob(q)
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        pulse(q, 0.08)
        self.at("how would you")
        hw = T("how would you prove it?", 42, YELLOW).move_to([0.8, 3.2, 0])
        self.play(FadeIn(hw, shift=DOWN * 0.15), run_time=0.9)
        self.at("colors are the same")
        k1 = chip("marine", BLUE, 32).move_to([-4.0, -3.2, 0])
        k2 = chip("Paxton", ORANGE, 32).move_to([-0.4, -3.2, 0])
        k3 = chip("Pitx1 RNA", GOLD, 32).move_to([3.4, -3.2, 0])
        self.play(FadeOut(hw), run_time=0.5)
        self.at("blue for marine")
        self.play(FadeIn(k1, shift=UP * 0.2), run_time=0.7)
        self.at("orange for paxton")
        self.play(FadeIn(k2, shift=UP * 0.2), run_time=0.7)
        self.at("gold for")
        self.play(FadeIn(k3, shift=UP * 0.2), run_time=0.7)
        self.finish()


def dna_world(sc, tab_label="PelA", second=False):
    ln = dna_line(DNAY)
    cd = coding(DNAY)
    return ln, cd


class S02Question(SpokenScene):
    def construct(self):
        start(self)
        ln, cd = dna_world(self)
        g = VGroup(ln, cd).shift(RIGHT * 7)
        self.add(g)
        self.play(g.animate.shift(LEFT * 7), run_time=0.7)
        self.at("the suspect")
        tb = tab("", -1.2, DNAY, 3.2)
        lens = Ellipse(width=4.4, height=2.3, stroke_color=YELLOW, stroke_width=8, fill_color=YELLOW, fill_opacity=0.08).move_to([-1.2, 0.85, 0])
        handle = Line([0.45, 1.4, 0], [1.3, 2.2, 0], color=YELLOW, stroke_width=10)
        sus = chip("Suspect", YELLOW, 34).move_to([0, 3.15, 0])
        self.play(FadeIn(tb, scale=0.6), run_time=0.6)
        self.play(Create(lens), Create(handle), FadeIn(sus), run_time=0.9)
        pulse(lens, 0.03)
        self.at("non coding dna")
        nc = T("noncoding DNA", 34, TEAL).move_to([-2.0, 2.3, 0])
        self.play(FadeIn(nc), run_time=0.8)
        self.at("just upstream")
        ar = Arrow([-1.2, -0.9, 0], [1.3, -0.9, 0], color=TEXT, buff=0, stroke_width=8)
        up = T("upstream", 34, TEXT).move_to([0.1, -1.55, 0])
        self.play(GrowArrow(ar), FadeIn(up), run_time=1.0)
        self.at("first called")
        lab = T("Pel", 34, TEXT).move_to(tb[0])
        self.play(FadeOut(nc), FadeOut(ar), FadeOut(up), FadeIn(lab), run_time=0.8)
        self.at("a second switch")
        t2 = tab("second switch", -5.3, DNAY, 3.0)
        t2[0].set_stroke(TEAL, 3).set_fill(TEAL, 0.12)
        t2[1].set_color(GREY)
        t2[1].scale(28 / 34).move_to(t2[0])
        self.play(FadeIn(t2, shift=RIGHT * 0.4), run_time=1.0)
        self.at("this one became")
        lab2 = T("PelA", 34, TEXT).move_to(tb[0])
        sus2 = chip("Suspect: PelA", YELLOW, 34).move_to([0, 3.15, 0])
        self.play(Transform(lab, lab2), Transform(sus, sus2), tb[0].animate.set_fill(TEAL, 0.8), run_time=1.0)
        self.at("three tests")
        c1 = chip("test 1", TEAL, 34).move_to([-3.2, -2.8, 0])
        c2 = chip("test 2", TEAL, 34).move_to([0, -2.8, 0])
        c3 = chip("test 3", TEAL, 34).move_to([3.2, -2.8, 0])
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.3)
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.3)
        self.play(FadeIn(c3, shift=UP * 0.2), run_time=0.3)
        self.at("on trial")
        self.play(Indicate(sus, color=WHITE), Indicate(tb[0], color=WHITE), run_time=1.2)
        self.finish()


class S03Reporter(SpokenScene):
    def construct(self):
        start(self)
        ln, cd = dna_world(self)
        tb = tab("PelA", -1.2, DNAY, 3.2)
        tb[0].set_fill(TEAL, 0.8)
        hole = DashedVMobject(Rectangle(width=3.2, height=1.0, stroke_color=RED, stroke_width=3, fill_opacity=0)).move_to([-1.2, 0.85, 0])
        t1 = chip("test 1: reporter", YELLOW, 34).move_to([0, 3.3, 0])
        self.add(ln, cd, tb)
        self.at("first test")
        self.play(FadeIn(t1, shift=DOWN * 0.2), run_time=0.8)
        # the cut
        c1 = DashedLine([-2.8, 1.5, 0], [-2.8, -0.9, 0], color=RED, stroke_width=5)
        c2 = DashedLine([0.4, 1.5, 0], [0.4, -0.9, 0], color=RED, stroke_width=5)
        self.at("cut out")
        self.play(Create(c1), Create(c2), run_time=1.0)
        row = construct_row()
        row.move_to([0, 2.0, 0])
        tgt = row[0].get_center()
        self.play(tb.animate.move_to(tgt), FadeIn(hole), FadeOut(c1), FadeOut(c2), run_time=1.4)
        tb.generate_target()
        # the tab is now a chip-sized block in the row: swap in the matching chip
        self.at("join it")
        row[0].move_to(tgt)
        self.play(FadeOut(tb), FadeIn(row[0]), run_time=0.4)
        prom = row[1]
        prom.shift(RIGHT * 4)
        self.add(prom)
        self.at("start signal")
        self.play(prom.animate.shift(LEFT * 4), run_time=1.1)
        sig = T("short start signal", 28, TEXT).move_to([prom.get_center()[0] - 3.85, 1.15, 0])
        self.play(FadeIn(sig), run_time=0.5)
        self.at("visible marker")
        mk = row[2]
        mk.shift(RIGHT * 4)
        self.add(mk)
        self.play(mk.animate.shift(LEFT * 4), run_time=1.1)
        gl = T("glows green", 28, GREEN).move_to([mk.get_center()[0], 1.15, 0])
        self.play(FadeIn(gl), run_time=0.5)
        pulse(mk[0], 0.04)
        self.at("put that into")
        self.play(FadeOut(ln), FadeOut(cd), FadeOut(hole), FadeOut(sig), FadeOut(gl), run_time=0.4)
        emb = Ellipse(width=9.0, height=3.8, stroke_color=LARVA, stroke_width=4, fill_color=LARVA, fill_opacity=0.14).move_to([0, -1.4, 0])
        yolk = Circle(radius=1.2, stroke_color=LARVA, stroke_width=3, fill_color=LARVA, fill_opacity=0.12).move_to([-2.3, -1.4, 0])
        spk = VGroup(*[Dot([x, y, 0], radius=0.07, color=LARVA).set_opacity(0.6) for x, y in
                       [(0.4, -0.5), (1.8, -1.0), (3.0, -0.6), (1.2, -2.2), (3.2, -2.0), (-0.2, -1.6)]])
        embg = VGroup(emb, yolk, spk)
        self.play(FadeIn(embg, shift=UP * 0.3), run_time=0.5)
        bob(embg, 0.05)
        needle = VGroup(Line([0, 1.0, 0], [0, -0.35, 0], color=TEXT, stroke_width=5),
                        Line([-0.25, 1.0, 0], [0.25, 1.0, 0], color=TEXT, stroke_width=9))
        needle.shift(UP * 0.0)
        self.play(row.animate.scale(0.42).move_to([0, 2.3, 0]), FadeIn(needle, shift=DOWN * 0.3), run_time=0.8)
        self.play(needle.animate.shift(DOWN * 0.7), run_time=0.4)
        self.play(FadeOut(row, scale=0.1, target_position=[0, -1.2, 0]), needle.animate.shift(UP * 0.7), run_time=0.5)
        self.play(FadeOut(needle), FadeOut(t1), run_time=0.3)
        self.at("watch where")
        sc = dring([-3.4, -1.4, 0], 1.1, GREEN, 6)
        q = T("where does the marker turn on?", 36, GREEN).move_to([0, 1.2, 0])
        self.play(Create(sc), FadeIn(q), run_time=0.6)
        self.play(sc.animate.shift(RIGHT * 6.8), run_time=2.0)
        self.play(sc.animate.shift(LEFT * 3.4), run_time=1.2)
        self.finish()


def pelvis_tab_pair(sc):
    pass


class S04Result(SpokenScene):
    def construct(self):
        start(self)
        fl = fish(BLUE, (-3.0, -0.5), 1.15, "none")
        fr = fish(ORANGE, (3.9, -0.5), 1.15, "none")
        tl = tab("PelA", -3.0, 1.45, 3.2, BLUE)
        tl[0].set_fill(BLUE, 0.5)
        ll = T("marine PelA reporter", 34, BLUE).move_to([-3.0, 3.2, 0])
        self.at("marine version")
        fl.shift(LEFT * 3)
        self.add(fl)
        self.play(fl.animate.shift(RIGHT * 3), FadeIn(tl), FadeIn(ll), run_time=1.2)
        bob(fl)
        gl = glow(loc(fl, PEL), 0.5, GREEN)
        bob(gl)
        self.at("drove the marker")
        self.play(FadeIn(gl, scale=0.2), run_time=1.0)
        pulse(gl, 0.06)
        self.at("developing pelvis")
        dr = dring(loc(fl, PEL), 0.8, TEXT)
        bob(dr)
        self.play(Create(dr), run_time=0.9)
        # Paxton
        tr = gap_tab(3.9, 2.0, 3.2, ORANGE)
        lr = T("Paxton PelA reporter", 34, ORANGE).move_to([3.9, 3.2, 0])
        self.at("paxton version")
        fr.shift(RIGHT * 3)
        self.add(fr)
        self.play(fr.animate.shift(LEFT * 3), FadeIn(lr), FadeIn(tr[0]), FadeIn(tr[2]), run_time=0.8)
        bob(fr)
        self.at("carries a deletion")
        dl = T("deletion", 34, RED).move_to([3.9, 1.05, 0])
        self.play(Create(tr[1]), FadeIn(dl, shift=DOWN * 0.1), run_time=1.0)
        dk = dring(loc(fr, PEL), 0.8, ORANGE)
        bob(dk)
        self.at("pelvic expression")
        self.play(Create(dk), run_time=0.9)
        self.at("none of the fish")
        n = M("0 of 8", 54, ORANGE).move_to([3.9, -2.9, 0])
        nc = T("fish with pelvic expression", 30, ORANGE).move_to([3.9, -3.55, 0])
        self.play(FadeIn(n, scale=0.7), FadeIn(nc), run_time=1.0)
        self.at("counter shows")
        self.play(Indicate(n, color=WHITE), run_time=1.2)
        self.finish()


def pred_world(with_text=True):
    f = fish(ORANGE, (0.5, -0.5), 2.0, "none")
    tg = gap_tab(0.5, 1.9, 3.2, ORANGE)
    dk = dring(loc(f, PEL), 1.0, ORANGE)
    t1 = T("No glow.", 46, YELLOW).move_to([-3.6, 2.2, 0])
    t2 = T("Does the pelvis need PelA?", 42, YELLOW).move_to([0, 3.3, 0])
    yes = chip("yes", TEXT, 40).move_to([-2.2, -3.0, 0])
    ny = chip("not yet", TEXT, 40).move_to([3.2, -3.0, 0])
    return dict(f=f, tg=tg, dk=dk, t1=t1, t2=t2, yes=yes, ny=ny)


class S05Predict(SpokenScene):
    def construct(self):
        start(self)
        w = pred_world()
        f = w["f"]
        f.shift(RIGHT * 4)
        self.add(f, w["tg"], w["dk"])
        self.play(f.animate.shift(LEFT * 4), run_time=1.2)
        for k in ("f", "dk"):
            bob(w[k])
        self.at("no pelvic glow")
        self.play(FadeIn(w["t1"], shift=DOWN * 0.15), Indicate(w["dk"], color=WHITE), run_time=1.2)
        self.at("does that prove")
        self.play(FadeIn(w["t2"], shift=DOWN * 0.15), run_time=1.0)
        self.play(FadeIn(w["yes"], shift=UP * 0.2), FadeIn(w["ny"], shift=UP * 0.2), run_time=0.8)
        pulse(w["yes"][0], 0.03)
        pulse(w["ny"][0], 0.03)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        start(self)
        w = pred_world()
        self.add(w["f"], w["tg"], w["dk"], w["t1"], w["t2"], w["yes"], w["ny"])
        for k in ("f", "dk"):
            bob(w[k])
        base = Circle(radius=0.55, color=GREY, stroke_width=3).move_to([-5.4, -2.9, 0])
        rg = Circle(radius=0.55, color=YELLOW, stroke_width=8).move_to([-5.4, -2.9, 0]).rotate(PI / 2).flip()
        self.add(base)
        self.play(Create(rg), run_time=4.8, rate_func=linear)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        start(self)
        w = pred_world()
        f = w["f"]
        self.add(f, w["tg"], w["dk"], w["t1"], w["t2"], w["yes"], w["ny"])
        for k in ("f", "dk"):
            bob(w[k])
        self.at("not yet")
        self.play(w["ny"][0].animate.set_fill(YELLOW, 0.6), FadeOut(w["t1"]), FadeOut(w["t2"]), FadeOut(w["yes"]), run_time=1.0)
        self.play(Indicate(w["ny"], color=YELLOW), run_time=0.8)
        cons = VGroup(chip("PelA", TEAL, 28), chip("promoter", TEXT, 28), chip("marker", GREEN, 28)).arrange(RIGHT, buff=0.18)
        cons.scale(0.4).move_to(loc(f, PEL))
        f2 = fish(ORANGE, (4.0, 0.9), 1.0, "none")
        self.at("a reporter shows")
        f.clear_updaters()
        w["dk"].clear_updaters()
        self.add(cons)
        self.play(ReplacementTransform(f, f2), FadeOut(w["dk"]), FadeOut(w["tg"]), FadeOut(w["ny"]), run_time=1.4)
        self.play(cons.animate.scale(2.5).move_to([-3.4, 1.4, 0]), run_time=1.0)
        bob(f2)
        cl = T("construct:", 34, GREEN).move_to([-3.4, 0.25, 0])
        cl2 = T("what the sequence CAN drive", 32, GREEN).move_to([-3.4, -0.35, 0])
        self.at("can drive")
        self.play(FadeIn(cl), FadeIn(cl2), Indicate(cons[2], color=GREEN), run_time=1.0)
        bl = T("the body:", 34, ORANGE).move_to([4.0, -0.35, 0])
        bl2 = T("does form DEPEND on it?", 32, ORANGE).move_to([4.0, -0.95, 0])
        self.at("the body depends")
        self.play(FadeIn(bl), FadeIn(bl2), Indicate(f2, color=WHITE, scale_factor=1.1), run_time=1.2)
        ar = Arrow([-3.4, -2.2, 0], [4.0, -2.2, 0], color=YELLOW, buff=0, stroke_width=8)
        at = T("a different question", 36, YELLOW).move_to([0.3, -3.0, 0])
        self.at("depends on it")
        self.play(GrowArrow(ar), FadeIn(at), run_time=1.2)
        self.at("change the fish")
        self.play(Indicate(f2, color=WHITE, scale_factor=1.15), Indicate(bl, color=WHITE), run_time=1.6)
        self.finish()


class S07bLadder(SpokenScene):
    def construct(self):
        start(self)
        rails = VGroup(Line([-6.5, -3.4, 0], [-6.5, 3.4, 0], color=GREY, stroke_width=6),
                       Line([6.5, -3.4, 0], [6.5, 3.4, 0], color=GREY, stroke_width=6))
        tit = T("each test asks its own question", 40, YELLOW).move_to([0, 0.0, 0])
        self.play(Create(rails[0]), Create(rails[1]), FadeIn(tit), run_time=1.0)
        pulse(tit, 0.03)

        def rung(y, l1, l2, color, icon):
            bx = RoundedRectangle(corner_radius=0.18, width=12.2, height=1.8, stroke_color=color, stroke_width=3,
                                  fill_color=color, fill_opacity=0.14).move_to([0, y, 0])
            tx = VGroup(T(l1, 30, color), T(l2, 36, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            tx.move_to([0, y, 0]).align_to([-4.0, 0, 0], LEFT)
            icon.move_to([-5.2, y, 0])
            return VGroup(bx, tx, icon)
        ic1 = VGroup(Circle(radius=0.45, stroke_width=0, fill_color=GREEN, fill_opacity=0.95))
        t_ = Rectangle(width=1.0, height=0.38, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([0, 0.3, 0])
        sp1 = Line([-0.1, 0.0, 0], [-0.3, -0.55, 0], color=TEXT, stroke_width=6)
        sp2 = Line([0.1, 0.0, 0], [0.2, -0.55, 0], color=TEXT, stroke_width=6)
        ic2 = VGroup(t_, sp1, sp2)
        ic3 = VGroup(Line([-0.8, -0.2, 0], [0.8, -0.2, 0], color=DNA_C, stroke_width=8),
                     Rectangle(width=0.55, height=0.32, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35).move_to([-0.5, 0.2, 0]),
                     Rectangle(width=0.55, height=0.32, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35).move_to([0.5, 0.2, 0]),
                     Line([-0.15, 0.6, 0], [0.15, -0.15, 0], color=RED, stroke_width=5))
        r1 = rung(-2.3, "reporter:", "what CAN it drive?", GREEN, ic1)
        r2 = rung(0.0, "add it back:", "can it restore form?", BLUE, ic2)
        r3 = rung(2.3, "remove it from the animal:", "does form DEPEND on it?", RED, ic3)
        self.at("a reporter asks")
        self.play(FadeOut(tit), FadeIn(r1, shift=UP * 0.3), run_time=0.9)
        pulse(ic1, 0.1)
        self.at("adding the switch back")
        self.play(FadeIn(r2, shift=UP * 0.3), run_time=0.9)
        self.at("removing it from")
        self.play(FadeIn(r3, shift=UP * 0.3), run_time=0.9)
        self.at("depends on it")
        self.play(Indicate(r3[0], color=RED), run_time=1.4)
        self.finish()


class S08Rescue(SpokenScene):
    def construct(self):
        start(self)
        tb = chip("PelA", BLUE, 48)
        pit = chip("Pitx1", PURPLE, 48)
        cons = VGroup(tb, pit).arrange(RIGHT, buff=0.1).move_to([0, 1.7, 0])
        lab = T("marine PelA + Pitx1", 44, BLUE).move_to([0, 0.0, 0])
        tgt_tb, tgt_pit = tb.get_center().copy(), pit.get_center().copy()
        tb.shift(LEFT * 5)
        pit.shift(UP * 2.5)
        self.add(tb, pit)
        self.at("rescue comes closer")
        self.play(tb.animate.shift(RIGHT * 5), run_time=1.2)
        self.at("marine pell")
        self.play(FadeIn(lab), run_time=0.6)
        self.at("driving pit")
        self.play(pit.animate.shift(DOWN * 2.5), run_time=1.0)
        self.play(Indicate(cons, color=WHITE), run_time=0.8)
        eggs = VGroup(*[egg((x, -0.6)) for x in (-4.0, 0.0, 4.0)])
        self.at("fertilized eggs")
        self.play(FadeIn(eggs, shift=UP * 0.3), FadeOut(lab), run_time=0.9)
        needle = VGroup(Line([-4.0, 1.7, 0], [-4.0, 0.0, 0], color=TEXT, stroke_width=5),
                        Line([-4.25, 1.7, 0], [-3.75, 1.7, 0], color=TEXT, stroke_width=9))
        self.at("another pelvic reduced")
        self.play(FadeIn(needle), cons.animate.scale(0.5).move_to([-4.0, 2.7, 0]), run_time=0.8)
        self.play(needle.animate.shift(DOWN * 0.5), run_time=0.4)
        self.play(needle.animate.shift(UP * 0.5), eggs[0][1].animate.set_fill(BLUE, 0.9), run_time=0.4)
        tag1 = T("Bear Paw Lake, Alaska", 36, ORANGE).move_to([0, -2.5, 0])
        tag2 = T("(another pelvic-reduced population)", 30, ORANGE).move_to([0, -3.1, 0])
        self.play(FadeIn(tag1), FadeIn(tag2), FadeOut(needle), FadeOut(cons), run_time=0.6)
        self.play(eggs[1][1].animate.set_fill(BLUE, 0.9), eggs[2][1].animate.set_fill(BLUE, 0.9), run_time=0.5)
        # uninjected row
        self.at("those fish normally")
        ra = VGroup(*[mini(ORANGE, (x, 1.8), 0.8, 0) for x in (-4.0, 0.0, 4.0)])
        la = T("normally: no pelvic spine", 34, ORANGE).move_to([0, 3.25, 0])
        self.play(FadeOut(tag1), FadeOut(tag2), FadeIn(ra, shift=DOWN * 0.3), FadeIn(la), run_time=1.2)
        for m in ra:
            bob(m, 0.05)
        for e in eggs:
            bob(e, 0.05)
        self.at("compared with uninjected")
        la2 = T("uninjected siblings", 34, ORANGE).move_to(la)
        self.play(Transform(la, la2), Indicate(ra, color=WHITE, scale_factor=1.05), run_time=1.2)
        # injected row hatches from the eggs
        rb = VGroup(mini(ORANGE, (-4.0, -0.7), 0.8, 1.0), mini(ORANGE, (0.0, -0.7), 0.8, 0.45), mini(ORANGE, (4.0, -0.7), 0.8, 0))
        lb = T("injected", 34, BLUE).move_to([0, 0.5, 0])
        self.at("pelvic spine growth")
        for e in eggs:
            e.clear_updaters()
        self.play(*[ReplacementTransform(e, m) for e, m in zip(eggs, rb)], FadeIn(lb), run_time=1.4)
        for m in rb:
            bob(m, 0.05)
        vt = T("variable", 46, YELLOW).move_to([0, -3.3, 0])
        self.at("variably enhanced")
        self.play(FadeIn(vt, scale=0.8), run_time=0.8)
        self.play(Indicate(rb, color=WHITE, scale_factor=1.05), run_time=1.2)
        self.finish()


class S09Map(SpokenScene):
    def construct(self):
        start(self)
        land, pins = make_map()
        sch = T("schematic", 28, TEXT).move_to([-3.6, -3.5, 0])
        self.at("now the wild")
        self.play(FadeIn(land), run_time=1.2)
        self.play(FadeIn(sch), run_time=0.5)
        pl = T("PelA", 34, ORANGE).move_to([3.7, -3.3, 0])
        self.at("many pelvic reduced")
        for p in pins:
            self.play(FadeIn(p, scale=0.2), run_time=0.45)
        self.play(FadeIn(pl), run_time=0.4)
        bars = [make_bar(i) for i in range(5)]
        links = [DashedLine([PINS[i][0] + 0.25, PINS[i][1], 0], [BAR[0] - 0.05, ROWY[i], 0], color=ORANGE, stroke_width=2) for i in range(5)]
        self.at("deletions at")
        for i in range(5):
            self.play(Create(links[i]), FadeIn(bars[i][0]), FadeIn(bars[i][2]), run_time=0.35)
            self.play(Create(bars[i][1]), run_time=0.25)
        self.at("differ in where")
        for i in range(5):
            self.play(Indicate(bars[i][1], color=RED), run_time=0.5)
        self.at("same switch was lost")
        dl = DashedLine([3.3, 3.0, 0], [3.3, -2.9, 0], color=YELLOW, stroke_width=6)
        ss = T("same switch", 36, YELLOW).move_to([3.3, 3.4, 0])
        self.play(Create(dl), FadeIn(ss), run_time=1.4)
        self.at("more than once")
        self.play(*[Indicate(p, color=WHITE, scale_factor=1.8) for p in pins], run_time=1.4)
        self.finish()


class S10Tally(SpokenScene):
    def construct(self):
        start(self)
        land, pins = make_map()
        mp = VGroup(land, pins)
        self.add(mp)
        self.at("in one survey")
        self.play(mp.animate.scale(0.42).move_to([-5.1, 2.35, 0]), run_time=1.3)
        sv = T("one survey", 38, TEXT).move_to([0.4, 3.1, 0])
        self.play(FadeIn(sv), run_time=0.5)
        x0 = -6.0
        p1 = RoundedRectangle(corner_radius=0.2, width=12.6, height=1.8, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.12).move_to([0, 0.1, 0])
        p2 = RoundedRectangle(corner_radius=0.2, width=12.6, height=1.8, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.12).move_to([0, -1.9, 0])
        l1 = T("pelvic-reduced populations", 32, ORANGE).move_to([x0, 0.5, 0], aligned_edge=LEFT)
        l1.align_to([x0 + 0.1, 0, 0], LEFT)
        row1 = [fish_icon(ORANGE, x0 + 0.25 + i * 0.5, -0.3, 1.0) for i in range(13)]
        self.at("deletions turned up")
        self.play(FadeIn(p1), FadeIn(l1), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in row1], lag_ratio=0.12), run_time=1.8)
        marks = [Square(0.16, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([m.get_x(), 0.0, 0]) for m in row1[:9]]
        self.at("as the tally")
        self.play(LaggedStart(*[FadeIn(k, scale=0.3) for k in marks], lag_ratio=0.1), run_time=1.4)
        c1 = M("9 of 13", 40, RED).move_to([4.7, 0.5, 0])
        self.play(FadeIn(c1, scale=0.8), run_time=0.7)
        key = VGroup(Square(0.16, stroke_width=0, fill_color=RED, fill_opacity=1), T("gap in PelA", 28, RED)).arrange(RIGHT, buff=0.15).move_to([3.0, 3.1, 0])
        self.play(FadeIn(key), run_time=0.5)
        l2 = T("pelvis-complete populations", 32, BLUE).move_to([x0, -1.5, 0], aligned_edge=LEFT)
        l2.align_to([x0 + 0.1, 0, 0], LEFT)
        row2 = [fish_icon(BLUE, x0 + 0.25 + i * 0.5, -2.3, 1.0) for i in range(21)]
        self.at("none of the")
        self.play(FadeIn(p2), FadeIn(l2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in row2], lag_ratio=0.08), run_time=1.9)
        c2 = M("0 of 21", 40, BLUE).move_to([4.7, -1.5, 0])
        self.at("had them")
        self.play(FadeIn(c2, scale=0.8), run_time=0.7)
        self.at("common then")
        self.play(Indicate(c1, color=WHITE), run_time=1.2)
        self.at("not universal")
        self.play(Indicate(VGroup(*row1[9:]), color=WHITE), run_time=1.0)
        tag = T("other routes?", 34, YELLOW).move_to([3.0, -0.3, 0])
        self.at("most of the others")
        self.play(FadeIn(tag, shift=LEFT * 0.2), run_time=0.8)
        pulse(tag, 0.05)
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.5) for m in row1[9:]], run_time=1.2)
        self.at("another route")
        self.play(Indicate(tag, color=WHITE), run_time=1.2)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        start(self)
        land, pins = make_map()
        mp = VGroup(land, pins).scale(0.6).move_to([-4.3, 1.85, 0])
        self.add(mp)
        tg = tab("PelA", 3.0, 1.45, 3.2, ORANGE)
        tg[0].set_fill(ORANGE, 0.6)
        self.at("different deletions")
        self.play(Indicate(pins, color=WHITE, scale_factor=1.6), run_time=1.2)
        lines = VGroup(*[Line(p.get_center(), [1.4, 2.0, 0], color=ORANGE, stroke_width=3) for p in pins])
        self.at("same switch")
        self.play(FadeIn(tg), Create(lines), run_time=1.4)
        # flat
        fb = fish(BLUE, (-3.6, -1.8), 1.0, "full")
        fo = fish(ORANGE, (3.8, -1.8), 1.0, "none")
        gb, go = glow(loc(fb, JAW), 0.24), glow(loc(fo, JAW), 0.24)
        self.at("pelvic reduction")
        self.play(FadeIn(fb, shift=UP * 0.3), FadeIn(fo, shift=UP * 0.3), run_time=1.0)
        self.play(FadeIn(gb, scale=0.3), FadeIn(go, scale=0.3), run_time=0.6)
        for m in (fb, fo, gb, go):
            bob(m, 0.05)
        self.at("again and again")
        self.play(*[Indicate(p, color=ORANGE, scale_factor=1.8) for p in pins], run_time=1.6)
        self.at("losing one enhancer")
        flat = tab("PelA", 3.0, 1.45, 3.2, RED, up=False)
        flat[0].stretch_to_fit_height(0.2).move_to([3.0, 1.8, 0])
        flat[0].set_stroke(RED, 3)
        crack = Line([2.3, 2.8, 0], [3.7, 1.8, 0], color=RED, stroke_width=7)
        self.play(Create(crack), run_time=0.5)
        self.play(Transform(tg[0], flat[0]), tg[1].animate.shift(UP * 0.35), FadeOut(crack), run_time=1.0)
        self.at("in many lakes")
        self.play(*[Indicate(p, color=WHITE, scale_factor=1.6) for p in pins], run_time=1.4)
        self.at("the deletions hit")
        self.play(Indicate(tg, color=RED), run_time=1.3)
        pb = blob(PURPLE, (-0.2, -1.9), 0.4)
        pt = T("Pitx1 protein", 30, PURPLE).move_to([-0.2, -3.3, 0])
        self.at("not the pitx1 protein")
        self.play(GrowFromCenter(pb), FadeIn(pt), run_time=0.9)
        tk = tickm((-0.2, -1.9), GREEN, 1.2)
        self.play(Create(tk), run_time=0.7)
        self.finish()


class S12End(EndCard):
    LINE = "In many lakes, pelvic loss evolved by deleting the same Pitx1 switch."
