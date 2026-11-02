"""Blips from a Silent Nerve — reviewed animation.

COLOR MAP: BLUE = motor axon / terminal; YELLOW = ACh only;
CALCIUM (violet) = Ca²⁺; PINK = receptors; GREEN = recorded voltage,
miniature and evoked EPP; ORANGE = firing threshold; GREY = neutral anatomy,
axes, vesicle membrane, and question panels. TEXT = explanatory text.
Every trace is a sum of the reference difference-of-exponentials model.
All amplitudes, timing and the illustrative integer count are schematic.
"""
import numpy as np
from bp_style import *

CALCIUM = '#B58CD9'
PINK = '#E88FC0'
ORANGE = '#F29E4C'
UNIT_HEIGHT = .6
AXIS_TEXT = TEXT

def label(s, x, y, color=TEXT, size=28):
    return T(s, size=size, color=color).move_to([x,y,0])

def arrow(a,b,color=GREY):
    return Arrow(a,b,buff=.06,color=color,stroke_width=4)

def leader(text, pos, end, color=TEXT, size=28):
    t=label(text,*pos,color,size)
    start=t.get_left() if end[0]<pos[0] else t.get_right()
    return VGroup(t,Line(start,end,color=color,stroke_width=2))

_F=lambda t: np.exp(-t/.22)-np.exp(-t/.04)
_PEAK=max(_F(t) for t in np.linspace(.001,1,1000))

def blip_y(x,onset,h):
    dt=x-onset
    return 0 if dt<0 else h*_F(dt)/_PEAK

def trace_from(events,x0=-5.15,x1=5.8,base=-2.55,dx=.012):
    xs=np.arange(x0,x1+dx/2,dx)
    m=VMobject(stroke_color=GREEN,stroke_width=4)
    m.set_points_as_corners([[x,base+sum(blip_y(x,t,h) for t,h in events),0] for x in xs])
    return m

BLIPS=[(-4.65,2.1),(-2.95,2.02),(-1.45,2.18),(.25,2.1),(2.15,2.0),(4.45,2.14)]

class Junction:
    """Fixed geometry throughout the relay; continuous axon-terminal outline."""
    def __init__(self,receptors=True):
        p=VMobject(stroke_color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=.12)
        p.start_new_path(np.array([-6,2.25,0])); p.add_line_to(np.array([-1.8,2.25,0]))
        p.add_cubic_bezier_curve_to(np.array([-1.4,2.9,0]),np.array([2.8,2.9,0]),np.array([3,2.0,0]))
        p.add_cubic_bezier_curve_to(np.array([3.2,1.5,0]),np.array([3.1,.65,0]),np.array([2.6,.65,0]))
        p.add_line_to(np.array([-1.2,.65,0]))
        p.add_cubic_bezier_curve_to(np.array([-1.8,.65,0]),np.array([-1.8,1.4,0]),np.array([-1.9,1.65,0]))
        p.add_line_to(np.array([-6,1.65,0])); p.close_path()
        self.term=p
        self.cleft=Rectangle(width=5.7,height=1.35,stroke_opacity=0,fill_color=GREY,fill_opacity=.08).move_to([.7,-.025,0])
        self.muscle=RoundedRectangle(width=12,height=1.65,corner_radius=.14,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([0,-1.525,0])
        self.receptors=VGroup(*[VGroup(*[Rectangle(width=.12,height=.42,color=PINK,fill_color=PINK,fill_opacity=.45).move_to([x+d,-.72,0]) for d in (-.14,.14)]) for x in (-.9,.7,2.3)]) if receptors else VGroup()
        self.patch=Line([-1.55,-.7,0],[2.95,-.7,0],color=GREEN,stroke_width=7)
        self.labels=VGroup(label('motor nerve',-4.25,2.72,BLUE,28),label('skeletal muscle fibre',-.2,-1.85,GREY,28))
        self.body=VGroup(self.cleft,self.term,self.muscle,self.receptors)
        self.all=VGroup(self.body,self.labels)

def contact_label():
    bracket=VGroup(Line([3.3,.65,0],[3.55,.65,0],color=TEXT),Line([3.55,.65,0],[3.55,-.7,0],color=TEXT),Line([3.3,-.7,0],[3.55,-.7,0],color=TEXT))
    return VGroup(bracket,leader('synapse',(4.8,1.05),[3.55,.1,0]))

def relay_slots(n=0):
    g=VGroup()
    for i,s in enumerate(('spike','Ca²⁺','fuse','cross','open')):
        c=TEXT if i<n else GREY
        r=RoundedRectangle(width=2.12,height=.7,corner_radius=.12,color=c,fill_color=c,fill_opacity=.16 if i<n else .025)
        g.add(VGroup(r,T(f'{i+1}  {s}',size=27,color=c).move_to(r)))
    return g.arrange(RIGHT,buff=.19).move_to([0,-3.12,0])

def relay_scene(scene,n,title):
    j=Junction(); slots=relay_slots(n)
    scene.add(j.all,slots,label(title,0,3.32,TEXT,31))
    return j,slots

def electrode(tip=(-2,2.45)):
    x,y=tip
    return VGroup(Line([x-1.55,y+1.0,0],[x,y,0],color=TEXT,stroke_width=5),Line([x-1.3,y+1.08,0],[x,y,0],color=TEXT,stroke_width=5))

def recording_stage(away=False):
    # Wide picture-in-picture strip: a legible electrode inside a continuous fibre.
    fibre=RoundedRectangle(width=11.3,height=.65,corner_radius=.09,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([.25,2.55,0])
    terminal=RoundedRectangle(width=1.8,height=.65,corner_radius=.22,color=BLUE,fill_color=BLUE,fill_opacity=.16).move_to([-2.05,3.2,0])
    axon=Line([-5.4,3.3,0],[-2.95,3.3,0],color=BLUE,stroke_width=6)
    patch=Line([-2.95,2.875,0],[-1.15,2.875,0],color=GREEN,stroke_width=6)
    e=electrode((3.5 if away else -2,2.45))
    end=VGroup(label('endplate',-4.25,2.58,GREEN,26),Line([-3.55,2.6,0],[-2.65,2.84,0],color=GREEN,stroke_width=2))
    return VGroup(fibre,terminal,axon,patch,e,end),e,terminal

def axes():
    return VGroup(Line([-5.35,-3.0,0],[-5.35,2.3,0],color=GREY,stroke_width=2),Line([-5.35,-3.0,0],[5.95,-3.0,0],color=GREY,stroke_width=2),label('voltage (mV)',-5.78,-.35,AXIS_TEXT,26).rotate(PI/2),label('time (s)',5.05,-3.48,AXIS_TEXT,26),label('schematic, not to scale',.3,-3.48,AXIS_TEXT,26))

def recording(scene,events=BLIPS,away=False):
    st,e,term=recording_stage(away); tr=trace_from(events)
    scene.add(st,axes(),tr)
    return st,e,term,tr

def stimulator():
    box=Rectangle(width=.85,height=.42,color=GREY).move_to([-4.6,3.58,0])
    cross=VGroup(Line([-5.05,3.43,0],[-4.15,3.78,0],color=RED,stroke_width=4),Line([-5.05,3.78,0],[-4.15,3.43,0],color=RED,stroke_width=4))
    wire=Line([-4.6,3.37,0],[-4.6,3.3,0],color=GREY,stroke_width=3)
    return VGroup(box,cross,wire,label('no stimulation',2.8,3.32,GREY,28))

def comparison():
    # Shared unit height; the large response is schematic, with no claimed count.
    sm=trace_from([(-4.85,UNIT_HEIGHT)],x0=-5.4,x1=-1.35,base=-1.9)
    big=trace_from([(1.8,6*UNIT_HEIGHT)],x0=1.25,x1=5.75,base=-1.9)
    labs=VGroup(label('miniature',-3.55,-2.35,GREEN),label('evoked response',3.6,-2.35,GREEN))
    return sm,big,labs

def comparison_axes():
    scale=VGroup(Line([5.65,-1.9,0],[5.65,-1.9+UNIT_HEIGHT,0],color=TEXT),Line([5.49,-1.9,0],[5.81,-1.9,0],color=TEXT),Line([5.49,-1.9+UNIT_HEIGHT,0],[5.81,-1.9+UNIT_HEIGHT,0],color=TEXT),label('1 unit',5.65,-.98,TEXT,26))
    return VGroup(Line([-5.7,-2.0,0],[-5.7,2.0,0],color=GREY),Line([-5.7,-2.0,0],[6.05,-2.0,0],color=GREY),label('voltage (mV)',-6.08,0,AXIS_TEXT,26).rotate(PI/2),label('time (s)',4.9,-3.25,AXIS_TEXT,26),label('schematic, not to scale',.3,-3.48,AXIS_TEXT,26),scale)

def unit_row():
    # Several examples + ellipsis: these are not falsely asserted to be three quanta.
    return VGroup(*[trace_from([(0,UNIT_HEIGHT)],x0=-.15,x1=1.05,base=0).move_to([x,-1.15,0]) for x in (-4.8,-3.55,-2.3)],label('…',-1.35,-1.25,GREEN,40))

def unit_stack():
    # Explicit illustration only: each block shares the miniature/scale height.
    return VGroup(*[Rectangle(width=.55,height=UNIT_HEIGHT,color=GREEN,fill_color=GREEN,fill_opacity=.14).move_to([.7,-1.9+UNIT_HEIGHT*(i+.5),0]) for i in range(6)])

def puzzle():
    _,big,labs=comparison(); labs[0].become(label('miniatures',-3.55,-2.35,GREEN))
    return VGroup(unit_row(),big,labs,label('Built from blips like these?',0,2.9,TEXT,36),comparison_axes()),label('?',-.35,.15,TEXT,66)

class S00Title(TitleCard):
    TITLE='Blips from a Silent Nerve'
    LESSON='Synaptic Transmission and Quantal Release'
    def construct(self):
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),T(self.TITLE,48,font=TITLE_FONT),Line(LEFT*1.3,RIGHT*1.3,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.6); self.finish()

class S01Question(SpokenScene):
    def construct(self):
        j=Junction(False); self.add(j.all)
        self.at('How does a nerve')
        q=label('How does a nerve hand a signal to a muscle?',0,3.35,TEXT,30)
        self.play(FadeIn(q),run_time=.3)
        pulse=Dot([-5.7,1.95,0],radius=.11,color=BLUE)
        self.add(pulse); self.play(pulse.animate.move_to([.7,1.7,0]),run_time=1.1)
        self.at('what is that')
        self.play(FadeIn(label('And what is that signal made of?',0,-3.15,TEXT,32)),run_time=.4)
        self.finish()

class S02Synapse(SpokenScene):
    def construct(self):
        j=Junction(False); self.add(j.all)
        self.at('A synapse')
        # A modest zoom into the contact, settling back on the common relay geometry.
        j.all.scale(.84)
        self.play(j.all.animate.scale(1/.84),FadeIn(contact_label()),run_time=.8)
        self.at('passes a signal')
        self.play(Indicate(j.term,color=BLUE,scale_factor=1.015),run_time=.65)
        self.finish()

class S03Chemical(SpokenScene):
    def construct(self):
        j=Junction(); self.add(j.all)
        self.at('At a chemical synapse')
        self.play(FadeIn(label('chemical synapse',0,3.35,TEXT,32)),run_time=.35)
        self.at('the terminal releases')
        p=Dot([.7,.8,0],radius=.1,color=YELLOW)
        self.play(FadeIn(p),FadeIn(label('terminal',.7,1.75,BLUE)),run_time=.4)
        self.at('It crosses a gap')
        self.play(p.animate.move_to([.7,-.25,0]),FadeIn(leader('cleft',(4.75,.05),[2.95,.05,0],GREY)),run_time=.8)
        self.at('acts on receptors')
        self.play(p.animate.move_to([.7,-.53,0]),FadeIn(leader('receptors',(4.7,-1.05),[2.45,-.8,0],PINK)),run_time=.55)
        self.finish()

class S04Nmj(SpokenScene):
    def construct(self):
        j=Junction(); self.add(j.all)
        self.at('The best studied example')
        self.play(FadeIn(label('the neuromuscular junction',0,3.35,TEXT,34)),run_time=.4)
        self.at('between a motor nerve')
        self.play(Indicate(j.labels[0],scale_factor=1.03,color=BLUE),run_time=.5)
        self.at('and a skeletal muscle')
        self.play(Indicate(j.labels[1],scale_factor=1.03,color=GREY),run_time=.5)
        self.finish()

class S05Relay(SpokenScene):
    def construct(self):
        j=Junction(); self.add(j.all)
        self.at('The signal crosses')
        self.play(FadeIn(label('A relay of five steps',0,3.35,TEXT,32)),run_time=.35)
        self.at('five steps')
        self.play(LaggedStart(*[FadeIn(s) for s in relay_slots()],lag_ratio=.1),run_time=.7)
        self.finish()

class S06Step1(SpokenScene):
    def construct(self):
        j=Junction(); self.add(j.all,relay_slots(1))
        spike=VMobject(color=BLUE,stroke_width=6).set_points_as_corners([[-5.7,1.9,0],[-5.5,1.9,0],[-5.35,2.25,0],[-5.2,1.68,0],[-5.05,1.9,0]])
        self.at('First'); self.add(spike)
        self.at('an action potential')
        self.play(FadeIn(label('1  Spike arrives',0,3.35,TEXT,32)),spike.animate.shift(RIGHT*5.8),run_time=.85)
        self.at('at the nerve terminal')
        self.play(Indicate(spike,scale_factor=1.08,color=BLUE),run_time=.4)
        self.finish()

class S07Step2(SpokenScene):
    def construct(self):
        j,slots=relay_scene(self,2,'2  Calcium in')
        # Membrane breaks and two rails show the route through each channel.
        channels=VGroup(*[VGroup(Line([x-.15,.65,0],[x+.15,.65,0],color=BG,stroke_width=10),Line([x-.16,.48,0],[x-.16,.82,0],color=CALCIUM,stroke_width=4),Line([x+.16,.48,0],[x+.16,.82,0],color=CALCIUM,stroke_width=4)) for x in (-.7,.7,2.1)])
        ions=VGroup(*[Dot([x,-.1,0],radius=.09,color=CALCIUM) for x in (-.7,.7,2.1)])
        self.at('Second'); self.add(channels)
        self.at('calcium flows')
        self.play(FadeIn(ions),FadeIn(chip('Ca²⁺',CALCIUM,28).move_to([4.5,.75,0])),run_time=.25)
        self.play(ions.animate.shift(UP*1.4),run_time=.7)
        self.finish()

class S08Step3(SpokenScene):
    def construct(self):
        j,slots=relay_scene(self,3,'3  Vesicles fuse → ACh released')
        xs=(-.9,.7,2.3)
        ves=VGroup(*[Circle(radius=.32,color=GREY,stroke_width=3).move_to([x,.99,0]) for x in xs])
        cargo=VGroup(*[Dot([x+d,.99,0],radius=.06,color=YELLOW) for x in xs for d in (-.12,.04,.15)])
        self.add(ves,cargo)
        self.at('vesicles fuse')
        cups=VGroup(*[Arc(radius=.32,start_angle=0,angle=PI,color=GREY,stroke_width=3).move_to([x,.81,0]) for x in xs])
        gaps=VGroup(*[Line([x-.28,.65,0],[x+.28,.65,0],color=BG,stroke_width=9) for x in xs])
        self.add(gaps); self.play(ReplacementTransform(ves,cups),cargo.animate.shift(DOWN*.17),run_time=.55)
        self.at('release their transmitter')
        self.play(cargo.animate.shift(DOWN*.48),run_time=.65)
        self.at('acetylcholine')
        self.play(FadeIn(chip('ACh',YELLOW,28).move_to([4.6,.7,0])),run_time=.3)
        self.finish()

class S09Step4(SpokenScene):
    def construct(self):
        j,slots=relay_scene(self,4,'4  ACh crosses')
        cargo=VGroup(*[Dot([x+d,.33,0],radius=.065,color=YELLOW) for x in (-.9,.7,2.3) for d in (-.1,.1)])
        self.add(cargo,leader('cleft',(4.8,.1),[2.95,.1,0],GREY))
        self.at('acetylcholine crosses')
        self.play(cargo.animate.shift(DOWN*.86),run_time=1.05,rate_func=linear)
        self.finish()

class S10Step5(SpokenScene):
    def construct(self):
        j,slots=relay_scene(self,5,'5  Receptors open')
        self.at('it opens receptor channels')
        self.play(*[r[0].animate.shift(LEFT*.1) for r in j.receptors],*[r[1].animate.shift(RIGHT*.1) for r in j.receptors],run_time=.6)
        self.at('and the')
        self.play(Create(j.patch),run_time=.55)
        self.play(Indicate(slots,scale_factor=1.025,color=TEXT),run_time=.6)
        self.finish()

class S11Epp(SpokenScene):
    def construct(self):
        j=Junction()
        for r in j.receptors:
            r[0].shift(LEFT*.1); r[1].shift(RIGHT*.1)
        self.add(j.all,j.patch,relay_slots(5))
        self.at('That depolarization')
        self.play(FadeIn(label('endplate potential (EPP)',0,3.35,GREEN,34)),run_time=.4)
        self.at('The end plate is')
        self.play(FadeIn(leader('endplate',(4.6,-1.1),[2.8,-.7,0],GREEN)),run_time=.4)
        self.at('the patch of')
        self.play(Indicate(j.patch,scale_factor=1.03,color=GREEN),run_time=.5)
        self.finish()

class S12Electrode(SpokenScene):
    def construct(self):
        j=Junction(); self.add(j.all,label('The record that started the story',0,3.35,TEXT,32))
        self.at('Paul')
        self.play(FadeIn(label('Paul Fatt  •  Bernard Katz',0,-3.15,TEXT,32)),run_time=.4)
        e=electrode((.7,-1.25)).shift(UP*1.5+LEFT*1.5)
        self.at('a fine glass electrode')
        self.play(Create(e),run_time=.5)
        self.at('inside a frog muscle')
        frog=label('frog muscle fibre',-.2,-1.85,GREY,28)
        self.play(e.animate.shift(DOWN*1.5+RIGHT*1.5),ReplacementTransform(j.labels[1],frog),run_time=.65)
        self.finish()

class S13Axes(SpokenScene):
    def construct(self):
        st,e,t=recording_stage(); self.add(st)
        ax=axes()
        self.at('Voltage runs')
        self.play(Create(ax[0]),FadeIn(ax[2]),FadeIn(ax[4]),run_time=.6)
        self.at('Time runs')
        self.play(Create(ax[1]),FadeIn(ax[3]),run_time=.6)
        self.finish()

class S14Nostim(SpokenScene):
    def construct(self):
        st,e,t,tr=recording(self,[])
        self.at('They did not stimulate')
        self.play(FadeIn(stimulator()),run_time=.4)
        # Time fiducials travel left with the flat recording: a visible scroll
        # without inventing voltage noise or spontaneous events before their cue.
        scroll=ValueTracker(0)
        ticks=always_redraw(lambda: VGroup(*[Line([x,-2.78,0],[x,-2.64,0],color=GREY,stroke_width=3) for x in np.arange(-5,18,2)-scroll.get_value() if -5.15<=x<=5.8]))
        self.at('the trace should')
        self.add(ticks)
        self.play(scroll.animate.set_value(8),run_time=1.6,rate_func=linear)
        ticks.clear_updaters(); self.finish()

class S15Blips(SpokenScene):
    def construct(self):
        st,e,t,tr=recording(self,[]); self.add(stimulator())
        self.at('But small blips')
        self.remove(tr)
        # Events enter at the right and scroll across a fixed recording window.
        clock=ValueTracker(0)
        moving=always_redraw(lambda: trace_from([(x+10.5-clock.get_value(),h) for x,h in BLIPS]))
        self.add(moving)
        self.play(clock.animate.set_value(10.5),run_time=2.6,rate_func=linear)
        moving.clear_updaters(); self.finish()

class S16Samesize(SpokenScene):
    def construct(self):
        st,e,t,tr=recording(self)
        marks=VGroup()
        for x,h in BLIPS:
            px=x+.084
            marks.add(VGroup(Line([px-.23,-2.55,0],[px-.23,-2.55+h,0],color=GREY,stroke_width=2),Line([px-.31,-2.55+h,0],[px-.15,-2.55+h,0],color=GREY,stroke_width=2),Line([px-.31,-2.55,0],[px-.15,-2.55,0],color=GREY,stroke_width=2)))
        self.at('Each blip')
        self.play(Create(marks),run_time=.5)
        self.at('the same size')
        self.play(FadeIn(label('about the same size',.3,.25,GREEN,30)),run_time=.35)
        self.at('far too small')
        self.add(DashedLine([-5.15,1.0,0],[5.8,1.0,0],color=ORANGE,stroke_width=3),label('firing threshold',4,1.48,ORANGE,28))
        self.finish()

class S17Distance(SpokenScene):
    def construct(self):
        st,e,t,tr=recording(self)
        self.at('Move the electrode')
        dim=VGroup(DoubleArrow([-1.9,2.05,0],[3.5,2.05,0],buff=0,color=TEXT,stroke_width=3),label('distance from endplate',1.3,1.53,TEXT,26))
        self.add(dim)
        self.play(e.animate.shift(RIGHT*5.5),run_time=1.05)
        self.at('and the blips')
        self.play(Transform(tr,trace_from([(x,h*.22) for x,h in BLIPS]).set_stroke(opacity=.6)),run_time=1.0)
        self.finish()

class S18Source(SpokenScene):
    def construct(self):
        st,e,t,tr=recording(self,[(x,h*.22) for x,h in BLIPS],True)
        self.at('So')
        self.play(e.animate.shift(LEFT*5.5),Transform(tr,trace_from(BLIPS)),run_time=.7)
        self.at('attributed them')
        # Release through the terminal's right membrane, above the fibre.
        dot=Dot([-1.15,3.18,0],radius=.08,color=YELLOW)
        self.add(dot); self.play(dot.animate.shift(RIGHT*.35),run_time=.3)
        a=Arrow(dot.get_center(),[.334,-.45,0],buff=0,color=GREY,stroke_width=4)
        dot.set_z_index(2)
        self.at('acetylcholine released spontaneously')
        self.play(GrowArrow(a),run_time=.55)
        self.play(FadeIn(label('spontaneous ACh release',3.1,1.2,YELLOW,28)),run_time=.3)
        self.finish()

class S19Name(SpokenScene):
    def construct(self):
        self.add(axes(),trace_from(BLIPS))
        self.at('They called them')
        self.play(FadeIn(label('miniature endplate potentials',0,2.9,GREEN,36)),run_time=.4)
        self.at('miniature endplate potentials')
        self.play(FadeIn(label('miniatures',0,2.15,GREEN,28)),run_time=.3)
        self.at('reported them in')
        self.play(FadeIn(label('Fatt and Katz • 1952',0,1.25,GREY,28)),run_time=.3)
        self.finish()

class S20Copies(SpokenScene):
    def construct(self):
        sm,big,labs=comparison(); self.add(sm,big,comparison_axes())
        self.at('Each miniature')
        self.play(FadeIn(labs),run_time=.3)
        self.at('looked like a')
        self.play(FadeIn(label('A miniature looks like a scaled-down copy.',0,3.2,TEXT,30)),run_time=.3)
        factor=ValueTracker(1)
        overlay=always_redraw(lambda: DashedVMobject(trace_from([(1.8,UNIT_HEIGHT*factor.get_value())],x0=1.25,x1=5.75,base=-1.9),num_dashes=45).set_stroke(GREEN,2))
        counter=label('× ?',-.15,.8,GREEN,36)
        self.at('copy of the response')
        travel=sm.copy(); self.add(travel)
        target=trace_from([(1.8,UNIT_HEIGHT)],x0=1.25,x1=5.75,base=-1.9)
        self.play(Transform(travel,target),run_time=.45)
        self.remove(travel); self.add(overlay,counter)
        self.play(factor.animate.set_value(6),big.animate.set_stroke(width=7,opacity=.45),run_time=1.0,rate_func=linear)
        overlay.clear_updaters()
        self.finish()

class S21Puzzle(SpokenScene):
    def construct(self):
        g,mark=puzzle(); self.add(g[1],g[2],g[4])
        self.at('Here is the puzzle')
        self.play(FadeIn(g[3]),run_time=.3)
        self.at('Is the')
        self.play(FadeIn(mark),run_time=.25)
        self.play(mark.animate.scale(1.18),run_time=.25)
        self.play(mark.animate.scale(1/1.18),run_time=.25)
        self.at('blips like these')
        self.play(LaggedStart(*[FadeIn(m,shift=UP*.15) for m in g[0]],lag_ratio=.22),run_time=.7)
        self.finish()

class S22Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        g,mark=puzzle(); self.add(g,mark)
        stack=unit_stack().set_stroke(opacity=.5).set_fill(opacity=.05)
        self.add(label('illustrative stack',.7,-2.9,TEXT,26))
        self.play(LaggedStart(*[FadeIn(b,shift=RIGHT*.2) for b in stack],lag_ratio=.15),mark.animate.scale(1.12),run_time=2.5)
        self.play(mark.animate.scale(1/1.12),run_time=2.5)

class S23Reveal(SpokenScene):
    def construct(self):
        g,mark=puzzle(); stack=unit_stack().set_stroke(opacity=.5).set_fill(opacity=.05); self.add(g,mark,stack,label('illustrative stack',.7,-2.9,TEXT,26))
        self.at('It is')
        answer=label('Yes: built from miniatures',0,2.9,GREEN,34)
        # Arc above the illustrative stack, ending at the evoked peak.
        link=CurvedArrow([-1.3,-.85,0],[1.884,1.7,0],angle=-2.1,color=GREEN,stroke_width=4)
        self.play(ReplacementTransform(mark,link),stack.animate.set_stroke(opacity=1).set_fill(opacity=.14),ReplacementTransform(g[3],answer),run_time=.45)
        self.at('The evidence comes')
        self.play(FadeIn(label('evidence: next chapter',0,3.48,TEXT,28)),run_time=.4)
        self.finish()

def question_tiles(two=False):
    items=[('Counting','How do you count merged units?'),('Calcium','Why does calcium matter so much?'),('Size','What sets the size of one unit?'),('Recording','How can a recording tell which side is at fault?')]
    g=VGroup()
    for i,(name,question) in enumerate(items):
        y=(1.6 if i==0 else -1.4) if two and i<2 else 2.08-i*1.65
        box=RoundedRectangle(width=11.8,height=1.35,corner_radius=.14,color=GREY,fill_color=GREY,fill_opacity=.06).move_to([0,y,0])
        heading=T(name,size=28,color=TEXT).move_to([0,y+.29,0])
        prompt=T(question,size=28,color=TEXT).move_to([0,y-.23,0])
        heading.set_x(-5.4,LEFT); prompt.set_x(-5.4,LEFT)
        g.add(VGroup(box,heading,prompt))
    return g

class S24More1(SpokenScene):
    def construct(self):
        g=question_tiles(two=True); self.add(label('More questions',0,3.38,TEXT,34))
        self.at('That answer')
        self.at('How do you count')
        self.play(FadeIn(g[0],shift=UP*.15),run_time=.4)
        self.at('Why does calcium')
        self.play(FadeIn(g[1],shift=UP*.15),run_time=.4)
        self.finish()

class S25More2(SpokenScene):
    def construct(self):
        g=question_tiles(); previous=question_tiles(two=True)
        self.add(label('More questions',0,3.38,TEXT,34),previous[0],previous[1])
        self.at('What sets the size')
        self.play(Transform(previous[0],g[0]),Transform(previous[1],g[1]),FadeIn(g[2],shift=UP*.15),run_time=.6)
        self.at('how can a recording')
        self.play(FadeIn(g[3],shift=UP*.15),run_time=.4)
        self.finish()

class S26Takeaway(SpokenScene):
    def construct(self):
        sm,big,labs=comparison(); self.add(sm,big,labs,comparison_axes())
        self.at('The miniature')
        self.play(FadeIn(label('The miniature is the unit.',0,3.35,GREEN,36)),run_time=.4)
        self.at('Every evoked response')
        stack=unit_stack()
        self.play(FadeIn(label('Every evoked response at this junction is built from it.',0,2.55,TEXT,30)),LaggedStart(*[FadeIn(b) for b in stack],lag_ratio=.08),FadeIn(label('× ?',-1.0,.5,GREEN,32)),FadeIn(label('illustrative stack',.7,-2.9,TEXT,26)),run_time=.65)
        self.at('is built from it')
        self.play(Indicate(stack,color=GREEN,scale_factor=1.025),run_time=.4)
        self.finish()

class S27End(EndCard):
    LINE='Every evoked response here is built from miniatures.'
    def construct(self):
        lines=VGroup(T('Every evoked response here',size=40,font=TITLE_FONT),T('is built from miniatures.',size=40,font=TITLE_FONT),T('biochemistrypedia.com',size=26,color=TEAL)).arrange(DOWN,buff=.4)
        self.play(FadeIn(lines),run_time=.5); self.finish()
