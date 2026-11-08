"""Neuronal polarity, chapter 3: What Makes a Winner  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept; shared with the other chapters of this lesson, from scenes.old.py)
  YELLOW = the axon, and the leading neurite once it has won: used ONLY for the winner / the future axon
  TEXT   = the leading neurite before it wins (white), labels, numbers, the open question
  GREY   = neurites that are not leading, cell body, outlines, axes, the chart baseline
  GREEN  = PIP3 and positive feedback (box 1, the loop's arrows, PI3-kinase, Cdc42 and Rac switches ON), "gain"
  GOLD   = competition and the shared supply only (box 2, reservoir, pipes, icons, cargo)
  RED    = cost / retraction, the brake RhoA, "no winner", the inhibitory signal
  PROPOSED = not a colour: white italic text, and a dashed outline on cards
  ORANGE = actin
  TEAL   = microtubules
  PINK   = the Par3/Par6/aPKC complex (new in this chapter; the series PURPLE stays reserved for ankyrin G)
  (series colours not used here: BLUE dendrites, PURPLE ankyrin G / initial segment)

Every curve and bar height is computed from the lesson's model (see simulate()): five neurites, four at 15 um
and one at 20 um; the supply (20 um an hour) is shared out in proportion to length ** p; every neurite pays a
fixed cost c (2 um an hour) and cannot shrink below a 2 um floor; 48 hours. p = 1, c = 0 gives 1.33 for ever;
p = 1, c = 2 gives about 5; p = 2, c = 0 gives about 15; p = 2, c = 2 gives about 400 and the floor by about
14 hours. Rule 1 (growth in simple proportion to length) uses a growth rate of ln(4)/48 an hour so that
every neurite grows about fourfold in 48 hours; any rate gives the same frozen 1.33.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

class _AudioFinish:
    def finish(self):
        """Finish on narration, without the shared helper's cumulative 0.4 s tails."""
        remaining = self.narration_s - self.elapsed()
        frames = int(np.floor((remaining + 1e-7) * config.frame_rate))
        if frames > 0:
            self.wait(frames / config.frame_rate)


class SpokenScene(_AudioFinish, SpokenScene):
    pass


class NarratedScene(_AudioFinish, NarratedScene):
    pass


class TitleCard(_AudioFinish, TitleCard):
    pass


class EndCard(_AudioFinish, EndCard):
    pass


PINK = "#F28DB2"
ORANGE = "#F29E4C"
SOMA_FILL = "#262b36"

# ---------------------------------------------------------------- the model
HR = np.arange(0, 48 + 1e-9, 0.25)
L0 = np.array([15.0, 15.0, 15.0, 15.0, 20.0])      # four siblings, then the leader (index 4)


def simulate(p, c, S=20.0, floor=2.0, T=48.0, dt=0.01):
    L = L0.copy()
    out = [L.copy()]
    per = int(round(0.25 / dt))
    for k in range(int(round(T / dt))):
        w = L ** p
        L = np.maximum(L + dt * (S * w / w.sum() - c), floor)
        if (k + 1) % per == 0:
            out.append(L.copy())
    return np.array(out)


SIM1 = np.stack([L0 * np.exp(np.log(4.0) / 48.0 * h) for h in HR])     # Rule 1: growth in proportion to length
SIM2 = simulate(1, 0)       # Rule 2: shared supply, split in proportion to length
SIMC = simulate(1, 2)       # supply share ~ length, plus fixed cost
SIMQ = simulate(2, 0)       # supply share ~ length squared
SIMB = simulate(2, 2)       # both
T_FLOOR = float(HR[int(np.argmax(SIMB[:, 0] <= 2.0 + 1e-6))])

# ---------------------------------------------------------------- layout
BASE = -3.0                 # chart baseline
HC = 5.5                    # chart height (axis length)
BW, SP = 1.05, 1.4          # bar width and spacing
AXX = -5.5                  # x of the vertical axis
XS = [-4.4 + SP * i for i in range(5)]     # bar centres; the leader is the last one
LEAD = 4
BX = XS[LEAD] + BW / 2 + 0.3        # x of the gap brackets
RX = 4.7                    # centre of the right-hand panel
STRIP_Y = 3.38
TICKS = {24: [0, 10, 20], 30: [0, 10, 20, 30], 90: [0, 30, 60, 90], 300: [0, 100, 200, 300],
         900: [0, 300, 600, 900], 20: [0, 5, 10, 15, 20], 60: [0, 30, 60]}


def at_left(m, x, y):
    return m.move_to([x + m.width / 2, y, 0])


def live(textfn, posfn, size=26, color=TEXT, left=False):
    """Text that is rebuilt every frame (for counters). m.op is its opacity tracker."""
    op = ValueTracker(1.0)
    m = M(textfn(), size, color)

    def upd(mm):
        n = M(textfn(), size, color)
        p = posfn()
        if left:
            at_left(n, p[0], p[1])
        else:
            n.move_to(p)
        n.set_opacity(op.get_value())
        mm.become(n)

    m.add_updater(upd)
    upd(m)
    m.op = op
    return m


def make_axis(ax_x, base, H, ymax, ticks, fs=26, ylab_x=None, ylabel="length (µm)"):
    g = VGroup(Line([ax_x, base, 0], [ax_x, base + H, 0], color=GREY, stroke_width=3))
    for v in ticks:
        y = base + H * v / ymax
        g.add(Line([ax_x - 0.1, y, 0], [ax_x, y, 0], color=GREY, stroke_width=3))
        lb = T(str(v), fs, TEXT)
        lb.move_to([ax_x - 0.18 - lb.width / 2, y, 0])
        g.add(lb)
    if ylabel and ylab_x is not None:
        g.add(T(ylabel, fs, TEXT).rotate(PI / 2).move_to([ylab_x, base + H / 2, 0]))
    return g


class Race:
    """Bars (four siblings, then the leader) on a fixed, labelled axis; driven by trackers or by a simulation and hour t."""

    def __init__(self, lengths=tuple(L0), ymax=30.0, H=HC, leader_color=TEXT, sim=None, t=0.0, xs=XS, base=BASE,
                 bw=BW, fs=26, lead=LEAD, ax_x=AXX, ylab_x=-6.45, ticks=None, ylabel="length (µm)", axis=True, below=False):
        self.tr = [ValueTracker(v) for v in lengths]
        self.ym = ValueTracker(ymax)
        self.t = ValueTracker(t)
        self.sim, self.H, self.base, self.xs, self.bw, self.fs = sim, H, base, xs, bw, fs
        self.ax_x, self.ylab_x, self.ylabel, self.lead, self.below = ax_x, ylab_x, ylabel, lead, below
        self.n = len(xs)
        self.bars = VGroup()
        for i, x in enumerate(xs):
            col = leader_color if i == lead else GREY
            r = Rectangle(width=bw, height=0.1, stroke_width=0, fill_color=col, fill_opacity=1)
            r.add_updater(lambda m, i=i: self._upd(m, i))
            self._upd(r, i)
            self.bars.add(r)
        self.base_line = Line([ax_x, base, 0], [xs[-1] + bw / 2 + 0.25, base, 0], color=GREY, stroke_width=3)
        self.axg = self.axis_for(ymax, ticks) if axis else VGroup()
        self.group = VGroup(self.base_line, self.bars)
        self.lab = []
        for i in range(self.n):
            lb = live(lambda i=i: f"{self.L(i):.0f}",
                      lambda i=i: np.array([xs[i], (self.base - 0.36) if self.below else (self.top(i) + 0.32), 0.0]), fs, TEXT)
            lb.op.set_value(0.0)
            self.lab.append(lb)
        self.labs = VGroup(*self.lab)

    def axis_for(self, ymax, ticks=None):
        return make_axis(self.ax_x, self.base, self.H, ymax, ticks or TICKS[int(ymax)], self.fs, self.ylab_x, self.ylabel)

    def L(self, i):
        if self.sim is not None:
            return float(np.interp(self.t.get_value(), HR, self.sim[:, i]))
        return self.tr[i].get_value()

    def h(self, i):
        return max(self.L(i) / self.ym.get_value() * self.H, 0.03)

    def top(self, i):
        return self.base + self.h(i)

    def _upd(self, m, i):
        h = self.h(i)
        m.stretch_to_fit_height(h)
        m.move_to([self.xs[i], self.base + h / 2, 0])

    def show(self, idx):
        return [self.lab[i].op.animate.set_value(1.0) for i in idx]

    def recolor(self, i, col):
        return self.bars[i].animate.set_color(col)

    def mobs(self):
        return [self.axg, self.group, self.labs]


def stage(scene, ymax=30.0, sim=None, t=0.0, lengths=tuple(L0), leader=TEXT, nums=True, corner=True, **kw):
    r = Race(lengths=lengths, ymax=ymax, leader_color=leader, sim=sim, t=t, **kw)
    scene.add(*r.mobs())
    if nums:
        for l in r.lab:
            l.op.set_value(1.0)
    if corner:
        scene.add(corner_label())
    return r


def zoom_axis(scene, r, ymax, run_time=1.2, cue="zoomed out", tag_pos=(-2.3, BASE + HC - 0.05)):
    """Visibly rescale the axis: bars shrink against new ticks, with a cue so the change is not silent."""
    new = r.axis_for(ymax)
    old = r.axg
    tag = T(cue, 28, TEXT, slant=ITALIC)
    tag.move_to([tag_pos[0], tag_pos[1], 0])
    tag.set_opacity(0)
    scene.add(tag)
    scene.play(r.ym.animate.set_value(ymax), FadeOut(old), FadeIn(new), tag.animate.set_opacity(1), run_time=run_time)
    r.axg = new
    return tag


def clock(scene, tracker, t0, t1, v0=0.0, v1=48.0):
    """Tracker that follows the scene's own time: v0 until t0, then linear to v1 at t1 (lets cues fire meanwhile)."""
    def f(m, dt):      # a dt argument makes it a time-based updater, so waits keep running it
        x = min(max((scene.elapsed() - t0) / (t1 - t0), 0.0), 1.0)
        m.set_value(v0 + (v1 - v0) * x)
    tracker.add_updater(f)
    scene.add(tracker)


def hold_until(scene, t):
    rest = t - scene.elapsed()
    if rest > 0.02:
        scene.wait(rest)


def corner_label():
    m = T("illustrative model", 26, TEXT, slant=ITALIC)
    return m.move_to([6.75 - m.width / 2, 3.5, 0])


def corner_big():
    return T("a model,\nnot a measurement", 52, TEXT, font=TITLE_FONT, line_spacing=0.95).move_to([0.0, 0.3, 0])


def card(title, body, color=GREY, w=4.0, bsize=26, mono=False, dashed=False):
    t = T(title, 26, color)
    fn = M if mono else T
    b = VGroup(*[fn(s, bsize, TEXT) for s in body]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    inner = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    box = RoundedRectangle(corner_radius=0.14, width=max(w, inner.width + 0.5), height=inner.height + 0.4,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.08)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
    return VGroup(box, inner)


def rule1_card():
    return card("Rule 1", ["growth = k × length"], GREY, w=4.0).move_to([RX, 2.4, 0])


def timer(tr, pos=(RX, 0.8, 0), r=0.5):
    pos = np.array(pos, float)
    ring = Circle(radius=r, stroke_color=GREY, stroke_width=5).move_to(pos)
    arc = Arc(radius=r, start_angle=PI / 2, angle=-TAU * 0.002, stroke_color=GOLD, stroke_width=8)
    arc.move_arc_center_to(pos)

    def f(m):
        fr = min(max(tr.get_value() / 48.0, 0.002), 0.999)
        n = Arc(radius=r, start_angle=PI / 2, angle=-TAU * fr, stroke_color=GOLD, stroke_width=8).move_arc_center_to(pos)
        m.become(n)

    arc.add_updater(f)
    txt = live(lambda: f"hour {tr.get_value():.0f} of 48", lambda: np.array([pos[0], pos[1] - 0.85, 0]), 26, TEXT)
    return VGroup(ring, arc), txt


def bracket(x, yl, yh, xs_from=None, color=TEXT):
    """A bracket at x spanning yl..yh, with a dashed reference line from the lower bar's edge."""
    parts = []
    if xs_from is not None:
        parts.append(DashedLine([xs_from, yl, 0], [x, yl, 0], color=color, stroke_width=2, stroke_opacity=0.7))
    br = VMobject(stroke_color=color, stroke_width=4)
    br.set_points_as_corners([[x - 0.15, yl, 0], [x, yl, 0], [x, yh, 0], [x - 0.15, yh, 0]])
    parts.append(br)
    return VGroup(*parts)


def ratio_card(race, pos=(RX, -1.9, 0), title="leader ÷ next sibling", fmt="{:.2f}", col=TEXT, lead=LEAD, nxt=3):
    t = T(title, 26, TEXT).move_to([pos[0], pos[1] + 0.55, 0])
    num = live(lambda: fmt.format(race.L(lead) / race.L(nxt)), lambda: np.array([pos[0], pos[1] - 0.15, 0]), 44, col)
    return t, num


def question():
    return T("Does one\nneurite win?", 46, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to([RX, -1.45, 0])


def chips_strip():
    c1 = chip("1  positive feedback", GREEN, 24)
    c2 = chip("2  competition", GOLD, 24)
    g = VGroup(c1, c2).arrange(RIGHT, buff=0.3)
    g.move_to([-6.75 + g.width / 2, STRIP_Y, 0])
    return c1, c2


BOX1 = np.array([-3.4, -0.15, 0.0])
BOX2 = np.array([3.4, -0.15, 0.0])


def ing_box(center, color, n):
    box = RoundedRectangle(corner_radius=0.2, width=6.0, height=4.8, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.05).move_to(center)
    num = T(str(n), 40, color).move_to(box.get_corner(UL) + RIGHT * 0.4 + DOWN * 0.4)
    return VGroup(box, num)


# ---------------------------------------------------------------- supply scenes (reservoir, pipes, icons)
RES_C = np.array([-1.7, 1.8, 0.0])
RES_BOT = RES_C[1] - 0.425
SB = -2.85                  # baseline of the small chart in the supply scenes
SH = 3.5                    # its height
PW0 = 0.55                  # neutral pipe width (scene units)


class Supply:
    def __init__(self, race, widths=(PW0,) * 5):
        self.race = race
        self.soma = RoundedRectangle(corner_radius=0.35, width=7.0, height=1.7, stroke_color=GREY, stroke_width=4,
                                     fill_color=SOMA_FILL, fill_opacity=1).move_to(RES_C)
        self.res = RoundedRectangle(corner_radius=0.2, width=6.8, height=0.85, stroke_color=GOLD, stroke_width=3,
                                    fill_color=GOLD, fill_opacity=0.35).move_to(RES_C)
        self.pw = [ValueTracker(w) for w in widths]
        self.pipes = VGroup()
        for i, x in enumerate(race.xs):
            pr = Rectangle(width=0.5, height=1.0, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.28)
            pr.add_updater(lambda m, i=i, x=x: self._pipe(m, i, x))
            self._pipe(pr, i, x)
            self.pipes.add(pr)
        self.fl = ValueTracker(0.0)
        self.iop = ValueTracker(0.0)
        self.icons = VGroup()
        kinds = [lambda: Circle(radius=0.07), lambda: Square(side_length=0.13), lambda: Triangle().scale(0.09).rotate(PI)]
        for i, x in enumerate(race.xs):
            for k in range(3):
                ic = kinds[k]().set_fill(GOLD, 1).set_stroke(GOLD, 1)
                ic.add_updater(lambda m, i=i, x=x, k=k: (m.move_to([x, RES_BOT - 0.1 + (race.top(i) + 0.1 - RES_BOT) *
                                                                     ((self.fl.get_value() + k / 3.0) % 1.0), 0]),
                                                          m.set_opacity(self.iop.get_value())))
                self.icons.add(ic)

    def _pipe(self, m, i, x):
        top = self.race.top(i) + 0.05
        h = max(RES_BOT - top, 0.05)
        m.stretch_to_fit_width(max(self.pw[i].get_value(), 0.05))
        m.stretch_to_fit_height(h)
        m.move_to([x, (RES_BOT + top) / 2, 0])

    def widths(self, ws):
        return [self.pw[i].animate.set_value(w) for i, w in enumerate(ws)]


def legend_rows():
    rows = VGroup()
    for name, mk in (("membrane", lambda: Circle(radius=0.12)), ("tubulin", lambda: Square(side_length=0.22)),
                     ("signalling proteins", lambda: Triangle().scale(0.15).rotate(PI))):
        ic = mk().set_fill(GOLD, 1).set_stroke(GOLD, 1)
        tx = T(name, 26, TEXT)
        rows.add(VGroup(ic, tx).arrange(RIGHT, buff=0.25))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    rows.move_to([RX + 0.1, 0.35, 0])
    return rows


def tabs(active=None):
    a = chip("way 1", TEXT if active == 1 else GREY, 26)
    b = chip("way 2", TEXT if active == 2 else GREY, 26)
    VGroup(a, b).arrange(RIGHT, buff=0.3).move_to([RX, -3.2, 0])
    return a, b


FRAME2 = dict(width=13.5, height=6.45)


def frame2():
    return RoundedRectangle(corner_radius=0.25, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.04,
                            **FRAME2).move_to([0, -0.5, 0])


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "One Axon, Many Dendrites: Neuronal Polarity"
    TITLE = "What Makes a Winner"


class S01(SpokenScene):
    def construct(self):
        r = Race(lengths=(0, 0, 0, 0, 0), ymax=30, leader_color=GREY)
        hd = T("What Makes a Winner", 44, font=TITLE_FONT).move_to([-1.0, 3.3, 0])
        self.add(r.axg, r.group)
        self.at("a longer")
        self.play(FadeIn(hd), *[tr.animate.set_value(v) for tr, v in zip(r.tr, L0)], run_time=1.2)
        self.at("grows faster")
        top = r.top(LEAD)
        arr = Arrow([XS[LEAD], top + 0.25, 0], [XS[LEAD], top + 1.3, 0], color=TEXT, buff=0, stroke_width=7)
        lab = T("grows faster", 28, TEXT).move_to([XS[LEAD] + 1.75, top + 0.9, 0])
        self.play(r.recolor(LEAD, TEXT), GrowArrow(arr), FadeIn(lab), run_time=0.7)
        self.at("is that enough")
        q = T("?", 170, TEXT, font=TITLE_FONT).move_to([RX, 0.9, 0])
        self.play(FadeOut(arr), FadeOut(lab), FadeIn(q, scale=0.6), run_time=0.7)
        self.at("one winner")
        w = T("one winner?", 50, TEXT, font=TITLE_FONT).move_to([RX, -1.3, 0])
        self.play(FadeIn(w, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        r = stage(self, 30, leader=TEXT, nums=False, corner=False)
        hd = T("What Makes a Winner", 44, font=TITLE_FONT).move_to([-1.0, 3.3, 0])
        q = T("?", 170, TEXT, font=TITLE_FONT).move_to([RX, 0.9, 0])
        w = T("one winner?", 50, TEXT, font=TITLE_FONT).move_to([RX, -1.3, 0])
        self.add(hd, q, w)
        self.at("a model")
        big = corner_big()
        self.play(FadeOut(q), FadeOut(w), FadeOut(hd), FadeIn(big, scale=0.9), *[m.animate.set_opacity(0.0) for m in (r.axg, r.group)], run_time=0.5)
        hold_until(self, 2.0)
        small = corner_label()
        self.play(ReplacementTransform(big, small), *[m.animate.set_opacity(1.0) for m in (r.axg, r.group)], run_time=0.7)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        r = stage(self, 30, leader=GREY, nums=False)
        self.at("five neurites")
        topy = r.top(LEAD) + 0.85
        bx0, bx1 = XS[0] - 0.6, XS[-1] + 0.6
        brk = VMobject(stroke_color=TEXT, stroke_width=4)
        brk.set_points_as_corners([[bx0, topy - 0.15, 0], [bx0, topy, 0], [bx1, topy, 0], [bx1, topy - 0.15, 0]])
        five = T("five neurites", 30, TEXT).move_to([(bx0 + bx1) / 2, topy + 0.4, 0])
        self.play(Create(brk), FadeIn(five), run_time=0.8)
        self.at("four are")
        self.play(FadeOut(brk), FadeOut(five), *r.show([0, 1, 2, 3]), run_time=0.8)
        self.at("one is 20")
        self.play(r.recolor(LEAD, TEXT), *r.show([LEAD]), run_time=0.6)
        self.at("five micrometers")
        x = BX
        br = bracket(x, r.top(3), r.top(LEAD), XS[LEAD] + BW / 2 - 0.0)
        t5 = at_left(T("5 µm ahead", 30, TEXT), x + 0.25, (r.top(3) + r.top(LEAD)) / 2)
        self.play(Create(br), run_time=0.5)
        self.play(FadeIn(t5), run_time=0.4)
        self.finish()


def growth_arrows(r, idx=range(5)):
    g = VGroup()
    for i in idx:
        top = r.top(i) + 0.7
        ln = 0.75 * r.L(i) / r.L(0)
        g.add(Arrow([XS[i], top, 0], [XS[i], top + ln, 0], color=TEXT, buff=0, stroke_width=6,
                    max_tip_length_to_length_ratio=0.4))
    return g


class S04(SpokenScene):
    def construct(self):
        r = stage(self, 30)
        self.at("grows")
        ar = growth_arrows(r)
        self.play(*[GrowArrow(a) for a in ar], run_time=0.45)
        self.at("in proportion")
        rc = rule1_card()
        self.play(FadeIn(rc, shift=LEFT * 0.2), run_time=0.5)
        self.at("own length")
        self.play(Indicate(r.bars, color=TEXT, scale_factor=1.0), run_time=0.8)
        self.at("longer one")
        tag = T("longer: faster", 28, TEXT).move_to([XS[LEAD] + 0.1, r.top(LEAD) + 2.0, 0])
        self.play(Indicate(ar[LEAD], color=YELLOW, scale_factor=1.3), FadeIn(tag), run_time=0.9)
        self.finish()


def clock_group(scene, tr, pos=(RX, 0.8, 0)):
    ring, txt = timer(tr, pos)
    scene.add(ring, txt)
    return ring, txt


class S05(SpokenScene):
    def construct(self):
        r = stage(self, 30, sim=SIM1, t=0.0)
        rc = rule1_card()
        self.add(rc)
        tr = ValueTracker(0.0)
        ring, txt = timer(tr)
        self.at("run the rule")
        self.play(Create(ring[0]), FadeIn(txt), run_time=0.6)
        self.add(ring[1])
        self.at("for two days")
        tag = zoom_axis(self, r, 90, run_time=1.0, cue="zoomed out: 0–90 µm")
        self.at("does")
        qq = question()
        self.play(FadeOut(tag), FadeIn(qq, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        r = stage(self, 90, sim=SIM1, t=0.0)
        self.add(rule1_card())
        tr = ValueTracker(0.0)
        ring, txt = timer(tr)
        self.add(ring, txt, question())
        self.finish()


class S07(SpokenScene):
    def construct(self):
        r = stage(self, 90, sim=SIM1, t=0.0)
        self.add(rule1_card())
        tr = ValueTracker(0.0)
        ring, txt = timer(tr)
        qq = question()
        self.add(ring, txt, qq)
        tr.add_updater(lambda m: m.set_value(r.t.get_value()))
        self.add(tr)
        # The first spoken word is transcribed as "Now"; answer at its onset.
        no = T("No.", 84, RED, font=TITLE_FONT).move_to([RX, -0.9, 0])
        self.remove(qq)
        self.add(no)
        self.play(r.t.animate.set_value(48.0), run_time=2.9, rate_func=rate_functions.linear)
        self.at("the leader")
        t_, num = ratio_card(r, pos=(RX, -2.45, 0))
        self.play(FadeIn(t_), FadeIn(num), run_time=0.5)
        self.at("same fraction")
        self.play(Indicate(num, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("a third longer")
        x = BX
        br = bracket(x, r.top(3), r.top(LEAD), XS[LEAD] + BW / 2)
        tl = at_left(T("a third\nlonger", 28, TEXT, line_spacing=0.9), x + 0.25, (r.top(3) + r.top(LEAD)) / 2)
        self.play(Create(br), FadeIn(tl), run_time=0.7)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        r = stage(self, 90, sim=SIM1, t=48.0)
        self.add(rule1_card())
        t_, num = ratio_card(r, pos=(RX, -0.15, 0))
        self.add(t_, num)
        x = BX
        self.at("the gap")
        br = bracket(x, r.top(3), r.top(LEAD), XS[LEAD] + BW / 2)
        gl = live(lambda: f"gap {r.L(LEAD) - r.L(3):.0f} µm", lambda: np.array([x + 0.25, (r.top(3) + r.top(LEAD)) / 2, 0]),
                  28, TEXT, left=True)
        self.play(Create(br), FadeIn(gl), run_time=0.6)
        self.at("widens")
        # the gap, then and now, drawn to one scale
        u = 0.14
        g0 = Rectangle(width=5 * u, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=1)
        g1 = Rectangle(width=20 * u, height=0.34, stroke_width=0, fill_color=TEXT, fill_opacity=1)
        x0 = 2.9
        g0.move_to([x0 + g0.width / 2, -1.75, 0])
        g1.move_to([x0 + g1.width / 2, -2.85, 0])
        l0 = at_left(T("gap at the start: 5 µm", 26, TEXT), x0, -1.3)
        l1 = at_left(T("gap at hour 48: 20 µm", 26, TEXT), x0, -2.4)
        self.play(FadeIn(l0), GrowFromEdge(g0, LEFT), run_time=0.5)
        self.play(FadeIn(l1), GrowFromEdge(g1, LEFT), run_time=0.8)
        self.at("nothing holds")
        ar = growth_arrows(r, range(4))
        kg = T("the other four\nstill grow", 28, TEXT, line_spacing=0.9).move_to([-2.9, r.top(0) + 2.1, 0])
        self.play(*[GrowArrow(a) for a in ar], FadeIn(kg), run_time=0.7)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        r = stage(self, 90, sim=SIM1, t=48.0)
        self.add(rule1_card())
        self.at("five long")
        topy = r.top(LEAD) + 0.75
        bx0, bx1 = XS[0] - 0.6, XS[-1] + 0.6
        brk = VMobject(stroke_color=TEXT, stroke_width=4)
        brk.set_points_as_corners([[bx0, topy - 0.15, 0], [bx0, topy, 0], [bx1, topy, 0], [bx1, topy - 0.15, 0]])
        five = T("five long neurites", 30, TEXT).move_to([(bx0 + bx1) / 2, topy + 0.4, 0])
        self.play(Create(brk), FadeIn(five), run_time=0.8)
        self.at("no single")
        nw = T("no single\nwinner", 50, RED, font=TITLE_FONT, line_spacing=0.9).move_to([RX, -0.9, 0])
        self.play(FadeIn(nw, scale=0.8), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- s10 to s16: the two ingredients
class S10(SpokenScene):
    def construct(self):
        r = stage(self, 90, sim=SIM1, t=48.0)
        rc = rule1_card()
        nw = T("no single\nwinner", 50, RED, font=TITLE_FONT, line_spacing=0.9).move_to([RX, -0.9, 0])
        self.add(rc, nw)
        self.at("growing faster")
        self.play(FadeOut(rc), FadeOut(nw), run_time=0.5)
        l1 = T("grows faster\nthe more it grows", 32, TEXT, line_spacing=0.9).move_to([RX, 2.1, 0])
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.6)
        self.at("is true")
        tr_ = chip("true", GREEN, 34).move_to([RX, 0.85, 0])
        self.play(FadeIn(tr_, scale=0.8), run_time=0.5)
        self.at("but growth")
        l2 = T("growth in simple\nproportion to length", 32, TEXT, line_spacing=0.9).move_to([RX, -0.55, 0])
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.7)
        self.at("picks no winner")
        l3 = T("picks no winner", 42, RED, font=TITLE_FONT).move_to([RX, -2.1, 0])
        self.play(FadeIn(l3, scale=0.8), run_time=0.6)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        r = stage(self, 30)
        self.at("gain must")
        top = r.top(LEAD)
        ga = Arrow([XS[LEAD], top + 0.75, 0], [XS[LEAD], top + 1.6, 0], color=GREEN, buff=0, stroke_width=9)
        gt = at_left(T("gain", 34, GREEN), XS[LEAD] + 0.45, top + 1.3)
        self.play(GrowArrow(ga), FadeIn(gt), run_time=0.7)
        self.at("the other's cost")
        cas = VGroup(*[Arrow([XS[i], r.top(i) + 1.4, 0], [XS[i], r.top(i) + 0.62, 0], color=RED, buff=0, stroke_width=9)
                       for i in range(4)])
        ct = T("cost", 34, RED).move_to([(XS[0] + XS[3]) / 2, r.top(0) + 1.8, 0])
        self.play(*[GrowArrow(a) for a in cas], FadeIn(ct), run_time=0.8)
        self.at("two ingredients")
        b1, b2 = ing_box(BOX1, GREEN, 1), ing_box(BOX2, GOLD, 2)
        self.play(*[FadeOut(m) for m in (r.axg, r.group, r.labs, ga, gt, cas, ct)], run_time=0.5)
        self.play(FadeIn(b1, shift=RIGHT * 0.2), FadeIn(b2, shift=LEFT * 0.2), run_time=0.8)
        self.finish()


def box1_parts():
    title = T("positive feedback", 32, GREEN).move_to([-3.4, 1.7, 0])
    tube = RoundedRectangle(corner_radius=0.5, width=5.4, height=2.5, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.12).move_to([-3.4, -0.5, 0])
    one = T("one neurite", 26, TEXT).move_to([-3.4, -2.05, 0])
    c1 = chip("growth", GREEN, 28).move_to([-5.2, -0.5, 0])
    c2 = chip("what drives\ngrowth", GREEN, 28).move_to([-2.2, -0.5, 0])
    a1 = CurvedArrow(c1.get_top(), c2.get_top(), angle=-PI / 2.2, color=GREEN, stroke_width=5)
    a2 = CurvedArrow(c2.get_bottom(), c1.get_bottom(), angle=-PI / 2.2, color=GREEN, stroke_width=5)
    return title, tube, one, c1, c2, a1, a2


class S12(SpokenScene):
    def construct(self):
        b1, b2 = ing_box(BOX1, GREEN, 1), ing_box(BOX2, GOLD, 2)
        self.add(b1, b2, corner_label())
        title, tube, one, c1, c2, a1, a2 = box1_parts()
        self.at("first")
        self.play(FadeIn(title, shift=DOWN * 0.1), b1[0].animate.set_fill(GREEN, 0.1),
                  b2[0].animate.set_stroke(opacity=0.35), b2[1].animate.set_opacity(0.35), run_time=0.7)
        self.at("within a")
        self.play(FadeIn(tube), FadeIn(one), run_time=0.8)
        self.at("growth recruits")
        self.play(FadeIn(c1, scale=0.8), run_time=0.5)
        self.play(Create(a1), run_time=0.6)
        self.at("whatever drives")
        self.play(FadeIn(c2, scale=0.8), run_time=0.5)
        self.play(Create(a2), run_time=0.6)
        self.play(Indicate(VGroup(a1, a2), color=GREEN, scale_factor=1.05), run_time=0.7)
        self.finish()


def full_box1(scene, dim_box2=True):
    b1, b2 = ing_box(BOX1, GREEN, 1), ing_box(BOX2, GOLD, 2)
    b1[0].set_fill(GREEN, 0.1)
    parts = box1_parts()
    g1 = VGroup(b1, *parts)
    if dim_box2:
        b2[0].set_stroke(opacity=0.35)
        b2[1].set_opacity(0.35)
    scene.add(g1, b2)
    return g1, b2


def pchip(text, color, size=26):
    """A 'proposed' card: dashed outline, white italic text."""
    lab = T(text, size, color, slant=ITALIC)
    box = RoundedRectangle(corner_radius=0.14, width=lab.width + 0.44, height=lab.height + 0.44, stroke_width=0)
    d = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height, stroke_color=color,
                                        stroke_width=2.5, fill_opacity=0), num_dashes=36)
    return VGroup(box, d, lab.move_to(box))


def sup_race(**kw):
    return Race(leader_color=TEXT, ymax=24.0, H=SH, base=SB, below=True, ylab_x=-6.65, **kw)


def supply_state(scene, widths, flow=True, sim=None, t=0.0, tag=True, legend=True, frame=True):
    r = sup_race(sim=sim, t=t)
    su = Supply(r, widths)
    fr = frame2() if frame else None
    cb = T("cell body", 26, TEXT)
    at_left(cb, RES_C[0] + 3.4 + 0.2, RES_C[1])
    c1, c2 = chips_strip()
    if fr is not None:
        scene.add(fr)
    scene.add(su.soma, su.res, su.pipes, su.icons, r.axg, r.group, r.labs, cb, c1, c2, corner_label())
    for l in r.lab:
        l.op.set_value(1.0)
    su.iop.set_value(1.0 if flow else 0.0)
    scene.add(su.fl, su.iop, *su.pw)
    if flow:
        su.fl.add_updater(lambda m, dt: m.increment_value(dt * 0.45))
    lim = T("limited supply", 26, TEXT).move_to(RES_C)
    scene.add(lim)
    lg = legend_rows() if legend else None
    if lg is not None:
        scene.add(lg)
    pt = pchip("one proposal", TEXT, 28).move_to([RX + 0.5, 2.1, 0]) if tag else None
    if pt is not None:
        scene.add(pt)
    return r, su, pt, lg


class S13(SpokenScene):
    def construct(self):
        g1, b2 = full_box1(self)
        c1, c2 = chips_strip()
        self.add(corner_label())
        self.at("second")
        fr = frame2()
        self.play(g1.animate.scale(0.1).move_to(c1.get_center()).set_opacity(0), FadeIn(c1),
                  ReplacementTransform(b2, fr), FadeIn(c2), run_time=0.9)
        self.at("competition")
        ct = T("competition", 64, GOLD, font=TITLE_FONT).move_to([0, 0.2, 0])
        self.play(FadeIn(ct, scale=0.85), run_time=0.6)
        self.at("neurites")
        r = sup_race(lengths=(0, 0, 0, 0, 0))
        self.add(r.axg, r.group, r.labs)
        self.play(FadeOut(ct), *[tr.animate.set_value(v) for tr, v in zip(r.tr, L0)], run_time=1.0)
        self.play(*r.show(range(5)), run_time=0.4)
        self.at("one proposal")
        su = Supply(r)
        pt = pchip("one proposal", TEXT, 28).move_to([RX + 0.5, 2.1, 0])
        self.add(su.icons, su.fl, su.iop, *su.pw)
        self.play(FadeIn(su.soma), FadeIn(su.res), FadeIn(pt, shift=LEFT * 0.2), run_time=0.8)
        self.at("draw on")
        self.play(FadeIn(su.pipes), run_time=0.7)
        self.at("limited supply")
        su.fl.add_updater(lambda m, dt: m.increment_value(dt * 0.45))
        lim = T("limited supply", 26, TEXT).move_to(RES_C)
        lg = legend_rows()
        su.iop.set_value(1.0)
        self.play(FadeIn(lim), FadeIn(lg), run_time=0.6)
        self.at("cell body")
        cb = T("cell body", 26, TEXT)
        at_left(cb, RES_C[0] + 3.4 + 0.2, RES_C[1])
        self.play(FadeIn(cb), run_time=0.5)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        r, su, pt, lg = supply_state(self, (PW0,) * 5)
        self.at("gain is")
        gl = T("wider pipe: gain", 28, GREEN).move_to([RX, -1.4, 0])
        self.play(su.pw[LEAD].animate.set_value(0.95), *[su.pw[i].animate.set_value(0.3) for i in range(4)],
                  FadeIn(gl), run_time=1.0)
        self.at("the other's loss")
        ll = T("narrow pipes: loss", 28, RED).move_to([RX, -2.1, 0])
        self.play(FadeIn(ll, shift=UP * 0.1), run_time=0.6)
        self.finish()


def share_widths(p=1.0, L=L0, k=2.75):
    w = np.array(L) ** p
    return list(k * w / w.sum())


def rule2_card():
    return card("Rule 2", ["supply split in", "proportion to length"], GOLD, w=4.0).move_to([RX, -1.75, 0])


class S15(SpokenScene):
    def construct(self):
        gw = T("wider pipe: gain", 28, GREEN).move_to([RX, -1.4, 0])
        r, su, pt, lg = supply_state(self, (0.3, 0.3, 0.3, 0.3, 0.95))
        self.add(gw, T("narrow pipes: loss", 28, RED).move_to([RX, -2.1, 0]))
        old = VGroup(*[m for m in self.mobjects[-2:]])
        self.at("but even")
        self.play(*su.widths(share_widths()), FadeOut(pt), FadeOut(old), run_time=0.7)
        self.at("a shared supply")
        rc = rule2_card()
        self.play(FadeIn(rc, shift=LEFT * 0.2), run_time=0.7)
        self.at("not quite")
        self.play(Indicate(rc, color=GOLD, scale_factor=1.05), run_time=0.7)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        r, su, pt, lg = supply_state(self, tuple(share_widths()), tag=False)
        rc = rule2_card()
        self.add(rc)
        tr = ValueTracker(0.0)
        hr = live(lambda: f"hour {r.t.get_value():.0f}", lambda: np.array([RX, -3.15, 0]), 26, TEXT)
        self.add(hr)
        r.sim = SIM2
        r.t.set_value(0.0)
        self.at("takes a share")
        tag = zoom_axis(self, r, 300, run_time=0.7, cue="zoomed out: 0–300 µm", tag_pos=(RX, 2.3))
        self.at("in proportion")
        self.play(FadeOut(lg), FadeOut(tag), r.t.animate.set_value(48.0), run_time=1.5, rate_func=rate_functions.linear)
        self.at("the fractions")
        t_, num = ratio_card(r, pos=(RX, 1.7, 0))
        self.play(FadeIn(t_), FadeIn(num), run_time=0.5)
        self.at("stay fixed")
        un = T("unchanged", 30, TEXT).move_to([RX, 0.35, 0])
        self.play(FadeIn(un, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- s17 to s22: what a lead needs
def gauge(x0, y, w, col, h=0.34):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=col, fill_opacity=1).move_to([x0 + w / 2, y, 0])


class S17(SpokenScene):
    def construct(self):
        r = stage(self, 30)
        c1, c2 = chips_strip()
        self.add(c1, c2)
        X0 = 2.5
        self.at("a long")
        hd = at_left(T("growth per unit length", 26, TEXT), X0, 2.3)
        la = at_left(T("long neurite", 26, TEXT), X0, 1.6)
        ga = gauge(X0, 1.15, 2.4, TEXT)
        self.play(FadeIn(hd), FadeIn(la), GrowFromEdge(ga, LEFT), run_time=0.7)
        self.at("relative to")
        lb = at_left(T("short neurite", 26, TEXT), X0, 0.35)
        gb = gauge(X0, -0.1, 2.4, GREY)
        eq = at_left(T("rules 1 and 2: equal", 26, TEXT), X0, -0.8)
        self.play(FadeIn(lb), GrowFromEdge(gb, LEFT), FadeIn(eq), run_time=0.8)
        self.at("larger than")
        mf = at_left(T("must favour the leader", 28, TEXT), X0, -1.65)
        self.play(ga.animate.stretch_to_fit_width(3.9, about_edge=LEFT), FadeOut(eq), FadeIn(mf, shift=UP * 0.1),
                  run_time=0.8)
        self.at("a short")
        self.play(Indicate(gb, color=TEXT, scale_factor=1.05), run_time=0.7)
        self.at("two ways")
        a, b = tabs()
        self.play(FadeIn(a, shift=UP * 0.1), FadeIn(b, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        r = stage(self, 30)
        c1, c2 = chips_strip()
        a, b = tabs(1)
        self.add(c1, c2, a, b)
        self.at("the feedback")
        rc = card("Rule 3", ["supply share in", "proportion to", "length squared"], GREEN, w=4.0).move_to([RX, 1.5, 0])
        hr = live(lambda: f"hour {r.t.get_value():.0f}", lambda: np.array([RX, -0.7, 0]), 26, TEXT)
        r.sim = SIMQ
        r.t.set_value(0.0)
        self.add(hr)
        tag = zoom_axis(self, r, 900, run_time=0.9, cue="zoomed out: 0–900 µm", tag_pos=(-2.3, 2.45))
        self.play(FadeIn(rc, shift=LEFT * 0.2), a.animate.set_stroke(TEXT), run_time=0.4)
        self.at("steeper")
        self.play(FadeOut(tag), r.t.animate.set_value(48.0), run_time=1.8, rate_func=rate_functions.linear)
        self.finish()


def leaks(r):
    g = VGroup()
    for x in XS:
        g.add(Arrow([x, BASE - 0.08, 0], [x, BASE - 0.6, 0], color=RED, buff=0, stroke_width=8,
                    max_tip_length_to_length_ratio=0.45))
    return g


class S19(SpokenScene):
    def construct(self):
        r = stage(self, 30)
        c1, c2 = chips_strip()
        a, b = tabs(2)
        self.add(c1, c2, a, b)
        self.at("every")
        rc = card("Way 2", ["every neurite pays", "the same fixed", "running cost"], RED, w=4.0).move_to([RX, 1.5, 0])
        self.play(FadeIn(rc, shift=LEFT * 0.2), b.animate.set_stroke(TEXT), run_time=0.6)
        self.at("same fixed")
        lk = leaks(r)
        self.play(*[GrowArrow(x) for x in lk], run_time=0.8)
        self.at("such as")
        rt = T("such as retraction", 30, RED).move_to([RX, -0.3, 0])
        self.play(FadeIn(rt, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        r = stage(self, 30)
        c1, c2 = chips_strip()
        a, b = tabs(2)
        lk = leaks(r)
        self.add(c1, c2, a, b, lk)
        X0 = 2.5
        self.at("that cost")
        hd = at_left(T("growth per hour", 28, TEXT), X0, 2.45)
        self.play(Indicate(lk, color=RED, scale_factor=1.15), FadeIn(hd), run_time=0.8)
        self.at("takes a")
        la = at_left(T("leader", 26, TEXT), X0, 1.85)
        lb = at_left(T("short neurite", 26, TEXT), X0, 0.25)
        gA = gauge(X0, 1.4, 3.0, TEXT)
        gB = gauge(X0, -0.2, 2.25, GREY)
        self.play(FadeIn(la), FadeIn(lb), GrowFromEdge(gA, LEFT), GrowFromEdge(gB, LEFT), run_time=0.5)
        self.at("bigger bite")
        rA = gauge(X0 + 3.0 - 1.2, 1.4, 1.2, RED)
        rB = gauge(X0 + 2.25 - 1.2, -0.2, 1.2, RED)
        cost = at_left(T("cost", 26, RED), X0 + 3.0 + 0.2, 1.4)
        self.play(GrowFromEdge(rA, RIGHT), GrowFromEdge(rB, RIGHT), FadeIn(cost), run_time=0.6)
        self.at("a short")
        sA = at_left(T("small share", 26, TEXT), X0, 0.9)
        sB = at_left(T("big share", 26, RED), X0, -0.8)
        self.play(FadeIn(sA), FadeIn(sB), run_time=0.6)
        self.play(Indicate(sB, color=RED, scale_factor=1.15), run_time=0.6)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        kw = dict(ymax=900, H=4.6, base=-2.9, bw=0.7, fs=26, leader_color=TEXT)
        xsL = [-4.6 + 0.95 * i for i in range(5)]
        xsR = [2.2 + 0.95 * i for i in range(5)]
        rL = Race(sim=SIMQ, xs=xsL, ax_x=-5.4, ylab_x=-6.62, **kw)
        rR = Race(sim=SIMC, xs=xsR, ax_x=1.4, ylab_x=None, **kw)
        ikw = dict(ymax=90, H=2.4, base=-1.0, bw=0.4, fs=26, ticks=[0, 30, 60, 90], ylab_x=None)
        xi = [-3.95, -3.3, -2.65, -2.0]
        iL = Race(sim=SIMQ[:, :4], xs=xi, ax_x=-4.5, **ikw)
        iR = Race(sim=SIMC[:, :4], xs=[x + 7.0 for x in xi], ax_x=2.5, **ikw)
        cxs = (-3.4, 3.6)
        frames = VGroup(*[RoundedRectangle(corner_radius=0.15, width=3.5, height=3.75, stroke_color=GREY, stroke_width=2,
                                           fill_color=BG, fill_opacity=1).move_to([cx, 0.37, 0]) for cx in cxs])
        for fr_ in frames:
            fr_.set_z_index(-1)
        zl = [T("four others, zoomed", 26, TEXT).move_to([cx, 1.95, 0]) for cx in cxs]
        self.add(frames, *[m for r_ in (rL, rR, iL, iR) for m in r_.mobs()], *zl, corner_label())
        for r_ in (rL, rR, iL, iR):
            for lb in r_.lab:
                lb.op.set_value(1.0)
        same = T("both charts: same scale", 28, TEXT).move_to([0, -3.45, 0])
        self.add(same)
        hL = T("way 1: steeper feedback", 28, TEXT).move_to([-3.0, 3.1, 0])
        hR = T("way 2: fixed cost", 28, TEXT).move_to([2.9, 3.1, 0])
        nL = T("leader ÷ next: about 15", 34, TEXT).move_to([-3.0, 2.55, 0])
        nR = T("leader ÷ next: about 5", 34, TEXT).move_to([3.2, 2.55, 0])
        for m in (hL, hR, nL, nR):
            m.set_opacity(0)
        self.add(hL, hR, nL, nR)
        for r_ in (rL, rR, iL, iR):
            clock(self, r_.t, 0.5, 6.9)
        self.at("with either")
        self.play(*[m.animate.set_opacity(1) for m in (hL, hR, nL, nR)], run_time=0.5)
        self.at("others grow")
        gl = [T("about 4×", 26, TEXT).move_to([cx, -1.28, 0]) for cx in cxs]
        self.play(*[FadeIn(g, shift=UP * 0.1) for g in gl], run_time=0.5)
        self.at("then slow")
        gl2 = [T("then a crawl", 26, TEXT).move_to([cx, -1.28, 0]) for cx in cxs]
        self.play(*[ReplacementTransform(a_, b_) for a_, b_ in zip(gl, gl2)], run_time=0.5)
        hold_until(self, 6.9)
        for r_ in (rL, rR, iL, iR):
            r_.t.clear_updaters()
            r_.t.set_value(48.0)
        self.play(Indicate(nL, color=TEXT, scale_factor=1.1), Indicate(nR, color=TEXT, scale_factor=1.1), run_time=0.5)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        x4 = [-4.8, -3.8, -2.8, -1.8]
        r4 = Race(lengths=(15,) * 4, sim=SIMB[:, :4], ymax=20, H=5.0, base=-3.0, xs=x4, bw=0.75, ax_x=-5.6,
                  ylab_x=-6.45, fs=26)
        rl = Race(lengths=(20,), sim=SIMB[:, 4:5], ymax=900, H=5.4, base=-3.0, xs=[5.8], bw=0.9, ax_x=4.5, ylab_x=3.35,
                  fs=26, lead=0, leader_color=TEXT)
        fy = -3.0 + 5.0 * 2 / 20
        fl = DashedLine([-5.6, fy, 0], [-1.2, fy, 0], color=TEXT, stroke_width=3)
        fln = T("dashed line: the 2 µm floor", 24, TEXT).move_to([-3.2, -3.45, 0])
        MX = 1.2
        ct = T("length squared + fixed cost", 28, TEXT).move_to([MX, 3.05, 0])
        tr = ValueTracker(0.0)
        ring, hrt = timer(tr, (MX, 2.2, 0))
        spec = VGroup(*[T(x, 24, TEXT) for x in ("supply: 20 µm an hour", "cost: 2 µm an hour each", "floor: 2 µm",
                                                  "run: 48 hours")])
        spec.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        spec.move_to([MX, -2.95, 0])
        self.add(*r4.mobs(), *rl.mobs(), fln, corner_label())
        for lb in list(r4.lab) + list(rl.lab):
            lb.op.set_value(1.0)
        self.add(ct, ring, hrt, spec)
        warp = lambda x: float(np.interp(x, [0, 0.5, 1], [0, T_FLOOR, 48]))
        t0, t1 = 0.1, 4.2

        def f(m, dt):
            x = min(max((self.elapsed() - t0) / (t1 - t0), 0.0), 1.0)
            m.set_value(warp(x))

        r4.t.add_updater(f)
        rl.t.add_updater(f)
        tr.add_updater(lambda m: m.set_value(r4.t.get_value()))
        self.add(r4.t, rl.t, tr)
        hold_until(self, 1.0)
        self.at("stubs")
        nt = T("floor reached\nby hour 14", 26, TEXT, line_spacing=0.9).move_to([MX, 0.45, 0])
        self.play(FadeIn(fl), FadeIn(nt, shift=UP * 0.1), run_time=0.2)
        floor_time = t0 + (t1 - t0) * 0.5
        hold_until(self, floor_time)
        self.play(rl.bars[0].animate.set_color(YELLOW), run_time=0.2)
        self.at("now there")
        wn = T("winner", 32, YELLOW).move_to([5.8, 2.95, 0])
        self.play(FadeIn(wn, shift=DOWN * 0.1), run_time=0.3)
        hold_until(self, t1)
        for r_ in (r4, rl):
            r_.t.clear_updaters()
            r_.t.set_value(48.0)
        tr.clear_updaters()
        tr.set_value(48.0)
        a400 = T("about 400", 42, YELLOW).move_to([MX, -0.65, 0])
        a820 = T("820 µm vs\nthe 2 µm floor", 26, TEXT, line_spacing=0.9).move_to([MX, -1.5, 0])
        self.play(FadeIn(a400), FadeIn(a820), run_time=0.4)
        self.finish()


# ================================================================ the loop at one growth cone (s23 to s32)
CY, CXF, FA, FB = -0.1, -2.9, 2.4, 2.3     # growth-cone fan: centre and half-axes (the tip is its right-hand edge)
SLOT_X, SLOT_W, SLOT_H = 3.95, 5.2, 1.0
SLOT_Y = [2.5 - 1.25 * i for i in range(5)]
SLOT_COL = [GREEN, PINK, GREEN, TEAL, GOLD]
SLOT_TXT = [["PI3-kinase makes PIP3"], ["Par3 / Par6 / aPKC", "gathers at the tip"], ["Cdc42 and Rac", "switch on"],
            ["looser actin, microtubules", "push in  (proposed)"], ["more material, more transport", "(thought to be physical)"]]
LOOP_X = 6.78
MT_END0 = (-1.5, -1.2, -0.9)


def ell(th, dx=0.0, sc=1.0):
    return np.array([CXF + dx + FA * sc * np.cos(th), CY + FB * sc * np.sin(th), 0.0])


def make_cone():
    fan = Ellipse(width=2 * FA, height=2 * FB, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW,
                  fill_opacity=0.07).move_to([CXF, CY, 0])
    sx = -5.25
    shaft = VGroup(Line([-6.75, CY + 0.45, 0], [sx, CY + 0.45, 0], color=YELLOW, stroke_width=5),
                   Line([-6.75, CY - 0.45, 0], [sx, CY - 0.45, 0], color=YELLOW, stroke_width=5))
    lab = T("growth cone", 28, YELLOW).move_to([CXF, CY + FB + 0.42, 0])
    return VGroup(shaft, fan, lab)


def patch(w=13, op=1.0):
    return ParametricFunction(lambda th: ell(th), t_range=[-0.55, 0.55], stroke_color=GREEN, stroke_width=w,
                              stroke_opacity=op)


def pip3_label():
    lab = T("PIP3", 30, GREEN).move_to([0.55, 1.6, 0])
    ln = Line([0.05, 1.5, 0], ell(0.55) + np.array([0.04, 0.04, 0]), color=GREEN, stroke_width=3)
    return VGroup(lab, ln)


def slots_empty():
    g = VGroup()
    for i in range(5):
        box = RoundedRectangle(corner_radius=0.16, width=SLOT_W, height=SLOT_H, stroke_color=GREY, stroke_width=2.5,
                               fill_color=BG, fill_opacity=1).move_to([SLOT_X, SLOT_Y[i], 0])
        badge = Circle(radius=0.24, stroke_color=GREY, stroke_width=2.5).move_to([SLOT_X - SLOT_W / 2 + 0.4, SLOT_Y[i], 0])
        num = T(str(i + 1), 24, GREY).move_to(badge)
        g.add(VGroup(box, badge, num))
    return g


def slot_downs():
    g = VGroup()
    for i in range(4):
        y = (SLOT_Y[i] + SLOT_Y[i + 1]) / 2
        g.add(Triangle(color=GREY, fill_opacity=1, stroke_width=0).scale(0.11).rotate(PI).move_to([SLOT_X, y, 0]))
    return g


def slot_text(i):
    lines = SLOT_TXT[i]
    t = VGroup(*[T(s, 22, TEXT, slant=ITALIC if s.startswith("(") else NORMAL) for s in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.06)
    return at_left(t, SLOT_X - SLOT_W / 2 + 0.72, SLOT_Y[i])


def slot_lit(slots, i):
    col = SLOT_COL[i]
    return [slots[i][0].animate.set_stroke(col, 3.5), slots[i][1].animate.set_stroke(col), slots[i][2].animate.set_color(col)]


def slot_filled_now(slots, i):
    col = SLOT_COL[i]
    slots[i][0].set_stroke(col, 3.5)
    slots[i][1].set_stroke(col)
    slots[i][2].set_color(col)
    return slot_text(i)


def return_arrow(color=GREY, op=0.8):
    a, b = [SLOT_X + SLOT_W / 2, SLOT_Y[4], 0], [LOOP_X, SLOT_Y[4], 0]
    c, d = [LOOP_X, SLOT_Y[0], 0], [SLOT_X + SLOT_W / 2, SLOT_Y[0], 0]
    g = VGroup(Line(a, b, color=color, stroke_width=6), Line(b, c, color=color, stroke_width=6),
               Arrow(c, d, color=color, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.5))
    g.set_stroke(opacity=op)
    return g


def solid_chip(text, color, size=22):
    c = chip(text, color, size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(c[0])
    return VGroup(back, c)


def toggle(on, color=GREEN):
    cap = RoundedRectangle(corner_radius=0.15, width=0.62, height=0.3, stroke_color=color if on else GREY, stroke_width=2.5,
                           fill_color=color if on else GREY, fill_opacity=0.9 if on else 0.3)
    knob = Circle(radius=0.11, stroke_width=0, fill_color=TEXT, fill_opacity=1)
    knob.move_to(cap.get_right() + LEFT * 0.17 if on else cap.get_left() + RIGHT * 0.17)
    return VGroup(cap, knob)


def mesh(kind, seed=7):
    rng = np.random.RandomState(seed)
    n = {"tight": 26, "radial": 26, "loose": 11}[kind]
    pts = []
    while len(pts) < n:
        x, y = rng.uniform(-4.75, -0.9), rng.uniform(-1.9, 1.9)
        if ((x - CXF) / (FA * 0.9)) ** 2 + ((y - CY) / (FB * 0.9)) ** 2 < 1:
            pts.append((x, y))
    g = VGroup()
    for k, (x, y) in enumerate(pts):
        if kind == "tight":
            a, L = rng.uniform(0, PI), 0.42
        elif kind == "radial":
            a, L = np.arctan2(y - CY, x - (-5.0)), 0.5
        else:
            a, L = np.arctan2(y - CY, x - (-5.0)) + rng.uniform(-0.5, 0.5), 0.8
        d = np.array([np.cos(a), np.sin(a), 0]) * L / 2
        c = np.array([x, y, 0])
        g.add(Line(c - d, c + d, color=ORANGE, stroke_width=3.5, stroke_opacity=0.9))
    return g


def mt_label():
    t = T("microtubules", 26, TEAL).move_to([-3.9, CY + 0.7, 0])
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.16, stroke_width=0, fill_color=BG, fill_opacity=0.9).move_to(t)
    return VGroup(back, t)


def mt_lines(ends):
    g = VGroup()
    for yo, xe in zip((-0.22, 0.0, 0.22), ends):
        g.add(Line([-6.6, CY + yo, 0], [xe, CY + yo, 0], color=TEAL, stroke_width=7))
    return g


def actin_label():
    return T("actin", 28, ORANGE).move_to([CXF, CY - FB - 0.38, 0])


def ph_blocks():
    g = VGroup()
    for th in (-0.35, 0.0, 0.35):
        c = ell(th, 0.0, 0.8)
        b = RoundedRectangle(corner_radius=0.1, width=0.62, height=0.62, stroke_color=TEXT, stroke_width=2.5,
                             fill_color=TEXT, fill_opacity=0.15).move_to(c)
        g.add(VGroup(b, T("PH", 22, TEXT).move_to(c)))
    return g


def ph_label():
    lab = T("proteins\nwith PH\ndomains", 26, TEXT, line_spacing=0.9).move_to([0.5, -1.75, 0])
    ln = Line([0.0, -1.2, 0], ell(-0.35, 0, 0.8) + np.array([0.3, -0.25, 0]), color=TEXT, stroke_width=2.5)
    return VGroup(lab, ln)


def par_chips(spread=False):
    g = VGroup(*[solid_chip(n, PINK, 24) for n in ("Par3", "Par6", "aPKC")])
    if spread:
        for c, p in zip(g, [(-4.3, 1.1), (-4.5, -0.1), (-4.1, -1.2)]):
            c.move_to([p[0], p[1], 0])
    else:
        g.arrange(DOWN, buff=0.14).move_to([-1.25, -0.1, 0])
    return g


def epi_inset():
    cell = RoundedRectangle(corner_radius=0.12, width=0.95, height=1.2, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.12).move_to([-6.1, -3.1, 0])
    top = Line(cell.get_corner(UL) + RIGHT * 0.06, cell.get_corner(UR) + LEFT * 0.06, color=PINK, stroke_width=9)
    lab = T("epithelial\ncell top", 24, TEXT, line_spacing=0.9).move_to([-4.85, -3.1, 0])
    return VGroup(cell, top, lab)


def park(k):
    return ell(-0.55 + 1.1 * k / 8.0, 0.0, 0.86)


def cargo_label():
    lab = T("cargo", 28, GOLD).move_to([0.55, 0.45, 0])
    ln = Line([0.0, 0.4, 0], park(5) + np.array([0.15, 0.0, 0]), color=GOLD, stroke_width=3)
    return VGroup(lab, ln)


def growth_arrow():
    return Arrow([-0.3, CY, 0], [0.75, CY, 0], color=YELLOW, buff=0, stroke_width=10, max_tip_length_to_length_ratio=0.4)


def mol_state(scene, upto, mesh_kind=None, mts=False, cargo=False, ph=False, par=False, sw=False, with_arrow=False,
              loop_color=GREY, phl=False, arrow_text=True):
    """Everything that stands on screen at the start of scene s(23+upto): upto = number of slots already filled."""
    cone = make_cone()
    slots = slots_empty()
    ra = return_arrow(loop_color, 0.8 if loop_color == GREY else 1.0)
    scene.add(cone, slots, slot_downs(), ra, corner_label())
    for i in range(upto):
        scene.add(slot_filled_now(slots, i))
    out = dict(cone=cone, slots=slots, ra=ra)
    if upto >= 1:
        gl, pt, pl = patch(26, 0.28), patch(), pip3_label()
        scene.add(gl, pt, pl)
        out.update(gl=gl, pt=pt, pl=pl)
    if ph:
        out["ph"] = ph_blocks()
        if par:
            out["ph"].set_opacity(0)  # Par now occupies this membrane docking site.
        scene.add(out["ph"])
        if phl:
            out["phl"] = ph_label()
            scene.add(out["phl"])
    if par:
        out["par"] = par_chips()
        out["parbox"] = SurroundingRectangle(out["par"], color=PINK, buff=0.12, corner_radius=0.12, stroke_width=3)
        scene.add(out["par"], out["parbox"])
    if mesh_kind:
        out["mesh"] = mesh(mesh_kind)
        scene.add(out["mesh"])
        out["al"] = actin_label()
        scene.add(out["al"])
    if sw:
        sw1 = solid_chip("Cdc42", GREEN, 24).move_to([-1.65, 0.65, 0])
        sw2 = solid_chip("Rac", GREEN, 24).move_to([-1.65, -0.85, 0])
        tg1 = toggle(True).next_to(sw1, RIGHT, buff=0.15)
        tg2 = toggle(True).next_to(sw2, RIGHT, buff=0.15)
        out["sw"] = VGroup(sw1, sw2, tg1, tg2)
        scene.add(out["sw"])
    if mts:
        out["mts"] = mt_lines(MT_END0)
        out["mtl"] = mt_label()
        scene.add(out["mts"], out["mtl"])
    if cargo:
        ves = VGroup(*[(Circle(radius=0.12) if k % 2 == 0 else Square(side_length=0.22)).set_fill(GOLD, 1).set_stroke(GOLD, 1)
                       .move_to(park(k)) for k in range(9)])
        out["ves"] = ves
        scene.add(ves)
    if with_arrow:
        out["ga"] = growth_arrow()
        scene.add(out["ga"])
    return out


class S23(SpokenScene):
    def construct(self):
        cone = make_cone()
        slots = slots_empty()
        self.add(corner_label())
        self.at("now place")
        self.play(FadeIn(cone), run_time=0.7)
        self.at("molecules")
        self.play(LaggedStart(*[FadeIn(slots[i], shift=LEFT * 0.2) for i in range(5)], lag_ratio=0.2), run_time=1.0)
        self.at("the loop")
        ra = return_arrow()
        self.play(FadeIn(slot_downs()), Create(ra), run_time=0.6)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        st = mol_state(self, 0)
        slots = st["slots"]
        fa = T("future\naxon", 28, YELLOW, line_spacing=0.9).move_to([-5.9, 1.3, 0])
        self.at("pi3 kinase")
        pk = solid_chip("PI3-kinase", GREEN, 26).move_to([-2.4, 0.9, 0])
        self.play(FadeIn(pk, scale=0.8), run_time=0.5)
        self.at("makes the lipid")
        rng = np.random.RandomState(3)
        dots = VGroup(*[Dot(ell(th, 0, 0.93), radius=0.09, color=GREEN) for th in rng.uniform(-1.0, 1.0, 7)])
        t1 = slot_text(0)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.1), *slot_lit(slots, 0), FadeIn(t1),
                  run_time=1.2)
        self.at("builds up")
        pt, gl, pl = patch(), patch(26, 0.28), pip3_label()
        self.play(*[d.animate.move_to(ell(-0.5 + 1.0 * k / 6, 0, 0.97)) for k, d in enumerate(dots)], run_time=0.6)
        self.play(Create(pt), FadeIn(gl), FadeOut(dots), FadeIn(pl), run_time=0.6)
        self.at("future axon")
        self.play(FadeIn(fa, shift=DOWN * 0.1), FadeOut(pk), run_time=0.6)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        st = mol_state(self, 1)
        fa = T("future\naxon", 28, YELLOW, line_spacing=0.9).move_to([-5.9, 1.3, 0])
        self.add(fa)
        self.at("a mark")
        glow = patch(40, 0.3)
        self.play(FadeIn(glow), Indicate(st["pt"], color=GREEN, scale_factor=1.0), run_time=0.9)
        self.at("draws proteins")
        blocks = ph_blocks()
        self.play(*[FadeIn(b, shift=RIGHT * 1.6) for b in blocks], run_time=1.2)
        self.at("domains")
        lab = ph_label()
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        st = mol_state(self, 1, ph=True, phl=True)
        self.add(T("future\naxon", 28, YELLOW, line_spacing=0.9).move_to([-5.9, 1.3, 0]))
        slots = st["slots"]
        self.at("complex which")
        pc = par_chips(spread=True)
        t2 = slot_text(1)
        self.play(FadeOut(st["phl"]), LaggedStart(*[FadeIn(c, scale=0.8) for c in pc], lag_ratio=0.2),
                  *slot_lit(slots, 1), FadeIn(t2), run_time=1.0)
        self.at("also marks")
        ins = epi_inset()
        self.play(FadeIn(ins, shift=RIGHT * 0.15), run_time=0.8)
        self.at("gathers there")
        tgt = par_chips()
        self.play(FadeOut(st["ph"]), *[c.animate.move_to(t.get_center()) for c, t in zip(pc, tgt)], run_time=1.0)
        box = SurroundingRectangle(pc, color=PINK, buff=0.12, corner_radius=0.12, stroke_width=3)
        self.play(Create(box), run_time=0.5)
        self.finish()


class S27(SpokenScene):
    def construct(self):
        st = mol_state(self, 2, ph=True, par=True)
        slots = st["slots"]
        self.add(T("future\naxon", 28, YELLOW, line_spacing=0.9).move_to([-5.9, 1.3, 0]))
        m0 = mesh("tight")
        self.at("at the tip")
        self.play(FadeOut(st["ph"]), FadeOut(st["par"]), FadeOut(st["parbox"]), FadeIn(m0), run_time=0.7)
        self.at("switches")
        sw1 = solid_chip("Cdc42", GREEN, 24).move_to([-1.65, 0.65, 0])
        sw2 = solid_chip("Rac", GREEN, 24).move_to([-1.65, -0.85, 0])
        tg1 = toggle(False).next_to(sw1, RIGHT, buff=0.15)
        tg2 = toggle(False).next_to(sw2, RIGHT, buff=0.15)
        t3 = slot_text(2)
        self.play(FadeIn(sw1), FadeIn(sw2), FadeIn(tg1), FadeIn(tg2), *slot_lit(slots, 2), FadeIn(t3), run_time=0.8)
        self.at("and")
        on1 = toggle(True).move_to(tg1)
        on2 = toggle(True).move_to(tg2)
        self.play(Transform(tg1, on1), Transform(tg2, on2), run_time=0.6)
        self.at("reorganize actin")
        m1 = mesh("radial")
        al = actin_label()
        self.play(Transform(m0, m1), FadeIn(al), run_time=1.5)
        self.finish()


class S28(SpokenScene):
    def construct(self):
        st = mol_state(self, 3, mesh_kind="radial", sw=True)
        slots = st["slots"]
        self.add(T("future\naxon", 28, YELLOW, line_spacing=0.9).move_to([-5.9, 1.3, 0]))
        self.at("loosened actin")
        m1 = mesh("loose")
        t4 = slot_text(3)
        self.play(Transform(st["mesh"], m1), FadeOut(st["sw"]), *slot_lit(slots, 3), FadeIn(t4), run_time=1.1)
        self.at("proposed")
        self.play(Indicate(t4, color=TEXT, scale_factor=1.06), run_time=0.7)
        self.at("microtubules")
        mts = mt_lines((-6.3, -6.3, -6.3))
        mt_end = mt_lines(MT_END0)
        ml = mt_label()
        self.add(mts)
        self.play(FadeIn(ml), Transform(mts, mt_end), run_time=1.4)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        st = mol_state(self, 4, mesh_kind="loose", mts=True)
        slots = st["slots"]
        self.add(T("future\naxon", 28, YELLOW, line_spacing=0.9).move_to([-5.9, 1.3, 0]))
        launch = [2.8, 2.8, 2.8, 4.0, 4.0, 4.0, 5.0, 5.0, 5.0]
        ves = VGroup()
        for k in range(9):
            row = k % 3
            yo = (-0.22, 0.0, 0.22)[row]
            ic = (Circle(radius=0.12) if k % 2 == 0 else Square(side_length=0.22)).set_fill(GOLD, 1).set_stroke(GOLD, 1)
            tgt = park(k)

            def upd(m, dt, k=k, yo=yo, tgt=tgt):
                u = min(max((self.elapsed() - launch[k] - 0.1 * (k % 3)) / 2.2, 0.0), 1.0)
                u = u * u * (3 - 2 * u)
                start = np.array([-6.5, CY + yo, 0.0])
                m.move_to(start + (tgt - start) * u)
                m.set_opacity(1.0 if self.elapsed() >= launch[k] + 0.1 * (k % 3) else 0.0)

            ic.add_updater(upd)
            upd(ic, 0)
            ves.add(ic)
        self.add(ves)
        self.at("part of the loop")
        t5 = slot_text(4)
        self.play(*slot_lit(slots, 4), FadeIn(t5), run_time=0.7)
        self.at("thought to be")
        self.play(Indicate(t5, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.at("more material")
        self.play(FadeIn(cargo_label()), run_time=0.5)
        self.finish()


class S30(SpokenScene):
    def construct(self):
        st = mol_state(self, 5, mesh_kind="loose", mts=True, cargo=True)
        self.add(T("future\naxon", 28, YELLOW, line_spacing=0.9).move_to([-5.9, 1.3, 0]))
        self.at("grows faster")
        ga = growth_arrow()
        gt = T("grows\nfaster", 28, TEXT, line_spacing=0.9).move_to([0.5, 0.75, 0])
        self.play(GrowArrow(ga), FadeIn(gt), run_time=0.9)
        self.at("the loop")
        ra = st["ra"]
        self.play(ra.animate.set_color(GREEN).set_stroke(opacity=1.0), run_time=0.5)
        dot = Dot(ra[0].get_start(), radius=0.12, color=GREEN)
        path = VMobject().set_points_as_corners([ra[0].get_start(), ra[0].get_end(), ra[1].get_end(), ra[2].get_end()])
        self.play(MoveAlongPath(dot, path), run_time=1.0, rate_func=rate_functions.linear)
        self.play(FadeOut(dot), Indicate(st["slots"][0][0], color=GREEN, scale_factor=1.03), run_time=0.4)
        self.finish()


class S31(SpokenScene):
    def construct(self):
        st = mol_state(self, 5, mesh_kind="loose", mts=True, cargo=True, with_arrow=True, loop_color=GREEN)
        self.add(T("future\naxon", 28, YELLOW, line_spacing=0.9).move_to([-5.9, 1.3, 0]))
        self.at("also")
        bar = Line([1.0, -0.75, 0], [1.0, 0.75, 0], color=RED, stroke_width=12)
        bl = T("brake", 28, RED).move_to([0.5, 1.05, 0])
        self.play(Create(bar), FadeIn(bl), run_time=0.7)
        self.at("tends to")
        rh = solid_chip("RhoA", RED, 26).move_to([0.62, -1.65, 0])
        stem = Line([0.7, -1.32, 0], [1.0, -0.75, 0], color=RED, stroke_width=6)
        tx = T("tends to\noppose\ngrowth", 26, TEXT, line_spacing=0.9).move_to([0.45, -2.75, 0])
        self.play(FadeIn(rh, scale=0.8), Create(stem), FadeIn(tx), run_time=0.7)
        self.at("oppose")
        self.play(Indicate(bar, color=RED, scale_factor=1.2),
                  st["ga"].animate.put_start_and_end_on([-0.3, CY, 0], [0.3, CY, 0]), run_time=1.0)
        self.finish()


class S32(SpokenScene):
    def construct(self):
        K = 1.0
        hd = T("What holds the losers back?", 42, TEXT, font=TITLE_FONT).move_to([-0.8, 3.1, 0])
        c = np.array([-0.45, -0.6, 0.0])
        soma = Circle(radius=1.05 * K, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL, fill_opacity=1).move_to(c)
        angs = (52, 18, -18, -52)
        dirs = [np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0]) for a in angs]
        stubs = VGroup(*[Line(c + d * 0.95 * K, c + d * 2.9 * K, color=GREY, stroke_width=28) for d in dirs])
        qs = VGroup(*[T("?", 60, TEXT, font=TITLE_FONT).move_to(c + d * 3.6 * K) for d in dirs])
        self.add(corner_label())
        self.at("what holds")
        self.play(FadeIn(hd, shift=DOWN * 0.1), FadeIn(stubs), FadeIn(soma), run_time=0.8)
        self.at("less settled")
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.2), run_time=0.8)
        self.at("a limited")
        res = RoundedRectangle(corner_radius=0.15, width=1.5, height=0.7, stroke_color=GOLD, stroke_width=3,
                               fill_color=GOLD, fill_opacity=0.35).move_to(c)
        pipes = VGroup(*[Line(c + d * 0.4 * K, c + d * 2.8 * K, color=GOLD, stroke_width=4) for d in dirs])
        c1 = pchip("shared supply", GOLD, 34).move_to([-4.5, 1.2, 0])
        feed = Arrow(c1.get_right(), res.get_left(), color=GOLD, buff=0.12, stroke_width=4)
        self.play(FadeIn(res), Create(pipes), FadeIn(c1, shift=LEFT * 0.2), GrowArrow(feed), run_time=0.8)
        self.at("an inhibitory")
        ars2 = VGroup(*[Arrow(c + d * 3.75 * K, c + d * 3.2 * K, color=RED, buff=0, stroke_width=14,
                              max_tip_length_to_length_ratio=0.6) for d in dirs])
        c2 = pchip("inhibitory signal", RED, 34).move_to([-4.5, -1.6, 0])
        inhibit = DashedLine(c2.get_right(), c + DOWN * 1.2, color=RED, stroke_width=3)
        self.play(FadeOut(qs), FadeIn(ars2), FadeIn(c2, shift=LEFT * 0.2), Create(inhibit), run_time=0.8)
        self.at("both proposed")
        proposed = VGroup(*[T("proposed", 24, TEXT, slant=ITALIC).move_to(c + d * 3.35 + RIGHT * 0.6 + DOWN * 0.35) for d in dirs])
        self.play(FadeIn(proposed), run_time=0.5)
        self.finish()


class S33(SpokenScene):
    def construct(self):
        c1 = chip("competition", GOLD, 36)
        c2 = chip("a lead that compounds", GREEN, 36)
        pl = T("+", 60, TEXT)
        row = VGroup(c1, pl, c2).arrange(RIGHT, buff=0.45).move_to([0, 0.8, 0])
        self.at("a winner", lead=0.0)
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("plus")
        self.play(FadeIn(pl, scale=0.6), run_time=0.4)
        self.at("something that")
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.7)
        self.at("next", lead=0.0)
        nx = T("Next: Rig the Race", 48, TEXT, font=TITLE_FONT).move_to([0, -1.2, 0])
        rule = Line(LEFT * 1.3, RIGHT * 1.3, color=GOLD, stroke_width=4).next_to(nx, UP, buff=0.4)
        self.play(FadeIn(nx, shift=UP * 0.15), GrowFromCenter(rule), run_time=0.35)
        self.finish()


class S34End(EndCard):
    LINE = "A winner needs competition, plus something that compounds a lead."
