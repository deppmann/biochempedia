"""Trend and Chance (conservation, film 1)

COLOUR MAP
  BLUE   = population runs (log numbers vs years)      RED  = the floor, and runs that touched it
  GOLD   = the trend arrow                             TEXT = labels, swings band (grey fill)
  YELLOW = dials / the question
Every run is computed: ln N(t+1) = ln N(t) + trend + swings * z, floor = 10 animals, 200 runs from one fixed seed.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

FL = float(np.log(10))
Z = np.random.default_rng(950).standard_normal((200, 1000))
LO, HI = 1.0, 9.0


class Panel:
    def __init__(s, x0, y0, w, h, tm=100, yticks=False, xlabel=True):
        s.x0, s.y0, s.w, s.h = x0, y0, w, h
        s.tm = ValueTracker(tm)
        s.yticks, s.xlabel = yticks, xlabel

    def X(s, t):
        return s.x0 + s.w * min(t / s.tm.get_value(), 1.0)

    def Y(s, l):
        return s.y0 + s.h * (min(max(l, LO), HI) - LO) / (HI - LO)

    def floor_line(s):
        return DashedLine([s.x0, s.Y(FL), 0], [s.x0 + s.w, s.Y(FL), 0], color=RED, stroke_width=4, dash_length=0.18)

    def base(s):
        g = VGroup(Rectangle(width=s.w, height=s.h, stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                             fill_opacity=0.07).move_to([s.x0 + s.w / 2, s.y0 + s.h / 2, 0]))
        ry = s.y0 - 0.32
        for t, txt in [(0, "0"), (100, "100"), (1000, "1000")]:
            lab = M(txt, 24, TEXT)

            def up(m, t=t, lab=lab):
                m.move_to([s.X(t), ry, 0])
                m.set_opacity(1 if s.tm.get_value() >= 0.999 * t else 0)
            lab.add_updater(up)
            up(lab)
            g.add(lab)
        if s.xlabel:
            g.add(T("years", 24).move_to([s.x0 + s.w / 2, ry, 0]))
        if s.yticks:
            for n in (10, 100, 1000):
                lab = M(str(n), 24).move_to([0, s.Y(np.log(n)), 0])
                lab.set_x(s.x0 - 0.15 - lab.width / 2)
                g.add(lab)
            g.add(T("numbers (log scale)", 24).rotate(PI / 2).move_to([s.x0 - 1.3, s.y0 + s.h / 2, 0]))
        return g


MAIN = dict(x0=-5.1, y0=-3.0, w=8.7, h=5.3)


def main_panel(tm=100):
    return Panel(tm=tm, yticks=True, **MAIN)


def split_panels(tm=100):
    return (Panel(-6.2, -2.7, 5.3, 4.3, tm), Panel(0.9, -2.7, 5.3, 4.3, tm))


class Fan(VGroup):
    def __init__(s, panel, rows, mu=0.01, sigma=0.2, n0=50, k=0.0, width=2.0, op=0.55):
        super().__init__()
        s.p = panel
        s.Zs = Z[rows]
        s.R = len(s.Zs)
        s.mu, s.sg, s.n0, s.k = ValueTracker(mu), ValueTracker(sigma), ValueTracker(n0), ValueTracker(k)
        s.width, s.op, s.dimf = width, op, 1.0
        s._key = None
        s.runs = [VMobject() for _ in range(s.R)]
        s.add(*s.runs)
        s.add_updater(lambda m: m._upd())
        s._upd()

    def _data(s):
        key = (round(s.mu.get_value(), 5), round(s.sg.get_value(), 5), round(s.n0.get_value(), 3))
        if key != s._key:
            s._key = key
            mu, sg, n0 = key
            x = np.log(n0) + np.concatenate([np.zeros((s.R, 1)), np.cumsum(mu + sg * s.Zs, axis=1)], axis=1)
            below = x[:, 1:] <= FL
            hit = np.where(below.any(axis=1), below.argmax(axis=1) + 1, 10 ** 6)
            s._x, s._hit = x, hit
        return s._x, s._hit

    def count(s):
        _, hit = s._data()
        return int((hit <= int(s.k.get_value())).sum())

    def frac(s):
        return s.count() / s.R

    def _upd(s):
        x, hit = s._data()
        p = s.p
        ki = int(s.k.get_value())
        tm = p.tm.get_value()
        stride = max(1, int(tm / 150))
        for i, r in enumerate(s.runs):
            end = min(ki, int(hit[i]), 1000)
            idx = np.arange(0, end + 1, stride)
            if idx[-1] != end:
                idx = np.append(idx, end)
            v = x[i, idx].copy()
            if hit[i] <= end:
                v[-1] = FL
            xs = p.x0 + p.w * np.minimum(idx / tm, 1.0)
            ys = p.y0 + p.h * (np.clip(v, LO, HI) - LO) / (HI - LO)
            pts = np.stack([xs, ys, np.zeros_like(xs)], axis=1)
            if len(pts) < 2:
                pts = np.vstack([pts, pts])
            r.set_points_as_corners(pts)
            hitnow = hit[i] <= ki
            r.set_stroke(RED if hitnow else BLUE, s.width + (0.6 if hitnow else 0), (0.8 if hitnow else s.op) * s.dimf if ki > 0 else 0)
            r.set_fill(opacity=0)


class Live(VGroup):
    def __init__(s, fn, size=30, color=TEXT, mono=False, anchor=ORIGIN, left=False, op=1.0):
        super().__init__()
        s.fn, s.size, s.color, s.mono, s.anchor, s.left, s.op, s._s = fn, size, color, mono, np.array(anchor, float), left, op, None
        s.add_updater(lambda m: m._upd())
        s._upd()

    def _upd(s):
        t = s.fn()
        if not hasattr(s, "_cache"):
            s._cache = {}
        if t not in s._cache:
            m = (M if s.mono else T)(t, s.size, s.color)
            if s.left:
                m.move_to(s.anchor + RIGHT * m.width / 2)
            else:
                m.move_to(s.anchor)
            s._cache[t] = m
            s.add(m)
        s._s = t
        for k, m in s._cache.items():
            m.set_opacity(s.op if k == t else 0)


def live_fade(live, a0, a1, rt):
    return UpdateFromAlphaFunc(live, lambda m, a: (setattr(m, "op", a0 + (a1 - a0) * a), m._upd()), run_time=rt)


def trend_arrow(panel, fan, color=GOLD):
    def build():
        mu, n0, tm = fan.mu.get_value(), np.log(fan.n0.get_value()), panel.tm.get_value()
        te = tm
        if mu < -1e-6:
            te = min(tm, (n0 - LO) / -mu)
        elif mu > 1e-6:
            te = min(tm, (HI - n0) / mu)
        te = max(te, tm * 0.12)
        st = np.array([panel.X(0), panel.Y(n0), 0])
        en = np.array([panel.X(te), panel.Y(n0 + mu * te), 0])
        if np.linalg.norm(en - st) < 0.4:
            en = st + (en - st) / max(np.linalg.norm(en - st), 1e-6) * 0.4
        return Arrow(st, en, buff=0, color=color, stroke_width=7, max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=12)
    a = build()
    a.set_z_index(5)
    a.add_updater(lambda m: m.become(build()).set_z_index(5))
    return a


def dial(center, r, tracker, vmin, vmax, color=YELLOW):
    ring = Circle(radius=r, stroke_color=TEXT, stroke_width=3, fill_color=color, fill_opacity=0.12).move_to(center)
    needle = Line(ORIGIN, RIGHT * r * 0.85, color=color, stroke_width=6)

    def up(m):
        a = np.radians(150 - (tracker.get_value() - vmin) / (vmax - vmin) * 120)
        m.become(Line(np.array(center) , np.array(center) + r * 0.85 * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=6))
    needle.add_updater(up)
    up(needle)
    return VGroup(ring, needle)


class Sc(SpokenScene):
    def ramp(self, tracker, v, phrase, lead=0.25, nth=0, min_t=0.4, rf=linear, **extra):
        d = self.t_of(phrase, nth) - lead - self.elapsed()
        self.play(tracker.animate.set_value(v), *[t.animate.set_value(x) for t, x in extra.items() and []], run_time=max(min_t, d), rate_func=rf)


def pick_main():
    for r in range(200):
        x = np.log(50) + np.cumsum(0.01 + 0.2 * Z[r, :100])
        if np.log(50) + 0.3 < x[-1] < np.log(50) + 1.3 and x.max() < np.log(50) + 2.4 and FL + 0.5 < x.min() < np.log(50) - 0.3:
            return r
    return 0


def pick_right():
    for r in range(200):
        x = np.log(50) + np.cumsum(0.01 + 0.25 * Z[r, :100])
        if np.log(50) + 0.9 < x[-1] < np.log(50) + 2.3 and x.min() > FL + 0.5 and np.abs(np.diff(x)).max() > 0.5:
            return r
    return 0


def pct(f):
    return f"{round(100 * f)}%"


class S00Title(TitleCard):
    LESSON = "Conservation and Restoration"
    TITLE = "Trend and Chance"


class S01Question(Sc):
    def construct(self):
        L, R = split_panels()
        fl = Fan(L, [0], mu=-0.01, sigma=0.05, n0=50, width=5, op=1)
        fr = Fan(R, [pick_right()], mu=0.01, sigma=0.25, n0=50, width=5, op=1)
        q = T("?", 96, color=YELLOW, weight=BOLD).move_to([0, 2.45, 0])
        self.play(FadeIn(L.base()), FadeIn(R.base()), run_time=0.8)
        self.add(fl, fr)
        self.play(Write(q), run_time=1.0)
        self.at("One shrinks")
        self.play(fl.k.animate.set_value(45), run_time=self.t_of("on average") - 0.2 - self.elapsed(), rate_func=linear)
        lab_l = T("shrinks a little,\nsmall swings", 28).move_to([L.x0 + L.w / 2, 2.45, 0])
        self.play(FadeIn(lab_l), fl.k.animate.set_value(100), run_time=self.t_of("The other") - 0.2 - self.elapsed(), rate_func=linear)
        self.at("The other")
        self.play(fr.k.animate.set_value(60), run_time=self.t_of("but its numbers") - 0.2 - self.elapsed(), rate_func=linear)
        lab_r = T("grows a little,\nwild swings", 28).move_to([R.x0 + R.w / 2, 2.45, 0])
        self.play(FadeIn(lab_r), fr.k.animate.set_value(100), run_time=self.t_of("Both start") - 0.4 - self.elapsed(), rate_func=linear)
        self.at("Both start")
        tags = VGroup(*[VGroup(Dot(color=YELLOW).move_to([P.x0, P.Y(np.log(50)), 0]),
                               T("start: 50", 28, YELLOW).move_to([P.x0 + 1.1, P.Y(np.log(50)) - 0.75, 0])) for P in (L, R)])
        self.play(FadeIn(tags), run_time=0.8)
        self.play(*[Indicate(t[0], color=YELLOW, scale_factor=2) for t in tags], run_time=1.2)
        self.finish()


def base_world(scene, run_k=100, floor=True, rows=(0,), mu=0.01, sigma=0.2, n0=50, tm=100):
    P = main_panel(tm)
    b = P.base()
    f = P.floor_line()
    fan = Fan(P, list(rows), mu=mu, sigma=sigma, n0=n0, k=run_k, width=4, op=1) if len(rows) == 1 else Fan(P, list(rows), mu=mu, sigma=sigma, n0=n0, k=run_k)
    return P, b, f, fan


class S02Axes(Sc):
    def construct(self):
        P = main_panel()
        b = P.base()
        run = Fan(P, [pick_main()], mu=0.01, sigma=0.2, n0=50, k=0, width=4.5, op=1)
        self.play(Create(b), run_time=2.6)
        self.at("Each blue line")
        self.add(run)
        self.play(run.k.animate.set_value(100), run_time=self.t_of("The red dashed") - 0.3 - self.elapsed(), rate_func=linear)
        fl = P.floor_line()
        self.at("The red dashed")
        self.play(Create(fl), run_time=1.3)
        lab = T("floor", 34, RED, weight=BOLD).move_to([5.1, P.Y(FL) + 0.35, 0])
        self.at("is the floor")
        self.play(FadeIn(lab), run_time=0.6)
        self.at("a number too low")
        sub = T("too low to\nrecover from", 28).move_to([5.1, P.Y(FL) - 0.7, 0])
        self.play(FadeIn(sub), Indicate(fl, color=RED), run_time=1.4)
        self.finish()


class S03Trend(Sc):
    def construct(self):
        P = main_panel()
        b, fl = P.base(), P.floor_line()
        run = Fan(P, [pick_main()], mu=0.01, sigma=0.2, n0=50, k=100, width=4.5, op=1)
        lab_f = T("floor", 34, RED, weight=BOLD).move_to([5.1, P.Y(FL) + 0.35, 0])
        self.add(b, fl, run, lab_f)
        # a marker that rides the run
        ts = {"t": 0.0}
        dot = Dot(radius=0.13, color=YELLOW).set_z_index(6)

        def ride(m, dt):
            ts["t"] = (ts["t"] + dt * 9) % 100
            i = int(ts["t"])
            m.move_to([P.X(i), P.Y(run._x[0, i]), 0])
        dot.add_updater(ride)
        self.add(dot)
        self.at("The gold arrow")
        arrow = trend_arrow(P, run)
        self.play(GrowFromPoint(arrow, arrow.get_start()), run_time=1.6)
        self.at("the trend")
        t1 = T("trend", 34, GOLD, weight=BOLD).move_to([5.1, 1.7, 0])
        self.play(FadeIn(t1), run_time=0.5)
        self.at("the average yearly")
        t2 = T("average yearly\nchange on a\nlog scale", 28).move_to([5.1, 0.4, 0])
        self.play(FadeIn(t2), run_time=0.8)
        self.at("Around it")
        sg = 0.2
        ts_ = np.linspace(0, 100, 60)
        mid = np.log(50) + 0.01 * ts_
        up_, lo_ = mid + sg * np.sqrt(ts_), mid - sg * np.sqrt(ts_)
        pts = [[P.X(t), P.Y(v), 0] for t, v in zip(ts_, up_)] + [[P.X(t), P.Y(v), 0] for t, v in zip(ts_[::-1], lo_[::-1])]
        band = Polygon(*pts, stroke_width=0, fill_color=TEXT, fill_opacity=0.15)
        band.set_z_index(0)
        self.play(FadeOut(t2), FadeIn(band), run_time=1.0)
        band.add_updater(lambda m, dt: None)
        self.at("Those are the")
        sw = T("swings", 34, TEXT, weight=BOLD).move_to([5.1, -0.4, 0])
        self.play(FadeIn(sw), band.animate.set_fill(TEXT, 0.28), run_time=0.8)
        self.at("the good years")
        x = run._x[0, :101]
        ig, ib = int(np.argmax(x)), int(np.argmin(x))
        g = T("good year", 28, GREEN, weight=BOLD).move_to([P.X(ig), min(P.Y(x[ig]) + 0.55, 2.0), 0])
        g.set_x(min(max(g.get_x(), -4.6), 3.0))
        self.play(FadeIn(g), run_time=0.5)
        self.at("and bad")
        bd = T("bad year", 28, RED, weight=BOLD).move_to([P.X(ib), max(P.Y(x[ib]) - 0.55, P.Y(FL) + 0.5), 0])
        bd.set_x(min(max(bd.get_x(), -4.6), 3.0))
        self.play(FadeIn(bd), run_time=0.5)
        self.finish()


class S04Fan(Sc):
    def construct(self):
        P = main_panel()
        b, fl = P.base(), P.floor_line()
        lab_f = T("floor", 34, RED, weight=BOLD).move_to([5.1, P.Y(FL) + 0.35, 0])
        one = Fan(P, [pick_main()], mu=0.01, sigma=0.2, n0=50, k=100, width=4.5, op=1)
        self.add(b, fl, lab_f, one)
        fan = Fan(P, list(range(200)), mu=0.01, sigma=0.2, n0=50, k=0)
        self.at("200 times")
        self.play(FadeOut(one), run_time=0.4)
        self.add(fan)
        cnt = Live(lambda: f"{fan.count()} of 200", 34, YELLOW, True, [5.45, 2.0, 0], op=0)
        c2 = T("touched\nthe floor", 28).move_to([5.45, 0.9, 0])
        self.add(cnt)
        self.play(live_fade(cnt, 0, 1, 0.5), FadeIn(c2), fan.k.animate.set_value(30), run_time=self.t_of("The runs fan") - 0.2 - self.elapsed() - 0.0 if self.t_of("The runs fan") - 0.2 - self.elapsed() > 0.5 else 0.5, rate_func=linear)
        self.at("The runs fan")
        self.play(fan.k.animate.set_value(75), run_time=self.t_of("The fraction") - 0.3 - self.elapsed(), rate_func=linear)
        self.play(fan.k.animate.set_value(100), run_time=0.01 + max(0.3, self.t_of("The fraction") - self.elapsed()), rate_func=linear) if False else None
        self.at("The fraction")
        self.play(fan.k.animate.set_value(100), run_time=1.6, rate_func=linear)
        fr = Live(lambda: f"= {pct(fan.frac())}", 44, TEXT, True, [5.1, -0.5, 0])
        self.add(fr)
        self.at("is the risk")
        rk = T("the risk", 34, GOLD, weight=BOLD).move_to([5.1, -1.15, 0])
        self.play(FadeIn(rk), Indicate(fr, color=GOLD), run_time=1.0)
        self.finish()


class S05Pva(Sc):
    def construct(self):
        P = main_panel()
        b, fl = P.base(), P.floor_line()
        lab_f = T("floor", 34, RED, weight=BOLD).move_to([5.1, P.Y(FL) + 0.35, 0])
        fan = Fan(P, list(range(200)), mu=0.01, sigma=0.2, n0=50, k=100)
        cnt = Live(lambda: f"{fan.count()} of 200", 34, YELLOW, True, [5.45, 2.0, 0])
        c2 = T("touched\nthe floor", 28).move_to([5.45, 0.9, 0])
        fr = Live(lambda: f"= {pct(fan.frac())}", 44, TEXT, True, [5.1, -0.5, 0])
        rk = T("the risk", 34, GOLD, weight=BOLD).move_to([5.1, -1.15, 0])
        self.add(b, fl, lab_f, fan, cnt, c2, fr, rk)
        self.at("population viability")
        t1 = T("population viability analysis (PVA)", 34, GOLD, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeOut(VGroup(c2, rk)), FadeOut(cnt), FadeOut(fr), FadeIn(t1), run_time=1.0)
        self.at("analysis")
        d1 = T("fraction of runs that reach the floor in a chosen time", 28).move_to([0, 2.75, 0])
        self.play(FadeIn(d1), fan.k.animate.set_value(0), run_time=1.6)
        self.at("A real one")
        tag = T("a fuller model\nadds ages,\ncrowding,\ncatastrophes", 28).move_to([5.1, 0.4, 0])
        self.play(FadeIn(tag), run_time=0.8)
        self.at("many times")
        self.play(fan.k.animate.set_value(100), run_time=self.t_of("counts the runs") - 0.3 - self.elapsed(), rate_func=linear)
        self.at("counts the runs")
        cnt2 = Live(lambda: f"{fan.count()} of 200", 34, YELLOW, True, [5.45, 2.0, 0])
        self.add(cnt2)
        self.play(Indicate(fan, color=RED, scale_factor=1.0), run_time=1.5)
        self.finish()


class S06Dials(Sc):
    def construct(self):
        P = main_panel()
        b, fl = P.base(), P.floor_line()
        lab_f = T("floor", 34, RED, weight=BOLD).move_to([5.1, P.Y(FL) - 0.5, 0])
        fan = Fan(P, list(range(200)), mu=0.01, sigma=0.2, n0=50, k=100)
        cnt = Live(lambda: pct(fan.frac()), 48, YELLOW, True, [5.1, 2.8, 0])
        ct = T("touched\nthe floor", 28).move_to([6.0 - 0.1, 2.5, 0]) if False else T("touched\nthe floor", 28).move_to([5.1, 1.7, 0])
        self.add(b, fl, fan, cnt, ct)
        d1 = dial([4.3, 0.4, 0], 0.5, fan.sg, 0.1, 0.4)
        d2 = dial([4.3, -1.5, 0], 0.5, fan.n0, 30, 300)
        l1 = T("swings", 28).move_to([5.9, 0.4, 0])
        l2 = T("start", 28).move_to([5.9, -1.5, 0])
        self.at("Turn two dials")
        self.play(FadeIn(d1), FadeIn(l1), run_time=0.6)
        self.play(FadeIn(d2), FadeIn(l2), run_time=0.6)
        self.at("Widen the swings")
        self.play(fan.sg.animate.set_value(0.35), run_time=self.t_of("floor", 0) + 0 - self.elapsed() if False else 2.0, rate_func=smooth)
        self.at("Raise the start")
        self.play(fan.sg.animate.set_value(0.2), run_time=0.8)
        self.play(fan.n0.animate.set_value(200), run_time=2.0, rate_func=smooth)
        self.finish()


def trend_world(scene):
    L, R = split_panels()
    fl_ = Fan(L, list(range(200)), mu=0.01, sigma=0.2, n0=50, k=100)
    fr_ = Fan(R, list(range(200)), mu=0.01, sigma=0.2, n0=500, k=100)
    return L, R, fl_, fr_


class S07Predict(Sc):
    def construct(self):
        L, R, fa, fb = trend_world(self)
        mu = ValueTracker(0.01)
        fa.mu, fb.mu = mu, mu
        fb.mu = mu
        aL, aR = trend_arrow(L, fa), trend_arrow(R, fb)
        bL, bR = L.base(), R.base()
        fL, fR = L.floor_line(), R.floor_line()
        hL = T("start 50", 34, TEXT, weight=BOLD).move_to([L.x0 + L.w / 2, 2.35, 0])
        hR = T("start 500", 34, TEXT, weight=BOLD).move_to([R.x0 + R.w / 2, 2.35, 0])
        dl = dial([0, 3.2, 0], 0.5, mu, -0.03, 0.03, GOLD)
        self.add(bL, bR, fL, fR, fa, fb, hL, hR, aL, aR)
        self.play(FadeIn(dl), run_time=0.5)
        self.at("tilt the gold")
        self.play(mu.animate.set_value(-0.02), run_time=2.0, rate_func=smooth)
        tl = T("trend below zero", 28, GOLD).move_to([0, 2.4, 0])
        self.at("shrinks on average")
        self.play(FadeIn(tl), run_time=0.6)
        self.at("starting with")
        x10 = T("x10", 48, YELLOW, weight=BOLD).move_to([0, 0.6, 0])
        self.play(FadeIn(x10), Indicate(hR, color=YELLOW), run_time=1.0)
        self.play(fa.k.animate.set_value(0), fb.k.animate.set_value(0), run_time=max(0.5, self.narration_s - self.elapsed() - 0.3), rate_func=linear)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        L, R, fa, fb = trend_world(self)
        mu = ValueTracker(-0.02)
        fa.mu, fb.mu = mu, mu
        fa.k.set_value(0)
        fb.k.set_value(0)
        aL, aR = trend_arrow(L, fa), trend_arrow(R, fb)
        hL = T("start 50", 34, TEXT, weight=BOLD).move_to([L.x0 + L.w / 2, 2.35, 0])
        hR = T("start 500", 34, TEXT, weight=BOLD).move_to([R.x0 + R.w / 2, 2.35, 0])
        cap = T("Predict: does a tenfold bigger start\nsave a shrinking population?", 32, YELLOW, weight=BOLD).move_to([0, 3.35, 0])
        self.add(L.base(), R.base(), L.floor_line(), R.floor_line(), fa, fb, hL, hR, aL, aR)
        self.play(FadeIn(cap), run_time=0.5)
        tr = ValueTracker(5.0)
        cd = Live(lambda: str(max(1, int(np.ceil(tr.get_value())))), 64, YELLOW, True, [0, 0, 0])
        self.add(cd)
        self.play(tr.animate.set_value(0.01), run_time=4.4, rate_func=linear)
        self.finish()


class S09Reveal(Sc):
    def construct(self):
        L, R, fa, fb = trend_world(self)
        mu = ValueTracker(-0.02)
        fa.mu, fb.mu = mu, mu
        fa.k.set_value(0)
        fb.k.set_value(0)
        aL, aR = trend_arrow(L, fa), trend_arrow(R, fb)
        hL = T("start 50", 34, TEXT, weight=BOLD).move_to([L.x0 + L.w / 2, 2.35, 0])
        hR = T("start 500", 34, TEXT, weight=BOLD).move_to([R.x0 + R.w / 2, 2.35, 0])
        cL = Live(lambda: f"{pct(fa.frac())} touched the floor", 30, RED, False, [L.x0 + L.w / 2, 3.35, 0])
        cR = Live(lambda: f"{pct(fb.frac())} touched the floor", 30, RED, False, [R.x0 + R.w / 2, 3.35, 0])
        self.add(L.base(), R.base(), L.floor_line(), R.floor_line(), fa, fb, hL, hR, aL, aR, cL, cR)
        self.play(fa.k.animate.set_value(100), fb.k.animate.set_value(100), run_time=self.t_of("But keep") - 0.3, rate_func=linear)
        self.at("But keep")
        t0 = self.elapsed()
        d = self.t_of("nearly every run") - t0
        self.play(L.tm.animate.set_value(1000), R.tm.animate.set_value(1000), run_time=2.4, rate_func=smooth) if False else None
        self.play(L.tm.animate.set_value(1000), R.tm.animate.set_value(1000),
                  fa.k.animate.set_value(1000), fb.k.animate.set_value(1000), run_time=max(3.0, self.narration_s - t0 - 0.8), rate_func=linear)
        self.finish()


class S10Time(Sc):
    def construct(self):
        P = main_panel(1000)
        b, fl = P.base(), P.floor_line()
        lab_f = T("floor", 34, RED, weight=BOLD).move_to([5.1, P.Y(FL) - 0.5, 0])
        fan = Fan(P, list(range(200)), mu=-0.02, sigma=0.2, n0=500, k=0)
        arrow = trend_arrow(P, fan)
        cnt = Live(lambda: pct(fan.frac()), 48, YELLOW, True, [5.1, 2.8, 0])
        ct = T("touched\nthe floor", 28).move_to([6.0, 2.5, 0]) if False else T("touched\nthe floor", 28).move_to([5.1, 1.7, 0])
        self.add(b, fl, fan, cnt, ct)
        self.at("bought time")
        self.play(fan.k.animate.set_value(300), run_time=self.t_of("bought time") + 0.0 - self.elapsed() + 0.01 if False else 1.0, rate_func=linear)
        ban = T("size buys time", 36, GOLD, weight=BOLD).move_to([-1.0, 3.3, 0])
        self.play(FadeIn(ban), fan.k.animate.set_value(450), run_time=1.5, rate_func=linear)
        self.at("With the arrow")
        self.add(arrow)
        self.play(fan.k.animate.set_value(1000), run_time=self.t_of("every start") - 0.3 - self.elapsed(), rate_func=linear)
        self.at("every start")
        self.play(Indicate(fan, color=RED, scale_factor=1.0), run_time=1.5)
        self.at("How soon")
        dT = dial([4.3, 0.3, 0], 0.4, fan.mu, -0.03, 0.03, GOLD)
        dS = dial([4.3, -0.9, 0], 0.4, fan.n0, 30, 600)
        dW = dial([4.3, -2.1, 0], 0.4, fan.sg, 0.1, 0.4)
        lT, lS, lW = [T(x, 28).move_to([5.8, y, 0]) for x, y in (("trend", 0.3), ("start", -0.9), ("swings", -2.1))]
        self.at("the trend")
        self.play(FadeIn(dT), FadeIn(lT), FadeOut(ct), run_time=0.6)
        self.at("the start and")
        self.play(FadeIn(dS), FadeIn(lS), fan.n0.animate.set_value(50), run_time=1.4)
        self.at("swings together")
        self.play(FadeIn(dW), FadeIn(lW), fan.sg.animate.set_value(0.24), run_time=1.0)
        self.play(fan.sg.animate.set_value(0.2), run_time=0.8)
        self.at("Tilt it up")
        self.play(fan.mu.animate.set_value(0.02), run_time=2.0, rate_func=smooth)
        self.at("most runs")
        tg = T("trend +0.02:\nmost runs stay clear", 28, GREEN, weight=BOLD).move_to([-0.5, 3.25, 0])
        self.play(FadeOut(ban), run_time=0.4)
        self.play(FadeIn(tg), run_time=0.5)
        self.finish()


class S11Small(Sc):
    def construct(self):
        P = Panel(-5.4, -3.0, 9.0, 5.3, tm=100, yticks=False)
        import types
        # zoomed chart: ln numbers 1..4.5 mapped over the panel height
        P.Y = types.MethodType(lambda s, l: s.y0 + s.h * (min(max(l, 1.0), 4.5) - 1.0) / 3.5, P)
        row, hit = 0, 0
        for r in range(200):
            x = np.log(50) - 0.02 * np.arange(1, 1001) + 0.2 * np.cumsum(Z[r])
            below = np.where(x <= FL)[0]
            if len(below) and 40 < below[0] + 1 < 90:
                row, hit = r, int(below[0] + 1)
                break
        xs = np.concatenate([[np.log(50)], np.log(50) + np.cumsum(-0.02 + 0.2 * Z[row])])
        end = min(hit, 100)
        kt = ValueTracker(0)
        run = VMobject()

        def upd(m):
            i = int(kt.get_value())
            idx = np.arange(0, i + 1)
            v = xs[idx].copy()
            if i >= hit:
                v[-1] = FL
            pts = np.stack([P.x0 + P.w * idx / 100, P.y0 + P.h * (np.clip(v, 1.0, 4.5) - 1.0) / 3.5, np.zeros(len(idx))], axis=1)
            if len(pts) < 2:
                pts = np.vstack([pts, pts])
            m.set_points_as_corners(pts)
            m.set_stroke(RED if i >= hit else BLUE, 5, 1)
            m.set_fill(opacity=0)
        run.add_updater(upd)
        upd(run)
        b = P.base()
        fl = P.floor_line()
        lab_f = T("floor", 34, RED, weight=BOLD).move_to([5.1, P.Y(FL) + 0.35, 0])
        self.add(b, fl, lab_f, run)
        # animal icons near the dive
        cx = P.x0 + P.w * (hit - 18) / 100
        cy = P.Y(FL) + 1.0
        icons = VGroup(*[Circle(radius=0.17, stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.9).move_to([cx + (i % 4) * 0.5, cy + (i // 4) * 0.5, 0]) for i in range(8)])
        self.at("few animals")
        self.play(FadeIn(icons), kt.animate.set_value(max(1, hit - 25)), run_time=1.4, rate_func=linear)
        self.at("one unlucky litter")
        self.play(*[FadeOut(icons[i]) for i in (1, 4, 6)], kt.animate.set_value(hit), run_time=1.6, rate_func=linear)
        self.at("So chance")
        lab = T("chance in single\nbirths and deaths", 24).move_to([5.3, 0.9, 0])
        self.play(FadeIn(lab), run_time=0.7)
        self.at("weighs most")
        fn = T("icons are schematic;\ncomputed runs keep\nswings steady", 24).move_to([5.1, -1.3, 0]) if False else None
        for k, i in enumerate((1, 4, 6, 0, 3)):
            if i in (1, 4, 6):
                self.play(FadeIn(icons[i]), run_time=0.4)
            else:
                self.play(FadeOut(icons[i]), run_time=0.4)
        fn = T("icons: schematic", 24).move_to([5.1, 2.4, 0])
        self.play(FadeIn(fn), run_time=0.5)
        for i in (2, 5, 7):
            self.play(FadeOut(icons[i]), run_time=0.5)
            self.play(FadeIn(icons[i]), run_time=0.5)
        self.finish()


class S12Vortex(Sc):
    def construct(self):
        mu = ValueTracker(0.0)
        ang = ValueTracker(-5.0)
        cx, cy = 5.0, 0.3
        needle = Arrow(ORIGIN, RIGHT, buff=0, color=GOLD, stroke_width=8)

        def up(m):
            a = np.radians(ang.get_value())
            m.become(Arrow([cx - 1.0 * np.cos(a), cy - 1.0 * np.sin(a), 0], [cx + 1.0 * np.cos(a), cy + 1.0 * np.sin(a), 0], buff=0, color=GOLD, stroke_width=8))
        needle.add_updater(up)
        up(needle)
        tl = T("trend", 34, GOLD, weight=BOLD).move_to([5.0, 2.0, 0])
        self.add(needle, tl)
        gn = chip("genes", TEAL, 34).move_to([5.0, -1.6, 0])
        self.at("Genes can")
        self.play(FadeIn(gn), run_time=0.6)
        self.at("tilt the arrow")
        self.play(ang.animate.set_value(-20), run_time=1.4)
        cxs = {"A": [-3.7, 2.2], "B": [1.3, 2.2], "C": [1.3, -2.3], "D": [-3.7, -2.3]}
        A = chip("fewer animals", RED, 28).move_to([*cxs["A"], 0])
        B = chip("more inbreeding", TEAL, 28).move_to([*cxs["B"], 0])
        C = chip("lower survival\nand fertility", YELLOW, 28).move_to([*cxs["C"], 0])
        D = chip("trend tilts down", GOLD, 28).move_to([*cxs["D"], 0])

        def arr(a, b):
            return Arrow(a.get_center(), b.get_center(), buff=0.95 if False else 0.0, color=TEXT, stroke_width=5).put_start_and_end_on(*self._edge(a, b))
        self.at("Fewer animals")
        self.play(FadeOut(gn), FadeIn(A), run_time=0.8)
        self.at("more mating")
        ab = self._arr(A, B)
        self.play(GrowArrow(ab), FadeIn(B), run_time=1.0)
        self.at("Inbreeding can")
        bc = self._arr(B, C)
        self.play(GrowArrow(bc), FadeIn(C), run_time=1.0)
        trav = Dot(radius=0.16, color=YELLOW).set_z_index(-1)
        path = [A.get_center(), B.get_center(), C.get_center(), D.get_center()]
        st = {"p": 0.0}

        def run(m, dt):
            st["p"] = (st["p"] + dt / 3.0) % 4
            i = int(st["p"])
            f = st["p"] - i
            m.move_to(path[i] * (1 - f) + path[(i + 1) % 4] * f)
        trav.add_updater(run)
        trav.move_to(path[0])
        self.add(trav)
        self.at("so the trend")
        cd = self._arr(C, D)
        self.play(GrowArrow(cd), FadeIn(D), ang.animate.set_value(-40), run_time=1.2)
        self.at("numbers fall")
        da = self._arr(D, A)
        self.play(GrowArrow(da), ang.animate.set_value(-58), run_time=1.4)
        self.at("This loop")
        ev = T("extinction vortex", 34, RED, weight=BOLD).move_to([-1.2, 0, 0])
        self.play(FadeIn(ev), ang.animate.set_value(-78), run_time=2.0)
        self.finish()

    def _arr(self, a, b):
        pa, pb = a.get_center(), b.get_center()
        d = (pb - pa) / np.linalg.norm(pb - pa)

        def edge(m, p, q):
            dx, dy = abs(q[0] - p[0]), abs(q[1] - p[1])
            t = min((m.width / 2 + 0.15) / max(dx, 1e-6), (m.height / 2 + 0.15) / max(dy, 1e-6))
            return p + (q - p) * t
        return Arrow(edge(a, pa, pb), edge(b, pb, pa), buff=0, color=TEXT, stroke_width=5)


class S13Answer(Sc):
    def construct(self):
        L, R = split_panels()
        one_l = Fan(L, [0], mu=-0.01, sigma=0.05, n0=50, k=100, width=5, op=1)
        one_r = Fan(R, [pick_right()], mu=0.01, sigma=0.25, n0=50, k=100, width=5, op=1)
        hL = T("trend below zero,\nsmall swings", 28).move_to([L.x0 + L.w / 2, 2.5, 0])
        hR = T("trend above zero,\nwild swings", 28).move_to([R.x0 + R.w / 2, 2.5, 0])
        self.add(L.base(), R.base(), one_l, one_r, hL, hR)
        self.play(FadeIn(L.floor_line()), FadeIn(R.floor_line()), run_time=1.0)
        fa = Fan(L, list(range(200)), mu=-0.01, sigma=0.05, n0=50, k=0)
        fb = Fan(R, list(range(200)), mu=0.01, sigma=0.25, n0=50, k=0)
        self.at("The shrinking one")
        self.play(FadeOut(one_l), FadeOut(one_r), L.tm.animate.set_value(1000), R.tm.animate.set_value(1000), run_time=0.8)
        self.add(fa, fb)
        cL = Live(lambda: f"{pct(fa.frac())} touched the floor", 30, RED, False, [L.x0 + L.w / 2, 3.5, 0])
        cR = Live(lambda: f"{pct(fb.frac())} touched the floor", 30, RED, False, [R.x0 + R.w / 2, 3.5, 0])
        self.add(cL, cR)
        self.play(fa.k.animate.set_value(500), fb.k.animate.set_value(500), run_time=self.t_of("however big") - 0.3 - self.elapsed(), rate_func=linear)
        self.at("however big")
        tg1 = T("fix the trend, add numbers", 28, GOLD, weight=BOLD).move_to([L.x0 + L.w / 2, -3.55, 0])
        self.play(FadeIn(tg1), fa.k.animate.set_value(850), fb.k.animate.set_value(750), run_time=self.t_of("The growing") - 0.3 - self.elapsed(), rate_func=linear)
        self.at("The growing")
        self.play(fa.k.animate.set_value(1000), fb.k.animate.set_value(1000), run_time=2.2, rate_func=linear)
        self.at("Its risk")
        tg2 = T("trend, numbers and swings together", 28, GOLD, weight=BOLD).move_to([R.x0 + R.w / 2, -3.55, 0])
        tg2.set_x(min(tg2.get_x(), 6.8 - tg2.width / 2))
        self.play(FadeIn(tg2), Indicate(fb, color=BLUE, scale_factor=1.0), run_time=1.2)
        self.finish()


class S14Mvp(Sc):
    def construct(self):
        P = main_panel()
        b, fl = P.base(), P.floor_line()
        lab_f = T("floor", 34, RED, weight=BOLD).move_to([5.1, P.Y(FL) - 0.5, 0]) if False else None
        fan = Fan(P, list(range(200)), mu=0.01, sigma=0.2, n0=50, k=100)
        target = 0.10
        mvp = 50
        for n in range(50, 800, 10):
            x = np.log(n) + np.cumsum(0.01 + 0.2 * Z[:, :100], axis=1)
            if (x.min(axis=1) <= FL).mean() <= target:
                mvp = n
                break
        gx, gy0, gh, gw = 3.95, -1.9, 3.4, 0.7
        gbox = Rectangle(width=gw, height=gh, stroke_color=TEXT, stroke_width=3).move_to([gx, gy0 + gh / 2, 0])
        gfill = Rectangle(width=gw, height=0.01, stroke_width=0, fill_color=RED, fill_opacity=0.7)

        def gup(m):
            h = max(0.01, min(1.0, fan.frac() / 0.5) * gh)
            m.become(Rectangle(width=gw, height=h, stroke_width=0, fill_color=GREEN if fan.frac() <= target else RED, fill_opacity=0.7).move_to([gx, gy0 + h / 2, 0]))
        gfill.add_updater(gup)
        gup(gfill)
        ty = gy0 + gh * target / 0.5
        tline = DashedLine([gx - 0.6, ty, 0], [gx + 1.8, ty, 0], color=YELLOW, stroke_width=4)
        tlab = T("chosen risk,\nchosen time", 28, YELLOW).move_to([5.65, ty + 0.75, 0])
        rl = Live(lambda: pct(fan.frac()), 44, TEXT, True, [4.55, 2.1, 0])
        sl = Live(lambda: f"start {int(round(fan.n0.get_value()))}", 34, YELLOW, False, [5.4, 2.1, 0] if False else [4.9, 2.9, 0])
        self.add(b, fl, fan)
        self.at("a target")
        self.play(FadeIn(gbox), FadeIn(gfill), FadeIn(tline), FadeIn(tlab), run_time=1.0)
        self.add(rl)
        self.at("one population")
        self.add(sl)
        self.play(fan.n0.animate.set_value(60), run_time=1.0)
        self.at("A minimum")
        self.play(fan.n0.animate.set_value(mvp), run_time=self.t_of("keeps the risk") - 0.3 - self.elapsed() + 0.8, rate_func=smooth)
        self.at("below a chosen")
        tag = T(f"minimum viable\npopulation (MVP): {mvp}", 28, GREEN, weight=BOLD).move_to([-1.0, 3.2, 0])
        self.play(FadeIn(tag), Indicate(gfill, color=GREEN), run_time=1.0)
        self.at("over a chosen")
        br = T("over 100 years", 28, TEXT).move_to([-0.9, -3.65 + 0.0, 0]) if False else None
        self.play(Indicate(P.base()[1] if False else tline, color=YELLOW), run_time=1.5)
        self.finish()


class S15Rule(Sc):
    def construct(self):
        P = Panel(-6.2, -3.0, 7.4, 5.3, tm=1000)
        P.yticks = False
        b, fl = P.base(), P.floor_line()
        fan = Fan(P, list(range(200)), mu=-0.02, sigma=0.2, n0=50, k=1000)
        arrow = trend_arrow(P, fan)
        self.add(b, fl, fan, arrow)
        c1 = T("1. Find and remove\nthe cause of decline", 28, GOLD, weight=BOLD).move_to([4.4, 2.2, 0])
        self.at("removing the cause")
        self.play(FadeIn(c1), fan.mu.animate.set_value(0.01), run_time=2.6, rate_func=smooth)
        self.at("Alongside it")
        l1 = T("2. Alongside:", 28, TEXT, weight=BOLD).move_to([4.4, 0.7, 0])
        l1.set_x(2.2 + l1.width / 2)
        self.play(FadeIn(l1), run_time=0.5)
        ls = []
        for ph, txt, y in (("numbers", "numbers", 0.2), ("connections", "connections", -0.3), ("genes", "genes", -0.8)):
            self.at(ph)
            t = T(txt, 28, TEAL, weight=BOLD)
            t.move_to([0, y, 0]).set_x(2.7 + t.width / 2)
            ls.append(t)
            self.play(FadeIn(t), run_time=0.4)
        self.at("lift the trend")
        self.play(fan.mu.animate.set_value(0.02), run_time=2.0, rate_func=smooth)
        fn = T("In this model, without\na trend above zero,\nsize only buys time.", 28, GOLD).move_to([4.4, -2.3, 0])
        self.at("But in this")
        self.play(FadeIn(fn), run_time=0.8)
        self.at("without a trend")
        self.play(fan.mu.animate.set_value(-0.02), run_time=1.6, rate_func=smooth)
        self.at("size only")
        self.play(fan.n0.animate.set_value(500), run_time=1.6, rate_func=smooth)
        self.finish()


class S16End(EndCard):
    LINE = "In this model, without a trend above zero, size only buys time."
