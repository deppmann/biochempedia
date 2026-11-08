"""Contacts Are Not Channels — reviewed revision.
COLOR MAP: BLUE hardware; YELLOW fields; TEAL channels; PURPLE neurons;
TEXT listeners/percepts; GREY structure; RED loss/negation.
Gaussian fields use 1.75 mm FWHM, 0.75 mm contact spacing.
Qualitative trends encode only rise/plateau or continued rise; no score data implied.
"""
import numpy as np
from bp_style import *
PURPLE='#B58CD9'
GREY='#BAC3CE'


def txt(s,x=0,y=0,size=28,color=TEXT):
    return T(s,size,color).move_to([x,y,0])


def path(points,color=BLUE,w=4,fill=0):
    return VMobject().set_points_as_corners([np.array([x,y,0]) for x,y in points]).set_stroke(color,w).set_fill(color,fill)


def contact(x,y,size=.24):
    return Square(side_length=size,color=BLUE,fill_opacity=.8).move_to([x,y,0])


def cell(x,y,r=.18):
    return VGroup(Circle(radius=r,color=PURPLE,fill_opacity=.6).move_to([x,y,0]),Line([x,y-r,0],[x,y-.65,0],color=PURPLE))


def person(x,y=0):
    return VGroup(Circle(radius=.55,color=TEXT).move_to([x,y+1,0]),RoundedRectangle(width=1.8,height=2.2,corner_radius=.4,color=TEXT).move_to([x,y-.5,0]),contact(x+.55,y+1.1,.3))


def dimension(x0,x1,y,text,color=GREY,above=False):
    return VGroup(Line([x0,y,0],[x1,y,0],color=color),*[Line([x,y-.10,0],[x,y+.10,0],color=color) for x in (x0,x1)],txt(text,(x0+x1)/2,y+(.3 if above else -.34),26,color))


def array_stage():
    return VGroup(RoundedRectangle(width=11.4,height=.6,corner_radius=.16,color=GREY).move_to([0,-1.8,0]),VGroup(*[contact(x,-1.8,.21) for x in np.linspace(-5.25,5.25,22)]))


def cloud(c=0,amp=3.6):
    sigma=(1.75/2.35482)*(10.5/15.75)
    xs=np.linspace(c-3.5*sigma,c+3.5*sigma,100)
    ys=-1.48+amp*np.exp(-.5*((xs-c)/sigma)**2)
    return path(list(zip(xs,ys))+[(xs[-1],-1.48),(xs[0],-1.48)],YELLOW,2,.08)


def packing():
    return VGroup(array_stage(),txt('22 contacts · 0.75 mm apart',0,3.15,30,BLUE),txt('Illustrative spread · chosen to fit',0,2.55,26,YELLOW),cloud(),dimension(-5.25,5.25,-2.5,'16 mm'),dimension(2.25,2.75,-1.12,'0.75 mm',BLUE,True),VGroup(dimension(-.583,.583,.32,'',YELLOW),txt('1.75 mm',-1.9,.85,28,YELLOW)),VGroup(txt('Non-overlapping stretches =',-.45,-3.4,32),txt('?',2.85,-3.4,46,TEAL)))


def plot_base(x=0,w=10.5,h=4.65,y=-.1):
    ax=Axes(x_range=[0,22,2],y_range=[0,1,1],x_length=w,y_length=h,axis_config={'color':GREY,'include_ticks':False,'include_tip':False}).move_to([x,y,0])
    nums=VGroup(*[txt(str(n),*ax.c2p(n,0)[:2],26,GREY).shift(DOWN*.3) for n in (0,8,10,22)])
    ticks=VGroup(*[Line(ax.c2p(n,0),ax.c2p(n,0)+DOWN*.12,color=GREY) for n in (0,8,10,22)])
    return VGroup(ax,nums,ticks,txt('Channels switched on',x,y-h/2-.95,26,TEAL),txt('Speech recognition',x,y+h/2+.35,28),txt('Reported trend · no numerical score scale',0,3.45,26,GREY))


def value(xs):
    # Concave, normalized rise with a flat section by 9; qualitative, not fitted data.
    z=np.clip(np.asarray(xs)/9,0,1)
    return .65*(2*z-z*z)


def trend(ax,continuing=False,color=TEXT):
    xs=np.linspace(0,15 if continuing else 22,181)
    ys=value(xs)
    if continuing: ys=ys+.025*np.maximum(xs-9,0)
    return path([tuple(ax.c2p(float(x),float(y))[:2]) for x,y in zip(xs,ys)],color,5)


def band(ax):
    lo=ax.c2p(8,0); hi=ax.c2p(10,1)
    return Rectangle(width=hi[0]-lo[0],height=hi[1]-lo[1],stroke_width=0,fill_color=YELLOW,fill_opacity=.25).move_to((lo+hi)/2)


def small_plot(x=3.7):
    p=plot_base(x,4.6,3.65,-.05)
    p.remove(p[-1])
    return VGroup(p,band(p[0]),trend(p[0]))


def anatomy():
    core=RoundedRectangle(width=2.35,height=5.6,corner_radius=.25,color=GREY,fill_opacity=.08).move_to([-4.7,-.15,0])
    ns=VGroup(*[cell(-3.95,y) for y in (-1.7,-.1,1.5)])
    chamber=RoundedRectangle(width=8.4,height=5.6,corner_radius=.35,color=GREY).move_to([.9,-.15,0])
    divider=Line([-3.3,0,0],[5.1,0,0],color=GREY)
    labels=VGroup(txt('Core / modiolus',-4.6,3.15,26),txt('Upper · scala vestibuli',.8,2.25,26,GREY),txt('Lower · scala tympani',.8,-2.4,26,GREY),txt('Nerve cell\nbodies',-5,-.25,24,'#D8B6FA'))
    straight=VGroup(Line([4.5,-1.9,0],[4.5,-.4,0],color=BLUE,stroke_width=7),*[contact(4.5,y) for y in np.linspace(-1.9,-.4,5)],txt('Straight',3.1,-.55,28,BLUE))
    pts=[(2.6,-1.8),(0,-1.8),(-2.5,-1.8),(-2.85,-1.3),(-2.85,-.8),(-2.85,-.3)]
    curved=VGroup(path(pts,BLUE,7),*[contact(x,y) for x,y in pts],txt('Precurved',-.1,-1.05,28,BLUE))
    return VGroup(core,ns,chamber,divider,labels),straight,curved


def prediction():
    # Same right-hand axes remain throughout prediction, pause and reveal.
    p=small_plot()
    p[2].set_stroke(opacity=.3)
    chamber=RoundedRectangle(width=4.7,height=4.5,corner_radius=.3,color=GREY).move_to([-3.6,-.1,0])
    ns=VGroup(*[cell(-5.25,y) for y in (-1.4,0,1.4)])
    pts=[(-1.8,-1.5),(-3,-1.5),(-4.4,-1.3),(-4.65,-.4)]
    arr=VGroup(path(pts,BLUE,7),*[contact(x,y) for x,y in pts])
    a=p[0][0]
    slot=DashedVMobject(RoundedRectangle(width=2.5,height=.85,corner_radius=.15,color=TEAL,stroke_opacity=.35).move_to([4.7,1.35,0]),num_dashes=20)
    return VGroup(chamber,ns,arr,txt('Well-placed precurved',-3.6,2.65,26,BLUE),txt('Scala tympani',-3.6,-2.7,26,GREY),p,slot,txt('?',4.7,1.35,48,TEAL),txt('What should this allow?',0,-3.5,30))


def linked(xs=(-3.8,0,3.8),top=.9,bottom=-.8):
    cs=VGroup(*[contact(x,top,.45) for x in xs])
    ns=VGroup(*[VGroup(*[cell(x+d,bottom) for d in (-.45,0,.45)]) for x in xs])
    ls=VGroup(*[Line([x,top-.23,0],[x,bottom+.2,0],color=TEAL,stroke_width=2) for x in xs])
    return VGroup(cs,ls,ns)


class S00Title(TitleCard):
    LESSON='Restoring Senses: Implants, Prostheses and Optogenetic Vision'
    TITLE='Contacts Are Not Channels'
    def construct(self):
        self.add(txt('BIOCHEMISTRYPEDIA',0,2.3,26,TEAL),txt('Restoring Senses: Implants, Prostheses\nand Optogenetic Vision',0,1,28,GREY),txt(self.TITLE,0,-.7,48),Line([-1.3,-1.7,0],[1.3,-1.7,0],color=GOLD))
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        panels=VGroup(*[RoundedRectangle(width=5.8,height=5.6,corner_radius=.25,color=GREY).move_to([x,0,0]) for x in (-3.3,3.3)])
        self.add(panels,person(-3.4).scale(1.3,about_point=[-3.4,0,0]),txt('Useful hearing',-3.3,2.3,32),txt('?',0,3.25,42,TEAL))
        arcs=VGroup(*[Arc(radius=r,start_angle=-.6,angle=1.2,color=YELLOW).move_to([-1.8,1,0]) for r in (.35,.65,.95)])
        self.add(Ellipse(width=4.5,height=2.9,color=GREY,stroke_opacity=.3).move_to([3.3,.25,0]),VGroup(*[Dot([3.3+dx,.25+dy,0],radius=.10,color=GREY).set_opacity(.2) for dx in (-.6,0,.6) for dy in (-.6,0,.6)])); self.at('A cochlear implant'); self.play(Create(arcs),run_time=.6)
        eye=VGroup(Ellipse(width=4.5,height=2.9,color=GREY).move_to([3.3,.25,0]),Circle(radius=1.1,color=PURPLE).move_to([3.3,.25,0]),txt('Retina',3.3,2.3,32,PURPLE))
        grid=VGroup(*[Dot([3.3+dx,.25+dy,0],radius=.10,color=TEXT).set_opacity(.25) for dx in (-.6,0,.6) for dy in (-.6,0,.6)])
        self.at('The same idea'); self.play(FadeIn(eye),FadeIn(grid),run_time=.5)
        self.at('gives streaks'); self.play(Create(Line([2.65,-.6,0],[3.95,1.1,0],color=TEXT,stroke_width=17)),run_time=.5)
        self.at('not pixels'); self.play(FadeIn(txt('Streaks, not pixels',3.3,-2.2,30)),run_time=.35)
        self.at('Why'); self.play(ReplacementTransform(self.mobjects[3],txt('Why the difference?',0,3.25,36,TEAL)),run_time=.3)
        self.finish()


class S02Map(SpokenScene):
    def construct(self):
        a=array_stage(); ns=VGroup(*[cell(x,1.1) for x in np.linspace(-5.1,5.1,8)])
        ruler=VGroup(*[Rectangle(width=.5,height=.25,stroke_width=0,fill_color=interpolate_color(ManimColor(TEAL),ManimColor(PURPLE),i/21),fill_opacity=.8).move_to([-5.25+i*.5,2.3,0]) for i in range(22)])
        ticks=VGroup(*[Line([x,2.15,0],[x,1.95,0],color=GREY) for x in np.linspace(-5.25,5.25,12)])
        self.add(ruler,ticks,txt('Unrolled cochlea · frequency map',0,3.35,30,TEAL),a[0])
        self.at('The implant'); self.play(FadeIn(a[1],shift=LEFT*5),run_time=.6)
        hair=VGroup(*[Line([x,-2.85,0],[x,-2.35,0],color=GREY) for x in (-.6,0,.6)],Line([-1,-2.95,0],[1,-2.25,0],color=RED),Line([-1,-2.25,0],[1,-2.95,0],color=RED),txt('Damaged hair cells · bypassed',0,-3.4,28,GREY))
        self.at('skips damaged'); self.play(FadeIn(hair),run_time=.4)
        links=VGroup(*[Line([x,-1.5,0],[x,.9,0],color=YELLOW,stroke_opacity=.5) for x in np.linspace(-5.1,5.1,8)])
        self.at('excites the auditory'); self.play(FadeIn(ns),Create(links),run_time=.6)
        pulses=VGroup(*[Dot([x,-1.5,0],radius=.09,color=YELLOW) for x in np.linspace(-5.1,5.1,8)])
        self.play(pulses.animate.shift(UP*2.4),run_time=.8); self.remove(pulses)
        self.at('High frequencies'); self.play(FadeIn(txt('HIGH · base',-4.1,2.85,28,TEAL)),run_time=.3)
        self.at('low toward'); self.play(FadeIn(txt('LOW · apex',4.1,2.85,28,TEAL)),run_time=.3)
        self.finish()


class S03Words(SpokenScene):
    def construct(self):
        xs=(-4.25,0,4.25)
        cards=VGroup(*[RoundedRectangle(width=3.7,height=5.9,corner_radius=.2,color=GREY).move_to([x,0,0]) for x in xs])
        self.add(cards.copy().set_opacity(.28),*[Arrow([x+1.85,0,0],[x+2.4,0,0],buff=0,color=GREY) for x in (-4.25,0)])
        self.at('A contact'); self.play(FadeIn(contact(-4.25,.8,.8)),cards[0].animate.set_color(BLUE),run_time=.4)
        self.add(cards[0])
        self.at('hardware on'); self.play(FadeIn(txt('Contact =\nhardware',-4.25,-1.4,30,BLUE)),run_time=.3)
        ruler=VGroup(Line([-1.4,.8,0],[1.4,.8,0],color=GREY),*[Line([x,.65,0],[x,.95,0],color=GREY) for x in np.linspace(-1.4,1.4,9)],Rectangle(width=.9,height=1,color=TEAL,fill_opacity=.3).move_to([0,.8,0]))
        self.at('A channel'); self.play(FadeIn(ruler),FadeIn(cards[1]),run_time=.4)
        self.at('band of frequencies'); self.play(FadeIn(txt('Channel =\nfrequency band',0,-1.4,28,TEAL)),run_time=.3)
        self.at('Truly separate'); self.play(FadeIn(VGroup(*[cell(x,.8) for x in (3.6,4.25,4.9)])),FadeIn(cards[2]),run_time=.4)
        self.at('groups of neurons'); self.play(FadeIn(txt('Neural group =\nseparate neurons',4.25,-1.4,27,PURPLE)),run_time=.3)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        g=packing(); self.add(g[0][0],g[0][1].copy().set_opacity(.2),g[7],txt('Predict',0,3.65,28,TEAL))
        self.at('Take'); self.play(LaggedStart(*[FadeIn(c) for c in g[0][1]],lag_ratio=.04),FadeIn(g[1]),run_time=.8)
        self.at('spanning about'); self.play(FadeIn(g[4]),FadeIn(g[5]),run_time=.4)
        self.at("Each contact's current"); self.play(Create(g[3]),FadeIn(g[2]),FadeIn(g[6]),run_time=.5)
        self.at('How many'); self.play(Indicate(g[7],color=TEAL),run_time=.4)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; g=packing(); self.add(g)
        q=g[7][1]
        for _ in range(5): self.play(q.animate.set_opacity(.25),run_time=.5); self.play(q.animate.set_opacity(1),run_time=.5)


class S06Reveal(SpokenScene):
    def construct(self):
        g=packing(); self.add(g[0],g[2],g[4])
        brackets=VGroup(*[dimension(-5.25+i*10.5/9,-5.25+(i+1)*10.5/9,.35,str(i+1),TEAL,True) for i in range(9)])
        self.at('About 9'); self.play(LaggedStart(*[FadeIn(b) for b in brackets],lag_ratio=.08),FadeIn(txt('16 mm ÷ 1.75 mm ≈ 9 stretches',0,3.2,32,TEAL)),run_time=1.15)
        caveat=txt('Toy 1-D packing · not a measured or predicted channel count',0,-3.35,26,GREY); self.add(caveat)
        clouds=VGroup(*[cloud(x) for x in np.linspace(-5.25,5.25,22)])
        self.at('Neighboring fields overlap'); self.play(FadeOut(brackets),FadeIn(clouds),run_time=.5)
        ns=VGroup(*[cell(x,.4,.24) for x in (-.5,0,.5)])
        self.at('same neurons'); self.play(FadeIn(ns),*[clouds[i].animate.set_stroke(YELLOW,4).set_fill(YELLOW,.2) for i in (9,10,11,12)],run_time=.4)
        self.at('This is called'); self.play(FadeOut(g[2]),FadeIn(txt('Channel interaction',0,2.55,32,YELLOW)),run_time=.3)
        self.finish()


class S07Plateau(SpokenScene):
    def construct(self):
        p=plot_base(h=4.5,y=-.1); preview=trend(p[0]).set_stroke(opacity=.3); self.add(p,preview,txt('Berg and colleagues, 2020 · n = 18 adults',0,2.95,26,GREY))
        tag=txt('1.75 mm: illustrative spread, chosen to fit',0,1.65,28,YELLOW); self.add(tag)
        self.at('In 18 implant users'); self.play(FadeOut(tag),run_time=.4)
        self.at('speech recognition'); self.play(preview.animate.set_stroke(opacity=1),run_time=.8)
        self.at('8 to 10 channels'); self.play(FadeIn(band(p[0])),run_time=.35)
        self.finish()


class S08OneReason(SpokenScene):
    def construct(self):
        p=plot_base(-2.8,6.3,4.6,-.1); p.remove(p[-1]); self.add(p,trend(p[0]),band(p[0]),txt('One main reason: channel interaction',0,3.4,30,YELLOW))
        cards=VGroup(*[RoundedRectangle(width=4.6,height=2.65,corner_radius=.15,color=GREY).move_to([4,y,0]) for y in (1.3,-1.75)])
        self.add(cards.copy().set_opacity(.25))
        ns=VGroup(*[cell(x,1.45) for x in (2.8,4,5.2)])
        loss=VGroup(*[VGroup(Line([x-.2,1.2,0],[x+.2,1.7,0],color=RED),Line([x+.2,1.2,0],[x-.2,1.7,0],color=RED)) for x in (4,5.2)])
        self.at('Neural survival'); self.play(FadeIn(cards[0]),FadeIn(ns),FadeIn(txt('Neural survival',4,2.2,28,PURPLE)),run_time=.25)
        self.play(ns[1:].animate.set_opacity(.2),FadeIn(loss),run_time=.3)
        short=VGroup(Line([3.75,-1.5,0],[4.7,-1.5,0],color=BLUE,stroke_width=6),Line([3.75,-2.15,0],[5.6,-2.15,0],color=BLUE,stroke_width=6),*[Line([x,-2.5,0],[x,-2.7,0],color=GREY) for x in np.linspace(2.4,5.6,9)])
        short.add(txt('Shallow',2.75,-1.5,24,BLUE),txt('Full',2.75,-2.15,24,BLUE))
        self.at('how far the array'); self.play(FadeIn(cards[1]),Create(short),FadeIn(txt('Insertion depth',4,-.85,28,BLUE)),run_time=.4)
        self.finish()


class S09Idea1(SpokenScene):
    def construct(self):
        frame=RoundedRectangle(width=12.5,height=6.7,corner_radius=.2,color=TEAL); g=linked(top=.65,bottom=-1.3)
        self.add(frame,txt('The one idea',0,2.75,32,TEAL),g.copy().set_opacity(.18),txt('Each group in its place on the map',0,-2.65,28,PURPLE))
        self.at('A prosthesis'); self.play(FadeIn(g[0]),run_time=.3)
        self.at('delivers detail'); self.play(FadeIn(txt('A prosthesis delivers detail only as far as it',0,1.95,31)),run_time=.35)
        self.at('drives distinct'); self.play(FadeIn(txt('drives distinct groups of neurons',0,1.25,31)),FadeIn(g[1:]),run_time=.4)
        self.wait(3.2)
        self.finish()


class S10Idea2(SpokenScene):
    def construct(self):
        left=linked((-4.7,-3.2,-1.7),.9,-1.1); right=linked((1.7,3.2,4.7),.9,-1.1)
        self.add(left,right,txt('Contacts ≠ channels',0,3.1,40),txt('Spatial detail only · not a formula',0,-3.25,28,GREY))
        fields=VGroup(*[Ellipse(width=2.4,height=2.1,color=YELLOW,fill_opacity=.12).move_to([x,-.1,0]) for x in (-4.7,-3.2,-1.7)])
        clean=VGroup(*[Ellipse(width=1.05,height=2.1,color=YELLOW,fill_opacity=.12).move_to([x,-.1,0]) for x in (1.7,3.2,4.7)])
        self.at('is not'); self.play(FadeIn(fields),FadeIn(clean),FadeIn(txt('Overlapping groups',-3.2,2.1,28,YELLOW)),FadeIn(txt('Distinct groups',3.2,2.1,28,TEAL)),run_time=.5)
        self.at('testing what'); self.play(FadeIn(txt('Measure what the listener can tell apart',0,-2.4,31,TEAL)),run_time=.3)
        self.finish()


class S11Test(SpokenScene):
    def construct(self):
        a,s,c=anatomy(); self.add(a,s)
        self.at('precurved'); self.play(FadeIn(c),run_time=.5)
        self.at('hug the inner'); self.play(c[0].animate.set_stroke(BLUE,10),run_time=.4)
        self.at('nerve cell bodies'); self.play(a[1].animate.set_stroke(PURPLE,4),run_time=.3)
        self.finish()


class S12Predict2(SpokenScene):
    def construct(self):
        g=prediction(); self.add(g[:-1])
        self.at('Predict'); self.play(FadeIn(txt('Predict',0,3.4,32,TEAL)),run_time=.3)
        self.at('If spread'); self.play(g[2].animate.set_stroke(YELLOW,6),run_time=.4)
        self.at('what should'); self.play(FadeIn(g[-1]),run_time=.3)
        self.finish()


class S13Pause(Scene):
    def construct(self):
        self.camera.background_color=BG; g=prediction(); self.add(g,txt('Predict',0,3.4,32,TEAL))
        for _ in range(5): self.play(g[7].animate.set_opacity(.25),run_time=.5); self.play(g[7].animate.set_opacity(1),run_time=.5)


class S14Reveal2(SpokenScene):
    def construct(self):
        g=prediction(); self.add(g[:6],txt('Reported trend · no numerical score scale',0,3.45,26,GREY))
        ax=g[5][0][0]
        self.at('More usable'); self.play(FadeIn(txt('More usable channels',-3.6,-3.45,30,TEAL)),FadeIn(txt('Berg and colleagues, 2019',3.6,-3.45,26,GREY)),Create(trend(ax,True,TEAL)),run_time=.7)
        end=ax.c2p(15,float(value(15))+.025*6)
        self.add(Circle(radius=.075,color=TEAL,fill_color=BG,fill_opacity=1).move_to(end))
        self.at('those listeners'); self.play(FadeIn(txt('Continued improvement',3.6,2.6,26,TEAL)),run_time=.3)
        self.finish()


def placement_row(y,kind):
    ns=VGroup(*[cell(-5.6,y+d,.14) for d in (-.3,.3)])
    x=-4.8 if kind=='Well-placed' else -2.8
    if kind=='Straight': pts=[(x,y+d) for d in (-.55,-.2,.2,.55)]
    else: pts=[(x+.4,y-.55),(x+.3,y-.2),(x,y+.2),(x-.15,y+.55)]
    arr=VGroup(path(pts,BLUE,6),*[contact(a,b,.18) for a,b in pts])
    dist=VGroup(DashedLine([-5.35,y,0],[x,y,0],color=YELLOW),*[Line([xx,y-.1,0],[xx,y+.1,0],color=YELLOW) for xx in (-5.35,x)])
    return VGroup(ns,arr,dist,txt(kind,-3.6,y+.92,26,BLUE))


class S15Placement(SpokenScene):
    def construct(self):
        p=small_plot(3.7); p[0][-1].move_to([3.7,2.05,0]); self.add(p,txt('Plateau group',0,3.45,34),txt('Straight or translocated arrays',3.7,2.85,24))
        well=placement_row(-2.05,'Well-placed'); self.add(well,txt('Modiolus',-5.5,2.95,26,PURPLE))
        self.at('straight arrays'); self.play(FadeIn(placement_row(1.6,'Straight')),run_time=.35)
        trans=placement_row(-.05,'Translocated')
        self.at('or precurved'); self.play(FadeIn(trans),run_time=.35)
        self.at('crossed into'); self.play(FadeIn(Line([-6.2,.05,0],[-.7,.05,0],color=GREY,stroke_opacity=.85)),FadeIn(txt('Upper\nchamber',-.2,.65,26,GREY)),run_time=.35)
        self.at('farther from'); self.play(FadeIn(txt('Proposed explanation: more channel interaction',0,-3.4,28,YELLOW)),run_time=.3); self.wait(5)
        self.finish()


class S16NoSingle(SpokenScene):
    def construct(self):
        self.add(txt('No single channel number',0,3.2,40))
        xs=(-4.3,0,4.3)
        cards=VGroup(*[RoundedRectangle(width=3.7,height=5.7,corner_radius=.2,color=GREY).move_to([x,-.15,0]) for x in xs])
        listener=person(-4.3,.2).scale(1.3,about_point=[-4.3,.2,0])
        placement=VGroup(*[cell(-1.25,y,.23) for y in (-.8,.8)],*[contact(.85,y,.36) for y in (-1.1,-.4,.4,1.2)],Line([.85,-1.1,0],[.85,1.2,0],color=BLUE,stroke_width=8),DashedLine([-.95,.2,0],[.65,.2,0],color=YELLOW))
        ax=Axes(x_range=[0,22,2],y_range=[0,1,1],x_length=2.85,y_length=3.25,axis_config={'include_ticks':False,'include_tip':False,'color':GREY}).move_to([4.3,.25,0])
        test=VGroup(ax,band(ax),trend(ax).set_stroke(width=6))
        drawings=[listener,placement,test]
        labels=VGroup(*[txt(name,x,-2.45,30,TEAL if name=='Test' else TEXT) for name,x in zip(('Listener','Placement','Test'),xs)])
        self.add(cards)
        ghosts=VGroup(*[d.copy().set_stroke(opacity=.2).set_fill(opacity=0) for d in drawings]); self.add(ghosts)
        self.at('the listener'); self.play(FadeIn(labels),run_time=.18)
        self.remove(ghosts[0]); self.play(FadeIn(listener),run_time=.18)
        self.at('the placement'); self.remove(ghosts[1]); self.play(FadeIn(placement),run_time=.18)
        self.at('the test'); self.remove(ghosts[2]); self.play(FadeIn(test),run_time=.18)
        self.wait(4.5)
        self.finish()


class S17Payoff(SpokenScene):
    def construct(self):
        self.add(txt('A large gain',0,3.2,40),person(-4.8,.1))
        # A broken qualitative axis and floating endpoints show only the change.
        axis=VGroup(Line([-2.6,-2.2,0],[-2.6,-1.75,0],color=GREY),Line([-2.6,-1.4,0],[-2.6,2.1,0],color=GREY),path([(-2.8,-1.75),(-2.4,-1.6),(-2.8,-1.45)],GREY,3),txt('CNC words correct (%)',.1,2.45,28))
        self.at('In 96 adults'); self.play(FadeIn(axis),FadeIn(txt('96 adults · Six months',3.4,-2.05,28,GREY)),run_time=.4)
        bracket=VGroup(Line([-.7,-.95,0],[-.7,1.35,0],color=YELLOW,stroke_width=5),Line([-1,-.95,0],[-.4,-.95,0],color=YELLOW),Line([-1,1.35,0],[-.4,1.35,0],color=YELLOW),txt('Before implant',-1,-1.35,26,GREY),txt('After implant',-1,1.8,26,GREY))
        self.at('word scores rose'); self.play(Create(bracket),FadeIn(txt('+40.5',1.5,.55,48,YELLOW)),FadeIn(txt('percentage points',2.1,-.15,28)),FadeIn(txt('Gain only\nAbsolute scores not shown',3.6,-1.1,28,YELLOW)),run_time=.6)
        self.at('with the implant'); self.play(FadeIn(txt('Implant + hearing aid in the other ear',0,-3.18,28,BLUE)),FadeIn(txt('Buchman et al., 2020 · model-estimated mean gain',0,-3.65,26,GREY)),run_time=.3)
        self.finish()


class S18Takeaway(SpokenScene):
    def construct(self):
        g=linked((-4.5,-1.8,1.8,4.5),1.5,-1.7)
        for group in g[2]: group.scale(1.18,about_point=group.get_top())
        fields=VGroup(*[Ellipse(width=w,height=4.25,color=YELLOW,fill_opacity=.12).move_to([x,-.4,0]) for x,w in ((-4.5,3.3),(-1.8,3.3),(1.8,1.2),(4.5,1.2))])
        self.add(g,fields,txt('How distinctly does it drive separate groups?',0,2.95,33))
        self.at('drives separate'); self.play(g[2].animate.set_stroke(PURPLE,4),run_time=.4)
        self.at('test what',lead=.3); self.play(FadeIn(txt('Test what the listener can tell apart',0,-3.25,33,TEAL)),run_time=.25)
        self.wait(4.5)
        self.finish()


class S19End(EndCard):
    LINE='Contacts are not channels: test what listeners can tell apart.'
    def construct(self):
        self.add(txt('Contacts are not channels:\ntest what listeners can tell apart.',0,.25,40),txt('biochemistrypedia.com',0,-1.3,26,TEAL)); self.finish()
