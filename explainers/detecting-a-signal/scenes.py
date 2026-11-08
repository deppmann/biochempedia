"""How we know: detecting a signal. One idea: in a radioimmunoassay, the more hormone in the sample,
the less labelled hormone the antibody holds.  Timed to the spoken words with self.at("...").

COLOR MAP (one color per concept, whole video)
  YELLOW = insulin / the hormone being measured (labelled or not)
  PINK   = the radioactive label, and the label held by the antibody (gauge, curve, "bound")
  BLUE   = the antibody and its binding sites (cups)
  GREY   = tubes, blood lanes, axes, labels, background molecules, "free"
  TEXT   = ordinary words
No molecular structures: insulin is a dot, the label a small dot on it, the antibody a bar with cups.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#F08BB4"

CX = -2.7                 # tube centre x
SEAT_Y = -2.38
CUP_DX = 0.95
GX, GY, GH, GW = 5.6, -1.2, 3.6, 0.9      # gauge


def seat(i, cx=CX):
    return np.array([cx + (i - 2.5) * CUP_DX, SEAT_Y, 0])


# ------------------------------------------------------------------ pieces
def antibody(cx=CX, by=-2.95, s=1.0, color=BLUE):
    bar = RoundedRectangle(corner_radius=0.1 * s, width=5.9 * s, height=0.3 * s, stroke_width=0,
                           fill_color=color, fill_opacity=0.9).move_to([cx, by, 0])
    cups = []
    for i in range(6):
        c = np.array([cx + (i - 2.5) * CUP_DX * s, by + 0.45 * s, 0])
        cups.append(AnnularSector(inner_radius=0.27 * s, outer_radius=0.37 * s, angle=200 * DEGREES,
                                  start_angle=170 * DEGREES, color=color, fill_opacity=1, stroke_width=0).shift(c))
    return VGroup(bar, *cups)


def tube():
    t = VMobject(stroke_color=GREY, stroke_width=4)
    t.set_points_as_corners([[-5.9, 2.2, 0], [-5.9, -3.2, 0], [0.5, -3.2, 0], [0.5, 2.2, 0]])
    return t


def ldot(pos, r=0.2):
    """labelled insulin: a yellow dot with a small pink radioactive tag."""
    pos = np.array(list(pos) + [0] * (3 - len(pos)), float)
    body = Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(pos)
    tag = Circle(radius=r * 0.45, stroke_color=BG, stroke_width=2, fill_color=PINK, fill_opacity=1).move_to(pos + r * np.array([0.8, 0.8, 0]))
    return VGroup(body, tag)


def sdot(pos, r=0.2):
    """sample insulin: a yellow dot, no label."""
    return Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(np.array(list(pos) + [0] * (3 - len(pos)), float))


def gauge(tr):
    out = Rectangle(width=GW, height=GH, stroke_color=GREY, stroke_width=3).move_to([GX, GY, 0])
    fill = always_redraw(lambda: Rectangle(width=GW, height=max(0.001, GH * tr.get_value()), stroke_width=0,
                                           fill_color=PINK, fill_opacity=0.85).align_to(out, DOWN).align_to(out, LEFT))
    title = VGroup(T("label held", 24, PINK), T("by antibody", 24, PINK)).arrange(DOWN, buff=0.08).move_to([GX, 1.3, 0])
    return out, fill, title


def key_label(y=-0.2):
    d = ldot([1.3, y])
    t = T("labelled insulin", 24, TEXT).move_to([1.7, y, 0], aligned_edge=LEFT)
    return VGroup(d, t)


def key_sample(y=-0.9):
    d = sdot([1.3, y])
    t = T("sample insulin", 24, TEXT).move_to([1.7, y, 0], aligned_edge=LEFT)
    return VGroup(d, t)


FLOAT3 = [(-5.0, 0.9), (-3.7, 1.5), (-2.4, 0.8), (-1.0, 1.4), (-4.2, -0.5), (-1.6, -0.3)]


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "How We Know: Detecting a Signal"
    TITLE = "More Hormone, Less Label"


class S01Scarce(SpokenScene):
    def construct(self):
        rng = np.random.default_rng(3)
        dots = VGroup()
        for gx in np.arange(-6.2, 6.3, 0.42):
            for gy in np.arange(-3.4, 3.5, 0.42):
                dots.add(Dot([gx + rng.uniform(-.12, .12), gy + rng.uniform(-.12, .12), 0], radius=0.07, color=GREY).set_opacity(0.6))
        lone = Dot([2.1, -1.2, 0], radius=0.15, color=YELLOW)
        blood = T("fasting blood", 30, GREY, weight=BOLD)
        blood_bg = SurroundingRectangle(blood, buff=0.2, corner_radius=0.12, stroke_width=0, fill_color=BG, fill_opacity=0.95)
        bl = VGroup(blood_bg, blood).move_to([0, 3.05, 0])
        self.add(dots)
        self.at("Fasting blood")
        self.play(FadeIn(bl), run_time=0.4)
        self.at("insulin at")
        self.play(FadeIn(lone, scale=3), run_time=0.5)
        self.play(Indicate(lone, color=YELLOW, scale_factor=2.2), run_time=0.6)
        ring = Circle(radius=0.45, stroke_color=YELLOW, stroke_width=4).move_to(lone)
        lab = VGroup(RoundedRectangle(corner_radius=0.12, width=2.6, height=0.7, stroke_width=0, fill_color=BG, fill_opacity=0.95),
                     T("one insulin", 28, YELLOW, weight=BOLD)).move_to([2.1, -2.2, 0])
        lab[1].move_to(lab[0])
        self.at("one insulin molecule")
        self.play(Create(ring), FadeIn(lab), run_time=0.5)
        water = T("a trillion water molecules", 28, GREY)
        wbg = SurroundingRectangle(water, buff=0.2, corner_radius=0.12, stroke_width=0, fill_color=BG, fill_opacity=0.95)
        wl = VGroup(wbg, water).move_to([-2.4, 0.4, 0])
        self.at("trillion molecules")
        self.play(FadeIn(wl, shift=UP * 0.1), run_time=0.5)
        self.at("rests on")
        self.play(ring.animate(rate_func=there_and_back).scale(1.8), run_time=0.8)
        self.at("something that scarce")
        self.play(ring.animate(rate_func=there_and_back).scale(1.8), run_time=0.8)
        q = T("?", 120, TEXT, weight=BOLD)
        qbg = Circle(radius=0.95, stroke_width=0, fill_color=BG, fill_opacity=0.95)
        qq = VGroup(qbg, q).move_to([0, 0, 0])
        self.at("How can anyone")
        self.play(FadeOut(wl), FadeIn(qq, scale=0.5), run_time=0.5)
        self.at("and Solomon")
        self.play(FadeOut(dots), FadeOut(lone), FadeOut(ring), FadeOut(lab), FadeOut(bl), FadeOut(qq), run_time=0.5)
        n1 = chip("Rosalyn Yalow", TEXT, 36)
        n2 = chip("Solomon Berson", TEXT, 36)
        names = VGroup(n1, n2).arrange(RIGHT, buff=0.8).move_to([0, 0.9, 0])
        self.play(FadeIn(n1, shift=UP * 0.2), FadeIn(n2, shift=UP * 0.2), run_time=0.5)
        self.at("found a way")
        way = T("a way to measure it", 34, YELLOW).move_to([0, -0.4, 0])
        self.play(FadeIn(way, shift=UP * 0.15), run_time=0.5)
        self.at("unexpected")
        bp = chip("a by-product of a different experiment", GREY, 30).move_to([0, -1.7, 0])
        self.play(FadeIn(bp, shift=UP * 0.15), run_time=0.5)
        self.finish()


def lane(y, label, color=GREY):
    band = RoundedRectangle(corner_radius=0.25, width=12.2, height=1.5, stroke_color=GREY, stroke_width=2,
                            fill_color=GREY, fill_opacity=0.12).move_to([0, y, 0])
    lab = T(label, 26, TEXT).move_to([-6.0, y + 1.1, 0], aligned_edge=LEFT)
    return band, lab


class S02Holder(SpokenScene):
    def construct(self):
        q = fit(T("Do people with adult-onset diabetes destroy insulin too fast?", 30, TEXT), max_w=12.2).move_to([0, 0.4, 0])
        self.at("testing whether")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)

        big = ldot([0, 0.5, 0], 0.45)
        t_ins = T("insulin", 30, YELLOW).move_to([-2.3, 0.5, 0])
        t_tag = T("radioactive iodine", 30, PINK).move_to([3.6, 1.45, 0])
        ln = Line([1.7, 1.3, 0], big[1].get_center() + RIGHT * 0.15, color=PINK, stroke_width=3)
        self.at("destroy insulin")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("tagged insulin")
        self.play(FadeOut(q), FadeIn(big, scale=0.6), FadeIn(t_ins), run_time=0.6)
        self.at("radioactive iodine")
        self.play(FadeIn(t_tag), Create(ln), Indicate(big[1], color=PINK, scale_factor=1.8), run_time=0.7)

        band = RoundedRectangle(corner_radius=0.25, width=12.2, height=1.1, stroke_color=GREY, stroke_width=2,
                                fill_color=GREY, fill_opacity=0.12).move_to([0, 0.4, 0])
        blood = T("blood", 26, TEXT).move_to([-6.0, 1.3, 0], aligned_edge=LEFT)
        small = ldot([-5.4, 0.4, 0], 0.17)
        self.at("injected it")
        self.play(FadeOut(t_ins), FadeOut(t_tag), FadeOut(ln), FadeIn(band), FadeIn(blood), Transform(big, small), run_time=0.8)
        self.at("followed the radioactivity")
        self.play(big.animate.shift(RIGHT * 10.9), run_time=1.6, rate_func=linear)
        self.play(FadeOut(big), run_time=0.15)

        # two groups of people
        b1, l1 = lane(1.35, "other people")
        b2, l2 = lane(-1.4, "people treated with insulin")
        d1 = [ldot([-5.7 + 0.5 * k, 1.35, 0], 0.15) for k in range(4)]
        d2 = [ldot([-5.7 + 0.5 * k, -1.05, 0], 0.15) for k in range(4)]
        ab = antibody(2.5, -1.9, 0.75, GREY)
        self.at("already treated")
        self.play(FadeOut(band), FadeOut(blood), FadeIn(b1), FadeIn(l1), FadeIn(b2), FadeIn(l2),
                  *[FadeIn(d) for d in d1 + d2], run_time=0.8)
        self.at("more slowly")
        tgt = [np.array([2.5 + (k - 2.5) * 0.95 * 0.75, -1.05, 0]) for k in range(4)]
        self.play(*[d.animate.shift(RIGHT * 11.8) for d in d1], *[d2[k].animate.move_to(tgt[k] - [0.0, 0, 0] - np.array([0, 0, 0])) for k in range(4)],
                  run_time=2.0, rate_func=linear)
        for d in d1:
            self.remove(d)
        self.at("was holding")
        drops = [d2[k].animate.move_to(np.array([2.5 + (k - 2.5) * 0.95 * 0.75, -1.47, 0])) for k in range(4)]
        self.play(FadeIn(ab), *drops, run_time=0.6)
        lab_ab = T("antibody", 28, BLUE, weight=BOLD).move_to([2.5, -2.55, 0])
        self.at("an antibody")
        self.play(ab.animate.set_color(BLUE), FadeIn(lab_ab), run_time=0.5)
        doubt = fit(T("doubted: so small a protein could raise antibodies", 28, GREY), max_w=12).move_to([0, 3.15, 0])
        self.at("Immunologists")
        self.play(FadeIn(doubt, shift=DOWN * 0.1), run_time=0.5)
        self.at("protein as small")
        self.play(*[d.animate.shift(UP * 0.4) for d in d2], run_time=0.4)
        self.play(*[d.animate.shift(RIGHT * 9.5) for d in d2], run_time=2.2, rate_func=linear)
        for d in d2:
            self.remove(d)
        self.at("Then they used")
        self.play(FadeOut(doubt), run_time=0.4)
        final = antibody(CX, -2.95, 1.0, BLUE)
        self.at("as a scale")
        self.play(FadeOut(b1), FadeOut(l1), FadeOut(b2), FadeOut(l2), FadeOut(lab_ab), Transform(ab, final), run_time=1.0)
        self.finish()


class S03Tube(SpokenScene):
    def construct(self):
        ab = antibody()
        self.add(ab)
        tb = tube()
        self.at("Take a tube")
        self.play(Create(tb), run_time=0.9)
        lab = T("antibody", 28, BLUE, weight=BOLD).move_to([CX, -1.75, 0])
        self.at("fixed, small amount of antibody")
        self.play(FadeIn(lab), Indicate(ab, color=BLUE, scale_factor=1.03), run_time=0.7)
        dots = [ldot([x, 3.3 if i < 4 else 2.7, 0]) for i, (x, y) in enumerate(FLOAT3)]
        key = key_label()
        self.at("radioactive insulin")
        self.play(*[FadeIn(d) for d in dots], FadeIn(key), run_time=0.3)
        self.play(*[d.animate.move_to([FLOAT3[i][0], FLOAT3[i][1], 0]) for i, d in enumerate(dots)],
                  run_time=1.3, lag_ratio=0.0)
        self.at("same amounts")
        self.play(*[Indicate(d[0], color=TEXT, scale_factor=1.25) for d in dots], Indicate(ab, color=BLUE, scale_factor=1.03), run_time=0.9)
        self.at("counter can find")
        self.play(*[Indicate(d[1], color=PINK, scale_factor=1.7) for d in dots], run_time=0.8)
        sites = T("a few binding sites", 28, BLUE, weight=BOLD).move_to([CX, -1.75, 0])
        self.at("few binding sites")
        self.play(Transform(lab, sites), run_time=0.4)
        tr = ValueTracker(0)
        out, fill, title = gauge(tr)
        self.at("fills them")
        self.add(fill)
        self.play(FadeIn(out), FadeIn(title), run_time=0.3)
        self.play(*[dots[i].animate.move_to(seat(i)) for i in range(6)], tr.animate.set_value(1.0), run_time=1.2)
        self.finish()


class S04Compete(SpokenScene):
    def construct(self):
        ab = antibody()
        tb = tube()
        dots = [ldot(seat(i)) for i in range(6)]
        key = key_label()
        tr = ValueTracker(1.0)
        out, fill, title = gauge(tr)
        self.add(tb, ab, *dots, key, out, fill, title)

        chipb = chip("blood sample", YELLOW, 26).move_to([CX, 3.1, 0])
        head = T("insulin in the sample", 24, TEXT).move_to([4.0, 3.15, 0])

        def val(txt):
            return T(txt, 32, YELLOW, weight=BOLD).move_to([4.0, 2.55, 0])
        v = val("none")
        self.at("Now add the")
        self.play(FadeIn(chipb, shift=DOWN * 0.1), FadeIn(head), FadeIn(v), run_time=0.5)
        ks = key_sample()
        self.at("carries no label")
        self.play(FadeIn(ks), run_time=0.4)
        self.play(Indicate(ks[0], color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.at("same few sites")
        self.play(Indicate(ab, color=BLUE, scale_factor=1.03), run_time=0.8)

        # case 1: a little
        v1 = val("a little")
        s1 = [sdot([CX - 0.4 + 0.8 * k, 2.5, 0]) for k in range(2)]
        self.at("A little sample")
        self.play(Transform(v, v1), *[FadeIn(s, scale=0.4) for s in s1], run_time=0.5)
        out1 = {1: (-4.5, -1.1), 4: (-0.85, -1.0)}
        self.at("displaces a few")
        self.play(*[dots[i].animate.move_to([out1[i][0], out1[i][1], 0]) for i in (1, 4)], tr.animate.set_value(4 / 6), run_time=0.5)
        self.play(*[s1[k].animate.move_to(seat(i)) for k, i in enumerate((1, 4))], run_time=0.6)

        # reset to the neutral state (no sample insulin) before the next case
        v0 = val("none")
        self.at("and a lot")
        self.play(*[FadeOut(s) for s in s1], *[dots[i].animate.move_to(seat(i)) for i in (1, 4)],
                  tr.animate.set_value(1.0), Transform(v, v0), run_time=0.5)

        # case 2: a lot
        v2 = val("a lot")
        s2 = [sdot([CX - 1.2 + 0.8 * k, 2.5, 0]) for k in range(4)]
        out2 = {0: (-5.2, -1.0), 2: (-3.6, -0.7), 3: (-2.0, -1.1), 5: (-0.3, -0.6)}
        self.at("displaces many")
        self.play(Transform(v, v2), *[FadeIn(s, scale=0.4) for s in s2], run_time=0.4)
        self.play(*[dots[i].animate.move_to([out2[i][0], out2[i][1], 0]) for i in out2], tr.animate.set_value(2 / 6), run_time=0.5)
        self.play(*[s2[k].animate.move_to(seat(i)) for k, i in enumerate(out2)], run_time=0.7)
        self.at("less radioactivity")
        self.play(Indicate(title, color=TEXT, scale_factor=1.1), Indicate(out, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.finish()


def f_curve(x):
    return 0.08 + 0.88 / (1 + np.exp(0.85 * (x - 5.0)))


class S05Curve(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.05, 0.5], x_length=8.4, y_length=4.5,
                  axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 4,
                               "tip_length": 0.2}).move_to([-1.1, -0.2, 0])
        ylab = T("label held by the antibody", 24, PINK).rotate(90 * DEGREES).move_to([-6.0, -0.2, 0])
        xlab = T("insulin in the sample", 26, YELLOW).move_to([-1.1, -3.1, 0])
        self.at("Now repeat")
        self.play(Create(ax), FadeIn(ylab), run_time=0.8)
        self.at("known amounts")
        self.play(FadeIn(xlab), run_time=0.4)
        xs = [1.0, 3.0, 5.0, 7.0, 9.0]
        pts = [Dot(ax.c2p(x, f_curve(x)), radius=0.14, color=PINK) for x in xs]
        self.play(LaggedStart(*[FadeIn(p, scale=2) for p in pts], lag_ratio=0.5), run_time=1.6)
        self.at("same antibody")
        self.play(*[Indicate(p, color=TEXT, scale_factor=1.6) for p in pts], run_time=0.9)
        curve = ax.plot(f_curve, x_range=[0.3, 9.7], color=PINK, stroke_width=5)
        self.at("build a curve")
        self.play(Create(curve), run_time=1.2)
        cb = chip("bound", PINK, 28)
        cf = chip("free", GREY, 28)
        cc = VGroup(cb, cf).arrange(DOWN, buff=0.5).move_to([5.0, 1.7, 0])
        self.at("Separate the bound")
        self.play(FadeIn(cb, shift=LEFT * 0.1), run_time=0.4)
        self.play(FadeIn(cf, shift=LEFT * 0.1), run_time=0.4)
        cnt = T("count each", 28, TEXT).move_to([5.0, 0.3, 0])
        self.at("count each")
        self.play(FadeIn(cnt), Indicate(cb, color=TEXT), Indicate(cf, color=TEXT), run_time=0.8)
        px = 5.9
        py = f_curve(px)
        h = DashedLine(ax.c2p(0, py), ax.c2p(px, py), color=PINK, stroke_width=4)
        vl = DashedLine(ax.c2p(px, py), ax.c2p(px, 0), color=YELLOW, stroke_width=4)
        pdot = Dot(ax.c2p(px, py), radius=0.16, color=TEXT)
        base = Dot(ax.c2p(px, 0), radius=0.16, color=YELLOW)
        pat = T("patient", 26, TEXT).move_to(ax.c2p(px, py / 2) + LEFT * 0.75)
        self.at("and read the")
        self.play(Create(h), run_time=0.6)
        self.play(FadeIn(pdot, scale=2), Create(vl), run_time=0.7)
        self.play(FadeIn(base, scale=2), FadeIn(pat), run_time=0.4)
        ttl = T("radioimmunoassay", 30, TEXT, weight=BOLD).move_to([4.6, 3.0, 0])
        self.at("This is the")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), run_time=0.5)
        lo = T("range depends on assay", 24, GREY).move_to(ax.c2p(0, 0) + DOWN * 0.75 + RIGHT * 1.6)
        self.at("Its range depends")
        self.play(FadeOut(xlab), FadeIn(lo), run_time=0.5)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        cup = AnnularSector(inner_radius=0.8, outer_radius=1.1, angle=200 * DEGREES, start_angle=170 * DEGREES,
                            color=BLUE, fill_opacity=1, stroke_width=0).move_to([0, 0.1, 0])
        stem = RoundedRectangle(corner_radius=0.1, width=0.5, height=1.4, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).next_to(cup, DOWN, buff=-0.1)
        ab = VGroup(stem, cup)
        ablab = T("antibody", 30, BLUE, weight=BOLD).next_to(ab, DOWN, buff=0.25)
        c1 = chip("cortisol", YELLOW, 32).move_to([-4.2, 0.9, 0])
        c2 = chip("corticosterone", YELLOW, 32).move_to([4.2, 0.9, 0])
        d = T("differ by one hydroxyl group", 30, GREY).next_to(ablab, DOWN, buff=0.45)
        self.at("An antibody can")
        self.play(FadeIn(ab, shift=UP * 0.2), FadeIn(ablab), run_time=0.6)
        self.at("cortisol")
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.4)
        self.at("two steroids")
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.4)
        self.at("differ by one")
        self.play(FadeIn(d), run_time=0.5)
        self.at("So the assay")
        eg = T("for example", 26, GREY).move_to([-2.5, 0.35, 0])
        self.play(c1.animate.scale(0.7).move_to([0, 0.35, 0]), run_time=0.7)
        self.play(FadeIn(eg), run_time=0.3)
        self.play(c2.animate.move_to([2.1, 1.35, 0]), run_time=0.6)
        self.play(c2.animate.move_to([4.2, 0.9, 0]).set_opacity(0.5), run_time=0.6)

        self.at("Bioseis")
        self.play(FadeOut(eg), FadeOut(ab), FadeOut(ablab), FadeOut(c1), FadeOut(c2), FadeOut(d), run_time=0.4)
        r1 = chip("a bioassay: what a hormone does", GREY, 32).move_to([0, 1.5, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.5)
        self.at("This counts")
        r2 = fit(chip("this assay: what the antibody recognises", YELLOW, 32), max_w=12.2).move_to([0, -0.3, 0])
        cnt = VGroup(*[sdot([0, 0, 0], 0.18) for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([0, -1.6, 0])
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in cnt], lag_ratio=0.4), run_time=1.2)

        self.at("Keep this rule")
        self.play(FadeOut(r1), FadeOut(r2), FadeOut(cnt), run_time=0.4)
        a = chip("more hormone in the sample", YELLOW, 30).move_to([-3.2, 2.6, 0])
        b = chip("less label on the antibody", PINK, 30).move_to([3.2, 2.6, 0])
        ar = Arrow(a.get_right(), b.get_left(), buff=0.15, color=TEXT, stroke_width=6)
        self.play(FadeIn(a, shift=RIGHT * 0.1), run_time=0.4)
        self.play(GrowArrow(ar), FadeIn(b, shift=LEFT * 0.1), run_time=0.5)
        # a small tube: more sample insulin in, less label held
        cups = antibody(0, -1.5, 1.1)
        pos = [np.array([(i - 2.5) * 0.95 * 1.1, -0.87, 0]) for i in range(6)]
        held = [ldot(p, 0.2) for p in pos]
        self.play(FadeIn(cups), *[FadeIn(h) for h in held], run_time=0.4)
        taken = (0, 2, 3, 5)
        sm = [sdot([pos[i][0], 1.1, 0], 0.2) for i in taken]
        self.play(LaggedStart(*[FadeIn(s_, scale=0.3) for s_ in sm], lag_ratio=0.3), run_time=0.8)
        self.play(*[held[i].animate.shift(UP * 1.0 + RIGHT * {0: 0.0, 2: -0.45, 3: 0.45, 5: 0.0}[i]) for i in taken], run_time=0.5)
        self.play(*[sm[k].animate.move_to(pos[i]) for k, i in enumerate(taken)], run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "More hormone in the sample means less label on the antibody."
