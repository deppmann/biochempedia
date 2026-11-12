"""Animal body plans, film 2: One segment, constant volume (Biochemistrypedia explainer)

COLOUR MAP (identical to film 1)
  BLUE   = outer layer (skin)            ORANGE = muscle, septa, muscular wall
  YELLOW = gut lining   WHITE = gut lumen   CYAN = coelomic fluid (pale)
  PINK   = the earthworm's body outside, rings in the ground colour
Head is at the LEFT (mouth left, anus right), as in film 1. Everything is a schematic cartoon.
Constant volume is computed: length = V / radius^2 for every segment shape on screen.
"""
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
CYAN = "#BDEFF4"
WHITE_ = "#FFFFFF"
PINK = "#E88FA0"
CREAM = "#EADFC2"
TAN = "#D9C7A0"
SOIL = "#6B4A30"
GRAIN = ["#8F6B47", "#7A5B3E", "#A07C55"]
BRISTLE = "#D8B48A"
FOOD = "#A9743B"

CY = 0.2
R0 = 1.35            # resting radius (unit scale)
V0 = 3.2 * R0 ** 2   # volume, fixed: L = V0 / r^2


def Pt(xs, ys):
    return np.column_stack([xs, ys, np.zeros_like(xs)])


def PL(*pts, color=TEXT, w=6):
    return VMobject(color=color, stroke_width=w).set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])


def svlab(x=0, y=CY):
    t = T("same\nvolume", 30, color=WHITE_, weight=BOLD)
    bg = RoundedRectangle(corner_radius=0.15, width=t.width + 0.3, height=t.height + 0.25, stroke_width=0,
                          fill_color=BG, fill_opacity=0.8)
    return VGroup(bg, t).move_to([x, y, 0]).set_z_index(20)


def lab(txt, x, y, color=TEXT, size=30, weight=NORMAL):
    return T(txt, size, color=color, weight=weight).move_to([x, y, 0])


def swap(g, parts):
    """Replace a group's children. Manim's renderer keeps drawing the children a play() started with,
    so the discarded ones are made invisible or they would stay on screen as ghosts."""
    for p in g.submobjects:
        p.set_opacity(0)
    g.submobjects = []
    g.add(*parts)


# ------------------------------------------------------------------ ambient motes (as film 1)
class Sc(SpokenScene):
    def setup(self):
        super().setup()
        import random
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        motes = VGroup()
        for _ in range(34):
            d = Dot(radius=rng.uniform(0.04, 0.08), color=rng.choice([TEAL, TEXT, GOLD])).set_opacity(rng.uniform(0.25, 0.5))
            d.move_to([rng.uniform(-6.6, 6.6), rng.uniform(-3.7, 3.7), 0])
            d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.15, 0.4))

            def drift(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 3.8:
                    m.shift(DOWN * 7.6)
                if abs(m.get_x()) > 6.8:
                    m.shift(LEFT * 13.6 * (1 if m.get_x() > 0 else -1))
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)


# ------------------------------------------------------------------ the earthworm (film 1 look)
def make_worm(y, x0=-3.6, x1=4.6, amp=0.3, ph0=0.0, speed=1.8):
    N = 70
    u = np.linspace(0, 1, N)
    body = VMobject(color=PINK, stroke_width=50).set_cap_style(CapStyleType.ROUND)
    gutl = VMobject(color=WHITE_, stroke_width=7).set_z_index(3)
    rings = VGroup(*[Line(ORIGIN, UP, color=BG, stroke_width=3) for _ in range(14)])
    g = VGroup(body, gutl, rings)
    g.t = ph0

    def path(t):
        env = np.sin(np.pi * u)
        return np.stack([x0 + (x1 - x0) * u, y + amp * 0.8 * env * np.sin(2 * np.pi * 1.4 * u - t), 0 * u], 1)

    def upd(m, dt):
        m.t += dt * speed
        P = path(m.t)
        body.set_points_smoothly(P)
        gutl.set_points_smoothly(P)
        for i, r in enumerate(rings):
            j = int((i + 1) / (len(rings) + 1) * (N - 1))
            tg = P[min(j + 1, N - 1)] - P[max(j - 1, 0)]
            nv = np.array([-tg[1], tg[0], 0])
            nv = nv / (np.linalg.norm(nv) + 1e-9) * 0.2
            r.put_start_and_end_on(P[j] - nv, P[j] + nv)
    g.add_updater(upd)
    upd(g, 0)
    return g


def grains(x0, x1, y0, y1, n, seed=1):
    import random
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.08, 0.2), color=rng.choice(GRAIN)).set_opacity(0.9)
        d.move_to([rng.uniform(x0, x1), rng.uniform(y0, y1), 0]).set_z_index(-3)
        g.add(d)
    return g


def critter(name):
    c = VGroup()
    if name == "nem":
        xs = np.linspace(-.3, .3, 20)
        c.add(VMobject(color=CREAM, stroke_width=6).set_points_smoothly([[x, .08 * np.sin(x * 14), 0] for x in xs]))
    elif name == "earth":
        c.add(Line([-.3, 0, 0], [.3, 0, 0], color=PINK, stroke_width=14).set_cap_style(CapStyleType.ROUND))
        for x in np.linspace(-.2, .2, 4):
            c.add(Line([x, -.07, 0], [x, .07, 0], color=BG, stroke_width=2))
    else:
        c.add(Ellipse(width=.6, height=.24, color=TAN, fill_opacity=1, stroke_width=0))
        c.add(Dot(radius=.025, color=BG).move_to([.18, .05, 0]), Dot(radius=.025, color=BG).move_to([.18, -.05, 0]))
    return c


# ------------------------------------------------------------------ the segment (side-view cutaway)
class Seg(VGroup):
    """One segment, side view. Radius r is the only shape variable; length = V0 / r^2 (constant volume).
    Trackers fade each part in: fl fluid, wall skin+muscle wall, sept septa, hoop (count of rings),
    lng (strips drawn), gut, ext (strips run into neighbours), nb (faint neighbours), setae, glow, osc."""

    def __init__(self, cx=0.0, cy=CY, sc=1.2, r=R0, live=True):
        super().__init__()
        self.cx, self.cy, self.sc = cx, cy, sc
        self.r = ValueTracker(r)
        for n, v in dict(pinch=0, fl=0, wall=0, hoop=0, lng=0, sept=0, gut=0, ext=0, nb=0, setae=0, glow=0,
                         osc=0, gutw=1, wallw=1).items():
            setattr(self, n, ValueTracker(v))
        self.dr, self.guty, self.t, self.auto_setae, self.reach = 0.0, 0.0, 0.0, 0.0, 0.0
        if live:
            self.add_updater(lambda m, dt: m.rebuild(dt))
        self.rebuild(0)

    def rr(self):
        return max(0.35, self.r.get_value() + self.dr + self.osc.get_value() * np.sin(self.t * 1.7))

    def dims(self):
        r = self.rr()
        return r * self.sc, V0 / r ** 2 * self.sc

    def hx(self, x, R, L, p):
        u = np.clip(x / (L / 2), -1, 1)
        env = (1 - np.abs(u) ** 8) ** 0.25
        bell = np.exp(-(x / (0.28 * L)) ** 2)
        return R * (1 - p * bell) * env

    def rebuild(self, dt=0.0):
        self.t += dt
        R, L = self.dims()
        p, cx, cy, sc = self.pinch.get_value(), self.cx, self.cy, self.sc
        ws = 0.6 + 0.4 * sc
        gl = self.glow.get_value()
        hot = interpolate_color(ManimColor(ORANGE), ManimColor(WHITE_), 0.55 * gl)
        parts = []
        nb = self.nb.get_value()
        if nb > 0.01:
            for sg in (-1, 1):
                edge = cx + sg * (L / 2 + 0.14)
                width = min(2.4, abs(sg * 6.5 - edge))
                if width > 0.3:
                    rr = RoundedRectangle(corner_radius=0.35, width=width, height=2 * R0 * sc * 0.9, stroke_color=BLUE,
                                          stroke_width=4, stroke_opacity=0.4 * nb, fill_color=CYAN, fill_opacity=0.1 * nb)
                    rr.move_to([edge + sg * width / 2, cy, 0])
                    parts.append(rr)
        xs = np.linspace(-L / 2, L / 2, 60)
        h = self.hx(xs, R, L, p)
        top = Pt(cx + xs, cy + h)
        bot = Pt(cx + xs[::-1], cy - h[::-1])
        pts = np.vstack([top, bot, top[:1]])
        fl = self.fl.get_value()
        fluid = VMobject().set_points_as_corners(pts).set_fill(CYAN, opacity=0.5 * fl).set_stroke(width=0)
        parts.append(fluid)
        gt = self.gut.get_value()
        if gt > 0.01:
            ge = 6.45 if nb > 0.01 else L / 2 + 0.45
            gw = 0.3 * sc * self.gutw.get_value()
            gy = cy + self.guty
            g1 = Rectangle(width=2 * ge, height=2 * gw, fill_color=YELLOW, fill_opacity=gt, stroke_width=0).move_to([cx, gy, 0])
            g2 = Rectangle(width=2 * ge, height=gw, fill_color=WHITE_, fill_opacity=0.9 * gt, stroke_width=0).move_to([cx, gy, 0])
            parts += [g1, g2]
        wl = self.wall.get_value()
        if wl > 0.01:
            parts.append(VMobject().set_points_as_corners(pts).set_stroke(BLUE, width=7 * ws, opacity=wl).set_fill(opacity=0))
            xi = xs * (L - 0.16) / L
            hi = np.maximum(h - 0.1, 0.0)
            ti, bi = Pt(cx + xi, cy + hi), Pt(cx + xi[::-1], cy - hi[::-1])
            parts.append(VMobject().set_points_as_corners(np.vstack([ti, bi, ti[:1]]))
                         .set_stroke(hot, width=5 * ws * self.wallw.get_value(), opacity=wl).set_fill(opacity=0))
        nh = self.hoop.get_value()
        for i in range(6):
            a = float(np.clip(nh - i, 0, 1))
            if a <= 0.02:
                continue
            x = -0.38 * L + 0.76 * L * i / 5
            hh = max(float(self.hx(np.array([x]), R, L, p)[0]) - 0.12, 0.05)
            th = np.linspace(0, TAU, 24)
            parts.append(VMobject().set_points_as_corners(Pt(cx + x + 0.07 * np.cos(th), cy + hh * np.sin(th)))
                         .set_stroke(hot, width=4 * ws * (1 + gl), opacity=a))
        lg = self.lng.get_value()
        if lg > 0.01:
            e = 0.9 * self.ext.get_value()
            x2 = np.linspace(-L / 2 - e, L / 2 + e, 50)
            h2 = np.where(np.abs(x2) <= L / 2, self.hx(x2, R, L, p), R0 * sc)
            n = max(2, int(lg * 50))
            for sg in (-1, 1):
                parts.append(VMobject().set_points_as_corners(Pt(cx + x2[:n], cy + sg * np.maximum(h2[:n] - 0.16, 0.05)))
                             .set_stroke(hot, width=7 * ws * (1 + 0.5 * gl), opacity=1))
        sp = self.sept.get_value()
        if sp > 0.01:
            xe = L / 2 - 0.07
            hs = max(float(self.hx(np.array([xe]), R, L, p)[0]) - 0.05, 0.05)
            for sg in (-1, 1):
                parts.append(Line([cx + sg * xe, cy - hs, 0], [cx + sg * xe, cy + hs, 0]).set_stroke(hot, width=10 * ws * (1 + 0.8 * gl), opacity=sp))
        se = max(self.setae.get_value(), self.auto_setae)
        if se > 0.02:
            ln = 0.42 * se * (0.6 + 0.4 * sc)
            for i in range(5):
                x = -0.3 * L + 0.6 * L * i / 4
                y0 = float(self.hx(np.array([x]), R, L, p)[0])
                for sg in (-1, 1):
                    parts.append(Line([cx + x, cy + sg * y0, 0], [cx + x + 0.07, cy + sg * (y0 + ln), 0]).set_stroke(BRISTLE, width=4))
        if self.reach > 0.02:
            op = float(np.clip((1.22 - self.rr()) / 0.25, 0, 1)) * self.reach
            if op > 0.03:
                y = cy + R + 0.3
                parts.append(Arrow([cx + 0.28 * L, y, 0], [cx - 0.28 * L, y, 0], color=YELLOW, stroke_width=6, buff=0,
                                   max_tip_length_to_length_ratio=0.4).set_opacity(op))
        swap(self, parts)


class FluidDots(VGroup):
    def __init__(self, seg, n=10, seed=3):
        super().__init__()
        import random
        rng = random.Random(seed)
        self.seg, self.t, self.speed = seg, 0.0, 1.0
        self.par = []
        for _ in range(n):
            self.add(Dot(radius=0.055, color=WHITE_))
            self.par.append((rng.uniform(.5, 1.1), rng.uniform(0, 6.3), rng.uniform(.6, 1.3), rng.uniform(0, 6.3),
                             rng.uniform(-0.85, 0.85), rng.uniform(-0.8, 0.8)))
        self.add_updater(self._upd)

    def _upd(self, m, dt):
        s = self.seg
        self.t += dt * self.speed
        R, L = s.dims()
        p = s.pinch.get_value()
        op = float(np.clip(s.fl.get_value() * 1.2 - 0.2, 0, 1)) * 0.8
        for d, (a, ph, b, q, ux, uy) in zip(self, self.par):
            x = s.cx + ux * (L / 2 - 0.3) + 0.25 * np.sin(a * self.t + ph)
            y = s.cy + uy * (R * (1 - 0.5 * p) - 0.2) + 0.12 * np.sin(b * self.t + q)
            d.move_to([x, y, 0]).set_opacity(op)


class Balloon(VGroup):
    """A water balloon squeezed by a cartoon hand (two fingers). d = 0..1 is how hard it is squeezed."""

    def __init__(self, cx=0.0, cy=CY, sc=1.0):
        super().__init__()
        self.cx, self.cy, self.sc = cx, cy, sc
        self.d = ValueTracker(0.0)
        self.op = ValueTracker(1.0)
        self.add_updater(lambda m, dt: m.rebuild())
        self.rebuild()

    def rebuild(self):
        d, sc, cx, cy, op = self.d.get_value(), self.sc, self.cx, self.cy, self.op.get_value()
        Lh = 1.9 * (1 + 0.24 * d)
        xs = np.linspace(-Lh, Lh, 70)
        base = 1.0 * np.sqrt(np.clip(1 - (xs / Lh) ** 2, 0, 1)) ** 0.85
        h = base * (1 - 0.5 * d * np.exp(-(xs / 0.6) ** 2)) * (1 + 0.3 * d * (np.abs(xs) / Lh) ** 2)
        top, bot = Pt(cx + xs * sc, cy + h * sc), Pt(cx + xs[::-1] * sc, cy - h[::-1] * sc)
        body = VMobject().set_points_as_corners(np.vstack([top, bot, top[:1]])).set_fill(CYAN, opacity=0.4 * op).set_stroke(CYAN, width=5, opacity=op)
        hm = h[len(xs) // 2] * sc
        parts = [body]
        for sg in (-1, 1):
            y0 = cy + sg * (hm + 0.28 * sc)
            parts.append(Line([cx - 0.15 * sc, y0, 0], [cx + 1.0 * sc, cy + sg * (hm + 2.4 * sc), 0])
                         .set_stroke(PINK, width=34 * sc, opacity=op).set_cap_style(CapStyleType.ROUND))
        swap(self, parts)


# ------------------------------------------------------------------ a row of segments (a worm)
class Row(VGroup):
    def __init__(self, n=5, sc=0.45, x0=-3.0, rs=None, cy=CY):
        super().__init__()
        self.sc, self.x0, self.cy, self.t = sc, x0, cy, 0.0
        self.vx = 0.0
        self.amp = ValueTracker(0.0)
        self.flex = ValueTracker(0.0)
        self.setae_on = ValueTracker(0.0)
        self.segs = [Seg(0, cy, sc, (rs or [R0] * n)[i], live=False) for i in range(n)]
        self.add(*self.segs)
        self.add_updater(lambda m, dt: m.step(dt))
        self.step(0)

    def step(self, dt):
        self.t += dt
        self.x0 += self.vx * dt
        x = self.x0
        amp, fx, so = self.amp.get_value(), self.flex.get_value(), self.setae_on.get_value()
        for i, s in enumerate(self.segs):
            dr = amp * 0.33 * np.sin(2 * np.pi * i / 3.2 - 2 * np.pi * self.t / 5.5)
            dr += fx * 0.1 * np.sin(0.9 * self.t + 2.1 * i + 0.4 * i * i)
            s.dr = dr
            R, L = s.dims()
            s.cx = x + L / 2
            x += L
            s.auto_setae = so * float(np.clip((s.rr() - 1.5) / 0.2, 0, 1))
            s.rebuild(dt)

    def show(self, **kw):
        """Set every segment's tracker to a value, e.g. show(fl=1, wall=1)."""
        for s in self.segs:
            for k, v in kw.items():
                getattr(s, k).set_value(v)
        return self

    def trk(self, name):
        return [getattr(s, name) for s in self.segs]


# ------------------------------------------------------------------ gut tube
GT = [0.55, 1.05, 0.85, 0.4]          # half-widths of pharynx, crop, gizzard, intestine
GFR = [0.0, 0.14, 0.30, 0.43, 1.0]    # region boundaries as fractions of the gut


class Gut(VGroup):
    def __init__(self, xa=-3.6, xb=3.6, cy=CY, wbase=0.25):
        super().__init__()
        self.xa, self.xb, self.len, self.wbase = ValueTracker(xa), ValueTracker(xb), ValueTracker(0.0), ValueTracker(wbase)
        self.tr = [ValueTracker(0) for _ in range(4)]
        self.gl = [ValueTracker(0) for _ in range(4)]
        self.cy, self.t = cy, 0.0
        self.add_updater(lambda m, dt: m.rebuild(dt))
        self.rebuild(0)

    def width_at(self, f):
        base = self.wbase.get_value()
        w = base * np.ones_like(f)
        mods = [1 + 0.18 * np.sin(5 * self.t), 1 + 0.06 * np.sin(1.3 * self.t), 1 - 0.14 * (0.5 + 0.5 * np.sin(3 * self.t)), 1.0]
        for k in range(4):
            S = 0.5 * (np.tanh((f - GFR[k]) / 0.012) - np.tanh((f - GFR[k + 1]) / 0.012))
            w = w + self.tr[k].get_value() * (GT[k] * mods[k] - base) * S
        return w

    def x_of(self, f):
        a, b = self.xa.get_value(), self.xb.get_value()
        return a + f * (b - a)

    def rebuild(self, dt=0.0):
        self.t += dt
        ln = self.len.get_value()
        if ln < 0.02:
            swap(self, [])
            return
        a, b, cy = self.xa.get_value(), self.xb.get_value(), self.cy
        f = np.linspace(0, ln, 120)
        xs = a + f * (b - a)
        w = self.width_at(f)
        S2 = 0.5 * (np.tanh((f - GFR[2]) / 0.012) - np.tanh((f - GFR[3]) / 0.012))
        wl = np.maximum(w - 0.16 - 0.2 * self.tr[2].get_value() * S2, 0.05)
        top, bot = Pt(xs, cy + w), Pt(xs[::-1], cy - w[::-1])
        yel = VMobject().set_points_as_corners(np.vstack([top, bot, top[:1]])).set_fill(YELLOW, opacity=0.95).set_stroke(YELLOW, width=2)
        lt, lb = Pt(xs, cy + wl), Pt(xs[::-1], cy - wl[::-1])
        lum = VMobject().set_points_as_corners(np.vstack([lt, lb, lt[:1]])).set_fill(WHITE_, opacity=0.9).set_stroke(width=0)
        parts = [yel, lum]
        for k in range(4):
            g = self.gl[k].get_value()
            if g > 0.02:
                m = (f >= GFR[k]) & (f <= GFR[k + 1])
                if m.sum() > 2:
                    parts.append(VMobject().set_points_as_corners(Pt(xs[m], cy + w[m])).set_stroke(WHITE_, width=8, opacity=g))
                    parts.append(VMobject().set_points_as_corners(Pt(xs[m], cy - w[m])).set_stroke(WHITE_, width=8, opacity=g))
        swap(self, parts)


class Food(VGroup):
    def __init__(self, gut, n=9):
        super().__init__()
        self.gut, self.t, self.n = gut, 0.0, n
        self.on = ValueTracker(0.0)
        self.regional = ValueTracker(0.0)
        for _ in range(n):
            self.add(Circle(radius=0.1, color=FOOD, fill_opacity=1, stroke_width=0))
        self.add_updater(self._upd)

    def _upd(self, m, dt):
        self.t += dt
        g, reg, on = self.gut, self.regional.get_value(), self.on.get_value()
        for i, d in enumerate(self):
            s = (self.t * 0.085 + i / self.n) % 1.0
            f_lin = -0.05 + 1.05 * s
            f_reg = float(np.interp(s, [0, .12, .45, .60, 1.0], [-0.05, 0.14, 0.30, 0.43, 1.0]))
            f = (1 - reg) * f_lin + reg * f_reg
            x = g.x_of(f)
            w = float(g.width_at(np.array([np.clip(f, 0, 1)]))[0])
            y = g.cy + 0.45 * w * np.sin(2.3 * self.t + 1.7 * i)
            sc = 1.0
            fade = 1.0
            if reg > 0.5 and f > 0.43:
                sc = max(0.08, 1 - (f - 0.43) / 0.45)
                fade = float(np.clip(1 - (f - 0.7) / 0.3, 0, 1))
            if reg > 0.5 and 0.30 < f < 0.43:
                sc = 0.75
            fade *= float(np.clip((f + 0.05) / 0.05, 0, 1)) * on
            d.set_width(max(0.03, 0.2 * sc)).move_to([x, y, 0]).set_opacity(fade)


# ================================================================== SCENES
class S00Title(TitleCard):
    TITLE = "One Segment, Constant Volume"
    LESSON = "Animal Body Plans"


def jiggle(m, dt):
    m.t0 += dt
    m.shift([0.12 * dt * np.sin(3 * m.t0), 0.12 * dt * np.cos(2.4 * m.t0), 0])


def blink(m, dt):
    m.bt = getattr(m, "bt", 0.0) + dt * 5
    m.set_opacity(0.65 + 0.35 * np.sin(m.bt))


class S01Question(Sc):
    def construct(self):
        soil = RoundedRectangle(corner_radius=0.3, width=3.0, height=3.6, stroke_width=0, fill_color=SOIL, fill_opacity=0.85).move_to([-5.1, 0.3, 0])
        gr = grains(-6.4, -3.8, -1.3, 1.9, 22, 4)
        for d in gr:
            d.set_z_index(-2)
            d.t0 = np.random.uniform(0, 6)
            d.add_updater(jiggle)
        worm = make_worm(0.3)
        self.add(soil, gr)
        self.play(FadeIn(worm), run_time=0.6)
        self.at("no bones")
        verts = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.26, height=0.5, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25).move_to([x, 0, 0])
                         for x in np.linspace(-1.2, 1.2, 8)])
        ribs = VGroup(*[Line([x, 0.25, 0], [x + 0.1, 0.62, 0], color=TEXT, stroke_width=3) for x in np.linspace(-1.0, 1.0, 5)],
                      *[Line([x, -0.25, 0], [x + 0.1, -0.62, 0], color=TEXT, stroke_width=3) for x in np.linspace(-1.0, 1.0, 5)])
        skull = Circle(radius=0.3, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25).move_to([-1.75, 0, 0])
        sk = VGroup(verts, ribs, skull).move_to([0.2, 2.5, 0])
        self.play(FadeIn(sk, shift=DOWN * 0.15), run_time=0.9)
        cross = VGroup(Line(sk.get_corner(UL), sk.get_corner(DR), color=RED, stroke_width=10),
                       Line(sk.get_corner(DL), sk.get_corner(UR), color=RED, stroke_width=10))
        self.play(Create(cross), run_time=0.8)
        self.at("what does it push against")
        self.play(FadeOut(sk), FadeOut(cross), run_time=0.5)
        q = T("?", 110, color=YELLOW, weight=BOLD).move_to([-2.4, 1.9, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        q.add_updater(blink)
        self.at("the first film")
        card = RoundedRectangle(corner_radius=0.2, width=4.4, height=2.4, color=GREY, stroke_width=3).move_to([4.3, 2.5, 0])
        tree = VGroup(PL((2.4, 2.5), (3.0, 2.5)), PL((3.0, 3.0), (3.0, 2.0)),
                      *[PL((3.0, y), (3.7, y)) for y in (3.0, 2.5, 2.0)])
        tips = VGroup(*[critter(k).scale(1.3).move_to([4.15, y, 0]) for k, y in zip(("plan", "nem", "earth"), (3.0, 2.5, 2.0))])
        cap = T("gene tree", 28, color=TEAL).move_to([5.55, 2.5, 0])
        inset = VGroup(card, tree, tips, cap)
        self.play(FadeIn(inset, shift=LEFT * 0.2), run_time=1.0)
        self.at("does not reveal")
        self.play(Indicate(tree, scale_factor=1.0, color=TEAL), run_time=1.6)
        self.at("this film asks")
        self.play(FadeOut(q), inset.animate.scale(0.15).move_to([6.2, 3.3, 0]).set_opacity(0), run_time=1.0)
        big = T("What is a body plan for?", 40, font=TITLE_FONT).move_to([0, 2.9, 0])
        self.at("a body plan is for")
        self.play(FadeIn(big, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S02Segment(Sc):
    def construct(self):
        soil = RoundedRectangle(corner_radius=0.3, width=3.0, height=3.6, stroke_width=0, fill_color=SOIL, fill_opacity=0.85).move_to([-5.1, 0.3, 0])
        gr = grains(-6.4, -3.8, -1.3, 1.9, 22, 4)
        worm = make_worm(0.3)
        self.add(soil, gr, worm)
        self.wait(0.3)
        box = Rectangle(width=1.1, height=1.6, color=YELLOW, stroke_width=6).move_to([0.2, 0.3, 0])
        self.play(Create(box), run_time=0.8)
        self.at("one segment")
        self.play(Indicate(box, scale_factor=1.15, color=YELLOW), run_time=1.0)
        seg = Seg()
        dots = FluidDots(seg)
        self.at("earthworm")
        worm.clear_updaters()
        self.add(seg, dots)
        self.play(FadeOut(worm, scale=2.5), FadeOut(soil, scale=1.5), FadeOut(gr), FadeOut(box, scale=2.5),
                  seg.wall.animate.set_value(1), run_time=1.5)
        self.at("coelum")
        l1 = lab("coelom: fluid", 0, -2.2, CYAN, 32, BOLD)
        self.play(seg.fl.animate.set_value(1), FadeIn(l1, shift=UP * 0.1), run_time=1.3)
        self.at("septa")
        self.play(seg.sept.animate.set_value(1), run_time=0.8)
        s1, s2 = lab("septum", -1.85, 2.65, ORANGE, 30, BOLD), lab("septum", 1.85, 2.65, ORANGE, 30, BOLD)
        a1 = Arrow([-1.85, 2.4, 0], [-1.85, 1.65, 0], color=ORANGE, buff=0, stroke_width=5)
        a2 = Arrow([1.85, 2.4, 0], [1.85, 1.65, 0], color=ORANGE, buff=0, stroke_width=5)
        self.play(FadeIn(s1), FadeIn(s2), Create(a1), Create(a2), FadeOut(l1), run_time=0.7)
        self.at("largely separate")
        gl = lab("gut, separate from the coelom", 0, -3.0, YELLOW, 30)
        self.play(seg.gut.animate.set_value(1), FadeIn(gl, shift=UP * 0.1), run_time=1.2)
        self.at("segments on either side")
        self.play(seg.nb.animate.set_value(1), run_time=1.2)
        self.finish()


class S03Muscles(Sc):
    def construct(self):
        seg = Seg()
        for n, v in dict(wall=1, fl=1, sept=1, gut=1, nb=1).items():
            getattr(seg, n).set_value(v)
        dots = FluidDots(seg)
        self.add(seg, dots)
        self.play(seg.wallw.animate.set_value(2.2), run_time=0.9)
        self.play(seg.wallw.animate.set_value(1), run_time=0.9)
        self.at("circular")
        c1 = lab("circular muscle", 0, 2.9, ORANGE, 34, BOLD)
        self.play(FadeIn(c1, shift=DOWN * 0.1), seg.hoop.animate.set_value(6), run_time=2.0, rate_func=linear)
        self.at("like rings")
        self.play(seg.glow.animate.set_value(1), run_time=0.5)
        self.play(seg.glow.animate.set_value(0), FadeOut(c1), run_time=0.6)
        self.at("longitudinal")
        c2 = lab("longitudinal muscle", 0, -2.7, ORANGE, 34, BOLD)
        seg.ext.set_value(1)
        self.play(FadeIn(c2, shift=UP * 0.1), seg.lng.animate.set_value(1), run_time=2.2, rate_func=linear)
        self.play(seg.glow.animate.set_value(1), run_time=0.4)
        self.play(seg.glow.animate.set_value(0), run_time=0.5)
        self.finish()


class S04Skeleton(Sc):
    def construct(self):
        bal = Balloon()
        seg = Seg()
        dots = FluidDots(seg)
        self.add(bal)
        self.wait(0.6)
        self.at("cannot be squeezed")
        self.play(bal.d.animate.set_value(1), run_time=1.6)
        self.at("smaller volume")
        self.play(bal.d.animate.set_value(0.2), run_time=0.8)
        self.play(bal.d.animate.set_value(1), run_time=0.8)
        self.at("so fluid held in")
        self.add(seg, dots)
        self.play(bal.op.animate.set_value(0), seg.wall.animate.set_value(1), seg.fl.animate.set_value(1), run_time=1.3)
        self.remove(bal)
        self.at("muscular wall")
        seg.ext.set_value(0)
        self.play(seg.hoop.animate.set_value(6), seg.lng.animate.set_value(1), run_time=1.2)
        self.at("gives muscles")
        a1 = Arrow([0, CY + 1.2 * R0 + 1.0, 0], [0, CY + 1.2 * R0 + 0.2, 0], color=ORANGE, buff=0, stroke_width=8)
        a2 = Arrow([0, CY - 1.2 * R0 - 1.0, 0], [0, CY - 1.2 * R0 - 0.2, 0], color=ORANGE, buff=0, stroke_width=8)
        self.play(Create(a1), Create(a2), run_time=0.8)
        self.at("something to push against")
        self.play(seg.glow.animate.set_value(1), run_time=0.6)
        self.play(seg.glow.animate.set_value(0), run_time=0.8)
        self.at("hydrostatic skeleton")
        self.play(FadeOut(a1), FadeOut(a2), run_time=0.4)
        h = lab("hydrostatic skeleton = fluid + muscular wall", 0, -2.9, TEAL, 30, BOLD)
        self.play(FadeIn(h, shift=UP * 0.1), run_time=0.8)
        self.at("water in a balloon")
        b2 = Balloon(4.7, 2.5, 0.42)
        self.add(b2)
        self.play(b2.d.animate.set_value(1), run_time=1.0)
        self.play(b2.d.animate.set_value(0.1), run_time=0.8)
        self.at("treat one segment")
        self.play(FadeOut(b2), run_time=0.4)
        tag = chip("model: one sealed segment", ORANGE, 30).move_to([0, 3.2, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.1), seg.sept.animate.set_value(1), seg.glow.animate.set_value(1), run_time=0.8)
        self.play(seg.glow.animate.set_value(0), run_time=0.8)
        self.finish()


class S05Organs(Sc):
    def construct(self):
        seg = Seg()
        for n, v in dict(wall=1, fl=1, sept=1, hoop=6, lng=1).items():
            getattr(seg, n).set_value(v)
        dots = FluidDots(seg)
        self.add(seg, dots)
        seg.osc.set_value(0.07)
        self.wait(0.4)
        self.at("organs inside")
        self.play(seg.gut.animate.set_value(1), run_time=1.0)
        self.at("such as the gut")
        gl = lab("gut", 0, -2.0, YELLOW, 30, BOLD)
        self.play(FadeIn(gl), run_time=0.5)
        self.at("can grow")
        self.play(seg.gutw.animate.set_value(1.7), FadeOut(gl), run_time=1.1)
        seg.gam = 0.0

        def move(m, dt):
            m.guty = m.gam * np.sin(m.t * 1.4)
        seg.add_updater(move)
        self.at("and move")
        self.play(UpdateFromAlphaFunc(seg, lambda m, a: setattr(m, "gam", 0.4 * a)), run_time=1.0, rate_func=linear)
        self.at("independence")
        t = lab("organs can move somewhat\nindependently of the wall", 0, -3.0, YELLOW, 30)
        self.play(FadeIn(t, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S06Predict(Sc):
    def construct(self):
        seg = Seg()
        for n, v in dict(wall=1, fl=1, sept=1, hoop=6, lng=1).items():
            getattr(seg, n).set_value(v)
        dots = FluidDots(seg)
        self.add(seg, dots)
        self.wait(0.5)
        self.at("circular muscles contract")
        self.play(seg.glow.animate.set_value(1), run_time=0.6)
        self.play(seg.pinch.animate.set_value(0.33), run_time=2.2)
        self.at("narrower")
        self.at("nowhere to go")
        dots.speed = 2.6
        c = lab("fluid has nowhere to go", 0, 2.7, CYAN, 32, BOLD)
        self.play(FadeIn(c, shift=DOWN * 0.1), run_time=0.6)
        self.at("does the segment get longer")
        q = lab("longer, shorter, or the same?", 0, 2.7, YELLOW, 36, BOLD)
        self.play(FadeOut(c), run_time=0.3)
        self.play(FadeIn(q), run_time=0.3)
        self.at("longer")
        c1 = chip("longer", YELLOW, 36).move_to([-4.0, -2.7, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.4)
        self.at("shorter")
        c2 = chip("shorter", YELLOW, 36).move_to([0, -2.7, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.4)
        self.at("stay the same")
        c3 = chip("the same", YELLOW, 36).move_to([4.0, -2.7, 0])
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.4)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        seg = Seg()
        for n, v in dict(wall=1, fl=1, sept=1, hoop=6, lng=1, glow=1, pinch=0.33).items():
            getattr(seg, n).set_value(v)
        dots = FluidDots(seg)
        dots.speed = 2.6
        q = lab("longer, shorter, or the same?", 0, 2.7, YELLOW, 36, BOLD)
        cs = [chip(t, YELLOW, 36).move_to([x, -2.7, 0]) for t, x in (("longer", -4.0), ("shorter", 0), ("the same", 4.0))]
        ring = Circle(radius=0.42, color=GREY, stroke_width=5).move_to([6.0, -3.2, 0])
        prog = ValueTracker(1.0)
        arc = always_redraw(lambda: Arc(radius=0.42, start_angle=PI / 2, angle=max(0.01, TAU * prog.get_value()), color=YELLOW, stroke_width=8).move_to([6.0, -3.2, 0]))
        self.add(seg, dots, q, *cs, ring, arc)
        self.play(prog.animate.set_value(0.0), run_time=4.9, rate_func=linear)
        self.finish()


class S08Reveal(Sc):
    def construct(self):
        seg = Seg()
        for n, v in dict(wall=1, fl=1, sept=1, hoop=6, lng=1, glow=1, pinch=0.33).items():
            getattr(seg, n).set_value(v)
        dots = FluidDots(seg)
        dots.speed = 2.6
        q = lab("longer, shorter, or the same?", 0, 2.7, YELLOW, 36, BOLD)
        c1 = chip("longer", YELLOW, 36).move_to([-4.0, -2.7, 0])
        c2 = chip("shorter", YELLOW, 36).move_to([0, -2.7, 0])
        c3 = chip("the same", YELLOW, 36).move_to([4.0, -2.7, 0])
        self.add(seg, dots, q, c1, c2, c3)
        self.wait(0.2)
        self.at("gets longer")
        self.play(FadeOut(c2), FadeOut(c3), FadeOut(q), Indicate(c1, scale_factor=1.2, color=GREEN),
                  seg.pinch.animate.set_value(0), seg.r.animate.set_value(1.05), run_time=2.0)
        dots.speed = 1.0
        self.play(FadeOut(c1), run_time=0.4)
        self.at("volume must stay the same")
        sv = svlab()
        self.play(FadeIn(sv), run_time=0.6)
        self.at("a narrower")
        self.play(seg.r.animate.set_value(0.95), seg.glow.animate.set_value(0), run_time=1.5)
        self.at("stretch")
        self.play(seg.r.animate.set_value(0.88), run_time=1.5)
        self.at("septum move apart")
        disc = Circle(radius=0.6, color=ORANGE, stroke_width=6, fill_color=ORANGE, fill_opacity=0.25).move_to([5.4, -2.2, 0])
        disc.add_updater(lambda m: m.become(Circle(radius=max(0.2, 1.2 * (seg.rr() - 0.35)), color=ORANGE, stroke_width=6, fill_color=ORANGE, fill_opacity=0.25).move_to([5.4, -2.2, 0])))
        dl = lab("end face", 5.4, -3.35, ORANGE, 28)
        ar = VGroup(*[Arrow([0, 0, 0], [0.8, 0, 0], color=ORANGE, buff=0, stroke_width=7) for _ in range(2)])

        def place(m, dt):
            R, L = seg.dims()
            m[0].put_start_and_end_on([-L / 2 + 0.1, CY + R + 0.5, 0], [-L / 2 - 0.8, CY + R + 0.5, 0])
            m[1].put_start_and_end_on([L / 2 - 0.1, CY + R + 0.5, 0], [L / 2 + 0.8, CY + R + 0.5, 0])
        ar.add_updater(place)
        self.add(ar)
        self.play(FadeIn(disc), FadeIn(dl), run_time=0.6)
        self.play(seg.r.animate.set_value(0.82), run_time=2.6)
        self.finish()


class S09Fat(Sc):
    def construct(self):
        seg = Seg(r=0.82)
        for n, v in dict(wall=1, fl=1, sept=1, hoop=6, lng=1).items():
            getattr(seg, n).set_value(v)
        dots = FluidDots(seg)
        sv = svlab()
        self.add(seg, dots, sv)
        self.wait(0.3)
        self.at("longitudinal muscles contract")
        l1 = lab("longitudinal muscles", 0, 2.9, ORANGE, 32, BOLD)
        self.play(FadeIn(l1, shift=DOWN * 0.1), seg.glow.animate.set_value(1), run_time=1.0)
        self.at("shorter")
        self.play(FadeOut(l1), seg.r.animate.set_value(1.55), run_time=3.2)
        self.at("fatter")
        self.at("tiny bristles")
        gr = grains(-2.4, 2.4, -3.1, -2.5, 10, 7)
        gr2 = grains(-2.4, 2.4, 2.8, 3.3, 10, 8)
        self.play(FadeIn(gr), FadeIn(gr2), seg.setae.animate.set_value(1), seg.glow.animate.set_value(0), run_time=1.3)
        self.at("seedy")
        sl = lab("setae", 3.6, -2.0, BRISTLE, 32, BOLD)
        self.play(FadeIn(sl, shift=UP * 0.1), run_time=0.6)
        self.at("grip the soil")
        self.play(Indicate(gr, scale_factor=1.0, color=WHITE_), Indicate(gr2, scale_factor=1.0, color=WHITE_), run_time=1.4)
        self.finish()


PAT = [1.35, 1.0, 1.65, 1.35, 1.2]   # head -> tail radii for the neighbours scene


class S10Neighbours(Sc):
    def construct(self):
        row = Row(5, 0.55, -5.0)
        row.show(wall=0, fl=0, sept=0)
        self.add(row)
        self.play(*[t.animate.set_value(1) for n in ("wall", "fl", "sept") for t in row.trk(n)], run_time=1.0)
        self.at("septa partition")
        self.play(*[t.animate.set_value(1) for t in row.trk("glow")], run_time=0.7)
        self.play(*[t.animate.set_value(0) for t in row.trk("glow")], run_time=0.7)
        self.at("neighbors")
        self.play(*[s.r.animate.set_value(r) for s, r in zip(row.segs, PAT)], run_time=2.2)
        self.at("in textbook accounts")
        self.play(row.flex.animate.set_value(1), run_time=0.6)
        self.at("each segment")
        tb = lab("each segment works on its own", 0, 3.1, TEAL, 32, BOLD)
        self.play(FadeIn(tb, shift=DOWN * 0.1), run_time=0.8)
        self.at("one is long and thin")
        self.play(row.flex.animate.set_value(0), FadeOut(tb), run_time=0.8)
        seg1, seg2 = row.segs[1], row.segs[2]
        ll = lab("long, thin", seg1.cx, 2.1, YELLOW, 32, BOLD)
        self.play(FadeIn(ll, shift=DOWN * 0.1), run_time=0.6)
        self.at("reaching forward")
        ar = Arrow([seg1.cx + 0.8, 1.4, 0], [seg1.cx - 0.9, 1.4, 0], color=YELLOW, buff=0, stroke_width=8)
        self.play(Create(ar), run_time=0.7)
        self.at("its neighbor is short")
        sf = lab("short, fat, anchored", seg2.cx, -3.0, GREEN, 32, BOLD)
        gr = grains(-4.5, 4.5, -2.4, -1.5, 18, 11)
        self.play(FadeIn(sf, shift=UP * 0.1), run_time=0.7)
        self.at("anchored")
        self.play(FadeIn(gr), seg2.setae.animate.set_value(1), run_time=1.2)
        self.finish()


class S11Wave(Sc):
    def construct(self):
        row = Row(5, 0.55, -4.6, PAT)
        row.show(wall=1, fl=1, sept=1)
        row.vx = -0.09
        gr = grains(-6.3, 6.3, -2.4, -1.5, 30, 11)
        peb = Ellipse(width=0.7, height=0.45, color=GREY, fill_color=GREY, fill_opacity=0.9, stroke_width=0).move_to([-5.2, -2.2, 0])
        self.add(gr, peb, row)
        self.wait(0.2)
        self.at("pass these shapes")
        self.play(*[s.r.animate.set_value(1.35) for s in row.segs], row.amp.animate.set_value(1), run_time=3.3)
        self.at("long thin")
        for s in row.segs:
            s.reach = 1.0
        c1 = chip("long, thin: reach ahead", YELLOW, 32).move_to([0, 3.1, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.6)
        self.at("short fat")
        c2 = chip("short, fat: hold the ground", GREEN, 32).move_to([0, -3.25, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        self.at("hold the ground")
        self.play(row.setae_on.animate.set_value(1), run_time=1.0)
        self.at("and the worm moves forward")
        self.play(FadeOut(c2), run_time=0.4)
        ml = lab("marker pebble", -4.7, -3.2, TEXT, 30)
        self.play(FadeIn(ml, shift=UP * 0.1), Indicate(peb, scale_factor=1.3, color=WHITE_), run_time=1.0)
        self.finish()


class S12Gut(Sc):
    def construct(self):
        row = Row(5, 0.55, -4.4)
        row.show(wall=0.45, fl=1, sept=0.6)
        row.flex.set_value(0.6)
        gut = Gut(-4.4, 4.4)
        food = Food(gut)
        self.add(row, gut, food)
        self.wait(0.5)
        self.at("the same body plan")
        self.play(*[t.animate.set_value(0.15) for t in row.trk("fl")], run_time=1.2)
        self.at("the gut runs through")
        self.play(gut.len.animate.set_value(1), run_time=1.6, rate_func=linear)
        self.at("mouth")
        m = lab("mouth", -5.55, CY, WHITE_, 32, BOLD)
        self.play(FadeIn(m, shift=RIGHT * 0.1), run_time=0.4)
        self.at("anus")
        a = lab("anus", 5.4, CY, WHITE_, 32, BOLD)
        self.play(FadeIn(a, shift=LEFT * 0.1), run_time=0.4)
        self.at("food moves")
        self.play(food.on.animate.set_value(1), run_time=0.5)
        self.at("one way")
        ar = Arrow([-2.6, 1.9, 0], [2.6, 1.9, 0], color=FOOD, buff=0, stroke_width=9)
        ow = lab("one way", 0, 2.55, FOOD, 34, BOLD)
        self.play(Create(ar), FadeIn(ow), run_time=0.8)
        self.at("successive regions")
        divs = VGroup(*[DashedLine([gut.x_of(f), CY - 1.5, 0], [gut.x_of(f), CY + 1.5, 0], color=WHITE_, stroke_width=4)
                        for f in GFR[1:4]])
        self.play(Create(divs), run_time=1.0)
        self.at("specialize")
        self.play(Indicate(divs, scale_factor=1.0, color=TEAL), run_time=1.4)
        self.finish()


class S13Regions(Sc):
    def construct(self):
        gut = Gut(-4.4, 4.4)
        gut.len.set_value(1)
        food = Food(gut)
        food.on.set_value(1)
        self.add(gut, food)
        self.play(gut.xa.animate.set_value(-5.4), gut.xb.animate.set_value(5.4), gut.wbase.animate.set_value(0.32), run_time=0.9)
        self.at("pharynx")
        l1 = lab("pharynx", -4.65, 2.1, WHITE_, 32, BOLD)
        self.play(gut.tr[0].animate.set_value(1), gut.gl[0].animate.set_value(1), FadeIn(l1), run_time=0.9)
        self.at("crop")
        food.regional.set_value(1)
        l2 = lab("crop", -3.0, -1.9, WHITE_, 32, BOLD)
        self.play(gut.gl[0].animate.set_value(0), gut.tr[1].animate.set_value(1), gut.gl[1].animate.set_value(1), FadeIn(l2), run_time=1.0)
        self.at("gizzard")
        l3 = lab("gizzard", -1.46, 2.1, WHITE_, 32, BOLD)
        grit = VGroup(*[Dot(radius=0.06, color=GREY) for _ in range(7)])
        grit.t = 0.0

        def jig(m, dt):
            m.t += dt
            x0 = gut.x_of(0.365)
            for i, d in enumerate(m):
                d.move_to([x0 + 0.35 * np.sin(2.1 * m.t + i * 1.7), CY + 0.18 * np.sin(3.3 * m.t + i * 2.3), 0])
        grit.add_updater(jig)
        self.play(gut.gl[1].animate.set_value(0), gut.tr[2].animate.set_value(1), gut.gl[2].animate.set_value(1), FadeIn(l3), FadeIn(grit), run_time=1.0)
        self.at("intestine")
        l4 = lab("intestine", 2.3, -1.9, WHITE_, 32, BOLD)
        self.play(gut.gl[2].animate.set_value(0), gut.tr[3].animate.set_value(1), gut.gl[3].animate.set_value(1), FadeIn(l4), run_time=1.0)
        self.wait(1.2)
        self.play(gut.gl[3].animate.set_value(0), run_time=0.6)
        self.finish()


class S14Close(Sc):
    def construct(self):
        seg = Seg()
        for n, v in dict(wall=1, fl=1, sept=1, hoop=6, lng=1).items():
            getattr(seg, n).set_value(v)
        seg.osc.set_value(0.04)
        dots = FluidDots(seg)
        self.add(seg, dots)
        self.wait(0.8)
        self.at("no bones")
        nb = lab("no bones", 0, 3.0, YELLOW, 38, BOLD)
        self.play(FadeIn(nb, shift=DOWN * 0.1), run_time=0.7)
        self.at("skeleton")
        sk = chip("fluid in muscle = skeleton", TEAL, 34).move_to([0, -2.9, 0])
        self.play(FadeOut(nb), FadeIn(sk, shift=UP * 0.1), seg.glow.animate.set_value(1), run_time=0.8)
        self.play(seg.glow.animate.set_value(0), run_time=0.6)
        self.at("the volume stays the same")
        sv = svlab()
        self.play(FadeIn(sv), run_time=0.7)
        self.at("narrow a segment")
        seg.osc.set_value(0)
        c1 = chip("narrower = longer", ORANGE, 36).move_to([0, 3.0, 0])
        self.play(FadeOut(sk), FadeIn(c1), seg.r.animate.set_value(0.85), run_time=2.4)
        self.at("shorten it")
        c2 = chip("shorter = wider", ORANGE, 36).move_to([0, 3.0, 0])
        self.play(FadeOut(c1), FadeIn(c2), seg.r.animate.set_value(1.7), run_time=1.6)
        self.finish()


class S15End(EndCard):
    LINE = "Fluid held in by muscle is a skeleton: narrower means longer."
