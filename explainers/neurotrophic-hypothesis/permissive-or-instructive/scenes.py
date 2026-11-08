"""Chapter 6: spatial delivery separates survival from innervation.
COLOR MAP: BLUE neurons/axons; GREEN survival; RED deletion/death;
YELLOW NGF; TEAL number made/ceiling; PURPLE TrkA; GREY tissue.
SAGE / CLAY are abstract cell fates, used only in the tile experiment.
All fibre drawings are qualitative schematics, never quantitative traces.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
SAGE, CLAY = '#9DB9A6', '#C38F78'

def label(s,x,y,size=30,color=TEXT):
    return T(s,size,color).move_to([x,y,0])
def head(s,color=TEXT):
    return T(s,34,color,font=TITLE_FONT).move_to([0,3.1,0])
def foot(s,color=TEXT,y=-3.1):
    return label(s,0,y,28,color)
def dot(p,color=BLUE,r=.22):
    return Circle(radius=r,color=color,fill_color=color,fill_opacity=.85).move_to(p)
def source(p):
    return dot(p,YELLOW,.16)
def panel(x=0,w=12,h=5.3):
    return RoundedRectangle(width=w,height=h,corner_radius=.25,color=GREY,fill_color=GREY,fill_opacity=.09).move_to([x,0,0])
def branch(a,b):
    return Line(a,b,color=BLUE,stroke_width=5)
def neuron(y=0):
    return dot([-5.4,y,0],r=.33)
def fuel():
    box=RoundedRectangle(width=1.65,height=2.1,corner_radius=.16,color=GREY,fill_color=GREY,fill_opacity=.18)
    return VGroup(box,Rectangle(width=.7,height=.35,color=GREY).next_to(box,UP,buff=0),Line(box.get_corner(UR),box.get_corner(UR)+[.5,.35,0],color=GREY,stroke_width=10))
def wheel():
    return VGroup(Circle(radius=1.1,color=GREY,stroke_width=7),*[Line(ORIGIN,1.1*np.array([np.cos(a),np.sin(a),0]),color=GREY,stroke_width=6) for a in [PI/2,7*PI/6,11*PI/6]],dot(ORIGIN,GREY,.18))

# Enlarged target cutaway: axon entry is at the left edge of a large islet.
ENTRY=np.array([-1.6,0,0])
def arbor(dense=False):
    ends=[(1.5,1.85),(2.7,1.65),(3.6,1.1),(4,.5),(4,-.5),(3.6,-1.1),(2.7,-1.65),(1.5,-1.85)] if dense else [(2.3,.9),(2.3,-.9)]
    return VGroup(*[branch(ENTRY,[x,y,0]) for x,y in ends])
def local_arbor():
    ends=[(1.5,1.85),(2.0,1.7),(2.5,1.55),(3,1.35),(3.4,1.1),(3.7,.85),(3.9,.6),(4,.35)]
    return VGroup(*[branch(ENTRY,[x,y,0]) for x,y in ends])
def wiring(axons=True,sparse=True,local=False):
    body=neuron(); tissue=panel(1.45,9.4,5.5)
    isle=Ellipse(width=6.3,height=5,color=YELLOW if local else GREY,fill_color=YELLOW if local else GREY,fill_opacity=.07).move_to([1.45,0,0])
    ax=branch([-5.05,0,0],ENTRY) if axons else VGroup()
    tw=arbor(not sparse) if axons else VGroup()
    dots=VGroup(source([-5.4,0,0]),source([-4.3,0,0]),source([-3.35,0,0]),source([3.2,0,0]))
    tags=VGroup(label('neuron',-5.35,.8,28),label('target tissue',-1.8,2.4,28),label('islet',4.95,-2.05,28),label('NGF',-4.5,-.65,28,YELLOW))
    return VGroup(body,tissue,dots,ax,tw,isle,tags)
def density_tag(dense=False):
    return chip('Dense' if dense else 'Sparse',BLUE,30).move_to([-4.8,-1.35,0])

# Every baseline stub has the same length, including those below islets.
ISLETS=[[-3.5,.75,0],[0,.75,0],[3.5,.75,0]]
def fan(p,dense=True):
    x,y,_=p
    ends=[(-.85,.3),(-.65,.8),(-.25,1),(.25,1),(.65,.8),(.85,.3),(-.65,-.1),(.65,-.1)] if dense else [(-.45,.4),(.45,.4)]
    return VGroup(*[branch([x,y-.7,0],[x+dx,y+dy,0]) for dx,dy in ends])
def pancreas(dense=False):
    tissue=panel(0,12.1,5.3)
    cells=VGroup(*[VGroup(*[dot(np.array(p)+[dx,dy,0],GREY,.29) for dx,dy in [(-.3,0),(.24,.27),(.24,-.3)]]) for p in ISLETS])
    glows=VGroup(*[Circle(radius=1.15,color=YELLOW,fill_color=YELLOW,fill_opacity=.08).move_to(p) for p in ISLETS])
    base=VGroup(branch([-5.65,-1.35,0],[5.65,-1.35,0]),*[branch([x,-1.35,0],[x,-1.05,0]) for x in np.linspace(-5.5,5.5,23)])
    fibres=VGroup(*[VGroup(branch([p[0],-1.05,0],[p[0],p[1]-.7,0]),fan(p)) for p in ISLETS]) if dense else VGroup()
    return VGroup(tissue,cells,glows,base,fibres)
def options():
    return VGroup(*[chip(t,TEXT,28,fill_opacity=.08) for t in ['Islets only','Everywhere','Nowhere in particular']]).arrange(RIGHT,buff=.5).move_to([0,-3.15,0])
def question():
    return VGroup(pancreas(),head('Where do the sympathetic fibres go?'),label('NGF-making islets',0,2.25,28,YELLOW),options())
RV=.25   # reveal scenes lift the pancreas so the legend sits below its panel
def reveal_pancreas(dense=False):
    p=pancreas(dense); p[0].stretch_to_fit_height(4.8).move_to([0,.25,0])
    return p.shift(UP*RV)
def surround_tag():
    return label('surrounding tissue: no matching rise',0,-1.75+RV,28)
def comparison():
    def icon(c,dense):
        f=fan([0,0,0],dense).scale(.62 if not dense else .5)
        if not dense: f.add(branch([0,-.7*.62-.22,0],[0,-.7*.62,0]))
        return VGroup(Circle(radius=.5,color=c,stroke_width=4),f.move_to([0,-.03,0]))
    a=icon(GREY,False).move_to([-4.4,-2.9,0]); b=icon(YELLOW,True).move_to([.6,-2.9,0])
    return VGroup(a,b,label('Normal islet',-2.7,-2.9,28),label('NGF-made islet',2.9,-2.9,28))
def reveal():
    p=reveal_pancreas(True)
    return VGroup(p,head('Pattern followed the delivery → instructive here',YELLOW),surround_tag(),comparison())

def tiles(y=0,moved=False):
    colors=([CLAY]*6+[SAGE]*2) if moved else ([SAGE]*4+[CLAY]*4)
    return VGroup(*[Rectangle(width=1.12,height=.82,color=BG,stroke_width=3,fill_color=c,fill_opacity=1).move_to([(i-3.5)*1.17+.8,y,0]) for i,c in enumerate(colors)])
def delivery(y,uniform=False,moved=False):
    return VGroup(*[source([(i-3.5)*1.17+.8,y,0]) for i in (range(8) if uniform else range(6,8) if moved else range(4))])
def legend():
    return VGroup(source([-4.8,2.4,0]),label('signal',-4,2.4,26),dot([-.8,2.4,0],SAGE,.16),label('fate A',0,2.4,26),dot([3.2,2.4,0],CLAY,.16),label('fate B',4,2.4,26))

class S00Title(TitleCard):
    TITLE='Permissive or Instructive'
    LESSON='The Neurotrophic Hypothesis Tested'
    def construct(self):
        brand=T('BIOCHEMISTRYPEDIA',22,TEAL)
        lesson=T(self.LESSON.upper(),22,GREY)
        title=T(self.TITLE,50,font=TITLE_FONT)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        group=VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.35)
        self.play(FadeIn(group),run_time=.6)
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        body=neuron(); target=panel(2.2,7.3,5.3); ax=branch([-5.05,0,0],[-1,0,0])
        self.add(head('Does NGF choose where axons go?'),body,target,source([3,1,0]),label('NGF',3,1.65,30,YELLOW),label('target tissue',2,-1.9,30))
        self.at('keeps neurons alive'); self.play(body.animate.set_color(GREEN),Create(ax),run_time=.7)
        self.at('Does it also'); self.play(FadeIn(label('?',-.75,0,60,YELLOW)),run_time=.4)
        self.finish()
class S02Defs(SpokenScene):
    def construct(self):
        a=VGroup(panel(-3.15,5.8,5.6),label('Permissive',-3.15,1.6,40),label('Allows what\nsomething else\nchooses',-3.15,-.25,34))
        b=VGroup(panel(3.15,5.8,5.6),label('Instructive',3.15,1.6,40),label('Chooses the\noutcome itself',3.15,-.25,34))
        self.add(a)
        self.at('An instructive signal'); self.play(FadeIn(b),run_time=.6)
        self.finish()
class S03Fuel(SpokenScene):
    def construct(self):
        f=fuel().scale(1.25).move_to([-4.2,.6,0]); w=wheel().scale(1.35).move_to([4.6,.9,0])
        car=VGroup(RoundedRectangle(width=2.5,height=.8,corner_radius=.15,color=BLUE),dot([-.75,-.45,0],GREY,.22),dot([.75,-.45,0],GREY,.22)).move_to([-1,-1.4,0])
        self.add(f,label('Fuel',-4.2,2.6,34),car,foot('Fuel allows motion; the driver chooses direction'))
        self.at('Fuel lets'); self.play(car.animate.shift(RIGHT*1.7),run_time=1.3)
        ways=VGroup(*[Arrow([2.1,-1.4,0],e,buff=0,color=BLUE,stroke_width=5,max_tip_length_to_length_ratio=.25) for e in ([3.2,-1.4,0],[3.0,-.6,0],[3.0,-2.2,0])])
        self.play(LaggedStart(*[GrowArrow(a) for a in ways],lag_ratio=.25),run_time=.7)
        self.at('The driver picks'); self.play(Create(w),FadeIn(label('Driver',4.6,3.0,34)),run_time=.5); self.play(Rotate(w,PI/5),run_time=.6)
        self.at('Fuel is permissive'); self.play(FadeIn(label('Permissive',-4.2,-2.25,32)),run_time=.4)
        self.at('The driver is'); self.play(FadeIn(label('Instructive',4.6,-2.25,32)),run_time=.4)
        self.finish()
class S04Why(SpokenScene):
    def construct(self):
        t=tiles(.5); d=delivery(1.45)
        cards=VGroup(chip('Permissive still possible',TEXT,28,fill_opacity=.06),chip('Instructive still possible',TEXT,28,fill_opacity=.06)).arrange(RIGHT,buff=.6).move_to([0,-1.7,0])
        self.add(t,d,legend(),cards,foot('Normal restoration cannot separate them'))
        off=t.copy().set_fill(GREY,opacity=.3)
        self.at('Removing a signal'); self.play(d.animate.set_opacity(.05),Transform(t,off),run_time=1.9)
        self.at('restoring its normal'); self.play(d.animate.set_opacity(1),Transform(t,tiles(.5)),run_time=1.9)
        self.at('It only shows'); self.play(FadeIn(head('The signal is needed')),run_time=.4)
        self.finish()
class S05Test(SpokenScene):
    def construct(self):
        t=tiles(0); d=delivery(1)
        cap=label('Normal signal and pattern',0,-1,30)
        self.add(t,d,legend(),head('Change the delivery'),cap)
        self.at('keep the signal'); self.play(Indicate(d,color=YELLOW),run_time=.5)
        self.at('but change where'); self.play(Transform(d,delivery(1,uniform=True)),Transform(cap,label('Even signal',0,-1,30)),run_time=1.2)
        self.at('Then ask whether'); self.play(FadeIn(foot('Does the pattern still form?')),run_time=.4)
        self.finish()
class S06Rule(SpokenScene):
    def construct(self):
        # Three rows, each: signal dots, tile strip, verdict beneath with clear space before the next row.
        # Convention: fate A (sage) forms where the signal is delivered, in the normal row and the moved row alike.
        def row(y,uniform=False,moved=False):
            tl=tiles(y,moved).stretch_to_fit_height(.9)
            return VGroup(tl,delivery(y+.7,uniform=uniform,moved=moved))
        normal=VGroup(row(2.35),label('Normal',-5.35,2.35,28))
        a=VGroup(row(.5,uniform=True),label('Even\nsignal',-5.35,.5,28))
        b=VGroup(row(-1.85),label('Moved\nsignal',-5.35,-1.85,28))
        pending=label('Move the signal; ask whether the pattern follows',0,-2.75,28)
        self.add(normal,a,b,pending)
        self.at('If the pattern stays'); self.play(Indicate(a,scale_factor=1.02),run_time=.6)
        self.at('was permissive'); self.play(FadeIn(label('Even signal: pattern unchanged → permissive',0,-.4,28)),run_time=.4)
        self.at('If the pattern follows')
        nb=VGroup(row(-1.85,moved=True),label('Moved\nsignal',-5.35,-1.85,28))
        self.play(Transform(b,nb),run_time=.8)
        self.at('it is instructive'); self.remove(pending)
        self.play(FadeIn(label('Moved signal: pattern follows → instructive',0,-2.75,28)),FadeIn(label('Fate A forms where the signal is delivered',0,-3.3,26,SAGE)),run_time=.4)
        self.finish()
class S07Edw(SpokenScene):
    def construct(self):
        p=pancreas(); p[2].set_opacity(0)
        self.add(p,head('Pancreas · scattered islets'),foot('Edwards and colleagues · 1989'),label('Sympathetic fibres at baseline',0,-2.05,28))
        self.at('directed'); self.play(p[2].animate.set_stroke(opacity=1).set_fill(opacity=.08),run_time=.8)
        self.at('pancreatic islets'); self.play(FadeIn(label('NGF-making islets',0,2.15,30,YELLOW)),run_time=.4)
        self.finish()
class S08Islet(SpokenScene):
    def construct(self):
        tissue=panel(); cells=VGroup(*[dot([x,y,0],GREY,.72) for x,y in [(-.8,0),(.55,.7),(.55,-.7)]])
        surround=VGroup(*[dot([x,y,0],GREY,.35).set_opacity(.3) for x,y in [(-4,1.7),(-4,-.5),(-3,-1.8),(3,1.8),(4,.5),(3,-1.8),(-2.5,1.8),(4,-1.6)]])
        self.add(tissue,surround,cells,Circle(radius=1.8,color=YELLOW),head('Islet: a hormone-making cell cluster'),foot('Within pancreatic tissue · three cells shown schematically'))
        self.at('clusters of'); self.play(Indicate(cells,scale_factor=1.05),run_time=.7)
        self.finish()
class S09Predict(SpokenScene):
    def construct(self):
        self.add(question())
        self.at('Predict'); self.play(Indicate(self.mobjects[0][1],scale_factor=1.02),run_time=.5)
        self.play(Indicate(self.mobjects[0][3],scale_factor=1.04,color=YELLOW),run_time=.8)
        self.finish()
class S10Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(question())
        for n in range(5,0,-1):
            count=VGroup(label('Predict',5.1,2.3,26,YELLOW),label(str(n),5.35,1.3,100,YELLOW)); self.add(count); self.wait(1); self.remove(count)
class S11Reveal(SpokenScene):
    def construct(self):
        p=reveal_pancreas(); h=head('NGF-making islets · in these mice'); self.add(p,h)
        self.at('of the islets'); self.play(Create(VGroup(*[VGroup(branch([q[0],-1.05+RV,0],[q[0],q[1]-.7+RV,0]),fan([q[0],q[1]+RV,0])) for q in ISLETS])),FadeIn(comparison()),run_time=1.1)
        self.at('The surrounding tissue'); self.play(FadeIn(surround_tag()),run_time=.4)
        self.at('The pattern followed'); self.play(FadeOut(h),FadeIn(head('Pattern followed the delivery → instructive here',YELLOW)),run_time=.4)
        self.finish()
class S12Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(reveal()); self.wait(3)
class S13Hoyle(SpokenScene):
    def construct(self):
        w=wiring(); w[4].set_opacity(0)
        self.add(w,head('Converse: NGF now also made by the neuron'),foot('Hoyle and colleagues · 1993'),label('Neuron makes\nits own NGF',-4.8,-1.6,28,YELLOW),label('Target NGF',2.9,.65,26,YELLOW))
        self.at('Their mice had'); self.play(Indicate(w[0],color=YELLOW),run_time=.7)
        self.finish()
class S14Flat(SpokenScene):
    def construct(self):
        w=wiring(); w[4].set_opacity(0)
        self.add(w,head('NGF in neuron, axon and target'),foot('Altered distribution, not shown to be uniform'))
        self.at('was made by'); self.play(Indicate(VGroup(*w[2][:3]),color=YELLOW),run_time=.7)
        self.at('not only by'); self.play(Indicate(w[2][3],color=YELLOW),run_time=.7)
        self.finish()
class S15Res(SpokenScene):
    def construct(self):
        w=wiring(False); self.add(w,DashedLine([-5.05,0,0],ENTRY,color=BLUE,stroke_opacity=.25),head('Neuron-made NGF'))
        self.at('Axons still'); self.play(Create(branch([-5.05,0,0],ENTRY)),run_time=1)
        reached=VGroup(chip('Reached\nthe target',TEXT,28,fill_opacity=.08).move_to([-4.9,1.85,0]),Arrow([-4.0,1.35,0],[-3.0,.12,0],buff=0,color=TEXT,stroke_width=4,max_tip_length_to_length_ratio=.25))
        self.play(FadeIn(reached),Create(arbor(False)),FadeIn(density_tag()),run_time=.7)
        self.play(FadeIn(foot('Sparse branching within the target')),run_time=.35)
        self.finish()
class S16Rest(SpokenScene):
    def construct(self):
        w=wiring(); tag=density_tag(); self.add(w,tag)
        self.at('in the islets'); self.play(FadeIn(head('Same mice · local rescue')),FadeIn(source([4.3,0,0])),FadeIn(label('NGF made\nin the islet',5.1,1.45,22,YELLOW)),Create(Line([4.65,1.05,0],[4.4,.16,0],color=YELLOW,stroke_width=3)),w[5].animate.set_color(YELLOW),run_time=.5)
        self.at('islet innervation'); self.play(Transform(w[4],arbor(True)),Transform(tag,density_tag(True)),FadeIn(foot('Islet innervation restored')),run_time=.7)
        self.finish()
class S17C1(SpokenScene):
    def construct(self):
        w=wiring(); self.add(w,head('Reaching a target'),foot('Sympathetic targets tested'))
        c=chip('Permissive',TEXT,28).move_to([-4.75,1.7,0])
        pointer=Arrow([-3.6,1.4,0],ENTRY,buff=.1,color=TEXT)
        self.at('is permissive'); self.play(FadeIn(c),GrowArrow(pointer),run_time=.5)
        self.finish()
class S18C2(SpokenScene):
    def construct(self):
        w=wiring(); w[1].set_stroke(opacity=0); dense=density_tag(True); self.add(w,head('Density and place within a target'),foot('In the sympathetic targets tested'),chip('Instructive',TEXT,28).move_to([-4.75,1.7,0]))
        self.at('It is instructive'); self.play(Transform(w[4],arbor(True)),FadeIn(dense),run_time=.7)
        self.at('and where'); self.play(Transform(w[4],local_arbor()),FadeIn(source([2.8,1.3,0])),FadeIn(label('NGF side',2.2,2.0,22,YELLOW)),FadeIn(Line([2.6,1.85,0],[2.78,1.46,0],color=YELLOW,stroke_width=3)),run_time=.7)
        self.at('Here the fuel');
        f=fuel().scale(.65).move_to([-6.1,-1.95,0]); wh=wheel().scale(.65).move_to([-4.5,-2.0,0])
        self.play(FadeOut(dense),FadeIn(f),FadeIn(wh),run_time=.5)
        self.finish()
class S19Dbl(SpokenScene):
    def construct(self):
        table=panel(0,11.6,2).move_to([0,1.5,0])
        row=VGroup(label('NGF and Bax deleted',-2.6,1.5,34,RED),label('→',.5,1.5,40),label('neurons alive',3.2,1.5,34,GREEN))
        cells=VGroup(*[dot([x,-1,0],GREEN,.62) for x in [-3,0,3]])
        self.add(head('Separate survival from innervation'),table,label('Survival test',0,1.5,32),cells,label('sympathetic neurons',0,-2.25,34))
        self.at('In mice lacking'); self.remove(self.mobjects[2]); self.play(FadeIn(row[:2]),run_time=.6)
        self.at('sympathetic neurons survive'); self.play(FadeIn(row[2]),Indicate(cells,color=GREEN),run_time=.6)
        self.finish()
class S20Dbl2(SpokenScene):
    def construct(self):
        self.add(head('NGF and Bax deleted'),foot('Needed for more than survival'))
        ys=[1.5,.2,-1.1]
        cells=VGroup(*[dot([-3.4,y,0],GREEN,.4) for y in ys])
        targets=VGroup(*[panel(x,2.5,1.0).move_to([x,y,0]) for x in [1.3,4.1] for y in ys])
        self.add(cells,targets,label('neurons alive',-3.4,2.5,28,GREEN),label('targets',2.7,2.5,28))
        self.at('With death blocked'); self.play(Indicate(cells,color=GREEN),run_time=.5)
        paths=VGroup(branch([-3,1.5,0],[.4,1.5,0]),branch([-3,.2,0],[-1.5,.2,0]),branch([-3,-1.1,0],[-1.5,-1.1,0]))
        self.at('They fail to'); self.play(Create(paths),targets[0].animate.set_stroke(BLUE),FadeIn(label('many targets not innervated',2.7,-2.25,28)),run_time=.8)
        self.finish()
class S21Sum1(SpokenScene):
    def construct(self):
        rows=VGroup()
        for i,text in enumerate(['Remove target → more death','Add target → less death','Add NGF → neurons saved','Remove NGF → neurons lost']):
            y=1.8-i*1.2
            line=T(text,36,GREY).move_to([0,y,0]).align_to([-4.1,y,0],LEFT)
            rows.add(VGroup(label('✓',-5.1,y,38,GREEN),line))
        self.add(head('Tests of the hypothesis'),rows)
        self.at('The target is needed'); self.play(rows[0][1].animate.set_color(TEXT),rows[1][1].animate.set_color(TEXT),run_time=.5)
        self.at('Adding'); self.play(rows[2][1].animate.set_color(TEXT),run_time=.5)
        self.at('Removing it'); self.play(rows[3][1].animate.set_color(TEXT),run_time=.5)
        self.finish()
class S22Sum2(SpokenScene):
    def construct(self):
        # Only the lesson's two reported age-specific relative counts are connected.
        a=Axes(x_range=[13.5,15.5,2],y_range=[0,1.1,.5],x_length=7.4,y_length=4.6,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([-1,.1,0])
        labs=VGroup(head('Neuron count relative to normal at the same age'),foot('Embryonic day',y=-3.3),*[label(str(v),a.c2p(13.5,v)[0]-.45,a.c2p(13.5,v)[1],28) for v in [0,.5,1]],*[label(str(v),a.c2p(v,0)[0],a.c2p(v,0)[1]-.4,28) for v in [13.5,15.5]])
        normal=a.plot_line_graph([13.5,15.5],[1,1],line_color=GREEN,add_vertex_dots=True)
        mutant=a.plot_line_graph([13.5,15.5],[1,.85],line_color=PURPLE,add_vertex_dots=True)
        ends=VGroup(label('Normal = 1',4.3,a.c2p(15.5,1)[1]+.2,28,GREEN),label('TrkA-null\n0.85',4.5,a.c2p(15.5,.85)[1]-.45,28,PURPLE))
        self.add(a,labs)
        self.at('the neurons were made'); self.play(Create(normal),Create(mutant),FadeIn(ends),run_time=.6)
        self.at('then lost'); self.play(Indicate(mutant,color=PURPLE),run_time=.5)
        # Allocation bound S=floor(min(N,F/q)), N=1000 and q=1.
        b=Axes(x_range=[0,1500,500],y_range=[0,1100,500],x_length=7.4,y_length=4.6,tips=False,axis_config={'color':GREY,'include_ticks':False}).move_to([-1,.1,0])
        ticks=VGroup(*[label(str(v),b.c2p(0,v)[0]-.65,b.c2p(0,v)[1],28) for v in [0,500,1000]],*[label(str(v),b.c2p(v,0)[0],b.c2p(v,0)[1]-.4,28) for v in [0,500,1000,1500]])
        cap=Line(b.c2p(0,1000),b.c2p(1500,1000),color=TEAL,stroke_width=12)
        f=np.arange(0,1501,10); survivors=np.floor(np.minimum(1000,f))
        curve=b.plot_line_graph(f,survivors,line_color=GREEN,stroke_width=4,add_vertex_dots=False)
        second=VGroup(b,ticks,head('Survivors (neurons) · ideal allocation bound'),foot('Supply / need per neuron (neuron equivalents)',y=-3.3),cap,label('N = number made',.3,2.5,28,TEAL),chip('Illustrative model',GREY,24).move_to([4.7,-1.2,0]))
        surv=VGroup(label('Survivors',4.45,b.c2p(1500,1000)[1]-.6,28,GREEN),Line(b.c2p(1500,1000)+[.12,-.1,0],[3.65,b.c2p(1500,1000)[1]-.6,0],color=GREEN))
        self.at('Acting as a survival factor'); self.play(FadeOut(VGroup(a,labs,normal,mutant,ends)),FadeIn(second),run_time=.45)
        self.at('cannot raise survivors'); self.play(Create(curve),FadeIn(surv),run_time=.65)
        self.finish()
class S23Net(SpokenScene):
    def construct(self):
        boxes=VGroup(*[panel(x,3.8,4.7).move_to([x,-.45,0]) for x in [-4.1,0,4.1]])
        self.add(head('Survival and connection pattern'),label('More neurons are made than the target can support.',0,2.45,28,TEAL),boxes)
        a=VGroup(dot([-4.1,.7,0],GREEN,.65),label('Keeps specified\nneurons alive',-4.1,-1.5,30))
        b=VGroup(dot([-.7,.8,0],BLUE,.38),dot([.7,.8,0],BLUE,.55),source([-.7,-.1,0]),source([.5,-.1,0]),source([.9,-.1,0]),label('Neuron types\ndiffer in need',0,-1.5,30))
        c=VGroup(Circle(radius=1.1,color=GREY).move_to([4.1,.65,0]),source([4.8,1.2,0]),fan([4.1,.5,0],True).scale(.85,about_point=[4.1,.5,0]),label('Local supply\nhelps connections\npersist',4.1,-1.5,28))
        for g in (a,b,c): g.shift(DOWN*.3)
        self.at('keeps already specified'); self.play(FadeIn(a),run_time=.5)
        self.at('types differ'); self.play(FadeIn(b),run_time=.5)
        self.at('Where it is supplied'); self.play(FadeIn(c),run_time=.6)
        self.finish()
class S24Next(SpokenScene):
    def construct(self):
        target=panel(2.8,5.2,5.1); site=source([2.1,0,0])
        self.add(head('Next lesson'),foot('Competition for targets',TEAL),target,site,neuron(1.5),neuron(-1.5))
        upper=branch([-5.05,1.5,0],[2.1,0,0]); lower=branch([-5.05,-1.5,0],[2.1,0,0])
        self.at('How some neurons'); self.play(Create(upper),Create(lower),run_time=.8)
        self.at('win'); self.play(Transform(lower,branch([-5.05,-1.5,0],[-2.7,-1.1,0])),upper.animate.set_stroke(width=8),run_time=1)
        self.play(FadeIn(label('keeps contact',-1.6,1.55,26)),FadeIn(label('withdraws',-3.0,-1.75,26,RED)),run_time=.4)
        self.finish()
class S25Take(SpokenScene):
    def construct(self):
        w=wiring(); self.add(w,foot('In the targets tested'))
        self.at('for survival'); self.play(w[0].animate.set_color(GREEN),FadeIn(head('For survival, NGF is permissive')),run_time=.5)
        self.at('Within a target'); self.play(FadeIn(source([2.8,1.3,0])),run_time=.4)
        self.at('it also instructs'); self.play(Transform(w[4],local_arbor()),FadeIn(label('Instructs where\naxons branch',1.45,-1.3,30,YELLOW)),run_time=.7)
        self.finish()
class S26End(EndCard):
    LINE='NGF permits survival; within tested targets, it also instructs branching.'
    def construct(self):
        self.add(label('For survival, NGF is permissive.',0,1,40),label('Within tested targets, it also instructs branching.',0,-.3,34,YELLOW),label('biochemistrypedia.com',0,-2,26,TEAL))
        self.finish()
