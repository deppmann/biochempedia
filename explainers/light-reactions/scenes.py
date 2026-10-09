"""From light to ATP and NADPH  (Biochemistrypedia explainer, lesson: light-reactions)

Every cue is timed to the SPOKEN words of the lesson's own slide audio (audio/words.json from align.py).

COLOR MAP (one color per concept, whole video)
  YELLOW = light: photons, excitation energy, the excited state
  BLUE   = the electron (always a small dot)
  RED    = protons, H+ (the lumen gradient)
  PINK   = water and oxygen (kept clear of the electron's blue)
  GREEN  = ATP
  PURPLE = NADPH (reducing power)
  ORANGE = heat (wasted energy)
  GOLD   = "this is the key moment" frames, used sparingly
  GREY   = membranes, protein complexes, axes, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F2994A"
PINK = "#F08BC8"   # water / O2


def Mk(markup, size=26, color=TEXT, **kw):
    """Text with <sub>/<sup> markup (no LaTeX)."""
    return MarkupText(markup, font=FONT, font_size=size, color=color, **kw)


def P(x, y):
    return np.array([x, y, 0.0])


def wave(p0, p1, color=YELLOW, amp=0.11, cycles=4, width=4):
    """A photon: a wavy line from p0 to p1."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    u = d / np.linalg.norm(d)
    n = np.array([-u[1], u[0], 0.0])
    return ParametricFunction(lambda t: p0 + d * t + n * amp * np.sin(2 * PI * cycles * t),
                              t_range=[0, 1, 0.01], color=color, stroke_width=width)


def edot(pos, r=0.11):
    """An electron: a small blue dot."""
    return Dot(pos, radius=r, color=BLUE)


def glow(pos, color=YELLOW, r=0.32, op=0.28):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to(pos)


def sign(ch, pos, color, r=0.17):
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=BG_FILL, fill_opacity=1)
    t = T(ch, 24, color, weight=BOLD)
    return VGroup(c, t.move_to(c)).move_to(pos)


BG_FILL = "#0f1117"


def proton(pos, size=22, r=0.22):
    c = Circle(radius=r, stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.18)
    t = Mk("H<sup>+</sup>", size, RED)
    return VGroup(c, t.move_to(c)).move_to(pos)


def water(pos, size=24):
    return chip_mk("H<sub>2</sub>O", PINK, size).move_to(pos)


def chip_mk(markup, color, size=26, pad=0.2):
    label = Mk(markup, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    return VGroup(box, label.move_to(box))


def swap(scene, old, new, rt=0.35):
    """Replace one caption by another without overlap."""
    if old is None:
        return scene.play(FadeIn(new, shift=UP * 0.1), run_time=rt)
    return scene.play(AnimationGroup(FadeOut(old), FadeIn(new, shift=UP * 0.1), lag_ratio=1.0), run_time=rt)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Light reactions"
    TITLE = "From light to ATP and NADPH"


# ---------------------------------------------------------------------------------------------
class S01Photon(SpokenScene):
    """Three panels: absorption, relaxation (heat / fluorescence), reaction-center charge separation."""

    def construct(self):
        head = T("The fate of one photon", 36, font=TITLE_FONT).move_to(P(0, 3.35))
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.7)
        cx = [-4.2, 0.0, 4.2]
        frames = [RoundedRectangle(corner_radius=0.2, width=3.95, height=5.1, stroke_color=GREY, stroke_width=2,
                                   stroke_opacity=0.5).move_to(P(c, 0.35)) for c in cx]
        self.at("in three panels")
        self.play(LaggedStart(*[Create(f) for f in frames], lag_ratio=0.25), run_time=1.2)

        ttl = [T("1  Absorption", 28, weight=BOLD), T("2  Relaxation", 28, weight=BOLD),
               T("3  Reaction center", 28, weight=BOLD)]
        for t, c in zip(ttl, cx):
            t.move_to(P(c, 2.45))

        def levels(c):
            ex = Line(P(c - 1.2, 1.0), P(c + 1.2, 1.0), color=GREY, stroke_width=4)
            gr = Line(P(c - 1.2, -1.2), P(c + 1.2, -1.2), color=GREY, stroke_width=4)
            return ex, gr

        # ---- panel 1: absorption -----------------------------------------------------------
        self.at("First absorption")
        ex1, gr1 = levels(cx[0])
        lab_ex = T("excited state", 24, GREY).move_to(P(cx[0], 1.58))
        lab_gr = T("ground state", 24, GREY).move_to(P(cx[0], -1.6))
        e1 = edot(P(cx[0], -1.07))
        self.play(FadeIn(ttl[0]), Create(ex1), Create(gr1), FadeIn(lab_ex), FadeIn(lab_gr), FadeIn(e1), run_time=0.9)

        self.at("Only a photon with the right energy")
        wrong = wave(P(cx[0] - 1.55, -0.1), P(cx[0] - 0.2, -0.95), color=GREY, amp=0.09, cycles=2, width=3)
        wl = T("wrong energy", 24, GREY).move_to(P(cx[0] - 0.45, 0.45))
        self.play(Create(wrong), FadeIn(wl), run_time=0.6)
        self.play(FadeOut(wrong, shift=RIGHT * 0.6), FadeOut(wl), run_time=0.5)
        right = wave(P(cx[0] - 1.55, -0.1), P(cx[0] - 0.2, -0.95), color=YELLOW, amp=0.11, cycles=5, width=4.5)
        pl = T("photon", 24, YELLOW).move_to(P(cx[0] - 0.95, 0.3))
        self.play(Create(right), FadeIn(pl), run_time=0.7)
        self.at("can promote an electron")
        up = Arrow(P(cx[0], -1.0), P(cx[0], 0.9), buff=0, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.2)
        self.play(FadeOut(right), FadeOut(pl), GrowArrow(up), e1.animate.move_to(P(cx[0], 1.13)), run_time=0.9)
        self.play(FadeOut(up), run_time=0.3)
        self.at("to an excited state")
        self.play(Indicate(lab_ex, color=YELLOW, scale_factor=1.12), run_time=0.7)

        # ---- panel 2: relaxation ------------------------------------------------------------
        self.at("Second")
        ex2, gr2 = levels(cx[1])
        e2 = edot(P(cx[1], 1.13))
        self.play(FadeIn(ttl[1]), TransformFromCopy(ex1, ex2), TransformFromCopy(gr1, gr2),
                  TransformFromCopy(e1, e2), run_time=1.0)
        self.at("not captured quickly enough")
        q = T("not captured in time?", 24, GREY).move_to(P(cx[1], 0.0))
        self.play(FadeIn(q), run_time=0.5)
        self.at("simply relaxes")
        self.play(FadeOut(q), e2.animate.move_to(P(cx[1], -1.07)), run_time=1.4, rate_func=smooth)
        self.at("heat or fluorescence")
        a_heat = Arrow(P(cx[1] - 0.6, 0.9), P(cx[1] - 0.6, -1.0), buff=0, color=ORANGE, stroke_width=6,
                       max_tip_length_to_length_ratio=0.15)
        l_heat = T("heat", 24, ORANGE).move_to(P(cx[1] - 0.85, -1.6))
        self.play(GrowArrow(a_heat), FadeIn(l_heat), run_time=0.6)
        w_fl = wave(P(cx[1] + 0.6, 0.9), P(cx[1] + 0.6, -1.0), color=YELLOW, amp=0.1, cycles=4, width=4.5)
        l_fl = T("fluorescence", 24, YELLOW).move_to(P(cx[1] + 0.85, -1.6))
        self.play(Create(w_fl), FadeIn(l_fl), run_time=0.8)
        self.at("the opportunity is lost")
        lost = T("energy lost", 28, RED if False else GREY, weight=BOLD).move_to(P(cx[1], 1.55))
        self.play(FadeIn(lost), run_time=0.5)

        # ---- panel 3: reaction center -------------------------------------------------------
        self.at("Third")
        p2 = VGroup(ex2, gr2, e2, a_heat, l_heat, w_fl, l_fl, lost)
        p1 = VGroup(ex1, gr1, e1, lab_ex, lab_gr)
        self.play(FadeIn(ttl[2]), p1.animate.set_opacity(0.3), p2.animate.set_opacity(0.3),
                  ttl[0].animate.set_opacity(0.4), ttl[1].animate.set_opacity(0.4), run_time=0.7)
        self.at("the productive route")
        pig = chip("excited pigment", YELLOW, size=22).move_to(P(cx[2], 1.3))
        acc = chip("primary acceptor", GREY, size=22).move_to(P(cx[2], -0.5))
        g = glow(pig.get_center(), YELLOW, r=0.75, op=0.12)
        e3 = edot(pig.get_right() + RIGHT * 0.3)
        self.play(FadeIn(pig), FadeIn(g), FadeIn(acc), FadeIn(e3), run_time=0.9)
        self.at("hands its electron")
        start, end = e3.get_center(), acc.get_right() + RIGHT * 0.3
        arc = ArcBetweenPoints(start, end, angle=-PI / 3)
        self.play(MoveAlongPath(e3, arc), run_time=1.3)
        self.at("creating charge separation")
        plus = sign("+", pig.get_left() + LEFT * 0.3, TEXT)
        minus = sign("−", acc.get_left() + LEFT * 0.3, BLUE)
        cs = T("charge separation", 26, TEXT, weight=BOLD).move_to(P(cx[2], -1.6))
        self.play(FadeOut(g), FadeIn(plus), FadeIn(minus), FadeIn(cs), run_time=0.8)
        self.at("That moment where an electron physically moves")
        take = T("an electron physically moves, not just energy", 30, BLUE, weight=BOLD).move_to(P(0, -3.15))
        self.play(FadeIn(take, shift=UP * 0.1), Indicate(e3, color=BLUE, scale_factor=2.2), run_time=0.9)
        self.at("where photosynthesis truly begins")
        box = SurroundingRectangle(frames[2], color=GOLD, buff=0.05, stroke_width=4)
        self.play(Create(box), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Funnel(SpokenScene):
    """Antenna: energy hops between pigments, electrons stay put. Reaction center: an electron moves."""

    def construct(self):
        head = T("Two jobs: harvest the light, then do the chemistry", 32, font=TITLE_FONT).move_to(P(0, 3.55))
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.8)
        hl = T("Antenna", 30, weight=BOLD).move_to(P(-3.55, 2.9))
        hl2 = T("energy transfer", 24, YELLOW).next_to(hl, DOWN, buff=0.08)
        hr = T("Reaction center", 30, weight=BOLD).move_to(P(3.7, 2.9))
        hr2 = T("electron transfer", 24, BLUE).next_to(hr, DOWN, buff=0.08)
        self.at("this funnel")
        pts = [P(-6.0, 1.85), P(-0.95, 0.5), P(-0.95, -0.5), P(-6.0, -1.85)]
        funnel = Polygon(*pts, stroke_color=GREY, stroke_width=3, fill_color=YELLOW, fill_opacity=0.05)
        self.play(Create(funnel), run_time=0.9)
        self.at("On the left")
        self.play(FadeIn(hl), FadeIn(hl2), run_time=0.5)

        # pigments on a grid inside the funnel
        grid = []
        for x in np.arange(-5.65, -1.25, 0.66):
            h = 0.5 + (x + 0.95) * (-1.35 / 5.05)  # half-height of funnel at x
            for y in np.arange(-2.0, 2.01, 0.58):
                if abs(y) <= h - 0.26:
                    grid.append(P(x, y))
        pigs, dots = [], []
        for p in grid:
            c = Circle(radius=0.2, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.14).move_to(p)
            pigs.append(c)
            dots.append(Dot(p, radius=0.055, color=BLUE))
        order = np.argsort([p[0] + 0.3 * np.random.RandomState(1).rand() for p in grid])
        self.at("in the antenna system")
        self.play(LaggedStart(*[FadeIn(pigs[i]) for i in range(len(pigs))], lag_ratio=0.02),
                  LaggedStart(*[FadeIn(dots[i]) for i in range(len(dots))], lag_ratio=0.02), run_time=1.8)
        self.at("two to three hundred pigments")
        cap_l = T("200–300 pigments", 26, TEXT).move_to(P(-3.55, -2.65))
        self.play(FadeIn(cap_l, shift=UP * 0.1), run_time=0.5)

        def near(x, y):
            return int(np.argmin([np.hypot(p[0] - x, p[1] - y) for p in grid]))

        path = [near(-5.65, 1.1), near(-4.95, 0.6), near(-4.3, 0.55), near(-3.65, 0.3), near(-3.0, 0.2),
                near(-2.35, 0.1), near(-1.7, 0.0)]
        self.at("pass excitation energy")
        pk = glow(grid[path[0]], YELLOW, r=0.3, op=0.45)
        pk_core = Dot(grid[path[0]], radius=0.11, color=YELLOW)
        packet = VGroup(pk, pk_core)
        self.play(FadeIn(packet, scale=0.5), pigs[path[0]].animate.set_fill(YELLOW, 0.55), run_time=0.5)

        def hop(i, rt=0.55):
            prev = pigs[path[i - 1]]
            nxt = pigs[path[i]]
            return self.play(packet.animate.move_to(grid[path[i]]), prev.animate.set_fill(GREY, 0.14),
                             nxt.animate.set_fill(YELLOW, 0.55), run_time=rt)

        self.at("from donor to acceptor")
        hop(1)
        self.at("by resonance transfer")
        cap2 = T("resonance transfer", 26, YELLOW).move_to(P(-3.55, -2.65))
        swap(self, cap_l, cap2)
        hop(2)
        self.at("The energy hops")
        hop(3)
        hop(4)
        self.at("electrons themselves stay put")
        rings = [Indicate(dots[path[i]], color=BLUE, scale_factor=2.6) for i in range(1, 5)]
        cap3 = T("energy hops, electrons stay put", 26, TEXT).move_to(P(-3.55, -2.65))
        self.play(*rings, AnimationGroup(FadeOut(cap2), FadeIn(cap3), lag_ratio=1.0), run_time=1.2)
        self.at("efficiency falls off steeply")
        a, b = grid[path[2]], grid[path[3]]
        dbl = DoubleArrow(a + DOWN * 0.38, b + DOWN * 0.38, buff=0, color=TEXT, stroke_width=3, tip_length=0.13)
        lr = T("R", 24, TEXT).next_to(dbl, DOWN, buff=0.05)
        cap4 = M("efficiency ∝ 1/R⁶", 26, TEXT).move_to(P(-3.55, -2.65))
        self.play(Create(dbl), FadeIn(lr), AnimationGroup(FadeOut(cap3), FadeIn(cap4), lag_ratio=1.0), run_time=0.8)

        # ---- the funnel feeds one reaction center -------------------------------------------
        self.at("All of that captured energy")
        self.play(FadeOut(dbl), FadeOut(lr), FadeOut(cap4), run_time=0.4)
        for i in range(5, 7):
            hop(i, rt=0.45)
        extra = [glow(grid[near(-5.0, y)], YELLOW, r=0.3, op=0.4) for y in (-1.0, 0.0, 1.0, -0.4)]
        self.at("funneled into a single reaction center")
        self.play(*[FadeIn(g_, scale=0.5) for g_ in extra], run_time=0.3)
        self.play(*[g_.animate.move_to(P(-1.3, 0.0)) for g_ in extra], run_time=1.5, rate_func=smooth)
        self.at("on the right")
        sp = chip("special pair", YELLOW, size=26).move_to(P(2.3, -0.1))
        acc = chip("acceptor", GREY, size=26).move_to(P(5.25, -0.1))
        divider = DashedLine(P(0.0, 2.4), P(0.0, -2.6), color=GREY, stroke_width=2, stroke_opacity=0.5)
        self.play(FadeOut(VGroup(*extra)), FadeIn(hr), FadeIn(hr2), FadeIn(sp), FadeIn(acc), Create(divider),
                  packet.animate.move_to(sp.get_left() + LEFT * 0.3), run_time=0.7)
        self.play(packet.animate.move_to(sp.get_center()), run_time=0.3)
        self.play(FadeOut(packet), pigs[path[6]].animate.set_fill(GREY, 0.14), sp[0].animate.set_fill(YELLOW, 0.5), run_time=0.4)

        self.at("There the special pair")
        cap_r = T("P680 or P700", 26, TEXT).move_to(P(2.3, -1.1))
        self.play(FadeIn(cap_r, shift=UP * 0.1), run_time=0.5)
        self.at("finally does something different")
        self.play(Indicate(sp, color=YELLOW, scale_factor=1.12), run_time=0.8)
        self.at("It gives up an actual electron")
        e = edot(sp.get_top() + UP * 0.0 + RIGHT * 0.5 + DOWN * 0.0)
        e.move_to(sp.get_right() + LEFT * 0.35 + UP * 0.45)
        arc = ArcBetweenPoints(sp.get_top() + RIGHT * 0.3, acc.get_top() + UP * 0.3 + LEFT * 0.1, angle=-PI / 2.2)
        arrow_lbl = T("electron", 24, BLUE).next_to(arc.get_end(), LEFT, buff=0.2)
        self.play(FadeIn(e, scale=0.5), run_time=0.3)
        self.play(MoveAlongPath(e, arc), FadeIn(arrow_lbl), run_time=1.3)
        plus = sign("+", sp.get_left() + LEFT * 0.3 + UP * 0.0, TEXT)
        minus = sign("−", acc.get_bottom() + DOWN * 0.3, BLUE)
        plus.move_to(sp.get_bottom() + DOWN * 0.3 + LEFT * 0.9)
        self.play(FadeIn(plus), FadeIn(minus), sp[0].animate.set_fill(YELLOW, 0.16), FadeOut(cap_r), run_time=0.6)

        self.at("Energy transfer concentrates the harvest")
        boxl = SurroundingRectangle(funnel, color=YELLOW, buff=0.12, stroke_width=3)
        txl = T("concentrates the harvest", 26, YELLOW).move_to(P(-3.55, -2.85))
        self.play(Create(boxl), FadeIn(txl), run_time=0.8)
        self.at("Electron transfer in the reaction center")
        boxr = SurroundingRectangle(VGroup(sp, acc, plus, minus, e, arrow_lbl), color=BLUE, buff=0.2, stroke_width=3)
        txr = T("commits it to chemistry", 26, BLUE).move_to(P(3.7, -2.85))
        self.play(FadeOut(boxl), boxl.animate.set_opacity(0), Create(boxr), FadeIn(txr), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Circuit(SpokenScene):
    """The whole circuit across the thylakoid membrane: stroma above, lumen below."""

    def construct(self):
        head = T("The light reactions, end to end", 32, font=TITLE_FONT).move_to(P(0, 3.55))
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.7)
        MY = 0.3  # membrane centre line
        self.at("across the thylakoid membrane")
        mem = Rectangle(width=12.4, height=0.6, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to(P(0, MY))
        l1 = Line(P(-6.2, MY + 0.3), P(6.2, MY + 0.3), color=GREY, stroke_width=3)
        l2 = Line(P(-6.2, MY - 0.3), P(6.2, MY - 0.3), color=GREY, stroke_width=3)
        stroma = T("stroma", 26, GREY).move_to(P(-5.5, 2.95))
        lumen = T("thylakoid lumen", 26, GREY).move_to(P(-4.7, -2.55))
        self.play(FadeIn(mem), Create(l1), Create(l2), FadeIn(stroma), FadeIn(lumen), run_time=1.0)

        def cx_box(label, sub, x, w=1.7, h=1.7, color=GREY):
            back = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_width=0, fill_color=BG_FILL,
                                    fill_opacity=1).move_to(P(x, MY))
            r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=3,
                                 fill_color=color, fill_opacity=0.22).move_to(P(x, MY))
            t1 = T(label, 28, TEXT, weight=BOLD).move_to(r.get_center() + (UP * 0.2 if sub else ORIGIN))
            t2 = T(sub, 24, TEXT).move_to(r.get_center() + DOWN * 0.3)
            return VGroup(back, r, t1, t2)

        self.at("Start at the left")
        psII = cx_box("PSII", "P680", -4.7)
        self.play(FadeIn(psII, scale=0.9), run_time=0.6)
        b6f = cx_box("b6f", "", -1.5, w=1.3, h=1.7)
        psI = cx_box("PSI", "P700", 1.5)
        self.play(FadeIn(b6f, scale=0.9), FadeIn(psI, scale=0.9), run_time=0.7)

        # water splitting at PSII (lumen side)
        self.at("Water is split at photosystem II")
        w1 = water(P(-5.8, -1.1))
        self.play(FadeIn(w1, shift=RIGHT * 0.3), run_time=0.5)
        self.play(w1.animate.move_to(P(-4.7, -1.05)), run_time=0.6)
        self.at("releasing oxygen and protons")
        o2 = chip_mk("O<sub>2</sub>", PINK, 24).move_to(P(-4.7, -1.05))
        h_a = proton(P(-3.95, -1.1))
        h_b = proton(P(-3.35, -1.5))
        self.play(ReplacementTransform(w1, o2), FadeIn(h_a, scale=0.4), FadeIn(h_b, scale=0.4), run_time=0.6)
        self.play(o2.animate.move_to(P(-5.8, -1.6)).set_opacity(0.0), run_time=0.9)
        self.at("feeding electrons into the chain")
        e = edot(P(-4.25, MY - 1.1), r=0.13)
        self.play(FadeIn(e, scale=0.5), run_time=0.4)

        # light excites P680, then P700. The electron travels IN the membrane (plastoquinol) to b6f,
        # then along the lumen face (plastocyanin) to PSI, and leaves PSI on the stromal face.
        self.at("Light excites")
        ph2 = wave(P(-5.6, 2.0), P(-4.95, MY + 0.85), color=YELLOW, amp=0.1, cycles=3, width=4.5)
        self.play(Create(ph2), run_time=0.35)
        self.play(FadeOut(ph2), psII[1].animate.set_fill(YELLOW, 0.45), e.animate.move_to(P(-3.72, MY)), run_time=0.4)
        self.play(e.animate.move_to(P(-2.28, MY)), psII[1].animate.set_fill(GREY, 0.22), run_time=0.4)
        self.play(e.animate.move_to(P(-1.5, MY - 1.05)), run_time=0.3)
        self.play(e.animate.move_to(P(1.5, MY - 1.05)), run_time=0.45)
        self.at("then C")
        ph1 = wave(P(0.4, 2.0), P(1.05, MY + 0.85), color=YELLOW, amp=0.1, cycles=3, width=4.5)
        self.play(Create(ph1), run_time=0.4)
        self.play(FadeOut(ph1), psI[1].animate.set_fill(YELLOW, 0.45), e.animate.move_to(P(2.48, MY)), run_time=0.3)
        self.play(e.animate.move_to(P(1.5, MY + 1.0)), run_time=0.3)
        self.at("lifting electrons twice")
        self.play(psI[1].animate.set_fill(GREY, 0.22), Indicate(psII[2], color=YELLOW), Indicate(psI[2], color=YELLOW), run_time=0.8)

        # protons accumulate in the lumen
        self.at("As electrons flow")
        pump = Arrow(P(-1.5, MY + 1.35), P(-1.5, MY - 1.2), buff=0.0, color=RED, stroke_width=5,
                     max_tip_length_to_length_ratio=0.12)
        pump.set_z_index(-1)   # passes behind the b6f box so it never crosses the label
        self.play(GrowArrow(pump), run_time=0.8)
        hs = [proton(P(x, y)) for x, y in [(-2.6, -1.0), (-1.9, -1.3), (-1.1, -1.0), (-0.3, -1.4), (0.5, -1.0),
                                             (1.3, -1.35), (2.1, -1.0), (-2.7, -1.85), (-0.8, -1.9), (0.6, -1.85)]]
        self.at("protons accumulate inside the thylakoid lumen")
        self.play(FadeOut(pump), LaggedStart(*[FadeIn(h, scale=0.4) for h in hs], lag_ratio=0.25), run_time=2.0)
        self.at("building a concentration gradient")
        grad = T("proton gradient", 26, RED).move_to(P(-0.6, -2.55))
        self.play(FadeIn(grad), run_time=0.6)

        # NADP+ -> NADPH
        self.at("NADP plus is reduced")
        nadp = chip_mk("NADP<sup>+</sup>", PURPLE, 24).move_to(P(1.5, 2.1))
        self.play(FadeIn(nadp, shift=DOWN * 0.2), run_time=0.5)
        self.play(e.animate.move_to(nadp.get_bottom() + DOWN * 0.05), run_time=0.6)
        nadph = chip_mk("NADPH", PURPLE, 24).move_to(nadp)
        self.at("to NADPH on the stromal side")
        self.play(ReplacementTransform(nadp, nadph), FadeOut(e), run_time=0.6)
        self.play(nadph.animate.move_to(P(0.2, 2.35)), run_time=0.5)

        # ATP synthase
        self.at("Finally that proton gradient drives ATP synthase")
        syn_body = RoundedRectangle(corner_radius=0.12, width=0.9, height=1.2, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.25).move_to(P(5.0, MY))
        syn_head = RoundedRectangle(corner_radius=0.3, width=1.3, height=0.9, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.25).move_to(P(5.0, MY + 1.05))
        syn = VGroup(syn_body, syn_head)
        syn_lbl = T("ATP synthase", 24, TEXT).move_to(P(5.0, MY + 1.85))
        self.play(FadeIn(syn, scale=0.9), FadeIn(syn_lbl), run_time=0.7)
        flow = [proton(P(3.4 + 0.7 * i, -1.0 - 0.3 * i)) for i in range(2)]
        self.play(*[FadeIn(h) for h in flow], run_time=0.3)
        self.play(*[h.animate.move_to(P(5.0, MY - 0.9)) for h in flow], run_time=0.8)
        self.play(*[h.animate.move_to(P(5.0, MY + 0.3)) for h in flow], run_time=0.5)
        self.play(*[h.animate.move_to(P(5.0 + 1.2 * (1 if i else -1), MY + 1.85)).set_opacity(0.0) for i, h in enumerate(flow)], run_time=0.9)
        self.at("which makes ATP")
        adp = chip_mk("ADP + P<sub>i</sub>", GREEN, 22).move_to(P(3.0, 2.85))
        atp = chip_mk("ATP", GREEN, 24).move_to(P(5.0, 2.85))
        self.play(FadeIn(adp), run_time=0.4)
        self.play(ReplacementTransform(adp, atp), run_time=0.7)

        # summary row
        self.at("In one picture")
        self.play(FadeOut(grad), FadeOut(stroma), FadeOut(lumen), run_time=0.4)
        specs = [("light in", YELLOW), ("water split", PINK), ("protons pumped", RED), ("NADPH", PURPLE), ("ATP", GREEN)]
        chips = [chip_mk(t, c, 26) for t, c in specs]
        plus_t = T("+", 30, TEXT)
        row = VGroup(chips[0], chips[1], chips[2], chips[3], plus_t, chips[4]).arrange(RIGHT, buff=0.4).move_to(P(0, -3.25))
        arrows = [Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.06, color=GREY, stroke_width=3,
                        max_tip_length_to_length_ratio=0.5) for i in range(2)]
        arrows.append(Arrow(chips[2].get_right(), chips[3].get_left(), buff=0.06, color=GREY, stroke_width=3,
                            max_tip_length_to_length_ratio=0.5))
        self.at("light in at two photosystems")
        self.play(FadeIn(chips[0], shift=UP * 0.1), run_time=0.4)
        self.at("water split")
        self.play(FadeIn(chips[1], shift=UP * 0.1), FadeIn(arrows[0]), run_time=0.4)
        self.at("protons pumped")
        self.play(FadeIn(chips[2], shift=UP * 0.1), FadeIn(arrows[1]), run_time=0.4)
        self.at("the two energy currencies")
        self.play(FadeIn(chips[3], shift=UP * 0.1), FadeIn(arrows[2]), FadeIn(plus_t), FadeIn(chips[4], shift=UP * 0.1),
                  Indicate(nadph, color=PURPLE), Indicate(atp, color=GREEN), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Twostep(SpokenScene):
    """Schematic Z: two light-driven uphill boosts with a downhill slide between them."""

    def construct(self):
        head = T("Two photosystems, two light-driven boosts", 32, font=TITLE_FONT).move_to(P(0, 3.65))
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)
        AX = -5.55
        axis = Arrow(P(AX, -2.5), P(AX, 3.0), buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.05)
        ay = T("free energy of the electron", 24, GREY).rotate(PI / 2).move_to(P(AX - 0.4, 0.2))
        self.play(GrowArrow(axis), FadeIn(ay), run_time=0.9)

        X2, X1 = -3.3, 1.7
        G2, E2, G1, E1 = -2.0, 1.2, -0.5, 2.1
        col2 = RoundedRectangle(corner_radius=0.2, width=1.8, height=4.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.10).move_to(P(X2, (-2.3 + 1.7) / 2))
        col1 = RoundedRectangle(corner_radius=0.2, width=1.8, height=3.45, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.10).move_to(P(X1, (-0.8 + 2.65) / 2))
        l2 = T("Photosystem II", 26, TEXT, weight=BOLD).move_to(P(X2, 2.1))
        l1 = T("Photosystem I", 26, TEXT, weight=BOLD).move_to(P(X1, 2.98))
        self.at("choreographed two step")
        self.play(FadeIn(col2), FadeIn(col1), run_time=0.7)

        # ---- Photosystem II: boost, water split ------------------------------------------
        self.at("Photosystem II leads")
        self.play(FadeIn(l2), run_time=0.4)
        e = edot(P(X2, G2), r=0.14)
        ph = wave(P(X2 - 1.5, G2 - 0.55), P(X2 - 0.15, G2 - 0.1), color=YELLOW, amp=0.1, cycles=4, width=4.5)
        up2 = Arrow(P(X2, G2 + 0.1), P(X2, E2 - 0.1), buff=0, color=YELLOW, stroke_width=10,
                    max_tip_length_to_length_ratio=0.12)
        n1 = sign("1", P(X2 - 0.5, (G2 + E2) / 2), YELLOW)
        self.play(FadeIn(e), Create(ph), run_time=0.5)
        self.play(GrowArrow(up2), e.animate.move_to(P(X2, E2)), FadeOut(ph), FadeIn(n1), run_time=1.0)

        self.at("splits water molecules")
        w1 = water(P(X2 - 1.1, -2.95))
        self.play(FadeIn(w1, shift=UP * 0.2), run_time=0.5)
        self.at("releases the oxygen we breathe")
        o2 = chip_mk("O<sub>2</sub>", PINK, 24).move_to(P(X2 + 1.0, -2.95))
        wo = CurvedArrow(w1.get_right() + RIGHT * 0.05, o2.get_left() + LEFT * 0.05, angle=-PI / 3, color=PINK, stroke_width=3)
        self.play(Create(wo), FadeIn(o2, shift=RIGHT * 0.2), run_time=0.8)

        # ---- the downhill slide ------------------------------------------------------------
        self.at("its electrons drop in energy")
        slide = Line(P(X2, E2), P(X1, G1), color=BLUE, stroke_width=4)
        self.play(Create(slide), e.animate.move_to(P(X1, G1)), run_time=1.4)
        self.at("to build a proton gradient")
        def on_line(x, dy=-0.5):
            t = (x - X2) / (X1 - X2)
            return P(x, E2 + (G1 - E2) * t + dy)
        hs = [proton(on_line(x)) for x in (-2.2, -1.3, -0.4)]
        pg = T("proton gradient", 26, RED).move_to(P(-0.55, -1.0))
        self.play(LaggedStart(*[FadeIn(h, scale=0.4) for h in hs], lag_ratio=0.3), FadeIn(pg), run_time=1.2)
        self.at("powers ATP synthesis")
        atp = chip_mk("ATP", GREEN, 26).move_to(P(-0.55, -1.9))
        ar = Arrow(pg.get_bottom() + DOWN * 0.05, atp.get_top() + UP * 0.05, buff=0, color=GREEN, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(ar), FadeIn(atp), run_time=0.8)

        # ---- Photosystem I ---------------------------------------------------------------
        self.at("Photosystem I follows")
        self.play(FadeIn(l1), run_time=0.4)
        self.at("a second hit of light")
        ph1 = wave(P(X1 + 1.6, G1 - 0.75), P(X1 + 0.15, G1 - 0.1), color=YELLOW, amp=0.1, cycles=4, width=4.5)
        self.play(Create(ph1), run_time=0.6)
        self.at("energizes the electrons")
        up1 = Arrow(P(X1, G1 + 0.1), P(X1, E1 - 0.1), buff=0, color=YELLOW, stroke_width=10,
                    max_tip_length_to_length_ratio=0.12)
        n2 = sign("2", P(X1 - 0.5, (G1 + E1) / 2), YELLOW)
        self.play(GrowArrow(up1), e.animate.move_to(P(X1, E1)), FadeOut(ph1), FadeIn(n2), run_time=1.0)
        self.at("so they can produce NADPH")
        nadph = chip_mk("NADPH", PURPLE, 26).move_to(P(5.2, 1.0))
        down2 = Line(P(X1, E1), nadph.get_left() + LEFT * 0.1, color=BLUE, stroke_width=4)
        self.play(Create(down2), e.animate.move_to(nadph.get_left() + LEFT * 0.1), FadeIn(nadph), run_time=1.0)
        self.at("the reducing power")
        rp = T("reducing power", 24, PURPLE).move_to(P(5.2, 0.35))
        self.play(FadeIn(rp), FadeOut(e), run_time=0.5)
        self.at("enables sugar production")
        sg = T("to sugar", 26, TEXT).move_to(P(5.2, -0.4))
        sa = Arrow(rp.get_bottom() + DOWN * 0.05, sg.get_top() + UP * 0.05, buff=0, color=GREY, stroke_width=3,
                   max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(sa), FadeIn(sg), run_time=0.6)

        # ---- the summary -------------------------------------------------------------------
        self.at("two uphill jumps")
        self.play(Indicate(up2, color=YELLOW, scale_factor=1.15), Indicate(up1, color=YELLOW, scale_factor=1.15),
                  Indicate(n1), Indicate(n2), run_time=1.2)
        self.at("downhill slide between them")
        self.play(slide.animate.set_stroke(width=9), *[Indicate(h, color=RED) for h in hs], run_time=1.2)
        self.play(slide.animate.set_stroke(width=4), run_time=0.3)
        self.at("one to make ATP")
        c1 = chip_mk("boost 1 → ATP", GREEN, 26).move_to(P(0.2, -3.1))
        self.play(FadeIn(c1, shift=UP * 0.1), Indicate(atp, color=GREEN), run_time=0.8)
        self.at("one to make NADPH")
        c2 = chip_mk("boost 2 → NADPH", PURPLE, 26).move_to(P(4.1, -3.1))
        self.play(FadeIn(c2, shift=UP * 0.1), Indicate(nadph, color=PURPLE), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Psii(SpokenScene):
    """Photosystem II as a machine: 4 photons + 2 H2O in; 4 e- (on QH2), 4 H+ (lumen), O2 out."""

    def construct(self):
        head = T("What Photosystem II accomplishes", 34, font=TITLE_FONT).move_to(P(0, 3.55))
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.7)
        self.at("one balanced statement")
        band = Rectangle(width=12.6, height=0.9, stroke_width=0, fill_color=GREY, fill_opacity=0.25).move_to(P(0, 0.05))
        bl1 = Line(P(-6.3, 0.5), P(6.3, 0.5), color=GREY, stroke_width=3)
        bl2 = Line(P(-6.3, -0.4), P(6.3, -0.4), color=GREY, stroke_width=3)
        back = RoundedRectangle(corner_radius=0.2, width=3.2, height=3.0, stroke_width=0, fill_color=BG_FILL,
                                fill_opacity=1).move_to(P(0, 0.05))
        box = RoundedRectangle(corner_radius=0.2, width=3.2, height=3.0, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.22).move_to(P(0, 0.05))
        bt = T("Photosystem II", 26, TEXT, weight=BOLD).move_to(P(0, 1.0))
        st = T("stroma", 24, GREY).move_to(P(-2.5, 1.2))
        lt = T("lumen", 24, GREY).move_to(P(-2.5, -1.0))
        self.play(FadeIn(band), Create(bl1), Create(bl2), FadeIn(back), FadeIn(box), FadeIn(bt), FadeIn(st), FadeIn(lt),
                  run_time=1.0)

        # inputs
        self.at("Inputs on the left")
        inp = T("inputs", 26, GREY).move_to(P(-4.75, 2.95))
        self.play(FadeIn(inp), run_time=0.4)
        self.at("four photons of light")
        waves = [wave(P(-5.8, 2.45 - 0.3 * i), P(-3.7, 2.45 - 0.3 * i), color=YELLOW, amp=0.07, cycles=5, width=3.5)
                 for i in range(4)]
        lp = Mk("4 photons", 26, YELLOW).move_to(P(-4.75, 1.05))
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2), FadeIn(lp), run_time=1.0)
        self.at("and two molecules of water")
        wch = chip_mk("2 H<sub>2</sub>O", PINK, 28).move_to(P(-4.75, -1.0))
        self.play(FadeIn(wch, shift=UP * 0.2), run_time=0.6)

        self.at("with its P680")
        p680 = chip("P680", GREEN if False else GOLD, size=26).move_to(P(0, -0.55))
        self.play(FadeIn(p680, scale=0.8), run_time=0.5)
        self.at("splits that water")
        self.play(*[w.animate.move_to(w.get_center() + RIGHT * 2.6 + DOWN * 0.7).set_opacity(0.0) for w in waves],
                  lp.animate.set_opacity(0.0), wch.animate.move_to(P(-0.8, -1.1)).scale(0.8), run_time=0.9)
        self.play(FadeOut(wch, scale=0.6), box.animate.set_fill(YELLOW, 0.4), run_time=0.4)
        self.play(box.animate.set_fill(GREY, 0.22), run_time=0.4)

        # outputs
        self.at("The outputs on the right")
        out = T("outputs", 26, GREY).move_to(P(4.3, 2.95))
        self.play(FadeIn(out), run_time=0.4)
        self.at("Electrons leave on")
        # 4 e- ride on TWO plastoquinols (2 e- each), which sit in the membrane
        qh2 = chip_mk("2 QH<sub>2</sub>", BLUE, 28).move_to(P(3.4, 0.05))
        es = VGroup(*[edot(P(2.98 + 0.28 * i, 0.95), r=0.1) for i in range(4)])
        el = Mk("4 e<sup>−</sup>", 24, BLUE).next_to(es, RIGHT, buff=0.25)
        self.play(FadeIn(qh2, shift=RIGHT * 0.4), FadeIn(es), FadeIn(el), run_time=0.9)
        self.at("the QH2 carrier")
        self.play(Indicate(qh2, color=BLUE), run_time=0.8)
        self.at("headed for cytochrome b6f")
        arr = Arrow(qh2.get_right() + RIGHT * 0.1, qh2.get_right() + RIGHT * 0.8, buff=0, color=GREY, stroke_width=3,
                    max_tip_length_to_length_ratio=0.35)
        cb = T("cyt b6f", 24, TEXT).next_to(arr, RIGHT, buff=0.15)
        self.play(GrowArrow(arr), FadeIn(cb), run_time=0.7)
        self.at("Four protons are deposited in the lumen")
        hs = [proton(P(-0.6 + 0.5 * i, -1.15)) for i in range(4)]
        self.play(*[FadeIn(h, scale=0.4) for h in hs], run_time=0.4)
        self.play(*[h.animate.move_to(P(2.4 + 0.6 * i, -1.1)) for i, h in enumerate(hs)], run_time=1.2)
        hl = Mk("4 H<sup>+</sup> in the lumen", 24, RED).move_to(P(3.3, -1.8))
        self.play(FadeIn(hl), run_time=0.4)
        self.at("feeding the gradient")
        self.play(*[Indicate(h, color=RED) for h in hs], run_time=0.8)
        self.at("And oxygen gas is released")
        o2 = chip_mk("O<sub>2</sub>", PINK, 30).move_to(P(5.45, -1.1))
        self.play(FadeIn(o2, shift=RIGHT * 0.4), run_time=0.7)
        self.at("arguably the most important")
        self.play(Indicate(o2, color=PINK, scale_factor=1.25), run_time=1.2)

        # the balanced statement
        self.at("One machine")
        self.play(FadeOut(VGroup(inp, out, st, lt)), run_time=0.4)
        parts = [Mk("2 H<sub>2</sub>O", 30, PINK), T("+", 30), Mk("4 photons", 30, YELLOW), T("→", 30),
                 Mk("O<sub>2</sub>", 30, PINK), T("+", 30), Mk("4 H<sup>+</sup>", 30, RED), T("+", 30),
                 Mk("4 e<sup>−</sup>", 30, BLUE)]
        eq = VGroup(*parts).arrange(RIGHT, buff=0.3)
        fit(eq, max_w=11.8)
        eq.move_to(P(0, -3.2))
        self.at("four photons", nth=1)
        self.play(FadeIn(parts[2], shift=UP * 0.1), run_time=0.5)
        self.at("two waters")
        self.play(FadeIn(parts[0], shift=UP * 0.1), FadeIn(parts[1]), run_time=0.5)
        self.at("and the breathable atmosphere")
        self.play(FadeIn(parts[3]), FadeIn(parts[4], shift=UP * 0.1), FadeIn(parts[5]), FadeIn(parts[6]), FadeIn(parts[7]),
                  FadeIn(parts[8]), run_time=0.8)
        self.at("is a byproduct")
        self.play(Indicate(parts[4], color=PINK, scale_factor=1.3), run_time=0.9)
        self.at("charging the electron transport chain")
        self.play(Indicate(parts[8], color=BLUE, scale_factor=1.3), Indicate(parts[6], color=RED, scale_factor=1.3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06End(EndCard):
    LINE = "Light lifts electrons twice, making NADPH, ATP and oxygen."
