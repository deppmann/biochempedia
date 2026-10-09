"""Signal transduction: cells compute with switches  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = first messenger (the extracellular signal: ligand, hormone, glucagon, epinephrine)
  BLUE   = receptor
  TEAL   = second messenger (cAMP, IP3, Ca2+)
  PURPLE = effector enzymes / kinases / target proteins (PKA, glycogen synthase, ...)
  ORANGE = the response, the fuel that comes out (glucose, fatty acids)
  GREEN  = ON / activated
  RED    = OFF / termination / failure (phosphatase, PDE, the stuck switch)
  GOLD   = a phosphate group (the little "P" badge)
  GREY   = membranes, outlines, stores, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color):
    """animations that recolor a bchip without touching its opaque backing."""
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def dim(c, o=0.4):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def pulse(c, color, s=1.1, **kw):
    """Indicate a bchip without recoloring its opaque backing (which would hide the label)."""
    return Indicate(VGroup(*c[1:]), color=color, scale_factor=s, **kw)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def toggle(on=False, color=None, scale=1.0):
    c = color or (GREEN if on else GREY)
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


def membrane_h(y, x0=-6.3, x1=6.3, h=0.32):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


class S00Title(TitleCard):
    LESSON = "Signal transduction"
    TITLE = "Cells compute with switches"


# ---------------------------------------------------------------------------------------------
class S01Switch(SpokenScene):
    """switch ON (ligand binds receptor, messengers fan out) -> switch OFF (phosphatase, PDE) -> four-beat sentence."""

    def construct(self):
        head = T("Cell signaling as switch logic", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=1.3)
        sw = toggle(False, scale=1.3).move_to([-0.4, 0.2, 0])
        state = T("OFF", 30, GREY, weight=BOLD).next_to(sw, UP, buff=0.35)
        self.at("switch logic")
        self.play(FadeIn(sw, scale=0.9), FadeIn(state), run_time=0.6)

        # --- ligand binds receptor ---------------------------------------------------------
        mem = RoundedRectangle(corner_radius=0.1, width=0.3, height=2.5, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([-3.7, 0.3, 0])
        rec = RoundedRectangle(corner_radius=0.2, width=0.7, height=1.4, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.3).move_to([-3.7, 0.3, 0])
        rec_lbl = T("receptor", 28, BLUE).move_to([-3.7, -1.3, 0])
        lig = VGroup(Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9),
                     ).move_to([-5.4, 1.8, 0])
        lig_lbl = T("ligand", 28, YELLOW).next_to(lig, UP, buff=0.15)
        lig_g = VGroup(lig, lig_lbl)
        self.at("When a ligand binds its receptor")
        self.play(FadeIn(mem), FadeIn(rec), FadeIn(rec_lbl), FadeIn(lig_g), run_time=0.7)
        self.at("binds")
        self.play(lig.animate.move_to([-4.4, 0.3, 0]), lig_lbl.animate.move_to([-5.45, 0.3, 0]), run_time=0.8)
        sig = arr([-3.25, 0.3, 0], [-1.85, 0.3, 0], GREY)
        self.at("the switch flips on")
        state_on = T("ON", 30, GREEN, weight=BOLD).next_to(sw, UP, buff=0.35)
        self.play(GrowArrow(sig), run_time=0.3)
        self.play(*flip(sw, True, GREEN), sig.animate.set_color(GREEN), ReplacementTransform(state, state_on), run_time=0.5)
        state = state_on

        # --- second messengers fan out ----------------------------------------------------------
        specs = [("cAMP", 1.7), ("IP3", 0.2), ("Ca²⁺", -1.3)]
        chips, arrows = [], []
        for name, y in specs:
            c = bchip(name, TEAL, 28).move_to([4.2, y, 0])
            a = arr([1.0, 0.2, 0], [c.get_left()[0], y, 0], TEAL)
            chips.append(c); arrows.append(a)
        self.at("cyclic AMP")
        self.play(GrowArrow(arrows[0]), FadeIn(chips[0], shift=RIGHT * 0.2), run_time=0.6)
        self.at("IP3")
        self.play(GrowArrow(arrows[1]), FadeIn(chips[1], shift=RIGHT * 0.2), run_time=0.5)
        self.at("calcium")
        self.play(GrowArrow(arrows[2]), FadeIn(chips[2], shift=RIGHT * 0.2), run_time=0.5)
        fan = VGroup()
        for c, (name, y) in zip(chips, specs):
            for dy in (0.55, 0.0, -0.55):
                fan.add(arr([c.get_right()[0], y, 0], [6.1, y + dy, 0], TEAL, w=3, tip=0.16))
        self.at("fan out")
        self.play(LaggedStart(*[GrowArrow(f) for f in fan], lag_ratio=0.08), run_time=0.9)

        # --- switch off: phosphatases and PDE ----------------------------------------------
        self.at("But every switch")
        clear = VGroup(lig_g, mem, rec, rec_lbl, sig, *chips, *arrows, fan)
        self.play(FadeOut(clear), sw.animate.scale(0.77).move_to([0, 1.6, 0]), state.animate.move_to([0, 2.55, 0]), run_time=0.9)
        state_off = T("OFF", 30, RED, weight=BOLD).move_to([0, 2.55, 0])
        self.at("turn off")
        self.play(*flip(sw, False, RED), ReplacementTransform(state, state_off), run_time=0.6)
        state = state_off

        prot = bchip("target protein", PURPLE, 26).move_to([-3.4, -0.45, 0])
        pb = pbadge().move_to(prot.get_corner(UR) + [0.05, 0.05, 0])
        phos = bchip("phosphatase", RED, 26).move_to([-3.4, -2.2, 0])
        lbl_l = T("remove phosphates", 24, GREY).move_to([-3.4, -3.2, 0])
        self.at("through phosphatuses")
        self.play(FadeIn(prot), FadeIn(pb), FadeIn(phos, shift=UP * 0.2), run_time=0.7)
        self.at("remove phosphates")
        self.play(phos.animate.move_to([-3.4, -1.35, 0]), run_time=0.4)
        self.play(pb.animate.shift([1.3, 0.9, 0]).set_opacity(0), *recolor(prot, GREY), FadeIn(lbl_l), run_time=0.8)

        cam = bchip("cAMP", TEAL, 28).move_to([3.4, -0.45, 0])
        pde = bchip("PDE", RED, 26).move_to([3.4, -2.2, 0])
        lbl_r = T("destroy messengers", 24, GREY).move_to([3.4, -3.2, 0])
        self.at("and enzymes")
        self.play(FadeIn(cam), FadeIn(pde, shift=UP * 0.2), run_time=0.6)
        self.at("destroy")
        self.play(pde.animate.move_to([3.4, -1.35, 0]), run_time=0.4)
        self.play(cam.animate.scale(0.2).set_opacity(0), FadeIn(lbl_r), run_time=0.7)

        # --- the pairing ------------------------------------------------------------------
        self.at("Hold on to that pairing")
        self.play(FadeOut(VGroup(prot, pb, phos, lbl_l, cam, pde, lbl_r)), FadeOut(state),
                  sw.animate.scale(1 / 0.77).move_to([0, 0.2, 0]), run_time=0.7)
        l_off = T("OFF", 34, RED, weight=BOLD).move_to([-3.0, 0.2, 0])
        l_on = T("ON", 34, GREEN, weight=BOLD).move_to([3.0, 0.2, 0])
        self.play(FadeIn(l_off), FadeIn(l_on), run_time=0.4)
        self.play(*flip(sw, True, GREEN), run_time=0.45)
        self.play(*flip(sw, False, RED), run_time=0.45)

        # --- four-beat sentence -----------------------------------------------------------
        self.at("Almost every pathway")
        self.play(FadeOut(VGroup(sw, l_off, l_on)), run_time=0.5)
        xs = [-4.575, -1.525, 1.525, 4.575]
        boxes, nums = [], []
        for i, x in enumerate(xs):
            b = RoundedRectangle(corner_radius=0.2, width=2.85, height=3.3, stroke_color=GREY, stroke_width=2.5).move_to([x, -0.1, 0])
            n = T(str(i + 1), 26, GREY).move_to(b.get_corner(UL) + [0.32, -0.32, 0])
            boxes.append(b); nums.append(n)
        self.at("in this chapter")
        self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(n)) for b, n in zip(boxes, nums)], lag_ratio=0.25), run_time=1.6)

        def label(lines, color, x):
            return T(lines, 26, color, line_spacing=0.8).move_to([x, -1.05, 0])

        ic1 = toggle(True, scale=0.7).move_to([xs[0], 0.5, 0])
        lb1 = label("switch\nturns ON", GREEN, xs[0])
        self.at("a switch turns on")
        self.play(FadeIn(ic1), FadeIn(lb1), run_time=0.5)
        ic2 = VGroup(Dot([0, 0, 0], radius=0.09, color=TEAL))
        for ang in np.linspace(-65, 65, 7):
            v = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
            ic2.add(Arrow(v * 0.18, v * 1.0, buff=0, color=TEAL, stroke_width=4, tip_length=0.16))
        ic2.move_to([xs[1], 0.5, 0])
        lb2 = label("signal spreads\nand amplifies", TEAL, xs[1])
        self.at("the signal spreads")
        self.play(FadeIn(ic2), FadeIn(lb2), run_time=0.6)
        ic3 = toggle(False, RED, scale=0.7).move_to([xs[2], 0.5, 0])
        lb3 = label("switch\nturns OFF", RED, xs[2])
        self.at("the switch turns off")
        self.play(FadeIn(ic3), FadeIn(lb3), run_time=0.5)
        ic4 = toggle(True, RED, scale=0.7).move_to([xs[3], 0.5, 0])
        lb4 = label("OFF step fails:\nswitch sticks", RED, xs[3])
        self.at("when the")
        self.play(FadeIn(ic4), FadeIn(lb4), run_time=0.6)
        self.at("the switch sticks")
        self.play(boxes[3].animate.set_stroke(RED, 4), Wiggle(ic4, scale_value=1.1, rotation_angle=0.03 * TAU), run_time=0.9)
        dis = T("disease", 44, RED, weight=BOLD).move_to([xs[3] - 1.0, -2.55, 0])
        dis.move_to([0, -2.6, 0])
        self.at("disease")
        self.play(FadeIn(dis, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Five(SpokenScene):
    """the five-part pipeline across the membrane, plus the sixth: active termination."""

    def construct(self):
        head = T("The same logic in every pathway", 34, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.play(Write(head), run_time=1.4)
        mem = membrane_h(0.55)
        out_lbl = T("outside the cell", 24, GREY).move_to([4.7, 1.3, 0])
        in_lbl = T("inside the cell", 24, GREY).move_to([4.7, -0.2, 0])
        c1 = bchip("primary messenger", YELLOW).move_to([-4.0, 2.1, 0])
        c2 = bchip("receptor", BLUE).move_to([-4.0, 0.55, 0])
        c3 = bchip("second messenger", TEAL).move_to([-4.0, -1.3, 0])
        c4 = bchip("effector molecules", PURPLE).move_to([0.2, -1.3, 0])
        c5 = bchip("response", ORANGE).move_to([4.1, -1.3, 0])
        a12 = arr(c1.get_bottom(), c2.get_top(), YELLOW)
        a23 = arr(c2.get_bottom(), c3.get_top(), BLUE)
        a34 = arr(c3.get_right(), c4.get_left(), TEAL)
        a45 = arr(c4.get_right(), c5.get_left(), PURPLE)
        sub = T("hormone or neurotransmitter", 24, GREY).next_to(c1, RIGHT, buff=0.3)

        self.at("shares the same molecular logic")
        self.play(Create(mem), FadeIn(out_lbl), FadeIn(in_lbl), run_time=0.8)
        self.at("A primary messenger")
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.6)
        self.at("a hormone or neurotransmitter")
        self.play(FadeIn(sub), run_time=0.5)
        self.at("is detected by")
        self.play(GrowArrow(a12), FadeIn(c2), run_time=0.7)
        self.at("The receptor generates")
        self.play(GrowArrow(a23), run_time=0.5)
        self.at("second messenger")
        self.play(FadeIn(c3, shift=DOWN * 0.2), run_time=0.5)
        self.at("which drives effector")
        self.play(GrowArrow(a34), FadeIn(c4), run_time=0.6)
        self.at("which produce the")
        self.play(GrowArrow(a45), FadeIn(c5), run_time=0.6)

        # signal flows through the chain once
        path = [c1.get_center(), c2.get_center(), c3.get_center(), c4.get_center(), c5.get_center()]
        pd = Dot(path[0], radius=0.14, color=TEXT)
        self.at("response", nth=0)
        self.play(FadeIn(pd), run_time=0.15)
        for p in path[1:]:
            self.play(pd.animate.move_to(p), run_time=0.28, rate_func=linear)
        self.play(FadeOut(pd), run_time=0.15)

        chain = [c1, c2, c3, c4, c5]
        badges = VGroup()
        for i, c in enumerate(chain):
            b = Circle(radius=0.23, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
            n = T(str(i + 1), 24, BG, weight=BOLD).move_to(b)
            g = VGroup(b, n).move_to(c.get_corner(UL) + [-0.05, 0.2, 0])
            badges.add(g)
        self.at("Five parts in order")
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in badges], lag_ratio=0.2), run_time=1.3)

        term_pos = np.array([0.2, -3.0, 0])
        ghost = chip("active termination", RED, size=26)
        ghost.move_to(term_pos)
        ghost_d = DashedVMobject(ghost[0].copy().set_fill(opacity=0), num_dashes=36).set_color(RED)
        q = T("?", 30, RED).move_to(term_pos)
        self.at("plus one that")
        self.play(Create(ghost_d), FadeIn(q), run_time=0.7)
        term = bchip("active termination", RED, 26).move_to(term_pos)
        self.at("Active")
        self.play(FadeOut(ghost_d), ReplacementTransform(q, term), run_time=0.6)
        bars = VGroup(*[inhib([term_pos[0] + dx, term_pos[1] + 0.4, 0], [c.get_center()[0], c.get_bottom()[1], 0]) for dx, c in
                        zip((-0.7, 0.7), (c3, c4))])
        self.at("The pathway has to be switched")
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.2),
                  *[a for m in (c1, c2, c3, c4, c5) for a in dim(m, 0.5)],
                  *[m.animate.set_opacity(0.5) for m in (a12, a23, a34, a45, sub)], run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03First(SpokenScene):
    """first messengers; small lipophilic slip through, large/polar need a membrane receptor."""

    def construct(self):
        q = T("What is doing the signaling?", 40, font=TITLE_FONT).move_to([0, 0.3, 0])
        self.at("Before the receptor")
        self.play(Write(q), run_time=1.4)
        label = T("first messengers", 30, YELLOW, weight=BOLD).move_to([-1.9, 3.25, 0])
        names = ["hormones", "neurotransmitters", "growth factors", "light"]
        row = VGroup(*[chip(n, YELLOW, 28) for n in names]).arrange(RIGHT, buff=0.3).move_to([0, 2.2, 0])
        self.at("First messengers are")
        self.play(FadeOut(q), FadeIn(label, shift=DOWN * 0.15), run_time=0.6)
        self.at("the extracellular signals")
        sub = T("the extracellular signals", 26, GREY)
        sub.next_to(label, RIGHT, buff=0.25)
        self.play(FadeIn(sub), run_time=0.5)
        self.at("hormones")
        self.play(FadeIn(row[0], shift=DOWN * 0.15), run_time=0.4)
        self.at("neurotransmitters")
        self.play(FadeIn(row[1], shift=DOWN * 0.15), run_time=0.4)
        self.at("growth factors")
        self.play(FadeIn(row[2], shift=DOWN * 0.15), run_time=0.4)
        self.at("even light")
        self.play(FadeIn(row[3], shift=DOWN * 0.15), run_time=0.4)

        YM = 0.0
        mem = membrane_h(YM)
        self.at("The key split")
        self.play(Create(mem), FadeOut(VGroup(label, sub, row)), run_time=1.0)
        out_lbl = T("outside", 26, GREY).move_to([-5.6, YM + 0.5, 0])
        in_lbl = T("inside", 26, GREY).move_to([-5.7, YM - 0.5, 0])
        self.play(FadeIn(out_lbl), FadeIn(in_lbl), run_time=0.4)

        XL, XR = -3.0, 3.6
        h_l = T("small, lipophilic", 30, TEXT).move_to([XL, 2.65, 0])
        st = Circle(radius=0.24, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
        st_lbl = T("steroid", 28, YELLOW).next_to(st, RIGHT, buff=0.2)
        stg = VGroup(st, st_lbl).move_to([XL, 1.6, 0])
        self.at("Small lipophilic")
        self.play(FadeIn(h_l, shift=DOWN * 0.1), run_time=0.5)
        self.at("steroids")
        self.play(FadeIn(stg), run_time=0.5)
        self.at("slip straight through")
        self.play(stg.animate.shift(DOWN * 2.8), run_time=1.3)
        rec_in = bchip("receptor", BLUE, 28).move_to([XL, -2.2, 0])
        self.at("receptors inside")
        self.play(FadeIn(rec_in, shift=UP * 0.15), run_time=0.5)
        self.play(stg.animate.shift(DOWN * 0.3), run_time=0.5)
        self.play(pulse(rec_in, BLUE, 1.06), run_time=0.6)

        h_r = T("large or polar", 30, TEXT).move_to([XR, 2.65, 0])
        pep = bchip("peptide hormone", YELLOW, 28).move_to([XR, 1.6, 0])
        self.at("Large or polar")
        self.play(FadeIn(h_r, shift=DOWN * 0.1), FadeIn(pep), run_time=0.6)
        self.at("cannot cross")
        self.play(pep.animate.move_to([XR, YM + 0.58, 0]), run_time=0.7)
        x1 = Line([XR + 1.85, YM + 0.3, 0], [XR + 2.35, YM - 0.2, 0], color=RED, stroke_width=8)
        x2 = Line([XR + 1.85, YM - 0.2, 0], [XR + 2.35, YM + 0.3, 0], color=RED, stroke_width=8)
        cross = VGroup(x1, x2)
        self.play(Create(cross), run_time=0.4)
        rec_m = RoundedRectangle(corner_radius=0.2, width=0.8, height=1.5, stroke_color=BLUE, stroke_width=4,
                                 fill_color=BLUE, fill_opacity=0.3).move_to([XR, YM, 0])
        rec_back = RoundedRectangle(corner_radius=0.2, width=0.8, height=1.5, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(rec_m)
        rec_m_lbl = btext("receptor", 28, BLUE).move_to([XR + 1.5, YM - 0.5, 0])
        self.at("so they must be read")
        self.play(FadeOut(cross), pep.animate.move_to([XR, YM + 1.18, 0]), run_time=0.5)
        self.play(FadeIn(VGroup(rec_back, rec_m)), FadeIn(rec_m_lbl), run_time=0.6)
        self.at("relays the news inward")
        relay = arr([XR, YM - 0.78, 0], [XR, YM - 1.5, 0], TEAL)
        sm = bchip("second messenger", TEAL, 28).move_to([XR, -2.2, 0])
        self.play(GrowArrow(relay), run_time=0.5)
        self.play(FadeIn(sm, shift=DOWN * 0.15), run_time=0.5)
        cap = T("Size and polarity decide where the receptor lives", 32, TEXT).move_to([0, -3.3, 0])
        self.at("Size and polarity decide")
        self.play(Write(cap), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Epi(SpokenScene):
    """glucagon + epinephrine launch a cascade with three simultaneous fronts; the signal is amplified."""

    def construct(self):
        glu = bchip("glucagon", YELLOW, 28).move_to([-3.8, 2.5, 0])
        epi = bchip("epinephrine", YELLOW, 28).move_to([3.8, 2.5, 0])
        self.at("Glucagon")
        self.play(FadeIn(glu, shift=DOWN * 0.15), run_time=0.5)
        self.at("and epinephrine")
        self.play(FadeIn(epi, shift=DOWN * 0.15), run_time=0.5)
        cap = T("first messengers for fuel mobilization", 30, YELLOW).move_to([0, 3.3, 0])
        self.at("classic first messengers")
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=1.0)
        t_l = T("blood glucose drops", 24, GREY).move_to([-4.2, 1.75, 0])
        t_r = T("fight-or-flight response", 24, GREY).move_to([4.3, 1.75, 0])
        self.at("When blood glucose drops")
        self.play(FadeIn(t_l, shift=DOWN * 0.1), pulse(glu, YELLOW, 1.08), run_time=0.8)
        self.at("or the fight or flight")
        self.play(FadeIn(t_r, shift=DOWN * 0.1), pulse(epi, YELLOW, 1.08), run_time=0.8)

        cell = RoundedRectangle(corner_radius=0.25, width=12.2, height=3.95, stroke_color=GREY, stroke_width=4).move_to([0, -0.875, 0])
        # two hormones, two different receptors (glucagon receptor, beta-adrenergic receptor), one shared cascade
        rec_g = bchip("receptor", BLUE, 26).move_to([-1.25, 1.1, 0])
        rec_e = bchip("receptor", BLUE, 26).move_to([1.25, 1.1, 0])
        ah1 = arr([-2.75, 2.25, 0], [-1.55, 1.45, 0], YELLOW)
        ah2 = arr([2.75, 2.25, 0], [1.55, 1.45, 0], YELLOW)
        self.at("these hormones launch")
        self.play(Create(cell), run_time=0.7)
        self.play(FadeIn(rec_g), FadeIn(rec_e), GrowArrow(ah1), GrowArrow(ah2), run_time=0.7)
        relay = VGroup(RoundedRectangle(corner_radius=0.14, width=3.6, height=0.7, stroke_width=0, fill_color=BG, fill_opacity=1),
                       DashedVMobject(RoundedRectangle(corner_radius=0.14, width=3.6, height=0.7), num_dashes=40).set_color(GREY),
                       T("signaling cascade", 26, TEXT)).move_to([0, 0.3, 0])
        relay.set_z_index(2)
        self.at("signaling cascade")
        self.play(FadeIn(relay, shift=DOWN * 0.1), run_time=0.7)

        xs = [-4.0, 0.0, 4.0]
        tops = [bchip("glycogen", GREY), bchip("glucose", ORANGE), bchip("stored fat", GREY)]
        bots = [bchip("glucose", ORANGE), bchip("glycogen", GREY), bchip("fatty acids", ORANGE)]
        for x, t, b in zip(xs, tops, bots):
            t.move_to([x, -0.95, 0]); b.move_to([x, -2.15, 0])
            t.set_z_index(2); b.set_z_index(2)
        fan = [arr([x * 0.3, 0.0, 0], [x, -0.55, 0], BLUE, w=4, tip=0.2) for x in xs]
        self.at("on several fronts")
        self.play(*[GrowArrow(a) for a in fan], *[FadeIn(t) for t in tops], run_time=0.9)

        arrows = [arr([xs[0], -1.35, 0], [xs[0], -1.8, 0], GREEN), arr([xs[1], -1.35, 0], [xs[1], -1.8, 0], GREY),
                  arr([xs[2], -1.35, 0], [xs[2], -1.8, 0], GREEN)]
        self.at("It breaks down glycogen")
        self.play(GrowArrow(arrows[0]), FadeIn(bots[0], shift=DOWN * 0.15), run_time=0.8)
        self.at("shuts off glycogen synthesis")
        cx1 = Line([xs[1] - 0.25, -1.4, 0], [xs[1] + 0.25, -1.75, 0], color=RED, stroke_width=7)
        cx2 = Line([xs[1] - 0.25, -1.75, 0], [xs[1] + 0.25, -1.4, 0], color=RED, stroke_width=7)
        self.play(GrowArrow(arrows[1]), FadeIn(bots[1], shift=DOWN * 0.15), run_time=0.5)
        self.play(Create(cx1), Create(cx2), run_time=0.4)
        self.at("frees stored fat")
        self.play(GrowArrow(arrows[2]), FadeIn(bots[2], shift=DOWN * 0.15), run_time=0.8)

        # one hormone arrives at the surface
        self.at("One hormone")
        hd = Dot(epi.get_center(), radius=0.14, color=YELLOW)
        self.play(FadeIn(hd), run_time=0.15)
        self.play(hd.animate.move_to(rec_e.get_top() + UP * 0.12), run_time=0.7, rate_func=smooth)
        self.at("surface")
        self.play(FadeOut(hd), pulse(rec_e, BLUE, 1.1), run_time=0.5)
        self.at("reorganizes the cell's entire")
        self.play(cell.animate.set_stroke(TEXT, 7), run_time=0.6)
        self.play(cell.animate.set_stroke(GREY, 4), run_time=0.8)

        # amplification: one arrival -> many relay signals -> a flood of fuel on every front
        self.at("because the signal")
        sd = Dot(rec_e.get_bottom(), radius=0.12, color=BLUE)
        self.play(FadeIn(sd, scale=0.5), run_time=0.2)
        self.play(sd.animate.move_to(relay.get_center()), Indicate(relay[1:], color=BLUE, scale_factor=1.06), run_time=0.6)
        self.remove(sd)
        rng = np.random.RandomState(3)
        relay_dots, moves = VGroup(), []
        for k in range(4):
            for x, t in zip(xs, tops):
                d = Dot(relay.get_center(), radius=0.08, color=BLUE)
                relay_dots.add(d)
                moves.append(Succession(d.animate(run_time=0.55).move_to(t.get_top() + DOWN * 0.05),
                                        FadeOut(d, run_time=0.1)))
        self.add(relay_dots)
        self.bring_to_front(*tops)
        self.at("amplified")
        self.play(LaggedStart(*moves, lag_ratio=0.08), run_time=1.3)
        fuel, flows = VGroup(), []
        for b in (bots[0], bots[2]):
            hw = b.width / 2
            for k in range(12):
                side = 1 if k % 2 else -1
                d = Dot(b.get_center(), radius=0.075, color=ORANGE)
                tgt = b.get_center() + np.array([side * (hw + rng.uniform(0.25, 1.0)), rng.uniform(-0.35, 0.35), 0])
                fuel.add(d)
                flows.append(Succession(d.animate(run_time=0.7).move_to(tgt), FadeOut(d, run_time=0.35)))
        self.add(fuel)
        self.bring_to_front(*bots)
        self.at("coordinated")
        self.play(LaggedStart(*flows, lag_ratio=0.04),
                  *[pulse(b, c, 1.1) for b, c in zip(bots, (ORANGE, GREY, ORANGE))], run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Camp(SpokenScene):
    """cAMP -> PKA -> synthase OFF, phosphorylase kinase -> phosphorylase ON; the cell's master switch flips."""

    def construct(self):
        camp = bchip("cAMP", TEAL, 30).move_to([-2.3, 2.7, 0])
        gauge_o = Rectangle(width=0.4, height=1.1, stroke_color=TEAL, stroke_width=3).move_to([-4.3, 2.7, 0])
        gauge_f = Rectangle(width=0.4, height=0.2, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).align_to(gauge_o, DOWN)
        gauge_f.align_to(gauge_o, DOWN).align_to(gauge_o, LEFT)
        gauge_lbl = T("level", 24, GREY).next_to(gauge_o, LEFT, buff=0.2)
        self.at("When cyclic AMP")
        self.play(FadeIn(camp), Create(gauge_o), FadeIn(gauge_f), FadeIn(gauge_lbl), run_time=0.7)
        self.at("rises")
        new = Rectangle(width=0.4, height=0.95, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).align_to(gauge_o, DOWN).align_to(gauge_o, LEFT)
        self.play(Transform(gauge_f, new), run_time=1.1)

        cap = T("master switch", 28, TEXT).move_to([4.7, 2.7, 0])
        sw = toggle(False, scale=0.8).move_to([4.7, 1.6, 0])
        st_lbl = T("storing fuel", 26, GREY).move_to([4.7, 0.65, 0])
        self.at("a master switch")
        self.play(FadeIn(cap), FadeIn(sw), FadeIn(st_lbl), run_time=0.7)

        pka = bchip("protein kinase A", PURPLE, 26).move_to([-2.3, 1.2, 0])
        a_pka = arr(camp.get_bottom(), pka.get_top(), TEAL)
        self.at("protein kinase A")
        self.play(GrowArrow(a_pka), FadeIn(pka), run_time=0.7)
        self.at("hits several targets")
        self.play(pulse(pka, PURPLE, 1.08), run_time=0.7)

        syn = bchip("glycogen synthase", PURPLE, 26).move_to([-4.85, -0.6, 0])
        pk = bchip("phosphorylase kinase", PURPLE, 26).move_to([-0.3, -0.6, 0])
        gp = bchip("glycogen phosphorylase", PURPLE, 26).move_to([-0.3, -2.2, 0])
        i_syn = inhib(pka.get_bottom() + [-0.5, 0, 0], syn.get_top(), RED)
        a_pk = arr(pka.get_bottom() + [0.5, 0, 0], pk.get_top(), GREEN)
        a_gp = arr(pk.get_bottom(), gp.get_top(), GREEN)
        r_syn = T("synthesis OFF", 28, RED).move_to([-4.85, -1.55, 0])
        r_gp = T("breakdown ON", 28, GREEN).move_to([-0.3, -3.15, 0])

        self.at("it shuts down glycogen synthesis")
        self.play(Create(i_syn), FadeIn(syn), run_time=0.8)
        self.at("inhibiting glycogen synthase")
        self.play(*recolor(syn, RED), FadeIn(r_syn), run_time=0.7)
        self.at("and it turns on glycogen breakdown")
        self.play(pulse(pka, GREEN, 1.05), run_time=0.6)
        self.at("activating phosphorylase kinase")
        self.play(GrowArrow(a_pk), FadeIn(pk), run_time=0.7)
        self.at("which activates glycogen phosphorylase")
        self.play(GrowArrow(a_gp), FadeIn(gp), run_time=0.6)
        self.play(*recolor(gp, GREEN), FadeIn(r_gp), run_time=0.6)

        self.at("One second messenger")
        self.play(pulse(camp, TEAL, 1.15), run_time=0.8)
        self.at("one kinase")
        self.play(pulse(pka, PURPLE, 1.12), run_time=0.8)
        on_lbl = T("releasing fuel", 26, GREEN).move_to([4.7, 0.65, 0])
        self.at("flips the cell")
        self.play(*flip(sw, True, GREEN), ReplacementTransform(st_lbl, on_lbl), run_time=0.7)

        # phosphates land on the right enzymes
        ps = [pbadge().move_to(pka.get_center()) for _ in range(3)]
        dests = [syn.get_corner(UR) + [0.1, 0.12, 0], pk.get_corner(UR) + [0.1, 0.12, 0], gp.get_corner(UR) + [0.1, 0.12, 0]]
        srcs = [pka.get_center(), pka.get_center(), pk.get_center()]
        for p, s in zip(ps, srcs):
            p.move_to(s)
        self.at("all by adding phosphates")
        self.play(*[FadeIn(p, scale=0.5) for p in ps], run_time=0.3)
        self.play(*[p.animate.move_to(d) for p, d in zip(ps, dests)], run_time=1.0)
        self.finish()


class S06End(EndCard):
    LINE = "Every switch that turns on must turn off."
