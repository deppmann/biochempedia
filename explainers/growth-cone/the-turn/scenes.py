"""A Small Difference, a Turn: reviewed animation rebuild.
COLOR MAP: BLUE cone/actin; TEAL actin addition; RED flow/loss/repellent;
YELLOW clutch; GREEN advance/protein; PURPLE microtubules; ORANGE cue;
OUTLINE/GREY axon, apparatus. Actin retains the series BLUE (not red).
All turning trajectories integrate dtheta/dt=.3(vL-vR),
dposition/dt=(vL+vR)/2*(cos(theta),sin(theta)); no measured data implied.
"""
import importlib.util
from pathlib import Path
import numpy as np
from bp_style import *
_spec=importlib.util.spec_from_file_location('growth_reference',Path(__file__).resolve().parent.parent/'scenes.old.py')
_ref=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_ref)
P, fan_at, pipette, cloud=_ref.P,_ref.fan_at,_ref.pipette,_ref.cloud
PURPLE,ORANGE,OUTLINE=_ref.PURPLE,_ref.ORANGE,_ref.OUTLINE

# Caption rails use >=38 pt (about 26 px at the 960-pixel review scale).
def tag(s,x=0,y=3.48,color=TEXT,size=36):
    label=T(s,size=max(38,size),color=color)
    if label.width>12.7:
        label.scale_to_fit_width(12.7)
    return label.move_to(P(x,y))

def path(points,width=22,color=OUTLINE):
    return VMobject(stroke_color=color,stroke_width=width,stroke_opacity=.85).set_points_as_corners(points)

def integrate(vl=.65,vr=.35,seconds=4,start=(-3.6,-.2),theta=0):
    p=P(*start); pts=[p.copy()]; th=theta
    for _ in range(round(seconds/.025)):
        th+=.3*(vl-vr)*.025
        p=p+(vl+vr)/2*P(np.cos(th),np.sin(th))*.025
        pts.append(p.copy())
    return pts,th

# Explicit origin anchoring avoids Manim's bounding-box pivot shifting the neck.
def fan_at(x=0,y=0,theta=0,scale=1,actin=True,tubules=False):
    fan=_ref.fan_at(0,0,0,1,actin,tubules)
    fan[0].set_fill(BLUE,opacity=.23)
    if scale>=2:
        # Keep the enlarged fan inside its caption rails; short filopodia
        # remain distinct from the broad lamellipodial body.
        for line in fan[1]:
            start=line.get_start()
            line.put_start_and_end_on(start,start*1.10)
    return fan.scale(scale,about_point=ORIGIN).rotate(theta,about_point=ORIGIN).shift(P(x,y))

NECK=P(-3.6,-.2)

def stage(tubes=False,scale=2.3):
    fan=fan_at(NECK[0]+1.5*scale,NECK[1],scale=scale,tubules=tubes)
    fan.stretch(.96,1,about_point=NECK)
    return VGroup(path([P(-6.1,-.2),NECK]),fan)

def source(drug=False):
    col=PURPLE if drug else ORANGE
    return VGroup(cloud(4.25,1.5,col),pipette(4.25,1.5,col))

def turned_stage(direction=1,scale=1.9,tubes=True,withdrawn=False,isolated=False):
    # Integrate the NECK, not the fan centre. Thus the entire shaft tangent
    # points in the cone's direction and its last point IS the cone base.
    scale=min(scale,1.35) if direction<0 else scale
    pts,th=integrate(1.25 if direction>0 else .25,.25 if direction>0 else 1.25,1.5)
    c=pts[-1]+1.5*scale*P(np.cos(th),np.sin(th))
    fan=fan_at(c[0],c[1],th,scale,tubules=tubes)
    if withdrawn and tubes:
        fan[2][-1].scale(.12,about_point=fan[2][-1].get_start()).set_opacity(.15)
    trail=path(([P(-4.5,-.2)] if isolated else [P(-6.1,-.2)])+pts)
    group=VGroup(trail,fan)
    if group.get_top()[1]>2.9:
        group.shift(DOWN*(group.get_top()[1]-2.9))
    if group.get_bottom()[1]<-2.9:
        group.shift(UP*(-2.9-group.get_bottom()[1]))
    if isolated:
        group.shift(DOWN*group.get_center()[1])
    return group

def turn(scene,obj,direction=1,duration=1.25,scale=1.9,withdrawn=False,isolated=False):
    scene.play(Transform(obj,turned_stage(direction,scale,len(obj[1])>2,withdrawn,isolated)),run_time=duration)

def near_tubes():
    return VGroup(*[Line(NECK+P(.1,j*.12),P(.35-j*.23,.5+j*.37),color=PURPLE,stroke_width=7) for j in range(3)])

def mesh():
    # A network cartoon, not a molecular structure.
    g=VGroup()
    for y in np.linspace(.45,1.55,5):
        g.add(Line(P(-.2,y),P(1.05-.35*(y-.45),y+.32),color=BLUE,stroke_width=4))
    for x in np.linspace(-.15,.75,5):
        g.add(Line(P(x,.5),P(x-.4,1.65),color=BLUE,stroke_width=4))
    return g

def sheet():
    return Polygon(P(-.65,1),P(-.2,2.25),P(.35,2.05),P(.9,1.55),P(1.25,.95),
                   color=BLUE,fill_opacity=.78,stroke_width=4)

def question_frame():
    o=stage(True); o[1][2][-1].set_stroke(width=10)
    return VGroup(o,source(True),tag('Microtubules stabilized on one side',color=PURPLE,size=34),
                  tag('No guidance cue  •  Which way does it turn?',y=-3.46,size=34))

# The bars are placed beside their corresponding half and linked to that half.
# All widths are rates in arbitrary units: gain = addition - retrograde flow.
def gain_stack(x,y,name,added=.30,flow=.20):
    g=VGroup(tag(name,x,y+1.0,size=34))
    for dy,txt,v,col in [( .45,'Added',added,TEAL),(-.12,'Slides back',flow,RED),(-.69,'Gain',added-flow,GREEN)]:
        lab=tag(txt,x-.8,y+dy,col,30)
        bar=Rectangle(width=max(.02,v*4.2),height=.22,color=col,fill_opacity=.85).move_to(P(x+.75+v*2.1,y+dy))
        g.add(VGroup(lab,bar))
    g.add(Line(P(x+.64,y-.4),P(x+2.01,y-.4),color=GREY,stroke_width=2),tag('−',x+.5,y-.12,size=30),tag('=',x+.5,y-.69,size=30))
    return g

def gain_scene(near=.30,flow=.14):
    return VGroup(gain_stack(3.9,1.25,'Near side',near,flow),gain_stack(3.9,-1.55,'Far side'))

def hist_data(mean=22):
    # Deterministic ensemble of 49 model growth cones, equal sample weights.
    angles=[]; traces=VGroup(); ends=[]
    for z in np.linspace(-2.4,2.4,49):
        bias=np.deg2rad(mean+13*z)/(.3*4)
        pts,th=integrate(.5+bias/2,.5-bias/2,4,start=(-4.8,-.4))
        pts=[P(-4.8,-.4)+(p-P(-4.8,-.4))*3 for p in pts]
        traces.add(path(pts,4,GREEN)); angles.append(np.rad2deg(th)); ends.append(pts[-1])
    counts,bins=np.histogram(angles,bins=np.arange(-60,81,10))
    bars=VGroup()
    for i,n in enumerate(counts):
        h=max(.015,n*.48)
        bars.add(Rectangle(width=.64,height=h,stroke_width=1,color=GREEN,fill_opacity=.75).move_to(P(-5.1+(i+.5)*.75,-2.15+h/2)))
    return traces,bars,angles

def hist_axes():
    axes=VGroup(Line(P(-5.1,-2.15),P(5.5,-2.15),color=GREY),Line(P(-5.1,-2.15),P(-5.1,2.8),color=GREY),
        DashedLine(P(-.6,-2.15),P(-.6,2.8),color=GREY),tag('Turning angle (degrees)',y=-3.43,size=32),
        tag('away',-3,-2.91,size=32),tag('toward pipette',2.5,-2.91,size=32),
        tag('Schematic model • not measured data',y=3.46,size=32))
    for a in [-60,-30,0,30,60,80]:
        axes.add(tag(f'{a:+d}' if a else '0',-5.1+(a+60)*.075,-2.5,size=30))
    for n in [0,5,10]:
        axes.add(tag(str(n),-5.5,-2.15+n*.48,size=30))
    axes.add(tag('Number of growth cones',-6.22,.3,size=32).rotate(PI/2))
    return axes

class S00Title(TitleCard):
    LESSON='The Growth Cone: The Tip That Steers the Axon'
    TITLE='A Small Difference, a Turn'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',size=30,color=TEAL),T(self.LESSON,size=30,color=GREY),T(self.TITLE,size=46,font=TITLE_FONT),Line(LEFT*1.2,RIGHT*1.2,color=GOLD)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.45); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        o=stage().shift(UP*.20)
        center=NECK+P(1.5*2.3,0)
        arc=[center+1.5*2.3*P(np.cos(a),.96*np.sin(a)) for a in np.linspace(1,0,24)]
        shade=Polygon(NECK,*arc,color=ORANGE,fill_opacity=.44,stroke_width=0).shift(UP*.20)
        caption=VGroup(T('How does a cue only 5 to 10% stronger on one side',size=38),
                       T('turn a whole axon?',size=38)).arrange(DOWN,buff=.10).move_to(P(0,-3.36))
        self.add(o,shade,source(),caption)
        self.at('cue only',lead=0)
        lab=tag('Near side: 5 to 10% more cue',y=3.46,color=ORANGE,size=40)
        self.play(FadeIn(lab),run_time=.4)
        self.finish()

class S02Gb(SpokenScene):
    def construct(self):
        # Dish occupies a clear margin; labels use rails outside its rim.
        self.add(Ellipse(width=12.8,height=6.2,color=GREY,stroke_opacity=.45),stage())
        self.at('in',lead=0); self.play(FadeIn(tag('Gundersen and Barrett • 1979',size=34)),run_time=.35)
        self.at('placed a pipette',lead=0); self.play(FadeIn(source()),run_time=.4)
        self.at('nerve growth factor',lead=0); ngf=VGroup(tag('Nerve growth',4.9,-.55,ORANGE,38),tag('factor (NGF)',4.9,-1.2,ORANGE,38)); self.play(FadeIn(ngf),run_time=.35)
        self.at('chick sensory axons',lead=0); self.play(FadeIn(tag('Chick sensory axons',y=-3.46,size=34)),run_time=.35); self.finish()

class S03Turned(SpokenScene):
    def construct(self):
        o=stage(); self.add(o,source(),tag('Turning toward the NGF source',y=-3.46,size=34))
        clock=VGroup(Circle(.44,color=TEXT).move_to(P(-4.9,2.3)),Line(P(-4.9,2.3),P(-4.9,2.65),color=TEXT),Line(P(-4.9,2.3),P(-4.6,2.3),color=ORANGE))
        self.at('within about',lead=0); self.play(Create(clock),FadeIn(tag('About 20 minutes',y=3.48,size=36)),run_time=.4)
        self.at('turn toward',lead=0); self.play(Rotate(clock[-1],angle=TAU,about_point=P(-4.9,2.3)),Transform(o,turned_stage(tubes=False)),run_time=1.5); self.wait(2); self.finish()

class S04Hist(SpokenScene):
    def construct(self):
        traces,bars,angles=hist_data(); heading=tag('One growth cone wanders',size=36)
        single=fan_at(*traces[24].get_end()[:2],theta=np.deg2rad(22),scale=.95)
        self.add(traces[24],single,heading)
        self.at('so the evidence',lead=0); self.play(FadeOut(single),LaggedStart(*[Create(traces[i]) for i in range(0,49,4)],lag_ratio=.04),run_time=.9)
        self.at('spread of turning angles',lead=0)
        axes=hist_axes(); self.play(FadeOut(heading),FadeIn(axes),traces.animate.set_stroke(opacity=.18),run_time=.35)
        dots=VGroup(*[Dot(traces[i].get_end(),radius=.065,color=GREEN) for i in range(0,49,4)])
        self.add(dots)
        self.at('across many cones',lead=0)
        moves=[]
        for dot,i in zip(dots,range(0,49,4)):
            k=int(np.clip((angles[i]+60)//10,0,13)); moves.append(dot.animate.move_to(bars[k].get_top()))
        self.play(*moves,FadeIn(bars),FadeOut(traces),run_time=1.0); self.play(FadeOut(dots),run_time=.2); self.wait(1.2); self.finish()

class S05Control(SpokenScene):
    def construct(self):
        _,gradient,_=hist_data(); _,control,_=hist_data(0); control.set_color(BLUE)
        self.add(hist_axes(),gradient)
        title=tag('Uniform bath control',.8,2.75,BLUE,34)
        self.at('in a control',lead=0); self.play(gradient.animate.set_fill(opacity=.12).set_stroke(opacity=.6),FadeIn(title),run_time=.4)
        self.at('uniform bath',lead=0); self.play(FadeIn(control),run_time=.65)
        self.at('centers on zero',lead=0); self.play(Indicate(control[6],color=TEXT),run_time=.6)
        self.add(tag('Gradient',3.8,2.15,GREEN,32)); self.finish()

class S06Apply(SpokenScene):
    def construct(self):
        o=stage()
        self.add(o,tag('Gain = Added − Slides back',size=40),
                 tag('Illustrative mechanism • rates in arbitrary units',y=-3.46,size=38))
        self.at('each side',lead=0)
        divider=DashedLine(NECK,P(2.85,-.2),color=TEXT,stroke_opacity=.65)
        self.play(Create(divider),run_time=.4)
        self.at('one common picture',lead=0)
        # Each stack sits ON its own half of the enlarged fan.
        def stacks(flow):
            return VGroup(gain_stack(-.1,1.25,'Near side',.30,flow),
                          gain_stack(-.1,-1.55,'Far side',.30,.20))
        p=stacks(.20); self.play(FadeIn(p),run_time=.5)
        self.at('near side gain more',lead=0)
        self.play(Transform(p,stacks(.14)),run_time=.7)
        self.wait(1); self.finish()

class S07How(SpokenScene):
    def construct(self):
        self.add(tag('Possible ways to increase near-side gain',size=34),tag('Illustrative mechanisms • not measured',y=-3.46,size=32))
        # Each mechanism persists as the next arrives: all have >=2.5 s reading time.
        p=RoundedRectangle(width=6.6,height=5.6,color=GREY).move_to(P(-2.9,0)); self.add(p)
        self.at('add actin faster',lead=0)
        a=tag('More actin added',-2.9,2.15,TEAL,34)
        bars=VGroup(Rectangle(width=1.8,height=.28,color=TEAL,fill_opacity=.8).move_to(P(-3.5,1.5)),Arrow(P(-2.3,1.5),P(-1,1.5),color=GREEN,buff=0))
        self.play(FadeIn(a),GrowFromEdge(bars[0],LEFT),GrowArrow(bars[1]),run_time=.5)
        self.at('ease the backward',lead=0)
        b=tag('Slower backward flow',-2.9,.35,RED,34); flow=Arrow(P(-1.7,-.3),P(-4.3,-.3),color=RED,buff=0)
        self.play(FadeIn(b),GrowArrow(flow),run_time=.3); self.play(Transform(flow,Arrow(P(-1.7,-.3),P(-3,-.3),color=RED,buff=0)),run_time=.4)
        self.at('engage more clutch',lead=0)
        c=tag('More clutch engaged',-2.9,-1.45,YELLOW,34)
        clutch=VGroup(Line(P(-4.6,-2.3),P(-1.2,-2.3),color=GREY),Line(P(-4.6,-1.95),P(-1.2,-1.95),color=BLUE),*[Line(P(x,-2.3),P(x,-1.95),color=YELLOW,stroke_width=7) for x in [-4,-3,-2]])
        self.play(FadeIn(c),Create(clutch),run_time=.5)
        self.at('a repellent',lead=0)
        panel=RoundedRectangle(width=5.2,height=5.6,color=RED).move_to(P(3.2,0)); self.play(Create(panel),FadeIn(tag('Repellent',3.2,2.15,RED,36)),run_time=.35)
        g=gain_stack(3.2,-.2,'Near side',.30,.14); self.play(FadeIn(g),run_time=.4)
        # Full contrast from its first frame, including sparse contact samples.
        self.add(tag('Gain shrinks',3.2,-2.1,TEXT,42))
        self.play(Transform(g,gain_stack(3.2,-.2,'Near side',.30,.26)),run_time=.7)
        self.wait(3); self.finish()

class S08Protrude(SpokenScene):
    def construct(self):
        o=stage(); self.add(o,source())
        self.at('puts out more',lead=0)
        sh=sheet()
        center=NECK+P(1.5*2.3,0)
        fil=VGroup()
        for angle in np.linspace(-.9,.95,13):
            u=P(np.cos(angle),np.sin(angle)); length=3.8 if angle>.15 else 3.65
            fil.add(Line(center+3.45*u,center+length*u,color=BLUE,stroke_width=5))
        self.play(FadeIn(sh),Transform(o[1][1],fil),run_time=.9)
        self.at('fan shifts',lead=0)
        dest=stage(); dest[1][1].become(fil)
        dest[1].rotate(.13,about_point=NECK)
        self.play(Transform(o,dest),sh.animate.rotate(.13,about_point=NECK),run_time=.85); self.finish()

class S09Mts(SpokenScene):
    def construct(self):
        o=stage(True); self.add(o,source(),tag('Microtubules probe the fan',size=36))
        self.at('enter the gaining',lead=0); self.play(Transform(o[1][2],near_tubes()),run_time=.75)
        probe=Line(NECK,P(.4,-1.2),color=PURPLE,stroke_width=5); self.play(Create(probe),run_time=.4)
        self.at('stay longer',lead=0)
        self.play(probe.animate.scale(.1,about_point=NECK).set_opacity(0),o[1][2].animate.set_stroke(width=9),FadeIn(tag('Near-side probes stay; far-side probes retract',y=-3.46,size=32)),run_time=.65); self.wait(1.8); self.finish()

class S10Shaft(SpokenScene):
    def construct(self):
        o=stage(True); o[1][2].become(near_tubes()); self.add(o,source())
        self.at('the fan narrows',lead=0); self.play(o[1][0].animate.stretch(.83,1,about_point=NECK),run_time=.7)
        self.at('becomes axon shaft',lead=0); turn(self,o,duration=1.4)
        self.at('pointing the new',lead=0); self.play(FadeIn(tag('New shaft points toward the source',y=-3.46,size=36)),Create(Arrow(P(-4,-.8),P(-2.85,-.12),color=TEXT,buff=.1)),run_time=.5); self.wait(1.8); self.finish()

class S11Add(SpokenScene):
    def construct(self):
        o=stage(True); heading=tag('Small difference in cue',size=40)
        self.add(o,source(),heading)
        def bias(near,far):
            return VGroup(Arrow(P(.2,1.15),P(.2+near,1.15),color=GREEN,buff=0,stroke_width=9),
                          Arrow(P(.2,-1.55),P(.2+far,-1.55),color=GREEN,buff=0,stroke_width=9))
        arrows=bias(.8,.72); self.add(arrows)
        labels=VGroup(tag('Near',-.6,1.6,size=38),tag('Far',-.6,-1.05,size=38))
        self.add(labels)
        self.at('can enlarge',lead=0)
        self.play(Transform(arrows,bias(2.3,.42)),Transform(heading,tag('Larger difference in growth',size=40)),run_time=1.5)
        self.wait(.5)
        self.at('repeated biased growth',lead=0)
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.add(tag('Repeated biased growth',size=40),tag('Schematic example',y=-3.46,size=38))
        # Four straight model time intervals: each heading is the integrated
        # heading at that interval's midpoint. Gaps expose the separate steps.
        pts,th=integrate(1.375,.625,4,start=(-5.7,-2.35))
        node=P(-5.7,-2.35)
        segments=VGroup()
        for k in range(4):
            theta=.3*(1.375-.625)*(k+.5)
            end=node+1.55*P(np.cos(theta),np.sin(theta))
            unit=(end-node)/np.linalg.norm(end-node)
            seg=path([node+.10*unit,end-.10*unit],32,BLUE if k%2 else OUTLINE)
            segments.add(seg)
            node=end
        # Enlarge and centre the cone in the open right half of the frame.
        theta=.3*(1.375-.625)*4
        cone=fan_at(*(node+1.5*1.45*P(np.cos(theta),np.sin(theta)))[:2],theta=theta,scale=1.45,tubules=True)
        figure=VGroup(segments,cone)
        fit(figure,max_w=11.8,max_h=5.35).move_to(P(0,-.1))
        for seg in segments:
            self.play(Create(seg),run_time=.65)
        self.play(FadeIn(cone),run_time=.5); self.wait(2.0); self.finish()

class S13Q(SpokenScene):
    def construct(self):
        f=question_frame(); self.add(f[0])
        self.at('stabilize the microtubules',lead=0); self.play(FadeIn(f[1]),FadeIn(f[2]),run_time=.55)
        self.at('with no',lead=0); c=tag('No guidance cue',y=-3.46,size=34); self.play(FadeIn(c),run_time=.3)
        self.at('which way',lead=0); self.play(FadeOut(c),FadeIn(f[3]),run_time=.4); self.finish()

class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame())
        base=Circle(.48,color=GREY,stroke_width=5).move_to(P(5,-1.3))
        tracker=ValueTracker(1)
        ring=always_redraw(lambda: Arc(radius=.48,start_angle=PI/2,angle=TAU*max(.001,tracker.get_value()),color=YELLOW,stroke_width=8).move_arc_center_to(P(5,-1.3)))
        self.add(base,ring); self.play(tracker.animate.set_value(0),run_time=5,rate_func=linear)

class S15Reveal(SpokenScene):
    def construct(self):
        o=stage(True); self.add(o,source(True),tag('Low-dose taxol',4.7,-2.6,PURPLE,38))
        self.at('toward the drug',lead=0); turn(self,o,duration=1.2); self.add(tag('Toward the drug',size=42,color=PURPLE))
        self.at('found this in',lead=0); self.play(FadeIn(tag('Buck & Zheng, 2002 • Xenopus spinal neurons',y=-3.46,size=32)),run_time=.4); self.finish()

class S15bActin(SpokenScene):
    def construct(self):
        o=stage(True); heading=tag('Taxol side protrudes before the turn',size=34); self.add(o,source(True),heading)
        act=mesh(); sh=sheet()
        self.at('near side protruded',lead=0); self.play(Create(act),FadeIn(sh),run_time=.8)
        self.at('turn needed actin',lead=0)
        block=tag('Block actin assembly → no turn',y=-3.46,size=34)
        self.play(FadeIn(block),act.animate.set_opacity(.08),sh.animate.set_opacity(.08),run_time=.5)
        self.wait(.7)
        self.at('can start a turn',lead=0)
        self.play(FadeOut(block),act.animate.set_opacity(1),sh.animate.set_opacity(.32),run_time=.35)
        self.remove(heading); self.add(tag('Actin and microtubules work together',size=34))
        self.play(Transform(act,mesh().shift(P(-.5,.5))),FadeOut(sh),Transform(o,turned_stage()),run_time=.8)
        self.at('working through actin',lead=0); self.play(FadeIn(tag('Microtubules → actin assembly → turn',y=-3.46,size=34)),run_time=.35); self.wait(1); self.finish()

class S16Away(SpokenScene):
    def construct(self):
        o=stage(True); self.add(o,source(True),tag('Nocodazole',color=PURPLE,size=38))
        self.at('break microtubules down',lead=0); self.play(o[1][2][-1].animate.scale(.12,about_point=o[1][2][-1].get_start()).set_opacity(.1),run_time=1)
        self.at('high enough dose',lead=0); self.play(FadeIn(tag('Effective dose',4.4,.55,PURPLE,38)),run_time=.35)
        self.at('cone turns away',lead=0); turn(self,o,-1,1.2,withdrawn=True)
        self.add(tag('Away from the drug',y=-3.46,size=36))
        # Separate no-turn comparison, held at least three seconds.
        panel=RoundedRectangle(width=4.5,height=3.0,color=GREY,fill_color=BG,fill_opacity=1).move_to(P(4,-1.45))
        mini=stage(True).scale(.20).move_to(P(3.7,-1.05)); pip=source(True).scale(.25).move_to(P(5,-1.05))
        self.play(FadeIn(panel),FadeIn(mini),FadeIn(pip),FadeIn(VGroup(tag('10× lower dose',4,-2.2,size=38),tag('No turn',4,-2.65,size=38))),run_time=.4); self.wait(3.2); self.finish()

class S17Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(tag('Microtubules can initiate a turn',size=36))
        for x,word,d in [(-3.2,'Taxol: toward',1),(3.2,'Nocodazole: away',-1)]:
            panel=RoundedRectangle(width=6.0,height=5.8,color=GREY).move_to(P(x,-.1))
            pts,th=integrate(1.25 if d>0 else .25,.25 if d>0 else 1.25,1,start=(x-2.7,-.1))
            if d<0: pts=[p+UP*.45 for p in pts]
            c=pts[-1]+1.575*P(np.cos(th),np.sin(th))
            fig=VGroup(path([P(x-2.9,pts[0][1])]+pts),fan_at(c[0],c[1],th,1.05,tubules=True))
            pip=VGroup(cloud(0,0,PURPLE),pipette(0,0,PURPLE)).scale(.6).shift(P(x+1.7,1.7))
            self.add(panel,fig,pip,tag(word,x,-2.65,PURPLE,34),Arrow(P(x-1.7,-1.8),P(x-.5,-1.8+d*.65),color=GREEN,buff=0))
        self.wait(4.8)

# Enlarge soma and fan without introducing an accidental loop during zoom-out.
def long_axon(cut=False):
    body=Circle(radius=1.4,color=BLUE,fill_opacity=.18).move_to(P(-4.8,0))
    body.add(Circle(radius=.4,color=BLUE,fill_opacity=.25).move_to(P(-4.8,0)))
    shaft=VGroup(path([P(-3.4,0),P(-1.8,0)]),path([P(-1.15,0),P(0,0)])) if cut else VGroup(path([P(-3.4,0),P(0,0)]))
    cone=fan_at(2.775,0,0,1.85,tubules=True)
    return VGroup(body,shaft,cone)

class S18Tip(SpokenScene):
    def construct(self):
        o=stage(True); self.add(o,tag('Does the tip need its cell body?',size=36))
        self.at('last question',lead=0); self.play(FadeOut(o),run_time=.25); full=long_axon(); self.play(FadeIn(full),run_time=.8)
        self.at('need its cell body',lead=0); self.play(FadeIn(tag('Cell body',-4.8,-1.9,BLUE,34)),run_time=.35); self.finish()

class S19Cut(SpokenScene):
    def construct(self):
        o=long_axon(); self.add(o,tag('Campbell and Holt • 2001',size=36))
        self.at('cut frog retinal',lead=0)
        scissors=VGroup(Line(P(-2.2,.9),P(-.75,-.9),color=TEXT,stroke_width=5),Line(P(-2.2,-.9),P(-.75,.9),color=TEXT,stroke_width=5),Circle(.22,color=TEXT).move_to(P(-2.35,1.1)),Circle(.22,color=TEXT).move_to(P(-2.35,-1.1)))
        axon_label=tag('Xenopus retinal axon',y=-3.46,size=40)
        self.play(Create(scissors),FadeIn(axon_label),run_time=.45)
        self.play(Rotate(scissors[0],angle=.15,about_point=P(-1.5,0)),Rotate(scissors[1],angle=-.15,about_point=P(-1.5,0)),run_time=.8)
        self.play(Transform(o,long_axon(True)),run_time=.4); self.play(FadeOut(scissors),run_time=.25)
        self.at('with no cell body',lead=0); self.play(FadeOut(axon_label),o[0].animate.shift(LEFT*.25),FadeIn(tag('Isolated tip',1.25,-3.46,TEXT,40)),run_time=.4); self.finish()

class S20Turns(SpokenScene):
    def construct(self):
        o=stage(True); o[0].set_points_as_corners([P(-4.5,-.2),NECK])
        cue=VGroup(cloud(4.25,1.5,TEAL),pipette(4.25,1.5,TEAL))
        self.add(o,cue,tag('Isolated tip • netrin-1 gradient',size=40))
        self.at('still turned',lead=0)
        # Sustain the turn over the sentence so draft samples catch its motion.
        turn(self,o,isolated=True,duration=3.4,scale=1.9)
        self.wait(1.5); self.finish()

class S21Mrna(SpokenScene):
    def construct(self):
        fig=turned_stage().scale(.65).move_to(P(-3.8,0)); self.add(fig,tag('Campbell & Holt: netrin-1 / Sema3A assay',size=32))
        frame=RoundedRectangle(width=6.2,height=5.4,color=GREY).move_to(P(2.8,0))
        self.at('their assay',lead=0)
        links=VGroup(Line(P(-1.9,.7),P(-.3,2.5),color=GREY),Line(P(-1.9,-.7),P(-.3,-2.5),color=GREY))
        rna=VGroup(*[Dot(P(1+i*.6,-1),radius=.12,color=TEAL) for i in range(6)])
        self.play(Create(frame),Create(links),FadeIn(rna),run_time=.5)
        self.at('turning needed protein',lead=0)
        prot=VGroup(*[Dot(P(1+i*.6,1.1),radius=.16,color=GREEN) for i in range(6)])
        self.play(FadeIn(tag('New protein',2.8,2.15,GREEN,36)),run_time=.3)
        self.at('messenger rna',lead=0); self.play(FadeIn(tag('mRNA already at tip',2.8,-2.1,TEAL,34)),run_time=.3)
        reader=RoundedRectangle(width=.45,height=.5,color=TEXT).move_to(rna[0])
        self.add(reader)
        for i in range(6):
            self.play(reader.animate.move_to(rna[i]),FadeIn(prot[i],shift=UP*.3),run_time=.25)
        self.add(Arrow(P(2.8,-.55),P(2.8,.65),color=TEXT,buff=.1)); self.wait(1); self.finish()

class S22Caveat(SpokenScene):
    def construct(self):
        card=RoundedRectangle(width=12.2,height=6.3,color=ORANGE,fill_color=ORANGE,fill_opacity=.06)
        self.add(card,tag('Depends on the cue and neuron',y=2.55,size=40))
        self.at('not every cue',lead=0); block=chip('Protein synthesis blocked',RED,size=36).move_to(P(0,1.3)); self.play(FadeIn(block),run_time=.45)
        self.at('chick sensory growth',lead=0); self.play(FadeIn(tag('Chick sensory growth cone',y=.1,size=38)),run_time=.4)
        self.at('turn toward',lead=0); arrow=Arrow(P(-4,-1),P(-2,-1),color=GREEN,buff=0); self.play(GrowArrow(arrow),FadeIn(tag('Still turns toward NGF',1.4,-1,GREEN,38)),run_time=.6)
        self.at('without it',lead=0); self.play(FadeIn(tag('Roche and colleagues • 2009',y=-2.45,size=34)),run_time=.35); self.wait(2.5); self.finish()

class S23Alone(SpokenScene):
    def construct(self):
        o=stage(True,scale=2.05); o[0].set_points_as_corners([P(-4.5,-.2),NECK])
        # Dish rim and fan have separate extents; the rim never crosses filopodia.
        dish=Ellipse(width=12.5,height=6.1,color=GREY,stroke_opacity=.55)
        self.add(dish,o,tag('The isolated tip can decide on its own',size=34))
        self.at('tip can decide',lead=0)
        self.play(Transform(o,turned_stage(scale=1.65,isolated=True).shift(UP*.45)),run_time=1.25)
        self.at('at least',lead=0); self.play(FadeIn(tag('At least in a dish',y=-3.46,size=38)),run_time=.35); self.finish()

class S24Takeaway(SpokenScene):
    def construct(self):
        self.add(RoundedRectangle(width=12.4,height=6.4,color=PURPLE,fill_color=PURPLE,fill_opacity=.06),tag('Carry the rule',y=2.55,size=42))
        self.at('a turn sticks',lead=0); a=tag('A turn sticks where',y=1.2,size=44); self.play(FadeIn(a),run_time=.35)
        self.at('microtubules move in',lead=0); self.play(FadeIn(tag('microtubules move in',y=.1,color=PURPLE,size=44)),run_time=.4)
        self.at('build axon',lead=0); self.play(FadeIn(tag('and build axon.',y=-1,size=44)),run_time=.4)
        self.at('can start it',lead=0); self.play(FadeIn(tag('They can start it too.',y=-2.3,color=PURPLE,size=42)),run_time=.4); self.wait(2.5); self.finish()

class S25Next(SpokenScene):
    def construct(self):
        # Centred fan, two cue families on each side with clear incoming arrows.
        fig=stage(True); fig[0].set_points_as_corners([P(-3.5,-.2),NECK]); fig.scale(.8).move_to(P(0,-.1))
        self.add(fig,tag('Next: cues that make the sides differ',size=36))
        for phrase,name,x,y in [('netrins','Netrins',-4.5,1.9),('slits','Slits',4.5,1.9),('semaphorins','Semaphorins',-4.5,-2.3),('ephrins','Ephrins',4.5,-2.3)]:
            self.at(phrase,lead=0); c=chip(name,ORANGE,size=38).move_to(P(x,y)); target=P(-.6 if x<0 else 1.4,.8 if y>0 else -1)
            start=c.get_right() if x<0 else c.get_left(); self.play(FadeIn(c),GrowArrow(Arrow(start,target,color=ORANGE,buff=.15)),run_time=.35)
        self.wait(2.2); self.finish()

class S26End(EndCard):
    LINE='A turn sticks where microtubules build axon.'
    def construct(self):
        self.add(tag('A turn sticks where',y=1.15,size=44),tag('microtubules build axon.',y=.1,color=PURPLE,size=44),tag('They can start it too.',y=-1.15,size=40),tag('biochemistrypedia.com',y=-2.5,color=TEAL,size=32)); self.finish()
