"""Wells Share One Scoop: film 2 of the evidence workshop (Biochemistrypedia explainer)

COLOUR MAP (same in both films, as in film 1)
  BLUE  = the scoop, theta        GREEN = capture, gamma        GOLD = the well, delta
  TEAL filled bar = chance the pond is still occupied      RED dashed line = the 5% stop line
Bars and gauges are computed from the lesson's formula (labelled 'computed'); the tree is a schematic.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PX = -2.35            # centre of the tree
BARX = 4.6            # the meter column (same place as film 1's side bar)
K = 0.4               # bar: 0.4 units of height per percent (frame is 5 tall = 12.5%)
BASE = -2.8           # meter floor
PONDY, BY, TY, WY = 3.25, 1.75, 0.3, -0.75
THETA, GAMMA, DELTA, PRIOR = 0.60, 0.49, 0.38, 0.20


def q_of(n, ext=2):
    """One sample's chance of detecting an occupied pond: n wells per extraction, ext extractions."""
    p = GAMMA * (1 - (1 - DELTA) ** n)
    return THETA * (1 - (1 - p) ** ext)


def pct_of(nb, n):
    """Chance the pond is still occupied after nb all-negative samples (n wells per extraction), in %."""
    m = (1 - q_of(n)) ** nb
    return 100 * PRIOR * m / ((1 - PRIOR) + PRIOR * m)


def pct_indep(k=20):
    """The mistaken version: k wells as if they were k independent samples, each detecting with 0.60 x 0.49 x 0.38."""
    m = (1 - THETA * GAMMA * DELTA) ** k
    return 100 * PRIOR * m / ((1 - PRIOR) + PRIOR * m)


def ambient(scene, n=16, seed=3):
    rng = random.Random(seed)
    motes = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.02, 0.05), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.12, 0.3))
        d.move_to([rng.uniform(-7, 7), rng.uniform(-4, 4), 0])
        d.v = (rng.uniform(-0.12, 0.12), rng.uniform(0.05, 0.2))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 4.1:
                m.shift(DOWN * 8.2)
            if abs(m.get_x()) > 7.2:
                m.shift(LEFT * 14.4 * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-10)
    scene.add(motes)


def shimmer(scene, squares):
    """Slow glow on the gold wells so a held tree is never a dead frame."""
    g = VGroup(*squares)
    g.t = 0.0
    for i, s in enumerate(g):
        s.ph = (i * 0.77) % 6.28

    def sh(grp, dt):
        grp.t += dt
        for s in grp:
            s.set_stroke(opacity=0.7 + 0.3 * np.sin(grp.t * 1.6 + s.ph))
    g.add_updater(sh)
    scene.add(g)
    return g


def bottle(color=BLUE, s=1.0):
    body = RoundedRectangle(corner_radius=0.08, width=0.42, height=0.55, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=0.3)
    neck = Rectangle(width=0.18, height=0.2, stroke_color=color, stroke_width=3.5, fill_opacity=0).next_to(body, UP, buff=0)
    return VGroup(body, neck).scale(s)


def tube_icon(w=0.3, h=0.5):
    return RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_color=GREEN, stroke_width=3.5,
                            fill_color=GREEN, fill_opacity=0.3)


def well_sq(w):
    return RoundedRectangle(corner_radius=0.04, width=w, height=w, stroke_color=GOLD, stroke_width=2.5,
                            fill_color=GOLD, fill_opacity=0.25)


def cross(w, h, center, sw=7):
    x, y = center[0], center[1]
    return VGroup(Line([x - w / 2, y + h / 2, 0], [x + w / 2, y - h / 2, 0]),
                  Line([x - w / 2, y - h / 2, 0], [x + w / 2, y + h / 2, 0])).set_stroke(RED, sw)


class Tree:
    """The pond -> bottles (blue) -> tubes (green) -> wells (gold) tree, always in the same place."""

    def __init__(self, nb=2, rows=1):
        self.nb = nb
        if nb == 2:
            dx, w, gap, self.rp, tw = 0.34, 0.26, 0.3, 0.3, 0.3
        else:
            dx, w, gap, self.rp, tw = 0.22, 0.17, 0.15, 0.22, 0.22
        self.dx, self.w = dx, w
        nt = 2 * nb
        block = 5 * dx
        pitch = block + gap
        total = nt * pitch - gap
        x0 = PX - total / 2 + block / 2
        self.tx = [x0 + j * pitch for j in range(nt)]
        self.bx = [(self.tx[2 * i] + self.tx[2 * i + 1]) / 2 for i in range(nb)]
        self.pond = VGroup(Ellipse(width=2.4, height=0.8, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.14),
                           T("S2", 30, TEXT, weight=BOLD)).move_to([PX, PONDY, 0])
        self.bottles = [bottle(BLUE, 1.4).move_to([x, BY, 0]) for x in self.bx]
        self.l_pb = [Line([PX, PONDY - 0.4, 0], [x, BY + 0.53, 0], color=BLUE, stroke_width=3.5) for x in self.bx]
        self.tubes = [tube_icon(tw).move_to([x, TY, 0]) for x in self.tx]
        self.l_bt = [Line([self.bx[j // 2], BY - 0.53, 0], [x, TY + 0.25, 0], color=GREEN, stroke_width=3.5) for j, x in enumerate(self.tx)]
        self.rows = []
        self.l_tw = []
        for j, x in enumerate(self.tx):
            rr = []
            for r in range(rows):
                rr.append(VGroup(*[well_sq(w).move_to([x + (c - 2) * dx, WY - r * self.rp, 0]) for c in range(5)]))
            self.rows.append(rr)
            self.l_tw.append(VGroup(*[Line([x, TY - 0.25, 0], [x + (c - 2) * dx, WY + w / 2, 0], color=GOLD, stroke_width=2.5)
                                      for c in range(5)]))

    def parts(self):
        return [self.pond] + self.l_pb + self.bottles + self.l_bt + self.tubes + self.l_tw + [r[0] for r in self.rows]

    def struct(self):
        return self.l_pb + self.bottles + self.l_bt + self.tubes + self.l_tw

    def extra(self, lo=1, hi=None):
        hi = hi if hi is not None else len(self.rows[0])
        return VGroup(*[self.rows[j][r] for r in range(lo, hi) for j in range(len(self.rows))])

    def row_squares(self, r=0):
        return [s for j in range(len(self.rows)) for s in self.rows[j][r]]

    def box(self, i):
        yt, yb = BY + 0.8, WY - (len(self.rows[0]) - 1) * self.rp - 0.4
        x0, x1 = self.tx[2 * i] - 0.9, self.tx[2 * i + 1] + 0.8
        return RoundedRectangle(corner_radius=0.2, width=x1 - x0, height=yt - yb, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.07).move_to([(x0 + x1) / 2, (yt + yb) / 2, 0])


def meter(val, per, fmt, title, fill_color, tsize=26, ty=2.95):
    """A vertical gauge in the side column. The fill and the readout follow `val`."""
    frame = Rectangle(width=1.4, height=5.0, stroke_color=GREY, stroke_width=3).move_to([BARX, -0.3, 0])

    def fill_fn(m):
        h = max(val.get_value() * per, 0.02)
        m.become(Rectangle(width=1.4, height=h, stroke_width=0, fill_color=fill_color, fill_opacity=0.92).move_to([BARX, BASE + h / 2, 0]))
    fill = Rectangle(width=1.4, height=0.1, stroke_width=0)
    fill_fn(fill)
    fill.add_updater(fill_fn)

    def ro_fn(m):
        m.become(M(fmt(val.get_value()), 30, TEXT, weight=BOLD).move_to([BARX, 1.65, 0]))
    ro = M("0", 30, TEXT)
    ro_fn(ro)
    ro.add_updater(ro_fn)
    ttl = T(title, tsize, TEXT).move_to([BARX, ty, 0])
    return VGroup(frame, fill, ro, ttl)


def stop_line():
    y = BASE + 5 * K
    return VGroup(DashedLine([3.75, y, 0], [5.3, y, 0], color=RED, stroke_width=6),
                  T("5% stop\nline", 24, RED).move_to([6.1, y, 0])).set_z_index(4)


def computed_tag():
    return T("computed", 24, TEXT).set_opacity(0.8).move_to([BARX, -3.3, 0])


BAR_TITLE = "chance S2 is\nstill occupied"
Q_TITLE = "q: a sample's\nchance of detecting\nan occupied pond"


def counter_lines(lines, x=2.75, y0=1.9, step=0.7):
    cols = {"b": BLUE, "g": GREEN, "y": GOLD}
    return [T(s, 32, cols[c], weight=BOLD).move_to([x, y0 - i * step, 0]) for i, (c, s) in enumerate(lines)]


def per_tube(n_text):
    lab = T("wells\nper tube", 28, GOLD, weight=BOLD).move_to([2.6, 1.3, 0])
    num = M(n_text, 64, GOLD, weight=BOLD).move_to([2.6, 0.2, 0])
    return lab, num


def morph_to_three(scene, tr2, run=1.2):
    """Slide the two-bottle tree into the compact three-bottle layout; returns the new Tree (bottle 3 not yet shown)."""
    tr3 = Tree(3, 1)
    pairs = []
    for i in range(2):
        pairs += [(tr2.bottles[i], tr3.bottles[i]), (tr2.l_pb[i], tr3.l_pb[i])]
    for j in range(4):
        pairs += [(tr2.tubes[j], tr3.tubes[j]), (tr2.l_bt[j], tr3.l_bt[j]), (tr2.l_tw[j], tr3.l_tw[j]), (tr2.rows[j][0], tr3.rows[j][0])]
    scene.play(*[ReplacementTransform(a, b) for a, b in pairs], run_time=run)
    return tr3


def add_tree(scene, tr, extra=False):
    scene.add(*tr.parts())
    if extra:
        scene.add(tr.extra())


def outlines(tr):
    return VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.05, width=0.3, height=0.5, stroke_color=BLUE, stroke_width=3.5), num_dashes=14)
                    .move_to([s.get_x(), -0.28, 0]) for s in tr.row_squares(0)])


def columns(tr):
    """Twenty one-well columns (bottle, tube, well) above the tree's own 20 wells."""
    bs, ts, l1, l2 = [], [], [], []
    for s in tr.row_squares(0):
        x = s.get_x()
        bs.append(bottle(BLUE, 0.65).move_to([x, 1.65, 0]))
        ts.append(tube_icon(0.17, 0.36).move_to([x, 0.55, 0]))
        l1.append(Line([x, 1.65 - 0.27, 0], [x, 0.55 + 0.18, 0], color=GREEN, stroke_width=3))
        l2.append(Line([x, 0.55 - 0.18, 0], [x, WY + tr.w / 2, 0], color=GOLD, stroke_width=3))
    return bs, ts, l1, l2


def eq_line():
    parts = [M("0.60", 30, BLUE, weight=BOLD), M("×", 30, TEXT), M("0.49", 30, GREEN, weight=BOLD), M("×", 30, TEXT),
             M("0.38", 30, GOLD, weight=BOLD), M("=", 30, TEXT), M("0.11", 30, TEXT, weight=BOLD)]
    return VGroup(*parts).arrange(RIGHT, buff=0.22)


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Integrative Evidence Workshop"
    TITLE = "Wells Share One Scoop"


class S01Link(SpokenScene):
    def construct(self):
        ambient(self)
        plate = RoundedRectangle(corner_radius=0.2, width=4.8, height=3.6, stroke_color=GREY, stroke_width=4).move_to([3.0, 0.6, 0])
        cells = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.55, height=0.55, stroke_color=GOLD, stroke_width=3,
                                          fill_color=GOLD, fill_opacity=0.25) for _ in range(20)]).arrange_in_grid(4, 5, buff=0.2).move_to(plate)
        plab = T("afternoon in the lab", 34, GOLD, weight=BOLD).move_to([3.0, -1.7, 0])
        self.play(FadeIn(plate), LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.06), FadeIn(plab, shift=UP * 0.15), run_time=2.0)
        self.play(Indicate(cells, color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("not a field trip")
        boot = Polygon([-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, -0.2, 0], [0.15, -0.05, 0], [0.12, 0.7, 0], [-0.35, 0.7, 0], [-0.35, -0.2, 0],
                       stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).scale(1.5)
        bt = bottle(BLUE, 2.4)
        icon = VGroup(boot, bt).arrange(RIGHT, buff=0.5).move_to([-3.4, 0.6, 0])
        flab = T("field trip", 34, TEXT, weight=BOLD).move_to([-3.4, -1.7, 0])
        self.play(FadeIn(icon, shift=RIGHT * 0.3), FadeIn(flab), run_time=1.2)
        self.play(icon.animate.shift(UP * 0.15), run_time=0.8, rate_func=there_and_back)
        self.at("pond s2")
        pond = VGroup(Ellipse(width=5.4, height=3.6, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.14),
                      T("S2", 80, TEXT, weight=BOLD)).move_to([PX, 0.3, 0])
        self.play(FadeOut(icon), FadeOut(flab), FadeIn(pond, scale=0.8), run_time=1.2)
        self.at("20 negative wells")
        neg = T("20 wells:\nall negative", 34, GOLD, weight=BOLD).move_to([3.0, -2.35, 0])
        self.play(Transform(plab, neg), *[c.animate.set_fill(GOLD, 0.0) for c in cells], run_time=1.4)
        self.at("are those 20 tries")
        t20 = chip("20 tries?", YELLOW, 34).move_to([-4.3, -2.9, 0])
        self.play(FadeIn(t20, shift=UP * 0.2), run_time=0.8)
        self.at("or only two")
        t2 = chip("2 tries?", YELLOW, 34).move_to([-0.4, -2.9, 0])
        self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.8)
        self.play(Indicate(t2, color=YELLOW, scale_factor=1.12), Indicate(pond[1], color=TEXT, scale_factor=1.1), run_time=1.2)
        self.finish()


class S02Tree(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 1)
        big = VGroup(Ellipse(width=5.4, height=3.6, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.14),
                     T("S2", 80, TEXT, weight=BOLD)).move_to([PX, 0.3, 0])
        self.add(big)
        self.wait(0.4)
        self.play(ReplacementTransform(big, tr.pond), run_time=1.6)
        self.at("the pond gives two blue")
        c1, c2, c3 = counter_lines([("b", "2 bottles"), ("g", "4 tubes"), ("y", "20 wells")], y0=1.9)
        self.play(*[Create(l) for l in tr.l_pb], *[GrowFromPoint(b, [PX, PONDY - 0.4, 0]) for b in tr.bottles], FadeIn(c1, shift=LEFT * 0.2), run_time=1.6)
        self.at("each bottle gives")
        self.play(*[Create(l) for l in tr.l_bt], *[FadeIn(t, shift=DOWN * 0.15) for t in tr.tubes], FadeIn(c2, shift=LEFT * 0.2), run_time=1.6)
        self.at("each tube feeds")
        self.play(*[Create(l) for l in tr.l_tw], run_time=0.8)
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in tr.row_squares(0)], lag_ratio=0.05), FadeIn(c3, shift=LEFT * 0.2), run_time=2.0)
        shimmer(self, tr.row_squares(0))
        self.at("so all 20 wells hang")
        b0, b1 = tr.box(0), tr.box(1)
        self.play(Create(b0), Create(b1), run_time=1.2)
        self.at("from just two")
        self.play(Indicate(tr.bottles[0], color=BLUE, scale_factor=1.3), Indicate(tr.bottles[1], color=BLUE, scale_factor=1.3), run_time=1.4)
        self.play(Indicate(c1, color=BLUE, scale_factor=1.15), run_time=1.0)
        self.finish()


class S03Numbers(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 1)
        add_tree(self, tr)
        shimmer(self, tr.row_squares(0))
        cover = Rectangle(width=14.5, height=8.2, stroke_width=0, fill_color=BG, fill_opacity=0.0).move_to([0, 0, 0]).set_z_index(5)
        self.add(cover)
        r_prior = T("prior = 0.20", 34, TEXT)
        r_stop = T("stop line = 5%", 34, RED)
        r_theta = T("θ = 0.60  (our choice)", 34, BLUE, weight=BOLD)
        r_g = T("γ = 0.49", 34, GREEN)
        r_d = T("δ = 0.38", 34, GOLD)
        r_gd = VGroup(r_g, r_d).arrange(RIGHT, buff=0.7)
        r_src = T("borrowed: wild pigs,\ncentral Texas (illustrative)", 28, TEXT)
        rows = VGroup(r_prior, r_stop, r_theta, r_gd, r_src).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to([PX, 0.2, 0]).set_z_index(6)
        qv = ValueTracker(0.0)
        gauge = meter(qv, 5, lambda v: f"{v:.3f}", Q_TITLE, TEXT, ty=3.0)
        gauge[1].set_fill(TEXT, 0.55)
        yb = BASE + THETA * 5
        bline = Line([3.75, yb, 0], [5.3, yb, 0], color=BLUE, stroke_width=7)
        blab = T("θ", 40, BLUE, weight=BOLD).move_to([5.85, yb, 0])
        for m_ in (gauge, bline, blab):
            m_.set_z_index(7)
        self.play(cover.animate.set_fill(BG, 0.84), run_time=1.0)
        self.play(FadeIn(r_prior, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(r_stop, shift=RIGHT * 0.2), run_time=0.6)
        self.at("a scoop holds")
        self.play(FadeIn(r_theta, shift=RIGHT * 0.2), FadeIn(gauge[0]), FadeIn(gauge[3]), Create(bline), FadeIn(blab), run_time=1.4)
        self.add(gauge[1], gauge[2])
        self.at("that is theta")
        self.play(Indicate(r_theta, color=BLUE, scale_factor=1.08), Indicate(bline, color=BLUE, scale_factor=1.15), Indicate(blab, color=BLUE, scale_factor=1.4), run_time=1.6)
        self.at("the capture and well values")
        self.play(FadeIn(r_gd, shift=RIGHT * 0.2), qv.animate.set_value(q_of(5)), run_time=2.0)
        self.at("borrowed from a wild pig")
        self.play(FadeIn(r_src, shift=RIGHT * 0.2), run_time=1.0)
        self.at("illustrations only")
        self.play(Indicate(r_src, color=TEXT, scale_factor=1.05), run_time=1.0)
        self.play(FadeOut(rows), cover.animate.set_fill(BG, 0.0), run_time=0.9)
        self.finish()


class S04MoreWells(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 10)
        add_tree(self, tr)
        shimmer(self, tr.row_squares(0))
        nv = ValueTracker(5)
        qv = ValueTracker(q_of(5))
        qv.add_updater(lambda t: t.set_value(q_of(nv.get_value())))
        self.add(qv)
        gauge = meter(qv, 5, lambda v: f"{v:.3f}", Q_TITLE, TEXT, ty=3.0)
        gauge[1].set_fill(TEXT, 0.55)
        yb = BASE + THETA * 5
        bline = Line([3.75, yb, 0], [5.3, yb, 0], color=BLUE, stroke_width=7)
        blab = T("θ", 40, BLUE, weight=BOLD).move_to([5.85, yb, 0])
        self.add(gauge, bline, blab)
        lab, num = per_tube("5")
        self.at("try adding wells")
        self.play(FadeIn(lab, shift=LEFT * 0.2), FadeIn(num, shift=LEFT * 0.2), run_time=1.0)
        self.at("pour more gold wells")
        self.play(FadeIn(tr.extra(1, 2), shift=DOWN * 0.1), Transform(num, M("10", 64, GOLD, weight=BOLD).move_to(num)), nv.animate.set_value(10), run_time=1.0)
        self.at("under the same two bottles")
        self.play(FadeIn(tr.extra(2, 4), shift=DOWN * 0.1), Transform(num, M("20", 64, GOLD, weight=BOLD).move_to(num)), nv.animate.set_value(20), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(tr.extra(r, r + 1), shift=DOWN * 0.1) for r in range(4, 10)], lag_ratio=0.2),
                  Transform(num, M("50", 64, GOLD, weight=BOLD).move_to(num)), nv.animate.set_value(50), run_time=1.6)
        self.at("the gauge for one sample")
        self.play(Indicate(gauge[0], color=TEXT, scale_factor=1.04), run_time=1.2)
        self.at("climbs at first")
        y5 = BASE + q_of(5) * 5
        up = Arrow([3.45, y5 - 0.1, 0], [3.45, y5 + 0.7, 0], color=TEXT, buff=0, stroke_width=6)
        self.play(GrowArrow(up), Indicate(gauge[2], color=TEXT, scale_factor=1.15), run_time=1.2)
        self.at("then it levels off")
        yp = BASE + q_of(10 ** 6) * 5
        plat = DashedLine([3.9, yp, 0], [5.3, yp, 0], color=TEXT, stroke_width=5)
        plab = M("0.444", 26, TEXT).move_to([6.05, yp, 0])
        self.play(FadeOut(up), Create(plat), FadeIn(plab), run_time=1.2)
        self.at("still below the blue line")
        gap = Rectangle(width=1.4, height=yb - yp, stroke_width=0, fill_color=BLUE, fill_opacity=0.28).move_to([BARX, (yb + yp) / 2, 0])
        gt = T("gap", 28, TEXT).move_to([BARX, (yb + yp) / 2, 0])
        self.play(FadeIn(gap), FadeIn(gt), run_time=1.0)
        self.at("it never crosses theta")
        self.play(Indicate(bline, color=BLUE, scale_factor=1.15), Indicate(blab, color=BLUE, scale_factor=1.4), Indicate(plat, color=TEXT, scale_factor=1.15), run_time=1.4)
        self.at("however many wells")
        self.play(Indicate(tr.extra(), color=GOLD, scale_factor=1.02), Indicate(num, color=GOLD, scale_factor=1.2), run_time=1.4)
        self.finish()


class S05Why(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 10)
        add_tree(self, tr, extra=True)
        shimmer(self, tr.row_squares(0))
        rng = random.Random(4)
        dots = VGroup()
        bxB = tr.bx[1]
        for _ in range(5):
            d = Dot(radius=0.055, color=TEXT).move_to([bxB + rng.uniform(-0.15, 0.15), BY - 0.2 + rng.uniform(-0.2, 0.2), 0])
            d.t0 = rng.uniform(0, 6)
            d.c = d.get_center().copy()

            def wob(m, dt):
                m.t0 += dt
                m.move_to(m.c + np.array([0.04 * np.sin(2.1 * m.t0), 0.04 * np.cos(1.7 * m.t0), 0]))
            d.add_updater(wob)
            dots.add(d)
        self.at("if the scoop held no")
        lab = T("no DNA in\nthis scoop", 28, TEXT, weight=BOLD).move_to([-5.5, 2.65, 0])
        arr = Arrow([-4.65, 2.25, 0], [-4.7, 1.95, 0], color=TEXT, buff=0, stroke_width=4)
        self.play(FadeIn(dots), FadeIn(lab, shift=RIGHT * 0.2), GrowArrow(arr), Indicate(tr.bottles[0], color=BLUE, scale_factor=1.3), run_time=1.6)
        self.at("every tube and every well")
        xa0, xa1 = tr.tx[0] - 0.95, tr.tx[1] + 0.95
        yt, yb = BY - 0.7, WY - 9 * tr.rp - 0.35
        cov = Rectangle(width=xa1 - xa0, height=yt - yb, stroke_width=0, fill_color=BG, fill_opacity=0.0).move_to([(xa0 + xa1) / 2, (yt + yb) / 2, 0]).set_z_index(5)
        self.add(cov)
        cx = [cross(0.5, 0.7, [tr.tx[j], TY]).set_z_index(6) for j in range(2)]
        self.play(cov.animate.set_fill(BG, 0.7), *[Create(c) for c in cx], run_time=1.4)
        self.at("testing empty water")
        big = cross(3.4, 3.2, [(xa0 + xa1) / 2, -2.1], sw=8).set_z_index(6)
        self.play(Create(big), run_time=1.4)
        self.at("no number of wells")
        self.play(Indicate(big, color=RED, scale_factor=1.06), Indicate(tr.extra(), color=GOLD, scale_factor=1.02), run_time=1.6)
        self.at("that the sample does not contain")
        self.play(Indicate(lab, color=TEXT, scale_factor=1.1), Indicate(tr.bottles[0], color=BLUE, scale_factor=1.3), run_time=1.4)
        self.finish()


class S06Bar(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 10)
        add_tree(self, tr, extra=True)
        shimmer(self, tr.row_squares(0))
        lab, num = per_tube("50")
        self.add(lab, num)
        nv = ValueTracker(5)
        pv = ValueTracker(pct_of(2, 5))
        pv.add_updater(lambda t: t.set_value(pct_of(2, nv.get_value())))
        self.add(pv)
        bar = meter(pv, K, lambda v: f"{v:.1f}%", BAR_TITLE, TEAL)
        self.play(FadeOut(tr.extra()), Transform(num, M("5", 64, GOLD, weight=BOLD).move_to(num)), FadeIn(bar), FadeIn(computed_tag()), run_time=0.8)
        self.at("watch the bar")
        self.at("that s2 is still occupied")
        self.play(Indicate(tr.pond, color=BLUE, scale_factor=1.08), Indicate(bar[1], color=TEAL, scale_factor=1.04), run_time=1.4)
        self.at("with unlimited wells")
        self.play(LaggedStart(*[FadeIn(tr.extra(r, r + 1), shift=DOWN * 0.1) for r in range(1, 10)], lag_ratio=0.2),
                  Transform(num, M("50", 64, GOLD, weight=BOLD).move_to(num)), nv.animate.set_value(50), run_time=1.0)
        shimmer(self, [q for r in range(1, 10) for q in tr.row_squares(r)])
        self.at("on two samples")
        self.play(Indicate(tr.bottles[0], color=BLUE, scale_factor=1.3), Indicate(tr.bottles[1], color=BLUE, scale_factor=1.3), run_time=1.4)
        self.at("stops at 7")
        self.play(Indicate(bar[2], color=YELLOW, scale_factor=1.25), run_time=1.4)
        self.at("that is still above")
        sl = stop_line()
        self.play(FadeIn(sl), run_time=0.8)
        sl.t = 0.0

        def pulse(m, dt):
            m.t += dt
            m[0].set_stroke(opacity=0.65 + 0.35 * np.sin(m.t * 3.0))
        sl.add_updater(pulse)
        self.at("the 5 percent line")
        self.play(Indicate(sl[0], color=RED, scale_factor=1.2), Indicate(bar[1], color=TEAL, scale_factor=1.04), run_time=1.4)
        self.finish()


class S07Bottle(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 10)
        add_tree(self, tr, extra=True)
        shimmer(self, tr.row_squares(0))
        lab, num = per_tube("50")
        self.add(lab, num)
        pv = ValueTracker(pct_of(2, 50))
        bar = meter(pv, K, lambda v: f"{v:.1f}%", BAR_TITLE, TEAL)
        sl = stop_line()
        self.add(bar, sl, computed_tag())
        self.play(FadeOut(tr.extra()), FadeOut(lab), FadeOut(num), pv.animate.set_value(pct_of(2, 5)), run_time=0.8)
        self.at("add a third blue bottle")
        tr3 = morph_to_three(self, tr, run=1.2)
        b3 = tr3.bottles[2]
        c1, c2, c3 = counter_lines([("b", "3 bottles"), ("g", "6 tubes"), ("y", "30 wells")], y0=1.9)
        self.play(Create(tr3.l_pb[2]), GrowFromPoint(b3, [PX, PONDY - 0.4, 0]), FadeIn(c1, shift=LEFT * 0.2), run_time=1.2)
        self.at("a new scoop of water")
        self.play(Indicate(b3, color=BLUE, scale_factor=1.4), Indicate(tr3.pond, color=BLUE, scale_factor=1.08), run_time=1.2)
        self.play(*[Create(tr3.l_bt[j]) for j in (4, 5)], *[FadeIn(tr3.tubes[j], shift=DOWN * 0.15) for j in (4, 5)], FadeIn(c2, shift=LEFT * 0.2), run_time=1.0)
        self.at("with the usual five wells")
        self.play(*[Create(tr3.l_tw[j]) for j in (4, 5)], run_time=0.6)
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for j in (4, 5) for s in tr3.rows[j][0]], lag_ratio=0.08), FadeIn(c3, shift=LEFT * 0.2), run_time=1.4)
        shimmer(self, tr3.row_squares(0))
        self.at("per extraction")
        self.play(Indicate(VGroup(*tr3.tubes), color=GREEN, scale_factor=1.2), run_time=1.2)
        self.at("the bar drops to 4")
        self.play(pv.animate.set_value(pct_of(3, 5)), run_time=1.6)
        self.at("that is below the line")
        tag = T("just under", 30, YELLOW, weight=BOLD).move_to([2.4, -1.65, 0])
        arr = Arrow([3.5, -1.55, 0], [3.95, -1.05, 0], color=YELLOW, buff=0, stroke_width=5)
        self.play(FadeIn(tag), GrowArrow(arr), Indicate(sl[0], color=RED, scale_factor=1.2), run_time=1.2)
        self.finish()


def two_tree_state(scene, tr, with_outlines=True):
    add_tree(scene, tr)
    shimmer(scene, tr.row_squares(0))
    pv = ValueTracker(pct_of(2, 5))
    bar = meter(pv, K, lambda v: f"{v:.1f}%", BAR_TITLE, TEAL)
    sl = stop_line()
    scene.add(bar, sl, computed_tag())
    return pv, bar, sl


class S08Predict(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 1)
        pv, bar, sl = two_tree_state(self, tr)
        self.at("here is a tempting mistake")
        self.play(Indicate(tr.pond, color=BLUE, scale_factor=1.08), run_time=1.2)
        self.at("suppose we pretend")
        self.play(*[l.animate.set_stroke(opacity=0.25) for l in tr.l_tw], run_time=0.8)
        self.at("20 separate trips")
        outs = outlines(tr)
        self.play(LaggedStart(*[FadeIn(o, shift=DOWN * 0.1) for o in outs], lag_ratio=0.1), run_time=2.2)
        self.at("will the pond look emptier")
        self.play(Indicate(bar[1], color=TEAL, scale_factor=1.04), run_time=1.0)
        self.at("emptier")
        e = chip("emptier?", YELLOW, 30).move_to([2.55, 0.5, 0])
        self.play(FadeIn(e, shift=LEFT * 0.2), run_time=0.7)
        self.at("or fuller")
        f = chip("fuller?", YELLOW, 30).move_to([2.55, -0.7, 0])
        self.play(FadeIn(f, shift=LEFT * 0.2), run_time=0.7)
        self.play(Indicate(e, color=YELLOW, scale_factor=1.1), Indicate(f, color=YELLOW, scale_factor=1.1), run_time=1.2)
        self.finish()


class S09Pause(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 1)
        pv, bar, sl = two_tree_state(self, tr)
        for l in tr.l_tw:
            l.set_stroke(opacity=0.25)
        e = chip("emptier?", YELLOW, 30).move_to([2.55, 0.5, 0])
        f = chip("fuller?", YELLOW, 30).move_to([2.55, -0.7, 0])
        cap = T("Predict: emptier or fuller?", 38, YELLOW, weight=BOLD).move_to([PX, -2.3, 0])
        self.add(outlines(tr), e, f, cap)
        for k in range(5, 0, -1):
            n = M(str(k), 64, YELLOW, weight=BOLD).move_to([2.55, 2.3, 0])
            self.add(n)
            self.play(n.animate.scale(0.85).set_opacity(0.5), run_time=0.95)
            self.remove(n)
            self.wait(0.05)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 1)
        pv, bar, sl = two_tree_state(self, tr)
        for l in tr.l_tw:
            l.set_stroke(opacity=0.25)
        outs = outlines(tr)
        e = chip("emptier?", YELLOW, 30).move_to([2.55, 0.5, 0])
        f = chip("fuller?", YELLOW, 30).move_to([2.55, -0.7, 0])
        self.add(outs, e, f)
        self.play(FadeOut(f), Indicate(e, color=YELLOW, scale_factor=1.15), run_time=1.4)
        self.at("redraw the tree as 20")
        bs, ts, l1, l2 = columns(tr)
        old = VGroup(*tr.struct())
        self.play(FadeOut(old), FadeOut(e), FadeOut(outs),
                  LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in bs], lag_ratio=0.05), run_time=1.8)
        self.at("each with one well")
        self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(t), Create(c)) for a, t, c in zip(l1, ts, l2)], lag_ratio=0.05), run_time=1.8)
        self.at("each one now looks like its own try")
        cap = T("per well, as if independent:", 30, TEXT).move_to([PX, -2.2, 0])
        eq = eq_line().move_to([PX, -3.0, 0])
        self.play(FadeIn(cap), FadeIn(eq, shift=UP * 0.15), LaggedStart(*[Indicate(b, color=BLUE, scale_factor=1.3) for b in bs], lag_ratio=0.05), run_time=2.4)
        self.at("the bar plunges to about")
        self.play(pv.animate.set_value(pct_indep()), run_time=1.6)
        self.at("and you would stop")
        fc = chip("false\nconfidence", RED, 28).move_to([2.55, -1.6, 0])
        self.play(FadeIn(fc, shift=LEFT * 0.2), Indicate(sl[0], color=RED, scale_factor=1.2), run_time=1.2)
        self.finish()


class S11Pseudo(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 1)
        self.add(tr.pond, *tr.rows[0][:0], *[r[0] for r in tr.rows])
        shimmer(self, tr.row_squares(0))
        bs, ts, l1, l2 = columns(tr)
        self.add(*bs, *ts, *l1, *l2)
        pv = ValueTracker(pct_indep())
        bar = meter(pv, K, lambda v: f"{v:.1f}%", BAR_TITLE, TEAL)
        sl = stop_line()
        cap = T("per well, as if independent:", 30, TEXT).move_to([PX, -2.2, 0])
        eq = eq_line().move_to([PX, -3.0, 0])
        fc = chip("false\nconfidence", RED, 28).move_to([2.55, -1.6, 0])
        self.add(bar, sl, computed_tag(), cap, eq, fc)
        self.at("in the model")
        em = chip("error in\nthe model", RED, 28).move_to([2.55, -1.6, 0])
        self.play(Transform(fc, em), run_time=1.0)
        self.at("not on evidence")
        self.play(Indicate(fc, color=RED, scale_factor=1.12), run_time=1.2)
        self.at("counting repeated measurements")
        tr2 = Tree(2, 1)
        self.play(FadeOut(VGroup(*bs, *ts, *l1, *l2)), FadeOut(cap), FadeOut(eq), FadeOut(fc),
                  *[Create(l) for l in tr2.l_pb], *[FadeIn(b) for b in tr2.bottles],
                  *[Create(l) for l in tr2.l_bt], *[FadeIn(t) for t in tr2.tubes], *[Create(l) for l in tr2.l_tw], run_time=1.6)
        self.at("of one unit")
        self.play(pv.animate.set_value(pct_of(2, 5)), Indicate(VGroup(*tr2.bottles), color=BLUE, scale_factor=1.3), run_time=1.6)
        self.at("as if they were separate units")
        d1 = T("repeated measurements of one unit,", 30, TEXT).move_to([PX, -2.7, 0])
        d2 = T("counted as separate units", 30, TEXT).move_to([PX, -3.3, 0])
        self.play(FadeIn(d1, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(d2, shift=UP * 0.1), run_time=1.0)
        self.at("it is called pseudo")
        nm = T("pseudoreplication", 52, YELLOW, weight=BOLD).move_to([PX, -1.8, 0])
        self.play(FadeIn(nm, shift=UP * 0.15), run_time=1.0)
        self.play(Indicate(nm, color=YELLOW, scale_factor=1.06), run_time=1.0)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        ambient(self)
        tr = Tree(2, 10)
        add_tree(self, tr)
        shimmer(self, tr.row_squares(0))
        self.at("from one sample")
        yt, yb = BY + 0.8, WY - 0.4
        b0 = RoundedRectangle(corner_radius=0.2, width=3.9, height=yt - yb, stroke_color=BLUE, stroke_width=4,
                              fill_color=BLUE, fill_opacity=0.07).move_to([(tr.tx[0] + tr.tx[1]) / 2, (yt + yb) / 2, 0])
        self.play(Create(b0), run_time=1.0)
        self.at("all test the same water")
        grp = VGroup(tr.tubes[0], tr.tubes[1], *tr.rows[0][0], *tr.rows[1][0])
        self.play(LaggedStart(*[Indicate(m, color=GOLD, scale_factor=1.3) for m in grp], lag_ratio=0.08), run_time=2.0)
        self.at("they are second chances")
        l1 = T("second chances at the lab steps", 32, GOLD, weight=BOLD).move_to([PX, -2.3, 0])
        self.play(FadeOut(b0), FadeIn(l1, shift=UP * 0.15), run_time=1.0)
        self.play(Indicate(VGroup(*tr.tubes), color=GREEN, scale_factor=1.15), run_time=1.0)
        self.at("not new tries")
        l2 = T("not new tries at the scoop", 32, BLUE, weight=BOLD).move_to([PX, -3.1, 0])
        self.play(FadeIn(l2, shift=UP * 0.15), Indicate(VGroup(*tr.bottles), color=BLUE, scale_factor=1.3), run_time=1.4)
        self.play(Indicate(tr.pond, color=BLUE, scale_factor=1.08), run_time=1.0)
        self.at("here adding wells cannot cross")
        pv = ValueTracker(pct_of(2, 5))
        nv = ValueTracker(5)
        pv.add_updater(lambda t: t.set_value(pct_of(2, nv.get_value())))
        self.add(pv)
        bar = meter(pv, K, lambda v: f"{v:.1f}%", BAR_TITLE, TEAL)
        sl = stop_line()
        self.play(FadeOut(l1), FadeOut(l2), FadeIn(bar), FadeIn(sl), FadeIn(computed_tag()), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(tr.extra(r, r + 1), shift=DOWN * 0.1) for r in range(1, 10)], lag_ratio=0.2), nv.animate.set_value(50), run_time=1.3)
        gy = BASE + pct_of(2, 50) * K
        ghost = VGroup(DashedLine([3.75, gy, 0], [5.3, gy, 0], color=TEXT, stroke_width=4), M("7.2%", 24, TEXT).move_to([3.2, gy + 0.3, 0]))
        self.play(FadeIn(ghost), run_time=0.3)
        self.at("a third water sample does")
        pv.clear_updaters()
        self.play(FadeOut(tr.extra()), run_time=0.3)
        tr3 = morph_to_three(self, tr, run=0.8)
        self.play(Create(tr3.l_pb[2]), GrowFromPoint(tr3.bottles[2], [PX, PONDY - 0.4, 0]),
                  *[Create(tr3.l_bt[j]) for j in (4, 5)], *[FadeIn(tr3.tubes[j]) for j in (4, 5)],
                  *[Create(tr3.l_tw[j]) for j in (4, 5)], *[FadeIn(s) for j in (4, 5) for s in tr3.rows[j][0]],
                  pv.animate.set_value(pct_of(3, 5)), run_time=1.2)
        self.play(Indicate(tr3.bottles[2], color=BLUE, scale_factor=1.4), Indicate(sl[0], color=RED, scale_factor=1.2), run_time=0.8)
        self.finish()


class S13End(EndCard):
    LINE = "Only new water is a new try at the scoop."
