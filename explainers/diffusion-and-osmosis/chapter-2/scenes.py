"""Water Drifts to the Saltier Side (diffusion-and-osmosis, film 2 of 2)

Same colour map and tank as film 1: membrane = WHITE dashed line; water = BLUE dots; salt = GREY squares;
tallies = WHITE arrows. Every tank and cell is a cartoon labelled 'schematic'.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PUR = "#B07CF0"
PINK = "#F08DAF"
CY, TW, TH = 0.25, 12.4, 5.0          # the big tank: centre y, width, height
P3 = lambda x, y: np.array([x, y, 0.0])


# ---------------------------------------------------------------------------------------------
# The world: dots with a home slot on each side, a gentle wobble, and timed hops across the line
# ---------------------------------------------------------------------------------------------
class World:
    def __init__(self, scene, specs, cx=0.0, cy=CY, w=TW, h=TH, amp=0.26, seed=11, flash=True, s=1.0, mt=0.42):
        self.mt = mt
        self.s, self.cx, self.cy, self.w, self.h, self.flash = s, cx, cy, w, h, flash
        n = len(specs)
        rng = np.random.default_rng(seed)
        self.slots = {"L": self._slots(rng, n, -1), "R": self._slots(rng, n, 1)}
        self.sides = [sp["side"] for sp in specs]
        self.colors = [sp.get("color", PUR) for sp in specs]
        self.dots = VGroup()
        for sp in specs:
            r = sp.get("r", 0.19) * s
            m = Square(side_length=2 * r * 0.9) if sp.get("shape") == "square" else Dot(radius=r)
            m.set_fill(sp.get("color", PUR), opacity=1).set_stroke(width=0)
            self.dots.add(m)
        self.anchor = [self.slots[sd][i].copy() for i, sd in enumerate(self.sides)]
        self.last = [a.copy() for a in self.anchor]
        self.q = [[] for _ in range(n)]
        self.free = [0.0] * n
        self.plan = list(self.sides)
        self.sgn = [-1 if sd == "L" else 1 for sd in self.sides]
        self.white = [False] * n
        self.ph = rng.uniform(0, 6.28, (n, 4))
        self.fr = rng.uniform(1.4, 3.4, (n, 4))
        self.amp = amp * s
        self.cross = {"lr": 0, "rl": 0}
        self.speed = 1.0
        self.t = scene.elapsed()
        for i, d in enumerate(self.dots):
            d.move_to(self.anchor[i])
        self.gop = ValueTracker(1.0)
        self.vt = [ValueTracker(1.0) for _ in range(n)]
        self.dots.add_updater(self._tick)

    def _slots(self, rng, n, sgn):
        s, cx, cy, w, h = self.s, self.cx, self.cy, self.w, self.h
        if sgn < 0:
            x0, x1 = cx - w / 2 + 0.45 * s, cx - 0.95 * s
        else:
            x0, x1 = cx + 0.95 * s, cx + w / 2 - 0.45 * s
        y0, y1 = cy - h / 2 + 0.42 * s, cy + h / 2 - self.mt * s
        pts = []
        dmin = 0.62 * s
        while len(pts) < n:
            for _ in range(400):
                p = P3(rng.uniform(x0, x1), rng.uniform(y0, y1))
                if all(np.linalg.norm(p - q) > dmin for q in pts):
                    pts.append(p)
                    break
            else:
                dmin *= 0.9
        return pts

    # -- scheduling -------------------------------------------------------------------------
    def route(self, i, pts, start=None):
        """Queue waypoints [(x, y, seconds), ...] for dot i."""
        t = max(self.t if start is None else start, self.free[i])
        p0 = self.last[i]
        for (x, y, dur) in pts:
            p1 = P3(x, y)
            self.q[i].append([t, t + dur, p0, p1])
            t += dur
            p0 = p1
        self.free[i] = t
        self.last[i] = p0

    def hop(self, i, to, t_cross):
        """Dot i hops to side 'L' or 'R'; it reaches the line, crosses, and settles; it crosses at t_cross."""
        s = self.s
        sg = -1 if self.plan[i] == "L" else 1
        start = max(t_cross - 1.25, self.free[i], self.t)
        src = self.last[i]
        dst = self.slots[to][i]
        ym = 0.5 * (src[1] + dst[1])
        nx = 0.38 * s
        self.route(i, [(self.cx + sg * nx, ym, 0.9), (self.cx - sg * nx, ym, 0.7), (dst[0], dst[1], 1.0)], start)
        self.plan[i] = to

    def bounce(self, i, t_touch):
        s = self.s
        src = self.last[i]
        sg = -1 if src[0] < self.cx else 1
        start = max(t_touch - 0.9, self.free[i], self.t)
        self.route(i, [(self.cx + sg * 0.42 * s, src[1], 0.9), (src[0], src[1], 1.1)], start)

    def pop(self, side):
        return sum(1 for x in self.sides if x == side)

    # -- the tick ---------------------------------------------------------------------------
    def _tick(self, grp, dt):
        self.t += dt * self.speed
        t = self.t
        for i, d in enumerate(self.dots):
            q = self.q[i]
            while q and t >= q[0][1]:
                done = q.pop(0)
                self.anchor[i] = done[3].copy()
                self._side(i, done[3][0])
            if q and t >= q[0][0]:
                t0, t1, p0, p1 = q[0]
                u = (t - t0) / (t1 - t0)
                u = u * u * (3 - 2 * u)
                a = p0 + (p1 - p0) * u
                self._side(i, a[0])
            else:
                a = self.anchor[i]
            ph, fr = self.ph[i], self.fr[i]
            ox = self.amp * 0.6 * (np.sin(fr[0] * t + ph[0]) - np.sin(ph[0]) + 0.6 * (np.sin(fr[1] * t + ph[1]) - np.sin(ph[1])))
            oy = self.amp * 0.6 * (np.sin(fr[2] * t + ph[2]) - np.sin(ph[2]) + 0.6 * (np.sin(fr[3] * t + ph[3]) - np.sin(ph[3])))
            d.move_to([a[0] + ox, a[1] + oy, 0])
            d.set_opacity(self.gop.get_value() * self.vt[i].get_value())
            if self.flash:
                near = bool(q) and t >= q[0][0] and abs(a[0] + ox - self.cx) < 0.5 * self.s
                if near != self.white[i]:
                    self.white[i] = near
                    d.set_fill(WHITE if near else self.colors[i])

    def _side(self, i, x):
        sg = -1 if x < self.cx else 1
        if sg != self.sgn[i]:
            self.sgn[i] = sg
            self.sides[i] = "L" if sg < 0 else "R"
            self.cross["lr" if sg > 0 else "rl"] += 1


# ---------------------------------------------------------------------------------------------
# Readouts that follow the world
# ---------------------------------------------------------------------------------------------
class LiveText(VGroup):
    def __init__(self, fn, pos, size=34, color=TEXT, op=1.0):
        super().__init__()
        self.fn, self.pos, self.size, self.color = fn, pos, size, color
        self.op = ValueTracker(op)
        self._v = self.fn()
        self._o = None
        self.add(T(self._v, size=self.size, color=self.color).move_to(self.pos))
        self.add_updater(self._upd)

    def _upd(self, m):
        v = self.fn()
        o = self.op.get_value()
        if v != self._v:
            self._v = v
            self._o = None
            self.submobjects[0].become(T(v, size=self.size, color=self.color).move_to(self.pos))
        if o != self._o:
            self._o = o
            self.submobjects[0].set_opacity(o)


def counters(w, xl=-4.6, xr=4.6, y=3.42, size=34, op=1.0):
    return VGroup(LiveText(lambda: f"left: {w.pop('L')}", P3(xl, y), size, TEXT, op),
                  LiveText(lambda: f"right: {w.pop('R')}", P3(xr, y), size, TEXT, op))


class Tally(VGroup):
    """White arrows with counters: '-> N' (left to right) and '<- N' (right to left)."""
    def __init__(self, w, x=0.0, y=3.42, gap=1.45, size=34, op=0.0):
        super().__init__()
        self.w = w
        self.op = ValueTracker(op)
        ar = lambda a, b: Arrow(P3(a, y), P3(b, y), buff=0, color=WHITE, stroke_width=7, tip_length=0.28,
                                max_tip_length_to_length_ratio=0.5)
        self.a1, self.a2 = ar(x - gap - 0.55, x - gap + 0.35), ar(x + gap + 0.35, x + gap - 0.55)
        self.n1 = LiveText(lambda: f"{w.cross['lr']}", P3(x - gap + 0.8, y), size, WHITE, op)
        self.n2 = LiveText(lambda: f"{w.cross['rl']}", P3(x - gap + 1.6, y), size, WHITE, op)
        self.add(self.a1, self.n1, self.a2, self.n2)
        self.add_updater(self._upd)

    def _upd(self, m):
        o = self.op.get_value()
        self.a1.set_opacity(o)
        self.a2.set_opacity(o)
        self.n1.op.set_value(o)
        self.n2.op.set_value(o)


class Bars(VGroup):
    """Purple shading under each half: darker where the dots are more crowded (follows the world)."""
    def __init__(self, w, y=-2.5, color=PUR, op=1.0):
        super().__init__()
        self.w, self.color = w, color
        self.op = ValueTracker(op)
        hw = w.w / 2 - 0.05
        self.l = Rectangle(width=hw, height=0.32, stroke_width=0).move_to(P3(w.cx - hw / 2 - 0.05, y))
        self.r = Rectangle(width=hw, height=0.32, stroke_width=0).move_to(P3(w.cx + hw / 2 + 0.05, y))
        self.dl = w.pop("L") / 14
        self.dr = w.pop("R") / 14
        self.add(self.l, self.r)
        self.add_updater(self._upd)

    def _upd(self, m, dt=0):
        k = min(1.0, 0.04)
        self.dl += (self.w.pop("L") / 14 - self.dl) * k
        self.dr += (self.w.pop("R") / 14 - self.dr) * k
        o = self.op.get_value()
        self.l.set_fill(self.color, opacity=o * (0.06 + 0.9 * self.dl))
        self.r.set_fill(self.color, opacity=o * (0.06 + 0.9 * self.dr))


# ---------------------------------------------------------------------------------------------
# Static pieces
# ---------------------------------------------------------------------------------------------
def tank_base(cx=0.0, cy=CY, w=TW, h=TH):
    water = Rectangle(width=w, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.14).move_to(P3(cx, cy))
    outline = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to(P3(cx, cy))
    return VGroup(water, outline)


def open_line(cx=0.0, cy=CY, h=TH):
    return DashedLine(P3(cx, cy - h / 2), P3(cx, cy + h / 2), dash_length=0.1, dashed_ratio=0.4, color=GREY, stroke_width=4)


def membrane(cx=0.0, cy=CY, h=TH):
    return DashedLine(P3(cx, cy - h / 2), P3(cx, cy + h / 2), dash_length=0.24, dashed_ratio=0.62, color=WHITE, stroke_width=8)


def cell_fill(cx=0.0, cy=CY, w=TW, h=TH):
    return RoundedRectangle(corner_radius=0.35, width=w / 2 - 0.12, height=h - 0.14, stroke_color=PINK, stroke_width=3,
                            fill_color=PINK, fill_opacity=0.2).move_to(P3(cx + w / 4 + 0.03, cy))


def schem(x=6.15, y=-3.72):
    return T("schematic", size=22, color=GREY).move_to(P3(x, y))


def caption(text, y=-3.05, size=30, color=TEXT):
    return T(text, size=size, color=color).move_to(P3(0, y))


S_12_2 = ["L"] * 12 + ["R"] * 2
LEFT_AFTER_6 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 12}
LEFT_S9 = {0, 1, 2, 3, 4, 5, 12}


def specs_from_left(left, color=PUR, n=14):
    return [{"side": "L" if i in left else "R", "color": color} for i in range(n)]


def specs_12_2(color=PUR):
    return [{"side": s, "color": color} for s in S_12_2]


def dim_anim(base, line, sch):
    return [base[0].animate.set_fill(opacity=0.05), base[1].animate.set_stroke(opacity=0.4),
            line.animate.set_stroke(opacity=0.4), sch.animate.set_opacity(0.4)]


class SS(SpokenScene):
    def idle(self, until=None):
        """Hold (dots keep moving) until scene time `until`."""
        rest = (until if until is not None else self.narration_s) - self.elapsed()
        if rest > 0.02:
            self.wait(rest)




# =============================================================================================
# Film 2 pieces
# =============================================================================================
OLIVE = "#6FAE4F"
CUKE = "#3E7D3A"
CUKE_L = "#A8D08D"
LEAF = "#7BC96F"
CLK = {"t": 0.0}


def ambient(scene):
    """A clock every scene can read from updaters (scene time)."""
    m = Mobject()
    CLK["t"] = scene.elapsed()

    def tick(mm, dt):
        CLK["t"] += dt
    m.add_updater(tick)
    scene.add(m)
    return m


def until(scene, t):
    rest = t - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


def drive(scene, tracker, t0, t1, v0, v1):
    """Move a tracker from v0 to v1 between scene times t0 and t1 (runs while anything else plays or waits)."""
    m = Mobject()

    def f(mm, dt):
        u = float(np.clip((CLK["t"] - t0) / (t1 - t0), 0, 1))
        u = u * u * (3 - 2 * u)
        tracker.set_value(v0 + (v1 - v0) * u)
    m.add_updater(f)
    scene.add(m)


def scatter(rng, n, xr, yr, dmin, avoid=()):
    pts = []
    d = dmin
    while len(pts) < n:
        for _ in range(500):
            p = np.array([rng.uniform(*xr), rng.uniform(*yr)])
            if all(np.linalg.norm(p - q) > d for q in list(pts) + list(avoid)):
                pts.append(p)
                break
        else:
            d *= 0.92
    return pts


# ---- the tank (same look as film 1) with two water levels ------------------------------------
class Tank2:
    def __init__(self, dl=0.0, dr=0.0, dim=1.0):
        self.dl, self.dr, self.dim = ValueTracker(dl), ValueTracker(dr), ValueTracker(dim)
        self.out = Rectangle(width=TW, height=TH, stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to(P3(0, CY))
        self.mem = membrane()
        self.sch = schem()
        self.fl, self.fr = self._fill(-1), self._fill(1)

    def _fill(self, side):
        def f():
            tr = self.dl if side < 0 else self.dr
            top = CY + TH / 2 - 0.55 + tr.get_value()
            bot = CY - TH / 2
            return Rectangle(width=TW / 2, height=top - bot, stroke_width=0, fill_color=BLUE,
                             fill_opacity=0.2 * self.dim.get_value()).move_to(P3(side * TW / 4, (top + bot) / 2))
        return always_redraw(f)

    def parts(self):
        return [self.fl, self.fr, self.out, self.mem, self.sch]

    def dim_anims(self, v=0.3, so=0.4):
        return [self.dim.animate.set_value(v), self.out.animate.set_stroke(opacity=so),
                self.mem.animate.set_stroke(opacity=so), self.sch.animate.set_opacity(so)]

    def undim_anims(self):
        return self.dim_anims(1.0, 1.0)


def specs_tank():
    sp = [{"side": "L", "color": BLUE, "r": 0.25} for _ in range(11)]
    sp += [{"side": "R", "color": BLUE, "r": 0.25} for _ in range(8)]
    sp += [{"side": "R", "color": GREY, "shape": "square", "r": 0.25} for _ in range(4)]
    return sp


WL = list(range(0, 11))
WR = list(range(11, 19))
SALT = list(range(19, 23))


class TankScene(SS):
    def stage(self, dl=0.0, dr=0.0, dim=1.0, wop=1.0):
        ambient(self)
        self.tk = Tank2(dl, dr, dim)
        self.w = World(self, specs_tank(), mt=0.9)
        self.w.gop.set_value(wop)
        self.add(*self.tk.parts(), self.w.dots)
        return self.w

    def bounces(self, times, ids=SALT):
        for k, t in enumerate(times):
            self.w.bounce(ids[k % len(ids)], t)


# ---- the cell ----------------------------------------------------------------------------------
class Cell:
    def __init__(self, cx=0.0, cy=0.0, sc=1.0, k=1.0, km=1.0):
        self.c = np.array([cx, cy, 0.0])
        self.sc = sc
        self.k, self.km, self.op = ValueTracker(k), ValueTracker(km), ValueTracker(1.0)
        self.wall = always_redraw(self._wall)
        self.mem = always_redraw(self._mem)
        self.vac = always_redraw(self._vac)

    def _wall(self):
        sc = self.sc
        return RoundedRectangle(corner_radius=0.5 * sc, width=7.0 * sc, height=4.4 * sc, stroke_color=OLIVE,
                                stroke_width=max(3, 10 * sc), stroke_opacity=self.op.get_value(), fill_opacity=0).move_to(self.c)

    def _mem(self):
        sc, kk = self.sc, self.km.get_value()
        r = RoundedRectangle(corner_radius=0.4 * sc, width=6.55 * sc * kk, height=3.95 * sc * kk).move_to(self.c)
        return DashedVMobject(r, num_dashes=48, dashed_ratio=0.6).set_stroke(WHITE, max(2, 6 * sc), opacity=self.op.get_value())

    def _vac(self):
        sc, k = self.sc, self.k.get_value()
        return RoundedRectangle(corner_radius=0.5 * sc * k, width=5.9 * sc * k, height=3.4 * sc * k, stroke_color=BLUE,
                                stroke_width=3, stroke_opacity=0.8 * self.op.get_value(), fill_color=BLUE,
                                fill_opacity=0.26 * self.op.get_value()).move_to(self.c)

    def parts(self):
        return [self.vac, self.wall, self.mem]


class Jig:
    """Dots in and around a cell. mode 'vac' = positions scale with the vacuole; 'fix' = fixed in the cell frame."""
    def __init__(self, scene, cell, items, seed=5, amp=0.26):
        self.cell, self.items = cell, items
        self.sc = cell.sc
        self.t = scene.elapsed()
        self.cross = {"out": 0, "in": 0}
        rng = np.random.default_rng(seed)
        self.dots = VGroup()
        for it in items:
            if it["k"] == "s":
                m = Square(side_length=0.42 * self.sc).set_fill(GREY, 1).set_stroke(width=0)
            else:
                m = Dot(radius=0.24 * self.sc).set_fill(BLUE, 1).set_stroke(width=0)
            it["q"] = []
            it["free"] = 0.0
            it["ph"] = rng.uniform(0, 6.28, 4)
            it["fr"] = rng.uniform(1.4, 3.4, 4)
            self.dots.add(m)
        self.amp = amp * self.sc
        self.gop = ValueTracker(1.0)
        for it in items:
            it["vt"] = ValueTracker(1.0)
        self.dots.add_updater(self._tick)
        for i, m in enumerate(self.dots):
            m.move_to(self._base(items[i]["m"], items[i]["x"], items[i]["y"]))

    def sel(self, fn):
        return VGroup(*[d for d, it in zip(self.dots, self.items) if fn(it)])

    def _base(self, mode, x, y):
        s = self.sc * (self.cell.k.get_value() if mode == "vac" else 1.0)
        return self.cell.c + np.array([x * s, y * s, 0.0])

    def go(self, i, t0, mode, x, y, dur=1.6, cnt=None):
        it = self.items[i]
        t0 = max(t0, it["free"], self.t)
        it["q"].append({"t0": t0, "t1": t0 + dur, "fm": mode, "fx": x, "fy": y, "p0": None, "cnt": cnt, "done": False})
        it["free"] = t0 + dur

    def bounce(self, i, t, dx):
        it = self.items[i]
        x, y = it["x"], it["y"]
        self.go(i, t - 0.8, "fix", x + dx, y, 0.8)
        self.go(i, t, "fix", x, y, 0.9)

    def _tick(self, grp, dt):
        self.t += dt
        t = self.t
        for i, d in enumerate(self.dots):
            it = self.items[i]
            q = it["q"]
            while q and t >= q[0]["t1"]:
                s = q.pop(0)
                it["m"], it["x"], it["y"] = s["fm"], s["fx"], s["fy"]
                if s["cnt"] and not s["done"]:
                    self.cross[s["cnt"]] += 1
            if q and t >= q[0]["t0"]:
                s = q[0]
                if s["p0"] is None:
                    s["p0"] = self._base(it["m"], it["x"], it["y"])
                u = (t - s["t0"]) / (s["t1"] - s["t0"])
                if s["cnt"] and u >= 0.5 and not s["done"]:
                    s["done"] = True
                    self.cross[s["cnt"]] += 1
                u = u * u * (3 - 2 * u)
                tgt = self._base(s["fm"], s["fx"], s["fy"])
                a = s["p0"] + (tgt - s["p0"]) * u
            else:
                a = self._base(it["m"], it["x"], it["y"])
            ph, fr = it["ph"], it["fr"]
            ox = self.amp * 0.6 * (np.sin(fr[0] * t + ph[0]) - np.sin(ph[0]) + 0.6 * (np.sin(fr[1] * t + ph[1]) - np.sin(ph[1])))
            oy = self.amp * 0.6 * (np.sin(fr[2] * t + ph[2]) - np.sin(ph[2]) + 0.6 * (np.sin(fr[3] * t + ph[3]) - np.sin(ph[3])))
            d.move_to([a[0] + ox, a[1] + oy, 0])
            d.set_opacity(self.gop.get_value() * it["vt"].get_value())

    def vis(self, fn, v, anim=True):
        tr = [it["vt"] for it in self.items if fn(it)]
        return [t.animate.set_value(v) for t in tr] if anim else [t.set_value(v) for t in tr]


def water(m, x, y, g="in"):
    return {"k": "w", "m": m, "x": float(x), "y": float(y), "g": g}


def salt(m, x, y, g="in"):
    return {"k": "s", "m": m, "x": float(x), "y": float(y), "g": g}


def bath(op=1.0):
    return Rectangle(width=12.4, height=5.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.16 * op).move_to(P3(0, 0))


def cuke_items():
    rng = np.random.default_rng(7)
    items = []
    sin_ = [(-1.3, 0.7), (1.5, -0.6), (0.1, 0.05)]
    for (x, y) in sin_:
        items.append(salt("vac", x, y, "in"))
    for p in scatter(rng, 14, (-2.35, 2.35), (-1.25, 1.25), 0.78, avoid=sin_):
        items.append(water("vac", p[0], p[1], "in"))
    used = []
    for sg in (-1, 1):
        pts = scatter(rng, 14, (4.15, 5.95) if sg > 0 else (-5.95, -4.15), (-2.55, 2.55), 0.66, avoid=used)
        used += pts
        for j, p in enumerate(pts):
            if j < 4:
                items.append(water("fix", p[0], p[1], "outw"))
            elif j < 10:
                items.append(salt("fix", p[0], p[1], "outs"))
            else:
                items.append(water("fix", p[0], p[1], "spare"))   # spare spots water will drift out to
    return items


def lettuce_items():
    rng = np.random.default_rng(9)
    items = []
    pts = scatter(rng, 9, (-2.3, 2.3), (-1.2, 1.2), 0.8)
    for j, p in enumerate(pts):
        items.append(salt("vac", p[0], p[1], "in") if j < 5 else water("vac", p[0], p[1], "inw"))
    used = []
    left = scatter(rng, 6, (-5.8, -4.2), (-2.5, 2.5), 0.7)
    used += left
    top = [np.array([-1.8, 2.62]), np.array([1.8, 2.62]), np.array([-1.8, -2.62]), np.array([1.8, -2.62])]
    for p in left + top:
        items.append(water("fix", p[0], p[1], "outw"))
    items.append(salt("fix", 5.0, -2.2, "outs"))
    return items


# ---- the cucumber slice -----------------------------------------------------------------------
SLX, SLY, SLR = -2.2, 0.2, 1.9


def slice_group(cx=SLX, cy=SLY, r=SLR, beads_on=True, bead_tr=None, salt_on=True):
    plate = Circle(radius=r + 0.85, stroke_color=GREY, stroke_width=6, fill_color=GREY, fill_opacity=0.12).move_to(P3(cx, cy))
    sl = Circle(radius=r, stroke_color=CUKE_L, stroke_width=9, fill_color=CUKE, fill_opacity=0.9).move_to(P3(cx, cy))
    ring = Circle(radius=r * 0.78, stroke_color="#7DB36B", stroke_width=3, fill_opacity=0).move_to(P3(cx, cy))
    seeds = VGroup()
    for a in np.linspace(0, 2 * PI, 9)[:-1]:
        e = Ellipse(width=0.26, height=0.12, fill_color="#E6EFC2", fill_opacity=1, stroke_width=0)
        e.rotate(a).move_to(P3(cx + 0.62 * np.cos(a), cy + 0.62 * np.sin(a)))
        seeds.add(e)
    return VGroup(plate, sl, ring, seeds)


BEAD_SPOTS = [(-0.9, 1.0), (0.5, 1.2), (1.2, 0.2), (0.9, -1.0), (-0.3, -1.3), (-1.3, -0.4), (0.0, 0.0)]
SALT_SPOTS = [(-1.2, 0.5), (0.2, 0.9), (1.0, 0.6), (-0.5, -0.2), (0.7, -0.4), (-1.0, -1.0), (0.1, -0.8), (1.2, -0.9), (-0.2, 1.4), (-1.5, 0.1)]


def beads(gt, cx=SLX, cy=SLY, shimmer=True):
    out = []
    for k, (dx, dy) in enumerate(BEAD_SPOTS):
        def f(dx=dx, dy=dy, k=k):
            g = gt.get_value()
            r = 0.3 * g * (1 + 0.1 * np.sin(2.0 * CLK["t"] + k))
            return Circle(radius=max(r, 0.001), stroke_color=WHITE, stroke_width=2 * min(1, g), fill_color=BLUE,
                          fill_opacity=0.75 * min(1, g * 3)).move_to(P3(cx + dx, cy + dy))
        out.append(always_redraw(f))
    return out


def salt_on_slice(op_tr, cx=SLX, cy=SLY):
    out = []
    for k, (dx, dy) in enumerate(SALT_SPOTS):
        def f(dx=dx, dy=dy, k=k):
            o = op_tr.get_value() * (0.75 + 0.25 * np.sin(2.5 * CLK["t"] + 1.7 * k))
            return Square(side_length=0.15, stroke_width=0, fill_color=GREY, fill_opacity=o).rotate(0.5 * k).move_to(P3(cx + dx, cy + dy))
        out.append(always_redraw(f))
    return out


class Leaf:
    """Two lettuce leaves in a bowl; `crisp` 0 = limp, 1 = upright."""
    def __init__(self, crisp=0.0, op=1.0):
        self.crisp, self.op = ValueTracker(crisp), ValueTracker(op)
        self.bowl = Sector(radius=2.7, start_angle=PI, angle=PI, stroke_color=GREY, stroke_width=6, fill_color=BLUE, fill_opacity=0.3).move_to(P3(0, -1.25))
        self.leaf_l = always_redraw(lambda: self._leaf(-1))
        self.leaf_r = always_redraw(lambda: self._leaf(1))

    @staticmethod
    def _bez(p, s):
        return ((1 - s) ** 3)[:, None] * p[0] + (3 * (1 - s) ** 2 * s)[:, None] * p[1] + (3 * (1 - s) * s ** 2)[:, None] * p[2] + (s ** 3)[:, None] * p[3]

    def _leaf(self, sg):
        c = self.crisp.get_value()
        limp = np.array([[0.2, -1.0], [0.9, 1.5], [2.5, 1.8], [3.4, -0.7]])
        crisp = np.array([[0.1, -1.0], [0.4, 0.4], [1.2, 1.9], [1.6, 3.3]])
        P = (1 - c) * limp + c * crisp
        P = P * np.array([sg, 1])
        s = np.linspace(0, 1, 40)
        pts = self._bez(P, s)
        d = np.gradient(pts, axis=0)
        n = np.stack([-d[:, 1], d[:, 0]], 1)
        n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
        w = 0.55 * np.sin(np.pi * s) ** 0.6 + 0.03
        a = pts + n * w[:, None]
        b = pts - n * w[:, None]
        poly = np.vstack([a, b[::-1]])
        m = VMobject(stroke_color=CUKE_L, stroke_width=5, stroke_opacity=self.op.get_value(), fill_color=LEAF,
                     fill_opacity=0.9 * self.op.get_value())
        m.set_points_as_corners([P3(x, y) for x, y in poly] + [P3(*poly[0])])
        return m

    def parts(self):
        return [self.bowl, self.leaf_l, self.leaf_r]


def counters_cell(j, op=0.0, y=3.42):
    a = LiveText(lambda: f"→ out {j.cross['out']}", P3(-2.6, y), 34, WHITE, op)
    b = LiveText(lambda: f"← in {j.cross['in']}", P3(2.6, y), 34, WHITE, op)
    return VGroup(a, b)


def two_part(y1=1.5, y2=0.5, size=28):
    def row(a, b, ca, cb, y):
        r = VGroup(T(a, size=size, color=ca), Arrow(LEFT * 0.55, RIGHT * 0.55, buff=0, color=WHITE, stroke_width=7, tip_length=0.25),
                   T(b, size=size, color=cb)).arrange(RIGHT, buff=0.3)
        fit(r, max_w=10.8)
        return r.move_to(P3(0, y))
    return row("more water", "less water", BLUE, BLUE, y1), row("fewer dissolved particles", "more dissolved particles", TEXT, TEXT, y2)


def battery():
    body = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.8, stroke_color=WHITE, stroke_width=5)
    tip = Rectangle(width=0.14, height=0.36, fill_color=WHITE, fill_opacity=1, stroke_width=0).next_to(body, RIGHT, buff=0)
    cells = VGroup(*[Rectangle(width=0.28, height=0.56, fill_color=GREEN, fill_opacity=1, stroke_width=0) for _ in range(4)]).arrange(RIGHT, buff=0.08).move_to(body)
    return VGroup(body, tip, cells)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Diffusion and Osmosis"
    TITLE = "Water Drifts to the Saltier Side"


# ---------------------------------------------------------------------------------------------
class S01Hook(SS):
    def construct(self):
        ambient(self)
        sg = slice_group()
        gt = ValueTracker(0.0)
        bd = beads(gt)
        sop = ValueTracker(0.0)
        sl = salt_on_slice(sop)
        cx, cy = 3.7, 1.0
        face = Circle(radius=1.25, stroke_color=WHITE, stroke_width=6, fill_opacity=0).move_to(P3(cx, cy))
        ticks = VGroup(*[Line(P3(cx + 1.05 * np.sin(a), cy + 1.05 * np.cos(a)), P3(cx + 1.2 * np.sin(a), cy + 1.2 * np.cos(a)), stroke_width=4, color=GREY) for a in np.arange(0, 2 * PI, PI / 2)])
        ang = ValueTracker(0.0)
        hand = always_redraw(lambda: Line(P3(cx, cy), P3(cx + 0.95 * np.sin(ang.get_value()), cy + 0.95 * np.cos(ang.get_value())), color=GOLD, stroke_width=7))
        crystals = VGroup(*[Square(side_length=0.24, stroke_width=0, fill_color=GREY, fill_opacity=1) for _ in range(10)])
        ct = ValueTracker(0.0)
        tg = [P3(SLX + dx, SLY + dy) for dx, dy in SALT_SPOTS]

        def fall(g, dt):
            for k, c in enumerate(g):
                u = float(np.clip((CLK["t"] - 0.5 - 0.32 * k) / 1.3, 0, 1))
                c.move_to(P3(tg[k][0], 3.8 + (tg[k][1] - 3.8) * u * u))
                c.set_opacity(1.0 if u < 1 else 0.0)
            sop.set_value(1.0 if CLK["t"] > 0.5 + 0.32 * 9 + 1.3 else 0.0)
        crystals.add_updater(fall)
        sweep = always_redraw(lambda: Sector(radius=1.1, start_angle=PI / 2, angle=-max(ang.get_value(), 0.001), fill_color=GOLD, fill_opacity=0.35, stroke_width=0, arc_center=P3(cx, cy)))
        self.add(*sl, crystals, sweep, hand, *bd)
        self.play(FadeIn(sg), FadeIn(face), FadeIn(ticks), run_time=0.8)
        # per-crystal landing: a crystal stays on the slice once it lands
        drive(self, ang, 1.0, 6.8, 0.0, PI / 2)
        drive(self, gt, 3.3, 6.3, 0.0, 1.0)
        until(self, 6.8)
        t15 = T("15 min", size=40, color=GOLD).move_to(P3(cx, cy - 1.95))
        self.play(FadeIn(t15, shift=UP * 0.1), run_time=0.5)
        q = chip("where did the water come from?", TEAL, size=34).move_to(P3(0, -3.2))
        self.at("So where", lead=0.2)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Link(TankScene):
    def construct(self):
        ambient(self)
        self.tk = Tank2()
        sp = [{"side": s, "color": PUR} for s in S_12_2]
        w = World(self, sp, mt=0.9)
        self.w = w
        tal = Tally(w, x=0.0, op=0.0)
        self.add(*self.tk.parts(), w.dots, tal)
        # 3 hops left to right, 1 right to left
        for k, (i, to, t) in enumerate([(2, "R", 1.2), (5, "R", 2.2), (7, "R", 3.0), (13, "L", 3.9)]):
            w.hop(i, to, t)
        self.play(tal.op.animate.set_value(1.0), run_time=0.6)
        self.at("from crowded", lead=0.2)
        cap = caption("crowded → less crowded", y=-3.1, size=30)
        self.play(FadeIn(cap), run_time=0.6)
        # the salt world replaces the dyes
        w2 = World(self, [{"side": "R", "color": GREY, "shape": "square"} for _ in range(8)], seed=4, mt=0.9)
        w2.gop.set_value(0)
        self.add(w2.dots)
        self.at("This time", lead=0.2)
        self.play(w.gop.animate.set_value(0), tal.op.animate.set_value(0), FadeOut(cap), w2.gop.animate.set_value(1), run_time=1.0)
        self.remove(w.dots, tal)
        for k, t in enumerate([self.t_of("holds it") - 0.1, self.t_of("holds it") + 0.5, self.t_of("back") + 0.1, self.t_of("back") + 0.7]):
            w2.bounce(k, t)
        lab = T("salt", size=34, color=GREY).move_to(P3(3.1, -3.1))
        self.at("salt", lead=0.1)
        self.play(FadeIn(lab), run_time=0.5)
        self.at("membrane", lead=0.2)
        self.play(self.tk.mem.animate.set_stroke(width=12), run_time=0.6)
        self.play(self.tk.mem.animate.set_stroke(width=8), run_time=0.6)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Tank(TankScene):
    def construct(self):
        ambient(self)
        self.tk = Tank2()
        w = World(self, specs_tank(), mt=0.9)
        self.w = w
        for v in w.vt:
            v.set_value(0.0)
        self.add(self.tk.out, self.tk.fl, self.tk.fr, w.dots)
        self.play(GrowFromPoint(self.tk.out, point=P3(-0.8, 0)), FadeIn(self.tk.fl), FadeIn(self.tk.fr), FadeIn(self.tk.sch), run_time=1.4)
        self.at("membrane", lead=0.2)
        self.play(Create(self.tk.mem), run_time=1.2)
        w.hop(1, "R", 5.4)
        w.hop(12, "L", 6.9)
        w.hop(4, "R", 8.8)
        self.at("Blue water", lead=0.2)
        self.play(*[w.vt[i].animate.set_value(1.0) for i in WL + WR], run_time=1.0)
        self.at("Gray salt", lead=0.2)
        self.play(*[w.vt[i].animate.set_value(1.0) for i in SALT], run_time=1.0)
        self.bounces([self.t_of("holds back") + 0.0, self.t_of("holds back") + 0.7, self.t_of("all the salt") + 0.2, self.t_of("all the salt") + 0.9, self.t_of("Real ones") - 0.4])
        self.at("In this model", lead=0.2)
        c1 = chip("model: all salt held back", TEAL, size=30).move_to(P3(0, 3.4))
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.6)
        self.at("Real ones", lead=0.2)
        c2 = T("real ones: a little through, much slower", size=28, color=TEXT).move_to(P3(0, -3.2))
        self.play(FadeIn(c2), run_time=0.7)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
def grid_panel(cx, cy, n_salt, grp_color=BLUE):
    rect = RoundedRectangle(corner_radius=0.25, width=5.0, height=2.5, stroke_color=TEAL, stroke_width=4, fill_color=BG, fill_opacity=0.93).move_to(P3(cx, cy))
    cells, items = VGroup(), []
    for i in range(2):
        for j in range(5):
            p = P3(cx + (j - 2) * 0.88, cy + (0.5 - i) * 0.95)
            cells.add(Square(side_length=0.7, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(p).set_stroke(opacity=0.5))
            items.append(p)
    return rect, cells, items


def space_item(p, salty):
    if salty:
        return Square(side_length=0.46, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to(p)
    return Dot(radius=0.27, color=BLUE).set_stroke(width=0).move_to(p)


class JiggleGrid(VGroup):
    """Grid contents that jiggle; per-item scale (`sc`) and opacity (`op`) trackers so single items can change."""
    def __init__(self, items):
        super().__init__(*items)
        self.bases = [m.copy() for m in items]
        self.base = [m.get_center().copy() for m in items]
        self.sc = [ValueTracker(1.0) for _ in items]
        self.op = [ValueTracker(1.0) for _ in items]
        self.ph = np.random.default_rng(2).uniform(0, 6.28, (len(items), 2))
        self.add_updater(self._u)

    def _u(self, g):
        t = CLK["t"]
        for k, (m, b, p) in enumerate(zip(g, self.base, self.ph)):
            m.become(self.bases[k].copy().scale(self.sc[k].get_value()).set_opacity(self.op[k].get_value())
                     .move_to(b + np.array([0.05 * np.sin(2.3 * t + p[0]), 0.05 * np.sin(2.9 * t + p[1]), 0])))


class S04Spoonful(TankScene):
    def construct(self):
        w = self.stage()
        w.hop(1, "R", 2.0)
        w.hop(13, "L", 3.4)
        spoon = VGroup(Ellipse(width=0.9, height=0.6, stroke_color=WHITE, stroke_width=6, fill_color=WHITE, fill_opacity=0.12),
                       Line(P3(0.4, 0.0), P3(1.9, 1.2), color=WHITE, stroke_width=7)).move_to(P3(-3.6, 1.8))
        self.at("spoonful", lead=0.3)
        self.play(FadeIn(spoon), run_time=0.3)
        self.play(spoon.animate.shift(DOWN * 0.7), run_time=0.35)
        self.play(spoon.animate.shift(UP * 0.7), run_time=0.35)
        self.play(spoon.animate.move_to(P3(3.6, 1.8)), run_time=0.5)
        self.play(spoon.animate.shift(DOWN * 0.7), run_time=0.35)
        self.play(spoon.animate.shift(UP * 0.7), run_time=0.35)
        rL, cL, iL = grid_panel(-3.1, 0.4, 0)
        rR, cR, iR = grid_panel(3.1, 0.4, 3)
        wl = JiggleGrid([space_item(p, False) for p in iL])
        wr_items = [space_item(p, False) for p in iR]
        for k in (1, 4, 8):
            pass
        squares = {k: space_item(iR[k], True) for k in (2, 5, 8)}
        wr = JiggleGrid(wr_items + list(squares.values()))
        for j_ in range(10, 13):
            wr.op[j_].set_value(0.0)
        ca = T("cartoon spaces, not real ones", size=28, color=GREY).move_to(P3(0, -3.1))
        self.at("On the left", lead=0.2)
        self.play(*self.tk.dim_anims(0.35), w.gop.animate.set_value(0.2), FadeOut(spoon), FadeIn(rL), FadeIn(cL), run_time=0.5)
        self.add(wl)
        self.play(FadeIn(wl), FadeIn(ca), run_time=0.4)
        lL = T("water: 10 of 10", size=34, color=BLUE).move_to(P3(-3.1, -1.3))
        self.at("every space", lead=0.2)
        self.play(FadeIn(lL, shift=UP * 0.1), run_time=0.6)
        self.at("On the right", lead=0.2)
        self.play(FadeIn(rR), FadeIn(cR), run_time=0.6)
        self.add(wr)
        self.play(FadeIn(wr), run_time=0.6)
        self.at("hold salt", lead=0.2)
        self.play(*[wr.op[k].animate.set_value(0.0) for k in (2, 5, 8)], *[wr.op[j_].animate.set_value(1.0) for j_ in range(10, 13)], run_time=1.0)
        self.at("less water", lead=0.5)
        lR = T("water: 7 of 10", size=34, color=BLUE).move_to(P3(3.1, -1.3))
        self.play(FadeIn(lR, shift=UP * 0.1), run_time=0.6)
        self.idle()
        self.finish()


class S05Scale(TankScene):
    def construct(self):
        w = self.stage(dim=0.35, wop=0.2)
        self.tk.out.set_stroke(opacity=0.4)
        self.tk.mem.set_stroke(opacity=0.4)
        self.tk.sch.set_opacity(0.4)
        rL, cL, iL = grid_panel(-3.1, 0.4, 0)
        rR, cR, iR = grid_panel(3.1, 0.4, 3)
        wl = JiggleGrid([space_item(p, False) for p in iL])
        items = [space_item(p, k in (2, 5, 8)) for k, p in enumerate(iR)]
        wr = JiggleGrid(items)
        lR = T("water: 7 of 10", size=34, color=BLUE).move_to(P3(3.1, -1.3))
        lL = T("water: 10 of 10", size=34, color=BLUE).move_to(P3(-3.1, -1.3))
        ca = T("cartoon spaces, not real ones", size=28, color=GREY).move_to(P3(0, -3.1))
        self.add(rL, cL, wl, rR, cR, wr, lR, lL, ca)
        # many extra, small blue dots for the "real" picture
        rng = np.random.default_rng(12)
        pts = scatter(rng, 40, (0.8, 5.4), (-0.7, 1.5), 0.3, avoid=[np.array([p[0], p[1]]) for p in iR])
        extra = VGroup(*[Dot(radius=0.1, color=BLUE).set_stroke(width=0).move_to(P3(p[0], p[1])) for p in pts])
        extra.set_opacity(0)
        self.add(extra)
        # let the grid sit a moment while the drifting tank behind it keeps moving
        self.play(FadeOut(rL), FadeOut(cL), FadeOut(wl), FadeOut(lL), run_time=1.0)
        self.at("We drew", lead=0.2)
        ban = chip("salt exaggerated so you can see it", GOLD, size=28).move_to(P3(0, 3.4))
        self.play(FadeIn(ban, shift=DOWN * 0.1), run_time=0.7)
        self.at("Real salt", lead=0.3)
        self.play(*[wr.sc[k].animate.set_value(0.3) for k in (2, 5, 8)], extra.animate.set_opacity(1), FadeOut(lR), run_time=1.6)
        self.at("The difference", lead=0.3)
        self.play(*[wr.sc[k].animate.set_value(1.0) for k in (2, 5, 8)], extra.animate.set_opacity(0), run_time=1.4)
        lR2 = T("water: 7 of 10", size=34, color=BLUE).move_to(P3(3.1, -1.3))
        self.play(FadeIn(lR2), run_time=0.6)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
def predict_card(tr):
    box = RoundedRectangle(corner_radius=0.3, width=11.6, height=4.0, stroke_color=TEAL, stroke_width=4, fill_color=BG, fill_opacity=0.93).move_to(P3(0, 0.3))
    q = VGroup(T("Which way will MORE", size=38), T("water dots cross?", size=38)).arrange(DOWN, buff=0.12).move_to(P3(0, 1.45))

    def button(label, rightward, x):
        rect = RoundedRectangle(corner_radius=0.2, width=5.2, height=0.95, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.15)
        a, b = (LEFT * 0.35, RIGHT * 0.35) if rightward else (RIGHT * 0.35, LEFT * 0.35)
        arr = Arrow(a, b, buff=0, color=WHITE, stroke_width=6, tip_length=0.25)
        g = VGroup(arr, T(label, size=28)).arrange(RIGHT, buff=0.25).move_to(rect)
        return VGroup(rect, g).move_to(P3(x, 0.15))
    b1 = button("toward the salt side", True, -2.95)
    b2 = button("toward the plain side", False, 2.95)
    ring_bg = Circle(radius=0.42, color=GREY, stroke_width=4).move_to(P3(0, -1.05))
    arc = always_redraw(lambda: Arc(radius=0.42, start_angle=PI / 2, angle=2 * PI * max(tr.get_value(), 0.001), color=YELLOW, stroke_width=8).move_to(P3(0, -1.05)))
    num = LiveText(lambda: str(int(np.ceil(tr.get_value() * 5 - 1e-6))) if tr.get_value() > 0 else "0", P3(0, -1.05), 30, TEXT)
    return box, q, b1, b2, ring_bg, arc, num


class S06Predict(TankScene):
    def construct(self):
        w = self.stage()
        w.hop(2, "R", 1.5)
        w.hop(13, "L", 2.5)
        w.hop(3, "L", 3.5) if False else None
        tr = ValueTracker(1.0)
        box, q, b1, b2, ring_bg, arc, num = predict_card(tr)
        self.at("So which", lead=0.5)
        self.play(*self.tk.dim_anims(0.5), w.gop.animate.set_value(0.8), FadeIn(box), run_time=0.8)
        self.play(Write(q), run_time=1.4)
        self.at("Toward the side", lead=0.3)
        self.play(FadeIn(b1, shift=UP * 0.15), run_time=0.5)
        self.at("or toward", lead=0.3)
        self.play(FadeIn(b2, shift=UP * 0.15), run_time=0.5)
        self.at("Pause", lead=0.3)
        self.add(num, arc)
        self.play(FadeIn(ring_bg), run_time=0.5)
        self.idle()
        self.finish()


class S07Pause(TankScene):
    def construct(self):
        w = self.stage(dim=0.5, wop=0.8)
        self.tk.out.set_stroke(opacity=0.4)
        self.tk.mem.set_stroke(opacity=0.4)
        self.tk.sch.set_opacity(0.4)
        w.hop(4, "R", 1.0)
        tr = ValueTracker(1.0)
        box, q, b1, b2, ring_bg, arc, num = predict_card(tr)
        self.add(box, q, b1, b2, ring_bg, arc, num)
        self.play(tr.animate.set_value(0.0), run_time=4.8, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Reveal(TankScene):
    def construct(self):
        w = self.stage()
        tal = Tally(w, x=0.0, op=0.0)
        self.add(tal)
        # 5 hops left to right, 3 right to left (water only)
        base = 1.2
        order = [(0, "R", 0.0), (11, "L", 0.7), (1, "R", 1.4), (2, "R", 2.3), (12, "L", 3.0), (3, "R", 3.9), (13, "L", 5.0), (4, "R", 6.0)]
        for i, to, dt_ in order:
            w.hop(i, to, base + dt_ + 0.6)
        self.bounces([2.5, 4.5, 6.5, 8.5, 9.5])
        self.at("On average", lead=0.0)
        self.play(tal.op.animate.set_value(1.0), run_time=0.8)
        self.at("Nothing pulls", lead=0.2)
        cap = T("nothing pulls the water", size=32, color=TEXT).move_to(P3(0, -3.2))
        self.play(FadeIn(cap), run_time=0.7)
        self.at("There is simply", lead=0.2)
        self.play(self.tk.dl.animate.set_value(-0.2), self.tk.dr.animate.set_value(0.2), run_time=3.5)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Osmosis(TankScene):
    def construct(self):
        w = self.stage(dl=-0.2, dr=0.2)
        for k, (i, to, t) in enumerate([(5, "R", 0.8), (14, "L", 1.8), (6, "R", 2.8), (7, "R", 3.8)]):
            w.hop(i, to, t)
        self.bounces([1.5, 3.0, 4.2])
        self.at("called osmosis", lead=0.5)
        r1, r2 = two_part(0.5, -0.6, 30)
        term = chip("osmosis", TEAL, size=44).move_to(P3(0, 2.45))
        dfn = VGroup(T("diffusion of water across a", size=30), T("selectively permeable membrane", size=30)).arrange(DOWN, buff=0.12).move_to(P3(0, 1.4))
        self.play(*self.tk.dim_anims(0.3, 0.1), w.gop.animate.set_value(0.25), Write(term), run_time=1.0)
        self.play(Write(dfn), run_time=1.6)
        self.at("Water moves", lead=0.2)
        self.play(Write(r1), run_time=1.4)
        self.at("That is the side", lead=0.2)
        self.play(Write(r2), run_time=1.6)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class CellScene(SS):
    def stage(self, kind, op_counts=0.0, k=None):
        ambient(self)
        self.bath = bath()
        if kind == "cuke":
            self.cell = Cell(k=1.0 if k is None else k)
            items = cuke_items()
        else:
            self.cell = Cell(k=0.5 if k is None else k)
            items = lettuce_items()
        self.j = Jig(self, self.cell, items)
        self.sch = schem()
        self.cnt = counters_cell(self.j, op_counts)
        self.add(self.bath, *self.cell.parts(), self.j.dots, self.sch, self.cnt)
        return self.j

    def grp(self, g):
        return self.j.sel(lambda it: it["g"] == g)


class S10Cucumber(CellScene):
    def construct(self):
        ambient(self)
        sg = slice_group()
        gt = ValueTracker(1.0)
        sop = ValueTracker(1.0)
        bd = beads(gt)
        sl = salt_on_slice(sop)
        self.add(sg, *bd, *sl)
        # the cell is built behind, invisible
        self.bath = bath(0.0)
        self.cell = Cell(k=1.0)
        self.cell.op.set_value(0.0)
        self.j = Jig(self, self.cell, cuke_items())
        self.sch = schem()
        self.sch.set_opacity(0)
        self.j.vis(lambda it: True, 0.0, False)
        self.add(self.bath, *self.cell.parts(), self.j.dots, self.sch)
        # the zoom
        self.at("Zoom", lead=0.3)
        zoom_grp = VGroup(sg)
        self.play(zoom_grp.animate.scale(4).set_opacity(0), sop.animate.set_value(0), gt.animate.set_value(0),
                  self.bath.animate.set_fill(opacity=0.16), self.cell.op.animate.set_value(1.0), self.sch.animate.set_opacity(1.0), run_time=1.6)
        self.remove(sg, *bd, *sl)
        outw, ins_w, ins_s, outs = self.grp("outw"), self.grp("inw"), self.grp("in"), self.grp("outs")
        spare = self.grp("spare")
        ins = self.j.sel(lambda it: it["g"] == "in" and it["k"] == "s")
        inw = self.j.sel(lambda it: it["g"] == "in" and it["k"] == "w")
        self.play(*self.j.vis(lambda it: it["g"] in ("outw", "spare") or (it["g"] == "in" and it["k"] == "w"), 1.0), run_time=1.0)
        # salt outside: bounce off the membrane
        for k, i in enumerate([n for n, it in enumerate(self.j.items) if it["g"] == "outs"]):
            it = self.j.items[i]
            dx = -0.35 if it["x"] > 0 else 0.35
            if abs(it["x"]) < 4.8:
                self.j.bounce(i, self.t_of("holds") + 0.2 * k + 0.6, dx)
        self.at("Salt sits", lead=0.2)
        self.play(*self.j.vis(lambda it: it["g"] == "outs", 1.0), run_time=1.0)
        self.at("most of it", lead=0.2)
        self.play(self.cell.km.animate.set_value(1.03), run_time=0.4)
        self.play(self.cell.km.animate.set_value(1.0), run_time=0.4)
        self.at("a few", lead=0.0) if False else None
        self.play(*self.j.vis(lambda it: it["g"] == "in" and it["k"] == "s", 1.0), run_time=0.8)
        self.at("The salty liquid", lead=0.2)
        a = T("outside: more dissolved particles", size=30, color=GREY).move_to(P3(0, 3.4))
        self.play(FadeIn(a, shift=DOWN * 0.1), run_time=0.7)
        self.at("so there is", lead=0.2)
        b = T("less water outside", size=30, color=BLUE).move_to(P3(0, -3.4))
        self.play(FadeIn(b, shift=UP * 0.1), run_time=0.7)
        self.idle()
        self.finish()


class S11Cucumber2(CellScene):
    def construct(self):
        j = self.stage("cuke", 0.0)
        out_ids = [n for n, it in enumerate(j.items) if it["k"] == "w" and it["m"] == "vac"][:6]
        spare = [n for n, it in enumerate(j.items) if it["g"] == "spare"]
        outw = [n for n, it in enumerate(j.items) if it["g"] == "outw"]
        times = [0.5, 1.0, 1.6, 2.2, 2.8, 3.3]
        for k, i in enumerate(out_ids):
            tgt = j.items[spare[k]]
            j.go(i, times[k], "fix", tgt["x"], tgt["y"] + 0.0, 1.9, "out")
        for n in spare[:6]:
            pass
        # one dot goes the other way
        j.go(outw[0], 2.0, "vac", 1.9, 0.9, 1.9, "in")
        self.play(self.cnt[0].op.animate.set_value(1.0), self.cnt[1].op.animate.set_value(1.0), run_time=0.5)
        self.at("The vacuole", lead=0.2)
        self.play(self.cell.k.animate.set_value(0.72), self.cell.km.animate.set_value(0.965), run_time=1.6)
        # zoom out to the slice, beads rise
        sg = slice_group()
        gt = ValueTracker(0.0)
        sop = ValueTracker(1.0)
        bd = beads(gt)
        sl = salt_on_slice(sop)
        sop.set_value(0.0)
        self.add(*bd, *sl)
        self.at("water beads", lead=0.5)
        drive(self, gt, 5.7, 7.5, 0.0, 1.0)
        drive(self, sop, 5.3, 6.3, 0.0, 1.0)
        self.play(self.cell.op.animate.set_value(0), self.j.gop.animate.set_value(0), self.cnt[0].op.animate.set_value(0), self.cnt[1].op.animate.set_value(0),
                  self.bath.animate.set_fill(opacity=0), self.sch.animate.set_opacity(0), FadeIn(sg), run_time=1.0)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Lettuce(CellScene):
    def construct(self):
        ambient(self)
        lf = Leaf(0.0)
        label = T("plain water", size=32, color=BLUE).move_to(P3(0, -1.9))
        limp = T("limp leaf", size=32, color=LEAF).move_to(P3(5.3, 1.3))
        self.add(lf.bowl, lf.leaf_l, lf.leaf_r)
        # the cell, built hidden
        self.bath = bath(0.0)
        self.cell = Cell(k=0.5)
        self.cell.op.set_value(0.0)
        self.j = Jig(self, self.cell, lettuce_items())
        self.j.gop.set_value(0.0)
        self.sch = schem()
        self.sch.set_opacity(0)
        self.add(self.bath, *self.cell.parts(), self.j.dots, self.sch)
        self.play(FadeIn(lf.bowl), run_time=0.4)
        self.play(Create(lf.leaf_l), Create(lf.leaf_r), run_time=1.0) if False else None
        drive(self, lf.crisp, 0.0, 12.0, 0.0, 0.0)
        sway = Mobject()
        sway.add_updater(lambda m, dt: lf.crisp.set_value(0.04 + 0.04 * np.sin(1.3 * CLK["t"])))
        self.add(sway)
        self.at("limp", lead=0.2)
        self.play(FadeIn(limp), run_time=0.6)
        self.at("plain water", lead=0.2)
        self.play(FadeIn(label), run_time=0.6)
        outw = self.grp("outw")
        self.at("Its cells", lead=0.4)
        grp = VGroup(lf.bowl, label, limp)
        self.remove(sway)
        self.play(lf.op.animate.set_value(0), FadeOut(grp), self.bath.animate.set_fill(opacity=0.16), self.cell.op.animate.set_value(1.0),
                  self.sch.animate.set_opacity(1.0), self.j.gop.animate.set_value(1.0), run_time=1.0)
        self.remove(lf.bowl, lf.leaf_l, lf.leaf_r)
        # outside salt hidden at first?  keep as built (almost none outside)
        ins = self.j.sel(lambda it: it["g"] == "in" and it["k"] == "s")
        self.at("more dissolved", lead=0.3)
        rt = ValueTracker(0.0)
        rings = [always_redraw(lambda d=d: Circle(radius=0.3, stroke_color=WHITE, stroke_width=4, stroke_opacity=rt.get_value()).move_to(d.get_center())) for d in ins]
        self.add(*rings)
        self.play(rt.animate.set_value(1.0), run_time=0.5)
        self.play(rt.animate.set_value(0.0), run_time=0.7)
        a = T("inside: more dissolved particles", size=30, color=GREY).move_to(P3(0, 3.4))
        self.play(FadeIn(a, shift=DOWN * 0.1), run_time=0.6)
        self.at("less water inside", lead=0.3) if False else self.at("so there is", lead=0.2)
        b = T("less water inside", size=30, color=BLUE).move_to(P3(0, -3.4))
        self.play(FadeIn(b, shift=UP * 0.1), run_time=0.6)
        self.idle()
        self.finish()


class S13Lettuce2(CellScene):
    def construct(self):
        j = self.stage("lettuce", 0.0)
        inw_out = [n for n, it in enumerate(j.items) if it["g"] == "outw"]
        rng = np.random.default_rng(31)
        tg = scatter(rng, 8, (-2.3, 2.3), (-1.2, 1.2), 0.8)
        times = [0.5, 0.9, 1.3, 1.8, 2.6, 3.0, 3.5, 4.0]
        for k, i in enumerate(inw_out[:8]):
            j.go(i, times[k], "vac", tg[k][0], tg[k][1], 1.9, "in")
        self.play(self.cnt[0].op.animate.set_value(1.0), self.cnt[1].op.animate.set_value(1.0), run_time=0.4)
        self.at("The vacuole", lead=0.2)
        self.play(self.cell.k.animate.set_value(1.0), run_time=2.0)
        self.at("presses out", lead=0.3)
        up = Arrow(P3(2.2, 0.9), P3(3.95, 0.9), buff=0, color=GOLD, stroke_width=9, tip_length=0.3)
        ul = T("presses\non wall", size=28, color=GOLD).move_to(P3(5.1, 0.9))
        self.play(GrowArrow(up), FadeIn(ul), run_time=0.9)
        self.at("The wall", lead=0.2)
        dn = Arrow(P3(3.95, -0.9), P3(2.2, -0.9), buff=0, color=TEAL, stroke_width=9, tip_length=0.3)
        dl_ = T("wall presses\nback", size=28, color=TEAL).move_to(P3(5.1, -0.9))
        self.play(GrowArrow(dn), FadeIn(dl_), run_time=0.9)
        # zoom out to the crisp leaf
        lf = Leaf(0.0, op=0.0)
        self.add(lf.bowl, lf.leaf_l, lf.leaf_r)
        lf.bowl.set_fill(opacity=0).set_stroke(opacity=0)
        self.at("The cells firm", lead=0.3)
        cellmobs = [self.bath, self.sch, up, ul, dn, dl_]
        self.play(self.cell.op.animate.set_value(0), self.j.gop.animate.set_value(0), self.cnt[0].op.animate.set_value(0), self.cnt[1].op.animate.set_value(0),
                  *[m.animate.set_opacity(0) for m in cellmobs], lf.op.animate.set_value(1.0),
                  lf.bowl.animate.set_fill(opacity=0.3).set_stroke(opacity=1), run_time=1.0)
        self.at("leaf turns", lead=0.2) if False else None
        self.at("turns crisp", lead=0.5)
        self.play(lf.crisp.animate.set_value(1.0), run_time=1.6)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14Passive(SS):
    def construct(self):
        ambient(self)
        sc = 0.5
        cL, cR = Cell(-3.3, -0.2, sc, k=0.72, km=0.965), Cell(3.3, -0.2, sc, k=1.0)
        cL.op.set_value(0.0)
        cR.op.set_value(0.0)
        rng = np.random.default_rng(14)

        def mini(cell, wcount, scount, outw, outs, sx):
            it = []
            used = []
            for p in scatter(rng, scount, (-2.0, 2.0), (-1.0, 1.0), 0.8):
                it.append(salt("vac", p[0], p[1])); used.append(p)
            for p in scatter(rng, wcount, (-2.2, 2.2), (-1.1, 1.1), 0.75, avoid=used):
                it.append(water("vac", p[0], p[1]))
            pts = scatter(rng, outw + outs, (4.3, 5.9), (-2.0, 2.0), 0.85)
            for k, p in enumerate(pts):
                x = p[0] * (1 if sx > 0 else -1)
                it.append(salt("fix", x, p[1]) if k < outs else water("fix", x, p[1]))
            return Jig(self, cell, it, seed=3 + wcount)
        jL = mini(cL, 6, 3, 0, 5, -1)
        jR = mini(cR, 10, 4, 4, 0, 1)
        nameL = T("cucumber cell", size=28, color=TEXT).move_to(P3(-3.3, -1.7))
        nameR = T("lettuce cell", size=28, color=TEXT).move_to(P3(3.3, -1.7))
        self.add(*cL.parts(), *cR.parts(), jL.dots, jR.dots)
        jL.gop.set_value(0.0)
        jR.gop.set_value(0.0)
        self.play(cL.op.animate.set_value(1.0), cR.op.animate.set_value(1.0), jL.gop.animate.set_value(1.0), jR.gop.animate.set_value(1.0),
                  FadeIn(nameL), FadeIn(nameR), run_time=1.2)
        wo = T("water out", size=36, color=BLUE).move_to(P3(-3.3, 2.1))
        wi = T("water in", size=36, color=BLUE).move_to(P3(3.3, 2.1))
        self.play(FadeIn(wo, shift=UP * 0.1), FadeIn(wi, shift=UP * 0.1), run_time=0.5)
        bL, bR = battery().scale(0.8).move_to(P3(-3.3, -2.4)), battery().scale(0.8).move_to(P3(3.3, -2.4))
        tL = T("no energy spent", size=28, color=GREEN).move_to(P3(-3.3, -3.2))
        tR = T("no energy spent", size=28, color=GREEN).move_to(P3(3.3, -3.2))
        self.at("The cell", lead=0.3) if False else self.at("spent no energy", lead=0.3)
        self.play(FadeIn(bL), FadeIn(bR), FadeIn(tL), FadeIn(tR), run_time=0.8)
        pas = chip("passive transport", TEAL, size=40).move_to(P3(0, 2.05))
        self.at("Osmosis is", lead=0.2)
        self.play(FadeOut(wo), FadeOut(wi), Write(pas), run_time=1.1)
        # first film's tank, then the water tank
        cy, tw, th = 2.05, 7.0, 1.9
        out = Rectangle(width=tw, height=th, stroke_color=GREY, stroke_width=4, fill_color=BLUE, fill_opacity=0.14).move_to(P3(0, cy))
        mem = DashedLine(P3(0, cy - th / 2), P3(0, cy + th / 2), dash_length=0.12, dashed_ratio=0.62, color=WHITE, stroke_width=5)
        wp = World(self, [{"side": s, "color": PUR} for s in S_12_2], cx=0, cy=cy, w=tw, h=th, s=0.5, mt=0.5, amp=0.26)
        wp.gop.set_value(0.0)
        ww = World(self, specs_tank(), cx=0, cy=cy, w=tw, h=th, s=0.5, mt=0.5, amp=0.26, seed=8)
        ww.gop.set_value(0.0)
        wp.hop(2, "R", self.t_of("same random") + 1.0)
        wp.hop(13, "L", self.t_of("same random") + 2.0)
        ww.hop(1, "R", self.t_of("only water") - 0.2) if False else None
        ww.bounce(19, self.t_of("only water") + 0.6)
        ww.bounce(20, self.t_of("only water") + 1.2)
        ww.hop(3, "R", self.t_of("only water") + 0.9)
        self.add(out, mem, wp.dots, ww.dots)
        out.set_fill(opacity=0).set_stroke(opacity=0)
        mem.set_stroke(opacity=0)
        self.at("It is the same", lead=0.2)
        self.play(FadeOut(pas), out.animate.set_fill(opacity=0.14).set_stroke(opacity=1), mem.animate.set_stroke(opacity=1), wp.gop.animate.set_value(1.0), run_time=0.8)
        self.at("In our model", lead=0.2)
        self.play(wp.gop.animate.set_value(0.0), ww.gop.animate.set_value(1.0), run_time=1.0)
        self.idle()
        self.finish()


class S15Rule(TankScene):
    def construct(self):
        w = self.stage(dl=-0.2, dr=0.2)
        for i, to, t in [(5, "R", 0.9), (14, "L", 1.9), (6, "R", 3.0), (7, "R", 3.9)]:
            w.hop(i, to, t)
        self.bounces([2.8, 3.6, 4.4, 5.2])
        r1, r2 = two_part(1.7, 0.55, 28)
        wall = Rectangle(width=0.35, height=3.2, stroke_width=0, fill_color=OLIVE, fill_opacity=1).move_to(P3(6.0, 0.4))
        arr = Arrow(P3(5.75, -0.45), P3(4.1, -0.45), buff=0, color=OLIVE, stroke_width=10, tip_length=0.3)
        lab = T("pushback can stop the drift", size=30, color=OLIVE).move_to(P3(3.1, -1.2))
        self.at("When the membrane", lead=0.3) if False else None
        self.at("water drifts toward", lead=0.5)
        self.play(*self.tk.dim_anims(0.3, 0.1), w.gop.animate.set_value(0.25), Write(r1), run_time=1.4)
        self.at("more dissolved", lead=0.3)
        self.play(Write(r2), run_time=1.4)
        self.at("pushback", lead=0.3)
        self.play(FadeIn(wall, shift=LEFT * 0.2), run_time=0.7)
        self.play(GrowArrow(arr), FadeIn(lab), run_time=0.9)
        self.idle()
        self.finish()


class S16End(EndCard):
    LINE = "Water drifts toward more dissolved particles, unless something pushes back."
