"""Macromolecules, chapter 2: Shape Decides the Job (Biochemistrypedia high school Biology film)

Same COLOUR MAP as chapter 1: simple sugar = GOLD hexagon; amino acid = BLUE bead; nucleotide = GREEN bead
with tab; fatty acid = ORANGE wavy tail; glycerol = ORANGE comb; water = light-blue bent V; links = bars
(grey in chapter 1; here recoloured by kind: starch link teal, branch link yellow, cellulose link purple).
Counters (top right) track links and waters. Blocks are labelled cartoons, never structures.
Added here: digestive enzyme = BLUE folded blob with a notch-shaped pocket.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

AMINO = "#4C7DFF"
WATER = "#A8E6FF"
ORANGE = "#F29E4C"
STARCH_L = TEAL
BRANCH_L = YELLOW
CELL_L = "#C77DFF"
WALL_G = "#5FBF6A"
PANEL = interpolate_color(ManimColor(BG), ManimColor(GREY), 0.17).to_hex()
PANEL_S14 = interpolate_color(ManimColor(BG), ManimColor(GREY), 0.08).to_hex()
T10 = 12.2   # about how long s10 runs, so the tumbling lipids carry on smoothly through the pause and reveal


# ------------------------------------------------------------------ helpers (as in chapter 1)
def wiggle(m, amp=0.06, w=1.6, seed=0.0):
    m._wo = np.zeros(3)
    m._wt = seed * 3.1

    def u(mm, dt):
        mm._wt += dt
        off = np.array([0.6 * amp * np.cos(w * mm._wt * 0.8 + seed), amp * np.sin(w * mm._wt + seed * 2), 0])
        mm.shift(off - mm._wo)
        mm._wo = off
    m.add_updater(u)
    return m


def wig_all(mobs, amp=0.06):
    for i, m in enumerate(mobs):
        wiggle(m, amp, 1.4 + 0.15 * (i % 4), i * 0.9)


def sugar(r=0.45, label=None):
    back = RegularPolygon(6, radius=r, start_angle=0, stroke_width=0, fill_color=BG, fill_opacity=1)
    front = RegularPolygon(6, radius=r, start_angle=0, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.4)
    g = VGroup(back, front)
    if label:
        g.add(T(label, 28, TEXT).move_to(front))
    g.set_z_index(2)
    return g


def amino(r=0.4):
    back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1)
    front = Circle(radius=r, stroke_color=AMINO, stroke_width=3, fill_color=AMINO, fill_opacity=0.4)
    g = VGroup(back, front)
    g.set_z_index(2)
    return g


def nuc(r=0.4):
    back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1)
    front = Circle(radius=r, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4)
    tab = Rectangle(width=0.22, height=0.26, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.7)
    tab.move_to(front.get_top() + UP * 0.1)
    g = VGroup(back, front, tab)
    g.set_z_index(2)
    return g


def vee(dashed=False, s=1.4):
    v = VMobject()
    v.set_points_as_corners([[-0.2, 0.22, 0], [0, 0, 0], [0.2, 0.22, 0]])
    v.set_stroke(WATER, 6)
    if dashed:
        g = VGroup(DashedVMobject(v, num_dashes=6), Dot(radius=0.08, color=WATER).set_opacity(0.7))
    else:
        g = VGroup(v, Dot(radius=0.09, color=WATER))
    g.scale(s)
    g.set_z_index(5)
    return g


def mk_bar(a, b, w=9, col=GREY):
    l = Line(a.get_center(), b.get_center(), color=col, stroke_width=w)
    l.add_updater(lambda m, a=a, b=b: m.put_start_and_end_on(a.get_center(), b.get_center()))
    l.set_z_index(1)
    return l


class Chain:
    def __init__(self, blocks, w=9, col=GREY):
        self.blocks = blocks
        self.bars = [mk_bar(a, b, w, col) for a, b in zip(blocks, blocks[1:])]
        self.group = VGroup(*self.bars, *self.blocks)

    def build(self, lag=0.3):
        an = []
        for i, b in enumerate(self.blocks):
            parts = [FadeIn(b, scale=0.6)]
            if i > 0:
                parts.insert(0, FadeIn(self.bars[i - 1]))
            an.append(AnimationGroup(*parts))
        return LaggedStart(*an, lag_ratio=lag)

    def mid(self, j):
        return (self.blocks[j].get_center() + self.blocks[j + 1].get_center()) / 2


class Counters:
    def __init__(self, a=5, b=0, label2="waters"):
        self.a, self.b, self.l2 = ValueTracker(a), ValueTracker(b), label2

        def row(tr, lab, y):
            def mk():
                v = tr.get_value()
                g = VGroup(T(lab(), 26, TEXT), M(str(int(round(v))), 30, WATER)).arrange(RIGHT, buff=0.3)
                g.move_to([6.7 - g.width / 2, y, 0])
                return g
            return always_redraw(mk)
        self.rows = VGroup(row(self.a, lambda: "links", 3.45), row(self.b, lambda: self.l2, 2.9))
        self.box_pt = np.array([5.0, 3.2, 0])

    def pulse_rect(self):
        return Rectangle(width=3.6, height=1.2, stroke_color=YELLOW, stroke_width=4).move_to(self.box_pt)


def row_chain(n, x0, y, dx, r=0.45, col=GREY, w=9):
    return Chain([sugar(r).move_to([x0 + dx * i, y, 0]) for i in range(n)], w=w, col=col)


COIL_C = (-3.4, 0.1)
COIL_S = 1.15


def coil_pos(i, c=None, s=None):
    c = COIL_C if c is None else c
    s = COIL_S if s is None else s
    ang = np.radians(120 - 55 * i)
    rad = (2.3 - 0.2 * i) * s
    return np.array([c[0] + rad * np.cos(ang), c[1] + rad * np.sin(ang), 0])


def battery(cx, cy, tr):
    body = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.8, stroke_color=GREEN, stroke_width=4).move_to([cx, cy, 0])
    tip = Rectangle(width=0.15, height=0.3, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([cx + 0.82, cy, 0])

    def mk():
        v = max(0.02, tr.get_value())
        return Rectangle(width=1.34 * v, height=0.64, stroke_width=0, fill_color=GREEN, fill_opacity=0.8).move_to(
            [cx - 0.67 + 0.67 * v, cy, 0])
    return VGroup(body, tip), always_redraw(mk)


# ---- the digestive enzyme: a BLUE folded blob with a notch-shaped pocket
class Enz:
    def __init__(self, pos, ang=0.0, r=0.8, nd=PI, label=None, bg=None):
        bg = bg or PANEL
        self.r, self.nd, self.pos, self.ang = r, nd, np.array(pos, dtype=float), 0.0
        f = lambda th: r * (1 + 0.07 * np.sin(3 * th) + 0.05 * np.sin(5 * th + 1.0))
        pts = lambda: ParametricFunction(lambda th: np.array([f(th) * np.cos(th), f(th) * np.sin(th), 0]), t_range=[0, TAU, 0.05])
        back = pts().set_fill(bg, 1).set_stroke(width=0)
        body = pts().set_fill(AMINO, 0.42).set_stroke(AMINO, 4)
        fold = ParametricFunction(lambda t: np.array([0.45 * r * np.cos(t) * (1 + 0.1 * np.sin(4 * t)),
                                                      0.45 * r * np.sin(t) * (1 + 0.1 * np.sin(4 * t)), 0]),
                                  t_range=[0.6, 5.4, 0.05]).set_fill(opacity=0).set_stroke(AMINO, 3, opacity=0.7)
        nr = 0.3 * r
        c = np.array([0.95 * r * np.cos(nd), 0.95 * r * np.sin(nd), 0])
        disc = Circle(radius=nr, stroke_width=0, fill_color=bg, fill_opacity=1).move_to(c)
        edge = Arc(radius=nr, start_angle=nd + PI - 1.3, angle=2.6, stroke_color=YELLOW, stroke_width=4).move_arc_center_to(c)
        self.mob = VGroup(back, body, fold, disc, edge)
        self.mob.set_z_index(4)
        self.mob.move_to(self.pos)
        self.base_c = self.mob.get_center() - self.pos
        self.mob.shift(-self.base_c)
        self.rot(ang)
        self.label = label

    def rot(self, ang):
        self.mob.rotate(ang - self.ang, about_point=self.pos)
        self.ang = ang

    def set(self, pos, ang):
        self.mob.shift(np.array(pos) - self.pos)
        self.pos = np.array(pos, dtype=float)
        self.rot(ang)

    def notch(self):
        a = self.nd + self.ang
        return self.pos + 0.95 * self.r * np.array([np.cos(a), np.sin(a), 0])

    def glide(self, pos, ang, rt=1.5):
        p0, a0 = self.pos.copy(), self.ang
        p1, a1 = np.array(pos, dtype=float), ang
        return UpdateFromAlphaFunc(self.mob, lambda m, a: self.set(p0 + (p1 - p0) * smooth(a), a0 + (a1 - a0) * smooth(a)), run_time=rt)

    def dock(self, link_mid, outward):
        """position and angle that put the notch on a link at link_mid, enzyme sitting 'outward' (unit vector)"""
        ang = np.arctan2(-outward[1], -outward[0]) - self.nd
        return link_mid + outward * 0.95 * self.r, ang


def unit(v):
    return v / np.linalg.norm(v)


# ---- phospholipid cartoon (head up at angle 0), centred on its own middle
def lipid(s=1.0):
    head = Circle(radius=0.27 * s, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.55)
    tab = Rectangle(width=0.15 * s, height=0.1 * s, stroke_width=0, fill_color="#5A3A12", fill_opacity=1).move_to(head.get_top() + DOWN * 0.04 * s)
    tails = VGroup(*[ParametricFunction(lambda t, x=x: np.array([x + 0.05 * s * np.sin(9 * t), -0.25 * s - 0.8 * s * t, 0]),
                                        t_range=[0, 1, 0.02], color=ORANGE, stroke_width=4) for x in (-0.1 * s, 0.1 * s)])
    head.set_z_index(3)
    tab.set_z_index(4)
    g = VGroup(tails, head, tab)
    g.move_to(ORIGIN)
    return g


LIP_S = 0.85
N_LIP = 28


def tumble_base():
    rng = np.random.RandomState(7)
    pts = []
    for r_, y in enumerate([1.9, 0.7, -0.5, -1.7]):
        for c_ in range(7):
            pts.append((-5.0 + 1.67 * c_ + rng.uniform(-0.25, 0.25), y + rng.uniform(-0.2, 0.2)))
    idx = rng.permutation(len(pts))[:N_LIP]
    return [pts[i] for i in idx], rng.uniform(0, TAU, N_LIP), rng.uniform(0, TAU, N_LIP), rng.uniform(0, TAU, N_LIP), rng.choice([-1, 1], N_LIP) * rng.uniform(0.5, 1.0, N_LIP)


BASE, PH1, PH2, A0, WR = tumble_base()
WAT_C = np.array([0.0, -0.2, 0.0])


def tumble_state(i, t, drop=True):
    x, y = BASE[i]
    p = np.array([x + 0.4 * np.sin(0.8 * t + PH1[i]), y + 0.3 * np.cos(0.6 * t + PH2[i]), 0.0])
    if drop:
        k = np.clip((t - 0.9 - 0.06 * i) / 1.5, 0, 1)
        p[1] += 6.0 * (1 - k) ** 2
    return p, A0[i] + WR[i] * t


def make_lipids(t0=0.0, drop=True):
    lips = []
    for i in range(N_LIP):
        m = lipid(LIP_S)
        m._t = t0
        p, a = tumble_state(i, t0, drop)
        m.rotate(a)
        m.shift(p)
        m._p, m._a = p, a

        def u(mm, dt, i=i):
            mm._t += dt
            p2, a2 = tumble_state(i, mm._t, drop)
            mm.rotate(a2 - mm._a, about_point=mm._p)
            mm.shift(p2 - mm._p)
            mm._p, mm._a = p2, a2
        m.add_updater(u)
        lips.append(m)
    return lips


def water_box():
    return Rectangle(width=12.6, height=6.0, stroke_color=WATER, stroke_width=3, fill_color=WATER, fill_opacity=0.10).move_to(WAT_C)


def stage(col=GREY, op=0.17):
    """a faint ground panel for the world of a scene (like chapter 1's gut and cell), so the frame is never a thin line on black"""
    r = RoundedRectangle(corner_radius=0.3, width=13.4, height=7.6, stroke_width=0, fill_color=col, fill_opacity=op).move_to([0, 0, 0])
    r.set_z_index(-5)
    return r


def predict_card():
    return chip("Heads point which way?", YELLOW, size=36).move_to([0, 3.3, 0])


def rope_mob(w=3.0, h=0.5, rot=0.0, n=4):
    """a cellulose fibre: a gold-edged rope with a few block-sized segments"""
    rr = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.35)
    segs = VGroup(*[Line([-w / 2 + h / 2 + k * (w - h) / (n - 1), -h / 2 + 0.05, 0], [-w / 2 + h / 2 + k * (w - h) / (n - 1), h / 2 - 0.05, 0],
                         color=GOLD, stroke_width=2).set_opacity(0.6) for k in range(n)])
    return VGroup(rr, segs).rotate(rot)


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "What Am I Made Of?"
    TITLE = "Shape Decides the Job"


class S01Hook(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        xs, xc = -3.9, 3.9
        ys = [1.3 - 1.0 * i for i in range(5)]
        st = Chain([sugar(0.45).move_to([xs, y, 0]) for y in ys], w=8)
        ce = Chain([sugar(0.45).move_to([xc, y, 0]) for y in ys], w=8)
        wig_all(st.blocks + ce.blocks, 0.05)
        sl = T("starch", 32, GOLD, weight=BOLD).move_to([xs, -3.55, 0])
        cl = T("cellulose", 32, GOLD, weight=BOLD).move_to([xc, -3.55, 0])
        glu = sugar(0.6).move_to([0, 2.3, 0])
        gl = T("glucose", 32, TEXT, weight=BOLD).next_to(glu, UP, buff=0.12)
        a1 = Arrow([-0.8, 2.2, 0], [-3.4, 1.8, 0], color=GOLD, buff=0, stroke_width=5)
        a2 = Arrow([0.8, 2.2, 0], [3.4, 1.8, 0], color=GOLD, buff=0, stroke_width=5)
        e1 = M("=", 44, GOLD).move_to([-2.1, 2.65, 0])
        e2 = M("=", 44, GOLD).move_to([2.1, 2.65, 0])
        card = VGroup(T("Why one", 36, YELLOW, weight=BOLD), T("and not the other?", 36, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.2).move_to([0, -0.5, 0])
        wiggle(glu, 0.05)
        self.wait(0.2)
        self.play(st.build(0.35), ce.build(0.35), FadeIn(sl), FadeIn(cl), run_time=2.4)
        self.at("glucose")
        self.play(FadeIn(glu, scale=0.5), FadeIn(gl), run_time=0.8)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(e1), FadeIn(e2), run_time=1.0)
        self.at("So why can")
        self.play(FadeIn(card, scale=0.8), run_time=0.9)
        self.at("take starch apart")
        self.play(Indicate(st.group, color=TEAL, scale_factor=1.05), run_time=1.3)
        self.at("but not cellulose")
        self.play(Indicate(ce.group, color=RED, scale_factor=1.05), run_time=1.3)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        dx = 1.6
        st = row_chain(6, -3.6, 1.3, dx, 0.6, GREY, 12)
        wig_all(st.blocks, 0.05)
        cn = Counters(5, 0)
        self.add(cn.rows)
        self.play(st.build(0.3), run_time=1.6)
        self.at("adding water")
        w = vee(False, 1.6).move_to(st.mid(2) + UP * 1.6)
        self.play(FadeIn(w, scale=0.6), run_time=0.4)
        self.play(w.animate.move_to(st.mid(2) + UP * 0.1), run_time=0.7)
        self.play(FadeOut(st.bars[2]), FadeOut(w, scale=0.3), st.blocks[3].animate.shift(RIGHT * 0.4),
                  st.blocks[4].animate.shift(RIGHT * 0.4), st.blocks[5].animate.shift(RIGHT * 0.4),
                  cn.a.animate.set_value(4), cn.b.animate.set_value(1), run_time=0.8)
        self.at("one water per link")
        self.play(ShowPassingFlash(cn.pulse_rect().set_stroke(YELLOW, 6), time_width=1.0), run_time=1.4)
        self.at("Here are the same")
        cel = row_chain(6, -3.6, -0.5, dx, 0.6, GREY, 12)
        wig_all(cel.blocks, 0.05)
        sl = T("starch", 32, GOLD, weight=BOLD).move_to([-5.7, 1.3, 0])
        cl = T("cellulose", 32, GOLD, weight=BOLD).move_to([-5.7, -0.5, 0])
        self.play(*[b.animate.shift(LEFT * 0.4) for b in st.blocks[3:]], FadeIn(st.bars[2]), FadeOut(cn.rows),
                  cel.build(0.25), FadeIn(sl), FadeIn(cl), run_time=2.2)
        self.at("But their links")
        legend_rows = [(STARCH_L, "starch link"), (BRANCH_L, "starch branch link"), (CELL_L, "cellulose link (schematic)")]
        recol = [b.animate.set_stroke(STARCH_L, 12) for b in st.bars]
        recol[2] = st.bars[2].animate.set_stroke(BRANCH_L, 12)
        recol += [b.animate.set_stroke(CELL_L, 12) for b in cel.bars]
        self.play(*recol, run_time=1.2)
        leg = VGroup()
        for k, (c, txt) in enumerate(legend_rows):
            y = -1.8 - 0.7 * k
            samp = Line([-5.9, y, 0], [-5.1, y, 0], color=c, stroke_width=12)
            lab = T(txt, 30, TEXT).next_to(samp, RIGHT, buff=0.25)
            leg.add(VGroup(samp, lab))
        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.2) for g in leg], lag_ratio=0.5), run_time=1.5)
        self.finish()


class S03Starch(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        st = Chain([sugar(0.42).move_to([-6.0 + 0.95 * i, 0.1, 0]) for i in range(7)], w=8, col=STARCH_L)
        wig_all(st.blocks, 0.05)
        self.wait(0.2)
        self.play(st.build(0.3), run_time=1.6)
        self.at("let the chain coil")
        self.play(*[b.animate.move_to(coil_pos(i)) for i, b in enumerate(st.blocks)], run_time=2.2)
        self.at("some starch branches")
        main = Chain([sugar(0.42).move_to([1.2 + 1.2 * i, 0.9, 0]) for i in range(5)], w=8, col=STARCH_L)
        wig_all(main.blocks, 0.05)
        self.play(main.build(0.2), run_time=1.0)
        br = []
        for k in (1, 3):
            x = main.blocks[k].get_center()[0]
            b1 = sugar(0.42).move_to(main.blocks[k])
            b2 = sugar(0.42).move_to(main.blocks[k])
            bar1 = mk_bar(main.blocks[k], b1, 8, BRANCH_L)
            bar2 = mk_bar(b1, b2, 8, STARCH_L)
            self.add(bar1, bar2, b1, b2)
            br += [(b1, [x, -0.3, 0]), (b2, [x, -1.5, 0])]
        self.play(*[b.animate.move_to(p) for b, p in br], run_time=1.4)
        lab = T("starch: coils, and some branches (schematic)", 30, TEAL, weight=BOLD).move_to([0, -3.2, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.8)
        self.at("store of sugar")
        tr = ValueTracker(0.0)
        bat, fill = battery(-0.6, 2.9, tr)
        bl = T("energy store", 30, GREEN, weight=BOLD).next_to(bat, RIGHT, buff=0.35)
        self.add(fill)
        self.play(FadeIn(bat), FadeIn(bl), tr.animate.set_value(1.0), run_time=2.0)
        self.at("take it apart for energy")
        self.play(Indicate(bat, color=GREEN, scale_factor=1.12), Indicate(st.group, color=TEAL, scale_factor=1.04), run_time=1.5)
        self.finish()


class S04Enzyme(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        st = Chain([sugar(0.5).move_to(coil_pos(i)) for i in range(7)], w=10, col=STARCH_L)
        wig_all(st.blocks, 0.04)
        cn = Counters(6, 0)
        self.add(cn.rows)
        self.play(st.build(0.15), run_time=1.0)
        en = Enz([2.6, 0.2, 0], 0.0, 0.8, PI)
        self.at("digestive enzyme")
        el = T("digestive enzyme", 30, AMINO, weight=BOLD).move_to([3.1, 1.6, 0])
        self.play(FadeIn(en.mob, scale=0.6), FadeIn(el), run_time=0.9)
        self.at("folded into a pocket")
        pl = T("pocket", 30, YELLOW, weight=BOLD).move_to([1.2, -0.9, 0])
        self.play(Indicate(en.mob, color=YELLOW, scale_factor=1.1), FadeIn(pl), run_time=1.4)
        c = np.array([COIL_C[0], COIL_C[1], 0])
        m1 = (coil_pos(2) + coil_pos(3)) / 2
        p1, a1 = en.dock(m1, unit(m1 - c))
        self.at("Starches links fit")
        self.play(FadeOut(el), FadeOut(pl), en.glide(p1, a1, 2.0), run_time=2.0)
        self.at("adds water")
        w = vee(False, 1.5).move_to(m1 + unit(m1 - c) * 1.7)
        wl = T("H2O", 28, WATER).next_to(w, UP, buff=0.12)
        self.play(FadeIn(w, scale=0.6), FadeIn(wl), run_time=0.5)
        self.play(w.animate.move_to(m1), FadeOut(wl), run_time=0.8)
        self.at("chain breaks")
        A = st.blocks[0:3]
        tgtA = [np.array([-0.2 + 0.85 * k, -2.45, 0]) for k in range(3)]
        m2 = (coil_pos(4) + coil_pos(5)) / 2
        p2, a2 = en.dock(m2, unit(m2 - c))
        self.play(FadeOut(st.bars[2]), FadeOut(w, scale=0.3), *[b.animate.move_to(t) for b, t in zip(A, tgtA)],
                  cn.a.animate.set_value(5), cn.b.animate.set_value(1), en.glide([-1.9, -2.0, 0], (a1 + a2) / 2, 1.2), run_time=1.2)
        self.at("smaller sugars")
        self.play(en.glide(p2, a2, 0.7), run_time=0.7)
        w2 = vee(False, 1.5).move_to(m2 + unit(m2 - c) * 1.5)
        self.play(FadeIn(w2, scale=0.6), w2.animate.move_to(m2), run_time=0.5)
        B = st.blocks[3:5]
        C = st.blocks[5:7]
        sl = T("smaller sugars", 30, GOLD, weight=BOLD).move_to([3.0, -1.2, 0])
        self.play(FadeOut(st.bars[4]), FadeOut(w2, scale=0.3),
                  *[b.animate.move_to(np.array([2.7 + 0.85 * k, -2.45, 0])) for k, b in enumerate(B)],
                  *[b.animate.move_to(np.array([4.9 + 0.85 * k, -2.45, 0])) for k, b in enumerate(C)],
                  cn.a.animate.set_value(4), cn.b.animate.set_value(2), FadeIn(sl), run_time=1.0)
        self.at("Other enzymes")
        en2 = Enz([-3.3, 1.0, 0], 0.0, 0.5, PI)
        e2l = T("other enzymes", 28, AMINO, weight=BOLD).move_to([-3.3, 2.0, 0])
        self.play(FadeOut(en.mob), FadeOut(sl), FadeIn(en2.mob, scale=0.6), FadeIn(e2l), run_time=0.6)
        links = [(st.bars[0], st.blocks[0], st.blocks[1]), (st.bars[1], st.blocks[1], st.blocks[2]),
                 (st.bars[3], st.blocks[3], st.blocks[4]), (st.bars[5], st.blocks[5], st.blocks[6])]
        done = 0
        for bar, ba, bb in links:
            mid = (ba.get_center() + bb.get_center()) / 2
            pp, aa = en2.dock(mid, np.array([0.0, 1.0, 0.0]))
            self.play(en2.glide(pp, aa, 0.35), run_time=0.35)
            done += 1
            self.play(FadeOut(bar), ba.animate.shift(LEFT * 0.25), bb.animate.shift(RIGHT * 0.25),
                      cn.a.animate.set_value(4 - done), cn.b.animate.set_value(2 + done), run_time=0.3)
        self.at("glucose")
        xs = [-5.4 + 1.8 * k for k in range(7)]
        gl = T("glucose", 34, GOLD, weight=BOLD).move_to([0, -3.4, 0])
        self.play(*[b.animate.move_to([xs[i], -2.45, 0]) for i, b in enumerate(st.blocks)], FadeOut(en2.mob), FadeOut(e2l),
                  FadeIn(gl), run_time=1.3)
        self.finish()


class S05Cellulose(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        rows = []
        ys = [1.65, 0.55, -0.55, -1.65]
        for k, y in enumerate(ys):
            rows.append(Chain([sugar(0.45).move_to([-3.25 + 1.3 * i, y, 0]) for i in range(6)], w=9, col=CELL_L))
        wig_all([b for ch in rows for b in ch.blocks], 0.03)
        for k, ch in enumerate(rows):
            ch.group.shift((LEFT if k % 2 == 0 else RIGHT) * 11.2)
        self.add(*[ch.group for ch in rows])
        self.wait(0.2)
        self.play(rows[0].group.animate.shift(RIGHT * 11.2), run_time=1.1)
        self.at("linked the other way")
        self.play(Indicate(rows[0].group, color=CELL_L, scale_factor=1.04), run_time=1.0)
        self.at("lie straight")
        self.play(rows[1].group.animate.shift(LEFT * 11.2), run_time=1.1)
        self.at("stack side by side")
        self.play(rows[2].group.animate.shift(RIGHT * 11.2), run_time=1.1)
        self.play(rows[3].group.animate.shift(LEFT * 11.2), run_time=1.1)
        self.at("form strong fibers")
        rope = RoundedRectangle(corner_radius=0.5, width=8.2, height=4.9, stroke_color=GOLD, stroke_width=5,
                                fill_color=GOLD, fill_opacity=0.10).move_to([0, 0, 0])
        fl = T("fiber", 40, GOLD, weight=BOLD).move_to([0, 3.2, 0])
        self.play(Create(rope), FadeIn(fl), run_time=1.4)
        self.at("stiffen plant cell walls")
        allc = VGroup(*[ch.group for ch in rows], rope)
        wall = Rectangle(width=11.6, height=6.0, stroke_color=WALL_G, stroke_width=6, fill_color=WALL_G, fill_opacity=0.12).move_to([0, -0.1, 0])
        wl = T("plant cell wall", 36, WALL_G, weight=BOLD).move_to([0, 3.3, 0])
        ropes = VGroup(*[rope_mob(3.6, 0.55, a).move_to(p) for a, p in
                         [(0.5, [-3.6, 1.2, 0]), (-0.6, [3.5, 1.3, 0]), (-0.2, [-3.7, -1.5, 0]), (0.7, [3.6, -1.4, 0])]])
        self.play(FadeOut(fl), allc.animate.scale(0.38).move_to([0, -0.2, 0]), FadeIn(wall), FadeIn(wl), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(r, scale=0.5) for r in ropes], lag_ratio=0.25), run_time=1.4)
        self.finish()


class S06Nofit(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        ch = row_chain(6, -4.1, -0.9, 1.65, 0.6, CELL_L, 12)
        wig_all(ch.blocks, 0.04)
        cn = Counters(5, 0)
        self.add(ch.group, cn.rows)
        en = Enz([1.5, 2.2, 0], 0.0, 1.0, PI)
        el = T("same enzyme", 30, AMINO, weight=BOLD).move_to([1.5, 3.4, 0])
        self.add(en.mob, el)
        self.at("Now the same enzyme")
        self.play(en.glide([-0.2, 1.0, 0], 0.0, 1.8), run_time=1.8)
        self.at("pocket does not fit")
        x = T("X", 80, RED, weight=BOLD).move_to([-0.3, -0.1, 0]).set_z_index(6)
        for k in range(2):
            self.play(en.glide([-0.2, -0.35, 0], 0.0, 0.7), run_time=0.7)
            self.play(en.glide([-0.2, 0.55, 0], 0.0, 0.6), run_time=0.6)
        self.play(FadeIn(x, scale=2.0), run_time=0.3)
        self.at("cannot break them")
        nb = T("no water enters: nothing breaks", 30, WATER, weight=BOLD).move_to([0, -2.6, 0])
        self.play(FadeIn(nb, shift=UP * 0.2), Indicate(ch.group, color=CELL_L, scale_factor=1.03), run_time=1.4)
        self.play(en.glide([-0.2, -0.35, 0], 0.0, 0.7), run_time=0.7)
        self.play(en.glide([-0.2, 0.55, 0], 0.0, 0.6), run_time=0.6)
        self.at("cellulose is fiber")
        fl = T("fiber", 44, GOLD, weight=BOLD).move_to([0, -3.35, 0])
        self.play(FadeOut(x), FadeOut(nb), en.mob.animate.shift(UP * 1.0 + RIGHT * 2.5).set_opacity(0.25), FadeIn(fl, scale=0.8), run_time=1.2)
        self.finish()


class S07Rule(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        div = Line([0, 3.4, 0], [0, -2.4, 0], color=GREY, stroke_width=3)
        blocks = [sugar(0.38).move_to(coil_pos(i, (-3.4, 0.55), 0.85)) for i in range(7)]
        st = Chain(blocks, w=7, col=STARCH_L)
        wig_all(blocks, 0.04)
        tr = ValueTracker(0.0)
        bat, fill = battery(-3.4, 3.2, tr)
        wall = Rectangle(width=5.8, height=4.6, stroke_color=WALL_G, stroke_width=5, fill_color=WALL_G, fill_opacity=0.12).move_to([3.5, 0.5, 0])
        ropes = VGroup(*[rope_mob(2.8, 0.5, a).move_to(p) for a, p in
                         [(0.3, [3.4, 1.8, 0]), (-0.3, [3.5, 0.7, 0]), (0.3, [3.4, -0.4, 0]), (-0.3, [3.5, -1.3, 0])]])
        self.add(div)
        self.play(st.build(0.15), FadeIn(wall), FadeIn(ropes), run_time=1.4)
        self.at("two shapes")
        self.play(Indicate(st.group, color=TEAL, scale_factor=1.05), Indicate(ropes, color=GOLD, scale_factor=1.05), run_time=1.4)
        self.at("stores energy")
        self.add(fill)
        self.play(FadeIn(bat), tr.animate.set_value(1.0), run_time=1.6)
        self.at("stiffens plant walls")
        self.play(Indicate(wall, color=WALL_G, scale_factor=1.03), run_time=1.4)
        parts = [("blocks", GOLD, "The blocks"), ("+ links", TEAL, "links between them"), ("+ shape", AMINO, "the shape they take"),
                 ("= job", YELLOW, "decide the job")]
        pos = [-5.0, -2.4, 0.4, 3.3]
        for (txt, col, ph), x in zip(parts, pos):
            t = T(txt, 40, col, weight=BOLD)
            self.at(ph)
            t.move_to([x + t.width / 2, -3.3, 0])
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S08Protein(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        en = Enz([-3.3, 0.5, 0], 0.0, 1.5, 0.0)
        wiggle(en.mob, 0.05)
        el = T("enzyme", 36, AMINO, weight=BOLD).move_to([-3.3, 2.7, 0])
        self.play(FadeIn(en.mob, scale=0.6), FadeIn(el), run_time=1.0)
        self.at("chain of amino acids")
        beads = VGroup(*[amino(0.34).move_to([-5.6 + 0.9 * i, 0.5, 0]) for i in range(9)])
        bars = VGroup(*[Line(beads[i].get_center(), beads[i + 1].get_center(), color=GREY, stroke_width=8).set_z_index(1) for i in range(8)])
        cl = T("chain of amino acids", 32, AMINO, weight=BOLD).move_to([-1.2, 2.0, 0])
        unrolled = VGroup(bars, beads)
        self.play(FadeOut(el), FadeOut(en.mob), FadeIn(unrolled, scale=0.6), FadeIn(cl), run_time=1.6)
        self.at("folded into a shape")
        en2 = Enz([-3.3, 0.5, 0], 0.0, 1.5, 0.0)
        self.play(FadeOut(unrolled, scale=0.4), FadeIn(en2.mob, scale=1.6), FadeOut(cl), run_time=1.6)
        wiggle(en2.mob, 0.05)
        self.at("makes the pocket")
        pk = T("pocket", 32, YELLOW, weight=BOLD).move_to([0.1, 1.5, 0])
        self.play(Indicate(en2.mob, color=YELLOW, scale_factor=1.08), FadeIn(pk), run_time=1.4)
        notch = en2.notch()
        self.at("the pocket fits")
        self.play(FadeOut(pk), run_time=0.2)
        top = sugar(0.36).move_to([notch[0] + 4.5, notch[1] + 0.6, 0])
        bot = sugar(0.36).move_to([notch[0] + 4.5, notch[1] - 0.6, 0])
        lbar = mk_bar(top, bot, 9, STARCH_L)
        self.add(lbar)
        self.add(top, bot)
        self.play(top.animate.move_to([notch[0] + 0.35, notch[1] + 0.6, 0]), bot.animate.move_to([notch[0] + 0.35, notch[1] - 0.6, 0]), run_time=0.8)
        tick = T("fits", 32, GREEN, weight=BOLD).move_to([notch[0] + 1.6, notch[1], 0])
        self.play(FadeIn(tick, scale=0.6), Indicate(en2.mob, color=GREEN, scale_factor=1.04), run_time=0.5)
        self.at("one kind of molecule")
        gb = nuc(0.4).move_to([notch[0] + 5.0, notch[1] + 2.0, 0])
        ot = ParametricFunction(lambda t: np.array([notch[0] + 4.5 + 1.4 * t, notch[1] - 2.0 + 0.12 * np.sin(8 * t), 0]),
                                t_range=[0, 1, 0.02], color=ORANGE, stroke_width=6)
        self.play(FadeOut(tick), gb.animate.move_to([notch[0] + 1.0, notch[1] + 1.4, 0]), FadeIn(ot), run_time=0.9)
        self.play(gb.animate.shift(DOWN * 0.3), ot.animate.shift(LEFT * 1.6 + UP * 0.6), run_time=0.8)
        self.play(gb.animate.shift(RIGHT * 1.3 + UP * 0.4), ot.animate.shift(RIGHT * 1.6 + DOWN * 0.2), run_time=0.7)
        self.finish()


class S09Lipid(SpokenScene):
    def construct(self):
        water = Rectangle(width=12.6, height=1.5, stroke_color=WATER, stroke_width=3, fill_color=WATER, fill_opacity=0.14).move_to([0, -3.0, 0])
        ph = ValueTracker(0.0)
        wave = always_redraw(lambda: ParametricFunction(lambda x: np.array([x, -2.25 + 0.1 * np.sin(1.8 * x + 2.5 * ph.get_value()), 0]),
                                                        t_range=[-6.3, 6.3, 0.1], color=WATER, stroke_width=5))
        self.add(water, wave)
        self.at("Lipids follow the rule")
        rule = chip("blocks + links + shape = job", YELLOW, size=30).move_to([0, 3.2, 0])
        self.play(FadeIn(rule, shift=DOWN * 0.2), ph.animate.set_value(6.0), run_time=1.8, rate_func=linear)
        self.at("a phospholipid")
        lp = lipid(2.8).move_to([-1.6, 0.0, 0])
        self.play(FadeOut(rule), FadeIn(lp, scale=0.6), ph.animate.set_value(8.0), run_time=1.4, rate_func=linear)
        bob = ValueTracker(0.0)
        lp._by = 0.0

        def bobber(m, dt):
            bob.increment_value(dt)
            ny = 0.12 * np.sin(2.0 * bob.get_value())
            m.shift(UP * (ny - m._by))
            m._by = ny
        lp.add_updater(bobber)
        head_c = lp[1].get_center()
        tails_c = lp[0].get_center()
        self.at("attracted to water")
        hl = T("head: attracted to water", 32, ORANGE, weight=BOLD).move_to([4.2, head_c[1] + 0.4, 0])
        ha = Arrow([1.3, head_c[1] + 0.4, 0], [head_c[0] + 0.95, head_c[1] + 0.1, 0], color=ORANGE, buff=0.05, stroke_width=4)
        self.play(FadeIn(hl, shift=LEFT * 0.2), GrowArrow(ha), Indicate(lp[1], color=ORANGE, scale_factor=1.25), run_time=1.6)
        self.at("two tails")
        tl = T("tails: avoid water", 32, ORANGE, weight=BOLD).move_to([4.2, tails_c[1] - 0.2, 0])
        ta = Arrow([1.3, tails_c[1] - 0.2, 0], [tails_c[0] + 0.7, tails_c[1] - 0.2, 0], color=ORANGE, buff=0.05, stroke_width=4)
        self.play(FadeIn(tl, shift=LEFT * 0.2), GrowArrow(ta), Indicate(lp[0], color=ORANGE, scale_factor=1.15), ph.animate.set_value(12.0), run_time=1.8, rate_func=linear)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        box = water_box()
        lips = make_lipids(0.0, True)
        self.add(box)
        card = predict_card()
        self.add(*lips)
        self.at("all tumbling")
        self.wait(0.5)
        self.at("Each head likes water")
        self.play(*[Indicate(l[1], color=ORANGE, scale_factor=1.5) for l in lips[::2]], run_time=1.3)
        self.at("each pair of tails")
        self.play(*[Indicate(l[0], color=ORANGE, scale_factor=1.3) for l in lips[1::2]], run_time=1.3)
        self.at("Which way will the heads point")
        self.play(FadeIn(card, scale=0.8), run_time=0.9)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        box = water_box()
        lips = make_lipids(T10, False)
        card = predict_card()
        self.add(box, card, *lips)
        t = ValueTracker(0)
        ring = Circle(radius=0.4, stroke_color=GREY, stroke_width=3).move_to([3.6, 3.3, 0])
        arc = always_redraw(lambda: Arc(radius=0.4, start_angle=PI / 2, angle=max(0.01, 2 * PI * (1 - t.get_value())),
                                        stroke_color=YELLOW, stroke_width=8).move_to([3.6, 3.3, 0]))
        self.add(ring, arc)
        self.play(t.animate.set_value(1), run_time=5.0, rate_func=linear)
        self.finish()


def ang_delta(a, b):
    return (b - a + PI) % TAU - PI


class S12Reveal(SpokenScene):
    def construct(self):
        box = water_box()
        lips = make_lipids(T10 + 5.0, False)
        card = predict_card()
        self.add(box, card, *lips)
        y0 = WAT_C[1]
        half = N_LIP // 2
        order = np.argsort([BASE[i][0] for i in range(N_LIP)])
        up_ids = [int(i) for i in order[0::2]]
        dn_ids = [int(i) for i in order[1::2]]
        xs = [-5.2 + 0.8 * k for k in range(half)]
        tgt = {}
        for k, i in enumerate(up_ids):
            tgt[i] = (np.array([xs[k], y0 + 2.0, 0]), 0.0, np.array([xs[k], y0 + 0.5, 0]))
        for k, i in enumerate(dn_ids):
            tgt[i] = (np.array([xs[k], y0 - 2.0, 0]), PI, np.array([xs[k], y0 - 0.5, 0]))

        def goto(which, dur):
            anims = []
            for i, m in enumerate(lips):
                m.clear_updaters()
                p0, a0 = m._p.copy(), m._a
                p1, a1 = which(i)
                da = ang_delta(a0, a1)

                def f(mm, a, p0=p0, a0=a0, p1=p1, da=da):
                    s = smooth(a)
                    pn, an = p0 + (p1 - p0) * s, a0 + da * s
                    mm.rotate(an - mm._a, about_point=mm._p)
                    mm.shift(pn - mm._p)
                    mm._p, mm._a = pn, an
                anims.append(UpdateFromAlphaFunc(m, f, run_time=dur))
            return anims
        self.at("Out toward the water")
        self.play(FadeOut(card), *goto(lambda i: (tgt[i][0], tgt[i][1]), 3.0))
        self.at("the tails tuck")
        self.play(*goto(lambda i: (tgt[i][2], tgt[i][1]), 2.0))
        dl = T("double layer: heads out, tails in", 34, ORANGE, weight=BOLD).move_to([0, 3.3, 0])
        self.at("That double layer")
        self.play(FadeIn(dl, shift=DOWN * 0.2), run_time=0.8)
        self.at("basic structure of a cell membrane")
        cx, cy = WAT_C[0], WAT_C[1]

        def ring_t(i):
            k = up_ids.index(i) if i in up_ids else dn_ids.index(i)
            ph = TAU * k / half + PI / 2
            if i in up_ids:
                R, rot = 2.45, ph - PI / 2
            else:
                R, rot = 1.45, ph + PI / 2
            return np.array([cx + R * np.cos(ph), cy + R * np.sin(ph), 0]), rot
        cell = Circle(radius=0.75, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([cx, cy, 0])
        nuc_ = Circle(radius=0.25, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([cx, cy, 0])
        cm = T("cell membrane", 36, ORANGE, weight=BOLD).move_to([0, 3.3, 0])
        self.play(*goto(lambda i: ring_t(i), 1.8), FadeIn(cell, scale=0.4), FadeIn(nuc_, scale=0.4), FadeOut(dl), FadeIn(cm, shift=DOWN * 0.2))
        self.play(Rotate(VGroup(*lips), angle=0.25, about_point=np.array([cx, cy, 0])), run_time=1.2, rate_func=there_and_back)
        self.finish()


class S13Fat(SpokenScene):
    def construct(self):
        self.add(stage(GREY))
        spine = Line([-4.5, 1.6, 0], [-4.5, -1.6, 0], color=ORANGE, stroke_width=8)
        teeth_y = [1.2, 0.0, -1.2]
        teeth = VGroup(*[Line([-4.5, y, 0], [-3.9, y, 0], color=ORANGE, stroke_width=8) for y in teeth_y])
        comb = VGroup(spine, teeth)
        tails = VGroup(*[ParametricFunction(lambda t, y=y: np.array([-1.5 + 2.4 * t, y + 0.13 * np.sin(11 * t), 0]),
                                            t_range=[0, 1, 0.01], color=ORANGE, stroke_width=7) for y in teeth_y])
        self.wait(0.2)
        self.play(Create(spine), Create(teeth), run_time=1.0)
        self.play(LaggedStart(*[Create(t) for t in tails], lag_ratio=0.3), run_time=1.4)
        self.at("not a chain")
        chain_q = T("chain?", 36, TEXT, weight=BOLD).move_to([-4.6, -3.0, 0])
        cross = Line(chain_q.get_corner(DL) + LEFT * 0.1, chain_q.get_corner(UR) + RIGHT * 0.1, color=RED, stroke_width=8)
        self.play(FadeIn(chain_q), run_time=0.5)
        self.play(Create(cross), run_time=0.5)
        self.at("One glycerol")
        gl = T("glycerol", 32, ORANGE, weight=BOLD).move_to([-4.5, 2.2, 0])
        self.play(FadeIn(gl), Indicate(comb, color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.at("three fatty acids")
        fl = T("fatty acid", 32, ORANGE, weight=BOLD).move_to([-0.3, 2.2, 0])
        self.play(FadeIn(fl), LaggedStart(*[Indicate(t, color=YELLOW, scale_factor=1.1) for t in tails], lag_ratio=0.3), run_time=1.6)
        self.at("three links")
        cn = Counters(0, 0)
        self.add(cn.rows)
        for j, y in enumerate(teeth_y):
            bar = Line([-3.9, y, 0], [-1.5, y, 0], color=GREY, stroke_width=10)
            self.play(Create(bar), cn.a.animate.set_value(j + 1), run_time=0.5)
            self.wait(0.15)
        self.at("Count from the free pieces")
        tb = VGroup(Rectangle(width=4.6, height=3.4, stroke_color=WATER, stroke_width=3, fill_color=WATER, fill_opacity=0.06).move_to([4.3, -0.4, 0]),
                    T("counted from free pieces", 26, WATER).move_to([4.3, 0.95, 0]))
        slots = [np.array([4.3 + (c - 1) * 1.1, -0.2 - r * 0.9, 0]) for r in range(2) for c in range(3)]
        self.play(FadeIn(tb, shift=LEFT * 0.3), run_time=1.0)
        self.at("three waters are missing")
        for j in range(3):
            v = vee(True, 1.4).move_to([-2.7, teeth_y[j] + 0.5, 0])
            self.play(FadeIn(v, scale=0.5), run_time=0.3)
            self.play(v.animate.move_to(slots[j]), cn.b.animate.set_value(j + 1), run_time=0.8)
        self.at("water count still works")
        self.play(ShowPassingFlash(cn.pulse_rect().set_stroke(YELLOW, 6), time_width=1.0),
                  Indicate(tb, color=WATER, scale_factor=1.04), run_time=1.5)
        self.at("chain picture does not")
        nc = T("not a chain", 36, RED, weight=BOLD).move_to([0.2, -3.0, 0])
        self.play(FadeIn(nc, shift=UP * 0.2), Indicate(cross, color=RED, scale_factor=1.3), run_time=1.2)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        xs = [-4.8, -1.6, 1.6, 4.8]
        panels = [RoundedRectangle(corner_radius=0.2, width=3.0, height=4.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([x, 0.5, 0]) for x in xs]
        ch = Chain([sugar(0.2).move_to(coil_pos(i, (xs[0], 0.5), 0.58)) for i in range(7)], w=4, col=STARCH_L)
        fib = VGroup(*[Chain([sugar(0.17).move_to([xs[1] - 0.95 + 0.38 * i, 1.3 - 0.55 * k, 0]) for i in range(6)], w=3, col=CELL_L).group for k in range(4)])
        en = Enz([xs[2], 0.5, 0], 0.0, 0.95, PI, bg=PANEL_S14)
        lip_up = [lipid(0.6).move_to([xs[3] - 1.15 + 0.46 * i, 1.0, 0]) for i in range(6)]
        lip_dn = [lipid(0.6).rotate(PI).move_to([xs[3] - 1.15 + 0.46 * i, 0.1, 0]) for i in range(6)]
        icons = [ch.group, fib, en.mob, VGroup(*lip_up, *lip_dn)]
        wig_all(ch.blocks, 0.03)
        wiggle(icons[3], 0.04)
        self.add(*panels)
        VGroup(*icons[:3]).scale(1.0)
        self.play(LaggedStart(*[FadeIn(ic, scale=0.7) for ic in icons], lag_ratio=0.3), run_time=1.3)
        self.at("tells you how many links")
        self.play(*[Indicate(p, color=WATER, scale_factor=1.02) for p in panels[:2]], run_time=1.2)
        self.at("tell you the job")
        tags = [T(s, 36, c, weight=BOLD).move_to([x, -2.35, 0]) for s, c, x in
                zip(["store", "support", "cut", "boundary"], [GREEN, GOLD, AMINO, ORANGE], xs)]
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tags], lag_ratio=0.4), run_time=2.0)
        self.at("decide what each molecule can do")
        self.play(*[Indicate(p, color=YELLOW, scale_factor=1.03) for p in panels], run_time=1.6)
        self.finish()


class S15End(EndCard):
    LINE = "Blocks, links and shape decide the job."
