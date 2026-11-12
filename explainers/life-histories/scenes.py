"""Life histories, film 1: One budget, many uses.

COLOUR MAP (same in both films and on the page)
  intake A  = dark bar with a light outline (the "black" bar on this dark ground)
  GOLD      = reproduction R        TEAL = self S (growth, upkeep, storage)
  GREY      = trend lines, labels   axes: horizontal = R (gold), vertical = S (teal)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

INK = "#232834"
BIRD_C = "#C9B28F"
SALMON_C = "#F08A7A"
SEED_C = "#E6D5A8"
TEAL2, TEAL3 = "#2E8F96", "#7FD6DB"
SNOW = "#BFE3F5"

# shared geometry (every scene that carries the trade-off picture rebuilds it here)
BX0, BW, BH = -6.0, 12.0, 1.1
O = np.array([-2.0, -3.3, 0.0])
L = 3.3


def P(x, y):
    return np.array([x, y, 0.0])


def songbird(s=1.0, color=BIRD_C):
    body = Ellipse(width=1.1, height=0.62, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    head = Circle(radius=0.21, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8).move_to(P(0.5, 0.26))
    beak = Polygon(P(0.68, 0.30), P(0.92, 0.24), P(0.68, 0.18), stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    tail = Polygon(P(-0.45, 0.05), P(-0.95, 0.3), P(-0.95, -0.12), stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    eye = Dot(P(0.56, 0.30), radius=0.04, color=BG)
    return VGroup(tail, body, head, beak, eye).scale(s)


def salmon(s=1.0):
    body = Ellipse(width=1.5, height=0.55, stroke_color=SALMON_C, stroke_width=3, fill_color=SALMON_C, fill_opacity=0.85)
    tail = Polygon(P(-0.65, 0.0), P(-1.15, 0.3), P(-1.15, -0.3), stroke_color=SALMON_C, stroke_width=3, fill_color=SALMON_C, fill_opacity=0.85)
    fin = Polygon(P(0.0, 0.25), P(-0.25, 0.5), P(0.2, 0.28), stroke_color=SALMON_C, stroke_width=2, fill_color=SALMON_C, fill_opacity=0.6)
    eye = Dot(P(0.5, 0.08), radius=0.045, color=BG)
    return VGroup(tail, fin, body, eye).scale(s)


def chick(x=0, y=0, r=0.12):
    return Circle(radius=r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.9).move_to(P(x, y))


def snowflake(s=0.4):
    g = VGroup(*[Line(ORIGIN, s * np.array([np.cos(a), np.sin(a), 0]), color=SNOW, stroke_width=4)
                 for a in np.arange(0, PI, PI / 3)])
    for a in np.arange(0, PI, PI / 3):
        g.add(Line(-s * np.array([np.cos(a), np.sin(a), 0]), ORIGIN, color=SNOW, stroke_width=4))
    return g


def idle(m, amp=0.06, speed=1.7, phase=0.0):
    """Gentle bob so a held picture is never frozen."""
    m._tt = phase
    m._off = 0.0

    def up(mob, dt):
        mob._tt += dt
        new = amp * np.sin(speed * mob._tt)
        mob.shift(UP * (new - mob._off))
        mob._off = new
    m.add_updater(up)
    return m


def bar_group(r, y=1.8, x0=BX0, w=BW, h=BH):
    teal = Rectangle(width=max(w * (1 - r), 0.01), height=h, stroke_width=0, fill_color=TEAL, fill_opacity=0.9)
    teal.move_to(P(x0 + w * (1 - r) / 2, y))
    gold = Rectangle(width=max(w * r, 0.01), height=h, stroke_width=0, fill_color=GOLD, fill_opacity=0.9)
    gold.move_to(P(x0 + w * (1 - r) + w * r / 2, y))
    out = Rectangle(width=w, height=h, stroke_color=TEXT, stroke_width=3).move_to(P(x0 + w / 2, y))
    return VGroup(teal, gold, out)


def axes_group(O=O, L=L, words=True):
    xa = Arrow(O, O + P(L + 0.4, 0), buff=0, color=GOLD, stroke_width=5, tip_length=0.2)
    ya = Arrow(O, O + P(0, L + 0.4), buff=0, color=TEAL, stroke_width=5, tip_length=0.2)
    g = VGroup(xa, ya)
    if words:
        g.add(T("reproduction R", 28, GOLD).move_to(O + P(L + 0.55 + 1.55, 0)),
              T("self S", 28, TEAL).move_to(O + P(1.0, L + 0.3)))
    return g


def tline(O=O, L=L):
    return Line(O + P(0, L), O + P(L, 0), color=GREY, stroke_width=5)


def tpoint(r, O=O, L=L):
    return O + P(r * L, (1 - r) * L)


def slider_handle(r, y, x0=BX0, w=BW):
    return Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1, stroke_width=1).scale(0.17).move_to(P(x0 + w * (1 - r), y))


class SB(SpokenScene):
    def until(self, t):
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


class S00Title(TitleCard):
    LESSON = "Life histories and trade-offs"
    TITLE = "One Budget, Many Uses"


# ----------------------------------------------------------------------------------------
class S01Question(SB):
    def construct(self):
        y1, y2, x0 = 2.1, -1.7, -6.0
        l1 = Line(P(x0, y1), P(x0 + 0.01, y1), color=GREY, stroke_width=5)
        s = salmon(1.3).move_to(P(x0 + 0.5, y1 + 0.55))
        lab1 = T("salmon", 32, SALMON_C).move_to(P(-5.0, y1 + 1.35))
        self.play(FadeIn(s), FadeIn(lab1), run_time=0.5)
        self.at("swims")
        xe = 2.2
        self.play(s.animate.move_to(P(xe, y1 + 0.55)),
                  Transform(l1, Line(P(x0, y1), P(xe, y1), color=GREY, stroke_width=5)),
                  run_time=1.9, rate_func=linear)
        self.at("spawns")
        m = Dot(P(1.5, y1), radius=0.3, color=GOLD)
        ring = Circle(radius=0.3, color=GOLD, stroke_width=4).move_to(m)
        once = T("once", 32, GOLD).move_to(P(1.5, y1 - 0.75))
        self.play(FadeIn(m, scale=0.4), Succession(Wait(0.1), ring.animate.scale(2.2).set_opacity(0)), FadeIn(once), run_time=0.9)
        self.at("and dies")
        end = Line(P(xe + 0.4, y1 - 0.4), P(xe + 0.4, y1 + 0.4), color=TEXT, stroke_width=6)
        self.play(l1.animate.put_start_and_end_on(P(x0, y1), P(xe + 0.4, y1)), Create(end),
                  s.animate.rotate(-0.6).set_opacity(0.35).shift(RIGHT * 0.5), run_time=1.2)
        # songbird
        l2 = Line(P(x0, y2), P(x0 + 0.01, y2), color=GREY, stroke_width=5)
        b = songbird(1.4).move_to(P(x0 + 0.6, y2 + 0.55))
        lab2 = T("songbird", 32, BIRD_C).move_to(P(-5.0, y2 - 1.2))
        self.at("A songbird", nth=0) if False else None
        self.add(l2)
        l2.add_updater(lambda m_: m_.put_start_and_end_on(P(x0, y2), P(max(b.get_x() - 0.0, x0 + 0.01), y2)))
        self.until(4.3)
        self.play(FadeIn(b), FadeIn(lab2), run_time=0.4)
        xs = [-4.4, -2.6, -0.8, 1.0, 2.8, 4.6]
        self.at("nests")
        for i, x in enumerate(xs):
            self.play(b.animate.move_to(P(x, y2 + 0.55)), run_time=0.35, rate_func=linear)
            mk = Dot(P(x, y2), radius=0.24, color=GOLD)
            sp = T(f"spring {i+1}", 24, GREY).move_to(P(x, y2 - 0.7))
            self.play(FadeIn(mk, scale=0.4), FadeIn(sp), run_time=0.2)
        self.play(b.animate.move_to(P(5.4, y2 + 0.55)), run_time=0.5, rate_func=linear)
        l2.clear_updaters()
        self.at("natural selection")
        ns = T("natural selection", 34, TEXT).move_to(P(0, 0.2))
        self.play(FadeIn(ns), run_time=0.5)
        self.at("So how can both")
        q = T("?", 150, GREY, weight=BOLD).move_to(P(0, 0.2))
        self.play(FadeOut(ns), FadeIn(q, scale=0.5), run_time=0.6)
        self.play(q.animate.scale(1.15), run_time=1.0, rate_func=there_and_back)
        self.play(q.animate.scale(1.15), run_time=1.0, rate_func=there_and_back)
        self.finish()


# ----------------------------------------------------------------------------------------
BANDS = [2.8, 4.0, 2.4, 2.8]
BCOL = [TEAL, TEAL2, TEAL3, GOLD]


def s02_objects():
    BY = 1.0
    bird = songbird(1.7).move_to(P(-4.6, -1.9))
    seeds_ground = VGroup(*[Dot(P(x, -2.55), radius=0.07, color=SEED_C) for x in np.linspace(-3.4, -1.0, 9)])
    return BY, bird, seeds_ground


def seed_stream(BY):
    seeds = VGroup(*[Dot(radius=0.08, color=SEED_C) for _ in range(6)])
    for i, d in enumerate(seeds):
        d._ph = i / 6.0
        d._x = -3.2 + 0.4 * i

    def up(g, dt):
        g._t = getattr(g, "_t", 0.0) + dt
        for d in g:
            p = (g._t * 0.3 + d._ph) % 1.0
            d.move_to(P(d._x + 0.5 * np.sin(p * 3), -2.4 + p * (BY - 0.5 + 2.4 - 0.0)))
            d.set_opacity(min(1, p * 5, (1 - p) * 5))
    seeds.add_updater(up)
    return seeds


class S02Budget(SB):
    def construct(self):
        BY, bird, ground = s02_objects()
        idle(bird, 0.05)
        outline = Rectangle(width=BW, height=BH, stroke_color=TEXT, stroke_width=3).move_to(P(0, BY))
        fill = Rectangle(width=0.01, height=BH, stroke_width=0, fill_color=INK, fill_opacity=1).move_to(P(BX0, BY))
        self.add(fill, outline)
        self.play(FadeIn(bird), FadeIn(ground), run_time=0.8)
        seeds = seed_stream(BY)
        self.add(seeds)
        self.at("Treat what it takes in")
        title = T("intake (A): one budget", 34, TEXT).move_to(P(0, 3.35))
        self.play(FadeIn(title), fill.animate.stretch_to_fit_width(BW).move_to(P(0, BY)), run_time=2.4)
        sch = T("schematic", 22, GREY).move_to(P(5.6, -3.55))
        self.play(FadeIn(sch), run_time=0.3)
        self.at("four uses")
        x = BX0
        segs, labs = [], []
        names = ["growth", "upkeep", "storage", "reproduction"]
        for i, (w, c) in enumerate(zip(BANDS, BCOL)):
            seg = Rectangle(width=w, height=BH, stroke_color=BG, stroke_width=2, fill_color=c, fill_opacity=0.9).move_to(P(x + w / 2, BY))
            lab = T(names[i], 30, c if i in (0, 3) else TEAL)
            lab.move_to(P(x + w / 2, 2.55))
            if i == 1:
                sub = T("maintenance and repair", 22, TEAL)
                lab = VGroup(lab, sub.next_to(lab, DOWN, buff=0.08))
                lab.move_to(P(x + w / 2, 2.35))
            segs.append(seg)
            labs.append(lab)
            x += w
        # the narrator says growth in the gap after "uses"
        self.until(11.0)
        self.play(FadeIn(segs[0]), FadeIn(labs[0], shift=DOWN * 0.15), run_time=0.7)
        self.at("Upkeep")
        self.play(FadeIn(segs[1]), FadeIn(labs[1][0], shift=DOWN * 0.15), run_time=0.7)
        self.at("maintenance")
        self.play(FadeIn(labs[1][1]), run_time=0.5)
        self.at("Storage")
        self.play(FadeIn(segs[2]), FadeIn(labs[2], shift=DOWN * 0.15), run_time=0.7)
        self.at("And reproduction")
        self.play(FadeIn(segs[3]), FadeIn(labs[3], shift=DOWN * 0.15), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------
class S03Tradeoff(SB):
    def construct(self):
        BY, bird, ground = s02_objects()
        idle(bird, 0.05)
        self.add(bird, ground, seed_stream(BY))
        outline = Rectangle(width=BW, height=BH, stroke_color=TEXT, stroke_width=3).move_to(P(0, BY))
        x = BX0
        segs, labs = VGroup(), VGroup()
        names = ["growth", "upkeep", "storage", "reproduction"]
        for i, (w, c) in enumerate(zip(BANDS, BCOL)):
            seg = Rectangle(width=w, height=BH, stroke_color=BG, stroke_width=2, fill_color=c, fill_opacity=0.9).move_to(P(x + w / 2, BY))
            segs.add(seg)
            if i != 1:
                labs.add(T(names[i], 30, c if i in (0, 3) else TEAL).move_to(P(x + w / 2, 2.55)))
            else:
                labs.add(VGroup(T("upkeep", 30, TEAL), T("maintenance and repair", 22, TEAL)).arrange(DOWN, buff=0.08).move_to(P(x + w / 2, 2.35)))
            x += w
        title = T("intake (A): one budget", 34, TEXT).move_to(P(0, 3.35))
        sch = T("schematic", 22, GREY).move_to(P(5.6, -3.55))
        self.add(segs, labs, outline, title, sch)
        self.at("Lump")
        merged = Rectangle(width=9.2, height=BH, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to(P(BX0 + 4.6, BY))
        selfl = T("self (S)", 32, TEAL).move_to(P(BX0 + 4.6, 2.55))
        self.play(FadeOut(labs[0]), FadeOut(labs[1]), FadeOut(labs[2]), FadeOut(title),
                  ReplacementTransform(VGroup(segs[0], segs[1], segs[2]), merged), run_time=1.6)
        self.play(FadeIn(selfl, shift=DOWN * 0.15), run_time=0.5)
        self.at("Reproduction stays gold")
        self.play(Indicate(segs[3], color=GOLD, scale_factor=1.05), Indicate(labs[3], color=GOLD), run_time=1.3)
        self.at("For this one bird")
        # move the budget up, bring in the axes
        grp = VGroup(merged, segs[3], outline, selfl, labs[3])
        self.play(grp.animate.shift(UP * 0.8), FadeOut(bird), FadeOut(ground), FadeOut(sch), run_time=1.0)
        # swap in the live bar
        r = ValueTracker(2.8 / 12)
        bar = always_redraw(lambda: bar_group(r.get_value()))
        self.add(bar)
        self.remove(merged, segs[3], outline)
        # the live bar has no seeds stream now; the stream mob was removed with fade? ensure gone
        for m in list(self.mobjects):
            if isinstance(m, VGroup) and len(m) == 6 and all(isinstance(d, Dot) for d in m):
                self.remove(m)
        ax = axes_group()
        self.play(Create(ax[0]), Create(ax[1]), FadeIn(ax[2]), FadeIn(ax[3]), run_time=1.2)
        self.at("gold plus teal")
        eq = M("R + S = A", 40, TEXT).move_to(P(4.6, -1.0))
        self.play(FadeIn(eq, shift=LEFT * 0.2), run_time=0.8)
        self.at("So more gold")
        line = tline()
        dot = always_redraw(lambda: Dot(tpoint(r.get_value()), radius=0.17, color=TEXT))
        hnd = always_redraw(lambda: slider_handle(r.get_value(), 0.95))
        track = Line(P(BX0, 0.95), P(BX0 + BW, 0.95), color=GREY, stroke_width=3)
        self.play(Create(line), FadeIn(track), FadeIn(dot), FadeIn(hnd), run_time=0.8)
        self.play(r.animate.set_value(0.7), run_time=2.0, rate_func=smooth)
        self.play(r.animate.set_value(0.35), run_time=1.0, rate_func=smooth)
        self.at("That negative link")
        tl = T("trade-off line", 30, GREY).move_to(P(3.6, -2.2)).rotate(0)
        self.play(FadeIn(tl), run_time=0.5)
        self.play(r.animate.set_value(0.6), run_time=1.2, rate_func=smooth)
        self.play(r.animate.set_value(2.8 / 12 + 0.07), run_time=1.5, rate_func=smooth)
        self.finish()


# ----------------------------------------------------------------------------------------
class S04Two(SB):
    def construct(self):
        r = ValueTracker(0.3)
        bar = always_redraw(lambda: bar_group(r.get_value()))
        selfl = T("self (S)", 32, TEAL).move_to(P(BX0 + 4.0, 3.2))
        repl = T("reproduction (R)", 32, GOLD).move_to(P(4.1, 3.2))
        ax = axes_group()
        line = tline()
        dot = always_redraw(lambda: Dot(tpoint(r.get_value()), radius=0.17, color=TEXT))
        hnd = always_redraw(lambda: slider_handle(r.get_value(), 0.95))
        track = Line(P(BX0, 0.95), P(BX0 + BW, 0.95), color=GREY, stroke_width=3)
        self.add(bar, selfl, repl, ax, line, dot, hnd, track)
        self.wait(1.0)
        self.play(r.animate.set_value(0.45), run_time=1.0)
        self.play(r.animate.set_value(0.3), run_time=0.8)
        self.at("First")
        l1 = VGroup(T("this year's young", 30, GOLD), T("vs parent's own future", 30, TEAL)).arrange(DOWN, buff=0.12).move_to(P(4.6, 0.0))
        self.play(FadeIn(l1, shift=LEFT * 0.3), run_time=0.6)
        self.play(r.animate.set_value(0.2), run_time=1.0)
        self.at("What a parent spends")
        self.play(r.animate.set_value(0.55), run_time=2.6, rate_func=smooth)
        self.play(r.animate.set_value(0.3), run_time=1.2)
        self.at("Second")
        self.play(FadeOut(l1), run_time=0.4)
        cx = BX0 + BW * 0.7 + BW * 0.3 / 2  # centre of gold band
        clutch = Rectangle(width=3.6, height=0.8, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.9).move_to(P(cx, 1.8))
        cl = T("clutch", 30, GOLD).move_to(P(cx, 0.3))
        self.play(FadeIn(clutch), run_time=0.3)
        self.play(clutch.animate.move_to(P(4.4, -0.4)), FadeIn(cl.move_to(P(4.4, 0.55))), run_time=1.2)
        self.at("A fixed amount")
        x0 = 4.4 - 1.8

        def eggs(n):
            w = 3.6 / n
            g = VGroup()
            for i in range(n):
                e = Ellipse(width=w * 0.8, height=0.5 + (0.3 if n < 5 else 0), stroke_color=GOLD, stroke_width=3,
                            fill_color=GOLD, fill_opacity=0.9).move_to(P(x0 + w * (i + 0.5), -0.4))
                g.add(e)
            return g
        small = eggs(8)
        self.play(ReplacementTransform(clutch, small), run_time=1.2)
        self.at("many small eggs")
        ms = T("many small", 30, TEXT).move_to(P(4.4, -1.5))
        self.play(FadeIn(ms), run_time=0.5)
        self.wait(0.8)
        self.at("or a few large ones") if False else None
        self.until(self.t_of("or a") - 0.2)
        big = eggs(3)
        self.play(ReplacementTransform(small, big), run_time=1.2)
        self.at("a few large")
        fl = T("few large", 30, TEXT).move_to(P(4.4, -1.5))
        self.play(ReplacementTransform(ms, fl), run_time=0.5)
        self.play(big.animate.scale(1.08), run_time=1.0, rate_func=there_and_back)
        self.finish()


# ----------------------------------------------------------------------------------------
def two_bars(rA, rB):
    """Birds A and B, same intake (same bar length), different splits."""
    return (always_redraw(lambda: bar_group(rA.get_value(), y=3.1, x0=-5.0, w=8.4, h=0.7)),
            always_redraw(lambda: bar_group(rB.get_value(), y=2.0, x0=-5.0, w=8.4, h=0.7)))


class S05Selection(SB):
    def construct(self):
        ax = axes_group(words=False)
        Rl = T("R", 30, GOLD).move_to(O + P(L + 0.8, 0))
        Sl = T("S", 30, TEAL).move_to(O + P(0, L + 0.8))
        line = tline()
        self.add(ax, Rl, Sl, line)
        rA, rB = ValueTracker(0.5), ValueTracker(0.5)
        barA, barB = two_bars(rA, rB)
        ia = songbird(0.6).move_to(P(-6.0, 3.1))
        ib = songbird(0.6).move_to(P(-6.0, 2.0))
        la = T("bird A", 28, TEXT).move_to(P(4.7, 3.1))
        lb = T("bird B", 28, TEXT).move_to(P(4.7, 2.0))
        self.play(FadeIn(barA), FadeIn(barB), FadeIn(ia), FadeIn(ib), FadeIn(la), FadeIn(lb), run_time=1.0)
        idle(ia, 0.04), idle(ib, 0.04, phase=1.5)
        self.wait(0.8)
        dA = always_redraw(lambda: Dot(tpoint(rA.get_value()), radius=0.2, color=TEXT))
        dB = always_redraw(lambda: Dot(tpoint(rB.get_value()), radius=0.2, color=BIRD_C))
        self.at("One pours")
        self.add(dA)
        self.play(rA.animate.set_value(0.8), run_time=2.4)
        self.at("The other keeps")
        self.add(dB)
        self.play(rB.animate.set_value(0.45), run_time=1.6)
        self.play(rB.animate.set_value(0.5), run_time=0.8, rate_func=there_and_back)
        self.at("Each sits")
        tA = always_redraw(lambda: T("A", 30, TEXT, weight=BOLD).move_to(tpoint(rA.get_value()) + P(0.4, 0.35)))
        tB = always_redraw(lambda: T("B", 30, BIRD_C, weight=BOLD).move_to(tpoint(rB.get_value()) + P(0.4, 0.35)))
        self.play(FadeIn(tA), FadeIn(tB), Indicate(dA, color=GOLD, scale_factor=1.6), Indicate(dB, color=GOLD, scale_factor=1.6), run_time=1.2)
        self.play(rA.animate.set_value(0.74), rB.animate.set_value(0.4), run_time=1.5)
        self.at("Selection acts")
        cap = T("selection acts on the split", 26, TEXT).move_to(P(4.5, -2.8))
        self.play(FadeIn(cap), rA.animate.set_value(0.8), rB.animate.set_value(0.45), run_time=1.5)
        self.at("It favors")
        # lifelines and descendants
        ya, yb = 0.7, -1.3
        la_l = Line(P(2.8, ya), P(6.6, ya), color=GREY, stroke_width=4)
        lb_l = Line(P(2.8, yb), P(6.6, yb), color=GREY, stroke_width=4)
        ta = T("A", 28, TEXT, weight=BOLD).move_to(P(2.4, ya))
        tb = T("B", 28, BIRD_C, weight=BOLD).move_to(P(2.4, yb))
        self.play(Create(la_l), Create(lb_l), FadeIn(ta), FadeIn(tb), run_time=0.8)
        xsA, xsB = [3.5, 4.5, 5.5], [3.3, 4.2, 5.1, 6.0]
        kids = VGroup()
        for i in range(4):
            anims = []
            if i < 3:
                mk = Dot(P(xsA[i], ya), radius=0.26, color=GOLD)
                cs = VGroup(*[chick(xsA[i] + dx, ya - 0.5 - 0.0, 0.1) for dx in (-0.22, 0.0, 0.22)])
                anims += [FadeIn(mk, scale=0.4), FadeIn(cs, shift=UP * 0.1)]
                kids.add(mk, cs)
            mk = Dot(P(xsB[i], yb), radius=0.17, color=GOLD)
            cs = VGroup(*[chick(xsB[i] + dx, yb - 0.4, 0.09) for dx in (-0.13, 0.13)])
            anims += [FadeIn(mk, scale=0.4), FadeIn(cs, shift=UP * 0.1)]
            kids.add(mk, cs)
            self.play(*anims, run_time=0.55)
            self.wait(0.2)
        desc = T("descendants", 28, GOLD).move_to(P(4.7, -0.3))
        self.play(FadeIn(desc), run_time=0.5)
        self.at("Which split wins")
        who = T("who dies, and when", 26, TEXT).move_to(P(4.5, -2.8))
        self.play(ReplacementTransform(cap, who), run_time=0.6)
        self.play(Indicate(who, color=GOLD), run_time=1.5)
        self.finish()


# ----------------------------------------------------------------------------------------
PX = (-3.45, 3.45)   # panel centres


def panel(cx, title):
    fr = RoundedRectangle(corner_radius=0.2, width=6.5, height=7.3, stroke_color=GREY, stroke_width=2).move_to(P(cx, 0))
    t = T(title, 32, TEXT, weight=BOLD).move_to(P(cx, 3.2))
    return VGroup(fr, t)


def adults(cx, n=5, y=2.0):
    return VGroup(*[songbird(0.55).move_to(P(cx - 2.2 + i * 1.1, y)) for i in range(n)])


def chicks(cx, n=5, y=-0.3):
    return VGroup(*[Circle(radius=0.28, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.9).move_to(P(cx - 2.0 + i * 1.0, y)) for i in range(n)])


def gauge(cx, v, y=-2.6, w=4.6):
    box = Rectangle(width=w, height=0.5, stroke_color=GREY, stroke_width=3).move_to(P(cx, y))
    fill = Rectangle(width=max(w * v, 0.01), height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9)
    fill.move_to(P(cx - w / 2 + w * v / 2, y))
    return VGroup(box, fill)


class S06Worlds(SB):
    def construct(self):
        c1, c2 = PX
        p1, p2 = panel(c1, "World 1"), panel(c2, "World 2")
        a1, a2 = adults(c1), adults(c2)
        k1, k2 = chicks(c1), chicks(c2)
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.8)
        self.play(FadeIn(a1), FadeIn(k1), FadeIn(a2), FadeIn(k2), run_time=1.0)
        for m in list(a1) + list(a2):
            idle(m, 0.04, phase=np.random.RandomState(int(m.get_x() * 10 + 99)).rand() * 6)
        self.at("In the first")
        sn1 = snowflake(0.45).move_to(P(c1 - 3.0, 3.0))
        self.add(sn1)
        sn1.add_updater(lambda m, dt: m.rotate(dt * 1.5))
        self.play(sn1.animate.move_to(P(c1 + 3.0, 0.3)), run_time=1.0, rate_func=linear)
        self.play(FadeOut(sn1), run_time=0.2)
        pl1 = T("adult survival p: low", 28, TEXT).move_to(P(c1, 1.0))
        cl1 = T("young survival c: high", 28, GOLD).move_to(P(c1, -1.3))
        g1 = gauge(c1, 0.85)
        # adults fade (we ride the narration "adults rarely survive")
        self.at("adults rarely survive") if False else None
        self.until(self.t_of("adults rarely") - 0.2)
        self.play(FadeIn(pl1), *[a1[i].animate.set_opacity(0.12) for i in (0, 1, 3, 4)], run_time=1.4)
        self.at("but their young")
        self.play(FadeIn(cl1), FadeIn(g1), *[Indicate(k, color=GOLD, scale_factor=1.15) for k in k1], run_time=1.5)
        self.at("In the second")
        sn2 = snowflake(0.45).move_to(P(c2 - 3.0, 3.0))
        self.add(sn2)
        sn2.add_updater(lambda m, dt: m.rotate(dt * 1.5))
        self.play(sn2.animate.move_to(P(c2 + 3.0, 0.3)), run_time=0.9, rate_func=linear)
        self.play(FadeOut(sn2), run_time=0.2)
        pl2 = T("adult survival p: high", 28, TEXT).move_to(P(c2, 1.0))
        cl2 = T("young survival c: low or variable", 26, GOLD).move_to(P(c2, -1.3))
        self.until(self.t_of("adults usually") - 0.2)
        self.play(FadeIn(pl2), *[Indicate(a, color=TEXT, scale_factor=1.12) for a in a2], run_time=1.4)
        self.at("while many young die")
        self.play(FadeIn(cl2), *[k2[i].animate.set_opacity(0.12) for i in (0, 2, 3)], run_time=1.6)
        self.at("survival swings")
        w = ValueTracker(0.0)
        box = Rectangle(width=4.6, height=0.5, stroke_color=GREY, stroke_width=3).move_to(P(c2, -2.6))

        def gfill():
            v = 0.5 + 0.38 * np.sin(w.get_value() * 2.2) * np.cos(w.get_value() * 0.7 + 1)
            f = Rectangle(width=4.6 * v, height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9)
            return f.move_to(P(c2 - 2.3 + 4.6 * v / 2, -2.6))
        gf = always_redraw(gfill)
        self.add(box, gf)
        self.play(w.animate.set_value(8.0), run_time=max(1.0, self.narration_s + 0.4 - self.elapsed()), rate_func=linear)
        self.finish()


# ----------------------------------------------------------------------------------------
def world1_static(scene, faded=True):
    c1 = PX[0]
    p1 = panel(c1, "World 1")
    a1 = adults(c1)
    k1 = chicks(c1)
    for i in (0, 1, 3, 4):
        a1[i].set_opacity(0.12)
    pl1 = T("adult survival p: low", 28, TEXT).move_to(P(c1, 1.0))
    cl1 = T("young survival c: high", 28, GOLD).move_to(P(c1, -1.3))
    g1 = gauge(c1, 0.85)
    scene.add(p1, a1, k1, pl1, cl1, g1)
    return a1, k1


def predict_right(r_tracker):
    O2 = P(1.9, -2.5)
    L2 = 3.2
    ax = axes_group(O2, L2, words=False)
    Rl = T("R", 30, GOLD).move_to(O2 + P(L2 + 0.75, 0))
    Sl = T("S", 30, TEAL).move_to(O2 + P(0, L2 + 0.75))
    ln = tline(O2, L2)
    dt = always_redraw(lambda: Dot(tpoint(r_tracker.get_value(), O2, L2), radius=0.18, color=TEXT))
    bar = always_redraw(lambda: bar_group(r_tracker.get_value(), y=2.5, x0=0.9, w=5.6, h=0.6))
    return VGroup(ax, Rl, Sl, ln, dt, bar)


class S07Predict(SB):
    def construct(self):
        a1, k1 = world1_static(self)
        r = ValueTracker(0.5)
        right = predict_right(r)
        self.play(FadeIn(right), run_time=0.5)
        q = T("?", 110, GOLD, weight=BOLD).move_to(P(5.7, -0.1))
        self.at("Here is a question")
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        q.add_updater(lambda m, dt: m.set_opacity(0.65 + 0.35 * np.sin(self.renderer.time * 4)))
        self.at("In the first world")
        self.play(Indicate(a1, color=TEXT, scale_factor=1.05), run_time=1.0)
        self.at("adults rarely live")
        self.play(r.animate.set_value(0.45), run_time=1.0)
        self.at("Does that lower")
        lo = chip("lower", TEAL, 34).move_to(P(3.0, 1.45))
        ro = chip("or raise", GOLD, 34).move_to(P(5.3, 1.45))
        self.play(FadeIn(lo), run_time=0.5)
        self.at("or raise")
        self.play(FadeIn(ro), run_time=0.5)
        self.at("extra young")
        self.play(r.animate.set_value(0.6), run_time=1.2)
        self.play(r.animate.set_value(0.4), run_time=1.2)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        a1, k1 = world1_static(self)
        r = ValueTracker(0.5)
        right = predict_right(r)
        self.add(right)
        q = T("?", 110, GOLD, weight=BOLD).move_to(P(5.7, -0.1))
        lo = chip("lower", TEAL, 34).move_to(P(3.0, 1.45))
        ro = chip("or raise", GOLD, 34).move_to(P(5.3, 1.45))
        self.add(q, lo, ro)
        t = ValueTracker(0.0)
        ring = always_redraw(lambda: Arc(radius=0.42, start_angle=PI / 2, angle=-TAU * (1 - t.get_value()) + 1e-3,
                                         color=GOLD, stroke_width=8).move_to(P(3.7, -3.2)))
        base = Circle(radius=0.42, color=GREY, stroke_width=3).move_to(P(3.7, -3.2))
        self.add(base, ring)
        q.add_updater(lambda m, dt: m.set_opacity(0.65 + 0.35 * np.sin(self.renderer.time * 4)))
        self.play(t.animate.set_value(0.999), r.animate.set_value(0.62), run_time=2.45, rate_func=linear)
        self.play(r.animate.set_value(0.38), run_time=2.45, rate_func=linear)
        self.finish()


# ----------------------------------------------------------------------------------------
def mini_panel(cx, title):
    p = panel(cx, title)
    O2 = P(cx - 2.8, -0.2)
    L2 = 2.5
    ax = axes_group(O2, L2, words=False)
    for m in ax:
        pass
    Rl = T("R", 28, GOLD).move_to(O2 + P(L2 + 0.7, 0))
    Sl = T("S", 28, TEAL).move_to(O2 + P(0, L2 + 0.65))
    ln = tline(O2, L2)
    return p, O2, L2, VGroup(ax, Rl, Sl, ln)


class S09Reveal(SB):
    def construct(self):
        c1, c2 = PX
        p1, O1, L1, g1 = mini_panel(c1, "World 1")
        p2, O2_, L2_, g2 = mini_panel(c2, "World 2")
        r1, r2 = ValueTracker(0.5), ValueTracker(0.5)
        d1 = always_redraw(lambda: Dot(tpoint(r1.get_value(), O1, L1), radius=0.17, color=TEXT))
        d2 = always_redraw(lambda: Dot(tpoint(r2.get_value(), O2_, L2_), radius=0.17, color=TEXT))
        # gauge: extra young needed (world 1)
        need = ValueTracker(0.9)
        gb = Rectangle(width=0.55, height=2.5, stroke_color=GREY, stroke_width=3).move_to(P(c1 + 1.1, 1.05))

        def gf():
            h = 2.5 * need.get_value()
            return Rectangle(width=0.55, height=max(h, 0.01), stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(P(c1 + 1.1, -0.2 + h / 2))
        gfill = always_redraw(gf)
        gl = VGroup(T("extra", 24, GOLD), T("young", 24, GOLD), T("needed", 24, GOLD)).arrange(DOWN, buff=0.06).move_to(P(c1 + 2.3, 1.05))
        # lifelines
        ly = -2.3
        l1 = Line(P(c1 - 2.8, ly), P(c1 + 2.8, ly), color=GREY, stroke_width=4)
        l2 = Line(P(c2 - 2.8, ly), P(c2 + 2.8, ly), color=GREY, stroke_width=4)
        fut = DashedLine(P(c1 + 0.3, ly), P(c1 + 2.8, ly), color=GREY, stroke_width=4)
        sal = salmon(0.55).move_to(P(c1 - 2.2, ly + 0.4))
        sb = songbird(0.7).move_to(P(c2 - 2.3, ly + 0.45))
        self.add(p1, p2, g1, g2, d1, d2, gb, gfill, gl, l1, l2, sal, sb)
        idle(sal, 0.04), idle(sb, 0.04, phase=1.0)
        # world 2 starts dim until its turn
        self.remove(d2)
        w2 = VGroup(p2[1], g2, l2, sb)
        w2.set_opacity(0.35)
        p2[0].set_stroke(opacity=0.35)
        self.at("It lowers it")
        self.play(need.animate.set_value(0.3), run_time=2.2)
        self.at("Holding back")
        self.play(Create(fut), run_time=1.2)
        fq = T("rarely comes", 28, GREY).move_to(P(c1 + 1.4, ly - 0.55))
        self.play(FadeIn(fq), fut.animate.set_opacity(0.35), run_time=1.0)
        self.at("So putting more")
        self.play(r1.animate.set_value(0.8), run_time=2.4)
        mk = Dot(P(c1 - 0.3, ly), radius=0.27, color=GOLD)
        self.at("as in the salmon")
        self.play(FadeOut(fut), FadeOut(fq), FadeIn(mk, scale=0.4), sal.animate.move_to(P(c1 - 0.3, ly + 0.4)),
                  l1.animate.set_stroke(TEXT, 6), run_time=1.4)
        self.at("How far")
        how = T("how far: set by the trade-off's shape", 24, GREY).move_to(P(c1 - 0.2, -1.0))
        self.play(FadeIn(how), r1.animate.set_value(0.75), run_time=1.0)
        self.play(Indicate(d1, color=GOLD, scale_factor=1.8), run_time=1.2)
        self.at("In the second world")
        self.add(d2)
        self.play(w2.animate.set_opacity(1.0), p2[0].animate.set_stroke(opacity=1.0), FadeOut(how), run_time=0.9)
        self.at("teal buys")
        self.play(r2.animate.set_value(0.2), run_time=2.0)
        tb = T("more breeding seasons", 24, TEAL).move_to(P(c2 + 0.2, -1.0))
        self.play(FadeIn(tb), run_time=0.5)
        self.at("Holding back to breed")
        xs = [c2 - 1.4, c2 - 0.3, c2 + 0.8, c2 + 1.9]
        l2.set_stroke(TEXT, 6)
        self.add(l2)
        for i, x in enumerate(xs):
            self.play(sb.animate.move_to(P(x, ly + 0.45)), run_time=0.45, rate_func=linear)
            self.play(FadeIn(Dot(P(x, ly), radius=0.2, color=GOLD), scale=0.4), run_time=0.2)
        self.finish()


# ----------------------------------------------------------------------------------------
class S10Rule(SB):
    def construct(self):
        words = ["grow fast", "breed early", "many large offspring", "live long"]
        chips = VGroup(*[chip(w, c, 34) for w, c in zip(words, [TEAL, GOLD, GOLD, TEAL])])
        chips.arrange_in_grid(2, 2, buff=(0.7, 0.6)).move_to(P(0, 0.8))
        self.at("grow fast")
        self.play(FadeIn(chips[0], scale=0.8), run_time=0.5)
        self.at("breed early")
        self.play(FadeIn(chips[1], scale=0.8), run_time=0.5)
        self.at("many large")
        self.play(FadeIn(chips[2], scale=0.8), run_time=0.5)
        self.at("and live long")
        self.play(FadeIn(chips[3], scale=0.8), run_time=0.5)
        self.at("all at once")
        no = T("not all at once", 36, RED, weight=BOLD).move_to(P(0, -1.6))
        self.play(FadeIn(no), *[c.animate.shift(P(0.1, 0) * (1 if i % 2 else -1)) for i, c in enumerate(chips)], run_time=0.8)
        self.play(Indicate(chips, color=RED, scale_factor=1.04), run_time=1.2)
        # the world
        self.until(self.t_of("Salmon and songbird") - 0.2)
        self.play(FadeOut(chips), FadeOut(no), run_time=0.4)
        sx0, sw = -4.6, 10.6
        bar = Rectangle(width=sw, height=0.8, stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=1).move_to(P(sx0 + sw / 2, 3.1))
        bl = T("one intake (A)", 30, TEXT).move_to(P(sx0 + sw / 2, 3.1))
        sa = salmon(0.55).move_to(P(-5.8, 1.9))
        so = songbird(0.7).move_to(P(-5.8, 0.75))
        ys, yb = 1.9, 0.75
        ssplit = bar_group(0.8, y=ys, x0=sx0, w=sw, h=0.7)
        bsplit = bar_group(0.45, y=yb, x0=sx0, w=sw, h=0.7)
        self.play(FadeIn(bar), FadeIn(bl), FadeIn(sa), FadeIn(so), run_time=0.5)
        self.play(FadeIn(ssplit, shift=UP * 0.3), FadeIn(bsplit, shift=UP * 0.3), run_time=0.6)
        # lifelines slide in from the sides, to sit under the bar
        ly1, ly2 = -0.9, -2.2
        ll1 = Line(P(-6.8, ly1), P(-6.0, ly1), color=GREY, stroke_width=4)
        ll2 = Line(P(6.8, ly2), P(6.0, ly2), color=GREY, stroke_width=4)
        sal2 = salmon(0.55).move_to(P(-6.2, ly1 + 0.4))
        sb2 = songbird(0.7).move_to(P(6.2, ly2 + 0.45))
        self.add(ll1, ll2)
        self.play(ll1.animate.put_start_and_end_on(P(sx0, ly1), P(sx0 + 4.2, ly1)).set_stroke(TEXT, 5),
                  ll2.animate.put_start_and_end_on(P(sx0, ly2), P(sx0 + sw, ly2)).set_stroke(TEXT, 5),
                  FadeIn(sal2), FadeIn(sb2), run_time=1.0)
        self.play(sal2.animate.move_to(P(sx0 + 3.6, ly1 + 0.4)), sb2.animate.move_to(P(sx0 + 0.6, ly2 + 0.45)), run_time=0.5)
        mk = Dot(P(sx0 + 3.4, ly1), radius=0.26, color=GOLD)
        self.add(mk)
        cap = T("same rule, different worlds", 34, TEXT).move_to(P(0.5, -3.3))
        self.play(FadeIn(cap), run_time=0.4)
        idle(sal2, 0.04), idle(sb2, 0.04, phase=1.2)
        self.at("One intake")
        self.play(Indicate(bar, color=GOLD, scale_factor=1.03), run_time=0.9)
        self.play(Indicate(ssplit, color=TEXT, scale_factor=1.03), Indicate(bsplit, color=TEXT, scale_factor=1.03), run_time=1.0)
        self.at("one split")
        for i in range(5):
            x = sx0 + 1.4 + 2.0 * i
            self.play(sb2.animate.move_to(P(x, ly2 + 0.45)), FadeIn(Dot(P(x, ly2), radius=0.2, color=GOLD), scale=0.4), run_time=0.4)
        self.at("Selection picks")
        ch = VGroup(*[chick(sx0 + 3.4 + dx, ly1 - 0.5, 0.11) for dx in (-0.4, -0.15, 0.1, 0.35)])
        ch2 = VGroup(*[chick(sx0 + 9.0 + 0.0, ly2 - 0.5 - 0.0, 0.0001)])
        self.play(FadeIn(ch, shift=UP * 0.1), Indicate(cap, color=GOLD), run_time=1.5)
        self.play(Indicate(cap, color=GOLD), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------
class S11Thread(SB):
    def construct(self):
        OA = P(-6.2, -3.4)
        a1, a2 = 3.6, 6.0
        axs = axes_group(OA, 3.0, words=False)
        axs = VGroup(Arrow(OA, OA + P(a2 + 0.3, 0), buff=0, color=GOLD, stroke_width=5, tip_length=0.2),
                     Arrow(OA, OA + P(0, a2 + 0.3), buff=0, color=TEAL, stroke_width=5, tip_length=0.2))
        line1 = Line(OA + P(0, a1), OA + P(a1, 0), color=GREY, stroke_width=6)
        b1 = songbird(0.8).move_to(P(-0.2, 2.8))
        bar1 = Rectangle(width=a1, height=0.8, stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=1).move_to(P(0.7 + a1 / 2, 2.8))
        self.play(FadeIn(axs), Create(line1), FadeIn(b1), FadeIn(bar1), run_time=1.0)
        idle(b1, 0.04)
        self.at("So far every bird")
        b2 = songbird(0.8, color="#D9C7A8").move_to(P(-0.2, 1.4))
        bar2 = Rectangle(width=a1, height=0.8, stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=1).move_to(P(0.7 + a1 / 2, 1.4))
        same = T("same intake", 32, TEXT).move_to(P(3.4, 0.45))
        self.play(FadeIn(b2), FadeIn(bar2), FadeIn(same), run_time=1.0)
        idle(b2, 0.04, phase=1.0)
        self.at("Real animals")
        line2 = Line(OA + P(0, a1), OA + P(a1, 0), color=GREY, stroke_width=6)
        self.play(FadeOut(same), bar2.animate.stretch_to_fit_width(a2).move_to(P(0.7 + a2 / 2, 1.4)),
                  Transform(line2, Line(OA + P(0, a2), OA + P(a2, 0), color=GREY, stroke_width=6)), run_time=2.2)
        self.at("Hold that thought")
        q = T("?", 110, GREY, weight=BOLD).move_to(P(-3.5, -1.3))
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        for _ in range(3):
            self.play(q.animate.scale(1.2), run_time=0.9, rate_func=there_and_back)
        self.at("changes what")
        self.play(Indicate(line2, color=TEXT, scale_factor=1.0), Indicate(line1, color=TEXT, scale_factor=1.0), run_time=1.5)
        self.finish()


class S12End(EndCard):
    LINE = "Selection picks the split leaving most descendants, given who dies when."
