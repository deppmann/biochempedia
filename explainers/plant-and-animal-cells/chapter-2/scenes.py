"""Looking at Real Cells (chapter 2 of the Plant and Animal Cells film pair).

COLOR MAP (same as chapter 1): cell wall TAN thick; membrane BLUE thin; central vacuole (tank) PALE BLUE;
nucleus PURPLE; mitochondria ORANGE; chloroplasts GREEN; light YELLOW. All schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TANC = "#C8A26B"
PALE = "#8EC9F2"
CELERY = "#A9C98A"

BX, BY = 2.4, -0.2          # the celery cell
BR = 1.85                   # its radius
BOXH = 2.15                 # half side of the wall
ACORNER = (-5.55, 2.85, 0.62)
ACENTRE = (-2.6, -0.2, 1.85)


def sup(th, a, n):
    c, s = np.abs(np.cos(th)), np.abs(np.sin(th))
    return a / ((c ** n + s ** n) ** (1.0 / n))


def sq_pts(c, a, n, N=96):
    th = np.linspace(0, 2 * np.pi, N, endpoint=False)
    r = sup(th, a, n)
    p = np.stack([c[0] + r * np.cos(th), c[1] + r * np.sin(th), np.zeros(N)], 1)
    return np.vstack([p, p[:1]])


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


class Cell:
    """A schematic cell driven by trackers: centre, radius, squareness, tank, water and pressure."""

    def __init__(self, sc, cx, cy, R, sq=0.0, tk=0.0, W=0.45, pr=0.0, kit_only=False):
        self.sc = sc
        self.cx, self.cy, self.R = ValueTracker(cx), ValueTracker(cy), ValueTracker(R)
        self.sq, self.tk, self.W, self.pr = ValueTracker(sq), ValueTracker(tk), ValueTracker(W), ValueTracker(pr)
        self.mem = VMobject(stroke_color=BLUE, stroke_width=4).set_z_index(6)
        self.cyto = VMobject(stroke_width=0, fill_color=GREY, fill_opacity=0.2).set_z_index(1)
        self.tank = VMobject(stroke_color=PALE, stroke_width=3, fill_color=PALE, fill_opacity=0.55).set_z_index(2)
        self.items = []   # (mob, base_r, angle, kind, idx)
        self.nuc = [Circle(radius=0.42, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.4)]
        self.er = [VGroup(*[ParametricFunction(lambda t, dy=dy: np.array([t, 0.09 * np.sin(t * 14) + dy, 0]),
                                               t_range=[-0.45, 0.45, 0.01], color=TEAL, stroke_width=5)
                            for dy in (-0.12, 0.12)])]
        self.mito = [Ellipse(width=0.76, height=0.4, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.4) for _ in range(3)]
        self.chl = [Ellipse(width=0.66, height=0.36, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4) for _ in range(6)]
        self.vac = [Circle(radius=0.18, stroke_color=PALE, stroke_width=3, fill_color=PALE, fill_opacity=0.5) for _ in range(2)]
        spec = [(self.nuc[0], 0.55, 130, "n"), (self.er[0], 0.8, 228, "n"),
                (self.mito[0], 0.85, 50, "n"), (self.mito[1], 0.9, 252, "n"), (self.mito[2], 0.88, 305, "n"),
                (self.vac[0], 0.45, 10, "v"), (self.vac[1], 0.5, 180, "v")]
        for m, r, a in zip(self.chl, [28, 72, 108, 152, 205, 330], [28, 72, 108, 152, 205, 330]):
            spec.append((m, 1.45, a, "n"))
        for i, (m, r, a, k) in enumerate(spec):
            m.kc = 1.0
            m.set_z_index(4)
            self.items.append((m, r, a, k, i))
        self.dots = VGroup(*[Dot(radius=0.05, color=TEXT) for _ in range(10)])
        self.dots.set_z_index(3)
        self.drv = Mobject()
        self.drv.add_updater(lambda m, dt: self.refresh())
        self.refresh()
        sc.add(self.drv)

    def refresh(self):
        c = np.array([self.cx.get_value(), self.cy.get_value(), 0.0])
        R = self.R.get_value()
        sq, tk, W = self.sq.get_value(), self.tk.get_value(), self.W.get_value()
        k = R / 1.85
        Am, nm = R * (1 + 0.11 * sq), 2 + 12 * sq
        p = sq_pts(c, Am, nm)
        self.mem.set_points_as_corners(p)
        self.cyto.set_points_as_corners(p)
        At, nt = tk * R * (0.4 + 0.44 * W), 2 + 10 * sq
        if At < 0.03:
            At = 0.03
        self.tank.set_points_as_corners(sq_pts(c, At, nt))
        t = self.sc.elapsed()
        for m, r, a, kind, i in self.items:
            th = np.radians(a)
            u = np.array([np.cos(th), np.sin(th), 0.0])
            base = u * r * k
            ring = u * (sup(th, Am, nm) + (sup(th, At, nt) if tk > 0.02 else 0)) / 2
            if kind == "v":
                q = base * (1 - min(1.0, tk * 1.5))
            else:
                q = base + (ring - base) * tk
            w = 0.1 * k * np.array([np.sin(0.8 * t + i * 1.7), np.cos(0.6 * t + i * 2.3), 0.0])
            if abs(k - m.kc) > 1e-4:
                m.scale(k / m.kc)
                m.kc = k
            m.move_to(c + q + w)
        for j, d in enumerate(self.dots):
            th = (0.3 * t * (1 if j % 2 else -1)) + j * 0.63
            fr = 0.3 + 0.55 * ((j * 0.37) % 1)
            d.move_to(c + fr * sup(th, Am, nm) * np.array([np.cos(th), np.sin(th), 0.0]))
            d.set_fill(opacity=0.55 * max(0.0, 1 - min(1.0, tk * 1.3)))

    def kit(self):
        return self.nuc + self.er + self.mito + self.vac

    def orgs(self):
        return self.nuc + self.er + self.mito + self.chl

    def add_kit(self, tint=True):
        self.sc.add(*([self.cyto, self.dots] if tint else []), self.mem, *self.kit())

    def stiff(self):
        return self.pr.get_value() * smooth((self.sq.get_value() - 0.35) / 0.65)

    def center(self):
        return np.array([self.cx.get_value(), self.cy.get_value(), 0.0])

    def edge(self, deg):
        th = np.radians(deg)
        sq = self.sq.get_value()
        r = sup(th, self.R.get_value() * (1 + 0.11 * sq), 2 + 12 * sq)
        return self.center() + r * np.array([np.cos(th), np.sin(th), 0.0])

    def dim(self, x):
        for m in self.orgs():
            m.set_stroke(opacity=x).set_fill(opacity=0.4 * x)


def lab(text, color, pos, target=None, size=28):
    t = T(text, size=size, color=color).move_to([pos[0], pos[1], 0])
    g = VGroup(t)
    if target is not None:
        target = np.array([target[0], target[1], 0.0])
        c = t.get_center()
        d = target - c
        if abs(d[0]) * 0.6 >= abs(d[1]):
            st = t.get_right() if d[0] > 0 else t.get_left()
        else:
            st = t.get_top() if d[1] > 0 else t.get_bottom()
        v = target - st
        st = st + v / np.linalg.norm(v) * 0.12
        g.add(Line(st, target, color=color, stroke_width=2.5), Dot(target, radius=0.06, color=color))
    return g


def wall(cx=BX, cy=BY, h=BOXH):
    return Rectangle(width=2 * h, height=2 * h, stroke_color=TANC, stroke_width=9).move_to([cx, cy, 0]).set_z_index(7)



# ============================================================================================
# CHAPTER 2: Looking at Real Cells.  Same colour map as chapter 1; the circle of light is the
# one world: it stays at the right of the frame, the left column holds labels and the sample.
# ============================================================================================
VC = np.array([2.5, 0.45, 0.0])     # centre of the circle of light
VR = 3.0                            # its radius
IODINE = "#B8862F"
STAINBLUE = "#4F83CC"
ONION = "#D9C48A"
LEFTX = -6.4                        # left edge of the label column


def tickmark(pos, size=0.32):
    p = np.array([pos[0], pos[1], 0.0])
    return VGroup(Line(p + [-0.55 * size, 0.0, 0], p + [-0.1 * size, -0.45 * size, 0]),
                  Line(p + [-0.1 * size, -0.45 * size, 0], p + [0.75 * size, 0.5 * size, 0])).set_stroke(GOLD, 9).set_z_index(15)


def left_align(g, y, x=LEFTX):
    g.move_to([0, y, 0])
    g.shift(RIGHT * (x - g.get_left()[0]))
    return g


def sample_card(name, stain, col):
    a = T(name, size=44, weight=BOLD)
    b = VGroup(Dot(radius=0.16, color=col), T(stain, size=32, color=col)).arrange(RIGHT, buff=0.25)
    g = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    return left_align(g, 2.55)


def schem(text="schematic", y=-3.35, x=None):
    return T(text, size=24, color=GREY).move_to([VC[0] if x is None else x, y, 0])


class View(VGroup):
    """The circle of light with its cells. .body drifts gently so the picture is never dead."""

    def __init__(self, disc, body, **kw):
        super().__init__(disc, body)
        self.disc, self.body = disc, body
        self.cells, self.nuc, self.chl, self.tanks, self.cluster, self.row = [], [], [], [], [], []


def disc(op=0.2):
    return Circle(radius=VR, stroke_color=YELLOW, stroke_width=5, fill_color="#F4EFD8", fill_opacity=op).move_to(VC).set_z_index(0)


def inside(pts, r=VR - 0.1):
    return all(np.hypot(p[0] - VC[0], p[1] - VC[1]) <= r for p in pts)


def sway(sc, v, amp=0.05):
    base = v.body.get_center().copy()

    def u(m):
        t = sc.elapsed()
        m.move_to(base + amp * np.array([np.sin(0.8 * t), np.cos(0.55 * t), 0.0]))
    v.body.add_updater(u)


def rim_light(sc, v=None):
    d = Dot(radius=0.1, color=YELLOW).set_z_index(9)

    def u(m):
        a = 0.7 * sc.elapsed() + 1.0
        m.move_to(VC + VR * np.array([np.cos(a), np.sin(a), 0.0]))
    d.add_updater(u)
    u(d)
    return d


def onion_view(nuc_op=0.9):
    cw, ch = 1.1, 0.52
    cells, nuc = [], []
    for r in range(-9, 10):
        y = VC[1] + r * ch
        off = cw / 2 if r % 2 else 0
        for k in range(-7, 8):
            x = VC[0] + k * cw + off
            cor = [(x + a * cw / 2, y + b * ch / 2, 0) for a in (-1, 1) for b in (-1, 1)]
            if not inside(cor):
                continue
            rc = Rectangle(width=cw, height=ch, stroke_color=TANC, stroke_width=4, fill_color=ONION, fill_opacity=0.38).move_to([x, y, 0])
            nx = x + 0.28 * (((r * 7 + k * 3) % 5) - 2) / 2
            n = Circle(radius=0.11, stroke_color=PURPLE, stroke_width=3, fill_color="#6B4A2B", fill_opacity=nuc_op).move_to([nx, y, 0])
            cells.append(rc)
            nuc.append(n)
    body = VGroup(*cells, *nuc)
    v = View(disc(), body)
    v.cells, v.nuc = cells, nuc
    return v


def waterweed_view(cluster_n=5, tanks=True, show_tanks=False):
    cw, ch = 0.85, 0.6
    cells, chl, cen = [], [], []
    for r in range(-8, 9):
        y = VC[1] + r * ch
        for k in range(-8, 9):
            x = VC[0] + k * cw
            cor = [(x + a * cw / 2, y + b * ch / 2, 0) for a in (-1, 1) for b in (-1, 1)]
            if not inside(cor):
                continue
            cells.append(Rectangle(width=cw, height=ch, stroke_color=TANC, stroke_width=4, fill_color="#3E6B3A", fill_opacity=0.28).move_to([x, y, 0]))
            cen.append(np.array([x, y, 0.0]))
    tgt = VC + np.array([0.6, 0.75, 0])
    order = sorted(range(len(cells)), key=lambda i: np.hypot(*(cen[i][:2] - tgt[:2])))
    cluster = sorted(order[:cluster_n])
    offs = [(-0.22, 0.14), (0.2, 0.16), (-0.08, -0.15), (0.24, -0.11), (-0.26, -0.09)]
    tk = []
    for i, c in enumerate(cen):
        mine = []
        if i in cluster:
            if tanks:
                t = RoundedRectangle(corner_radius=0.12, width=cw * 0.62, height=ch * 0.58, stroke_color=PALE, stroke_width=3,
                                     fill_color=PALE, fill_opacity=0.6).move_to(c)
                tk.append(t)
        else:
            for j, (dx, dy) in enumerate(offs):
                e = Ellipse(width=0.22, height=0.13, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.5)
                e.base = c + np.array([dx * (1 + 0.05 * ((i + j) % 3)), dy * (1 + 0.05 * ((i * 2 + j) % 3)), 0])
                e.ph = (i * 0.7 + j * 1.9)
                e.move_to(e.base)
                mine.append(e)
        chl.append(mine)
    allc = [e for m in chl for e in m]
    body = VGroup(*cells, *(tk if show_tanks else []), *allc)
    v = View(disc(), body)
    v.cells, v.chl, v.cluster, v.tanks, v.cen = cells, chl, cluster, tk, cen
    v.allc = allc
    v.cluster_c = np.mean([cen[i] for i in cluster], axis=0) if cluster else np.array(VC)
    return v


def stream(sc, v):
    """Chloroplasts drift slowly inside their cells (cytoplasmic streaming), so a held frame still moves."""
    def u(m):
        t = sc.elapsed()
        for e in v.allc:
            e.move_to(e.base + 0.045 * np.array([np.sin(0.9 * t + e.ph), np.cos(0.7 * t + e.ph), 0.0]))
    d = Mobject()
    d.add_updater(lambda m, dt: u(m))
    sc.add(d)
    return d


def blob(c, a, b, seed, nuc=True):
    rs = np.random.RandomState(seed)
    p1, p2 = rs.uniform(0, 6.3, 2)
    th = np.linspace(0, 2 * np.pi, 48, endpoint=False)
    r = 1 + 0.07 * np.sin(3 * th + p1) + 0.05 * np.sin(5 * th + p2)
    pts = np.stack([c[0] + a * r * np.cos(th), c[1] + b * r * np.sin(th), np.zeros(48)], 1)
    pts = np.vstack([pts, pts[:1]])
    m = VMobject(stroke_color=BLUE, stroke_width=2.5, fill_color=STAINBLUE, fill_opacity=0.38)
    m.set_points_as_corners(pts)
    n = Circle(radius=0.12, stroke_color=PURPLE, stroke_width=3, fill_color="#2F4F8F", fill_opacity=0.7).move_to([c[0] + 0.1 * (rs.rand() - 0.5), c[1], 0])
    return m, n, pts


def cheek_view():
    cells, nuc, row = [], [], []
    w = 2 * VR / 8
    for i in range(8):
        c = [VC[0] - VR + (i + 0.5) * w, VC[1] + 0.04 * ((i * 3) % 3 - 1), 0]
        m, n, _ = blob(c, w * 0.47, 0.3 + 0.03 * (i % 3), 10 + i)
        cells.append(m)
        nuc.append(n)
        row.append(m)
    sc_pos = [(-1.9, 1.15, .6, .36), (-0.5, 1.3, .55, .38), (1.0, 1.15, .62, .36), (2.15, 1.5, .5, .33),
              (-1.2, 2.05, .6, .38), (0.4, 2.15, .62, .36), (-0.3, 2.65, .5, .27),
              (-1.9, -1.2, .6, .36), (-0.4, -1.3, .58, .38), (1.1, -1.15, .6, .36), (2.2, -1.45, .5, .33),
              (-1.1, -2.05, .62, .38), (0.5, -2.15, .6, .36), (0.1, -2.7, .5, .26)]
    for j, (dx, dy, a, b) in enumerate(sc_pos):
        c = [VC[0] + dx, VC[1] + dy, 0]
        m, n, pts = blob(c, a, b, 40 + j)
        if inside(pts, VR - 0.08):
            cells.append(m)
            nuc.append(n)
    body = VGroup(*cells, *nuc)
    v = View(disc(), body)
    v.cells, v.nuc, v.row = cells, nuc, row
    return v


def tagset(v):
    g = VGroup()
    for i, m in enumerate(v.row):
        c = m.get_center()
        g.add(VGroup(Circle(radius=0.23, stroke_color=GOLD, stroke_width=3, fill_color=BG, fill_opacity=1),
                     T(str(i + 1), size=26, color=GOLD)).move_to([c[0], VC[1] + 0.68, 0]).set_z_index(12))
    return g


def width_arrow():
    y = VC[1] - VR - 0.42
    return DoubleArrow([VC[0] - VR, y, 0], [VC[0] + VR, y, 0], buff=0, color=GREY, stroke_width=6, tip_length=0.22,
                       max_tip_length_to_length_ratio=1)


def place(g, c, R):
    g.scale(R / VR, about_point=VC)
    g.shift(np.array([c[0], c[1], 0.0]) - VC)
    return g


def microscope(c=(-3.6, -0.35)):
    """Side view of a light microscope. Axis at x=0; height 5.4."""
    P = lambda x, y: np.array([x, y, 0.0])
    ink = dict(stroke_color=TEXT, stroke_width=4)
    base = RoundedRectangle(corner_radius=0.1, width=3.0, height=0.35, fill_color=GREY, fill_opacity=0.45, **ink).move_to(P(0.2, -2.52))
    arm = CubicBezier(P(1.1, -2.4), P(2.2, -1.8), P(2.2, 0.5), P(0.35, 1.2)).set_stroke(GREY, 18)
    stage = Rectangle(width=2.0, height=0.12, fill_color=GREY, fill_opacity=0.6, **ink).move_to(P(0, -1.0))
    slide = Rectangle(width=1.6, height=0.07, stroke_color=PALE, stroke_width=2, fill_color=PALE, fill_opacity=0.3).move_to(P(0, -0.92))
    tube = Rectangle(width=0.7, height=2.0, fill_color=GREY, fill_opacity=0.25, **ink).move_to(P(0, 0.95))
    obj = Rectangle(width=0.4, height=0.3, fill_color=GREY, fill_opacity=0.5, **ink).move_to(P(0, -0.12))
    eye = Rectangle(width=0.45, height=0.7, fill_color=GREY, fill_opacity=0.5, **ink).move_to(P(0, 2.25))
    lamp = Circle(radius=0.26, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(P(0, -2.18))
    g = VGroup(arm, base, stage, slide, tube, obj, eye, lamp)
    g.shift(P(c[0], c[1]))
    g.eyepiece_top = P(c[0], c[1] + 2.6)
    g.lamp_top = P(c[0], c[1] - 1.95)
    g.slide_c = P(c[0], c[1] - 0.92)
    return g


def eye_icon(pos):
    p = np.array([pos[0], pos[1], 0.0])
    e = Ellipse(width=1.0, height=0.5, stroke_color=TEXT, stroke_width=4)
    pu = Dot(radius=0.13, color=TEXT)
    return VGroup(e, pu).move_to(p)


def lens_icon(pos):
    p = np.array([pos[0], pos[1], 0.0])
    r = Circle(radius=0.42, stroke_color=TEXT, stroke_width=6, fill_color=PALE, fill_opacity=0.25)
    h = Line(p + [0.3, -0.3, 0], p + [0.8, -0.8, 0]).set_stroke(TEXT, 9)
    return VGroup(r.move_to(p), h)


def ruler_icon(pos, w=1.7):
    p = np.array([pos[0], pos[1], 0.0])
    b = Rectangle(width=w, height=0.5, stroke_color=TEXT, stroke_width=4, fill_color=GOLD, fill_opacity=0.25).move_to(p)
    t = VGroup(*[Line(p + [-w / 2 + 0.15 + i * (w - 0.3) / 8, 0.25, 0], p + [-w / 2 + 0.15 + i * (w - 0.3) / 8, 0.25 - (0.22 if i % 2 == 0 else 0.13), 0]).set_stroke(TEXT, 3)
                 for i in range(9)])
    return VGroup(b, t)


def pulse_walls(items, w=9):
    return [m.animate(rate_func=there_and_back).set_stroke(width=w) for m in items]


def celery_world(sc, cx, cy, R, h, full=True):
    B = Cell(sc, cx, cy, R, sq=1, tk=1, W=1, pr=1)
    B.add_kit()
    sc.remove(*B.vac)
    w = Rectangle(width=2 * h, height=2 * h, stroke_color=TANC, stroke_width=9 if R > 1.5 else 6).move_to([cx, cy, 0]).set_z_index(7)
    sc.add(*B.chl, B.tank, w)
    B.dim(1.0 if full else 0.3)
    B.w = w
    mobs = [B.cyto, B.dots, B.mem, *B.nuc, *B.er, *B.mito, *B.chl, B.tank, w]
    return B, mobs


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Plant Cells and Animal Cells"
    TITLE = "Looking at Real Cells"


class S01Hook(SpokenScene):
    def construct(self):
        paper = Rectangle(width=5.8, height=6.8, stroke_color=TEXT, stroke_width=3, fill_color="#2A2E38", fill_opacity=1).move_to([BX, -0.1, 0]).set_z_index(0)
        pencil = VGroup(Rectangle(width=0.28, height=3.0, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.8),
                        Triangle(fill_color=TANC, fill_opacity=1, stroke_color=TANC).scale(0.2).rotate(PI).shift(DOWN * 1.65)).rotate(0.4).move_to([-5.9, -0.5, 0])
        self.play(FadeIn(paper), FadeIn(pencil, shift=UP * 0.4), run_time=0.8)
        B, mobs = celery_world(self, BX, BY + 0.0, BR, BOXH)
        self.remove(*mobs)
        self.play(FadeIn(Group(*mobs)), run_time=1.0)
        self.at("drawing")
        stamp = VGroup(RoundedRectangle(corner_radius=0.1, width=3.0, height=0.95, stroke_color=RED, stroke_width=6),
                       T("drawing", size=48, color=RED, weight=BOLD)).rotate(0.18).move_to([-3.5, 2.7, 0])
        self.play(FadeIn(stamp, scale=1.5), run_time=0.5)
        self.at("kit")
        self.play(*[m.animate(rate_func=there_and_back).set_stroke(width=9) for m in B.nuc + B.er + B.mito], run_time=0.9)
        self.at("a box")
        self.play(B.w.animate(rate_func=there_and_back).set_stroke(width=16), run_time=0.8)
        self.at("water tank")
        self.play(B.tank.animate(rate_func=there_and_back).set_stroke(width=9), run_time=0.8)
        self.at("how do we know")
        q1 = chip("a real box?", color=TANC, size=36)
        q1.move_to([-3.6, 0.7, 0])
        self.play(FadeIn(q1, scale=0.6), run_time=0.6)
        self.play(Indicate(q1, color=TANC, scale_factor=1.1), run_time=0.9)
        self.at("how big")
        q2 = chip("how big?", color=YELLOW, size=36)
        q2.move_to([-3.6, -1.1, 0])
        self.play(FadeIn(q2, scale=0.6), run_time=0.6)
        self.play(Indicate(q2, color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.finish()


class S02Tools(SpokenScene):
    def construct(self):
        stalk = VGroup(Line([-5.4, -2.7, 0], [-5.4, 2.0, 0], color=CELERY, stroke_width=40, cap_style=CapStyleType.ROUND),
                       Ellipse(width=0.5, height=1.3, stroke_color=CELERY, stroke_width=3, fill_color=CELERY, fill_opacity=0.7).rotate(0.5).move_to([-5.1, 2.6, 0]),
                       Ellipse(width=0.5, height=1.3, stroke_color=CELERY, stroke_width=3, fill_color=CELERY, fill_opacity=0.7).rotate(-0.5).move_to([-5.7, 2.6, 0]))
        mc = np.array([-1.7, 0.4, 0.0])
        ring = Circle(radius=1.9, stroke_color=TEXT, stroke_width=8).move_to(mc)
        handle = Line(mc + [1.34, -1.34, 0], mc + [2.6, -2.6, 0]).set_stroke(TEXT, 16)
        blobs = VGroup(*[Circle(radius=rr, stroke_width=0, fill_color=col, fill_opacity=0.4).move_to(mc + np.array([dx, dy, 0]))
                         for rr, col, dx, dy in [(0.8, TANC, -0.5, 0.3), (0.7, GREEN, 0.5, 0.5), (0.8, PALE, 0.1, -0.5), (0.6, GREEN, -0.6, -0.6), (0.55, TANC, 0.7, -0.3)]])
        blobs.base = [b.get_center().copy() for b in blobs]

        def ub(m):
            t = self.elapsed()
            for i, b in enumerate(m):
                b.move_to(m.base[i] + 0.12 * np.array([np.sin(1.3 * t + i), np.cos(1.1 * t + 2 * i), 0]))
        blobs.add_updater(ub)
        self.play(FadeIn(stalk), run_time=0.8)
        self.at("cell")
        z1 = DashedLine([-5.2, 0.4, 0], mc + [-1.9, 0.1, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(ring), FadeIn(handle), Create(z1), run_time=0.9)
        self.at("too small")
        self.play(FadeIn(blobs), run_time=0.8)
        lab1 = T("too small to see", size=36).move_to([3.5, 0.4, 0])
        self.play(FadeIn(lab1, shift=LEFT * 0.3), run_time=0.7)
        self.at("model's parts")
        self.play(*[b.animate(rate_func=there_and_back).set_fill(opacity=0.8) for b in blobs], run_time=0.7)
        self.play(FadeOut(stalk), FadeOut(ring), FadeOut(handle), FadeOut(blobs), FadeOut(z1), FadeOut(lab1), run_time=0.5)
        ms = microscope((9.0, -0.35))
        self.add(ms)
        self.play(ms.animate.shift(LEFT * 12.6), run_time=1.0)
        self.at("light microscope")
        lm = T("light microscope", size=36).move_to([3.0, 2.6, 0])
        self.play(FadeIn(lm, shift=LEFT * 0.3), run_time=0.5)
        le = lens_icon((0.6, 0.9))
        ll = T("look", size=36, color=YELLOW).move_to([2.5, 0.9, 0])
        self.play(FadeIn(le), FadeIn(ll), run_time=0.6)
        self.at("a way to measure")
        ru = ruler_icon((0.8, -0.9))
        rl = T("measure", size=36, color=GOLD).move_to([3.2, -0.9, 0])
        self.play(FadeIn(ru, shift=UP * 0.2), FadeIn(rl), run_time=0.6)
        self.play(Indicate(ru, color=GOLD), run_time=1.0)
        self.finish()


class S03Wetmount(SpokenScene):
    def construct(self):
        slide = Rectangle(width=7.0, height=0.9, stroke_color=TEXT, stroke_width=3, fill_color=PALE, fill_opacity=0.12).move_to([0, -2.0, 0])
        bulb = VGroup(Circle(radius=1.4, stroke_color="#B9A878", stroke_width=5, fill_color="#E8DFC0", fill_opacity=0.5),
                      Circle(radius=0.95, stroke_color="#B9A878", stroke_width=3), Circle(radius=0.5, stroke_color="#B9A878", stroke_width=3)).move_to([0, 1.7, 0])
        self.play(FadeIn(slide), FadeIn(bulb), run_time=0.9)
        sheet = Rectangle(width=2.0, height=0.14, stroke_color="#E8DFC0", stroke_width=2, fill_color="#E8DFC0", fill_opacity=0.5).move_to([1.2, 0.5, 0]).set_z_index(5)
        tw = VGroup(Line(ORIGIN, [1.4, 1.3, 0]), Line([0.05, -0.1, 0], [1.5, 1.2, 0])).set_stroke(TEXT, 7).set_z_index(6)
        tw.add_updater(lambda m: m.move_to(sheet.get_right() + np.array([0.55, 0.75, 0])))
        self.at("thin piece")
        self.play(FadeIn(sheet), FadeIn(tw), run_time=0.5)
        self.play(sheet.animate.move_to([0.2, 0.6, 0]), run_time=0.4)
        self.at("onion skin")
        l1 = lab("onion skin", TEXT, (-4.6, -0.3), (-0.8, -1.55), size=32)
        self.play(sheet.animate.move_to([0, -1.55, 0]), FadeIn(l1), run_time=1.1)
        self.at("drop of", lead=0.5)
        tw.clear_updaters()
        dr = Circle(radius=0.2, stroke_width=0, fill_color=IODINE, fill_opacity=0.95).move_to([0.3, 1.6, 0])
        l2 = lab("iodine stain", "#E0A83E", (4.7, -3.2), (0.9, -1.75), size=32)
        self.play(FadeIn(dr), FadeOut(tw), run_time=0.3)
        self.play(dr.animate.move_to([0.3, -1.35, 0]), FadeIn(l2), run_time=0.8, rate_func=rush_into)
        spread = Ellipse(width=3.0, height=0.34, stroke_width=0, fill_color=IODINE, fill_opacity=0.65).move_to([0, -1.68, 0]).set_z_index(4)
        self.play(ReplacementTransform(dr, spread), run_time=0.5)
        self.at("thin glass", lead=0.3)
        slip = Rectangle(width=2.9, height=0.08, stroke_color=TEXT, stroke_width=2, fill_color=PALE, fill_opacity=0.55).set_z_index(8)
        slip.rotate(0.45).move_to([0.9, -0.5, 0])
        self.play(FadeIn(slip), run_time=0.3)
        self.play(slip.animate.rotate(-0.45).move_to([0, -1.43, 0]), run_time=1.4)
        l3 = lab("cover slip", PALE, (4.7, -0.2), (1.2, -1.43), size=32)
        self.play(FadeIn(l3), run_time=0.6)
        self.finish()


class S04Light(SpokenScene):
    def construct(self):
        ms = microscope()
        thin = Rectangle(width=0.8, height=0.045, stroke_width=0, fill_color=IODINE, fill_opacity=0.9).move_to(ms.slide_c + [0, 0.06, 0])
        self.add(ms, thin)
        f = ValueTracker(0.0)
        y0, y1 = ms.lamp_top[1], ms.eyepiece_top[1] - 0.1
        x = ms.lamp_top[0]
        beam = Polygon([x - 0.3, y0, 0], [x + 0.3, y0, 0], [x + 0.1, y1, 0], [x - 0.1, y1, 0], stroke_width=0, fill_color=YELLOW, fill_opacity=0.38).set_z_index(9)

        def ub(m):
            ff = max(0.02, f.get_value())
            top = y0 + (y1 - y0) * ff
            wtop = 0.3 - 0.2 * ff
            m.set_points_as_corners([[x - 0.3, y0, 0], [x + 0.3, y0, 0], [x + wtop, top, 0], [x - wtop, top, 0], [x - 0.3, y0, 0]])
        beam.add_updater(ub)
        self.add(beam)
        self.play(f.animate.set_value(0.62), run_time=1.6, rate_func=linear)
        self.at("thin layer", lead=0.0)
        self.play(thin.animate(rate_func=there_and_back).set_fill(opacity=1.0).scale(1.6), run_time=1.0)
        self.at("eyepiece")
        eye = eye_icon((x, ms.eyepiece_top[1] + 0.5))
        self.play(f.animate.set_value(1.0), FadeIn(eye), run_time=1.0)
        self.at("circle of light", lead=0.8)
        d = disc()
        lines = DashedLine(eye.get_right() + [0.1, 0, 0], VC + [-VR, 0.7, 0], color=YELLOW, stroke_width=3)
        self.play(Create(lines), run_time=0.5)
        self.play(GrowFromCenter(d), run_time=1.0)
        lc = T("circle of light", size=36).move_to(VC)
        self.play(FadeIn(lc), run_time=0.6)
        rl = rim_light(self)
        self.add(rl)
        self.finish()


class S05Onion(SpokenScene):
    def construct(self):
        v = onion_view(nuc_op=0.18)
        self.add(v.disc)
        rl = rim_light(self)
        self.add(rl)
        sw = sway(self, v)
        card = sample_card("onion skin", "iodine stain", "#E0A83E")
        self.play(FadeIn(card), run_time=0.6)
        self.at("onion skin cells")
        self.play(FadeIn(v.body, lag_ratio=0.0), run_time=1.4)
        self.at("side by side")
        self.play(*[m.animate(rate_func=there_and_back).set_stroke(width=7) for m in v.cells[::2]], run_time=1.4)
        self.at("long boxes")
        sel = min(range(len(v.cells)), key=lambda i: np.hypot(*(v.cells[i].get_center()[:2] - (VC[:2] + [-1.4, 0.4]))))
        c = v.cells[sel]
        self.play(c.animate.set_stroke(width=12, color=TANC), run_time=0.5)
        wl = lab("wall", TANC, (-3.6, 0.9), c.get_left(), size=34)
        self.play(FadeIn(wl), run_time=0.6)
        self.at("stain makes")
        self.play(*[n.animate.set_fill(opacity=0.9) for n in v.nuc], run_time=0.8)
        self.at("nucleus")
        sel2 = min(range(len(v.cells)), key=lambda i: np.hypot(*(v.cells[i].get_center()[:2] - (VC[:2] + [-0.7, -0.8]))))
        nl = lab("nucleus", PURPLE, (-3.6, -0.7), v.nuc[sel2].get_center() + [-0.12, 0, 0], size=34)
        self.play(FadeIn(nl), v.nuc[sel2].animate.scale(1.5), run_time=0.7)
        sc_ = schem()
        self.add(sc_)
        self.finish()


class S06Nogreen(SpokenScene):
    def construct(self):
        v = onion_view()
        self.add(v)
        rl = rim_light(self)
        self.add(rl)
        sway(self, v)
        card = sample_card("onion skin", "iodine stain", "#E0A83E")
        self.add(card, schem())
        self.at("notice")
        ch = Ellipse(width=1.1, height=0.6, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.6).move_to(VC + [-2.3, 2.0, 0]).set_z_index(10)
        self.play(FadeIn(ch, scale=0.5), run_time=0.6)
        path = [(-2.3, -1.2), (-0.4, 0.2), (-1.9, -0.4), (1.5, 1.6), (0.6, -1.5)]
        for dx, dy in path:
            self.play(ch.animate.move_to(VC + [dx, dy, 0]), run_time=0.55)
            self.wait(0.12)
        self.at("not green", lead=0.1)
        dash = Line(ch.get_center() + [-0.5, 0, 0], ch.get_center() + [0.5, 0, 0], color=GREY, stroke_width=10).set_z_index(10)
        self.play(FadeOut(ch), FadeIn(dash), run_time=0.6)
        l1 = T("no chloroplasts seen", size=34).move_to([-3.6, 0.0, 0])
        l1.shift(RIGHT * (LEFTX - l1.get_left()[0]))
        self.play(FadeIn(l1, shift=RIGHT * 0.3), run_time=0.7)
        self.play(FadeOut(dash), run_time=0.4)
        self.at("walls")
        self.play(*pulse_walls(v.cells, 11), run_time=1.2)
        self.at("developed chloroplasts")
        self.play(l1.animate.set_color(GREEN).scale(1.04), run_time=0.8)
        self.finish()


class S07Waterweed(SpokenScene):
    def construct(self):
        o = onion_view()
        self.add(o)
        rl = rim_light(self)
        self.add(rl)
        card = sample_card("onion skin", "iodine stain", "#E0A83E")
        self.add(card)
        stem = VMobject(stroke_color=GREEN, stroke_width=8)
        stem.set_points_as_corners([[-3.6, -0.2, 0], [-3.5, 0.8, 0], [-3.7, 1.8, 0]])
        leaves = VGroup(*[Ellipse(width=0.9, height=0.38, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.55).rotate(a).move_to([p[0], p[1], 0])
                          for a, p in [(0.6, (-3.0, 0.1)), (-0.6, (-4.1, 0.2)), (0.6, (-3.0, 0.8)), (-0.6, (-4.1, 0.9)), (0.6, (-3.1, 1.5)), (-0.6, (-4.2, 1.6))]])
        sprig = VGroup(stem, leaves).shift(DOWN * 0.3)
        card2 = sample_card("waterweed leaf", "water", BLUE)
        self.play(FadeOut(o.body), FadeOut(card), FadeIn(card2), FadeIn(sprig), run_time=0.7)
        self.at("waterweed leaf")
        self.play(Indicate(leaves[0], color=GREEN, scale_factor=1.3), run_time=0.8)
        self.at("mounted in")
        leaf = leaves[1].copy()
        wd = Ellipse(width=2.8, height=0.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3).move_to([-3.6, -1.6, 0])
        self.play(FadeIn(wd), leaf.animate.move_to([-3.6, -1.5, 0]).rotate(-0.4), run_time=1.2)
        v = waterweed_view(cluster_n=0, tanks=False)
        sway(self, v)
        self.at("cells are boxy")
        self.play(FadeIn(v.body), run_time=1.0)
        self.add(stream(self, v))
        self.play(*pulse_walls(v.cells, 8), run_time=1.2)
        self.at("packed")
        self.play(*[m.animate.set_fill(opacity=0.9).scale(1.12) for m in v.allc[::3]], run_time=1.2)
        t = T("tens to hundreds per cell", size=30, color=GREEN)
        t.move_to([-3.6, -2.9, 0])
        self.play(FadeIn(t), run_time=0.7)
        self.add(schem())
        self.finish()


class S08Cheek(SpokenScene):
    def construct(self):
        rl = rim_light(self)
        self.add(disc(), rl)
        card = sample_card("cheek cells", "blue stain", STAINBLUE)
        self.add(card)
        sl = Rectangle(width=3.8, height=0.5, stroke_color=TEXT, stroke_width=3, fill_color=PALE, fill_opacity=0.12).move_to([-3.6, -0.3, 0])
        self.at("few cells")
        pale = VGroup(*[Ellipse(width=0.6, height=0.2, stroke_color="#C9C3B5", stroke_width=2, fill_color="#C9C3B5", fill_opacity=0.5).move_to([-4.7 + i * 0.7, -0.3 + 0.07 * ((i * 3) % 3 - 1), 0]) for i in range(4)])
        self.play(FadeIn(sl), FadeIn(pale, shift=DOWN * 0.3), run_time=1.2)
        self.at("blue stain", lead=0.6)
        dr = Circle(radius=0.2, stroke_width=0, fill_color=STAINBLUE, fill_opacity=0.95).move_to([-3.6, 1.0, 0])
        self.play(FadeIn(dr), run_time=0.3)
        self.play(dr.animate.move_to([-3.6, -0.15, 0]), run_time=0.7, rate_func=rush_into)
        self.play(FadeOut(dr), *[p.animate.set_fill(STAINBLUE, 0.6).set_stroke(STAINBLUE) for p in pale], run_time=0.6)
        v = cheek_view()
        sway(self, v)
        self.play(FadeIn(v.body), run_time=1.2)
        self.at("no box")
        c0 = v.row[3]
        cc = c0.get_center()
        g = DashedVMobject(Rectangle(width=1.1, height=1.1, stroke_color=TANC, stroke_width=7)).move_to(cc)
        cross = VGroup(Line(cc + [-0.5, 0.5, 0], cc + [0.5, -0.5, 0]), Line(cc + [-0.5, -0.5, 0], cc + [0.5, 0.5, 0])).set_stroke(RED, 7).set_z_index(12)
        nb = lab("no box", RED, (-3.6, 1.2), cc + [-0.5, 0.4, 0], size=36)
        self.play(FadeIn(g), Create(cross), FadeIn(nb), run_time=0.9)
        self.add(T("outline only; the membrane itself is too thin to see", size=22, color=GREY).move_to([VC[0], -3.3, 0]))
        self.play(FadeOut(sl), FadeOut(pale), run_time=0.5)
        self.at("thin and flat")
        fl = VGroup(T("thin and flat", size=36).move_to([-3.6, -0.6, 0]))
        side = Ellipse(width=2.2, height=0.28, stroke_color=BLUE, stroke_width=4, fill_color=STAINBLUE, fill_opacity=0.5).move_to([-3.6, -1.3, 0])
        self.play(FadeIn(fl), FadeIn(side), run_time=0.7)
        self.at("tiles on")
        floor = VGroup(*[Ellipse(width=1.0, height=0.2, stroke_color=BLUE, stroke_width=3, fill_color=STAINBLUE, fill_opacity=0.5).move_to([-5.4 + i * 1.2, -2.2, 0]) for i in range(4)])
        ft = T("tiles on a floor", size=34).move_to([-3.6, -2.9, 0])
        self.play(FadeIn(floor, lag_ratio=0.3), FadeIn(ft), run_time=1.0)
        self.finish()


class S09Compare(SpokenScene):
    def construct(self):
        R, cy = 1.9, 0.25
        cx = [-4.4, 0.0, 4.4]
        cheek = cheek_view()
        self.add(cheek)
        q = chip("a real box?", color=TANC, size=34).move_to([-3.4, 3.2, 0])
        self.add(q)
        tk = tickmark([q.get_right()[0] + 0.5, 3.2], 0.5)
        self.play(cheek.animate.scale(R / VR, about_point=VC).shift(np.array([cx[2], cy, 0]) - VC), Create(tk), run_time=1.6)
        self.add(T("cheek", size=32, color=STAINBLUE).move_to([cx[2], cy - R - 0.45, 0]))
        o = onion_view()
        place(o, [cx[0], cy], R)
        w = waterweed_view(cluster_n=0, tanks=False)
        place(w, [cx[1], cy], R)
        self.at("box is real", lead=0.0)
        self.play(FadeIn(o), FadeIn(w), run_time=1.0)
        l1 = T("onion", size=32, color=TEXT).move_to([cx[0], cy - R - 0.45, 0])
        l2 = T("waterweed", size=32, color=GREEN).move_to([cx[1], cy - R - 0.45, 0])
        self.add(l1, l2)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.3)
        self.at("straight walls")
        self.play(*pulse_walls(o.cells + w.cells, 10), run_time=1.6)
        self.at("thin outline")
        self.play(cheek.disc.animate.set_stroke(BLUE, 8), *[m.animate(rate_func=there_and_back).set_stroke(width=6) for m in cheek.cells[:8]], run_time=1.4)
        self.at("no wall")
        nw = T("no wall", size=36, color=RED).move_to([cx[2], cy + R + 0.6, 0])
        self.play(FadeIn(nw), run_time=0.6)
        self.add(T("circles not drawn to the same scale", size=24, color=GREY).move_to([0, -3.4, 0]))
        self.finish()


class S10Unit(SpokenScene):
    def construct(self):
        y = 0.4
        band = Rectangle(width=12.0, height=1.1, stroke_color=TEXT, stroke_width=3, fill_color=GOLD, fill_opacity=0.12).move_to([0, y, 0])
        ticks = VGroup(*[Line([-6 + i, y + 0.55, 0], [-6 + i, y + 0.15, 0]).set_stroke(TEXT, 4) for i in range(13)])
        nums = VGroup(*[T(str(i), size=26, color=TEXT).move_to([-6 + i, y - 0.9, 0]) for i in range(0, 13, 2)])
        unit = T("millimeters", size=30, color=GOLD).move_to([0, y + 1.3, 0])
        self.play(FadeIn(band), Create(ticks), FadeIn(nums), run_time=1.0)
        self.play(FadeIn(unit), run_time=0.5)
        self.at("how big")
        q = chip("how big?", color=YELLOW, size=36).move_to([0, 3.0, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.at("measure cells", lead=0.0)
        gap = Rectangle(width=1.0, height=1.1, stroke_color=YELLOW, stroke_width=6).move_to([-5.5, y, 0])
        self.play(Create(gap), FadeOut(unit), run_time=0.7)
        big = Rectangle(width=12.0, height=1.1, stroke_color=YELLOW, stroke_width=6, fill_color=YELLOW, fill_opacity=0.08).move_to([0, y, 0])
        l0 = T("0", size=30).move_to([-6.0, y - 0.9, 0])
        l1 = T("1 millimeter", size=30, color=YELLOW).move_to([4.7, y - 0.9, 0])
        self.at("micrometers", lead=0.4)
        self.play(FadeOut(ticks), FadeOut(nums), FadeOut(band), FadeOut(q), ReplacementTransform(gap, big), run_time=1.6)
        self.play(FadeIn(l0), FadeIn(l1), run_time=0.4)
        sl = VMobject(stroke_color=TEXT, stroke_width=1.4)
        N = 1000
        for i in range(N):
            x = -6 + 12.0 * (i + 0.5) / N
            sl.start_new_path(np.array([x, y - 0.5, 0.0]))
            sl.add_line_to(np.array([x, y + 0.5, 0.0]))
        sl.set_opacity(0.0)
        self.add(sl)
        self.play(sl.animate.set_stroke(opacity=0.75), run_time=1.3)
        t1 = T("1000 thin slices", size=36, color=TEXT).move_to([0, y + 1.3, 0])
        self.play(FadeIn(t1), run_time=0.6)
        self.at("one micrometer")
        xg = -6 + 12.0 * 500.5 / N
        glow = Rectangle(width=0.1, height=1.4, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([xg, y, 0]).set_z_index(10)
        halo = Rectangle(width=0.4, height=1.8, stroke_width=0, fill_color=YELLOW, fill_opacity=0.25).move_to([xg, y, 0]).set_z_index(9)
        ar = Arrow([xg, y - 2.0, 0], [xg, y - 0.8, 0], buff=0, color=YELLOW, stroke_width=8, tip_length=0.25)
        lb = T("1 micrometer (µm)", size=40, color=YELLOW).move_to([xg, y - 2.5, 0])
        lb2 = T("= 1/1000 mm", size=36).move_to([xg, y - 3.15, 0])
        self.play(FadeOut(t1), FadeIn(halo), FadeIn(glow), GrowArrow(ar), run_time=0.9)
        self.play(FadeIn(lb), FadeIn(lb2), run_time=0.7)
        self.play(halo.animate(rate_func=there_and_back).scale(1.8), run_time=1.3)
        self.finish()


def count_view(sc, with_tags=True, arrow_label=None):
    v = cheek_view()
    sway(sc, v)
    rl = rim_light(sc)
    sc.add(v, rl)
    ar = width_arrow()
    tags = tagset(v)
    return v, rl, ar, tags


class S11Rule(SpokenScene):
    def construct(self):
        v, rl, ar, tags = count_view(self)
        self.add(schem("schematic", y=-3.45, x=-4.5))
        self.at("tiny ruler", lead=0.0)
        rline = VGroup(Line([VC[0] - 2.4, VC[1] - 1.1, 0], [VC[0] + 2.4, VC[1] - 1.1, 0]).set_stroke(YELLOW, 5),
                       *[Line([VC[0] - 2.4 + i * 0.4, VC[1] - 1.1, 0], [VC[0] - 2.4 + i * 0.4, VC[1] - 1.1 + (0.28 if i % 5 == 0 else 0.16), 0]).set_stroke(YELLOW, 4) for i in range(13)]).set_z_index(11)
        self.play(Create(rline), run_time=1.2)
        rl_ = lab("eyepiece ruler", YELLOW, (-3.6, -0.65), (VC[0] - 2.4, VC[1] - 1.1), size=34)
        self.play(FadeIn(rl_), run_time=0.6)
        self.at("In class", lead=0.0)
        self.play(FadeOut(rline), FadeOut(rl_), run_time=0.6)
        self.at("circle of light itself", lead=0.0)
        self.play(v.disc.animate(rate_func=there_and_back).set_stroke(YELLOW, 14), run_time=1.0)
        self.play(GrowFromCenter(ar), run_time=0.6)
        lw = T("circle width", size=34, color=GREY).move_to([VC[0], -3.45, 0])
        self.play(FadeIn(lw), run_time=0.5)
        self.at("cells lying")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.5) for t in tags], lag_ratio=0.5), run_time=3.2)
        self.at("then divide", lead=0.2)
        r2 = T("≈ circle width", size=36).move_to([0, 0.3, 0])
        left_align(r2, 0.3)
        self.play(FadeIn(r2), ar.animate(rate_func=there_and_back).set_color(YELLOW), run_time=1.2)
        self.at("that count", lead=0.3)
        r3 = left_align(T("÷ number of cells", size=36), -0.6)
        self.play(FadeIn(r3), *[t.animate(rate_func=there_and_back).scale(1.3) for t in tags], run_time=1.2)
        self.at("rough average")
        r1 = left_align(T("average cell width", size=40, color=GOLD, weight=BOLD), 1.3)
        self.play(FadeIn(r1, shift=DOWN * 0.2), run_time=0.7)
        hl = SurroundingRectangle(v.row[0], color=GOLD, buff=0.06, stroke_width=7)
        self.play(Create(hl), run_time=0.6)
        self.play(hl.animate.move_to(v.row[1].get_center()), run_time=0.8)
        self.finish()


class S12Predict(SpokenScene):
    def construct(self):
        v, rl, ar, tags = count_view(self)
        self.add(schem("schematic", y=-3.45, x=-4.5))
        self.add(ar)
        self.at("made")
        card = VGroup(T("made-up numbers", size=34), T("for practice", size=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        left_align(card, 1.9)
        bx = SurroundingRectangle(card, color=GREY, buff=0.25, corner_radius=0.12, stroke_width=3)
        self.play(FadeIn(card), Create(bx), run_time=0.9)
        self.at("circle's width")
        lw = M("450 µm", size=38, color=GOLD).move_to([VC[0], -3.45, 0])
        self.play(FadeIn(lw, shift=UP * 0.2), ar.animate(rate_func=there_and_back).set_color(YELLOW), run_time=1.0)
        self.at("cell count")
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in tags], lag_ratio=0.35), run_time=1.8)
        self.at("how wide")
        q = left_align(T("one cell ≈ ? µm", size=48, color=YELLOW, weight=BOLD), -0.3)
        self.play(FadeIn(q, scale=0.8), run_time=0.7)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.08), *[t.animate(rate_func=there_and_back).scale(1.25) for t in tags], run_time=1.2)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        v, rl, ar, tags = count_view(self)
        lw = M("450 µm", size=38, color=GOLD).move_to([VC[0], -3.45, 0])
        self.add(ar, tags, lw)
        q = VGroup(T("450 µm across,", size=44), T("8 cells:", size=44), T("one cell ≈ ? µm", size=48, color=YELLOW, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        left_align(q, 0.2)
        self.add(q)
        ring = Circle(radius=0.45, stroke_color=GREY, stroke_width=4).move_to([6.1, -3.1, 0])
        arc = Arc(radius=0.45, start_angle=PI / 2, angle=2 * PI, stroke_color=GOLD, stroke_width=8).move_to([6.1, -3.1, 0])
        t0 = self.elapsed()

        def ua(m):
            f = min(1.0, (self.elapsed() - t0) / max(0.1, self.narration_s - 0.5))
            m.become(Arc(radius=0.45, start_angle=PI / 2, angle=max(0.01, 2 * PI * (1 - f)), stroke_color=GOLD, stroke_width=8).move_to([6.1, -3.1, 0]))
        arc.add_updater(ua)
        self.add(ring, arc)
        self.finish()


class S14Reveal(SpokenScene):
    def construct(self):
        v, rl, ar, tags = count_view(self)
        lw = M("450 µm", size=38, color=GOLD).move_to([VC[0], -3.45, 0])
        self.add(ar, tags, lw)
        q = chip("how big?", color=YELLOW, size=32).move_to([-4.3, 3.1, 0])
        self.add(q)
        self.at("answer")
        eq = left_align(VGroup(T("450 ÷ 8 ≈", size=44), T("56 µm", size=48, color=GOLD, weight=BOLD)).arrange(RIGHT, buff=0.3), 1.5)
        self.play(FadeIn(eq, shift=RIGHT * 0.3), run_time=0.9)
        self.play(Indicate(eq[1], color=GOLD, scale_factor=1.15), run_time=1.0)
        self.at("published study")
        card = VGroup(T("published study:", size=34), T("55 µm", size=48, color=GREEN, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        left_align(card, -0.7)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        self.at("nearly the same")
        a56 = eq[1]
        a55 = card[1]
        cap1 = T("my count", size=28)
        cap2 = T("study", size=28)
        self.play(FadeOut(eq[0]), FadeOut(card[0]), a56.animate.move_to([-5.2, 0.4, 0]), a55.animate.move_to([-2.3, 0.4, 0]), run_time=1.2)
        cap1.next_to(a56, DOWN, buff=0.2)
        cap2.next_to(a55, DOWN, buff=0.2)
        ap = T("≈", size=60).move_to([-3.75, 0.4, 0])
        ab = T("about the same", size=34, color=YELLOW).move_to([-3.6, -1.1, 0])
        self.play(FadeIn(cap1), FadeIn(cap2), FadeIn(ap), FadeIn(ab), run_time=0.8)
        self.at("rough count lands")
        tk = tickmark([q.get_right()[0] + 0.5, 3.1], 0.55)
        self.play(Create(tk), *[t.animate(rate_func=there_and_back).scale(1.25) for t in tags], run_time=1.2)
        self.finish()


class S15Clear(SpokenScene):
    def construct(self):
        v = waterweed_view(tanks=False)
        self.add(v)
        sway(self, v)
        self.add(stream(self, v))
        rl = rim_light(self)
        self.add(rl, sample_card("waterweed leaf", "water", BLUE), schem())
        self.at("one more")
        self.play(*[m.animate(rate_func=there_and_back).set_stroke(width=7) for m in v.cells[::3]], run_time=1.4)
        self.at("scientists found")
        cd = left_align(VGroup(T("Hara and colleagues,", size=32), T("2015", size=32)).arrange(DOWN, aligned_edge=LEFT, buff=0.1), 0.9)
        self.play(FadeIn(cd), run_time=0.8)
        self.at("colorless")
        cc = v.cluster_c
        ring = DashedVMobject(Circle(radius=1.2, stroke_color=YELLOW, stroke_width=6)).move_to(cc)
        ring.add_updater(lambda m, dt: m.rotate(0.4 * dt))
        self.play(Create(ring), run_time=1.0)
        nl = lab("colorless cells", YELLOW, (-3.6, -0.5), cc + [-1.2, -0.2, 0], size=36)
        self.play(FadeIn(nl), run_time=0.7)
        self.at("these cells")
        self.play(*pulse_walls([v.cells[i] for i in v.cluster], 11), run_time=1.2)
        nc = left_align(T("no chloroplasts", size=36, color=GREEN), -1.6)
        self.play(FadeIn(nc), run_time=0.7)
        self.finish()


class S16Dye(SpokenScene):
    def construct(self):
        v = waterweed_view(tanks=True)
        self.add(v)
        sway(self, v)
        self.add(stream(self, v))
        rl = rim_light(self)
        cc = v.cluster_c
        ring = DashedVMobject(Circle(radius=1.2, stroke_color=YELLOW, stroke_width=6)).move_to(cc)
        ring.add_updater(lambda m, dt: m.rotate(0.4 * dt))
        self.add(rl, sample_card("waterweed leaf", "dye", PALE), schem(), ring)
        dots = VGroup(*[Dot(radius=0.09, color=PALE) for _ in range(12)])
        t0 = self.elapsed()

        def ud(m):
            t = self.elapsed() - t0
            for i, d in enumerate(m):
                ph = (t * 0.45 + i * 0.083) % 1
                d.move_to([VC[0] - VR + 6 * ph, VC[1] + 2.2 * np.sin(i * 2.1) * (1 - 0.3 * ph), 0])
                d.set_fill(opacity=np.sin(np.pi * ph) * 0.9)
        dots.add_updater(ud)
        self.add(dots)
        self.at("lit up", lead=0.5)
        self.play(LaggedStart(*[FadeIn(t) for t in v.tanks], lag_ratio=0.3), run_time=1.2)
        self.at("central vacuole")
        nl = lab("large central vacuole", PALE, (-3.6, 0.0), v.tanks[0].get_center() + [-0.3, 0, 0], size=34)
        self.play(FadeIn(nl), *[t.animate(rate_func=there_and_back).set_stroke(width=9) for t in v.tanks], run_time=1.0)
        self.play(FadeOut(dots), run_time=0.4)
        self.at("green leaf")
        self.play(*[m.animate(rate_func=there_and_back).set_stroke(width=5) for m in v.allc[::2]], run_time=1.4)
        self.at("not every")
        t = left_align(VGroup(T("not every plant cell", size=34), T("is green", size=40, color=GREEN, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12), -1.5)
        self.play(FadeIn(t), run_time=0.8)
        self.finish()


class S17Close(SpokenScene):
    def construct(self):
        R, cy = 1.45, -0.55
        cx = [-5.1, -1.7, 1.7, 5.1]
        o = place(onion_view(), [cx[0], cy], R)
        w = place(waterweed_view(cluster_n=0, tanks=False), [cx[1], cy], R)
        ch = place(cheek_view(), [cx[2], cy], R)
        w2 = place(waterweed_view(tanks=True, show_tanks=True), [cx[3], cy], R)
        self.play(FadeIn(o), FadeIn(w), FadeIn(ch), run_time=1.4)
        self.at("box is real", lead=0.2)
        B, mobs = celery_world(self, 0.0, 2.8, 0.78, 0.9, full=True)
        self.remove(*mobs)
        self.play(FadeIn(Group(*mobs)), run_time=0.7)
        # dashed lines from the model's parts to where they show
        top = lambda i: np.array([cx[i], cy + R + 0.02, 0.0])
        l_box = DashedLine([-0.92, 2.8, 0], top(0), color=TANC, stroke_width=4)
        l_box2 = DashedLine([-0.6, 1.9, 0], top(1) + [-0.4, 0, 0], color=TANC, stroke_width=4)
        lm = T("model's parts seen", size=32, color=YELLOW).move_to([-4.6, 2.9, 0])
        self.play(Create(l_box), Create(l_box2), FadeIn(lm), run_time=0.9)
        self.at("green chloroplasts")
        l_ch = DashedLine([-0.25, 2.0, 0], top(1) + [0.4, 0, 0], color=GREEN, stroke_width=4)
        self.play(Create(l_ch), *[m.animate(rate_func=there_and_back).set_stroke(width=8) for m in B.chl], run_time=1.0)
        self.at("water tank")
        self.play(FadeIn(w2), run_time=0.8)
        l_tk = DashedLine([0.3, 2.3, 0], top(3), color=PALE, stroke_width=4)
        self.play(Create(l_tk), B.tank.animate(rate_func=there_and_back).set_stroke(width=8), run_time=1.0)
        self.at("only some", lead=0.3)
        self.play(*[m.animate(rate_func=there_and_back).set_stroke(width=5) for m in w.allc[::2]], w2.disc.animate(rate_func=there_and_back).set_stroke(PALE, 10), run_time=1.6)
        self.at("many shapes", lead=0.5)
        i1 = Rectangle(width=1.6, height=0.5, stroke_color=TANC, stroke_width=5, fill_color=TANC, fill_opacity=0.25).move_to([-2.9, -3.0, 0])
        i2 = Rectangle(width=0.9, height=0.62, stroke_color=TANC, stroke_width=5, fill_color=TANC, fill_opacity=0.25).move_to([-0.8, -3.0, 0])
        i3 = Ellipse(width=1.5, height=0.2, stroke_color=BLUE, stroke_width=4, fill_color=STAINBLUE, fill_opacity=0.5).move_to([1.0, -3.0, 0])
        self.play(FadeIn(i1, shift=UP * 0.2), run_time=0.45)
        self.play(FadeIn(i2, shift=UP * 0.2), run_time=0.45)
        self.play(FadeIn(i3, shift=UP * 0.2), run_time=0.45)
        sz = T("many shapes and sizes", size=34).move_to([4.3, -3.0, 0])
        self.play(FadeIn(sz), run_time=0.6)
        self.finish()


class S18End(EndCard):
    LINE = "Under the microscope, plant cells show their box; only some are green."
