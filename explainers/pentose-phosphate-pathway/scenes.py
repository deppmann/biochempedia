"""The Pentose Phosphate Pathway: glucose's other road  (Biochemistrypedia explainer)

Timed to the SPOKEN words: self.at("phrase") waits until the narrator starts that phrase
(word timestamps in audio/words.json, from the real slide audio).

COLOR MAP (one color per concept, whole video)
  YELLOW  = glucose 6-phosphate, sugars, carbon (the cargo that moves)
  BLUE    = glycolysis, catabolism, the NAD+/NADH pool (the energy road)
  ORANGE  = the pentose phosphate pathway and its enzyme G6PD (the other road)
  PURPLE  = NADPH, reducing power for building and defending
  GREEN   = ATP
  TEAL    = glutathione (GSH / GSSG), the antioxidant shield
  RED     = reactive oxygen species and damage, blocked steps
  GREY    = enzyme names, structure, de-emphasized things
  TEXT    = electrons (white dots), neutral labels
No molecular structures are drawn anywhere: only labelled chips, flows, bars and block counts.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

ORANGE = "#F2A154"
PURPLE = "#B58CD9"
TEAL_G = "#3FB8C0"   # glutathione (same hue as the site's interactive cue, used here only for GSH)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def met(text, size=24, color=YELLOW, pad=0.15, min_w=0.0, fill=0.14, text_color=TEXT, **kw):
    """Chip with a colored outline and neutral text."""
    lab = T(text, size, text_color, **kw)
    w = max(lab.width + 2 * pad, min_w)
    box = RoundedRectangle(corner_radius=0.12, width=w, height=max(lab.height, 0.3) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, lab.move_to(box))


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), color=color, stroke_width=w,
                 buff=0.0, tip_length=tip, max_tip_length_to_length_ratio=0.45)


def darr(a, b, color=GREY, w=4, tip=0.16):
    return DoubleArrow(np.array(a, dtype=float), np.array(b, dtype=float), color=color, stroke_width=w,
                       buff=0.0, tip_length=tip, max_tip_length_to_length_ratio=0.4)


def xmark(center, size=0.2, color=RED, w=6):
    c = np.array(center, dtype=float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def edot(pos, r=0.07):
    return Dot(np.array(pos, dtype=float), radius=r, color=TEXT)


def ros_star(r=0.62):
    st = Star(n=8, outer_radius=r, inner_radius=r * 0.62, stroke_color=RED, stroke_width=3,
              fill_color=RED, fill_opacity=0.28)
    lab = T("ROS", 24, TEXT, weight=BOLD).move_to(st)
    return VGroup(st, lab)


def overlay_for(chip, opacity=0.0):
    """A BG-colored veil that dims a chip without touching its own fills."""
    box = chip[0]
    ov = RoundedRectangle(corner_radius=0.12, width=box.width, height=box.height, stroke_width=0,
                          fill_color=BG, fill_opacity=opacity).move_to(box)
    ov.set_z_index(5)
    return ov


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Pentose Phosphate Pathway"
    TITLE = "Glucose’s Other Road"


# =============================================================================================
class S01Fork(SpokenScene):
    """Glucose 6-phosphate is a fork: glycolysis for energy, the pentose phosphate pathway for NADPH and ribose."""

    def construct(self):
        glu = met("Glucose", 28, YELLOW).move_to([0, 3.0, 0])
        self.at("Glucose enters")
        self.play(FadeIn(glu, shift=DOWN * 0.2), run_time=0.6)

        self.at("hexokinase")
        a0 = arr([0, 2.55, 0], [0, 1.5, 0], YELLOW)
        hk = T("hexokinase", 24, GREY).next_to(a0, RIGHT, buff=0.25)
        self.play(GrowArrow(a0), FadeIn(hk), run_time=0.7)

        self.at("glucose 6 phosphate")
        g6p = met("Glucose\n6-phosphate", 28, YELLOW, pad=0.2).move_to([0, 0.9, 0])
        self.play(FadeIn(g6p, scale=0.85), run_time=0.7)

        self.at("true branch point")
        ring = SurroundingRectangle(g6p, color=YELLOW, buff=0.15, corner_radius=0.2, stroke_width=3)
        self.play(Create(ring), run_time=0.5)
        self.play(FadeOut(ring), run_time=0.4)

        self.at("committed choice")
        ql = arr([-1.45, 0.9, 0], [-3.55, 0.9, 0], GREY, 3)
        qr = arr([1.45, 0.9, 0], [3.55, 0.9, 0], GREY, 3)
        self.play(GrowArrow(ql), GrowArrow(qr), run_time=0.8)

        # ---- left road: glycolysis -----------------------------------------------------
        self.at("Phospho glucose")
        pgi = T("phosphoglucose\nisomerase", 22, GREY, line_spacing=0.8).move_to([-2.5, 0.08, 0])
        self.play(ql.animate.set_color(BLUE).set_stroke(width=6), FadeIn(pgi), run_time=0.7)
        self.at("glycolysis")
        gly = met("Glycolysis", 28, BLUE, min_w=2.4).move_to([-4.9, 0.9, 0])
        self.play(FadeIn(gly, shift=LEFT * 0.2), run_time=0.6)
        self.at("ATP and pyruvate")
        da = arr([-4.9, 0.5, 0], [-4.9, -0.45, 0], BLUE, 4, 0.16)
        atp = met("ATP", 28, GREEN, min_w=1.3).move_to([-4.9, -1.0, 0])
        plus_l = T("+", 26, GREY).move_to([-4.9, -1.6, 0])
        pyr = met("Pyruvate", 26, YELLOW).move_to([-4.9, -2.2, 0])
        self.play(GrowArrow(da), FadeIn(atp, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(plus_l), FadeIn(pyr, shift=UP * 0.1), run_time=0.6)
        self.at("energy currency")
        self.play(Indicate(atp, color=GREEN, scale_factor=1.15), run_time=0.8)

        # ---- right road: pentose phosphate pathway --------------------------------------
        self.at("Alternatively")
        g6pd = VGroup(T("G6PD", 28, ORANGE, weight=BOLD),
                      T("glucose 6-P\ndehydrogenase", 22, GREY, line_spacing=0.8)).arrange(DOWN, buff=0.08)
        g6pd[0].move_to([2.55, 0.52, 0]); g6pd[1].move_to([2.55, -0.12, 0])
        self.play(qr.animate.set_color(ORANGE).set_stroke(width=6), FadeIn(g6pd), run_time=0.8)
        self.at("pentose phosphate pathway")
        ppp = met("Pentose\nphosphate\npathway", 24, ORANGE, min_w=2.2).move_to([4.9, 0.9, 0])
        self.play(FadeIn(ppp, shift=RIGHT * 0.2), run_time=0.6)
        self.at("NADPH for reductive")
        db = arr([4.9, 0.1, 0], [4.9, -0.45, 0], ORANGE, 4, 0.16)
        nadph = met("NADPH", 28, PURPLE, min_w=1.7).move_to([4.9, -1.0, 0])
        self.play(GrowArrow(db), FadeIn(nadph, shift=UP * 0.1), run_time=0.6)
        bio = T("biosynthesis", 22, GREY).next_to(nadph, LEFT, buff=0.25)
        self.at("biosynthesis")
        self.play(FadeIn(bio, shift=RIGHT * 0.1), run_time=0.5)
        self.at("ribose 5 phosphate")
        plus_r = T("+", 26, GREY).move_to([4.9, -1.6, 0])
        rib = met("Ribose\n5-phosphate", 24, YELLOW, min_w=2.1).move_to([4.9, -2.35, 0])
        self.play(FadeIn(plus_r), FadeIn(rib, shift=UP * 0.1), run_time=0.7)
        self.at("nucleotide synthesis")
        nuc = T("nucleotides", 22, GREY).next_to(rib, LEFT, buff=0.25)
        self.play(FadeIn(nuc, shift=RIGHT * 0.1), run_time=0.5)

        # ---- the decision ----------------------------------------------------------------
        self.at("The deciding factor")
        self.play(FadeOut(glu), FadeOut(a0), FadeOut(hk), run_time=0.6)
        self.at("What does the cell need right now")
        q = T("What does the cell need right now?", 34, TEXT).move_to([0, 2.95, 0])
        self.play(Write(q), run_time=1.2)
        self.at("Energy or")
        self.play(Indicate(gly, color=BLUE, scale_factor=1.12), Indicate(atp, color=GREEN, scale_factor=1.12),
                  run_time=0.8)
        self.at("building blocks")
        self.play(Indicate(ppp, color=ORANGE, scale_factor=1.1), Indicate(nadph, color=PURPLE, scale_factor=1.1),
                  Indicate(rib, color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.at("This fork captures")
        self.play(Indicate(g6p, color=YELLOW, scale_factor=1.12), run_time=0.8)
        self.finish()


# =============================================================================================
class S02Pools(SpokenScene):
    """Two nicotinamide pools held in opposite redox states: NAD+ mostly oxidized, NADPH mostly reduced."""

    def construct(self):
        LX, RX = -3.3, 3.3
        # header names
        nad = met("NAD", 30, BLUE, min_w=1.5).move_to([LX, 3.15, 0])
        nadp = met("NADP", 30, PURPLE, min_w=1.5).move_to([RX, 3.15, 0])
        self.at("NAD and")
        self.play(FadeIn(nad, shift=DOWN * 0.15), run_time=0.5)
        self.at("NADP look")
        self.play(FadeIn(nadp, shift=DOWN * 0.15), run_time=0.5)

        # one extra phosphate
        self.at("differing by a single phosphate")
        ptag = VGroup(Circle(radius=0.22, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.3),
                      T("P", 24, TEXT, weight=BOLD)).move_to(nadp.get_right() + RIGHT * 0.4 + UP * 0.05)
        ptag[1].move_to(ptag[0])
        plab = T("one extra phosphate", 22, GOLD).move_to([RX, 2.62, 0])
        self.play(FadeIn(ptag, shift=LEFT * 0.4), FadeIn(plab), run_time=0.8)
        self.at("dramatically different states")
        self.play(Indicate(nad, color=BLUE), Indicate(nadp, color=PURPLE), run_time=0.9)

        # ---- the NAD pool -----------------------------------------------------------------
        self.at("The NAD pool")
        by, bh = 1.35, 0.7
        big_l = Rectangle(width=4.85, height=bh, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                          fill_opacity=0.18).move_to([-5.8 + 4.85 / 2, by, 0])
        sliver_l = Rectangle(width=0.15, height=bh, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                             fill_opacity=0.9).move_to([-0.95 + 0.075, by, 0])
        big_l_lab = T("NAD⁺", 30, TEXT, weight=BOLD).move_to(big_l)
        self.play(FadeOut(plab), FadeOut(ptag), run_time=0.3)
        self.play(FadeIn(big_l), FadeIn(big_l_lab), FadeIn(sliver_l), run_time=0.8)
        nadh_lab = T("NADH", 22, BLUE).move_to([-0.9, 2.0, 0])
        nadh_tick = Line([-0.88, 1.72, 0], [-0.88, 1.85, 0], color=BLUE, stroke_width=3)
        self.at("sits oxidized")
        self.play(FadeIn(nadh_lab), FadeIn(nadh_tick), run_time=0.5)
        self.at("roughly a thousand")
        ratio = M("≈ 1000 : 1", 28, BLUE).move_to([LX, 0.62, 0])
        sub_l = T("mostly the oxidized form", 22, GREY).move_to([LX, 0.18, 0])
        self.play(FadeIn(ratio, shift=UP * 0.1), FadeIn(sub_l), run_time=0.7)

        self.at("catabolism needs")
        cat = T("Catabolism", 32, BLUE, weight=BOLD)
        cat.move_to([-4.7 + cat.width / 2, -0.55, 0])
        self.play(FadeIn(cat, shift=RIGHT * 0.15), run_time=0.5)
        self.at("electron acceptor")
        acc = T("needs an electron acceptor", 22, TEXT)
        acc.move_to([-4.7 + acc.width / 2, -1.2, 0])
        self.play(FadeIn(acc, shift=RIGHT * 0.1), run_time=0.6)
        self.at("grab electrons")
        fuel = met("Fuel", 26, YELLOW, min_w=1.1).move_to([-5.5, -2.38, 0])
        self.play(FadeIn(fuel, shift=UP * 0.1), run_time=0.4)
        e_lab = T("e⁻", 28, TEXT).move_to([-5.12, -0.6, 0])
        stream_l = arr([-5.5, -2.0, 0], [-5.5, 0.98, 0], TEXT, 3, 0.16)
        dots = VGroup(*[edot([-5.5, -2.0, 0]) for _ in range(5)])
        self.add(dots)
        self.play(GrowArrow(stream_l), FadeIn(e_lab),
                  LaggedStart(*[d.animate.move_to([-5.5, 1.0, 0]) for d in dots], lag_ratio=0.2),
                  run_time=1.4)
        self.play(FadeOut(dots), Indicate(big_l_lab, color=BLUE), run_time=0.4)

        # ---- the NADP pool ----------------------------------------------------------------
        self.at("The NADP pool")
        sliver_r = Rectangle(width=0.15, height=bh, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                             fill_opacity=0.18).move_to([0.8 + 0.075, by, 0])
        big_r = Rectangle(width=4.85, height=bh, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                          fill_opacity=0.9).move_to([0.95 + 4.85 / 2, by, 0])
        big_r_lab = T("NADPH", 30, TEXT, weight=BOLD).move_to(big_r)
        nadpp_lab = T("NADP⁺", 22, PURPLE).move_to([0.9, 2.0, 0])
        nadpp_tick = Line([0.88, 1.72, 0], [0.88, 1.85, 0], color=PURPLE, stroke_width=3)
        self.play(FadeIn(sliver_r), FadeIn(big_r), FadeIn(big_r_lab), FadeIn(nadpp_lab), FadeIn(nadpp_tick),
                  run_time=0.9)
        self.at("mirror image")
        mirror = DashedLine([0, 3.45, 0], [0, -3.0, 0], color=GREY, stroke_width=3, dash_length=0.18)
        self.play(Create(mirror), run_time=0.7)
        self.at("held about")
        sub_r = T("NADPH outweighs NADP⁺", 22, GREY).move_to([RX, 0.18, 0])
        reduced = T("mostly reduced", 28, PURPLE, weight=BOLD).move_to([RX, 0.62, 0])
        self.play(FadeIn(reduced, shift=UP * 0.1), FadeIn(sub_r), run_time=0.7)

        self.at("anabolism and")
        ana = T("Anabolism", 32, PURPLE, weight=BOLD)
        ana.move_to([4.6 - ana.width / 2, -0.55, 0])
        self.play(FadeIn(ana, shift=LEFT * 0.15), run_time=0.5)
        self.at("antioxidant defense")
        dfn = T("+ antioxidant defense", 22, TEXT)
        dfn.move_to([4.6 - dfn.width / 2, -1.05, 0])
        self.play(FadeIn(dfn, shift=LEFT * 0.1), run_time=0.6)
        self.at("electron donor")
        don = T("needs an electron donor", 22, TEXT)
        don.move_to([4.6 - don.width / 2, -1.55, 0])
        target = met("Biosynthesis\n& defense", 22, PURPLE, min_w=1.9).move_to([5.0, -2.33, 0])
        self.play(FadeIn(don, shift=LEFT * 0.1), FadeIn(target, shift=DOWN * 0.1), run_time=0.7)
        self.at("on tap")
        stream_r = arr([5.5, 0.98, 0], [5.5, -1.85, 0], TEXT, 3, 0.16)
        e_lab2 = T("e⁻", 28, TEXT).move_to([5.12, -0.6, 0])
        dots2 = VGroup(*[edot([5.5, 1.0, 0]) for _ in range(5)])
        self.add(dots2)
        self.play(GrowArrow(stream_r), FadeIn(e_lab2),
                  LaggedStart(*[d.animate.move_to([5.5, -1.82, 0]) for d in dots2], lag_ratio=0.2), run_time=1.1)
        self.play(FadeOut(dots2), Indicate(target, color=PURPLE), run_time=0.4)

        self.at("Same backbone")
        self.play(Indicate(nad, color=BLUE), Indicate(nadp, color=PURPLE), run_time=0.9)
        self.at("opposite redox")
        self.play(Indicate(big_l, color=BLUE, scale_factor=1.03), Indicate(big_r, color=PURPLE, scale_factor=1.03),
                  run_time=1.0)

        # ---- separate pools ------------------------------------------------------------------
        self.at("separate cytosolic pools")
        rl = RoundedRectangle(corner_radius=0.2, width=5.8, height=5.3, stroke_color=GREY, stroke_width=3,
                              ).move_to([-3.2, -0.22, 0])
        rr = RoundedRectangle(corner_radius=0.2, width=5.8, height=5.3, stroke_color=GREY, stroke_width=3,
                              ).move_to([3.2, -0.22, 0])
        rl.set_stroke(opacity=0.8); rr.set_stroke(opacity=0.8)
        cap = T("separate pools in the cytosol", 26, GREY).move_to([0, -3.3, 0])
        self.play(FadeOut(mirror), Create(rl), Create(rr), FadeIn(cap), run_time=1.2)
        self.at("breakdown and biosynthesis")
        self.play(Indicate(cat, color=BLUE), Indicate(ana, color=PURPLE), run_time=0.9)
        self.at("simultaneously")
        d1 = VGroup(*[edot([-5.5, -2.0, 0]) for _ in range(4)])
        d2 = VGroup(*[edot([5.5, 1.0, 0]) for _ in range(4)])
        self.add(d1, d2)
        self.play(LaggedStart(*[d.animate.move_to([-5.5, 1.0, 0]) for d in d1], lag_ratio=0.2),
                  LaggedStart(*[d.animate.move_to([5.5, -1.82, 0]) for d in d2], lag_ratio=0.2), run_time=1.6)
        self.play(FadeOut(d1), FadeOut(d2), run_time=0.2)
        self.at("interfering")
        bar = DashedLine([-0.2, -0.9, 0], [0.2, -0.9, 0], color=RED, stroke_width=4, dash_length=0.08)
        xm = xmark([0, -0.9, 0], 0.18)
        cap2 = T("no interference", 26, RED).move_to([0, -3.3, 0])
        self.play(FadeIn(bar), FadeIn(xm), ReplacementTransform(cap, cap2), run_time=0.8)
        self.finish()


# =============================================================================================
class S03Shield(SpokenScene):
    """ROS damage; glutathione takes the hit; NADPH recharges it; the pentose phosphate pathway supplies NADPH."""

    def construct(self):
        # ---- reactive oxygen species --------------------------------------------------------
        ros = ros_star(0.7).move_to([-4.2, 0.8, 0])
        self.at("Reactive oxygen species")
        self.play(FadeIn(ros, scale=0.6), run_time=0.7)
        self.at("super energetic")
        orb = VGroup(*[edot(ros[0].get_center() + 1.05 * np.array([np.cos(a), np.sin(a), 0]), 0.075)
                       for a in np.linspace(0, TAU, 7)[:-1]])
        elab = T("energetic electrons", 22, TEXT).move_to([-4.2, -0.55, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in orb], lag_ratio=0.1), FadeIn(elab), run_time=0.9)
        self.play(Rotate(orb, angle=TAU / 4, about_point=ros[0].get_center()), run_time=0.9)

        self.at("attack and damage")
        tg = [met(n, 28, GREY, min_w=1.9) for n in ["Proteins", "Lipids", "DNA"]]
        for m, y in zip(tg, [2.1, 0.8, -0.5]):
            m.move_to([3.9, y, 0])
        self.play(*[FadeIn(m, shift=LEFT * 0.2) for m in tg], run_time=0.5)
        hits = [arr(ros[0].get_center() + [0.8, 0, 0], [m.get_left()[0] - 0.12, m.get_center()[1], 0], RED, 4, 0.16)
                for m in tg]
        self.play(*[GrowArrow(h) for h in hits], run_time=0.5)
        xs = [xmark(m.get_right() + RIGHT * 0.28, 0.14, RED, 5) for m in tg]
        self.at("proteins")
        self.play(*[m[0].animate.set_stroke(RED) for m in tg], *[Create(x) for x in xs], run_time=0.8)

        # ---- glutathione --------------------------------------------------------------------
        self.at("The cell's frontline defense")
        stageA = VGroup(*tg, *hits, *xs, orb, elab)
        self.play(FadeOut(stageA), ros.animate.move_to([0, 2.45, 0]), run_time=1.0)
        self.at("glutathione")
        gsh = met("2 GSH", 30, TEAL_G, min_w=1.9).move_to([-4.4, 0.32, 0])
        gssg = met("GSSG", 30, TEAL_G, min_w=1.9).move_to([4.4, 0.32, 0])
        gsh_lab = T("reduced: protective", 22, GREY).move_to([-4.4, -0.45, 0])
        a_top = arr([-3.25, 0.5, 0], [3.25, 0.5, 0], TEAL_G, 5)
        a_bot = arr([3.25, 0.12, 0], [-3.25, 0.12, 0], TEAL_G, 5)
        self.play(FadeIn(gsh, scale=0.85), FadeIn(gsh_lab), run_time=0.7)
        self.at("neutralizes these threats")
        hitarr = arr([0, 1.85, 0], [0, 0.68, 0], RED, 4, 0.16)
        self.play(GrowArrow(hitarr), run_time=0.5)
        self.at("taking the oxidative hit")
        self.play(GrowArrow(a_top), FadeIn(gssg, shift=LEFT * 0.2), run_time=0.9)
        self.at("so other molecules")
        neutral = met("neutralized", 24, GREY, min_w=1.5).move_to([2.6, 2.45, 0])
        self.play(FadeOut(hitarr), ReplacementTransform(ros, neutral), run_time=0.8)

        self.at("But once glutathione absorbs")
        self.play(Indicate(gssg, color=TEAL_G, scale_factor=1.12), run_time=0.8)
        self.at("oxidized and useless")
        olab = T("oxidized: used up", 22, GREY).move_to([4.4, -0.45, 0])
        self.play(gssg[0].animate.set_stroke(GREY), FadeIn(olab), FadeOut(gsh_lab), run_time=0.8)
        self.at("linked into")
        dim = T("two GSH linked together", 22, GREY).move_to([4.4, -0.85, 0])
        self.play(FadeIn(dim, shift=UP * 0.1), run_time=0.7)

        # ---- NADPH recharges it ---------------------------------------------------------------
        self.at("To get it back")
        self.play(GrowArrow(a_bot), run_time=0.8)
        self.at("reduced protective")
        self.play(gsh[0].animate.set_stroke(TEAL_G), FadeOut(olab), FadeOut(dim), Indicate(gsh, color=TEAL_G),
                  run_time=0.9)
        self.at("the cell spends NADPH")
        nadph = met("NADPH", 28, PURPLE, min_w=1.7).move_to([-1.4, -1.6, 0])
        nadpp = met("NADP⁺", 28, PURPLE, min_w=1.7).move_to([1.4, -1.6, 0])
        up = arr([-1.4, -1.2, 0], [-1.4, 0.0, 0], PURPLE, 4, 0.16)
        dn = arr([1.4, 0.0, 0], [1.4, -1.2, 0], GREY, 4, 0.16)
        self.play(FadeIn(nadph, shift=UP * 0.1), GrowArrow(up), run_time=0.7)
        dots = VGroup(*[edot([-1.4, -1.2, 0]) for _ in range(3)])
        self.add(dots)
        self.play(LaggedStart(*[MoveAlongPath(d, VMobject().set_points_as_corners(
            [[-1.4, -1.2, 0], [-1.4, 0.12, 0], [-3.1, 0.12, 0]])) for d in dots], lag_ratio=0.25), run_time=1.5)
        self.play(FadeOut(dots), GrowArrow(dn), FadeIn(nadpp, shift=DOWN * 0.1), run_time=0.6)

        self.at("where does that NADPH come from")
        qm = T("?", 56, PURPLE, weight=BOLD).move_to([-2.65, -1.6, 0])
        self.play(Indicate(nadph, color=PURPLE, scale_factor=1.15), FadeIn(qm, scale=0.5), run_time=0.9)
        self.at("The pentose phosphate pathway")
        ppp = met("Pentose phosphate pathway", 22, ORANGE, min_w=3.4).move_to([0, -3.05, 0])
        l1 = arr([1.3, -2.0, 0], [0.9, -2.67, 0], ORANGE, 4, 0.14)
        l2 = arr([-0.9, -2.67, 0], [-1.3, -2.0, 0], ORANGE, 4, 0.14)
        self.play(FadeOut(qm), FadeIn(ppp, shift=UP * 0.1), GrowArrow(l1), GrowArrow(l2), run_time=0.9)
        self.at("G6PD")
        g6pd = met("G6PD", 28, ORANGE, min_w=1.5, fill=0.3).move_to([4.5, -3.05, 0])
        ga = arr([3.7, -3.05, 0], [2.3, -3.05, 0], ORANGE, 4, 0.16)
        self.play(FadeIn(g6pd, shift=LEFT * 0.2), GrowArrow(ga), run_time=0.8)
        self.at("antioxidant defense")
        cyc = VGroup(gsh, gssg, a_top, a_bot, nadph, nadpp, up, dn)
        self.play(Indicate(cyc, color=TEAL_G, scale_factor=1.03), run_time=1.0)

        # ---- lose G6PD ----------------------------------------------------------------------------
        self.at("Lose that enzyme")
        gx = xmark([5.62, -3.05, 0], 0.2, RED, 7)
        self.play(Create(gx),
                  g6pd[0].animate.set_stroke(opacity=0.45).set_fill(opacity=0.06), g6pd[1].animate.set_opacity(0.45),
                  ppp[0].animate.set_stroke(opacity=0.3).set_fill(opacity=0.04), ppp[1].animate.set_opacity(0.3),
                  FadeOut(l1), FadeOut(l2), FadeOut(ga),
                  nadph[0].animate.set_stroke(opacity=0.3).set_fill(opacity=0.04), nadph[1].animate.set_opacity(0.3),
                  run_time=0.9)
        self.at("regenerate glutathione")
        bx = xmark([0, 0.12, 0], 0.22, RED, 8)
        self.play(a_bot.animate.set_color(RED), Create(bx), run_time=0.8)
        self.at("oxidative damage")
        ros2 = ros_star(0.6).move_to([2.2, 2.45, 0])
        dmg = met("Proteins, lipids, DNA", 24, GREY, min_w=3.4).move_to([-2.6, 2.45, 0])
        hit2 = arr([1.5, 2.45, 0], [-0.85, 2.45, 0], RED, 4, 0.16)
        self.play(FadeOut(neutral), FadeIn(ros2, scale=0.6), run_time=0.5)
        self.play(GrowArrow(hit2), FadeIn(dmg), run_time=0.6)
        self.at("runs unchecked")
        self.play(dmg[0].animate.set_stroke(RED), Create(xmark([-4.55, 2.45, 0], 0.16, RED, 6)), run_time=0.8)
        self.finish()


# =============================================================================================
UNIT = 0.34


def cbar(n, unit=UNIT):
    """A bar of n unit blocks: a sugar drawn only as a carbon COUNT (no atoms, no bonds)."""
    w = n * unit
    r = Rectangle(width=w, height=0.5, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.2)
    ticks = VGroup(*[Line([-w / 2 + k * unit, -0.25, 0], [-w / 2 + k * unit, 0.25, 0], color=YELLOW,
                          stroke_width=1.5, stroke_opacity=0.45) for k in range(1, n)])
    lab = M(f"C{n}", 22, TEXT, weight=BOLD)
    return VGroup(r, ticks, lab)


class S04Carbons(SpokenScene):
    """Carbon bookkeeping: transketolase and transaldolase turn 3 C5 into 2 C6 + C3."""

    def construct(self):
        title = T("Non-oxidative phase", 32, ORANGE, weight=BOLD).move_to([0, 3.3, 0])
        self.at("The non oxidative phase")
        self.play(Write(title), run_time=1.2)
        self.at("carbon bookkeeping")
        sub = T("carbon bookkeeping", 28, TEXT).move_to([0, 2.5, 0])
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)
        self.at("two enzymes", nth=0)
        tkc = met("transketolase", 28, GREY, min_w=2.8).move_to([-2.2, 0.9, 0])
        tac = met("transaldolase", 28, GREY, min_w=2.8).move_to([2.2, 0.9, 0])
        self.at("transketolase", nth=0)
        self.play(FadeIn(tkc, shift=DOWN * 0.1), run_time=0.5)
        self.at("transaldolase", nth=0)
        self.play(FadeIn(tac, shift=DOWN * 0.1), run_time=0.5)

        self.at("Track the carbons")
        self.play(FadeOut(tkc), FadeOut(tac), FadeOut(sub), run_time=0.4)
        demo = cbar(5).move_to([0, 1.2, 0])
        legend = T("each block is one carbon", 26, TEXT).move_to([0, 0.35, 0])
        self.play(FadeIn(demo), FadeIn(legend), run_time=0.5)
        blocks = [Rectangle(width=UNIT, height=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
                  .move_to(demo[0].get_left() + RIGHT * (UNIT * (k + 0.5))) for k in range(5)]
        self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.15, run_time=0.7))
        self.play(FadeOut(VGroup(*blocks)), FadeOut(demo), FadeOut(legend), run_time=0.4)

        def make_row(y, left, right, enzyme):
            L = VGroup(cbar(left[0]), T("+", 30, GREY), cbar(left[1])).arrange(RIGHT, buff=0.22)
            R = VGroup(cbar(right[0]), T("+", 30, GREY), cbar(right[1])).arrange(RIGHT, buff=0.22)
            L.move_to([-3.9, y, 0]); R.move_to([2.9, y, 0])
            ar = darr([-1.4, y, 0], [0.3, y, 0], GREY, 4)
            lb = T(enzyme, 24, GREY).move_to([-0.55, y + 0.4, 0])
            return L, R, ar, lb

        # row 1: transketolase  C5 + C5 -> C3 + C7
        L1, R1, ar1, lb1 = make_row(2.1, (5, 5), (3, 7), "transketolase")
        self.at("transketolase", nth=1)
        self.play(FadeIn(L1, shift=RIGHT * 0.2), GrowArrow(ar1), FadeIn(lb1), run_time=0.9)
        self.at("three carbon and a seven")
        self.play(TransformFromCopy(L1[0], R1[0]), FadeIn(R1[1]), TransformFromCopy(L1[2], R1[2]), run_time=1.1)

        # row 2: transaldolase  C3 + C7 -> C6 + C4
        L2, R2, ar2, lb2 = make_row(0.75, (3, 7), (6, 4), "transaldolase")
        self.at("transaldolase", nth=1)
        self.play(TransformFromCopy(R1[0], L2[0]), FadeIn(L2[1]), TransformFromCopy(R1[2], L2[2]),
                  GrowArrow(ar2), FadeIn(lb2), run_time=1.2)
        self.at("a six and a four")
        self.play(TransformFromCopy(L2[0], R2[0]), FadeIn(R2[1]), TransformFromCopy(L2[2], R2[2]), run_time=1.1)

        # row 3: transketolase  C4 + C5 -> C6 + C3
        L3, R3, ar3, lb3 = make_row(-0.6, (4, 5), (6, 3), "transketolase")
        self.at("transketolase", nth=2)
        self.play(GrowArrow(ar3), FadeIn(lb3), run_time=0.6)
        self.at("a four and a five")
        self.play(TransformFromCopy(R2[2], L3[0]), FadeIn(L3[1]), FadeIn(L3[2], shift=DOWN * 0.3), run_time=1.0)
        self.at("into a six and a three")
        self.play(TransformFromCopy(L3[0], R3[0]), FadeIn(R3[1]), TransformFromCopy(L3[2], R3[2]), run_time=1.1)

        # ---- the sum ---------------------------------------------------------------------------------
        self.at("Some at all")
        inter = [R1, L2, R2[2], L3[0]]
        rule = Line([-6.0, -1.35, 0], [6.0, -1.35, 0], color=GREY, stroke_width=3)
        self.play(Create(rule), *[g.animate.set_opacity(0.22) for g in inter], run_time=0.9)
        self.at("net result is clean")
        cancel = T("intermediates cancel out", 22, GREY).move_to([2.9, 1.42, 0])
        self.play(FadeIn(cancel), run_time=0.4)

        U2 = 0.27
        sl = VGroup(cbar(5, U2), cbar(5, U2), cbar(5, U2)).arrange(RIGHT, buff=0.2).move_to([-3.4, -2.05, 0])
        sar = darr([-0.85, -2.05, 0], [0.15, -2.05, 0], GREY, 4)
        sr = VGroup(cbar(6, U2), cbar(6, U2), cbar(3, U2)).arrange(RIGHT, buff=0.2).move_to([3.4, -2.05, 0])
        self.at("Three five carbon sugars")
        self.play(TransformFromCopy(L1[0], sl[0]), TransformFromCopy(L1[2], sl[1]), TransformFromCopy(L3[2], sl[2]),
                  GrowArrow(sar), FadeOut(cancel), run_time=1.3)
        self.at("two six carbon sugars")
        self.play(TransformFromCopy(R2[0], sr[0]), TransformFromCopy(R3[0], sr[1]), run_time=1.0)
        self.at("one three carbon sugar")
        self.play(TransformFromCopy(R3[2], sr[2]), run_time=0.9)
        cl = M("3 × 5 = 15 C", 24, GREY).move_to([-3.4, -2.85, 0])
        cr = M("2 × 6 + 3 = 15 C", 24, GREY).move_to([3.4, -2.85, 0])
        self.play(FadeIn(cl), FadeIn(cr), run_time=0.6)
        self.at("That is how excess pentoses")
        self.play(Indicate(sl, color=YELLOW, scale_factor=1.06), run_time=0.9)
        self.at("recycled back into glycolytic")
        glyc = met("glycolytic intermediates", 26, BLUE, min_w=4.4).move_to([3.4, -2.9, 0])
        self.play(FadeOut(cl), FadeOut(cr), sr.animate.set_color(BLUE), FadeIn(glyc, shift=UP * 0.1), run_time=0.9)
        self.at("when the cell needs energy")
        self.play(Indicate(glyc, color=BLUE, scale_factor=1.06), run_time=0.9)
        self.finish()


# =============================================================================================
class S05Modes(SpokenScene):
    """One pathway skeleton, four routes: ribose-only, balanced, NADPH-heavy, NADPH + ATP."""

    def construct(self):
        Y = 0.3
        g6p = met("Glucose\n6-P", 24, YELLOW, min_w=1.5).move_to([-5.3, Y, 0])
        oxid = met("Oxidative\nphase", 24, ORANGE, min_w=1.8).move_to([-2.4, Y, 0])
        nonox = met("Non-oxidative\nphase", 24, ORANGE, min_w=2.4).move_to([1.2, Y, 0])
        glyc = met("Glycolytic\nintermediates", 24, BLUE, min_w=2.4).move_to([4.7, Y, 0])
        nadph = met("NADPH", 26, PURPLE, min_w=1.6).move_to([-2.4, 1.85, 0])
        rib = met("Ribose\n5-phosphate", 24, YELLOW, min_w=2.0).move_to([1.2, 1.85, 0])
        pyr = met("Pyruvate", 24, YELLOW, min_w=1.7).move_to([3.95, 1.85, 0])
        atp = met("ATP", 26, GREEN, min_w=1.1).move_to([5.75, 1.85, 0])
        chips = dict(g6p=g6p, oxid=oxid, nonox=nonox, glyc=glyc, nadph=nadph, rib=rib, pyr=pyr, atp=atp)
        ovs = {k: overlay_for(v, 0.0) for k, v in chips.items()}

        a1 = arr([-4.5, Y, 0], [-3.4, Y, 0], GREY, 4, 0.16)
        a2 = arr([-1.4, Y, 0], [-0.1, Y, 0], GREY, 4, 0.16)
        a3 = darr([2.5, Y, 0], [3.45, Y, 0], GREY, 4, 0.14)
        an = arr([-2.4, 0.88, 0], [-2.4, 1.42, 0], GREY, 4, 0.14)
        ar_ = arr([1.2, 0.88, 0], [1.2, 1.42, 0], GREY, 4, 0.14)
        ap = arr([4.4, 0.88, 0], [4.0, 1.4, 0], GREY, 4, 0.14)
        aa = arr([5.0, 0.88, 0], [5.6, 1.4, 0], GREY, 4, 0.14)
        rec = VGroup(Line([4.7, -0.15, 0], [4.7, -1.75, 0], color=GREY, stroke_width=4),
                     Line([4.7, -1.75, 0], [-5.3, -1.75, 0], color=GREY, stroke_width=4),
                     arr([-5.3, -1.75, 0], [-5.3, -0.3, 0], GREY, 4, 0.16))
        recl = T("recycle to glucose 6-phosphate", 22, GREY).move_to([-0.3, -1.4, 0])
        arrows = dict(a1=a1, a2=a2, a3=a3, an=an, ar=ar_, ap=ap, aa=aa, rec=rec)

        def route(chip_keys, arrow_keys, colors=None):
            anims = []
            for k, ov in ovs.items():
                anims.append(ov.animate.set_fill(opacity=0.0 if k in chip_keys else 0.78))
            for k, a in arrows.items():
                lit = k in arrow_keys
                col = YELLOW if lit else GREY
                anims.append(a.animate.set_color(col).set_opacity(1.0 if lit else (0.0 if k == "rec" else 0.25)))
            return anims

        # ---- skeleton builds up while the intro is spoken ----------------------------------------------
        self.at("The pentose phosphate pathway")
        self.play(FadeIn(g6p, shift=RIGHT * 0.2), GrowArrow(a1), FadeIn(oxid, shift=RIGHT * 0.2), GrowArrow(a2),
                  FadeIn(nonox, shift=RIGHT * 0.2), run_time=1.4)
        self.add(*ovs.values())
        self.play(GrowArrow(a3), FadeIn(glyc, shift=RIGHT * 0.2), run_time=0.7)
        self.at("one fixed route")
        for ch, a in [(nadph, an), (rib, ar_), (pyr, ap), (atp, aa)]:
            pass
        self.play(FadeIn(nadph, shift=UP * 0.1), GrowArrow(an), FadeIn(rib, shift=UP * 0.1), GrowArrow(ar_),
                  FadeIn(pyr, shift=UP * 0.1), GrowArrow(ap), FadeIn(atp, shift=UP * 0.1), GrowArrow(aa),
                  run_time=1.0)
        self.add(rec)
        rec.set_opacity(0.0)

        self.at("four operating modes")
        names = ["1  ribose", "2  balanced", "3  NADPH", "4  NADPH + ATP"]
        chipsm = VGroup(*[met(n, 24, GREY, pad=0.15) for n in names]).arrange(RIGHT, buff=0.25).move_to([0, -3.2, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chipsm], lag_ratio=0.25), run_time=1.4)
        self.at("selects among them")
        self.play(Indicate(chipsm, color=TEXT, scale_factor=1.04), run_time=1.0)

        def header(txt):
            return T(txt, 30, TEXT, weight=BOLD).move_to([0, 3.15, 0])

        def hl(i):
            return chipsm[i][0].animate.set_stroke(YELLOW, width=4)

        def unhl(i):
            return chipsm[i][0].animate.set_stroke(GREY, width=2.5)

        # ---- mode 1 -------------------------------------------------------------------------------------
        self.at("When it needs ribose")
        h = header("Mode 1:  ribose needed, little NADPH")
        self.play(FadeIn(h, shift=DOWN * 0.1), hl(0), *route(["rib"], []), run_time=0.7)
        self.at("runs only")
        self.play(*route(["glyc", "nonox", "rib"], ["a3", "ar"]), run_time=0.9)
        self.play(Indicate(chips["nonox"], color=ORANGE), run_time=0.8)

        # ---- mode 2 -------------------------------------------------------------------------------------
        self.at("needs both NADPH")
        h2 = header("Mode 2:  NADPH and ribose in balance")
        self.play(ReplacementTransform(h, h2), unhl(0), hl(1), *route(["nadph", "rib"], []), run_time=0.7)
        self.at("oxidative phase straight through")
        self.play(*route(["g6p", "oxid", "nadph", "nonox", "rib"], ["a1", "a2", "an", "ar"]), run_time=1.2)

        # ---- mode 3 -------------------------------------------------------------------------------------
        self.at("lots of NADPH")
        h3 = header("Mode 3:  lots of NADPH, little ribose")
        self.play(ReplacementTransform(h2, h3), unhl(1), hl(2), *route(["nadph"], []), run_time=0.7)
        self.at("routes ribose back")
        rec.set_opacity(1.0)
        self.add(recl)
        self.play(*route(["g6p", "oxid", "nadph", "nonox", "glyc"], ["a1", "a2", "an", "a3", "rec"]),
                  FadeIn(recl), run_time=1.3)
        self.at("recycles them")
        self.play(Indicate(rec, color=YELLOW), run_time=0.9)

        # ---- mode 4 -------------------------------------------------------------------------------------
        self.at("needs NADPH plus ATP")
        h4 = header("Mode 4:  NADPH and ATP")
        self.play(ReplacementTransform(h3, h4), unhl(2), hl(3), FadeOut(recl), *route(["nadph", "atp"], []), run_time=0.7)
        rec.set_opacity(0.0)
        self.at("pushes carbon")
        self.play(*route(["g6p", "oxid", "nadph", "nonox", "glyc", "pyr", "atp"],
                         ["a1", "a2", "an", "a3", "ap", "aa"]), run_time=1.3)

        # ---- one pathway ------------------------------------------------------------------------------------
        self.at("One pathway")
        h5 = header("One pathway, four behaviors")
        self.play(ReplacementTransform(h4, h5), unhl(3),
                  *[o.animate.set_fill(opacity=0.0) for o in ovs.values()],
                  *[a.animate.set_color(GREY).set_opacity(1.0) for k, a in arrows.items() if k != "rec"], run_time=1.0)
        self.at("a different combination")
        self.play(Indicate(chipsm, color=TEXT, scale_factor=1.04), run_time=1.0)
        self.finish()


# =============================================================================================
class S06End(EndCard):
    LINE = "Glycolysis makes ATP. This road makes NADPH and ribose."
