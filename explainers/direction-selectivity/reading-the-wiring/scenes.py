"""Reading the Wiring, reviewed animation.
COLOR MAP: PURPLE starburst; BLUE ganglion; ORANGE calcium; GREEN preferred;
RED null/inhibition; YELLOW stimulus/questions; GOLD contacts; GREY unknowns.
Traces are explicit illustrative models, never experimental measurements.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
ORANGE='#F29E4C'

def arr(a,b,color=GREY,w=5):
    return Arrow(a,b,buff=0,color=color,stroke_width=w,tip_length=.2,max_tip_length_to_length_ratio=.4)
def label(txt,pos,color=TEXT,size=26):
    return T(txt,size,color,line_spacing=1.1).move_to(pos)
def heading(txt,color=TEXT): return label(txt,[0,3.35,0],color,30)
def star(c=(-3,0,0),R=2.8,n=4):
    c=np.array(c,float); parts=[Dot(c,radius=.25,color=PURPLE)]
    for a in np.arange(n)*TAU/n:
        d=np.array([np.cos(a),np.sin(a),0]); branch=VGroup(Line(c+.25*d,c+R*d))
        for f,s in ((.45,1),(.72,-1)):
            p=c+R*f*d; branch.add(Line(p,p+.55*np.array([np.cos(a+s*.6),np.sin(a+s*.6),0])))
        parts.append(branch.set_stroke(PURPLE,5))
    return VGroup(*parts)
def gang(c=(3,0,0),r=1.6):
    return VGroup(Circle(radius=r,color=BLUE,fill_color=BLUE,fill_opacity=.08).move_to(c),Dot(c,radius=.3,color=BLUE))
def cellnames(sc=(-3,0,0),gc=None):
    g=VGroup(label('starburst cell',[sc[0]+1.6,sc[1]+2.6,0],PURPLE),Line([sc[0]+.6,sc[1]+2.4,0],[sc[0]+.15,sc[1]+2.1,0],color=PURPLE,stroke_width=2))
    if gc is not None: g.add(label('ganglion cell',[gc[0],gc[1]-.55,0],BLUE,24))
    return g
def directions(x=3,y=2.25,w=2):
    return VGroup(arr([x-w/2,y,0],[x+w/2,y,0],GREEN),label('preferred',[x,y+.4,0],GREEN),arr([x+w/2,-y,0],[x-w/2,-y,0],RED),label('null',[x,-y-.4,0],RED))
def prefs(c=(-3,0,0),r=2.4):
    c=np.array(c,float)
    return VGroup(*[arr(c+.65*d,c+r*d,GREEN) for d in (RIGHT,UP,LEFT,DOWN)])
def soma_question():
    return VGroup(star(),heading('Predict: what does the soma show?',YELLOW),RoundedRectangle(width=5,height=3.8,color=GREY).move_to([3,0,0]),label('soma voltage: ?',[3,0,0],YELLOW,30),cellnames(),label('four branches shown',[-3,-3.25,0],GREY,22))
def wiring_question():
    g=gang((0,0,0),2.4); bs=VGroup()
    for c,d in [((5,1.3,0),LEFT),((-5,-1.3,0),RIGHT),((3,-2.6,0),UP),((-3,2.6,0),DOWN)]:
        c=np.array(c,float); bs.add(VGroup(Dot(c,radius=.2,color=PURPLE),arr(c,c+1.7*d,GREY)))
    return VGroup(g,bs,VGroup(arr([3.7,2.5,0],[5.5,2.5,0],GREEN),label('preferred',[4.6,3,0],GREEN)),label('Which way do the contacting branches point?',[0,-3.35,0],YELLOW,28),label('ganglion cell',[0,-.65,0],BLUE),label('starburst cell\nbranches',[-4.5,-2.1,0],PURPLE))
def field():
    return VGroup(RoundedRectangle(width=10,height=5.4,color=GREY),VGroup(*[gang((x,y,0),.7) for x,y in [(-3,1),(0,-1),(3,.8)]]),label('ganglion cells',[0,-2.3,0],BLUE))
def recon():
    g=gang((0,0,0),2.4); branches=VGroup()
    for y in (-1.6,0,1.6):
        tip=[1.6,y*.75,0]; branches.add(VGroup(Dot([5,y,0],radius=.2,color=PURPLE),arr([5,y,0],tip,PURPLE,7),Dot(tip,radius=.13,color=GOLD)))
    minority=VGroup(arr([-5,-1,0],[-1.8,-.6,0],PURPLE),Dot([-1.8,-.6,0],radius=.12,color=GOLD)).set_opacity(.45)
    return VGroup(g,branches,minority,VGroup(arr([-1,2.85,0],[1,2.85,0],GREEN),label('preferred',[2.2,2.85,0],GREEN),arr([1,-2.85,0],[-1,-2.85,0],RED),label('null',[2.2,-2.85,0],RED)),label('ganglion cell',[0,-.65,0],BLUE),label('starburst cell\nbranches',[4.3,2.25,0],PURPLE),label('a few from\nother directions',[-4.4,-2.05,0],TEXT))
def caveat():
    d=VGroup(Dot([-5,-1.5,0],radius=.3,color=PURPLE),Line([-5,-1.5,0],[-2,1.5,0],color=ORANGE,stroke_width=12))
    return VGroup(d,heading('A limit of the measurement'),label('calcium signal',[-3.7,2.2,0],ORANGE,30),label('?', [0,0,0],YELLOW,64),Circle(radius=.6,color=TEAL).move_to([3,0,0]),label('release at the tip?',[3,-1.2,0],TEAL,30))

class S00Title(TitleCard):
    LESSON='Computing Motion in the Retina'
    TITLE='Reading the Wiring'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',[0,1.4,0],TEAL,26),label(self.LESSON,[0,.7,0],TEXT,28),label(self.TITLE,[0,-.3,0],TEXT,54)); self.finish()
class S01Q(SpokenScene):
    def construct(self):
        c=star(n=8); self.at('A starburst cell'); self.add(c,heading('Reading the Wiring'),cellnames())
        self.at('branches pointing'); self.play(LaggedStart(*[Indicate(p,color=PURPLE) for p in c[1:]],lag_ratio=.05),run_time=.8)
        self.at('Which ones'); self.add(gang((3.4,0,0),2),label('ganglion cell',[3.4,-.65,0],BLUE),label('Which branches inhibit this ganglion cell?',[0,-3.35,0],YELLOW,28))
        qs=VGroup(*[label('?',[-3+3.05*np.cos(a),3.05*np.sin(a),0],YELLOW,28) for a in np.arange(8)*TAU/8]); qs[6].shift(UP*.35+RIGHT*.35); self.play(FadeIn(qs),run_time=.4); self.finish()
class S02Euler(SpokenScene):
    def construct(self):
        c=star(n=8); self.add(c,cellnames()); self.at('In'); self.add(heading('Euler, Detwiler and Denk · 2002'))
        self.at('imaged calcium'); self.add(label('two-photon\ncalcium imaging',[3,.7,0],ORANGE,32)); self.play(c[1].animate.set_stroke(ORANGE,9),run_time=.4)
        glow=Dot([-1,0,0],radius=.3,color=ORANGE); self.play(FadeIn(glow),run_time=.3); self.play(Indicate(glow,color=ORANGE,scale_factor=1.8),run_time=.7)
        self.at('in rabbit'); self.add(label('isolated rabbit retina',[3,-1.5,0],TEXT,28)); self.finish()
class S03Out(SpokenScene):
    def construct(self):
        self.at('A dendrite'); self.add(heading('One branch: outward versus inward'))
        self.add(Dot([-4,-2.8,0],radius=.3,color=PURPLE),Line([-4,-2.8,0],[-4,2.7,0],color=PURPLE,stroke_width=8),label('cell body',[-5.4,-2.8,0],PURPLE))
        self.add(arr([-3.7,-1.8,0],[-3.7,1.8,0],GREEN),label('outward',[-2.6,1.9,0],GREEN),arr([-4.3,1.8,0],[-4.3,-1.8,0],RED),label('inward',[-5.3,1.9,0],RED))
        ax=Axes(x_range=[0,5,1],y_range=[0,1.7,.5],x_length=6,y_length=5.2,tips=False,axis_config={'color':GREY}).move_to([2.3,-.1,0])
        self.add(ax,label('calcium response (relative)',[2.3,2.9,0],ORANGE),label('time',[2.3,-3,0]),label('0',ax.c2p(0,0)+LEFT*.35))
        # Illustrative pulse: lesson's directional gain times a stated common transient.
        pulse=lambda t: np.exp(-((t-2.5)/.75)**2)
        out=ax.plot(lambda t:(1+.515)*pulse(t),x_range=[0,5,.03],color=GREEN)
        inn=ax.plot(lambda t:(1-.515)*pulse(t),x_range=[0,5,.03],color=RED)
        self.play(Create(out),Create(inn),run_time=.8)
        self.add(label('outward',[4.7,1.8,0],GREEN),label('inward',[4.7,-.65,0],RED),label('illustrative model · normalized',[2,-3.45,0],TEXT,24))
        self.at('motion outward'); self.play(Indicate(out,scale_factor=1.03),run_time=.4)
        self.at('than for motion'); self.play(Indicate(inn,scale_factor=1.03),run_time=.4); self.finish()
class S04Predict(SpokenScene):
    def construct(self):
        q=soma_question(); self.at('Predict'); self.add(q)
        self.at('The cell body'); self.play(Indicate(q[0][0],color=PURPLE,scale_factor=1.5),run_time=.6); self.at('What should'); self.finish()
class S05Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(soma_question()); self.wait(5)
class S06Reveal(SpokenScene):
    def construct(self):
        c=star(); self.add(c,cellnames(),heading('Little somatic preference'))
        ax=Axes(x_range=[0,5,1],y_range=[0,1,1],x_length=4.3,y_length=3.5,tips=False,axis_config={'color':GREY}).move_to([3,.2,0])
        self.at('Little preference'); self.add(ax,label('voltage (relative)',[3,2.5,0]),label('time',[3,-2,0]),label('rightward = leftward',[3,-2.6,0],TEXT))
        self.add(ax.plot(lambda t:.5,x_range=[0,5],color=GREEN,stroke_width=7),DashedLine(ax.c2p(0,.5),ax.c2p(5,.5),color=RED,stroke_width=4))
        a=prefs(); self.add(a,label("green arrows: each branch’s preferred (outward) direction",[0,-3.4,0],GREEN,26))
        self.at('Motion outward'); spot=Dot([-2.5,0,0],radius=.16,color=YELLOW); self.add(spot); self.play(spot.animate.move_to([-.2,0,0]),c[1].animate.set_stroke(ORANGE,8),run_time=1)
        self.at('runs inward'); self.remove(a[2]); self.add(arr([-5.6,.2,0],[-3.6,.2,0],RED),label('inward',[-4.6,-.5,0],RED)); self.play(c[3].animate.set_opacity(.4),run_time=.4); self.finish()
class S07Cancel(SpokenScene):
    def construct(self):
        c=star(); a=prefs(); cols=[GREEN,ORANGE,PURPLE,BLUE]
        for p,ar,col in zip(c[1:],a,cols): p.set_color(col); ar.set_color(col)
        self.at('A soma'); self.add(c,a,cellnames(),heading('Add the four branch preferences'))
        target=VGroup(); p=np.array([1,-1.5,0])
        for d,col in zip((RIGHT,UP,LEFT,DOWN),cols): target.add(arr(p,p+3*d,col)); p=p+3*d
        self.play(Transform(a,target),c.animate.set_opacity(.5),run_time=1)
        self.at('would see them cancel'); self.add(label('sum ≈ 0 in this simple model',[3,-2.3,0],TEXT,26))
        self.at('The measured somatic voltage'); self.add(label('soma: little preference under the conditions tested',[0,-3.4,0],TEXT,26)); self.finish()
class S08Unit(SpokenScene):
    def construct(self):
        c=star((0,0,0),2.8); self.add(c,cellnames((0,0,0))); self.at('So the branch'); self.play(c[1].animate.set_stroke(ORANGE,8),run_time=.5)
        self.at('is the unit'); self.add(heading('The branch is the unit')); self.at('Each branch'); a=prefs((0,0,0),2.6); self.play(LaggedStart(*[GrowArrow(x) for x in a],lag_ratio=.12),run_time=.9); self.at('set by where'); self.play(Indicate(a),run_time=.5); self.finish()
class S09Caveat(SpokenScene):
    def construct(self):
        self.at('One limit here'); self.add(caveat()); self.at('A calcium signal'); self.add(label('calcium is a proxy, not release',[0,-2.8,0],TEXT,30)); self.at('not transmitter release'); self.finish()
class S10Beat(Scene):
    def construct(self): self.camera.background_color=BG; self.add(caveat(),label('calcium is a proxy, not release',[0,-2.8,0],TEXT,30)); self.wait(2)
class S11Select(SpokenScene):
    def construct(self):
        c=star((-4.3,0,0),1.8); g=gang((.6,0,0),1.15); self.at('In that simple sum'); self.add(c,g,VGroup(label('starburst cell',[-4.7,-2.7,0],PURPLE,24),label('ganglion cell',[.6,-.55,0],BLUE,24)),heading('Equal input from all branches'),VGroup(arr([2.5,2.35,0],[3.7,2.35,0],GREEN),label('preferred',[3.1,2.8,0],GREEN,24),arr([6.1,2.35,0],[4.9,2.35,0],RED),label('null',[5.5,2.8,0],RED,24)))
        # Four separate routes, ordered around the cell boundary; none shares an entry.
        tips=[p[0].get_end() for p in c[1:]]; paths=VGroup()
        routes=[([-1.9,.15,0],[-1.1,.15,0],[-.55,0,0]),
                ([-3.2,1.8,0],[-1.3,1.3,0],[0, .982,0]),
                ([-6.65,3.3,0],[2,3.3,0],[1.4,.826,0]),
                ([-3.6,-2.5,0],[-.4,-2,0],[.4,-1.133,0])]
        for tip,(control1,control2,dest) in zip(tips,routes):
            curve=CubicBezier(tip,control1,control2,dest,color=RED,stroke_width=3)
            paths.add(VGroup(curve,arr(curve.point_from_proportion(.93),dest,RED,3)))
        self.at('input taken equally'); self.play(Create(paths),run_time=.7)
        self.at('carries no direction signal'); base=-1.7
        hs=[sum(1+.515*np.cos(m-a) for a in np.arange(4)*PI/2)/2 for m in (PI,0)]
        self.add(Line([2.5,base,0],[6.1,base,0],color=GREY),label('inhibition',[4.3,1.1,0],RED))
        for x,h,txt in zip((3.2,5.2),hs,('leftward','rightward')):
            self.add(Rectangle(width=.8,height=h,color=RED,fill_color=RED,fill_opacity=.6).move_to([x,base+h/2,0]),label(txt+'\nmotion',[x,-2.3,0],TEXT,26))
        self.at('So the wiring'); self.add(label('The wiring should be selective',[0,-3.4,0],YELLOW,30)); self.finish()
class S12Fried(SpokenScene):
    def construct(self):
        self.at('Paired recordings'); self.add(heading('Fried, Münch and Werblin · 2002'),label('paired recordings · rabbit',[0,2.75,0],TEXT))
        c=np.array([-3,0,0]); self.add(Dot(c,radius=.28,color=PURPLE),Line([-5.6,0,0],[-.4,0,0],color=PURPLE,stroke_width=6),VGroup(label('starburst cell',[-3,-.6,0],PURPLE),label('ganglion cell',[3.6,.75,0],BLUE,24)),gang((3.6,0,0),1.25),directions(3.6,1.8,2))
        self.at('Branches pointing'); self.add(arr([-3.3,.12,0],[-5.6,.12,0],PURPLE,7),arr([-2.7,.12,0],[-.4,.12,0],PURPLE,7))
        self.at('null direction'); self.add(label('null-pointing',[-4.7,.65,0],RED),label('Branch direction: soma → tip, relative to the null arrow',[0,-3.2,0],TEXT,24))
        self.at('inhibited it'); path=CubicBezier([-5.6,0,0],[-5.6,-2,0],[1,-2.3,0],[2.5,-.55,0],color=RED,stroke_width=5)
        self.play(Create(path),Create(Line([2.3,-.4,0],[2.7,-.7,0],color=RED,stroke_width=7)),run_time=.5); self.add(label('inhibitory current',[-2,-2.1,0],RED))
        self.at('preferred pointing'); self.add(label('preferred-pointing',[-.8,.7,0],GREEN))
        self.at('did not'); self.add(DashedLine([-.4,0,0],[2.4,.5,0],color=GREY),label('×',[1,.3,0],TEXT,40),label('no inhibitory current',[.3,1.35,0],TEXT,26)); self.finish()
class S13Briggman(SpokenScene):
    def construct(self):
        f=field(); self.at('In'); self.add(f,heading('Briggman, Helmstaedter and Denk · 2011'))
        self.at('read the wiring'); self.play(Indicate(f[1],color=BLUE),run_time=.6)
        self.at('in mouse retina'); self.add(label('mouse retina',[3.7,2.3,0],TEXT)); self.finish()
class S14Image(SpokenScene):
    def construct(self):
        f=field(); self.at('First'); self.add(f,heading('Calcium imaging · moving bars'))
        b=Rectangle(width=.3,height=4.9,color=YELLOW,fill_color=YELLOW,fill_opacity=.5).move_to([-4.8,0,0]); self.at('imaged calcium'); self.add(b)
        # Two full 3 s sweeps. Response is model gain times bar overlap.
        positions=[(-3,1),(0,-1),(3,.8)]; cols=[GREEN,TEAL,PURPLE]
        for sign in (1,-1):
            start=-4.8*sign; end=4.8*sign
            def sweep(mob,alpha):
                bx=start+(end-start)*alpha; mob.move_to([bx,0,0])
                for i,(cell,(x,y)) in enumerate(zip(f[1],positions)):
                    gain=(1+.515*np.cos((0 if sign==1 else PI)-(0 if i<2 else PI)))/1.515
                    response=gain*np.exp(-((bx-x)/.65)**2)
                    cell[0].set_fill(ORANGE,opacity=.08+.65*response)
                    cell[1].set_color(interpolate_color(ManimColor(BLUE),ManimColor(ORANGE),float(response)))
            self.play(UpdateFromAlphaFunc(b,sweep),run_time=3,rate_func=linear)
            for i in ((0,1) if sign==1 else (2,)):
                x,y=positions[i]; d=RIGHT if sign==1 else LEFT
                self.play(GrowArrow(arr([x,y,0],np.array([x,y,0])+1.1*d,cols[i])),run_time=.2)
        self.remove(b); self.add(label('preferred directions',[0,-3.3,0],TEXT,28)); self.finish()
class S15Em(SpokenScene):
    def construct(self):
        self.at('Then they cut'); self.add(heading('Same tissue · electron microscopy'))
        stack=VGroup(); outlines=VGroup()
        for k in range(5):
            off=np.array([k*.18,k*.2,0]); sec=VGroup(Rectangle(width=5.5,height=3.7,color=GREY,fill_color=BG,fill_opacity=.7).shift(off))
            for x,y in [(-1.7,.7),(.2,-.8),(1.7,.6)]: sec.add(Ellipse(width=.85,height=.55,color=BLUE,stroke_opacity=.55).move_to(np.array([x,y,0])+off))
            stack.add(sec); outlines.add(Ellipse(width=.85,height=.55,color=BLUE,stroke_width=6).move_to(np.array([.2,-.8,0])+off))
        stack.shift(LEFT*2.6); outlines.shift(LEFT*2.6)
        self.add(stack,label('serial sections',[-2.3,-2.6,0],TEXT),label('trace ganglion cell',[3.5,2.6,0],BLUE))
        self.at('electron microscopy'); self.wait(max(0,2-self.elapsed())); self.play(LaggedStart(*[Create(o) for o in outlines],lag_ratio=.3),run_time=2)
        self.at('traced the cells')
        # Mixed directions, no preferred/null arrow: the next Predict stays unanswered.
        # Oblique view: matching contours at different depths become a volume.
        r=VGroup(*[Ellipse(width=2.8,height=1.4,color=BLUE,stroke_opacity=.55).move_to([3.5,z,0]) for z in (-.35,0,.35)],
                 Line([2.1,-.35,0],[2.1,.35,0],color=BLUE),Line([4.9,-.35,0],[4.9,.35,0],color=BLUE),
                 Dot([3.5,0,0],radius=.23,color=BLUE))
        contacts=VGroup()
        for a in (0,2.2,4.4):
            d=np.array([np.cos(a),np.sin(a),0]); p=np.array([3.5,0,0])+1.2*d
            r.add(Line(p+1.25*d,p,color=PURPLE,stroke_width=6)); contacts.add(Dot(p,radius=.12,color=GOLD))
        self.play(ReplacementTransform(outlines.copy(),r),run_time=.55); self.add(label('same traced cell · 3D reconstruction',[3.5,-2.8,0],TEXT,22))
        self.at('and their contacts'); self.play(FadeIn(contacts),FadeIn(label('starburst branches',[4.6,1.6,0],PURPLE,24)),run_time=.45); self.wait(2); self.finish()
class S16Predict(SpokenScene):
    def construct(self):
        q=wiring_question(); self.at('Predict'); self.add(q[0],q[1],q[4],q[5],heading('Predict',YELLOW)); self.at('prefers rightward'); self.play(FadeIn(q[2]),run_time=.4); self.at('Which way should'); self.play(FadeIn(q[3]),run_time=.4); self.finish()
class S17Pause(Scene):
    def construct(self): self.camera.background_color=BG; self.add(wiring_question(),heading('Predict',YELLOW)); self.wait(5)
class S18Reveal(SpokenScene):
    def construct(self):
        self.at('Most starburst input'); R=3; c=np.array([0,-.05,0])
        rings=VGroup(*[Circle(radius=r,color=GREY,stroke_opacity=.6).move_to(c) for r in (1,2,3)])
        self.add(rings,Line(c+LEFT*R,c+RIGHT*R,color=GREY),Line(c+UP*R,c+DOWN*R,color=GREY),heading('Directions of contacting branches'))
        self.add(label('null (180°)',[-4.3,-.05,0],RED,28),label('preferred (0°)',[4.4,-.05,0],GREEN,28),label('number of contacts\n(relative rings)',[4.5,-1.9,0],TEXT,26),label('illustrative sketch of the lesson’s model, not measured counts',[0,-3.45,0],TEXT,24))
        # A qualitative orientation histogram, explicitly not measured counts.
        # Smooth null-centred illustrative density allows weaker other-direction contacts.
        angles=np.arange(24)*TAU/24; radii=.35+2.3*((1-np.cos(angles))/2)**2
        rays=VGroup(*[Line(c,c+r*np.array([np.cos(a),np.sin(a),0]),color=PURPLE,stroke_width=6) for a,r in zip(angles,radii)])
        self.at('branches pointing'); self.play(Create(rays),run_time=.5)
        self.at('roughly left'); self.add(label('most contacts',[-4.4,1.6,0],PURPLE,28),Line([-3,1.4,0],[-2,1,0],color=PURPLE)); self.at('in the null direction'); self.finish()

def branch_comparison():
    g=gang((-1.4,-.5,0),1.9); soma=Dot([4,1.8,0],radius=.28,color=PURPLE)
    actual=np.array([.1,-1.45,0]); miss=np.array([.3,.35,0])
    branch=VGroup(Line([4,1.8,0],[3,-1.45,0],color=PURPLE,stroke_width=6),arr([3,-1.45,0],actual,PURPLE,7))
    rulea=VGroup(DashedLine([4,1.8,0],[-1.4,-.5,0],color=GREY,stroke_opacity=.65),arr([4,1.8,0],miss,GREY,4),Circle(radius=.16,color=GREY).move_to(miss),label('A: soma line',[3,2.65,0],GREY))
    ruleb=VGroup(label('B: branch direction',[3,-2.25,0],PURPLE),label('true contact',[-.2,-2.7,0],GOLD),Line([-.2,-2.4,0],actual,color=GOLD))
    return VGroup(g,soma,branch,Dot(actual,radius=.15,color=GOLD),rulea,ruleb,VGroup(label('starburst cell',[5,.65,0],PURPLE),Line([4.8,.95,0],[4.2,1.65,0],color=PURPLE),label('ganglion cell',[-1.4,-1.1,0],BLUE)),VGroup(arr([-3,2.4,0],[-1,2.4,0],GREEN),label('preferred',[-2,2.8,0],GREEN),arr([-3.8,-2.35,0],[-5.8,-2.35,0],RED),label('null',[-4.8,-2.8,0],RED)))
class S19Branch(SpokenScene):
    def construct(self):
        c=branch_comparison(); h=heading('Two predictions · one true contact'); self.at('and the direction'); self.add(c,h,label('one example',[4.5,-3.2,0],GREY,22))
        self.at('individual branch'); self.play(Indicate(c[2],color=PURPLE),run_time=.5)
        self.at('predicted contact better'); self.play(Transform(h,label('Branch direction predicts better across traced contacts',[0,3.35,0],PURPLE,28)),Indicate(c[3],color=GOLD,scale_factor=1.5),run_time=.5)
        self.at('than the line'); self.play(c[4].animate.set_opacity(.3),run_time=.4); self.finish()
class S20Beat(Scene):
    def construct(self):
        self.camera.background_color=BG; c=branch_comparison(); c[4].set_opacity(.3); self.add(c,label('Branch direction predicts better across traced contacts',[0,3.35,0],PURPLE,28),label('one example',[4.5,-3.2,0],GREY,22)); self.wait(2)
class S21Limit(SpokenScene):
    def construct(self):
        r=recon(); self.at('One limit'); self.add(r,heading('What a contact tells us'))
        self.at('A contact shows wiring'); self.play(Indicate(r[1],color=GOLD,scale_factor=1.03),run_time=.5)
        self.at('not synaptic strength'); self.add(label('contacts show wiring, not strength',[0,-3.5,0],TEXT,28)); self.finish()
class S22Take(SpokenScene):
    def construct(self):
        r=recon(); self.at('So the picture holds'); self.add(r)
        for b in r[1]: b[1].set_opacity(.45)
        self.at('Most starburst contacts'); self.play(LaggedStart(*[Indicate(b[2],color=GOLD,scale_factor=1.5) for b in r[1]],lag_ratio=.2),run_time=.8)
        self.at('branches pointing roughly'); self.play(LaggedStart(*[b[1].animate.set_opacity(1).set_stroke(PURPLE,9) for b in r[1]],lag_ratio=.35),run_time=1.4); self.finish()
class S23End(EndCard):
    LINE='In mouse retina, most starburst contacts come from branches\npointing roughly in the cell’s null direction.'
    def construct(self):
        self.add(label('ON-OFF direction-selective ganglion cells',[0,1.8,0],BLUE,28))
        line=T(self.LINE,32,TEXT,font=TITLE_FONT,line_spacing=1.3); fit(line,max_w=12); self.play(FadeIn(line),run_time=.5)
        self.add(label('biochemistrypedia.com',[0,-2,0],TEAL,26)); self.finish()
