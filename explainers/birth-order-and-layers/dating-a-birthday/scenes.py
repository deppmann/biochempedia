"""Dating a Birthday.
COLOR MAP: orange earliest/layer 6; yellow layer 5; green layer 4;
blue latest/layers 2/3; pink preplate/subplate; purple progenitors;
teal pulse/date record; grey tissue and neutral neurons; red rejected cue.
Diagrams are schematic; dilution grains are computed as 16 / 2**k.
Timeline windows are qualitative, not measured production intervals.
"""
from bp_style import *
import numpy as np

ORANGE='#F29E4C'
PURPLE='#B58CD9'
PINK='#E58FB4'
COH=[ORANGE,YELLOW,GREEN,BLUE]
LESSON='Birth Order and Fate: Temporal Identity and the Inside-Out Cortex'
CX=-3.9
ROW=[-1.45,-.35,.75,1.85]

def label(text,x=0,y=3.1,size=28,color=TEXT):
    return T(text,size,color).move_to([x,y,0])

def nd(c,x,y,r=.31):
    return Circle(radius=r,stroke_color=c,fill_color=c,fill_opacity=.85).move_to([x,y,0])

def nucleus(x,y,n=16,r=.65,c=TEAL):
    shell=Circle(radius=r,color=c,fill_color=c,fill_opacity=.95)
    grains=VGroup(*[Dot([r*.68*np.sqrt((i+.5)/max(n,1))*np.cos(i*2.39996),r*.68*np.sqrt((i+.5)/max(n,1))*np.sin(i*2.39996),0],radius=r*.065,color=BLACK) for i in range(n)])
    return VGroup(shell,grains).move_to([x,y,0])

def cortex(layers=True):
    g=VGroup(Rectangle(width=3.6,height=6.15,color=GREY).move_to([CX,0,0]),
      Line([CX-1.8,3.075,0],[CX+1.8,3.075,0],color=GREY,stroke_width=4),
      Rectangle(width=3.55,height=.5,stroke_width=0,fill_color=GREY,fill_opacity=.2).move_to([CX,-2.8,0]),
      label('surface',CX,3.45,26),label('white matter',CX,-2.8,26))
    if layers:
        for y,name,c in zip(ROW[::-1]+[-2.25],['layer 2/3','layer 4','layer 5','layer 6','subplate'],COH[::-1]+[PINK]):
            g.add(Line([CX+1.8,y,0],[CX+2,y,0],color=c),label(name,-.97,y,26,c))
    return g

def cohorts():
    return VGroup(*[VGroup(*[nd(c,CX+dx,y) for dx in [-1.05,0,1.05]]) for c,y in zip(COH,ROW)])

def models():
    g=VGroup()
    for x,name in [(-3.25,'Model 1: push'),(3.25,'Model 2: pass')]:
        g.add(Rectangle(width=4.7,height=5.6,color=GREY).move_to([x,-.2,0]),label(name,x,3.35,28),label('surface',x,2.85,26),label('birth zone',x,-2.63,26,PURPLE))
    return g

def prediction(parts=None):
    # Shared timeline on top (E12 pulse -> P21 look); two model boxes below, each with a '?'.
    g=VGroup()
    pulse=label('E12 pulse',-2.2,3.35,32,TEAL); look=label('P21: look',2.2,3.35,32,TEAL)
    arrow=Arrow([-.8,3.35,0],[.8,3.35,0],color=TEAL,buff=0)
    q1=label('?',-3.25,-.55,84); q2=label('?',3.25,-.55,84)
    g.add(pulse,arrow,look)
    for x,name in [(-3.25,'Model 1: push'),(3.25,'Model 2: pass')]:
        g.add(Rectangle(width=4.7,height=4.5,color=GREY).move_to([x,-.85,0]),label(name,x,2.2,28),label('surface',x,1.0,26),label('birth zone',x,-2.8,26,PURPLE))
    g.add(q1,q2,label('Where are the heavily labeled cells?',0,-3.5,28))
    if parts is not None: parts.update(pulse=pulse,arrow=arrow,look=look,q1=q1,q2=q2)
    return g

def overlap_panel():
    g=VGroup(cortex(),label('Pulse day',3.6,2.8,30))
    for k,(c,y) in enumerate(zip(COH,ROW)):
        g.add(Rectangle(width=3.45,height=1.55,stroke_width=0,fill_color=c,fill_opacity=.25).move_to([CX,y,0]),label(['earliest','early','later','latest'][k],3.6,y,28,c))
    g.add(label('Strong tendency; days overlap',0,-3.5,28))
    return g

LAYERS=['layer 2/3','layer 4','layer 5','layer 6','subplate']
YS=[1.8,.8,-.2,-1.2,-2.2]

DOTS=[[(-1.2,.2),(-.9,-.22),(.8,.25),(1.2,-.15)],
      [(-1.0,-.1),(-.75,.25),(.9,-.25),(1.25,.2)],
      [(-1.3,-.2),(-.85,.12),(.75,-.15),(1.05,.26)],
      [(-1.15,.25),(-.95,-.25),(.85,.12),(1.3,-.2)],
      [(-1.25,.05),(-.8,.27),(.95,-.05),(1.2,.22)]]

def evidence(second=False,light=False,dx=0):
    g=VGroup(label('Heavily labeled cells · idealized',0,3.4,30))
    t=VGroup(label('surface ↑',-4.9,2.65,26),label('E12 pulse',-1.9,2.65,28,ORANGE))
    for name,y,v,c in zip(LAYERS,YS,['few','few','many','most','most'],COH[::-1]+[PINK]):
        t.add(label(name,-4.9,y,26,c),RoundedRectangle(width=3.1,height=.82,corner_radius=.08,color=GREY,fill_color=ORANGE,fill_opacity={'few':.07,'many':.25,'most':.45}[v]).move_to([-1.9,y,0]),label(v,-1.9,y,27,ORANGE))
    if second:
        t.add(label('E16 pulse',2,2.65,28,BLUE))
        for y,v in zip(YS,['most','few','few','few','few']):
            t.add(RoundedRectangle(width=3.1,height=.82,corner_radius=.08,color=GREY,fill_color=BLUE,fill_opacity=.45 if v=='most' else .07).move_to([2,y,0]),label(v,2,y,27,BLUE))
    if light:
        for row,y in enumerate(YS):
            for ox,oy in DOTS[row]:
                t.add(Dot([-1.9+ox,y+oy,0],radius=.14,color=GREY).set_opacity(.9))
    g.add(t.shift(RIGHT*dx))
    return g

def dilution(x=0):
    g=VGroup(label('Extra divisions',x-1.2,2.65,26),label('Label · idealized',x+1.9,2.65,26,TEAL))
    for k,word in enumerate(['full','half','quarter','eighth']):
        y=1.65-k*1.27
        g.add(VGroup(label(str(k),x-1.2,y,28),nucleus(x+.6,y,16//2**k,.38),label(word,x+2,y,26,TEAL)))
    return g

def climb(scene,cell,target,run=1.5,grow=1):
    # Gap between the centre and right-hand slots; no collisions with settled cells.
    scene.play(cell.animate.move_to([CX+.53,-1.95,0]),run_time=.2)
    scene.play(cell.animate.set_y(target),run_time=run)
    scene.play(cell.animate.set_x(CX).scale(grow),run_time=.5 if grow!=1 else .25)

class S00Title(TitleCard):
    TITLE='Dating a Birthday'
    LESSON=LESSON
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',0,2.1,26,TEAL),label('Birth Order and Fate',0,1.2,30))
        self.play(FadeIn(label(self.TITLE,0,-.3,52)),Create(Line([-1.5,-1.3,0],[1.5,-1.3,0],color=GOLD)),run_time=.8)
        self.finish()

class S01Q(SpokenScene):
    def construct(self):
        wall=cortex(False); birth=label('birth zones',CX,-2.8,26,PURPLE)
        wall.remove(wall[-1]); cells=cohorts().set_color(GREY)
        targets=[m.get_center().copy() for row in cells for m in row]
        for row in cells:
            for cell in row: cell.set_y(-2.05)
        self.add(wall,birth,cells)
        self.at('then climb'); self.play(*[cell.animate.move_to(pos) for cell,pos in zip([m for row in cells for m in row],targets)],run_time=1.2)
        self.at('So how can'); self.play(Create(Circle(radius=.48,color=TEAL).move_to([CX,ROW[2],0])),FadeIn(label('?',CX+2.2,ROW[2],40,TEAL)),FadeOut(birth),FadeIn(label('When was\nit born?',3.1,.4,44)),run_time=.5)
        self.finish()

class S02Sphase(SpokenScene):
    def construct(self):
        C=np.array([-3.4,.4,0]); R0,R1=2.0,2.7; Rm=(R0+R1)/2
        # Clockwise cycle: S (left) -> G2 (top) -> M (right) -> G1 (bottom).
        starts={'S':135,'G2':45,'M':-45,'G1':-135}
        ring=VGroup(*[AnnularSector(inner_radius=R0,outer_radius=R1,start_angle=a*DEGREES+.03,angle=90*DEGREES-.06,arc_center=C,color=PURPLE,fill_opacity=.25) for a in starts.values()])
        self.add(ring)
        for name,a in starts.items():
            ang=(a+45)*DEGREES
            self.add(label(name,C[0]+(R1+.4)*np.cos(ang),C[1]+(R1+.4)*np.sin(ang),30))
        self.at('last S phase'); self.play(ring[0].animate.set_fill(PURPLE,.95),run_time=.4)
        self.at('when DNA is copied'); self.play(FadeIn(label('DNA copied',C[0],C[1],28)),run_time=.4)
        # The cell token enters at S, then travels clockwise through G2 to M.
        token=nd(PURPLE,C[0]-Rm,C[1],.3)
        self.at('final S phase'); self.play(FadeIn(token,scale=.5),run_time=.4)
        path=Arc(radius=Rm,start_angle=PI,angle=-PI,arc_center=C)   # left -> top -> right
        trail=path.copy().set_color(PURPLE).set_stroke(width=6)
        self.at('cell that divides')
        self.play(MoveAlongPath(token,path),Create(trail),run_time=1.0,rate_func=smooth)
        # Leaves the ring at M, grows and divides.
        big=nd(PURPLE,1.9,C[1],.75)
        self.play(Create(Arrow([C[0]+R1+.8,C[1],0],[1.0,C[1],0],color=PURPLE,buff=0)),ReplacementTransform(token,big),run_time=.4)
        a=nd(PURPLE,3.3,C[1]+.9,.6); b=nd(ORANGE,5.4,C[1]+.9,.6)
        self.add(a)
        self.play(ReplacementTransform(big,VGroup(a,b)),run_time=.6)
        self.add(label('neuron',5.4,C[1]-.2,28,ORANGE),label('Birthday = last S phase before the neuron is made',0,-3.5,27,TEAL))
        self.finish()

class S03Dose(SpokenScene):
    def construct(self):
        body=Ellipse(width=5.3,height=3.3,color=GREY,fill_opacity=.12,fill_color=GREY).move_to([-1,0,0])
        embryos=VGroup(Ellipse(width=2.5,height=1.9,color=PURPLE).move_to([-1,-.2,0]),*[nd(PURPLE,x,y,.22) for x,y in [(-1.6,0),(-.8,.2),(-1.2,-.7)]])
        mouse=VGroup(body,Ellipse(width=1.6,height=1.3,color=GREY).move_to([1.7,.7,0]),Circle(radius=.42,color=GREY).move_to([1.3,1.5,0]),Dot([2,.85,0]),Line([-3.6,-.2,0],[-5.8,-1,0],color=GREY),embryos)
        self.add(mouse,label('embryos',3.8,-1,28,PURPLE),Arrow([2.7,-1,0],[.3,-.3,0],color=PURPLE))
        syringe=VGroup(Rectangle(width=.45,height=1,color=TEAL),Line([0,-.5,0],[0,-1.1,0],color=TEAL)).rotate(-PI/4).move_to([.2,2.5,0])
        self.at('one dose'); self.play(FadeIn(syringe),run_time=.3); self.play(syringe.animate.shift(DOWN*.5+LEFT*.5),run_time=.4)
        self.at('thymidine carrying tritium'); self.play(embryos.animate.set_color(TEAL),Create(Arrow([-.5,1.6,0],[-1,.7,0],color=TEAL)),FadeIn(label('Tritiated thymidine · one pulse',0,-2.6,30,TEAL)),run_time=.6)
        self.at('radioactive form'); self.add(label('tritium: radioactive hydrogen',0,-3.35,26,TEAL)); self.finish()

class S04Dna(SpokenScene):
    def construct(self):
        strip=Rectangle(width=11.8,height=2.7,color=PURPLE,fill_color=PURPLE,fill_opacity=.1).move_to([0,-.3,0])
        cells=VGroup(*[nd(PURPLE,x,-.5,.75) for x in [-4.5,-1.5,1.5,4.5]])
        self.add(strip,cells,label('Thymidine → DNA',0,3,34,TEAL),label('ventricular zone',0,-2.4,28,PURPLE),label('ventricle',0,-3.3,26,GREY))
        self.at('cells copying DNA'); self.add(label('S phase',-4.5,1.4,28,PURPLE),label('S phase',1.5,1.4,28,PURPLE))
        self.at('next hour or so'); self.play(ReplacementTransform(cells[0],nucleus(-4.5,-.5,16,.75)),ReplacementTransform(cells[2],nucleus(1.5,-.5,16,.75)),FadeIn(label('Label available: next hour or so',0,2.1,28,TEAL)),run_time=.6)
        split=VGroup(nd(PURPLE,4.15,-1.4,.43),nd(PURPLE,4.9,-1.4,.43))
        self.play(ReplacementTransform(cells[3],split),Create(Arrow([4.5,-.5,0],[4.5,-1.15,0],buff=.05,color=GREY)),run_time=.6); self.finish()

class S05Halve(SpokenScene):
    def construct(self):
        table=dilution(1.9); parent=nucleus(-4.4,1,32,.75)
        self.add(parent,*table[:2])
        self.at('divides once'); daughter=nucleus(-3.5,-.4,16,.62)
        cycling=nucleus(-5.2,-.4,16,.62)
        self.play(ReplacementTransform(parent,VGroup(cycling,daughter)),Create(Arrow([-4.4,1.4,0],[-3.5,.35,0],color=TEAL)),FadeIn(table[2]),run_time=.65)
        self.at('make a neuron'); self.add(label('neuron',-3.5,-1.45,26,TEAL))
        self.at('Each extra division')
        for k in range(1,4):
            descendant=nucleus(-5.2,-.4,16//2**k,.42)
            branch=Arrow([-5.2,-1.05,0],[-5.2,-1.65,0],color=TEAL,buff=.02)
            self.play(Transform(cycling,nucleus(-5.2,-.4,16//2**k,.62)),TransformFromCopy(cycling,descendant),FadeIn(table[2+k]),run_time=.3)
            self.play(descendant.animate.set_y(-2.1),Create(branch),run_time=.4)
            self.wait(.6)
            self.play(FadeOut(descendant),FadeOut(branch),run_time=.2)
        self.finish()

class S06Heavy(SpokenScene):
    def construct(self):
        table=dilution(-3.8)
        self.add(table,nucleus(3.25,.6,16,1.35),SurroundingRectangle(table[2],color=TEAL,buff=.2))
        self.at('weeks later'); self.add(label('weeks later',3.25,-1.05,30))
        self.at('last DNA copy'); self.add(label('Left the cycle at the first\ndivision after the pulse',3.25,-2.1,26,TEAL))
        self.at('The pulse dates'); self.add(label('A cohort born around the pulse',0,-3.45,28)); self.finish()

class S07Stamp(SpokenScene):
    def construct(self):
        cell=nucleus(-3,.1,0,1.4); stamp=chip('S phase · date recorded',TEAL,28).move_to([-3,2.55,0])
        self.add(cell,stamp)
        self.at('that S phase'); self.play(stamp.animate.set_y(1.3),run_time=.35)
        imprint=RoundedRectangle(width=3.4,height=3.4,corner_radius=.25,stroke_color=TEAL,stroke_width=5,stroke_opacity=.7).move_to([-3,.1,0])
        self.play(Transform(cell,nucleus(-3,.1,16,1.4)),FadeIn(imprint,scale=1.2),stamp.animate.set_y(2.75),run_time=.4)
        self.at('does not tell'); arrow=Arrow([-.7,.1,0],[2.6,.1,0],color=GREY)
        self.add(arrow,label('cell fate',4,.1,30)); self.play(Create(Cross(arrow,stroke_color=RED)),FadeIn(label('A record, not an instruction',0,-2.6,34)),run_time=.5); self.finish()

class S08M1(SpokenScene):
    def construct(self):
        self.add(models()); old=nd(ORANGE,-3.25,-.6,.48); new=nd(BLUE,-3.25,-1.8,.48)
        self.at('In model one'); self.add(old)
        self.at('each new neuron'); self.play(FadeIn(new),run_time=.35)
        self.at('shoves the older'); self.play(old.animate.set_y(.8),new.animate.set_y(-.6),Create(Arrow([-4.4,-.6,0],[-4.4,.8,0],color=GREY)),run_time=1.2); self.finish()

class S09M2(SpokenScene):
    def construct(self):
        self.add(models(),nd(ORANGE,-3.25,.8,.48),nd(BLUE,-3.25,-.6,.48),nd(ORANGE,3.25,-.6,.48))
        new=nd(BLUE,4.45,-1.8,.48); self.add(new)
        self.at('climbs past'); self.play(new.animate.set_y(.8),run_time=1.5)
        self.at('settles above'); self.play(new.animate.set_x(3.25),run_time=.5); self.finish()

class S10Predict(SpokenScene):
    def construct(self):
        p={}; g=prediction(p); self.add(g)
        self.remove(*[p['pulse'],p['arrow'],p['look']])
        self.at('Pulse on embryonic'); self.play(FadeIn(p['pulse']),run_time=.4)
        self.at('then look'); self.play(GrowArrow(p['arrow']),FadeIn(p['look']),run_time=.6)
        self.at('Where does each'); self.play(Indicate(p['q1'],color=TEAL,scale_factor=1.3),run_time=.5); self.play(Indicate(p['q2'],color=TEAL,scale_factor=1.3),run_time=.5); self.finish()

class S11Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction()); self.wait(5)

class S12Reveal(SpokenScene):
    def construct(self):
        self.add(models(),label('orange with grains = E12 heavily labeled',0,-3.45,27,ORANGE))
        a=nucleus(-3.25,-1.7,16,.45); b=nucleus(3.25,-1.7,16,.45,ORANGE); a.set_color(ORANGE); a[1].set_color(BLACK)
        self.add(a,b)
        self.at('nearest the surface')
        olds=VGroup(a)
        for k in range(3):
            new=nd(BLUE,-3.25,-1.7,.4); self.add(new)
            self.play(olds.animate.shift(UP*1.05),new.animate.set_y(-1.5),run_time=.45); olds.add(new)
        self.at('Model two puts')
        for k in range(3):
            new=nd(BLUE,4.4,-1.7,.4); self.add(new)
            self.play(new.animate.set_y(-.6+1.05*k),run_time=.4); self.play(new.animate.set_x(3.25),run_time=.2)
        self.finish()

class S13Angevine(SpokenScene):
    def construct(self):
        self.add(label('Angevine and Sidman · 1961',0,3,34),label('mouse · separate pulse groups',0,2.15,28,GREY),Line([-5,0,0],[5,0,0],color=GREY))
        xs=[-4.5,-2.25,0,2.25,4.5]; cols=[interpolate_color(ManimColor(ORANGE),ManimColor(BLUE),k/4) for k in range(5)]
        for k,x in enumerate(xs):
            self.add(Line([x,-.15,0],[x,.15,0],color=cols[k]),label(f'E{12+k}',x,-.7,28,cols[k]))
        self.add(label('embryonic day',0,-1.5,28,GREY))
        self.at('gave pulses')
        for k,x in enumerate(xs):
            self.play(GrowArrow(Arrow([x,1.35,0],[x,.25,0],color=TEAL)),FadeIn(label('pulse',x,1.65,26,TEAL)),run_time=.4); self.wait(.1)
        self.finish()

class S14Result(SpokenScene):
    def construct(self):
        self.add(cortex()); cs=cohorts()
        self.at('Cells labeled earliest'); self.play(FadeIn(cs[0]),FadeIn(label('earliest → deep',3.6,-1.45,28,ORANGE)),run_time=.5)
        self.at('Cells labeled later')
        for k in range(1,4):
            row=cs[k]; row.move_to([CX,-2.05,0])
            for cell in row: cell.scale(.5)
            self.add(row)
            self.play(*[cs[m].animate.set_fill(opacity=.25).set_stroke(opacity=.3) for m in range(k)],run_time=.1)
            # Whole cohort travels through staggered gaps, then occupies its row.
            self.play(row.animate.shift(RIGHT*.53),run_time=.1)
            self.play(row.animate.set_y(ROW[k]),run_time=.4)
            self.play(row.animate.shift(LEFT*.53),*[cell.animate.scale(2) for cell in row],*[cs[m].animate.set_fill(opacity=.85).set_stroke(opacity=1) for m in range(k)],run_time=.2)
        self.at('near the surface'); self.add(label('later → surface',3.6,1.85,28,BLUE),label('✓ Model 2: pass',3.6,.25,30,GREEN)); self.wait(2); self.finish()

class S15Passed(SpokenScene):
    def construct(self):
        self.add(cortex(),cohorts())
        self.at('passed earlier'); self.play(Indicate(self.mobjects[1][-1],color=BLUE),run_time=.6)
        self.at('strong tendency'); self.play(*[FadeOut(m) for m in list(self.mobjects)],FadeIn(overlap_panel()),run_time=.6); self.finish()

class S16Hold(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(overlap_panel()); self.wait(2.5)

class S17Sig(SpokenScene):
    def construct(self):
        self.add(evidence(dx=3))
        self.at('mostly in layers'); self.play(Create(Rectangle(width=3.25,height=1.87,color=ORANGE).move_to([1.1,-.7,0])),run_time=.5); self.finish()

class S18Sig2(SpokenScene):
    def construct(self):
        a=evidence(dx=3); self.add(a)
        self.at('From an embryonic'); self.play(ReplacementTransform(a,evidence(True)),run_time=.5)
        self.at('mostly in layers'); self.play(Create(Rectangle(width=3.25,height=.94,color=BLUE).move_to([2,1.8,0])),run_time=.5); self.finish()

class S19Light(SpokenScene):
    def construct(self):
        p=evidence(True); self.add(p)
        self.at('Lightly labeled cells'); self.play(ReplacementTransform(p,evidence(True,True)),run_time=.6)
        self.at('Born later'); self.add(label('lightly labeled: born after the pulse',0,-3.45,28,GREY)); self.finish()

class S20Rakic(SpokenScene):
    def construct(self):
        self.add(cortex(),label('Rakic · 1974',3.55,3.1,30),label('rhesus monkey\nvisual cortex',3.55,2.2,28))
        # Schematic side view: occipital pole is the posterior end, highlighted blue.
        pts=[[1.3,.1,0],[1.5,1,0],[2.5,1.4,0],[4,1.25,0],[5.4,.5,0],[5.7,-.4,0],[4.7,-1.1,0],[3.4,-.95,0],[2.7,-.5,0],[1.3,.1,0]]
        outline=VMobject(color=GREY,fill_color=GREY,fill_opacity=.12).set_points_smoothly(pts)
        pole=Ellipse(width=1.1,height=1.5,color=BLUE,fill_color=BLUE,fill_opacity=.4).move_to([5.12,-.1,0])
        self.add(outline,pole,Arrow([4,-2.15,0],[5.1,-.8,0],color=BLUE),label('occipital pole',3.8,-2.5,26,BLUE))
        self.at('same order')
        for c,y in zip(COH,ROW):
            self.add(Rectangle(width=3.45,height=.78,color=c,fill_color=c,fill_opacity=.5).move_to([CX,y,0]))
        self.finish()

class S21Mouse(SpokenScene):
    def construct(self):
        self.add(cortex(),cohorts(),label('mouse',3.6,3.15,30))
        # Equal qualitative window widths; stagger is illustrative, not fitted data.
        x0,x1=.8,6.15
        self.add(Line([x0,-2.45,0],[x1,-2.45,0],color=GREY))
        for k in range(7):
            x=x0+(x1-x0)*k/6
            self.add(Line([x,-2.35,0],[x,-2.55,0],color=GREY),label(str(11+k),x,-2.95,26))
        self.add(label('embryonic day',3.5,-3.5,26))
        bars=VGroup()
        for i,(name,c,start) in enumerate([('subplate',PINK,0),('layer 6',ORANGE,.9),('layer 5',YELLOW,1.8),('layer 4',GREEN,2.7),('layer 2/3',BLUE,3.35)]):
            y=-1.7+i*.8; x=x0+start
            bars.add(VGroup(Line([x,y,0],[x+2,y,0],color=c,stroke_width=14),label(name,x+1,y+.3,26,c)))
        self.at('about six embryonic days'); self.play(FadeIn(bars),run_time=.6)
        self.at('Subplate and layer'); self.play(Indicate(bars[0],color=PINK),Indicate(bars[1],color=ORANGE),run_time=.4)
        self.at('upper layers last'); self.play(Indicate(bars[-1],color=BLUE),run_time=.4)
        self.add(label('approximate; classes overlap',3.45,2.5,26,GREY)); self.wait(2); self.finish()

class S22Io(SpokenScene):
    def construct(self):
        cs=cohorts().set_opacity(.18); cs[-1].remove(cs[-1][1]); runner=nd(BLUE,CX-2.25,-2.05,.20)
        self.add(cortex(),cs,runner,label('later wave',3.5,-1.8,30,BLUE))
        self.at('passes the neurons'); self.play(cs[0].animate.set_opacity(1),run_time=.25)
        self.play(runner.animate.move_to([CX+.53,-1.95,0]),run_time=.3)
        self.play(runner.animate.set_y(.15),cs[1].animate.set_opacity(1),run_time=.7)
        self.play(runner.animate.set_y(1.3),cs[2].animate.set_opacity(1),run_time=.7)
        self.at('settles above'); self.play(runner.animate.set_y(1.85),cs[3].animate.set_opacity(1),run_time=.4); self.play(runner.animate.set_x(CX).scale(1.55),run_time=.5)
        self.wait(1)
        self.add(label('Layer 6 first\n↓\nLayer 2/3 last',3.5,.8,30)); self.wait(1.5); self.finish()

class S23Except(SpokenScene):
    def construct(self):
        wall=cortex(); wall.remove(*wall[-2:]); self.add(wall); sheet=Rectangle(width=3.45,height=.42,color=PINK,fill_color=PINK,fill_opacity=.65).move_to([CX,.2,0]); self.add(sheet,label('preplate: born first',3.5,2.7,28,PINK))
        self.at('preplate cells'); bottom=sheet.copy(); self.add(bottom)
        plate=Rectangle(width=3.4,height=.2,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([CX,.2,0]); self.add(plate)
        self.play(sheet.animate.set_y(2.7),bottom.animate.set_y(-2.25),plate.animate.stretch_to_fit_height(4.3).move_to([CX,.2,0]),run_time=1.3)
        self.add(cohorts())
        self.at('at the top'); self.add(label('marginal zone',3.5,1.8,28,PINK),Arrow([1.8,1.8,0],[-2.1,2.7,0],color=PINK))
        self.at('at the bottom'); self.add(label('subplate',3.5,-2.25,28,PINK),Arrow([2,-2.25,0],[-2.1,-2.25,0],color=PINK))
        self.at('Earlier means deeper'); self.add(label('Earlier → deeper',3.5,.5,30))
        self.at('only inside'); self.add(label('within the\ncortical plate',3.5,-.6,28)); self.finish()

class S24Retina(SpokenScene):
    def construct(self):
        self.add(cortex(),cohorts(),label('neocortex',CX,-3.5,28))
        panel=Rectangle(width=4.5,height=5.8,color=GREY).move_to([3.5,0,0])
        self.at('The retina'); self.add(panel,label('retina',3.5,3.35,30))
        for i in range(3):
            y=1.7-i*1.1
            self.add(Rectangle(width=4.3,height=.7,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([3.5,y,0]))
        self.at('birth order too'); self.add(Arrow([1.6,2.3,0],[5.3,2.3,0],color=TEAL),label('birth order',3.5,2.7,26,TEAL))
        for k,(c,y) in enumerate(zip([PURPLE,TEAL,PINK],[1.7,.6,-.5])):
            self.add(nd(c,2.1,y,.22),label(['cell type A','cell type B','cell type C'][k],3.85,y,26,c))
        self.at('another way'); a=Arrow([2.0,-2.55,0],[2.0,-1.35,0],color=GREY,buff=0); self.add(a,Cross(a,stroke_color=RED),label('not by passing',4.05,-1.95,26),label('Birth order biases type',3.5,-3.35,26)); self.wait(3); self.finish()

class S25Take(SpokenScene):
    def construct(self):
        cs=cohorts(); cs[-1].remove(cs[-1][1]); self.add(cortex(),cs)
        # A true compact table in the upper-right corner.
        table=VGroup(Rectangle(width=4.3,height=2.8,color=GREY).move_to([4,1.55,0]),label('Extra divisions | label',4,2.65,26,GREY))
        for k,v in enumerate(['full','half','quarter','eighth']):
            table.add(label(f'{k}                 {v}',4,2.1-k*.52,26,TEAL))
        self.add(table)
        self.at('a thymidine pulse'); self.play(FadeIn(label('A pulse dates\na birthday',3.65,-.65,32,TEAL)),run_time=.5)
        runner=nd(BLUE,CX-2.25,-2.05,.20)
        self.at('later born neurons'); self.add(runner)
        self.at('pass earlier ones'); climb(self,runner,1.85,1,grow=1.55)
        self.at('settle above'); self.wait(1.0)
        self.add(label('Later-born neurons\npass earlier ones\nto settle above them',3.65,-2.1,28)); self.wait(2); self.finish()

class S26End(EndCard):
    LINE='A pulse dates birth; later-born neurons pass earlier ones.'
    def construct(self):
        self.add(label('A pulse dates birth;',0,.8,40),label('later-born neurons pass earlier ones.',0,-.25,36),label('biochemistrypedia.com',0,-1.5,26,TEAL)); self.finish()
