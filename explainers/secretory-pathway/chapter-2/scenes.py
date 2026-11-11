"""Crossing the Golgi Stack: chapter 2 of the secretory-pathway film pair.

Colours keep chapter 1's meaning: BLUE membranes/COPI, GOLD cargo, TEAL ER chaperone + KDEL + its loop,
WHITE receptor and questions, GREY flow. New here: ORANGE = early Golgi enzymes, MAGENTA = late ones.
Blocks are coloured by where their sac sits in the stack (cis = orange, trans = magenta), so a sac that
slides right changes character on screen. Everything is schematic.
"""
import importlib.util
import pathlib
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

_p = pathlib.Path(__file__).resolve().parent.parent / "scenes.py"
_spec = importlib.util.spec_from_file_location("ch1_scenes", _p)
ch1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ch1)

ORANGE = "#F2994A"
MAGENTA = "#E056C6"
INK = ch1.INK
GOLGI_X = ch1.GOLGI_X
SX = (-3.0, 0.0, 3.0)     # big-stack slot centres
SAC_CY = 0.2


def lab(text, p, color=TEXT, size=30):
    return T(text, size=size, color=color).move_to(p)


def qcard(text, size=34, pos=(0, 3.3, 0)):
    t = T(text, size=size, color=TEXT)
    box = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.4, corner_radius=0.15,
                           stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=0.9)
    return VGroup(box, t.move_to(box)).move_to(pos)


class Sac(VGroup):
    """A cisterna with enzyme blocks (colour follows x position) and optional gold cargo."""

    def __init__(self, x=0.0, cy=SAC_CY, k=1.0, kh=None, n=12, seed=1, gold=0, bs=0.22, ref=(-3.0, 3.0), colored=True):
        kh = kh or k
        rng = random.Random(seed)
        body = RoundedRectangle(width=1.55 * k, height=4.5 * kh, corner_radius=0.6 * k, stroke_color=BLUE,
                                stroke_width=4, fill_color=BLUE, fill_opacity=0.14).move_to([x, cy, 0])
        slots = [(cx * k, (-1.7 + 0.68 * j) * kh) for j in range(6) for cx in (-0.40, 0.0, 0.40)]
        rng.shuffle(slots)
        ths = [(i + 0.5) / n for i in range(n)]
        rng.shuffle(ths)
        blocks = VGroup()
        for i in range(n):
            sx, sy = slots[i]
            b = Square(side_length=bs * k, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95)
            b.move_to([x + sx, cy + sy, 0])
            b.th = ths[i]
            b.col = ORANGE
            blocks.add(b)
        golds = VGroup(*[Dot([x + slots[n + i][0], cy + slots[n + i][1], 0], radius=0.1 * k + 0.02, color=GOLD)
                         for i in range(gold)])
        super().__init__(body, blocks, golds)
        self.body, self.blocks, self.golds = body, blocks, golds
        self.ref = ref
        if colored:
            self.recolor()
            self.add_updater(lambda m: m.recolor())

    def recolor(self):
        x = self.body.get_center()[0]
        f = float(np.clip((x - self.ref[0]) / (self.ref[1] - self.ref[0]), 0, 1))
        fe = 0.1 + 0.8 * f
        for b in self.blocks:
            c = ORANGE if fe < b.th else MAGENTA
            if c != b.col:
                b.set_fill(color=c)
                b.col = c

    def of_color(self, c):
        return VGroup(*[b for b in self.blocks if b.col == c])


def big_sacs(seed0=1, gold=0, n=12):
    return [Sac(x, seed=seed0 + i, gold=gold, n=n) for i, x in enumerate(SX)]


def backdrop():
    """ERGIC off the left edge, TGN off the right, flow chevrons under the stack."""
    er = ch1.ergic().shift(LEFT * 2.47)
    tg = ch1.tgn().shift(RIGHT * 4.47)
    flow = ch1.flow_arrow().shift(DOWN * 1.3)
    return er, tg, flow


class Stream(VGroup):
    """Gold dots drifting right between x0 and x1; `gate` fades the whole stream."""

    def __init__(self, n, x0, x1, ys, speed=1.2, r=0.1, gate=1.0):
        super().__init__()
        self.gate = gate
        for i in range(n):
            d = Dot(radius=r, color=GOLD)
            d.x = x0 + (x1 - x0) * i / n
            d.y = ys[i % len(ys)]
            d.move_to([d.x, d.y, 0])

            def up(m, dt, s=self):
                m.x += speed * dt
                if m.x > x1:
                    m.x = x0
                m.move_to([m.x, m.y, 0])
                edge = min(m.x - x0, x1 - m.x)
                m.set_opacity(float(np.clip(edge / 0.7, 0, 1)) * s.gate)
            d.add_updater(up)
            self.add(d)


def gate_to(s, v, run=1.0):
    g0 = s.gate
    return UpdateFromAlphaFunc(s, lambda m, a: setattr(m, "gate", g0 + (v - g0) * a), run_time=run)


def copi(r=0.3, content=ORANGE):
    ring = Circle(radius=r, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.22)
    spikes = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * r, np.array([np.cos(a), np.sin(a), 0]) * (r + 0.11),
                           color=BLUE, stroke_width=3) for a in np.linspace(0, TAU, 9)[:-1]])
    blk = Square(side_length=r * 0.55, stroke_width=0, fill_color=content, fill_opacity=0.95)
    return VGroup(ring, spikes, blk)


def plain_ves(r=0.27, gold=2):
    ring = Circle(radius=r, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2)
    ds = VGroup(*[Dot(np.array([(-0.08 + 0.16 * i), 0.0, 0]), radius=0.07, color=GOLD) for i in range(gold)])
    return VGroup(ring, ds)


def ride(v, src, dst, run, arc=0.35):
    def f(m, a):
        p = src() * (1 - a) + dst() * a + UP * arc * np.sin(PI * a)
        m.move_to(p)
    return UpdateFromAlphaFunc(v, f, run_time=run, rate_func=smooth)


def pin(x, y):
    return VGroup(Dot([x, y + 0.22, 0], radius=0.09, color=TEXT), Line([x, y + 0.22, 0], [x, y - 0.12, 0], color=TEXT, stroke_width=4))


def hop(scene, src, dst, run=1.8, y=None):
    """A vesicle buds from sac `src`, crosses the gap and fuses with `dst` (sacs stay put)."""
    y = SAC_CY + 0.2 if y is None else y
    a = np.array([src.body.get_right()[0] + 0.28, y, 0.0])
    b = np.array([dst.body.get_left()[0] - 0.28, y, 0.0])
    v = plain_ves().move_to(a)
    arrow = Arrow([a[0] - 0.1, y + 0.85, 0], [b[0] + 0.1, y + 0.85, 0], buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
    scene.play(FadeIn(v, scale=0.3), FadeIn(arrow), run_time=0.4)
    scene.play(v.animate.move_to(b), run_time=run)
    scene.play(FadeOut(v, scale=0.3), FadeOut(arrow), Indicate(dst.body, color=GOLD, scale_factor=1.0), run_time=0.5)


# ----------------------------------------------------------------------------------------------
# Panels: looping stable / maturation pictures (side by side and in the small world)
# ----------------------------------------------------------------------------------------------
def smoothstep(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def _bases(m):
    for x in m.family_members_with_points():
        x._bf = x.get_fill_opacity()
        x._bs = x.get_stroke_opacity()


def _setop(m, a):
    for x in m.family_members_with_points():
        if hasattr(x, "_bf"):
            x.set_fill(opacity=x._bf * a)
            x.set_stroke(opacity=x._bs * a)


class Panel:
    def __init__(self, kind, cx, cy, k, kh=None, bs=0.22, period=6.0):
        self.kind, self.cx, self.cy, self.k, self.kh = kind, cx, cy, k, kh or k
        self.t = 0.0
        self.on = False
        self.vis = 1.0
        self.period = period
        ref = (cx - 3 * k, cx + 3 * k)
        mk = lambda lx, i: Sac(cx + lx * k, cy=cy, k=k, kh=self.kh, seed=i + 5, gold=(3 if kind == "mature" else 0), bs=bs, ref=ref)
        if kind == "stable":
            self.sacs = [mk(lx, i) for i, lx in enumerate(SX)]
            self.pins = VGroup(*[pin(s.body.get_center()[0], s.body.get_top()[1] + 0.05) for s in self.sacs])
            self.ves = plain_ves(0.27 * max(k, 0.5) / 0.75 if k < 0.75 else 0.27)
            self.ves.set_opacity(0)
            self.group = VGroup(*self.sacs, self.pins, self.ves)
        else:
            self.sacs = [mk(lx, i) for i, lx in enumerate((-6.0, -3.0, 0.0, 3.0))]
            self.lx = [-6.0, -3.0, 0.0, 3.0]
            self.cop = copi(0.27 if k >= 0.6 else 0.2)
            self.cop.set_opacity(0)
            self.group = VGroup(*self.sacs, self.cop)
            self.apply(0.0)
        self.group.add(*[])
        _bases(self.group)
        self.driver = Mobject()
        self.driver.add_updater(lambda m, dt: self.step(dt))

    def pos(self, lx, dy=0.0):
        return np.array([self.cx + lx * self.k, self.cy + dy, 0.0])

    def step(self, dt):
        if self.on:
            self.t += dt
        self.apply((self.t % self.period) / self.period)

    def apply(self, ph):
        if self.kind == "stable":
            v = self.ves
            hopw = [(0.05, 0.40, -3.0, 0.0), (0.50, 0.85, 0.0, 3.0)]
            vis, p = 0.0, self.pos(-3.0)
            for a, b, x0, x1 in hopw:
                if a <= ph <= b:
                    u = (ph - a) / (b - a)
                    x = x0 + 1.5 + (x1 - x0 - 3.0) * smoothstep(u) + 1.5 * 0  # gap midpoints
                    xs = x0 + 1.5 * 1.0
                    xe = x1 - 1.5 * 1.0
                    x = xs + (xe - xs) * smoothstep(u)
                    p = self.pos(x, 0.2 * self.kh)
                    vis = min(1.0, u * 8, (1 - u) * 8)
            v.move_to(p)
            _setop(v, vis * self.vis)
            for s in self.sacs:
                _setop(s, self.vis)
            _setop(self.pins, self.vis)
        else:
            s1 = smoothstep((ph - 0.08) / 0.3) if self.period <= 7 else 0
            if self.period > 7:
                s1 = smoothstep((ph - 0.08) / 0.2) + smoothstep((ph - 0.55) / 0.2)
                sh = 3.0 * s1 / 1.0
            sh = 3.0 * (smoothstep((ph - 0.1) / 0.5)) if self.period <= 7 else 3.0 * s1
            for i, s in enumerate(self.sacs):
                lx = self.lx[i] + sh
                s.move_to(self.pos(lx) + (s.get_center()[1] - s.get_center()[1]) * UP) if False else None
                dx = self.pos(lx)[0] - s.body.get_center()[0]
                s.shift(RIGHT * dx)
                _setop(s, float(np.clip((4.6 - abs(lx)) / 1.6, 0, 1)) * self.vis)
            # COPI vesicle carries orange back from the mid sac to the cis sac while all rest
            vis, p = 0.0, self.pos(0)
            if 0.62 <= ph <= 0.92 and self.period <= 7:
                u = (ph - 0.62) / 0.3
                a = self.pos(0.0 + 3.0 - 3.0, 0)          # mid slot (centre 0)
                a = self.pos(0.0 - 0.0)
                src, dst = self.pos(-0.0 + 0.0 - 0.0 + 0.0), self.pos(-3.0)
                src = self.pos(-0.0) + RIGHT * 0.0
                p = (self.pos(-0.8) * (1 - smoothstep(u)) + self.pos(-2.2) * smoothstep(u)) + UP * 0.35 * np.sin(PI * u)
                vis = min(1.0, u * 8, (1 - u) * 8)
            self.cop.move_to(p)
            _setop(self.cop, vis * self.vis)


def panel_fade(panel, v, run=1.0):
    v0 = panel.vis
    return UpdateFromAlphaFunc(panel.driver, lambda m, a: setattr(panel, "vis", v0 + (v - v0) * a), run_time=run)


# ----------------------------------------------------------------------------------------------
# Test-tube frame shared by s04-s07
# ----------------------------------------------------------------------------------------------
def tube():
    L, R, TOP, BOT, r = -6.3, 6.3, 3.0, -2.9, 1.0
    pts = [[L, TOP, 0], [L, BOT + r, 0]]
    for a in np.linspace(PI, 1.5 * PI, 8)[1:]:
        pts.append([L + r + r * np.cos(a), BOT + r + r * np.sin(a), 0])
    for a in np.linspace(1.5 * PI, 2 * PI, 8)[:-1]:
        pts.append([R - r + r * np.cos(a), BOT + r + r * np.sin(a), 0])
    pts += [[R, BOT + r, 0], [R, TOP, 0]]
    t = VMobject(stroke_color=TEXT, stroke_width=4)
    t.set_points_as_corners(pts)
    return t


TUBE_SC = 0.55
DONOR_X, ACC_X, TUBE_Y = -3.6, 3.6, -0.05


def mini_stack(cx, seed=1, gold=0):
    ref = (cx - 3 * TUBE_SC, cx + 3 * TUBE_SC)
    return VGroup(*[Sac(cx + lx * TUBE_SC, cy=TUBE_Y, k=TUBE_SC, seed=seed + i, gold=gold, ref=ref) for i, lx in enumerate(SX)])


def donor_gold(cx=DONOR_X):
    return VGroup(*[Dot([cx + dx, TUBE_Y + dy, 0], radius=0.11, color=GOLD)
                    for dx, dy in [(-1.6, 0.6), (-1.55, -0.5), (-0.5, 0.2), (0.4, -0.7), (0.5, 0.8), (1.5, 0.1), (1.6, -0.6)]])


def drift_dots(group, amp=0.12, speed=0.7):
    for i, d in enumerate(group):
        d.base = d.get_center().copy()
        d.ph = i * 1.3
        d.t = 0.0

        def up(m, dt):
            m.t += dt
            m.move_to(m.base + np.array([amp * np.sin(speed * m.t + m.ph), amp * np.cos(0.8 * speed * m.t + m.ph), 0]))
        d.add_updater(up)


def magnifier():
    g = VGroup(Circle(radius=0.38, stroke_color=TEXT, stroke_width=5), Line([0.27, -0.27, 0], [0.62, -0.62, 0], color=TEXT, stroke_width=7))
    return g


def bob(m, base, amp=0.15):
    m.t = 0.0
    m.base = np.array(base, float)

    def up(mm, dt):
        mm.t += dt
        mm.move_to(mm.base + UP * amp * np.sin(2.0 * mm.t) + RIGHT * amp * np.sin(1.3 * mm.t))
    m.add_updater(up)


# ----------------------------------------------------------------------------------------------
# Small world (chapter 1's cell) used in s00, s01, s13
# ----------------------------------------------------------------------------------------------
def mini_world():
    org = VGroup(ch1.cell_outline(), ch1.er_stack(), ch1.ergic(), ch1.tgn(), ch1.membrane(), ch1.shelf(), ch1.routes())
    flow = ch1.flow_arrow()
    sacs = [Sac(x, cy=0, k=0.374, kh=0.522, bs=0.34, seed=i + 3, ref=(GOLGI_X[0], GOLGI_X[2])) for i, x in enumerate(GOLGI_X)]
    return org, flow, sacs


def mini_stream(gate=1.0):
    return Stream(7, -3.6, 1.5, [-0.8, -0.35, 0.1, 0.55, 0.9], speed=1.1, gate=gate)


def loop_path():
    return VMobject().set_points_smoothly([[-1.4, 1.3, 0], [-2.3, 2.0, 0], [-3.7, 2.15, 0], [-5.0, 1.3, 0]])


# ================================================================================================
class S00Link(SpokenScene):
    def construct(self):
        org, flow, sacs = mini_world()
        st = mini_stream()
        self.add(org, flow, *sacs, st)
        q = qcard("Cargo moves. Enzymes stay. How?")
        self.wait(0.4)
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.8)
        self.at("Chapter 1")
        loop = loop_path().set_stroke(TEAL, 4, opacity=0.4)
        tag = lab("chapter 1", [-5.4, 3.3, 0], TEAL, 28)
        self.play(Create(loop), FadeIn(tag), run_time=1.4)
        self.at("chaperone")
        blob = RoundedRectangle(width=0.8, height=0.42, corner_radius=0.18, stroke_color=TEAL, stroke_width=3,
                                fill_color=TEAL, fill_opacity=0.35)
        kd = T("KDEL", size=24, color=TEAL).next_to(blob, UP, buff=0.4)
        chap = VGroup(blob, kd).move_to([-4.9, 1.45, 0])
        self.play(FadeIn(chap, scale=0.5), run_time=0.7)
        self.at("drifted forward")
        self.play(chap.animate.move_to([-1.5, 1.45, 0]), run_time=2.4, rate_func=smooth)
        self.at("A receptor")
        recep = VGroup(Arc(radius=0.2, start_angle=PI, angle=PI, color=TEXT, stroke_width=6),
                       Line([0, -0.2, 0], [0, -0.45, 0], color=TEXT, stroke_width=6))
        ves = copi(0.62, TEAL)
        ves[2].set_opacity(0)
        ves.move_to(chap[0])
        recep.move_to(chap[0].get_center() + DOWN * 0.1 + LEFT * 0.0).shift(DOWN * 0.0)
        self.play(FadeIn(ves), FadeIn(recep), kd.animate.shift(UP * 0.55), run_time=0.8)
        grp = VGroup(chap, ves, recep)
        self.at("bring it back")
        self.play(MoveAlongPath(grp, loop), run_time=3.2, rate_func=smooth)
        self.play(grp.animate.scale(0.9), Indicate(org[1], color=TEAL), run_time=0.6)
        self.finish()


class S01Title(TitleCard):
    LESSON = "The Secretory Pathway"
    TITLE = "Crossing the Golgi Stack"

    def construct(self):
        org, flow, sacs = mini_world()
        st = mini_stream()
        q = qcard("Cargo moves. Enzymes stay. How?")
        loop = loop_path().set_stroke(TEAL, 4, opacity=0.4)
        self.add(org, flow, *sacs, st, q, loop)
        self.play(q.animate.scale(0.55).move_to([-4.6, 3.45, 0]), run_time=0.5)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.0)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        back = RoundedRectangle(width=title.width + 1.0, height=1.8, corner_radius=0.2, stroke_width=0,
                                fill_color=INK, fill_opacity=0.95)
        title.move_to([0, 0.3, 0])
        rule.move_to([0, -0.4, 0])
        card = VGroup(back, title, rule).move_to([0, 0.3, 0])
        self.play(FadeIn(card), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(card), run_time=0.4)
        self.finish()


class S02Stack(SpokenScene):
    def construct(self):
        er, tg, flow = backdrop()
        sacs = big_sacs(1)
        for s in sacs:
            s.blocks.set_opacity(0)
            s.body.add_updater(lambda m, dt=0: None)
        for s in sacs:
            s.remove_updater(s.updaters[0]) if s.updaters else None   # no recolour while hidden
        self.play(FadeIn(er), FadeIn(tg), FadeIn(flow), *[FadeIn(s.body) for s in sacs], run_time=1.2)
        for s in sacs:
            s.body.t = 0.0

            def br(m, dt):
                m.t += dt
                m.set_fill(opacity=0.14 + 0.05 * np.sin(1.6 * m.t))
            s.body.add_updater(br)
        self.add(*sacs)
        self.at("cisterna", lead=0.4)
        l_cist = lab("cisterna", [0, 2.95, 0], TEXT, 34)
        self.play(sacs[1].body.animate.set_stroke(WHITE, 7), FadeIn(l_cist), run_time=0.6)
        self.at("cis face")
        l_cis = lab("cis", [-3.0, 2.95, 0], TEXT, 34)
        s1 = Stream(4, -6.4, -2.4, [0.2, 0.9, -0.5, 0.5], speed=1.0, gate=0.0)
        self.add(s1)
        self.play(FadeIn(l_cis), gate_to(s1, 1, 0.8), sacs[1].body.animate.set_stroke(BLUE, 4), run_time=0.8)
        self.at("trans face")
        l_trans = lab("trans", [3.0, 2.95, 0], TEXT, 34)
        s2 = Stream(4, 3.6, 6.2, [0.2, -0.4, 0.8, 0.0], speed=1.0, gate=0.0)
        self.add(s2)
        self.play(FadeIn(l_trans), gate_to(s2, 1, 0.8), run_time=0.8)
        self.at("Early sugar enzymes")
        self.play(FadeOut(l_cist), run_time=0.3)
        for s in sacs:
            s.recolor()
        org_b = VGroup(*[b for s in sacs for b in s.of_color(ORANGE)])
        mag_b = VGroup(*[b for s in sacs for b in s.of_color(MAGENTA)])
        for b in list(org_b) + list(mag_b):
            b.set_opacity(0)
        self.play(*[b.animate.set_opacity(0.95) for b in org_b], run_time=2.2, lag_ratio=0.0)
        self.at("later ones")
        self.play(*[b.animate.set_opacity(0.95) for b in mag_b], run_time=2.0)
        self.at("they overlap")
        l_ov = lab("overlap", [0, 2.95, 0], TEXT, 34)
        sch = lab("schematic", [5.6, -2.6, 0], GREY, 26)
        self.play(FadeIn(l_ov), FadeIn(sch), Indicate(sacs[1].body, color=WHITE, scale_factor=1.0), run_time=0.8)
        self.finish()


def stack_state(with_pins=False, hidden_blocks=False):
    er, tg, flow = backdrop()
    sacs = big_sacs(1)
    for s in sacs:
        s.body.t = 0.0

        def br(m, dt):
            m.t += dt
            m.set_fill(opacity=0.14 + 0.05 * np.sin(1.6 * m.t))
        s.body.add_updater(br)
    return er, tg, flow, sacs


class S03Stable(SpokenScene):
    def construct(self):
        er, tg, flow, sacs = stack_state()
        self.add(er, tg, flow, *sacs)
        self.wait(0.2)
        self.at("Picture one", lead=0.1)
        l_st = lab("stable compartments", [0, 3.1, 0], TEXT, 34)
        self.play(FadeIn(l_st, shift=DOWN * 0.15), run_time=0.8)
        self.at("long lived")
        pins = VGroup(*[pin(s.body.get_center()[0], s.body.get_top()[1] + 0.05) for s in sacs])
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in pins], lag_ratio=0.3), run_time=1.4)
        self.at("characteristic set")
        self.play(*[Indicate(s.blocks, color=WHITE, scale_factor=1.15) for s in sacs], run_time=1.6)
        self.at("Small vesicles bud")
        hop(self, sacs[0], sacs[1], run=2.2)
        self.at("forward to the next")
        hop(self, sacs[1], sacs[2], run=2.2)
        self.at("medial")
        labs = VGroup(lab("cis", [-3.0, -2.75, 0], BLUE, 30), lab("medial", [0, -2.75, 0], BLUE, 30), lab("trans", [3.0, -2.75, 0], BLUE, 30))
        self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.3), run_time=1.2)
        hop(self, sacs[0], sacs[1], run=1.8)
        self.finish()


class S04Rothman(SpokenScene):
    def construct(self):
        er, tg, flow, sacs = stack_state()
        self.add(er, tg, flow, *sacs)
        t = tube()
        cell = lab("cell-free system", [0, 3.4, 0], TEXT, 30)
        stack = VGroup(*sacs)
        self.at("lab rebuilt", lead=0.3)
        self.play(FadeOut(er), FadeOut(tg), FadeOut(flow), Create(t), FadeIn(cell), run_time=1.6)
        for s in sacs:
            s.clear_updaters()
            s.recolor()
        ref = (DONOR_X - 3 * TUBE_SC, DONOR_X + 3 * TUBE_SC)
        don = mini_stack(DONOR_X, seed=1)
        self.play(ReplacementTransform(stack, don), run_time=1.8)
        credit = lab("Rothman laboratory", [-4.3, -3.45, 0], GREY, 26)
        self.play(FadeIn(credit), run_time=0.4)
        self.at("VSVG")
        dg = donor_gold()
        l_don = lab("donor", [DONOR_X, 1.75, 0], TEXT, 30)
        l_vsv = lab("VSV G", [DONOR_X, -1.8, 0], GOLD, 30)
        self.play(FadeIn(dg, scale=0.3), FadeIn(l_don), FadeIn(l_vsv), run_time=1.0)
        drift_dots(dg)
        self.at("Acceptor Golgi")
        acc = mini_stack(ACC_X, seed=11)
        l_acc = lab("acceptor", [ACC_X, 1.75, 0], TEXT, 30)
        self.play(FadeIn(acc, shift=DOWN * 0.8), FadeIn(l_acc), run_time=1.2)
        self.at("added a sugar")
        dash = DashedLine([-1.35, -0.75, 0], [1.35, -0.75, 0], color=TEXT, stroke_width=4, dash_length=0.18)
        dash.add_tip(tip_length=0.22)
        l_tr = lab("transfer inferred", [0, -0.2, 0], TEXT, 26)
        card = qcard("no added sugar", 28, (0, -2.4, 0))
        self.play(Create(dash), FadeIn(l_tr), FadeIn(card), run_time=1.3)
        self.at("readout")
        self.play(Indicate(card, color=WHITE, scale_factor=1.1), run_time=1.0)
        self.at("Transport needed")
        bolt = Polygon([-0.1, 0.35, 0], [-0.3, -0.05, 0], [-0.05, -0.05, 0], [-0.2, -0.4, 0], [0.3, 0.05, 0], [0.05, 0.05, 0],
                       stroke_width=0, fill_color=YELLOW, fill_opacity=1)
        atp = VGroup(chip("ATP", YELLOW, 28), bolt.scale(0.9).shift(LEFT * 1.05)).move_to([0, 1.95, 0])
        self.play(FadeIn(atp, shift=DOWN * 0.5), run_time=0.9)
        self.at("cytosol")
        cyt = VGroup(Ellipse(width=2.3, height=0.9, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.3),
                     T("cytosol", size=28, color=TEXT)).move_to([0, 0.95, 0])
        card2 = qcard("added sugar detected", 28, (0, -2.4, 0))
        self.play(FadeIn(cyt, shift=DOWN * 0.5), run_time=0.9)
        self.play(ReplacementTransform(card, card2), Indicate(dash, color=WHITE), run_time=1.0)
        cyt.t = 0.0
        cyt.base = cyt.get_center().copy()
        cyt.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.move_to(m.base + RIGHT * 0.1 * np.sin(1.5 * m.t)))[0])
        self.finish()


def tube_frame(scene, with_mag=True):
    t = tube()
    don, acc = mini_stack(DONOR_X, 1), mini_stack(ACC_X, 11)
    dg = donor_gold()
    drift_dots(dg)
    scene.add(t, don, acc, dg)
    return t, don, acc, dg


class S05Predict(SpokenScene):
    def construct(self):
        t, don, acc, dg = tube_frame(self)
        cell = lab("cell-free system", [0, 3.4, 0], TEXT, 30)
        self.add(cell)
        l_don = lab("donor", [DONOR_X, 1.75, 0], TEXT, 30)
        l_acc = lab("acceptor", [ACC_X, 1.75, 0], TEXT, 30)
        self.add(l_don, l_acc)
        q = qcard("Proof of within-stack vesicle transport?", 32, (0, 3.4, 0))
        self.wait(0.3)
        self.play(FadeOut(cell), FadeIn(q, shift=DOWN * 0.2), run_time=0.8)
        mag = magnifier().move_to([0, 0.3, 0])
        self.at("Does it prove")
        self.play(FadeIn(mag, scale=0.5), run_time=0.8)
        bob(mag, [0, 0.3, 0])
        self.at("Separate what")
        m1 = lab("measured", [-2.2, -2.4, 0], TEXT, 32)
        self.play(FadeIn(m1), run_time=0.8)
        self.at("mechanism")
        m2 = lab("proposed mechanism", [2.6, -2.4, 0], TEXT, 32)
        self.play(FadeIn(m2), run_time=0.8)
        self.finish()


class S06Think(NarratedScene):
    def construct(self):
        t, don, acc, dg = tube_frame(self)
        self.add(lab("donor", [DONOR_X, 1.75, 0], TEXT, 30), lab("acceptor", [ACC_X, 1.75, 0], TEXT, 30),
                 qcard("Proof of within-stack vesicle transport?", 32, (0, 3.4, 0)),
                 lab("measured", [-2.2, -2.4, 0], TEXT, 32), lab("proposed mechanism", [2.6, -2.4, 0], TEXT, 32))
        mag = magnifier().move_to([0, 0.3, 0])
        self.add(mag)
        bob(mag, [0, 0.3, 0], 0.25)
        atp = chip("ATP", YELLOW, 28).move_to([0, 1.5, 0])
        atp.t = 0.0
        atp.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.move_to([0.15 * np.sin(2 * m.t), 1.5 + 0.1 * np.cos(2.5 * m.t), 0]))[0])
        self.add(atp)
        self.finish()


class S07Answer(SpokenScene):
    def construct(self):
        t, don, acc, dg = tube_frame(self)
        l_don = lab("donor", [DONOR_X, 1.75, 0], TEXT, 30)
        l_acc = lab("acceptor", [ACC_X, 1.75, 0], TEXT, 30)
        q = qcard("Proof of within-stack vesicle transport?", 32, (0, 3.4, 0))
        mag = magnifier().move_to([0, 0.3, 0])
        self.add(l_don, l_acc, q, mag)
        bob(mag, [0, 0.3, 0])
        self.wait(0.3)
        self.at("Not on its own", lead=0.0)
        self.play(FadeOut(q), FadeOut(mag), run_time=1.0)
        self.at("assay inferred")
        br = VGroup(Line([-1.5, 1.15, 0], [1.5, 1.15, 0], color=TEXT, stroke_width=5),
                    Line([-1.5, 1.15, 0], [-1.5, 0.85, 0], color=TEXT, stroke_width=5),
                    Line([1.5, 1.15, 0], [1.5, 0.85, 0], color=TEXT, stroke_width=5))
        l_inf = lab("inferred: between populations", [0, 2.2, 0], TEXT, 28)
        self.play(Create(br), FadeIn(l_inf), run_time=1.6)
        self.at("did not watch")
        dbr = VGroup(DashedLine([-5.5, -1.6, 0], [-1.7, -1.6, 0], color=TEXT, stroke_width=4, dash_length=0.15),
                     Line([-5.5, -1.6, 0], [-5.5, -1.35, 0], color=TEXT, stroke_width=4),
                     Line([-1.7, -1.6, 0], [-1.7, -1.35, 0], color=TEXT, stroke_width=4))
        l_ns = lab("not seen: within one stack", [-3.0, -2.35, 0], TEXT, 26)
        qm = lab("?", [-3.6, -1.98, 0], TEXT, 30)
        self.play(Create(dbr), FadeIn(l_ns), FadeIn(qm), run_time=1.6)
        self.at("identify the carrier")
        car = VGroup(DashedVMobject(Circle(radius=0.45, color=TEXT, stroke_width=4), num_dashes=14), T("?", size=40, color=TEXT)).move_to([0, 0.0, 0])
        self.play(FadeIn(car, scale=0.5), run_time=1.0)
        self.wait(1.2)
        self.at("second picture", lead=1.0)
        fade = VGroup(t, don, acc, dg, br, l_inf, dbr, l_ns, qm, car, l_don, l_acc)
        er, tg, flow, sacs = stack_state()
        self.play(FadeOut(fade), FadeIn(er), FadeIn(tg), FadeIn(flow), *[FadeIn(s) for s in sacs], run_time=1.6)
        self.finish()


def sac_strip(sacs, cols=(0,)):
    return sacs


class S08Maturation(SpokenScene):
    def construct(self):
        er, tg, flow = backdrop()
        mid = Sac(SX[1], seed=21, gold=3)
        trn = Sac(SX[2], seed=22, gold=3)
        for s in (mid, trn):
            s.body.t = 0.0
        self.add(er, tg, flow, mid, trn)
        l_m = lab("cisternal maturation", [0, 3.1, 0], TEXT, 34)
        self.wait(0.3)
        self.play(FadeIn(l_m, shift=DOWN * 0.15), run_time=0.8)
        self.at("cisterna itself")
        self.play(Indicate(mid.body, color=GOLD, scale_factor=1.0), Indicate(trn.body, color=GOLD, scale_factor=1.0), run_time=1.4)
        self.at("forms at the cis face", lead=0.5)
        carriers = VGroup(*[plain_ves(0.2, 1).move_to([-5.95, y, 0]) for y in (1.1, 0.0, -1.1)])
        self.play(FadeIn(carriers), run_time=0.4)
        self.play(carriers.animate.move_to([-3.0, 0.2, 0]).scale(0.7), run_time=1.6)
        new = Sac(SX[0], seed=23, gold=3)
        self.play(FadeOut(carriers), FadeIn(new, scale=0.6), run_time=1.2)
        self.at("moves through the stack", lead=0.4)
        n2 = Sac(SX[0], seed=24, gold=2)
        shift = RIGHT * 3.0
        self.play(trn.animate.shift(shift).set_opacity(0), mid.animate.shift(shift), new.animate.shift(shift),
                  FadeIn(n2, scale=0.6), run_time=1.6, rate_func=smooth)
        self.remove(trn)
        self.at("ends as trans", lead=0.5)
        n3 = Sac(SX[0], seed=25, gold=2)
        self.play(mid.animate.shift(shift).set_opacity(0), new.animate.shift(shift), n2.animate.shift(shift),
                  FadeIn(n3, scale=0.6), run_time=1.6, rate_func=smooth)
        self.remove(mid)
        self.at("network", lead=0.3)
        # the gold-carrying sac frays into the tubular TGN net
        self.play(new.body.animate.set_stroke(opacity=0.35).set_fill(opacity=0.04), run_time=3.2)
        self.at("cargo remains")
        golds = new.golds
        self.play(*[g.animate.move_to([5.2 + 0.4 * i, 0.4 - 0.5 * i, 0]) for i, g in enumerate(golds)], run_time=2.2)
        self.finish()


class S09Recycle(SpokenScene):
    def construct(self):
        er, tg, flow = backdrop()
        Y = Sac(SX[0], seed=31, gold=2)
        N = Sac(SX[1], seed=32, gold=3)
        O = Sac(SX[2], seed=33, gold=2)
        self.add(er, tg, flow, Y, N, O)
        arrow = Arrow([2.6, -2.75, 0], [-2.8, -2.75, 0], buff=0, color=ORANGE, stroke_width=5, tip_length=0.25)
        prog = ValueTracker(0)
        N.add_updater(lambda m: m.shift(RIGHT * (SX[1] + 1.4 * prog.get_value() - m.body.get_center()[0])))
        Y.add_updater(lambda m: m.shift(RIGHT * (SX[0] + 1.4 * prog.get_value() - m.body.get_center()[0])))
        O.add_updater(lambda m: m.shift(RIGHT * (SX[2] + 1.4 * prog.get_value() - m.body.get_center()[0])))
        O.add_updater(lambda m: m.set_opacity(max(0.0, 1 - 1.6 * prog.get_value() ** 2)) if prog.get_value() > 0.6 else None)
        slow = lambda p, d: self.play(prog.animate.set_value(p), run_time=d, rate_func=linear)
        src = lambda: N.body.get_left() + LEFT * 0.0
        dst = lambda: Y.body.get_right() + RIGHT * 0.3
        self.wait(0.2)
        slow(0.12, 3.2)
        self.at("keep being carried")
        v1 = copi(0.32, ORANGE).move_to(N.body.get_left())
        self.add(v1)
        self.play(FadeIn(v1, scale=0.3), ride(v1, lambda: N.body.get_left() + LEFT * 0.35, dst, 2.4), prog.animate.set_value(0.28), run_time=2.4, rate_func=linear)
        self.at("COPI vesicles")
        l_c = lab("COPI", [0, 0.0, 0], BLUE, 26)
        l_c.add_updater(lambda m: m.move_to(v1.get_center() + UP * 0.95 + RIGHT * 0.45))
        self.add(l_c)
        self.play(prog.animate.set_value(0.38), Create(arrow), run_time=1.6, rate_func=linear)
        self.at("younger cisterna")
        Y.body.set_stroke(ORANGE, 8)
        self.play(FadeOut(v1), prog.animate.set_value(0.48), run_time=1.6, rate_func=linear)
        Y.body.set_stroke(BLUE, 4)
        self.remove(l_c)
        slow(0.55, 1.2)
        self.at("Backward recycling")
        v2 = copi(0.32, ORANGE).move_to(N.body.get_left())
        v3 = copi(0.32, MAGENTA).move_to(O.body.get_left())
        self.add(v2, v3)
        self.play(FadeIn(v2, scale=0.3), ride(v2, lambda: N.body.get_left() + LEFT * 0.35, dst, 2.2),
                  prog.animate.set_value(0.66), run_time=2.2, rate_func=linear)
        self.play(FadeOut(v2), run_time=0.2)
        self.at("later ones")
        self.play(FadeIn(v3, scale=0.3), ride(v3, lambda: O.body.get_left() + LEFT * 0.35, lambda: N.body.get_right() + RIGHT * 0.35, 2.0),
                  prog.animate.set_value(0.78), run_time=2.0, rate_func=linear)
        self.play(FadeOut(v3), run_time=0.6)
        self.at("sacs flow forward")
        self.play(prog.animate.set_value(0.92), flow[1].animate.shift(RIGHT * 0.8), run_time=1.6, rate_func=linear)
        self.at("enzymes keep going back")
        v4 = copi(0.32, ORANGE).move_to(N.body.get_left())
        self.add(v4)
        self.play(FadeIn(v4, scale=0.3), ride(v4, lambda: N.body.get_left() + LEFT * 0.35, dst, 1.8),
                  Indicate(arrow, color=ORANGE), prog.animate.set_value(1.0), run_time=1.8, rate_func=linear)
        self.play(FadeOut(v4), run_time=0.3)
        self.finish()


class S10Echo(SpokenScene):
    def construct(self):
        er, tg, flow = backdrop()
        sacs = big_sacs(41)
        for s in sacs:
            s.body.t = 0.0
        self.add(er, tg, flow, *sacs)
        arrow = Arrow([2.6, -2.75, 0], [-2.8, -2.75, 0], buff=0, color=ORANGE, stroke_width=5, tip_length=0.25)
        self.add(arrow)
        world = VGroup(er, tg, *sacs, arrow)
        er_cell = ch1.er_stack()
        loop = VMobject().set_points_smoothly([[-1.0, 1.9, 0], [-3.0, 2.8, 0], [-5.2, 2.2, 0], [-6.0, 1.0, 0]])
        self.at("That is", lead=0.0)
        self.play(world.animate.scale(0.8, about_point=[0, 0, 0]).shift(DOWN * 0.45), run_time=1.5)
        # ER sits off the left edge; the faint teal loop runs from the Golgi back to it
        erg = ch1.er_stack(0.8, np.array([-5.8, 0.55, 0.0]))
        loop = VMobject().set_points_smoothly([[-0.6, 1.95, 0], [-2.4, 2.9, 0], [-4.6, 2.7, 0], [-5.6, 1.3, 0]]).set_stroke(TEAL, 5, opacity=0.35)
        self.play(FadeIn(erg), Create(loop), run_time=1.6)
        dotT = Dot(radius=0.12, color=TEAL)
        dotT.t = 0.0

        def tp(m, dt):
            m.t += dt
            m.move_to(loop.point_from_proportion((m.t * 0.12) % 1.0))
        dotT.add_updater(tp)
        self.add(dotT)
        dotO = Square(side_length=0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=1)
        dotO.t = 0.0
        dotO.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.move_to(arrow.point_from_proportion(0.04 + 0.9 * ((m.t * 0.2) % 1.0)) if False else [2.4 - 5.0 * ((m.t * 0.2) % 1.0), -2.75, 0]))[0])
        self.add(dotO)
        self.at("recycling against the flow")
        both = lab("recycling against the flow", [3.4, 2.6, 0], TEXT, 30)
        bk = RoundedRectangle(width=both.width + 0.4, height=0.7, corner_radius=0.12, stroke_width=0, fill_color=INK, fill_opacity=0.92).move_to(both)
        self.play(loop.animate.set_stroke(TEAL, 6, opacity=1.0), arrow.animate.set_stroke(width=8), FadeIn(bk), FadeIn(both), run_time=1.0)
        self.wait(1.0)
        self.at("Golgi enzymes")
        own = lab("own machinery", [-0.2, -3.05, 0], ORANGE, 28)
        self.play(loop.animate.set_stroke(TEAL, 4, opacity=0.3), FadeOut(both), FadeOut(bk), FadeIn(own), run_time=1.2)
        self.finish()


def compare_panels(t0=0.0):
    L = Panel("stable", -3.4, -0.1, 0.75, period=7.0)
    R = Panel("mature", 3.4, -0.1, 0.75, period=7.0)
    return L, R


class S11Compare(SpokenScene):
    def construct(self):
        L, R = compare_panels()
        self.add(L.driver, R.driver)
        L.vis = 0.0
        R.vis = 0.0
        self.add(L.group, R.group)
        ll = lab("stable compartments", [-3.4, 2.9, 0], TEXT, 30)
        rl = lab("cisternal maturation", [3.4, 2.9, 0], TEXT, 30)
        sch = lab("schematic", [5.8, -3.45, 0], GREY, 24)
        self.at("pictures", lead=0.3)
        self.play(panel_fade(L, 1.0, 1.2), FadeIn(ll), run_time=1.2)
        self.play(panel_fade(R, 1.0, 1.2), FadeIn(rl), FadeIn(sch), run_time=1.2)
        self.at("In one")
        L.on = True
        self.wait(0.1)
        self.at("In the other")
        R.on = True
        self.at("from cis to trans")
        self.play(Indicate(rl, color=WHITE), run_time=1.0)
        self.finish()


class S12Open(SpokenScene):
    def construct(self):
        L, R = compare_panels()
        self.add(L.driver, R.driver, L.group, R.group)
        L.on = R.on = True
        L.t = R.t = 11.0
        ll = lab("stable compartments", [-3.4, 2.9, 0], TEXT, 30)
        rl = lab("cisternal maturation", [3.4, 2.9, 0], TEXT, 30)
        self.add(ll, rl)
        self.at("Which is right", lead=0.0)
        qm = lab("?", [0, 0.1, 0], TEXT, 80)
        self.play(FadeIn(qm, scale=0.4), run_time=0.8)
        self.at("one filmed cisterna")
        cam = VGroup(RoundedRectangle(width=0.9, height=0.55, corner_radius=0.1, stroke_color=TEXT, stroke_width=4),
                     Circle(radius=0.17, stroke_color=TEXT, stroke_width=4)).move_to([3.4, 1.8, 0])
        tg = lab("predict timing in the text", [3.4, -2.4, 0], TEXT, 26)
        self.play(FadeIn(cam, scale=0.5), FadeIn(tg), run_time=0.9)
        bob(cam, [3.4, 2.1, 0], 0.1)
        self.at("stacked mammalian")
        o1 = lab("mammalian stack: open", [-3.4, -2.45, 0], TEXT, 26)
        o2 = lab("mammalian stack: open", [3.4, -2.45, 0], TEXT, 26)
        self.play(FadeOut(tg), FadeIn(o1), FadeIn(o2), FadeOut(qm), run_time=0.9)
        self.at("no single model")
        outl = RoundedRectangle(width=13.0, height=6.9, corner_radius=0.3, stroke_color=TEXT, stroke_width=3).move_to([0, 0.0, 0])
        self.play(Create(outl), run_time=1.6)
        self.at("best candidate")
        core = lab("proposed shared core", [3.4, -3.05, 0], TEXT, 28)
        self.play(FadeIn(core), Indicate(rl, color=WHITE), run_time=1.0)
        gl = lab("Glick & Luini", [-4.9, -3.05, 0], GREY, 26)
        self.play(FadeIn(gl), run_time=0.6)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        org, flow, sacs = mini_world()
        for s in sacs:
            s.clear_updaters()
        st = mini_stream()
        q = qcard("Cargo moves. Enzymes stay. How?")
        q.set_opacity(0.0)
        self.add(org, flow, st)
        P = Panel("stable", GOLGI_X[1], 0.0, 0.322, kh=0.522, bs=0.34, period=6.0)
        M = Panel("mature", GOLGI_X[1], 0.0, 0.322, kh=0.522, bs=0.34, period=6.0)
        M.vis = 0.0
        self.add(P.driver, M.driver, P.group, M.group, q)
        P.on = True
        self.play(q.animate.set_opacity(0.55), run_time=0.8)
        self.at("Fixed sacs")
        self.wait(0.6)
        self.at("or moving sacs")
        self.play(panel_fade(P, 0.0, 0.8), panel_fade(M, 1.0, 0.8), run_time=0.8)
        M.on = True
        self.at("Either way")
        self.play(*[c.animate.set_stroke(TEXT, 5) for c in flow[1]], gate_to(st, 1.0, 0.1), FadeOut(q), run_time=1.0)
        self.finish()


class S14End(EndCard):
    LINE = "Cargo crosses the Golgi by vesicles or maturation; the question remains open."
