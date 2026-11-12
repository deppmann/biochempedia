"""Mean and Spread (drift, gene flow, consistent selection across replicate bags of beads)

COLOR MAP (one color per concept, whole film)
  GOLD bead / bar   = the "gold" allele          BLUE bead / bar = the other allele
  WHITE TRIANGLE    = mean allele frequency across replicates
  PURPLE            = drift: chance sampling and the scatter (spread) it makes
  ORANGE            = gene flow: immigrants and the shift they cause
  GREEN             = consistent selection
  TEAL              = effective population size (Ne)
  TEXT              = labels; GREY = de-emphasised
Honesty: every dot cloud is a computed Wright-Fisher run (40 replicates, 2N copies per bag) or marked schematic.
The gene-flow slide is one mixing step with sampling set aside (marked schematic in the scene).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

GB = "#F2C230"       # gold bead
BB = BLUE            # blue bead
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BAG = "#C9A27A"

AX_Y = -2.45


def sx(f):
    return -6.0 + 12.0 * f


# ------------------------------------------------------------------ computed models
def wf(copies, gens, seed, s=0.0, m=0.0, pi=0.2, n=40, p0=0.5):
    """Wright-Fisher: n replicates, `copies` gene copies each, optional selection s and migration m."""
    rng = np.random.default_rng(seed)
    out = np.zeros((n, gens + 1))
    out[:, 0] = p0
    for g in range(gens):
        p = out[:, g]
        q = p * (1 + s) / (1 + s * p) if s else p
        if m:
            q = (1 - m) * q + m * pi
        out[:, g + 1] = rng.binomial(copies, q) / copies
    return out


A_SIM = wf(20, 40, seed=244)                 # small bags, neutral
B_SIM = wf(200, 20, seed=5)                 # ten times bigger
C_SIM = wf(20, 40, seed=3, s=0.12)          # weak consistent selection
D_SIM = wf(20, 40, seed=8, m=0.12, pi=0.2)  # gene flow
FLOW = np.array([[0.5, 0.4]] * 40)          # one mixing step, schematic
_l = np.linspace(-2.17, -0.05, 40)
_perm = np.random.default_rng(2).permutation(39) + 1
LANES = np.concatenate([[_l[0]], _l[_perm]])
ZERO = np.array([[0.5, 0.5]] * 40)


# ------------------------------------------------------------------ pieces
def make_axis():
    line = Line([-6.0, AX_Y, 0], [6.0, AX_Y, 0], stroke_color=TEXT, stroke_width=3)
    ticks = VGroup(*[Line([sx(f), AX_Y - 0.1, 0], [sx(f), AX_Y + 0.1, 0], stroke_color=TEXT, stroke_width=3) for f in (0, 0.5, 1)])
    labs = VGroup(T("0", 28).move_to([sx(0), -3.3, 0]), T("0.5", 28).move_to([sx(0.5), -3.3, 0]), T("1", 28).move_to([sx(1), -3.3, 0]),
                  T("frequency of gold", 28, GB).move_to([-3.0, -3.3, 0]))
    return VGroup(line, ticks, labs)


def set_k(bag, k):
    if bag.k == k:
        return
    bag.k = k
    for i, b in enumerate(bag.beads):
        op = b.get_fill_opacity()
        b.set_fill(GB if bag.rank[i] < k else BB, opacity=op if op > 0 else 1)


def make_bag(scale=1.0, k=10, seed=0, jig=0.028, copies=20):
    w, h = 1.7, 1.4
    body = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=BAG, stroke_width=3, fill_color="#6B4F36", fill_opacity=0.5)
    neck = Polygon([-0.3, h / 2, 0], [0.3, h / 2, 0], [0.42, h / 2 + 0.22, 0], [-0.42, h / 2 + 0.22, 0],
                   stroke_color=BAG, stroke_width=3, fill_color="#6B4F36", fill_opacity=0.5)
    tie = Line([-0.3, h / 2, 0], [0.3, h / 2, 0], stroke_color="#E8D3A8", stroke_width=5)
    rng = np.random.default_rng(seed)
    beads = []
    for r in range(4):
        for c in range(5):
            x = -0.65 + c * 0.325 + rng.uniform(-0.04, 0.04)
            y = 0.45 - r * 0.3 + rng.uniform(-0.04, 0.04)
            b = Circle(radius=0.105, stroke_color=BG, stroke_width=1.2, fill_opacity=1).move_to([x, y, 0])
            beads.append(b)
    bag = VGroup(body, neck, tie, *beads)
    bag.beads = beads
    bag.rank = list(rng.permutation(copies))
    bag.k = -1
    bag.scale(scale)
    bag.jig = jig * scale
    set_k(bag, k)
    return bag


def jiggle(bag, speed=1.0):
    rng = np.random.default_rng(int(abs(bag.get_center()[0] * 7) + 3))
    for b in bag.beads:
        b.off = np.zeros(3)
        b.ph = rng.uniform(0, 6.28)
        b.wv = rng.uniform(1.8, 3.4) * speed

        def u(m, dt, amp=bag.jig):
            m.ph += dt * m.wv
            new = amp * np.array([np.sin(m.ph), np.cos(m.ph * 1.3), 0])
            m.shift(new - m.off)
            m.off = new
        b.add_updater(u)
    return bag


def bag_row(arr, g, rows=range(5), xs=(-4.4, -2.2, 0.0, 2.2, 4.4), y=2.2, scale=1.0):
    bags = VGroup()
    for j, (r, x) in enumerate(zip(rows, xs)):
        bg = make_bag(scale, k=int(round(arr[r, int(g.get_value())] * 20)), seed=j + 1).move_to([x, y, 0])
        jiggle(bg)
        bg.row = r
        bags.add(bg)

    def upd(m):
        gv = min(g.get_value(), arr.shape[1] - 1)
        for bg in m:
            set_k(bg, int(round(arr[bg.row, int(gv)] * 20)))
    bags.add_updater(upd)
    return bags


def make_dots(arr, g, r=0.12, bob=0.03):
    dots = VGroup()
    for i in range(len(arr)):
        d = Circle(radius=r, stroke_width=2, stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.22)
        d.st = 0
        d.ph = i * 0.9
        d.idx = i

        def u(m, dt):
            m.ph += dt * 1.6
            gv = min(g.get_value(), arr.shape[1] - 1.001)
            k = int(gv)
            fr = gv - k
            p = arr[m.idx, k] * (1 - fr) + arr[m.idx, k + 1] * fr
            m.move_to([sx(p), LANES[m.idx] + bob * np.sin(m.ph), 0])
            a = arr[m.idx, k]
            st = 1 if a >= 1 else (-1 if a <= 0 else 0)
            if st != m.st:
                m.st = st
                if st == 1:
                    m.set_fill(GB, 0.95).set_stroke(GB)
                elif st == -1:
                    m.set_fill(BB, 0.95).set_stroke(BB)
                else:
                    m.set_fill(TEXT, 0.22).set_stroke(TEXT)
        d.add_updater(u)
        d.move_to([sx(arr[i, 0]), LANES[i], 0])
        dots.add(d)
    return dots


def make_tri(arr, g, y=AX_Y - 0.33):
    tri = Triangle(stroke_width=0, fill_color=WHITE, fill_opacity=1).scale(0.19)

    def u(m):
        gv = min(g.get_value(), arr.shape[1] - 1.001)
        k = int(gv)
        fr = gv - k
        mean = float((arr[:, k] * (1 - fr) + arr[:, k + 1] * fr).mean())
        m.move_to([sx(mean), y, 0])
    tri.add_updater(u)
    u(tri)
    return tri


def follow(label, mob, dx=0.3, dy=0.0):
    def u(m):
        c = mob.get_center()
        m.move_to([c[0] + dx, AX_Y - 0.33 + dy, 0], aligned_edge=LEFT)
    label.add_updater(u)
    u(label)
    return label


def make_counter(g, fmt, pos, color=TEXT, size=28, align=LEFT):
    t = T(fmt(int(g.get_value())), size, color)
    t.cur = int(g.get_value())
    t.move_to(pos, aligned_edge=align)

    def u(m):
        v = int(g.get_value())
        if v != m.cur:
            m.cur = v
            m.become(T(fmt(v), size, color).move_to(pos, aligned_edge=align))
    t.add_updater(u)
    return t


def make_bracket(dots, label, y=0.25, color=PURPLE):
    ln = Line(LEFT, RIGHT, stroke_color=color, stroke_width=4)
    tl = Line([0, -0.12, 0], [0, 0.12, 0], stroke_color=color, stroke_width=4)
    tr = tl.copy()
    lab = T(label, 28, color)
    grp = VGroup(ln, tl, tr, lab)

    def u(m):
        xs = [d.get_center()[0] for d in dots]
        a, b = min(xs) - 0.2, max(xs) + 0.2
        b = max(b, a + 0.6)
        ln.put_start_and_end_on([a, y, 0], [b, y, 0])
        tl.move_to([a, y, 0])
        tr.move_to([b, y, 0])
        lab.move_to([float(np.clip((a + b) / 2, -3.2, 3.0)), y + 0.34, 0])
    grp.add_updater(u)
    u(grp)
    return grp


def run_g(g, rate, gmax):
    def u(m, dt):
        m.set_value(min(m.get_value() + rate * dt, gmax))
    g.add_updater(u)


def ring_on(mob, color=TEXT, r=0.3, w=4):
    c = Circle(radius=r, stroke_color=color, stroke_width=w)
    c.add_updater(lambda m: m.move_to(mob.get_center()))
    return c


class W(SpokenScene):
    """Scene with the shared world helpers."""

    def world(self, arr, g0=0.0, bags=True, tri=True, axis=True, rows=range(5), bag_scale=1.0, dots=True):
        self.g = ValueTracker(g0)
        self.add(self.g)
        self.axis = make_axis()
        if axis:
            self.add(self.axis)
        self.bags = bag_row(arr, self.g, rows=rows, scale=bag_scale) if bags else VGroup()
        self.dots = make_dots(arr, self.g) if dots else VGroup()
        self.tri = make_tri(arr, self.g) if tri else VGroup()
        self.add(self.bags, self.dots, self.tri)
        return self


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Drift, Gene Flow and Competing Explanations"
    TITLE = "Mean and Spread"


def lizard(color="#C9B27A", s=1.0):
    body = Ellipse(width=0.9, height=0.3, stroke_width=0, fill_color=color, fill_opacity=1)
    head = Circle(radius=0.16, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0.5, 0.04, 0])
    tail = ArcBetweenPoints([-0.4, 0, 0], [-1.0, -0.2, 0], angle=1.0, stroke_color=color, stroke_width=7)
    legs = VGroup(*[Line([x, 0, 0], [x + dx, -0.2, 0], stroke_color=color, stroke_width=5) for x, dx in ((-0.25, -0.1), (-0.25, 0.1), (0.25, -0.1), (0.25, 0.1))])
    return VGroup(legs, body, head, tail).scale(s)


class S01Question(W):
    def construct(self):
        PW, PH = 5.6, 3.5
        cl, cr = -3.45, 3.45
        py = 1.15
        sea = RoundedRectangle(corner_radius=0.2, width=PW, height=PH, stroke_color=BLUE, stroke_width=2, fill_color="#1d3b57", fill_opacity=0.65).move_to([cl, py, 0])
        isl = Ellipse(width=3.4, height=1.1, stroke_width=0, fill_color="#4F8A4B", fill_opacity=1).move_to([cl, py - 0.35, 0])
        land = RoundedRectangle(corner_radius=0.2, width=PW, height=PH, stroke_color="#7aa56a", stroke_width=2, fill_color="#3b5a3a", fill_opacity=0.7).move_to([cr, py, 0])
        hill = ArcBetweenPoints([cr - 2.8, py - 0.6, 0], [cr + 2.8, py - 0.6, 0], angle=-0.7, stroke_color="#8fbf7a", stroke_width=5)
        liz1 = lizard(s=0.9).move_to([cl + 0.1, py + 0.12, 0])
        liz2 = lizard(s=0.9).move_to([cr, py + 0.05, 0])
        nm1 = T("island", 34).move_to([cl, 3.4, 0])
        nm2 = T("mainland", 34).move_to([cr, 3.4, 0])
        waves = VGroup(*[VMobject(stroke_color=BLUE, stroke_width=3, stroke_opacity=0.7) for _ in range(3)])
        t = ValueTracker(0)
        self.add(t)

        def wv(m, dt):
            t.increment_value(dt)
            xs = np.linspace(cl - 2.5, cl + 2.5, 40)
            for j, w in enumerate(m):
                ys = 0.07 * np.sin(xs * 2.2 + t.get_value() * 1.6 + j * 2)
                base = py - 1.2 + j * 0.3 if j < 2 else py + 1.1
                w.set_points_as_corners([[x, base + y, 0] for x, y in zip(xs, ys)])
        waves.add_updater(wv)
        wv(waves, 0)
        for L, ph in ((liz1, 0.0), (liz2, 1.5)):
            L.ph = ph
            L.base = L.get_center()[1]
            L.add_updater(lambda m, dt: (setattr(m, "ph", m.ph + dt * 2.0), m.set_y(m.base + 0.05 * np.sin(m.ph))))
        self.add(waves)
        self.play(FadeIn(sea), FadeIn(land), FadeIn(nm1), FadeIn(nm2), FadeIn(isl), Create(hill), FadeIn(liz1, scale=0.6), run_time=0.8)
        bw, by = 5.0, -1.35

        def bar(frac, cx):
            gld = Rectangle(width=max(bw * frac, 0.01), height=0.6, stroke_width=0, fill_color=GB, fill_opacity=1)
            blu = Rectangle(width=max(bw * (1 - frac), 0.01), height=0.6, stroke_width=0, fill_color=BB, fill_opacity=1)
            gld.move_to([cx - bw / 2, by, 0], aligned_edge=LEFT)
            blu.next_to(gld, RIGHT, buff=0)
            return VGroup(gld, blu)
        b1, b2 = bar(0.85, cl), bar(0.1, cr)
        l1 = T("gold allele: common", 30, GB).move_to([cl, -2.0, 0])
        l2 = T("gold allele: rare", 30, GB).move_to([cr, -2.0, 0])
        self.at("common")
        self.play(GrowFromEdge(b1[0], LEFT), FadeIn(b1[1]), FadeIn(l1), run_time=1.0)
        self.at("rare")
        self.play(FadeIn(liz2, scale=0.6), GrowFromEdge(b2[0], LEFT), FadeIn(b2[1]), FadeIn(l2), run_time=1.0)
        t1 = chip("favored?", GREEN, 30).move_to([-4.2, -3.1, 0])
        t2 = chip("luck?", PURPLE, 30).move_to([0, -3.1, 0])
        t3 = chip("migrants?", ORANGE, 30).move_to([4.2, -3.1, 0])
        self.at("favor")
        self.play(FadeIn(t1, shift=UP * 0.2, scale=1.2), run_time=0.7)
        self.at("luck")
        self.play(FadeIn(t2, shift=UP * 0.2, scale=1.2), run_time=0.7)
        self.at("migrants")
        arr = Arrow([0.9, py, 0], [-0.9, py, 0], buff=0, color=ORANGE, stroke_width=8, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(t3, shift=UP * 0.2, scale=1.2), GrowArrow(arr), run_time=0.9)
        self.finish()


class S02Bag(W):
    def construct(self):
        bag = make_bag(2.1, k=10, seed=1).move_to([0, 1.55, 0])
        jiggle(bag)
        axis = make_axis()
        self.play(FadeIn(bag, scale=0.6), run_time=1.0)
        lab = T("one generation's\ngene pool", 32).move_to([-4.3, 1.7, 0])
        self.at("generation's")
        self.play(FadeIn(lab, shift=RIGHT * 0.2), run_time=0.8)
        self.at("bag of beads")
        self.play(Indicate(bag, scale_factor=1.06, color=BAG), run_time=1.0)
        gl = T("gold = one allele", 30, GB).move_to([4.3, 2.3, 0])
        self.at("Gold beads")
        gold = [b for i, b in enumerate(bag.beads) if bag.rank[i] < 10]
        blue = [b for i, b in enumerate(bag.beads) if bag.rank[i] >= 10]
        self.play(FadeIn(gl), *[Indicate(b, scale_factor=1.5, color=GB) for b in gold], run_time=1.4)
        bl = T("blue = the other", 30, BB).move_to([4.3, 1.1, 0])
        self.at("blue beads")
        self.play(FadeIn(bl), *[Indicate(b, scale_factor=1.5, color=BB) for b in blue], run_time=1.4)
        self.at("Half of them")
        dot = Circle(radius=0.12, stroke_width=2, stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.22).move_to([0, LANES[0], 0])
        guide = DashedLine([0, 0.2, 0], [0, -2.0, 0], color=GREY, stroke_width=3)
        self.play(Create(axis), run_time=1.0)
        self.play(Create(guide), FadeIn(dot, shift=UP * 0.4), run_time=0.9)
        tag = T("this bag", 28).move_to([0, -1.6, 0])
        self.play(FadeIn(tag), run_time=0.4)
        self.finish()


def sequence_13():
    s = [1] * 13 + [0] * 7
    np.random.default_rng(4).shuffle(s)
    return s


class S03Draw(W):
    def construct(self):
        axis = make_axis()
        dot = Circle(radius=0.12, stroke_width=2, stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.22).move_to([0, LANES[0], 0])
        tag = T("this bag", 28).move_to([0, -1.6, 0])
        self.add(axis, dot, tag)
        sc = 1.5
        A = make_bag(sc, k=10, seed=1).move_to([-3.6, 1.9, 0])
        B = make_bag(sc, k=10, seed=1).move_to([3.6, 1.9, 0])
        seq = sequence_13()
        for i, b in enumerate(B.beads):
            b.set_fill(GB if seq[i] else BB, 1)
        jiggle(A)
        self.play(FadeIn(A, scale=0.8), run_time=0.8)
        lblB = T("next generation", 30).move_to([3.6, 3.5, 0])
        for b in B.beads:
            b.set_opacity(0)
        self.at("next generation")
        self.play(FadeIn(B, scale=0.8), FadeIn(lblB), run_time=0.9)
        for b in B.beads:
            b.set_opacity(0)
        jiggle(B)
        slots = [b.get_center().copy() for b in B.beads]
        goldA = [b for i, b in enumerate(A.beads) if A.rank[i] < 10]
        blueA = [b for i, b in enumerate(A.beads) if A.rank[i] >= 10]
        palm = Circle(radius=0.24, stroke_color="#B98A68", stroke_width=2, fill_color="#E6B999", fill_opacity=1)
        arm = Rectangle(width=0.3, height=0.8, stroke_color="#B98A68", stroke_width=2, fill_color="#E6B999", fill_opacity=1)
        hand = VGroup(arm, palm)
        cur = [None]

        def hu(m):
            if cur[0] is not None:
                c = cur[0].get_center()
                palm.move_to([c[0], c[1] + 0.42, 0])
                arm.next_to(palm, UP, buff=-0.05)
        hand.add_updater(hu)
        rng = np.random.default_rng(9)
        label = T("20 draws,\neach bead put back", 30).move_to([0, 0.5, 0])
        self.at("a hand draws")
        t_end = self.t_of("A small draw") - 0.4
        dt = max(0.12, (t_end - self.elapsed() - 0.6) / 20.0)
        count = None
        gold_n = 0
        first = True
        for i in range(20):
            pool = goldA if seq[i] else blueA
            src = pool[int(rng.integers(0, len(pool)))]
            c = Circle(radius=0.16, stroke_color=BG, stroke_width=1.2, fill_color=GB if seq[i] else BB, fill_opacity=1)
            c.move_to(src.get_center()).set_z_index(5)
            hand.set_z_index(4)
            cur[0] = c
            if first:
                hu(hand)
                self.add(hand, c)
                self.play(FadeIn(hand), FadeIn(label), run_time=0.3)
                first = False
            else:
                self.add(c)
            self.play(c.animate.move_to(slots[i]), run_time=dt, rate_func=smooth)
            B.beads[i].set_opacity(1)
            self.remove(c)
            gold_n += seq[i]
            if count is not None:
                self.remove(count)
            count = T(f"{gold_n} of {i + 1} gold", 30, GB).move_to([3.6, 0.3, 0])
            self.add(count)
        cur[0] = None
        self.play(FadeOut(hand), run_time=0.4)
        self.at("A small draw")
        self.play(FadeOut(label), run_time=0.5)
        self.at("This one came out")
        ghost = dot.copy().set_fill(opacity=0.0).set_stroke(GREY, 3)
        self.add(ghost)
        tag2 = T("this draw", 28, GB).move_to([1.95, -1.25, 0])
        self.play(dot.animate.move_to([sx(0.65), LANES[0], 0]).set_fill(GB, 0.95).set_stroke(GB), FadeIn(tag2), Indicate(count, scale_factor=1.2, color=GB), run_time=1.6)
        self.finish()


class S04Drift(W):
    def construct(self):
        axis = make_axis()
        ghost = Circle(radius=0.12, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([0, LANES[0], 0])
        dot = Circle(radius=0.12, stroke_width=2, stroke_color=GB, fill_color=GB, fill_opacity=0.95).move_to([sx(0.65), LANES[0], 0])
        sc = 1.5
        A = make_bag(sc, k=10, seed=1).move_to([-3.6, 1.9, 0])
        B = make_bag(sc, k=10, seed=1).move_to([3.6, 1.9, 0])
        seq = sequence_13()
        for i, b in enumerate(B.beads):
            b.set_fill(GB if seq[i] else BB, 1)
        jiggle(A)
        jiggle(B)
        lblB = T("next generation", 30).move_to([3.6, 3.5, 0])
        count = T("13 of 20 gold", 30, GB).move_to([3.6, 0.3, 0])
        self.add(axis, ghost, dot, A, B, lblB, count)
        self.at("Nobody chose")
        self.play(Indicate(B, scale_factor=1.06, color=GB), run_time=1.2)
        self.at("just small")
        self.play(Indicate(B, scale_factor=1.08, color=PURPLE), Indicate(A, scale_factor=1.04, color=GREY), run_time=1.3)
        self.at("Change in allele")
        l2 = T("chance change in allele frequency\nfrom sampling parents", 32, TEXT, line_spacing=0.8).move_to([0, -0.65, 0])
        self.play(FadeOut(count), Write(l2), run_time=2.0)
        title = T("genetic drift", 48, PURPLE, font=TITLE_FONT).move_to([0, 0.4, 0])
        self.at("genetic drift")
        self.play(FadeIn(title, scale=1.3), Flash(title, color=PURPLE, flash_radius=0.9, line_length=0.3), run_time=1.0)
        badge = chip("no fitness difference needed", GREEN, 28).move_to([0, -1.58, 0])
        self.at("no difference")
        self.play(FadeIn(badge, scale=1.5), run_time=0.5)
        self.play(Indicate(badge, scale_factor=1.08), run_time=0.8)
        self.finish()


class S05Replicates(W):
    def construct(self):
        self.world(ZERO, bags=False, dots=True, tri=False)
        for d in self.dots[1:]:
            d.set_opacity(0)
        xs = (-4.4, -2.2, 0.0, 2.2, 4.4)
        bags = [make_bag(1.0, k=10, seed=j + 1).move_to([0, 2.2, 0]) for j in range(5)]
        for b in bags:
            jiggle(b)
        mid = bags[2]
        self.add(mid)
        self.at("One bag")
        self.play(Indicate(mid, scale_factor=1.1, color=BAG), run_time=1.0)
        self.at("run mini bags")
        self.add(*[b for b in bags if b is not mid])
        self.play(*[bags[j].animate.move_to([xs[j], 2.2, 0]) for j in range(5)], run_time=1.6)
        lab = T("same start, same conditions", 28, GREY).move_to([0, 0.95, 0])
        self.at("all starting")
        self.play(LaggedStart(*[d.animate.set_opacity(1) for d in self.dots[1:]], lag_ratio=0.04, run_time=2.0))
        for d in self.dots[1:]:
            d.set_fill(TEXT, 0.22)
        self.play(FadeIn(lab), run_time=0.5)
        self.at("Each bag")
        self.play(*[Indicate(b, scale_factor=1.1, color=BAG) for b in bags], run_time=1.0)
        lab2 = T("replicate populations", 30, PURPLE).move_to([0, 3.55, 0])
        self.at("replicate population")
        self.play(FadeIn(lab2, shift=DOWN * 0.2), run_time=0.6)
        tri = make_tri(ZERO, self.g)
        self.play(FadeIn(tri, shift=UP * 0.3), run_time=0.8)
        self.add(tri)
        self.finish()


class S06Spread(W):
    def construct(self):
        self.world(A_SIM, g0=0.0)
        ctr = make_counter(self.g, lambda v: f"generation {v}", [-6.4, 1.1, 0])
        cp = T("2N = 20 copies, computed", 28, GREY).move_to([6.4, 1.1, 0], aligned_edge=RIGHT)
        self.add(ctr, cp)
        self.wait(0.4)
        run_g(self.g, 1.8, 20)
        self.at("each bag wanders")
        mid = [i for i in range(40) if 0 < A_SIM[i, 14] < 1]
        up = max(mid, key=lambda i: A_SIM[i, 14])
        dn = min(mid, key=lambda i: A_SIM[i, 14])
        self.at("Some climb")
        r1 = ring_on(self.dots[up], GB, 0.28)
        self.play(FadeIn(r1), run_time=0.4)
        self.at("some fall")
        r2 = ring_on(self.dots[dn], BB, 0.28)
        self.play(FadeIn(r2), run_time=0.4)
        self.at("A few reach")
        self.play(FadeOut(r1), FadeOut(r2), run_time=0.4)
        tg = T("all gold", 28, GB).move_to([5.4, 0.3, 0])
        tb = T("all blue", 28, BB).move_to([-5.4, 0.3, 0])
        self.at("all gold")
        self.play(FadeIn(tg), run_time=0.4)
        self.at("all blue")
        self.play(FadeIn(tb), run_time=0.4)
        self.at("stay there")
        self.finish()


class S07Mean(W):
    def construct(self):
        self.world(A_SIM, g0=20.0)
        ctr = make_counter(self.g, lambda v: f"generation {v}", [-6.4, 1.1, 0])
        cp = T("2N = 20 copies, computed", 28, GREY).move_to([6.4, 1.1, 0], aligned_edge=RIGHT)
        self.add(ctr, cp)
        run_g(self.g, 0.9, 30)
        ring = ring_on(self.tri, TEXT, 0.35)
        self.at("white triangle")
        self.play(FadeIn(ring, scale=1.5), run_time=0.6)
        self.play(Indicate(self.tri, scale_factor=1.6), run_time=0.8)
        lab = follow(T("average", 28, TEXT), self.tri, dx=0.4)
        self.at("average across")
        self.play(FadeIn(lab), run_time=0.5)
        self.play(FadeOut(ring), run_time=0.4)
        br = make_bracket(self.dots, "spread", color=PURPLE)
        self.at("spread apart")
        self.play(FadeIn(br), run_time=0.8)
        self.at("where it started")
        start = DashedLine([0, AX_Y - 0.15, 0], [0, 0.15, 0], color=TEXT, stroke_width=3)
        self.play(Create(start), run_time=0.8)
        self.finish()


class S08Signature(W):
    def construct(self):
        self.world(A_SIM, g0=30.0)
        ctr = make_counter(self.g, lambda v: f"generation {v}", [-6.4, 1.1, 0])
        cp = T("2N = 20 copies, computed", 28, GREY).move_to([6.4, 1.1, 0], aligned_edge=RIGHT)
        start = DashedLine([0, AX_Y - 0.15, 0], [0, 0.15, 0], color=TEXT, stroke_width=3)
        lab = follow(T("average", 28, TEXT), self.tri, dx=0.4)
        br = make_bracket(self.dots, "spread", color=PURPLE)
        self.add(ctr, cp, start, lab, br)
        run_g(self.g, 0.9, 40)
        self.at("drift's signature")
        self.play(Indicate(br, scale_factor=1.1, color=PURPLE), run_time=1.0)
        self.at("spreads them apart")
        br2 = make_bracket(self.dots, "spread: grows", color=PURPLE)
        self.remove(br)
        self.add(br2)
        self.play(Flash(br2[3], color=PURPLE, flash_radius=0.8, line_length=0.25), run_time=0.9)
        self.at("without pushing")
        lab2 = T("average: no push, small wobble", 28, TEXT)
        lab2.add_updater(lambda m: m.move_to([self.tri.get_x() - 0.35, AX_Y - 0.33, 0], aligned_edge=RIGHT))
        self.play(FadeOut(lab), run_time=0.3)
        self.play(FadeIn(lab2), run_time=0.6)
        self.at("Chance favors")
        i = [j for j in range(40) if 0 < A_SIM[j, 35] < 1 and 0 < A_SIM[j, 40] < 1][1]
        d = self.dots[i]
        aL = Arrow(ORIGIN, LEFT * 0.7, buff=0, color=PURPLE, stroke_width=6, max_tip_length_to_length_ratio=0.5)
        aR = Arrow(ORIGIN, RIGHT * 0.7, buff=0, color=PURPLE, stroke_width=6, max_tip_length_to_length_ratio=0.5)
        aL.add_updater(lambda m: m.move_to(d.get_center() + LEFT * 0.55))
        aR.add_updater(lambda m: m.move_to(d.get_center() + RIGHT * 0.55))
        self.play(FadeIn(aL), FadeIn(aR), run_time=0.7)
        self.at("triangle only")
        self.play(Indicate(self.tri, scale_factor=1.8), run_time=1.0)
        self.finish()


class S09Size(W):
    def construct(self):
        self.world(A_SIM, g0=20.0)
        ctr = make_counter(self.g, lambda v: f"generation {v}", [-6.4, 1.1, 0])
        cp = T("2N = 20 copies, computed", 28, GREY).move_to([6.4, 1.1, 0], aligned_edge=RIGHT)
        self.add(ctr, cp)
        self.g.clear_updaters()
        self.at("Now make")
        self.wait(0.3)
        old = self.dots
        for d in old:
            d.clear_updaters()
        self.play(*[d.animate.set_fill(PURPLE, 0.25).set_stroke(PURPLE, opacity=0.35) for d in old], FadeOut(self.tri), run_time=0.8)
        self.remove(ctr)
        self.at("ten times")
        cp2 = T("2N = 200 copies, computed", 28, GREY).move_to([6.4, 0.95, 0], aligned_edge=RIGHT)
        self.play(*[b.animate.scale(1.15) for b in self.bags], Transform(cp, cp2), run_time=1.4)
        g2 = ValueTracker(0.0)
        self.add(g2)
        self.bags.clear_updaters()

        def bu(m):
            gv = min(g2.get_value(), 19.999)
            for bg in m:
                set_k(bg, int(round(B_SIM[bg.row, int(gv)] * 20)))
        self.bags.add_updater(bu)
        nd = make_dots(B_SIM, g2)
        nt = make_tri(B_SIM, g2)
        ctr2 = make_counter(g2, lambda v: f"generation {v}", [-6.4, 0.95, 0])
        gl = T("faint: 2N = 20 copies", 28, PURPLE).move_to([-3.4, 0.38, 0])
        self.at("start again")
        self.play(FadeIn(nd), FadeIn(nt), FadeIn(ctr2), FadeIn(gl), run_time=0.9)
        self.at("The dots still")
        run_g(g2, 4.0, 20)
        self.at("far more slowly")
        self.wait(1.2)
        self.at("Bigger pools")
        self.play(Indicate(cp, scale_factor=1.08, color=TEXT), run_time=1.0)
        self.finish()


class S10Ne(W):
    def construct(self):
        self.world(A_SIM, g0=0.0, bags=False)
        run_g(self.g, 1.8, 20)
        br = make_bracket(self.dots, "scatter", color=PURPLE)
        self.at("scatter")
        self.play(FadeIn(br), run_time=0.6)
        marks = VGroup()
        for gi in range(3):
            grp = VGroup(*[Line([gi * 1.15 + j * 0.2, 0, 0], [gi * 1.15 + j * 0.2, 1.1, 0], stroke_color=TEXT, stroke_width=6) for j in range(4)],
                         Line([gi * 1.15 - 0.1, 0.15, 0], [gi * 1.15 + 0.7, 0.95, 0], stroke_color=TEXT, stroke_width=6))
            marks.add(grp)
        marks.move_to([-3.6, 2.6, 0])
        tl = T("animals counted", 30).move_to([-3.6, 1.45, 0])
        self.at("not simply")
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.3), FadeIn(tl), run_time=1.8)
        cross = Line(marks.get_corner(UR) + UR * 0.15, marks.get_corner(DL) + DL * 0.15, stroke_color=RED, stroke_width=7).set_opacity(0.85)
        self.at("count")
        self.play(Create(cross), run_time=0.8)
        chp = chip("effective population\nsize, Ne", TEAL, 28).move_to([4.0, 2.95, 0])
        self.at("effective population")
        self.play(FadeIn(chp, shift=LEFT * 0.3), run_time=0.9)
        sub = T("the size of an ideal\npopulation that drifts\nas fast", 28, TEXT, line_spacing=0.8).move_to([4.0, 1.5, 0])
        self.at("the size of")
        self.play(FadeIn(sub), run_time=0.8)
        ideal = make_bag(0.8, k=10, seed=3).move_to([0.9, 2.3, 0])
        jiggle(ideal)
        self.at("ideal population")
        self.play(FadeIn(ideal, scale=0.7), run_time=0.8)
        self.at("drifts as fast")
        self.play(Indicate(ideal, scale_factor=1.15, color=TEAL), Indicate(br, scale_factor=1.1, color=PURPLE), run_time=1.2)
        self.finish()


def jug():
    body = RoundedRectangle(corner_radius=0.18, width=0.8, height=0.95, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.35)
    spout = Polygon([0.35, 0.3, 0], [0.65, 0.5, 0], [0.4, 0.05, 0], stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.35)
    handle = Arc(radius=0.25, start_angle=PI / 2, angle=PI, stroke_color=ORANGE, stroke_width=4).move_to([-0.45, 0.0, 0])
    beads = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=(GB if j == 2 else BB), fill_opacity=1).move_to([-0.2 + (j % 3) * 0.2, -0.15 + (j // 3) * 0.25, 0]) for j in range(6)])
    return VGroup(handle, body, spout, beads)


class S11Flow(W):
    def construct(self):
        self.world(ZERO, g0=0.0)
        lab = T("immigrants: mostly blue", 28, ORANGE).move_to([-3.0, 3.55, 0])
        j = jug().move_to([-6.1, 2.8, 0])
        self.at("all half gold")
        self.wait(0.6)
        self.at("Now pour")
        self.play(FadeIn(j, shift=DOWN * 0.3), FadeIn(lab), run_time=0.9)
        self.at("pour beads")
        mouth = np.array([-5.5, 3.0, 0])
        beads = []
        anims = []
        for x in (-4.4, -2.2, 0.0, 2.2, 4.4):
            for q in range(3):
                col = GB if q == 2 else BB
                c = Circle(radius=0.1, stroke_color=BG, stroke_width=1, fill_color=col, fill_opacity=1).move_to(mouth).set_z_index(6)
                path = ArcBetweenPoints(mouth, np.array([x + (q - 1) * 0.25, 2.35, 0]), angle=-0.8)
                beads.append(c)
                self.add(c)
                anims.append(MoveAlongPath(c, path, run_time=2.0 + 0.1 * q, rate_func=smooth))
        self.play(Rotate(j, angle=0.6, about_point=j.get_center()), LaggedStart(*anims, lag_ratio=0.05), run_time=2.8)
        self.play(*[FadeOut(c, scale=0.3) for c in beads], Rotate(j, angle=-0.6, about_point=j.get_center()), run_time=0.5)
        self.bags.clear_updaters()
        for bg in self.bags:
            set_k(bg, 8)
        self.play(*[Flash(bg, color=ORANGE, flash_radius=1.0, line_length=0.2) for bg in self.bags], run_time=0.8)
        self.at("gene flow")
        gf = T("gene flow", 48, ORANGE, font=TITLE_FONT).move_to([0, 0.6, 0])
        self.play(FadeIn(gf, scale=1.3), run_time=0.8)
        self.finish()


class S12Flow2(W):
    def construct(self):
        g = ValueTracker(0.0)
        self.add(g)
        axis = make_axis()
        bags = bag_row(ZERO, g)
        bags.clear_updaters()
        for bg in bags:
            set_k(bg, 8)
        dots = make_dots(FLOW, g)
        tri = make_tri(FLOW, g)
        self.add(axis, bags, dots, tri)
        start = DashedLine([0, AX_Y - 0.15, 0], [0, 0.15, 0], color=TEXT, stroke_width=3)
        tag = T("all bags started at 0.5;\nsame pour", 28, TEXT, line_spacing=0.8).move_to([4.0, -0.9, 0])
        sch = T("schematic: one pour, sampling set aside", 24, GREY).move_to([3.6, -1.85, 0])
        self.add(sch)
        self.at("started at")
        self.play(Create(start), FadeIn(tag), run_time=1.0)
        self.at("same pour")
        self.play(*[Indicate(b, scale_factor=1.08, color=ORANGE) for b in bags], run_time=1.0)
        mk = DashedLine([sx(0.2), AX_Y - 0.15, 0], [sx(0.2), 0.15, 0], color=ORANGE, stroke_width=4)
        mkl = T("immigrants' frequency", 28, ORANGE).move_to([sx(0.2) - 0.1, 0.55, 0])
        arrow = Arrow([0, 0.15, 0], [sx(0.4), 0.15, 0], buff=0, color=ORANGE, stroke_width=8, max_tip_length_to_length_ratio=0.25)
        self.at("slides")
        self.play(g.animate.set_value(1.0), GrowArrow(arrow), run_time=2.0, rate_func=smooth)
        self.at("immigrants")
        self.play(Create(mk), FadeIn(mkl), run_time=0.8)
        self.at("triangle slides")
        ring = ring_on(tri, ORANGE, 0.35)
        gfl = T("gene flow pushes the average", 28, ORANGE).move_to([3.0, 1.0, 0])
        self.play(FadeIn(ring, scale=1.5), FadeIn(gfl), run_time=0.8)
        self.play(Indicate(tri, scale_factor=1.7), run_time=0.8)
        self.at("Unlike drift")
        self.play(FadeOut(ring), Indicate(arrow, scale_factor=1.15, color=ORANGE), run_time=1.2)
        self.at("same way every")
        self.play(Indicate(tag, scale_factor=1.1, color=ORANGE), run_time=1.2)
        self.finish()


def glow(bags):
    for bg in bags:
        for i, b in enumerate(bg.beads):
            if bg.rank[i] < 10:
                b.gl = 0.0

                def u(m, dt):
                    m.gl += dt * 3.0
                    m.set_stroke(GB, 2.0 + 2.5 * (0.5 + 0.5 * np.sin(m.gl)), 1.0)
                b.add_updater(u)


def question_marks():
    sp = VGroup(Line([-0.9, 0.25, 0], [0.9, 0.25, 0], stroke_color=PURPLE, stroke_width=4), Line([-0.9, 0.13, 0], [-0.9, 0.37, 0], stroke_color=PURPLE, stroke_width=4),
                Line([0.9, 0.13, 0], [0.9, 0.37, 0], stroke_color=PURPLE, stroke_width=4))
    q1 = T("?", 56, TEXT, weight=BOLD).move_to([-0.8, AX_Y - 0.33, 0])
    q2 = T("?", 56, PURPLE, weight=BOLD).move_to([0, 0.75, 0])
    return q1, sp, q2


class S13Predict(W):
    def construct(self):
        self.world(ZERO, g0=0.0)
        self.at("gold carriers")
        glow(self.bags)
        lab = T("gold carriers leave\nmore offspring, in every bag", 28, GREEN, line_spacing=0.8).move_to([3.9, -1.2, 0])
        self.play(FadeIn(lab), *[Flash(bg, color=GB, flash_radius=1.0, line_length=0.2) for bg in self.bags], run_time=1.4)
        self.at("consistent selection")
        cs = T("consistent selection", 38, GREEN, font=TITLE_FONT).move_to([3.9, -0.1, 0])
        self.play(FadeIn(cs, scale=1.3), run_time=0.9)
        q1, sp, q2 = question_marks()
        self.at("the triangle")
        self.play(FadeIn(q1, scale=1.6), Indicate(self.tri, scale_factor=1.8), run_time=0.9)
        self.at("spread")
        self.play(Create(sp), FadeIn(q2, scale=1.6), run_time=0.9)
        self.finish()


class S14Pause(NarratedScene):
    def construct(self):
        ax = make_axis()
        g = ValueTracker(0.0)
        self.add(g)
        bags = bag_row(ZERO, g)
        bags.clear_updaters()
        glow(bags)
        dots = make_dots(ZERO, g)
        tri = make_tri(ZERO, g)
        lab = T("gold carriers leave\nmore offspring, in every bag", 28, GREEN, line_spacing=0.8).move_to([3.9, -1.2, 0])
        cs = T("consistent selection", 38, GREEN, font=TITLE_FONT).move_to([3.9, -0.1, 0])
        q1, sp, q2 = question_marks()
        cap = T("Predict:\ntriangle?  spread?", 34, TEXT, line_spacing=0.8).move_to([-3.7, -0.6, 0])
        self.add(ax, bags, dots, tri, lab, cs, q1, sp, q2, cap)
        for n in (5, 4, 3, 2, 1):
            tm = T(str(n), 64, GB, weight=BOLD).move_to([-3.7, -1.85, 0])
            self.add(tm)
            self.play(Indicate(tm, scale_factor=1.25, color=GB), run_time=0.95)
            self.wait(0.05)
            self.remove(tm)
        self.finish()


class S15Reveal(W):
    def construct(self):
        self.world(C_SIM, g0=0.0)
        glow(self.bags)
        lab = T("selection pushes the average; drift still spreads", 28, GREEN).move_to([0, 1.1, 0])
        br = make_bracket(self.dots, "spread", color=PURPLE)
        run_g(self.g, 1.9, 20)
        self.wait(0.2)
        self.at("triangle creeps")
        ring = ring_on(self.tri, GREEN, 0.35)
        self.play(FadeIn(ring, scale=1.5), run_time=0.6)
        self.at("selection pushes")
        self.play(FadeIn(lab), run_time=0.8)
        self.at("But while")
        self.play(FadeOut(ring), FadeIn(br), run_time=0.8)
        self.at("keep scattering")
        self.play(Indicate(br, scale_factor=1.1, color=PURPLE), run_time=1.0)
        self.finish()


def panel(cx, arr, g, title, color, ax_y=0.45, band=(0.75, 2.6), seed=0):
    rng = np.random.default_rng(seed)
    lanes = np.linspace(band[0], band[1], 40)[rng.permutation(40)]
    w = 1.85

    def px(p):
        return cx - w + 2 * w * p
    frame = RoundedRectangle(corner_radius=0.15, width=2 * w + 0.4, height=3.7, stroke_color=color, stroke_width=2).move_to([cx, 1.65, 0])
    ax = Line([cx - w, ax_y, 0], [cx + w, ax_y, 0], stroke_color=TEXT, stroke_width=3)
    st = DashedLine([px(0.5), ax_y - 0.1, 0], [px(0.5), band[1] + 0.1, 0], color=GREY, stroke_width=2)
    ttl = T(title, 34, color).move_to([cx, 3.1, 0])
    dots = VGroup()
    for i in range(40):
        d = Circle(radius=0.075, stroke_width=1.5, stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.25)
        d.idx = i
        d.st = 0

        def u(m):
            gv = min(g.get_value(), arr.shape[1] - 1.001)
            k = int(gv)
            fr = gv - k
            p = arr[m.idx, k] * (1 - fr) + arr[m.idx, k + 1] * fr
            m.move_to([px(p), lanes[m.idx], 0])
            a = arr[m.idx, k]
            s2 = 1 if a >= 1 else (-1 if a <= 0 else 0)
            if s2 != m.st:
                m.st = s2
                m.set_fill(GB if s2 == 1 else (BB if s2 == -1 else TEXT), 0.95 if s2 else 0.25)
        d.add_updater(u)
        d.move_to([px(0.5), lanes[i], 0])
        dots.add(d)
    tri = Triangle(stroke_width=0, fill_color=WHITE, fill_opacity=1).scale(0.13)

    def ut(m):
        gv = min(g.get_value(), arr.shape[1] - 1.001)
        k = int(gv)
        fr = gv - k
        mean = float((arr[:, k] * (1 - fr) + arr[:, k + 1] * fr).mean())
        m.move_to([px(mean), ax_y - 0.22, 0])
    tri.add_updater(ut)
    ut(tri)
    return VGroup(frame, ax, st, ttl, dots, tri)


class S16Test(W):
    def construct(self):
        g = ValueTracker(0.0)
        self.add(g)
        p1 = panel(-4.2, A_SIM, g, "drift", PURPLE, seed=1)
        p2 = panel(0.0, D_SIM, g, "gene flow", ORANGE, seed=2)
        p3 = panel(4.2, C_SIM, g, "selection", GREEN, seed=3)
        self.at("Here is")
        self.play(FadeIn(p1), run_time=0.7)
        self.play(FadeIn(p2), run_time=0.7)
        self.play(FadeIn(p3), run_time=0.7)
        run_g(g, 2.0, 20)
        cap = T("three computed Wright-Fisher runs", 24, GREY).move_to([0, -3.6, 0])
        self.add(cap)
        s1 = chip("neutral null: what chance alone gives", PURPLE, 28).move_to([0, -0.9, 0])
        s2 = chip("fitness assay: do carriers do better?", GREEN, 28).move_to([0, -1.85, 0])
        s3 = chip("immigration and ancestry: who came in?", ORANGE, 28).move_to([0, -2.8, 0])
        self.at("Compare the replicate")
        self.play(FadeIn(s1, shift=UP * 0.2), Indicate(p1[5], scale_factor=1.8), run_time=1.0)
        self.at("for selection")
        self.play(FadeIn(s2, shift=UP * 0.2), Indicate(p3[5], scale_factor=1.8), run_time=1.0)
        self.at("For gene flow")
        self.play(FadeIn(s3, shift=UP * 0.2), Indicate(p2[5], scale_factor=1.8), run_time=1.0)
        self.finish()


class S17Scope(W):
    def construct(self):
        g = ValueTracker(20.0)
        self.add(g)
        p1 = panel(-4.2, A_SIM, g, "drift", PURPLE, seed=1)
        p2 = panel(0.0, D_SIM, g, "gene flow", ORANGE, seed=2)
        p3 = panel(4.2, C_SIM, g, "selection", GREEN, seed=3)
        self.add(p1, p2, p3)
        axis = make_axis()
        dots = make_dots(A_SIM, g)
        keep = [i for i in range(40) if 0.3 < A_SIM[i, 20] < 0.7][0]
        d0 = dots[keep]
        self.play(*[p.animate.scale(0.15).move_to([0, 0, 0]).set_opacity(0) for p in (p1, p2, p3)], FadeIn(axis), run_time=1.0)
        self.remove(p1, p2, p3)
        for d in dots:
            d.clear_updaters()
        d0.set_fill(TEXT, 0.9).set_stroke(TEXT)
        d0.move_to([sx(A_SIM[keep, 20]), AX_Y + 0.35, 0])
        self.play(FadeIn(d0, scale=2.0), run_time=0.4)
        self.at("on its own")
        lab = T("one population:\nno average to compare", 34, GREY, line_spacing=0.8).move_to([3.2, -0.6, 0])
        q = T("?", 80, GREY, weight=BOLD).move_to([d0.get_x(), -0.5, 0])
        self.play(FadeIn(lab), FadeIn(q, scale=1.4), run_time=0.9)
        self.at("cannot tell")
        self.play(Indicate(q, scale_factor=1.25, color=GREY), run_time=1.0)
        self.at("Replicates give")
        for i, d in enumerate(dots):
            if i == keep:
                continue
            d.move_to([sx(A_SIM[i, 20]), LANES[i], 0])
            a = A_SIM[i, 20]
            c = GB if a >= 1 else (BB if a <= 0 else TEXT)
            d.set_fill(c, 0.95 if a in (0, 1) else 0.22).set_stroke(c)
        self.play(FadeOut(lab), FadeOut(q), d0.animate.move_to([sx(A_SIM[keep, 20]), LANES[keep], 0]),
                  LaggedStart(*[FadeIn(d) for i, d in enumerate(dots) if i != keep], lag_ratio=0.02), run_time=1.0)
        mean = float(A_SIM[:, 20].mean())
        tri = Triangle(stroke_width=0, fill_color=WHITE, fill_opacity=1).scale(0.19).move_to([sx(mean), AX_Y - 0.33, 0])
        tl = T("average", 28, TEXT).move_to([sx(mean) + 0.4, AX_Y - 0.33, 0], aligned_edge=LEFT)
        self.at("an average")
        self.play(FadeIn(tri, shift=UP * 0.3), FadeIn(tl), run_time=0.8)
        self.at("compare with")
        self.play(Indicate(tri, scale_factor=1.8), run_time=1.0)
        self.finish()


class S18End(EndCard):
    LINE = "Drift scatters replicates; gene flow and selection push their average."
