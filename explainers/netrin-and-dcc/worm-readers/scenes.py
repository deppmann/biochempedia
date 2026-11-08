"""Chapter 3: reviewed schematic animation.
COLOR MAP: yellow UNC-6 cue; blue cells/axons; teal UNC-40;
purple UNC-5; green toward; red away; grey anatomy/normal results;
amber and white disrupted results. Paths are anatomical schematics, not data.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
AMBER='#F3BB63'
LESSON='Netrin and DCC: One Cue, Two Answers'

def label(s,x=0,y=0,color=TEXT,size=28):
    return T(s,size=size,color=color).move_to([x,y,0])
def heading(s): return label(s,0,3.2,size=32)
def route(points,color=BLUE,width=7):
    return VMobject().set_points_as_corners([np.array(p,float) for p in points]).set_stroke(color,width)
def cone(p,scale=.65):
    c=np.array(p,float)
    shape=Polygon(c+[-scale,-scale*.6,0],c+[scale*.55,-scale*.5,0],c+[scale,0,0],c+[scale*.55,scale*.5,0],c+[-scale,scale*.6,0],color=BLUE,fill_color=BLUE,fill_opacity=.3)
    fingers=VGroup(*[Line(c+[scale*.5,dy*.5,0],c+[scale*1.25,dy,0],color=BLUE,stroke_width=4) for dy in [-scale,0,scale]])
    return VGroup(shape,fingers)
def cups(p,color,scale=.65):
    c=np.array(p,float)
    return VGroup(*[VGroup(Line(c+[x,scale*.5,0],c+[x,scale*.9,0],color=color,stroke_width=5),Arc(radius=.18,start_angle=PI,angle=PI,arc_center=c+[x,scale*1.1,0],color=color,stroke_width=5)) for x in [-scale*.6,0,scale*.6]])
def section(x=0,y=-.1,r=2.6,cue=True):
    return VGroup(Circle(radius=r,color=GREY).move_to([x,y,0]),Line([x-r*.67,y-r*.73,0],[x+r*.67,y-r*.73,0],color=YELLOW,stroke_width=13) if cue else VGroup())
def section_labels():
    return VGroup(label('worm, cross-section',-4.35,2.35,size=26),label('dorsal',0,2.8,size=26),label('ventral · UNC-6',0,-3.15,YELLOW,28))
def worm(y=0,height=4.5):
    return RoundedRectangle(width=11.4,height=height,corner_radius=height/2-.05,color=GREY,fill_color=BLUE,fill_opacity=.035).move_to([0,y,0])
def sides(): return VGroup(label('dorsal',4.4,2.35,size=26),label('ventral',4.4,-2.95,size=26))
def cord(center=(-1.8,-.1,0),scale=1.2,labels=True):
    c=np.array(center); pt=lambda x,y:c+scale*np.array([x,y,0])
    outer=Ellipse(width=4.4*scale,height=4.8*scale,color=GREY).move_to(c)
    canal=Ellipse(width=.45*scale,height=1.15*scale,color=GREY).move_to(pt(0,.4))
    zone=Ellipse(width=1.15*scale,height=2.0*scale,color=GREY,stroke_opacity=.6).move_to(pt(0,.4))
    fp=Line(pt(-.4,-2.13),pt(.4,-2.13),color=YELLOW,stroke_width=14)
    path=route([pt(-1.3,1.5),pt(-1.8,.8),pt(-1.9,-.45),pt(-1.3,-1.7),pt(-.45,-2.08),pt(.65,-2.08)],BLUE,8)
    neuron=Dot(pt(-1.3,1.5),radius=.14,color=BLUE)
    g=VGroup(outer,canal,zone,fp,path,neuron)
    if labels:
        for s,xy,anchor,col in [('dorsal commissural\nneurons',(-4.5,2.65),pt(-1.3,1.5),BLUE),('pia',(3.7,-1.2),pt(1.7,-1.4),GREY),('floor plate',(-1.8,-3.35),pt(0,-2.13),YELLOW),('ventricular zone',(3.65,1.3),pt(.57,.8),TEXT),('central canal',(3.65,.1),pt(.2,.4),TEXT),('commissural path',(3.65,-2.45),pt(.6,-2.08),BLUE)]:
            t=label(s,*xy,col,26); g.add(t,Line(t.get_left() if xy[0]>0 else t.get_bottom(),anchor,color=col,stroke_width=1.5))
    return g
GENES=['unc-6','unc-40','unc-5']
COLS=[YELLOW,TEAL,PURPLE]
RESULTS=[['disrupted','disrupted'],['mainly fails','largely normal'],['largely normal','mainly fails']]
YS=[1.15,-.3,-1.75]
def result(s,x,y):
    t=label(s,x,y,GREY if s=='largely normal' else TEXT,26)
    if s=='largely normal': return t
    return VGroup(RoundedRectangle(width=2.55,height=.68,corner_radius=.12,stroke_width=0,fill_color=AMBER,fill_opacity=.23).move_to(t),t)
def table(n=0,side=False):
    xs=[-4.65,-1.55,2.65] if not side else [-5.2,-3.25,-.5]
    g=VGroup(label('Mutant',xs[0],2.35,size=26),label('Toward\nventral',xs[1],2.35,GREEN,26),label('Away from\nventral',xs[2],2.35,RED,26))
    for i,y in enumerate(YS):
        g.add(label(GENES[i],xs[0],y,COLS[i],28),Line([xs[0]-.8,y-.68,0],[xs[2]+1.4,y-.68,0],color=GREY,stroke_opacity=.35))
        if i<n:
            for j in range(2): g.add(result(RESULTS[i][j],xs[j+1],y))
    return g

def highlight(i,side=False):
    return RoundedRectangle(width=7.9 if side else 11.4,height=1.25,corner_radius=.1,color=COLS[i],fill_color=COLS[i],fill_opacity=.07).move_to([-2.5 if side else -.3,YS[i],0])
def mini_routes(cue=True):
    x=4.45
    sec=section(x,-.1,1.85,cue)
    a=Arrow([x-.65,1.05,0],[x-.65,-1.15,0],buff=0,color=GREEN,stroke_width=8)
    b=Arrow([x+.65,-1.15,0],[x+.65,1.05,0],buff=0,color=RED,stroke_width=8)
    return VGroup(sec,a,b,Dot(a.get_start(),radius=.13,color=BLUE),Dot(b.get_start(),radius=.13,color=BLUE),label('ventral',x,-2.45,YELLOW if cue else TEXT,26),label('dorsal',x,2.15,size=26))
def prediction1():
    return VGroup(heading('Lose the cue: which migrations fail?'),table(),highlight(0),label('Toward, away, or both?',0,-3.12,size=30))
def wandering():
    x=4.45
    a=route([[x-.65,1.05,0],[x-1.15,.35,0],[x-.55,-.2,0],[x-1.1,-1.05,0]],GREEN)
    b=route([[x+.65,-1.15,0],[x+1.15,-.4,0],[x+.55,.25,0],[x+1.1,1.05,0]],RED)
    return VGroup(a,b,Triangle(color=GREEN,fill_color=GREEN,fill_opacity=1).scale(.13).rotate(PI).move_to(a.get_end()),Triangle(color=RED,fill_color=RED,fill_opacity=1).scale(.13).move_to(b.get_end()))
def touch(receptors=False,turned=False,cue=True):
    outline=worm(-.2,5.3)
    band=Line([-4.8,-2.25,0],[4.8,-2.25,0],color=YELLOW,stroke_width=14)
    p=[1.6,1.3,0] if turned else [0,-1.2,0]
    ax=Line([-4.6,-1.2,0],[0,-1.2,0],color=BLUE,stroke_width=8)
    # The dorsal shaft reaches into the cone's rear edge, with no gap.
    turn=route([[0,-1.2,0],[.7,-1.2,0],[1.6,-.5,0],[1.6,1.3,0]],BLUE,8)
    normal=DashedLine([.8,-1.2,0],[4.7,-1.2,0],color=GREY,dash_length=.15)
    return VGroup(outline,band if cue else VGroup(),label('ventral UNC-6',0,-3.2,YELLOW,28) if cue else VGroup(),ax,cone(p).rotate(PI/2,about_point=p) if turned else cone(p),cups(p,PURPLE).rotate(PI/2 if turned else 0,about_point=p) if receptors else VGroup(),turn if turned else VGroup(),label('dorsal',-4.2,1.75,size=26),label('axon',-3,-.65,BLUE,28),normal,label('normal route',3.6,-1.7,GREY,26),VGroup(label('growth cone',3.6,.65,BLUE,28),Line([2.1,.85,0],[2.4,.65,0],color=BLUE)) if turned else label('growth cone',0,-2.0,BLUE,26))
def prediction2():
    return VGroup(touch(True),heading('Which way will the axon grow?').shift(UP*.2),label('Does the new route need UNC-6?',0,2.75,YELLOW,26),label('UNC-5 added',-2,1.15,PURPLE,28))

class S00Title(TitleCard):
    LESSON=LESSON
    TITLE='The Worm Already Knew'
class S01Question(SpokenScene):
    def construct(self):
        s=section(); self.add(s,section_labels(),heading('How can one cue send cells in two directions?'))
        a=Arrow([-.8,1.35,0],[-.8,-1.3,0],color=GREEN,buff=0,stroke_width=10)
        b=Arrow([.8,-1.3,0],[.8,1.35,0],color=RED,buff=0,stroke_width=10)
        self.add(Dot(a.get_start(),color=BLUE,radius=.18),Dot(b.get_start(),color=BLUE,radius=.18))
        self.at('a worm held'); self.play(Indicate(s[1],color=YELLOW),run_time=.6)
        self.at('How can one'); self.play(GrowArrow(a),GrowArrow(b),run_time=.8); self.finish()
class S02Map(SpokenScene):
    def construct(self):
        c=cord(); sec=section(); self.add(c)
        self.at('then switch to'); self.wait(1.2)
        self.play(c.animate.shift(LEFT*15),FadeIn(sec,shift=RIGHT*4),FadeIn(section_labels()),run_time=1.1)
        self.remove(c)
        self.at('There'); self.play(Indicate(sec[1],color=YELLOW),run_time=.5); self.finish()
class S03Transparent(SpokenScene):
    def construct(self):
        w=worm(0,5.3); self.add(w,heading('C. elegans · transparent'))
        internal=RoundedRectangle(width=9.8,height=3.5,corner_radius=1.65,color=BLUE,stroke_opacity=.35,stroke_width=2)
        inside=VGroup(*[Dot([x,-.25,0],radius=.2,color=BLUE) for x in [-3.2,0,3.2]])
        tags=VGroup(*[label(name,x,.45,BLUE,34) for name,x in zip(['ALM','AVM','PLM'],[-3.2,0,3.2])])
        self.at('is transparent'); self.play(FadeIn(internal),FadeIn(inside),w.animate.set_fill(opacity=.015),run_time=.55)
        self.at('Many of its cells'); self.play(FadeIn(tags),run_time=.5)
        self.at('found again')
        # Two broad bodies retain readable cell names and visible inner contours.
        second=VGroup(worm(-1.5,2.65),internal.copy().stretch(.53,1).move_to([0,-1.5,0]),inside.copy().shift(DOWN*1.5),tags.copy().shift(DOWN*1.5))
        self.play(w.animate.stretch(.5,1).move_to([0,1.45,0]),internal.animate.stretch(.53,1).move_to([0,1.45,0]),inside.animate.shift(UP*1.45),tags.animate.shift(UP*1.45),FadeIn(second),run_time=.7); self.finish()
class S04Hedgecock(SpokenScene):
    def construct(self):
        self.add(worm(-.4,4.8),heading('1990 · Hedgecock and colleagues'),sides())
        p=route([[-3.7,-2,0],[-3.7,-.8,0],[-2.7,.5,0],[-2.7,1.4,0]])
        d=Dot(p.get_start(),radius=.2,color=BLUE); self.add(d)
        self.at('followed migrating cells'); self.play(Create(p),MoveAlongPath(d,p),run_time=1.2)
        ax=route([[-.8,-2,0],[.2,-2,0],[1.4,-.5,0],[2,1.4,0],[3.5,1.4,0]])
        self.at('pioneer axons'); self.add(cone(ax.get_start(),.25)); self.play(Create(ax),run_time=.9); self.finish()
class S05Pioneer(SpokenScene):
    def construct(self):
        self.add(worm(-.25,5.5),heading('Pioneer axon'),label('dorsal',-4.1,1.9,size=28),label('ventral',0,-3.3,size=28))
        p=route([[-4.6,-1.35,0],[-2.6,-1.35,0],[-.3,1.1,0],[4.4,1.1,0]],'#A8EDFF',10)
        followers=VGroup(*[p.copy().shift(DOWN*d).set_stroke(BLUE,width=4,opacity=1) for d in [.3,.6,.9]])
        self.at('Pioneer axons'); self.play(Create(p),run_time=.8)
        self.at('the first axons'); self.play(FadeIn(label('pioneer',-3.6,-.7,'#A8EDFF',32)),run_time=.25)
        self.at('to lay down'); self.play(LaggedStart(*[Create(f) for f in followers],lag_ratio=.25),FadeIn(label('later axons follow',2.6,-1.3,BLUE,32)),run_time=.8)
        self.add(followers); self.wait(2.3); self.finish()
class S06Routes(SpokenScene):
    def construct(self):
        self.add(section(r=2.7),section_labels(),heading('Worm cross-section'))
        a=Arrow([-.85,1.45,0],[-.85,-1.35,0],color=GREEN,buff=0,stroke_width=10)
        b=Arrow([.85,-1.35,0],[.85,1.45,0],color=RED,buff=0,stroke_width=10)
        self.at('Some cells move'); self.play(FadeIn(Dot(a.get_start(),radius=.2,color=BLUE)),GrowArrow(a),run_time=.7)
        self.at('Others move away'); self.play(FadeIn(Dot(b.get_start(),radius=.2,color=BLUE)),GrowArrow(b),run_time=.7); self.finish()
class S07Genes(SpokenScene):
    def construct(self):
        self.add(heading('Three mutant genes'),table())
        self.at('The first was'); self.play(FadeIn(highlight(0)),run_time=.4)
        self.at('the gene for'); self.play(FadeIn(label('unc-6: the cue itself',0,-3.15,YELLOW,30)),run_time=.4); self.finish()
class S08Predict(SpokenScene):
    def construct(self):
        p=prediction1(); self.add(*p[:3]); self.at('which migrations should fail'); self.play(FadeIn(p[3]),run_time=.3); self.finish()
class S09Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction1())
        dots=VGroup(*[Dot([x,-3.6,0],radius=.055,color=GREY) for x in [-.4,-.2,0,.2,.4]])
        self.add(dots)
        for d in dots: self.play(d.animate.set_color(YELLOW),run_time=1)
class S10Reveal(SpokenScene):
    def construct(self):
        tab=table(side=True); m=mini_routes(False); self.add(heading('Without UNC-6'),tab,highlight(0,True),m)
        self.at('Both'); self.play(Transform(tab,table(1,True)),run_time=.4)
        self.at('wrong way'); w=wandering(); self.play(FadeOut(m[1]),FadeOut(m[2]),Create(w),run_time=.55)
        self.at('still moved'); self.play(FadeIn(label('Still moving, but misdirected',0,-3.15,BLUE,30)),MoveAlongPath(m[3],w[0]),MoveAlongPath(m[4],w[1]),run_time=.6); self.finish()
class S11Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; m=mini_routes(False)
        self.add(heading('Without UNC-6'),table(1,True),highlight(0,True),m[0],m[5],m[6],wandering(),label('Still moving, but misdirected',0,-3.15,BLUE,30)); self.wait(2.5)
class S12Unc40(SpokenScene):
    def construct(self):
        m=mini_routes(); self.add(heading('unc-40 mutant'),table(1,True),highlight(1,True),m)
        self.at('failed mainly'); self.play(FadeIn(result('mainly fails',-3.25,YS[1])),m[1].animate.set_color(GREY),run_time=.4)
        self.at('Movement away'); self.play(FadeIn(result('largely normal',-.5,YS[1])),Indicate(m[2],color=RED),run_time=.5); self.finish()
class S13Unc5(SpokenScene):
    def construct(self):
        m=mini_routes(); self.add(heading('unc-5 mutant'),table(2,True),highlight(2,True),m)
        self.at('showed the mirror image'); self.play(FadeIn(result('largely normal',-3.25,YS[2])),run_time=.4)
        self.at('failed mainly in movement'); self.play(FadeIn(result('mainly fails',-.5,YS[2])),m[2].animate.set_color(GREY),FadeIn(label('×',5.1,.1,TEXT,40)),run_time=.4); self.finish()
class S14Reading(SpokenScene):
    def construct(self):
        self.add(heading('One cue, two readers'))
        rows=VGroup()
        for y,g,desc,col in zip([1.7,-.15,-2],GENES,['no cue','toward reader','away reader'],COLS):
            rows.add(VGroup(RoundedRectangle(width=11.7,height=1.5,corner_radius=.15,color=col,fill_color=col,fill_opacity=.05).move_to([0,y,0]),label(g,-3.6,y,col,36),label(desc,1.8,y,col,36)))
        self.add(rows)
        self.at('reads toward',lead=.5); self.play(rows[1][0].animate.set_fill(TEAL,.25),run_time=.25)
        self.at('reads away'); self.play(rows[1][0].animate.set_fill(TEAL,.05),rows[2][0].animate.set_fill(PURPLE,.25),run_time=.25); self.wait(2); self.finish()
class S151992(SpokenScene):
    def construct(self):
        self.add(heading('1992'))
        cue=RoundedRectangle(width=2.1,height=4.4,corner_radius=.8,color=YELLOW,fill_color=YELLOW,fill_opacity=.25).rotate(-.55).move_to([-3.4,-.25,0])
        self.at('In'); self.play(FadeIn(cue),run_time=.5)
        self.at('turned out'); self.play(Indicate(cue,color=YELLOW),FadeIn(label('UNC-6',-3.4,2.65,YELLOW,38)),run_time=.4)
        self.at('related protein'); self.play(FadeIn(label('laminin-related\nprotein',-3.4,-3.1,YELLOW,30)),run_time=.4)
        mem=VGroup(*[Line([.1,y,0],[6.1,y,0],color=GREY,stroke_width=10) for y in [-.45,-.05]])
        rec=RoundedRectangle(width=1.7,height=4.7,corner_radius=.4,color=PURPLE,fill_color=PURPLE,fill_opacity=.3).move_to([3.1,-.25,0])
        self.at('turned out to span'); self.play(FadeIn(mem),GrowFromCenter(rec),FadeIn(label('UNC-5',3.1,2.65,PURPLE,38)),FadeIn(label('outside',5.15,1.15,size=30)),FadeIn(label('inside',5.15,-1.6,size=30)),FadeIn(label('membrane',3.1,-3.1,GREY,30)),run_time=.55); self.finish()
class S16Test(SpokenScene):
    def construct(self):
        self.add(heading('Table: gene → direction'))
        c1=np.array([-3.1,-.2,0]); c2=np.array([3.1,-.2,0])
        dials=VGroup(Circle(radius=1.6,color=PURPLE).move_to(c1),Circle(radius=1.6,color=YELLOW).move_to(c2))
        rp=Arrow(c1,c1+[-1.15,0,0],buff=0,color=PURPLE); cp=Arrow(c2,c2+[0,1.2,0],buff=0,color=YELLOW)
        self.add(dials,rp,cp,label('reader',-3.1,-2.8,PURPLE,32),label('cue · fixed',3.1,-2.8,YELLOW,32),label('unc-40',-5.45,-.2,TEAL,26),label('none',-3.1,1.8,size=26),label('unc-5',-.75,-.2,PURPLE,26))
        self.at('change the reader'); self.play(Rotate(rp,-PI/2,about_point=c1),run_time=.5); self.wait(.25); self.play(Rotate(rp,-PI/2,about_point=c1),run_time=.5)
        self.at('leave the'); self.play(Indicate(cp,color=YELLOW),run_time=.4); self.finish()
class S17Touch(SpokenScene):
    def construct(self):
        t=touch(); self.add(t,heading('Worm touch neuron').shift(UP*.2))
        self.at('do not normally carry'); self.play(FadeIn(label('no UNC-5',-1.5,1.3,TEXT,30)),run_time=.4)
        self.at('Their axons'); self.play(Create(DashedVMobject(Arrow([2,-.55,0],[2,1.6,0],color=TEXT,buff=0,stroke_width=7),num_dashes=10)),FadeIn(label('×',2,.55,RED,64)),FadeIn(label('does not grow dorsally',0,2.75,TEXT,34)),run_time=.5); self.finish()
class S18Predict2(SpokenScene):
    def construct(self):
        t=touch(); self.add(t,heading('Which way will the axon grow?').shift(UP*.2))
        self.at('Force them to make'); self.play(FadeIn(cups([0,-1.2,0],PURPLE)),FadeIn(label('UNC-5 added',-2,1.15,PURPLE,28)),run_time=1.2)
        self.at('Which way do'); self.play(Indicate(t[4],color=BLUE),run_time=.4)
        self.at('And does the new'); self.play(FadeIn(label('Does the new route need UNC-6?',0,2.75,YELLOW,26)),run_time=.3); self.finish()
class S19Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction2()); self.wait(5)
class S20Reveal2(SpokenScene):
    def construct(self):
        t=touch(True); self.add(t,heading('1993 · Michel Hamelin and colleagues').shift(UP*.2),label('UNC-5 added',-2,1.15,PURPLE,28))
        self.at('grew dorsally'); end=touch(True,True)
        self.play(Create(end[6]),Transform(t[4],end[4]),Transform(t[5],end[5]),Transform(t[11],end[11]),run_time=.75)
        self.at('away from the'); self.play(FadeIn(label('Dorsal growth · away from UNC-6',0,2.75,RED,28)),run_time=.3); self.finish()
class S21Still(SpokenScene):
    def construct(self):
        t=touch(True,True); self.add(t,heading('The new route still needs UNC-6'))
        self.at('the new route'); end=touch(True,False,False)
        self.play(Uncreate(t[6]),Transform(t[4],end[4]),Transform(t[5],end[5]),Transform(t[11],end[11]),t[1].animate.set_opacity(.1),FadeOut(t[2]),run_time=.6)
        self.add(label('unc-6 mutant · dorsal turn lost',0,-3.1,TEXT,28))
        self.at('still needed'); self.play(FadeIn(label('UNC-5 remains',-2,1.2,PURPLE,28)),run_time=.25); self.wait(3); self.finish()
class S22Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(touch(True,False,False),heading('The new route still needs UNC-6'),label('unc-6 mutant · dorsal turn lost',0,-3.1,size=28),label('UNC-5 remains',-2,1.2,PURPLE,28)); self.wait(2.5)
class S23Meaning(SpokenScene):
    def construct(self):
        self.add(section(r=2.75),label('same cue · ventral UNC-6',0,-3.2,YELLOW,30))
        c=cone([-.6,.2,0],1.45); r=cups([-.6,.2,0],TEAL,1.45)
        a=Arrow([1.8,1.55,0],[1.8,-1.45,0],color=GREEN,buff=0,stroke_width=12)
        tag=label('UNC-40',-4.5,.3,TEAL,36); self.add(c,r,a,tag)
        self.at('It marked the ventral'); self.play(Indicate(self.mobjects[0][1],color=YELLOW),run_time=.4)
        self.at('The receptor set'); self.play(Transform(r,cups([-.6,.2,0],PURPLE,1.45)),Transform(tag,label('UNC-5',-4.5,.3,PURPLE,36)),Transform(a,Arrow([1.8,-1.45,0],[1.8,1.55,0],color=RED,buff=0,stroke_width=12)),run_time=.5); self.wait(2.6); self.finish()
class S24Takeaway(SpokenScene):
    def construct(self):
        c=cord((-3.35,0,0),1.35,False); self.add(c,label('dorsal start',-3.35,3.5,BLUE,30),label('floor plate crossing',-3.35,-3.5,YELLOW,28))
        box=RoundedRectangle(width=5.8,height=5.6,corner_radius=.2,color=TEAL).move_to([3.15,0,0])
        self.add(box,label('2 · Receptors',3.15,2.05,TEAL,38))
        takeaway=label('Changing the receptor\nchanged the answer\nto an unchanged cue.',3.15,-.35,size=36)
        self.at('changing the receptor'); self.play(box.animate.set_fill(TEAL,.15),FadeIn(takeaway),c[4].animate.set_stroke('#A8EDFF',width=12),run_time=.5); self.finish()
class S25End(EndCard):
    def construct(self):
        # The takeaway has landed in the filled box; keep it there through the close.
        c=cord((-3.35,0,0),1.35,False); c[4].set_stroke('#A8EDFF',width=12)
        box=RoundedRectangle(width=5.8,height=5.6,corner_radius=.2,color=TEAL,fill_color=TEAL,fill_opacity=.15).move_to([3.15,0,0])
        self.add(c,label('dorsal start',-3.35,3.5,BLUE,30),label('floor plate crossing',-3.35,-3.5,YELLOW,28),box,label('2 · Receptors',3.15,2.05,TEAL,38),label('Changing the receptor\nchanged the answer\nto an unchanged cue.',3.15,-.35,size=36))
        self.wait(self.narration_s*.55)
        self.play(FadeOut(Group(*self.mobjects)),run_time=.45)
        self.play(FadeIn(label('biochemistrypedia.com',0,0,TEAL,32)),run_time=.35); self.finish()
