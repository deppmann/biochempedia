"""107 Bottles (chapter 2 of drift, gene flow and competing explanations)

Same colour map and world as chapter 1 (../scenes.py):
  GOLD bead / bar   = the "gold" allele          BLUE bead = the other allele
  WHITE TRIANGLE    = mean allele frequency across replicates, under the axis "frequency of gold" (0 to 1)
  PURPLE            = drift: chance sampling and the scatter (spread) it makes
  GREEN             = consistent selection ("pushed")
  TEAL              = effective population size (Ne)
Honesty: the histogram is a computed Wright-Fisher run (107 lines, 2Ne = 18 gene copies, 19 generations) built with
Buri's estimate Ne = 9.0 and is labelled "illustration; not his data". The ideal-16 outline is the computed expected
histogram for 32 gene copies (20000 runs scaled to 107 lines). Differences between bottles in scene 5 are computed.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

GB = "#F2C230"       # gold allele
BB = BLUE            # blue allele
PURPLE = "#B58CD9"
GREEN_C = GREEN
GLASS = "#9DB7C9"
MEDIA = "#B9965B"
FLYC = "#C8AE7C"
AX_Y = -2.45
HMAX = 4.0
A_X = -5.0           # the single bottle, same place in scenes 2 to 5


def sx(f):
    return -6.0 + 12.0 * f


# ------------------------------------------------------------------ computed models
def wf(copies, gens, seed, n, p0=0.5):
    rng = np.random.default_rng(seed)
    out = np.zeros((n, gens + 1))
    out[:, 0] = p0
    for g in range(gens):
        out[:, g + 1] = rng.binomial(copies, out[:, g]) / copies
    return out


def bin_counts(col):
    """Lines per bar: bars at exactly 0 and 1, and 15 interior bars of width 1/16 centred on j/16.
    A line between two bar centres is split between the two (so the picture has no rounding gaps)."""
    c = np.zeros(17)
    for p in col:
        if p <= 0:
            c[0] += 1
        elif p >= 1:
            c[16] += 1
        else:
            x = min(max(p * 16, 1.0), 15.0)
            lo = min(int(x), 14)
            fr = x - lo
            c[lo] += 1 - fr
            c[lo + 1] += fr
    return c


SIM = wf(18, 19, 59, 107)                                   # Buri's Ne = 9.0 -> 18 gene copies, 107 lines
COUNTS = np.array([bin_counts(SIM[:, g]) for g in range(20)])
YM = np.maximum(COUNTS.max(axis=1), 10.0)
_big = wf(32, 19, 0, 20000)
IDEAL16 = bin_counts(_big[:, 19]) * 107.0 / 20000.0         # ideal population of 16 = 32 gene copies
ONE_LINE = wf(18, 19, 21, 1)[0]                              # one line: climbs, dips, climbs again
A_SIM = wf(20, 40, seed=244, n=40)                           # chapter 1's neutral bead run (40 bags, 20 beads)
_l = np.linspace(-2.17, -0.05, 40)
_perm = np.random.default_rng(2).permutation(39) + 1
LANES = np.concatenate([[_l[0]], _l[_perm]])


def interp(arr2d, gv):
    k = int(min(max(gv, 0), 18))
    fr = min(gv - k, 1.0)
    return arr2d[k] * (1 - fr) + arr2d[k + 1] * fr


# ------------------------------------------------------------------ pieces
def make_axis():
    line = Line([-6.0, AX_Y, 0], [6.0, AX_Y, 0], stroke_color=TEXT, stroke_width=3)
    ticks = VGroup(*[Line([sx(f), AX_Y - 0.1, 0], [sx(f), AX_Y + 0.1, 0], stroke_color=TEXT, stroke_width=3) for f in (0, 0.5, 1)])
    labs = VGroup(T("0", 28).move_to([sx(0), -3.3, 0]), T("0.5", 28).move_to([sx(0.5), -3.3, 0]), T("1", 28).move_to([sx(1), -3.3, 0]),
                  T("frequency of gold", 28, GB).move_to([-3.0, -3.3, 0]))
    return VGroup(line, ticks, labs)


def make_counter(g, fmt, pos, color=TEXT, size=28, align=LEFT):
    t = T(fmt(int(g.get_value() + 1e-6)), size, color)
    t.cur = int(g.get_value() + 1e-6)
    t.move_to(pos, aligned_edge=align)

    def u(m):
        v = int(g.get_value() + 1e-6)
        if v != m.cur:
            m.cur = v
            m.become(T(fmt(v), size, color).move_to(pos, aligned_edge=align))
    t.add_updater(u)
    return t


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


def run_g(g, rate, gmax):
    def u(m, dt):
        m.set_value(min(m.get_value() + rate * dt, gmax))
    g.add_updater(u)


def pos_of(arr, g, i, ph, bob=0.03):
    gv = min(g.get_value(), arr.shape[1] - 1.001)
    k = int(gv)
    fr = gv - k
    p = arr[i, k] * (1 - fr) + arr[i, k + 1] * fr
    return [sx(p), LANES[i] + bob * np.sin(ph), 0]


def make_dots(arr, g, r=0.12):
    dots = VGroup()
    for i in range(len(arr)):
        d = Circle(radius=r, stroke_width=2, stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.22)
        d.st = 0
        d.ph = i * 0.9
        d.idx = i

        def u(m, dt):
            m.ph += dt * 1.6
            m.move_to(pos_of(arr, g, m.idx, m.ph))
            gv = min(g.get_value(), arr.shape[1] - 1.001)
            a = arr[m.idx, int(gv)]
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
        d.move_to(pos_of(arr, g, i, d.ph))
        dots.add(d)
    return dots


def make_fly(s=1.0, detail=False):
    body = Ellipse(width=0.5, height=0.26, stroke_width=0, fill_color=FLYC, fill_opacity=1)
    head = Circle(radius=0.13, stroke_width=0, fill_color=FLYC, fill_opacity=1).move_to([0.29, 0.03, 0])
    eye = Circle(radius=0.075, stroke_width=0, fill_color="#A3412A", fill_opacity=1).move_to([0.33, 0.06, 0])
    wing = Ellipse(width=0.38, height=0.16, stroke_color="#DDE3EA", stroke_width=0.8, fill_color=WHITE, fill_opacity=0.55)
    wing.rotate(0.5).move_to([-0.04, 0.16, 0])
    parts = [body, wing, head, eye]
    if detail:
        legs = VGroup(*[Line([x, -0.1, 0], [x + dx, -0.24, 0], stroke_color="#8C7650", stroke_width=3) for x, dx in ((-0.12, -0.08), (0.03, 0.0), (0.16, 0.08))])
        stripes = VGroup(*[Line([x, -0.12, 0], [x, 0.12, 0], stroke_color="#6A5535", stroke_width=3) for x in (-0.18, -0.08, 0.02)])
        parts = [legs, body, stripes, wing, head, eye]
    f = VGroup(*parts).scale(s)
    f.wing = wing
    f.eye = eye
    return f


def flutter(f, speed=9.0):
    f.t = 0.0

    def u(m, dt):
        m.t += dt
        m.wing.set_fill(opacity=0.35 + 0.25 * np.sin(m.t * speed))
    f.add_updater(u)
    return f


def make_bottle(H=1.0, stripe=False, sw=None):
    w, bh = 0.62 * H, 0.8 * H
    sw = sw if sw is not None else max(1.5, 2.5 * H)
    body = RoundedRectangle(corner_radius=0.12 * H, width=w, height=bh, stroke_color=GLASS, stroke_width=sw, fill_color=GLASS, fill_opacity=0.12)
    neck = Rectangle(width=0.34 * H, height=0.2 * H, stroke_color=GLASS, stroke_width=sw, fill_color=GLASS, fill_opacity=0.12).next_to(body, UP, buff=0)
    parts = []
    W = w - 0.09 * H
    mh = 0.2 * H
    my = body.get_bottom()[1] + 0.05 * H + mh / 2
    bot = VGroup()
    if stripe:
        gold = Rectangle(width=W / 2, height=mh, stroke_width=0, fill_color=GB, fill_opacity=0.95).move_to([body.get_center()[0] - W / 4, my, 0])
        blue = Rectangle(width=W / 2, height=mh, stroke_width=0, fill_color=BB, fill_opacity=0.95).move_to([body.get_center()[0] + W / 4, my, 0])
        parts = [gold, blue, body, neck]
        bot = VGroup(*parts)
        bot.gold, bot.blue = gold, blue
        bot.sw_left = body.get_center()[0] - W / 2
        bot.sw_w = W
        bot.sw_y = my
    else:
        media = Rectangle(width=W, height=mh, stroke_width=0, fill_color=MEDIA, fill_opacity=0.9).move_to([body.get_center()[0], my, 0])
        plug = Rectangle(width=0.4 * H, height=0.1 * H, stroke_width=0, fill_color="#E8D3A8", fill_opacity=1).next_to(neck, UP, buff=-0.03 * H)
        bot = VGroup(media, body, neck, plug)
    bot.body = body
    bot.H = H
    return bot


def set_frac(b, f):
    f = float(np.clip(f, 0.02, 0.98))
    g, bl = b.gold, b.blue
    g.stretch_to_fit_width(b.sw_w * f)
    g.move_to([b.sw_left + b.sw_w * f / 2, b.sw_y, 0])
    bl.stretch_to_fit_width(b.sw_w * (1 - f))
    bl.move_to([b.sw_left + b.sw_w * f + b.sw_w * (1 - f) / 2, b.sw_y, 0])


def swarm(bottle, n, fs, seed, orbit=None, grid=False):
    """Flies that move around inside a bottle (computed positions are decorative, not data)."""
    rng = np.random.default_rng(seed)
    bc = bottle.body.get_center()
    H = bottle.H
    iw = 0.62 * H - 0.3 * H * (1.0 if not grid else 0.6)
    ih = 0.8 * H - 0.5 * H
    flies = VGroup()
    cols = int(np.ceil(np.sqrt(n)))
    for i in range(n):
        f = make_fly(fs)
        if grid:
            r_, c_ = divmod(i, cols)
            cx = bc[0] + (c_ - (cols - 1) / 2) * (iw / cols) * 1.1
            cy = bc[1] + 0.1 * H + ((cols - 1) / 2 - r_) * (ih / cols) * 1.15
            ax_, ay_ = (orbit or 0.12), (orbit or 0.12)
        else:
            cx = bc[0] + rng.uniform(-iw / 2, iw / 2) * 0.9
            cy = bc[1] + 0.08 * H + rng.uniform(-ih / 2, ih / 2) * 0.9
            ax_, ay_ = iw * 0.3, ih * 0.22
        f.c = (cx, cy)
        f.a = (ax_, ay_)
        f.w = (rng.uniform(0.8, 1.7), rng.uniform(0.9, 1.9))
        f.p = (rng.uniform(0, 6.28), rng.uniform(0, 6.28))
        f.t = 0.0
        f.move_to([cx, cy, 0])

        def u(m, dt):
            m.t += dt
            m.move_to([m.c[0] + m.a[0] * np.sin(m.w[0] * m.t + m.p[0]), m.c[1] + m.a[1] * np.sin(m.w[1] * m.t + m.p[1]), 0])
            m.wing.set_fill(opacity=0.35 + 0.25 * np.sin(m.t * 9 + m.p[0]))
        f.add_updater(u)
        flies.add(f)
    return flies


def make_hist(g, grow=None):
    bars = VGroup()
    for j in range(17):
        b = VMobject()
        b.j = j
        b.edge = j in (0, 16)
        b.hidden = None
        bars.add(b)

    def style(b, on):
        if b.hidden == (not on):
            return
        b.hidden = not on
        if on:
            b.set_fill(GB, 0.95)
            b.set_stroke(TEXT if b.edge else "#8A6A1C", 4 if b.edge else 2, 1.0)
        else:
            b.set_fill(GB, 0.0)
            b.set_stroke(TEXT, 0, 0.0)

    def upd(m):
        gv = g.get_value()
        c = interp(COUNTS, gv)
        sc = HMAX / float(interp(YM.reshape(-1, 1), gv)[0])
        gr = grow.get_value() if grow is not None else 1.0
        for b in m:
            h = c[b.j] * sc * gr
            x = sx(b.j / 16)
            hw = 0.31
            if h < 0.03:
                style(b, False)
                b.set_points_as_corners([[x - hw, AX_Y, 0], [x + hw, AX_Y, 0], [x + hw, AX_Y + 0.001, 0], [x - hw, AX_Y + 0.001, 0], [x - hw, AX_Y, 0]])
            else:
                style(b, True)
                b.set_points_as_corners([[x - hw, AX_Y, 0], [x + hw, AX_Y, 0], [x + hw, AX_Y + h, 0], [x - hw, AX_Y + h, 0], [x - hw, AX_Y, 0]])
    bars.add_updater(upd)
    upd(bars)
    return bars


def bar_ring(bar, color=TEXT, w=4, buff=0.08):
    r = VMobject()

    def u(m):
        pts = bar.points
        if len(pts) == 0:
            return
        x0, x1 = pts[:, 0].min() - buff, pts[:, 0].max() + buff
        y0, y1 = pts[:, 1].min() - buff, pts[:, 1].max() + buff
        m.set_points_as_corners([[x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0], [x0, y0, 0]])
        m.set_stroke(color, w, 1.0).set_fill(opacity=0)
    r.add_updater(u)
    u(r)
    return r


def ring_on(mob, color=TEXT, r=0.3, w=4):
    c = Circle(radius=r, stroke_color=color, stroke_width=w)
    c.add_updater(lambda m: m.move_to(mob.get_center()))
    return c


def pulse(mob, base=1.0, amp=0.18, speed=3.0):
    mob.pt = 0.0
    mob.pb = mob.get_height()

    def u(m, dt):
        m.pt += dt
        m.set_height(m.pb * (base + amp * (0.5 + 0.5 * np.sin(m.pt * speed))))
    mob.add_updater(u)
    return mob


def ripple(mob_center_fn, color=TEXT, period=1.6, r0=0.2, r1=0.55):
    c = Circle(radius=r0, stroke_color=color, stroke_width=4)
    c.tt = 0.0

    def u(m, dt):
        m.tt += dt
        ph = (m.tt % period) / period
        m.become(Circle(radius=r0 + (r1 - r0) * ph, stroke_color=color, stroke_width=4, stroke_opacity=1 - ph).move_to(mob_center_fn()))
    c.add_updater(u)
    c.move_to(mob_center_fn())
    return c


def note_label(txt="bars: illustration built with Buri's estimate,\nNe = 9.0; not his data"):
    return T(txt, 22, TEXT, line_spacing=0.8).move_to([-6.6, 3.42, 0], aligned_edge=LEFT)


def scale_label(g):
    t = T("full height = 107 lines", 22, TEXT)
    t.cur = 107

    def u(m):
        v = int(round(float(interp(YM.reshape(-1, 1), g.get_value())[0])))
        if v != m.cur:
            m.cur = v
            m.become(T(f"full height = {v} lines", 22, TEXT).move_to([6.6, 3.45, 0], aligned_edge=RIGHT))
    t.add_updater(u)
    t.move_to([6.6, 3.45, 0], aligned_edge=RIGHT)
    return t


def check_mark(s=1.0):
    return VMobject(stroke_color=TEXT, stroke_width=14).set_points_as_corners([[-0.55 * s, 0.0, 0], [-0.15 * s, -0.42 * s, 0], [0.6 * s, 0.5 * s, 0]])


# graph geometry for the single-line plot (scenes 2 and 16)
GX0, GW, GY0, GH = -2.6, 8.4, -2.5, 5.0


def gx(gen):
    return GX0 + GW * gen / 19.0


def gy(p):
    return GY0 + GH * p


def make_graph(labels=True):
    ax = VGroup(Line([GX0, GY0, 0], [GX0 + GW + 0.2, GY0, 0], stroke_color=TEXT, stroke_width=3),
                Line([GX0, GY0, 0], [GX0, GY0 + GH + 0.2, 0], stroke_color=TEXT, stroke_width=3))
    mid = DashedLine([GX0, gy(0.5), 0], [GX0 + GW, gy(0.5), 0], color=GREY, stroke_width=2)
    labs = VGroup()
    if labels:
        labs = VGroup(T("0", 28).move_to([GX0 - 0.35, gy(0), 0]), T("0.5", 28).move_to([GX0 - 0.5, gy(0.5), 0]), T("1", 28).move_to([GX0 - 0.35, gy(1), 0]),
                      T("0", 28).move_to([gx(0), GY0 - 0.4, 0]), T("10", 28).move_to([gx(10), GY0 - 0.4, 0]), T("19", 28).move_to([gx(19), GY0 - 0.4, 0]),
                      T("generation", 28).move_to([GX0 + GW / 2, GY0 - 0.85, 0]),
                      T("frequency of gold", 28, GB).rotate(PI / 2).move_to([GX0 - 1.15, gy(0.5), 0]))
    return VGroup(ax, mid, labs)


def make_line(gl):
    line = VMobject(stroke_color=TEXT, stroke_width=6)
    head = Dot(radius=0.13, color=GB)

    def u(m):
        v = min(gl.get_value(), 19.0)
        k = int(min(v, 18))
        pts = [[gx(i), gy(ONE_LINE[i]), 0] for i in range(k + 1)]
        fr = v - k
        if fr > 0 and k < 19:
            pts.append([gx(k + fr), gy(ONE_LINE[k] * (1 - fr) + ONE_LINE[k + 1] * fr), 0])
        if len(pts) < 2:
            pts.append([pts[0][0] + 0.001, pts[0][1], 0])
        line.set_points_as_corners(pts)
        head.move_to(pts[-1])
    grp = VGroup(line, head)
    grp.add_updater(u)
    u(grp)
    return grp


class HW(SpokenScene):
    """Scene with the histogram world: axis, bars, triangle, note and scale label."""

    def hist_world(self, g0=0.0, grow=None, counter=True, tri=True, note=True, note_txt=None):
        self.g = ValueTracker(g0)
        self.add(self.g)
        self.axis = make_axis()
        self.hist = make_hist(self.g, grow)
        self.tri = make_tri(SIM, self.g)
        self.add(self.axis, self.hist)
        if tri:
            self.add(self.tri)
        self.ctr = make_counter(self.g, lambda v: f"generation {v}", [-6.6, 2.55, 0], align=LEFT)
        if counter:
            self.add(self.ctr)
        self.note = note_label(note_txt) if note_txt else note_label()
        self.sl = scale_label(self.g)
        if note:
            self.add(self.note, self.sl)
        return self


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Drift, Gene Flow and Competing Explanations"
    TITLE = "107 Bottles"


class S01Link(SpokenScene):
    def construct(self):
        g = ValueTracker(0.0)
        self.add(g)
        axis = make_axis()
        dots = make_dots(A_SIM, g)
        tri = make_tri(A_SIM, g)
        xs = (-4.4, -2.2, 0.0, 2.2, 4.4)
        bags = VGroup()
        for j, x in enumerate(xs):
            bag = RoundedRectangle(corner_radius=0.3, width=1.7, height=1.4, stroke_color="#C9A27A", stroke_width=3, fill_color="#6B4F36", fill_opacity=0.5)
            bag.move_to([x, 2.1, 0])
            beads = VGroup(*[Circle(radius=0.105, stroke_color=BG, stroke_width=1.2, fill_color=GB if (r * 5 + c + j) % 2 == 0 else BB, fill_opacity=1).move_to([x - 0.65 + c * 0.325, 2.55 - r * 0.3, 0])
                             for r in range(4) for c in range(5)])
            bags.add(VGroup(bag, beads))
        ctr = make_counter(g, lambda v: f"generation {v}", [-6.4, 0.7, 0])
        cp = T("computed: bead model", 28, TEXT).move_to([6.4, 0.7, 0], aligned_edge=RIGHT)
        self.add(axis, dots, tri, bags, ctr, cp)
        run_g(g, 1.7, 40)
        self.wait(0.5)
        lab = T("many populations", 32, PURPLE).move_to([0, 3.5, 0])
        self.at("many populations")
        self.play(FadeIn(lab, shift=DOWN * 0.2), run_time=0.7)
        # beads dissolve into flies
        flies = VGroup()
        for i in range(40):
            f = make_fly(0.55)
            f.i = i
            f.ph = i * 0.9
            f.t = 0.0

            def u(m, dt):
                m.ph += dt * 1.6
                m.t += dt
                m.move_to(pos_of(A_SIM, g, m.i, m.ph))
                m.wing.set_fill(opacity=0.35 + 0.25 * np.sin(m.t * 9 + m.i))
            f.add_updater(u)
            f.move_to(pos_of(A_SIM, g, i, f.ph))
            f.set_opacity(0)
            flies.add(f)
        bottles = VGroup(*[make_bottle(1.5).move_to([x, 2.15, 0]) for x in xs])
        self.add(flies)
        self.at("real animals")
        lab2 = T("real animals", 32, TEXT).move_to([0, 3.5, 0])
        for f in flies:
            f.wing.set_fill(WHITE, 0.55)
        self.play(FadeOut(bags, scale=0.85), FadeIn(bottles, scale=1.15), FadeOut(dots), Transform(lab, lab2),
                  *[f.animate.set_opacity(1) for f in flies], run_time=0.9)
        self.at("spread apart")
        run_g(g, 0.0, 40)
        g.clear_updaters()
        run_g(g, 0.45, 40)
        tl = follow(T("average", 28, TEXT), tri, dx=0.4)
        self.at("average left alone")
        self.play(FadeIn(tl), Indicate(tri, scale_factor=1.8, color=WHITE), run_time=1.0)
        self.finish()


class S02One(SpokenScene):
    def construct(self):
        bot = make_bottle(3.0).move_to([A_X, 0.0, 0])
        fl = swarm(bot, 7, 0.6, 3)
        gr = make_graph()
        gl = ValueTracker(0.0)
        line = make_line(gl)
        self.add(gl)
        self.play(FadeIn(bot, scale=0.8), FadeIn(fl), Create(gr[0]), Create(gr[1]), run_time=1.2)
        self.play(FadeIn(gr[2]), FadeIn(line), run_time=0.8)
        lb = T("one bottle", 28).move_to([A_X, -2.35, 0])
        q = T("?", 64, TEXT, weight=BOLD).move_to([A_X, 2.35, 0])
        self.at("could not tell")
        self.play(FadeIn(lb), FadeIn(q, scale=1.4), run_time=0.8)
        self.at("follow one line alone")
        self.play(FadeOut(q), gl.animate.set_value(3.0), run_time=1.9, rate_func=linear)
        self.at("it climbs")
        self.play(gl.animate.set_value(8.0), run_time=1.0, rate_func=linear)
        self.at("dips")
        self.play(gl.animate.set_value(11.0), run_time=0.55, rate_func=linear)
        self.at("climbs again")
        self.play(gl.animate.set_value(19.0), run_time=1.8, rate_func=linear)
        qh = T("?", 64, TEXT, weight=BOLD).move_to([gx(19) + 0.4, gy(ONE_LINE[19]) + 0.5, 0])
        self.at("was it pushed")
        c1 = chip("pushed?", GREEN_C, 32).move_to([1.2, 3.3, 0])
        self.play(FadeIn(qh, scale=1.4), FadeIn(c1, shift=UP * 0.2), run_time=0.7)
        c2 = chip("luck?", PURPLE, 32).move_to([3.7, 3.3, 0])
        self.at("luck")
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S03Buri(SpokenScene):
    def construct(self):
        bot = make_bottle(3.0).move_to([A_X, 0.0, 0])
        fl = swarm(bot, 7, 0.6, 3)
        self.add(bot, fl)
        card = chip("Peter Buri, Evolution, 1956", TEXT, 34).move_to([0.3, 3.2, 0])
        self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.8)
        self.at("real experiment")
        self.play(Indicate(bot, scale_factor=1.05, color=GLASS), run_time=1.0)
        fly = make_fly(7.0, detail=True).move_to([-0.6, -0.2, 0])
        flutter(fly)
        self.at("fruit flies")
        self.play(FadeIn(fly, scale=0.6), run_time=1.0)
        eye_c = fly.eye.get_center()
        gb = Circle(radius=0.2, stroke_color=BG, stroke_width=1.2, fill_color=GB, fill_opacity=1).move_to([2.4, -0.9, 0])
        bb = Circle(radius=0.2, stroke_color=BG, stroke_width=1.2, fill_color=BB, fill_opacity=1).move_to([2.4, -1.9, 0])
        gl = T("gold allele", 32, GB).next_to(gb, RIGHT, buff=0.3)
        bl = T("blue allele", 32, BB).next_to(bb, RIGHT, buff=0.3)
        self.at("two alleles")
        self.play(FadeIn(gb, scale=1.6), FadeIn(gl), run_time=0.7)
        self.play(FadeIn(bb, scale=1.6), FadeIn(bl), run_time=0.7)
        ring = Circle(radius=0.42, stroke_color=TEXT, stroke_width=5).move_to(eye_c)
        self.at("eye color")
        self.play(Create(ring), run_time=0.8)
        lab = T("two alleles at the\nbrown eye-colour locus", 30, TEXT, line_spacing=0.8).move_to([3.9, 1.6, 0])
        ln = Line(ring.get_right() + RIGHT * 0.05, lab.get_left() + LEFT * 0.15, stroke_color=TEXT, stroke_width=3)
        self.at("brown locus")
        self.play(Create(ln), FadeIn(lab, shift=LEFT * 0.2), run_time=0.9)
        self.play(Indicate(ring, scale_factor=1.4, color=GB), run_time=1.0)
        self.finish()


def rack_pos(i, cols=11):
    r, c = divmod(i, cols)
    return [1.35 + 0.5 * c, 2.95 - 0.56 * r, 0]


def make_rack():
    rack = VGroup()
    for i in range(107):
        b = make_bottle(0.5, stripe=True, sw=1.5)
        p = rack_pos(i)
        b.move_to(p)
        b.sw_left += p[0] - 0.0 if False else 0
        rack.add(b)
    return rack


def build_rack():
    rack = VGroup()
    for i in range(107):
        b = make_bottle(0.5, stripe=True, sw=1.5)
        c0 = b.get_center()
        p = rack_pos(i)
        dx, dy = p[0] - c0[0], p[1] - c0[1]
        b.shift([dx, dy, 0])
        b.sw_left += dx
        b.sw_y += dy
        b.row = i // 11
        b.idx = i
        rack.add(b)
    return rack


class S04Setup(SpokenScene):
    def construct(self):
        bot = make_bottle(3.0).move_to([A_X, -0.3, 0])
        fl = swarm(bot, 16, 0.4, 5, orbit=0.1, grid=True)
        self.add(bot, fl)
        bw = 3.0
        gold = Rectangle(width=bw / 2, height=0.5, stroke_width=0, fill_color=GB, fill_opacity=1)
        blue = Rectangle(width=bw / 2, height=0.5, stroke_width=0, fill_color=BB, fill_opacity=1)
        bar = VGroup(gold, blue).arrange(RIGHT, buff=0).move_to([A_X, 2.5, 0])
        st = T("start: 0.5", 30).move_to([A_X, 3.3, 0])
        self.wait(0.3)
        self.at("one half gold")
        self.play(GrowFromEdge(gold, LEFT), FadeIn(blue), FadeIn(st), run_time=1.2)
        # parents
        glows = VGroup(*[Circle(radius=0.2, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.3) for _ in fl])
        for gcirc, f in zip(glows, fl):
            gcirc.add_updater(lambda m, f=f: m.move_to(f.get_center()))
            gcirc.move_to(f.get_center())
        xs = (-2.0, 0.6, 3.2, 5.6)
        chain = [make_bottle(2.0).move_to([x, -0.3, 0]) for x in xs]
        arrows = [Arrow([a + 0.75, -0.3, 0], [b - 0.75, -0.3, 0], buff=0, color=TEXT, stroke_width=5, max_tip_length_to_length_ratio=0.3)
                  for a, b in zip((A_X + 0.0,) + xs[:-1], xs)]
        arrows[0] = Arrow([A_X + 1.15, -0.3, 0], [xs[0] - 0.85, -0.3, 0], buff=0, color=TEXT, stroke_width=5, max_tip_length_to_length_ratio=0.3)
        labs = [T(t, 28).move_to([x, -1.9, 0]) for t, x in zip(("generation 1", "2", "3", "19"), xs)]
        dots3 = T("...", 36).move_to([4.4, -0.3, 0])
        gen = T("19 generations", 32, TEXT).move_to([1.8, 1.6, 0])
        self.at("each generation")
        self.play(FadeIn(chain[0], scale=0.8), GrowArrow(arrows[0]), FadeIn(labs[0]), FadeIn(gen), run_time=1.0)
        par = T("16 parents\neach generation", 30, TEXT, line_spacing=0.8).move_to([A_X, -2.85, 0])
        self.at("picked 16 flies")
        self.play(LaggedStart(*[FadeIn(gc, scale=1.8) for gc in glows], lag_ratio=0.05), FadeIn(par), run_time=1.3)
        self.at("parents of the next")
        copies = VGroup(*[make_fly(0.4) for _ in range(16)])
        rng = np.random.default_rng(1)
        for f, cpy in zip(fl, copies):
            cpy.move_to(f.get_center())
        self.add(copies)
        self.play(*[c.animate.move_to([xs[0] + rng.uniform(-0.3, 0.3), -0.15 + rng.uniform(-0.45, 0.35), 0]) for c in copies], run_time=1.0)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(arrows[i]), FadeIn(chain[i], scale=0.8), FadeIn(labs[i])) for i in (1, 2, 3)], lag_ratio=0.4), run_time=1.1)
        rack = build_rack()
        cnt = ValueTracker(0)
        self.add(cnt)
        ct = make_counter(cnt, lambda v: f"{v} lines", [3.8, -3.1, 0], size=36, align=ORIGIN)
        self.at("his first series")
        self.play(*[FadeOut(m) for m in (*chain, *arrows, *labs, copies, gen, glows, bar, st)], run_time=0.6)
        self.add(ct)
        self.play(LaggedStart(*[FadeIn(r, scale=0.6) for r in rack], lag_ratio=0.012), cnt.animate.set_value(107), run_time=1.9, rate_func=linear)
        self.finish()


class S05Same(SpokenScene):
    def construct(self):
        bot = make_bottle(3.0).move_to([A_X, -0.3, 0])
        fl = swarm(bot, 16, 0.38, 5, orbit=0.1, grid=True)
        par = T("16 parents\neach generation", 30, TEXT, line_spacing=0.8).move_to([A_X, -2.85, 0])
        rack = build_rack()
        cnt = ValueTracker(107)
        ct = make_counter(cnt, lambda v: f"{v} lines", [3.8, -3.1, 0], size=36, align=ORIGIN)
        self.add(bot, fl, par, rack, ct)
        dv = ValueTracker(0.0)
        self.add(dv)
        diffs = SIM[:, 5] - 0.5

        def rup(m):
            for b in m:
                set_frac(b, 0.5 + dv.get_value() * diffs[b.idx])
        rack.add_updater(rup)
        wave = ValueTracker(-1.0)
        self.add(wave)

        def wup(m):
            w = wave.get_value()
            for b in m:
                d = abs(b.row - w)
                b.body.set_stroke(TEXT if d < 1.2 else GLASS, 3 if d < 1.2 else 1.5)
        rack.add_updater(wup)
        self.wait(0.3)
        lab = T("same start,\nsame conditions", 30, TEXT, line_spacing=0.8).move_to([A_X, -2.85, 0])
        self.at("set up the same way")
        self.play(FadeOut(par, run_time=0.3), wave.animate.set_value(10.5), run_time=1.6, rate_func=linear)
        self.add(lab)
        self.at("kept the same way")
        wave.set_value(-1.0)
        self.play(wave.animate.set_value(10.5), run_time=1.5, rate_func=linear)
        chk = check_mark(1.0).move_to([A_X, 2.55, 0])
        self.play(Create(chk), run_time=0.8)
        wave.set_value(-5.0)
        c1 = chip("chance alone", PURPLE, 32).move_to([A_X, 3.45, 0])
        self.at("chance alone")
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.7)
        lab2 = T("later (computed):\nbottles differ", 30, TEXT, line_spacing=0.8).move_to([A_X, -2.85, 0])
        self.at("differences")
        self.remove(lab)
        self.add(lab2)
        self.play(dv.animate.set_value(1.0), run_time=2.2)
        self.play(Indicate(rack, scale_factor=1.03, color=PURPLE), run_time=1.0)
        self.finish()


class S06Hist(HW):
    def construct(self):
        # rebuild the end of the last scene, then the rack drops into the first bar
        bot = make_bottle(3.0).move_to([A_X, -0.3, 0])
        fl = swarm(bot, 16, 0.38, 5, orbit=0.1, grid=True)
        rack = build_rack()
        diffs = SIM[:, 5] - 0.5
        dv = ValueTracker(1.0)
        self.add(dv)
        rack.add_updater(lambda m: [set_frac(b, 0.5 + dv.get_value() * diffs[b.idx]) for b in m])
        cnt = ValueTracker(107)
        ct = make_counter(cnt, lambda v: f"{v} lines", [3.8, -3.1, 0], size=36, align=ORIGIN)
        self.add(bot, fl, rack, ct)
        grow = ValueTracker(0.0)
        self.hist_world(0.0, grow, counter=False, tri=False, note=False)
        self.add(self.g)
        self.remove(self.axis, self.hist)
        self.play(FadeOut(bot), FadeOut(fl), FadeOut(ct), dv.animate.set_value(0.0), FadeIn(self.axis), run_time=0.5)
        self.add(self.hist)
        tgt = [sx(0.5), AX_Y + 0.3, 0]
        self.at("stack all the lines")
        self.play(LaggedStart(*[b.animate.scale(0.3).move_to(tgt).set_opacity(0) for b in rack], lag_ratio=0.012), grow.animate.set_value(1.0), run_time=2.4)
        self.remove(rack)
        self.add(self.note, self.sl)
        self.play(FadeIn(self.note), FadeIn(self.sl), run_time=0.5)
        top = T("107 lines", 34, GB).move_to([0, AX_Y + HMAX + 0.4, 0])
        ring = bar_ring(self.hist[8], TEXT, 4)
        self.at("each bar counts")
        self.play(FadeIn(ring), FadeIn(top, shift=DOWN * 0.2), run_time=0.7)
        bl = T("bar height = number of lines", 30, TEXT).move_to([3.4, 1.3, 0])
        self.play(FadeIn(bl, shift=LEFT * 0.2), run_time=0.8)
        self.at("frequency")
        self.play(Indicate(self.axis[2][3], scale_factor=1.2, color=GB), run_time=1.0)
        ctr = make_counter(self.g, lambda v: f"generation {v}", [-6.6, 2.55, 0], align=LEFT)
        self.at("at the start")
        self.play(FadeOut(bl), FadeIn(ctr), FadeIn(self.tri, shift=UP * 0.3), run_time=0.8)
        self.add(self.tri)
        mid = T("every line: middle bar", 30, TEXT).move_to([3.3, 0.4, 0])
        self.at("every line")
        self.play(Indicate(ring, scale_factor=1.1, color=GB), FadeIn(mid), run_time=1.0)
        self.at("middle bar")
        self.play(Indicate(self.tri, scale_factor=1.9, color=WHITE), run_time=1.0)
        self.finish()


class S07Spread(HW):
    def construct(self):
        self.hist_world(0.0)
        self.wait(0.3)
        run_g(self.g, 0.9, 10.0)
        dbl = DoubleArrow([-1.6, 2.5, 0], [1.6, 2.5, 0], buff=0, color=PURPLE, stroke_width=6, max_tip_length_to_length_ratio=0.12)
        self.at("the pile flattens")
        self.wait(0.8)
        self.at("lines drift up and down")
        self.play(GrowFromCenter(dbl), run_time=0.8)
        tg = T("all gold", 30, GB).move_to([5.9, 2.2, 0])
        tb = T("all blue", 30, BB).move_to([-5.9, 2.2, 0])
        rr = bar_ring(self.hist[16], GB, 5)
        rl = bar_ring(self.hist[0], BB, 5)
        self.at("some lose blue entirely")
        self.play(FadeOut(dbl), FadeIn(tg), FadeIn(rr), run_time=0.6)
        self.at("some lose gold")
        self.play(FadeIn(tb), FadeIn(rl), run_time=0.6)
        fx = chip("fixed or lost", PURPLE, 32).move_to([0, 2.55, 0])
        self.at("those stay at the edges")
        self.play(FadeIn(fx, scale=1.3), run_time=0.6)
        self.play(Indicate(rr, scale_factor=1.15, color=TEXT), Indicate(rl, scale_factor=1.15, color=TEXT), run_time=0.9)
        self.finish()


class S08Predict(HW):
    def construct(self):
        self.hist_world(10.0)
        er = bar_ring(self.hist[16], TEXT, 4)
        el = bar_ring(self.hist[0], TEXT, 4)
        self.add(er, el)
        er.tt = 0.0
        er.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.set_stroke(opacity=0.4 + 0.6 * abs(np.sin(m.tt * 2.2)))))
        el.tt = 0.0
        el.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.set_stroke(opacity=0.4 + 0.6 * abs(np.sin(m.tt * 2.2)))))
        loop = Rectangle(width=0.5, height=HMAX + 0.3, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to([-6.0, AX_Y + HMAX / 2, 0])
        loop.tt = 0.0
        loop.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.set_x(-6.0 + 12.0 * ((m.tt % 3.2) / 3.2))))
        self.add(loop)
        self.at("by generation 10")
        self.play(Indicate(self.ctr, scale_factor=1.2, color=GB), run_time=1.0)
        self.at("edges are filling up")
        self.play(Indicate(er, scale_factor=1.1, color=GB), Indicate(el, scale_factor=1.1, color=BB), run_time=1.2)
        rp = ripple(lambda: self.tri.get_center(), TEXT)
        self.at("white triangle")
        self.play(FadeOut(er), FadeOut(el), run_time=0.3)
        self.remove(er, el)
        self.add(rp)
        self.play(Indicate(self.tri, scale_factor=1.9, color=WHITE), run_time=0.9)
        lab = follow(T("pooled frequency", 28, TEXT), self.tri, dx=0.65)
        self.at("pooled frequency")
        self.play(FadeIn(lab), run_time=0.5)
        self.at("across all lines")
        self.play(Indicate(self.hist[8], scale_factor=1.0, color=TEXT), run_time=1.0)
        q = T("next: generation 19?", 28, TEXT).move_to([-6.6, 2.0, 0], aligned_edge=LEFT)
        self.at("by generation 19")
        self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=0.6)
        c1 = chip("up", TEXT, 30).move_to([-1.2, 2.55, 0])
        c2 = chip("down", TEXT, 30).move_to([0.8, 2.55, 0])
        c3 = chip("still 0.5", TEXT, 30).move_to([3.3, 2.55, 0])
        self.at("be up")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.5)
        self.at("down")
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.5)
        self.at("or still")
        self.play(FadeIn(c3, shift=UP * 0.2), run_time=0.5)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        g = ValueTracker(10.0)
        self.add(g)
        axis = make_axis()
        hist = make_hist(g)
        tri = make_tri(SIM, g)
        ctr = make_counter(g, lambda v: f"generation {v}", [-6.6, 2.55, 0], align=LEFT)
        note = note_label()
        sl = scale_label(g)
        lab = follow(T("pooled frequency", 28, TEXT), tri, dx=0.65)
        rp = ripple(lambda: tri.get_center(), TEXT)
        cap = T("Predict: where is the triangle at generation 19?", 30, TEXT).move_to([0.6, 1.95, 0])
        self.add(axis, hist, tri, ctr, note, sl, lab, rp, cap)
        for n in (5, 4, 3, 2, 1):
            tm = T(str(n), 64, GB, weight=BOLD).move_to([4.6, -3.1, 0])
            self.add(tm)
            self.play(Indicate(tm, scale_factor=1.25, color=GB), run_time=0.95)
            self.wait(0.05)
            self.remove(tm)
        self.finish()


class S10Reveal(HW):
    def construct(self):
        self.hist_world(10.0)
        run_g(self.g, 1.0, 19.0)
        rp = ripple(lambda: self.tri.get_center(), TEXT)
        lab = follow(T("pooled frequency", 28, TEXT), self.tri, dx=0.65)
        self.add(rp, lab)
        self.at("still at about one half")
        self.play(Indicate(self.tri, scale_factor=1.9, color=WHITE), run_time=1.0)
        c1 = chip("many ended with one allele", PURPLE, 30).move_to([0.6, 2.55, 0])
        rr = bar_ring(self.hist[16], GB, 5)
        rl = bar_ring(self.hist[0], BB, 5)
        self.at("by then")
        self.play(FadeIn(c1, scale=1.2), FadeIn(rr), FadeIn(rl), run_time=0.7)
        self.at("yet the pooled frequency")
        self.play(FadeOut(c1), FadeOut(rr), FadeOut(rl), run_time=0.5)
        tag = chip("about 0.5: no systematic change", GB, 30).move_to([0.8, 2.55, 0])
        self.at("no systematic change")
        self.play(FadeIn(tag, scale=1.2), Indicate(self.tri, scale_factor=1.9, color=WHITE), run_time=1.0)
        self.finish()


class S11Signature(HW):
    def construct(self):
        self.hist_world(19.0)
        rp = ripple(lambda: self.tri.get_center(), TEXT)
        self.add(rp)
        ln = Line([-6.3, 1.85, 0], [6.3, 1.85, 0], stroke_color=PURPLE, stroke_width=5)
        tl = Line([-6.3, 1.7, 0], [-6.3, 2.0, 0], stroke_color=PURPLE, stroke_width=5)
        tr = Line([6.3, 1.7, 0], [6.3, 2.0, 0], stroke_color=PURPLE, stroke_width=5)
        sp = T("spread: grew", 32, PURPLE).move_to([0, 1.3, 0])
        self.play(FadeOut(self.ctr), run_time=0.3)
        self.at("spread without a push")
        self.play(Create(ln), Create(tl), Create(tr), FadeIn(sp, shift=DOWN * 0.2), run_time=1.0)
        mean_x = self.tri.get_center()[0]
        dash = DashedLine([mean_x, AX_Y - 0.1, 0], [mean_x, -0.2, 0], color=TEXT, stroke_width=4)
        av = T("average: no systematic change", 32, TEXT).move_to([mean_x, 0.15, 0])
        self.at("on the average")
        self.play(Create(dash), FadeIn(av, shift=DOWN * 0.2), Indicate(self.tri, scale_factor=1.9, color=WHITE), run_time=1.2)
        ban = T("the drift prediction", 44, PURPLE, font=TITLE_FONT).move_to([-1.9, 2.55, 0])
        ul = Line([-5.0, 2.15, 0], [1.2, 2.15, 0], stroke_color=PURPLE, stroke_width=4)
        self.at("that is the pattern drift predicts")
        self.play(FadeIn(ban, scale=1.2), GrowFromCenter(ul), Flash(ban, color=PURPLE, flash_radius=0.9, line_length=0.3), run_time=1.1)
        fly = make_fly(1.0, detail=True)
        flutter(fly)
        fly.move_to([4.2, 2.55, 0])
        beads = VGroup(Circle(radius=0.17, stroke_color=BG, fill_color=GB, fill_opacity=1), Circle(radius=0.17, stroke_color=BG, fill_color=BB, fill_opacity=1)).arrange(RIGHT, buff=0.1).move_to([5.9, 2.55, 0])
        self.at("now seen in real flies")
        self.play(FadeIn(fly, scale=1.6), run_time=0.7)
        self.at("rather than beads")
        self.play(FadeIn(beads, scale=1.3), Indicate(fly, scale_factor=1.3), run_time=0.9)
        self.finish()


def stopwatch(r=0.45):
    face = Circle(radius=r, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1)
    top = Rectangle(width=0.2, height=0.12, stroke_width=0, fill_color=TEXT, fill_opacity=1).next_to(face, UP, buff=0.0)
    hand = Line(ORIGIN, UP * r * 0.8, stroke_color=GB, stroke_width=5)
    hand.t = 0.0

    def u(m, dt):
        m.t += dt
        m.put_start_and_end_on(face.get_center(), face.get_center() + r * 0.8 * np.array([np.sin(m.t * 3.0), np.cos(m.t * 3.0), 0]))
    hand.add_updater(u)
    grp = VGroup(face, top, hand)
    return grp


class S12Speed(HW):
    def construct(self):
        self.hist_world(0.0)
        self.g.set_value(0.0)
        sw = stopwatch().move_to([-2.4, 2.55, 0])
        self.at("but how fast")
        run_g(self.g, 6.0, 19.0)
        self.play(FadeIn(sw, scale=0.6), run_time=0.6)
        self.wait(1.2)
        self.at("asked how big")
        card = T("how big an ideal population\nwould spread this fast?", 30, TEXT, line_spacing=0.8)
        box = RoundedRectangle(corner_radius=0.14, width=card.width + 0.5, height=card.height + 0.4, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.14)
        cd = VGroup(box, card.move_to(box)).move_to([3.0, 2.55, 0])
        self.play(FadeIn(cd, shift=LEFT * 0.3), run_time=0.8)
        self.at("ideal population")
        self.play(Indicate(card, scale_factor=1.06, color=TEAL), run_time=1.0)
        self.at("spread that fast")
        er = bar_ring(self.hist[16], GB, 5)
        el = bar_ring(self.hist[0], BB, 5)
        self.play(FadeIn(er), FadeIn(el), run_time=0.6)
        self.play(Flash(sw, color=GB, flash_radius=0.8, line_length=0.25), run_time=0.9)
        self.finish()


def ideal_outline(g, color=TEAL):
    outs = VGroup()
    sc = HMAX / float(YM[19])
    for j in range(17):
        h = IDEAL16[j] * sc
        x = sx(j / 16)
        hw = 0.31
        r = VMobject(stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.15)
        r.set_points_as_corners([[x - hw, AX_Y, 0], [x + hw, AX_Y, 0], [x + hw, AX_Y + h, 0], [x - hw, AX_Y + h, 0], [x - hw, AX_Y, 0]])
        outs.add(r)
    return outs


class S13Ghost16(HW):
    def construct(self):
        self.hist_world(19.0)
        outs = ideal_outline(self.g)
        l1 = T("computed: ideal population of 16", 28, TEAL).move_to([3.2, 2.9, 0])
        self.at("here is the spread computed")
        self.play(LaggedStart(*[Create(o) for o in outs], lag_ratio=0.07), run_time=2.0)
        self.at("ideal population of 16")
        self.play(FadeIn(l1, shift=DOWN * 0.2), run_time=0.7)
        loop = Rectangle(width=0.5, height=HMAX + 0.3, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to([-6.0, AX_Y + HMAX / 2, 0])
        loop.tt = 0.0
        loop.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.set_x(-6.0 + 12.0 * ((m.tt % 3.2) / 3.2))))
        self.add(loop)
        l2 = T("ideal 16: slower than Buri's lines", 28, TEXT).move_to([2.9, 2.25, 0])
        er = bar_ring(self.hist[16], GB, 5)
        el = bar_ring(self.hist[0], BB, 5)
        self.at("real lines spread faster")
        self.play(FadeIn(l2, shift=DOWN * 0.2), Indicate(self.hist[8], scale_factor=1.0, color=GB), run_time=1.0)
        self.at("more of them at the edges")
        self.play(FadeIn(er), FadeIn(el), run_time=0.6)
        self.play(Indicate(er, scale_factor=1.15, color=TEXT), Indicate(el, scale_factor=1.15, color=TEXT), run_time=1.0)
        self.finish()


class S14Ghost9(HW):
    def construct(self):
        self.hist_world(19.0)
        outs = ideal_outline(self.g)
        l1 = T("computed: ideal population of 16", 28, TEAL).move_to([3.2, 2.9, 0])
        l2 = T("ideal 16: slower than Buri's lines", 28, TEXT).move_to([2.9, 2.25, 0])
        self.add(outs, l1, l2)
        n2 = note_label("bars: illustration built with Ne = 9.0;\nnot a fit")
        sweep = Rectangle(width=0.5, height=HMAX + 0.3, stroke_width=0, fill_color=GB, fill_opacity=0.2).move_to([-6.0, AX_Y + HMAX / 2, 0])
        self.at("from how fast his own lines")
        self.remove(self.note)
        self.add(n2)
        self.play(FadeOut(outs), FadeOut(l1), FadeOut(l2), sweep.animate.move_to([6.0, AX_Y + HMAX / 2, 0]), run_time=1.8, rate_func=linear)
        self.remove(sweep)
        cardA = T("Buri's mean estimate,\nfirst series: Ne = 9.0", 30, TEAL, line_spacing=0.8)
        boxA = RoundedRectangle(corner_radius=0.14, width=cardA.width + 0.5, height=cardA.height + 0.4, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.14)
        cA = VGroup(boxA, cardA.move_to(boxA)).move_to([3.5, 2.55, 0])
        self.at("estimated about nine")
        self.play(FadeIn(cA, scale=1.2), run_time=0.8)
        cardB = T("16 flies in\neach bottle", 30, TEXT, line_spacing=0.8)
        boxB = RoundedRectangle(corner_radius=0.14, width=cardB.width + 0.5, height=cardB.height + 0.4, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.1)
        cB = VGroup(boxB, cardB.move_to(boxB)).move_to([-1.6, 2.55, 0])
        self.at("they drifted as if")
        self.play(FadeIn(cB, scale=1.2), run_time=0.8)
        cC = chip("as if only 9 flies", TEAL, 30).move_to([-1.6, 1.4, 0])
        self.at("only nine flies")
        self.play(FadeIn(cC, shift=UP * 0.2), Indicate(cA, scale_factor=1.08), run_time=1.0)
        self.finish()


class S15Ne(SpokenScene):
    def construct(self):
        bot = make_bottle(4.0).move_to([-4.2, 0.1, 0])
        fl = swarm(bot, 16, 0.55, 5, orbit=0.12, grid=True)
        cen = T("census: 16 flies", 32, TEXT).move_to([-4.2, -2.75, 0])
        self.play(FadeIn(bot, scale=0.8), FadeIn(fl), FadeIn(cen), run_time=1.0)
        t1 = T("effective size, Ne", 38, TEAL, font=TITLE_FONT).move_to([2.6, 3.0, 0])
        self.at("effective population size")
        self.play(FadeIn(t1, scale=1.2), run_time=0.8)
        a = chip("faster spread", PURPLE, 32)
        b = chip("smaller Ne", TEAL, 32)
        arr = Arrow(LEFT * 0.5, RIGHT * 0.5, buff=0, color=TEXT, stroke_width=6, max_tip_length_to_length_ratio=0.5)
        row = VGroup(a, arr, b).arrange(RIGHT, buff=0.3).move_to([2.6, 1.5, 0])
        self.at("faster spread means")
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.7)
        self.at("smaller effective size")
        self.play(GrowArrow(arr), FadeIn(b, shift=RIGHT * 0.2), run_time=0.8)
        glows = VGroup()
        for f in list(fl)[:9]:
            gc = Circle(radius=0.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4)
            gc.add_updater(lambda m, f=f: m.move_to(f.get_center()))
            gc.move_to(f.get_center())
            glows.add(gc)
        lab = T("effective size:\nhow hard chance acted", 32, TEAL, line_spacing=0.8).move_to([2.6, -0.4, 0])
        self.at("it measures how hard")
        self.play(LaggedStart(*[FadeIn(gc, scale=1.8) for gc in glows], lag_ratio=0.08), FadeIn(lab), run_time=1.6)
        sch = T("schematic: not 9 particular flies", 28, TEXT).move_to([2.6, -1.9, 0])
        self.at("not how many flies")
        self.play(FadeIn(sch), Indicate(cen, scale_factor=1.15, color=GB), run_time=1.0)
        self.finish()


class S16Rule(HW):
    def construct(self):
        gr = make_graph()
        gl = ValueTracker(0.0)
        line = make_line(gl)
        self.add(gr, line, gl)
        self.at("one line wanders")
        self.play(gl.animate.set_value(19.0), run_time=1.5, rate_func=linear)
        qh = T("?", 64, TEXT, weight=BOLD).move_to([gx(19) + 0.4, gy(ONE_LINE[19]) + 0.5, 0])
        self.at("tells you little")
        self.play(FadeIn(qh, scale=1.4), run_time=0.6)
        # shrink the line to the corner while the histogram rebuilds
        grow = ValueTracker(0.0)
        self.g = ValueTracker(19.0)
        self.add(self.g)
        self.axis = make_axis()
        self.hist = make_hist(self.g, grow)
        self.tri = make_tri(SIM, self.g)
        small = VGroup(gr[0], gr[1], line).copy()
        line.clear_updaters()
        self.remove(line)
        self.play(FadeOut(gr[2]), FadeOut(qh), run_time=0.3)
        big = VGroup(gr[0], gr[1], line)
        self.at("many replicates")
        self.add(self.axis, self.hist)
        self.play(big.animate.scale(0.36).move_to([-4.1, 2.6, 0]), FadeIn(self.axis), grow.animate.set_value(1.0), run_time=1.2)
        one = T("one line", 30, TEXT).move_to([-4.1, 1.45, 0])
        self.add(self.tri)
        self.at("side by side")
        self.play(FadeIn(one), FadeIn(self.tri, shift=UP * 0.3), run_time=0.7)
        arr = Arrow([-1.9, 2.7, 0], [0.4, 2.7, 0], buff=0, color=TEXT, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        lab = T("replicates reveal\nthe average", 32, GB, line_spacing=0.8).move_to([3.4, 2.7, 0])
        rp = ripple(lambda: self.tri.get_center(), TEXT)
        self.at("show whether the average")
        self.play(GrowArrow(arr), FadeIn(lab, shift=LEFT * 0.2), run_time=0.9)
        self.add(rp)
        self.at("was pushed")
        self.play(Indicate(self.tri, scale_factor=1.9, color=WHITE), run_time=1.0)
        self.finish()


class S17End(EndCard):
    LINE = "Drift spreads replicates apart while leaving their average alone."
