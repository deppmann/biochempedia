"""A Water Balloon in a Box: plant vs animal cells (grade 7 Life Science film, re-paced).

COLOR MAP: cell wall TAN thick; membrane BLUE thin; central vacuole (tank) PALE BLUE; water BLUE;
nucleus PURPLE; mitochondria ORANGE; chloroplasts GREEN; ER TEAL; cytoplasm GREY tint; light YELLOW;
stiffness meter GOLD. All schematic.
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


class Flow(VGroup):
    """Moving water arrows. specs: (far, near, inward)."""

    def __init__(self, sc, specs, gain=0.0):
        super().__init__()
        self.gain = ValueTracker(gain)
        for i, (far, near, inw) in enumerate(specs):
            far, near = np.array([far[0], far[1], 0.0]), np.array([near[0], near[1], 0.0])
            a, b = (far, near) if inw else (near, far)
            u = (b - a) / np.linalg.norm(b - a)
            ar = Arrow(-0.28 * u, 0.28 * u, buff=0, color=BLUE, stroke_width=9, tip_length=0.22,
                       max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=30)
            ar.a, ar.b, ar.i = a, b, i
            self.add(ar)
        def step():
            t = sc.elapsed()
            g = self.gain.get_value()
            for ar in self.submobjects:
                ph = (t * 0.45 + ar.i * 0.31) % 1
                ar.move_to(ar.a + (ar.b - ar.a) * ph)
                op = (np.sin(np.pi * ph) ** 0.5) * g
                ar.set_fill(opacity=op).set_stroke(opacity=op)
        self.step = step
        self.add_updater(lambda m, dt: step())
        step()


def b_specs(inward, sides="tbl"):
    s = []
    if "t" in sides:
        s += [((BX + x, 3.2), (BX + x, 2.4), inward) for x in (-1.0, 1.0)]
    if "b" in sides:
        s += [((BX + x, -3.6), (BX + x, -2.8), inward) for x in (-1.0, 1.0)]
    if "l" in sides:
        s += [((-0.6, BY + y), (0.05, BY + y), inward) for y in (-0.9, 0.9)]
    return s


class PushArrows(VGroup):
    """BLUE out-arrows in the ring and TAN in-arrows outside the wall; opacity follows cell.pr."""

    def __init__(self, sc, cell):
        super().__init__()
        self.blue, self.tan = [], []
        for ang in (0, 90, 180, 270):
            u = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0.0])
            b = Arrow(u * 1.62, u * 2.0, buff=0, color=BLUE, stroke_width=8, tip_length=0.2, max_tip_length_to_length_ratio=1).shift(np.array([BX, BY, 0]))
            t = Arrow(u * 2.85, u * 2.28, buff=0, color=TANC, stroke_width=9, tip_length=0.22, max_tip_length_to_length_ratio=1).shift(np.array([BX, BY, 0]))
            b.z_index, t.z_index = 8, 8
            b.base, t.base = b.get_center().copy(), t.get_center().copy()
            b.u, t.u = u, u
            self.blue.append(b)
            self.tan.append(t)
            self.add(b, t)
        def step():
            t = sc.elapsed()
            pr = cell.pr.get_value()
            for m in self.blue:
                m.move_to(m.base + m.u * 0.05 * np.sin(3 * t))
                m.set_fill(opacity=pr).set_stroke(opacity=pr)
            for m in self.tan:
                m.move_to(m.base - m.u * 0.05 * np.sin(3 * t))
                m.set_fill(opacity=pr).set_stroke(opacity=pr)
        self.step = step
        self.add_updater(lambda m, dt: step())
        step()


def make_meter(sc, fn, x=5.7, y0=-2.1, h=3.8):
    outline = Rectangle(width=0.5, height=h, stroke_color=GREY, stroke_width=3).move_to([x, y0 + h / 2, 0])
    fill = Rectangle(width=0.4, height=0.02, stroke_width=0, fill_color=GOLD, fill_opacity=0.95).move_to([x, y0 + 0.01, 0])

    def upd(m):
        hh = max(0.02, h * fn())
        m.become(Rectangle(width=0.4, height=hh, stroke_width=0, fill_color=GOLD, fill_opacity=0.95).move_to([x, y0 + hh / 2, 0]))
    fill.add_updater(upd)
    return outline, fill


class Checklist(VGroup):
    def __init__(self, ticked=0):
        super().__init__()
        self.rows = []
        for i, txt in enumerate(["1  box", "2  food makers", "3  water tank"]):
            sq_ = Square(0.42, stroke_color=GREY, stroke_width=3)
            tx = T(txt, size=30)
            row = VGroup(sq_, tx).arrange(RIGHT, buff=0.3)
            self.rows.append(row)
        g = VGroup(*self.rows).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([-4.4, 0.2, 0])
        self.add(*self.rows)
        self.ticks = []
        for i, row in enumerate(self.rows):
            s = row[0].get_center()
            tk = VGroup(Line(s + [-0.14, 0.0, 0], s + [-0.03, -0.14, 0]), Line(s + [-0.03, -0.14, 0], s + [0.18, 0.16, 0])).set_stroke(GOLD, 7)
            self.ticks.append(tk)
            if i < ticked:
                self.add(tk)

    def tick(self, i):
        return Create(self.ticks[i])


def box_icon(pos):
    r = Rectangle(width=0.8, height=0.55, stroke_color=TANC, stroke_width=4, fill_color=TANC, fill_opacity=0.35)
    f = Line(r.get_corner(UL), r.get_corner(UR)).shift(DOWN * 0.15).set_stroke(TANC, 4)
    return VGroup(r, f).move_to([pos[0], pos[1], 0])


def stalk_up(sc, base, L, d_tr, grow_tr=None, width=30):
    m = VMobject(stroke_color=CELERY, stroke_width=width, cap_style=CapStyleType.ROUND)

    def upd(mm):
        d = d_tr.get_value() + 0.03 * np.sin(1.7 * sc.elapsed())
        g = grow_tr.get_value() if grow_tr else 1.0
        n = 40
        s = np.linspace(0, L * g, n)
        th = np.pi / 2 - d * 1.9 * (s / L) ** 1.6
        ds = s[1] - s[0] if n > 1 else 0
        x = base[0] + np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * ds)])
        y = base[1] + np.concatenate([[0], np.cumsum(np.sin(th[:-1]) * ds)])
        mm.set_points_as_corners(np.stack([x, y, np.zeros(n)], 1))
    m.add_updater(upd)
    upd(m)
    return m


def stalk_ctr(sc, d_tr, base=(-6.4, -1.1), L=4.6, s0=2.8, width=30):
    m = VMobject(stroke_color=CELERY, stroke_width=width, cap_style=CapStyleType.ROUND)

    def upd(mm):
        d = d_tr.get_value() + 0.03 * np.sin(1.7 * sc.elapsed())
        n = 50
        s = np.linspace(0, L, n)
        th = np.array([-d * (np.pi / 2) * smooth((q - s0) / 1.2) for q in s])
        ds = s[1] - s[0]
        x = base[0] + np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * ds)])
        y = base[1] + np.concatenate([[0], np.cumsum(np.sin(th[:-1]) * ds)])
        mm.set_points_as_corners(np.stack([x, y, np.zeros(n)], 1))
    m.add_updater(upd)
    upd(m)
    return m


def plank():
    return Rectangle(width=3.4, height=0.22, stroke_width=0, fill_color=TANC, fill_opacity=0.9).move_to([-5.1, -1.4, 0])


def drops(sc, x0=-5.8, x1=-1.8, y0=-0.9, rise=2.2, n=8):
    g = VGroup(*[Dot(radius=0.1, color=BLUE) for _ in range(n)])
    for i, d in enumerate(g):
        d.i = i
    g.gain = ValueTracker(1.0)

    def upd(m):
        t = sc.elapsed()
        for d in m:
            ph = (t * 0.35 + d.i * 0.137) % 1
            x = x0 + (x1 - x0) * ((d.i * 0.618) % 1) + 0.15 * np.sin(2 * t + d.i)
            d.move_to([x, y0 + rise * ph, 0])
            op = np.sin(np.pi * ph) * m.gain.get_value()
            d.set_fill(opacity=op)
    g.add_updater(upd)
    upd(g)
    return g


def sun(sc, x_from=6.0, x_to=0.8, t0=0.0, dur=6.0):
    core = Circle(radius=0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
    rays = VGroup(*[Line(0.55 * np.array([np.cos(a), np.sin(a), 0]), 0.8 * np.array([np.cos(a), np.sin(a), 0]), color=YELLOW, stroke_width=5)
                    for a in np.linspace(0, 2 * np.pi, 9)[:-1]])
    g = VGroup(core, rays)

    def upd(m):
        f = min(1.0, max(0.0, (sc.elapsed() - t0) / dur))
        m.move_to([x_from + (x_to - x_from) * f, 3.1 - 0.4 * np.sin(np.pi * f), 0])
        rays.rotate(0.03)
    g.add_updater(upd)
    upd(g)
    return g


def ghost_label(g):
    return g


class S00Title(TitleCard):
    LESSON = "Plant Cells and Animal Cells"
    TITLE = "A Water Balloon in a Box"


# --------------------------------------------------------------------------------------------
def kid_parts(sc, hip, s, amp_tr, glass_tr):
    """Stick-figure kid that sways (bendy) and drinks from a glass."""
    limbs = VGroup(*[Line(ORIGIN, UP, stroke_width=w, color=TEXT).set_stroke(opacity=0.9) for w in (22, 14, 14, 14, 14)])
    for l in limbs:
        l.set_cap_style(CapStyleType.ROUND)
    head = Circle(radius=0.5 * s, stroke_color=TEXT, stroke_width=5, fill_color=BG, fill_opacity=1)
    gl = VGroup(Rectangle(width=0.4, height=0.55, stroke_color=TEXT, stroke_width=4),
                Rectangle(width=0.32, height=0.35, stroke_width=0, fill_color=BLUE, fill_opacity=0.7).shift(DOWN * 0.08))
    g = VGroup(limbs, head, gl)

    def R2(v, a):
        c, sn = np.cos(a), np.sin(a)
        return np.array([c * v[0] - sn * v[1], sn * v[0] + c * v[1], 0.0])
    hip = np.array([hip[0], hip[1], 0.0])

    def upd(m):
        phi = amp_tr.get_value() * np.sin(1.7 * sc.elapsed())
        up = R2(np.array([0, 1.0, 0]), phi)
        neck = hip + up * 1.7 * s
        sh = hip + up * 1.5 * s
        headc = neck + up * 0.5 * s
        mouth = headc + R2(np.array([0.35, -0.3, 0]), phi)
        gv = glass_tr.get_value()
        h1 = (sh + R2(np.array([0.7, -0.9, 0]) * s, phi)) * (1 - gv) + (mouth + np.array([0.25, 0, 0])) * gv
        h2 = sh + R2(np.array([-0.7, -0.9, 0]) * s, phi)
        pts = [(hip, neck), (hip, hip + np.array([0.45, -1.6, 0]) * s), (hip, hip + np.array([-0.45, -1.6, 0]) * s), (sh, h1), (sh, h2)]
        for l, (a, b) in zip(limbs, pts):
            l.put_start_and_end_on(a, b)
        head.move_to(headc)
        gl.move_to(h1 + np.array([0.12, 0.2, 0]))
    g.add_updater(upd)
    upd(g)
    return g


class S01Hook(SpokenScene):
    def construct(self):
        d = ValueTracker(1.0)
        grow = ValueTracker(1.0)
        stalk = stalk_up(self, (-3.4, -2.5), 4.4, d, grow)
        glass = VMobject(stroke_color=TEXT, stroke_width=6).set_z_index(5)
        glass.set_points_as_corners([[-4.35, -0.9, 0], [-4.15, -2.9, 0], [-2.65, -2.9, 0], [-2.45, -0.9, 0]])
        wl = ValueTracker(0.0)
        water = Rectangle(width=1.5, height=0.02, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).set_z_index(4)

        def uw(m):
            h = max(0.02, 1.7 * wl.get_value())
            m.become(Rectangle(width=1.5, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to([-3.4, -2.88 + h / 2, 0]).set_z_index(4))
        water.add_updater(uw)
        bub = VGroup(*[Dot(radius=0.06, color=BLUE) for _ in range(6)])

        def ub(m):
            t = self.elapsed()
            for i, b in enumerate(m):
                ph = (t * 0.3 + i * 0.17) % 1
                b.move_to([-3.4 + 0.5 * np.sin(2 * t + i * 2), -2.8 + 1.5 * wl.get_value() * ph, 0])
                b.set_fill(opacity=0.8 * min(1, wl.get_value() * 3) * np.sin(np.pi * ph))
        bub.add_updater(ub)
        div = DashedLine([0, -3.6, 0], [0, 3.6, 0], color=GREY, stroke_width=3)
        self.add(div, stalk, glass, water, bub)
        self.at("stands in water")
        self.play(wl.animate.set_value(1.0), run_time=1.3, rate_func=linear)
        self.at("for a few hours")
        clock = VGroup(Circle(radius=0.5, stroke_color=TEXT, stroke_width=5), Line(ORIGIN, UP * 0.38, color=YELLOW, stroke_width=6)).move_to([-1.3, 2.9, 0])
        self.play(FadeIn(clock), run_time=0.4)
        self.play(Rotate(clock[1], angle=-6 * PI, about_point=clock[0].get_center(), rate_func=linear), run_time=1.9)
        self.at("turn crisp")
        self.play(d.animate.set_value(0.0), run_time=1.8)
        self.play(FadeOut(clock), run_time=0.4)
        self.at("you drink")
        amp, gtr = ValueTracker(0.0), ValueTracker(0.0)
        kid = kid_parts(self, (3.4, -0.9), 1.1, amp, gtr)
        self.play(FadeIn(kid), run_time=0.6)
        self.play(gtr.animate.set_value(1.0), run_time=1.0)
        self.at("bendy")
        self.play(gtr.animate.set_value(0.0), amp.animate.set_value(0.7), run_time=1.0)
        self.at("what is different")
        q = T("?", size=110, color=YELLOW, weight=BOLD).move_to([0, 0.3, 0]).set_z_index(10)
        bg = Circle(radius=0.8, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(q).set_z_index(9)
        self.play(FadeIn(bg), FadeIn(q, scale=0.5), run_time=0.6)
        self.play(q.animate.scale(1.15), rate_func=there_and_back, run_time=1.2)
        self.finish()


# --------------------------------------------------------------------------------------------
class S02Kit1(SpokenScene):
    def construct(self):
        A = Cell(self, 0, -0.2, 2.5)
        tmp = Circle(radius=2.5, stroke_color=BLUE, stroke_width=4).move_to([0, -0.2, 0])
        self.play(Create(tmp), run_time=1.6)
        self.add(A.mem)
        self.remove(tmp)
        self.at("your own cells")
        l0 = lab("your cell", TEXT, (0, 3.2))
        self.play(FadeIn(l0), run_time=0.5)
        self.at("nucleus")
        self.play(FadeOut(l0), FadeIn(A.nuc[0], scale=0.4), run_time=0.8)
        l1 = lab("nucleus", PURPLE, (-4.6, 1.9), A.nuc[0].get_center() + np.array([-0.3, 0.1, 0]))
        self.play(FadeIn(l1), run_time=0.5)
        self.at("a thin")
        self.play(FadeOut(l1), A.mem.animate.set_stroke(width=10), run_time=0.7)
        l2 = lab("cell membrane", BLUE, (4.6, 1.9), A.edge(35))
        self.play(FadeIn(l2), run_time=0.5)
        # bouncing dots
        rng = np.random.RandomState(3)
        dots = VGroup(*[Dot(radius=0.09, color=TEXT) for _ in range(10)])
        ang = rng.uniform(0, 2 * np.pi, 10)
        pos = np.array([[np.cos(a) * 3.6, np.sin(a) * 2.8 - 0.2] for a in ang])
        vel = np.array([[-np.cos(a) * 0.8 + rng.uniform(-.6, .6), -np.sin(a) * 0.8 + rng.uniform(-.6, .6)] for a in ang])
        passers = {1, 5, 8}
        st = {"pos": pos, "vel": vel, "t": self.elapsed()}

        def ud(m):
            now = self.elapsed()
            dt = min(0.1, now - st["t"])
            st["t"] = now
            for i, d in enumerate(m):
                p, v = st["pos"][i], st["vel"][i]
                old = p.copy()
                p += v * dt
                if abs(p[0]) > 6.0:
                    v[0] *= -1
                    p[0] = np.sign(p[0]) * 6.0
                if abs(p[1]) > 3.4:
                    v[1] *= -1
                    p[1] = np.sign(p[1]) * 3.4
                if i not in passers:
                    q = p - np.array([0, -0.2])
                    qo = old - np.array([0, -0.2])
                    if (np.linalg.norm(q) < 2.5) != (np.linalg.norm(qo) < 2.5):
                        n = q / np.linalg.norm(q)
                        v -= 2 * np.dot(v, n) * n
                        p[:] = old
                d.move_to([p[0], p[1], 0])
        dots.add_updater(ud)
        ud(dots)
        self.play(FadeIn(dots), run_time=0.6)
        self.at("and out")
        self.play(FadeOut(l2), A.mem.animate.set_stroke(width=4), run_time=0.6)
        self.finish()


class S03Kit2(SpokenScene):
    def construct(self):
        A = Cell(self, 0, -0.2, 2.5)
        self.add(A.mem, A.nuc[0])
        L = {}
        self.at("jelly")
        self.play(FadeIn(A.cyto), FadeIn(A.dots), run_time=1.0)
        self.at("cytoplasm")
        L["c"] = lab("cytoplasm", TEXT, (-4.9, -0.1), (-1.9, -0.7))
        self.play(FadeIn(L["c"]), run_time=0.5)
        self.at("a folded")
        self.play(FadeOut(L["c"]), FadeIn(A.er[0], scale=0.5), run_time=0.9)
        self.at("endoplasmic")
        L["e"] = lab("endoplasmic\nreticulum", TEAL, (-5.1, -2.0), A.er[0].get_center() + np.array([-0.45, -0.05, 0]))
        self.play(FadeIn(L["e"]), run_time=0.5)
        self.at("mitochondria")
        self.play(FadeOut(L["e"]), *[FadeIn(m, scale=0.5) for m in A.mito], lag_ratio=0.3, run_time=1.4)
        L["m"] = lab("mitochondria", ORANGE, (4.9, 1.6), A.mito[0].get_center() + np.array([0.3, 0.1, 0]))
        self.play(FadeIn(L["m"]), run_time=0.5)
        self.at("small sacks")
        self.play(FadeOut(L["m"]), *[FadeIn(v, scale=0.4) for v in A.vac], run_time=1.0)
        L["v"] = lab("vacuoles", PALE, (4.9, -1.6), A.vac[0].get_center() + np.array([0.15, -0.05, 0]))
        self.play(FadeIn(L["v"]), run_time=0.5)
        self.at("store water")
        self.play(FadeOut(L["v"]), run_time=0.4)
        br = Brace(Line([-2.7, -2.85, 0], [2.7, -2.85, 0]), direction=DOWN, color=GOLD)
        tx = T("the shared kit", size=30, color=GOLD).next_to(br, DOWN, buff=0.1)
        self.play(FadeIn(br), FadeIn(tx), run_time=0.8)
        self.finish()


def kit_cell(sc, c, R, **kw):
    X = Cell(sc, c[0], c[1], R, **kw)
    X.add_kit()
    return X


class S04Plan(SpokenScene):
    def construct(self):
        A = Cell(self, 0, -0.2, 2.5)
        A.add_kit()
        B = Cell(self, 0, -0.2, 2.5)
        B.add_kit()
        for m in B.orgs():
            pass
        self.wait(0.3)
        self.at("a celery cell")
        self.play(A.cx.animate.set_value(ACORNER[0]), A.cy.animate.set_value(ACORNER[1]), A.R.animate.set_value(ACORNER[2]),
                  B.cx.animate.set_value(BX), B.cy.animate.set_value(BY), B.R.animate.set_value(BR),
                  run_time=2.6)
        self.at("your cell")
        la = lab("your cell", TEXT, (-3.7, 2.85))
        self.play(FadeIn(la), run_time=0.5)
        self.at("adding")
        ck = Checklist()
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in ck.rows], lag_ratio=0.9), run_time=1.8)
        self.finish()


def stage(sc, st):
    """Rebuild the carried world for scenes 5 to 9. st = 5..9."""
    A = Cell(sc, *ACORNER)
    A.add_kit()
    B = Cell(sc, BX, BY, BR, sq=0 if st < 9 else 1, tk=1 if st >= 8 else 0, W=0.45 if st < 9 else 1, pr=0 if st < 9 else 0)
    B.add_kit()
    la = lab("your cell", TEXT, (-3.7, 2.85))
    ck = Checklist(ticked={5: 0, 6: 1, 7: 2, 8: 3, 9: 3}[st])
    sc.add(la, ck)
    wl = None
    if st >= 6:
        wl = wall()
        sc.add(wl)
    if st >= 7:
        sc.add(*B.chl)
    if st >= 8:
        sc.add(B.tank)
        sc.remove(*B.vac)
    return A, B, ck, wl


class S05Box(SpokenScene):
    def construct(self):
        A, B, ck, _ = stage(self, 5)
        box = wall().scale(1.35).set_stroke(opacity=0)
        self.add(box)
        self.at("a stiff cell wall")
        self.play(box.animate.scale(1 / 1.35).set_stroke(opacity=1), run_time=1.5)
        self.at("outside")
        l1 = lab("cell wall = the box", TANC, (BX, 2.85))
        self.play(FadeIn(l1), run_time=0.5)
        self.at("the membrane")
        self.play(B.mem.animate.set_stroke(width=10), run_time=0.6)
        l2 = lab("membrane", BLUE, (BX, -3.1), (BX, BY - BR))
        self.play(FadeIn(l2), run_time=0.5)
        self.at("think of")
        self.play(B.mem.animate.set_stroke(width=4), FadeOut(l2), run_time=0.5)
        ic = box_icon((5.5, 2.85))
        self.play(FadeIn(ic, scale=0.6), run_time=0.7)
        self.at("cardboard")
        self.play(ck.tick(0), run_time=0.7)
        self.finish()


class S06Green(SpokenScene):
    def construct(self):
        A, B, ck, wl = stage(self, 6)
        rays = VGroup(*[Line([-1.2 + 1.0 * i, 3.7, 0], [BX - 1.2 + 0.8 * i, BY + 2.3, 0], color=YELLOW, stroke_width=6) for i in range(5)])
        rays.gain = ValueTracker(0.0)

        def ur(m):
            t = self.elapsed()
            for i, r in enumerate(m):
                r.set_stroke(opacity=m.gain.get_value() * (0.55 + 0.35 * np.sin(2.2 * t + i)))
        rays.add_updater(ur)
        self.add(rays)
        self.play(rays.gain.animate.set_value(1.0), run_time=0.9)
        self.at("chloroplasts")
        self.play(*[FadeIn(m, scale=0.4) for m in B.chl], lag_ratio=0.25, run_time=1.6)
        self.at("food makers")
        lg = lab("chloroplasts = food makers", GREEN, (BX, -3.15), B.chl[5].get_center() + np.array([0, -0.15, 0]))
        self.play(FadeIn(lg), run_time=0.5)
        self.at("make sugar")
        sug = VGroup(*[Dot(radius=0.07, color=GOLD) for _ in range(6)])

        def us(m):
            t = self.elapsed()
            for i, d in enumerate(m):
                ch = B.chl[i]
                ph = (t * 0.55 + i * 0.19) % 1
                tow = B.center() - ch.get_center()
                tow = tow / np.linalg.norm(tow)
                d.move_to(ch.get_center() + tow * (0.2 + 0.6 * ph))
                d.set_fill(opacity=np.sin(np.pi * ph))
        sug.add_updater(us)
        us(sug)
        self.add(sug)
        self.wait(1.4)
        self.play(ck.tick(1), FadeOut(lg), rays.gain.animate.set_value(0.0), run_time=0.7)
        self.finish()


class S07Tank(SpokenScene):
    def construct(self):
        A, B, ck, wl = stage(self, 7)
        self.add(B.tank)
        self.at("one large")
        self.play(B.tk.animate.set_value(1.0), run_time=2.6)
        self.remove(*B.vac)
        self.at("water tank")
        lt = lab("large central vacuole\n= water tank", PALE, (BX, -3.15))
        self.play(FadeIn(lt), run_time=0.5)
        self.at("most of the space")
        self.play(ck.tick(2), B.tank.animate.set_stroke(width=6), run_time=0.8)
        self.play(B.tank.animate.set_stroke(width=3), run_time=0.8)
        self.finish()


class S08Fill(SpokenScene):
    def construct(self):
        A, B, ck, wl = stage(self, 8)
        fl = Flow(self, b_specs(True))
        self.add(fl)
        self.at("now let water")
        self.play(fl.gain.animate.set_value(1.0), run_time=0.8)
        self.at("the tank swells")
        self.play(B.W.animate.set_value(1.0), run_time=2.0)
        self.at("it pushes")
        self.play(B.sq.animate.set_value(1.0), run_time=4.4, rate_func=smooth)
        self.at("presses into")
        ring = Circle(radius=0.55, stroke_color=YELLOW, stroke_width=6).move_to([BX + 1.95, BY + 1.95, 0]).set_z_index(12)
        self.play(Create(ring), run_time=0.6)
        self.play(ring.animate.scale(1.25), rate_func=there_and_back, run_time=1.0)
        self.wait(0.6)
        self.play(fl.gain.animate.set_value(0.0), FadeOut(ring), run_time=0.8)
        self.finish()


def model_box(sc, g_tr, pos=(-3.7, -0.3)):
    c = np.array([pos[0], pos[1], 0.0])
    bx = Rectangle(width=2.7, height=2.4, stroke_color=TANC, stroke_width=7).move_to(c)
    fl1 = Line(c + [-1.35, 1.2, 0], c + [-1.9, 1.75, 0], color=TANC, stroke_width=7)
    fl2 = Line(c + [1.35, 1.2, 0], c + [1.9, 1.75, 0], color=TANC, stroke_width=7)
    bal = VMobject(stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5)

    def ub(m):
        g = g_tr.get_value()
        a = 0.35 + 0.85 * g
        m.set_points_as_corners(sq_pts(c, a, 2 + 8 * g))
    bal.add_updater(ub)
    ub(bal)
    return VGroup(bx, fl1, fl2, bal), bal


class S09Pushback(SpokenScene):
    def construct(self):
        A, B, ck, wl = stage(self, 9)
        B.dim(0.3)
        out, fill = make_meter(self, B.stiff)
        pa = PushArrows(self, B)
        self.add(pa)
        self.at("the stiff wall pushes")
        l1 = lab("wall pushes back", TANC, (BX, 3.4))
        self.play(FadeIn(l1), B.pr.animate.set_value(0.45), run_time=1.2)
        self.at("it holds")
        self.play(FadeOut(l1), B.pr.animate.set_value(0.7), FadeIn(out), run_time=1.4)
        self.add(fill)
        self.at("the cell turns")
        lf = lab("firm", GOLD, (5.7, 2.15))
        self.play(B.pr.animate.set_value(1.0), run_time=1.5)
        self.play(FadeIn(lf), run_time=0.4)
        self.at("picture")
        gt = ValueTracker(0.0)
        mg, bal = model_box(self, gt)
        lm = lab("model", BLUE, (-3.7, -2.25))
        self.play(FadeOut(ck), FadeIn(mg), FadeIn(lm), run_time=0.8)
        self.at("filled tight")
        self.play(gt.animate.set_value(1.0), run_time=2.4)
        self.finish()


class S10Stalk(SpokenScene):
    def construct(self):
        B = Cell(self, BX, BY, BR, sq=1, tk=1, W=1, pr=1)
        B.add_kit()
        self.remove(*B.vac)
        wl10 = wall()
        self.add(B.tank, wl10)
        B.dim(0.3)
        out, fill = make_meter(self, B.stiff)
        self.add(out, fill)
        pa = PushArrows(self, B)
        self.add(pa)
        self.wait(0.8)
        self.at("holds many")
        # build the wall of cells
        cols, rows, ts = 9, 6, 0.95
        tiles = VGroup()
        for i in range(cols):
            for j in range(rows):
                c = np.array([(i - (cols - 1) / 2) * ts, (j - (rows - 1) / 2) * ts, 0])
                tiles.add(VGroup(
                    Square(ts, stroke_color=TANC, stroke_width=4).move_to(c),
                    RoundedRectangle(corner_radius=0.08, width=ts * 0.78, height=ts * 0.78, stroke_width=0, fill_color=GREY, fill_opacity=0.25).move_to(c),
                    RoundedRectangle(corner_radius=0.06, width=ts * 0.56, height=ts * 0.56, stroke_color=PALE, stroke_width=2, fill_color=PALE, fill_opacity=0.55).move_to(c)))
        P0 = tiles[(4 * rows) + 3].get_center().copy()
        s0 = 2 * BOXH / ts
        tiles.scale(s0, about_point=P0).shift(np.array([BX, BY, 0]) - P0)
        self.add(tiles)
        tiles.set_z_index(30)
        grp = [pa, out, fill]
        self.play(FadeOut(VGroup(*grp)), run_time=0.3)
        for x in (pa, out, fill):
            x.clear_updaters()
        self.remove(B.drv, B.mem, B.cyto, B.dots, B.tank, wl10, *B.kit(), *B.chl)
        self.play(tiles.animate.shift(P0 - np.array([BX, BY, 0])).scale(1 / s0, about_point=P0).shift(np.array([-0.0, 0.0, 0.0])), run_time=2.2)
        self.at("together")
        d = ValueTracker(0.0)
        gr = ValueTracker(0.0)
        st = stalk_up(self, (-3.4, -3.2), 5.2, d, gr, width=44)
        self.add(st)
        self.play(tiles.animate.scale(0.25).move_to([-3.4, 0.0, 0]).set_opacity(0.0), gr.animate.set_value(1.0), run_time=1.6)
        ls = lab("many firm cells\n= firm stalk", CELERY, (2.2, 0.2))
        self.at("they hold")
        self.play(FadeIn(ls), run_time=0.6)
        self.finish()


def ctr_scene_base(sc, d, with_drops=True):
    p = plank()
    s = stalk_ctr(sc, d)
    sc.add(p, s)
    dr = None
    if with_drops:
        dr = drops(sc)
        sc.add(dr)
    return p, s, dr


class S11Predict(SpokenScene):
    def construct(self):
        d = ValueTracker(0.0)
        p, s, _ = ctr_scene_base(self, d, with_drops=False)
        self.play(FadeIn(p), FadeIn(s), run_time=0.6)
        self.at("counter")
        sn = sun(self, 6.2, 0.8, self.elapsed(), 6.0)
        self.add(sn)
        self.wait(0.8)
        self.at("loses water")
        dr = drops(self)
        dr.gain.set_value(0.0)
        self.add(dr)
        self.play(dr.gain.animate.set_value(1.0), run_time=0.8)
        self.at("what happens")
        q1 = T("tank?", size=64, color=PALE).move_to([3.0, -0.6, 0])
        self.play(FadeIn(q1, scale=0.7), run_time=0.7)
        self.at("then")
        q2 = T("stalk?", size=64, color=CELERY).move_to([3.0, -2.0, 0])
        self.play(FadeIn(q2, scale=0.7), run_time=0.7)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        d = ValueTracker(0.0)
        p, s, dr = ctr_scene_base(self, d)
        sn = sun(self, 0.8, 0.8, 0, 1.0)
        self.add(sn)
        q = T("What happens to\nthe tank, and then\nto the stalk?", size=44, line_spacing=0.9).move_to([2.6, 0.9, 0])
        self.add(q)
        ring = Circle(radius=0.5, stroke_color=GREY, stroke_width=4).move_to([5.9, -3.0, 0])
        arc = Arc(radius=0.5, start_angle=PI / 2, angle=2 * PI, stroke_color=GOLD, stroke_width=8).move_to([5.9, -3.0, 0])
        t0 = self.elapsed()

        def ua(m):
            f = min(1.0, (self.elapsed() - t0) / self.narration_s)
            m.become(Arc(radius=0.5, start_angle=PI / 2, angle=max(0.01, 2 * PI * (1 - f)), stroke_color=GOLD, stroke_width=8).move_to([5.9, -3.0, 0]))
        arc.add_updater(ua)
        self.add(ring, arc)
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        d = ValueTracker(0.0)
        p, s, dr = ctr_scene_base(self, d)
        B = Cell(self, BX, BY, BR, sq=1, tk=1, W=1, pr=1)
        B.add_kit()
        self.remove(*B.vac)
        self.add(B.tank, wall(), *B.chl)
        B.dim(0.3)
        out, fill = make_meter(self, B.stiff)
        lf = lab("firm", GOLD, (5.7, 2.15))
        pa = PushArrows(self, B)
        self.add(out, fill, lf, pa)
        fo = Flow(self, b_specs(False))
        self.add(fo)
        self.at("tank shrinks")
        self.play(fo.gain.animate.set_value(1.0), B.W.animate.set_value(0.2), run_time=2.4)
        self.at("so it pushes less")
        self.play(B.pr.animate.set_value(0.3), run_time=1.6)
        self.at("the box is no longer")
        self.play(B.sq.animate.set_value(0.4), B.pr.animate.set_value(0.1), fo.gain.animate.set_value(0.0), run_time=2.4)
        self.at("each cell")
        ls = lab("soft", TEXT, (5.7, 2.15))
        self.play(ReplacementTransform(lf, ls), run_time=0.6)
        self.at("stock goes limp")
        self.play(d.animate.set_value(1.0), run_time=1.6)
        self.finish()


class S14Back(SpokenScene):
    def construct(self):
        d = ValueTracker(1.0)
        p, s, _ = ctr_scene_base(self, d, with_drops=False)
        B = Cell(self, BX, BY, BR, sq=0.4, tk=1, W=0.2, pr=0.1)
        B.add_kit()
        self.remove(*B.vac)
        self.add(B.tank, wall(), *B.chl)
        B.dim(0.3)
        out, fill = make_meter(self, B.stiff)
        ls = lab("soft", TEXT, (5.7, 2.15))
        pa = PushArrows(self, B)
        self.add(out, fill, ls, pa)
        wl = ValueTracker(0.0)
        gx, gb = -2.85, -3.7
        glass = VMobject(stroke_color=TEXT, stroke_width=6).set_z_index(5)
        glass.set_points_as_corners([[gx - 0.95, -1.9, 0], [gx - 0.8, gb, 0], [gx + 0.8, gb, 0], [gx + 0.95, -1.9, 0]])
        water = Rectangle(width=1.5, height=0.02, stroke_width=0, fill_color=BLUE, fill_opacity=0.55).set_z_index(4)

        def uw(m):
            h = max(0.02, 1.5 * wl.get_value())
            m.become(Rectangle(width=1.55, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.55).move_to([gx, gb + 0.05 + h / 2, 0]).set_z_index(4))
        water.add_updater(uw)
        self.add(water)
        self.at("put")
        self.play(FadeIn(glass), run_time=0.5)
        self.play(wl.animate.set_value(1.0), run_time=1.5)
        fi = Flow(self, b_specs(True))
        self.add(fi)
        self.at("water moves")
        self.play(fi.gain.animate.set_value(1.0), run_time=0.6)
        self.play(B.W.animate.set_value(1.0), B.sq.animate.set_value(1.0), B.pr.animate.set_value(1.0), run_time=3.0)
        lf = lab("firm", GOLD, (5.7, 2.15))
        self.play(ReplacementTransform(ls, lf), fi.gain.animate.set_value(0.0), run_time=0.6)
        self.at("the stock can turn")
        self.play(d.animate.set_value(0.0), run_time=1.9)
        self.finish()


def center_world(sc):
    B = Cell(sc, BX, BY, BR, sq=1, tk=1, W=1, pr=1)
    B.add_kit()
    sc.remove(*B.vac)
    w = wall()
    sc.add(*B.chl, B.tank, w)
    B.dim(0.3)
    B.w = w
    return B


class S15You(SpokenScene):
    def construct(self):
        B = center_world(self)
        A = Cell(self, *ACORNER)
        A.add_kit()
        outB, fillB = make_meter(self, B.stiff)
        lfB = lab("firm", GOLD, (5.7, 2.15))
        self.add(outB, fillB, lfB)
        self.play(A.cx.animate.set_value(ACENTRE[0]), A.cy.animate.set_value(ACENTRE[1]), A.R.animate.set_value(ACENTRE[2]), run_time=2.4)
        self.at("your cells")
        lk = lab("shared kit", GOLD, (ACENTRE[0], 3.4))
        self.play(FadeIn(lk), *[m.animate(rate_func=there_and_back).set_stroke(width=8) for m in A.kit()], run_time=1.2)
        self.at("but no box")
        g = DashedVMobject(Rectangle(width=2 * BOXH, height=2 * BOXH, stroke_color=TANC, stroke_width=8)).move_to([ACENTRE[0], ACENTRE[1], 0])
        c0 = np.array([ACENTRE[0], ACENTRE[1], 0])
        cross = VGroup(Line(c0 + [-1.2, 1.2, 0], c0 + [1.2, -1.2, 0]), Line(c0 + [-1.2, -1.2, 0], c0 + [1.2, 1.2, 0])).set_stroke(RED, 10).set_z_index(12)
        ln = lab("no box", RED, (ACENTRE[0], -3.1))
        self.play(FadeOut(lk), FadeIn(g), run_time=0.6)
        self.play(Create(cross), FadeIn(ln), run_time=0.7)
        self.at("with no stiff wall")
        self.play(FadeOut(g), FadeOut(cross), run_time=0.5)
        ax = ACENTRE[0]
        sp = [((ax - 1.0, 2.9), (ax - 1.0, 2.2), True), ((ax + 1.0, 2.2), (ax + 1.0, 2.9), False),
              ((ax - 1.0, -2.9), (ax - 1.0, -2.2), False), ((ax + 1.0, -2.2), (ax + 1.0, -2.9), True)]
        sp = [(f, n, i) for f, n, i in sp]
        fa = Flow(self, [((ax + (-1.0 if k % 2 == 0 else 1.0), (2.9 if k < 2 else -2.9)), (ax + (-1.0 if k % 2 == 0 else 1.0), (2.2 if k < 2 else -2.2)), k in (0, 3)) for k in range(4)])
        self.add(fa)
        self.play(fa.gain.animate.set_value(1.0), run_time=0.8)
        self.at("water cannot")
        outA, fillA = make_meter(self, lambda: 0.06, x=-5.7)
        lsA = lab("soft", TEXT, (-5.7, 2.15))
        self.play(FadeIn(outA), FadeIn(lsA), FadeOut(ln), run_time=0.7)
        self.add(fillA)
        self.finish()


def kid_static(sc, amp=0.0):
    hip = np.array([0.0, -1.0, 0.0])
    parts = VGroup()
    body = [((0, -1.0), (0, 1.4), 80), ((0.4, -1.0), (0.55, -3.5), 44), ((-0.4, -1.0), (-0.55, -3.5), 44),
            ((0.75, 1.2), (1.25, -0.9), 34), ((-0.75, 1.2), (-1.25, -0.9), 34)]
    for a, b, w in body:
        parts.add(Line([a[0], a[1], 0], [b[0], b[1], 0], stroke_width=w, color=GREY).set_stroke(opacity=0.35).set_cap_style(CapStyleType.ROUND))
    head = Circle(radius=0.55, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.3).move_to([0, 2.25, 0])
    return VGroup(parts, head)


def skeleton():
    sk = VGroup()
    W_ = 6
    def ln(a, b):
        return Line([a[0], a[1], 0], [b[0], b[1], 0], color=TEXT, stroke_width=W_)
    sk.add(ln((0, -1.0), (0, 1.5)), ln((-0.75, 1.2), (0.75, 1.2)), ln((-0.45, -1.0), (0.45, -1.0)))
    for y in (0.9, 0.5, 0.1):
        sk.add(ln((-0.5, y), (0.5, y)))
    sk.add(ln((0.75, 1.2), (1.0, 0.2)), ln((1.0, 0.2), (1.25, -0.9)), ln((-0.75, 1.2), (-1.0, 0.2)), ln((-1.0, 0.2), (-1.25, -0.9)))
    sk.add(ln((0.4, -1.0), (0.5, -2.2)), ln((0.5, -2.2), (0.55, -3.5)), ln((-0.4, -1.0), (-0.5, -2.2)), ln((-0.5, -2.2), (-0.55, -3.5)))
    sk.add(Circle(radius=0.45, stroke_color=TEXT, stroke_width=W_).move_to([0, 2.25, 0]))
    for p in [(0.5, -2.2), (-0.5, -2.2), (1.0, 0.2), (-1.0, 0.2)]:
        sk.add(Dot([p[0], p[1], 0], radius=0.1, color=TEXT))
    return sk


class S16Skeleton(SpokenScene):
    def construct(self):
        B = center_world(self)
        A = Cell(self, *ACENTRE)
        A.add_kit()
        outB, fillB = make_meter(self, B.stiff)
        kid = kid_static(self).set_z_index(0)
        self.wait(0.2)
        grpB = [B.mem, B.cyto, B.tank, *B.orgs(), *B.vac]
        extra = [m for m in self.mobjects if m not in [A.drv, A.mem, A.cyto, *A.kit(), *grpB, B.drv]]
        self.play(*[FadeOut(m) for m in grpB + extra if m in self.mobjects], run_time=0.7)
        self.remove(B.drv)
        self.play(A.cx.animate.set_value(0.9), A.cy.animate.set_value(0.2), A.R.animate.set_value(0.3), FadeIn(kid), run_time=1.8)
        self.play(FadeOut(VGroup(A.mem, A.cyto, *A.kit())), run_time=0.4)
        self.remove(A.drv)
        self.at("a skeleton")
        sk = skeleton()
        glow = sk.copy().set_stroke(width=16, opacity=0.25)
        self.play(Create(glow), Create(sk), run_time=1.8)
        lb = lab("skeleton\nholds you up", TEXT, (4.6, 0.6))
        self.play(FadeIn(lb), run_time=0.5)
        self.at("your body also")
        dr = VGroup(*[Dot(radius=0.1, color=BLUE) for _ in range(9)])
        rng = np.random.RandomState(5)
        st = {"p": rng.uniform([-0.5, -0.8], [0.5, 1.2], (9, 2)), "v": rng.uniform(-0.8, 0.8, (9, 2)), "t": self.elapsed()}

        def ud(m):
            now = self.elapsed()
            dt = min(0.1, now - st["t"])
            st["t"] = now
            for i, d in enumerate(m):
                st["p"][i] += st["v"][i] * dt
                for k, (lo, hi) in enumerate([(-0.5, 0.5), (-0.8, 1.2)]):
                    if st["p"][i][k] < lo or st["p"][i][k] > hi:
                        st["v"][i][k] *= -1
                        st["p"][i][k] = min(hi, max(lo, st["p"][i][k]))
                d.move_to([st["p"][i][0], st["p"][i][1], 0])
        dr.add_updater(ud)
        ud(dr)
        dr.set_z_index(20)
        self.play(FadeIn(dr), run_time=0.8)
        self.finish()


class S17Close(SpokenScene):
    def construct(self):
        B = center_world(self)
        A = Cell(self, *ACENTRE)
        A.add_kit()
        A.dim(1.0)
        B.dim(1.0)
        outB, fillB = make_meter(self, B.stiff)
        lfB = lab("firm", GOLD, (5.7, 2.15))
        pa = PushArrows(self, B)
        pa.step()
        for m in pa:
            m.set_fill(opacity=0).set_stroke(opacity=0)
        pa.clear_updaters()
        self.add(outB, fillB, lfB)
        self.at("same shared kit")
        self.play(*[m.animate(rate_func=there_and_back).set_stroke(width=9) for m in A.kit() + B.nuc + B.er + B.mito], run_time=1.3)
        self.at("a box")
        w = [B.w]
        l1 = lab("box", TANC, (BX, 2.85))
        self.play(FadeIn(l1), *[x.animate(rate_func=there_and_back).set_stroke(width=16) for x in w], run_time=0.9)
        self.at("a food maker")
        l2 = lab("food maker", GREEN, (BX, 2.85))
        self.play(FadeOut(l1), FadeIn(l2), *[x.animate(rate_func=there_and_back).set_stroke(width=9) for x in B.chl], run_time=0.9)
        self.at("a water tank")
        l3 = lab("water tank", PALE, (BX, 2.85))
        self.play(FadeOut(l2), FadeIn(l3), B.tank.animate(rate_func=there_and_back).set_stroke(width=9), run_time=0.9)
        self.at("when the tank is full")
        mg = VGroup(Rectangle(width=1.5, height=0.9, stroke_color=TANC, stroke_width=5),
                    RoundedRectangle(corner_radius=0.15, width=1.2, height=0.62, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5)).move_to([BX, -3.3, 0])
        self.add(pa)
        pa.add_updater(lambda m, dt: pa.step())
        self.play(FadeOut(l3), FadeIn(mg), run_time=0.8)
        self.at("it pushes the cell")
        self.wait(1.4)
        self.at("a soft plant")
        self.play(fillB.animate.set_fill(opacity=1.0), lfB.animate.scale(1.25), run_time=0.8)
        self.finish()


class S18End(EndCard):
    LINE = "Full tank, stiff box: water pressure holds soft plants up."
