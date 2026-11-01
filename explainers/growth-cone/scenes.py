"""Adhesion turns flow into advance  (Biochemistrypedia explainer, growth cone lesson)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the actin network (the engine); the growth cone's fill
  TEAL   = newly added actin at the leading edge ("addition")
  RED    = retrograde flow, myosin pull, removed actin (backward / loss); repellent cloud
  YELLOW = adhesion molecules, the clutch
  GREEN  = advance of the edge; attractive cue cloud
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


class S00Title(TitleCard):
    LESSON = "Harrison's Living Axon and the Growth Cone"
    TITLE = "Adhesion Turns Flow Into Advance"


class S07End(EndCard):
    LINE = "Advance is addition minus flow. Turning is the difference between sides."


# Top-down fan reuses Turner's outline and filopodia. Transforming a whole fan
# keeps the shaft continuous while a deliberately bounded path shows the turn.
def fan_at(x=0, y=0, theta=0, scale=1, actin=True, tubules=False):
    t = Turner(P(0, 0), 0, 0, 0)
    t.running = False
    fan = VGroup(t.fan.copy(), t.fil.copy())
    if not actin:
        fan[1].set_opacity(0.12)
    if tubules:
        fan.add(VGroup(*[Line(P(-1.5, j * .16), P(.65, j * .32),
                             color=PURPLE, stroke_width=5) for j in range(-1, 2)]))
    return fan.scale(scale).rotate(theta).shift(P(x, y))


def cloud(x, y, color):
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=o)
                    for r, o in ((1.05, .07), (.75, .12), (.4, .22))]).move_to(P(x, y))


def pipette(x, y, color=ORANGE):
    return Polygon(P(x, y), P(x + .7, y + .85), P(x + 1.15, y + .85),
                   stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=.12)


def route(points):
    return VMobject(stroke_color=OUTLINE, stroke_width=17, stroke_opacity=.4).set_points_smoothly(
        [P(*p) for p in points])


class S01Steer(SpokenScene):
    def construct(self):
        cone = fan_at(-3.5, -.3, scale=.65)
        shaft = route([(-6, -.3), (-4.5, -.3)])
        cells = VGroup(*[Circle(radius=.45, color=GREY, fill_opacity=.08).move_to(P(x, y))
                        for x, y in [(-1.8, 2.3), (3, -1.4), (3, 2.4), (5, .8)]])
        target = cells[-1]
        self.at('A growing axon')
        self.play(FadeIn(cells), Create(shaft), FadeIn(cone), run_time=.8)
        ax = label('axon', GREY).move_to(P(-5, -1.1))
        self.at('at its tip')
        tag = label('growth cone', BLUE, 30).move_to(P(-2.5, -2.1))
        self.play(FadeIn(ax), FadeIn(tag), run_time=.5)
        self.at('feels its way')
        self.play(Transform(cone, fan_at(-2.7, -.3, scale=.65)),
                  Transform(shaft, route([(-6, -.3), (-3.7, -.3)])), run_time=1)
        attract = cloud(.7, 1.2, GREEN)
        repel = cloud(.7, -1.0, RED)
        cues = VGroup(label('attract', GREEN).move_to(P(.7, 2.65)),
                      label('repel', RED).move_to(P(.7, -2.65)))
        self.at('guidance cues')
        self.play(FadeOut(ax), FadeOut(tag), FadeIn(attract), FadeIn(repel), FadeIn(cues), run_time=.6)
        self.at('one side more strongly')
        self.play(Transform(cone, fan_at(-1.4, .25, .4, .65)),
                  Transform(shaft, route([(-6, -.3), (-3, -.3), (-2.3, -.15)])), run_time=1.1)
        self.at('the growth cone turns')
        self.play(Transform(cone, fan_at(.1, .85, .3, .65)),
                  Transform(shaft, route([(-6, -.3), (-3, -.3), (-1.8, .3), (-.85, .55)])), run_time=1.2)
        self.at('to its target')
        self.play(FadeOut(attract), FadeOut(repel), FadeOut(cues),
                  Transform(cone, fan_at(3.4, .8, 0, .65)),
                  Transform(shaft, route([(-6, -.3), (-3, -.3), (-1.5, .7), (1, 1), (2.4, .8)])),
                  target.animate.set_stroke(GREEN, 5), run_time=1.3)
        self.at('So how does')
        q = label('How does the tip move and turn?', TEXT, 34).move_to(P(0, -2.6))
        self.play(FadeIn(q), run_time=.6)
        self.finish()


class S02Assay(SpokenScene):
    def construct(self):
        cone = fan_at(-1, -.5)
        shaft = route([(-6, -.5), (-2.5, -.5)])
        title = label('Gundersen and Barrett', GREY, 30).move_to(P(0, 3.1))
        self.at('First the evidence')
        self.play(FadeIn(cone), Create(shaft), FadeIn(title), run_time=.7)
        pip = pipette(2, 1.3)
        cue = cloud(2, 1.3, ORANGE)
        name = label('nerve growth factor', ORANGE).move_to(P(3.2, -.2))
        source = label('chick sensory neuron', GREY).move_to(P(-3, -2.8))
        self.at('a pipette releasing')
        self.play(FadeIn(pip), FadeIn(cue), FadeIn(name), FadeIn(source), run_time=.7)
        self.at('met more of it')
        gradient = VGroup(*[Dot(P(.25, y), radius=.09, color=ORANGE).set_opacity(o)
                            for y, o in [(-1.3, .2), (-.6, .4), (.1, .7), (.8, 1)]])
        self.play(FadeIn(gradient), run_time=.6)
        self.at('turned toward it')
        self.play(Transform(cone, fan_at(.2, .1, .5)),
                  Transform(shaft, route([(-6, -.5), (-2.5, -.5), (-1.1, -.6)])), run_time=1.2)
        self.at('then cut growth cones')
        cut = DashedLine(P(-3, -1.4), P(-3, .6), color=RED, stroke_width=5)
        newtitle = label('Campbell and Holt', GREY, 30).move_to(title)
        newsource = label('frog retinal neuron', GREY).move_to(source)
        self.play(FadeOut(gradient), FadeOut(name), FadeOut(pip), FadeOut(cue),
                  Transform(cone, fan_at(-1, -.5)),
                  Transform(shaft, route([(-6, -.5), (-2.5, -.5)])),
                  Transform(title, newtitle), Transform(source, newsource), Create(cut), run_time=.7)
        self.at('away from their cell bodies')
        short = route([(-2.9, -.5), (-2.5, -.5)])
        self.play(Transform(shaft, short), run_time=.6)
        self.at('The isolated tips')
        self.play(FadeOut(cut), FadeIn(pip), FadeIn(cue), run_time=.6)
        self.at('to guidance cues')
        self.play(Transform(cone, fan_at(.2, .1, .5)),
                  Transform(shaft, route([(-2.9, -.5), (-2, -.5), (-1.1, -.6)])), run_time=1.2)
        self.at('The decision is made')
        result = label('the decision is at the tip', BLUE, 32).move_to(P(0, -2.8))
        self.play(FadeOut(source), FadeIn(result), run_time=.6)
        self.finish()


class S03Flow(SpokenScene):
    def construct(self):
        top = fan_at(0, 0, scale=1.35, tubules=True)
        top[2].set_opacity(0)
        self.at('Now open the fan')
        self.play(FadeIn(top), run_time=.6)
        self.at('Microtubules fill')
        mt = label('microtubules', PURPLE, 30).move_to(P(-3.4, -2.8))
        self.play(top[2].animate.set_opacity(1), FadeIn(mt), run_time=.6)
        self.at('Actin fills the edge')
        act = label('actin', BLUE, 30).move_to(P(2.6, -2.8))
        self.play(FadeIn(act), Indicate(top[1], color=TEAL), run_time=.8)
        self.at('New actin joins')
        cut = DashedLine(P(-2, 0), P(2.7, 0), color=GREY)
        self.play(Create(cut), run_time=.3)
        self.remove(top, mt, act, cut)
        cone = Cone(edge=1.6, dash_op=0, flow_op=0)
        cone.attach(self)
        new = label('addition at the front', TEAL, 30).move_to(P(2.6, 3.05))
        self.play(cone.dash_op.animate.set_value(1), FadeIn(new), run_time=.7)
        self.at('Motor proteins')
        my = label('myosin II pulls back', RED, 30).move_to(P(-3.2, 3.05))
        self.play(cone.flow_op.animate.set_value(1), FadeIn(my), run_time=.7)
        self.at('That backward movement')
        rf = label('retrograde flow', RED, 30).move_to(my)
        self.play(Transform(my, rf), run_time=.6)
        self.at('at the same rate')
        same = VGroup(label('addition', TEAL, 32), label('=', TEXT, 32), label('flow', RED, 32))
        same.arrange(RIGHT, buff=.3).move_to(P(0, 3.05))
        self.play(FadeOut(new), FadeOut(my), FadeIn(same), run_time=.5)
        self.at('the edge goes nowhere')
        mk = marker(1.6)
        stay = label('edge stays here', GREY, 28).move_to(P(3.9, -.3))
        self.play(Create(mk), FadeIn(stay), run_time=.6)
        self.at('The engine runs')
        self.play(Indicate(cone.dashes, color=BLUE, scale_factor=1.02), run_time=.6)
        self.at('the car stays put')
        self.play(Indicate(stay, color=TEXT), run_time=.6)
        self.finish()


class S04Clutch(SpokenScene):
    def construct(self):
        cone = Cone(edge=1.6, h=2)
        cone.attach(self)
        mk = marker(1.6, h=2)
        self.add(mk)
        header = label('the clutch', YELLOW, 34).move_to(P(0, 3.1))
        self.at('Now add a clutch')
        self.play(FadeIn(header), run_time=.6)
        adh = label('adhesion links', YELLOW, 28).move_to(P(-1, -2.65))
        self.at('adhesion molecules link')
        self.play(cone.links.animate.set_value(1), FadeIn(adh), run_time=1)
        self.at('retrograde flow slows')
        self.play(cone.clutch.animate.set_value(1), run_time=.8)
        self.at('pushes the edge forward')
        self.play(cone.adv_op.animate.set_value(1), run_time=.7)
        self.at('proposed this')
        who = label('Mitchison and Kirschner · 1988', GREY, 28).move_to(P(0, 2.15))
        self.play(FadeIn(who), run_time=.6)
        words = [label('advance', GREEN, 34), label('=', TEXT, 34), label('addition', TEAL, 34),
                 label('−', TEXT, 34), label('flow', RED, 34)]
        eq = VGroup(*words).arrange(RIGHT, buff=.28).move_to(P(0, 3.1))
        self.at('Put it as a rule')
        self.play(FadeOut(header), FadeOut(who), run_time=.5)
        bars = VGroup()
        for n, c, y, value in [('addition', TEAL, 2.25, .30), ('flow', RED, 1.65, .20),
                               ('advance', GREEN, 1.05, .10)]:
            name = label(n, c, 24).move_to(P(-3, y)).align_to(P(-2.1, y), RIGHT)
            bar = Rectangle(width=value * 10, height=.25, stroke_width=0, fill_color=c, fill_opacity=.9)
            bar.move_to(P(-1.7 + value * 5, y))
            bars.add(VGroup(name, bar))
        self.at('The rate of advance')
        self.play(FadeIn(words[0]), FadeIn(bars[2]), run_time=.4)
        self.at('equals')
        self.play(FadeIn(words[1]), run_time=.25)
        self.at('rate of actin addition')
        self.play(FadeIn(words[2]), FadeIn(bars[0]), run_time=.4)
        self.at('minus')
        self.play(FadeIn(words[3]), run_time=.25)
        self.at('rate of retrograde flow')
        self.play(FadeIn(words[4]), FadeIn(bars[1]), run_time=.4)
        self.finish()


class S05Turn(SpokenScene):
    def construct(self):
        cone = fan_at(0, -.1, PI/2)
        shaft = route([(0, -3.1), (0, -1.6)])
        arrows = VGroup(arrow(P(-1.05, 1.7), P(-1.05, 2.4), GREEN),
                        arrow(P(1.05, 1.7), P(1.05, 2.4), GREEN))
        self.at('Turning is that rule')
        self.play(FadeIn(cone), Create(shaft), FadeIn(arrows), run_time=.7)
        cue = cloud(-3, 1.1, ORANGE)
        cue_label = label('cue', ORANGE).move_to(P(-3, 2.5))
        self.at('A cue on one side')
        self.play(FadeIn(cue), FadeIn(cue_label), run_time=.5)
        self.at('one side advances more')
        self.play(Transform(arrows[0], arrow(P(-1.05, 1.7), P(-1.05, 3.1), GREEN)),
                  Transform(cone, fan_at(-.65, .2, PI/2+.35)),
                  Transform(shaft, route([(0, -3.1), (0, -1.8), (-.15, -1.3)])), run_time=1)
        self.at('Drugs released onto')
        pip = pipette(-3, 1.1, RED)
        # Reset both the shape and the old result before the drug experiment.
        self.play(FadeOut(cue), FadeOut(cue_label), FadeOut(arrows), FadeIn(pip),
                  Transform(cone, fan_at(0, -.1, PI/2)),
                  Transform(shaft, route([(0, -3.1), (0, -1.6)])), run_time=.6)
        self.at('Remove actin on one side')
        # In the upward-facing fan, indices 5..8 are the screen-left edge.
        removed = label('actin removed', RED, 28).move_to(P(-3.5, -.6))
        self.play(*[cone[1][i].animate.set_opacity(.03) for i in range(5, 9)], FadeIn(removed), run_time=.7)
        self.at('turns away from that side')
        dest = fan_at(.9, .2, PI/2-.5)
        for i in range(5, 9):
            dest[1][i].set_opacity(.03)
        self.play(Transform(cone, dest),
                  Transform(shaft, route([(0, -3.1), (0, -1.7), (.2, -1.1)])), run_time=1.1)
        self.finish()


class S06Tubules(SpokenScene):
    def construct(self):
        cone = fan_at(0, -.1, PI/2, tubules=True)
        shaft = route([(0, -3.1), (0, -1.6)])
        self.at('Microtubules steer too')
        self.play(FadeIn(cone), Create(shaft), run_time=.6)
        pip = pipette(-3, 1.1, PURPLE)
        taxol = label('taxol', PURPLE, 28).move_to(P(-3.2, 2.6))
        self.at('Stabilize them on one side')
        dest = fan_at(-.6, .2, PI/2+.35, tubules=True)
        dest[2][2].set_stroke(width=9)
        self.play(FadeIn(pip), FadeIn(taxol), cone[2][2].animate.set_stroke(width=9), run_time=.6)
        self.at('turns toward that side')
        self.play(Transform(cone, dest), Transform(shaft, route([(0, -3.1), (0, -1.8), (-.1, -1.3)])), run_time=.9)
        self.at('Break them down on one side')
        neutral = fan_at(0, -.1, PI/2, tubules=True)
        neutral[2][2].set_opacity(.05)
        loss = label('microtubules lost', RED, 28).move_to(P(-3.5, 2.6))
        self.play(FadeOut(taxol), FadeIn(loss),
                  Transform(cone, neutral), Transform(shaft, route([(0, -3.1), (0, -1.6)])), run_time=.7)
        self.at('it turns away')
        away = fan_at(.8, .1, PI/2-.45, tubules=True)
        away[2][2].set_opacity(.05)
        self.play(Transform(cone, away),
                  Transform(shaft, route([(0, -3.1), (0, -1.8), (.15, -1.3)])), run_time=.8)
        self.at('As the edge moves')
        self.play(FadeOut(pip), FadeOut(loss),
                  Transform(cone, fan_at(0, -.1, PI/2, tubules=True)),
                  Transform(shaft, route([(0, -3.1), (0, -1.6)])), run_time=.6)
        self.at('microtubules extend into the new territory')
        tubes = VGroup(*[Line(P(j*.18, -2.9), P(j*.3, 1.2), color=PURPLE, stroke_width=5)
                         for j in range(-1, 2)])
        self.play(Transform(cone[2], tubes), run_time=1.1)
        self.at('the fan behind them narrows')
        narrow = fan_at(0, 1.1, PI/2, scale=.65, tubules=True)
        self.play(Transform(cone, narrow),
                  Transform(shaft, route([(0, -3.1), (0, .1)])), run_time=.9)
        self.at('becomes axon shaft')
        shaft_label = label('axon shaft', GREY, 28).move_to(P(2, -.9))
        consolidated = VGroup(*[Line(P(j*.13, -2.9), P(j*.13, .2), color=PURPLE, stroke_width=4)
                               for j in range(-1, 2)])
        self.play(FadeIn(shaft_label), Create(consolidated), run_time=.6)
        self.at('Keep the rule')
        self.play(FadeOut(shaft_label), run_time=.4)
        sense = label('senses a cue', ORANGE, 32).move_to(P(-3.5, 2.9))
        self.at('The tip senses a cue')
        self.play(FadeIn(sense), run_time=.5)
        self.at('turning is the difference')
        rule = label('turns by the difference\nbetween its two sides', GREEN, 30).move_to(P(3.3, -1.8))
        self.play(FadeIn(rule), run_time=.7)
        self.finish()
