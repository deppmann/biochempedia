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
SUBY = -1.54     # the substrate
H = 3.6          # height of the flat fan in the side view
HS = 0.9         # height of the axon shaft
XL = -6.1        # left end of the drawn axon
LMAX = 4.2       # how far behind the edge the actin network reaches
A_RATE = 0.30    # actin addition at the edge
F_OFF = 0.30     # retrograde flow with the clutch off
F_ON = 0.10      # retrograde flow with the clutch on


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
            op = min(1.0, (d + 0.12) / 0.25) * min(1.0, (LMAX - d) / 0.7) * dop
            dash.set_stroke(col, width=5.5, opacity=op)
        fop = self.flow_op.get_value()
        L = max(0.25, self.Fv * 6.0)
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


# All track curves below are integrated from the reference kinematic equations.
# They illustrate a population, and are explicitly labelled schematic, not data.

def tag(s, x=0, y=3.15, c=TEXT, size=30):
    return T(s, size=size, color=c, line_spacing=.9).move_to(P(x,y))


def leader(s, xy, dest, color=TEXT, size=28):
    t=tag(s,*xy,c=color,size=size)
    start=t.get_right() if dest[0]>xy[0] else t.get_left()
    return VGroup(Line(start,dest,color=color,stroke_width=2),t)


def fan_at(x=0,y=0,scale=1,theta=0,tubules=False,bulge=0):
    # Top view: a continuous lamellipodial sheet between radial filopodia.
    # Index 0=sheet, 1=filopodia, 2=tubules, 3=peripheral actin bundles.
    angles=np.linspace(-1.03,1.03,45)
    arc=[P((1.65+bulge*max(0,np.sin(a)))*np.sin(a),
           (1.65+bulge*max(0,np.sin(a)))*np.cos(a)) for a in angles]
    sheet=VMobject(color=BLUE,stroke_width=3,fill_color=BLUE,fill_opacity=.18)
    sheet.set_points_as_corners([P(-.38,-1.65),P(.38,-1.65)]+list(reversed(arc))+[P(-.38,-1.65)])
    fil=VGroup(); bundles=VGroup()
    for a in np.linspace(-.98,.98,9):
        r=1.65+bulge*max(0,np.sin(a))
        fil.add(Line(P(r*np.sin(a),r*np.cos(a)),P((r+.48)*np.sin(a),(r+.48)*np.cos(a)),color=BLUE,stroke_width=4))
        bundles.add(Line(P(.65*np.sin(a),.65*np.cos(a)),P(r*np.sin(a),r*np.cos(a)),color=BLUE,stroke_width=2,stroke_opacity=.45))
    mts=VGroup(*[Line(P(j*.13,-1.6),P(j*.36,.45),color=PURPLE,stroke_width=5) for j in range(-2,3)])
    if not tubules: mts.set_opacity(0)
    return VGroup(sheet,fil,mts,bundles).scale(scale,about_point=ORIGIN).rotate(theta,about_point=ORIGIN).shift(P(x,y))


def top(tubules=False):
    return fan_at(0,-.25,1.35,tubules=tubules)


def dish():
    return RoundedRectangle(width=12.4,height=5.5,corner_radius=.45,color=GREY,stroke_width=2).move_to(P(0,-.1))


def neuron(end=-1.2):
    body=Circle(radius=1.05,color=OUTLINE,fill_color=BLUE,fill_opacity=.18).move_to(P(-4.8,-.4))
    branches=VGroup(*[Line(P(-4.8,-.4),P(-4.8+1.5*np.cos(a),-.4+1.5*np.sin(a)),color=OUTLINE,stroke_width=5) for a in (1.7,2.5,3.8,4.5)])
    ax=Line(P(-3.75,-.4),P(end-1.32,-.4),color=OUTLINE,stroke_width=17)
    f=fan_at(end,-.4,.8,theta=-PI/2)
    partner=Circle(radius=.9,color=OUTLINE,fill_color=BLUE,fill_opacity=.15).move_to(P(5.1,.4))
    return VGroup(dish(),branches,body,ax,f,partner)


def pipette(x=3.7,y=1.6):
    return Polygon(P(x,y),P(x+.55,y+.9),P(x+1.15,y+.9),color=ORANGE,stroke_width=3,fill_color=ORANGE,fill_opacity=.2)


def field():
    # Continuous raster of c~1/r: the alpha channel is sampled directly from
    # the point-source model, with no tile boundaries or decorative dot grid.
    xx,yy=np.meshgrid(np.linspace(-5.6,5.1,640),np.linspace(2.65,-2.5,320))
    r=np.maximum(.25,np.hypot(xx-3.7,yy-1.6))
    rgba=np.zeros((320,640,4),dtype=np.uint8)
    rgba[:,:,:3]=[242,158,76]
    rgba[:,:,3]=np.uint8(255*(.015+.38/(1+r)))
    image=ImageMobject(rgba).stretch_to_fit_width(10.7).stretch_to_fit_height(5.15)
    return image.move_to(P(-.25,.075))


def assay():
    f=fan_at(-1,-.35,1.2,tubules=True)
    shaft=Line(P(-1,-2.9),P(-1,-2.2),color=OUTLINE,stroke_width=17)
    return Group(field(),shaft,f,pipette(),tag('pipette',4.5,2.95,ORANGE,28),tag('enlarged cone · distance compressed',y=-3.2,c=GREY,size=26))


def edges(equal=False,x=-1,y=-.35,scale=1.2,near_right=True):
    # Exaggerate the small concentration contrast so it survives a draft render.
    bars=VGroup()
    for right in (False,True):
        near=right == near_right
        height=.8 if equal or near else .46
        opacity=.95 if equal or near else .42
        xx=x+(1 if right else -1)*1.35*scale
        bars.add(Line(P(xx,y+.7-height/2),P(xx,y+.7+height/2),
                      color=ORANGE,stroke_width=16,stroke_opacity=opacity))
    return bars


def bath(question=True):
    dots=VGroup(*[Dot(P(x,y),radius=.035,color=ORANGE,fill_opacity=.5) for x in np.linspace(-5.8,5.8,40) for y in np.linspace(-2.5,2.25,18)])
    cones=VGroup(*[fan_at(x,-.25,1.12) for x in (-4,0,4)])
    q=VGroup(*[tag('?',x,2.4,ORANGE,32) for x in (-4,0,4)])
    return VGroup(dish(),dots,cones,tag('10× cue · equal on both sides',y=3.15,c=ORANGE,size=30),q,
                  tag('Do growth cones turn harder?',y=-3.25,size=34))


def tracks(bias=0,width=1):
    if bias:
        # Retain the already reviewed gradient population unchanged.
        paths=VGroup()
        for i in range(7):
            for sign in (-1,1):
                p=P(sign*(i%3)*.10,-2.2); th=PI/2; pts=[p.copy()]
                for step in range(int((8.2+.30*i)/.06)):
                    t=step*.06
                    delta=bias+sign*(.13+.025*i+.13*np.sin(.9*t+i*.7))
                    th+=.3*delta*.06
                    p+=.45*P(np.cos(th),np.sin(th))*.06
                    pts.append(p.copy())
                paths.add(VMobject(color=ORANGE,stroke_width=3,stroke_opacity=.8).set_points_as_corners(pts))
        return paths.stretch(width,0)
    # Independently seeded rate fluctuations, integrated from the reference
    # dtheta/dt=.3*(vL-vR), dp/dt=mean(vL,vR)*heading equations.
    rng=np.random.default_rng(29)
    samples=[]
    for i in range(14):
        p=P(rng.uniform(-.35,.35),-2.2); th=PI/2; pts=[p.copy()]
        duration=rng.uniform(5.0,11.0)
        drift=rng.uniform(-.6,.6) if i>3 else rng.uniform(-.06,.06)
        phase=rng.uniform(0,2*PI)
        for step in range(int(duration/.06)):
            t=step*.06
            delta=bias+drift+.32*np.sin(.95*t+phase)
            th+=.3*delta*.06
            p+=.45*P(np.cos(th),np.sin(th))*.06
            pts.append(p.copy())
        samples.append(np.array(pts))
    # Remove population drift without pairing/mirroring individual paths.
    # A constant heading rotation retains every integrated path's geometry.
    if not bias:
        displacement=np.mean([p[-1]-p[0] for p in samples],axis=0)
        angle=PI/2-math.atan2(displacement[1],displacement[0])
        rot=np.array([[np.cos(angle),-np.sin(angle),0],
                      [np.sin(angle),np.cos(angle),0],[0,0,1]])
        samples=[(p-p[0])@rot.T+p[0] for p in samples]
    paths=VGroup(*[VMobject(color=ORANGE if bias else BLUE,stroke_width=3,
                           stroke_opacity=.85).set_points_as_corners(p) for p in samples])
    return paths.stretch(width,0)


def compare(amount=False):
    left=tracks(-.26).shift(LEFT*3.25)
    right=tracks().shift(RIGHT*3.15)
    source=VGroup(pipette(-.95,1.95).scale(.7,about_point=P(-.95,1.95)),tag('attractant',-1.3,3.2,ORANGE,26))
    dots=VGroup(*[Dot(P(x,y),radius=.035,color=ORANGE,fill_opacity=.32) for x in np.linspace(1,5.8,23) for y in np.linspace(-2.25,2.35,19)])
    leftcap=tag('difference → direction',-3.25,-2.85,size=28)
    rightcap=tag('amount: how strongly\nit responds' if amount else 'no preferred direction',3.15,-2.95,size=28)
    return VGroup(dots,left,right,source,tag('gradient',-4.1,3.2,ORANGE,30),tag('10× cue · uniform',3.4,3.2,ORANGE,30),leftcap,rightcap,
                  tag('schematic tracks',-3.25,-3.5,c=GREY,size=26),
                  arrow(P(3.15,-2.2),P(3.15,2.25),GREY,w=3,tip=.2))


def formula():
    return VGroup(T('advance',size=34,color=GREEN),T('=',size=34),T('added',size=34,color=TEAL),T('−',size=34),T('slides back',size=34,color=RED)).arrange(RIGHT,buff=.25).move_to(P(0,3.1))


def rule_labels(c=None):
    labels=VGroup(tag('simplified culture model',y=-3.3,c=GREY,size=26),
                  leader('front edge',(4.6,1.6),P(1.3,-.1),BLUE),
                  tag('dish surface',4.3,-2.1,GREY,26))
    if c is not None:
        labels[1][0].add_updater(lambda m: m.put_start_and_end_on(labels[1][1].get_left(),P(c.edge.get_value(),-.1)))
    return labels


class S00Title(TitleCard):
    LESSON='The Growth Cone: The Tip That Steers the Axon'
    TITLE='The Tip That Reads a Difference'
    def construct(self):
        lesson=VGroup(T('The Growth Cone:',26,color=GREY),T('The Tip That Steers the Axon',26,color=GREY)).arrange(DOWN,buff=.14)
        title=VGroup(T('The Tip That Reads',48,font=TITLE_FONT),T('a Difference',48,font=TITLE_FONT)).arrange(DOWN,buff=.2)
        self.add(VGroup(T('BIOCHEMISTRYPEDIA',26,color=TEAL),lesson,title,Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.4))
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(neuron(),tag('The tip that reads a difference',y=3.2,size=36),tag('Which way?',.5,1.6,size=36))
        self.at('tip of a growing axon')
        self.play(Indicate(self.mobjects[0][4],color=BLUE,scale_factor=1.08),run_time=.6)
        self.finish()


class S02Axon(SpokenScene):
    def construct(self):
        n=neuron(); self.add(n)
        axlabel=leader('axon',(-2.4,-2.4),P(-3.2,-.4),GREY)
        cone_label=leader('growth cone',(.4,1.9),P(-.05,.15),BLUE)
        self.at('An axon')
        self.play(FadeIn(axlabel),FadeIn(cone_label),run_time=.3)
        self.at('sends out')
        self.play(Transform(n,neuron(2.3)),Transform(cone_label,leader('growth cone',(2.4,2),P(3.2,.4),BLUE)),run_time=.9)
        self.at('reach its partner')
        self.play(Indicate(n[5],scale_factor=1.08),run_time=.5)
        self.finish()


class S03Fan(SpokenScene):
    def construct(self):
        n=neuron(2.3); self.add(n)
        self.at('a flat')
        self.play(ReplacementTransform(n,top()),run_time=.65)
        self.at('the growth cone')
        self.play(FadeIn(tag('growth cone',y=3.2,c=BLUE,size=32)),run_time=.3)
        self.finish()


class S04Parts(SpokenScene):
    def construct(self):
        f=top(); self.add(f)
        central=Ellipse(width=1.7,height=2.9,color=PURPLE,stroke_width=2).move_to(P(0,-.85))
        peripheral=Arc(radius=2.18,start_angle=.4,angle=PI-.8,color=BLUE,stroke_width=5).shift(DOWN*.25)
        self.at('Microtubules fill')
        self.play(f[2].animate.set_opacity(1),Create(central),run_time=.4)
        self.at('center of the fan')
        self.play(FadeIn(leader('microtubules\ncentral domain',(-4,-1.35),P(-.8,-1),PURPLE)),run_time=.35)
        self.at('fills its edge')
        self.play(Create(peripheral),FadeIn(leader('actin\nperipheral domain',(4.25,1.65),P(1.65,1.2),BLUE)),run_time=.4)
        self.at('thin spikes')
        self.play(FadeIn(leader('filopodia',(-4.3,2.65),P(-1.8,1.8),BLUE)),run_time=.25)
        self.at('flat sheets')
        self.play(f[0].animate.set_fill(opacity=.32),FadeIn(leader('lamellipodia',(4.25,-1.4),P(1.3,.1),BLUE)),run_time=.3)
        self.finish()


class S05Filopodia(SpokenScene):
    def construct(self):
        f=top(True)
        sheet_label=leader('lamellipodia',(4.4,.2),P(1.45,1.4),BLUE)
        self.add(f,tag('filopodia',y=3.2,c=BLUE,size=32),sheet_label)
        # Oblique contact view: the substrate is beneath the probing tips.
        surface=Line(P(-5.7,-2.35),P(5.7,-2.35),color=GREY,stroke_width=5)
        self.at('feelers and feet')
        oblique=fan_at(0,.3,1.4,theta=-PI/2,tubules=True).stretch(.8,1,about_point=P(0,.3))
        self.play(Transform(f,oblique),Create(surface),
                  Transform(sheet_label,leader('lamellipodia',(-3.8,1.6),P(1.9,.95),BLUE)),
                  FadeIn(tag('surface contact · oblique view',y=-3.2,c=GREY,size=28)),run_time=.45)
        self.at('sampling the ground')
        sample=f[1][5]
        self.play(sample.animate.put_start_and_end_on(sample.get_start(),P(2.8,-2.35)),run_time=.35)
        self.play(sample.animate.put_start_and_end_on(sample.get_start(),P(2.8,-1.7)),run_time=.3)
        self.add(leader('sampling',(4.5,-.4),P(2.8,-1.7),BLUE))
        self.at('gripping it')
        attach=f[1][7]; attach2=f[1][8]
        self.play(attach2.animate.put_start_and_end_on(attach2.get_start(),P(.9,-2.35)),
                  FadeIn(Dot(P(.9,-2.35),radius=.12,color=YELLOW)),
                  attach.animate.put_start_and_end_on(attach.get_start(),P(1.8,-2.35)),
                  FadeIn(Dot(P(1.8,-2.35),radius=.12,color=YELLOW)),
                  FadeIn(leader('grip',(4.5,-1.65),P(1.8,-2.35),YELLOW)),run_time=.3)
        self.finish()


class S06Cues(SpokenScene):
    def construct(self):
        f=top(True); self.add(f,tag('guidance cues',y=3.2,c=ORANGE,size=32))
        left=cloud_cue(-4,1.25); right=cloud_cue(4,1.25)
        self.at('Molecules outside')
        self.play(FadeIn(left),FadeIn(right),run_time=.3)
        left.add_updater(lambda m,dt:m.rotate(.15*dt,about_point=P(-4,1.25)))
        right.add_updater(lambda m,dt:m.rotate(-.15*dt,about_point=P(4,1.25)))
        self.at('attract')
        self.play(GrowArrow(arrow(P(-2,.8),P(-3.4,1.2),GREEN)),FadeIn(tag('attract',-4,-.1,GREEN,30)),run_time=.25)
        self.at('repel')
        self.play(GrowArrow(arrow(P(3.4,1.2),P(2,.8),RED)),FadeIn(tag('repel',4,-.1,RED,30)),run_time=.25)
        self.finish()


def cloud_cue(x,y):
    return VGroup(*[Dot(P(x+.5*np.cos(a),y+.5*np.sin(a)),radius=.09,color=ORANGE) for a in np.linspace(0,2*PI,7,endpoint=False)])


class S07Pipette(SpokenScene):
    def construct(self):
        g=assay(); self.add(g[1:3],g[5])
        self.at('a fine pipette')
        self.play(FadeIn(g[3:5]),run_time=.3)
        self.at('releases a cue')
        self.play(FadeIn(g[0]),run_time=.5)
        self.bring_to_front(g[1:5]); self.finish()


class S08Thins(SpokenScene):
    def construct(self):
        self.add(assay(),edges(),tag('far',-3.25,1.15,ORANGE,28),
                 tag('near',.9,1.25,ORANGE,28))
        self.at('thins with distance')
        self.add(tag('cue fades with distance',y=3.2,c=ORANGE,size=30))
        self.at('the near side')
        self.play(FadeIn(leader('a little more',(3.35,-.75),P(.62,.4),ORANGE)),run_time=.3)
        self.at('the far side')
        self.play(FadeIn(leader('a little less',(-4.6,-.75),P(-2.62,.4),ORANGE)),run_time=.3)
        self.finish()


class S09Tenth(SpokenScene):
    def construct(self):
        f=fan_at(-3,-.15,1.3,tubules=True)
        self.add(f,tag('Standard pipette assay',x=2.7,y=3.25,size=26),pipette(3.7,1.5),tag('pipette',4.65,2.75,ORANGE,28))
        # Bracket spans the sheet's true lateral diameter, not the shaft.
        a,b=P(-4.84,2.7),P(-1.16,2.7)
        bracket=VGroup(Line(a,b,color=GREY),Line(a+UP*.14,a+DOWN*.14,color=GREY),Line(b+UP*.14,b+DOWN*.14,color=GREY),tag('10 µm',-3,3.25,GREY,30))
        dist=VGroup(Line(P(-1.16,.95),P(.7,1.05),color=GREY),Line(P(1.25,1.2),P(3.7,1.5),color=GREY),
                    Line(P(.78,.9),P(.95,1.25),color=GREY),Line(P(1.02,.97),P(1.19,1.32),color=GREY),tag('100 µm',1.6,1.95,GREY,30))
        self.at('the standard assay')
        self.play(FadeIn(bracket),FadeIn(dist),run_time=.3)
        self.at('only about')
        self.play(FadeIn(chip('near side\n5–10% more',ORANGE,size=38).move_to(P(3,-1.05))),run_time=.35)
        self.add(tag('enlarged cone · broken distance',y=-3.15,c=GREY,size=26)); self.finish()


class S10Q(SpokenScene):
    def construct(self):
        g=bath(); self.add(g[0],g[2:])
        self.at('flood the whole dish')
        self.play(FadeIn(g[1]),run_time=.7)
        self.bring_to_front(g[2:]); self.finish()


class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(bath())
        track=Circle(radius=.32,color=GREY,stroke_width=3).move_to(P(5.9,3.15))
        arc=Arc(radius=.32,start_angle=PI/2,angle=2*PI-.001,color=YELLOW,stroke_width=6).move_arc_center_to(P(5.9,3.15))
        self.add(track,arc)
        self.play(Uncreate(arc),run_time=5,rate_func=linear)


class S12Reveal(SpokenScene):
    def construct(self):
        g=bath(); self.add(g[0],g[1],g[3],g[2])
        self.at('across many cones')
        population=tracks().stretch_to_fit_width(10.3).stretch_to_fit_height(4.15).move_to(P(0,-.1))
        self.play(FadeOut(g[2]),Create(population),run_time=.7)
        self.at('no net turn')
        self.play(FadeIn(tag('no net turn · mean ≈ 0–1°',y=-3.2,size=34)),GrowArrow(arrow(P(0,-2.25),P(0,2.5),GREY,w=4)),run_time=.35)
        self.add(tag('schematic tracks',-4.55,-2.5,GREY,26))
        self.at('no difference between')
        bars=edges(True,x=4.7,y=-.5,scale=.55)
        self.play(FadeIn(bars),FadeIn(tag('equal edges',4.6,1.5,ORANGE,26)),run_time=.3)
        self.finish()


class S13Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(compare()); self.wait(3)


class S14Difference(SpokenScene):
    def construct(self):
        g=compare(); self.add(g)
        self.at('gives the direction')
        self.play(Indicate(g[1],scale_factor=1.025),run_time=.4)
        self.at('The overall amount')
        self.play(Transform(g[7],tag('amount: how strongly\nit responds',3.15,-2.95,size=28)),g[0].animate.set_opacity(.85),run_time=.4)
        self.finish()


class S15Rule1(SpokenScene):
    def construct(self):
        c=Cone(edge=1.3,flow_op=0); c.attach(self)
        self.add(rule_labels(c))
        eq=formula(); self.add(eq[:2])
        self.at('The edge moves forward')
        self.play(Indicate(c.outline,scale_factor=1.01),run_time=.4)
        self.at('actin added there')
        self.play(FadeIn(eq[2]),FadeIn(leader('new actin',(4.5,.5),P(1.0,-.4),TEAL)),run_time=.3)
        self.at('minus the actin')
        self.play(FadeIn(eq[3:]),c.flow_op.animate.set_value(1),run_time=.3)
        self.finish()


class S16Rule2(SpokenScene):
    def construct(self):
        c=Cone(edge=1.3); c.attach(self)
        self.add(rule_labels(c),formula())
        for link in c.linkset:
            link[1].scale(1.6); link[2].scale(1.6)
        self.at('Grip on the ground')
        self.play(c.links.animate.set_value(1),FadeIn(leader('grip · clutch',(-2,-2.25),P(-.8,-1.6),YELLOW)),run_time=.3)
        self.at('holds back part')
        self.play(c.clutch.animate.set_value(1),c.adv_op.animate.set_value(1),FadeIn(tag('advance',4.4,-.8,GREEN,28)),run_time=.4)
        self.finish()


def remodel_inset(stage=0):
    # Two explicit panels preserve the order; the alternative reverses it.
    panels=VGroup()
    for i,x in enumerate((2.25,4.85)):
        box=RoundedRectangle(width=2.4,height=3.1,color=GREY,
                             corner_radius=.12).move_to(P(x,-.35))
        mt_first=stage==2
        bulge=.9 if not mt_first or i else 0
        f=fan_at(x,-.45,.55,tubules=True,bulge=bulge)
        if (not mt_first and i==0):
            f[2].set_opacity(.2)
        else:
            for line in f[2]:
                line.put_start_and_end_on(line.get_start(),line.get_end()+P(.46,.4))
        label=('microtubules' if i==0 else 'edge follows') if mt_first else ('edge bulges' if i==0 else 'tubules enter')
        panels.add(VGroup(box,f,tag(label,x,-2.25,PURPLE if mt_first or i else BLUE,22)))
    return VGroup(panels,arrow(P(3.48,-.25),P(3.62,-.25),GREY,w=3,tip=.1),
                  tag('or microtubules first' if stage==2 else 'actin → microtubules',3.55,1.65,
                      PURPLE if stage==2 else TEXT,24))


class S17Rule3(SpokenScene):
    def construct(self):
        # The entire remodelling scene is seen from above.
        view_label=tag('top view',y=3.2,c=GREY,size=28)
        self.add(view_label,tag('simplified culture model',y=-3.35,c=GREY,size=26))
        side=Ellipse(width=5.2,height=1.3,color=BLUE,fill_color=BLUE,fill_opacity=.18).move_to(P(-2.5,-.5))
        self.add(side)
        self.at('A turn sticks')
        f=fan_at(-2.7,-.2,1.3,tubules=True,bulge=.5)
        inset=remodel_inset(0)
        self.play(ReplacementTransform(side,f),FadeIn(leader('near',(.5,2.1),P(-.7,1.1),ORANGE)),FadeIn(inset),FadeIn(pipette(-.5,1.45).scale(.55,about_point=P(-.5,1.45))),run_time=.5)
        self.at('microtubules move in')
        targets=VGroup(*[Line(P(-2.7+j*.14,-2.25),P(-1.45+j*.19,1.3+j*.12),color=PURPLE,stroke_width=5) for j in range(-2,3)])
        self.play(Transform(f[2],targets),run_time=.5)
        self.at('build new axon')
        # Keep the front arc attached to its filopodia while the rear narrows.
        angles=np.linspace(1.03,-1.03,45)
        front=[P(-2.7+1.3*(1.65+.5*max(0,np.sin(a)))*np.sin(a),
                 -.2+1.3*(1.65+.5*max(0,np.sin(a)))*np.cos(a)) for a in angles]
        consolidated=f[0].copy().set_points_as_corners(
            [P(-3,-2.7),P(-2.4,-2.7),P(-2.4,-.8)]+front+[P(-3,-.8),P(-3,-2.7)])
        shaft=Line(P(-2.7,-2.7),P(-2.7,-1.25),color=OUTLINE,stroke_width=18,stroke_opacity=.45)
        new_mts=VGroup(*[VMobject(color=PURPLE,stroke_width=5).set_points_smoothly(
            [P(-2.7+j*.09,-2.65),P(-2.65+j*.11,-.7),P(-1.45+j*.19,1.3+j*.12)]) for j in range(-2,3)])
        self.play(Create(shaft),Transform(f[0],consolidated),Transform(f[2],new_mts),run_time=.45)
        self.play(Transform(inset,remodel_inset(1)),run_time=.3)
        self.at('can also start')
        self.play(Transform(view_label,tag('Microtubules can also start a turn',y=3.2,c=PURPLE,size=28)),run_time=.3)
        self.at('the turn themselves')
        self.play(Transform(inset,remodel_inset(2)),run_time=.45)
        self.finish()


class S18Next1(SpokenScene):
    def construct(self):
        c=Cone(edge=1.3,clutch=1,links=1,adv_op=1); c.attach(self)
        self.add(tag('1 / 3',-5.5,3.2,c=GREY,size=36),tag('Actin slides back.\nHow does the edge advance?',y=-2.65,size=32),
                  tag('simplified culture model',y=-3.5,c=GREY,size=26))
        self.at('move forward')
        self.play(Indicate(c.adv,scale_factor=1.08),run_time=.4); self.finish()


class S19Next2(SpokenScene):
    def construct(self):
        self.add(top(True),tag('2 / 3',-5.5,3.2,c=GREY,size=36),tag('A small difference. A whole turn?',y=-3.15,size=34),edges(x=0,y=-.3,scale=1.35),pipette(4.6,1.7),
                  leader('far',(-4.4,.4),P(-1.82,.4),ORANGE,size=28),
                  leader('near: 5–10%\ndifference',(4.4,.4),P(1.82,.4),ORANGE,size=28))
        self.at('a turn of')
        self.play(Indicate(self.mobjects[0][0],scale_factor=1.04),run_time=.4); self.finish()


class S20Next3(SpokenScene):
    def construct(self):
        f=top(True)
        self.add(f,tag('3 / 3',-5.5,3.2,c=GREY,size=36),tag('Can the tip decide alone?',y=-3.15,size=36))
        self.at('make that decision')
        self.play(Indicate(f[0],scale_factor=1.04),run_time=.5); self.finish()


class S21Takeaway(SpokenScene):
    def construct(self):
        f=fan_at(0,-.2,1.12,tubules=True)
        self.add(f,tag('Carry one idea',y=3.25,size=34),edges(x=0,y=-.2,scale=1.12),
                 leader('far',(-4,.7),P(-1.5,.5),ORANGE),leader('near',(4,.7),P(1.5,.5),ORANGE),pipette(4.6,1.7))
        self.at('A cue gives')
        self.play(FadeIn(tag('A cue gives a direction\nby making the two sides differ.',y=-3.0,size=32)),run_time=.3)
        self.finish()


class S22End(EndCard):
    LINE='A cue gives a direction by making the two sides differ.'
    def construct(self):
        self.add(VGroup(T('A cue gives a direction',40,font=TITLE_FONT),T('by making the two sides differ.',40,font=TITLE_FONT),T('biochemistrypedia.com',26,color=TEAL)).arrange(DOWN,buff=.4))
        self.finish()
