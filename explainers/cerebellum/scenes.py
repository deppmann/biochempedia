"""Chapter 1: A Predictor That Learns from Error.
COLOR MAP: BLUE=context, mossy/granule/parallel fibres; ORANGE=climbing
fibre/error; GREEN=Purkinje/inhibition; GOLD=nuclear output; RED=weakened
synapse; YELLOW=movement/target; GREY=anatomy/time. All reach curves use
the reference smoothstep/sinusoidal model; spike trains are schematic.
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
CTX,ERR,PUR,NUC,WEAK,MOVE=BLUE,ORANGE,GREEN,GOLD,RED,YELLOW

def P(x,y): return np.array([x,y,0.])
def poly(pts,c,w=4):
    v=VMobject(stroke_color=c,stroke_width=w)
    v.set_points_as_corners([P(*p) for p in pts]);return v

def label(s,x,y,c=TEXT,size=30): return T(s,size=size,color=c).move_to(P(x,y))
def heading(s,c=TEXT): return label(s,0,3.25,c,34)
def arrow(a,b,c=GREY,w=4): return Arrow(P(*a),P(*b),buff=0,color=c,stroke_width=w,tip_length=.18)
def smooth(q): return 3*q*q-2*q*q*q

def reach(q,cx,bad=False):
    start,target=P(cx-1.25,-1.3),P(cx+.12,.9)
    d=target-start;u=d/np.linalg.norm(d);n=P(-u[1],u[0])
    if bad:
        if q<.55:
            t=q/.55;along,lat=1.25*smooth(t),.45*np.sin(np.pi*t)
        else:
            t=(q-.55)/.45;along,lat=1.25-.25*t,.55*np.sin(6*np.pi*t)*(.15+.85*t)
    else: along,lat=smooth(min(1,q*1.8)),0
    return start+d*along+n*lat

def cup(cx):
    return VGroup(poly([(cx+.3,1.35),(cx+.4,.5),(cx+1,.5),(cx+1.1,1.35)],MOVE),Line(P(cx+.3,1.35),P(cx+1.1,1.35),color=MOVE),Arc(radius=.27,start_angle=-PI/2,angle=PI,color=MOVE).move_to(P(cx+1.2,.9)))
def arm(cx,q,bad=False):
    h=reach(q,cx,bad);shoulder=P(cx-.7,-3.05);elbow=P(cx-1.1,-2.3)
    return VGroup(poly([shoulder[:2],elbow[:2],h[:2]],MOVE,16),Dot(h,radius=.18,color=MOVE))
def reaches(q=.35):
    return VGroup(label('healthy',-3.2,2.95,MOVE),label('cerebellar damage',3.2,2.95,MOVE),cup(-3.2),cup(3.2),arm(-3.2,q),arm(3.2,q,True),DashedLine(P(0,-3.2),P(0,1.5),color=GREY,stroke_opacity=.35))
def questions():
    return VGroup(label('Weak, or clumsy?',0,2.25,size=32),label('Where does it go most wrong?',0,1.7,size=28))

def fan(x,y=0,scale=1):
    paths=[[(0,0),(0,.7)],[(0,.7),(-1,2.25)],[(0,.7),(-.4,2.4)],[(0,.7),(.4,2.4)],[(0,.7),(1,2.25)]]
    return VGroup(*[poly([(x+a*scale,y+b*scale) for a,b in pts],PUR,4) for pts in paths],Circle(radius=.24*scale,color=PUR,fill_color=PUR,fill_opacity=.45).move_to(P(x,y)))

def slots(context=False,error=False):
    g=VGroup()
    for x,s,c,filled in [(-4.65,'Context',CTX,context),(-1.45,'Error',ERR,error)]:
        box=RoundedRectangle(width=2.7,height=.65,corner_radius=.12,color=c,fill_color=c,fill_opacity=.28 if filled else .02).move_to(P(x,3.05))
        g.add(box,label(s+(' ✓' if filled else ''),x,3.05,c,28))
    return g

def sources():
    return VGroup(chip('pons',CTX,28).move_to(P(-4.8,-2.7)),chip('spinal / vestibular',CTX,28).move_to(P(2.6,-2.7)))
def mossy():
    # Both source populations converge on all four granule-cell positions.
    g=VGroup()
    for start in (-4.8,2.6):
        for end in (-4.6,-2.7,1.1,5.2):
            g.add(poly([(start,-2.32),(start,-1.8),(end,-1.05)],CTX,3))
    return g

def circuit():
    cells=VGroup(fan(-.9,-.45,.9),fan(3.45,-.45,.9))
    gran=VGroup(*[Dot(P(x,-1.05),radius=.16,color=CTX) for x in (-4.6,-2.7,1.1,5.2)])
    pf=VGroup(*[Line(P(-5.8,y),P(5.8,y),color=CTX,stroke_width=2.5) for y in np.linspace(.65,1.65,6)],*[poly([(x,-.9),(x,.65)],CTX,3) for x in (-4.6,-2.7,1.1,5.2)])
    return cells,pf,gran

def nucleus(x,y): return Circle(radius=.4,color=GREY,fill_color=GREY,fill_opacity=.3).move_to(P(x,y))
def pedal(x,y,eased=False):
    # A pivot, lever and broad tread, offset from the cell body.
    end=P(x+.6,y+(.32 if eased else -.12))
    tread=RoundedRectangle(width=.48,height=.18,corner_radius=.04,color=PUR,fill_color=PUR,fill_opacity=.7).move_to(end).rotate(.45 if eased else -.2)
    return VGroup(Dot(P(x,y),radius=.08,color=PUR),Line(P(x,y),end,color=PUR,stroke_width=7),tread)

def inhibition(x,soma_y,nucleus_y,eased=False):
    terminal_y=nucleus_y+.6
    return VGroup(Line(P(x,soma_y-.25),P(x,terminal_y),color=PUR,stroke_width=4 if eased else 8),
                  Line(P(x-.3,terminal_y),P(x+.3,terminal_y),color=PUR,stroke_width=6),
                  label('−',x+.48,terminal_y,PUR,32),
                  Circle(radius=.52,color=GREY,fill_color=GREY,fill_opacity=.3).move_to(P(x,nucleus_y)),
                  pedal(x,(soma_y+terminal_y)/2,eased))
def train(x0,x1,y,dense=False,burst=False):
    xs=np.arange(x0,x1,.28 if dense else .65)
    if burst: xs=np.unique(np.r_[np.arange(x0,x1,.65),np.arange((x0+x1)/2-.5,(x0+x1)/2+.6,.16)])
    return VGroup(Line(P(x0,y),P(x1,y),color=NUC,stroke_width=2),*[Line(P(x,y),P(x,y+.5),color=NUC,stroke_width=3) for x in xs])

def brake_stage(eased=False):
    pur=fan(-2.65,-.5,1.45)
    parts=inhibition(-2.65,-.5,-2.55,eased)
    terminal=VGroup(parts[1],parts[2])
    axon=Line(P(-2.13,-2.55),P(.1,-2.55),color=NUC,stroke_width=4)
    return VGroup(pur,parts[0],terminal,parts[3],axon,parts[4],label('Purkinje cell',2.2,2.2,PUR,34),label('inhibits (−)',.1,-.55,PUR,30),label('deep / vestibular\nnucleus cell',-5,-2.45,GREY,28),label('brake eased' if eased else 'brake on',-.1,-1.4,PUR,30),label('deep nucleus output',2.7,-1.85,NUC,30),train(.1,5.8,-2.55,eased))

RULES=[('The cerebellum learns\nto predict, and it learns\nfrom error.',TEXT),('Timed error can weaken\neligible parallel-fibre synapses.',ERR),('Weaker input to the brake:\nmore output at that point,\nnext time.',NUC),('Unpaired activity can\nstrengthen the same synapses.',CTX)]
def rule_row(i):
    s,c=RULES[i];t=T(s,size=30 if i else 32,color=c,line_spacing=.7)
    return t.move_to(P(-3.25,[1.95,.35,-1.15,-2.65][i])).align_to(P(-6.1,0),LEFT)
def rules(n):
    bottom=[.95,-.35,-2.05,-3.35][max(0,n-1)];top=2.9
    box=RoundedRectangle(width=6.4,height=top-bottom,corner_radius=.12,color=GREY,stroke_width=2).move_to(P(-3.2,(top+bottom)/2))
    return VGroup(box,*[rule_row(i) for i in range(n)])
def synapse_stage(weak=False):
    pf=Line(P(.5,1.85),P(6,1.85),color=CTX,stroke_width=6)
    cell=fan(3.3,-.7,1.05)
    dots=VGroup(*[Dot(P(x,1.85),radius=.16,color=WEAK if weak and i>0 else CTX).set_opacity(.4 if weak and i>0 else 1) for i,x in enumerate((2.25,3.3,4.35))])
    return VGroup(pf,cell,dots,label('parallel fibre',3.3,2.55,CTX,28),label('Purkinje cell',5,-.7,PUR,28))

def rule_title(): return heading('The learning rule',PUR)

class S00Title(TitleCard):
    LESSON='The Cerebellum'
    TITLE='A Predictor That Learns from Error'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.2,TEAL,28),label(self.LESSON,0,1.4,GREY,30))
        title=label('A Predictor That\nLearns from Error',0,-.1,size=53)
        self.play(FadeIn(title),Create(Line(P(-4.8,-1.6),P(4.8,-1.6),color=GOLD,stroke_width=4)),run_time=.6)
        self.wait(2.2);self.play(FadeOut(Group(*self.mobjects)),run_time=.2);self.finish()

class S01(SpokenScene):
    def construct(self):
        # Lateral profile: frontal pole left, occipital pole above cerebellum right.
        outline=[(-6.1,.1),(-6.25,1),(-5.8,2),(-4.7,2.65),(-3,2.85),(-1.1,2.55),(.65,1.8),(1.3,.8),(1.1,.05),(.35,-.25),(-.8,-.3),(-1.9,-.8),(-3.5,-.65),(-4.4,-.3),(-5.4,-.5),(-6.1,.1)]
        hemi=poly(outline,GREY,5).make_smooth().set_fill(GREY,opacity=.12)
        gyri=VGroup(*[poly(p,GREY,2).make_smooth() for p in [[(-5.5,.1),(-5.6,1),(-4.8,1.8),(-4.5,.8),(-3.8,1.8)],[(-4.1,2.5),(-3.4,1.7),(-3.9,.8),(-3.1,-.1)],[(-2.7,2.55),(-1.9,1.8),(-2.5,.9),(-1.6,.2)],[(-1,2.1),(-.25,1.3),(-.7,.3)]]])
        cb=poly([(-1.35,-.6),(-.65,-.35),(.35,-.45),(1,-.95),(.95,-1.65),(.3,-2.05),(-.65,-1.95),(-1.25,-1.4),(-1.35,-.6)],PUR,5).make_smooth().set_fill(PUR,opacity=.18)
        glow=VGroup(*[cb.copy().set_fill(opacity=0).set_stroke(PUR,width=w,opacity=o) for w,o in [(28,.05),(18,.1),(10,.18)]])
        folia=VGroup(*[poly([(-1,y),(-.3,y-.12),(.55,y-.05)],PUR,2).make_smooth() for y in (-.75,-1.05,-1.35,-1.65)])
        stem=poly([(-2,-.65),(-1.9,-1.3),(-1.5,-2.65),(-.95,-2.85),(-1.15,-1.5),(-1,-1)],GREY,4).make_smooth().set_fill(GREY,opacity=.25)
        VGroup(hemi,gyri,stem,glow,cb,folia).scale(1.1,about_point=P(-6,0))
        self.at('damage the cerebellum');self.add(hemi,gyri,stem,glow,cb,folia,label('Damage the cerebellum',0,3.5,PUR,32),label('front',-5.25,-1.25,GREY,32),label('back',.65,-2.65,GREY,32),label('cerebellum',3.7,-1.3,PUR,32),Line(P(1.9,-1.3),P(2.3,-1.3),color=PUR))
        self.play(glow.animate.set_stroke(opacity=.2),Indicate(cb,color=PUR,scale_factor=1.08),run_time=.8)
        self.at('can still move');self.play(FadeIn(label('Still able to move',3.7,1.1,MOVE,30)),run_time=.35)
        self.at('so what is lost');self.play(FadeIn(label('What is lost?',3.7,0,size=38)),run_time=.35);self.finish()

class S02(SpokenScene):
    def construct(self):
        g=reaches(0);self.at('watch someone');self.add(g)
        self.at('reach for');self.play(Transform(g[4],arm(-3.2,.35)),Transform(g[5],arm(3.2,.35,True)),run_time=.8);self.finish()
class S03(SpokenScene):
    def construct(self):
        self.add(reaches());q=questions()
        self.at('is the movement');self.play(FadeIn(q[0]),run_time=.3)
        self.at('where does it');self.play(FadeIn(q[1]),run_time=.3);self.finish()
class S04Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(reaches(),questions());self.wait(5)
class S05(SpokenScene):
    def construct(self):
        g=reaches();self.add(g)
        self.at('clumsy');self.add(label('Clumsy, not weak',0,2.15,MOVE,34))
        self.at('the reach overshoots');tr=ValueTracker(.35)
        a=always_redraw(lambda:arm(-3.2,tr.get_value()))
        b=always_redraw(lambda:arm(3.2,tr.get_value(),True))
        self.remove(g[4],g[5]);self.add(a,b);self.play(tr.animate.set_value(.55),run_time=.8,rate_func=linear)
        self.at('the hand shakes')
        # Magnified lateral component of exactly the same sinusoidal reach model.
        pts=[(4+.75*np.sin(6*np.pi*t)*(.15+.85*t),.9-2.5*t) for t in np.linspace(0,1,160)]
        path=poly(pts,WEAK,5)
        self.add(label('overshoot,\nshaking near\nthe target',5.7,-1.1,WEAK,26),DashedLine(P(3.95,.9),P(4,.9),color=WEAK))
        self.play(Create(path),tr.animate.set_value(1),run_time=1.5,rate_func=linear);self.finish()
class S06(SpokenScene):
    def construct(self):
        axis=arrow((-5.7,-.6),(5.7,-.6));self.at('feedback is slow');self.add(heading('Feedback is slow',ERR),axis,label('time',5.4,-1.2,GREY,28),label('0',-5.2,-1.2,GREY,28))
        events=[VGroup(chip('command',MOVE,30).move_to(P(-5,1.8)),Line(P(-5,1.45),P(-5,-.6),color=MOVE)),VGroup(chip('arm moves',MOVE,30).move_to(P(-1.8,.6)),Line(P(-1.8,.25),P(-1.8,-.6),color=MOVE))]
        self.play(FadeIn(events[0]),run_time=.3);self.play(FadeIn(events[1]),run_time=.3)
        wrong=VGroup(label('arm goes wrong',-1.8,2.35,WEAK,28),arrow((-1.8,2),(-1.8,1.1),WEAK))
        self.play(FadeIn(wrong),run_time=.3)
        self.at('a visual error');dot=Dot(P(-1.8,-.6),color=ERR,radius=.15);self.add(dot)
        self.play(dot.animate.move_to(P(4.3,-.6)),run_time=.8)
        self.at('arrives a tenth');report=VGroup(chip('report arrives',ERR,30).move_to(P(4.3,1.65)),Line(P(4.3,1.3),P(4.3,-.6),color=ERR))
        bracket=VGroup(Line(P(-1.8,-2),P(4.3,-2),color=ERR),Line(P(-1.8,-1.8),P(-1.8,-2.2),color=ERR),Line(P(4.3,-1.8),P(4.3,-2.2),color=ERR),label('0.1 s or more',1.25,-2.65,ERR,36))
        self.play(FadeIn(report),Create(bracket),run_time=.4);self.finish()
class S07(SpokenScene):
    def construct(self):
        self.at('in one model');self.add(heading('Late feedback + strong corrections',MOVE),label('One model; one proposed contributor',0,-3.25,GREY,28))
        # Magnify the reference reach's final oscillation and spread it along time.
        def point(t):
            q=.55+.45*t;p=reach(q,0,True);target=reach(1,0)
            d=target-reach(0,0);u=d/np.linalg.norm(d);n=P(-u[1],u[0])
            return P(-5.3+10.6*t,4.8*np.dot(p-target,n))
        pts=[point(t) for t in np.linspace(0,1,300)]
        self.add(DashedLine(P(-5.6,0),P(5.8,0),color=MOVE),label('target',-5.55,1.75,MOVE,28),Line(P(-5.55,1.4),P(-5.55,0),color=MOVE,stroke_width=2),label('time →',4.8,-2.6,GREY,28))
        t=ValueTracker(0);hand=always_redraw(lambda:Dot(point(t.get_value()),radius=.17,color=MOVE))
        lag=always_redraw(lambda:Circle(radius=.2,color=ERR,stroke_width=4).move_to(point(max(0,t.get_value()-.13))))
        correction=always_redraw(lambda:arrow(tuple(point(max(0,t.get_value()-.13))[:2]),(point(max(0,t.get_value()-.13))[0],0),ERR) if abs(point(max(0,t.get_value()-.13))[1])>.15 else VGroup())
        hand_label=always_redraw(lambda:label('hand',point(t.get_value())[0],point(t.get_value())[1]+.5,MOVE,26))
        ghost_label=always_redraw(lambda:label('late report',point(max(0,t.get_value()-.13))[0],point(max(0,t.get_value()-.13))[1]-.5,ERR,26))
        trail=always_redraw(lambda:poly([point(q)[:2] for q in np.linspace(max(0,t.get_value()-.13),t.get_value(),25)],ERR,7).set_opacity(.45))
        self.at('a hand steered');self.add(trail,hand,lag,correction,hand_label,ghost_label)
        path=poly([p[:2] for p in pts],MOVE,4)
        self.play(Create(path),t.animate.set_value(1),run_time=4.3,rate_func=linear)
        self.add(*[arrow(tuple(point(q)[:2]),(point(q)[0],0),ERR,w=6) for q in (.42,.59,.75)])
        self.finish()
class S08(SpokenScene):
    def construct(self):
        self.at('so the cerebellum');self.add(heading('Prediction',PUR))
        frame=RoundedRectangle(width=11.8,height=3.9,corner_radius=.2,color=PUR).move_to(P(0,0))
        a=chip('command',MOVE,34).move_to(P(-3.4,1));b=chip('estimated result',PUR,34).move_to(P(2.6,1))
        self.play(Create(frame),FadeIn(a),run_time=.4)
        self.at('it estimates');self.play(GrowArrow(arrow((-1.8,1),(.6,1),PUR)),FadeIn(b),run_time=.4)
        self.at('before the senses');self.play(FadeIn(label('An estimate made before\nthe senses report the result.',0,-1.3,size=36)),run_time=.4);self.finish()
class S09(SpokenScene):
    def construct(self):
        self.at('to learn a prediction');self.add(heading('Learning a prediction',PUR))
        boxes=VGroup(*[RoundedRectangle(width=5,height=3.1,corner_radius=.16,color=c).move_to(P(x,-.3)) for x,c in [(-3.1,CTX),(3.1,ERR)]])
        self.at('you need two things');self.play(Create(boxes),run_time=.4);self.add(label('Context',-3.1,.6,CTX,34),label('Error',3.1,.6,ERR,34))
        self.at('a description');self.play(FadeIn(label('What is happening?',-3.1,-.6,CTX,30)),run_time=.3)
        self.at('a signal');self.play(FadeIn(label('What is wrong?',3.1,-.6,ERR,30)),run_time=.3);self.finish()
class S10(SpokenScene):
    def construct(self):
        self.at('mossy');self.add(slots(),sources(),label('mossy fibres',0,2.25,CTX,36))
        paths=VGroup(*[poly([(start,-2.3),(start,.4),(end,1)],CTX,4) for start,ends in [(-4.8,(-5.15,-4.45)),(2.6,(2.25,2.95))] for end in ends])
        self.play(Create(paths),run_time=.55)
        self.add(DashedLine(P(-5.8,1),P(5.8,1),color=GREY),label('granule-cell layer',0,1.5,GREY,28))
        self.at('including a copy');self.play(FadeIn(label('copy of command\nfrom cortex',-2.65,-.2,CTX,28)),FadeIn(label('what the\nbody senses',4.65,-.2,CTX,28)),run_time=.4);self.finish()
class S11(SpokenScene):
    def construct(self):
        cells,pf,gran=circuit();header=slots();self.add(header,sources(),mossy())
        self.at('granule cells');self.play(FadeIn(gran),FadeIn(label('granule cells',-4.1,-.55,CTX,28)),run_time=.3)
        self.at('relay it as');self.play(Create(pf),run_time=.5)
        self.at('which run');self.play(FadeIn(cells),FadeIn(label('Purkinje cells',3.4,2.35,PUR,30)),FadeIn(label('parallel fibres',-3.9,2.15,CTX,28)),run_time=.35)
        self.remove(header);self.add(slots(True));pulses=VGroup(*[Dot(P(-5.6,y),radius=.08,color=CTX) for y in np.linspace(.65,1.65,6)])
        self.add(pulses);self.play(pulses.animate.shift(RIGHT*11),run_time=1,rate_func=linear);self.remove(pulses);self.finish()
class S12(SpokenScene):
    def construct(self):
        cells,pf,gran=circuit();header=slots(True);self.add(header,cells,pf,gran,label('parallel fibres',-3.9,2.15,CTX,28),label('Purkinje cells',3.4,2.35,PUR,30))
        self.at('in the classical model');self.add(label('classical model',4.3,3.05,GREY,28))
        olive=chip('inferior olive',ERR,28).move_to(P(-3.7,-2.5))
        def cf(x):return poly([(-3.7,-2.13),(-3.7,-1.75),(x-1.15,-1.75),(x-1.15,.05),(x-.5,.65),(x-.25,1),(x-.45,1.4),(x-.3,1.7)],ERR,5)
        self.at('one climbing');self.play(FadeIn(olive),Create(cf(-.9)),run_time=.65)
        self.at('carries the error');self.remove(header);self.add(slots(True,True),label('climbing fibre: teaching signal',2,-2.5,ERR,28))
        self.at('each adult');self.play(Create(cf(3.45)),FadeIn(label('One climbing fibre per adult Purkinje cell',0,-3.25,ERR,28)),run_time=.5);self.finish()
class S13(SpokenScene):
    def construct(self):
        g=brake_stage();self.add(g,label('Only output of the cerebellar cortex',0,3.4,PUR,30))
        self.at('are the only output');self.play(Indicate(g[0],color=PUR,scale_factor=1.02),run_time=.4)
        self.at('they inhibit');self.play(Indicate(g[2],color=PUR,scale_factor=1.15),run_time=.4)
        self.at('they press');self.play(Indicate(g[5],color=PUR,scale_factor=1.15),run_time=.4);self.finish()

class S14(SpokenScene):
    def construct(self):
        g=brake_stage();self.add(g,heading('A brake on a firing cell',PUR))
        self.at('many nuclear cells');self.play(ShowPassingFlash(g[11].copy().set_color(TEXT)),run_time=.6)
        self.at('ease off');self.play(Transform(g,brake_stage(True)),run_time=.6)
        self.add(label('other inputs unchanged',2.7,-3.05,GREY,28));self.finish()
class S15(SpokenScene):
    def construct(self):
        self.at('here is the rule');self.add(rule_title(),synapse_stage(),inhibition(3.3,-.7,-2.55),label('nucleus',5,-2.55,GREY,28))
        self.at('the cerebellum learns');self.play(FadeIn(rules(1)),run_time=.35)
        self.at('it learns from error');self.play(Indicate(rule_row(0),color=ERR,scale_factor=1),run_time=.4);self.finish()
class S16(SpokenScene):
    def construct(self):
        s=synapse_stage();s[4].set_opacity(0);r=rules(1);self.add(r,s,rule_title(),label('Purkinje cell',1.7,-.65,PUR,28))
        axis=arrow((.8,-1.5),(5.9,-1.5));self.add(axis,label('time (ms)',5.05,-2,GREY,26),label('timing varies by region',3.2,-3.15,GREY,28))
        self.at('in this model')
        marks=VGroup(*[Line(P(x,-1.7),P(x,-1.25),color=CTX,stroke_width=5) for x in (1.2,2.6,3.2)])
        window=Rectangle(width=1.4,height=.65,color=ERR,fill_color=ERR,fill_opacity=.12).move_to(P(2.9,-1.45))
        self.add(window,label('−120 ms (mouse flocculus)',2.7,-2.6,ERR,26))
        for i in range(3):
            self.play(Flash(s[2][i],color=CTX,flash_radius=.32),s[2][i].animate.scale(1.5).set_color(TEXT),Create(marks[i]),run_time=.25)
            self.play(s[2][i].animate.scale(1/1.5).set_color(CTX),run_time=.15)
        self.at('error signal');self.play(GrowArrow(arrow((5.9,.15),(3.55,-.5),ERR)),FadeIn(label('climbing fibre\n(error)',5.1,-.9,ERR,26)),Create(Line(P(5,-1.7),P(5,-1.25),color=ERR,stroke_width=6)),run_time=.4)
        self.at('can weaken');self.remove(r);r=rules(2);self.add(r)
        weakened=synapse_stage(True);weakened[4].set_opacity(0)
        self.play(Transform(s,weakened),run_time=.4)
        self.at('active at the right moment');self.play(Indicate(window,color=ERR,scale_factor=1),run_time=.4);self.finish()
class S17(SpokenScene):
    def construct(self):
        s=synapse_stage(True);s[3].set_opacity(0);s[4].set_opacity(0);r=rules(2);self.add(r,s,rule_title())
        parts=inhibition(3.3,-.7,-2.35)
        ax=Line(P(3.82,-2.35),P(4.05,-2.35),color=NUC,stroke_width=4);out=train(4.05,6,-2.35)
        self.add(label('Purkinje cell',1.55,-.65,PUR,26),parts,ax,out,label('nucleus',1.8,-2.35,GREY,26),label('before',5.1,-.85,NUC,26),train(4.05,6,-1.65))
        self.at('with other inputs unchanged');self.add(label('other inputs unchanged',3.35,-3.4,GREY,27))
        self.at('weaker input');self.remove(r);r=rules(3);self.add(r)
        self.add(label('next time: same context',3.3,2.65,CTX,28))
        self.at('more output');self.play(Transform(out,train(4.05,6,-2.35,burst=True)),Transform(parts,inhibition(3.3,-.7,-2.35,True)),run_time=.45)
        self.add(label('brake eased',1.55,-1.35,PUR,26),Line(P(4.45,-2.7),P(5.55,-2.7),color=NUC),label('this moment',5,-3,NUC,26));self.finish()

class S18(SpokenScene):
    def construct(self):
        s=synapse_stage(True);r=rules(3);self.add(s,r,rule_title())
        self.at('parallel');self.play(Indicate(s[0],color=CTX,scale_factor=1),run_time=.4)
        self.at('without a paired');unpaired=label('No paired climbing fibre',3.3,-1.5,GREY,28);self.add(unpaired)
        self.at('can strengthen');self.remove(r);r=rules(4);self.add(r);self.remove(s[3]);s[3].set_opacity(0);self.add(label('parallel fibre',2.1,2.55,CTX,28))
        up=VGroup(arrow((4.35,2),(4.35,2.45),CTX),label('strengthen',5.35,2.65,CTX,26))
        self.play(*[d.animate.set_color(CTX).set_opacity(1).scale(1.3) for d in s[2][1:]],FadeIn(up),run_time=.5)
        self.at('corrections can run');self.remove(unpaired,up)
        paired=VGroup(arrow((5.9,.15),(3.55,-.5),ERR),label('Paired climbing fibre',3.3,-1.5,ERR,28),label('weaken',5.35,2.65,WEAK,26),arrow((4.35,2.45),(4.35,2),WEAK))
        weakened=synapse_stage(True);weakened[3].set_opacity(0)
        self.play(Transform(s,weakened),FadeIn(paired),FadeIn(label('Corrections can run both ways.',3.2,-2.5,size=29)),run_time=.4);self.finish()

class S19(SpokenScene):
    def construct(self):
        self.add(rules(4),synapse_stage(),rule_title())
        # The complete caveat holds throughout this beat, with equal weight.
        self.at('this is the classical');self.add(label('Marr–Albus–Ito\nclassical model',3.3,-1.6,size=30),label('Supported for some tasks',3.3,-2.3,size=29),label('Not the whole story',3.3,-3.05,size=29));self.finish()
class S20(SpokenScene):
    def construct(self):
        self.at('the takeaway');self.add(heading('The cerebellum',PUR))
        self.play(FadeIn(label('A predictor',0,1.05,PUR,64)),FadeIn(label('that learns from error.',0,-.25,ERR,56)),run_time=.55)
        self.add(label('Next: following the sign',0,-2.4,GREY,30));self.finish()
class S21End(EndCard):
    LINE='The cerebellum is a predictor that learns from error.'
