"""COLOR MAP: YELLOW tone; GOLD CRH (and prior-chapter shock); BLUE freezing;
ORANGE pressure; TEAL amygdala; PURPLE relay tissue/hippocampus; RED damage;
PINK people; GREY unknowns/axes; GREEN glucocorticoid; ACTH cyan (#65A9F3).
All traces are equations: normalized synthesis/clearance transients, a 24-hour
circadian envelope, and the lesson's ideal 0.89/h oscillator. Not fitted data.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
ORANGE='#F29E4C'
PINK='#E58FB5'
ACTH='#65A9F3'

class SpokenScene(SpokenScene):
    # Exact transcript onset; no default anticipatory lead or cumulative tail.
    def at(self, phrase, lead=0, nth=0):
        rest=self.t_of(phrase,nth)-self.elapsed()
        if rest>.001: self.wait(rest)
    def finish(self):
        if self.narration_s>self.elapsed(): self.wait(self.narration_s-self.elapsed())

def txt(s,x,y,c=TEXT,size=28): return T(s,size,c).move_to([x,y,0])
def heading(s): return txt(s,0,3.25,size=32)
def nbox(s,c=PURPLE,w=3.8,h=1,size=28):
    t=VGroup(*[T(l,size,c) for l in s.split('\n')]).arrange(DOWN,buff=.10)
    r=RoundedRectangle(width=max(w,t.width+.4),height=max(h,t.height+.35),corner_radius=.15,color=c,fill_color=BG,fill_opacity=1)
    return VGroup(r,t)
def arr(a,b,c=GREY): return Arrow(a,b,buff=0,color=c,stroke_width=4,tip_length=.18)
def chain():
    b=[nbox(s,w=6,h=1.1).move_to([0,y,0]) for s,y in zip(['hypothalamus','pituitary','adrenal'],[2.1,0,-2.1])]
    a=[arr(b[i].get_bottom(),b[i+1].get_top()) for i in range(2)]
    return b,a

def graph(xmax=60,xlabel='minutes',y=-.1,h=5.2,ylabel='relative level'):
    ax=Axes(x_range=[0,xmax,xmax/4],y_range=[0,1.4,.35],x_length=10.5,y_length=h,axis_config={'color':GREY,'include_ticks':False,'include_tip':False}).move_to([.45,y,0])
    ticks=VGroup(*[txt(f'{v:g}',*ax.c2p(v,0)[:2],GREY,26).shift(DOWN*.30) for v in np.linspace(0,xmax,5)])
    cap=T(xlabel,26,GREY).next_to(ax,DOWN,buff=.65)
    yl=T(ylabel,26,GREY).rotate(PI/2).next_to(ax,LEFT,buff=.30)
    return ax,VGroup(ax,ticks,cap,yl)
def curve(ax,fn,xmax,c): return ax.plot(fn,x_range=[0,xmax,xmax/800],color=c,stroke_width=4,use_smoothing=False)
def act(t): return .16+(t/4)*np.exp(1-t/4)
def gluc(t): return .16+(t/28)**2*np.exp(2-2*t/28)
def pulse(t):
    if t<=.35: return .22
    return .22+.90*(1-np.exp(-(t-.35)*4))*(.5-.5*np.cos(2*np.pi*.89*(t-.35)))**3
def envelope(t): return .22+.73*(.5+.5*np.cos(2*np.pi*t/24))
def daily(t): return .16+envelope(t)*(.35+.65*(.5+.5*np.cos(2*np.pi*t))**3)
def drop(c=GREEN):
    # Continuous droplet silhouette, rather than a circle with a detached cap.
    d=VMobject(color=c,fill_color=c,fill_opacity=.75)
    d.set_points_as_corners([[0,.65,0],[-.26,.13,0]])
    d.add_cubic_bezier_curve_to(np.array([-.65,-.6,0]),np.array([.65,-.6,0]),np.array([.26,.13,0]))
    d.add_line_to(np.array([0,.65,0]));return d
def rat():
    body=Ellipse(width=2.5,height=1.15,color=BLUE,fill_color=BLUE,fill_opacity=.18)
    head=Ellipse(width=.95,height=.72,color=BLUE).move_to([1.25,.28,0])
    nose=Dot([1.75,.20,0],radius=.055,color=BLUE)
    ear=Circle(.23,color=BLUE).move_to([1.05,.75,0])
    eye=Dot([1.42,.42,0],radius=.045,color=TEXT)
    tail=ArcBetweenPoints([-1.2,0,0],[-2.2,-.4,0],angle=.6,color=BLUE)
    feet=VGroup(*[Line([x,-.45,0],[x+.3,-.65,0],color=BLUE) for x in [-.7,.7]])
    return VGroup(body,head,nose,ear,eye,tail,feet)
def dial(x,y,label,c=GREEN,r=1.45):
    face=Circle(r,color=c).move_to([x,y,0])
    ticks=VGroup(*[Line(face.get_center()+r*.88*np.array([np.cos(a),np.sin(a),0]),face.get_center()+r*np.array([np.cos(a),np.sin(a),0]),color=c) for a in np.linspace(0,TAU,13)])
    hand=Line(face.get_center(),face.get_center()+UP*r*.75,color=c,stroke_width=6)
    return VGroup(face,hand,ticks,txt(label,x,y-r-.45,c))
def pump():
    barrel=Rectangle(width=1.1,height=.42,color=GOLD).move_to([-4.9,2.45,0])
    plunger=VGroup(Line([-5.7,2.45,0],[-5.45,2.45,0],color=GOLD),Line([-5.7,2.15,0],[-5.7,2.75,0],color=GOLD))
    tube=Line([-4.35,2.45,0],[5.7,2.45,0],color=GOLD,stroke_width=4)
    return VGroup(barrel,plunger,tube,txt('constant CRH · steady drip',.2,3.12,GOLD))
def experiment(question=False):
    ax,g=graph(6,'hours of infusion',y=-.30,h=4.55,ylabel='corticosterone, relative')
    p=pump();q=nbox('What should you see?',GREY,w=5.6).move_to([.8,.4,0])
    return VGroup(g,p,*([q] if question else [])),ax,q

def person():
    head=Circle(.48,color=PINK).move_to([0,1.7,0])
    torso=RoundedRectangle(width=1.9,height=2.4,corner_radius=.6,color=PINK,fill_color=PINK,fill_opacity=.10).move_to([0,-.15,0])
    arms=VGroup(Line([-.92,.55,0],[-1.12,-.85,0],color=PINK),Line([.92,.55,0],[1.12,-.85,0],color=PINK))
    return VGroup(head,torso,arms)

class S00Title(TitleCard):
    LESSON='Emotion and Stress'
    TITLE='The Slow Route, and Where the Map Stops'
    def construct(self):
        self.add(VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T(self.LESSON,28,GREY),T('The Slow Route,',46,font=TITLE_FONT),T('and Where the Map Stops',44,font=TITLE_FONT),Line(LEFT,RIGHT,color=GOLD)).arrange(DOWN,buff=.4))
        self.wait(3)

class S01Question(SpokenScene):
    def construct(self):
        self.add(heading('The slow route, and where the map stops'),rat().scale(1.1).move_to([-3.3,1.8,0]),drop().scale(1.2).move_to([3.2,1.8,0]))
        f=dial(-3.3,-.7,'freezing · seconds',BLUE,r=1.2);s=dial(3.2,-.7,'hormone · minutes',GREEN,r=1.2)
        self.at('Freezing begins');self.add(f,txt('frozen',-3.3,2.85,BLUE))
        self.play(Rotate(f[1],-TAU*2,about_point=f[0].get_center()),run_time=1.7,rate_func=linear)
        self.at('So why');self.add(s,txt('Why does the hormone peak so much later?',0,-3.25,size=30))
        self.play(Rotate(s[1],-PI/6,about_point=s[0].get_center()),run_time=2.6,rate_func=linear);self.finish()

class S02ThreeStops(SpokenScene):
    def construct(self):
        b,a=chain();self.add(heading('H P A axis'),*b,*a)
        for p,i in [('hypothalamus',0),('pituitary',1),('adrenal',2)]:
            self.at(p);self.play(Indicate(b[i],scale_factor=1.06),run_time=.35)
        self.finish()

class S03Crh(SpokenScene):
    def construct(self):
        b,a=chain();self.add(heading('H P A axis'),*b,*a)
        vessels=VGroup(*[Line([x,1.55,0],[x,.55,0],color=GREY,stroke_width=3) for x in [-.18,.18]])
        dots=VGroup(*[Dot([0,1.4+i*.06,0],radius=.07,color=GOLD) for i in range(3)])
        self.at('release');self.remove(a[0]);self.play(Create(vessels),FadeIn(dots),run_time=.35)
        self.at('into tiny vessels');self.add(txt('CRH · tiny portal vessels',3.4,1.05,GOLD,26));self.play(dots.animate.shift(DOWN*.75),run_time=1.1)
        self.at('lead to');self.play(Indicate(b[1]),run_time=.5);self.finish()

class S04Acth(SpokenScene):
    def construct(self):
        b,a=chain();self.add(heading('H P A axis'),*b,*a)
        blood=VGroup(*[Line([-5.7,y,0],[5.7,y,0],color=GREY,stroke_width=4) for y in [-.8,-1.5]])
        dots=VGroup(*[Dot([-4+i*.45,-1.15,0],radius=.11,color=ACTH) for i in range(5)])
        self.at('releasing');self.play(Create(blood),FadeIn(dots),run_time=.35)
        self.at('into the general');self.add(txt('ACTH · general circulation',0,-3.18,ACTH,28));self.play(dots.animate.shift(RIGHT*7),run_time=1.2);self.finish()

class S05Cortex(SpokenScene):
    def construct(self):
        mini=VGroup(*[nbox(s,w=3,size=26).move_to([-4.75,y,0]) for s,y in zip(['hypothalamus','pituitary','adrenal'],[2,0,-2])])
        self.add(mini,arr(mini[0].get_bottom(),mini[1].get_top()),arr(mini[1].get_bottom(),mini[2].get_top()))
        outer=Ellipse(width=4.3,height=5.1,color=PURPLE,stroke_width=22).move_to([.4,.1,0]);inner=Ellipse(width=3.2,height=4,color=GREY).move_to(outer)
        self.add(outer,inner,txt('adrenal cortex',.4,-3.05,PURPLE),heading('The adrenal makes the hormone'))
        d=Dot([-2.9,1.6,0],radius=.15,color=ACTH);self.add(d,txt('ACTH',-2.8,1.1,ACTH))
        self.at('reaches the adrenal');self.play(d.animate.move_to(outer.get_left()),Indicate(outer),run_time=.7)
        products=VGroup(*[drop().move_to([3.4+i*.7,.5,0]) for i in range(3)])
        self.at('makes cortisol');self.play(FadeIn(products),run_time=.4);self.add(txt('cortisol',4.25,1.6,GREEN))
        self.at('or corticosterone');self.add(txt('(corticosterone',4.2,-.7,GREEN,26),txt('in rats)',4.2,-1.2,GREEN,26));self.finish()

class S06Tens(SpokenScene):
    def construct(self):
        ax,g=graph();self.add(g,heading('Synthesis sets the slow clock · schematic'))
        self.at('within minutes');self.play(Create(curve(ax,act,60,ACTH)),run_time=.6);al=txt('ACTH',-2.1,1.25,ACTH);self.add(al,arr(al.get_left()+LEFT*.15,ax.c2p(8,act(8)),ACTH))
        self.at('adrenal must make');self.play(Create(curve(ax,gluc,60,GREEN)),run_time=.7)
        self.at('levels peak');lab=txt('cortisol (corticosterone in rats)',2.5,-.7,GREEN,26);self.add(lab,arr(lab.get_top(),ax.c2p(43,gluc(43)),GREEN))
        p1=ax.c2p(4,1.30);p2=ax.c2p(28,1.30)
        self.add(Line(p1,p2,color=GOLD),Line(p1+DOWN*.12,p1+UP*.12,color=GOLD),Line(p2+DOWN*.12,p2+UP*.12,color=GOLD),txt('lag: adrenal makes the hormone',-1.4,2.65,GOLD,26));self.finish()

class S07Feedback(SpokenScene):
    def construct(self):
        b,a=chain();self.add(*b,*a)
        fb=VGroup(CurvedArrow(b[2].get_right(),b[0].get_right(),angle=PI/1.6,color=GREEN),CurvedArrow(b[2].get_left(),b[1].get_left(),angle=-PI/1.5,color=GREEN))
        self.at('feeds back');self.play(Create(fb),run_time=.55)
        self.at('turns down');self.add(txt('−',3.8,2.7,GREEN,72),txt('−',-3.8,.65,GREEN,72))
        self.at('A low baseline');self.clear();ax,g=graph(120);self.add(g,heading('Feedback limits further release'))
        self.add(DashedLine(ax.c2p(0,.16),ax.c2p(120,.16),color=GREY),txt('continuing low baseline',3.1,-2.35,GREEN,26))
        self.play(Create(curve(ax,gluc,120,GREEN)),run_time=.55)
        lab=txt('feedback turns it down',.8,2.5,GREEN,26);self.add(lab,arr(lab.get_bottom(),ax.c2p(28,gluc(28)),GREEN),Dot(ax.c2p(28,gluc(28)),radius=.10,color=GREEN));self.finish()

class S08TwoSpeeds(SpokenScene):
    def construct(self):
        f=dial(-2.6,.1,'fast',GREEN,r=1.65)
        self.add(heading('Feedback thermostat · two speeds'),f,txt('hormone output',3.2,2.1,GREEN))
        frame=Rectangle(width=2,height=3.8,color=GREY).move_to([3.2,-.2,0]);level=Rectangle(width=1.8,height=3.4,fill_color=GREEN,fill_opacity=.65,stroke_width=0).align_to(frame,DOWN).move_to([3.2,-.3,0]);self.add(frame,level)
        self.at('A fast arm');self.play(Rotate(f[1],-PI/2,about_point=f[0].get_center()),level.animate.stretch_to_fit_height(.9).align_to(frame,DOWN),run_time=.8)
        self.at('seconds to minutes');self.add(txt('fast: seconds to minutes, nongenomic',0,-3.1,GREEN,28));self.finish()

class S09SlowArm(SpokenScene):
    def construct(self):
        s=dial(-4.1,.9,'slow',GREEN,r=1.45);self.add(s)
        cell=Ellipse(width=6.4,height=5.5,color=GREY).move_to([2,.0,0]);nuc=Ellipse(width=4,height=3.8,color=GREY).move_to([2.6,0,0]);self.add(cell,nuc,txt('cell',.2,2.1,GREY),txt('nucleus',3.0,2.15,GREY))
        rec=nbox('receptor',GREEN,w=2,h=.65,size=26).move_to([-2.25,-1.7,0]);self.add(rec)
        self.at('A slow arm');self.play(Rotate(s[1],-PI/3,about_point=s[0].get_center()),run_time=.6)
        self.at('changing which genes');self.add(arr(rec.get_right()+RIGHT*.12,[1.35,-.65,0],GREEN));self.play(rec.animate.move_to([2.6,-.65,0]),run_time=.5)
        genes=Rectangle(width=2.6,height=.35,color=GREY).move_to([2.6,.4,0]);self.add(genes,txt('genes',2.6,.85,GREY,26));self.play(genes.animate.set_fill(GREEN,opacity=.8).set_color(GREEN),run_time=.35)
        self.at('over hours');self.add(txt('hours to days · genomic',0,-3.25,GREEN,30));self.finish()

class S10Rhythm(SpokenScene):
    def construct(self):
        ax,g=graph(24,'hours since start of active phase');self.add(g,heading('Baseline hormone · idealized'))
        broad=curve(ax,envelope,24,GREEN)
        self.at('rises and falls');self.play(Create(broad),run_time=1.6)
        self.at('daily rhythm');self.add(txt('peak near active-phase onset',1.7,2.5,GREEN,26))
        self.at('pulses about');self.play(Transform(broad,curve(ax,daily,24,GREEN)),run_time=.8);self.finish()

class S11Command(SpokenScene):
    def construct(self):
        ax,g=graph(24,'hours since start of active phase');self.add(g,curve(ax,daily,24,GREEN))
        box=nbox('hypothalamus\neach pulse a command?',GREY,w=5.5,h=1.2,size=26).move_to([2.8,2.2,0])
        self.at('each hourly pulse');self.add(box)
        marks=VGroup(*[Circle(.13,color=GREEN).move_to(ax.c2p(t,daily(t))) for t in [1,2,3]])
        self.play(Create(marks),run_time=.4);self.add(CurvedArrow(box.get_left(),marks.get_right(),angle=.3,color=GREY),txt('?',-1.9,2.6,GREY,36));self.finish()

class S12Walker(SpokenScene):
    def construct(self):
        ax,g=graph(6,'hours of infusion',y=-.30,h=4.55,ylabel='corticosterone, relative');self.add(g,heading('Walker and colleagues · 2012'))
        r=rat().scale(1.25).move_to([0,1.3,0]);self.add(r)
        self.play(Create(curve(ax,lambda t:.22,6,GREEN)),run_time=.5);self.add(txt('daily low point',3,-1.62,GREEN,26))
        self.at('tested this in rats');self.play(Indicate(r),run_time=.4)
        self.at('own CRH is low');self.add(txt('own CRH expected low',0,2.55,GOLD,28))
        self.at('new pulses were unlikely');self.add(txt('unlikely to be its own commands',0,-.1,GREY,26));self.finish()

class S13Predict(SpokenScene):
    def construct(self):
        e,ax,q=experiment();self.add(e[0])
        self.at('dripped in');self.add(e[1][0],e[1][1],e[1][3])
        self.at('perfectly steady rate');self.play(Create(e[1][2]),run_time=.7)
        self.at('what should you see');self.play(FadeIn(q),run_time=.3);self.finish()

class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;e,ax,q=experiment(True);self.add(e)
        ring=Circle(.40,color=GOLD).move_to([4.75,.4,0]);self.add(ring)
        self.play(Uncreate(ring),run_time=5,rate_func=linear)

class S15Reveal(SpokenScene):
    def construct(self):
        e,ax,q=experiment(True);self.add(e)
        prediction=curve(ax,lambda t:.75,6,GREY);label=txt('if every pulse were a command: steady, raised',.5,1.1,GREY,26)
        self.at('steady raised level');self.remove(q);self.play(Create(prediction),FadeIn(label),run_time=.5)
        self.at('Instead');self.remove(prediction,label)
        self.at('still rose and fell');self.play(Create(curve(ax,pulse,6,GREEN)),run_time=.9)
        self.at('about once an hour');self.add(txt('≈ 0.89 pulses/hour · idealized',1.8,1.65,GREEN,26));self.finish()

class S16Meaning(SpokenScene):
    def construct(self):
        h=nbox('hypothalamus: own CRH expected low,\nnot measured or controlled',GREY,w=10.8,size=26).move_to([0,2.65,0])
        p=nbox('pituitary',PURPLE,w=3.7,h=1.1).move_to([-2.7,-.1,0]);a=nbox('adrenal',PURPLE,w=3.7,h=1.1).move_to([2.7,-.1,0]);self.add(h,p,a)
        infusion=nbox('IV: constant CRH · 0.5 µg/h',GOLD,w=6,size=26).move_to([-2.6,1.4,0])
        self.at('pulsed CRH was not needed');self.play(Circumscribe(h,color=GOLD,stroke_width=3),run_time=.5)
        self.add(infusion,arr(infusion.get_bottom(),p.get_top(),GOLD))
        self.at('Given a steady infusion');self.add(arr(p.get_right(),a.get_left(),ACTH),txt('ACTH',0,.4,ACTH,26))
        back=VMobject(color=GREEN,stroke_width=5).set_points_smoothly([a.get_right(),[5.5,-.65,0],[0,-.95,0],[-5.5,-.65,0],[-5.0,-.1,0]]);self.add(back,Arrow([-5.0,-.1,0],p.get_left(),buff=0,color=GREEN,stroke_width=5,tip_length=.3,max_tip_length_to_length_ratio=.5),txt('−',-5.3,.4,GREEN,72))
        ap=Axes(x_range=[0,3,1],y_range=[0,1.4,.5],x_length=3.8,y_length=1.65,axis_config={'color':GREY,'include_ticks':False,'include_tip':False}).move_to([-2.7,-1.85,0])
        aa=ap.copy().move_to([2.7,-1.85,0])
        # Mini-plot labels are separate, unscaled 26pt text.
        self.add(ap,aa,txt('ACTH first',-2.7,-3.0,ACTH,26),txt('corticosterone later',2.7,-3.0,GREEN,26),txt('relative level · schematic time →',0,-3.55,GREY,26))
        self.play(Create(curve(ap,lambda t:.2+.9*np.exp(-((t-.7)/.27)**2),3,ACTH)),run_time=.35)
        self.at('pituitary');self.play(Create(curve(aa,lambda t:.2+.9*np.exp(-((t-1.2)/.32)**2),3,GREEN)),run_time=.3);self.finish()

class S17Edges(SpokenScene):
    def construct(self):
        self.add(heading('Edge 1 of 3 · learning a place'))
        chamber=Rectangle(width=5.3,height=4.8,color=GREY).move_to([-3.05,-.15,0])
        patterns=VGroup(*[Line([-5.65+i*.7,2.2,0],[-5.25+i*.7,1.5,0],color=GREY) for i in range(7)])
        self.add(chamber,patterns,txt('distinctive chamber',-3.05,-3.05,GREY,26),rat().scale(1.15).move_to([-3.05,-.5,0]))
        brain=Ellipse(width=5.5,height=4.7,color=GREY).move_to([3,-.1,0]);amy=Ellipse(width=1.1,height=.8,color=TEAL,fill_color=TEAL,fill_opacity=.4).move_to([2,-1,0]);hip=Ellipse(width=2.4,height=.9,color=PURPLE).rotate(.3).move_to([3.4,.65,0])
        self.add(brain,amy,hip,txt('amygdala',2.1,-2,TEAL),txt('hippocampus',3.5,1.7,PURPLE))
        self.at('learning about a place');self.play(Indicate(chamber),run_time=.5)
        self.at('also needed the hippocampus');self.play(hip.animate.set_fill(PURPLE,opacity=.65),run_time=.3);self.play(Circumscribe(hip,color=PURPLE),run_time=.5);self.finish()

class S18Knowing(SpokenScene):
    def construct(self):
        self.add(heading('Edge 2 of 3 · knowing and responding'),person().scale(1.5).move_to([-4.25,-.4,0]))
        self.at('damage to both amygdalae');self.add(nbox('both amygdalae damaged',RED,w=6,size=26).move_to([2,2.2,0]))
        bubble=nbox('“This went with that.”',PINK,w=5.7,h=1.3).move_to([2,.6,0]);tail=Polygon([-2.7,1,0],[-.9,.9,0],[-.9,.4,0],color=PINK,fill_color=BG,fill_opacity=1)
        self.at('could still say');self.add(tail,bubble)
        self.at('learned bodily response')
        ax=Axes(x_range=[0,10,5],y_range=[0,1.4,.7],x_length=6.4,y_length=2.0,axis_config={'color':GREY,'include_ticks':False,'include_tip':False}).move_to([2,-1.9,0])
        line=curve(ax,lambda t:0,10,GREY).set_stroke(width=7)
        self.add(ax,line,txt('0',ax.c2p(0,0)[0],-3.25,GREY,26),txt('10 s',ax.c2p(10,0)[0],-3.25,GREY,26),txt('learned autonomic response: absent',2,-1.3,GREY,26),txt('seconds after stimulus',2,-3.65,GREY,26));self.finish()


class S19Co2(SpokenScene):
    def construct(self):
        self.add(heading('Edge 3 of 3 · one breath of CO2'))
        puff=VGroup(*[Circle(r,color=GREY).move_to([-5.1+i*.55,.9+(.15 if i%2 else 0),0]) for i,r in enumerate([.3,.45,.55])]);self.add(puff,txt('one breath',-4.4,2.0,GREY));self.at('one breath');self.play(puff.animate.shift(RIGHT*.5).scale(1.2),run_time=.8)
        dots=VGroup(*[Circle(.56,color=PINK).move_to([-.6+i*2.4,1.15,0]) for i in range(3)])
        self.at('made three women');self.add(dots,arr(puff.get_right(),dots.get_left()))
        self.at('panic');self.play(dots.animate.set_fill(PINK,opacity=.85),run_time=.25);self.add(txt('3 of 3 patients panicked',1.8,2.35,PINK,32))
        comp=VGroup(*[Circle(.34,color=GREY,fill_color=GREY,fill_opacity=.85 if i<3 else 0).move_to([-3.6+(i%6)*1.45,-1.0-(i//6)*1.0,0]) for i in range(12)])
        self.add(comp,txt('3 of 12 comparison women',0,-2.95,GREY,30))
        self.at('one rare disease');self.add(txt('one rare disease',1.8,.15,PINK,28));self.finish()

class S20Feeling(SpokenScene):
    def construct(self):
        # Same chapter-one layout: tone and lateral/central amygdala at left;
        # PAG/freezing, lateral hypothalamus/pressure, HPA/hormone in three rows.
        tone=nbox('tone',YELLOW,w=2.7,size=26).move_to([-4.9,2.3,0]);la=nbox('lateral\namygdala',TEAL,w=2.7,size=26).move_to([-4.9,.65,0]);ce=nbox('central\namygdala',TEAL,w=2.7,size=26).move_to([-4.9,-1.2,0])
        targets=[nbox(s,c,w=3.6,size=26).move_to([-.2,y,0]) for s,c,y in [('PAG, midbrain',BLUE,1.9),('lateral\nhypothalamus',ORANGE,0),('hypothalamus\npituitary → adrenal',GREEN,-2)]]
        outs=[nbox(s,c,w=2.7,size=26).move_to([4.25,y,0]) for s,c,y in [('freezing',BLUE,1.9),('pressure rise',ORANGE,0),('hormone',GREEN,-2)]]
        self.add(tone,la,ce,arr(tone.get_bottom(),la.get_top(),YELLOW),arr(la.get_bottom(),ce.get_top(),TEAL),*targets,*outs)
        for t,o,c in zip(targets,outs,[BLUE,ORANGE,GREEN]):
            link=arr(ce.get_right(),t.get_left(),c)
            self.add(DashedVMobject(link,num_dashes=12) if c==GREEN else link,arr(t.get_right(),o.get_left(),c))
        map_group=VGroup(*self.mobjects);self.remove(*self.mobjects);map_group.scale(.87).shift(UP*.1);self.add(map_group)
        cards=[nbox('1 Place + hippocampus',GREY,w=5.0,h=.65,size=26).move_to([-3.2,3.2,0]),nbox('2 Stated pairing',GREY,w=3.9,h=.65,size=26).move_to([-4.1,-3.2,0]),nbox('3 CO2 panic',GREY,w=3.6,h=.65,size=26).move_to([4.0,3.2,0])]
        self.add(*cards,Line([-6.4,2.75,0],[-6.4,-2.75,0],color=GREY),Line([6.4,2.75,0],[6.4,-2.75,0],color=GREY),txt('HPA input mostly indirect',-.1,-2.85,GREEN,24))
        self.at('necessary steps');self.play(Indicate(ce),run_time=.5)
        self.at('what is felt');self.play(FadeIn(nbox('What is felt?',GREY,w=3.7,h=.7,size=30).move_to([3.8,-3.2,0])),run_time=.25);self.finish()

class S21Takeaway(SpokenScene):
    def construct(self):
        self.add(heading('In rats: learning an outside threat'))
        amy=nbox('amygdala needed',TEAL,w=5.6).move_to([0,1.9,0]);fast=nbox('fast neural routes',BLUE,w=5).move_to([-3.3,-.05,0]);slow=nbox('slower hormone route',GREEN,w=5).move_to([3.3,-.05,0]);syn=nbox('adrenal hormone synthesis',GREEN,w=6).move_to([2,-2.15,0])
        self.add(amy)
        r=rat().scale(1.65).move_to([0,-.6,0]);learned=txt('learned outside threat',0,-2.3,TEAL,30);opening_link=arr(amy.get_bottom(),r.get_top()+UP*.08,TEAL);self.add(r,learned,opening_link)
        self.at('learn an outside threat');self.play(Indicate(amy),run_time=.45)
        self.at('respond fast');self.remove(r,learned,opening_link);self.add(fast,arr(amy.get_left(),fast.get_top(),BLUE))
        self.at('is slower');self.add(slow,Line(amy.get_right(),[6.1,1.9,0],color=GREEN),Line([6.1,1.9,0],[6.1,-.05,0],color=GREEN),arr([6.1,-.05,0],slow.get_right(),GREEN),txt('indirectly: releases the brake',2.7,1.04,GREEN,26))
        self.at('adrenal must make');self.add(syn,arr(slow.get_bottom(),syn.get_top(),GREEN))
        self.at('its hormone');self.play(FadeIn(txt('The map has edges',0,-3.35,GREY,30)),run_time=.35);self.finish()

class S22End(EndCard):
    LINE='Fast neural routes, a slower hormone route: the map has edges.'
    def construct(self):
        self.add(VGroup(T('Fast neural routes, a slower hormone route:',36,font=TITLE_FONT),T('the map has edges.',40,font=TITLE_FONT),T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.55))
        self.wait(3.5)
