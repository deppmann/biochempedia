"""Osmoregulation: Which Way Does the Water Go? (one world: tank + fish + osmolality bar + ledger).
Colours: water BLUE, sodium chloride ORANGE, urea GREEN, outlines light grey.
DASHED arrow = passive leak; SOLID arrow with ATP tag = paid transport."""
import math, random
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
OUTL = "#B8BEC9"
FILL = "#1d2333"
TMAO_C = "#C9CED8"
TOP_W, TOP_S = [-4.6, -3.7], [-2.6, -1.5]
BOT_W, BOT_S = [-4.2, -3.3], [-3.1, -2.0]
FISH = {"bony": (-3.2, -0.2, 2.4, 1.7), "shark": (-3.1, -0.2, 2.5, 1.25)}
TANK_L, TANK_R, TANK_T, TANK_B = -6.75, 0.35, 2.85, -3.6
BAR_X, BAR_Y0, BAR_H = 3.4, 0.3, 3.0
PAN = (0.6, 6.8, -3.6, -0.45)        # ledger panel x0 x1 y0 y1


def P(x, y):
    return np.array([x, y, 0.0])


def edge_y(kind, x, side):
    cx, cy, a, b = FISH[kind]
    dx = max(-1, min(1, (x - cx) / a))
    return cy + side * b * math.sqrt(1 - dx * dx)


class _Ref:
    """Invisible guide geometry: opacity and colour changes on a parent group never reveal it."""
    _locked = False

    def lock(self):
        VMobject.set_fill(self, opacity=0)
        VMobject.set_stroke(self, opacity=0)
        self._locked = True
        return self

    def set_opacity(self, *a, **k): return self if self._locked else super().set_opacity(*a, **k)
    def set_fill(self, *a, **k): return self if self._locked else super().set_fill(*a, **k)
    def set_stroke(self, *a, **k): return self if self._locked else super().set_stroke(*a, **k)
    def set_color(self, *a, **k): return self if self._locked else super().set_color(*a, **k)
    def fade(self, *a, **k): return self if self._locked else super().fade(*a, **k)


class Tube(VMobject):
    """A thick open line: opacity changes touch the stroke only (never a fill)."""
    def set_opacity(self, o, *a, **k):
        return self.set_stroke(opacity=o * 0.35)


class RefRect(_Ref, Rectangle):
    pass


class RefLine(_Ref, Line):
    pass


class RefPoly(_Ref, VMobject):
    pass


# ---------------------------------------------------------------- moving things
def jitter(n, x0, x1, y0, y1, color, seed, speed=0.4, r=0.07, op=0.9, z=1):
    ref = RefRect(width=x1 - x0, height=y1 - y0).move_to(P((x0 + x1) / 2, (y0 + y1) / 2)).lock()
    g = VGroup(ref)
    rng = random.Random(seed)
    for _ in range(n):
        d = Dot(radius=r, color=color).set_opacity(op)
        d.u, d.v = rng.random(), rng.random()
        ang = rng.uniform(0, TAU)
        sp = speed * rng.uniform(0.6, 1.4)
        d.vu, d.vv = math.cos(ang) * sp / (x1 - x0), math.sin(ang) * sp / (y1 - y0)

        def upd(m, dt, ref=ref):
            m.u += m.vu * dt
            m.v += m.vv * dt
            if m.u < 0 or m.u > 1:
                m.vu *= -1
                m.u = min(1, max(0, m.u))
            if m.v < 0 or m.v > 1:
                m.vv *= -1
                m.v = min(1, max(0, m.v))
            m.move_to(ref.get_corner(DL) + np.array([m.u * ref.width, m.v * ref.height, 0]))
        d.add_updater(upd)
        upd(d, 0)
        g.add(d)
    g.set_z_index(z)
    return g


def flow(ref, colors, period=2.2, r=0.08, z=6):
    """Dots travelling along ref (a Line or polyline), fading in and out at the ends."""
    g = VGroup(ref)
    n = len(colors)
    for i, c in enumerate(colors):
        d = Dot(radius=r, color=c)
        d.ph = i / n

        def upd(m, dt, ref=ref):
            m.ph = (m.ph + dt / period) % 1
            m.move_to(ref.point_from_proportion(m.ph))
            m.set_opacity(max(0.0, min(1, 5 * m.ph, 5 * (1 - m.ph))))
        d.add_updater(upd)
        upd(d, 0)
        g.add(d)
    g.set_z_index(z)
    return g


def dashed(a, b, color, period=2.2, n=3):
    a, b = P(*a[:2]), P(*b[:2])
    u = (b - a) / np.linalg.norm(b - a)
    line = DashedLine(a, b - u * 0.22, color=color, stroke_width=5, dash_length=0.16)
    head = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.17)
    head.rotate(angle_of_vector(u) - PI / 2).move_to(b - u * 0.14)
    ref = RefLine(a, b).lock()
    line.set_z_index(6)
    head.set_z_index(6)
    return VGroup(line, head, flow(ref, [color] * n, period=period, r=0.07))


def solid(a, b, color=ORANGE):
    return Arrow(P(*a), P(*b), buff=0, color=color, stroke_width=9, tip_length=0.3,
                 max_tip_length_to_length_ratio=0.5).set_z_index(6)


def arrows(kind, xs, side, direction, color, period=2.2):
    g = VGroup()
    for x in xs:
        e = edge_y(kind, x, side)
        inner, outer = e - side * 0.55, e + side * 1.0
        a, b = (inner, outer) if direction == "out" else (outer, inner)
        g.add(dashed((x, a), (x, b), color, period))
    return g


def atp_chip(size=22, pad=0.09):
    c = chip("ATP", ORANGE, size=size, pad=pad)
    bg = c[0].copy().set_fill(BG, 1).set_stroke(width=0)
    return VGroup(bg, c)


def solid_pair(kind, xs, side, direction, tag=True):
    g = VGroup()
    ys = []
    for x in xs:
        e = edge_y(kind, x, side)
        inner, outer = e - side * 0.55, e + side * 1.0
        a, b = (inner, outer) if direction == "out" else (outer, inner)
        g.add(solid((x, a), (x, b)))
        ys.append((inner + outer) / 2)
    if tag:
        g.add(atp_chip(22, 0.09).move_to(P(sum(xs) / len(xs), sum(ys) / len(ys))).set_z_index(7))
    return g


def drink_path():
    pts = [P(0.2, -0.15), P(-0.85, -0.15), P(-1.6, -0.95), P(-3.9, -0.95)]
    tube = Tube().set_points_as_corners(pts[1:]).set_stroke(OUTL, 16, opacity=0.35).set_fill(opacity=0).set_z_index(3)
    ref = RefPoly().set_points_as_corners(pts).lock()
    return VGroup(tube, flow(ref, [BLUE, ORANGE, BLUE, ORANGE, BLUE, ORANGE], period=3.0, r=0.085))


def urine_stream():
    e = edge_y("bony", -5.0, -1)
    a, b = P(-5.0, e + 0.1), P(-5.0, -3.4)
    band = Line(a, b, color=BLUE, stroke_width=26, stroke_opacity=0.5).set_z_index(4)
    ref = RefLine(a, b).lock()
    return VGroup(band, flow(ref, [WHITE, BLUE, ORANGE, WHITE], period=1.6, r=0.07))


# ---------------------------------------------------------------- fish
def bony_fish():
    tail = Polygon(P(-5.4, -0.2), P(-6.55, 1.0), P(-6.3, -0.2), P(-6.55, -1.4), color=OUTL, stroke_width=4,
                   fill_color=FILL, fill_opacity=1)
    body = Ellipse(width=4.8, height=3.4, color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1).move_to(P(-3.2, -0.2))
    eye = Dot(P(-1.05, 0.35), radius=0.09, color=TEXT)
    gill = Arc(radius=1.2, start_angle=PI - 0.62, angle=1.24, arc_center=P(-0.7, -0.2), color="#7F8896", stroke_width=5)
    return VGroup(tail, body, eye, gill).set_z_index(2)


def shark_fish():
    tail = Polygon(P(-5.4, -0.2), P(-6.55, 1.35), P(-6.1, -0.2), P(-6.55, -1.3), color=OUTL, stroke_width=4,
                   fill_color=FILL, fill_opacity=1)
    dorsal = Polygon(P(-3.9, 0.95), P(-3.1, 2.0), P(-2.5, 1.0), color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1)
    pect = Polygon(P(-2.6, -1.1), P(-3.4, -2.2), P(-3.5, -1.1), color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1)
    body = Ellipse(width=5.0, height=2.5, color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1).move_to(P(-3.1, -0.2))
    eye = Dot(P(-0.95, 0.25), radius=0.09, color=TEXT)
    slits = VGroup(*[Arc(radius=1.0, start_angle=PI - 0.5, angle=1.0, arc_center=P(-0.7 + 0.2 * i, -0.2), color="#7F8896", stroke_width=4)
                     for i in range(3)])
    return VGroup(tail, dorsal, pect, body, eye, slits).set_z_index(2)


# ---------------------------------------------------------------- bar
class Bar:
    def __init__(self, labels=True, body=350, out=1000, stack=None):
        self.labels = labels
        self.frame = Rectangle(width=0.4, height=BAR_H, color=OUTL, stroke_width=4).move_to(P(BAR_X, BAR_Y0 + BAR_H / 2))
        self.bt, self.ot = ValueTracker(body), ValueTracker(out)
        self.seg_t = [ValueTracker(v) for v in (stack or (0, 0, 0))]
        self.tri_b = Triangle(color=TEXT, fill_opacity=1, stroke_width=0).scale(0.15).rotate(-PI / 2)
        self.tri_o = Triangle(color=BLUE, fill_opacity=1, stroke_width=0).scale(0.15).rotate(-PI / 2)
        self.segs = []
        for t, c in zip(self.seg_t, (ORANGE, GREEN, TMAO_C)):
            r = Rectangle(width=0.4, height=0.01, stroke_width=0, fill_color=c, fill_opacity=0.95)
            r.t = t
            self.segs.append(r)
        self.lab_b = T("body", 24, TEXT) if labels else VMobject()
        self.lab_o = T("outside", 24, BLUE) if labels else VMobject()
        self.axis = T("mOsm/kg\nillustrative", 22, TEXT).move_to(P(5.6, 0.55)) if labels else VMobject()
        self.drv = VMobject()
        self.drv.add_updater(lambda m: self.place())
        self.parts = VGroup(self.frame, *self.segs, self.tri_b, self.tri_o, self.lab_b, self.lab_o, self.axis, self.drv)
        self.place()

    def y_of(self, v):
        return self.frame.get_bottom()[1] + v / 1100 * self.frame.height

    def place(self):
        k = self.frame.width / 0.4
        cx = self.frame.get_center()[0]
        yb, yo = self.y_of(self.bt.get_value()), self.y_of(self.ot.get_value())
        self.tri_b.move_to(P(cx - 0.3 * k, yb))
        self.tri_o.move_to(P(cx - 0.3 * k, yo))
        base = self.frame.get_bottom()[1]
        acc = 0.0
        for r in self.segs:
            h = max(r.t.get_value() / 1100 * self.frame.height, 1e-3)
            r.stretch_to_fit_height(h)
            r.move_to(P(cx, base + acc + h / 2))
            acc += h
        if self.labels:
            ly_b, ly_o = yb, yo
            if abs(yb - yo) < 0.5:
                mid = (yb + yo) / 2
                ly_b, ly_o = (mid + 0.25, mid - 0.25) if yb >= yo else (mid - 0.25, mid + 0.25)
            self.lab_b.move_to(P(cx - 0.55 * k - self.lab_b.width / 2, ly_b))
            self.lab_o.move_to(P(cx - 0.55 * k - self.lab_o.width / 2, ly_o))

    def set_labels(self, body=None, out=None):
        if body:
            self.lab_b.become(T(body, 24, TEXT))
        if out:
            self.lab_o.become(T(out, 24, BLUE))
        self.place()

    def hide_pointers(self):
        for m in (self.tri_b, self.tri_o, self.lab_b, self.lab_o):
            m.set_opacity(0)

    def seg_labels(self):
        """Labels for the stack, right of the bar (fixed spots for the shark's numbers)."""
        out = VGroup()
        for txt, c, y in (("salts", ORANGE, self.y_of(225)), ("urea", GREEN, self.y_of(700)), ("TMAO", TMAO_C, self.y_of(985))):
            t = T(txt, 22, c)
            t.move_to(P(BAR_X + 0.4 + t.width / 2, y))
            out.add(t)
        return out


def flow_ind(direction):
    body = T("body", 24, TEXT).move_to(P(4.45, 3.5))
    outside = T("outside", 24, BLUE).move_to(P(6.2, 3.5))
    arr = Arrow(P(4.9, 3.5), P(5.55, 3.5), buff=0, color=BLUE, stroke_width=7, tip_length=0.22, max_tip_length_to_length_ratio=0.5)
    if direction == "in":
        arr.rotate(PI)
    wl = T("water", 22, BLUE).move_to(P(5.22, 3.1))
    g = VGroup(body, arr, outside, wl)
    g.arr = arr
    return g


# ---------------------------------------------------------------- ledger
def mark_mob(st, pos, k=1.0):
    if st == "ok":
        m = VMobject().set_points_as_corners([pos + k * P(-0.13, 0.0), pos + k * P(-0.03, -0.12), pos + k * P(0.17, 0.14)]).set_stroke(GREEN, 7 * k)
        m.set_fill(opacity=0)
    elif st == "bad":
        m = Circle(radius=0.13 * k, color=RED, fill_opacity=1, stroke_width=0).move_to(pos)
    else:
        m = Circle(radius=0.03, color=RED, fill_opacity=0, stroke_width=0).move_to(pos)
        m.set_stroke(opacity=0)
    return m


class Ledger:
    ROW = {"water": -1.85, "salt": -2.6}
    IN_X, OUT_X, MAXW, MARK_X = 2.15, 4.35, 1.7, 6.5

    def __init__(self, labels=True, headers=True):
        x0, x1, y0, y1 = PAN
        self.panel = Rectangle(width=x1 - x0, height=y1 - y0, color=OUTL, stroke_width=3, fill_color=BG, fill_opacity=0.9)
        self.panel.move_to(P((x0 + x1) / 2, (y0 + y1) / 2))
        self.tr = {k: ValueTracker(0) for k in ("wi", "wo", "si", "so")}
        self.bars = {}
        for k, row, col in (("wi", "water", BLUE), ("wo", "water", BLUE), ("si", "salt", ORANGE), ("so", "salt", ORANGE)):
            r = Rectangle(width=0.01, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.9)
            r.k = k
            self.bars[k] = r
        self.marks = {r: mark_mob(None, P(self.MARK_X, y)) for r, y in self.ROW.items()}
        self.title = T("ledger, schematic", 22, TEXT).move_to(P(2.35, -0.72)) if labels else VMobject()
        self.head_in = T("In", 26, TEXT).move_to(P(3.0, -1.2)) if labels else VMobject()
        self.head_out = T("Out", 26, TEXT).move_to(P(5.2, -1.2)) if labels else VMobject()
        self.rowlab = VGroup(T("water", 26, BLUE).move_to(P(1.4, -1.85)), T("salt", 26, ORANGE).move_to(P(1.4, -2.6))) if labels else VGroup()
        self.cap_pos = P(3.7, -3.25)
        self.cap = T(".", 24, BG).move_to(self.cap_pos) if labels else VMobject()
        self.labels = labels
        self.drv = VMobject()
        self.drv.add_updater(lambda m: self.place())
        self.parts = VGroup(self.panel, self.title, self.head_in, self.head_out, self.rowlab, *self.bars.values(),
                            *self.marks.values(), self.cap, self.drv)
        self.place()

    def place(self):
        k = self.panel.width / 6.2
        c = self.panel.get_center()
        for key, r in self.bars.items():
            row = "water" if key[0] == "w" else "salt"
            x0 = self.IN_X if key[1] == "i" else self.OUT_X
            w = max(self.tr[key].get_value() * self.MAXW * k, 1e-3)
            r.stretch_to_fit_width(w)
            r.stretch_to_fit_height(0.42 * k)
            r.move_to(c + k * P(x0 - 3.7, self.ROW[row] + 2.025) + P(w / 2, 0))

    def set(self, wi=None, wo=None, si=None, so=None, ws=None, ss=None, cap=None, capc=TEXT):
        """Static set."""
        for k, v in (("wi", wi), ("wo", wo), ("si", si), ("so", so)):
            if v is not None:
                self.tr[k].set_value(v)
        for row, st in (("water", ws), ("salt", ss)):
            if st is not None or True:
                if (row == "water" and ws is not None) or (row == "salt" and ss is not None):
                    self.marks[row].become(mark_mob(st if st != "none" else None, self.marks_pos(row), self.kc()[0]))
        if cap is not None and self.labels:
            self.cap.become(self.cap_mob(cap, capc))
        self.place()

    def kc(self):
        return self.panel.width / 6.2, self.panel.get_center()

    def marks_pos(self, row):
        k, c = self.kc()
        return c + k * P(self.MARK_X - 3.7, self.ROW[row] + 2.025)

    def cap_mob(self, txt, c):
        k, ctr = self.kc()
        t = T(txt if txt else ".", 24, c if txt else BG).scale(k)
        return t.move_to(ctr + k * P(0, -3.25 + 2.025))

    def anim(self, wi=None, wo=None, si=None, so=None, ws=None, ss=None, cap=None, capc=TEXT):
        an = []
        for k, v in (("wi", wi), ("wo", wo), ("si", si), ("so", so)):
            if v is not None:
                an.append(self.tr[k].animate.set_value(v))
        for row, st in (("water", ws), ("salt", ss)):
            if st is not None:
                an.append(Transform(self.marks[row], mark_mob(None if st == "none" else st, self.marks_pos(row), self.kc()[0])))
        if cap is not None and self.labels:
            an.append(Transform(self.cap, self.cap_mob(cap, capc)))
        return an


# ---------------------------------------------------------------- the world
class World:
    def __init__(self, fish="bony", water="sea", label=None, labels=True, bar=(350, 1000), stack=None, flow_dir="out",
                 body_n=6, tank_n=24, ledger=True, bar_on=True):
        self.fish_kind = fish
        self.frame = Rectangle(width=TANK_R - TANK_L, height=TANK_T - TANK_B, color=OUTL, stroke_width=4).move_to(
            P((TANK_L + TANK_R) / 2, (TANK_T + TANK_B) / 2))
        op = {"plain": 0.08, "sea": 0.16, "river": 0.05}[water]
        self.fill = Rectangle(width=TANK_R - TANK_L, height=TANK_T - TANK_B, stroke_width=0, fill_color=BLUE, fill_opacity=op).move_to(self.frame)
        self.fish = bony_fish() if fish == "bony" else shark_fish()
        self.tank_dots = jitter(tank_n, TANK_L + 0.15, TANK_R - 0.15, TANK_B + 0.15, TANK_T - 0.15, ORANGE, 11, 0.45) if tank_n else VGroup()
        bx = (-4.7, -2.3, -0.55, 0.9) if fish == "bony" else (-4.7, -2.2, -0.75, 0.7)
        self.body_box = bx
        self.body_dots = jitter(body_n, *bx, ORANGE, 5, 0.3, z=3) if body_n else VGroup()
        self.label = T(label, 34, BLUE, weight=BOLD).move_to(P(TANK_L + 0.05, 3.4)) if label else VGroup()
        if label:
            self.label.move_to(P(TANK_L + 0.05 + self.label.width / 2, 3.4))
        self.tank = VGroup(self.fill, self.tank_dots, self.frame, self.fish, self.body_dots, self.label)
        self.bar = Bar(labels, *bar, stack=stack) if bar_on else None
        self.ledger = Ledger(labels) if ledger else None
        self.flow = flow_ind(flow_dir) if labels and bar_on else VGroup()
        self.flow_dir = flow_dir
        parts = [self.tank]
        if self.bar:
            parts.append(self.bar.parts)
        if self.ledger:
            parts.append(self.ledger.parts)
        parts.append(self.flow)
        self.all = VGroup(*parts)
        self.bubbles = None

    def parts_list(self, pointers=True, flow=True):
        out = [self.fill, self.tank_dots, self.frame, self.fish, self.body_dots, self.label]
        if self.bar:
            b = self.bar
            out += [b.frame, b.axis, *b.segs, b.drv]
            if pointers:
                out += [b.tri_b, b.tri_o, b.lab_b, b.lab_o]
        if self.ledger:
            out.append(self.ledger.parts)
        if flow:
            out.append(self.flow)
        return out

    def add_to(self, sc, pointers=True, flow=True):
        sc.add(*self.parts_list(pointers, flow))

    def gill_label(self):
        t = T("gills", 26, YELLOW).move_to(P(-0.1, -1.15))
        line = Line(P(-0.5, -1.05), P(-1.62, -0.72), color=YELLOW, stroke_width=3)
        hl = Arc(radius=1.2, start_angle=PI - 0.62, angle=1.24, arc_center=P(-0.7, -0.2), color=YELLOW, stroke_width=7).set_z_index(3)
        return VGroup(t, line, hl)

    def strip(self, txt, color=TEXT):
        t = T(txt, 26, color)
        return t.move_to(P(-5.2 + t.width / 2, 3.4))

    def flip_flow(self):
        self.flow_dir = "in" if self.flow_dir == "out" else "out"
        return Rotate(self.flow.arr, PI)


def sea_leaks(kind="bony"):
    water = VGroup(arrows(kind, TOP_W, 1, "out", BLUE), arrows(kind, BOT_W[:1], -1, "out", BLUE))
    salt = arrows(kind, TOP_S, 1, "in", ORANGE)
    return water, salt


def river_leaks():
    water = VGroup(arrows("bony", TOP_W, 1, "in", BLUE), arrows("bony", BOT_W[:1], -1, "in", BLUE))
    salt = arrows("bony", TOP_S, 1, "out", ORANGE)
    return water, salt


class S00Title(TitleCard):
    LESSON = "Osmoregulation"
    TITLE = "Which Way Does the Water Go?"


class S01Hook(SpokenScene):
    def construct(self):
        bowl = Circle(radius=2.5, color=OUTL, stroke_width=5, fill_color=BLUE, fill_opacity=0.14).move_to(P(-3.4, 0.25))
        sea = Rectangle(width=6.3, height=5.0, color=OUTL, stroke_width=5, fill_color=BLUE, fill_opacity=0.18).move_to(P(3.4, 0.25))

        def fish(cx, cy, s):
            body = Ellipse(width=2.9 * s, height=1.8 * s, color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1).move_to(P(cx, cy))
            tail = Polygon(P(cx - 1.4 * s, cy), P(cx - 2.15 * s, cy + 0.6 * s), P(cx - 2.0 * s, cy), P(cx - 2.15 * s, cy - 0.6 * s),
                           color=OUTL, stroke_width=4, fill_color=FILL, fill_opacity=1)
            eye = Dot(P(cx + 0.9 * s, cy + 0.2 * s), radius=0.08, color=TEXT)
            return VGroup(tail, body, eye).set_z_index(2)
        gf, cod = fish(-3.1, 0.25, 1.0), fish(3.7, 0.25, 1.0)
        l1, l2 = T("goldfish", 30, TEXT).move_to(P(-3.4, -3.0)), T("cod", 30, TEXT).move_to(P(3.4, -3.0))
        dots_l = jitter(5, -5.6, -0.9, -1.8, 1.9, ORANGE, 2, 0.3, z=1)
        dots_r = jitter(16, 0.45, 6.2, -2.0, 2.7, ORANGE, 3, 0.4, z=1)
        w_in = VGroup(dashed(P(-4.1, 2.0), P(-4.1, 1.0), BLUE), dashed(P(-2.6, 2.0), P(-2.6, 1.0), BLUE),
                      dashed(P(-3.5, -1.9), P(-3.5, -0.8), BLUE))
        w_out = VGroup(dashed(P(3.2, 1.05), P(3.2, 2.2), BLUE), dashed(P(4.4, 1.05), P(4.4, 2.2), BLUE),
                       dashed(P(3.8, -0.65), P(3.8, -1.9), BLUE))
        q = T("same size, day after day?", 32, YELLOW).move_to(P(0, -3.55))
        self.play(FadeIn(bowl), FadeIn(dots_l), FadeIn(gf), FadeIn(l1), run_time=1.0)
        self.at("soaks up water")
        self.play(Create(w_in), run_time=0.8)
        self.at("and a cod")
        self.play(FadeIn(sea), FadeIn(dots_r), FadeIn(cod), FadeIn(l2), run_time=1.0)
        self.at("loses it")
        self.play(Create(w_out), run_time=0.8)
        self.at("How does each one")
        self.play(Indicate(gf, scale_factor=1.06), Indicate(cod, scale_factor=1.06), run_time=1.4)
        self.at("same size")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S02Rule(SpokenScene):
    def construct(self):
        mem = Line(P(0, -2.7), P(0, 2.7), color=OUTL, stroke_width=7)
        mlab = T("membrane", 26, TEXT).move_to(P(0, 3.3))
        left = jitter(6, -6.2, -2.0, -2.3, 2.0, ORANGE, 1, 0.45, r=0.09)
        right = jitter(28, 2.0, 6.2, -2.3, 2.0, ORANGE, 2, 0.45, r=0.09)
        few = T("fewer particles", 28, TEXT).move_to(P(-4.0, 2.65))
        many = T("more particles", 28, TEXT).move_to(P(4.0, 2.65))
        wat = VGroup(dashed(P(-1.9, 1.5), P(1.9, 1.5), BLUE, 2.6), dashed(P(-1.9, 0.5), P(1.9, 0.5), BLUE, 2.6))
        sal = VGroup(dashed(P(1.9, -0.6), P(-1.9, -0.6), ORANGE, 2.6), dashed(P(1.9, -1.6), P(-1.9, -1.6), ORANGE, 2.6))
        cap = T("osmolality = dissolved particles per kg of water", 28, YELLOW).move_to(P(0, -3.1))
        small = T("assumes: water can cross, no opposing pressure", 22, TEXT).move_to(P(0, -3.55))
        self.play(Create(mem), run_time=1.0)
        self.play(FadeIn(mlab), run_time=0.5)
        self.at("surface water can")
        self.play(FadeIn(left), FadeIn(right), run_time=1.2)
        self.at("With nothing pushing back")
        self.play(FadeIn(small), FadeIn(few), FadeIn(many), run_time=1.0)
        self.at("water moves on")
        self.play(Create(wat), run_time=1.0)
        self.at("more dissolved particles")
        self.play(Indicate(many, color=YELLOW, scale_factor=1.12), run_time=1.5)
        self.at("That count is called")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=1.2)
        self.at("In these fish")
        self.play(FadeOut(wat), run_time=0.6)
        self.at("each salt leaks")
        self.play(Create(sal), run_time=1.0)
        self.at("where it is scarcer")
        self.play(Indicate(few, color=YELLOW, scale_factor=1.12), run_time=1.2)
        self.finish()


class S03Bar(SpokenScene):
    def construct(self):
        w = World(water="plain", label=None, bar=(350, 1000), tank_n=0, body_n=6, ledger=False)
        w.bar.set_labels("body ~350", "outside ~1,000")
        bub = jitter(10, TANK_L + 0.2, TANK_R - 0.2, TANK_B + 0.2, TANK_T - 0.2, BLUE, 4, 0.6, r=0.09, op=0.85)
        self.add(w.bar.drv)
        self.play(FadeIn(w.fill), FadeIn(w.frame), FadeIn(w.fish), FadeIn(w.body_dots), FadeIn(bub), run_time=1.2)
        self.at("bar in the corner")
        self.play(FadeIn(w.bar.frame), FadeIn(w.bar.axis), run_time=1.0)
        self.add(*w.bar.segs)
        self.at("One mark shows")
        self.play(FadeIn(w.bar.tri_b), FadeIn(w.bar.lab_b), run_time=0.9)
        self.at("one shows the water outside")
        self.play(FadeIn(w.bar.tri_o), FadeIn(w.bar.lab_o), run_time=0.9)
        self.at("Water drifts toward")
        self.play(FadeIn(w.flow), run_time=0.9)
        self.at("higher mark")
        self.play(Indicate(w.bar.lab_o, color=YELLOW, scale_factor=1.15), run_time=1.6)
        self.finish()


class S04Ledger(SpokenScene):
    def construct(self):
        w = World(water="plain", bar=(350, 1000), tank_n=0, body_n=6)
        w.bar.set_labels("body ~350", "outside ~1,000")
        L = w.ledger
        bub = jitter(10, TANK_L + 0.2, TANK_R - 0.2, TANK_B + 0.2, TANK_T - 0.2, BLUE, 4, 0.6, r=0.09, op=0.85)
        w.add_to(self, flow=True)
        self.add(bub)
        self.remove(L.parts)
        self.add(*L.bars.values(), *L.marks.values(), L.cap, L.drv)
        self.play(FadeIn(L.panel), FadeIn(L.title), run_time=1.0)
        self.at("one column")
        self.play(FadeIn(L.head_in, shift=DOWN * 0.1), run_time=0.7)
        self.at("one for what goes out")
        self.play(FadeIn(L.head_out, shift=DOWN * 0.1), run_time=0.7)
        self.at("water and salts hold steady")
        self.play(FadeIn(L.rowlab, shift=RIGHT * 0.1), run_time=0.9)
        self.at("the columns must match")
        self.play(*L.anim(wi=0.55, wo=0.55, si=0.4, so=0.4, ws="ok", ss="ok", cap="steady: in = out", capc=GREEN), run_time=1.8)
        self.at("for water and")
        self.play(Indicate(L.bars["wi"], color=WHITE), Indicate(L.bars["wo"], color=WHITE), run_time=1.0)
        self.at("each salt")
        self.play(Indicate(L.bars["si"], color=WHITE), Indicate(L.bars["so"], color=WHITE), run_time=1.0)
        self.finish()


class S05Sea(SpokenScene):
    def construct(self):
        w = World(fish="bony", water="plain", label=None, bar=(350, 1000), body_n=6, tank_n=0)
        w.bar.set_labels("body ~350", "outside ~1,000")
        w.ledger.set(wi=0.55, wo=0.55, si=0.4, so=0.4, ws="ok", ss="ok", cap="steady: in = out", capc=GREEN)
        bub = jitter(10, TANK_L + 0.2, TANK_R - 0.2, TANK_B + 0.2, TANK_T - 0.2, BLUE, 4, 0.6, r=0.09, op=0.85)
        w.add_to(self)
        self.add(bub)
        sea_dots = jitter(24, TANK_L + 0.15, TANK_R - 0.15, TANK_B + 0.15, TANK_T - 0.15, ORANGE, 11, 0.45)
        lab = T("SEA", 34, BLUE, weight=BOLD)
        lab.move_to(P(TANK_L + 0.05 + lab.width / 2, 3.4))
        self.play(w.fill.animate.set_fill(BLUE, 0.16), FadeIn(lab), FadeOut(bub), FadeIn(sea_dots),
                  *w.ledger.anim(wi=0, wo=0, si=0, so=0, ws="none", ss="none", cap=""), run_time=1.6)
        self.at("Its blood")
        st = w.strip("blood: about a third of seawater")
        self.play(FadeIn(st, shift=UP * 0.1), Indicate(w.bar.lab_b, color=YELLOW, scale_factor=1.12), run_time=1.2)
        self.at("than seawater")
        self.play(Indicate(w.bar.lab_o, color=YELLOW, scale_factor=1.12), run_time=1.3)
        water, salt = sea_leaks()
        gl = w.gill_label()
        self.at("water leaks out")
        self.play(Create(water), *w.ledger.anim(wo=0.9, ws="bad"), run_time=1.2)
        self.at("across its gills")
        self.play(FadeIn(gl), run_time=0.8)
        self.at("and salt leaks in")
        self.play(Create(salt), *w.ledger.anim(si=0.45, ss="bad", cap="unbalanced", capc=RED), run_time=1.0)
        self.finish()


def sea_state(sc, ledger, with_gill=True):
    w = World(fish="bony", water="sea", label="SEA", bar=(350, 1000), body_n=6, tank_n=24)
    w.bar.set_labels("body ~350", "outside ~1,000")
    w.ledger.set(**ledger)
    w.add_to(sc)
    water, salt = sea_leaks()
    sc.add(water, salt)
    w.water, w.salt, w.gl = water, salt, None
    if with_gill:
        w.gl = w.gill_label()
        sc.add(w.gl)
    return w


class S06Drink(SpokenScene):
    def construct(self):
        w = sea_state(self, dict(wi=0, wo=0.9, si=0.45, so=0, ws="bad", ss="bad", cap="unbalanced", capc=RED))
        self.add(w.strip("blood: about a third of seawater"))
        w.water.set_opacity(0.5)
        w.salt.set_opacity(0.5)
        self.at("Water is short")
        self.play(Indicate(w.ledger.bars["wo"], color=WHITE, scale_factor=1.1), run_time=1.1)
        self.at("so the fish drink")
        path = drink_path()
        dl = T("drinking", 26, YELLOW).move_to(P(-1.2, -2.35))
        self.play(FadeIn(path), FadeIn(dl), run_time=1.2)
        self.at("Its gut absorbs the water")
        self.play(*w.ledger.anim(wi=0.9, ws="ok"), run_time=1.6)
        self.at("but the salt comes in")
        self.play(*w.ledger.anim(si=0.85, ss="bad"), Indicate(w.ledger.bars["si"], color=WHITE, scale_factor=1.08), run_time=1.5)
        self.finish()


class S07Pump(SpokenScene):
    def construct(self):
        w = sea_state(self, dict(wi=0.9, wo=0.9, si=0.85, so=0, ws="ok", ss="bad", cap="unbalanced", capc=RED))
        self.add(w.strip("blood: about a third of seawater"))
        path = drink_path()
        dl = T("drinking", 26, YELLOW).move_to(P(-1.2, -2.35))
        self.add(path, dl)
        self.at("Now salt is the problem")
        self.play(w.water.animate.set_opacity(0.3), path.animate.set_opacity(0.3), FadeOut(dl),
                  Indicate(w.ledger.bars["si"], color=WHITE, scale_factor=1.1), run_time=1.5)
        self.at("Cells in the gills")
        self.play(Indicate(w.gl, color=YELLOW, scale_factor=1.1), run_time=1.3)
        self.at("send sodium and chloride")
        pump = solid_pair("bony", BOT_S, -1, "out", tag=False)
        self.play(Create(pump), run_time=1.3)
        self.play(*w.ledger.anim(so=0.85), run_time=1.5)
        self.at("against the leak")
        self.play(Indicate(w.salt, color=YELLOW, scale_factor=1.08), run_time=1.3)
        self.at("so it costs")
        tag = atp_chip(22, 0.09).move_to(P(-2.55, -2.1)).set_z_index(7)
        self.play(FadeIn(tag, scale=1.2), run_time=0.7)
        self.play(*w.ledger.anim(ss="ok", ws="ok", cap="balanced", capc=GREEN), run_time=0.9)
        self.finish()


def river_world(ledger, fill=True):
    w = World(fish="bony", water="river", label="RIVER", bar=(300, 5), flow_dir="in", body_n=16, tank_n=2)
    w.bar.set_labels("body ~300", "outside ~5")
    w.ledger.set(**ledger)
    return w


class S08River(SpokenScene):
    def construct(self):
        w = sea_state(self, dict(wi=0.9, wo=0.9, si=0.85, so=0.85, ws="ok", ss="ok", cap="balanced", capc=GREEN))
        pump = solid_pair("bony", BOT_S, -1, "out")
        st = w.strip("blood: about a third of seawater")
        self.add(pump, st)
        w.water.set_opacity(0.4)
        w.salt.set_opacity(0.4)
        self.at("Now move")
        lab = T("RIVER", 34, BLUE, weight=BOLD)
        lab.move_to(P(TANK_L + 0.05 + lab.width / 2, 3.4))
        newdots = jitter(2, TANK_L + 0.15, TANK_R - 0.15, TANK_B + 0.15, TANK_T - 0.15, ORANGE, 12, 0.45)
        bodyx = jitter(10, *w.body_box, ORANGE, 8, 0.3, z=3)
        self.play(FadeOut(w.water), FadeOut(w.salt), FadeOut(pump), FadeOut(w.gl), FadeOut(st),
                  w.fill.animate.set_fill(BLUE, 0.05), FadeOut(w.tank_dots), FadeIn(newdots), FadeIn(bodyx),
                  Transform(w.label, lab),
                  *w.ledger.anim(wi=0, wo=0, si=0, so=0, ws="none", ss="none", cap=""), run_time=1.6)
        self.at("The bar flips")
        self.play(w.bar.bt.animate.set_value(300), w.bar.ot.animate.set_value(5), w.flip_flow(), run_time=2.0)
        w.bar.set_labels("body ~300", "outside ~5")
        self.at("Its blood is far saltier")
        st2 = w.strip("blood: far saltier than fresh water")
        self.play(FadeIn(st2, shift=UP * 0.1), Indicate(w.bar.lab_b, color=YELLOW, scale_factor=1.12), run_time=1.3)
        water, salt = river_leaks()
        gl = w.gill_label()
        self.at("So water pours in")
        self.play(Create(water), *w.ledger.anim(wi=0.9, ws="bad"), run_time=1.2)
        self.play(FadeIn(gl), run_time=0.6)
        self.at("salt leaks out")
        self.play(Create(salt), *w.ledger.anim(so=0.45, ss="bad", cap="unbalanced", capc=RED), run_time=1.0)
        self.finish()


def river_state(sc, ledger, strip=True):
    w = river_world(ledger)
    w.add_to(sc)
    water, salt = river_leaks()
    gl = w.gill_label()
    sc.add(water, salt, gl)
    if strip:
        sc.add(w.strip("blood: far saltier than fresh water"))
    w.water, w.salt, w.gl = water, salt, gl
    return w


class S09Urine(SpokenScene):
    def construct(self):
        w = river_state(self, dict(wi=0.9, wo=0, si=0, so=0.45, ws="bad", ss="bad", cap="unbalanced", capc=RED))
        self.at("The water is easy")
        self.play(w.water.animate.set_opacity(0.5), w.gl.animate.set_opacity(0.5), run_time=1.0)
        self.at("The kidney makes")
        urine = urine_stream()
        ul = T("dilute\nurine", 26, BLUE).move_to(P(-6.0, -2.55))
        self.play(FadeIn(urine), FadeIn(ul), run_time=1.5)
        self.at("and the extra water")
        self.play(*w.ledger.anim(wo=0.9, ws="ok"), run_time=1.8)
        self.finish()


def urine_boxes():
    b1 = RoundedRectangle(corner_radius=0.06, width=0.85, height=0.42, color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.85).move_to(P(4.65, -2.6))
    b2 = b1.copy().move_to(P(5.7, -2.6))
    l1 = T("urine", 22, TEXT).move_to(P(4.65, -3.0))
    l2 = T("gill leak", 22, TEXT).move_to(P(5.75, -3.0))
    return VGroup(b1, l1), VGroup(b2, l2)


class S10Predict(SpokenScene):
    def construct(self):
        w = river_state(self, dict(wi=0.9, wo=0.9, si=0, so=0.45, ws="ok", ss="bad", cap="unbalanced", capc=RED), strip=False)
        w.water.set_opacity(0.5)
        urine = urine_stream()
        ul = T("dilute\nurine", 26, BLUE).move_to(P(-6.0, -2.55))
        self.add(urine, ul)
        self.at("But that urine")
        u, g = urine_boxes()
        self.play(w.ledger.tr["so"].animate.set_value(0), *w.ledger.anim(cap=""), FadeIn(u), run_time=0.9)
        self.at("salt keeps leaking")
        self.play(FadeIn(g), Indicate(w.salt, color=YELLOW, scale_factor=1.08), run_time=1.2)
        self.at("What must the gills")
        card = RoundedRectangle(corner_radius=0.12, width=5.1, height=0.75, color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(P(-2.4, 3.4))
        qt = T("gills: pump salt in or out?", 28, YELLOW).move_to(card)
        self.play(FadeIn(card), FadeIn(qt), run_time=1.0)
        self.play(Indicate(w.gl, color=YELLOW, scale_factor=1.1), run_time=1.5)
        self.finish()


class S11Pause(SpokenScene):
    def construct(self):
        w = river_state(self, dict(wi=0.9, wo=0.9, si=0, so=0, ws="ok", ss="bad", cap="", capc=RED), strip=False)
        w.water.set_opacity(0.5)
        urine = urine_stream()
        ul = T("dilute\nurine", 26, BLUE).move_to(P(-6.0, -2.55))
        u, g = urine_boxes()
        card = RoundedRectangle(corner_radius=0.12, width=5.1, height=0.75, color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(P(-2.4, 3.4))
        qt = T("gills: pump salt in or out?", 28, YELLOW).move_to(card)
        self.add(urine, ul, u, g, card, qt)
        ring_c = P(0.75, 3.4)
        base = Circle(radius=0.28, color=OUTL, stroke_width=4).move_to(ring_c)
        prog = ValueTracker(1.0)
        arc = always_redraw(lambda: Arc(radius=0.28, start_angle=PI / 2, angle=max(prog.get_value(), 0.001) * TAU, arc_center=ring_c,
                                       color=YELLOW, stroke_width=7))
        self.add(base, arc)
        self.play(prog.animate.set_value(0.0), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        w = river_state(self, dict(wi=0.9, wo=0.9, si=0, so=0, ws="ok", ss="bad", cap="", capc=RED), strip=False)
        w.water.set_opacity(0.5)
        urine = urine_stream()
        ul = T("dilute\nurine", 26, BLUE).move_to(P(-6.0, -2.55))
        u, g = urine_boxes()
        card = RoundedRectangle(corner_radius=0.12, width=5.1, height=0.75, color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(P(-2.4, 3.4))
        qt = T("gills: pump salt in or out?", 28, YELLOW).move_to(card)
        self.add(urine, ul, u, g, card, qt)
        self.at("Take it in")
        ans = T("in", 34, ORANGE, weight=BOLD).move_to(card)
        self.play(FadeOut(qt), FadeIn(ans), run_time=0.8)
        self.at("Gill cells pull")
        self.play(FadeOut(ans), FadeOut(card), run_time=0.5)
        pump = solid_pair("bony", BOT_S, -1, "in", tag=False)
        self.play(Create(pump), run_time=1.2)
        self.play(*w.ledger.anim(si=0.9), run_time=1.3)
        self.at("against the leak")
        self.play(Indicate(w.salt, color=YELLOW, scale_factor=1.08), run_time=1.3)
        self.at("Again")
        tag = atp_chip(22, 0.09).move_to(P(-2.55, -2.1)).set_z_index(7)
        self.play(FadeIn(tag, scale=1.2), *w.ledger.anim(ss="ok", cap="balanced", capc=GREEN), run_time=0.9)
        self.play(w.ledger.cap.animate.shift(LEFT * 1.1), run_time=0.3)
        a = chip("SEA: salt out", ORANGE, size=24)
        b = chip("RIVER: salt in", ORANGE, size=24)
        both = VGroup(a, b).arrange(RIGHT, buff=0.3).move_to(P(-2.3, 3.35))
        self.play(FadeIn(both, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


def shark_world(stack=(450, 0, 0), body=450, flow_dir="out", ledger=None, green=False, tmao=False):
    w = World(fish="shark", water="sea", label="SEA", bar=(body, 1000), stack=stack, flow_dir=flow_dir, body_n=8, tank_n=24)
    w.bar.set_labels("body", "outside")
    if ledger:
        w.ledger.set(**ledger)
    return w


class S13Shark(SpokenScene):
    def construct(self):
        w = river_state(self, dict(wi=0.9, wo=0.9, si=0.9, so=0.9, ws="ok", ss="ok", cap="balanced", capc=GREEN))
        pump = solid_pair("bony", BOT_S, -1, "in")
        urine = urine_stream()
        ul = T("dilute\nurine", 26, BLUE).move_to(P(-6.0, -2.55))
        self.add(pump, urine, ul)
        self.at("One more tank")
        old = list(self.mobjects)
        self.play(*[FadeOut(m) for m in old], run_time=0.8)
        sw = shark_world(stack=(0, 0, 0), body=0, ledger=dict(wi=0, wo=0, si=0, so=0, ws="none", ss="none", cap=""))
        sw.bar.bt.set_value(0)
        parts = sw.parts_list(pointers=False, flow=False) + [sw.bar.tri_o, sw.bar.lab_o]
        self.play(*[FadeIn(m) for m in parts], run_time=1.2)
        self.at("A shark lives")
        self.play(Indicate(sw.fish, color=WHITE, scale_factor=1.04), run_time=1.5)
        self.at("its blood holds less salt")
        sl = sw.bar.seg_labels()
        self.play(sw.bar.seg_t[0].animate.set_value(450), sw.bar.bt.animate.set_value(450), FadeIn(sw.bar.tri_b), FadeIn(sw.bar.lab_b),
                  FadeIn(sw.flow), FadeIn(sl[0]), run_time=1.4)
        self.at("than seawater")
        self.play(Indicate(sw.bar.lab_o, color=YELLOW, scale_factor=1.12), run_time=1.0)
        self.at("Yet it does not lose water")
        self.play(Indicate(sw.fish, color=BLUE, scale_factor=1.04), run_time=1.5)
        self.at("Why not")
        q = T("?", 96, YELLOW, weight=BOLD).move_to(P(-0.2, 2.1))
        self.play(FadeIn(q, scale=0.5), run_time=0.8)
        self.finish()


def shark_state(sc, stack, body, ledger=None, q=False, labels=("salts",)):
    w = shark_world(stack=stack, body=body, ledger=ledger)
    w.add_to(sc)
    sl = w.bar.seg_labels()
    for i, t in enumerate(sl):
        if stack[i] > 0:
            sc.add(t)
    w.sl = sl
    return w


class S14Urea(SpokenScene):
    def construct(self):
        w = shark_state(self, (450, 0, 0), 450, dict(wi=0, wo=0, si=0, so=0, ws="none", ss="none", cap=""))
        ur = jitter(26, *w.body_box, GREEN, 21, 0.35, r=0.08, z=3)
        ur.set_opacity(0)
        self.add(ur)
        self.at("Its blood also carries")
        self.play(ur.animate.set_opacity(0.95), w.bar.seg_t[1].animate.set_value(500), w.bar.bt.animate.set_value(950),
                  FadeIn(w.sl[1]), run_time=3.0)
        self.at("which the shark makes")
        self.play(Indicate(ur, color=GREEN, scale_factor=1.08), run_time=1.5)
        self.at("A little")
        tm = jitter(6, *w.body_box, TMAO_C, 33, 0.35, r=0.08, z=3)
        tm.set_opacity(0)
        self.add(tm)
        self.play(tm.animate.set_opacity(1), w.bar.seg_t[2].animate.set_value(70), w.bar.bt.animate.set_value(1020),
                  FadeIn(w.sl[2]), run_time=2.0)
        self.at("Both count as dissolved")
        self.play(Indicate(ur, color=GREEN, scale_factor=1.06), Indicate(tm, color=WHITE, scale_factor=1.06), run_time=2.0)
        self.at("With them")
        w.bar.set_labels("body ~1,020", "outside ~1,000")
        self.play(Indicate(w.bar.lab_b, color=YELLOW, scale_factor=1.12), run_time=1.5)
        self.play(Indicate(w.bar.lab_o, color=YELLOW, scale_factor=1.12), run_time=1.3)
        self.finish()


class S15Trickle(SpokenScene):
    def construct(self):
        w = shark_state(self, (450, 500, 70), 1020, dict(wi=0, wo=0, si=0, so=0, ws="none", ss="none", cap=""))
        w.bar.set_labels("body ~1,020", "outside ~1,000")
        ur = jitter(26, *w.body_box, GREEN, 21, 0.35, r=0.08, z=3)
        tm = jitter(6, *w.body_box, TMAO_C, 33, 0.35, r=0.08, z=3)
        self.add(ur, tm)
        self.at("So the water leak")
        self.play(w.flip_flow(), run_time=1.0)
        tr = arrows("shark", TOP_W, 1, "in", BLUE, period=5.0)
        self.at("as a slow trickle")
        self.play(Create(tr), *w.ledger.anim(wi=0.2), run_time=1.5)
        self.at("The shark need not")
        path = drink_path()
        self.play(FadeIn(path), run_time=0.8)
        dl = T("drinking", 26, YELLOW).move_to(P(-1.2, -2.35))
        x = VGroup(Line(P(-0.5, 0.2), P(0.2, -0.5), color=RED, stroke_width=10), Line(P(-0.5, -0.5), P(0.2, 0.2), color=RED, stroke_width=10)).set_z_index(9)
        self.at("drink seawater")
        self.play(FadeIn(dl), Create(x), run_time=1.0)
        self.finish()


def mini(kind, x0):
    """A small tank, bar and ledger column; labels are left out of the small copies."""
    if kind == "sea":
        w = World(fish="bony", water="sea", label=None, labels=False, bar=(350, 1000), body_n=6, tank_n=14)
        water, salt = sea_leaks()
    elif kind == "river":
        w = World(fish="bony", water="river", label=None, labels=False, bar=(300, 5), body_n=14, tank_n=2)
        water, salt = river_leaks()
    else:
        w = World(fish="shark", water="sea", label=None, labels=False, bar=(1020, 1000), stack=(450, 500, 70), body_n=8, tank_n=14)
        water, salt = arrows("shark", TOP_W, 1, "in", BLUE, period=5.0), arrows("shark", TOP_S, 1, "in", ORANGE)
    w.ledger.set(wi=0, wo=0, si=0, so=0, ws="none", ss="none")
    tank = VGroup(w.tank, water, salt)
    tank.scale(0.55, about_point=P(-3.2, 0)).shift(P(x0 + 3.2, 1.4))
    L, B = w.ledger.parts, w.bar.parts
    L.scale(0.6, about_point=w.ledger.panel.get_center())
    L.shift(P(x0 - 0.25, -1.95) - w.ledger.panel.get_center())
    B.scale(0.6, about_point=w.bar.frame.get_center())
    B.shift(P(x0 + 1.95, -1.9) - w.bar.frame.get_center())
    w.water, w.salt, w.tank_g = water, salt, tank
    return w


def tx(g, x0):
    return g.scale(0.55, about_point=P(-3.2, 0)).shift(P(x0 + 3.2, 1.4))


class S16Close(SpokenScene):
    def construct(self):
        xs = [-4.5, 0.0, 4.5]
        names = ["bony fish, sea", "bony fish, river", "shark, sea"]
        ws = [mini(k, x) for k, x in zip(["sea", "river", "shark"], xs)]
        labs = [T(nm, 28, TEXT).move_to(P(x, 3.5)) for nm, x in zip(names, xs)]
        items = []
        for w, lab in zip(ws, labs):
            items += [w.tank_g, w.ledger.parts, w.bar.parts, lab]
        self.play(*[FadeIn(m) for m in items], run_time=1.0)
        self.at("one budget")
        self.play(*[Indicate(w.tank_g[0][1], color=WHITE, scale_factor=1.03) for w in ws], run_time=1.2)
        self.at("The gap between body")
        self.play(*[Indicate(w.water, color=YELLOW, scale_factor=1.05) for w in ws], run_time=1.6)
        self.play(*[Indicate(w.salt, color=YELLOW, scale_factor=1.05) for w in ws], run_time=1.6)
        self.at("Drinking, urine")
        sea_r = tx(VGroup(drink_path(), solid_pair("bony", BOT_S, -1, "out", tag=False)), -4.5)
        riv_r = tx(VGroup(urine_stream(), solid_pair("bony", BOT_S, -1, "in", tag=False)), 0.0)
        tag1 = atp_chip(28, 0.05).move_to(tx(Dot(P(-2.55, -2.1)), -4.5).get_center()).set_z_index(8)
        tag2 = atp_chip(28, 0.05).move_to(tx(Dot(P(-2.55, -2.1)), 0.0).get_center()).set_z_index(8)
        self.play(FadeIn(sea_r), FadeIn(riv_r), run_time=0.9)
        self.play(FadeIn(tag1), FadeIn(tag2), run_time=0.5)
        self.at("close each gap")
        w1, w2, w3 = ws
        self.play(*w1.ledger.anim(wi=0.9, wo=0.9, si=0.85, so=0.85, ws="ok", ss="ok"),
                  *w2.ledger.anim(wi=0.9, wo=0.9, si=0.9, so=0.9, ws="ok", ss="ok"),
                  *w3.ledger.anim(wi=0.2, si=0.4), run_time=1.6)
        cap = T("total gains = total losses", 30, YELLOW).move_to(P(-2.3, -3.6))
        stamp = T("incomplete here:\noutput routes in the lesson", 22, RED).move_to(P(4.5, -3.35))
        self.play(FadeIn(cap), FadeIn(stamp), run_time=0.8)
        self.finish()


class S17End(EndCard):
    LINE = "Gains must equal losses, for water and each salt."
