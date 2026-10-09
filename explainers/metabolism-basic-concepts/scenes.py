"""Metabolism: the cell's energy economy.

COLOR MAP (one color per concept, whole video)
  BLUE   = molecules / reactant A / the material being built or broken (circles, chains)
  PINK   = product B of the A <-> B reaction (scene 4 only)
  YELLOW = ATP and usable cellular energy currency (ATP chips, ion gradient chips)
  GREEN  = energy released / downhill / favorable / catabolism flux
  RED    = energy required / uphill / unfavorable / strain / anabolism flux
  ORANGE = ADP          PURPLE = AMP
  TEAL   = water (hydration dots)
  GREY   = neutral labels, axes, frames       TEXT = plain text, enzyme chip
No molecular structures are drawn: molecules are circles, chains of circles, and labelled chips.
"""
import math
import random
from bp_style import *  # noqa: F401,F403

ORANGE = "#F0A04B"
PURPLE = "#B58CE0"
PINK = "#E58FC4"


# ----------------------------------------------------------------------------- helpers
def dot(color=BLUE, r=0.26, op=0.9):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=op)


def chain(n, color=BLUE, r=0.26):
    """n touching circles = one large molecule (schematic, no bonds)."""
    return VGroup(*[dot(color, r) for _ in range(n)]).arrange(RIGHT, buff=-0.02)


def spread(n, color=BLUE, r=0.26, buff=0.5):
    return VGroup(*[dot(color, r) for _ in range(n)]).arrange(RIGHT, buff=buff)


def mini(text, color, size=24, pad=0.12):
    return chip(text, color, size=size, pad=pad)


def lane_frame(center_y, label, w=12.4, h=2.5):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2,
                           fill_color=GREY, fill_opacity=0.06).move_to([0, center_y, 0])
    lab = T(label, 24, TEXT, weight=BOLD).rotate(PI / 2).move_to([-w / 2 + 0.38, center_y, 0])
    return box, lab


def sig(x, c, w):
    return 0.5 * (1 + math.tanh((x - c) / w))


def gauss(x, c, w):
    return math.exp(-((x - c) / w) ** 2)


def make_axes(y_lo, y_hi, width, height, y_step=10):
    """Axes with no numbers or ticks."""
    return Axes(x_range=[0, 10, 1], y_range=[y_lo, y_hi, y_step], x_length=width, y_length=height,
                axis_config={"include_numbers": False, "include_ticks": False, "color": GREY,
                             "stroke_width": 3, "tip_width": 0.16, "tip_height": 0.16}, tips=True)


def place_axes(ax, left, bottom):
    ax.shift(np.array([left, bottom, 0]) - ax.c2p(0, ax.y_range[0]))
    return ax


# ============================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Metabolism: basic concepts"
    TITLE = "The cell's energy economy"


# ----------------------------------------------------------------------------- s01: two camps
class S01TwoCamps(SpokenScene):
    def construct(self):
        top, top_lab = lane_frame(2.25, "CATABOLISM")
        bot, bot_lab = lane_frame(-2.25, "ANABOLISM")

        # ---- catabolism lane contents
        big = chain(4).move_to([-3.9, 2.75, 0])
        fuel_cap = T("carbohydrates, fats", 24, GREY).next_to(big, DOWN, buff=0.22)
        arr_c = Arrow([-2.4, 2.75, 0], [-0.6, 2.75, 0], color=TEXT, stroke_width=6, buff=0, tip_length=0.28)
        small = spread(4, BLUE, 0.2, 0.55).move_to([1.6, 2.75, 0])
        prod = VGroup(mini("CO₂", TEXT, 26), mini("H₂O", TEXT, 26)).arrange(RIGHT, buff=0.35).move_to([1.6, 2.75, 0])
        e_lab = T("energy released", 26, GREEN).move_to([-3.0, 1.5, 0])
        e_arr = Arrow([-1.55, 1.5, 0], [-0.85, 1.5, 0], color=GREEN, stroke_width=5, buff=0, tip_length=0.2)
        atp_c = mini("ATP", YELLOW, 26).move_to([0.0, 1.5, 0])
        or_t = T("or", 24, GREY).move_to([1.05, 1.5, 0])
        ion_c = mini("ion gradients", YELLOW, 26).move_to([2.8, 1.5, 0])

        # ---- anabolism lane contents
        pre = spread(4, BLUE, 0.2, 0.3).move_to([-4.1, -1.75, 0])
        pre_cap = T("simple precursors", 24, GREY).next_to(pre, DOWN, buff=0.22)
        arr_a = Arrow([-2.4, -1.75, 0], [-0.6, -1.75, 0], color=TEXT, stroke_width=6, buff=0, tip_length=0.28)
        built = chain(4).move_to([1.6, -1.75, 0])
        built_cap = T("complex biomolecules", 24, GREY).next_to(built, DOWN, buff=0.22)
        atp_a = mini("ATP", YELLOW, 26).move_to([-4.6, -3.0, 0])
        red_a = mini("reducing power", YELLOW, 26).move_to([-2.45, -3.0, 0])
        e_need = T("energy required", 26, RED).move_to([-1.5, -3.0, 0])
        e_need_arr = Arrow([-1.5, -2.65, 0], [-1.5, -2.0, 0], color=RED, stroke_width=5, buff=0, tip_length=0.2)

        # opening: one pathway = a chain of conversions, which then sorts into two camps
        pw_dots = VGroup(*[dot(BLUE, 0.3) for _ in range(5)]).arrange(RIGHT, buff=0.9)
        pw_arrows = VGroup(*[Arrow(pw_dots[i].get_right(), pw_dots[i + 1].get_left(), color=TEXT, buff=0.08,
                                   stroke_width=4, tip_length=0.2) for i in range(4)])
        pathway = VGroup(pw_dots, pw_arrows).move_to([0, 0, 0])
        self.at("Every metabolic pathway", 0.0)
        seq = []
        for i in range(5):
            seq.append(FadeIn(pw_dots[i], scale=0.6))
            if i < 4:
                seq.append(GrowArrow(pw_arrows[i]))
        self.play(LaggedStart(*seq, lag_ratio=0.15), run_time=1.6)
        self.at("two camps", 0.4)
        self.play(FadeOut(pathway, scale=0.7), FadeIn(top), FadeIn(bot), FadeIn(top_lab), FadeIn(bot_lab), run_time=0.8)

        # ---- catabolism
        self.at("Catabolic pathways", 0.3)
        self.play(Indicate(top_lab, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.at("break large molecules down", 0.2)
        self.play(FadeIn(big, scale=0.8), run_time=0.5)
        self.play(FadeIn(arr_c), TransformFromCopy(big, small), run_time=1.2)
        self.at("carbohydrates and fats", 0.4)
        self.play(FadeIn(fuel_cap, shift=UP * 0.1), run_time=0.6)
        self.at("carbon dioxide and water", 0.3)
        self.play(ReplacementTransform(small, prod), run_time=1.0)
        self.at("capture the released energy", 0.2)
        self.play(FadeIn(e_lab, shift=RIGHT * 0.1), GrowArrow(e_arr), run_time=0.8)
        self.at("as ATP", 0.2)
        self.play(FadeIn(atp_c, scale=0.7), run_time=0.5)
        self.at("or as ion gradients", 0.2)
        self.play(FadeIn(or_t), FadeIn(ion_c, scale=0.7), run_time=0.7)

        # ---- anabolism
        self.at("Anabolic pathways", 0.3)
        self.play(Indicate(bot_lab, color=RED, scale_factor=1.15), run_time=0.8)
        self.at("They take simple precursors", 0.2)
        self.play(FadeIn(pre, shift=RIGHT * 0.1), FadeIn(pre_cap), FadeIn(arr_a), run_time=0.8)
        self.at("spend energy and reducing power", 0.2)
        self.play(FadeIn(atp_a, shift=UP * 0.1), FadeIn(red_a, shift=UP * 0.1), run_time=0.7)
        mid = np.array([-1.5, -1.75, 0])
        self.play(atp_a.animate.move_to(mid).scale(0.5).set_opacity(0),
                  red_a.animate.move_to(mid).scale(0.4).set_opacity(0), run_time=1.0)
        self.play(FadeIn(e_need, shift=UP * 0.1), GrowArrow(e_need_arr), run_time=0.6)
        self.at("build complex biomolecules", 0.2)
        self.play(TransformFromCopy(pre, built), FadeIn(built_cap), run_time=1.2)

        # ---- summary
        self.at("So catabolism releases energy", 0.2)
        self.play(Indicate(e_lab, color=GREEN, scale_factor=1.12), Indicate(top_lab, color=GREEN), run_time=1.2)
        self.at("Anabolism consumes energy", 0.2)
        self.play(Indicate(e_need, color=RED, scale_factor=1.12), Indicate(bot_lab, color=RED), run_time=1.2)

        # ---- both at once, products feed each other
        self.at("The cell is constantly running both", 0.2)
        self.play(Indicate(top, color=GREEN, scale_factor=1.02), Indicate(bot, color=RED, scale_factor=1.02), run_time=1.2)
        # catabolism's products (ATP, reducing power) feed anabolism; anabolism's products (stored fuel) feed catabolism
        a1 = Arrow([-0.6, 0.92, 0], [-0.6, -0.92, 0], color=YELLOW, stroke_width=6, buff=0, tip_length=0.25)
        a2 = Arrow([0.6, -0.92, 0], [0.6, 0.92, 0], color=BLUE, stroke_width=6, buff=0, tip_length=0.25)
        l1 = T("ATP, reducing power", 26, YELLOW)
        l1.next_to(a1, LEFT, buff=0.3)
        l2 = T("stored fuel, macromolecules", 26, BLUE)
        l2.next_to(a2, RIGHT, buff=0.3)
        self.at("with the products of one feeding", 0.2)
        self.play(GrowArrow(a1), FadeIn(l1, shift=DOWN * 0.1), run_time=0.8)
        self.play(GrowArrow(a2), FadeIn(l2, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s02: coupling
class S02Coupling(SpokenScene):
    def construct(self):
        y_lo, y_hi = -20, 50
        axL = make_axes(y_lo, y_hi, 5.0, 4.5)
        place_axes(axL, -6.0, -2.6)
        axR = make_axes(y_lo, y_hi, 5.0, 4.5)
        place_axes(axR, 1.0, -2.6)

        xlabL = T("reaction coordinate", 24, GREY).move_to([axL.c2p(5, y_lo)[0], axL.c2p(0, y_lo)[1] - 0.5, 0])
        xlabR = T("reaction coordinate", 24, GREY).move_to([axR.c2p(5, y_lo)[0], axR.c2p(0, y_lo)[1] - 0.5, 0])
        ylabL = T("free energy (kJ/mol)", 24, GREY).rotate(PI / 2).move_to([-6.45, -0.35, 0])
        ylabR = T("free energy (kJ/mol)", 24, GREY).rotate(PI / 2).move_to([0.55, -0.35, 0])

        # one smooth hill up to B + C (barrier peak ~ +29), then the coupled path continues downhill
        fL = lambda x: 21 * sig(x, 5.4, 0.9) + 26 * gauss(x, 4.7, 1.0)
        fR1 = lambda x: 21 * sig(x, 3.0, 0.65) + 26 * gauss(x, 2.4, 0.75)
        fR = lambda x: fR1(x) - 34 * sig(x, 7.0, 0.5)

        curveL = axL.plot(fL, x_range=[0, 10], color=RED, stroke_width=6)
        curveR_up = axR.plot(fR1, x_range=[0, 6.0], color=RED, stroke_width=6)
        curveR_dn = axR.plot(fR, x_range=[5.9, 10], color=GREEN, stroke_width=6)

        zeroL = DashedLine(axL.c2p(0, 0), axL.c2p(10, 0), color=GREY, stroke_width=2, dash_length=0.1)
        zeroR = DashedLine(axR.c2p(0, 0), axR.c2p(10, 0), color=GREY, stroke_width=2, dash_length=0.1)

        titL = T("ALONE", 26, TEXT, weight=BOLD).move_to([axL.c2p(5, 0)[0], 3.15, 0])
        titR = T("COUPLED", 26, TEXT, weight=BOLD).move_to([axR.c2p(5, 0)[0], 3.15, 0])

        # markers
        A_L = T("A", 30, TEXT, weight=BOLD).move_to(axL.c2p(0.7, 0) + UP * 0.38)
        BC_L = T("B + C", 30, TEXT, weight=BOLD).move_to(axL.c2p(8.4, 21) + UP * 0.42)
        A_R = T("A", 30, TEXT, weight=BOLD).move_to(axR.c2p(0.7, 0) + UP * 0.38)
        B_R = T("B", 30, TEXT, weight=BOLD).move_to(axR.c2p(4.9, 21) + UP * 0.42)
        CD_R = T("C + D", 30, TEXT, weight=BOLD).move_to(axR.c2p(8.4, -18.5))

        # delta-G arrows
        up21 = Arrow(axL.c2p(9.0, 0), axL.c2p(9.0, 21), color=RED, buff=0, stroke_width=6, tip_length=0.22)
        up21_t = T("+21", 28, RED, weight=BOLD).next_to(up21, LEFT, buff=0.12)
        r21 = Arrow(axR.c2p(4.2, 0), axR.c2p(4.2, 21), color=RED, buff=0, stroke_width=6, tip_length=0.22)
        r21_t = T("+21", 28, RED, weight=BOLD).next_to(r21, RIGHT, buff=0.12).shift(DOWN * 0.25)
        top_dash = DashedLine(axR.c2p(4.2, 21), axR.c2p(9.1, 21), color=GREY, stroke_width=2, dash_length=0.1)
        g34 = Arrow(axR.c2p(9.1, 21), axR.c2p(9.1, -13), color=GREEN, buff=0, stroke_width=6, tip_length=0.22)
        g34_t = T("−34", 28, GREEN, weight=BOLD).next_to(g34, LEFT, buff=0.12).shift(UP * 0.8)
        net = Arrow(axR.c2p(0.5, 0), axR.c2p(0.5, -13), color=GREEN, buff=0, stroke_width=7, tip_length=0.22)
        net_dash = DashedLine(axR.c2p(0.5, -13), axR.c2p(10, -13), color=GREEN, stroke_width=2.5, dash_length=0.12)
        net_t = T("net −13", 28, GREEN, weight=BOLD).move_to(axR.c2p(0.5, -13) + RIGHT * 1.15 + DOWN * 0.38)
        eq = M("+21 + (−34) = −13", 26, TEXT).move_to([axR.c2p(5, 0)[0], 1.5, 0])
        eq_u = T("kJ/mol", 22, GREY).next_to(eq, DOWN, buff=0.08)

        ball = Dot(radius=0.14, color=TEXT).move_to(axL.c2p(0, 0))

        # ---- left panel
        self.play(Create(axL), FadeIn(xlabL), FadeIn(ylabL), run_time=0.6)
        self.add(ball)
        self.at("won't go on its own", 0.2)
        self.play(FadeIn(zeroL), Create(curveL), FadeIn(A_L), run_time=1.6)
        self.at("forced uphill", 0.0)
        self.play(Indicate(curveL, color=RED, scale_factor=1.0), run_time=1.0)
        self.at("On the left", 0.2)
        self.play(FadeIn(titL), run_time=0.5)
        self.at("A to B plus C", 0.2)
        self.play(FadeIn(BC_L, shift=UP * 0.1), run_time=0.5)
        self.at("positive delta G of plus", 0.2)
        self.play(GrowArrow(up21), FadeIn(up21_t), run_time=0.8)
        self.at("so alone it stalls", 0.3)
        # the ball climbs toward the barrier and rolls back
        self.play(ball.animate.move_to(axL.c2p(4.2, fL(4.2))), run_time=0.7, rate_func=smooth)
        self.play(ball.animate.move_to(axL.c2p(0, 0)), run_time=0.45, rate_func=rush_into)

        # ---- right panel
        self.at("On the right", 0.2)
        self.play(Create(axR), FadeIn(xlabR), FadeIn(ylabR), FadeIn(titR), FadeIn(zeroR), run_time=0.7)
        self.at("we couple it to", 0.2)
        self.play(Create(curveR_up), FadeIn(A_R), FadeIn(B_R), run_time=1.0)
        self.at("strongly favorable reaction", 0.2)
        self.play(GrowArrow(r21), FadeIn(r21_t), run_time=0.4)
        self.play(Create(curveR_dn), FadeIn(CD_R), FadeIn(top_dash), run_time=1.0)
        self.at("with a delta G of minus", 0.2)
        self.play(GrowArrow(g34), FadeIn(g34_t), run_time=0.8)

        # ---- add them
        self.at("Add them", 0.1)
        self.play(FadeIn(eq), FadeIn(eq_u), run_time=0.8)
        self.at("the net delta G is minus", 0.2)
        self.play(GrowArrow(net), Create(net_dash), FadeIn(net_t), run_time=1.0)
        self.at("so the combined pathway proceeds", 0.2)
        rball = Dot(radius=0.14, color=TEXT).move_to(axR.c2p(0, 0))
        self.add(rball)
        tr = ValueTracker(0.0)
        rball.add_updater(lambda m: m.move_to(axR.c2p(tr.get_value(), fR(tr.get_value()))))
        self.play(tr.animate.set_value(10.0), run_time=3.0, rate_func=linear)
        rball.clear_updaters()

        # ---- the principle
        self.at("This is the central trick", 0.2)
        self.play(Indicate(net_t, color=GREEN, scale_factor=1.2), Indicate(net, color=GREEN), run_time=1.3)
        self.at("Individual steps must be specific", 0.2)
        s1 = T("specific step", 24, RED).move_to([axR.c2p(2.6, 0)[0], 1.25, 0])
        s2 = T("specific step", 24, GREEN).move_to([axR.c2p(7.6, 0)[0], 1.25, 0])
        self.play(FadeOut(eq), FadeOut(eq_u), FadeIn(s1, shift=DOWN * 0.1), FadeIn(s2, shift=DOWN * 0.1), run_time=0.9)
        self.at("only the pathway as a whole", 0.2)
        path_all = axR.plot(fR, x_range=[0, 10], color=GREEN, stroke_width=11)
        whole_t = fit(T("the whole pathway must be favorable", 26, GREEN), max_w=4.8).move_to([3.8, 1.5, 0])
        self.play(FadeOut(s1), FadeOut(s2), FadeIn(whole_t), ShowPassingFlash(path_all, time_width=0.5), run_time=1.4)
        self.play(Indicate(net_t, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.at("Coupling is how the cell pays", 0.2)
        pay = fit(T("coupling pays for the uphill step", 26, TEXT), max_w=4.8).move_to([3.8, 1.5, 0])
        self.play(FadeOut(whole_t), Indicate(g34, color=GREEN), Indicate(g34_t, color=GREEN),
                  FadeIn(pay), run_time=1.3)
        self.finish()


# ----------------------------------------------------------------------------- s03: why ATP hydrolysis releases energy
class S03WhyAtp(SpokenScene):
    def construct(self):
        CW, CH = 6.15, 2.4
        centers = [(-3.1, 1.2), (3.1, 1.2), (-3.1, -1.5), (3.1, -1.5)]
        titles = ["1  Charge repulsion drops", "2  Resonance stabilization", "3  Entropy rises", "4  Better hydration"]
        frames, ttl = [], []
        for (cx, cy), tx in zip(centers, titles):
            f = RoundedRectangle(corner_radius=0.16, width=CW, height=CH, stroke_color=GREY, stroke_width=2,
                                 fill_color=GREY, fill_opacity=0.06).move_to([cx, cy, 0])
            t = T(tx, 26, TEXT, weight=BOLD).move_to([cx, cy + 0.88, 0])
            frames.append(f); ttl.append(t)

        rx = VGroup(T("ATP + H₂O", 32, YELLOW), T("→", 32, TEXT), T("ADP + Pi", 32, ORANGE)).arrange(RIGHT, buff=0.35)
        dg = M("ΔG°′ = −30.5 kJ/mol", 28, GREEN)
        rx.move_to([-2.9, 3.1, 0]); dg.move_to([3.4, 3.1, 0])

        def P(label="P", color=YELLOW, w=0.46, fs=22):
            sq = RoundedRectangle(corner_radius=0.08, width=w, height=0.46, stroke_color=color, stroke_width=2.5,
                                  fill_color=color, fill_opacity=0.18)
            return VGroup(sq, T(label, fs, color).move_to(sq))

        def ado():
            return P("Ado", GREY, w=0.8, fs=22)

        def charge(color, r=0.12):
            c = Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_opacity=0)
            return VGroup(c, Line(LEFT * r * 0.55, RIGHT * r * 0.55, color=color, stroke_width=3))

        def arrow_at(x, y, w=0.7):
            return Arrow([x - w / 2, y, 0], [x + w / 2, y, 0], color=GREY, buff=0, stroke_width=4, tip_length=0.2)

        # ---- card 1: charge repulsion
        c1x, c1y = centers[0]
        ry = c1y - 0.12
        a_ado, a_p = ado(), [P(), P(), P()]
        atpG = VGroup(a_ado, *a_p).arrange(RIGHT, buff=0.08).move_to([c1x - 1.7, ry - 0.15, 0])
        minus1 = VGroup(*[charge(RED).next_to(p, UP, buff=0.08) for p in a_p])
        arcs1 = VGroup(*[ArcBetweenPoints(minus1[i].get_top() + UP * 0.03, minus1[i + 1].get_top() + UP * 0.03,
                                          angle=-PI / 1.3, color=RED, stroke_width=3) for i in range(2)])
        cap1a = T("strained", 22, RED).move_to([c1x - 1.7, c1y - 0.88, 0])
        r_ado = ado()
        r_p1, r_p2 = P(color=ORANGE), P(color=ORANGE)
        adpG = VGroup(r_ado, r_p1, r_p2).arrange(RIGHT, buff=0.08)
        piG = P("Pi", ORANGE)
        rightG = VGroup(adpG, piG).arrange(RIGHT, buff=0.35).move_to([c1x + 1.6, ry - 0.15, 0])
        minus1b = VGroup(*[charge(GREEN).next_to(p, UP, buff=0.08) for p in (r_p1, r_p2, piG)])
        cap1b = T("relaxed", 22, GREEN).move_to([c1x + 1.6, c1y - 0.88, 0])
        arr1 = arrow_at(c1x - 0.1, ry - 0.15, 0.45)
        left1 = VGroup(a_ado, *a_p, *minus1)
        right1 = VGroup(r_ado, r_p1, r_p2, piG, *minus1b)

        # ---- card 2: resonance
        c2x, c2y = centers[1]
        ry2 = c2y - 0.12
        lockbox = RoundedRectangle(corner_radius=0.1, width=0.95, height=0.95, stroke_color=GREY, stroke_width=3,
                                   fill_opacity=0).move_to([c2x - 1.7, ry2, 0])
        lockP = P("P", YELLOW).move_to(lockbox)
        cap2a = T("locked in ATP", 22, GREY).move_to([c2x - 1.7, c2y - 0.88, 0])
        arr2 = arrow_at(c2x - 0.1, ry2, 0.6)
        piF = P("Pi", ORANGE, w=0.66).move_to([c2x + 1.4, ry2, 0])
        corners = VGroup(*[Dot(radius=0.075, color=ORANGE).move_to(piF.get_center() + np.array([0.52 * sx, 0.44 * sy, 0]))
                           for sx, sy in [(-1, 1), (1, 1), (1, -1), (-1, -1)]])
        cap2b = T("more resonance forms", 22, GREEN).move_to([c2x + 1.3, c2y - 0.88, 0])

        # ---- card 3: entropy
        c3x, c3y = centers[2]
        ry3 = c3y - 0.12
        one = chip("ATP", YELLOW, size=24, pad=0.13).move_to([c3x - 1.7, ry3, 0])
        arr3 = arrow_at(c3x - 0.45, ry3, 0.7)
        two_a = chip("ADP", ORANGE, size=24, pad=0.13).move_to([c3x + 0.85, ry3 + 0.1, 0])
        two_b = chip("Pi", ORANGE, size=24, pad=0.13).move_to([c3x + 2.25, ry3 - 0.15, 0])
        cap3 = T("one molecule becomes two", 22, GREEN).move_to([c3x, c3y - 0.88, 0])

        # ---- card 4: hydration
        c4x, c4y = centers[3]
        ry4 = c4y - 0.12
        atp4 = chip("ATP", YELLOW, size=24, pad=0.13).move_to([c4x - 2.2, ry4, 0])

        def shell(center, n, a, b, phase=0.0):
            return VGroup(*[Dot(radius=0.07, color=TEAL).move_to(
                center + np.array([a * math.cos(2 * PI * k / n + phase), b * math.sin(2 * PI * k / n + phase), 0]))
                for k in range(n)])
        sh_atp = shell(atp4.get_center(), 3, 0.68, 0.45, 0.4)
        arr4 = arrow_at(c4x - 0.95, ry4, 0.5)
        adp4 = chip("ADP", ORANGE, size=24, pad=0.13).move_to([c4x + 0.5, ry4, 0])
        pi4 = chip("Pi", ORANGE, size=24, pad=0.13).move_to([c4x + 2.2, ry4, 0])
        sh_adp = shell(adp4.get_center(), 8, 0.78, 0.45)
        sh_pi = shell(pi4.get_center(), 6, 0.55, 0.45, 0.3)
        cap4 = T("better solvated by water", 22, GREEN).move_to([c4x, c4y - 0.88, 0])

        # ---- intro
        self.at("ATP hydrolysis", 0.0)
        self.play(FadeIn(rx, shift=UP * 0.1), run_time=0.8)
        self.at("exergonic", 0.2)
        self.play(FadeIn(dg, shift=LEFT * 0.1), run_time=0.8)
        self.at("four distinct effects", 0.2)
        self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.15), run_time=1.2)

        # ---- 1 charge repulsion
        self.at("First, charge repulsion", 0.2)
        self.play(FadeIn(ttl[0]), run_time=0.4)
        self.play(FadeIn(left1), run_time=0.6)
        self.at("closely packed negative charges", 0.2)
        self.play(Create(arcs1), FadeIn(cap1a), run_time=0.9)
        self.at("cutting it apart", 0.2)
        self.play(FadeIn(arr1), FadeOut(arcs1), TransformFromCopy(left1, right1), run_time=1.2)
        self.play(FadeIn(cap1b), run_time=0.4)

        # ---- 2 resonance
        self.at("Second, resonance", 0.2)
        self.play(FadeIn(ttl[1]), FadeIn(lockbox), FadeIn(lockP), FadeIn(cap2a), run_time=0.7)
        self.at("inorganic phosphate has more", 0.2)
        self.play(FadeIn(arr2), FadeIn(piF), FadeIn(corners), FadeIn(cap2b), run_time=0.8)
        self.at("more equivalent resonance forms", 0.0)
        for k in range(4):
            self.play(Indicate(corners[k], color=ORANGE, scale_factor=2.2), run_time=0.45)
        self.at("locked inside ATP", 0.4)
        self.play(Indicate(lockbox, color=GREY, scale_factor=1.1), run_time=0.7)

        # ---- 3 entropy
        self.at("Third, entropy", 0.2)
        self.play(FadeIn(ttl[2]), FadeIn(one), run_time=0.6)
        self.at("one molecule becomes two", 0.2)
        self.play(FadeIn(arr3), TransformFromCopy(one, two_a), TransformFromCopy(one, two_b),
                  FadeIn(cap3), run_time=1.0)
        t0 = self.elapsed()
        for m, ph in [(two_a, 0.0), (two_b, 1.7)]:
            base = m.get_center().copy()
            m.add_updater(lambda mm, base=base, ph=ph: mm.move_to(
                base + np.array([0.12 * math.sin(2.6 * (self.elapsed() - t0) + ph),
                                 0.08 * math.cos(3.1 * (self.elapsed() - t0) + ph), 0])))

        # ---- 4 hydration
        self.at("Fourth, the products", 0.2)
        self.play(FadeIn(ttl[3]), FadeIn(atp4), FadeIn(sh_atp), run_time=0.7)
        self.at("better stabilized by water", 0.2)
        self.play(FadeIn(arr4), TransformFromCopy(atp4, adp4), TransformFromCopy(atp4, pi4), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in [*sh_adp, *sh_pi]], lag_ratio=0.05), FadeIn(cap4),
                  run_time=1.2)

        # ---- no single factor
        self.at("No single factor dominates", 0.2)
        self.play(*[Indicate(f, color=GREY, scale_factor=1.03) for f in frames], run_time=1.4)
        self.at("Together, they make hydrolysis favorable", 0.2)
        self.play(Indicate(dg, color=GREEN, scale_factor=1.15), *[f.animate.set_stroke(GREEN, width=3) for f in frames],
                  run_time=1.2)

        # ---- thermodynamically unstable, kinetically stable
        for mob in (two_a, two_b):
            mob.clear_updaters()
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=0.6)

        y_lo, y_hi = -10, 65
        ax = make_axes(y_lo, y_hi, 7.6, 5.2)
        place_axes(ax, -5.8, -3.2)
        yl = T("free energy", 24, GREY).rotate(PI / 2).move_to([-6.3, -0.6, 0])
        xl = T("reaction coordinate", 24, GREY).move_to([ax.c2p(5, y_lo)[0], -3.55, 0])
        bar = ValueTracker(26.0)                                  # activation barrier height above ATP's level
        f = lambda x: 30 * (1 - sig(x, 7.6, 0.7)) + bar.get_value() * gauss(x, 5.0, 1.1)
        curve = always_redraw(lambda: ax.plot(f, x_range=[0, 10], color=TEXT, stroke_width=6))
        atp_l = mini("ATP + H₂O", YELLOW, 26).move_to(ax.c2p(1.9, 30) + UP * 0.6)
        adp_l = mini("ADP + Pi", ORANGE, 26).move_to(ax.c2p(8.4, -5.5))
        drop = Arrow(ax.c2p(9.8, 30), ax.c2p(9.8, 0), color=GREEN, buff=0, stroke_width=6, tip_length=0.22)
        dg_a = T("ΔG°′ = −30.5", 26, GREEN, weight=BOLD)
        dg_b = T("kJ/mol", 24, GREEN)
        dg_t = VGroup(dg_a, dg_b).arrange(DOWN, buff=0.05, aligned_edge=LEFT).next_to(drop, RIGHT, buff=0.25)
        thermo = VGroup(T("thermodynamically", 26, GREEN), T("unstable", 26, GREEN)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        thermo.next_to(dg_t, DOWN, buff=0.5).align_to(dg_t, LEFT)
        barrier = always_redraw(lambda: Arrow(ax.c2p(5.0, 30), ax.c2p(5.0, 30 + bar.get_value()), color=RED, buff=0,
                                              stroke_width=6, tip_length=0.2))
        kin = T("kinetically stable", 26, RED).move_to([ax.c2p(5.0, 0)[0], 2.45, 0])
        ball = Dot(radius=0.14, color=YELLOW).move_to(ax.c2p(0.4, f(0.4)))

        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.5)
        self.add(curve)
        self.play(FadeIn(atp_l), FadeIn(adp_l), FadeIn(ball), run_time=0.5)
        self.at("thermodynamically unstable", 0.2)
        self.play(GrowArrow(drop), FadeIn(dg_t), FadeIn(thermo), run_time=0.9)
        self.at("kinetically stable", 0.2)
        self.play(FadeIn(kin, shift=DOWN * 0.1), FadeIn(barrier), run_time=0.5)
        self.play(ball.animate.move_to(ax.c2p(3.2, f(3.2))), run_time=0.6)
        self.play(ball.animate.move_to(ax.c2p(0.4, f(0.4))), run_time=0.4)
        self.at("until an enzyme calls on it", 0.5)
        enz = chip("enzyme", TEXT, size=26).move_to(kin)
        self.play(FadeTransform(kin, enz), bar.animate.set_value(5.0), run_time=1.0)
        self.remove(barrier)
        tr = ValueTracker(0.4)
        ball.add_updater(lambda mob: mob.move_to(ax.c2p(tr.get_value(), f(tr.get_value()))))
        self.play(tr.animate.set_value(9.2), run_time=1.5, rate_func=smooth)
        ball.clear_updaters()
        self.finish()


# ----------------------------------------------------------------------------- s04: equilibrium shift
class S04Shift(SpokenScene):
    def construct(self):
        RT = 2.479   # kJ/mol at 25 C
        K0, K1 = 0.001, 267.0
        dG0 = -RT * math.log(K0)       # +17.1
        dG1 = -RT * math.log(K1)       # -13.9

        rxn = VGroup(T("A", 40, BLUE, weight=BOLD), T("⇌", 40, TEXT), T("B", 40, PINK, weight=BOLD)).arrange(RIGHT, buff=0.35)
        rxn.move_to([0, 3.3, 0])

        # particle fields at equilibrium: 1000 A : 1 B   versus   1 A : 267 B (counts follow K = [B]/[A])
        rnd = random.Random(7)

        def field(nA, nB, cols, cx, cy, sp=0.1):
            n = nA + nB
            rows = math.ceil(n / cols)
            cells = [(c, r) for r in range(rows) for c in range(cols)][:n]
            kinds = ["A"] * nA + ["B"] * nB
            rnd.shuffle(kinds)
            dots_, odd = VGroup(), None
            for (c, r), k in zip(cells, kinds):
                p = np.array([cx + (c - (cols - 1) / 2) * sp, cy + (r - (rows - 1) / 2) * sp, 0])
                d = Dot(p, radius=0.034, color=BLUE if k == "A" else PINK)
                dots_.add(d)
                if (k == "B" and nB == 1) or (k == "A" and nA == 1):
                    odd = d
            frame = SurroundingRectangle(dots_, color=GREY, buff=0.12, stroke_width=2)
            return dots_, odd, frame

        fl, oddL, frL = field(999, 1, 40, -3.4, 1.05)
        fr, oddR, frR = field(1, 267, 20, 3.4, 1.05)
        ringL = Circle(radius=0.2, color=TEXT, stroke_width=4).move_to(oddL)
        ringR = Circle(radius=0.2, color=TEXT, stroke_width=4).move_to(oddR)
        cntL = VGroup(T("about 1000 A", 26, BLUE, weight=BOLD), T(":", 26), T("1 B", 26, PINK, weight=BOLD)).arrange(RIGHT, buff=0.2)
        cntR = VGroup(T("1 A", 26, BLUE, weight=BOLD), T(":", 26), T("267 B", 26, PINK, weight=BOLD)).arrange(RIGHT, buff=0.2)
        cntL.move_to([-3.4, 2.8, 0]); cntR.move_to([3.4, 2.8, 0])
        capL = T("A alone", 28, TEXT, weight=BOLD).move_to([-3.4, 3.3, 0])
        capR = T("A coupled to ATP", 28, TEXT, weight=BOLD).move_to([3.4, 3.3, 0])
        keL = M("K = 0.001", 30, TEXT).move_to([-3.4, -0.85, 0])
        dgL = M(f"ΔG°′ ≈ +{dG0:.0f} kJ/mol", 26, RED).move_to([-3.4, -1.45, 0])
        keR = M("K = 267", 30, TEXT).move_to([3.4, -0.85, 0])
        dgR = M(f"ΔG°′ ≈ −{abs(dG1):.0f} kJ/mol", 26, GREEN).move_to([3.4, -1.45, 0])
        nopL = T("almost no product", 26, PINK).move_to([-3.4, -2.2, 0])
        domR = T("product dominates", 26, PINK).move_to([3.4, -2.2, 0])
        atp_use = VGroup(mini("ATP", YELLOW, 28), T("→", 28), mini("ADP + Pi", ORANGE, 28)).arrange(RIGHT, buff=0.25).move_to([3.4, -3.15, 0])
        key = VGroup(VGroup(Dot(radius=0.07, color=BLUE), T("A", 24, BLUE)).arrange(RIGHT, buff=0.12),
                     VGroup(Dot(radius=0.07, color=PINK), T("B", 24, PINK)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.6)
        key.move_to([-3.4, -3.15, 0])

        # ---- intro
        self.at("Here's the payoff of coupling", 0.0)
        self.play(FadeIn(rxn, shift=DOWN * 0.1), run_time=0.8)
        self.at("made quantitative", 0.2)
        self.play(FadeIn(key), run_time=0.6)

        # ---- alone
        self.at("An unfavorable reaction sitting alone", 0.2)
        self.play(FadeIn(capL), Create(frL), FadeIn(fl), run_time=1.0)
        self.at("equilibrium constant of about", 0.2)
        self.play(FadeIn(cntL, shift=DOWN * 0.1), FadeIn(keL, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(dgL, shift=UP * 0.1), run_time=0.6)
        self.at("so almost no product forms", 0.2)
        self.play(FadeIn(nopL), Create(ringL), run_time=1.0)

        # ---- coupled
        self.at("Now couple that same reaction", 0.2)
        self.play(FadeIn(capR), run_time=0.6)
        self.at("to ATP hydrolysis", 0.2)
        self.play(FadeIn(atp_use, shift=UP * 0.1), run_time=0.8)
        self.at("The favorable energy of hydrolysis adds in", 0.2)
        self.play(FadeIn(dgR, shift=UP * 0.1), Indicate(atp_use, color=GREEN, scale_factor=1.1), run_time=1.0)
        self.at("the combined equilibrium constant jumps", 0.2)
        self.play(FadeIn(keR, shift=UP * 0.1), Create(frR), FadeIn(fr), FadeIn(cntR, shift=DOWN * 0.1), run_time=1.0)
        self.at("product now dominates", 0.2)
        self.play(FadeIn(domR), Create(ringR), run_time=1.0)

        # ---- 10^5 on a log axis
        self.at("That's a shift of about", 0.2)
        self.play(*[FadeOut(mob) for mob in (fl, frL, fr, frR, ringL, ringR, cntL, cntR, capL, capR, nopL, domR, atp_use,
                                              key, keL, keR, dgL, dgR, rxn)], run_time=0.6)

        ax_x = -3.0
        yb, yt = -2.5, 2.3           # log10 K = -3 .. +3
        ly = lambda logk: yb + (logk + 3) / 6 * (yt - yb)
        axis = Line([ax_x, yb - 0.1, 0], [ax_x, yt + 0.1, 0], color=GREY, stroke_width=3)
        ticks, tl = VGroup(), VGroup()
        for lk, lab in [(-3, "1/1000"), (0, "1"), (3, "1000")]:
            ticks.add(Line([ax_x - 0.12, ly(lk), 0], [ax_x + 0.12, ly(lk), 0], color=GREY, stroke_width=3))
            tl.add(M(lab, 24, GREY).next_to([ax_x - 0.2, ly(lk), 0], LEFT, buff=0.1))
        ktitle = T("equilibrium constant K", 24, GREY).rotate(PI / 2).move_to([-6.4, -0.1, 0])
        fav = T("favors B", 26, PINK).move_to([ax_x, yt + 0.55, 0])
        unf = T("favors A", 26, BLUE).move_to([ax_x, yb - 0.6, 0])
        p0 = Dot(radius=0.17, color=RED).move_to([ax_x, ly(math.log10(K0)), 0])
        p1 = Dot(radius=0.17, color=GREEN).move_to([ax_x, ly(math.log10(K1)), 0])
        k0l = M("K = 0.001", 26, RED).next_to(p0, RIGHT, buff=0.3)
        k0s = T("A alone", 24, RED).next_to(k0l, RIGHT, buff=0.25)
        k1l = M("K = 267", 26, GREEN).next_to(p1, RIGHT, buff=0.3)
        k1s = T("coupled to ATP", 24, GREEN).next_to(k1l, RIGHT, buff=0.25)
        span = DoubleArrow([2.1, p0.get_center()[1], 0], [2.1, p1.get_center()[1], 0], color=YELLOW,
                           buff=0, stroke_width=5, tip_length=0.22)
        big = VGroup(T("about 10⁵-fold", 38, YELLOW, weight=BOLD),
                     VGroup(M("267 / 0.001", 26, TEXT), M("≈ 2.7 × 10⁵", 26, TEXT)).arrange(DOWN, buff=0.12)
                     ).arrange(DOWN, buff=0.25)
        big.move_to([4.35, -0.1, 0])

        self.play(Create(axis), Create(ticks), FadeIn(tl), FadeIn(ktitle), FadeIn(fav), FadeIn(unf), run_time=0.6)
        self.play(FadeIn(p0, scale=0.5), FadeIn(k0l), FadeIn(k0s), run_time=0.4)
        self.play(FadeIn(p1, scale=0.5), FadeIn(k1l), FadeIn(k1s), run_time=0.4)
        self.at("a hundred thousand fold change", 0.4)
        self.play(GrowFromCenter(span), FadeIn(big[0], shift=LEFT * 0.1), run_time=0.9)
        self.play(FadeIn(big[1]), run_time=0.6)

        # ---- ATP as the coupling agent
        self.at("This single idea", 0.2)
        marker = Dot(radius=0.2, color=YELLOW).move_to(p0)
        pull = mini("ATP", YELLOW, 30, pad=0.18)
        self.play(Indicate(p0, color=RED, scale_factor=1.6), run_time=0.8)
        pull.next_to(marker, LEFT, buff=1.5)
        self.at("why ATP", 0.2)
        self.play(FadeIn(marker, scale=0.5), FadeIn(pull, scale=0.7), run_time=0.6)
        self.at("universal coupling agent", 0.2)
        self.play(Indicate(pull, color=YELLOW, scale_factor=1.2), run_time=0.9)
        self.at("Spending one phosphin hydride bond", 0.2)
        pull.add_updater(lambda mob: mob.next_to(marker, LEFT, buff=1.5))
        self.play(marker.animate.move_to(p1), run_time=2.2, rate_func=smooth)
        pull.clear_updaters()
        self.at("all the way to completion", 0.0)
        self.play(Indicate(p1, color=GREEN, scale_factor=1.6), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------- s05: energy charge
class S05Charge(SpokenScene):
    def construct(self):
        a = ValueTracker(0.0)    # ATP (relative units)
        d = ValueTracker(0.0)    # ADP
        m = ValueTracker(0.0)    # AMP

        def ec():
            A, D, Mm = a.get_value(), d.get_value(), m.get_value()
            tot = A + D + Mm
            return (A + 0.5 * D) / tot if tot > 1e-6 else 0.0

        # ---- gauge (semicircle, 0 on the left, 1 on the right)
        GC = np.array([-3.2, -1.0, 0])
        R = 2.8
        ang = lambda v: PI * (1 - v)
        pt = lambda v, r: GC + r * np.array([math.cos(ang(v)), math.sin(ang(v)), 0])
        segs = VGroup()
        N = 40
        for i in range(N):
            v0, v1 = i / N, (i + 1) / N
            vm = (v0 + v1) / 2
            col = interpolate_color(ManimColor(RED), ManimColor(GREEN), min(1, max(0, (vm - 0.55) / 0.25)))
            segs.add(Arc(radius=R, start_angle=ang(v0), angle=-(ang(v0) - ang(v1)), arc_center=GC, color=col, stroke_width=24))
        ticks = VGroup(); tlabs = VGroup()
        for v in (0, 0.5, 1):
            ticks.add(Line(pt(v, R - 0.32), pt(v, R + 0.32), color=TEXT, stroke_width=3))
            tlabs.add(M(f"{v:g}", 26, TEXT).move_to(pt(v, R + 0.65)))
        needle = always_redraw(lambda: Line(GC, pt(ec(), R - 0.28), color=YELLOW, stroke_width=7))
        hub = Dot(GC, radius=0.14, color=YELLOW)
        g_title = T("ENERGY CHARGE", 28, TEXT, weight=BOLD).move_to([GC[0], 3.15, 0])
        readout = always_redraw(lambda: M(f"{ec():.2f}", 44, YELLOW, weight=BOLD).move_to(GC + DOWN * 0.95))

        show_normal = ValueTracker(0.0)    # switched on for the final "balancing" beat

        def state():
            e = ec()
            if show_normal.get_value() > 0.5 and 0.84 <= e <= 0.91:
                return T("normally held near 0.85–0.90", 26, GREEN)
            if e > 0.88:
                return T("loaded with ATP", 26, GREEN)
            if e < 0.7:
                return T("depleted", 26, RED)
            return T(" ", 26, GREY)
        state_lab = always_redraw(lambda: state().move_to(GC + DOWN * 1.65))

        # ---- formula
        fA = T("ATP", 30, YELLOW, weight=BOLD)
        fD = T("ADP", 30, ORANGE, weight=BOLD)
        fM = T("AMP", 30, PURPLE, weight=BOLD)
        EC_t = T("EC", 32, TEXT, weight=BOLD)
        eqs = T("=", 32)
        num = VGroup(fA.copy(), T("+ ½", 30), fD.copy()).arrange(RIGHT, buff=0.15)
        den = VGroup(fA.copy(), T("+", 30), fD.copy(), T("+", 30), fM.copy()).arrange(RIGHT, buff=0.15)
        bar_l = Line(LEFT, RIGHT, color=TEXT, stroke_width=3).set_width(den.width + 0.2)
        frac = VGroup(num, bar_l, den).arrange(DOWN, buff=0.14)
        formula = VGroup(EC_t, eqs, frac).arrange(RIGHT, buff=0.25).move_to([3.3, 2.5, 0])

        # ---- adenylate pool bars (relative amounts)
        BX = {"ATP": 1.4, "ADP": 3.3, "AMP": 5.2}
        BASE = -1.7
        SC = 0.5   # world units per relative unit

        def bar(key, col, tr):
            return always_redraw(lambda: Rectangle(width=1.1, height=max(0.02, tr.get_value() * SC), stroke_color=col,
                                                   stroke_width=2, fill_color=col, fill_opacity=0.85)
                                 .move_to([BX[key], BASE + max(0.02, tr.get_value() * SC) / 2, 0]))
        bA, bD, bM = bar("ATP", YELLOW, a), bar("ADP", ORANGE, d), bar("AMP", PURPLE, m)
        base_line = Line([0.5, BASE, 0], [6.1, BASE, 0], color=GREY, stroke_width=3)
        lA = T("ATP", 26, YELLOW).move_to([BX["ATP"], BASE - 0.4, 0])
        lD = T("ADP", 26, ORANGE).move_to([BX["ADP"], BASE - 0.4, 0])
        lM = T("AMP", 26, PURPLE).move_to([BX["AMP"], BASE - 0.4, 0])
        pool_brace = Brace(VGroup(lA, lM), DOWN, color=GREY, buff=0.05)
        pool_t = T("adenylate pool", 26, GREY).next_to(pool_brace, DOWN, buff=0.1)

        # ---- flux panel (appears later)
        FX0, FX1 = 0.9, 6.1

        def flux(y, color, f):
            def build():
                s = f(ec())
                h = 0.12 + 0.62 * s
                body = Rectangle(width=FX1 - FX0 - 0.55, height=h, stroke_width=0, fill_color=color, fill_opacity=0.35 + 0.6 * s)
                body.move_to([(FX0 + FX1 - 0.55) / 2, y, 0])
                hh = max(0.4, h + 0.25) / 2
                tip = Polygon([FX1 - 0.55, y + hh, 0], [FX1 - 0.55, y - hh, 0], [FX1, y, 0], stroke_width=0,
                              fill_color=color, fill_opacity=0.35 + 0.6 * s)
                return VGroup(body, tip)
            return always_redraw(build)
        s_cat = lambda e: min(1, max(0, (0.97 - e) / 0.22))
        s_ana = lambda e: min(1, max(0, (e - 0.75) / 0.22))
        fcat = flux(1.0, GREEN, s_cat)
        fana = flux(-1.5, RED, s_ana)
        cat_t = T("catabolism: makes ATP", 26, GREEN).move_to([3.5, 1.9, 0])
        ana_t = T("anabolism: spends ATP", 26, RED).move_to([3.5, -0.6, 0])

        # ---- intro
        self.at("The cell monitors its own energy state", 0.0)
        self.play(Create(segs), run_time=1.2)
        self.at("energy charge", 0.2)
        self.play(FadeIn(g_title), Create(ticks), FadeIn(tlabs), run_time=0.8)
        self.at("fuel gauge running from zero to one", 0.3)
        a.set_value(0.0); d.set_value(1.0); m.set_value(4.0)   # EC low -> needle starts at the left
        self.add(needle, hub)
        self.play(FadeIn(hub), run_time=0.3)
        self.play(a.animate.set_value(10), d.animate.set_value(0.0), m.animate.set_value(0.0), run_time=1.8, rate_func=smooth)

        # ---- formula
        self.at("The formula weights ATP", 0.2)
        self.play(FadeIn(EC_t), FadeIn(eqs), FadeIn(bar_l), FadeIn(num[0]), run_time=0.8)
        self.at("and ADP half", 0.2)
        self.play(FadeIn(num[1]), FadeIn(num[2]), run_time=0.6)
        self.at("divides by the total adenylate pool", 0.2)
        self.play(FadeIn(den), run_time=0.8)

        # healthy pool
        self.at("so a cell loaded with ATP", 0.2)
        self.add(base_line, bA, bD, bM)
        self.play(FadeIn(base_line), FadeIn(lA), FadeIn(lD), FadeIn(lM), FadeIn(pool_brace), FadeIn(pool_t), run_time=0.4)
        self.play(a.animate.set_value(7.0), d.animate.set_value(1.0), m.animate.set_value(0.2), run_time=1.2)
        self.add(readout, state_lab)
        self.at("reads near the top", 0.2)
        self.play(Indicate(needle, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("a depleted cell reads low", 0.2)
        self.play(a.animate.set_value(2.0), d.animate.set_value(2.2), m.animate.set_value(1.8), run_time=1.8)

        # ---- regulation
        self.at("This single value governs flux", 0.2)
        self.play(FadeOut(formula), FadeOut(bar_l), FadeOut(base_line), FadeOut(lA), FadeOut(lD), FadeOut(lM),
                  FadeOut(pool_brace), FadeOut(pool_t), FadeOut(bA), FadeOut(bD), FadeOut(bM), run_time=0.8)
        self.play(FadeIn(cat_t), FadeIn(ana_t), FadeIn(fcat), FadeIn(fana), run_time=0.9)
        self.at("When the charge is high", 0.2)
        self.play(a.animate.set_value(7.0), d.animate.set_value(1.0), m.animate.set_value(0.2), run_time=1.6)
        self.at("throttles down catabolic", 0.2)
        self.play(Indicate(cat_t, color=GREEN, scale_factor=1.08), run_time=1.0)
        self.at("turns up anabolic", 0.2)
        self.play(Indicate(ana_t, color=RED, scale_factor=1.08), run_time=1.0)
        self.at("When the charge falls", 0.2)
        self.play(a.animate.set_value(2.0), d.animate.set_value(2.2), m.animate.set_value(1.8), run_time=1.8)
        self.at("it does the reverse", 0.2)
        self.play(Indicate(cat_t, color=GREEN, scale_factor=1.08), Indicate(ana_t, color=RED, scale_factor=1.08), run_time=1.0)
        self.at("master signal", 0.2)
        self.play(Indicate(g_title, color=YELLOW, scale_factor=1.12), Indicate(needle, color=YELLOW), run_time=0.8)
        self.at("balancing energy production", 0.2)
        show_normal.set_value(1.0)
        self.play(a.animate.set_value(7.5), d.animate.set_value(1.5), m.animate.set_value(0.5), run_time=1.8)
        self.finish()


# ----------------------------------------------------------------------------- end
class S06End(EndCard):
    LINE = "Coupling to ATP lets the cell pay for what it builds."
