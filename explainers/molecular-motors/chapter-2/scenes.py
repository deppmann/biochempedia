"""Turning Motion Into a Measurement: molecular motors, chapter 2.

Same colour map as chapter 1.
  BLUE   microtubule (the track)
  ORANGE kinesin-1
  YELLOW cargo / the trapped bead
  GREEN  ATP
  RED    force, load, the trap's spring
  TEXT   annotations, outlines, the laser trap
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
STEP = 0.6          # one 8 nm step, in scene units (schematic)
SPECK = "#BFEBF5"


# ---------------------------------------------------------------- small helpers
def sstep(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def lab(text, x, y, size=28, color=TEXT, weight=NORMAL):
    return T(text, size, color, weight=weight).move_to([x, y, 0])


def schem():
    return T("schematic", 24, TEXT).move_to([5.75, -3.62, 0]).set_z_index(20)


class Sc(SpokenScene):
    def until(self, t):
        r = t - self.renderer.time
        if r > 0.02:
            self.wait(r)


def microtubule(y=-1.15, width=12.2, tiles=16):
    bar = RoundedRectangle(width=width, height=1.24, corner_radius=0.24, stroke_color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=0.58).move_to([0, y, 0])
    xs = np.linspace(-width / 2 + 0.42, width / 2 - 0.42, tiles)
    marks = VGroup(*[VGroup(Line([x - .18, y - .22, 0], [x + .10, y, 0]), Line([x + .10, y, 0], [x - .18, y + .22, 0]))
                     .set_stroke(BLUE, 4) for x in xs])
    return VGroup(bar, marks)


def cycle_dial(center=(4.55, 2.15, 0), radius=1.18, size=28):
    rr = radius * .45
    ring = Circle(radius=rr, color=GREY, stroke_width=2).move_to(center)
    labs = VGroup(
        T("GRIP", size, ORANGE).move_to(np.array(center) + UP * (rr + .4)),
        T("SWING", size, ORANGE).move_to(np.array(center) + RIGHT * (rr + .95)),
        T("LET GO", size, ORANGE).move_to(np.array(center) + DOWN * (rr + .4)),
        T("RE-COCK", size, ORANGE).move_to(np.array(center) + LEFT * (rr + 1.15)),
    )
    pointer = Arrow(center, np.array(center) + UP * (rr - .05), buff=0, color=YELLOW, stroke_width=4, tip_length=.14)
    return VGroup(ring, labs, pointer)


def shimmer(track, color=TEXT, op=.5):
    d = RoundedRectangle(width=1.35, height=max(.5, track.height * .8), corner_radius=.12, stroke_width=0,
                         fill_color=color, fill_opacity=op)
    d.t = 0.0

    def move(m, dt):
        m.t = (m.t + dt * .12) % 1
        L, W = track.get_left()[0] + .2, track.width - .4
        m.move_to([L + W * m.t, track.get_center()[1], 0])
    d.add_updater(move)
    move(d, 0)
    return d


# ---------------------------------------------------------------- walker (free or clamped)
def walker(bx, contact, up=1, mode="free", s=1.0, L=1.7, cargo_r=0.0, P=4.0, v=.16, t0=0.0, on=True):
    """Schematic two-foot motor. contact = y of the track surface; up = +1 when the tail is above the
    contact (free motor), -1 when the tail points down to the glass (clamped, feet face up)."""
    fw, fh = .5 * s, .3 * s

    def mk():
        return RoundedRectangle(width=fw, height=fh, corner_radius=.1 * s, stroke_color=ORANGE, stroke_width=3,
                                fill_color=ORANGE, fill_opacity=.55)
    feet = [mk(), mk()]
    legs = [Line(LEFT, RIGHT, color=ORANGE, stroke_width=5) for _ in (0, 1)]
    stalk = Line(LEFT, RIGHT, color=ORANGE, stroke_width=6)
    hip = Dot(radius=.13 * s, color=ORANGE)
    parts = [*legs, stalk, hip, *feet]
    cg = None
    if cargo_r:
        cg = Circle(radius=cargo_r, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=.4)
        parts.append(cg)
    g = VGroup(*parts)
    g.t, g.on, g.bx = t0, on, bx
    swing = v * P
    a = v * P / 4

    def pose(m):
        xs, ys = [], []
        for k in (0, 1):
            if mode == "free":
                u = m.t / P + (0.5 if k == 0 else 0.0)
                n = math.floor(u)
                f = u - n
                w = swing / 4
                rel = (-w if k == 0 else w)
                if f >= .5:
                    sw = (f - .5) * 2
                    x = bx + rel + swing * (n + sstep(sw))
                    lift = .3 * s * math.sin(math.pi * sw)
                else:
                    x = bx + rel + swing * n
                    lift = 0.0
            else:
                u = m.t / P + (0.0 if k == 0 else 0.5)
                n = math.floor(u)
                f = u - n
                off = (-.5 * s if k == 0 else .5 * s)
                if f < .5:
                    x = bx + off + a - 2 * a * (f * 2)
                    lift = 0.0
                else:
                    sw = (f - .5) * 2
                    x = bx + off - a + 2 * a * sstep(sw)
                    lift = .3 * s * math.sin(math.pi * sw)
            xs.append(x)
            ys.append(contact + up * (fh / 2 + lift))
        mx = (xs[0] + xs[1]) / 2
        hx = mx if mode == "free" else bx + (mx - bx) * .5
        hy = contact + up * L * .58
        tail = np.array([hx if mode == "free" else bx, contact + up * L, 0])
        hip.move_to([hx, hy, 0])
        stalk.put_start_and_end_on([hx, hy, 0], tail)
        for k in (0, 1):
            feet[k].move_to([xs[k], ys[k], 0])
            legs[k].put_start_and_end_on([hx, hy, 0], [xs[k], ys[k], 0])
        if cg is not None:
            cg.move_to([hx, contact + up * (L + cargo_r * .85), 0])

    def upd(m, dt):
        if m.on:
            m.t += dt
        pose(m)
    g.add_updater(upd)
    pose(g)
    return g


# ---------------------------------------------------------------- the carried field (end of s00, behind the title)
FIELD_C = np.array([0, .1, 0])


def field_parts(op=1.0):
    fc = Circle(radius=3.45, stroke_color=TEXT, stroke_width=4, fill_color="#07090d", fill_opacity=1).move_to(FIELD_C)
    fc.set_z_index(-1)
    ftr = microtubule(0, 12.2, 16).scale(.42).move_to(FIELD_C)
    fd = VGroup(Circle(radius=.30, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=.18),
                Dot(radius=.1, color=ORANGE)).set_z_index(5)
    fd.t = 0.0

    def drift(m, dt):
        m.t += dt
        m.move_to([.55 * math.sin(.4 * m.t), .1 + .02 * math.sin(.9 * m.t), 0])
    fd.add_updater(drift)
    drift(fd, 0)
    q = T("?", 170, YELLOW).set_opacity(.3).move_to(FIELD_C).set_z_index(1)
    for m in (fc, ftr, q):
        m.set_opacity(op * (m.get_fill_opacity() if hasattr(m, "get_fill_opacity") else 1)) if False else None
    return fc, ftr, fd, q


# ---------------------------------------------------------------- gliding chamber
GTOP = -2.5
CONTACT = .2           # y of the track's lower surface above the clamped motors
TRK_Y = .7
TRK_W = 10.4
TRK_X0 = 1.3
MX = [-3.6, -1.6, .4, 2.4]
VG = .16               # glide speed (units per second)
PER = 4.0


def glide_track(cx=TRK_X0, y=TRK_Y, w=TRK_W, h=1.0, speckle=True):
    glow = RoundedRectangle(width=w + .3, height=h + .3, corner_radius=.3, stroke_width=0, fill_color=BLUE,
                            fill_opacity=.16)
    bar = RoundedRectangle(width=w, height=h, corner_radius=.24, stroke_color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=.58)
    parts = [glow, bar]
    if speckle:
        rng = np.random.RandomState(4)
        xs = np.cumsum(rng.uniform(.55, 1.15, 12)) - w / 2 + .1
        for x in xs:
            if x < w / 2 - .2:
                parts.append(Dot([x, rng.uniform(-.22, .22), 0], radius=.07, color=SPECK).set_opacity(.85))
    g = VGroup(*parts).move_to([cx, y, 0])
    g.on = True
    g.v = VG

    def upd(m, dt):
        if m.on:
            m.shift(LEFT * m.v * dt)
    g.add_updater(upd)
    return g


def glass_strip(y=-3.15, h=1.3):
    return Rectangle(width=14.2, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=.3).move_to([0, y, 0])


def clamp_pad(x, y=GTOP):
    return RoundedRectangle(width=.62, height=.2, corner_radius=.06, stroke_color=TEXT, stroke_width=2,
                            fill_color=GREY, fill_opacity=.9).move_to([x, y - .06, 0]).set_z_index(4)


def chamber(cx=TRK_X0, on=False, ghost=1.0):
    glass = glass_strip()
    tr = glide_track(cx)
    tr.on = on
    ws = [walker(x, CONTACT, -1, "clamped", 1.0, L=CONTACT - GTOP, P=PER, v=VG, t0=1.1 * i, on=on) for i, x in enumerate(MX)]
    pads = [clamp_pad(x) for x in MX]
    return glass, tr, ws, pads


def end_marks(tr):
    circ = Circle(radius=.3, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=.35).set_z_index(6)
    tri = Triangle(color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=.35).scale(.34).rotate(-PI / 2).set_z_index(6)
    bar = tr[1]

    def follow(m, dt):
        circ.move_to([bar.get_left()[0] + .5, bar.get_center()[1], 0])
        tri.move_to([bar.get_right()[0] - .5, bar.get_center()[1], 0])
    circ.add_updater(follow)
    follow(circ, 0)
    return circ, tri


# ---------------------------------------------------------------- the trapped-bead rig
XC = -4.6


def make_rig(xc=XC, ty=-3.0, sc=1.0, tw=12.9, tx=0.0, drive=None, xs=0.0, d=0.0, fid=0.0, wob=1.0, aoff=1.6,
             tcolor=BLUE):
    TH = .7 * sc
    track = RoundedRectangle(width=tw, height=TH, corner_radius=.2 * sc, stroke_color=tcolor, stroke_width=4,
                             fill_color=tcolor, fill_opacity=.58).move_to([tx, ty, 0])
    top = ty + TH / 2
    fw, fh = .5 * sc, .32 * sc
    feet = [RoundedRectangle(width=fw, height=fh, corner_radius=.12 * sc, stroke_color=ORANGE, stroke_width=3,
                             fill_color=ORANGE, fill_opacity=.55).set_z_index(3) for _ in (0, 1)]
    legs = [Line(LEFT, RIGHT, color=ORANGE, stroke_width=5).set_z_index(2) for _ in (0, 1)]
    stalk = Line(LEFT, RIGHT, color=ORANGE, stroke_width=6).set_z_index(2)
    hip = Dot(radius=.12 * sc, color=ORANGE).set_z_index(3)
    bead = Circle(radius=.65 * sc, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=.45).set_z_index(3)
    R = VGroup(track, *legs, stalk, hip, *feet, bead)
    R.t, R.drive, R.xs, R.d, R.fid, R.wob = 0.0, drive, xs, d, fid, wob
    R.sc, R.xc, R.ty = sc, xc, ty
    R.track, R.bead = track, bead
    R.kt = ValueTracker(1.0)
    # extras (added to the scene separately; they follow the same state)
    R.cone = Polygon([0, 0, 0], [1, 0, 0], [0, 1, 0], stroke_color=TEXT, stroke_width=2, stroke_opacity=.35,
                     fill_color=TEXT, fill_opacity=.11).set_z_index(1)
    R.ring = VGroup(Circle(radius=.26 * sc, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=.18),
                    Circle(radius=.42 * sc, stroke_color=TEXT, stroke_width=2, stroke_opacity=.4)).set_z_index(4)
    R.arrow = Arrow(LEFT, RIGHT, buff=0, color=RED, stroke_width=6).set_z_index(5)
    R.coil = VMobject(stroke_color=RED, stroke_width=5).set_z_index(4)
    R.aoff = aoff

    def bead_y(m):
        return m.ty + 2.15 * m.sc

    def pose(m):
        if m.drive:
            m.xs, m.d = m.drive(m.t)
        adv = m.xs + m.d
        sc_ = m.sc
        fx, fy = [], []
        for k in (0, 1):
            u = adv / (2 * STEP) - (0.5 if k else 0.0)
            n = math.floor(u)
            f = u - n
            s_ = min(1.0, 2 * f)
            rel = (STEP / 2 if k else -STEP / 2) + 2 * STEP * (n + sstep(s_))
            lift = .3 * math.sin(math.pi * s_) if 0 < s_ < 1 else 0.0
            if m.fid:
                ph = 2.3 * m.t + k * math.pi
                lift += m.fid * .16 * max(0.0, math.sin(ph))
                rel += m.fid * .05 * math.sin(ph)
            fx.append(m.xc + sc_ * rel)
            fy.append(top + fh / 2 + sc_ * lift)
        hx, hy = (fx[0] + fx[1]) / 2, top + .8 * sc_
        bxw = m.wob * sc_ * (.1 * math.sin(7.1 * m.t) + .07 * math.sin(11.3 * m.t + 1))
        byw = m.wob * sc_ * .08 * math.sin(5.3 * m.t + 2)
        bx, by = m.xc + sc_ * adv + bxw, bead_y(m) + byw
        m.bead.move_to([bx, by, 0])
        hip.move_to([hx, hy, 0])
        stalk.put_start_and_end_on([hx, hy, 0], [bx, by - .65 * sc_, 0])
        for k in (0, 1):
            feet[k].move_to([fx[k], fy[k], 0])
            legs[k].put_start_and_end_on([hx, hy, 0], [fx[k], fy[k], 0])
        # trap
        rx, ry = m.xc + sc_ * m.xs, bead_y(m)
        m.ring.move_to([rx, ry, 0])
        k_ = m.kt.get_value()
        topy = (3.75 * (1 - k_) + (ry + 1.0 * sc_) * k_)
        hw = (3.2 * (1 - k_) + 1.1 * sc_ * k_)
        m.cone.set_points_as_corners([[rx - hw, topy, 0], [rx + hw, topy, 0], [rx + .12 * sc_, ry, 0],
                                      [rx - .12 * sc_, ry, 0], [rx - hw, topy, 0]])
        # force arrow and coil (displacement of the bead from the trap centre)
        L = sc_ * m.d
        ay = ry + sc_ * m.aoff
        if L > .35:
            tip = min(.34, .45 * L)
            new = Arrow([bx, ay, 0], [rx + .02, ay, 0], buff=0, color=RED, stroke_width=3 + 2.0 * m.d,
                        tip_length=tip, max_tip_length_to_length_ratio=.5)
            m.arrow.become(new)
            m.arrow.set_opacity(1)
        else:
            m.arrow.set_opacity(0)
        x0, x1 = rx + .3 * sc_, bx - .65 * sc_
        if x1 - x0 > .5:
            n_z = 12
            xs_ = np.linspace(x0, x1, 2 * n_z + 1)
            pts = [[xs_[0], ry, 0]]
            for i in range(1, 2 * n_z):
                pts.append([xs_[i], ry + (.2 * sc_ if i % 2 else -.2 * sc_), 0])
            pts.append([xs_[-1], ry, 0])
            m.coil.set_points_as_corners(pts)
        else:
            m.coil.set_points_as_corners([[x0, ry, 0], [x0 + .01, ry, 0]])

    def upd(m, dt):
        m.t += dt
        pose(m)
    R.add_updater(upd)
    R.pose = pose
    pose(R)
    return R


def add_rig(scene, R, *extra, shim=True):
    R.t = scene.renderer.time
    scene.add(R, *extra)
    if shim:
        scene.add(shimmer(R.track, TEXT, .22))


def stairs(ts, d0, step=STEP, w=.35):
    return lambda t: (0.0, d0 + step * sum(sstep((t - s) / w) for s in ts))


def clamps_pair(y=-3.0):
    return VGroup(*[RoundedRectangle(width=.5, height=.8, corner_radius=.08, stroke_color=TEXT, stroke_width=3,
                                     fill_color=GREY, fill_opacity=.85).move_to([x, y + .05, 0]).set_z_index(6)
                    for x in (-6.2, 6.2)])


# ---------------------------------------------------------------- graph
GX0, GY0 = -4.0, .55
GRISE = .55            # graph units per step
GXS = .39              # graph units per second


def graph_frame():
    xa = Arrow([GX0, GY0, 0], [GX0 + 7.4, GY0, 0], buff=0, color=TEXT, stroke_width=3, tip_length=.2)
    ya = Arrow([GX0, GY0, 0], [GX0, GY0 + 3.1, 0], buff=0, color=TEXT, stroke_width=3, tip_length=.2)
    tl = lab("time", GX0 + 6.8, GY0 - .38)
    yl = lab("bead position", GX0 - .42, GY0 + 1.7).rotate(PI / 2)
    return VGroup(xa, ya, tl, yl)


def make_trace(R, d_ref, tmax=None, color=YELLOW, x0=GX0, y0=GY0, xs=GXS, rise=GRISE):
    tr = VMobject(stroke_color=color, stroke_width=6).set_z_index(5)
    dot = Dot(radius=.12, color=color).set_z_index(6)

    def upd(m, dt):
        t = R.t if tmax is None else min(R.t, tmax)
        n = max(2, int(t / .1) + 2)
        ts = np.linspace(0, max(t, .001), n)
        pts = [[x0 + xs * tt, y0 + (R.drive(tt)[1] - d_ref) / STEP * rise, 0] for tt in ts]
        m.set_points_as_corners(pts)
        dot.move_to(pts[-1])
    tr.add_updater(upd)
    upd(tr, 0)
    return tr, dot


def vgauge(x, y0, h, color=RED, w=.5):
    frame = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3).move_to([x, y0 + h / 2, 0])
    fill = Rectangle(width=w - .1, height=.02, stroke_width=0, fill_color=color, fill_opacity=.85)
    fill.val = lambda: 0.0

    def upd(m, dt):
        v = max(.01, min(1.0, m.val()))
        m.become(Rectangle(width=w - .1, height=h * v, stroke_width=0, fill_color=color, fill_opacity=.85)
                 .move_to([x, y0 + h * v / 2, 0]))
    fill.add_updater(upd)
    upd(fill, 0)
    g = VGroup(frame, fill)
    g.fill = fill
    return g


def clamp_icon(x, y):
    c = VGroup(Arc(radius=.34, start_angle=PI / 2, angle=PI).set_stroke(TEXT, 9),
               Line([0, .34, 0], [.38, .34, 0]).set_stroke(TEXT, 9), Line([0, -.34, 0], [.38, -.34, 0]).set_stroke(TEXT, 9),
               Line([.1, .62, 0], [.1, .34, 0]).set_stroke(TEXT, 6))
    c.set_z_index(15)
    return c.move_to([x, y, 0])


# ================================================================= scenes
class S00Link(Sc):
    def construct(self):
        tr = microtubule(-1.75, 12.2, 16)
        glint = shimmer(tr[0], BLUE)
        w = walker(-4.2, -1.13, 1, "free", 1.6, L=2.7, cargo_r=.85, P=3.6, v=.42)
        dial = cycle_dial((4.55, 2.35, 0), 1.18, 28)
        ptr = dial[2]
        ptr.add_updater(lambda m, dt: m.rotate(-dt * TAU / 4.6, about_point=dial[0].get_center()))
        self.add(tr, glint, w, dial, schem())
        for ph, i in (("gripping", 0), ("swinging", 1), ("releasing", 2), ("resetting", 3)):
            self.at(ph)
            self.play(Indicate(dial[1][i], color=YELLOW), run_time=.6)
        self.at("too small")
        fc, ftr, fd, q = field_parts()
        self.remove(glint)
        ptr.clear_updaters()
        self.play(FadeOut(w), FadeOut(dial), ReplacementTransform(tr, ftr), FadeIn(fc), run_time=1.6)
        self.add(fd, shimmer(ftr[0], BLUE))
        self.play(GrowFromCenter(q), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Molecular Motors and Cargo"
    TITLE = "Turning Motion Into a Measurement"

    def construct(self):
        fc, ftr, fd, q = field_parts()
        field = VGroup(fc, ftr, q)
        field.set_opacity(.22)
        fd.set_opacity(.4)
        self.add(field, fd, shimmer(ftr[0], BLUE, .2), schem())
        super().construct()


class S02GlidingSetup(Sc):
    def construct(self):
        fc, ftr, fd, q = field_parts()
        field = VGroup(fc, ftr, q)
        field.set_opacity(.22)
        fd.set_opacity(.4)
        sh = shimmer(ftr[0], BLUE, .2)
        self.add(field, fd, sh, schem())
        glass, tr, ws, pads = chamber(on=False)
        for k, wk in enumerate(ws):
            wk.on = False
        tr.on = False
        self.at("gliding assay")
        gl = lab("glass coverslip", -4.5, -3.3)
        self.remove(sh)
        self.play(FadeOut(field), FadeOut(fd), FadeIn(glass, shift=UP * .8), run_time=1.6)
        self.at("purified motors")
        for wk in ws:
            wk.shift(UP * 2.2)
        self.play(*[AnimationGroup(FadeIn(wk, shift=DOWN * 0), wk.animate.shift(DOWN * 2.2), run_time=1.0) for wk in ws],
                  run_time=1.0)
        self.at("fastened by their tails")
        self.play(*[FadeIn(p) for p in pads], run_time=.7)
        self.play(*[Indicate(p, color=YELLOW, scale_factor=1.3) for p in pads], run_time=.7)
        self.at("glass cover slip")
        self.play(FadeIn(gl), run_time=.6)
        self.at("add fluorescent tracks")
        tl = lab("fluorescent track", 0.0, 2.05, 28, BLUE)
        tr.shift(UP * 1.2)
        self.play(FadeIn(tr), tr.animate.shift(DOWN * 1.2), FadeIn(tl), run_time=1.0)
        self.at("a tp")
        chips = VGroup(*[chip("ATP", GREEN, 26) for _ in range(4)])
        pos = [(-5.2, 3.2), (-1.8, 2.9), (1.8, 3.3), (5.0, 3.0)]
        vel = [(.22, -.05), (.18, .04), (-.2, -.06), (-.24, .05)]
        lanes = [(-6.0, -4.2), (-3.4, -1.1), (1.1, 3.4), (4.2, 6.0)]
        for c, p, v, ln in zip(chips, pos, vel, lanes):
            c.move_to([p[0], p[1], 0])
            c.vel = v
            c.lane = ln
            c.t = 0.0

            def drift(m, dt):
                m.shift([m.vel[0] * dt, m.vel[1] * dt, 0])
                x, y = m.get_center()[:2]
                if x > m.lane[1]:
                    m.vel = (-abs(m.vel[0]), m.vel[1])
                if x < m.lane[0]:
                    m.vel = (abs(m.vel[0]), m.vel[1])
                if y > 3.3:
                    m.vel = (m.vel[0], -abs(m.vel[1]))
                if y < 2.75:
                    m.vel = (m.vel[0], abs(m.vel[1]))
            c.add_updater(drift)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * .3) for c in chips], lag_ratio=.25), run_time=1.4)
        self.at("motors cannot travel")
        self.play(*[Indicate(p, color=YELLOW, scale_factor=1.4) for p in pads], run_time=.8)
        self.at("their feet can still walk")
        for wk in ws:
            wk.on = True
        tr.on = True
        self.play(Indicate(VGroup(*[wk[-1] for wk in ws]), color=YELLOW), run_time=.7)
        self.at("a fluorescence microscope")
        self.play(FadeOut(tl), run_time=.3)
        bx0, bx1, by0, by1 = -5.4, 5.4, -.15, 1.75
        corners = VGroup()
        for sx, sy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
            cx_, cy_ = (bx1 if sx > 0 else bx0), (by1 if sy > 0 else by0)
            corners.add(VGroup(Line([cx_, cy_, 0], [cx_ - sx * .55, cy_, 0]), Line([cx_, cy_, 0], [cx_, cy_ - sy * .55, 0]))
                        .set_stroke(TEXT, 5))
        ml = lab("microscope", 0, 2.05)
        self.play(Create(corners), FadeIn(ml), run_time=1.4)
        self.at("each motor is far too small")
        self.play(*[wk.animate.set_opacity(.3) for wk in ws], *[p.animate.set_opacity(.3) for p in pads], run_time=1.2)
        self.finish()


class S03FrameFlip(Sc):
    def construct(self):
        glass, tr, ws, pads = chamber(cx=-2.3, on=True)
        for wk in ws:
            wk.on = True
        chips = VGroup()
        self.add(glass, tr, *ws, *pads, schem())
        # the chamber folds into the lower panel
        g2 = Rectangle(width=14.2, height=.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.3).move_to([0, -3.5, 0])
        tr2 = glide_track(1.0, y=-1.3, w=11.0, h=.7)
        tr2.on = False
        w2 = walker(.4, -.95 - .35 + 0.0, -1, "clamped", 1.0, L=-.95 - .35 + 3.2, P=PER, v=VG, on=False)
        # lower panel: glass top at -3.2, tail there, contact at track lower surface (-1.65)
        w2 = walker(.4, -1.65, -1, "clamped", 1.0, L=1.55, P=PER, v=VG, on=False)
        pad2 = clamp_pad(.4, -3.2)
        self.play(ReplacementTransform(glass, g2), ReplacementTransform(tr, tr2),
                  FadeOut(VGroup(*ws)), FadeOut(VGroup(*pads)), FadeIn(w2), FadeIn(pad2), run_time=.8)
        veil = Rectangle(width=14.4, height=3.2, stroke_width=0, fill_color=BG, fill_opacity=.68).move_to([0, -2.2, 0]).set_z_index(12)
        self.add(veil)
        # the free motor on its fixed track above
        top_tr = RoundedRectangle(width=12.8, height=.7, corner_radius=.2, stroke_color=BLUE, stroke_width=4,
                                  fill_color=BLUE, fill_opacity=.58).move_to([0, 1.1, 0])
        rng = np.random.RandomState(7)
        sp = VGroup(*[Dot([x, 1.1 + rng.uniform(-.14, .14), 0], radius=.06, color=SPECK).set_opacity(.85)
                      for x in np.linspace(-6, 6, 14)])
        w1 = walker(-2.8, 1.45, 1, "free", 1.0, L=1.6, P=4.0, v=VG, on=False)
        self.at("free motor")
        self.play(FadeIn(top_tr), FadeIn(sp), FadeIn(w1), run_time=.6)
        fl = lab("free motor", -5.0, 2.65)
        fa = Arrow([-5.9, 2.2, 0], [-4.2, 2.2, 0], buff=0, color=TEXT, stroke_width=5)
        self.play(FadeIn(fl), Create(fa), run_time=.4)
        self.at("walks right")
        w1.on = True
        self.at("clamp that motor instead")
        w2.on = True
        tr2.on = True
        self.play(FadeOut(veil), run_time=1.0)
        self.at("every stroke pushes")
        guide = DashedLine([.4, -3.2, 0], [.4, -.6, 0], color=TEXT, stroke_width=3).set_z_index(7)
        la = Arrow([3.2, -.45, 0], [1.2, -.45, 0], buff=0, color=TEXT, stroke_width=6)
        self.play(Create(guide), Create(la), run_time=1.2)
        self.at("the same interaction")
        self.play(Indicate(w1, color=YELLOW), run_time=.8)
        self.at("the other partner")
        self.play(Indicate(tr2[1], color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.finish()


class S04Direction(Sc):
    def construct(self):
        glass, tr, ws, pads = chamber(cx=TRK_X0, on=True)
        for wk in ws:
            wk.on = True
        self.add(glass, tr, *ws, *pads, schem())
        circ, tri = end_marks(tr)
        self.at("mark the")
        self.play(GrowFromCenter(circ), GrowFromCenter(tri), run_time=1.0)
        self.add(circ, tri)
        # ruler + timer
        ruler = VGroup(Line([-6, 2.15, 0], [6, 2.15, 0]).set_stroke(TEXT, 4),
                       *[Line([x, 2.15, 0], [x, 2.15 + (.28 if abs(x * 2 % 2) < .01 else .16), 0]).set_stroke(TEXT, 3)
                         for x in np.arange(-6, 6.01, .5)])
        pointer = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(.16).rotate(PI)
        pointer.add_updater(lambda m, dt: m.move_to([circ.get_center()[0], 2.15 - .22, 0]))
        timer = M("t = 0 s", 30).move_to([-5.2, 3.3, 0])
        timer.t = 0.0
        timer.last = 0

        def tick(m, dt):
            m.t += dt
            s = int(m.t)
            if s != m.last:
                m.last = s
                m.become(M(f"t = {s} s", 30).move_to([-5.2, 3.3, 0]))
        timer.add_updater(tick)
        frame = RoundedRectangle(width=1.7, height=1.7, corner_radius=.15, stroke_color=TEXT, stroke_width=4).set_z_index(8)
        frame.add_updater(lambda m, dt: m.move_to([circ.get_center()[0] - .2, TRK_Y, 0]))
        frame.move_to([circ.get_center()[0] - .2, TRK_Y, 0])
        self.at("which end leads")
        self.play(Create(frame), FadeIn(ruler), FadeIn(pointer), FadeIn(timer), run_time=1.4)
        self.at("because the track glides opposite")
        la = Arrow([2.4, 1.78, 0], [.6, 1.78, 0], buff=0, color=TEXT, stroke_width=6)
        lt = lab("glides", 3.55, 1.78)
        self.play(Create(la), FadeIn(lt), run_time=.9)
        self.at("the motor's walk")
        ra = Arrow([-.5, -3.2, 0], [1.3, -3.2, 0], buff=0, color=TEXT, stroke_width=6).set_z_index(9)
        rt = lab("walks", -1.6, -3.2).set_z_index(9)
        self.play(Create(ra), FadeIn(rt), run_time=.9)
        self.at("that movie reveals direction")
        self.play(Indicate(circ, color=YELLOW, scale_factor=1.4), run_time=1.0)
        self.play(FadeOut(la), FadeOut(lt), FadeOut(ra), FadeOut(rt), run_time=.5)
        self.at("also reports speed")
        box = Rectangle(width=4.5, height=1.25, stroke_color=TEXT, stroke_width=3).move_to([4.35, 3.12, 0])
        ml = lab("many motors", 3.75, 3.42)
        line = VMobject(stroke_color=YELLOW, stroke_width=5)
        t0 = self.renderer.time

        def grow(m, dt):
            e = min(self.renderer.time - t0, 3.2)
            m.set_points_as_corners([[2.3, 2.68, 0], [2.3 + 4.0 * e / 3.2, 2.68 + .6 * e / 3.2 + .001, 0]])
        line.add_updater(grow)
        self.play(Create(box), FadeIn(ml), run_time=.8)
        self.add(line)
        self.at("many motors")
        self.play(Indicate(ml, color=YELLOW), run_time=.8)
        self.finish()


class S05OneMotor(Sc):
    def construct(self):
        glass, tr, ws, pads = chamber(cx=-.9, on=True)
        for wk in ws:
            wk.on = True
        self.add(glass, tr, *ws, *pads, schem())
        circ, tri = end_marks(tr)
        self.add(circ, tri)
        R = make_rig(drive=lambda t: (0.0, .6 * sstep((t - 14.8) / .4)), fid=.6)
        R.kt.set_value(0.0)
        R.remove(R.track)
        R.remove(R.bead)
        clamps = clamps_pair()
        self.at("reverse the geometry")
        tr.on = False
        for wk in ws:
            wk.on = False
        self.play(FadeOut(VGroup(circ, tri)), FadeOut(glass), FadeOut(VGroup(*pads)),
                  ReplacementTransform(tr[1], R.track), FadeOut(tr[0]), FadeOut(VGroup(*tr[2:])),
                  *[wk.animate.shift(DOWN * 1.2).set_opacity(0) for wk in ws], run_time=1.8)
        self.remove(*ws)
        self.at("fix the blue track")
        self.add(shimmer(R.track, TEXT, .22))
        self.play(FadeIn(clamps), run_time=.7)
        self.play(Indicate(clamps, color=YELLOW), run_time=.6)
        self.at("attach one motor")
        R.t = self.renderer.time
        self.play(FadeIn(R), run_time=.9)
        self.at("yellow bead")
        self.play(FadeIn(R.bead, scale=.4), run_time=.8)
        self.at("place that bead")
        self.add(R.cone)
        self.play(FadeIn(R.cone), run_time=1.0)
        self.at("focused laser trap")
        self.play(FadeIn(R.ring), run_time=.8)
        rl = lab("trap centre", -2.2, .5)
        self.play(FadeIn(rl), run_time=.6)
        self.at("most beads")
        self.until(14.8)
        self.at("separating one walker")
        self.play(Indicate(R.bead, color=TEXT, scale_factor=1.12), run_time=1.0)
        self.finish()


def graph_world(scene, d0, d_ref=None, extra=None):
    pass


class S06Predict(Sc):
    def construct(self):
        R = make_rig(d=.6, drive=lambda t: (0.0, .6 + .6 * sstep((t - 2.3) / .4)), fid=.6)
        clamps = clamps_pair()
        add_rig(self, R, R.cone, R.ring, clamps, schem())
        R.kt.set_value(0.0)
        gf = graph_frame()
        self.play(R.kt.animate.set_value(1.0), Create(gf), run_time=1.6)
        self.at("equal jumps")
        self.until(2.6)
        self.at("between them")
        dot = Dot([GX0, GY0, 0], radius=.14, color=YELLOW).set_z_index(6)
        dot.t = 0.0
        dot.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_width(.28 * (1 + .25 * math.sin(4 * m.t)))))
        self.play(FadeIn(dot), run_time=.6)
        self.at("what shape should")
        qc = VGroup(T("smooth ramp", 34, TEXT), T("or staircase?", 34, TEXT)).arrange(DOWN, buff=.15)
        box = RoundedRectangle(corner_radius=.15, width=qc.width + .5, height=qc.height + .4, stroke_color=YELLOW,
                               stroke_width=3, fill_color=YELLOW, fill_opacity=.1)
        qg = VGroup(box, qc).move_to([5.1, 2.6, 0])
        self.play(FadeIn(qg, shift=LEFT * .3), run_time=.8)
        self.at("position record")
        self.play(Indicate(gf[3], color=YELLOW), run_time=.8)
        self.at("pause and predict")
        self.play(Indicate(qg, color=YELLOW), run_time=.9)
        self.finish()


class S07Hold(NarratedScene):
    def construct(self):
        R = make_rig(d=1.2, fid=.6)
        R.kt.set_value(1.0)
        clamps = clamps_pair()
        gf = graph_frame()
        dot = Dot([GX0, GY0, 0], radius=.14, color=YELLOW).set_z_index(6)
        dot.t = 0.0
        dot.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_width(.28 * (1 + .25 * math.sin(4 * m.t)))))
        qc = VGroup(T("smooth ramp", 34, TEXT), T("or staircase?", 34, TEXT)).arrange(DOWN, buff=.15)
        box = RoundedRectangle(corner_radius=.15, width=qc.width + .5, height=qc.height + .4, stroke_color=YELLOW,
                               stroke_width=3, fill_color=YELLOW, fill_opacity=.1)
        qg = VGroup(box, qc).move_to([5.1, 2.6, 0])
        add_rig(self, R, R.cone, R.ring, clamps, schem(), gf, dot, qg)
        self.play(Indicate(qg, color=YELLOW, scale_factor=1.05), run_time=1.6)
        self.play(Indicate(qg, color=YELLOW, scale_factor=1.05), run_time=1.6)
        self.finish()


TS8 = [1.8, 5.0, 9.4, 15.4]
D0 = 1.2


class S08Steps(Sc):
    def construct(self):
        R = make_rig(d=D0, drive=stairs(TS8, D0), fid=.6)
        clamps = clamps_pair()
        gf = graph_frame()
        tr, dot = make_trace(R, D0)
        qc = VGroup(T("smooth ramp", 34, TEXT), T("or staircase?", 34, TEXT)).arrange(DOWN, buff=.15)
        box = RoundedRectangle(corner_radius=.15, width=qc.width + .5, height=qc.height + .4, stroke_color=YELLOW,
                               stroke_width=3, fill_color=YELLOW, fill_opacity=.1)
        qg = VGroup(box, qc).move_to([5.1, 2.6, 0])
        add_rig(self, R, R.cone, R.ring, clamps, schem(), gf, qg, tr, dot)
        self.at("a staircase")
        self.play(FadeOut(qg), run_time=.8)
        # counter and timer
        cnt = [T(f"step {i}", 34, YELLOW).move_to([5.3, 3.1, 0]) for i in range(1, 5)]
        timer = M("t = 0 s", 30).move_to([5.3, 2.3, 0])
        timer.t = 0.0
        timer.last = 0

        def tick(m, dt):
            m.t += dt
            s = int(m.t)
            if s != m.last:
                m.last = s
                m.become(M(f"t = {s} s", 30).move_to([5.3, 2.3, 0]))
        timer.add_updater(tick)
        self.add(timer)
        px = lambda t: GX0 + GXS * t
        lvl = lambda k: GY0 + k * GRISE
        self.until(TS8[0] + .3)
        self.play(FadeIn(cnt[0]), run_time=.4)
        self.at("flat stretches are")
        br = Line([px(TS8[0] + .35), lvl(1) + .3, 0], [px(TS8[0] + .35) + .01, lvl(1) + .3, 0]).set_stroke(TEXT, 5).set_z_index(7)
        t_b = self.renderer.time

        def growbr(m, dt):
            e = min(R.t, TS8[1]) - (TS8[0] + .35)
            m.put_start_and_end_on([px(TS8[0] + .35), lvl(1) + .3, 0], [px(TS8[0] + .35) + max(.02, GXS * e), lvl(1) + .3, 0])
        br.add_updater(growbr)
        wl = lab("wait", px(3.4), lvl(1) + .72).set_z_index(7)
        self.add(br)
        self.play(FadeIn(wl), run_time=.5)
        self.at("sudden rises")
        self.until(TS8[1] + .3)
        br.clear_updaters()
        self.play(Transform(cnt[0], cnt[1]), run_time=.4)
        sl = lab("step", px(TS8[1]) + .9, lvl(2) + .45).set_z_index(7)
        sl.set_color(YELLOW)
        self.play(FadeIn(sl), FadeOut(wl), FadeOut(br), run_time=.5)
        self.at("rises 8 nanometers")
        self.play(FadeOut(sl), run_time=.3)
        self.until(TS8[2] + .1)
        self.play(Transform(cnt[0], cnt[2]), run_time=.4)
        x8 = px(TS8[2]) + .25
        brk = VGroup(Line([x8, lvl(2), 0], [x8, lvl(3), 0]).set_stroke(TEXT, 5),
                     Line([x8 - .1, lvl(2), 0], [x8 + .1, lvl(2), 0]).set_stroke(TEXT, 5),
                     Line([x8 - .1, lvl(3), 0], [x8 + .1, lvl(3), 0]).set_stroke(TEXT, 5)).set_z_index(7)
        l8 = M("8 nm", 30, TEXT).move_to([x8 + .85, (lvl(2) + lvl(3)) / 2, 0]).set_z_index(7)
        self.play(Create(brk), FadeIn(l8), run_time=.8)
        self.at("timing the flat")
        self.play(FadeOut(brk), FadeOut(l8), run_time=.4)
        br2 = Line([px(TS8[2] + .35), lvl(3) + .3, 0], [px(TS8[2] + .35) + .01, lvl(3) + .3, 0]).set_stroke(TEXT, 5).set_z_index(7)

        def growbr2(m, dt):
            e = min(R.t, TS8[3]) - (TS8[2] + .35)
            m.put_start_and_end_on([px(TS8[2] + .35), lvl(3) + .3, 0], [px(TS8[2] + .35) + max(.02, GXS * e), lvl(3) + .3, 0])
        br2.add_updater(growbr2)
        wl2 = lab("wait", px(12.4), lvl(3) + .72).set_z_index(7)
        self.add(br2)
        self.play(FadeIn(wl2), run_time=.5)
        self.at("before each jump")
        self.until(TS8[3] + .3)
        br2.clear_updaters()
        self.play(Transform(cnt[0], cnt[3]), run_time=.4)
        self.play(FadeOut(wl2), run_time=.4)
        self.at("the invisible walk")
        self.until(18.4)
        self.at("step rate")
        badge = chip("steps per\nsecond", TEXT, 28).move_to([5.3, 2.7, 0]) if False else VGroup(
            RoundedRectangle(corner_radius=.14, width=2.5, height=1.2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                             fill_opacity=.12),
            VGroup(T("steps per", 28, TEXT), T("second", 28, TEXT)).arrange(DOWN, buff=.05)).move_to([5.3, 2.7, 0])
        badge[1].move_to(badge[0])
        timer.clear_updaters()
        self.play(ReplacementTransform(VGroup(cnt[0], timer), badge), run_time=1.0)
        self.finish()


D9 = D0 + STEP * 4
TS9 = [5.6, 17.4]


class S09Spring(Sc):
    def construct(self):
        R = make_rig(d=D9, drive=stairs(TS9, D9), aoff=1.6, fid=.6)
        clamps = clamps_pair()
        gf = graph_frame()
        tr, dot = make_trace(R, D9)
        # the carried graph from chapter's previous scene is cleared at once
        add_rig(self, R, R.cone, R.ring, clamps, schem())
        self.at("the trap also behaves")
        self.wait(.6)
        self.at("like a spring")
        self.play(Create(R.coil), run_time=1.2)
        self.add(R.coil)
        self.at("pull the bead")
        self.play(Indicate(R.bead, color=TEXT, scale_factor=1.1), run_time=.8)
        self.at("restoring force grows")
        self.add(R.arrow)
        self.play(FadeIn(R.arrow), run_time=.8)
        self.at("after calibration")
        FM = 7.4
        gg = vgauge(6.0, -.1, 3.3, RED)
        gg.fill.val = lambda: R.d / FM
        gl = lab("force", 6.0, 3.55, 28, RED)
        cl = lab("calibrated", 5.6, -.5, 26, TEXT)
        self.play(FadeIn(gg), FadeIn(gl), FadeIn(cl), run_time=.9)
        self.at("displacement becomes force")
        dl = lab("displacement", -3.0, -1.6, 28, TEXT)
        self.play(FadeIn(dl), run_time=.6)
        self.play(Indicate(gg, color=YELLOW, scale_factor=1.08), run_time=.8)
        self.at("trap stiffness")
        self.play(FadeOut(dl), run_time=.3)
        sl = lab("stiffness", -3.0, -1.6, 28, RED)
        self.play(FadeIn(sl), run_time=.6)
        self.at("each nanometer")
        sl2 = lab("force per nm", -3.0, -1.6, 28, RED)
        self.play(Transform(sl, sl2), run_time=.6)
        self.at("farther from center")
        self.play(FadeOut(sl), run_time=.3)
        ol = lab("opposing load", -2.3, 1.45, 28, RED)
        self.play(FadeIn(ol), run_time=.6)
        self.at("larger opposing load")
        self.play(Indicate(R.arrow, color=YELLOW), run_time=1.0)
        self.finish()


class S10Stall(Sc):
    def construct(self):
        R = make_rig(d=D9 + STEP * 2, fid=1.0, aoff=1.6)
        clamps = clamps_pair()
        FM = 7.4
        gg = vgauge(6.0, -.1, 3.3, RED)
        gg.fill.val = lambda: R.d / FM
        gl = lab("force", 6.0, 3.55, 28, RED)
        cl = lab("calibrated", 5.6, -.5, 26, TEXT)
        add_rig(self, R, R.cone, R.ring, R.coil, R.arrow, clamps, schem(), gg, gl, cl)
        self.at("eventually the motor may stall")
        sl = lab("stalled", -1.3, -1.0 + 1.9 - 3.4 + .0, 28, TEXT)
        sl.move_to([R.bead.get_center()[0] + 1.9, -1.2, 0])
        self.play(FadeIn(sl), run_time=.6)
        self.at("keeps trying")
        self.play(Indicate(VGroup(R[-3], R[-2]), color=YELLOW), run_time=1.2)
        self.at("bead's offset")
        self.play(FadeOut(sl), run_time=.3)
        rx = R.xc
        bxw = lambda: R.bead.get_center()[0]
        brk = VMobject(stroke_color=TEXT, stroke_width=5).set_z_index(7)

        def updb(m, dt):
            x0, x1, y = R.ring.get_center()[0], R.bead.get_center()[0], 1.55
            m.set_points_as_corners([[x0, y - .14, 0], [x0, y, 0], [x1, y, 0], [x1, y - .14, 0]])
        brk.add_updater(updb)
        updb(brk, 0)
        bl = lab("offset", -2.6, 2.0)
        self.add(brk)
        self.play(FadeIn(bl), run_time=.6)
        self.at("opposing force")
        self.play(Indicate(gg, color=YELLOW, scale_factor=1.08), Indicate(R.arrow, color=YELLOW), run_time=1.0)
        self.at("different loads")
        self.play(FadeOut(bl), FadeOut(brk), run_time=.4)
        # computed record: staircase of the whole run (waits grow with the load)
        times = [1.8, 5.0, 9.4, 15.4, 21.25 + TS9[0], 21.25 + TS9[1]]
        ox, oy, W, H = -6.2, 1.45, 5.4, 1.85
        tmax = 55.0
        pts = [[ox, oy, 0]]
        lvl = 0
        for ts in times:
            pts += [[ox + W * ts / tmax, oy + H * lvl / 6.5, 0]]
            lvl += 1
            pts += [[ox + W * (ts + .35) / tmax, oy + H * lvl / 6.5, 0]]
        pts += [[ox + W, oy + H * lvl / 6.5, 0]]
        axs = VGroup(Arrow([ox, oy, 0], [ox + W + .15, oy, 0], buff=0, color=TEXT, stroke_width=3, tip_length=.18),
                     Arrow([ox, oy, 0], [ox, oy + H + .4, 0], buff=0, color=TEXT, stroke_width=3, tip_length=.18))
        rec = VMobject(stroke_color=YELLOW, stroke_width=5).set_points_as_corners(pts)
        tlab = lab("time", ox + W - .3, oy - .3, 26)
        plab = lab("position", ox + .85, oy + H + .35, 26)
        self.play(Create(axs), FadeIn(tlab), FadeIn(plab), run_time=.5)
        self.play(Create(rec, rate_func=linear), run_time=1.6)
        self.at("speed changes")
        sl_ = DashedLine([ox + W * .02, oy + .05, 0], [ox + W * .72, oy + H * 4.4 / 6.5, 0], color=TEXT, stroke_width=3).set_z_index(7)
        self.play(Create(sl_), run_time=1.0)
        self.at("time and calibration")
        self.play(FadeOut(sl_), run_time=.3)
        self.at("into steps")
        stc = chip("step", YELLOW, 30).move_to([1.2, 3.0, 0])
        ln1 = Line(stc.get_left(), [ox + W * (21.25 + TS9[0]) / tmax + .4, oy + H * 4.5 / 6.5, 0], color=YELLOW, stroke_width=2)
        self.play(FadeIn(stc), Create(ln1), run_time=.8)
        self.at("speed and pull")
        spc = chip("speed", TEXT, 30).move_to([1.2, 2.1, 0])
        ln2 = Line(spc.get_left(), [ox + W * .72, oy + H * 4.4 / 6.5, 0], color=TEXT, stroke_width=2)
        self.play(FadeIn(spc), Create(ln2), run_time=.8)
        self.play(Indicate(gl, color=YELLOW, scale_factor=1.2), Indicate(gg, color=YELLOW, scale_factor=1.06), run_time=1.0)
        self.finish()


class S11Conditions(Sc):
    def construct(self):
        SCP = .62
        xc = -3.3
        tys = (.75, -2.6)
        dtop = stairs([4.4, 5.6, 6.9, 8.4, 10.2, 12.4, 15.0, 17.8], .6, w=.4)

        def dbot(t):
            if t < 7.9:
                return (0.0, .6)
            if t < 14.4:
                return (.25 * (t - 7.9), .6)
            x = .25 * (14.4 - 7.9)
            d = .6 + STEP * sum(sstep((t - s) / .4) for s in (16.0, 18.4, 20.2))
            return (x, d)
        R1 = make_rig(d=D9 + STEP * 2, fid=1.0)
        clamps = clamps_pair()
        FM = 7.4
        add_rig(self, R1, R1.cone, R1.ring, R1.coil, R1.arrow, clamps, schem())
        Rt = make_rig(xc=xc, ty=tys[0], sc=SCP, tw=10.6, tx=-.6, drive=dtop, aoff=1.35)
        Rb = make_rig(xc=xc, ty=tys[1], sc=SCP, tw=10.6, tx=-.6, drive=dbot, fid=0.0, aoff=1.35)
        self.play(FadeOut(VGroup(R1.cone, R1.ring, R1.coil, R1.arrow, clamps)),
                  ReplacementTransform(R1, Rt), TransformFromCopy(R1, Rb), run_time=1.0)
        Rt.t = Rb.t = self.renderer.time
        self.add(Rt, Rb, Rt.cone, Rt.ring, Rb.cone, Rb.ring, shimmer(Rt.track, TEXT, .22), shimmer(Rb.track, TEXT, .22))
        Rb.fid = 1.0
        for R in (Rt, Rb):
            R.kt.set_value(1.0)
        self.at("a number belongs")
        lt = lab("fixed trap", -5.15, 3.45)
        self.play(FadeIn(lt), run_time=.6)
        self.at("in a fixed trap")
        self.add(Rt.arrow)
        gt = vgauge(5.2, 1.0, 2.2, RED)
        gt.fill.val = lambda: Rt.d / FM
        ll = lab("load", 5.2, 3.5, 28, RED)
        self.play(FadeIn(Rt.arrow), FadeIn(gt), FadeIn(ll), run_time=.8)
        self.at("load rises")
        self.play(Indicate(gt, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.at("feedback can hold")
        lb = lab("constant load", -4.9, .0)
        self.add(Rb.arrow)
        gb = vgauge(5.2, -2.45, 2.2, RED)
        gb.fill.val = lambda: Rb.d / FM
        Rb.fid = 0.0
        self.play(FadeIn(lb), FadeIn(Rb.arrow), FadeIn(gb), run_time=.8)
        self.at("compare motors only")
        # ATP gauges and a grey comparison bracket
        atp_t = vgauge(6.3, 1.0, 2.2, GREEN)
        atp_b = vgauge(6.3, -2.45, 2.2, GREEN)
        atp_t.fill.val = lambda: .7
        lvl_b = {"v": .4}
        atp_b.fill.val = lambda: lvl_b["v"]
        al = lab("ATP", 6.3, 3.5, 28, GREEN)
        bx = -6.5
        brack = VGroup(Line([bx, 2.0, 0], [bx, -1.5, 0]), Line([bx, 2.0, 0], [bx + .25, 2.0, 0]),
                       Line([bx, -1.5, 0], [bx + .25, -1.5, 0])).set_stroke(GREY, 5)
        self.play(FadeIn(atp_t), FadeIn(atp_b), FadeIn(al), Create(brack), run_time=1.0)
        self.at("matched fuel")
        self.play(Indicate(al, color=YELLOW, scale_factor=1.15), run_time=.8)
        self.at("loading conditions")
        lb2 = lab("fixed trap", -5.15, .0)
        self.play(Transform(lb, lb2), run_time=.6)
        lvl_b["v"] = .4
        self.play(UpdateFromAlphaFunc(Mobject(), lambda m, a: lvl_b.__setitem__("v", .4 + .3 * a)), run_time=.9)
        self.play(brack.animate.set_stroke(TEXT, 5), run_time=.6)
        self.at("a neat calculation")
        self.play(Indicate(brack, color=TEXT, scale_factor=1.04), run_time=.9)
        self.finish()


class S12Rule(Sc):
    def construct(self):
        # left bench: motors clamped to glass drive the marked track left
        gl = Rectangle(width=7.0, height=.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.3).move_to([-3.4, -3.45, 0])
        LV = .1
        trL = glide_track(-3.2, y=.55, w=4.4, h=.7)
        trL.v = LV
        trL.on = False
        wl = [walker(x, .2, -1, "clamped", 1.1, L=3.3, P=4.0, v=LV, t0=1.3 * i, on=False) for i, x in enumerate((-4.4, -2.6))]
        pads = [clamp_pad(x, -3.1) for x in (-4.4, -2.6)]
        circ, tri = end_marks(trL)
        # right bench: motor on a fixed track pulls a trapped bead
        TSR = [2.0, 4.2, 6.9, 9.6, 12.5]
        D0R = .6
        R = make_rig(xc=1.3, ty=-2.9, sc=.9, tw=6.3, tx=3.65, d=D0R, drive=stairs(TSR, D0R, w=.4), aoff=1.35, fid=.6)
        R.kt.set_value(1.0)
        div = DashedLine([0, -3.8, 0], [0, 3.8, 0], color=GREY, stroke_width=2).set_opacity(.5)
        rsh = shimmer(R.track, TEXT, .22)
        self.add(gl, trL, *wl, *pads, circ, tri, R, R.cone, R.ring, div, schem(), rsh)
        self.at("one bench")
        self.wait(.4)
        self.at("fix the motor")
        ci = clamp_icon(-3.5, -2.55)
        trL.on = True
        for w_ in wl:
            w_.on = True
        self.play(FadeIn(ci), run_time=.6)
        self.at("the track reports direction")
        self.play(ci.animate.move_to([-3.2, 1.7, 0]), run_time=.8)
        la = Arrow([-1.0, 1.7, 0], [-2.4, 1.7, 0], buff=0, color=TEXT, stroke_width=6)
        self.play(Create(la), run_time=.8)
        self.at("hold the bead")
        self.play(FadeOut(la), ci.animate.move_to([-.6, -1.0, 0]), run_time=.9)
        self.at("its motion reports steps")
        GX, GY = 1.3, .75
        axs = VGroup(Arrow([GX, GY, 0], [GX + 4.6, GY, 0], buff=0, color=TEXT, stroke_width=3, tip_length=.18),
                     Arrow([GX, GY, 0], [GX, GY + 2.9, 0], buff=0, color=TEXT, stroke_width=3, tip_length=.18))
        tr_, dot_ = make_trace(R, D0R, color=YELLOW, x0=GX, y0=GY, xs=.31, rise=.5)
        self.play(Create(axs), run_time=.8)
        self.add(tr_, dot_)
        self.at("steps and force")
        gg = vgauge(6.35, GY, 2.5, RED)
        gg.fill.val = lambda: R.d / 7.4 + .12
        fl = lab("force", 6.35, 3.5, 28, RED)
        self.add(R.arrow)
        self.play(FadeIn(gg), FadeIn(fl), FadeIn(R.arrow), run_time=.8)
        self.at("change what is held still")
        left = VGroup(gl, trL, *wl, *pads, circ, tri, ci)
        right = VGroup(R, R.cone, R.ring, R.arrow, axs, tr_, dot_, gg, fl, div, rsh)
        trL.on = False
        for w_ in wl:
            w_.on = False
        self.play(FadeOut(left), FadeOut(right), run_time=1.0)
        ruler = VGroup(Line([-5, -.8, 0], [5, -.8, 0]).set_stroke(TEXT, 5),
                       *[Line([x, -.8, 0], [x, -.8 + (.4 if abs(x % 1) < .01 else .22), 0]).set_stroke(TEXT, 4)
                         for x in np.arange(-5, 5.01, .5)])
        arr = Arrow([-6.2, .9, 0], [-3.2, .9, 0], buff=0, color=YELLOW, stroke_width=16, tip_length=.55).set_z_index(5)
        self.play(FadeIn(ruler), FadeIn(arr), run_time=.7)
        self.at("motion becomes a measurement")
        self.play(arr.animate.shift(RIGHT * 7.0), run_time=1.6, rate_func=linear)
        tick = Line([3.5, -.8, 0], [3.5, .45, 0]).set_stroke(YELLOW, 10).set_z_index(6)
        ml = lab("measurement", 3.5, 1.7, 34, YELLOW)
        self.play(FadeOut(arr), Create(tick), FadeIn(ml), run_time=.8)
        self.finish()


class S13End(EndCard):
    LINE = "Hold one thing still, and motion becomes a measurement."
