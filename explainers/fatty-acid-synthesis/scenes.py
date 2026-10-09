"""Fatty acid synthesis: building fat, two carbons at a time  (Biochemistrypedia explainer)

Timed to the SPOKEN words (audio/words.json, from the real slide audio): every self.at("phrase") waits
until the narrator starts that phrase, minus a short lead.

COLOR MAP (one color per concept, whole video)
  BLUE    = enzymes (ATP-citrate lyase, acetyl CoA carboxylase, fatty acid synthase)
  YELLOW  = acetyl CoA, the two-carbon units, and the growing fatty-acid chain made of them
  GREEN   = malonyl CoA (the activated three-carbon extender)   [also Stage 2 tab]
  RED     = CO2 and bicarbonate (the carbon we pay for and then throw away)
  TEAL    = ATP (energy paid)
  PURPLE  = biotin, the CO2 carrier
  ORANGE  = citrate (the shuttle carrier)                         [also Stage 1 tab]
  GOLD    = the decision / drive: committed step, regulation valve, the CO2-driven push
  GREY    = structure, axes, de-emphasized labels
No molecular structures are drawn: everything is labelled chips, blocks, arrows, a lever and schematic energy levels.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
PURPLE = "#B58CD9"


# ---------------------------------------------------------------- helpers
def arrow(a, b, color=GREY, w=4, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.3,
                 tip_length=tip)


def heading(text, size=36):
    return T(text, size, font=TITLE_FONT).to_edge(UP, buff=0.4)


def P(c, R, deg):
    a = math.radians(deg)
    return np.array([c[0] + R * math.cos(a), c[1] + R * math.sin(a), 0.0])


def block(color=YELLOW, w=0.5):
    return Square(side_length=w, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.4)


def hco3(size=26):
    return chip("HCO₃⁻", RED, size=size, pad=0.16)


def co2(size=24):
    return chip("CO₂", RED, size=size, pad=0.14)


def atp(size=26):
    return chip("ATP", TEAL, size=size, pad=0.16)


def acetyl(size=28, label="acetyl CoA"):
    return chip(label, YELLOW, size=size)


def malonyl(size=28, label="malonyl CoA"):
    return chip(label, GREEN, size=size)


def chip2(lines, color=BLUE, size=26, pad=0.22, fill_opacity=0.16):
    """Chip with centered multi-line label."""
    label = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.08)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill_opacity)
    return VGroup(box, label.move_to(box))


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Fatty acid synthesis"
    TITLE = "Building fat, two carbons at a time"


# --------------------------------------------------------------------------------------------
class S01Stages(SpokenScene):
    """Three stages: transport (citrate leaves the mitochondrion, lyase frees acetyl CoA), activation
    (ACC makes malonyl CoA, the committed step), elongation (FAS cycles to C16); then the logic of the order."""

    def construct(self):
        specs = [("1  Transport", ORANGE), ("2  Activation", GREEN), ("3  Elongation", YELLOW)]
        tabs = VGroup(*[chip(n, c, size=30) for n, c in specs]).arrange(RIGHT, buff=0.45).move_to([0, 3.05, 0])

        def bar_at(i, y_off=0.14):
            t = tabs[i]
            return Line([t.get_left()[0], t.get_bottom()[1] - y_off, 0], [t.get_right()[0], t.get_bottom()[1] - y_off, 0],
                        color=specs[i][1], stroke_width=7)

        self.at("three stages")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tabs], lag_ratio=0.3), run_time=1.1)

        # ---------------- stage 1: transport
        self.at("Stage 1")
        bar = bar_at(0)
        mito = RoundedRectangle(corner_radius=0.3, width=5.0, height=4.2, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([-3.7, -0.6, 0])
        mito_l = T("mitochondrion", 26, GREY).move_to(mito.get_bottom() + UP * 0.4)
        cyto = RoundedRectangle(corner_radius=0.3, width=6.2, height=4.2, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.04).move_to([3.0, -0.6, 0])
        cyto_l = T("cytoplasm", 26, GREY).move_to(cyto.get_bottom() + UP * 0.4)
        citrate = chip("citrate", ORANGE, 30).move_to([-3.7, 0.2, 0])
        self.play(Create(bar), FadeIn(mito), FadeIn(mito_l), FadeIn(cyto), FadeIn(cyto_l), FadeIn(citrate), run_time=1.0)
        self.at("ATP citrate lyase")
        lyase = chip("ATP-citrate lyase", BLUE, 28).move_to([3.0, 0.85, 0])
        self.play(citrate.animate.move_to([3.0, -0.05, 0]), FadeIn(lyase, shift=DOWN * 0.2), run_time=1.3)
        self.at("cleaves citrate")
        ac = acetyl(30).move_to([1.6, -1.15, 0])
        oaa = chip("oxaloacetate", GREY, 28).move_to([4.5, -1.15, 0])
        self.play(FadeOut(citrate, scale=0.6), FadeIn(ac, shift=LEFT * 0.4), FadeIn(oaa, shift=RIGHT * 0.4), run_time=0.8)
        self.at("deliver acetyl CoA")
        self.play(Indicate(ac, color=YELLOW, scale_factor=1.2), run_time=0.9)
        self.at("into the cytoplasm")
        ring = SurroundingRectangle(cyto, color=ORANGE, buff=0.06, corner_radius=0.3, stroke_width=4)
        self.play(Create(ring), run_time=0.7)

        # ---------------- stage 2: activation
        self.at("Stage 2")
        st1 = VGroup(mito, mito_l, cyto, cyto_l, lyase, ac, oaa, ring)
        self.play(FadeOut(st1), Transform(bar, bar_at(1)), run_time=0.7)
        ac2 = acetyl(28, "acetyl CoA (2C)").move_to([-4.4, -0.5, 0])
        self.at("Activation")
        self.play(FadeIn(ac2, shift=RIGHT * 0.3), run_time=0.6)
        self.at("The committed step")
        tag = chip("committed step", GOLD, 28).move_to([0, -2.4, 0])
        self.play(FadeIn(tag, shift=UP * 0.2), run_time=0.6)
        self.at("Acetyl CoA carboxylase")
        acc = chip("acetyl CoA carboxylase", BLUE, 24).move_to([-0.1, -0.5, 0])
        a1 = arrow(ac2.get_right() + RIGHT * 0.05, acc.get_left(), GREY)
        self.play(FadeIn(acc, scale=0.8), GrowArrow(a1), run_time=0.8)
        self.at("spends an ATP")
        at = atp(28).move_to([-0.9, 1.3, 0])
        cg = hco3(26).move_to([0.9, 1.3, 0])
        d1 = arrow(at.get_bottom(), acc.get_top() + LEFT * 0.7, TEAL, 3)
        d2 = arrow(cg.get_bottom(), acc.get_top() + RIGHT * 0.7, RED, 3)
        self.play(FadeIn(at, shift=DOWN * 0.2), GrowArrow(d1), run_time=0.7)
        self.play(FadeIn(cg, shift=DOWN * 0.2), GrowArrow(d2), run_time=0.6)
        self.at("to make malonyl CoA")
        mal = malonyl(28, "malonyl CoA (3C)").move_to([4.3, -0.5, 0])
        a2 = arrow(acc.get_right(), mal.get_left(), GREY)
        self.play(GrowArrow(a2), FadeIn(mal, shift=RIGHT * 0.3), run_time=0.8)
        self.at("locking the cell into building fat")
        self.play(Indicate(tag, color=GOLD, scale_factor=1.2), run_time=0.9)
        self.play(tag[0].animate.set_fill(GOLD, opacity=0.4), run_time=0.3)

        # ---------------- stage 3: elongation
        self.at("Stage 3")
        st2 = VGroup(ac2, tag, acc, a1, at, cg, d1, d2, mal, a2)
        self.play(FadeOut(st2), Transform(bar, bar_at(2)), run_time=0.7)
        C = np.array([-3.3, -0.7, 0])
        RR = 1.8
        names = ["C", "R", "D", "R"]
        angs = [90, 0, -90, 180]
        arcs = VGroup(*[
            Arc(radius=RR, start_angle=math.radians(a - 22), angle=-math.radians(46), arc_center=C, color=GREY,
                stroke_width=5).add_tip(tip_length=0.2, tip_width=0.2)
            for a in angs])
        nodes = VGroup(*[VGroup(Circle(radius=0.34, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1),
                                 T(n, 30, GREY, weight=BOLD)).move_to(P(C, RR, a)) for n, a in zip(names, angs)])
        for nd in nodes:
            nd[1].move_to(nd[0])
        nodes.set_z_index(3)
        fas = chip2(["fatty acid", "synthase"], BLUE, 28).move_to(C)
        self.at("Fatty acid synthase")
        self.play(FadeIn(fas, scale=0.8), run_time=0.7)
        self.at("four step cycle")
        self.play(Create(arcs, lag_ratio=0.2), FadeIn(nodes), run_time=1.0)
        dot = Dot(radius=0.14, color=YELLOW).move_to(P(C, RR, 90))
        k = [1]
        counter = always_redraw(lambda: VGroup(M(str(2 * k[0]), 44, YELLOW), T("carbons", 30, GREY))
                                .arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([3.75, 0.85, 0]))
        slots = [np.array([1.5 + 0.6 * i, -0.55, 0]) for i in range(8)]
        blocks = [block(YELLOW, 0.5).move_to(s) for s in slots]
        chain_l = T("the growing chain", 26, GREY).move_to([3.75, 1.75, 0])
        self.at("over and over")
        self.play(FadeIn(dot), FadeIn(chain_l), FadeIn(counter), FadeIn(blocks[0], scale=0.6), run_time=0.5)
        for i in range(1, 8):
            k[0] = i + 1
            self.play(UpdateFromAlphaFunc(dot, lambda m, a: m.move_to(P(C, RR, 90 - 360 * a))),
                      FadeIn(blocks[i], scale=0.5, shift=DOWN * 0.3), run_time=0.42, rate_func=linear)
        self.at("palmitate")
        pal = chip("palmitate", YELLOW, 30).move_to([3.75, -2.2, 0])
        br = Brace(VGroup(*blocks), DOWN, buff=0.15, color=YELLOW)
        self.play(FadeIn(pal, shift=UP * 0.2), GrowFromCenter(br), Indicate(counter, color=YELLOW), run_time=1.0)

        # ---------------- the logic of the order
        self.at("Notice the logic")
        st3 = VGroup(fas, arcs, nodes, dot, chain_l, counter, pal, br, *blocks)
        caps_txt = ["get the bricks\nto the site", "commit\nirreversibly", "then\nbuild"]
        self.play(FadeOut(st3), FadeOut(bar), tabs.animate.move_to([0, 0.7, 0]), run_time=0.9)
        caps = VGroup(*[T(t, 28, c, line_spacing=0.9).next_to(tabs[i], DOWN, buff=0.45)
                        for i, (t, c) in enumerate(zip(caps_txt, [ORANGE, GREEN, YELLOW]))])
        for cp in caps[1:]:
            cp.set_y(caps[0].get_y())
        self.at("get the bricks")
        self.play(FadeIn(caps[0], shift=UP * 0.15), run_time=0.7)
        self.at("commit irreversibly")
        self.play(FadeIn(caps[1], shift=UP * 0.15), run_time=0.7)
        self.at("then build")
        self.play(FadeIn(caps[2], shift=UP * 0.15), run_time=0.7)
        for i in range(3):
            self.at(["transport", "activation", "elongation"][i], nth=1)
            self.play(Indicate(tabs[i], color=specs[i][1], scale_factor=1.12), run_time=0.7)
        self.at("in that order")
        arrs = VGroup(arrow(tabs[0].get_right(), tabs[1].get_left(), TEXT, 4, 0.2),
                      arrow(tabs[1].get_right(), tabs[2].get_left(), TEXT, 4, 0.2))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.5), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S02Commit(SpokenScene):
    """ACC: acetyl CoA + bicarbonate + ATP -> malonyl CoA (committed); biotin as a swinging arm carrying CO2;
    one-way arrow; regulation valve."""

    def construct(self):
        head = heading("The decision point")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.8)

        # ---------------- phase 1: the reaction
        self.at("Acetyl CoA carboxylase")
        acc = chip("ACC", BLUE, 32).move_to([-1.6, 0.1, 0])
        acc_l = T("acetyl CoA carboxylase", 24, BLUE).next_to(acc, DOWN, buff=0.25)
        self.play(FadeIn(acc, scale=0.8), FadeIn(acc_l), run_time=0.7)
        self.at("takes acetyl CoA")
        ac = acetyl(28).move_to([-5.0, 0.1, 0])
        a1 = arrow(ac.get_right(), acc.get_left(), GREY)
        self.play(FadeIn(ac, shift=RIGHT * 0.3), GrowArrow(a1), run_time=0.7)
        self.at("bicarbonate")
        hc = hco3(28).move_to([-2.5, 2.0, 0])
        d1 = arrow(hc.get_bottom(), acc.get_top() + LEFT * 0.3, RED, 3)
        self.play(FadeIn(hc, shift=DOWN * 0.2), GrowArrow(d1), run_time=0.6)
        self.at("and ATP")
        at = atp(28).move_to([-0.7, 2.0, 0])
        d2 = arrow(at.get_bottom(), acc.get_top() + RIGHT * 0.3, TEAL, 3)
        self.play(FadeIn(at, shift=DOWN * 0.2), GrowArrow(d2), run_time=0.6)
        self.at("produces malonyl CoA")
        mal = malonyl(28).move_to([1.8, 0.1, 0])
        a2 = arrow(acc.get_right(), mal.get_left(), GREY)
        adp = T("ADP + Pᵢ", 26, GREY).move_to([-1.6, -1.15, 0])
        d3 = arrow(acc.get_bottom(), [-1.6, -0.85, 0], GREY, 3)
        self.play(GrowArrow(a2), FadeIn(mal, shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeOut(acc_l), FadeIn(adp, shift=DOWN * 0.2), GrowArrow(d3), run_time=0.5)
        self.at("This is the committed step")
        tag = chip("committed step", GOLD, 30).move_to([-1.6, -2.75, 0])
        brace = Brace(VGroup(ac, mal), DOWN, buff=1.05, color=GOLD)
        self.play(FadeIn(tag, shift=UP * 0.2), GrowFromCenter(brace), run_time=0.8)
        self.at("making fat and nothing else")
        fat = chip("fat", YELLOW, 28).move_to([5.4, 0.1, 0])
        a3 = arrow(mal.get_right(), fat.get_left(), YELLOW, 6)
        self.play(GrowArrow(a3), FadeIn(fat, shift=RIGHT * 0.3), run_time=0.9)

        # ---------------- phase 2: biotin, a swinging arm
        self.at("The enzyme depends on biotin")
        ph1 = VGroup(acc, ac, a1, hc, d1, at, d2, mal, a2, adp, d3, tag, brace, a3, fat)
        blob = RoundedRectangle(corner_radius=0.35, width=8.0, height=3.6, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.10).move_to([0, -1.4, 0])
        blob_l = T("acetyl CoA carboxylase", 24, BLUE).move_to([-1.9, 0.05, 0])
        slotA = RoundedRectangle(corner_radius=0.15, width=2.9, height=1.0, stroke_color=GREY, stroke_width=2.5,
                                 fill_opacity=0).move_to([-2.5, -2.4, 0])
        slotA.move_to([-2.4, -2.4, 0])
        slotB = slotA.copy().move_to([2.4, -2.4, 0])
        hcA = hco3(24).move_to(slotA.get_center() + LEFT * 0.7)
        atA = atp(24).move_to(slotA.get_center() + RIGHT * 0.65)
        acB = acetyl(26).move_to(slotB)
        PIV = np.array([0.0, -0.3, 0.0])
        TIPA, TIPB = np.array([-2.4, -1.15, 0.0]), np.array([2.4, -1.15, 0.0])
        angA = math.atan2(TIPA[1] - PIV[1], TIPA[0] - PIV[0])
        angB = math.atan2(TIPB[1] - PIV[1], TIPB[0] - PIV[0])
        Larm = float(np.linalg.norm(TIPA - PIV))
        ang = ValueTracker(angA)

        def tip():
            a = ang.get_value()
            return PIV + Larm * np.array([math.cos(a), math.sin(a), 0])

        arm = always_redraw(lambda: Line(PIV, tip(), color=PURPLE, stroke_width=9))
        tipdot = always_redraw(lambda: Dot(tip(), radius=0.2, color=PURPLE))
        pivot = Dot(PIV, radius=0.14, color=GREY)
        biotin_l = T("biotin: a vitamin cofactor", 26, PURPLE).move_to([0, -3.65, 0])
        self.play(FadeOut(ph1), Transform(head, heading("Biotin: the CO₂ carrier")), FadeIn(blob), FadeIn(blob_l),
                  FadeIn(slotA), FadeIn(slotB), FadeIn(hcA), FadeIn(atA), FadeIn(acB), run_time=1.1)
        self.at("biotin", nth=0)
        self.play(FadeIn(pivot), Create(arm), FadeIn(tipdot), run_time=0.6)
        self.at("a vitamin cofactor")
        self.play(FadeIn(biotin_l, shift=UP * 0.15), run_time=0.7)
        self.at("carry carbon dioxide")
        self.play(Transform(biotin_l, T("biotin: carries CO₂", 26, PURPLE).move_to(biotin_l)),
                  Indicate(hcA, color=RED, scale_factor=1.2), run_time=0.8)
        self.at("swinging arm")
        self.play(ang.animate.set_value(angA + 0.18), run_time=0.45)
        self.play(ang.animate.set_value(angA), run_time=0.45)
        self.at("grabs a carboxyl group")
        cg = co2(26).move_to(TIPA + UP * 0.42)
        adpA = T("ADP + Pᵢ", 22, GREY).move_to(atA)
        self.play(ReplacementTransform(hcA, cg), Transform(atA, adpA), run_time=0.6)
        cg.add_updater(lambda m: m.move_to(tip() + UP * 0.42))
        self.at("delivers it")
        self.play(ang.animate.set_value(angB), run_time=1.1, rate_func=smooth)
        cg.clear_updaters()
        mal2 = malonyl(26).move_to(slotB)
        self.play(cg.animate.move_to(acB.get_top() + UP * 0.05).scale(0.7), run_time=0.3)
        self.play(FadeOut(cg), ReplacementTransform(acB, mal2), run_time=0.4)

        # ---------------- phase 3: irreversible, so this is where regulation sits
        self.at("committed and irreversible")
        s_ac = acetyl(26).move_to([-5.0, 2.45, 0])
        s_mal = malonyl(26).move_to([-1.2, 2.45, 0])
        s_a = arrow(s_ac.get_right(), s_mal.get_left(), TEXT, 5)
        back = DashedLine(s_mal.get_left() + DOWN * 0.9, s_ac.get_right() + DOWN * 0.9, color=GREY, stroke_width=4, dash_length=0.14)
        back.add_tip(tip_length=0.2, tip_width=0.2)
        x = Cross(Square(side_length=0.4), stroke_color=RED, stroke_width=6).move_to(back.get_center())
        irrev = T("irreversible", 24, GOLD).next_to(x, DOWN, buff=0.12)
        self.play(Transform(head, heading("Irreversible, so regulated here")),
                  FadeIn(s_ac), FadeIn(s_mal), GrowArrow(s_a), run_time=0.7)
        self.at("irreversible")
        self.play(Create(back), Create(x), FadeIn(irrev), run_time=0.8)
        self.at("exactly where regulation should sit")
        wheel = VGroup(Circle(radius=0.5, stroke_color=GOLD, stroke_width=5),
                       Line(UP * 0.5, DOWN * 0.5, color=GOLD, stroke_width=5), Line(LEFT * 0.5, RIGHT * 0.5, color=GOLD, stroke_width=5))
        wheel.move_to([3.0, 1.7, 0])
        stem = Line([3.0, 1.2, 0], [3.0, 0.4, 0], color=GOLD, stroke_width=6)
        reg = T("regulation", 26, GOLD).move_to([5.3, 1.7, 0])
        self.play(FadeIn(wheel, shift=DOWN * 0.2), Create(stem), FadeIn(reg), run_time=0.8)
        self.at("master control valve")
        self.play(Rotate(wheel, angle=PI, about_point=wheel.get_center()),
                  Transform(reg, VGroup(T("master", 26, GOLD), T("control valve", 26, GOLD)).arrange(DOWN, buff=0.06).move_to([5.3, 1.7, 0])),
                  run_time=1.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S03Crdr(SpokenScene):
    """FAS: the four-step CRDR cycle, run seven times, adding two carbons per pass to reach C16 palmitate."""

    def construct(self):
        head = heading("Building the chain")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.8)
        C = np.array([-4.2, -0.35, 0])
        RR = 1.55
        names = ["C", "R", "D", "R"]
        words = ["condensation", "reduction", "dehydration", "reduction"]
        angs = [90, 0, -90, 180]
        arcs = VGroup(*[
            Arc(radius=RR, start_angle=math.radians(a - 22), angle=-math.radians(46), arc_center=C, color=GREY,
                stroke_width=5).add_tip(tip_length=0.2, tip_width=0.2)
            for a in angs])
        nodes = VGroup(*[VGroup(Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1),
                                 T(n, 28, GREY, weight=BOLD)).move_to(P(C, RR, a)) for n, a in zip(names, angs)])
        for nd in nodes:
            nd[1].move_to(nd[0])
        nodes.set_z_index(3)
        fas = chip2(["fatty acid", "synthase"], BLUE, 26).move_to(C)
        legend = VGroup(*[VGroup(T(n, 28, GREY, weight=BOLD), T(w, 28, GREY)).arrange(RIGHT, buff=0.3)
                          for n, w in zip(names, words)]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-0.3, -0.35, 0])
        for row in legend:
            row[0].set_x(legend.get_left()[0] + 0.15)
            row[1].next_to(row[0], RIGHT, buff=0.3)

        self.at("Fatty acid synthase")
        self.play(FadeIn(fas, scale=0.8), run_time=0.7)
        self.at("one enzyme complex")
        self.play(Indicate(fas, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("four step cycle")
        self.play(Create(arcs, lag_ratio=0.2), FadeIn(nodes), run_time=1.0)

        def light(i, color=YELLOW):
            return AnimationGroup(nodes[i][0].animate.set_stroke(color, width=5), nodes[i][1].animate.set_color(color),
                                  legend[i][0].animate.set_color(color), legend[i][1].animate.set_color(TEXT))

        self.at("condensation")
        self.play(FadeIn(legend[0]), light(0), run_time=0.6)
        self.at("reduction")
        self.play(FadeIn(legend[1]), light(1), run_time=0.6)
        self.at("dehydration")
        self.play(FadeIn(legend[2]), light(2), run_time=0.6)
        self.at("reduction", nth=1)
        self.play(FadeIn(legend[3]), light(3), run_time=0.6)
        self.at("Remember it as")
        crdr = T("CRDR", 44, YELLOW, weight=BOLD).move_to([C[0], -3.0, 0])
        self.play(LaggedStart(*[Circumscribe(n, color=YELLOW, shape=Circle, run_time=0.6) for n in nodes], lag_ratio=0.15), run_time=0.9)
        self.at("CRDR")
        self.play(FadeIn(crdr, shift=UP * 0.15), run_time=0.6)

        # ---- the chain it builds
        k = [1]
        CX = 3.97
        counter = always_redraw(lambda: VGroup(M(str(2 * k[0]), 44, YELLOW), T("carbons", 30, GREY))
                                .arrange(RIGHT, buff=0.25, aligned_edge=DOWN).move_to([CX, 1.1, 0]))
        slots = [np.array([2.15 + 0.52 * i, -0.55, 0]) for i in range(8)]
        blocks = [block(YELLOW, 0.44).move_to(s) for s in slots]
        chain_l = T("the growing chain", 26, GREY).move_to([CX, 2.0, 0])
        dot = Dot(radius=0.14, color=YELLOW).move_to(P(C, RR, 90))
        self.at("Each turn of the cycle")
        self.play(FadeIn(chain_l), FadeIn(counter), FadeIn(blocks[0], scale=0.6), FadeIn(dot), run_time=0.7)
        self.at("joins the growing chain")
        self.play(Circumscribe(nodes[0], color=YELLOW, shape=Circle, run_time=0.6), run_time=0.6)
        self.at("a fresh two carbon unit")
        new = block(YELLOW, 0.44).move_to([slots[1][0], 0.15, 0])
        plus = T("+2", 28, YELLOW).next_to(new, UP, buff=0.1)
        self.play(FadeIn(new), FadeIn(plus), run_time=0.4)
        k[0] = 2
        self.play(new.animate.move_to(slots[1]), FadeOut(plus), run_time=0.7)
        self.remove(new)
        self.add(blocks[1])
        self.at("chemically grooms the new linkage")
        self.play(UpdateFromAlphaFunc(dot, lambda m, a: m.move_to(P(C, RR, 90 - 270 * a))), run_time=1.8, rate_func=linear)
        self.at("saturated stretch")
        sat = VGroup(Brace(VGroup(blocks[0], blocks[1]), DOWN, buff=0.12, color=YELLOW),)
        sat_l = T("saturated", 26, YELLOW).next_to(sat, DOWN, buff=0.08)
        self.play(GrowFromCenter(sat), FadeIn(sat_l), run_time=0.7)
        self.play(UpdateFromAlphaFunc(dot, lambda m, a: m.move_to(P(C, RR, -180 - 90 * a))),
                  run_time=0.4, rate_func=linear)

        # ---- seven turns
        self.at("not run once")
        self.play(FadeOut(sat), FadeOut(sat_l), run_time=0.4)
        self.at("seven times")
        turn_l = always_redraw(lambda: T(f"turn {min(k[0] - 1, 7)} of 7", 28, GREY).move_to([CX, -2.4, 0]))
        self.add(turn_l)
        for i in range(2, 8):
            if i == 4:
                self.at("each pass adds two carbons")
                plus2 = T("+2 carbons each pass", 26, YELLOW).move_to([CX, 0.3, 0])
                self.play(FadeIn(plus2), run_time=0.3)
            k[0] = i + 1
            self.play(UpdateFromAlphaFunc(dot, lambda m, a: m.move_to(P(C, RR, 90 - 360 * a))),
                      FadeIn(blocks[i], scale=0.5, shift=DOWN * 0.3), run_time=0.45, rate_func=linear)
        self.at("16 carbon product")
        self.play(Indicate(counter, color=YELLOW, scale_factor=1.15), FadeOut(plus2), run_time=0.9)
        self.at("palmitate")
        pal = chip("palmitate", YELLOW, 30).move_to([CX, -1.75, 0])
        br = Brace(VGroup(*blocks), DOWN, buff=0.15, color=YELLOW)
        self.play(FadeOut(turn_l), GrowFromCenter(br), FadeIn(pal, shift=UP * 0.2), run_time=0.9)

        # ---- one assembly line
        self.at("single enzyme assembly")
        self.play(Indicate(fas, color=BLUE, scale_factor=1.15), run_time=0.9)
        self.at("same four moves")
        self.play(LaggedStart(*[Circumscribe(n, color=YELLOW, shape=Circle, run_time=0.6) for n in nodes], lag_ratio=0.25), run_time=1.4)
        self.at("stamping out identical parts")
        self.play(LaggedStart(*[Indicate(b, color=YELLOW, scale_factor=1.3) for b in blocks], lag_ratio=0.18), run_time=2.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S04Engine(SpokenScene):
    """Primer + extender -> joined chain; the extra carboxyl leaves as CO2 and that drop in free energy is the
    engine (schematic energy levels, then a weight-and-rope analogy); the CO2 was paid for in stage two."""

    def construct(self):
        banner = heading("The chemical trick")
        self.play(FadeIn(banner, shift=DOWN * 0.15), run_time=0.8)
        Y = 0.7
        # ---- the two reactants
        self.at("We have a primer")
        primer = chip2(["acetyl", "(primer)"], YELLOW, 28).move_to([-4.7, Y, 0])
        self.play(FadeIn(primer, shift=RIGHT * 0.3), run_time=0.7)
        self.at("an extender")
        plus = T("+", 40).move_to([-3.4, Y, 0])
        ext = chip2(["malonyl", "(extender)"], GREEN, 28).move_to([-1.8, Y, 0])
        extra = chip("extra carboxyl", RED, 24, pad=0.14).next_to(ext, UP, buff=0.04)
        self.play(FadeIn(plus), FadeIn(ext, shift=LEFT * 0.3), run_time=0.7)
        self.play(FadeIn(extra, shift=DOWN * 0.1), run_time=0.5)
        self.at("When they condense")
        a1 = arrow([-0.5, Y, 0], [2.0, Y, 0], TEXT, 5)
        prod = chip("joined chain", YELLOW, 28).move_to([3.4, Y, 0])
        self.play(GrowArrow(a1), FadeIn(prod, shift=RIGHT * 0.3), run_time=0.9)
        self.at("loses its extra carboxyl")
        cg = chip("CO₂", RED, 28).move_to([0.75, Y + 0.95, 0])
        self.play(Transform(extra, cg), run_time=1.0, path_arc=-0.5)
        # ---- decarboxylation is the engine
        self.at("decarboxylation is the engine")
        row = VGroup(primer, plus, ext, a1, prod, extra)
        self.play(Transform(banner, heading("Decarboxylation is the engine")), row.animate.shift(UP * 0.7), run_time=0.8)
        ox, oy = -5.2, -3.4
        ax_y = Arrow([ox, oy, 0], [ox, -0.55, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2, max_tip_length_to_length_ratio=1)
        ax_l = T("free energy", 24, GREY).rotate(PI / 2).move_to([ox - 0.45, -2.0, 0])
        yr, yp = -1.3, -3.0
        lvl_r = Line([-4.5, yr, 0], [-2.0, yr, 0], color=TEXT, stroke_width=6)
        lvl_p = Line([0.2, yp, 0], [2.7, yp, 0], color=TEXT, stroke_width=6)
        curve = CubicBezier([-2.0, yr, 0], [-0.9, yr, 0], [-0.9, yp, 0], [0.2, yp, 0], color=TEXT, stroke_width=5)
        lab_r = T("acetyl + malonyl", 26, TEXT).next_to(lvl_r, UP, buff=0.12)
        lab_p = T("joined chain + CO₂", 26, TEXT).next_to(lvl_p, DOWN, buff=0.12)
        self.play(Create(ax_y), FadeIn(ax_l), Create(lvl_r), FadeIn(lab_r), run_time=0.9)
        self.at("so thermodynamically favorable")
        self.play(Create(curve), Create(lvl_p), FadeIn(lab_p), run_time=1.2)
        drop = Arrow([3.4, yr, 0], [3.4, yp, 0], buff=0, color=GOLD, stroke_width=7, tip_length=0.25)
        dash = DashedLine([-2.0, yr, 0], [3.4, yr, 0], color=GREY, stroke_width=3)
        drop_l = T("big drop in\nfree energy", 26, GOLD, line_spacing=0.9).next_to(drop, RIGHT, buff=0.2)
        self.play(Create(dash), GrowArrow(drop), FadeIn(drop_l), run_time=0.9)
        self.at("drags the otherwise sluggish condensation")
        self.play(Indicate(drop, color=GOLD, scale_factor=1.2), Indicate(prod, color=YELLOW), run_time=1.0)
        # ---- weight and rope
        self.at("the way letting go of a heavy weight")
        diagram = VGroup(ax_y, ax_l, lvl_r, lvl_p, curve, lab_r, lab_p, drop, dash, drop_l)
        self.play(FadeOut(diagram), run_time=0.5)
        cart = chip("condensation", YELLOW, 30)
        d = ValueTracker(0.0)
        cart_y = -0.55
        cart.move_to([-3.8, cart_y, 0])
        track = Line([-5.8, cart_y - cart.height / 2 - 0.03, 0], [2.3, cart_y - cart.height / 2 - 0.03, 0],
                     color=GREY, stroke_width=4)
        cart.add_updater(lambda m: m.move_to([-3.8 + d.get_value(), cart_y, 0]))
        PX, PR = 3.0, 0.5
        pul = VGroup(Circle(radius=PR, stroke_color=GREY, stroke_width=4), Dot(radius=0.07, color=GREY)).move_to([PX, cart_y - PR, 0])
        rope1 = always_redraw(lambda: Line([cart.get_right()[0], cart_y, 0], [PX, cart_y, 0], color=TEXT, stroke_width=4))
        wt = chip("CO₂ lets go", RED, 28)
        wt.move_to([PX + PR, -2.5, 0])
        wt.add_updater(lambda m: m.move_to([PX + PR, -2.5 - d.get_value(), 0]))
        rope2 = always_redraw(lambda: Line([PX + PR, cart_y - PR, 0], [PX + PR, wt.get_top()[1], 0], color=TEXT, stroke_width=4))
        self.play(FadeIn(track), FadeIn(cart), FadeIn(pul), FadeIn(rope1), FadeIn(rope2), FadeIn(wt), run_time=0.8)
        self.at("pulls the whole rope along")
        self.play(d.animate.set_value(1.1), run_time=1.3, rate_func=smooth)
        # ---- the product
        self.at("The product")
        rig = Group(track, cart, pul, rope1, rope2, wt)
        cart.clear_updaters(); wt.clear_updaters()
        self.play(FadeOut(rig), run_time=0.6)
        self.at("acetoacetyl acp")
        prod2 = chip("acetoacetyl-ACP", YELLOW, 28)
        prod2.move_to(prod).align_to(prod, LEFT)
        self.play(ReplacementTransform(prod, prod2), run_time=0.8)
        self.at("forms readily")
        ready = T("forms readily", 28, YELLOW).next_to(prod2, DOWN, buff=0.2)
        self.play(FadeIn(ready, shift=UP * 0.1), run_time=0.6)
        self.at("because the cell paid")
        left = chip2(["stage two:", "ATP spent, CO₂ added"], TEAL, 26).move_to([-3.4, -2.3, 0])
        right = chip2(["this step:", "CO₂ leaves, powers it"], RED, 26).move_to([3.0, -2.3, 0])
        link = arrow(left.get_right(), right.get_left(), GREY, 4)
        self.play(FadeIn(left, shift=UP * 0.2), run_time=0.7)
        self.at("the carbon we added")
        dotc = chip("CO₂", RED, 24).move_to(left.get_top() + UP * 0.45)
        self.play(FadeIn(dotc, scale=0.7), GrowArrow(link), FadeIn(right, shift=UP * 0.2), run_time=0.8)
        self.play(dotc.animate.move_to(right.get_top() + UP * 0.45 + RIGHT * 1.0), run_time=1.0, path_arc=-0.6)
        self.at("its purpose was always")
        up = arrow([right.get_top()[0] - 0.9, right.get_top()[1] + 0.1, 0], [0.9, a1.get_bottom()[1] - 0.05, 0], GOLD, 7)
        self.play(GrowArrow(up), Indicate(a1, color=GOLD, scale_factor=1.3), run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S05Gambit(SpokenScene):
    """Why pay ATP to attach CO2 only to throw it away: two schematic energy diagrams, direct vs pay-first."""

    def construct(self):
        q = heading("A fair question", 34)
        ac = acetyl(26).move_to([-4.8, 0.9, 0])
        mal = malonyl(26).move_to([-0.2, 0.9, 0])
        jn = chip("joined chain", YELLOW, 26).move_to([4.5, 0.9, 0])
        a1 = arrow(ac.get_right(), mal.get_left(), GREY, 4)
        a2 = arrow(mal.get_right(), jn.get_left(), GREY, 4)
        self.play(FadeIn(q, shift=DOWN * 0.15), FadeIn(ac), run_time=0.8)
        self.at("Why spend an ATP")
        atp_c = atp(24).move_to([-2.8, 1.85, 0])
        co_c = co2(24).move_to([-1.7, 1.85, 0])
        st2 = T("stage two", 24, GREY).next_to(a1, DOWN, buff=0.15)
        self.play(Transform(q, heading("Why spend ATP to throw CO₂ away?", 34)), GrowArrow(a1), FadeIn(mal),
                  FadeIn(atp_c, shift=DOWN * 0.15), run_time=0.8)
        self.at("to attach a carbon dioxide")
        self.play(FadeIn(co_c, shift=DOWN * 0.15), run_time=0.5)
        self.at("in stage two")
        self.play(FadeIn(st2), run_time=0.4)
        self.at("throw that same carbon dioxide away")
        co_out = co2(24).move_to([2.2, 1.85, 0])
        cond = T("condensation", 24, GREY).next_to(a2, DOWN, buff=0.15)
        self.play(GrowArrow(a2), FadeIn(jn), FadeIn(co_out, shift=UP * 0.15), FadeIn(cond), run_time=1.0)
        self.at("It looks wasteful")
        waste = T("looks wasteful…", 30, GOLD).move_to([0, -0.5, 0])
        self.play(FadeIn(waste, shift=UP * 0.1), run_time=0.7)

        # ---- the answer: two energy diagrams
        self.at("buying thermodynamics")
        row = VGroup(ac, mal, jn, a1, a2, atp_c, co_c, st2, co_out, cond, waste)
        self.play(FadeOut(row), Transform(q, heading("The cell is buying thermodynamics", 34)), run_time=0.8)
        self.at("Direct condensation")
        ox, oy = -6.2, -3.3
        axL = Arrow([ox, oy, 0], [ox, 1.6, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2, max_tip_length_to_length_ratio=1)
        axL_l = T("free energy", 24, GREY).rotate(PI / 2).move_to([ox - 0.4, -0.8, 0])
        tL = T("Direct condensation", 28, TEXT).move_to([-3.9, 2.3, 0])
        yst, yup = -2.2, -0.5
        lv1 = Line([-5.4, yst, 0], [-4.4, yst, 0], color=TEXT, stroke_width=6)
        lv2 = Line([-3.1, yup, 0], [-2.0, yup, 0], color=TEXT, stroke_width=6)
        cv1 = CubicBezier([-4.4, yst, 0], [-3.9, yst, 0], [-3.7, yup, 0], [-3.1, yup, 0], color=TEXT, stroke_width=5)
        l1 = T("2 acetyl CoA", 24, YELLOW).next_to(lv1, DOWN, buff=0.12)
        l2 = T("joined chain", 24, YELLOW).next_to(lv2, UP, buff=0.12)
        self.play(FadeIn(tL), Create(axL), FadeIn(axL_l), Create(lv1), FadeIn(l1), run_time=0.9)
        self.at("is unfavorable")
        self.play(Create(cv1), Create(lv2), FadeIn(l2), run_time=1.1)
        self.at("would barely proceed")
        stall = T("uphill: barely goes", 26, GREY).move_to([-3.9, -3.25, 0])
        xx = Cross(Square(side_length=0.45), stroke_color=RED, stroke_width=6).move_to([-3.8, -1.35, 0])
        self.play(FadeIn(stall), Create(xx), run_time=0.8)

        # right panel: pay first
        self.at("By investing one ATP")
        tR = T("Carboxylate first", 28, TEXT).move_to([2.5, 2.3, 0])
        r0, r1, r2 = -2.2, 0.7, -2.9
        rs = Line([-0.9, r0, 0], [0.3, r0, 0], color=TEXT, stroke_width=6)
        rm = Line([1.7, r1, 0], [2.9, r1, 0], color=TEXT, stroke_width=6)
        re = Line([4.4, r2, 0], [5.6, r2, 0], color=TEXT, stroke_width=6)
        ls = T("2 acetyl CoA", 24, YELLOW).next_to(rs, DOWN, buff=0.12)
        lm = T("malonyl CoA:\nenergy stored", 24, GREEN, line_spacing=0.9).next_to(rm, UP, buff=0.12)
        le = T("joined chain\n+ CO₂", 24, YELLOW, line_spacing=0.9).next_to(re, DOWN, buff=0.12)
        up_a = Arrow([1.0, r0, 0], [1.0, r1, 0], buff=0, color=TEAL, stroke_width=7, tip_length=0.25)
        up_l = T("+1 ATP", 26, TEAL).next_to(up_a, RIGHT, buff=0.12).shift(DOWN * 0.5)
        self.play(FadeIn(tR), Create(rs), FadeIn(ls), run_time=0.7)
        self.play(GrowArrow(up_a), FadeIn(up_l), run_time=0.9)
        self.at("stores energy in malonyl CoA")
        self.play(Create(rm), FadeIn(lm), run_time=0.9)
        self.at("that carbon dioxide is released")
        co_l = co2(24).move_to([4.9, r1 + 0.65, 0])
        co_arrow = arrow([3.5, r1 + 0.3, 0], [4.35, r1 + 0.55, 0], RED, 3)
        self.play(FadeIn(co_l, shift=LEFT * 0.4), GrowArrow(co_arrow), run_time=0.7)
        self.at("strongly downhill")
        cv2 = CubicBezier([2.9, r1, 0], [3.7, r1, 0], [3.6, r2, 0], [4.4, r2, 0], color=GOLD, stroke_width=7)
        dl = T("strongly\ndownhill", 26, GOLD, line_spacing=0.9).move_to([5.4, -0.9, 0])
        self.play(Create(cv2), Create(re), FadeIn(le), FadeIn(dl), run_time=1.2)

        # ---- gambit
        self.at("It is a gambit")
        self.play(Transform(q, heading("The gambit", 34)), run_time=0.5)
        left_stuff = VGroup(axL, axL_l, tL, lv1, lv2, cv1, l1, l2, stall, xx, tR, rs, rm, re, ls, lm, le, up_a, up_l, co_l, co_arrow, cv2, dl)
        self.play(FadeOut(left_stuff), run_time=0.7)
        c1 = chip("pay up front", TEAL, 32).move_to([-4.3, 0.4, 0])
        c2 = chip("release on demand", RED, 32).move_to([0.0, 0.4, 0])
        c3 = chip("gain control", GOLD, 32).move_to([4.3, 0.4, 0])
        ar1 = arrow(c1.get_right(), c2.get_left(), TEXT, 4)
        ar2 = arrow(c2.get_right(), c3.get_left(), TEXT, 4)
        self.at("Pay up front")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        self.at("release on demand")
        self.play(GrowArrow(ar1), FadeIn(c2, shift=UP * 0.2), run_time=0.7)
        self.at("gain control")
        self.play(GrowArrow(ar2), FadeIn(c3, shift=UP * 0.2), run_time=0.7)
        self.at("otherwise would not run")
        cap = T("a reaction that otherwise would not run", 28, GREY).move_to([0, -1.2, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        # ---- every carbon traces back to acetyl CoA
        self.at("Every carbon still traces")
        self.play(Transform(q, heading("Where every carbon comes from", 34)), FadeOut(VGroup(c1, c2, c3, ar1, ar2, cap)), run_time=0.4)
        bl = VGroup(*[chip("2C", YELLOW, 26, pad=0.16) for _ in range(8)]).arrange(RIGHT, buff=0.12).move_to([0, 0.4, 0])
        brc = Brace(bl, DOWN, buff=0.2, color=YELLOW)
        cap2 = T("palmitate: 16 carbons, every one from acetyl CoA", 28, YELLOW).next_to(brc, DOWN, buff=0.2)
        self.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in bl], lag_ratio=0.08), run_time=0.9)
        self.at("traces back to acetyl CoA")
        self.play(GrowFromCenter(brc), FadeIn(cap2, shift=UP * 0.1), run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------------------------
class S06End(EndCard):
    LINE = "Pay one ATP up front; let CO₂ pull the chain forward."
