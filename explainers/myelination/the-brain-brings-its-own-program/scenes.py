"""Chapter 3 animation.
COLOR MAP: BLUE normal axons; PURPLE glia/myelin; TEAL neuregulin signaling;
YELLOW vesicle release; GOLD light stimulation; RED blocked axon only;
GREY inert fibres/removed signal/outlines; TEXT results and prediction prompts.
All cartoons are schematic, not quantitative traces or molecular structures.
"""
import numpy as np
from bp_style import *
PURPLE = '#B58CD9'


def label(s, x, y, size=28, color=TEXT):
    return T(s, size, color).move_to([x, y, 0])


def hbar(a, b, y, h=.22, color=BLUE, op=.85):
    return Rectangle(width=b-a, height=h, stroke_color=color, stroke_width=2,
                     fill_color=color, fill_opacity=op).move_to([(a+b)/2, y, 0])


def sheath(a, b, y, h=.62):
    return RoundedRectangle(width=b-a, height=h, corner_radius=.12,
                            color=PURPLE, fill_color=PURPLE, fill_opacity=.55, stroke_width=3).move_to([(a+b)/2,y,0])


def oligo(c, ends, r=.65):
    c=np.array([*c,0.])
    body=Circle(radius=r, color=PURPLE, fill_color=PURPLE, fill_opacity=.35).move_to(c)
    ps=VGroup()
    for end in ends:
        e=np.array([*end,0.]); d=(e-c)/np.linalg.norm(e-c)
        ps.add(ArcBetweenPoints(c+d*r,e,angle=.22,color=PURPLE,stroke_width=4))
    return body,ps


def box(x,w=6.1,h=6.4):
    return RoundedRectangle(width=w,height=h,corner_radius=.2,color=GREY,stroke_width=2).move_to([x,0,0])


def arrow(a,b,dashed=False):
    arr=Arrow(a,b,buff=0,color=BLUE,stroke_width=3 if dashed else 9,tip_length=.22)
    return DashedVMobject(arr,num_dashes=10) if dashed else arr


class S00Title(TitleCard):
    LESSON='Myelination: Wrapping the Axon So the Signal Jumps'
    TITLE='The Brain Brings Its Own Program'
    def construct(self):
        title=T('The Brain Brings\nIts Own Program',48,font=TITLE_FONT,line_spacing=1.1)
        g=VGroup(T('BIOCHEMISTRYPEDIA',26,TEAL),T('MYELINATION',28,GREY),title,
                 Line(LEFT*1.3,RIGHT*1.3,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.45)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        title=label('The Brain Brings Its Own Program',0,3.1,32)
        a1=hbar(-1,5.8,1.55); a2=hbar(-1,5.8,-1.75)
        b,p=oligo([2.3,0],[(0,1.55),(4.8,1.55),(0,-1.75),(4.8,-1.75)],.85)
        cell=VGroup(a1,a2,b,p,label('oligodendrocyte',2.3,-2.65,28,PURPLE),label('axons',5.1,2.1,28,BLUE))
        card=VGroup(box(-4.1,w=3.5,h=3.7),label('LAST CHAPTER',-4.1,1.4,26,GREY),
                    label('In nerve',-4.1,.55,30),label('the axon',-4.1,-.2,30,BLUE),label('decides',-4.1,-.8,30,BLUE))
        self.add(title,cell,card)
        self.at('brain and spinal cord')
        self.play(Indicate(b,color=PURPLE,scale_factor=1.08),run_time=.6)
        self.at('axon decide there too')
        self.play(FadeIn(label('?',2.3,.1,80)),run_time=.4)
        self.finish()


FIB_Y=[1.65,0,-1.65]
def plastic():
    dish=Ellipse(width=12.3,height=6.1,color=GREY,stroke_width=3)
    fibres=VGroup(*[hbar(-.6,4.7,y,color=GREY) for y in FIB_Y])
    b,p=oligo([-3.5,.2],[(1.4,y) for y in FIB_Y],.8)
    wraps=VGroup(*[sheath(.0,2.8,y,.36) for y in FIB_Y])
    base=VGroup(dish,b,label('culture dish',-3.9,3.25,26,GREY),label('oligodendrocyte',-3.4,-1.1,26,PURPLE))
    fl=label('plastic fibres',1.8,-2.25,28,GREY)
    no=label('no axon here',0,-3.35,30)
    return base,p,fibres,wraps,fl,no


class S02Plastic(SpokenScene):
    def construct(self):
        base,p,f,w,fl,no=plastic()
        self.add(base)
        self.at('oligodendrocytes')
        self.play(Create(p),run_time=.6)
        self.at('plastic fibers')
        self.play(FadeIn(f),FadeIn(fl),run_time=.4)
        self.at('suitable diameter')
        self.play(LaggedStart(*[GrowFromEdge(s,LEFT) for s in w],lag_ratio=.2),run_time=1.1)
        self.at('no axon')
        self.play(FadeIn(no),run_time=.4)
        self.at('still a wrap')
        self.play(Indicate(w,color=PURPLE,scale_factor=1.04),run_time=.5)
        self.finish()


class S03Beat(SpokenScene):
    def construct(self):
        self.add(*plastic()); self.finish()


class S04Brink(SpokenScene):
    def construct(self):
        head=label('Mouse brain and spinal cord',0,3.15,32)
        left=box(-3.25,w=6.0,h=5.1).shift(DOWN*.1)
        right=box(3.25,w=6.0,h=5.1).shift(DOWN*.1)
        sig=VGroup(chip('neuregulin-1',TEAL,30),T('↓',40,TEAL),chip('ErbB signaling',TEAL,30)).arrange(DOWN,buff=.4).move_to([-3.25,.25,0])
        axs=VGroup(*[hbar(.65,5.85,y) for y in [1.35,.05,-1.25]])
        wraps=VGroup(*[sheath(a,a+1.8,y) for y in [1.35,.05,-1.25] for a in [.95,3.65]])
        cross=VGroup(Line([-3.8,.6,0],[-2.7,-.05,0],color=GREY,stroke_width=8),Line([-3.8,-.05,0],[-2.7,.6,0],color=GREY,stroke_width=8))
        self.add(head,left,right,axs,label('SIGNAL',-3.25,2,28,GREY),label('AXONS',3.25,2,28,BLUE),label('Brinkmann and colleagues, 2008',0,-3.25,26,GREY))
        self.at('removed')
        self.play(FadeIn(sig),run_time=.5)
        self.at('signaling')
        self.play(Create(cross),run_time=.5)
        self.play(FadeIn(label('removed',-3.25,-1.9,28,GREY)),run_time=.3)
        self.at('myelin still formed')
        self.play(LaggedStart(*[GrowFromEdge(s,LEFT) for s in wraps],lag_ratio=.07),run_time=.75)
        self.play(FadeIn(label('myelin still formed',3.25,-2.05,28,PURPLE)),run_time=.3)
        self.wait(1.8)
        self.finish()


class S05Extra(SpokenScene):
    def construct(self):
        c=np.array([-3.5,-.75,0]); radius=2.6
        arc=Arc(radius=radius,start_angle=0,angle=PI,arc_center=c,color=TEAL,stroke_width=5)
        ticks=VGroup(*[Line(c+2.45*np.array([np.cos(a),np.sin(a),0]),c+2.75*np.array([np.cos(a),np.sin(a),0]),color=TEAL) for a in np.linspace(0,PI,5)])
        needle=Line(c,c+2.3*np.array([np.cos(PI*.88),np.sin(PI*.88),0]),color=TEAL,stroke_width=7)
        dial=VGroup(arc,ticks,needle,Dot(c,color=TEAL),label('low',-5.9,-1.25,28,TEAL),label('high',-1.1,-1.25,28,TEAL),
                    label('neuronal neuregulin',-3.5,-2.0,28,TEAL))
        centers=[[1.45,-.05,0],[4.65,-.05,0]]
        axes=VGroup(*[Circle(radius=1.0,color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to(v) for v in centers])
        rings=VGroup(*[Annulus(inner_radius=1.0,outer_radius=1.25,color=PURPLE,fill_opacity=.65).move_to(v) for v in centers])
        thick=VGroup(*[Annulus(inner_radius=1.0,outer_radius=1.48,color=PURPLE,fill_opacity=.65).move_to(v) for v in centers])
        baseline=label('intact myelin at baseline',3,-2.0,27,PURPLE)
        extra=label('extra neuregulin',-3.5,2.65,30,TEAL)
        self.add(dial,axes,rings,baseline,label('Central myelin',3,2.6,32,PURPLE))
        self.at('extra')
        self.remove(baseline)
        self.play(FadeIn(extra),Rotate(needle,-PI*.76,about_point=c),run_time=1.4)
        self.at('thicken central myelin')
        self.play(Transform(rings,thick),run_time=1.15)
        self.play(FadeIn(label('thicker myelin',3,-2.0,28,PURPLE)),run_time=.25)
        self.at('tilt the wrap')
        self.play(Indicate(rings,color=PURPLE,scale_factor=1.03),run_time=.5)
        self.at('not needed to start')
        self.play(FadeIn(label('not needed to start, but can tilt',0,-2.9,32)),run_time=.45)
        self.finish()


def halves():
    frames=VGroup(box(-3.25),box(3.25),label('IN NERVE',-3.25,2.75,30),label('IN THE BRAIN',3.25,2.75,30))
    cells=[]; axs=[]
    for x,name in [(-3.25,'Schwann cell'),(3.25,'glial cell')]:
        cells.append(VGroup(Ellipse(width=4.9,height=2.0,color=PURPLE,fill_color=PURPLE,fill_opacity=.22).move_to([x,1.15,0]),label(name,x,1.15,30,PURPLE)))
        axs.append(VGroup(hbar(x-2.45,x+2.45,-1.85,h=.5),label('axon',x,-2.5,28,BLUE)))
    la=arrow([-3.25,-1.55,0],[-3.25,.05,0])
    ra=arrow([3.25,-1.55,0],[3.25,.05,0],True)
    return frames,cells,axs,la,ra


class S06Flip(SpokenScene):
    def construct(self):
        f,c,a,la,ra=halves()
        self.add(f,c[0],a[0],la,label('decides',-4.65,-.7,27,BLUE),label('Preview: two halves',0,3.5,26,GREY))
        self.at('in the brain')
        self.play(FadeIn(c[1]),run_time=.4)
        self.at('brings much of the program')
        prog=label('much of the program',3.25,0.6,26,PURPLE)
        # Move the cell name up inside its ellipse, leaving a separate program label.
        self.play(c[1][1].animate.move_to([3.25,1.55,0]),FadeIn(prog),run_time=.4)
        self.at('axon cues')
        self.play(FadeIn(a[1]),run_time=.4)
        self.at('activity')
        self.play(Create(ra),FadeIn(label('activity',1.8,-.5,26,BLUE)),run_time=.45)
        self.at('caliber')
        self.play(FadeIn(label('caliber',4.7,-.5,26,BLUE)),run_time=.4)
        self.at('bias it')
        self.play(FadeIn(label('bias',3.25,-3.0,27,BLUE)),run_time=.35)
        self.finish()


class S07Fish(SpokenScene):
    def construct(self):
        # A tapered transparent larva: rounded head, narrowing body and continuous tail.
        outline=VMobject(color=GREY,stroke_width=3,fill_color=GREY,fill_opacity=.1)
        outline.set_points_smoothly([[-5.8,0,0],[-5.2,1.35,0],[-3.4,1.6,0],[-.5,.95,0],[3,.45,0],[5.8,.95,0],[5.25,0,0],[5.8,-.95,0],[3,-.45,0],[-.5,-.95,0],[-3.4,-1.6,0],[-5.2,-1.35,0],[-5.8,0,0]])
        eye=Dot([-4.6,.5,0],radius=.23,color=TEXT)
        cord=hbar(-3.8,2.3,.15,h=.24)
        # Internal body line and fin make the transparent larva readable.
        notochord=Line([-4,-.3,0],[2.7,-.15,0],color=GREY,stroke_width=2)
        fin=ArcBetweenPoints([-2.5,-1.1,0],[-1.3,-.65,0],angle=1.0,color=GREY,stroke_width=2)
        fish=VGroup(outline,eye,notochord,fin)
        cl=label('spinal cord',.2,1.8,28,BLUE)
        title=label('Zebrafish larva',0,3.0,34)
        self.add(fish,cord,title)
        self.at('transparent spinal cords')
        self.play(FadeIn(cl),run_time=.4)
        tube=RoundedRectangle(width=12.2,height=5.3,corner_radius=.3,color=BLUE,stroke_width=2)
        ys=[1.6,0,-1.6]
        ax=VGroup(*[hbar(-5.7,5.7,y) for y in ys])
        self.at('first sheaths')
        # Expand the actual cord and its tiny fibres continuously into the panel.
        mini=ax.copy().stretch_to_fit_width(cord.width).stretch_to_fit_height(.15).move_to(cord)
        self.add(mini)
        self.play(ReplacementTransform(cord,tube),ReplacementTransform(mini,ax),
                  fish.animate.scale(2.0,about_point=cord.get_center()).set_opacity(0),
                  FadeOut(cl),FadeOut(title),run_time=1.0)
        self.remove(fish)
        self.add(label('Spinal cord · magnified',0,3.0,30,BLUE))
        sh=[sheath(a,a+1.5,y,.65) for y in ys for a in [-5,-2.2,.6,3.4]]
        self.at('filmed as they form')
        self.play(LaggedStart(*[GrowFromEdge(s,LEFT) for s in sh],lag_ratio=.12),run_time=1.25)
        self.at('most early wraps')
        gone=[s for i,s in enumerate(sh) if i not in [1,6,11]]
        self.play(*[s.animate.stretch(.015,0,about_point=s.get_left()).set_opacity(0) for s in gone],run_time=.9)
        self.wait(.35)
        self.play(FadeIn(label('most are withdrawn',0,-3.15,32,PURPLE)),run_time=.35)
        self.finish()


Y8=[1.65,.8,-.05,-.9,-1.75]
def tube8():
    tube=RoundedRectangle(width=12.1,height=4.8,corner_radius=.3,color=BLUE,stroke_width=2).move_to([0,-.1,0])
    ax=VGroup(*[hbar(-5.55,5.55,y,h=.25,color=RED if i==4 else BLUE) for i,y in enumerate(Y8)])
    dots=VGroup(*[Dot([x,y+.23,0],radius=.065,color=YELLOW) for y in Y8[:4] for x in np.arange(-5,5.1,1.2)])
    normal=label('normal neighbours',-3.6,2.65,26,BLUE)
    blocked=label('tetanus toxin · vesicle release blocked',0,-2.85,27,RED)
    legend=VGroup(Dot(radius=.07,color=YELLOW),T('yellow dot = vesicle release',26,YELLOW)).arrange(RIGHT,buff=.15).move_to([2.15,2.65,0])
    return tube,ax,dots,normal,blocked,legend


def predict():
    return label('Predict: will glia treat the red axon differently?',0,3.4,29)


def think():
    return label('Think: compare the red axon with its neighbours',0,-3.4,26)


class S08Q(SpokenScene):
    def construct(self):
        t,a,d,n,b,l=tube8()
        self.add(t,a,n,b)
        self.at('blocked vesicle release')
        self.play(Indicate(b,color=RED,scale_factor=1.02),run_time=.5)
        self.at('normal neighbors')
        self.play(FadeIn(d),FadeIn(l),run_time=.5)
        self.at('will oligodendrocytes')
        self.play(FadeIn(predict()),FadeIn(think()),run_time=.5)
        self.finish()


class S09Pause(SpokenScene):
    def construct(self):
        self.add(*tube8(),predict(),think())
        self.finish()


def results():
    nb=VGroup(*[sheath(a,a+2.0,y,.55) for y in Y8[:4] for a in [-5.25,-2.5,.25,3]])
    red=VGroup(*[sheath(a,a+.95,Y8[-1],.55) for a in [-2.7,1.7]])
    return nb,red


def result_label():
    return label('Release from the axon biases the choice',0,3.35,32)


class S10R(SpokenScene):
    def construct(self):
        t,a,d,n,b,l=tube8(); pr=predict(); th=think()
        self.add(t,a,d,n,b,l,pr,th)
        nb,red=results()
        self.at('yes')
        self.play(FadeOut(pr),FadeOut(th),run_time=.3)
        self.at('release blocked axon')
        self.play(Indicate(a[-1],color=RED,scale_factor=1),run_time=.45)
        self.at('wrapped less often')
        self.play(FadeOut(d),FadeOut(l),run_time=.25)
        self.play(LaggedStart(*[GrowFromEdge(s,LEFT) for s in nb],lag_ratio=1.0),run_time=1.25)
        self.at('sheaths were shorter')
        self.play(LaggedStart(*[GrowFromEdge(s,LEFT) for s in red],lag_ratio=.5),run_time=.8)
        self.play(FadeIn(label('fewer, shorter sheaths',2.5,-3.35,28,PURPLE)),run_time=.3)
        self.at('release from the axon biases')
        self.play(FadeIn(result_label()),run_time=.4)
        self.finish()


class S11Beat(SpokenScene):
    def construct(self):
        t,a,d,n,b,l=tube8()
        self.add(t,a,n,b,*results(),result_label(),label('fewer, shorter sheaths',2.5,-3.35,28,PURPLE)); self.finish()


class S12Gibson(SpokenScene):
    def construct(self):
        slab=RoundedRectangle(width=12.1,height=5.6,corner_radius=.3,color=GREY,stroke_width=2).move_to([0,-.1,0])
        ys=[1.35,-.35,-2.05]
        neurons=VGroup(*[Circle(radius=.46,color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([-5,y,0]) for y in ys])
        axs=VGroup(*[hbar(-4.6,5.6,y,h=.18) for y in ys])
        thin=VGroup(*[sheath(3.5,5.15,y,.28) for y in ys])
        thick=VGroup(*[sheath(3.5,5.15,y,.64) for y in ys])
        probe=Line([-5,3.1,0],[-5,2.15,0],color=GREY,stroke_width=7)
        cone=Polygon([-5,2.15,0],[-5.8,-2.35,0],[-4.2,-2.35,0],stroke_width=0,fill_color=GOLD,fill_opacity=.25)
        self.add(slab,neurons,axs,label('mouse premotor cortex',1.4,3.15,32),label('Gibson, Monje and colleagues, 2014',0,-3.3,26,GREY))
        self.at('stimulating neurons with light')
        self.play(FadeIn(probe),FadeIn(cone),FadeIn(label('light',-3.9,2.6,28,GOLD)),neurons.animate.set_fill(GOLD,opacity=.8),run_time=.7)
        self.play(LaggedStart(*[GrowFromEdge(w,LEFT) for w in thin],lag_ratio=.15),run_time=.4)
        cells=VGroup(); procs=VGroup(); wraps=VGroup()
        for y in ys:
            b,p=oligo([-1.0,y+.72],[(1.05,y)],.43)
            cells.add(b); procs.add(p); wraps.add(sheath(.35,2,y,.58))
        self.at('new oligodendrocytes')
        self.play(FadeIn(cells,scale=.6),FadeIn(label('new oligodendrocytes',1.25,2.45,27,PURPLE)),run_time=.4)
        self.play(Create(procs),run_time=.4)
        self.play(LaggedStart(*[GrowFromEdge(w,LEFT) for w in wraps],lag_ratio=.15),run_time=.55)
        self.at('thickened myelin')
        self.play(Transform(thin,thick),run_time=.7)
        self.finish()


def brain_shape():
    outline=VMobject(color=GREY,stroke_width=4,fill_color=GREY,fill_opacity=.15)
    # Lateral cortex: lobulated dome, flatter ventral surface, distinct hindbrain.
    pts=[[-2.2,-.65,0],[-2.55,-.2,0],[-2.5,.45,0],[-2.2,.85,0],[-1.95,1.35,0],[-1.4,1.55,0],[-.95,1.85,0],[-.35,1.8,0],[.25,1.9,0],[.85,1.65,0],[1.35,1.5,0],[1.7,1.05,0],[1.95,.55,0],[1.95,.05,0],[1.6,-.3,0],[.95,-.5,0],[.35,-.55,0],[-.25,-.65,0],[-.75,-.85,0],[-1.4,-.85,0],[-2.2,-.65,0]]
    outline.set_points_smoothly(pts)
    folds=VGroup()
    paths=[
        [[-.25,1.55,0],[-.55,1.05,0],[-.35,.6,0],[-.6,.1,0]],
        [[-2.1,.15,0],[-1.6,.4,0],[-1.05,.2,0],[-.5,.05,0],[.1,.15,0],[.8,.1,0],[1.5,.35,0]],
        [[-1.8,.95,0],[-1.3,1.1,0],[-1.05,.65,0]],
        [[.2,1.4,0],[.6,1.,0],[1.2,1.1,0]],
        [[.15,.55,0],[.5,.85,0],[.9,.55,0]],
        [[-1.75,-.3,0],[-1.2,-.15,0],[-.95,-.5,0]]]
    for points in paths:
        fold=VMobject(color=GREY,stroke_width=3);fold.set_points_smoothly(points);folds.add(fold)
    cerebellum=Ellipse(width=1.35,height=.85,color=GREY,fill_color=GREY,fill_opacity=.2).move_to([1.35,-.8,0])
    stem=VMobject(color=GREY,stroke_width=8).set_points_as_corners([[.6,-.65,0],[.45,-1.2,0],[.65,-1.55,0]])
    folds.add(cerebellum,stem)
    return VGroup(outline,folds)


class S13Open(SpokenScene):
    def construct(self):
        sources=VGroup(chip('larval fish',BLUE,30),chip('mouse cortex',BLUE,30)).arrange(DOWN,buff=.65).move_to([-4.1,.3,0])
        brain=brain_shape().scale(1.25).move_to([3.45,.3,0])
        link=DashedVMobject(Arrow([-1.9,.3,0],[.4,.3,0],buff=0,color=GREY,stroke_width=3,tip_length=.2),num_dashes=12)
        q=label('?',3.45,.5,125,'#FFFFFF')
        self.add(sources,brain,link,label('Evidence so far',-4.1,2.65,30),label('?',-.75,.95,60,'#FFFFFF'))
        self.at('larval fish')
        self.play(Indicate(sources[0],color=BLUE,scale_factor=1.04),run_time=.4)
        self.at('mouse cortex')
        self.play(Indicate(sources[1],color=BLUE,scale_factor=1.04),run_time=.4)
        self.at('adult humans')
        self.add(label('adult humans',3.45,-2.55,38,'#FFFFFF'),q)
        self.wait(.4)
        self.at('still open')
        self.play(FadeIn(label('still open',0,-3.3,32)),run_time=.3)
        self.finish()


class S14Take(SpokenScene):
    def construct(self):
        f,c,a,la,ra=halves()
        self.add(f,*c,*a)
        self.at('two halves')
        self.play(Indicate(VGroup(c[0],c[1]),color=PURPLE,scale_factor=1.02),run_time=.4)
        self.at('the axon decides')
        self.play(Create(la),FadeIn(label('decides',-4.65,-.7,28,BLUE)),run_time=.45)
        self.at('glia bring much of the program')
        self.play(c[1][1].animate.move_to([3.25,1.55,0]),FadeIn(label('much of the program',3.25,.65,26,PURPLE)),run_time=.5)
        self.at('axon tunes it')
        self.play(Create(ra),FadeIn(label('tunes',4.55,-.7,28,BLUE)),run_time=.45)
        self.finish()


class S15End(EndCard):
    LINE='Axon decides in nerve; in brain, glia lead and the axon tunes.'
    def construct(self):
        text=T('Axon decides in nerve;\nin brain, glia lead\nand the axon tunes.',38,font=TITLE_FONT,line_spacing=1.15)
        self.play(FadeIn(VGroup(text,T('biochemistrypedia.com',26,TEAL)).arrange(DOWN,buff=.6)),run_time=.5)
        self.finish()
