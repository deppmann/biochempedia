"""Where the nitrogen goes  (Biochemistrypedia explainer, lesson: protein turnover and amino acid catabolism)

Timed to the SPOKEN words (audio/words.json, from the real slide audio): every self.at("phrase") waits
until the narrator starts that phrase, minus a short lead.

COLOR MAP (one color per concept, whole video)
  PURPLE = the nitrogen itself: the round "N" tokens that hop from carrier to carrier
  BLUE   = the nitrogen CARRIERS: glutamate, alanine, glutamine
  YELLOW = the CARBON side: carbon skeletons, pyruvate, glucose, the TCA wheel
  RED    = free ammonia (toxic), and stop / blocked
  GREEN  = urea and the urea cycle (the safe end point)
  ORANGE = the shared intermediates that link the two wheels (fumarate, aspartate)
  GREY   = compartments, frame, structure, de-emphasized labels
No molecular structures are drawn: molecules are labelled chips; nitrogen is a purple "N" token.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F2994A"


# ---------------------------------------------------------------- helpers
def arrow(a, b, color=GREY, w=3.5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.3,
                 tip_length=tip)


def heading(text, size=36):
    return T(text, size, font=TITLE_FONT).to_edge(UP, buff=0.4)


def ndot(r=0.27):
    """The nitrogen token: a purple disc with an N."""
    return VGroup(Circle(radius=r, stroke_width=0, fill_color=PURPLE, fill_opacity=1.0),
                  T("N", 22, BG, weight=BOLD))


def akg_chip(size=30, color=YELLOW, pad=0.22):
    """chip("α-ketoglutarate") with the α set in Georgia: Avenir Next's α reads as a plain "a"."""
    label = Text("α-ketoglutarate", font=FONT, font_size=size, color=color, t2f={"α": TITLE_FONT})
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    return VGroup(box, label.move_to(box))


def pulse(mob, s=1.4):
    """Grow and shrink back without recoloring (Indicate would paint the N letter the disc color)."""
    return mob.animate(rate_func=there_and_back).scale(s)


def at_pt(mob, p):
    mob.move_to([p[0], p[1], 0])
    return mob


def hop(dot, target, angle=-PI / 3):
    """MoveAlongPath that carries a token along a shallow arc to `target`."""
    t = np.array([target[0], target[1], 0.0])
    return MoveAlongPath(dot, ArcBetweenPoints(dot.get_center(), t, angle=angle))


def pt(x, y):
    return np.array([x, y, 0.0])


class Spin:
    """Dots circling a ring at an adjustable speed (deg/s), clockwise."""

    def __init__(self, scene, c, R, n=3, color=BLUE, speed=70, r=0.12, phase0=90):
        self.phase = ValueTracker(0)
        self.speed = ValueTracker(speed)
        self.driver = Mobject()
        self.driver.add_updater(lambda m, dt: self.phase.increment_value(self.speed.get_value() * dt))
        self.dots = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
        for i, d in enumerate(self.dots):
            d.add_updater(lambda m, i=i: m.move_to(
                pt(c[0] + R * math.cos(math.radians(phase0 - self.phase.get_value() - (360 / n) * i)),
                   c[1] + R * math.sin(math.radians(phase0 - self.phase.get_value() - (360 / n) * i)))))
        scene.add(self.driver, self.dots)

    def stop(self):
        self.speed.set_value(0)


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Protein turnover and amino acid catabolism"
    TITLE = "Where the nitrogen goes"


# --------------------------------------------------------------------------------------------
class S01Split(SpokenScene):
    """An amino acid has two problems: carbon (fuel) and nitrogen (toxic). Split them; track the N."""

    def construct(self):
        head = heading("Every amino acid has two fates")
        cx = -3.5
        carbon = chip("carbon skeleton", YELLOW, 28).move_to([cx, -1.25, 0])
        nblk = chip("amino N", PURPLE, 28).move_to([cx, -0.48, 0])
        lab_aa = T("amino acid", 28, GREY).move_to([cx, 0.3, 0])
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.5)

        # --- the amino acid is one block: a carbon skeleton carrying an amino nitrogen
        self.at("amino acid")
        self.play(FadeIn(carbon, shift=UP * 0.1), FadeIn(nblk, shift=DOWN * 0.1), FadeIn(lab_aa), run_time=0.9)
        self.at("two separate problems")
        self.play(Indicate(carbon, color=YELLOW, scale_factor=1.1), run_time=0.6)
        self.play(Indicate(nblk, color=PURPLE, scale_factor=1.1), run_time=0.6)

        # --- problem 1: the carbon skeleton is fuel
        self.at("carbon skeleton")
        self.play(Indicate(carbon, color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.at("burned in the TCA cycle")
        d1 = chip("burned in the TCA cycle", YELLOW, 28).move_to([-0.6, -0.6, 0], aligned_edge=LEFT)
        a1 = arrow(carbon.get_right(), d1.get_left(), YELLOW)
        self.play(GrowArrow(a1), FadeIn(d1, shift=RIGHT * 0.2), run_time=0.8)
        self.at("rebuilt into glucose")
        d2 = chip("rebuilt: glucose, fatty acids", YELLOW, 28).move_to([-0.6, -2.0, 0], aligned_edge=LEFT)
        a2 = arrow(carbon.get_right(), d2.get_left(), YELLOW)
        self.play(GrowArrow(a2), FadeIn(d2, shift=RIGHT * 0.2), run_time=0.8)

        # --- problem 2: the nitrogen is a liability (free ammonia is toxic)
        self.at("liability")
        self.play(Indicate(nblk, color=PURPLE, scale_factor=1.15), run_time=0.8)
        self.at("Free ammonia is toxic")
        tox = T("free ammonia: toxic", 28, RED).move_to([cx, 0.3, 0])
        self.play(FadeOut(lab_aa), FadeIn(tox), nblk[0].animate.set_stroke(RED).set_fill(RED, opacity=0.25),
                  run_time=0.6)
        self.play(Indicate(nblk, color=RED, scale_factor=1.15), run_time=0.8)

        # --- so the cell splits the molecule: the nitrogen lifts off into its own lane
        self.at("splits the molecule")
        lane_y = 1.7
        n_tok = ndot().move_to([-5.45, lane_y, 0])
        self.play(nblk.animate.move_to([cx, lane_y, 0]), FadeOut(tox), run_time=0.9)
        self.play(Transform(nblk, n_tok), run_time=0.6)
        divider = DashedLine([-6.2, 0.55, 0], [6.2, 0.55, 0], color=GREY, stroke_width=2.5, dash_length=0.12)
        self.play(Create(divider), run_time=0.6)

        # --- nitrogen lane: glutamate -> blood (alanine, glutamine) -> liver -> urea cycle -> urine
        names = [("glutamate", BLUE), ("blood", TEXT), ("liver", TEXT), ("urea cycle", GREEN), ("urine", TEXT)]
        chips = [chip(n, c, 28) for n, c in names]
        lane = VGroup(*chips).arrange(RIGHT, buff=0.6).move_to([-4.85, lane_y, 0], aligned_edge=LEFT)
        arrows = [arrow(chips[i].get_right(), chips[i + 1].get_left(), PURPLE) for i in range(len(chips) - 1)]
        sub = T("alanine, glutamine", 26, BLUE).next_to(chips[1], DOWN, buff=0.18)

        self.at("collected onto glutamate")
        self.play(FadeIn(chips[0], shift=RIGHT * 0.2), run_time=0.5)
        self.play(hop(nblk, chips[0].get_top() + UP * 0.32), run_time=0.7)
        self.at("through the blood")
        self.play(GrowArrow(arrows[0]), FadeIn(chips[1], shift=RIGHT * 0.2), run_time=0.5)
        self.play(hop(nblk, chips[1].get_top() + UP * 0.32), run_time=0.7)
        self.at("alanine and glutamine")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)
        self.at("funneled to the liver")
        self.play(GrowArrow(arrows[1]), FadeIn(chips[2], shift=RIGHT * 0.2), run_time=0.5)
        self.play(hop(nblk, chips[2].get_top() + UP * 0.32), run_time=0.7)
        self.at("urea cycle")
        self.play(GrowArrow(arrows[2]), FadeIn(chips[3], shift=RIGHT * 0.2), run_time=0.5)
        self.play(hop(nblk, chips[3].get_top() + UP * 0.32), run_time=0.7)
        self.at("excreted in urine")
        self.play(GrowArrow(arrows[3]), FadeIn(chips[4], shift=RIGHT * 0.2), run_time=0.5)
        self.play(hop(nblk, chips[4].get_top() + UP * 0.32), run_time=0.7)

        # --- the two summaries
        self.at("Carbon can be burned or rebuilt")
        b1 = chip("carbon: burn or rebuild", YELLOW, 28)
        b2 = chip("nitrogen: collect, transport, excrete", PURPLE, 28)
        banner = VGroup(b1, b2).arrange(RIGHT, buff=0.35).move_to([0, -3.15, 0])
        fit(banner, max_w=12.4)
        self.play(FadeIn(b1, shift=UP * 0.15), Indicate(d1, color=YELLOW), Indicate(d2, color=YELLOW), run_time=0.9)
        self.at("Nitrogen must be collected")
        self.play(FadeIn(b2, shift=UP * 0.15), run_time=0.9)
        self.at("Keeping these two fates separate")
        self.play(Indicate(divider, color=TEXT), run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S02Twosteps(SpokenScene):
    """Step 1 transamination funnels N onto glutamate; step 2 deamination frees ammonia."""

    def construct(self):
        head = heading("Two moves strip the nitrogen")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.6)

        # ---- the amino acid column
        names = ["alanine", "aspartate", "leucine", "valine"]
        ys = [0.45, 1.35, -0.45, -1.35]
        col_x = -3.2
        aas = [chip(n, TEXT, 28, pad=0.16).move_to([col_x, y, 0]) for n, y in zip(names, ys)]
        dots = [ndot().move_to(a.get_right() + RIGHT * 0.3) for a in aas]
        self.at("amino acid")
        self.play(FadeIn(aas[0], shift=RIGHT * 0.2), FadeIn(dots[0], scale=0.6), run_time=0.7)

        # ---- step 1
        self.at("Step one is transamination")
        step1 = heading("Step 1: transamination")
        self.play(Transform(head, step1), run_time=0.7)
        self.at("amino transferase")
        tag = chip("aminotransferase", GREY, 26, pad=0.14).move_to([-0.6, 2.4, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.6)
        self.at("many different amino acids")
        self.play(*[FadeIn(a, shift=RIGHT * 0.2) for a in aas[1:]], *[FadeIn(d, scale=0.6) for d in dots[1:]],
                  run_time=0.9)
        self.at("alpha ketoglutarate")
        hub = akg_chip(30).move_to([2.55, 0, 0])
        self.play(FadeIn(hub, shift=LEFT * 0.2), run_time=0.6)
        arrs = [arrow(d.get_right(), hub.get_left() + np.array([0, 0.18 * (1.5 - i) * 1.0, 0]), GREY, 3)
                for i, d in enumerate(dots)]
        self.play(*[GrowArrow(a) for a in arrs], run_time=0.5)
        self.at("collecting all that nitrogen")
        landing = hub.get_top() + UP * 0.28
        flights = []
        for i, d in enumerate(dots):
            flights.append(AnimationGroup(hop(d, landing + RIGHT * (0.62 * (i - 1.5)), angle=-PI / 4),
                                          aas[i].animate.set_color(GREY).set_opacity(0.45), lag_ratio=0.0))
        self.play(LaggedStart(*flights, lag_ratio=0.3), run_time=2.0)
        self.at("single carrier")
        self.play(Indicate(hub, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("glutamate")
        glu = chip("glutamate", BLUE, 30).move_to(hub.get_center())
        carried = ndot().move_to(glu.get_corner(UR) + np.array([-0.05, 0.12, 0]))
        self.play(Transform(hub, glu), *[FadeOut(d) for d in dots], FadeIn(carried, scale=0.6), run_time=0.8)
        self.at("reversible")
        rev = VGroup(DoubleArrow(LEFT * 0.45, RIGHT * 0.45, color=TEXT, stroke_width=4, buff=0,
                                 tip_length=0.18), T("reversible", 28, TEXT)).arrange(RIGHT, buff=0.25)
        rev.move_to([2.55, -0.95, 0])
        self.play(FadeIn(rev, shift=UP * 0.1), run_time=0.6)
        self.at("one channel")
        one = T("many inputs, one channel", 28, GREY).move_to([2.55, -1.75, 0])
        self.play(FadeIn(one, shift=UP * 0.1), *[Indicate(a, color=PURPLE) for a in arrs], run_time=1.0)

        # ---- step 2: clear the stage; glutamate moves left
        self.at("Step two is oxidative deamination")
        step2 = heading("Step 2: oxidative deamination", 36)
        stage1 = VGroup(*aas, *arrs, tag, rev, one)
        self.play(FadeOut(stage1), Transform(head, step2), run_time=0.9)
        pair = VGroup(hub, carried)
        self.play(pair.animate.shift(LEFT * 6.35), run_time=0.8)
        amm = chip("free ammonia (NH₄⁺)", RED, 30).move_to([3.45, 0, 0])
        a_main = arrow(pt(-2.0, 0), amm.get_left(), TEXT, 4)
        self.at("Glutamate dehydrogenase")
        gdh = chip("glutamate dehydrogenase", GREY, 26, pad=0.14).move_to([-0.1, 1.15, 0])
        self.play(FadeIn(gdh, shift=DOWN * 0.1), GrowArrow(a_main), run_time=0.8)
        self.at("releases the nitrogen")
        self.play(hop(carried, [-0.1, 0.0], angle=-PI / 3), run_time=0.8)
        self.at("free ammonia")
        self.play(hop(carried, amm.get_left() + LEFT * 0.35, angle=-PI / 4), FadeIn(amm, scale=0.8), run_time=0.8)
        self.play(FadeOut(carried), run_time=0.3)
        self.at("regenerating")
        kg = akg_chip(30).move_to(hub.get_center())
        self.play(Transform(hub, kg), run_time=0.8)
        self.at("to do it all again")
        loop = ArcBetweenPoints(hub.get_bottom() + RIGHT * 0.7 + DOWN * 0.05, hub.get_bottom() + LEFT * 0.7 + DOWN * 0.05,
                                angle=-PI * 0.9, color=YELLOW, stroke_width=4)
        loop.add_tip(tip_length=0.2, tip_width=0.2)
        again = T("ready for more nitrogen", 26, GREY).next_to(loop, DOWN, buff=0.15)
        self.play(Create(loop), FadeIn(again), run_time=1.0)

        # ---- reversible, with the urea cycle pulling the ammonia off
        # lay out the real equilibrium: glutamate <-> alpha-ketoglutarate + NH4+ (alpha-KG is a product, not the substrate)
        self.at("can run both ways")
        glu2 = chip("glutamate", BLUE, 30).move_to(hub.get_center())
        plus = T("+", 40, GREY).move_to([3.45, 0.84, 0])
        self.play(FadeOut(loop), FadeOut(again), hub.animate.scale(26 / 30).move_to([3.45, 1.6, 0]),
                  FadeIn(glu2), FadeIn(plus), gdh.animate.move_to([-0.9, 1.15, 0]), run_time=0.9)
        a_back = arrow(amm.get_left() + LEFT * 0.1 + DOWN * 0.45, pt(-2.0, -0.45), TEXT, 4)
        both = T("the reaction runs both ways", 28, TEXT).move_to([0.5, -1.05, 0])
        self.play(GrowArrow(a_back), FadeIn(both, shift=UP * 0.1), run_time=0.9)
        self.at("the urea cycle")
        urea = chip("urea cycle (liver)", GREEN, 28).move_to([3.45, -2.55, 0])
        draw = arrow(amm.get_bottom(), urea.get_top(), GREEN, 4)
        self.play(FadeIn(urea, shift=UP * 0.1), GrowArrow(draw), run_time=0.8)
        self.at("drawing the ammonia off")
        pulled = ndot().move_to(amm.get_bottom())
        self.play(FadeIn(pulled, scale=0.6), run_time=0.25)
        self.play(pulled.animate.move_to(urea.get_top() + UP * 0.35), run_time=0.9)
        self.play(FadeOut(pulled), Indicate(urea, color=GREEN, scale_factor=1.1), run_time=0.4)
        self.at("so the nitrogen flows")
        net = T("net flow: toward disposal", 28, TEXT).move_to([0.5, -1.05, 0])
        self.play(a_main.animate.set_stroke(width=9), a_back.animate.set_stroke(width=2).set_opacity(0.4),
                  Transform(both, net), run_time=0.9)
        self.play(Indicate(urea, color=GREEN, scale_factor=1.12), run_time=0.8)

        # ---- recap row
        self.at("Many amino acids in")
        self.play(FadeOut(VGroup(hub, glu2, plus, amm, a_main, a_back, gdh, both, urea, draw)),
                  Transform(head, heading("Many in, two moves, ammonia out")), run_time=0.6)
        r1 = chip("amino acids", TEXT, 28)
        r2 = chip("glutamate", BLUE, 28)
        r3 = chip("free ammonia", RED, 28)
        r4 = chip("to the liver", TEXT, 28)
        row = VGroup(r1, r2, r3, r4).arrange(RIGHT, buff=0.8).move_to([0, -0.2, 0])
        fit(row, max_w=12.2)
        links = [arrow(row[i].get_right(), row[i + 1].get_left(), GREY, 4) for i in range(3)]
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.6)
        self.at("two moves", nth=1)
        self.play(GrowArrow(links[0]), FadeIn(r2, shift=LEFT * 0.1), run_time=0.7)
        self.play(GrowArrow(links[1]), FadeIn(r3, shift=LEFT * 0.1), run_time=0.7)
        n1 = T("move 1", 26, GREY).move_to([links[0].get_center()[0], row.get_top()[1] + 0.45, 0])
        n2 = T("move 2", 26, GREY).move_to([links[1].get_center()[0], row.get_top()[1] + 0.45, 0])
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.5)
        self.at("ready to be packaged")
        self.play(GrowArrow(links[2]), FadeIn(r4, shift=LEFT * 0.1), run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------------------------
class S03Alanine(SpokenScene):
    """Muscle -> blood -> liver: alanine carries N one way, glucose carries fuel back."""

    def construct(self):
        head = heading("The glucose-alanine cycle")
        BW, BH, CY = 3.8, 4.9, -0.15
        mus = RoundedRectangle(corner_radius=0.2, width=BW, height=BH, stroke_color=GREY, stroke_width=3
                               ).move_to([-4.3, CY, 0])
        liv = RoundedRectangle(corner_radius=0.2, width=BW, height=BH, stroke_color=GREY, stroke_width=3
                               ).move_to([4.3, CY, 0])
        mus_l = T("skeletal muscle", 28, TEXT).move_to([-4.3, 2.05, 0])
        liv_l = T("liver", 28, TEXT).move_to([4.3, 2.05, 0])
        Y_ALA, Y_GLC = -0.4, -1.55
        self.at("Working muscle")
        self.play(FadeIn(head, shift=DOWN * 0.15), Create(mus), FadeIn(mus_l), run_time=0.9)
        self.at("nitrogen home")
        blood_l = T("blood", 28, GREY).move_to([0, 1.0, 0])
        lane_a = arrow(pt(-2.35, Y_ALA), pt(2.35, Y_ALA), GREY, 2.5)
        lane_g = arrow(pt(2.35, Y_GLC), pt(-2.35, Y_GLC), GREY, 2.5)
        self.play(Create(liv), FadeIn(liv_l), FadeIn(blood_l), GrowArrow(lane_a), GrowArrow(lane_g), run_time=1.1)

        # ---- in muscle: amino acids -> N onto pyruvate -> alanine
        self.at("As muscle breaks down amino acids")
        aa = chip("amino acids", TEXT, 28).move_to([-4.3, 1.0, 0])
        n_tok = ndot().move_to(aa.get_top() + np.array([0.7, 0.18, 0]))
        self.play(FadeIn(aa, shift=DOWN * 0.1), FadeIn(n_tok, scale=0.6), run_time=0.8)
        self.at("transaminates")
        ttag = T("transamination", 26, GREY).move_to([-4.3, 0.38, 0])
        self.play(FadeIn(ttag), run_time=0.5)
        self.at("onto pyruvate")
        pyr = chip("pyruvate", YELLOW, 28).move_to([-4.3, Y_ALA, 0])
        self.play(FadeIn(pyr, shift=UP * 0.1), hop(n_tok, pyr.get_right() + np.array([0.36, 0.0, 0]), angle=-PI / 3),
                  run_time=0.9)
        self.at("to make alanine")
        ala = chip("alanine", BLUE, 28).move_to(pyr.get_center())
        self.play(Transform(pyr, ala), FadeOut(ttag), aa.animate.set_opacity(0.35), run_time=0.8)
        self.at("non toxic")
        nt = T("non-toxic", 26, GREY).move_to([-4.3, -0.98, 0])
        self.play(FadeIn(nt, shift=UP * 0.1), run_time=0.6)

        # ---- alanine rides the blood to the liver
        self.at("through the blood")
        sign_a = T("alanine →", 26, BLUE).move_to([0, 0.2, 0])
        grp = VGroup(pyr, n_tok)
        self.play(FadeOut(nt), FadeIn(sign_a), grp.animate.shift(RIGHT * 8.6), run_time=2.0)
        # the group moved as one: pyr center now at liver

        # ---- liver strips the nitrogen, urea cycle takes it, leftover pyruvate -> glucose
        self.at("strips the nitrogen")
        pyr2 = chip("pyruvate", YELLOW, 28).move_to(pyr.get_center())
        urea = chip("urea cycle", GREEN, 28).move_to([4.3, 0.75, 0])
        self.play(Transform(pyr, pyr2), run_time=0.5)
        self.at("feeding it into the urea cycle")
        self.play(FadeIn(urea, shift=DOWN * 0.1), hop(n_tok, urea.get_top() + np.array([0.0, 0.2, 0]),
                                                      angle=PI / 3), run_time=1.0)
        self.at("converts the leftover pyruvate")
        glc = chip("glucose", YELLOW, 28).move_to([4.3, Y_GLC, 0])
        down = arrow(pyr.get_bottom(), glc.get_top(), YELLOW, 3)
        self.play(GrowArrow(down), FadeIn(glc, shift=UP * 0.15), pyr.animate.set_opacity(0.4), run_time=1.0)

        # ---- glucose returns to muscle as fuel
        self.at("glucose returns")
        sign_g = T("← glucose", 26, YELLOW).move_to([0, -2.1, 0])
        self.play(FadeIn(sign_g), glc.animate.move_to([-4.3, Y_GLC, 0]), FadeOut(down), run_time=1.6)
        self.at("as fuel")
        fuel = T("fuel", 28, YELLOW).move_to([-4.3, -2.2, 0])
        self.play(FadeIn(fuel, shift=UP * 0.1), Indicate(glc, color=YELLOW), run_time=0.8)

        # ---- the two shuttles, opposite directions
        self.at("alanine is the nitrogen shuttle")
        c1 = chip("alanine = nitrogen shuttle", BLUE, 28)
        c2 = chip("glucose = energy shuttle", YELLOW, 28)
        shut = VGroup(c1, c2).arrange(RIGHT, buff=0.35).move_to([0, -3.15, 0])
        fit(shut, max_w=12.4)
        self.play(FadeIn(c1, shift=UP * 0.15), Indicate(sign_a, color=BLUE, scale_factor=1.25), run_time=0.9)
        self.at("glucose is the energy shuttle")
        self.play(FadeIn(c2, shift=UP * 0.15), Indicate(sign_g, color=YELLOW, scale_factor=1.25), run_time=0.9)
        self.at("opposite directions")
        ga = chip("alanine", BLUE, 26, pad=0.12).move_to([-1.9, Y_ALA, 0])
        gg = chip("glucose", YELLOW, 26, pad=0.12).move_to([1.9, Y_GLC, 0])
        self.add(ga, gg)
        self.play(ga.animate.move_to([1.9, Y_ALA, 0]), gg.animate.move_to([-1.9, Y_GLC, 0]), run_time=1.8)
        self.play(FadeOut(ga), FadeOut(gg), run_time=0.3)
        self.at("offloads its waste nitrogen")
        self.play(Indicate(mus, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.at("round trip")
        self.play(Indicate(lane_a, color=BLUE), Indicate(lane_g, color=YELLOW), run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S04Glutamine(SpokenScene):
    """Glutamine: abundant, carries two N, delivered to liver / kidney / gut + immune cells."""

    def construct(self):
        head = heading("Glutamine, the nitrogen courier")

        # ---- the courier
        gln = chip("glutamine", BLUE, 34, pad=0.3).move_to([0, 0.2, 0])
        d1, d2 = ndot(), ndot()
        d1.move_to(gln.get_top() + np.array([-0.55, 0.25, 0]))
        d2.move_to(gln.get_top() + np.array([0.55, 0.25, 0]))
        self.play(FadeIn(head, shift=DOWN * 0.15), FadeIn(gln, scale=0.85), run_time=0.6)
        self.at("workhorse of nitrogen transport")
        self.play(FadeIn(d1, scale=0.6), FadeIn(d2, scale=0.6), run_time=0.5)
        self.play(Indicate(gln, color=BLUE, scale_factor=1.1), run_time=0.7)

        # ---- the most abundant free amino acid in blood: relative bars (approximate plasma values)
        self.at("most abundant")
        self.play(FadeOut(gln), FadeOut(d1), FadeOut(d2), run_time=0.3)
        data = [("glutamine", 600, BLUE), ("alanine", 350, GREY), ("glycine", 250, GREY), ("valine", 230, GREY),
                ("proline", 200, GREY), ("lysine", 180, GREY), ("serine", 120, GREY), ("leucine", 120, GREY)]
        x0, scale = -2.6, 5.4 / 600
        bars, names = [], []
        for i, (n, v, c) in enumerate(data):
            y = 1.95 - i * 0.55
            r = Rectangle(width=v * scale, height=0.38, stroke_width=0, fill_color=c, fill_opacity=0.9 if c == BLUE else 0.55)
            r.move_to([x0 + v * scale / 2, y, 0])
            t = T(n, 24, BLUE if c == BLUE else TEXT).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            bars.append(r)
            names.append(t)
        axis = Line([x0, 2.3, 0], [x0, 2.3 - 8 * 0.55 + 0.1, 0], color=GREY, stroke_width=3)
        caption = T("free amino acids in blood plasma (relative, approximate)", 26, GREY).move_to([0.2, -2.75, 0])
        self.play(Create(axis), *[FadeIn(n) for n in names], *[GrowFromEdge(b, LEFT) for b in bars],
                  FadeIn(caption, shift=UP * 0.1), run_time=0.8)
        mm = M("≈ 0.6 mM", 24, BLUE).next_to(bars[0], RIGHT, buff=0.2)
        self.at("in your blood")
        self.play(FadeIn(mm), Indicate(bars[0], color=BLUE, scale_factor=1.05), run_time=0.6)

        # ---- made everywhere: a second amino group goes onto glutamate
        # the chart stays up through "Tissues everywhere" (it was on screen ~1 s); cross-fade on the next words
        glu = chip("glutamate", BLUE, 32, pad=0.26).move_to([-1.0, 0.1, 0])
        g1 = ndot().move_to(glu.get_top() + np.array([0, 0.28, 0]))
        tis = T("tissues everywhere", 28, GREY).move_to([-1.0, -1.45, 0])
        g2 = ndot().move_to([-5.4, 1.4, 0])
        lab2 = T("amino group", 28, PURPLE).next_to(g2, UP, buff=0.18)
        self.at("Tissues everywhere", lead=-0.4)
        self.play(FadeOut(VGroup(*bars, *names, axis, caption, mm)),
                  FadeIn(glu, shift=UP * 0.1), FadeIn(g1, scale=0.6), FadeIn(tis), run_time=0.5)
        self.at("a second amino group")
        self.play(FadeIn(g2, scale=0.6), FadeIn(lab2), run_time=0.4)
        self.at("onto glutamate")
        self.play(hop(g2, glu.get_top() + np.array([1.0, 0.28, 0]), angle=-PI / 5), FadeOut(lab2), run_time=1.0)
        self.at("make glutamine")
        gln2 = chip("glutamine", BLUE, 32, pad=0.26).move_to(glu.get_center())
        self.play(Transform(glu, gln2), g1.animate.move_to(gln2.get_top() + np.array([-0.6, 0.28, 0])),
                  g2.animate.move_to(gln2.get_top() + np.array([0.6, 0.28, 0])), FadeOut(tis), run_time=0.9)
        self.at("two nitrogens")
        self.play(pulse(g1), pulse(g2), run_time=1.0)
        self.at("without toxicity")
        safe = T("non-toxic", 28, GREY).move_to([-1.0, -1.5, 0])
        self.play(FadeIn(safe, shift=UP * 0.1), run_time=0.6)

        # ---- delivery
        self.at("The bloodstream")
        src = VGroup(glu, g1, g2)
        self.play(FadeOut(safe), src.animate.move_to([-4.3, 0.2, 0]), run_time=0.9)
        blood = T("in the blood", 28, GREY).next_to(glu, DOWN, buff=0.45)
        self.play(FadeIn(blood), run_time=0.4)
        rows = [("liver", "urea synthesis", GREEN, 1.9), ("kidney", "acid-base balance", TEXT, 0.3),
                ("gut and immune cells", "fuel, building block", YELLOW, -1.3)]
        row_objs = {}

        def add_row(i, t_name):
            name, desc, dc, y = rows[i]
            c = chip(name, TEXT, 32).move_to([0.0, y, 0], aligned_edge=LEFT)
            a = arrow(glu.get_right() + RIGHT * 0.05, c.get_left(), BLUE, 3)
            d = T(desc, 28, dc).move_to([c.get_left()[0] + 0.1, y - 0.62, 0], aligned_edge=LEFT)
            row_objs[i] = (c, a, d) if i < 2 else (c, a)
            return c, a, d

        self.at("The liver")
        c, a, d = add_row(0, "liver")
        self.play(GrowArrow(a), FadeIn(c, shift=RIGHT * 0.2), run_time=0.7)
        self.play(FadeIn(d, shift=RIGHT * 0.1), run_time=0.5)
        self.at("the kidney")
        c, a, d = add_row(1, "kidney")
        self.play(GrowArrow(a), FadeIn(c, shift=RIGHT * 0.2), run_time=0.7)
        self.play(FadeIn(d, shift=RIGHT * 0.1), run_time=0.5)
        self.at("rapidly dividing cells")
        c, a, d = add_row(2, "gut")
        self.play(GrowArrow(a), FadeIn(c, shift=RIGHT * 0.2), run_time=0.7)
        d_fuel = T("fuel", 28, YELLOW)
        d_bb = T("building block", 28, YELLOW)
        d_fuel.move_to([c.get_left()[0] + 0.1, rows[2][3] - 0.62, 0], aligned_edge=LEFT)
        d_bb.move_to([c.get_left()[0] + 0.1, rows[2][3] - 1.07, 0], aligned_edge=LEFT)
        self.at("as fuel")
        self.play(FadeIn(d_fuel, shift=RIGHT * 0.1), run_time=0.5)
        self.at("building block")
        self.play(FadeIn(d_bb, shift=RIGHT * 0.1), run_time=0.6)

        # ---- ammonia is not moved freely; nitrogen travels as glutamine
        self.at("Ammonia is toxic")
        every = VGroup(src, blood, *[o for t in row_objs.values() for o in t], d_fuel, d_bb)
        self.play(FadeOut(every), run_time=0.7)
        amm = chip("free ammonia", RED, 30).move_to([-3.6, 1.0, 0])
        bl = chip("blood", TEXT, 30).move_to([3.8, 0.0, 0])
        a_x = arrow(amm.get_right(), bl.get_top() + LEFT * 0.4, RED, 4)
        cross = VGroup(Line(UL * 0.3, DR * 0.3, color=RED, stroke_width=8), Line(UR * 0.3, DL * 0.3, color=RED, stroke_width=8))
        cross.move_to(a_x.point_from_proportion(0.5))
        self.play(FadeIn(amm, shift=RIGHT * 0.2), FadeIn(bl), run_time=0.7)
        self.at("so the body almost never moves it freely")
        self.play(GrowArrow(a_x), run_time=0.6)
        self.play(FadeIn(cross, scale=1.4), run_time=0.4)
        self.at("Most nitrogen travels as glutamine")
        gl3 = chip("glutamine", BLUE, 30).move_to([-3.6, -1.0, 0])
        k1 = ndot(0.24).move_to(gl3.get_top() + np.array([-0.5, 0.22, 0]))
        k2 = ndot(0.24).move_to(gl3.get_top() + np.array([0.5, 0.22, 0]))
        a_ok = arrow(gl3.get_right(), bl.get_bottom() + LEFT * 0.4, BLUE, 6)
        self.play(FadeIn(gl3, shift=RIGHT * 0.2), FadeIn(k1, scale=0.6), FadeIn(k2, scale=0.6), run_time=0.7)
        self.play(GrowArrow(a_ok), run_time=0.7)
        self.at("the safe")
        row_t = T("safe      abundant      two nitrogens", 30, TEXT).move_to([0, -2.75, 0])
        assert len(row_t) == 24, len(row_t)
        t1, t2, t3 = row_t[0:4], row_t[4:12], row_t[12:24]
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.4)
        self.at("abundant", nth=1)
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.4)
        self.at("two nitrogen")
        self.play(FadeIn(t3, shift=UP * 0.1), pulse(k1), pulse(k2), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S05Bicycle(SpokenScene):
    """Two wheels, one chain: urea cycle + TCA cycle linked by fumarate and aspartate."""

    def construct(self):
        head = heading("The Krebs bicycle")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.6)
        box = RoundedRectangle(corner_radius=0.25, width=12.2, height=5.7, stroke_color=TEXT, stroke_width=2.5
                               ).move_to([0, -0.6, 0])
        box.set_stroke(opacity=0.5)
        liv = T("liver", 28, TEXT).move_to([-5.4, 1.8, 0])
        self.at("liver's chemistry")
        self.play(Create(box), FadeIn(liv), run_time=1.0)
        HL, HR, R = pt(-3.2, -0.45), pt(3.2, -0.45), 1.5
        ST, HT, BB = pt(-1.9, 1.9), pt(1.9, 1.9), pt(0.0, 0.25)
        fcol = GREY
        frame = VGroup(Line(HL, ST), Line(ST, HT), Line(HT, HR), Line(ST, BB), Line(BB, HT), Line(HL, BB),
                       Line(ST + LEFT * 0.35, ST + RIGHT * 0.3 + UP * 0.12), Line(HT, HT + RIGHT * 0.55 + UP * 0.1)
                       ).set_stroke(color=fcol, width=5, opacity=0.55)
        crank = Circle(radius=0.28, color=fcol, stroke_width=4).move_to(BB).set_stroke(opacity=0.7)

        self.at("Picture a bicycle")
        self.play(Create(frame, lag_ratio=0.15), Create(crank), run_time=0.9)
        self.at("two wheels")
        ring_l = Circle(radius=R, color=GREY, stroke_width=6).move_to(HL)
        ring_r = Circle(radius=R, color=GREY, stroke_width=6).move_to(HR)
        self.play(Create(ring_l), Create(ring_r), run_time=0.8)
        self.at("share a chain")
        ch1 = DashedLine(pt(-1.7, -1.5), pt(1.7, -1.5), color=ORANGE, stroke_width=4, dash_length=0.14)
        ch2 = DashedLine(pt(-1.7, -0.8), pt(1.7, -0.8), color=ORANGE, stroke_width=4, dash_length=0.14)
        self.play(Create(ch1), Create(ch2), run_time=0.9)

        # ---- the wheels get names
        self.at("urea cycle")
        self.play(ring_l.animate.set_color(GREEN), run_time=0.5)
        lab_l = T("urea\ncycle", 28, GREEN, weight=BOLD).move_to(HL + DOWN * 0.6)
        self.play(FadeIn(lab_l), run_time=0.5)
        self.at("TCA cycle")
        self.play(ring_r.animate.set_color(YELLOW), run_time=0.5)
        lab_r = T("TCA\ncycle", 28, YELLOW, weight=BOLD).move_to(HR + DOWN * 0.6)
        self.play(FadeIn(lab_r), run_time=0.5)

        # ---- shared intermediates on the chain
        self.at("fumarate")
        fum = chip("fumarate", ORANGE, 26, pad=0.14).move_to([0, -1.5, 0])
        self.play(FadeOut(ch1), FadeIn(fum, scale=0.8), run_time=0.4)
        a_f = arrow(pt(-1.7, -1.5), fum.get_left(), ORANGE, 4)
        a_f2 = arrow(fum.get_right(), pt(1.7, -1.5), ORANGE, 4)
        self.play(GrowArrow(a_f), GrowArrow(a_f2), run_time=0.4)
        self.at("aspartate")
        asp = chip("aspartate", ORANGE, 26, pad=0.14).move_to([0, -0.8, 0])
        self.play(FadeOut(ch2), FadeIn(asp, scale=0.8), run_time=0.4)
        a_a = arrow(pt(1.7, -0.8), asp.get_right(), ORANGE, 4)
        a_a2 = arrow(asp.get_left(), pt(-1.7, -0.8), ORANGE, 4)
        self.play(GrowArrow(a_a), GrowArrow(a_a2), run_time=0.5)

        # ---- pedal: both wheels turn together
        self.at("When you pedal")
        sp_l = Spin(self, HL, R, n=3, color=PURPLE, speed=0, r=0.13)
        sp_r = Spin(self, HR, R, n=3, color=YELLOW, speed=0, r=0.13)
        pedal = Line(BB, BB + UP * 0.5, color=TEXT, stroke_width=6)
        ph = ValueTracker(0)
        pedal.add_updater(lambda m: m.put_start_and_end_on(BB, pt(0.5 * math.sin(math.radians(ph.get_value())) + 0.0,
                                                               0.25 + 0.5 * math.cos(math.radians(ph.get_value())))))
        drv = Mobject()
        drv.add_updater(lambda m, dt: ph.increment_value(sp_l.speed.get_value() * dt * 1.0))
        self.add(drv, pedal)
        sp_l.speed.set_value(80)
        sp_r.speed.set_value(80)
        self.at("both wheels turn together")
        self.wait(1.0)

        # ---- urea out one side, glucose-building carbon out the other
        self.at("Urea comes out")
        urea = chip("urea", GREEN, 30).move_to([-3.6, -2.95, 0])
        a_u = arrow(HL + DOWN * (R + 0.02), urea.get_top(), GREEN, 5)
        self.play(GrowArrow(a_u), FadeIn(urea, shift=DOWN * 0.1), run_time=0.8)
        waste = T("nitrogen waste", 26, GREEN).next_to(urea, RIGHT, buff=0.25)
        self.at("nitrogen waste product")
        self.play(FadeIn(waste, shift=RIGHT * 0.1), run_time=0.6)
        self.at("and glucose building carbon")
        glc = chip("glucose-building carbon", YELLOW, 26).move_to([3.5, -2.95, 0])
        a_g = arrow(HR + DOWN * (R + 0.02) + RIGHT * 0.6, glc.get_top() + LEFT * 0.4, YELLOW, 5)
        self.play(GrowArrow(a_g), FadeIn(glc, shift=DOWN * 0.1), run_time=0.8)

        # ---- the liver runs both wheels at once
        self.at("The liver runs both wheels")
        self.play(Indicate(box, color=TEXT, scale_factor=1.01), Indicate(liv, color=TEXT), run_time=1.0)
        self.at("Dispose of nitrogen as urea")
        self.play(Indicate(urea, color=GREEN, scale_factor=1.2), run_time=0.9)
        self.at("reclaiming carbon")
        self.play(Indicate(glc, color=YELLOW, scale_factor=1.07), run_time=0.9)
        self.at("Nitrogen out one side")
        self.play(Indicate(urea, color=GREEN, scale_factor=1.2), run_time=0.9)
        self.at("glucose out the other")
        self.play(Indicate(glc, color=YELLOW, scale_factor=1.07), run_time=0.9)
        self.at("one connected machine")
        self.play(Indicate(box, color=TEXT, scale_factor=1.01), run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S06End(EndCard):
    LINE = "Collect the nitrogen, ship it safely, burn or rebuild the carbon."
