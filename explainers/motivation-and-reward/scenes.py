"""Received Minus Predicted, revision.
COLOR MAP: TEAL prediction; YELLOW received reward; GREEN positive error/burst;
RED negative error/pause; BLUE tone; PURPLE dopamine; PINK hypothalamic AgRP;
ORANGE learning step; TEXT light/firing; GREY anatomy/axes.
Model: delta=r-V; V_next=V+.30*delta. Firing diagrams are deterministic
illustrations, not recordings: baseline 4 ticks/unit, extra ticks proportional
 to positive delta, a central pause proportional to negative delta.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
PINK='#ED91AE'
ORANGE='#F29E4C'
BASE=-2.15
SCALE=4.5
PX=-4.6
RX=-2.2
LINE='Dopamine bursts and pauses report better or worse than predicted.'

def label(s,x=0,y=3.15,size=32,color=TEXT):
    return T(s,size=size,color=color).move_to([x,y,0])

def mouse():
    body=Ellipse(width=3.5,height=1.9,color=GREY,fill_color=GREY,fill_opacity=.25)
    head=Ellipse(width=1.3,height=1.15,color=GREY,fill_opacity=.3).move_to([1.65,.22,0])
    ear=Circle(radius=.43,color=GREY,fill_opacity=.3).move_to([1.3,.92,0])
    eye=Dot([1.95,.42,0],radius=.07,color=TEXT)
    feet=VGroup(Line([-.9,-.8,0],[-.3,-1,0],color=GREY),Line([1,-.65,0],[1.5,-.9,0],color=GREY))
    tail=ArcBetweenPoints([-1.7,-.1,0],[-3,-.65,0],angle=1,color=GREY)
    return VGroup(body,head,ear,eye,feet,tail)

def dish():
    bowl=Polygon([-1,.3,0],[-.7,-.35,0],[.7,-.35,0],[1,.3,0],color=GREY,fill_opacity=.2)
    food=VGroup(*[RoundedRectangle(width=.35,height=.25,corner_radius=.06,color=YELLOW,fill_opacity=.85).move_to([x,y,0]) for x,y in [(-.5,.35),(0,.4),(.5,.35)]])
    return VGroup(bowl,food)

def brain():
    # Schematic sagittal silhouette: anterior left, posterior right, ventral base below.
    pts=[[-4,-.2,0],[-3.8,1.3,0],[-2.3,2.3,0],[0,2.45,0],[2,1.65,0],[2.6,.4,0],[2.2,-.5,0],[2.8,-1.6,0],[1.9,-1.8,0],[1.1,-.8,0],[-.2,-1.05,0],[-1.9,-.9,0],[-3.5,-.8,0],[-4,-.2,0]]
    outline=VMobject(color=GREY,fill_color=GREY,fill_opacity=.1).set_points_smoothly(pts)
    hypo=VGroup(*[Dot([x,y,0],radius=.14,color=PINK) for x,y in [(-1.3,-.6),(-.9,-.75),(-.5,-.6)]])
    mid=VGroup(*[Dot([x,y,0],radius=.14,color=PURPLE) for x,y in [(.8,-.25),(1.2,-.4),(1.5,-.2)]])
    hl=VGroup(label('hypothalamus',-2.8,-2,28,PINK),Line([-2,-1.7,0],[-1,-.9,0],color=PINK))
    ml=VGroup(label('midbrain',3.8,-.6,28,PURPLE),Line([2.9,-.55,0],[1.65,-.3,0],color=PURPLE))
    return VGroup(outline,hypo,mid,hl,ml)

def switch():
    return chip('light switch',TEXT,28).move_to([4,2,0])

def illumination():
    return VGroup(Polygon([3.4,1.7,0],[-1.6,-.35,0],[-.4,-1,0],color=TEXT,fill_color=TEXT,fill_opacity=.12,stroke_width=0),Circle(radius=.67,color=TEXT,stroke_width=5).move_to([-1,-.6,0]))

def cup():
    return Polygon([-.4,.38,0],[-.3,-.38,0],[.3,-.38,0],[.4,.38,0],color=YELLOW,fill_color=YELLOW,fill_opacity=.65).move_to([-.75,2,0])

def bar(x,v,color):
    if v<=0:
        return DashedVMobject(Rectangle(width=1.05,height=.16,color=color).move_to([x,BASE+.08,0]),num_dashes=12)
    return Rectangle(width=1.05,height=v*SCALE,color=color,fill_color=color,fill_opacity=.7).move_to([x,BASE+v*SCALE/2,0])

def bars(v=0,r=1):
    axis=VGroup(Arrow([-5.6,BASE,0],[-5.6,2.6,0],buff=0,color=GREY),Line([-5.6,BASE,0],[-1.4,BASE,0],color=GREY),label('reward amount',-3.55,2.8,26))
    return VGroup(axis,bar(PX,v,TEAL),bar(RX,r,YELLOW),VGroup(label('predicted',PX,-2.6,26,TEAL),label('received',RX,-2.6,26,YELLOW)),cup())

def gap(v,r,word='error'):
    yp,yr=BASE+v*SCALE,BASE+r*SCALE
    color=GREEN if r>v else RED if r<v else TEXT
    guides=VGroup(DashedLine([PX+.55,yp,0],[-3.4,yp,0],color=color),DashedLine([RX-.55,yr,0],[-3.4,yr,0],color=color))
    if abs(r-v)<.005:
        arrow=VGroup(Line([-3.65,yr,0],[-3.15,yr,0],color=TEXT),Line([-3.65,yr-.08,0],[-3.65,yr+.08,0],color=TEXT),Line([-3.15,yr-.08,0],[-3.15,yr+.08,0],color=TEXT))
    else:
        arrow=DoubleArrow([-3.4,yp,0],[-3.4,yr,0],buff=0,color=color,tip_length=min(.12,abs(yr-yp)/4))
    # Label below the chart, clearly separate from the firing panel.
    return VGroup(guides,arrow,label(word,-3.4,-3.2,28,color))

def spike_ticks(delta=0,cx=3.55,y=-.65,w=5.1,h=1.65):
    xs=list(np.arange(-w/2,w/2+.001,.34))
    if delta<0: xs=[x for x in xs if abs(x)>.78*abs(delta)]
    if delta>0: xs+=list(np.linspace(-.55,.55,int(round(15*delta))))
    return VGroup(*[Line([cx+x,y,0],[cx+x,y+h,0],color=TEXT,stroke_width=2.6) for x in sorted(xs)])

def firing(delta=0,question=False,marker='juice arrives'):
    axis=Arrow([.9,-.65,0],[6.3,-.65,0],buff=0,color=GREY)
    mark=DashedLine([3.55,-1,0],[3.55,1.5,0],color=YELLOW,stroke_opacity=.6)
    title=label('dopamine neuron firing',3.5,2.35,27,PURPLE)
    labs=VGroup(label(marker,3.55,1.8,26,YELLOW),label('time',5.8,-1.15,26))
    spikes=spike_ticks(delta) if not question else VGroup()
    return VGroup(title,axis,mark,labs,spikes)

def question_frame():
    return VGroup(bars(1,1),label('Exactly as predicted',0,3.4,34),firing(question=True),label('?',3.55,.2,60),label('What does the neuron do?',3.55,-1.8,26),label('after many trials',-3.4,-3.2,28))

def gauge(value=0):
    a=PI*(1-value)
    return VGroup(Arc(radius=1.4,start_angle=0,angle=PI,color=GREY,stroke_width=7),Arrow(ORIGIN,[1.2*np.cos(a),1.2*np.sin(a),0],buff=0,color=YELLOW),Dot(radius=.1,color=YELLOW))

def scope():
    texts=['Many, not all, dopamine neurons','Trained monkeys and rodents','Tasks with predictable reward timing','A signal; recording alone ≠ proof of teaching','Nothing about pleasure']
    rows=VGroup(*[label(t,0,2.1-i*1.12,38) for i,t in enumerate(texts)])
    # Long line uses two rows rather than shrinking the font.
    rows[3].become(VGroup(label('A signal; recording alone',0,-1.12,38),label('≠ proof of teaching',0,-1.67,38)))
    rows[4].move_to([0,-2.75,0]).set_color(ORANGE)
    return VGroup(RoundedRectangle(width=12.5,height=6.6,corner_radius=.2,color=GREY),rows)

class S00Title(TitleCard):
    LESSON='Feeding, Motivation and Reward'
    TITLE='Received Minus Predicted'

class S01Question(SpokenScene):
    def construct(self):
        m=mouse().scale(1.9).move_to([-1.6,.2,0]); d=dish().scale(1.4).move_to([5,-1.05,0])
        self.add(m,d,label('well-fed • no hunger',-1.6,-2.85,32),label('?',3.45,1.8,80))
        self.at('Why would'); self.play(Indicate(d,color=YELLOW),run_time=.7); self.finish()

class S02Hook(SpokenScene):
    def construct(self):
        b=brain(); b[1].set_opacity(0); b[2].set_opacity(.35); self.add(b)
        self.at('light sensitive switch'); self.play(FadeIn(switch()),run_time=.4)
        self.at('small group of neurons'); self.play(b[1].animate.set_opacity(1),run_time=.4)
        self.at('base of its brain'); self.play(FadeIn(label('AgRP neurons at the base',0,-3,30,PINK)),run_time=.4); self.finish()

class S03Hook2(SpokenScene):
    def construct(self):
        b=brain(); sw=switch(); beam=illumination(); self.add(b,sw)
        self.at('shone light'); self.play(FadeIn(beam),FadeIn(label('Aponte, Atasoy and Sternson, 2011',0,-3.1,26)),run_time=.3)
        # Preserve an anatomical inset without scaling text below readable size.
        self.play(FadeOut(b[3]),FadeOut(b[4]),FadeOut(sw[1]),run_time=.15)
        inset=VGroup(b[0],b[1],b[2],sw[0],beam)
        m=mouse().scale(.85).move_to([-2.8,-.9,0]); d=dish().move_to([3,-1.45,0])
        self.play(inset.animate.scale(.4).move_to([-3.9,1.65,0]),FadeIn(m),FadeIn(d),run_time=.35)
        self.add(label('light on',-3.9,2.95,26))
        self.at('on those neurons'); self.play(m.animate.shift(RIGHT*3.5),run_time=1.5)
        self.at('began eating'); self.play(m.animate.rotate(-.07),FadeOut(d[1][0]),run_time=.3)
        self.play(m.animate.rotate(.07),FadeOut(d[1][1]),run_time=.3)
        self.at('within minutes'); self.play(FadeIn(label('eating within minutes',2,1.4,32,YELLOW)),run_time=.25); self.finish()

class S04Two(SpokenScene):
    def construct(self):
        a=RoundedRectangle(width=12,height=2.5,color=GREY).move_to([0,1.6,0]); b=a.copy().move_to([0,-1.6,0]); q1=label('?',0,1.6,60); q2=label('?',0,-1.6,60); self.add(a,b,q1,q2)
        self.at('two questions'); self.play(a.animate.set_stroke(TEXT),b.animate.set_stroke(TEXT),run_time=.4)
        self.at('Why is food'); self.play(FadeOut(q1),FadeIn(label('Why is food worth seeking?',0,1.6,38)),run_time=.4)
        self.at('how does the brain'); self.play(FadeOut(q2),FadeIn(label('How does the brain learn where it is?',0,-1.6,36)),run_time=.4); self.finish()

class S05Worth(SpokenScene):
    def construct(self):
        g=gauge(.15).scale(1.35).shift(LEFT*2.7+DOWN*.3); d=dish().scale(2).move_to([2.5,-.6,0]); tag=chip('worth now',YELLOW,34).move_to([2.5,1.7,0]); self.add(g,d,tag,Line([-.9,.3,0],d[0].get_vertices()[0],color=YELLOW),label('hunger',-2.7,-1.2,32))
        self.at('Hunger answers'); self.play(Indicate(g),run_time=.4)
        self.at('Hunger changes'); self.play(Transform(g,gauge(.85).scale(1.35).shift(LEFT*2.7+DOWN*.3)),tag.animate.scale(1.2),d[0].animate.set_stroke(YELLOW,width=7),run_time=1.2)
        self.at('hypothalamus'); self.play(FadeIn(label('Hypothalamus circuits may help set worth',0,-2.9,30,PINK)),run_time=.4); self.finish()

class S06Dopamine(SpokenScene):
    def construct(self):
        b=brain(); self.add(b)
        self.at('Dopamine neurons'); self.play(Indicate(b[2],color=PURPLE),run_time=.5)
        self.at('in the midbrain')
        # Keep a highlighted anatomical inset beside the magnified neurons.
        enlarged=b[2].copy().scale(4).move_to([2.7,.6,0])
        anatomy=VGroup(b[0],b[1],b[2])
        self.play(anatomy.animate.scale(.65).move_to([-3.5,.6,0]),
                  FadeOut(b[3]),b[4].animate.move_to([-3.5,-1.5,0]),run_time=.65)
        # Re-anchor the readable midbrain label to the highlighted inset region.
        b[4][0].move_to([-3.5,-1.5,0])
        b[4][1].put_start_and_end_on([-3.5,-1.2,0],b[2].get_bottom()+DOWN*.1)
        ring=SurroundingRectangle(b[2],buff=.18,color=PURPLE,corner_radius=.12)
        connector=DashedLine(ring.get_right(),enlarged.get_left(),color=PURPLE)
        self.play(Create(ring),Create(connector),FadeIn(enlarged),run_time=.5)
        self.add(label('dopamine neurons',2.7,2.5,34,PURPLE))
        self.at('help with the second'); self.play(FadeIn(label('Learning where to find reward',0,-2.8,32)),run_time=.4); self.finish()

class S07Rule(SpokenScene):
    def construct(self):
        c=chip('reward alone?',GREY,36).move_to([0,1.9,0]); self.add(label('Dopamine neuron signal'),c)
        self.at('They do not'); self.play(Create(Line(c.get_left(),c.get_right(),color=RED,stroke_width=6)),run_time=.4)
        self.at('They report how much'); self.play(FadeIn(label('received − predicted',0,.35,48)),FadeIn(label('better',-3.5,-2.5,36,GREEN)),FadeIn(label('worse',3.5,-2.5,36,RED)),Create(spike_ticks(1,-3.5,-1.8,4,.9)),Create(spike_ticks(-1,3.5,-1.8,4,.9)),run_time=.7); self.finish()

class S08Bars(SpokenScene):
    def construct(self):
        b=bars(); self.add(b[0],b[4],firing(question=True))
        self.at('Picture two bars'); self.play(FadeIn(b[1]),run_time=.4)
        self.at('One shows'); self.play(FadeIn(b[3][0]),run_time=.4)
        self.at('The other shows'); self.play(GrowFromEdge(b[2],DOWN),FadeIn(b[3][1]),run_time=.7); self.finish()

class S09Gap(SpokenScene):
    def construct(self):
        self.add(bars(),firing(question=True)); g=gap(0,1)
        self.at('The gap between'); self.play(Create(g[0]),Create(g[1]),run_time=.45)
        self.at('is the error'); self.play(FadeIn(g[2]),Indicate(g[1],color=GREEN,scale_factor=1.1),run_time=.55); self.finish()

class S10Better(SpokenScene):
    def construct(self):
        f=firing(question=True); self.add(bars(),gap(0,1),f)
        self.at('better than predicted'); self.play(FadeIn(label('Better than predicted',0,3.45,34,GREEN)),run_time=.35)
        self.at('gap is positive'); self.play(Transform(self.mobjects[1],gap(0,1,'positive error')),run_time=.4)
        self.at('neuron fires'); self.play(Create(spike_ticks(1)),FadeIn(label('brief burst',3.55,-2.3,32,GREEN)),run_time=.6); self.finish()

class S11Q(SpokenScene):
    def construct(self):
        f=question_frame(); self.add(f[0],f[2],f[5])
        self.at('exactly as predicted'); self.play(FadeIn(f[1]),run_time=.4)
        self.at('What does the neuron'); self.play(FadeIn(f[3]),FadeIn(f[4]),run_time=.4); self.finish()

class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question_frame())
        ring=Circle(radius=.42,color=GREY).move_to([5.2,.2,0]); sweep=Arc(radius=.42,start_angle=PI/2,angle=-TAU,color=TEAL,stroke_width=7).move_to(ring)
        self.add(ring); self.play(Create(sweep),run_time=5,rate_func=linear)

class S13Reveal(SpokenScene):
    def construct(self):
        f=question_frame(); self.add(f)
        ring=Circle(radius=.42,color=TEAL).move_to([5.2,.2,0]); self.add(ring)
        self.at('nothing'); self.play(FadeOut(f[3]),FadeOut(f[4]),FadeOut(f[5]),FadeOut(ring),Create(spike_ticks()),run_time=.5)
        self.at('no gap'); self.play(Create(gap(1,1,'no error')),run_time=.4)
        self.at('firing stays steady'); self.play(FadeIn(label('steady firing',3.55,-2.3,32)),run_time=.4); self.finish()

class S14Worse(SpokenScene):
    def construct(self):
        b=bars(1,.3); f=firing(question=True,marker='expected juice time'); self.add(b,f)
        self.at('worse than predicted'); self.play(FadeIn(label('Worse than predicted',0,3.45,34,RED)),run_time=.4)
        self.at('or missing'); self.play(Transform(b[2],bar(RX,0,YELLOW)),FadeIn(label('reward omitted',3.55,-3.1,28,YELLOW)),run_time=.45)
        self.at('gap is negative'); self.play(Create(gap(1,0,'negative error')),run_time=.4)
        self.at('Firing pauses briefly'); self.play(Create(spike_ticks(-1)),FadeIn(label('brief pause',3.55,-2.3,32,RED)),run_time=.5); self.finish()

class S15Learn(SpokenScene):
    def construct(self):
        b=bars(0,1); g=gap(0,1); f=firing(1); count=label('trial 1 • same juice',0,3.45,34); self.add(b,g,f,count)
        self.at('same juice comes'); self.play(Indicate(b[2],color=YELLOW),run_time=.4)
        self.at('the prediction moves')
        v=0
        # A solid rectangle grows continuously; dashed zero and text never morph.
        growing=bar(PX,.001,TEAL)
        self.remove(b[1]); b[1].become(growing); self.add(b[1])
        for n in range(1,4):
            nv=v+.3*(1-v)
            portion=Line([PX+.65,BASE+v*SCALE,0],[PX+.65,BASE+nv*SCALE,0],color=ORANGE,stroke_width=9)
            new_count=label(f'trial {n+1} • same juice',0,3.45,34)
            self.play(FadeOut(count),Create(portion),run_time=.15)
            self.play(FadeIn(new_count),run_time=.15); count=new_count
            next_gap=gap(nv,1); next_ticks=spike_ticks(1-nv)
            self.play(b[1].animate.stretch_to_fit_height(nv*SCALE).move_to([PX,BASE+nv*SCALE/2,0]),
                      FadeOut(g),FadeIn(next_gap),FadeOut(f[4]),FadeIn(next_ticks),FadeOut(portion),run_time=.5)
            g=next_gap; f[4].become(next_ticks)
            # Keep the new tick object in the firing group for the next swap.
            self.remove(next_ticks); self.add(f[4])
            v=nv
        self.finish()

class S16Shrink(SpokenScene):
    def construct(self):
        v=1-.7**3; b=bars(v,1); g=gap(v,1); f=firing(1-v); title=label('Repeated, certain juice',0,3.45,34); self.add(b,g,f,title)
        self.at('error at the juice')
        for n in (5,8,12):
            nv=1-.7**n
            self.play(Transform(b[1],bar(PX,nv,TEAL)),Transform(g,gap(nv,1)),Transform(f[4],spike_ticks(1-nv)),run_time=.45)
        self.at('An uncertain reward'); self.play(Transform(title,label('Uncertain reward',0,3.45,34)),Transform(b[1],bar(PX,.5,TEAL)),Transform(g,gap(.5,1,'positive error')),Transform(f[4],spike_ticks(.5)),run_time=.4)
        outcome=label('half the trials: full juice',3.55,-2.4,28,GREEN); self.play(FadeIn(outcome),run_time=.25); self.wait(.5)
        self.at('leaves some surprise'); self.play(Transform(b[2],bar(RX,0,YELLOW)),Transform(g,gap(.5,0,'negative error')),Transform(f[4],spike_ticks(-.5)),Transform(outcome,label('other half: no juice',3.55,-2.4,28,RED)),Transform(f[3][0],label('expected juice time',3.55,1.8,26,YELLOW)),run_time=.5); self.finish()

class S17Earliest(SpokenScene):
    def construct(self):
        y=-.4; w=11.5
        baseline=spike_ticks(0,0,y,w,1.8)
        extra=VGroup(*[Line([x,y,0],[x,y+1.8,0],color=TEXT,stroke_width=2.6) for x in np.linspace(3.5-.55,3.5+.55,15)])
        tone=chip('tone',BLUE,32).move_to([-3.5,-1.7,0]); juice=chip('juice',YELLOW,32).move_to([3.5,-1.7,0])
        title=label('Before learning',0,3.35,36)
        self.add(title,baseline,extra,Arrow([-5.9,y,0],[6.1,y,0],buff=0,color=GREY),tone,juice,label('dopamine neuron firing',0,2.45,30,PURPLE),label('time',5.7,-1,26),label('Tone comes at unpredictable times',0,-2.85,32),DashedLine([-3.5,-.8,0],[-3.5,1.45,0],color=BLUE),DashedLine([3.5,-.8,0],[3.5,1.45,0],color=YELLOW))
        self.at('With learning'); self.wait(1.5)
        self.at('to the tone'); self.play(extra.animate.shift(LEFT*7),Transform(title,label('After learning',0,3.35,36)),run_time=1.1)
        self.at('Good news'); self.play(FadeIn(label('burst: good news',-3.5,1.9,28,GREEN)),FadeIn(label('no change',3.5,1.9,28)),run_time=.4); self.finish()

class S18Hunger(SpokenScene):
    def construct(self):
        b=bars(.5,1); g=gap(.5,1); d=gauge(.85).scale(.95).shift(RIGHT*3.4+DOWN*.3)
        worth=label('worth',RX,2.55,28,YELLOW)
        link=Arrow([1.9,.2,0],[-1.55,.2,0],buff=0,color=YELLOW)
        state=label('greater worth',3.4,1.8,30,YELLOW)
        self.add(b,g,d,worth,link,state,label('Worth changes the error',0,3.45,34),label('hunger / satiety',3.4,-1.3,30),label('a modelling idea',-3.55,-3.6,28))
        self.at('Hunger and satiety')
        low=label('worth',RX,BASE+.25*SCALE+.3,28,YELLOW)
        lower=label('less worth',3.4,1.8,30,YELLOW)
        explanation=label('worth below prediction',3.4,-2.4,28,RED)
        low_gap=gap(.5,.25,'negative error')
        self.play(Transform(d,gauge(.2).scale(.95).shift(RIGHT*3.4+DOWN*.3)),
                  Transform(b[2],bar(RX,.25,YELLOW)),FadeOut(g),FadeIn(low_gap),
                  worth.animate.move_to(low),FadeOut(state),FadeIn(lower),FadeIn(explanation),run_time=.6)
        self.at('change how much')
        # Clear the negative case together with its explanation as worth rises.
        self.play(Transform(d,gauge(.85).scale(.95).shift(RIGHT*3.4+DOWN*.3)),
                  Transform(b[2],bar(RX,1,YELLOW)),worth.animate.move_to([RX,2.55,0]),
                  FadeOut(lower),FadeIn(state),FadeOut(explanation),FadeOut(low_gap),FadeIn(g),run_time=1)
        self.finish()

class S19Scope(SpokenScene):
    def construct(self):
        s=scope(); s[1][3:].set_opacity(0)
        for row,y in zip(s[1][:3],[1.2,0,-1.2]): row.move_to([0,y,0]).set_opacity(.5)
        self.add(s)
        self.at('Keep the scope'); self.play(s[0].animate.set_stroke(TEAL),run_time=.4)
        self.at('many not all'); self.play(s[1][0].animate.set_color(PURPLE).set_opacity(1),run_time=.4)
        self.at('monkeys and rodents'); self.play(s[1][0].animate.set_opacity(.5),s[1][1].animate.set_color(TEAL).set_opacity(1),s[1][2].animate.set_color(YELLOW).set_opacity(.55),run_time=.4); self.finish()

class S20Scope2(SpokenScene):
    def construct(self):
        s=scope(); s[0].set_stroke(TEAL); s[1][3:].set_opacity(0)
        for row,y,col,opacity in zip(s[1][:3],[1.2,0,-1.2],[PURPLE,TEAL,YELLOW],[.5,1,.55]):
            row.move_to([0,y,0]).set_color(col).set_opacity(opacity)
        self.add(s)
        self.at('It describes a signal')
        # Centre the visible rows, making room as each qualification arrives.
        self.play(s[1][0].animate.move_to([0,1.8,0]).set_opacity(.4),
                  s[1][1].animate.move_to([0,.7,0]).set_opacity(.4),
                  s[1][2].animate.move_to([0,-.4,0]).set_opacity(.4),
                  s[1][3].animate.move_to([0,-1.8,0]),run_time=.3)
        self.play(s[1][3].animate.set_opacity(1),run_time=.3)
        self.at('recording alone'); self.play(Indicate(s[1][3],color=TEAL,scale_factor=1.02),run_time=.6)
        self.at('nothing about pleasure')
        self.play(s[1][0].animate.move_to([0,2.1,0]),s[1][1].animate.move_to([0,.98,0]),
                  s[1][2].animate.move_to([0,-.14,0]),s[1][3].animate.move_to([0,-1.395,0]).set_opacity(.4),
                  s[1][4].animate.set_opacity(1),run_time=.3); self.finish()

class S21Takeaway(SpokenScene):
    def construct(self):
        self.add(label('dopamine neuron firing',0,3.35,30,PURPLE))
        strips=VGroup()
        for x,d,word,col in [(-4.4,1,'better',GREEN),(0,0,'as predicted',TEXT),(4.4,-1,'worse',RED)]:
            strips.add(VGroup(spike_ticks(d,x,-.2,3.3,2),Arrow([x-1.7,-.2,0],[x+1.75,-.2,0],buff=0,color=GREY),DashedLine([x,-.35,0],[x,2.05,0],color=YELLOW),label('juice arrives',x,2.4,26,YELLOW),label(word,x,-1.05,30,col),label('time',x+1.25,-.55,22)))
        eq=label('received − predicted',0,-1.85,42); self.add(strips,eq)
        self.at('Carry one idea'); self.play(Indicate(eq,color=TEAL,scale_factor=1.04),run_time=.4)
        self.at('Dopamine bursts and pauses'); self.play(Indicate(strips[0],color=GREEN,scale_factor=1.03),Indicate(strips[2],color=RED,scale_factor=1.03),run_time=.5)
        self.at('better or worse'); self.play(FadeIn(VGroup(label('Dopamine bursts and pauses report',0,-2.75,34),label('better or worse than predicted.',0,-3.35,34))),run_time=.4)
        self.at('hunger shapes'); self.play(Transform(eq,label('received (worth) − predicted',0,-1.85,34)),run_time=.4); self.finish()

class S22End(EndCard):
    LINE=LINE
    def construct(self):
        self.add(label('received − predicted',0,1.8,46,TEAL))
        a=label('Dopamine bursts and pauses report',0,.2,38)
        b=label('better or worse than predicted.',0,-.6,38)
        self.play(FadeIn(a),FadeIn(b),run_time=.6)
        self.add(label('biochemistrypedia.com',0,-2,26,TEAL)); self.finish()
