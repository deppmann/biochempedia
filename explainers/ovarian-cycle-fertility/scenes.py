"""The ovarian cycle and fertility: one follicle wins, then estradiol flips  (Biochemistrypedia explainer, Physiology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = FSH (and the FSH receptor)
  YELLOW = LH (and the LH receptor), the LH surge
  PINK   = estradiol / estrogen
  PURPLE = progesterone
  ORANGE = androgen
  GOLD   = inhibin B
  TEAL   = the dominant follicle
  TEXT   = enzymes (CYP17, aromatase), neutral labels, a single blood sample
  RED    = brake (lowers), atresia, a fall
  GREEN  = accelerator (raises), positive feedback
  GREY   = follicles, cells, glands, axes, outlines, de-emphasized text
All curves are sketches ("in this sketch", relative units), computed from simple equations.
Nothing is a measurement; the only numbers on screen are the lesson's own.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E58BB0"
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def P3(x, y):
    return np.array([x, y, 0.0])


def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color=GREY, fill=0.10, sw=3, pos=(0, 0)):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill).move_to([pos[0], pos[1], 0])


def cap(x, y, color=RED, half=0.4, w=7):
    """Flat bar: the end of a line that lowers (a brake)."""
    return Line(P3(x - half, y), P3(x + half, y), color=color, stroke_width=w)


def head(x, y, color=GREEN, s=0.3):
    """Upward arrowhead: the end of a line that raises."""
    t = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=2).scale(s)
    return t.move_to(P3(x, y - 0.05))


def sketch_axes(x_range, y_range, x_len, y_len, origin):
    ax = Axes(x_range=x_range, y_range=y_range, x_length=x_len, y_length=y_len, tips=False,
              axis_config=dict(stroke_color=GREY, stroke_width=3, include_ticks=False, include_numbers=False))
    ax.shift(P3(*origin) - ax.c2p(x_range[0], y_range[0]))
    return ax


def sig(z):
    return 1.0 / (1.0 + np.exp(-z))


class S00Title(TitleCard):
    LESSON = "The ovarian cycle and fertility"
    TITLE = "One Follicle Wins, Then Estradiol Flips"


# ---------------------------------------------------------------------------------------------
class S01Crowd(SpokenScene):
    """A crowd of follicles, one oocyte released after a surge: how? Two steps."""

    def construct(self):
        cols = [-5.0, -2.5, 0.0, 2.5]
        rows = [1.5, -0.9]
        blocks, dots, boxes = VGroup(), [], []
        for r in rows:
            for c in cols:
                b = box(2.2, 2.0, GREY, 0.10, pos=(c, r))
                d = Circle(radius=0.34, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                           fill_opacity=0.35).move_to(b)
                boxes.append(b)
                dots.append(d)
                blocks.add(VGroup(b, d))
        lab = T("a crowd of small follicles", 28, GREY).move_to([-1.25, -2.3, 0])
        self.at("a crowd of small")
        self.play(LaggedStart(*[FadeIn(g, scale=0.85) for g in blocks], lag_ratio=0.12), FadeIn(lab),
                  run_time=1.6)

        # a follicle = oocyte + the cells around it
        l1 = T("cells around it", 24, GREY).move_to([-5.1, 3.3, 0])
        a1 = arr([-5.3, 3.05, 0], [-5.3, 2.55, 0], GREY, 3, 0.16)
        l2 = T("oocyte", 24, TEXT).move_to([-3.0, 3.3, 0])
        a2 = arr([-3.4, 3.05, 0], [-4.75, 1.85, 0], TEXT, 3, 0.16)
        self.at("oocyte with the cells")
        self.play(Indicate(blocks[0], color=TEXT, scale_factor=1.06), FadeIn(l1), GrowArrow(a1),
                  FadeIn(l2), GrowArrow(a2), run_time=1.0)

        # one oocyte is released
        chosen = 3
        others = [blocks[i] for i in range(8) if i != chosen]
        released = T("one oocyte\nreleased", 24, TEXT, line_spacing=0.8).move_to([5.5, 0.55, 0])
        out = arr([3.75, 1.5, 0], [5.0, 1.5, 0], TEXT, 4, 0.2)
        self.at("one oocyte is released")
        self.play(FadeOut(l1), FadeOut(a1), FadeOut(l2), FadeOut(a2), FadeOut(lab),
                  *[g.animate.set_opacity(0.25) for g in others], run_time=0.6)
        self.play(GrowArrow(out), dots[chosen].animate.move_to([5.5, 1.5, 0]), FadeIn(released), run_time=1.0)

        # at a predictable time after a hormone surge
        c1 = bchip("a hormone surge", YELLOW, 26).move_to([-3.4, -3.05, 0])
        c2 = bchip("oocyte released", TEXT, 26).move_to([3.2, -3.05, 0])
        ar = arr(c1.get_right() + RIGHT * 0.05, c2.get_left() + LEFT * 0.05, GREY, 4)
        pt = T("predictable time", 24, GREY).next_to(ar, UP, buff=0.12)
        self.at("predictable time after")
        self.play(FadeIn(c1), run_time=0.5)
        self.play(GrowArrow(ar), FadeIn(pt), FadeIn(c2), run_time=0.9)

        q = T("?", 130, TEXT, weight=BOLD).move_to([-1.25, 0.3, 0])
        self.at("turn a crowd into one")
        self.play(FadeIn(q, scale=0.6), run_time=0.7)

        # two steps
        step1 = VGroup(box(5.6, 4.6, BLUE, 0.12, 4, pos=(-3.4, 0.1)), T("1", 64, BLUE, weight=BOLD),
                       T("FSH picks\none follicle", 44, BLUE, line_spacing=0.9))
        step1[1].move_to(step1[0].get_corner(UL) + RIGHT * 0.55 + DOWN * 0.6)
        step1[2].move_to(step1[0].get_center() + DOWN * 0.3)
        step2 = VGroup(box(5.6, 4.6, PINK, 0.12, 4, pos=(3.4, 0.1)), T("2", 64, PINK, weight=BOLD),
                       T("estradiol turns\na brake into an\naccelerator", 40, PINK, line_spacing=0.9))
        step2[1].move_to(step2[0].get_corner(UL) + RIGHT * 0.55 + DOWN * 0.6)
        step2[2].move_to(step2[0].get_center() + DOWN * 0.3)
        mid = arr([-0.45, 0.1, 0], [0.45, 0.1, 0], GREY, 6)
        self.at("picks one follicle")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.play(FadeIn(step1, scale=0.92), run_time=0.8)
        self.at("turns a")
        self.play(GrowArrow(mid), FadeIn(step2, scale=0.92), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Select(SpokenScene):
    """FSH rescues a cohort; inhibin B lowers FSH; only the follicle most sensitive to FSH keeps growing."""

    def construct(self):
        ax = sketch_axes([0, 10, 1], [0, 1.1, 0.5], 9.2, 5.0, (-6.1, -2.55))
        f = lambda t: 0.18 + 0.82 * (t / 2.0) * np.exp(1 - t / 2.0)
        thr = [0.86, 0.68, 0.50, 0.36, 0.22]
        yb = [ax.c2p(0, h)[1] for h in thr]
        ylab = T("FSH, relative units, in this sketch", 22, GREY).move_to([-3.6, 3.2, 0])
        xl1 = T("end of previous cycle", 22, GREY).move_to([-4.7, -3.0, 0])
        xl2 = T("time", 22, GREY).move_to([-0.6, -3.0, 0])
        xl3 = T("mid-follicular phase", 22, GREY).move_to([1.7, -3.0, 0])
        rise = ax.plot(f, x_range=[0, 2.0], color=BLUE, stroke_width=6)
        fsh_l = T("FSH", 30, BLUE, weight=BOLD).move_to([-3.2, 2.55, 0])
        self.at("end of the previous")
        self.play(Create(ax), FadeIn(ylab), FadeIn(xl1), FadeIn(xl2), run_time=0.9)
        self.play(Create(rise), FadeIn(fsh_l), run_time=1.2)

        # the cohort and its thresholds
        blocks, lines, dashes = [], [], VGroup()
        for y in yb:
            b = VGroup(box(1.9, 0.5, GREY, 0.14, 2.5, pos=(4.9, y)),
                       T("follicle", 22, TEXT).move_to([4.9, y, 0]))
            blocks.append(b)
            dashes.add(DashedLine(P3(ax.c2p(0, 0)[0], y), P3(3.95, y), color=GREY, stroke_width=2,
                                  dash_length=0.15).set_opacity(0.7))
        cohort = T("cohort of small\nantral follicles", 22, GREY, line_spacing=0.8).move_to([4.9, 2.2, 0])
        thr_l = T("dashed lines: each follicle's\nFSH threshold (in this sketch)", 22, GREY,
                  line_spacing=0.8).move_to([0.2, -2.05, 0])
        self.at("rescues a cohort")
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in blocks], lag_ratio=0.15),
                  FadeIn(cohort), run_time=1.0)
        self.play(Create(dashes), FadeIn(thr_l), FadeIn(xl3), run_time=0.8)

        atr = T("atresia:\ndegeneration", 22, RED, line_spacing=0.8).move_to([4.9, -2.45, 0])
        self.at("that ends almost")
        self.play(FadeIn(atr), run_time=0.5)

        inh = bchip("inhibin B", GOLD, 28).move_to([4.9, 3.05, 0])
        self.at("rescued follicles make")
        self.play(FadeIn(inh, shift=DOWN * 0.2), run_time=0.5)
        tgt = ax.c2p(4.0, f(4.0))
        sup = Line(P3(3.9, 3.05), P3(tgt[0] + 0.05, tgt[1] + 0.1), color=RED, stroke_width=5)
        n = (sup.get_end() - sup.get_start())
        n = np.array([-n[1], n[0], 0]) / np.linalg.norm(n)
        bar = Line(sup.get_end() + n * 0.3, sup.get_end() - n * 0.3, color=RED, stroke_width=7)
        sup_l = T("suppresses pituitary FSH", 22, RED).move_to([0.2, 2.85, 0])
        self.at("suppresses pituitary")
        self.play(Create(sup), FadeIn(bar), FadeIn(sup_l), run_time=0.8)

        # FSH falls: first a little, then through the thresholds
        part1 = ax.plot(f, x_range=[2.0, 3.2], color=BLUE, stroke_width=6)
        self.at("lowers the very hormone")
        self.play(Create(part1), run_time=1.0)

        def tcross(h):
            ts = np.linspace(2.0, 10, 4000)
            v = f(ts)
            return ts[np.argmax(v < h)]
        cross_t = [tcross(h) for h in thr[:4]]
        t_dom = self.t_of("It becomes dominant") - 0.5
        self.at("saved it", lead=0.0)
        t0 = self.elapsed()
        span = max(2.5, t_dom - t0 - 1.9)
        seg = 10 - 3.2
        cur = 3.2
        for i, ct in enumerate(cross_t + [10.0]):
            if ct <= cur:
                ct = cur + 0.01
            part = ax.plot(f, x_range=[cur, ct], color=BLUE, stroke_width=6)
            rt = span * (ct - cur) / seg
            self.play(Create(part, rate_func=linear), run_time=max(rt, 0.1))
            if i < 4:
                self.play(blocks[i].animate.set_opacity(0.28), dashes[i].animate.set_opacity(0.15), run_time=0.2)
            cur = ct
        keep = blocks[4]
        self.at("keeps growing")
        self.play(keep[0].animate.set_color(TEAL).set_fill(TEAL, 0.25), keep[1].animate.set_color(TEAL),
                  dashes[4].animate.set_color(TEAL).set_opacity(0.9), run_time=0.6)
        dom = T("keeps growing:\ndominant", 22, TEAL, weight=BOLD, line_spacing=0.8).move_to([4.9, -2.45, 0])
        self.at("It becomes dominant")
        self.play(FadeOut(atr), run_time=0.25)
        self.play(FadeIn(dom), run_time=0.3)
        xs = VGroup(*[VGroup(Line(b.get_corner(UL), b.get_corner(DR), color=RED, stroke_width=4),
                             Line(b.get_corner(UR), b.get_corner(DL), color=RED, stroke_width=4))
                      for b in [blocks[i][0] for i in range(4)]])
        atr2 = T("atresia", 24, RED, weight=BOLD).move_to([4.9, 2.2, 0])
        self.at("The rest undergo")
        self.play(Create(xs), FadeOut(cohort), run_time=0.6)
        self.play(FadeIn(atr2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Twocell(SpokenScene):
    """Theca (LH receptor, CYP17) makes androgen; granulosa (FSH receptor, aromatase) makes estrogen;
    granulosa gains LH receptors."""

    def construct(self):
        BX, BW = -1.7, 9.0                      # follicle wall blocks: x from -6.2 to 2.8
        theca = box(BW, 2.5, GREY, 0.10, 3, pos=(BX, 2.15))
        gran = box(BW, 2.5, GREY, 0.10, 3, pos=(BX, -0.6))
        memb = Rectangle(width=BW, height=0.14, stroke_width=0, fill_color=TEXT, fill_opacity=0.8).move_to(P3(BX, 0.78))
        t_lab = T("theca cells\noutside", 24, TEXT, line_spacing=0.8).move_to([-5.0, 2.15, 0])
        g_lab = T("granulosa cells\ninside", 24, TEXT, line_spacing=0.8).move_to([-4.85, -0.6, 0])
        m_lab = T("basement\nmembrane", 22, GREY, line_spacing=0.8).move_to([4.55, 0.78, 0])
        self.at("two cell types")
        self.play(FadeIn(theca), FadeIn(gran), FadeIn(t_lab), FadeIn(g_lab), run_time=0.9)
        self.at("outside the basement")
        self.play(FadeIn(memb, scale=1.02), FadeIn(m_lab), run_time=0.7)

        lh_r = bchip("LH receptor", YELLOW, 24).move_to([-2.3, 2.6, 0])
        cyp = bchip("CYP17", TEXT, 24).move_to([1.3, 2.6, 0])
        self.at("carry")
        self.play(FadeIn(lh_r, scale=0.8), run_time=0.5)
        self.at("an enzyme")
        self.play(FadeIn(cyp, scale=0.8), run_time=0.5)
        andro = bchip("androgen", ORANGE, 24).move_to([1.65, 1.55, 0])
        self.at("make androgen")
        self.play(FadeIn(andro, shift=DOWN * 0.25), run_time=0.6)

        fsh_r = bchip("FSH receptor", BLUE, 24).move_to([-1.9, 0.15, 0])
        arom = bchip("aromatase", TEXT, 24).move_to([0.5, 0.15, 0])
        self.at("Granulosa cells inside")
        self.play(Indicate(gran, color=TEXT, scale_factor=1.02), run_time=0.7)
        self.play(FadeIn(fsh_r, scale=0.8), FadeIn(arom, scale=0.8), run_time=0.7)

        est = bchip("estrogen", PINK, 24).move_to([1.65, -1.25, 0])
        out = arr([2.95, -1.25, 0], [3.7, -1.25, 0], PINK, 4, 0.2)
        out_l = T("estrogen,\nmainly estradiol", 22, PINK, line_spacing=0.8).move_to([5.1, -1.25, 0])
        self.at("converts the androgen")
        self.play(andro.animate.move_to([1.65, -1.25, 0]), run_time=0.9)
        self.play(ReplacementTransform(andro, est), run_time=0.6)
        self.play(GrowArrow(out), FadeIn(out_l), run_time=0.7)

        lh2 = bchip("LH receptor", YELLOW, 24).move_to([-1.9, -1.25, 0])
        gained = T("gained", 22, GREEN).next_to(lh2, RIGHT, buff=0.2)
        self.at("gain")
        self.play(FadeIn(lh2, scale=0.6), FadeIn(gained), run_time=0.7)
        self.play(Indicate(lh2, color=YELLOW, scale_factor=1.12), run_time=0.7)

        ans = T("responds to LH as well as FSH", 30, TEAL).move_to([-1.7, -2.75, 0])
        self.at("most mature follicle")
        self.play(FadeIn(ans, shift=UP * 0.15), run_time=0.6)
        fsh_f = bchip("FSH", BLUE, 24).move_to([4.4, -2.75, 0])
        down = arr([5.4, -2.4, 0], [5.4, -3.15, 0], RED, 5, 0.2)
        falling = T("falling", 22, RED).move_to([5.45, -3.4, 0])
        self.at("while")
        self.play(FadeIn(fsh_f), GrowArrow(down), FadeIn(falling), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Switch(SpokenScene):
    """Estradiol feedback: brake (negative) for most of the cycle; late in the follicular phase it flips to
    positive feedback and LH surges."""

    def construct(self):
        Y = 1.0
        hyp = VGroup(box(3.0, 1.7, GREY, 0.10, pos=(-4.7, Y)), T("hypothalamus", 26, TEXT).move_to([-4.7, Y + 0.3, 0]),
                     T("GnRH release", 22, GREY).move_to([-4.7, Y - 0.3, 0]))
        pit = VGroup(box(3.0, 1.7, GREY, 0.10, pos=(0, Y)), T("pituitary", 26, TEXT).move_to([0, Y + 0.3, 0]),
                     T("LH release", 22, YELLOW).move_to([0, Y - 0.3, 0]))
        ova = VGroup(box(3.0, 1.7, GREY, 0.10, pos=(4.7, Y)), T("ovary", 26, TEXT).move_to([4.7, Y + 0.3, 0]),
                     T("dominant follicle", 22, GREY).move_to([4.7, Y - 0.3, 0]))
        a1 = arr([-3.15, Y, 0], [-1.65, Y, 0], GREY, 5)
        a2 = arr([1.65, Y, 0], [3.15, Y, 0], YELLOW, 5)
        l1 = T("GnRH", 22, GREY).move_to([-2.4, Y + 0.45, 0])
        l2 = T("LH", 24, YELLOW).move_to([2.4, Y + 0.45, 0])
        self.at("most of the cycle")
        self.play(LaggedStart(FadeIn(hyp), FadeIn(pit), FadeIn(ova), lag_ratio=0.25), run_time=0.8)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(l1), FadeIn(l2), run_time=0.4)

        # the feedback path (pink), ending in brakes
        FY = -1.15
        seg_l = Line(P3(0, FY), P3(-4.7, FY), color=PINK, stroke_width=6)
        path_main = VGroup(Line(P3(4.7, Y - 0.85), P3(4.7, FY), color=PINK, stroke_width=6),
                           Line(P3(4.7, FY), P3(0, FY), color=PINK, stroke_width=6), seg_l)
        up_p = Line(P3(0, FY), P3(0, Y - 0.95), color=PINK, stroke_width=6)
        up_h = Line(P3(-4.7, FY), P3(-4.7, Y - 0.95), color=PINK, stroke_width=6)
        cap_p = cap(0, Y - 0.9)
        cap_h = cap(-4.7, Y - 0.9)
        e_lab = T("estradiol", 28, PINK, weight=BOLD).move_to([2.4, FY - 0.4, 0])
        brake = T("BRAKE: lowers release", 36, RED, weight=BOLD).move_to([0, -2.4, 0])
        self.at("estradiol is a")
        self.play(Create(path_main), FadeIn(e_lab), run_time=0.7)
        self.play(Create(up_p), Create(up_h), run_time=0.4)
        self.play(FadeIn(cap_p), FadeIn(cap_h), run_time=0.2)
        self.at("It lowers")
        self.play(FadeIn(brake, shift=UP * 0.15), run_time=0.6)

        late = T("late in the follicular phase", 26, TEXT).move_to([0, 3.0, 0])
        self.at("Late in the follicular")
        self.play(FadeIn(late), run_time=0.5)
        dom = ova[0]
        self.at("from the dominant follicle")
        self.play(dom.animate.set_color(TEAL).set_fill(TEAL, 0.2), run_time=0.5)
        e_lab2 = T("estradiol, high for long enough", 28, PINK, weight=BOLD).move_to([2.0, FY - 0.4, 0])
        self.at("stays high for long")
        self.play(Transform(e_lab, e_lab2), run_time=0.6)

        tri_p = head(0, Y - 0.85)
        tri_h = head(-4.7, Y - 0.85)
        accel = T("ACCELERATOR: raises its own trigger", 36, GREEN, weight=BOLD).move_to([0, -2.4, 0])
        pos_l = T("positive feedback", 26, GREEN).move_to([0, -3.05, 0])
        self.at("becomes positive feedback")
        self.play(ReplacementTransform(cap_p, tri_p), ReplacementTransform(cap_h, tri_h),
                  Transform(brake, accel), FadeIn(pos_l), run_time=1.0)

        surge = bchip("LH surge", YELLOW, 30).move_to([0, 3.0, 0])
        up = arr([0, Y + 0.9, 0], [0, 2.55, 0], YELLOW, 5, 0.2)
        self.at("climbs steeply")
        self.play(FadeOut(late), run_time=0.3)
        self.play(GrowArrow(up), FadeIn(surge, scale=0.8), pit[0].animate.set_color(YELLOW).set_fill(YELLOW, 0.2),
                  run_time=0.8)

        mice = T("most mechanistic work is in mice; whether women have a GnRH surge is debated;\nthe site of positive feedback in women is not settled", 22, GREY, line_spacing=0.8).move_to([0, -3.15, 0])
        self.at("in mice")
        self.play(FadeOut(pos_l), run_time=0.3)
        self.play(FadeIn(mice), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def e2_curve(t):
    """Sketch: slow climb to a late-follicular peak, a dip after ovulation, a smaller luteal rise."""
    s = np.where(t < -1.5, 3.2, 1.0)
    pre = 0.80 * np.exp(-((t + 1.5) / s) ** 2)
    lut = 0.30 * np.exp(-((t - 7.0) / 3.3) ** 2)
    return 0.10 + pre + lut


def lh_curve(t):
    return 0.08 + 0.92 * np.exp(-((t + 0.6) / 0.4) ** 2)


def fsh_curve(t):
    sl = np.where(t < -12.0, 1.1, 3.0)
    return 0.15 + 0.60 * np.exp(-((t + 12.0) / sl) ** 2) + 0.55 * np.exp(-((t - 14.0) / 2.6) ** 2)


def p4_curve(t):
    early = 0.12 * sig((t + 1.0) / 0.5)
    lut = 0.88 * sig((t - 1.2) / 1.5) * np.exp(-(np.maximum(t - 7.0, 0) / 4.6) ** 2)
    return 0.04 + early + lut


class S05Curves(SpokenScene):
    """One time axis aligned to ovulation: FSH, estradiol, LH, progesterone in the lesson's order."""

    def construct(self):
        ax = sketch_axes([-14, 14, 1], [0, 1.1, 0.5], 11.6, 5.0, (-5.9, -2.55))
        x0 = ax.c2p(0, 0)[0]
        ovl = DashedLine(P3(x0, -2.55), P3(x0, 2.6), color=TEXT, stroke_width=3, dash_length=0.18)
        ov_l = T("ovulation", 26, TEXT, weight=BOLD).move_to([x0, 2.95, 0])
        fol = T("follicular phase", 24, GREY).move_to([-3.3, -3.05, 0])
        lut = T("luteal phase", 24, GREY).move_to([3.4, -3.05, 0])
        skl = T("relative units, in this sketch", 22, GREY).move_to([4.2, 3.2, 0])
        self.at("this sketch")
        self.play(Create(ax), Create(ovl), FadeIn(ov_l), FadeIn(fol), FadeIn(lut), FadeIn(skl), run_time=0.9)

        def plot(fn, a, b, col):
            return ax.plot(fn, x_range=[a, b], color=col, stroke_width=6)

        fsh1 = plot(fsh_curve, -14, -3, BLUE)
        fsh_l = T("FSH", 30, BLUE, weight=BOLD).move_to([ax.c2p(-9.6, 0.8)[0], ax.c2p(-9.6, 0.8)[1], 0])
        self.at("rises at the end")
        self.play(Create(fsh1, rate_func=linear), FadeIn(fsh_l), run_time=2.6)

        e2a = plot(e2_curve, -14, -0.4, PINK)
        e2_l = T("estradiol", 28, PINK, weight=BOLD).move_to([ax.c2p(-3.4, 0.82)[0] - 0.9, ax.c2p(-3.4, 0.82)[1] + 0.3, 0])
        self.at("Estradiol climbs")
        self.play(Create(e2a, rate_func=linear), FadeIn(e2_l), run_time=3.0)

        lhc = plot(lh_curve, -14, 14, YELLOW)
        lh_l = T("LH", 30, YELLOW, weight=BOLD).move_to([ax.c2p(0.9, 0.95)[0] + 0.4, ax.c2p(0.9, 0.95)[1] + 0.1, 0])
        self.at("surges within a day")
        self.play(Create(lhc, rate_func=linear), FadeIn(lh_l), run_time=2.4)

        on = ax.c2p(-1.45, 0)[0]
        brk = VGroup(DoubleArrow(P3(on, 2.35), P3(x0, 2.35), color=YELLOW, stroke_width=4, tip_length=0.18, buff=0),
                     DashedLine(P3(on, 2.35), P3(on, ax.c2p(0, 0.08)[1]), color=YELLOW, stroke_width=2, dash_length=0.1))
        brk_l = T("surge onset roughly\n34 to 36 hours before ovulation\n(textbook; intervals vary widely)",
                  22, YELLOW, line_spacing=0.8).move_to([3.9, 1.95, 0])
        self.at("surge onset roughly")
        self.play(Create(brk), FadeIn(brk_l), run_time=0.9)

        p4 = plot(p4_curve, -14, 14, PURPLE)
        p4_l = T("progesterone", 28, PURPLE, weight=BOLD).move_to([ax.c2p(12.3, 1.0)[0], ax.c2p(12.3, 1.0)[1], 0])
        self.at("begins to rise shortly")
        self.play(FadeOut(brk), FadeOut(brk_l), run_time=0.4)
        self.play(Create(p4, rate_func=linear), FadeIn(p4_l), run_time=3.4)

        e2b = plot(e2_curve, -0.4, 14, PINK)
        self.at("second smaller rise")
        self.play(Create(e2b, rate_func=linear), run_time=2.0)

        fsh2 = plot(fsh_curve, -3, 14, BLUE)
        self.at("FSH rises again")
        self.play(Create(fsh2, rate_func=linear), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Luteal(SpokenScene):
    """Progesterone in episodes after LH pulses; a single sample is one point."""

    def construct(self):
        cl = VGroup(box(4.8, 2.4, GREY, 0.12, pos=(-3.3, 0.2)), T("corpus luteum", 40, TEXT).move_to([-3.3, 0.2, 0]))
        pg = bchip("progesterone", PURPLE, 44).move_to([3.7, 0.2, 0])
        ar = arr([-0.7, 0.2, 0], [1.4, 0.2, 0], PURPLE, 7)
        self.at("After ovulation")
        self.play(FadeIn(cl, scale=0.9), run_time=0.7)
        self.at("secretes progesterone")
        self.play(GrowArrow(ar), FadeIn(pg, scale=0.8), run_time=0.9)

        # axes: LH on top, progesterone below, time in hours
        axl = sketch_axes([0, 24, 4], [0, 1.1, 0.5], 11.4, 1.3, (-5.7, 2.0))
        axp = sketch_axes([0, 24, 4], [0, 1.1, 0.5], 11.4, 3.0, (-5.7, -2.45))
        pulses = [0.7, 3.4, 6.0, 8.9, 11.5, 14.4, 17.0, 19.8, 22.5]
        amps = [0.7, 1.0, 0.8, 0.95, 0.6, 1.0, 0.75, 0.9, 0.65]

        def lh(t):
            v = 0.06
            for p, a in zip(pulses, amps):
                v += 0.9 * a * np.exp(-((t - p) / 0.28) ** 2)
            return v

        def p4(t):
            v = 0.10
            for p, a in zip(pulses, amps):
                d = t - (p + 0.25)
                v += 0.85 * a * np.where(d > 0, (1 - np.exp(-d / 0.18)) * np.exp(-d / 0.75), 0.0)
            return v

        # sample ticks (every 10 minutes: 144 over 24 hours)
        ticks = VGroup(*[Line(P3(axp.c2p(h / 6.0, 0)[0], -2.97), P3(axp.c2p(h / 6.0, 0)[0], -2.75), color=TEXT,
                              stroke_width=1.5) for h in range(0, 145)])
        tick_l = T("a blood sample every 10 minutes", 22, GREY).move_to([-3.4, -3.3, 0])
        hrs_l = T("24 hours", 22, GREY).move_to([4.6, -3.3, 0])
        self.at("blood was drawn")
        self.play(FadeOut(cl), FadeOut(ar), FadeOut(pg), run_time=0.5)
        self.play(Create(axp), run_time=0.6)
        self.play(Create(ticks, lag_ratio=0.02), FadeIn(tick_l), FadeIn(hrs_l), run_time=2.2)

        p_l = T("progesterone", 26, PURPLE, weight=BOLD).move_to([-4.6, 0.78, 0])
        sk = T("relative units, in this sketch", 22, GREY).move_to([4.6, 0.78, 0])
        pcurve = axp.plot(p4, x_range=[0, 24, 0.03], color=PURPLE, stroke_width=5, use_smoothing=False)
        self.at("progesterone rose in episodes")
        self.play(Create(pcurve, rate_func=linear), FadeIn(p_l), FadeIn(sk), run_time=1.3)

        lh_l = T("LH, in this sketch", 24, YELLOW, weight=BOLD).move_to([-4.5, 3.4, 0])
        axl_c = Create(axl)
        lcurve = axl.plot(lh, x_range=[0, 24, 0.03], color=YELLOW, stroke_width=5, use_smoothing=False)
        guides = VGroup(*[DashedLine(P3(axl.c2p(p, 0)[0], 2.0), P3(axl.c2p(p, 0)[0], -2.3), color=YELLOW,
                                     stroke_width=1.8, dash_length=0.12).set_opacity(0.55) for p in pulses])
        self.at("after LH pulses")
        self.play(axl_c, FadeIn(lh_l), run_time=0.5)
        self.play(Create(lcurve, rate_func=linear), run_time=1.3)
        self.play(Create(guides), run_time=0.4)

        rng = VGroup(box(7.0, 0.85, PURPLE, 0.14, 3, pos=(0, 1.45)),
                     T("values ranged from 2.3 to 40.1 ng per mL", 22, PURPLE).move_to([0, 1.62, 0]),
                     T("across the sampled women and times", 20, GREY).move_to([0, 1.29, 0]))
        self.at("ranged from")
        self.play(FadeOut(guides), FadeIn(rng, scale=0.95), run_time=0.7)

        s1t, s2t = 4.3, 8.9 + 0.25 + 0.5
        d1 = Dot(axp.c2p(s1t, p4(s1t)), color=TEXT, radius=0.13)
        d2 = Dot(axp.c2p(s2t, p4(s2t)), color=TEXT, radius=0.13)
        l1 = T("one sample", 22, TEXT).next_to(d1, UP, buff=0.15)
        l2 = T("one sample", 22, TEXT).next_to(d2, UP, buff=0.15)
        self.at("one sample cannot")
        self.play(FadeOut(rng), run_time=0.4)
        self.play(FadeIn(d1, scale=2), FadeIn(l1), run_time=0.6)
        self.play(FadeIn(d2, scale=2), FadeIn(l2), run_time=0.6)

        seqa = arr(axp.c2p(0.5, 0.0) + DOWN * 0.0 + P3(0, 0.0), axp.c2p(23.5, 0.0), GREEN, 6)
        seq_l = T("a sequence in time", 30, GREEN, weight=BOLD).move_to([0, 0.4, 0])
        self.at("a sequence in time")
        self.play(FadeOut(l1), FadeOut(l2), FadeOut(d1), FadeOut(d2), FadeIn(seq_l), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Read a pulsatile hormone as a sequence in time."
