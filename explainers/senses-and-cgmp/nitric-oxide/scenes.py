"""Senses and cGMP, section film: How an artery learned to relax  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the endothelium (the lining) and its receptor
  ORANGE = smooth muscle (the vessel wall)
  YELLOW = acetylcholine, the stimulus
  GOLD   = calcium
  PINK   = nitric oxide, the gas
  PURPLE = enzymes and kinases (nitric oxide synthase, guanylyl cyclase, protein kinase G)
  TEAL   = cGMP
  GREEN  = switched on / relaxed
  RED    = the off-switch (PDE5) and a failure to relax
  GREY   = substrates (arginine, GTP), baths, outlines, labels

No molecular structures: enzymes are labelled chips, NO is a pink dot, the vessel is idealised rings and bars.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08BB4"


def bchip(text, color=BLUE, size=24, pad=0.14, two=False, **kw):
    """chip with an opaque backing. [back, box, label]"""
    if two:
        label = T(text, size, color, line_spacing=0.8)
        box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
                               stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
        c = VGroup(box, label.move_to(box))
    else:
        c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color):
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dot(color, r=0.17, pos=ORIGIN):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.95).move_to(pos)


def cellbox(x0, x1, y0, y1, color):
    return RoundedRectangle(corner_radius=0.2, width=x1 - x0, height=y1 - y0, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.08).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def ring_set(open_=False):
    """two rings of vessel wall in an organ bath. returns dict of parts."""
    cy = 0.3
    bath = RoundedRectangle(corner_radius=0.25, width=12.2, height=4.4, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.07).move_to([0, cy, 0])
    bath_lbl = T("organ bath", 22, GREY).move_to([0, cy + 1.95, 0]).set_opacity(0)
    rings = {}
    for key, x in (("L", -3.0), ("R", 3.0)):
        ri, ro = (1.5, 2.05) if open_ and key == "L" else (1.2, 1.85)
        rings[key] = Annulus(inner_radius=ri, outer_radius=ro, stroke_width=2, color=ORANGE,
                             fill_opacity=0.4).move_to([x, cy, 0])
    lin = Annulus(inner_radius=1.1, outer_radius=1.2, stroke_width=0, color=BLUE, fill_opacity=0.95).move_to([-3.0, cy, 0])
    return bath, rings, lin


class S00Title(TitleCard):
    LESSON = "Sensing the world: cGMP and the senses"
    TITLE = "How an Artery Learned to Relax"


class S01Rings(SpokenScene):
    def construct(self):
        q = T("What relaxes an artery?", 32, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(Write(q), run_time=1.6)
        bath, rings, lin = ring_set()
        musc_lbl = T("rabbit aorta", 24, ORANGE).move_to([0, 0.3, 0])
        self.at("rings of rabbit aorta")
        self.play(FadeIn(bath), GrowFromCenter(rings["L"]), GrowFromCenter(rings["R"]), run_time=0.9)
        self.play(FadeIn(musc_lbl), run_time=0.4)
        endo = T("endothelium", 22, BLUE).move_to([-3.0, 0.3, 0])
        keep = T("lining kept", 26, BLUE, weight=BOLD).move_to([-3.0, -2.45, 0])
        self.at("kept their endothelium")
        self.play(FadeOut(musc_lbl), run_time=0.2)
        self.play(FadeIn(lin, scale=1.2), FadeIn(endo), FadeIn(keep), run_time=0.7)
        gone = T("lining rubbed off", 26, GREY, weight=BOLD).move_to([3.0, -2.45, 0])
        self.at("rubbed off")
        self.play(FadeIn(gone, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S02Lining(SpokenScene):
    def construct(self):
        q = T("What relaxes an artery?", 32, font=TITLE_FONT).move_to([0, 3.0, 0])
        bath, rings, lin = ring_set()
        endo = T("endothelium", 22, BLUE).move_to([-3.0, 0.3, 0])
        keep = T("lining kept", 26, BLUE, weight=BOLD).move_to([-3.0, -2.45, 0])
        gone = T("lining rubbed off", 26, GREY, weight=BOLD).move_to([3.0, -2.45, 0])
        self.add(q, bath, rings["L"], rings["R"], lin, endo, keep, gone)
        ach = chip("acetylcholine", YELLOW, size=26).move_to([0, 3.0, 0])
        a1 = arr([-0.9, 2.75, 0], [-2.2, 2.4, 0], YELLOW)
        a2 = arr([0.9, 2.75, 0], [2.2, 2.4, 0], YELLOW)
        self.at("They added")
        self.play(FadeOut(q), FadeIn(ach), run_time=0.4)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.4)
        new_L = Annulus(inner_radius=1.5, outer_radius=2.05, stroke_width=2, color=ORANGE, fill_opacity=0.4).move_to([-3.0, 0.3, 0])
        new_lin = Annulus(inner_radius=1.4, outer_radius=1.5, stroke_width=0, color=BLUE, fill_opacity=0.95).move_to([-3.0, 0.3, 0])
        yes = T("relaxes", 26, GREEN, weight=BOLD).move_to([-3.0, -2.95, 0])
        self.at("relaxed the intact rings")
        self.play(Transform(rings["L"], new_L), Transform(lin, new_lin), FadeIn(yes, shift=UP * 0.1), run_time=0.9)
        no = T("does not relax", 26, RED, weight=BOLD).move_to([3.0, -2.95, 0])
        self.at("but not the rubbed")
        self.play(FadeIn(no, shift=UP * 0.1), Indicate(rings["R"], color=RED, scale_factor=1.03), run_time=0.7)

        # layers
        endo_box = cellbox(-5.5, 5.5, 0.7, 2.6, BLUE)
        musc_box = cellbox(-5.5, 5.5, -3.2, -0.7, ORANGE)
        endo_l = T("endothelium: the lining", 24, BLUE).move_to([-3.3, 2.15, 0])
        musc_l = T("smooth muscle", 24, ORANGE).move_to([-4.0, -2.75, 0])
        ach_y = dot(YELLOW, 0.2, [-4.5, 3.1, 0])
        ach_t = T("acetylcholine", 22, YELLOW).next_to(ach_y, RIGHT, buff=0.2)
        arrA = arr([-4.5, 2.85, 0], [-4.5, 2.2, 0], YELLOW)
        self.at("the lining was sending")
        self.play(*[FadeOut(m) for m in (bath, rings["L"], rings["R"], lin, endo, keep, gone, yes, no, ach, a1, a2)], run_time=0.4)
        self.play(FadeIn(endo_box), FadeIn(endo_l), FadeIn(ach_y), FadeIn(ach_t), GrowArrow(arrA), run_time=0.7)
        qchip = bchip("?", GREY, size=36, pad=0.24).move_to([0, 0, 0])
        self.at("something to the muscle")
        self.play(FadeIn(musc_box), FadeIn(musc_l), run_time=0.5)
        self.play(FadeIn(qchip, scale=0.8), run_time=0.4)
        secs = T("lasts only seconds", 22, GREY).move_to([-3.4, 0, 0])
        self.at("only seconds")
        self.play(FadeIn(secs, shift=RIGHT * 0.1), run_time=0.5)
        no_chip = bchip("NO", PINK, size=40, pad=0.25).move_to([0, 0, 0])
        who1 = T("Furchgott, 1986: proposes NO", 22, TEXT).move_to([3.4, 0.25, 0])
        who2 = T("Ignarro: the same proposal", 22, TEXT).move_to([3.4, -0.25, 0])
        self.at("proposed that it is")
        self.play(FadeIn(who1), run_time=0.5)
        self.at("gas nitric oxide")
        self.play(ReplacementTransform(qchip, no_chip), FadeOut(secs), run_time=0.7)
        self.at("independently proposed")
        self.play(FadeIn(who2), run_time=0.6)
        self.finish()


class S03Make(SpokenScene):
    def construct(self):
        endo_box = cellbox(-5.5, 5.5, 0.7, 2.6, BLUE)
        musc_box = cellbox(-5.5, 5.5, -3.2, -0.7, ORANGE)
        endo_l = T("endothelial cell", 22, BLUE).move_to([4.2, 2.25, 0])
        musc_l = T("smooth muscle cell", 24, ORANGE).move_to([-3.6, -2.75, 0])
        note = T("schematic, not to scale", 22, GREY).move_to([4.2, -3.2, 0])
        self.add(endo_box, musc_box, endo_l, musc_l)
        self.add(note)
        ach = dot(YELLOW, 0.2, [-4.5, 3.15, 0])
        ach_t = T("acetylcholine", 22, YELLOW).next_to(ach, RIGHT, buff=0.2)
        gpcr = bchip("GPCR", BLUE, size=24).move_to([-4.5, 2.6, 0])
        self.at("Acetylcholine binds")
        self.play(FadeIn(gpcr), FadeIn(ach), FadeIn(ach_t), run_time=0.5)
        self.play(ach.animate.move_to([-4.5, 3.0, 0]).set_opacity(1), FadeOut(ach_t), run_time=0.4)
        self.play(recolor(gpcr, GREEN)[0], recolor(gpcr, GREEN)[1], run_time=0.3)
        ca = bchip("Ca²⁺", GOLD, size=26).move_to([-2.9, 1.6, 0])
        a1 = arr([-4.2, 2.2, 0], [-3.4, 1.8, 0], GREY)
        self.at("calcium rises")
        self.play(GrowArrow(a1), FadeIn(ca, scale=0.8), run_time=0.5)
        cam = bchip("calmodulin", GREY, size=24).move_to([-1.0, 1.6, 0])
        self.at("bound to calmodulin")
        self.play(FadeIn(cam), run_time=0.4)
        self.play(ca.animate.next_to(cam, LEFT, buff=-0.05), run_time=0.5)
        cam_ca = VGroup(ca, cam)
        nos = bchip("nitric oxide\nsynthase", GREY, size=22, two=True).move_to([1.7, 1.65, 0])
        a2 = arr([-0.1, 1.6, 0], [0.7, 1.6, 0], GREY)
        self.at("switches on nitric oxide synthase")
        self.play(GrowArrow(a2), FadeIn(nos), run_time=0.5)
        self.play(*recolor(nos, PURPLE), run_time=0.4)
        arg = bchip("arginine", GREY, size=22).move_to([4.4, 1.2, 0])
        a3 = arr([3.6, 1.35, 0], [2.9, 1.55, 0], GREY)
        self.at("from the amino acid")
        self.play(FadeIn(arg), GrowArrow(a3), run_time=0.5)
        # NO dots made
        dots = VGroup(*[dot(PINK, 0.17, [1.1 + 0.55 * i, 0.95, 0]) for i in range(4)])
        no_t = T("NO", 26, PINK, weight=BOLD).move_to([0.35, 0.95, 0])
        self.at("arginine")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.2), FadeIn(no_t), run_time=0.8)
        self.at("small and uncharged")
        self.play(Indicate(dots, color=PINK, scale_factor=1.15), run_time=0.7)
        # cross membranes freely
        targets = [[0.9, -1.5], [1.9, -1.8], [2.8, -1.4], [1.4, -2.2]]
        no_t2 = T("NO", 26, PINK, weight=BOLD).move_to([4.2, -1.8, 0])
        self.at("crosses membranes freely")
        self.play(FadeOut(no_t), FadeIn(no_t2), *[d.animate.move_to([tx, ty, 0]) for d, (tx, ty) in zip(dots[:3], targets)],
                  dots[3].animate.move_to([4.2, -0.3, 0]).set_opacity(0.0), run_time=1.6)
        self.at("cannot be aimed")
        extra = VGroup(*[dot(PINK, 0.17, [1.7, 0.9, 0]) for _ in range(3)])
        self.add(extra)
        self.play(extra[0].animate.move_to([-0.2, 0.15, 0]), extra[1].animate.move_to([3.6, 0.1, 0]),
                  extra[2].animate.move_to([1.7, 0.1, 0]), run_time=1.0)
        self.at("within seconds")
        self.play(*[e.animate.set_opacity(0.0) for e in extra], run_time=0.8)
        self.at("near neighbors receive")
        self.play(Indicate(dots[:3], color=PINK, scale_factor=1.2), musc_box.animate.set_fill(ORANGE, 0.2), run_time=0.7)
        self.finish()


class S04Relax(SpokenScene):
    def construct(self):
        musc_box = cellbox(-6.2, 6.2, 0.05, 3.4, ORANGE).set_fill(ORANGE, 0.12)
        musc_l = T("smooth muscle cell", 22, ORANGE).move_to([-4.6, 3.05, 0])
        note = T("idealised", 22, GREY).move_to([5.2, -3.2, 0])
        # vessel wall, contracted
        def walls(top_y, bot_y):
            t = Rectangle(width=7.5, height=0.45, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                          fill_opacity=0.4).move_to([-1.2, top_y, 0])
            b = Rectangle(width=7.5, height=0.45, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                          fill_opacity=0.4).move_to([-1.2, bot_y, 0])
            return t, b
        wt, wb = walls(-1.6, -2.4)
        w_l = T("artery wall", 24, ORANGE).move_to([4.7, -2.0, 0])
        self.add(musc_box, musc_l, note, wt, wb, w_l)

        no = bchip("NO", PINK, size=30).move_to([-5.4, 1.65, 0])
        sgc = bchip("soluble\nguanylyl cyclase", GREY, size=22, two=True).move_to([-2.6, 1.65, 0])
        sgc_tag = T("heme iron", 22, GREY).move_to([-2.6, 0.85, 0])
        self.at("In the muscle cell")
        self.play(FadeIn(no, scale=0.8), run_time=0.5)
        self.at("binds the iron")
        self.play(FadeIn(sgc), FadeIn(sgc_tag), run_time=0.5)
        self.play(no.animate.next_to(sgc, LEFT, buff=0.15), run_time=0.5)
        self.at("changes shape")
        self.play(*recolor(sgc, GREEN), FadeOut(sgc_tag), run_time=0.4)
        self.play(sgc[1].animate.scale(1.12), sgc[2].animate.scale(1.12), run_time=0.25)
        self.play(sgc[1].animate.scale(1/1.12), sgc[2].animate.scale(1/1.12), run_time=0.25)
        gtp = bchip("GTP", GREY, size=24).move_to([-2.6, 2.75, 0])
        gtp_a = arr([-2.6, 2.45, 0], [-2.6, 2.1, 0], GREY, tip=0.18)
        cg = bchip("cGMP", TEAL, size=28).move_to([0.5, 1.65, 0])
        a_out = arr([-1.35, 1.65, 0], [-0.4, 1.65, 0], TEAL)
        self.at("and makes")
        self.play(FadeIn(gtp), GrowArrow(gtp_a), run_time=0.4)
        self.play(GrowArrow(a_out), FadeIn(cg, scale=0.8), run_time=0.6)
        pkg = bchip("protein\nkinase G", GREY, size=22, two=True).move_to([3.3, 1.65, 0])
        a_pk = arr([1.4, 1.65, 0], [2.2, 1.65, 0], TEAL)
        self.at("switches on protein kinase G")
        self.play(GrowArrow(a_pk), FadeIn(pkg), run_time=0.5)
        self.play(*recolor(pkg, GREEN), run_time=0.4)
        wt2, wb2 = walls(-1.1, -2.9)
        out_a = VGroup(arr([-1.2, -1.45, 0], [-1.2, -1.15, 0], GREEN, tip=0.16), arr([-1.2, -2.55, 0], [-1.2, -2.85, 0], GREEN, tip=0.16))
        rel = T("relaxes", 28, GREEN, weight=BOLD).move_to([5.0, -0.9, 0])
        self.at("The muscle relaxes")
        self.play(Transform(wt, wt2), Transform(wb, wb2), FadeIn(rel), run_time=1.2)
        self.at("vessel widens")
        self.play(Indicate(VGroup(wt, wb), color=GREEN, scale_factor=1.03), run_time=0.7)
        pde = bchip("PDE5", RED, size=28).move_to([0.5, 0.5, 0])
        a_p = arr([0.5, 0.82, 0], [0.5, 1.28, 0], RED)
        self.at("phosphodiesterase")
        self.play(FadeIn(pde), GrowArrow(a_p), run_time=0.5)
        self.at("ends the signal")
        ghost = DashedVMobject(cg[1].copy().set_fill(opacity=0), num_dashes=24).set_stroke(GREY)
        wt3, wb3 = walls(-1.6, -2.4)
        self.play(FadeOut(cg), FadeOut(a_out), FadeOut(a_pk), FadeIn(ghost), Transform(wt, wt3), Transform(wb, wb3), FadeOut(rel), run_time=0.9)
        self.play(*[pkg[1].animate.set_stroke(GREY).set_fill(GREY, 0.1), pkg[2].animate.set_color(GREY)], run_time=0.5)
        self.at("Outside the eye")
        self.play(*[FadeOut(m) for m in (pde, a_p, ghost, pkg, gtp, gtp_a, sgc, no, rel, musc_l)], run_time=0.6)
        cg2 = bchip("cGMP", TEAL, size=40, pad=0.25).move_to([-1.0, 1.65, 0])
        up = arr([1.2, 0.7, 0], [1.2, 2.6, 0], TEAL, w=9, tip=0.4)
        rise = T("rises", 30, GREEN, weight=BOLD).move_to([2.3, 1.65, 0])
        self.play(FadeIn(cg2, scale=0.8), GrowArrow(up), FadeIn(rise), run_time=0.7)
        self.at("by rising")
        self.play(Indicate(up, color=GREEN, scale_factor=1.08), run_time=0.6)
        self.finish()


class S05End(EndCard):
    LINE = "Outside the eye, cGMP carries its signal by rising."
