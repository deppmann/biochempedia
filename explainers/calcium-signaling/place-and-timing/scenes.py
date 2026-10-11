"""Calcium signaling, section film: where and how often calcium rises  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = calcium (ions, spikes)
  BLUE   = the channel
  PURPLE = calmodulin
  ORANGE = hormone (the stimulus)
  GREEN  = active / "sees it"
  GOLD   = phosphate badge
  RED    = "no" (crossed out)
  GREY   = membrane, buffers, protein that sees nothing, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ca_dot(pos, r=0.1):
    return Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(pos)


def pbadge(size=0.22):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def spike_pts(x0, base, width, height, times, tmax, rise=0.08, tau=0.3):
    """polyline points of a spike train drawn from an equation (idealised)."""
    ts = np.linspace(0, tmax, int(tmax / 0.02) + 1)
    pts = []
    for t in ts:
        v = 0.0
        for s in times:
            if t >= s:
                dt = t - s
                v = max(v, min(dt / rise, 1.0) * np.exp(-max(dt - rise, 0) / tau))
        pts.append([x0 + width * t / tmax, base + height * v, 0])
    return pts


def line_from(pts, color, w=5):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([np.array(p) for p in pts])
    return m


def legend_item(kind, text, color):
    if kind == "dot":
        sw = Circle(radius=0.1, stroke_width=0, fill_color=color, fill_opacity=1)
    else:
        sw = pbadge(0.15)
    return VGroup(sw, T(text, 22, color)).arrange(RIGHT, buff=0.15)


class S00Title(TitleCard):
    LESSON = "Calcium signaling"
    TITLE = "Where and how often calcium rises"


# ---------------------------------------------------------------------------------------------
class S01Place(SpokenScene):
    @staticmethod
    def P(x, y):
        return [-1.5 + (x + 3.2) * 1.7, 2.6 + (y - 2.6) * 1.35, 0]

    def construct(self):
        P = self.P
        mem = RoundedRectangle(corner_radius=0.1, width=12.6, height=0.32, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([0, 2.6, 0])
        out_l = T("outside", 22, GREY).move_to([5.4, 3.2, 0])
        cyt_l = T("cytosol", 22, GREY).move_to([5.4, -3.2, 0])
        chan = RoundedRectangle(corner_radius=0.14, width=1.2, height=0.7, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.5).move_to(P(-3.2, 2.6))
        chan_l = T("channel", 24, BLUE).move_to([-1.5, 3.25, 0])
        leg = legend_item("dot", "calcium", YELLOW).move_to([-5.2, -3.15, 0])
        sch = T("schematic, not to scale", 22, GREY).move_to([2.0, -3.2, 0])
        self.play(FadeIn(mem), FadeIn(out_l), FadeIn(cyt_l), FadeIn(chan), FadeIn(chan_l), FadeIn(leg), FadeIn(sch), run_time=0.8)

        self.at("same ion")
        where = T("WHERE", 24, TEXT, weight=BOLD).move_to([-5.7, 3.25, 0])
        self.play(FadeIn(where, shift=DOWN * 0.1), run_time=0.4)
        self.at("and when")
        when = T("WHEN", 24, TEXT, weight=BOLD).move_to([-4.5, 3.25, 0])
        self.play(FadeIn(when, shift=DOWN * 0.1), run_time=0.4)

        bpos = [(-5.3, 0.6), (-4.4, -0.5), (-1.1, 0.6), (-2.0, -0.5)]
        buffers = VGroup(*[RoundedRectangle(corner_radius=0.2, width=1.2, height=0.75, stroke_color=GREY,
                                            stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to(P(x, y))
                           for x, y in bpos])
        blab = T("buffer proteins", 24, GREY).move_to([-1.5, -2.55, 0])
        self.at("Buffer proteins")
        self.play(FadeIn(buffers, lag_ratio=0.2), FadeIn(blab), run_time=0.8)

        near = [(-3.9, 2.15), (-3.2, 2.05), (-2.5, 2.15), (-4.4, 1.85), (-3.55, 1.75), (-2.85, 1.75), (-2.0, 1.85),
                (-3.2, 2.35)]
        far_start = [(-4.4, 1.95), (-2.0, 1.95), (-4.6, 1.6), (-1.8, 1.6)]
        far_end = [bpos[0], bpos[2], bpos[1], bpos[3]]
        start = P(-3.2, 2.3)
        nd = VGroup(*[ca_dot(start, 0.14) for _ in near])
        fd = VGroup(*[ca_dot(start, 0.14) for _ in far_start])
        self.add(nd, fd)
        self.at("capture a free")
        self.play(*[d.animate.move_to(P(x, y)) for d, (x, y) in zip(nd, near)],
                  *[d.animate.move_to(P(x, y)) for d, (x, y) in zip(fd, far_start)], run_time=0.8)
        self.at("does not travel far")
        self.play(*[d.animate.move_to(P(x, y)).scale(0.2) for d, (x, y) in zip(fd, far_end)], run_time=1.0)
        self.play(*[FadeOut(d) for d in fd],
                  *[Indicate(b, color=GREY, scale_factor=1.15) for b in buffers], run_time=0.5)

        pa = chip("protein", PURPLE, size=28).move_to(P(-3.2, 0.95))
        self.at("A protein beside")
        self.play(FadeIn(pa, scale=0.9), run_time=0.5)
        self.at("sees a high level")
        ha = T("sees a high level", 26, GREEN).next_to(pa, DOWN, buff=0.2)
        self.play(pa[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.3), FadeIn(ha), run_time=0.5)
        pb = chip("protein", PURPLE, size=28).move_to([5.1, -1.0, 0])
        self.at("A protein across")
        self.play(FadeIn(pb, scale=0.9), run_time=0.5)
        self.at("sees nothing")
        hb = T("sees nothing", 26, GREY).next_to(pb, DOWN, buff=0.2)
        self.play(pb.animate.set_opacity(0.5), FadeIn(hb), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Spikes(SpokenScene):
    X0, W, TMAX = -3.2, 9.2, 12.0

    def panel(self, yc, times, label, color=ORANGE):
        base = yc - 0.8
        axis = Line([self.X0, base, 0], [self.X0 + self.W, base, 0], color=GREY, stroke_width=3)
        lab = T(label, 24, color).move_to([self.X0, yc + 1.15, 0], aligned_edge=LEFT)
        lab.align_to([self.X0, 0, 0], LEFT)
        trace = line_from(spike_pts(self.X0, base, self.W, 1.6, times, self.TMAX), YELLOW, 5)
        return axis, lab, trace, base

    def construct(self):
        when = T("WHEN", 24, TEXT, weight=BOLD).move_to([-5.7, 3.25, 0])
        ideal = T("idealised traces", 22, GREY).move_to([5.0, -3.15, 0])
        ax1, lab1, tr1, base1 = self.panel(1.35, [1.5, 5.5, 9.5], "steady stimulus")
        self.at("Under a steady")
        self.play(Create(ax1), FadeIn(lab1), FadeIn(ideal), FadeIn(when), run_time=0.6)
        # held-high plateau, crossed out
        plateau = DashedLine([self.X0, base1 + 1.5, 0], [self.X0 + self.W, base1 + 1.5, 0], color=YELLOW,
                             stroke_width=5)
        self.at("do not hold")
        self.play(Create(plateau), run_time=0.6)
        cx = VGroup(Line([1.3, base1 + 1.9, 0], [1.9, base1 + 1.1, 0], color=RED, stroke_width=8),
                    Line([1.3, base1 + 1.1, 0], [1.9, base1 + 1.9, 0], color=RED, stroke_width=8))
        self.play(Create(cx), run_time=0.3)
        self.at("spike again")
        self.play(FadeOut(plateau), FadeOut(cx), run_time=0.3)
        self.play(Create(tr1), run_time=2.0, rate_func=linear)

        # the experiment
        cell = Circle(radius=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15
                      ).move_to([-5.2, 0.2, 0])
        rep = chip("reporter", TEXT, size=22).move_to(cell)
        cl = T("single rat\nliver cell", 22, GREY).next_to(cell, DOWN, buff=0.2)
        att = chip("Woods, Cuthbertson, Cobbold, 1986", GOLD, size=24).move_to([0.5, 3.25, 0])
        self.at("injected")
        self.play(FadeIn(att), FadeIn(cell), FadeIn(cl), run_time=0.6)
        self.at("calcium reporter")
        self.play(FadeIn(rep, scale=0.9), run_time=0.5)

        ax2, lab2, tr2, base2 = self.panel(-1.35, [0.8, 2.3, 3.8, 5.3, 6.8, 8.3, 9.8], "more hormone")
        lab1b = T("less hormone", 24, ORANGE).move_to(lab1.get_left(), aligned_edge=LEFT)
        self.at("The more hormone")
        self.play(ReplacementTransform(lab1, lab1b), Create(ax2), FadeIn(lab2), run_time=0.6)
        self.at("more often")
        self.play(Create(tr2), run_time=2.0, rate_func=linear)

        self.at("written in frequency")
        dose = T("dose written in frequency", 26, TEXT).move_to([-1.5, -3.15, 0])
        self.play(FadeIn(dose, shift=UP * 0.1), run_time=0.5)
        self.at("radio")
        fm = chip("like FM radio", GREY, size=24).next_to(dose, RIGHT, buff=0.4)
        self.play(FadeIn(fm, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Count(SpokenScene):
    CX, CY, R = -2.6, -0.35, 1.95

    def construct(self):
        # the spike train that needs counting
        base = 2.85
        tr = line_from(spike_pts(-5.5, base, 6.0, 0.5, [0.8, 2.2, 3.6, 5.0], 6.0, tau=0.2), YELLOW, 4)
        leg = VGroup(legend_item("dot", "calcium", YELLOW), legend_item("dot", "calmodulin", PURPLE),
                     legend_item("p", "phosphate", GOLD), legend_item("dot", "active subunit", GREEN)
                     ).arrange(RIGHT, buff=0.5).move_to([0, -3.25, 0])
        sch = T("schematic", 22, GREY).move_to([5.4, 3.25, 0])
        self.add(sch)
        self.at("count the spikes")
        self.play(Create(tr), run_time=1.5, rate_func=linear)
        cap = T("something has to\ncount the spikes", 26, TEXT).move_to([3.0, 1.2, 0])
        self.play(FadeIn(cap), run_time=0.4)

        # gauge
        gb = Rectangle(width=0.6, height=3.0, stroke_color=GREY, stroke_width=3).move_to([5.6, -0.1, 0])
        gl = T("calcium", 22, YELLOW).move_to([5.6, -2.0, 0])
        gfill = Rectangle(width=0.6, height=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        gfill.move_to(gb.get_bottom() + UP * 0.15)

        # subunits around a hub
        angs = [np.pi / 2 - k * np.pi / 6 for k in range(12)]
        pos = [np.array([self.CX + self.R * np.cos(a), self.CY + self.R * np.sin(a), 0]) for a in angs]
        subs = VGroup(*[Circle(radius=0.34, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2
                               ).move_to(p) for p in pos])
        hub = Circle(radius=0.55, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35
                     ).move_to([self.CX, self.CY, 0])
        spokes = VGroup(*[Line(hub.get_center(), p, color=GREY, stroke_width=3) for p in pos]).set_z_index(-1)
        self.at("subunits are assembled")
        cap2 = T("twelve subunits\nround a hub", 26, TEXT).move_to([3.0, 1.2, 0])
        self.play(ReplacementTransform(cap, cap2), FadeIn(subs, lag_ratio=0.1), run_time=1.3)
        self.at("central hub")
        self.play(FadeIn(hub, scale=0.5), FadeIn(spokes), FadeIn(leg), run_time=0.6)

        # two neighbours hold calmodulin
        caps = []
        for i in (0, 1):
            d = (pos[i] - hub.get_center()) / self.R
            caps.append(Circle(radius=0.17, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                               fill_opacity=0.9).move_to(pos[i] + d * 0.58))
        cap3 = T("two neighbours hold\ncalmodulin at once", 26, TEXT).move_to([3.0, 1.2, 0])
        self.at("hold calmodulin")
        self.play(ReplacementTransform(cap2, cap3), FadeIn(gb), FadeIn(gl), FadeIn(gfill), run_time=0.5)
        gfull = Rectangle(width=0.6, height=2.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        gfull.move_to(gb.get_bottom() + UP * 1.2)
        self.play(*[FadeIn(c, scale=0.5) for c in caps], Transform(gfill, gfull), run_time=0.7)

        # phosphate passes
        cap4 = T("one phosphorylates\nthe other", 26, TEXT).move_to([3.0, 1.2, 0])
        self.at("phosphorylates the other")
        pb = pbadge(0.2).move_to(pos[0])
        self.play(ReplacementTransform(cap3, cap4), FadeIn(pb, scale=0.5), run_time=0.4)
        self.play(pb.animate.move_to(pos[1] + (pos[1] - hub.get_center()) / self.R * 0.0), run_time=0.7)
        self.play(subs[1].animate.set_stroke(GREEN).set_fill(GREEN, 0.6), run_time=0.4)

        # calcium falls
        cap5 = T("still active after\ncalcium falls", 26, GREEN).move_to([3.0, 1.2, 0])
        gempty = Rectangle(width=0.6, height=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        gempty.move_to(gb.get_bottom() + UP * 0.15)
        self.at("stays active")
        self.play(ReplacementTransform(cap4, cap5), run_time=0.4)
        self.at("calcium falls")
        self.play(Transform(gfill, gempty), *[FadeOut(c) for c in caps], run_time=0.9)
        self.play(Indicate(VGroup(subs[1], pb), color=GREEN, scale_factor=1.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Frequency(SpokenScene):
    X0, W, TMAX = -3.9, 10.0, 12.0
    TAU_A, GAIN = 1.6, 0.5

    def activity_pts(self, base, times):
        ts = np.linspace(0, self.TMAX, int(self.TMAX / 0.02) + 1)
        a, last, pts = 0.0, 0.0, []
        evs = sorted(times)
        k = 0
        for t in ts:
            a *= np.exp(-0.02 / self.TAU_A) if t > 0 else 1
            while k < len(evs) and t >= evs[k]:
                a += self.GAIN * (1 - a)
                k += 1
            pts.append([self.X0 + self.W * t / self.TMAX, base + 1.1 * a / 0.9, 0])
        return pts

    def panel(self, yc, times, label):
        sb, ab = yc + 0.3, yc - 1.0
        s_ax = Line([self.X0, sb, 0], [self.X0 + self.W, sb, 0], color=GREY, stroke_width=2)
        a_ax = Line([self.X0, ab, 0], [self.X0 + self.W, ab, 0], color=GREY, stroke_width=2)
        lab = T(label, 24, TEXT).move_to([self.X0, yc + 1.2, 0], aligned_edge=LEFT)
        l1 = T("calcium", 22, YELLOW).move_to([-5.2, sb + 0.3, 0])
        l2 = T("active\nCaMKII", 22, GREEN).move_to([-5.2, ab + 0.55, 0])
        sp = line_from(spike_pts(self.X0, sb, self.W, 0.65, times, self.TMAX, tau=0.15), YELLOW, 4)
        ac = line_from(self.activity_pts(ab, times), GREEN, 5)
        return VGroup(s_ax, a_ax, lab, l1, l2), sp, ac

    def construct(self):
        close = [0.8, 1.8, 2.8, 3.8, 4.8, 5.8]
        far = [0.8, 6.0, 11.0]
        ideal = T("idealised, same time scale", 22, GREY).move_to([4.5, -3.2, 0])
        fr1, sp1, ac1 = self.panel(1.3, close, "spikes close together")
        fr2, sp2, ac2 = self.panel(-1.75, far, "spikes far apart")
        self.at("close together")
        self.play(FadeIn(fr1), FadeIn(ideal), run_time=0.3)
        self.play(Create(sp1), run_time=0.9, rate_func=linear)
        self.at("build on each other")
        self.play(Create(ac1), run_time=2.2, rate_func=linear)
        self.at("far apart")
        self.play(FadeIn(fr2), run_time=0.4)
        self.play(Create(sp2), run_time=0.8, rate_func=linear)
        self.at("start from nothing")
        self.play(Create(ac2), run_time=2.0, rate_func=linear)
        att = chip("De Koninck and Schulman, 1998 · purified enzyme", GOLD, size=24).move_to([0, 3.35, 0])
        self.at("In 1998")
        self.play(FadeIn(att, shift=DOWN * 0.1), run_time=0.5)
        fq = T("lasting activity depends on pulse frequency", 26, TEXT).move_to([-1.2, -3.2, 0])
        self.at("frequency of calcium pulses")
        self.play(FadeIn(fq, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "Place and timing carry the message."
