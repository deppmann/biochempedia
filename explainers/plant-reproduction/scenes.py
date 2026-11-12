"""Whose Cells Are in a Seed?  (plant-reproduction, Biochemistrypedia explainer)

COLOR MAP (whole film)
  MAGENTA blocks = maternal chromosome sets      TEAL blocks = paternal sets
  GREEN = embryo      CREAM = endosperm      BROWN = seed coat (integuments)
  ORANGE = fruit wall (ovary wall)           PALE YELLOW = pollen grain and tube
  GREY = structure, signals     TEXT = plain labels
All drawings are flat schematic cartoons; sets are blocks, never molecules.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

MAG = "#E040C8"
PAT = TEAL
EMBC = GREEN
ENDC = "#E9D9A0"
COATC = "#A9744A"
FRUITC = "#F29E4C"
POLC = "#F7EC9A"
OX, OY = -2.4, -0.35      # centre of the ovule, the same in every ovule scene
KX, KY = -2.4, -0.1       # centre of the kernel, the same in every kernel scene


def P(x, y):
    return np.array([x, y, 0.0])


def blk(color, w=0.9, h=0.36):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2,
                            fill_color=color, fill_opacity=0.9)


def stack(cols, w=0.9, h=0.36, gap=0.07, empty=0):
    g = VGroup(*[blk(c, w, h) for c in cols])
    for _ in range(empty):
        s = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=PAT, stroke_width=2.5), num_dashes=16)
        g.add(s)
    g.arrange(UP, buff=gap)
    return g


def legend():
    a = VGroup(blk(MAG, 0.5, 0.26), T("mother", 26, MAG)).arrange(RIGHT, buff=0.15)
    b = VGroup(blk(PAT, 0.5, 0.26), T("father", 26, PAT)).arrange(RIGHT, buff=0.15)
    g = VGroup(a, b).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    g.to_corner(UR, buff=0.3)
    return g


def rings(center, color=GREY, r0=0.15, r1=1.0, n=3, period=2.6, sw=3, op=0.8):
    g = VGroup(*[Circle(radius=1, stroke_color=color, stroke_width=sw) for _ in range(n)])
    g.t = 0.0

    def up(m, dt):
        m.t += dt
        for i, c in enumerate(m):
            p = ((m.t / period) + i / n) % 1
            r = r0 + (r1 - r0) * p
            c.set_width(2 * r).move_to(center)
            c.set_stroke(opacity=op * (1 - p))
    g.add_updater(up)
    up(g, 0)
    return g


def motes(center, rx, ry, n=6, color=PAT, seed=1, size=0.05, op=0.55):
    rng = np.random.default_rng(seed)
    g = VGroup(*[Dot(radius=size, color=color).set_opacity(op) for _ in range(n)])
    ph = rng.uniform(0, 6.3, (n, 4))
    sp = rng.uniform(0.5, 1.1, (n, 2))
    g.t = 0.0

    def up(m, dt):
        m.t += dt
        for i, d in enumerate(m):
            d.move_to(center + P(rx * np.sin(sp[i, 0] * m.t + ph[i, 0]), ry * np.sin(sp[i, 1] * m.t + ph[i, 1])))
    g.add_updater(up)
    up(g, 0)
    return g


def bob(m, amp=0.06, per=2.2, ph=0.0):
    base = m.get_center().copy()
    st = [ph]

    def up(mm, dt):
        st[0] += dt
        mm.move_to(base + P(amp * np.sin(6.283 * st[0] / per), amp * np.cos(6.283 * st[0] / (per * 1.3)) ))
    m.add_updater(up)
    return m


def sperm(pos, r=0.3):
    body = Circle(radius=r, stroke_color=PAT, stroke_width=3, fill_color=PAT, fill_opacity=0.4).move_to(pos)
    tag = blk(PAT, r * 1.1, r * 0.45).move_to(body)
    tail = VMobject(stroke_color=PAT, stroke_width=3.5)
    tail.t = 0.0

    def up(m, dt):
        m.t += dt
        c = body.get_center() + LEFT * r
        pts = [c + P(-0.9 * r * 5 * s, 0.22 * r * 3 * np.sin(5 * s * 3 - 4 * m.t) * s) for s in np.linspace(0, 0.2, 8)]
        m.set_points_smoothly(pts)
    tail.add_updater(up)
    up(tail, 0)
    return VGroup(tail, body, tag)


def lab(text, color=TEXT, size=30, **kw):
    return T(text, size, color, **kw)


def leader(a, b, color=GREY):
    return Line(a, b, color=color, stroke_width=2).set_opacity(0.8)


def pooled(t):
    return t


class W(SpokenScene):
    def cue(self, phrase, *anims, rt=0.8, nth=0, lead=0.2):
        self.at(phrase, lead=lead, nth=nth)
        if anims:
            self.play(*anims, run_time=rt)

    def fill(self, phrase, *anims, nth=0, lead=0.2):
        rt = self.t_of(phrase, nth) - lead - self.elapsed()
        if anims:
            self.play(*anims, run_time=max(rt, 0.3))
        elif rt > 0.02:
            self.wait(rt)


# ---------------------------------------------------------------------------------------------
# shared drawings
# ---------------------------------------------------------------------------------------------
def kernel(c=P(KX, KY), w=4.6, h=6.0):
    fw = RoundedRectangle(corner_radius=1.9, width=w, height=h, stroke_width=0, fill_color=FRUITC, fill_opacity=1)
    co = RoundedRectangle(corner_radius=1.75, width=w - 0.3, height=h - 0.3, stroke_width=0, fill_color=COATC, fill_opacity=1)
    en = RoundedRectangle(corner_radius=1.6, width=w - 0.6, height=h - 0.6, stroke_width=0, fill_color=ENDC, fill_opacity=0.95)
    g = VGroup(fw, co, en).move_to(c)
    em = Ellipse(width=1.3, height=1.9, stroke_width=0, fill_color=EMBC, fill_opacity=1).rotate(-0.25).move_to(c + P(0.7, 0.9))
    g.add(em)
    g.fw, g.co, g.en, g.em = fw, co, en, em
    return g


def ovule_shell(thick=1.0):
    a, b, gap = 2.7, 3.2, 0.3
    f = lambda aa, bb: (lambda t: P(OX + aa * np.cos(t), OY + bb * np.sin(t)))
    outer = ParametricFunction(f(a, b), t_range=[PI / 2 + gap, PI / 2 + TAU - gap], stroke_color=COATC, stroke_width=9 * thick)
    inner = ParametricFunction(f(a - 0.3, b - 0.3), t_range=[PI / 2 + gap, PI / 2 + TAU - gap], stroke_color=COATC, stroke_width=6 * thick)
    sac = Ellipse(width=4.0, height=5.4, stroke_color=TEXT, stroke_width=2.5, fill_color=TEXT, fill_opacity=0.06).move_to(P(OX, OY))
    sac.set_stroke(opacity=0.55)
    g = VGroup(outer, inner, sac)
    g.outer, g.inner, g.sac = outer, inner, sac
    return g


EGG = P(OX, 1.35)
SYNL, SYNR = P(OX - 1.05, 1.35), P(OX + 1.05, 1.35)
CCC = P(OX, -0.9)
POL = [P(OX - 0.75, -0.9), P(OX + 0.75, -0.9)]


def cells(egg_block=True, cc_blocks=True, glow_syn=False):
    egg = Circle(radius=0.62, stroke_color=MAG, stroke_width=3, fill_color=MAG, fill_opacity=0.18).move_to(EGG)
    syn = VGroup(*[Ellipse(width=0.75, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to(p) for p in (SYNL, SYNR)])
    cc = Ellipse(width=3.2, height=2.4, stroke_color=MAG, stroke_width=3, fill_color=MAG, fill_opacity=0.1).move_to(CCC)
    g = VGroup(egg, syn, cc)
    g.egg, g.syn, g.cc = egg, syn, cc
    g.egg_lab = lab("egg", TEXT, 26).move_to(EGG + P(0, 0.24))
    g.egg_blk = blk(MAG, 0.7, 0.28).move_to(EGG + P(0, -0.2))
    g.cc_lab = lab("central cell", TEXT, 28).move_to(CCC + P(0.27, 0.5))
    g.cc_b = VGroup(blk(MAG, 0.85, 0.36).move_to(CCC + P(-0.95, -0.25)), blk(MAG, 0.85, 0.36).move_to(CCC + P(0.95, -0.25)))
    g.eq = T("=", 36, TEXT).move_to(CCC + P(0, -0.25))
    return g


def embryo_cartoon(c, s=1.0):
    e = Ellipse(width=1.3 * s, height=1.8 * s, stroke_color=EMBC, stroke_width=3, fill_color=EMBC, fill_opacity=0.85).move_to(c)
    leaf = Ellipse(width=0.45 * s, height=0.8 * s, stroke_width=0, fill_color="#B8E6A0", fill_opacity=0.9).move_to(c + P(0.1 * s, 0.35 * s)).rotate(-0.5)
    return VGroup(e, leaf)


def pollen_grain(c, r=2.4, labels=False):
    """Grain with its cells: big tube cell (the grain), one sperm pair, each carrying one teal block."""
    g = Circle(radius=r, stroke_color=POLC, stroke_width=5, fill_color=POLC, fill_opacity=0.18).move_to(c)
    s1 = Circle(radius=0.62 * r / 2.4 * 1.0, stroke_color=PAT, stroke_width=3, fill_color=PAT, fill_opacity=0.25).move_to(c + P(-0.7 * r / 2.4, 0.9 * r / 2.4))
    s2 = s1.copy().move_to(c + P(0.7 * r / 2.4, 0.9 * r / 2.4))
    k = r / 2.4
    b0 = blk(PAT, 0.9 * k, 0.36 * k).move_to(c + P(0, -1.0 * k))
    b1 = blk(PAT, 0.6 * k, 0.26 * k).move_to(s1)
    b2 = blk(PAT, 0.6 * k, 0.26 * k).move_to(s2)
    return VGroup(g, s1, s2, b0, b1, b2)


def timeline_stack_rows():
    pass


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Double Fertilization: How a Flower Makes a Seed"
    TITLE = "Whose Cells Are in a Seed?"


# ---------------------------------------------------------------------------------------------
class S01Hook(W):
    def construct(self):
        c = P(KX, KY)
        solid = RoundedRectangle(corner_radius=1.9, width=4.6, height=6.0, stroke_width=0, fill_color=FRUITC, fill_opacity=1).move_to(c)
        self.play(FadeIn(solid, scale=0.9), run_time=0.7)
        crack = VMobject(stroke_color=TEXT, stroke_width=5)
        crack.set_points_as_corners([c + P(x, y) for x, y in [(0.1, 3.0), (-0.3, 1.8), (0.3, 0.6), (-0.2, -0.6), (0.25, -1.8), (0, -3.0)]])
        self.play(Create(crack), run_time=0.8)
        K = kernel(c)
        self.play(ReplacementTransform(solid, K), FadeOut(crack), K.animate.scale(1.0), run_time=1.2)
        # regions light up in turn
        rows = [("baby plant", EMBC, 1.7, c + P(0.9, 1.0), "baby plant", K.em),
                ("its food", ENDC, -0.1, c + P(0.4, -0.7), "food", K.en),
                ("a wrapper", FRUITC, -1.9, c + P(2.28, -1.5), "wrapper", K.fw)]
        qs = []
        for ph, col, y, tgt, name, part in rows:
            self.at(ph, lead=0.4)
            l = lab(name, col, 34).move_to(P(2.6 + (0.0), y), aligned_edge=LEFT)
            l.move_to(P(1.4, y), aligned_edge=LEFT)
            ln = leader(P(1.3, y), tgt)
            q = lab("?", TEXT, 46, weight=BOLD).next_to(l, RIGHT, buff=0.3)
            self.play(Indicate(part, color=WHITE, scale_factor=1.06), FadeIn(l, shift=LEFT * 0.2), Create(ln), run_time=0.9)
            self.play(FadeIn(q, scale=1.6), run_time=0.4)
            qs.append(q)
            bob(q, 0.05)
            self.add(q)
        self.cue("which parts", *[Indicate(q, color=PAT, scale_factor=1.4) for q in qs], rt=1.2)
        fa = lab("father?", PAT, 60, weight=BOLD).move_to(P(4.2, -3.1))
        self.cue("the father", Write(fa), rt=0.9)
        self.fill("father", *[q.animate.set_color(PAT) for q in qs])
        self.finish()


class S02Sets(W):
    def construct(self):
        egg = Circle(radius=1.5, stroke_color=MAG, stroke_width=5, fill_color=MAG, fill_opacity=0.15).move_to(P(-3.6, 0.7))
        body = Ellipse(width=2.2, height=1.7, stroke_color=PAT, stroke_width=5, fill_color=PAT, fill_opacity=0.2).move_to(P(3.2, 1.3))
        tail = VMobject(stroke_color=PAT, stroke_width=6)
        tail.t = 0.0

        def up(m, dt):
            m.t += dt
            s0 = body.get_bottom() + DOWN * 0.0
            pts = [s0 + P(0.35 * np.sin(3 * s - 3 * m.t) * s * 1.2, -2.0 * s) for s in np.linspace(0, 1, 14)]
            m.set_points_smoothly(pts)
        tail.add_updater(up)
        up(tail, 0)
        self.play(FadeIn(egg, scale=0.8), FadeIn(body, scale=0.8), FadeIn(tail), run_time=1.2)
        self.add(tail)
        tray_l = VMobject(stroke_color=MAG, stroke_width=5)
        tray_l.set_points_as_corners([P(-4.8, -1.6), P(-4.8, -2.4), P(-2.4, -2.4), P(-2.4, -1.6)])
        tray_r = VMobject(stroke_color=PAT, stroke_width=5)
        tray_r.set_points_as_corners([P(2.0, -1.6), P(2.0, -2.4), P(4.4, -2.4), P(4.4, -1.6)])
        self.fill("one set", FadeIn(tray_l), FadeIn(tray_r))
        bm = blk(MAG, 1.1, 0.45).move_to(egg)
        self.cue("one set", FadeIn(bm, scale=1.5), rt=0.6)
        self.play(bm.animate.move_to(P(-3.6, -2.05)), run_time=1.2)
        tl = lab("one maternal set", MAG, 30).move_to(P(-3.6, -3.1))
        self.play(FadeIn(tl), run_time=0.5)
        bp = blk(PAT, 1.1, 0.45).move_to(body)
        self.cue("or one sperm", FadeIn(bp, scale=1.5), rt=0.6)
        self.play(bp.animate.move_to(P(3.2, -2.05)), run_time=1.3)
        tr = lab("one paternal set", PAT, 30).move_to(P(3.2, -3.1))
        self.play(FadeIn(tr), run_time=0.5)
        lg = legend()
        self.cue("mother sets", FadeIn(lg[0], shift=LEFT * 0.2), Indicate(bm, color=MAG), rt=1.0)
        self.cue("the fathers", FadeIn(lg[1], shift=LEFT * 0.2), Indicate(bp, color=PAT), rt=1.0)
        self.finish()


class S03Pollen(W):
    def construct(self):
        lg = legend()
        self.add(lg)
        # tassel -> one anther -> one grain
        stem = Line(P(-0.8, -3.0), P(-0.8, 2.6), color=GREY, stroke_width=8)
        br = VGroup(*[Line(P(-0.8, 2.4 - 0.5 * i), P(-0.8 + d * 2.6, 3.0 - 0.9 * i), color=GREY, stroke_width=5) for i, d in enumerate([1, -1, 1, -1, 1])])
        an = VGroup(*[Ellipse(width=0.45, height=0.25, stroke_color=POLC, stroke_width=2, fill_color=POLC, fill_opacity=0.8).move_to(b.get_end()) for b in br])
        tassel = VGroup(stem, br, an)
        self.play(FadeIn(tassel), run_time=0.6)
        dust = motes(P(0.6, 1.4), 3.0, 1.6, n=10, color=POLC, seed=3, size=0.07, op=0.8)
        self.add(dust)
        self.play(tassel.animate.shift(RIGHT * 0.3), run_time=max(0.5, 1.1 - self.elapsed()))
        grain_big = pollen_grain(P(-0.8, -0.1), 2.5)
        tube_ring = grain_big[0]
        dot = Dot(P(-0.8 + 2.6, 3.0 - 0.9 * 1 - 0.0), color=POLC)
        self.play(FadeOut(tassel), FadeOut(dust), FadeIn(tube_ring, scale=0.2), run_time=1.2)
        gl = lab("pollen grain", POLC, 34).move_to(P(-0.8, 3.35))
        self.cue("a pollen grain", FadeIn(gl), rt=0.5)
        inner = motes(P(-0.8, -0.1), 1.8, 1.8, n=9, color=POLC, seed=5, size=0.06, op=0.7)
        self.add(inner)
        self.cue("not a sperm", Indicate(tube_ring, color=POLC, scale_factor=1.03), rt=1.0)
        gl2 = lab("male gametophyte: 2 or 3 cells", TEXT, 32).move_to(P(-1.6, 3.35))
        self.cue("tiny separate", ReplacementTransform(gl, gl2), rt=0.8)
        self.cue("two or three", FadeIn(grain_big[1]), FadeIn(grain_big[3]), rt=0.9)
        tc = lab("tube cell", POLC, 28).move_to(P(-0.8, -0.2))
        self.play(FadeIn(tc), run_time=0.4)
        self.at("and it makes")
        s1, s2 = grain_big[1], grain_big[2]
        s2.move_to(s1)
        b1, b2 = grain_big[4], grain_big[5]
        b1.move_to(s1); b2.move_to(s1)
        self.add(s2, b1, b2)
        self.play(s1.animate.shift(LEFT * 0.7), s2.animate.shift(RIGHT * 0.7), b1.animate.shift(LEFT * 0.7), b2.animate.shift(RIGHT * 0.7), grain_big[3].animate.shift(DOWN * 0.0), run_time=1.2)
        sl = lab("two sperm", PAT, 30).move_to(P(-5.3, 0.8))
        self.fill("sperm", FadeIn(sl))
        self.finish()


class S04Tube(W):
    def construct(self):
        lg = legend()
        self.add(lg)
        grain = pollen_grain(P(-0.8, -0.1), 2.5)
        # the s03 grain, carried
        grain[1].shift(P(-0.7, 0)); grain[2].shift(P(0.7, 0)); grain[4].move_to(grain[1]); grain[5].move_to(grain[2])
        inner = motes(P(-0.8, -0.1), 1.8, 1.8, n=9, color=POLC, seed=5, size=0.06, op=0.7)
        self.add(grain, inner)
        self.cue("one set", *[Indicate(b, color=WHITE, scale_factor=1.25) for b in (grain[3], grain[4], grain[5])], rt=1.5)
        self.fill("the grain lands", Indicate(grain[0], color=POLC, scale_factor=1.02))
        silk_pts = [P(-4.6, 2.6), P(-2.2, 2.2), P(-0.6, 0.5), P(1.2, -1.2), P(3.0, -1.6), P(3.8, -2.2)]
        silk = VMobject(stroke_color=GREY, stroke_width=26, stroke_opacity=0.5)
        silk.set_points_smoothly(silk_pts)
        hairs = VGroup(*[Line(P(-4.6, 2.6), P(-4.6 + 0.55 * np.cos(a), 2.6 + 0.55 * np.sin(a)), color=GREY, stroke_width=4) for a in np.linspace(1.4, 3.6, 7)])
        ov = Ellipse(width=1.8, height=1.3, stroke_color=COATC, stroke_width=6, fill_color=COATC, fill_opacity=0.25).move_to(P(3.9, -2.5))
        self.play(FadeOut(grain[3:]), FadeOut(inner), run_time=0.3)
        tiny = Circle(radius=0.28, stroke_color=POLC, stroke_width=4, fill_color=POLC, fill_opacity=0.6).move_to(P(-4.6, 3.0))
        self.play(ReplacementTransform(VGroup(grain[0], grain[1], grain[2]), tiny), Create(silk), FadeIn(hairs), FadeIn(ov), run_time=1.6)
        st = lab("stigma", TEXT, 32).move_to(P(-3.3, 3.45))
        self.cue("sticky tip", FadeIn(st), Indicate(hairs, color=WHITE), rt=1.0)
        ol = lab("ovule", TEXT, 30).move_to(P(3.9, -3.4))
        tube = silk.copy().set_stroke(POLC, 12, 1)
        self.remove(tiny)
        a = ValueTracker(0.0)
        tubev = always_redraw(lambda: tube.copy().pointwise_become_partial(tube, 0, max(a.get_value(), 0.001)).set_stroke(POLC, 12, 1))
        sp = [sperm(P(0, 0), 0.2), sperm(P(0, 0), 0.2)]

        def place(i, d):
            def f(m):
                al = max(a.get_value() - d, 0.0)
                m.move_to(tube.point_from_proportion(al))
            return f
        for i, s in enumerate(sp):
            s.add_updater(place(i, 0.06 + 0.07 * i))
        self.at("grows a tube")
        self.add(tubev, *sp)
        sl = lab("two sperm", PAT, 30).move_to(P(1.0, -3.0))
        t0 = self.elapsed()
        tot = self.t_of("inside") + 0.9 - t0
        self.play(AnimationGroup(a.animate.set_value(0.97).set_rate_func(linear),
                                 Succession(Wait(max(self.t_of("an ovule") - 0.2 - t0, 0.01)), FadeIn(ol, run_time=0.5)),
                                 Succession(Wait(max(self.t_of("the two sperm") - 0.2 - t0, 0.01)), FadeIn(sl, run_time=0.5))),
                  run_time=tot)
        self.finish()


class S05Sac(W):
    def construct(self):
        lg = legend()
        self.add(lg)
        small = Ellipse(width=1.8, height=1.3, stroke_color=COATC, stroke_width=6, fill_color=COATC, fill_opacity=0.25).move_to(P(3.9, -2.5))
        self.add(small)
        ov = ovule_shell()
        self.play(ReplacementTransform(small, VGroup(ov)), run_time=1.4)
        l1 = lab("embryo sac", TEXT, 34).move_to(P(3.2, 1.6))
        self.cue("the embryo", FadeIn(l1), Create(leader(P(2.0, 1.6), P(OX + 1.9, 1.0))), rt=0.8)
        b = blk(MAG, 1.5, 0.6).move_to(P(3.6, 0.1))
        bl = lab("one maternal set", MAG, 30).move_to(P(3.6, -0.7))
        self.cue("one spore", FadeIn(b, scale=1.4), FadeIn(bl), rt=0.8)
        nuc = VGroup(*[Circle(radius=0.22, stroke_color=MAG, stroke_width=3, fill_color=MAG, fill_opacity=0.8).move_to(p)
                       for p in [EGG, SYNL, SYNR, POL[0], POL[1]]])
        copies = [b.copy() for _ in range(5)]
        self.add(*copies)
        self.cue("its nuclei", *[ReplacementTransform(c, n) for c, n in zip(copies, nuc)], rt=0.9)
        for i, n in enumerate(nuc):
            bob(n, 0.05, 2.0 + 0.3 * i, ph=i)
        l2 = VGroup(lab("all copies of", MAG, 30), lab("one maternal set", MAG, 30)).arrange(DOWN, buff=0.1).move_to(P(3.6, -1.9))
        self.cue("all copies", FadeOut(bl), FadeIn(l2), rt=0.8)
        self.fill("set", Indicate(nuc, color=WHITE, scale_factor=1.3))
        self.finish()


class S06Cells(W):
    def construct(self):
        lg = legend()
        ov = ovule_shell()
        nuc = VGroup(*[Circle(radius=0.22, stroke_color=MAG, stroke_width=3, fill_color=MAG, fill_opacity=0.8).move_to(p)
                       for p in [EGG, SYNL, SYNR, POL[0], POL[1]]])
        self.add(lg, ov, nuc)
        for i, n in enumerate(nuc):
            bob(n, 0.05, 2.0 + 0.3 * i, ph=i)
        C = cells()
        self.cue("three kinds", FadeIn(C.egg), FadeIn(C.syn), FadeIn(C.cc), rt=1.5)
        self.cue("the egg holds", FadeIn(C.egg_lab), rt=0.5)
        self.play(FadeOut(nuc[0]), FadeIn(C.egg_blk, scale=1.5), Indicate(C.egg, color=WHITE, scale_factor=1.15), run_time=1.0)
        self.cue("the large central", FadeIn(C.cc_lab), Indicate(C.cc, color=WHITE, scale_factor=1.04), rt=1.0)
        self.cue("two identical", FadeOut(nuc[3]), FadeOut(nuc[4]), FadeIn(C.cc_b[0], scale=1.4), FadeIn(C.cc_b[1], scale=1.4), rt=0.5)
        self.cue("identical", FadeIn(C.eq, scale=1.5), rt=0.6)
        self.cue("that same set", Indicate(C.cc_b, color=WHITE, scale_factor=1.15), rt=1.2)
        sl = lab("synergids", TEXT, 30).move_to(P(OX, 3.4))
        lns = VGroup(leader(P(OX - 0.4, 3.2), SYNL + P(0, 0.55)), leader(P(OX + 0.4, 3.2), SYNR + P(0, 0.55)))
        self.cue("two synergids", FadeIn(sl), Create(lns), C.syn.animate.set_fill(GREY, 0.6), rt=1.0)
        self.play(C.syn.animate.set_fill(GREY, 0.25), run_time=1.0)
        self.finish()


def ovule_state(fertilized=False, tube=False, sperms=False):
    lg = legend()
    ov = ovule_shell()
    C = cells()
    g = VGroup(lg, ov, C.egg, C.syn, C.cc, C.egg_lab, C.egg_blk, C.cc_lab, C.cc_b, C.eq)
    return g, C, ov, lg


class S07Arrive(W):
    def construct(self):
        g, C, ov, lg = ovule_state()
        self.add(g)
        r1 = rings(SYNL + P(0, 0.4), GREY, 0.1, 0.9, 3, 2.2)
        r2 = rings(SYNR + P(0, 0.4), GREY, 0.1, 0.9, 3, 2.2)
        self.add(r1, r2)
        tube = VMobject(stroke_color=POLC, stroke_width=14)
        tube.set_points_smoothly([P(1.6, 3.5), P(-0.6, 3.5), P(OX - 0.0, 3.2), P(OX - 0.1, 2.6), P(SYNL[0] + 0.1, 2.0)])
        a = ValueTracker(0.001)
        tv = always_redraw(lambda: tube.copy().pointwise_become_partial(tube, 0, max(a.get_value(), 0.001)).set_stroke(POLC, 14, 1))
        self.add(tv)
        self.play(a.animate.set_value(0.45), run_time=max(self.t_of("the tube bursts") - 0.2 - self.elapsed(), 0.5), rate_func=linear)
        self.at("bursts into")
        self.play(a.animate.set_value(1.0), run_time=1.0, rate_func=linear)
        self.play(Flash(SYNL + P(0, 0.9), color=PAT, line_length=0.3, flash_radius=0.4), FadeOut(r1), FadeOut(r2), run_time=0.7)
        s1 = sperm(SYNL + P(0, 0.6), 0.2)
        s2 = sperm(SYNL + P(0.1, 0.5), 0.2)
        self.cue("releases", FadeIn(s1), FadeIn(s2), rt=0.4)
        self.play(s1.animate.move_to(EGG + P(-0.95, -0.3)).scale(1.4), s2.animate.move_to(P(OX - 1.2, -0.1)).scale(1.4), run_time=1.6)
        self.finish()


class S08Embryo(W):
    def construct(self):
        g, C, ov, lg = ovule_state()
        self.add(g)
        s1 = sperm(EGG + P(-0.95, -0.3), 0.28)
        s2 = sperm(P(OX - 1.2, -0.1), 0.28)
        self.add(s1, s2)
        self.play(s1.animate.move_to(EGG + P(-0.2, 0.0)), run_time=1.3)
        self.play(FadeOut(s1), C.egg.animate.set_stroke(EMBC, 4).set_fill(EMBC, 0.25), run_time=0.5)
        tb = blk(PAT, 0.7, 0.28).move_to(EGG + P(0.0, -0.58))
        zy = lab("zygote", EMBC, 32).move_to(P(OX + 3.8, 1.3))
        self.cue("the zygote", FadeIn(zy), FadeIn(tb, scale=1.4), FadeOut(C.egg_lab), C.egg_blk.animate.shift(UP * 0.25), rt=0.9)
        emb = embryo_cartoon(P(1.7, 1.4), 1.0)
        self.cue("grows into", ReplacementTransform(C.egg.copy(), emb), rt=0.8)
        el = lab("embryo", EMBC, 30).move_to(P(1.7, -0.2))
        self.cue("the embryo", FadeIn(el), FadeOut(zy), rt=0.5)
        st = stack([MAG, PAT]).move_to(P(1.7, -1.0))
        self.cue("magenta block", FadeIn(st[0], shift=UP * 0.2), rt=0.6)
        self.cue("and one teal", FadeIn(st[1], shift=DOWN * 0.2), rt=0.6)
        self.play(FadeIn(M("1 + 1", 36, TEXT).move_to(P(1.7, -2.1))), run_time=0.5)
        self.finish()


def right_panel_embryo():
    emb = embryo_cartoon(P(1.7, 1.4), 1.0)
    el = lab("embryo", EMBC, 30).move_to(P(1.7, -0.2))
    st = stack([MAG, PAT]).move_to(P(1.7, -1.0))
    nm = M("1 + 1", 36, TEXT).move_to(P(1.7, -2.1))
    return VGroup(emb, el, st, nm)


class S09Predict(W):
    def construct(self):
        g, C, ov, lg = ovule_state()
        C.egg.set_stroke(EMBC, 4).set_fill(EMBC, 0.25)
        self.add(g, right_panel_embryo())
        s2 = sperm(P(OX - 1.5, 0.0), 0.28)
        self.add(s2)
        self.play(s2.animate.move_to(P(OX - 1.55, -0.35)), run_time=1.5)
        self.cue("holds two", Indicate(C.cc_b, color=WHITE, scale_factor=1.15), rt=1.2)
        q = VGroup(lab("How many blocks?", TEXT, 32), lab("How many teal?", PAT, 32)).arrange(DOWN, buff=0.4).move_to(P(4.9, 0.3))
        self.cue("how many blocks", Write(q[0]), rt=1.2)
        self.cue("are the fathers", Write(q[1]), rt=1.2)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        g, C, ov, lg = ovule_state()
        C.egg.set_stroke(EMBC, 4).set_fill(EMBC, 0.25)
        s2 = sperm(P(OX - 1.55, -0.35), 0.28)
        q = VGroup(lab("How many blocks?", TEXT, 32), lab("How many teal?", PAT, 32)).arrange(DOWN, buff=0.4).move_to(P(4.9, 0.3))
        self.add(g, right_panel_embryo(), s2, q)
        ring = Circle(radius=0.55, stroke_color=GREY, stroke_width=8).move_to(P(5.9, -3.1))
        arc = Arc(radius=0.55, start_angle=PI / 2, angle=-TAU, stroke_color=GOLD, stroke_width=8).move_to(P(5.9, -3.1))
        self.add(ring)
        self.play(Create(arc), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S11Reveal(W):
    def construct(self):
        g, C, ov, lg = ovule_state()
        C.egg.set_stroke(EMBC, 4).set_fill(EMBC, 0.25)
        s2 = sperm(P(OX - 1.55, -0.35), 0.28)
        self.add(g, right_panel_embryo(), s2)
        self.play(s2.animate.move_to(CCC + P(-1.45, 0.0)), run_time=0.5)
        t = blk(PAT, 0.85, 0.36).move_to(CCC + P(0.0, 0.0))
        self.play(FadeOut(s2), FadeIn(t, scale=1.5), FadeOut(C.eq), C.cc_b[0].animate.shift(P(-0.1, -0.35)), C.cc_b[1].animate.shift(P(0.1, -0.35)), t.animate.move_to(CCC + P(0.0, -0.1 + 0.0)), run_time=0.6)
        self.cue("only one of them", Indicate(t, color=WHITE, scale_factor=1.3), rt=1.0)
        self.cue("the endosperm", C.cc.animate.set_stroke(ENDC, 4).set_fill(ENDC, 0.55), rt=1.2)
        # endosperm block on the right, beside the embryo
        en = Circle(radius=0.85, stroke_color=ENDC, stroke_width=4, fill_color=ENDC, fill_opacity=0.8).move_to(P(4.9, 1.4))
        el = lab("endosperm", ENDC, 30).move_to(P(4.9, -0.1))
        self.cue("the food", FadeIn(en, scale=0.3), rt=1.0)
        self.play(FadeIn(el), run_time=0.4)
        st = stack([MAG, MAG, PAT]).move_to(P(4.9, -1.15))
        nm = M("2 + 1", 36, TEXT).move_to(P(4.9, -2.3))
        self.cue("two maternal", FadeIn(st[0]), FadeIn(st[1]), rt=0.7)
        self.cue("one paternal", FadeIn(st[2]), FadeIn(nm), rt=0.7)
        self.finish()


class S12Double(W):
    def construct(self):
        lg = legend()
        self.add(lg)
        ttl = lab("double fertilization", GOLD, 44, font=TITLE_FONT).move_to(P(-2.0, 3.3))
        # left half
        sp1 = sperm(P(-5.4, 1.4), 0.3)
        egg = Circle(radius=0.7, stroke_color=MAG, stroke_width=4, fill_color=MAG, fill_opacity=0.2).move_to(P(-3.7, 1.4))
        eb = blk(MAG, 0.7, 0.28).move_to(egg)
        plus = lab("+", TEXT, 40).move_to(P(-4.6, 1.4))
        ar = Arrow(P(-2.8, 1.4), P(-1.8, 1.4), color=TEXT, buff=0, stroke_width=6)
        emb = embryo_cartoon(P(-0.9, 1.4), 1.0)
        st = stack([MAG, PAT]).move_to(P(-3.0, -1.0))
        nm = VGroup(lab("embryo", EMBC, 32), M("1 + 1", 36, TEXT)).arrange(DOWN, buff=0.15).move_to(P(-3.0, -2.5))
        self.play(FadeIn(sp1), FadeIn(egg), FadeIn(eb), FadeIn(plus), run_time=0.9)
        self.play(GrowArrow(ar), FadeIn(emb, scale=0.4), run_time=1.0)
        self.play(FadeIn(st), FadeIn(nm), run_time=0.8)
        # right half
        sp2 = sperm(P(0.7, 1.4), 0.3)
        cc = Ellipse(width=2.0, height=1.4, stroke_color=MAG, stroke_width=4, fill_color=MAG, fill_opacity=0.2).move_to(P(2.8, 1.4))
        cb = VGroup(blk(MAG, 0.7, 0.28).move_to(P(2.45, 1.4)), blk(MAG, 0.7, 0.28).move_to(P(3.15, 1.4)))
        plus2 = lab("+", TEXT, 40).move_to(P(1.3, 1.4))
        ar2 = Arrow(P(4.0, 1.4), P(4.9, 1.4), color=TEXT, buff=0, stroke_width=6)
        en = Circle(radius=0.75, stroke_color=ENDC, stroke_width=4, fill_color=ENDC, fill_opacity=0.8).move_to(P(5.8, 1.4))
        st2 = stack([MAG, MAG, PAT]).move_to(P(4.9, -1.15))
        nm2 = VGroup(lab("endosperm", ENDC, 32), M("2 + 1", 36, TEXT)).arrange(DOWN, buff=0.15).move_to(P(4.9, -2.7))
        self.cue("the other starts", FadeIn(sp2), FadeIn(cc), FadeIn(cb), FadeIn(plus2), rt=0.9)
        self.play(GrowArrow(ar2), FadeIn(en, scale=0.4), run_time=1.0)
        self.play(FadeIn(st2), FadeIn(nm2), run_time=0.8)
        self.cue("double fertilization", Write(ttl), rt=1.2)
        fn = lab("most flowering plants", GREY, 28).move_to(P(0, -3.5))
        self.play(FadeIn(fn), run_time=0.6)
        self.finish()


def ovule_fert():
    ov = ovule_shell()
    cc = Ellipse(width=3.2, height=2.4, stroke_color=ENDC, stroke_width=3, fill_color=ENDC, fill_opacity=0.55).move_to(CCC)
    emb = embryo_cartoon(EGG, 0.75)
    g = VGroup(ov, cc, emb)
    g.ov = ov
    return g


class S13Coat(W):
    def construct(self):
        lg = legend()
        g = ovule_fert()
        self.add(lg, g)
        self.cue("layers of", Indicate(g.ov.outer, color=WHITE, scale_factor=1.02), Indicate(g.ov.inner, color=WHITE, scale_factor=1.02), rt=1.5)
        self.fill("surround", g.ov.outer.animate.set_stroke(width=14))
        sl = lab("seed coat", COATC, 34).move_to(P(3.9, 2.0))
        self.cue("seed coat", g.ov.outer.animate.set_stroke(COATC, 20), g.ov.inner.animate.set_stroke(COATC, 14), FadeIn(sl), Create(leader(P(2.8, 2.0), P(OX + 2.6, 1.2))), rt=0.9)
        st = stack([MAG, MAG], empty=1).move_to(P(3.9, 0.1))
        nm = VGroup(lab("seed coat: 2 + 0", COATC, 32), lab("the mother's tissue", MAG, 28)).arrange(DOWN, buff=0.15).move_to(P(3.9, -1.7))
        self.cue("with no teal", FadeIn(st), FadeIn(nm), Indicate(st[2], color=PAT, scale_factor=1.2), rt=1.2)
        self.finish()


class S14Fruit(W):
    def construct(self):
        lg = legend()
        g = ovule_fert()
        g.ov.outer.set_stroke(COATC, 20)
        g.ov.inner.set_stroke(COATC, 14)
        self.add(lg, g)
        wall = Ellipse(width=6.6, height=7.0, stroke_color=FRUITC, stroke_width=6, fill_color=FRUITC, fill_opacity=0.15).move_to(P(OX, OY))
        small = g.copy()
        self.cue("the ovary wall", FadeIn(wall), g.animate.scale(0.5, about_point=P(OX, OY)), rt=1.8)
        wl = lab("fruit wall", FRUITC, 34).move_to(P(3.3, 2.0))
        self.cue("fruit wall", wall.animate.set_stroke(FRUITC, 16), FadeIn(wl), Create(leader(P(2.3, 2.0), P(OX + 3.0, 1.5))), rt=1.0)
        st = stack([MAG, MAG], empty=1).move_to(P(3.9, 0.0))
        nm = VGroup(lab("fruit wall: 2 + 0", FRUITC, 32), lab("the mother's tissue", MAG, 28)).arrange(DOWN, buff=0.15).move_to(P(3.9, -1.8))
        self.cue("the mother's tissue", FadeIn(st), FadeIn(nm), rt=1.0)
        K = kernel()
        kl = lab("fruit wall (pericarp)", FRUITC, 30).move_to(P(3.9, 2.0))
        self.cue("in maize", FadeOut(VGroup(wall, g, wl, st, nm)), FadeIn(K, scale=0.9), rt=1.2)
        kl.move_to(P(4.1, -0.2))
        self.cue("thin outer", FadeIn(kl), Create(leader(P(1.4, -0.2), P(KX + 2.3, -0.2))), Indicate(K.fw, color=WHITE, scale_factor=1.02), rt=1.2)
        self.finish()


def ledger_group():
    K = kernel()
    K.em.move_to(P(KX + 0.7, KY + 1.0))
    rows = []
    specs = [([MAG, PAT], "embryo", EMBC, "1 + 1", 1.9, 0),
             ([MAG, MAG, PAT], "endosperm", ENDC, "2 + 1", 0.1, 0),
             ([MAG, MAG], "coat and fruit wall", FRUITC, "2 + 0", -1.9, 1)]
    tgts = [K.em.get_center() + P(0.3, 0.0), P(KX + 0.5, KY - 0.8), P(KX + 2.28, KY - 1.0)]
    for (cols, name, col, num, y, em), tg in zip(specs, tgts):
        s = stack(cols, 0.8, 0.32, 0.06, empty=em).move_to(P(2.5, y))
        t1 = lab(name, col, 28)
        t2 = M(num, 32, TEXT)
        t = VGroup(t1, t2).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(s, RIGHT, buff=0.35)
        ln = leader(tg, s.get_left() + LEFT * 0.1)
        rows.append(VGroup(ln, s, t))
    return K, rows


class S15Ledger(W):
    def construct(self):
        lg = legend()
        K, rows = ledger_group()
        self.add(lg, K)
        self.play(Indicate(K.em, color=WHITE), Indicate(K.en, color=WHITE, scale_factor=1.02), Indicate(K.fw, color=WHITE, scale_factor=1.02), run_time=2.0)
        self.cue("embryo", FadeIn(rows[0], shift=LEFT * 0.2), Indicate(K.em, color=WHITE, scale_factor=1.15), rt=1.2)
        self.cue("endosperm", FadeIn(rows[1], shift=LEFT * 0.2), Indicate(K.en, color=WHITE, scale_factor=1.02), rt=1.2)
        self.cue("coat and", FadeIn(rows[2], shift=LEFT * 0.2), Indicate(K.fw, color=WHITE, scale_factor=1.02), rt=1.2)
        self.finish()


class S18Scope(W):
    def construct(self):
        lg = legend()
        K = kernel(P(-4.0, -0.4), 3.2, 4.2)
        K.em.move_to(P(-4.0 + 0.5, -0.4 + 0.7)).scale(0.7)
        st = stack([MAG, MAG, PAT]).move_to(P(-1.2, -0.4))
        nm = VGroup(lab("endosperm", ENDC, 30), M("2 + 1", 36, TEXT)).arrange(DOWN, buff=0.15).move_to(P(-1.2, -1.9))
        ml = lab("most flowering plants", TEXT, 36).move_to(P(-2.6, 3.0))
        self.add(lg)
        self.play(FadeIn(K), run_time=0.8)
        self.cue("holds for", FadeIn(ml), rt=0.6)
        self.cue("most flowering", FadeIn(st), FadeIn(nm), rt=0.8)
        self.fill("water lilies", Indicate(st, color=WHITE, scale_factor=1.1))
        water = Line(P(2.4, -0.2), P(6.6, -0.2), color=BLUE, stroke_width=5)
        pad = Ellipse(width=3.6, height=0.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to(P(4.5, -0.1))
        petals = VGroup(*[Ellipse(width=0.8, height=2.1, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.5).move_to(P(4.5, 0.2 + 1.0)).rotate(a, about_point=P(4.5, 0.2)) for a in (-0.9, -0.45, 0, 0.45, 0.9)])
        lily = VGroup(water, pad, petals)
        st2 = stack([MAG, PAT]).move_to(P(4.5, -1.7))
        nm2 = VGroup(lab("water lilies", TEXT, 30), M("1 + 1", 36, TEXT)).arrange(RIGHT, buff=0.3).move_to(P(4.5, -2.9))
        self.cue("water lilies", FadeIn(lily, shift=UP * 0.3), rt=1.0)
        self.cue("change the numbers", FadeIn(st2), FadeIn(nm2), rt=0.9)
        self.finish()


class S16Caution(W):
    def construct(self):
        lg = legend()
        self.add(lg)
        y1, y2 = 1.2, -1.8
        ax1 = Line(P(-5.0, y1), P(5.4, y1), color=GREY, stroke_width=3)
        ax2 = Line(P(-5.0, y2), P(5.4, y2), color=GREY, stroke_width=3)
        stg = lambda y: VGroup(*[Line(P(-5.0, y + 0.0), P(-5.0 + 0.4 * np.cos(a), y + 0.4 * np.sin(a)), color=GREY, stroke_width=3) for a in np.linspace(1.0, 2.2, 4)])
        self.play(Create(ax1), Create(ax2), run_time=0.8)
        g1 = Circle(radius=0.3, stroke_color=POLC, stroke_width=4, fill_color=POLC, fill_opacity=0.6).move_to(P(-5.0, y1 + 1.8))
        self.play(g1.animate.move_to(P(-5.0, y1 + 0.3)), run_time=1.2)
        p1 = lab("pollination", POLC, 34).move_to(P(-3.4, y1 + 0.6))
        self.cue("pollination", FadeIn(p1), rt=0.6)
        tube = Line(P(-5.0, y1), P(5.0, y1), color=POLC, stroke_width=10)
        ov = Ellipse(width=0.9, height=0.7, stroke_color=COATC, stroke_width=4, fill_color=COATC, fill_opacity=0.3).move_to(P(5.4, y1))
        self.cue("fertilization comes", FadeIn(ov), rt=0.5)
        f1 = lab("fertilization", ENDC, 34).move_to(P(4.4, y1 + 0.85))
        self.play(Create(tube), run_time=max(self.t_of("inside") - self.elapsed() - 0.2, 1.0), rate_func=linear)
        self.play(FadeIn(f1), Flash(ov, color=PAT, flash_radius=0.6), run_time=0.7)
        g2 = Circle(radius=0.3, stroke_color=POLC, stroke_width=4, fill_color=POLC, fill_opacity=0.6).move_to(P(-5.0, y2 + 1.8))
        stub0 = Line(P(-5.0, y2), P(-3.0, y2), color=POLC, stroke_width=10)
        self.cue("and only if", g2.animate.move_to(P(-5.0, y2 + 0.3)), Create(stub0), rt=0.8)
        x = VGroup(Line(P(-3.0, y2 + 0.3), P(-2.4, y2 - 0.3)), Line(P(-3.0, y2 - 0.3), P(-2.4, y2 + 0.3))).set_stroke(RED, 8)
        nl = lab("pollinated, never fertilized", RED, 32).move_to(P(-1.0, y2 - 0.8))
        self.cue("arrives", Create(x), FadeIn(nl), rt=0.8)
        self.finish()


class S17Rule(W):
    def construct(self):
        lg = legend()
        K = kernel(P(2.5, -0.1))
        K.em.move_to(P(2.5 + 0.7, -0.1 + 1.0))
        grain = Circle(radius=0.7, stroke_color=POLC, stroke_width=5, fill_color=POLC, fill_opacity=0.25).move_to(P(-5.3, 0.4))
        gb = blk(PAT, 0.8, 0.32).move_to(grain)
        self.add(lg, K, grain, gb)
        tgt1, tgt2 = K.em.get_center() + P(-0.2, 0), P(2.2, -0.9)
        a1 = Arrow(P(-4.5, 0.6), tgt1, color=PAT, buff=0.05, stroke_width=7)
        a2 = Arrow(P(-4.5, 0.2), tgt2, color=PAT, buff=0.05, stroke_width=7)
        c1, c2 = gb.copy(), gb.copy()
        self.cue("the father sends", GrowArrow(a1), rt=0.5)
        self.add(c1)
        self.cue("one set", c1.animate.move_to(tgt1 + P(0.0, 0.0)), rt=0.6)
        self.cue("twice", GrowArrow(a2), rt=0.5)
        self.add(c2)
        self.play(c2.animate.move_to(tgt2), run_time=0.8)
        self.cue("his sets", Indicate(K.em, color=WHITE, scale_factor=1.08), Indicate(K.en, color=WHITE, scale_factor=1.02), rt=0.9)
        fl = lab("father: embryo and endosperm only", PAT, 30).move_to(P(-2.4, 3.4))
        self.cue("only the embryo", FadeIn(fl), rt=0.8)
        mg = K.fw.copy().set_fill(opacity=0).set_stroke(MAG, 10)
        mg2 = K.co.copy().set_fill(opacity=0).set_stroke(MAG, 6)
        self.cue("the seed coat", Create(mg), Create(mg2), rt=1.2)
        ml = lab("coat and fruit wall: mother", MAG, 30).move_to(P(-2.4, -3.4))
        self.cue("the mothers own", FadeIn(ml), Indicate(VGroup(mg, mg2), color=MAG), rt=1.0)
        self.finish()


class S19End(EndCard):
    LINE = "The father reaches embryo and endosperm; coat and fruit wall stay maternal."
