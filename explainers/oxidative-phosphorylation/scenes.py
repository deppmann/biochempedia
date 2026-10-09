"""Oxidative phosphorylation: electrons build a proton battery  (Biochemistrypedia explainer)

Timed to the SPOKEN words of the lesson's own slide clips (word timestamps in audio/words.json).

COLOR MAP (one color per concept, whole video)
  YELLOW = electrons (e-): the dots that move, and any carrier that is REDUCED (holds electrons)
  BLUE   = protons (H+) and the proton gradient / proton-motive force (battery charge)
  GREEN  = a proton PUMP (Complexes I, III, IV) and the electron-transport chain
  GREY   = a non-pump (Complex II), an OXIDIZED (empty) carrier, membranes, axes, secondary labels
  TEAL   = ATP synthase and ATP
  PURPLE = electron donors (NADH, FADH2)
  ORANGE = oxygen (O2), the final electron acceptor
  RED    = a block (inhibitor), a leak (uncoupler), heat: anything that stops or wastes the flow
  GOLD   = title rule and the single Nobel Prize highlight
  TEXT   = neutral labels, mobile carriers (Q, cytochrome c), equations
No molecular structures are drawn: labelled blocks, dots, arrows, a computed ladder, a battery.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2A154"
PURPLE = "#B58CD9"
MINUS = "−"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def P3(p):
    p = list(p)
    return np.array(p + [0.0] * (3 - len(p)), dtype=float)


def arr(a, b, color=GREY, w=5, tip=0.2, buff=0.0):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), color=color, stroke_width=w,
                 buff=buff, tip_length=tip, max_tip_length_to_length_ratio=0.45)


def edot(p, r=0.11):
    return Dot(P3(p), radius=r, color=YELLOW)


def hdot(p, r=0.11):
    return Dot(P3(p), radius=r, color=BLUE)


def mv(mob, p, t=0.5, rf=smooth):
    return mob.animate(run_time=t, rate_func=rf).move_to(P3(p))


def seq(mob, pts, t=0.5):
    return Succession(*[mv(mob, p, t) for p in pts])


def hop(a, b, up=0.35):
    """Path for an electron hopping from a to b (a little arc)."""
    return ArcBetweenPoints(P3(a), P3(b), angle=-PI / 2.2)


def box(w, h, color, op=0.28, r=0.14, sw=3):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op)


def block(label, color, w, h, size=34, op=0.28):
    b = box(w, h, color, op)
    return VGroup(b, T(label, size, color, weight=BOLD).move_to(b))


def left_at(m, x, y):
    return m.move_to([x + m.width / 2, y, 0])


def xmark(center, size=0.16, color=RED, w=6):
    c = np.array(center, dtype=float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def block_mark(center, r=0.25):
    c = Circle(radius=r, stroke_color=RED, stroke_width=5, fill_color=BG, fill_opacity=1)
    d = Line(c.get_center() + np.array([-0.7 * r, -0.7 * r, 0]), c.get_center() + np.array([0.7 * r, 0.7 * r, 0]),
             color=RED, stroke_width=5)
    return VGroup(c, d).move_to(np.array(center, dtype=float))


def legend_hpe(x=5.2, y=3.25):
    g = VGroup(hdot([0, 0, 0]), T("H⁺", 26, BLUE), edot([0, 0, 0]), T("e⁻", 26, YELLOW))
    g[1].next_to(g[0], RIGHT, buff=0.12)
    g[2].next_to(g[1], RIGHT, buff=0.4)
    g[3].next_to(g[2], RIGHT, buff=0.12)
    return g.move_to([x, y, 0])


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Oxidative phosphorylation"
    TITLE = "Electrons build a proton battery"


class S06End(EndCard):
    LINE = "Electrons charge the gradient; ATP synthase spends it."


# =============================================================================================
class S01Chemiosmosis(SpokenScene):
    """Two machines, one link: the proton gradient. Mitchell 1961."""

    def construct(self):
        MY = -0.1
        memb = Rectangle(width=12.4, height=0.9, stroke_width=0, fill_color=GREY, fill_opacity=0.24).move_to([0, MY, 0])
        lab_ims = T("intermembrane\nspace", 24, GREY).move_to([-4.85, 1.75, 0])
        lab_mem = T("inner\nmembrane", 24, GREY).move_to([-4.85, MY, 0])
        lab_mat = T("matrix", 24, GREY).move_to([-4.85, -1.7, 0])

        xs = (-2.4, -0.8, 0.8)
        blocks = VGroup(*[box(1.0, 1.6, GREEN).move_to([x, MY, 0]) for x in xs])
        stalk = box(1.0, 1.3, TEAL).move_to([3.5, MY, 0])
        knob = Ellipse(width=1.7, height=1.4, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                       fill_opacity=0.28).move_to([3.5, -1.4, 0])
        synth = VGroup(stalk, knob)
        synth_lab = T("ATP synthase", 26, TEAL).move_to([3.5, -2.55, 0])

        # ---- the scaffold ---------------------------------------------------------------------
        self.at("single most important idea")
        self.play(FadeIn(memb), FadeIn(lab_ims), FadeIn(lab_mem), FadeIn(lab_mat), run_time=1.0)

        self.at("Electron flow")
        lbl_e = T("electron flow", 30, YELLOW).move_to([-0.8, 1.45, 0])
        self.play(FadeIn(blocks, lag_ratio=0.25), FadeIn(lbl_e, shift=UP * 0.1), run_time=0.9)
        self.at("ATP synthesis")
        lbl_a = T("ATP synthesis", 30, TEAL).move_to([3.5, 1.45, 0])
        self.play(FadeIn(synth), FadeIn(synth_lab), FadeIn(lbl_a, shift=UP * 0.1), run_time=0.9)

        self.at("linked only by")
        conn = DoubleArrow([-0.5, 2.35, 0], [3.1, 2.35, 0], color=BLUE, stroke_width=6, buff=0, tip_length=0.2)
        conn_l = T("proton gradient", 30, BLUE).move_to([1.55, 2.85, 0])
        self.play(GrowFromCenter(conn), FadeIn(conn_l, shift=UP * 0.1), run_time=0.9)

        # ---- left machine: electrons hop, protons are pushed up -------------------------------
        self.at("On the left")
        self.play(FadeOut(conn), FadeOut(conn_l), FadeOut(lbl_a), FadeOut(lbl_e), run_time=0.6)

        self.at("electrons hop downhill")
        pts = [(-3.4, MY), (-2.4, MY), (-0.8, MY), (0.8, MY), (1.9, MY)]
        dots = [edot(pts[0]) for _ in range(3)]
        self.add(*dots)
        anims = []
        for k, d in enumerate(dots):
            segs = [MoveAlongPath(d, hop(pts[i], pts[i + 1]), run_time=0.55, rate_func=smooth) for i in range(4)]
            anims.append(Succession(Wait(0.55 * k * 1.3), *segs, FadeOut(d, run_time=0.25)))
        self.play(AnimationGroup(*anims), run_time=3.4)

        self.at("pushing protons")
        src = VGroup(*[hdot([x + dx, yy, 0]) for x in xs for dx in (-0.28, 0.28) for yy in (-1.25, -1.6)])
        self.play(FadeIn(src), run_time=0.5)
        self.at("out into the")
        tops = [(x + dx, yy) for x in xs for dx in (-0.28, 0.28) for yy in (0.95, 1.5)]
        self.play(LaggedStart(*[mv(d, p, 1.1) for d, p in zip(src, tops)], lag_ratio=0.12), run_time=2.4)

        self.at("That accumulation of protons")
        many = T("many H⁺", 30, BLUE).move_to([-0.8, 2.3, 0])
        few = T("few H⁺", 28, GREY).move_to([-0.8, -2.15, 0])
        self.play(FadeIn(many, shift=DOWN * 0.1), FadeIn(few, shift=UP * 0.1), run_time=0.7)
        self.at("potential energy")
        pe = T("stored as potential energy", 30, TEXT, weight=BOLD).move_to([-0.8, 3.0, 0])
        self.play(FadeIn(pe, shift=UP * 0.1), run_time=0.8)
        self.at("like water behind a dam")
        water = Rectangle(width=12.4, height=2.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.16)
        water.move_to([0, 0.35 + 1.1, 0])
        dam_l = T("like water behind a dam", 30, BLUE).move_to([-0.8, 3.0, 0])
        self.play(FadeIn(water), Transform(pe, dam_l), run_time=1.0)

        # ---- right machine: protons flood back down through ATP synthase -----------------------
        self.at("On the right")
        self.play(Indicate(synth, color=TEAL, scale_factor=1.06), run_time=0.9)
        flood = VGroup(*[hdot(p) for p in [(3.0, 1.0), (4.0, 1.0), (3.25, 1.55), (3.75, 1.55), (3.5, 2.05)]])
        self.play(FadeIn(flood), run_time=0.4)
        self.at("flood back down")
        anims = []
        for k, d in enumerate(flood):
            x0 = d.get_center()[0]
            anims.append(Succession(mv(d, [3.5, 0.4, 0], 0.45), mv(d, [3.5, -1.0, 0], 0.5),
                                    mv(d, [3.5 + (k - 2) * 0.28, -2.05, 0], 0.5), FadeOut(d, run_time=0.2)))
        self.play(LaggedStart(*anims, lag_ratio=0.22), run_time=2.4)

        self.at("phosphorylation of ADP")
        adp = chip("ADP", GREY, 26).move_to([1.45, -1.4, 0])
        atp = chip("ATP", TEAL, 26).move_to([5.5, -1.4, 0])
        a_in = arr([2.1, -1.4, 0], [2.6, -1.4, 0], GREY, 4, 0.16)
        a_out = arr([4.4, -1.4, 0], [4.95, -1.4, 0], TEAL, 4, 0.16)
        self.play(FadeIn(adp), GrowArrow(a_in), run_time=0.4)
        self.play(GrowArrow(a_out), TransformFromCopy(adp, atp), Flash(atp, color=TEAL, flash_radius=0.7, line_length=0.18),
                  run_time=0.8)

        # ---- the man who proposed it -------------------------------------------------------------
        self.at("Peter Mitchell", lead=0.7)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        name = T("Peter Mitchell", 46, font=TITLE_FONT).move_to([0, 2.5, 0])
        line = Line([-4.6, 0, 0], [4.6, 0, 0], color=GREY, stroke_width=5)
        self.play(Write(name), Create(line), run_time=0.8)
        self.at("proposed this in")
        d61 = Dot([-3.6, 0, 0], radius=0.16, color=BLUE)
        y61 = M("1961", 34, TEXT).move_to([-3.6, 0.65, 0])
        t61 = T("proposes\nchemiosmosis", 28, BLUE).move_to([-3.6, -1.0, 0])
        self.play(FadeIn(d61, scale=0.4), FadeIn(y61), FadeIn(t61, shift=UP * 0.1), run_time=0.9)
        self.at("met with deep")
        sk = T("deep skepticism", 28, GREY).move_to([0, 0.65, 0])
        self.play(FadeIn(sk, shift=UP * 0.1), run_time=0.8)
        self.at("won the Nobel")
        d78 = Dot([3.6, 0, 0], radius=0.16, color=GOLD)
        y78 = M("1978", 34, TEXT).move_to([3.6, 0.65, 0])
        t78 = T("Nobel Prize\nin Chemistry", 28, GOLD).move_to([3.6, -1.0, 0])
        self.play(FadeIn(d78, scale=0.4), FadeIn(y78), FadeIn(t78, shift=UP * 0.1), run_time=0.9)
        self.play(Flash(d78, color=GOLD, flash_radius=0.6, line_length=0.15), run_time=0.7)
        self.finish()


# =============================================================================================
def Y(E):
    """Reduction potential (V) -> y on screen; NEGATIVE at the top, as on the lesson slide."""
    return 2.5 - (E + 0.4) * (5.4 / 1.4)


class S02Redox(SpokenScene):
    """Electrons fall from low reduction potential (NADH) to high (O2): a 1.14 V drop."""

    def construct(self):
        AX = -4.6
        axis = Line([AX, Y(-0.4) + 0.1, 0], [AX, Y(1.0) - 0.1, 0], color=GREY, stroke_width=4)
        ticks = VGroup()
        labs = VGroup()
        for E in (-0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
            ticks.add(Line([AX - 0.08, Y(E), 0], [AX + 0.08, Y(E), 0], color=GREY, stroke_width=3))
            s = ("0.0" if E == 0 else (f"+{E:.1f}" if E > 0 else MINUS + f"{abs(E):.1f}"))
            labs.add(M(s, 24, GREY).next_to([AX - 0.12, Y(E), 0], LEFT, buff=0.08))
        ytitle = T("Reduction potential  E°′ (V)", 26, GREY).rotate(PI / 2).move_to([-6.0, -0.2, 0])

        self.at("Every carrier has a reduction potential")
        self.play(Create(axis), FadeIn(ticks), run_time=1.2)
        self.at("plotted here on the vertical axis")
        self.play(FadeIn(labs, lag_ratio=0.08), FadeIn(ytitle), run_time=1.4)

        # ---- NADH at the top ------------------------------------------------------------------
        self.at("NADH sits high")
        nadh = chip("NADH", PURPLE, 28).move_to([-3.3, Y(-0.32), 0])
        nv = M(MINUS + "0.32 V", 26, TEXT).next_to(nadh, RIGHT, buff=0.3)
        g_n = DashedLine([AX, Y(-0.32), 0], nadh.get_left(), color=GREY, dash_length=0.1, stroke_width=3)
        self.play(FadeIn(nadh, shift=RIGHT * 0.2), Create(g_n), FadeIn(nv), run_time=1.0)
        self.at("holds electrons loosely")
        # NADH donates a PAIR of electrons (as a hydride): two dots, not three
        edots = VGroup(*[edot([0, 0, 0]) for _ in range(2)])
        edots.arrange(RIGHT, buff=0.22).move_to(nadh.get_top() + UP * 0.32)
        self.play(FadeIn(edots), run_time=0.5)
        self.play(*[d.animate(rate_func=there_and_back, run_time=0.8).shift(UP * 0.18 * (1 + 0.3 * i))
                    for i, d in enumerate(edots)])
        self.at("donates them readily")
        self.play(*[d.animate.shift(RIGHT * 0.5 + DOWN * 0.1 * i) for i, d in enumerate(edots)], run_time=0.8)

        # ---- O2 at the bottom -------------------------------------------------------------------
        self.at("Oxygen sits at the bottom")
        o2 = chip("O₂", ORANGE, 28).move_to([-3.3, Y(0.82), 0])
        ov = M("+0.82 V", 26, TEXT).next_to(o2, RIGHT, buff=0.3)
        g_o = DashedLine([AX, Y(0.82), 0], o2.get_left(), color=GREY, dash_length=0.1, stroke_width=3)
        self.play(FadeIn(o2, shift=LEFT * 0.2), Create(g_o), FadeIn(ov), run_time=1.0)
        self.at("grabs electrons hungrily")
        self.play(Indicate(o2, color=ORANGE, scale_factor=1.25), run_time=1.3)

        # ---- the flow: low to high ----------------------------------------------------------------
        self.at("Electrons always flow")
        flow = arr([0.0, 2.0, 0], [0.0, -1.95, 0], YELLOW, 8, 0.28)
        flow_l = T("e⁻ flow", 28, YELLOW).next_to(flow, RIGHT, buff=0.25)
        self.play(GrowArrow(flow), FadeIn(flow_l), FadeOut(edots), run_time=1.0)
        self.at("generous donor")
        gd = T("generous donor", 26, PURPLE).move_to([-2.9, Y(-0.32) + 0.72, 0])
        self.play(FadeIn(gd, shift=DOWN * 0.1), run_time=0.7)
        self.at("greedy acceptor")
        ga = T("greedy acceptor", 26, ORANGE).move_to([-2.9, Y(0.82) + 0.72, 0])
        self.play(FadeIn(ga, shift=UP * 0.1), run_time=0.7)

        # ---- cascade: the straight arrow becomes steps ---------------------------------------------
        self.at("cascade")
        levels = [-0.32, 0.04, 0.25, 0.82]
        x0 = -0.2
        pts = []
        for i, E in enumerate(levels):
            pts += [np.array([x0 + 0.5 * i, Y(E), 0]), np.array([x0 + 0.5 * (i + 1), Y(E), 0])]
        stair = VMobject(stroke_color=TEXT, stroke_width=6)
        stair.set_points_as_corners(pts)
        q_l = T("Q", 26, TEXT).next_to(np.array([x0 + 0.5, Y(0.04), 0]), LEFT, buff=0.12)
        c_l = T("cyt c", 26, TEXT).next_to(np.array([x0 + 1.0, Y(0.25), 0]), LEFT, buff=0.12)
        self.play(FadeOut(flow), FadeOut(flow_l), Create(stair), FadeIn(q_l), FadeIn(c_l), run_time=1.1)
        ball = edot(pts[0] + np.array([0.15, 0, 0]), 0.13)
        self.add(ball)
        self.play(seq(ball, [pts[1] + [0.0, 0, 0], pts[2] + [0.0, 0, 0], pts[3], pts[4], pts[5], pts[6], pts[7]], 0.24),
                  run_time=1.7)

        # ---- the numbers ---------------------------------------------------------------------------
        self.at("The total drop is about")
        gx = 2.3
        g1 = DashedLine([x0 + 0.5, Y(-0.32), 0], [gx, Y(-0.32), 0], color=GREY, dash_length=0.1, stroke_width=3)
        g2 = DashedLine([x0 + 0.5 * 4, Y(0.82), 0], [gx, Y(0.82), 0], color=GREY, dash_length=0.1, stroke_width=3)
        br = DoubleArrow([gx, Y(-0.32), 0], [gx, Y(0.82), 0], color=YELLOW, stroke_width=6, buff=0, tip_length=0.22)
        dE = M("ΔE°′ = 1.14 V", 26, TEXT, weight=BOLD)
        left_at(dE, 2.65, 1.55)
        self.play(Create(g1), Create(g2), GrowFromCenter(br), FadeIn(dE, shift=LEFT * 0.1), run_time=1.3)
        self.at("roughly minus")
        e1 = M("ΔG°′ = " + MINUS + "n F ΔE°′", 24, TEXT)
        left_at(e1, 2.65, 0.7)
        e2 = M("= " + MINUS + "2 × 96.5 × 1.14", 24, TEXT)
        left_at(e2, 2.65, 0.05)
        e3 = M("≈ " + MINUS + "220 kJ/mol", 30, YELLOW, weight=BOLD)
        left_at(e3, 2.65, -0.7)
        self.play(FadeIn(e1, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(e2, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(e3, shift=UP * 0.1), run_time=0.7)

        self.at("pumping protons")
        mem = Rectangle(width=3.2, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to([4.7, -2.62, 0])
        a_dn = arr([4.7, -1.05, 0], [4.7, -1.8, 0], YELLOW, 5, 0.18)
        self.play(FadeIn(mem), GrowArrow(a_dn), run_time=0.7)
        hs = VGroup(*[hdot([3.9 + 0.55 * i, -2.95, 0]) for i in range(4)])
        pl = T("pumps H⁺ across", 26, BLUE).move_to([4.7, -3.3, 0])
        self.add(hs)
        self.play(FadeIn(pl), LaggedStart(*[mv(d, [d.get_center()[0], -2.3, 0], 1.2) for d in hs], lag_ratio=0.2),
                  run_time=1.8)
        self.finish()


# =============================================================================================
class S03Pumps(SpokenScene):
    """The chain from named parts: three pumps (I, III, IV) plus a feeder (II)."""

    def construct(self):
        chain = Group()  # everything that must fade out/in together later

        strip = Rectangle(width=5.2, height=5.75, stroke_width=0, fill_color=GREY, fill_opacity=0.18).move_to([-0.3, 0.05, 0])
        l_mat = T("matrix", 24, GREY).move_to([-4.0, 3.2, 0])
        l_ims = T("intermembrane space", 24, GREY).move_to([4.3, 3.2, 0])
        cap = [None]

        def caption(text):
            new = T(text, 28, TEXT).move_to([0.2, -3.3, 0])
            if cap[0] is None:
                self.play(FadeIn(new, shift=UP * 0.1), run_time=0.4)
            else:
                self.play(FadeOut(cap[0], shift=UP * 0.1), FadeIn(new, shift=UP * 0.1), run_time=0.4)
            cap[0] = new
            return new

        self.at("assemble the chain")
        self.play(FadeIn(strip), FadeIn(l_mat), FadeIn(l_ims), run_time=0.9)
        chain.add(strip, l_mat, l_ims)

        YI, YQ, YIII, YIV, YII, YCC = 2.4, 1.2, 0.0, -2.1, 0.3, -1.05
        # ---- NADH -> complex I -> Q ------------------------------------------------------------
        self.at("Electrons from NADH enter")
        nadh = chip("NADH", PURPLE, 28).move_to([-3.9, YI, 0])
        self.play(FadeIn(nadh, shift=RIGHT * 0.2), run_time=0.7)
        chain.add(nadh)
        self.at("enter at complex")
        bI = block("I", GREEN, 2.9, 0.9).move_to([0.5, YI, 0])
        aI = arr([nadh.get_right()[0] + 0.05, YI, 0], [-0.95, YI, 0], PURPLE, 5)
        self.play(FadeIn(bI, scale=0.8), GrowArrow(aI), run_time=0.8)
        chain.add(bI, aI)
        self.at("NADH Q")
        c1 = caption("Complex I:  NADH-Q oxidoreductase")
        self.at("handed to ubiquinone")
        q = chip("Q", TEXT, 28).move_to([0.5, YQ, 0])
        aQ = arr([0.5, YI - 0.45, 0], [0.5, YQ + 0.35, 0], YELLOW, 5, 0.18)
        e = edot([-3.0, YI, 0], 0.13)
        self.add(e)
        self.play(FadeIn(q), GrowArrow(aQ), seq(e, [(0.5, YI, 0), (0.5, YQ + 0.0, 0)], 0.5), run_time=1.0)
        self.play(FadeOut(e), run_time=0.2)
        chain.add(q, aQ)
        caption("Ubiquinone (Q), a mobile carrier")

        # ---- complex III -> cytochrome c ----------------------------------------------------------
        self.at("Complex III")
        bIII = block("III", GREEN, 2.9, 0.9).move_to([0.5, YIII, 0])
        aIII = arr([0.5, YQ - 0.35, 0], [0.5, YIII + 0.45, 0], YELLOW, 5, 0.18)
        self.play(FadeIn(bIII, scale=0.8), GrowArrow(aIII), run_time=0.8)
        chain.add(bIII, aIII)
        caption("Complex III:  Q-cytochrome c oxidoreductase")
        self.at("passes them to cytochrome")
        cc = chip("cyt c", TEXT, 28).move_to([3.3, YCC, 0])
        a_c1 = CurvedArrow([1.2, YIII - 0.45, 0], [2.65, YCC + 0.1, 0], color=YELLOW, angle=-TAU / 8, stroke_width=5, tip_length=0.18)
        self.play(FadeIn(cc, shift=LEFT * 0.2), Create(a_c1), run_time=0.9)
        chain.add(cc, a_c1)
        caption("Cytochrome c, a mobile carrier")

        # ---- complex IV -> oxygen ---------------------------------------------------------------
        self.at("Complex RV")
        bIV = block("IV", GREEN, 2.9, 0.9).move_to([0.5, YIV, 0])
        a_c2 = CurvedArrow([3.2, YCC - 0.35, 0], [1.7, YIV + 0.3, 0], color=YELLOW, angle=-TAU / 8, stroke_width=5, tip_length=0.18)
        self.play(FadeIn(bIV, scale=0.8), Create(a_c2), run_time=0.8)
        chain.add(bIV, a_c2)
        caption("Complex IV:  cytochrome c oxidase")
        self.at("delivers them to oxygen")
        o2 = chip("O₂", ORANGE, 28).move_to([-3.9, YIV, 0])
        aO = arr([-3.3, YIV, 0], [-0.95, YIV, 0], ORANGE, 5)
        self.play(FadeIn(o2, shift=RIGHT * 0.2), GrowArrow(aO), run_time=0.9)
        chain.add(o2, aO)

        # ---- the three pumps ----------------------------------------------------------------------
        self.at("Those three are the proton pumps")
        pumps = []
        hds = []
        for yy in (YI, YIII, YIV):
            pa = arr([2.0, yy, 0], [5.2, yy, 0], BLUE, 5)
            pumps.append(pa)
            for k in range(3):
                hds.append(hdot([2.05, yy, 0]))
        hds = VGroup(*hds)
        tag = T("pumps H⁺ out", 26, BLUE).move_to([4.5, 1.2, 0])
        self.play(*[GrowArrow(p) for p in pumps], Indicate(VGroup(bI, bIII, bIV), color=GREEN, scale_factor=1.06),
                  FadeIn(tag), run_time=0.7)
        self.add(hds)
        self.play(LaggedStart(*[mv(d, [5.15, d.get_center()[1], 0], 1.1) for d in hds], lag_ratio=0.06), run_time=1.1)
        chain.add(*pumps, hds, tag)

        # ---- the side door: complex II -------------------------------------------------------------
        self.at("Notice the side door")
        bII = block("II", GREY, 1.4, 0.8).move_to([-2.0, YII, 0])
        self.play(FadeIn(bII, scale=0.8), run_time=0.7)
        chain.add(bII)
        self.at("Complex II")
        caption("Complex II:  succinate-Q reductase")
        self.at("feeds electrons from")
        fad = chip("FADH₂", PURPLE, 28).move_to([-3.9, YII, 0])
        aF = arr([-3.05, YII, 0], [-2.7, YII, 0], PURPLE, 5, 0.15)
        self.play(FadeIn(fad, shift=RIGHT * 0.2), GrowArrow(aF), run_time=0.8)
        chain.add(fad, aF)
        self.at("into the Q")
        aII = arr([-1.3, YII + 0.3, 0], [0.0, YQ - 0.1, 0], YELLOW, 5, 0.18)
        e2 = edot([-3.4, YII, 0], 0.13)
        self.add(e2)
        self.play(GrowArrow(aII), seq(e2, [(-2.0, YII, 0), (-0.6, YQ - 0.05, 0), (0.45, YQ, 0)], 0.5), run_time=1.5)
        self.play(FadeOut(e2), run_time=0.2)
        chain.add(aII)
        self.at("does not pump protons")
        nopump = T("no pump", 28, RED).move_to([-2.0, -0.78, 0])
        nx = xmark([-3.05, -0.78, 0], 0.13, RED, 5)
        self.play(FadeIn(nopump, shift=UP * 0.1), Create(nx), run_time=0.7)
        chain.add(nopump, nx)
        self.at("that complex II is a feeder")
        feed = T("feeder, not a pump", 28, GREY, weight=BOLD).move_to([-2.0, -0.78, 0])
        self.play(Transform(nopump, feed), FadeOut(nx), Indicate(bII, color=GREY, scale_factor=1.12), run_time=1.0)

        # ---- the consequence: fewer protons for FADH2 ----------------------------------------------------
        self.at("explains why")
        head = T("Protons pumped per electron pair", 32, font=TITLE_FONT).move_to([0, 2.5, 0])
        self.play(FadeOut(chain), FadeOut(cap[0]), FadeIn(head), run_time=0.7)

        def route(label, mid_first, y, hnum, anum):
            ch = chip(label, PURPLE, 28)
            ch.move_to([-4.9 + ch.width / 2, y, 0])
            cx = [-2.6, -1.5, -0.4]
            names = [mid_first, "III", "IV"]
            cols = [GREEN if n != "II" else GREY for n in names]
            blks = VGroup(*[block(n, c, 0.85, 0.75, 30) for n, c in zip(names, cols)])
            for b, x in zip(blks, cx):
                b.move_to([x, y, 0])
            a0 = arr([ch.get_right()[0] + 0.05, y, 0], [-3.1, y, 0], PURPLE, 4, 0.15)
            a1 = arr([0.15, y, 0], [0.85, y, 0], BLUE, 4, 0.15)
            hn = M(hnum, 28, BLUE, weight=BOLD).move_to([1.95, y, 0])
            a2 = arr([2.95, y, 0], [3.55, y, 0], TEAL, 4, 0.15)
            an = M(anum, 28, TEAL, weight=BOLD).move_to([4.75, y, 0])
            return ch, a0, blks, a1, hn, a2, an

        self.at("FADH2 yields")
        rf = route("FADH₂", "II", 0.65, "~6 H⁺", "~1.5 ATP")
        self.play(FadeIn(rf[0]), GrowArrow(rf[1]), FadeIn(rf[2], lag_ratio=0.2), run_time=0.8)
        self.play(GrowArrow(rf[3]), FadeIn(rf[4]), run_time=0.4)
        self.at("less ATP")
        self.play(GrowArrow(rf[5]), FadeIn(rf[6]), run_time=0.5)
        self.at("than NADH")
        rn = route("NADH", "I", -1.0, "~10 H⁺", "~2.5 ATP")
        self.play(FadeIn(rn[0]), GrowArrow(rn[1]), FadeIn(rn[2], lag_ratio=0.2), run_time=0.7)
        self.play(GrowArrow(rn[3]), FadeIn(rn[4]), GrowArrow(rn[5]), FadeIn(rn[6]), run_time=0.6)

        # ---- back to the chain: every step is downhill ------------------------------------------------
        self.at("The reduction potentials")
        panel = Group(head, *[m for r in (rf, rn) for m in r])
        cap2 = T("", 24)
        self.play(FadeOut(panel), run_time=0.5)
        chain2 = Group(strip, l_mat, l_ims, nadh, bI, aI, q, aQ, bIII, aIII, cc, a_c1, bIV, a_c2, o2, aO,
                       bII, fad, aF, aII)
        # reset what changed: pumps arrows come back thin, no dots
        self.play(FadeIn(chain2), FadeIn(VGroup(*pumps)), run_time=0.7)
        self.at("on the left")
        hdr = T("E°′ (V)", 26, GREY).move_to([-5.6, 3.2, 0])
        vals = VGroup(
            M(MINUS + "0.32", 26, PURPLE).move_to([-5.6, YI, 0]),
            M("+0.04", 26, TEXT).move_to([-5.6, YQ, 0]),
            M("+0.25", 26, TEXT).move_to([-5.6, YCC, 0]),
            M("+0.82", 26, ORANGE).move_to([-5.6, YIV, 0]),
        )
        who = VGroup(T("Q", 24, GREY).move_to([-4.7, YQ, 0]), T("cyt c", 24, GREY).move_to([-4.6, YCC, 0]))
        self.play(FadeIn(hdr), FadeIn(vals, lag_ratio=0.15), FadeIn(who), run_time=1.0)
        self.at("downhill")
        ball = edot([-5.6, YI + 0.4, 0], 0.14)
        self.add(ball)
        self.play(seq(ball, [(-5.6, YQ + 0.4, 0), (-5.6, YCC + 0.4, 0), (-5.6, YIV + 0.4, 0)], 0.6), run_time=1.8)
        self.finish()


# =============================================================================================
class S04Inhibitors(SpokenScene):
    """Block the chain and read the pattern: upstream reduced, downstream oxidized."""

    NAMES = ["NADH", "Q", "b", "c₁", "c", "a", "a₃", "O₂"]

    def make_row(self, y):
        chips, dots = [], []
        for n in self.NAMES:
            c = chip(n, TEXT, 30, pad=0.14, fill_opacity=0.08)
            chips.append(c)
        g = VGroup(*chips).arrange(RIGHT, buff=0.8).move_to([0, y, 0])
        arrows = []
        for a, b in zip(chips[:-1], chips[1:]):
            arrows.append(arr(a.get_right() + RIGHT * 0.04, b.get_left() + LEFT * 0.04, GREY, 4, 0.14))
        for c in chips:
            d = edot(c[0].get_corner(UR) + np.array([-0.05, 0.02, 0]), 0.11)
            d.set_opacity(0)
            dots.append(d)
        return {"chips": chips, "arrows": arrows, "dots": dots, "y": y}

    def row_group(self, r):
        return VGroup(*r["chips"], *r["arrows"], *r["dots"])

    def state(self, r, k):
        """Chips [0,k) reduced (yellow, hold e-), chips [k,end) oxidized (grey, empty)."""
        out = []
        for i, c in enumerate(r["chips"]):
            if i < k:
                out += [c[0].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.3), c[1].animate.set_color(TEXT),
                        r["dots"][i].animate.set_opacity(1)]
            else:
                out += [c[0].animate.set_stroke(GREY).set_fill(GREY, 0.0), c[1].animate.set_color(GREY),
                        r["dots"][i].animate.set_opacity(0)]
        return out

    def gap_x(self, r, g):
        a, b = r["chips"][g], r["chips"][g + 1]
        return (a.get_right()[0] + b.get_left()[0]) / 2

    def construct(self):
        head = T("Block the chain, then read the pattern", 36, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.at("This is a beautiful piece")
        self.play(Write(head), run_time=1.6)

        legend = VGroup()
        lr = chip("reduced", YELLOW, 26, pad=0.14, fill_opacity=0.3)
        ld = edot(lr[0].get_corner(UR) + np.array([-0.05, 0.02, 0]), 0.11)
        lt = T("holds e⁻", 24, GREY).next_to(lr, RIGHT, buff=0.2)
        lo = chip("oxidized", GREY, 26, pad=0.14, fill_opacity=0.0)
        lt2 = T("empty", 24, GREY).next_to(lo, RIGHT, buff=0.2)
        legend = VGroup(VGroup(lr, ld, lt), VGroup(lo, lt2)).arrange(RIGHT, buff=0.9).move_to([0, 2.55, 0])

        r1 = self.make_row(1.15)
        r1_title = T("the electron-transport chain", 26, GREY)
        left_at(r1_title, -6.0, 1.85)

        self.at("reason through it")
        self.play(FadeIn(self.row_group(r1)), FadeIn(r1_title), run_time=0.8)
        # electrons flow freely down the neutral chain
        ball = edot([r1["chips"][0].get_center()[0], 1.15, 0], 0.13)
        self.add(ball)
        path = [(c.get_center()[0], 1.15, 0) for c in r1["chips"][1:]]
        self.play(seq(ball, path, 0.17), run_time=1.2)
        self.play(FadeOut(ball), run_time=0.15)

        self.at("block the chain")
        gx = self.gap_x(r1, 1)
        bm = block_mark([gx, 1.15, 0])
        bl_t = T("a block", 26, RED)
        left_at(bl_t, -6.0, 1.85)
        self.play(FadeIn(bm, scale=0.4), Transform(r1_title, bl_t), run_time=0.8)

        self.at("everything upstream of the block")
        up = Brace(VGroup(*r1["chips"][:2]), DOWN, color=GREY, buff=0.1)
        up_l = T("upstream", 24, GREY).next_to(up, DOWN, buff=0.05)
        self.play(GrowFromCenter(up), FadeIn(up_l), run_time=0.7)
        self.at("piles up in the reduced state")
        self.play(FadeIn(legend[0]), *self.state(r1, 2)[:6], run_time=1.2)
        self.at("everything downstream")
        dn = Brace(VGroup(*r1["chips"][2:]), DOWN, color=GREY, buff=0.1)
        dn_l = T("downstream", 24, GREY).next_to(dn, DOWN, buff=0.05)
        self.play(GrowFromCenter(dn), FadeIn(dn_l), run_time=0.7)
        self.at("becomes oxidized")
        self.play(FadeIn(legend[1]), *self.state(r1, 2), run_time=1.3)

        # ---- rotenone ---------------------------------------------------------------------------------
        self.at("So rotenone")
        rt = T("Rotenone: blocks Complex I", 28, GREY, t2c={"Rotenone": RED})
        left_at(rt, -6.0, 1.85)
        self.play(FadeOut(up), FadeOut(up_l), FadeOut(dn), FadeOut(dn_l), Transform(r1_title, rt),
                  bm.animate.move_to([self.gap_x(r1, 0), 1.15, 0]), run_time=1.0)
        self.at("leaves NADH reduced")
        self.play(*self.state(r1, 1), run_time=1.0)

        # ---- antimycin A ------------------------------------------------------------------------------
        self.at("Antimycin")
        r2 = self.make_row(-0.55)
        at_t = T("Antimycin A: blocks Complex III", 28, GREY, t2c={"Antimycin A": RED})
        left_at(at_t, -6.0, 0.15)
        self.play(FadeIn(self.row_group(r2)), FadeIn(at_t), run_time=0.9)
        self.at("blocking complex III")
        bm2 = block_mark([self.gap_x(r2, 2), -0.55, 0])
        self.play(FadeIn(bm2, scale=0.4), run_time=0.6)
        self.at("leaves carriers up to")
        self.play(*self.state(r2, 3), run_time=1.4)

        # ---- cyanide ----------------------------------------------------------------------------------
        self.at("Cyanide")
        r3 = self.make_row(-2.25)
        cy_t = T("Cyanide: blocks Complex IV", 28, GREY, t2c={"Cyanide": RED})
        left_at(cy_t, -6.0, -1.55)
        self.play(FadeIn(self.row_group(r3)), FadeIn(cy_t), run_time=0.9)
        self.at("blocking complex IV")
        bm3 = block_mark([self.gap_x(r3, 6), -2.25, 0])
        self.play(FadeIn(bm3, scale=0.4), run_time=0.6)
        self.at("leaves the entire chain reduced")
        self.play(*self.state(r3, 7), run_time=1.4)
        self.at("only oxygen unreduced")
        ox = T("only O₂ unreduced", 24, GREY).next_to(r3["chips"][7], DOWN, buff=0.22)
        self.play(FadeIn(ox, shift=UP * 0.1), Indicate(r3["chips"][7], color=ORANGE, scale_factor=1.15), run_time=0.9)

        # ---- read the pattern ---------------------------------------------------------------------------
        self.at("By reading which carriers")
        bounds = VGroup()
        for r, g in ((r1, 0), (r2, 2), (r3, 6)):
            x = self.gap_x(r, g)
            bounds.add(DashedLine([x, r["y"] + 0.42, 0], [x, r["y"] - 0.42, 0], color=TEXT, dash_length=0.08, stroke_width=3))
        self.play(Create(bounds), run_time=0.9)
        self.at("deduce")
        note = T("the reduced | oxidized boundary maps the order of flow", 26, TEXT).move_to([0, -3.35, 0])
        self.play(FadeIn(note, shift=UP * 0.1), FadeOut(ox), run_time=1.0)
        self.finish()


# =============================================================================================
class S05Battery(SpokenScene):
    """The mitochondrion as a rechargeable battery: charging cable, discharge circuit, cut cable, short."""

    def construct(self):
        lv = ValueTracker(0.0)
        BX, BY, BW, BH = 0.0, -0.1, 3.4, 4.4
        body = RoundedRectangle(corner_radius=0.2, width=BW, height=BH, stroke_color=GREY, stroke_width=5,
                                fill_opacity=0).move_to([BX, BY, 0])
        cap = Rectangle(width=1.0, height=0.28, stroke_color=GREY, stroke_width=5, fill_color=GREY,
                        fill_opacity=0.6).move_to([BX, BY + BH / 2 + 0.14, 0])
        bottom = BY - BH / 2 + 0.07

        def fill():
            H = max(0.001, lv.get_value() * (BH - 0.14))
            return Rectangle(width=BW - 0.14, height=H, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to(
                [BX, bottom + H / 2, 0])

        fillm = always_redraw(fill)
        pmf = VGroup(T("proton-motive", 28, TEXT, weight=BOLD), T("force", 28, TEXT, weight=BOLD)).arrange(DOWN, buff=0.12)
        pmf.move_to([BX, BY, 0])
        l_top = T("intermembrane space  (+)", 24, GREY).move_to([BX, BY + BH / 2 + 0.7, 0])
        l_bot = T("matrix  (" + MINUS + ")", 24, GREY).move_to([BX, BY - BH / 2 - 0.4, 0])
        legend = legend_hpe(5.2, 3.2)

        self.at("the mitochondrion as a rechargeable battery")
        self.add(fillm)
        self.play(Create(body), FadeIn(cap), FadeIn(l_top), FadeIn(l_bot), FadeIn(legend), run_time=1.6)

        # ---- charging side ---------------------------------------------------------------------------
        self.at("The electron transport chain")
        etc = VGroup(box(1.9, 1.5, GREEN, 0.28), T("electron-\ntransport\nchain", 24, GREEN, weight=BOLD))
        etc[1].move_to(etc[0])
        etc.move_to([-4.9, 0.55, 0])
        self.play(FadeIn(etc, shift=RIGHT * 0.2), run_time=0.8)
        self.at("is the charging cable")
        cable_y = 0.55
        cable = Line([-3.95, cable_y, 0], [BX - BW / 2, cable_y, 0], color=TEXT, stroke_width=9)
        cab_l = T("charging\ncable", 26, TEXT).move_to([-2.65, cable_y + 0.85, 0])
        self.play(Create(cable), FadeIn(cab_l, shift=DOWN * 0.1), run_time=1.0)

        self.at("using the energy of electron flow")
        ee = [edot([-6.1 + 0.0, -0.75, 0], 0.11) for _ in range(4)]
        efl = T("e⁻ flow", 24, YELLOW).move_to([-4.9, -1.2, 0])
        self.add(*ee)
        self.play(FadeIn(efl), LaggedStart(*[Succession(mv(d, [-3.75, -0.75, 0], 1.0, linear), FadeOut(d, run_time=0.1))
                                            for d in ee], lag_ratio=0.35), run_time=2.0)
        self.at("to pump protons")
        hs = [hdot([-3.9, cable_y, 0]) for _ in range(5)]
        self.add(*hs)
        self.play(FadeOut(efl, run_time=0.6), LaggedStart(*[Succession(mv(d, [BX - BW / 2 + 0.3, cable_y, 0], 0.8, linear), FadeOut(d, run_time=0.1))
                                for d in hs], lag_ratio=0.25),
                  lv.animate(run_time=3.2, rate_func=linear).set_value(0.85), run_time=3.2)
        self.at("proton motive force")
        self.play(FadeIn(pmf), run_time=0.7)

        # ---- discharge side ---------------------------------------------------------------------------
        self.at("ATP synthase is the discharge circuit")
        syn = VGroup(box(1.8, 1.3, TEAL, 0.28), T("ATP\nsynthase", 26, TEAL, weight=BOLD))
        syn[1].move_to(syn[0])
        syn.move_to([4.9, 0.55, 0])
        wire = Line([BX + BW / 2, cable_y, 0], [4.0, cable_y, 0], color=TEXT, stroke_width=9)
        wir_l = T("discharge\ncircuit", 26, TEXT).move_to([2.7, cable_y + 0.85, 0])
        self.play(FadeIn(syn, shift=LEFT * 0.2), Create(wire), FadeIn(wir_l, shift=DOWN * 0.1), run_time=1.2)
        self.at("letting protons flow back")
        hs2 = [hdot([BX + BW / 2 - 0.3, cable_y, 0]) for _ in range(5)]
        self.add(*hs2)
        self.play(LaggedStart(*[Succession(mv(d, [4.0, cable_y, 0], 0.9, linear), FadeOut(d, run_time=0.1)) for d in hs2],
                              lag_ratio=0.22),
                  lv.animate(run_time=2.6, rate_func=linear).set_value(0.7), run_time=2.6)
        self.at("and make ATP")
        atps = VGroup(chip("ATP", TEAL, 26).move_to([4.2, -1.1, 0]), chip("ATP", TEAL, 26).move_to([5.6, -1.1, 0]))
        a_a = VGroup(arr([4.5, -0.25, 0], [4.35, -0.72, 0], TEAL, 4, 0.15), arr([5.3, -0.25, 0], [5.45, -0.72, 0], TEAL, 4, 0.15))
        self.play(FadeIn(a_a), FadeIn(atps, shift=DOWN * 0.15, lag_ratio=0.3), run_time=1.0)

        # ---- cut the charging cable ------------------------------------------------------------------------
        self.at("Cut the charging cable")
        cut_gap = [(-3.0, cable_y), (-2.4, cable_y)]
        gap = Rectangle(width=0.6, height=0.5, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([-2.7, cable_y, 0])
        gap.set_z_index(3)
        cut_x = xmark([-2.7, cable_y, 0], 0.2, RED, 7)
        cut_x.set_z_index(4)
        etc.save_state()
        self.play(FadeIn(gap), Create(cut_x), cab_l.animate.set_opacity(0.4), etc.animate.set_opacity(0.45), run_time=0.8)
        self.at("cyanide")
        cy = T("cyanide blocks\nComplex IV", 26, RED).move_to([-3.35, -0.6, 0])
        self.play(FadeIn(cy, shift=UP * 0.1), run_time=0.8)
        self.at("the battery never charges")
        self.play(lv.animate(run_time=1.6, rate_func=smooth).set_value(0.08),
                  FadeOut(atps), FadeOut(a_a), run_time=1.6)

        # ---- the uncoupler: a short circuit ------------------------------------------------------------------
        self.at("Add an uncoupler")
        self.play(FadeOut(gap), FadeOut(cut_x), FadeOut(cy), cab_l.animate.set_opacity(1), Restore(etc),
                  run_time=0.5)
        hs3 = [hdot([-3.9, cable_y, 0]) for _ in range(4)]
        self.add(*hs3)
        self.play(LaggedStart(*[Succession(mv(d, [BX - BW / 2 + 0.3, cable_y, 0], 0.5, linear), FadeOut(d, run_time=0.1))
                                for d in hs3], lag_ratio=0.2),
                  lv.animate(run_time=1.1, rate_func=linear).set_value(0.75), run_time=1.1)
        self.at("pokes holes")
        HY = -1.3
        hole = Circle(radius=0.2, stroke_color=RED, stroke_width=6, fill_color=BG, fill_opacity=1)
        hole.move_to([BX + BW / 2, HY, 0]).set_z_index(3)
        unc = T("uncoupler", 28, RED).move_to([3.0, -0.35, 0])
        self.play(FadeIn(hole, scale=0.3), FadeIn(unc, shift=UP * 0.1), run_time=0.7)
        self.at("the battery short")
        leak = [hdot([BX + BW / 2 - 0.2, HY, 0]) for i in range(5)]
        self.add(*leak)
        self.play(LaggedStart(*[Succession(mv(d, [BX + BW / 2 + 0.9, HY + 0.1 * (i - 2), 0], 0.6, linear),
                                           mv(d, [BX + BW / 2 + 1.7, HY + 0.25 * (i - 2), 0], 0.5, linear),
                                           FadeOut(d, run_time=0.1)) for i, d in enumerate(leak)], lag_ratio=0.25),
                  run_time=1.9)
        self.at("draining its charge as heat")
        heat = VGroup()
        for i in range(3):
            xs = 3.2 + 0.5 * i
            pts = [np.array([xs + 0.13 * np.sin(k * 1.8 + i), -2.3 + 0.28 * k, 0]) for k in range(5)]
            w = VMobject(stroke_color=RED, stroke_width=5)
            w.set_points_smoothly(pts)
            heat.add(w)
        heat_l = T("heat", 30, RED).move_to([3.7, -2.85, 0])
        self.play(Create(heat, lag_ratio=0.3), FadeIn(heat_l), lv.animate(run_time=1.6, rate_func=smooth).set_value(0.12),
                  run_time=1.6)
        self.at("instead of ATP")
        ghost = chip("ATP", TEAL, 26).move_to([5.2, -1.0, 0])
        ghost[0].set_stroke(opacity=0.6).set_fill(opacity=0.06)
        ghost[1].set_opacity(0.6)
        gx = Line(ghost.get_corner(DL) + LEFT * 0.08, ghost.get_corner(UR) + RIGHT * 0.08, color=RED, stroke_width=6)
        self.play(FadeIn(ghost), Create(gx), run_time=0.8)
        self.finish()
