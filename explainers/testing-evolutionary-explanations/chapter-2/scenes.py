"""Changing the Cause on Purpose  (Biochemistrypedia explainer, film 2 of 2, level-up 2026-11-11)

COLOR MAP (same as film 1, one colour per concept)
  GREY = the starting / source population (and natural, unmanipulated panels)
  GOLD = the cause that is changed or selected (predator outlines, the "change" arrow)
  TEAL = the population after the change (moved guppies)
  BLUE = inheritance (only in the recap lamps)
Film 1 keeps the pipeline's dark ground, so this film does too. Guppies are simple cartoon fish.
Life-history panels are schematic (bar lengths show direction, not data); the film says so on screen.
THE WORLD: two stream reaches side by side (left: predators of adults; right: predator of juveniles),
each with a strip under it that holds the panels / timeline / question. Carried through every scene.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

POP, CAUSE, AFTER, HER = GREY, GOLD, TEAL, BLUE
WATER, WEDGE = "#1E3B52", "#5C86A8"
BEAK = "#E8C27A"

# ---------------------------------------------------------------- geometry
CXL, CXR = -3.5, 3.5
BW = 5.6
Y0, Y1 = -3.65, 3.1


def comp(y):
    """Fish y when the reaches are squeezed into their upper part (strip below)."""
    return 0.2 + (y + 3.2) * (2.6 / 6.0)


LA_POS = [(-0.4, 1.0), (-1.7, -0.4), (0.4, -1.7), (-1.3, -2.6), (1.7, -2.4)]
LJ_POS = [(-0.6, -1.1)]
RA_POS = [(-1.7, -0.3), (0.5, -1.6), (-1.0, -2.6), (1.8, -2.2)]
RJ_POS = [(-0.2, 1.0), (-1.4, 1.7), (1.0, -0.4)]
PL_POS, PR_POS = (1.3, 1.0), (1.6, 1.0)
MOVED_POS = [(2.3, 1.2), (3.4, 0.6), (4.2, 1.5)]          # absolute, compressed coordinates
TEAL_J_POS = [(2.6, 2.3), (4.6, 0.7), (3.0, 1.9)]
GAD, GJ = 0.8, 0.4                                          # adult / juvenile guppy scale


# ---------------------------------------------------------------- helpers
def L(text, size=28, color=TEXT, **kw):
    """Label with a dark halo so a dashed line behind it never cuts it."""
    t = T(text, size, color, **kw)
    t.set_stroke(BG, 8, background=True)
    t.set_z_index(9)
    return t


def fish(s=1.0, color=GREY, edge=TEXT, flip=False, sw=2.5):
    body = Ellipse(width=1.0 * s, height=0.5 * s).set_fill(color, 1).set_stroke(edge, sw)
    tail = Polygon([-0.42 * s, 0, 0], [-0.85 * s, 0.28 * s, 0], [-0.85 * s, -0.28 * s, 0]).set_fill(color, 1).set_stroke(edge, sw)
    fin = Polygon([-0.05 * s, 0.23 * s, 0], [0.15 * s, 0.45 * s, 0], [0.2 * s, 0.2 * s, 0]).set_fill(color, 1).set_stroke(edge, sw * 0.8)
    eye = Dot([0.27 * s, 0.07 * s, 0], radius=0.055 * s, color=BG)
    g = VGroup(tail, fin, body, eye)
    g.tint = VGroup(tail, fin, body)
    if flip:
        g.flip(UP)
    return g


def predator(s, flip=True):
    return fish(s, "#59606E", edge=GOLD, flip=flip, sw=4.5)


def swim(m, ax=0.35, ay=0.16, w=0.8, ph=0.0):
    """Slow wander written as a velocity, so a play(m.animate.shift(...)) still works on top of it."""
    m._t = 0.0

    def u(mob, dt):
        mob._t += dt
        t = mob._t
        mob.shift(np.array([ax * w * np.cos(w * t + ph), ay * 1.37 * w * np.cos(1.37 * w * t + 2 * ph), 0.0]) * dt)
    m.add_updater(u)


def reach(cx):
    water = RoundedRectangle(corner_radius=0.2, width=BW, height=Y1 - Y0).set_fill(WATER, 1).set_stroke(WEDGE, 3).move_to([cx, (Y0 + Y1) / 2, 0])
    rng = np.random.RandomState(int(abs(cx) * 10) % 97 + 3)
    flows = VGroup(*[Line([0, 0, 0], [0.55, 0, 0]).set_stroke("#8FB3CF", 3, opacity=0.3).move_to([cx + rng.uniform(-2.6, 2.6), rng.uniform(Y0 + 0.3, Y1 - 0.3), 0]) for _ in range(10)])
    for f in flows:
        f.sp = rng.uniform(0.25, 0.5)

    def u(g, dt):
        for f in g:
            f.shift(RIGHT * f.sp * dt)
            if f.get_x() > cx + 2.7:
                f.shift(LEFT * 5.4)
    flows.add_updater(u)
    g = VGroup(water, flows)
    g.set_z_index(0)
    return g


def dock():
    strip = Rectangle(width=14.4, height=3.85).set_fill(BG, 1).set_stroke(width=0).move_to([0, -2.075, 0])
    wl = VGroup(*[Line([cx - BW / 2 + 0.2, -0.15, 0], [cx + BW / 2 - 0.2, -0.15, 0]).set_stroke(WEDGE, 3) for cx in (CXL, CXR)])
    g = VGroup(strip, wl)
    g.set_z_index(6)
    return g


def spawn(rel, cx, s, color, comp_on, flip=False, seed=0, pred=False, absolute=False):
    f = predator(s, flip=True) if pred else fish(s, color, flip=flip)
    x, y = rel
    if not absolute:
        x = cx + x
        y = comp(y) if comp_on else y
    elif not comp_on:
        pass
    f.move_to([x, y, 0])
    rng = np.random.RandomState(seed + 7)
    if pred:
        swim(f, 0.12, 0.08, 0.7, rng.uniform(0, 6))
    else:
        swim(f, 0.35 if s > 0.6 else 0.25, 0.14, rng.uniform(0.6, 1.0), rng.uniform(0, 6))
    f.set_z_index(2)
    return f


class Wd:
    pass


def world(sc, comp_on=True, left="full", right="natural", preds=(True, True), tint=0.0):
    """Both reaches and their fish, added to the scene. Same positions in every scene."""
    W = Wd()
    W.rL, W.rR = reach(CXL), reach(CXR)
    sc.add(W.rL, W.rR)
    idx = [0, 1, 2, 3, 4] if left == "full" else [0, 4]
    W.LA = [spawn(LA_POS[i], CXL, GAD, POP, comp_on, flip=True, seed=i) for i in idx]
    W.LJ = [spawn(p, CXL, GJ, POP, comp_on, seed=10 + k) for k, p in enumerate(LJ_POS)]
    W.RA, W.RJ, W.MV, W.TJ = [], [], [], []
    if right == "natural":
        W.RA = [spawn(p, CXR, GAD, POP, comp_on, flip=True, seed=20 + k) for k, p in enumerate(RA_POS)]
        W.RJ = [spawn(p, CXR, GJ, POP, comp_on, flip=True, seed=30 + k) for k, p in enumerate(RJ_POS)]
    elif right in ("moved", "teal"):
        col = POP if right == "moved" else TEAL
        W.MV = [spawn(p, 0, GAD, col, True, flip=True, seed=40 + k, absolute=True) for k, p in enumerate(MOVED_POS)]
        if right == "teal":
            W.TJ = [spawn(p, 0, GJ, TEAL, True, flip=True, seed=50 + k, absolute=True) for k, p in enumerate(TEAL_J_POS)]
    W.PL = spawn(PL_POS, CXL, 1.7, POP, comp_on, seed=60, pred=True) if preds[0] else None
    W.PR = spawn(PR_POS, CXR, 1.1, POP, comp_on, seed=61, pred=True) if preds[1] else None
    W.all = [f for f in W.LA + W.LJ + W.RA + W.RJ + W.MV + W.TJ if f is not None] + [p for p in (W.PL, W.PR) if p is not None]
    for f in W.all:
        sc.add(f)
    return W


def tint_fish(sc, fs, tr, c0=POP, c1=AFTER):
    h = VMobject()
    a, b = ManimColor(c0), ManimColor(c1)
    h.add_updater(lambda m: [f.tint.set_fill(interpolate_color(a, b, tr.get_value())) for f in fs])
    sc.add(h)
    return h


def top(text, cx, color=TEXT, size=30):
    size = min(size, 30)
    return L(text, size, color).move_to([cx, 3.5, 0])


def bar(x0, y, w, color=POP):
    return Rectangle(width=max(w, 0.01), height=0.28).set_fill(color, 1).set_stroke(width=0).move_to([x0 + max(w, 0.01) / 2, y, 0])


ROWS3 = ["age at maturity", "size at maturity", "number of young"]


class Card:
    """A schematic life-history card in the strip: title, row labels, bars (values 0..1)."""

    def __init__(self, cx, vals, rows=ROWS3, title="life history (schematic)", color=POP, width=5.4, maxw=4.8, tsize=26, lsize=28):
        n = len(rows)
        self.x0 = cx - width / 2 + 0.3
        self.maxw, self.color, self.cx = maxw, color, cx
        self.box = RoundedRectangle(corner_radius=0.15, width=width, height=3.2).set_stroke(color, 3).set_fill(BG, 1).move_to([cx, -1.9, 0])
        self.title = L(title, tsize, TEXT).move_to([cx, -0.62, 0])
        step = 0.85 if n == 3 else 1.05
        self.ly = [-1.12 - step * k for k in range(n)]
        self.by = [y - 0.38 for y in self.ly]
        self.labels = [L(r, lsize, TEXT) for r in rows]
        for lab, y in zip(self.labels, self.ly):
            lab.move_to([self.x0, y, 0], aligned_edge=LEFT)
            lab.shift(RIGHT * (self.x0 - lab.get_left()[0]))
        self.vals = list(vals)
        self.bars = [bar(self.x0, y, v * maxw, color) for y, v in zip(self.by, vals)]
        self.frame = VGroup(self.box, self.title)

    def row(self, k):
        return VGroup(self.labels[k], self.bars[k])

    def all(self):
        return VGroup(self.box, self.title, *self.labels, *self.bars)


def lamp(color, r=1.0):
    glow = Circle(radius=r * 1.35).set_fill(color, 0).set_stroke(width=0)
    bulb = Circle(radius=r).set_stroke(color, 6).set_fill(color, 0.0)
    base = RoundedRectangle(corner_radius=0.08, width=r * 0.9, height=r * 0.3).set_fill(GREY, 0.9).set_stroke(TEXT, 2).next_to(bulb, DOWN, buff=0)
    g = VGroup(glow, bulb, base)
    g.glow, g.bulb = glow, bulb
    return g


def lit(g, color):
    g.bulb.set_fill(color, 0.9)
    g.glow.set_fill(color, 0.28)
    g._t = 0.0

    def u(m, dt):
        m._t += dt
        m.glow.set_fill(color, 0.2 + 0.1 * np.sin(2.2 * m._t))
    g.add_updater(u)


# ---- rival icons (drawn in neutral TEXT so GOLD stays the cause)
def icon_ruler():
    r = Rectangle(width=0.95, height=0.3).set_stroke(TEXT, 4).set_fill(BG, 1)
    ticks = VGroup(*[Line([-0.38 + 0.19 * k, 0.15, 0], [-0.38 + 0.19 * k, 0.15 - (0.14 if k % 2 == 0 else 0.08), 0]).set_stroke(TEXT, 3) for k in range(5)])
    return VGroup(r, ticks)


def icon_leaf():
    e = Ellipse(width=0.85, height=0.45).set_stroke(TEXT, 4).set_fill(BG, 1).rotate(0.6)
    v = Line([-0.28, -0.2, 0], [0.28, 0.2, 0]).set_stroke(TEXT, 3)
    st = Line([-0.28, -0.2, 0], [-0.5, -0.42, 0]).set_stroke(TEXT, 4)
    return VGroup(e, v, st)


def icon_sun():
    c = Circle(radius=0.2).set_stroke(TEXT, 4).set_fill(BG, 1)
    rays = VGroup(*[Line(0.3 * np.array([np.cos(a), np.sin(a), 0]), 0.5 * np.array([np.cos(a), np.sin(a), 0])).set_stroke(TEXT, 4) for a in np.linspace(0, TAU, 8, endpoint=False)])
    return VGroup(c, rays)


def icon_clock():
    c = Circle(radius=0.38).set_stroke(TEXT, 4).set_fill(BG, 1)
    h = VGroup(Line([0, 0, 0], [0, 0.26, 0]), Line([0, 0, 0], [0.18, -0.05, 0])).set_stroke(TEXT, 4)
    return VGroup(c, h)


RIVALS = [("stream size", icon_ruler), ("food", icon_leaf), ("light", icon_sun), ("history", icon_clock)]
RIV_Y = [2.7, 1.85, 1.0, 0.15]


def rival_set(with_lines=True):
    """The four rival icons + labels in the gap between the reaches, and their dashed lines to both panels."""
    items, lines = [], VGroup()
    rng = np.random.RandomState(4)
    for k, ((name, mk), y) in enumerate(zip(RIVALS, RIV_Y)):
        ic = mk().move_to([-1.4, y, 0])
        lab = L(name, 28, TEXT).move_to([ic.get_right()[0] + 0.2 + 0.5 * 0, y, 0])
        lab.shift(RIGHT * (ic.get_right()[0] + 0.25 - lab.get_left()[0]))
        g = VGroup(BackgroundRectangle(lab, color=BG, fill_opacity=0.92, buff=0.06), ic, lab)
        g.set_z_index(8)
        items.append(g)
        if with_lines:
            xl = CXL + (-1.8 + 1.2 * k + rng.uniform(-0.2, 0.2))
            xr = CXR + (-1.8 + 1.2 * ((k + 2) % 4) + rng.uniform(-0.2, 0.2))
            lines.add(DashedLine(ic.get_left() + LEFT * 0.05, [xl, -0.3, 0], dash_length=0.15).set_stroke(TEXT, 3, opacity=0.6))
            lines.add(DashedLine(lab.get_right() + RIGHT * 0.05, [xr, -0.3, 0], dash_length=0.15).set_stroke(TEXT, 3, opacity=0.6))
    lines.set_z_index(7)
    return items, lines


def person(color, s=1.0):
    head = Circle(radius=0.28 * s).set_stroke(color, 5).set_fill(BG, 1).move_to([0, 0.95 * s, 0])
    torso = RoundedRectangle(corner_radius=0.2 * s, width=0.8 * s, height=1.1 * s).set_stroke(color, 5).set_fill(BG, 1).move_to([0, 0.15 * s, 0])
    legs = VGroup(Line([-0.2 * s, -0.4 * s, 0], [-0.25 * s, -1.1 * s, 0]), Line([0.2 * s, -0.4 * s, 0], [0.25 * s, -1.1 * s, 0])).set_stroke(color, 5)
    arm = Line([0.35 * s, 0.4 * s, 0], [0.85 * s, 0.25 * s, 0]).set_stroke(color, 5)
    return VGroup(legs, torso, head, arm)


def icon_naturalist(color, s=1.0):
    p = person(color, s)
    nb = Rectangle(width=0.55 * s, height=0.72 * s).set_stroke(color, 4).set_fill(BG, 1).move_to([1.1 * s, 0.4 * s, 0]).rotate(-0.15)
    ln = VGroup(*[Line([0.92 * s, (0.6 - 0.17 * k) * s, 0], [1.28 * s, (0.6 - 0.17 * k) * s, 0]).set_stroke(color, 3) for k in range(3)])
    pen = Line([1.05 * s, 0.1 * s, 0], [1.45 * s, 0.55 * s, 0]).set_stroke(TEXT, 4)
    pen._t = 0.0

    def u(m, dt):
        m._t += dt
        m.shift(np.array([0.05 * np.cos(4 * m._t), 0.03 * np.sin(5 * m._t), 0]) * dt * 4)
    pen.add_updater(u)
    return VGroup(p, nb, ln, pen)


def icon_experimenter(color, s=1.0):
    p = person(color, s)
    pole = Line([0.85 * s, 0.25 * s, 0], [1.55 * s, 1.15 * s, 0]).set_stroke(color, 5)
    ring = Circle(radius=0.38 * s).set_stroke(color, 5).set_fill(color, 0.1).move_to([1.75 * s, 1.4 * s, 0])
    mesh = VGroup(Line([1.5 * s, 1.4 * s, 0], [2.0 * s, 1.4 * s, 0]), Line([1.75 * s, 1.15 * s, 0], [1.75 * s, 1.65 * s, 0])).set_stroke(color, 2.5)
    net = VGroup(pole, ring, mesh)
    net._t = 0.0
    piv = np.array([0.85 * s, 0.25 * s, 0])

    def u(m, dt):
        m._t += dt
        m.rotate(0.45 * np.cos(1.6 * m._t) * dt, about_point=piv + 0)
    net.add_updater(u)
    return VGroup(p, net)


def icon_detective(color, s=1.0):
    p = person(color, s)
    hat = Polygon([-0.4 * s, 1.18 * s, 0], [0.4 * s, 1.18 * s, 0], [0.22 * s, 1.5 * s, 0], [-0.22 * s, 1.5 * s, 0]).set_stroke(color, 4).set_fill(color, 0.25)
    lens = Circle(radius=0.34 * s).set_stroke(color, 5).set_fill(color, 0.08).move_to([1.35 * s, 0.7 * s, 0])
    hnd = Line([0.85 * s, 0.25 * s, 0], [1.12 * s, 0.5 * s, 0]).set_stroke(color, 5)
    mag = VGroup(lens, hnd)
    mag._t = 0.0

    def u(m, dt):
        m._t += dt
        m.shift(np.array([0.18 * np.cos(1.5 * m._t), 0.1 * np.cos(2.1 * m._t), 0]) * dt)
    mag.add_updater(u)
    return VGroup(p, hat, mag)


def pulse(m, k=1.25):
    return m.animate(rate_func=there_and_back).scale(k)


def check(color=AFTER, s=0.32, sw=10):
    return VMobject().set_points_as_corners([[-0.55 * s, 0.0, 0], [-0.15 * s, -0.45 * s, 0], [0.6 * s, 0.5 * s, 0]]).set_stroke(color, sw)


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "How to Test an Evolutionary Explanation"
    TITLE = "Changing the Cause on Purpose"


# ---------------------------------------------------------------- s01
class S01Link(SpokenScene):
    def construct(self):
        frame = RoundedRectangle(corner_radius=0.25, width=12.2, height=6.6).set_stroke(GREY, 3).set_fill(BG, 1).move_to([0, 0.2, 0])
        # seed panel (right)
        sp = RoundedRectangle(corner_radius=0.2, width=4.2, height=3.0).set_stroke("#B58A4B", 4).set_fill("#B58A4B", 0.12).move_to([3.6, 0.1, 0])
        rng = np.random.RandomState(8)
        seeds = VGroup(*[Ellipse(width=0.3, height=0.17).set_fill("#B58A4B", 1).set_stroke(width=0).rotate(rng.uniform(0, 3)).move_to([3.6 + rng.uniform(-1.6, 1.6), 0.1 + rng.uniform(-1.1, 1.1), 0]) for _ in range(16)])
        # dot pile (left): 40 grey finch dots from normal quantiles, 6 gold survivors
        from statistics import NormalDist
        zs = [NormalDist().inv_cdf((i + 0.5) / 40) for i in range(40)]
        xs = [-3.5 + 1.15 * z for z in zs]
        cnt, pts = {}, []
        for x in xs:
            b = round(x / 0.3)
            k = cnt.get(b, 0)
            cnt[b] = k + 1
            pts.append((b * 0.3, -1.55 + 0.3 * k))
        surv = list(range(33, 39))
        pile = VGroup(*[Dot([x, y, 0], radius=0.125, color=GOLD if i in surv else POP).set_opacity(0.95) for i, (x, y) in enumerate(pts)])
        for i, d in enumerate(pile):
            d._t = 0.7 * i

            def u(m, dt):
                m._t += dt
                m.shift(UP * 0.04 * np.cos(1.6 * m._t) * dt * 1.6)
            d.add_updater(u)
        m0 = float(np.mean([p[0] for p in pts]))
        ms = float(np.mean([pts[i][0] for i in surv]))
        s_arrow = Arrow([m0, 0.55, 0], [ms, 0.55, 0], buff=0, color=GOLD, stroke_width=9, tip_length=0.26)
        s_lab = L("S", 44, GOLD).move_to([ms + 0.5, 0.55, 0])
        lamps = [lamp(c, 0.4).move_to([x, 2.55, 0]) for x, c in zip((-1.7, 0.0, 1.7), (GOLD, BLUE, TEAL))]
        for lp, c in zip(lamps, (GOLD, BLUE, TEAL)):
            lit(lp, c)
        tile = VGroup(frame, sp, seeds, pile, s_arrow, s_lab, *lamps)
        self.play(FadeIn(frame), FadeIn(sp), LaggedStart(*[FadeIn(s, scale=0.5) for s in seeds], lag_ratio=0.04), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in pile], lag_ratio=0.02), *[FadeIn(l) for l in lamps], run_time=0.9)
        self.play(GrowArrow(s_arrow), FadeIn(s_lab), run_time=0.5)
        self.at("leading suspect")
        sus = L("suspect", 36, GOLD).move_to([3.6, -2.0, 0])
        self.play(FadeIn(sus, shift=UP * 0.2), Indicate(sp, color=GOLD, scale_factor=1.04), run_time=0.9)
        tile.add(sus)
        self.at("nobody can rerun")
        q = Text("?", font=FONT, font_size=190, color=TEXT, weight=BOLD).set_opacity(0.92).move_to([3.6, 0.1, 0])
        q.set_stroke(BG, 10, background=True)
        self.play(GrowFromCenter(q), run_time=0.8)
        tile.add(q)
        self.at("rerun 1977")
        yr = chip("1977", color=TEXT, size=36).move_to([-4.6, 2.6, 0])
        self.play(FadeIn(yr, shift=DOWN * 0.2), run_time=0.7)
        tile.add(yr)
        # the question, then the stream fades in behind a shrinking tile
        self.at("how do you test")
        rl, rr = reach(CXL), reach(CXR)
        fl = [spawn(p, CXL, GAD, POP, False, flip=True, seed=i) for i, p in enumerate(LA_POS)] + [spawn(p, CXL, GJ, POP, False, seed=10 + k) for k, p in enumerate(LJ_POS)]
        fr = [spawn(p, CXR, GAD, POP, False, flip=True, seed=20 + k) for k, p in enumerate(RA_POS)] + [spawn(p, CXR, GJ, POP, False, flip=True, seed=30 + k) for k, p in enumerate(RJ_POS)]
        for f in fl + fr:
            f.set_opacity(0)
        rl.set_opacity(0)
        rr.set_opacity(0)
        self.add(rl, rr, *fl, *fr)
        tile.set_z_index(20)
        self.play(tile.animate.scale(0.3).move_to([-5.0, 2.85, 0]), rl.animate.set_opacity(1), rr.animate.set_opacity(1),
                  *[f.animate.set_opacity(1) for f in fl + fr], run_time=1.3)
        self.at("what did the selecting")
        qc = chip("What did the selecting?", color=TEXT, size=40).set_z_index(21).move_to([0, -3.0, 0])
        qc[0].set_fill(BG, 0.95)
        self.play(FadeIn(qc, shift=UP * 0.2), run_time=0.7)
        self.wait(0.3)
        self.play(FadeOut(tile, shift=LEFT * 1.5 + UP * 0.8), FadeOut(qc), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- s02
class S02Streams(SpokenScene):
    def construct(self):
        W = world(self, comp_on=False, preds=(False, False))
        self.wait(0.3)
        self.at("trinidad")
        tr = L("Trinidad", 40, TEXT).move_to([0, 3.5, 0])
        self.play(FadeIn(tr, shift=DOWN * 0.2), run_time=0.7)
        self.at("where guppies live")
        self.play(*[pulse(f, 1.25) for f in W.LA + W.RA], run_time=1.2)
        self.at("in some stream reaches")
        self.play(FadeOut(tr), run_time=0.4)
        tl = top("predators of adults", CXL, TEXT, 32)
        self.play(FadeIn(tl, shift=DOWN * 0.2), run_time=0.6)
        pl = spawn(PL_POS, CXL, 1.7, POP, False, seed=60, pred=True)
        pl.shift(RIGHT * 1.4).set_opacity(0)
        self.add(pl)
        self.at("main predators")
        self.play(pl.animate.shift(LEFT * 1.4).set_opacity(1), run_time=1.0)
        self.at("eat adult guppies")
        tgt = W.LA[0]
        self.play(pl.animate.shift(LEFT * 1.3), tgt.animate.shift(LEFT * 1.1 + DOWN * 0.7), run_time=0.5, rate_func=rush_into)
        self.play(pl.animate.shift(RIGHT * 1.3), run_time=0.9)
        self.play(tgt.animate.shift(RIGHT * 0.9 + UP * 0.5), run_time=0.8)
        self.at("in others")
        tr_ = top("predator of juveniles", CXR, TEXT, 32)
        self.play(FadeIn(tr_, shift=DOWN * 0.2), run_time=0.6)
        pr = spawn(PR_POS, CXR, 1.1, POP, False, seed=61, pred=True)
        pr.shift(RIGHT * 1.0).set_opacity(0)
        self.add(pr)
        self.at("main fish predator")
        self.play(pr.animate.shift(LEFT * 1.0).set_opacity(1), run_time=0.9)
        self.at("takes small juveniles")
        jt = W.RJ[0]
        self.play(pr.animate.shift(LEFT * 1.3), jt.animate.shift(LEFT * 1.0 + DOWN * 0.8), run_time=0.5, rate_func=rush_into)
        self.play(pr.animate.shift(RIGHT * 1.3), run_time=0.9)
        self.play(jt.animate.shift(RIGHT * 0.9 + UP * 0.6), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- s03
class S03Differ(SpokenScene):
    def construct(self):
        W = world(self, comp_on=False)
        tl = top("predators of adults", CXL, TEXT, 32)
        tr = top("predator of juveniles", CXR, TEXT, 32)
        self.add(tl, tr)
        dk = dock()
        dk.set_opacity(0)
        self.add(dk)
        self.wait(0.2)
        # the fish squeeze into the upper part of each reach; the strip rises under them
        anims = [f.animate.move_to([f.get_x(), comp(f.get_y()), 0]) for f in W.all]
        self.play(*anims, dk.animate.set_opacity(1), run_time=1.6)
        self.at("life history")
        cl = Card(CXL, [0.45, 0.45, 0.85])
        cr = Card(CXR, [0.8, 0.8, 0.45])
        for c in (cl, cr):
            c.all().set_z_index(7)
        self.play(FadeIn(cl.box), FadeIn(cr.box), FadeIn(cl.title), FadeIn(cr.title), run_time=0.9)
        self.at("when they mature")
        self.play(*[FadeIn(c.labels[0]) for c in (cl, cr)], *[GrowFromEdge(c.bars[0], LEFT) for c in (cl, cr)], run_time=1.3)
        self.at("at what size")
        self.play(*[FadeIn(c.labels[1]) for c in (cl, cr)], *[GrowFromEdge(c.bars[1], LEFT) for c in (cl, cr)], run_time=1.3)
        self.at("how many young")
        self.play(*[FadeIn(c.labels[2]) for c in (cl, cr)], *[GrowFromEdge(c.bars[2], LEFT) for c in (cl, cr)], run_time=1.3)
        self.play(*[Indicate(c.bars[k], color=TEXT, scale_factor=1.04) for c in (cl, cr) for k in range(3)], run_time=1.2)
        self.finish()


def stage(sc, left="full", right="natural", cards=True, tops=True, dim=False):
    """Rebuild the s03-s05 picture: reaches (squeezed), strip, two cards, top labels."""
    W = world(sc, comp_on=True, left=left, right=right)
    dk = dock()
    sc.add(dk)
    cl, cr = Card(CXL, [0.45, 0.45, 0.85]), Card(CXR, [0.8, 0.8, 0.45])
    for c in (cl, cr):
        c.all().set_z_index(7)
        sc.add(c.all())
    tl, tr = top("predators of adults", CXL, TEXT, 32), top("predator of juveniles", CXR, TEXT, 32)
    sc.add(tl, tr)
    return W, dk, cl, cr, tl, tr


# ---------------------------------------------------------------- s04
class S04Assoc(SpokenScene):
    def construct(self):
        W, dk, cl, cr, tl, tr = stage(self)
        self.wait(0.2)
        self.at("predators shape")
        stamp = VGroup(RoundedRectangle(corner_radius=0.12, width=2.3, height=0.75).set_stroke(GOLD, 5), T("CAUSE?", 30, GOLD, weight=BOLD)).move_to([0, 3.45, 0]).rotate(-0.1)
        stamp.set_z_index(9)
        stamp._t = 0.0

        def hov(m, dt):
            m._t += dt
            m.shift(UP * 0.12 * np.cos(2.0 * m._t) * dt)
        stamp.add_updater(hov)
        self.play(FadeIn(stamp, shift=DOWN * 0.3), Indicate(W.PL, color=GOLD, scale_factor=1.15), Indicate(W.PR, color=GOLD, scale_factor=1.15), run_time=1.3)
        self.at("pattern fits")
        lines = VGroup(*[DashedLine([p.get_x(), p.get_bottom()[1] - 0.05, 0], [p.get_x(), -0.3, 0], dash_length=0.16).set_stroke(GOLD, 5) for p in (W.PL, W.PR)])
        lines.set_z_index(7)
        self.play(Create(lines), run_time=1.4)
        self.at("but a comparison")
        self.play(W.rL[0][0].animate(rate_func=there_and_back).set_stroke(TEXT, 6), W.rR[0][0].animate(rate_func=there_and_back).set_stroke(TEXT, 6), run_time=1.2)
        self.at("an association")
        al = [chip("association", color=GOLD, size=30).set_z_index(30).move_to([p.get_x(), 0.85, 0]) for p in (W.PL, W.PR)]
        for a in al:
            a[0].set_fill(BG, 1)
        self.play(*[FadeIn(a, shift=UP * 0.15) for a in al], run_time=0.8)
        self.at("not a cause")
        self.play(stamp.animate.shift(UP * 0.18).rotate(0.12), run_time=0.9)
        self.play(stamp.animate.shift(DOWN * 0.1).rotate(-0.08), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- s05
class S05Rivals(SpokenScene):
    def construct(self):
        W, dk, cl, cr, tl, tr = stage(self)
        gl = VGroup(*[DashedLine([p.get_x(), p.get_bottom()[1] - 0.05, 0], [p.get_x(), -0.3, 0], dash_length=0.16).set_stroke(GOLD, 5) for p in (W.PL, W.PR)]).set_z_index(7)
        al = [chip("association", color=GOLD, size=30).set_z_index(30).move_to([p.get_x(), 0.85, 0]) for p in (W.PL, W.PR)]
        for a in al:
            a[0].set_fill(BG, 1)
        self.add(gl, *al)
        items, rl = rival_set()
        self.at("differ in other ways")
        self.play(*[f.animate.set_opacity(0.3) for f in W.all], *[a.animate.set_opacity(0.0) for a in al], run_time=1.0)
        self.at("stream size")
        self.play(FadeIn(items[0], shift=DOWN * 0.4), Create(VGroup(*rl[0:2])), run_time=1.0)
        self.at("food")
        self.play(FadeIn(items[1], shift=DOWN * 0.4), Create(VGroup(*rl[2:4])), run_time=0.8)
        self.at("light")
        self.play(FadeIn(items[2], shift=DOWN * 0.4), Create(VGroup(*rl[4:6])), run_time=0.6)
        self.at("history")
        self.play(FadeIn(items[3], shift=DOWN * 0.4), Create(VGroup(*rl[6:8])), run_time=0.8)
        self.at("change from one site")
        self.play(*[pulse(it[0], 1.3) for it in items], run_time=1.4)
        self.at("comparing the sites")
        allines = VGroup(gl, rl)
        self.play(Indicate(allines, color=TEXT, scale_factor=1.0), run_time=1.0)
        self.at("pull those apart")
        self.play(*[ln.animate.shift(UP * 0.12 * (1 if k % 2 else -1)) for k, ln in enumerate(rl)], run_time=0.5)
        self.play(*[ln.animate.shift(DOWN * 0.12 * (1 if k % 2 else -1)) for k, ln in enumerate(rl)], run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s06
class S06Move(SpokenScene):
    def construct(self):
        W, dk, cl, cr, tl, tr = stage(self)
        items, rl = rival_set()
        for f in W.all:
            f.set_opacity(0.3)
        self.add(*items, rl)
        self.play(FadeOut(VGroup(*items)), FadeOut(rl), *[f.animate.set_opacity(1) for f in W.all], run_time=1.2)
        self.at("proposed cause")
        self.play(Indicate(W.PL, color=GOLD, scale_factor=1.2), Indicate(W.PR, color=GOLD, scale_factor=1.2), run_time=1.3)
        self.at("guppies from a site")
        rock = Polygon([-0.6, 2.2, 0], [0.6, 2.2, 0], [0.45, 1.6, 0], [-0.45, 1.6, 0]).set_fill("#6B5B45", 1).set_stroke("#8A7658", 3)
        streaks = VGroup(*[Line([x, 1.6, 0], [x, 0.15, 0]).set_stroke("#8FB3CF", 5, opacity=0.8) for x in (-0.25, 0, 0.25)])
        for k, s_ in enumerate(streaks):
            s_._t = 0.4 * k

            def uu(m, dt):
                m._t += dt
                m.set_stroke(opacity=0.5 + 0.3 * np.sin(5 * m._t))
            s_.add_updater(uu)
        wf = VGroup(rock, streaks).set_z_index(3)
        net = VGroup(Line([0.0, 0.0, 0], [0.85, -0.85, 0]).set_stroke(TEXT, 6), Circle(radius=0.55).set_stroke(TEXT, 6).set_fill(TEXT, 0.1),
                     Line([-0.55, 0, 0], [0.55, 0, 0]).set_stroke(TEXT, 3), Line([0, -0.55, 0], [0, 0.55, 0]).set_stroke(TEXT, 3)).set_z_index(10)
        net.move_to([CXL - 0.4, 2.6, 0])
        scoop = [W.LA[1], W.LA[2], W.LA[3]]
        for f in scoop:
            f.clear_updaters()
        self.play(FadeIn(wf), FadeIn(net, shift=DOWN * 0.3), run_time=0.6)
        self.play(net.animate.move_to([CXL - 0.4, 1.3, 0]), run_time=0.6)
        self.play(LaggedStart(*[f.animate.scale(0.6).move_to([CXL - 0.4, 1.3, 0] + np.array([0.15 * k - 0.15, 0.1 * (k % 2), 0])) for k, f in enumerate(scoop)], lag_ratio=0.25), run_time=1.1)
        arc = ArcBetweenPoints([CXL + 0.5, 2.3, 0], [CXR - 0.5, 2.3, 0], angle=-0.8).set_stroke(GOLD, 9)
        path = arc.copy()
        arc.add_tip(tip_length=0.3)
        ml = L("moved", 34, GOLD).move_to([0, 3.4, 0])
        for f in W.RA + W.RJ:
            f.clear_updaters()
        self.at("were moved")
        self.play(Create(arc), FadeIn(ml), FadeOut(tl), FadeOut(tr), *[f.animate.set_opacity(0) for f in W.RA + W.RJ], run_time=0.6)
        grp = VGroup(net, *scoop)
        self.play(grp.animate.move_to([CXL + 0.5, 2.3, 0]), run_time=0.4)
        self.play(MoveAlongPath(grp, path), run_time=1.5, rate_func=smooth)
        self.play(FadeOut(net), *[f.animate.scale(1 / 0.6).move_to([x, y, 0]) for f, (x, y) in zip(scoop, MOVED_POS)], run_time=1.1)
        for k, f in enumerate(scoop):
            swim(f, 0.35, 0.14, 0.8, 1.3 * k)
        self.finish()


# ---------------------------------------------------------------- s07
class S07Wait(SpokenScene):
    def construct(self):
        W = world(self, comp_on=True, left="after", right="moved")
        dk = dock()
        self.add(dk)
        tl, tr = top("predators of adults", CXL, TEXT, 32), top("predator of juveniles", CXR, TEXT, 32)
        self.add(tl, tr)
        prog = ValueTracker(0.0)
        tint_fish(self, W.MV, prog)
        self.wait(0.2)
        # the strip becomes a timeline
        ax = Arrow([-5.9, -1.25, 0], [5.9, -1.25, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.3).set_z_index(7)
        l0 = L("moved", 34, GOLD).move_to([-5.2, -0.65, 0])
        self.play(FadeOut(tl), FadeOut(tr), Create(ax), FadeIn(l0), run_time=1.0)
        mt = top("moved population", CXR, TEAL, 32)
        self.play(FadeIn(mt, shift=DOWN * 0.2), run_time=0.5)
        self.at("evolved")
        ticks = VGroup(*[Line([-5.5 + 11.0 * k / 44, -1.25 - 0.18, 0], [-5.5 + 11.0 * k / 44, -1.25 + 0.18, 0]).set_stroke(TEXT, 3) for k in range(45)]).set_z_index(7)
        gen = L("30 to 60 guppy generations", 34, TEXT).move_to([0, -2.15, 0])
        nm = L("Reznick, Bryga and Endler", 30, TEXT).move_to([0, -3.15, 0])
        sl = top("source population", CXL, TEXT, 32)
        l1 = L("11 years later", 34, TEXT).move_to([5.0, -0.65, 0])
        phr = ["evolved", "new reach", "david", "heather", "john endler", "compared it with", "its source population", "11 years later"]
        extra = {"new reach": [FadeIn(gen, shift=UP * 0.15)], "david": [FadeIn(nm, shift=UP * 0.15)],
                 "its source population": [FadeIn(sl, shift=DOWN * 0.2)], "11 years later": [FadeIn(l1, shift=UP * 0.15)]}
        n = len(phr)
        for k, p in enumerate(phr):
            if k:
                self.at(p)
            span = (self.t_of(phr[k + 1]) - 0.2 - self.elapsed()) if k + 1 < n else 1.4
            span = max(span, 0.3)
            n0, n1 = int(round(45 * k / n)), int(round(45 * (k + 1) / n))
            self.play(prog.animate.set_value(0.8 * (k + 1) / n), LaggedStart(*[FadeIn(t, scale=0.5) for t in ticks[n0:n1]], lag_ratio=0.8 / max(1, n1 - n0)),
                      *extra.get(p, []), run_time=span, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- s08
class S08Same(SpokenScene):
    def construct(self):
        W = world(self, comp_on=True, left="after", right="moved")
        dk = dock()
        self.add(dk)
        prog = ValueTracker(0.8)
        tint_fish(self, W.MV, prog)
        sl, mt = top("source population", CXL, TEXT, 32), top("moved population", CXR, TEAL, 32)
        self.add(sl, mt)
        self.wait(0.3)
        self.at("notice what is different")
        self.play(W.rL[0][0].animate(rate_func=there_and_back).set_stroke(TEXT, 7), W.rR[0][0].animate(rate_func=there_and_back).set_stroke(TEAL, 7), run_time=1.5)
        self.at("moved guppies")
        self.play(*[pulse(f, 1.4) for f in W.MV + W.LA], run_time=1.4)
        self.at("started as one population")
        br = VGroup(Line([CXL - 2.5, 3.15, 0], [CXL - 2.5, 3.35, 0]), Line([CXL - 2.5, 3.35, 0], [CXR + 2.5, 3.35, 0]), Line([CXR + 2.5, 3.35, 0], [CXR + 2.5, 3.15, 0])).set_stroke(POP, 5).set_z_index(9)
        bl = L("one starting population", 30, TEXT).set_z_index(10).move_to([0, 3.65, 0])
        bl[0:].set_stroke(BG, 10, background=True)
        self.play(FadeOut(sl), FadeOut(mt), Create(br), run_time=0.8)
        self.play(FadeIn(bl, shift=DOWN * 0.15), run_time=0.6)
        self.at("the researchers made the change")
        ga = Arrow([-5.4, -0.9, 0], [5.4, -0.9, 0], buff=0, color=GOLD, stroke_width=11, tip_length=0.35).set_z_index(7)
        gl = VGroup(L("the change made:", 32, GOLD), L("a new reach, with a different predator", 30, TEXT)).arrange(DOWN, buff=0.15).move_to([0, -1.95, 0])
        self.play(GrowArrow(ga), run_time=1.0)
        self.play(FadeIn(gl, shift=UP * 0.15), run_time=0.8)
        self.at("instead of finding sites")
        items = []
        for k, ((name, mk), x) in enumerate(zip(RIVALS, (-4.8, -1.6, 1.6, 4.8))):
            ic = mk().scale(0.8).move_to([x - 0.4, -3.1, 0])
            tag = L("?", 34, GREY).move_to([x + 0.35, -3.1, 0])
            items.append(VGroup(ic, tag))
        grp = VGroup(*items).set_opacity(0.45).set_z_index(8)
        self.play(FadeIn(grp, shift=UP * 0.2), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------- s09 / s10
def predict_state(sc, early=False):
    W = world(sc, comp_on=True, left="after", right="teal", preds=(True, True))
    for f in W.LA + W.LJ + [W.PL]:
        f.set_opacity(0)
    dk = dock()
    sc.add(dk)
    W.rL[0].set_fill(WATER, 0.25)
    W.rL[0].set_stroke(WEDGE, 3, opacity=0.35)
    W.rL[1].set_opacity(0.0)
    card = VGroup(RoundedRectangle(corner_radius=0.2, width=5.0, height=2.3).set_stroke(TEXT, 4).set_fill(BG, 0.92),
                  T("Mature earlier", 42, TEXT), T("or later?", 42, TEXT)).set_z_index(9)
    card[1].move_to([CXL, 1.75, 0])
    card[2].move_to([CXL, 1.05, 0])
    card[0].move_to([CXL, 1.4, 0])
    sc.add(card)
    return W, dk, card


class S09Predict(SpokenScene):
    def construct(self):
        W = world(self, comp_on=True, left="after", right="teal", preds=(True, True))
        dk = dock()
        self.add(dk)
        # the right reach is the subject: the source reach dims, its predator question card arrives later
        for f in W.TJ:
            f.set_opacity(0)
        prog = ValueTracker(0.8)
        self.wait(0.2)
        self.play(*[f.animate.set_opacity(0.25) for f in W.LA + W.LJ + [W.PL]], W.rL[0].animate.set_opacity(0.4), run_time=1.0)
        self.at("adults are safer")
        c1 = chip("adults: safer", color=TEAL, size=38).set_z_index(9).move_to([-3.2, -1.7, 0])
        self.play(FadeIn(c1, shift=UP * 0.2), *[pulse(f, 1.3) for f in W.MV], run_time=1.2)
        self.at("young are the ones")
        c2 = chip("young: eaten", color=GOLD, size=38).set_z_index(9).move_to([3.2, -1.7, 0])
        self.play(FadeIn(c2, shift=UP * 0.2), *[f.animate.set_opacity(1) for f in W.TJ], run_time=1.0)
        self.play(W.PR.animate.shift(LEFT * 1.4), W.TJ[2].animate.shift(LEFT * 0.4 + DOWN * 0.2), run_time=0.5, rate_func=rush_into)
        self.play(W.PR.animate.shift(RIGHT * 1.4), W.TJ[2].animate.shift(RIGHT * 0.6 + UP * 0.2), run_time=1.0)
        self.at("should the moved guppies")
        card = VGroup(RoundedRectangle(corner_radius=0.2, width=5.0, height=2.3).set_stroke(TEXT, 4).set_fill(BG, 0.92),
                      T("Mature earlier", 42, TEXT), T("or later?", 42, TEXT)).set_z_index(9)
        card[0].move_to([CXL, 1.4, 0])
        card[1].move_to([CXL, 1.75, 0])
        card[2].move_to([CXL, 1.05, 0])
        self.play(FadeOut(c1), FadeOut(c2), FadeIn(card, shift=DOWN * 0.3), run_time=0.9)
        self.at("mature earlier")
        e = chip("earlier", color=TEXT, size=44).set_z_index(9).move_to([-2.2, -1.9, 0])
        self.play(FadeIn(e, shift=UP * 0.2), run_time=0.6)
        self.at("or later")
        la = chip("later", color=TEXT, size=44).set_z_index(9).move_to([2.2, -1.9, 0])
        self.play(FadeIn(la, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        W = world(self, comp_on=True, left="after", right="teal", preds=(True, True))
        dk = dock()
        self.add(dk)
        for f in W.LA + W.LJ + [W.PL]:
            f.set_opacity(0.25)
        W.rL[0].set_opacity(0.4)
        card = VGroup(RoundedRectangle(corner_radius=0.2, width=5.0, height=2.3).set_stroke(TEXT, 4).set_fill(BG, 0.92),
                      T("Mature earlier", 42, TEXT), T("or later?", 42, TEXT)).set_z_index(9)
        card[0].move_to([CXL, 1.4, 0])
        card[1].move_to([CXL, 1.75, 0])
        card[2].move_to([CXL, 1.05, 0])
        e = chip("earlier", color=TEXT, size=44).set_z_index(9).move_to([-2.2, -1.9, 0])
        la = chip("later", color=TEXT, size=44).set_z_index(9).move_to([2.2, -1.9, 0])
        self.add(card, e, la)
        ang = ValueTracker(TAU)
        ring = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=ang.get_value(), color=TEXT, stroke_width=8).move_to([6.0, -3.2, 0]).set_z_index(9))
        back = Circle(radius=0.5).set_stroke(GREY, 4).move_to([6.0, -3.2, 0]).set_z_index(9)
        self.add(back, ring)
        self.play(ang.animate.set_value(0.001), run_time=5.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- s11
class S11Reveal(SpokenScene):
    def construct(self):
        W = world(self, comp_on=True, left="after", right="teal", preds=(True, True))
        dk = dock()
        self.add(dk)
        sl, mt = top("source population", CXL, TEXT, 32), top("moved population", CXR, TEAL, 32)
        self.add(sl, mt)
        rows2 = ["age at maturity", "size at maturity"]
        cs = Card(-4.5, [0.45, 0.45], rows2, "source population", POP, 4.2, 3.5, 26, 28)
        cm = Card(0.0, [0.45, 0.45], rows2, "moved population", TEAL, 4.2, 3.5, 26, 28)
        cn = Card(4.5, [0.8, 0.8], rows2, "natural right reach", POP, 4.2, 3.5, 26, 28)
        for c in (cs, cm, cn):
            c.all().set_z_index(7)
        self.at("later")
        self.play(FadeIn(cs.all()), FadeIn(cm.all()), FadeIn(cn.all()), run_time=1.0)
        self.at("and at a larger size")
        new = [bar(cm.x0, cm.by[0], 0.62 * 3.5, TEAL), bar(cm.x0, cm.by[1], 0.6 * 3.5, TEAL)]
        for n_ in new:
            n_.set_z_index(7)
        lt = L("later", 34, TEAL).set_z_index(9); lt.move_to([cm.x0 + 0.62 * 3.5 + 0.15 + lt.width / 2, cm.by[0], 0])
        self.play(Transform(cm.bars[0], new[0]), FadeIn(lt, shift=RIGHT * 0.2), run_time=1.4)
        self.at("the moved population had changed")
        lg = L("larger", 34, TEAL).set_z_index(9); lg.move_to([cm.x0 + 0.6 * 3.5 + 0.15 + lg.width / 2, cm.by[1], 0])
        self.play(Transform(cm.bars[1], new[1]), FadeIn(lg, shift=RIGHT * 0.2), run_time=1.4)
        self.play(pulse(cm.box, 1.03), *[pulse(f, 1.25) for f in W.MV], run_time=1.5)
        self.at("direction life history theory")
        self.play(pulse(cm.bars[0], 1.06), pulse(cm.bars[1], 1.06), run_time=1.3)
        self.at("it matched the natural comparison")
        arc = ArcBetweenPoints([0.0, -0.3, 0], [4.5, -0.3, 0], angle=-1.2).set_stroke(TEAL, 5).set_z_index(8)
        ck = check(TEAL, 0.9).move_to([2.25, 0.62, 0]).set_z_index(9)
        self.play(Create(arc), run_time=0.9)
        self.play(FadeIn(ck, scale=1.5), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- s12
class S12Limits(SpokenScene):
    def construct(self):
        W = world(self, comp_on=True, left="after", right="teal", preds=(True, True))
        dk = dock()
        self.add(dk)
        sl, mt = top("source population", CXL, TEXT, 32), top("moved population", CXR, TEAL, 32)
        self.add(sl, mt)
        ga = Arrow([-5.4, -0.9, 0], [5.4, -0.9, 0], buff=0, color=GOLD, stroke_width=11, tip_length=0.35).set_z_index(7)
        self.play(GrowArrow(ga), run_time=0.8)
        self.at("rule out some explanations")
        stamp = VGroup(RoundedRectangle(corner_radius=0.12, width=5.1, height=0.95).set_stroke(GOLD, 6).set_fill(BG, 0.85), T("CHANGE TESTED", 38, GOLD, weight=BOLD)).set_z_index(9)
        stamp.move_to([0, -1.0, 0]).scale(1.6).set_opacity(0).rotate(-0.08)
        self.play(stamp.animate.scale(1 / 1.6).set_opacity(1), run_time=0.45, rate_func=rush_into)
        self.play(ga.animate.shift(DOWN * 0.06), rate_func=there_and_back, run_time=0.3)
        self.at("an observation leaves open")
        items = []
        for k, ((name, mk), x) in enumerate(zip(RIVALS, (-4.8, -1.6, 1.6, 4.8))):
            ic = mk().scale(0.8).move_to([x - 0.4, -3.5, 0])
            tag = L("?", 34, GREY).move_to([x + 0.35, -3.5, 0])
            items.append(VGroup(ic, tag))
        riv = VGroup(*items).set_opacity(0.4).set_z_index(8)
        self.play(FadeIn(riv, shift=UP * 0.2), run_time=1.0)
        self.at("but this is still one stream")
        t1 = VGroup(Triangle().scale(0.2).set_stroke(TEXT, 4).set_fill(BG, 1), T("!", 26, TEXT, weight=BOLD)).arrange(ORIGIN)
        t1 = VGroup(RoundedRectangle(corner_radius=0.12, width=6.1, height=0.7).set_stroke(TEXT, 3).set_fill(BG, 1), T("one stream, one introduction", 30, TEXT)).set_z_index(9).move_to([0, -2.05, 0])
        self.play(FadeIn(t1, shift=UP * 0.2), run_time=0.8)
        self.at("and the new reach differed")
        t2 = VGroup(RoundedRectangle(corner_radius=0.12, width=8.2, height=0.7).set_stroke(TEXT, 3).set_fill(BG, 1), T("new reach differs in more than predator", 30, TEXT)).set_z_index(9).move_to([0, -2.75, 0])
        self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.8)
        self.play(pulse(riv, 1.1), run_time=1.0)
        self.at("so it showed that the change of setting")
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(stamp), FadeOut(riv), run_time=0.7)
        ra = L("that the change caused evolution", 30, TEAL).set_z_index(9)
        rb = L("exactly how it did", 30, TEXT).set_z_index(9)
        la_ = Line([-5.2, -1.95, 0], [-5.2, -1.95, 0])
        ra.move_to([-3.3, -1.95, 0]); ra.shift(RIGHT * (-6.2 - ra.get_left()[0]))
        rb.move_to([-4.3, -3.0, 0]); rb.shift(RIGHT * (-6.2 - rb.get_left()[0]))
        lna = Line([ra.get_right()[0] + 0.3, -1.95, 0], [5.8, -1.95, 0]).set_stroke(TEAL, 14).set_z_index(9)
        lnb = DashedLine([rb.get_right()[0] + 0.3, -3.0, 0], [rb.get_right()[0] + 2.9, -3.0, 0], dash_length=0.2).set_stroke(TEXT, 5, opacity=0.8).set_z_index(9)
        self.play(FadeIn(ra, shift=RIGHT * 0.2), Create(lna), run_time=1.2)
        self.at("more firmly")
        self.play(pulse(lna, 1.04), run_time=1.0)
        self.at("exactly how")
        self.play(FadeIn(rb, shift=RIGHT * 0.2), Create(lnb), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------- s13 / s14
CARD_X = [-4.6, 0.0, 4.6]


def tool_card(cx, color, icon, name_lines, ans_lines):
    box = RoundedRectangle(corner_radius=0.2, width=4.3, height=5.9).set_stroke(color, 4).set_fill(color, 0.07).move_to([cx, -0.45, 0])
    icon.move_to([cx, 1.0, 0])
    txt = VGroup(*[T(n, 32, TEXT) for n in name_lines], *[T(a, 28, TEXT) for a in ans_lines]).arrange(DOWN, buff=0.14).move_to([cx, -1.55, 0])
    return VGroup(box, icon, txt)


def tools(sc, lit_n=2):
    """The three tool cards; lit_n of them lit, the rest dim. Returns the cards."""
    c1 = tool_card(CARD_X[0], GREY, icon_naturalist(GREY, 1.05), ["observation"], ["shows an", "association"])
    c2 = tool_card(CARD_X[1], GOLD, icon_experimenter(GOLD, 1.0), ["experimental", "contrast"], ["tests a cause"])
    c3 = tool_card(CARD_X[2], TEAL, icon_detective(TEAL, 1.05), ["historical", "inference"], ["tests rival pasts", "against traces"])
    return [c1, c2, c3]


class S13Ladder(SpokenScene):
    def construct(self):
        cards = tools(self)
        head = L("three tools", 38, TEXT).move_to([0, 3.3, 0])
        for c in cards:
            c[1].set_opacity(0)
            c[2].set_opacity(0)
            c[0].set_stroke(opacity=0)
            c[0].set_fill(opacity=0)
        self.add(*cards)
        self.at("three tools")
        self.play(FadeIn(head, shift=DOWN * 0.2), *[c[0].animate.set_stroke(opacity=1).set_fill(opacity=0.07) for c in cards], run_time=1.0)
        self.at("each for its own question")
        self.play(*[pulse(c[0], 1.03) for c in cards], run_time=1.3)
        self.at("observation of natural variation")
        self.play(cards[0][1].animate.set_opacity(1), cards[0][2][0].animate.set_opacity(1), run_time=1.2)
        self.at("an association")
        self.play(cards[0][2][1:].animate.set_opacity(1), run_time=0.8)
        self.at("an experimental contrast")
        self.play(cards[1][1].animate.set_opacity(1), cards[1][2][0:2].animate.set_opacity(1), run_time=1.3)
        self.at("tests a cause")
        self.play(cards[1][2][2:].animate.set_opacity(1), run_time=0.8)
        self.at("because the cause was changed")
        self.play(pulse(cards[1][1], 1.1), run_time=1.5)
        self.at("on purpose")
        self.play(cards[2][1].animate.set_opacity(0.2), cards[2][0].animate.set_stroke(opacity=0.35), pulse(cards[1][0], 1.02), run_time=1.5)
        self.finish()


class S14History(SpokenScene):
    def construct(self):
        cards = tools(self)
        head = L("three tools", 38, TEXT).move_to([0, 3.3, 0])
        cards[2][1].set_opacity(0.2)
        cards[2][0].set_stroke(opacity=0.35)
        cards[2][2].set_opacity(0)
        self.add(*cards, head)
        self.at("nobody can move a past event")
        h2 = L("a past event can't be moved", 38, TEXT).move_to([0, 3.3, 0])
        yr = chip("1977", color=TEXT, size=40).move_to([CARD_X[2], 1.2, 0]).set_z_index(9)
        xx = VGroup(Line([-0.5, -0.5, 0], [0.5, 0.5, 0]), Line([-0.5, 0.5, 0], [0.5, -0.5, 0])).set_stroke(TEXT, 8).move_to(yr).set_z_index(10)
        self.play(FadeOut(head), FadeIn(h2, shift=DOWN * 0.2), FadeIn(yr, scale=0.8), run_time=0.9)
        self.play(Create(xx), run_time=0.6)
        self.at("the third tool")
        self.play(FadeOut(yr), FadeOut(xx), cards[2][1].animate.set_opacity(1), cards[2][0].animate.set_stroke(opacity=1), run_time=1.2)
        self.at("historical inference")
        self.play(cards[2][2][0:2].animate.set_opacity(1), run_time=1.0)
        self.at("rival explanations")
        self.play(cards[2][2][2:].animate.set_opacity(1), run_time=1.0)
        self.at("traces")
        tr = VGroup(*[Dot([CARD_X[2] - 1.5 + 0.38 * k, 0.1 + 0.08 * (k % 2), 0], radius=0.07, color=TEAL) for k in range(8)]).set_z_index(9)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in tr], lag_ratio=0.2), run_time=1.6)
        self.at("past has left")
        self.play(pulse(cards[2][1], 1.08), run_time=1.5)
        self.at("each tool answers")
        h3 = L("each tool answers a different question", 36, TEXT).move_to([0, 3.3, 0])
        self.play(FadeOut(h2), FadeIn(h3, shift=DOWN * 0.2), FadeOut(tr), run_time=0.8)
        self.play(*[pulse(c[0], 1.03) for c in cards], run_time=1.0)
        self.play(*[c[0].animate.set_stroke(width=8) for c in cards], run_time=1.0)
        self.finish()


class S15End(EndCard):
    LINE = "Changing a cause on purpose tests what a comparison only suggests."
