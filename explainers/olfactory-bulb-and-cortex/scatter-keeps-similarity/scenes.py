"""Chapter 3. COLOR MAP: GOLD odour A, BLUE odour B, GREEN odour C;
TEAL inputs/cortical activity; white labels; GREY structure. No molecular art.
Response bars are illustrative. Pair counts are exact combinations. Scatter
points are exact multivariate hypergeometric conditional probabilities.
"""
from bp_style import *
import numpy as np
from itertools import combinations
from math import comb
from functools import lru_cache
A, B, C = GOLD, BLUE, GREEN
LABEL = TEXT


def text(s, x=0, y=0, size=28, color=TEXT):
    return (Paragraph(*s.split('\n'),alignment='center',font=FONT,font_size=size,color=color) if '\n' in s else T(s,size,color)).move_to([x,y,0])


def head(s):
    return text(s, y=3.25, size=32)


def panel(w,h,x,y):
    return RoundedRectangle(width=w,height=h,corner_radius=.25,color=GREY,stroke_width=2).move_to([x,y,0])


VALUES_A=[1,0,.25,.8,0,.6,.9,0]
VALUES_B=[.8,0,.5,0,0,.9,.6,.3]


def population(values=None,center=False):
    # 36 recorded cells; first eight correspond to the numbered response rows.
    cx=0 if center else -3.15
    cells=VGroup()
    nums=VGroup()
    for i in range(36):
        x=cx-2.25+(i%6)*.9; y=2.1-(i//6)*.9
        v=0 if values is None else (values[i] if i<8 else values[(i*3)%8])
        cells.add(Circle(radius=.28,color=TEAL if v else GREY,fill_color=TEAL,
                         fill_opacity=v).move_to([x,y,0]))
        if i<8:
            nums.add(text(str(i+1),x,y,26))
    return VGroup(panel(5.75,5.9,cx,-.2),cells,nums,text('piriform neurons',cx,2.95,28))


def column(values,x,color,label):
    rows=VGroup()
    for i,v in enumerate(values):
        y=2.05-i*.64
        bg=Rectangle(width=1.25,height=.34,color=GREY,stroke_width=1.5).move_to([x,y,0])
        bar=Rectangle(width=max(.012,1.25*v),height=.32,stroke_width=0,fill_color=color,fill_opacity=1)
        bar.move_to([x-.625+bar.width/2,y,0])
        rows.add(VGroup(bg,bar,text(str(i+1),x-.95,y,26),text(f'{v:g}',x+1.05,y,26,color)))
    return VGroup(rows,text(label,x,2.9,30,color))


def pair_graph(shared=False,x=-2.9,r=2.55):
    pts=[np.array([x+r*np.cos(PI/2+i*TAU/10),r*np.sin(PI/2+i*TAU/10),0]) for i in range(10)]
    lines=VGroup(*[Line(pts[i],pts[j],color=B if shared and i<6 and j<6 else (GREY if shared else A),
                           stroke_width=3 if shared and i<6 and j<6 else 1.7,
                           stroke_opacity=1 if shared and i<6 and j<6 else (.3 if shared else .65)) for i,j in combinations(range(10),2)])
    nodes=VGroup(*[Circle(radius=.23,color=B if shared and i<6 else A,fill_color=B if shared and i<6 else A,
                             fill_opacity=1).move_to(p) for i,p in enumerate(pts)])
    return VGroup(lines,nodes)


def odours(include_c=False,include_b=True):
    rows=VGroup()
    cases=[('A',A,set(range(10))),('B (related ester)',B,set(range(6))|set(range(10,14)))]
    if include_c: cases.append(('C (unrelated amine)',C,set(range(14,24))))
    for j,(name,col,ids) in enumerate(cases):
        if j==1 and not include_b: continue
        y=1.65-j*1.85
        dots=VGroup(*[Circle(radius=.19,color=col if i in ids else GREY,fill_color=col,
                          fill_opacity=1 if i in ids else 0).move_to([-5.75+i*.5,y,0]) for i in range(24)])
        rings=VGroup(*[Circle(radius=.26,color=A,stroke_width=3).move_to(dots[i]) for i in range(6)]) if j==1 else VGroup()
        rows.add(VGroup(text(name,-3.75,y+.65,28,col),dots,rings))
    return rows


def prediction():
    return VGroup(head('How much overlap survives?'),
        panel(5.6,4.7,-3.1,0),panel(5.6,4.7,3.1,0),
        text('shared glomeruli',-3.1,1.65,30),text('60%',-3.1,.15,76,A),text('6 of 10',-3.1,-1.3,30,A),
        text('shared neurons',3.1,1.65,30),text('?',3.1,.15,90,TEAL),text('also respond to B',3.1,-1.3,28),
        text('Among neurons responding to A',y=-3.05,size=28))


def ranking():
    out=VGroup(head('Two-input toy: overlap of responses'))
    # Common zero and a genuine 0–60% scale, not arbitrary decorative bars.
    for y,label,v,col in [(1.8,'shared glomeruli',.6,A),(-.1,'A to B neurons',1/3,B),(-2,'A to C neurons',0,C)]:
        out.add(text(label,-3.95,y+.55,28,col))
        out.add(Line([-5.8,y-.25,0],[4.8,y-.25,0],color=GREY))
        if v: out.add(Rectangle(width=10.6*v/.6,height=.48,stroke_width=0,fill_color=col,fill_opacity=.9).move_to([-5.8+5.3*v/.6,y,0]))
        else: out.add(Line([-5.8,y-.25,0],[-5.8,y+.25,0],color=C,stroke_width=5))
        out.add(text('60%' if v==.6 else ('33%' if v else '0%'),5.45,y,32,col))
    return out


def neuron(x,y,lit=True,w=1.5,h=1.4):
    return RoundedRectangle(width=w,height=h,corner_radius=.35,color=TEAL,fill_color=TEAL,
                            fill_opacity=.5 if lit else .04).move_to([x,y,0])


def position_wiring(shift=-2):
    gl=VGroup(*[Circle(radius=.32,color=TEAL,fill_color=TEAL,fill_opacity=.9).move_to([x,2,0]) for x in [-3,3]])
    cell=neuron(shift,-1,True,2,1.7)
    links=VGroup(*[Line(g.get_bottom(),cell.get_top()+RIGHT*(i-.5)*.6,color=TEAL,stroke_width=4) for i,g in enumerate(gl)])
    return VGroup(gl,links,cell)


@lru_cache(None)
def conditional_overlap(shared):
    groups=(shared,100-shared,100-shared,800+shared)
    den=sum(comb(100,k)*comb(900,20-k) for k in range(5,21))
    num=0
    for h in range(min(shared,20)+1):
        for a in range(min(groups[1],20-h)+1):
            if h+a<5: continue
            for b in range(min(groups[2],20-h-a)+1):
                d=20-h-a-b
                if h+b>=5 and d<=groups[3]:
                    num+=comb(groups[0],h)*comb(groups[1],a)*comb(groups[2],b)*comb(groups[3],d)
    return num/den


def model_plot(points=True):
    ax=Axes(x_range=[0,1,.2],y_range=[0,1,.2],x_length=8.3,y_length=5.0,
            axis_config={'color':TEXT,'include_tip':False}).move_to([-.1,.15,0])
    ticks=VGroup(*[text(f'{v:g}',*(ax.c2p(v,0)[:2]+[0,-.28]),26) for v in [0,.2,.4,.6,.8,1]],
        *[text(f'{v:g}',*(ax.c2p(0,v)[:2]+[-.38,0]),26) for v in [.2,.4,.6,.8,1]])
    diag=Line(ax.c2p(0,0),ax.c2p(1,1),color=GREY,stroke_width=2)
    dots=VGroup(*[Dot(ax.c2p(s/100,conditional_overlap(s)),radius=.1,color=TEAL) for s in range(0,101,10)])
    labels=VGroup(text("Share of A’s responders that also respond to B",y=3.45,size=29),
        text('shared glomeruli',0,-3.05,28,A),text('shared neurons',-5.45,.1,28,TEAL).rotate(PI/2),
        text('100 of 1,000 active; 20 inputs per neuron; fires at 5 or more',y=-3.56,size=26),
        text('no loss',1.6,2.15,26),text('schematic,\nnot data',5.15,2.55,26),
        text('rising =\norder kept',5.1,.7,26,TEAL),text('below the line\n= less alike',4.9,-1.45,26,TEAL))
    return VGroup(ax,ticks,diag,dots if points else VGroup(),labels)


class S00Title(TitleCard):
    LESSON='From Glomeruli to Piriform Cortex'
    TITLE='How a Scatter Keeps Similarity'
    def construct(self):
        self.add(text('BIOCHEMISTRYPEDIA',y=2.15,size=28,color=TEAL),text(self.LESSON,y=1.1,size=30))
        self.play(FadeIn(text('How a Scatter\nKeeps Similarity',y=-.6,size=52)),run_time=.7)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        gl=Circle(radius=.58,color=TEAL,fill_color=TEAL,fill_opacity=.6).move_to([-5.3,0,0])
        sheet=panel(8.3,5.6,1.65,0)
        ends=[[-1.6,1.8,0],[.3,-1.8,0],[4.7,1.4,0],[3.2,-.6,0],[1.4,.8,0]]
        links=VGroup(*[Line(gl.get_right(),p,color=TEAL,stroke_width=3) for p in ends])
        self.add(gl,sheet,text('one\nglomerulus',-5.25,1.5,28,TEAL),text('piriform cortex',1.65,3.2,30))
        self.at('If one glomerulus'); self.play(Create(links),FadeIn(VGroup(*[Dot(p,radius=.13,color=TEAL) for p in ends])),run_time=1.3)
        self.at('is the chemistry lost'); self.play(FadeIn(text('Chemistry lost?',y=-3.25,size=34)),run_time=.4)
        self.finish()


class S02SimilarQ(SpokenScene):
    def construct(self):
        self.add(population(center=True))
        self.at('what does similar mean'); self.play(FadeIn(text('Similar across a population?',y=-3.5,size=30)),run_time=.4)
        self.finish()


class S03Pattern1(SpokenScene):
    def construct(self):
        p=population(); self.add(p)
        self.at('Record many'); self.play(FadeIn(text('mouse smells A',2.6,2.95,30,A)),run_time=.4)
        puff=VGroup(*[Circle(radius=r,color=A,fill_color=A,fill_opacity=.4).move_to([x,y,0]) for x,y,r in [(1.2,1.5,.2),(1.65,1.8,.27),(2.15,1.45,.32)]])
        self.at('while the mouse smells')
        self.play(FadeIn(puff),run_time=.25)
        self.play(puff.animate.shift(LEFT*1.3).set_opacity(0),Transform(p,population(VALUES_A)),run_time=.7)
        self.remove(puff)
        self.at('Write down each'); self.play(FadeIn(column(VALUES_A,2.6,A,'')[0]),FadeIn(text('0 to 1 response',3,-3.25,28)),run_time=.7)
        self.finish()


class S04Pattern2(SpokenScene):
    def construct(self):
        p=population(VALUES_A); col=column(VALUES_A,2.6,A,'A'); self.add(p,col,text('0 to 1 response',2.6,-3.25,28))
        previous=None
        for phrase,i in [('This one fired',0),('That one did not',1),('A third fired',2)]:
            self.at(phrase)
            ring=Circle(radius=.37,color=A,stroke_width=4).move_to(p[1][i])
            start=p[1][i].get_top()+UP*.09
            line=VMobject(color=A,stroke_width=2.5).set_points_as_corners([start,[start[0],2.63,0],[1.4,2.63,0],[1.4,col[0][i][0].get_y()+.25,0],[2.1,col[0][i][0].get_y()+.25,0],[2.1,col[0][i][0].get_y()+.17,0]])
            cue=VGroup(ring,line)
            anim=[Create(cue)]
            if previous is not None: anim.append(FadeOut(previous))
            self.play(*anim,run_time=.4); previous=cue
        self.at('That list is'); self.play(FadeOut(previous),Transform(col[1],text('pattern for A',2.6,2.95,30,A)),run_time=.4)
        self.finish()


class S05Pattern3(SpokenScene):
    def construct(self):
        p=population(VALUES_A); a=column(VALUES_A,.8,A,'A'); b=column(VALUES_B,4.1,B,'B')
        self.add(p,a)
        self.at('Do the same'); self.play(Transform(p,population()),run_time=.3)
        self.at('for odor'); self.play(Transform(p,population(VALUES_B)),FadeIn(b),run_time=.6)
        self.at('many of the same neurons')
        both=VGroup(*[SurroundingRectangle(VGroup(a[0][i][0],b[0][i][0]),buff=.08,color=TEAL) for i in range(8) if VALUES_A[i] and VALUES_B[i]])
        self.play(Create(both),FadeIn(text('4 rows both active',2.5,-3.2,30,TEAL)),run_time=.6)
        self.finish()


class S06Correlation(SpokenScene):
    def construct(self):
        a=column(VALUES_A,-3.6,A,'A'); b=column(VALUES_B,-.3,B,'B')
        readout=VGroup(panel(4.7,4.3,4,.5),
            text('correlation\n(real analyses)',4,1.9,30),
            text(f'r ≈ {np.corrcoef(VALUES_A,VALUES_B)[0,1]:.2f}',4,.55,38,GREY),
            text('related measure\nnot the same number',4,-.85,27))
        self.add(a,b,text('overlap here',-2,3.5,30,TEAL),readout,
                 text('overlap = rows where both respond (4 of 8)',y=-3.25,size=28))
        self.at('Real analyses correlate')
        both=VGroup(*[SurroundingRectangle(VGroup(a[0][i][0],b[0][i][0]),buff=.08,color=TEAL) for i in [0,2,5,6]])
        self.play(Create(both),run_time=.6)
        self.at('but not the same number'); self.play(Indicate(a[1],scale_factor=1.08),Indicate(b[1],scale_factor=1.08),run_time=.4)
        self.finish()


class S07Wiring1(SpokenScene):
    def construct(self):
        bulb=Ellipse(width=5.3,height=5.5,color=GREY).move_to([-3.6,0,0]); cell=neuron(3.4,-.2,False,2.8,3.7)
        gl=VGroup(*[Circle(radius=.28,color=TEAL,fill_color=TEAL,fill_opacity=.8).move_to([x,y,0]) for x,y in [(-4.9,1.4),(-3.5,2),(-2.1,.8),(-4.4,-1.4),(-2.5,-1.7)]])
        links=VGroup(*[Line(g.get_right(),cell.get_left()+UP*(i-2)*.55,color=TEAL,stroke_width=3) for i,g in enumerate(gl)])
        self.add(bulb,gl,cell,text('olfactory bulb',-3.6,3.1,30),text('piriform neuron',3.4,2.3,30),
                 text('glomeruli',-3.6,-3.15,28,TEAL),text('Miyamichi and colleagues, 2011',2.1,-3.35,26))
        self.at('Now the wiring'); self.play(Create(links),run_time=1.2)
        self.at('spread across the bulb'); self.play(LaggedStart(*[Indicate(g) for g in gl],lag_ratio=.15),run_time=.9)
        self.finish()


class S08Wiring2(SpokenScene):
    def construct(self):
        self.add(head('In this simple model'))
        cell=neuron(1,-.3,False,4.1,5.1)
        gl=VGroup(*[Circle(radius=.42,color=TEAL,fill_color=TEAL,fill_opacity=.1).move_to([-4.9,y,0]) for y in [1.6,-1.2]])
        wires=VGroup(*[Line(g.get_right(),cell.get_left()+UP*y,color=TEAL,stroke_width=4) for g,y in zip(gl,[1,-1])])
        track=Rectangle(width=.65,height=3.6,color=TEXT).move_to([.15,-.4,0])
        bar=Rectangle(width=.6,height=.06,fill_color=TEAL,fill_opacity=1,stroke_width=0).move_to([.15,-2.17,0])
        threshold=DashedLine([-.4,.5,0],[2.7,.5,0],color=TEXT)
        status=text('one input',4.8,1.5,28)
        self.add(cell,gl,wires,track,bar,threshold,status,text('voltage',1.65,-1.8,26),text('threshold',4.8,.5,28),text('piriform neuron',1,-3.15,28),
                 text('Davison and Ehlers, 2011: one input did not evoke firing',y=-3.65,size=26))
        self.at('Driving one glomerulus')
        self.play(gl[0].animate.set_fill(TEAL,1),Transform(bar,Rectangle(width=.6,height=1.8,fill_color=TEAL,fill_opacity=1,stroke_width=0).move_to([.15,-1.3,0])),run_time=.7)
        below=text('below threshold,\nno spike',4.85,-1,27)
        self.at('did not make'); self.play(FadeIn(below),run_time=.3)
        self.at('In this simple model'); self.play(Indicate(cell,color=TEAL,scale_factor=1.02),run_time=.4)
        self.at('enough inputs are active together')
        self.play(gl[1].animate.set_fill(TEAL,1),cell.animate.set_fill(TEAL,.35),Transform(status,text('two inputs',4.8,1.5,28)),
            Transform(bar,Rectangle(width=.6,height=3.2,fill_color=TEAL,fill_opacity=1,stroke_width=0).move_to([.15,-.6,0])),FadeOut(below),run_time=.6)
        self.add(text('spike',4.85,-1,36,TEAL)); self.finish()


class S09Wiring3(SpokenScene):
    def construct(self):
        self.add(panel(11.7,3.6,0,-1),head('same inputs, same response'),text('cortex sheet',-4.5,-3.25,28),text('spike',4.7,-1,30,TEAL))
        w=position_wiring(); self.add(w)
        self.at('Nothing about'); self.play(Transform(w,position_wiring(2)),run_time=1.7)
        self.finish()


class S10Toy(SpokenScene):
    def construct(self):
        gl=VGroup(*[Circle(radius=.31,color=TEAL,fill_color=TEAL,fill_opacity=.85).move_to([-5+i*2,2,0]) for i in range(6)])
        cells=VGroup(*[neuron(x,-1,True,2.5,2.8) for x in [-4,0,4]])
        def links(pairlist):
            return VGroup(*[Line(gl[g].get_bottom(),cells[i].get_top()+RIGHT*(j-.5)*.6,color=TEAL,stroke_width=3) for i,pair in enumerate(pairlist) for j,g in enumerate(pair)])
        wires=links([(0,2),(1,4),(3,5)])
        title=head('Two-input toy')
        self.add(title,gl,cells,wires,text('glomeruli',y=2.65,size=28),text('piriform neurons',y=-2.85,size=28))
        self.at('only if both are active'); self.play(FadeIn(text('fires only if both are active',y=-3.5,size=30,color=TEAL)),run_time=.4)
        # Lead into the final sentence, then retain the random-pair state for 2 s.
        self.at('Wiring is random',lead=1.6)
        self.play(Transform(wires,links([(1,5),(0,3),(2,4)])),Transform(title,head('Random pairs of inputs')),run_time=.6)
        self.wait(.5)
        self.play(Transform(wires,links([(0,4),(2,5),(1,3)])),run_time=.6)
        self.wait(1.0)
        self.finish()


class S11Odours(SpokenScene):
    def construct(self):
        rows=odours(); self.add(head('Active glomeruli'),rows[0],text('A = 10',-3.9,-2.7,32,A))
        self.at('A related ester'); self.play(FadeIn(rows[1]),FadeIn(text('B = 10',-.4,-2.7,32,B)),run_time=.5)
        self.at('shares six with'); self.play(FadeIn(text('shared = 6',3.9,-2.7,32,TEAL)),FadeIn(text('gold rings = same glomeruli as A',y=-1.3,size=28)),run_time=.4)
        self.finish()


class S12Amine(SpokenScene):
    def construct(self):
        rows=odours(True); self.add(head('Active glomeruli'),rows[0],rows[1])
        self.at('An unrelated amine'); self.play(FadeIn(rows[2]),FadeIn(text('C shared = 0',y=-3.3,size=34,color=C)),run_time=.4)
        self.finish()


class S13APairs(SpokenScene):
    def construct(self):
        p=pair_graph(); self.add(head("Pairs from A’s 10 glomeruli"),p[1])
        cell=neuron(3.4,.6,True,1.5,1.6)
        wires=VGroup(*[Line(p[1][i].get_center(),cell.get_left()+UP*(j-.5)*.4,color=TEAL,stroke_width=3) for j,i in enumerate([1,3])])
        pair_label=text('one input pair',3.4,-.65,28,TEAL)
        self.add(cell,wires,pair_label)
        self.bring_to_front(p[1])
        self.at('Any pair of'); self.play(Create(p[0]),run_time=1.1); self.bring_to_front(p[1])
        self.at('Those neurons respond'); self.play(Indicate(cell),run_time=.4)
        self.at('The pairs are counted')
        self.play(FadeOut(cell),FadeOut(wires),FadeOut(pair_label),FadeIn(text('10 × 9 / 2 = 45',3.1,1.2,34,A)),run_time=.4)
        self.add(text('input pairs',3.1,.3,30),text('Equally many neurons\nper pair, on average',3.1,-1.25,28))
        self.finish()


class S14BPairs(SpokenScene):
    def construct(self):
        p=pair_graph(); self.add(head('Which also respond to B?'),p,text('45 input pairs',3.1,1,32))
        self.at('Only neurons whose'); self.play(Transform(p,pair_graph(True)),run_time=.65)
        self.at('two inputs both')
        self.remove(self.mobjects[2]); self.add(text('6 × 5 / 2 = 15',3.15,1.2,34,B),text('of 45 input pairs',3.15,.25,30),
            text('6 blue nodes: shared',3.15,-1.05,28,B),text('4 gold nodes: A only',3.15,-1.85,28,A))
        self.finish()


class S15Predict(SpokenScene):
    def construct(self):
        self.add(prediction()); self.at('Pause and predict'); self.finish()


class S16Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction())
        cues=VGroup(*[Dot([-.8+i*.4,-3.55,0],radius=.07,color=TEAL) for i in range(5)])
        self.add(cues)
        for d in cues: self.play(d.animate.set_color(TEXT).scale(1.3),run_time=1)


class S17Reveal(SpokenScene):
    def construct(self):
        p=pair_graph(True); self.add(head('Two-input toy: 15 of 45 pairs'),p,
            text('shared glomeruli',3.2,2.1,28),text('60%',3.2,1.35,48,A),
            Rectangle(width=4.5*.6,height=.35,fill_color=A,fill_opacity=1,stroke_width=0).move_to([2.3,.65,0]))
        self.at('About one third'); self.play(FadeIn(text('15 / 45 = 1/3',3.2,-.25,34,B)),FadeIn(text('33% of neurons',3.2,-1,32,B)),run_time=.4)
        bar=Rectangle(width=4.5/3,height=.35,fill_color=B,fill_opacity=1,stroke_width=0).move_to([1.7,-1.7,0])
        self.play(GrowFromEdge(bar,LEFT),run_time=.6)
        self.at('but only a third'); self.play(Indicate(VGroup(*[p[0][k] for k,(i,j) in enumerate(combinations(range(10),2)) if i<6 and j<6]),scale_factor=1.015,color=B),run_time=.6)
        self.add(text('Among A-responsive neurons',y=-3.25,size=28)); self.finish()


class S18CZero(SpokenScene):
    def construct(self):
        self.add(head('Two-input toy: A and C'))
        for x,col,label in [(-3.15,A,'A glomeruli'),(3.15,C,'C glomeruli')]:
            self.add(text(label,x,2.4,30,col))
            for i in range(10): self.add(Circle(radius=.23,color=col,fill_color=col,fill_opacity=1).move_to([x-1.6+(i%5)*.8,1.45-(i//5)*.85,0]))
        cells=VGroup(*[neuron(-4.5+i, -1.15,False,.65,.65) for i in range(10)])
        self.add(cells,text('A-responsive neurons: no C response',y=-2.05,size=29),text('no shared glomeruli → zero lit input pairs',y=-2.7,size=28))
        self.at('And for'); self.play(FadeIn(text('overlap = 0',y=-3.35,size=34,color=C)),run_time=.4)
        self.finish()


class S19Order(SpokenScene):
    def construct(self):
        self.add(ranking()); self.at('The order of similarity'); self.play(FadeIn(text('order kept',y=-3.3,size=32,color=TEAL)),run_time=.4); self.finish()


class S20Shrink(SpokenScene):
    def construct(self):
        self.add(head('Both inputs must be shared'))
        cell=neuron(0,-1,True,4.8,3.1)
        gl=VGroup(*[Circle(radius=.38,color=B,fill_color=B,fill_opacity=.8).move_to([x,2,0]) for x in [-3.6,3.6]])
        wires=VGroup(*[Line(g.get_bottom(),cell.get_top()+RIGHT*(i-.5),color=B,stroke_width=4) for i,g in enumerate(gl)])
        self.at('But the overlap')
        self.play(FadeIn(cell),FadeIn(text('two-input neuron',0,-3.0,28,TEAL)),run_time=.35)
        self.play(FadeIn(gl),Create(wires),run_time=.8)
        self.at('Both of a')
        self.play(FadeIn(text('first input shared',-4.6,.25,28,B)),
                  FadeIn(text('second input shared',4.5,.25,28,B)),
                  Indicate(wires,scale_factor=1.02),run_time=.4)
        self.at('so six tenths'); self.play(FadeIn(text('6/10',-4.6,-.45,34,B)),run_time=.25)
        self.at('times five ninths'); self.play(FadeIn(text('5/9',4.5,-.45,34,B)),run_time=.25)
        self.at('gives one third'); self.play(FadeIn(text('6/10 × 5/9 = 1/3',0,-1.4,30)),run_time=.25)
        self.add(text('60% → 33%',4.5,-1.65,32,TEAL),text('close to 0.6² = 0.36',y=-3.6,size=29)); self.wait(3.2); self.finish()


class S21Position(SpokenScene):
    def construct(self):
        rng=np.random.default_rng(21)
        pts=np.array([[-5.5+(i%9)*.76+rng.uniform(-.12,.12),-2.2+(i//9)*1.03+rng.uniform(-.12,.12),0] for i in range(45)])
        dots=VGroup(*[Dot(p,radius=.15,color=B if i<15 else A) for i,p in enumerate(pts)])
        self.add(head('A-responsive neurons'),panel(7.7,5.6,-2.45,-.15),dots,text('cortex sheet',-2.45,-3.3,28),
                 text('15 also respond to B',4,1.35,28,B),text('45 respond to A',4,.4,28,A),text('15 / 45 = 1/3',4,-.8,32),text('counts unchanged',4,-2,28))
        self.at('Where the neurons'); self.play(*[d.animate.move_to(p) for d,p in zip(dots,pts[rng.permutation(45)])],run_time=1.6); self.finish()


class S22Sim(SpokenScene):
    def construct(self):
        p=model_plot(False); self.add(p)
        self.at('A larger toy'); self.play(Create(p[2]),run_time=.8)
        self.at('gives the same'); self.play(FadeIn(model_plot()[3]),run_time=.5); self.finish()


class S23Sim2(SpokenScene):
    def construct(self):
        p=model_plot(False); self.add(p)
        self.at('The order is kept'); self.play(LaggedStart(*[FadeIn(d,scale=.5) for d in model_plot()[3]],lag_ratio=.12),run_time=1.5)
        self.at('Related odors become'); self.play(Indicate(p[4][-1],scale_factor=1.05),run_time=.5); self.finish()


class S24Rule(SpokenScene):
    def construct(self):
        self.add(head('In this model'),panel(11.8,3.7,0,-.55),text('cortex sheet',-4.6,-2.8,26))
        gl=VGroup(*[Circle(radius=.32,color=TEAL,fill_color=TEAL,fill_opacity=1 if i<2 else .05).move_to([x,2.25,0]) for i,x in enumerate([-3,0,3])])
        cells=VGroup(neuron(-3,-.7),neuron(3,-.7))
        def links(other=False):
            return VGroup(*[Line(gl[j].get_bottom(),cells[i].get_top()+RIGHT*(k-.5)*.5,color=TEAL,stroke_width=3) for i,ids in enumerate([(0,1),(1,2) if other else (0,1)]) for k,j in enumerate(ids)])
        w=links(); rule=text('Position does not enter; which glomeruli feed it does.',y=-3.45,size=28)
        status=text('same inputs, same response',y=-1.85,size=28,color=TEAL)
        self.add(gl,cells,w,rule,status)
        self.at('where a neuron sits'); self.play(Indicate(cells,scale_factor=1.04),run_time=.5)
        self.at('Which glomeruli feed')
        self.play(Transform(w,links(True)),cells[1].animate.set_fill(TEAL,.04),Transform(status,text('same sites; different inputs → different responses',y=-1.85,size=28,color=TEAL)),run_time=.6)
        self.wait(3.2)
        self.finish()


class S26Test(SpokenScene):
    def construct(self):
        self.add(head('Overlap of responses: test for real data'))
        base=-2.3
        self.add(Line([-5.8,base,0],[5.8,base,0],color=TEXT),text('0%',-6.1,base,26),text('60%',-6.1,1.7,26),
            text('shared\nglomeruli',-3.8,-3.05,28,A),text('shared neurons,\nthis model',0,-3.05,28,B),text('real piriform:\nmeasure this',3.8,-3.05,28))
        bars=VGroup(*[Rectangle(width=1.9,height=h,fill_color=col,fill_opacity=.85,stroke_width=0).move_to([x,base+h/2,0]) for x,h,col in [(-3.8,4,A),(0,4*(1/3)/.6,B)]])
        # An unknown measurement has no bar height until data are supplied.
        question=text('?',4.15,-.65,56)
        self.add(question,text('less alike\nif model holds',3.8,1.8,28))
        direction=Arrow([2.8,1,0],[2.8,-1.75,0],buff=0,color=TEAL,stroke_width=3)
        cue=Dot([2.8,1,0],radius=.09,color=TEXT)
        self.at('So here is'); self.play(*[GrowFromEdge(bar,DOWN) for bar in bars],run_time=1.5)
        self.add(text('60%',-3.8,2.1,34,A),text('33%',0,.35,34,B))
        self.at('If piriform worked')
        self.play(GrowArrow(direction),FadeIn(cue),run_time=.6)
        # Repeat the downward comparison throughout the narrated hold.
        start=self.elapsed()
        cue.add_updater(lambda m, dt: m.move_to([2.8,1-2.75*((self.elapsed()-start)%1.8)/1.8,0]))
        self.finish()
        cue.clear_updaters()


class S27Takeaway(SpokenScene):
    def construct(self):
        r=ranking(); self.add(r)
        self.at('random wiring keeps'); label=text('expected order kept',y=-3.3,size=30,color=TEAL); self.play(FadeIn(label),run_time=.4)
        self.at('but makes related')
        self.play(FadeOut(r),FadeOut(label),FadeIn(head('Two-input toy: related odours less alike')),FadeIn(text('60% → 33%',y=.4,size=70,color=TEAL)),FadeIn(text('shared glomeruli → shared neurons',y=-1.2,size=30)),run_time=.6)
        self.at('Anything tighter needs')
        old=Group(*self.mobjects)
        card=text('Anything tighter needs\nmore than this model.',y=-2.55,size=40)
        self.play(FadeIn(card),run_time=.25)
        self.play(FadeOut(old),run_time=.25)
        self.play(card.animate.move_to(ORIGIN),run_time=.4)
        self.finish()


class S28End(EndCard):
    LINE='In this model, random wiring keeps the order of likeness but makes related odours less alike.'
    def construct(self):
        self.add(text('In this model, random wiring\nkeeps the order of likeness\nbut makes related odours less alike.',y=.45,size=38),
                 text('biochemistrypedia.com',y=-2.2,size=30))
        self.finish()
