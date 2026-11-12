"""One of Each Pair, by Coin Toss (chromosomes and meiosis, chapter 1)  (Biochemistrypedia explainer)

COLOR MAP (same in every scene)
  BLUE / ORANGE   = first homolog pair (alleles A / a)
  GREEN / PURPLE  = second homolog pair (alleles B / b)
  GREY rods       = the other pairs of the fly (hook only)
  TEAL            = names of stages (meiosis I, anaphase I ...)
  YELLOW          = what is being asked, counted or highlighted
  RED             = the thing that does not happen
  TEXT (white)    = allele letters, centromere dot, counters
THE WORLD: horizontal rods (chromosomes). Sister chromatids are two thin rods stacked and joined by ONE
white centromere dot. A white 'centromeres: N' box counts cells. The meiosis cell is an ellipse centred
at CY with spindle poles above and below.
"""
import numpy as np
import random
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B07CFF"
GA, GB, GC = "#A9B1BF", "#7E8BA3", "#C2C7D2"
CY = 0.1
CW, CH = 8.8, 6.2
L = 3.6          # chromosome length inside the cell
LP = 3.2         # chromosome length in the two-pair cell (keeps labels off the outline)
TH = 0.30        # sister thickness inside the cell
BIG, BTH = 4.4, 0.30


# ------------------------------------------------------------------ helpers
class Ch:
    """A chromosome, centred on (x, y): one chromatid or two sisters, one centromere dot, optional label."""

    def __init__(s, color, length, rep=True, th=TH, label=None, x=0.0, y=0.0, lab_size=34):
        s.color, s.length, s.rep, s.th = color, length, rep, th
        gap = th + 0.05
        offs = [gap / 2, -gap / 2] if rep else [0.0]
        s.rods = VGroup(*[RoundedRectangle(corner_radius=th / 2, width=length, height=th, stroke_color=color, stroke_width=3,
                                           fill_color=color, fill_opacity=0.6).move_to([0, o, 0]) for o in offs])
        r = th * (0.75 if rep else 0.34)
        s.dots = VGroup(Circle(radius=r, stroke_width=0, fill_color=TEXT, fill_opacity=1))
        parts = [s.rods, s.dots]
        s.lab = None
        if label:
            s.lab = T(label, lab_size, TEXT, weight=BOLD)
            s.lab.move_to([-length / 2 - 0.4, 0, 0])
            parts.append(s.lab)
        s.g = VGroup(*parts).shift([x, y, 0])

    def c(s):
        return s.dots[0].get_center()


def alab(txt, ch, size=34):
    return T(txt, size, TEXT, weight=BOLD).next_to(ch.rods, LEFT, buff=0.25)


def counter(n, pos=(5.2, 3.4), size=24):
    t = M(f"centromeres: {n}", size, TEXT)
    box = SurroundingRectangle(t, buff=0.14, corner_radius=0.1, stroke_color=TEXT, stroke_width=2)
    return VGroup(box, t).move_to([pos[0], pos[1], 0])


def head(text, color=TEAL, size=34):
    return T(text, size, color, weight=BOLD).move_to([-4.9, 3.4, 0])


def cell_e(cx, cy, w, h, color=GREY):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.12).move_to([cx, cy, 0])


def pole(p):
    return Circle(radius=0.15, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.9).move_to(p)


def equator(y=CY, w=CW - 0.6):
    return DashedLine([-w / 2, y, 0], [w / 2, y, 0], color=GREY, stroke_width=2, dash_length=0.18)


def fibre(pl, ch):
    return always_redraw(lambda: Line(pl.get_center(), ch.c(), color=GREY, stroke_width=2.5))


def coin(pos, r=0.42):
    d = Circle(radius=r, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.55).move_to([pos[0], pos[1], 0])
    d.p0 = d.get_center()
    return d


def spin(c, w=5.0, ph=0.0):
    c.tt = ph

    def f(m, dt):
        m.tt += dt
        m.stretch_to_fit_height(max(0.06, 2 * 0.42 * abs(np.cos(w * m.tt))))
        m.move_to(m.p0)
    c.add_updater(f)


def drift(m, amp=0.05, w=1.3, ph=0.0):
    m.dt_ = ph

    def f(mm, dt):
        mm.dt_ += dt
        mm.shift(UP * amp * w * np.cos(w * mm.dt_) * dt)
    m.add_updater(f)


def wob_cell(cellm):
    cellm.tw = 0.0

    def f(m, dt):
        m.tw += dt
        m.set_stroke(width=4 + 1.2 * np.sin(2.2 * m.tw))
    cellm.add_updater(f)


def kind(a, b, size=34):
    return T(a + b, size, TEXT, weight=BOLD)


class W(SpokenScene):
    """SpokenScene plus a faint slow field of drifting motes so a held frame is never dead."""

    def setup(self):
        super().setup()
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        ms = VGroup()
        for _ in range(16):
            d = Dot(radius=rng.uniform(0.03, 0.06), color=rng.choice([TEAL, GREY])).set_opacity(rng.uniform(0.15, 0.3))
            d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
            d.v = (rng.uniform(-0.12, 0.12), rng.uniform(0.08, 0.22))

            def mv(m):
                pass

            def f(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 4.0:
                    m.shift(DOWN * 8.0)
            d.add_updater(f)
            ms.add(d)
        ms.set_z_index(-10)
        self.add(ms)


def rods_pair(color1, color2, x, y, length=L, th=TH, lab1=None, lab2=None, dy=0.48):
    a = Ch(color1, length, True, th, lab1, x, y + dy)
    b = Ch(color2, length, True, th, lab2, x, y - dy)
    return a, b


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Chromosomes and meiosis"
    TITLE = "One of Each Pair, by Coin Toss"


class S01Hook(W):
    def construct(self):
        lc = np.array([-3.3, 0.0, 0.0])
        cell = cell_e(lc[0], 0, 6.2, 6.2)
        specs = [(BLUE, ORANGE), (GA, GA), (GB, GB), (GC, GC)]
        pos = [(-1.3, 1.35), (1.3, 1.35), (-1.3, -1.35), (1.3, -1.35)]
        rods = []
        grp = VGroup()
        for (c1, c2), (px, py) in zip(specs, pos):
            a = Ch(c1, 2.1, False, 0.34, None, lc[0] + px, py + 0.3)
            b = Ch(c2, 2.1, False, 0.34, None, lc[0] + px, py - 0.3)
            rods.append((a, b))
            grp.add(a.g, b.g)
            drift(a.g, 0.04, 1.1, px)
            drift(b.g, 0.04, 1.3, py)
        c8 = counter(8, (lc[0], 3.45))
        head_c = Ellipse(width=3.1, height=2.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([3.4, 1.0, 0])
        tail = ParametricFunction(lambda t: np.array([3.4 + 0.45 * np.sin(2.2 * t * 3.0), -0.35 - 3.0 * t, 0]), t_range=[0, 1],
                                  color=GREY, stroke_width=6)
        c4 = counter(4, (3.4, 3.45))
        q = T("?", 96, YELLOW, weight=BOLD).move_to([5.9, 1.0, 0])

        self.play(Create(cell), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(g, scale=0.7) for g in grp], lag_ratio=0.15), run_time=1.6)
        self.at("body cells")
        self.play(FadeIn(c8), run_time=0.6)
        self.at("hold eight")
        self.play(LaggedStart(*[Indicate(g, scale_factor=1.12, color=YELLOW) for g in grp], lag_ratio=0.12), run_time=1.6)
        self.at("eggs and sperm")
        self.play(Create(head_c), Create(tail), run_time=1.2)
        self.at("one from each")
        picks = [rods[0][0], rods[1][0], rods[2][0], rods[3][0]]
        tgt = [(2.55, 1.55), (4.25, 1.55), (2.55, 0.55), (4.25, 0.55)]
        cps = []
        for p, (tx, ty) in zip(picks, tgt):
            cp = p.g.copy()
            cp.clear_updaters()
            cps.append(cp)
        self.add(*cps)
        self.play(*[cp.animate.scale(0.62).move_to([tx, ty, 0]) for cp, (tx, ty) in zip(cps, tgt)], FadeIn(c4), run_time=1.5)
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.play(q.animate.shift(UP * 0.2), rate_func=there_and_back, run_time=1.2)
        self.finish()


class S02Mendel(W):
    def construct(self):
        # left: pea pod + tally
        pod = Ellipse(width=3.8, height=1.1, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.35).move_to([-4.0, 0.7, 0])
        peas = VGroup(*[Circle(radius=0.27, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.8).move_to([-5.2 + 0.8 * i, 0.7, 0]) for i in range(4)])
        lab = T("Mendel: counts", 30, TEXT, weight=BOLD).move_to([-4.0, -0.5, 0])
        tally = M("||||  ||||  |||", 38, TEXT).move_to([-4.0, 2.2, 0])
        podg = VGroup(pod, peas, lab, tally)
        # right: the fly cell, hidden
        cc = np.array([3.6, 0.0, 0.0])
        cell = cell_e(cc[0], 0, 4.6, 4.6)
        ra = Ch(BLUE, 1.7, False, 0.26, None, cc[0], 0.45)
        rb = Ch(ORANGE, 1.7, False, 0.26, None, cc[0], -0.05)
        rc = Ch(GA, 1.7, False, 0.26, None, cc[0], -0.75)
        rd = Ch(GB, 1.7, False, 0.26, None, cc[0], -1.3)
        re_ = Ch(GC, 1.7, False, 0.26, None, cc[0], 1.2)
        inner = VGroup(ra.g, rb.g, rc.g, rd.g, re_.g)
        inner_dim = VGroup(rc.g, rd.g, re_.g)
        eye = VGroup(Arc(radius=0.7, start_angle=PI + 0.45, angle=PI - 0.9, color=TEXT, stroke_width=5).move_to([cc[0], 0.35, 0]))
        for k in (-0.5, 0.0, 0.5):
            eye.add(Line([cc[0] + k, 0.2, 0], [cc[0] + k * 1.15, -0.05, 0], color=TEXT, stroke_width=4))
        eye.shift(DOWN * 0.1)
        self.play(FadeIn(pod), LaggedStart(*[GrowFromCenter(p) for p in peas], lag_ratio=0.2), FadeIn(lab), run_time=1.6)
        self.at("counts of")
        self.play(FadeIn(tally, shift=UP * 0.1), Create(cell), FadeIn(inner), run_time=1.4)
        self.at("never saw")
        self.play(inner.animate.set_opacity(0.3), FadeIn(eye), run_time=0.9)
        self.at("did the separating")
        self.play(podg.animate.shift(LEFT * 9), FadeOut(eye), FadeOut(inner_dim), VGroup(cell, ra.g, rb.g).animate.scale(1.4).move_to([0, 0, 0]), run_time=1.0)
        fa = Ch(BLUE, BIG, False, 0.65, None, 0, 1.0)
        fb = Ch(ORANGE, BIG, False, 0.65, None, 0, -1.0)
        self.play(FadeOut(cell), ReplacementTransform(ra.g, fa.g), ReplacementTransform(rb.g, fb.g), run_time=0.9)
        self.finish()


def s03_world():
    fa = Ch(BLUE, BIG, False, 0.65, None, 0, 1.0)
    fb = Ch(ORANGE, BIG, False, 0.65, None, 0, -1.0)
    return fa, fb


class S03Pair(W):
    def construct(self):
        fa, fb = s03_world()
        self.add(fa.g, fb.g)
        drift(fa.g, 0.04, 1.2)
        drift(fb.g, 0.04, 1.2, 1.0)
        cnt = counter(2)
        self.play(FadeIn(cnt), run_time=0.6)
        self.at("homologues")
        brace = Brace(VGroup(fa.rods, fb.rods), RIGHT, color=TEXT)
        hom = T("homologs", 36, TEXT, weight=BOLD).next_to(brace, RIGHT, buff=0.25).shift(UP * 0.5)
        self.play(GrowFromCenter(brace), FadeIn(hom), Indicate(fa.g, color=BLUE, scale_factor=1.05), Indicate(fb.g, color=ORANGE, scale_factor=1.05), run_time=1.4)
        self.at("one inherited")
        par = VGroup(T("one from", 30, TEXT), T("each parent", 30, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(hom, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(par, shift=UP * 0.1), run_time=1.0)
        self.at("same genes")
        xs = [-1.6, -0.7, 0.4, 1.5]
        bands = VGroup()
        links = VGroup()
        for x in xs:
            for ch in (fa, fb):
                bands.add(Rectangle(width=0.14, height=0.55, stroke_width=0, fill_color="#D5D9E1", fill_opacity=0.9).move_to([x, ch.rods.get_center()[1], 0]))
            links.add(DashedLine([x, 0.65, 0], [x, -0.65, 0], color=GREY, stroke_width=2.5, dash_length=0.12))
        self.play(LaggedStart(*[FadeIn(b) for b in bands], lag_ratio=0.12), run_time=1.8)
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.2), run_time=1.5)
        self.at("different versions")
        ga = Rectangle(width=0.2, height=0.62, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([-1.6, 1.0, 0])
        gb = Rectangle(width=0.2, height=0.62, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([-1.6, -1.0, 0])
        self.play(FadeIn(ga, scale=1.6), FadeIn(gb, scale=1.6), run_time=1.0)
        self.at("alleles")
        la, lb = alab("A", fa), alab("a", fb)
        self.play(FadeIn(la, shift=RIGHT * 0.15), FadeIn(lb, shift=RIGHT * 0.15), run_time=1.0)
        self.at("blue carries")
        self.play(Indicate(fa.rods, color=TEXT, scale_factor=1.06), Indicate(la, scale_factor=1.4), run_time=1.2)
        self.at("orange carries")
        self.play(Indicate(fb.rods, color=TEXT, scale_factor=1.06), Indicate(lb, scale_factor=1.4), run_time=1.2)
        self.at("follow the colors")
        self.play(Indicate(fa.g, color=BLUE, scale_factor=1.05), Indicate(fb.g, color=ORANGE, scale_factor=1.05), run_time=1.4)
        self.finish()


class S04Copy(W):
    def construct(self):
        fa = Ch(BLUE, BIG, False, 0.65, "A", 0, 1.0)
        fb = Ch(ORANGE, BIG, False, 0.65, "a", 0, -1.0)
        self.add(fa.g, fb.g)
        cnt = counter(2)
        self.add(cnt)
        sa = Ch(BLUE, BIG, True, BTH, "A", 0, 1.0)
        sb = Ch(ORANGE, BIG, True, BTH, "a", 0, -1.0)
        self.at("each chromosome is copied")
        sph = head("S phase")
        self.play(FadeIn(sph), run_time=0.5)
        self.play(ReplacementTransform(fa.g, sa.g), ReplacementTransform(fb.g, sb.g), run_time=2.0)
        self.at("sister chromatids")
        br = Brace(sa.rods, RIGHT, color=TEXT)
        lab = VGroup(T("sister", 32, TEXT, weight=BOLD), T("chromatids", 32, TEXT, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(br, RIGHT, buff=0.25)
        self.play(GrowFromCenter(br), FadeIn(lab), run_time=1.1)
        self.at("joined at")
        ring = Circle(radius=0.38, stroke_color=YELLOW, stroke_width=5).move_to(sa.c())
        self.play(Create(ring), run_time=0.8)
        self.play(Indicate(sa.dots, color=YELLOW, scale_factor=1.6), run_time=1.0)
        self.at("count centromeres")
        note = M("chromatids: 4", 24, TEXT).move_to([5.2, 2.75, 0])
        self.play(FadeOut(br), FadeOut(lab), Indicate(cnt, color=YELLOW, scale_factor=1.15), FadeIn(note), run_time=1.2)
        self.at("not arms")
        self.play(FadeOut(note), FadeOut(ring), run_time=0.8)
        self.at("a copied chromosome")
        box = SurroundingRectangle(sa.g, buff=0.2, corner_radius=0.15, stroke_color=YELLOW, stroke_width=5)
        one = T("1 chromosome", 34, YELLOW, weight=BOLD).next_to(box, RIGHT, buff=0.2)
        one.set_x(min(one.get_x(), 4.6))
        self.play(Create(box), FadeIn(one), run_time=1.0)
        self.play(Indicate(sa.dots, color=YELLOW, scale_factor=1.5), run_time=1.0)
        self.finish()


def stage1(self, pair_y=0.48, with_poles=True, fibres=True):
    """Meiosis I cell with the blue/orange pair at the equator; returns (cell, a, b, poles, fibs, eq)."""
    cellm = cell_e(0, CY, CW, CH)
    a, b = rods_pair(BLUE, ORANGE, 0, CY, L, TH, "A", "a", pair_y)
    pt, pb = pole([0, CY + CH / 2 - 0.15, 0]), pole([0, CY - CH / 2 + 0.15, 0])
    return cellm, a, b, pt, pb


class S05LineUp(W):
    def construct(self):
        sa = Ch(BLUE, BIG, True, BTH, "A", 0, 1.0)
        sb = Ch(ORANGE, BIG, True, BTH, "a", 0, -1.0)
        cnt = counter(2)
        self.add(sa.g, sb.g, cnt)
        self.at("one round of copying")
        c1 = chip("1 copying", TEAL, 30)
        c2 = chip("2 divisions", TEAL, 30)
        arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, color=TEXT, buff=0)
        top = VGroup(c1, arrow, c2).arrange(RIGHT, buff=0.3).move_to([0, 3.2, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.8)
        self.at("two divisions")
        self.play(GrowArrow(arrow), FadeIn(c2, shift=DOWN * 0.1), run_time=0.9)
        self.at("in the first")
        cellm = cell_e(0, CY, CW, CH)
        wob_cell(cellm)
        a0, b0 = rods_pair(BLUE, ORANGE, 0, CY, L, TH, "A", "a", 0.85)
        m1 = head("meiosis I")
        self.play(FadeOut(top), Create(cellm), ReplacementTransform(sa.g, a0.g), ReplacementTransform(sb.g, b0.g), FadeIn(m1), run_time=2.2)
        self.at("homologues find")
        self.play(Indicate(a0.g, color=BLUE, scale_factor=1.04), Indicate(b0.g, color=ORANGE, scale_factor=1.04), run_time=1.0)
        self.at("line up")
        a1, b1 = rods_pair(BLUE, ORANGE, 0, CY, L, TH, "A", "a", 0.42)
        self.play(ReplacementTransform(a0.g, a1.g), ReplacementTransform(b0.g, b1.g), run_time=1.8)
        self.at("then the pair")
        eq = equator()
        pt, pb = pole([0, CY + CH / 2 - 0.15, 0]), pole([0, CY - CH / 2 + 0.15, 0])
        self.play(FadeIn(eq), GrowFromCenter(pt), GrowFromCenter(pb), run_time=1.0)
        f1, f2 = fibre(pt, a1), fibre(pb, b1)
        self.add(f1, f2)
        self.play(FadeIn(f1), FadeIn(f2), run_time=1.2)
        self.at("facing opposite poles")
        self.play(Indicate(a1.g, color=BLUE, scale_factor=1.05), Indicate(pt, color=YELLOW, scale_factor=1.8), run_time=1.0)
        self.play(Indicate(b1.g, color=ORANGE, scale_factor=1.05), Indicate(pb, color=YELLOW, scale_factor=1.8), run_time=1.0)
        self.finish()


def rebuild_stage1(self, cnt_n=2, pair_dy=0.42, label="meiosis I", extra_pair=False):
    cellm = cell_e(0, CY, CW, CH)
    wob_cell(cellm)
    a, b = rods_pair(BLUE, ORANGE, 0, CY, L, TH, "A", "a", pair_dy)
    pt, pb = pole([0, CY + CH / 2 - 0.15, 0]), pole([0, CY - CH / 2 + 0.15, 0])
    eq = equator()
    cnt = counter(cnt_n)
    m1 = head(label)
    self.add(cellm, eq, pt, pb, a.g, b.g, cnt, m1)
    f1, f2 = fibre(pt, a), fibre(pb, b)
    self.add(f1, f2)
    return cellm, a, b, pt, pb, eq, cnt, m1, f1, f2


class S06AnaphaseOne(W):
    def construct(self):
        cellm, a, b, pt, pb, eq, cnt, m1, f1, f2 = rebuild_stage1(self)
        self.at("anaphase 1")
        m2 = head("anaphase I")
        self.play(FadeOut(eq), ReplacementTransform(m1, m2), run_time=0.6)
        ya, yb = CY + 1.6, CY - 1.6
        self.play(a.g.animate.move_to([0, ya, 0]).shift(LEFT * 0.0), b.g.animate.move_to([0, yb, 0]), run_time=3.0)
        # g includes the label (left of rod), so recentre by rods
        self.at("each new cell")
        top = cell_e(0, ya, 5.5, 3.0)
        bot = cell_e(0, yb, 5.5, 3.0)
        self.play(FadeOut(f1), FadeOut(f2), FadeOut(pt), FadeOut(pb), FadeOut(cnt), ReplacementTransform(cellm, VGroup(top, bot)), run_time=2.0)
        self.at("count its centromeres")
        ct = counter(1, (4.7, ya + 0.2))
        cb = counter(1, (4.7, yb + 0.2))
        self.play(FadeIn(ct), FadeIn(cb), run_time=0.8)
        self.at("already haploid")
        ht = T("haploid", 32, TEXT, weight=BOLD).move_to([-4.9, ya + 0.2, 0])
        hb = T("haploid", 32, TEXT, weight=BOLD).move_to([-4.9, yb + 0.2, 0])
        self.play(FadeIn(ht), FadeIn(hb), run_time=0.9)
        self.at("one homolog")
        self.play(Indicate(a.g, color=BLUE, scale_factor=1.06), Indicate(b.g, color=ORANGE, scale_factor=1.06), run_time=1.2)
        self.at("still two sister")
        sist = T("still 2 sisters", 30, TEXT, weight=BOLD)
        s1 = sist.copy().move_to([4.7, ya - 0.6, 0])
        s2 = sist.copy().move_to([4.7, yb - 0.6, 0])
        self.play(FadeIn(s1), FadeIn(s2), Indicate(a.rods, color=TEXT, scale_factor=1.08), Indicate(b.rods, color=TEXT, scale_factor=1.08), run_time=1.4)
        self.finish()


PX = [-4.8, -1.6, 1.6, 4.8]


def product(x, color, lab, y=CY):
    e = cell_e(x, y, 3.0, 2.6)
    r = Ch(color, 2.0, False, 0.2, None, x, y)
    lt = T(lab, 34, TEXT, weight=BOLD).move_to([x, y + 0.6, 0])
    return e, r, lt


class S07MeiosisTwo(W):
    def construct(self):
        ya, yb = CY + 1.6, CY - 1.6
        top = cell_e(0, ya, 5.5, 3.0)
        bot = cell_e(0, yb, 5.5, 3.0)
        a = Ch(BLUE, L, True, TH, "A", 0, ya)
        b = Ch(ORANGE, L, True, TH, "a", 0, yb)
        h = head("anaphase I")
        ht = T("haploid", 32, TEXT, weight=BOLD).move_to([-4.9, ya + 0.2, 0])
        hb = T("haploid", 32, TEXT, weight=BOLD).move_to([-4.9, yb + 0.2, 0])
        self.add(top, bot, a.g, b.g, h, ht, hb)
        self.at("no DNA is copied")
        nc = T("no copying", 36, RED, weight=BOLD).move_to([5.0, CY, 0])
        self.play(FadeIn(nc, shift=UP * 0.1), Indicate(nc, color=RED, scale_factor=1.15), run_time=1.2)
        self.at("second division")
        m2 = head("meiosis II")
        self.play(FadeOut(nc), FadeOut(ht), FadeOut(hb), ReplacementTransform(h, m2), run_time=0.8)
        self.at("sisters part")
        # sisters of each chromosome part, labels dropped; cells divide to the row of four
        for ch in (a, b):
            ch.lab_old = ch.lab
        pa = [product(PX[0], BLUE, "A"), product(PX[1], BLUE, "A")]
        pb = [product(PX[2], ORANGE, "a"), product(PX[3], ORANGE, "a")]
        self.play(FadeOut(a.lab), FadeOut(b.lab), FadeOut(a.dots), FadeOut(b.dots),
                  a.rods[0].animate.shift(UP * 0.45), a.rods[1].animate.shift(DOWN * 0.45),
                  b.rods[0].animate.shift(UP * 0.45), b.rods[1].animate.shift(DOWN * 0.45), run_time=1.2)
        self.play(ReplacementTransform(top, VGroup(pa[0][0], pa[1][0])), ReplacementTransform(bot, VGroup(pb[0][0], pb[1][0])),
                  ReplacementTransform(a.rods[0], pa[0][1].rods[0]), ReplacementTransform(a.rods[1], pa[1][1].rods[0]),
                  ReplacementTransform(b.rods[0], pb[0][1].rods[0]), ReplacementTransform(b.rods[1], pb[1][1].rods[0]), run_time=2.4)
        self.add(*[p[1].dots for p in pa + pb])
        self.at("four products")
        self.play(*[FadeIn(p[1].dots) for p in pa + pb], run_time=0.6)
        cs = VGroup(*[counter(1, (x, CY - 1.7), size=22) for x in PX])
        self.play(FadeIn(cs), run_time=0.8)
        self.at("two carry")
        self.play(*[FadeIn(p[2]) for p in pa], Indicate(VGroup(pa[0][0], pa[1][0]), color=BLUE, scale_factor=1.05), run_time=1.2)
        tally = M("2 A : 2 a", 50, TEXT).move_to([0, 3.1, 0])
        self.at("two carry", nth=1)
        self.play(*[FadeIn(p[2]) for p in pb], Indicate(VGroup(pb[0][0], pb[1][0]), color=ORANGE, scale_factor=1.05), FadeIn(tally), run_time=1.2)
        self.finish()


class S08Segregation(W):
    def construct(self):
        cs, tally = None, M("2 A : 2 a", 50, TEXT).move_to([0, 3.1, 0])
        prods = []
        mob = VGroup()
        for x, col, lab in zip(PX, [BLUE, BLUE, ORANGE, ORANGE], ["A", "A", "a", "a"]):
            e, r, lt = product(x, col, lab)
            prods.append(e)
            mob.add(e, r.g, lt)
        cs = VGroup(*[counter(1, (x, CY - 1.7), size=22) for x in PX])
        self.add(mob, cs, tally)
        self.at("Mendel's model")
        self.play(FadeOut(cs), Indicate(tally, color=YELLOW, scale_factor=1.15), run_time=1.2)
        self.at("law of segregation")
        ban = T("Segregation = the deal", 46, YELLOW, weight=BOLD).move_to([0, 3.1, 0])
        self.play(ReplacementTransform(tally, ban), run_time=1.0)
        self.at("chromosome movement")
        minis = VGroup()
        for k, x in enumerate([-3.6, 0.0, 3.6]):
            ic = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=c, fill_opacity=1).move_to([x + dx, CY - 2.6, 0]) for c, dx in zip([BLUE, BLUE, ORANGE, ORANGE], [-0.9, -0.3, 0.3, 0.9])])
            minis.add(ic)
        note = T("expected outcome; rare exceptions in the lesson", 22, GREY).move_to([0, -3.5, 0])
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in minis], lag_ratio=0.3), FadeIn(note), run_time=1.6)
        self.finish()


def two_pair_stage(self, cnt_n=4, green_top=True, label="meiosis I"):
    cellm = cell_e(0, CY, CW, CH)
    wob_cell(cellm)
    a, b = rods_pair(BLUE, ORANGE, -2.0, CY, LP, TH, "A", "a", 0.42)
    top_c, bot_c = (GREEN, PURPLE) if green_top else (PURPLE, GREEN)
    top_l, bot_l = ("B", "b") if green_top else ("b", "B")
    c, d = rods_pair(top_c, bot_c, 2.25, CY, LP, TH, top_l, bot_l, 0.42)
    pt, pb = pole([0, CY + CH / 2 - 0.15, 0]), pole([0, CY - CH / 2 + 0.15, 0])
    eq = equator()
    cnt = counter(cnt_n)
    m1 = head(label)
    f1, f2, f3, f4 = fibre(pt, a), fibre(pb, b), fibre(pt, c), fibre(pb, d)
    return cellm, a, b, c, d, pt, pb, eq, cnt, m1, [f1, f2, f3, f4]


class S09SecondPair(W):
    def construct(self):
        cellm = cell_e(0, CY, CW, CH)
        wob_cell(cellm)
        a, b = rods_pair(BLUE, ORANGE, 0, CY, LP, TH, "A", "a", 0.42)
        pt, pb = pole([0, CY + CH / 2 - 0.15, 0]), pole([0, CY - CH / 2 + 0.15, 0])
        eq = equator()
        m1 = head("meiosis I")
        cnt = counter(2)
        f1, f2 = fibre(pt, a), fibre(pb, b)
        self.add(cellm, eq, pt, pb, a.g, b.g, m1, cnt, f1, f2)
        self.at("second pair")
        c0, d0 = rods_pair(GREEN, PURPLE, 6.5, CY, LP, TH, None, None, 0.42)
        c1, d1 = rods_pair(GREEN, PURPLE, 2.15, CY, L, TH, None, None, 0.42)
        f3, f4 = fibre(pt, c0), fibre(pb, d0)
        self.add(c0.g, d0.g, f3, f4)
        self.play(a.g.animate.shift(LEFT * 2.0), b.g.animate.shift(LEFT * 2.0), c0.g.animate.shift(LEFT * 4.25), d0.g.animate.shift(LEFT * 4.25),
                  Transform(cnt, counter(4)), run_time=2.2)
        self.at("different chromosome")
        self.play(Indicate(c0.g, color=GREEN, scale_factor=1.04), Indicate(d0.g, color=PURPLE, scale_factor=1.04), run_time=1.0)
        self.at("second gene")
        la, lb = T("B", 34, TEXT, weight=BOLD).next_to(c0.rods, LEFT, buff=0.25), T("b", 34, TEXT, weight=BOLD).next_to(d0.rods, LEFT, buff=0.25)
        self.play(FadeIn(la, shift=RIGHT * 0.15), FadeIn(lb, shift=RIGHT * 0.15), run_time=1.0)
        self.finish()


class S10Question(W):
    def construct(self):
        cellm, a, b, c, d, pt, pb, eq, cnt, m1, fibs = two_pair_stage(self)
        self.add(cellm, eq, pt, pb, a.g, b.g, c.g, d.g, cnt, m1, *fibs)
        card = T("Does the blue pair's direction change the green pair's?", 28, TEXT, weight=BOLD)
        cbox = SurroundingRectangle(card, buff=0.16, corner_radius=0.12, stroke_color=YELLOW, stroke_width=3).set_fill(BG, 0.9)
        cardg = VGroup(cbox, card).move_to([0, -3.45, 0])
        q = T("?", 80, YELLOW, weight=BOLD).move_to([2.15, CY + 1.9, 0])
        self.at("here is the question")
        self.play(Indicate(VGroup(a.g, b.g), color=BLUE, scale_factor=1.03), run_time=1.0)
        self.at("does the way")
        self.play(FadeIn(cardg, shift=UP * 0.15), run_time=1.0)
        self.at("blue pair faces")
        self.play(Indicate(a.rods, color=BLUE, scale_factor=1.05), Indicate(pt, color=YELLOW, scale_factor=1.8), run_time=1.0)
        self.at("green pair")
        glow = SurroundingRectangle(VGroup(c.g, d.g), buff=0.12, corner_radius=0.15, stroke_color=YELLOW, stroke_width=4)
        self.play(Create(glow), FadeIn(q, scale=0.6), run_time=0.6)
        self.play(Swap(c.g, d.g), run_time=0.9)
        self.play(Swap(c.g, d.g), run_time=0.9)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        cellm, a, b, c, d, pt, pb, eq, cnt, m1, fibs = two_pair_stage(self)
        self.add(cellm, eq, pt, pb, a.g, b.g, c.g, d.g, cnt, m1, *fibs)
        card = T("Does the blue pair's direction change the green pair's?", 28, TEXT, weight=BOLD)
        cbox = SurroundingRectangle(card, buff=0.16, corner_radius=0.12, stroke_color=YELLOW, stroke_width=3).set_fill(BG, 0.9)
        cardg = VGroup(cbox, card).move_to([0, -3.45, 0])
        q = T("?", 80, YELLOW, weight=BOLD).move_to([2.15, CY + 1.9, 0])
        glow = SurroundingRectangle(VGroup(c.g, d.g), buff=0.12, corner_radius=0.15, stroke_color=YELLOW, stroke_width=4)
        glow.tg = 0.0

        def pulse(m, dt):
            m.tg += dt
            m.set_stroke(opacity=0.45 + 0.45 * np.sin(3.0 * m.tg))
        glow.add_updater(pulse)
        self.add(cardg, q, glow)
        self.finish()


def mini_layout(cx, second_top, cy=0.15):
    """One small meiosis I cell: pair 1 (blue on top) and pair 2 (green or purple on top)."""
    e = cell_e(cx, cy, 6.4, 4.4)
    ptp = pole([cx, cy + 2.05, 0])
    pbp = pole([cx, cy - 2.05, 0])
    eqq = DashedLine([cx - 3.0, cy, 0], [cx + 3.0, cy, 0], color=GREY, stroke_width=2, dash_length=0.16)
    a, b = rods_pair(BLUE, ORANGE, cx - 1.6, cy, 2.2, 0.2, None, None, 0.36)
    t2, b2 = (GREEN, PURPLE) if second_top == "green" else (PURPLE, GREEN)
    l2t, l2b = ("B", "b") if second_top == "green" else ("b", "B")
    c, d = rods_pair(t2, b2, cx + 1.6, cy, 2.2, 0.2, None, None, 0.36)
    labs = VGroup()
    for ch, tx in [(a, "A"), (b, "a"), (c, l2t), (d, l2b)]:
        labs.add(T(tx, 26, TEXT, weight=BOLD).move_to(ch.rods.get_center() + LEFT * 0.7 + UP * 0.0))
    cnt = counter(4, (cx, cy + 2.55), size=22)
    return VGroup(e, eqq, ptp, pbp, a.g, b.g, c.g, d.g, labs, cnt)


class S12Reveal(W):
    def construct(self):
        cellm, a, b, c, d, pt, pb, eq, cnt, m1, fibs = two_pair_stage(self)
        self.add(cellm, eq, pt, pb, a.g, b.g, c.g, d.g, cnt, m1, *fibs)
        self.at("each pair faces")
        c1 = coin([-2.15, CY + 2.15])
        c2 = coin([2.15, CY + 2.15])
        spin(c1, 5.0, 0.0)
        spin(c2, 6.3, 0.7)
        self.play(FadeIn(c1, scale=0.6), FadeIn(c2, scale=0.6), run_time=0.7)
        self.at("coin toss")
        c1.clear_updaters()
        c2.clear_updaters()
        self.play(c1.animate.stretch_to_fit_height(0.84).move_to(c1.p0), c2.animate.stretch_to_fit_height(0.84).move_to(c2.p0), run_time=0.5)
        self.play(Swap(c.g, d.g), run_time=1.0)
        self.at("blue may end up")
        left = mini_layout(-3.5, "green")
        right = mini_layout(3.5, "purple")
        self.play(FadeOut(VGroup(cellm, eq, pt, pb, a.g, b.g, c.g, d.g, cnt, m1, c1, c2, *fibs)), FadeIn(left), run_time=1.2)
        self.at("blue with purple")
        self.play(FadeIn(right), run_time=1.2)
        self.wait(0.6)
        cap = T("each pair: its own coin toss", 34, YELLOW, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.9)
        self.finish()


def prod2(x, cl1, cl2, k1, k2, y=0.3):
    e = cell_e(x, y, 3.0, 2.6)
    r1 = Ch(cl1, 1.5, False, 0.22, None, x, y + 0.3)
    r2 = Ch(cl2, 1.5, False, 0.22, None, x, y - 0.3)
    l1 = T(k1, 24, TEXT, weight=BOLD).move_to(r1.rods.get_center() + LEFT * 0.5)
    l2 = T(k2, 24, TEXT, weight=BOLD).move_to(r2.rods.get_center() + LEFT * 0.5)
    lab = kind(k1, k2).move_to([x, y - 1.75, 0])
    return VGroup(e, r1.g, r2.g, l1, l2, lab)


class S13OneMeiosis(W):
    def construct(self):
        left = mini_layout(-3.5, "green")
        right = mini_layout(3.5, "purple")
        self.add(left, right)
        cap = T("each pair: its own coin toss", 34, YELLOW, weight=BOLD).move_to([0, -3.1, 0])
        self.add(cap)
        self.at("ignoring crossovers")
        note = T("no crossovers", 26, TEXT).move_to([-5.2, 3.45, 0])
        self.play(FadeOut(cap), FadeIn(note), run_time=0.8)
        self.at("one meiosis takes")
        self.play(FadeOut(right), left.animate.shift(RIGHT * 3.5), run_time=1.6)
        self.play(Indicate(left[1:8], color=YELLOW, scale_factor=1.02), run_time=1.2)
        self.at("so one meiosis")
        prods = [prod2(PX[0], BLUE, GREEN, "A", "B"), prod2(PX[1], BLUE, GREEN, "A", "B"),
                 prod2(PX[2], ORANGE, PURPLE, "a", "b"), prod2(PX[3], ORANGE, PURPLE, "a", "b")]
        row = VGroup(*prods)
        self.play(FadeOut(left), LaggedStart(*[FadeIn(p, scale=0.85) for p in prods], lag_ratio=0.2), run_time=2.0)
        self.at("two kinds")
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=13.0, height=4.7, stroke_color=YELLOW, stroke_width=4).move_to([0, 0.0, 0]), num_dashes=60)
        lab = T("one meiosis: 2 kinds", 38, YELLOW, weight=BOLD).move_to([0, 2.9, 0])
        self.play(Create(box), FadeIn(lab), run_time=1.2)
        self.at("two of each")
        self.play(Indicate(VGroup(prods[0], prods[1]), color=TEXT, scale_factor=1.03), run_time=0.9)
        self.play(Indicate(VGroup(prods[2], prods[3]), color=TEXT, scale_factor=1.03), run_time=0.9)
        self.finish()


def icon(x, y, kind_):
    cols = [BLUE, GREEN, ORANGE, PURPLE] if kind_ == 0 else [BLUE, PURPLE, ORANGE, GREEN]
    pts = [(-0.14, 0.14), (0.14, 0.14), (-0.14, -0.14), (0.14, -0.14)]
    g = VGroup(Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0]),
               *[Dot(radius=0.09, color=c).move_to([x + dx, y + dy, 0]) for c, (dx, dy) in zip(cols, pts)])
    return g


class S14Many(W):
    def construct(self):
        random.seed(7)
        seq = [0, 1] * 12
        random.shuffle(seq)
        n_t = ValueTracker(0)
        counts = [0, 0]
        # counts as step function of how many icons have landed
        c1 = [0]
        for s in seq:
            c1.append(c1[-1] + (1 if s == 0 else 0))
        base_y = -1.9
        names = [("A", "B"), ("A", "b"), ("a", "B"), ("a", "b")]
        xs = [0.9, 2.45, 4.0, 5.55]
        cols = [(BLUE, GREEN), (BLUE, PURPLE), (ORANGE, GREEN), (ORANGE, PURPLE)]

        def frac(i):
            n = max(1, int(round(n_t.get_value())))
            k1 = c1[min(n, 24)]
            k2 = n - k1
            if n_t.get_value() < 0.5:
                return 0.0
            return [k1, k2, k2, k1][i] / (2.0 * n)

        bars = VGroup()
        for i in range(4):
            def mk(i=i):
                h = max(0.02, frac(i) * 8.0)
                return Rectangle(width=1.0, height=h, stroke_color=cols[i][1], stroke_width=5, fill_color=cols[i][0], fill_opacity=0.85).move_to([xs[i], base_y + h / 2, 0])
            bars.add(always_redraw(mk))
        labs = VGroup(*[kind(a, b, 34).move_to([x, base_y - 0.4, 0]) for (a, b), x in zip(names, xs)])
        axis = Line([0.2, base_y, 0], [6.4, base_y, 0], color=GREY, stroke_width=3)
        grid = VGroup()
        icons = []
        for k, s in enumerate(seq):
            r, cidx = divmod(k, 6)
            ic = icon(-5.9 + 0.82 * cidx, 3.0 - 0.9 * r, s)
            icons.append(ic)
        self.add(axis, labs, bars)
        self.play(n_t.animate.set_value(24), LaggedStart(*[FadeIn(ic, scale=0.4) for ic in icons], lag_ratio=1.0 / 24 * 1.0), run_time=3.6, rate_func=linear)
        self.at("both layouts")
        ia, ib = icon(-5.4, -1.0, 0), icon(-5.4, -2.2, 1)
        ta, tb = T("1/2", 34, TEXT, weight=BOLD).next_to(ia, RIGHT, buff=0.3), T("1/2", 34, TEXT, weight=BOLD).next_to(ib, RIGHT, buff=0.3)
        self.play(FadeIn(ia), FadeIn(ib), FadeIn(ta), FadeIn(tb), run_time=1.0)
        self.at("all four kinds")
        self.play(Indicate(bars, color=YELLOW, scale_factor=1.06), run_time=1.2)
        self.at("a quarter each")
        quarters = VGroup(*[T("1/4", 34, YELLOW, weight=BOLD).move_to([x, base_y + 0.25 * 8.0 + 0.45, 0]) for x in xs])
        self.play(FadeIn(quarters, shift=UP * 0.1), run_time=1.0)
        self.at("independent assortment")
        ban = T("Independent assortment = the coin tosses, counted over many", 28, YELLOW, weight=BOLD).move_to([0, -3.45, 0])
        self.play(FadeIn(ban, shift=UP * 0.1), run_time=1.2)
        self.finish()


class S15MorePairs(W):
    def construct(self):
        xs = [-4.9, -1.65, 1.65, 4.9]
        cols = [(BLUE, ORANGE), (GREEN, PURPLE), (GA, GA), (GB, GB)]
        grp = VGroup()
        coins = VGroup()
        for i, (x, (c1, c2)) in enumerate(zip(xs, cols)):
            a, b = rods_pair(c1, c2, x, 1.2, 2.8, 0.3, None, None, 0.42)
            drift(a.g, 0.04, 1.2, i)
            drift(b.g, 0.04, 1.4, i)
            grp.add(a.g, b.g)
            cn = coin([x, 2.95], 0.42)
            coins.add(cn)
        eq = DashedLine([-6.6, 1.2, 0], [6.6, 1.2, 0], color=GREY, stroke_width=2, dash_length=0.18)
        self.add(eq)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in grp], lag_ratio=0.1), run_time=1.0)
        self.at("each extra pair")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in coins], lag_ratio=0.2), run_time=1.0)
        for i, c in enumerate(coins):
            c.p0 = c.get_center()
            c.stretch_to_fit_height(0.72)
            spin(c, 4.0 + 0.9 * i, 0.4 * i)
        self.at("combinations climb")
        l1 = M("4 pairs: 2 × 2 × 2 × 2 = 16", 38, YELLOW).move_to([0, -0.7, 0])
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=1.2)
        self.at("two choices")
        base = M("human, 23 pairs: 2", 38, TEXT)
        ex = M("23", 26, TEXT).next_to(base, RIGHT, buff=0.04).shift(UP * 0.2)
        tail = M("≈ 8.4 million", 38, TEXT).next_to(ex, RIGHT, buff=0.14).align_to(base, DOWN)
        l2 = VGroup(base, ex, tail).move_to([0, -2.0, 0])
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=1.2)
        note = T("ignoring crossing over", 26, GREY).move_to([0, -3.3, 0])
        self.play(FadeIn(note), run_time=0.8)
        self.finish()


def pair_pic(cx, cy, c1, c2, l1, l2, length=2.5):
    a, b = rods_pair(c1, c2, cx, cy, length, 0.2, None, None, 0.34)
    t1 = T(l1, 28, TEXT, weight=BOLD).move_to(a.rods.get_center() + LEFT * 0.6)
    t2 = T(l2, 28, TEXT, weight=BOLD).move_to(b.rods.get_center() + LEFT * 0.6)
    return VGroup(a.g, b.g, t1, t2), a, b


class S16Scope(W):
    def construct(self):
        pl = RoundedRectangle(corner_radius=0.2, width=6.3, height=5.6, stroke_color=GREY, stroke_width=3).move_to([-3.4, 0.1, 0])
        pr = RoundedRectangle(corner_radius=0.2, width=6.3, height=5.6, stroke_color=GREY, stroke_width=3).move_to([3.4, 0.1, 0])
        p1, a1, b1 = pair_pic(-4.9, 1.2, BLUE, ORANGE, "A", "a")
        p2, a2, b2 = pair_pic(-1.9, 1.2, GREEN, PURPLE, "B", "b")
        tl = VGroup(T("different chromosomes:", 28, TEXT, weight=BOLD), T("independent", 28, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.12).move_to([-3.4, -1.3, 0])
        # right: one pair carrying A and B close together
        a, b = rods_pair(BLUE, ORANGE, 3.5, 1.2, 4.4, 0.24, None, None, 0.4)
        la, lb = T("A B", 30, TEXT, weight=BOLD).move_to([2.35, 1.2 + 0.98, 0]), T("a b", 30, TEXT, weight=BOLD).move_to([2.35, 1.2 - 0.98, 0])
        tick = VGroup(*[Rectangle(width=0.16, height=0.34, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to([2.3 + 0.28 * k, 1.2 + o, 0]) for k in (0, 1) for o in (0.4, -0.4)])
        brk = Brace(Line([2.1, 0, 0], [2.7, 0, 0]), UP, color=YELLOW).shift(UP * 1.9 + DOWN * 0.0)
        brk.move_to([2.5, 2.35, 0])
        tr = VGroup(T("close together:", 28, TEXT, weight=BOLD), T("travel together", 28, YELLOW, weight=BOLD), T("(linkage)", 28, TEXT, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([3.4, -1.25, 0])
        self.at("this holds")
        self.play(Create(pl), FadeIn(p1), FadeIn(p2), run_time=1.6)
        self.at("genes on different")
        self.play(FadeIn(tl, shift=UP * 0.1), run_time=1.0)
        self.at("genes close together")
        self.play(Create(pr), FadeIn(a.g), FadeIn(b.g), run_time=1.4)
        self.play(FadeIn(tick), FadeIn(la), FadeIn(lb), FadeIn(tr), run_time=1.4)
        self.at("something has to hold")
        # push in on one pair
        L2 = L
        na, nb = rods_pair(BLUE, ORANGE, 0, CY, L2, TH, "A", "a", 0.42)
        dotted = DashedVMobject(Ellipse(width=L2 + 2.4, height=2.7, stroke_color=YELLOW, stroke_width=4).move_to([0, CY, 0]), num_dashes=40)
        self.play(FadeOut(VGroup(pl, pr, p1, p2, tl, tick, la, lb, tr)), ReplacementTransform(a.g, na.g), ReplacementTransform(b.g, nb.g), run_time=1.8)
        self.play(Create(dotted), run_time=1.5)
        self.at("chapter two")
        ch2 = T("chapter 2", 44, YELLOW, weight=BOLD).move_to([0, CY - 2.0, 0])
        self.play(FadeIn(ch2, shift=UP * 0.15), run_time=1.0)
        self.finish()


class S17Idea(W):
    def construct(self):
        # faint drifting rods behind the text
        bg = VGroup()
        for i, (x, y, col) in enumerate([(-5.2, -1.0, BLUE), (5.0, 2.2, ORANGE), (4.2, -2.3, GREEN), (-4.8, 2.6, PURPLE)]):
            r = RoundedRectangle(corner_radius=0.2, width=3.6, height=0.6, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.5).move_to([x, y, 0])
            r.set_opacity(0.10)
            r.v = 0.1 + 0.05 * i

            def f(m, dt):
                m.rotate(m.v * dt)
            r.add_updater(f)
            bg.add(r)
        self.add(bg)
        self.at("here is the idea")
        hd = T("The idea (simple Mendelian model)", 38, TEAL, weight=BOLD).move_to([-6.2, 3.1, 0]).align_to([-6.2, 0, 0], LEFT)
        self.play(FadeIn(hd, shift=RIGHT * 0.2), run_time=1.0)
        note = T("Mendelian model; exceptions in the lesson", 22, GREY).move_to([0, -3.55, 0])
        self.add(note)
        l1 = T("Meiosis I deals one homolog of each pair.", 44, TEXT).align_to([-6.2, 0, 0], LEFT).set_y(1.9)
        l2 = T("Each pair: its own fair coin toss.", 44, TEXT).align_to([-6.2, 0, 0], LEFT).set_y(0.8)
        l3 = T("Meiosis II splits sisters.", 44, TEXT).align_to([-6.2, 0, 0], LEFT).set_y(-0.3)
        self.at("meiosis I deals")
        self.play(Write(l1), run_time=2.2)
        self.at("each pair is dealt")
        c = coin([5.2, 0.8], 0.45)
        spin(c, 5.0)
        self.play(Write(l2), FadeIn(c), run_time=2.0)
        self.at("meiosis II then")
        self.play(Write(l3), run_time=1.8)
        self.at("segregation is the deal")
        card1 = RoundedRectangle(corner_radius=0.1, width=0.8, height=1.1, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.4)
        card2 = RoundedRectangle(corner_radius=0.1, width=0.8, height=1.1, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.4)
        cards = VGroup(card1, card2).arrange(RIGHT, buff=0.15).move_to([-5.4, -1.9, 0])
        s1 = T("segregation", 34, YELLOW, weight=BOLD).next_to(cards, RIGHT, buff=0.35)
        self.play(FadeIn(cards, shift=UP * 0.2), FadeIn(s1), run_time=1.0)
        self.play(card1.animate.shift(LEFT * 0.25 + UP * 0.1), card2.animate.shift(RIGHT * 0.25 + DOWN * 0.1), run_time=1.2)
        self.at("independent assortment is")
        c2 = coin([-0.2, -1.9], 0.45)
        spin(c2, 5.5)
        s2 = T("independent assortment", 32, YELLOW, weight=BOLD).next_to(c2, RIGHT, buff=0.3)
        self.play(FadeIn(c2, scale=0.5), FadeIn(s2), run_time=1.2)
        self.finish()


class S18End(EndCard):
    LINE = "Meiosis I deals one homolog per pair, each by coin toss."
