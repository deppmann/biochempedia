"""The citric acid cycle: harvesting electrons  (Biochemistrypedia explainer)

Timed to the SPOKEN words (audio/words.json, from the real slide audio): every self.at("phrase") waits
until the narrator starts that phrase, minus a short lead.

COLOR MAP (one color per concept, whole video)
  BLUE    = the carbon backbone: the C4/C5/C6 token that travels round the cycle, and the cycle's dots
  YELLOW  = the fuel going in: the acetyl group (C2) and acetyl-CoA / pyruvate
  PINK    = high-energy electrons carried by NADH and FADH2 (filled chip = loaded; outline chip =
            empty carrier NAD+/FAD waiting to be reloaded)
  GOLD    = ATP (the cash-in-hand currency); title rule
  LIGHT   = CO2 leaving (pale grey-blue)
  ORANGE  = Stage 1, the burn (oxidation)        TEAL = Stage 2, the reset (regeneration)
  PURPLE  = the electron transport chain / oxidative phosphorylation (downstream)
  TEAL-ish O2 chip uses OXY (a distinct sea-green) so it is not confused with Stage 2
  RED     = STOP / blocked / no oxygen         GREEN = GO / open
  GREY    = rings, axes, structure, de-emphasized labels
No molecular structures are drawn: carbons are counted on labelled chips (C2, C4, C5, C6).
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
PURPLE = "#B58CD9"
PINK = "#E86AB0"
LIGHT = "#C3CAD6"
OXY = "#3FD6A0"


# ---------------------------------------------------------------- helpers
def P(c, R, deg):
    a = math.radians(deg)
    return np.array([c[0] + R * math.cos(a), c[1] + R * math.sin(a), 0.0])


def ring_arc(c, R, a0, a1, color=GREY, g0=0, g1=0, w=5, tip=True):
    """Clockwise arc from angle a0 down to a1 (degrees), shortened by g0/g1 at each end."""
    s, e = a0 - g0, a1 + g1
    arc = Arc(radius=R, start_angle=math.radians(s), angle=math.radians(e - s), arc_center=c,
              color=color, stroke_width=w)
    if tip:
        arc.add_tip(tip_length=0.2, tip_width=0.2)
    return arc


def pk(label, size=26, filled=True, pad=0.16):
    """Pink carrier chip. Filled = loaded with electrons; outline = empty."""
    return chip(label, PINK, size=size, pad=pad, fill_opacity=0.28 if filled else 0.0)


def tk(label, size=28):
    """Blue carbon-backbone token on an opaque backing, so ring lines and dots never show through it."""
    c = chip(label, BLUE, size)
    back = c[0].copy().set_fill(BG, 1.0).set_stroke(width=0)
    return VGroup(back, c)


def co2(size=24):
    return chip("CO₂", LIGHT, size=size, pad=0.14)


def arrow(a, b, color=GREY, w=3.5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.3,
                 tip_length=tip)


def heading(text, size=36):
    return T(text, size, font=TITLE_FONT).to_edge(UP, buff=0.4)


class Spin:
    """Dots circling a ring at an adjustable speed (deg/s). Stop with speed.set_value(0)."""

    def __init__(self, scene, c, R, n=3, color=BLUE, speed=70, r=0.13):
        self.phase = ValueTracker(0)
        self.speed = ValueTracker(speed)
        self.c, self.R = c, R
        self.driver = Mobject()
        self.driver.add_updater(lambda m, dt: self.phase.increment_value(self.speed.get_value() * dt))
        self.dots = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
        for i, d in enumerate(self.dots):
            d.add_updater(lambda m, i=i: m.move_to(P(self.c, self.R, 90 - self.phase.get_value() - (360 / n) * i)))
        scene.add(self.driver, self.dots)

    def stop(self):
        self.speed.set_value(0)


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The citric acid cycle"
    TITLE = "Harvesting electrons"


# --------------------------------------------------------------------------------------------
class S01Job(SpokenScene):
    """The ring: C2 joins C4 -> C6 -> C5 -> C4; every carbon lost banks electrons; one GTP (worth one ATP) is the only direct payout."""

    def construct(self):
        C = np.array([-0.8, -0.7, 0])
        R = 2.1
        ND = {"oaa": 110, "c6": 50, "c5": -15, "c4": -90}
        arcs = VGroup(ring_arc(C, R, 110, 50, GREY, 13, 13), ring_arc(C, R, 50, -15, GREY, 13, 13),
                      ring_arc(C, R, -15, -90, GREY, 13, 13), ring_arc(C, R, -90, -250, GREY, 13, 13))
        mid = T("citric acid\ncycle", 28, GREY).move_to(C)
        head = heading("Harvest high-energy electrons")

        self.play(Create(arcs, lag_ratio=0.25), FadeIn(mid), run_time=1.6)

        self.at("Harvest high energy electrons")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.7)

        # ---- an acetyl fragment enters and condenses onto a four-carbon receiver -> six carbons
        self.at("carbon acetyl")
        acetyl = chip("C₂ acetyl", YELLOW, 26).move_to(P(C, R, 110) + np.array([-0.2, 1.3, 0]))
        self.play(FadeIn(acetyl, shift=DOWN * 0.2), run_time=0.6)
        self.at("four carbon receiver")
        tok = tk("C₄").move_to(P(C, R, ND["oaa"]))
        oaa_lbl = T("oxaloacetate", 24, GREY).next_to(tok, LEFT, buff=0.2)
        self.play(FadeIn(tok, scale=0.7), FadeIn(oaa_lbl), run_time=0.6)
        self.play(Indicate(tok[1], color=BLUE, scale_factor=1.15), run_time=0.7)
        self.at("make six carbons")
        self.play(acetyl.animate.move_to(tok).scale(0.5).set_opacity(0), run_time=0.45)
        self.remove(acetyl)
        self.play(Transform(tok, tk("C₆").move_to(P(C, R, ND["c6"])), path_arc=-math.radians(60)),
                  run_time=0.9)

        # ---- around the ring we lose two carbons as CO2 and shrink back down
        self.at("lose two carbons")
        co2a = co2().move_to([2.8, -0.35, 0])
        a_co2a = arrow(P(C, R, 0), co2a.get_left(), LIGHT)
        self.play(Transform(tok, tk("C₅").move_to(P(C, R, ND["c5"])), path_arc=-math.radians(65)),
                  FadeIn(co2a, shift=RIGHT * 0.2), GrowArrow(a_co2a), run_time=1.0)
        self.at("shrink back down")
        co2b = co2().move_to([2.8, -2.7, 0])
        a_co2b = arrow(P(C, R, -70), co2b.get_left(), LIGHT)
        self.play(Transform(tok, tk("C₄").move_to(P(C, R, ND["c4"])), path_arc=-math.radians(75)),
                  FadeIn(co2b, shift=RIGHT * 0.2), GrowArrow(a_co2b), run_time=1.0)

        # ---- we capture electrons in NADH and FADH2 and squeeze out a single GTP, worth one ATP
        self.at("NADH")
        n1 = pk("NADH").move_to([2.8, 0.75, 0])
        n2 = pk("NADH").move_to([2.8, -1.6, 0])
        n3 = pk("NADH").move_to([-4.2, 0.3, 0])
        a_n1 = arrow(P(C, R, 35), n1.get_left(), PINK)
        a_n2 = arrow(P(C, R, -40), n2.get_left(), PINK)
        a_n3 = arrow(P(C, R, 150), n3.get_right(), PINK)
        self.play(FadeIn(n1, scale=0.7), GrowArrow(a_n1), run_time=0.3)
        self.play(FadeIn(n2, scale=0.7), GrowArrow(a_n2), run_time=0.3)
        self.play(FadeIn(n3, scale=0.7), GrowArrow(a_n3), run_time=0.3)
        self.at("FADH2", 0.4)
        fad = pk("FADH₂").move_to([-4.2, -0.9, 0])
        a_fad = arrow(P(C, R, 180), fad.get_right(), PINK)
        self.play(FadeIn(fad, scale=0.7), GrowArrow(a_fad), run_time=0.5)
        self.at("squeeze out")
        atp = chip("GTP", GOLD, 26, pad=0.16).move_to([-4.2, -2.3, 0])
        a_atp = arrow(P(C, R, -130), atp.get_right(), GOLD)
        # the label steps aside while the token rides the ring home, so the two never overlap
        self.play(Transform(tok, tk("C₄").move_to(P(C, R, ND["oaa"])), path_arc=-math.radians(160)),
                  oaa_lbl.animate(rate_func=rush_from).set_opacity(0), run_time=0.9)
        self.at("single GTP")
        self.play(FadeIn(atp, scale=0.7), GrowArrow(a_atp), oaa_lbl.animate.set_opacity(1), run_time=0.6)
        self.at("worth one ATP")
        atp_eq = T("= 1 ATP", 24, GOLD).next_to(atp, DOWN, buff=0.15)
        self.play(FadeIn(atp_eq, shift=UP * 0.1), run_time=0.5)
        self.play(Indicate(oaa_lbl, color=BLUE), run_time=0.7)

        # ---- the carbon bookkeeping along the rim: six to five to four
        self.at("carbon bookkeeping")
        g6 = chip("C₆", GREY, 28, fill_opacity=0.0).move_to(P(C, R, 50))
        g5 = chip("C₅", GREY, 28, fill_opacity=0.0).move_to(P(C, R, -15))
        g4 = chip("C₄", GREY, 28, fill_opacity=0.0).move_to(P(C, R, -90))
        self.play(FadeIn(g6), FadeIn(g5), FadeIn(g4), run_time=0.7)
        self.at("6 to")
        self.play(g6.animate.set_color(BLUE), run_time=0.3)
        self.at("5 to")
        self.play(g5.animate.set_color(BLUE), run_time=0.3)
        self.at("to 4")
        self.play(g4.animate.set_color(BLUE), run_time=0.3)

        # ---- every step that drops a carbon also banks reducing power
        self.at("every step that drops")
        self.play(Indicate(co2a, color=LIGHT), Indicate(co2b, color=LIGHT), run_time=0.9)
        self.at("banks reducing power")
        self.play(Indicate(n1, color=PINK), Indicate(n2, color=PINK), run_time=0.9)

        # ---- not really about making ATP directly: an electron-harvesting machine feeding the next stage
        self.at("not really about")
        self.play(atp.animate.scale(0.75).set_opacity(0.35), atp_eq.animate.set_opacity(0.35), FadeOut(a_atp), run_time=0.8)
        self.at("electron harvesting machine")
        rim = VGroup(arcs, mid, tok, g6, g5, g4, oaa_lbl, co2a, co2b, a_co2a, a_co2b, a_n1, a_n2, a_n3,
                     a_fad, atp, atp_eq)
        col = [1.25, 0.35, -0.55, -1.45]
        self.play(rim.animate.set_opacity(0.0),
                  n1.animate.move_to([-1.3, col[0], 0]).scale(1.15),
                  n2.animate.move_to([-1.3, col[1], 0]).scale(1.15),
                  n3.animate.move_to([-1.3, col[2], 0]).scale(1.15),
                  fad.animate.move_to([-1.3, col[3], 0]).scale(1.15), run_time=1.3)
        self.at("feeding the next stage")
        etc = chip("next stage:\nelectron\ntransport chain", PURPLE, 26, pad=0.25).move_to([2.5, -0.1, 0])
        brace = VGroup(*[arrow(p.get_right(), etc.get_left() + np.array([0, (p.get_y() + 0.1) * 0.35, 0]), PINK)
                         for p in (n1, n2, n3, fad)])
        self.play(FadeIn(etc, shift=LEFT * 0.3), *[GrowArrow(a) for a in brace], run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S02Stages(SpokenScene):
    """Eight steps, two halves: Stage 1 burns two carbons, Stage 2 rebuilds oxaloacetate."""

    def construct(self):
        C = np.array([0.0, -0.5, 0])
        R = 2.1
        ang = [90 - 45 * k for k in range(9)]      # node angles, node 8 == node 0
        arcs = [ring_arc(C, R, ang[k], ang[k + 1], GREY, 7, 7, w=5) for k in range(8)]
        dots = VGroup(*[Dot(P(C, R, ang[k]), radius=0.08, color=GREY) for k in range(8)])
        nums = VGroup(*[T(str(k + 1), 24, GREY).move_to(P(C, R - 0.5, (ang[k] + ang[k + 1]) / 2)) for k in range(8)])
        head = heading("A two-stage machine")

        self.play(Create(VGroup(*arcs), lag_ratio=0.1), FadeIn(dots), FadeIn(nums), run_time=0.9)
        self.at("two stage machine")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.6)

        # ---- stage one: oxidation
        self.at("In stage one")
        shade1 = AnnularSector(inner_radius=R - 0.75, outer_radius=R + 0.6, angle=PI, start_angle=-PI / 2,
                               arc_center=C, color=ORANGE, fill_opacity=0.13, stroke_width=0)
        s1a = T("STAGE 1", 32, ORANGE, weight=BOLD)
        s1b = T("Oxidation", 28, TEXT)
        s1 = VGroup(s1a, s1b).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([4.55, 2.35, 0])
        self.play(FadeIn(shade1), *[arcs[k].animate.set_color(ORANGE) for k in range(4)], FadeIn(s1a, shift=LEFT * 0.2),
                  run_time=0.8)
        self.at("oxidation")
        self.play(FadeIn(s1b, shift=LEFT * 0.2), run_time=0.5)

        self.at("two carbons are introduced")
        acetyl = chip("C₂ acetyl", YELLOW, 26).move_to([-3.0, 2.5, 0])
        self.play(FadeIn(acetyl, shift=DOWN * 0.2), run_time=0.6)
        self.at("onto oxaloacetate")
        tok = tk("C₄").move_to(P(C, R, 90))
        oaa_lbl = T("oxaloacetate", 24, GREY).move_to(tok.get_center() + np.array([1.35, 0.62, 0]))
        self.play(FadeIn(tok, scale=0.7), FadeIn(oaa_lbl), acetyl.animate.move_to([-1.6, 2.15, 0]), run_time=0.8)
        self.at("to form citrate")
        self.play(acetyl.animate.move_to(tok).scale(0.5).set_opacity(0), run_time=0.4)
        self.remove(acetyl)
        cit_lbl = T("citrate", 24, GREY)
        self.play(Transform(tok, tk("C₆").move_to(P(C, R, 45)), path_arc=-math.radians(45)),
                  FadeOut(oaa_lbl), run_time=0.8)
        cit_lbl.next_to(tok, RIGHT, buff=0.25)
        self.play(FadeIn(cit_lbl), run_time=0.4)

        self.at("two oxidative")
        self.play(Transform(tok, tk("C₆").move_to(P(C, R, 0)), path_arc=-math.radians(45)),
                  FadeOut(cit_lbl), run_time=0.7)
        self.at("decarboxylations")
        co2a = co2().move_to([3.6, -0.55, 0])
        a1 = arrow(P(C, R, -22), co2a.get_left(), LIGHT)
        self.play(Transform(tok, tk("C₅").move_to(P(C, R, -45)), path_arc=-math.radians(45)),
                  FadeIn(co2a, shift=RIGHT * 0.2), GrowArrow(a1), run_time=0.9)
        self.at("burning off two")
        co2b = co2().move_to([3.6, -1.75, 0])
        a2 = arrow(P(C, R, -67), co2b.get_left(), LIGHT)
        self.play(Transform(tok, tk("C₄").move_to(P(C, R, -90)), path_arc=-math.radians(45)),
                  FadeIn(co2b, shift=RIGHT * 0.2), GrowArrow(a2), run_time=0.9)
        self.at("burn carbon")
        s1c = T("burn the carbons", 26, ORANGE).next_to(s1b, DOWN, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(s1c, shift=LEFT * 0.2), run_time=0.6)

        # ---- stage two: regeneration
        self.at("Stage two")
        shade2 = AnnularSector(inner_radius=R - 0.75, outer_radius=R + 0.6, angle=PI, start_angle=PI / 2,
                               arc_center=C, color=TEAL, fill_opacity=0.13, stroke_width=0)
        s2a = T("STAGE 2", 32, TEAL, weight=BOLD)
        s2b = T("Regeneration", 28, TEXT)
        s2 = VGroup(s2a, s2b).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-4.55, 2.35, 0])
        s2.align_to(np.array([-6.2, 0, 0]), LEFT)
        self.play(FadeIn(shade2), *[arcs[k].animate.set_color(TEAL) for k in range(4, 8)],
                  FadeIn(s2a, shift=RIGHT * 0.2), run_time=0.8)
        self.at("regeneration")
        self.play(FadeIn(s2b, shift=RIGHT * 0.2), run_time=0.5)
        self.at("rebuilding the catalyst")
        s2c = T("rebuild the catalyst", 26, TEAL).next_to(s2b, DOWN, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(s2c, shift=RIGHT * 0.2), run_time=0.6)
        self.at("remaining backbone")
        for k in range(4, 8):
            self.play(Transform(tok, tk("C₄").move_to(P(C, R, ang[k + 1])), path_arc=-math.radians(45)),
                      run_time=0.7)
        self.at("until oxaloacetate")
        oaa_lbl2 = T("oxaloacetate", 24, GREY).move_to(tok.get_center() + np.array([1.35, 0.62, 0]))
        self.play(FadeIn(oaa_lbl2), Indicate(tok[1], color=BLUE, scale_factor=1.15), run_time=0.8)
        self.at("ready to accept")
        acetyl2 = chip("C₂ acetyl", YELLOW, 26).move_to([-3.0, 2.5, 0])
        self.play(FadeIn(acetyl2, shift=DOWN * 0.2), acetyl2.animate.move_to([-1.6, 2.15, 0]), run_time=0.9)

        # ---- the dividing line
        self.at("dividing line")
        d_top = DashedLine([0, 1.1, 0], [0, 0.0, 0], color=TEXT, stroke_width=3, dash_length=0.12)
        d_bot = DashedLine([0, -1.0, 0], [0, -2.1, 0], color=TEXT, stroke_width=3, dash_length=0.12)
        bnd = T("stage boundary", 24, TEXT).move_to([0, -0.5, 0])
        self.play(Create(d_top), Create(d_bot), FadeIn(bnd), run_time=0.9)

        # ---- both halves bank electrons for oxidative phosphorylation
        self.at("Both halves matter")
        self.play(FadeOut(co2a), FadeOut(co2b), FadeOut(a1), FadeOut(a2), FadeOut(acetyl2),
                  Indicate(s1a, color=ORANGE), Indicate(s2a, color=TEAL), run_time=1.0)
        self.at("high energy electrons")
        r1 = pk("NADH").move_to([4.3, -0.3, 0])
        r2 = pk("NADH").move_to([4.3, -1.15, 0])
        l1 = pk("NADH").move_to([-4.3, 0.45, 0])
        l2 = pk("FADH₂").move_to([-4.3, -1.0, 0])
        ar1 = arrow(P(C, R, -22), r1.get_left(), PINK)
        ar2 = arrow(P(C, R, -67), r2.get_left(), PINK)
        al1 = arrow(P(C, R + 0.08, 118), l1.get_right(), PINK)
        al2 = arrow(P(C, R, -157.5), l2.get_right(), PINK)
        self.play(*[FadeIn(m, scale=0.7) for m in (r1, r2, l1, l2)], *[GrowArrow(a) for a in (ar1, ar2, al1, al2)],
                  run_time=1.0)
        self.at("power ATP synthesis")
        fade = VGroup(*arcs, dots, nums, shade1, shade2, tok, oaa_lbl2, d_top, d_bot, bnd, ar1, ar2, al1, al2,
                      s1a, s1b, s1c, s2a, s2b, s2c, head)
        self.play(FadeOut(fade),
                  r1.animate.move_to([-3.6, 0.9, 0]), r2.animate.move_to([-3.6, 0.05, 0]),
                  l1.animate.move_to([-3.6, -0.8, 0]), l2.animate.move_to([-3.6, -1.65, 0]), run_time=1.2)
        ox = chip("oxidative\nphosphorylation", PURPLE, 28, pad=0.28).move_to([1.2, -0.3, 0])
        atp = chip("ATP", GOLD, 30, pad=0.22).move_to([5.0, -0.3, 0])
        arr_in = VGroup(*[arrow(p.get_right(), ox.get_left() + np.array([0, (p.get_y() + 0.3) * 0.3, 0]), PINK)
                          for p in (r1, r2, l1, l2)])
        self.play(FadeIn(ox, shift=LEFT * 0.3), *[GrowArrow(a) for a in arr_in], run_time=0.9)
        a_out = arrow(ox.get_right(), atp.get_left(), GOLD)
        self.play(GrowArrow(a_out), FadeIn(atp, scale=0.7), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S03Throttle(SpokenScene):
    """Energy balance sets the speed: ATP/NADH high -> brakes on the committed steps; ADP high -> brakes off."""

    def construct(self):
        C = np.array([-2.2, -0.3, 0])
        R = 1.9
        ang = [90 - 45 * k for k in range(9)]
        arcs = VGroup(*[ring_arc(C, R, ang[k], ang[k + 1], GREY, 7, 7, w=5) for k in range(8)])
        mid = T("citric acid\ncycle", 26, GREY).move_to(C)
        head = heading("The cycle follows the cell's energy", 32)

        # --- gauge on the right (low <-> high energy)
        GX0, GX1, GY = 0.9, 6.0, 2.05
        gauge = Line([GX0, GY, 0], [GX1, GY, 0], color=GREY, stroke_width=6)
        gl = T("low energy", 24, GREY).move_to([GX0 + 0.85, GY - 0.55, 0])
        gh = T("high energy", 24, GREY).move_to([GX1 - 0.9, GY - 0.55, 0])
        gt = T("cell's energy balance", 26, TEXT).move_to([(GX0 + GX1) / 2, GY + 0.68, 0])
        level = ValueTracker(0.5)
        marker = Triangle(color=GOLD, fill_opacity=1.0, stroke_width=0).scale(0.2).rotate(PI)
        marker.add_updater(lambda m: m.move_to([GX0 + (GX1 - GX0) * level.get_value(), GY + 0.22, 0]))

        # --- signal bars (a bar chart of the three signals)
        BX0, BW = 2.9, 3.2
        rows = {"ATP": 0.35, "NADH": -0.3, "ADP": -0.95}
        vals = {"ATP": ValueTracker(0.5), "NADH": ValueTracker(0.5), "ADP": ValueTracker(0.5)}
        cols = {"ATP": GOLD, "NADH": PINK, "ADP": GOLD}
        bar_items = []
        for name, y in rows.items():
            lab = T(name, 26, cols[name]).move_to([BX0 - 0.15, y, 0], aligned_edge=RIGHT)
            frame = Rectangle(width=BW, height=0.34, stroke_color=GREY, stroke_width=2).move_to([BX0 + BW / 2, y, 0])
            fill = always_redraw(lambda n=name, y=y: Rectangle(
                width=max(0.02, BW * vals[n].get_value()), height=0.24, stroke_width=0, fill_color=cols[n],
                fill_opacity=0.9 if n != "ADP" else 0.45).move_to([BX0 + max(0.02, BW * vals[n].get_value()) / 2, y, 0]))
            bar_items += [lab, frame, fill]
        rate = ValueTracker(0.5)
        rate_lab = T("cycle rate", 26, BLUE).move_to([BX0 - 0.15, -2.1, 0], aligned_edge=RIGHT)
        rate_frame = Rectangle(width=BW, height=0.34, stroke_color=GREY, stroke_width=2).move_to([BX0 + BW / 2, -2.1, 0])
        rate_fill = always_redraw(lambda: Rectangle(
            width=max(0.02, BW * rate.get_value()), height=0.24, stroke_width=0, fill_color=BLUE, fill_opacity=0.9
        ).move_to([BX0 + max(0.02, BW * rate.get_value()) / 2, -2.1, 0]))
        sep = Line([0.9, -1.5, 0], [6.1, -1.5, 0], color=GREY, stroke_width=1.5)

        # --- gates (brakes) on the two committed steps; PDH gate appears later
        def gate(pos, closed=False):
            g = Square(0.42, stroke_width=3)
            g.move_to(pos)
            g.set_color(RED if closed else GREEN).set_fill(RED if closed else GREEN, 0.25)
            return g

        g3 = gate(P(C, R, -22.5))
        g4 = gate(P(C, R, -67.5))
        l3 = T("step 3", 24, GREY).next_to(g3, RIGHT, buff=0.2)
        l4 = T("step 4", 24, GREY).next_to(g4, DOWN, buff=0.18)

        spin = Spin(self, C, R, speed=70)
        spin.dots.set_opacity(0)

        self.at("regulation of the")
        self.play(Create(arcs, lag_ratio=0.1), FadeIn(mid), FadeIn(head, shift=DOWN * 0.15), run_time=1.4)
        spin.dots.set_opacity(1)
        self.play(FadeIn(rate_lab), FadeIn(rate_frame), FadeIn(rate_fill), run_time=0.6)

        self.at("tracks the cell's energy")
        self.play(FadeIn(gauge), FadeIn(gl), FadeIn(gh), FadeIn(gt), FadeIn(marker), run_time=0.9)

        # ---- high-energy state
        self.at("In a high energy state")
        self.play(*[FadeIn(m) for m in (sep,)], *[FadeIn(m) for m in bar_items], FadeIn(g3), FadeIn(g4), FadeIn(l3),
                  FadeIn(l4), level.animate.set_value(0.92), run_time=1.2)
        self.at("ATP and NADH")
        self.play(vals["ATP"].animate.set_value(0.92), vals["NADH"].animate.set_value(0.88),
                  vals["ADP"].animate.set_value(0.1), run_time=1.2)
        self.at("burn more fuel")
        note = T("plenty of ATP: no need to burn more", 24, TEXT).move_to([3.5, 1.02, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.at("act as signals")
        self.play(Indicate(bar_items[0], color=GOLD), Indicate(bar_items[3], color=PINK), run_time=0.9)
        self.at("slow the cycle down")
        self.play(FadeOut(note), rate.animate.set_value(0.06), spin.speed.animate.set_value(8),
                  *[g.animate.set_color(RED).set_fill(RED, 0.55) for g in (g3, g4)], run_time=1.6)
        self.at("committed irreversible")
        self.play(Indicate(g3, color=RED, scale_factor=1.5), Indicate(g4, color=RED, scale_factor=1.5), run_time=1.0)

        # ---- low-energy state
        self.at("In a low energy state")
        self.play(level.animate.set_value(0.08), vals["ATP"].animate.set_value(0.2),
                  vals["NADH"].animate.set_value(0.2), run_time=1.3)
        self.at("when ADP piles up")
        self.play(vals["ADP"].animate.set_value(0.92), run_time=1.0)
        self.at("ATP is scarce")
        self.play(Indicate(bar_items[0], color=GOLD), run_time=0.9)
        self.at("the brakes come off")
        self.play(*[g.animate.set_color(GREEN).set_fill(GREEN, 0.25) for g in (g3, g4)], run_time=0.6)
        self.at("speeds up")
        self.play(rate.animate.set_value(0.95), spin.speed.animate.set_value(220), run_time=0.6)
        self.at("to regenerate ATP")
        self.play(vals["ATP"].animate.set_value(0.5), run_time=1.2)

        # ---- the same logic upstream at pyruvate dehydrogenase
        self.at("pyruvate dehydrogenase")
        entry_b = P(C, R, 90) + np.array([-0.4, 0.3, 0])
        acoa = chip("pyruvate", YELLOW, 24, pad=0.14).move_to([-4.9, 2.45, 0])
        e_arr = arrow(acoa.get_right(), entry_b, YELLOW)
        gp = gate((acoa.get_right() + entry_b) / 2)
        gp.set_color(GREEN).set_fill(GREEN, 0.25)
        lp = T("PDH", 24, GREY).next_to(gp, UP, buff=0.16)
        self.play(FadeIn(acoa), GrowArrow(e_arr), FadeIn(gp), FadeIn(lp), run_time=1.0)
        self.at("feeding into the cycle")
        self.play(level.animate.set_value(0.92), vals["ATP"].animate.set_value(0.92),
                  vals["NADH"].animate.set_value(0.88), vals["ADP"].animate.set_value(0.1),
                  rate.animate.set_value(0.06), spin.speed.animate.set_value(8),
                  *[g.animate.set_color(RED).set_fill(RED, 0.55) for g in (g3, g4, gp)], run_time=1.4)
        self.at("stay matched")
        self.play(level.animate.set_value(0.08), vals["ATP"].animate.set_value(0.4),
                  vals["NADH"].animate.set_value(0.2), vals["ADP"].animate.set_value(0.9),
                  rate.animate.set_value(0.95), spin.speed.animate.set_value(200),
                  *[g.animate.set_color(GREEN).set_fill(GREEN, 0.25) for g in (g3, g4, gp)], run_time=1.4)
        self.at("Supply chases demand")
        self.play(Indicate(e_arr, color=YELLOW, scale_factor=1.15), Circumscribe(rate_frame, color=BLUE), run_time=1.2)
        self.at("controls sit exactly")
        self.play(*[Indicate(g, color=GOLD, scale_factor=1.7) for g in (gp, g3, g4)], run_time=1.4)
        self.finish()


# --------------------------------------------------------------------------------------------
class S04Oxygen(SpokenScene):
    """Why a cycle with no oxygen in it stops without oxygen: the carrier loop through the ETC."""

    def construct(self):
        CC = np.array([-5.0, 0.5, 0])
        RC = 1.1
        EP = np.array([1.0, 0.5, 0])
        OP = np.array([5.6, 0.5, 0])
        LANE_Y = -2.3
        head = heading("Where is the oxygen?")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.7)

        ring = Circle(radius=RC, color=GREY, stroke_width=5).move_to(CC)
        name = T("citric acid\ncycle", 26, GREY).move_to(CC)
        spin = Spin(self, CC, RC, speed=80, r=0.12)
        spin.dots.set_opacity(0)
        etc = chip("electron\ntransport chain", PURPLE, 28, pad=0.3).move_to(EP)
        o2 = chip("O₂", OXY, 30, pad=0.2).move_to(OP)

        # ---- oxygen never appears in the cycle, yet the cycle is strictly aerobic
        self.at("Oxygen never")
        self.play(FadeIn(ring), FadeIn(name), FadeIn(o2, scale=0.7), run_time=0.7)
        spin.dots.set_opacity(1)
        self.at("never appears anywhere")
        ghost = chip("O₂", OXY, 28, pad=0.18).move_to(CC + np.array([3.0, 1.0, 0]))
        cross = VGroup(Line(ghost.get_corner(UL), ghost.get_corner(DR), color=RED, stroke_width=6),
                       Line(ghost.get_corner(UR), ghost.get_corner(DL), color=RED, stroke_width=6))
        no_lbl = T("no O₂ in the cycle", 24, TEXT).next_to(ghost, DOWN, buff=0.15)
        self.play(FadeIn(ghost, scale=0.7), run_time=0.4)
        self.play(Create(cross), FadeIn(no_lbl), run_time=0.5)
        self.at("strictly aerobic")
        aer = T("strictly aerobic", 26, TEXT).next_to(ring, DOWN, buff=0.3)
        self.play(FadeOut(ghost), FadeOut(cross), FadeOut(no_lbl), FadeIn(aer), run_time=0.7)
        self.at("Why")
        why = T("Why?", 56, YELLOW, font=TITLE_FONT).move_to([0.5, 1.9, 0])
        self.play(FadeIn(why, scale=0.8), run_time=0.5)

        # ---- the cycle makes NADH and FADH2 but needs NAD+ and FAD back
        self.at("produces NADH")
        nad_red = pk("NADH", 26).move_to(CC + np.array([2.2, 0.75, 0]))
        self.play(FadeOut(why), FadeOut(aer), FadeIn(nad_red, shift=RIGHT * 0.3), run_time=0.5)
        self.at("FADH2")
        fad_red = pk("FADH₂", 26).move_to(CC + np.array([2.2, -0.15, 0]))
        self.play(FadeIn(fad_red, shift=RIGHT * 0.3), run_time=0.5)
        self.at("gets NAD")
        lane_bot = VMobject(color=GREY, stroke_width=3).set_points_as_corners(
            [[EP[0], EP[1] - 0.75, 0], [EP[0], LANE_Y, 0], [CC[0], LANE_Y, 0], [CC[0], CC[1] - RC - 0.28, 0]])
        lane_tip = Arrow([CC[0], LANE_Y + 0.9, 0], [CC[0], CC[1] - RC - 0.02, 0], color=GREY, stroke_width=3,
                         buff=0, tip_length=0.2)
        ph = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=3.3, height=1.5, stroke_color=GREY,
                                             stroke_width=2.5).move_to(EP), num_dashes=36)
        ph_q = T("?", 44, GREY).move_to(EP)
        g_nad = pk("NAD⁺", 26, filled=False).move_to([-0.6, LANE_Y, 0])
        g_fad = pk("FAD", 26, filled=False).move_to([-2.6, LANE_Y, 0])
        for g in (g_nad, g_fad):
            g[0].set_stroke(opacity=0.5)
            g[1].set_opacity(0.5)
        need_lab = T("needed back", 24, GREY).move_to([-1.6, LANE_Y - 0.5, 0])
        self.play(FadeIn(ph), FadeIn(ph_q), Create(lane_bot), FadeIn(lane_tip), FadeIn(g_nad), FadeIn(g_fad),
                  FadeIn(need_lab), run_time=1.0)

        # ---- the ETC regenerates the carriers, and hands its electrons to oxygen
        self.at("the electron transport chain")
        self.play(FadeTransform(VGroup(ph, ph_q), etc), run_time=0.8)
        self.at("oxidizes")
        lane_top = Line([CC[0] + RC + 0.1, 0.5, 0], [EP[0] - 1.7, 0.5, 0], color=PINK, stroke_width=3)
        self.play(Create(lane_top), run_time=0.3)
        self.play(nad_red.animate.move_to([EP[0] - 1.1, 0.8, 0]).scale(0.5).set_opacity(0.0),
                  fad_red.animate.move_to([EP[0] - 1.1, 0.3, 0]).scale(0.5).set_opacity(0.0),
                  g_nad[0].animate.set_stroke(opacity=1.0), g_nad[1].animate.set_opacity(1.0),
                  g_fad[0].animate.set_stroke(opacity=1.0), g_fad[1].animate.set_opacity(1.0),
                  FadeOut(need_lab), FadeOut(lane_top), run_time=0.9)
        self.play(g_nad.animate.move_to([CC[0] + 0.9, LANE_Y, 0]), g_fad.animate.move_to([CC[0] - 0.9, LANE_Y, 0]),
                  run_time=0.7)
        self.play(g_nad.animate.move_to([CC[0], CC[1] - RC - 0.5, 0]),
                  FadeOut(g_fad), run_time=0.6)
        self.play(FadeOut(g_nad), run_time=0.2)
        self.at("hands its electrons")
        e_arr = arrow(etc.get_right(), o2.get_left(), PINK)
        e_lab = T("e⁻", 28, PINK).next_to(e_arr, UP, buff=0.1)
        dots = VGroup(*[Dot(radius=0.1, color=PINK).move_to(etc.get_right() + np.array([0.15, 0, 0])) for _ in range(3)])
        self.play(GrowArrow(e_arr), FadeIn(e_lab), run_time=0.4)
        self.add(dots)
        end = o2.get_left() + np.array([-0.15, 0, 0])
        self.play(LaggedStart(*[d.animate.move_to(end) for d in dots], lag_ratio=0.35), run_time=1.6)
        self.play(FadeOut(dots), o2.animate.scale(1.2), run_time=0.3)
        self.play(o2.animate.scale(1 / 1.2), run_time=0.2)

        # ---- remove oxygen: the chain backs up and the cycle halts
        self.at("Remove oxygen")
        ocross = VGroup(Line(o2.get_corner(UL), o2.get_corner(DR), color=RED, stroke_width=7),
                        Line(o2.get_corner(UR), o2.get_corner(DL), color=RED, stroke_width=7))
        self.play(o2.animate.set_opacity(0.35), Create(ocross), e_arr.animate.set_color(GREY).set_opacity(0.4),
                  FadeOut(e_lab), run_time=0.9)
        self.at("the chain backs up")
        q1 = pk("NADH", 26).move_to([EP[0] - 2.5, 0.5, 0])
        q2 = pk("FADH₂", 26).move_to([EP[0] - 4.0, 0.5, 0])
        q3 = pk("NADH", 26).move_to([EP[0] - 3.25, 1.45, 0])
        queue = VGroup(q1, q2, q3)
        self.play(etc[0].animate.set_color(RED), FadeIn(queue, shift=RIGHT * 0.4, lag_ratio=0.3), run_time=1.0)
        self.at("the carriers stay reduced")
        q_lab = T("all still loaded", 24, PINK).move_to([EP[0] - 3.25, 2.15, 0])
        self.play(FadeIn(q_lab), Indicate(queue, color=PINK, scale_factor=1.1), run_time=0.9)
        self.at("never return")
        none_lab = T("no NAD⁺, no FAD", 26, RED).move_to([-1.8, LANE_Y - 0.5, 0])
        self.play(lane_bot.animate.set_color(RED), lane_tip.animate.set_color(RED), FadeIn(none_lab), run_time=0.9)
        self.at("the cycle grinds")
        halt = T("HALT", 36, RED, weight=BOLD).move_to(CC)
        self.play(spin.speed.animate.set_value(0), ring.animate.set_color(RED), FadeOut(name),
                  FadeIn(halt, scale=0.8), run_time=0.9)

        # ---- indirect dependence: O2 -> ETC -> carriers -> cycle
        self.at("depends")
        everything = Group(*[m for m in self.mobjects])
        self.play(FadeOut(everything), run_time=0.5)
        items = [chip("O₂", OXY, 32, pad=0.22), chip("electron\ntransport chain", PURPLE, 28, pad=0.25),
                 chip("NAD⁺ and FAD", PINK, 28, pad=0.25, fill_opacity=0.0), chip("citric acid\ncycle", BLUE, 28, pad=0.25)]
        row = VGroup(*items).arrange(RIGHT, buff=0.7).move_to([0, -0.2, 0])
        fit(row, max_w=12.4)
        arrs = [arrow(row[i].get_right(), row[i + 1].get_left(), GREY) for i in range(3)]
        h2 = T("an indirect dependence", 38, font=TITLE_FONT).move_to([0, 1.9, 0])
        self.add(h2.set_opacity(0))
        self.at("on oxygen indirectly")
        self.play(h2.animate.set_opacity(1), FadeIn(row[0], scale=0.8), run_time=0.7)
        self.play(GrowArrow(arrs[0]), FadeIn(row[1], shift=RIGHT * 0.2), run_time=0.5)
        self.at("through the carriers")
        self.play(GrowArrow(arrs[1]), FadeIn(row[2], shift=RIGHT * 0.2), run_time=0.5)
        self.at("it must recycle")
        self.play(GrowArrow(arrs[2]), FadeIn(row[3], shift=RIGHT * 0.2), run_time=0.6)
        self.finish()


# --------------------------------------------------------------------------------------------
class S05Cash(SpokenScene):
    """The cycle banks electrons; the ETC cashes them in. Exchange rate: NADH ~2.5 ATP, FADH2 ~1.5 ATP."""

    def construct(self):
        head = heading("The cell trades in currencies", 32)

        # layout: pipeline on the top row, exchange rates bottom-left, ATP tally bottom-right
        CC = np.array([-5.0, 1.45, 0])
        ring = Circle(radius=0.7, color=GREY, stroke_width=5).move_to(CC)
        spin = Spin(self, CC, 0.7, n=2, speed=90, r=0.1)
        spin.dots.set_opacity(0)
        cname = T("citric acid cycle", 24, GREY).move_to(CC + np.array([0.3, 1.2, 0]))
        bank = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.6, stroke_color=GREY, stroke_width=2.5,
                                fill_color=GREY, fill_opacity=0.06).move_to([-2.2, 1.45, 0])
        bank_lab = T("bank", 24, GREY).next_to(bank, UP, buff=0.1)
        etc = chip("electron\ntransport chain", PURPLE, 26, pad=0.25).move_to([1.9, 1.45, 0])

        # ---- currencies
        self.at("financially literate")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.7)
        self.at("converting between currencies")
        c1 = chip("ATP", GOLD, 32, pad=0.22).move_to([-2.6, 0.2, 0])
        c2 = pk("NADH", 32, pad=0.22).move_to([2.6, 0.2, 0])
        dbl = DoubleArrow(c1.get_right(), c2.get_left(), buff=0.15, color=GREY, stroke_width=4)
        self.play(FadeIn(c1, shift=RIGHT * 0.3), FadeIn(c2, shift=LEFT * 0.3), GrowFromCenter(dbl), run_time=1.0)

        # ---- the cycle hands off the charge
        self.at("The citric acid cycle")
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(dbl), FadeIn(ring), FadeIn(cname), FadeIn(bank), FadeIn(bank_lab),
                  run_time=0.8)
        spin.dots.set_opacity(1)
        self.at("hands off")
        b1 = pk("NADH", 22, pad=0.1).move_to(CC)
        slots = [[-2.85, 1.75, 0], [-1.55, 1.75, 0], [-2.85, 1.15, 0], [-1.55, 1.15, 0]]
        items = [b1] + [pk(t, 22, pad=0.1).move_to(CC) for t in ("NADH", "NADH", "FADH₂")]
        self.play(AnimationGroup(*[Succession(FadeIn(it, scale=0.6), it.animate.move_to(slots[i]))
                                   for i, it in enumerate(items)], lag_ratio=0.3), run_time=2.0)

        # ---- the single ATP is cash in hand; the rest is reducing power
        self.at("cash in hand")
        coin = chip("ATP/GTP", GOLD, 24, pad=0.14).move_to(CC + np.array([0.2, -1.3, 0]))
        coin_lab = T("just 1 per turn", 24, GOLD).next_to(coin, DOWN, buff=0.12)
        self.play(FadeIn(coin, scale=0.7), FadeIn(coin_lab), run_time=0.7)
        self.at("reducing power")
        self.play(Indicate(VGroup(*items), color=PINK, scale_factor=1.08), run_time=1.2)
        self.at("high value asset")
        sell = T("assets to be sold", 24, PINK).next_to(bank, DOWN, buff=0.12)
        self.play(FadeIn(sell, shift=UP * 0.1), run_time=0.7)

        # ---- the ETC is where the sale happens: exchange rates
        self.at("The electron transport chain")
        self.play(FadeIn(etc, shift=LEFT * 0.3), run_time=0.7)
        a_bank = arrow(bank.get_right(), etc.get_left(), GREY)
        self.play(GrowArrow(a_bank), run_time=0.5)
        # bars: ATP per carrier (computed from the two exchange rates)
        BASE = -3.0
        K = 0.5
        ax_lab = T("ATP per carrier", 26, TEXT).move_to([-3.6, -0.95, 0])
        bar_n = Rectangle(width=1.0, height=0.02, stroke_width=0, fill_color=PINK, fill_opacity=0.9).move_to([-4.4, BASE + 0.01, 0])
        bar_f = Rectangle(width=1.0, height=0.02, stroke_width=0, fill_color=PINK, fill_opacity=0.6).move_to([-2.4, BASE + 0.01, 0])
        base_line = Line([-5.6, BASE, 0], [-1.2, BASE, 0], color=GREY, stroke_width=3)
        lab_n = T("NADH", 24, PINK).move_to([-4.4, BASE - 0.32, 0])
        lab_f = T("FADH₂", 24, PINK).move_to([-2.4, BASE - 0.32, 0])
        self.play(FadeIn(ax_lab), Create(base_line), FadeIn(lab_n), FadeIn(lab_f), run_time=0.6)

        def grow(bar, val, color, op):
            h = K * val
            new = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=color, fill_opacity=op)
            new.move_to([bar.get_center()[0], BASE + h / 2, 0])
            return Transform(bar, new)

        self.at("converting each NADH")
        self.play(grow(bar_n, 2.5, PINK, 0.9), run_time=0.9)
        self.at("roughly 2")
        v_n = M("≈ 2.5", 26, GOLD).move_to([-4.4, BASE + K * 2.5 + 0.32, 0])
        self.play(FadeIn(v_n, shift=UP * 0.1), run_time=0.5)
        self.at("each FADH2")
        self.play(grow(bar_f, 1.5, PINK, 0.6), run_time=0.8)
        self.at("about 1")
        v_f = M("≈ 1.5", 26, GOLD).move_to([-2.4, BASE + K * 1.5 + 0.32, 0])
        self.play(FadeIn(v_f, shift=UP * 0.1), run_time=0.5)
        self.at("by reducing oxygen")
        o2 = chip("O₂", OXY, 26, pad=0.16).move_to([5.5, 1.45, 0])
        a_o2 = arrow(o2.get_left(), etc.get_right(), OXY)
        self.play(FadeIn(o2, shift=LEFT * 0.2), GrowArrow(a_o2), run_time=0.8)

        # ---- the cycle banks, the next pathway liquidates: the tally of ATP made downstream
        self.at("banks the electrons")
        self.play(Indicate(bank, color=PINK, scale_factor=1.06), Indicate(bank_lab, color=PINK), run_time=1.0)
        TX0, TW, TS = 2.7, 1.4, 0.25     # tally: two bars, ATP made in the cycle vs downstream
        tbase = -3.0
        tline = Line([1.7, tbase, 0], [5.9, tbase, 0], color=GREY, stroke_width=3)
        tl_c = T("in the cycle", 24, GOLD).move_to([TX0, tbase - 0.32, 0])
        tl_d = T("downstream", 24, GOLD).move_to([TX0 + 2.2, tbase - 0.32, 0])
        total = ValueTracker(0)
        tbar_d = always_redraw(lambda: Rectangle(width=TW, height=max(0.02, TS * total.get_value()), stroke_width=0,
                                                 fill_color=GOLD, fill_opacity=0.9).move_to(
            [TX0 + 2.2, tbase + max(0.02, TS * total.get_value()) / 2, 0]))
        tval_d = always_redraw(lambda: M(f"≈ {total.get_value():.1f}" if total.get_value() > 0.05 else "0", 26, GOLD).move_to(
            [TX0 + 2.2, tbase + max(0.02, TS * total.get_value()) + 0.32, 0]))
        tbar_c = Rectangle(width=TW, height=TS * 1, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(
            [TX0, tbase + TS * 0.5, 0])
        tval_c = M("1", 26, GOLD).move_to([TX0, tbase + TS * 1 + 0.32, 0])
        t_title = T("ATP per turn", 26, TEXT).move_to([TX0 + 1.1, 0.05, 0])
        self.play(Create(tline), FadeIn(t_title), FadeIn(tl_c), FadeIn(tl_d), FadeIn(tbar_c), FadeIn(tval_c), FadeIn(tbar_d), FadeIn(tval_d),
                  run_time=0.8)
        self.at("liquidates")
        atp_out = T("ATP", 26, GOLD)
        for i, it in enumerate(items):
            gain = 1.5 if it is items[3] else 2.5
            self.play(it.animate.move_to(etc.get_center()).scale(0.4).set_opacity(0.0), run_time=0.35)
            self.play(total.animate.set_value(total.get_value() + gain), run_time=0.4)
        self.at("real ATP windfall")
        self.play(Indicate(tbar_d, color=GOLD, scale_factor=1.05), Indicate(tval_d, color=GOLD), run_time=1.2)
        self.at("comes downstream")
        self.play(Indicate(tbar_c, color=GOLD, scale_factor=1.15), run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
class S06End(EndCard):
    LINE = "The cycle banks the electrons; the next pathway spends them."
