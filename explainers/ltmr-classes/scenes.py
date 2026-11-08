"""Chapter 1, reviewed fix round.
COLOR MAP: TEAL SA I/Merkel; BLUE RA/Aβ; GREY PC/skin/probe;
YELLOW Aδ; ORANGE C; PURPLE Schwann; GOLD takeaway/highlight.
All stimulus curves are sampled equations. Rasters are deterministic schematic
response models (sustained drive versus change detection), not measured counts.
Sensitivity curves are illustrative filters, not fitted physiological data.
"""
import os
import numpy as np
from bp_style import *
BLUE = '#659BFF'  # More distinct from SA I teal, same RA concept.
ORANGE = '#F29A57'
PURPLE = '#B68CDB'
COL = [TEAL, BLUE, GREY]
NAMES = ['SA I', 'RA', 'PC']

_style_text = T

def T(text, size=30, color=TEXT, **kw):
    # Manim Text keeps multiline strings left aligned; centre each line explicitly.
    kw.pop('should_center', None)
    spacing = kw.pop('line_spacing', 1)
    if '\n' in text:
        return VGroup(*[_style_text(line, size, color, **kw) for line in text.split('\n')]).arrange(DOWN, buff=.18*spacing)
    return _style_text(text, size, color, **kw)



def exact_finish(self):
    # No default 0.4-s tail on every clip. Quantize to nearest output frame.
    target = round(self.narration_s * config.frame_rate) / config.frame_rate
    if target > self.renderer.time + .001:
        self.wait(target - self.renderer.time)


class SpokenScene(SpokenScene):
    def at(self, phrase, lead=.12, nth=0):
        target = self.t_of(phrase, nth) - lead
        if target > self.elapsed() + .02:
            self.wait(target-self.elapsed())
    finish = exact_finish


def heading(s):
    return T(s, 32, font=TITLE_FONT).move_to([0,3.25,0])


def curve(points, color=GREY, width=4):
    return VMobject(stroke_color=color,stroke_width=width).set_points_as_corners(points)


def ramp(t):
    return np.interp(t,[0,.2,.4,1.4,1.6,1.8],[0,0,1,1,0,0])


def events(mode):
    # Fixed-step toy response to sustained indentation or its temporal derivative.
    t=np.arange(0,1.8,.002)
    p=ramp(t); change=np.abs(np.gradient(p,t))
    if mode=='steady': drive=np.where(p>.05,12.,0.)
    elif mode=='burst': drive=np.where(change>1,18.,0.)
    elif mode=='brief': drive=np.where(change>1,5.,0.)
    elif mode=='vibration':
        # A 250-Hz carrier, growing envelope, sampled in a 64-ms window.
        t=np.arange(0,.064,.00002)
        drive=np.where(t>.009,250.,0.)
    else: return []
    phase=0.; out=[]; dt=t[1]-t[0]
    for ti,d in zip(t,drive):
        phase+=d*dt
        if phase>=1:
            out.append(ti/(.064 if mode=='vibration' else 1.8)); phase-=1
    return out


def position():
    return curve([[-4.5+10.1*t/1.8,1.3+.62*ramp(t),0] for t in np.linspace(0,1.8,300)],TEXT)


def phase_labels():
    return VGroup(*[T(s,26,GREY).move_to([x,2.3,0]) for s,x in [('press',-2.8),('hold',.55),('lift',4.05)]])


def raster(i,mode=None):
    y=.65-i*1.35
    base=Line([-4.5,y,0],[5.6,y,0],color=COL[i],stroke_opacity=.5)
    lab=T(NAMES[i],30,COL[i]).move_to([-5.5,y+.15,0])
    spikes=VGroup(*[Line([-4.5+10.1*t,y,0],[-4.5+10.1*t,y+.55,0],color=COL[i],stroke_width=3) for t in events(mode)])
    return VGroup(base,lab,spikes)


def timebar(vib=False):
    return VGroup(Line([-4.5,-2.65,0],[5.6,-2.65,0],color=GREY),
        *[VGroup(Line([x,-2.58,0],[x,-2.73,0],color=GREY),T(s,26,GREY).move_to([x,-3,0])) for x,s in [(-4.5,'0'),(.55,'32 ms' if vib else '0.9 s'),(5.6,'64 ms' if vib else '1.8 s')]],
        T('Illustrative firing records',26,GREY).move_to([0,-3.5,0]))


def record(modes=(None,None,None)):
    return VGroup(position(),phase_labels(),*[raster(i,m) for i,m in enumerate(modes)],timebar())


def hold_band():
    return Rectangle(width=10.1/1.8,height=4.65,stroke_width=0,fill_color=GOLD,fill_opacity=.10).move_to([.55,.025,0]).set_z_index(-1)


def predict():
    return VGroup(record(),hold_band(),heading('Which one keeps firing?'))


def vibration():
    return curve([[-4.5+10.1*t/.064,1.6+.28*t/.064*np.sin(2*PI*250*t),0] for t in np.linspace(0,.064,1000)],TEXT,3)


def vib_record(answer=False):
    return VGroup(vibration(),T('250 Hz • growing vibration',26,TEXT).move_to([0,2.3,0]),
        *[raster(i,'vibration' if answer and i==2 else None) for i in range(3)],timebar(True))


def vib_question():
    return VGroup(vib_record(),heading('Who detects the smallest vibration?'))


def table():
    cells=VGroup()
    for j,y in enumerate((1.1,-1.65)):
        for i,x in enumerate((-1.8,3.15)):
            box=RoundedRectangle(width=4.65,height=2.35,corner_radius=.15,color=GREY,fill_color=GREY,fill_opacity=.07).move_to([x,y,0])
            cells.add(VGroup(box,T(('SA I','SA II','RA','PC')[j*2+i],34).move_to(box)))
    labels=VGroup(T('Small field',28,GREY).move_to([-1.8,2.7,0]),T('Large field',28,GREY).move_to([3.15,2.7,0]),
        T('Slowly\nadapting',26,GREY,line_spacing=1).move_to([-5.3,1.1,0]),T('Rapidly\nadapting',26,GREY,line_spacing=1).move_to([-5.3,-1.65,0]))
    return VGroup(cells,labels).shift(RIGHT*.2+DOWN*.1)


def skin_probe():
    skin=RoundedRectangle(width=9,height=2,corner_radius=.9,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([0,-.8,0])
    probe=RoundedRectangle(width=2.2,height=2.7,corner_radius=.2,color=TEXT,fill_color=TEXT,fill_opacity=.12).move_to([0,1.5,0])
    labels=VGroup(T('probe',28).move_to([2.7,1.6,0]),Line([1.2,1.6,0],[2,1.6,0],color=GREY),
        T('fingertip',28,GREY).move_to([0,-2.3,0]))
    return VGroup(skin,probe,labels)


def sensitivity(i,f):
    if i==0: return 1/(1+(f/8)**1.3)
    return np.exp(-.5*(np.log10(np.maximum(f,.01)/(25 if i==1 else 250))/(.6 if i==1 else .42))**2)


def bands():
    ax=Axes(x_range=[-1,3,1],y_range=[0,1.15,.5],x_length=9.9,y_length=4.6,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([.75,-.15,0])
    labs=VGroup(T('relative sensitivity',26,GREY).rotate(PI/2).move_to([-5.65,-.05,0]),
        T('static\n0 Hz',26,GREY).move_to(ax.c2p(-1,0)+DOWN*.55),
        T('increasing vibration frequency →',26,GREY).move_to([1.8,-2.95,0]),
        T('Schematic • peaks and widths not to scale',26,GREY).move_to([0,-3.5,0]))
    lines=VGroup(*[curve([ax.c2p(x,sensitivity(i,10**x)) for x in np.linspace(-1,3,400)],COL[i]) for i in range(3)])
    labels=VGroup(*[T(s,28,c).move_to(ax.c2p(x,1.08)) for s,c,x in [('SA I',TEAL,-.75),('RA',BLUE,1.4),('PC',GREY,2.4)]])
    # Break between static indentation and the logarithmic vibration axis.
    labs.add(T('//',26,GREY).move_to(ax.c2p(-.48,0)))
    axes=VGroup(Line(ax.c2p(-1,0),ax.c2p(3,0),color=GREY),Line(ax.c2p(-1,0),ax.c2p(-1,1.15),color=GREY))
    return VGroup(axes,labs,lines,labels)


class S00Title(TitleCard):
    TITLE='One Press, Several Reports'
    LESSON='The Low-Threshold Mechanoreceptors: One Touch, Several Signals'
    finish=exact_finish
    def construct(self):
        self.add(T('BIOCHEMISTRYPEDIA',26,TEAL).move_to([0,2.1,0]),
            T('The Low-Threshold Mechanoreceptors:\nOne Touch, Several Signals',26,GREY,line_spacing=1,should_center=True).move_to([0,.85,0]))
        self.play(FadeIn(T(self.TITLE,44,font=TITLE_FONT).move_to([0,-.65,0])),run_time=.45)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        g=skin_probe(); self.add(g,heading('One press, several reports'))
        self.at('Press a fingertip'); self.play(g[1].animate.shift(DOWN*.4),run_time=.6)
        self.at('Is that one signal'); self.play(FadeIn(T('One signal — or several?',32,GOLD).move_to([0,-3.2,0])),run_time=.4); self.finish()


class S02Recall(SpokenScene):
    def construct(self):
        self.add(table(),heading('What you already know: firing'))
        self.at('You used firing alone'); self.play(Indicate(self.mobjects[0],color=GOLD,scale_factor=1.015),run_time=.5); self.finish()


class S03Ask(SpokenScene):
    def construct(self):
        g=table(); self.add(g,heading('What lies behind each box?'))
        self.at('So what lies'); self.play(*[Transform(c[1],T('?',46,GOLD).move_to(c[0])) for c in g[0]],run_time=.4)
        self.at('And why split'); self.play(Transform(self.mobjects[1],heading('Why several signals for one touch?')),run_time=.4); self.finish()


class S04Setup(SpokenScene):
    def construct(self):
        # The time trace begins directly below the enlarged physical probe.
        skin=RoundedRectangle(width=5.2,height=1.65,corner_radius=.7,color=GREY,
            fill_color=GREY,fill_opacity=.15).move_to([-3.8,0,0])
        probe=RoundedRectangle(width=2.2,height=1.9,corner_radius=.2,color=TEXT,
            fill_color=TEXT,fill_opacity=.12).move_to([-3.8,1.8,0])
        self.add(skin,probe,heading('Press → hold → lift'),
            T('probe',30).move_to([-.9,1.8,0]),
            Line([-2.6,1.8,0],[-1.8,1.8,0],color=GREY),
            T('fingertip',30,GREY).move_to([-3.8,-1.25,0]),
            DashedLine([-3.8,-1.55,0],[-3.8,-2.2,0],color=GREY))
        def part(a,b):
            return curve([[-3.8+9.4*t/1.8,-2.25+1.1*ramp(t),0]
                for t in np.linspace(a,b,100)],TEXT,6)
        self.at('presses into'); self.play(probe.animate.shift(DOWN*.45),
            Create(part(0,.4)),FadeIn(T('press',30,GREY).move_to([-2.7,-3.05,0])),run_time=.65)
        self.at('holds still'); self.play(Create(part(.4,1.4)),
            FadeIn(T('hold • 1 s',30,GREY).move_to([.9,-3.05,0])),run_time=.6)
        self.at('then lifts'); self.play(probe.animate.shift(UP*.45),
            Create(part(1.4,1.8)),FadeIn(T('lift',30,GREY).move_to([4.6,-3.05,0])),run_time=.45)
        self.wait(2)
        self.finish()


class S05Record(SpokenScene):
    def construct(self):
        g=record(); self.add(g[0],g[1],g[5],heading('One probe • three records'))
        self.at('Record from each kind'); self.play(LaggedStart(*[FadeIn(r) for r in g[2:5]],lag_ratio=.2),run_time=.8); self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        self.add(predict()); self.at('while the probe'); self.play(Indicate(hold_band(),scale_factor=1),run_time=.5); self.finish()


def countdown(scene,g):
    scene.camera.background_color=BG; scene.add(g)
    track=Line([-1.6,-3.78,0],[1.6,-3.78,0],color=GREY,stroke_width=5)
    bar=Line(track.get_start(),track.get_end(),color=GOLD,stroke_width=5)
    scene.add(track,bar); scene.play(bar.animate.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*.005),run_time=5,rate_func=linear)


class S07Pause(Scene):
    def construct(self): countdown(self,predict())


class S08Sa(SpokenScene):
    def construct(self):
        self.add(record(),heading('Slowly adapting • Merkel cells'))
        r=raster(0,'steady')[2]
        self.at('It fires going in'); self.play(Create(r[:2]),run_time=.4)
        self.at('keeps firing through'); self.play(Create(r[2:]),run_time=.7); self.finish()


class S09Sa2(SpokenScene):
    def construct(self):
        self.add(heading('Presence and edges'))
        disc=Circle(radius=2.1,color=TEAL,stroke_width=5).move_to([-2,0,0])
        dots=VGroup(*[Dot(disc.point_at_angle(a),radius=.09,color=GOLD) for a in np.linspace(0,TAU,12,endpoint=False)])
        self.add(disc,T('Contact disc',28,TEAL).move_to([-2,-2.8,0]))
        r=raster(0,'steady'); r.remove(r[1]); r.scale(.5).move_to([3,-.1,0]); self.add(r,T('SA I • held press',28,TEAL).move_to([3,1,0]))
        self.at('where its edges'); self.play(FadeIn(dots),FadeIn(T('edges',30,GOLD).move_to([-4.7,1.8,0])),Create(Line([-4.05,1.65,0],[-3.2,1.05,0],color=GOLD)),run_time=.4); self.finish()


class S10Ra(SpokenScene):
    def construct(self):
        self.add(record(('steady',None,None)),heading('Rapidly adapting • Meissner corpuscle'))
        r=raster(1,'burst')[2]; half=len(r)//2
        self.at('fires going in'); self.play(Create(r[:half]),run_time=.4)
        self.at('and again on'); self.play(Create(r[half:]),run_time=.4)
        self.at('During the hold'); self.play(FadeIn(hold_band()),run_time=.3); self.finish()


class S11Pc(SpokenScene):
    def construct(self):
        self.add(record(('steady','burst',None)),heading('Pacinian'))
        self.at('is silent during'); self.play(FadeIn(hold_band()),run_time=.3)
        self.at('a brief burst'); self.play(Create(raster(2,'brief')[2]),run_time=.5); self.finish()


class S12Predict2(SpokenScene):
    def construct(self):
        self.add(vib_record(),heading('Tiny, fast probe movements'))
        self.at('which afferent detects'); self.play(Transform(self.mobjects[1],heading('Who detects the smallest vibration?')),run_time=.3); self.finish()


class S13Pause(Scene):
    def construct(self): countdown(self,vib_question())


class S14PcReveal(SpokenScene):
    def construct(self):
        self.add(vib_record(),heading('Pacinian • best near 100–300 Hz'))
        self.at('The'); self.play(Create(raster(2,'vibration')[2]),run_time=.55)
        self.at('The slowly adapting'); self.play(Indicate(raster(0)[0],color=TEAL,scale_factor=1.01),run_time=.5); self.finish()


class S15Bands(SpokenScene):
    def construct(self):
        g=bands(); self.add(g[0],g[1],heading('Bands overlap'))
        self.at('Each class has'); self.play(LaggedStart(*[AnimationGroup(Create(g[2][i]),FadeIn(g[3][i])) for i in range(3)],lag_ratio=.3),run_time=1.5)
        self.at('not a cutoff'); self.play(Indicate(g[2],color=GOLD,scale_factor=1.01),run_time=.5); self.finish()


class S16Same(SpokenScene):
    def construct(self):
        self.add(record(('steady','burst','brief')),heading('One probe • three records'))
        self.at('different records'); self.play(*[Indicate(raster(i,m)[2],color=COL[i],scale_factor=1.02) for i,m in enumerate(('steady','burst','brief'))],run_time=.6); self.finish()


class S17Idea(SpokenScene):
    def construct(self):
        card=RoundedRectangle(width=11.8,height=5.9,corner_radius=.3,color=GOLD,fill_color=GOLD,fill_opacity=.06)
        self.add(card,T('The one idea',32,GOLD).move_to([0,2,0]),T('Each LTMR class is\nmost sensitive to a different\npart of a touch.',57,line_spacing=1.3,should_center=True).move_to([0,-.1,0]))
        self.at('is most sensitive'); self.play(card.animate.set_stroke(width=5),run_time=.4); self.finish()


def stimulus(i):
    # Large individual beat; the whole panel is replaced on each named stimulus.
    c=[TEAL,BLUE,GREY,YELLOW,ORANGE][i]
    box=RoundedRectangle(width=10.8,height=5.5,corner_radius=.25,color=c,fill_color=c,fill_opacity=.04).move_to([0,-.25,0])
    skin=Line([-4,-1.2,0],[4,-1.2,0],color=GREY,stroke_width=5)
    if i in (0,1):
        icon=RoundedRectangle(width=1.6,height=2,corner_radius=.18,color=c,fill_color=c,fill_opacity=.2).move_to([0,-.1,0])
        action=Arrow([0,1.7,0],[0,.9,0],color=c,buff=0) if i==0 else Arrow([-2,1.4,0],[2,1.4,0],color=c,buff=0)
    elif i==2:
        icon=curve([[-4+8*t,.1+.5*np.sin(2*PI*8*t),0] for t in np.linspace(0,1,500)],c)
        action=T('fast oscillation',28,c).move_to([0,1.5,0])
    elif i==3:
        icon=curve([[0,-1.2,0],[0,0,0],[.3,1,0],[1,1.8,0]],c,7)
        action=Arrow([-.8,1.3,0],[.4,1.3,0],color=c,buff=0)
    else:
        icon=VGroup(Rectangle(width=2.7,height=.6,color=c,fill_color=c,fill_opacity=.2).move_to([0,.2,0]),*[Line([x,-.1,0],[x,-1.05,0],color=c,stroke_width=4) for x in np.linspace(-1.2,1.2,7)])
        action=Arrow([-2.5,1.4,0],[2.5,1.4,0],color=c,buff=0)
    label=T(['held press','skin motion','fast vibration','hair bend','slow stroke'][i],34,c).move_to([0,-2.25,0])
    return VGroup(box,skin,icon,action,label)


class S18Filter(SpokenScene):
    def construct(self):
        self.add(heading('Overlapping filters'))
        intro=bands(); self.add(intro)
        # Preview the first stimulus as the general filter sentence ends.
        self.at('each class favors',lead=.05)
        self.remove(intro); preview=stimulus(0); self.add(preview)
        for i,cue in enumerate(('A held press','skin motion','fast vibration','the slightest bend','A slow stroke')):
            self.at(cue); g=stimulus(i)
            self.remove(preview if i==0 else prev); self.add(g)
            if i in (1,4): self.play(g[2].animate.shift(RIGHT*.7),run_time=.5)
            elif i==0: self.play(g[2].animate.shift(DOWN*.18),run_time=.5)
            elif i==3: self.play(Rotate(g[2],-.12,about_point=[0,-1.2,0]),run_time=.5)
            else: self.play(Indicate(g[2],scale_factor=1.04),run_time=.5)
            prev=g
        self.finish()


def neuron(c,x,y):
    # Branched sensory ending, continuous axon and a large cell body.
    return VGroup(*[Line([x+d,y+.6,0],[x,y+.1,0],color=c,stroke_width=3) for d in (-.4,0,.4)],
        Line([x,y+.1,0],[x,y-.45,0],color=c,stroke_width=4),Circle(radius=.24,color=c,fill_color=c,fill_opacity=.25).move_to([x,y-.65,0]))


def axons():
    g=VGroup()
    for y,c,n,w,length,tag in ((1.45,BLUE,'Aβ',11,3.1,'faster'),(-.15,YELLOW,'Aδ',6,1.9,'intermediate'),(-1.75,ORANGE,'C',3,.65,'slower')):
        line=Line([-3.9,y,0],[.8,y,0],color=c,stroke_width=w)
        sheaths=VGroup(*[RoundedRectangle(width=.65,height=.43 if n=='Aβ' else .27,corner_radius=.08,color=c,fill_color=c,fill_opacity=.3).move_to([x,y,0]) for x in np.arange(-3.4,.8,1)]) if n!='C' else VGroup()
        g.add(VGroup(T(n,30,c).move_to([-5,y,0]),line,sheaths,Arrow([1.3,y,0],[1.3+length,y,0],color=c,buff=0),T(tag,26,c).move_to([3,y-.45,0])))
    return g


class S19Ending(SpokenScene):
    def construct(self):
        self.add(heading('Ending + neuron shape the response'))
        labels=VGroup(*[T(s,26,c,should_center=True).move_to([x,2.2,0]) for x,s,c in zip((-5,-2.5,0,2.5,5),('held\npress','skin\nmotion','fast\nvibration','hair\nbend','slow\nstroke'),(TEAL,BLUE,GREY,YELLOW,ORANGE))])
        icons=VGroup(*[stimulus(i)[2].copy().scale(.22).move_to([-5+2.5*i,1.25,0]) for i in range(5)])
        cells=VGroup(*[neuron(c,-5+2.5*i,-.2) for i,c in enumerate((TEAL,BLUE,GREY,YELLOW,ORANGE))])
        tag=T("Ending + neuron's own properties\nshape the response",30,GOLD,should_center=True).move_to([0,-2.2,0])
        self.add(labels,icons,cells,tag)
        self.at('with the'); self.play(*[Indicate(n,scale_factor=1.08) for n in cells],run_time=.65)
        self.at('Axon size and myelin'); self.remove(labels,icons,cells,tag,self.mobjects[0]); self.add(heading('Axon size + myelin → travel speed'),axons(),T('Relative speed, schematic',26,GREY).move_to([0,-3.4,0])); self.finish()


def comparison_panel(x,pc=False):
    c=GREY if pc else TEAL
    panel=RoundedRectangle(width=5.8,height=5.9,corner_radius=.2,color=c).move_to([x,-.2,0])
    label=T('PC • tiny vibration' if pc else 'SA I • held press',29,c).move_to([x,2.1,0])
    # Both rows share a normalized time axis, including stimulus onset/offset.
    ts=np.linspace(0,1,700)
    onset,offset=.16,.84
    def drive(t):
        if pc:
            return .11*np.sin(2*PI*18*(t-onset)) if onset<=t<=offset else 0
        return .65*np.interp(t,[0,onset,onset+.10,offset-.10,offset,1],[0,0,1,1,0,0])
    stim=curve([[x-2.35+4.7*t,.7+drive(t),0] for t in ts],TEXT,3)
    base=Line([x-2.35,-1.1,0],[x+2.35,-1.1,0],color=c)
    # SA I begins at the press edge, then adapts to a lower sustained rate.
    times=onset+np.arange(1,13)/18 if pc else np.r_[onset,onset+.035,onset+.08,np.arange(onset+.17,offset-.07,.085)]
    spikes=VGroup(*[Line([x-2.35+4.7*t,-1.1,0],[x-2.35+4.7*t,-.5,0],color=c,stroke_width=3) for t in times])
    edge=DashedLine([x-2.35+4.7*onset,1.4,0],[x-2.35+4.7*onset,-1.4,0],color=c,stroke_opacity=.45)
    return VGroup(panel,label,stim,base,spikes,edge,T('Response • schematic',26,GREY).move_to([x,-2.2,0]))


class S20Why(SpokenScene):
    def construct(self):
        a,b=comparison_panel(-3.15),comparison_panel(3.15,True)
        self.add(heading('Complementary reports'),a,b)
        self.at('One keeps reporting'); self.play(Indicate(a[4],color=TEAL,scale_factor=1.03),run_time=.6)
        self.at('Another catches fast'); self.play(Indicate(b[2:5],color=GREY,scale_factor=1.03),run_time=.6); self.finish()


class S21Pattern(SpokenScene):
    def construct(self):
        g=record(('steady','burst','brief')).stretch(.76,0).shift(LEFT*.9)
        self.add(g,heading('No class reports the whole touch'))
        self.at('reads the pattern')
        brace=Brace(VGroup(*g[2:5]),RIGHT,buff=.12,color=GOLD)
        label=T('pattern\nacross\nclasses',28,GOLD,should_center=True).next_to(brace,RIGHT,buff=.2)
        self.play(Create(brace),FadeIn(label),*[Indicate(r[2],color=COL[i],scale_factor=1.04) for i,r in enumerate(g[2:5])],run_time=1)
        self.finish()


class S22Rule(SpokenScene):
    def construct(self):
        g=table(); self.add(g,heading('Endings help shape the report'))
        self.at('Endings help decide'); endings=VGroup()
        for i,(cell,name,c) in enumerate(zip(g[0],('Merkel cells','ending not settled','Meissner','Pacinian'),(TEAL,GREY,BLUE,GREY))):
            center=cell[0].get_center(); cell[1].shift(UP*.65)
            lab=T(name,26,c).move_to(center+DOWN*.65)
            if i==0: glyph=VGroup(*[Dot(center+np.array([d,0,0]),radius=.12,color=c) for d in (-.45,0,.45)])
            elif i==1: glyph=T('?',32,c).move_to(center)
            elif i==2:
                glyph=VGroup(*[Ellipse(width=1.1,height=.17,color=c,stroke_width=4).move_to(center+UP*d) for d in (-.28,-.14,0,.14,.28)])
            else: glyph=VGroup(*[Ellipse(width=w,height=w*.45,color=c,stroke_width=4).move_to(center) for w in (.65,1,1.4)])
            endings.add(VGroup(glyph,lab))
        self.play(FadeIn(endings),run_time=.5); self.finish()


def hair_scene():
    skin=Line([-5.3,.9,0],[5.3,.9,0],color=GREY,stroke_width=4)
    sheath=RoundedRectangle(width=1.8,height=3.8,corner_radius=.7,color=GREY,stroke_width=6,fill_color=GREY,fill_opacity=.12).move_to([0,-.9,0])
    hair=curve([[0,-2.6,0],[0,.8,0],[.15,2,0],[.5,2.7,0]],GREY,10)
    return VGroup(skin,sheath,hair)


def hair_ending(i):
    c=[BLUE,YELLOW,ORANGE][i]; x=-.65+i*.65
    # Offset longitudinal terminals beside a common shaft, with separate axons.
    terminals=VGroup(*[Line([x+d,-1.6,0],[x+d,.45,0],color=c,stroke_width=6) for d in (-.12,0,.12)])
    side=-1 if i<2 else 1; y=(-1.3,-2.2,-2.8)[i]
    axon=curve([[x,-1.6,0],[x,y,0],[side*2.5,y,0],[side*3.3,y+.25,0]],c,6)
    lab=T(['Aβ RA','Aδ','C'][i],30,c).next_to(axon,LEFT if side<0 else RIGHT,buff=.18).set_y(y+.25)
    return VGroup(terminals,axon,lab)


class S23Takeaway(SpokenScene):
    def construct(self):
        self.add(hair_scene(),heading('Next: mouse hairy skin'))
        self.at('Next'); self.play(FadeIn(hair_ending(0)),run_time=.35)
        self.at('where three classes'); self.play(FadeIn(hair_ending(1)),run_time=.35)
        self.at('can share'); self.play(FadeIn(hair_ending(2)),run_time=.35); self.finish()


class S24End(EndCard):
    LINE='Each class favours a different part of a touch.'
    def construct(self):
        # Direct crossfade from the final hair diagram, then 3.6 s reading time.
        previous=VGroup(hair_scene(),heading('Next: mouse hairy skin'),*[hair_ending(i) for i in range(3)])
        card=VGroup(T('Each class favours\na different part of a touch.',42,font=TITLE_FONT,should_center=True,line_spacing=1.2),
            T('No class reports the whole touch.',28,GREY).move_to([0,-1.65,0]),T('biochemistrypedia.com',26,TEAL).move_to([0,-2.6,0]))
        self.add(previous)
        self.play(FadeOut(previous),FadeIn(card),run_time=.4)
        self.finish()
    def finish(self):
        self.wait(3.6)
