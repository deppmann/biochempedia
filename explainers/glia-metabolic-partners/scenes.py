"""Who Feeds the Far End?  (chapter 1 of Feeding the Axon: Glia as Metabolic Partners)

COLOR MAP (one color per concept, whole series; taken from scenes.old.py)
  BLUE   = the neuron / axon (and its pumps)
  TEAL   = myelinating glia (oligodendrocyte, Schwann cell) and the myelin they make
  PURPLE = astrocyte (not used in this chapter)
  ORANGE = lactate and pyruvate, glycolysis
  YELLOW = ATP, energy, the thing being asked about
  GREY   = membranes, ions, myelin before we learn whose it is, outlines
  TEXT   = glucose, fluid outside
  GOLD   = the numbered fact labels (1. Cost, 2. Distance, 3. Cover)
  GREEN  = evidence for / intact
  RED    = blocked, failure, lost
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rrect(w, h, color, fo=0.15, sw=3, r=0.2):
    return RoundedRectangle(corner_radius=min(r, w / 2, h / 2), width=w, height=h, stroke_color=color,
                            stroke_width=sw, fill_color=color, fill_opacity=fo)


def dot(label, color, r=0.3, size=22, fo=0.3):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fo)
    return VGroup(c, T(label, size, TEXT).move_to(c))


def mito(x, y, w=1.0, h=0.55, color=YELLOW):
    o = Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.18)
    pts = [[-w * .30, 0, 0], [-w * .18, h * .22, 0], [-w * .06, -h * .22, 0], [w * .06, h * .22, 0],
           [w * .18, -h * .22, 0], [w * .30, 0, 0]]
    ins = VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
    return VGroup(o, ins).move_to([x, y, 0])


def gate(x, y, color=GREY, h=0.95):
    a = rrect(0.5, h, color, 0.5, 3, 0.1).move_to([x - 0.45, y, 0])
    b = rrect(0.5, h, color, 0.5, 3, 0.1).move_to([x + 0.45, y, 0])
    return VGroup(a, b)


def cross(c, color=RED, s=0.3):
    return VGroup(Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=7),
                  Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=7))


GREY_MYELIN = "#3d4452"    # opaque dark grey: myelin whose owner we have not shown yet
TEAL_MYELIN = "#296d74"    # opaque teal: myelin that belongs to a glial cell


def myelin_block(w, h, r=0.3, teal=False):
    return RoundedRectangle(corner_radius=min(r, w / 2, h / 2), width=w, height=h,
                            stroke_color=TEAL if teal else GREY, stroke_width=3,
                            fill_color=TEAL_MYELIN if teal else GREY_MYELIN, fill_opacity=1)


def solid_chip(text, color, size=24):
    """a chip with an opaque backing, so a line behind it does not show through the label."""
    c = chip(text, color, size)
    under = Rectangle(width=c[0].width, height=c[0].height, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(under, *c)


def fact_label(text, pos=(-5.3, 3.3)):
    return T(text, 40, GOLD, weight=BOLD).move_to([pos[0], pos[1], 0])


# ============================================================================================
class S00Title(TitleCard):
    LESSON = "Feeding the Axon: Glia as Metabolic Partners"
    TITLE = "Who Feeds the Far End?"


# ============================================================================================
def body_figure(cx=-5.0):
    st = dict(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    head = Circle(radius=0.55, **st).move_to([cx, 2.55, 0])
    torso = RoundedRectangle(corner_radius=0.4, width=1.7, height=2.6, **st).move_to([cx, 0.85, 0])
    arms = [RoundedRectangle(corner_radius=0.2, width=0.42, height=2.2, **st).move_to([cx + s * 1.2, 0.85, 0]) for s in (-1, 1)]
    legs = [RoundedRectangle(corner_radius=0.25, width=0.7, height=2.7, **st).move_to([cx + s * 0.42, -1.75, 0]) for s in (-1, 1)]
    return VGroup(head, torso, *arms, *legs)


class S01Q(SpokenScene):
    def construct(self):
        cx = -5.0
        body = body_figure(cx).scale(1.12, about_point=np.array([cx, 0, 0]))
        head_c = body[0].get_center()
        brain = Ellipse(width=0.95, height=0.68, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.7).move_to(head_c)
        brain_l = T("brain", 34, BLUE).move_to(head_c + np.array([1.55, 0.0, 0]))
        self.play(FadeIn(body), run_time=0.4)
        self.at("brain")
        self.play(GrowFromCenter(brain), FadeIn(brain_l), run_time=0.5)
        base_y = -3.0
        base = Line([-1.2, base_y, 0], [6.8, base_y, 0], color=GREY, stroke_width=3)
        h20 = 5.2
        b1 = Rectangle(width=2.2, height=h20 * 0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([0.5, base_y + h20 * 0.05, 0])
        b2 = Rectangle(width=2.2, height=h20, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([4.6, base_y + h20 / 2, 0])
        self.at("about 2")
        v1 = M("2%", 48, GREY, weight=BOLD).next_to(b1, UP, buff=0.2)
        l1 = T("of body weight", 32, GREY).move_to([0.5, -3.45, 0])
        self.play(Create(base), GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.6)
        self.play(FadeIn(v1), run_time=0.2)
        self.at("about 20")
        v2 = M("20%", 56, YELLOW, weight=BOLD).next_to(b2, UP, buff=0.2)
        l2 = T("of resting energy", 32, YELLOW).move_to([4.6, -3.45, 0])
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=1.0)
        self.play(FadeIn(v2), Indicate(b2, color=YELLOW, scale_factor=1.03), run_time=0.5)
        # zoom from the brain into one neuron
        self.at("who delivers")
        soma = Circle(radius=1.8, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.2).move_to([-4.8, 0, 0])
        dends = VGroup(*[Line([-4.8 - 1.7 * np.cos(a), 1.7 * np.sin(a), 0], [-4.8 - 2.5 * np.cos(a) - 0.2, 2.5 * np.sin(a), 0], color=BLUE, stroke_width=6)
                         for a in (0.8, 0.25, -0.3, -0.85)])
        soma_l = T("cell body", 34, BLUE).move_to([-4.8, 0, 0])
        neuron = VGroup(soma, dends, soma_l)
        old = VGroup(body, brain, brain_l, base, b1, b2, v1, v2, l1, l2)
        self.play(old.animate.scale(7, about_point=brain.get_center()).set_opacity(0),
                  FadeIn(neuron, scale=0.4), run_time=0.7)
        tube = Rectangle(width=11.2, height=0.7, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to([-3.0 + 5.6, 0, 0])
        axl = T("axon", 34, BLUE).move_to([0.5, 0.75, 0])
        self.at("fuel to")
        self.play(GrowFromEdge(tube, LEFT), FadeIn(axl), run_time=0.7)
        self.at("far end")
        q = T("?", 130, YELLOW, weight=BOLD).move_to([5.9, 1.25, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.4)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=0.7)
        self.finish()


# ============================================================================================
class S02Cost(SpokenScene):
    def construct(self):
        title = fact_label("1. Cost", (-5.7, 3.45))
        CX, PX = -3.4, 3.0
        pieces = VGroup(
            rrect(2.4, 0.7, GREY, 0.4, 3, 0.1).move_to([-6.2, 0, 0]),
            rrect(3.6, 0.7, GREY, 0.4, 3, 0.1).move_to([0.0, 0, 0]),
            rrect(3.0, 0.7, GREY, 0.4, 3, 0.1).move_to([5.7, 0, 0]),
        )
        chan = VGroup(rrect(0.6, 0.9, BLUE, 0.55, 3, 0.1).move_to([CX - 1.25, 0, 0]),
                      rrect(0.6, 0.9, BLUE, 0.55, 3, 0.1).move_to([CX + 1.25, 0, 0]))
        pump = rrect(2.4, 1.3, BLUE, 0.35, 3, 0.2).move_to([PX, 0, 0])
        out_l = T("outside", 34, GREY).move_to([0.0, 0.72, 0])
        in_l = T("inside", 34, GREY).move_to([0.0, -0.72, 0])
        chan_l = T("channel", 34, BLUE).move_to([CX, 3.45, 0])
        chan_ld = Line([-2.0, 3.15, 0], [-2.0, 0.5, 0], color=BLUE, stroke_width=2, stroke_opacity=0.6)
        self.play(FadeIn(title), FadeIn(pieces), FadeIn(chan), FadeIn(pump), FadeIn(out_l), FadeIn(in_l),
                  FadeIn(chan_l), Create(chan_ld), run_time=0.5)
        NL, KL = CX - 0.65, CX + 0.65
        na1 = dot("Na+", TEXT, 0.52, 30).move_to([NL, 1.7, 0])
        na2 = dot("Na+", TEXT, 0.52, 30).move_to([-0.8, 2.5, 0])
        k1 = dot("K+", GREY, 0.52, 30).move_to([KL, -1.75, 0])
        k2 = dot("K+", GREY, 0.52, 30).move_to([-1.0, -2.1, 0])
        self.play(*[FadeIn(i, scale=0.6) for i in (na1, na2, k1, k2)], run_time=0.5)
        # the impulse: one Na+ in, one K+ out through the channel
        self.at("after every")
        spk = spikes(-6.6, 2.1, 1.7, 1.0, 1)
        spk_l = T("impulse", 34, YELLOW).move_to([-5.75, 1.3, 0])
        a_in = arr([NL, 1.25, 0], [NL, -1.0, 0], TEXT, 5)
        a_out = arr([KL, -1.0, 0], [KL, 1.25, 0], GREY, 5)
        self.play(Create(spk), FadeIn(spk_l), GrowArrow(a_in), GrowArrow(a_out), run_time=0.4)
        self.play(na1.animate.move_to([NL, -1.7, 0]), run_time=0.6)
        self.play(k1.animate.move_to([KL, 1.7, 0]), run_time=0.6)
        # the pump has to undo it
        self.at("sodium potassium pump")
        pump_l = T("Na+/K+ pump", 34, BLUE).move_to([PX, 3.45, 0])
        pump_ld = Line([4.0, 3.15, 0], [4.0, 0.7, 0], color=BLUE, stroke_width=2, stroke_opacity=0.6)
        nas = [dot("Na+", TEXT, 0.52, 30).move_to([x, -1.5, 0]) for x in (1.4, 2.65, 3.9)]
        ks = [dot("K+", GREY, 0.52, 30).move_to([x, 1.5, 0]) for x in (4.95, 6.2)]
        self.play(FadeOut(VGroup(a_in, a_out, spk, spk_l)), FadeIn(pump_l), Create(pump_ld), Indicate(pump, color=BLUE, scale_factor=1.08),
                  *[FadeIn(i, scale=0.6) for i in nas + ks], run_time=0.9)
        self.at("puts sodium")
        t1 = T("3 Na+ out", 36, TEXT)
        t2 = T("2 K+ in", 36, GREY)
        t3 = T("1 ATP", 36, YELLOW)
        tally = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.9).move_to([0.2, -3.05, 0])
        t1.set_opacity(0), t2.set_opacity(0), t3.set_opacity(0)
        self.add(tally)
        self.play(pump.animate.set_fill(BLUE, 0.7), t1.animate.set_opacity(1),
                  LaggedStart(*[n.animate.move_to([n.get_center()[0], 1.5, 0]) for n in nas], lag_ratio=0.25), run_time=1.1)
        self.at("potassium back")
        self.play(t2.animate.set_opacity(1),
                  LaggedStart(*[k.animate.move_to([k.get_center()[0], -1.5, 0]) for k in ks], lag_ratio=0.3), run_time=1.0)
        self.at("each cycle")
        atp = chip("ATP", YELLOW, 32).move_to([PX, -2.4, 0])
        self.play(FadeIn(atp, shift=UP * 0.2), pump.animate.set_fill(BLUE, 0.35), run_time=0.5)
        self.at("1 ATP")
        self.play(t3.animate.set_opacity(1), Indicate(atp, color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.finish()


# ============================================================================================
class S03Budget(SpokenScene):
    def construct(self):
        head = T("Energy used for signalling", 44, TEXT).move_to([0, 3.35, 0])
        sub = T("rodent grey matter", 34, GREY).move_to([0, 2.65, 0])
        W, H, X0, Y = 12.2, 3.4, -6.1, 0.35
        pw = W * 0.68
        pumps = Rectangle(width=pw, height=H, stroke_width=0, fill_color=BLUE, fill_opacity=0.55).move_to([X0 + pw / 2, Y, 0])
        rest = Rectangle(width=W - pw, height=H, stroke_width=0, fill_color=GREY, fill_opacity=0.3).move_to([X0 + pw + (W - pw) / 2, Y, 0])
        frame = Rectangle(width=W, height=H, stroke_color=GREY, stroke_width=3).move_to([0, Y, 0])
        rest_l = T("everything\nelse", 34, GREY).move_to(rest)
        self.play(FadeIn(head), FadeIn(sub), FadeIn(pumps), FadeIn(rest), FadeIn(rest_l), Create(frame), run_time=0.5)
        credit = T("Attwell and Laughlin, 2001, and later revisions", 32, GREY).move_to([0, -2.75, 0])
        note = T("exact share varies", 34, GREY).move_to([0, -1.75, 0])
        self.play(FadeIn(credit), run_time=0.5)
        self.at("most of")
        most = T("most", 72, TEXT, weight=BOLD).move_to(pumps)
        self.play(FadeIn(most, scale=0.8), Indicate(pumps, color=BLUE, scale_factor=1.02), FadeIn(note), run_time=0.7)
        self.at("these pumps")
        pl = T("Na+/K+ pumps", 60, TEXT, weight=BOLD).move_to(pumps)
        self.play(ReplacementTransform(most, pl), Indicate(pumps, color=BLUE, scale_factor=1.03), run_time=0.7)
        self.finish()


# ============================================================================================
def leg_xy(x, y):
    return [x, y * 0.95 - 0.35, 0]


class S04Dist(SpokenScene):
    def construct(self):
        title = fact_label("2. Distance", (-5.4, 3.45))
        pts = [(-3.3, 3.5), (-0.4, 3.5), (-0.5, 1.5), (-0.3, 0.2), (-0.8, -1.5), (-0.9, -2.6), (-0.2, -2.8), (0.9, -3.2),
               (0.9, -3.6), (-2.7, -3.6), (-2.8, -2.7), (-3.2, -1.2), (-3.3, 0.1), (-3.2, 1.6)]
        leg = Polygon(*[leg_xy(x, y) for x, y in pts], stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.3).round_corners(0.3)
        cord = rrect(3.3, 0.6, GREY, 0.35, 3, 0.25).move_to([-1.85, 3.5, 0])
        cord_l = T("spinal cord", 34, GREY).move_to([2.1, 3.5, 0])
        parts = [("hip", (-1.85, 2.9)), ("knee", (-1.8, 0.0)), ("ankle", (-1.7, -2.7))]
        self.play(FadeIn(title), FadeIn(leg), FadeIn(cord), FadeIn(cord_l), run_time=0.6)
        soma = Circle(radius=0.32, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.6).move_to([-1.6, 3.3, 0])
        apts = [(-1.6, 3.3), (-1.75, 1.5), (-1.9, 0.2), (-1.8, -1.5), (-1.7, -2.8), (-1.0, -3.1), (-0.1, -3.1)]
        axon = VMobject(color=BLUE, stroke_width=8).set_points_smoothly([np.array(leg_xy(x, y)) for x, y in apts])
        self.at("a motor axon")
        self.play(GrowFromCenter(soma), run_time=0.4)
        axl = T("motor axon", 34, BLUE).move_to([-5.3, 0.9, 0])
        axl_ld = Line([-3.95, 0.9, 0], [-1.85, 0.75, 0], color=BLUE, stroke_width=2, stroke_opacity=0.8)
        self.play(FadeIn(axl), Create(axl_ld), run_time=0.4)
        self.at("run from")
        self.play(Create(axon), run_time=1.8)
        end = Circle(radius=0.2, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.6).move_to(axon.get_end())
        foot_l = T("foot", 34, GREY).move_to([2.0, -3.1, 0])
        self.play(GrowFromCenter(end), FadeIn(foot_l), run_time=0.3)
        self.at("about a meter")
        ruler = DoubleArrow([4.6, 3.5, 0], [4.6, -3.1, 0], color=TEXT, buff=0, stroke_width=8, tip_length=0.35)
        rl = T("about\n1 metre", 54, TEXT, weight=BOLD).move_to([4.6, 0.2, 0])
        rl.shift(RIGHT * 0.0)
        under = Rectangle(width=rl.width + 0.3, height=rl.height + 0.3, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(rl)
        self.play(GrowFromCenter(ruler), FadeIn(under), FadeIn(rl), run_time=0.8)
        self.finish()


# ============================================================================================
SOMA_C = np.array([-4.4, 0.0, 0.0])
MITO_POS = [(-5.3, 1.2), (-3.5, 1.2), (-5.9, 0.0), (-4.4, 0.0), (-2.9, 0.0), (-5.3, -1.2), (-3.5, -1.2)]
ATP_SPREAD = [(-1.7, 0.0), (-1.0, 0.0), (-0.3, 0.0), (0.4, 0.0), (1.1, 0.0)]


def s05_soma():
    soma = Circle(radius=2.2, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to(SOMA_C)
    lab = T("cell body", 34, BLUE).move_to([-4.4, -2.85, 0])
    ms = VGroup(*[mito(x, y, 1.0, 0.55) for x, y in MITO_POS])
    tube = Rectangle(width=9.5, height=0.5, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.35).move_to([2.55, 0, 0])
    return soma, lab, ms, tube


def s05_question():
    dash = DashedLine([1.8, 0.95, 0], [6.1, 0.95, 0], color=YELLOW, stroke_width=5, dash_length=0.2)
    dash.add_tip(tip_length=0.22)
    q = T("?", 64, YELLOW, weight=BOLD).move_to([6.4, 0.95, 0])
    t1 = T("Pause and predict", 32, YELLOW, weight=BOLD)
    t2 = T("Diffuse all the way?", 40, TEXT)
    g = VGroup(t1, t2).arrange(DOWN, buff=0.15)
    box = rrect(g.width + 0.7, g.height + 0.5, YELLOW, 0.1, 3, 0.2).move_to(g)
    card = VGroup(box, g).move_to([1.8, 2.9, 0])
    return dash, q, card


class S05Q(SpokenScene):
    def construct(self):
        soma, lab, ms, tube = s05_soma()
        self.play(FadeIn(soma), FadeIn(lab), FadeIn(ms), GrowFromEdge(tube, LEFT), run_time=0.6)
        self.at("full of")
        ml = T("mitochondria", 34, YELLOW).move_to([-4.4, 2.8, 0])
        self.play(FadeIn(ml), *[m[0].animate.set_fill(YELLOW, 0.5) for m in ms], run_time=0.8)
        self.at("just make")
        atp_l = chip("ATP", YELLOW, 32).move_to([-1.0, 0.95, 0])
        atps = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, 0, 0]) for x in (-1.9, -1.6, -1.3, -1.0, -0.7)])
        self.play(LaggedStart(*[FadeIn(a, scale=0.4) for a in atps], lag_ratio=0.15), FadeIn(atp_l), run_time=0.9)
        self.at("let it diffuse")
        self.play(*[a.animate.move_to([x, 0, 0]) for a, (x, _) in zip(atps, ATP_SPREAD)], FadeOut(atp_l), FadeOut(ml), run_time=0.6)
        self.at("down the axon")
        dash, q, card = s05_question()
        self.play(Create(dash), FadeIn(q), FadeIn(card, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        soma, lab, ms, tube = s05_soma()
        for m in ms:
            m[0].set_fill(YELLOW, 0.5)
        atps = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, 0, 0]) for x, _ in ATP_SPREAD])
        dash, q, card = s05_question()
        self.add(soma, lab, ms, tube, atps, dash, q, card)
        ring_c = np.array([5.7, -2.2, 0])
        tr = ValueTracker(5.0)
        ring_bg = Circle(radius=0.8, stroke_color=GREY, stroke_width=4, stroke_opacity=0.4).move_to(ring_c)
        ring = always_redraw(lambda: Arc(radius=0.8, start_angle=PI / 2, angle=-TAU * (tr.get_value() / 5.0), arc_center=ring_c, stroke_color=YELLOW, stroke_width=8)
                             if tr.get_value() > 0.02 else VMobject())
        num = always_redraw(lambda: T(str(int(np.ceil(max(tr.get_value(), 0.01)))), 54, YELLOW, weight=BOLD).move_to(ring_c))
        cap = T("think", 34, YELLOW).move_to([5.7, -3.5, 0])
        self.add(ring_bg, ring, num, cap)
        self.play(tr.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        self.finish()


# ============================================================================================
CX0, CW, CLO, CHI = -5.4, 10.8, -3.5, 10.0
ROWY = {"um": 2.15, "mm": 0.85, "cm": -0.45, "m": -1.75}
AXIS_Y = -2.8
YEAR = 3.156e7
TICKS = [(1e-3, "1 ms"), (1.0, "1 s"), (3600.0, "1 hour"), (86400.0, "1 day"), (YEAR, "1 year"), (100 * YEAR, "100 years")]


def px(t):
    return CX0 + (np.log10(t) - CLO) / (CHI - CLO) * CW


def diff_times(L_um):
    """time for ATP to diffuse L (in micrometres): t = L^2 / 2D, D = 150-300 square micrometres per second."""
    return L_um ** 2 / (2 * 300.0), L_um ** 2 / (2 * 150.0)


def clock_axis(nticks):
    line = Line([CX0, AXIS_Y, 0], [CX0 + CW, AXIS_Y, 0], color=GREY, stroke_width=3)
    parts = [line]
    for t, name in TICKS[:nticks]:
        x = px(t)
        low = name == "1 day"       # neighbours "1 hour" and "1 day" sit close: stagger the day label
        parts.append(Line([x, AXIS_Y - 0.1, 0], [x, AXIS_Y + 0.1, 0], color=GREY, stroke_width=3))
        parts.append(T(name, 28, GREY).move_to([x, AXIS_Y - (0.78 if low else 0.38), 0]))
    return VGroup(*parts)


def clock_tracks():
    return VGroup(*[Rectangle(width=CW, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.12).move_to([CX0 + CW / 2, y, 0])
                    for key, y in ROWY.items() if key != "cm"])


def clock_row(key, L_um, name, text):
    y = ROWY[key]
    lo, hi = diff_times(L_um)
    x_lo, x_hi = px(lo), px(hi)
    bar = Rectangle(width=x_lo - CX0, height=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
    bar.move_to([CX0 + bar.width / 2, y, 0])
    ext = Rectangle(width=max(0.05, x_hi - x_lo), height=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.45)
    ext.move_to([x_lo + ext.width / 2, y, 0])
    lab = T(name, 32, TEXT).move_to([CX0, y + 0.58, 0], aligned_edge=LEFT)
    val = T(text, 32, YELLOW).move_to(lab.get_right() + RIGHT * 0.5, aligned_edge=LEFT)
    return lab, VGroup(bar, ext), val


def clock_note():
    return T("10x the distance = 100x the time", 36, TEXT, weight=BOLD).move_to([0, 3.5, 0])


def log_note():
    return T("log scale", 26, GREY).move_to([-1.9, -3.72, 0])


def m_box():
    return Rectangle(width=12.8, height=1.7, stroke_color=YELLOW, stroke_width=4).move_to([0.0, -1.55, 0])


class S07R1(SpokenScene):
    def construct(self):
        ax = clock_axis(3)
        ln = log_note()
        tracks = clock_tracks()
        l1, b1, v1 = clock_row("um", 1, "1 micrometre", "a few milliseconds")
        l2, b2, v2 = clock_row("mm", 1000, "1 millimetre", "about half an hour to an hour")
        self.play(FadeIn(ax), FadeIn(ln), FadeIn(tracks), FadeIn(l1), run_time=0.5)
        self.at("spreads in")
        self.play(GrowFromEdge(b1, LEFT), run_time=0.5)
        self.play(FadeIn(v1), run_time=0.4)
        self.at("over a millimeter")
        self.play(FadeIn(l2), run_time=0.5)
        self.at("takes about")
        self.play(GrowFromEdge(b2, LEFT), run_time=1.3)
        self.play(FadeIn(v2), run_time=0.4)
        self.play(FadeIn(clock_note()), run_time=0.4)
        self.finish()


class S08R2(SpokenScene):
    def construct(self):
        ax = clock_axis(3)
        ln = log_note()
        l1, b1, v1 = clock_row("um", 1, "1 micrometre", "a few milliseconds")
        l2, b2, v2 = clock_row("mm", 1000, "1 millimetre", "about half an hour to an hour")
        l4, b4, v4 = clock_row("m", 1e6, "1 metre", "about 50 to 100 years")
        self.add(clock_tracks(), ax, ln, l1, b1, v1, l2, b2, v2, clock_note())
        extra = VGroup(*clock_axis(6)[1 + 3 * 2:])
        self.at("meter", lead=0.0)
        self.play(FadeIn(l4), FadeIn(extra), run_time=0.4)
        self.at("50 to")
        self.play(GrowFromEdge(b4, LEFT), run_time=1.0)
        self.at("years")
        self.play(Create(m_box()), run_time=0.4)
        self.play(FadeIn(v4), run_time=0.3)
        self.finish()


class S09Beat(NarratedScene):
    def construct(self):
        ax = clock_axis(6)
        l1, b1, v1 = clock_row("um", 1, "1 micrometre", "a few milliseconds")
        l2, b2, v2 = clock_row("mm", 1000, "1 millimetre", "about half an hour to an hour")
        l4, b4, v4 = clock_row("m", 1e6, "1 metre", "about 50 to 100 years")
        self.add(clock_tracks(), ax, log_note(), l1, b1, v1, l2, b2, v2, l4, b4, v4, m_box(), clock_note())
        self.finish()


# ============================================================================================
class S10Local(SpokenScene):
    def construct(self):
        tube = Rectangle(width=14.0, height=4.6, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.16).move_to([0, -0.2, 0])
        axl = T("axon", 34, BLUE, weight=BOLD).move_to([-5.9, 1.65, 0])
        mts = [mito(x, 0.95, 2.3, 1.25) for x in (-4.2, 0.0, 4.2)]
        atps = [chip("ATP", YELLOW, 30).move_to([x, -0.15, 0]) for x in (-4.2, 0.0, 4.2)]
        self.play(GrowFromEdge(tube, LEFT), FadeIn(axl), run_time=0.5)
        self.play(*[FadeIn(m, scale=0.7) for m in mts], *[m[0].animate.set_fill(YELLOW, 0.6) for m in mts],
                  *[FadeIn(a, scale=0.7) for a in atps], run_time=0.5)
        self.at("locally")
        lab = T("made locally", 48, YELLOW, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), run_time=0.5)
        self.at("in its own")
        ml = T("mitochondria", 36, YELLOW).move_to([0.0, 2.65, 0])
        self.play(FadeIn(ml), *[Indicate(m, color=YELLOW, scale_factor=1.12) for m in mts], run_time=0.8)
        self.at("glycolysis")
        def marks(x):
            ds = VGroup(*[Circle(radius=0.27, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95).move_to([x + dx, -1.15 + dy, 0])
                          for dx, dy in ((-0.7, 0.0), (0.0, 0.2), (0.7, 0.0))])
            rg = VGroup(*[Circle(radius=0.44, stroke_color=ORANGE, stroke_width=3, stroke_opacity=0.7).move_to(d) for d in ds])
            return VGroup(ds, rg)
        gm = [marks(x) for x in (-4.2, 0.0, 4.2)]
        gl = T("glycolysis", 40, ORANGE, weight=BOLD).move_to([0, -2.05, 0])
        self.play(*[FadeIn(g, scale=0.5) for g in gm], FadeIn(gl), run_time=0.8)
        self.play(*[Indicate(g, color=ORANGE, scale_factor=1.12) for g in gm], run_time=0.6)
        self.finish()


# ============================================================================================
SEG_X = [-5.0, -2.5, 0.0, 2.5, 5.0]


def break_mark(c):
    s = 0.22
    a = Line(c + np.array([-0.18 - s * 0.4, -s, 0]), c + np.array([-0.18 + s * 0.4, s, 0]), color=TEXT, stroke_width=4)
    b = Line(c + np.array([0.18 - s * 0.4, -s, 0]), c + np.array([0.18 + s * 0.4, s, 0]), color=TEXT, stroke_width=4)
    return VGroup(a, b)


class S11Cover(SpokenScene):
    def construct(self):
        title = fact_label("3. Cover", (-5.6, 3.5))
        AY = 1.35
        axon = Rectangle(width=14.0, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([0, AY, 0])
        axl = T("axon", 34, BLUE, weight=BOLD).move_to([-6.0, AY - 1.0, 0])
        axl_ld = Line([-6.0, AY - 0.7, 0], [-6.0, AY - 0.25, 0], color=BLUE, stroke_width=3)
        self.play(FadeIn(title), GrowFromEdge(axon, LEFT), FadeIn(axl), Create(axl_ld), run_time=0.5)
        segs = VGroup(*[myelin_block(2.36, 1.6, 0.35).move_to([x, AY, 0]) for x in SEG_X])
        brk = VGroup(*[break_mark(np.array([x, AY, 0])) for x in SEG_X])
        self.at("myelinated")
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.9) for s in segs], lag_ratio=0.4), run_time=1.4)
        self.play(FadeIn(brk), run_time=0.3)
        self.at("spinal cord")
        gx = (SEG_X[0] + SEG_X[1]) / 2
        node_marks = VGroup(*[Rectangle(width=0.12, height=0.5, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to([(a + b) / 2, AY, 0])
                              for a, b in zip(SEG_X[:-1], SEG_X[1:])])
        my_l = T("myelin", 34, TEXT, weight=BOLD).move_to([SEG_X[0], AY + 1.25, 0])
        nd_l = T("node", 34, TEXT, weight=BOLD).move_to([gx, AY - 1.35, 0])
        nd_ld = Line([gx, AY - 1.05, 0], [gx, AY - 0.3, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(node_marks), FadeIn(my_l), FadeIn(nd_l), Create(nd_ld), run_time=0.5)
        self.at("myelin covers")
        mx0, mw, my = -6.4, 8.8, -1.75
        meter = Rectangle(width=mw, height=1.0, stroke_color=GREY, stroke_width=3).move_to([mx0 + mw / 2, my, 0])
        fillw = mw * 0.985
        fill = Rectangle(width=fillw, height=1.0, stroke_width=0, fill_color=GREY, fill_opacity=0.75).move_to([mx0 + fillw / 2, my, 0])
        ml = T("covered by myelin", 34, GREY).move_to([mx0, my + 0.85, 0], aligned_edge=LEFT)
        self.play(Create(meter), FadeIn(ml), run_time=0.3)
        self.play(GrowFromEdge(fill, LEFT), run_time=0.7)
        self.at("98 to 99")
        val = M("98 to 99%", 50, TEXT, weight=BOLD).move_to([2.7, my, 0], aligned_edge=LEFT)
        self.play(FadeIn(val), run_time=0.3)
        self.at("percent", lead=1.2)
        sub = T("one myelinated stretch; real axons vary", 34, GREY).move_to([0, -2.85, 0])
        scale = T("not to scale: node 1 micrometre, internode 50 to 100", 32, GREY).move_to([0, -3.5, 0])
        self.play(FadeIn(sub), FadeIn(scale), run_time=0.5)
        self.finish()


# ============================================================================================
class S12Limit(SpokenScene):
    def construct(self):
        axon = Rectangle(width=14.6, height=1.3, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.4).move_to([0, 0, 0])
        def sheath(x0, x1, y0, y1):
            return myelin_block(x1 - x0, y1 - y0, 0.25).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        sheaths = VGroup(sheath(-7.6, -2.2, 0.88, 2.7), sheath(-7.6, -2.2, -2.7, -0.88),
                         sheath(2.2, 7.6, 0.88, 2.7), sheath(2.2, 7.6, -2.7, -0.88))
        spaces = VGroup(*[Rectangle(width=5.4, height=0.2, stroke_width=0, fill_color=TEXT, fill_opacity=0.3).move_to([cx, y, 0])
                          for cx in (-4.9, 4.9) for y in (0.75, -0.75)])
        axl = T("axon", 34, BLUE, weight=BOLD).move_to([-5.0, 0, 0])
        myl = T("myelin", 34, TEXT, weight=BOLD).move_to([-4.8, 1.8, 0])
        self.play(FadeIn(axon), FadeIn(sheaths), FadeIn(spaces), FadeIn(axl), FadeIn(myl), run_time=0.5)
        self.at("nodes")
        node_l = T("node", 40, BLUE, weight=BOLD).move_to([0, -1.9, 0])
        glow = Rectangle(width=4.4, height=1.3, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to([0, 0, 0])
        na = arr([0, -1.4, 0], [0, -0.7, 0], BLUE, 5)
        self.play(FadeIn(glow), FadeIn(node_l), GrowArrow(na), run_time=0.6)
        self.at("the axon meets the fluid")
        fl = T("fluid outside", 34, TEXT).move_to([-1.9, 3.4, 0])
        fa = arr([0, 3.3, 0], [0, 0.75, 0], TEXT, 9, 0.4)
        self.play(FadeIn(fl), GrowArrow(fa), run_time=0.8)
        self.at("mainly there")
        self.play(Indicate(glow, color=BLUE, scale_factor=1.06), run_time=0.8)
        self.at("myelin is not")
        ts1 = T("thin space under sheath", 32, TEXT).move_to([4.0, 3.4, 0])
        ts2 = T("thin space under sheath", 32, TEXT).move_to([4.0, -3.4, 0])
        l1 = Line([3.2, 3.1, 0], [3.2, 0.8, 0], color=TEXT, stroke_width=3)
        l2 = Line([3.2, -3.1, 0], [3.2, -0.8, 0], color=TEXT, stroke_width=3)
        self.play(spaces.animate.set_fill(TEXT, 0.85), FadeIn(ts1), FadeIn(ts2), Create(l1), Create(l2), run_time=0.8)
        self.at("but it limits")
        lim = T("limits, not seals", 44, YELLOW, weight=BOLD).move_to([-3.6, -3.35, 0])
        self.play(FadeIn(lim, shift=UP * 0.15), run_time=0.6)
        self.at("access", lead=0.5)
        # glucose streams into the node; a couple stall at the sheath edge
        pts = [(-1.5, 2.9), (-0.8, 2.5), (0.8, 2.6), (1.5, 3.0), (0.4, 2.2)]
        parts = VGroup(*[Circle(radius=0.22, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.9).move_to([x, y, 0]) for x, y in pts])
        stalled = VGroup(*[Circle(radius=0.14, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.9).move_to([x, 1.05, 0]) for x in (-1.95, 1.95)])
        self.play(FadeIn(parts, scale=0.5), FadeIn(stalled), run_time=0.25)
        self.play(*[p.animate.move_to([x * 0.7, 0.95, 0]) for i, (p, (x, _)) in enumerate(zip(parts, pts))], run_time=0.7)
        self.at("glucose")
        gl = T("glucose", 32, TEXT, weight=BOLD).move_to([-0.4, 1.95, 0], aligned_edge=RIGHT)
        self.play(FadeIn(gl), run_time=0.4)
        self.play(parts.animate.set_opacity(0.0), run_time=0.7)
        self.finish()


# ============================================================================================
S13_X = [-4.3, 0.0, 4.3]


class S13Who(SpokenScene):
    def construct(self):
        AY = -1.55
        axon = Rectangle(width=13.4, height=0.65, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([0, AY, 0])
        segs = VGroup(*[myelin_block(3.8, 2.5, 0.4).move_to([x, AY, 0]) for x in S13_X])
        axl = T("axon", 36, BLUE, weight=BOLD).move_to([-2.15, -3.3, 0])
        axl_ld = Line([-2.15, -2.95, 0], [-2.15, AY - 0.3, 0], color=BLUE, stroke_width=3)
        self.play(FadeIn(axon), FadeIn(segs), FadeIn(axl), Create(axl_ld), run_time=0.5)
        self.at("the cell touching")
        cell = Ellipse(width=4.6, height=2.0, stroke_color=TEAL, stroke_width=4,
                       fill_color=TEAL, fill_opacity=0.2).move_to([0, 2.45, 0])
        lab = T("one glial cell", 38, TEAL).move_to(cell)
        arms = VGroup(*[CubicBezier(np.array([x * 0.32, 1.8, 0]),
                    np.array([x * 0.65, 1.0, 0]), np.array([x, 0.65, 0]),
                    np.array([x, AY + 1.25, 0]), stroke_color=TEAL, stroke_width=10) for x in S13_X])
        self.play(FadeIn(cell), FadeIn(lab), run_time=0.5)
        self.at("the axon")
        self.play(Create(arms), run_time=0.7)
        self.at("made its myelin")
        cap = T("wraps made by this cell", 34, TEAL, weight=BOLD).move_to([2.5, -3.3, 0])
        self.play(*[seg.animate.set_stroke(TEAL).set_fill(TEAL_MYELIN, 1) for seg in segs], FadeIn(cap), run_time=0.7)
        self.play(Indicate(segs, color=TEAL, scale_factor=1.03), run_time=0.6)
        self.finish()


# ============================================================================================
class S14Sheet(SpokenScene):
    def construct(self):
        cx, cy = 3.0, -0.2
        R0, R1 = 1.75, 3.15
        axon = Circle(radius=1.55, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to([cx, cy, 0])
        axl = T("axon", 36, BLUE, weight=BOLD).move_to([cx, cy, 0])
        cell = Ellipse(width=4.6, height=3.6, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.2).move_to([-4.4, 0.9, 0])
        cell_l = T("glial cell", 36, TEAL).move_to([-4.4, 1.3, 0])
        view = T("cross-section", 36, GREY).move_to([cx, 3.55, 0])
        strand = CubicBezier(np.array([-2.15, 0.3, 0]), np.array([-1.3, 0.1, 0]), np.array([-0.8, cy, 0]), np.array([cx - R1, cy, 0]),
                             stroke_color="#8FE3E9", stroke_width=16, stroke_opacity=1.0)
        st_l = T("cytoplasm stays\nconnected", 34, "#8FE3E9").move_to([-1.9, -2.1, 0])
        st_ld = Line([-1.7, -1.55, 0], [-1.25, -0.1, 0], color="#8FE3E9", stroke_width=3)

        def spiral(t):
            tt = 6 * np.pi - t
            r = R0 + (R1 - R0) * tt / (6 * np.pi)
            return np.array([cx + r * np.cos(tt + np.pi), cy + r * np.sin(tt + np.pi), 0])
        wrap = ParametricFunction(spiral, t_range=[0, 6 * np.pi, 0.05], color=TEAL, stroke_width=11)
        self.play(FadeIn(cell), FadeIn(cell_l), FadeIn(axon), FadeIn(axl), FadeIn(view), run_time=0.5)
        self.at("sheet of one")
        self.play(Create(strand), run_time=0.6)
        self.play(FadeIn(st_l), Create(st_ld), run_time=0.4)
        self.at("glial cell's")
        self.play(Indicate(cell, color=TEAL, scale_factor=1.04), run_time=0.6)
        self.at("wound around")
        self.play(Create(wrap), run_time=1.5, rate_func=linear)
        my_l = T("myelin", 36, TEAL, weight=BOLD).move_to([cx + 2.9, -3.3, 0])
        self.play(FadeIn(my_l), Indicate(wrap, color=TEAL, scale_factor=1.02), run_time=0.5)
        self.finish()


# ============================================================================================
class S15Oligo(SpokenScene):
    def construct(self):
        div = DashedLine([0, 3.9, 0], [0, -3.9, 0], color=GREY, stroke_width=2)
        h1 = T("CNS: one oligodendrocyte", 34, TEAL, weight=BOLD).move_to([-3.4, 3.45, 0])
        fit(h1, max_w=6.5)
        # CNS panel: round body on the left, three axons to the right edge of the panel
        body1 = Circle(radius=1.0, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.25).move_to([-5.6, 0, 0])
        ys = (2.0, 0.0, -2.0)
        axons = VGroup(*[Arrow([-3.6, y, 0], [-0.45, y, 0], buff=0, color=BLUE, stroke_width=14, tip_length=0.3) for y in ys])
        segs = VGroup(*[myelin_block(1.7, 1.15, 0.3, True).move_to([-2.4, y, 0]) for y in ys])
        arms = VGroup(*[Line(body1.get_center() + 0.95 * np.array([0.8, 0.6 * np.sign(y), 0]) * (1 if y else 1.0), [-3.25, y, 0], color=TEAL, stroke_width=9) for y in ys])
        self.play(FadeIn(div), FadeIn(h1), FadeIn(body1), FadeIn(axons), run_time=0.5)
        self.at("segments on")
        self.play(LaggedStart(*[AnimationGroup(Create(a), GrowFromCenter(s)) for a, s in zip(arms, segs)], lag_ratio=0.25), run_time=0.8)
        self.at("many axons")
        many = T("many axons, many segments", 36, TEAL).move_to([-3.4, -3.45, 0])
        self.play(Indicate(axons, color=BLUE, scale_factor=1.04), FadeIn(many), run_time=0.7)
        self.at("a myelinating schwann")
        h2 = T("PNS: one Schwann cell", 34, TEAL, weight=BOLD).move_to([3.4, 3.45, 0])
        body2 = Ellipse(width=1.3, height=2.8, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.25).move_to([1.3, 0, 0])
        ax2 = Arrow([3.3, 0, 0], [6.5, 0, 0], buff=0, color=BLUE, stroke_width=14, tip_length=0.3)
        self.play(FadeIn(h2), FadeIn(body2), FadeIn(ax2), run_time=0.6)
        self.at("makes just")
        seg2 = myelin_block(1.7, 1.15, 0.3, True).move_to([4.5, 0, 0])
        arm2 = Line([1.95, 0, 0], [3.65, 0, 0], color=TEAL, stroke_width=9)
        self.play(Create(arm2), GrowFromCenter(seg2), run_time=0.7)
        one = T("one segment", 40, TEAL, weight=BOLD).move_to([3.4, -3.45, 0])
        self.play(FadeIn(one), run_time=0.4)
        self.finish()


# ============================================================================================
class S16Idea(SpokenScene):
    def construct(self):
        box = rrect(12.4, 7.0, GOLD, 0.06, 3, 0.3).move_to([0, 0, 0])
        lab = T("The one idea of this lesson", 44, GOLD, weight=BOLD).move_to([0, 2.8, 0])
        g = chip("wrapping glia", TEAL, 40).move_to([-3.6, -2.5, 0])
        a = chip("axon", BLUE, 40).move_to([3.6, -2.5, 0])
        ar = arr(g.get_right() + RIGHT * 0.15, a.get_left() + LEFT * 0.15, GREY, 7)
        self.play(FadeIn(box), FadeIn(lab), FadeIn(g), FadeIn(a), GrowArrow(ar), run_time=0.5)
        self.at("whoever")
        l1 = Text("Whoever wraps the axon", font=TITLE_FONT, font_size=62, color=TEXT, t2c={"wraps": TEAL, "axon": BLUE}).move_to([0, 1.0, 0])
        self.play(Write(l1), run_time=0.9)
        self.at("helps feed")
        l2 = Text("helps feed it.", font=TITLE_FONT, font_size=62, color=TEXT).move_to([0, -0.4, 0])
        self.play(Write(l2), run_time=0.6)
        self.play(Indicate(ar, color=TEAL, scale_factor=1.1), run_time=0.5)
        self.finish()
        self.wait(2.0)  # silent reading time after the narration


# ============================================================================================
GLIA_C = np.array([0, 2.1, 0]); GLIA_W, GLIA_H = 12.4, 3.0
AX_C = np.array([0, -2.15, 0]); AX_W, AX_H = 12.4, 3.0
GATE_X = -1.5; GATE_Y = -0.02


class S17How(SpokenScene):
    def construct(self):
        glia = rrect(GLIA_W, GLIA_H, TEAL, 0.14, 4, 0.7).move_to(GLIA_C)
        ax = rrect(AX_W, AX_H, BLUE, 0.14, 4, 0.7).move_to(AX_C)
        gl = T("oligodendrocyte", 34, TEAL, weight=BOLD).move_to([-3.6, 3.1, 0])
        al = T("axon", 34, BLUE, weight=BOLD).move_to([-4.9, -1.15, 0])
        g = gate(GATE_X, GATE_Y, BLUE, 1.25)
        m1 = T("MCT1", 34, TEXT, weight=BOLD)
        m2 = T("(thought to export fuel)", 30, GREY)
        mct = VGroup(m1, m2).arrange(RIGHT, buff=0.2).move_to([0.5, GATE_Y, 0], aligned_edge=LEFT)
        mct.move_to([-0.4 + mct.width / 2, GATE_Y, 0])
        self.play(FadeIn(ax), FadeIn(al), FadeIn(glia), FadeIn(gl), FadeIn(g), FadeIn(mct), run_time=0.6)
        self.at("made its myelin")
        mye = chip("has made its myelin", GREY, 30).move_to([-3.4, 2.15, 0])
        self.play(FadeIn(mye, shift=UP * 0.1), run_time=0.5)
        self.at("live on")
        gly = chip("glycolysis", ORANGE, 30).move_to([-4.4, 1.1, 0])
        self.play(FadeIn(gly, shift=UP * 0.1), run_time=0.5)
        self.at("glycolysis")
        self.play(Indicate(gly, color=ORANGE, scale_factor=1.2), run_time=0.9)
        self.at("the evidence fits")
        h = DashedLine([-3.1, 1.1, 0], [GATE_X, 1.1, 0], color=YELLOW, stroke_width=5, dash_length=0.2)
        v = DashedLine([GATE_X, 1.1, 0], [GATE_X, -1.6, 0], color=YELLOW, stroke_width=5, dash_length=0.2)
        v.add_tip(tip_length=0.22)
        inf = T("inferred", 32, YELLOW).move_to([-0.2, 1.1, 0], aligned_edge=LEFT)
        mt = mito(3.7, -2.65, 3.0, 1.5)
        mtl = T("mitochondrion", 32, YELLOW).move_to([3.7, -1.15, 0])
        self.play(Create(h), FadeIn(inf), FadeIn(mt), FadeIn(mtl), run_time=0.5)
        self.play(Create(v), run_time=0.4)
        self.at("passing")
        lac = solid_chip("lactate", ORANGE, 38).move_to([-2.1, 1.1, 0])
        self.play(FadeIn(lac, scale=0.6), run_time=0.25)
        self.play(lac.animate.move_to([GATE_X, 1.1, 0]), run_time=0.4)
        self.play(lac.animate.move_to([GATE_X, -1.4, 0]), run_time=0.7)
        self.at("pyruvate")
        pyr = solid_chip("pyruvate", ORANGE, 38).move_to([GATE_X, -1.4, 0])
        ldh = T("LDH", 36, TEXT, weight=BOLD).move_to([0.25, -0.95, 0])
        lac_key = solid_chip("lactate", ORANGE, 34).move_to([-4.1, -1.65, 0])
        conversion = arr([-2.85, -1.65, 0], [-0.95, -1.65, 0], ORANGE, 6)
        pyr.move_to([0.5, -1.65, 0])
        self.play(ReplacementTransform(lac, pyr), FadeIn(ldh), FadeIn(lac_key), GrowArrow(conversion), run_time=0.5)
        self.at("to the axon")
        entry = arr([1.85, -1.85, 0], [2.7, -2.4, 0], ORANGE, 6)
        fuel = pyr.copy()
        self.add(fuel)
        self.play(GrowArrow(entry), fuel.animate.move_to([3.7, -2.65, 0]).scale(0.7),
                  mt[0].animate.set_fill(YELLOW, 0.6), run_time=0.8)
        # Keep the complete lactate -> LDH -> pyruvate -> mitochondrion chain
        # visible through the transporter explanation, over three seconds.
        self.at("loses MCT1")
        x = cross(np.array([GATE_X, GATE_Y, 0]), RED, 0.5)
        self.play(g.animate.set_color(RED), FadeIn(x), m1.animate.set_color(RED), run_time=0.5)
        self.play(FadeOut(h), FadeOut(v), FadeOut(inf), mt.animate.set_opacity(0.3), mtl.animate.set_opacity(0.4), run_time=0.7)
        self.at("transporter thought")
        self.play(Indicate(g, color=RED, scale_factor=1.15), Indicate(mct, color=RED, scale_factor=1.05), run_time=1.0)
        # timeline: young and old states of the same axon
        self.at("carry that")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.35)
        cause = T("glial MCT1 removed, mice", 42, RED, weight=BOLD).move_to([0, 3.5, 0])
        yl = T("young axon: intact", 40, GREEN, weight=BOLD).move_to([-6.4, 2.6, 0], aligned_edge=LEFT)
        yb = Rectangle(width=12.8, height=1.5, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.55).move_to([0, 1.5, 0])
        ol = T("same axon, older", 40, GREY, weight=BOLD).move_to([-6.4, -0.85, 0], aligned_edge=LEFT)
        old = yb.copy().move_to([0, -2.2, 0])
        # A single continuous bar first, then irregular cracks in that same bar.
        cracks = VGroup(*[Polygon([x - .14, -1.45, 0], [x + .12, -1.95, 0],
                     [x - .08, -2.4, 0], [x + .2, -2.95, 0],
                     [x + .38, -2.95, 0], [x + .1, -2.4, 0],
                     [x + .3, -1.95, 0], [x + .04, -1.45, 0],
                     stroke_width=0, fill_color=BG, fill_opacity=1)
                     for x in (-4.5, -1.8, 1.4, 4.1)])
        tarrow = arr([0, 0.65, 0], [0, -0.3, 0], GREY, 7)
        self.play(FadeIn(cause), FadeIn(yl), FadeIn(yb), FadeIn(ol), FadeIn(old), GrowArrow(tarrow), run_time=0.5)
        self.at("axons degenerate")
        dl = T("old axon: degenerated", 40, RED, weight=BOLD).move_to([-6.4, -0.85, 0], aligned_edge=LEFT)
        self.play(old.animate.set_stroke(RED).set_fill(RED, 0.6), FadeIn(cracks),
                  ReplacementTransform(ol, dl), run_time=1.0)
        self.at("mice age")
        sl = T("slowly, late", 44, YELLOW, weight=BOLD).move_to([0.5, 0.15, 0], aligned_edge=LEFT)
        self.play(FadeIn(sl, shift=RIGHT * 0.2), Indicate(tarrow, color=YELLOW, scale_factor=1.2), run_time=0.6)
        self.finish()


# ============================================================================================
def spikes(x0, y0, w, h, n=3):
    """a short train of action potentials, computed from a simple spike shape."""
    xs = np.linspace(0, 1, 400)
    ys = np.zeros_like(xs)
    for k in range(n):
        c = (k + 0.5) / n
        ys += np.exp(-((xs - c) / (0.22 / n)) ** 2) - 0.25 * np.exp(-((xs - c - 0.35 / n) / (0.4 / n)) ** 2)
    pts = [[x0 + w * x, y0 + h * y * 0.5, 0] for x, y in zip(xs, ys)]
    return VMobject(color=YELLOW, stroke_width=5).set_points_smoothly(pts)


class S18Scope(SpokenScene):
    def construct(self):
        TX = -1.6
        title = T("The rule has limits", 44, GOLD, weight=BOLD).move_to([0, 3.5, 0])
        # row 1 (shown from the start)
        y1 = 2.2
        ic1 = VGroup(Rectangle(width=4.4, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.9),
                     myelin_block(2.4, 1.5, 0.3, True)).move_to([-4.5, y1, 0])
        t1 = T("Clearest for oligodendrocytes", 42, TEXT).move_to([TX, y1 + 0.35, 0], aligned_edge=LEFT)
        s1 = T("the glia that have made their myelin", 30, GREY).move_to([TX, y1 - 0.35, 0], aligned_edge=LEFT)
        panels = VGroup(rrect(13.0, 1.7, GREY, 0.04, 2, 0.3).move_to([0, 2.2, 0]), rrect(13.0, 1.9, GREY, 0.04, 2, 0.3).move_to([0, 0.45, 0]),
                        rrect(13.0, 2.7, GREY, 0.04, 2, 0.3).move_to([0, -2.3, 0]))
        for p_ in panels:
            p_.set_stroke(opacity=0.35)
        self.play(FadeIn(title), FadeIn(panels[0]), FadeIn(ic1), FadeIn(t1), FadeIn(s1), run_time=0.5)
        # row 2
        y2 = 0.6
        ic2 = VGroup(Arrow([-6.7, y2 + 0.1, 0], [-2.4, y2 + 0.1, 0], buff=0, color=GREY, stroke_width=10, tip_length=0.3),
                     T("years", 30, GREY).move_to([-4.5, y2 - 0.45, 0]))
        t2 = T("and for long-term upkeep", 42, TEXT).move_to([TX, y2 + 0.4, 0], aligned_edge=LEFT)
        self.at("and for long term")
        self.play(FadeIn(panels[1]), FadeIn(ic2), FadeIn(t2), run_time=0.6)
        self.at("the experiments do not")
        sp = spikes(4.4, y2 - 0.45, 2.3, 1.1, 3)
        s2 = T("each impulse: not measured;\nhelp not ruled out", 30, GREY).move_to([TX, y2 - 0.35, 0], aligned_edge=LEFT)
        self.play(FadeIn(s2), Create(sp), run_time=0.9)
        self.at("rule out")
        self.play(Indicate(sp, color=YELLOW, scale_factor=1.15), run_time=0.8)
        # Row 3 arrives complete with its first spoken words.
        self.at("and it is help")
        t3 = T("Help, not the only supply", 38, TEXT).move_to([0, -1.35, 0])
        ax3 = Rectangle(width=6.0, height=0.55, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([-2.6, -3.05, 0])
        blocks = VGroup(myelin_block(1.9, 1.1, 0.3, True).move_to([-4.6, -3.05, 0]),
                        myelin_block(1.9, 1.1, 0.3, True).move_to([-0.6, -3.05, 0]))
        a_help = arr([-4.6, -2.0, 0], [-4.6, -2.48, 0], TEAL, 8, .3)
        h_l = T("glia help", 30, TEAL, weight=BOLD).move_to([-4.6, -1.8, 0])
        a_glu = arr([-2.6, -2.0, 0], [-2.6, -2.77, 0], TEXT, 8, .3)
        g_l = T("glucose", 30, TEXT, weight=BOLD).move_to([-2.3, -1.8, 0])
        node_l = T("node", 30, BLUE, weight=BOLD).move_to([-2.6, -3.65, 0])
        s3 = T("The axon also takes in\nglucose at a node", 32, GREY).move_to([3.5, -2.7, 0])
        self.play(FadeIn(panels[2]), FadeIn(t3), FadeIn(ax3), FadeIn(blocks),
                  GrowArrow(a_help), FadeIn(h_l), GrowArrow(a_glu), FadeIn(g_l),
                  FadeIn(node_l), FadeIn(s3), run_time=0.6)
        self.at("not the only")
        self.play(Indicate(a_glu, color=TEXT, scale_factor=1.15), run_time=0.5)
        self.finish()
        self.wait(2.0)


# ============================================================================================
class S19Take(SpokenScene):
    def construct(self):
        head = T("Keep three facts together", 44, GOLD, weight=BOLD).move_to([0, 3.5, 0])
        xs = [-4.6, 0.0, 4.6]
        yi = 1.1
        slots = VGroup(*[rrect(4.3, 5.4, GREY, 0.05, 2, 0.3).move_to([x, 0.4, 0]) for x in xs])
        nums = VGroup(*[T(str(i + 1), 140, GOLD, weight=BOLD).move_to([x, 0.6, 0]).set_opacity(0.45) for i, x in enumerate(xs)])
        self.play(FadeIn(head), FadeIn(slots), FadeIn(nums), run_time=0.5)
        # 1 pump
        px0 = xs[0]
        pump = VGroup(rrect(1.3, 0.7, GREY, 0.4, 3, 0.1).move_to([px0 - 1.5, yi, 0]), rrect(1.3, 0.7, GREY, 0.4, 3, 0.1).move_to([px0 + 1.5, yi, 0]),
                      rrect(1.7, 2.7, BLUE, 0.5, 3, 0.2).move_to([px0, yi, 0]),
                      arr([px0, yi - 1.0, 0], [px0, yi + 1.1, 0], TEXT, 7),
                      chip("ATP", YELLOW, 32).move_to([px0, yi - 1.75, 0]))
        c1 = T("pumps keep\nspending", 36, TEXT).move_to([xs[0], -1.75, 0])
        self.at("the pumps keep")
        self.play(FadeIn(pump), FadeIn(c1), FadeOut(nums[0]), run_time=0.7)
        # 2 ruler
        soma = Circle(radius=0.6, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to([xs[1] - 1.55, yi, 0])
        end = Circle(radius=0.22, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.5).move_to([xs[1] + 1.75, yi, 0])
        tube = Line([xs[1] - 0.95, yi, 0], [xs[1] + 1.55, yi, 0], color=BLUE, stroke_width=9)
        ruler = DoubleArrow([xs[1] - 1.55, yi - 1.0, 0], [xs[1] + 1.75, yi - 1.0, 0], color=GREY, buff=0, stroke_width=6, tip_length=0.25)
        rl = T("1 m", 44, TEXT, weight=BOLD).move_to([xs[1], yi + 0.95, 0])
        ruler_g = VGroup(soma, tube, end, ruler, rl)
        c2 = T("cell body\nis far away", 36, TEXT).move_to([xs[1], -1.75, 0])
        self.at("the cell body")
        self.play(FadeIn(ruler_g), FadeIn(c2), FadeOut(nums[1]), run_time=0.7)
        # 3 wrap
        ax = Rectangle(width=4.0, height=0.45, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([xs[2], yi, 0])
        wraps = VGroup(*[myelin_block(1.1, 2.7, 0.3).move_to([xs[2] + dx, yi, 0]) for dx in (-1.3, 0.0, 1.3)])
        c3 = T("myelin covers\nalmost all", 36, TEXT).move_to([xs[2], -1.75, 0])
        self.at("myelin covers")
        self.play(FadeIn(ax), LaggedStart(*[FadeIn(w, shift=DOWN * 0.5) for w in wraps], lag_ratio=0.3), FadeIn(c3), FadeOut(nums[2]), run_time=1.0)
        self.at("the wrapping cell", lead=0.5)
        take = T("The wrapping cell is placed to help feed the axon.", 40, TEAL, weight=BOLD)
        fit(take, max_w=11.8)
        take.move_to([0, -3.3, 0])
        box = rrect(take.width + 0.6, take.height + 0.5, TEAL, 0.1, 3, 0.2).move_to(take)
        self.play(*[w.animate.set_stroke(TEAL).set_fill(TEAL_MYELIN, 1) for w in wraps], FadeIn(box), FadeIn(take, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S20End(EndCard):
    LINE = "The wrapping cell is placed to help feed the axon."
