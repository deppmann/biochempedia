"""Chapter 3 — computed, illustrative schematics, never recordings.
COLOR MAP: BLUE outer hair cells/channel; YELLOW input; TEAL emission;
GREY passive structure; RED absent; GOLD living gain; GREEN contraction.
Model: x=.5 cos(2π2000t)+.5 cos(2π2400t); y=x-.3x³, |x|<=1.
FFT uses exact 40-Hz bins. Spectral height is a logarithmic arbitrary scale.
Ear return transfer 1/(1+(f/1900)^6) is illustrative, not a fitted measurement.
Waveform close-ups drive the cubic harder, with a constant continuation beyond
its stationary points (saturating cubic, never the unphysical foldback).
Click impulse Gaussian; delayed tail tau=14 ms. Seeded noise is averaged.
Gain: smooth saturating enhancement; spatial envelopes asymmetric Gaussians.
"""
import numpy as np
from bp_style import *
LESSON='The Cochlear Amplifier and Otoacoustic Emissions'
GREY='#B7BFCC'

def head(s,c=TEXT): return T(s,32,c).move_to([0,3.25,0])
def txt(s,x,y,c=TEXT,size=26): return T(s,size,c).move_to([x,y,0])
def axes(w,h,xr,yr,pos=(0,0)):
    return Axes(x_range=[*xr,(xr[1]-xr[0])/4],y_range=[*yr,(yr[1]-yr[0])/4],x_length=w,y_length=h,tips=False,axis_config={'color':GREY,'include_ticks':False,'stroke_width':2}).move_to([*pos,0])
def curve(ax,fn,xr,c,step=None,w=5):
    xs=np.linspace(*xr,601) if step is None else np.arange(xr[0],xr[1]+step/2,step)
    return VMobject(color=c,stroke_width=w).set_points_as_corners([ax.c2p(x,fn(x)) for x in xs])
def nl(x):return x-.3*x**3
def sat(x):return nl(np.clip(x,-np.sqrt(1/.9),np.sqrt(1/.9)))
def summed(t):return 1.7*(.5*np.cos(2*PI*2*t)+.5*np.cos(2*PI*2.4*t))
def tick(ax,x,label,y=0,c=GREY):
    p=ax.c2p(x,y)
    return VGroup(Line(p+DOWN*.07,p+UP*.07,color=GREY),txt(label,p[0],p[1]-.33,c))
def spiral(x,y,r=1,c=GREY):
    ts=np.linspace(0,4.5*PI,300)
    return VMobject(color=c,stroke_width=5).set_points_as_corners([[x+r*.085*t*np.cos(t),y+r*.085*t*np.sin(t),0] for t in ts])
def sound(x,y,c=TEAL):
    return VMobject(color=c,stroke_width=5).set_points_as_corners([[x+t,y+.23*np.sin(4*PI*t),0] for t in np.linspace(0,1,100)])
def canal():
    body=Polygon([-4.7,2,0],[-1,1.05,0],[2.5,.8,0],[2.5,-.8,0],[-1,-1.05,0],[-4.7,-2,0],color=GREY,fill_opacity=.07)
    seal=Line([-4.7,-2,0],[-4.7,2,0],color=GREY,stroke_width=9)
    mic=RoundedRectangle(width=.5,height=.9,corner_radius=.1,color=TEAL,fill_opacity=.3).move_to([-4.15,0,0])
    co=spiral(4.2,0,.85)
    return VGroup(body,seal,mic,co,Line([2.5,0,0],[3.3,-.7,0],color=GREY),txt('microphone',-4,2.55,TEAL),txt('sealed ear canal',-.8,-2.35,GREY),txt('cochlea',4.2,1.6,BLUE))
def click(t):return 1.1*np.exp(-((t-.7)/.22)**2)
def tail(t):return .65*np.exp(-(t-5)/14)*np.sin(2*PI*.8*(t-5)) if t>=5 else 0

def io(pos=(0,-.15),w=8,h=5.3):
    ax=axes(w,h,(-1.12,1.12),(-.85,.85),pos)
    labels=VGroup(txt('input',pos[0]+w/2-.2,-3.1,GREY),txt('output',pos[0]-w/2+.1,2.75,GREY))
    return VGroup(ax,curve(ax,nl,(-1,1),BLUE),labels)
def inputs(x=-4.35,y=-.2):
    ax=axes(3,2.9,(1700,2700),(0,1),(x,y))
    bars=VGroup(*[Line(ax.c2p(f,0),ax.c2p(f,.85),color=YELLOW,stroke_width=9) for f in (2000,2400)])
    labs=VGroup(*[tick(ax,f,s) for f,s in [(2000,'2,000'),(2400,'2,400')]],txt('frequency (Hz)',x,y-2.2,GREY),txt('amplitude',x,y+1.95,GREY))
    return VGroup(ax,bars,labs)
_tt=np.arange(1200)/48000
_x=.5*np.cos(2*PI*2000*_tt)+.5*np.cos(2*PI*2400*_tt)
_fft=2*np.abs(np.fft.rfft(nl(_x)))/len(_x)
_freq=np.fft.rfftfreq(len(_x),1/48000)
def amp(f):return float(_fft[np.argmin(abs(_freq-f))])
FS=(1600,2000,2400,2800)
def spectrum(kind='toy'):
    ax=axes(10.5,4.65,(1200,3200),(0,1),(0,-.05))
    bars=VGroup()
    for f in FS:
        a=amp(f)
        if kind=='linear':a=.5 if f in (2000,2400) else 0
        if kind=='ear':a*=1/(1+(f/1900)**6)
        level=max(0,(20*np.log10(max(a,1e-9)/.5)+55)/55)
        bars.add(Line(ax.c2p(f,0),ax.c2p(f,max(.0001,level)),color=YELLOW if f in (2000,2400) else TEAL,stroke_width=11))
    labs=VGroup(*[tick(ax,f,f'{f:,}') for f in FS],txt('frequency (Hz)',0,-3.1,GREY),T('relative amplitude (arbitrary)',26,GREY).rotate(PI/2).move_to([-6.15,0,0]),txt('log scale · higher products outside this window',0,2.6,GREY))
    return VGroup(ax,bars,labs)
def prediction():
    sp=spectrum('linear')
    sp[2][-1].become(txt('two input tones remain',0,2.6,YELLOW))
    return VGroup(head('Predict: what else comes out?'),sp,txt('?',sp[0].c2p(1600,0)[0],.1,TEAL,76))
def death_question():
    co=spiral(-3.8,.2,1.1)
    ax=axes(5.9,4.2,(1200,3000),(0,1),(2.5,-.1))
    labels=VGroup(txt('cochlea · after death',-3.7,-1.9,GREY),txt('moderate level',-3.8,2.6,YELLOW),txt('2,000 + 2,400 Hz',-3.8,-2.65,YELLOW),tick(ax,1600,'1,600'),txt('output frequency (Hz)',2.5,-3.1,GREY),txt('amplitude',2.6,2.4,GREY))
    tones=VGroup(Line([-5.4,.1,0],[-5.4,1.3,0],color=YELLOW,stroke_width=8),Line([-4.9,.1,0],[-4.9,1.3,0],color=YELLOW,stroke_width=8),Arrow([-5,.7,0],[-2.2,.7,0],color=YELLOW,buff=.2))
    q=txt('?',ax.c2p(1600,0)[0]+.65,.2,TEAL,70)
    product=Line(ax.c2p(1600,0),ax.c2p(1600,.65),color=TEAL,stroke_width=11)
    return VGroup(head('Predict again: what comes back?'),co,ax,labels,tones,q,product)
def box(lines,x,y,c=BLUE,w=5.1,h=2.3):
    b=RoundedRectangle(width=w,height=h,corner_radius=.18,color=c,fill_opacity=.08).move_to([x,y,0])
    ls=VGroup(*[T(s,26,c if i==0 else TEXT) for i,s in enumerate(lines)]).arrange(DOWN,buff=.25).move_to(b)
    return VGroup(b,ls)
def ear():
    outline=Ellipse(width=2.3,height=3.1,color=GREY).move_to([-4.65,.75,0])
    canalbody=Rectangle(width=4.3,height=1.1,color=GREY,fill_opacity=.08).move_to([-2.4,.6,0])
    drum=Line([-.2,-.1,0],[-.2,1.3,0],color=GREY,stroke_width=5)
    middle=Line([-.1,.7,0],[2.6,.7,0],color=GREY,stroke_width=6)
    co=spiral(3.35,.6,.8,BLUE)
    probe=RoundedRectangle(width=.55,height=.9,corner_radius=.1,color=TEAL,fill_opacity=.3).move_to([-4.2,.6,0])
    return VGroup(outline,canalbody,drum,middle,co,probe,txt('probe',-4.25,2.6,TEAL),txt('middle ear',.7,2.1,GREY),txt('cochlea',3.65,2.1,BLUE))

class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='The Sound That Comes Back'
    def construct(self):
        self.add(txt('BIOCHEMISTRYPEDIA',0,2.2,TEAL),txt('The Cochlear Amplifier',0,1.2,GREY),txt('and Otoacoustic Emissions',0,.65,GREY))
        self.play(FadeIn(T(self.TITLE,48,font=TITLE_FONT).move_to([0,-.6,0])),Create(Line([-1.2,-1.4,0],[1.2,-1.4,0],color=GOLD)),run_time=.8);self.finish()
class S01Q(SpokenScene):
    def construct(self):
        self.add(canal(),head('The Sound That Comes Back'))
        w=sound(1,0)
        self.at('send sound back');self.add(w);self.play(w.animate.shift(LEFT*4.8),run_time=.8);self.remove(w)
        self.at('a screening test');self.play(FadeIn(VGroup(txt('Why would a healthy ear send sound back out?',0,-2.95,TEAL),txt('What can a screening test learn from it?',0,-3.55,TEAL))),run_time=.3);self.finish()
class S02Kemp(SpokenScene):
    def construct(self):
        g=canal();self.add(g,head('Kemp · 1978'))
        self.at('brief clicks');p=VMobject(color=YELLOW,stroke_width=6).set_points_as_corners([[-4.1,0,0],[-3.95,0,0],[-3.9,.7,0],[-3.85,0,0],[-3.7,0,0]])
        self.play(Create(p),run_time=.12);self.play(p.animate.shift(RIGHT*6),run_time=1.05,rate_func=linear)
        self.at('human ear canals');self.play(FadeOut(g),FadeOut(p),run_time=.2)
        rng=np.random.default_rng(1978);ts=np.linspace(0,35,480)
        rows=[];values=[]
        for i in range(6):
            vals=np.array([click(t)+tail(t) for t in ts])+rng.normal(0,.19,len(ts));values.append(vals)
            rows.append(VMobject(color=GREY,stroke_width=1.5).set_points_as_corners([[-5.6+t/35*11.2,2.2-i*.76+v*.25,0] for t,v in zip(ts,vals)]))
        traces=VGroup(*rows);self.play(Create(traces),run_time=.4)
        self.at('and averaged');ax=axes(11.1,3.8,(0,35),(-1,1.4),(0,-.35));mean=np.mean(values,axis=0)
        avg=VMobject(color=TEAL,stroke_width=4).set_points_as_corners([ax.c2p(t,v) for t,v in zip(ts,mean)])
        self.play(ReplacementTransform(traces,avg),FadeIn(ax),FadeIn(txt('many clicks, averaged',0,2.6,TEAL)),FadeIn(txt('time after click (ms)',0,-3.1,GREY)),run_time=.7);self.finish()
class S03Echo(SpokenScene):
    def construct(self):
        a=axes(10.8,2.25,(0,35),(-.8,1.3),(0,1.2));b=axes(10.8,2.25,(0,35),(-.8,1.3),(0,-1.65))
        labs=VGroup(txt('normal hearing ear',0,2.65,TEAL),txt('time after click (ms)',0,-3.5,GREY),T('amplitude (arbitrary)',26,GREY).rotate(PI/2).move_to([-6.25,0,0]),*[tick(ax,v,str(v)) for ax in (a,b) for v in (0,5)])
        self.add(head('The response after a click'),a,b,labs,curve(a,click,(0,1.5),YELLOW),curve(b,click,(0,1.5),YELLOW))
        self.at('a slowly decaying');self.play(Create(curve(a,lambda t:click(t)+tail(t),(0,35),TEAL)),run_time=.6)
        self.at('after each click');self.play(Create(DashedLine(a.c2p(5,-.8),a.c2p(5,1.3),color=GREY)),run_time=.3)
        self.at('cochlear deafness');self.play(FadeIn(txt('ear tested with cochlear deafness',1,-.25,YELLOW)),run_time=.3)
        self.at('it was absent');self.play(Create(curve(b,lambda t:0,(1.5,35),YELLOW)),run_time=.4);self.finish()
class S04Two(SpokenScene):
    def construct(self):
        a=box(['reflection','click-evoked','reflected travelling wave'],-3.15,-.1,TEAL,w=5.8,h=5.3)
        b=box(['nonlinearity','distortion product','fast saturating curve'],3.15,-.1,BLUE,w=5.8,h=5.3)
        a[1].shift(DOWN*1.3);b[1].shift(DOWN*1.3)
        w=sound(-5,1);ax=axes(3.5,1.6,(-1,1),(-.8,.8),(3.15,1.1));c=curve(ax,nl,(-1,1),BLUE)
        self.add(head('Two ways sound comes back'),a,b,w,ax,c)
        self.at('reflections of');self.play(w.animate.shift(RIGHT*2.3),run_time=.6);self.play(w.animate.shift(LEFT*2.3),run_time=.6)
        self.at('others come from');self.play(Indicate(c),run_time=.7);self.finish()
class S05Curve(SpokenScene):
    def construct(self):
        g=io();self.add(head('Toy fast nonlinearity',BLUE),g)
        d=Dot(g[0].c2p(-.2,nl(-.2)),color=YELLOW)
        self.at('passes small inputs');self.play(FadeIn(d),run_time=.15);self.play(MoveAlongPath(d,curve(g[0],nl,(-.2,.2),YELLOW)),run_time=.7)
        self.at('flattens large ones');self.play(MoveAlongPath(d,curve(g[0],nl,(.2,1),YELLOW)),run_time=.7)
        self.at('feed it two tones');small=io((2.5,-.15),5.7,5.3);inp=inputs()
        self.play(Transform(g,small),FadeOut(d),FadeIn(inp,shift=RIGHT*.6),run_time=.5)
        ar=Arrow([-2.4,.2,0],[-.7,.2,0],color=YELLOW,buff=0)
        self.play(GrowArrow(ar),run_time=.3)
        wave=sound(-2.4,.2,YELLOW);self.play(Create(wave),run_time=.2);self.play(wave.animate.shift(RIGHT*2),run_time=.55);self.remove(wave);self.finish()
class S06Predict(SpokenScene):
    def construct(self):self.add(prediction());self.at('predict');self.finish()
class S07Pause(Scene):
    def construct(self):self.camera.background_color=BG;self.add(prediction());self.wait(5)
class S08Reveal(SpokenScene):
    def construct(self):
        a=axes(10.5,2.15,(0,2.5),(-1.85,1.85),(0,1.25));b=axes(10.5,2.15,(0,2.5),(-1.85,1.85),(0,-1.55))
        fn=summed
        raw=curve(a,fn,(0,2.5),YELLOW)
        labels=VGroup(txt('two tones added',0,2.65,YELLOW),txt('time (ms) · same amplitude scale',0,-3.45,GREY),T('amplitude (arbitrary)',26,GREY).rotate(PI/2).move_to([-6.25,0,0]))
        for ax in (a,b):
            labels.add(*[tick(ax,x,str(x)) for x in (0,1,2)])
            for y in (-sat(2),sat(2)):labels.add(DashedLine(ax.c2p(0,y),ax.c2p(2.5,y),color=GREY,stroke_opacity=.5))
            for y in (-1,1):labels.add(txt(str(y),-5.65,ax.c2p(0,y)[1],GREY))
        self.add(head('What the curve does to the sum'),a,b,labels,raw)
        self.at('where the two tones');self.play(Indicate(raw,scale_factor=1.01),run_time=.4)
        self.at('the curve squashes');ghost=curve(b,fn,(0,2.5),YELLOW).set_stroke(opacity=.65);out=curve(b,lambda t:sat(fn(t)),(0,2.5),TEAL)
        self.play(FadeIn(ghost),Create(out),FadeIn(txt('after curve',3.9,-.2,TEAL)),run_time=.55)
        ts=np.linspace(0,2.5,2501);ys=np.array([fn(t) for t in ts])
        peaks=[i for i in range(1,len(ts)-1) if abs(ys[i])>abs(ys[i-1]) and abs(ys[i])>=abs(ys[i+1]) and abs(ys[i])>np.sqrt(1/.9)]
        rings=VGroup(*[Circle(radius=.15,color=TEAL,stroke_width=3).move_to(b.c2p(ts[i],sat(ys[i]))) for i in peaks])
        self.play(Create(rings),run_time=.3);self.finish()
class S09Reveal2(SpokenScene):
    def construct(self):
        sp=spectrum();title=head('Toy curve: y = ax − bx³',BLUE)
        self.add(title,sp[0],sp[2],sp[1][1],sp[1][2])
        self.at('a cubic term');self.play(Indicate(title,scale_factor=1.02),run_time=.3)
        self.at('that makes');formula=txt('2f1 − f2 = 2 × 2,000 − 2,400 = 1,600 Hz',0,-3.65,TEAL)
        self.play(Create(sp[1][0]),Create(sp[1][3]),FadeIn(formula),run_time=.4)
        self.at('among other new');self.play(Indicate(sp[1][3]),run_time=.3)
        self.wait(.3)
        # Fade out a complete state: no transform fragments or orphan result labels.
        self.play(FadeOut(VGroup(*sp[1])),FadeOut(formula),FadeOut(title),run_time=.15)
        lin=spectrum('linear');lt=head('Linear y = ax: only f1 and f2',GREY)
        self.add(lin[1][1],lin[1][2],lt);self.wait(.65)
        self.at('in ear canal');self.remove(lin[1][1],lin[1][2],lt,sp[0],sp[2]);earsp=spectrum('ear');self.add(earsp);self.add(head('Schematic ear-canal spectrum',TEAL))
        self.at('usually the largest');self.play(Indicate(earsp[1][0]),run_time=.45);self.finish()
class S10Beat(Scene):
    def construct(self):self.camera.background_color=BG;self.add(spectrum('ear'),head('Schematic ear-canal spectrum',TEAL));self.wait(2)
class S11Predict2(SpokenScene):
    def construct(self):
        g=death_question();self.add(g);self.at('play the same');self.play(Indicate(g[4],scale_factor=1.03),run_time=.6);self.finish()
class S12Pause(Scene):
    def construct(self):self.camera.background_color=BG;self.add(death_question());self.wait(5)
class S13Reveal3(SpokenScene):
    def construct(self):
        g=death_question();self.add(g)
        self.at('usually little');self.remove(g[5],g[0]);self.add(head('Moderate levels: product gone',TEAL))
        self.play(Transform(g[6],Line(g[2].c2p(1600,0),g[2].c2p(1600,.005),color=TEAL,stroke_width=11)),FadeIn(txt('product gone',2.4,.1,TEAL)),run_time=.65)
        self.at('the living drive');self.remove(g[4],g[3][1],g[3][2]);mech=Arrow([-5.8,1.8,0],[-2.2,1.8,0],color=GREY,buff=0,stroke_width=9,max_tip_length_to_length_ratio=.18);elec=mech.copy().shift(DOWN*3.2).set_color(BLUE)
        labs=VGroup(txt('mechanical',-4,2.6,GREY),txt('electrical',-4,-2.65,BLUE))
        self.play(FadeIn(labs),GrowArrow(mech),GrowArrow(elec),run_time=.35);self.play(mech.animate.scale(.15),elec.animate.scale(.15),run_time=.65)
        self.at('that does not mean');self.play(FadeOut(VGroup(g[3][0],mech,elec,labs)),run_time=.15)
        ax=axes(4.3,3.8,(-1.1,1.1),(-.85,.85),(-3.7,-.1))
        self.play(FadeOut(g[1]),FadeIn(ax),Create(curve(ax,nl,(-1,1),BLUE)),FadeIn(txt('transduction channel',-3.6,2.6,BLUE)),FadeIn(txt('output',-5.5,2.05,GREY)),FadeIn(txt('input',-1.8,-2.5,GREY)),run_time=.5)
        self.at('transduction channel');self.remove(g[3][4]);self.play(FadeIn(VGroup(txt('some nonlinearity can remain',0,-3.05,BLUE),txt('(e.g. high levels, prestin-less mice)',0,-3.6,GREY))),run_time=.35);self.finish()
class S14Idea(SpokenScene):
    def construct(self):
        ax=axes(7.3,5.2,(0,100),(0,110),(-1.9,-.1))
        living=lambda x:x+48*(1-np.exp(-x/8))*np.exp(-(x/65)**4)
        xs=np.linspace(0,100,301)
        shade=Polygon(*([ax.c2p(x,living(x)) for x in xs]+[ax.c2p(x,x) for x in xs[::-1]]),stroke_width=0,fill_color=GOLD,fill_opacity=.25)
        self.add(head('One vulnerable process'),ax,curve(ax,lambda x:x,(0,100),GREY),curve(ax,living,(0,100),GOLD),txt('sound level',-1.9,-3.25,GREY),T('motion',26,GREY).rotate(PI/2).move_to([-6.1,0,0]),txt('living',-3.7,1.65,GOLD),txt('after death',-.4,-1.4,GREY),txt('schematic',4.5,2.55,GREY))
        self.at('gives the gain');self.play(FadeIn(shade),run_time=.4)
        self.at('makes the emission');self.play(GrowArrow(Arrow([.1,.5,0],[3.8,.5,0],color=GOLD,stroke_width=7,buff=0)),Create(Rectangle(width=.65,height=3.4,color=TEAL,fill_opacity=.8).move_to([4.5,-.2,0])),FadeIn(txt('emission',4.5,-2.65,TEAL,30)),run_time=.6);self.finish()
class S15Caveat(SpokenScene):
    def construct(self):
        left=axes(5.1,3.8,(0,2.5),(-1.85,1.85),(-3.2,-.1))
        right=axes(5.1,3.8,(0,2.5),(-1.85,1.85),(3.2,-.1))
        raw=curve(left,summed,(0,2.5),YELLOW)
        out=curve(right,lambda t:sat(summed(t)),(0,2.5),TEAL)
        self.add(head('Maths alone'),left,right,raw,txt('two tones added',-3.2,2.35,YELLOW),txt('after fast curve',3.2,2.35,TEAL),txt('time (ms) · same amplitude scale',0,-2.5,GREY),txt('any fast curve mixes tones',0,-3.15,TEAL),txt('once input reaches the bend',0,-3.65,TEAL))
        self.at('makes new tones');self.play(FadeIn(curve(right,summed,(0,2.5),YELLOW).set_stroke(opacity=.5)),Create(out),run_time=.6)
        self.at('input reaches');self.play(Indicate(out,scale_factor=1.02),run_time=.65)
        self.at('what ties this');self.clear();a=box(['outer hair cells'],-3.3,-.1,BLUE,h=3.6);b=box(['emission'],3.3,-.1,TEAL,h=3.6)
        self.add(head('The biological link'),a,b,Arrow(a.get_right(),b.get_left(),color=GREY,buff=.1))
        self.at('at screening levels');self.play(FadeIn(txt('at screening levels the product fails when they fail',0,2.5,GREY)),run_time=.3)
        self.at('it fails when');self.play(a[0].animate.set_color(GREY),b[0].animate.set_color(GREY),FadeIn(txt('fails',-3.3,-1.1,RED,36)),FadeIn(txt('fails',3.3,-1.1,RED,36)),run_time=.5);self.finish()
class S16Screen(SpokenScene):
    def construct(self):
        a=box(['outer hair cells'],-3,-2.35,BLUE,w=5.5,h=1.8);b=box(['nerve + pathway'],3,-2.35,GREY,w=5.5,h=1.8)
        a[1].shift(UP*.35)
        anatomy=ear().scale(1.15).shift(UP*.4)
        anatomy[0].stretch(1.15,1)
        anatomy[6].move_to([-5.4,3.35,0])
        self.add(head('Newborn screening'),anatomy,a,b,Arrow(a.get_right(),b.get_left(),color=GREY,buff=.1))
        self.at('make an emission');w=sound(0,0).scale(.8).move_to(anatomy[4].get_center());self.play(Create(w),run_time=.2)
        self.play(w.animate.move_to(anatomy[3].get_center()),run_time=.55,rate_func=linear)
        self.at('through the middle');self.play(w.animate.move_to(anatomy[5].get_center()),run_time=.8,rate_func=linear)
        self.play(Indicate(anatomy[5],color=TEAL),FadeOut(w),a[0].animate.set_color(TEAL).set_fill(TEAL,opacity=.2),FadeIn(txt('✓ emission received',-3,-2.75,TEAL,30)),run_time=.35);self.finish()
class S17Neuro(SpokenScene):
    def construct(self):
        a=box(['outer hair cells','emission: present'],-3.15,-.1,TEAL,w=5.8,h=4.9)
        b=box(['nerve + pathway','brainstem response','?'],3.15,-.1,GREY,w=5.8,h=4.9)
        title=head('A pass does not show intact hearing',RED);self.add(title,a,b)
        self.at('in auditory neuropathy');self.remove(title);self.add(head('Auditory neuropathy',RED))
        self.at('the brainstem response');self.play(Indicate(b[1][1],scale_factor=1.03),run_time=.3)
        self.at('absent or very');self.remove(b[1][2]);self.play(FadeIn(VGroup(txt('can be absent',3.15,-.9,RED),txt('or very abnormal',3.15,-1.5,RED))),run_time=.35);self.finish()
class S18Open(SpokenScene):
    def construct(self):
        xs=np.linspace(-5.8,2.4,500);site=.6
        def env(p,c,scale=1):return VMobject(color=c,stroke_width=5).set_points_as_corners([[x,-1.8+scale*3.6*np.exp(-.5*((x-p)/(1.1 if x<p else .32))**2),0] for x in xs])
        ax=axes(1.5,4.8,(0,1),(0,1),(4.9,-.1))
        bar=Line(ax.c2p(.5,0),ax.c2p(.5,.9),color=GOLD,stroke_width=22)
        probe=env(site,GOLD)
        self.add(head('How far along is gain gathered?'),Line([-5.8,-1.8,0],[2.4,-1.8,0],color=GREY),DashedLine([site,-2,0],[site,2.2,0],color=GREY),txt('measured site',1,2.7),txt('base',-5.3,-2.3,GREY),txt('apex',2,-2.3,GREY),probe,ax,bar,txt("probe tone’s envelope",-3,2.7,GOLD),T('response at site',26,GREY).rotate(PI/2).move_to([6.15,0,0]))
        pointer=Arrow([site,2.35,0],[site,1.5,0],color=GOLD,buff=0)
        marker=Dot([site,1.8,0],color=GOLD,radius=.09)
        self.add(pointer,marker)
        # Keep the measured site active throughout the opening question.
        for _ in range(3):self.play(Indicate(marker,scale_factor=2.4),run_time=.85);self.wait(.55)
        self.at('a second tone');self.remove(pointer,marker);e=env(-.3,TEAL);lab=txt('second (suppressing) tone',-2.5,-2.95,TEAL);self.add(lab);self.play(Create(e),run_time=.4)
        def response(p):
            # Local overlap proxy: near basal peaks suppress, distant peaks do not.
            return .9*(1-.72*np.exp(-.5*((p-site)/1.0)**2))
        def state(p):
            q=response(p)
            # Fade to black between positions: never interpolate two envelope peaks.
            self.play(FadeOut(e),run_time=.15)
            e.become(env(p,TEAL))
            self.play(FadeIn(e),Transform(probe,env(site,GOLD,q/.9)),Transform(bar,Line(ax.c2p(.5,0),ax.c2p(.5,q),color=GOLD,stroke_width=22)),run_time=.4)
        self.at('can lower the response');state(-.3)
        self.at('changing its frequency');state(-3.8);self.wait(.3);state(-2.5)
        self.at('where it acts');state(.2)
        self.at('helps map the gain');self.play(FadeIn(txt('helps map where the gain is gathered',0,-3.6,TEAL)),run_time=.3);self.finish()
class S19Take(SpokenScene):
    def construct(self):
        sp=spectrum('ear');self.add(sp,head('Two tones in → new tones made',TEAL))
        self.remove(sp[1][3],sp[2][3],sp[2][-1])
        legend=VGroup(Line([-4.8,2.6,0],[-4.3,2.6,0],color=YELLOW,stroke_width=7),txt('tones in',-3.35,2.6,YELLOW),Line([-.9,2.6,0],[-.4,2.6,0],color=TEAL,stroke_width=7),txt('made by the ear',1.35,2.6,TEAL))
        co=VGroup(Line([-4.8,.9,0],[-2.2,.9,0],color=GREY),Line([-4.8,1.9,0],[-2.2,1.9,0],color=GREY),Line([-2.2,.9,0],[-2.2,1.9,0],color=GREY))
        mic=RoundedRectangle(width=.38,height=.7,corner_radius=.1,color=TEAL,fill_opacity=.4).move_to([-4.25,1.4,0])
        mic_label=txt('ear-canal mic',-3.7,2.15,TEAL,22)
        link=Arrow(mic.get_bottom(),sp[1][0].get_top(),color=TEAL,buff=.1,stroke_width=4)
        self.add(legend,co,mic,mic_label)
        self.at("a living cochlea's");self.play(Indicate(sp[1][1]),Indicate(sp[1][2]),run_time=.4)
        self.at('makes new tones');self.play(Indicate(sp[1][0]),run_time=.4)
        self.at('a microphone');self.play(Indicate(mic),GrowArrow(link),run_time=.4)
        self.at('can hear them');self.play(FadeIn(txt('2f1 − f2 = 1,600 Hz',0,-3.65,TEAL)),run_time=.3);self.finish()
class S20End(EndCard):
    LINE="A living cochlea's nonlinearity makes new tones."
    def construct(self):
        self.add(VGroup(T(self.LINE,37,font=TITLE_FONT),T('A microphone in the ear canal can hear them.',32,font=TITLE_FONT),T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.55));self.finish()
