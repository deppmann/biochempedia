"""Vagal sensory neurons: a label is not a type  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = (periwinkle) the P2ry1-labelled set (airway protection afferents)
  YELLOW = the Npy2r-labelled set
  GREEN  = the Piezo2-positive stretch neurons, and "function" once tied
  RED    = breathing / inspiration halted
  TEAL   = light (optogenetic drive)
  ORANGE = the light-gated channel
  PINK   = an open question, candidate or hypothesis
  GREY   = nerve, structure, unlabelled cells, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BLUE = "#7C9CFF"   # P2ry1 set (distinct from the teal of light)
PURPLE = "#E58BC4"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell(color=GREY, r=0.36, pos=(0, 0)):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to([pos[0], pos[1], 0])


def membrane(cx, cy, w=4.0, h=0.3):
    return RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([cx, cy, 0])


def tube(x0, x1, y, h=1.0):
    return RoundedRectangle(corner_radius=0.3, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.15).move_to([(x0 + x1) / 2, y, 0])


def strand(x0, x1, y, color, w=9):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w)


class S00Title(TitleCard):
    LESSON = "Vagal sensory neurons"
    TITLE = "A label is not a type"


class S01Question(SpokenScene):
    def construct(self):
        prep = T("in an anaesthetized mouse", 26, GREY).move_to([0, 3.2, 0])
        nerve = tube(-4.6, 4.6, 0.6)
        nlab = T("vagus: sensory axons", 22, GREY).move_to([0, -0.2, 0])
        self.at("light on one set")
        self.play(FadeIn(nerve), FadeIn(prep), FadeIn(nlab), run_time=0.4)
        sa = strand(-4.3, -0.2, 0.6, BLUE)
        la = arr([-2.3, 2.5, 0], [-2.3, 1.3, 0], TEAL)
        ll = T("light", 24, TEAL).next_to(la, RIGHT, buff=0.1)
        self.play(Create(sa), run_time=0.6)
        self.play(GrowArrow(la), FadeIn(ll), run_time=0.4)
        ra = arr([-2.3, 0.05, 0], [-2.3, -0.8, 0], BLUE)
        rc = chip("breathing suppressed", BLUE, 26).move_to([-3.0, -1.4, 0])
        self.play(GrowArrow(ra), FadeIn(rc), run_time=0.6)
        self.at("light on another set")
        sb = strand(0.2, 4.3, 0.6, YELLOW)
        lb = arr([2.3, 2.5, 0], [2.3, 1.3, 0], TEAL)
        llb = T("light", 24, TEAL).next_to(lb, RIGHT, buff=0.1)
        self.play(Create(sb), run_time=0.6)
        self.play(GrowArrow(lb), FadeIn(llb), run_time=0.4)
        rb = arr([2.3, 0.05, 0], [2.3, -0.8, 0], YELLOW)
        rcb = chip("fast, shallow breathing", YELLOW, 26).move_to([3.0, -1.4, 0])
        self.play(GrowArrow(rb), FadeIn(rcb), run_time=0.6)
        self.at("sensory axons here")
        self.play(Indicate(nlab, color=TEXT, scale_factor=1.05), run_time=0.6)
        self.at("one cable")
        one = chip("one cable: the body is stretched", GREY, 26).move_to([0, -2.6, 0])
        self.play(FadeIn(one), run_time=0.5)
        self.at("could not happen")
        x = Cross(one, stroke_color=RED, stroke_width=6)
        self.play(Create(x), run_time=0.5)
        self.at("what does each set report")
        q = T("what does each set report?", 28, PURPLE).move_to([0, -3.4, 0])
        self.play(FadeIn(q), run_time=0.5)
        self.finish()


class S02Access(SpokenScene):
    def construct(self):
        xs = [-5.0 + 2.0 * i for i in range(6)]
        cols = [BLUE, GREY, YELLOW, GREY, BLUE, YELLOW]
        cells = VGroup(*[cell(GREY, 0.4, (x, 1.5)) for x in xs])
        glab = T("two ganglia at the base of the skull", 26, GREY).move_to([0, 2.75, 0])
        self.at("cell bodies")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.12), FadeIn(glab), run_time=1.2)
        self.at("genetic access")
        anims = []
        labs = VGroup()
        for c, col, x in zip(cells, cols, xs):
            if col != GREY:
                anims.append(c.animate.set_stroke(col).set_fill(col, 0.4))
                labs.add(T("P2ry1" if col == BLUE else "Npy2r", 22, col).move_to([x, 0.7, 0]))
        self.play(*anims, run_time=0.7)
        self.play(FadeIn(labs), run_time=0.5)
        self.at("in mice")
        mem = membrane(0, -1.7, 4.4)
        mlab = T("membrane of a labelled neuron", 24, GREY).move_to([0, -2.55, 0])
        ch = chip("light-gated channel", ORANGE, 26).move_to([0, -1.7, 0])
        chb = RoundedRectangle(corner_radius=0.14, width=ch[0].width, height=ch[0].height, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(ch[0])
        ch = VGroup(chb, *ch)
        self.play(FadeIn(mem), FadeIn(mlab), run_time=0.5)
        self.play(FadeIn(ch, shift=DOWN * 0.3), run_time=0.6)
        self.at("carry one label")
        self.play(Indicate(labs, color=TEXT, scale_factor=1.1), run_time=0.6)
        self.at("light then drives")
        la = arr([0, -0.2, 0], [0, -1.15, 0], TEAL)
        ll = T("light", 24, TEAL).next_to(la, RIGHT, buff=0.12)
        self.play(GrowArrow(la), FadeIn(ll), run_time=0.5)
        self.play(Indicate(VGroup(*ch[1:]), color=ORANGE, scale_factor=1.12), run_time=0.7)
        self.at("two labels")
        self.play(Indicate(labs[0], color=BLUE), Indicate(labs[2], color=YELLOW), run_time=0.8)
        self.finish()


def breathing(x0, w, yc, t_light, amp0, per0, amp1, per1, t_end=8.5, color=BLUE, sx=None):
    pts = []
    n = 500
    phase = 0.0
    prev_t = 0.0
    for i in range(n + 1):
        t = t_end * i / n
        if t < t_light:
            amp, per = amp0, per0
        else:
            amp, per = amp1, per1
        phase += 2 * np.pi * (t - prev_t) / per
        prev_t = t
        pts.append([x0 + w * t / t_end, yc + amp * np.sin(phase), 0])
    m = VMobject(stroke_color=color, stroke_width=5)
    m.set_points_smoothly([np.array(p) for p in pts[::5]])
    return m


class S03Light(SpokenScene):
    def construct(self):
        prep = T("mice under deep isoflurane, vagus exposed", 26, GREY).move_to([0, 3.25, 0])
        self.at("under deep")
        self.play(FadeIn(prep), run_time=0.5)
        W = 5.4
        panels = [(-3.4, BLUE, "P2ry1 neurons + light", "breathing suppressed"),
                  (3.4, YELLOW, "Npy2r neurons + light", "rapid shallow breathing")]
        lighted = []
        for cx, col, title, res in panels:
            t = T(title, 28, col).move_to([cx, 2.55, 0])
            base = Line([cx - W / 2, 0.75, 0], [cx + W / 2, 0.75, 0], color=GREY, stroke_width=1.5)
            tl = 4.0 / 8.5 * W
            lb = Rectangle(width=W - tl, height=0.18, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to([cx - W / 2 + tl + (W - tl) / 2, -0.35, 0])
            ltx = T("light on", 22, TEAL).move_to([lb.get_center()[0], -0.75, 0])
            lighted.append((cx, col, t, base, lb, ltx, res))
        # draw both baselines and the pre-light trace together with the first sentence of results
        a = lighted[0]; b = lighted[1]
        self.play(FadeIn(a[2]), FadeIn(b[2]), Create(a[3]), Create(b[3]), run_time=0.6)
        tr_a = breathing(-3.4 - W / 2, W, 0.75, 4.0, 0.55, 2.0, 0.06, 2.0, color=BLUE)
        tr_b = breathing(3.4 - W / 2, W, 0.75, 4.0, 0.55, 2.0, 0.2, 0.8, color=YELLOW)
        self.at("suppressed breathing")
        self.play(FadeIn(a[4]), FadeIn(a[5]), Create(tr_a), run_time=1.2)
        ra = T(a[6], 26, BLUE).move_to([-3.4, 1.9, 0])
        self.play(FadeIn(ra), run_time=0.4)
        self.at("rapid shallow breathing")
        self.play(FadeIn(b[4]), FadeIn(b[5]), Create(tr_b), run_time=1.2)
        rb = T(b[6], 26, YELLOW).move_to([3.4, 1.9, 0])
        self.play(FadeIn(rb), run_time=0.4)
        tag = T("breathing traces: in this sketch", 24, GREY).move_to([0, -3.3, 0])
        self.play(FadeIn(tag), run_time=0.4)
        self.at("nerve recordings")
        la = T("nerve recordings", 24, GREY).move_to([0, -1.35, 0])
        self.play(FadeIn(la), run_time=0.4)
        self.at("largely fast")
        ca = chip("largely fast A fibres", BLUE, 26).move_to([-3.4, -2.2, 0])
        self.play(FadeIn(ca, shift=UP * 0.2), run_time=0.5)
        self.at("largely slow")
        cb = chip("largely slow C fibres", YELLOW, 26).move_to([3.4, -2.2, 0])
        self.play(FadeIn(cb, shift=UP * 0.2), run_time=0.5)
        self.finish()


class S04Stop(SpokenScene):
    def construct(self):
        halt = chip("inspiration halts", RED, 28).move_to([4.7, 0.2, 0])
        # top route
        p = chip("P2ry1 neurons", BLUE, 26).move_to([-4.6, 2.3, 0])
        defence = chip("airway defence", BLUE, 26).move_to([-0.6, 2.3, 0])
        dl = T("apnoea, closed vocal folds,\nswallowing, expiratory reflexes", 22, GREY, line_spacing=0.9).move_to([-0.6, 1.2, 0])
        self.at("airway defense")
        self.play(FadeIn(p), run_time=0.4)
        self.play(GrowArrow(arr(p.get_right(), defence.get_left(), BLUE)), FadeIn(defence), run_time=0.6)
        self.play(FadeIn(dl), run_time=0.5)
        a1 = arr(defence.get_right() + RIGHT * 0.05, halt.get_top() + LEFT * 0.4, BLUE)
        self.play(FadeIn(halt), GrowArrow(a1), run_time=0.7)
        # bottom route
        self.at("second way")
        fill = chip("lung fills", GREY, 26).move_to([-5.0, -2.0, 0])
        self.play(FadeIn(fill), run_time=0.5)
        self.at("a filling lung")
        st = chip("stretch-responsive neurons", GREEN, 26).move_to([-0.1, -2.0, 0])
        a2 = arr(fill.get_right(), st.get_left(), GREEN)
        hb = T("Hering-Breuer reflex", 22, GREY).move_to([-3.0, -2.75, 0])
        self.play(GrowArrow(a2), FadeIn(st), run_time=0.6)
        self.play(FadeIn(hb), run_time=0.4)
        a3 = arr(st.get_right(), halt.get_bottom() + LEFT * 0.4, GREEN)
        self.play(GrowArrow(a3), run_time=0.6)
        self.at("ganglion imaging")
        tag = T("mouse ganglion imaging: most were Piezo2-positive, P2ry1-negative", 22, GREEN).move_to([0, -3.4, 0])
        self.play(FadeIn(tag), run_time=0.6)
        self.finish()


class S05Limits(SpokenScene):
    def construct(self):
        xs = [-4.5, 0.0, 4.5]
        h1 = chip("light: sufficiency", TEAL, 26).move_to([xs[0], 2.8, 0])
        h2 = chip("label, not sensor", BLUE, 26).move_to([xs[1], 2.8, 0])
        h3 = chip("cluster: candidate", PURPLE, 26).move_to([xs[2], 2.8, 0])
        # panel 1
        c1 = cell(BLUE, 0.5, (xs[0], 1.0))
        l1 = arr([xs[0] - 1.6, 1.0, 0], [xs[0] - 0.6, 1.0, 0], TEAL)
        t1 = T("what cells can do\nwhen driven", 24, TEXT, line_spacing=0.9).move_to([xs[0], -0.3, 0])
        q1 = T("what drives them\nin life?", 24, PURPLE, line_spacing=0.9).move_to([xs[0], -1.6, 0])
        # panel 2
        c2 = cell(BLUE, 0.5, (xs[1], 1.0))
        lab2 = chip("gene used as label", BLUE, 22).move_to([xs[1], 0.0, 0])
        m2 = membrane(xs[1], -0.9, 3.4)
        s2 = chip("the sensing molecule?", PURPLE, 22).move_to([xs[1], -1.8, 0])
        # panel 3
        rng = np.random.default_rng(4)
        dots = VGroup()
        centers = [(xs[2] - 1.0, 1.6), (xs[2] + 0.9, 1.5), (xs[2], 0.1)]
        cand = VGroup()
        for k, (cx, cy) in enumerate(centers):
            for _ in range(9):
                d = Dot(point=[cx + rng.normal(0, 0.22), cy + rng.normal(0, 0.18), 0], radius=0.07,
                        color=PURPLE if k == 2 else GREY)
                (cand if k == 2 else dots).add(d)
        ring = Circle(radius=0.55, color=PURPLE, stroke_width=3).move_to([xs[2], 0.1, 0])
        n3 = chip("NP19", PURPLE, 24).move_to([xs[2], -1.0, 0])
        t3 = T("candidate for the\ndefence reflexes", 22, GREY, line_spacing=0.9).move_to([xs[2], -2.1, 0])
        self.at("test of sufficiency")
        self.play(FadeIn(h1), run_time=0.4)
        self.play(FadeIn(c1), GrowArrow(l1), run_time=0.6)
        self.play(FadeIn(t1), run_time=0.5)
        self.at("not what drives")
        self.play(FadeIn(q1), run_time=0.5)
        self.at("receptor gene")
        self.play(FadeIn(h2), FadeIn(c2), run_time=0.6)
        self.play(FadeIn(lab2), run_time=0.4)
        self.at("senses")
        self.play(FadeIn(m2), FadeIn(s2), run_time=0.6)
        self.at("candidate")
        self.play(FadeIn(h3), FadeIn(dots), FadeIn(cand), run_time=0.7)
        self.play(Create(ring), FadeIn(n3), run_time=0.6)
        self.play(FadeIn(t3), run_time=0.5)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        nerve = tube(-6.0, -2.4, 2.2, 0.9)
        cols = [BLUE, YELLOW, GREEN, GREY, GREY, GREY, GREY]
        ys = [3.05, 2.7, 2.35, 2.0, 1.65, 1.3, 0.95]
        self.at("not one cable")
        self.play(FadeIn(nerve), run_time=0.5)
        cable = strand(-5.8, -2.6, 2.2, GREY, 8)
        self.play(Create(cable), run_time=0.4)
        nl = T("vagus: sensory axons", 24, GREY).next_to(nerve, DOWN, buff=0.25).align_to(nerve, LEFT)
        self.play(FadeIn(nl), run_time=0.3)
        self.at("many types")
        fan = VGroup(*[Line([-2.4, 2.2, 0], [3.0, y, 0], color=c, stroke_width=7) for c, y in zip(cols, ys)])
        self.play(ReplacementTransform(cable.copy(), fan), run_time=0.9)
        self.remove(cable)
        self.play(FadeIn(Dot([-2.4, 2.2, 0], radius=0.08, color=GREY)), run_time=0.1)
        jobs = T("different types,\nsome tied to\ndifferent jobs", 24, TEXT, line_spacing=0.9).move_to([5.0, 2.0, 0])
        self.play(FadeIn(jobs), run_time=0.4)
        self.at("atlases give")
        at = T("atlases: counts differ with scope", 24, GREY).move_to([3.4, 0.3, 0])
        self.play(FadeIn(at), run_time=0.5)
        c1 = chip("label: a handle", BLUE, 28).move_to([-4.8, -1.5, 0])
        c2 = chip("type: a hypothesis", PURPLE, 28).move_to([-0.1, -1.5, 0])
        c3 = chip("function", GREEN, 28).move_to([4.7, -1.5, 0])
        self.at("a label is a handle")
        self.play(FadeIn(c1), run_time=0.5)
        self.at("a type is a hypothesis")
        a1 = arr(c1.get_right(), c2.get_left(), GREY)
        self.play(GrowArrow(a1), FadeIn(c2), run_time=0.6)
        self.at("ties it to one")
        a2 = arr(c2.get_right(), c3.get_left(), GREEN)
        tie = T("genetic access, physiology\nor behaviour", 22, GREY, line_spacing=0.9).move_to([2.35, -0.55, 0])
        self.play(GrowArrow(a2), FadeIn(c3), FadeIn(tie), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A label is a handle. A type is a hypothesis until tested."
