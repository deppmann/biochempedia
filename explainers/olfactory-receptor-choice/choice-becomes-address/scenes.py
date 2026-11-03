"""Chapter 5: The Choice Becomes an Address.

COLOR MAP (shared with scenes.old.py): BLUE = replacement receptor gene;
ORANGE = expressed receptor; GREEN = held choice; PURPLE = stress relay;
YELLOW = intracellular cAMP; TEAL = lesson pointer; GOLD = title rule;
GREY = anatomy / neutral inputs; TEXT = guidance genes and proteins.
All anatomy, bars and meters are qualitative cartoons, not measured traces.
The lesson supplies no signed activity/expression or cAMP/axis relationship:
comparison states therefore explicitly omit direction and numerical values.
"""
from bp_style import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LESSON = "One Receptor per Neuron: How Olfactory Neurons Choose"


def label(s, x=0, y=3.15, color=TEXT, size=28):
    return T(s, size=size, color=color).move_to([x, y, 0])


def arr(a, b, color=GREY):
    return Arrow(a, b, buff=0, stroke_width=5, color=color,
                 max_tip_length_to_length_ratio=0.18)


def box(s, x, y, color=TEXT, size=30):
    b = chip(s, color, size=size).move_to([x, y, 0])
    b[1].set_color(TEXT)
    return b


def cell(x, y, color=ORANGE, r=0.8):
    body = Circle(radius=r, color=GREY, fill_color=GREY, fill_opacity=0.08).move_to([x,y,0])
    receptor = RoundedRectangle(width=0.32, height=0.64, corner_radius=0.08,
                                color=color, fill_color=color, fill_opacity=0.75).move_to([x-r,y,0])
    return VGroup(body, receptor)


def tip(x=4.9, y=0, scale=1):
    return VGroup(Line([x-1.0*scale,y,0],[x,y,0], color=TEXT, stroke_width=7),
                  *[Line([x-0.2*scale,y,0],[x+0.65*scale,y+d*scale,0], color=TEXT, stroke_width=5)
                    for d in (-0.75,0,0.75)])


def bulb():
    return VGroup(Ellipse(width=4.8,height=5.6,color=GREY,fill_color=GREY,fill_opacity=0.07).move_to([3.5,0,0]),
                  label("olfactory bulb",3.5,3.15))


def nose_neurons(colors=(ORANGE,BLUE,GREEN)):
    return VGroup(*[cell(-4.8,y,c,0.8) for y,c in zip((2,0,-2),colors)])


def lock_icon(x=3.4,y=1.5,scale=1):
    body=RoundedRectangle(width=1.65,height=1.2,corner_radius=0.14,color=GREEN,
                          fill_color=GREEN,fill_opacity=0.15).move_to([0,0,0])
    shackle=Arc(radius=0.52,start_angle=0,angle=PI,color=GREEN,stroke_width=6).move_to([0,0.9,0])
    legs=VGroup(Line([-.52,.85,0],[-.52,.5,0],color=GREEN,stroke_width=6),
                Line([.52,.85,0],[.52,.5,0],color=GREEN,stroke_width=6))
    keyhole=VGroup(Dot([0,.1,0],radius=.11,color=GREEN),Line([0,.1,0],[0,-.25,0],color=GREEN,stroke_width=6))
    return VGroup(body,shackle,legs,keyhole).scale(scale).move_to([x,y,0])


def question_frame():
    c=cell(-3.5,-.15,ORANGE,2.15)
    n=Circle(radius=.9,color=GREY).move_to([-3.05,-.4,0])
    ax=Line([-1.36,-.4,0],[4.65,-.4,0],color=GREY,stroke_width=6)
    t=tip(4.7,-.4,1.3)
    q=label("?",.6,1.0,RED,70)
    dash=VGroup(DashedLine([-1.2,1,0],[.05,1,0],color=GREY),
                DashedLine([1.15,1,0],[4.7,1,0],color=GREY))
    labs=VGroup(label("receptor",-4.9,2.45,ORANGE),label("nucleus",-3.05,-2.95),
                label("growing axon",3.8,-2.95),
                label("How could it change what the axon carries?",0,3.2,TEXT,30))
    leaders=VGroup(Line([-4.9,2.1,0],[-5.65,.2,0],color=ORANGE),
                   Line([-3.05,-2.65,0],[-3.05,-1.3,0],color=GREY),
                   Line([3.8,-2.65,0],[5.545,-1.375,0],color=GREY))
    return VGroup(c,n,ax,t,q,dash,labs,leaders)


def camp_frame():
    c=cell(-3.1,-.1,ORANGE,2.5)
    c[1].move_to([-5.6,.7,0])
    n=Circle(radius=.96,color=GREY,fill_color=GREY,fill_opacity=.06).move_to([-2.5,-.65,0])
    ax=Line([-.65,-.65,0],[4.9,-.65,0],color=GREY,stroke_width=7)
    t=tip(4.9,-.65,1.25)
    ca=box("cAMP",-3.7,1.1,YELLOW,32)
    genes=VGroup(*[Rectangle(width=.3,height=.6,color=TEXT,fill_color=TEXT,fill_opacity=.25)
                       .move_to([-2.95+i*.45,-.7,0]) for i in range(3)])
    signals=VGroup(arr([-5.42,.7,0],ca.get_left(),YELLOW),arr(ca.get_bottom(),genes[0].get_top(),YELLOW))
    proteins=VGroup(*[RoundedRectangle(width=.35,height=.75,corner_radius=.07,color=TEXT,
                      fill_color=TEXT,fill_opacity=.7).move_to([x,-.65,0]) for x in (1.3,2.5,3.7)])
    labs=VGroup(label("guidance genes",-2.6,-3.13,TEXT,28),label("guidance proteins",2.6,-2.5,TEXT,28),
                label("receptor",-4.7,2.73,ORANGE,28))
    leaders=VGroup(Line([-2.6,-2.82,0],[-2.6,-1.62,0],color=GREY),
                   Line([2.6,-2.17,0],[2.6,-1.04,0],color=GREY),
                   Line([-5,2.4,0],[-5.6,1.02,0],color=ORANGE))
    return VGroup(c,n,ax,t,ca,genes,signals,proteins,labs,leaders)


def lock_chain():
    nodes=VGroup(box("Receptor",-4.8,2.2,ORANGE,30),box("PERK",-1.65,2.2,PURPLE,32),
                 box("eIF2α",1.2,2.2,PURPLE,32),box("ATF5",4.25,2.2,PURPLE,32),
                 box("Adcy3",4.25,0,PURPLE,32),box("Lsd1 turned down",.3,0,PURPLE,30))
    greek=T("eIF2α",size=32,font="Arial",color=TEXT).move_to(nodes[2][1])
    nodes[2][1].become(greek)
    arrows=VGroup(*[arr(nodes[i].get_right(),nodes[i+1].get_left(),PURPLE) for i in range(3)],
                  arr(nodes[3].get_bottom(),nodes[4].get_top(),PURPLE),
                  arr(nodes[4].get_left(),nodes[5].get_right(),PURPLE))
    lock=lock_icon(-3.8,-1.85,1.15)
    stable=label("Hold the choice",-.2,-2.5,GREEN,36)
    end=arr(nodes[5].get_bottom(),lock.get_right(),PURPLE)
    ring=SurroundingRectangle(nodes[1],buff=.15,color=PURPLE,corner_radius=.18,stroke_width=5)
    return VGroup(nodes,arrows,lock,stable,end,ring)


def fork_frame():
    p=box("PERK",-4.6,0,PURPLE,48)
    lock=lock_icon(3.0,1.35,1.5)
    held=label("Hold the choice",3.0,2.95,GREEN,38)
    ax=tip(3.5,-1.25,1.85)
    tuned=label("Tune the address",3.0,-2.95,TEXT,38)
    junction=[-1.7,0,0]
    stem=arr(p.get_right(),junction,PURPLE)
    upper=arr(junction,lock.get_left(),PURPLE)
    lower=arr(junction,ax.get_left(),PURPLE)
    labs=VGroup(label("stress signal",-4.6,1.0,PURPLE,30),label("choice",-.2,1.6,GREEN,30),
                label("axon",-.2,-1.8,TEXT,30))
    return VGroup(p,VGroup(lock,held),VGroup(ax,tuned),upper,lower,stem,labs)


class S00Title(TitleCard):
    LESSON = LESSON
    TITLE = "The Choice Becomes an Address"

    def construct(self):
        self.add(label("BIOCHEMISTRYPEDIA",0,2.3,TEAL,26),
                 label("One Receptor per Neuron:",0,1.4,GREY,28),
                 label("How Olfactory Neurons Choose",0,.85,GREY,28))
        title=T(self.TITLE,size=44,font=TITLE_FONT).move_to([0,-.5,0])
        self.play(FadeIn(title),Create(Line([-1.2,-1.5,0],[1.2,-1.5,0],color=GOLD)),run_time=.7)
        self.finish()


class S01(SpokenScene):
    def construct(self):
        cells=nose_neurons(); b=bulb()
        self.add(cells,b,label("nose",-4.8,3.15))
        self.at("A neuron has")
        self.play(Indicate(cells[0][1],color=ORANGE),run_time=.6)
        self.at("How does its axon")
        paths=VGroup(*[CubicBezier([-4,y,0],[-2,y,0],[0,y*.7,0],[2.8,y*.7,0],color=c,stroke_width=6)
                       for y,c in zip((2,0,-2),(ORANGE,BLUE,GREEN))])
        self.play(Create(paths),FadeIn(label("?",4.4,0,RED,80)),run_time=.85)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        cells=VGroup(*[cell(-4.8,y,ORANGE,.65) for y in (2.25,.75,-.75,-2.25)])
        b=bulb()
        self.add(cells,b,label("same receptor",-4.6,3.15,ORANGE,28))
        gl=VGroup(*[Circle(radius=.4,color=ORANGE,fill_color=ORANGE,fill_opacity=.4).move_to([3.5,y,0]) for y in (1.25,-1.25)])
        self.at("one receptor")
        self.play(*[Indicate(c[1],color=ORANGE) for c in cells],run_time=.5)
        self.at("two glomeruli")
        self.play(FadeIn(gl),FadeIn(label("two glomeruli per bulb",2.8,-3.3,ORANGE,28)),run_time=.5)
        self.at("each neuron's axon")
        paths=VGroup(*[CubicBezier([-4.15,y,0],[-2,y,0],[0,z,0],[3.5,z,0],color=ORANGE,stroke_width=5)
                       for y,z in ((2.25,1.25),(.75,1.25),(-.75,-1.25),(-2.25,-1.25))])
        self.play(Create(paths),run_time=.8)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        # The gene itself is a coloured segment in the DNA rail; labels float clear.
        rail=VGroup(Line([-5.7,0,0],[-1.65,0,0],color=GREY,stroke_width=10),
                    Line([1.65,0,0],[5.7,0,0],color=GREY,stroke_width=10))
        old=VGroup(Rectangle(width=3.3,height=.6,color=ORANGE,fill_color=ORANGE,fill_opacity=.65),
                   label("original receptor gene",0,-.9,ORANGE,30))
        new=VGroup(Rectangle(width=3.3,height=.6,color=BLUE,fill_color=BLUE,fill_opacity=.65).move_to([0,2,0]),
                   label("replacement receptor gene",0,2.8,BLUE,30))
        self.add(rail,old,label("DNA",-5.3,-.65,GREY,28),label("Mouse receptor-gene swap",0,-3.1,TEXT,34))
        self.at("and colleagues")
        self.play(FadeIn(label("Mombaerts and colleagues, 1996",0,3.4,GREY,28)),run_time=.4)
        self.at("swapped receptor genes")
        cuts=VGroup(*[Line([x,-.5,0],[x,.5,0],color=TEXT,stroke_width=4) for x in (-1.65,1.65)])
        self.play(*[Create(c) for c in cuts],old[0].animate.shift(UP*1.55),run_time=.5)
        self.play(FadeOut(old),FadeOut(cuts),FadeIn(new),run_time=.4)
        self.play(new.animate.shift(DOWN*2),run_time=.65)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        b=bulb(); c=cell(-4.8,0,BLUE,1.15)
        target=Circle(radius=.4,color=BLUE).move_to([4.3,1.35,0])
        old=Circle(radius=.4,color=GREY).move_to([3.2,-1.35,0])
        path=CubicBezier([-3.65,0,0],[-1,0,0],[1,-1.35,0],[3.2,-1.35,0],color=BLUE,stroke_width=6)
        oldlab=label("original target",.1,-2.15,GREY,28)
        newlab=label("expected new target",-.8,2.3,BLUE,28)
        leaders=VGroup(Line([1,-1.96,0],[2.9,-1.55,0],color=GREY),
                       Line([1.3,2.3,0],[4.1,1.7,0],color=BLUE))
        self.add(b,c,target,old,path,oldlab,newlab,leaders)
        self.at("receptor identity")
        self.play(Transform(path,CubicBezier([-3.65,0,0],[-1,0,0],[1,.45,0],[3.1,.45,0],color=BLUE,stroke_width=6)),run_time=1)
        self.at("is instructive")
        text=label("instructive",0,-3.2,BLUE,36)
        self.play(FadeIn(text),run_time=.4)
        self.at("but not the only factor")
        gap=DashedLine([3.1,.45,0],[4.3,1.35,0],color=GREY)
        bracket=VGroup(Line([3.15,.15,0],[4.45,1.05,0],color=GREY),
                       Line([3.02,.32,0],[3.28,-.02,0],color=GREY),
                       Line([4.32,1.22,0],[4.58,.88,0],color=GREY))
        self.play(Create(gap),Create(bracket),Transform(text,label("instructive, not exclusive",0,-3.2,BLUE,36)),run_time=.6)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        t=tip(3.4,0,2.2)
        rc=box("Receptor",-4.3,2.25,ORANGE,36)
        other=VGroup(*[Square(side_length=.9,color=GREY,fill_color=GREY,fill_opacity=.25).move_to([-4.3,y,0]) for y in (0,-2.25)])
        self.add(t,rc)
        self.at("the receptor")
        self.play(GrowArrow(arr(rc.get_right(),t.get_left(),ORANGE)),run_time=.45)
        self.at("one input among several")
        self.play(FadeIn(other),*[GrowArrow(arr(o.get_right(),t.get_left())) for o in other],
                  FadeIn(label("One input among several",0,3.25,TEXT,34)),run_time=.6)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        q=question_frame()
        self.add(q[0],q[1],q[2],q[3],q[6][0],q[6][1],q[6][2],q[7])
        self.at("the receptor helps")
        self.play(Indicate(q[0][1],color=ORANGE),run_time=.5)
        self.at("how could it change")
        self.play(Create(q[5]),FadeIn(q[4]),FadeIn(q[6][3]),run_time=.65)
        self.finish()


class S08Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        q=question_frame(); self.add(q)
        self.play(q[5].animate.set_color(TEAL),rate_func=there_and_back,run_time=2.5)
        self.play(q[4].animate.scale(1.15),rate_func=there_and_back,run_time=2.5)


class S09(SpokenScene):
    def construct(self):
        f=camp_frame()
        self.add(*f[:4],f[8][2],f[9][2])
        self.at("One route runs through")
        self.play(FadeIn(f[4]),GrowArrow(f[6][0]),run_time=.7)
        self.at("and colleagues reported")
        self.play(FadeIn(label("Imai and colleagues, 2006",1.4,3.25,GREY,28)),run_time=.45)
        self.at("signals shift")
        self.play(GrowArrow(f[6][1]),FadeIn(f[5]),FadeIn(f[8][0]),Create(f[9][0]),run_time=.45)
        self.play(f[5].animate.set_fill(YELLOW,.9).set_stroke(YELLOW),run_time=.4)
        self.at("guidance molecule expression")
        dots=VGroup(*[Dot([-2.5,-.65,0],radius=.10,color=TEXT) for _ in range(3)])
        self.add(dots)
        self.play(LaggedStart(*[d.animate.move_to([x,-.65,0]) for d,x in zip(dots,(1.3,2.5,3.7))],lag_ratio=.2),run_time=.8)
        self.play(FadeOut(dots),FadeIn(f[7]),FadeIn(f[8][1]),Create(f[9][1]),run_time=.4)
        self.finish()


class S10Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        f=camp_frame(); f[5].set_fill(YELLOW,.9).set_stroke(YELLOW)
        self.add(f,label("Imai and colleagues, 2006",1.4,3.25,GREY,28))
        self.wait(2.5)


class S11(SpokenScene):
    def construct(self):
        self.add(bulb())
        c=VGroup(*[cell(-4.8,y,ORANGE,.65) for y in (1.35,0,-1.35)])
        self.add(c,label("front",1.6,3.05,TEXT,28),label("back",5.4,3.05,TEXT,28),
                 DoubleArrow([1.8,2.35,0],[5.2,2.35,0],buff=0,color=GREY),
                 label("Illustrative shift along the front-to-back axis",0,-3.3,GREY,26))
        ys=(.8,0,-.8)
        # All endpoints shift together. The dial marks two unnamed cAMP states,
        # so this cartoon asserts no low/high mapping onto the anatomical axis.
        starts=(2.8,3.2,3.6)
        ends=(3.8,4.2,4.6)
        paths=VGroup(*[CubicBezier([-4.15,sy,0],[-1,sy,0],[1,y,0],[x,y,0],color=ORANGE,stroke_width=5)
                      for x,y,sy in zip(starts,ys,(1.35,0,-1.35))])
        pts=VGroup(*[Dot([x,y,0],radius=.18,color=ORANGE) for x,y in zip(starts,ys)])
        self.add(paths,pts)
        meter=VGroup(Line([-5.3,-2.3,0],[-1.8,-2.3,0],color=YELLOW,stroke_width=5),
                     Dot([-4.9,-2.3,0],color=YELLOW,radius=.13),
                     label("cAMP level changes",-3.55,-2.85,YELLOW,28))
        self.at("It also shifts")
        self.play(FadeIn(meter),run_time=.4)
        self.at("where axons project")
        newpaths=VGroup(*[CubicBezier([-4.15,sy,0],[-1,sy,0],[1,y,0],[x,y,0],color=ORANGE,stroke_width=5)
                         for x,y,sy in zip(ends,ys,(1.35,0,-1.35))])
        self.play(Transform(paths,newpaths),*[p.animate.move_to([x,y,0]) for p,x,y in zip(pts,ends,ys)],
                  meter[1].animate.move_to([-2.2,-2.3,0]),run_time=1)
        self.at("along the front")
        self.play(Indicate(pts,color=ORANGE),run_time=.6)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        names=("Kirrel2","Kirrel3","ephrin-A5","EphA5")
        def panel(x,title,heights):
            frame=RoundedRectangle(width=5.85,height=5.5,corner_radius=.2,color=GREY).move_to([x,.15,0])
            content=VGroup(frame,label(title,x,2.35,TEXT,32))
            for dx,name,h in zip((-2.1,-.7,.7,2.1),names,heights):
                content.add(Rectangle(width=.62,height=2.8,color=GREY).move_to([x+dx,.1,0]),
                            Rectangle(width=.54,height=h,color=TEXT,fill_color=TEXT,fill_opacity=.65)
                            .move_to([x+dx,-1.3+h/2,0]),label(name,x+dx,-1.85,TEXT,22))
            return content
        # Simultaneous fixed states: no ordered activity levels or animated heights.
        panels=VGroup(panel(-3.1,"one activity level",(1.7,2.5,1.0,2.0)),
                      panel(3.1,"another activity level",(2.4,1.3,1.9,.8)))
        self.add(panels,label("Expression levels • illustrative comparisons",0,-2.95,TEXT,28),
                 label("Serizawa and colleagues, 2006",0,3.4,GREY,28))
        self.at("found four")
        self.play(Indicate(VGroup(*[p[i] for p in panels for i in (4,7,10,13)]),color=TEXT),run_time=.5)
        self.at("whose levels vary")
        self.play(Circumscribe(panels,color=GREY),run_time=.7)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        # Retain the preceding four-molecule motif as the source of the pointer.
        mini=VGroup(*[Rectangle(width=.45,height=h,color=TEXT,fill_color=TEXT,fill_opacity=.5)
                        .move_to([-5.5+i*.65,-1.9+h/2,0]) for i,h in enumerate((2.3,1.4,2,1))])
        page=RoundedRectangle(width=7.8,height=5.4,corner_radius=.2,color=TEAL,
                              fill_color=TEAL,fill_opacity=.05).move_to([1.7,0,0])
        title=label("Topographic maps lesson",1.7,1.95,TEAL,34)
        grid=VGroup(*[Line([x,-1.7,0],[x,.8,0],color=GREY,stroke_width=2) for x in (-.5,.6,1.7,2.8,3.9)],
                    *[Line([-.5,y,0],[3.9,y,0],color=GREY,stroke_width=2) for y in (-1.7,-.87,0,.8)])
        dots=VGroup(*[Dot([x,y,0],color=TEAL,radius=.16) for x,y in ((0,-1.2),(1.15,-.65),(2.3,0),(3.45,.5))])
        self.add(mini,page,title,grid,dots,label("molecules → map",1.7,-2.15,TEXT,30))
        self.at("How such molecules")
        self.play(Indicate(mini,color=TEXT),run_time=.6)
        self.at("covered in the lesson")
        self.play(GrowArrow(arr(mini.get_right(),page.get_left(),TEAL)),run_time=.5)
        self.at("on topographic maps")
        self.play(Circumscribe(title,color=TEAL),run_time=.6)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        c=lock_chain(); self.add(c)
        self.at("Now recall the lock")
        self.play(Indicate(c[2],color=GREEN),run_time=.6)
        self.at("Its relay ran through")
        self.play(Circumscribe(c[0][1],color=PURPLE),run_time=.8)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        c=lock_chain().scale(.9).shift(DOWN*.65); self.add(c)
        self.at("pathway reaches")
        genes=box("Guidance genes",3.2,2.85,TEXT,38)
        start=c[5].get_top()
        elbow=[start[0],2.85,0]
        branch=VGroup(DashedLine(start,elbow,buff=0,color=PURPLE,stroke_width=5),
                      DashedLine(elbow,genes.get_left(),buff=0,color=PURPLE,stroke_width=5))
        link=label("link ?",-.5,3.35,PURPLE,28)
        self.play(Create(branch),FadeIn(genes),FadeIn(link),run_time=.7)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        xs=(-4.35,0,4.35)
        cells=VGroup(*[cell(x,0,c,1.6) for x,c in zip(xs,(ORANGE,BLUE,"#E07C92"))])
        names=VGroup(*[label("sequence "+n,x,2.25,c,30) for x,n,c in zip(xs,"ABC",(ORANGE,BLUE,"#E07C92"))])
        self.add(label("Shayya and colleagues, 2022",0,3.3,TEXT,32),cells,names)
        self.at("and colleagues reported")
        self.play(*[Indicate(c[1]) for c in cells],run_time=.5)
        self.at("different receptor sequences")
        self.play(Indicate(names),run_time=.5)
        self.at("different patterns of stress")
        meters=VGroup()
        for x,w in zip(xs,(.5,2.2,1.3)):
            er=box("ER",x,.65,PURPLE,28)
            rail=Rectangle(width=2.65,height=.4,color=PURPLE).move_to([x,-.35,0])
            fill=Rectangle(width=w,height=.3,color=PURPLE,fill_color=PURPLE,fill_opacity=.75).move_to([x-1.27+w/2,-.35,0])
            ends=VGroup(label("less",x-.65,-.85,PURPLE,24),label("more",x+.65,-.85,PURPLE,24))
            meters.add(VGroup(er,rail,fill,ends,Line(er.get_bottom(),rail.get_top(),color=PURPLE)))
        self.play(FadeIn(meters),FadeIn(label("ER stress • qualitative schematics",0,-2.7,PURPLE,30)),run_time=.6)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        pk=box("PERK",-4.8,0,PURPLE,36)
        dd=box("Ddit3",-1.55,0,PURPLE,38)
        genes=VGroup(box("Guidance genes",3.5,1.6,TEXT,32),box("Adhesion genes",3.5,-1.6,TEXT,32))
        frame=RoundedRectangle(width=4.9,height=5.6,corner_radius=.3,color=GREY,fill_opacity=0).move_to([3.5,-.1,0])
        cluster=VGroup(*[Rectangle(width=.3,height=.45,color=TEXT,fill_color=TEXT,fill_opacity=.35)
                         .move_to([2.8+i*.7,y,0]) for y in (.65,-2.55) for i in range(3)])
        self.add(pk,label("Stress signalling → wiring genes",0,3.2,TEXT,34))
        self.at("A gene called")
        self.play(FadeIn(dd),GrowArrow(arr(pk.get_right(),dd.get_left(),PURPLE)),run_time=.5)
        self.at("links perk")
        self.play(Indicate(dd,color=PURPLE),run_time=.5)
        self.at("to guidance and adhesion")
        self.play(FadeIn(frame),FadeIn(genes),FadeIn(cluster),
                  *[GrowArrow(arr(dd.get_right(),g.get_left(),PURPLE)) for g in genes],run_time=.65)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        f=fork_frame(); self.add(f[0],f[5])
        self.at("the stress signal")
        self.play(FadeIn(f[6][0]),Indicate(f[0],color=PURPLE),run_time=.5)
        self.at("helps hold the choice")
        self.play(GrowArrow(f[3]),FadeIn(f[1]),FadeIn(f[6][1]),run_time=.6)
        self.at("can also influence")
        self.play(GrowArrow(f[4]),FadeIn(f[2]),FadeIn(f[6][2]),run_time=.7)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        card=RoundedRectangle(width=11.8,height=6.1,corner_radius=.25,color=GREY,fill_color=GREY,fill_opacity=.06)
        title=label("Mouse reports",0,2.05,TEXT,52)
        link=label("show a link",0,.6,GREEN,52)
        rules=VGroup(label("Not the full rules",0,-.9,TEXT,46),
                     label("for building the map",0,-1.95,TEXT,46))
        # Context and the central claim are visible from the opening frame.
        self.add(card,title,link)
        self.at("These are mouse reports")
        self.play(Circumscribe(title,color=GREY),run_time=.5)
        self.at("They show a link")
        self.play(Indicate(link,color=GREEN),run_time=.5)
        self.at("not the full rules")
        self.play(FadeIn(rules[0]),run_time=.35)
        self.at("for building the map")
        self.play(FadeIn(rules[1]),run_time=.35)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        f=fork_frame(); self.add(f)
        self.at("The choice and the address")
        self.play(Indicate(f[1][0],color=GREEN),run_time=.6)
        self.at("can share a signal")
        self.play(FadeIn(label("One signal, two jobs",-3.25,3.0,PURPLE,34)),run_time=.25)
        pulse=Dot(f[0].get_right(),radius=.12,color=PURPLE)
        self.add(pulse)
        self.play(pulse.animate.move_to([-1.7,0,0]),run_time=.4)
        p2=pulse.copy(); self.add(p2)
        self.play(pulse.animate.move_to(f[1][0].get_left()),p2.animate.move_to(f[2][0].get_left()),run_time=.7)
        self.remove(pulse,p2)
        self.at("Choosing a receptor")
        self.play(Indicate(f[0],color=PURPLE),run_time=.5)
        self.at("helps set where")
        self.play(Indicate(f[2][0],color=TEXT),run_time=.7)
        self.finish()


class S23End(EndCard):
    LINE = "The choice and the address can share a signal"
