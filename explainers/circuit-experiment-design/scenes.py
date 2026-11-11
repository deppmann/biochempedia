"""What Did the Light Change? (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  YELLOW = light            GOLD = opsin-linked manipulation / remainder
  TEAL   = fluorophore or no opsin      BLUE = measured outcome
  RED    = unresolved alternative (light itself, passing axons, backward drive)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

LIGHT, OPSIN, FLUOR, OUT, ALT = YELLOW, GOLD, TEAL, BLUE, RED
C0 = np.array([-3.0, 0.0, 0.0])
AR = 3.2


def rot(v, a):
    return np.array([v[0] * np.cos(a) - v[1] * np.sin(a), v[0] * np.sin(a) + v[1] * np.cos(a), 0.0])


def lab(text, color=TEXT, size=28, **kw):
    return T(text, size=size, color=color, weight=BOLD, **kw)


def make_mouse(L=1.3, color=TEXT):
    body = Ellipse(width=0.58 * L, height=0.95 * L)
    head = Ellipse(width=0.42 * L, height=0.46 * L).move_to(UP * 0.56 * L)
    ears = VGroup(*[Circle(radius=0.11 * L).move_to([s * 0.2 * L, 0.72 * L, 0]) for s in (-1, 1)])
    for m in (body, head, ears):
        m.set_stroke(color, 3).set_fill(color, 0.22)
    tail = ArcBetweenPoints(np.array([0, -0.47 * L, 0]), np.array([0.18 * L, -1.05 * L, 0]), angle=0.9).set_stroke(color, 3)
    nose = Dot(np.array([0, 0.79 * L, 0]), radius=0.04 * L + 0.01, color=color)
    return VGroup(tail, body, ears, head, nose)


class Rig:
    """A mouse walking a left-turning circle (counter-clockwise)."""
    def __init__(self, center, radius, L=1.3, speed=0.9, th0=-PI / 2, color=TEXT):
        self.base = make_mouse(L, color)
        self.c = np.array(center, float)
        self.r, self.w, self.th, self.L = radius, speed, th0, L
        self.mob = self.base.copy()
        self._place()
        self.mob.add_updater(self._upd)

    def pos(self):
        return self.c + self.r * np.array([np.cos(self.th), np.sin(self.th), 0])

    def _place(self):
        self.mob.become(self.base.copy().rotate(self.th, about_point=ORIGIN).shift(self.pos()))

    def _upd(self, m, dt):
        self.th += self.w * dt
        self._place()

    def head(self, local=(-0.12, 0.62)):
        return self.pos() + rot(np.array([local[0] * self.L, local[1] * self.L, 0]), self.th)


def idle(m, phase=0.0, amp=0.15, w=1.2):
    st = {"t": phase, "a": amp * np.sin(w * phase)}

    def u(mm, dt):
        st["t"] += dt
        a = amp * np.sin(w * st["t"])
        mm.rotate(a - st["a"])
        st["a"] = a
    m.add_updater(u)
    return m


def make_arena():
    return Circle(radius=AR, stroke_color=GREY, stroke_width=5, fill_color=TEXT, fill_opacity=0.05).move_to(C0)


def make_beam(rig, src, spread=0.35):
    src = np.array(src, float)

    def build():
        h = rig.head()
        d = h - src
        d = d / np.linalg.norm(d)
        perp = np.array([-d[1], d[0], 0])
        op = 0.26 + 0.1 * np.sin(3 * rig.th)
        poly = Polygon(src, h + perp * spread, h - perp * spread, stroke_width=0, fill_color=LIGHT, fill_opacity=op)
        halo = Circle(radius=0.32, stroke_width=0, fill_color=LIGHT, fill_opacity=op + 0.15).move_to(h)
        return VGroup(poly, halo)
    g = build()
    g.add_updater(lambda m: m.become(build()))
    return g


def badge(text="NO OPSIN", color=FLUOR, size=30):
    return chip(text, color, size=size)


def meter(x, ybot, h, w, val, color=OUT, outline=TEXT):
    frame = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=outline, stroke_width=3,
                             fill_opacity=0).move_to([x, ybot + h / 2, 0])
    fill = Rectangle(width=w - 0.1, height=0.05, stroke_width=0, fill_color=color, fill_opacity=0.9)

    def upd(m):
        hh = max(float(val()) * (h - 0.1), 0.03)
        m.stretch_to_fit_height(hh)
        m.move_to([x, ybot + 0.05 + hh / 2, 0])
    fill.add_updater(upd)
    upd(fill)
    return VGroup(frame, fill)


class W(SpokenScene):
    def setup(self):
        super().setup()
        self.clk = ValueTracker(0)
        self.clk.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.clk)


# ------------------------------------------------------------------------------------------
# The two-by-two board (rows: construct, columns: light)
COLX = [-0.35, 4.15]
ROWY = [1.425, -1.525]
CW, RH = 4.5, 2.95


class Board:
    def __init__(self, clk, bob=0.1):
        self.clk = clk
        self.bob = ValueTracker(bob)
        self.vals = {(r, c): ValueTracker(0.5) for r in (0, 1) for c in (0, 1)}
        self.cells, self.mice, self.meters = {}, {}, {}
        for r in (0, 1):
            for c in (0, 1):
                fill, op = (LIGHT, 0.10) if c else ("#05060a", 0.6)
                self.cells[(r, c)] = Rectangle(width=CW, height=RH, stroke_color=GREY, stroke_width=2.5,
                                               fill_color=fill, fill_opacity=op).move_to([COLX[c], ROWY[r], 0])
                col = OPSIN if r == 0 else FLUOR
                self.mice[(r, c)] = idle(make_mouse(0.9, col).move_to([COLX[c] - 1.2, ROWY[r], 0]), phase=r * 1.7 + c * 0.9)
                self.meters[(r, c)] = meter(COLX[c] + 1.55, ROWY[r] - 1.1, 2.2, 0.5, self._val(r, c))
        self.rowlabs = [chip("OPSIN", OPSIN, size=30).move_to([-4.5, ROWY[0], 0]),
                        chip("FLUOROPHORE", FLUOR, size=28, pad=0.15).move_to([-4.5, ROWY[1], 0])]
        self.heads = [lab("LIGHT OFF", TEXT, 32).move_to([COLX[0], 3.33, 0]),
                      lab("LIGHT ON", LIGHT, 32).move_to([COLX[1], 3.33, 0])]
        self.frame = VGroup(*self.cells.values())

    def _val(self, r, c):
        return lambda: float(np.clip(self.vals[(r, c)].get_value() + self.bob.get_value() * np.sin(1.1 * self.clk.get_value() + r * 1.7 + c * 0.9), 0.03, 1))

    def cell_group(self, r, c):
        return VGroup(self.cells[(r, c)], self.mice[(r, c)], self.meters[(r, c)])

    def everything(self):
        return VGroup(self.frame, *self.mice.values(), *self.meters.values(), *self.rowlabs, *self.heads)

    def meter_top(self, r, c, v):
        return ROWY[r] - 1.1 + 0.05 + v * 2.1


SET_VALS = {(0, 0): 0.30, (0, 1): 0.85, (1, 0): 0.30, (1, 1): 0.60}


def light_bar(clk):
    bar = Rectangle(width=0.4, height=5.9, stroke_width=0, fill_color=LIGHT, fill_opacity=0.28).move_to([COLX[1], -0.05, 0])
    bar.add_updater(lambda m: m.move_to([COLX[1] + 1.9 * np.sin(0.8 * clk.get_value()), -0.05, 0]))
    return bar


def fluoro_parts(bd):
    return [bd.cells[(1, 0)], bd.cells[(1, 1)], bd.mice[(1, 0)], bd.mice[(1, 1)], bd.meters[(1, 0)], bd.meters[(1, 1)], bd.rowlabs[1]]


def dim_anims(bd, instant=False):
    """Dim the fluorophore row (state saved first so Restore brings it back exactly)."""
    out = []
    for i, p in enumerate(fluoro_parts(bd)):
        p.save_state()
        if i < 2:
            a = p.animate.set_stroke(opacity=0.3)
            if instant:
                p.set_stroke(opacity=0.3)
        elif i < 4:
            a = p.animate.set_opacity(0.0)
            if instant:
                p.set_opacity(0.0)
        elif i < 6:
            a = p.animate.set_opacity(0.0)
            if instant:
                p.set_opacity(0.0)
        else:
            a = p.animate.set_opacity(0.4)
            if instant:
                p.set_opacity(0.4)
        out.append(a)
    return out


# ------------------------------------------------------------------------------------------
class S00Hook(W):
    def construct(self):
        arena = make_arena()
        rig = Rig(C0, 1.5, 1.3, speed=0.9)
        trail = TracedPath(rig.mob.get_center, stroke_color=OUT, stroke_width=6, stroke_opacity=0.9)
        self.add(arena, trail)
        self.play(FadeIn(arena), FadeIn(rig.mob), run_time=0.6)
        self.at("no opsin")
        b = badge().move_to([3.8, 3.2, 0])
        self.play(FadeIn(b, shift=DOWN * 0.2), run_time=0.5)
        self.at("light changes")
        beam = make_beam(rig, [-4.8, 3.7, 0])
        self.play(FadeIn(beam), run_time=0.5)
        self.at("firing")
        ax = VGroup(Line([1.2, 2.7, 0], [1.2, 0.4, 0]), Line([1.2, 0.4, 0], [6.5, 0.4, 0])).set_stroke(TEXT, 4)

        def f(t):
            base = 1.0 if t < 0.3 else 1 - 0.55 * (1 - np.exp(-(t - 0.3) / 0.12))
            return base + 0.04 * np.sin(45 * t)
        trace = ParametricFunction(lambda t: np.array([1.35 + 5.0 * t, 0.5 + 1.8 * f(t), 0]), t_range=[0, 1, 0.004],
                                   color=OUT, stroke_width=6)
        on = DashedLine([1.35 + 1.5, 0.45, 0], [1.35 + 1.5, 2.6, 0], color=LIGHT, stroke_width=4)
        cap = lab("FIRING (schematic)", OUT, 26).move_to([3.85, -0.15, 0])
        self.play(FadeIn(ax), FadeIn(cap), FadeIn(on), run_time=0.4)
        self.play(Create(trace), run_time=2.3, rate_func=linear)
        self.at("what did the light change")
        q = T("What did the\nlight change?", size=42, color=TEXT).move_to([3.9, -1.9, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Designing a Causal Circuit Experiment"
    TITLE = "What Did the Light Change?"


class S02LightIsACause(W):
    def construct(self):
        arena = make_arena()
        rig = Rig(C0, 1.5, 1.3, speed=0.9, th0=0.2)
        self.add(arena)
        self.play(FadeIn(arena), FadeIn(rig.mob), run_time=0.6)
        self.at("continuous striatal light")
        beam = make_beam(rig, [-4.8, 3.7, 0])
        self.play(FadeIn(beam), run_time=0.6)
        self.at("bias turning")
        gx = 6.0
        gauge = meter(gx, -2.2, 4.4, 0.7, lambda: 0.5 + 0.3 * np.sin(1.5 * self.clk.get_value()))
        gl = lab("TURNING", OUT, 26).move_to([gx - 0.1, 2.65, 0])
        self.play(FadeIn(gauge), FadeIn(gl), run_time=0.6)
        self.at("illumination had changed tissue")
        self.play(Indicate(beam[1], color=LIGHT, scale_factor=1.6), run_time=1.2)
        self.at("without a light sensitive construct")
        b = badge().move_to([3.4, 3.2, 0])
        self.play(FadeIn(b, shift=DOWN * 0.2), run_time=0.6)
        self.at("light on comparison")
        self.play(FadeOut(beam), run_time=0.6)
        self.at("two things")
        t1, t2 = np.array([1.3, 1.5, 0]), np.array([1.3, -1.5, 0])
        arrs = []
        for tgt in (t1, t2):
            a = Arrow(rig.head(), tgt, buff=0.05, color=LIGHT, stroke_width=8)
            a.add_updater(lambda m, tgt=tgt: m.become(Arrow(rig.head(), tgt, buff=0.05, color=m.get_color(), stroke_width=8)))
            arrs.append(a)
        self.play(*[GrowArrow(a) for a in arrs], run_time=0.9)
        self.at("intended neural activity")
        bx1 = VGroup(RoundedRectangle(corner_radius=0.15, width=2.5, height=1.5, stroke_color=OPSIN, stroke_width=4,
                                      fill_color=OPSIN, fill_opacity=0.15), lab("Intended\nactivity", OPSIN, 28)).move_to([2.55, 1.5, 0])
        self.play(arrs[0].animate.set_color(OPSIN), FadeIn(bx1), run_time=0.7)
        self.at("light itself")
        bx2 = VGroup(RoundedRectangle(corner_radius=0.15, width=2.5, height=1.5, stroke_color=ALT, stroke_width=4,
                                      fill_color=ALT, fill_opacity=0.15), lab("Light\nitself", ALT, 28)).move_to([2.55, -1.5, 0])
        self.play(arrs[1].animate.set_color(ALT), FadeIn(bx2), run_time=0.7)
        f1 = Arrow([3.85, 1.5, 0], [5.55, 0.6, 0], buff=0, color=OPSIN, stroke_width=7)
        f2 = Arrow([3.85, -1.5, 0], [5.55, -0.6, 0], buff=0, color=ALT, stroke_width=7)
        self.play(GrowArrow(f1), GrowArrow(f2), run_time=0.8)
        self.finish()


class S03Questions(W):
    def construct(self):
        arena = make_arena()
        rig = Rig(C0, 1.5, 1.3, speed=0.9, th0=0.2)
        self.add(arena)
        self.play(FadeIn(arena), FadeIn(rig.mob), run_time=0.4)
        act, amp = ValueTracker(0.5), ValueTracker(0.25)
        clk = self.clk

        def A():
            return float(np.clip(act.get_value() + amp.get_value() * np.sin(1.4 * clk.get_value()), 0.05, 1))

        def B():
            return 0.1 + 0.85 * A()
        band = RoundedRectangle(corner_radius=0.3, width=9.4, height=1.6, stroke_color=GREY, stroke_width=4,
                                fill_color=TEXT, fill_opacity=0.05)
        self.at("recording")
        self.play(Transform(arena, band), FadeOut(rig.mob), run_time=1.6)
        ma = meter(-5.5, -2.4, 4.8, 0.8, A)
        mb = meter(5.5, -2.4, 4.8, 0.8, B)
        self.play(FadeIn(ma), FadeIn(mb), run_time=0.6)
        self.at("activity and behavior")
        la = lab("ACTIVITY", OUT, 28).move_to([-5.5, 2.95, 0])
        lb = lab("BEHAVIOUR", OUT, 28).move_to([5.5, 2.95, 0])
        self.play(FadeIn(la), FadeIn(lb), run_time=0.5)
        self.at("vary together")
        dash = DashedLine([-4.65, 0, 0], [4.65, 0, 0], color=GREY, stroke_width=6)
        vt = lab("VARY TOGETHER", TEXT, 30).move_to([0, 1.3, 0])
        self.play(Create(dash), FadeIn(vt), run_time=1.0)
        self.at("manipulation asks")
        solid = Arrow([-4.65, 0, 0], [4.65, 0, 0], buff=0, color=OPSIN, stroke_width=12)
        mp = lab("MANIPULATION", OPSIN, 32).move_to([0, 1.3, 0])
        self.play(Transform(dash, solid), Transform(vt, mp), amp.animate.set_value(0.05), run_time=1.2)
        self.at("driving chosen cells")
        push = Arrow([-6.4, -2.2, 0], [-6.4, 0.4, 0], buff=0, color=OPSIN, stroke_width=10)
        self.play(GrowArrow(push), act.animate.set_value(0.85), run_time=2.6)
        self.at("sufficient")
        suf = lab("SUFFICIENT?", OPSIN, 46).move_to([0, 2.3, 0])
        self.play(FadeIn(suf, shift=DOWN * 0.2), run_time=0.6)
        self.at("suppressing them")
        brake = VGroup(Line([-6.4, 2.3, 0], [-6.4, 1.0, 0]), Line([-6.75, 1.0, 0], [-6.05, 1.0, 0])).set_stroke(OPSIN, 10)
        self.play(FadeOut(push), FadeIn(brake), act.animate.set_value(0.12), run_time=2.0)
        self.at("necessary")
        nec = lab("NECESSARY?", OPSIN, 46).move_to([0, 2.3, 0])
        self.play(Transform(suf, nec), run_time=0.6)
        self.at("each answer")
        br = Brace(Line([-4.65, -0.9, 0], [4.65, -0.9, 0]), DOWN, color=OPSIN)
        tc = lab("TESTED CONDITIONS", TEXT, 30).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(tc), amp.animate.set_value(0.12), run_time=1.0)
        self.finish()


class S04BuildGrid(W):
    def construct(self):
        clk = self.clk
        bd = Board(clk)
        band = RoundedRectangle(corner_radius=0.3, width=9.4, height=1.6, stroke_color=GREY, stroke_width=4,
                                fill_color=TEXT, fill_opacity=0.05)
        a, b = ValueTracker(0.15), ValueTracker(0.2)
        ma = meter(-5.5, -2.4, 4.8, 0.8, lambda: float(a.get_value() + 0.05 * np.sin(clk.get_value())))
        mb = meter(5.5, -2.4, 4.8, 0.8, lambda: float(b.get_value() + 0.05 * np.sin(clk.get_value())))
        self.add(band, ma, mb)
        self.play(FadeIn(band), FadeIn(ma), FadeIn(mb), run_time=0.4)
        self.at("to separate the two causes")
        self.play(FadeOut(ma), FadeOut(mb), Transform(band, bd.frame), run_time=2.0)
        self.at("cross construct")
        self.remove(band)
        self.play(Create(bd.frame, lag_ratio=0.3), run_time=2.0)
        self.at("opsin and fluorophore")
        self.play(FadeIn(bd.rowlabs[0], shift=RIGHT * 0.6), run_time=0.7)
        self.wait(0.3)
        self.play(FadeIn(bd.rowlabs[1], shift=RIGHT * 0.6), run_time=0.7)
        self.at("light off and light on")
        self.play(FadeIn(bd.heads[0], shift=DOWN * 0.2), run_time=0.7)
        bar = light_bar(clk)
        self.play(FadeIn(bd.heads[1], shift=DOWN * 0.2), FadeIn(bar), run_time=0.8)
        self.at("now every effect")
        for k, key in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            self.play(FadeIn(bd.mice[key], scale=0.6), run_time=0.5)
        self.at("matched place")
        for key in bd.meters:
            bd.vals[key].set_value(0.5)
        self.play(*[FadeIn(m) for m in bd.meters.values()], run_time=1.0)
        tag = T("schematic meters", size=24, color=TEXT).move_to([-4.5, -3.45, 0])
        self.play(FadeIn(tag), run_time=0.4)
        self.finish()


class S05Predict(W):
    def construct(self):
        clk = self.clk
        bd = Board(clk)
        for k in bd.vals:
            bd.vals[k].set_value(0.5)
        bar = light_bar(clk)
        self.add(bd.everything(), bar)
        self.wait(0.3)
        self.at("only in")
        self.play(*dim_anims(bd), run_time=1.0)
        self.play(*[bd.cells[k].animate.set_stroke(OPSIN, 5) for k in ((0, 0), (0, 1))], run_time=0.8)
        self.at("which missing comparison")
        qm = T("?", size=130, color=ALT, weight=BOLD).move_to([-0.35, ROWY[1], 0])
        qt = T("Which comparison\nis missing?", size=34, color=TEXT).move_to([4.15, ROWY[1], 0])
        qb = Rectangle(width=4.2, height=1.1, stroke_width=0, fill_color="#0c0f16", fill_opacity=0.92).move_to(qt.get_center())
        qt = VGroup(qb, qt)
        self.play(GrowFromCenter(qm), FadeIn(qt), run_time=1.0)
        self.play(qm.animate.scale(1.1), run_time=1.5, rate_func=there_and_back)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        clk = ValueTracker(0)
        clk.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clk)
        bd = Board(clk)
        for k, v in {(0, 0): 0.5, (0, 1): 0.5, (1, 0): 0.0, (1, 1): 0.0}.items():
            bd.vals[k].set_value(v)
        bar = light_bar(clk)
        dim_anims(bd, instant=True)
        for k in ((0, 0), (0, 1)):
            bd.cells[k].set_stroke(OPSIN, 5)
        qm = T("?", size=130, color=ALT, weight=BOLD).move_to([-0.35, ROWY[1], 0])
        qt = T("Which comparison\nis missing?", size=34, color=TEXT).move_to([4.15, ROWY[1], 0])
        qb = Rectangle(width=4.2, height=1.1, stroke_width=0, fill_color="#0c0f16", fill_opacity=0.92).move_to(qt.get_center())
        qt = VGroup(qb, qt)
        self.add(bd.everything(), bar, qm, qt)
        self.play(qm.animate.scale(1.12), run_time=2.0, rate_func=there_and_back)
        self.finish()


class S07Reveal(W):
    def construct(self):
        clk = self.clk
        bd = Board(clk, bob=0.0)
        bd.vals[(0, 0)].set_value(0.30)
        bd.vals[(0, 1)].set_value(0.85)
        bd.vals[(1, 0)].set_value(0.0)
        bd.vals[(1, 1)].set_value(0.0)
        bar = light_bar(clk)
        dim_anims(bd, instant=True)
        for k in ((0, 0), (0, 1)):
            bd.cells[k].set_stroke(OPSIN, 5)
        self.add(bd.everything(), bar)
        self.wait(0.3)
        self.at("fluorophore only animals")
        self.play(*[Restore(p) for p in fluoro_parts(bd)], run_time=0.8)
        self.play(bd.vals[(1, 0)].animate.set_value(0.30), bd.vals[(1, 1)].animate.set_value(0.60), run_time=1.6)
        self.at("first measure")

        def bracket(r, v0, v1):
            y0, y1 = bd.meter_top(r, 0, v0), bd.meter_top(r, 1, v1)
            d = DashedLine([1.5, y0, 0], [6.15, y0, 0], color=OUT, stroke_width=4)
            a = Arrow([6.15, y0, 0], [6.15, y1, 0], buff=0, color=OUT, stroke_width=9)
            return VGroup(d, a), y1 - y0
        br0, e0 = bracket(0, 0.30, 0.85)
        br1, e1 = bracket(1, 0.30, 0.60)
        self.play(Create(br0), run_time=1.2)
        self.wait(0.4)
        self.play(Create(br1), run_time=1.2)
        self.at("then compare")
        fade = [bd.frame, *bd.mice.values(), *bd.meters.values(), *bd.rowlabs, *bd.heads, bar]
        self.play(*[m.animate.set_opacity(0.05) for m in fade], run_time=0.8)
        base_y = -3.0
        s = 2.8
        h0, h1 = e0 * s, e1 * s
        opsin_low = Rectangle(width=1.8, height=h1, stroke_width=0, fill_color=OUT, fill_opacity=0.9).move_to([-1.0, base_y + h1 / 2, 0])
        opsin_up = Rectangle(width=1.8, height=h0 - h1, stroke_width=0, fill_color=OUT, fill_opacity=0.9).move_to([-1.0, base_y + h1 + (h0 - h1) / 2, 0])
        fl = Rectangle(width=1.8, height=h1, stroke_width=0, fill_color=OUT, fill_opacity=0.9).move_to([1.6, base_y + h1 / 2, 0])
        lo = lab("OPSIN", OPSIN, 30).move_to([-1.0, -3.45, 0])
        lf = lab("FLUOROPHORE", FLUOR, 30).move_to([1.6, -3.45, 0])
        self.play(TransformFromCopy(br0, VGroup(opsin_low, opsin_up)), TransformFromCopy(br1, fl), FadeIn(lo), FadeIn(lf), run_time=1.6)
        guide = DashedLine([1.6 - 0.9, base_y + h1, 0], [-1.0 + 0.9, base_y + h1, 0], color=TEXT, stroke_width=4)
        self.play(Create(guide), run_time=0.8)
        self.at("shared light effect cancels")
        self.play(opsin_low.animate.set_fill(ALT), fl.animate.set_fill(ALT), run_time=0.7)
        self.play(fl.animate.move_to([-1.0, base_y + h1 / 2, 0]), FadeOut(guide), FadeOut(lf), run_time=1.0)
        self.play(FadeOut(fl, scale=0.2), FadeOut(opsin_low, scale=0.2), run_time=0.8)
        self.play(opsin_up.animate.move_to([-1.0, base_y + (h0 - h1) / 2, 0]), lo.animate.move_to([-1.0, -3.45, 0]), run_time=1.0)
        self.at("the remainder")
        self.play(opsin_up.animate.set_fill(OPSIN), run_time=0.8)
        self.at("extra light linked effect")
        ex = lab("EXTRA WITH OPSIN", OPSIN, 40).move_to([2.6, -0.9, 0])
        tg = T("schematic", size=24, color=TEXT).next_to(ex, DOWN, buff=0.2)
        self.play(FadeIn(ex, shift=LEFT * 0.3), FadeIn(tg), FadeOut(lo), *[m.animate.set_opacity(0.0) for m in fade], run_time=0.8)
        self.at("associated with carrying")
        self.play(opsin_up.animate.scale(1.08), run_time=1.0, rate_func=there_and_back)
        self.play(Indicate(ex, color=OPSIN, scale_factor=1.05), run_time=1.5)
        self.finish()


class S08Interaction(W):
    def construct(self):
        clk = self.clk
        bd = Board(clk, bob=0.0)
        for k, v in SET_VALS.items():
            bd.vals[k].set_value(v)
        self.add(bd.everything())
        self.wait(0.4)
        self.at("not four separate boxes")
        for k in bd.cells:
            self.play(Indicate(bd.cells[k], color=TEXT, scale_factor=1.03), run_time=0.45)
        self.at("measure the light effect in opsin")
        fade = [bd.frame, *bd.mice.values(), *bd.meters.values(), *bd.heads]
        self.play(*[m.animate.set_opacity(0.04) for m in fade], run_time=0.7)
        x0 = -2.8
        top_a = Line([x0, ROWY[0], 0], [x0 + 3.0, ROWY[0], 0]).set_stroke(OUT, 12)
        top_b = Arrow([x0 + 3.0, ROWY[0], 0], [x0 + 5.5, ROWY[0], 0], buff=0, color=OUT, stroke_width=12)
        bot = Arrow([x0, ROWY[1], 0], [x0 + 3.0, ROWY[1], 0], buff=0, color=OUT, stroke_width=12)
        le0 = lab("LIGHT EFFECT", OUT, 30).move_to([x0 + 2.75, ROWY[0] + 0.85, 0])
        le1 = lab("LIGHT EFFECT", OUT, 30).move_to([x0 + 1.5, ROWY[1] + 0.85, 0])
        self.play(Create(top_a), GrowArrow(top_b), FadeIn(le0), run_time=1.4)
        self.at("measure it again")
        self.play(GrowArrow(bot), FadeIn(le1), run_time=1.4)
        self.at("subtract")
        self.play(FadeOut(bd.rowlabs[0]), FadeOut(bd.rowlabs[1]), FadeOut(le0), FadeOut(le1),
                  top_a.animate.shift(UP * (0.9 - ROWY[0])), top_b.animate.shift(UP * (0.9 - ROWY[0])),
                  bot.animate.shift(UP * (-0.1 - ROWY[1])), *[m.animate.set_opacity(0.0) for m in fade], run_time=1.2)
        self.play(top_a.animate.set_color(ALT), bot.animate.set_color(ALT), run_time=0.6)
        self.play(bot.animate.shift(UP * 1.0), run_time=0.8)
        self.play(FadeOut(top_a, scale=0.2), FadeOut(bot, scale=0.2), run_time=0.7)
        self.at("difference of differences")
        dd = lab("DIFFERENCE OF DIFFERENCES", TEXT, 32).move_to([0, -1.8, 0])
        self.play(FadeIn(dd, shift=UP * 0.2), top_b.animate.set_color(OPSIN), run_time=0.8)
        self.at("opsin linked remainder")
        self.play(FadeOut(dd), top_b.animate.scale(1.8).move_to([0, 0.4, 0]), run_time=1.2)
        rl = lab("OPSIN-LINKED REMAINDER", OPSIN, 38).move_to([0, -1.2, 0])
        self.play(FadeIn(rl, shift=UP * 0.2), run_time=0.7)
        self.play(Indicate(top_b, color=OPSIN, scale_factor=1.06), run_time=1.5)
        self.finish()


class S09ClaimScope(W):
    def construct(self):
        rem = Arrow([-2.2, 0.4, 0], [2.2, 0.4, 0], buff=0, color=OPSIN, stroke_width=22)
        frame = RoundedRectangle(corner_radius=0.25, width=12.8, height=3.0, stroke_color=OPSIN, stroke_width=5,
                                 fill_color=OPSIN, fill_opacity=0.06).move_to([0, 2.1, 0])
        self.add(rem)
        self.wait(0.5)
        self.at("not a license")
        self.play(Transform(rem, frame), run_time=1.6)
        self.at("controls the behavior")
        self.play(Indicate(rem, color=ALT, scale_factor=1.02), run_time=1.2)
        slots = {}
        pos = {"CELLS": [-3.1, 2.85], "PROJECTION": [3.1, 2.85], "TIME": [-3.1, 1.4], "ASSAY": [3.1, 1.4]}
        for name in ("CELLS", "PROJECTION", "TIME", "ASSAY"):
            slots[name] = VGroup(RoundedRectangle(corner_radius=0.15, width=5.6, height=1.2, stroke_color=TEXT, stroke_width=3,
                                                  fill_color=TEXT, fill_opacity=0.08), lab(name, TEXT, 36)).move_to(pos[name] + [0])
        self.at("name the cells")
        self.play(FadeIn(slots["CELLS"], scale=1.3), run_time=0.5)
        self.at("the projection")
        self.play(FadeIn(slots["PROJECTION"], scale=1.3), run_time=0.5)
        self.at("time window")
        self.play(FadeIn(slots["TIME"], scale=1.3), run_time=0.5)
        self.at("assay")
        self.play(FadeIn(slots["ASSAY"], scale=1.3), run_time=0.5)
        self.at("activation tests")
        suf = lab("SUFFICIENT", OPSIN, 38).move_to([-3.2, -0.2, 0])
        track = RoundedRectangle(corner_radius=0.3, width=0.6, height=1.6, stroke_color=OPSIN, stroke_width=4).move_to([-3.2, -1.8, 0])
        knob = Circle(radius=0.22, stroke_width=0, fill_color=OPSIN, fill_opacity=1).move_to([-3.2, -2.3, 0])
        self.play(FadeIn(suf, shift=DOWN * 0.2), FadeIn(track), FadeIn(knob), run_time=0.7)
        self.play(knob.animate.move_to([-3.2, -1.3, 0]), run_time=1.4)
        self.at("silencing tests")
        nec = lab("NECESSARY", OPSIN, 38).move_to([3.2, -0.2, 0])
        brk = VGroup(Line([3.2, -0.8, 0], [3.2, -2.0, 0]), Line([2.8, -2.0, 0], [3.6, -2.0, 0])).set_stroke(OPSIN, 10)
        self.play(FadeIn(nec, shift=DOWN * 0.2), run_time=0.6)
        self.play(Create(brk), run_time=1.2)
        self.at("neither says")
        st = VGroup(RoundedRectangle(corner_radius=0.12, width=3.6, height=0.75, stroke_color=ALT, stroke_width=5, fill_opacity=0),
                    lab("ONLY ROUTE", ALT, 30)).rotate(0.12).move_to([-9, -3.3, 0])
        self.play(st.animate.move_to([-0.5, -3.3, 0]), run_time=1.4)
        self.at("route")
        self.play(st.animate.move_to([10, -3.3, 0]), run_time=1.0)
        self.finish()


class S10Projection(W):
    def construct(self):
        clk = self.clk
        chp = chip("PROJECTION", TEXT, size=40).move_to([0, 0, 0])
        self.add(chp)
        parent = VGroup(Rectangle(width=3.2, height=2.0, stroke_color=OPSIN, stroke_width=4, fill_color=OPSIN, fill_opacity=0.12),
                        lab("PARENT\nCELLS", OPSIN, 28)).move_to([-5.0, 0, 0])
        target = VGroup(Rectangle(width=2.6, height=2.0, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.08),
                        lab("TARGET", TEXT, 28)).move_to([5.4, 0, 0])
        axon = Line([-3.4, 0, 0], [1.0, 0, 0]).set_stroke(OPSIN, 8)
        spot = Circle(radius=1.1, stroke_color=LIGHT, stroke_width=3, fill_color=LIGHT, fill_opacity=0.18).move_to([1.9, 0, 0])
        syn = Arrow([3.0, 0, 0], [4.0, 0, 0], buff=0, color=OPSIN, stroke_width=8)
        self.play(FadeOut(chp), FadeIn(parent), FadeIn(target), Create(axon), run_time=0.9)
        self.play(Create(syn), run_time=0.3)
        self.at("light spot")
        self.play(FadeIn(spot, scale=0.5), run_time=0.6)
        self.at("terminal illumination")
        beam = Polygon([1.9, 3.7, 0], [2.5, 1.0, 0], [1.3, 1.0, 0], stroke_width=0, fill_color=LIGHT, fill_opacity=0.32)
        beam.add_updater(lambda m: m.set_fill(LIGHT, 0.28 + 0.08 * np.sin(3 * clk.get_value())))
        self.play(FadeIn(beam), run_time=0.8)
        self.at("labeled axons")

        def arch(t):
            return np.array([-0.4 + 4.6 * t, -3.5 * (1 - t) ** 2 + 5.0 * t * (1 - t) - 3.5 * t ** 2, 0])
        pa = ParametricFunction(arch, t_range=[0, 1, 0.01], color=ALT, stroke_width=7)
        self.play(Create(pa), run_time=2.0)
        pl = lab("PASSING AXON", ALT, 28).move_to([-1.9, -2.6, 0])
        self.play(FadeIn(pl), run_time=0.5)
        self.at("drive activity back")
        back = Arrow([1.3, 0.8, 0], [-3.3, 0.8, 0], buff=0, color=ALT, stroke_width=8)
        self.play(GrowArrow(back), run_time=1.5)
        bl = lab("BACKWARD", ALT, 28).move_to([-1.2, 1.4, 0])
        self.play(FadeIn(bl), FadeOut(pl), run_time=0.5)
        self.at("parent cell bodies")
        self.play(Indicate(parent, color=ALT, scale_factor=1.06), run_time=1.0)
        self.at("a local receptor block")
        ef = ValueTracker(0.9)
        gauge = meter(4.7, 1.3, 2.2, 0.6, lambda: float(ef.get_value() + 0.04 * np.sin(2 * clk.get_value())), color=OUT)
        gl = lab("EFFECT", OUT, 28).move_to([6.0, 2.4, 0])
        self.play(FadeIn(gauge), FadeIn(gl), FadeOut(bl), run_time=0.7)
        self.at("receptor block")
        gate = Line([3.5, -0.9, 0], [3.5, 0.9, 0]).set_stroke(FLUOR, 12)
        gt = lab("RECEPTOR\nBLOCK", FLUOR, 28).move_to([5.4, -1.8, 0])
        self.play(Create(gate), FadeIn(gt), run_time=0.8)
        self.at("transmitter action")
        self.play(syn.animate.set_opacity(0.3), run_time=0.8)
        self.at("measured behavioral effect")
        self.play(ef.animate.set_value(0.0), run_time=1.2)
        tg = T("schematic", size=24, color=TEXT).move_to([-5.2, -3.45, 0])
        self.play(FadeIn(tg), run_time=0.3)
        self.finish()


class S11Validate(W):
    def construct(self):
        clk = self.clk
        frame = RoundedRectangle(corner_radius=0.25, width=12.8, height=3.0, stroke_color=OPSIN, stroke_width=5,
                                 fill_color=OPSIN, fill_opacity=0.06).move_to([0, 2.1, 0])
        self.add(frame)
        P = {"TL": [-4.3, 2.35], "TR": [4.3, 2.35], "BL": [-4.3, -0.5], "BR": [4.3, -0.5]}
        panels = {k: RoundedRectangle(corner_radius=0.2, width=4.4, height=2.5, stroke_color=GREY, stroke_width=3).move_to(p + [0])
                  for k, p in P.items()}
        mouse = idle(make_mouse(2.1, TEXT).move_to([0, 0.5, 0]), 0.3, 0.1)
        self.wait(0.3)
        self.at("finally")
        self.play(ReplacementTransform(frame, VGroup(*panels.values())), run_time=1.6)
        self.at("verify what")
        self.play(FadeIn(mouse, scale=0.7), run_time=0.8)
        self.at("record during")
        tl = panels["TL"]
        ax = VGroup(Line([-6.2, 1.5, 0], [-6.2, 2.5, 0]), Line([-6.2, 1.5, 0], [-2.5, 1.5, 0])).set_stroke(TEXT, 3)
        strip = Rectangle(width=1.8, height=1.0, stroke_width=0, fill_color=LIGHT, fill_opacity=0.2).move_to([-4.2, 2.0, 0])

        def f(t):
            if t < 0.2:
                v = 1.0
            elif t < 0.6:
                v = 1 - 0.55 * (1 - np.exp(-(t - 0.2) / 0.08))
            else:
                v = 0.45 + 0.55 * (1 - np.exp(-(t - 0.6) / 0.15))
            return v + 0.05 * np.sin(40 * t)
        tr = ParametricFunction(lambda t: np.array([-6.1 + 3.5 * t, 1.55 + 0.9 * f(t) * 0.9, 0]), t_range=[0, 1, 0.004], color=OUT, stroke_width=5)
        ld = lab("DURING", LIGHT, 26).move_to([-4.9, 2.75, 0])
        la = lab("AFTER", OUT, 26).move_to([-3.2, 2.75, 0])
        self.play(FadeIn(ax), FadeIn(strip), FadeIn(ld), run_time=0.5)
        self.play(Create(tr), run_time=1.4, rate_func=linear)
        self.play(FadeIn(la), run_time=0.3)
        self.at("confirm expression")
        ring = DashedVMobject(Circle(radius=0.45, color=TEXT, stroke_width=3)).move_to([4.3, 2.25, 0])
        patch = Ellipse(width=0.9, height=0.6, stroke_width=0, fill_color=OPSIN, fill_opacity=0.8).move_to([4.9, 1.95, 0])
        tip = Polygon([4.3, 2.95, 0], [4.15, 2.5, 0], [4.45, 2.5, 0], stroke_width=0, fill_color=LIGHT, fill_opacity=0.9).move_to([3.2, 2.9, 0])
        ex = lab("EXPRESSION · FIBRE", TEXT, 24).move_to([4.3, 1.4, 0])
        self.play(FadeIn(ring), FadeIn(patch), FadeIn(tip), FadeIn(ex), run_time=0.6)
        self.play(patch.animate.move_to([4.3, 2.25, 0]), tip.animate.move_to([4.3, 2.8, 0]), run_time=1.6)
        self.at("randomize allocation")
        cards = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.7, height=0.9, stroke_color=[OPSIN, FLUOR][i % 2], stroke_width=4,
                                          fill_color=[OPSIN, FLUOR][i % 2], fill_opacity=0.25).move_to([-5.4 + 0.95 * i, -0.2, 0]) for i in range(4)])
        rl = lab("RANDOMIZE", TEXT, 28).move_to([-4.3, -1.2, 0])
        self.play(FadeIn(cards), FadeIn(rl), run_time=0.5)
        order = [2, 0, 3, 1]
        self.play(*[cards[i].animate.move_to([-5.4 + 0.95 * order[i], -0.2, 0]) for i in range(4)], run_time=1.0)
        self.play(*[cards[i].animate.move_to([-5.4 + 0.95 * ((order[i] + 1) % 4), -0.2, 0]) for i in range(4)], run_time=1.0)
        self.at("blind the scoring")
        eye = Ellipse(width=1.6, height=0.9, stroke_color=TEXT, stroke_width=4).move_to([4.3, 0.1, 0])
        pup = Dot([4.3, 0.1, 0], radius=0.2, color=TEXT)
        sl = lab("SCORE", TEXT, 28).move_to([4.3, -1.2, 0])
        self.play(FadeIn(eye), FadeIn(pup), FadeIn(sl), run_time=0.5)
        self.play(eye.animate.stretch_to_fit_height(0.12), FadeOut(pup), run_time=1.0)
        self.at("only when the manipulation")
        bar = VGroup(RoundedRectangle(corner_radius=0.15, width=7.0, height=0.9, stroke_color=OPSIN, stroke_width=4,
                                      fill_color=OPSIN, fill_opacity=0.25), lab("MATCHED CONTRAST", OPSIN, 32)).move_to([0, -3.1, 0])
        arrows = [Arrow(panels[k].get_bottom() if k in ("BL", "BR") else mouse.get_bottom(), bar.get_top() + [dx, 0, 0], buff=0.1,
                        color=OPSIN, stroke_width=5) for k, dx in (("BL", -2.4), ("BR", 2.4))]
        self.play(FadeIn(bar, shift=UP * 0.3), *[GrowArrow(a) for a in arrows], run_time=1.2)
        self.at("can the matched contrast")
        self.play(Indicate(bar, color=OPSIN, scale_factor=1.06), run_time=1.5)
        self.at("a claim can be")
        self.play(mouse.animate.scale(1.1), run_time=1.5, rate_func=there_and_back)
        self.finish()


class S12End(EndCard):
    LINE = "A claim can be no broader than that contrast."
