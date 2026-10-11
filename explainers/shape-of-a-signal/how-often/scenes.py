"""How often: why a slow off switch can count spikes  (Biochemistrypedia section film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  TEAL   = calcium spikes (and the cups of water, one per spike)
  GREEN  = decoder activity (the water level, the decay curve, "on")
  RED    = switching off / loss ("off slowly")
  BLUE   = NFAT
  PURPLE = NF-kB
  YELLOW = the numbers to notice (one eighth, about 70 percent)
  GREY   = axes, labels, dashed question box, things not activated
  TEXT   = formula, headings

No molecular structures: factors are labelled chips; buckets are outlines; curves are computed
from the equation 0.5 ** (gap / half-time). The bucket scene and the bars are idealised.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"


def spike(x, y0, h, color=TEAL, w=0.22):
    m = VMobject(stroke_color=color, stroke_width=5)
    m.set_points_as_corners([[x - 0.04, y0, 0], [x, y0 + h, 0], [x + w, y0, 0]])
    return m


def train(xs, y0, x0, x1, h=0.9, color=TEAL):
    base = Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3)
    return VGroup(base, *[spike(x, y0, h, color) for x in xs])


class S00Title(TitleCard):
    LESSON = "The shape of a signal"
    TITLE = "Why a Slow Off Switch Can Count"


# ---------------------------------------------------------------------------------------------
class S01Count(SpokenScene):
    def construct(self):
        weak_x = [-2.4, 0.9, 4.2]
        strong_x = [-2.8 + 1.3 * i for i in range(7)]
        qbox = RoundedRectangle(corner_radius=0.14, width=3.4, height=1.1, stroke_color=GREY, stroke_width=3)
        qbox = DashedVMobject(qbox, num_dashes=40)
        q = T("?", 40, GREY)
        qgrp = VGroup(qbox, q).move_to([0, -1.6, 0])
        self.play(FadeIn(qgrp, scale=0.9), run_time=0.6)

        self.at("Calcium often rises")
        wl = T("weaker stimulus", 24, GREY).move_to([-4.9, 2.3, 0])
        sl = T("stronger stimulus", 24, GREY).move_to([-4.9, 0.4, 0])
        wt = train(weak_x, 2.0, -3.3, 5.4, h=1.2)
        st = train(strong_x, 0.1, -3.3, 5.4, h=1.2)
        self.play(FadeIn(wl), FadeIn(sl), Create(wt[0]), Create(st[0]), run_time=0.5)
        self.play(LaggedStart(*[Create(s) for s in wt[1:]], lag_ratio=0.5), run_time=1.0)

        self.at("stronger stimulus")
        self.play(LaggedStart(*[Create(s) for s in st[1:]], lag_ratio=0.3), Indicate(sl, color=TEAL), run_time=1.6)

        self.at("about the same height")
        guide = DashedLine([-3.3, 3.2, 0], [5.4, 3.2, 0], color=GREY, stroke_width=2)
        guide2 = DashedLine([-3.3, 1.3, 0], [5.4, 1.3, 0], color=GREY, stroke_width=2)
        self.play(Create(guide), Create(guide2), run_time=0.8)

        self.at("switches on fast")
        dec = chip("decoder", PURPLE, size=30).move_to([0, -1.6, 0])
        on = VGroup(T("on fast", 26, GREEN), T("↑", 30, GREEN)).arrange(RIGHT, buff=0.15).move_to([-3.6, -3.0, 0])
        self.play(ReplacementTransform(qgrp, dec), run_time=0.7)
        self.play(FadeIn(on, shift=UP * 0.1), run_time=0.5)
        self.at("off slowly")
        off = VGroup(T("off slowly", 26, RED), T("↓", 30, RED)).arrange(RIGHT, buff=0.15).move_to([3.6, -3.0, 0])
        self.play(FadeIn(off, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
BW, BH = 2.8, 3.8          # bucket inner width, height
BOT = -2.3                 # bucket bottom y
J, HL = 0.18, 1.0          # idealised: each cup adds 0.18; half-time 1 (arbitrary units)


def level(t, spikes):
    return sum(J * 0.5 ** ((t - s) / HL) for s in spikes if s <= t)


def bucket_outline(cx):
    l, r = cx - BW / 2, cx + BW / 2
    left = Line([l, BOT + BH, 0], [l, BOT, 0], color=GREY, stroke_width=5)
    bl = Line([l, BOT, 0], [cx - 0.14, BOT, 0], color=GREY, stroke_width=5)
    br = Line([cx + 0.14, BOT, 0], [r, BOT, 0], color=GREY, stroke_width=5)
    right = Line([r, BOT, 0], [r, BOT + BH, 0], color=GREY, stroke_width=5)
    return VGroup(left, bl, br, right)


def bucket_live(cx, trk, spikes):
    def water():
        h = max(level(trk.get_value(), spikes), 0.0) * BH * 1.0
        h = min(h, BH)
        r = Rectangle(width=BW - 0.12, height=max(h, 0.001), stroke_width=0,
                      fill_color=GREEN, fill_opacity=0.55 if h > 0.01 else 0)
        r.move_to([cx, BOT + 0.03 + max(h, 0.001) / 2, 0])
        return r

    def cup():
        t = trk.get_value()
        for s in spikes:
            if 0 <= t - s < 0.3:
                f = (t - s) / 0.3
                top = BOT + BH + 0.7
                surf = BOT + level(t, spikes) * BH
                y = top + (surf - top) * f
                return Circle(radius=0.15, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to([cx, y, 0])
        return Circle(radius=0.15, stroke_width=0, fill_opacity=0).move_to([cx, BOT + BH + 0.7, 0])

    def drip():
        t = trk.get_value()
        lv = level(t, spikes)
        f = (t * 2.5) % 1.0
        op = 1.0 if lv > 0.02 else 0.0
        return Circle(radius=0.07, stroke_width=0, fill_color=GREEN, fill_opacity=op * (1 - f)).move_to(
            [cx, BOT - 0.15 - 0.5 * f, 0])

    return always_redraw(water), always_redraw(cup), always_redraw(drip)


class S02Bucket(SpokenScene):
    def construct(self):
        cx_r, cx_o = -3.6, 3.6
        rare = [0.3, 3.3, 6.3]
        often = [0.3 + 0.5 * i for i in range(10)]
        tr, to = ValueTracker(0), ValueTracker(0)
        self.at("Picture a bucket")
        b1, b2 = bucket_outline(cx_r), bucket_outline(cx_o)
        self.play(Create(b1), Create(b2), run_time=1.0)
        hole = T("each bucket has a small hole", 22, GREY).move_to([0, BOT + 0.5, 0])
        self.play(FadeIn(hole), run_time=0.4)
        cupnote = T("one cup per spike", 24, TEAL).move_to([0, BOT + BH + 0.7, 0])
        self.at("topped up by one cup")
        self.play(FadeIn(cupnote), run_time=0.4)
        idea = T("idealised", 22, GREY).to_corner(DR, buff=0.5)
        self.add(idea)
        l1 = T("fill it rarely", 28, TEXT).move_to([cx_r, BOT - 0.75, 0])
        l2 = T("fill it often", 28, TEXT).move_to([cx_o, BOT - 0.75, 0])

        w1, c1, d1 = bucket_live(cx_r, tr, rare)
        self.at("Fill it rarely")
        self.add(w1, c1, d1)
        self.play(FadeIn(l1), run_time=0.3)
        run1 = max(self.t_of("Fill it often") - 0.25 - self.elapsed(), 0.5)
        self.play(tr.animate.set_value(2.0 * run1), run_time=run1, rate_func=linear)

        w2, c2, d2 = bucket_live(cx_o, to, often)
        self.at("Fill it often")
        self.add(w2, c2, d2)
        self.play(FadeIn(l2), run_time=0.3)
        run2 = max(self.narration_s - self.elapsed() - 0.2, 0.5)
        # rare keeps going so its drain stays visible
        self.play(to.animate.set_value(2.0 * run2), tr.animate.set_value(2.0 * (run1 + run2)),
                  run_time=run2, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rule(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[0, 70, 10], y_range=[0, 1.05, 0.25], x_length=9.2, y_length=3.7,
                  tips=False, axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False})
        ax.move_to([0.4, -0.75, 0])
        xl = VGroup(*[T(str(v), 22, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in (0, 20, 40, 60)])
        xt = T("gap since the last spike (seconds)", 22, GREY).next_to(ax, DOWN, buff=0.55)
        yl = VGroup(T("1", 22, GREY).next_to(ax.c2p(0, 1), LEFT, buff=0.15),
                    T("0", 22, GREY).next_to(ax.c2p(0, 0), LEFT, buff=0.15))
        yt = T("activity left", 22, GREY).next_to(ax.c2p(0, 1.05), UP, buff=0.12).align_to(ax.c2p(0, 1.05), LEFT)
        curve = ax.plot(lambda x: 0.5 ** (x / 20.0), x_range=[0, 70], color=GREEN, stroke_width=6)

        self.at("Take a decoder")
        self.play(Create(ax), FadeIn(xl), FadeIn(xt), FadeIn(yl), FadeIn(yt), run_time=0.9)
        self.play(Create(curve), run_time=1.4)

        self.at("The fraction left")
        lab = T("fraction left at the next spike", 22, GREY).move_to([0, 3.35, 0])
        f = M("= (1/2) ^ (gap ÷ half-time)", 30, TEXT).move_to([0, 2.75, 0])
        self.play(FadeIn(lab), Write(f), run_time=1.2)

        self.at("of 20 seconds")
        ex = T("example: half-time 20 s", 24, GREY).move_to(ax.c2p(52, 0.82))
        hdot = Dot(ax.c2p(20, 0.5), color=GREEN, radius=0.09)
        hline = DashedLine(ax.c2p(0, 0.5), ax.c2p(20, 0.5), color=GREY, stroke_width=2)
        hdrop = DashedLine(ax.c2p(20, 0.5), ax.c2p(20, 0), color=GREY, stroke_width=2)
        self.play(FadeIn(ex), Create(hline), Create(hdrop), FadeIn(hdot), run_time=0.9)

        self.at("a minute apart")
        v60 = DashedLine(ax.c2p(60, 0), ax.c2p(60, 0.125), color=YELLOW, stroke_width=3)
        d60 = Dot(ax.c2p(60, 0.125), color=YELLOW, radius=0.1)
        t60 = T("one eighth", 26, YELLOW).next_to(d60, UP, buff=0.3)
        self.play(Create(v60), FadeIn(d60), run_time=0.6)
        self.play(FadeIn(t60, shift=UP * 0.1), run_time=0.4)

        self.at("Spikes 10 seconds")
        v10 = DashedLine(ax.c2p(10, 0), ax.c2p(10, 0.7071), color=YELLOW, stroke_width=3)
        d10 = Dot(ax.c2p(10, 0.7071), color=YELLOW, radius=0.1)
        t10 = T("about 70%", 26, YELLOW).next_to(d10, UR, buff=0.12)
        self.play(Create(v10), FadeIn(d10), run_time=0.6)
        self.play(FadeIn(t10, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tf_chip(name, color, lit=True, size=24):
    c = chip(name, color, size=size, pad=0.18)
    if not lit:
        c.set_opacity(0.25)
    return c


class S04Tcells(SpokenScene):
    def construct(self):
        head = T("Human T cells · Dolmetsch, Xu and Lewis, 1998", 26, TEXT).move_to([0, 3.35, 0])
        self.at("In 1998")
        self.play(Write(head), run_time=1.4)

        x1 = [-5.6 + 0.9 * i for i in range(6)]
        x2 = [-5.2, -2.2]
        tr1 = train(x1, 1.0, -6.0, -0.6, h=1.1)
        tr2 = train(x2, -1.3, -6.0, -0.6, h=1.1)
        lab1 = T("closely spaced spikes", 24, TEAL).move_to([-3.3, 2.6, 0])
        lab2 = T("widely spaced spikes", 24, TEAL).move_to([-3.3, 0.3, 0])
        cx = [1.5, 3.5, 5.4]
        row1 = VGroup(tf_chip("NFAT", BLUE), tf_chip("NF-κB", PURPLE), tf_chip("one more", GREY, size=22))
        row2 = VGroup(tf_chip("NFAT", BLUE, False), tf_chip("NF-κB", PURPLE), tf_chip("one more", GREY, False, size=22))
        for g, y in ((row1, 1.2), (row2, -1.1)):
            for c, x in zip(g, cx):
                c.move_to([x, y, 0])
        key = T("bright = activated", 22, GREY).move_to([3.5, -2.1, 0])

        self.at("imposed calcium spikes")
        self.play(FadeIn(lab1), FadeIn(lab2), Create(tr1[0]), Create(tr2[0]), run_time=0.6)
        self.at("Closely spaced")
        self.play(LaggedStart(*[Create(s) for s in tr1[1:]], lag_ratio=0.3), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in row1], lag_ratio=0.3), run_time=0.9)
        self.at("Widely spaced")
        self.play(LaggedStart(*[Create(s) for s in tr2[1:]], lag_ratio=0.6), run_time=1.0)
        self.play(FadeIn(row2), FadeIn(key), run_time=0.7)
        self.play(Indicate(row2[1], color=PURPLE, scale_factor=1.1), run_time=0.7)

        # ---- reason: how fast each one switches off
        self.at("how fast each")
        self.play(FadeOut(VGroup(head, tr1, tr2, lab1, lab2, row1, row2, key)), run_time=0.5)
        sub = T("how fast each factor switches off", 26, TEXT).move_to([0, 2.7, 0])
        self.play(FadeIn(sub), run_time=0.4)
        xl = -2.6
        cal = DashedLine([xl, 1.8, 0], [xl, -2.0, 0], color=TEAL, stroke_width=3)
        callab = T("calcium falls", 22, TEAL).next_to(cal, UP, buff=0.08)
        nf = tf_chip("NFAT", BLUE).move_to([-4.9, 0.9, 0])
        nk = tf_chip("NF-κB", PURPLE).move_to([-4.9, -0.9, 0])
        self.play(Create(cal), FadeIn(callab), FadeIn(nf), FadeIn(nk), run_time=0.8)

        self.at("leaves the nucleus")
        bar1 = Rectangle(width=1.6, height=0.4, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
        bar1.move_to([xl + 0.8, 0.9, 0])
        t1 = T("leaves the nucleus within minutes", 24, BLUE).move_to([xl + 2.0, 0.3, 0])
        t1.align_to(bar1, LEFT).shift(RIGHT * 0.2)
        self.play(GrowFromEdge(bar1, LEFT), run_time=0.6)
        self.play(FadeIn(t1), run_time=0.4)

        self.at("In B cells")
        tag = T("B cells", 22, PURPLE).next_to(nk, DOWN, buff=0.12)
        self.play(FadeIn(tag), run_time=0.4)
        self.at("It stayed")
        parts = [Rectangle(width=5.2, height=0.4, stroke_width=0, fill_color=PURPLE, fill_opacity=0.9).move_to([xl + 2.6, -0.9, 0])]
        for i, op in enumerate([0.65, 0.45, 0.28, 0.14, 0.05]):
            parts.append(Rectangle(width=0.36, height=0.4, stroke_width=0, fill_color=PURPLE, fill_opacity=op).move_to([xl + 5.2 + 0.18 + 0.36 * i, -0.9, 0]))
        bar2 = VGroup(*parts)
        t2 = VGroup(T("stays in the nucleus: more than 16 minutes", 24, PURPLE),
                    T("after a brief calcium spike", 24, PURPLE)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        t2.next_to(bar2, DOWN, buff=0.18).align_to(bar2, LEFT).shift(RIGHT * 0.2)
        ns = T("idealised, not to scale", 26, TEXT).to_corner(UR, buff=0.5)
        self.play(FadeIn(bar2, shift=RIGHT * 0.6), FadeIn(ns), run_time=1.2)
        self.play(FadeIn(t2), run_time=0.5)

        self.at("holds on between spikes")
        ban = chip("holds on between spikes: can count", GREEN, size=28).move_to([0, -3.0, 0])
        self.play(FadeIn(ban, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S05End(EndCard):
    LINE = "A decoder that holds on between spikes can count."
