"""The gate to the cycle: pyruvate dehydrogenase complex  (Biochemistrypedia explainer)

Four narrated slide clips, one arc: pyruvate becomes acetyl-CoA in three chemical moves inside ONE
complex (s01) -> a tethered lipoamide arm carries the acetyl unit between three enzymes (s02) ->
on the timeline of four steps, NADH is made only at the very end (s03) -> a kinase/phosphatase switch
on E1, read from the cell's energy state, opens or closes the gate (s04).

COLOR MAP (one color per concept, whole video)
  YELLOW = the carbon cargo (pyruvate, the 2-carbon unit, acetyl)
  GREEN  = acetyl-CoA (the product) and "ON / stimulated"
  RED    = "OFF / blocked / inhibited", and the "No NADH" badges
  BLUE   = enzymes (E1, E2, E3, kinase, phosphatase, the complex)
  PINK   = coenzymes (TPP, lipoamide, CoA, FAD, NAD+)
  ORANGE = electrons and NADH (reducing power)
  PURPLE = phosphate
  GREY   = structure, axes, CO2, de-emphasized text
Everything is chips, boxes, arrows and flows: no molecular structures are drawn.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

PINK = "#E58FC0"
ORANGE = "#F59E42"
PURPLE = "#B58CD9"


def tok(text, color, size=22, pad=0.17):
    return chip(text, color, size=size, pad=pad)


def at_pt(mob, p):
    return mob.move_to([p[0], p[1], 0])


def solid_tok(text, color, size=22, pad=0.17):
    """A chip with an opaque backing, so lines it travels over do not show through it."""
    c = chip(text, color, size=size, pad=pad)
    back = c[0].copy().set_fill(BG, 1).set_stroke(width=0)
    return VGroup(back, *c)


def step_label(text, x, top_y):
    """Step heading whose cap height sits on a common line (all three have ascenders; one has a descender)."""
    t = T(text, 24, TEXT).move_to([x, 0, 0])
    return t.shift(UP * (top_y - t.get_top()[1]))


class S00Title(TitleCard):
    LESSON = "Pyruvate dehydrogenase"
    TITLE = "The gate to the cycle"


# ----------------------------------------------------------------------------------------------------
class S01ThreeSteps(SpokenScene):
    """Pyruvate -> acetyl-CoA is three reactions in ONE complex; carbon flows through, electrons peel off to NAD+."""

    def construct(self):
        BW, BH, GAP = 2.3, 3.0, 0.45
        CY, ROW = 0.5, 1.3
        xs = [-(BW + GAP), 0.0, BW + GAP]
        names = ["Decarboxylation", "Oxidation", "Transfer to CoA"]

        heading = T("Pyruvate to acetyl-CoA", 32, font=TITLE_FONT).move_to([0, 3.3, 0])
        pyr = tok("pyruvate", YELLOW).move_to([-5.35, ROW, 0])
        ace = tok("acetyl-CoA", GREEN).move_to([5.2, ROW, 0])
        ace.set_opacity(0.4)
        long_arrow = Arrow(pyr.get_right() + RIGHT * 0.08, ace.get_left() + LEFT * 0.08, color=GREY, stroke_width=5, buff=0)
        self.play(FadeIn(heading), FadeIn(pyr), FadeIn(ace), run_time=0.9)
        self.play(GrowArrow(long_arrow), run_time=1.2)

        self.at("but three")
        boxes = [RoundedRectangle(corner_radius=0.18, width=BW, height=BH, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.07).move_to([x, CY, 0]) for x in xs]
        gaps = [Arrow([-5.35 + 0.95, ROW, 0], [xs[0] - BW / 2, ROW, 0], color=GREY, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.5),
                Arrow([xs[0] + BW / 2, ROW, 0], [xs[1] - BW / 2, ROW, 0], color=GREY, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.6),
                Arrow([xs[1] + BW / 2, ROW, 0], [xs[2] - BW / 2, ROW, 0], color=GREY, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.6),
                Arrow([xs[2] + BW / 2, ROW, 0], [5.2 - 1.05, ROW, 0], color=GREY, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.5)]
        nums = [T(str(i + 1), 40, GREY, font=TITLE_FONT).move_to([xs[i], CY - 1.05, 0]) for i in range(3)]
        for n in nums:
            n.set_opacity(0)
        self.play(FadeOut(long_arrow), LaggedStart(*[GrowFromCenter(b) for b in boxes], lag_ratio=0.25), *[FadeIn(g) for g in gaps], run_time=1.2)

        self.at("single complex")
        outline = RoundedRectangle(corner_radius=0.3, width=3 * BW + 2 * GAP + 0.5, height=BH + 0.5,
                                   stroke_color=BLUE, stroke_width=4, fill_opacity=0).move_to([0, CY, 0])
        cx_lbl = T("one complex", 28, BLUE).move_to([-4.2, CY - BH / 2 - 0.58, 0])
        self.play(Create(outline), FadeIn(cx_lbl), run_time=1.2)

        # ---- step 1 -------------------------------------------------------------------------
        self.at("First comes")
        t1 = step_label(names[0], xs[0], 2.73)
        self.play(FadeIn(t1, shift=DOWN * 0.1), boxes[0].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.1), run_time=0.7)
        self.play(pyr.animate.move_to([xs[0], ROW, 0]), run_time=0.9)
        self.at("loses carbon dioxide")
        co2 = T("CO₂", 28, GREY).move_to([xs[0], ROW, 0])
        self.add(co2)
        self.play(co2.animate.move_to([-5.15, 2.45, 0]), run_time=1.1)
        self.play(FadeOut(co2), run_time=0.4)
        self.at("remaining two carbon")
        frag = tok("2-C unit", YELLOW).move_to([xs[0], ROW, 0])
        self.play(ReplacementTransform(pyr, frag), run_time=0.8)
        pyr = frag
        self.at("captured on thiamine")
        tpp = tok("TPP", PINK).move_to([xs[0], 0.2, 0])
        self.play(FadeIn(tpp, shift=UP * 0.2), run_time=0.8)

        # ---- step 2 -------------------------------------------------------------------------
        self.at("Second is oxidation")
        t2 = step_label(names[1], xs[1], 2.73)
        self.play(FadeIn(t2, shift=DOWN * 0.1), boxes[0].animate.set_stroke(GREY).set_fill(GREY, 0.07),
                  boxes[1].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.1), pyr.animate.move_to([xs[1], ROW, 0]),
                  run_time=1.0)
        self.at("two electrons leave")
        etok = solid_tok("2 e−", ORANGE).move_to([xs[1], ROW, 0])
        etok.set_z_index(5)
        self.play(FadeIn(etok, scale=0.6), run_time=0.4)
        gx = xs[1] + BW / 2 + GAP / 2
        path = VMobject().set_points_as_corners([[xs[1], ROW, 0], [gx, 0.95, 0], [gx, -2.7, 0]])
        self.play(MoveAlongPath(etok, path), run_time=1.3)
        self.at("handed to the lipoamide")
        lip = tok("lipoamide", PINK).move_to([xs[1], 0.2, 0])
        self.play(FadeIn(lip, shift=UP * 0.2), Indicate(pyr, color=YELLOW, scale_factor=1.12), run_time=0.9)

        # ---- step 3 -------------------------------------------------------------------------
        self.at("Third is transfer")
        t3 = step_label(names[2], xs[2], 2.73)
        self.play(FadeIn(t3, shift=DOWN * 0.1), boxes[1].animate.set_stroke(GREY).set_fill(GREY, 0.07),
                  boxes[2].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.1), pyr.animate.move_to([xs[2], ROW, 0]),
                  run_time=1.0)
        coa = tok("CoA", PINK).move_to([xs[2], 0.2, 0])
        self.play(FadeIn(coa, shift=UP * 0.2), run_time=0.6)
        self.at("producing acetyl CoA")
        acetylcoa = tok("acetyl-CoA", GREEN).move_to([xs[2], ROW, 0])
        self.play(ReplacementTransform(pyr, acetylcoa), run_time=0.7)
        self.play(acetylcoa.animate.move_to([5.2, ROW, 0]), boxes[2].animate.set_stroke(GREY).set_fill(GREY, 0.07),
                  FadeOut(ace), run_time=0.9)
        pyr = acetylcoa

        # ---- follow the carbon, then the electrons ---------------------------------------------
        self.at("Follow the carbon")
        trail = Line([-5.0, 1.8, 0], [4.6, 1.8, 0], color=YELLOW, stroke_width=6)
        dot = Dot([-5.0, 1.8, 0], radius=0.12, color=YELLOW)
        self.add(dot)
        self.play(Create(trail), MoveAlongPath(dot, Line([-5.0, 1.8, 0], [4.6, 1.8, 0])), run_time=2.0, rate_func=smooth)
        self.play(FadeOut(trail), FadeOut(dot), run_time=0.4)
        self.at("follow the electrons separately")
        nad = tok("NAD⁺", PINK).move_to([4.5, -2.7, 0])
        lane = Arrow(etok.get_right() + RIGHT * 0.12, nad.get_left() + LEFT * 0.12, color=ORANGE, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.12)
        lane.set_z_index(1)
        etok.set_z_index(5)
        self.play(Indicate(etok, color=ORANGE, scale_factor=1.2), GrowArrow(lane), FadeIn(nad, shift=LEFT * 0.3), run_time=1.2)
        self.at("reducing NAD plus")
        self.play(etok.animate.next_to(nad, LEFT, buff=0.06), run_time=0.9)
        self.at("to NADH")
        nadh = tok("NADH", ORANGE).move_to([4.5, -2.7, 0])
        self.play(etok.animate.move_to(nad).scale(0.3).set_opacity(0), ReplacementTransform(nad, nadh), run_time=0.8)
        self.remove(etok)

        # ---- coenzymes and vitamins --------------------------------------------------------------
        self.at("Notice that each step")
        self.play(Indicate(tpp, color=PINK, scale_factor=1.25), run_time=0.7)
        self.play(Indicate(lip, color=PINK, scale_factor=1.25), run_time=0.7)
        self.play(Indicate(coa, color=PINK, scale_factor=1.25), run_time=0.7)
        self.at("trace back to B vitamins")
        v1 = T("from vitamin B1", 22, GREY).move_to([xs[0], -0.55, 0])
        v5 = T("from vitamin B5", 22, GREY).move_to([xs[2], -0.55, 0])
        v3 = T("NAD⁺ comes from niacin (B3)", 22, GREY).move_to([3.7, -3.3, 0])
        self.play(FadeIn(v1, shift=UP * 0.1), FadeIn(v5, shift=UP * 0.1), FadeIn(v3, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------------------------------
class S02Arm(SpokenScene):
    """One tethered lipoamide arm (pink) swings its tip between E1, E2 and E3 (blue), carrying the acetyl unit (yellow)."""

    def construct(self):
        B = np.array([0.0, -0.75, 0.0])
        R = 2.7
        th = ValueTracker(90.0)

        def tip_at(deg):
            a = np.radians(deg)
            return B + R * np.array([np.cos(a), np.sin(a), 0.0])

        def arm_mob():
            tip = tip_at(th.get_value())
            d = tip - B
            n = np.array([-d[1], d[0], 0.0]) / np.linalg.norm(d)
            pts = []
            for k in range(61):
                u = k / 60
                amp = 0.15 * np.sin(np.pi * min(1, u * 1.0)) ** 0.5
                pts.append(B + d * u + n * amp * np.sin(2 * np.pi * 7 * u))
            m = VMobject(stroke_color=PINK, stroke_width=6, fill_opacity=0, cap_style=CapStyleType.ROUND)
            m.set_points_as_corners(pts)
            return m

        def tip_mob():
            return Circle(radius=0.17, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to(tip_at(th.get_value()))

        # ---- the machine: E2 core with E1 and E3 beside it -------------------------------------
        core = Circle(radius=1.25, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to([0, -2.0, 0])
        copies = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=BLUE, fill_opacity=0.75).move_to(
            [1.0 * np.cos(a), -2.0 + 0.95 * np.sin(a), 0]) for a in np.linspace(0, 2 * PI, 11)[:-1]])
        e2_lbl = T("E2 core", 26, BLUE).move_to([0, -2.0, 0])
        e1 = Ellipse(width=1.9, height=1.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to([-3.3, 0.9, 0])
        e3 = Ellipse(width=1.9, height=1.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to([3.3, 0.9, 0])
        # E2's own active site, where the arm hands the acetyl to CoA (the core is the E2 scaffold)
        e2s = Ellipse(width=1.7, height=0.85, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to([0, 2.66, 0])
        e2s_lbl = T("E2 site", 26, BLUE).move_to(e2s.get_center() + UP * 0.05)
        e1_lbl = T("E1", 30, BLUE).move_to(e1)
        e3_lbl = T("E3", 30, BLUE).move_to(e3)
        arm = always_redraw(arm_mob)
        tipd = always_redraw(tip_mob)
        anchor = Dot(B, radius=0.1, color=PINK)
        arm_lbl = T("lipoamide arm", 26, PINK).move_to([-2.95, 2.6, 0])
        state_hd = T("the arm carries", 22, GREY).move_to([-6.1, -1.1, 0], aligned_edge=LEFT)
        cur = {"state": None}

        def set_state(txt, color=PINK):
            new = T(txt, 26, color).move_to([-6.1, -1.65, 0], aligned_edge=LEFT)
            old = cur["state"]
            cur["state"] = new
            if old is None:
                return [FadeIn(new)]
            return [ReplacementTransform(old, new)]

        self.play(FadeIn(core), FadeIn(copies), run_time=0.8)
        self.play(Create(arm), FadeIn(tipd), FadeIn(anchor), run_time=1.0)
        self.add(arm, tipd)
        self.play(FadeIn(arm_lbl), run_time=0.6)
        self.at("Tethered to the E2 core")
        self.play(FadeIn(e2_lbl), copies.animate.set_opacity(0.35), Indicate(anchor, color=PINK, scale_factor=2.2),
                  FadeIn(e1), FadeIn(e3), FadeIn(e2s), run_time=1.0)
        self.add(arm, tipd)
        self.play(FadeIn(state_hd), *set_state("lipoamide (oxidized)"), run_time=0.6)

        # ---- 1. swing to E1 and pick up acetyl ---------------------------------------------------
        self.at("swings to E1")
        self.play(FadeIn(e1_lbl), th.animate.set_value(150), run_time=1.4, rate_func=smooth)
        self.at("picks up the acetyl")
        cargo = Dot(radius=0.14, color=YELLOW).move_to([-3.3, 1.35, 0])
        cl = T("acetyl", 24, YELLOW).next_to(cargo, UP, buff=0.12)
        self.play(FadeIn(cargo), FadeIn(cl), run_time=0.5)
        self.play(cargo.animate.move_to(tip_at(150) + np.array([-0.3, 0.2, 0])), FadeOut(cl), run_time=0.7)
        cargo.add_updater(lambda m: m.move_to(tip_at(th.get_value()) + np.array([-0.3, 0.2, 0]) * 1.0 if False else
                                              tip_at(th.get_value()) + 0.3 * np.array([np.cos(np.radians(th.get_value())), np.sin(np.radians(th.get_value())), 0])))
        self.at("becoming acetyl lipoamide")
        self.play(*set_state("acetyl-lipoamide", YELLOW), run_time=0.6)

        # ---- 2. pivot to E2, hand to CoA ---------------------------------------------------------
        self.at("it pivots")
        self.play(th.animate.set_value(90), FadeIn(e2s_lbl), run_time=1.3, rate_func=smooth)
        self.at("delivers that acetyl unit")
        coa = tok("CoA", PINK).move_to([1.8, 2.66, 0])
        self.play(FadeIn(coa, shift=LEFT * 0.15), run_time=0.6)
        cargo.clear_updaters()
        self.play(cargo.animate.next_to(coa, LEFT, buff=0.04), run_time=0.8)
        self.at("releasing acetyl CoA")
        acoa = tok("acetyl-CoA", GREEN).move_to(coa)
        self.play(FadeOut(cargo, scale=0.4), FadeTransform(coa, acoa), run_time=0.6)
        self.play(acoa.animate.move_to([4.7, 2.7, 0]), run_time=1.0)
        self.at("reduced as dihydrolipoamide")
        ring = always_redraw(lambda: Circle(radius=0.3, stroke_color=ORANGE, stroke_width=5, fill_opacity=0).move_to(tip_at(th.get_value())))
        self.play(Create(ring), *set_state("dihydrolipoamide (reduced)", ORANGE), run_time=0.8)

        # ---- 3. E3 reoxidizes the arm -------------------------------------------------------------
        self.at("Finally, it reaches E3")
        self.play(FadeIn(e3_lbl), th.animate.set_value(30), run_time=1.3, rate_func=smooth)
        self.at("to be reoxidized")
        edots = VGroup(*[Dot(radius=0.1, color=ORANGE).move_to(tip_at(30) + np.array([0.1 * k, 0.12 * (1 - 2 * k), 0])) for k in range(2)])
        self.add(edots)
        self.play(*[d.animate.move_to(e3.get_center() + np.array([0.3 * (1 - 2 * k), -0.4, 0])) for k, d in enumerate(edots)],
                  FadeOut(ring), run_time=1.0)
        self.play(FadeOut(edots), e3.animate.set_fill(ORANGE, 0.0).set_fill(BLUE, 0.22), run_time=0.4)
        self.at("regenerating the disulfide")
        self.play(*set_state("lipoamide (oxidized)"), run_time=0.7)
        self.at("so the cycle can repeat")
        self.play(th.animate.set_value(150), run_time=1.4, rate_func=smooth)

        # ---- reach: 14 angstroms, many copies ---------------------------------------------------------
        self.at("about 14 angstroms")
        t = tip_at(150)
        nrm = np.array([0.5, 0.866, 0.0])
        dim = DashedLine(B + nrm * 0.4, t + nrm * 0.4, color=GREY, stroke_width=3, dash_length=0.12)
        dim_lbl = M("≈ 14 Å", 26, PINK).move_to((B + t) / 2 + nrm * 0.95)
        self.play(Create(dim), FadeIn(dim_lbl), run_time=0.9)
        self.at("many copies")
        self.play(copies.animate.set_opacity(1.0), run_time=0.6)
        self.at("24 or 60")
        n_lbl = M("24 or 60 copies", 26, BLUE).move_to([3.7, -2.0, 0])
        self.play(FadeIn(n_lbl, shift=LEFT * 0.2), run_time=0.7)
        self.at("all three active sites")
        self.play(FadeOut(dim), FadeOut(dim_lbl), FadeOut(acoa), FadeOut(state_hd), FadeOut(cur["state"]),
                  th.animate.set_value(90), run_time=0.5)
        arc = ArcBetweenPoints(tip_at(150), tip_at(30), angle=-PI / 3.1, color=GREY, stroke_width=3)
        arc = DashedVMobject(arc, num_dashes=28)
        rings = VGroup(*[Circle(radius=0.32, stroke_color=PINK, stroke_width=4).move_to(tip_at(a)) for a in (150, 90, 30)])
        self.play(Create(arc), LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.5), run_time=2.0)
        self.at("never escape")
        cargo2 = Dot(radius=0.14, color=YELLOW).move_to(tip_at(90) + np.array([0, 0.3, 0]))
        shell = RoundedRectangle(corner_radius=0.45, width=9.4, height=6.75, stroke_color=BLUE, stroke_width=2.5,
                                 stroke_opacity=0.55).move_to([0, -0.08, 0])
        self.play(FadeIn(cargo2), Create(shell), FadeOut(n_lbl), run_time=1.0)
        self.at("ride the tethered arm")
        cargo2.add_updater(lambda m: m.move_to(tip_at(th.get_value()) + 0.3 * np.array([np.cos(np.radians(th.get_value())), np.sin(np.radians(th.get_value())), 0])))
        self.play(th.animate.set_value(150), run_time=1.1, rate_func=smooth)
        self.play(th.animate.set_value(90), run_time=1.1, rate_func=smooth)
        cargo2.clear_updaters()
        self.finish()


# ----------------------------------------------------------------------------------------------------
class S03Nadh(SpokenScene):
    """Four steps on one timeline: carbon (yellow) and electrons (orange) tracked; NADH appears only at step 4."""

    def construct(self):
        CW, GAP = 2.85, 0.28
        xs = [-6.12 + CW / 2 + i * (CW + GAP) for i in range(4)]
        CYc, CH = 0.55, 3.0
        names = ["Decarboxylation", "Oxidative\ntransfer", "Acetyl\ntransfer", "Regeneration"]
        enz = ["E1", "E1", "E2", "E3"]
        LC, LE = -1.7, -2.8

        w1 = T("Where is ", 36, TEXT, font=TITLE_FONT)
        w2 = T("NADH", 36, ORANGE, font=TITLE_FONT, weight=BOLD)
        w3 = T(" born?", 36, TEXT, font=TITLE_FONT)
        heading = VGroup(w1, w2, w3).arrange(RIGHT, buff=0.2).move_to([0, 3.2, 0])
        self.play(FadeIn(heading), run_time=0.8)

        self.at("on one timeline")
        cards = [RoundedRectangle(corner_radius=0.16, width=CW, height=CH, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.06).move_to([x, CYc, 0]) for x in xs]
        steps = [T(f"STEP {i + 1}", 22, GREY).move_to([xs[i], CYc + 1.2, 0]) for i in range(4)]
        arrows = [Arrow([xs[i] + CW / 2 + 0.01, CYc + 0.2, 0], [xs[i + 1] - CW / 2 - 0.01, CYc + 0.2, 0], color=GREY,
                        stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.9, tip_length=0.2) for i in range(3)]
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.15), *[FadeIn(s) for s in steps],
                  *[FadeIn(a) for a in arrows], run_time=1.4)

        def reveal(i):
            nm = VGroup(*[T(ln, 24, TEXT) for ln in names[i].split("\n")]).arrange(DOWN, buff=0.1).move_to([xs[i], CYc + 0.55, 0])
            ec = tok(enz[i], BLUE).move_to([xs[i], CYc - 0.3, 0])
            return nm, ec

        def highlight(i, color):
            return cards[i].animate.set_stroke(color).set_fill(color, 0.1)

        def unhighlight(i):
            return cards[i].animate.set_stroke(GREY).set_fill(GREY, 0.06)

        badge = [None] * 4

        def no_nadh(i):
            b = tok("No NADH", RED).move_to([xs[i], CYc - 1.05, 0])
            badge[i] = b
            return FadeIn(b, scale=0.7)

        # ---- step 1 -------------------------------------------------------------------------
        self.at("Step 1")
        nm, ec = reveal(0)
        self.play(highlight(0, YELLOW), FadeIn(nm), FadeIn(ec), run_time=0.9)
        self.at("decarboxylation on E1")
        carbon = tok("pyruvate", YELLOW).move_to([xs[0], LC, 0])
        lg = VGroup(Dot(radius=0.09, color=YELLOW), T("carbon", 22, GREY), Dot(radius=0.09, color=ORANGE), T("electrons", 22, GREY))
        lg.arrange(RIGHT, buff=0.18)
        lg[2].shift(RIGHT * 0.4); lg[3].shift(RIGHT * 0.4)
        lg.move_to([0, -3.4, 0])
        self.play(FadeIn(carbon, shift=UP * 0.2), FadeIn(lg), run_time=0.6)
        self.at("releases carbon dioxide")
        co2 = T("CO₂", 28, GREY).move_to([xs[0], LC, 0])
        self.add(co2)
        hyd = tok("hydroxyethyl", YELLOW).move_to([xs[0], LC, 0])
        self.play(co2.animate.move_to([-5.95, -1.15, 0]), ReplacementTransform(carbon, hyd), run_time=1.1)
        carbon = hyd
        etok = tok("2 e− in fragment", ORANGE).move_to([xs[0], LE, 0])
        self.play(FadeIn(etok, shift=UP * 0.2), FadeOut(co2), run_time=0.6)
        self.at("makes no NADH")
        self.play(no_nadh(0), run_time=0.6)

        # ---- step 2 -------------------------------------------------------------------------
        self.at("Step 2")
        nm2, ec2 = reveal(1)
        self.play(unhighlight(0), highlight(1, YELLOW), FadeIn(nm2), FadeIn(ec2), run_time=0.9)
        self.at("hands the hydroxyethyl group")
        etok2 = tok("2 e− on lipoamide", ORANGE).move_to([xs[1], LE, 0])
        self.play(carbon.animate.move_to([xs[1], LC, 0]), ReplacementTransform(etok, etok2), run_time=1.2)
        etok = etok2
        self.at("oxidized to an acetyl group")
        ac = tok("acetyl", YELLOW).move_to([xs[1], LC, 0])
        self.play(ReplacementTransform(carbon, ac), run_time=0.7)
        carbon = ac
        self.at("still no NADH")
        self.play(no_nadh(1), run_time=0.6)

        # ---- step 3 -------------------------------------------------------------------------
        self.at("Step 3")
        nm3, ec3 = reveal(2)
        self.play(unhighlight(1), highlight(2, YELLOW), FadeIn(nm3), FadeIn(ec3), run_time=0.9)
        self.at("acetyl transfer on E2")
        self.play(carbon.animate.move_to([xs[2], LC, 0]), run_time=1.0)
        self.at("produces acetyl CoA")
        acoa = tok("acetyl-CoA", GREEN).move_to([xs[2], LC, 0])
        self.play(ReplacementTransform(carbon, acoa), cards[2].animate.set_stroke(GREEN).set_fill(GREEN, 0.1), run_time=0.8)
        self.at("leaves dihydrolipoamide")
        etok3 = tok("2 e− on the arm", ORANGE).move_to([xs[2], LE, 0])
        self.play(ReplacementTransform(etok, etok3), run_time=0.9)
        etok = etok3
        self.at("again no NADH")
        self.play(no_nadh(2), run_time=0.6)

        # ---- step 4 -------------------------------------------------------------------------
        self.at("Only in Step 4")
        nm4, ec4 = reveal(3)
        self.play(unhighlight(2), highlight(3, ORANGE), FadeIn(nm4), FadeIn(ec4), run_time=0.9)
        self.at("reoxidized by FAD")
        etok4 = tok("2 e− → FAD", ORANGE).move_to([xs[3], LE, 0])
        self.play(ReplacementTransform(etok, etok4), run_time=0.9)
        self.at("electrons flow onward")
        nadh = tok("NADH", ORANGE, size=28).move_to([xs[3], LE, 0])
        self.play(ReplacementTransform(etok4, nadh), run_time=0.9)
        yes = tok("NADH here!", ORANGE).move_to([xs[3], CYc - 1.05, 0])
        self.play(FadeIn(yes, scale=0.7), run_time=0.6)

        # ---- the punchline ------------------------------------------------------------------------
        self.at("So three steps")
        brace1 = Brace(VGroup(cards[0], cards[2]), UP, color=GREEN, buff=0.12)
        lbl1 = T("build the product", 26, GREEN).next_to(brace1, UP, buff=0.1)
        self.play(FadeOut(heading), GrowFromCenter(brace1), FadeIn(lbl1), run_time=1.0)
        self.at("exactly one step")
        brace2 = Brace(cards[3], UP, color=ORANGE, buff=0.12)
        lbl2 = T("reducing power", 26, ORANGE).next_to(brace2, UP, buff=0.1)
        self.play(GrowFromCenter(brace2), FadeIn(lbl2), Indicate(yes, color=ORANGE), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------------------------------
class S04Gate(SpokenScene):
    """E1 carries an on/off switch (kinase adds a phosphate = off, phosphatase removes it = on) read from the energy state."""

    def construct(self):
        ROW = 0.9
        pyr = tok("pyruvate", YELLOW).move_to([-5.3, ROW, 0])
        pdc = RoundedRectangle(corner_radius=0.18, width=2.6, height=1.5, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.18).move_to([-2.2, ROW, 0])
        pdc_lbl = T("PDC", 34, BLUE, weight=BOLD).move_to(pdc.get_center() + UP * 0.3)
        e1c = tok("E1", BLUE).move_to(pdc.get_center() + DOWN * 0.38)
        ace = tok("acetyl-CoA", GREEN).move_to([1.3, ROW, 0])
        tca = T("citric acid\ncycle", 26, GREY, line_spacing=0.8)
        tcabox = RoundedRectangle(corner_radius=0.18, width=2.5, height=1.4, stroke_color=GREY, stroke_width=3,
                                  fill_opacity=0).move_to([4.7, ROW, 0])
        tca.move_to(tcabox)
        a1 = Arrow(pyr.get_right() + RIGHT * 0.05, pdc.get_left() + LEFT * 0.05, color=GREY, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.5)
        a2 = Arrow(pdc.get_right() + RIGHT * 0.05, ace.get_left() + LEFT * 0.05, color=GREY, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.6)
        a3 = Arrow(ace.get_right() + RIGHT * 0.05, tcabox.get_left() + LEFT * 0.05, color=GREY, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.6)
        flow = VGroup(pyr, a1, pdc, pdc_lbl, e1c, a2, ace, a3, tcabox, tca)
        self.play(LaggedStart(*[FadeIn(m) for m in flow], lag_ratio=0.08), run_time=1.8)
        self.at("regulatory site")
        self.play(Indicate(e1c, color=BLUE, scale_factor=1.35), pdc.animate.set_stroke(BLUE, 6), run_time=1.1)

        # ---- the switch -------------------------------------------------------------------------
        self.at("on off switch")
        SW = np.array([-2.2, 2.55, 0])
        pill = RoundedRectangle(corner_radius=0.25, width=1.1, height=0.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to(SW)
        knob = Circle(radius=0.2, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(SW + RIGHT * 0.3)
        sw_lbl = T("ON", 26, GREEN, weight=BOLD).move_to(SW + UP * 0.55)
        self.play(FadeIn(pill), FadeIn(knob), FadeIn(sw_lbl), run_time=0.8)

        def flip(on):
            c = GREEN if on else RED
            nl = T("ON" if on else "OFF", 26, c, weight=BOLD).move_to(SW + UP * 0.55)
            return [knob.animate.move_to(SW + (RIGHT if on else LEFT) * 0.3), pill.animate.set_stroke(c).set_fill(c, 0.35),
                    Transform(sw_lbl, nl)]

        self.at("kinase and a phosphatase")
        kin = tok("kinase", BLUE).move_to([-5.0, 2.55, 0])
        pho = tok("phosphatase", BLUE).move_to([1.0, 2.55, 0])
        self.play(FadeIn(kin, shift=RIGHT * 0.3), FadeIn(pho, shift=LEFT * 0.3), run_time=0.9)
        self.at("travel with the complex")
        l1 = DashedLine(kin.get_bottom(), pdc.get_corner(UL) + RIGHT * 0.25, color=BLUE, stroke_width=3, dash_length=0.1)
        l2 = DashedLine(pho.get_bottom(), pdc.get_corner(UR) + LEFT * 0.1, color=BLUE, stroke_width=3, dash_length=0.1)
        self.play(Create(l1), Create(l2), run_time=0.9)

        # ---- kinase OFF / phosphatase ON ---------------------------------------------------------
        self.at("A kinase phosphorylates E1")
        P = VGroup(Circle(radius=0.21, stroke_width=0, fill_color=PURPLE, fill_opacity=1), T("P", 24, BG, weight=BOLD)).move_to(kin.get_center() + DOWN * 0.1)
        blocked = Line([-0.55, ROW - 0.5, 0], [-0.55, ROW + 0.5, 0], color=RED, stroke_width=10)
        self.play(FadeIn(P, scale=0.5), run_time=0.4)
        self.play(P.animate.move_to(pdc.get_corner(UL) + np.array([0.45, -0.08, 0])), run_time=0.9)
        self.at("and inactivates it")
        self.play(pdc.animate.set_stroke(RED, 5).set_fill(RED, 0.18), *flip(False), Create(blocked), run_time=0.9)
        self.at("A phosphatase removes")
        self.play(P.animate.move_to(pho.get_bottom() + DOWN * 0.3), run_time=1.1)
        self.at("and reactivates it")
        self.play(FadeOut(P), FadeOut(blocked), pdc.animate.set_stroke(BLUE, 5).set_fill(BLUE, 0.18), *flip(True), run_time=0.9)

        # ---- reading the energy state ----------------------------------------------------------
        self.at("reads the cell's energy state")
        BAR_Y = -3.05
        bar = Line([-5.2, BAR_Y, 0], [5.2, BAR_Y, 0], color=GREY, stroke_width=4)
        left_end = T("plenty of fuel", 22, GREY).move_to([-4.2, BAR_Y - 0.4, 0])
        right_end = T("fuel needed", 22, GREY).move_to([4.2, BAR_Y - 0.4, 0])
        ptr = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1).scale(0.14).rotate(PI).move_to([0, BAR_Y + 0.2, 0])
        es = T("the cell's energy state", 26, TEXT).move_to([0, BAR_Y + 0.6, 0])
        self.play(Create(bar), FadeIn(left_end), FadeIn(right_end), FadeIn(ptr), FadeIn(es), run_time=1.2)

        self.at("When ATP")
        atp = tok("ATP", GREY).move_to([-5.35, -1.3, 0])
        acoa2 = tok("acetyl-CoA", GREY).move_to([-3.55, -1.3, 0])
        nadh = tok("NADH", GREY).move_to([-1.55, -1.3, 0])
        grp1 = VGroup(atp, acoa2, nadh)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in grp1], lag_ratio=0.45), ptr.animate.move_to([-3.6, BAR_Y + 0.2, 0]), run_time=2.0)
        self.at("plenty of fuel")
        cap1 = T("abundant: plenty of fuel and product", 24, RED).move_to([-3.2, -1.95, 0])
        self.play(FadeIn(cap1), run_time=0.6)
        self.at("the complex is inhibited")
        inhib = Line([-3.3, -0.95, 0], [-2.5, ROW - 0.8, 0], color=RED, stroke_width=6)
        tbar = Line([-2.5 - 0.2, ROW - 0.82, 0], [-2.5 + 0.2, ROW - 0.78, 0], color=RED, stroke_width=8)
        self.play(Create(inhib), Create(tbar), run_time=0.5)
        P2 = VGroup(Circle(radius=0.21, stroke_width=0, fill_color=PURPLE, fill_opacity=1), T("P", 24, BG, weight=BOLD)).move_to(pdc.get_corner(UL) + np.array([0.45, -0.08, 0]))
        self.play(pdc.animate.set_stroke(RED, 5).set_fill(RED, 0.18), *flip(False), Create(blocked), FadeIn(P2, scale=0.5), run_time=0.9)

        self.at("When ADP and pyruvate")
        self.play(FadeOut(grp1), FadeOut(cap1), FadeOut(inhib), FadeOut(tbar), run_time=0.6)
        adp = tok("ADP", GREY).move_to([2.6, -1.3, 0])
        pyr2 = tok("pyruvate", GREY).move_to([4.6, -1.3, 0])
        grp2 = VGroup(adp, pyr2)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in grp2], lag_ratio=0.5), ptr.animate.move_to([3.6, BAR_Y + 0.2, 0]), run_time=1.6)
        self.at("demand and available substrate")
        cap2 = T("accumulate: demand + substrate", 24, GREEN).move_to([3.7, -1.95, 0])
        self.play(FadeIn(cap2), run_time=0.6)
        self.at("the complex is stimulated")
        stim = Arrow([3.0, -0.95, 0], [-1.3, ROW - 0.78, 0], color=GREEN, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.12)
        self.play(GrowArrow(stim), run_time=0.5)
        self.play(pdc.animate.set_stroke(GREEN, 6).set_fill(GREEN, 0.18), *flip(True), FadeOut(blocked), FadeOut(P2), run_time=0.8)

        # ---- the gate opens ------------------------------------------------------------------------
        self.at("So the gateway")
        dots = VGroup(*[Dot(radius=0.11, color=YELLOW).move_to([-4.5, ROW, 0]) for _ in range(3)])
        self.add(dots)
        self.play(LaggedStart(*[dots[i].animate.move_to([-3.55, ROW, 0]) for i in range(3)], lag_ratio=0.3), run_time=1.0, rate_func=linear)
        self.play(FadeOut(dots), run_time=0.15)
        gdots = VGroup(*[Dot(radius=0.11, color=GREEN).move_to([-0.85, ROW, 0]) for _ in range(3)])
        self.add(gdots)
        self.play(LaggedStart(*[gdots[i].animate.move_to([3.3, ROW, 0]) for i in range(3)], lag_ratio=0.3), run_time=1.9, rate_func=linear)
        self.play(FadeOut(gdots), run_time=0.2)
        self.at("opens only when")
        self.play(Indicate(pdc, color=GREEN, scale_factor=1.06), Indicate(tcabox, color=GREEN, scale_factor=1.06), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------------------
class S05End(EndCard):
    LINE = "One gate, three enzymes, five coenzymes, one switch."
