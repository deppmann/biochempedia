"""From Where to What — chapter 3, word-synchronized teaching film.

COLOR MAP (scenes.old.py, unchanged): BLUE = map/plain structures; TEAL =
selected region / preferred direction; RED = lesion/damage; YELLOW = recording;
GREEN = imaging/blood signal; ORANGE = stimulation; GREY = neutral/limits.
CHAPTERS.md is left untouched because TASK.md restricts edits to scenes.py.

Plots are computed, not hand-drawn. The choice demonstration uses the lesson's
quiz example, P(preferred|zero motion)=.50 without stimulation and .72 with it.
A unit-slope logistic is calibrated to those points; horizontal units and slope
are illustrative, not a fit to Salzman data. The traces encode the qualitative
sustained-field/sustained-blood/transient-spiking example in the lesson quiz,
using explicitly illustrative normalized dynamics, not measured amplitudes or latencies.
Anatomical continuity only: chapter 1 PURPLE cerebrum, GREEN midbrain, ORANGE
hindbrain, TAN cord; chapter 2 TEAL endothelium, GREY membrane, TAN endfeet.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as _SpokenScene

class SpokenScene(_SpokenScene):
    def at(self,phrase,lead=0,nth=0):
        target=self.t_of(phrase,nth)-lead
        if target>self.elapsed(): self.wait(target-self.elapsed())


ORANGE = '#F29E4C'
MAP, HIL, LES, REC, IMG, STIM = BLUE, TEAL, RED, YELLOW, GREEN, ORANGE


def p(x,y): return np.array([x,y,0.])
def lab(s,x=0,y=0,c=TEXT,size=28):
    if '\n' in s:
        return VGroup(*[T(line,size=size,color=c) for line in s.split('\n')]).arrange(DOWN,buff=.23).move_to(p(x,y))
    return T(s,size=size,color=c).move_to(p(x,y))
def head(s,c=TEXT): return lab(s,0,3.05,c,34)
def lines(points,c=GREY,w=3):
    return VMobject().set_points_as_corners([p(x,y) for x,y in points]).set_stroke(c,w)


def brain():
    # Chapter 1's lateral contour and anatomical palette, carried across the cut.
    def blob(ps,c,opacity=.3):
        return VMobject().set_points_smoothly([p(*v) for v in ps+[ps[0]]]).set_stroke(c,2.5).set_fill(c,opacity)
    purple='#AC8CDE';tan='#CCA982'
    hemi=blob([(-3.5,.1),(-3.7,1.1),(-3,2.2),(-1.7,2.85),(.1,2.8),(1.7,2.2),(2.1,1.2),(1.7,.25),(.6,-.25),(-.4,-.8),(-1.8,-.7),(-2.6,-.4)],purple)
    far=hemi.copy().scale(.92).shift(UP*.22+RIGHT*.15).set_fill(purple,.12)
    mid=blob([(-.15,-.4),(.65,-.25),(.9,-1.05),(.25,-1.25)],GREEN,.6)
    hind=blob([(.25,-1.1),(.85,-.9),(1.8,-1.25),(1.7,-2.1),(.8,-2.85),(.2,-2.6),(.15,-2),(-.2,-1.65)],ORANGE,.4)
    cb=blob([(1,-1.25),(1.1,-.55),(1.7,-.35),(2.5,-.7),(2.6,-1.3),(2,-1.65),(1.4,-1.55)],ORANGE,.65)
    return VGroup(far,hemi,mid,hind,cb,Line(p(.6,-2.85),p(.6,-3.25),color=tan,stroke_width=30))


def tool(kind):
    if kind==0:  # scalpel
        return VGroup(Line(p(-.7,.7),p(.3,-.25),color=LES,stroke_width=14),Polygon(p(.25,-.2),p(.8,-.75),p(.27,-.52),color=LES,fill_opacity=.6))
    if kind==1:  # electrode
        return VGroup(RoundedRectangle(width=1.25,height=.5,corner_radius=.08,color=MAP,fill_opacity=.18).move_to(p(0,-.45)),Line(p(.35,.65),p(-.15,-.45),color=REC,stroke_width=7),Line(p(.35,.65),p(.7,.65),color=REC,stroke_width=4))
    if kind==2:  # scanner
        return VGroup(Annulus(inner_radius=.42,outer_radius=.76,color=IMG,fill_opacity=.4,stroke_width=2),Rectangle(width=1.6,height=.18,color=GREY,fill_opacity=.6).move_to(p(0,-.38)))
    return VGroup(RoundedRectangle(width=1.4,height=1.3,corner_radius=.15,color=STIM,fill_opacity=.12),lines([(-.5,0),(-.2,0),(-.2,.35),(.1,.35),(.1,-.2),(.4,-.2),(.4,0)],STIM,5))


def regions(height=3.5,width=2.65):
    return VGroup(*[VGroup(RoundedRectangle(width=width,height=height,corner_radius=.15,color=MAP,fill_opacity=.18).move_to(p(x,0)),lab('region '+name,x,-height/2+.38,MAP,28)) for x,name in zip([-width-.12,0,width+.12],'ABC')])

def damage(w=1.6):
    return Ellipse(width=w,height=2.4,color=LES,fill_opacity=.3,stroke_width=5).move_to(p(.35,.3))

def slice_brain():
    return VGroup(Ellipse(width=6.7,height=5.1,color=MAP,fill_opacity=.17).move_to(p(-1.25,-.1)))

def activation(): return Ellipse(width=1.7,height=1.25,color=IMG,fill_opacity=.65).rotate(.3).move_to(p(-.6,.65))

def dots_field(width=6.5,height=5.0,n=51,seed=11,reserve_corner=False):
    rng=np.random.default_rng(seed)
    box=RoundedRectangle(width=width,height=height,corner_radius=.12,color=GREY,fill_opacity=.05)
    xy=rng.uniform([-width/2+.15,-height/2+.15],[width/2-.15,height/2-.15],(n,2))
    dots=VGroup(*[Dot(p(*a),radius=.058,color=HIL if i<n//3 else GREY) for i,a in enumerate(xy)])
    field=VGroup(box,dots)
    # Persistent model: coherent rightward velocities; seeded independent noise.
    vel=rng.uniform(-.8,.8,(n,2));vel[:n//3]=[.9,0]
    age=[0.]
    def drift(m,dt):
        age[0]+=dt
        center=m[0].get_center();w=m[0].width-.25;h=m[0].height-.25
        for i,d in enumerate(m[1]):
            v=xy[i]+vel[i]*age[0]
            dx=(v[0]+w/2)%w-w/2;dy=(v[1]+h/2)%h-h/2
            # Reserve the upper-right corner for the current marker, even in motion.
            if reserve_corner and dx>width/2-.7 and dy>height/2-.7:
                dy-=.7
            d.move_to(center+p(dx,dy))
    field.add_updater(drift)
    return field


def choice_targets(x=4.5):
    return VGroup(Arrow(p(x-.65,.85),p(x+.65,.85),color=HIL,buff=0),lab('preferred',x,.25,HIL,28),Arrow(p(x+.65,-.8),p(x-.65,-.8),color=GREY,buff=0),lab('other',x,-1.4,TEXT,28))


def neuron(c=MAP):
    # Same labelled cartoon vocabulary as reference neuron().
    soma=Circle(radius=.32,color=c,fill_opacity=.35)
    dend=VGroup(*[Line(p(.28*np.cos(a),.28*np.sin(a)),p(.65*np.cos(a),.65*np.sin(a)),color=c,stroke_width=3) for a in [PI/4,PI/2,3*PI/4]])
    axon=Line(p(0,-.3),p(0,-1),color=c,stroke_width=3)
    return VGroup(soma,dend,axon)


def mt_panel():
    box=RoundedRectangle(width=10.7,height=5.25,corner_radius=.2,color=MAP,fill_opacity=.1).move_to(p(0,-.05))
    cells=VGroup(*[neuron().scale(2.05).move_to(p(x,.25)) for x in [-3.5,0,3.5]])
    elec=Line(p(1.5,2.5),p(.3,.9),color=STIM,stroke_width=7)
    arrows=VGroup(*[Arrow(p(x-.4,.65),p(x+.4,.65),color=HIL,buff=0,stroke_width=5) for x in [-3.5,0,3.5]])
    return box,cells,elec,arrows


def choice_plot():
    # Exactly .50 and .72 at zero motion. Normalized slope/strength are illustrative.
    axes=Axes(x_range=[-4,4,2],y_range=[0,1,.5],x_length=8.7,y_length=5.0,tips=False,axis_config={'color':GREY,'include_ticks':True}).move_to(p(.8,.1))
    curve=axes.plot(lambda x:1/(1+np.exp(-x)),x_range=[-4,4,.04],color=TEXT,stroke_width=4)
    stim=axes.plot(lambda x:1/(1+np.exp(-(x+np.log(.72/.28)))),x_range=[-4,4,.04],color=STIM,stroke_width=5)
    axes.y_axis.set_opacity(0)
    zero=VGroup(DashedLine(axes.c2p(0,0),axes.c2p(0,1),color=GREY,stroke_width=2),Line(axes.c2p(-4,0),axes.c2p(-4,1),color=GREY,stroke_width=2),*[Line(axes.c2p(-4,v)+LEFT*.08,axes.c2p(-4,v)+RIGHT*.08,color=GREY) for v in [0,.5,1]])
    ticks=VGroup(*[lab(str(v)+'%',-4.1,axes.c2p(0,v/100)[1],TEXT,26) for v in [0,50,100]])
    labels=VGroup(zero,ticks,lab('Choices toward preferred direction',-5.35,.1,HIL,26).rotate(PI/2),lab('dot motion',.8,-3.05,TEXT,28),lab('other',-3.15,-2.8,TEXT,26),lab('preferred →',4.7,-2.8,HIL,26),lab('Illustrative model · lesson example',0,-3.5,GREY,26),lab('no net motion',.8,2.85,TEXT,26),lab('without stimulation',3.5,-1.2,TEXT,26),Line(p(3.5,-.9),axes.c2p(1.4,.802),color=TEXT,stroke_width=2))
    q=lab('?',-.3,.9,STIM,70)
    title=lab('Which way should stimulation push choices?',0,3.5,STIM,30)
    return axes,curve,stim,labels,q,title


def table():
    headers=VGroup(lab('Evidence',-4.9,3.0,TEXT,28),lab('Can show',-.8,3.0,TEXT,28),lab('Cannot show alone',3.8,3.0,LES,28))
    data=[('Lesion',LES,'Contribution','Which part mattered'),('Recording',REC,'Covariation','Use'),('Imaging',IMG,'Where blood\nsignal goes','Which neural signal'),('Stimulation',STIM,'Contribution','Region is required')]
    rows=[]
    for i,(name,c,yes,no) in enumerate(data):
        y=1.8-i*1.5
        rows.append(VGroup(lab(name,-4.9,y,c,28),lab(yes,-.8,y,TEXT,28),lab(no,3.8,y,LES,28),Line(p(-6.3,y-.65),p(6.3,y-.65),color=GREY,stroke_opacity=.25)))
    return headers,rows


class S00Title(TitleCard):
    LESSON='The Map: How the Nervous System Is Organized'
    TITLE='From Where to What'
    def construct(self):
        self.add(lab('BIOCHEMISTRYPEDIA',0,1.8,TEAL,26),lab('The Map: How the Nervous System',0,.9,GREY,26),lab('Is Organized',0,.4,GREY,26))
        self.play(FadeIn(lab(self.TITLE,0,-.8,TEXT,48)),run_time=.7)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        b=brain().scale(.9).shift(DOWN*.2);h=head('Where?');self.add(b,h)
        self.at('where a region');self.play(b[1].animate.set_fill(HIL,.5),FadeIn(lab('Cerebrum',4.25,1.4,HIL,30)),Create(Line(p(3.1,1.4),p(1.2,1.2),color=HIL)),run_time=.5)
        self.at('How do you');self.play(FadeIn(lab('?',-.8,1.2,HIL,110)),Transform(h,head('What does it do?')),run_time=.5)
        self.finish()


class S02License(SpokenScene):
    def construct(self):
        heading=lab('Each kind licenses (entitles you to)\na different claim',0,2.9,TEXT,32)
        self.at('You need');self.add(heading)
        icons=VGroup(*[VGroup(tool(i).scale(1.45).move_to(p(-4.8+i*3.2,.15)),lab(name,-4.8+i*3.2,-2.1,[LES,REC,IMG,STIM][i],30)) for i,name in enumerate(['Lesion','Recording','Imaging','Stimulation'])])
        self.play(LaggedStart(*[FadeIn(t) for t in icons],lag_ratio=.15),run_time=1.0)
        self.at('Each kind');self.play(Indicate(heading,scale_factor=1.02),run_time=.45)
        self.finish()


class S03Lesion(SpokenScene):
    def construct(self):
        # Two full-height tissue sets allow an actual control comparison.
        a=regions(width=1.7).move_to(p(-3.25,0));b=regions(width=1.7).move_to(p(3.25,0))
        # Region names belong to the border-spread scene; keep these uncluttered.
        for group in [a,b]:
            for reg in group: reg[1].set_opacity(0)
        icon=tool(0).scale(.9).move_to(p(2.8,1.05))
        self.add(a,b,icon,head('Lesion',LES),lab('Control',-3.25,2.25,TEXT,30),lab('After damage',3.25,2.25,LES,30))
        self.at('A deficit');self.play(icon.animate.move_to(p(2.92,.7)),run_time=.35)
        self.play(FadeIn(damage().move_to(p(3.25,.15))),FadeOut(icon),FadeIn(lab('task impaired',3.25,-2.3,LES,30)),run_time=.35)
        self.at('compared with controls');self.play(FadeIn(lab('task intact',-3.25,-2.3,TEXT,30)),Indicate(a,scale_factor=1.02),run_time=.45)
        self.at('contributes to the task');self.play(FadeIn(lab('Does losing it hurt the task?',0,-3.25,LES,32)),run_time=.4)
        self.finish()


class S04Lesion2(SpokenScene):
    def construct(self):
        r=regions();d=damage();self.add(r,d,head('Damage can cross borders',LES))
        self.at('But damage');self.play(Transform(d,damage(6.5)),run_time=1.5)
        self.at('so which part');self.play(FadeIn(lab('Which part mattered?',0,-2.65,LES,34)),run_time=.4)
        self.finish()


class S05Recording(SpokenScene):
    def construct(self):
        cell=neuron().scale(2.7).move_to(p(-4.5,.1))
        electrode=Line(p(-2.8,2.2),p(-4.25,1),color=REC,stroke_width=7)
        wire=lines([(-2.8,2.2),(-2.2,2.2),(-2.2,-.3),(-1.7,-.3)],REC,3)
        large=VGroup(neuron().scale(3.6).move_to(p(0,-.2)),Line(p(2.5,2.1),p(.6,1.1),color=REC,stroke_width=7))
        self.add(large,head('Recording',REC))
        baseline=Line(p(-1.7,-.3),p(5.9,-.3),color=GREY)
        # Event times from a piecewise-rate schematic model; not measured spikes.
        ts=np.r_[np.arange(.2,2,.6),np.arange(2,4.5,.14),np.arange(4.5,6.7,.6)]
        ticks=VGroup(*[Line(p(-1.7+t,-.3),p(-1.7+t,2.25),color=REC,stroke_width=3) for t in ts])
        axis=Arrow(p(-1.7,-1.7),p(5.9,-1.7),color=GREY,buff=0)
        choice=Rectangle(width=2.5,height=.65,color=HIL,fill_opacity=.4).move_to(p(1.55,-.95))
        self.at('Firing that goes');self.play(Transform(large,VGroup(cell,electrode)),Create(wire),Create(baseline),Create(ticks),FadeIn(lab('neuron',-4.5,-2.0,MAP,28)),run_time=.65)
        self.at('with a choice');self.play(FadeIn(choice),FadeIn(lab('choice',1.55,-.95,HIL,28)),Create(axis),FadeIn(lab('time',5.4,-2.15,TEXT,26)),run_time=.4)
        self.at('not that the brain');self.play(FadeIn(lab('Does it go along? ≠ Is it used?',0,-3.1,REC,32)),run_time=.4)
        self.add(lab('Schematic spike raster',2,2.75,GREY,26))
        self.finish()


class S06Imaging(SpokenScene):
    def construct(self):
        self.add(slice_brain(),tool(2).scale(1.65).move_to(p(4.6,.5)),lab('MRI scanner',4.6,-1.0,IMG,28),head('Imaging',IMG))
        self.at('Functional');self.play(FadeIn(activation()),FadeIn(lab('Where does blood follow?',-1.25,-1.55,IMG,28)),run_time=.45)
        self.at('blood oxygenation');self.add(lab('Blood oxygenation',-1.25,-3.1,IMG,32))
        self.at('not spikes');self.play(FadeIn(lab('≠ spikes',4.6,-1.6,TEXT,30)),run_time=.35)
        self.finish()


class S07Imaging2(SpokenScene):
    def construct(self):
        self.add(lab('Anaesthetized macaque · visual cortex',0,3.4,TEXT,28))
        # Illustrative normalized dynamics, not fits or measured traces:
        # sustained local activity, adapting spikes, and a delayed low-pass blood response.
        t=np.linspace(0,8,321);u=((t>=1)&(t<6)).astype(float)
        field=u*(1-.08*np.cos(t*4));spikes=u*np.exp(-np.maximum(t-1,0)/.65)
        blood=np.zeros_like(t)
        for i in range(1,len(t)):
            drive=u[max(0,i-16)];blood[i]=blood[i-1]+(t[i]-t[i-1])*(drive-blood[i-1])/.7
        traces=[]
        for y,v,c,name in [(1.9,field,REC,'Field potential'),(.15,blood,IMG,'Blood signal'),(-1.6,spikes,GREY,'Spiking')]:
            trace=lines(list(zip(-1.8+t*.9,y-.35+v*.9)),c,4)
            traces.append(VGroup(lab(name,-4.3,y,c,28),Line(p(-1.8,y-.35),p(5.4,y-.35),color=GREY,stroke_opacity=.3),trace))
        self.add(*traces,lab('fell back early',3.5,-1.45,TEXT,26))
        self.add(Rectangle(width=4.5,height=.12,color=HIL,fill_opacity=1).move_to(p(1.35,-2.6)),lab('stimulus on',1.3,-2.95,HIL,26),lab('time →',5,-2.95,TEXT,26),lab('Qualitative model · not measured traces',0,-3.55,GREY,26))
        self.at('local field potentials');self.play(Create(lines([(5.7,2.45),(5.95,2.45),(5.95,.5),(5.7,.5)],IMG,3)),run_time=.45)
        self.at('Field potentials mostly');self.play(traces[2][0].animate.set_opacity(.5),traces[2][1].animate.set_stroke(opacity=.5),traces[2][2].animate.set_stroke(opacity=.5),Indicate(traces[0],scale_factor=1.02),run_time=.4)
        self.at('synaptic and dendritic currents');self.play(FadeIn(lab('(synaptic +\ndendritic currents)',-4.3,1.05,REC,26)),run_time=.4)
        self.at('near the electrode');self.play(FadeIn(VGroup(Line(p(1.2,2.95),p(.45,2.35),color=REC,stroke_width=7),Line(p(1.2,2.95),p(1.75,2.95),color=REC,stroke_width=4),Dot(p(.45,2.35),radius=.07,color=REC))),run_time=.4)
        self.finish()


class S08Seat(SpokenScene):
    def construct(self):
        b=slice_brain();a=activation();g=VGroup(b,a).scale(1.08).move_to(p(-.9,-.1));self.add(g,tool(2).scale(1.5).move_to(p(4.7,0)))
        self.at('So an activation');self.play(a.animate.set_fill(opacity=.12).set_stroke(opacity=.3),run_time=.8)
        self.at('does not mark');self.play(FadeIn(head('Activation is not a seat',IMG)),run_time=.4)
        self.finish()


class S09Stim(SpokenScene):
    def construct(self):
        # Dots drift throughout, including holds. Rightward teal dots form a third.
        g=dots_field().move_to(p(-1.5,-.1));self.add(g,head('Stimulation',STIM),tool(3).scale(.85).move_to(p(4.6,2)))
        self.at('adds activity');self.play(Indicate(self.mobjects[-1],color=STIM),run_time=.4)
        self.at('Monkeys judged');self.play(FadeIn(choice_targets()),run_time=.4)
        self.at('noisy dots');self.play(FadeIn(lab('Enough to move the choice?',0,-3.25,STIM,30)),run_time=.4)
        self.finish()


class S10Mt(SpokenScene):
    def construct(self):
        box,cells,e,a=mt_panel();self.add(box,cells)
        self.at('An electrode');self.play(Create(e),run_time=.5)
        self.at('neurons that');self.play(FadeIn(head('area MT',MAP)),run_time=.4)
        bursts=VGroup(*[VGroup(*[Line(p(x+dx,-1.4),p(x+dx,-.75),color=REC,stroke_width=3) for dx in [-.4,-.2,0,.2,.4]]) for x in [-3.5,0,3.5]])
        self.at('all fire most');self.play(*[GrowArrow(x) for x in a],Create(bursts),run_time=.65)
        self.at('their preferred direction');self.add(lab('Preferred direction →',0,-3.2,HIL,30))
        self.finish()


class S11Pulses(SpokenScene):
    def construct(self):
        self.add(head('Randomly interleaved trials'),lab('Preferred direction →',0,-3.45,HIL,28))
        on=[True,False,False,True,False,True]
        flashes=VGroup()
        for i,active in enumerate(on):
            x=-4.3+(i%3)*4.3;y=1.2-(i//3)*2.7
            # Each trial has a 1.6-high continuously drifting stimulus.
            g=dots_field(3.3,1.6,18,seed=101+i,reserve_corner=True).move_to(p(x,y));self.add(g)
            self.add(lab(str(i+1),x-1.4,y+1.05,TEXT,26))
            self.add(lab('current' if active else 'no current',x,y-1.1,STIM if active else TEXT,28))
            if active:flashes.add(lines([(x+1.4,y+.65),(x+1.15,y+.4),(x+1.4,y+.4),(x+1.15,y+.15)],STIM,5))
        self.at('weak current flowed');self.play(FadeIn(flashes),run_time=.4)
        self.at('while the dots');self.play(Indicate(flashes,scale_factor=1.08),run_time=.4)
        self.finish()


class S12Predict(SpokenScene):
    def construct(self):
        ax,c,st,l,q,h=choice_plot();self.add(ax,l)
        self.at('If the monkey');self.play(Create(c),run_time=.65)
        self.at('which way should');self.play(FadeIn(h),FadeIn(q),run_time=.4)
        self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        ax,c,st,l,q,h=choice_plot();self.add(ax,c,l,q,h);self.wait(5)


class S14Reveal(SpokenScene):
    def construct(self):
        ax,c,st,l,q,h=choice_plot();self.add(ax,c,l,q,h)
        # The label is present from the start of the curve reveal, held to 'In'.
        y_at=1/(1+np.exp(1.3-np.log(.72/.28)))
        label=VGroup(lab('with stimulation',-1.3,2.1,STIM,26),Line(p(-1.3,1.85),ax.c2p(-1.3,y_at),color=STIM,stroke_width=2))
        a=Arrow(ax.c2p(0,.5),ax.c2p(0,.72),buff=0,color=STIM,stroke_width=5,max_tip_length_to_length_ratio=.3)
        nums=VGroup(lab('50%',1.45,-.05,TEXT,26),lab('72%',1.45,1.4,STIM,26))
        caption=lab('More choices toward preferred at every motion strength',0,3.5,STIM,27)
        self.at('toward');self.remove(q,h);self.add(label,caption)
        self.play(Create(st),GrowArrow(a),FadeIn(nums),run_time=.55)
        self.at('In');self.play(FadeOut(VGroup(ax,c,st,l,label,a,nums,caption)),run_time=.2)
        title=head('139 experiments',TEXT)
        total=Rectangle(width=11.6,height=1.0,color=GREY,fill_opacity=.15).move_to(p(0,1.8))
        sig=Rectangle(width=11.6*89/139,height=1.0,color=STIM,fill_opacity=.6).align_to(total,LEFT).set_y(1.8)
        # A second, enlarged view of exactly those 89; 86 is nested INSIDE 89.
        subset=Rectangle(width=11.6,height=1.0,color=STIM,fill_opacity=.15).move_to(p(0,-.65))
        toward=Rectangle(width=11.6*86/89,height=1.0,color=HIL,fill_opacity=.55).align_to(subset,LEFT).set_y(-.65)
        self.add(title,total,sig,subset,toward,lab('89 with a significant effect',0,.85,STIM,32),lab('86 of those 89: toward preferred',0,-1.65,HIL,32),lab('86 / 89',0,-.65,TEXT,32),lab('89 / 139',-2.1,1.8,TEXT,32))
        self.add(lab('Enlarged view of the 89',0,-2.8,TEXT,28))
        self.at('significant effect');self.play(Indicate(sig,scale_factor=1.015),run_time=.35)
        self.at('that is what happened');self.play(Indicate(toward,scale_factor=1.015),run_time=.35)
        self.finish()


class S15Licenses(SpokenScene):
    def construct(self):
        card=RoundedRectangle(width=11.6,height=2.8,corner_radius=.2,color=STIM,fill_opacity=.14).move_to(p(0,1.45))
        self.add(card)
        self.at('That shows');self.play(FadeIn(lab('licenses: a causal contribution\nin this task',0,1.45,STIM,38)),run_time=.5)
        self.at('It does not make');self.add(lab('Does not show:',0,-.85,TEXT,32))
        # Shape both items in one text run so their typographic baselines match.
        row=T('Seat of motion       Required',size=36,disable_ligatures=True).move_to(p(0,-2.7))
        seat=VGroup(*row[:14]);req=VGroup(*row[21:])
        seat.shift(RIGHT*(-2.8-seat.get_x()));req.shift(RIGHT*(3-req.get_x()))
        self.play(FadeIn(seat),Create(lines([(-5.5,-2.5),(-5.1,-2.9)],LES)),Create(lines([(-5.5,-2.9),(-5.1,-2.5)],LES)),run_time=.4)
        self.at('or show it');self.play(FadeIn(req),Create(lines([(1,-2.5),(1.4,-2.9)],LES)),Create(lines([(1,-2.9),(1.4,-2.5)],LES)),run_time=.4)
        self.finish()


class S16Table1(SpokenScene):
    def construct(self):
        h,r=table();self.add(h)
        self.at('So a lesion');self.play(FadeIn(VGroup(r[0][0],r[0][1],r[0][3])),run_time=.35)
        self.at('not which part');self.play(FadeIn(r[0][2]),run_time=.35)
        self.at('A recording');self.play(VGroup(r[0][0],r[0][1]).animate.set_opacity(.65),FadeIn(VGroup(r[1][0],r[1][1],r[1][3])),run_time=.35)
        self.at('not use');self.play(FadeIn(r[1][2]),run_time=.35)
        self.finish()


class S17Table2(SpokenScene):
    def construct(self):
        h,r=table();self.add(h,*r[:2])
        for row in r[:2]:
            row[0].set_opacity(.65);row[1].set_opacity(.65)
        self.at('Imaging shows');self.play(FadeIn(VGroup(r[2][0],r[2][1],r[2][3])),run_time=.35)
        self.at('not which neural');self.play(FadeIn(r[2][2]),run_time=.35)
        self.at('Stimulation shows');self.play(VGroup(r[2][0],r[2][1]).animate.set_opacity(.65),FadeIn(VGroup(r[3][0],r[3][1],r[3][3])),run_time=.35)
        self.at('not that the region');self.play(FadeIn(r[3][2]),run_time=.35)
        self.finish()


class S18Link(SpokenScene):
    def construct(self):
        # Same chapter-2 capillary vocabulary: teal endothelium, grey basement
        # membrane, tan endfeet. Longitudinal inset exposes the junction route.
        x=-3.3
        vessel=VGroup(Rectangle(width=5.5,height=3.35,color=TEAL,fill_opacity=.08).move_to(p(x,.175)),Line(p(-6.05,1.85),p(-.55,1.85),color=TEAL,stroke_width=14),Rectangle(width=2.68,height=.55,color=TEAL,fill_opacity=.4).move_to(p(-4.71,-1.77)),Rectangle(width=2.68,height=.55,color=TEAL,fill_opacity=.4).move_to(p(-1.89,-1.77)),Line(p(-6.05,-2.17),p(-.55,-2.17),color=GREY,stroke_width=5),Line(p(-6.05,-2.45),p(-.55,-2.45),color='#CCA982',stroke_width=12))
        seal=Line(p(x-.1,-1.83),p(x+.1,-1.83),color=HIL,stroke_width=9)
        tracer=VGroup(*[Dot(p(-5.6+i*.7,.45+(i%2)*.4),radius=.09,color=REC) for i in range(6)])
        self.add(vessel,seal,lab('Capillary',x,2.55,TEAL,30),lab('blood · lumen',x,1.3,TEXT,28),lab('Reese and Karnovsky',x,3.35,TEXT,28))
        field=dots_field(4.7,2.2,30).move_to(p(3.4,1.3))
        electrode=Line(p(5.9,2.6),p(4.95,1.75),color=STIM,stroke_width=6)
        flash=lines([(5.8,1.6),(5.55,1.1),(5.9,1.1),(5.55,.6)],STIM,5)
        # Miniature of the same computed choice model, kept beside the tracer.
        ax=Axes(x_range=[-4,4,4],y_range=[0,1,1],x_length=4.4,y_length=1.85,tips=False,axis_config={'include_ticks':False,'color':GREY}).move_to(p(3.4,-1.2))
        self.add(field,electrode,flash,lab('Stimulation',3.4,3.35,STIM,30),ax,ax.plot(lambda z:1/(1+np.exp(-z)),color=TEXT),ax.plot(lambda z:1/(1+np.exp(-(z+np.log(.72/.28)))),color=STIM))
        self.add(lab('Illustrative model',3.4,-2.4,GREY,26))
        self.at('also added something');self.play(FadeIn(tracer),run_time=.3)
        self.play(*[d.animate.move_to(p(x+(i-2.5)*.035,-1.68+.12*(i%2))) for i,d in enumerate(tracer)],run_time=1.5)
        self.at('But their tracer');self.add(lab('Tracer: where it stops',x,-3.25,REC,28),lab('tight junction',x,-2.7,HIL,26),Line(p(x+.15,-2.5),p(x+.15,-1.95),color=HIL,stroke_width=2))
        self.at('a different kind');self.play(FadeIn(lab('Stimulation: a causal contribution',3.4,-3.25,STIM,28)),Indicate(flash,scale_factor=1.08),run_time=.35)
        self.finish()


class S19Close(SpokenScene):
    def construct(self):
        self.at('Claim only');self.add(lab('Claim only what\nthe evidence licenses.',0,0,GOLD,52))
        self.finish()


class S20End(EndCard):
    LINE='Claim only what the evidence licenses.'
    def construct(self):
        self.add(lab('Claim only what\nthe evidence licenses.',0,0,GOLD,52),lab('biochemistrypedia.com',0,-2,TEAL,26))
        self.finish()
