"""Myelination: wrap the axon, make the signal jump  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the axon
  PURPLE = myelin / the glial membrane wrapped around the axon
  YELLOW = the action potential and the current that carries it
  RED    = current leaking out across the membrane
  GREEN  = nodes and their sodium channels
  GREY   = labels, outlines, axes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"

AX_X0, AX_X1 = -6.1, 6.1


def axon_bar(x0=AX_X0, x1=AX_X1, y=0.0, h=1.4, op=0.22):
    r = Rectangle(width=x1 - x0, height=h, stroke_color=BLUE, stroke_width=3.5,
                  fill_color=BLUE, fill_opacity=op)
    return r.move_to([(x0 + x1) / 2, y, 0])


def sheath_rects(pitch, w=1.8, h=3.4, y=0.0, n=5):
    return VGroup(*[Rectangle(width=w, height=h, stroke_color=PURPLE, stroke_width=3,
                              fill_color=PURPLE, fill_opacity=0.35).move_to([(i - 2) * pitch, y, 0])
                    for i in range(n)])


def leak(x, y0, y1, color=RED, w=5):
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, color=color, stroke_width=w, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.5)


def spiral(cx, r_out, pitch, turns=4, width=6):
    return ParametricFunction(
        lambda t: np.array([cx + (r_out - pitch * t / TAU) * np.cos(t),
                            (r_out - pitch * t / TAU) * np.sin(t), 0.0]),
        t_range=[0, TAU * turns, 0.05], color=PURPLE, stroke_width=width)


class S00Title(TitleCard):
    LESSON = "Myelination: Wrapping the Axon"
    TITLE = "Wrap the axon, make the signal jump"


# ---------------------------------------------------------------------------------------------
class S01Creep(SpokenScene):
    """A bare axon leaks; the pulse is rebuilt patch by patch and creeps."""

    def construct(self):
        y = -0.3
        axon = axon_bar(y=y, h=2.0)
        divs = VGroup(*[Line([x, y - 1.0, 0], [x, y + 1.0, 0], color=BLUE, stroke_width=2).set_opacity(0.5)
                        for x in (-4.1, -2.05, 0.0, 2.05, 4.1)])
        q = T("Fast, down a thin axon?", 38, TEXT, font=TITLE_FONT).move_to([0, 2.75, 0])
        lbl = T("bare axon", 30, BLUE).move_to([0, -2.75, 0])
        centers = [-5.1, -3.05, -1.0, 1.0, 3.05, 5.1]
        pulse = Rectangle(width=2.0, height=2.0, stroke_width=0, fill_color=YELLOW, fill_opacity=0.65)
        pulse.move_to([centers[0] - 0.05, y, 0])

        self.at("How does a nerve signal")
        self.play(FadeIn(axon), FadeIn(divs), Write(q), run_time=1.0)
        self.play(FadeIn(pulse, scale=0.8), run_time=0.4)
        self.at("leaky garden hose")
        self.play(FadeIn(lbl, shift=UP * 0.15), run_time=0.5)
        self.at("Current leaks out")
        arrows = VGroup()
        for cx in centers:
            for dx in (-0.45, 0.45):
                arrows.add(leak(cx + dx, y + 1.05, y + 1.8), leak(cx + dx, y - 1.05, y - 1.8))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.03), run_time=1.2)
        self.at("rebuilt on every patch")
        T0 = self.elapsed()
        T1 = self.narration_s - 0.3
        slow = T("slow", 34, TEXT, weight=BOLD).move_to([0, -3.4, 0])
        shown = False
        for k in range(1, 6):
            tgt = T0 + (T1 - T0) * k / 5
            nxt = pulse.copy().move_to([centers[k], y, 0])
            anims = [FadeOut(pulse), FadeIn(nxt)]
            if not shown and self.elapsed() >= self.t_of("That is slow") - 0.3:
                anims.append(FadeIn(slow, shift=UP * 0.1)); shown = True
            self.play(*anims, run_time=0.4)
            pulse = nxt
            rest = tgt - self.elapsed()
            if rest > 0.02:
                self.wait(rest)
        if not shown:
            self.add(slow)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Wrap(SpokenScene):
    """Cross-section: a glial cell winds its membrane around the axon, then it is squeezed tight."""

    def construct(self):
        cx = -2.7
        axon = Circle(radius=1.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25)
        axon.move_to([cx, 0, 0])
        a_lbl = T("axon", 32, BLUE).move_to(axon)
        blob = Ellipse(width=3.0, height=2.4, stroke_color=PURPLE, stroke_width=4,
                       fill_color=PURPLE, fill_opacity=0.25).move_to([4.1, 0, 0])
        g_lbl = T("glial cell", 30, PURPLE).move_to(blob)
        self.at("The answer is to wrap it")
        self.play(FadeIn(axon, scale=0.9), FadeIn(a_lbl), run_time=0.7)
        self.at("Myelin is membrane")
        self.play(FadeIn(blob, scale=0.9), FadeIn(g_lbl), run_time=0.7)

        b1 = T("brain: oligodendrocyte", 24, PURPLE).move_to([3.9, -1.95, 0])
        b2 = T("nerve: Schwann cell", 24, PURPLE).move_to([3.9, -1.95, 0])
        self.at("In the brain")
        self.play(FadeIn(b1, shift=UP * 0.1), run_time=0.4)
        self.at("In a nerve")
        self.play(ReplacementTransform(b1, b2), run_time=0.5)

        loose = VGroup(Line([2.6, 0, 0], [cx + 1.3 + 0.3 * 4, 0, 0], color=PURPLE, stroke_width=6),
                       spiral(cx, 1.3 + 0.3 * 4, 0.3))
        cyto = T("cytoplasm between turns", 24, GREY).move_to([3.9, -2.75, 0])
        self.at("winds its membrane")
        self.play(FadeOut(b2), run_time=0.2)
        self.play(Create(loose[0]), run_time=0.4)
        self.play(Create(loose[1]), run_time=2.5, rate_func=linear)
        self.play(FadeIn(cyto), run_time=0.4)
        tight = VGroup(Line([2.6, 0, 0], [cx + 1.3 + 0.13 * 4, 0, 0], color=PURPLE, stroke_width=6),
                       spiral(cx, 1.3 + 0.13 * 4, 0.13, width=7))
        self.at("squeezed until")
        self.play(ReplacementTransform(loose, tight), FadeOut(cyto), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Insulate(SpokenScene):
    """Bare vs wrapped, side by side: leaks, resistance, capacitance, reach of the current."""

    def construct(self):
        y = 0.4
        xl, xr = -3.3, 3.3
        L = axon_bar(xl - 2.8, xl + 2.8, y, 1.2)
        R = axon_bar(xr - 2.8, xr + 2.8, y, 1.2)
        tl = T("bare", 32, BLUE).move_to([xl, 2.55, 0])
        tr = T("wrapped", 32, PURPLE).move_to([xr, 2.55, 0])
        strips = VGroup()
        for k in range(3):
            for sgn in (1, -1):
                yy = y + sgn * (0.6 + 0.08 + 0.16 * k)
                strips.add(Rectangle(width=5.6, height=0.16, stroke_color=PURPLE, stroke_width=2,
                                     fill_color=PURPLE, fill_opacity=0.4).move_to([xr, yy, 0]))
        self.at("Think of many thin walls")
        self.play(FadeIn(L), FadeIn(R), FadeIn(tl), FadeIn(tr), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(s, shift=s.get_center()[1] * 0.0 * UP) for s in strips],
                              lag_ratio=0.15), run_time=1.4)

        self.at("leaking much harder")
        leaks = VGroup()
        for i in range(5):
            x = xl - 2.2 + i * 1.1
            leaks.add(leak(x, y + 0.65, y + 1.45), leak(x, y - 0.65, y - 1.45))
        self.play(LaggedStart(*[GrowArrow(a) for a in leaks], lag_ratio=0.05), run_time=0.9)

        c1 = chip("higher resistance", PURPLE, 26).move_to([xr, -1.55, 0])
        c2 = chip("lower capacitance", PURPLE, 26).move_to([xr, -2.55, 0])
        self.at("raise the resistance")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("lower its capacitance")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)

        self.at("entering at one spot")
        dl = Dot([xl - 2.5, y, 0], radius=0.16, color=YELLOW)
        dr = Dot([xr - 2.5, y, 0], radius=0.16, color=YELLOW)
        self.play(FadeIn(dl), FadeIn(dr), run_time=0.4)
        al = arr_(xl - 2.5, 1.5, y)
        ar = arr_(xr - 2.5, 4.9, y)
        self.at("travels farther")
        self.play(GrowArrow(al), GrowArrow(ar), run_time=1.0)
        ahead = Rectangle(width=0.9, height=1.2, stroke_width=0, fill_color=YELLOW,
                          fill_opacity=0.6).move_to([xr + 2.35, y, 0])
        self.at("charges the membrane ahead")
        self.play(FadeIn(ahead), run_time=0.6)
        self.finish()


def arr_(x0, length, y):
    return Arrow([x0, y, 0], [x0 + length, y, 0], buff=0.1, color=YELLOW, stroke_width=7, tip_length=0.28,
                 max_tip_length_to_length_ratio=0.5)


# ---------------------------------------------------------------------------------------------
NODE_X = [-3.75, -1.25, 1.25, 3.75]


def build_wrapped(pitch):
    axon = axon_bar(h=1.8)
    axon.set_z_index(2)
    sheaths = sheath_rects(pitch)
    return axon, sheaths


class S04Nodes(SpokenScene):
    """The sheath opens into internodes with gaps; sodium channels sit only at the nodes."""

    def construct(self):
        axon, sheaths = build_wrapped(1.8)
        self.at("The wrap is not")
        self.play(FadeIn(sheaths), FadeIn(axon), run_time=0.8)
        self.at("Short gaps")
        self.play(*[s.animate.move_to([(i - 2) * 2.5, 0, 0]) for i, s in enumerate(sheaths)], run_time=1.2)

        node_lbl = T("node of Ranvier", 30, GREEN).move_to([-3.75, -2.95, 0])
        node_arr = Arrow([-3.75, -2.55, 0], [-3.75, -1.2, 0], buff=0.05, color=GREEN, stroke_width=5, tip_length=0.2)
        self.at("These gaps are")
        self.play(FadeIn(node_lbl), GrowArrow(node_arr), run_time=0.6)

        brace = Brace(sheaths[2], UP, color=PURPLE, buff=0.1)
        inter = T("internode", 30, PURPLE).next_to(brace, UP, buff=0.12)
        self.at("Each wrapped stretch")
        self.play(GrowFromCenter(brace), FadeIn(inter), run_time=0.7)

        chans = VGroup()
        for xn in NODE_X:
            for dx in (-0.2, 0.0, 0.2):
                for sgn in (1, -1):
                    chans.add(Rectangle(width=0.12, height=0.36, stroke_color=GREEN, stroke_width=2,
                                        fill_color=GREEN, fill_opacity=0.9).move_to([xn + dx, sgn * 0.9, 0]))
        na_lbl = T("sodium channels", 30, GREEN).move_to([3.75, -2.95, 0])
        na_arr = Arrow([3.75, -2.55, 0], [3.75, -1.3, 0], buff=0.05, color=GREEN, stroke_width=5, tip_length=0.2)
        self.at("sodium channels")
        self.play(LaggedStart(*[FadeIn(c, scale=1.6) for c in chans], lag_ratio=0.03), run_time=1.2)
        self.play(FadeIn(na_lbl), GrowArrow(na_arr), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Jump(SpokenScene):
    """The pulse is rebuilt only at the nodes and leaps from node to node."""

    def construct(self):
        axon, sheaths = build_wrapped(2.5)
        chans = VGroup()
        for xn in NODE_X:
            for dx in (-0.2, 0.0, 0.2):
                for sgn in (1, -1):
                    chans.add(Rectangle(width=0.12, height=0.36, stroke_color=GREEN, stroke_width=2,
                                        fill_color=GREEN, fill_opacity=0.9).move_to([xn + dx, sgn * 0.9, 0]))
        chans.set_z_index(3)
        self.add(sheaths, axon, chans)

        def glow(k):
            return Circle(radius=0.75, stroke_width=0, fill_color=YELLOW, fill_opacity=0.75).move_to([NODE_X[k], 0, 0]).set_z_index(4)

        self.at("Now follow the signal")
        dotp = Dot([AX_X0 + 0.2, 0, 0], radius=0.2, color=YELLOW).set_z_index(4)
        self.play(FadeIn(dotp), run_time=0.3)
        span = self.t_of("regenerated only at") - 0.5 - self.elapsed()
        self.play(dotp.animate.move_to([NODE_X[0], 0, 0]), run_time=max(0.5, span), rate_func=linear)
        g = glow(0)
        self.at("regenerated only at")
        self.remove(dotp)
        self.play(FadeIn(g, scale=0.4), run_time=0.5)
        under = Arrow([NODE_X[0] + 0.5, 0, 0], [NODE_X[1] - 0.5, 0, 0], buff=0, color=YELLOW,
                      stroke_width=7, tip_length=0.26).set_z_index(4)
        self.at("current spreads quietly")
        self.play(GrowArrow(under), run_time=0.9)
        g1 = glow(1)
        self.at("reaches the next node")
        self.play(FadeOut(under), FadeIn(g1, scale=0.4), FadeOut(g), run_time=0.5)
        self.at("rebuilt again")
        self.play(Indicate(g1, color=YELLOW, scale_factor=1.25), run_time=0.7)
        self.play(FadeOut(g1), run_time=0.3)

        arcs = [CurvedArrow([NODE_X[k], 2.0, 0], [NODE_X[k + 1], 2.0, 0], angle=-PI * 0.65, color=YELLOW,
                            stroke_width=6, tip_length=0.25) for k in range(3)]
        self.at("seems to leap")
        cur = glow(0)
        self.play(FadeIn(cur, scale=0.4), run_time=0.2)
        for k in range(3):
            nxt = glow(k + 1)
            self.play(Create(arcs[k]), FadeOut(cur), FadeIn(nxt, scale=0.5), run_time=0.55)
            cur = nxt
        self.at("salutatory")
        name = chip("saltatory conduction", YELLOW, 34).move_to([0, -2.9, 0])
        self.play(FadeIn(name, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Speed(SpokenScene):
    """Speed against diameter: square-root curve for bare axons, straight line for myelinated fibers."""

    def construct(self):
        ax = Axes(x_range=[0, 4.4, 1], y_range=[0, 10, 1], x_length=9.6, y_length=5.0, tips=False,
                  axis_config={"include_ticks": False, "include_numbers": False, "color": GREY, "stroke_width": 3})
        ax.move_to([0.4, -0.35, 0])
        xl = T("fiber diameter", 28, GREY).next_to(ax.x_axis, DOWN, buff=0.2).align_to(ax.x_axis, RIGHT)
        yl = T("speed", 28, GREY).next_to(ax.y_axis, LEFT, buff=0.2).align_to(ax.y_axis, UP)
        self.at("The gain is large")
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.0)

        bare = ax.plot(lambda x: 1.3 * np.sqrt(x), x_range=[0.3, 4.2], color=BLUE, stroke_width=6)
        bl = T("bare axon", 28, BLUE).move_to(ax.c2p(3.3, 1.3 * np.sqrt(3.3)) + DOWN * 0.55)
        self.at("square root of diameter")
        self.play(Create(bare), run_time=1.5, rate_func=linear)
        self.play(FadeIn(bl), run_time=0.4)

        line = ax.plot(lambda x: 2.2 * x, x_range=[0.3, 4.2], color=PURPLE, stroke_width=6)
        ml = T("myelinated", 28, PURPLE).move_to(ax.c2p(2.0, 2.2 * 2.0) + UL * 0.5 + LEFT * 0.5)
        self.at("in proportion to diameter")
        self.play(Create(line), run_time=1.5, rate_func=linear)
        self.play(FadeIn(ml), run_time=0.4)

        top = chip("tens of m/s", PURPLE, 26).move_to(ax.c2p(3.2, 9.2) + LEFT * 0.4)
        self.at("tens of meters per second")
        self.play(FadeIn(top, shift=RIGHT * 0.2), run_time=0.5)
        est = chip("about 6 m/s per µm", PURPLE, 26).move_to(ax.c2p(1.2, 7.4))
        self.at("classic estimate")
        self.play(FadeIn(est, shift=LEFT * 0.2), run_time=0.5)

        dot = Dot(ax.c2p(0.7, 1.3 * np.sqrt(0.7)), radius=0.14, color=BLUE)
        thin = VGroup(T("thin bare fiber:", 26, BLUE), T("about 1 m/s or less", 26, BLUE)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        thin.move_to(ax.c2p(2.9, 3.5))
        lead = DashedLine(dot.get_center(), thin.get_left() + LEFT * 0.1, color=BLUE, stroke_width=3)
        self.at("Thin bare fibers")
        self.play(FadeIn(dot, scale=2), Create(lead), FadeIn(thin), run_time=0.6)
        self.at("Wrap the axon")
        self.play(Indicate(line, color=PURPLE, scale_factor=1.04), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Wrap the axon, and the signal jumps from gap to gap."
