"""One carried cell: unfinished job -> sensor -> wire -> brake -> commitment.
COLOR MAP: YELLOW DNA; ORANGE damage/separase; RED wait/sensors/MCC/Wee1;
GREEN recovery/Cdc25; TEAL Cdc20; BLUE APC/C; PURPLE securin; PINK cyclin B;
GOLD phosphate/ubiquitin/questions; TEXT Cdk1/kinetochores/laser; GREY cell/spindle.
All protein drawings are abstract functional shapes, never molecular structures.
"""
from bp_style import *
import math
ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58FB5'

def label(s, x=0, y=3.25, c=TEXT, size=32):
    return fit(T(s, size=size, color=c), max_w=12.5).move_to([x,y,0])

def protein(s,c,x,y):
    return chip(s,c,size=30,pad=.2).move_to([x,y,0])

def arrow(a,b,c=RED):
    return Arrow(a,b,buff=.1,color=c,stroke_width=5)

def dna(broken=False):
    g=VGroup()
    for y in [-.75,.05,.85]:
        if broken:
            g.add(Line([-2.9,y,0],[-2.05,y,0],color=YELLOW,stroke_width=12),
                  Line([-1.65,y,0],[-.8,y,0],color=YELLOW,stroke_width=12),
                  Line([-2.02,y+.17,0],[-1.68,y-.17,0],color=ORANGE,stroke_width=7))
        else:g.add(Line([-2.9,y,0],[-.8,y,0],color=YELLOW,stroke_width=12))
    return g

def world(sc,broken=False,tag='a vertebrate cell',phase=2,mitotic=False,stranded=False):
    cell=Ellipse(width=11.7,height=5.5,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.16).shift(UP*.15)
    cell.base=cell.copy(); cell.clock=0
    def breathe(m,dt):
        m.clock+=dt
        m.become(m.base.copy().scale(1+.02*math.sin(m.clock*1.15)))
    cell.add_updater(breathe)
    header=label(tag)
    track=VGroup(Line([-4.9,-2.85,0],[4.9,-2.85,0],color=GREY,stroke_width=5))
    for x,s in zip([-4.4,-2.2,0,2.2,4.4],['G1','S','G2','M','anaphase']):
        track.add(label(s,x,-3.24,size=28))
    track.add(label('schematic',0,-3.65,size=28))
    marker=Triangle(color=TEXT,fill_opacity=1).scale(.14).rotate(PI).move_to([[-4.4,-2.2,0,2.2,4.4][phase],-2.55,0])
    marker.clock=0
    def idle(m,dt):
        m.clock+=dt; m.shift(UP*(.045*math.sin(m.clock*4)-.045*math.sin((m.clock-dt)*4)))
    marker.add_updater(idle)
    chrom=spindle(stranded) if mitotic else dna(broken)
    sc.add(cell,header,track,marker,chrom)
    sc.cell,sc.header,sc.track,sc.marker,sc.chrom=cell,header,track,marker,chrom
    return cell

def brake(x=.6):
    return VGroup(Line([x,-3.02,0],[x,-2.22,0],color=RED,stroke_width=12),
                  Line([x-.25,-2.22,0],[x+.25,-2.22,0],color=RED,stroke_width=12))

def wire(start=(-1.7,.1,0),end=(2.2,1,0)):
    # A single carried signal path, wholly inside the cell.
    a=np.array(start,dtype=float); b=np.array(end,dtype=float)
    return CubicBezier(a,a+np.array([1.1,1.1,0]),
                       b+np.array([-1.3,.65,0]),b,color=RED,stroke_width=5).set_z_index(1)

def engine():
    return VGroup(protein('cyclin B',PINK,3,1.25),protein('Cdk1',TEXT,3,.35))

def sensor(x=-1.7,y=.1):
    ring=Circle(radius=.34,color=RED,stroke_width=7,fill_color=RED,fill_opacity=.35).move_to([x,y,0]); ring.clock=0
    ring.add_updater(lambda m,dt: pulse(m,dt))
    name=label('ATM/ATR' if y==.1 else 'kinetochore',x if y==.1 else x-.9,y+1.3 if y==.1 else y-.75,RED,28)
    return VGroup(ring,name).set_z_index(3)

def pulse(m,dt):
    m.clock+=dt; m.set_stroke(opacity=.65+.35*math.sin(m.clock*2)**2)

def phosphate(x,y):
    return VGroup(Dot([x,y,0],radius=.22,color=GOLD),T('P',size=28,color=BG).move_to([x,y,0]))

def spindle(stranded=False):
    poles=VGroup(Dot([-4.5,0,0],radius=.13,color=GREY),Dot([4.5,0,0],radius=.13,color=GREY))
    pairs=VGroup(); fibers=VGroup(); links=VGroup()
    for i,y in enumerate([-.8,0,.8]):
        x=-2.7 if stranded and i==0 else -.8
        pair=VGroup()
        for dx in [-.18,.18]:
            rod=Line([x+dx,y-.28,0],[x+dx,y+.28,0],color=YELLOW,stroke_width=10)
            kt=Dot([x+dx,y,0],radius=.085,color=TEXT)
            pair.add(VGroup(rod,kt))
        pairs.add(pair)
        fibers.add(Line([-4.5,0,0],[x-.18,y,0],color=GREY,stroke_width=2.5))
        if not(stranded and i==0):fibers.add(Line([4.5,0,0],[x+.18,y,0],color=GREY,stroke_width=2.5))
        links.add(Line([x-.18,y-.13,0],[x+.18,y-.13,0],color=GREY,stroke_width=6))
    g=VGroup(fibers,poles,links,pairs); g.pairs=pairs; g.links=links;g.fibers=fibers
    return g

def follow_spindle(g):
    idx=0
    for pair in g.pairs:
        for j in range(2):
            if idx>=len(g.fibers):break
            if len(g.fibers)==5 and pair is g.pairs[0] and j==1:continue
            line=g.fibers[idx];idx+=1
            pole=np.array([-4.5 if j==0 else 4.5,0,0])
            line.add_updater(lambda m,dt,p=pair[j],a=pole: m.put_start_and_end_on(a,p[1].get_center()))

def apc():
    return VGroup(protein('APC/C',BLUE,3,1.85),protein('Cdc20',TEAL,3,.95)).set_z_index(4)

def question(sc,laser=False):
    world(sc,broken=not laser,tag='PtK1 · rat-kangaroo' if laser else 'no RAD9 · irradiated',mitotic=laser,stranded=laser,phase=3 if laser else 2)
    q=label('Does anaphase wait?' if laser else 'What would mean\na repair gene?',1.5 if laser else 2.5,1.75,GOLD,34)
    sc.q=q;sc.add(q)
    if laser:
        w=wire((-2.52,-.8,0));w.set_stroke(opacity=.3);sc.add(w);sc.oldwire=w
        sc.chrom.pairs[0][1][1].set_opacity(0)
    else:sc.add(brake())

class S00Hook(SpokenScene):
    def construct(self):
        world(self,tag='budding yeast · no RAD9',phase=0)
        # The hook uses a round yeast mother, with a bud already visible.
        self.cell.clear_updaters()
        self.cell.become(Circle(radius=2.35,color=GREY,stroke_width=4,
                                fill_color=GREY,fill_opacity=.16).move_to([-1.5,.15,0]))
        seed=Circle(radius=.32,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.16).move_to([.98,.15,0])
        self.add(seed)
        self.at('irradiate it')
        rays=VGroup(*[arrow([-5.4,1.6+i*.4,0],[-3.1,.5+i*.4,0],ORANGE) for i in range(2)])
        self.play(FadeIn(rays),Transform(self.chrom,dna(True)),run_time=.7)
        self.at('does not pause')
        self.play(self.marker.animate.set_x(2.2),FadeOut(rays),run_time=1.1)
        self.at('it keeps dividing')
        buds=VGroup()
        for i,dest in enumerate(([3,1.15,0],[3,-1,0])):
            bud=VGroup(Circle(radius=.68,color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.16),
                       Line([-.35,.13,0],[-.07,.13,0],color=YELLOW,stroke_width=8),
                       Line([.1,.13,0],[.38,.13,0],color=YELLOW,stroke_width=8),
                       Line([-.07,.28,0],[.1,-.02,0],color=ORANGE,stroke_width=7)).move_to([1.48,.15,0])
            neck=VGroup(Line([.78,.4,0],[1.04,.32,0],color=GREY,stroke_width=5),
                        Line([.78,-.1,0],[1.04,-.02,0],color=GREY,stroke_width=5))
            if i==0:
                self.play(ReplacementTransform(seed,bud),FadeIn(neck),run_time=.35)
            else:
                self.play(GrowFromCenter(bud),FadeIn(neck),run_time=.35)
            self.play(bud.animate.move_to(dest),neck.animate.stretch(.05,1).set_opacity(0),run_time=.4)
            self.remove(neck);buds.add(bud)
        self.at('and dies')
        self.play(self.cell.animate.set_stroke(GREY,opacity=.35).set_fill(GREY,.04),
                  self.chrom.animate.set_color(GREY).set_opacity(.3),
                  buds.animate.set_color(GREY).set_opacity(.3),run_time=.6)
        self.at('hold it back')
        b=brake()
        self.play(*[bud.animate.move_to([-1.5,.15,0]).scale(.01) for bud in buds],
                  self.cell.animate.set_stroke(GREY,opacity=1).set_fill(GREY,.16),
                  self.marker.animate.set_x(0),Transform(self.chrom,dna(True)),FadeIn(b),run_time=.8)
        self.remove(buds)
        self.at('it repairs the damage')
        self.play(Transform(self.chrom,dna()),run_time=.8)
        self.at('what was the gene')
        self.play(Transform(self.header,label('RAD9: what was it for?',c=GOLD)),run_time=.5)
        self.finish()

class S01Title(TitleCard):
    LESSON='Checkpoints and Irreversible Transitions'
    TITLE='A Brake Wired to a Sensor'
    def construct(self):
        world(self,tag=self.TITLE)
        self.add(brake());self.wait(2)

class S02Waiting(SpokenScene):
    def construct(self):
        world(self,tag='RAD9: what was it for?'); b=brake();self.add(b)
        self.at('was needed for waiting')
        hour=VGroup(Polygon([-4.6,1.5,0],[-3.8,1.5,0],[-4.6,-.4,0],[-3.8,-.4,0],color=RED),label('needed for waiting',.9,1.8,RED))
        self.play(FadeIn(hour),run_time=.7)
        self.at('and leland hartwell')
        self.play(Transform(self.header,label('Weinert and Hartwell · 1988')),b.animate.shift(UP*.8).set_opacity(0),self.marker.animate.set_x(2.2),run_time=.9)
        self.finish()

class S03Name(SpokenScene):
    def construct(self):
        world(self,phase=0,tag='checkpoint')
        job=Rectangle(width=4,height=.45,color=YELLOW).move_to([-1.7,1.5,0]); fill=Rectangle(width=.2,height=.42,fill_color=YELLOW,fill_opacity=1,stroke_width=0).move_to([-3.6,1.5,0]);b=brake();w=wire((-1.7,1.25,0),(.6,-2.2,0))
        self.at('they named such controls')
        self.play(FadeIn(VGroup(job,fill,label('copy and repair DNA',-1.7,2.15))),run_time=.6)
        self.at('makes one cell cycle')
        self.play(Create(w),FadeIn(b),self.marker.animate.set_x(0),run_time=.7)
        self.play(fill.animate.stretch_to_fit_width(3.95).move_to([-1.7,1.5,0]).set_color(GREEN),run_time=1.2)
        self.play(b.animate.shift(UP*.8).set_opacity(0),self.marker.animate.set_x(2.2),w.animate.set_opacity(.1),run_time=.7)
        self.at('without it')
        self.play(self.marker.animate.set_x(-4.4),fill.animate.stretch_to_fit_width(2).move_to([-2.7,1.5,0]).set_color(YELLOW),FadeOut(w),run_time=.5)
        self.at('on time')
        self.play(self.marker.animate.set_x(2.2),Transform(self.header,label('on time ≠ on completion')),run_time=.9)
        self.finish()

class S04Predict(SpokenScene):
    def construct(self):
        world(self,True,'no RAD9 · irradiated');self.add(brake())
        self.at('what result would')
        self.play(FadeIn(label('What would mean\na repair gene?',2.5,1.75,GOLD,34)),run_time=.7)
        self.finish()

class S05Think(NarratedScene):
    def construct(self):
        question(self);self.wait(5)

class S06Answer(SpokenScene):
    def construct(self):
        question(self)
        self.at('if the held cells')
        upper=VGroup(Ellipse(width=4.7,height=1.65,color=GREY),Line([-1,0,0],[1,0,0],color=ORANGE,stroke_width=9)).move_to([-2.7,1.1,0])
        lower=upper.copy().move_to([-2.7,-1.15,0])
        self.play(FadeOut(self.chrom),FadeOut(self.q),FadeIn(upper),FadeIn(lower),run_time=.7)
        self.at('though not prove it')
        hedge=label('points to repair\nnot proof',2.7,1.1,ORANGE)
        self.play(FadeIn(hedge),run_time=.6)
        self.at('but more time rescued')
        self.play(FadeOut(upper),FadeOut(hedge),lower[1].animate.set_color(YELLOW),FadeIn(label('rescue: waiting',2.7,-1.15,GREEN)),run_time=.7)
        self.play(Transform(lower,dna()),run_time=.7)
        self.finish()

class S07Sensors(SpokenScene):
    def construct(self):
        world(self,tag='vertebrate cell · schematic')
        self.at('broken dna ends')
        mrn=protein('MRN',TEXT,-2.7,1.7);atm=protein('ATM',RED,-.5,1.7)
        self.play(Transform(self.chrom,dna(True)),FadeIn(mrn),run_time=.6)
        self.play(mrn.animate.move_to([-2,.1,0]),run_time=.5)
        self.play(TransformFromCopy(mrn,atm),run_time=.6)
        self.at('single strands')
        self.play(FadeOut(mrn),FadeOut(atm),run_time=.3)
        fork=VGroup(Line([-3,0,0],[-1.7,0,0],color=YELLOW,stroke_width=8),Line([-1.7,0,0],[-.7,.7,0],color=YELLOW,stroke_width=8),Line([-1.7,0,0],[-.7,-.7,0],color=YELLOW,stroke_width=8))
        rpa=VGroup(*[Dot([-1.45+i*.22,.16+i*.16,0],radius=.1,color=GREY) for i in range(3)],label('RPA',-2.7,1.6))
        atr=protein('ATR–ATRIP',RED,1.3,1.5);top=protein('TopBP1',TEXT,3.9,1.5)
        self.play(Transform(self.chrom,fork),FadeIn(rpa),run_time=.6)
        self.play(FadeIn(atr),FadeIn(top),rpa[0].animate.set_color(TEXT),run_time=.5)
        self.play(top.animate.shift(LEFT*.5),atr[0].animate.set_fill(RED,.4),run_time=.5)
        self.at('mainly switches on')
        e=engine(); w=wire(); s=sensor()
        mess=VGroup(protein('Chk2',RED,0,0),protein('Chk1',RED,0,0)).set_z_index(5)
        self.play(FadeOut(rpa),FadeOut(atr),FadeOut(top),Transform(self.chrom,dna(True)),FadeIn(e),FadeIn(s),Create(w),run_time=.7)
        for messenger in mess:
            messenger.move_to(w.get_start());self.add(messenger)
            self.play(MoveAlongPath(messenger,w),run_time=.65)
            self.play(FadeOut(messenger),run_time=.15)
        self.finish()

class S08Brake(SpokenScene):
    def construct(self):
        world(self,True);e=engine();p=VGroup(phosphate(2.4,.8),phosphate(3.6,.8));c=protein('Cdc25',GREEN,.1,.4);w=wire();self.chrom.shift(LEFT*.7);self.add(e,p,c,w,sensor())
        self.at('these messengers inhibit')
        m=VGroup(protein('Chk1',RED,0,0),protein('Chk2',RED,0,0)).set_z_index(5);tag=phosphate(.6,.9)
        for messenger in m:
            messenger.move_to(w.get_start());self.add(messenger)
            self.play(MoveAlongPath(messenger,w),run_time=.55)
            self.remove(messenger)
        self.play(FadeIn(tag),c.animate.set_color(GREY).shift(LEFT*.5),run_time=.4)
        self.at('keeps its inhibitory phosphates')
        self.play(Indicate(p,color=GOLD),e[1][0].animate.set_stroke(GREY).set_fill(GREY,.1),FadeOut(m),run_time=.7)
        self.at('the cell waits')
        self.play(FadeIn(brake()),run_time=.5);self.finish()

class S09Lift(SpokenScene):
    def construct(self):
        world(self,True);e=engine();p=VGroup(phosphate(2.4,.8),phosphate(3.6,.8));c=protein('Cdc25',GREY,-.4,.4);tag=phosphate(.1,.9);w=wire();b=brake();self.chrom.shift(LEFT*.7);self.add(e,p,c,tag,w,b)
        self.at('nothing was destroyed')
        self.play(Indicate(e,color=TEXT),run_time=.7)
        self.at('once the signal is silenced')
        self.play(Transform(self.chrom,dna().shift(LEFT*.7)),run_time=.6)
        phosph=protein('phosphatase',TEXT,-.9,1.7)
        self.play(Uncreate(w),FadeIn(phosph),run_time=.6)
        self.play(tag.animate.move_to(phosph).set_opacity(0),c.animate.set_color(GREEN),run_time=.6)
        self.at('able to recover')
        self.play(p.animate.move_to(c).set_opacity(0),FadeOut(phosph),run_time=.6)
        self.play(e[1][0].animate.set_fill(GREEN,.35),b.animate.shift(UP).set_opacity(0),self.marker.animate.set_x(2.2),run_time=.7)
        self.finish()

class S10Idea(SpokenScene):
    def construct(self):
        world(self,True,tag='A brake wired to a sensor');e=engine();s=sensor();w=wire();b=brake();self.add(e,s,w,b)
        self.at('while the sensor sees')
        self.play(Indicate(s,color=RED),run_time=.6)
        self.at('the brake holds back')
        self.play(Indicate(b,color=RED),run_time=.6)
        self.at('when the cell finally moves')
        self.play(Transform(self.chrom,dna()),s.animate.set_color(GREEN),Uncreate(w),run_time=.7)
        self.play(b.animate.shift(UP).set_opacity(0),self.marker.animate.set_x(4.4),run_time=.9)
        self.at('hard to undo')
        self.play(Create(chevron()),run_time=.5);self.finish()

def chevron():
    return VGroup(Line([2.8,-3.05,0],[3.1,-2.85,0],color=GOLD,stroke_width=7),Line([3.1,-2.85,0],[2.8,-2.65,0],color=GOLD,stroke_width=7))

class S11Kinetochore(SpokenScene):
    def construct(self):
        world(self,mitotic=True,phase=3,tag='PtK1 · rat-kangaroo · schematic');self.add(apc())
        self.at('each pair of sister chromatids')
        self.play(Indicate(self.chrom.pairs,color=YELLOW),run_time=.7)
        self.at('opposite spindle poles')
        self.play(Indicate(self.chrom[1],color=TEXT),run_time=.7)
        self.at('called kinetochores')
        k=VGroup(*[p[j][1] for p in self.chrom.pairs for j in range(2)])
        self.play(Indicate(k,color=TEXT,scale_factor=2),FadeIn(label('kinetochores',-.7,1.7)),run_time=.7);self.finish()

class S12Laser(SpokenScene):
    def construct(self):
        world(self,mitotic=True,stranded=True,phase=3,tag='PtK1 · rat-kangaroo · schematic');a=apc();s=sensor(-2.52,-.8);w=wire((-2.52,-.8,0));self.add(a,s,w)
        self.at('attached to only one pole')
        self.play(Indicate(self.chrom.pairs[0],color=RED),run_time=.6)
        self.at('with a laser')
        laser=Line([-5,2.2,0],[-2.52,-.8,0],color=TEXT,stroke_width=7)
        self.play(Create(laser),run_time=.3)
        self.play(FadeOut(s),self.chrom.pairs[0][1][1].animate.set_opacity(0),w.animate.set_stroke(opacity=.3),FadeOut(laser),run_time=.5)
        self.at('does anaphase still wait')
        self.play(FadeIn(label('Does anaphase wait?',1.5,1.75,GOLD,34)),FadeOut(a),run_time=.5);self.finish()

class S13Think(NarratedScene):
    def construct(self):
        question(self,True);self.wait(5)

class S14Answer(SpokenScene):
    def construct(self):
        question(self,True)
        self.at('anaphase followed about')
        self.play(Transform(self.q,label('about 20 min',2.5,1.75,GOLD)),FadeOut(self.oldwire),run_time=.5)
        follow_spindle(self.chrom)
        self.play(*[p[j].animate.shift((LEFT if j==0 else RIGHT)*2.3) for p in self.chrom.pairs[1:] for j in range(2)],self.marker.animate.set_x(4.4),FadeOut(self.chrom.links),run_time=.9)
        self.at('never reached the middle')
        self.play(Transform(self.q,label('never aligned',2.5,1.75,ORANGE)),run_time=.5)
        self.at('came from the unattached')
        self.chrom.fibers.clear_updaters(recursive=True)
        self.play(Transform(self.chrom,spindle(True)),FadeOut(self.q),self.marker.animate.set_x(2.2),Create(wire((-2.52,-.8,0))),FadeIn(sensor(-2.52,-.8)),run_time=.8);self.finish()

class S15Mcc(SpokenScene):
    def construct(self):
        world(self,mitotic=True,stranded=True,phase=3,tag='mitotic checkpoint');self.add(apc(),sensor(-2.52,-.8),wire((-2.52,-.8,0)))
        self.at('promote assembly')
        m=protein('MCC',RED,-2.52,-.8).set_z_index(5);self.play(GrowFromCenter(m),run_time=.6)
        self.at('it holds back')
        self.play(MoveAlongPath(m,wire((-2.52,-.8,0),(1.3,1.5,0))),run_time=1)
        self.at('marks proteins for destruction')
        targets=VGroup(protein('securin',PURPLE,-1.3,-1.6),protein('cyclin B',PINK,1.2,-1.6));self.play(FadeIn(targets),run_time=.7);self.finish()

# The notches and key tabs are functional cartoons of substrate recognition.
def decoy_stage(sc):
    world(sc,mitotic=True,phase=3,tag='Cdc20: target-recognition slots')
    sc.chrom.set_opacity(.22)
    a=protein('APC/C',BLUE,-2,1.3)
    body=Rectangle(width=3.5,height=1.3,color=TEAL,fill_color=TEAL,fill_opacity=.25).move_to([0,.4,0])
    name=label('Cdc20',0,.5,TEAL)
    slots=VGroup(*[Rectangle(width=.65,height=.45,color=TEAL,fill_color=BG,fill_opacity=1).move_to([x,-.2,0]) for x in [-.85,.85]])
    tabs=VGroup(*[Rectangle(width=.45,height=.7,color=RED,fill_color=RED,fill_opacity=.8).move_to([x,-1.15,0]) for x in [-.85,.85]])
    VGroup(a,body,name,slots,tabs).shift(UP*1.05).set_z_index(4)
    a.move_to([-3,1.8,0])
    self_mask=Rectangle(width=3.6,height=1.4,stroke_width=0,fill_color=BG,fill_opacity=1).move_to(body).set_z_index(3)
    sc.add(self_mask,a,body,name,slots);return tabs

class S16Decoy(SpokenScene):
    def construct(self):
        tabs=decoy_stage(self)
        self.at('a decoy key')
        self.play(FadeIn(tabs),run_time=.5)
        self.at('it fills the slots')
        self.play(tabs.animate.shift(UP*.9),run_time=.8)
        self.at('would grip a real target')
        targets=VGroup(protein('securin',PURPLE,-3,-1.5),protein('cyclin B',PINK,3,-1.5))
        self.play(FadeIn(targets),run_time=.5)
        self.at('are kept out')
        self.play(targets.animate.shift(UP*.7),rate_func=there_and_back,run_time=1);self.finish()

class S17Release(SpokenScene):
    def construct(self):
        world(self,mitotic=True,stranded=True,phase=3,tag='last attachment');a=apc();w=wire((-2.52,-.8,0));s=sensor(-2.52,-.8);m=protein('MCC',RED,1.3,1.5).set_z_index(5);self.add(a,w,s,m)
        self.at('last kinetochore attaches')
        self.play(Transform(self.chrom,spindle()),FadeOut(s),Uncreate(w),run_time=.7)
        self.at('come apart')
        self.play(m.animate.scale(.3).shift(DOWN).set_opacity(0),run_time=.6)
        self.at('tags securin')
        targets=VGroup(protein('securin',PURPLE,.7,1.8),protein('cyclin B',PINK,.7,.9));tags=VGroup(*[Dot([-.1+i*.25,y,0],radius=.1,color=GOLD) for y in [1.8,.9] for i in range(3)])
        self.play(FadeIn(targets),run_time=.4);self.play(FadeIn(tags),targets.animate.shift(RIGHT*.5),run_time=.5)
        self.at('the proteasome destroys them')
        barrel=VGroup(RoundedRectangle(width=2.8,height=1.1,color=GREY,fill_color=GREY,fill_opacity=.25),label('proteasome',0,0,size=28)).move_to([1.5,-1.4,0]);self.play(FadeIn(barrel),run_time=.4)
        self.play(VGroup(targets,tags).animate.move_to(barrel).scale(.1).set_opacity(0),run_time=.6)
        self.play(FadeIn(VGroup(fragments([3.1,-.95,0],PURPLE),fragments([3.1,-1.55,0],PINK))),run_time=.4);self.finish()

def fragments(pos,c=PINK):
    return VGroup(*[Square(side_length=.25,color=c,fill_opacity=1).move_to(np.array(pos)+np.array([i*.32,(i%2)*.27,0])) for i in range(4)])

class S18Anaphase(SpokenScene):
    def construct(self):
        world(self,mitotic=True,phase=3,tag='two brakes on separase');e=engine();sec=protein('securin',PURPLE,-2.5,1.8);sep=protein('separase',ORANGE,-2.5,1);self.add(e,sec,sep)
        self.at('in vertebrates')
        inhibition=arrow([2.3,.4,0],[-1.7,1,0],RED)
        self.play(Create(inhibition),run_time=.5)
        self.at('freed seperase cuts')
        self.play(FadeOut(sec),FadeOut(inhibition),e[0].animate.set_opacity(0),e[1][0].animate.set_stroke(GREY).set_fill(GREY,.1),run_time=.6)
        self.play(sep.animate.move_to([-.8,-1.6,0]),FadeOut(self.chrom.links),run_time=.7)
        self.at('and anaphase begins')
        follow_spindle(self.chrom)
        self.play(*[p[j].animate.shift((LEFT if j==0 else RIGHT)*2.5) for p in self.chrom.pairs for j in range(2)],self.marker.animate.set_x(4.4),Create(chevron()),run_time=1)
        self.at('losing cyclin b')
        self.play(Transform(self.header,label('cyclin B loss → Cdk1 off')),run_time=.6);self.finish()

class S19Oneway(SpokenScene):
    def construct(self):
        world(self,mitotic=True,phase=4,tag='Why not run backwards?')
        follow_spindle(self.chrom)
        for pair in self.chrom.pairs:
            pair[0].shift(LEFT*2.5);pair[1].shift(RIGHT*2.5)
        self.chrom.links.set_opacity(0);self.chrom.set_opacity(.22);self.chrom.links.set_opacity(0)
        p=protein('protein',TEXT,-2,.6);tag=phosphate(-1.3,1.2);sec=protein('securin',PURPLE,2,.6);self.add(p,tag,sec)
        self.at('a phosphate can be put back')
        self.play(tag.animate.shift(UP*.8),rate_func=there_and_back,run_time=1)
        self.at('within seconds to minutes')
        self.play(FadeIn(label('seconds to minutes',-2,-.6,GOLD)),tag.animate.shift(UP*.8),rate_func=there_and_back,run_time=1)
        self.at('a destroyed protein')
        ghost=DashedVMobject(sec[0].copy()).set_color(PURPLE);f=fragments([2,.6,0],PURPLE)
        self.play(FadeOut(sec),FadeIn(ghost),FadeIn(f),run_time=.5)
        self.at('must be made again')
        self.play(FadeOut(f,shift=DOWN*.7),FadeIn(label('must be made again',2,-1.4,PURPLE)),run_time=.6);self.finish()

class S20Washout(SpokenScene):
    def construct(self):
        world(self,mitotic=True,phase=3,tag='Potapova and colleagues');e=engine();self.add(e)
        cap=protein('inhibitor',TEXT,3,-.6);branch=Line([2.2,-2.85,0],[4.7,-1.8,0],color=GREY,stroke_width=5);g=label('G1-like state',3.9,-1.25)
        self.at('out of mitosis')
        self.play(FadeIn(cap),e[1][0].animate.set_stroke(GREY).set_fill(GREY,.1),Create(branch),FadeIn(g),self.marker.animate.move_to([4.7,-1.8,0]),run_time=.8)
        self.at('cyclin b was kept')
        self.play(Indicate(e[0],color=PINK),run_time=.5)
        self.at('after washout')
        self.play(FadeOut(cap,shift=UP),Transform(e[1],protein('Cdk1',TEXT,3,.35)),run_time=.5)
        self.at('many went back')
        self.play(self.marker.animate.move_to([2.2,-2.55,0]),Transform(self.header,label('cyclin B kept: many return')),run_time=.7)
        self.at('cells whose cyclin b')
        self.play(Transform(self.header,label('cyclin B destroyed')),self.marker.animate.move_to([4.7,-1.8,0]),FadeOut(e[0]),e[1][0].animate.set_stroke(GREY).set_fill(GREY,.1),run_time=.7)
        self.at('did not')
        self.play(Transform(self.header,label('cyclin B destroyed: stays out')),run_time=.5);self.finish()

def feedback(sc,high=False):
    world(sc,tag='Cdk1 activity · schematic');sc.chrom.set_opacity(0);e=engine();c=protein('Cdc25',GREEN,-1.6,1);w=protein('Wee1',RED,-1.6,-.6)
    gauge=Rectangle(width=.6,height=2.5,color=TEXT).move_to([4.8,0,0]);bar=Rectangle(width=.5,height=2.35 if high else .3,fill_color=GREEN,fill_opacity=1,stroke_width=0).move_to([4.8,-1.2+(2.35 if high else .3)/2,0]);sc.add(e,c,w,gauge,bar);return e,c,w,bar

class S21Feedback(SpokenScene):
    def construct(self):
        e,c,w,bar=feedback(self)
        self.at('switches on its activator')
        loop=CurvedArrow([2.2,1.2,0],[-1,1.3,0],angle=PI/3,color=GREEN)
        self.play(Create(loop),c[0].animate.set_fill(GREEN,.5),run_time=.7)
        self.at('switches off its inhibitor')
        stop=Line([2.3,.3,0],[-.8,-.6,0],color=RED,stroke_width=5);end=Line([-.8,-.85,0],[-.8,-.35,0],color=RED,stroke_width=6)
        self.play(Create(stop),Create(end),w[0].animate.set_stroke(GREY).set_fill(GREY,.1),run_time=.7)
        self.at('it feeds itself')
        self.play(bar.animate.stretch_to_fit_height(2.35).move_to([4.8,-.025,0]),e[1][0].animate.set_fill(GREEN,.4),self.marker.animate.set_x(2.2),run_time=.8);self.finish()

class S22Switch(SpokenScene):
    def construct(self):
        e,c,w,bar=feedback(self,True);m=protein('Chk1',RED,-3.6,1);self.add(m)
        self.at('tends to stay on')
        self.play(m.animate.shift(RIGHT*.5),c[0].animate.set_stroke(GREY).set_fill(GREY,.1),bar.animate.shift(DOWN*.1),rate_func=there_and_back,run_time=.9)
        self.at('that may be why')
        self.play(Transform(self.header,label('may explain the G2 brake')),bar.animate.stretch_to_fit_height(.3).move_to([4.8,-1.05,0]),e[1].animate.set_opacity(.4),self.marker.animate.set_x(0),run_time=.7)
        self.at('before the switch flips')
        self.play(FadeIn(brake()),c[0].animate.set_stroke(GREY).set_fill(GREY,.1),run_time=.6);self.finish()

class S23Leak(SpokenScene):
    def construct(self):
        world(self,mitotic=True,stranded=True,phase=3,tag='a mitotic brake can leak');e=engine();self.add(e,sensor(-2.52,-.8),wire((-2.52,-.8,0)),brake(2.8))
        barrel=protein('proteasome',TEXT,2.8,-1.4)
        self.at('can eventually slip out')
        self.play(FadeIn(barrel),Create(Line([2.2,-2.85,0],[4.7,-2,0],color=GREY)),run_time=.5)
        self.at('cyclin b is still slowly destroyed')
        for i in range(2):
            copy=e[0].copy();self.add(copy);self.play(copy.animate.move_to(barrel).scale(.2).set_opacity(0),run_time=.6);self.remove(copy)
        self.play(e[0].animate.set_opacity(.2),e[1].animate.set_opacity(.3),self.marker.animate.move_to([4.7,-2,0]),Transform(self.header,label('slippage: no normal anaphase')),run_time=.7);self.finish()

class S24Return(SpokenScene):
    def construct(self):
        world(self,mitotic=True,stranded=True,phase=3,tag='Is the job finished?');s=sensor(-2.52,-.8);w=wire((-2.52,-.8,0));b=brake(2.8);a=apc();self.add(s,w,b,a)
        self.at('a sensor holds the brake')
        self.play(Indicate(s,color=RED),Indicate(b,color=RED),run_time=.8)
        self.at('then destruction or feedback')
        self.play(Transform(self.chrom,spindle()),s.animate.set_color(GREEN),Uncreate(w),run_time=.6)
        targets=VGroup(protein('securin',PURPLE,1,-1.5),protein('cyclin B',PINK,3.3,-1.5));self.play(FadeIn(targets),run_time=.4)
        bits=VGroup(fragments([1,-1.5,0],PURPLE),fragments([3.3,-1.5,0],PINK))
        self.play(ReplacementTransform(targets,bits),b.animate.shift(UP).set_opacity(0),self.marker.animate.set_x(4.4),run_time=.8)
        self.play(FadeOut(bits,shift=DOWN*.3),run_time=.4)
        self.at('hard to take back')
        self.play(Create(chevron()),run_time=.5);self.finish()

class S25End(EndCard):
    LINE='Checkpoints make the cell wait; destruction and feedback make it commit.'
    def construct(self):
        lines=VGroup(label('Checkpoints make the cell wait;',y=.6,size=42),label('destruction and feedback make it commit.',y=-.35,size=42))
        fit(lines,max_w=12.5);self.add(lines)
        rule=Line([-4,-1.3,0],[4,-1.3,0],color=GOLD,stroke_width=5)
        self.play(Create(rule),run_time=1);self.finish()
