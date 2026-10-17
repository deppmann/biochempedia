"""Adhesion turns flow into advance  (Biochemistrypedia explainer, growth cone lesson)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the actin network (the engine); the growth cone's fill
  TEAL   = newly added actin at the leading edge ("addition")
  RED    = retrograde flow, myosin pull, removed actin (backward / loss)
  YELLOW = adhesion molecules, the clutch
  GREEN  = advance of the edge
  PURPLE = microtubules
  ORANGE = the guidance cue
  GREY   = substrate, outlines, markers, de-emphasized
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
OUTLINE = "#AEB6C4"

BASE = -1.5      # underside of the growth cone (side view)
SUBY = -1.95     # the substrate
H = 3.6          # height of the flat fan in the side view
HS = 0.9         # height of the axon shaft
XL = -6.1        # left end of the drawn axon
LMAX = 4.2       # how far behind the edge the actin network reaches
A_RATE = 0.30    # actin addition at the edge
F_OFF = 0.30     # retrograde flow with the clutch off
F_ON = 0.20      # retrograde flow with the clutch on


def prof(x, edge, sh, H=H, ramp=1.4, w=1.3):
    """Height of the side-view cone at x."""
    if x <= sh:
        h = HS
    elif x < sh + ramp:
        s = (x - sh) / ramp
        s = s * s * (3 - 2 * s)
        h = HS + (H - HS) * s
    else:
        h = H
    if x > edge - w:
        u = (x - (edge - w)) / w
        h *= math.sqrt(max(0.0, 1 - u * u))
    return h


def P(x, y):
    return np.array([x, y, 0.0])


def arrow(a, b, color, w=8, tip=0.25):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=20)


class Cone:
    """Side view of a growth cone on the substrate. One object drives all the motion."""

    def __init__(self, edge=1.6, A=A_RATE, clutch=0.0, links=0.0, sh=-5.0, tip=-4.0, lock=False,
                 dash_op=1.0, flow_op=1.0, adv_op=0.0, mt_op=0.0, seed=4, h=H):
        self.h = h
        self.edge, self.A = ValueTracker(edge), ValueTracker(A)
        self.clutch, self.links = ValueTracker(clutch), ValueTracker(links)
        self.sh, self.tip = ValueTracker(sh), ValueTracker(tip)
        self.dash_op, self.flow_op = ValueTracker(dash_op), ValueTracker(flow_op)
        self.adv_op, self.mt_op = ValueTracker(adv_op), ValueTracker(mt_op)
        self.lock = lock
        rng = random.Random(seed)
        n = 40
        self.d = [(i + rng.random() * 0.7) / n * LMAX for i in range(n)]
        self.r = [0.12 + 0.76 * ((i * 0.618034) % 1.0) for i in range(n)]
        self.ang = [rng.uniform(-0.6, 0.6) for _ in range(n)]
        self.fill = VMobject(fill_color=BLUE, fill_opacity=0.10, stroke_width=0)
        self.outline = VMobject(stroke_color=OUTLINE, stroke_width=4, fill_opacity=0)
        self.dashes = VGroup(*[VMobject() for _ in range(n)])
        self.mts = VGroup(*[VMobject() for _ in range(4)])
        self.flow = VGroup(*[arrow(P(0, 0), P(-1, 0), RED) for _ in range(3)])
        self.adv = arrow(P(0, 0), P(1, 0), GREEN, w=12, tip=0.32)
        self.linkset = VGroup()
        self.link_x = [-4.0 + 0.8 * k for k in range(14)]
        for x in self.link_x:
            ln = Line(P(x, SUBY), P(x, BASE), color=YELLOW, stroke_width=5)
            d1 = Dot(P(x, SUBY), radius=0.09, color=YELLOW)
            d2 = Dot(P(x, BASE), radius=0.09, color=YELLOW)
            self.linkset.add(VGroup(ln, d1, d2))
        self.substrate = Line(P(-6.3, SUBY), P(6.3, SUBY), color=GREY, stroke_width=7)
        self.shell = VGroup(self.fill, self.outline, self.substrate)
        self.inner = VGroup(self.mts, self.dashes, self.linkset, self.flow, self.adv)
        self.driver = Mobject()
        self.driver.add_updater(lambda m, dt: self.step(dt))
        self.refresh()

    @property
    def Fv(self):
        return F_OFF + (F_ON - F_OFF) * self.clutch.get_value()

    def step(self, dt):
        A = self.A.get_value()
        if not self.lock:
            self.edge.increment_value((A - self.Fv) * dt)
        self.d = [(d + A * dt) % LMAX for d in self.d]
        self.refresh()

    def attach(self, scene):
        scene.add(self.fill, self.mts, self.dashes, self.linkset, self.flow, self.adv, self.outline,
                  self.substrate, self.driver)

    def refresh(self):
        edge = self.edge.get_value()
        sh = self.sh.get_value()
        xs = np.linspace(XL, edge, 220)
        top = [P(x, BASE + prof(x, edge, sh, self.h)) for x in xs]
        closed = top + [P(edge, BASE), P(XL, BASE)]
        self.fill.set_points_as_corners(closed)
        self.outline.set_points_as_corners(closed)
        dop = self.dash_op.get_value()
        for i, dash in enumerate(self.dashes):
            d = self.d[i]
            x = edge - 0.15 - d
            y = BASE + self.r[i] * prof(x, edge, sh, self.h)
            v = np.array([math.cos(self.ang[i]), math.sin(self.ang[i]), 0]) * 0.18
            dash.set_points_as_corners([P(x, y) - v, P(x, y) + v])
            col = interpolate_color(ManimColor(TEAL), ManimColor(BLUE), min(1.0, d / 1.2))
            op = min(1.0, d / 0.25) * min(1.0, (LMAX - d) / 0.7) * dop
            dash.set_stroke(col, width=5.5, opacity=op)
        fop = self.flow_op.get_value()
        L = max(0.45, self.Fv * 4.5)
        for k, a in enumerate(self.flow):
            x0 = edge - 1.3 - 0.35 * k
            y = BASE + self.h * (0.25 + 0.25 * k)
            a.become(arrow(P(x0, y), P(x0 - L, y), RED))
            a.set_opacity(fop)
        adv = (self.A.get_value() - self.Fv) * 10
        aop = self.adv_op.get_value() if adv > 0.25 else 0.0
        self.adv.become(arrow(P(edge + 0.12, BASE + 0.33 * self.h), P(edge + 0.12 + max(adv, 0.3), BASE + 0.33 * self.h), GREEN, w=12, tip=0.32))
        self.adv.set_opacity(aop)
        lop = self.links.get_value()
        for x, g in zip(self.link_x, self.linkset):
            inside = min(1.0, max(0.0, (edge - 0.3 - x) / 0.6)) * (1.0 if x > edge - LMAX else 0.0)
            g.set_opacity(lop * inside)
        tip = self.tip.get_value()
        mop = self.mt_op.get_value()
        for k, m in enumerate(self.mts):
            y = BASE + 0.18 + 0.18 * k
            m.set_points_as_corners([P(XL + 0.1, y), P(tip - 0.1 * (k % 2), y)])
            m.set_stroke(PURPLE, width=5, opacity=mop)


def marker(x, color=GREY, h=H):
    return DashedLine(P(x, SUBY), P(x, BASE + h + 0.25), color=color, stroke_width=3, dash_length=0.15)


def label(text, color, size=26, **kw):
    return T(text, size, color, **kw)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Harrison's Living Axon and the Growth Cone"
    TITLE = "Adhesion Turns Flow Into Advance"


# ---------------------------------------------------------------------------------------------
class S01Fan(SpokenScene):
    def construct(self):
        cone = Cone(edge=1.6, lock=True, dash_op=0.0, flow_op=0.0)
        # top-down fan
        shaft = RoundedRectangle(corner_radius=0.3, width=5.2, height=0.9, stroke_color=OUTLINE, stroke_width=4,
                                 fill_color=BLUE, fill_opacity=0.10).move_to(P(-3.6, 0))
        ap = P(-1.2, 0)
        arc = [ap + 3.0 * np.array([math.cos(a), math.sin(a), 0]) for a in np.linspace(-0.95, 0.95, 40)]
        fan = Polygon(ap, *arc, stroke_color=OUTLINE, stroke_width=4, fill_color=BLUE, fill_opacity=0.10)
        fil = VGroup(*[Line(ap + 3.0 * np.array([math.cos(a), math.sin(a), 0]),
                            ap + 3.5 * np.array([math.cos(a), math.sin(a), 0]), color=BLUE, stroke_width=4)
                       for a in np.linspace(-0.85, 0.85, 9)])
        top = VGroup(shaft, fan, fil)
        tag = label("growth cone: a flat fan", BLUE).move_to(P(1.0, -3.25))
        axon = label("axon", GREY).move_to(P(-3.6, -0.85))
        self.at("The tip of a growing")
        self.play(FadeIn(top), FadeIn(axon), run_time=0.9)
        self.play(FadeIn(tag), run_time=0.5)
        self.at("Slice through it")
        cut = DashedLine(P(-1.2, 0), P(2.7, 0), color=YELLOW, stroke_width=4)
        self.play(Create(cut), run_time=0.8)
        self.at("look from the side")
        cone.attach(self)
        sub = label("substrate", GREY).move_to(P(-5.0, -2.55))
        self.play(FadeOut(VGroup(top, axon, tag, cut)), FadeIn(VGroup(cone.fill, cone.outline, cone.substrate)),
                  FadeIn(sub), run_time=0.8)
        self.at("New actin joins")
        new = label("new actin joins at the front", TEAL).move_to(P(3.7, 3.0))
        pt = arrow(P(2.8, 2.65), P(1.4, 0.5), TEAL, w=6, tip=0.22)
        self.play(cone.dash_op.animate.set_value(1.0), cone.A.animate.set_value(A_RATE), FadeIn(new), GrowArrow(pt),
                  run_time=1.2)
        self.at("Motor proteins")
        my = label("myosin II pulls the network back", RED).move_to(P(-2.4, 3.0))
        self.play(cone.flow_op.animate.set_value(1.0), FadeIn(my), run_time=1.2)
        self.at("So how does")
        mk = marker(1.6)
        q = T("?", 120, GREEN, weight=BOLD).move_to(P(3.1, 0.4))
        self.play(Create(mk), FadeIn(q, scale=0.6), new.animate.set_opacity(0.45), my.animate.set_opacity(0.45),
                  pt.animate.set_opacity(0.45), run_time=0.9)
        self.play(Indicate(q, color=GREEN, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Flow(SpokenScene):
    def construct(self):
        cone = Cone(edge=1.6)
        cone.attach(self)
        sub = label("substrate", GREY).move_to(P(-5.0, -2.55))
        self.add(sub)
        self.at("That backward movement")
        rf = label("retrograde flow", RED, 30).move_to(P(-3.4, 2.65))
        self.play(FadeIn(rf, shift=LEFT * 0.2), run_time=0.8)
        self.at("The network treadmills")
        self.wait(1.0)
        self.at("is added")
        add = label("added", TEAL, 30).move_to(P(3.7, 2.7))
        pt = arrow(P(3.2, 2.4), P(1.4, 0.5), TEAL, w=6, tip=0.22)
        self.play(FadeIn(add), GrowArrow(pt), run_time=0.8)
        self.at("carried back")
        cb = label("carried back", RED, 28).move_to(P(-0.4, 2.55))
        cbar = arrow(P(-0.4, 2.2), P(-0.4, 1.5), RED, w=6, tip=0.22)
        self.play(FadeIn(cb), GrowArrow(cbar), run_time=0.6)
        self.at("at the same rate")
        same = VGroup(label("added", TEAL, 34), label("=", TEXT, 34), label("carried back", RED, 34)).arrange(RIGHT, buff=0.3)
        same.move_to(P(0.6, 3.25))
        self.play(FadeIn(same, shift=DOWN * 0.2), run_time=0.7)
        self.at("so the edge goes nowhere")
        mk = marker(1.6)
        stay = label("the edge stays here", GREY, 26).move_to(P(3.4, 0.3))
        self.play(Create(mk), FadeIn(stay), run_time=0.8)
        self.play(FadeOut(VGroup(add, pt, cb, cbar, rf)), run_time=0.5)
        self.at("running engine")
        self.play(FadeOut(same), run_time=0.4)
        eng = chip("engine: the actin network", BLUE, size=26).move_to(P(-2.8, 3.0))
        self.play(FadeIn(eng, shift=DOWN * 0.2), run_time=0.7)
        self.at("as the road")
        road = chip("road: the substrate", GREY, size=26).move_to(P(0.5, -2.75))
        self.play(FadeIn(road, shift=UP * 0.2), FadeOut(sub), run_time=0.7)
        self.at("The engine runs")
        self.play(Indicate(eng, color=BLUE, scale_factor=1.1), run_time=0.9)
        self.at("the car stays put")
        self.play(Indicate(stay, color=TEXT, scale_factor=1.12), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Clutch(SpokenScene):
    def construct(self):
        cone = Cone(edge=1.6)
        cone.attach(self)
        mk = marker(1.6)
        sub = label("substrate", GREY).move_to(P(-5.0, -2.55))
        self.add(mk, sub)
        self.at("Now add a clutch")
        cl = chip("a clutch", YELLOW, size=30).move_to(P(-3.4, 2.9))
        self.play(FadeIn(cl, shift=DOWN * 0.2), run_time=0.7)
        self.at("adhesion molecules")
        am = label("adhesion molecules", YELLOW, 26).move_to(P(-1.0, -2.55))
        self.play(cone.links.animate.set_value(1.0), FadeIn(am), run_time=1.6)
        self.at("the clutch engages")
        self.play(cone.clutch.animate.set_value(1.0), cone.adv_op.animate.set_value(1.0), run_time=1.3,
                  rate_func=smooth)
        self.at("Retrograde flow slows")
        fs = label("flow slows", RED, 30).move_to(P(0.0, 2.9))
        self.play(FadeIn(fs), run_time=0.6)
        self.at("pushes the edge forward")
        fw = label("the edge moves forward", GREEN, 30).move_to(P(3.7, 2.9))
        self.play(FadeIn(fw), FadeOut(fs), run_time=0.6)
        self.at("proposed this")
        who = label("Mitchison and Kirschner, 1988", GREY, 26).move_to(P(0, 3.3))
        self.play(FadeIn(who), FadeOut(cl), FadeOut(fw), run_time=0.6)
        self.at("It is called")
        hyp = T("the clutch hypothesis", 44, YELLOW, font=TITLE_FONT).move_to(P(0, 2.7))
        self.play(FadeIn(hyp, shift=UP * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Rule(SpokenScene):
    def construct(self):
        cone = Cone(edge=2.3, clutch=0.0, links=0.0, adv_op=1.0, h=2.0)
        cone.attach(self)
        mk = marker(2.3, h=2.0)
        self.add(mk)
        # equation, built piece by piece
        sz = 40
        w_adv = label("advance", GREEN, sz)
        eq1 = label("=", TEXT, sz)
        w_add = label("addition", TEAL, sz)
        minus = label("−", TEXT, sz)
        w_flow = label("flow", RED, sz)
        eq = VGroup(w_adv, eq1, w_add, minus, w_flow).arrange(RIGHT, buff=0.3).move_to(P(0, 3.05))
        # bars (rates)
        x0 = -2.2
        rows = [("addition", TEAL, 2.25), ("flow", RED, 1.7), ("advance", GREEN, 1.15)]
        names = VGroup(*[label(n, c, 26).move_to(P(x0 - 0.3 - 0.0, y)).align_to(P(x0 - 0.25, y), RIGHT)
                         for n, c, y in rows])
        bars = VGroup()

        def mkbar(getter, color, y):
            b = Rectangle(width=0.1, height=0.3, stroke_width=0, fill_color=color, fill_opacity=0.9)

            def up(m):
                w = getter() * 9
                m.become(Rectangle(width=max(w, 0.04), height=0.3, stroke_width=0, fill_color=color,
                                   fill_opacity=0.9 if w > 0.03 else 0.0).move_to(P(x0 + max(w, 0.04) / 2, y)))
            b.add_updater(up)
            return b
        b_add = mkbar(lambda: cone.A.get_value(), TEAL, 2.25)
        b_flow = mkbar(lambda: cone.Fv, RED, 1.7)
        b_adv = mkbar(lambda: cone.A.get_value() - cone.Fv, GREEN, 1.15)
        state = chip("clutch off", GREY, size=28).move_to(P(4.6, 1.7))
        self.at("Put it as a rule")
        self.wait(0.2)
        self.at("The rate of advance")
        self.play(FadeIn(w_adv), run_time=0.5)
        self.at("equals")
        self.play(FadeIn(eq1), run_time=0.3)
        self.at("actin addition")
        self.play(FadeIn(w_add, shift=LEFT * 0.2), run_time=0.5)
        self.at("minus")
        self.play(FadeIn(minus), run_time=0.3)
        self.at("retrograde flow")
        self.play(FadeIn(w_flow, shift=LEFT * 0.2), run_time=0.5)
        self.at("With the clutch off")
        self.add(b_add, b_flow, b_adv)
        self.play(FadeIn(names), FadeIn(state), run_time=0.8)
        self.at("flow matches addition")
        self.play(Indicate(VGroup(b_add, b_flow), color=TEXT, scale_factor=1.05), run_time=0.9)
        self.at("advance is zero")
        self.play(Indicate(w_adv, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.at("With the clutch on")
        on = chip("clutch on", YELLOW, size=28).move_to(state)
        self.play(Transform(state, on), cone.links.animate.set_value(1.0),
                  cone.clutch.animate.set_value(1.0), run_time=4.0, rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Tubules(SpokenScene):
    def construct(self):
        cone = Cone(edge=2.7, clutch=1.0, links=1.0, adv_op=1.0)
        cone.attach(self)
        self.at("Actin makes the advance")
        a = label("actin makes the advance", BLUE, 30).move_to(P(1.0, 2.65))
        self.play(FadeIn(a, shift=UP * 0.15), run_time=0.7)
        self.at("Microtubules make it permanent")
        m = label("microtubules make it permanent", PURPLE, 32).move_to(P(-0.6, 3.25))
        self.play(FadeIn(m, shift=UP * 0.15), a.animate.set_opacity(0.4), run_time=0.7)
        self.at("hollow tubes")
        self.play(cone.mt_op.animate.set_value(1.0), run_time=1.2)
        mt = label("microtubules", PURPLE, 26).move_to(P(-2.0, 0.4))
        self.play(FadeIn(mt), run_time=0.4)
        self.at("extend into the new territory")
        self.play(cone.tip.animate.set_value(-1.8), FadeOut(mt), run_time=2.6, rate_func=smooth)
        self.at("narrows")
        self.play(cone.sh.animate.set_value(-2.6), cone.tip.animate.set_value(-0.8), run_time=1.5, rate_func=smooth)
        self.at("becomes axon shaft")
        shaft = label("axon shaft", GREY, 28).move_to(P(-4.2, 0.2))
        self.play(FadeIn(shaft), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class Turner:
    """Top view of a growth cone that turns when its two sides advance at different rates."""
    R = 1.5

    def __init__(self, pos, theta, vL, vR):
        self.pos = np.array(pos, float)
        self.th = theta
        self.vL, self.vR = ValueTracker(vL), ValueTracker(vR)
        self.trail_pts = [self.pos.copy()]
        self.trail = VMobject(stroke_color=OUTLINE, stroke_width=22, stroke_opacity=0.35)
        self.fan = VMobject(stroke_color=OUTLINE, stroke_width=4, fill_color=BLUE, fill_opacity=0.14)
        self.fil = VGroup(*[Line(ORIGIN, RIGHT, color=BLUE, stroke_width=4) for _ in range(9)])
        self.aL = arrow(P(0, 0), P(1, 0), GREEN, w=10, tip=0.28)
        self.aR = arrow(P(0, 0), P(1, 0), GREEN, w=10, tip=0.28)
        self.driver = Mobject()
        self.driver.add_updater(lambda m, dt: self.step(dt))
        self.running = True
        self.draw()

    def step(self, dt):
        if self.running:
            vl, vr = self.vL.get_value(), self.vR.get_value()
            self.th += 0.3 * (vl - vr) * dt
            self.pos = self.pos + (vl + vr) / 2 * np.array([math.cos(self.th), math.sin(self.th), 0]) * dt
            self.trail_pts.append(self.pos.copy())
        self.draw()

    def unit(self, a):
        return np.array([math.cos(a), math.sin(a), 0])

    def draw(self):
        th, R, p = self.th, self.R, self.pos
        apex = p - self.unit(th) * 1.5
        arc = [p + R * self.unit(th + a) * 1.0 for a in np.linspace(-1.0, 1.0, 30)]
        self.fan.set_points_as_corners([apex] + arc + [apex])
        for line, a in zip(self.fil, np.linspace(-0.9, 0.9, 9)):
            line.put_start_and_end_on(p + R * self.unit(th + a), p + (R + 0.5) * self.unit(th + a))
        if len(self.trail_pts) > 1:
            self.trail.set_points_as_corners(self.trail_pts[:: max(1, len(self.trail_pts) // 400)] + [apex])
        for ar, a, v in ((self.aL, 0.62, self.vL), (self.aR, -0.62, self.vR)):
            s = p + (R + 0.75) * self.unit(th + a)
            ln = max(0.12, v.get_value() * 2.4)
            ar.become(arrow(s, s + self.unit(th) * ln, GREEN, w=10, tip=min(0.28, ln * 0.9)))

    def side_point(self, a, extra=0.0):
        return self.pos + (self.R + 1.15 + extra) * self.unit(self.th + a)

    def attach(self, scene):
        scene.add(self.trail, self.fan, self.fil, self.aL, self.aR, self.driver)

    @property
    def group(self):
        return VGroup(self.trail, self.fan, self.fil, self.aL, self.aR)


class S06Turn(SpokenScene):
    def construct(self):
        t1 = Turner(P(-4.6, -1.5), 0.0, 0.22, 0.22)
        t1.attach(self)
        self.at("Now see how")
        self.wait(0.1)
        self.at("a difference in that balance")
        diff = label("one side advances more", GREEN, 28).move_to(P(-1.0, 3.0))
        cue = VGroup(*[Circle(radius=r, stroke_color=ORANGE, stroke_width=3, stroke_opacity=o, fill_opacity=0)
                       for r, o in ((0.4, 0.9), (0.8, 0.55), (1.2, 0.3))])
        cue.add(Dot(color=ORANGE, radius=0.18))
        cue.move_to(P(4.8, 2.4))
        cl = label("nerve growth factor", ORANGE, 24).move_to(P(4.7, 0.5))
        self.play(t1.vL.animate.set_value(0.30), t1.vR.animate.set_value(0.14), FadeIn(diff), FadeIn(cue, scale=0.6),
                  FadeIn(cl), run_time=1.5)
        self.at("A cue on one side")
        self.play(FadeOut(diff), run_time=0.6)
        self.at("sensory neurons")
        src = label("chick sensory neuron", OUTLINE, 26).move_to(P(-3.4, -2.4))
        self.play(FadeIn(src), run_time=0.6)
        # case 2
        self.at("Drugs released")
        self.wait(0.1)
        self.at("Remove actin")
        t1.running = False
        self.play(FadeOut(VGroup(t1.group, cue, cl, src)), run_time=0.6)
        self.remove(t1.driver)
        t2 = Turner(P(-4.6, 0.2), 0.0, 0.3, 0.3)
        t2.attach(self)
        self.at("on one side", nth=1)
        xmark = VGroup(Line(P(-.25, -.25), P(.25, .25), color=RED, stroke_width=9),
                       Line(P(-.25, .25), P(.25, -.25), color=RED, stroke_width=9))
        xmark.add_updater(lambda m: m.move_to(t2.side_point(0.62, 0.45)))
        lab = label("actin addition blocked", RED, 26)
        lab.add_updater(lambda m: m.move_to(t2.side_point(0.62, 0.45) + UP * 0.5))
        self.add(xmark, lab)
        self.play(t2.vL.animate.set_value(0.15), t2.vR.animate.set_value(0.45), FadeIn(xmark), FadeIn(lab), run_time=1.5)
        self.at("away from that side")
        self.wait(0.4)
        self.at("Keep the rule")
        xmark.clear_updaters()
        lab.clear_updaters()
        self.play(FadeOut(VGroup(xmark, lab)), run_time=0.5)
        r1 = VGroup(label("advance", GREEN, 36), label("=", TEXT, 36), label("addition", TEAL, 36),
                    label("−", TEXT, 36), label("flow", RED, 36)).arrange(RIGHT, buff=0.28)
        r1.move_to(P(0.6, 3.1))
        r2 = VGroup(label("turning", GREEN, 36), label("=", TEXT, 36), label("difference between sides", GREEN, 36)
                    ).arrange(RIGHT, buff=0.28).move_to(P(0.6, 2.5))
        self.play(FadeIn(r1, shift=DOWN * 0.15), run_time=0.8)
        self.at("Turning is", nth=1)
        self.play(FadeIn(r2, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Advance is addition minus flow. Turning is the difference between sides."
