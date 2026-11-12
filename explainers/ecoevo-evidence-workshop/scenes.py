"""What a Negative Is Worth: film 1 of the evidence workshop (Biochemistrypedia explainer)

COLOUR MAP (same in both films)
  BLUE  = the scoop, theta        GREEN = capture, gamma        GOLD = the well, delta
  TEAL filled pond = occupied     GREY outline pond = empty     RED dashed line = the 5% stop line
Bars and counters are computed from the lesson's formula; nets, dials and sliders are schematic.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

NEWT = "#F29E4C"
DARK = "#0f1117"
GX, GY, CELL = -3.6, -0.2, 0.6          # the pond grid: 10 x 10, x -6.6..-0.6
BARX = 4.6                                # the side bar
RX = 1.85                                 # centre of the middle column

_rs = random.Random(11)
ORDER = _rs.sample(range(100), 20)       # the 20 occupied ponds, in the order they get caught
D1, D2, D3, HALF, REST = ORDER[:10], ORDER[10:15], ORDER[15:17], ORDER[17], ORDER[18:20]


def pct_after(prior, n, q=0.5):
    m = (1 - q) ** n
    return 100 * prior * m / ((1 - prior) + prior * m)


def ambient(scene, n=16, seed=3):
    rng = random.Random(seed)
    motes = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.02, 0.05), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.12, 0.3))
        d.move_to([rng.uniform(-7, 7), rng.uniform(-4, 4), 0])
        d.v = (rng.uniform(-0.12, 0.12), rng.uniform(0.05, 0.2))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 4.1:
                m.shift(DOWN * 8.2)
            if abs(m.get_x()) > 7.2:
                m.shift(LEFT * 14.4 * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-10)
    scene.add(motes)


def pond_icon(kind):
    if kind == "empty":
        m = Ellipse(width=0.5, height=0.4, stroke_color=GREY, stroke_width=2.5, fill_opacity=0)
    elif kind == "occ":
        m = Ellipse(width=0.5, height=0.4, stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.9)
    else:  # hidden
        m = Ellipse(width=0.5, height=0.4, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL, fill_opacity=0.3)
    m.kind = kind
    return m


def bottle(color=BLUE, s=1.0):
    body = RoundedRectangle(corner_radius=0.08, width=0.42, height=0.55, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=0.3)
    neck = Rectangle(width=0.18, height=0.2, stroke_color=color, stroke_width=3.5, fill_opacity=0).next_to(body, UP, buff=0)
    return VGroup(body, neck).scale(s)


def net(y, color, holes, x0=-6.2, x1=1.2, hw=1.0):
    g = VGroup()
    edges = [x0] + sum([[h - hw / 2, h + hw / 2] for h in sorted(holes)], []) + [x1]
    for a, b in zip(edges[0::2], edges[1::2]):
        g.add(Line([a, y, 0], [b, y, 0], color=color, stroke_width=12).set_cap_style(CapStyleType.ROUND))
        for xx in np.arange(a + 0.15, b - 0.05, 0.3):
            g.add(Line([xx, y, 0], [xx, y - 0.4, 0], color=color, stroke_width=4).set_opacity(0.7))
    return g


NET_Y = [2.3, 0.3, -1.7]
NET_SPEC = [(NET_Y[0], BLUE, [-5.2, -3.0, -1.0], "the scoop (θ)"),
            (NET_Y[1], GREEN, [-4.6, -3.0, -1.6], "capture (γ)"),
            (NET_Y[2], GOLD, [-5.4, -3.0, -0.6], "the well (δ)")]


def net_label(y, color, text):
    return T(text, 34, color, weight=BOLD).move_to([3.9, y + 0.0, 0])


class PondScene(SpokenScene):
    """Shared pieces of the pond-grid world, rebuilt in the same place in every scene."""

    def pos(self, i):
        r, c = divmod(i, 10)
        return np.array([GX + (c - 4.5) * CELL, GY + (4.5 - r) * CELL, 0])

    def grid(self, removed=(), hidden=(), occ=(), shimmer=True):
        self.pd = {}
        g = VGroup()
        for i in range(100):
            if i in removed:
                continue
            kind = "occ" if i in occ else ("hidden" if i in hidden else "empty")
            m = pond_icon(kind).move_to(self.pos(i))
            m.phase = (i * 0.73) % 6.28
            self.pd[i] = m
            g.add(m)
        self.g = g
        g.t = 0.0
        if shimmer:
            def sh(grp, dt):
                grp.t += dt
                for p in grp:
                    if p.kind == "empty":
                        p.set_stroke(opacity=0.62 + 0.3 * np.sin(grp.t * 1.3 + p.phase))
                    elif p.kind == "hidden":
                        p.set_fill(TEAL, 0.3 + 0.12 * np.sin(grp.t * 2.2 + p.phase))
            g.add_updater(sh)
        return g

    def slot(self, k):
        return np.array([RX + (k % 6 - 2.5) * 0.45, -1.75 - (k // 6) * 0.5, 0])

    def tray(self, n):
        box = RoundedRectangle(corner_radius=0.15, width=3.3, height=2.6, stroke_color=TEAL, stroke_width=2.5).move_to([RX, -2.1, 0])
        lab = T("detected", 28, TEAL).move_to([RX, -1.15, 0])
        ps = VGroup(*[pond_icon("occ").scale(0.8).move_to(self.slot(k)) for k in range(n)])
        return VGroup(box, lab, ps)

    def make_bar(self, v):
        self.pct = ValueTracker(v)
        frame = Rectangle(width=1.4, height=5.0, stroke_color=GREY, stroke_width=3).move_to([BARX, -0.3, 0])
        fill = Rectangle(width=1.4, height=0.1, stroke_width=0, fill_color=TEAL, fill_opacity=0.95)

        def fu(m):
            h = max(self.pct.get_value() * 0.2, 0.02)
            m.become(Rectangle(width=1.4, height=h, stroke_width=0, fill_color=TEAL, fill_opacity=0.95)
                     .move_to([BARX, -2.8 + h / 2, 0]))
        fu(fill)
        fill.add_updater(fu)
        ro = M("0", 28, DARK)

        def ru(m):
            h = max(self.pct.get_value() * 0.2, 0.02)
            m.become(M(f"{self.pct.get_value():.1f}%", 28, TEXT, weight=BOLD).move_to([BARX, 1.65, 0]))
        ru(ro)
        ro.add_updater(ru)
        line = DashedLine([3.75, -1.8, 0], [5.3, -1.8, 0], color=RED, stroke_width=5)
        lt = T("5% stop\nline", 24, RED).move_to([6.1, -1.8, 0])
        title = T("negatives still\noccupied", 26, TEXT).move_to([BARX, 2.95, 0])
        return VGroup(frame, fill, ro, line, lt, title)

    def sweep(self, label, dur):
        band = Rectangle(width=6.1, height=0.7, stroke_width=0, fill_color=BLUE, fill_opacity=0.22).move_to([GX, GY + 2.9, 0])
        bt = bottle().move_to([-0.15, GY + 2.9, 0])
        g = VGroup(band, bt)
        self.add(g)
        self.play(g.animate.shift(DOWN * 5.8), run_time=dur, rate_func=linear)
        self.play(FadeOut(g), run_time=0.3)

    def flash_and_move(self, idxs, start_slot, extra=(), extra2=()):
        ps = [self.pd[i] for i in idxs]
        self.play(*[p.animate.set_fill(TEAL, 1).set_stroke(YELLOW, 4).scale(1.5) for p in ps], *extra, run_time=0.6)
        for p in ps:
            p.kind = "occ"
        tg = [pond_icon("occ").scale(0.8).move_to(self.slot(start_slot + j)) for j in range(len(ps))]
        self.play(*[Transform(p, t) for p, t in zip(ps, tg)], *extra2, run_time=1.2)

    def counter(self, lines, y=1.25):
        cols = [TEAL, TEXT, GREY]
        g = VGroup(*[T(s, 30, cols[i]) for i, s in enumerate(lines)]).arrange(DOWN, buff=0.12)
        return g.move_to([RX, y, 0])

    def hidden_after(self, n):
        """Hidden occupied ponds after n samples (grid indices)."""
        out = []
        if n < 1:
            out += D1
        if n < 2:
            out += D2
        if n < 3:
            out += D3
        out += [HALF] + REST
        return out


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Integrative Evidence Workshop"
    TITLE = "What a Negative Is Worth"


class S01Question(SpokenScene):
    def construct(self):
        ambient(self)
        pond = Ellipse(width=7.2, height=5.2, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.14).move_to([-2.7, -0.2, 0])
        body = Ellipse(width=0.9, height=0.34, fill_color=NEWT, fill_opacity=1, stroke_width=0)
        head = Circle(radius=0.2, fill_color=NEWT, fill_opacity=1, stroke_width=0).move_to([0.5, 0, 0])
        tail = Polygon([-0.45, 0.12, 0], [-1.05, 0, 0], [-0.45, -0.12, 0], fill_color=NEWT, fill_opacity=1, stroke_width=0)
        legs = VGroup(*[Line([x, s * 0.12, 0], [x + 0.08, s * 0.34, 0], color=NEWT, stroke_width=5) for x in (0.2, -0.25) for s in (1, -1)])
        newt = VGroup(body, head, tail, legs).scale(1.4)
        newt.t = 0.0
        newt.ang = 0.0
        cx, cy = -2.7, -0.3

        def swim(m, dt):
            m.t += dt
            a = 0.55 * m.t
            m.move_to([cx + 2.3 * np.cos(a), cy + 1.5 * np.sin(a), 0])
            h = np.arctan2(1.5 * np.cos(a), -2.3 * np.sin(a))
            m.rotate(h - m.ang)
            m.ang = h
        newt.add_updater(swim)
        swim(newt, 0)
        self.play(FadeIn(pond), FadeIn(newt), run_time=1.0)
        self.at("what have you learned")
        bt = bottle(s=1.6).move_to([0.2, 1.6, 0])
        self.play(FadeIn(bt, shift=DOWN * 0.3), run_time=0.8)
        self.at("is the species gone")
        q = T("?", 96, YELLOW, weight=BOLD).move_to([-2.7, 3.0, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.at("at 53 english")
        c1 = VGroup(M("53", 60, TEAL, weight=BOLD), T("ponds: newts seen\nduring sampling", 28)).arrange(RIGHT, buff=0.3).move_to([4.4, 2.4, 0])
        self.play(FadeOut(q), FadeIn(c1, shift=LEFT * 0.3), run_time=0.8)
        self.at("newts were seen")
        self.play(bt.animate.shift(DOWN * 1.4), run_time=1.2)
        self.play(bt.animate.shift(UP * 1.4), run_time=1.2)
        self.at("yet 13")
        c2 = VGroup(M("13%", 60, RED, weight=BOLD), T("of samples\n(about 7):\nno newt DNA", 28)).arrange(RIGHT, buff=0.3).move_to([4.4, 0.4, 0])
        self.play(FadeIn(c2, shift=LEFT * 0.3), run_time=0.8)
        self.at("showed no newt dna")
        base = Line([1.7, -2.1, 0], [6.5, -2.1, 0], color=GOLD, stroke_width=6)
        lab = T("qPCR trace: flat", 28, GOLD).move_to([4.1, -1.5, 0])
        dot = Dot(radius=0.12, color=TEXT).move_to([1.7, -2.1, 0])
        self.play(Create(base), FadeIn(lab), run_time=0.6)
        self.add(dot)
        self.play(dot.animate.move_to([6.5, -2.1, 0]), run_time=2.2, rate_func=linear)
        src = T("Buxton and colleagues, 2021", 26, TEXT).move_to([4.1, -3.3, 0])
        self.play(FadeIn(src), dot.animate.move_to([1.7, -2.1, 0]), run_time=2.4, rate_func=linear)
        self.finish()


class S02Nets(SpokenScene):
    def construct(self):
        ambient(self)
        dot = Dot(radius=0.17, color=TEXT).move_to([-3.0, 3.4, 0])
        dl = T("DNA", 28, TEXT).add_updater(lambda m: m.next_to(dot, RIGHT, 0.2))
        self.play(FadeIn(dot), FadeIn(dl), run_time=0.6)
        dot.add_updater(lambda m, dt: None)
        self.play(dot.animate.shift(DOWN * 0.15), run_time=0.8, rate_func=there_and_back)
        self.at("a series of nets")
        nets = [net(y, c, h) for (y, c, h, _) in NET_SPEC]
        for n_ in nets:
            n_.set_opacity(0.25)
        self.play(LaggedStart(*[FadeIn(n_) for n_ in nets], lag_ratio=0.4), run_time=1.6)
        self.play(dot.animate.shift(DOWN * 0.15), run_time=0.8, rate_func=there_and_back)
        labels = [net_label(y, c, t) for (y, c, h, t) in NET_SPEC]
        # first net
        self.at("first")
        self.play(nets[0].animate.set_opacity(1), run_time=0.6)
        self.at("in the water you scoop")
        self.play(dot.animate.move_to([-3.0, 1.3, 0]), run_time=1.5)
        self.at("that chance is theta")
        self.play(FadeIn(labels[0], shift=LEFT * 0.3), run_time=0.7)
        self.at("second")
        self.play(nets[1].animate.set_opacity(1), run_time=0.6)
        self.at("must capture it")
        self.play(dot.animate.move_to([-3.0, -0.7, 0]), run_time=1.5)
        self.at("that chance is gamma")
        self.play(FadeIn(labels[1], shift=LEFT * 0.3), run_time=0.7)
        self.at("third")
        self.play(nets[2].animate.set_opacity(1), run_time=0.6)
        self.at("must amplify it")
        self.play(dot.animate.move_to([-3.0, -3.0, 0]), run_time=1.3)
        self.at("that chance is delta")
        self.play(FadeIn(labels[2], shift=LEFT * 0.3), dot.animate.move_to([-3.0, -3.2, 0]), run_time=0.9)
        self.finish()


class S03Q(SpokenScene):
    def construct(self):
        ambient(self)
        nets = VGroup(*[net(y, c, h) for (y, c, h, _) in NET_SPEC])
        labels = VGroup(*[net_label(y, c, t) for (y, c, h, t) in NET_SPEC])
        self.add(nets, labels)
        self.play(FadeOut(labels), run_time=0.4)
        self.play(nets[0].animate.move_to([-2.5, 0.3, 0]), nets[2].animate.move_to([-2.5, 0.3, 0]),
                  nets[1].animate.set_x(-2.5), run_time=1.0)
        # dial
        CX, CY, R = 0.0, -0.4, 3.4
        arcs = VGroup(Arc(radius=R, start_angle=PI * 2 / 3, angle=PI / 3, arc_center=[CX, CY, 0], color=GOLD, stroke_width=14),
                      Arc(radius=R, start_angle=PI / 3, angle=PI / 3, arc_center=[CX, CY, 0], color=GREEN, stroke_width=14),
                      Arc(radius=R, start_angle=0, angle=PI / 3, arc_center=[CX, CY, 0], color=BLUE, stroke_width=14))
        arcs = VGroup(Arc(radius=R, start_angle=0, angle=PI / 3, arc_center=[CX, CY, 0], color=GOLD, stroke_width=14),
                      Arc(radius=R, start_angle=PI / 3, angle=PI / 3, arc_center=[CX, CY, 0], color=GREEN, stroke_width=14),
                      Arc(radius=R, start_angle=2 * PI / 3, angle=PI / 3, arc_center=[CX, CY, 0], color=BLUE, stroke_width=14))
        ticks = VGroup(*[T(s, 30, TEXT).move_to([CX + (R + 0.45) * np.cos(PI * (1 - v)), CY + (R + 0.45) * np.sin(PI * (1 - v)), 0])
                         for s, v in (("0", 0), ("0.5", 0.5), ("1", 1))])
        self.play(FadeTransform(nets, arcs), FadeIn(ticks), run_time=1.2)
        v = ValueTracker(0.0)
        needle = Line([CX, CY, 0], [CX - 2.6, CY, 0], color=TEXT, stroke_width=8)
        needle.add_updater(lambda m: m.become(Line([CX, CY, 0], [CX + 2.6 * np.cos(PI * (1 - v.get_value())),
                                                                 CY + 2.6 * np.sin(PI * (1 - v.get_value())), 0],
                                                    color=TEXT, stroke_width=8)))
        hub = Dot([CX, CY, 0], radius=0.15, color=TEXT)
        qt = M("q", 60, YELLOW, weight=BOLD).move_to([CX, -1.3, 0])
        self.play(FadeIn(needle), FadeIn(hub), FadeIn(qt, scale=0.6), run_time=0.6)
        self.at("it is the chance")
        cap = T("one sample's chance of detecting\nan occupied pond", 30).move_to([CX, -2.45, 0])
        self.play(Write(cap), run_time=4.5)
        self.at("round number")
        tag = T("round number for this film", 28, GOLD).move_to([CX, -3.5, 0])
        self.play(FadeIn(tag), run_time=0.6)
        self.at("q is one half")
        ro = M("q = 0.00", 60, YELLOW, weight=BOLD)
        ro.add_updater(lambda m: m.become(M(f"q = {v.get_value():.2f}", 60, YELLOW, weight=BOLD).move_to([CX, -1.3, 0])))
        self.remove(qt)
        self.add(ro)
        self.play(v.animate.set_value(0.5), run_time=2.0, rate_func=smooth)
        self.finish()


class S04Grid(PondScene):
    def construct(self):
        ambient(self)
        g = self.grid()
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in g], lag_ratio=0.012), run_time=2.4)
        self.at("before sampling")
        self.play(Indicate(g, color=GREY, scale_factor=1.03), run_time=1.2)
        self.at("20 of them")
        ps = [self.pd[i] for i in ORDER]
        self.play(*[p.animate.set_fill(TEAL, 0.9).set_stroke(TEAL, 2).scale(1.25) for p in ps], run_time=1.0)
        self.play(*[p.animate.scale(1 / 1.25) for p in ps], run_time=0.5)
        for p in ps:
            p.kind = "occ"
        self.at("those are teal")
        l1 = VGroup(T("occupied: 20", 32, TEAL, weight=BOLD), T("the prior", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([RX, 2.0, 0])
        self.play(FadeIn(l1, shift=LEFT * 0.3), *[Indicate(p, color=TEAL, scale_factor=1.35) for p in ps], run_time=1.4)
        self.at("the other 80")
        l2 = T("empty: 80", 32, GREY, weight=BOLD).move_to([RX, 0.5, 0])
        self.play(FadeIn(l2, shift=LEFT * 0.3), run_time=0.8)
        self.at("with no false positives")
        bar = self.make_bar(0.0)
        self.play(FadeIn(bar), run_time=0.5)
        self.play(self.pct.animate.set_value(20.0), run_time=1.4)
        self.at("an empty pond always")
        grey = [p for p in g if p.kind == "empty"]
        self.play(LaggedStart(*[Indicate(p, color=TEXT, scale_factor=1.3) for p in grey], lag_ratio=0.02), run_time=2.2)
        self.finish()


class S05Sample1(PondScene):
    def construct(self):
        ambient(self)
        hid = set(ORDER)
        g = self.grid(occ=hid)
        bar = self.make_bar(20.0)
        l1 = VGroup(T("occupied: 20", 32, TEAL, weight=BOLD), T("the prior", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([RX, 2.0, 0])
        l2 = T("empty: 80", 32, GREY, weight=BOLD).move_to([RX, 0.5, 0])
        self.add(g, bar, l1, l2)
        tag = T("sample 1", 34, BLUE, weight=BOLD).move_to([RX, 2.7, 0])
        self.play(FadeOut(l1), FadeOut(l2), FadeIn(tag), run_time=0.6)
        tr = self.tray(0)
        self.play(FadeIn(tr), run_time=0.6)
        self.sweep("sample 1", 2.0)
        self.at("half the occupied")
        self.at("light up")
        self.flash_and_move(D1, 0)
        self.at("ten occupied ponds stay")
        rest = [self.pd[i] for i in ORDER if i not in D1]
        self.play(*[p.animate.set_fill(TEAL, 0.3).set_stroke(TEAL, 2.5) for p in rest], FadeOut(tag), run_time=1.0)
        for p in rest:
            p.kind = "hidden"
            p.set_stroke(TEAL, 2.5)
        self.at("hidden among")
        ctr = self.counter(["10 hidden", "90 negative"])
        self.play(FadeIn(ctr, shift=LEFT * 0.3), run_time=0.8)
        self.at("drops to eleven")
        self.play(self.pct.animate.set_value(100 / 9), run_time=2.0)
        self.finish()


class S06Predict(PondScene):
    def construct(self):
        ambient(self)
        g = self.grid(removed=set(D1), hidden=self.hidden_after(1))
        tr = self.tray(10)
        bar = self.make_bar(100 / 9)
        ctr = self.counter(["10 hidden", "90 negative"])
        self.add(g, tr, bar, ctr)
        self.at("take a second")
        tag = T("sample 2:\nnew water", 30, BLUE, weight=BOLD).move_to([RX, 2.7, 0])
        bt = bottle(s=1.5).move_to([GX, 3.3, 0])
        bt.t = 0.0

        def hov(m, dt):
            m.t += dt
            m.move_to([GX + 2.2 * np.sin(0.7 * m.t), 3.3 + 0.12 * np.sin(2.1 * m.t), 0])
        bt.add_updater(hov)
        self.play(FadeIn(tag), FadeIn(bt), run_time=0.8)
        self.at("how many hidden")
        t1 = T("hidden ponds\nleft?", 32, YELLOW, weight=BOLD).move_to([RX, 1.3, 0])
        self.play(FadeOut(ctr), run_time=0.3)
        self.play(FadeIn(t1), run_time=0.5)
        hid = [self.pd[i] for i in self.hidden_after(1)]
        self.play(*[Indicate(p, color=TEAL, scale_factor=1.5) for p in hid], run_time=1.5)
        self.at("and what share")
        t2 = T("share of negatives\noccupied?", 26, YELLOW, weight=BOLD).move_to([RX, -0.1, 0])
        self.play(FadeIn(t2), Indicate(bar[1], color=YELLOW, scale_factor=1.06), run_time=1.0)
        self.finish()


class S07Pause(PondScene):
    def construct(self):
        ambient(self)
        g = self.grid(removed=set(D1), hidden=self.hidden_after(1))
        tr = self.tray(10)
        bar = self.make_bar(100 / 9)
        t1 = T("hidden ponds\nleft?", 32, YELLOW, weight=BOLD).move_to([RX, 1.3, 0])
        t2 = T("share of negatives\noccupied?", 26, YELLOW, weight=BOLD).move_to([RX, -0.1, 0])
        cap = T("Predict: how many hidden ponds, and what share?", 28, TEXT).move_to([0.5, -3.7 + 0.0, 0])
        cap.move_to([-1.2, 3.55, 0])
        self.add(g, tr, bar, t1, t2, cap)
        for k in range(5, 0, -1):
            n = M(str(k), 64, YELLOW, weight=BOLD).move_to([RX, 2.45, 0])
            self.add(n)
            self.play(n.animate.scale(0.85).set_opacity(0.5), run_time=0.95)
            self.remove(n)
            self.wait(0.05)
        self.finish()


class S08Reveal(PondScene):
    def construct(self):
        ambient(self)
        g = self.grid(removed=set(D1), hidden=self.hidden_after(1))
        tr = self.tray(10)
        bar = self.make_bar(100 / 9)
        ctr = self.counter(["10 hidden", "90 negative"])
        self.add(g, tr, bar, ctr)
        tag = T("sample 2", 34, BLUE, weight=BOLD).move_to([RX, 2.75, 0])
        self.play(FadeIn(tag), run_time=0.4)
        self.sweep("sample 2", 1.6)
        self.at("are caught")
        self.flash_and_move(D2, 10)
        self.at("five stay hidden")
        self.play(Transform(ctr, self.counter(["5 hidden", "85 negative"])), run_time=0.8)
        self.at("the share falls")
        self.play(self.pct.animate.set_value(100 * 5 / 85), run_time=1.8)
        self.at("a third sample")
        self.play(Transform(tag, T("sample 3", 34, BLUE, weight=BOLD).move_to([RX, 2.75, 0])), run_time=0.3)
        self.sweep("sample 3", 1.0)
        self.at("two and a half hidden")
        hp = self.pd[HALF]
        self.flash_and_move(D3, 15, extra=(hp.animate.scale(0.55).set_fill(TEAL, 0.25),),
                            extra2=(Transform(ctr, self.counter(["2.5 hidden", "82.5 negative", "(on average)"])),))
        self.at("about 3")
        self.play(self.pct.animate.set_value(100 * 2.5 / 82.5), run_time=1.5)
        self.finish()


class S09Bar(SpokenScene):
    def construct(self):
        ambient(self)
        vals = [pct_after(0.2, n) for n in range(4)]
        xs = [-4.2, -1.5, 1.2, 3.9]
        base, k = -2.7, 0.2
        # the side bar as it ended in the last scene, then it grows into the step plot
        side = Rectangle(width=1.4, height=vals[3] * k * 1.0, stroke_width=0, fill_color=TEAL, fill_opacity=0.95).move_to([BARX, -2.8 + vals[3] * 0.1, 0])
        sframe = Rectangle(width=1.4, height=5.0, stroke_color=GREY, stroke_width=3).move_to([BARX, -0.3, 0])
        stitle = T("negatives still\noccupied", 26, TEXT).move_to([BARX, 2.95, 0])
        sline = DashedLine([3.75, -1.8, 0], [5.3, -1.8, 0], color=RED, stroke_width=5)
        slt = T("5% stop\nline", 24, RED).move_to([6.1, -1.8, 0])
        side.become(Rectangle(width=1.4, height=vals[3] * 0.2, stroke_width=0, fill_color=TEAL, fill_opacity=0.95).move_to([BARX, -2.8 + vals[3] * 0.1, 0]))
        self.add(sframe, side, stitle, sline, slt)
        self.at("tracks the chance")
        bars = VGroup(*[Rectangle(width=1.7, height=v * k, stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.9)
                        .move_to([x, base + v * k / 2, 0]) for v, x in zip(vals, xs)])
        axis = Line([-5.5, base, 0], [5.2, base, 0], color=GREY, stroke_width=3)
        ln = DashedLine([-5.5, base + 5 * k, 0], [5.3, base + 5 * k, 0], color=RED, stroke_width=5)
        lt = T("5% stop\nline", 24, RED).move_to([6.1, base + 5 * k, 0])
        xl = VGroup(*[M(str(n), 32, TEXT).move_to([x, base - 0.35, 0]) for n, x in enumerate(xs)])
        xt = T("independent negative samples", 28, TEXT).move_to([-0.3, base - 0.85, 0])
        self.play(FadeOut(VGroup(sframe, side, stitle, sline, slt)), FadeIn(axis), FadeIn(ln), FadeIn(lt), FadeIn(xl), FadeIn(xt), run_time=1.2)
        vl = []
        for i, (b, v, x) in enumerate(zip(bars, vals, xs)):
            ly = base + v * k + 0.35
            if abs(ly - (base + 5 * k)) < 0.45:
                ly = base + 5 * k + 0.5
            lab = M(f"{v:.1f}%" if v < 10 else f"{v:.0f}%", 34, TEXT, weight=BOLD).move_to([x, ly, 0])
            lab.set_stroke(DARK, 10, background=True)
            vl.append(lab)
        comp = T("computed", 26, GREY).move_to([-5.8, 3.4, 0]).align_to([-6.6, 0, 0], LEFT)
        self.play(FadeIn(comp), run_time=0.3)
        for i, b in enumerate(bars):
            b.save_state()
            b.stretch_to_fit_height(0.02, about_edge=DOWN)
            b.move_to([xs[i], base + 0.01, 0])
        self.add(bars)
        self.play(*[b.animate.restore() for b in bars[:1]], FadeIn(vl[0]), run_time=1.0)
        self.at("it falls with every")
        self.play(Succession(*[AnimationGroup(bars[i].animate.restore(), FadeIn(vl[i])) for i in (1, 2, 3)], lag_ratio=1.0), run_time=3.6)
        self.at("never reaches zero")
        sl = VGroup(*[Rectangle(width=1.7, height=0.08, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, base + 0.04, 0]) for x in xs])
        nz = T("never zero", 34, YELLOW, weight=BOLD).move_to([3.9, 1.4, 0])
        self.play(FadeIn(sl), FadeIn(nz), run_time=0.9)
        self.play(Indicate(sl, color=YELLOW, scale_factor=1.15), run_time=1.4)
        self.finish()


def equation_group(prior_part=True):
    lhs = T("P(occupied | all negative) =", 30, TEXT).move_to([3.7, 2.9, 0])
    num = T("prior × m", 38, TEAL, weight=BOLD).move_to([3.7, 1.6, 0])
    fbar = Line([1.0, 0.95, 0], [6.4, 0.95, 0], color=TEXT, stroke_width=4)
    d1 = T("(1 − prior)", 38, GREY, weight=BOLD)
    pl = T("+", 38, TEXT)
    d2 = T("prior × m", 38, TEAL, weight=BOLD)
    den = VGroup(d1, pl, d2).arrange(RIGHT, buff=0.22).move_to([3.7, 0.3, 0])
    return lhs, num, fbar, den


class S10Equation(PondScene):
    def construct(self):
        ambient(self)
        g = self.grid(removed=set(D1), hidden=self.hidden_after(1))
        self.add(g)
        lhs, num, fbar, den = equation_group()
        self.at("the equation")
        self.play(FadeIn(lhs), Create(fbar), run_time=1.0)
        self.at("on top sit")
        hid = [self.pd[i] for i in self.hidden_after(1)]
        cps = VGroup(*[p.copy() for p in hid[:5]])
        for c in cps:
            c.clear_updaters()
        self.play(*[Indicate(p, color=TEAL, scale_factor=1.6) for p in hid], run_time=1.0)
        self.add(cps)
        tgts = [np.array([2.5 + j * 0.5, 1.6, 0]) for j in range(5)]
        self.play(*[c.animate.move_to(t) for c, t in zip(cps, tgts)], run_time=1.6)
        self.at("the prior times")
        self.play(FadeOut(cps), FadeIn(num), run_time=0.9)
        mt = T("m = chance an occupied pond\nmisses on every sample", 28, YELLOW).move_to([3.7, -1.3, 0])
        self.at("misses every time")
        self.play(FadeIn(mt), run_time=0.8)
        self.at("below sit")
        greys = [p for p in g if p.kind == "empty"][:6]
        gcp = VGroup(*[p.copy() for p in greys])
        self.add(gcp)
        self.play(*[c.animate.move_to([1.6 + j * 0.28, 0.3, 0]) for j, c in enumerate(gcp)], run_time=1.6)
        self.at("the empty ones")
        self.play(FadeOut(gcp), FadeIn(den[0]), run_time=0.7)
        self.at("plus those hidden")
        hcp = VGroup(*[p.copy() for p in hid[:4]])
        self.add(hcp)
        self.play(*[c.animate.move_to([4.4 + j * 0.4, 0.3, 0]) for j, c in enumerate(hcp)], FadeIn(den[1]), run_time=0.9)
        self.play(FadeOut(hcp), FadeIn(den[2]), run_time=0.5)
        self.finish()


class S11Choices(SpokenScene):
    def construct(self):
        ambient(self)
        lhs, num, fbar, den = equation_group()
        mt = T("m = chance an occupied pond\nmisses on every sample", 28, YELLOW).move_to([3.7, -1.3, 0])
        self.add(lhs, num, fbar, den, mt)
        self.at("set by us")
        tagt = T("set by us, not measured", 34, TEAL, weight=BOLD).move_to([-3.4, 3.2, 0])
        self.play(FadeIn(tagt, shift=DOWN * 0.2), run_time=0.8)
        self.at("one is the prior")
        prior = ValueTracker(20.0)
        stop = ValueTracker(5.0)
        x0, x1 = -6.2, -0.6

        def kx(v):
            return x0 + (x1 - x0) * v / 100

        def slider(y, label, tr, col):
            track = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=6)
            knob = Dot(radius=0.24, color=col)
            knob.add_updater(lambda m: m.move_to([kx(tr.get_value()), y, 0]))
            val = M("20%", 32, col, weight=BOLD)
            val.add_updater(lambda m: m.become(M(f"{tr.get_value():.0f}%", 32, col, weight=BOLD).move_to([kx(tr.get_value()), y + 0.55, 0])))
            lab = T(label, 34, col, weight=BOLD).move_to([-3.4, y + 1.1, 0])
            return VGroup(lab, track), VGroup(knob, val)
        s1, d1 = slider(1.4, "prior", prior, TEAL)
        s2, d2 = slider(-0.5, "stop line", stop, RED)
        self.play(FadeIn(s1), Indicate(num, color=TEAL, scale_factor=1.1), run_time=1.2)
        self.add(d1)
        self.at("the stop line")
        self.play(FadeIn(s2), run_time=1.0)
        self.add(d2)
        self.at("change either")
        need = ValueTracker(0)

        def nneed():
            n = 0
            while pct_after(prior.get_value() / 100, n) > stop.get_value() and n < 20:
                n += 1
            return n
        ro = VGroup(T("samples needed", 30, TEXT), M("3", 56, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([-3.4, -2.5, 0])
        ro.add_updater(lambda m: m.become(VGroup(T("samples needed", 30, TEXT), M(str(nneed()), 56, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([-3.4, -2.5, 0])))
        cmp_ = T("computed, with q = 0.5", 24, GREY).move_to([-3.4, -3.65, 0])
        self.add(ro)
        self.play(FadeIn(cmp_), run_time=0.6)
        self.play(prior.animate.set_value(35.0), run_time=1.0)
        self.play(prior.animate.set_value(20.0), run_time=0.6)
        self.at("and the samples")
        self.play(stop.animate.set_value(2.0), run_time=1.4)
        self.finish()


class S12Scope(SpokenScene):
    def construct(self):
        ambient(self)
        lhs, num, fbar, den = equation_group()
        self.add(lhs, num, fbar, den)
        items = [("no false positives", "The count also assumes no false positives."[:0] or "no false positives", 1.8),
                 ("occupancy stays fixed\nduring the survey", "", 0.0),
                 ("each sample is\nindependent", "", -1.8)]
        rows = []
        for txt, _, y in items:
            box = Square(side_length=0.55, stroke_color=TEXT, stroke_width=3).move_to([-6.0, y, 0])
            tx = T(txt, 32, TEXT).next_to(box, RIGHT, buff=0.35)
            tx.align_to(box, LEFT).shift(RIGHT * 0.9)
            tick = VGroup(Line([-6.2, y, 0], [-6.05, y - 0.2, 0]), Line([-6.05, y - 0.2, 0], [-5.75, y + 0.25, 0])).set_stroke(GREEN, 8)
            rows.append((box, tx, tick))
        self.at("no false positives")
        self.play(FadeIn(rows[0][0]), FadeIn(rows[0][1], shift=RIGHT * 0.2), run_time=0.8)
        self.play(Create(rows[0][2]), run_time=0.6)
        self.at("each pond stays")
        self.play(FadeIn(rows[1][0]), FadeIn(rows[1][1], shift=RIGHT * 0.2), run_time=0.8)
        self.play(Create(rows[1][2]), run_time=0.6)
        self.at("and each sample")
        self.play(FadeIn(rows[2][0]), FadeIn(rows[2][1], shift=RIGHT * 0.2), run_time=0.8)
        self.play(Create(rows[2][2]), run_time=0.6)
        self.play(Indicate(VGroup(*[r[1] for r in rows]), color=YELLOW, scale_factor=1.05), run_time=1.5)
        self.finish()


class S13Rule(PondScene):
    def construct(self):
        ambient(self)
        g = self.grid(occ=set(ORDER))
        for p in g:
            if p.kind == "occ":
                p.set_fill(TEAL, 0.3)
                p.kind = "hidden"
        self.add(g)
        self.at("so a negative never")
        t0 = T("hidden occupied: 20", 30, TEAL, weight=BOLD).move_to([3.7, 3.05, 0])
        self.play(Indicate(g, color=TEAL, scale_factor=1.03), FadeIn(t0), run_time=1.2)
        self.at("each negative sample")
        vals = [pct_after(0.2, n) for n in range(4)]
        xs = [1.3, 2.7, 4.1, 5.5]
        base, k = -2.6, 0.14
        axis = Line([0.6, base, 0], [6.4, base, 0], color=GREY, stroke_width=3)
        bars = VGroup(*[Rectangle(width=1.0, height=v * k, stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.9)
                        .move_to([x, base + v * k / 2, 0]) for v, x in zip(vals, xs)])
        xt = T("independent negative samples", 26, TEXT).move_to([3.5, base - 0.5, 0])
        rl = DashedLine([0.6, base + 5 * k, 0], [6.4, base + 5 * k, 0], color=RED, stroke_width=4)
        self.play(FadeIn(axis), FadeIn(xt), FadeIn(rl), FadeIn(bars[0]), run_time=1.0)
        groups = [D1, D2, D3]
        labs = ["× ½", "× ½", "× ½"]
        cues = ["negative sample", "multiplies the hidden", "by the missed"]
        hidden_ps = [[self.pd[i] for i in grp] for grp in (D1, D2, D3)]
        for j in range(3):
            self.play(*[FadeOut(p, scale=0.4) for p in hidden_ps[j]], FadeIn(bars[j + 1]), run_time=1.0)
            self.wait(0.4)
        self.at("the empty")
        greys = [p for p in g if p.kind == "empty"]
        t1 = T("empty: 80, unchanged", 30, GREY, weight=BOLD).move_to([3.7, 1.7, 0])
        self.play(FadeIn(t1), LaggedStart(*[Indicate(p, color=TEXT, scale_factor=1.25) for p in greys], lag_ratio=0.02), run_time=2.0)
        self.at("every test you run")
        self.play(FadeOut(VGroup(axis, xt, rl, bars, t0, t1)), run_time=0.8)
        wells = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.5, height=0.5, stroke_color=GOLD, stroke_width=3,
                                          fill_color=GOLD, fill_opacity=0.2) for _ in range(20)]).arrange_in_grid(4, 5, buff=0.16).move_to([3.7, -1.0, 0])
        bt = bottle(color=BLUE, s=1.9).move_to([3.7, 2.2, 0])
        qm = T("?", 90, YELLOW, weight=BOLD).move_to([6.2, 2.2, 0])
        self.play(FadeIn(bt, shift=DOWN * 0.2), LaggedStart(*[FadeIn(w) for w in wells], lag_ratio=0.04), run_time=1.5)
        self.play(FadeIn(qm, scale=0.6), run_time=0.5)
        self.play(wells.animate.scale(1.04), run_time=0.8, rate_func=there_and_back)
        self.finish()


class S14End(EndCard):
    LINE = "Each negative sample multiplies the hidden ponds by the miss chance."
