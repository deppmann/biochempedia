"""Sensing the World: a fall can carry a signal  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the stimulus from outside (a photon of light, an odorant, nitric oxide)
  BLUE   = the receptor (rhodopsin, the odorant receptor)
  GOLD   = retinal, the receptor's own built-in ligand
  PURPLE = the G protein (transducin, the nose's G protein)
  ORANGE = the enzyme the G protein switches on (PDE6, adenylyl cyclase)
  TEAL   = the cyclic messenger that holds a channel open (cGMP, cAMP)
  GREEN  = open / flowing / active (an open gate, the inward current, an active protein)
  RED    = shut / a fall / off (a closed gate, a drop in level, an inactive receptor)
  PINK   = the transmitter, glutamate
  GREY   = membranes, axes, labels, ghosts

No molecular structures: the receptor is a rounded block, retinal is a labelled chip whose name changes
from bent to straight, a channel is two posts in the membrane with a hinged gate, a messenger is a chip,
a current is a stream of dots, and every trace is computed from an equation.

Framings (the same rod, rebuilt where the action is):
  A  (s02)      channels at mid-height, ions falling in from above, the messenger pool below, traces at right
  B  (s03-s05)  the whole channel row lifted to the top, the chain of events along the bottom or traces below
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08BB4"

XS = [-4.5, -2.3, -0.1, 2.1]       # channel centres
OPEN_IDX = [0, 1, 3]               # the channels cGMP holds open in the dark ("some of them")
GAP, POST, MT = 0.9, 0.22, 0.6     # gate gap, post width, membrane thickness
X0, X1 = -6.3, 3.2                 # membrane extent
YA, YB = 0.6, 2.5                  # membrane height in framings A and B
DXB = 1.5                          # framing B slides the row right so it is centred
CHIP = 28                          # text size of messenger chips

POOL1 = [-4.4, -2.2, 0.0, 2.2]     # pool rows (x), y = membrane y - 1.85 and - 3.15
POOL2 = [-3.3, -1.1, 1.1]
BOUND_FROM = [0, 1, 3]             # POOL1 index of the chips that go and bind (to channels 0, 1, 3)


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=24, pad=0.14, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through. [back, box, label]"""
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def bchip2(text, color=BLUE, size=24, pad=0.16):
    """a two-line chip with an opaque backing. [back, box, label]"""
    label = T(text, size, color, line_spacing=0.8)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, box, label).move_to(ORIGIN)


def pulse(c, color, s=1.1, **kw):
    return Indicate(VGroup(*c[1:]), color=color, scale_factor=s, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def ghost_of(c):
    """a dashed outline where a chip used to be."""
    box = RoundedRectangle(corner_radius=0.14, width=c[1].width, height=c[1].height).move_to(c[1])
    return DashedVMobject(box, num_dashes=24).set_color(GREY)


def photon(x, y):
    halo = Circle(radius=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.22)
    core = Dot(radius=0.13, color=YELLOW)
    return VGroup(halo, core).move_to([x, y, 0])


class Stream(VGroup):
    """dots that fall for ever through a channel: an ion current (or a drip of transmitter)."""

    def __init__(self, x, y_top, y_bot, n=9, color=GREEN, speed=1.5, jitter=0.14, seed=0, r=0.075):
        super().__init__()
        rng = np.random.RandomState(seed)
        self.y_top, self.y_bot, self.speed = y_top, y_bot, speed
        self.master = 1.0
        self.mult = np.ones(n)
        H = y_top - y_bot
        for i in range(n):
            self.add(Dot([x + rng.uniform(-jitter, jitter), y_bot + H * (i + rng.uniform(0, 0.5)) / n, 0], radius=r, color=color))
        self.add_updater(self._step)
        self._step(self, 0)

    def _step(self, m, dt):
        H = self.y_top - self.y_bot
        for i, d in enumerate(self.submobjects):
            c = d.get_center()
            ny = c[1] - self.speed * dt
            if ny < self.y_bot:
                ny += H
            d.move_to([c[0], ny, 0])
            edge = min(ny - self.y_bot, self.y_top - ny)
            d.set_opacity(float(np.clip(edge / 0.35, 0, 1)) * self.master * self.mult[i])

    def fade(self, target, run_time=0.5):
        v0 = self.master
        return UpdateFromAlphaFunc(Mobject(), lambda m, a: setattr(self, "master", v0 + (target - v0) * a), run_time=run_time)

    def thin(self, keep, run_time=0.8):
        m0 = self.mult.copy()
        tgt = np.array([1.0 if i < keep else 0.0 for i in range(len(self.submobjects))])
        return UpdateFromAlphaFunc(Mobject(), lambda m, a: setattr(self, "mult", m0 + (tgt - m0) * a), run_time=run_time)


def resp(u):
    """a rod's response to one photon: rises to its peak at u = 1, then recovers slowly (computed, not drawn by hand)."""
    u = np.maximum(u, 0.0)
    return (u * np.exp(1 - u)) ** 3


class Panel(VGroup):
    """A small plot: axes, title and the flat dark trace.  .dip(u_end) is the response to a photon."""

    def __init__(self, x0, x1, y_axis, y_top, title, color, base, depth, t0=0.42, tp=0.1, tsize=22):
        super().__init__()
        self.x0, self.x1, self.base, self.dep, self.t0, self.tp, self.col = x0, x1, base, depth, t0, tp, color
        self.axes = VGroup(Line([x0, y_axis, 0], [x0, y_top, 0], color=GREY, stroke_width=3),
                           Line([x0, y_axis, 0], [x1, y_axis, 0], color=GREY, stroke_width=3))
        self.title = T(title, tsize, color).move_to([x0 + 0.12, y_top - 0.22, 0], aligned_edge=LEFT)
        self.flat = Line([self.xm(0.0), base, 0], [self.xm(t0), base, 0], color=color, stroke_width=5)
        self.add(self.axes, self.title, self.flat)

    def xm(self, t):
        return self.x0 + 0.15 + t * (self.x1 - self.x0 - 0.3)

    def dip(self, u_end=None):
        """the fall after a photon.  u_end=1 stops at the trough; None runs on until the trace has recovered."""
        u_max = (1 - self.t0) / self.tp
        u_end = u_max if u_end is None else min(u_end, u_max)
        us = np.linspace(0, u_end, 90)
        pts = [[self.xm(self.t0 + self.tp * u), self.base - self.dep * float(resp(u)), 0] for u in us]
        return VMobject(stroke_color=self.col, stroke_width=5).set_points_as_corners(pts)

    def trough(self):
        return np.array([self.xm(self.t0 + self.tp), self.base - self.dep, 0])


# ---------------------------------------------------------------------------------------------
# the channel row
# ---------------------------------------------------------------------------------------------
class ChanRow:
    """A membrane with four channels. Each channel is two posts and a hinged gate (green = open, red = shut).
    dx slides the whole row sideways (framing B centres it)."""

    def __init__(self, ym, open_idx=(), dx=0.0):
        self.ym, self.dx = ym, dx
        self.xs = [x + dx for x in XS]
        self.segs, self.posts, self.flaps = VGroup(), VGroup(), []
        prev = X0 + dx
        for x in self.xs:
            self.segs.add(self._seg(prev, x - GAP / 2 - POST))
            prev = x + GAP / 2 + POST
            for s in (-1, 1):
                px = x + s * (GAP / 2 + POST / 2)
                self.posts.add(RoundedRectangle(corner_radius=0.06, width=POST, height=MT + 0.5, stroke_color=GREY,
                                                stroke_width=3, fill_color=GREY, fill_opacity=0.65).move_to([px, ym, 0]))
        self.segs.add(self._seg(prev, X1 + dx))
        for i, x in enumerate(self.xs):
            f = RoundedRectangle(corner_radius=0.05, width=GAP, height=0.16, stroke_color=RED, stroke_width=2,
                                 fill_color=RED, fill_opacity=0.95).move_to([x, ym, 0])
            self.flaps.append(f)
            if i in open_idx:
                f.rotate(PI / 2, about_point=self.pivot(i)).set_color(GREEN)
        self.group = VGroup(self.segs, self.posts, *self.flaps)

    def _seg(self, a, b):
        return RoundedRectangle(corner_radius=0.08, width=b - a, height=MT, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.35).move_to([(a + b) / 2, self.ym, 0])

    def pivot(self, i):
        return np.array([self.xs[i] - GAP / 2 + 0.08, self.ym, 0])

    def bound_xy(self, i):
        return np.array([self.xs[i] - 0.95, self.ym - (MT + 0.5) / 2 - 0.33, 0])

    def pool_xy(self, row, k):
        y = self.ym - (1.75 if row == 1 else 3.25)
        return np.array([(POOL1 if row == 1 else POOL2)[k] + self.dx, y, 0])

    def swing(self, i, opening, run_time=0.5):
        f, P = self.flaps[i], self.pivot(i)
        start = f.copy()
        ang = PI / 2 if opening else -PI / 2
        c0, c1 = (ManimColor(RED), ManimColor(GREEN)) if opening else (ManimColor(GREEN), ManimColor(RED))

        def upd(m, a):
            m.become(start.copy().rotate(a * ang, about_point=P).set_color(interpolate_color(c0, c1, a)))
        return UpdateFromAlphaFunc(f, upd, run_time=run_time)


def pool_chips(row, label="cGMP", color=TEAL):
    """the seven free chips of a pool (rows 1 and 2), as a list in POOL1 then POOL2 order."""
    out = []
    for k in range(len(POOL1)):
        out.append(bchip(label, color, CHIP).move_to(row.pool_xy(1, k)))
    for k in range(len(POOL2)):
        out.append(bchip(label, color, CHIP).move_to(row.pool_xy(2, k)))
    return out


def ion(label, x, y, y_end=-0.7, speed=3.0):
    """a labelled ion that falls on its own (an updater), so the scene does not wait for it."""
    c = Circle(radius=0.31, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.22)
    t = T(label, 22, TEXT).move_to(c)
    g = VGroup(c, t).move_to([x, y, 0])

    def upd(m, dt):
        m.shift(DOWN * speed * dt)
        v = float(np.clip((m.get_center()[1] - y_end) / 0.5, 0, 1))
        c.set_stroke(opacity=v).set_fill(opacity=0.22 * v)
        t.set_opacity(v)
        if v <= 0:
            m.clear_updaters()
    g.add_updater(upd)
    return g


def panels_narrow():
    top = Panel(3.9, 6.25, 0.35, 3.35, "inward current", GREEN, base=2.2, depth=1.1)
    bot = Panel(3.9, 6.25, -3.3, -0.15, "transmitter", PINK, base=-1.25, depth=1.1)
    return top, bot


class Film(SpokenScene):
    def outro(self, *anims, then=None, run_time=0.45):
        """hold until the narration ends, clear what the next scene does not inherit, then reframe."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        if anims:
            self.play(*anims, run_time=run_time)
        if then:
            self.play(*then, run_time=0.9)
            self.wait(0.1)
        self.finish()


class S00Title(TitleCard):
    LESSON = "Sensing the World"
    TITLE = "A fall can carry a signal"


# ---------------------------------------------------------------------------------------------
class S01Dip(Film):
    """one photon, a current switched off: the puzzle is a fall."""

    def construct(self):
        RX = -4.7
        rod = RoundedRectangle(corner_radius=0.8, width=2.0, height=4.8, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.12).move_to([RX, 0.4, 0])
        rod_lbl = T("rod cell", 28, TEXT).move_to([RX, 0.4, 0])
        self.play(Create(rod), FadeIn(rod_lbl), run_time=0.8)

        # the photon waits above the rod
        ph = photon(RX, 3.15)
        ph_lbl = T("photon", 24, YELLOW).next_to(ph, RIGHT, buff=0.15)
        self.at("single photon")
        self.play(FadeIn(ph, scale=0.5), FadeIn(ph_lbl), run_time=0.5)

        # the current: arrows crossing into the rod
        ins = VGroup()
        for y in (1.6, 0.4, -0.8):
            ins.add(Arrow([-6.3, y, 0], [-5.75, y, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.2))
            ins.add(Arrow([-3.1, y, 0], [-3.65, y, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.2))
        top = Panel(-1.9, 6.2, 0.7, 3.35, "inward current", GREEN, base=2.25, depth=1.2)
        bot = Panel(-1.9, 6.2, -3.3, -0.55, "transmitter", PINK, base=-1.6, depth=1.2)
        self.at("reports that")
        self.play(Indicate(ph[1], color=TEXT, scale_factor=1.6), run_time=0.7)
        self.at("switching a current off")
        self.play(FadeIn(top.axes), FadeIn(top.title), run_time=0.5)
        self.at("In the dark")
        self.play(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.1), run_time=0.9)
        self.at("steady inward current")
        self.play(Create(top.flat), run_time=1.0)

        # transmitter: a steady drip from the foot of the rod
        drip = Stream(RX, -2.05, -3.4, n=6, color=PINK, speed=1.2, jitter=0.12, seed=2, r=0.08)
        drip_lbl = T("transmitter", 22, PINK).move_to([RX + 1.55, -2.75, 0])
        self.at("releases transmitter")
        self.add(drip)
        self.play(FadeIn(bot.axes), FadeIn(bot.title), FadeIn(drip_lbl), Create(bot.flat), run_time=1.0)

        # light: the photon drops in and both traces dip
        mark_t = DashedLine([top.xm(top.t0), 3.2, 0], [top.xm(top.t0), 0.7, 0], color=YELLOW, stroke_width=3, dash_length=0.12)
        mark_b = DashedLine([bot.xm(bot.t0), -0.6, 0], [bot.xm(bot.t0), -3.3, 0], color=YELLOW, stroke_width=3, dash_length=0.12)
        self.at("Light reduces both")
        d_top, d_bot = top.dip(), bot.dip()
        self.play(ph.animate.move_to([RX, 2.2, 0]), FadeOut(ph_lbl), run_time=0.3, rate_func=rush_into)
        self.play(Flash(ph.get_center(), color=YELLOW, line_length=0.3, flash_radius=0.4), FadeOut(ph), FadeIn(mark_t),
                  FadeIn(mark_b), Create(d_top), Create(d_bot), ins.animate.set_opacity(0.25), drip.thin(2, 1.0),
                  run_time=1.3, rate_func=linear)

        # the puzzle: a fall, and nothing yet says why it should mean anything
        tr = top.trough()
        fall = Arrow([top.xm(top.t0) - 0.4, top.base, 0], [top.xm(top.t0) - 0.4, tr[1], 0], buff=0, color=RED, stroke_width=8, tip_length=0.25)
        fall_lbl = T("a fall", 28, RED, weight=BOLD).next_to(fall, LEFT, buff=0.15)
        box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.0, height=0.8), num_dashes=30).set_color(GREY)
        q = T("signal?", 28, TEXT, weight=BOLD)
        sig = VGroup(box, q).move_to([4.8, 1.55, 0])
        self.at("How can a fall")
        self.play(GrowArrow(fall), FadeIn(fall_lbl), run_time=0.6)
        self.at("signal")
        self.play(Create(box), FadeIn(q), run_time=0.7)
        self.play(pop(q, 1.2), run_time=0.5)

        # reframe: the rod and its photon go; the two traces move to the right and reset to the dark
        n_top, n_bot = panels_narrow()
        self.outro(FadeOut(VGroup(rod, rod_lbl, ins, drip, drip_lbl, mark_t, mark_b, fall, fall_lbl, sig, d_top, d_bot)),
                   then=[Transform(top.axes, n_top.axes), Transform(top.title, n_top.title), Transform(top.flat, n_top.flat),
                         Transform(bot.axes, n_bot.axes), Transform(bot.title, n_bot.title), Transform(bot.flat, n_bot.flat)])


# ---------------------------------------------------------------------------------------------
class S02Hold(Film):
    """in the dark, cGMP holds channels open; the inflow is the dark current. (framing A)"""

    def construct(self):
        top, bot = panels_narrow()
        self.add(top.axes, top.title, top.flat, bot.axes, bot.title, bot.flat)
        row = ChanRow(YA)
        chips = pool_chips(row)                                   # 4 on row one, 3 on row two
        out_lbl = T("outside", 22, GREY).move_to([-5.75, 2.95, 0])
        in_lbl = T("inside", 22, GREY).move_to([-5.75, -1.9, 0])

        # the messenger, already in the cell
        self.at("rod contains")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in chips], lag_ratio=0.1), FadeIn(in_lbl), run_time=1.3)

        self.at("called")
        self.play(LaggedStart(*[pulse(c, TEAL, 1.1) for c in chips], lag_ratio=0.08), run_time=0.9)

        # the channels, all shut
        self.at("binds directly")
        self.play(FadeIn(row.group), FadeIn(out_lbl), run_time=0.7)
        ch_lbl = T("cation channels", 26, GREY).move_to([row.xs[2], 1.85, 0])
        self.at("cation channels")
        self.play(FadeIn(ch_lbl, shift=DOWN * 0.1), run_time=0.5)

        # three chips fly up and bind directly; then their gates swing open
        movers = [chips[k] for k in BOUND_FROM]
        self.at("no kinase")
        self.play(*[m.animate.move_to(row.bound_xy(i)) for m, i in zip(movers, OPEN_IDX)], run_time=1.0)
        self.at("holds some")
        self.play(*[row.swing(i, True, 0.55) for i in OPEN_IDX], run_time=0.55)

        # sodium and calcium
        na = ion("Na⁺", row.xs[0] + 0.1, 3.2)
        ca = ion("Ca²⁺", row.xs[1] + 0.1, 3.2)
        self.at("Sodium")
        self.add(na)
        self.at("calcium")
        self.add(ca)
        streams = [Stream(row.xs[i], 3.4, -0.55, n=9, speed=1.6, seed=i) for i in OPEN_IDX]
        for s in streams:
            s.master = 0.0
        self.add(*streams)
        self.at("through those")
        self.play(*[s.fade(1.0, 0.7) for s in streams], run_time=0.7)

        dc = T("dark current", 30, GREEN, weight=BOLD).move_to([row.xs[2], 1.85, 0])
        self.at("dark current")
        self.play(FadeTransform(ch_lbl, dc), Indicate(top.flat, color=TEXT, scale_factor=1.0), run_time=0.7)

        self.at("Because of it")
        self.play(Indicate(dc, color=TEXT, scale_factor=1.08), run_time=0.6)
        self.at("partly depolarized")
        self.play(Indicate(row.segs, color=GREEN, scale_factor=1.0), run_time=0.8)
        gl = T("glutamate", 22, PINK).move_to(bot.title, aligned_edge=LEFT)
        self.at("releases glutamate")
        self.play(FadeTransform(bot.title, gl), Indicate(bot.flat, color=TEXT, scale_factor=1.0), run_time=0.7)

        # continuously: a cursor runs along each flat trace
        dots = [Dot([tp.flat.get_left()[0], tp.base, 0], radius=0.09, color=TEXT) for tp in (top, bot)]
        self.at("continuously")
        self.add(*dots)
        self.play(*[d.animate.move_to([tp.flat.get_right()[0], tp.base, 0]) for d, tp in zip(dots, (top, bot))],
                  run_time=1.0, rate_func=linear)
        self.play(FadeOut(dots[0]), FadeOut(dots[1]), run_time=0.2)

        # the baseline
        bl_t = DashedLine([top.flat.get_right()[0], top.base, 0], [top.x1 - 0.05, top.base, 0], color=GREY, stroke_width=3, dash_length=0.12)
        bl_b = DashedLine([bot.flat.get_right()[0], bot.base, 0], [bot.x1 - 0.05, bot.base, 0], color=GREY, stroke_width=3, dash_length=0.12)
        bl_lbl = T("baseline", 22, GREY).next_to(bl_t, UP, buff=0.1)
        self.at("this baseline")
        self.play(Create(bl_t), Create(bl_b), FadeIn(bl_lbl), run_time=0.8)

        # reframe to B: lift the channel row; the cation current and the traces make room for the cascade
        shift_up = UP * (YB - YA) + RIGHT * DXB
        self.outro(FadeOut(VGroup(*streams, top.axes, top.title, top.flat, bot.axes, bot.flat, gl, bl_t, bl_b, bl_lbl, dc, out_lbl, in_lbl)),
                   then=[row.group.animate.shift(shift_up), *[c.animate.shift(shift_up) for c in chips]])


# ---------------------------------------------------------------------------------------------
class S03Light(Film):
    """light turns retinal; rhodopsin, transducin, PDE6; PDE6 destroys the cGMP that was already there. (framing B)"""

    def construct(self):
        row = ChanRow(YB, open_idx=OPEN_IDX, dx=DXB)
        chips = pool_chips(row)
        for k, i in zip(BOUND_FROM, OPEN_IDX):
            chips[k].move_to(row.bound_xy(i))
        streams = [Stream(row.xs[i], 3.4, 1.3, n=5, speed=1.4, seed=i) for i in OPEN_IDX]
        self.add(row.group, *chips, *streams)

        YC = -2.45
        blob = RoundedRectangle(corner_radius=0.35, width=3.9, height=1.9, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.18).move_to([-3.9, YC, 0])
        rho = T("rhodopsin", 28, BLUE, weight=BOLD).move_to([-5.6, YC + 0.5, 0], aligned_edge=LEFT)
        off = T("off", 26, RED, weight=BOLD).move_to([-2.3, YC + 0.5, 0], aligned_edge=RIGHT)
        ret = bchip("bent retinal", GOLD, CHIP).move_to([-3.9, YC - 0.35, 0])
        self.play(FadeIn(VGroup(blob, rho)), run_time=0.5)
        self.at("bent molecule")
        self.play(FadeIn(ret, shift=UP * 0.12), run_time=0.5)
        self.at("While")
        self.play(pulse(ret, GOLD, 1.08), run_time=0.6)
        self.at("stays off")
        self.play(FadeIn(off, scale=0.8), run_time=0.4)

        # light straightens the retinal
        ph = photon(-7.0, YC - 0.35)
        self.at("A photon")
        self.add(ph)
        self.play(ph.animate.move_to([-5.95, YC - 0.35, 0]), run_time=0.6, rate_func=rush_into)
        self.play(Flash(ph.get_center(), color=YELLOW, line_length=0.3, flash_radius=0.4), FadeOut(ph), run_time=0.35)
        straight = bchip("straight retinal", GOLD, CHIP).move_to(ret)
        self.at("straightens")
        self.play(FadeTransform(ret, straight), run_time=0.7)
        ret = straight
        act = T("active", 26, GREEN, weight=BOLD).move_to(off, aligned_edge=RIGHT)
        self.at("becomes active")
        self.play(blob.animate.set_stroke(GREEN, 7), FadeTransform(off, act), pop(rho, 1.12), run_time=0.7)

        # the chain of switches
        trans = bchip("transducin", PURPLE, 28).move_to([-0.1, YC, 0])
        gp = T("G protein", 22, GREY).move_to([-0.1, YC - 0.62, 0])
        a1 = arr([-1.9, YC, 0], [-1.25, YC, 0], GREEN, w=6)
        self.at("switches on transducin")
        self.play(GrowArrow(a1), FadeIn(trans), run_time=0.6)
        self.at("G protein")
        self.play(FadeIn(gp), pulse(trans, PURPLE, 1.08), run_time=0.5)
        pde = bchip("PDE6", ORANGE, 28).move_to([4.3, YC, 0])
        a2 = arr([1.05, YC, 0], [3.6, YC, 0], GREEN, w=6)
        pde_lbl = T("phosphodiesterase", 22, GREY).move_to([4.3, YC - 0.62, 0])
        self.at("transducin switches on")
        self.play(trans[1].animate.set_stroke(GREEN, 5), GrowArrow(a2), FadeIn(pde), run_time=0.7)
        self.play(pde[1].animate.set_stroke(GREEN, 5), run_time=0.3)
        self.at("a phosphodiesterase")
        self.play(FadeIn(pde_lbl), run_time=0.4)

        # PDE6 reaches the cGMP and destroys it
        self.at("This enzyme")
        self.play(pde.animate.move_to([4.3, 0.0, 0]), FadeOut(VGroup(a2, gp, pde_lbl)), trans[1].animate.set_stroke(PURPLE, 3), run_time=0.7)
        self.at("destroys")
        ghosts = VGroup(*[ghost_of(c) for c in chips])
        order = sorted(range(len(chips)), key=lambda k: -chips[k].get_center()[0])
        kills = []
        for k in order:
            kills.append(Succession(AnimationGroup(chips[k][1].animate.set_stroke(RED), chips[k][2].animate.set_color(RED), run_time=0.15),
                                    FadeOut(chips[k], scale=0.3, run_time=0.3)))
        self.play(LaggedStart(*kills, lag_ratio=0.18), FadeIn(ghosts, run_time=1.6), run_time=2.0)
        self.at("already there")
        self.play(pulse(pde, ORANGE, 1.1), run_time=0.6)

        self.outro(FadeOut(VGroup(ghosts, pde, trans, a1, blob, rho, act, ret, *streams)))


# ---------------------------------------------------------------------------------------------
class S04Close(Film):
    """cGMP falls, the gates shut, the current and the glutamate fall. (framing B, traces below)"""

    def construct(self):
        row = ChanRow(YB, open_idx=OPEN_IDX, dx=DXB)
        streams = [Stream(row.xs[i], 3.4, 1.3, n=5, speed=1.4, seed=i) for i in OPEN_IDX]
        self.add(row.group, *streams)

        cur = Panel(-6.2, -0.4, -3.3, 0.95, "inward current", GREEN, base=-0.2, depth=1.9)
        glu = Panel(0.5, 6.2, -3.3, 0.95, "glutamate", PINK, base=-0.2, depth=1.9)
        self.play(FadeIn(cur), FadeIn(glu), run_time=0.7)

        # the level of cGMP
        gx = -5.6
        gauge_o = Rectangle(width=0.5, height=1.5, stroke_color=TEAL, stroke_width=3).move_to([gx, 2.0, 0])
        gauge_f = Rectangle(width=0.5, height=1.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.85).move_to(gauge_o)
        g_lbl = T("cGMP", 26, TEAL, weight=BOLD).move_to([gx, 3.15, 0])
        self.at("falls")
        self.play(FadeIn(gauge_o), FadeIn(gauge_f), FadeIn(g_lbl), run_time=0.3)
        shrunk = Rectangle(width=0.5, height=0.04, stroke_width=0, fill_color=RED, fill_opacity=0.85).move_to(gauge_o.get_bottom() + UP * 0.02)
        self.play(Transform(gauge_f, shrunk), run_time=0.7)

        # the gates shut and the ions stop
        self.at("channels close")
        self.play(*[s.fade(0.0, 0.7) for s in streams],
                  LaggedStart(*[row.swing(i, False, 0.5) for i in OPEN_IDX], lag_ratio=0.25), run_time=1.3)
        self.remove(*streams)

        # the current falls
        d_cur = cur.dip(1.0)
        self.at("current shrinks")
        self.play(Create(d_cur), run_time=1.3, rate_func=linear)
        self.at("membrane")
        self.play(Indicate(row.segs, color=TEXT, scale_factor=1.0), run_time=0.8)

        d_glu = glu.dip(1.0)
        self.at("release drops")
        self.play(Create(d_glu), run_time=1.3, rate_func=linear)
        nxt = bchip("next cell", GREY, 26).move_to([5.1, -1.0, 0])
        tg = glu.trough()
        link = arr([tg[0] + 0.15, tg[1] - 0.05, 0], [nxt.get_left()[0] - 0.05, nxt.get_center()[1], 0], GREY)
        self.at("next cell")
        self.play(GrowArrow(link), FadeIn(nxt, shift=LEFT * 0.1), run_time=0.6)

        # the sizes, from the toad rod recording
        trod = T("toad rod", 22, GREY).next_to(cur.title, RIGHT, buff=0.35)
        self.at("toad rod")
        self.play(FadeIn(trod, shift=LEFT * 0.1), run_time=0.4)
        n20 = M("roughly 20 pA", 22, GREEN).move_to([cur.xm(0.0), -0.2 + 0.4, 0], aligned_edge=LEFT)
        self.at("roughly")
        self.play(FadeIn(n20, shift=DOWN * 0.1), Indicate(cur.flat, color=TEXT, scale_factor=1.0), run_time=0.8)
        tc = cur.trough()
        shut = T("all channels shut", 22, GREY).move_to([tc[0] + 0.3, tc[1] + 0.35, 0], aligned_edge=LEFT)
        nx = cur.xm(0.2)
        notch = VMobject(stroke_color=RED, stroke_width=5).set_points_as_corners(
            [[nx + 0.5 * u, cur.base - 0.095 * float(resp(u * 1.0 + 0.0)) , 0] for u in np.linspace(0, 1.4, 40)])
        brk = Arrow([nx + 0.7, cur.base, 0], [nx + 0.7, cur.base - 0.095, 0], buff=0, color=RED, stroke_width=3, tip_length=0.06)
        n1 = M("about 1 pA", 22, RED).move_to([nx, cur.base - 0.6, 0], aligned_edge=LEFT)
        ptr = Line([nx + 0.7, cur.base - 0.12, 0], [nx + 0.7, cur.base - 0.42, 0], color=RED, stroke_width=2)
        ns = T("not to scale", 24, TEXT, weight=BOLD).move_to([cur.x1 - 0.1, -3.0, 0], aligned_edge=RIGHT)
        self.at("Each rhodopsin")
        self.play(FadeIn(shut), FadeIn(ns), run_time=0.5)
        self.play(Create(notch), GrowArrow(brk), Create(ptr), FadeIn(n1), run_time=0.8)

        self.outro(FadeOut(VGroup(cur, glu, d_cur, d_glu, gauge_o, gauge_f, g_lbl, nxt, link, trod, n20, brk, n1, ns, shut, notch, ptr)))


# ---------------------------------------------------------------------------------------------
class S05Nose(Film):
    """the nose: one receptor, an odorant, a G protein, a cyclase; cAMP rises and opens the same kind of channel. (framing B)"""

    def construct(self):
        row = ChanRow(YB, dx=DXB)
        self.add(row.group)
        chips = pool_chips(row, "cAMP", TEAL)
        YC = -2.45

        nose = T("nose", 28, GREY).move_to([row.xs[2], 3.15, 0])
        self.play(FadeIn(nose, shift=DOWN * 0.1), run_time=0.6)
        sens = T("sensory neuron", 26, GREY).move_to(nose)

        # one receptor, chosen from a very large family
        fam = [bchip("receptor", GREY, 22).move_to(row.pool_xy(1, k)) for k in range(4)] + \
              [bchip("receptor", GREY, 22).move_to(row.pool_xy(2, k)) for k in range(3)]
        pick = fam[1]
        self.at("sensory neuron")
        self.play(FadeTransform(nose, sens), LaggedStart(*[FadeIn(c, scale=0.8) for c in fam], lag_ratio=0.1), run_time=1.1)
        self.at("one receptor")
        self.play(pick[1].animate.set_stroke(BLUE, 4).set_fill(BLUE, 0.2), pick[2].animate.set_color(BLUE), run_time=0.5)
        self.at("very large family")
        others = [c for c in fam if c is not pick]
        self.play(LaggedStart(*[pulse(c, GREY, 1.12) for c in others], lag_ratio=0.1), run_time=1.0)
        rec = bchip("receptor", BLUE, 28).move_to([-3.15, YC, 0])
        self.play(FadeOut(VGroup(*others)), ReplacementTransform(pick, rec), run_time=0.8)

        # odorant binds
        odo = bchip("odorant", YELLOW, 28).move_to([-5.4, YC, 0])
        self.at("An odorant")
        self.play(FadeIn(odo, shift=RIGHT * 0.15), run_time=0.5)
        self.at("binds its receptor")
        self.play(odo.animate.move_to([-4.87, YC, 0]), rec[1].animate.set_stroke(GREEN, 5), run_time=0.6)

        # G protein, then the cyclase
        gp = bchip("G protein", PURPLE, 28).move_to([-0.5, YC, 0])
        a1 = arr([-2.25, YC, 0], [-1.5, YC, 0], GREEN, w=6)
        self.at("G protein then")
        self.play(GrowArrow(a1), FadeIn(gp), run_time=0.6)
        cyc = bchip2("adenylyl\ncyclase", ORANGE, 28).move_to([2.1, YC, 0])
        a2 = arr([0.5, YC, 0], [1.2, YC, 0], GREEN, w=6)
        self.at("an enzyme")
        self.play(gp[1].animate.set_stroke(GREEN, 5), GrowArrow(a2), FadeIn(cyc), run_time=0.7)
        self.play(cyc[1].animate.set_stroke(GREEN, 5), run_time=0.3)

        # cAMP rises: chips pour up from the cyclase into the cell
        ups = []
        for c in chips:
            target = c.get_center().copy()
            c.move_to([2.1, YC + 0.9, 0])
            ups.append(Succession(FadeIn(c, scale=0.6, run_time=0.25), c.animate(run_time=0.9, path_arc=0.5).move_to(target)))
        self.at("The messenger")
        self.play(LaggedStart(*ups, lag_ratio=0.12), run_time=2.2)

        # it opens the channel directly
        movers = [chips[k] for k in BOUND_FROM]
        self.at("directly opens")
        self.play(*[m.animate.move_to(row.bound_xy(i)) for m, i in zip(movers, OPEN_IDX)], run_time=0.9)
        self.play(*[row.swing(i, True, 0.5) for i in OPEN_IDX], run_time=0.5)
        streams = [Stream(row.xs[i], 3.4, 1.3, n=5, speed=1.4, seed=i) for i in OPEN_IDX]
        for s in streams:
            s.master = 0.0
        self.add(*streams)
        self.play(*[s.fade(1.0, 0.6) for s in streams], run_time=0.6)

        self.at("related to")
        self.play(*[Indicate(row.flaps[i], color=TEXT, scale_factor=1.15) for i in OPEN_IDX], run_time=0.8)

        # the neuron depolarizes and fires
        vp = Panel(3.5, 6.25, -3.3, -0.75, "voltage", GREEN, base=-2.8, depth=0.0, t0=0.3)
        rise = VMobject(stroke_color=GREEN, stroke_width=5).set_points_as_corners(
            [[vp.xm(0.3 + 0.2 * s), -2.8 + 0.8 / (1 + np.exp(-(s - 0.5) * 9)), 0] for s in np.linspace(0, 1, 40)])
        self.at("depolarizes")
        self.play(FadeIn(vp.axes), FadeIn(vp.title), Create(vp.flat), run_time=0.4)
        self.play(Create(rise), run_time=1.0)
        spikes = VGroup()
        x_end = vp.xm(0.5)
        for dx in (0.0, 0.5, 1.0):
            spikes.add(Line([x_end + dx * 0.55, -2.0, 0], [x_end + dx * 0.55, -1.35, 0], color=YELLOW, stroke_width=5))
        self.at("fires")
        self.play(LaggedStart(*[Create(s) for s in spikes], lag_ratio=0.3), run_time=0.9)
        self.outro(FadeOut(VGroup(row.group, *chips, *streams, sens, rec, odo, gp, cyc, a1, a2, vp, rise, spikes)))


# ---------------------------------------------------------------------------------------------
class S06Rule(Film):
    """three cells, one rule: a signal is a change from a baseline, in either direction."""

    def construct(self):
        ys = [2.35, 0.1, -2.15]
        specs = [("rod", "light", "cGMP", -1), ("nose", "smell", "cAMP", +1), ("artery wall", "nitric oxide", "cGMP", +1)]
        GX0, GX1 = -1.3, 4.3
        rows = []
        for y, (cell, stim, name, sgn) in zip(ys, specs):
            lab = T(cell, 28, TEXT).move_to([-6.2, y, 0], aligned_edge=LEFT)
            ch = bchip(stim, YELLOW, 26).move_to([-4.15, y, 0], aligned_edge=LEFT)
            base = DashedLine([GX0, y, 0], [GX1, y, 0], color=GREY, stroke_width=3, dash_length=0.12)
            xs = np.linspace(GX0, GX1, 90)
            pts = [[x, y + sgn * 0.8 / (1 + np.exp(-(x - 1.8) / 0.25)), 0] for x in xs]
            tr = VMobject(stroke_color=TEAL, stroke_width=6).set_points_as_corners(pts)
            nm = T(name, 26, TEAL, weight=BOLD).move_to([GX0, y + 0.55, 0], aligned_edge=LEFT)
            aro = Arrow([GX1 + 0.35, y, 0], [GX1 + 0.35, y + sgn * 0.8, 0], buff=0, color=GREEN if sgn > 0 else RED, stroke_width=8, tip_length=0.25)
            link = arr([ch.get_right()[0] + 0.05, y, 0], [GX0 - 0.1, y, 0], YELLOW)
            rows.append(dict(lab=lab, ch=ch, base=base, tr=tr, nm=nm, aro=aro, link=link))

        # rod
        r = rows[0]
        self.play(FadeIn(r["lab"]), FadeIn(r["ch"], shift=RIGHT * 0.15), GrowArrow(r["link"]), Create(r["base"]), FadeIn(r["nm"]), run_time=0.7)
        self.at("light makes")
        self.play(Create(r["tr"]), run_time=1.1)
        self.play(GrowArrow(r["aro"]), run_time=0.4)

        # nose
        r = rows[1]
        self.at("In the nose")
        self.play(FadeIn(r["lab"]), FadeIn(r["ch"], shift=RIGHT * 0.15), GrowArrow(r["link"]), Create(r["base"]), FadeIn(r["nm"]), run_time=0.8)
        self.at("smell makes")
        self.play(Create(r["tr"]), run_time=1.0)
        self.play(GrowArrow(r["aro"]), run_time=0.4)

        # artery
        r = rows[2]
        self.at("In an artery")
        self.play(FadeIn(r["lab"]), FadeIn(r["ch"], shift=RIGHT * 0.15), GrowArrow(r["link"]), Create(r["base"]), FadeIn(r["nm"]), run_time=0.8)
        self.at("nitric oxide makes")
        self.play(Create(r["tr"]), run_time=1.0)
        self.play(GrowArrow(r["aro"]), run_time=0.4)
        self.at("that same")
        boxes = VGroup(*[SurroundingRectangle(rows[k]["nm"], color=TEAL, buff=0.1, corner_radius=0.1) for k in (0, 2)])
        self.play(Create(boxes), run_time=0.6)
        rel = T("muscle\nrelaxes", 26, GREEN, line_spacing=0.8).move_to([5.6, ys[2] + 0.1, 0])
        self.at("muscle")
        self.play(FadeIn(rel, shift=LEFT * 0.1), run_time=0.6)

        # the rule
        self.at("Keep this rule")
        self.play(FadeOut(boxes), *[rows[k]["base"].animate.set_stroke(TEXT, 4) for k in range(3)], run_time=0.6)
        bl = T("baseline", 24, TEXT).next_to(rows[0]["base"], UP, buff=0.1).align_to(rows[0]["base"], RIGHT)
        self.at("a baseline")
        self.play(FadeIn(bl), *[Indicate(rows[k]["base"], color=TEXT, scale_factor=1.0) for k in range(3)], run_time=0.9)
        self.at("either direction")
        self.play(*[pop(rows[k]["aro"], 1.35) for k in range(3)], run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "A signal is a change from a baseline, in either direction."
