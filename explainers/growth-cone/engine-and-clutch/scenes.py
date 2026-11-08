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

BASE = -2.25      # underside of the growth cone (side view)
SUBY = -2.8     # the substrate
H = 4.3          # height of the flat fan in the side view
HS = 0.9         # height of the axon shaft
XL = -6.1        # left end of the drawn axon
LMAX = 4.2       # how far behind the edge the actin network reaches
A_RATE = 0.30    # actin addition at the edge
F_OFF = 0.30     # retrograde flow with the clutch off
F_ON = 0.06      # retrograde flow with the clutch on


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


def side_p(x, y):
    return P(x + 1.9, y)


class Cone:
    """Side view of a growth cone on the substrate. One object drives all the motion."""

    def __init__(self, edge=2.2, A=A_RATE, clutch=0.0, links=0.0, sh=-5.0, tip=-4.0, lock=False,
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
        self.flow = VGroup(*[arrow(side_p(0, 0), side_p(-1, 0), RED) for _ in range(3)])
        self.adv = arrow(side_p(0, 0), side_p(1, 0), GREEN, w=12, tip=0.32)
        self.linkset = VGroup()
        self.link_x = [-4.0 + 0.8 * k for k in range(14)]
        for x in self.link_x:
            ln = Line(side_p(x, SUBY), side_p(x, BASE), color=YELLOW, stroke_width=5)
            hook = Line(side_p(x, SUBY), side_p(x+.22, SUBY+.17), color=YELLOW, stroke_width=5)
            self.linkset.add(VGroup(ln, hook))
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
        self.d = [(d + (self.Fv if self.lock else A) * dt) % LMAX for d in self.d]
        self.refresh()

    def attach(self, scene):
        # Put the time-based updater first so Cairo redraws every dependent graphic.
        scene.add(self.driver, self.fill, self.mts, self.dashes, self.linkset, self.flow, self.adv, self.outline,
                  self.substrate)

    def refresh(self):
        edge = self.edge.get_value()
        sh = self.sh.get_value()
        xs = np.linspace(XL, edge, 220)
        top = [side_p(x, BASE + prof(x, edge, sh, self.h)) for x in xs]
        closed = top + [side_p(edge, BASE), side_p(XL, BASE)]
        self.fill.set_points_as_corners(closed)
        self.outline.set_points_as_corners(closed)
        dop = self.dash_op.get_value()
        for i, dash in enumerate(self.dashes):
            d = self.d[i]
            x = edge - 0.15 - d
            y = BASE + self.r[i] * prof(x, edge, sh, self.h)
            v = np.array([math.cos(self.ang[i]), math.sin(self.ang[i]), 0]) * 0.18
            dash.set_points_as_corners([side_p(x, y) - v, side_p(x, y) + v])
            col = interpolate_color(ManimColor(TEAL), ManimColor(BLUE), min(1.0, d / 1.2))
            op = min(1.0, d / 0.25) * min(1.0, (LMAX - d) / 0.7) * dop
            dash.set_stroke(col, width=5.5, opacity=op)
        fop = self.flow_op.get_value()
        L = max(0.45, self.Fv * 5.5)
        for k, a in enumerate(self.flow):
            x0 = edge - 1.3 - 0.35 * k
            y = BASE + self.h * (0.25 + 0.25 * k)
            a.become(arrow(side_p(x0, y), side_p(x0 - L, y), RED))
            a.set_opacity(fop)
        adv = (self.A.get_value() - self.Fv) * 5
        aop = self.adv_op.get_value() if adv > 0.25 else 0.0
        self.adv.become(arrow(side_p(edge - 0.075, BASE + 0.33 * self.h), side_p(edge - 0.075 + max(adv, 0.3), BASE + 0.33 * self.h), GREEN, w=12, tip=0.32))
        self.adv.set_opacity(aop)
        lop = self.links.get_value()
        for x, g in zip(self.link_x, self.linkset):
            inside = min(1.0, max(0.0, (edge - 0.3 - x) / 0.6)) * (1.0 if x > edge - LMAX else 0.0)
            g.set_opacity(lop * inside)
        tip = self.tip.get_value()
        mop = self.mt_op.get_value()
        for k, m in enumerate(self.mts):
            y = BASE + 0.18 + 0.18 * k
            m.set_points_as_corners([side_p(XL + 0.1, y), side_p(tip - 0.1 * (k % 2), y)])
            m.set_stroke(PURPLE, width=5, opacity=mop)


def marker(x, color=GREY, h=H):
    return DashedLine(side_p(x, SUBY), side_p(x, BASE + h + 0.25), color=color, stroke_width=3, dash_length=0.15)


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



# The palette follows the lesson's earlier film: BLUE actin, PURPLE microtubules.
# Motion is schematic; edge velocity = addition - retrograde flow throughout.
# Override logging only: the repair is restricted to scenes.py and deliverables.
class SpokenScene(SpokenScene):
    def at(self, phrase, lead=.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > .02:
            self.wait(rest)


def heading(s, color=TEXT):
    return T(s, 32, color).move_to(P(0,3.45))


YS = [-1.85 + j*.8 for j in range(6)]
LEFT_EDGE, RIGHT_EDGE = -5.5, 5.5


def filament(y, end):
    # Central disassembly is visible as a spatial fade, not an abrupt box edge.
    xs=[-4.8,-4.4,-4.0,-3.6,-3.2,end]
    return VGroup(*[Line(P(a,y),P(b,y),color=BLUE,stroke_width=4,stroke_opacity=op)
        for a,b,op in zip(xs[:-1],xs[1:],[.08,.25,.5,.8,1])])


def edge_view(gap=0):
    body=RoundedRectangle(width=11,height=5.0,corner_radius=.45,
        color=OUTLINE,fill_color=BLUE,fill_opacity=.07).move_to(P(0,.05))
    membrane=Line(P(5.5,-2.1),P(5.5,2.2),color=OUTLINE,stroke_width=7)
    mesh=VGroup(*[filament(y,5.4-gap) for y in YS])
    names=VGroup(T('centre',28,TEXT).move_to(P(-4.7,-3.05)),
                 T('front edge',28,TEXT).move_to(P(4.7,-3.05)))
    return VGroup(body,membrane,mesh,names)


def band(gap=2):
    return Rectangle(width=max(.015,gap),height=4.65,color=GOLD,stroke_width=3,
        fill_color=GOLD,fill_opacity=.08).move_to(P(5.5-gap/2,.1))


def gap_label():
    lab=T('actin-free band',28,GOLD).move_to(P(2.3,-3.05))
    lead=Line(P(3.5,-2.85),P(4.5,-2.3),color=GOLD,stroke_width=2)
    return VGroup(lab,lead)


def blocked():
    return chip('addition blocked',RED,26,pad=.15).move_to(P(3.6,2.91))


def moving_dots(scene, right=5.25, speed=.65, gap=None, replenish=True):
    # dx/dt=-flow; rows deliberately lie between filament lines.
    dots=VGroup(*[Dot(P(x,y+.3),radius=.06,color=RED)
        for y in YS[:-1] for x in np.linspace(-4.4,right,10)])
    def update(m,dt):
        boundary=right-(gap.get_value() if gap is not None else 0)
        for d in m:
            d.shift(LEFT*speed*dt)
            if d.get_x() < -4.8 and replenish:
                d.set_x(boundary)
            opacity=np.clip((d.get_x()+4.8)/.8,0,1)
            if d.get_x()>boundary: opacity=0
            d.set_opacity(opacity)
    dots.add_updater(update)
    scene.add(dots)
    return dots


def blocked_question():
    return VGroup(edge_view(),blocked(),heading('What happens just behind the edge?').shift(LEFT*.7))


def tubes_to(x):
    # Tubules occupy gaps between the actin rows, never overlaid on them.
    return VGroup(*[Line(P(-4.7,y+.4),P(x,y+.4),color=PURPLE,stroke_width=7)
        for y in YS[1:4]])


def clutch_scene(scene, engaged=False):
    c=Cone(edge=2.2,clutch=1 if engaged else 0,links=1 if engaged else 0,lock=True)
    c.attach(scene)
    return c


def note(s,color=TEXT,y=-3.25):
    return T(s,28,color).move_to(P(0,y))


def side_label(s,color=TEXT,y=.9):
    return T(s,26,color).move_to(P(-4.4,y))


def bead():
    b=Circle(radius=.5,color=OUTLINE,fill_color=OUTLINE,fill_opacity=.2).move_to(side_p(2.45,.05))
    coat=VGroup(*[Line(b.get_center()+.48*P(math.cos(a),math.sin(a)),
        b.get_center()+.66*P(math.cos(a),math.sin(a)),color=YELLOW,stroke_width=5)
        for a in np.linspace(0,TAU,10)[:-1]])
    # A clamp rather than an unexplained pendulum.
    hold=VGroup(Line(side_p(2.45,.6),side_p(2.45,1.65),color=OUTLINE,stroke_width=5),
        Line(side_p(2.2,1.65),side_p(3,1.65),color=OUTLINE,stroke_width=6))
    return VGroup(b,coat,hold)


class S00Title(TitleCard):
    LESSON='The Growth Cone: The Tip That Steers the Axon'
    TITLE='Engine and Clutch'
    def construct(self):
        title=T(self.TITLE,54,font=TITLE_FONT)
        lesson=VGroup(T('The Growth Cone:',28),T('The Tip That Steers the Axon',28)).arrange(DOWN,buff=.15)
        g=VGroup(lesson,title,Line(LEFT*1.4,RIGHT*1.4,color=GOLD)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.6)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        f=fan_at(scale=2).move_to(P(-1.3,-.1))
        self.add(f,heading('How can the edge advance while actin flows back?'))
        # Speckle field inside the widening fan, streamed towards its centre.
        phase=ValueTracker(0)
        dots=VGroup(*[Dot(radius=.065,color=RED) for _ in range(40)])
        def draw(m,dt):
            phase.increment_value(.5*dt)
            for i,d in enumerate(m):
                u=(i/40+phase.get_value()/4)%1
                a=(-.85+(i%8)/7*1.7)
                d.move_to(P(-3.3+(1-u)*4.5*math.cos(a),(1-u)*2.7*math.sin(a)))
                d.set_opacity(min(1,(1-u)*4))
        dots.add_updater(draw);self.add(dots)
        self.at('move forward')
        self.play(GrowArrow(arrow(P(3.4,1),P(5.6,1),GREEN)),FadeIn(T('edge advance',28,GREEN).move_to(P(4.5,1.65))),run_time=.4)
        self.at('while its actin')
        self.play(GrowArrow(arrow(P(5.6,-1),P(3.4,-1),RED)),FadeIn(T('flow',28,RED).move_to(P(4.5,-1.65))),run_time=.3)
        self.at('streams backward');self.finish()


class S02Add(SpokenScene):
    def construct(self):
        v=edge_view(gap=.9);self.add(v,heading('New actin joins here',TEAL))
        self.at('Look inside the fan')
        subunits=VGroup(*[Dot(P(4.55,y),radius=.12,color=TEAL) for y in YS])
        self.add(subunits)
        self.at('joins the filaments')
        self.play(*[d.animate.set_x(5.35) for d in subunits],Transform(v[2],edge_view()[2]),run_time=.9,rate_func=linear)
        self.at('at the front edge')
        leads=VGroup(*[Line(P(4.5,y),P(5.35,y),color=TEAL,stroke_width=8) for y in YS])
        self.play(FadeIn(leads),run_time=.4);self.finish()


class S03Pull(SpokenScene):
    def construct(self):
        self.add(edge_view(),heading('Myosin II pulls the network back',RED))
        self.at('Myosyn 2')
        motors=VGroup(*[chip('myosin II',RED,26).move_to(P(-2.6,y+.4)) for y in (YS[1],YS[3])])
        self.add(motors)
        self.at('pulls the network back')
        arrows=VGroup(*[arrow(P(.8,y+.4),P(-.8,y+.4),RED) for y in (YS[1],YS[3])])
        self.play(FadeIn(arrows),run_time=.4)
        self.at('Its own assembly')
        self.play(FadeOut(motors),FadeOut(arrows),run_time=.25)
        self.remove(*[m for m in self.mobjects if isinstance(m,Text)])
        self.add(heading('Assembly also pushes the network back',TEAL))
        self.at('pushes it back too')
        push=VGroup(*[arrow(P(5.2,y+.4),P(3.4,y+.4),TEAL) for y in (YS[1],YS[3])])
        self.play(FadeIn(push),FadeIn(T('push',28,TEAL).move_to(P(2.4,.15))),run_time=.4);self.finish()


class S04Flow(SpokenScene):
    def construct(self):
        v=edge_view();self.add(v,heading('Filaments are taken apart near the centre'))
        moving_dots(self)
        self.at('Near the center')
        self.at('taken apart')
        # Fade the network at its central end: assembly at the front sustains it.
        pieces=VGroup(*[Line(P(-4.7,y),P(-3.7,y),color=BLUE,stroke_width=5) for y in YS])
        self.add(pieces)
        self.play(pieces.animate.shift(LEFT*.3).set_opacity(0),run_time=.7)
        self.at('This backward movement')
        lab=T('retrograde flow',30,RED).move_to(P(0,2.85))
        back=arrow(P(3.8,2.85),P(2.1,2.85),RED)
        self.play(FadeIn(lab),GrowArrow(back),run_time=.4)
        self.at('retrograde flow');self.finish()


class S05Slug(SpokenScene):
    def construct(self):
        self.add(heading('Forscher and Smith · 1988'))
        # Aplysia outline: tapered foot, broad mantle folds, head, rolled rhinophores.
        body=VMobject(color=OUTLINE,fill_color=OUTLINE,fill_opacity=.22)
        body.set_points_smoothly([P(-5,-1.2),P(-3.6,-.5),P(-3.1,1.1),P(-1.2,1.7),P(1.4,.9),P(2.7,.7),P(3.3,1.4),P(4,.9),P(3.5,-.5),P(4.9,-1.1),P(2.2,-1.4),P(-1.7,-1.6),P(-5,-1.2)])
        folds=VGroup(*[ArcBetweenPoints(P(-3+i*.85,-.5),P(-2.3+i*.85,.8),angle=-.8,color=OUTLINE,stroke_width=3) for i in range(5)])
        horns=VGroup(*[RoundedRectangle(width=.25,height=.95,corner_radius=.1,color=OUTLINE,fill_color=OUTLINE,fill_opacity=.4).rotate(a).move_to(P(x,1.6)) for x,a in [(2.8,.25),(3.6,-.25)]])
        eye=Dot(P(3.5,.6),radius=.08,color=TEXT)
        slug=VGroup(body,folds,horns,eye)
        self.add(slug,T('Aplysia (sea slug)',32).move_to(P(0,-2.7)))
        self.at('In 1988');self.at('filmed this');self.at('in a sea slug')
        self.at('with giant')
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not self.mobjects[0]],run_time=.3)
        cone=fan_at(scale=1.85).stretch(.72,1).move_to(P(-1.3,.2))
        typical=fan_at(scale=.36).stretch(.72,1).move_to(P(4.3,.2))
        self.play(FadeIn(cone),FadeIn(typical),run_time=.4)
        self.add(T('typical cone',26).move_to(P(4.3,-1.1)),
                 T('size comparison (schematic)',26).move_to(P(3.4,-2.1)))
        self.add(T('Aplysia: broad, flat growth cone',30,BLUE).move_to(P(0,-2.8)),
                 T('Much larger than a typical growth cone',28).move_to(P(0,-3.3)))
        self.finish()


class S06Drug(SpokenScene):
    def construct(self):
        v=edge_view();self.add(v)
        self.at('They added')
        wash=RoundedRectangle(width=10.85,height=4.85,corner_radius=.44,stroke_width=0,fill_color=RED,fill_opacity=.16).move_to(P(0,.05))
        self.play(FadeIn(wash),FadeIn(heading('Cytochalasin blocks addition at the edge',RED)),run_time=.4)
        self.at('a drug that stops')
        self.at('adding at the front edge')
        self.play(FadeOut(wash),FadeIn(blocked()),run_time=.4);self.finish()


class S07Q(SpokenScene):
    def construct(self):
        g=blocked_question();self.add(g)
        self.at('Addition at the front stops')
        self.at('What happens to')
        self.play(Indicate(g[1],scale_factor=1.04),run_time=.5);self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(blocked_question())
        track=Rectangle(width=4,height=.15,color=OUTLINE).move_to(P(0,-3.25))
        fill=Rectangle(width=4,height=.15,color=TEAL,fill_color=TEAL,fill_opacity=1).move_to(track)
        self.add(track,fill)
        self.play(fill.animate.stretch_to_fit_width(.02).align_to(track,LEFT),run_time=5,rate_func=linear)


class S09Reveal(SpokenScene):
    def construct(self):
        v=edge_view();v[3][1].set_opacity(0);v[1].set_opacity(0)
        g=ValueTracker(0);self.add(v,blocked(),heading('An actin-free band opens'))
        b=band(.015)
        self.add(b)
        # Retain all initial speckles until they leave the central end. No births.
        moving_dots(self,speed=.36,gap=g,replenish=False)
        driver=Mobject()
        def retreat(m,dt):
            g.increment_value(.36*dt)
            for y,ln in zip(YS,v[2]):
                ln.become(filament(y,5.4-g.get_value()))
            b.become(band(g.get_value()))
        self.at('An empty band opens');driver.add_updater(retreat);self.add(driver);self.bring_to_back(driver)
        self.at('and widens')
        self.play(FadeIn(gap_label()),run_time=.35)
        self.at('The rest of the network');self.finish()


class S10Meaning(SpokenScene):
    def construct(self):
        v=edge_view(gap=2);v[3][1].set_opacity(0)
        self.add(v,band(),gap_label(),blocked(),heading('The flow was always there',RED))
        moving_dots(self,right=3.25,speed=.5)
        self.at('So the flow');self.at('Addition at the front')
        self.play(FadeIn(note('Addition had hidden the flow',TEAL,y=-3.65)),run_time=.4);self.finish()


class S11Mts(SpokenScene):
    def construct(self):
        v=edge_view(gap=2);v[3][1].set_opacity(0)
        self.add(v,band(),gap_label(),heading('Microtubules enter the empty band',PURPLE))
        ts=tubes_to(-4.35);self.add(ts,note('Actin had held microtubules back',PURPLE,y=-3.65))
        self.at('microtubules push forward')
        self.play(Transform(ts,tubes_to(5.05)),run_time=3.5,rate_func=linear)
        self.at('into the emptied band')
        self.at('had been holding them back')
        self.finish()


class S12Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(heading('Before and after blocking addition'))
        for x,after in [(-3.15,False),(3.15,True)]:
            # Tall comparison crops preserve 26+ pt labels and give each result 7 s.
            box=RoundedRectangle(width=5.6,height=4.9,corner_radius=.35,color=OUTLINE,fill_color=BLUE,fill_opacity=.07).move_to(P(x,0))
            self.add(box,T('Cytochalasin' if after else 'Before',30,RED if after else TEXT).move_to(P(x,2.75)))
            for y in np.linspace(-1.95,1.9,6):
                self.add(Line(P(x-2.5,y),P(x+(1.2 if after else 2.45),y),color=BLUE,stroke_width=4))
            self.add(Line(P(x-2.5,-.75),P(x+(2.35 if after else -1.2),-.75),color=PURPLE,stroke_width=8),
                     Line(P(x-2.5,.85),P(x+(2.35 if after else -1.2),.85),color=PURPLE,stroke_width=8))
            if after:
                self.add(Rectangle(width=1.25,height=4.55,color=GOLD,stroke_width=3).move_to(P(x+1.9,0)),
                    T('empty band',28,GOLD).move_to(P(x+1.1,-2.9)),
                    Line(P(x+1.9,-2.4),P(x+1.9,-2.65),color=GOLD))
            else:
                self.add(T('actin to the edge',28,BLUE).move_to(P(x,-2.9)))
        self.add(T('Microtubules: held near centre → extend forward',28,PURPLE).move_to(P(0,-3.55)))
        self.wait(7)


class S13Clutch(SpokenScene):
    def construct(self):
        c=clutch_scene(self)
        self.add(heading('Why does the edge advance?'),side_label('clutch hypothesis',YELLOW),
                 note('Mitchison and Kirschner · 1988'))
        self.at('why does the edge');self.at('proposed a clutch')
        self.play(Indicate(c.dashes,scale_factor=1.01),run_time=.4);self.finish()


class S14Engine(SpokenScene):
    def construct(self):
        self.add(heading('Actin network = running engine',BLUE))
        body=RoundedRectangle(width=8,height=2.8,corner_radius=.3,color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to(P(-.4,.9))
        self.add(body,T('actin network',32,BLUE).move_to(body),
                 note('This picture is for moving forward only'))
        self.at('Think of the actin network')
        wheels=VGroup(*[Circle(radius=.95,color=BLUE,stroke_width=6).move_to(P(x,-1.45)) for x in (-2.7,1.5)])
        spokes=VGroup(*[Line(P(x,-1.45),P(x+.8,-1.1),color=TEAL,stroke_width=5) for x in (-2.7,1.5)])
        for spoke in spokes:
            centre=spoke.get_start().copy()
            spoke.add_updater(lambda m,dt,c=centre:m.rotate(-3*dt,about_point=c))
        self.at('a running engine');self.add(wheels,spokes)
        self.at('the ground as the road')
        road=Line(P(-6,-2.45),P(6,-2.45),color=OUTLINE,stroke_width=7)
        self.play(Create(road),FadeIn(T('ground = road',30).move_to(P(4.55,-1.4))),run_time=.4);self.finish()


def equal_bars():
    g=VGroup(T('equal rates',28).move_to(P(-3.8,2)))
    for y,s,col in [(1.15,'added',TEAL),(-.1,'carried back',RED)]:
        g.add(T(s,28,col).move_to(P(-3.8,y+.35)),
            Rectangle(width=2.3,height=.22,stroke_width=0,fill_color=col,fill_opacity=1).move_to(P(-3.8,y-.05)))
    return g


class S15Slip(SpokenScene):
    def construct(self):
        c=clutch_scene(self);self.add(marker(2.2),heading('Clutch disengaged',YELLOW),equal_bars(),note('Equal rates: the edge stays here'))
        self.at('If actin is added');self.at('and carried back');self.at('at the same rate')
        self.at('the engine runs');self.at('the edge goes nowhere');self.finish()


class S16Engage(SpokenScene):
    def construct(self):
        c=clutch_scene(self);self.add(heading('Adhesion molecules',YELLOW),marker(2.2))
        label=note('Adhesion molecules link actin to the ground',YELLOW);self.add(label)
        self.at('Adhesion molecules');self.at('can link the network')
        self.play(c.links.animate.set_value(1),c.clutch.animate.set_value(.4),run_time=.7)
        self.at('the clutch engages')
        self.play(c.clutch.animate.set_value(1),FadeIn(side_label('clutch engaged',YELLOW,y=1.2)),run_time=.55)
        self.at('the backward flow slows')
        self.play(FadeIn(side_label('flow slows',RED,y=.1)),run_time=.3);self.finish()


class S17Push(SpokenScene):
    def construct(self):
        c=clutch_scene(self,True);self.add(marker(2.2),heading('Same actin addition',TEAL))
        self.at('If building stays the same')
        self.at('it now pushes')
        c.lock=False
        # Three seconds of schematic motion per displayed second; addition is unchanged.
        c.driver.clear_updaters()
        c.driver.add_updater(lambda m,dt:c.step(dt*3))
        c.adv_op.set_value(1)
        def advance_bracket():
            x=c.edge.get_value()
            return VGroup(Line(side_p(2.2,-3.0),side_p(max(2.21,x),-3.0),color=GREEN,stroke_width=5),
                Line(side_p(2.2,-2.88),side_p(2.2,-3.12),color=GREEN,stroke_width=4),
                Line(side_p(x,-2.88),side_p(x,-3.12),color=GREEN,stroke_width=4),
                T('advance',28,GREEN).move_to(side_p((2.2+x)/2,-3.55)))
        self.add(always_redraw(advance_bracket))
        self.wait(1.4)
        c.lock=True
        self.finish();self.wait(1.8)


class S18Rule(SpokenScene):
    def construct(self):
        c=clutch_scene(self,True)
        self.add(heading('rate of advance =',GREEN))
        self.at('Put it as bookkeeping');self.at('Advance equals')
        row=VGroup(T('rate of addition',30,TEAL),T('−',30),T('rate of retrograde flow',30,RED)).arrange(RIGHT,buff=.25).move_to(P(0,2.55))
        self.at('actin added at the edge');self.play(FadeIn(row[0]),run_time=.35)
        self.at('minus actin carried back');self.play(FadeIn(row[1:]),run_time=.4)
        self.add(side_label('grip reduces flow',YELLOW,y=.5));self.finish()


class BeadCone(Cone):
    def __init__(self):
        self.local_grip=ValueTracker(0)
        super().__init__(edge=2.2,lock=True)
    def step(self,dt):
        for i,d in enumerate(self.d):
            x=self.edge.get_value()-.15-d
            y=BASE+self.r[i]*prof(x,self.edge.get_value(),self.sh.get_value(),self.h)
            f=F_OFF*(1-.87*self.local_grip.get_value()) if abs(y-.05)<1.3 else F_OFF
            self.d[i]=(d+f*dt)%LMAX
        self.refresh()
    def refresh(self):
        super().refresh()
        length=max(.5,F_OFF*5.5*(1-.87*self.local_grip.get_value()))
        for k,a in enumerate(self.flow):
            y=BASE+self.h*(.25+.25*k)
            a.become(arrow(side_p(.55,y),side_p(.55-length,y),RED))


def bead_labels(scene):
    scene.add(T('holder',28).move_to(P(5.5,1.85)),
        T('bead coated with',26,YELLOW).move_to(P(-4.45,.9)),
        T('adhesion molecule',26,YELLOW).move_to(P(-4.45,.35)),
        Line(P(4.9,-.35),P(5.7,-.65),color=YELLOW))


class S19Bead(SpokenScene):
    def construct(self):
        c=BeadCone();c.attach(self);self.add(heading('Suter and colleagues · 1998'))
        self.at('Suter and colleagues');self.at('They held a bead')
        b=bead();b[1].set_opacity(0)
        self.play(FadeIn(b),FadeIn(T('holder',28).move_to(P(5.5,1.85))),run_time=.4)
        self.at('coated with an adhesion molecule')
        self.play(b[1].animate.set_opacity(1),run_time=.3)
        bead_labels(self)
        self.at('against the edge');self.finish()


class S20Slows(SpokenScene):
    def construct(self):
        c=BeadCone();c.local_grip.set_value(1);c.refresh();c.attach(self)
        self.add(bead(),heading('Flow slowed here',RED),note('Flow slows in line with the held bead',RED));bead_labels(self)
        self.at('Behind the bead');self.at('the backward flow slowed')
        self.finish();self.wait(.8)


def value_panel(x,title,flow):
    addition=4.;advance=addition-flow;scale=.93
    title=T(title,30).move_to(P(x,2.55))
    axis=VGroup(Line(P(x-2.05,-2.2),P(x-2.05,1.9),color=OUTLINE,stroke_width=2),
        Line(P(x-2.05,-2.2),P(x-2.05+4*scale,-2.2),color=OUTLINE,stroke_width=2))
    for val in (0,2,4):
        xx=x-2.05+val*scale
        axis.add(Line(P(xx,-2.2),P(xx,-2.35),color=OUTLINE),M(str(val),26).move_to(P(xx,-2.6)))
    axis.add(T('micrometres per minute',26).move_to(P(x,-3.15)))
    rows=VGroup()
    for y,name,val,col in [(1.4,'added',addition,TEAL),(0,'flow',flow,RED),(-1.4,'advance',advance,GREEN)]:
        bar=Rectangle(width=val*scale,height=.38,stroke_width=0,fill_color=col,fill_opacity=1).move_to(P(x-2.05+val*scale/2,y))
        rows.add(VGroup(T(name,28,col).move_to(P(x-1.35,y+.5)),bar,M(f'{val:.1f}',28,col).move_to(P(x+2.25,y))))
    return VGroup(title,axis,*rows)


class S21Bars(SpokenScene):
    def construct(self):
        left=value_panel(-3.25,'Before',3.5);right=value_panel(3.05,'Under the bead',.5)
        self.add(heading('Illustrative values'),left[:3],right[:3])
        self.at('With illustrative numbers');self.at('flow falls from')
        self.play(FadeIn(left[3]),run_time=.35)
        self.at('to half a');self.play(FadeIn(right[3]),run_time=.35)
        self.at('Building stays the same')
        self.play(Indicate(left[2],scale_factor=1.02),Indicate(right[2],scale_factor=1.02),run_time=.4)
        self.at('so the edge moves')
        self.play(FadeIn(left[4]),FadeIn(right[4]),run_time=.35)
        self.at('seven times faster')
        # Keep numerical result readable after the fast closing spoken phrase.
        self.play(Transform(self.mobjects[0],heading('advance: 3.5 / 0.5 = 7 times faster',GREEN)),run_time=.4)
        self.finish();self.wait(1.2)


class S22Bridge(SpokenScene):
    def construct(self):
        self.add(heading('Grip or building can differ'))
        base=fan_at(scale=1.4,theta=PI/2).move_to(P(0,-.7));self.add(base)
        self.add(DashedLine(P(0,-3),P(0,2.45),color=TEXT,stroke_width=3,dash_length=.18))
        grips=VGroup(*[VGroup(
            Line(P(x,-.05),P(x,.7),color=YELLOW,stroke_width=10),
            Line(P(x,.7),P(x+.5,.7),color=YELLOW,stroke_width=10),
            Line(P(x+.5,.7),P(x+.5,.35),color=YELLOW,stroke_width=10)) for x in (-1.6,1.1)])
        grips.shift(UP*.3)
        self.add(grips,T('grip',28,YELLOW).move_to(P(-3,.7)),T('grip',28,YELLOW).move_to(P(3,.7)))
        self.at('Now make the grip');self.at('or the building');self.at('unequal across')
        # One hook versus three hooks expresses grip without dimming either side.
        extra=VGroup(grips[1].copy().shift(RIGHT*.55),grips[1].copy().shift(LEFT*.55))
        self.add(extra)
        self.at('the two sides')
        def unequal(p):
            fraction=np.clip((p[0]+1.8)/3.6,0,1)
            return p+UP*((.2+1.2*fraction)*np.clip((p[1]+3)/3,0,1))
        aleft=arrow(P(-2.9,1.1),P(-2.9,1.35),GREEN)
        aright=arrow(P(2.9,1.1),P(2.9,2.5),GREEN)
        self.play(GrowArrow(aleft),GrowArrow(aright),base.animate.apply_function(unequal),
            grips[0].animate.shift(UP*.3),grips[1].animate.shift(UP*1.15),extra.animate.shift(UP*1.15),run_time=.8)
        self.add(note('Different advance on the two sides',GREEN,y=-3.55));self.finish();self.wait(.6)


class S23Takeaway(SpokenScene):
    def construct(self):
        c=clutch_scene(self,True);self.add(heading('Same building',TEAL),marker(2.2))
        self.at('Carry one idea');self.at('grip can speed the edge')
        c.lock=False
        self.play(c.adv_op.animate.set_value(1),FadeIn(side_label('edge advance',GREEN,y=.9)),run_time=.4)
        self.at('holding back the flow')
        self.play(FadeIn(note('Grip holds back the flow',YELLOW)),run_time=.4)
        self.at('with no faster building');self.finish()


class S24End(EndCard):
    LINE='Grip can speed the edge just by holding back the flow.'
    def construct(self):
        line=VGroup(T('Grip can speed the edge',38,font=TITLE_FONT),T('just by holding back the flow.',38,font=TITLE_FONT)).arrange(DOWN,buff=.25)
        self.play(FadeIn(line),run_time=.6)
        self.play(FadeIn(T('biochemistrypedia.com',26,TEAL).move_to(P(0,-1.7))),run_time=.4)
        self.finish()
