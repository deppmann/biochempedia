"""How Microglia Let a Touch Through.
COLOR MAP: BLUE withdrawal threshold; TEAL innocuous touch; RED blocked;
GREY cells and compartments; TEXT neuronal signalling; GOLD model annotations.
Behavioural levels are qualitative state diagrams, never experimental time series.
Passive traces and bars are computed from V=sum(gE)/sum(g).
"""
import numpy as np
from bp_style import *


def label(s,x=0,y=0,size=30,color=TEXT):
    return T(s,max(30,size),color).move_to([x,y,0])

def head(s):
    return fit(label(s,0,3.15,34),12.5,0.7)

def box(s,x,y,size=32,color=TEXT):
    return chip(s,color,size=size,pad=.22).move_to([x,y,0])

def arr(a,b,color=TEXT):
    return Arrow(a,b,buff=.08,color=color,stroke_width=4)

def cell(x=0,y=0,r=.8,micro=False):
    p=np.array([x,y,0]); soma=Circle(r,color=GREY,fill_opacity=.18).move_to(p)
    branches=VGroup()
    for a in ([.2,1.25,2.4,3.3,4.4,5.5] if micro else [.7,2.7,4.5]):
        u=np.array([np.cos(a),np.sin(a),0]); v=np.array([-u[1],u[0],0]); q=p+u*r*1.65
        branches.add(Line(p+u*r,q,color=GREY,stroke_width=4))
        if micro: branches.add(Line(q,q+u*.22+v*.22,color=GREY),Line(q,q+u*.22-v*.22,color=GREY))
    return VGroup(soma,branches)

def rodent(x=0,y=0,scale=1,rat=False):
    # Rats have a long heavy body, wedge-shaped muzzle, small ears and a long tail.
    body=Ellipse(width=3.0 if rat else 2.3,height=1.25 if rat else 1.15,color=GREY,fill_opacity=.3)
    nose=(Polygon([1,.45,0],[2.05,-.05,0],[1.1,-.4,0],color=GREY,fill_opacity=.3) if rat else Ellipse(width=.9,height=.65,color=GREY,fill_opacity=.3).move_to([1.1,.1,0]))
    ear=Circle(.17 if rat else .27,color=GREY,fill_opacity=.5).move_to([1.05 if rat else .8,.48 if rat else .55,0])
    tail=ArcBetweenPoints([-1.45 if rat else -1.1,0,0],[-3.2 if rat else -2,-.5,0],angle=-.8,color=GREY,stroke_width=4)
    feet=VGroup(*[Line([a,-.4,0],[a+.2,-.75,0],color=GREY,stroke_width=5) for a in [-.7,.7]])
    eye=Dot([1.5 if rat else 1.25,.18,0],radius=.05,color=TEXT)
    animal=VGroup(body,nose,ear,tail,feet,eye).scale(scale).move_to([x,y,0])
    if rat: animal.add(label('rat',x,y-.95*scale,30))
    return animal

def brain(x=-.6,y=1.5):
    b=VGroup(Ellipse(width=1.25,height=.9,color=GREY),Arc(radius=.3,start_angle=0,angle=PI,color=GREY).shift(LEFT*.25),Line([0,-.4,0],[.2,-.75,0],color=GREY))
    return VGroup(b.move_to([x,y,0]),label('brain',x,y-.9))

def neuron():
    return VGroup(cell(-3.7,-.25,1.1),arr([-2.75,.2,0],[-.8,1.45,0]),label('lamina I neuron',-3.7,-2.4),brain())

def vy(v): return -2.55+(v+75)/35*4.9

def gauge(e=-70,v=-56.25):
    rail=Line([2.5,-2.55,0],[2.5,2.35,0],color=GREY,stroke_width=5)
    ticks=VGroup(*[VGroup(Line([2.35,vy(z),0],[2.65,vy(z),0],color=GREY),label(f'−{abs(z)}',1.35,vy(z),30)) for z in [-70,-65,-55,-50,-40]])
    th=VGroup(DashedLine([2.8,vy(-50),0],[5.9,vy(-50),0],color=GOLD),label('threshold',4.9,vy(-50)+.38,30,GOLD))
    ep=VGroup(Line([2.25,vy(e),0],[2.85,vy(e),0],color=TEAL,stroke_width=7),label('E_anion',4.7,vy(e),30,TEAL))
    vm=VGroup(Dot([2.5,vy(v),0],radius=.13,color=TEXT),label('V',3.15,vy(v),30))
    return VGroup(rail,ticks,th,ep,vm,label('mV',1.35,-3.15))

def membrane():
    return VGroup(Line([-6.1,0,0],[-3.9,0,0],color=GREY,stroke_width=24),Line([-2.5,0,0],[.1,0,0],color=GREY,stroke_width=24),label('outside',-5,1.8),label('inside · lamina I neuron',-3.2,-2.7))

def transport_membrane():
    return VGroup(Line([-6.2,0,0],[.4,0,0],color=GREY,stroke_width=24),label('outside',-5.25,1.25),label('inside · lamina I neuron',-3,-2.7))

def transporter():
    body=RoundedRectangle(width=2.2,height=1.3,corner_radius=.22,color=TEXT,fill_color=BG,fill_opacity=1).move_to([-3.2,0,0])
    arrow=arr([-3.2,-1.5,0],[-3.2,1.65,0],TEAL)
    return VGroup(body,arrow,label('KCC2',-1.05,.8,34),label('coupled outward transport',-3.1,2.45,30))

def resting_gauge(e=-55):
    # Closed synaptic inputs: a resting reference, distinct from the touch-on model.
    g=gauge(e,-65)
    g[4][1].become(label('V_rest',3.65,vy(-65)-.4,30))
    g[5].move_to([1.35,-2.95,0])
    g.add(label('no touch · synaptic inputs closed',3.5,-3.55,30))
    return g

def ions(x=-3.2,y=1.2,n=5):
    return VGroup(*[VGroup(Dot([x+(i%3-.8)*.48,y+(i//3)*.45,0],radius=.13,color=TEXT)) for i in range(n)])

def predict1(): return VGroup(neuron(),resting_gauge(),head('What happens to inhibition’s grip?'))

def think(scene,question):
    scene.camera.background_color=BG; scene.add(question)
    cue=label('Think · 5',-1.2,-3.2,30,GOLD); scene.add(cue)
    for n in range(5,0,-1):
        cue.become(label(f'Think · {n}',-1.2,-3.2,30,GOLD)); scene.wait(1)

def grid(a='?',b='?',c='?'):
    rows=VGroup()
    for y,s,result in [(1.25,'Male · intact',a),(-.35,'Female · intact',b),(-1.95,'Female · lacking\nadaptive immune cells',c)]:
        val='No, under the\nconditions tested' if result=='No' else result
        rows.add(VGroup(RoundedRectangle(width=12,height=1.45,corner_radius=.15,color=GREY).move_to([0,y,0]),label(s,-2.6,y,32),label(val,3.35,y,30)))
    return VGroup(head('Does microglial inhibition reverse hypersensitivity?'),rows,label('mice',0,-3.05))

def predict2():
    g=grid('Yes','No','?'); g[2].become(label('What happens without adaptive immune cells?',0,2.45,30,GOLD))
    return g

# Behavioural plots deliberately use labelled discrete qualitative states: no fabricated data.
def behavior(names,levels,left=-4.6,right=5.4,bottom=-1.8,top=1.9):
    xs=np.linspace(left,right,len(names)); ys=[bottom+.35+(top-bottom-.65)*v for v in levels]
    frame=VGroup(Line([left-.4,bottom,0],[left-.4,top+.25,0],color=BLUE),Line([left-.4,bottom,0],[right+.4,bottom,0],color=GREY),label('Withdrawal threshold · higher = less sensitive',0,2.5,32,BLUE),label('qualitative states · not measured values',0,-3.2,30))
    tags=VGroup(*[label(name,x,bottom-.65,30) for name,x in zip(names,xs)])
    marks=VGroup(*[VGroup(Line([x-.4,y,0],[x+.4,y,0],color=BLUE,stroke_width=7),Dot([x,y,0],color=BLUE)) for x,y in zip(xs,ys)])
    links=VGroup(*[DashedLine([xs[i]+.5,ys[i],0],[xs[i+1]-.5,ys[i+1],0],color=BLUE) for i in range(len(xs)-1)])
    return VGroup(frame,tags,marks,links)

class S00Title(TitleCard):
    LESSON='When Pain Persists'
    TITLE='How Microglia Let a Touch Through'

class S01Q(SpokenScene):
    def construct(self):
        cord=Ellipse(width=6.7,height=5.7,color=TEXT,fill_color=GREY,fill_opacity=.12).move_to([-2,-.3,0])
        # Butterfly grey matter with paired dorsal and ventral horns inside white matter.
        pts=[[-.3,1.25,0],[-1.45,2,0],[-1.05,.5,0],[-1.5,-1.5,0],[-.6,-1.2,0],[0,-.5,0],[.6,-1.2,0],[1.5,-1.5,0],[1.05,.5,0],[1.45,2,0],[.3,1.25,0]]
        grey=Polygon(*pts,color=GREY,fill_opacity=.7).shift(LEFT*2+DOWN*.3)
        horn=Polygon([-1.7,.95,0],[-.55,1.7,0],[-.95,.2,0],color=TEAL,fill_opacity=.5)
        self.add(cord,grey,head('What changed in the cord? Who changed it?'))
        self.at('After a nerve injury'); self.play(FadeIn(horn),run_time=.4)
        rat=rodent(3.9,-.4,.8,True)
        touch_arrow=arr([3,-2.2,0],rat[4][1].get_end(),TEAL)
        self.at('a light touch'); self.play(FadeIn(rat),GrowArrow(touch_arrow),FadeIn(label('touch → withdrawal',3.7,-2.8,30,TEAL)),run_time=.6)
        self.play(rat.animate.shift(UP*.3),touch_arrow.animate.shift(UP*.3),run_time=.35)
        self.at('What changed'); self.play(Create(Line([-.7,1.4,0],[2.2,1.8,0],color=TEAL)),FadeIn(label('dorsal horn',3.6,1.8,32,TEAL)),run_time=.5); self.finish()

class S02Neuron(SpokenScene):
    def construct(self):
        n=VGroup(cell(-2,-.2,1.6),arr([-.5,.3,0],[3.9,1.25,0]),label('lamina I neuron',-2,-3,36),brain(4.8,1.4)); self.add(n[0],n[2])
        self.at('Meet a'); self.play(Indicate(n[0]),run_time=.5)
        self.at('in the outermost'); self.play(FadeIn(head('Outermost dorsal horn · lamina I')),run_time=.4)
        self.at('It sends signals'); self.play(GrowArrow(n[1]),FadeIn(n[3]),run_time=.5)
        d=Dot(n[1].get_start(),color=TEXT); self.add(d); self.play(d.animate.move_to(n[1].get_end()),run_time=.7); self.remove(d); self.finish()

class S03Inhib(SpokenScene):
    def construct(self):
        g=gauge(-70,-65); n=neuron(); self.add(n,g,head('Simple picture · inputs balance'))
        self.at('a light touch'); self.play(GrowArrow(arr([-6,-.3,0],[-4.9,-.3,0],TEAL)),Transform(g[4],gauge(-70,-53)[4]),run_time=.7)
        syn=VGroup(Circle(.4,color=TEXT,fill_opacity=.6).move_to([-3.7,-1.4,0]),Line([-4.25,-1.6,0],[-3.15,-1.6,0],color=TEXT,stroke_width=8),label('inhibitory\nsynapse',-.7,-1.2,32),Line([-1.7,-1.2,0],[-3.2,-1.4,0],color=GREY))
        self.at('Inhibitory synapses'); self.play(FadeIn(syn),Transform(g[4],gauge(-70,-56.25)[4]),run_time=.8); self.finish()

class S04Chloride(SpokenScene):
    def construct(self):
        g=gauge(-70,-53); self.add(membrane(),g,head('Chloride channels · pull toward E_anion'))
        gate=VGroup(Line([-3.65,-.5,0],[-3.65,.5,0],color=TEXT,stroke_width=8),Line([-2.75,-.5,0],[-2.75,.5,0],color=TEXT,stroke_width=8),label('channel',-1.1,1.2),Line([-1.7,1,0],[-2.8,.5,0],color=GREY))
        self.at('Those synapses'); self.play(FadeIn(gate),run_time=.4)
        flow=ions(n=6); self.add(label('Cl−',-3.2,2.2))
        self.at('pass chloride'); self.play(FadeIn(flow),run_time=.2); self.play(flow.animate.shift(DOWN*2.5),run_time=.9)
        self.at('They pull the voltage'); self.play(Transform(g[4],gauge(-70,-56.25)[4]),run_time=1)
        self.add(label('model balance: −56.2 mV',-3.2,-1.9,30)); self.finish()

class S05Kcc2(SpokenScene):
    def construct(self):
        self.add(transport_membrane(),gauge(-70,-56.25),head('Keeping the reversal potential low'))
        tr=transporter(); self.at('a transporter'); self.play(FadeIn(tr),run_time=.5)
        pair=VGroup(label('K+',-3.95,-1.4,34),label('Cl−',-2.45,-1.4,34))
        self.at('carries potassium'); self.play(FadeIn(pair),run_time=.25); self.play(pair.animate.shift(UP*2.9),run_time=1.3); self.finish()

class S06Coull(SpokenScene):
    def construct(self):
        g=gauge(-70,-56.25); tr=transporter(); self.add(transport_membrane(),g,tr,head('Coull, De Koninck and colleagues · 2003 · rats'))
        self.at('had less'); self.play(tr[0].animate.set_opacity(.25),tr[1].animate.set_opacity(.15),Transform(tr[2],label('less KCC2',-1.05,.8,34)),FadeIn(ions(-3.5,-1.7,6)),FadeIn(label('Cl− builds up',-3.2,-2.15,30)),Transform(g[3],gauge(-65)[3]),run_time=.8); self.finish()

class S07Shift(SpokenScene):
    def construct(self):
        g=resting_gauge(-65); self.add(neuron(),g,head('Reversal potential moves; voltage need not change'))
        self.at('Their anion'); self.play(Transform(g[3],gauge(-55)[3]),run_time=1.4)
        self.at('That does not'); self.play(Indicate(g[4],color=TEXT),run_time=.6); self.finish()

class S08Predict(SpokenScene):
    def construct(self):
        p=predict1(); self.add(p); self.at('what happens'); self.play(Indicate(p[1][3]),run_time=.6); self.finish()

class S09Pause(Scene):
    def construct(self): think(self,predict1())


def balance(e=-70):
    v=(-65+e)/2.4
    # Full reversal-potential range, including the excitatory anchor at 0 mV.
    yy=lambda z:-2.2+(z+75)/75*4.5
    scale=VGroup(Line([0,-2.5,0],[0,2.4,0],color=GREY),*[VGroup(Line([-.15,yy(z),0],[.15,yy(z),0],color=GREY),label(f'−{abs(z)}',.65 if z in [-70,-55] else 1.85,yy(z),30)) for z in [-70,-65,-55,-50]],label('0 mV',.7,yy(0),30))
    scale.add(*[Line([.15,yy(z),0],[1.4,yy(z),0],color=GREY,stroke_width=1) for z in [-65,-50]])
    anchors=VGroup()
    for name,E,x,c in [('leak · 1',-65,-1.9,GREY),('touch · 0.4',0,3.8,TEAL),('inhibition · 1\n(E_anion)',e,-3.9,TEXT)]:
        p=[x,yy(E),0]
        tx=-5.15 if x==-3.9 else (-1.9 if x==-1.9 else 4.8)
        ty=-2.65 if x==-1.9 else yy(E)
        anchors.add(VGroup(Dot(p,color=c),Line(p,[0,yy(v),0],color=c,stroke_width=4),label(name,tx,ty,30,c)))
    return VGroup(scale,anchors,Dot([0,yy(v),0],radius=.16,color=TEXT),head('Balance point · voltage = Σ(g × E) / Σg'),label('steady state · no injected current · weights = conductances',0,-3.2,30))

class S10Rule(SpokenScene):
    def construct(self):
        p=predict1(); self.add(p)
        self.at('Recall the balance'); b=balance(); self.play(FadeOut(p),FadeIn(b),run_time=.8)
        self.at('The synapse'); self.play(Indicate(b[1][2],scale_factor=1.04),run_time=.6); self.finish()

class S11Reveal(SpokenScene):
    def construct(self):
        b=balance(); self.add(b)
        self.at('as that potential'); self.play(Transform(b,balance(-55)),run_time=1.1)
        self.at('the pull weakens'); self.play(Transform(b[3],head('Same conductance · weaker pull near threshold')),run_time=.4)
        need=lambda e:(15+(-50-e))/50
        x=2.6; y=-1.3
        ghost=Rectangle(width=need(-70)*4,height=.3,color=TEAL).move_to([x+need(-70)*2,y,0]).set_opacity(.35)
        bar=ghost.copy().set_fill(TEAL,.7).set_opacity(1)
        labels=VGroup(label('excitation needed',4,.1,30,TEAL),label('0.70 → 0.40',4,-2,30,TEAL),label('relative conductance',3.9,-2.55,30))
        self.at('Less excitation'); self.play(FadeIn(ghost),FadeIn(bar),FadeIn(labels),run_time=.3)
        self.play(bar.animate.stretch(need(-55)/need(-70),0,about_edge=LEFT),run_time=.8); self.finish()

class S12Numbers(SpokenScene):
    def construct(self):
        self.add(head('Illustrative passive model · not measurements'),label('Leak 1 at −65 mV · inhibition 1 · touch 0.4 at 0 mV',0,2.4,30),label('Threshold −50 mV',0,1.8,30))
        self.add(label('E_anion',-4.8,.95,32),label('Steady voltage',-1.5,.95,32),label('Result',2,.95,32),Line([4.65,-2.4,0],[4.65,.05,0],color=GREY),label('mV',5.5,.65,30))
        # Unique word cues avoid the earlier repeated “it sits” alignment ambiguity.
        for phrase,e,y,state,c in [('this touch leaves',-70,-.1,'below',TEXT),('With the reversal',-55,-1.1,'at boundary',GOLD),('At minus',-50,-2.1,'above',TEAL)]:
            row=VGroup(label(f'−{abs(e)} mV',-4.8,y,44),label(f'−{abs((-65+e)/2.4):.1f} mV',-1.5,y,44),label(state,2,y,40,c))
            gy=-2.3+(e+70)/20*2.3
            tick=VGroup(Line([4.45,gy,0],[4.85,gy,0],color=c,stroke_width=5),label(f'−{abs(e)}',5.6,gy,30,c))
            self.at(phrase,nth=1 if e==-50 else 0); self.play(FadeIn(row),FadeIn(tick),run_time=.4)
            if e==-50: self.add(label('Equilibrium values; threshold crossing needs sustained input.',0,-3.1,30))
        self.finish()

class S13Notflip(SpokenScene):
    def construct(self):
        wrong=box('Inhibition flips\nto excitation',0,1.35,56); right=box('Inhibition weakens',0,-1.05,56)
        self.add(wrong,right,label('steady-state model · real cells: timing and location also matter',0,-3.1,30))
        self.at('Inhibition did not'); self.play(wrong.animate.set_opacity(.35),*[Create(Line([wrong.get_left()[0]+.2,y,0],[wrong.get_right()[0]-.2,y,0],color=RED,stroke_width=7)) for y in [1.72,.98]],run_time=.5)
        self.at('It only'); self.play(right.animate.set_color(TEAL),run_time=.5); self.finish()

class S14Who(SpokenScene):
    def construct(self):
        n=neuron(); n.remove(n[1],n[3]); m=cell(3,-.1,1.25,True)
        self.add(n.set_opacity(.3),m,label('?',3,2,54),head('Who changed the neuron?'))
        self.at('Not a neuron'); self.play(Indicate(m),run_time=.5); self.finish()

class S15Tsuda(SpokenScene):
    def construct(self):
        micro=cell(-3.9,0,1,True); others=VGroup(cell(.4,0,.9),cell(4.4,0,.9,True))
        self.add(micro,head('Tsuda and colleagues · rats'),label('microglia',-3.9,-2,34),label('resident immune cells of the cord',-2.3,-3.15,30))
        rec=VGroup(*[RoundedRectangle(width=.3,height=.6,corner_radius=.1,color=TEXT,fill_color=TEXT,fill_opacity=.5).move_to([-3.9+dx,dy,0]) for dx,dy in [(-1,0),(1,0),(0,1)]])
        atp=ions(-5.1,1.8,4)
        self.at('found'); self.play(FadeIn(rec),FadeIn(atp),FadeIn(label('ATP',-5.2,2.55,30)),FadeIn(label('P2X4',-2.1,1.8,34)),Create(Line([-2.7,1.6,0],[-3.1,.3,0],color=TEXT)),run_time=.6)
        self.at('Microglia are'); self.play(FadeIn(others),FadeIn(label('neuron',.4,-2,34)),FadeIn(label('astrocyte',4.4,-2,34)),run_time=.4)
        self.add(label('no P2X4 detected',2.4,-2.65,30))
        for x in [.4,4.4]: self.add(DashedVMobject(RoundedRectangle(width=.3,height=.6,corner_radius=.1).move_to([x+.9,0,0]),num_dashes=8).set_opacity(.5))
        self.finish()

class S16Need(SpokenScene):
    def construct(self):
        p=behavior(['before\ninjury','after\ninjury','P2X4\nlowered'],[1,0,1]); self.add(p[0],p[1],p[2][:2],p[3][0],head('Test 1 · was P2X4 needed?'))
        self.at('Lowering'); self.play(Create(p[3][1]),FadeIn(p[2][2]),run_time=1)
        self.at('So the receptor'); self.play(Transform(p[0][3],label('The receptor was needed',0,-3.2,34)),run_time=.4); self.finish()

class S17Enough(SpokenScene):
    def construct(self):
        p=behavior(['naive','after transfer'],[1,0],left=0,right=5.2); p[0][2].become(label('Withdrawal threshold',2.4,2.5,32,BLUE)); self.add(p[0],p[1],p[2][0],head('Test 2 · were stimulated cells enough?'))
        c=cell(-4,1,.5,True); dish=Ellipse(width=3,height=.7,color=GREY).move_to([-4,.6,0]); rat=rodent(-3.7,-1.1,.8,True)
        self.at('stimulated with'); self.play(FadeIn(c),FadeIn(dish),FadeIn(label('ATP',-4,2.2)),run_time=.4)
        self.at('were transferred'); self.play(FadeIn(rat),c.animate.move_to([-3.7,-.9,0]),run_time=.8)
        self.at('Those rats'); self.play(Create(p[3][0]),FadeIn(p[2][1]),run_time=.8)
        self.at('so stimulated'); self.play(Transform(p[0][3],label('Stimulated cells were enough · higher = less sensitive',0,-3.2,30)),run_time=.4); self.finish()

# Shared membrane receptor picture remains present through the cause and effect.
def trkb_receptor(x,y):
    # A large extracellular cup seated on the soma membrane.
    return VGroup(Line([x+.4,y,0],[x-.15,y,0],color=TEXT,stroke_width=8),
                  Line([x-.15,y,0],[x-.4,y+.32,0],color=TEXT,stroke_width=8),
                  Line([x-.15,y,0],[x-.4,y-.32,0],color=TEXT,stroke_width=8))

def bdnf_arc(x,y):
    return VGroup(*[Dot([x+dx,y+dy,0],radius=.09,color=TEXT) for dx,dy in [(-1.65,.2),(-1.4,.55),(-1.05,.75),(-.7,.7),(-.4,.5),(-.25,.15)]])

def messenger():
    micro=cell(-5.2,.1,.6,True); n=cell(-1.5,-.25,1.1)
    receptor=VGroup(trkb_receptor(-2.6,-.25),label('TrkB',-1.45,1.8,32),Line([-2,1.5,0],[-2.95,.15,0],color=GREY))
    dots=bdnf_arc(-2.6,-.25)
    return VGroup(micro,n,receptor,dots,label('microglia',-5.1,-1.6),label('lamina I\nneuron',-1.35,-2.6),label('BDNF',-4.2,1.55,32))

class S18Bdnf(SpokenScene):
    def construct(self):
        m=messenger(); self.add(m[0],m[1],m[4],m[5],gauge(),head('Coull and colleagues · 2005 · rats'))
        self.at('release'); self.play(FadeIn(m[3]),FadeIn(m[6]),run_time=.25)
        self.play(m[3].animate.shift(RIGHT*.15),run_time=1); self.finish()

class S19Trkb(SpokenScene):
    def construct(self):
        m=messenger(); g=gauge(); self.add(m[0],m[1],m[3],m[4],m[5],m[6],g,head('BDNF → TrkB → reversal-potential shift'))
        self.at('acts through'); self.play(FadeIn(m[2]),m[3].animate.shift(RIGHT*.1),run_time=.8)
        self.at('It shifts'); self.play(Transform(g[3],gauge(-55)[3]),run_time=1.4)
        self.at('the same change'); self.play(Indicate(g[3]),run_time=.5); self.finish()

class S20Block(SpokenScene):
    def construct(self):
        n=cell(-3.8,-.2,1.05)
        receptor=trkb_receptor(-4.85,-.2)
        dots=bdnf_arc(-4.85,-.2)
        def middle(e):
            y=lambda v:-2.25+(v+75)/35*4.4
            return VGroup(Line([0,-2.25,0],[0,2.15,0],color=GREY),*[VGroup(Line([-.15,y(z),0],[.15,y(z),0],color=GREY),label(f'−{abs(z)}',-.85,y(z),30)) for z in [-70,-55,-50]],label('mV',-.8,2.25),Line([-.2,y(e),0],[.3,y(e),0],color=TEAL,stroke_width=7),label('E_anion',1.2,y(e),30,TEAL),Dot([0,y(-56.25),0],radius=.12,color=TEXT),label('V',.45,y(-56.25)-.35,30))
        g=middle(-55)
        self.add(n,receptor,dots,g,head('Block TrkB signalling · both effects reverse'),label('TrkB',-3.7,1.65,32),Line([-4.15,1.35,0],[-5.2,.15,0],color=GREY),label('BDNF',-5.75,1.5,30),label('lamina I neuron',-3.8,-2.6,30))
        plot=VGroup(Line([3,-2.1,0],[3,1.6,0],color=BLUE),label('Withdrawal\nthreshold',4.7,2.1,30,BLUE),label('higher = less sensitive',4.5,-3.55,30),Line([3.5,-1.5,0],[4.2,-1.5,0],color=BLUE,stroke_width=7),label('with BDNF\nsignalling',3.65,-2.5,30),label('TrkB\nblocked',5.65,-2.5,30))
        self.add(plot)
        self.at('Block that'); self.play(Create(Cross(receptor,stroke_color=RED)),dots.animate.shift(RIGHT*.2),run_time=.3); self.play(dots.animate.shift(LEFT*.05),run_time=.3)
        self.at('both the shift'); self.play(Transform(g,middle(-70)),Create(DashedLine([4.3,-1.4,0],[5.3,.7,0],color=BLUE)),Create(Line([5.2,.8,0],[5.95,.8,0],color=BLUE,stroke_width=7)),run_time=1); self.finish()


def chain():
    names=['injury','P2X4 in\nmicroglia','BDNF','TrkB','E_anion\nshift','weaker\ninhibition','touch that\nfires']
    positions=[(-5,1),(-1.8,1),(1.4,1),(4.8,1),(4.8,-1.2),(1,-1.2),(-3.5,-1.2)]
    nodes=VGroup(*[box(n,x,y,34) for n,(x,y) in zip(names,positions)])
    links=VGroup()
    for i in range(6):
        start=nodes[i].get_right() if i<3 else (nodes[i].get_bottom() if i==3 else nodes[i].get_left())
        end=nodes[i+1].get_left() if i<3 else (nodes[i+1].get_top() if i==3 else nodes[i+1].get_right())
        links.add((DashedLine if i==5 else Line)(start,end,color=GOLD if i==5 else GREY,stroke_width=4))
    tags=VGroup(label('P2X4 · Tsuda 2003',-3.4,.15,30),label('BDNF / TrkB · Coull 2005',3.1,2.2,30),label('KCC2 / E_anion · Coull 2003',3.2,-2.3,30),label('model',-1.6,-1.95,30,GOLD))
    return VGroup(nodes,links,tags)

class S21Chain(SpokenScene):
    def construct(self):
        c=chain(); self.add(c[0][:6],c[1][:5],head('Three papers · different links · rats'))
        self.at('different links'); self.play(FadeIn(c[2][:3]),run_time=.5)
        self.at('was always'); self.play(Create(Line([-6,-3,0],[6,-3,0],color=BLUE)),FadeIn(label('Behavioural readout: withdrawal threshold',0,-3.5,30,BLUE)),run_time=.4)
        self.at('The last link'); self.play(FadeIn(c[0][6]),Create(c[1][5]),FadeIn(c[2][3]),run_time=.6); self.finish()

class S22Sorge(SpokenScene):
    def construct(self):
        # A readable two-row recap occupies 40% of the frame width.
        c=chain(); c.remove(c[2]); c.scale(.48).move_to([3.35,2.25,0])
        self.add(c,head('Sorge, Mapplebeck and colleagues · mice').shift(UP*.25))
        # Put the experimental groups on screen immediately; injury lowers both bars together.
        mice=VGroup(rodent(-4.5,.9,.48),rodent(-4.5,-1.25,.48),label('male',-4.5,1.8,32),label('female',-4.5,-.35,32))
        self.add(mice)
        bars=VGroup(*[Line([-3.1,y,0],[-1.8,y,0],color=BLUE,stroke_width=7) for y in [1.05,-1.1]])
        self.add(bars.copy().set_opacity(.25),bars)
        rows=VGroup()
        for y,name in [(.25,'Male · intact'),(-1.2,'Female · intact'),(-2.65,'Female · lacking\nadaptive immune cells')]:
            rows.add(VGroup(RoundedRectangle(width=7.1,height=1.25,corner_radius=.1,color=GREY).move_to([2.6,y,0]),label(name,1.9,y,30),label('?',5.3,y,32)))
        self.add(rows,label('microglial inhibitor?',2.6,1.12,30),label('withdrawal\nthreshold',-2.15,2.05,30,BLUE))
        self.at('gave male'); self.play(bars.animate.shift(DOWN*.65),FadeIn(label('Comparable drop',-3.8,-2.65,32,BLUE)),run_time=.8)
        self.at('The hypersensitivity'); self.play(Indicate(bars),run_time=.5); self.finish()

class S23Males(SpokenScene):
    def construct(self):
        g=grid(); self.add(g)
        self.at('reversed'); self.play(Transform(g[1][0][2],grid('Yes')[1][0][2]),run_time=.4)
        self.at('it did not'); self.play(Transform(g[1][1][2],grid('Yes','No')[1][1][2]),run_time=.4); self.finish()

class S24Predict(SpokenScene):
    def construct(self):
        p=predict2(); self.add(p)
        self.at('What does the inhibitor'); self.play(Indicate(p[1][2][0],scale_factor=1.01,color=GOLD),run_time=.6); self.finish()

class S25Pause(Scene):
    def construct(self):
        p=predict2(); think(self,p)

class S26Reveal(SpokenScene):
    def construct(self):
        g=predict2(); self.add(g)
        self.at('It works'); self.play(Transform(g[1][2][2],grid('Yes','No','Yes')[1][2][2]),run_time=.4)
        self.at('can switch'); self.play(Transform(g[2],label('microglia ⇄ adaptive immune cells · route can switch',0,2.45,30)),run_time=.4); self.finish()

class S27Rats(SpokenScene):
    def construct(self):
        self.add(head('Separate rat study · intact animals'),rodent(-3.8,.2,1.05,True),box('Male · yes',1.6,1.2,40),box('Female · no',1.6,-.3,40),label('Adaptive-cell condition: shown for mice',0,-1.8,30))
        self.at('but it stays'); self.play(FadeIn(box('Conditional on model and assay',0,-2.9,34)),run_time=.5); self.finish()

class S28Macro(SpokenScene):
    def construct(self):
        gang=Ellipse(width=6.5,height=4.4,color=GREY).move_to([-3,-.2,0]); n=cell(-3,-.2,.8)
        sites=[(-4.9,.6),(-1.2,.8),(-4.7,-1.1),(-1.2,-1.2),(-3.8,1.1),(-2.3,1.2),(-3.7,-1.55),(-2.3,-1.55)]
        macros=VGroup(*[VGroup(Circle(.3,color=GREY,fill_opacity=.55),Circle(.12,color=TEXT,fill_opacity=.2).shift(LEFT*.06)).move_to([x,y,0]) for x,y in sites])
        self.add(gang,n,head('Dorsal root ganglion · another immune route'),label('sensory neuron',-3,-2.9,30),label('macrophages',-3,2.35,32),macros[:2])
        self.at('Macrophages'); self.play(*[m.animate.scale(1.35) for m in macros[:2]],LaggedStart(*[FadeIn(m,scale=.5) for m in macros[2:]],lag_ratio=.1),run_time=.8)
        mouse=rodent(3.8,1.2,.8); bodydots=VGroup(*[Dot([x,y,0],radius=.12,color=GREY) for x,y in [(3.2,1.2),(3.7,1.4),(4.2,1.2),(4.5,1)]])
        self.at('In mice'); self.play(FadeIn(mouse),FadeIn(bodydots),FadeIn(label('mice · both sexes',3.8,2.35,30)),run_time=.4)
        self.at('depleting macrophages'); self.play(macros.animate.set_opacity(.15),bodydots.animate.set_opacity(.1),*[Create(Cross(m,stroke_color=RED,stroke_width=3)) for m in macros],FadeIn(label('depleted',-3,-2.15,32,RED)),FadeIn(label('Body-wide depletion',3.8,-.2,30)),run_time=.7)
        self.at('reduced hypersensitivity'); self.play(FadeIn(label('Hypersensitivity\nreduced in both sexes',3.8,-1.3,30,BLUE)),run_time=.5)
        self.at('The authors'); self.play(FadeIn(label('ganglion route favoured',-3,-3.5,30)),run_time=.4)
        self.at('but'); self.play(FadeIn(box('Skin dendritic cells\nalso depleted',3.7,-2.9,30)),run_time=.4); self.finish()

class S29Take(SpokenScene):
    def construct(self):
        qs=VGroup(*[box(s,0,y,44) for s,y in [('Which cell?',1.5),('In which sex?',-.1),('In which compartment?',-1.7)]])
        self.add(qs,head('Ask of any immune result'))
        for phrase,i in [('which cell',0),('in which sex',1),('in which compartment',2)]:
            self.at(phrase); self.play(qs[i].animate.set_color(TEAL),run_time=.25)
        self.finish()

class S30End(EndCard):
    LINE='Ask which cell, in which sex, in which compartment.'
