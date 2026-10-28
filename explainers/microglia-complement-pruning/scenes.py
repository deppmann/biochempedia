"""Microglia and complement prune synapses: a tag, an eater, a quieter eye (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = inputs from eye A (retinal terminals)
  ORANGE = inputs from eye B
  YELLOW = the complement tag (C1q, C3b, iC3b)
  PURPLE = microglia, the eater (and the eating cell in scene one)
  TEAL   = complement receptor 3 on the microglia
  RED    = silenced eye, removal, mice without the receptor or C3
  GREEN  = boosted (more active) eye
  GREY   = outlines, neurons, lysosome, unknown
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
EYE_A, EYE_B = BLUE, ORANGE


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def P(x, y):
    return np.array([x, y, 0.0])


def bulb(c, color=BLUE, r=0.45, op=0.45):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to(c)


def tag_dots(c, r, n=8, a0=0.0, rad=0.1):
    return VGroup(*[Dot(radius=rad, color=YELLOW).move_to(c + r * P(np.cos(a0 + 2 * PI * k / n), np.sin(a0 + 2 * PI * k / n)))
                    for k in range(n)])


def rcap(line):
    line.set_cap_style(CapStyleType.ROUND)
    return line


def process(a, b, w=18, op=0.55):
    return rcap(Line(a, b, color=PURPLE, stroke_width=w, stroke_opacity=op))


def _unit(deg):
    return P(np.cos(np.radians(deg)), np.sin(np.radians(deg)))


def branch(c, ang, ln, sx, w=13, op=0.55, bend=7):
    """one gently curved process with a twig, leaving the soma at angle `ang` (degrees)."""
    pts = [c + _unit(ang) * 0.6 * sx, c + _unit(ang + bend) * 0.55 * ln, c + _unit(ang + bend * 1.5) * 0.8 * ln,
           c + _unit(ang + bend * 1.6) * ln]
    m = VMobject().set_points_smoothly(pts).set_stroke(PURPLE, w, opacity=op)
    m.set_cap_style(CapStyleType.ROUND)
    t0 = c + _unit(ang + bend * 1.2) * 0.7 * ln
    tw = rcap(Line(t0, t0 + _unit(ang + 50) * 0.5 * sx, color=PURPLE, stroke_width=w * 0.7, stroke_opacity=op))
    return VGroup(m, tw)


def microglia(c, sx=1.0, procs=((160, 1.5), (200, 1.5), (110, 1.3), (70, 1.3), (250, 1.3))):
    """small soma (ellipse) with branched processes. returns a VGroup; .body is the soma."""
    body = Ellipse(width=1.7 * sx, height=1.5 * sx, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to(c)
    parts = [branch(c, ang, ln * sx, sx) for ang, ln in procs] + [body]
    g = VGroup(*parts)
    g.body = body
    return g


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar_rect(x0, y, w, h, color):
    return Rectangle(width=max(w, 0.02), height=h, stroke_color=color, stroke_width=3,
                     fill_color=color, fill_opacity=0.5).move_to(P(x0 + max(w, 0.02) / 2, y))


def terr(x0, x1, cy, h, color, op=0.35):
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                     fill_color=color, fill_opacity=op).move_to(P((x0 + x1) / 2, cy))


class S00Title(TitleCard):
    LESSON = "Microglia and complement prune synapses"
    TITLE = "A tag, an eater, a quieter eye"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        NC = P(3.4, 0.2)
        self.at("Why would a young neuron")
        soma = Circle(radius=1.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.16).move_to(NC)
        stubs = VGroup(*[rcap(Line(NC + _unit(a) * 1.7, NC + _unit(a) * 2.15, color=GREY, stroke_width=6)) for a in (200, 250, 290, 340)])
        q = T("?", 140, GREY, font=TITLE_FONT).move_to(NC)
        yl = T("young neuron", 28, GREY).move_to(NC + P(0, -2.65))
        self.play(FadeIn(soma, scale=0.9), FadeIn(stubs), FadeIn(q), FadeIn(yl), run_time=0.8)
        self.at("of an immune cascade")
        ic = chip("immune cascade", YELLOW, size=30).move_to(NC + P(0, 2.55))
        self.play(FadeIn(ic, shift=DOWN * 0.1), run_time=0.6)

        # left: complement coats a microbe and an eating cell swallows it
        self.at("is a set of proteins")
        MB = P(-4.9, 0.4)
        mic = Circle(radius=1.1, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to(MB)
        mic_l = T("microbe", 26, GREY).move_to(MB + P(0, -1.85))
        self.play(FadeIn(mic, scale=0.9), FadeIn(mic_l), run_time=0.6)
        self.at("coat microbes")
        tags = tag_dots(MB, 1.32, 12, rad=0.12)
        tag_l = T("complement", 28, YELLOW).move_to(MB + P(0, 2.15))
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in tags], lag_ratio=0.08), FadeIn(tag_l), run_time=1.0)
        self.at("eating cells")
        ep = P(-0.9, 0.4)
        eater = Circle(radius=1.3, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to(ep)
        eater_l = T("eating cell", 26, PURPLE).move_to(ep + P(0, -1.95))
        self.play(FadeIn(eater, scale=0.9), FadeIn(eater_l), run_time=0.6)
        self.at("swallow")
        ep2 = P(-3.9, 0.4)
        self.play(eater.animate.move_to(ep2), eater_l.animate.move_to(ep2 + P(0, -1.95)),
                  FadeOut(mic_l), FadeOut(tag_l), run_time=0.9)
        grp = VGroup(mic, tags)
        self.play(grp.animate.move_to(ep2).scale(0.4), run_time=0.7)
        self.play(FadeOut(grp), run_time=0.3)

        # right: the neuron makes C1q
        self.at("retinal neurons make")
        nl = T("retinal neuron", 28, GREY).move_to(NC + P(0, -2.65))
        c1q = chip("C1q", YELLOW, size=44).move_to(NC)
        self.play(FadeOut(q), FadeIn(c1q, scale=0.8), ReplacementTransform(yl, nl), FadeOut(ic), FadeOut(eater), FadeOut(eater_l), run_time=0.7)
        shift = P(-3.0, 0.0)
        self.play(VGroup(soma, stubs, c1q, nl).animate.shift(shift), run_time=0.8)
        NC = NC + shift
        self.at("connections it built")
        terms = VGroup()
        for k, a in enumerate((20, 60, 100, 140)):
            col = EYE_A if k % 2 == 0 else EYE_B
            ln = rcap(Line(NC + _unit(a) * 1.7, NC + _unit(a) * 2.3, color=col, stroke_width=5))
            terms.add(VGroup(ln, bulb(NC + _unit(a) * 2.55, col, 0.3)))
        self.play(LaggedStart(*[FadeIn(t, scale=0.4) for t in terms], lag_ratio=0.25), run_time=1.2)
        self.at("too many")
        self.play(*[Indicate(t, color=TEXT, scale_factor=1.25) for t in terms], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Overlap(SpokenScene):
    def construct(self):
        cy = -0.2
        self.at("visual thalamus")
        box = RoundedRectangle(corner_radius=0.25, width=12.2, height=5.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.06).move_to(P(0, -0.2))
        bl = T("visual thalamus", 30, GREY).move_to(P(0, 3.2))
        self.play(FadeIn(box), FadeIn(bl), run_time=0.7)
        self.at("inputs from the two eyes")
        ta = terr(-5.6, 1.0, cy, 3.0, EYE_A)
        tb = terr(-1.0, 5.6, cy, 3.0, EYE_B)
        la = T("eye A inputs", 28, EYE_A).move_to(P(-3.6, 2.0))
        lb = T("eye B inputs", 28, EYE_B).move_to(P(3.6, 2.0))
        self.play(FadeIn(ta), FadeIn(tb), run_time=0.7)
        self.play(FadeIn(la), FadeIn(lb), run_time=0.4)
        self.at("overlap there")
        dots = VGroup()
        for k, (x, y) in enumerate([(-0.5, 0.5), (0.4, -0.1), (-0.3, -0.6), (0.5, 0.7), (-0.55, -0.1), (0.2, -0.9)]):
            col = EYE_A if k % 2 == 0 else EYE_B
            dots.add(Dot(radius=0.17, color=col).move_to(P(x, y)))
        ov = DoubleArrow(P(-1.0, -2.1), P(1.0, -2.1), buff=0, color=TEXT, stroke_width=4, tip_length=0.2)
        ovl = T("overlap", 26, TEXT).move_to(P(0, -2.5))
        self.play(FadeIn(dots), GrowFromCenter(ov), FadeIn(ovl), run_time=0.7)
        self.at("separate territories")
        ta2 = terr(-5.6, -0.2, cy, 3.0, EYE_A)
        tb2 = terr(0.2, 5.6, cy, 3.0, EYE_B)
        self.play(Transform(ta, ta2), Transform(tb, tb2), FadeOut(ov), FadeOut(ovl), run_time=1.4)
        self.at("Inputs that lose")
        self.play(*[d.animate.set_color(RED) for d in dots], run_time=0.3)
        self.play(*[d.animate.scale(0.2).set_opacity(0) for d in dots], run_time=0.7)
        self.at("Which inputs go")
        q = T("?", 120, GREY, font=TITLE_FONT).move_to(P(0, -0.2))
        self.play(FadeIn(q, scale=0.7), run_time=0.5)
        self.at("takes them away")
        ring = DashedVMobject(Circle(radius=0.95, stroke_color=PURPLE, stroke_width=5).move_to(P(0, -0.2)), num_dashes=18)
        q2 = T("?", 120, PURPLE, font=TITLE_FONT).move_to(P(0, -0.2))
        self.play(ReplacementTransform(q, q2), FadeIn(ring), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Tag(SpokenScene):
    def construct(self):
        BC, RC = P(-2.7, 0.6), P(1.1, 0.6)
        self.at("first part of the answer")
        axon = rcap(Line(P(-2.7, 3.5), BC + P(0, 1.45), color=EYE_A, stroke_width=6))
        b = bulb(BC, EYE_A, 1.45, 0.4)
        relay = Circle(radius=2.0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to(RC)
        rl = T("relay neuron", 28, GREY).move_to(RC)
        bl = T("a retinal input", 28, EYE_A).move_to(BC + P(0, -2.2))
        self.play(Create(axon), FadeIn(b, scale=0.8), FadeIn(relay), FadeIn(rl), FadeIn(bl), run_time=1.0)

        c1 = chip("C1q", YELLOW, size=30)
        ch = chip("chain of cuts", GREY, size=28)
        c3 = chip("C3", YELLOW, size=30)
        c3b = chip("C3b", YELLOW, size=30)
        ic = chip("iC3b", YELLOW, size=30)
        row = VGroup(c1, ch, c3, c3b, ic).arrange(RIGHT, buff=0.75).move_to(P(0, -3.0))
        a1 = arr(c1.get_right(), ch.get_left()); a2 = arr(ch.get_right(), c3.get_left())
        a3 = arr(c3.get_right(), c3b.get_left()); a4 = arr(c3b.get_right(), ic.get_left())
        self.at("binds a target")
        mark = chip("C1q", YELLOW, size=24, pad=0.12).move_to(BC + P(0.9, 1.55))
        self.play(FadeIn(c1, shift=DOWN * 0.1), FadeIn(mark, scale=0.7), run_time=0.7)
        self.at("chain of cuts")
        self.play(GrowArrow(a1), FadeIn(ch), run_time=0.5)
        self.at("cut in two")
        self.play(GrowArrow(a2), FadeIn(c3), run_time=0.5)
        small = Dot(radius=0.1, color=YELLOW).move_to(c3.get_top() + UP * 0.1)
        self.play(FadeIn(small), run_time=0.15)
        self.play(small.animate.shift(UP * 0.7 + RIGHT * 0.5).set_opacity(0), GrowArrow(a3), FadeIn(c3b), run_time=0.8)
        self.at("big piece")
        self.play(Indicate(c3b, color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.at("nearby surface")
        tags = tag_dots(BC, 1.7, 10, a0=0.3, rad=0.14)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in tags], lag_ratio=0.12), FadeOut(mark), run_time=1.1)
        self.at("trimmed")
        self.play(GrowArrow(a4), FadeIn(ic), run_time=0.5)
        self.play(Indicate(ic, color=YELLOW, scale_factor=1.15), *[Indicate(d, color=TEXT, scale_factor=1.5) for d in tags], run_time=0.7)
        self.at("developing synapses")
        cons = VGroup(); tg = VGroup()
        RC2 = RC
        for k, a in enumerate((25, 60, 95, 130, 230, 265, 300, 335)):
            col = EYE_A if k % 2 == 0 else EYE_B
            pos = RC2 + _unit(a) * 2.5
            cons.add(bulb(pos, col, 0.28, 0.5))
            if k % 3 != 2:
                tg.add(tag_dots(pos, 0.48, 5, a0=0.2, rad=0.08))
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cons], lag_ratio=0.1), run_time=0.9)
        self.play(FadeIn(tg), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Eater(SpokenScene):
    def construct(self):
        MC = P(-3.6, 0.3)
        TC = P(3.7, 0.3)
        # carried over: a tagged input
        axon = rcap(Line(P(3.7, 3.5), TC + P(0, 0.9), color=EYE_A, stroke_width=6))
        tb = bulb(TC, EYE_A, 0.9, 0.45)
        tg = tag_dots(TC, 1.12, 9, a0=0.3, rad=0.12)
        tl = T("tagged input", 28, YELLOW).move_to(P(3.7, -1.75))
        self.add(axon, tb, tg, tl)
        self.at("The second part is the eater")
        mg = microglia(MC, 1.5, procs=((160, 1.4), (205, 1.4), (115, 1.2), (70, 1.1)))
        self.play(FadeIn(mg, scale=0.85), run_time=0.8)
        self.at("resident immune cells")
        ml = T("microglia", 32, PURPLE).move_to(MC + P(0, -2.5))
        self.play(FadeIn(ml, shift=UP * 0.1), run_time=0.5)
        self.at("complement receptor")
        tip = P(1.1, 0.3)
        reach = process(MC + P(1.1, 0.0), tip, w=24, op=0.55)
        self.play(Create(reach), run_time=0.9)
        caps = VGroup(*[Arc(radius=0.24, start_angle=PI / 2, angle=PI, arc_center=tip + P(0.2, dy), color=TEAL, stroke_width=7)
                        for dy in (-0.5, 0.0, 0.5)])
        rl = T("complement receptor 3", 28, TEAL).move_to(P(0.0, 1.75))
        self.play(FadeIn(caps), FadeIn(rl), run_time=0.6)
        self.at("binds")
        self.play(reach.animate.put_start_and_end_on(MC + P(1.1, 0.0), P(2.0, 0.3)),
                  caps.animate.shift(P(0.9, 0)), run_time=0.8)
        self.at("promotes engulfment")
        lys = Circle(radius=0.75, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to(MC + P(-0.1, 0.0))
        ll = T("lysosome", 26, GREY).move_to(MC + P(0.9, -1.55))
        self.play(FadeIn(lys), FadeIn(ll), FadeOut(rl), run_time=0.5)
        pc = bulb(P(2.85, 0.3), EYE_A, 0.3, 0.6)
        pd = VGroup(*[Dot(radius=0.07, color=YELLOW).move_to(P(2.62, 0.3 + dy)) for dy in (-0.15, 0.15)])
        stuff = VGroup(pc, pd)
        self.play(FadeIn(stuff, scale=0.5), run_time=0.4)
        self.play(stuff.animate.move_to(lys.get_center()).scale(0.6),
                  FadeOut(reach), FadeOut(caps), run_time=1.4)
        self.at("retinal material inside")
        allg = VGroup(mg, ml, lys, ll, stuff)
        self.play(FadeOut(VGroup(axon, tb, tg, tl)), allg.animate.scale(1.35).move_to(P(-0.8, 0.2)), run_time=0.9)
        rm = T("retinal material", 28, EYE_A).move_to(lys.get_center() + P(3.0, -0.9))
        ar = arr(rm.get_left() + P(-0.05, 0.1), lys.get_center() + P(0.55, -0.15), EYE_A)
        self.play(FadeIn(rm), GrowArrow(ar), run_time=0.7)
        self.at("digestive compartments")
        self.play(Indicate(lys, color=TEXT, scale_factor=1.25), run_time=0.8)
        self.at("glows only in acid")
        self.play(lys.animate.set_fill(TEXT, 0.55).set_stroke(TEXT), Flash(lys, color=TEXT, line_length=0.3, flash_radius=1.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Quieter(SpokenScene):
    def construct(self):
        X0, W, HB = 3.3, 3.0, 0.6
        yA, yB = 0.9, -1.0
        self.at("Does the eater choose")
        ea = chip("eye A", EYE_A, size=32).move_to(P(-5.3, 1.9))
        eb = chip("eye B", EYE_B, size=32).move_to(P(-5.3, -1.9))
        ba, bb = bulb(P(-3.1, 1.9), EYE_A, 0.45, 0.5), bulb(P(-3.1, -1.9), EYE_B, 0.45, 0.5)
        la = rcap(Line(ea.get_right(), ba.get_left(), color=EYE_A, stroke_width=5))
        lb = rcap(Line(eb.get_right(), bb.get_left(), color=EYE_B, stroke_width=5))
        MC = P(0.0, 0.0)
        mg = microglia(MC, 1.5, procs=((20, 1.3), (340, 1.3), (90, 1.1), (270, 1.1)))
        pa = process(MC + P(-0.8, 0.45), ba.get_right() + P(0.05, -0.03), w=16, op=0.5)
        pb = process(MC + P(-0.8, -0.45), bb.get_right() + P(0.05, 0.03), w=16, op=0.5)
        ml = T("microglia", 28, PURPLE).move_to(MC + P(0, -2.2))
        title = T("material in microglia", 28, TEXT).move_to(P(4.6, 2.6))
        tA = T("from eye A", 26, EYE_A).move_to(P(X0 + 0.95, yA + 0.6))
        tB = T("from eye B", 26, EYE_B).move_to(P(X0 + 0.95, yB + 0.6))
        rA, rB = bar_rect(X0, yA, 0.0, HB, EYE_A), bar_rect(X0, yB, 0.0, HB, EYE_B)
        base = Line(P(X0, 2.1), P(X0, -1.8), color=GREY, stroke_width=3)
        self.play(FadeIn(ea), FadeIn(eb), FadeIn(ba), FadeIn(bb), Create(la), Create(lb),
                  FadeIn(pa), FadeIn(pb), FadeIn(mg), FadeIn(ml), FadeIn(title), FadeIn(tA), FadeIn(tB), FadeIn(base), run_time=1.2)

        # case one: eye A silenced
        self.at("Silence one eye")
        case = T("eye A silenced", 30, RED, weight=BOLD).move_to(P(-5.3, 0.75))
        self.play(FadeIn(case, shift=DOWN * 0.1), ba.animate.set_fill(EYE_A, 0.12).set_stroke(opacity=0.45), la.animate.set_stroke(opacity=0.35),
                  run_time=0.5)
        self.at("held more material")
        self.play(Transform(rA, bar_rect(X0, yA, W, HB, EYE_A)), Transform(rB, bar_rect(X0, yB, 1.2, HB, EYE_B)), run_time=1.0)
        self.wait(0.4)

        # case two: eye A boosted. the old answer is cleared in the same move that brings in the new label
        self.at("Boost one eye")
        case2 = T("eye A boosted", 30, GREEN, weight=BOLD).move_to(P(-5.3, 0.75))
        self.play(Transform(rA, bar_rect(X0, yA, 0.0, HB, EYE_A)), Transform(rB, bar_rect(X0, yB, 0.0, HB, EYE_B)),
                  ReplacementTransform(case, case2), ba.animate.set_fill(EYE_A, 0.7).set_stroke(opacity=1.0), la.animate.set_stroke(opacity=1.0),
                  run_time=0.7)
        self.at("untreated eye")
        self.play(Transform(rB, bar_rect(X0, yB, W, HB, EYE_B)), Transform(rA, bar_rect(X0, yA, 1.2, HB, EYE_A)), run_time=1.0)
        self.at("whole eyes")
        note = T("whole eyes, not single synapses", 28, GREY).move_to(P(0.0, -3.3))
        self.play(FadeIn(note), Indicate(ea, color=TEXT, scale_factor=1.2), Indicate(eb, color=TEXT, scale_factor=1.2), run_time=0.9)
        self.at("how activity becomes a tag")
        note2 = T("how does activity become a tag?", 28, YELLOW).move_to(P(0.0, -3.3))
        self.play(ReplacementTransform(note, note2), run_time=0.5)
        self.at("preferentially remove")
        fin = T("less active inputs are removed more", 30, PURPLE).move_to(P(0.0, -3.3))
        self.play(ReplacementTransform(note2, fin), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Knockout(SpokenScene):
    def construct(self):
        base_y, H = -1.8, 3.4
        self.at("take away the reader")
        title = T("uptake by microglia", 32, TEXT).move_to(P(0, 3.1))
        axis = Line(P(-6, base_y), P(6, base_y), color=GREY, stroke_width=3)
        n_bar = Rectangle(width=2.4, height=H, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.5)
        n_bar.move_to(P(-3.0, base_y + H / 2))
        n_l = T("normal", 30, TEXT).move_to(P(-3.0, base_y - 0.5))
        self.play(FadeIn(title), Create(axis), GrowFromEdge(n_bar, DOWN), FadeIn(n_l), run_time=1.0)
        self.at("Without complement receptor")
        k_bar = Rectangle(width=2.4, height=H / 2, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.4)
        k_bar.move_to(P(3.0, base_y + H / 4))
        k_l = T("no receptor, or no C3", 30, RED).move_to(P(3.0, base_y - 0.5))
        self.play(FadeIn(k_l, shift=UP * 0.1), run_time=0.6)
        self.at("roughly half as much")
        k2 = Rectangle(width=2.4, height=H / 2, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.4)
        k2.move_to(P(3.0, base_y + H / 4))
        half = DashedLine(P(-1.7, base_y + H / 2), P(1.8, base_y + H / 2), color=GREY, stroke_width=3)
        self.play(GrowFromEdge(k_bar, DOWN), Create(half), run_time=1.0)
        self.at("remained without the receptor")
        self.play(Indicate(k_bar, color=RED, scale_factor=1.08), run_time=0.8)
        self.at("other routes")
        oc = chip("other routes", GREY, size=30).move_to(P(3.0, base_y + H / 2 + 0.95))
        oa = arr(oc.get_bottom(), P(3.0, base_y + H / 2 - 0.25), GREY)
        self.play(FadeIn(oc, shift=DOWN * 0.1), GrowArrow(oa), run_time=0.7)

        # a month later: two thalamus pictures
        self.at("A month after birth")
        self.play(*[FadeOut(m) for m in (title, axis, n_bar, k_bar, n_l, k_l, half, oc, oa)], run_time=0.6)

        def pic(cx, label, col):
            bx = RoundedRectangle(corner_radius=0.2, width=5.9, height=3.7, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.06).move_to(P(cx, 0.1))
            lab = T(label, 30, col).move_to(P(cx, 2.3))
            return bx, lab

        bxn, labn = pic(-3.3, "normal", TEXT)
        bxk, labk = pic(3.3, "no receptor, or no C3", RED)
        cy = 0.4
        tan = terr(-5.9, -3.4, cy, 2.2, EYE_A); tbn = terr(-3.2, -0.7, cy, 2.2, EYE_B)
        tak = terr(0.7, 3.7, cy, 2.2, EYE_A); tbk = terr(2.9, 5.9, cy, 2.2, EYE_B)

        def dots_at(pts, col):
            return VGroup(*[Dot(radius=0.13, color=col).move_to(P(x, y)) for x, y in pts])
        dn = VGroup(dots_at([(-5.4, 1.0), (-4.6, 0.3), (-4.0, 0.95)], EYE_A), dots_at([(-2.6, 1.0), (-1.9, 0.3), (-1.3, 0.95)], EYE_B))
        dk = VGroup(dots_at([(1.3, 1.0), (2.1, 0.3), (2.7, 0.95), (1.7, -0.2), (2.4, 0.65), (3.0, -0.1)], EYE_A),
                    dots_at([(3.5, 0.8), (4.3, -0.2), (5.1, 0.7), (4.0, 1.0), (4.8, 0.3), (5.4, -0.1)], EYE_B))
        when = T("about a month after birth", 30, GREY).move_to(P(0, 3.15))
        self.play(FadeIn(bxn), FadeIn(labn), FadeIn(bxk), FadeIn(labk), FadeIn(when), FadeIn(tan), FadeIn(tbn),
                  FadeIn(tak), FadeIn(tbk), FadeIn(dn), FadeIn(dk), run_time=1.0)
        self.at("more retinal synapses")
        syn = T("dots: synapses", 26, TEXT).move_to(P(0, -2.3))
        self.play(FadeIn(syn), Indicate(dk, color=TEXT, scale_factor=1.1), run_time=0.8)
        self.at("more overlap")
        ovl = DoubleArrow(P(2.9, -1.0), P(3.7, -1.0), buff=0, color=TEXT, stroke_width=4, tip_length=0.18)
        ovt = T("more overlap", 26, TEXT).move_to(P(3.3, -1.45))
        self.play(FadeIn(ovl), FadeIn(ovt), run_time=0.6)

        # the rule
        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in (bxn, labn, bxk, labk, tan, tbn, tak, tbk, dn, dk, ovl, ovt, when, syn)], run_time=0.6)
        sc = T("in the mouse visual thalamus", 32, GREY).move_to(P(0, 3.0))
        r1 = chip("complement tags", YELLOW, size=44)
        r2 = chip("microglia eat", PURPLE, size=44)
        r3 = chip("less active inputs eaten more", TEXT, size=40)
        col = VGroup(r1, r2, r3).arrange(DOWN, buff=0.9).move_to(P(0, -0.2))
        ra = arr(r1.get_bottom(), r2.get_top(), TEXT); rb = arr(r2.get_bottom(), r3.get_top(), TEXT)
        self.play(FadeIn(sc), run_time=0.4)
        self.at("complement tags")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.at("microglia eat")
        self.play(GrowArrow(ra), FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.at("less active inputs")
        self.play(GrowArrow(rb), FadeIn(r3, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "In mouse thalamus, complement tags, microglia eat, less active inputs eaten more."
