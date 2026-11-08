"""Enough Does Not Prove Needed — word-timed chapter animation.
COLOR MAP (from scenes.old.py): YELLOW active cells; BLUE light / opsin;
GREEN tagged cells; RED silenced cells / shock;
PURPLE controls; GOLD questions; GREY resting cells / structure; ORANGE candidates.
YELLOW also denotes freezing behavior; GREEN is reserved for tags.
Bars are qualitative schematics of the narrated comparisons, not numerical data.
No plotted curves are used. Cell and ring helpers preserve the reference model.
"""
from bp_style import *
import numpy as np

PURPLE = '#B58CD9'
ORANGE = '#F29E4C'


def cell(p, r=0.26):
    p = np.array([p[0], p[1], 0.])
    soma = Circle(radius=r, stroke_color=GREY, stroke_width=3,
                  fill_color=GREY, fill_opacity=.25).move_to(p)
    stubs = VGroup()
    for ang in (100, 215, 325):
        d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        stubs.add(Line(p+d*r, p+d*(r+.17), color=GREY, stroke_width=3))
    g = VGroup(soma, stubs)
    g.soma, g.stubs = soma, stubs
    return g


def ring(c, color=BLUE, k=1.62):
    return Circle(radius=c.soma.width/2*k, color=color, stroke_width=4).move_to(c)


def state(c, col, opacity=.8):
    return c.animate.set_color(col).set_fill(col, opacity)



# Exact word onset, without the shared helper's anticipatory 0.2-second lead.
class TimedScene(SpokenScene):
    def at(self, phrase, lead=0, nth=0):
        target = self.t_of(phrase, nth)
        remaining = target - self.elapsed()
        if remaining > .001:
            self.wait(remaining)


def label(s, x, y, size=28, color=TEXT):
    return T(s, size, color, should_center=True).move_to([x,y,0])


def heading(s,color=TEXT):
    return label(s,0,3.15,32,color)


def cells_at(x=2.9,y=.3):
    # Three tagged cells among eight untagged background cells.
    selected=[(-1,.5),(.45,1),(.8,-.8)]
    background=[(-2,1.3),(-.8,1.8),(1.8,1.4),(-2.1,-.3),(-1.4,-1.5),(-.2,-1.4),(1.9,-.2),(1.6,-1.5)]
    return VGroup(*[cell((x+dx,y+dy),.3) for dx,dy in selected+background])


def brain():
    return RoundedRectangle(width=6.3,height=5.6,corner_radius=1.2,color=GREY).move_to([2.9,.25,0])


def mouse(x=-3.7,y=-.3):
    body=Ellipse(width=1.7,height=.9,color=GREY,fill_color=GREY,fill_opacity=.3)
    head=Circle(radius=.38,color=GREY,fill_color=GREY,fill_opacity=.3).move_to([.8,.22,0])
    ear=Circle(radius=.2,color=GREY).move_to([.67,.58,0])
    eye=Dot([.99,.29,0],radius=.045,color=TEXT)
    tail=Line([-.8,0,0],[-1.5,.35,0],color=GREY)
    legs=VGroup(Line([-.45,-.3,0],[-.65,-.65,0],color=GREY),Line([.4,-.3,0],[.6,-.65,0],color=GREY))
    return VGroup(body,head,ear,eye,tail,legs).move_to([x,y,0])


def setup_mouse(text=''):
    box=RoundedRectangle(width=4.8,height=5.6,corner_radius=.2,color=GREY).move_to([-3.7,.25,0])
    b=VGroup(box)
    if text:b.add(label(text,-3.7,2.3,26))
    return b,mouse(),brain(),cells_at()


def light(x=2.9,y=2.7):
    return VGroup(Arrow([x,y,0],[x,y-.9,0],color=BLUE,buff=0,stroke_width=7),label('light',x+1,y-.15,26,BLUE))


def tag_group(cs):
    return VGroup(*[ring(c,GREEN,1.45) for c in cs[:3]])


def ladder(question=False,conditional=False):
    rails=VGroup(Line([-5.7,-1.6,0],[-5.7,2.4,0],color=GREY),Line([5.7,-1.6,0],[5.7,2.4,0],color=GREY),Line([-5.7,-1.25,0],[5.7,-1.25,0],color=GREY),Line([-5.7,1.5,0],[5.7,1.5,0],color=GREY))
    corr=chip('correlation',YELLOW,30).move_to([0,-1.25,0])
    suf=chip('sufficiency',GREEN,32).move_to([-3,1.5,0])
    nec=chip('necessity',TEAL if conditional else GREY,32).move_to([3,1.5,0])
    for c in (corr,suf,nec):c[0].set_fill(BG,1)
    g=VGroup(rails,corr,suf,nec,label('in this preparation',-3,.65,26,GREEN))
    if conditional:
        g.add(label('day 12, prefrontal, mice',3,.65,26,TEAL),label('natural recall in other regions: untested',0,-2.35,27,TEXT))
    if question:
        nec[0].stretch_to_fit_height(1.5).move_to([3,1.9,0])
        q=label('?',3,2.3,46,GOLD)
        needed=label('Needed?',3,.05,34,GOLD)
        outline=SurroundingRectangle(VGroup(nec,q),color=GOLD,buff=.16,corner_radius=.12)
        g.add(q,needed,outline)
        g.pulse=outline
    return g


def pulse(scene,obj,seconds):
    scene.play(obj.animate.set_stroke(opacity=.25),run_time=seconds/2,rate_func=smooth)
    scene.play(obj.animate.set_stroke(opacity=1),run_time=seconds/2,rate_func=smooth)


def timeline(y=-1.8):
    g=VGroup(Arrow([-5.7,y,0],[5.7,y,0],color=GREY,buff=0))
    for x,lab in [(-4.7,'learning'),(0,'day 2'),(4.7,'day 12')]:
        g.add(Line([x,y+.15,0],[x,y-.15,0],color=GREY),label(lab,x,y-.65))
    return g


def bar(x,h,col,base=-1.65,w=.7):
    return Rectangle(width=w,height=h,stroke_color=col,fill_color=col,fill_opacity=.75).move_to([x,base+h/2,0])


def result_chart():
    # Ordinal schematic heights encode only the comparisons in the narration.
    # No numerical percentages or data traces are implied.
    axis=VGroup(Arrow([-.8,-2,0],[-.8,2.5,0],color=GREY,buff=0),Line([-.8,-2,0],[6.1,-2,0],color=GREY))
    axis.add(label('time spent freezing',2.75,3.25,28),label('relative, schematic',2.75,2.75,26,TEXT),label('low',-1.25,-1.9,26,TEXT),label('high',-1.25,2.4,26,TEXT))
    names=[('off',.85,GREY),('on',2.2,YELLOW)]
    for name,x,col in names:axis.add(label(name,x,-2.45,26,col))
    axis.add(label('light',1.5,-3,26,BLUE))
    return axis


def assay_stage(text):
    box=RoundedRectangle(width=5.5,height=5.2,corner_radius=.2,color=GREY).move_to([-3.6,-.1,0])
    m=mouse(-3.7,-1.2)
    cs=VGroup(*[cell((x,y),.23) for x,y in [(-4.8,1),(-3.5,1.4),(-2.1,.9),(-5.5,.35),(-4.8,1.9),(-2.6,1.9),(-1.5,.2),(-2.7,.25),(-4.4,.2)]])
    stage=VGroup(box,*([label(text,-3.6,-2.3,26)] if text else []))
    VGroup(stage,m,cs).scale(.8,about_point=np.array([-3.6,-.1,0])).shift(LEFT*.5)
    return stage,m,cs


def reference_bars():
    return VGroup(bar(.85,.5,GREY,base=-2),bar(2.2,4.5,YELLOW,base=-2))


def spines(c,n,length):
    p=c.get_center(); r=c.soma.width/2
    return VGroup(*[Line(p+np.array([np.cos(a),np.sin(a),0])*r,p+np.array([np.cos(a),np.sin(a),0])*(r+length),color=GREEN,stroke_width=3) for a in np.linspace(0,2*PI,n,endpoint=False)])


def region_graph():
    # Separate named compartments: a conceptual network, not an anatomical map.
    pts=[(-3.7,1.2),(3.7,1.2),(-3.7,-1.45),(3.7,-1.45)]
    names=['hippocampus','prefrontal cortex','other regions','other regions']
    nodes=VGroup(*[cell(p,.5) for p in pts])
    panels=VGroup(*[RoundedRectangle(width=5.3,height=2.2,corner_radius=.45,color=GREY).move_to([x,y,0]) for x,y in pts])
    names=VGroup(*[label(n,x,y+.87,27) for n,(x,y) in zip(names,pts)])
    edges=VGroup(Line([-1.05,1.2,0],[1.05,1.2,0],color=GREY),Line([-3.7,.1,0],[-3.7,-.35,0],color=GREY),Line([3.7,.1,0],[3.7,-.35,0],color=GREY),Line([-1.05,-1.45,0],[1.05,-1.45,0],color=GREY))
    return panels,edges,nodes,names


def takeaway():
    return VGroup(label('Sufficiency does not prove necessity.',0,.9,36),label('Ask which control each claim needs.',0,-.65,36,GOLD))


class S00Title(TitleCard):
    LESSON='Plasticity, Networks and Consolidation'
    TITLE='Enough Does Not Prove Needed'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),VGroup(T('Enough Does Not',52,font=TITLE_FONT),T('Prove Needed',52,font=TITLE_FONT)).arrange(DOWN,buff=.12),Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.45)
        self.play(FadeIn(g),run_time=.5)
        self.finish()


class S01(TimedScene):
    def construct(self):
        b,m,br,cs=setup_mouse()
        self.add(b,m,br,cs)
        self.at('Shine light')
        self.play(FadeIn(light()),run_time=.4)
        self.at('certain cells')
        self.play(*[state(c,YELLOW) for c in cs[:3]],run_time=.4)
        self.at('it freezes')
        self.play(m.animate.set_color(YELLOW),FadeIn(label('freezing',-3.7,-1.6,30,YELLOW)),run_time=.35)
        self.at('Has the memory')
        self.play(FadeIn(label('Has the memory been found?',0,-3.15,34,GOLD)),run_time=.35)
        self.finish()


class S02(TimedScene):
    def construct(self):
        b,m,br,cs=setup_mouse('conditioning chamber')
        self.add(b,m,br,cs,label('dentate gyrus',2.9,2.55,28))
        self.at('cells were tagged')
        self.play(Create(tag_group(cs)),run_time=.5)
        self.at('learned to fear')
        zap=VMobject(color=RED,stroke_width=7).set_points_as_corners([[-4.6,-1.5,0],[-4.1,-.9,0],[-4.45,-.9,0],[-3.95,-.35,0]])
        self.play(Create(zap),m.animate.shift(RIGHT*.35),FadeIn(label('shock',-4.2,-2.1,28,RED)),run_time=.45)
        self.finish()


class S03(TimedScene):
    def construct(self):
        c=cell((0,-.15),2.6)
        gene=chip('c-fos',GREY,38).move_to([0,-.15,0])
        self.add(c)
        self.at('A gene called')
        self.play(Indicate(c,color=YELLOW,scale_factor=1.03),run_time=.6)
        self.play(FadeIn(gene),run_time=.3)
        self.at('switches on')
        self.play(gene.animate.set_color(YELLOW),FadeIn(label('ON',0,-1.1,36,YELLOW)),run_time=.5)
        self.at('recently active neurons')
        self.play(FadeIn(heading('recently active neuron',YELLOW)),run_time=.3)
        self.finish()


class S04(TimedScene):
    def construct(self):
        c=cell((0,0),2.5)
        promoter=chip('c-fos promoter',YELLOW,26).move_to([-1,0,0])
        gene=chip('gene',GREY,28).move_to([1.6,0,0])
        link=Arrow(promoter.get_right(),gene.get_left(),color=YELLOW,buff=.06,stroke_width=3,max_tip_length_to_length_ratio=.3)
        channel=RoundedRectangle(width=.6,height=1.25,corner_radius=.1,color=BLUE,fill_color=BLUE,fill_opacity=.4).move_to([2.3,-1,0])
        self.add(c)
        self.at('Its promoter')
        self.play(FadeIn(promoter),FadeIn(gene),GrowArrow(link),run_time=.5)
        self.at('light driven channel')
        path=Arrow([1.6,-.45,0],[2.05,-.85,0],color=BLUE,buff=.08)
        self.play(GrowArrow(path),FadeIn(channel),run_time=.55)
        self.at('channel rhodopsin 2')
        name=label('channelrhodopsin-2',3.9,1.55,30,BLUE)
        leader=Line([1.15,-.7,0],[2.5,1.15,0],color=BLUE)
        self.play(VGroup(c,promoter,gene,link,path,channel).animate.shift(LEFT*1.5),FadeIn(name),Create(leader),FadeIn(label('light-driven',3.9,.3,28,BLUE)),FadeIn(label('excites the cell',3.9,-.4,28,BLUE)),run_time=.4)
        self.finish()


class S05(TimedScene):
    def construct(self):
        frame=Rectangle(width=8,height=4.8,color=GREY).move_to([0,.2,0])
        shutter=Rectangle(width=7.8,height=4.6,color=RED,fill_color=RED,fill_opacity=.08).move_to([0,.2,0])
        cs=VGroup(cell((-1.8,-.1),.8),cell((1.8,-.1),.8))
        tags=tag_group(cs)
        closed=label('doxycycline on: window closed',0,2.95,30,RED)
        opened=label('doxycycline off: window open',0,2.95,30,GREEN)
        self.add(frame,cs,shutter)
        self.at('A drug')
        self.play(FadeIn(closed),run_time=.4)
        self.at('blocks the tag')
        self.play(Indicate(shutter,color=RED,scale_factor=1.02),run_time=.5)
        self.at('Take it away')
        self.play(FadeOut(closed),run_time=.3)
        self.at('a window opens')
        self.play(shutter.animate.stretch(.025,0).move_to([-3.9,.2,0]),FadeIn(opened),*[state(c,YELLOW) for c in cs],Create(tags),run_time=.6)
        self.at('Give it back')
        self.at('the window closes')
        self.play(FadeOut(opened),shutter.animate.stretch(40,0).move_to([0,.2,0]),FadeIn(closed),*[state(c,GREY,.25) for c in cs],run_time=.55)
        self.add(label('tags restricted to the open window',0,-2.65,28,GREEN))
        self.finish()


class S06(TimedScene):
    def construct(self):
        axis=Arrow([-5.9,-1.95,0],[5.9,-1.95,0],color=GREY,buff=0)
        win=Rectangle(width=6.5,height=4.5,color=GREEN,fill_color=GREEN,fill_opacity=.06).move_to([0,.3,0])
        cs=VGroup(cell((-1.6,.7),.55),cell((0,1),.55),cell((1.7,.6),.55),cell((2.6,-.9),.35),cell((-4.6,.3),.5),cell((4.6,.3),.5))
        self.add(axis,cs,label('doxycycline on',-4.65,-2.65,26,RED),label('doxycycline on',4.65,-2.65,26,RED))
        self.at('Open it around training')
        self.play(Create(win),FadeIn(label('doxycycline off: window open',0,3.05,30,GREEN)),FadeIn(label('training',0,-2.65,28)),run_time=.6)
        self.add(label('off 1–2 days before training',0,2.3,26,TEXT))
        self.at('mostly cells active')
        self.play(*[state(c,YELLOW) for c in cs[:3]],run_time=.4)
        self.at('get the channel')
        self.play(Create(tag_group(cs)),Create(ring(cs[3],GREEN,1.45)),FadeIn(label('some background labelling',-.5,-.95,26,TEXT)),Create(Line([1.85,-.95,0],[2.12,-.9,0],color=TEXT)),run_time=.5)
        self.finish()


class S07(TimedScene):
    def construct(self):
        b,m,cs=assay_stage('')
        self.add(b,m,cs,tag_group(cs),result_chart())
        self.at('Days later')
        self.play(FadeIn(label('Liu and colleagues, 2012',-4.1,3.15,28)),run_time=.35)
        self.at('in a different box')
        self.play(FadeIn(label('different box',-4.1,-2.7,26)),run_time=.3)
        self.at('light on the cells')
        self.play(FadeIn(light(-4.1,2.4)),*[state(c,YELLOW) for c in cs[:3]],run_time=.4)
        self.at('mice freeze')
        self.play(m.animate.set_color(YELLOW),*[GrowFromEdge(b,DOWN) for b in reference_bars()],run_time=.45)
        self.finish()


class S08(TimedScene):
    def construct(self):
        b,m,cs=assay_stage('')
        # The comparison stays across the two control scenes.
        self.add(b,m,cs,result_chart(),reference_bars())
        self.at('Two controls')
        self.play(FadeIn(label('Control 1',-4.1,3.15,30,PURPLE)),FadeIn(label('light-on controls',4.45,-3,26,PURPLE)),run_time=.35)
        self.at('tagged in a neutral box')
        self.play(Create(tag_group(cs)),FadeIn(label('neutral box · no shock',-4.1,-2.7,26)),FadeIn(label('neutral',3.65,-2.45,26,PURPLE)),run_time=.45)
        self.at('caused no fear freezing')
        self.play(FadeIn(light(-4.1,2.4)),*[state(c,YELLOW) for c in cs[:3]],m.animate.shift(RIGHT*.35),GrowFromEdge(bar(3.65,.5,PURPLE,base=-2),DOWN),run_time=.5)
        self.finish()


class S09(TimedScene):
    def construct(self):
        b,m,cs=assay_stage('')
        self.add(b,m,cs,result_chart(),reference_bars(),bar(3.65,.5,PURPLE,base=-2),label('neutral',3.65,-2.45,26,PURPLE),label('light-on controls',4.45,-3,26,PURPLE),label('Control 2',-4.1,3.15,30,PURPLE))
        self.at('with a fluorescent protein')
        self.play(*[state(c,GREEN,.35) for c in cs[:3]],FadeIn(label('fluorescent-protein control',-4.1,-2.7,26)),run_time=.45)
        self.at('but no channel')
        self.play(FadeIn(label('no channel',-4.1,-.2,28,PURPLE)),FadeIn(label('no ChR2',5.2,-2.45,26,PURPLE)),run_time=.35)
        self.at('did not freeze')
        # Without ChR2, light does NOT drive these cells to fire.
        self.play(FadeIn(light(-4.1,2.4)),m.animate.shift(RIGHT*.35),GrowFromEdge(bar(5.2,.5,PURPLE,base=-2),DOWN),run_time=.5)
        self.finish()


class S10(TimedScene):
    def construct(self):
        g=ladder();g[2][1].set_opacity(.25);g[4].set_opacity(0)
        self.add(g)
        self.at('enough to drive')
        self.play(g[2][1].animate.set_opacity(1),run_time=.4)
        self.at('in this preparation')
        self.play(g[4].animate.set_opacity(1),run_time=.4)
        self.at('That is sufficiency')
        self.play(Indicate(g[2],color=GREEN,scale_factor=1.05),run_time=.5)
        self.finish()


class S11(TimedScene):
    def construct(self):
        g=ladder();self.add(g)
        self.at('needs these cells')
        q=ladder(True)
        self.remove(g);self.add(q)
        pulse(self,q.pulse,2.4)
        self.finish()


class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=ladder(True);self.add(g)
        pulse(self,g.pulse,5)


class S13(TimedScene):
    def construct(self):
        g=ladder(True);self.add(g)
        self.at('Not yet')
        self.play(Indicate(g.pulse,color=GOLD,scale_factor=1.03),run_time=.4)
        self.at('Necessity needs the reverse')
        self.play(FadeOut(g),run_time=.4)
        b,m,br,cs=setup_mouse()
        self.play(FadeIn(VGroup(b,m,br,cs,tag_group(cs))),run_time=.4)
        self.at('Silence the tagged cells')
        self.play(*[state(c,RED,.15) for c in cs[:3]],FadeIn(label('inhibitory opsin',0,3.5,30,RED)),run_time=.5)
        self.at('during natural recall')
        self.play(FadeIn(label('natural recall',2.9,-2.1,28)),run_time=.4)
        self.at('shock box')
        self.play(FadeIn(label('shock box',-3.7,2.3,28)),run_time=.3)
        self.finish()


class S14(TimedScene):
    def construct(self):
        br=RoundedRectangle(width=10.8,height=5.35,corner_radius=1,color=GREY).move_to([0,-.15,0])
        cs=VGroup(cell((-3,.1),.65),cell((0,.1),.65),cell((3,.1),.65))
        self.add(br,cs)
        self.at('Kitamura and colleagues')
        self.play(FadeIn(heading('Kitamura and colleagues, 2017')),run_time=.4)
        self.at('tagged prefrontal cells')
        self.play(Create(tag_group(cs)),FadeIn(label('prefrontal cortex',0,1.75,30)),run_time=.5)
        self.at('at learning')
        self.play(FadeIn(label('tagged at learning',0,-1.65,30,GREEN)),run_time=.35)
        self.at('silenced them later')
        self.play(*[state(c,RED,.15) for c in cs],run_time=.5)
        self.finish()


class S15(TimedScene):
    def construct(self):
        self.add(label('Prefrontal silencing at recall',0,3.45,32))
        axis=VGroup(Arrow([-5.25,-1.9,0],[-5.25,2.3,0],color=GREY,buff=0),Line([-5.25,-1.9,0],[5.9,-1.9,0],color=GREY))
        axis.add(label('time spent freezing',-3.35,2.85,28),label('relative, schematic',3.7,2.85,26,TEXT),label('low',-5.8,-1.8,26,TEXT),label('high',-5.8,1.6,26,TEXT))
        self.add(axis)
        def pair(x,low=False):
            return VGroup(bar(x-.65,3.5,GREY,base=-1.9),bar(x+.65,.65 if low else 3.5,RED,base=-1.9),label('light off',x-.75,-2.25,26),label('light on',x+.75,-2.25,26,RED))
        self.at('On day two')
        a=pair(-2.8)
        self.play(FadeIn(a),FadeIn(label('Day 2',-2.8,2.15,30)),run_time=.55)
        self.at('recall was intact')
        self.play(FadeIn(label('intact',-2.8,-3,30,TEAL)),run_time=.35)
        self.at('On day twelve')
        self.play(FadeIn(pair(3.4,True)),FadeIn(label('Day 12',3.4,2.15,30)),run_time=.55)
        self.at('it was disrupted')
        self.play(FadeIn(label('disrupted',3.4,-3,30,RED)),run_time=.35)
        self.finish()


class S16(TimedScene):
    def construct(self):
        cs=VGroup(*[cell((x,.6),.8) for x in (-4.7,0,4.7)])
        self.add(timeline(),cs,label('prefrontal cells',0,2.2,28,GREEN))
        self.at('The standard model')
        self.play(FadeIn(heading('The standard model predicted this order')),run_time=.4)
        # Day numbers are not spoken in this final narration; reveal its prediction
        # at "predicted that order" rather than inventing non-existent word cues.
        self.at('predicted that order')
        self.play(FadeIn(label('not needed',0,-.85,30,TEAL)),FadeIn(label('needed',4.7,-.85,30,RED)),run_time=.45)
        self.at('But these cells')
        self.play(Create(tag_group(cs)),run_time=.4)
        self.at('tagged at learning')
        badge=chip('tag',GREEN,30).move_to([-4.7,-.85,0])
        self.play(FadeIn(badge),Indicate(cs[0],color=GREEN,scale_factor=1.12),run_time=.65)
        self.finish()


class S17(TimedScene):
    def construct(self):
        claim=label('Cortical ensemble first appears much later',0,3.1,30)
        cs=VGroup(*[cell((x,.65),.55) for x in (-4.7,0,4.7)])
        self.add(timeline(),claim,cs,tag_group(cs),label('prefrontal cells',0,2.1,28,GREEN))
        hip=cell((-1.65,-3.15),.28)
        hip_label=label('hippocampus',.25,-3.15,27,TEXT)
        hip_box=RoundedRectangle(width=4.6,height=.95,corner_radius=.15,color=GREY).move_to([-.25,-3.15,0])
        self.add(hip_box,hip,hip_label)
        self.at('did not first appear')
        self.play(Create(Line(claim.get_left()+LEFT*.1,claim.get_right()+RIGHT*.1,color=RED,stroke_width=5)),run_time=.5)
        self.at('It formed at once')
        self.play(Indicate(cs[0],color=GREEN,scale_factor=1.1),Create(spines(cs[0],4,.13)),run_time=.45)
        self.at('and matured')
        self.play(Create(spines(cs[1],8,.23)),Create(spines(cs[2],16,.4)),FadeIn(label('more spines',4.7,-.85,28,GREEN)),run_time=.55)
        self.wait(1.8)
        self.finish()


class S18(TimedScene):
    def construct(self):
        left=RoundedRectangle(width=5.4,height=5.6,corner_radius=.7,color=GREY).move_to([-3.2,.1,0])
        right=left.copy().move_to([3.2,.1,0])
        pfc=VGroup(cell((-4.2,.3),.55),cell((-2.2,.3),.55))
        dg=VGroup(cell((2.2,.3),.55),cell((4.2,.3),.55))
        for c in dg:c.set_color(YELLOW)
        self.add(left,right,pfc,dg,tag_group(pfc),tag_group(dg),label('prefrontal cortex',-3.2,2.1,30),label('hippocampus',3.2,2.1,30),label('dentate engram cells',3.2,-1.25,28))
        self.at('not fixed in one place')
        self.play(Create(Line([-1.3,.3,0],[1.3,.3,0],color=GREEN,stroke_width=4)),run_time=.5)
        self.at('depends on when')
        self.play(*[state(c,YELLOW) for c in pfc],*[state(c,GREY,.12) for c in dg],run_time=.9)
        self.finish()


class S19(TimedScene):
    def construct(self):
        panels,edges,cs,names=region_graph()
        self.add(panels,edges,cs,label('a few of many regions · schematic',0,-3.2,26,TEXT))
        self.at('the group spans regions')
        self.play(FadeIn(names),edges.animate.set_color(GREEN),run_time=.5)
        self.at('driving one part')
        self.play(FadeIn(light(-3.7,3.15)),state(cs[0],YELLOW),run_time=.4)
        self.at('can complete it')
        self.play(*[state(c,YELLOW) for c in cs[1:]],run_time=.5)
        self.finish()


class S20(TimedScene):
    def construct(self):
        panels,edges,cs,names=region_graph()
        for c in cs:c.set_color(YELLOW)
        edges.set_color(GREEN)
        self.add(panels,edges,cs,names,label('a few of many regions · schematic',0,3.15,26,TEXT))
        self.at('Silencing one part')
        self.play(state(cs[0],RED,.1),edges[0].animate.set_color(GREY),edges[1].animate.set_color(GREY),FadeIn(label('an interpretation, from the model',0,-3.15,28,GOLD)),run_time=.6)
        self.at('enough of the rest')
        self.play(Indicate(VGroup(*cs[1:]),color=YELLOW,scale_factor=1.08),run_time=.55)
        self.at('to complete it')
        self.play(edges[2:].animate.set_color(YELLOW),run_time=.4)
        self.finish()


class S21(TimedScene):
    def construct(self):
        g=ladder(conditional=True);self.add(g)
        self.at('mouse fear')
        self.play(FadeIn(label('mice · contextual fear',0,3.15,30)),run_time=.35)
        self.at('days to weeks')
        self.add(label('days to weeks',0,-3.15,28,TEXT))
        self.at('not yet human memory')
        self.play(FadeIn(label('Human memory over years?',0,-.35,34,GOLD)),run_time=.45)
        self.finish()


class S22(TimedScene):
    def construct(self):
        card=takeaway()
        self.add(card[0])
        self.at('Enough does not')
        self.play(Indicate(card[0],color=TEXT,scale_factor=1.02),run_time=.4)
        self.at('ask which control')
        self.play(FadeIn(card[1]),run_time=.45)
        self.finish()


class S23End(EndCard):
    LINE='Sufficiency does not prove necessity. Ask which control each claim needs.'
    def construct(self):
        self.add(takeaway())
        self.finish()
