"""What the Bulb Sends — revised schematic animation.
COLOR MAP: receptor identity = RED, BLUE, GOLD, GREEN throughout;
TEAL = cortical response / odour A; GOLD = odour B / recruitment ring;
BLUE/YELLOW = mitral/tufted output; PURPLE = inhibition; ORANGE = timing;
GREY = anatomy; RED cross = omitted relay. Geometry is schematic.
The pair coincidence rule computes all overlap counts; no invented traces.
"""
import numpy as np
from itertools import combinations
from bp_style import *
ORANGE='#F29E4C'
PURPLE='#B58CD9'
RC=[RED,BLUE,GOLD,GREEN]
A={0,1,4,5}; B={1,2,5}; MORE_B=A|B
RECRUITED={2,3}  # New receptor types: gold and green, never second copies.
# 40 spatially dispersed cells; 4 responders (10%) for A in every sheet.
POSITIONS=[(-2.05+(i%5)*1.02+.09*np.sin(i*3),2.0-(i//5)*.57) for i in range(40)]
ACTIVE=(2,11,24,37)
# Pair listeners under the same A and B sets used in s05. Each odour
# drives its paired-input listeners; sharing increases from one to four.
PAIRS=[(8,9)]*40
for i,pair in {2:(0,1),11:(0,4),24:(1,5),37:(4,5),5:(1,2),19:(2,5)}.items(): PAIRS[i]=pair

def responders(s):
    return {i for i,p in enumerate(PAIRS) if set(p)<=s}

def label(s,y=3.15,size=32,color=TEXT):
    return T(s,size,color).move_to([0,y,0])

def row(y=.25,typed=True,active=(),x=0,step=1.9,radius=.78):
    return VGroup(*[Circle(radius=radius,color=RC[i%4],stroke_width=4,
      fill_color=RC[i%4],fill_opacity=.78 if i in active else .08)
      .move_to([x+(i-2.5)*step,y,0]) for i in range(6)])

def sheet(x=3.4,y=0,title='piriform cortex'):
    border=RoundedRectangle(width=5.3,height=5.15,corner_radius=.22,color=GREY,stroke_width=2).move_to([x,y,0])
    cells=VGroup(*[Dot([x+a,y+b,0],radius=.105,color=GREY).set_opacity(.42) for a,b in POSITIONS])
    return VGroup(border,cells,T(title,28,GREY).move_to([x,y+3.05,0]))

def activity(cells,indices=ACTIVE):
    return [d.animate.set_color(TEAL if i in indices else GREY).set_opacity(1 if i in indices else .42) for i,d in enumerate(cells)]

def map_pair(lit=False):
    b=row(x=-3.5,y=.4,step=.77,radius=.31,active=A if lit else ())
    b.add(Ellipse(width=5.3,height=5.15,color=GREY,stroke_opacity=.55).move_to([-3.5,0,0]))
    c=sheet(3.4)
    a=Arrow([- .8,.4,0],[.65,.4,0],buff=.06,color=TEAL)
    n=T('bulb glomeruli',28,GREY).move_to([-3.5,3.05,0])
    return b,c,a,n

def bulb_outline(y=.25,height=4.6):
    return Ellipse(width=12.6,height=height,color=GREY,stroke_opacity=.45)

def prediction():
    b=row(y=.9,active=A)
    q=label('Same set, or more?',-3.1,36)
    n=label('Odour A',3.1,32,TEAL)
    tr=Line([-4,-1.15,0],[4,-1.15,0],color=GREY,stroke_width=5)
    k=Dot([-4,-1.15,0],radius=.18,color=TEAL)
    e=VGroup(*[VGroup(Line([x,-1.0,0],[x,-1.3,0],color=GREY),T(t,26,GREY).move_to([x,-1.75,0])) for x,t in [(-4,'low'),(0,'mid'),(4,'high')]],label('concentration',-2.4,26,GREY))
    return b,q,n,tr,k,e

def output_pair():
    g=VGroup(*[Circle(radius=.7,color=TEAL if i==0 else GREEN,fill_opacity=.25,fill_color=TEAL if i==0 else GREEN).move_to([x,2.2,0]) for i,x in enumerate([-2.2,3.6])])
    points=[(-3.5,-.9),(-.8,.45),(3.6,-.9)]
    c=VGroup(*[Circle(radius=.43,color=co,fill_color=co,fill_opacity=.25).move_to([x,y,0]) for (x,y),co in zip(points,[BLUE,YELLOW,GREY])])
    d=VGroup(*[Line(cc.get_top(),g[0 if i<2 else 1].get_bottom()+RIGHT*(.22 if i==1 else -.22 if i==0 else 0),color=TEAL if i<2 else GREEN,stroke_width=5) for i,cc in enumerate(c)])
    a=VGroup(*[Arrow(cc.get_bottom(),[cc.get_x()+.5,-2.7,0],buff=0,color=co,stroke_width=4) for cc,co in zip(c,[BLUE,YELLOW,GREY])])
    n=VGroup(T('mitral',28,BLUE).move_to([-4.75,-.85,0]),T('tufted',28,YELLOW).move_to([.6,.45,0]),T('other cell',26,GREY).move_to([5,-.85,0]))
    # Glomerular layer and labels are present from the first frame.
    band=RoundedRectangle(width=12.1,height=1.75,corner_radius=.25,color=GREY,stroke_opacity=.45).move_to([0,2.2,0])
    n.add(band,T('glomerulus',24,TEAL).move_to([-2.2,3.28,0]),T('different glomerulus',24,GREEN).move_to([3.6,3.28,0]))
    # Enlarge the anatomy together so dendrites still meet their knots.
    VGroup(g,c,d,a,n).scale(1.08,about_point=ORIGIN).shift(DOWN*.25)
    return g,c,d,a,n

def puzzles(n):
    lines=['Scatter: one glomerulus together?', 'Similarity: chemistry kept?', 'Meaning: acquire learned meaning?', 'Stability: stay put week to week?']
    out=VGroup()
    for i,s in enumerate(lines[:n]):
        y=1.9-i*1.55; co=TEAL if i==n-1 else GREY
        txt=T(str(i+1)+'   '+s,36,co).move_to([.65,y,0])
        if i==0: icon=VGroup(*[Dot([-.4+.32*j,.22*np.sin(j*2),0],radius=.08,color=co) for j in range(4)])
        elif i==1: icon=VGroup(Circle(radius=.3,color=co).shift(LEFT*.2),Circle(radius=.3,color=co).shift(RIGHT*.2))
        elif i==2: icon=VGroup(Circle(radius=.3,color=co),Line([-.17,-.4,0],[.17,-.4,0],color=co),Arrow([-.65,.1,0],[-.35,.1,0],buff=0,color=co))
        else: icon=VGroup(*[Dot([-.4+.25*j,.15*np.sin(j*2),0],radius=.05+.02*j,color=co) for j in range(4)],Arrow([-.5,-.4,0],[.5,-.4,0],buff=0,color=co))
        icon.move_to([-5.65,y,0]); out.add(VGroup(icon,txt))
    return out

def detector():
    points=[(-4.7,1.5),(-2.7,.65),(-4.5,-1.25),(-2.1,-1.3)]
    g=VGroup(*[Circle(radius=.47,color=RC[i],fill_color=RC[i],fill_opacity=.15).move_to([x,y,0]) for i,(x,y) in enumerate(points)])
    n=Circle(radius=.73,color=TEAL,fill_color=TEAL,fill_opacity=.12).move_to([3.8,.1,0])
    links=VGroup(*[Line(gg.get_right(),n.get_left(),color=RC[i],stroke_width=4,stroke_opacity=.85) for i,gg in enumerate(g)])
    outline=Ellipse(width=5.7,height=4.9,color=GREY,stroke_opacity=.5).move_to([-3.4,.1,0])
    cap=VGroup(outline,T('its glomerular inputs',28,GREY).move_to([-3.4,2.95,0]),T('piriform neuron',28,TEAL).move_to([3.8,1.4,0]),label('Simple model',3.65,28,GREY))
    return g,n,links,cap

class S00Title(TitleCard):
    LESSON='From Glomeruli to Piriform Cortex'
    TITLE='What the Bulb Sends'

class S01Question(SpokenScene):
    def construct(self):
        b,c,a,n=map_pair()
        self.at('Your nose')
        self.play(FadeIn(b),run_time=.6)
        self.at('orderly map')
        self.play(FadeIn(n),run_time=.4)
        self.at('and the cortex')
        self.play(GrowArrow(a),FadeIn(c),run_time=.5)
        self.play(*activity(c[1]),run_time=.4)
        self.at('So what does')
        self.play(FadeIn(label('What does the cortex keep?',-3.05,34)),run_time=.5)
        self.finish()

class S02Molecules(SpokenScene):
    def construct(self):
        membrane=Rectangle(width=11.8,height=.2,color=GREY,fill_opacity=.25).move_to([0,.4,0])
        xs=[-4.5,-2.7,-.9,.9,2.7,4.5]
        cells=VGroup(*[VGroup(Line([x,.4,0],[x,-1.65,0],color=RC[i%4],stroke_width=5),Circle(radius=.32,color=RC[i%4],fill_color=RC[i%4],fill_opacity=.15).move_to([x,-1.9,0]),Square(side_length=.32,color=RC[i%4]).move_to([x,.7,0])) for i,x in enumerate(xs)])
        mol=VGroup(*[Dot([x,2.4,0],radius=.16,color=GREY) for x in [-4.5,-.9,2.7]])
        ml=T('odour molecule',28,GREY).move_to([-2.5,2.6,0])
        rl=T('receptor',28,GREY).move_to([4.7,1.65,0])
        self.add(membrane,cells,mol,label('Olfactory epithelium',3.3,30))
        leader=always_redraw(lambda: Line(ml.get_left()+LEFT*.18,mol[0].get_right()+RIGHT*.12,color=GREY))
        self.at('molecules')
        self.play(FadeIn(ml),Create(leader),FadeIn(rl),Create(Line(rl.get_bottom()+DOWN*.12,cells[5][2].get_top(),color=GREY)),run_time=.3)
        self.at('binding',lead=0)
        self.play(*[m.animate.move_to([x+.3,1.65,0]) for m,x in zip(mol,[-4.5,-.9,2.7])],run_time=.6)
        self.play(*[m.animate.move_to([x,1,0]) for m,x in zip(mol,[-4.5,-.9,2.7])],run_time=.5)
        self.play(*[cells[i][1].animate.set_fill(RC[i%4],.9) for i in (0,2,4)],run_time=.3)
        self.at('Each receptor neuron')
        self.play(FadeIn(label('One receptor type per neuron',-3,32)),run_time=.4)
        self.finish()

class S03Converge(SpokenScene):
    def construct(self):
        neurons=VGroup(); paths=VGroup(); gl=VGroup()
        for i,co in enumerate(RC):
            x=-4.5+i*3
            g=Circle(radius=.65,color=co,fill_color=co,fill_opacity=.3).move_to([x,1.9,0]); gl.add(g)
            for j in range(3):
                xx=x+(j-1)*.75
                n=Dot([xx,-2.35+.2*(j%2),0],radius=.22,color=co); neurons.add(n)
                paths.add(CubicBezier(n.get_top(),[xx,-.6,0],[x,.35,0],g.get_bottom(),color=co,stroke_width=4))
        bulb=Ellipse(width=12.4,height=2.8,color=GREY,stroke_opacity=.45).move_to([0,1.7,0])
        bulbname=label('Olfactory bulb',3.4,30,GREY)
        self.add(bulb,bulbname,neurons,label('Receptor neurons',-3.15,28,GREY))
        self.at('send their axons')
        self.play(Create(paths),run_time=.85)
        self.at('same small knot')
        self.play(FadeIn(gl),Transform(bulbname,label('Glomerulus',3.4,34,TEAL)),run_time=.45)
        self.at('That knot')
        self.play(Indicate(gl,scale_factor=1.08),run_time=.5)
        self.finish()

class S04TwoPerBulb(SpokenScene):
    def construct(self):
        bulb=Ellipse(width=11.5,height=5.3,color=GREY)
        dots=VGroup(*[Circle(radius=.75,color=GOLD,fill_color=GOLD,fill_opacity=.65).move_to([x,0,0]) for x in [-4,4]])
        tag=label('one receptor type',1.6,32,GOLD)
        leaders=VGroup(*[Line(tag.get_bottom()+RIGHT*x*.15,d.get_top(),color=GOLD) for x,d in zip([-1,1],dots)])
        self.add(bulb,label('Mouse olfactory bulb',3.3,32,GREY))
        self.at('each receptor type')
        self.play(FadeIn(dots),FadeIn(tag),Create(leaders),run_time=.5)
        self.at('in each bulb')
        self.play(FadeIn(label('Mice: usually two per bulb',-3.25,32,GOLD)),run_time=.4)
        self.finish()

class S05Set(SpokenScene):
    def construct(self):
        b=row(); name=label('Odour A',3.1,34,TEAL)
        self.add(bulb_outline(),b,name)
        self.at('some receptor types')
        self.play(*[g.animate.set_fill(RC[i%4],.8 if i in A else .08) for i,g in enumerate(b)],run_time=.6)
        self.at('so it activates')
        self.play(FadeIn(label('A set of glomeruli',-2.9,34)),run_time=.4)
        self.at('a set of')
        self.play(Transform(name,label('Odour B',3.1,34,GOLD)),*[g.animate.set_fill(RC[i%4],.8 if i in B else .08) for i,g in enumerate(b)],run_time=.65)
        self.finish()

class S06PredictConc(SpokenScene):
    def construct(self):
        b,q,n,tr,k,e=prediction()
        self.at('Here is a question')
        self.play(FadeIn(b),FadeIn(n),run_time=.5)
        self.at('Raise the concentration')
        self.play(Create(tr),FadeIn(k),FadeIn(e),run_time=.6)
        self.at('the same glomeruli')
        self.play(FadeIn(q),run_time=.6)
        self.finish()

class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(*prediction())
        self.wait(5)

class S08Conc(SpokenScene):
    def construct(self):
        b,q,n,tr,k,e=prediction()
        # Concentration starts from the A set carried from the question.
        self.add(b,n,tr,k,e,label('Characteristic at a given concentration',2.25,28,TEAL))
        rings=VGroup(*[Circle(radius=.9,color=GOLD,stroke_width=5).move_to(b[i]) for i in sorted(RECRUITED)])
        self.at('Usually more')
        self.play(Indicate(k,scale_factor=1.3),run_time=.4)
        self.at('higher concentrations')
        self.play(k.animate.move_to([0,-1.15,0]),run_time=.6)
        self.at('recruit extra glomeruli')
        self.play(*[b[i].animate.set_fill(RC[i%4],.8) for i in sorted(RECRUITED)],Create(rings),run_time=.65)
        self.at('though this can')
        self.play(k.animate.move_to([4,-1.15,0]),FadeIn(label('Same set at mid and high: recruitment levels off',-3.1,28,GREY)),run_time=.8)
        self.at('So the set')
        self.play(Indicate(e[0],scale_factor=1.05),run_time=.5)
        self.finish()

class S09IdentityMap(SpokenScene):
    def construct(self):
        b=row(active=range(6))
        tags=VGroup(*[T('R'+str(i%4+1),32,RC[i%4]).move_to(g.get_center()+DOWN*1.2) for i,g in enumerate(b)])
        self.add(bulb_outline(),b,tags,label('Map of receptor identity',3.1,36,TEAL))
        self.at('glomerulus sits')
        pointer=Arrow([-4.75,-2.8,0],[-4.75,-1.25,0],color=GREY,buff=.05)
        self.play(GrowArrow(pointer),FadeIn(label('Position = which receptor',-3.25,30)),run_time=.45)
        self.at('tells you which')
        self.play(pointer.animate.shift(RIGHT*3.8),run_time=.8)
        self.finish()

class S10NotChemical(SpokenScene):
    def construct(self):
        b=row(y=-.25)
        tags=VGroup(T('molecule 1',28,GREY).move_to([-4.75,2.2,0]),T('molecule 2',28,GREY).move_to([4.75,2.2,0]))
        alike=VGroup(Line([-3,2.2,0],[3,2.2,0],color=GREY),label('alike',2.65,28,GREY),label('two similar molecules',3.45,30))
        arr=VGroup(*[Arrow(t.get_bottom(),g.get_top(),color=GREY,buff=.08) for t,g in zip(tags,[b[0],b[5]])])
        dim=VGroup(Line([-4.75,-1.8,0],[4.75,-1.8,0],color=GREY),*[Line([x,-1.65,0],[x,-1.95,0],color=GREY) for x in [-4.75,4.75]],label('far apart',-2.25,30,GREY))
        self.add(b,tags,alike,label('Not a fine chemical map',-3.15,34))
        self.at('coarsely related')
        self.play(Create(arr),*[b[i].animate.set_fill(RC[i%4],.8) for i in A],Create(dim),run_time=.65)
        self.finish()

class S11OutputCells(SpokenScene):
    def construct(self):
        g,c,d,a,n=output_pair()
        self.add(g,c,n)
        self.at('carry the pattern out')
        axname=T('axon',28,BLUE).move_to([-5,-2.25,0])
        self.play(Create(a),FadeIn(axname),run_time=.5)
        self.at('Each sends')
        dname=T('primary dendrite',28,TEAL).move_to([.3,1.35,0])
        self.play(Create(d),FadeIn(dname),run_time=.55)
        self.at('one glomerulus')
        self.play(FadeIn(label('One main dendrite per cell',3.65,28)),run_time=.4)
        self.finish()

class S12Sisters(SpokenScene):
    def construct(self):
        g,c,d,a,n=output_pair()
        self.add(g,c,d,a,n,label('Sisters: one shared input',3.65,28,TEAL))
        contrast=T('different input',28,GREEN).move_to([5.1,1.1,0])
        self.at('Cells that send')
        self.play(Indicate(VGroup(d[0],d[1]),color=TEAL,scale_factor=1.03),run_time=.6)
        self.at('are called sister')
        self.play(FadeIn(contrast),run_time=.45)
        self.at('They share')
        self.play(g[0].animate.set_fill(TEAL,.9),*[c[i].animate.set_fill(TEAL,.8).set_stroke(TEAL) for i in (0,1)],run_time=.65)
        self.finish()

class S13Interneurons(SpokenScene):
    def construct(self):
        g,c,d,a,n=output_pair()
        # Keep the tufted label above its lateral dendrite.
        n[1].shift(UP*.6)
        # Two clean horizontal lateral dendrites, separated by depth.
        lateral=VGroup(Line(c[0].get_right(),[1,c[0].get_y(),0],color=BLUE,stroke_width=5),Line(c[1].get_right(),[2,c[1].get_y(),0],color=YELLOW,stroke_width=5))
        pg=Circle(radius=.3,color=PURPLE,fill_color=PURPLE,fill_opacity=.5).move_to([-4.3,2.2,0])
        pgl=T('periglomerular cell',26,PURPLE).move_to([-4.8,1.55,0])
        pgcontact=VGroup(Line(pg.get_right(),g[0].get_left(),color=PURPLE,stroke_width=4),Line([-2.9,1.95,0],[-2.9,2.45,0],color=PURPLE,stroke_width=5))
        gran=Circle(radius=.32,color=PURPLE,fill_color=PURPLE,fill_opacity=.55).move_to([1.5,-2.35,0])
        gd=VGroup(Line(gran.get_top(),[-.1,c[0].get_y(),0],color=PURPLE,stroke_width=4),Line(gran.get_top(),[1.2,c[1].get_y(),0],color=PURPLE,stroke_width=4),Line([-.35,c[0].get_y(),0],[.15,c[0].get_y(),0],color=PURPLE,stroke_width=7),Line([.95,c[1].get_y(),0],[1.45,c[1].get_y(),0],color=PURPLE,stroke_width=7))
        gl=T('granule cell',28,PURPLE).move_to([3.6,-2.3,0]); no=T('no axon',28,PURPLE).move_to([3.6,-3.15,0])
        self.add(g,c,d,n,pg,pgcontact,pgl)
        self.at('cells work')
        self.play(Indicate(pg,color=PURPLE),run_time=.5)
        self.at('Granule cells')
        self.play(FadeIn(gran),FadeIn(gl),Create(lateral),Create(gd),run_time=.6)
        self.at('have no axons')
        self.play(FadeIn(no),Create(Line(no.get_left()+LEFT*.22,gran.get_bottom(),color=PURPLE)),run_time=.45)
        self.finish()

class S14ToCortex(SpokenScene):
    def construct(self):
        b,c,a,n=map_pair()
        self.add(b,n)
        origins=[[-2.8,-.7,0],[-2.4,-1.45,0],[-3.4,-1.8,0]]
        colors=[BLUE,YELLOW,TEAL]
        cells=VGroup(*[Dot(p,radius=.17,color=co) for p,co in zip(origins,colors)])
        axons=VGroup(*[CubicBezier(p,[-.5,p[1]-1,0],[-.3,1.4-i*.5,0],[2,1.4-i*.7,0],color=co,stroke_width=4) for i,(p,co) in enumerate(zip(origins,colors))])
        cellnames=VGroup(T('mitral',26,BLUE).move_to([-4,-.7,0]),T('tufted',26,YELLOW).move_to([-4,-1.45,0]))
        self.at('Mitral and tufted axons')
        self.play(FadeIn(cells),FadeIn(cellnames),Create(axons),run_time=.7)
        self.at('run on to')
        self.play(FadeIn(c),run_time=.5)
        self.at('the main olfactory')
        self.play(FadeIn(label('Main olfactory area of cortex',-3.25,28,GREY)),run_time=.4)
        box=chip('thalamus',GREY,26).move_to([0,3.15,0])
        cross=VGroup(Line([-.3,2.2,0],[.3,2.55,0],color=RED,stroke_width=4),Line([-.3,2.55,0],[.3,2.2,0],color=RED,stroke_width=4))
        self.at('There is no relay')
        self.play(FadeIn(box),run_time=.25)
        self.play(Create(cross),run_time=.25)
        self.finish()

class S15Scatter(SpokenScene):
    def construct(self):
        b,c,a,n=map_pair(True)
        self.add(b,c,a,n,T('Odour A',30,TEAL).move_to([-3.5,1.65,0]))
        self.at('There the tidy')
        self.play(Indicate(b,scale_factor=1.02),run_time=.5)
        self.at('One odor switches')
        self.play(*activity(c[1]),run_time=.6)
        self.at('scattered across')
        self.play(FadeIn(label('One odour • scattered neurons',-3.3,32,TEAL)),run_time=.4)
        self.finish()

class S16Puzzle1(SpokenScene):
    def construct(self):
        p=puzzles(4).set_color(GREY).set_opacity(.55)
        self.add(p,label('Four puzzles',3.3,36))
        self.at('Does the output')
        self.play(p[0].animate.set_color(TEAL).set_opacity(1),run_time=.5)
        self.finish()

class S17Puzzle2(SpokenScene):
    def construct(self):
        p=puzzles(4).set_color(GREY).set_opacity(.55)
        self.add(p,label('Four puzzles',3.3,36))
        self.at('how can the cortex')
        self.play(p[1].animate.set_color(TEAL).set_opacity(1),run_time=.5)
        self.finish()

class S18Puzzle34(SpokenScene):
    def construct(self):
        p=puzzles(4).set_color(GREY).set_opacity(.55)
        self.add(p,label('Four puzzles',3.3,36))
        self.at('Can a scattered')
        self.play(p[2].animate.set_color(TEAL).set_opacity(1),run_time=.5)
        self.at('pattern stay put')
        self.play(p[2].animate.set_color(GREY).set_opacity(.55),p[3].animate.set_color(TEAL).set_opacity(1),run_time=.5)
        self.finish()

class S19Idea1(SpokenScene):
    def construct(self):
        b,c,a,n=map_pair(True)
        self.add(b,c,n)
        target=c[1][24]
        links=VGroup(*[CubicBezier(b[i].get_bottom(),b[i].get_bottom()+DOWN*1.6,[-.2,-2.1-k*.25,0],target.get_left(),color=RC[i%4],stroke_width=4) for k,i in enumerate((1,5))])
        pin=VGroup(Circle(radius=.24,color=GOLD).move_to(target.get_center()+UP*.65),Line(target.get_center()+UP*.4,target.get_center()+UP*.1,color=GOLD,stroke_width=4))
        self.at('One idea answers')
        self.play(Create(links),target.animate.set_color(TEAL).set_opacity(1),run_time=.5)
        self.at('where a')
        self.play(FadeIn(pin),run_time=.35)
        self.at('tells you little')
        self.play(pin.animate.set_color(GREY).set_opacity(.35),c[0].animate.set_opacity(.2),FadeIn(label('Where it sits tells you little',-3.3,34)),run_time=.55)
        self.finish()

class S20Idea2(SpokenScene):
    def construct(self):
        g,n,links,cap=detector()
        self.add(g,n,links,cap)
        note=VGroup(label('Model inputs and threshold;',-2.9,28,GREY),label('cortical position does not enter this calculation',-3.5,26,GREY))
        self.at('In our simple model')
        self.play(FadeIn(note),run_time=.4)
        self.at('its glomerular inputs')
        self.play(*[gg.animate.set_fill(RC[i],.8) for i,gg in enumerate(g)],run_time=.5)
        th=chip('threshold',TEAL,28).move_to([3.8,-1.2,0])
        self.at('and its threshold')
        self.play(FadeIn(th),Create(Line(n.get_bottom(),th.get_top(),color=TEAL)),run_time=.35)
        self.at('decide its response')
        self.play(n.animate.set_fill(TEAL,.8),run_time=.4)
        self.at('Real tuning also')
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.35)
        real=Circle(radius=.75,color=TEAL,fill_color=TEAL,fill_opacity=.3).move_to([0,1.1,0])
        self.add(real,label('Real tuning also depends on…',3.2,34))
        for phrase,text,co,x in [('input strengths','input strengths',TEAL,-4),('timing','timing',ORANGE,0),('own network','cortical network',GREY,4)]:
            self.at(phrase)
            ch=chip(text,co,28).move_to([x,-1.7,0])
            self.play(FadeIn(ch),GrowArrow(Arrow(ch.get_top(),real.get_bottom(),buff=.1,color=co)),run_time=.4)
        self.finish()

class S21Idea3(SpokenScene):
    def construct(self):
        g,n,links,cap=detector()
        self.add(g,n,links,cap,chip('Example odour active',TEAL,26).move_to([3.8,2.8,0]))
        threshold=3; active={0,1}
        status=label('2 active inputs < threshold 3',-3.2,30,GREY)
        self.at('Each neuron gets')
        self.play(*[g[i].animate.set_fill(RC[i],.8) for i in active],FadeIn(status),run_time=.6)
        self.at('several scattered glomeruli')
        self.play(Indicate(g,scale_factor=1.03),run_time=.45)
        self.at('It fires only')
        active.add(2)
        self.play(g[2].animate.set_fill(RC[2],.8),Transform(status,label('3 active inputs: threshold reached',-3.2,30,TEAL)),run_time=.5)
        self.at('when enough are')
        self.play(n.animate.set_fill(TEAL,.9 if len(active)>=threshold else .1),run_time=.5)
        self.finish()

class S22Idea4(SpokenScene):
    def construct(self):
        top=row(y=1.25,x=-3.5,step=.78,radius=.37,active=A)
        bottom=row(y=-.7,x=-3.5,step=.78,radius=.37,active=B)
        c=sheet(3.4)
        names=VGroup(T('A',30,TEAL).move_to([-6.25,1.25,0]),T('B',30,GOLD).move_to([-6.25,-.7,0]),T('Glomeruli',30,GREY).move_to([-3.5,3.05,0]))
        def colors(bset):
            ra,rb=responders(A),responders(bset)
            return [cell.animate.set_color(TEAL if i in ra else GOLD if i in rb else GREY).set_opacity(1 if i in ra|rb else .42) for i,cell in enumerate(c[1])]
        def shared(bset):
            return VGroup(*[Circle(radius=.2,color=GOLD,stroke_width=3).move_to(c[1][i]) for i in responders(A)&responders(bset)])
        def brackets(bset):
            return VGroup(*[VGroup(Line([top[i].get_x(),.7,0],[top[i].get_x(),-.15,0],color=TEXT,stroke_width=2),Line([top[i].get_x()-.13,.7,0],[top[i].get_x()+.13,.7,0],color=TEXT),Line([top[i].get_x()-.13,-.15,0],[top[i].get_x()+.13,-.15,0],color=TEXT)) for i in A&bset])
        legend=VGroup(Dot([-4.8,-2.7,0],color=TEAL),T('A',28,TEAL).move_to([-4.25,-2.7,0]),Dot([-2.9,-2.7,0],color=GOLD),T('B',28,GOLD).move_to([-2.35,-2.7,0]),Dot([-.95,-2.7,0],color=TEAL),Circle(radius=.2,color=GOLD).move_to([-.95,-2.7,0]),T('both',28).move_to([0,-2.7,0]))
        rings=shared(B); bracket=brackets(B)
        tally=label(f'Brackets: {len(A&B)} shared glomeruli',-3.45,28,GREY)
        self.add(top,bottom,c,names,legend,tally)
        self.play(*colors(B),FadeIn(rings),Create(bracket),run_time=.45)
        self.at('two odors share')
        self.play(*[gg.animate.set_fill(RC[i%4],.8 if i in MORE_B else .08) for i,gg in enumerate(bottom)],Transform(bracket,brackets(MORE_B)),Transform(tally,label(f'Brackets: {len(A&MORE_B)} shared glomeruli',-3.45,28,GREY)),run_time=.65)
        self.at('the more neurons')
        self.play(*colors(MORE_B),Transform(rings,shared(MORE_B)),run_time=.6)
        self.finish()

class S23Idea5(SpokenScene):
    def construct(self):
        # Exact worked-example expectation: every distinct input pair equally likely.
        na=10; ns=6; ra=len(list(combinations(range(na),2))); shared=len(list(combinations(range(ns),2)))
        f_gl=ns/na; f_cx=shared/ra
        self.add(label('With sparse responses • prediction of this model',3.4,28,TEAL),label('Not a rule of all random wiring',-3.45,26,GREY))
        # Carry the same sparse A ensemble as the small contextual panel.
        c=sheet(4.1); c.scale(.62).move_to([4.4,.1,0]); c[2].become(T('A and B responders',24,TEAL).move_to([4.4,1.9,0])); self.add(c)
        self.add(label('Worked example: 10 active glomeruli per odour',2.75,26,GREY))
        for i in ACTIVE: c[1][i].set_color(TEAL).set_opacity(1)
        left=-5.8; width=6.7
        bg=VGroup(*[Rectangle(width=width,height=.6,color=GREY,fill_color=GREY,fill_opacity=.15).move_to([left+width/2,y,0]) for y in [1.35,-.35]])
        bars=VGroup(*[Rectangle(width=width*f_gl,height=.6,color=TEAL,fill_color=TEAL,fill_opacity=.85,stroke_width=0).move_to([left+width*f_gl/2,y,0]) for y in [1.35,-.35]])
        names=VGroup(T('Glomeruli shared by A and B: 60%',28).move_to([-2.45,2.05,0]),T('Responding neurons shared: about 33%',26).move_to([-2.45,.35,0]))
        response_label=T('Responding neurons shared',26).move_to([-2.45,.35,0])
        self.add(bg,bars,names[0],response_label)
        order=VGroup(T('B stays closer to A than C',30,TEAL).move_to([-2.4,-1.55,0]),T('C shares 0 glomeruli → 0 shared responders',26,GREY).move_to([-2.3,-2.25,0]))
        self.at('keeps the order')
        self.play(FadeIn(order),run_time=.5)
        self.at('on average')
        self.play(Indicate(order[0],scale_factor=1.03),run_time=.4)
        self.at('But related odors')
        new=Rectangle(width=width*f_cx,height=.6,color=TEAL,fill_color=TEAL,fill_opacity=.85,stroke_width=0).move_to([left+width*f_cx/2,-.35,0])
        self.play(FadeOut(response_label),run_time=.2)
        self.play(Transform(bars[1],new),FadeIn(names[1]),run_time=.7)
        self.at('than in the bulb')
        self.play(Indicate(bars[1],scale_factor=1.04),run_time=.5)
        self.finish()

class S24Idea6(SpokenScene):
    def construct(self):
        c=sheet(3.4)
        self.add(c,label('Anything tighter? Not this model.',-3.3,32))
        for i in ACTIVE: c[1][i].set_color(TEAL).set_opacity(1)
        subset=[2,11,24,37]
        links=VGroup()
        for k,(i,j) in enumerate(zip(subset,subset[1:]+subset[:1])):
            a=c[1][i].get_center(); b=c[1][j].get_center()
            arc=CurvedArrow(a,b,angle=.6 if k%2 else -.6,color=TEAL,stroke_width=3,tip_length=.22)
            links.add(arc)
        name=T("cortex's own network",30,TEAL).move_to([-3.3,1.5,0])
        leader=Arrow(name.get_right(),[.6,1.2,0],buff=.1,color=TEAL)
        self.at('own network')
        self.play(Create(links),FadeIn(name),GrowArrow(leader),run_time=.6)
        self.at('and experience')
        self.play(FadeIn(chip('experience',GREEN,30).move_to([-3.3,-1.3,0])),run_time=.5)
        self.finish()

class S25Takeaway(SpokenScene):
    def construct(self):
        b,c,a,n=map_pair(True)
        self.add(b,n)
        self.at('a map of')
        self.play(FadeIn(label('A map of receptor identity',-3.25,32,TEAL)),run_time=.5)
        self.at('The rest of this story')
        self.play(GrowArrow(a),FadeIn(c),FadeIn(T('What does the cortex keep?',30).move_to([0,3.6,0])),run_time=.5)
        self.at('what the cortex keeps')
        self.play(*activity(c[1]),run_time=.45)
        self.finish()

class S26End(EndCard):
    LINE='The bulb sends a map of which receptors are active.'
