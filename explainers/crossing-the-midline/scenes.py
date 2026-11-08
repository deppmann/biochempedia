"""Chapter 1: schematic anatomy, with word-synchronised progressive growth.
COLOR MAP: BLUE axons/cones; RED Slit/push/stop; YELLOW Robo;
PURPLE #B58CD9 Comm; ORANGE #F29E4C mammalian Robo3;
TEAL timing; GREY anatomy; GOLD shared midline highlight.
Threshold plot: normal-CDF response, Phi((push-theta)/sigma).
Illustrative theta=.50, sigma=.075 (not the lesson's fitted dosage-margin
parameters: that margin is explicitly NOT literal Slit-dependent push).
"""
import math
import numpy as np
from bp_style import *

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def label(txt, x, y, size=28, color=TEXT):
    return T(txt, size=size, color=color).move_to([x, y, 0])


def strip(x, y0, y1, w=.8, color=GREY):
    return RoundedRectangle(corner_radius=.14, width=w, height=y1-y0,
        stroke_color=color, stroke_width=3, fill_color=color,
        fill_opacity=.22).move_to([x, (y0+y1)/2, 0])


def slit_dot(x, y, r=.13):
    return Dot([x, y, 0], radius=r, color=RED)


def make_cone(x, y, s=1., color=BLUE):
    body = Circle(radius=.28*s, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=.5)
    fil = VGroup(*[Line(.26*s*np.array([np.cos(a), np.sin(a), 0]),
        .55*s*np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=3)
        for a in (-.8, -.3, .3, .8)])
    return VGroup(body, fil).move_to([x, y, 0])


def ear(x, y, s=1):
    # An open cup facing the incoming ligand, plus a membrane stem.
    cup = Arc(radius=.28*s, start_angle=-PI/2, angle=PI,
              color=YELLOW, stroke_width=7)
    stem = Line([.28*s, 0, 0], [.55*s, 0, 0], color=YELLOW, stroke_width=7)
    return VGroup(cup, stem).move_to([x, y, 0])


def push(a, b, color=RED, w=6):
    return Arrow([*a, 0], [*b, 0], buff=0, color=color,
                 stroke_width=w, tip_length=.2)


def blocked(x, y):
    return VGroup(Line([x-.18, y-.18, 0], [x+.18, y+.18, 0], color=RED, stroke_width=6),
                  Line([x-.18, y+.18, 0], [x+.18, y-.18, 0], color=RED, stroke_width=6))


def path(points, opacity=1, color=BLUE):
    return VMobject(stroke_color=color, stroke_width=7, stroke_opacity=opacity,
                    fill_opacity=0).set_points_as_corners([[x, y, 0] for x, y in points])


APPROACH = [(-3.7, 2), (-3.2, .6), (-2.6, -1.8), (-.8, -1.8)]
CROSS = [(-.8, -1.8), (1.8, -1.8)]
LEAVE = [(1.8, -1.8), (3, -.8), (3.5, 1.8)]
FULL = APPROACH + CROSS[1:] + LEAVE[1:]
IPSI = [(4.3, 1.7), (3.9, .5), (3.2, -1), (1.15, -1.45), (1.15, -.4), (1.8, .35)]


def cord(floor_label=True):
    outline = Ellipse(width=11.8, height=6.0, stroke_color=GREY,
                      stroke_width=3, fill_color=GREY, fill_opacity=.05)
    mid = strip(0, -2.65, -1.05, 1.2)
    axis = DashedLine([0, -1.0, 0], [0, 2.95, 0], color=GREY, stroke_opacity=.6)
    g = VGroup(outline, mid, axis)
    if floor_label:
        g.add(label('floor plate', 0, -3.35, 27),
              Line([0, -3.08, 0], [0, -2.68, 0], color=GREY))
    return g


def grow(scene, pts, duration=1, color=BLUE, tip=None):
    p = path(pts, color=color)
    if tip is None:
        tip = make_cone(*pts[0], s=.85, color=color)
    scene.add(tip)
    motion = p.copy()
    # Create uses Bezier-segment progress, whereas MoveAlongPath uses arc
    # length. Match Create exactly so the cone never detaches at a bend.
    scene.play(Create(p), UpdateFromAlphaFunc(tip,
        lambda mob, alpha: mob.move_to(motion.get_subcurve(0,alpha).get_end())),
        run_time=duration, rate_func=linear)
    return VGroup(p, tip)


def completed():
    return VGroup(path(FULL), make_cone(3.5, 1.8, .85))


def meter(x, y, value, width=2.3, state=None):
    box = Rectangle(width=width, height=.38, stroke_color=GREY, stroke_width=2).move_to([x,y,0])
    fill = Rectangle(width=max(.02,width*value), height=.29, stroke_width=0,
                     fill_color=RED, fill_opacity=.9)
    fill.move_to([x-width/2+width*value/2,y,0])
    mark = Line([x,y-.28,0],[x,y+.28,0],color=TEXT,stroke_width=3)
    g = VGroup(box, fill, mark, label('push',x-width*.32,y+.48,26,RED))
    if state:
        g.add(label(state,x+width*.33,y+.48,26,RED))
    g.add_to_back(BackgroundRectangle(g,color=BG,fill_opacity=1,buff=.10,stroke_width=0))
    return g


def ride(scene, pts, value, state, duration, tip=None, gauge=None):
    if tip is None:
        tip = make_cone(*pts[0], s=.95)
    if gauge is None:
        gauge = meter(pts[0][0], pts[0][1]+.95, value, state=state)
    offset = gauge.get_center()-tip.get_center()
    gauge.add_updater(lambda m: m.move_to(tip.get_center()+offset))
    scene.add(gauge)
    result = grow(scene, pts, duration, tip=tip)
    gauge.clear_updaters()
    return result, gauge


class S00Title(TitleCard):
    TITLE = 'One Crossing, and Only One'
    LESSON = 'Crossing the Midline Once: Slit, Robo and Comm'
    def construct(self):
        lines = VGroup(T('Crossing the Midline Once:',26,color=TEXT),
                       T('Slit, Robo and Comm',26,color=TEXT)).arrange(DOWN,buff=.15)
        title = T(self.TITLE,44,font=TITLE_FONT)
        g = VGroup(lines,title,Line(LEFT*1.4,RIGHT*1.4,color=GOLD)).arrange(DOWN,buff=.5)
        self.add(g)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(cord())
        self.at('an axon grows'); a=grow(self,APPROACH,2)
        self.at('it crosses'); self.remove(a[1]); b=grow(self,CROSS,.8)
        self.at('then it treats'); self.remove(b[1]); c=grow(self,LEAVE,1.2)
        self.at('as forbidden ground')
        self.play(GrowArrow(push((2.7,.3),(.9,.3))),Create(blocked(1.5,.3)),run_time=.5)
        self.at('what changed'); self.play(FadeIn(label('What changed?',0,3.4,34)),run_time=.3)
        self.finish()


class S02Sides(SpokenScene):
    def construct(self):
        # Front view: the figure's LEFT hand is on the viewer's right.
        brain=VGroup(*[Ellipse(width=1.15,height=1.4,color=GREY,fill_color=GREY,fill_opacity=.12)
                      .move_to([x,2.05,0]) for x in (-.65,.65)])
        head=Ellipse(width=3.1,height=2.1,color=GREY).move_to([0,2.05,0])
        body=VGroup(Line([0,1,0],[0,-1.25,0]),
                    Line([0,.6,0],[2.6,-.35,0]),Line([0,.6,0],[-2.6,-.35,0]),
                    Line([0,-1.25,0],[-1.2,-3.0,0]),Line([0,-1.25,0],[1.2,-3.,0])).set_color(GREY).set_stroke(width=8)
        self.add(head,body,brain,label('left hand',4.1,-.35,29),label('right brain',-3.6,2.15,29))
        self.at('much touch')
        star=VGroup(*[Line([2.6+.23*np.cos(a),-.35+.23*np.sin(a),0],
                          [2.6+.5*np.cos(a),-.35+.5*np.sin(a),0],color=BLUE,stroke_width=4)
                      for a in np.linspace(0,TAU,8,endpoint=False)])
        self.play(Create(star),run_time=.35)
        self.at('information from one side')
        p=path([(2.6,-.35),(.65,.4),(.65,.85),(-.65,1.25),(-.65,2.05)])
        self.play(Create(p),run_time=1.15)
        crossing=Circle(.18,color=GOLD).move_to([0,1.05,0])
        self.play(Create(crossing),FadeIn(label('crossing',-3.3,.75,28,GOLD)),
                  Create(Line([-2.25,.75,0],[-.2,1.05,0],color=GOLD)),run_time=.35)
        self.at('opposite half'); self.play(brain[0].animate.set_color(BLUE).set_fill(BLUE,.5),run_time=.4)
        self.finish()


class S03Walking(SpokenScene):
    def construct(self):
        # A tapered trunk flows into rounded hips, with articulated legs.
        torso=VMobject(stroke_color=GREY,stroke_width=5,fill_color=GREY,fill_opacity=.06)
        torso.set_points_smoothly([[-2.8,2.8,0],[-2.5,1.3,0],[-2.15,.2,0],
            [-2.7,-.65,0],[-1.6,-1.0,0],[0,-.5,0],[1.6,-1.0,0],
            [2.7,-.65,0],[2.15,.2,0],[2.5,1.3,0],[2.8,2.8,0]])
        halves=VGroup(strip(-1.15,.05,2.6,1.45),strip(1.15,.05,2.6,1.45))
        def legs(left):
            lk,lf=((-2.4,-2.0),(-2.8,-3.3)) if left else ((-1.1,-1.8),(-.5,-2.6))
            rk,rf=((1.1,-1.8),(.5,-2.6)) if left else ((2.4,-2.0),(2.8,-3.3))
            return VGroup(path([(-1.8,-.75),lk,lf],color=GREY),
                          path([(1.8,-.75),rk,rf],color=GREY),
                          Line([lf[0]-.25,lf[1],0],[lf[0]+.3,lf[1],0],color=GREY,stroke_width=8),
                          Line([rf[0]-.3,rf[1],0],[rf[0]+.25,rf[1],0],color=GREY,stroke_width=8))
        l=legs(True)
        self.add(torso,halves,l,label('left cord',-4.3,2.7,29),label('right cord',4.3,2.7,29),
                 Line([-3.2,2.5,0],[-1.95,2.0,0],color=GREY),Line([3.2,2.5,0],[1.95,2.0,0],color=GREY))
        self.at('coordinate walking')
        self.play(Transform(l,legs(False)),run_time=.45)
        self.play(Transform(l,legs(True)),run_time=.45)
        self.play(Transform(l,legs(False)),run_time=.45)
        self.at('both jobs need')
        p=path([(-1.55,2.35),(-1.25,1.35),(1.25,1.35),(1.55,.35)])
        q=path([(1.55,2.35),(1.25,.75),(-1.25,.75),(-1.55,.1)])
        self.play(Create(p),Create(q),run_time=.6)
        self.at('commissural axons')
        self.play(FadeIn(label('commissural axons',4.35,.2,28,BLUE)),
                  Create(Line([2.75,.35,0],[1.65,.75,0],color=BLUE)),run_time=.35)
        self.finish()


class S04Ipsi(SpokenScene):
    def construct(self):
        ghost=completed(); ghost[0].set_stroke(opacity=.22); ghost[1].set_opacity(.22)
        self.add(cord(),ghost)
        self.at('their neighbors')
        # A monotonic ventral approach, distinct from the far-side trail.
        ipsi=VMobject(stroke_color=BLUE,stroke_width=7,fill_opacity=0)
        ipsi.set_points_smoothly([[2.4,2.1,0],[2.0,.8,0],[1.65,-.45,0],[.95,-1.15,0]])
        tip=make_cone(2.4,2.1,.85).rotate(PI)
        self.add(tip); motion=ipsi.copy()
        self.play(Create(ipsi),UpdateFromAlphaFunc(tip,
            lambda m,a:m.move_to(motion.get_subcurve(0,a).get_end())),run_time=2.3,rate_func=linear)
        self.at('stay on the side')
        self.play(FadeIn(label('ipsilateral axon',3.2,3.4,29,BLUE)),run_time=.35)
        self.at('must never cross')
        self.play(Create(blocked(.65,-1.15)),FadeIn(label('stays on its side',3.1,-.9,28,BLUE)),run_time=.45)
        self.finish()


class S05Jobs(SpokenScene):
    def construct(self):
        tip=make_cone(*APPROACH[0],s=.85)
        self.add(cord(False),tip,label('Three jobs',0,3.4,32))
        self.at('grow toward'); a=grow(self,APPROACH,1.2,tip=tip)
        self.play(FadeIn(label('1  approach',-4.45,-.55,28,BLUE)),run_time=.25)
        self.at('enter it'); self.remove(a[1]); b=grow(self,CROSS+LEAVE[1:],1.15)
        self.play(FadeIn(label('2  cross and leave',.8,-3.35,28,BLUE)),run_time=.25)
        self.at('and never')
        self.play(FadeIn(label('3  never return',1.65,1.4,28,BLUE)),
                  GrowArrow(push((2.7,.3),(.85,.3))),Create(blocked(1.5,.3)),run_time=.5)
        self.finish()


class S06Fail1(SpokenScene):
    def construct(self):
        self.add(cord(),label('stall',1.7,-.85,32,BLUE))
        self.at('each job fails'); a=grow(self,APPROACH+[(.45,-1.8)],1.5)
        self.at('if the pull')
        self.play(GrowArrow(push((.45,-1.57),(-1.6,-1.57),BLUE)),
                  FadeIn(label('pull toward\nthe midline',-4.45,-.45,27,BLUE)),run_time=.4)
        self.at('beats the push')
        self.play(GrowArrow(push((.45,-2.03),(1.35,-2.03))),
                  FadeIn(label('push away',2.9,-2.2,27,RED)),run_time=.4)
        self.at('the axon stalls')
        self.play(Create(blocked(.9,-1.8)),run_time=.4)
        self.finish()


class S07Fail2(SpokenScene):
    def construct(self):
        self.add(cord())
        # Ghost 2 occupies the upper left; ghost 3 uses the ventral plate.
        early=[(-4.4,1.9),(-3.8,.8),(-2.5,-.55),(-1.15,-.55),(-1.65,.45)]
        self.at('get repelled'); a=grow(self,early,1.25,color=BLUE)
        self.play(Create(blocked(-.7,-.55)),run_time=.2)
        self.at('never crosses')
        self.play(FadeIn(label('never crosses',-3.25,2.7,29,BLUE)),run_time=.25)
        self.at('lose the repulsion')
        self.play(a[0].animate.set_stroke(opacity=.65),a[1].animate.set_opacity(.65),run_time=.15)
        pts=[(-3.7,-1.25),(-2.5,-2.25),(-.9,-2.25),(.95,-2.25),(2.6,-1.9)]
        b=grow(self,pts,1.25,color=TEAL)
        self.at('and it'); self.remove(b[1])
        loop=VMobject(stroke_color=TEAL,stroke_width=7,fill_opacity=0)
        loop.set_points_smoothly([[2.6,-1.9,0],[2.8,-1.25,0],[1.65,-1.35,0],
                                 [.6,-1.65,0],[-.85,-1.65,0]])
        tip=make_cone(2.6,-1.9,.85,TEAL).rotate(PI); self.add(tip)
        motion=loop.copy()
        self.add(label('recross',2.7,-.35,30,TEAL))
        self.play(Create(loop),UpdateFromAlphaFunc(tip,
            lambda mob,alpha: mob.move_to(motion.get_subcurve(0,alpha).get_end())),
            GrowArrow(push((1.1,-.85),(-.85,-.85),TEAL)),
            run_time=.55,rate_func=linear)
        self.finish()


class S08Midline(SpokenScene):
    def construct(self):
        fly=VGroup(Line([-5.7,-2.55,0],[-5.7,2.4,0],color=GREY),
                   Line([-.9,-2.55,0],[-.9,2.4,0],color=GREY))
        cells=VGroup(*[Circle(.34,color=GOLD,fill_color=GOLD,fill_opacity=.3).move_to([-3.3,y,0])
                       for y in (-2.1,-1.25,-.4,.45,1.3,2.15)])
        rails=VGroup(path([(-5.2,2.1),(-4.6,.8),(-2,.8),(-1.4,-1.8)]),
                     path([(-1.4,2.1),(-2,-.5),(-4.5,-.5),(-5.2,-2.1)]))
        verte=VGroup(Ellipse(width=5.6,height=4.3,color=GREY).move_to([3.2,0,0]),
                     strip(3.2,-1.9,-.6,.7,GOLD),
                     DashedLine([3.2,-.55,0],[3.2,2.1,0],color=GREY))
        self.add(fly,cells,rails,verte,label('fly nerve cord',-3.3,3.15,30),
                 label('vertebrate spinal cord',3.2,3.15,29))
        self.at('in the fly'); self.play(Indicate(cells,color=GOLD,scale_factor=1.05),run_time=.5)
        self.at('glial cells'); self.play(FadeIn(label('midline glia',-3.3,-3.15,29,GOLD)),run_time=.3)
        self.at('in the spinal cord'); self.play(Indicate(verte[1],color=GOLD,scale_factor=1.08),run_time=.45)
        self.at('the floor plate'); self.play(FadeIn(label('floor plate',3.2,-3.15,29,GOLD)),
                         Create(Line([3.2,-2.85,0],[3.2,-1.92,0],color=GOLD)),run_time=.3)
        self.finish()


class S09Same(SpokenScene):
    def construct(self):
        xs=(-4.4,0,4.4)
        for x,txt in zip(xs,('before','during','after')):
            self.add(strip(x,-2.4,2.35,1.1),label(txt,x,3.15,30))
            for dx,y,col in ((-.25,-1.95,RED),(.25,-.8,GREY),(-.25,.25,RED),(.25,1.35,GREY)):
                self.add(Dot([x+dx,y,0],radius=.17,color=col))
        def pts(x,stage):
            a=[(x-1.55,1.9),(x-1.35,.5),(x-1.05,-1.55),(x-.65,-1.55)]
            if stage>0: a += [(x+.8,-1.55)]
            if stage>1: a += [(x+1.3,-.7),(x+1.55,1.45)]
            return a
        self.at('before'); grow(self,pts(xs[0],0),.55)
        self.at('during'); grow(self,pts(xs[1],1),.13)
        self.at('and after'); grow(self,pts(xs[2],2),.7)
        self.at('midline did not change')
        self.play(FadeIn(label('same cells, same molecules',0,-3.15,34)),run_time=.35)
        self.finish()


class S10Axon(SpokenScene):
    def construct(self):
        stage=cord(); ax=completed(); self.add(stage,ax)
        self.at('so the change')
        cone=make_cone(0,.4,4.3)
        self.play(FadeOut(stage),FadeOut(ax),FadeIn(cone),
                  FadeIn(label('the change is here',0,-2.65,36,BLUE)),run_time=.5)
        self.at('in the axon'); self.play(Indicate(cone,color=BLUE,scale_factor=1.06),run_time=.3)
        self.finish()


class S11Puzzles(SpokenScene):
    def construct(self):
        self.add(label('Three puzzles',0,3.15,38,BLUE))
        # The opening holds the axon, not unexplained question placeholders.
        anchor=VGroup(path([(-4.8,2),(-2.5,2),(0,2),(3.8,2)]),make_cone(3.8,2,.85))
        self.add(anchor)
        for cue,txt,y in zip(('why does an','why does it','and why'),
                ('1  Why leave the midline?','2  Why never come back?',
                 '3  Why do ipsilateral neighbours\nnever cross?'),(.75,-.8,-2.45)):
            self.at(cue)
            q=T(txt,size=34,color=BLUE,line_spacing=.8).move_to([0,y,0])
            self.play(AddTextLetterByLetter(q),run_time=.8)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        first=label('The midline stays the same.',0,1.3,40)
        second=label('The axon changes what it can hear.',0,-.7,36,BLUE)
        self.add(label('One idea to carry through',0,3.15,30,GOLD),first,second,
                 Line([-5,-2.4,0],[5,-2.4,0],color=BLUE,stroke_width=6),make_cone(5,-2.4,.9))
        self.at('while an axon'); self.play(Indicate(second,color=BLUE,scale_factor=1.03),run_time=.6)
        self.at('midline stays'); self.play(Indicate(first,color=TEXT,scale_factor=1.03),run_time=.5)
        self.at('the axon changes'); self.play(Indicate(second,color=BLUE,scale_factor=1.03),run_time=.5)
        self.finish()


class S13Slit(SpokenScene):
    def construct(self):
        mid=strip(-4.4,-2.5,2.5,1.1)
        self.add(mid,label('floor plate',-4.4,-3.15,28))
        # All ligand dots are born at the source, then spread away from it.
        dots=VGroup(*[slit_dot(-4.4,y,.15) for y in (-1.8,-1.1,-.4,.4,1.1,1.8)])
        self.at('called slit',lead=0)
        self.play(FadeIn(dots),run_time=.2)
        self.play(FadeIn(label('Slit',-2.6,2.9,34,RED)),
                  *[d.animate.shift(RIGHT*dx).set_opacity(op) for d,dx,op in
                    zip(dots,(.9,1.6,2.4,3.1,1.5,.8),(.9,.8,.65,.45,.8,.9))],run_time=.9)
        self.at('the growth cone')
        cone=make_cone(3.2,0,4.1).stretch_to_fit_height(4.6)
        self.play(FadeIn(cone),FadeIn(label('growth cone',3.2,2.9,30,BLUE)),run_time=.4)
        self.at('carries')
        ears=VGroup(ear(1.8,.7,1.65),ear(1.8,-.7,1.65))
        self.play(Create(ears),FadeIn(label('Robo receptors',3.0,-2.65,31,YELLOW)),
                  Create(Line([2.2,-2.25,0],[1.9,-1.15,0],color=YELLOW)),run_time=.45)
        self.at('that hear it')
        # The cup opens left; park the ligand visibly within the cup.
        docking=ears[0][0].get_center()+LEFT*.08
        self.play(dots[3].animate.move_to(docking).set_opacity(1),run_time=.45)
        self.play(Indicate(ears[0],color=YELLOW,scale_factor=1.08),run_time=.2)
        self.finish()


class S14Product(SpokenScene):
    def construct(self):
        self.add(label('toy model',0,3.15,28),
                 label('Repulsion at the growth cone',0,-3.05,30,BLUE))
        terms=VGroup(T('push',size=52,color=RED),T('≈',size=52),T('Slit',size=52,color=RED),
                     T('×',size=52),T('Robo activity',size=52,color=YELLOW)).arrange(RIGHT,buff=.32)
        terms.move_to([0,.65,0])
        self.at('in a simple'); self.play(FadeIn(terms),run_time=.45)
        self.at("the axon's push")
        m=meter(terms[0].get_x(),-.7,.2,1.8)
        self.play(FadeIn(m),run_time=.35)
        self.at('is slit times')
        ds=VGroup(*[slit_dot(terms[2].get_x()+dx,-.75+dy,.17) for dx,dy in ((-.3,0),(.2,.3),(.3,-.3))])
        self.play(FadeIn(ds),run_time=.4)
        self.at('the repelling')
        e=ear(terms[4].get_x(),-.8,2)
        self.play(Create(e),Transform(m,meter(terms[0].get_x(),-.7,.85,1.8)),run_time=.6)
        self.finish()


class S15Threshold(SpokenScene):
    def construct(self):
        # Normal-CDF toy response. Parameters are illustrative, not a fitted
        # literal-push interpretation of the separate dosage-margin model.
        theta,sigma=.5,.075
        response=lambda x:.5*(1+math.erf((x-theta)/(sigma*math.sqrt(2))))
        axes=Axes(x_range=[0,1,.25],y_range=[0,1,.5],x_length=9.8,y_length=5.4,
                  axis_config={'include_tip':False,'color':GREY}).move_to([.65,.1,0])
        curve=axes.plot(response,x_range=[0,1,.004],color=RED)
        ylabel=T('chance of being turned away',size=27).rotate(PI/2).move_to([-5.95,.15,0])
        self.add(axes,ylabel,label('0',-4.7,-2.6,27),label('1',-4.7,2.8,27),
                 label('push',.6,-3.4,30,RED),label('low',-4.2,-3.15,27),
                 label('high',5.55,-3.15,27),label('toy model',4.4,3.35,27))
        self.at('the axon'); self.play(Create(curve),run_time=.6)
        dot=Dot(axes.c2p(.2,response(.2)),radius=.11,color=TEAL)
        low=label('little turning',-2.3,1.8,29,TEAL)
        self.add(dot,low)
        self.at('when that push')
        line=DashedLine(axes.c2p(theta,0),axes.c2p(theta,response(theta)+.025),color=TEXT,
                        stroke_width=4,dash_length=.12,dashed_ratio=.7)
        intersection=Dot(axes.c2p(theta,response(theta)),radius=.07,color=TEXT)
        self.add(line,intersection,label('threshold',2.1,-2.05,29,TEXT))
        self.at('passes a threshold')
        self.play(MoveAlongPath(dot,axes.plot(response,x_range=[.2,.85,.004])),FadeOut(low),run_time=.8,rate_func=linear)
        self.play(FadeIn(label('turned away',3.4,1.4,29,TEAL)),run_time=.2)
        self.finish()


class S16Timing(SpokenScene):
    def construct(self):
        mid=strip(0,-2.9,2.5,.65).set_fill(BG,1).set_z_index(3)
        self.add(mid,label('midline',0,3.2,28),
                 label('ipsilateral',-4.6,3.45,30,BLUE),label('commissural',-4.5,-3.2,30,BLUE))
        # Establish the near-side low stage before the contrasting high case.
        tip=make_cone(-4.7,-1.9,.95)
        low=meter(-4.7,-.95,.15,state='low').set_z_index(5)
        self.add(path([(-5.5,-1.9),(-4.7,-1.9)]),tip,low)
        self.at('ipsilateral axons')
        ips,hi=ride(self,[(-4.7,1.5),(-2.6,1.5),(-1.65,1.1)],.85,'high',1.7)
        self.at('high from the start')
        self.play(Create(blocked(-1.05,1.1)),FadeIn(label('stays on its side',3.25,1.5,28,BLUE)),run_time=.45)
        self.at('commissural axons')
        com,low=ride(self,[(-4.7,-1.9),(-1.1,-1.9)],.15,'low',.85,tip,low)
        self.at('hold it low')
        self.play(Indicate(low,scale_factor=1.04),run_time=.35)
        self.at('until they have crossed')
        self.remove(com[1]); com2,low=ride(self,[(-1.1,-1.9),(3.9,-1.9)],.15,'low',1.1,tip,low)
        self.at('then they')
        self.play(Transform(low,meter(3.9,-.95,.85,state='high').set_z_index(5)),run_time=.75)
        self.finish()


class S17How(SpokenScene):
    def construct(self):
        self.add(label('commissural axon',0,3.3,31,BLUE),
                 strip(1.1,1.5,2.9,.6),label('crossing',3.2,2.7,28,TEAL),
                 Line([2.1,2.55,0],[1.1,2.2,0],color=TEAL),
                 path([(-5,2.2),(-1.4,2.2)]),make_cone(-1.4,2.2,.95),
                 DashedLine([-.9,2.2,0],[4.9,2.2,0],color=BLUE))
        low=meter(-1.4,.65,.15,state='low'); self.add(low)
        # Plain links describe the shared functional result, not trafficking.
        self.at('flies do this'); self.play(FadeIn(label('flies',-4.4,-.65,34)),run_time=.3)
        self.at('a protein called')
        self.play(FadeIn(chip('Comm',PURPLE,size=38).move_to([-4.4,-1.7,0])),run_time=.35)
        link=VMobject(stroke_color=PURPLE,stroke_width=3,fill_opacity=0).set_points_as_corners(
            [[-3.5,-1.7,0],[-2.7,-1.7,0],[-2.7,.65,0],[-2.6,.65,0]])
        self.play(Create(link),FadeIn(label('keeps push low',-3.9,-2.9,28,PURPLE)),run_time=.4)
        self.at('mammals do it'); self.play(FadeIn(label('mammals',3.8,-.65,34)),run_time=.3)
        self.at('a relative')
        self.play(FadeIn(chip('Robo3',ORANGE,size=38).move_to([3.8,-1.7,0])),run_time=.4)
        link2=VMobject(stroke_color=ORANGE,stroke_width=3,fill_opacity=0).set_points_as_corners(
            [[2.8,-1.7,0],[.2,-1.7,0],[.2,.65,0],[-.2,.65,0]])
        self.play(Create(link2),FadeIn(label('keeps push low',3.8,-2.9,28,ORANGE)),run_time=.45)
        self.finish()


class S18Questions(SpokenScene):
    def construct(self):
        self.add(label('Read a Slit–Robo mutant',0,3.15,36,BLUE))
        # Concrete source/receiver/timing symbols carry the introductory clause.
        icons=VGroup(slit_dot(-4.5,2.05,.22),ear(0,2.05,1.3),
                     Circle(.3,color=TEAL).move_to([4.5,2.05,0]),
                     Line([4.5,2.05,0],[4.5,2.28,0],color=TEAL),
                     Line([4.5,2.05,0],[4.7,1.94,0],color=TEAL))
        self.add(icons)
        for cue,txt,col,y in zip(('is slit there','can the axon','when does it'),
                ('Is Slit there?','Can the axon hear it?','When does it start hearing it?'),
                (RED,YELLOW,TEAL),(.9,-.8,-2.5)):
            self.at(cue)
            q=chip(txt,col,size=35).move_to([0,y,0])
            self.play(FadeIn(q),run_time=.35)
        self.finish()


class S19Take(SpokenScene):
    def construct(self):
        # Keep the section large; put captions inside its clear dorsal area.
        stage=VGroup(cord(),completed()).scale(.95).shift(DOWN*.4)
        self.add(stage,label('The midline stays the same.',0,3.45,31))
        self.at('the midline stays')
        self.play(Indicate(stage[0][1],color=GOLD,scale_factor=1.05),run_time=.4)
        self.at('and the axon')
        self.play(FadeIn(label('The axon changes what it can hear, and when.',0,2.85,28,BLUE)),
                  FadeIn(meter(1.6,.25,.85,1.9,'high')),run_time=.45)
        self.at('repulsion side')
        self.play(FadeIn(label('repulsion only',-3.8,-3.25,30)),run_time=.35)
        self.finish()


class S20End(EndCard):
    LINE = 'The axon changes what it can hear, and when.'
