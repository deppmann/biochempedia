"""Hedgehog and the primary cilium: Hedgehog switches off an off-switch  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = Hedgehog, the signal
  BLUE   = Patched, the brake protein (the off-switch)
  PURPLE = Smoothened, the protein the brake keeps off (the switch)
  ORANGE = Gli, the transcription factor (its front part and its back part)
  GOLD   = a phosphate badge
  TEAL   = the ubiquitin tag
  GREEN  = ON / active
  RED    = OFF / the brake's action (a bar that switches something off)
  GREY   = membranes, cilium, cell outline, kinases, proteasome, target genes, de-emphasised things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
YM = 0.5  # y of the membrane bar in the membrane pictures


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, color=GREY, size=28):
    """dashed outline with a label: a thing that is absent."""
    c = chip(text, color, size=size)
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height), num_dashes=34).set_color(color)
    return VGroup(box, c[1])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 1))


def toggle(on=False, color=None, scale=1.0):
    c = color or (GREEN if on else RED)
    body = RoundedRectangle(corner_radius=0.5, width=2.0, height=1.0, stroke_color=c, stroke_width=5,
                            fill_color=c, fill_opacity=0.25)
    knob = Circle(radius=0.36, stroke_width=0, fill_color=TEXT, fill_opacity=1)
    knob.move_to(body.get_center() + RIGHT * (0.5 if on else -0.5))
    g = VGroup(body, knob)
    g.body, g.knob = body, knob
    g.scale(scale)
    return g


def flip(sw, on, color):
    off = sw.body.width * 0.25
    tgt = sw.body.get_center() + RIGHT * (off if on else -off)
    return [sw.knob.animate.move_to(tgt), sw.body.animate.set_stroke(color).set_fill(color, 0.25)]


def pbadge(size=0.24):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def badge(on, size=26):
    return T("ON" if on else "OFF", size, GREEN if on else RED, weight=BOLD)


def protein(color, w, h, label=None, ls=24):
    """a protein crossing the membrane: opaque backing, tinted body, label in the top part."""
    back = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    body = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.28)
    g = VGroup(back, body)
    g.back, g.body, g.col, g.lab = back, body, color, None
    if label:
        g.lab = T(label, ls, color).move_to(body.get_center() + UP * (h / 2 - 0.55))
        g.add(g.lab)
    return g


def ghost_protein(color, w, h, label=None, ls=24, above=False):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=w, height=h), num_dashes=40).set_color(GREY)
    g = VGroup(box)
    if label:
        dy = (h / 2 + 0.4) if above else (h / 2 - 0.55)
        g.add(T(label, ls, GREY).move_to(box.get_center() + UP * dy))
    return g


def dim_anims(p):
    return [p.body.animate.set_stroke(p.col, opacity=0.35).set_fill(p.col, 0.05), p.lab.animate.set_opacity(0.4)]


def undim_anims(p):
    return [p.body.animate.set_stroke(p.col, opacity=1).set_fill(p.col, 0.28), p.lab.animate.set_opacity(1)]


def brake(x0, x1, depth, y0=None, y1=None):
    """a red brake arc from under Patched to just short of the foot of a Smoothened, ending in a bar."""
    y0 = YM - PH / 2 - 0.05 if y0 is None else y0
    y1 = YM - SH / 2 - 0.12 if y1 is None else y1
    D = depth * 1.35
    curve = CubicBezier(np.array([x0, y0, 0]), np.array([x0, y0 - D, 0]),
                        np.array([x1, y1 - D, 0]), np.array([x1, y1, 0]))
    curve.set_stroke(RED, 5).set_fill(opacity=0)
    bar = Line([x1 - 0.3, y1, 0], [x1 + 0.3, y1, 0], color=RED, stroke_width=6)
    return VGroup(curve, bar)


def membrane(x0=-6.3, x1=6.3, y=YM, h=0.5):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def swap(a, b):
    """cross-fade one label for another (a letter-by-letter morph looks broken half way)."""
    return AnimationGroup(FadeOut(a), FadeIn(b))


def chip_dim(c, color, o=0.35):
    return [c[1].animate.set_stroke(color, opacity=o).set_fill(color, 0.05), c[2].animate.set_opacity(o)]


def chip_lit(c, color):
    return [c[1].animate.set_stroke(color, opacity=1).set_fill(color, 0.16), c[2].animate.set_opacity(1)]


def retract(arc):
    """animations that pull a brake arc back toward Patched."""
    return [FadeOut(arc[1]), Uncreate(arc[0])]


# the membrane picture: one Patched, four Smoothened (near and far, left and right)
SM = [(2.75, 0.9, 0.7), (-2.75, 0.9, -0.7), (4.85, 1.5, 0.35), (-4.85, 1.5, -0.35)]   # (x, arc depth, arc start x)
PW, PH, SW, SH = 2.0, 3.2, 1.5, 2.8


def make_patched(x=0.0, label="Patched"):
    return protein(BLUE, PW, PH, label).move_to([x, YM, 0])


def make_smo(x, label=None, w=SW, h=SH, ls=24):
    """Smoothened is narrower than its name, so its label sits just above the body."""
    g = protein(PURPLE, w, h).move_to([x, YM, 0])
    if label:
        g.lab = T(label, ls, PURPLE).move_to([x, YM + h / 2 + 0.5, 0])
        g.add(g.lab)
    return g


def badge_at(p, on, dy=-1.0):
    return badge(on).move_to(p.body.get_center() + UP * dy)


def halo(p):
    return SurroundingRectangle(p.body, color=GREEN, buff=0.1, corner_radius=0.38, stroke_width=4)


class S00Title(TitleCard):
    LESSON = "Hedgehog and the primary cilium"
    TITLE = "Hedgehog switches off an off-switch"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """adding a phosphate switches a switch on; Hedgehog does the opposite: bar, off-switch, bar, switch."""

    def construct(self):
        CX = -2.2   # x of the chain
        sw = toggle(False, scale=2.2).move_to([0.0, 0.0, 0])
        sw_lbl = T("switch", 32, GREY).next_to(sw, DOWN, buff=0.45)
        self.at("Most pathways")
        self.play(FadeIn(sw, scale=0.9), FadeIn(sw_lbl), run_time=0.7)

        p = pbadge(0.34).move_to([-5.0, 1.2, 0])
        self.at("adding something")
        self.play(FadeIn(p, scale=0.6), run_time=0.4)
        self.play(p.animate.move_to(sw.body.get_corner(UR) + [-0.15, 0.15, 0]), run_time=0.8)
        self.play(*flip(sw, True, GREEN), run_time=0.5)

        # Hedgehog works the other way
        hh = bchip("Hedgehog", YELLOW, 38).move_to([CX, 3.0, 0])
        self.at("Hedgehog works")
        self.play(FadeOut(p), FadeOut(sw_lbl), *flip(sw, False, RED), run_time=0.4)
        self.play(sw.animate.scale(0.68).move_to([CX, -2.5, 0]), FadeIn(hh, shift=DOWN * 0.2), run_time=0.6)
        sw_l2 = T("switch", 30, GREY).next_to(sw, RIGHT, buff=0.5)
        self.play(FadeIn(sw_l2), run_time=0.2)
        direct = arr([CX, 2.4, 0], [CX, -1.7, 0], GREEN, w=7, tip=0.3)
        self.at("other way")
        self.play(GrowArrow(direct), run_time=0.7)
        x1 = Line([CX - 0.5, 0.65, 0], [CX + 0.5, -0.35, 0], color=RED, stroke_width=10)
        x2 = Line([CX - 0.5, -0.35, 0], [CX + 0.5, 0.65, 0], color=RED, stroke_width=10)
        self.play(Create(x1), Create(x2), run_time=0.4)

        # the real route: bar, off-switch, bar
        side = T("tells cells where they are", 32, GREY).move_to([3.4, 3.0, 0])
        self.at("tells the cells")
        self.play(FadeIn(side, shift=LEFT * 0.15), run_time=0.5)
        off = bchip("off-switch", BLUE, 38).move_to([CX, 0.3, 0])
        bar1 = inhib([CX, 2.4, 0], [CX, 0.9, 0])
        bar2 = inhib([CX, -0.3, 0], [CX, -1.7, 0])
        # first, with no Hedgehog acting: the off-switch holds the switch OFF
        self.at("by switching")
        self.play(FadeOut(direct), FadeOut(VGroup(x1, x2)), FadeOut(side), *chip_dim(hh, YELLOW), run_time=0.4)
        self.play(FadeIn(off, scale=0.9), Create(bar2), run_time=0.6)
        # then Hedgehog blocks the off-switch, and the switch turns ON
        self.at("off switch")
        self.play(*chip_lit(hh, YELLOW), Create(bar1), *chip_dim(off, BLUE), bar2.animate.set_opacity(0.3),
                  *flip(sw, True, GREEN), run_time=1.0)
        self.at("piece of logic")
        self.play(Indicate(bar1, color=RED, scale_factor=1.15), run_time=0.8)
        dn = T("double negative", 46, font=TITLE_FONT).move_to([3.3, 0.3, 0])
        self.at("double negative")
        self.play(Indicate(bar1, color=RED, scale_factor=1.15), FadeIn(dn, shift=LEFT * 0.2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def membrane_stage():
    """the s02 end state, built instantly (also the start of s03)."""
    mem = membrane()
    pat = make_patched()
    smos = [make_smo(x, "Smoothened" if i == 0 else None) for i, (x, _, _) in enumerate(SM)]
    return mem, pat, smos


class S02Brake(SpokenScene):
    """default state: active Patched keeps Smoothened off, without holding it; one Patched, many Smoothened."""

    def construct(self):
        mem = membrane()
        out_l = T("outside the cell", 24, GREY).move_to([-4.6, 3.3, 0])
        in_l = T("inside the cell", 24, GREY).move_to([-4.6, -3.3, 0])
        pat = make_patched()
        smos = [make_smo(x, "Smoothened" if i == 0 else None) for i, (x, _, _) in enumerate(SM)]
        sm1 = smos[0]
        self.at("Two proteins")
        self.play(Create(mem), FadeIn(out_l), FadeIn(in_l), run_time=0.6)
        self.play(FadeIn(pat, shift=UP * 0.15), FadeIn(sm1, shift=UP * 0.15), run_time=0.7)

        self.at("Patched is a")
        self.play(Indicate(VGroup(pat.body, pat.lab), color=BLUE, scale_factor=1.07), run_time=0.8)
        self.at("Smoothened is the protein")
        self.play(Indicate(VGroup(sm1.body, sm1.lab), color=PURPLE, scale_factor=1.07), run_time=0.8)

        ghost = ghost_chip("no Hedgehog", GREY, 30).move_to([0, 3.1, 0])
        self.at("With no Hedgehog")
        self.play(FadeIn(ghost, shift=DOWN * 0.15), run_time=0.6)

        b_pat = badge_at(pat, True)
        self.at("Patched is active")
        self.play(FadeIn(b_pat, scale=0.6), run_time=0.4)
        arcs = [brake(sx, x, d) for (x, d, sx) in SM]
        b_sm1 = badge_at(sm1, False)
        self.at("so Smoothened is off")
        self.play(Create(arcs[0][0]), FadeIn(arcs[0][1]), FadeIn(b_sm1, scale=0.6), run_time=0.9)

        # not held: Smoothened slides by itself
        mover = VGroup(sm1, b_sm1)
        self.at("does not hold")
        self.play(mover.animate.shift(RIGHT * 0.35), run_time=0.45)
        self.play(mover.animate.shift(LEFT * 0.35), run_time=0.45)

        # one Patched, many Smoothened
        self.at("One Patched can keep")
        self.play(Indicate(VGroup(pat.body, pat.lab), color=BLUE, scale_factor=1.06), run_time=0.7)
        badges = [b_sm1]
        anims = []
        for i in (1, 2, 3):
            b = badge_at(smos[i], False)
            badges.append(b)
            anims.append(AnimationGroup(FadeIn(smos[i], shift=UP * 0.1), Create(arcs[i][0]), FadeIn(arcs[i][1]), FadeIn(b)))
        self.at("many Smoothened")
        self.play(LaggedStart(*anims, lag_ratio=0.35), run_time=1.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Release(SpokenScene):
    """Hedgehog binds Patched: it switches off, the brake arcs retract, every Smoothened is on."""

    def construct(self):
        mem, pat, smos = membrane_stage()
        b_pat = badge_at(pat, True)
        b_sms = [badge_at(s, False) for s in smos]
        arcs = [brake(sx, x, d) for (x, d, sx) in SM]
        ghost = ghost_chip("no Hedgehog", GREY, 30).move_to([0, 3.1, 0])
        self.add(mem, pat, *smos, b_pat, *b_sms, *arcs, ghost)

        hh = bchip("Hedgehog", YELLOW, 30).move_to([0, 3.1, 0])
        self.at("Now Hedgehog arrives")
        self.play(FadeOut(ghost), FadeIn(hh, shift=DOWN * 0.1), run_time=0.7)
        self.at("binds Patched")
        self.play(hh.animate.move_to([0, YM + PH / 2 + 0.5, 0]), run_time=0.8)

        # the accelerator it does not press
        acc = arr([-1.15, 2.85, 0], [-2.5, 2.1, 0], GREY, w=7, tip=0.3)
        acc_l = T("accelerator", 28, GREY).move_to([-3.3, 3.1, 0])
        cx1 = Line([-2.15, 2.85, 0], [-1.65, 2.2, 0], color=RED, stroke_width=10)
        cx2 = Line([-2.15, 2.2, 0], [-1.65, 2.85, 0], color=RED, stroke_width=10)
        self.at("does not press")
        self.play(GrowArrow(acc), FadeIn(acc_l), run_time=0.5)
        self.play(Create(cx1), Create(cx2), run_time=0.35)

        self.at("releases the handbrake")
        self.play(FadeOut(VGroup(acc, acc_l, cx1, cx2)), *dim_anims(pat), *[a for ar in arcs for a in retract(ar)], run_time=1.1)

        b_pat_off = badge_at(pat, False)
        self.at("switched off")
        self.play(swap(b_pat, b_pat_off), run_time=0.4)
        halos = [halo(s) for s in smos]
        b_sms_on = [badge_at(s, True) for s in smos]
        self.at("Smoothened is on")
        self.play(*[swap(a, b) for a, b in zip(b_sms, b_sms_on)], *[Create(h) for h in halos], run_time=0.8)

        # the chain: Hedgehog, Patched, Smoothened
        c1 = bchip("Hedgehog", YELLOW, 26)
        c2 = bchip("Patched", BLUE, 26)
        c3 = bchip("Smoothened", PURPLE, 26)
        c1.move_to([-3.7, -3.05, 0]); c2.move_to([-0.0, -3.05, 0]); c3.move_to([3.8, -3.05, 0])
        i1 = inhib([c1.get_right()[0] + 0.05, -3.05, 0], [c2.get_left()[0] - 0.05, -3.05, 0])
        i2 = inhib([c2.get_right()[0] + 0.05, -3.05, 0], [c3.get_left()[0] - 0.05, -3.05, 0])
        self.at("switches off the protein")
        self.play(FadeIn(c1), FadeIn(c2), Create(i1), run_time=0.8)
        self.at("keeps Smoothened off")
        self.play(FadeIn(c3), Create(i2), run_time=0.7)
        self.at("double negative")
        self.play(Indicate(i1, color=RED, scale_factor=1.2), Indicate(i2, color=RED, scale_factor=1.2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gli(SpokenScene):
    """Smoothened off: Gli is marked and its back part is destroyed -> repressor. Smoothened on: Gli stays whole."""

    def construct(self):
        sm = bchip("Smoothened", PURPLE, 30).move_to([-4.6, 3.0, 0])
        GY = 0.1   # y of the Gli bar
        FX, BX = -2.2, 2.0
        front = RoundedRectangle(corner_radius=0.2, width=4.0, height=1.3, stroke_color=ORANGE, stroke_width=4,
                                 fill_color=ORANGE, fill_opacity=0.5).move_to([FX, GY, 0])
        back = RoundedRectangle(corner_radius=0.2, width=4.4, height=1.3, stroke_color=ORANGE, stroke_width=4,
                                fill_color=ORANGE, fill_opacity=0.2).move_to([BX, GY, 0])
        gli_l = T("Gli", 42, TEXT, weight=BOLD).move_to(front)
        gli = VGroup(front, back, gli_l)

        genes = Rectangle(width=11.0, height=0.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.15).move_to([-0.4, -3.0, 0])
        genes_l = T("target genes", 30, GREY).move_to(genes)
        genes_g = VGroup(genes, genes_l)

        self.at("The pathway ends")
        self.play(FadeIn(gli, shift=UP * 0.15), run_time=0.8)

        b_sm = badge(False, 30).next_to(sm, RIGHT, buff=0.3)
        self.at("With Smoothened off")
        self.play(FadeIn(sm, shift=DOWN * 0.15), FadeIn(b_sm, scale=0.6), run_time=0.6)

        # kinases add phosphates
        kin = bchip("kinases", GREY, 28).move_to([-5.2, 1.7, 0])
        ps = [pbadge().move_to(kin.get_center()) for _ in range(3)]
        spots = [[-3.4, GY + 1.2, 0], [-1.2, GY + 1.2, 0], [2.6, GY + 1.2, 0]]
        self.at("kinases add phosphates")
        self.play(FadeIn(kin), run_time=0.4)
        self.play(LaggedStart(*[p.animate.move_to(s) for p, s in zip(ps, spots)], lag_ratio=0.25), run_time=1.3)

        ub = bchip("ubiquitin", TEAL, 28).move_to([0.5, 2.2, 0])
        ub_line = Line(ub.get_bottom(), [0.5, GY + 0.65, 0], color=TEAL, stroke_width=3)
        self.at("ubiquitin tags")
        self.play(FadeIn(ub, shift=DOWN * 0.15), Create(ub_line), run_time=0.7)

        pro = bchip("proteasome", GREY, 28).move_to([4.2, 2.2, 0])
        self.at("for the proteasome")
        self.play(pro.animate.move_to([BX, GY, 0]), run_time=0.9)
        ghost_back = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=4.4, height=1.3), num_dashes=34).set_color(GREY).move_to(back)
        act_l = T("activating region", 26, GREY).move_to([BX, GY - 1.2, 0])
        self.at("destroys only")
        self.play(FadeOut(back), FadeOut(ps[2]), run_time=0.6)
        self.play(pro.animate.move_to([4.2, 2.2, 0]).set_opacity(0), FadeIn(ghost_back), run_time=0.8)
        self.at("activating region")
        self.play(FadeIn(act_l, shift=UP * 0.1), run_time=0.5)

        dna_l = T("binds DNA", 26, ORANGE).move_to([FX, GY - 1.2, 0])
        self.at("front part")
        self.play(Indicate(front, color=ORANGE, scale_factor=1.04), FadeIn(dna_l, shift=UP * 0.1), run_time=0.8)
        rep_l = T("repressor", 34, ORANGE, weight=BOLD)
        b_genes = badge(False, 32).move_to([5.7, -3.0, 0])
        self.at("as a repressor")
        frontg = VGroup(front, gli_l)
        self.play(FadeOut(VGroup(ub, ub_line, ps[0], ps[1], dna_l, act_l, ghost_back, kin)), FadeIn(genes_g), run_time=0.5)
        self.play(frontg.animate.move_to([FX, -1.85, 0]), run_time=0.8)
        rep_l.next_to(frontg, RIGHT, buff=0.5)
        self.play(FadeIn(rep_l, shift=LEFT * 0.1), run_time=0.4)
        self.at("target genes off")
        self.play(FadeIn(b_genes, scale=0.6), run_time=0.5)

        # Smoothened on: the marking stops, Gli stays whole
        b_sm_on = badge(True, 30).next_to(sm, RIGHT, buff=0.3)
        front2 = front.copy().move_to([FX, GY, 0])
        back2 = RoundedRectangle(corner_radius=0.2, width=4.4, height=1.3, stroke_color=ORANGE, stroke_width=4,
                                 fill_color=ORANGE, fill_opacity=0.2).move_to([BX, GY, 0])
        gl2 = T("Gli", 42, TEXT, weight=BOLD).move_to(front2)
        gli2 = VGroup(front2, back2, gl2)
        self.at("With Smoothened on")
        self.play(FadeOut(VGroup(frontg, rep_l)), FadeOut(b_genes), swap(b_sm, b_sm_on), FadeIn(gli2, shift=UP * 0.15), run_time=0.8)
        kin2 = bchip("kinases", GREY, 28).move_to([-5.2, 1.7, 0])
        stop = inhib([-4.5, 1.45, 0], [-3.5, 0.95, 0])
        self.at("marking stops")
        self.play(FadeIn(kin2), Create(stop), run_time=0.7)
        act_g = T("activator", 34, ORANGE, weight=BOLD)
        b_genes_on = badge(True, 32).move_to([5.7, -3.0, 0])
        self.at("stays whole")
        self.play(Indicate(gli2, color=ORANGE, scale_factor=1.03), run_time=0.8)
        self.at("becomes an activator")
        self.play(gli2.animate.move_to([-0.2, -1.85, 0]), run_time=0.9)
        act_g.next_to(gli2, UP, buff=0.25)
        self.play(FadeIn(act_g), FadeIn(b_genes_on, scale=0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Cilium(SpokenScene):
    """vertebrates: Patched sits in the cilium wall, Smoothened outside; Hedgehog binds, they swap places."""

    def construct(self):
        YT = -1.1   # y of the cell's top edge
        CW = 1.2    # half width of the cilium
        body = RoundedRectangle(corner_radius=0.5, width=12.4, height=2.4, stroke_color=GREY, stroke_width=4).move_to([0, YT - 1.2, 0])
        patch = Rectangle(width=2 * CW - 0.06, height=0.2, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, YT, 0])
        wall_l = Line([-CW, YT, 0], [-CW, 2.0, 0], color=GREY, stroke_width=4)
        wall_r = Line([CW, YT, 0], [CW, 2.0, 0], color=GREY, stroke_width=4)
        tip = ArcBetweenPoints([-CW, 2.0, 0], [CW, 2.0, 0], angle=-PI, color=GREY, stroke_width=4)
        cilium = VGroup(wall_l, wall_r, tip)
        cil_l = T("primary cilium", 28, GREY).move_to([-4.0, 2.2, 0])

        self.at("In vertebrates")
        self.play(Create(body), run_time=0.9)
        self.at("primary cilium")
        self.add(patch)
        self.play(Create(cilium), FadeIn(cil_l), run_time=1.2)
        self.at("a single")
        self.play(Indicate(cilium, color=TEXT, scale_factor=1.04), run_time=0.8)

        ghost = ghost_chip("no Hedgehog", GREY, 28).move_to([4.6, 2.6, 0])
        self.at("Without Hedgehog")
        self.play(FadeIn(ghost, shift=DOWN * 0.15), run_time=0.5)
        pat = bchip("Patched", BLUE, 28).move_to([CW, 0.9, 0])
        smo = bchip("Smoothened", PURPLE, 28).move_to([-3.7, YT, 0])
        self.at("Patched sits at")
        self.play(FadeIn(pat, scale=0.8), run_time=0.5)
        self.at("Smoothened stays out")
        self.play(FadeIn(smo, scale=0.8), run_time=0.5)

        hh = bchip("Hedgehog", YELLOW, 28)
        hh_bound = [pat.get_right()[0] + hh.width / 2 + 0.03, 0.9, 0]
        hh.move_to(ghost)
        self.at("When Hedgehog binds")
        self.play(FadeOut(ghost), FadeIn(hh), run_time=0.4)
        self.play(hh.animate.move_to(hh_bound), run_time=0.6)

        # Patched leaves the cilium (Hedgehog stays bound to it); then Smoothened moves in
        dx = hh.get_center()[0] - pat.get_center()[0]
        self.at("Patched leaves")
        self.play(pat.animate.move_to([CW, -0.2, 0]), hh.animate.move_to([CW + dx, -0.2, 0]), run_time=0.7)
        self.play(pat.animate.move_to([CW, YT, 0]), run_time=0.4)
        self.play(pat.animate.move_to([4.2, YT, 0]), hh.animate.move_to([4.2, YT + 0.95, 0]), run_time=0.8)
        self.at("moves in")
        self.play(smo.animate.move_to([-CW, YT, 0]), run_time=0.7)
        self.play(smo.animate.move_to([-CW, 0.9, 0]), run_time=0.8)

        # Gli at the tip, sent to the nucleus as activators
        g1 = chip("Gli", ORANGE, 24).move_to([-0.45, 2.3, 0])
        g2 = chip("Gli", ORANGE, 24).move_to([0.55, 2.3, 0])
        nuc = Ellipse(width=3.8, height=1.9, stroke_color=GREY, stroke_width=3).move_to([-3.6, -2.25, 0])
        nuc_l = T("nucleus", 24, GREY).move_to([-3.6, -2.85, 0])
        self.at("gathered at the tip")
        self.play(FadeIn(g1, scale=0.7), FadeIn(g2, scale=0.7), FadeIn(nuc), FadeIn(nuc_l), run_time=0.6)
        pts2 = [g2.get_center(), [0.65, 0.2, 0], [0.65, YT - 0.2, 0], [-2.0, -1.9, 0], [-4.1, -1.9, 0]]
        pts1 = [g1.get_center(), [0.65, 2.0, 0], [0.65, 0.2, 0], [0.65, YT - 0.2, 0], [-2.0, -1.9, 0], [-3.1, -1.9, 0]]
        path2 = VMobject().set_points_as_corners([np.array(p, float) for p in pts2])
        path1 = VMobject().set_points_as_corners([np.array(p, float) for p in pts1])
        self.at("sent to the nucleus")
        self.play(LaggedStart(MoveAlongPath(g2, path2, rate_func=smooth), MoveAlongPath(g1, path1, rate_func=smooth), lag_ratio=0.55), run_time=1.8)
        act_l = T("activators", 30, ORANGE, weight=BOLD).move_to([-0.1, -2.3, 0])
        self.at("activators")
        self.play(FadeIn(act_l, shift=RIGHT * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Predict(SpokenScene):
    """lose a part, watch the pathway lamp: the later step decides. Ask what state Smoothened is in.

    Every case starts by resetting the lamp and the ON/OFF tags to neutral, so no frame ever pairs a
    new case label with the previous case's result; the result is shown on the narrator's words."""

    def construct(self):
        XP, XS = -3.7, 0.0
        P6W, P6H, S6W, S6H = 2.4, 3.2, 2.0, 2.7
        BY = -0.4   # y of the state badges
        mem = membrane(-6.3, 1.9)

        def mk_pat():
            return protein(BLUE, P6W, P6H, "Patched", 28).move_to([XP, YM, 0])

        def mk_smo():
            return make_smo(XS, "Smoothened", S6W, S6H, 28)

        def bdg(x, on):
            return badge(on, 30).move_to([x, BY, 0])

        def mk_arc():
            return brake(XP + 0.6, XS, 1.0, y0=YM - P6H / 2 - 0.05, y1=YM - S6H / 2 - 0.12)

        def readout(on):
            return badge(on, 64).move_to([5.1, 0.0, 0])

        def unknown():
            return T("?", 64, GREY, weight=BOLD).move_to([5.1, 0.0, 0])

        def lamp_neutral():
            return lamp.animate.set_stroke(GREY).set_fill(GREY, 0.3)

        def lamp_on(on):
            c = GREEN if on else RED
            return lamp.animate.set_stroke(c).set_fill(c, 0.5)

        def hh_chip():
            return bchip("Hedgehog", YELLOW, 30).move_to([XP, 2.95, 0])

        def case(text):
            return T(text, 38, TEXT, font=TITLE_FONT).move_to([4.5, 2.7, 0])

        pat, smo, arc = mk_pat(), mk_smo(), mk_arc()
        b_pat, b_smo = bdg(XP, True), bdg(XS, False)
        pw_l = T("pathway", 34, GREY).move_to([4.5, 1.3, 0])
        lamp = Circle(radius=0.45, stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.5).move_to([3.4, 0.0, 0])
        ro = readout(False)
        self.at("Now use that logic")
        self.play(Create(mem), run_time=0.5)
        self.play(FadeIn(pat), FadeIn(smo), run_time=0.5)
        self.play(FadeIn(b_pat), FadeIn(b_smo), Create(arc[0]), FadeIn(arc[1]), FadeIn(pw_l), FadeIn(lamp), FadeIn(ro), run_time=0.9)

        # --- no Patched -----------------------------------------------------------------
        gp = ghost_protein(BLUE, P6W, P6H, "Patched", 28).move_to([XP, YM, 0])
        cs = case("no Patched")
        q = unknown()
        self.at("With no Patched")
        self.play(lamp_neutral(), swap(ro, q), FadeOut(b_pat), FadeOut(b_smo), run_time=0.3)   # reset first
        ro = q
        self.play(FadeIn(cs, shift=DOWN * 0.1), FadeOut(pat), FadeIn(gp), *retract(arc), run_time=0.8)
        b_smo_on, ro_on = bdg(XS, True), readout(True)
        hh = hh_chip()
        self.at("pathway is on")
        self.play(FadeIn(b_smo_on, scale=0.6), swap(ro, ro_on), lamp_on(True), FadeIn(hh, shift=DOWN * 0.15), run_time=0.6)
        ro = ro_on
        self.at("without Hedgehog")
        self.play(FadeOut(hh, shift=UP * 0.15), run_time=0.5)

        # --- no Smoothened --------------------------------------------------------------
        gs = VGroup(ghost_protein(PURPLE, S6W, S6H).move_to([XS, YM, 0]),
                    T("Smoothened", 28, GREY).move_to([XS, YM + S6H / 2 + 0.5, 0]))
        cs2 = case("no Smoothened")
        pat2 = mk_pat()
        q = unknown()
        self.at("With no Smoothened")
        self.play(lamp_neutral(), swap(ro, q), FadeOut(b_smo_on), FadeOut(cs), run_time=0.3)   # reset first
        ro = q
        self.play(FadeIn(cs2, shift=DOWN * 0.1), FadeOut(gp), FadeIn(pat2), FadeOut(smo), FadeIn(gs), run_time=0.8)
        ro_off, b_pat2 = readout(False), bdg(XP, True)
        self.at("pathway is off")
        self.play(swap(ro, ro_off), lamp_on(False), FadeIn(b_pat2, scale=0.6), run_time=0.6)
        ro = ro_off
        hh = hh_chip()
        b_pat2_off = bdg(XP, False)
        self.at("both ways")
        self.play(FadeIn(hh, shift=DOWN * 0.15), *dim_anims(pat2), swap(b_pat2, b_pat2_off), run_time=0.5)
        b_pat2_on = bdg(XP, True)
        self.wait(0.5)
        self.play(FadeOut(hh, shift=UP * 0.15), *undim_anims(pat2), swap(b_pat2_off, b_pat2_on), run_time=0.5)
        b_pat2 = b_pat2_on

        # --- neither --------------------------------------------------------------------
        cs3 = case("neither")
        gp2 = ghost_protein(BLUE, P6W, P6H, "Patched", 28).move_to([XP, YM, 0])
        q = unknown()
        self.at("with", nth=3)
        self.play(lamp_neutral(), swap(ro, q), FadeOut(b_pat2), FadeOut(cs2), run_time=0.3)   # reset first
        ro = q
        self.play(FadeIn(cs3, shift=DOWN * 0.1), FadeOut(pat2), FadeIn(gp2), run_time=0.7)
        ro_off3 = readout(False)
        self.at("off as well")
        self.play(swap(ro, ro_off3), lamp_on(False), run_time=0.5)
        ro = ro_off3
        self.at("later step decides")
        self.play(Indicate(gs, color=PURPLE, scale_factor=1.06), run_time=0.9)

        # --- the rule -------------------------------------------------------------------
        pat3, smo3, arc3 = mk_pat(), mk_smo(), mk_arc()
        b3p, b3s = bdg(XP, True), bdg(XS, False)
        qq = T("What state is Smoothened in?", 42, TEXT, font=TITLE_FONT).move_to([-2.0, -3.2, 0])
        self.at("So ask what state")
        self.play(FadeOut(cs3), FadeOut(gp2), FadeOut(gs), FadeIn(pat3), FadeIn(smo3), FadeIn(b3p), FadeIn(b3s),
                  Create(arc3[0]), FadeIn(arc3[1]), run_time=1.0)
        ring = SurroundingRectangle(smo3.body, color=TEXT, buff=0.1, corner_radius=0.38, stroke_width=5)
        self.at("Smoothened is in")
        self.play(Create(ring), FadeIn(qq, shift=UP * 0.1), run_time=0.8)
        self.at("everything after it")
        self.play(Indicate(ring, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Ask what state Smoothened is in, and everything after it follows."
