"""One Hair, Three Classes — review redraw.
COLOR MAP: BLUE Aβ RA; YELLOW Aδ; ORANGE C; TAN SA1/Merkel;
GREEN field-LTMR; SAGE Schwann processes; GREY hair/skin;
TEXT generic genetic access; GOLD questions/takeaway.
Models: t_ms=1000*L/v; illustrative adaptation r(t)=r0*exp(-t/tau),
spikes at integer crossings of integrated rate; waveform is a sum of
analytic spike kernels. No experimental spike counts are implied.
"""
import numpy as np
from bp_style import *

ORANGE='#F29E4C'
TAN='#D5B68C'
SAGE='#93B2A0'
CLS={'RA':BLUE,'AD':YELLOW,'C':ORANGE,'SA1':TAN}
CNAME={'RA':'Aβ RA','AD':'Aδ','C':'C','SA1':'SA1'}
VELOCITIES=np.array([13.6,5.8,.58])
ARRIVALS=1000*.02/VELOCITIES

# Word timing without creating an extra, unrequested sync.log artifact.
class Timed(SpokenScene):
    def at(self,phrase,lead=.2,nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)

def heading(s): return T(s,34,font=TITLE_FONT).move_to([0,3.15,0])
def label(s,x,y,size=28,col=TEXT): return T(s,size,col).move_to([x,y,0])
def events(key):
    tau=.10 if key!='C' else .8
    r0=35 if key!='C' else 12
    t=np.linspace(0,3,3001)
    integral=r0*tau*(1-np.exp(-t/tau))
    return np.interp(np.arange(1,int(integral[-1])+1),integral,t)

def follicle(kind='awl',x=-3,y=-.3,s=1.3,bent=False,endings=True,dome=False):
    sheath=RoundedRectangle(width=1.55*s,height=2.6*s,corner_radius=.3*s,stroke_color=GREY,fill_color=GREY,fill_opacity=.10).move_to([x,y,0])
    surface=y+1.3*s
    top=surface+{'guard':1.35,'awl':.9,'zig':.65}[kind]*s
    # Shaft deliberately offset from the central ending, with root above bar tips.
    pts=[[x+.48*s,y-.75*s,0],[x+.48*s,surface,0]]
    if bent: pts += [[x+1.05*s,top-.25,0]]
    elif kind=='zig': pts += [[x+.7*s,surface+.22*s,0],[x+.3*s,surface+.4*s,0],[x+.48*s,top,0]]
    else: pts += [[x+.48*s,top,0]]
    shaft=VMobject(stroke_color=GREY,stroke_width=6).set_points_as_corners(pts)
    skin=Line([x-1.25*s,surface,0],[x+1.35*s,surface,0],color=GREY,stroke_width=3)
    pat={'guard':['RA'],'awl':['RA','AD','C'],'zig':['AD','C']}[kind]
    pk=VGroup(*[RoundedRectangle(width=.15*s,height=1.95*s,corner_radius=.05,stroke_width=0,fill_color=CLS[k],fill_opacity=1).move_to([x+(-.48+i*.31)*s,y,0]) for i,k in enumerate(pat)])
    g=VGroup(sheath,skin,shaft)
    if endings:g.add(pk)
    g.pk=pk;g.shaft=shaft;g.sheath=sheath;g.kind=kind
    g.dome=VGroup(Sector(radius=.43*s,angle=PI,color=TAN,fill_opacity=.4).move_to([x+1.05*s,surface+.23*s,0]),Line([x+1.05*s,surface,0],[x+1.05*s,surface-.8*s,0],color=TAN,stroke_width=5))
    if dome:g.add(g.dome)
    return g

def probe(f):
    p=f.shaft.get_end()
    return VGroup(Line(p+UP*.35+RIGHT*1.05,p,color=TEXT,stroke_width=7),Circle(radius=.10,color=TEXT,fill_opacity=1).move_to(p))

def prediction():
    f=follicle(bent=True,endings=False)
    return VGroup(f,probe(f),label('awl/auchene',-3,-2.55),T('Which classes\nanswer?',40,font=TITLE_FONT,line_spacing=1.2).move_to([2.8,.5,0]))

def legend(y=-3.1):
    return VGroup(*[label(CNAME[k],x,y,28,CLS[k]) for x,k in zip((-4.8,-1.7,1.2,4.4),('RA','AD','C','SA1'))])

def soma(col=TEXT):
    return VGroup(Circle(radius=1.15,color=col,fill_opacity=.22).move_to([-3.8,.1,0]),Line([-2.65,.1,0],[-1.3,.1,0],color=col,stroke_width=6))

def electrode():
    path=VMobject(stroke_color=TEXT,stroke_width=4).set_points_as_corners([[-3.4,.45,0],[-2.5,1.85,0],[-.7,1.85,0]])
    box=chip('recorder',TEXT,26).move_to([.3,1.85,0])
    return VGroup(path,box)

def response(key,x=.2,width=5.6,y=-1.3):
    col=CLS[key]; start=.3; end=2.8
    xx=lambda t:x+t/3*width
    stimulus=VMobject(stroke_color=TEXT,stroke_width=3).set_points_as_corners([[xx(0),y+1,0],[xx(start),y+1,0],[xx(start),y+1.5,0],[xx(end),y+1.5,0],[xx(end),y+1,0],[xx(3),y+1,0]])
    shade=Rectangle(width=xx(end)-xx(start),height=2.2,stroke_width=0,fill_color=GREY,fill_opacity=.08).move_to([(xx(start)+xx(end))/2,y+.5,0])
    ts=events(key);ts=ts[ts<end-start]+start
    spikes=VGroup(*[Line([xx(t),y-.28,0],[xx(t),y+.28,0],color=col,stroke_width=4) for t in ts])
    axis=VGroup(Line([xx(0),y,0],[xx(3),y,0],color=GREY),*[label(str(t),xx(t),y-.65,26,GREY) for t in (0,1,2,3)],label('s',xx(3)+.35,y-.65,26,GREY))
    return VGroup(shade,stimulus,axis,spikes,label('bend → hold',x+width/2,y+1.95,26),label('Illustrative adaptation model',x+width/2,y-1.3,26,GREY))

def mount():
    # Exactly 1 guard, 23 awl/auchene and 76 zigzag, top view.
    out=VGroup()
    for i in range(100):
        x=-5.7+(i%20)*.6;y=2.1-(i//20)*.97
        kind='guard' if i==0 else 'awl' if i<24 else 'zig'
        pat={'guard':['RA'],'awl':['RA','AD','C'],'zig':['AD','C']}[kind]
        ring=Circle(radius=.19,color=GREY,stroke_width=2).move_to([x,y,0])
        ends=VGroup(*[Dot([x+.25*np.cos(j*TAU/len(pat)),y+.25*np.sin(j*TAU/len(pat)),0],radius=.065,color=CLS[k]) for j,k in enumerate(pat)])
        g=VGroup(ring,ends);g.ends=ends;g.kind=kind
        if kind=='guard':
            dome=Dot([x+.33,y+.16,0],radius=.07,color=TAN);g.add(dome);g.ends.add(dome)
        out.add(g)
    return out

class S00Title(TitleCard):
    LESSON='The Low-Threshold Mechanoreceptors: One Touch, Several Signals'
    TITLE='One Hair, Three Classes'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.3,26,TEAL),T('The Low-Threshold Mechanoreceptors:\nOne Touch, Several Signals',26,GREY,line_spacing=1.2).move_to([0,1,0]))
        self.play(FadeIn(T(self.TITLE,48,font=TITLE_FONT).move_to([0,-.6,0])),run_time=.6);self.finish()

class S01Question(Timed):
    def construct(self):
        f=follicle(endings=False);self.add(f,heading('One hair, three classes'))
        self.at('Bend one hair');b=follicle(bent=True,endings=False)
        self.play(Transform(f,b),Create(probe(b)),run_time=.7)
        self.at('How many kinds');self.play(FadeIn(T('How many kinds\nof touch neuron?',36,font=TITLE_FONT).move_to([2.9,.7,0])),run_time=.4)
        self.at('It depends');self.play(FadeIn(label('It depends on the hair',2.8,-1.4,28,GOLD)),run_time=.3);self.finish()

class S02Hairs(Timed):
    def construct(self):
        self.add(heading('Mouse trunk skin'))
        fs=VGroup(*[follicle(k,x,-.3,.92,endings=False) for k,x in zip(('guard','awl','zig'),(-4.2,0,4.2))]);self.add(fs)
        hairs=VGroup()
        for i in range(100):
            x=-5.9+i*.119;y=-2.65
            pts=[[x,y,0],[x,y+(.65 if i==0 else .43 if i<24 else .25),0]]
            if i>=24:pts.insert(1,[x+.04,y+.13,0])
            hairs.add(VMobject(stroke_color=TEXT if i<24 else GREY,stroke_width=2).set_points_as_corners(pts))
        self.play(Create(hairs),FadeIn(label('guard : awl/auchene : zigzag ≈ 1 : 23 : 76',0,-3.25,28)),run_time=.4)
        for x,name,cue in [(-4.2,'guard','long guard hairs'),(0,'awl/auchene','a la keen'),(4.2,'zigzag','short bent zigzag')]:
            self.at(cue);self.play(FadeIn(label(name,x,-1.85)),run_time=.25)
        self.finish()

class S03Old(Timed):
    def construct(self):
        self.add(follicle(endings=False),heading('Recording first'))
        self.at('defined by recording')
        ts=np.linspace(0,3,1200);ev=events('RA')+.4
        voltage=sum(np.exp(-((ts-t)/.012)**2)-.3*np.exp(-((ts-t-.025)/.025)**2) for t in ev)
        trace=VMobject(stroke_color=TEXT,stroke_width=3).set_points_as_corners([[.1+t/3*5.5,-.5+v*1.1,0] for t,v in zip(ts,voltage)])
        axes=VGroup(Line([.1,-1,0],[5.6,-1,0],color=GREY),label('0',.1,-1.45,26),label('3 s',5.6,-1.45,26),label('Illustrative spike waveform',2.9,1.5,28))
        self.play(Create(trace),FadeIn(axes),run_time=.6)
        self.at('The ending behind');self.play(FadeIn(VGroup(*[label('?',x,-.4,46) for x in (-4.35,-3.9,-2)])),FadeIn(label('ending inferred',2.9,-2.5,30,GREY)),run_time=.4);self.finish()

class S04Genetic(Timed):
    def construct(self):
        self.add(heading('Genetic access'),label('Dorsal root ganglion neurons',0,2.25,28))
        cells=VGroup(*[Circle(radius=.56,color=GREY,fill_opacity=.18).move_to([x,y,0]) for y in (.95,-.5) for x in (-4,-1.35,1.35,4)])
        self.add(cells)
        self.at('A Cree driver');self.play(FadeIn(chip('Cre driver + reporter',TEXT,28).move_to([0,-1.85,0])),run_time=.4)
        self.at('marked cells');self.play(*[cells[i].animate.set_color(TEXT).set_fill(TEXT,opacity=.65) for i in (0,2,5)],FadeIn(T('Driver switches reporter on in cells\nthat expressed the chosen gene',28,line_spacing=1.25).move_to([0,-2.95,0])),run_time=.6);self.finish()

class S05Handle(Timed):
    def construct(self):
        self.add(soma(),heading('A label gives access'))
        self.at('But a label');self.play(Create(Arc(radius=.55,start_angle=0,angle=PI,arc_center=[-3.8,1.2,0],color=TEXT,stroke_width=6)),FadeIn(label('labelled neuron',-3.8,-1.7,28)),run_time=.4)
        self.at('until recording confirms');self.play(FadeIn(electrode()),FadeIn(label('What does it do?',2.8,-.4,34)),run_time=.6);self.finish()

class S06Li(Timed):
    def construct(self):
        self.add(soma(),electrode(),label('labelled neuron',-3.8,-1.7,28),heading('Li and colleagues, 2011'))
        self.at('did that check');self.play(Indicate(soma(),color=TEXT),FadeIn(label('Label + physiological recording',1.9,-1.7,28)),run_time=.5);self.finish()

def identity(scene,key,marker,name,cue,detailcue,extra=''):
    col=CLS[key];scene.add(soma(col),electrode())
    scene.at(cue);scene.play(FadeIn(chip(marker,col,28).move_to([-3.8,-1.65,0])),FadeIn(label(name,3,2.8,36,col)),run_time=.45)
    scene.at(detailcue)
    speed={'RA':'13.6','AD':'5.8','C':'0.58'}[key]
    adapt='intermediate adaptation' if key=='C' else 'rapidly adapting'
    scene.play(FadeIn(label(speed+' m/s',3,1.8,42,col)),FadeIn(label(adapt,-3.8,-2.6,26,col)),FadeIn(response(key,y=-1.2)),run_time=.5)
    if extra:scene.add(label(extra,-3.8,-3.25,26,col))
    scene.finish()
class S07Trkb(Timed):
    def construct(self):identity(self,'AD','TrkB','Aδ-LTMR','Neurons labeled','They answer','threshold < 0.07 mN')
class S08Th(Timed):
    def construct(self):identity(self,'C','TH','C-LTMR','Neurons with','Slow with')
class S09Ret(Timed):
    def construct(self):
        identity(self,'RA','Npy2r-GFP','Aβ RA-LTMR','A third label','fast and rapidly','subset of early Ret neurons')

class S10Map(Timed):
    def construct(self):
        p=mount();self.add(heading('Whole-mount trunk skin • top view'),legend(),label('1 guard • 23 awl/auchene • 76 zigzag',0,-2.45,28))
        self.at('Then they imaged');self.play(LaggedStart(*[FadeIn(g[0]) for g in p],lag_ratio=.015),run_time=1.5)
        self.at('each label surrounded');self.play(LaggedStart(*[FadeIn(g.ends) for g in p],lag_ratio=.01),run_time=1);self.finish()
class S11Predict(Timed):
    def construct(self):
        g=prediction();self.add(follicle(endings=False))
        self.at('Now bend');self.clear();self.add(g[0],g[2]);self.play(Create(g[1]),run_time=.4)
        self.at('Which labeled classes');self.play(FadeIn(g[3]),run_time=.4);self.finish()
class S12Pause(Scene):
    def construct(self):
        self.camera.background_color=BG;self.add(prediction())
        ring=Circle(radius=.57,color=GOLD,stroke_width=4).move_to([2.8,-1.75,0])
        self.add(ring)
        for n in range(5,0,-1):
            num=label(str(n),2.8,-1.75,54,GOLD)
            arc=Arc(radius=.57,start_angle=PI/2,angle=TAU,color=GOLD,stroke_width=7).move_arc_center_to([2.8,-1.75,0])
            self.add(num,arc)
            self.play(Uncreate(arc),run_time=1,rate_func=linear)
            self.remove(num)
class S13Reveal(Timed):
    def construct(self):
        f=follicle(x=0,bent=True,endings=False);self.add(f,probe(f),label('awl/auchene',-4,2.1,28),heading('Three classes at one follicle'))
        for i,(k,cue) in enumerate(zip(('RA','AD','C'),('A beta','a delta','and C'))):
            self.at(cue)
            loc=[(-4,.2),(-.22,-2.8),(4,.2)][i]
            start=[f.pk[i].get_left(),f.pk[i].get_bottom(),f.pk[i].get_right()][i]
            stop=[[-2,.2,0],[-.22,-2.35,0],[2,.2,0]][i]
            self.play(FadeIn(f.pk[i]),Create(Line(start,stop,color=CLS[k],stroke_width=2)),FadeIn(label(CNAME[k],*loc,38,CLS[k])),run_time=.35)
        self.at('Their');self.play(FadeIn(T('lanceolate\nendings',30,line_spacing=1.2).move_to([3.9,-1.65,0])),run_time=.4);self.finish()
class S14Picket(Timed):
    def construct(self):
        self.add(heading('Lanceolate endings • lengthwise'))
        sheath=RoundedRectangle(width=4.2,height=5.4,corner_radius=.5,color=GREY,fill_opacity=.06).move_to([-2.5,-.1,0]);self.add(sheath,Line([-.85,-2.15,0],[-.85,2.8,0],color=GREY,stroke_width=7),Line([-4.9,2.6,0],[-.3,2.6,0],color=GREY,stroke_width=3))
        bars=VGroup(*[RoundedRectangle(width=.42,height=4.5,corner_radius=.12,stroke_width=0,fill_color=CLS[k],fill_opacity=1).move_to([-3.6+i*1.1,-.1,0]) for i,k in enumerate(('RA','AD','C'))])
        self.at('Each ending runs');self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.3),run_time=.9)
        sch=VGroup(*[RoundedRectangle(width=.32,height=4.9,corner_radius=.13,stroke_width=0,fill_color=SAGE,fill_opacity=.9).move_to([x,-.1,0]) for x in (-3.05,-1.95)])
        self.at('like one picket');self.play(FadeIn(sch),FadeIn(T('Schwann cell\nprocesses',30,TEXT).move_to([3,1,0])),Create(VMobject(stroke_color=SAGE,stroke_width=3).set_points_as_corners([[1.2,1.3,0],[.2,2.85,0],[-1.95,2.85,0],[-1.95,2.1,0]])),FadeIn(T('Pickets in a fence',32,font=TITLE_FONT).move_to([3,-1.3,0])),run_time=.5);self.finish()
class S15Field(Timed):
    def construct(self):
        fs=[follicle(k,x,-.3,1.05) for k,x in [('awl',-3.3),('zig',3.3)]];self.add(*fs,label('awl/auchene',-3.3,2.5,30),label('zigzag',3.3,2.5,30))
        self.at('circumferential endings');self.play(*[Create(Ellipse(width=2.5,height=.65,color=GREEN,stroke_width=6).move_to([x,-.6,0])) for x in (-3.3,3.3)],run_time=.5)
        self.at('from field');self.play(FadeIn(T('field-LTMR • circumferential • not labelled by Li\nBai and colleagues, 2015',28,GREEN,line_spacing=1.15).move_to([0,-2.3,0])),run_time=.4)
        self.at('That makes four');self.play(FadeIn(label('3 lanceolate + field = 4',-3.3,-3.2,30)),run_time=.3)
        self.at('and three at');self.play(FadeIn(label('2 lanceolate + field = 3',3.3,-3.2,30)),run_time=.3);self.finish()
class S16Others(Timed):
    def construct(self):
        guard=follicle('guard',-3.4,-.45,1.25,endings=False);zig=follicle('zig',3.2,-.35,1.45,endings=False)
        self.add(guard,zig,heading('Different hairs, different combinations'))
        self.at('Guard hairs carry');self.play(FadeIn(guard.pk),FadeIn(label('guard • Aβ RA',-3.4,-2.3,30,BLUE)),run_time=.4)
        self.at('a touch dome');self.play(FadeIn(guard.dome),FadeIn(T('SA1, found through\nits Merkel cells',28,TAN).move_to([-3.4,-3.05,0])),run_time=.4)
        self.at('Zigzag hairs carry')
        # Explicitly add the two bars at the cue, then hold through the class names.
        self.add(*zig.pk)
        self.play(FadeIn(label('zigzag • Aδ + C',3.2,-2.65,30)),run_time=.35)
        self.finish()
class S17Repeat(Timed):
    def construct(self):
        p=mount();self.add(p,heading('Repeated combinations across the skin'),legend())
        self.at('One movement');self.play(*[Indicate(g,color=TEXT,scale_factor=1.08) for g in p if g.kind=='awl'],run_time=.7)
        self.at('three classes in parallel');self.play(FadeIn(label('Awl/auchene: Aβ RA + Aδ + C',0,-2.45,32)),run_time=.4);self.finish()

def race(scene,start,end,duration):
    clock=ValueTracker(start)
    scene.add(heading('2 cm • equal paths • t = L / v'))
    scene.add(label('Illustrative • conduction only • mean velocities',0,-3.3,26,GREY))
    counter=always_redraw(lambda:label(f'{clock.get_value():04.1f} ms',0,2.25,32))
    scene.add(counter,Line([3.7,1.9,0],[3.7,-1.9,0],color=TEXT))
    for k,y,v,t in zip(('RA','AD','C'),(1.4,0,-1.4),VELOCITIES,ARRIVALS):
        scene.add(label(CNAME[k],-5.4,y+.25,30,CLS[k]),label(f'{v:g} m/s',-5.4,y-.3,26,CLS[k]),Line([-3.7,y,0],[3.7,y,0],color=CLS[k],stroke_width=3))
        d=Dot(radius=.14,color=CLS[k]);d.add_updater(lambda m,y=y,t=t:m.move_to([-3.7+7.4*min(clock.get_value()/t,1),y,0]));scene.add(d);d.update()
        result=label((f'{t:.0f}' if k=='C' else f'{t:.1f}')+' ms',4.95,y,30,CLS[k]);result.add_updater(lambda m,t=t:m.set_opacity(1 if clock.get_value()>=t else 0));scene.add(result);result.update()
    scene.play(clock.animate.set_value(end),run_time=duration,rate_func=linear)
    return clock
class S18Race(Timed):
    def construct(self):
        # The visible clock and dots use the same physical time throughout.
        self.add(heading('Same start • equal paths'),label('2 cm',0,-2.5,32))
        self.at('Assume their spikes');
        # Race runs over the full explanatory sentence; C continues next scene.
        self.clear();race(self,0,4,5.9);self.add(label('clock paused for comparison',0,-2.45,26,GREY));self.finish()
class S19Race2(Timed):
    def construct(self):
        # Complete C's crossing before holding the final result.
        clock=race(self,4,4,.067)
        paused=label('clock paused for comparison',0,1.85,24,GREY);self.add(paused)
        self.at('2 milliseconds apart')
        # Brackets join the finish dots on their actual lanes.
        a=VGroup(DoubleArrow([3.7,1.4,0],[3.7,0,0],buff=.16,color=GOLD,tip_length=.10),label('≈ 2 ms',5,.7,28,GOLD))
        self.play(FadeIn(a),run_time=.3)
        self.at('The C report')
        self.remove(paused)
        self.play(clock.animate.set_value(ARRIVALS[2]+.2),run_time=.8,rate_func=linear)
        b=VGroup(DoubleArrow([3.7,0,0],[3.7,-1.4,0],buff=.16,color=ORANGE,tip_length=.10),label('≈ 30 ms',5,-.7,28,ORANGE))
        self.play(FadeIn(b),run_time=.3);self.finish()
class S20Hold(Timed):
    def construct(self):
        self.add(heading('Bend → hold'))
        x=-2.7;w=8.5;xx=lambda t:x+t/3*w
        self.add(Rectangle(width=xx(2.8)-xx(.3),height=4.7,stroke_width=0,fill_color=GREY,fill_opacity=.09).move_to([(xx(2.8)+xx(.3))/2,.15,0]))
        stim=VMobject(stroke_color=TEXT,stroke_width=4).set_points_as_corners([[x,2,0],[xx(.3),2,0],[xx(.3),2.5,0],[xx(2.8),2.5,0],[xx(2.8),2,0],[xx(3),2,0]])
        self.add(stim,label('stimulus',-4.7,2.25,28))
        for k,y in zip(('RA','AD','C'),(1, -.4,-1.8)):
            self.add(label(CNAME[k],-4.7,y,30,CLS[k]),Line([x,y,0],[xx(3),y,0],color=GREY))
            ev=events(k)+.3;ev=ev[ev<2.8]
            spikes=VGroup(*[Line([xx(t),y-.27,0],[xx(t),y+.27,0],color=CLS[k],stroke_width=4) for t in ev])
            self.add(spikes)
            if k!='C':
                quiet=label('quiet',xx(ev[-1])+.8,y,26,GREY)
                quiet.add_background_rectangle(color=BG,opacity=1,buff=.08)
                self.add(quiet)
        self.add(*[label(str(t),xx(t),-2.6,26,GREY) for t in (0,1,2,3)],label('s',6.2,-2.6,26,GREY),label('Illustrative adaptation model • counts are schematic',0,-3.25,26,GREY))
        self.at('The C unit');self.play(Indicate(VGroup(*[m for m in self.mobjects if m.get_color()==ManimColor(ORANGE)]),color=ORANGE),run_time=.6);self.finish()
class S21Meaning(Timed):
    def construct(self):
        self.add(heading('2 cm to 4 cm • conduction only'))
        xx=lambda t:-3.6+t/80*8.4
        # Tick labels belong to the three plotted lanes; no empty fourth lane.
        self.add(*[label(str(t),xx(t),-1.95,26,GREY) for t in (0,20,40,60,80)],label('ms',5.6,-1.95,26,GREY))
        dots=VGroup();labs=VGroup();ghosts=VGroup()
        ys=(1.65,.35,-.95)
        for k,y,t in zip(('RA','AD','C'),ys,ARRIVALS):
            self.add(label(CNAME[k],-5.2,y,30,CLS[k]),Line([xx(0),y,0],[xx(80),y,0],color=GREY))
            dots.add(Dot([xx(t),y,0],color=CLS[k],radius=.13))
            labs.add(label(f'2 cm: {t:.1f} ms',xx(t)+1,y+.4,24,CLS[k]))
            ghosts.add(Circle(radius=.13,color=CLS[k],stroke_width=2).move_to([xx(t),y,0]))
        self.add(dots,labs)
        dist=label('2 cm',4.5,2.65,28);self.add(dist)
        self.at('On longer paths')
        self.at('every gap grows')
        self.add(ghosts)
        newlabs=VGroup(*[label(f'4 cm: {t*2:.1f} ms',xx(t*2)+.7,y-.4,24,CLS[k]) for t,y,k in zip(ARRIVALS,ys,('RA','AD','C'))])
        self.play(Transform(dist,label('○ 2 cm   ● 4 cm',3.5,2.65,26)),*[d.animate.move_to([xx(t*2),y,0]) for d,t,y in zip(dots,ARRIVALS,ys)],labs.animate.set_opacity(.65),FadeIn(newlabs),run_time=1.1)
        self.at('What fires');self.play(FadeIn(T('What fires + when it arrives\nBoth are part of what reaches the spinal cord',28,GOLD,line_spacing=1.3).move_to([0,-3,0])),run_time=.5);self.finish()
class S22Caution(Timed):
    def construct(self):
        self.add(heading('One neuron branches to many hairs'),label("Each ending’s axon also reaches other hairs",0,2.4,26,TEXT))
        fs=VGroup(*[follicle('awl',x,.1,.7) for x in (-4.7,-1.6,1.6,4.7)]);self.add(fs)
        self.at('A single neuron branches')
        self.add(label('For field-LTMRs: an arbor can reach 20–180 follicles',0,1.98,24,GREEN))
        # Separate buses for the three classes; each reaches multiple follicles.
        buses=VGroup()
        for i,k in enumerate(('RA','AD','C')):
            y=-1.4-i*.35
            buses.add(Line([-5.2,y,0],[5.2,y,0],color=CLS[k],stroke_width=3))
            for x in (-4.7,-1.6,1.6,4.7):
                bx=x+(-.48+i*.31)*.7
                points=[-.58]+[z for j in range(i) for z in (-1.4-j*.35+.07,-1.4-j*.35-.07)]+[y]
                for a,b in zip(points[::2],points[1::2]):buses.add(Line([bx,a,0],[bx,b,0],color=CLS[k],stroke_width=3))
                buses.add(Dot([bx,y,0],radius=.055,color=CLS[k]))
        self.play(Create(buses),FadeIn(VGroup(*[label(CNAME[k]+' neuron',x,-2.55,26,CLS[k]) for k,x in zip(('RA','AD','C'),(-4,0,4))])),run_time=.7)
        self.at('So endings at');self.play(FadeIn(T('Endings at a hair are not a count of neurons.',30,GOLD).move_to([0,-3.1,0])),run_time=.4);self.finish()
class S23Takeaway(Timed):
    def construct(self):
        f=follicle(x=-4,y=-.4,s=1.2);self.add(f,heading('One hair • three classes • three speeds'))
        self.at('The skin splits')
        # Each axon leaves its own side of the ending; ordered, disjoint paths.
        paths=VGroup();labs=VGroup()
        for i,(k,v) in enumerate(zip(('RA','AD','C'),VELOCITIES)):
            # Reverse vertical order of the outputs so nested routes cannot cross.
            y=-2.6+i*1.45
            start=f.pk[i].get_bottom()
            exit_y=-2.6+i*.4
            p=VMobject(stroke_color=CLS[k],stroke_width=5).set_points_as_corners([start,[start[0],exit_y,0],[-2+i*.5,exit_y,0],[-.4+i*.5,y,0],[4.2,y,0]]);paths.add(p)
            labs.add(label(f'{CNAME[k]} • {v:g} m/s',2,y+.4,28,CLS[k]))
        dest=RoundedRectangle(width=1.1,height=5.2,corner_radius=.4,color=TEXT,fill_opacity=.1).move_to([4.8,-.8,0])
        self.play(Create(paths),FadeIn(labs),FadeIn(dest),FadeIn(label('spinal cord',4.7,2.4,28)),run_time=.6)
        self.at('into parallel reports')
        travel=np.array([p.get_arc_length()/v for p,v in zip(paths,VELOCITIES)])
        travel=1.4*travel/travel.max()
        self.play(AnimationGroup(*[MoveAlongPath(Dot(p.get_start(),color=CLS[k],radius=.13),p,rate_func=linear,run_time=float(t)) for p,k,t in zip(paths,('RA','AD','C'),travel)]));self.finish()
class S24End(EndCard):
    LINE='The skin splits even a single hair movement into parallel reports.'
    def construct(self):
        self.add(T('The skin splits even a single hair\nmovement into parallel reports.',36,font=TITLE_FONT,line_spacing=1.25));self.play(FadeIn(label('biochemistrypedia.com',0,-1.6,26,TEAL)),run_time=.4);self.finish()
