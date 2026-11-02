"""Less Than Double: passive, isopotential, fixed-conductance model.

COLOR MAP: BLUE cell; GREEN excitation (the brief's red ropes use series green);
GREY leak/structure; YELLOW voltage; TEAL threshold. All curves and numerical
comparisons are computed from the model below. No inhibitory rope is present,
so the displayed equation specializes the general model to gI = 0.
"""
import numpy as np
from bp_style import *

EL, EE, EI, THR, C = -65., 0., -65., -50., 200.
LIGHT = '#C6CBD4'

def vss(gL=10., gE=5., gI=0.):
    return (gL*EL + gE*EE + gI*EI)/(gL+gE+gI)

def tau(gE):
    return C/(10+gE)

def yv(v):
    return 2.5 + v*5.4/65

def label(s,x,y,size=28,color=TEXT,mono=False):
    return (M if mono else T)(s,size,color).move_to([x,y,0])

def heading(s):
    return label(s,0,3.35,34)

def marker(v,ghost=True):
    y=yv(v)
    return VGroup(DashedLine([-1.85,y,0],[-.65,y,0],color=YELLOW,stroke_width=4),
                  Circle(.12,color=YELLOW,stroke_width=3).move_to([-1.35,y,0]) if ghost else Dot([-1.35,y,0],radius=.12,color=YELLOW))

def ropes(v=EL,n=0):
    p=[-1.35,yv(v),0]
    # Endpoints are exact, stationary reversal potentials, not animated draw tips.
    out=VGroup(Line(p,[-5.6,yv(EL),0],color=LIGHT,stroke_width=10),
               Dot([-5.6,yv(EL),0],color=LIGHT),
               label('leak · 10 nS',-4.7,-3.6,26,LIGHT),
               label('EL = −65 mV',-4.55,-3.23,26,LIGHT))
    for i in range(n):
        x=-5.7+2.2*i
        out.add(Line(p,[x,yv(EE),0],color=GREEN,stroke_width=7),
                Dot([x,yv(EE),0],color=GREEN),label('5 nS',x,2.94,26,GREEN))
    return out

def gauge(threshold=True,zero=True):
    g=VGroup(Line([-.8,yv(EL),0],[-.8,yv(0),0],color=LIGHT,stroke_width=2),
             label('membrane voltage',-3.45,3.55,27,LIGHT))
    if zero:
        g.add(label('0 mV',-.65,2.94,26,GREEN))
    if threshold:
        g.add(DashedLine([-2.1,yv(THR),0],[.05,yv(THR),0],color=TEAL),
              label('threshold',.9,yv(THR)+.3,26,TEAL),label('−50 mV',.9,yv(THR)-.3,26,TEAL))
    return g

def stage(s,v=EL,n=0,threshold=False):
    g,r,m=gauge(threshold),ropes(v,n),marker(v)
    s.add(g,r,m)
    return g,r,m

def prediction_text():
    return VGroup(label('Your prediction?',3.6,2.8,32,TEAL),
                  label('2 × depolarization?',3.6,1.9,30),
                  label('If it doubled:',3.6,.7,28,LIGHT),
                  label('43.3 mV from rest',3.6,.05,28,YELLOW),
                  label('= −21.7 mV',3.6,-.6,30,YELLOW,True),
                  label('Both open;',3.6,-2.0,26,LIGHT),
                  label('voltage not yet settled',3.6,-2.55,26,LIGHT))

def pause_frame(s):
    stage(s,vss(),2)
    s.add(marker(EL+2*(vss()-EL)),prediction_text())

def fraction(top,bottom,x,y=1.2,width=5.6):
    return VGroup(label(top,x,y+.6,26,GREEN,True),
                  Line([x-width/2,y,0],[x+width/2,y,0],color=TEXT),
                  label(bottom,x,y-.6,28,LIGHT,True))

def formula(s,leak=False,show_legend=False):
    g,r,m=stage(s,vss(),1)
    s.add(label('Voltage from rest',3.5,3.3,32,YELLOW),label('Vss − EL =',3.5,2.55,30,YELLOW,True))
    f=fraction('gL × 0 + gE × (EE − EL)' if leak else 'gE × (EE − EL)','gL + gE',3.5,1.2,5.7)
    if leak:
        f[0].become(VGroup(label('gL × 0 +',1.5,1.8,26,LIGHT,True),
                           label('gE × (EE − EL)',4.7,1.8,26,GREEN,True)))
    f[2].become(VGroup(label('gL',2.75,.6,28,LIGHT,True),label('+',3.5,.6,28,LIGHT,True),label('gE',4.25,.6,28,GREEN,True)))
    s.add(f)
    legend=VGroup(label('Vss: settled voltage',3.5,-.25,26,YELLOW),
                  label('EL: rest / leak end',3.5,-.85,26,LIGHT),
                  label('EE: excitatory rope end',3.5,-1.45,26,GREEN),
                  label('gL: leak conductance',3.5,-2.05,26,LIGHT),
                  label('gE: input conductance',3.5,-2.65,26,GREEN))
    if show_legend:s.add(legend)
    return f,r,m,legend

def pair(s,results=True,two=True,settled=True):
    g,r,m=stage(s,vss(gE=10) if two and settled else vss(),2 if two else 1)
    a=fraction('5 × 65 = 325','10 + 5',1.9,1.3,2.5)
    b=fraction('10 × 65 = 650','10 + 10',5.0,1.3,2.7)
    # Separate factors from totals vertically; never put sums below answers.
    for f,x,top in [(a,1.9,'5 × 65'),(b,5.,'10 × 65')]:
        f[0].become(label(top,x,2.,26,GREEN,True))
    totals=VGroup(label('= 15',1.9,.12,28,LIGHT,True),label('= 20',5.,.12,28,LIGHT,True))
    nums=VGroup(label('= 325',1.9,1.64,26,GREEN,True),label('= 650',5.,1.64,26,GREEN,True))
    heads=VGroup(label('One input',1.9,2.9,28,GREEN),label('Two inputs',5.,2.9,28,GREEN))
    answers=VGroup(label('21.7 mV',1.9,-.85,28,YELLOW,True),label('32.5 mV',5.,-.85,28,YELLOW,True))
    s.add(heads,a,nums[0],totals[0])
    if two:s.add(b,nums[1],totals[1])
    if results:s.add(answers)
    return a,b,nums,totals,answers,r,m

def sharebar(two=False):
    total=20 if two else 15
    widths=[10,5,5] if two else [10,5]
    cols=[LIGHT,GREEN,GREEN]
    names=['leak','first','second']
    pieces=VGroup()
    x=.6
    for i,w in enumerate(widths):
        width=5.8*w/total
        rect=Rectangle(width=width,height=.65,color=cols[i],fill_color=cols[i],fill_opacity=.28 if i!=1 else .7).move_to([x+width/2,-2.7,0])
        pieces.add(VGroup(rect,label(names[i],x+width/2,-2.7,26,TEXT)))
        x+=width
    return VGroup(label(f'{"Two inputs" if two else "One input"}: first share = 5/{total}',3.5,-1.85,26,GREEN),pieces)

class S00Title(TitleCard):
    LESSON='Integration, Inhibition and Neuromodulation'
    TITLE='Less Than Double'

class S01Question(SpokenScene):
    def construct(self):
        cell=Circle(1.55,color=BLUE,fill_opacity=.12).move_to([0,-1.45,0])
        ropes_=VGroup(*[Line([x,2.2,0],[x*.23,-.1,0],color=GREEN,stroke_width=10) for x in [-2.7,2.7]])
        self.add(cell,ropes_,heading('2 inputs = 2 × the depolarization?'),
                 label('input 1',-2.7,2.65,28,GREEN),label('input 2',2.7,2.65,28,GREEN),label('?',0,-1.45,94,YELLOW))
        self.at('If one input')
        self.play(Indicate(ropes_[0],color=GREEN),run_time=.65)
        self.at('do two identical')
        self.play(Indicate(ropes_,color=GREEN),run_time=.65)
        self.finish()

class S02Cell(SpokenScene):
    def construct(self):
        g,r,m=stage(self,EL,0)
        self.add(label('Illustrative cell',-3.4,.3,32,BLUE),label('C = 200 pF',-3.4,-.4,30,BLUE,True))
        self.at('The leak is')
        self.play(Indicate(r[0],color=LIGHT),run_time=.65)
        self.at('tied at minus')
        self.play(Indicate(r[3],color=LIGHT),run_time=.6)
        self.at('Threshold is')
        self.play(FadeIn(VGroup(*gauge(True)[3:])),run_time=.4)
        self.finish()

class S03Illustrative(SpokenScene):
    def construct(self):
        self.add(RoundedRectangle(width=12.6,height=6.9,color=LIGHT,fill_color=BLUE,fill_opacity=.05),
                 label('Illustrative values',0,3.0,34),label('C = 200 pF     gL = 10 nS',0,2.25,34,BLUE,True),
                 label('EL = −65 mV     threshold = −50 mV',0,1.3,30,LIGHT,True))
        self.at('The cell is passive')
        self.play(FadeIn(label('Passive · isopotential',0,.25,36,BLUE)),run_time=.4)
        self.at('same everywhere')
        self.play(FadeIn(label('Same voltage everywhere',0,-.45,30,BLUE)),run_time=.4)
        self.at('Voltages above threshold')
        self.play(FadeIn(label('Above −50 mV: passive predictions',0,-1.35,32,YELLOW)),run_time=.4)
        self.at('with the spike')
        self.play(FadeIn(label('Spike mechanism switched off',0,-2.2,32,TEAL)),run_time=.4)
        self.play(FadeIn(label('Real thresholds shift with channel state',0,-3.,28,LIGHT)),run_time=.4)
        self.finish()

class S04One(SpokenScene):
    def construct(self):
        g,r,m=stage(self,EL,0,True)
        self.at('Open a steady')
        # Fade a complete rope rather than transform unrelated subobject counts.
        new=ropes(EL,1)
        self.play(FadeIn(VGroup(new[4],new[5])),run_time=.5)
        self.at('input of')
        self.play(FadeIn(new[6]),FadeIn(label('AMPA · steady input',3.6,1.5,30,GREEN)),run_time=.35)
        self.at('tied at')
        self.play(FadeIn(label('5 nS at 0 mV',3.6,.65,30,GREEN,True)),run_time=.4)
        self.add(label('Green ropes = excitation',3.6,-2.8,26,GREEN))
        self.finish()

class S05OneResult(SpokenScene):
    def construct(self):
        g,r,m=stage(self,EL,1,True)
        self.add(label('Passive prediction',3.7,3.1,30,YELLOW))
        self.at('The passive prediction')
        self.play(Transform(m,marker(vss())),Transform(r,ropes(vss(),1)),run_time=1.2)
        self.play(FadeIn(label(f'{vss():.1f} mV'.replace('-','−'),3.7,2.2,38,YELLOW,True)),run_time=.3)
        self.at('That is about')
        self.play(FadeIn(label(f'ΔV = {vss()-EL:.1f} mV',3.7,1.25,30,YELLOW,True)),run_time=.4)
        self.add(label('(10 × (−65) + 5 × 0)',3.7,.35,26,TEXT,True),label('──────────────────',3.7,-.1,26,TEXT,True),label('15',3.7,-.65,28,TEXT,True))
        self.at('A real cell')
        spark=Star(n=8,outer_radius=.24,inner_radius=.08,color=TEAL,fill_opacity=1).move_to([-2.7,yv(THR)+.45,0])
        self.play(GrowFromCenter(spark),FadeIn(label('A real cell would fire',3.7,-2.15,27,TEAL)),run_time=.4)
        self.play(FadeIn(label('on the way (spike off here)',3.7,-2.8,26,TEAL)),run_time=.35)
        self.finish()

class S06Tau(SpokenScene):
    def construct(self):
        # Same asymptote, two computed exponential approaches. The grey comparison
        # isolates the resting time constant; it is not a leak-only voltage trace.
        x0,x1,y0,y1=-4.9,5.7,-2.45,2.45
        xy=lambda t,v:np.array([x0+(x1-x0)*t/60,y0+(v-EL)*(y1-y0)/(vss()-EL),0])
        axes=VGroup(Line([x0,y0,0],[x1,y0,0],color=LIGHT),Line([x0,y0,0],[x0,y1+.2,0],color=LIGHT))
        self.add(heading('More conductance → faster settling'),axes,
                 label('membrane voltage (mV)',-5.95,0,26,LIGHT).rotate(PI/2),
                 label('−65',-5.45,y0,26,LIGHT),label('−43.3',-5.6,y1,26,YELLOW),label('time (ms)',.5,-3.3,26,LIGHT))
        for t in [0,20,40,60]:
            x=xy(t,EL)[0]
            self.add(Line([x,y0-.1,0],[x,y0+.1,0],color=LIGHT),label(str(t),x,y0-.35,26,LIGHT))
        def trace(tm,col):
            return VMobject(color=col,stroke_width=4).set_points_as_corners([xy(t,vss()+(EL-vss())*np.exp(-t/tm)) for t in np.linspace(0,60,301)])
        slow,fast=trace(tau(0),LIGHT),trace(tau(5),YELLOW)
        self.add(slow,label('20 ms: resting τ, same target',1.6,-1.5,26,LIGHT))
        self.at('It gets there')
        self.play(Create(fast),run_time=.8)
        self.at('about')
        eq=VGroup(label('τ = 200 pF / 15 nS',-2.,2.2,28,YELLOW,True),
                  label('= 13.3 ms',-2.6,1.55,28,YELLOW,True))
        p=xy(tau(5),vss()+(EL-vss())*np.exp(-1))
        self.play(FadeIn(eq),FadeIn(DashedLine([p[0],y0,0],p,color=YELLOW)),FadeIn(Dot(p,color=YELLOW)),run_time=.2)
        self.add(Line([p[0],-.6,0],[-1.5,-.6,0],color=YELLOW,stroke_width=2),label('13.3 ms · 63%',0,-.6,26,YELLOW))
        self.at('because the total')
        self.play(Indicate(eq,color=GREEN,scale_factor=1.02),run_time=.5)
        self.finish()

class S07Predict(SpokenScene):
    def construct(self):
        g,r,m=stage(self,vss(),1)
        self.at('Now open a second')
        new=ropes(vss(),2)
        self.play(FadeIn(VGroup(*new[7:])),run_time=.5)
        unsettled=label('Both open; voltage not yet settled',3.5,-2.6,26,LIGHT)
        self.add(unsettled)
        self.at('Does the depolarization')
        self.remove(unsettled)
        self.play(FadeIn(prediction_text()),FadeIn(marker(EL+2*(vss()-EL))),run_time=.5)
        self.finish()

class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        pause_frame(self)
        countdown=label('Think: 5',3.6,-3.3,28,TEAL,True)
        self.add(countdown)
        for n in range(5,0,-1):
            countdown.become(label(f'Think: {n}',3.6,-3.3,28,TEAL,True))
            self.wait(1)

class S09Reveal(SpokenScene):
    def construct(self):
        g,r,m=stage(self,vss(),2)
        self.add(marker(EL+2*(vss()-EL)),label('if doubled: −21.7 mV',3.5,3.25,26,LIGHT))
        self.at('the passive prediction')
        self.play(Transform(m,marker(vss(gE=10))),Transform(r,ropes(vss(gE=10),2)),run_time=.9)
        self.add(label('Passive prediction: −32.5 mV',3.5,2.55,27,YELLOW))
        self.at('is about')
        # Shared zero, shared mV scale. Bars never encode absolute voltage.
        bars=VGroup(label('depolarization from rest (mV)',3.5,1.65,26,TEXT))
        x0=.65
        bars.add(Line([x0,-2.,0],[6.3,-2.,0],color=LIGHT))
        for val in [0,20,40]:
            x=x0+5.6*val/(2*(vss()-EL))
            bars.add(label(str(val),x,-2.35,26,LIGHT))
        for y,val,name,col in [(.75,vss()-EL,'one input',GREEN),(-.35,vss(gE=10)-EL,'two inputs',YELLOW)]:
            w=5.6*val/(2*(vss()-EL))
            bars.add(Rectangle(width=w,height=.35,color=col,fill_color=col,fill_opacity=.7).move_to([x0+w/2,y,0]),label(f'{name}: {val:.1f}',4.4 if name=='two inputs' else 3.5,y+.42,26,col))
        w=5.6
        # Dashed horizontal edges joined by solid end caps keep all corners closed.
        outline=VGroup(DashedLine([x0,-1.275,0],[x0+w,-1.275,0],color=LIGHT,dash_length=.14),
                       DashedLine([x0,-1.625,0],[x0+w,-1.625,0],color=LIGHT,dash_length=.14),
                       Line([x0,-1.625,0],[x0,-1.275,0],color=LIGHT),
                       Line([x0+w,-1.625,0],[x0+w,-1.275,0],color=LIGHT))
        bars.add(outline,label(f'if it doubled: {2*(vss()-EL):.1f}',3.5,-1.0,26,LIGHT))
        self.play(FadeIn(bars),run_time=.5)
        # Ratio physically between the two measured bars.
        self.at('That is about')
        bracket=VGroup(Line([.9,.52,0],[.9,-.12,0],color=YELLOW),
                       Line([.9,.52,0],[1.15,.52,0],color=YELLOW),
                       Line([.9,-.12,0],[1.15,-.12,0],color=YELLOW),
                       label('1.5 ×',1.85,.2,28,YELLOW))
        self.play(FadeIn(bracket),run_time=.35)
        self.at('not twice')
        self.play(FadeIn(label('1.5 ×, not 2 ×',3.5,-3.15,30,YELLOW)),run_time=.35)
        self.finish()

class S10FromRest(SpokenScene):
    def construct(self):
        f,r,m,legend=formula(self,True,show_legend=True)
        self.at('measure the voltage')
        self.play(Indicate(m,color=YELLOW),Indicate(legend[1],color=LIGHT),run_time=.6)
        self.at('Then the leak')
        self.play(Indicate(r[0],color=LIGHT),Indicate(f[0],color=LIGHT,scale_factor=1.02),run_time=.6)
        # Define once, then retire the legend for the rest of this sequence.
        self.play(FadeOut(legend),run_time=.3)
        self.finish()

class S11WhyDrop(SpokenScene):
    def construct(self):
        f,r,m,legend=formula(self,True)
        self.at('The leak is tied')
        self.play(Indicate(r[3],color=LIGHT),run_time=.6)
        self.at('so its top')
        self.remove(legend)
        zero=label('0 +',1.5,1.8,26,LIGHT,True)
        explanation=label('10 × 0 = 0',3.5,-.65,32,LIGHT,True)
        self.play(Transform(f[0][0],zero),FadeIn(explanation),run_time=.4)
        self.wait(.6)
        self.play(FadeOut(f[0][0]),f[0][1].animate.move_to([3.5,1.8,0]),run_time=.4)
        # Rebuild the identical stage after removing a nested text term: Manim
        # otherwise retains a reparented copy of the surviving numerator.
        self.clear()
        f,r,m,legend=formula(self)
        self.remove(legend)
        self.add(explanation)
        self.at('But the leak')
        f[2][0].set_color(YELLOW)
        self.play(Indicate(f[2][0],color=YELLOW,scale_factor=1.15),run_time=.5)
        leak_box=SurroundingRectangle(f[2][0],color=YELLOW,buff=.12,stroke_width=3)
        self.play(Create(leak_box),run_time=.25)
        self.at('and still carries')
        self.remove(explanation)
        start=np.array([-1.35,yv(vss()),0])
        end=np.array([-5.6,yv(EL),0])
        arrow=Arrow(start+.25*(end-start),start+.78*(end-start),buff=0,color=YELLOW,stroke_width=6)
        self.play(GrowArrow(arrow),FadeIn(label('Leak still carries current',3.5,-1.3,28,LIGHT)),run_time=.5)
        self.finish()

class S12Top(SpokenScene):
    def construct(self):
        f,r,m,legend=formula(self)
        self.at('Each top')
        top_box=SurroundingRectangle(f[0],color=GREEN,buff=.16,stroke_width=4)
        rope_glow=r[4].copy().set_stroke(GREEN,width=18,opacity=.32).set_z_index(-1)
        self.play(Create(top_box),FadeIn(rope_glow),r[4].animate.set_stroke(width=10),run_time=.4)
        self.at('times how far')
        self.remove(legend)
        # Distance is from rest to reversal, independent of current marker.
        distance=DoubleArrow([-6.35,yv(EL),0],[-6.35,yv(EE),0],buff=0,color=GREEN)
        self.play(GrowArrow(distance),FadeIn(label('EE − EL = 65 mV',3.5,-.55,30,GREEN,True)),run_time=.5)
        self.add(label('g × (E − EL)',3.5,-1.6,34,GREEN,True),label('Conductance × distance from rest',3.5,-2.7,27,LIGHT))
        self.finish()

class S13Bottom(SpokenScene):
    def construct(self):
        f,r,m,legend=formula(self)
        self.at('The bottom line')
        bottom_box=SurroundingRectangle(f[2],color=YELLOW,buff=.16,stroke_width=4)
        rope_glows=VGroup(*[r[i].copy().set_stroke(YELLOW,width=20,opacity=.4).set_z_index(-1) for i in [0,4]])
        self.play(Create(bottom_box),FadeIn(rope_glows),f[2].animate.set_color(YELLOW),run_time=.4)
        self.remove(legend)
        self.add(label('Total conductance',3.5,-.65,34,LIGHT),label('10 + 5 = 15 nS',3.5,-1.7,32,LIGHT,True))
        self.finish()

class S14Double(SpokenScene):
    def construct(self):
        a,b,nums,totals,answers,r,m=pair(self,results=False,two=False)
        self.at('Two inputs double')
        newropes=ropes(vss(),2)
        self.play(FadeIn(b[0]),FadeIn(b[1]),FadeIn(nums[1]),FadeIn(VGroup(*newropes[7:])),run_time=.5)
        self.remove(r,*newropes[7:])
        self.add(newropes)
        r=newropes
        self.play(Indicate(VGroup(nums[0],nums[1]),color=GREEN,scale_factor=1.06),run_time=.5)
        self.at('but they also')
        self.play(FadeIn(b[2]),FadeIn(totals[1]),run_time=.4)
        self.play(Circumscribe(VGroup(totals[0],totals[1]),color=YELLOW),run_time=.6)
        self.finish()

class S15OneVsTwo(SpokenScene):
    def construct(self):
        a,b,nums,totals,answers,r,m=pair(self,results=False,settled=False)
        self.at('With one input')
        self.play(Indicate(totals[0],color=YELLOW,scale_factor=1.08),run_time=.6)
        self.at('With two')
        self.play(Indicate(totals[1],color=YELLOW,scale_factor=1.08),run_time=.5)
        self.at('the top doubles')
        glow=Underline(nums[1],color=GREEN,buff=.035,stroke_width=3).set_z_index(-1)
        self.play(Create(glow),run_time=.5)
        self.at('but the bottom')
        rings=VGroup(*[Ellipse(width=1.5,height=.65,color=YELLOW).move_to(t) for t in totals])
        self.play(Create(rings),run_time=.5)
        # Reveal results only once both denominator totals have been spoken.
        self.at('20',lead=-.32)
        self.play(FadeIn(answers),Transform(m,marker(vss(gE=10))),Transform(r,ropes(vss(gE=10),2)),run_time=.4)
        self.finish()

class S16Dilute(SpokenScene):
    def construct(self):
        g,r,m=stage(self,vss(),1)
        bar=sharebar(False)
        self.add(bar,label('Each rope stays 5 nS',3.5,1.8,30,GREEN))
        # Hold the one-input comparison long enough to read before dilution.
        self.wait(2)
        self.at('the second input')
        target=ropes(vss(gE=10),2)
        self.play(Transform(bar,sharebar(True)),Transform(r,VGroup(*target[:7])),FadeIn(VGroup(*target[7:])),Transform(m,marker(vss(gE=10))),run_time=.65)
        self.wait(2)
        self.finish()

class S17Rope(SpokenScene):
    def construct(self):
        g,r,m=stage(self,vss(),1)
        def arrows(v,n):
            return VGroup(*[Arrow([-1.35,yv(v),0],[-5.7+2.2*i,yv(EE),0],buff=.18,color=YELLOW,stroke_width=4).shift(RIGHT*.14) for i in range(n)])
        a=arrows(vss(),1)
        case=label('One input',3.5,2.6,34,GREEN)
        eq=VGroup(label('Driving force per rope',3.5,1.5,30,YELLOW),label('0 − (−43.3)',3.5,.5,30,YELLOW,True),label('= 43.3 mV',3.5,-.25,32,YELLOW,True))
        self.add(a,case,eq)
        self.at('That is the same')
        self.play(Indicate(a,color=YELLOW),run_time=.6)
        self.at('The marker is nearer')
        neweq=VGroup(label('Driving force per rope',3.5,1.5,30,YELLOW),label('0 − (−32.5)',3.5,.5,30,YELLOW,True),label('= 32.5 mV',3.5,-.25,32,YELLOW,True))
        # Geometry, case label and numbers change in the same animation.
        target=ropes(vss(gE=10),2)
        targetarrows=arrows(vss(gE=10),2)
        self.play(Transform(r,VGroup(*target[:7])),FadeIn(VGroup(*target[7:])),Transform(m,marker(vss(gE=10))),Transform(a[0],targetarrows[0]),FadeIn(targetarrows[1]),Transform(eq,neweq),Transform(case,label('Two inputs',3.5,2.6,34,GREEN)),run_time=.8)
        a.add(targetarrows[1])
        self.at('so each')
        self.play(Indicate(a,color=YELLOW),run_time=.6)
        self.add(label('Each driving force shrinks',3.5,-2.1,28,YELLOW))
        self.finish()

class S18Name(SpokenScene):
    def construct(self):
        # A large shared membrane patch; schematic channels have sliding gates.
        membrane=RoundedRectangle(width=11.7,height=2.6,color=LIGHT,fill_color=BLUE,fill_opacity=.12).move_to([0,-1.3,0])
        channels=VGroup(*[Rectangle(width=.8,height=2.6,color=GREEN,fill_color=BG,fill_opacity=1).move_to([x,-1.3,0]) for x in [-1.15,1.15]])
        gates=VGroup(*[Line([x-.4,-.6,0],[x+.4,-.6,0],color=GREEN,stroke_width=9) for x in [-1.15,1.15]])
        inputs=VGroup(*[Arrow([x,2.,0],[x,.2,0],color=GREEN,buff=0,stroke_width=8) for x in [-1.15,1.15]])
        self.add(membrane,channels,gates,inputs,heading('Sublinear summation'),label('two nearby synapses',0,2.5,30,GREEN))
        self.at('This is sublinear')
        self.play(Indicate(channels,color=GREEN,scale_factor=1.03),run_time=.6)
        self.at('Inputs sharing')
        self.play(gates[0].animate.shift(LEFT*.65),gates[1].animate.shift(RIGHT*.65),run_time=.5)
        self.play(*[GrowArrow(Arrow([x,-.2,0],[x,-2.2,0],color=GREEN,buff=0,stroke_width=7)) for x in [-1.15,1.15]],run_time=.5)
        self.add(label('one small patch of membrane',0,-3.2,30,LIGHT))
        self.finish()

class S19Where(SpokenScene):
    def construct(self):
        a,b,nums,totals,answers,r,m=pair(self)
        self.at('Notice where')
        self.play(Indicate(VGroup(nums[0],nums[1]),color=GREEN),run_time=.5)
        self.at('in the bottom')
        rings=VGroup(*[Ellipse(width=1.5,height=.65,color=YELLOW).move_to(t) for t in totals])
        self.play(Create(rings),run_time=.55)
        self.at('the total conductance')
        self.add(label('Total conductance: 15 → 20 nS',3.5,-2.4,28,YELLOW))
        self.finish()

class S20Takeaway(SpokenScene):
    def construct(self):
        self.add(heading('Conductances add'),
                 label('Passive · isopotential · steady inputs',0,2.6,32,BLUE))
        self.at('Each new input')
        bars=VGroup(*[Rectangle(width=w,height=.4,color=c,fill_opacity=.65).move_to([x,1.8,0]) for w,x,c in [(4,-1,GREY),(2,2,GREEN),(2,4,GREEN)]])
        self.play(FadeIn(bars),run_time=.4)
        self.at('So the voltage')
        self.play(FadeIn(label('Voltage settles at a weighted average',0,.9,38,YELLOW)),run_time=.3)
        self.at('not a sum')
        self.play(FadeIn(label('Two strong inputs: 1.5 ×, not 2 ×',0,0,38,YELLOW)),
                  FadeIn(label('(each input = half the leak)',0,-.65,32,LIGHT)),run_time=.3)
        self.at('Small inputs nearly')
        self.play(FadeIn(label('Small compared with leak → nearly add',0,-1.75,36,GREEN)),run_time=.3)
        self.at('Large ones fall')
        self.play(FadeIn(label('Large compared with leak → fall short',0,-2.95,36,GREEN)),run_time=.3)
        self.finish()

class S21End(EndCard):
    LINE='Millivolts add only approximately.'
