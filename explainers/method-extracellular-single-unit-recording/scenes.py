"""Extracellular single-unit and nerve recording: listening to one neuron fire  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the electrode / needle (the apparatus)
  GREY   = cells, tissue, skin, structure, de-emphasised text
  YELLOW = spikes (action potentials, ticks, blips) and the recorded trace
  GREEN  = rate (histogram bars, tuning curve) and a control
  RED    = the pitfall (missed, contaminated)
  ORANGE = unit 1 / a liquid reward; TEAL = unit 2 / a cue; PURPLE = unit 3 (units sorted by spike shape)
  GOLD   = dates, source tags and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
UNIT = [ORANGE, TEAL, PURPLE]


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=4):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def wave(d, amp, w):
    """An extracellular spike: a sharp peak with a small undershoot. d = distance from the centre."""
    return amp * np.exp(-(d / w) ** 2) - 0.22 * amp * np.exp(-((d - 1.8 * w) / (1.6 * w)) ** 2)


def trace_xy(x0, x1, events, noise=0.04, seed=0, N=900):
    rng = np.random.RandomState(seed)
    xs = np.linspace(x0, x1, N)
    ys = np.convolve(rng.randn(N + 4), np.ones(3) / 3.0, mode="same")[2:N + 2] * noise
    for (xc, amp, w) in events:
        ys = ys + wave(xs - xc, amp, w)
    return xs, ys


def trace_chunks(xs, ys, y, cuts, color=YELLOW, w=3.5):
    """Split a trace into polys at the x positions in `cuts` (so pieces can be drawn one by one)."""
    edges = [xs[0]] + list(cuts) + [xs[-1] + 1e-9]
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        idx = np.where((xs >= a) & (xs <= b))[0]
        if len(idx) < 2:
            continue
        lo = max(idx[0] - 1, 0)
        out.append(poly([[xs[i], y + ys[i]] for i in range(lo, idx[-1] + 1)], color, w))
    return out


def neuron(c, r=0.8, color=GREY, dend=6, seed=1):
    """A schematic neuron: round body and radiating processes (a cartoon, not a structure)."""
    rng = np.random.RandomState(seed)
    body = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.14).move_to([c[0], c[1], 0])
    procs = VGroup()
    for k in range(dend):
        a = np.pi * 0.5 + 2 * np.pi * k / dend + rng.uniform(-0.15, 0.15)
        L = r * rng.uniform(1.25, 1.7)
        p0 = np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0])
        p1 = np.array([c[0] + (r + L) * np.cos(a), c[1] + (r + L) * np.sin(a), 0])
        procs.add(Line(p0, p1, color=color, stroke_width=3))
    g = VGroup(procs, body)
    g.body = body
    return g


def electrode(tip, top, wire=BLUE, insulated=True):
    """A fine wire, insulated down to just short of the tip. Tip and top are points."""
    tip = np.array([tip[0], tip[1], 0.0]); top = np.array([top[0], top[1], 0.0])
    d = (top - tip) / np.linalg.norm(top - tip)
    g = VGroup()
    if insulated:
        g.add(Line(tip + d * 0.35, top, color=GREY, stroke_width=11, stroke_opacity=0.45))
    g.add(Line(tip, top, color=wire, stroke_width=4))
    g.tip = tip
    return g


def ticks(xs_, y, h=0.34, color=YELLOW, w=3):
    return VGroup(*[Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=color, stroke_width=w) for x in xs_])


def srctag(text, color=GOLD, size=22):
    return T(text, size, color)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Listening to One Neuron Fire"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a nerve is a tangle of fibres, so one ending's message is unknown; the question; inside versus outside."""

    def construct(self):
        # ---- A: the tangle
        x0, x1, y = -3.4, 3.4, 0.5
        fib = VGroup()
        for k in range(11):
            ph = k * 0.9
            ys_ = y + (k - 5) * 0.19
            pts = [[x, ys_ + 0.13 * np.sin(1.7 * x + ph)] for x in np.linspace(x0, x1, 90)]
            fib.add(poly(pts, GREY, 3))
        outline = RoundedRectangle(corner_radius=0.5, width=x1 - x0 + 0.5, height=2.7, stroke_color=GREY,
                                   stroke_width=3).move_to([0, y, 0])
        nerve_lbl = lab("a whole nerve: many fibres", 30, GREY).move_to([0, 2.5, 0])
        end = chip("sensory ending", GREY, 26).move_to([-5.2, y, 0])
        brain = chip("brain", GREY, 26).move_to([5.5, y, 0])
        a_in = arr([-3.95, y, 0], [-3.62, y, 0], GREY, 4, 0.14)
        a_out = arr([3.62, y, 0], [4.55, y, 0], GREY, 4, 0.16)
        self.at("A whole nerve")
        self.play(FadeIn(outline), Create(fib, run_time=1.4, lag_ratio=0.12), FadeIn(nerve_lbl), run_time=1.5)
        self.at("no one could say")
        hot = fib[5].copy().set_stroke(YELLOW, 6)
        q = T("?", 64, YELLOW, weight=BOLD).move_to([0, -1.6, 0])
        self.play(FadeIn(end, shift=RIGHT * 0.2), FadeIn(brain, shift=LEFT * 0.2), GrowArrow(a_in), GrowArrow(a_out), run_time=0.6)
        self.play(Create(hot, run_time=0.9, rate_func=linear), FadeIn(q), run_time=0.9)
        qt = lab("what did this one fibre send?", 30, YELLOW).move_to([0, -2.6, 0])
        self.play(FadeIn(qt), run_time=0.4)

        # ---- B: the question
        self.at("What does one neuron")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        nc = [-1.0, 0.3]
        nr = neuron(nc, 0.85, GREY, 7, 3)
        qn = T("?", 56, YELLOW, weight=BOLD).move_to([nc[0], nc[1], 0])
        self.play(FadeIn(nr), FadeIn(qn), run_time=0.7)
        ax_o = np.array([1.7, -0.6, 0])
        axis = Line(ax_o, ax_o + [4.4, 0, 0], color=GREY, stroke_width=3)
        axl = lab("time", 24, GREY).next_to(axis, DOWN, buff=0.12)
        qline = poly([[ax_o[0] + t, 0.6 + (0.0 if i % 2 else 0.0)] for i, t in enumerate(np.linspace(0, 4.4, 8))], GREY, 3).set_stroke(opacity=0.0)
        fire = lab("when does it fire?", 30, YELLOW).move_to([3.9, 0.7, 0])
        self.play(Create(axis), FadeIn(axl), FadeIn(fire), run_time=0.6)
        c1 = chip("stimulus", BLUE, 28).move_to([-5.2, 1.7, 0])
        c2 = chip("movement", BLUE, 28).move_to([-5.2, 0.3, 0])
        c3 = chip("reward", BLUE, 28).move_to([-5.2, -1.1, 0])
        self.at("a stimulus")
        self.play(FadeIn(c1, shift=RIGHT * 0.2), GrowArrow(arr([c1.get_right()[0] + 0.1, 1.7, 0], [-3.45, 1.2, 0], GREY, 4, 0.18)), run_time=0.5)
        self.at("movement")
        self.play(FadeIn(c2, shift=RIGHT * 0.2), GrowArrow(arr([c2.get_right()[0] + 0.1, 0.3, 0], [-3.45, 0.3, 0], GREY, 4, 0.18)), run_time=0.5)
        self.at("reward changes")
        self.play(FadeIn(c3, shift=RIGHT * 0.2), GrowArrow(arr([c3.get_right()[0] + 0.1, -1.1, 0], [-3.45, -0.6, 0], GREY, 4, 0.18)), run_time=0.5)

        # ---- C: inside vs outside
        self.at("Recording from inside")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        L = neuron([-3.3, 0.8], 0.95, GREY, 6, 5)
        el = electrode([-3.3 + 0.2, 0.95], [-1.5, 3.0], insulated=False)
        self.play(FadeIn(L), run_time=0.4)
        self.play(Create(el), run_time=0.7)
        inl = lab("inside the cell", 30, BLUE).move_to([-3.3, -2.3, 0])
        imp = lab("only for a cell you can impale", 26, GREY).move_to([-3.3, -2.95, 0])
        self.at("only for a cell")
        self.play(FadeIn(inl), FadeIn(imp), run_time=0.5)
        self.at("from outside")
        # tissue on the right
        rng = np.random.RandomState(4)
        cells = VGroup()
        spots = [(1.6, 1.8), (3.4, 1.2), (2.6, -0.2), (4.9, -0.1), (1.2, -0.6), (4.3, 2.4), (2.4, 3.0), (5.3, 1.4), (3.6, -1.5), (1.8, -1.8), (5.0, -1.9)]
        for (cx, cy) in spots:
            cells.add(Circle(radius=rng.uniform(0.45, 0.75), stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                             fill_opacity=0.12).move_to([cx, cy, 0]))
        e2 = electrode([2.6 + 0.5, 0.15], [3.9, 3.3], insulated=False)
        tis = lab("outside, in intact tissue", 30, YELLOW).move_to([3.4, -2.85, 0])
        self.play(FadeIn(cells, lag_ratio=0.1), run_time=0.8)
        self.play(Create(e2), FadeIn(tis), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Electrode(SpokenScene):
    """current outside the cell; a fine electrode beside it hears blips; the same idea with a needle in a human nerve."""

    def construct(self):
        cx, cy = -3.6, 1.15
        nr = neuron([cx, cy], 0.85, GREY, 6, 7)
        body = nr.body
        # --- A: currents outside
        self.at("Active neurons")
        self.play(FadeIn(nr), run_time=0.6)
        arrows = VGroup()
        for a in (0.2, 0.9, 1.6, 2.4, 3.9, 4.6, 5.4):
            p0 = np.array([cx + 0.98 * np.cos(a), cy + 0.98 * np.sin(a), 0])
            p1 = np.array([cx + 1.6 * np.cos(a), cy + 1.6 * np.sin(a), 0])
            arrows.add(arr(p0, p1, YELLOW, 4, 0.14))
        cur_lbl = lab("currents in the fluid outside", 26, YELLOW).move_to([cx + 3.9, cy - 0.3, 0])
        self.at("measured in the fluid")
        self.play(*[GrowArrow(a) for a in arrows], FadeIn(cur_lbl), run_time=0.7)
        # --- B: the electrode
        el = electrode([cx + 1.1, cy + 0.15], [cx + 3.3, cy + 2.15])
        self.at("a fine electrode")
        self.play(FadeOut(arrows), FadeOut(cur_lbl), run_time=0.3)
        self.play(Create(el), run_time=0.8)
        el_lbl = lab("fine electrode, outside the cell", 26, BLUE).move_to([cx + 6.3, cy + 1.45, 0])
        self.play(FadeIn(el_lbl), run_time=0.4)
        # trace with blips, drawn piece by piece; the cell flashes at each spike
        ty = -2.2
        sp = [-4.1, -1.6, 0.4, 1.7, 4.4]
        xs, ys = trace_xy(-6.0, 6.0, [(x, 1.25, 0.07) for x in sp], noise=0.045, seed=3)
        cuts = []
        for x in sp:
            cuts += [x - 0.35, x + 0.45]
        pieces = trace_chunks(xs, ys, ty, cuts, YELLOW, 3.5)
        base = DashedLine([-6.0, ty, 0], [6.0, ty, 0], color=GREY, stroke_width=1.5)
        self.at("records its action potentials")
        self.play(FadeIn(base), run_time=0.2)
        for i, pc in enumerate(pieces):
            is_spike = (i % 2 == 1)
            if is_spike:
                self.play(body.animate.set_fill(YELLOW, 0.55), run_time=0.08)
                self.play(Create(pc, rate_func=linear), body.animate.set_fill(GREY, 0.14), run_time=0.2)
            else:
                self.play(Create(pc, rate_func=linear), run_time=0.14)
        blip_lbl = lab("each action potential: a brief blip", 26, YELLOW).move_to([0, -3.3, 0])
        self.play(FadeIn(blip_lbl), run_time=0.4)
        # --- C: Hubel and Wiesel's wire
        self.at("sharpened tungsten")
        w1 = lab("sharpened tungsten wire", 26, BLUE).move_to([cx + 6.3, cy + 1.45, 0])
        self.play(Transform(el_lbl, w1), run_time=0.5)
        self.at("insulated with lacquer")
        ins = lab("insulated with lacquer", 26, GREY).move_to([cx + 6.3, cy + 0.8, 0])
        self.play(FadeIn(ins), run_time=0.5)

        # --- D: microneurography
        self.at("In a conscious person")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        sk = 1.7
        skin = VGroup(Line([-6.0, sk, 0], [6.0, sk, 0], color=GREY, stroke_width=4),
                      Line([-6.0, sk - 0.18, 0], [6.0, sk - 0.18, 0], color=GREY, stroke_width=2, stroke_opacity=0.5))
        skl = lab("skin", 26, GREY).move_to([-5.5, sk + 0.4, 0])
        ny = 0.2
        nerve = VGroup(RoundedRectangle(corner_radius=0.4, width=11.0, height=1.5, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.1).move_to([0, ny, 0]))
        for k in range(7):
            yy = ny + (k - 3) * 0.17
            nerve.add(Line([-5.3, yy, 0], [5.3, yy, 0], color=GREY, stroke_width=2, stroke_opacity=0.7))
        nl = lab("a nerve in the arm", 26, GREY).move_to([-4.0, ny - 1.2, 0])
        self.play(Create(skin), FadeIn(skl), FadeIn(nerve), FadeIn(nl), run_time=0.8)
        d = np.array([0.5, 0.866, 0.0])
        tip0 = np.array([0.6, sk + 0.3, 0.0])
        needle = electrode(tip0, tip0 + d * 1.9, insulated=True)
        nd_lbl = lab("tungsten needle", 26, BLUE).move_to([3.7, 3.0, 0])
        self.play(Create(needle), FadeIn(nd_lbl), run_time=0.5)
        self.at("through the skin")
        self.play(needle.animate.shift(np.array([-0.55, -0.95, 0])), run_time=0.7)
        ty2 = -2.3
        xs2, ys2 = trace_xy(-6.0, 6.0, [], noise=0.09, seed=8)
        nz = poly([[xs2[i], ty2 + ys2[i]] for i in range(len(xs2))], GREY, 3)
        self.play(Create(nz, run_time=0.9, rate_func=linear))
        self.at("moved by hand")
        hand = lab("moved by hand", 26, BLUE).move_to([3.7, 2.3, 0])
        self.play(FadeIn(hand), run_time=0.3)
        for dx in (0.3, -0.3):
            self.play(needle.animate.shift(RIGHT * dx), run_time=0.3)
        self.play(needle.animate.shift(np.array([-0.3, -0.52, 0])), run_time=0.5)
        self.at("activity of interest")
        sp2 = [-4.4, -2.8, -1.2, 0.5, 2.1, 3.8, 5.2]
        xs3, ys3 = trace_xy(-6.0, 6.0, [(x, 1.2, 0.07) for x in sp2], noise=0.045, seed=9)
        good = poly([[xs3[i], ty2 + ys3[i]] for i in range(len(xs3))], YELLOW, 3.5)
        disc = lab("activity discriminated", 26, YELLOW).move_to([0, -3.3, 0])
        self.play(FadeOut(nz), run_time=0.25)
        self.play(Create(good, run_time=1.6, rate_func=linear), FadeIn(disc), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def snippet(shape, cx, cy, sx=1.0, color=YELLOW, w=3):
    """One spike waveform as a small plot, centred at (cx, cy). shape = (amp, width)."""
    amp, wd = shape
    xs = np.linspace(-0.7, 0.9, 80)
    ys = wave(xs, amp, wd)
    return poly([[cx + sx * x, cy + y] for x, y in zip(xs, ys)], color, w)


SHAPES = [(1.0, 0.07), (0.45, 0.07), (0.6, 0.2)]     # unit 1: tall and narrow, 2: short and narrow, 3: broad


class S03Sorting(SpokenScene):
    """a raw trace with spikes of three shapes; group by shape into units; then the Purkinje cell's two shapes."""

    def construct(self):
        ty = 2.4
        seq = [0, 2, 1, 0, 1, 2, 0, 0, 2, 1, 0, 2, 1, 1]
        xs_s = np.linspace(-4.2, 5.4, len(seq))
        rng = np.random.RandomState(5)
        xs_s = xs_s + rng.uniform(-0.15, 0.15, len(seq))
        ev = [(x, SHAPES[k][0] * 1.0, SHAPES[k][1]) for x, k in zip(xs_s, seq)]
        xs, ys = trace_xy(-5.0, 6.0, ev, noise=0.05, seed=2)
        raw = poly([[xs[i], ty + ys[i]] for i in range(len(xs))], YELLOW, 3)
        raw_lbl = lab("raw record (example)", 24, GREY).move_to([-4.2, ty + 1.15, 0])
        self.at("Spikes from one cell")
        self.play(Create(raw, run_time=1.3, rate_func=linear), FadeIn(raw_lbl))
        self.at("characteristic shape")
        # three overlay boxes
        boxes = VGroup()
        snips = VGroup()
        cxs = [-3.9, 0.0, 3.9]
        for k, cxx in enumerate(cxs):
            b = RoundedRectangle(corner_radius=0.12, width=3.0, height=1.7, stroke_color=GREY, stroke_width=2).move_to([cxx, 0.15, 0])
            boxes.add(b)
        self.play(FadeIn(boxes), run_time=0.4)
        for k, cxx in enumerate(cxs):
            s = snippet(SHAPES[k], cxx - 0.35, -0.15, 1.0, GREY, 4)
            snips.add(s)
        self.play(*[Create(s) for s in snips], run_time=0.9)
        self.at("grouped by waveform")
        # recolour trace spikes into units: overlay coloured spike pieces
        over = VGroup()
        for (x, k) in zip(xs_s, seq):
            idx = np.where((xs > x - 0.32) & (xs < x + 0.48))[0]
            over.add(poly([[xs[i], ty + ys[i]] for i in idx], UNIT[k], 4.5))
        self.play(FadeIn(over), *[snips[k].animate.set_stroke(UNIT[k], 5) for k in range(3)], run_time=0.8)
        names = VGroup(*[lab(f"unit {k + 1}", 26, UNIT[k]).move_to([cxs[k], 1.3, 0]) for k in range(3)])
        self.play(FadeIn(names), run_time=0.4)
        self.at("spike sorting")
        rows = VGroup()
        for k in range(3):
            yk = -1.7 - 0.5 * k
            tk = ticks([x for x, kk in zip(xs_s, seq) if kk == k], yk, 0.36, UNIT[k], 4)
            rows.add(tk)
        rlab = VGroup(*[lab(f"unit {k + 1}", 22, UNIT[k]).move_to([-5.7, -1.7 - 0.5 * k, 0]) for k in range(3)])
        self.play(*[Create(r) for r in rows], FadeIn(rlab), run_time=1.2)
        self.at("decoding the spike times")
        st = lab("the spike times of each neuron", 28, TEXT).move_to([0.0, -3.2, 0])
        self.play(FadeIn(st), run_time=0.5)

        # ---- Purkinje
        self.at("In a Purkinje cell")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        pk = lab("a Purkinje cell, one record (schematic)", 28, GREY).move_to([0, 3.1, 0])
        simple = (0.9, 0.07)
        cplx = (0.9, 0.3)
        evp = []
        px = np.linspace(-5.2, 5.2, 9)
        kinds = [0, 0, 1, 0, 0, 0, 1, 0, 0]
        for x, k in zip(px, kinds):
            evp.append((x, 1.0 if k == 0 else 1.15, 0.07 if k == 0 else 0.3))
        xp, yp = trace_xy(-6.0, 6.0, evp, noise=0.05, seed=12)
        ptr = poly([[xp[i], 0.4 + yp[i]] for i in range(len(xp))], YELLOW, 3.5)
        self.play(FadeIn(pk), Create(ptr, run_time=0.9, rate_func=linear), run_time=0.9)
        self.at("simple and complex")
        s1 = snippet((1.0, 0.07), -3.2, -2.3, 1.6, GREEN, 5)
        s2 = snippet((1.15, 0.3), 2.6, -2.3, 1.6, ORANGE, 5)
        l1 = lab("simple spike", 28, GREEN).move_to([-3.2, -3.35, 0])
        l2 = lab("complex spike", 28, ORANGE).move_to([2.8, -3.35, 0])
        self.play(Create(s1), FadeIn(l1), Create(s2), FadeIn(l2), run_time=1.0)
        self.at("one record gives both")
        bx = SurroundingRectangle(VGroup(s1, s2, l1, l2), color=GREY, buff=0.25, corner_radius=0.15, stroke_width=2)
        self.play(Create(bx), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Trials(SpokenScene):
    """repeat the stimulus; one raster row per trial, one tick per spike; histogram bars; spikes per second."""

    def construct(self):
        rng = np.random.RandomState(21)
        NT = 12
        X0, X1 = -5.2, 2.4
        tmin, tmax = -1.0, 2.0

        def tx(t):
            return X0 + (t - tmin) / (tmax - tmin) * (X1 - X0)

        def rate(t):
            return 3.0 + (22.0 * np.exp(-(t - 0.3) / 0.45) if t > 0.0 else 0.0) * min(1.0, t / 0.08 if t > 0 else 0.0)
        trials = []
        for _ in range(NT):
            sp = []
            t = tmin
            while t < tmax:
                t += 0.01
                if rng.rand() < rate(t) * 0.01:
                    sp.append(t)
            trials.append(sp)
        rowy0, dy = 3.0, 0.24
        ex = lab("example data", 24, GREY).move_to([-4.6, 3.55, 0])
        onset = DashedLine([tx(0), 3.3, 0], [tx(0), -2.95, 0], color=GREY, stroke_width=2)
        onl = lab("stimulus onset", 24, GREY).move_to([tx(0) + 1.1, 3.55, 0])
        rl = lab("trial", 22, GREY).rotate(PI / 2).move_to([X0 - 0.45, rowy0 - dy * 5.5, 0])
        rows = VGroup()
        self.add(ex, onset, onl)
        self.at("repeated many times")
        for i in range(NT):
            y = rowy0 - dy * i
            tk = ticks([tx(t) for t in trials[i]], y, 0.19, YELLOW, 3)
            rows.add(tk)
            self.play(FadeIn(tk), run_time=0.16)
        self.at("Each repeat")
        hl = SurroundingRectangle(rows[3], color=BLUE, buff=0.04, stroke_width=3)
        hl.stretch_to_fit_width(X1 - X0 + 0.2).move_to([(X0 + X1) / 2, rowy0 - dy * 3, 0])
        self.play(Create(hl), FadeIn(rl), run_time=0.5)
        k_lbl = lab("one row = one repeat", 24, BLUE).move_to([4.55, rowy0 - dy * 3, 0])
        self.play(FadeIn(k_lbl), run_time=0.3)
        self.at("one tick")
        self.play(Indicate(rows[3], color=YELLOW, scale_factor=1.0), run_time=0.6)
        k2 = lab("one tick = one spike", 24, YELLOW).move_to([4.55, rowy0 - dy * 3 - 0.55, 0])
        self.play(FadeOut(hl), FadeIn(k2), run_time=0.3)
        # histogram
        self.at("peristimulus time histogram")
        nb = 24
        edges = np.linspace(tmin, tmax, nb + 1)
        bw = (tmax - tmin) / nb
        counts = np.array([sum(1 for tr in trials for t in tr if edges[i] <= t < edges[i + 1]) for i in range(nb)])
        rates = counts / (NT * bw)
        hmax = 2.6
        scale = hmax / max(rates.max(), 1e-6)
        hy = -2.95
        bars = VGroup()
        for i in range(nb):
            h = max(rates[i] * scale, 0.02)
            r = Rectangle(width=(X1 - X0) / nb * 0.92, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
            r.move_to([X0 + (i + 0.5) * (X1 - X0) / nb, hy + h / 2, 0])
            bars.add(r)
        hax = Line([X0, hy, 0], [X1, hy, 0], color=GREY, stroke_width=2)
        ylab = lab("spikes per second", 24, GREEN).rotate(PI / 2).move_to([X0 - 0.45, hy + 1.3, 0])
        self.play(Create(hax), run_time=0.3)
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], FadeIn(ylab), run_time=1.0)
        self.at("aligned to stimulus onset")
        self.play(Indicate(onl, color=YELLOW), run_time=0.5)
        self.at("It divides each")
        pk = int(np.argmax(rates))
        self.play(bars[pk].animate.set_fill(YELLOW, 0.95), FadeOut(k_lbl), FadeOut(k2), run_time=0.4)
        f1 = lab("rate in one bin =", 26, GREEN).move_to([4.5, -0.2, 0])
        f2 = lines("spike count", "÷ (repeats × bin width)", size=24, color=TEXT, buff=0.1, align=LEFT)
        f2.next_to(f1, DOWN, buff=0.2, aligned_edge=LEFT)
        fg = VGroup(f1, f2).move_to([4.5, -0.4, 0])
        self.play(FadeIn(fg), run_time=0.5)
        self.at("giving spikes per second")
        self.play(Indicate(ylab, color=GREEN), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Tuning(SpokenScene):
    """a tuning curve: rate against bar orientation, versus the spontaneous rate; idealised V1 numbers."""

    def construct(self):
        AX0, AX1 = -4.8, 2.9
        AY0, AY1 = -1.9, 2.5
        def px(d):
            return AX0 + d / 180.0 * (AX1 - AX0)
        def py(r):
            return AY0 + r / 44.0 * (AY1 - AY0)
        def curve(d):
            return 2.0 + 38.0 * np.exp(-((d - 90.0) ** 2) / (2 * 27.5 ** 2))
        ax = VGroup(Line([AX0, AY0, 0], [AX1, AY0, 0], color=GREY, stroke_width=3),
                    Line([AX0, AY0, 0], [AX0, AY1 + 0.2, 0], color=GREY, stroke_width=3))
        yl = lab("mean rate (spikes per second)", 24, GREEN).rotate(PI / 2).move_to([AX0 - 0.55, 0.0, 0])
        xl = lab("bar orientation (degrees)", 24, BLUE).move_to([(AX0 + AX1) / 2, AY0 - 1.3, 0])
        tag = chip("idealised example, not a real cell", RED, 22).move_to([3.6, 3.15, 0])
        self.at("A tuning curve")
        self.play(Create(ax), run_time=0.6)
        self.at("mean rate")
        self.play(FadeIn(yl), run_time=0.4)
        self.at("bar orientation")
        icons = VGroup()
        for d in (0, 30, 60, 90, 120, 150, 180):
            ang = np.deg2rad(d)
            c = np.array([px(d), AY0 - 0.4, 0])
            v = np.array([np.cos(ang), np.sin(ang), 0]) * 0.22
            icons.add(Line(c - v, c + v, color=BLUE, stroke_width=7))
            icons.add(lab(str(d), 22, GREY).move_to([px(d), AY0 - 0.85, 0]).set_opacity(0.9) if d in (0, 90, 180) else VGroup())
        self.play(FadeIn(xl), FadeIn(icons), run_time=0.7)
        self.at("many trials per value")
        dots = VGroup()
        for d in range(0, 181, 15):
            dots.add(Dot([px(d), py(curve(d)), 0], radius=0.07, color=GREEN))
        self.play(LaggedStart(*[FadeIn(dd, scale=1.6) for dd in dots], lag_ratio=0.12), run_time=1.6)
        self.at("spontaneous rate")
        sp = DashedLine([AX0, py(2.0), 0], [AX1, py(2.0), 0], color=GREY, stroke_width=3)
        spl = lines("spontaneous rate,", "with no bar", size=24, color=GREY, buff=0.06, align=LEFT).move_to([AX1 + 2.3, py(2.0) + 0.1, 0])
        self.play(Create(sp), FadeIn(spl), run_time=0.6)
        self.at("In this idealized cell")
        cv = poly([[px(d), py(curve(d))] for d in np.linspace(0, 180, 120)], GREEN, 5)
        self.play(FadeIn(tag, shift=DOWN * 0.1), Create(cv, run_time=1.0, rate_func=linear), run_time=1.0)
        self.at("90 degrees")
        pk = Dot([px(90), py(40), 0], radius=0.12, color=YELLOW)
        pkl = M("40", 34, YELLOW).next_to(pk, RIGHT, buff=0.2)
        pkn = lab("spikes per second", 24, YELLOW).next_to(pkl, RIGHT, buff=0.15)
        self.play(FadeIn(pk, scale=1.6), FadeIn(pkl), FadeIn(pkn), run_time=0.5)
        self.at("30 and 150")
        d1 = Dot([px(30), py(5.5), 0], radius=0.12, color=YELLOW)
        d2 = Dot([px(150), py(5.5), 0], radius=0.12, color=YELLOW)
        l1 = M("5 to 6", 28, YELLOW).move_to([d1.get_x() - 0.2, d1.get_y() + 0.95, 0])
        l2 = M("5 to 6", 28, YELLOW).move_to([d2.get_x() + 0.2, d2.get_y() + 0.95, 0])
        self.play(FadeIn(d1, scale=1.6), FadeIn(d2, scale=1.6), FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.at("With no bar")
        z = M("2", 30, GREY).move_to([AX1 + 0.4, py(2.0) + 0.0, 0])
        self.play(FadeIn(z), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """bias to large active cells (and how many cells are missed); merged units and the interval check."""

    def construct(self):
        # ---- A: bias
        cells = VGroup()
        spec = [(-4.2, 1.2, 1.0, 1), (-1.9, -0.9, 0.42, 0), (-3.9, -2.2, 0.38, 0), (0.0, 1.9, 0.45, 0),
                (0.9, -0.5, 1.0, 1), (2.9, 1.1, 0.42, 0), (3.6, -1.9, 0.45, 0), (-1.7, 2.3, 0.38, 0),
                (-5.5, -0.7, 0.4, 0), (4.6, 2.5, 0.38, 0), (-2.2, 0.7, 0.4, 0)]
        for (x, y, r, big) in spec:
            c = Circle(radius=r, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.14).move_to([x, y, 0])
            cells.add(c)
        el = electrode([0.35, 0.25], [2.2, 3.4], insulated=True)
        self.at("The method samples")
        self.play(FadeIn(cells, lag_ratio=0.08), run_time=0.9)
        self.play(Create(el), run_time=0.8)
        el_l = lab("electrode", 26, BLUE).move_to([3.3, 3.0, 0])
        self.play(FadeIn(el_l), run_time=0.3)
        self.at("favors large")
        big = [cells[0], cells[4]]
        self.play(*[b.animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.4) for b in big], run_time=0.5)
        small = VGroup(*[c for i, c in enumerate(cells) if i not in (0, 4)])
        self.play(small.animate.set_stroke(RED, 2.5).set_stroke(opacity=0.8), run_time=0.5)
        l_big = lab("large, active cells: picked up", 26, YELLOW).move_to([-1.0, -3.2, 0])
        l_small = lines("small or quiet cells:", "missed", size=26, color=RED, buff=0.06, align=ORIGIN).move_to([4.6, -0.95, 0])
        self.play(FadeIn(l_big), FadeIn(l_small), run_time=0.5)

        # ---- B: how many are missed
        self.at("In one hippocampal estimate")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        W = 9.0
        X = -5.6
        b1 = Rectangle(width=W, height=0.7, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([X + W / 2, 1.7, 0])
        t1 = lab("signals in range (about 1,000)", 28, TEXT).move_to([X + 2.6, 2.55, 0])
        tg = chip("rat CA1, tetrode", GREY, 24).move_to([4.6, 2.55, 0])
        self.play(FadeIn(tg), run_time=0.4)
        self.at("could record signals")
        self.play(GrowFromEdge(b1, LEFT), FadeIn(t1), run_time=0.8)
        wd = W * 0.08
        b2 = Rectangle(width=wd, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([X + wd / 2, 0.2, 0])
        t2 = lab("should be detectable (60 to 100)", 28, YELLOW).next_to(b2, RIGHT, buff=0.3)
        self.at("should be detectable")
        self.play(GrowFromEdge(b2, LEFT), FadeIn(t2), run_time=0.7)
        b3 = Rectangle(width=W * 0.006, height=0.7, stroke_width=0, fill_color=ORANGE, fill_opacity=1.0).move_to([X + W * 0.003, -1.2, 0])
        t3 = lab("usually found (about 6)", 28, ORANGE).next_to(b3, RIGHT, buff=0.3)
        self.at("usually found")
        self.play(GrowFromEdge(b3, LEFT), FadeIn(t3), run_time=0.7)
        ctl = chip("control: pair with imaging, which does not need large spikes", GREEN, 26).move_to([0, -2.8, 0])
        self.at("The control is to pair")
        self.play(FadeIn(ctl, shift=UP * 0.15), run_time=0.7)

        # ---- C: merged units
        self.at("A unit may also hold")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        nA = neuron([-2.2, 1.7], 0.55, GREY, 5, 11)
        nB = neuron([2.2, 1.7], 0.55, GREY, 5, 12)
        la = lab("neuron A", 28, GREY).move_to([-4.6, 1.7, 0])
        lb = lab("neuron B", 28, GREY).move_to([4.6, 1.7, 0])
        ry = -1.0
        xs_all = [-4.6, -3.9, -3.2, -2.5, -1.9, -0.4, 0.2, 0.95, 1.6, 2.26, 2.44, 3.4, 4.0, 4.6]
        row_line = Line([-5.5, ry, 0], [5.5, ry, 0], color=GREY, stroke_width=2)
        tk_all = ticks(xs_all, ry + 0.45, 0.8, YELLOW, 5)
        ul = lab("one unit", 28, YELLOW).move_to([4.6, ry - 0.6, 0])
        self.play(FadeIn(nA), FadeIn(nB), FadeIn(la), FadeIn(lb), run_time=0.7)
        self.play(FadeIn(row_line), FadeIn(tk_all), FadeIn(ul), run_time=0.8)
        self.at("Because a neuron")
        gap_ok = DoubleArrow([-3.2, ry - 0.25, 0], [-2.5, ry - 0.25, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.12)
        gap_ok_l = lab("a normal gap", 24, GREY).move_to([-2.85, ry - 0.7, 0])
        self.play(Create(gap_ok), FadeIn(gap_ok_l), run_time=0.5)
        self.at("too close together")
        ring = Circle(radius=0.55, stroke_color=RED, stroke_width=4).move_to([2.35, ry + 0.45, 0])
        gap_bad = DoubleArrow([2.26, ry - 0.25, 0], [2.44, ry - 0.25, 0], buff=0, color=RED, stroke_width=3, tip_length=0.08)
        self.play(Create(ring), Create(gap_bad), run_time=0.5)
        self.at("signal contamination")
        cl = lab("schematic: a gap too short for one neuron: contamination", 26, RED).move_to([0.3, ry - 1.5, 0])
        self.play(FadeIn(cl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Findings(SpokenScene):
    """Hubel and Wiesel: orientation; O'Keefe and Dostrovsky: place."""

    def construct(self):
        LX, RX = -3.3, 3.5
        C = 0.0                      # the left panel is built at the centre, then slides left
        CY = 1.5
        scr = Circle(radius=1.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([C, CY, 0])
        bar = Line([C - 1.25, CY, 0], [C + 1.25, CY, 0], color=BLUE, stroke_width=10).rotate(-PI / 2 - 150 * DEGREES, about_point=[C, CY, 0])
        self.at("recorded single cells")
        self.play(FadeIn(scr), FadeIn(bar), run_time=0.6)
        t1 = srctag("Hubel and Wiesel, 1962 (cat), 1968 (monkey)", GOLD, 22).move_to([C, -3.35, 0])
        t1.scale(min(1.0, 5.8 / t1.width))
        self.play(FadeIn(t1), run_time=0.4)
        sy = -0.35
        sx0, sx1 = C - 2.7, C + 2.7
        strip = Line([sx0, sy - 0.3, 0], [sx1, sy - 0.3, 0], color=GREY, stroke_width=2)
        rng = np.random.RandomState(31)
        xs_t = []
        for x in np.linspace(sx0, sx1, 170):
            u = (x - (sx0 + sx1) / 2) / ((sx1 - sx0) / 2)
            p = (u + 1) / 2          # fraction of the sweep (150 degrees); the burst only in the last 20 degrees
            rt = 0.07 + (0.9 * np.exp(-(((1 - p) / 0.07)) ** 2) if p > 1 - 20 / 150.0 else 0.0)
            if rng.rand() < rt * 0.5:
                xs_t.append(x)
        tk = ticks(xs_t, sy + 0.05, 0.45, YELLOW, 3)
        self.play(Create(strip), run_time=0.2)
        rt0 = max(3.0, self.t_of("orientation selectivity") - 0.3 - self.elapsed())
        self.play(Rotate(bar, angle=150 * DEGREES, about_point=[C, CY, 0], rate_func=linear),
                  Create(tk, rate_func=linear, lag_ratio=1.0), run_time=rt0)
        self.at("orientation selectivity")
        sel = lab("fires most at one orientation", 26, YELLOW).move_to([C, -1.05, 0])
        self.play(FadeIn(sel), run_time=0.4)
        r1 = VGroup(lab("cat", 24, GREY), chip("simple", GREY, 22), chip("complex", GREY, 22)).arrange(RIGHT, buff=0.2)
        r2 = VGroup(lab("monkey", 24, GREY), chip("simple", GREY, 22), chip("complex", GREY, 22), chip("hypercomplex", GREY, 22)).arrange(RIGHT, buff=0.18)
        cls = VGroup(r1, r2).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        cls.scale(min(1.0, 5.9 / cls.width)).move_to([C, -2.0, 0])
        self.play(FadeIn(cls, lag_ratio=0.3), run_time=0.7)
        leftp = VGroup(scr, bar, t1, strip, tk, sel, cls)

        # ---- right: place
        self.at("In 1971")
        self.play(leftp.animate.shift(RIGHT * (LX - C)), run_time=0.6)
        arena = Rectangle(width=5.0, height=3.6, stroke_color=GREY, stroke_width=3).move_to([RX, 1.0, 0])
        self.play(Create(arena), run_time=0.5)
        t2 = srctag("O'Keefe and Dostrovsky, 1971", GOLD, 22).move_to([RX, -3.35, 0])
        self.play(FadeIn(t2), run_time=0.3)
        self.at("recorded single units")
        cx0, cy0 = RX, 1.0

        def path(t):
            return np.array([cx0 + 2.1 * np.sin(2 * np.pi * (2 * t + 0.1)), cy0 + 1.33 * np.sin(2 * np.pi * (3 * t)), 0])
        pth = ParametricFunction(lambda t: path(t), t_range=[0, 1], color=GREY, stroke_width=1.5, stroke_opacity=0.5)
        trk = ValueTracker(0.0)
        dot = Dot(path(0), radius=0.14, color=TEXT)
        dot.add_updater(lambda m: m.move_to(path(trk.get_value())))

        def vel(t):
            v = path(min(t + 0.002, 1.0)) - path(max(t - 0.002, 0.0))
            return v / (np.linalg.norm(v) + 1e-9)
        face = always_redraw(lambda: Arrow(path(trk.get_value()), path(trk.get_value()) + vel(trk.get_value()) * 0.5, buff=0,
                                           color=BLUE, stroke_width=4, tip_length=0.14, max_tip_length_to_length_ratio=0.5))
        fld_c = np.array([cx0 + 1.1, cy0 + 0.75, 0])
        field = DashedVMobject(Circle(radius=0.85, stroke_color=YELLOW, stroke_width=3).move_to(fld_c))
        spk = VGroup()
        rng2 = np.random.RandomState(6)
        for tk_ in np.linspace(0, 1, 900):
            p = path(tk_)
            if np.linalg.norm(p - fld_c) < 0.85 and vel(tk_)[0] > 0.3 and rng2.rand() < 0.3:
                d = Dot(p + np.array([rng2.uniform(-0.05, 0.05), rng2.uniform(-0.05, 0.05), 0.0]), radius=0.06, color=YELLOW)
                d.set_opacity(0)
                d.add_updater(lambda m, tt=tk_: m.set_opacity(1.0 if trk.get_value() >= tt else 0.0))
                spk.add(d)
        fr = lab("schematic: a freely moving animal; arrow = facing", 22, GREY).move_to([RX, -1.2, 0])
        fr.scale(min(1.0, 6.2 / fr.width)).move_to([RX, -1.2, 0])
        fl = lines("each yellow dot: one spike,", "only here and facing this way", size=22, color=YELLOW, buff=0.06, align=ORIGIN).move_to([RX, -1.95, 0])
        self.add(spk)
        self.play(Create(pth), FadeIn(dot), FadeIn(face), FadeIn(fr), run_time=0.7)
        self.at("freely moving")
        rt = max(2.0, self.t_of("particular places") - 0.1 - self.elapsed())
        self.play(trk.animate.set_value(1.0), run_time=rt, rate_func=linear)
        self.at("particular places")
        self.play(Create(field), FadeIn(fl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Findings(SpokenScene):
    """Mirenowicz and Schultz: the response moves to the cue; Johansson and Vallbo: 334 human units in four classes; the rule."""

    def construct(self):
        LX, RX = -3.3, 3.5
        hd1 = lab("monkey dopamine neurons", 28, TEXT).move_to([LX, 3.15, 0])
        rowx0, rowx1 = LX - 2.8, LX + 2.8
        TH = 0.8

        def burst(x, y, n=7, seed=0, spread=0.4):
            r = np.random.RandomState(seed)
            return ticks(sorted(x + r.uniform(0, spread, n)), y, TH, YELLOW, 4)

        def sparse(y, seed, xs_excl=()):
            r = np.random.RandomState(seed)
            xs_ = [x for x in r.uniform(rowx0 + 0.15, rowx1 - 0.15, 5) if all(abs(x - e) > 0.7 for e in xs_excl)]
            return ticks(xs_, y, TH, YELLOW, 3)
        y1, y2 = 1.2, -1.2
        ln1 = Line([rowx0, y1 - 0.5, 0], [rowx1, y1 - 0.5, 0], color=GREY, stroke_width=2)
        liq1 = chip("liquid", ORANGE, 24).move_to([LX + 1.0, y1 + 0.95, 0])
        l1 = lab("unpredicted", 24, GREY).move_to([rowx0 + 1.0, y1 + 0.95, 0])
        self.at("In 1994")
        self.play(FadeIn(hd1), FadeIn(ln1), FadeIn(l1), FadeIn(sparse(y1, 3, [LX + 1.0])), run_time=0.5)
        self.at("three quarters")
        q = chip("three quarters of neurons", GREEN, 24).move_to([LX, -2.5, 0])
        self.play(FadeIn(q), run_time=0.5)
        self.at("unpredicted liquid")
        self.play(FadeIn(liq1, shift=DOWN * 0.15), run_time=0.4)
        self.play(FadeIn(burst(LX + 1.0, y1, 8, 1)), run_time=0.5)
        ln2 = Line([rowx0, y2 - 0.5, 0], [rowx1, y2 - 0.5, 0], color=GREY, stroke_width=2)
        cue = chip("cue", TEAL, 24).move_to([LX - 1.4, y2 + 0.95, 0])
        liq2 = chip("liquid", ORANGE, 24).move_to([LX + 1.5, y2 + 0.95, 0])
        self.at("Once a cue predicted")
        self.play(FadeIn(ln2), FadeIn(cue, shift=DOWN * 0.15), FadeIn(liq2, shift=DOWN * 0.15), run_time=0.6)
        self.play(FadeIn(sparse(y2, 5, [LX - 1.4, LX + 1.5])), run_time=0.4)
        self.at("moved to the cue")
        self.play(FadeIn(burst(LX - 1.4, y2, 8, 2)), run_time=0.6)
        t1 = srctag("Mirenowicz and Schultz, 1994", GOLD, 22).move_to([LX, -3.15, 0])
        self.play(FadeIn(t1), run_time=0.3)

        # ---- right: touch afferents
        self.at("grouped")
        hd2 = lab("human median nerve", 28, TEXT).move_to([RX, 3.15, 0])
        sk = 2.3
        skin = Line([RX - 2.9, sk, 0], [RX + 2.9, sk, 0], color=GREY, stroke_width=4)
        ny = 1.2
        nerve = VGroup(RoundedRectangle(corner_radius=0.35, width=5.8, height=1.5, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.12).move_to([RX, ny, 0]))
        for k in range(6):
            nerve.add(Line([RX - 2.6, ny + (k - 2.5) * 0.2, 0], [RX + 2.6, ny + (k - 2.5) * 0.2, 0], color=GREY,
                           stroke_width=2, stroke_opacity=0.7))
        d = np.array([0.5, 0.866, 0.0])
        tipn = np.array([RX - 0.6, ny + 0.1, 0.0])
        nd = electrode(tipn, tipn + d * 1.35, insulated=True)
        self.play(FadeIn(hd2), Create(skin), FadeIn(nerve), Create(nd), run_time=0.8)
        self.at("units from the human")
        n334 = M("334 units", 38, YELLOW).move_to([RX, 0.0, 0])
        n334b = lab("low-threshold units, human hand", 24, GREY).move_to([RX, -0.5, 0])
        self.play(FadeIn(n334, shift=UP * 0.1), FadeIn(n334b), run_time=0.5)
        self.at("into four classes")
        names = ["RA", "PC", "SA I", "SA II"]
        chips = VGroup(*[chip(n, TEXT, 30) for n in names]).arrange(RIGHT, buff=0.22).move_to([RX, -1.6, 0])
        by = lab("grouped by firing and receptive field", 24, TEXT).move_to([RX, -0.85 + 0.0, 0]).shift(UP * 0.0)
        by.move_to([RX, -1.0, 0])
        small = VGroup(*[Circle(radius=0.14, stroke_color=YELLOW, stroke_width=3).next_to(chips[i], DOWN, buff=0.15) for i in (0, 2)])
        small_l = lab("small fields (RA, SA I)", 22, YELLOW).move_to([RX, -2.75, 0])
        self.play(FadeIn(chips, lag_ratio=0.2), FadeIn(by), run_time=0.8)
        self.play(FadeIn(small), FadeIn(small_l), run_time=0.4)
        t2 = srctag("Johansson and Vallbo, 1979", GOLD, 22).move_to([RX, -3.3, 0])
        self.play(FadeIn(t2), run_time=0.3)

        # ---- the rule
        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        rule = lines("A recording shows that firing", "goes with an event, never", "that firing causes it.",
                     size=40, color=TEXT, buff=0.2, align=ORIGIN)
        rule_box = SurroundingRectangle(rule, color=GOLD, stroke_width=3, buff=0.45, corner_radius=0.2)
        head = lab("KEEP THIS RULE", 26, GOLD, weight=BOLD).next_to(rule_box, UP, buff=0.25)
        grp = VGroup(rule, rule_box, head).move_to([0, 0, 0])
        self.play(FadeIn(head), Create(rule_box), run_time=0.5)
        self.at("a recording shows")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "Recording shows firing goes with an event, never that firing causes it."
