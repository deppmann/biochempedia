"""Attention and decisions: a correlate is not a requirement  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the coherent dots / motion evidence in the display
  BLUE   = area MT (evidence)
  PINK   = area LIP and its firing (the ramp)
  GOLD   = the level / bound / threshold line, and the "in this sketch" tags
  GREEN  = the monkey's choice and eye movement; an intact result
  PURPLE = the experimenter's manipulation (weak current, muscimol, a silenced area)
  RED    = an impaired result
  GREY   = structure, random dots, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#E58AC0"

# plot frame shared by scenes 3 and 4 (time 0 to 2000 ms, rate 20 to 80 spikes/s)
PX0, PW, PY0, PH = -5.2, 10.8, -2.3, 3.6


def px(t):
    return PX0 + t / 2000.0 * PW


def py(r):
    return PY0 + (r - 20) / 60.0 * PH


def tag(text, color=GOLD, size=22):
    return T(text, size, color)


def poly(pts, color, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([x, y, 0.0]) for x, y in pts])
    m.set_stroke(color, w).set_fill(opacity=0)
    return m


def dotfield(cx, cy, w, h, coh, n=52, seed=0, speed=0.8, r=0.055):
    rng = np.random.RandomState(seed)
    box = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, cy, 0])
    nc = int(round(coh * n))
    dots, vel = VGroup(), []
    for i in range(n):
        p = [cx + rng.uniform(-w / 2 + .12, w / 2 - .12), cy + rng.uniform(-h / 2 + .12, h / 2 - .12), 0]
        if i < nc:
            v = np.array([speed, 0.0, 0.0]); col = YELLOW
        else:
            a = rng.uniform(0, 2 * np.pi); v = speed * np.array([np.cos(a), np.sin(a), 0.0]); col = GREY
        dots.add(Dot(p, radius=r, color=col)); vel.append(v)

    def upd(m, dt):
        c = box.get_center()
        for d, v in zip(m, vel):
            d.shift(v * dt)
            p = d.get_center()
            if p[0] > c[0] + w / 2 - .1: d.shift(LEFT * (w - .2))
            if p[0] < c[0] - w / 2 + .1: d.shift(RIGHT * (w - .2))
            if p[1] > c[1] + h / 2 - .1: d.shift(DOWN * (h - .2))
            if p[1] < c[1] - h / 2 + .1: d.shift(UP * (h - .2))
    dots.add_updater(upd)
    g = VGroup(box, dots)
    g.dots = dots
    return g


def neuron(c, color, s=1.0):
    c = np.array([c[0], c[1], 0.0])
    soma = Circle(radius=0.26 * s, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.35).move_to(c)
    parts = VGroup(soma)
    for a in (110, 160, 210, 250):
        d = np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
        parts.add(Line(c + d * 0.26 * s, c + d * 0.78 * s, color=color, stroke_width=3.5))
    parts.add(Line(c + RIGHT * 0.26 * s, c + RIGHT * 1.0 * s, color=color, stroke_width=3.5))
    parts.add(Dot(c + RIGHT * 1.05 * s, radius=0.07 * s, color=color))
    return parts


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def axes_lines(x0=1.0, x1=6.0, y0=-2.2, y1=1.0):
    return VGroup(Line([x0, y0, 0], [x1, y0, 0], color=GREY, stroke_width=3.5),
                  Line([x0, y0, 0], [x0, y1, 0], color=GREY, stroke_width=3.5))


def ramp_pts(slope, base=30, bound=70, lat=200):
    return [(px(0), py(base)), (px(lat), py(base)), (px(lat + (bound - base) / slope * 1000.0), py(bound))]


SLOPES = {"strong": 400.0, "mid": 100.0, "weak": 25.0}
RT = {"strong": 370, "mid": 670, "weak": 1870}


def plot_frame():
    return axes_lines(PX0, PX0 + PW, PY0, PY0 + PH)


class S00Title(TitleCard):
    LESSON = "Attention, executive control and decisions"
    TITLE = "A correlate is not a requirement"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        field = dotfield(0.0, 0.65, 5.4, 3.6, 0.35, n=56, seed=3)
        self.play(FadeIn(field), run_time=0.8)
        self.at("moving together")
        l1 = tag("some move together", YELLOW, 26).move_to([0.0, -1.7, 0])
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at("at random")
        l2 = tag("the rest move at random", GREY, 26).move_to([0.0, -2.15, 0])
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.5)

        n = neuron([1.9, 2.45], PINK, 1.0)
        nl = T("parietal neuron", 26, PINK).move_to([4.6, 2.45, 0])
        self.at("parietal cortex")
        self.play(field.animate.shift(LEFT * 3.5), l1.animate.shift(LEFT * 3.5), l2.animate.shift(LEFT * 3.5),
                  FadeIn(n), FadeIn(nl), run_time=0.9)

        ax = axes_lines(1.0, 6.0, -2.2, 1.0)
        yl = T("firing", 24, GREY).move_to([0.1, 0.1, 0])
        base, lev = -1.5, 0.5
        t0, t1 = 2.1, 4.3
        ramp = poly([(1.0, base), (t0, base), (t1, lev)], PINK, 6)
        xl = tag("time, in this sketch", GOLD, 22).move_to([3.5, -2.6, 0])
        self.at("faster and faster")
        self.play(FadeIn(ax), FadeIn(yl), FadeIn(xl), run_time=0.4)
        self.play(Create(ramp, rate_func=linear), run_time=2.0)
        self.at("certain level")
        levl = DashedLine([1.0, lev, 0], [6.0, lev, 0], color=GOLD, stroke_width=4)
        levt = T("certain level", 24, GOLD).move_to([5.0, lev + 0.38, 0])
        self.play(Create(levl), FadeIn(levt), run_time=0.6)

        chip_eye = chip("eyes move to answer", GREEN, 28).move_to([-3.5, -2.95, 0])
        self.at("moves its eyes")
        self.play(FadeIn(chip_eye, shift=UP * 0.15), run_time=0.6)
        self.at("Is that neuron")
        q = T("?", 44, GOLD, weight=BOLD)
        q.next_to(n, LEFT, buff=0.35)
        self.play(FadeIn(q, scale=1.4), Indicate(n, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.at("Silence the area")
        sil = T("silenced", 26, PURPLE).move_to([4.6, 2.45, 0])
        self.play(FadeOut(ramp), FadeOut(levl), FadeOut(levt), FadeOut(q), run_time=0.5)
        self.play(n.animate.set_color(PURPLE), ReplacementTransform(nl, sil), run_time=0.6)
        self.at("decides just as well")
        chip2 = chip("decides just as well", GREEN, 28).move_to([-3.5, -2.95, 0])
        qq = T("?", 110, GOLD, weight=BOLD).move_to([3.5, -0.5, 0])
        self.play(ReplacementTransform(chip_eye, chip2), FadeIn(qq, scale=1.3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Evidence(SpokenScene):
    def construct(self):
        # --- coherence ---
        xs = [-4.2, 0.0, 4.2]
        cohs = [0.032, 0.128, 0.512]
        fields = [dotfield(x, 0.6, 3.5, 2.8, c, n=60, seed=5 + i) for i, (x, c) in enumerate(zip(xs, cohs))]
        self.play(*[FadeIn(f) for f in fields], run_time=0.8)
        self.at("percentage of dots")
        pl = [M(s, 32, YELLOW).move_to([x, -1.2, 0]) for x, s in zip(xs, ["3.2%", "12.8%", "51.2%"])]
        self.play(*[FadeIn(p, shift=UP * 0.1) for p in pl], run_time=0.6)
        self.at("move together")
        cap = T("coherence: the share of dots moving together", 30, TEXT).move_to([0, -2.3, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)

        # --- tuning ---
        self.at("Neurons in area")
        self.play(*[FadeOut(f) for f in fields], *[FadeOut(p) for p in pl], FadeOut(cap), run_time=0.6)
        n = neuron([-5.0, 2.6], BLUE, 1.0)
        nl = T("MT neuron", 28, BLUE).move_to([-2.55, 2.6, 0])
        self.play(FadeIn(n), FadeIn(nl), run_time=0.5)
        ax = axes_lines(-4.6, 4.6, -1.8, 1.9)
        xl = T("direction of motion", 26, GREY).move_to([0, -2.35, 0])
        yl = T("response", 24, GREY).move_to([-5.3, 0.4, 0])
        xs_ = np.linspace(-4.5, 4.5, 80)
        curve = poly([(x, -1.8 + 3.3 * np.exp(-(x / 1.5) ** 2 / 2)) for x in xs_], BLUE, 6)
        sk = tag("relative, in this sketch", GOLD, 22).move_to([3.3, 2.6, 0])
        self.at("tuned to the direction")
        self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(sk), run_time=0.5)
        self.play(Create(curve, rate_func=linear), run_time=1.6)
        pk = DashedLine([0, -1.8, 0], [0, 1.5, 0], color=YELLOW, stroke_width=3)
        pt = T("preferred direction", 26, YELLOW).move_to([0, 2.1, 0])
        self.play(Create(pk), FadeIn(pt), run_time=0.6)

        # --- neurons vs monkey ---
        self.at("In monkeys")
        self.play(*[FadeOut(m) for m in (n, nl, ax, xl, yl, sk, curve, pk, pt)], run_time=0.5)
        c1 = chip("each neuron tested on a matched task", BLUE, 34).move_to([0, 2.4, 0])
        t1 = T("most discriminated motion about as well as", 32, TEXT).move_to([0, 0.85, 0])
        c2 = chip("the monkey", GREEN, 36).move_to([0, -0.6, 0])
        t2 = T("or better", 32, TEXT).move_to([0, -1.7, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.5)
        self.at("Most of the")
        self.play(FadeIn(t1), run_time=0.5)
        self.at("as the monkey")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at("or better")
        self.play(FadeIn(t2), run_time=0.5)

        # --- microstimulation ---
        self.at("Weak current")
        self.play(*[FadeOut(m) for m in (c1, t1, c2, t2)], run_time=0.5)
        cl = VGroup(*[Circle(radius=0.42, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.35)
                      .move_to([-4.0 + dx, 0.9 + dy, 0]) for dx, dy in
                      [(-0.8, 0.4), (0.0, 0.9), (0.8, 0.35), (-0.35, -0.35), (0.5, -0.6), (-1.05, -0.65)]])
        elec = Line([-4.0, 3.2, 0], [-4.0, 2.0, 0], color=GREY, stroke_width=5)
        cur = T("weak current", 30, PURPLE).move_to([-2.2, 3.0, 0])
        self.play(Create(elec), FadeIn(cur), run_time=0.6)
        self.at("small cluster")
        cll = T("small cluster of MT neurons", 26, BLUE).move_to([-3.6, -1.0, 0])
        self.play(FadeIn(cl, lag_ratio=0.15), FadeIn(cll), run_time=0.8)
        self.at("one preferred direction")
        pa = arrow([-5.2, -1.75, 0], [-2.8, -1.75, 0], YELLOW)
        pal = T("one preferred direction", 26, YELLOW).move_to([-4.0, -2.35, 0])
        self.play(GrowArrow(pa), FadeIn(pal), run_time=0.7)
        base = -1.6
        b0 = Rectangle(width=1.3, height=1.5, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([2.2, base + 0.75, 0])
        b1 = Rectangle(width=1.3, height=3.0, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to([4.1, base + 1.5, 0])
        bl = Line([1.3, base, 0], [5.0, base, 0], color=GREY, stroke_width=3)
        bt = T("choices toward that direction", 26, GREEN).move_to([3.2, 3.0, 0])
        bn0 = T("no current", 24, GREY).move_to([2.2, base - 0.4, 0])
        bn1 = T("current", 24, PURPLE).move_to([4.1, base - 0.4, 0])
        sk2 = tag("relative heights, in this sketch", GOLD, 22).move_to([3.2, base - 1.0, 0])
        self.at("biased")
        self.play(FadeIn(bl), FadeIn(bt), FadeIn(bn0), FadeIn(bn1), FadeIn(sk2),
                  GrowFromEdge(b0, DOWN), run_time=0.7)
        self.play(GrowFromEdge(b1, DOWN), run_time=0.8)

        # --- MT supplies evidence ---
        self.at("supplies evidence")
        self.play(*[FadeOut(m) for m in (cl, elec, cur, cll, pa, pal, b0, b1, bl, bt, bn0, bn1, sk2)], run_time=0.5)
        mt = chip("MT", BLUE, 48).move_to([-3.6, 0.3, 0])
        ch = chip("choice", GREEN, 48).move_to([3.6, 0.3, 0])
        ar = arrow([-2.2, 0.3, 0], [2.0, 0.3, 0], YELLOW, 7)
        al = T("evidence", 32, YELLOW).move_to([-0.1, 0.95, 0])
        self.play(FadeIn(mt), FadeIn(ch), run_time=0.5)
        self.play(GrowArrow(ar), FadeIn(al), run_time=0.7)
        self.at("sway the choice")
        self.play(Indicate(ch, color=GREEN, scale_factor=1.18), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def row_swap(scene, old, new, rt=0.5):
    scene.play(FadeOut(old), FadeIn(new, shift=UP * 0.1), run_time=rt)
    return new


class S03Ramp(SpokenScene):
    def construct(self):
        frame = plot_frame()
        big = neuron([-4.0, 0.9], PINK, 1.7)
        bigl = T("LIP neuron", 34, PINK).move_to([-4.0, -0.7, 0])
        xl = tag("time, in this sketch", GOLD, 22).move_to([3.7, -2.75, 0])
        self.at("lateral intraparietal")
        self.play(FadeIn(big), FadeIn(bigl), run_time=0.8)
        # spikes, then an eye movement into the response field
        fix = Dot([0.9, -0.2, 0], radius=0.1, color=GREY)
        tgt = Dot([4.7, -0.2, 0], radius=0.1, color=GREY)
        rf = DashedVMobject(Circle(radius=1.25, color=PINK, stroke_width=4).move_to([4.7, -0.2, 0]), num_dashes=24)
        rfl = T("response field", 26, PINK).move_to([4.7, -1.85, 0])
        sp = VGroup(*[Line([x, 1.9, 0], [x, 2.5, 0], color=PINK, stroke_width=4) for x in (0.7, 1.4, 1.9, 2.3, 2.65, 2.95, 3.2, 3.42)])
        spl = T("spikes", 26, PINK).move_to([-0.3, 2.2, 0])
        self.at("fire before")
        self.play(FadeIn(fix), FadeIn(tgt), FadeIn(spl), LaggedStart(*[Create(x) for x in sp], lag_ratio=0.2), run_time=1.0)
        self.at("eye movements")
        ar = arrow([1.1, -0.2, 0], [4.45, -0.2, 0], GREEN, 7)
        arl = T("eye movement", 26, GREEN).move_to([2.2, 0.4, 0])
        self.play(GrowArrow(ar), FadeIn(arl), run_time=0.5)
        self.at("response field")
        self.play(Create(rf), FadeIn(rfl), run_time=0.7)
        tg = tag("rhesus monkeys answer whenever they are ready", GOLD, 24).move_to([0.6, -3.0, 0])
        self.at("rhesus monkeys")
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.6)
        n = neuron([-5.6, 2.7], PINK, 0.9)
        nl = T("LIP neuron", 26, PINK).move_to([-3.4, 2.7, 0])
        row = T("one line for each motion strength", 24, TEXT).move_to([2.0, 2.7, 0])
        self.at("Stronger motion")
        self.play(*[FadeOut(m) for m in (fix, tgt, rf, rfl, sp, spl, ar, arl, tg)], ReplacementTransform(big, n),
                  ReplacementTransform(bigl, nl), FadeIn(frame), FadeIn(xl), FadeIn(row), run_time=0.8)
        ramps = {k: poly(ramp_pts(s), PINK, 6) for k, s in SLOPES.items()}
        ends = {k: ramp_pts(s)[-1] for k, s in SLOPES.items()}
        names = {"strong": "strong", "mid": "medium", "weak": "weak"}
        lbl = {k: T(names[k], 22, PINK).move_to([ends[k][0], ends[k][1] + 0.42, 0]) for k in SLOPES}
        for k in ("weak", "mid", "strong"):
            self.play(Create(ramps[k], rate_func=linear), FadeIn(lbl[k]), run_time=0.7)
        self.at("more steeply")
        self.play(Indicate(ramps["strong"], color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.at("similar level")
        lev = DashedLine([PX0, py(70), 0], [PX0 + PW, py(70), 0], color=GOLD, stroke_width=4)
        self.play(Create(lev), run_time=0.7)
        self.at("before the eye movement")
        mk = VGroup(*[DashedLine([px(RT[k]), PY0, 0], [px(RT[k]), py(70), 0], color=GREEN, stroke_width=4) for k in SLOPES])
        self.play(LaggedStart(*[Create(m) for m in mk], lag_ratio=0.3), run_time=1.0)
        self.at("read as a threshold")
        row = row_swap(self, row, T("the authors read this level as a threshold", 24, GOLD).move_to([2.0, 2.7, 0]))
        self.at("averages across trials")
        row = row_swap(self, row, T("each ramp is an average across trials", 24, TEXT).move_to([2.0, 2.7, 0]))
        self.at("ramp or step")
        ic1 = poly([(0, 0), (0.4, 0), (1.2, 0.55)], PINK, 5)
        ic2 = poly([(0, 0), (0.6, 0), (0.6, 0.55), (1.2, 0.55)], PINK, 5)
        g = VGroup(T("single trials:", 24, TEXT), ic1, T("or", 24, GREY), ic2, T("debated", 24, GOLD)).arrange(RIGHT, buff=0.3)
        g.move_to([2.0, 2.7, 0])
        row = row_swap(self, row, g)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Model(SpokenScene):
    def construct(self):
        frame = plot_frame()
        ramps = {k: poly(ramp_pts(s), PINK, 6) for k, s in SLOPES.items()}
        lev = DashedLine([PX0, py(70), 0], [PX0 + PW, py(70), 0], color=GOLD, stroke_width=4)
        xl = T("time (ms)", 24, GREY).move_to([4.6, -3.2, 0])
        self.play(FadeIn(frame), *[FadeIn(r) for r in ramps.values()], FadeIn(lev), run_time=0.7)
        ticks = VGroup()
        for t in (0, 500, 1000, 1500, 2000):
            ticks.add(Line([px(t), PY0, 0], [px(t), PY0 - 0.12, 0], color=GREY, stroke_width=3))
            ticks.add(M(str(t), 22, GREY).move_to([px(t), PY0 - 0.42, 0]))
        self.at("adds up evidence")
        form = M("rise time = (bound − baseline) / slope", 28, TEXT).move_to([0, 3.3, 0])
        self.play(FadeIn(form, shift=DOWN * 0.1), FadeIn(ticks), FadeIn(xl), run_time=0.7)
        self.at("hits a bound")
        bl = T("bound", 24, GOLD).move_to([PX0 + 0.55, py(70) - 0.32, 0])
        self.play(FadeIn(bl), Indicate(lev, color=GOLD, scale_factor=1.0), run_time=0.6)
        self.at("with no noise")
        note = T("invented numbers, no noise · rates in spikes/s, slope in (spikes/s)/s", 22, GOLD).move_to([0, 2.75, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("starts at")
        b0 = DashedLine([PX0, py(30), 0], [PX0 + PW, py(30), 0], color=GREY, stroke_width=2.5)
        v30 = M("30", 24, GREY).move_to([PX0 - 0.35, py(30), 0])
        v70 = M("70", 24, GOLD).move_to([PX0 - 0.35, py(70), 0])
        bll = T("baseline", 22, GREY).move_to([PX0 + 0.65, py(30) - 0.33, 0])
        self.play(Create(b0), FadeIn(v30), FadeIn(bll), run_time=0.6)
        self.at("climbs to")
        self.play(FadeIn(v70, scale=1.3), run_time=0.5)
        self.at("latency")
        br = VGroup(Line([px(0), -3.25, 0], [px(200), -3.25, 0], color=YELLOW, stroke_width=4),
                    Line([px(0), -3.15, 0], [px(0), -3.35, 0], color=YELLOW, stroke_width=4),
                    Line([px(200), -3.15, 0], [px(200), -3.35, 0], color=YELLOW, stroke_width=4))
        brl = T("latency 200 ms", 22, YELLOW).move_to([px(200) + 1.45, -3.25, 0])
        self.play(Create(br), FadeIn(brl), run_time=0.7)

        marks, rts, pcts, slps = {}, {}, {}, {}
        for k, pc, sl in (("strong", "51.2%", "400"), ("mid", "12.8%", "100"), ("weak", "3.2%", "25")):
            ex, ey = ramp_pts(SLOPES[k])[-1]
            pcts[k] = M(pc, 22, PINK).move_to([ex, ey + 0.4, 0])
            slps[k] = T("slope " + sl, 22, PINK).move_to([ex, ey + 0.82, 0])
            marks[k] = DashedLine([px(RT[k]), PY0, 0], [px(RT[k]), py(70), 0], color=GREEN, stroke_width=4)
        self.at("eye moves")
        m70 = T("+70 ms", 22, GREEN).move_to([px(RT["strong"]) + 0.55, -1.98, 0])
        self.play(Create(marks["strong"]), FadeIn(m70), run_time=0.7)
        self.at("the slope is")
        self.play(FadeIn(pcts["strong"]), FadeIn(slps["strong"]), run_time=0.6)
        self.at("reaction time is")
        rt = {k: M(f"{RT[k]:,} ms", 22, GREEN) for k in RT}
        rt["strong"].move_to([px(RT["strong"]) + 0.6, -1.98, 0])
        self.play(ReplacementTransform(m70, rt["strong"]), run_time=0.6)
        self.at("it is", nth=0)
        self.play(FadeIn(pcts["mid"]), FadeIn(slps["mid"]), run_time=0.5)
        rt["mid"].move_to([px(RT["mid"]) + 0.7, -1.98, 0])
        self.play(Create(marks["mid"]), FadeIn(rt["mid"]), run_time=0.7)
        self.at("it is", nth=1)
        self.play(FadeIn(pcts["weak"]), FadeIn(slps["weak"]), run_time=0.5)
        rt["weak"].move_to([px(RT["weak"]) - 0.95, -1.98, 0])
        self.play(Create(marks["weak"]), FadeIn(rt["weak"]), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def meter(x, y, w=3.8):
    back = Rectangle(width=w, height=0.5, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([x, y, 0])
    fill = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to([x, y, 0])
    return back, fill


class S05Silence(SpokenScene):
    def construct(self):
        h1 = T("correlation", 36, GREY, weight=BOLD).move_to([-3.4, 2.7, 0])
        d1 = T("activity that goes with a choice", 26, GREY).move_to([-3.4, 2.15, 0])
        pa = axes_lines(-5.6, -1.2, -1.7, 1.4)
        ra = poly([(-5.6, -1.2), (-4.7, -1.2), (-2.2, 1.0)], PINK, 6)
        mk = DashedLine([-1.9, -1.7, 0], [-1.9, 1.0, 0], color=GREEN, stroke_width=4)
        mkl = T("choice", 26, GREEN).move_to([-1.9, -2.15, 0])
        self.at("Correlation shows")
        self.play(FadeIn(h1), FadeIn(d1), FadeIn(pa), run_time=0.6)
        self.play(Create(ra, rate_func=linear), run_time=1.4)
        self.play(Create(mk), FadeIn(mkl), run_time=0.6)
        h2 = T("manipulation", 36, PURPLE, weight=BOLD).move_to([3.4, 2.7, 0])
        d2 = T("change the area, test the choice", 26, PURPLE).move_to([3.4, 2.15, 0])
        ca = chip("area", GREY, 40).move_to([3.4, 0.7, 0])
        cc = chip("choice", GREEN, 40).move_to([3.4, -1.3, 0])
        ar = arrow([3.4, 0.1, 0], [3.4, -0.7, 0], GREY, 6)
        self.at("only a manipulation")
        self.play(FadeIn(h2), FadeIn(d2), FadeIn(ca), run_time=0.6)
        self.play(GrowArrow(ar), FadeIn(cc), run_time=0.6)
        self.at("needs it")
        qm = T("?", 60, GOLD, weight=BOLD).move_to([4.9, -0.3, 0])
        self.play(ca.animate.set_color(PURPLE), FadeIn(qm, scale=1.3), run_time=0.7)
        self.at("silenced each area")
        self.play(*[FadeOut(m) for m in (h1, d1, pa, ra, mk, mkl, h2, d2, ca, cc, ar, qm)], run_time=0.6)

        mt = chip("MT", BLUE, 44).move_to([-3.4, 1.4, 0])
        lip = chip("LIP", PINK, 44).move_to([3.4, 1.4, 0])
        mb, mf = meter(-3.4, -0.9)
        lb, lf = meter(3.4, -0.9)
        c1 = T("motion discrimination", 24, TEXT).move_to([-3.4, -0.3, 0])
        c2 = T("motion discrimination", 24, TEXT).move_to([3.4, -0.3, 0])
        self.at("each area")
        self.play(FadeIn(mt), FadeIn(lip), FadeIn(mb), FadeIn(mf), FadeIn(lb), FadeIn(lf), FadeIn(c1), FadeIn(c2), run_time=0.8)
        self.at("rhesus monkeys")
        rh = VGroup(tag("rhesus monkeys", GOLD, 24), tag("bars: relative, in this sketch", GOLD, 22)).arrange(RIGHT, buff=0.8).move_to([0, -3.2, 0])
        self.play(FadeIn(rh), run_time=0.4)
        drug = chip("muscimol", PURPLE, 28).move_to([0, 1.4, 0])
        dl = T("activates GABA-A receptors", 24, PURPLE).move_to([0, 0.65, 0])
        self.at("muscimol")
        self.play(FadeIn(drug, scale=0.9), FadeIn(dl), run_time=0.7)
        self.at("Silencing", nth=0)
        dar = arrow([-0.9, 1.4, 0], [-2.2, 1.4, 0], PURPLE, 6)
        self.play(GrowArrow(dar), mt.animate.set_color(PURPLE), run_time=0.5)
        sm = T("silenced", 24, PURPLE).move_to([-3.4, 2.3, 0])
        self.play(FadeIn(sm), run_time=0.3)
        self.at("impaired motion")
        mf2 = Rectangle(width=1.5, height=0.5, stroke_width=0, fill_color=RED, fill_opacity=0.9)
        mf2.move_to(mb.get_left() + RIGHT * 0.75)
        rl = T("impaired", 28, RED, weight=BOLD).move_to([-3.4, -1.75, 0])
        self.play(Transform(mf, mf2), FadeIn(rl), run_time=0.8)
        self.at("Silencing", nth=1)
        dar2 = arrow([0.9, 1.4, 0], [2.2, 1.4, 0], PURPLE, 6)
        self.play(FadeOut(dar), FadeOut(sm), mt.animate.set_color(BLUE), GrowArrow(dar2), lip.animate.set_color(PURPLE), run_time=0.6)
        sl = T("silenced", 24, PURPLE).move_to([3.4, 2.3, 0])
        self.play(FadeIn(sl), run_time=0.3)
        self.at("no measurable impairment")
        gl = VGroup(T("no measurable impairment", 26, GREEN), T("in the tasks tested", 26, GREEN)).arrange(DOWN, buff=0.12).move_to([3.4, -1.9, 0])
        self.play(Indicate(lf, color=GREEN, scale_factor=1.04), FadeIn(gl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Control(SpokenScene):
    def construct(self):
        lc = chip("LIP", PURPLE, 44).move_to([3.4, 1.4, 0])
        lcl = T("silenced", 24, PURPLE).move_to([3.4, 2.3, 0])
        lb, lf = meter(3.4, -0.9)
        lcap = T("motion discrimination", 24, TEXT).move_to([3.4, -0.3, 0])
        lres = VGroup(T("no measurable impairment", 26, GREEN), T("in the tasks tested", 26, GREEN)).arrange(DOWN, buff=0.12).move_to([3.4, -1.9, 0])
        self.play(FadeIn(lc), FadeIn(lcl), FadeIn(lb), FadeIn(lf), FadeIn(lcap), FadeIn(lres), run_time=0.3)
        self.at("missed injection")
        miss = VGroup(T("did the injection miss?", 40, GOLD), T("could explain a null result", 28, GREY)).arrange(DOWN, buff=0.25).move_to([-3.2, 0.5, 0])
        self.play(FadeIn(miss, shift=RIGHT * 0.2), run_time=0.8)
        self.at("choice task")
        self.play(*[FadeOut(m) for m in (lc, lcl, lb, lf, lcap, lres, miss)], run_time=0.5)
        fcx, fcy = -2.4, 0.5
        box = Rectangle(width=7.0, height=3.6, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([fcx, fcy, 0])
        aff = Rectangle(width=3.5, height=3.6, stroke_width=0, fill_color=PURPLE, fill_opacity=0.2).move_to([fcx + 1.75, fcy, 0])
        pos = [(-4.2, 1.5), (-4.2, -0.5), (-0.6, 1.5), (-0.6, -0.5)]
        tg = VGroup(*[Circle(radius=0.25, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to([x, y, 0]) for x, y in pos])
        tt = T("free choice: targets, no right answer", 26, TEXT).move_to([fcx, 2.8, 0])
        self.play(Create(box), FadeIn(tg), FadeIn(tt), run_time=0.9)
        self.at("inactivation")
        al = VGroup(T("part of space the silenced LIP covers", 22, PURPLE), T("(side not specified here)", 22, PURPLE)).arrange(DOWN, buff=0.08).move_to([fcx + 0.4, -1.9, 0])
        lip = chip("LIP silenced", PURPLE, 26).move_to([4.2, 2.8, 0])
        self.play(FadeIn(aff), FadeIn(al), FadeIn(lip), run_time=0.7)
        base = -1.3
        b0 = Rectangle(width=1.1, height=2.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to([3.3, base + 1.15, 0])
        b1 = Rectangle(width=1.1, height=1.2, stroke_width=0, fill_color=GREEN, fill_opacity=0.85).move_to([5.0, base + 0.6, 0])
        bl = Line([2.5, base, 0], [5.8, base, 0], color=GREY, stroke_width=3)
        bn0 = T("before", 24, TEXT).move_to([3.3, base - 0.4, 0])
        bn1 = T("after", 24, TEXT).move_to([5.0, base - 0.4, 0])
        bt = VGroup(T("targets chosen in the", 24, GREEN), T("affected part of space", 24, GREEN)).arrange(DOWN, buff=0.08).move_to([4.2, 1.6, 0])
        sk = tag("relative, in this sketch", GOLD, 22).move_to([4.2, base - 1.0, 0])
        self.at("chose targets")
        self.play(FadeIn(bl), FadeIn(bt), FadeIn(bn0), FadeIn(bn1), FadeIn(sk), GrowFromEdge(b0, DOWN), run_time=0.7)
        self.at("less often")
        self.play(GrowFromEdge(b1, DOWN), run_time=0.9)

        # saccade landing scatter at one target in the affected part of space
        rng = np.random.RandomState(4)
        tgt = np.array([-0.6, 1.5, 0])
        tight = VGroup(*[Dot(tgt + np.array([rng.normal(0, .1), rng.normal(0, .1), 0]), radius=0.09, color=GREEN) for _ in range(12)])
        wide = VGroup(*[Dot(tgt + np.array([rng.normal(0, .5), rng.normal(0, .5), 0]), radius=0.09, color=GREEN) for _ in range(12)])
        for d in wide:  # keep inside the field
            c = d.get_center(); d.move_to([min(max(c[0], -2.1), 0.95), min(max(c[1], -1.1), 2.1), 0])
        ll = T("eye landing points: before", 24, GREEN).move_to([fcx - 1.2, -2.3, 0])
        self.at("eye movements")
        self.play(FadeOut(al), FadeIn(ll), FadeIn(tight), run_time=0.6)
        self.at("landed less accurately")
        ll2 = T("eye landing points: after", 24, GREEN).move_to(ll)
        self.play(Transform(tight, wide), ReplacementTransform(ll, ll2), run_time=1.0)

        self.at("The drug had acted")
        self.play(*[FadeOut(m) for m in (box, aff, tg, tt, ll2, tight, lip, b0, b1, bl, bn0, bn1, bt, sk)], run_time=0.6)
        ca = chip("the drug had acted", PURPLE, 40)
        ta = T("free-choice behaviour changed", 36, TEXT)
        rowa = VGroup(ca, ta).arrange(RIGHT, buff=0.6)
        fit(rowa, max_w=12.2)
        rowa.move_to([0, 1.5, 0])
        self.play(FadeIn(ca, shift=RIGHT * 0.1), FadeIn(ta), run_time=0.7)
        self.at("not needed")
        cb = chip("LIP not needed", GREY, 40)
        tb = T("for this discrimination, in the tasks tested", 36, TEXT)
        rowb = VGroup(cb, tb).arrange(RIGHT, buff=0.6)
        fit(rowb, max_w=12.2)
        rowb.move_to([0, -0.5, 0])
        self.play(FadeIn(cb, shift=RIGHT * 0.1), FadeIn(tb), run_time=0.7)
        self.at("Keep this rule")
        self.play(FadeOut(rowa), FadeOut(rowb), run_time=0.5)
        g = VGroup(chip("tracks the choice", PINK, 46), T("is not always", 40, TEXT), chip("needed for it", GREY, 46)).arrange(DOWN, buff=0.55)
        g.move_to([0, 0.1, 0])
        self.play(FadeIn(g[0], shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(g[1]), FadeIn(g[2], shift=UP * 0.2), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A neuron that tracks a choice is not always needed for it."
