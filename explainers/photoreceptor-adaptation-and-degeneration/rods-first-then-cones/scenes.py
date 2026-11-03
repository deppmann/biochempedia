"""Chapter 3: Rods First, Then Cones.
COLOR MAP (from scenes.old.py, shared across the series):
YELLOW light; ORANGE #F29E4C calcium; PURPLE #B58CD9 calcium sensors;
TEAL membrane proteins; GREEN cGMP / support / therapy;
PINK #E58FB0 active pigment; BLUE rods / intact / control; PINK cones; GOLD uncertain benefit;
RED removed / lacking / off; GREY membranes / outlines / unknowns.
No response curves are needed in this chapter. The result interval uses
only the supplied trial data: difference 1.6, 95% CI [0.72, 2.41].
"""
from bp_style import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB0"
LESSON_NAME = "Calcium Feedback Sets Photoreceptor Gain,\nand When Photoreceptors Die"


def label(text, x=0, y=3.05, size=30, color=TEXT):
    mob = (Paragraph(*text.split('\n'), alignment='center', font=FONT, font_size=size, color=color)
           if '\n' in text else T(text, size=size, color=color))
    return mob.move_to([x, y, 0])


# The rod and cone silhouettes reproduce the reference film's helpers.
def rod_cell(color=BLUE, s=1.0):
    outer = RoundedRectangle(corner_radius=0.15, width=0.7, height=1.7,
        stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18).move_to([0, 0.85, 0])
    body = RoundedRectangle(corner_radius=0.4, width=1.1, height=1.1,
        stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18).move_to([0, -0.55, 0])
    return VGroup(outer, body, Line([0, -1.1, 0], [0, -1.6, 0], color=color, stroke_width=4)).scale(s)


def cone_cell(color=BLUE, s=1.0):
    outer = Polygon([-0.55, 0, 0], [0.55, 0, 0], [0.14, 1.7, 0], [-0.14, 1.7, 0],
        stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18)
    body = RoundedRectangle(corner_radius=0.4, width=1.4, height=1.1,
        stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18).move_to([0, -0.55, 0])
    return VGroup(outer, body, Line([0, -1.1, 0], [0, -1.6, 0], color=color, stroke_width=4)).scale(s)


# Cues use the existing word alignment without changing the shared sync.log.
class TimedScene(SpokenScene):
    def at(self, phrase, lead=0.2, nth=0):
        rest = self.t_of(phrase, nth) - lead - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

    def hold(self, seconds):
        self.wait(max(0.05, seconds))


def retina():
    xs = (-5.1, -3.06, -1.02, 1.02, 3.06, 5.1)
    rods = VGroup(*[rod_cell(BLUE, 1.52).move_to([x, 0, 0]) for x in xs[::2]])
    cones = VGroup(*[cone_cell(PINK, 1.40).move_to([x, 0, 0]) for x in xs[1::2]])
    names = VGroup(*[label('rod' if i%2 == 0 else 'cone', x, -2.72, 28,
                         BLUE if i%2 == 0 else PINK) for i,x in enumerate(xs)])
    return rods, cones, names


def predict_frame():
    r,c,n = retina()
    r.set_opacity(0.20)
    q = label('Should the cones be spared?', y=3.22, size=36)
    # Question marks sit directly beside the upper segment of each cone.
    marks = VGroup(*[label('?', x+0.55, 1.45, 36, PINK) for x in (-3.06,1.02,5.1)])
    return r,c,n,q,marks


def candidates():
    return VGroup(*[VGroup(
        RoundedRectangle(width=3.85,height=5.0,corner_radius=0.2,color=GREY),
        label(t,0,0.1,34),
    ).move_to([x,-0.15,0]) for t,x in
        (('lost rod\nsupport',-4.15),('cone\nstarvation',0),('oxidative\ndamage',4.15))])


def stamp():
    return VGroup(Rectangle(width=11.5,height=0.65,color=GOLD,fill_color=BG,fill_opacity=1),
                  T('NOT SETTLED',size=30,color=GOLD)).move_to([0,-1.55,0])


def eye(x=0,y=0,color=BLUE,scale=1):
    return VGroup(Ellipse(width=3.4,height=2.7,color=color,stroke_width=5),
        Circle(radius=0.64,color=color,fill_color=color,fill_opacity=0.15),
        Dot(radius=0.24,color=color)).scale(scale).move_to([x,y,0])


def eye_pair():
    left=eye(-3.25,0.25,GREEN,1.55); right=eye(3.25,0.25,GREY,1.55)
    # Extra scleral space holds the tool without crossing iris or outer wall.
    left[0].stretch(1.2,1); right[0].stretch(1.2,1)
    return VGroup(left,right,
        label('worse eye • treated',-3.25,-2.6,28,GREEN),
        label('untreated fellow eye',3.25,-2.6,28,GREY))


def trial_head(text):
    return label(text,y=3.25,size=34,color=GREEN)


class S00Title(TitleCard):
    LESSON = LESSON_NAME
    TITLE = 'Rods First, Then Cones'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',y=2.2,size=26,color=TEAL),
                 label(self.LESSON,y=1,size=26,color=GREY))
        title=label(self.TITLE,y=-0.5,size=48)
        self.play(FadeIn(title),Create(Line([-1.4,-1.35,0],[1.4,-1.35,0],color=GOLD)),run_time=0.5)
        self.finish()


class S01Q(TimedScene):
    def construct(self):
        r,c,n=retina()
        self.at('A new question')
        self.play(FadeIn(r),FadeIn(c),FadeIn(n),run_time=0.45)
        self.at('What happens when')
        self.play(FadeIn(label('When photoreceptors die?',y=3.22,size=36)),run_time=0.35)
        self.finish()


class S02Rp(TimedScene):
    def construct(self):
        r,c,n=retina(); self.add(r,c,n)
        self.at('In typical retinitis pigmentosa')
        self.play(FadeIn(label('Typical retinitis pigmentosa',y=3.3,size=34)),run_time=0.3)
        # Badges fit fully inside each soma, with no membrane through text.
        xs=(-5.1,-3.06,-1.02,1.02,3.06,5.1)
        badges=VGroup(*[VGroup(T('DNA',size=26,color=RED),T('variant',size=26,color=RED))
            .arrange(DOWN,buff=0.08).move_to([x,-0.9,0]) for x in xs])
        for badge in badges:
            badge.add_to_back(RoundedRectangle(width=1.35,height=.94,corner_radius=.08,
                stroke_color=RED,stroke_width=2,fill_color=BG,fill_opacity=.95).move_to(badge))
        self.at('the faulty gene')
        self.play(FadeIn(badges),run_time=0.3)
        self.at('is often not expressed')
        tags=VGroup(*[label('ON' if i%2==0 else 'not\nexpressed',x,-3.25,26,
            GREEN if i%2==0 else GREY) for i,x in enumerate(xs)])
        self.play(FadeIn(tags),FadeIn(label('in many forms: gene not expressed in cones',y=2.72,size=26,color=GREY)),run_time=0.3)
        self.finish()


class S03Predict(TimedScene):
    def construct(self):
        r,c,n,q,m=predict_frame(); self.add(r,c,n)
        self.at('Predict')
        self.play(FadeIn(m),run_time=0.25)
        note=label('gene not expressed in cones',y=3.22,size=34,color=GREY)
        self.at('If the faulty gene')
        self.play(FadeIn(note),run_time=0.25)
        self.at('should the cones')
        self.play(ReplacementTransform(note,q),run_time=0.25)
        self.finish()


class S04Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*predict_frame()); self.wait(5)


class S05Die(TimedScene):
    def construct(self):
        r,c,n,q,m=predict_frame(); self.add(r,c,n,q,m)
        self.at('they die too')
        self.play(FadeOut(q),FadeOut(m),
                  FadeIn(label('Xue and Cepko, 2024',y=-3.38,size=26,color=GREY)),run_time=0.25)
        # Labels attach to each alternating cell, never to the opposite type.
        first=VGroup(*[label('rods first',x,2.9,26,RED) for x in (-5.1,-1.02,3.06)])
        later=VGroup(*[label('then cones',x,2.9,26,RED) for x in (-3.06,1.02,5.1)])
        self.at('typically after most')
        self.play(r.animate.set_opacity(0.06),FadeIn(first),run_time=0.3)
        self.at('have gone')
        self.play(c.animate.set_opacity(0.06),FadeIn(later),run_time=0.3)
        self.finish()


def field_picture(x,y,r=1.12):
    field=Circle(radius=r,color=BLUE,fill_color=BLUE,fill_opacity=0.12)
    house=VGroup(Rectangle(width=1.15,height=0.8,color=TEXT).shift(DOWN*0.2),
        Polygon([-0.72,0.2,0],[0,0.8,0],[0.72,0.2,0],color=TEXT),
        Rectangle(width=0.25,height=0.45,color=TEXT).shift(DOWN*0.35))
    return VGroup(field,house).move_to([x,y,0])


class S06Symptoms(TimedScene):
    def construct(self):
        # Three persistent before/after columns allow all stages to be read,
        # even though the final narration leaves little time after 'cones fail'.
        xs=(-4.25,0,4.25)
        columns=VGroup(*[VGroup(field_picture(x,1.15,r=.98),field_picture(x,-1.65,r=.98)) for x in xs])
        headers=VGroup(*[label(t,x,2.75,30) for t,x in zip(('Night vision','Peripheral vision','Central vision'),xs)])
        self.add(columns,headers,label('before',-6.1,1,26,GREY),label('after',-6.1,-1.65,26,GREY))
        self.at('Patients typically lose')
        self.play(FadeIn(label('Verbakel and colleagues, 2018',y=-3.4,size=26,color=GREY)),run_time=0.2)
        self.at('night vision first')
        self.play(columns[0][1][1].animate.set_opacity(0.18),
                  FadeIn(label('dims',xs[0],-0.25,28,YELLOW)),run_time=0.25)
        self.at('then peripheral vision')
        mask=Annulus(inner_radius=0.43,outer_radius=.96,fill_color=BG,fill_opacity=1,stroke_width=0).move_to(columns[1][1])
        self.play(FadeIn(mask),FadeIn(label('narrows',0,-0.25,28,YELLOW)),run_time=0.25)
        self.at('Central vision goes later')
        # The before/after comparison displays the narrated future end state.
        before_mask=Annulus(inner_radius=.43,outer_radius=.96,fill_color=BG,fill_opacity=1,stroke_width=0).move_to(columns[2][0])
        centre=Circle(radius=.96,fill_color=BG,fill_opacity=1,stroke_width=0).move_to(columns[2][1])
        self.play(FadeIn(before_mask),FadeIn(centre),
                  FadeIn(label('peripheral already lost',xs[2],2.35,22,GREY)),
                  FadeIn(label('centre lost',xs[2],-0.25,28,YELLOW)),run_time=0.25)
        self.finish()


class S07Depend(TimedScene):
    def construct(self):
        r=rod_cell(BLUE,1.65).move_to([-4.6,0,0]); c=cone_cell(PINK,1.55).move_to([-0.6,0,0])
        a=Arrow([-3.5,0.6,0],[-1.85,0.6,0],color=GREY,stroke_width=7,buff=0.05)
        self.add(r,c,label('rod',-4.6,-3,30,BLUE),label('cone',-0.6,-3,30,PINK))
        self.at('So cones depend')
        self.play(GrowArrow(a),FadeIn(label('support?',-2.65,1.35,28,GREY)),run_time=0.35)
        self.at('daylight')
        sun=VGroup(Circle(radius=0.32,color=YELLOW),*[Line([0.43*np.cos(t),0.43*np.sin(t),0],[0.6*np.cos(t),0.6*np.sin(t),0],color=YELLOW) for t in np.arange(0,TAU,TAU/8)]).move_to([2.65,1.8,0])
        self.play(FadeIn(sun),FadeIn(label('daylight',4.5,1.8,30)),run_time=0.2)
        self.at('color')
        wheel=VGroup(*[Sector(radius=0.5,start_angle=i*TAU/3,angle=TAU/3,fill_color=col,fill_opacity=1,stroke_width=0) for i,col in enumerate([RED,GREEN,BLUE])]).move_to([2.65,0,0])
        self.play(FadeIn(wheel),FadeIn(label('colour',4.5,0,30)),run_time=0.2)
        self.at('sharp central vision')
        self.play(FadeIn(label('E',2.65,-1.8,52,BLUE)),FadeIn(label('sharp central\nvision',4.65,-1.8,30)),run_time=0.2)
        self.finish()


class S08Why(TimedScene):
    def construct(self):
        cs=candidates(); self.add(*[c[0] for c in cs])
        self.at('Why cones die')
        self.play(FadeIn(label('Why do cones die?',y=3.25,size=36)),run_time=0.25)
        self.at('is not settled')
        self.play(FadeIn(stamp()),run_time=0.25)
        self.at('One candidate')
        self.play(cs[0][0].animate.set_stroke(TEAL,width=5),run_time=0.25)
        self.at('lost support from rods')
        self.play(FadeIn(cs[0][1]),run_time=0.25)
        self.finish()


def support_pair():
    return rod_cell(BLUE,1.7).move_to([-3.9,-0.2,0]),cone_cell(PINK,1.7).move_to([3.3,-0.2,0])


class S09Rdcvf(TimedScene):
    def construct(self):
        r,c=support_pair()
        self.add(label('Candidate: lost rod support',y=3.25,size=34),r,c,
            label('rod',-3.9,-3.25,30,BLUE),label('cone',3.3,-3.25,30,PINK))
        path=Arrow([-3.9,.25,0],[2.1,.25,0],color=GREEN,stroke_width=5,buff=0)
        factor=chip('cone viability\nfactor',GREEN,26,fill_opacity=1).move_to([-3.9,.25,0])
        factor[0].set_fill(BG,opacity=1)
        factor.set_z_index(3)
        self.at('Rods make')
        self.play(FadeIn(factor),GrowArrow(path),run_time=.3)
        self.at('cone viability factor')
        self.play(factor.animate.move_to([-.2,.25,0]),run_time=1.2)
        self.at('called',lead=0)
        named=chip('RdCVF',GREEN,32,fill_opacity=1).move_to(factor)
        named[0].set_fill(BG,opacity=1)
        self.play(Transform(factor,named),run_time=.3)
        self.play(factor.animate.move_to([2.1,.25,0]),run_time=.6)
        self.finish()


class S10Glucose(TimedScene):
    def construct(self):
        r=rod_cell(BLUE,1.55).move_to([-4.8,-.2,0])
        # Same tapered outer segment and rounded soma as s09, enlarged for the mechanism.
        # No axon tick: the soma fills the lower frame and contains the transport action.
        outer=Polygon([2.15,.25,0],[4.25,.25,0],[3.48,2.55,0],[2.92,2.55,0],
            stroke_color=PINK,stroke_width=4,fill_color=PINK,fill_opacity=.18)
        body=RoundedRectangle(width=5.2,height=3,corner_radius=.4,
            stroke_color=PINK,stroke_width=4,fill_color=PINK,fill_opacity=.10).move_to([3.2,-1.25,0])
        band=Rectangle(width=4.9,height=1.18,stroke_width=0,
            fill_color=PINK,fill_opacity=.28).move_to([3.2,-.48,0])
        b=chip('basigin-1',TEAL,28,fill_opacity=1).move_to([1.9,-.48,0])
        g=chip('GLUT1',TEAL,28,fill_opacity=1).move_to([4.5,-.48,0])
        for block in (b,g):
            block[0].set_fill(BG,opacity=1)
        factor=chip('RdCVF',GREEN,30,fill_opacity=1).move_to([-4.8,.9,0])
        factor[0].set_fill(BG,opacity=1)
        factor.set_z_index(3)
        dock=[1.9,.87,0]
        path=Arrow([-4.8,.9,0],dock,color=GREEN,stroke_width=5,buff=0)
        self.add(r,outer,body,band,label('rod',-4.8,-3.1,28,BLUE),
                 label('cone',3.2,-1.48,30,PINK),
                 label('experimental models, not a human trial',y=-3.5,size=26,color=GREY))
        self.at('In chicken cone cultures')
        self.play(FadeIn(label('chicken cone cultures + mouse model',y=3.3,size=30)),run_time=.25)
        self.at('binds')
        self.play(FadeIn(b),FadeIn(factor),GrowArrow(path),run_time=.2)
        self.play(factor.animate.move_to(dock),run_time=.55)
        self.play(Create(Line(factor.get_bottom(),b.get_top(),color=GREEN,stroke_width=5)),run_time=.2)
        self.at('associates with')
        self.play(FadeIn(g),Create(Line(b.get_right(),g.get_left(),color=TEAL,stroke_width=4)),run_time=.3)
        glucose=chip('glucose',GREEN,28,fill_opacity=1).move_to([4.5,1.3,0])
        glucose[0].set_fill(BG,opacity=1)
        glucose.set_z_index(3)
        entry=Arrow(glucose.get_bottom(),g.get_top(),color=GREEN,stroke_width=3,buff=.08)
        inside=Arrow(g.get_bottom(),[4.5,-2.25,0],color=GREEN,stroke_width=3,buff=.08)
        self.at('a glucose transporter')
        self.play(FadeIn(glucose),GrowArrow(entry),GrowArrow(inside),run_time=.3)
        self.at('cone glucose entry rises')
        self.play(entry.animate.set_stroke(width=11),inside.animate.set_stroke(width=11),
                  FadeIn(label('more glucose enters',2.65,-2.35,25,GREEN)),run_time=.3)
        self.hold(1.5)
        self.finish()


class S11Other(TimedScene):
    def construct(self):
        cs=candidates()
        self.add(label('Candidate mechanisms',y=3.25,size=36),cs[0],cs[1][0],cs[2][0],stamp())
        self.at('Cone starvation')
        self.play(FadeIn(cs[1][1]),cs[1][0].animate.set_stroke(TEAL,width=5),
             FadeIn(label('Cone starvation: Punzo and colleagues, 2009',y=-3.2,size=26,color=GREY)),run_time=0.25)
        self.at('oxidative damage')
        self.play(FadeIn(cs[2][1]),cs[2][0].animate.set_stroke(TEAL,width=5),run_time=0.25)
        self.finish()


class S12Rescue(TimedScene):
    def construct(self):
        # Sagittal schematic: convex cornea/lens at the left, posterior retina at right.
        globe=Ellipse(width=7.4,height=5.2,color=BLUE,stroke_width=5).move_to([-1.45,-.1,0])
        cornea=Arc(radius=1.2,start_angle=PI*.6,angle=PI*.8,color=BLUE,stroke_width=5).move_to([-5.05,-.1,0])
        lens=Ellipse(width=.65,height=2.05,color=BLUE,fill_color=BLUE,fill_opacity=.15).move_to([-4.15,-.1,0])
        retina_wall=Arc(radius=2.45,start_angle=-PI/3,angle=2*PI/3,color=PINK,stroke_width=12).stretch(1.4,0).shift([-1.45,-.1,0])
        self.add(globe,cornea,lens,retina_wall,label('front',-4.3,-2.95,28,GREY),
                 label('back: retina / RPE',1,-2.95,28,PINK))
        self.at('Can vision be rescued')
        self.play(FadeIn(label('Can vision be rescued?',y=3.25,size=36)),run_time=.25)
        gene=chip('working\ngene',GREEN,30,fill_opacity=1).move_to([4.6,0,0])
        gene[0].set_fill(BG,opacity=1)
        gene.set_z_index(3)
        self.at('Gene therapy')
        self.play(FadeIn(gene),run_time=.25)
        self.at('has begun to improve')
        path=Arrow([3.8,0,0],[-.4,0,0],color=GREEN,stroke_width=5,buff=0)
        self.play(GrowArrow(path),run_time=.25)
        self.play(gene.animate.move_to([-.4,0,0]),run_time=.65)
        self.at('specific genetic forms')
        self.play(FadeIn(label('specific genetic forms',y=-3.5,size=30,color=GREEN)),run_time=.25)
        self.finish()


class S13Rpe(TimedScene):
    def construct(self):
        participants=chip('participants',GREY,30).move_to([0,2.25,0])
        treated=chip('treated',GREEN,32).move_to([-3.4,.6,0])
        control=chip('control',BLUE,32).move_to([3.4,.6,0])
        # Three connected illumination lanes are part of the same large mobility course.
        course=VGroup()
        for i,t in enumerate(('dim','medium','bright')):
            y=-1.25-i*.72
            lane=Rectangle(width=8.1,height=.66,color=YELLOW,stroke_width=2,
                fill_color=YELLOW,fill_opacity=.04+i*.08).move_to([-.65,y,0])
            obstacles=VGroup(*[Rectangle(width=.32,height=.25,color=GREY,
                fill_color=GREY,fill_opacity=.6).move_to([x,y+.14*(-1)**j,0])
                for j,x in enumerate((-2.8,-.8,1.2))])
            route=VMobject(color=GREEN,stroke_width=3).set_points_as_corners(
                [[-4.4,y-.17,0],[-3.2,y-.17,0],[-2.1,y+.17,0],[-1.2,y+.17,0],[0,y-.17,0],[2.8,y-.17,0]])
            course.add(lane,obstacles,route,label(t,-5.55,y,26,YELLOW))
        course.add(Line([3.45,-1.25,0],[3.45,-2.69,0],color=YELLOW,stroke_width=4))
        grader=chip('masked\ngrader',GREY,26).move_to([5,-1.95,0])
        self.add(trial_head('RPE65 gene augmentation'),participants)
        self.add(label('Russell and colleagues, 2017',y=-3.5,size=26,color=GREY))
        self.at('One trial added')
        gene=chip('working RPE65',GREEN,28).move_to([-3.4,2.25,0])
        self.play(FadeIn(gene),FadeIn(treated),run_time=.25)
        self.play(GrowArrow(Arrow(gene.get_bottom(),treated.get_top(),color=GREEN,buff=.12)),run_time=.25)
        self.at('It was randomized')
        self.play(GrowArrow(Arrow([-.9,2,0],[-2.7,1,0],color=GREY,buff=.1)),
            GrowArrow(Arrow([.9,2,0],[2.7,1,0],color=GREY,buff=.1)),FadeIn(control),run_time=.3)
        self.at('and open')
        self.play(FadeIn(label('randomized • open-label',y=-.25,size=28)),run_time=.25)
        self.at('with masked grading')
        self.play(FadeIn(course),FadeIn(grader),
            Create(Line([3.5,-1.95,0],[4.1,-1.95,0],color=GREY)),run_time=.25)
        self.at('a mobility test')
        walker=Dot([-4.4,-1.42,0],radius=.13,color=GREEN)
        self.play(FadeIn(walker),run_time=.2)
        self.play(MoveAlongPath(walker,course[2]),run_time=.8)
        self.hold(1.5)
        self.finish()


class S14Result(TimedScene):
    def construct(self):
        x=lambda v:-5.4+4.25*v
        # Exact trial values mapped linearly, including the zero null value.
        axis=Line([x(0),-.15,0],[x(2.5),-.15,0],color=GREY,stroke_width=4)
        ticks=VGroup(*[Line([x(v),-.32,0],[x(v),.02,0],color=GREY) for v in (0,.72,1.6,2.41)])
        vals=VGroup(*[label(t,x(v),-.75,28) for v,t in ((0,'0'),(.72,'0.72'),(1.6,'1.6'),(2.41,'2.41'))])
        self.add(trial_head('RPE65 • mobility test'),axis,ticks,vals,
            label('difference in light levels (treated minus control)',y=-2.1,size=30),
            label('no difference',x(0)+.5,-1.35,26,GREY),
            label('treated better →',2,-1.35,28,GREEN))
        self.at('At one year')
        self.play(FadeIn(label('at one year',y=2.5,size=28)),run_time=.2)
        self.at('treated participants did better')
        self.play(FadeIn(label('treated better than control',y=1.75,size=34,color=GREEN)),run_time=.25)
        self.at('by')
        interval=Line([x(.72),.55,0],[x(2.41),.55,0],color=GREEN,stroke_width=9)
        ends=VGroup(*[Line([x(v),.3,0],[x(v),.8,0],color=GREEN,stroke_width=5) for v in (.72,2.41)])
        self.play(Create(interval),FadeIn(ends),FadeIn(Dot([x(1.6),.55,0],radius=.17,color=GREEN)),
            FadeIn(label('1.6 light levels',x(1.6),1.1,36,GREEN)),
            FadeIn(label('95% CI: 0.72 to 2.41',y=-3.05,size=30,color=GREY)),run_time=.35)
        self.finish()


class S15Cep(TimedScene):
    def construct(self):
        pair=eye_pair(); self.add(pair)
        self.at('A later study')
        self.play(FadeIn(trial_head('CEP290 editing • 14 participants')),
            FadeIn(label('Pierce and colleagues, 2024',y=-3.6,size=26,color=GREY)),run_time=.25)
        tool=chip('editing\nmachinery',GREEN,24,pad=.16).move_to([0,2.2,0])
        self.at('delivered editing machinery')
        self.play(FadeIn(tool),run_time=.25)
        self.at('inside the eye',lead=0)
        # Within the lower sclera, clear of iris, pupil, and outer wall.
        self.play(tool.animate.move_to([-3.25,-1.4,0]),run_time=.4)
        self.at('It had no randomized')
        self.play(FadeIn(label('single arm • no randomized or sham control',y=-3.1,size=28,color=GOLD)),run_time=.25)
        self.at('only the untreated')
        self.play(Indicate(pair[1],color=GREY,scale_factor=1.03),run_time=.35)
        self.finish()


class S16Safety(TimedScene):
    def construct(self):
        boxes=VGroup(*[RoundedRectangle(width=1.45,height=1.7,corner_radius=.15,color=GREY,
            fill_color=GREY,fill_opacity=.12).move_to([-5.25+(i%7)*1.75,1.15-(i//7)*2.0,0]) for i in range(14)])
        marks=VGroup(*[T('✓',size=34,color=GREEN).move_to(b) for b in boxes])
        self.add(trial_head('CEP290 • 14 participants'),boxes,
                 label('single arm • counts pooled across three dose levels',y=-3.5,size=26,color=GREY))
        self.at('It recorded no')
        self.play(FadeIn(marks),FadeIn(label('all 14: no dose-limiting toxicity',y=2.5,size=30,color=GREEN)),run_time=.3)
        self.at('signs of possible benefit')
        self.play(*[b.animate.set_fill(GOLD,opacity=.28).set_stroke(GOLD,width=4) for b in boxes[:6]],
            FadeIn(label('6 of 14: improved cone-mediated sensitivity',y=-2.25,size=30,color=GOLD)),
            FadeIn(label('possible signal • no control',y=-2.9,size=30,color=GOLD)),run_time=.3)
        self.hold(1.5)
        self.finish()


class S17Limits(TimedScene):
    def construct(self):
        pair=VGroup(eye(-3.25,.5,GREEN,1.05),eye(3.25,.5,GREY,1.05),
            label('treated',-3.25,-1.35,28,GREEN),label('fellow eye',3.25,-1.35,28,GREY))
        head=trial_head('CEP290 • interpreting the fellow eye')
        self.add(pair,head)
        self.at('shares the person')
        bracket=VGroup(Line([-5.8,2.4,0],[5.8,2.4,0],color=TEAL),
            Line([-5.8,2.4,0],[-5.8,2.1,0],color=TEAL),Line([5.8,2.4,0],[5.8,2.1,0],color=TEAL))
        self.play(Create(bracket),FadeIn(label('shared: person • testing days',y=2.8,size=28,color=TEAL)),run_time=.3)
        cards=VGroup(*[chip(t,GREY,30).move_to([x,-3.05,0]) for t,x in (('practice',-4.3),('expectation',0),('fluctuation',4.3))])
        self.at('but practice')
        lower=VGroup(Line([-5.8,-1.7,0],[5.8,-1.7,0],color=GOLD),
            Line([-5.8,-1.7,0],[-5.8,-1.55,0],color=GOLD),Line([5.8,-1.7,0],[5.8,-1.55,0],color=GOLD))
        self.play(FadeIn(cards[0]),FadeIn(label('cannot be fully separated',y=-2.4,size=24,color=GREY)),Create(lower),FadeIn(label('not shared: procedure • eye-specific change',y=-2.0,size=26,color=GOLD)),run_time=.25)
        self.at('expectation'); self.play(FadeIn(cards[1]),run_time=.25)
        self.at('fluctuation'); self.play(FadeIn(cards[2]),run_time=.25)
        self.at('cannot be fully separated')
        self.play(Transform(head,label('Cannot fully separate these from treatment',y=3.4,size=30,color=GREY)),run_time=.25)
        self.finish()


class S18Take(TimedScene):
    def construct(self):
        head=label('The design limits the claim.',y=3.3,size=38)
        rows=VGroup(*[Rectangle(width=12.7,height=2.5,color=GREY).move_to([0,y,0]) for y in (.65,-1.95)])
        divider=Line([-.65,1.9,0],[-.65,-3.2,0],color=GREY)
        self.add(rows,divider,label('DESIGN',-3.5,2.45,30),label('WHAT IT SUPPORTS',2.85,2.45,30))
        self.at('The takeaway'); self.play(FadeIn(head),run_time=.25)
        self.at('The randomized trial')
        self.play(FadeIn(label('RPE65\nrandomized control\nopen-label • masked grading',-3.5,.65,29)),run_time=.25)
        self.at('supports a benefit')
        self.play(FadeIn(label('treated beat control\n1.6 light levels\nmobility test • one year',2.85,.65,32,GREEN)),run_time=.25)
        self.at('A small single arm')
        self.play(FadeIn(label('CEP290\nsingle arm\nfellow eye only',-3.5,-1.95,32)),run_time=.25)
        self.at('supports observed safety')
        self.play(FadeIn(label('no dose-limiting toxicity\nduring follow-up',2.85,-1.45,29,GOLD)),run_time=.25)
        self.at('a preliminary signal')
        self.play(FadeIn(label('preliminary signal',2.85,-2.65,32,GOLD)),run_time=.25)
        self.hold(3.2)
        self.finish()


class S19End(EndCard):
    LINE = 'The design limits the claim.'
    def construct(self):
        line=label(self.LINE,y=.35,size=44)
        self.play(FadeIn(line),run_time=.3)
        self.wait(2.1)
        self.play(FadeIn(label('biochemistrypedia.com',y=-.65,size=28,color=TEAL)),run_time=.3)
        self.finish()
