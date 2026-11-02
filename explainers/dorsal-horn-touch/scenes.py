"""Chapter 1: Two Routes, One Patch of Skin.
COLOR MAP: BLUE #58C4DD = direct afferent; GOLD #E4BF51 = PSDC/indirect.
PURPLE #B58CD9 = gracile nucleus; GREY = anatomy; TEXT = labels;
RED = negation. All anatomy is schematic. Response traces are illustrative
model outputs, never recordings: sinusoidal vibration with one spike/cycle;
constant-rate firing gated by a rectangular held press (no fitted parameters).
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
GOLD = '#E4BF51'
LESSON = 'Where Touch Is First Processed: Dorsal Horn and Dorsal Column Nuclei'

def poly(pts, color=GREY, w=4, opacity=1):
    return VMobject().set_points_as_corners([[x,y,0] for x,y in pts]).set_stroke(color,w,opacity=opacity).set_fill(opacity=0)
def label(s,x,y,color=TEXT,size=28):
    return T(s,size=size,color=color).move_to([x,y,0])
def lines(ss,x,y,color=TEXT,size=28):
    return VGroup(*[T(s,size=size,color=color) for s in ss]).arrange(DOWN,buff=.12).move_to([x,y,0])
def arr(a,b,color=GOLD,w=5):
    return Arrow([*a,0],[*b,0],buff=0,color=color,stroke_width=w,tip_length=.2)
def leader(a,b,color=GREY): return poly([a,b],color,2)
def cell(x,y,r=.3,color=GOLD):
    return Circle(radius=r,color=color,fill_color=color,fill_opacity=.24).move_to([x,y,0])
def paw(center=(-4.7,-2.5),scale=1):
    # Continuous, rounded silhouette: five toes above the broad plantar pad.
    pts=[(-.65,-.65),(-.85,-.15),(-.9,.35),(-.72,.65),(-.62,.4),(-.5,.95),(-.3,1.05),(-.25,.55),(-.12,1.17),(.08,1.17),(.18,.55),(.34,1.05),(.53,.95),(.5,.42),(.72,.74),(.87,.6),(.8,.15),(.65,-.4),(.25,-.75)]
    p=VMobject().set_points_smoothly([[x,y,0] for x,y in pts+[pts[0]]]).set_stroke(GREY,3).set_fill(GREY,.22)
    pad=Ellipse(width=.9,height=.72,color=GREY,fill_color=GREY,fill_opacity=.3).move_to([0,-.15,0])
    return VGroup(p,pad).scale(scale).move_to([*center,0])
def glow(x,y,r=.32):
    return VGroup(*[Circle(radius=r+k*.1,stroke_width=0,fill_color=BLUE,fill_opacity=.035*(5-k)).move_to([x,y,0]) for k in reversed(range(5))],cell(x,y,r,BLUE))

class Cord:
    def __init__(self, zoom=False):
        if not zoom:
            self.outer=Ellipse(width=7.3,height=6.3,color=GREY,fill_color=GREY,fill_opacity=.06).move_to([-1,0,0])
            pts=[(-1,.1),(-2,1.1),(-2.9,2.1),(-3.1,1.2),(-2.6,.25),(-3.4,-1.6),(-2.7,-2.1),(-1,-.55),(.7,-2.1),(1.4,-1.6),(.6,.25),(1.1,1.2),(.9,2.1),(0,1.1),(-1,.1)]
            self.grey=VMobject().set_points_smoothly([[x,y,0] for x,y in pts]).set_stroke(GREY,2).set_fill(GREY,.25)
            self.column=RoundedRectangle(width=1.4,height=1.2,corner_radius=.1,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([-.1,2.5,0])
            self.entry=poly([(5.8,.6),(2.6,.6),(1.1,1.6),(.2,1.5)],BLUE,6)
            self.up=poly([(.2,1.5),(.2,3)],BLUE,6)
            self.base=VGroup(self.outer,self.grey,self.column,DashedLine([-1,-3,0],[-1,3,0],color=GREY,stroke_opacity=.5))
            self.labels=VGroup(label('dorsal column',3.1,2.65,GREY),leader((1.6,2.65),(.6,2.65)),label('dorsal',-3.8,2.9,GREY,26),label('lumbar spinal cord',-1,-3.4,GREY,26))
            return
        # Isolated enlargement of the UPPER wing; ventral tissue is outside this view.
        pts=[(-4.6,-3.0),(-4.5,.7),(-3.8,2),(-3.1,2.55),(-2.5,1.55),(-1.1,.9),(.55,-.1),(.65,-3.0),(-4.6,-3.0)]
        horn=VMobject().set_points_smoothly([[x,y,0] for x,y in pts]).set_stroke(GREY,3).set_fill(GREY,.12)
        column=RoundedRectangle(width=1.8,height=2,corner_radius=.12,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([1,2.1,0])
        self.base=VGroup(horn,column)
        self.layers=VGroup(*[poly([(-4.2,y),(-3.3,y+.12),(-2.1,y+.12),(-.5,y-.12)],GREY,2,.6) for y in [1,.0,-1.05]])
        self.labels=VGroup(label('lumbar dorsal horn',-2.7,3.15,GREY,28),leader((-3,2.88),(-3.1,2.35)),label('dorsal column',3.8,2.7,GREY,28),leader((2.35,2.7),(1.8,2.7)),*[label(s,-4.9,y,GREY,26) for s,y in [('II',1.15),('III',.1),('IV',-1)]],label('enlarged dorsal wing · schematic',-2,-3.55,GREY,26))
        self.entry=poly([(5.7,1),(2.7,1),(1.45,1.3)],BLUE,6)
        self.up=poly([(1.45,1.3),(1.45,3.1)],BLUE,6)
        # A small bridge gap keeps the incoming blue fiber distinct from gold.
        self.entry_bridge=VGroup(poly([(5.7,1),(2.7,1),(1.88,1.197)],BLUE,6),poly([(1.62,1.259),(1.45,1.3)],BLUE,6))
        # Branch leaves to the LEFT of the two ascending axons; gold never crosses it.
        self.branch=poly([(1.45,1.3),(1.1,-.1),(-3.3,-.1)],BLUE,6)
        self.inter=VGroup(cell(-3,-1),cell(-2,-1.9))
        self.neuron=cell(-.15,-1.8,.43)
        self.links=VGroup(arr((-3,-.18),(-3,-.65)),arr((-2.75,-1.2),(-2.25,-1.65)),arr((-1.65,-1.9),(-.65,-1.8)))
        self.short=arr((-.7,-.12),(-.25,-1.3),w=3)
        self.axon=poly([(.28,-1.8),(1.75,-1.8),(1.75,3.1)],GOLD,6)
        self.interlabel=VGroup(lines(['local','interneurons'],-3,-2.6,GOLD,26),leader((-2.65,-2.2),(-2.25,-2.07),GOLD))
    def group(self,circuit=False):
        g=VGroup(self.base,self.layers,self.labels,self.entry_bridge if circuit else self.entry,self.up,self.branch)
        if circuit: g.add(self.inter,self.neuron,self.links,self.short,self.axon,self.interlabel)
        return g

class Routes:
    def __init__(self):
        self.paw=paw((-4.7,-2.25)); self.patch=glow(-4.7,-2.4,.25)
        self.column=RoundedRectangle(width=1.25,height=4.35,corner_radius=.1,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([.65,-.5,0])
        self.horn=RoundedRectangle(width=3.4,height=2.25,corner_radius=.25,color=GREY,fill_color=GREY,fill_opacity=.09).move_to([-1.95,-1.65,0])
        self.med=RoundedRectangle(width=4.9,height=1.4,corner_radius=.2,color=PURPLE,fill_color=PURPLE,fill_opacity=.10).move_to([.1,2.4,0])
        self.soma=cell(.65,2.25,.36,TEXT)
        self.blue=poly([(-4.4,-2.4),(-3.8,-3.05),(1,-3.05),(1,1.75),(.86,1.95)],BLUE,6)
        self.branch=poly([(-3,-3.05),(-3,-1.6),(-2.5,-1.6)],GOLD,5)
        self.local=VGroup(cell(-2.3,-1.6,.22),arr((-2.02,-1.6),(-1.18,-1.6)))
        self.psdc=cell(-.85,-1.6,.3)
        self.gold=poly([(-.55,-1.6),(.3,-1.6),(.3,1.7)],GOLD,6)
        self.end=poly([(.3,1.7),(.47,1.95)],GOLD,6)
        breaks=VGroup(*[poly([(x-.13,.4),(x+.06,.56),(x-.13,.72)],GREY,3) for x in [.03,1.27]])
        self.labels=VGroup(label('gracile nucleus',-.2,3.35,PURPLE,28),leader((-.2,3.1),(-.2,2.98),PURPLE),label('caudal medulla',-4.2,2.45,GREY,26),leader((-2.7,2.45),(-2.36,2.45)),label('dorsal column',3.2,.85,GREY,26),leader((1.8,.85),(1.28,.85)),label('long way up',3.1,.12,GREY,26),leader((1.8,.12),(1.28,.5)),label('dorsal horn',-2,-.22,GREY,26),leader((-2,-.48),(-2,-.57)),label('hindpaw',-4.7,-3.55,GREY,26))
        self.base=VGroup(self.horn,self.column,self.med,self.paw,self.patch,self.blue,breaks,self.soma,self.labels)
        self.indirect=VGroup(self.branch,self.local,self.psdc,self.gold)
    def all(self): return VGroup(self.base,self.indirect)

def prediction():
    r=Routes()
    other=cell(2,2.25,.32,GREY)
    opts=VGroup(DashedLine([.3,1.7,0],[.47,1.95,0],color=GOLD),DashedLine([.3,1.7,0],[1.8,1.99,0],color=GOLD))
    names=VGroup(lines(['same neuron','as blue'],-3.9,1.25,GOLD,26),leader((-2.6,1.4),(.3,2.1),GOLD),lines(['a separate','neuron'],4.45,2.4,GREY,26),leader((3.2,2.3),(2.35,2.25)))
    q=lines(['Does gold reach the','same brainstem neuron?'],3.9,-2.25,size=29)
    return VGroup(r.all(),other,opts,names,q)
def report_tags():
    return VGroup(VGroup(lines(['Direct,','keeps timing'],3.9,-.65,BLUE,28),leader((2.5,-.65),(1,-.65),BLUE)),VGroup(lines(['Rebuilt in the','dorsal horn,','sustained pressure'],3.8,-2.05,GOLD,26),leader((2.1,-2),(.3,-1.7),GOLD)))
def copy_mark():
    t=label('just a copy',-1.4,.7,GOLD,26)
    return VGroup(t,Line(t.get_left(),t.get_right(),color=RED,stroke_width=4),leader((t.get_right()[0]+.08,.7),(.3,.7),GOLD))
def summary():
    r=Routes(); return VGroup(r.all(),r.end,report_tags(),copy_mark())

class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='Two Routes, One Patch of Skin'
    def construct(self):
        g=VGroup(label('BIOCHEMISTRYPEDIA',0,2,TEAL,26),lines(['WHERE TOUCH IS FIRST PROCESSED:','DORSAL HORN AND DORSAL COLUMN NUCLEI'],0,.8,GREY,26),lines(['Two Routes,','One Patch of Skin'],0,-.8,size=48))
        self.add(g); self.finish()
class S01Question(SpokenScene):
    def construct(self):
        p=paw((-2.7,-.25),2.7); patch=glow(-2.7,-.9,.48)
        probe=RoundedRectangle(width=.42,height=1.7,corner_radius=.12,color=TEXT,fill_color=GREY,fill_opacity=1).move_to([-2.7,-.35,0])
        q=lines(['How does the news','reach the brainstem?'],2.9,2.1,size=33)
        self.add(p,probe,q,lines(['1 mm probe','schematic, not to scale'],3,-.25,GREY,26),label('mouse hindpaw',-2.7,-3.3,GREY))
        self.at('Press the skin'); self.play(probe.animate.shift(DOWN*.35),FadeIn(patch),run_time=.6)
        self.at('How does the news'); self.play(Indicate(q,scale_factor=1.03),run_time=.4)
        one=VGroup(arr((1,-1.5),(5.4,-1.5),BLUE),label('one route',3.2,-1.1,BLUE,28))
        self.at('The textbook draws'); self.play(FadeIn(one),run_time=.4)
        two=VGroup(arr((1,-1.5),(5.4,-1.5),BLUE),arr((1,-2.15),(5.4,-2.15),GOLD),label('two routes',3.2,-1.05,size=28))
        self.at('There are two',lead=.3); self.play(FadeOut(one),FadeIn(two),run_time=.3); self.finish()
class S02Textbook(SpokenScene):
    def construct(self):
        c=Cord(); self.add(c.base,c.labels,c.entry)
        self.at('A touch afferent'); self.play(FadeIn(lines(['touch afferent','Aβ low-threshold','mechanoreceptor'],4,-1.3,BLUE,26)),run_time=.35)
        self.at('enters the spinal cord'); self.play(Create(c.entry.copy()),run_time=.6)
        side=VGroup(lines(['same side','as the paw'],.75,-2.05,BLUE,28),leader((-.75,-1.8),(-1,-1.8),BLUE))
        self.at('Its main branch'); self.play(Create(c.up),FadeIn(side),run_time=.65)
        self.at('on the same side',lead=.4); self.play(Indicate(side[0],scale_factor=1.03),run_time=.25); self.finish()
class S03Direct(SpokenScene):
    def construct(self):
        r=Routes(); self.add(r.base)
        self.at('It reaches'); self.play(Create(r.blue.copy()),run_time=1)
        self.at('in the brainstem'); self.play(Indicate(r.med,scale_factor=1.02),run_time=.4)
        tag=VGroup(lines(['direct route','no synapse on the way'],3.9,-1.6,BLUE,26),leader((1.8,-1.3),(1,-1.3),BLUE))
        self.at('with no synapse'); self.play(FadeIn(tag),run_time=.35)
        self.at('Call this'); self.play(Indicate(tag[0],scale_factor=1.02),run_time=.4); self.finish()
class S04Below(SpokenScene):
    def construct(self):
        c=Cord(True); self.add(c.base,c.labels,c.layers,c.entry,c.up)
        self.at('Now look below'); self.play(Indicate(c.base[0],scale_factor=1.02),run_time=.4)
        self.at('also sends branches'); self.play(Create(c.branch),run_time=.6)
        self.at('a layered circuit'); self.play(Indicate(c.layers,scale_factor=1.03),run_time=.4); self.finish()
class S05Psdc(SpokenScene):
    def construct(self):
        c=Cord(True); self.add(c.group())
        self.at('Those branches drive'); self.play(FadeIn(c.inter),FadeIn(c.interlabel),GrowArrow(c.links[0]),run_time=.55)
        self.at('Through them'); self.play(GrowArrow(c.links[1]),GrowArrow(c.links[2]),FadeIn(c.neuron),run_time=.5)
        self.at('in places directly'); self.play(GrowArrow(c.short),run_time=.4)
        self.at('a spinal neuron'); self.play(Indicate(c.neuron),run_time=.4)
        self.at('whose own axon'); self.remove(c.entry); self.add(c.entry_bridge); self.play(Create(c.axon),run_time=.9); self.finish()
class S06Define(SpokenScene):
    def construct(self):
        c=Cord(True); self.add(c.group(True)); ring=Circle(radius=.57,color=GOLD).move_to(c.neuron)
        self.at('This is a'); self.play(Create(ring),run_time=.3)
        name=VGroup(lines(['postsynaptic dorsal','column (PSDC) neuron'],3.8,-.4,GOLD,26),leader((2,-.7),(.45,-1.65),GOLD))
        self.at('postsynaptic dorsal column'); self.play(FadeIn(name),run_time=.35)
        definition=lines(['PSDC = driven in','the dorsal horn;','axon up the','dorsal column'],3.8,-2.05,GOLD,26)
        self.at('It is driven'); self.play(FadeIn(definition),run_time=.35)
        self.at('projects to the brainstem',lead=.4); self.play(FadeIn(label('to brainstem',1.7,3.5,GOLD,26)),Indicate(c.axon,scale_factor=1),run_time=.3); self.finish()

def animal(mouse=False):
    # Smooth side-view silhouettes with species-specific ears, muzzle and tail.
    def filled(m):
        return m.set_stroke(width=0).set_fill(GREY,1)
    body=filled(Ellipse(width=3.1,height=1.6).move_to([-.5,0,0]))
    if mouse:
        head=filled(VMobject().set_points_smoothly([[.45,.5,0],[1.2,.6,0],[2,-.05,0],[1.45,-.45,0],[.5,-.5,0],[.45,.5,0]]))
        ears=VGroup(*[filled(Circle(radius=r).move_to([x,y,0])) for x,y,r in [(1,.73,.4),(.55,.72,.34)]])
        feet=VGroup(*[filled(Ellipse(width=.65,height=.2).move_to([x,-.72,0])) for x in [-1,.85]])
        tail=VMobject().set_points_smoothly([[-1.8,-.2,0],[-2.3,-.45,0],[-2.9,-.2,0],[-3.1,.3,0],[-2.9,.55,0]]).set_stroke(GREY,5)
        eye=Dot([1.35,.12,0],radius=.065,color=BG)
    else:
        head=filled(Circle(radius=.64).move_to([1,.64,0]))
        muzzle=filled(Ellipse(width=.6,height=.4).move_to([1.5,.4,0]))
        ears=VGroup(*[filled(Polygon([x-.28,1,0],[x-.2,1.72,0],[x+.3,1.12,0])) for x in [.6,1.25]])
        feet=VGroup(*[filled(RoundedRectangle(width=.36,height=1.15,corner_radius=.16).move_to([x,-.7,0])) for x in [-1.45,-.85,.65,1.12]])
        tail=VMobject().set_points_smoothly([[-1.8,0,0],[-2.4,.4,0],[-2.5,1.35,0],[-2.2,1.65,0],[-1.95,1.4,0]]).set_stroke(GREY,15)
        eye=Dot([1.24,.76,0],radius=.065,color=BG)
    return VGroup(tail,body,feet,ears,head,*([muzzle] if not mouse else []),eye).scale(1.1).move_to([-2.65,.05,0])
class S07Cats(SpokenScene):
    def construct(self):
        cat=animal(); title=label('Cat recordings',0,3,size=36); date=label('by the early 1980s',-2.5,-2.45,GREY,30)
        electrode=VGroup(poly([(1.5,1.6),(1.5,-1)],TEXT,4),lines(['electrode','recordings'],3.4,-1,TEXT,30),arr((2.2,.8),(1.55,.3),TEXT))
        self.add(cat,title,date,electrode)
        self.at('Recordings in cats'); self.play(Indicate(cat,scale_factor=1.02),run_time=.4)
        switches=VGroup(); knobs=[]; states=[]
        for y,s,col in [(1.5,'direct',BLUE),(.1,'indirect',GOLD)]:
            knob=cell(4.7,y,.19,col); state=label('ON',5.65,y,col,24)
            switches.add(label(s,3.4,y+.45,col,28),Line([2.1,y,0],[4.9,y,0],color=col,stroke_width=6),knob,state)
            knobs.append(knob); states.append(state)
        blue=poly([(1.7,-2),(2.2,-1.2),(5.8,-1.2)],BLUE,6)
        gold=poly([(1.7,-2),(2.4,-2.15),(3.2,-2.15),(3.2,-1.85),(5.8,-1.85)],GOLD,6)
        mini=VGroup(blue,gold,cell(3.2,-2.15,.16),cell(5.8,-1.52,.23,PURPLE))
        self.at('Mousework adds'); self.play(FadeOut(cat),FadeIn(animal(True)),FadeOut(electrode),FadeOut(date),FadeOut(title),FadeIn(label('Mouse studies',0,3,size=36)),FadeIn(switches),FadeIn(mini),run_time=.45)
        self.at('genetic access'); self.play(FadeIn(label('genetic access; test each route',0,-3.05,size=30)),run_time=.35)
        self.at('a test of each')
        off=label('OFF',5.65,1.5,GREY,24)
        self.play(knobs[0].animate.shift(LEFT*2.4),blue.animate.set_stroke(color=GREY,opacity=.3),FadeOut(states[0]),FadeIn(off),run_time=.4)
        # Reset the direct route before testing the indirect route.
        self.play(knobs[0].animate.shift(RIGHT*2.4),blue.animate.set_stroke(color=BLUE,opacity=1),FadeOut(off),FadeIn(states[0]),knobs[1].animate.shift(LEFT*2.4),gold.animate.set_stroke(color=GREY,opacity=.3),mini[2].animate.set_color(GREY).set_opacity(.3),FadeOut(states[1]),FadeIn(label('OFF',5.65,.1,GREY,24)),run_time=.4); self.finish()
class S08Gold(SpokenScene):
    def construct(self):
        r=Routes(); self.add(r.base)
        self.at('So draw a second line'); self.play(Create(r.branch),run_time=.7)
        self.at('in gold'); self.play(FadeIn(r.local[0]),run_time=.3)
        self.at('from the afferent'); self.play(GrowArrow(r.local[1]),FadeIn(r.psdc),run_time=.45)
        self.at('through the circuit'); self.play(Indicate(r.psdc,scale_factor=1.08),run_time=.25)
        self.at('and up to the',lead=.45); self.play(Succession(Create(r.gold,run_time=.8),Create(r.end,run_time=.2)),FadeIn(label('indirect route',3.8,-1.5,GOLD,28)),run_time=1); self.finish()
class S09Question(SpokenScene):
    def construct(self):
        p=prediction(); self.add(p)
        self.at('Pause and predict'); self.play(Indicate(p[2],scale_factor=1.02),run_time=.4)
        self.at('Does the gold line'); self.play(Indicate(p[4],scale_factor=1.02),run_time=.4); self.finish()
class S10Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(prediction()); self.wait(5)
class S11Reveal(SpokenScene):
    def construct(self):
        r=Routes(); self.add(r.all())
        self.at('For thalamus'); self.play(Create(r.end),run_time=.3)
        name=VGroup(lines(['thalamus-projecting','gracile neuron'],4.3,2.5,PURPLE,26),leader((2.55,2.45),(1.05,2.3),PURPLE))
        self.play(FadeIn(name),run_time=.35)
        self.at('yes'); self.play(Indicate(r.soma,color=GOLD),run_time=.4)
        inset=VGroup(RoundedRectangle(width=5.4,height=3.65,corner_radius=.2,color=GREY).move_to([4,-1.55,0]),paw((4,-1.35),1.45))
        blue=Circle(radius=.83,color=BLUE,stroke_width=5).move_to([3.85,-1.55,0]); gold=DashedVMobject(Circle(radius=.63,color=GOLD,stroke_width=5).move_to([4.08,-1.66,0]),num_dashes=16)
        self.at('highly aligned'); self.play(FadeOut(r.labels[6]),FadeOut(r.labels[7]),FadeOut(r.labels[4]),FadeOut(r.labels[5]),FadeIn(inset),Create(blue),Create(gold),run_time=.45)
        self.at('Both reported'); self.play(FadeIn(lines(['aligned receptive fields:','the same patch of skin'],4,-2.97,size=26)),run_time=.35); self.finish()

# Computed toy response model. Time is normalized: no measurement or frequency
# is implied. One phase-locked spike/cycle, and a constant-rate pressure response.
def response_row(y,col,vibration):
    xs=np.linspace(-4.6,5.2,1000); t=(xs+4.6)/9.8; gate=(t>=.1)&(t<=.9)
    stim=np.where(gate,.18*np.sin(2*np.pi*8*(t-.1)/.8) if vibration else .35,0)
    trace=poly(list(zip(xs,y-1+stim)),col,3)
    spiket=(.1+np.arange(8)*.8/8 if vibration else np.arange(.12,.9,.031))
    spikes=VGroup(*[Line([-4.6+9.8*v,y,0],[-4.6+9.8*v,y+.52,0],color=col,stroke_width=3) for v in spiket])
    axes=VGroup(arr((-4.6,y-.05),(5.6,y-.05),GREY,2),arr((-4.6,y-1.22),(5.6,y-1.22),GREY,2),label('time',5.65,y-.7,GREY,26),label('firing',-5.55,y+.2,col,26),label('stimulus',-5.55,y-1,col,26))
    return VGroup(axes,spikes,trace)
class S12Differ(SpokenScene):
    def construct(self):
        blue=response_row(1.85,BLUE,True); gold=response_row(-1.4,GOLD,False)
        self.add(label('Two different reports',0,3.45,size=34),label('illustrative model responses',0,-3.65,GREY,26),blue[0],gold[0])
        self.at('But the two reports'); self.play(FadeIn(blue[2]),FadeIn(gold[2]),run_time=.35)
        self.at('The direct route'); self.play(FadeIn(label('direct: vibration, precise timing',0,2.8,BLUE,28)),Create(blue[1]),run_time=.45)
        self.at('The indirect route'); self.play(FadeIn(lines(['indirect: sustained firing, up to high forces'],0,-.55,GOLD,28)),Create(gold[1]),run_time=.45); self.finish()
class S13Idea(SpokenScene):
    def construct(self):
        r=Routes(); tags=report_tags(); self.add(r.all(),r.end)
        self.at('That is the idea'); self.play(Indicate(r.patch),run_time=.35)
        self.at('One report keeps'); self.play(FadeIn(tags[0]),run_time=.3)
        self.at('The other is rebuilt'); self.play(FadeIn(tags[1]),run_time=.3)
        self.at('not copied'); self.play(FadeIn(copy_mark()),run_time=.3); self.finish()
class S14Hold(Scene):
    def construct(self): self.camera.background_color=BG; self.add(summary()); self.wait(3)
class S16Scope(SpokenScene):
    def construct(self):
        self.add(label('Scope of the evidence',0,3.15,size=36))
        cards=VGroup(*[VGroup(RoundedRectangle(width=11,height=1.6,corner_radius=.18,color=GREY,fill_color=GREY,fill_opacity=.1).move_to([0,y,0]),label(s,0,y,size=34)) for y,s in [(1.65,'mouse hindlimb'),(-.35,'mostly anaesthetized adults'),(-2.35,'dorsal column route only')]])
        self.at('these are mouse studies'); self.play(FadeIn(cards[0]),run_time=.25)
        self.at('mostly in'); self.play(FadeIn(cards[1]),run_time=.25)
        self.at('and the dorsal column'); self.play(FadeIn(cards[2]),run_time=.25); self.finish()
class S17Takeaway(SpokenScene):
    def construct(self):
        r=Routes(); self.add(r.all(),r.end)
        block=lines(['One touch, two routes,','two different reports','on the same skin.'],3.7,-1.8,size=31)
        self.at('The Takeaway'); self.play(FadeIn(block),run_time=.3)
        self.at('one touch'); self.play(Indicate(r.patch,scale_factor=1.2),run_time=.3)
        self.at('two roots'); self.play(Indicate(r.blue),Indicate(r.gold),run_time=.3); self.finish()
class S18End(EndCard):
    LINE='One touch, two routes, two different reports on the same skin.'
    def construct(self):
        self.add(lines(['One touch, two routes,','two different reports on the same skin.'],0,.3,size=36),label('biochemistrypedia.com',0,-1.35,TEAL,26)); self.finish()
