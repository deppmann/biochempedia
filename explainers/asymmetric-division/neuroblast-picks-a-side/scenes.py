"""Chapter 5, reviewed animation.
COLOR MAP: BLUE neuroblast/renewal; GREEN differentiated daughter; GOLD apical
polarity; YELLOW Numb; TEXT Miranda/Prospero/Brat; RED faulty control/OFF;
GREY outline/unknown; TEAL interactive cue. Geometry is schematic, not data.
"""
import numpy as np
from bp_style import *
from bp_style import SpokenScene as BaseSpokenScene

C = np.array([-1.5, 0., 0.])
R = 3.12

class SpokenScene(BaseSpokenScene):
    # Keep timing identical to the shared helper without modifying sync.log.
    def at(self, phrase, lead=.2, nth=0):
        rest=self.t_of(phrase,nth)-lead-self.elapsed()
        if rest>.02: self.wait(rest)

def txt(s,x=0,y=0,color=TEXT,size=28):
    return T(s,size=size,color=color,line_spacing=1.2).move_to([x,y,0])

def tag(s,x,y,col=TEXT,size=26):
    g=chip(s,col,size=size,pad=.14,fill_opacity=.22).move_to([x,y,0])
    g[0].set_fill(BG,opacity=1)
    return g

def head(s): return txt(s,0,3.53,size=28)
def cell(c=C,r=R,color=BLUE,op=.08):
    return Circle(radius=r,color=color,stroke_width=4,fill_color=color,fill_opacity=op).move_to(c)
def patch(top=True,col=GOLD,c=C,r=R):
    return Arc(radius=r,start_angle=PI*.30 if top else PI*1.2,angle=PI*.40 if top else PI*.6,arc_center=c,color=col,stroke_width=14)
def basal(c=C,r=R):
    return VGroup(Arc(radius=r,start_angle=PI*1.2,angle=PI*.28,arc_center=c,color=YELLOW,stroke_width=14),Arc(radius=r,start_angle=PI*1.52,angle=PI*.28,arc_center=c,color=TEXT,stroke_width=14))
def spindle(vertical=False,c=C,scale=1):
    a=UP if vertical else RIGHT
    p,q=c+1.35*scale*a,c-1.35*scale*a
    b=np.array([a[1],-a[0],0])
    return VGroup(*[VGroup(Line(p,c+b*d*scale,color=GREY,stroke_width=3),Line(c+b*d*scale,q,color=GREY,stroke_width=3)) for d in (-.48,0,.48)],Dot(p,radius=.13*scale,color=TEXT),Dot(q,radius=.13*scale,color=TEXT))
def checklist(step=0):
    lines=['1  Mark the top','2  Aim the spindle','3  Keep the cargo\n    off the top','4  Carry the cargo']
    return VGroup(*[txt(s,4.5,2.1-i*1.25,GOLD if i+1==step else GREY,26) for i,s in enumerate(lines)])
def linked(s,x,y,anchor,col=GOLD):
    g=tag(s,x,y,col)
    ax=anchor[0]; below=anchor[1]<y
    edge=g.get_bottom() if below else g.get_top()
    over=g.get_left()[0]+.2<ax<g.get_right()[0]-.2
    start=np.array([ax,edge[1],0]) if over else edge
    line=Line(start,anchor,color=col,stroke_width=3)
    return VGroup(line,g)
def top_labels(n=3):
    # Bazooka and Par6 sit inside the cortex; aPKC sits on the arc itself.
    out=[linked('Bazooka (Par3)',-2.1,1.95,[-2.7,2.88,0]),linked('Par6',-.05,1.95,[-.1,2.79,0]),VGroup(tag('aPKC',-1.5,3.1,GOLD))]
    return VGroup(*out[:n])
def top_scene(scene,n=3,step=1):
    scene.add(cell(),patch(),top_labels(n),checklist(step))
def rig_labels(n=4):
    specs=[('Inscuteable',-1.5,2.4,[-1.5,3.12,0]),('Pins',-2.8,1.65,[-3.3,2.5,0]),('G alpha-i',-.15,1.65,[.3,2.5,0]),('Mud',-.15,.7,[-.15,1.33,0])]
    return VGroup(*[linked(*a) for a in specs[:n]])
def rig(scene,n=4,vertical=False):
    sp=spindle(vertical)
    scene.add(cell(),patch(),sp,rig_labels(n),checklist(2))
    return sp

def motor():
    return VGroup(RoundedRectangle(width=1.3,height=.40,corner_radius=.1,color=GOLD,fill_color=GOLD,fill_opacity=.5).move_to(C+UP*2.9),Line(C+UP*2.7,C+UP*2.25,color=GOLD,stroke_width=9),linked('dynein',-3.,1.8,[-2.15,2.9,0],GOLD))
def astral(vertical=False):
    p=C+(UP if vertical else RIGHT)*1.35
    return VGroup(*[Line(p,C+np.array([x,2.7,0]),color=GREY,stroke_width=5) for x in (-.65,0,.65)])

def basal_labels():
    return VGroup(tag('Numb',-2.65,-2.15,YELLOW),tag('Miranda',-.6,-2.25))
def cortical_proteins():
    # Six chips distributed around the inner cortex, clear of the outline.
    specs=[('Numb',-3.1,1.65,YELLOW),('Miranda',.1,1.65,TEXT),('Lgl · helper',-1.5,2.3,TEXT),('Numb',-3.15,-1.6,YELLOW),('Miranda',.15,-1.6,TEXT),('Lgl · helper',-1.5,-2.5,TEXT)]
    return VGroup(*[tag(*s) for s in specs])
def badges():
    return VGroup(*[tag('P',x,y,GOLD) for x,y in [(-3.1,1.08),(.1,1.08),(-1.5,1.65)]])
def phos_base(scene,with_badges=True):
    proteins=cortical_proteins()
    key=VGroup(*[txt(t,0,0,TEXT,26) for t in ['P = phosphate tag','Miranda tagging:','larval neuroblasts']]).arrange(DOWN,aligned_edge=LEFT,buff=.2).move_to([2.9,-2.8,0],aligned_edge=LEFT)
    scene.add(cell(),patch(),proteins,checklist(3),tag('aPKC',-1.5,3.1,GOLD),key)
    if with_badges: scene.add(badges())
    return proteins

def cargo_scene(scene,step=4):
    body,top,cres,labs=cell(),patch(),basal(),basal_labels()
    scene.add(body,top,cres,labs,checklist(step))
    return body,top,cres,labs

def loaded():
    pro=tag('Prospero',-1.2,-1.35); brat=tag('Brat',.5,-1.35)
    # Short straight stems join both cargo chips to the Miranda chip, inside the cortex.
    links=VGroup(Line([-1.0,-1.64,0],[-.9,-1.95,0],color=TEXT,stroke_width=5),Line([.5,-1.64,0],[-.1,-1.95,0],color=TEXT,stroke_width=5))
    caption=txt('translational\nrepressor',-.1,-.5,size=26)
    return VGroup(links,pro,brat,caption)
def pon():
    return VGroup(Line([-3.3,.1,0],[-2.65,-1.87,0],color=YELLOW,stroke_width=4),tag('Partner of Numb (Pon)',-2.15,.4,YELLOW))

NBC=np.array([-1.5,1.3,0]); NBR=1.8
GMC=np.array([-1.5,-1.58,0]); GMR=1.08   # about 60% of the neuroblast's diameter
def daughters():
    return cell(NBC,NBR),cell(GMC,GMR,GREEN)
CARGO=[('Numb',-.75,YELLOW),('Miranda',-1.39,TEXT),('Prospero',-2.03,TEXT),('Brat',-2.67,TEXT)]
def daughter_cargo():
    # a column of chips to the right of the small daughter, left edges aligned
    return VGroup(*[tag(s,0,y,col).move_to([.45,y,0],aligned_edge=LEFT) for s,y,col in CARGO])
def cargo_links(chips):
    out=[]
    for ch,(s,y,col) in zip(chips,CARGO):
        ty=float(np.clip(y,GMC[1]-.92*GMR,GMC[1]+.92*GMR))
        ex=GMC[0]+np.sqrt(GMR**2-(ty-GMC[1])**2)
        out.append(Line([ch.get_left()[0],y,0],[ex,ty,0],color=col,stroke_width=3))
    return VGroup(*out)

def prediction():
    return VGroup(cell(),head('Lose Miranda'),tag('Prospero ?',-2.2,.7),tag('Brat ?',-.5,-.3),txt('Where do Prospero\nand Brat go?',4.0,1.3,size=28),txt('What happens over\nmany divisions?',4.0,-.8,size=28))

def comparison(mark=False):
    g=VGroup(VectorizedPoint([0,3.7,0]))
    for x,name,vertical in [(-3.4,'Sensory organ precursor',False),(3.4,'Neuroblast',True)]:
        c=np.array([x,-.15,0])
        g.add(txt(name,x,3.48,size=27),Rectangle(width=6.1,height=1.7,color=GREY,fill_opacity=.07).move_to(c),cell(c,3.05),spindle(vertical,c,1.25),linked('epithelial surface',x-1.65,1.3,[x-1.65,.7,0],GREY),txt('basal',x,-3.55,GREY,26))
        if mark:
            g.add(Arc(radius=3.05,start_angle=PI*.32 if vertical else -PI*.18,angle=PI*.36,arc_center=c,color=GOLD,stroke_width=14))
    return g

class S00Title(TitleCard):
    LESSON='Asymmetric Division: Numb and the Neuroblast'
    TITLE='How the Neuroblast Picks a Side'
    def construct(self):
        self.add(txt(self.LESSON,0,2,GREY,26),VGroup(T('How the Neuroblast',44,font=TITLE_FONT),T('Picks a Side',44,font=TITLE_FONT)).arrange(DOWN,buff=.25),Line([-1,-1.2,0],[1,-1.2,0],color=GOLD,stroke_width=4))
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        q=txt('?',-3.7,1.95,GOLD,76)
        num=tag('Numb',-1.7,.3,YELLOW)
        self.add(cell(),q,num,txt('How does a cell put\na protein on one side?',4,0,size=28))
        self.at('The bristle showed')
        self.play(num.animate.move_to([-2.4,1,0]),run_time=.8)
        self.at('But how does')
        self.play(num.animate.move_to([-.2,-1,0]),Indicate(q),run_time=1)
        self.finish()

class S02Nb(SpokenScene):
    def construct(self):
        nb,gmc=daughters()
        self.add(nb,gmc,txt('apical',-1.5,3.52,GOLD),txt('basal',-1.5,-3.1,GREY),txt('neuroblast',2.2,1.3,BLUE),txt('small basal\ndaughter',2.3,-1.58,GREEN))
        self.finish()

class S03Clue(SpokenScene):
    def construct(self):
        card=RoundedRectangle(width=4.6,height=2.2,corner_radius=.2,color=GOLD,stroke_width=4,fill_color=GOLD,fill_opacity=.1).move_to([4.2,1.5,0])
        yr=T('1995',size=80,color=GOLD,font=TITLE_FONT).move_to([4.2,1.9,0])
        who=txt('Knoblich, Jan and Jan',4.2,.8,TEXT,26)
        self.add(cell(),card,yr,who)
        nuc=cell(C,1.45,GREY,.05)
        self.at('Prospero is')
        self.play(FadeIn(tag('Prospero',-1.5,0)),run_time=.35)
        self.at('works in the nucleus')
        lab=VGroup(Line([-1.5,1.45,0],[-1.5,1.7,0],color=GREY,stroke_width=3),tag('nucleus',-1.5,2.0,GREY))
        self.play(Create(nuc),FadeIn(lab),run_time=.5)
        self.finish()

class S04Clue2(SpokenScene):
    def construct(self):
        pro=tag('Prospero',-1.5,0)
        self.add(cell(),head('Knoblich, Jan and Jan · 1995'),pro)
        self.at('found it at the membrane')
        cres=patch(False,TEXT)
        self.play(pro.animate.move_to([-.4,-1.95,0]),Create(cres),FadeIn(txt('at the membrane',4.3,-1.3,TEXT,28)),run_time=.65)
        self.at('in the same crescent')
        self.play(ReplacementTransform(cres,basal()),FadeIn(tag('Numb',-2.65,-2.15,YELLOW)),FadeIn(txt('same crescent\nas Numb',4.3,-2.5,YELLOW,28)),run_time=.5)
        self.finish()

class S05Centrosome(SpokenScene):
    def construct(self):
        sp=spindle(True)
        self.add(cell(),basal(),tag('Numb',-2.65,-2.15,YELLOW),tag('Prospero',-.4,-1.95),sp)
        self.at('one centrosome')
        self.play(Indicate(sp[-1],color=GOLD),FadeIn(linked('centrosome',3.4,-1.35,sp[-1].get_center(),TEXT)),run_time=.5)
        self.at('did not need microtubules')
        self.play(FadeOut(VGroup(*sp[:-2])),FadeIn(txt('no microtubules\nneeded',4.1,1.2,TEXT,28)),run_time=.65)
        self.at('not carried into place')
        self.play(FadeIn(txt('Crescent stays',4,-2.5)),run_time=.4)
        self.finish()

class S06System(SpokenScene):
    def construct(self):
        self.add(cell(),checklist())
        chips=VGroup(tag('Numb',-2.65,-2.15,YELLOW),tag('Miranda',-.6,-2.25),tag('Prospero',-1.2,-1.35),tag('Brat',.5,-1.35))
        brace=Brace(chips,UP,buff=.12,color=TEXT)
        label=txt('cargo',-1.0,-.55,TEXT,28)
        self.at('marks one side')
        self.play(FadeIn(basal()),FadeIn(chips),run_time=.6)
        self.play(FadeIn(brace),FadeIn(label),run_time=.4)
        self.finish()
class S07Step1(SpokenScene):
    def construct(self):
        self.add(cell(),checklist(1))
        self.at('Step one')
        self.finish()
class S08Par3(SpokenScene):
    def construct(self):
        self.add(cell(),checklist(1))
        dots=VGroup(*[Dot(C+np.array([x,y,0]),radius=.13,color=GOLD) for x,y in [(-1,.4),(.8,.7),(0,-.8)]])
        start=VGroup(Line([-1.5,-1.45,0],[-1.5,-.95,0],color=GOLD,stroke_width=3),tag('Bazooka (Par3)',-1.5,-1.75,GOLD))
        self.add(dots,start)
        self.at('gathers at the top')
        self.play(FadeOut(start),ReplacementTransform(dots,patch()),FadeIn(top_labels(1)),run_time=.6)
        self.finish()
class S09Par6(SpokenScene):
    def construct(self):
        top_scene(self,1)
        self.at('Par six')
        self.play(FadeIn(top_labels(2)[1],shift=UP*.2),run_time=.35)
        self.finish()
class S10Apkc(SpokenScene):
    def construct(self):
        top_scene(self,2)
        self.at('a kinase called')
        self.play(FadeIn(top_labels(3)[2]),run_time=.4)
        self.at('they define the top')
        self.play(Indicate(self.mobjects[1],color=GOLD),run_time=.5)
        self.finish()
class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        top_scene(self)
        self.wait(2)
class S12Step2(SpokenScene):
    def construct(self):
        self.add(cell(),patch(),checklist(2),spindle())
        self.at('Step two')
        self.finish()
class S13Insc(SpokenScene):
    def construct(self):
        self.add(cell(),patch(),spindle(),checklist(2))
        self.at('joins the top complex')
        self.play(FadeIn(rig_labels(1)),run_time=.35)
        self.at('recruits a protein')
        self.play(FadeIn(rig_labels(2)[1]),run_time=.35)
        self.finish()
class S14Gai(SpokenScene):
    def construct(self):
        rig(self,2)
        self.at('protein subunit')
        self.play(FadeIn(rig_labels(3)[2]),run_time=.35)
        self.at('and a protein called')
        self.play(FadeIn(rig_labels(4)[3]),run_time=.35)
        self.finish()
class S15Dynein(SpokenScene):
    def construct(self):
        sp=spindle(); self.add(cell(),patch(),sp,checklist(2))
        mot=motor()
        self.at('they anchor the motor')
        self.play(FadeIn(mot),run_time=.45)
        ast=astral()
        self.at('pulls on microtubules')
        self.play(Create(ast),run_time=.35)
        for _ in range(2):
            self.play(Indicate(ast,color=GOLD,scale_factor=1.02),mot[1].animate.shift(UP*.15),rate_func=there_and_back,run_time=.65)
        self.finish()
class S16Aligned(SpokenScene):
    def construct(self):
        sp,ast=spindle(),astral()
        self.add(cell(),patch(),motor(),sp,ast,checklist(2))
        self.at('spindle lines up')
        self.play(Transform(sp,spindle(True)),Transform(ast,astral(True)),run_time=.7)
        self.at('furrow will cut')
        ring=DashedVMobject(Ellipse(width=6.24,height=.38,color=TEXT,stroke_width=3).move_to(C),num_dashes=35)
        self.play(Create(ring),FadeIn(txt('future furrow',.05,-.45,TEXT,26)),run_time=.5)
        self.finish()

def insc_picture():
    return VGroup(cell(),patch(),spindle(False).rotate(.35,about_point=C),Arc(radius=R,start_angle=-.2,angle=.45,arc_center=C,color=YELLOW,stroke_width=14),Arc(radius=R,start_angle=-.8,angle=.45,arc_center=C,color=TEXT,stroke_width=14),tag('Numb',.7,-.1,YELLOW),tag('Prospero',.25,-1.4),head('Without Inscuteable'),txt('orientation lost',-1.7,.8,RED,27),checklist(2),txt('spindle misaimed; Numb\nand Prospero misplaced',3.8,-3,RED,26))
class S17InscNeed(SpokenScene):
    def construct(self):
        pic=insc_picture(); self.add(pic)
        self.at('both to aim the spindle')
        self.play(Rotate(pic[2],.65,about_point=C),run_time=.8)
        self.at('and to place')
        self.play(Rotate(pic[2],-1.15,about_point=C),run_time=.8)
        self.finish()
class S18Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(insc_picture()); self.wait(2)
class S19Step3(SpokenScene):
    def construct(self):
        self.add(cell(),patch(),checklist(3),cortical_proteins(),txt('Cargo: Numb, Miranda,\nProspero and Brat',4.2,-3.0,size=26))
        self.at('Step three')
        self.finish()
class S20Phos(SpokenScene):
    def construct(self):
        phos_base(self,False)
        self.at('phosphorylates')
        self.play(FadeIn(badges()),run_time=.6)
        self.finish()
class S21Release(SpokenScene):
    def construct(self):
        proteins=phos_base(self,False); b=badges(); self.add(b)
        self.at('let go of the cortex')
        shifts=[np.array([1.,.3,0]),np.array([.35,-.8,0]),np.array([0,-2.25,0])]
        self.play(*[VGroup(proteins[i],b[i]).animate.shift(shifts[i]).set_opacity(.15) for i in range(3)],run_time=.8)
        self.at('works only at the top')
        self.play(Indicate(self.mobjects[1],color=GOLD),run_time=.5)
        self.finish()
class S21bBasal(SpokenScene):
    def construct(self):
        p=cortical_proteins(); b=badges()
        for i,shift in enumerate([[1.,.3,0],[.35,-.8,0],[0,-2.25,0]]):
            p[i].shift(shift); b[i].shift(shift)
        released=VGroup(*p[:3],b).set_opacity(.15)
        self.add(cell(),patch(),released,VGroup(*p[3:]),checklist(3))
        self.at('bound only at the bottom')
        self.play(FadeOut(released),FadeOut(VGroup(*p[3:])),Create(basal()),FadeIn(basal_labels()),run_time=.65)
        self.at('is a helper here')
        self.play(FadeIn(tag('Lgl: helper, not cargo',-1.5,2.2)),run_time=.4)
        self.finish()
class S22Step4(SpokenScene):
    def construct(self):
        cargo_scene(self,4); self.at('Step four'); self.finish()
class S23Miranda(SpokenScene):
    def construct(self):
        cargo_scene(self); g=loaded()
        self.at('carries Prospero')
        self.play(FadeIn(g[1]),Create(g[0][0]),run_time=.4)
        self.at('the translational repressor')
        self.play(FadeIn(g[2]),Create(g[0][1]),FadeIn(g[3]),run_time=.4)
        self.finish()
class S24Pon(SpokenScene):
    def construct(self):
        cargo_scene(self); self.add(loaded())
        self.at('uses its own')
        self.play(FadeIn(pon()),run_time=.4)
        self.finish()
class S25Divide(SpokenScene):
    def construct(self):
        body,top,cres,labs=cargo_scene(self); load=loaded(); po=pon(); self.add(load,po)
        nb,gmc=daughters(); cargo=daughter_cargo()
        self.at('The cell divides')
        # A pinching outline bridges the mother and the two separated daughters.
        pinch=VGroup(cell([-1.5,1.3,0],2.2),cell([-1.5,-1.7,0],1.2,GREEN))
        self.play(Transform(body,pinch),FadeOut(self.mobjects[4]),FadeOut(top),FadeOut(cres),FadeOut(po),FadeOut(load[0]),FadeOut(load[3]),run_time=.65)
        source=VGroup(labs[0],labs[1],load[1],load[2])
        self.play(ReplacementTransform(body,VGroup(nb,gmc)),Transform(source,cargo),FadeIn(txt('neuroblast',-4.6,1.3,BLUE)),FadeIn(cargo_links(cargo)),run_time=.7)
        self.at('the ganglion mother cell')
        self.play(FadeIn(txt('ganglion mother\ncell (GMC)',-4.75,-1.58,GREEN)),run_time=.35)
        self.at('inherits the cargo')
        self.play(Indicate(source,color=TEXT,scale_factor=1.06),run_time=.5)
        self.finish()
class S26Prospero(SpokenScene):
    def construct(self):
        self.add(cell(C,R,GREEN),head('Ganglion mother cell'),cell(C,1.4,GREY,.05))
        pro=tag('Prospero',-1.5,-2.35); self.add(pro)
        genes=VGroup(tag('self-renewal',4,1,BLUE),tag('division',4,-.5,BLUE))
        for g in genes: g[1].set_color(TEXT)
        self.add(genes,txt('nucleus',-1.5,1.05,GREY,26))
        self.at('enters its nucleus')
        self.play(pro.animate.move_to(C),GrowArrow(Arrow([-1.5,-1.9,0],[-1.5,-.5,0],color=TEXT,buff=.12)),run_time=.7)
        self.at('shuts down genes')
        self.play(Transform(genes,VGroup(tag('self-renewal: OFF',4,1,RED),tag('division: OFF',4,-.5,RED))),run_time=.5)
        self.finish()
class S27Predict(SpokenScene):
    def construct(self):
        mir=tag('Miranda',-.6,-2.25); pic=prediction()
        self.add(cell(),mir)
        self.at('Now remove')
        self.play(FadeOut(mir),FadeIn(VGroup(*pic[1:4])),run_time=.35)
        self.at('Where do')
        self.play(FadeIn(pic[4]),run_time=.3)
        self.at('What happens')
        self.play(FadeIn(pic[5]),run_time=.3)
        self.finish()
class S28Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction(),txt('pause and predict',4,-2.4,TEAL,26))
        ring=Arc(radius=.35,start_angle=PI/2,angle=TAU,color=TEAL,stroke_width=7).move_to([4,-3.15,0]); self.add(ring)
        self.play(Uncreate(ring),run_time=5,rate_func=linear)
class S29Reveal(SpokenScene):
    def construct(self):
        pic=prediction(); cres=DashedVMobject(patch(False,TEXT),num_dashes=18).set_opacity(.75)
        self.add(VGroup(*pic[:4]),cres)
        self.at('They lose their crescent',lead=-.6)
        self.play(FadeOut(cres),pic[2].animate.set_opacity(.6),pic[3].animate.set_opacity(.6),FadeIn(txt('No basal crescent',4,1.4,RED,28)),run_time=1.4)
        self.at('Where they end up')
        self.play(FadeIn(txt('Location varies with\nstage and lineage',4,-.2,size=28)),run_time=.4)
        self.finish()

POP=[np.array([-2.6+.68*np.sqrt(i+.5)*np.cos(i*2.39996),-.2+.78*.68*np.sqrt(i+.5)*np.sin(i*2.39996),0]) for i in range(24)]
def pcell(i):
    green=i%3==2
    return cell(POP[i],.26 if green else .34,GREEN if green else RED,.2)
def population(n):
    # Schematic branching counts, not measurements: every third daughter stays green and stops dividing.
    return VGroup(*[pcell(i) for i in range(n)])
def host():
    return VGroup(head('Larval miranda mutant brain tissue'),RoundedRectangle(width=7.4,height=5.8,color=GREY).move_to([-2.6,-.3,0]),txt('transplanted into adult host',-2.6,2.93,GREY,26),txt('schematic',4.8,-3,GREY,26))
def count_txt(n): return txt('Dividing cells: '+str(n),4.3,1.5,RED,26)
def tail_labels(): return VGroup(txt('some daughters\nkeep dividing',4.3,-.4,RED,26),txt('others stop',4.3,-1.6,GREEN,26))
class S30Reveal2(SpokenScene):
    def construct(self):
        self.add(host()); nb=cell([-2.6,-.2,0],1.5,RED,.18); self.add(nb)
        count=count_txt(1); self.add(count)
        self.at('overgrows when transplanted')
        first=VGroup(pcell(0),pcell(1))
        self.play(ReplacementTransform(nb,first),run_time=.65)
        self.at('Faulty sorting can let')
        self.play(Transform(count,count_txt(2)),run_time=.35)
        shown=2
        for total,div in [(4,3),(8,6),(15,10),(24,16)]:
            new=[pcell(i) for i in range(shown,total)]
            par=[POP[max(range(i),key=lambda j:-np.linalg.norm(POP[j]-POP[i]))] for i in range(shown,total)]
            self.play(*[GrowFromPoint(c,q) for c,q in zip(new,par)],Transform(count,count_txt(div)),run_time=.7)
            shown=total
        self.play(FadeIn(tail_labels()),run_time=.4)
        self.finish()
class S31Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(host(),population(24),count_txt(16),tail_labels()); self.wait(2)
class S32Sop(SpokenScene):
    def construct(self):
        g=comparison(); self.add(g)
        self.at('within its epithelium')
        self.play(Indicate(g[4],color=GOLD),run_time=.6)
        self.at('The neuroblast divides')
        self.play(Indicate(g[10],color=GOLD),run_time=.6)
        self.finish()
class S33Same(SpokenScene):
    def construct(self):
        g=comparison(); self.add(g)
        self.at('both mark one side')
        marks=comparison(True)
        self.play(Create(marks[7]),Create(marks[14]),run_time=.5)
        self.at('aim the spindle')
        self.play(Indicate(g[4],color=GOLD),Indicate(g[10],color=GOLD),run_time=.5)
        self.finish()

def takeaway():
    nb,gmc=daughters()
    cargo=daughter_cargo()
    return VGroup(nb,gmc,patch(c=NBC,r=NBR),spindle(True,NBC,.95),cargo,cargo_links(cargo),txt('neuroblast',-4.6,1.3,BLUE,26),txt('small daughter',-4.65,-1.58,GREEN,26))
class S34Takeaway(SpokenScene):
    def construct(self):
        self.add(takeaway()); steps=checklist(); self.add(steps)
        for phrase,n in [('Mark the top',1),('aim the spindle',2),('keep the cargo',3),('load the small daughter',4)]:
            self.at(phrase); self.play(Transform(steps,checklist(n)),run_time=.2)
        self.finish(); self.wait(2)
class S35End(EndCard):
    LINE='Mark the top, aim the spindle, clear the top, load the daughter.'
    def construct(self):
        block=VGroup(*[txt(t,0,0,TEXT,29) for t in ['Mark the top,','aim the spindle,','clear the top,','load the daughter.']]).arrange(DOWN,aligned_edge=LEFT,buff=.28).move_to([3.3,.9,0],aligned_edge=LEFT)
        self.add(block,takeaway(),txt('biochemistrypedia.com',4.6,-3.2,TEAL,26))
        self.finish()
