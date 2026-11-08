"""Spinal circuits that gate pain: a gate can fail two ways (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = excitatory: skin input, excitatory arrows, "output" of a working path
  RED    = inhibitory neuron, inhibitory (T-bar) arrows, removal / failure marks
  BLUE   = the lamina I target neuron and its membrane
  YELLOW = the quantity under attention: anion reversal potential, driving force, "allodynia"
  PURPLE = microglia and BDNF (modulatory, dashed arrows)
  ORANGE = ATP
  GREY   = dorsal horn outline, laminae, labels, preparation tags, de-emphasised things
  Arrow types: filled head = excitatory, T-bar = inhibitory, dashed = modulatory.
  Schematic only: the dorsal horn is flat bands and boxes. Nothing here is a recording.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dim(c, o=0.3):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def undim(c):
    return [c[1].animate.set_stroke(opacity=1).set_fill(opacity=0.16), c[2].animate.set_opacity(1)]


def exc(a, b, color=GREEN, w=6):
    return Arrow(np.array(a, float), np.array(b, float), buff=0.0, color=color, stroke_width=w, tip_length=0.26,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def inh(a, b, color=RED, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 2))


def mod(a, b, color=PURPLE, w=5):
    return DashedLine(np.array(a, float), np.array(b, float), color=color, stroke_width=w, dash_length=0.18).add_tip(
        tip_length=0.24)


def prep_tag(text):
    return T(text, 26, GREY).to_corner(UL, buff=0.45).shift(RIGHT * 0.1)


def cross(center, s=0.4, color=RED, w=8):
    c = np.array(list(center)[:2] + [0], float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


# geometry of the flat dorsal horn schematic
PX0, PX1, PY0, PY1 = -6.2, 6.2, -3.3, 2.3     # panel
LY = 0.8                                       # boundary between lamina I and the deeper dorsal horn
TX, TY = -0.8, 1.55                            # lamina I neuron
IX, IY = -0.8, -1.2                            # inhibitory neuron


def panel():
    """Dorsal horn as a flat schematic: an outline with lamina I as a band and the rest of the horn below."""
    outline = RoundedRectangle(corner_radius=0.2, width=PX1 - PX0, height=PY1 - PY0, stroke_color=GREY,
                               stroke_width=3, fill_opacity=0).move_to([(PX0 + PX1) / 2, (PY0 + PY1) / 2, 0])
    band = Rectangle(width=PX1 - PX0 - 0.1, height=LY - (PY1 - 0.05) if False else (PY1 - 0.05) - LY,
                     stroke_width=0, fill_color=BLUE, fill_opacity=0.10)
    band.move_to([(PX0 + PX1) / 2, (LY + PY1 - 0.05) / 2, 0])
    divider = DashedLine([PX0, LY, 0], [PX1, LY, 0], color=GREY, stroke_width=2, dash_length=0.15)
    l1 = T("Lamina I", 24, GREY).move_to([PX0 + 1.1, (LY + PY1) / 2 + 0.05, 0])
    l2 = T("Deeper dorsal horn", 22, GREY).move_to([PX0 + 1.75, LY - 0.4, 0])
    return VGroup(outline)


def target_node(label="Target neuron"):
    return bchip(label, BLUE, 28).move_to([TX, TY, 0])


def inhib_node(label="Inhibitory neuron"):
    return bchip(label, RED, 26).move_to([IX, IY, 0])


def legend():
    a = exc([3.1, -2.45, 0], [3.9, -2.45, 0], w=5)
    ta = T("excitatory", 22, GREEN).next_to(a, RIGHT, buff=0.15)
    b = inh([3.1, -3.0, 0], [3.9, -3.0, 0], w=5)
    tb = T("inhibitory", 22, RED).next_to(b, RIGHT, buff=0.15)
    return VGroup(a, ta, b, tb)


def voltage_ladder(cx, ytop=2.6, ybot=-2.9, e_y=-1.3, vm_y=0.3, width=1.2):
    """A bare voltage axis: membrane potential (blue) and anion reversal potential (yellow). No numbers: in this sketch."""
    axx = cx - width / 2 - 0.5
    ax = Arrow([axx, ybot, 0], [axx, ytop, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
    up = T("more positive", 22, GREY).rotate(PI / 2).next_to(ax, LEFT, buff=0.12)
    vm = Line([cx - width / 2, vm_y, 0], [cx + width / 2, vm_y, 0], color=BLUE, stroke_width=7)
    vm_l = T("membrane potential", 22, BLUE).move_to([cx + width / 2 + 0.2, vm_y, 0], aligned_edge=LEFT)
    ev = Line([cx - width / 2, e_y, 0], [cx + width / 2, e_y, 0], color=YELLOW, stroke_width=7)
    ev_l = T("anion reversal potential", 22, YELLOW).move_to([cx + width / 2 + 0.2, e_y, 0], aligned_edge=LEFT)
    return VGroup(ax, up), vm, vm_l, ev, ev_l


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Spinal circuits that gate pain"
    TITLE = "Gatekeeper gone, or sign flipped"


# ---------------------------------------------------------------------------------------------
class S01Gate(SpokenScene):
    def construct(self):
        pn = panel()
        self.at("spinal gate for pain")
        self.play(FadeIn(pn), run_time=0.8)
        tgt = target_node()
        skin = bchip("Skin input", GREEN, 28).move_to([TX, 3.15, 0])
        a_in = exc([TX, 3.15 - 0.45, 0], [TX, TY + 0.45, 0])
        outc = exc([TX + 1.55, TY, 0], [PX1 - 0.15, TY, 0])
        outl = T("output", 22, GREEN).next_to(outc, UP, buff=0.08)
        self.at("1965" if False else "Melzack and Wall")
        self.play(FadeIn(skin), run_time=0.4)
        self.play(GrowArrow(a_in), FadeIn(tgt), run_time=0.6)
        self.play(GrowArrow(outc), FadeIn(outl), run_time=0.5)
        ih = inhib_node()
        ib = inh([IX, IY + 0.45, 0], [TX, TY - 0.45, 0])
        lg = legend()
        self.at("between skin input")
        self.play(FadeIn(ih, shift=UP * 0.2), run_time=0.5)
        self.play(Create(ib), FadeIn(lg), run_time=0.5)
        self.at("Gates fail")
        self.play(Indicate(ih, color=RED, scale_factor=1.08), run_time=0.8)
        # failure one: the gatekeeper is gone
        self.at("The gatekeeper can be gone")
        gone = cross([IX, IY], 0.5)
        lbl1 = T("gone", 26, RED).next_to(ih, RIGHT, buff=0.5)
        self.play(*dim(ih), FadeOut(ib), Create(gone), FadeIn(lbl1), run_time=0.7)
        # reset, then failure two: still there, sign flipped
        self.at("Or it can still be there")
        ib2 = exc([IX, IY + 0.45, 0], [TX, TY - 0.45, 0], color=GREEN)
        lbl2 = T("still there, sign changed", 24, YELLOW).next_to(ih, RIGHT, buff=0.5)
        self.play(FadeOut(gone), FadeOut(lbl1), *undim(ih), FadeIn(ib2), FadeIn(lbl2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Gone(SpokenScene):
    def construct(self):
        pn = panel()
        tag = prep_tag("in male mice")
        tgt = target_node()
        skin = bchip("Skin input", GREEN, 28).move_to([TX, 3.15, 0])
        a_in = exc([TX, 3.15 - 0.45, 0], [TX, TY + 0.45, 0])
        outc = exc([TX + 1.55, TY, 0], [PX1 - 0.15, TY, 0], w=6)
        outl = T("output", 22, GREEN).next_to(outc, UP, buff=0.08)
        ih = inhib_node()
        ib = inh([IX, IY + 0.45, 0], [TX, TY - 0.45, 0])
        lg = legend()
        self.play(FadeIn(pn), FadeIn(skin), FadeIn(a_in), FadeIn(tgt), FadeIn(outc), FadeIn(outl), FadeIn(ih), FadeIn(ib),
                  FadeIn(lg), FadeIn(tag), run_time=0.8)
        self.at("In male mice")
        self.play(Indicate(ih, color=RED, scale_factor=1.08), run_time=0.8)
        # ablation, generically
        ih_pv = inhib_node("Parvalbumin neurons")
        self.at("a blading spinal parvalbumin")
        self.play(Transform(ih, ih_pv), run_time=0.5)
        self.play(*dim(ih), FadeOut(ib), Create(cross([IX, IY], 0.5)), run_time=0.7)
        gone_x = self.mobjects[-1]
        allo = bchip("mechanical allodynia", YELLOW, 26).move_to([3.4, 3.15, 0])
        self.at("mechanical allodynia")
        self.play(FadeIn(allo, shift=DOWN * 0.15), run_time=0.5)
        self.at("pain from touch")
        self.wait(0.2)
        outc_big = exc([TX + 1.55, TY, 0], [PX1 - 0.15, TY, 0], w=14)
        self.at("Excitation then runs unopposed")
        self.play(Transform(outc, outc_big), run_time=0.6)
        # silencing: neuron is back, only its release stops
        outc_n = exc([TX + 1.55, TY, 0], [PX1 - 0.15, TY, 0], w=6)
        ib_cut = DashedLine([IX, IY + 0.45, 0], [TX, TY - 0.45, 0], color=GREY, stroke_width=4, dash_length=0.12)
        ih_gen = inhib_node("Inhibitory neuron")
        self.at("Silencing transmitter release")
        self.play(FadeOut(gone_x), FadeOut(allo), Transform(outc, outc_n), FadeOut(ih), FadeIn(ih_gen), run_time=0.7)
        ih = ih_gen
        self.at("The neuron survives")
        self.play(Indicate(ih, color=RED, scale_factor=1.08), run_time=0.7)
        nr = T("transmitter release blocked", 24, GREY).next_to(ih, RIGHT, buff=0.5)
        self.at("but it stops")
        self.play(FadeIn(ib_cut), FadeIn(nr), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Counts(SpokenScene):
    def construct(self):
        tag = prep_tag("in male mice")
        self.play(FadeIn(tag), run_time=0.3)
        # timeline
        ax = Arrow([-6.0, 1.45, 0], [6.0, 1.45, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        axl = T("weeks after spared nerve injury", 24, GREY).move_to([0, 0.95, 0])
        wk = {3: -4.2, 5: -1.0, 8: 3.8}
        ticks, tlab, glyphs = [], [], []
        for w, x in wk.items():
            ticks.append(Line([x, 1.33, 0], [x, 1.57, 0], color=GREY, stroke_width=4))
            tlab.append(T(f"{w}", 26, GREY).move_to([x, 1.05, 0]))
            glyphs.append(bchip("PV neurons", RED, 24).move_to([x, 2.35, 0]))
        axl.move_to([0, 0.55, 0])
        self.at("count the cells")
        self.play(Create(ax), FadeIn(axl), *[FadeIn(t) for t in ticks + tlab], run_time=0.6)
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.15) for g in glyphs], lag_ratio=0.6), run_time=1.2)
        self.at("spared nerve injury")
        nf = T("counts did not fall significantly", 26, GREEN).move_to([0, 3.2, 0])
        self.at("did not fall significantly")
        self.play(FadeIn(nf), run_time=0.4)
        # mini gate
        px, tx_ = -3.0, 0.4
        base_y = -1.6
        pv = bchip("PV neurons", RED, 26).move_to([px, base_y, 0])
        tg = bchip("Target neuron", BLUE, 26).move_to([tx_, base_y, 0])
        b_ = inh([px + 1.25, base_y, 0], [tx_ - 1.5, base_y, 0])
        o_ = exc([tx_ + 1.5, base_y, 0], [5.2, base_y, 0], w=6)
        ol = T("output", 22, GREEN).next_to(o_, UP, buff=0.08)
        self.at("Yet ablating those neurons")
        self.play(FadeOut(nf), FadeIn(pv), FadeIn(tg), Create(b_), GrowArrow(o_), FadeIn(ol), run_time=0.7)
        x1 = cross([px, base_y], 0.45)
        o_big = exc([tx_ + 1.5, base_y, 0], [5.2, base_y, 0], w=14)
        allo = T("allodynia", 26, YELLOW).move_to([3.6, base_y - 0.75, 0])
        self.at("produced allodynia")
        self.play(*dim(pv), FadeOut(b_), Create(x1), Transform(o_, o_big), FadeIn(allo), run_time=0.7)
        # reset to a neutral state before the next case
        o_n = exc([tx_ + 1.5, base_y, 0], [5.2, base_y, 0], w=6)
        rel = T("hypersensitivity relieved", 26, GREEN).move_to([3.0, base_y - 0.75, 0])
        self.at("activating them relieved")
        self.play(FadeOut(x1), FadeOut(allo), *undim(pv), FadeIn(b_), Transform(o_, o_n), run_time=0.5)
        self.play(Indicate(pv, color=GREEN, scale_factor=1.1), FadeIn(rel), run_time=0.7)
        o_big2 = exc([tx_ + 1.5, base_y, 0], [5.2, base_y, 0], w=14)
        pres = T("present, and the gate is open", 26, YELLOW).move_to([0.8, base_y - 0.75, 0])
        self.at("The gatekeepers were present")
        self.play(FadeOut(rel), run_time=0.3)
        self.play(*[Indicate(g, color=RED, scale_factor=1.08) for g in glyphs], run_time=0.8)
        self.at("the gate was open")
        self.play(Transform(o_, o_big2), FadeIn(pres), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mem_cell(cx, cy):
    """a lamina I neuron as a labelled membrane bar with a channel chip."""
    mem = RoundedRectangle(corner_radius=0.12, width=5.2, height=0.42, stroke_color=BLUE, stroke_width=3,
                           fill_color=BLUE, fill_opacity=0.35).move_to([cx, cy, 0])
    return mem


class S04Sign(SpokenScene):
    def construct(self):
        tag = prep_tag("in adult male rats")
        self.play(FadeIn(tag), run_time=0.3)
        cx = -3.9
        mem = mem_cell(cx, 0.4)
        out_l = T("outside", 24, GREY).move_to([cx - 1.9, 1.3, 0])
        in_l = T("inside: lamina I neuron", 24, BLUE).move_to([cx, -0.7, 0])
        kc = bchip("KCC2", BLUE, 26).move_to([cx, 0.4, 0])
        lowl = T("KCC2 lowered", 26, RED).move_to([cx, -1.55, 0])
        cl_low = T("normally keeps chloride low inside", 24, GREEN).move_to([cx, -2.4, 0])
        cellg = VGroup(mem, out_l, in_l, kc, lowl, cl_low)
        cellg.shift(RIGHT * 3.9)
        lowl.set_opacity(0)
        cl_low.set_opacity(0)
        lad, vm, vm_l, ev, ev_l = voltage_ladder(1.9)
        sk = T("in this sketch", 22, GREY).move_to([2.2, 3.15, 0])
        self.at("Another route")
        self.play(FadeIn(mem), FadeIn(out_l), FadeIn(in_l), FadeIn(kc), run_time=0.7)
        self.at("nerve injury lowered")
        self.play(*dim(kc), lowl.animate.set_opacity(1), run_time=0.6)
        self.at("keeps chloride low")
        self.play(cl_low.animate.set_opacity(1), run_time=0.4)
        pushd = Arrow([1.7, 0.25, 0], [1.7, -1.15, 0], buff=0, color=RED, stroke_width=8, tip_length=0.28)
        pd_l = T("inhibitory", 24, RED).move_to([2.3, -0.45, 0], aligned_edge=LEFT)
        self.at("acute slices")
        self.play(cellg.animate.shift(LEFT * 3.9), run_time=0.8)
        self.play(FadeIn(lad), FadeIn(vm), FadeIn(vm_l), FadeIn(ev), FadeIn(ev_l), FadeIn(sk), run_time=0.7)
        self.play(GrowArrow(pushd), FadeIn(pd_l), run_time=0.4)
        pushu = Arrow([1.7, 0.35, 0], [1.7, 1.55, 0], buff=0, color=GREEN, stroke_width=8, tip_length=0.28)
        pu_l = T("now depolarizing", 24, GREEN).move_to([2.3, 0.95, 0], aligned_edge=LEFT)
        self.at("shifted anion gradient")
        self.play(ev.animate.shift(UP * 2.9), ev_l.animate.shift(UP * 2.9), FadeOut(pushd), FadeOut(pd_l), run_time=1.0)
        self.play(GrowArrow(pushu), FadeIn(pu_l), run_time=0.4)
        self.at("When reversal moves")
        self.play(Indicate(vm, color=BLUE), Indicate(ev, color=YELLOW), run_time=0.9)
        self.at("positive of the membrane")
        self.play(Indicate(ev_l, color=YELLOW), run_time=0.7)
        self.at("the sign flips")
        self.play(Indicate(pushu, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Source(SpokenScene):
    def construct(self):
        tag = prep_tag("in rats")
        self.play(FadeIn(tag), run_time=0.3)
        mg = Circle(radius=0.75, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to([-4.7, 0.8, 0])
        mgl = T("microglia", 26, PURPLE).next_to(mg, LEFT, buff=0.0).move_to([-4.7, -0.3, 0])
        neuron = bchip("Lamina I neuron", BLUE, 26).move_to([-3.0, -1.9, 0])
        atp = bchip("ATP", ORANGE, 26).move_to([-4.7, 2.5, 0])
        atp_ar = exc([-4.7, 2.1, 0], [-4.7, 1.6, 0], color=ORANGE, w=5)
        self.at("Where did the signal come from")
        self.play(FadeIn(mg), FadeIn(mgl), FadeIn(neuron), run_time=0.6)
        self.at("stimulated microglia")
        self.play(FadeIn(atp), GrowArrow(atp_ar), run_time=0.6)
        bd = bchip("BDNF", PURPLE, 26).move_to([-2.2, -0.45, 0])
        link = mod([-3.9, 0.45, 0], [-3.2, -1.45, 0])
        self.at("released")
        self.play(FadeIn(bd, shift=DOWN * 0.1), Create(link), run_time=0.7)
        lad, vm, vm_l, ev, ev_l = voltage_ladder(1.9, e_y=-1.3, ybot=-2.4)
        sk = T("in this sketch", 22, GREY).move_to([2.2, 3.15, 0])
        self.play(FadeIn(lad), FadeIn(vm), FadeIn(vm_l), FadeIn(ev), FadeIn(ev_l), FadeIn(sk), run_time=0.6)
        tag2 = prep_tag("uninjured adult male rats")
        trans = bchip("transferred microglia", PURPLE, 24).move_to([-4.7, 2.5, 0])
        self.at("Transferring those cells")
        self.play(FadeOut(atp), FadeOut(atp_ar), FadeOut(tag), FadeIn(tag2), run_time=0.5)
        self.play(FadeIn(trans), run_time=0.4)
        self.at("reproduced the shift")
        self.play(ev.animate.shift(UP * 2.9), ev_l.animate.shift(UP * 2.9), run_time=0.9)
        beh = T("behavioural change", 26, YELLOW).move_to([-3.0, -3.0, 0])
        self.at("and the behavior")
        self.play(FadeIn(beh), run_time=0.4)
        tag3 = prep_tag("injured rats")
        self.at("Blocking")
        self.play(FadeOut(tag2), FadeOut(trans), FadeOut(beh), FadeIn(tag3), run_time=0.5)
        blockx = cross([-3.4, -0.75], 0.3)
        blabel = T("BDNF to TrkB blocked", 26, RED).move_to([-3.0, -3.0, 0])
        self.play(Create(blockx), FadeIn(blabel), run_time=0.5)
        self.at("reversed both")
        self.play(ev.animate.shift(DOWN * 2.9), ev_l.animate.shift(DOWN * 2.9), run_time=0.9)
        lim1 = bchip("shown in adult male rats", GREY, 24)
        lim2 = bchip("female mice: microglial role debated", GREY, 22)
        lims = VGroup(lim1, lim2).arrange(DOWN, buff=0.25).move_to([0.4, -3.0, 0])
        lim1.move_to([-3.6, -3.0, 0])
        self.at("This was shown in")
        self.play(FadeOut(blockx), FadeOut(blabel), FadeOut(tag3), FadeIn(prep_tag("adult male rats")), run_time=0.4)
        self.play(FadeIn(lim1), run_time=0.4)
        self.at("mouse study")
        lim2.move_to([2.4, -3.0, 0])
        self.play(FadeIn(lim2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Test(SpokenScene):
    def construct(self):
        c1, c2 = 0.8, 4.6
        rows_y = [1.3, -0.1, -1.5]
        h1 = T("Cell death predicts", 24, RED).move_to([c1, 2.75, 0])
        h2 = T("Sign change predicts", 24, YELLOW).move_to([c2, 2.75, 0])
        hl = Line([-6.3, 2.2, 0], [6.3, 2.2, 0], color=GREY, stroke_width=2)

        def label(a, b, y):
            ta = T(a, 26, TEXT)
            tb = T(b, 22, GREY)
            g = VGroup(ta, tb).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            g.move_to([-6.3 + g.width / 2, y, 0])
            return g
        r1 = label("Cells counted", "permanent reporter", rows_y[0])
        r2 = label("Inhibitory currents", "recorded in the target neuron", rows_y[1])
        r3 = label("Anion reversal potential", "gramicidin perforated patch", rows_y[2])
        self.at("tell them apart")
        self.play(FadeIn(hl), run_time=0.3)
        self.at("Count the cells")
        self.play(FadeIn(r1, shift=RIGHT * 0.15), run_time=0.5)
        self.at("Record the inhibitory currents")
        self.play(FadeIn(r2, shift=RIGHT * 0.15), run_time=0.5)
        self.at("Measure the anion reversal")
        self.play(FadeIn(r3, shift=RIGHT * 0.15), run_time=0.5)
        self.at("leaves the cell's own chloride")
        self.play(Indicate(r3, color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.at("Death predicts fewer cells")
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.4)
        d1 = T("fewer", 28, RED).move_to([c1, rows_y[0], 0])
        d2 = T("fewer events", 28, RED).move_to([c1, rows_y[1], 0])
        d3 = T("unchanged", 28, RED).move_to([c1, rows_y[2], 0])
        self.play(FadeIn(VGroup(d1, d2, d3), shift=UP * 0.1), run_time=0.5)
        self.at("A sign change predicts")
        s1 = T("stable", 28, YELLOW).move_to([c2, rows_y[0], 0])
        self.play(FadeIn(s1, shift=UP * 0.1), run_time=0.4)
        self.at("evoked events")
        s2 = T("still present", 28, YELLOW).move_to([c2, rows_y[1], 0])
        s2b = T("(current changes)", 22, YELLOW).move_to([c2, rows_y[1] - 0.4, 0])
        self.play(FadeIn(VGroup(s2, s2b), shift=UP * 0.1), run_time=0.4)
        self.at("depolarized reversal potential")
        s3 = T("depolarized", 28, YELLOW).move_to([c2, rows_y[2], 0])
        self.play(FadeIn(s3, shift=UP * 0.1), run_time=0.4)
        rule = T("A cell count cannot show a change of sign.", 30, TEXT, font=TITLE_FONT).move_to([0, -3.0, 0])
        box = SurroundingRectangle(VGroup(r1, d1, s1), color=GREY, buff=0.15, stroke_width=2)
        self.at("Keep this rule")
        self.play(Create(box), run_time=0.5)
        self.at("It cannot show")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "A cell count cannot show that a signal changed sign."
