"""Animal reproduction, film 2: Pulses, Not Amount (the Knobil pump experiment).

Same COLOUR MAP and boxes as film 1 (imported from ../scenes.py): GnRH GOLD; LH BLUE; FSH GREEN;
hypothalamus / pituitary = stacked rounded boxes in the same place. Everything schematic is labelled so.
"""
import importlib.util
import math
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

_spec = importlib.util.spec_from_file_location("ar_ch1", str(Path(__file__).resolve().parent.parent / "scenes.py"))
_ch1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ch1)
WS = _ch1.WS
HX, BW, BH, HY, PY = _ch1.HX, _ch1.BW, _ch1.BH, _ch1.HY, _ch1.PY
TAN, PINK, BLOOD = _ch1.TAN, _ch1.PINK, _ch1.BLOOD

# right-hand panel (narrow world)
NX0, NX1 = 2.9, 6.6
N_SY0, N_SY1 = 2.0, 3.0
N_PY0, N_PY1 = -2.55, 1.3
# side bars under the pituitary
BAR_BASE, BAR_MAX = -3.05, 1.6
BAR_X = (HX - 1.0, HX + 1.0)
P_PULSE, P_STEADY = 0.62, 0.82      # schematic totals per day; steady >= pulses
BLOODC = "#FF8A80"


# ------------------------------------------------------------------ schematic LH / FSH model
def _lh_base(d):
    if d < 1.5:
        return 0.04
    if d < 4.5:
        return 0.04 + 0.56 * (1 - math.exp(-(d - 1.5) / 0.5))
    vA = 0.04 + 0.56 * (1 - math.exp(-3.0 / 0.5))
    if d < 7.5:
        return 0.08 + (vA - 0.08) * math.exp(-(d - 4.5) / 0.9)
    v0 = 0.08 + (vA - 0.08) * math.exp(-3.0 / 0.9)
    return v0 + (0.60 - v0) * (1 - math.exp(-(d - 7.5) / 0.5))


def lh_val(d, cyc):
    v = _lh_base(d)
    if (1.5 <= d < 4.5) or d >= 7.5:
        v += 0.05 * max(0.0, math.sin(2 * math.pi * d * cyc)) ** 2
    return v


def fsh_val(d):
    return 0.85 * _lh_base(d)


def monkey(scale=1.0):
    """A small rhesus-monkey face cartoon."""
    fur = "#A47C4F"
    head = Circle(radius=1.0, stroke_color=fur, stroke_width=5, fill_color=fur, fill_opacity=0.75)
    ears = VGroup(*[Circle(radius=0.38, stroke_color=fur, stroke_width=5, fill_color=fur, fill_opacity=0.75).move_to([sx * 1.05, 0.2, 0]) for sx in (-1, 1)])
    inner = VGroup(*[Circle(radius=0.2, stroke_width=0, fill_color=PINK, fill_opacity=0.7).move_to([sx * 1.05, 0.2, 0]) for sx in (-1, 1)])
    face = Ellipse(width=1.45, height=1.25, stroke_width=0, fill_color="#E3C9A2", fill_opacity=0.95).move_to([0, -0.18, 0])
    eyes = VGroup(*[Dot(radius=0.08, color=BG).move_to([sx * 0.33, 0.2, 0]) for sx in (-1, 1)])
    nose = VGroup(*[Dot(radius=0.04, color=BG).move_to([sx * 0.08, -0.12, 0]) for sx in (-1, 1)])
    smile = Arc(radius=0.34, start_angle=-2.5, angle=1.85, stroke_color=BG, stroke_width=4).move_to([0, -0.4, 0])
    g = VGroup(ears, inner, head, face, eyes, nose, smile)
    return g.scale(scale)


def tick_mark(center, size=0.4, color=GREEN):
    c = np.array(list(center) + [0])[:3].astype(float)
    return VGroup(Line(c + [-size * 0.6, 0, 0], c + [-size * 0.15, -size * 0.5, 0], color=color, stroke_width=9),
                  Line(c + [-size * 0.15, -size * 0.5, 0], c + [size * 0.7, size * 0.6, 0], color=color, stroke_width=9))


def cross_mark(center, w, h, color=RED):
    c = np.array(list(center) + [0])[:3].astype(float)
    return VGroup(Line(c + [-w / 2, h / 2, 0], c + [w / 2, -h / 2, 0], color=color, stroke_width=8),
                  Line(c + [-w / 2, -h / 2, 0], c + [w / 2, h / 2, 0], color=color, stroke_width=8))


class W2(WS):
    """The carried world of film 2: pump over pituitary at left; GnRH-in strip, LH plot and totals at right."""

    def setup(self):
        super().setup()
        self.rin = ValueTracker(0.0)    # days of GnRH delivery drawn
        self.rlh = ValueTracker(0.0)    # days of LH / FSH record drawn
        self.gp = ValueTracker(0.0)     # gate: pulse dots
        self.gs = ValueTracker(0.0)     # gate: steady dots
        self.hp = ValueTracker(0.0)     # side bar heights (fraction of schematic maximum)
        self.hs = ValueTracker(0.0)
        self.add(self.rin, self.rlh, self.gp, self.gs, self.hp, self.hs)
        import random
        rng = random.Random(type(self).__name__)
        motes = VGroup()
        for _ in range(34):
            d = Dot(radius=rng.uniform(0.04, 0.08), color=rng.choice([GOLD, BLUE, TEXT])).set_opacity(rng.uniform(0.22, 0.4))
            d.move_to([rng.uniform(-6.9, 6.9), rng.uniform(-3.9, 3.9), 0])
            d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.15, 0.4))

            def drift(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 4.0:
                    m.shift(DOWN * 8.0)
                if abs(m.get_x()) > 7.0:
                    m.shift(LEFT * 14.0 * np.sign(m.get_x()))
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)

    # ---- left column
    def pit_box(self):
        self.pit = self.mkbox("pituitary", PY)
        self.pit_rect = self.pit[0]
        self.add(self.pit)
        return self.pit

    def hyp_crossed(self):
        hyp = self.mkbox("hypothalamus", HY)
        x = cross_mark([HX, HY - 0.3], BW - 0.6, 0.5)
        g = VGroup(hyp, x)
        self.add(g)
        return g

    def pump(self):
        body = RoundedRectangle(corner_radius=0.18, width=2.7, height=1.2, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.35).move_to([HX - 0.2, HY, 0])
        shaft = Line([HX + 1.15, HY, 0], [HX + 1.75, HY, 0], color=GREY, stroke_width=6)
        handle = Line([HX + 1.75, HY - 0.35, 0], [HX + 1.75, HY + 0.35, 0], color=GREY, stroke_width=8)
        nozzle = Rectangle(width=0.28, height=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([HX, HY - 0.7, 0])
        lab = T("pump", 28, TEXT).move_to([HX - 0.2, HY, 0])
        return VGroup(body, shaft, handle, nozzle, lab)

    def gold_tube(self, top=HY - 0.8, bot=PY + BH / 2):
        return Line([HX, top, 0], [HX, bot, 0], color=GOLD, stroke_width=6, stroke_opacity=0.45)

    def stream(self, x=HX, ytop=HY - 0.8, ybot=PY + BH / 2, pit=True, gp=None, gs=None, t0=None):
        """GnRH dots: pulsed bursts (gate gp) or a steady stream (gate gs). Also lights the pituitary fill."""
        gp = gp or self.gp
        gs = gs or self.gs
        t0 = self.now() if t0 is None else t0
        P = 3.0
        pd = VGroup(*[Dot(radius=0.14, color=GOLD) for _ in range(3)])
        sd = VGroup(*[Dot(radius=0.11, color=GOLD) for _ in range(8)])
        span = ytop - ybot

        def upd_p(m):
            s0 = (self.now() - t0) % P
            for i, d in enumerate(m):
                s = s0 - i * 0.3
                if 0 <= s < 1.0:
                    d.set_opacity(gp.get_value())
                    d.move_to([x, ytop - span * s, 0])
                else:
                    d.set_opacity(0)

        def upd_s(m):
            for i, d in enumerate(m):
                u = ((self.now() - t0) / 1.8 + i / 8) % 1
                d.move_to([x, ytop - span * u, 0])
                d.set_opacity(gs.get_value() * min(1, u * 8, (1 - u) * 8))
        pd.add_updater(upd_p)
        sd.add_updater(upd_s)
        self.add(pd, sd)
        if pit and hasattr(self, "pit_rect"):
            def glow(m):
                u = (self.now() - t0 - 0.9) % P
                e = math.exp(-u / 0.8)
                m.set_fill(GOLD, opacity=0.14 + 0.5 * e * gp.get_value() + 0.28 * gs.get_value())
            self.pit_rect.add_updater(glow)
        return VGroup(pd, sd)

    def sidebars(self, heading=True):
        g = VGroup()
        for x, tr, name in [(BAR_X[0], self.hp, "pulses"), (BAR_X[1], self.hs, "steady")]:
            frame = Rectangle(width=0.9, height=BAR_MAX, stroke_color=GOLD, stroke_width=3).move_to([x, BAR_BASE + BAR_MAX / 2, 0])
            fill = Rectangle(width=0.82, height=0.05, stroke_width=0, fill_color=GOLD, fill_opacity=0.85)

            def upd(m, tr=tr, x=x):
                h = max(0.03, BAR_MAX * tr.get_value())
                m.stretch_to_fit_height(h)
                m.move_to([x, BAR_BASE + h / 2, 0])
            fill.add_updater(upd)
            g.add(frame, fill, T(name, 26, GOLD).move_to([x, BAR_BASE - 0.35, 0]))
        if heading:
            h = T("GnRH per day (schematic)", 26, TEXT)
            fit(h, max_w=4.1)
            g.add(h.move_to([HX, -1.05, 0]))
        self.add(g)
        self.bars_g = g
        return g

    # ---- right panel (narrow or wide)
    def panel(self, x0=NX0, x1=NX1, sy0=N_SY0, sy1=N_SY1, py0=N_PY0, py1=N_PY1, cyc=2.0, fsh=True):
        rin, rlh = self.rin, self.rlh
        W = x1 - x0
        X = lambda d: x0 + W * d / 10.0
        sbox = Rectangle(width=W, height=sy1 - sy0, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([(x0 + x1) / 2, (sy0 + sy1) / 2, 0])
        pbox = Rectangle(width=W, height=py1 - py0, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([(x0 + x1) / 2, (py0 + py1) / 2, 0])
        marks = VGroup()
        sh = sy1 - sy0
        bw = max(0.05, W * 0.3 / (10 * cyc))
        for a, b in ((1.5, 4.5), (7.5, 10.0)):
            n = int(round((b - a) * cyc))
            for i in range(n):
                d = a + i / cyc
                r = Rectangle(width=bw, height=sh * 0.82, stroke_width=0, fill_color=GOLD, fill_opacity=0.95)
                r.move_to([X(d) + bw / 2 + 0.03, sy0 + 0.06 + sh * 0.41, 0])
                r.d0 = d
                r.op = 0.95
                marks.add(r)
        ns = 24
        for i in range(ns):
            d = 4.5 + 3.0 * i / ns
            r = Rectangle(width=W * 3.0 / 10 / ns + 0.004, height=sh * 0.55, stroke_width=0, fill_color=GOLD, fill_opacity=0.8)
            r.move_to([X(d) + (W * 3.0 / 10 / ns) / 2, sy0 + 0.06 + sh * 0.275, 0])
            r.d0 = d
            r.op = 0.8
            marks.add(r)

        def upd_marks(m):
            v = rin.get_value()
            for r in m:
                r.set_fill(opacity=r.op if r.d0 <= v else 0.0)
        marks.add_updater(upd_marks)
        ph = py1 - py0

        def Y(v):
            return py0 + 0.1 + (ph - 0.2) * v

        lh_tr = VMobject(stroke_color=BLUE, stroke_width=6)
        fs_tr = VMobject(stroke_color=GREEN, stroke_width=5)

        def upd_lh(m):
            r = max(0.02, rlh.get_value())
            ds = np.append(np.arange(0, r, 0.03), r)
            m.set_points_as_corners([[X(d), Y(lh_val(d, cyc)), 0] for d in ds])

        def upd_fs(m):
            r = max(0.02, rlh.get_value())
            ds = np.append(np.arange(0, r, 0.06), r)
            pts = [[X(d), Y(fsh_val(d)), 0] for d in ds]
            m.clear_points()
            for k in range(0, len(pts) - 1, 2):
                m.start_new_path(np.array(pts[k]))
                m.add_line_to(np.array(pts[k + 1]))
        lh_tr.add_updater(upd_lh)
        fs_tr.add_updater(upd_fs)
        g = VGroup(sbox, marks, pbox, lh_tr)
        if fsh:
            g.add(fs_tr)
        self.add(g)
        self.X, self.Y = X, Y
        self.pan = dict(sbox=sbox, pbox=pbox, marks=marks, lh=lh_tr, fs=fs_tr, x0=x0, x1=x1, sy0=sy0, sy1=sy1, py0=py0, py1=py1)
        return g

    def panel_labels(self, gn=True, lh=True):
        p = self.pan
        out = VGroup()
        if gn:
            out.add(T("GnRH given", 28, GOLD, weight=BOLD).move_to([(p["x0"] + p["x1"]) / 2, p["sy1"] + 0.42, 0]))
        if lh:
            out.add(T("LH (schematic)", 26, BLUE, weight=BOLD).move_to([p["x0"] + 1.5, p["py1"] - 0.3, 0]))
        self.add(out)
        return out

    def days_label(self):
        p = self.pan
        lab = T("days", 26, TEXT).move_to([(p["x0"] + p["x1"]) / 2, p["py0"] - 0.3, 0])
        self.add(lab)
        return lab

    def stream_panel(self, x, ytop, ybot, steady, w=3.6):
        """A GnRH stream into a pituitary box (opening scene)."""
        gp = ValueTracker(0.0 if steady else 1.0)
        gs = ValueTracker(1.0 if steady else 0.0)
        self.add(gp, gs)
        box = RoundedRectangle(corner_radius=0.2, width=w, height=1.9, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to([x, ybot - 0.95, 0])
        t = T("pituitary", 28, TEXT).move_to([x, ybot - 0.4, 0])
        line = Line([x, ytop, 0], [x, ybot, 0], color=GOLD, stroke_width=4, stroke_opacity=0.3)
        return box, t, line, gp, gs


# ---------------------------------------------------------------------------
class S00Title(TitleCard):
    TITLE = "Pulses, Not Amount"
    LESSON = "Animal Reproduction"


# ---------------------------------------------------------------------------
class S01Question(W2):
    def construct(self):
        ytop, ybot = 3.0, -0.4
        xs = (-3.4, 3.4)
        parts = [self.stream_panel(x, ytop, ybot, steady) for x, steady in zip(xs, (True, False))]
        self.at("Same hormone")
        panels = VGroup()
        for box, t, line, gp, gs in parts:
            panels.add(box, t, line)
        self.play(FadeIn(panels), run_time=1.0)
        streams = VGroup()
        for (box, t, line, gp, gs), x in zip(parts, xs):
            streams.add(self.stream(x=x, ytop=ytop, ybot=ybot, pit=False, gp=gp, gs=gs))
        self.at("Could the timing")
        l1 = T("steady", 34, GOLD, weight=BOLD).move_to([xs[0], 3.45, 0])
        l2 = T("bursts", 34, GOLD, weight=BOLD).move_to([xs[1], 3.45, 0])
        self.play(FadeIn(l1, shift=DOWN * 0.1), FadeIn(l2, shift=DOWN * 0.1), run_time=0.8)
        self.at("as much as its amount")
        qs = VGroup(*[T("?", 80, TEXT, weight=BOLD).move_to([x, ybot - 1.25, 0]) for x in xs])
        self.play(FadeIn(qs, scale=1.4), run_time=0.8)
        qs.add_updater(lambda m: [q.set_y(ybot - 1.25 + 0.06 * math.sin(2.2 * self.now() + i)) for i, q in enumerate(m)])
        self.at("The first film showed")
        keep = VGroup(panels, l1, l2, qs)
        self.play(keep.animate.set_opacity(0.3), run_time=0.7)
        ih = RoundedRectangle(corner_radius=0.15, width=2.6, height=0.85, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([0, 2.3, 0])
        ip = RoundedRectangle(corner_radius=0.15, width=2.6, height=0.85, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([0, -0.3, 0])
        ih_t = T("hypothalamus", 22, TEXT).move_to(ih)
        ip_t = T("pituitary", 22, TEXT).move_to(ip)
        tube = Line([0, 1.88, 0], [0, 0.13, 0], color=GREY, stroke_width=4)
        ig = VGroup(ih, ip, tube, ih_t, ip_t)
        self.play(FadeIn(ig), run_time=0.8)
        gpi, gsi = ValueTracker(1.0), ValueTracker(0.0)
        self.add(gpi, gsi)
        idots = self.stream(x=0, ytop=1.88, ybot=0.13, pit=False, gp=gpi, gs=gsi)
        self.at("reaching")
        gl = T("GnRH", 28, GOLD, weight=BOLD).move_to([0, 1.0, 0])
        self.play(FadeIn(gl), run_time=0.5)
        self.at("This film asks")
        self.play(FadeOut(ig), FadeOut(idots), FadeOut(gl), keep.animate.set_opacity(1.0), run_time=0.9)
        self.play(Indicate(qs, color=GOLD, scale_factor=1.25), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------
class S02Setup(W2):
    def construct(self):
        self.at("Ernst")
        mk = monkey(1.5)
        mk.move_to([0, 0.5, 0])
        self.play(FadeIn(mk, shift=UP * 0.2), run_time=1.0)
        self.at("laboratory")
        yr = T("1978", 44, GOLD, weight=BOLD).move_to([-5.5, 3.2, 0])
        self.play(FadeIn(yr), run_time=0.6)
        self.at("rhesus monkeys")
        ml = T("rhesus monkey", 30, TEXT).next_to(mk, DOWN, buff=0.3)
        self.play(FadeIn(ml, shift=UP * 0.1), run_time=0.5)
        self.at("Damage to the hypothalamus")
        corner = monkey(0.55).move_to([-5.75, -2.7, 0])
        ml2 = T("rhesus monkey", 24, TEXT).move_to([-5.45, -3.5, 0])
        self.play(Transform(mk, corner), FadeOut(ml), run_time=0.9)
        self.add(ml2)
        hyp = self.mkbox("hypothalamus", HY)
        tubeL = Line([HX, HY - BH / 2, 0], [HX, PY + BH / 2, 0], color=GREY, stroke_width=6)
        pit = self.pit_box()
        self.remove(pit)
        self.play(FadeIn(hyp, shift=DOWN * 0.3), FadeIn(pit, shift=UP * 0.3), FadeIn(tubeL), run_time=0.9)
        self.at("called a lesion")
        x = cross_mark([HX, HY - 0.3], BW - 0.6, 0.5)
        ll = T("hypothalamic lesion", 30, RED, weight=BOLD).move_to([4.4, HY, 0])
        self.play(Create(x), FadeIn(ll, shift=LEFT * 0.2), hyp[0].animate.set_fill(RED, opacity=0.12), run_time=1.0)
        gap = VGroup(Line([HX, HY - BH / 2, 0], [HX, 1.6, 0], color=GREY, stroke_width=6),
                     Line([HX, 1.2, 0], [HX, PY + BH / 2, 0], color=GREY, stroke_width=6))
        self.play(FadeOut(tubeL), FadeIn(gap), run_time=0.6)
        self.at("stopped their LH")
        fr = []
        for xx, col, nm in ((3.5, BLUE, "LH"), (5.4, GREEN, "FSH")):
            frame = Rectangle(width=0.7, height=1.5, stroke_color=col, stroke_width=3).move_to([xx, PY - 0.1, 0])
            lab = T(nm, 28, col, weight=BOLD).move_to([xx, PY - 1.15, 0])
            fr.append(VGroup(frame, lab))
        self.play(FadeIn(fr[0]), FadeIn(fr[1]), run_time=0.6)
        self.at("But the pituitary")
        pl = T("pituitary intact", 30, TEXT, weight=BOLD).move_to([HX, -1.05, 0])
        self.play(self.pit_rect.animate.set_stroke(GREEN, 6), FadeIn(pl, shift=UP * 0.1), run_time=0.9)
        self.play(Indicate(self.pit_rect, color=GREEN, scale_factor=1.04), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------
class S03Design(W2):
    def construct(self):
        cx = (-4.5, 0.0, 4.5)
        titles = ["remove the\nsource", "give it back\nfrom outside", "compare delivery\npatterns"]
        ts = [T(t, 30, TEXT, weight=BOLD, line_spacing=0.8).move_to([x, 3.0, 0]) for x, t in zip(cx, titles)]
        self.at("Remove the animal's own source")
        hyp = self.mkbox("hypothalamus", 0.8)
        hyp[0].stretch_to_fit_width(3.6).move_to([cx[0], 0.8, 0])
        hyp[1].move_to([cx[0], 1.2, 0])
        x1 = cross_mark([cx[0], 0.5, 0], 3.0, 0.5)
        self.play(FadeIn(ts[0]), FadeIn(hyp), run_time=0.8)
        self.play(Create(x1), hyp[0].animate.set_fill(RED, opacity=0.12), run_time=0.7)
        self.at("Then give it back")
        pump = self.pump().scale(0.9).move_to([cx[1], 0.8, 0])
        tube = Line([cx[1], 0.25, 0], [cx[1], -1.3, 0], color=GOLD, stroke_width=6, stroke_opacity=0.45)
        self.play(FadeIn(ts[1]), FadeIn(pump), run_time=0.8)
        self.play(Create(tube), run_time=0.6)
        gp1, gs1 = ValueTracker(1.0), ValueTracker(0.0)
        self.add(gp1, gs1)
        self.stream(x=cx[1], ytop=0.25, ybot=-1.3, pit=False, gp=gp1, gs=gs1)
        pit_s = RoundedRectangle(corner_radius=0.2, width=3.0, height=1.1, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.14).move_to([cx[1], -1.85, 0])
        pit_t = T("pituitary", 26, TEXT).move_to(pit_s)
        self.play(FadeIn(pit_s), FadeIn(pit_t), run_time=0.4)
        self.at("different schedules")
        self.play(FadeIn(ts[2]), run_time=0.7)
        W = 3.6
        x0 = cx[2] - W / 2
        train = VGroup(*[Rectangle(width=0.12, height=0.7, stroke_width=0, fill_color=GOLD, fill_opacity=0.95) for _ in range(9)])
        steady = Rectangle(width=W, height=0.45, stroke_width=0, fill_color=GOLD, fill_opacity=0.8).move_to([cx[2], 0.35, 0])
        rowtop = Rectangle(width=W, height=0.8, stroke_color=GREY, stroke_width=2).move_to([cx[2], 1.55, 0])
        rowbot = Rectangle(width=W, height=0.8, stroke_color=GREY, stroke_width=2).move_to([cx[2], 0.35, 0])
        t0 = self.now()

        def utrain(m):
            for i, r in enumerate(m):
                u = ((self.now() - t0) * 0.35 + i / 9) % 1
                r.move_to([x0 + 0.1 + (W - 0.2) * u, 1.55, 0])
        train.add_updater(utrain)
        self.play(Create(rowtop), Create(rowbot), run_time=0.5)
        self.add(train)
        self.play(FadeIn(steady), run_time=0.5)
        self.at("with the steady one")
        hdr = T("total per day (schematic)", 26, TEXT)
        fit(hdr, max_w=3.9)
        hdr.move_to([cx[2], -0.62, 0])
        base = -2.6
        bh1, bh2 = 1.3 * P_PULSE, 1.3 * P_STEADY
        b1 = Rectangle(width=0.8, height=bh1, stroke_width=0, fill_color=GOLD, fill_opacity=0.85).move_to([cx[2] - 0.9, base + bh1 / 2, 0])
        b2 = Rectangle(width=0.8, height=bh2, stroke_width=0, fill_color=GOLD, fill_opacity=0.85).move_to([cx[2] + 0.9, base + bh2 / 2, 0])
        l1 = T("pulses", 24, GOLD).move_to([cx[2] - 0.9, base - 0.3, 0])
        l2 = T("steady", 24, GOLD).move_to([cx[2] + 0.9, base - 0.3, 0])
        self.play(FadeIn(hdr), GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(l1), FadeIn(l2), run_time=1.3)
        self.at("at least as much")
        tag = T("steady: at least as much", 26, GOLD, weight=BOLD)
        fit(tag, max_w=4.0)
        tag.move_to([cx[2], -3.45, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), Indicate(b2, color=GOLD, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------
class S04Supply(W2):
    def construct(self):
        hc = self.hyp_crossed()
        hc[0][0].set_fill(RED, opacity=0.12)
        self.pit_box()
        tubeL = Line([HX, HY - BH / 2, 0], [HX, 1.6, 0], color=GREY, stroke_width=6)
        tubeL2 = Line([HX, 1.2, 0], [HX, PY + BH / 2, 0], color=GREY, stroke_width=6)
        self.add(tubeL, tubeL2)
        self.at("clean supply")
        vx, vy = -5.0, 0.9
        glass = RoundedRectangle(corner_radius=0.15, width=1.3, height=2.6, stroke_color=TEXT, stroke_width=5, fill_opacity=0).move_to([vx, vy, 0])
        cap = Rectangle(width=1.0, height=0.35, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.6).move_to([vx, vy + 1.45, 0])
        liq = Rectangle(width=1.14, height=1.9, stroke_width=0, fill_color=GOLD, fill_opacity=0.85).move_to([vx, vy - 0.25, 0])
        vial = VGroup(liq, glass, cap)
        vlab = T("synthetic GnRH", 28, GOLD, weight=BOLD).move_to([vx + 0.5, vy - 1.85, 0])
        self.play(FadeIn(glass), FadeIn(cap), run_time=0.7)
        self.play(GrowFromEdge(liq, DOWN), run_time=1.4)
        self.at("had just been isolated")
        self.play(FadeIn(vlab, shift=UP * 0.1), Indicate(liq, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.at("Pure synthetic")
        pump = self.pump()
        self.play(FadeOut(hc), FadeOut(vlab), FadeIn(pump, shift=DOWN * 0.2), run_time=1.0)
        self.play(vial.animate.scale(0.55).move_to([HX - 0.65, HY, 0]), run_time=1.0)
        self.play(FadeOut(vial), FadeOut(tubeL), FadeOut(tubeL2), run_time=0.5)
        self.at("made this kind")
        tube = self.gold_tube()
        self.play(Create(tube), run_time=0.5)
        self.gp.set_value(1.0)
        self.stream()
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------
def blood_ribbon(scene):
    rib = VMobject(stroke_color=BLOOD, stroke_width=10, stroke_opacity=0.6)
    rib.set_points_as_corners([[HX + BW / 2, PY, 0], [NX0, PY, 0]])
    scene.add(rib)
    scene.flow([[HX + BW / 2, PY, 0], [NX0, PY, 0]], 5, 2.5, [BLOOD], r=0.1)
    return rib


class S05Pump(W2):
    def construct(self):
        self.pit_box()
        self.add(self.pump())
        tube = self.gold_tube()
        self.add(tube)
        self.stream()
        self.gp.set_value(0.0)
        self.at("through a vein")
        vl = T("through a vein", 28, TEXT).move_to([1.7, 1.45, 0])
        self.play(FadeIn(vl, shift=LEFT * 0.1), Indicate(tube, color=GOLD), run_time=1.0)
        self.at("blood samples")
        rib = VMobject(stroke_color=BLOOD, stroke_width=10, stroke_opacity=0.6)
        rib.set_points_as_corners([[HX + BW / 2, PY, 0], [NX0, PY, 0]])
        self.add(rib)
        self.play(Create(rib), FadeOut(vl), run_time=0.8)
        self.flow([[HX + BW / 2, PY, 0], [NX0, PY, 0]], 5, 2.5, [BLOOD], r=0.1)
        bl = T("blood", 28, BLOODC).move_to([2.2, 0.65, 0])
        self.panel()
        self.play(FadeIn(bl), FadeIn(self.pan["pbox"]), run_time=0.9)
        self.add(self.panel_labels(gn=False), self.days_label())
        self.at("With no drive from above")
        self.add(self.panel_labels(gn=True, lh=False))
        self.sidebars()
        self.at("started flat")
        self.play(self.rlh.animate.set_value(1.5), run_time=3.2, rate_func=linear)
        self.finish()


def carry(scene, rin, rlh, gp, gs, hp, hs):
    scene.pit_box()
    scene.add(scene.pump())
    scene.add(scene.gold_tube())
    scene.rin.set_value(rin)
    scene.rlh.set_value(rlh)
    scene.gp.set_value(gp)
    scene.gs.set_value(gs)
    scene.hp.set_value(hp)
    scene.hs.set_value(hs)
    scene.stream()
    scene.panel()
    scene.panel_labels()
    scene.days_label()
    scene.sidebars()
    blood_ribbon(scene)
    scene.add(T("blood", 28, BLOODC).move_to([2.2, 0.65, 0]))


def arrows_set(scene):
    """The three 'what next?' arrows beyond the dashed line (rebuilt exactly)."""
    y0 = scene.Y(_lh_base(4.5))
    x0 = scene.X(4.5) + 0.12
    out = VGroup()
    for dy, lab, ly, lx in ((0.0, "stay up?", 0.0, 1.22), (0.7, "higher?", 0.7, 1.15), (-0.7, "fall?", -0.7, 1.15)):
        out.add(Arrow([x0, y0 + 0.1 * np.sign(dy), 0], [x0 + (0.4 if dy == 0 else 0.35), y0 + dy, 0], buff=0, color=BLUE, stroke_width=6, tip_length=0.2))
        out.add(T(lab, 24, TEXT, weight=BOLD).move_to([scene.X(4.5) + lx, y0 + ly, 0]))
    return out


class S06Pulses(W2):
    def construct(self):
        carry(self, 0.0, 1.5, 0.0, 0.0, 0.0, 0.0)
        self.at("brief infusions")
        self.gp.set_value(1.0)
        self.play(self.rin.animate.set_value(2.1), self.rlh.animate.set_value(2.1), run_time=1.2, rate_func=linear)
        self.at("once every hour")
        clk = Circle(radius=0.55, stroke_color=TEXT, stroke_width=5).move_to([-4.7, 0.9, 0])
        hand = Line([-4.7, 0.9, 0], [-4.7, 1.35, 0], color=GOLD, stroke_width=6)
        t0 = self.now()
        hand.add_updater(lambda m: m.become(Line([-4.7, 0.9, 0], [-4.7 + 0.42 * math.sin(2.1 * (self.now() - t0)), 0.9 + 0.42 * math.cos(2.1 * (self.now() - t0)), 0], color=GOLD, stroke_width=6)))
        cl = T("every hour", 28, TEXT, weight=BOLD).move_to([-4.7, 0.0, 0])
        self.play(FadeIn(clk), FadeIn(hand), FadeIn(cl), run_time=0.9)
        self.at("The pump gives a short burst")
        self.play(Indicate(self.pit_rect, color=GOLD, scale_factor=1.03), run_time=1.4)
        self.at("then stops")
        self.wait(1.5)
        self.at("Hourly pulses restored")
        self.play(self.rin.animate.set_value(4.5), self.rlh.animate.set_value(3.2), self.hp.animate.set_value(P_PULSE), run_time=2.5, rate_func=linear)
        self.at("FSH secretion")
        fl = T("FSH", 26, GREEN, weight=BOLD).move_to([NX0 + 0.6, N_PY1 - 0.75, 0])
        self.play(FadeIn(fl), self.rlh.animate.set_value(4.5), run_time=1.4, rate_func=linear)
        self.at("kept it going")
        self.play(Indicate(self.pan["lh"], color=BLUE), FadeOut(clk), FadeOut(hand), FadeOut(cl), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------
class S07Predict(W2):
    def construct(self):
        carry(self, 4.5, 4.5, 1.0, 0.0, P_PULSE, 0.0)
        self.add(T("FSH", 26, GREEN, weight=BOLD).move_to([NX0 + 0.6, N_PY1 - 0.75, 0]))
        self.at("steady stream")
        self.play(self.gp.animate.set_value(0.0), self.gs.animate.set_value(1.0), run_time=1.0)
        self.play(self.rin.animate.set_value(5.8), run_time=2.0, rate_func=linear)
        self.at("at least as much GnRH")
        dl = DashedLine([self.X(4.5), N_PY0, 0], [self.X(4.5), N_PY1 - 0.6, 0], color=TEXT, stroke_width=4)
        self.play(self.hs.animate.set_value(P_STEADY), self.rin.animate.set_value(7.5), Create(dl), run_time=3.0, rate_func=linear)
        arr = arrows_set(self)
        self.at("Will LH stay up")
        self.play(GrowArrow(arr[0]), FadeIn(arr[1]), run_time=0.8)
        self.at("rise higher")
        self.play(GrowArrow(arr[2]), FadeIn(arr[3]), run_time=0.8)
        self.at("fall away")
        self.play(GrowArrow(arr[4]), FadeIn(arr[5]), run_time=0.8)
        self.finish()


class S08Pause(W2):
    def construct(self):
        carry(self, 7.5, 4.5, 0.0, 1.0, P_PULSE, P_STEADY)
        self.add(T("FSH", 26, GREEN, weight=BOLD).move_to([NX0 + 0.6, N_PY1 - 0.75, 0]))
        self.add(DashedLine([self.X(4.5), N_PY0, 0], [self.X(4.5), N_PY1 - 0.6, 0], color=TEXT, stroke_width=4))
        self.add(arrows_set(self))
        ring_bg = Circle(radius=0.38, stroke_color=GREY, stroke_width=5).move_to([6.2, -3.35, 0])
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()) + 1e-3, stroke_color=GOLD, stroke_width=7).move_to([6.2, -3.35, 0]))
        self.add(ring_bg, ring)
        self.play(tr.animate.set_value(1.0), run_time=5.0, rate_func=linear)


# ---------------------------------------------------------------------------
class S09Reveal(W2):
    def construct(self):
        carry(self, 7.5, 4.5, 0.0, 1.0, P_PULSE, P_STEADY)
        self.add(T("FSH", 26, GREEN, weight=BOLD).move_to([NX0 + 0.6, N_PY1 - 0.75, 0]))
        self.add(DashedLine([self.X(4.5), N_PY0, 0], [self.X(4.5), N_PY1 - 0.6, 0], color=TEXT, stroke_width=4))
        old = arrows_set(self)
        self.add(old)
        self.at("It falls away")
        self.play(FadeOut(old), run_time=0.5)
        self.play(self.rlh.animate.set_value(6.5), run_time=3.0, rate_func=linear)
        self.at("did not sustain")
        ns = T("not\nsustained", 24, RED, weight=BOLD, line_spacing=0.8).move_to([5.6, 0.4, 0])
        self.play(FadeIn(ns), self.rlh.animate.set_value(7.5), run_time=2.5, rate_func=linear)
        note = T("schematic;\nnot the paper's data", 22, TEXT, line_spacing=0.8).move_to([4.75, -3.4, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("If the pituitary counted only the total")
        self.play(Indicate(self.bars_g, color=GOLD, scale_factor=1.04), run_time=1.5)
        self.at("the steady drip")
        self.wait(1.3)
        self.at("It did not")
        self.play(Indicate(ns, color=RED, scale_factor=1.15), Indicate(self.pan["lh"], color=BLUE), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------------------
class S10Back(W2):
    def construct(self):
        carry(self, 7.5, 7.5, 0.0, 1.0, P_PULSE, P_STEADY)
        self.add(T("FSH", 26, GREEN, weight=BOLD).move_to([NX0 + 0.6, N_PY1 - 0.75, 0]))
        self.at("went back to hourly pulses")
        self.play(self.gs.animate.set_value(0.0), self.gp.animate.set_value(1.0), run_time=1.0)
        self.play(self.rin.animate.set_value(8.7), self.rlh.animate.set_value(8.7), run_time=2.0, rate_func=linear)
        self.at("The authors reported")
        self.play(self.rin.animate.set_value(9.5), self.rlh.animate.set_value(9.5), run_time=3.0, rate_func=linear)
        self.at("so the pituitary had not")
        tk = tick_mark([HX + 1.7, PY + 0.4], 0.45, GREEN)
        sl = T("still able to respond", 26, GREEN, weight=BOLD).move_to([HX, PY - 0.3, 0])
        self.play(Create(tk), FadeIn(sl, shift=UP * 0.1), self.pit_rect.animate.set_stroke(GREEN, 6),
                  self.rin.animate.set_value(10), self.rlh.animate.set_value(10), run_time=1.6, rate_func=linear)
        self.at("It could still answer")
        self.play(Indicate(sl, color=GREEN, scale_factor=1.1), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------
class S11Readout(W2):
    def construct(self):
        self.panel(x0=-6.0, x1=6.2, sy0=1.95, sy1=3.05, py0=-2.2, py1=1.35, cyc=4.0)
        gl = T("GnRH", 30, GOLD, weight=BOLD).move_to([-6.0 + 0.9, 2.5, 0])
        ll = T("LH", 30, BLUE, weight=BOLD).move_to([-6.0 + 0.6, 0.95, 0])
        days = T("days", 26, TEXT).move_to([0.1, -2.5, 0])
        self.add(gl, ll, days)
        self.at("reads the timing")
        self.play(self.rin.animate.set_value(10), run_time=4.0, rate_func=linear)
        self.at("Hourly pulses keep it working")
        lab1 = T("pulses:\nLH up", 28, BLUE, weight=BOLD, line_spacing=0.8).move_to([self.X(3.0), -3.25, 0])
        self.play(self.rlh.animate.set_value(4.5), FadeIn(lab1), run_time=2.2, rate_func=linear)
        self.at("A steady supply")
        lab2 = T("steady:\nLH not sustained", 28, RED, weight=BOLD, line_spacing=0.8).move_to([self.X(6.0), -3.25, 0])
        self.play(self.rlh.animate.set_value(7.5), FadeIn(lab2), run_time=2.2, rate_func=linear)
        self.at("a larger one")
        lab3 = T("pulses again:\nLH up", 28, BLUE, weight=BOLD, line_spacing=0.8).move_to([self.X(8.75), -3.25, 0])
        self.play(self.rlh.animate.set_value(10), FadeIn(lab3), run_time=2.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------
class S12Limits(W2):
    def construct(self):
        self.at("has limits")
        card = RoundedRectangle(corner_radius=0.25, width=10.6, height=6.0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([0.9, 0.1, 0])
        self.play(FadeIn(card), run_time=0.9)
        mk = monkey(0.7).move_to([-5.6, -2.55, 0])
        ml = T("rhesus monkeys", 24, TEXT).move_to([-5.45, -3.5, 0])
        self.at("in these monkeys")
        self.play(FadeIn(mk), FadeIn(ml), run_time=0.8)
        rows = []
        qbs = []
        texts = ["where do pulses\ncome from?", "normal interval\nin people?", "why does steady\nfail?"]
        for y, t in zip((1.8, 0.1, -1.6), texts):
            q = T("?", 64, GREY, weight=BOLD).move_to([-2.9, y, 0])
            tx = T(t, 34, TEXT, weight=BOLD, line_spacing=0.8).move_to([1.4, y, 0])
            q.base_y = y
            qbs.append(q)
            rows.append(VGroup(q, tx))
        for i, q in enumerate(qbs):
            q.add_updater(lambda m, i=i: m.set_y(m.base_y + 0.07 * math.sin(2.0 * self.now() + i * 1.7)))
        self.at("where the pulses come from")
        self.play(FadeIn(rows[0], shift=LEFT * 0.3), run_time=0.9)
        self.at("what interval between pulses")
        self.play(FadeIn(rows[1], shift=LEFT * 0.3), run_time=0.9)
        self.at("why a steady supply fails")
        self.play(FadeIn(rows[2], shift=LEFT * 0.3), run_time=0.9)
        self.finish()


class S13End(EndCard):
    LINE = "The pituitary reads the timing of GnRH, not only its total."
