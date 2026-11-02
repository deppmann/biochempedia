"""Cutting the Bridge: timed schematic pathways, no quantitative traces.
COLOR MAP: BLUE = left hemisphere / right hand; YELLOW = right hemisphere /
left hand / left visual field; GREY = neutral anatomy; RED = blocked;
GREEN = answer. Paths are schematic, not measured anatomical trajectories.
"""
from bp_style import *


def label(s, x, y, size=28, color=TEXT):
    return T(s, size=size, color=color).move_to([x,y,0])


def path(points, color=GREY, width=6):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([[x,y,0] for x,y in points])


def key_icon(color=YELLOW):
    return VGroup(Circle(radius=.23,color=color,stroke_width=6).move_to([-.45,0,0]),
                  path([(-.22,0),(.65,0),(.65,-.2)],color),
                  Line([.35,0,0],[.35,-.2,0],color=color,stroke_width=6))


def spoon(color=BLUE):
    return VGroup(Ellipse(width=.44,height=.68,color=color,stroke_width=5).shift(UP*.45),
                  Line([0,.1,0],[0,-.8,0],color=color,stroke_width=6))


def hand(color=YELLOW):
    pts=[(-.48,-.65),(-.48,.15),(-.72,.45),(-.6,.62),(-.3,.36),
         (-.3,.95),(-.14,1.05),(-.03,.42),(.07,1.18),(.23,1.18),
         (.3,.42),(.43,1.04),(.58,1.0),(.56,.37),(.72,.77),(.85,.69),(.65,-.65)]
    return Polygon(*[[x,y,0] for x,y in pts],color=color,fill_color=color,fill_opacity=.18,stroke_width=3)


def bubble(text, x=-3.25, y=1.05, color=TEXT):
    # Internal speech panel: both border and tail lie entirely inside the hemisphere.
    box=RoundedRectangle(width=3.8,height=1.05,corner_radius=.22,color=color,stroke_width=2)
    tail=path([(-.9,-.525),(-1.1,-.85),(-.5,-.525)],color,2)
    return VGroup(box,tail,label(text,0,0,28,color)).move_to([x,y,0])


def person(closed=False, blind=False):
    head=Circle(radius=.78,color=GREY,stroke_width=4).move_to([-3,1.1,0])
    body=path([(-4.55,-1.5),(-4.55,-.6),(-4.1,.1),(-3.65,.35),(-2.35,.35),(-1.9,.1),(-1.45,-.6),(-1.45,-1.5)],GREY,4)
    eyes=VGroup(*[Line([x-.12,1.2,0],[x+.12,1.2,0],color=TEXT,stroke_width=4) if closed else Dot([x,1.2,0],radius=.055,color=TEXT) for x in [-3.28,-2.72]])
    if blind: eyes=Rectangle(width=1.47,height=.35,color=GREY,fill_color=GREY,fill_opacity=1).move_to([-3,1.2,0])
    return VGroup(head,body,eyes)


def test_screen():
    return VGroup(RoundedRectangle(width=6.5,height=2.8,corner_radius=.12,color=GREY).move_to([2.5,1.05,0]),
                  Dot([2.5,1.05,0],radius=.075,color=TEXT))


def tray():
    return VGroup(Rectangle(width=6.5,height=1.9,color=GREY,fill_color=GREY,fill_opacity=.08).move_to([2.5,-1.9,0]),
                  label('behind screen',2.5,-3.3,26,GREY))


def hemis(speaks=False, cut=True):
    l=RoundedRectangle(width=4.6,height=4.4,corner_radius=.65,color=BLUE,fill_color=BLUE,fill_opacity=.1).move_to([-3.25,.4,0])
    r=l.copy().set_color(YELLOW).set_fill(YELLOW,.1).move_to([3.25,.4,0])
    labs=VGroup(label('left hemisphere',-3.25,3,28,BLUE),label('right hemisphere',3.25,3,28,YELLOW))
    bridge=VGroup(Line([-.95,.4,0],[-.26,.4,0],color=GREY,stroke_width=10),Line([.26,.4,0],[.95,.4,0],color=GREY,stroke_width=10))
    if cut: bridge.add(path([(-.18,-.05),(.18,.85)],RED,5),path([(-.18,.85),(.18,-.05)],RED,5))
    if speaks: labs.add(label('speaks',-3.25,1.55,34,BLUE))
    return VGroup(l,r,labs,bridge)


def touch_motor():
    # Both routes pass below the left box, with separate lanes at the hand.
    up=path([(-4.15,-2.55),(-3.5,-2.15),(0,-2.15),(3.2,-2.15),(3.2,-.65)],YELLOW,6)
    up.add(Arrow([3.2,-1.2,0],[3.2,-.5,0],color=YELLOW,buff=0,stroke_width=6))
    down=DashedVMobject(path([(4.3,-.8),(4.3,-2.85),(0,-2.85),(-3.6,-2.85)],YELLOW,5),num_dashes=30)
    down.add(Arrow([-3.35,-2.85,0],[-4,-2.85,0],color=YELLOW,buff=0,stroke_width=5))
    band=VGroup(Line([0,-3.02,0],[0,-1.98,0],color=GREY,stroke_width=7),
                label('medulla',1.5,-2.5,26,GREY),Line([.7,-2.5,0],[.12,-2.5,0],color=GREY,stroke_width=2))
    labs=VGroup(label('touch',-1.9,-1.96,26,YELLOW),label('mainly motor',.9,-3.4,26,YELLOW))
    return VGroup(up,down,band,labs)


def eyes_paths():
    eyes=VGroup(*[Circle(radius=.73,color=GREY,stroke_width=3).move_to([x,1.35,0]) for x in [-2.5,2.5]],
                label('left eye',-4.4,1.65,26),label('right eye',4.4,1.65,26))
    retina=VGroup(*[Line([x-.55,.92,0],[x,.67,0],color=GREY,stroke_width=7) for x in [-2.5,2.5]],
                  *[Line([x,.67,0],[x+.55,.92,0],color=GREY,stroke_width=7) for x in [-2.5,2.5]])
    nasal=VGroup(path([(-2.25,.78),(0,-.6),(2.8,-2.1)],GREY,5),path([(2.25,.78),(0,-.6),(-2.8,-2.1)],GREY,5))
    temporal=VGroup(path([(-2.95,.87),(-3.8,-.7),(-3.8,-2.1)],GREY,5),path([(2.95,.87),(3.8,-.7),(3.8,-2.1)],GREY,5))
    ends=VGroup(chip('left hemisphere',BLUE,28).move_to([-3.25,-2.5,0]),chip('right hemisphere',YELLOW,28).move_to([3.25,-2.5,0]))
    # Explicitly land fibres on the receiving panel, rather than above it.
    for route in list(nasal)+list(temporal):
        route.add(Line(route.get_end(),[route.get_end()[0],ends[0].get_top()[1],0],color=GREY,stroke_width=5))
    return VGroup(eyes,retina,nasal,temporal,ends)


def question_frame():
    p=person(closed=True).scale(1.25).move_to([-3.6,.2,0])
    screen=test_screen().stretch_to_fit_height(1.9).move_to([2.5,.6,0]).set_stroke(opacity=.3).set_fill(opacity=0)
    h=hand(BLUE).scale(1.05).move_to([2,-1.75,0])
    sp=spoon().scale(1.05).move_to([2.25,-1.25,0])
    return VGroup(p,tray(),h,sp,label('right hand',4.4,-1.8,28,BLUE),label('Can he name it?',-.8,3.1,38),screen)


class S00Title(TitleCard):
    LESSON='Language and Lateralization'
    TITLE='Cutting the Bridge'

    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',size=26,color=TEAL,weight=BOLD)
        lesson=T(self.LESSON.upper(),size=26,color=GREY)
        title=T(self.TITLE,size=54,font=TITLE_FONT)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.35)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=.35)
        self.play(FadeIn(title),GrowFromCenter(rule),run_time=.5)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(person().scale(1.2).move_to([-3.6,-.15,0]),test_screen(),tray())
        k=key_icon().scale(1.15).move_to([.6,1.05,0]); ghost=k.copy().set_stroke(opacity=.25).set_fill(opacity=0)
        self.at('A key flashes'); self.play(FadeIn(k),run_time=.1); self.wait(.6)
        self.play(Transform(k,ghost),FadeIn(label('key was here',.6,.15,26,GREY)),run_time=.2)
        self.at('The man says'); self.play(FadeIn(bubble('I saw nothing',-3.6,2.7)),run_time=.35)
        h=hand().scale(.95).move_to([1.8,-1.9,0]); held=key_icon().move_to([1.85,-1.4,0])
        self.at('Yet his left hand'); self.play(FadeIn(h),FadeIn(held),FadeIn(label('left hand',4.4,-1.9,28,YELLOW)),run_time=.3)
        self.at('picks out the key'); self.play(VGroup(h,held).animate.shift(UP*.5),run_time=.6)
        self.play(FadeIn(label('How?',-3.6,-2.9,44)),run_time=.3); self.finish()


class S02Surgery(SpokenScene):
    def construct(self):
        cortex=path([(-4.6,-1.5),(-4.9,-.3),(-4.5,1.2),(-3.5,2.2),(-1.8,2.7),(.5,2.65),(2.5,2.1),(4,1),(4.6,-.4),(4,-1.7),(2.5,-2.1),(.8,-1.75),(-.4,-2.15),(-2.6,-2.1),(-4.6,-1.5)],GREY,4)
        folds=VGroup(*[Arc(radius=.65,start_angle=.1,angle=2.5,color=GREY,stroke_width=2).move_to([x,y,0]) for x,y in [(-3,1),(-1.3,1.5),(.6,1.5),(2.6,.8)]])
        a=path([(-2.8,-.4),(-2.5,.65),(-1.4,1.15),(-.15,1.15)],GREY,20)
        b=path([(.15,1.15),(1.3,1.15),(2.4,.6),(2.7,-.4)],GREY,20)
        self.add(cortex,folds,a,b,label('front',-5.5,0,26,GREY),label('back',5.35,0,26,GREY),label('midline view',0,3.25,26,GREY))
        self.at('Cutting the forebrain'); self.play(a.animate.shift(LEFT*.22),b.animate.shift(RIGHT*.22),Create(Line([0,.55,0],[0,1.8,0],color=RED,stroke_width=6)),run_time=.65)
        self.at('treat epilepsy'); self.play(FadeIn(label('epilepsy uncontrolled by drugs',0,-3,30)),run_time=.4)
        self.at('The corpus callosum'); self.play(a.animate.set_color(YELLOW),b.animate.set_color(YELLOW),FadeIn(label('corpus callosum',0,0,32,YELLOW)),run_time=.45)
        self.at('largest commissure'); self.play(FadeIn(label('largest commissure',0,-.8,28,YELLOW)),run_time=.3); self.finish()


class S03Wj(SpokenScene):
    def construct(self):
        self.add(Line([-5,1.8,0],[5,1.8,0],color=GREY),Dot([0,1.8,0],color=GOLD),label('1962',0,2.6,50,GOLD))
        self.at('In'); self.play(FadeIn(label('Gazzaniga, Bogen and Sperry',0,.65,36)),run_time=.45)
        self.at('one such patient'); self.play(FadeIn(chip('Patient W.J.',GREY,40).move_to([0,-.65,0])),run_time=.4)
        icon=VGroup(Line([-1.1,-2.15,0],[-.3,-2.15,0],color=GREY,stroke_width=8),Line([.3,-2.15,0],[1.1,-2.15,0],color=GREY,stroke_width=8),label('×',0,-2.15,40,RED))
        self.play(FadeIn(icon),FadeIn(label('forebrain commissures cut',0,-3,28)),run_time=.4); self.finish()


class S04Wj2(SpokenScene):
    def construct(self):
        self.at('Blindfolded'); self.add(person(blind=True).scale(1.65).move_to([-2,.1,0]))
        h=hand().scale(1.05).move_to([.5,-1.9,0])
        comb=VGroup(Rectangle(width=1.8,height=.22,color=YELLOW),*[Line([x,0,0],[x,-.45,0],color=YELLOW,stroke_width=4) for x in [-.75,-.45,-.15,.15,.45,.75]]).move_to([.6,-1.25,0])
        self.at('use familiar objects'); self.play(FadeIn(h),FadeIn(comb),run_time=.4)
        self.at('with his left hand'); self.play(VGroup(h,comb).animate.shift(LEFT*.65),FadeIn(label('left hand',2.1,-2.5,30,YELLOW)),run_time=.55)
        self.at('But he could'); self.play(FadeIn(bubble('',1.45,2,RED)),FadeIn(label('×',1.45,2.15,56,RED)),FadeIn(label('cannot name it',2.4,.65,30,RED)),run_time=.4); self.finish()


class S05Chiasm(SpokenScene):
    def construct(self):
        g=eyes_paths(); self.add(g[0],g[1],g[4])
        self.at('First'); self.play(Create(g[3]),run_time=.5)
        self.at('At the optic chiasm'); self.play(Create(g[2]),FadeIn(label('optic chiasm',0,-1.75,28)),Create(Line([0,-1.4,0],[0,-.65,0],color=GREY,stroke_width=2)),run_time=.5)
        self.at('only the'); self.play(g[2][0].animate.set_color(YELLOW),g[2][1].animate.set_color(BLUE),run_time=.45)
        self.at('nasal half'); self.play(FadeIn(label('nasal',0,.9,28)),Create(Line([-.45,.65,0],[-1.35,.22,0],color=GREY,stroke_width=2)),FadeIn(label('temporal',-5,-.4,28)),Create(Line([-4.5,-.65,0],[-3.8,-.9,0],color=GREY,stroke_width=3)),run_time=.3); self.finish()


class S06Field(SpokenScene):
    def construct(self):
        g=eyes_paths(); self.add(g)
        field=Rectangle(width=4.4,height=.7,color=YELLOW,fill_color=YELLOW,fill_opacity=.2).move_to([-2.2,3,0])
        fixation=VGroup(Dot([0,3,0],radius=.07),label('fixation',1.05,3,26))
        rays=VGroup(Arrow([-1.4,2.6,0],[-2.25,.8,0],color=YELLOW,buff=0,stroke_width=3),Arrow([-1.4,2.6,0],[2.95,.87,0],color=YELLOW,buff=0,stroke_width=3))
        self.at('So everything'); self.play(FadeIn(field),FadeIn(fixation),run_time=.3)
        self.at('left of the point'); self.play(FadeIn(label('left visual field',-2.2,3,26,YELLOW)),Create(rays),run_time=.6)
        self.at('reaches the right'); self.play(g[2][0].animate.set_color(YELLOW),g[3][1].animate.set_color(YELLOW),g[4][1][0].animate.set_fill(YELLOW,.3),run_time=.6)
        self.at('from both eyes'); self.play(Indicate(g[0][0],color=YELLOW),Indicate(g[0][1],color=YELLOW),run_time=.5)
        self.at('The hemifield matters'); self.play(FadeIn(label('hemifield, not eye',0,-3.3,32)),run_time=.4); self.finish()


class S07Flash(SpokenScene):
    def construct(self):
        screen=test_screen().scale(1.45).move_to([0,.5,0]); self.add(screen)
        k=key_icon().scale(1.2).move_to([-2.4,.5,0]); trace=k.copy().set_stroke(opacity=.22).set_fill(opacity=0)
        self.add(label('left field',-2.4,-.5,28,YELLOW))
        flash=label('flash',-2.4,1.5,28)
        self.at('A brief flash'); self.play(FadeIn(k),FadeIn(flash),run_time=.1); self.wait(.5)
        self.play(Transform(k,trace),FadeOut(flash),FadeIn(label('gone',-2.4,1.5,26,GREY)),run_time=.2)
        self.play(FadeIn(label('e.g. 150 ms or less',0,3.2,30,GREY)),run_time=.3)
        ring=Circle(radius=.52,color=GREEN,stroke_width=4).move_to(screen[1])
        self.at('monitor his gaze'); self.play(Create(ring),FadeIn(label('maintain fixation • track gaze',0,-2.25,30)),run_time=.4)
        self.at('discard trials'); self.play(ring.animate.move_to(k),run_time=.45)
        x=label('×',-2.4,.5,88,RED)
        self.play(FadeIn(x),run_time=.2)
        self.play(FadeIn(chip('reject eye-movement trials',RED,28).move_to([0,-3.2,0])),run_time=.3)
        self.at('the other hemisphere'); self.play(ring.animate.set_color(RED),run_time=.3); self.finish()


class S08Touch(SpokenScene):
    def construct(self):
        b=hemis(); h=hand().scale(.65).move_to([-4.65,-2.85,0]); p=touch_motor()
        self.add(b,h,label('left hand',-4.65,-3.65,26,YELLOW))
        self.at('Touch from'); self.play(Create(p[0]),FadeIn(p[3][0]),run_time=.9)
        self.at('right hemisphere'); self.play(b[1].animate.set_fill(YELLOW,.25),FadeIn(p[2]),run_time=.4)
        self.at('each hand'); self.play(Create(p[1]),run_time=.65)
        self.at('controlled mainly'); self.play(FadeIn(p[3][1]),run_time=.4); self.finish()


class S09Rule(SpokenScene):
    def construct(self):
        b=hemis(); self.add(b)
        self.at('Now apply'); self.play(FadeIn(label('You can say only what reaches',0,-2.6,34)),run_time=.4)
        self.at('the speaking hemisphere'); self.play(FadeIn(label('the speaking hemisphere.',0,-3.25,34)),run_time=.4)
        self.at('that is the left'); self.play(FadeIn(label('speaks',-3.25,.8,42,BLUE)),run_time=.4); self.finish()


class S10Answer(SpokenScene):
    def construct(self):
        b=hemis(speaks=True); k=key_icon().scale(1.2).move_to([-3.8,-2.65,0]); self.add(b,k,label('left field',-3.8,-3.35,26,YELLOW))
        p=path([(-2.8,-2.65),(3.25,-2.65),(3.25,-.65)],YELLOW,6)
        self.at('The key'); self.play(Create(p),run_time=1)
        self.at('only the right'); self.play(b[1].animate.set_fill(YELLOW,.3),FadeIn(key_icon().scale(1.2).move_to([3.25,.8,0])),run_time=.4)
        self.at('With the bridge cut'); self.play(Create(Arrow([1.05,.65,0],[.3,.65,0],color=YELLOW,buff=0,stroke_width=6,max_tip_length_to_length_ratio=.25)),run_time=.45)
        self.at('no route to speech'); self.play(Indicate(b[3],color=RED,scale_factor=1.1),FadeIn(label('blocked',.1,2.5,26,RED)),run_time=.4); self.finish()


class S11Answer2(SpokenScene):
    def construct(self):
        b=hemis(); b[1].set_fill(YELLOW,.25); self.add(b)
        self.at('so he cannot'); self.play(FadeIn(bubble('I saw nothing')),run_time=.4)
        h=hand().scale(.65).move_to([-4.65,-2.85,0]); k=key_icon().scale(.7).move_to([-4.55,-2.5,0]); p=touch_motor()
        self.at('But his right'); self.play(FadeIn(h),FadeIn(k),Create(p[0]),Create(p[1]),FadeIn(p[2]),FadeIn(p[3]),run_time=.8)
        self.at('the left hand'); self.play(FadeIn(label('left hand',-4.65,-3.65,26,YELLOW)),run_time=.3)
        self.at('which finds'); self.play(VGroup(h,k).animate.shift(UP*.15),run_time=.45); self.finish()


class S12Q(SpokenScene):
    def construct(self):
        g=question_frame(); self.add(g[0],g[1],g[6])
        self.at('Now his eyes'); self.wait(.2)
        self.at('a spoon is placed'); self.play(FadeIn(g[2]),FadeIn(g[3]),FadeIn(g[4]),run_time=.55)
        self.at('Can he name it'); self.play(FadeIn(g[5]),run_time=.3); self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame())
        # Clockwise progress arc, two units across, next to the question.
        track=Circle(radius=.85,color=GREY,stroke_width=3).move_to([4.7,2.55,0]); self.add(track)
        sweep=Arc(radius=.85,start_angle=PI/2,angle=-TAU,color=GREEN,stroke_width=8).move_to(track)
        self.play(Create(sweep,rate_func=linear),run_time=5)


class S14Reveal(SpokenScene):
    def construct(self):
        q=question_frame(); self.add(q)
        yes=label('Yes.',-.8,3.1,42,GREEN)
        self.at('Yes'); self.play(ReplacementTransform(q[5],yes),run_time=.3)
        self.at('touch from the right hand'); self.play(FadeOut(q),FadeOut(yes),run_time=.25)
        b=hemis(); h=hand(BLUE).scale(.85).move_to([3.5,-2.65,0]); sp=spoon().scale(.8).move_to([3.65,-2.2,0]); self.add(b,h,sp,label('right hand',5.35,-2.8,26,BLUE))
        p=path([(3.5,-2),(1,-1.3),(-1,-.9),(-3.25,-.5)],BLUE,6)
        p.add(Arrow([-2.65,-.61,0],[-3.25,-.5,0],color=BLUE,buff=0,stroke_width=6))
        crossing=Line([-.13,-1.55,0],[.13,-.65,0],color=GREY,stroke_width=8)
        self.at('crosses in the medulla'); self.play(Create(p),Create(crossing),FadeIn(label('medulla',0,-2.3,26,GREY)),Create(Line([0,-1.95,0],[0,-1.55,0],color=GREY,stroke_width=2)),run_time=.65)
        self.play(FadeIn(bubble('spoon',color=BLUE)),run_time=.35)
        self.at('which usually speaks'); self.play(b[0].animate.set_fill(BLUE,.23),run_time=.3); self.finish()


class S15Flip(SpokenScene):
    def construct(self):
        b=hemis()
        # Raise the lower borders so the held objects stay clear of them.
        for side in b[:2]:
            side.stretch_to_fit_height(4).shift(UP*.4)
        speaks=label('speaks',-3.25,2,30,BLUE)
        left=bubble('spoon',-3.25,1,BLUE); right=bubble('cannot name key',3.25,1,RED)
        lh=hand().scale(.85).move_to([-3.6,-2.4,0]); rh=hand(BLUE).scale(.85).move_to([3.6,-2.4,0])
        items=VGroup(key_icon().scale(.85).move_to([-3.55,-1.95,0]),spoon().scale(.75).move_to([3.65,-1.95,0]))
        wires=VGroup(path([(-3.25,-.15),(-2,-.75),(0,-1.15),(3.5,-1.9)],BLUE,4),path([(3.25,-.15),(2,-.65),(0,-1.6),(-3.5,-1.9)],YELLOW,4))
        # A dark clearance at the crossing preserves both lanes.
        wires[1].set_z_index(2)
        self.add(b,speaks,left,right,wires,lh,rh,items,
                 label('left hand',-5.35,-2.75,26,YELLOW),label('right hand',5.35,-2.75,26,BLUE),
                 label('finds key',-3.6,-3.5,26,YELLOW),label('holds spoon',3.6,-3.5,26,BLUE))
        self.wait(.7)
        self.at('speech were on the right'); self.play(FadeOut(left),FadeOut(right),speaks.animate.move_to([3.25,2,0]).set_color(YELLOW),run_time=.6)
        self.at('naming answers would flip'); self.play(FadeIn(bubble('cannot name spoon',-3.25,1,RED)),FadeIn(bubble('key',3.25,1,YELLOW)),run_time=.55)
        self.at('The hands would still'); self.play(FadeIn(label('hand results do not change',0,-2.65,26,GREY)),run_time=.4); self.finish()


class S16Rh(SpokenScene):
    def construct(self):
        b=hemis(speaks=True); self.add(b)
        glow=Ellipse(width=3.8,height=2.4,stroke_width=0,fill_color=YELLOW,fill_opacity=.12).move_to([3.25,.2,0])
        self.at('the disconnected right'); self.play(FadeIn(glow),run_time=.4)
        self.at('understands some spoken words'); self.play(FadeIn(label('understands\nsome words',3.25,.6,32,YELLOW)),run_time=.4)
        self.at('It is mute'); self.play(FadeIn(label('cannot say them',3.25,-.9,30,RED)),run_time=.4); self.finish()


class S17Rh2(SpokenScene):
    def construct(self):
        b=hemis(); self.add(b)
        glow=VGroup(*[Ellipse(width=3.7,height=1.2,stroke_width=0,fill_color=c,fill_opacity=.13).move_to([x,-1.05,0]) for x,c in [(-3.25,BLUE),(3.25,YELLOW)]])
        self.add(glow[1],label('some words',3.25,-1.05,28,YELLOW))
        self.at('That fits'); self.wait(.2)
        self.at('Understanding words'); self.add(label('understanding: both sides',0,-2.6,32)); self.play(FadeIn(glow[0]),FadeIn(label('words',-3.25,-1.05,28,BLUE)),run_time=.4)
        planner=chip('planner',BLUE,30).move_to([-3.25,1.2,0])
        road=Arrow([-4.15,-.65,0],[-3.65,.8,0],color=BLUE,buff=0,stroke_width=5)
        road_label=label('to speech',-4.7,.15,24,BLUE)
        self.at('the road to speech'); self.play(FadeIn(planner),Create(road),FadeIn(road_label),run_time=.5)
        self.at('usually runs'); self.play(FadeIn(label('road to speech: usually left',0,-3.25,32,BLUE)),run_time=.4); self.finish()


class S18Pinto(SpokenScene):
    def construct(self):
        card=RoundedRectangle(width=10.7,height=4.3,corner_radius=.3,color=GREY)
        content=VGroup(card,label('Exceptions',0,1.3,48),
                       label('two patients • 2017',0,.1,42,GOLD),
                       label('See Going deeper in the lesson',0,-1.25,36,TEAL))
        self.at('The tidy rule'); self.add(content); self.finish()


class S19Takeaway(SpokenScene):
    def construct(self):
        b=hemis(speaks=True); self.add(b)
        self.at('His right hemisphere'); self.play(b[1].animate.set_fill(YELLOW,.2),run_time=.35)
        self.at('see'); self.play(FadeIn(label('see',3.25,1.65,34,YELLOW)),run_time=.25)
        self.at('feel'); self.play(FadeIn(label('feel',3.25,.65,34,YELLOW)),run_time=.25)
        self.at('understand some words'); self.play(FadeIn(label('understand\nsome words',3.25,-.6,32,YELLOW)),run_time=.35)
        self.at('But he cannot say'); self.play(FadeIn(chip('cannot say',RED,32).move_to([3.25,-2.65,0])),run_time=.4)
        self.at('the speaking hemisphere'); self.play(Indicate(b[3],color=RED,scale_factor=1.1),run_time=.4); self.finish()


class S20End(EndCard):
    LINE='He cannot say what never reaches\nthe speaking hemisphere.'

    def construct(self):
        line=T(self.LINE,size=44,font=TITLE_FONT,line_spacing=1.2)
        sub=T('biochemistrypedia.com',size=26,color=TEAL)
        VGroup(line,sub).arrange(DOWN,buff=.6)
        self.play(FadeIn(line),run_time=.5)
        self.play(FadeIn(sub),run_time=.3)
        self.finish()
