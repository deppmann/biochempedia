"""One Cell, Every Job  (Biochemistrypedia Life Science film, levels-of-organization, chapter 1)

COLOUR MAP (one colour per concept, whole film)
  TEAL   = the Paramecium (its cilia a lighter teal)      AMBER = food / bacteria
  CYAN   = oxygen        GREY = carbon dioxide            PALE BLUE = water / body fluid
  BROWN  = wastes        job colours (checklist icons and group tints):
  move YELLOW, food AMBER, gases CYAN, wastes+water BROWN, respond RED, reproduce GREEN
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F5A623"
CYAN = "#5CE1FF"
WATER = "#9CC9FF"
BROWN = "#C98B52"
CILC = "#9FE8EC"
JOB = [YELLOW, AMBER, CYAN, BROWN, RED, GREEN]
JOBNAME = ["move", "food", "gases", "wastes", "respond", "reproduce"]
POND = (-2.4, 0.0)


# ------------------------------------------------------------------ icons and checklist
def icon(i, s=1.0):
    c = JOB[i]
    if i == 0:
        g = VGroup(Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=c, stroke_width=7, tip_length=0.22))
    elif i == 1:
        g = VGroup(Line([0, -0.3, 0], [0, 0.0, 0]), Line([-0.17, 0.3, 0], [-0.17, 0.0, 0]), Line([0, 0.3, 0], [0, 0.0, 0]),
                   Line([0.17, 0.3, 0], [0.17, 0.0, 0]), Line([-0.17, 0.0, 0], [0.17, 0.0, 0])).set_stroke(c, 6)
    elif i == 2:
        g = VGroup(Arrow([-0.3, 0.14, 0], [0.3, 0.14, 0], buff=0, color=c, stroke_width=6, tip_length=0.18),
                   Arrow([0.3, -0.14, 0], [-0.3, -0.14, 0], buff=0, color=c, stroke_width=6, tip_length=0.18))
    elif i == 3:
        g = VGroup(Polygon([-0.2, 0.12, 0], [0.2, 0.12, 0], [0.15, -0.3, 0], [-0.15, -0.3, 0], color=c, stroke_width=5),
                   Line([-0.26, 0.12, 0], [0.26, 0.12, 0]).set_stroke(c, 5), Dot([0, 0.32, 0], radius=0.07, color=c))
    elif i == 4:
        g = Polygon([0.06, 0.34, 0], [-0.17, -0.02, 0], [0.0, -0.02, 0], [-0.06, -0.34, 0], [0.18, 0.06, 0], [0.02, 0.06, 0],
                    color=c, stroke_width=3, fill_color=c, fill_opacity=1)
        g = VGroup(g)
    else:
        g = VGroup(Circle(radius=0.15, color=c, stroke_width=5).move_to([-0.2, 0, 0]), Circle(radius=0.15, color=c, stroke_width=5).move_to([0.2, 0, 0]))
    return g.scale(s)


def check(color=GREEN, s=1.0):
    return VMobject().set_points_as_corners([[-0.12, 0, 0], [-0.03, -0.1, 0], [0.14, 0.13, 0]]).set_stroke(color, 5).scale(s)


class Panel(VGroup):
    def __init__(self, done=()):
        super().__init__()
        self.rows = []
        for i in range(6):
            y = 2.85 - 1.14 * i
            box = RoundedRectangle(corner_radius=0.12, width=3.1, height=0.98, stroke_color=GREY, stroke_width=2,
                                   fill_color="#1A1F2B", fill_opacity=0.9).move_to([5.05, y, 0])
            ic = icon(i, 0.95).move_to([3.95, y, 0]).set_opacity(0.45)
            lab = T(JOBNAME[i], 24, TEXT).move_to([4.95, y, 0])
            lab.align_to([4.4, 0, 0], LEFT)
            tb = Square(0.34, stroke_color=GREY, stroke_width=3).move_to([6.3, y, 0])
            row = VGroup(box, ic, lab, tb)
            row.box, row.ic, row.tb, row.i = box, ic, tb, i
            row.mark = None
            self.rows.append(row)
            self.add(row)
        for i in done:
            self.add_tick(i)

    def add_tick(self, i):
        r = self.rows[i]
        r.mark = check(GREEN).move_to(r.tb)
        self.add(r.mark)
        return r.mark

    def light(self, i, dim=None):
        r = self.rows[i]
        anims = [r.box.animate.set_stroke(JOB[i], 4), r.ic.animate.set_opacity(1).scale(1.25)]
        if dim is not None:
            d = self.rows[dim]
            anims += [d.box.animate.set_stroke(GREY, 2), d.ic.animate.set_opacity(0.45).scale(1 / 1.25)]
        return anims

    def unlight(self, i):
        d = self.rows[i]
        return [d.box.animate.set_stroke(GREY, 2), d.ic.animate.set_opacity(0.45).scale(1 / 1.25)]


# ------------------------------------------------------------------ the Paramecium
def tw(cell, rt, rf=smooth, **kw):
    st = {}

    def f(m, al):
        if not st:
            st.update({k: m.s[k] for k in kw})
        for k, v in kw.items():
            m.s[k] = st[k] + (v - st[k]) * al
    return UpdateFromAlphaFunc(cell, f, run_time=rt, rate_func=rf)


class Para(VGroup):
    def __init__(self, pos=(0, 0), sc=1.0, ang=0.0, a=2.6, b=1.3, ncil=38, pinch=0.0, wander=None):
        super().__init__()
        self.s = dict(x=pos[0], y=pos[1], sc=sc, ang=ang, p=pinch)
        self.a, self.b, self.wander, self.t, self.n = a, b, wander, 0.0, ncil
        self.body = VMobject(stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.35)
        self.cil = VGroup(*[Line(ORIGIN, RIGHT) for _ in range(ncil)]).set_stroke(CILC, 3)
        self.add(self.body, self.cil)
        self.add_updater(lambda m, dt: m._upd(dt))
        self._upd(0)

    def geom(self):
        s = self.s
        return np.array([s["x"], s["y"], 0.0]), self.a * s["sc"], self.b * s["sc"]

    def _upd(self, dt):
        self.t += dt
        s = self.s
        if self.wander:
            cx, cy, rx, ry, w = self.wander
            s["x"] = cx + rx * math.sin(w * self.t)
            s["y"] = cy + ry * math.sin(1.7 * w * self.t + 1.0)
            s["ang"] = 0.25 * math.sin(1.7 * w * self.t + 1.0)
        c, a, b = self.geom()
        p = s["p"]
        ca, sa = math.cos(s["ang"]), math.sin(s["ang"])
        R = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])

        def pt(th):
            x = a * math.cos(th)
            y = b * math.sin(th) * (1 + 0.12 * (-math.cos(th)))
            y *= (1 - p * math.exp(-(x / (0.3 * a)) ** 2))
            return c + R @ np.array([x, y, 0]), x
        pts = [pt(th)[0] for th in np.linspace(0, 2 * math.pi, 72, endpoint=False)]
        self.body.set_points_as_corners(pts + [pts[0]])
        L = 0.3 * max(s["sc"], 0.6)
        for i, ln in enumerate(self.cil):
            th = 2 * math.pi * (i + 0.5) / self.n
            base, x = pt(th)
            d = np.array([math.cos(th) / a, math.sin(th) / b, 0.0])
            d = d / np.linalg.norm(d)
            w = 0.6 * math.sin(2 * math.pi * (1.8 * self.t - 1.4 * x / a))
            dd = np.array([d[0] * math.cos(w) - d[1] * math.sin(w), d[0] * math.sin(w) + d[1] * math.cos(w), 0])
            ln.put_start_and_end_on(base, base + R @ dd * L)


def pond(c=POND, r=3.7, vx=0.0, seed=3):
    rng = random.Random(seed)
    circ = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=WATER, fill_opacity=0.08).move_to([c[0], c[1], 0])
    motes = VGroup()
    for _ in range(12):
        d = Dot(radius=rng.uniform(0.04, 0.08), color=WATER).set_opacity(0.55)
        a, rr = rng.uniform(0, 6.28), rng.uniform(0, r * 0.95)
        d.move_to([c[0] + rr * math.cos(a), c[1] + rr * math.sin(a), 0])
        d.v = (vx + rng.uniform(-0.12, 0.12), rng.uniform(-0.12, 0.12))
        motes.add(d)

    def drift(m, dt):
        for d in m:
            d.shift([d.v[0] * dt, d.v[1] * dt, 0])
            p = d.get_center() - np.array([c[0], c[1], 0])
            if np.hypot(p[0], p[1]) > r * 0.97:
                d.move_to(np.array([c[0], c[1], 0]) - p * 0.95)
    motes.add_updater(drift)
    g = VGroup(circ, motes)
    return g


class Flow(VGroup):
    def __init__(self, n, color, getg, inward=True, ang=(0, 360), spread=0.8, depth=0.45, speed=0.22, r=0.09, seed=1):
        super().__init__()
        rng = random.Random(seed)
        self.recs = []
        for _ in range(n):
            self.add(Dot(radius=r, color=color).set_opacity(0))
            self.recs.append([math.radians(rng.uniform(*ang)), rng.random(), rng.uniform(0.85, 1.15)])
        self.on, self.inward, self.spread, self.depth, self.speed, self.getg = 0.0, inward, spread, depth, speed, getg
        self.add_updater(lambda m, dt: m._u(dt))

    def _u(self, dt):
        c, ax, ay = self.getg()
        outer = 1 + self.spread
        for dot, rec in zip(self.submobjects, self.recs):
            th, u, j = rec
            u = (u + dt * self.speed * j) % 1.0
            rec[1] = u
            f = outer + (self.depth - outer) * u if self.inward else self.depth + (outer - self.depth) * u
            dot.move_to(c + np.array([ax * f * math.cos(th), ay * f * math.sin(th), 0]))
            dot.set_opacity(min(1, 4 * u, 4 * (1 - u)) * self.on)


class RCell(VGroup):
    def __init__(self, c=(1.5, 0), r=1.5, core=0.0, fill="#2A3550"):
        super().__init__()
        self.s = dict(x=c[0], y=c[1], r=r, core=core)
        self.disc = Circle(radius=r, stroke_color=TEXT, stroke_width=5, fill_color=fill, fill_opacity=1)
        self.coreC = Circle(radius=0.9, stroke_width=0, fill_color=WHITE, fill_opacity=0)
        self.doors = VGroup()
        self.N = 28
        for k in range(self.N):
            th = 2 * math.pi * k / self.N
            d = RoundedRectangle(corner_radius=0.05, width=0.4, height=0.15, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).rotate(th)
            d.th = th
            self.doors.add(d)
        self.add(self.disc, self.coreC, self.doors)
        self.add_updater(lambda m, dt: m._upd())
        self._upd()

    def geom(self):
        return np.array([self.s["x"], self.s["y"], 0.0]), self.s["r"], self.s["r"]

    def _upd(self):
        s = self.s
        c = np.array([s["x"], s["y"], 0.0])
        self.disc.set_points(Circle(radius=s["r"]).move_to(c).points)
        self.coreC.set_points(Circle(radius=0.9).move_to(c).points)
        self.coreC.set_fill(WHITE, opacity=0.9 * s["core"])
        for d in self.doors:
            d.move_to(c + s["r"] * np.array([math.cos(d.th), math.sin(d.th), 0]))


# ------------------------------------------------------------------ people and cell clusters
PERSON = [(-0.6, 2.3), (-2.0, 2.2), (-2.7, 1.5), (-2.8, -0.5), (-2.1, -0.5), (-1.9, 0.6), (-1.8, -0.9), (-1.7, -3.7), (-0.1, -3.7), (0, -1.2),
          (0.1, -3.7), (1.7, -3.7), (1.8, -0.9), (1.9, 0.6), (2.1, -0.5), (2.8, -0.5), (2.7, 1.5), (2.0, 2.2), (0.6, 2.3)]


def person(k=1.0, c=(0, 0)):
    cc = np.array([c[0], c[1], 0.0])
    body = Polygon(*[cc + np.array([x * k, y * k, 0]) for x, y in PERSON]).round_corners(0.3 * k)
    head = Circle(radius=0.65 * k).move_to(cc + np.array([0, 3.05 * k, 0]))
    g = VGroup(body, head).set_stroke(GREY, 4).set_fill(GREY, 0)
    return g


def in_person(x, y):
    if x * x + (y - 3.05) ** 2 < 0.62 ** 2:
        return True
    inside = False
    n = len(PERSON)
    for i in range(n):
        x1, y1 = PERSON[i]
        x2, y2 = PERSON[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def zone(x, y):
    if y > 2.35:
        return 4
    if x < -1.9:
        return 3
    if x > 1.9:
        return 5
    if y < -0.9:
        return 2
    return 0 if y > 0.7 else 1


def mesh(k, c, colorfn=None, step=0.27, r=0.055):
    rng = random.Random(5)
    g = VGroup()
    for j, y in enumerate(np.arange(-3.6, 3.75, step * 0.9)):
        for x in np.arange(-2.8, 2.85, step):
            xx = x + (step / 2 if j % 2 else 0)
            if in_person(xx, y):
                col = colorfn(xx, y) if colorfn else "#C7D2E8"
                d = Dot(radius=r * k * 1.5, color=col)
                d.move_to([c[0] + xx * k, c[1] + y * k, 0])
                d.ph = rng.uniform(0, 6.28)
                g.add(d)
    g.t = 0.0

    def sh(m, dt):
        m.t += dt
        for d in m:
            d.set_opacity(0.6 + 0.4 * math.sin(1.6 * m.t + d.ph))
    g.add_updater(sh)
    return g


def lattice(c, R=3.15, sp=1.12):
    pts = []
    rows = int(R / (sp * 0.866)) + 1
    for j in range(-rows, rows + 1):
        y = j * sp * 0.866
        for i in range(-6, 7):
            x = (i + (j % 2) * 0.5) * sp
            if math.hypot(x, y) <= R:
                pts.append(np.array([c[0] + x, c[1] + y, 0.0]))
    return pts


class Cluster(VGroup):
    def __init__(self, c=(1.5, 0)):
        super().__init__()
        self.c = np.array([c[0], c[1], 0.0])
        self.pts = lattice(c)
        self.edges = [(i, j) for i in range(len(self.pts)) for j in range(i + 1, len(self.pts)) if np.linalg.norm(self.pts[i] - self.pts[j]) < 1.18]
        self.nbr = {i: [] for i in range(len(self.pts))}
        for i, j in self.edges:
            self.nbr[i].append(j)
            self.nbr[j].append(i)
        self.chan = VGroup(*[Line(self.pts[i], self.pts[j]) for i, j in self.edges]).set_stroke(WATER, 6, opacity=0.8)
        self.cells = VGroup(*[Circle(radius=0.44, stroke_color=TEXT, stroke_width=3, fill_color="#E8EAF0", fill_opacity=0.85).move_to(p) for p in self.pts])
        self.add(self.chan, self.cells)


class Walkers(VGroup):
    def __init__(self, cl, n=18, seed=4):
        super().__init__()
        rng = random.Random(seed)
        self.cl, self.rng, self.on = cl, rng, 0.0
        self.recs = []
        for k in range(n):
            self.add(Dot(radius=0.1, color=AMBER if k % 2 else CYAN).set_opacity(0))
            i = rng.randrange(len(cl.pts))
            self.recs.append([i, rng.choice(cl.nbr[i]), rng.random()])
        self.add_updater(lambda m, dt: m._u(dt))

    def _u(self, dt):
        cl = self.cl
        for d, r in zip(self.submobjects, self.recs):
            r[2] += dt * 0.5
            if r[2] >= 1:
                r[2] -= 1
                prev = r[0]
                r[0] = r[1]
                opts = [x for x in cl.nbr[r[0]] if x != prev] or cl.nbr[r[0]]
                r[1] = self.rng.choice(opts)
            d.move_to(cl.pts[r[0]] * (1 - r[2]) + cl.pts[r[1]] * r[2])
            d.set_opacity(self.on)


def groups_of(cl):
    phis = [60, 0, -60, -120, 180, 120]
    used, out = set(), []
    for ph in phis:
        tgt = cl.c + 2.0 * np.array([math.cos(math.radians(ph)), math.sin(math.radians(ph)), 0])
        order = sorted((i for i in range(len(cl.pts)) if i not in used), key=lambda i: np.linalg.norm(cl.pts[i] - tgt))[:3]
        used.update(order)
        out.append(order)
    return out


def tag(text, color, size=28):
    return VGroup(Dot(radius=0.11, color=color), T(text, size, TEXT)).arrange(RIGHT, buff=0.18)


def plate(m):
    return VGroup(BackgroundRectangle(m, fill_color=BG, fill_opacity=0.92, buff=0.12), m)


def swim_cell(**kw):
    return Para(**kw)


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "From Cells to Organisms"
    TITLE = "One Cell, Every Job"


class S01Question(SpokenScene):
    def construct(self):
        pd = pond((-3.4, 0.3), 2.5)
        cell = Para(pos=(-3.4, 0.3), sc=0.55, wander=(-3.4, 0.3, 0.6, 0.4, 0.9))
        self.add(pd)
        self.play(FadeIn(cell), run_time=0.5)
        self.at("one cell")
        l1 = T("1 cell", 32, TEXT, weight=BOLD).move_to([-3.4, -2.55, 0])
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at("You are made")
        pk, pc = 0.82, (3.4, 0.1)
        outl = person(pk, pc)
        ms = mesh(pk, pc)
        self.play(Create(outl), run_time=1.0)
        self.at("about 30 trillion")
        self.play(LaggedStart(*[FadeIn(d) for d in ms], lag_ratio=0.004, run_time=2.0))
        l2 = T("about 30 trillion cells", 30, TEXT, weight=BOLD).move_to([3.4, -3.45, 0])
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.5)
        self.at("so why do you need")
        q = T("?", 150, GOLD, weight=BOLD).move_to([0, 0.2, 0])
        self.play(FadeIn(q, scale=0.3), run_time=0.7)
        self.play(q.animate.scale(1.15), run_time=0.6, rate_func=there_and_back)
        self.finish()


class S02Joblist(SpokenScene):
    def construct(self):
        pd = pond(POND, 3.7)
        cell = Para(pos=(-2.4, 0), sc=0.6, wander=(-2.4, 0, 1.3, 0.7, 0.8))
        self.add(pd, cell)
        panel = Panel()
        self.play(FadeIn(panel, shift=LEFT * 0.6), run_time=1.4)
        self.at("move,")
        self.play(*panel.light(0), run_time=0.4)
        self.at("get food")
        self.play(*panel.light(1, dim=0), run_time=0.4)
        self.at("exchange gases")
        self.play(*panel.light(2, dim=1), run_time=0.4)
        self.at("get rid of")
        self.play(*panel.light(3, dim=2), run_time=0.4)
        self.at("respond")
        self.play(*panel.light(4, dim=3), run_time=0.4)
        self.at("reproduce")
        self.play(*panel.light(5, dim=4), run_time=0.4)
        self.wait(0.8)
        self.play(*panel.unlight(5), run_time=0.4)
        self.finish()


class S03Move(SpokenScene):
    def construct(self):
        pd = pond(POND, 3.7, vx=-0.5)
        cell = Para(pos=(-2.4, 0), sc=0.6, wander=None)
        panel = Panel()
        self.add(pd, cell, panel)
        self.play(tw(cell, 3.0, sc=0.9, x=-3.4), run_time=3.0)
        lab = T("cilia", 32, CILC, weight=BOLD).move_to([-2.9, 3.0, 0])
        arr = Arrow(lab.get_bottom() + DOWN * 0.05, [-2.9, 1.75, 0], buff=0, color=CILC, stroke_width=5, tip_length=0.2)
        self.at("cilia")
        self.play(FadeIn(lab, shift=DOWN * 0.1), GrowArrow(arr), run_time=0.6)
        self.at("push it through")
        self.play(tw(cell, 4.5, x=-1.6, rf=linear), run_time=4.5)
        mk = panel.add_tick(0)
        self.play(Create(mk), FadeOut(lab), FadeOut(arr), run_time=0.5)
        self.finish()


def stage(sc=1.0, y=0.0, done=()):
    pd = pond(POND, 3.7)
    cell = Para(pos=(-2.4, y), sc=sc, wander=(-2.4, y, 0.25, 0.12, 0.7))
    panel = Panel(done=done)
    return pd, cell, panel


class S04Food(SpokenScene):
    def construct(self):
        pd, cell, panel = stage(0.95, 0.3, done=(0,))
        self.add(pd, cell, panel)
        cell.wander = None
        cell.s.update(x=-2.4, y=0.3, ang=0.0)
        c = np.array([-2.4, 0.3, 0])
        mouth, gend = c + np.array([0.9, -1.0, 0]), c + np.array([-0.2, -0.25, 0])
        groove = Line(mouth, gend).set_stroke("#0E3238", 11)
        self.add(groove)
        rng = random.Random(7)
        bact = VGroup(*[Dot(radius=0.1, color=AMBER).move_to(c + np.array([rng.uniform(-0.5, 2.4), rng.uniform(-3.0, -1.7), 0])) for _ in range(12)])
        self.at("sweeps")
        self.play(FadeIn(bact), run_time=0.4)
        anims = []
        for d in bact:
            pth = VMobject().set_points_as_corners([d.get_center(), mouth, gend])
            anims.append(MoveAlongPath(d, pth))
        self.play(LaggedStart(*anims, lag_ratio=0.08, run_time=1.6, rate_func=linear))
        self.at("groove")
        gl = T("groove", 30, TEXT, weight=BOLD).move_to(c + np.array([1.6, -2.4, 0]))
        ga = Arrow(gl.get_top(), mouth + DOWN * 0.1, buff=0.05, color=TEXT, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(gl), GrowArrow(ga), run_time=0.5)
        self.at("small sacs")
        vac = Circle(radius=0.34, stroke_color=AMBER, stroke_width=4, fill_color=AMBER, fill_opacity=0.2).move_to(gend)
        inner = VGroup(*[Dot(radius=0.07, color=AMBER).move_to(gend + np.array(o)) for o in [(-.1, .05, 0), (.1, -.08, 0), (.05, .12, 0)]])
        vg = VGroup(vac, inner)
        self.play(FadeOut(bact), GrowFromPoint(vg, gend), run_time=0.6)
        self.play(vg.animate.shift(LEFT * 0.9 + UP * 0.55), run_time=0.6)
        self.at("food vacuoles")
        vl = T("food vacuole", 30, AMBER, weight=BOLD).move_to(c + np.array([-0.5, 2.4, 0]))
        va = Arrow(vl.get_bottom(), vg.get_top() + UP * 0.1, buff=0.08, color=AMBER, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(vl), GrowArrow(va), FadeOut(gl), FadeOut(ga), run_time=0.5)
        self.at("digested")
        self.play(inner.animate.set_opacity(0.1), vac.animate.set_fill(AMBER, 0.05), run_time=1.0)
        mk = panel.add_tick(1)
        self.play(Create(mk), run_time=0.4)
        self.finish()


class S05Gas(SpokenScene):
    def construct(self):
        pd, cell, panel = stage(1.05, 0.0, done=(0, 1))
        cell.wander = None
        cell.s.update(x=-2.4, y=0.0, ang=0.0)
        self.add(pd, cell, panel)
        o2 = Flow(14, CYAN, cell.geom, True, ang=(0, 360), spread=0.5, depth=0.45, seed=2)
        co2 = Flow(14, GREY, cell.geom, False, ang=(0, 360), spread=0.5, depth=0.45, seed=3)
        self.add(o2, co2)
        self.play(cell.body.animate.set_stroke(TEXT, 7), run_time=0.3)
        self.at("Oxygen")
        o2.on = 1
        lo = tag("oxygen", CYAN).move_to([-2.4, 3.15, 0])
        self.play(FadeIn(lo), run_time=0.4)
        self.at("outer membrane")
        ml = T("outer membrane", 30, TEXT, weight=BOLD).move_to([-2.4, 2.35, 0])
        ma = Arrow(ml.get_bottom(), [-2.4, 1.7, 0], buff=0.05, color=TEXT, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(ml), GrowArrow(ma), run_time=0.5)
        self.at("Carbon dioxide")
        co2.on = 1
        lc = tag("carbon dioxide", GREY).move_to([-2.4, -3.0, 0])
        self.play(FadeIn(lc), run_time=0.4)
        self.at("same way")
        mk = panel.add_tick(2)
        self.play(Create(mk), run_time=0.4)
        self.at("surface")
        self.play(ShowPassingFlash(cell.body.copy().set_stroke(YELLOW, 12), time_width=0.6), run_time=1.6)
        self.finish()


class S06Water(SpokenScene):
    def construct(self):
        pd, cell, panel = stage(1.05, 0.1, done=(0, 1, 2))
        cell.wander = None
        cell.s.update(x=-2.4, y=0.1, ang=0.0)
        self.add(pd, cell, panel)
        w = Flow(18, WATER, cell.geom, True, ang=(0, 360), spread=0.5, depth=0.5, seed=5, r=0.1)
        self.add(w)
        self.at("Pond water")
        w.on = 1
        c = np.array([-2.4, 0.1, 0])
        vpos = c + np.array([-0.7, 0.3, 0])
        self.at("contractile vacuole")
        vac = Star(n=8, outer_radius=0.7, inner_radius=0.33, stroke_color=WATER, stroke_width=4, fill_color=WATER, fill_opacity=0.5).move_to(vpos).scale(0.5)
        vl = T("contractile vacuole", 30, WATER, weight=BOLD).move_to([-2.4, 2.85, 0])
        va = Arrow(vl.get_bottom() + DOWN * 0.05, vpos + UP * 0.45, buff=0.05, color=WATER, stroke_width=4, tip_length=0.18)
        self.play(GrowFromCenter(vac), FadeIn(vl), GrowArrow(va), run_time=0.7)
        self.at("fills")
        self.play(vac.animate.scale(2.4), run_time=1.6)
        self.at("squeezes")
        sq = VGroup(*[Dot(radius=0.1, color=WATER).move_to(vpos + np.array([dx, 0, 0])) for dx in (-0.3, -0.1, 0.1, 0.3)])
        self.add(sq)
        self.play(vac.animate.scale(1 / 4.0), *[d.animate.move_to(vpos + np.array([dx * 2.2, 2.0, 0])).set_opacity(0) for d, dx in zip(sq, (-0.3, -0.1, 0.1, 0.3))],
                  run_time=1.0)
        self.at("Bits of food")
        sp = VGroup(*[Dot(radius=0.09, color=BROWN).move_to(c + np.array([-1.0 + dx, -0.3 + dy, 0])) for dx, dy in [(0, 0), (.3, .15), (.15, -.25), (.5, -.1), (-.2, .2)]])
        self.play(FadeIn(sp), FadeOut(vl), FadeOut(va), run_time=0.5)
        self.play(sp.animate.shift(LEFT * 0.7 + DOWN * 0.1), run_time=1.3)
        self.at("leave through")
        op = c + np.array([-2.57, -0.52, 0])
        opn = Dot(radius=0.16, color="#0E3238").move_to(op)
        self.add(opn)
        self.play(*[d.animate.move_to(op + np.array([-1.2 - 0.25 * k, -0.15 * k + 0.1, 0])).set_opacity(0.0) for k, d in enumerate(sp)], run_time=0.9)
        self.at("small opening")
        ol = T("opening", 30, BROWN, weight=BOLD).move_to([-5.3, -2.2, 0])
        oa = Arrow(ol.get_top() + UP * 0.05, op + DOWN * 0.15, buff=0.05, color=BROWN, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(ol), GrowArrow(oa), run_time=0.5)
        mk = panel.add_tick(3)
        self.play(Create(mk), run_time=0.4)
        self.finish()


class S07Respond(SpokenScene):
    def construct(self):
        pd = pond(POND, 3.7)
        cell = Para(pos=(-3.7, 0.2), sc=0.7)
        panel = Panel(done=(0, 1, 2, 3))
        grain = Polygon([-0.4, 0.1, 0], [-0.1, 0.45, 0], [0.35, 0.3, 0], [0.4, -0.15, 0], [0.05, -0.4, 0], [-0.35, -0.25, 0]).set_stroke(GREY, 3)
        grain.set_fill(GREY, 0.6).move_to([0.0, 0.2, 0])
        self.add(pd, grain, cell, panel)
        l1 = DashedLine([-3.7, 0.2, 0], [-2.25, 0.2, 0], dash_length=0.14).set_stroke(TEXT, 4)
        self.play(tw(cell, 0.9, x=-2.25), Create(l1), run_time=0.9)
        self.at("backs up")
        l2 = DashedLine([-2.25, 0.05, 0], [-3.4, 0.05, 0], dash_length=0.14).set_stroke(TEXT, 4)
        self.play(tw(cell, 1.0, x=-3.4), Create(l2), run_time=1.0)
        self.at("turns")
        self.play(tw(cell, 0.5, ang=math.radians(55)), run_time=0.5)
        self.at("swims off")
        l3 = DashedLine([-3.4, 0.2, 0], [-2.08, 2.08, 0], dash_length=0.14).set_stroke(TEXT, 4)
        self.play(tw(cell, 2.0, x=-2.08, y=2.08), Create(l3), run_time=2.0)
        self.at("That is a response")
        rl = T("a response", 38, RED, weight=BOLD).move_to([-2.4, -2.9, 0])
        self.play(FadeIn(rl, shift=UP * 0.1), run_time=0.5)
        self.at("response")
        mk = panel.add_tick(4)
        self.play(Create(mk), run_time=0.4)
        self.finish()


class S08Divide(SpokenScene):
    def construct(self):
        pd = pond(POND, 3.7)
        cell = Para(pos=(-2.4, 0), sc=0.85, wander=(-2.4, 0, 0.35, 0.2, 0.7))
        panel = Panel(done=(0, 1, 2, 3, 4))
        self.add(pd, cell, panel)
        self.at("pinches")
        cell.wander = None
        self.play(tw(cell, 1.7, p=0.97), run_time=1.7)
        x, y = cell.s["x"], cell.s["y"]
        a = Para(pos=(x - 1.1, y), sc=0.85, a=1.3, b=1.25)
        b = Para(pos=(x + 1.1, y), sc=0.85, a=1.3, b=1.25)
        self.add(a, b)
        self.remove(cell)
        mk = panel.add_tick(5)
        self.play(tw(a, 1.6, x=x - 2.4 + 0.2, y=y + 0.5), tw(b, 1.6, x=x + 1.0, y=y - 0.5), Create(mk), run_time=1.6)
        self.at("Every job")
        a.wander = (x - 2.0, y + 0.5, 0.3, 0.2, 0.7)
        b.wander = (x + 1.0, y - 0.5, 0.3, 0.2, 0.8)
        self.play(*[r.box.animate.set_stroke(GREEN, 4) for r in panel.rows], run_time=0.8)
        self.wait(1.0)
        self.play(*[r.box.animate.set_stroke(GREY, 2) for r in panel.rows], run_time=0.6)
        self.finish()


def body_scene(sc, k=0.94):
    pc = (0, 0.1)
    outl = person(k, pc)
    return outl


class S09Predict(SpokenScene):
    def construct(self):
        cell = Para(pos=(0, 0.1 + 0.7 * 0.94), sc=0.55, wander=(0, 0.1 + 0.7 * 0.94, 0.25, 0.15, 0.8))
        self.play(FadeIn(cell), run_time=0.6)
        self.at("make it bigger")
        outl = person(0.94, (0, 0.1))
        self.play(Create(outl), run_time=2.0)
        self.at("as big as you")
        self.play(outl.animate.set_fill(GREY, 0.18), run_time=1.5)
        self.at("Pause and decide" if False else "Pause")
        pp = T("Pause and\npredict", 40, GOLD, weight=BOLD).move_to([-4.6, 0.3, 0])
        self.play(FadeIn(pp, shift=RIGHT * 0.2), run_time=0.7)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        cell = Para(pos=(0, 0.1 + 0.7 * 0.94), sc=0.55, wander=(0, 0.1 + 0.7 * 0.94, 0.25, 0.15, 0.8))
        outl = person(0.94, (0, 0.1)).set_fill(GREY, 0.18)
        pp = T("Pause and\npredict", 40, GOLD, weight=BOLD).move_to([-4.6, 0.3, 0])
        bar = Rectangle(width=12.0, height=0.12, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([0, -3.72, 0])
        self.add(outl, cell, pp, bar)

        def f(m, al):
            m.stretch_to_fit_width(12.0 * (1 - al))
            m.move_to([-6.0 + m.width / 2, -3.72, 0])
        self.play(UpdateFromAlphaFunc(bar, f, run_time=4.6, rate_func=linear))
        self.finish()


class S11Reveal(SpokenScene):
    def construct(self):
        cell = RCell((1.5, 0), 2.0)
        self.play(FadeIn(cell), run_time=0.6)
        g = cell.geom
        fin1 = Flow(10, AMBER, g, True, ang=(120, 240), spread=1.0, depth=0.5, seed=1)
        fin2 = Flow(10, CYAN, g, True, ang=(120, 240), spread=1.0, depth=0.5, seed=2)
        fout1 = Flow(10, GREY, g, False, ang=(-45, 45), spread=0.7, depth=0.5, seed=3)
        fout2 = Flow(8, BROWN, g, False, ang=(-45, 45), spread=0.7, depth=0.5, seed=4)
        self.add(fin1, fin2, fout1, fout2)
        self.at("growing bigger")
        arrs = VGroup(*[Arrow(np.array([1.5, 0, 0]) + 2.15 * d, np.array([1.5, 0, 0]) + 2.95 * d, buff=0, color=TEXT, stroke_width=6, tip_length=0.22)
                        for d in (UP, DOWN, LEFT, RIGHT)])
        self.play(FadeIn(arrs), run_time=0.5)
        self.play(arrs.animate.shift(0), run_time=0.01)
        self.play(*[a.animate.shift(a.get_vector() / np.linalg.norm(a.get_vector()) * 0.25) for a in arrs], run_time=0.8, rate_func=there_and_back)
        self.play(FadeOut(arrs), run_time=0.4)
        self.at("Food")
        fin1.on = 1
        t1 = tag("food", AMBER, 32).move_to([-5.3, 1.6, 0])
        self.play(FadeIn(t1), run_time=0.4)
        self.at("oxygen")
        fin2.on = 1
        t2 = tag("oxygen", CYAN, 32).move_to([-5.3, 0.7, 0])
        self.play(FadeIn(t2), run_time=0.4)
        self.at("surface")
        sl = T("surface", 32, TEXT, weight=BOLD).move_to([1.5, 3.3, 0])
        sa = Arrow(sl.get_bottom() + DOWN * 0.05, [1.5, 2.3, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(sl), GrowArrow(sa), run_time=0.5)
        self.at("outer membrane")
        sl2 = T("outer membrane", 32, TEXT, weight=BOLD).move_to([1.5, 3.3, 0])
        self.play(ReplacementTransform(sl, sl2), run_time=0.5)
        self.at("Carbon dioxide")
        fout1.on = 1
        t3 = tag("carbon dioxide", GREY, 28).move_to([4.7, -2.6, 0])
        self.play(FadeIn(t3), FadeOut(t1), FadeOut(t2), FadeOut(sl2), FadeOut(sa), run_time=0.4)
        self.at("many wastes")
        fout2.on = 1
        t4 = tag("wastes", BROWN, 28).move_to([4.2, -3.3, 0])
        self.play(FadeIn(t4), run_time=0.4)
        self.finish()


class S12Grow(SpokenScene):
    def construct(self):
        cell = RCell((1.5, 0), 2.0)
        self.add(cell)
        g = cell.geom
        reach = {"d": 0.35, "sp": 0.25}
        fl = Flow(14, AMBER, g, True, ang=(120, 240), spread=0.9, depth=0.35, seed=1)
        fl2 = Flow(14, CYAN, g, True, ang=(120, 240), spread=0.9, depth=0.35, seed=2)
        fl.on = fl2.on = 1
        self.add(fl, fl2)
        sch = T("schematic", 22, GREY).move_to([5.8, -3.6, 0])
        self.add(sch)
        self.at("grow")
        self.play(tw(cell, 1.1, r=3.4), run_time=1.1)
        self.at("shape")
        sh = plate(T("same shape", 30, TEXT, weight=BOLD).move_to([-4.7, 3.3, 0]))
        self.play(FadeIn(sh), run_time=0.4)
        self.at("inside")
        r0 = plate(M("width  x2", 30, TEXT).move_to([-4.6, 2.4, 0]))
        r1 = plate(M("inside  x8", 30, GOLD).move_to([-4.6, 1.5, 0]))
        self.play(FadeIn(r0), run_time=0.4)
        self.play(FadeIn(r1), run_time=0.4)
        self.at("surface")
        r2 = plate(M("surface x4", 30, TEXT).move_to([-4.6, 0.6, 0]))
        self.play(FadeIn(r2), run_time=0.4)
        fl.tt = 0.0

        def reach(m, dt):
            m.tt += dt
            al = min(1.0, m.tt / 3.5)
            for f in (fl, fl2):
                f.depth = 0.35 + 0.5 * al
                f.speed = 0.25 - 0.17 * al
        fl.add_updater(reach)

        self.at("middle")
        self.play(tw(cell, 0.8, core=1.0), run_time=0.8)
        self.at("get food")
        ml = T("middle falls behind", 30, TEXT, weight=BOLD).move_to([-4.6, -2.0, 0])
        ma = Arrow(ml.get_right() + RIGHT * 0.05, [0.5, -0.4, 0], buff=0.05, color=TEXT, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(ml), GrowArrow(ma), run_time=0.5)
        self.play(tw(cell, 2.4, core=0.15), run_time=2.4)
        self.finish()


class S13Many(SpokenScene):
    def construct(self):
        cell = RCell((1.5, 0), 3.4, core=0.15)
        g = cell.geom
        fl = Flow(14, AMBER, g, True, ang=(120, 240), spread=0.3, depth=0.8, seed=1, speed=0.12)
        fl2 = Flow(14, CYAN, g, True, ang=(120, 240), spread=0.3, depth=0.8, seed=2, speed=0.12)
        fl.on = fl2.on = 1
        self.add(cell, fl, fl2)
        cl = Cluster((1.5, 0))
        wk = Walkers(cl)
        self.wait(1.0)
        self.at("many small cells")
        self.play(FadeOut(cell, run_time=1.6), FadeOut(fl, run_time=1.0), FadeOut(fl2, run_time=1.0),
                  Create(cl.chan, lag_ratio=0.02, run_time=2.0), LaggedStart(*[GrowFromCenter(c) for c in cl.cells], lag_ratio=0.04, run_time=2.0))
        self.add(wk)
        self.at("Each one")
        wk.on = 1
        self.at("watery fluid")
        fl_l = T("watery fluid", 32, WATER, weight=BOLD).move_to([-4.7, 0.3, 0])
        fa = Arrow(fl_l.get_right() + RIGHT * 0.05, cl.pts[min(range(len(cl.pts)), key=lambda i: cl.pts[i][0])] + LEFT * 0.25, buff=0.05, color=WATER, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(fl_l), GrowArrow(fa), run_time=0.6)
        self.finish()


class S14Share(SpokenScene):
    def construct(self):
        cl = Cluster((1.5, 0))
        wk = Walkers(cl)
        wk.on = 1
        self.add(cl, wk)
        icons = [icon(i, 1.0).move_to([6.15, 2.5 - i * 1.0, 0]) for i in range(6)]
        self.play(FadeIn(VGroup(*icons), shift=LEFT * 0.3), run_time=0.8)
        grp = groups_of(cl)
        for i, ic in enumerate(icons):
            ic.tt = i
            ic.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.shift(UP * 0.35 * dt * math.sin(3.0 * m.tt))))
        self.at("split up")
        fl = [np.array([1.5 + 1.2 * math.cos(math.radians(60 * k)), 1.0 * math.sin(math.radians(60 * k)), 0]) for k in range(6)]
        self.play(*[ic.animate.move_to(p).scale(1.2) for ic, p in zip(icons, fl)], run_time=1.5)
        self.at("Different groups")
        cen = [sum(cl.pts[i] for i in gr) / 3 for gr in grp]
        self.play(*[ic.animate.move_to(p) for ic, p in zip(icons, cen)], run_time=1.5)
        self.at("different jobs")
        self.play(*[cl.cells[i].animate.set_fill(JOB[k], 0.9).set_stroke(JOB[k]) for k, gr in enumerate(grp) for i in gr], run_time=0.9)
        self.finish()


class S15Name(SpokenScene):
    def construct(self):
        cl = Cluster((1.5, 0))
        wk = Walkers(cl)
        wk.on = 1
        grp = groups_of(cl)
        for k, gr in enumerate(grp):
            for i in gr:
                cl.cells[i].set_fill(JOB[k], 0.9).set_stroke(JOB[k])
        cen = [sum(cl.pts[i] for i in gr) / 3 for gr in grp]
        ics = VGroup(*[icon(k, 1.2).move_to(cen[k]) for k in range(6)])
        self.add(cl, wk, ics)
        self.at("division of labor")
        ban = T("division\nof labor", 50, GOLD, weight=BOLD).move_to([-4.3, 0.3, 0])
        self.play(FadeIn(ban, shift=DOWN * 0.15), run_time=0.8)
        self.at("A paramecium")
        pd = pond((-3.4, -0.2), 2.5)
        cell = Para(pos=(-3.4, -0.2), sc=0.55, wander=(-3.4, -0.2, 0.6, 0.4, 0.9))
        row = VGroup(*[icon(k, 0.7).move_to([-5.6 + 0.88 * k + 0.2, -3.2, 0]) for k in range(6)])
        ban2 = T("division of labor", 46, GOLD, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeOut(cl), FadeOut(wk), FadeOut(ics), FadeIn(pd), FadeIn(cell), FadeIn(row), ReplacementTransform(ban, ban2), run_time=0.9)
        self.at("does the whole list")
        marks = VGroup(*[check(GREEN, 0.7).move_to([-5.6 + 0.88 * k + 0.2, -3.62, 0]) for k in range(6)])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.25, run_time=1.8))
        self.at("You do the same")
        pk, pc = 0.74, (3.9, -0.45)
        outl = person(pk, pc)
        ms = mesh(pk, pc, lambda x, y: JOB[zone(x, y)])
        self.play(Create(outl), run_time=1.2)
        self.at("trillions")
        self.play(LaggedStart(*[FadeIn(d) for d in ms], lag_ratio=0.004, run_time=2.0))
        self.finish()


class S16End(EndCard):
    LINE = "Grow a cell in every direction, and its surface falls behind."
