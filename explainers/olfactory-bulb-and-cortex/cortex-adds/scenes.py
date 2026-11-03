"""What the Cortex Adds — revision.
COLOR MAP: TEAL=bulb input/cortical activity; BLUE=odour A; YELLOW=odour B;
PURPLE=inhibitory neighbours; GOLD=intervention/flagged schematic comparison;
GREY=structure; RED=spatial-map cross. All matrix values are illustrative,
not measured data. The sniff trace is computed as sin(2*pi*f*t-pi/2).
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'
ORANGE = '#F29E4C'
POSITIONS = [(-1,.7),(-2,1.1),(2,1.1),(1,.7),(-2,-1.1),(-1,-.7),(1,-.7),(2,-1.1)]
ACTIVE = (0,3,5,6)

def label(s,y=3.1,size=30,color=TEXT):
    return T(s,size,color).move_to([0,y,0])

def values(kind):
    # Explicit symmetric schematic matrices: retain related pairs, but selectively
    # regroup B/C in cortex. Blocked output restores the input rank order while
    # raising the off-diagonal floor. These are NOT estimates of the experiment.
    a=np.full((4,4),.08)
    np.fill_diagonal(a,1.)
    for i,j in ((0,1),(2,3)): a[i,j]=a[j,i]=.4
    if kind=='empty': return np.zeros((4,4))
    if kind=='model':
        a=np.where(np.eye(4),1.,np.where(a>.1,.22,.04))
    if kind=='cortex':
        # One positive-semidefinite schematic in every observed piriform panel.
        # Related A/B and C/D sharpen; B/C is additionally regrouped by cortex.
        a=np.array([[1.,.7,.4,.15],[.7,1.,.8,.4],
                    [.4,.8,1.,.7],[.15,.4,.7,1.]])
    if kind=='blocked':
        a=.5+.45*a
        np.fill_diagonal(a,1.)
    return a

def scale_key(y=-2.6):
    # Constant, shared dim-to-bright key on EVERY matrix scene.
    swatches=VGroup(*[Rectangle(width=.21,height=.22,stroke_width=0,
        fill_color=TEAL,fill_opacity=v).move_to([-1.1+i*.21,y,0]) for i,v in enumerate(np.linspace(.02,1,9))])
    return VGroup(T('less',26,GREY).move_to([-2.15,y,0]),swatches,
        T('more',26,TEAL).move_to([1.45,y,0]),T('pattern similarity',26).move_to([4.2,y,0]))

def panel(x,title,kind='empty',w=4.35,y=.25):
    step=w/4; h=4.3 if w==3.5 else w; row=h/4; cells=VGroup(); a=values(kind)
    for r in range(4):
        for c in range(4):
            cells.add(Rectangle(width=step-.045,height=row-.045,stroke_color=GREY,stroke_width=1,
                fill_color=TEAL,fill_opacity=.025+.95*a[r,c]).move_to([x+(c-1.5)*step,y+(1.5-r)*row,0]))
    letters=VGroup(*[T(s,26).move_to([x+(i-1.5)*step,y+h/2+.24,0]) for i,s in enumerate('ABCD')],
        *[T(s,26).move_to([x-w/2-.25,y+(1.5-i)*row,0]) for i,s in enumerate('ABCD')])
    name=T(title,28,TEAL).move_to([x,3.52 if w==3.5 else 3.15,0])
    axis=T('odours',26,GREY).move_to([x,y-h/2-.3,0])
    return VGroup(cells,letters,name,axis)

def pair(a='input',b='input'):
    return VGroup(panel(-3.05,'boutons',a),panel(3.05,'piriform',b),scale_key(),
        label('A–B / C–D: related odours • schematic',-3.12,26,GREY))

def prediction():
    return VGroup(pair('empty','empty'),label('Tighter, same, or looser?',-3.55,30))

def outlines():
    # Dashed inset marks the faint MODEL level; observed solid fill extends
    # beyond this inset, making the stronger-than-predicted result visible.
    step=4.35/4
    g=VGroup()
    for r,c in ((0,1),(1,0),(2,3),(3,2)):
        p=np.array([3.05+(c-1.5)*step,.25+(1.5-r)*step,0])
        box=Square(side_length=step*.58,stroke_color=GOLD,stroke_width=4,
                   fill_color=TEAL,fill_opacity=.06).move_to(p)
        g.add(VGroup(box.copy().set_stroke(width=0),DashedVMobject(box.copy().set_fill(opacity=0),num_dashes=12)))
    g.add(T('Dashed inset: random model predicts softer',26,GOLD).move_to([0,-3.55,0]))
    return g

def three(kinds=('input','cortex','empty'),names=('boutons','piriform','output blocked')):
    return VGroup(*[panel(x,n,k,3.5,.45) for x,n,k in zip((-4.25,0,4.25),names,kinds)],
        scale_key(-2.55),label('Qualitative relationships • schematic',-3.08,26,GREY))

def triple(blocked='empty'): return three(('input','cortex',blocked))
def predict2(): return VGroup(triple(),label('What happens to the blocks?',-3.5,30))

def bc_marks(p):
    return VGroup(*[SurroundingRectangle(p[n][0][i],color=GOLD,buff=.02,stroke_width=3)
        for n in (0,1,2) for i in (6,9)])

def sheet(x=0,y=0,w=11,h=5.4,title='piriform cortex'):
    border=RoundedRectangle(width=w,height=h,corner_radius=.2,color=GREY).move_to([x,y,0])
    cells=VGroup(*[Circle(radius=.24,color=TEAL,fill_color=TEAL,fill_opacity=.1)
        .move_to([x+a*w/5.1,y+b*h/3.5,0]) for a,b in POSITIONS])
    name=T(title,28,TEAL).move_to([x,y+h/2+.45,0])
    return VGroup(border,cells,name)

def light(cells,ids=ACTIVE):
    for i,c in enumerate(cells): c.set_fill(TEAL,.95 if i in ids else .08).set_stroke(TEAL if i in ids else GREY)
    return cells

def links(s,thick=False):
    g=VGroup()
    for i in range(8):
        for j in range(i+1,8):
            a=s[1][i].get_center(); b=s[1][j].get_center(); d=b-a; u=d/np.linalg.norm(d)
            strong=thick and i in ACTIVE and j in ACTIVE
            g.add(ArcBetweenPoints(a+u*.27,b-u*.27,angle=(.22 if (i+j)%2 else -.22),
                color=TEAL,stroke_width=5 if strong else 1.4,stroke_opacity=.9 if strong else .35))
    return g

def recurrent(s):
    # Visible return routes on all four cells of the familiar-odour ensemble.
    loops=VGroup()
    for i in ACTIVE:
        p=s[1][i].get_center()
        direction=UP if i in (0,3) else DOWN
        loops.add(CurvedArrow(p+LEFT*.28,p+RIGHT*.28,
            angle=(-TAU*.78 if direction[1]>0 else TAU*.78),
            color=TEAL,stroke_width=4,tip_length=.2))
    return loops

def ensemble(s):
    pts=VGroup(*[s[1][i] for i in ACTIVE])
    return Ellipse(width=pts.width+.8,height=pts.height+1.,color=TEAL,stroke_width=4).move_to(pts)

def anatomy(x):
    # Small brain silhouette and cortical field, visible before imaging is named.
    outline=Ellipse(width=4.6,height=3.8,color=GREY,stroke_width=2,
        fill_color=GREY,fill_opacity=.15).move_to([x,-.2,0])
    region=RoundedRectangle(width=3.9,height=2.8,corner_radius=.35,
        color=TEAL,stroke_opacity=.45,fill_color=TEAL,fill_opacity=.08).move_to([x,-.35,0])
    folds=VGroup(*[ArcBetweenPoints([x-1.6,y,0],[x+1.6,y,0],angle=.28,
        color=GREY,stroke_width=1.5,stroke_opacity=.35) for y in (-1.1,-.35,.4)])
    return VGroup(outline,region,T('piriform cortex',26,GREY).move_to([x,2.13,0]),folds)

def windows():
    g=VGroup()
    for x,title in ((-3.15,'boutons • input'),(3.15,'neurons • output')):
        s=sheet(x,0,5.4,5.3,title)
        s[1].scale(.72,about_point=np.array([x,0,0])).set_fill(TEAL,.18)
        g.add(VGroup(*s,anatomy(x)))
    return g

def boutons():
    s=windows()[0]
    for c in s[1]: c.scale(1.05).set_fill(TEAL,.95)
    stalks=VGroup(*[Line(c.get_center()+LEFT*.5,c.get_center(),color=TEAL,stroke_width=3) for c in s[1]])
    return VGroup(s,stalks)

def spatial():
    s=sheet(-3.25,0,5.,5.2,'spatial map'); s[1].set_opacity(0)
    patches=VGroup()
    for r in range(4):
        for c in range(4):
            col=BLUE if (r,c)==(1,1) else YELLOW if (r,c)==(1,2) else GREY
            patches.add(Square(side_length=.83,color=col,fill_color=col,fill_opacity=.75 if col!=GREY else .1)
                .move_to([-4.75+c,1.5-r,0]))
    names=VGroup(T('A',28,BG).move_to(patches[5]),T('B',28,BG).move_to(patches[6]))
    return VGroup(s,patches,names)

def geometry(both=False):
    s=sheet(3.25,0,5.,5.2,'population patterns'); light(s[1])
    for i,c in enumerate(s[1]): c.set_fill(BLUE,.85 if i in ACTIVE else .06).set_stroke(GREY)
    b=VGroup(*[Circle(radius=.25,color=YELLOW,stroke_width=4,fill_opacity=0).move_to(s[1][i]) for i in (0,2,3,5)])
    return VGroup(s,b if both else VGroup())

def geometry_key():
    return VGroup(T('A: blue fill',26,BLUE).move_to([1.9,-3.1,0]),T('B: gold rim',26,YELLOW).move_to([4.65,-3.1,0]))

def circuit():
    source=chip('bulb input',TEAL,30).move_to([-4.75,.2,0])
    cell=Circle(.65,color=TEAL,fill_color=TEAL,fill_opacity=.9).move_to([-1.5,.2,0])
    name=T('excitatory\npiriform neuron',28,TEAL).move_to([-1.5,-1.25,0])
    inp=Arrow(source.get_right(),cell.get_left(),buff=.12,color=TEAL,stroke_width=7)
    exc=Circle(.52,color=TEAL,fill_color=TEAL,fill_opacity=.75).move_to([3.25,2.,0])
    inh=Circle(.52,color=PURPLE,fill_color=PURPLE,fill_opacity=.75).move_to([3.25,-2.,0])
    neighbours=VGroup(exc,inh,T('excitatory neighbour',26,TEAL).move_to([3.25,2.95,0]),
        T('inhibitory neighbour',26,PURPLE).move_to([3.25,-2.95,0]))
    outs=VGroup(*[Arrow(cell.get_right(),c.get_left(),buff=.14,color=TEAL,stroke_width=5) for c in (exc,inh)])
    syn=VGroup(*[Line([.55,y-.25,0],[.55,y+.25,0],color=GOLD,stroke_width=7) for y in (.95,-.65)])
    return VGroup(source,cell,name,inp,neighbours,outs,syn)

def block_label(): return label('Genetic tool blocks transmitter release',-3.58,28,GOLD)

def feedback():
    b=chip('bulb',TEAL,34).move_to([-4.5,1.55,0]); c=chip('piriform',TEAL,34).move_to([2.7,1.55,0])
    o=chip('other olfactory areas',TEXT,30).move_to([2.7,-1.9,0])
    arrow=Arrow(c.get_left(),b.get_right(),buff=.15,color=TEAL,stroke_width=5)
    out=Arrow(c.get_bottom(),o.get_top(),buff=.15,color=TEAL,stroke_width=5)
    return VGroup(b,c,o,arrow,out,T('feedback to bulb',30,TEAL).move_to([-.8,2.15,0]),
        T('connects to',28).move_to([4.25,-.15,0]))

class S00Title(TitleCard):
    TITLE='What the Cortex Adds'
    LESSON='From Glomeruli to Piriform Cortex'
    def construct(self):
        self.add(label('BIOCHEMISTRYPEDIA',1.6,26,TEAL),label(self.LESSON,.8,28,GREY))
        title=T(self.TITLE,54,font=TITLE_FONT)
        self.play(FadeIn(title),Create(Line([-1.5,-.7,0],[1.5,-.7,0],color=GOLD)),run_time=.55)
        self.finish()

class S01Question(SpokenScene):
    def construct(self):
        b=chip('bulb',TEAL,30).move_to([-4.8,0,0]); s=sheet(1.3,0,7,5.4)
        fan=VGroup(*[Line(b.get_right(),s[1][i].get_center(),color=TEAL,stroke_width=2) for i in ACTIVE])
        self.add(b,s,T('?',66,GOLD).move_to([5.6,0,0]))
        self.at('just scatter its input'); self.play(Create(fan),*[c.animate.set_fill(TEAL,.95) for i,c in enumerate(s[1]) if i in ACTIVE],FadeIn(label('Scattered input',-3.25,28,TEAL)),run_time=.55)
        self.finish()

class S02Pashkovski(SpokenScene):
    def construct(self):
        w=windows()
        for s in w: s[1].set_fill(TEAL,.18)
        self.add(w,label('Pashkovski and colleagues, 2020',3.48,28))
        self.at('imaged two things'); self.play(*[s[3][1].animate.set_stroke(TEAL,opacity=1,width=3) for s in w],run_time=.45)
        self.at('the same panel'); self.play(FadeIn(label('Same odour panel • mice',-3.1,28)),run_time=.4)
        self.finish()

class S03Boutons(SpokenScene):
    def construct(self):
        b=boutons(); r=windows()[1]
        dim=b[0][1].copy().set_fill(TEAL,.18)
        self.add(b[0][0],b[0][2],b[0][3],dim,r)
        self.at('bulb axon boutons'); self.play(FadeOut(dim),FadeIn(b[0][1]),Create(b[1]),run_time=.5)
        self.at('These are the terminals'); self.play(FadeIn(T('mitral / tufted terminals',26,TEAL).move_to([-3.15,-3.15,0])),run_time=.4)
        self.finish()

class S04Neurons(SpokenScene):
    def construct(self):
        b=boutons(); r=windows()[1]
        self.add(b,r[0],r[2],r[3],T('mitral / tufted terminals',26,TEAL).move_to([-3.15,-3.15,0]))
        self.at('Second'); self.play(FadeIn(r[1]),run_time=.4)
        self.at('in layers'); self.play(FadeIn(T('layer 2/3',28).move_to([3.15,-3.15,0])),run_time=.4)
        self.finish()

class S05Sniff(SpokenScene):
    def construct(self):
        w=VGroup(boutons(),windows()[1]); w.scale(.83).shift(UP*.4); self.add(w)
        # Dedicated strip below both imaging windows.
        pts=[np.array([-5.7+11.4*t,-2.43+.28*np.sin(6*np.pi*t-np.pi/2),0]) for t in np.linspace(0,1,220)]
        wave=VMobject(color=ORANGE,stroke_width=5).set_points_as_corners(pts)
        self.at('The mice breathed'); self.play(Create(wave),FadeIn(label('Controlled sniff rate • schematic',-3.35,28,ORANGE)),run_time=.45)
        self.finish()

class S06Predict1(SpokenScene):
    def construct(self):
        self.add(pair('empty','empty'))
        self.at('Pause and predict'); self.play(FadeIn(label('Tighter, same, or looser?',-3.55,30)),run_time=.4)
        self.finish()

class S07Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(prediction()); self.wait(5)

class S08ScatterPred(SpokenScene):
    def construct(self):
        self.add(pair('empty','empty'))
        self.at('By that model'); self.play(FadeIn(outlines()),run_time=.45)
        self.at('should be less alike'); self.play(Indicate(outlines()[:4],color=GOLD,scale_factor=1.06),run_time=.5)
        self.finish()

class S09FirstHalf(SpokenScene):
    def construct(self):
        p=pair('empty','empty'); self.add(p,outlines())
        self.at('The first half held'); self.play(Transform(p[3],label('Comparison in mice • schematic',-3.12,26,GREY)),run_time=.35)
        self.at('more similar patterns'); self.play(Transform(p[0],panel(-3.05,'boutons','input')),Transform(p[1],panel(3.05,'piriform','cortex')),run_time=.55)
        self.finish()

class S10Kept(SpokenScene):
    def construct(self):
        p=pair('input','cortex'); p[3].become(label('Chemistry kept in both • schematic',-3.12,26,TEAL)); self.add(p,outlines())
        self.at('kept the chemistry'); self.play(Indicate(p[0][0],scale_factor=1.01),run_time=.35)
        self.finish()

class S11SecondHalf(SpokenScene):
    def construct(self):
        p=pair('input','cortex'); p[3].become(label('Beyond the random prediction • schematic',-3.12,26,TEAL)); self.add(p,outlines())
        self.at('more tightly'); self.play(Indicate(VGroup(*[p[1][0][i] for i in (1,4,11,14)]),color=GOLD,scale_factor=1.04),run_time=.6)
        self.finish()

class S12Numbers(SpokenScene):
    def construct(self):
        self.add(label('Made-up example, not measured averages',3.42,28,GOLD),
            label('Pattern similarity of related odours (correlation)',2.7,28))
        base=-2.6; height=4.65
        axis=VGroup(Line([-3.7,base,0],[-3.7,base+height,0],color=GREY),Line([-3.7,base,0],[4.2,base,0],color=GREY))
        for v in (0,.5,1):
            y=base+height*v; axis.add(Line([-3.85,y,0],[-3.7,y,0],color=GREY),T(str(v),28).move_to([-4.3,y,0]))
        self.add(axis,T('boutons',30,TEAL).move_to([-1.8,-3.15,0]),T('piriform',30,TEAL).move_to([2.1,-3.15,0]))
        bars=VGroup(*[Rectangle(width=1.7,height=height*v,stroke_color=TEAL,fill_color=TEAL,fill_opacity=.7).move_to([x,base+height*v/2,0]) for x,v in ((-1.8,.4),(2.1,.7))])
        nums=VGroup(*[T(str(v),34,TEAL).move_to([x,base+height*v+.3,0]) for x,v in ((-1.8,.4),(2.1,.7))])
        self.at('numbers on screen'); self.play(GrowFromEdge(bars,DOWN),FadeIn(nums),run_time=.6)
        self.at('sits above'); self.play(Indicate(bars[1],scale_factor=1.02),run_time=.4)
        self.finish()

class S12bModel(SpokenScene):
    def construct(self):
        p=three(('input','empty','cortex'),('boutons','random model','piriform')); self.add(p)
        flow=VGroup(CurvedArrow([-4.25,-2.85,0],[0,-2.85,0],angle=PI/5,
            color=TEAL,stroke_width=7,tip_length=.25),
            T('bouton data in',28,TEAL).move_to([-2.15,-3.53,0]))
        p[4].set_opacity(0)
        self.at('data through'); self.play(Create(flow),run_time=.5)
        self.at('a random wiring model'); self.play(Transform(p[1],panel(0,'random model','model',3.5,.45)),run_time=.5)
        self.at('patterns less alike'); self.play(Indicate(p[1][0],scale_factor=1.02),run_time=.4)
        self.finish()

class S13Added(SpokenScene):
    def construct(self):
        self.add(three(('input','model','cortex'),('boutons','random model','piriform')))
        self.at('added structure'); self.play(FadeIn(label('The cortex added structure',-3.5,32,TEAL)),run_time=.4)
        self.finish()

class S14Geometry1(SpokenScene):
    def construct(self):
        s=spatial(); neutral=s[1].copy().set_fill(GREY,.1).set_stroke(GREY)
        self.add(s[0][0],s[0][2],neutral,label('Similar odours: neighbouring patches',-3.2,28))
        self.at('A spatial map'); self.play(FadeIn(s[1]),FadeIn(s[2]),run_time=.5)
        self.finish()

class S15Geometry2(SpokenScene):
    def construct(self):
        g=geometry(); self.add(spatial())
        self.at('A representational geometry'); self.play(FadeIn(g),FadeIn(T('A: blue fill',26,BLUE).move_to([1.9,-3.1,0])),run_time=.4)
        self.at('similar population patterns'); self.play(FadeIn(geometry(True)[1]),FadeIn(T('B: gold rim',26,YELLOW).move_to([4.65,-3.1,0])),run_time=.5)
        self.finish()

class S16Geometry3(SpokenScene):
    def construct(self):
        left=spatial(); right=geometry(True); self.add(left,right,geometry_key())
        self.at('has the second'); self.play(right[0][0].animate.set_stroke(TEAL,width=4),run_time=.35)
        cross=VGroup(Line([-5.3,-2.,0],[-1.2,2.,0],color=RED,stroke_width=6),Line([-5.3,2.,0],[-1.2,-2.,0],color=RED,stroke_width=6))
        self.at('without the first'); self.play(left[1].animate.set_opacity(.3),left[2].animate.set_opacity(.3),Create(cross),run_time=.4)
        self.finish()

class S17Fibres(SpokenScene):
    def construct(self):
        s=sheet(); self.add(s)
        self.at('What could add'); self.play(FadeIn(label('What adds structure?',-3.35,30)),run_time=.35)
        self.at('linked to each other'); self.play(Create(links(s)),Transform(s[2],label('association fibres',3.15,28,TEAL)),run_time=.5)
        self.finish()

class S18Stored(SpokenScene):
    def construct(self):
        s=sheet(title='association fibres'); l=links(s); self.add(s,l)
        self.at('recurrent connections'); self.play(Create(recurrent(s)),FadeIn(label('Recurrent connections',-3.05,28,TEAL)),run_time=.5)
        self.at('Reviews treat them'); self.play(FadeIn(label('Thought to store experience • proposed',-3.55,28,TEAL)),run_time=.4)
        self.finish()

class S19Bind(SpokenScene):
    def construct(self):
        s=sheet(title='association fibres'); l=links(s); self.add(s,l,recurrent(s),label('Proposed mechanism',-3.35,28,GREY))
        self.at('Strengthening synapses'); self.play(Transform(l,links(s,True)),run_time=.5)
        self.at('active together'); self.play(*[c.animate.set_fill(TEAL,.95) for i,c in enumerate(s[1]) if i in ACTIVE],run_time=.4)
        self.at('is thought to bind'); self.play(Create(ensemble(s)),run_time=.5)
        self.at('a familiar'); self.play(Transform(s[2],label('One familiar odour • proposed',3.15,28,TEAL)),run_time=.35)
        self.finish()

class S20Complete(SpokenScene):
    def construct(self):
        s=sheet(title='One familiar odour • proposed'); l=links(s,True)
        arrows=VGroup()
        for j,i in enumerate(ACTIVE):
            p=s[1][i].get_center()
            start=p+UP*1.45+LEFT*1.0 if j<2 else p+DOWN*1.45+RIGHT*1.0
            arrows.add(Arrow(start,p,buff=.28,color=TEAL,stroke_width=9,tip_length=.38,
                max_tip_length_to_length_ratio=.3))
        status=label('Proposed mechanism',-3.35,28,GREY)
        self.add(s,l,ensemble(s),status)
        self.at('Then the whole'); self.play(Create(arrows),run_time=.3)
        self.at('ensemble could respond'); self.play(*[c.animate.set_fill(TEAL,.95) for i,c in enumerate(s[1]) if i in ACTIVE],run_time=.3)
        self.at('part of the input is missing'); self.play(*[Transform(arrows[i],DashedVMobject(arrows[i].copy().set_color(GREY).set_opacity(.4),num_dashes=7)) for i in (1,3)],
            Transform(status,label('Partial input → full ensemble • proposed',-3.35,28,TEAL)),run_time=.4)
        self.at('This is pattern completion',lead=.35); self.play(Transform(s[2],label('Pattern completion • proposed',3.15,30,TEAL)),run_time=.3)
        self.finish()

class S21Silence(SpokenScene):
    def construct(self):
        c=circuit(); c[6].set_opacity(0); self.add(c)
        self.at('tested the network'); self.play(FadeIn(label('Testing the network',3.58,30)),run_time=.4)
        self.at('blocked transmitter release'); self.play(c[6].animate.set_opacity(1),c[5].animate.set_opacity(.12),c[4][:2].animate.set_fill(opacity=.08),FadeIn(block_label()),run_time=.55)
        self.finish()

class S22StillInput(SpokenScene):
    def construct(self):
        c=circuit(); c[5].set_opacity(.12); c[4][:2].set_fill(opacity=.08); self.add(c,block_label())
        self.at('bulb input still arrived'); self.play(ShowPassingFlash(c[3].copy().set_stroke(width=12),time_width=.6),run_time=.65)
        self.at('they still responded'); self.play(Indicate(c[1],color=TEAL,scale_factor=1.12),FadeIn(T('still responds',28,TEAL).move_to([-1.5,1.65,0])),run_time=.4)
        self.at('But they excited'); self.play(FadeIn(label('Less drive to neighbours',3.58,30)),run_time=.4)
        self.at('including inhibitory cells'); self.play(ShowPassingFlash(c[3].copy().set_stroke(width=12),time_width=.6),run_time=.55)
        self.finish()

class S23Predict2(SpokenScene):
    def construct(self):
        self.add(triple())
        self.at('Pause and predict'); self.play(FadeIn(label('What happens to the blocks?',-3.5,30)),run_time=.4)
        self.finish()

class S24Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; self.add(predict2()); self.wait(5)

class S25Reveal2(SpokenScene):
    def construct(self):
        p=triple(); self.add(p)
        self.at('relationships became'); self.play(Transform(p[2],panel(4.25,'before block','cortex',3.5,.45)),run_time=.3)
        self.at('became more like'); self.play(Transform(p[2],panel(4.25,'output blocked','blocked',3.5,.45)),run_time=.55)
        marks=bc_marks(p)
        self.play(Create(marks),FadeIn(label('B–C pair returns toward the bouton pattern',-3.5,26,GOLD)),run_time=.25)
        self.finish()

class S25bBroader(SpokenScene):
    def construct(self):
        p=triple('blocked'); self.add(p)
        self.at('Tuning broadened'); self.play(Transform(p[4],label('Broader tuning • schematic',-3.08,28,TEAL)),run_time=.35)
        self.at('correlations rose overall'); self.play(FadeIn(label('Higher correlations overall',-3.5,28,TEAL)),run_time=.35)
        # Arrow terminates at the B/C comparison, with both symmetric cells marked.
        a=p[2][0][6].get_top()+RIGHT*.28; b=p[0][0][6].get_top()+RIGHT*.28
        path=VGroup(Line(a,[a[0],3.22,0],color=GOLD,stroke_width=3),
            Line([a[0],3.22,0],[b[0],3.22,0],color=GOLD,stroke_width=3),
            Arrow([b[0],3.22,0],b,buff=0,color=GOLD,stroke_width=3,tip_length=.18))
        self.at('the pattern moved'); self.play(Create(path),Create(bc_marks(p)),run_time=.45)
        self.finish()

class S26Caveat(SpokenScene):
    def construct(self):
        f=feedback(); self.add(f[0],f[1],label('One caveat',3.3,32))
        self.at('sends feedback'); self.play(GrowArrow(f[3]),FadeIn(f[5]),run_time=.5)
        self.at('connects to other'); self.play(FadeIn(f[2]),GrowArrow(f[4]),FadeIn(f[6]),run_time=.5)
        self.finish()

class S27Needed(SpokenScene):
    def construct(self):
        f=feedback().shift(DOWN*.35); self.add(f)
        thumb=panel(-4.5,'output blocked','blocked',w=1.8,y=-1.55)
        thumb[2].move_to([-4.5,.15,0]); thumb[3].set_opacity(0)
        needed=T('Network activity needed',28,TEAL).move_to([0,3.2,0])
        connector=VGroup(
            Line(needed.get_left()+LEFT*.15,[-6.2,3.2,0],color=TEAL,stroke_width=3),
            Line([-6.2,3.2,0],[-6.2,-1.55,0],color=TEAL,stroke_width=3),
            Arrow([-6.2,-1.55,0],thumb[0].get_left(),buff=.03,color=TEAL,stroke_width=3,tip_length=.14))
        self.at('network activity'); self.play(FadeIn(thumb),FadeIn(needed),Create(connector),run_time=.4)
        ring=SurroundingRectangle(f[1],color=GOLD,buff=.18)
        question=T('local only?',30,GOLD).move_to([5.05,2.45,0])
        pointer=Arrow(question.get_bottom(),ring.get_right(),buff=.12,color=GOLD,stroke_width=3)
        self.at('It is not shown'); self.play(Create(ring),FadeIn(question),GrowArrow(pointer),
            FadeIn(label('Local connections alone: not shown',-3.3,30,GOLD)),run_time=.4)
        self.finish()

class S28Takeaway(SpokenScene):
    def construct(self):
        p=pair('input','cortex'); self.add(p)
        self.at("keeps the bulb's chemistry"); self.play(Transform(p[3],label('Keeps the chemistry • schematic',-3.12,28,TEAL)),run_time=.35)
        self.at('then reshapes it'); self.play(Transform(p[0],panel(-3.05,'output blocked','blocked')),run_time=.4)
        self.at('with its own network'); self.play(Transform(p[3],label('Its network reshapes the relationships',-3.12,28,TEAL)),run_time=.35)
        self.finish()

class S29End(EndCard):
    LINE='The cortex keeps the chemistry;\nits network reshapes odour relationships.'
