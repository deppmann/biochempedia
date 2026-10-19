"""Which speed did you measure?  (Sensory Systems: Five Ways to Turn a Stimulus into a Current)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, whole film)
  YELLOW = tissue latency (the 40 microsecond delay across the sheet of hair cells)
  BLUE   = channel (the transduction channel, CALHM channels) and channel time constant
  PURPLE = molecular gain
  ORANGE = behavioural latency
  TEAL   = the 3 ms depolarizing pulse
  GREEN  = activation fraction reached (gauges)
  RED    = crossed out: not this, does not identify
  GREY   = cells, membranes, axes, de-emphasized
  TEXT   = labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def hair_cell(s=1.0, chan=True):
    """A simple hair cell: body, three stereocilia in a staircase, two tip links, a channel chip on each link."""
    body = RoundedRectangle(corner_radius=0.3 * s, width=1.5 * s, height=1.7 * s, stroke_color=GREY,
                            stroke_width=3, fill_color=GREY, fill_opacity=0.2)
    top = body.get_top()
    xs, hs = [-0.4, 0.0, 0.4], [0.7, 1.1, 1.5]
    cil = VGroup(*[Line(top + RIGHT * x * s, top + RIGHT * x * s + UP * h * s, color=TEXT, stroke_width=5)
                   for x, h in zip(xs, hs)])
    links = VGroup(*[Line(top + RIGHT * xs[i] * s + UP * hs[i] * s,
                          top + RIGHT * xs[i + 1] * s + UP * (hs[i] + 0.22) * s, color=GREY, stroke_width=3)
                     for i in range(2)])
    chans = VGroup(*[RoundedRectangle(corner_radius=0.04, width=max(0.16, 0.24 * s), height=max(0.12, 0.17 * s),
                                      stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.9
                                      ).move_to(l.get_center()) for l in links]) if chan else VGroup()
    bundle = VGroup(cil, links, chans)
    g = VGroup(body, bundle)
    g.body, g.bundle, g.chans, g.base = body, bundle, chans, top
    return g


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def mapper(ox, oy, w, h, xmax, ymax):
    return lambda t, v: np.array([ox + w * t / xmax, oy + h * v / ymax, 0.0])


def trace(f, t0, t1, mp, color, n=140, width=5, dashed=False):
    pts = [mp(t, f(t)) for t in np.linspace(t0, t1, n)]
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts)
    return DashedVMobject(m, num_dashes=40) if dashed else m


def span(x0, x1, y, color, tick=0.12, w=4):
    """a horizontal bracket from x0 to x1 at height y, with end ticks"""
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w),
                  Line([x0, y - tick, 0], [x0, y + tick, 0], color=color, stroke_width=w),
                  Line([x1, y - tick, 0], [x1, y + tick, 0], color=color, stroke_width=w))


class S00Title(TitleCard):
    LESSON = "Five ways to turn a stimulus into a current"
    TITLE = "Which Speed Did You Measure?"


# ---------------------------------------------------------------------------------------------
class S01Number(SpokenScene):
    """40 µs on a hair cell -> is it a channel opening time? crossed out -> it belongs to a whole tissue."""

    def construct(self):
        cell = hair_cell(1.25).move_to([-4.2, -0.9, 0])
        lbl = T("hair cell", 26, GREY).next_to(cell, DOWN, buff=0.25)
        tag = M("40 µs", 56, YELLOW).move_to([1.7, 2.2, 0])
        self.at("most often quoted")
        self.play(FadeIn(cell), FadeIn(lbl), run_time=0.7)
        self.play(Write(tag), run_time=0.7)

        self.at("how long one channel")
        q = T("= how long one channel takes to open?", 28, BLUE).move_to([1.7, 0.9, 0])
        self.play(FadeIn(q, shift=UP * 0.1), Indicate(cell.chans, color=BLUE, scale_factor=1.7), run_time=0.9)

        self.at("It is not")
        cross = Line(q.get_left() + LEFT * 0.12, q.get_right() + RIGHT * 0.12, color=RED, stroke_width=7)
        self.play(Create(cross), q.animate.set_opacity(0.5), run_time=0.5)

        self.at("corrected delay")
        note = T("a corrected delay", 30, YELLOW).move_to([1.7, 0.9, 0])
        self.play(FadeOut(q), FadeOut(cross), FadeIn(note), run_time=0.5)

        self.at("whole piece")
        row = VGroup(*[hair_cell(0.6, chan=False) for _ in range(5)])
        for i, c in enumerate(row):
            c.move_to([1.7 + (i - 2) * 1.05, -1.4, 0])
        brk = span(-0.95, 4.35, -2.3, YELLOW)
        blbl = T("a whole piece of tissue", 28, YELLOW).move_to([1.7, -2.85, 0])
        arrow = Arrow([1.7, 0.55, 0], [1.7, 0.18, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in row], lag_ratio=0.12), run_time=1.0)
        self.play(Create(brk), GrowArrow(arrow), FadeIn(blbl), run_time=0.8)

        self.at("which quantity")
        qq = T("which quantity?", 42, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.play(Write(qq), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Tissue(SpokenScene):
    """a sheet of hair cells is deflected; the summed response across the sheet is slowed; the delay shrinks to 40 µs."""

    def construct(self):
        cells = VGroup(*[hair_cell(0.5, chan=False) for _ in range(7)]).arrange(RIGHT, buff=0.35).move_to([0, 1.85, 0])
        yb = cells[0].body.get_bottom()[1] - 0.08
        sheet = Line([-4.1, yb, 0], [4.1, yb, 0], color=GREY, stroke_width=8)
        what = T("in vitro bullfrog sacculus", 26, GREY).move_to([0, 3.4, 0])

        # plot frame (in this sketch)
        ox, oy, w, h = -4.5, -2.85, 9.0, 2.35
        mp = mapper(ox, oy, w, h, 10.0, 1.0)
        xax = Line([ox, oy, 0], [ox + w, oy, 0], color=GREY, stroke_width=3)
        yax = Line([ox, oy, 0], [ox, oy + h + 0.1, 0], color=GREY, stroke_width=3)
        ylab = T("response", 22, GREY).next_to(yax.get_end(), RIGHT, buff=0.12)
        xlab = T("time, not to scale", 22, GREY).move_to([ox + w - 1.2, oy - 0.33, 0])
        sk = T("in this sketch", 22, GREY).move_to([ox + 1.0, oy - 0.33, 0])
        stim_x = mp(4.0, 0)[0]
        stim = DashedVMobject(Line([stim_x, oy, 0], [stim_x, oy + h, 0], color=GREY, stroke_width=3), num_dashes=14)
        stim_l = T("stimulus", 22, GREY).move_to([stim_x + 0.02, oy - 0.33, 0])

        self.at("stimulated hair bundles")
        self.play(FadeIn(cells), Create(sheet), FadeIn(what), run_time=0.9)
        tilt = [c.bundle.animate.rotate(-0.22, about_point=c.body.get_top()) for c in cells]
        self.play(*tilt, run_time=0.6)

        self.at("summed electrical response")
        br = span(-3.9, 3.9, yb - 0.25, YELLOW)
        bl = T("summed response across the sheet", 26, YELLOW).move_to([0, yb - 0.62, 0])
        self.play(Create(br), FadeIn(bl), run_time=0.7)
        self.play(Create(xax), Create(yax), FadeIn(ylab), FadeIn(xlab), FadeIn(sk), Create(stim), FadeIn(stim_l), run_time=0.8)
        rec = trace(lambda t: 1 - np.exp(-(t - 4.5) / 1.3), 4.5, 10.0, mp, YELLOW)
        pre = Line(mp(0, 0), mp(4.5, 0), color=YELLOW, stroke_width=5)
        self.play(Create(pre), run_time=0.4)
        self.play(Create(rec), run_time=1.6)

        self.at("slows that signal")
        yy = oy + 0.88 * h
        x0, x1 = mp(4.0, 0)[0], mp(5.9, 0)[0]
        d1 = VGroup(Line([x0, yy - 0.12, 0], [x0, yy + 0.12, 0], color=YELLOW, stroke_width=4),
                    DashedVMobject(Line([x0, yy, 0], [x1, yy, 0], color=YELLOW, stroke_width=4), num_dashes=12),
                    Arrow([x1 - 0.2, yy, 0], [x1, yy, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.18))
        d1l = T("recorded delay\n(longer)", 24, YELLOW, line_spacing=0.9).next_to(d1, LEFT, buff=0.2)
        v1 = VGroup()
        self.play(Create(d1), FadeIn(d1l), Create(v1), run_time=0.8)

        self.at("After correcting")
        d2 = span(mp(4.0, 0)[0], mp(4.5, 0)[0], oy + 0.5 * h, TEXT)
        d2l = T("corrected:\n40 µs at 22 °C", 24, TEXT, line_spacing=0.9).next_to(d2, LEFT, buff=0.2)
        self.play(Create(d2), FadeIn(d2l), v1.animate.set_opacity(0.3), d1.animate.set_opacity(0.45), d1l.animate.set_opacity(0.45), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def card(title, body, color, icon):
    box = RoundedRectangle(corner_radius=0.2, width=6.1, height=2.45, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.08)
    icon.move_to(box.get_left() + RIGHT * 1.15)
    t = T(title, 27, color, weight=BOLD, line_spacing=0.9)
    b = T(body, 23, TEXT, line_spacing=0.9)
    txt = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    txt.move_to(box.get_center() + RIGHT * 0.95)
    g = VGroup(box, icon, txt)
    g.box = box
    return g


class S03Four(SpokenScene):
    """four cards: tissue latency, channel time constant, molecular gain, behavioural latency."""

    def construct(self):
        head = T("four quantities, one word: speed", 34, font=TITLE_FONT).move_to([0, 3.2, 0])

        mini = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.4, height=0.6, stroke_color=GREY, stroke_width=2,
                                         fill_color=GREY, fill_opacity=0.25) for _ in range(3)]).arrange(RIGHT, buff=0.12)
        ic1 = VGroup(mini, span(mini.get_left()[0], mini.get_right()[0], mini.get_bottom()[1] - 0.25, YELLOW))
        mem = Line(LEFT * 0.75, RIGHT * 0.75, color=GREY, stroke_width=8).shift(DOWN * 0.45)
        curve = VMobject(stroke_color=BLUE, stroke_width=5)
        curve.set_points_as_corners([np.array([-0.7 + 1.4 * u, -0.25 + 0.85 * (1 - np.exp(-3.2 * u)), 0]) for u in np.linspace(0, 1, 30)])
        ic2 = VGroup(mem, curve)
        ic3 = VGroup(T("output", 22, PURPLE), Line(LEFT * 0.6, RIGHT * 0.6, color=PURPLE, stroke_width=4),
                     T("input", 22, PURPLE)).arrange(DOWN, buff=0.1)
        dots = [Circle(radius=0.1, stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=1, stroke_width=1) for _ in range(4)]
        ic4 = VGroup(*dots).arrange(RIGHT, buff=0.3)
        arrs = [Arrow(dots[i].get_right(), dots[i + 1].get_left(), buff=0.02, color=ORANGE, stroke_width=3, tip_length=0.12) for i in range(3)]
        ic4 = VGroup(ic4, *arrs)

        c1 = card("Tissue latency", "the delay of a population\nof cells", YELLOW, ic1)
        c2 = card("Channel time\nconstant", "how fast a current rises\nafter a step", BLUE, ic2)
        c3 = card("Molecular gain", "output events per\ninput event", PURPLE, ic3)
        c4 = card("Behavioural\nlatency", "stimulus to movement", ORANGE, ic4)
        c1.move_to([-3.2, 1.25, 0]); c2.move_to([3.2, 1.25, 0]); c3.move_to([-3.2, -1.6, 0]); c4.move_to([3.2, -1.6, 0])

        self.at("Four different quantities")
        self.play(Write(head), run_time=1.0)
        self.at("tissue latency")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.7)
        self.at("channel time constant")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.7)
        self.at("molecular gain")
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.7)
        self.at("stimulus to movement")
        self.play(FadeIn(c4, shift=UP * 0.15), run_time=0.7)
        self.at("constant stands in")
        self.play(c2.animate.set_opacity(0.35), c1.animate.set_opacity(0.35), c3.animate.set_opacity(0.35),
                  Indicate(c4.box, color=ORANGE, scale_factor=1.05), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Channel(SpokenScene):
    """a 3 ms depolarization; two channel rows with their time constants."""

    def construct(self):
        # left: the pulse
        lh = T("a taste cell depolarizes", 28, TEAL).move_to([-3.3, 3.0, 0])
        ox, oy = -5.9, -1.7
        mp = mapper(ox, oy, 5.4, 3.9, 10.0, 1.0)
        xax = Line(mp(0, 0), mp(10, 0), color=GREY, stroke_width=3)
        yax = Line(mp(0, 0), mp(0, 1.05), color=GREY, stroke_width=3)
        vlab = T("membrane voltage", 22, GREY).next_to(yax.get_end(), RIGHT, buff=0.12)
        pulse = VMobject(stroke_color=TEAL, stroke_width=6)
        pulse.set_points_as_corners([mp(0, 0.1), mp(1, 0.1), mp(1, 0.85), mp(4, 0.85), mp(4, 0.1), mp(10, 0.1)])
        pb = span(mp(1, 0)[0], mp(4, 0)[0], oy - 0.35, TEAL)
        pbl = M("3 ms", 30, TEAL).move_to([(mp(1, 0)[0] + mp(4, 0)[0]) / 2, oy - 0.8, 0])
        sk = T("a square pulse, in this sketch", 22, GREY).move_to([-3.3, oy - 1.45, 0])

        # right: two channel rows
        rh = T("in cultured mouse N2a cells", 28, GREY).move_to([3.3, 3.0, 0])
        def row(y, chips, tau):
            mem = RoundedRectangle(corner_radius=0.1, width=5.6, height=0.3, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.35).move_to([3.3, y, 0])
            cs = VGroup(*[bchip(n, BLUE, 32) for n in chips]).arrange(RIGHT, buff=0.3).next_to(mem, UP, buff=0.12)
            tl = M(tau, 32, BLUE).next_to(mem, DOWN, buff=0.3)
            return VGroup(mem, cs), tl
        r1, t1 = row(1.25, ["CALHM1"], "τ above 500 ms")
        r2, t2 = row(-1.35, ["CALHM1", "CALHM3"], "τ about 10 ms")

        self.play(FadeIn(lh), Create(xax), Create(yax), FadeIn(vlab), run_time=0.7)
        self.at("Suppose a taste cell")
        self.play(Create(pulse), run_time=1.0)
        self.play(Create(pb), FadeIn(pbl), FadeIn(sk), run_time=0.6)

        self.at("cultured mouse")
        self.play(FadeIn(rh), FadeIn(r1), run_time=0.7)
        self.at("alone activated")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.at("added the time constant")
        self.play(FadeIn(r2), run_time=0.6)
        self.at("the time constant was")
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Fraction(SpokenScene):
    """a(t) = 1 - exp(-t/tau) for tau 10 ms and 500 ms; at 3 ms: 25.9 % and 0.60 %; about 43 times."""

    def construct(self):
        eq = M("a(t) = 1 − exp(−t/τ)", 30, TEXT).move_to([-2.3, 3.15, 0])
        ox, oy, w, h = -5.5, -2.15, 6.3, 3.95
        mp = mapper(ox, oy, w, h, 30.0, 1.0)
        xax = Line(mp(0, 0), mp(30, 0), color=GREY, stroke_width=3)
        yax = Line(mp(0, 0), mp(0, 1.04), color=GREY, stroke_width=3)
        ticks = VGroup()
        for t in (0, 10, 20, 30):
            ticks.add(M(str(t), 22, GREY).move_to(mp(t, 0) + DOWN * 0.3))
        for v, lab in ((0.5, "50%"), (1.0, "100%")):
            ticks.add(M(lab, 22, GREY).move_to(mp(0, v) + LEFT * 0.45))
        xl = T("time (ms)", 22, GREY).move_to(mp(15, 0) + DOWN * 0.66)
        yl = T("activation", 22, GREY).next_to(yax.get_end(), UP, buff=0.12).align_to(yax, LEFT)
        shade = Rectangle(width=w * 3 / 30, height=h, stroke_width=0, fill_color=TEAL, fill_opacity=0.18
                          ).move_to(mp(1.5, 0.5))
        shade_l = M("3 ms pulse", 22, TEAL).move_to(mp(3.8, 0.93), aligned_edge=LEFT)

        fast = VGroup(trace(lambda t: 1 - np.exp(-t / 10.0), 0, 3, mp, BLUE, n=30),
                      trace(lambda t: 1 - np.exp(-t / 10.0), 3, 30, mp, BLUE, dashed=True))
        slow = VGroup(trace(lambda t: 1 - np.exp(-t / 500.0), 0, 3, mp, BLUE, n=20),
                      trace(lambda t: 1 - np.exp(-t / 500.0), 3, 30, mp, BLUE, dashed=True))
        cont = T("dashed: if depolarization continued", 22, GREY).move_to(mp(19.5, 1.1))
        fl = T("CALHM1 + CALHM3: τ = 10 ms", 24, BLUE).move_to(mp(19.5, 0.46))
        sl = T("CALHM1 alone: τ 500 ms\n(measured: above 500)", 22, BLUE, line_spacing=0.9).move_to(mp(19.5, 0.2))
        d1 = Dot(mp(3, 1 - np.exp(-0.3)), color=GREEN, radius=0.1)
        d2 = Dot(mp(3, 1 - np.exp(-0.006)), color=GREEN, radius=0.1)

        # gauges
        gh = 3.95
        gx1, gx2, gy = 2.7, 5.0, -2.15
        def gauge(x):
            fr = Rectangle(width=0.8, height=gh, stroke_color=GREY, stroke_width=3)
            fr.move_to([x, gy + gh / 2, 0])
            return fr
        g1, g2 = gauge(gx1), gauge(gx2)
        f1 = Rectangle(width=0.8, height=gh * 0.259, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
        f1.move_to([gx1, gy + gh * 0.259 / 2, 0])
        f2 = Rectangle(width=0.8, height=max(gh * 0.006, 0.03), stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
        f2.move_to([gx2, gy + max(gh * 0.006, 0.03) / 2, 0])
        v1 = M("25.9%", 28, GREEN).next_to(g1, UP, buff=0.15)
        v2 = M("0.60%", 28, GREEN).next_to(g2, UP, buff=0.15)
        v2b = M("under 0.60%", 24, GREEN).next_to(g2, UP, buff=0.15)
        n1 = M("τ 10 ms", 22, BLUE).next_to(g1, DOWN, buff=0.25)
        n2 = VGroup(M("τ 500 ms", 22, BLUE), T("measured: above 500", 20, BLUE)).arrange(DOWN, buff=0.06).next_to(g2, DOWN, buff=0.2)
        big = T("about 43 times", 34, GREEN, weight=BOLD).move_to([3.85, 3.15, 0])
        sk = T("teaching assumptions: one exponential, a square 3 ms pulse", 22, GREY).move_to([-1.7, -3.35, 0])

        self.at("Model a channel")
        self.play(FadeIn(eq), Create(xax), Create(yax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), run_time=0.9)
        self.play(FadeIn(shade), FadeIn(shade_l), run_time=0.5)
        self.play(FadeIn(sk), run_time=0.4)
        self.at("single exponential")
        self.play(Create(fast), FadeIn(cont), run_time=1.2)
        self.at("With a time constant")
        self.play(FadeIn(fl), run_time=0.5)
        self.at("reaches about")
        self.play(FadeIn(d1), FadeIn(g1), FadeIn(n1), run_time=0.5)
        self.play(FadeIn(f1), FadeIn(v1), run_time=0.6)
        self.at("reaches about", nth=1)
        self.play(Create(slow), FadeIn(sl), FadeIn(d2), FadeIn(g2), FadeIn(n2), run_time=0.9)
        self.play(FadeIn(f2), FadeIn(v2), run_time=0.5)
        self.at("smaller still")
        self.play(ReplacementTransform(v2, v2b), run_time=0.5)
        self.at("partner makes")
        self.play(Write(big), run_time=0.9)
        self.at("teaching assumptions")
        self.play(Indicate(sk, color=TEXT, scale_factor=1.06), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """fast latency fits a candidate channel, does not identify it; tissue vs channel; the two questions."""

    def construct(self):
        a = bchip("fast latency", YELLOW, 28).move_to([-4.7, 2.4, 0])
        b = bchip("candidate channel", BLUE, 28).move_to([4.5, 2.4, 0])
        ar1 = Arrow([a.get_right()[0] + 0.1, 2.65, 0], [b.get_left()[0] - 0.1, 2.65, 0], buff=0, color=GREEN, stroke_width=5, tip_length=0.2)
        l1 = T("can fit", 24, GREEN).move_to([0, 3.05, 0])
        ar2 = Arrow([a.get_right()[0] + 0.1, 2.15, 0], [b.get_left()[0] - 0.1, 2.15, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.2)
        l2 = T("identifies", 24, GREY).move_to([-0.9, 1.75, 0])
        x = VGroup(Line([0.55, 1.5, 0], [1.15, 2.8 - 0.65, 0], color=RED, stroke_width=7),
                   Line([0.55, 2.8 - 0.65, 0], [1.15, 1.5, 0], color=RED, stroke_width=7))
        x.move_to([ (a.get_right()[0] + b.get_left()[0]) / 2, 2.15, 0]).shift(RIGHT * 1.5)
        l2.move_to([x.get_center()[0] - 1.8, 1.75, 0])

        def box(color, title, num, where):
            bx = RoundedRectangle(corner_radius=0.2, width=5.8, height=2.5, stroke_color=color, stroke_width=3,
                                  fill_color=color, fill_opacity=0.08)
            t = T(title, 28, color, weight=BOLD)
            n = M(num, 40, TEXT)
            wh = T(where, 22, GREY, line_spacing=0.9)
            VGroup(t, n, wh).arrange(DOWN, buff=0.24).move_to(bx)
            return VGroup(bx, t, n, wh)
        c1 = box(YELLOW, "Tissue latency", "40 µs", "in vitro bullfrog sacculus").move_to([-3.3, -0.6, 0])
        c2 = box(BLUE, "Channel time constant", "about 10 ms", "CALHM1 + CALHM3,\ncultured mouse N2a cells").move_to([3.3, -0.6, 0])
        q = T("which quantity?   in which cell?", 38, font=TITLE_FONT).move_to([0, -2.95, 0])

        top = VGroup(a, b, ar1, l1, ar2, l2, x)
        top.shift(DOWN * 2.2)
        for m in (ar2, l2, x):
            m.set_opacity(0)
        self.at("fast latency")
        self.play(FadeIn(a), FadeIn(b), run_time=0.6)
        self.play(GrowArrow(ar1), FadeIn(l1), run_time=0.6)
        self.at("constraint on the kinetics")
        self.play(Indicate(b, color=BLUE, scale_factor=1.08), run_time=0.8)
        self.at("Speed alone")
        self.play(ar2.animate.set_opacity(1), l2.animate.set_opacity(1), run_time=0.5)
        self.play(x.animate.set_opacity(1), run_time=0.4)
        self.at("describes a tissue")
        self.play(top.animate.shift(UP * 2.2), run_time=0.6)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.at("describes a channel")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        self.at("ask which quantity")
        self.play(Write(q), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Ask which quantity it is, and in which cell."
