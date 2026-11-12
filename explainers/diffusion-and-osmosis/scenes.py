"""Random Moves, One-Way Drift (diffusion-and-osmosis, film 1)

COLOUR MAP (both films): membrane = WHITE dashed line; dye = PURPLE dots; water = BLUE dots;
salt = GREY squares; oxygen = GREEN dots; carbon dioxide = RED dots; tallies = WHITE arrows.
Every tank and cell is a cartoon labelled 'schematic'. One world through the film: a tank split by a line
at x = 0, with dots that random-walk (sine wobble) and hop across the line in timed routes.
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
    def __init__(self, scene, specs, cx=0.0, cy=CY, w=TW, h=TH, amp=0.26, seed=11, flash=True, s=1.0):
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
        self.dots.add_updater(self._tick)

    def _slots(self, rng, n, sgn):
        s, cx, cy, w, h = self.s, self.cx, self.cy, self.w, self.h
        if sgn < 0:
            x0, x1 = cx - w / 2 + 0.45 * s, cx - 0.95 * s
        else:
            x0, x1 = cx + 0.95 * s, cx + w / 2 - 0.45 * s
        y0, y1 = cy - h / 2 + 0.42 * s, cy + h / 2 - 0.42 * s
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


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Diffusion and Osmosis"
    TITLE = "Random Moves, One-Way Drift"


# ---------------------------------------------------------------------------------------------
class S01Hook(SS):
    """A drop of dye blooms in a glass, the film runs backwards, and does not gather back."""

    def construct(self):
        gx, W, H, wy = -0.8, 5.4, 5.2, -0.1
        F, n = 420, 56
        rng = np.random.default_rng(3)
        traj = np.zeros((F, n, 2))
        p = np.stack([rng.normal(0, 0.1, n), (H / 2 - 0.45) + rng.normal(0, 0.1, n)], 1)
        for f in range(F):
            p = p + rng.normal(0, 0.15, (n, 2))
            p[:, 0] = np.where(p[:, 0] > W / 2 - 0.1, W - 0.2 - p[:, 0], p[:, 0])
            p[:, 0] = np.where(p[:, 0] < -W / 2 + 0.1, -W + 0.2 - p[:, 0], p[:, 0])
            p[:, 1] = np.where(p[:, 1] > H / 2 - 0.1, H - 0.2 - p[:, 1], p[:, 1])
            p[:, 1] = np.where(p[:, 1] < -H / 2 + 0.1, -H + 0.2 - p[:, 1], p[:, 1])
            traj[f] = p
        origin = np.array([gx, wy])
        water = Rectangle(width=W, height=H, stroke_width=0, fill_color=BLUE, fill_opacity=0.12).move_to(P3(gx, wy))
        tint = Rectangle(width=W, height=H, stroke_width=0, fill_color=PUR, fill_opacity=0.0).move_to(P3(gx, wy))
        glass = VMobject(color=GREY, stroke_width=7)
        glass.set_points_as_corners([P3(gx - W / 2, wy + H / 2 + 0.4), P3(gx - W / 2, wy - H / 2), P3(gx + W / 2, wy - H / 2), P3(gx + W / 2, wy + H / 2 + 0.4)])
        dots = VGroup(*[Dot(radius=0.085, color=PUR).set_stroke(width=0) for _ in range(n)])
        dots.set_opacity(0)
        ctl = {"f": 0.0, "rate": 0.0}

        def upd(g, dt):
            ctl["f"] = float(np.clip(ctl["f"] + ctl["rate"] * 15 * dt, 0, F - 1))
            f = int(ctl["f"])
            for i, d in enumerate(g):
                d.move_to(P3(*(traj[f, i] + origin)))
            tint.set_fill(PUR, opacity=min(0.3, f / 130 * 0.3))
        dots.add_updater(upd)
        ring = Circle(radius=0.2, color=WHITE, stroke_width=5)
        trail = VMobject(color=WHITE, stroke_width=4)
        show = ValueTracker(0.0)

        def tr(m, dt):
            o = show.get_value()
            f = int(ctl["f"])
            pts = [P3(*(traj[k, 0] + origin)) for k in range(max(0, f - 70), f + 2)]
            trail.set_points_as_corners(pts)
            trail.set_stroke(opacity=0.9 * o)
            ring.move_to(pts[-1])
            ring.set_stroke(opacity=o)
        trail.add_updater(tr)
        drop = Dot(radius=0.24, color=PUR).move_to(P3(gx, 3.5))
        self.add(water, tint, glass, dots, drop)
        self.play(drop.animate.move_to(P3(gx, wy + H / 2 - 0.45)), run_time=0.8, rate_func=rate_functions.ease_in_quad)
        self.remove(drop)
        dots.set_opacity(1)
        ctl["rate"] = 1.0
        self.add(trail, ring)
        self.at("None of them", lead=0.5)
        self.play(show.animate.set_value(1), run_time=0.5)
        self.at("So why")
        self.play(show.animate.set_value(0), run_time=0.5)
        self.at("almost never", lead=0.3)
        ctl["rate"] = -4.5
        x = VGroup(Line(P3(gx - 1.7, wy + 1.7), P3(gx + 1.7, wy - 1.7)), Line(P3(gx - 1.7, wy - 1.7), P3(gx + 1.7, wy + 1.7)))
        x.set_stroke(RED, 14)
        self.at("gather back", lead=0.0)
        self.play(Create(x[0]), Create(x[1]), run_time=0.5)
        q = chip("why only\none way?", TEAL, size=36)
        q.move_to(P3(4.95, 0.2))
        self.at("into a drop", lead=0.0)
        self.play(FadeIn(q, shift=LEFT * 0.2), run_time=0.5)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Tank(SS):
    def construct(self):
        base = tank_base()
        sch = schem()
        self.play(GrowFromPoint(base[1], point=P3(-0.8, 0)), FadeIn(base[0]), run_time=1.4)
        w = World(self, specs_12_2())
        w.dots.set_opacity(0)
        self.add(w.dots)
        self.play(w.dots.animate.set_opacity(1), FadeIn(sch), run_time=0.8)
        self.at("split down the middle", lead=0.1)
        line = open_line()
        self.play(Create(line), run_time=1.3)
        cl = LiveText(lambda: f"left: {w.pop('L')}", P3(-4.6, 3.3), 34, TEXT, 0.0)
        cr = LiveText(lambda: f"right: {w.pop('R')}", P3(4.6, 3.3), 34, TEXT, 0.0)
        self.add(cl, cr)
        self.at("start on the left", lead=0.5)
        self.play(cl.op.animate.set_value(1), run_time=0.6)
        self.at("Only a few", lead=0.0)
        self.play(cr.op.animate.set_value(1), run_time=0.6)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class World0(SS):
    """Base for scenes that start from the 12:2 tank with the open line."""
    def stage(self, op=1.0, line=True):
        self.base = tank_base()
        self.line = open_line()
        self.w = World(self, specs_12_2())
        self.hud = counters(self.w, op=op)
        self.sch = schem()
        self.add(self.base, self.line, self.w.dots, self.hud, self.sch)
        return self.w


class S03Hops(World0):
    def construct(self):
        w = self.stage()
        # one dot leaves a path behind it: "its own path"
        pts = []
        trail = VMobject(color=WHITE, stroke_width=4)
        ring = Circle(radius=0.22, color=WHITE, stroke_width=4)
        d2 = w.dots[2]
        on = ValueTracker(0.0)

        def tr(m, dt):
            pts.append(d2.get_center().copy())
            del pts[:-90]
            if len(pts) > 1:
                trail.set_points_as_corners(pts)
            o = on.get_value()
            trail.set_stroke(opacity=0.9 * o)
            ring.move_to(d2.get_center())
            ring.set_stroke(opacity=o)
        trail.add_updater(tr)
        self.add(trail, ring)
        # hops, timed to the sentences
        w.hop(4, "R", self.t_of("hop across") + 0.1)
        w.hop(12, "L", self.t_of("either way") + 0.2)
        w.hop(12, "R", self.t_of("where the crowd") + 1.9)
        w.hop(4, "L", self.t_of("nothing pushes") + 0.6)
        self.at("jiggles", lead=0.0)
        self.play(on.animate.set_value(1), run_time=0.5)
        self.at("Any dot", lead=0.2)
        self.play(on.animate.set_value(0), run_time=0.5)
        cap = caption("any dot at the line can hop, either way")
        self.play(FadeIn(cap), run_time=0.6)
        self.idle()
        self.finish()


class S04Predict(World0):
    @staticmethod
    def card(tr):
        box = RoundedRectangle(corner_radius=0.3, width=11.2, height=3.9, stroke_color=TEAL, stroke_width=4,
                               fill_color=BG, fill_opacity=0.8).move_to(P3(0, 0.3))
        q = VGroup(T("Over many seconds, which way", size=36), T("will MORE dots cross on average?", size=36)).arrange(DOWN, buff=0.15).move_to(P3(0, 1.2))
        btn = lambda txt, right: RoundedRectangle(corner_radius=0.2, width=3.5, height=1.0, stroke_color=TEAL, stroke_width=3,
                                                  fill_color=TEAL, fill_opacity=0.15)
        def button(label, rightward):
            rect = btn(label, rightward)
            arr = Arrow(LEFT * 0.35, RIGHT * 0.35, buff=0, color=WHITE, stroke_width=6, tip_length=0.25) if rightward else Arrow(RIGHT * 0.35, LEFT * 0.35, buff=0, color=WHITE, stroke_width=6, tip_length=0.25)
            lab = T(label, size=28)
            g = VGroup(arr, lab).arrange(RIGHT, buff=0.25).move_to(rect)
            return VGroup(rect, g)
        b1 = button("left to right", True).move_to(P3(-3.55, -0.75))
        b2 = button("right to left", False).move_to(P3(3.55, -0.75))
        ring_bg = Circle(radius=0.55, color=GREY, stroke_width=4).move_to(P3(0, -0.75))
        arc = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=2 * PI * max(tr.get_value(), 0.001), color=YELLOW, stroke_width=8).move_to(P3(0, -0.75)))
        num = LiveText(lambda: str(int(np.ceil(tr.get_value() * 5 - 1e-6))) if tr.get_value() > 0 else "0", P3(0, -0.75), 34, TEXT)
        return box, q, b1, b2, ring_bg, arc, num

    def construct(self):
        w = self.stage()
        tr = ValueTracker(1.0)
        box, q, b1, b2, ring_bg, arc, num = self.card(tr)
        self.play(*dim_anim(self.base, self.line, self.sch), w.dots.animate.set_opacity(0.55),
                  self.hud[0].op.animate.set_value(0.3), self.hud[1].op.animate.set_value(0.3), run_time=0.7)
        self.add(box)
        self.play(FadeIn(box), run_time=0.4)
        self.at("which way", lead=0.5)
        self.play(Write(q), run_time=1.6)
        self.at("From left to right", lead=0.3)
        self.play(FadeIn(b1, shift=UP * 0.15), run_time=0.5)
        self.at("or from right", lead=0.3)
        self.play(FadeIn(b2, shift=UP * 0.15), run_time=0.5)
        self.at("Pause and decide", lead=0.3)
        self.add(num)
        self.add(arc)
        self.play(FadeIn(ring_bg), run_time=0.5)
        self.idle()
        self.finish()


class S05Pause(World0):
    def construct(self):
        w = self.stage(op=0.3)
        self.base[0].set_fill(opacity=0.05)
        self.base[1].set_stroke(opacity=0.4)
        self.line.set_stroke(opacity=0.4)
        self.sch.set_opacity(0.4)
        w.dots.set_opacity(0.55)
        tr = ValueTracker(1.0)
        box, q, b1, b2, ring_bg, arc, num = S04Predict.card(tr)
        self.add(box, q, b1, b2, ring_bg, arc, num)
        self.play(tr.animate.set_value(0.0), run_time=4.8, rate_func=linear)
        self.finish()


class S06Reveal(World0):
    def construct(self):
        w = self.stage()
        tal = Tally(w, x=0.0)
        self.add(tal)
        for i, ph in ((9, "from left to right"), (10, "No dot chose"), (11, "more dots on")):
            pass
        w.hop(9, "R", self.t_of("left to right") + 0.2)
        w.hop(10, "R", self.t_of("chose that") + 0.3)
        w.hop(11, "R", self.t_of("to make the hop") + 0.2)
        w.hop(12, "L", self.t_of("hop back") + 0.4)
        cap = caption("on average")
        self.at("On average", lead=0.0)
        self.play(tal.op.animate.set_value(1), FadeIn(cap), run_time=0.8)
        self.at("There are simply", lead=0.2)
        hl = Rectangle(width=6.1, height=TH - 0.1, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.08).move_to(P3(-3.1, CY))
        self.play(FadeIn(hl), run_time=0.6)
        self.at("hop back", lead=1.0)
        self.play(FadeOut(hl), run_time=0.6)
        self.idle()
        self.finish()


class S07Concentration(SS):
    def construct(self):
        base = tank_base()
        line = open_line()
        w = World(self, specs_from_left(LEFT_AFTER_6))
        sch = schem()
        bars = Bars(w, op=0.0)
        self.add(base, line, w.dots, sch, bars)
        hl = Rectangle(width=6.1, height=TH - 0.1, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.08).move_to(P3(-3.1, CY))
        self.at("crowded", lead=0.0)
        self.play(FadeIn(hl), run_time=0.6)
        self.at("has a name", lead=0.0)
        self.play(FadeOut(hl), run_time=0.6)
        term = chip("concentration", TEAL, size=40).move_to(P3(0, 3.28))
        self.at("Concentration", lead=0.2)
        self.play(Write(term), run_time=1.2)
        self.at("how much of a substance", lead=0.2)
        d = caption("how much of a substance is in a given space", y=-3.5, size=28)
        self.play(Write(d), run_time=2.4)
        self.at("At the start", lead=0.2)
        self.play(bars.op.animate.set_value(1), run_time=0.8)
        self.at("more concentrated", lead=0.2)
        a = T("more concentrated", size=30, color=PUR).move_to(P3(-3.1, -3.0))
        self.play(FadeIn(a), run_time=0.5)
        b = T("less concentrated", size=30, color=PUR).move_to(P3(3.1, -3.0))
        self.wait(self.room(1.3))
        self.play(FadeIn(b), run_time=0.5)
        self.idle()
        self.finish()

    def room(self, a):
        return a


class S08Diffusion(SS):
    def construct(self):
        base = tank_base()
        line = open_line()
        w = World(self, specs_from_left(LEFT_AFTER_6))
        hud = counters(w)
        sch = schem()
        bars = Bars(w)
        self.add(base, line, w.dots, sch, hud, bars)
        # a neutral pair swap keeps the tallies of the hops visible without changing the counts
        w.hop(0, "R", 1.3)
        w.hop(13, "L", 1.3)
        w.hop(8, "R", self.t_of("crowd thins") + 0.0)
        w.hop(7, "R", self.t_of("grows on") + 0.2)
        w.hop(6, "R", self.t_of("grows on") + 1.7)
        w.hop(0, "L", 8.2)
        w.hop(13, "R", 8.2)
        arrow = Arrow(P3(-5.2, -3.0), P3(5.2, -3.0), buff=0, color=PUR, stroke_width=16, tip_length=0.5,
                      max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=30)
        arrow.set_opacity(0)
        self.add(arrow)
        keep = {"on": False}
        arrow.add_updater(lambda m: m.set_opacity(0.35 + 0.65 * abs(w.pop("L") - w.pop("R")) / 14 * 1.0) if keep["on"] else None)
        self.at("This drift", lead=0.2)
        keep["on"] = True
        self.play(GrowArrow(arrow), run_time=1.4)
        a = T("more concentrated", size=30, color=PUR).move_to(P3(-3.4, -3.52))
        b = T("less concentrated", size=30, color=PUR).move_to(P3(3.4, -3.52))
        self.at("more concentrated", lead=0.2)
        self.play(FadeIn(a), run_time=0.5)
        self.at("less concentrated", lead=0.2)
        self.play(FadeIn(b), run_time=0.5)
        self.at("called diffusion", lead=0.2)
        dv = chip("diffusion", TEAL, size=34).move_to(P3(0, -3.52))
        self.play(Write(dv), run_time=0.9)
        self.idle()
        self.finish()


class S09Even(SS):
    def construct(self):
        base = tank_base()
        line = open_line()
        w = World(self, specs_from_left(LEFT_S9))
        hud = counters(w)
        tal = Tally(w, x=0.0, op=0.0)
        sch = schem()
        bars = Bars(w)
        self.add(base, line, w.dots, sch, hud, bars, tal)
        # window A: -> 2, <- 3 (7:7 -> 8:6); window B: -> 3, <- 2 (8:6 -> 7:7)
        tA = self.t_of("Dots still cross")
        w.hop(0, "R", tA + 0.6)
        w.hop(6, "L", tA + 0.9)
        w.hop(7, "L", tA + 1.7)
        w.hop(1, "R", tA + 2.0)
        w.hop(8, "L", tA + 2.4)
        tB = self.t_of("just as many") + 1.2
        w.hop(2, "R", tB)
        w.hop(0, "L", tB + 0.2)
        w.hop(3, "R", tB + 0.9)
        w.hop(1, "L", tB + 1.2)
        w.hop(4, "R", tB + 2.0)
        cap = caption("still moving, no change overall")
        self.at("Dots still cross", lead=0.3)
        self.play(tal.op.animate.set_value(1), run_time=0.6)
        self.at("just as many", lead=0.0)
        # reset the window tallies between the two windows
        self.wait(max(0.01, tB - 0.7 - self.elapsed()))
        w.cross["lr"] = 0
        w.cross["rl"] = 0
        self.at("The color stops", lead=0.3)
        self.play(FadeIn(cap), run_time=0.6)
        self.idle()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10Membrane(SS):
    def construct(self):
        base = tank_base()
        line = open_line()
        w = World(self, specs_from_left(LEFT_S9))
        sch = schem()
        self.add(base, line, w.dots, sch)
        self.at("swap", lead=0.2)
        mem = membrane()
        self.play(Transform(line, mem), run_time=1.1)
        cell = cell_fill()
        self.at("cell membrane", lead=0.3)
        lab = T("cell membrane", size=30, color=WHITE).move_to(P3(0, 3.42))
        self.play(FadeIn(cell), FadeIn(lab), run_time=1.2)
        # purple dots give way to the oxygen picture: crowded blood, few in the cell
        g = World(self, specs_12_2(GREEN))
        g.dots.set_opacity(0)
        self.add(g.dots)
        self.at("On one side", lead=0.0)
        self.play(w.dots.animate.set_opacity(0), g.dots.animate.set_opacity(1), run_time=1.2)
        self.remove(w.dots)
        self.at("the blood", lead=0.3)
        blood = T("blood", size=34, color=WHITE).move_to(P3(-3.1, 3.42))
        self.play(FadeIn(blood), run_time=0.5)
        self.at("crowded with oxygen", lead=0.2)
        ox = T("oxygen", size=30, color=GREEN).move_to(P3(-3.1, -3.05))
        self.play(FadeIn(ox), run_time=0.5)
        self.at("muscle cell", lead=0.3)
        mc = T("muscle cell", size=34, color=PINK).move_to(P3(3.1, 3.42))
        self.play(FadeIn(mc), run_time=0.5)
        self.idle()
        self.finish()


class Cellular(SS):
    def stage(self, specs, color=GREEN, op=1.0):
        self.base = tank_base()
        self.mem = membrane()
        self.cell = cell_fill()
        self.sch = schem()
        self.blood = T("blood", size=34, color=WHITE).move_to(P3(-5.3, 3.42))
        self.mc = T("muscle cell", size=34, color=PINK).move_to(P3(5.0, 3.42))
        self.w = World(self, specs)
        self.add(self.base, self.cell, self.mem, self.w.dots, self.sch, self.blood, self.mc)
        return self.w


class S11Oxygen(Cellular):
    def construct(self):
        w = self.stage(specs_12_2(GREEN))
        tal = Tally(w, x=0.0)
        self.add(tal)
        leg = T("oxygen", size=32, color=GREEN).move_to(P3(0, -3.05))
        self.add(leg)
        w.hop(9, "R", self.t_of("carry more") + 0.4)
        w.hop(10, "R", self.t_of("into the cell") + 0.1)
        w.hop(11, "R", self.t_of("than out") + 0.2)
        w.hop(13, "L", self.t_of("out of it") + 0.2)
        self.at("same random hops", lead=0.3)
        self.play(tal.op.animate.set_value(1), run_time=0.6)
        self.at("Carbon dioxide", lead=0.3)
        # carbon dioxide: crowded inside the cell
        self.play(w.dots.animate.set_opacity(0), tal.op.animate.set_value(0), run_time=0.8)
        self.remove(w.dots, tal)
        w2 = World(self, [{"side": "L" if i < 3 else "R", "color": RED} for i in range(14)], seed=5)
        w2.dots.set_opacity(0)
        tal2 = Tally(w2, x=0.0)
        self.add(w2.dots, tal2)
        leg2 = T("carbon dioxide", size=32, color=RED).move_to(P3(0, -3.05))
        self.play(w2.dots.animate.set_opacity(1), tal2.op.animate.set_value(1), Transform(leg, leg2), run_time=0.9)
        w2.hop(5, "L", self.t_of("drifts out") + 0.2)
        w2.hop(6, "L", self.t_of("drifts out") + 0.9)
        w2.hop(7, "L", self.t_of("the other way") + 0.3)
        w2.hop(1, "R", self.t_of("the other way") + 0.9)
        self.idle()
        self.finish()


class S12Passive(Cellular):
    def construct(self):
        w = self.stage(specs_from_left(set(range(10)), GREEN))
        w.hop(9, "R", 2.6)
        w.hop(8, "R", 5.2)
        w.hop(11, "L", 7.0)
        body = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.8, stroke_color=WHITE, stroke_width=5)
        tip = Rectangle(width=0.14, height=0.36, fill_color=WHITE, fill_opacity=1, stroke_width=0).next_to(body, RIGHT, buff=0)
        cells = VGroup(*[Rectangle(width=0.28, height=0.56, fill_color=GREEN, fill_opacity=1, stroke_width=0) for _ in range(4)]).arrange(RIGHT, buff=0.08).move_to(body)
        batt = VGroup(body, tip, cells)
        lab = T("no energy spent", size=32, color=GREEN)
        row = VGroup(batt, lab).arrange(RIGHT, buff=0.35).move_to(P3(0, 3.42))
        self.remove(self.blood, self.mc)
        self.at("The cell spent", lead=0.3)
        self.play(FadeIn(batt), run_time=0.7)
        self.at("no energy", lead=0.2)
        self.play(FadeIn(lab), run_time=0.6)
        self.at("needs no energy", lead=0.3)
        d = caption("needs no energy from the cell", y=-3.62, size=28)
        self.play(FadeIn(d), run_time=0.7)
        self.at("passive transport", lead=0.3)
        term = chip("passive transport", TEAL, size=30).move_to(P3(0, -2.85))
        self.play(Write(term), run_time=1.1)
        self.idle()
        self.finish()


class S13Rule(SS):
    def construct(self):
        cyy, hh, ww = 0.55, 3.8, 6.0
        cxl, cxr = -3.4, 3.4
        specL = specs_from_left(LEFT_AFTER_6, PUR)
        specR = specs_from_left(LEFT_AFTER_6, GREEN)
        wl = World(self, specL, cx=cxl, cy=cyy, w=ww, h=hh, amp=0.26, seed=21, s=0.85)
        wr = World(self, specR, cx=cxr, cy=cyy, w=ww, h=hh, amp=0.26, seed=22, s=0.85)
        tl = tank_base(cxl, cyy, ww, hh)
        tr_ = tank_base(cxr, cyy, ww, hh)
        ll = open_line(cxl, cyy, hh)
        cr = cell_fill(cxr, cyy, ww, hh)
        mr = membrane(cxr, cyy, hh)
        sch = schem(5.6, -3.5)
        tal_l = Tally(wl, x=cxl, y=3.0, gap=1.2, size=32)
        tal_r = Tally(wr, x=cxr, y=3.0, gap=1.2, size=32)
        self.add(tl, tr_, ll, cr, mr, wl.dots, wr.dots, sch, tal_l, tal_r)
        self.remove(tl, tr_, ll, cr, mr, sch)
        wl.dots.set_opacity(0)
        wr.dots.set_opacity(0)
        self.play(FadeIn(tl), FadeIn(tr_), FadeIn(ll), FadeIn(cr), FadeIn(mr), FadeIn(sch),
                  wl.dots.animate.set_opacity(1), wr.dots.animate.set_opacity(1), run_time=1.0)
        base_t = self.t_of("on average") + 0.6
        for wk in (wl, wr):
            wk.hop(7, "R", base_t)
            wk.hop(8, "R", base_t + 0.8)
            wk.hop(6, "R", base_t + 1.6)
            wk.hop(13, "L", base_t + 2.3)
        self.at("on average", lead=0.3)
        self.play(tal_l.op.animate.set_value(1), tal_r.op.animate.set_value(1), run_time=0.6)
        self.at("That makes", lead=0.2)
        arr = Arrow(P3(-5.4, -2.0), P3(5.4, -2.0), buff=0, color=PUR, stroke_width=16, tip_length=0.5,
                    max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=30)
        self.play(GrowArrow(arr), run_time=1.3)
        lab = T("more crowded → less crowded", size=36).move_to(P3(0, -2.85))
        self.at("one -way drift", lead=0.1) if False else self.at("drift", lead=0.3)
        self.play(FadeIn(lab), run_time=0.8)
        self.idle()
        self.finish()


class S14Tease(SS):
    def construct(self):
        base = tank_base()
        mem = membrane()
        specs = [{"side": "R", "color": GREY, "shape": "square", "r": 0.15} for _ in range(8)]
        specs += [{"side": "L", "color": BLUE, "r": 0.11} for _ in range(5)] + [{"side": "R", "color": BLUE, "r": 0.11} for _ in range(4)]
        w = World(self, specs, flash=False, seed=31)
        sch = schem()
        w.dots[8:].set_opacity(0)
        self.add(base, mem, w.dots, sch)
        w.bounce(0, 3.6)
        w.bounce(1, 8.0)
        salt = T("salt", size=34, color=GREY).move_to(P3(3.1, 3.42))
        self.at("crowded particle", lead=0.2)
        self.play(FadeIn(salt), run_time=0.5)
        qm = T("?", size=90, color=TEXT).move_to(P3(0, 3.1))
        self.at("will not let", lead=0.2)
        self.play(FadeIn(qm, scale=1.4), run_time=0.6)
        self.at("what if water", lead=0.3)
        wl = T("water", size=34, color=BLUE).move_to(P3(-3.1, 3.42))
        self.play(w.dots[8:].animate.set_opacity(1), FadeIn(wl), run_time=0.9)
        self.idle()
        self.finish()


class S15End(EndCard):
    LINE = "Random moves make a one-way drift, no push needed."
