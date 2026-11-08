"""Computed teaching diagrams; all circuits and event rasters are schematic.
COLOR MAP: BLUE direct afferent; ORANGE indirect PSDC; GREEN excitation;
RED inhibition/high-threshold input; PURPLE gracile; YELLOW timing; GOLD synapses;
GREY anatomy. Models: t=L/v; sine=sin(2*pi*f*t); VS=exp(-.5*(2*pi*f*sigma)**2).
"""
import numpy as np
from bp_style import *
ORANGE='#F29E4C'
PURPLE='#B58CD9'
def p(x,y): return np.array([x,y,0.])
def label(s,x,y,size=28,color=TEXT): return T(s,size,color).move_to(p(x,y))
def head(s): return label(s,0,3.25,32)
def poly(pts,c,w=5): return VMobject().set_points_as_corners([p(*q) for q in pts]).set_stroke(c,w)
def arr(a,b,c=GREEN,w=5): return Arrow(p(*a),p(*b),buff=0,color=c,stroke_width=w,tip_length=.18)
def cell(x,y,c,r=.5): return Circle(radius=r,color=c,fill_color=c,fill_opacity=.22,stroke_width=4).move_to(p(x,y))
def inhib(a,b):
    a,b=p(*a),p(*b); d=(b-a)/np.linalg.norm(b-a); n=np.array([-d[1],d[0],0])*.18
    return VGroup(Line(a,b,color=RED,stroke_width=5),Line(b-n,b+n,color=RED,stroke_width=6))
def routes(tags=False):
    skin=Ellipse(width=8.8,height=1.2,color=GREY,fill_color=GREY,fill_opacity=.12).move_to(p(0,-2.65))
    patch=cell(0,-2.65,TEXT,.46)
    brain=chip('one gracile neuron',PURPLE,30).move_to(p(0,2.45))
    d=poly([(0,-2.19),(-4.9,-1.9),(-4.9,2.1),tuple(brain.get_left()[:2])],BLUE,7)
    i=poly([(0,-2.19),(4.9,-1.9),(4.9,2.1),tuple(brain.get_right()[:2])],ORANGE,7)
    relays=VGroup(cell(4.9,-1.1,ORANGE,.28),cell(4.9,.15,ORANGE,.28))
    g=VGroup(skin,patch,brain,d,i,relays,label('one patch of skin',0,-3.5,28))
    if tags: g.add(route_tags())
    return g

def route_tags(final=False):
    left=label('timing' if final else 'fast timing',-3.35,.7,30,BLUE)
    right=VGroup(label('sustained pressure',3.05,1.15,26,ORANGE),label('in mice',3.05,.65,26,ORANGE)) if final else VGroup(label('adds: sustained',3.05,1.15,26,ORANGE),label('pressure in mice',3.05,.65,26,ORANGE))
    g=VGroup(left,Line(p(-4.8,.7),p(left.get_left()[0]-.12,.7),color=BLUE),right,Line(p(right.get_right()[0]+.12,.9),p(4.8,.9),color=ORANGE))
    if final: g.add(label('rebuilt in cord',3.05,-.55,26,ORANGE),Line(p(4.45,-.55),p(4.8,-.55),color=ORANGE))
    return g
def wave(y=.6,period=1.4):
    return poly([(x,y+.9*np.sin(2*np.pi*(x+5.6)/period)) for x in np.linspace(-5.6,5.6,900)],YELLOW,3)
def spikes(ts,y,c=BLUE,scale=.7):
    return VGroup(*[Line(p(-5.6+scale*t,y),p(-5.6+scale*t,y+.6),color=c,stroke_width=4) for t in ts])
def predict():
    return VGroup(head('Where do a few milliseconds matter more?'),
        Rectangle(width=4.8,height=2.8,color=ORANGE,fill_opacity=.25).move_to(p(-3.2,.1)),
        poly([(x,1.4*np.sin(2*np.pi*2*(x-.8))) for x in np.linspace(.8,5.6,400)],YELLOW,4),
        label('long press',-3.2,-1.9,30,ORANGE),label('fast vibration',3.2,-1.9,30,YELLOW),
        label('Compare the lag with the duration of one event',0,-3.1,26))
def paw(x=0,y=0,scale=1):
    g=VGroup(Ellipse(width=2.8,height=3.6,color=GREY,fill_opacity=.1),
        *[Ellipse(width=.65,height=1.0,color=GREY).move_to(p(t,1.8)) for t in [-1.05,-.35,.35,1.05]])
    return g.scale(scale).move_to(p(x,y))
def field_question():
    return VGroup(head('Remove either kind of inhibition'),paw(0,.1,1.12),cell(0,-.15,ORANGE,.65),
        paw(-4.3,.1,1.12).set_opacity(.35),cell(-4.3,-.15,ORANGE,.32).set_opacity(.5),
        paw(4.3,.1,1.12).set_opacity(.35),cell(4.3,-.15,ORANGE,1.13).set_opacity(.5),
        label('shrink?',-4.3,-2.8,30),label('PSDC field',0,-2.8,28,ORANGE),label('grow?',4.3,-2.8,30))
def table():
    g=VGroup(head('Vector strength: 0 = none, 1 = perfect locking'),label('Toy model · assumed jitter: 0.20 ms / 0.73 ms',0,2.5,26))
    for s,x,c in [('Frequency',-4,TEXT),('Direct',0,BLUE),('Indirect',4,ORANGE)]: g.add(label(s,x,1.7,28,c))
    for f,y in [(50,.6),(300,-.5),(500,-1.6)]:
        vs=np.exp(-.5*(2*np.pi*f*np.array([.2,np.sqrt(.2**2+2*.5**2)])/1000)**2)
        g.add(label(f'{f} Hz',-4,y,32),label(f'{vs[0]:.2f}',0,y,36,BLUE),label(f'{vs[1]:.2f}',4,y,36,ORANGE))
    g.add(label('Most thalamus-projecting gracile neurons lock',0,-2.7,26),label('only below about 150 Hz',0,-3.2,26))
    return g

def motif(x,pre=False,complete=False):
    # A narrow axon swells into a vesicle-filled synaptic bouton.
    bouton=VMobject(color=BLUE,fill_color=BLUE,fill_opacity=.3,stroke_width=5)
    bouton.start_new_path(p(x-2.65,1.25))
    bouton.add_line_to(p(x-1.95,1.25))
    bouton.add_cubic_bezier_curve_to(p(x-1.55,2.0),p(x-.48,1.85),p(x-.48,1.0))
    bouton.add_cubic_bezier_curve_to(p(x-.48,.15),p(x-1.55,0),p(x-1.95,.75))
    bouton.add_line_to(p(x-2.65,.75)); bouton.close_path()
    a=VGroup(bouton,*[cell(x+dx,y,BLUE,.085) for dx,y in [(-1.35,.7),(-1.05,1),(-1.4,1.3),(-.85,.65)]])
    out=cell(x+1.5,1,ORANGE,.96)
    ex=arr((x-.4,1),(x+.5,1),GREEN,8 if pre else 5)
    it=cell(x-.7,-1.35,RED if complete else GREY,.88)
    labs=VGroup(label('afferent bouton',x-1.35,2.15,26,BLUE),label('PSDC',x+1.5,2.25,28,ORANGE))
    if pre:
        connection=inhib((x-.9,-.5),(x-1.22,.27))
        connection[1].set_stroke(width=9).scale(1.35)
        extra=VGroup(label('PVi sources',x-.7,-2.55,26,RED),label('GABA-A dependent',x,-3.2,26,RED))
    else:
        connection=VGroup(arr((x-1.6,.3),(x-1.15,-.58)),inhib((x+.16,-1.15),(x+1.22,.08)))
        extra=VGroup(label('Rorβ interneuron',x-.7,-2.55,26,RED),label('glycinergic',x-.7,-3.2,26,RED))
    return VGroup(a,out,ex,it,labs,connection,extra)
def panels():
    return VGroup(head('Two kinds of inhibition shape output'),Line(p(0,-3.4),p(0,2.7),color=GREY,stroke_width=1),label('Feedforward',-3.25,2.65,28),label('Presynaptic',3.25,2.65,28))

class S00Title(TitleCard):
    TITLE='Why Later Is Fine, and What the Cord Does'
    LESSON='Where Touch Is First Processed: Dorsal Horn and Dorsal Column Nuclei'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.8,26,TEAL),label('Where Touch Is First Processed',0,1.8,28),label('Dorsal Horn and Dorsal Column Nuclei',0,1.2,26))
        title=VGroup(T('Why Later Is Fine,',44,font=TITLE_FONT),T('and What the Cord Does',44,font=TITLE_FONT)).arrange(DOWN,buff=.25).move_to(p(0,-.5))
        self.play(FadeIn(title),run_time=.6); self.finish()
class S01Question(SpokenScene):
    def construct(self):
        g=routes(); self.add(g,head('Simple model: why arrive later?'))
        self.at('In a simple model')
        # Two visible spike fronts per route; direct arrivals precede both relay arrivals.
        fronts=VGroup()
        for path,c,duration in [(g[3],BLUE,1.55),(g[4],ORANGE,2.8)]:
            for delay in [0,.55]:
                spike=VGroup(Dot(radius=.17,color=c),poly([(-.2,-.2),(0,.16),(.2,-.2)],TEXT,4)).move_to(path.get_start())
                fronts.add(spike)
        self.add(fronts)
        animations=[]
        for n,spike in enumerate(fronts):
            path=g[3] if n<2 else g[4]; duration=1.55 if n<2 else 2.8; delay=.55*(n%2)
            animations.append(UpdateFromAlphaFunc(spike,lambda m,t,path=path,duration=duration,delay=delay:m.move_to(path.point_from_proportion(np.clip((3.4*t-delay)/duration,0,1)))))
        self.play(*animations,run_time=3.4,rate_func=linear)
        self.at('What does a slower report')
        self.play(FadeOut(fronts),Transform(g[6],label('What does it cost — and add?',0,-3.5,30)),run_time=.4); self.finish()
class S02Sum(SpokenScene):
    def construct(self):
        self.add(head('Illustrative numbers · mouse hindpaw'),label('Common scale: arrival time (ms)',0,-3.2,26))
        x=lambda t:-5.4+t*1.08
        self.add(Line(p(x(0),-2.4),p(x(10),-2.4),color=GREY))
        for t in [0,2.5,5,7.5,10]: self.add(Line(p(x(t),-2.3),p(x(t),-2.5),color=GREY),label(str(t),x(t),-2.8,26))
        self.at('Take illustrative numbers')
        d=Rectangle(width=5*1.08,height=.8,color=BLUE,fill_opacity=.4).move_to(p(x(2.5),1.3))
        self.play(GrowFromEdge(d,LEFT),FadeIn(label('Direct: 0.08 m / 16 m/s = 5.0 ms',0,2.35,28,BLUE)),run_time=.7)
        self.at('In this model')
        for start,dur,c in [(0,2.5,BLUE),(2.5,2,GOLD),(4.5,5,ORANGE)]:
            box=Rectangle(width=dur*1.08,height=.85,color=c,fill_opacity=.3).move_to(p(x(start+dur/2),-.25))
            self.play(GrowFromEdge(box,LEFT),FadeIn(label(f'{dur:.1f}',x(start+dur/2),-.25,28)),run_time=.3)
        self.add(label('to cord',x(1.25),-1,26),label('synapses',x(3.5),-1,26),label('PSDC axon',x(7),-1,26,ORANGE))
        self.at('input arrives')
        self.play(Create(DoubleArrow(p(x(5),-1.7),p(x(9.5),-1.7),buff=0,color=YELLOW)),FadeIn(label('4.5 ms later',x(7.25),-2.02,28,YELLOW)),FadeIn(label('Indirect total: 9.5 ms',2,.65,28,ORANGE)),run_time=.5); self.finish()
class S03Sign(SpokenScene):
    def construct(self):
        self.add(head('Model, not a measurement'),label('Illustrative model range · not measured uncertainty',0,2.55,26))
        x=lambda t:-5.4+(t-.5)*10.8/11.2
        bar=Rectangle(width=10.8,height=.55,color=YELLOW,fill_opacity=.22).move_to(p(0,1.7))
        self.add(bar,label('0.5 ms',-5.1,1,26),label('11.7 ms',5,1,26))
        mark=VGroup(Line(p(x(4.5),1.4),p(x(4.5),2.05),color=TEXT,stroke_width=5),label('4.5 ms',x(4.5),2.25,28))
        self.add(mark)
        # Same two-route anatomy, present from the opening frame.
        g=routes(); g[6].set_opacity(0); g[2].set_opacity(0); g.scale(.6).move_to(p(-3.6,-1.25)); self.add(g)
        self.at('and its size is uncertain'); self.play(Indicate(bar),run_time=.6)
        self.at('With equal paths'); self.play(FadeIn(label('Equal cord-to-brainstem paths',2.2,-.2,26)),run_time=.35)
        self.at('matched final synapses'); self.play(FadeIn(label('Matched final synapses',2.2,-.9,26)),FadeIn(label('PSDC axon no faster',2.2,-1.6,26)),run_time=.4)
        self.at('the spinal synapses'); self.play(Create(Line(g[5][0].get_center(),g[5][1].get_center(),color=YELLOW,stroke_width=8)),g[5].animate.set_color(YELLOW).set_stroke(width=8),FadeIn(label('Extra spinal synapses → later',2.2,-2.6,26,ORANGE)),run_time=.5); self.finish()
class S04Question(SpokenScene):
    def construct(self):
        g=predict(); self.add(g); self.at('Pause and predict'); self.play(Indicate(g[0]),run_time=.4)
        self.at('a long press'); self.play(Indicate(g[1]),run_time=.5)
        self.at('for fast vibration'); self.play(Indicate(g[2]),run_time=.5); self.finish()
class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(predict())
        for i in range(5,0,-1):
            t=label(str(i),0,2.5,28,YELLOW); self.add(t); self.wait(1); self.remove(t)
class S06Press(SpokenScene):
    def construct(self):
        bar=Rectangle(width=11.2,height=3.5,color=ORANGE,fill_opacity=.2).move_to(p(0,.1))
        self.add(head('A 300 ms press'),bar,label('steady firing during the press',0,.5,32,ORANGE),label('0 ms',-5.3,-2.1,26),label('300 ms',5.1,-2.1,26))
        self.at('For the steady firing'); self.play(Indicate(bar),run_time=.5)
        self.at('The lag is a sliver')
        x=-5.6+11.2*4.5/600
        sl=Rectangle(width=11.2*4.5/300,height=3.5,color=YELLOW,fill_opacity=.9).move_to(p(x,.1))
        self.play(FadeIn(sl),Create(poly([(x,-1.65),(-4,-2.65),(-2.8,-2.65)],YELLOW,2)),FadeIn(label('4.5 ms = 1.5% of 300 ms',.8,-2.65,30,YELLOW)),run_time=.5)
        self.at('though onset timing'); self.play(FadeIn(label('Onset timing is a separate question',0,-3.35,26)),run_time=.35); self.finish()
class S07Vib(SpokenScene):
    def construct(self):
        self.add(head('500 Hz vibration'),wave(.1)); self.at('one cycle lasts')
        self.play(Create(DoubleArrow(p(-5.6,-1.5),p(-4.2,-1.5),buff=0,color=YELLOW)),FadeIn(label('2.0 ms per cycle',-3.7,-2.25,30,YELLOW)),run_time=.5)
        self.at('The lag spans')
        shade=Rectangle(width=1.4*4.5/2,height=2.6,color=YELLOW,fill_opacity=.15).move_to(p(-5.6+1.4*4.5/4,.1))
        self.play(FadeIn(shade),FadeIn(label('4.5 ms = 2.25 cycles',1.8,2,30,YELLOW)),run_time=.5); self.finish()
class S08Fixed(SpokenScene):
    def construct(self):
        self.add(head('Fixed delay: locking kept'),wave(.7))
        # Eight periodic events; observation window crops arrivals outside 0..16 ms.
        ts=np.arange(0,16,2); reference=spikes(ts,-.9,BLUE).set_opacity(.45); row=spikes(ts,-2,ORANGE)
        self.add(reference,row,label('original',-4.4,-1.12,26,BLUE),label('delayed',-4.4,-2.5,26,ORANGE))
        reference_mark=DashedLine(p(-2.8,1.9),p(-2.8,-2.1),color=BLUE); self.add(reference_mark)
        self.at('Every spike is equally late')
        # A moving observation window preserves eight cycles while discarding two whole cycles.
        self.add(label('4.5 ms = 2 cycles + ¼ cycle',0,2.25,28,YELLOW),label('¼ cycle = 90° phase change',1.3,-2.6,28,YELLOW))
        self.play(UpdateFromAlphaFunc(row,lambda m,a:m.become(spikes((ts+4.5*a)%16,-2,ORANGE))),run_time=1.2,rate_func=linear)
        self.remove(row); row=spikes(ts+.5,-2,ORANGE); self.add(row)
        self.add(label('Periodic view: discard 2 whole cycles',0,-3.3,26))
        self.at('so the spikes still share'); self.play(Indicate(row),run_time=.5)
        self.at('That phase shifts')
        self.play(Indicate(reference_mark),Create(DashedLine(p(-2.45,1.9),p(-2.45,-2.1),color=ORANGE)),Create(DoubleArrow(p(-2.8,-2.7),p(-2.45,-2.7),buff=0,color=YELLOW,tip_length=.08)),Indicate(row),run_time=.5); self.finish()
class S09Jitter(SpokenScene):
    def construct(self):
        # 100 Hz view: 0.5 ms is 5% of a cycle, preserving the true jitter scale.
        self.add(head('Jitter spreads spike timing'),wave(.7),label('100 Hz view · 10 ms per cycle',0,2.45,26,YELLOW))
        base=np.arange(5,80,10); row=spikes(base,-1.35,ORANGE,scale=.14); self.add(row)
        rng=np.random.default_rng(15); noise=rng.normal(0,.5,(2,len(base)))
        self.at('In this toy model'); self.add(label('Independent Gaussian jitter: 0.5 ms / synapse',0,-3.2,26))
        self.at('each synapse adds')
        s1=VGroup(cell(-3.5,-2.3,GOLD,.23),label('synapse 1',-1.9,-2.3,26,GOLD))
        self.play(Transform(row,spikes(base+noise[0],-1.35,ORANGE,scale=.14)),FadeIn(s1),run_time=.6)
        self.at('when the next spike')
        s2=VGroup(cell(1,-2.3,GOLD,.23),label('synapse 2',2.6,-2.3,26,GOLD))
        self.play(Transform(row,spikes(base+noise.sum(axis=0),-1.35,ORANGE,scale=.14)),FadeIn(s2),run_time=.6); self.finish()
class S10Model(SpokenScene):
    def construct(self):
        self.add(table()); self.at('two synapses')
        box=Rectangle(width=11,height=.8,color=ORANGE).move_to(p(0,-1.6)); self.play(Create(box),run_time=.4)
        self.at('locking barely changes',lead=1.3); self.play(box.animate.move_to(p(0,.6)).set_color(YELLOW),run_time=.5); self.finish()
class S11Payoff(SpokenScene):
    def construct(self):
        old=table(); self.add(old); self.at('That model is not')
        self.play(FadeOut(old),run_time=.25)
        stamp=chip('A model, not a measurement',YELLOW,32); self.play(FadeIn(stamp),run_time=.35)
        self.at('But it shows'); self.play(FadeOut(stamp),FadeIn(routes()),FadeIn(head('Two routes, different contributions')),run_time=.5)
        self.at('why fast timing'); self.play(FadeIn(route_tags()),run_time=.4); self.finish()
class S12Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(routes(True),head('Two routes, different contributions')); self.wait(3)
class S13Rebuilt(SpokenScene):
    def construct(self):
        box=RoundedRectangle(width=12,height=5.7,corner_radius=.3,color=GREY).move_to(p(0,-.25))
        ps=cell(3.8,.1,ORANGE,.9); a=cell(-4.7,1.4,BLUE,.5)
        self.add(head('What does the cord do?'),box,ps,a,label('afferent',-4.7,2.3,28,BLUE),label('PSDC',3.8,1.5,30,ORANGE),label('lumbar dorsal horn',0,-3.45,28))
        local=VGroup(*[cell(-1.2,y,GREEN,.48) for y in [1.35,-.15,-1.65]])
        direct=VGroup(poly([(-4.7,.9),(-4.7,-2.2),(1.9,-2.2)],BLUE,2),arr((1.9,-2.2),(3,-.4),BLUE,2))
        inputs=VGroup(*[arr((-.7,y),(2.8,.1),GREEN,7) for y in [1.35,-.15,-1.65]])
        self.add(local,direct,inputs,label('local interneurons',-1.1,-2.65,28,GREEN))
        self.at('What does the cord'); self.play(Indicate(box),run_time=.4)
        self.at('neurons get most'); self.play(Indicate(inputs),FadeIn(label('most excitation',.7,2.2,26,GREEN)),run_time=.6)
        self.at('from local interneurons'); self.play(Indicate(local),run_time=.5); self.finish()
class S14Converge(SpokenScene):
    def construct(self):
        ps=cell(2.9,.45,TEXT,1.65)
        low=arr((-5.5,1.7),(1.24,.9),BLUE,9)
        high=arr((-5.5,-1.25),(1.24,-.05),RED,9)
        self.add(head('Inputs converge in the dorsal horn'),ps,low,high,label('one dorsal horn neuron',2.9,-1.65,26),label('Chirila et al., 2022 · anaesthetized adult mice',0,-3.45,26))
        self.at('received input from both'); self.play(Indicate(VGroup(low,high)),run_time=.4)
        self.at('low threshold'); self.play(Indicate(low),FadeIn(label('low-threshold input',-3.5,2.3,28,BLUE)),run_time=.4)
        self.at('and high threshold'); self.play(Indicate(high),FadeIn(label('high-threshold input',-3.5,-1.85,28,RED)),run_time=.5)
        self.play(FadeIn(label('Rebuilt, not passed on',0,-2.65,30)),run_time=.4); self.finish()
class S15Ff(SpokenScene):
    def construct(self):
        g=motif(-3.25); r=motif(3.25,True,True)
        self.add(panels(),g[0],g[1],g[4],r)
        self.at('the afferent excites'); self.play(GrowArrow(g[2]),run_time=.5)
        self.at('and an inhibitory interneuron'); self.play(FadeIn(g[3]),GrowArrow(g[5][0]),FadeIn(label('interneuron',-3.95,-2.55,26)),run_time=.5); self.finish()
class S16Ff2(SpokenScene):
    def construct(self):
        g=motif(-3.25); r=motif(3.25,True,True)
        generic=label('interneuron',-3.95,-2.55,26)
        self.add(panels(),g[0],g[1],g[2],g[3],g[4],g[5][0],generic,r)
        self.at('then inhibits'); self.play(Create(g[5][1]),g[3].animate.set_color(RED),run_time=.5)
        self.at('Here'); self.play(ReplacementTransform(generic,g[6][0]),run_time=.4)
        self.at('using glycine'); self.play(FadeIn(g[6][1]),run_time=.35); self.finish()
class S17Pre(SpokenScene):
    def construct(self):
        left=motif(-3.25,complete=True); g=motif(3.25,True,True)
        self.add(panels(),left,g)
        self.at('Presynaptic inhibition'); self.play(Indicate(g[3]),run_time=.4)
        self.at('lands on'); self.play(Indicate(g[5]),run_time=.5)
        self.at('and scales down'); self.play(g[2].animate.set_stroke(width=2),FadeIn(label('less transmitter',4.6,-.15,26,GREEN)),run_time=.6); self.finish()
class S18Question(SpokenScene):
    def construct(self):
        g=field_question(); self.add(g[1],g[2],g[8]); title=head('Pause and predict'); self.add(title)
        self.at('Remove either kind'); self.play(ReplacementTransform(title,g[0]),run_time=.3)
        self.at('receptive field'); self.play(*[FadeIn(g[i]) for i in [3,4,5,6,7,9]],run_time=.4); self.finish()
class S19Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(field_question()); self.wait(5)
class S20Reveal(SpokenScene):
    def construct(self):
        skin=paw(-4.6,.1,1.0); disc=cell(-4.6,-.1,ORANGE,.6)
        self.add(label('Without inhibition',-4.5,3.2,28),skin,disc,label('PSDC field grows',-4.5,-2.7,26,ORANGE))
        self.at('It grows'); self.play(disc.animate.scale(1.8),run_time=.65)
        self.at('And losing presynaptic inhibition')
        self.add(label('Without presynaptic inhibition',2.05,3.2,28),label('SCHEMATIC · firing events',2.05,2.65,26,YELLOW))
        x=lambda t:-.7+1.05*t
        step=poly([(x(0),1.5),(x(0),2),(x(3),2),(x(3),1.5),(x(6),1.5)],GREY,3)
        self.add(step,label('indentation',.75,1.6,26),label('with inhibition',1,.9,26,BLUE),label('without presynaptic inhibition',2,-.75,26,ORANGE))
        # Deterministic schematic generator: baseline events during input, decay after release.
        during=np.arange(.2,3,.45); after=[]; t=3.15
        while t<6: after.append(t); t+=.3+.18*(t-3)
        def raster(ts,y,c): return VGroup(*[Line(p(x(t),y),p(x(t),y+.5),color=c,stroke_width=4) for t in ts])
        self.add(raster(during,.05,BLUE),raster(during,-1.55,ORANGE))
        self.at('left neurons firing')
        self.add(DashedLine(p(x(3),2.05),p(x(3),-2.2),color=GREY),label('stimulus end',x(3),-3.3,26),label('after-discharge',3.8,-2.2,26,ORANGE))
        self.play(Create(raster(after,-1.55,ORANGE)),run_time=.6)
        self.at('after the indentation ended'); self.play(Indicate(step),run_time=.4)
        self.add(arr((x(0),-2.8),(x(6),-2.8),TEXT,2),label('time →',5.1,-3.3,26)); self.finish()
class S21Caveat(SpokenScene):
    def construct(self):
        self.add(head('Limits of the evidence'),label('Chronic conditional knockouts',0,2.15,30))
        self.at('recorded under'); self.play(FadeIn(label('Anaesthetized recordings',0,1.4,30)),run_time=.4)
        self.at('And no study here')
        self.add(cell(-3.8,-.7,PURPLE,.8),cell(3.8,-.7,ORANGE,.8),label('?',-3.8,-.7,44),label('?',3.8,-.7,44),label('gracile neuron',-3.8,-2,28,PURPLE),label('PSDC neuron',3.8,-2,28,ORANGE))
        mouse=VGroup(Ellipse(width=2.5,height=1.15,color=TEXT,fill_opacity=.18).move_to(p(0,-.7)),cell(1.25,-.4,TEXT,.42),Circle(radius=.25,color=TEXT).move_to(p(1.1,.05)),Dot(p(1.48,-.31),radius=.06,color=TEXT),poly([(-1.25,-.7),(-1.8,-1),(-2.1,-.6)],TEXT,3),Line(p(-.5,-1.1),p(-.6,-1.5),color=TEXT),Line(p(.6,-1.1),p(.7,-1.5),color=TEXT))
        self.play(FadeIn(mouse),FadeIn(label('Open question: never recorded awake here',0,-3.15,30,YELLOW)),run_time=.4)
        self.at('in an awake animal'); self.play(Indicate(mouse),run_time=.4); self.finish()
class S22Takeaway(SpokenScene):
    def construct(self):
        tags=route_tags(final=True)
        self.add(routes(),head('Two routes, one patch of skin'),tags)
        self.at('One keeps the timing'); self.play(Indicate(tags[0]),run_time=.4)
        self.at('The other'); self.play(Indicate(tags[2]),run_time=.4)
        self.at('rebuilt in the cord'); self.play(Indicate(tags[4]),run_time=.4)
        self.at('reports the pressure'); self.play(Indicate(tags[2]),run_time=.4); self.finish()
class S23End(EndCard):
    LINE='In mice: one keeps timing; the other reports sustained pressure.'
    def construct(self):
        self.add(routes(),route_tags(final=True),head('Two routes, one patch of skin'))
        self.add(label('biochemistrypedia.com',0,-1.5,24,TEAL)); self.finish()
