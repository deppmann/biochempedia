"""Global change: species on the move  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  RED    = the isotherm and warming (the moving warm line)
  GREEN  = the species (dots on the slope)
  YELLOW = the lag, the gap between line and species
  TEAL   = measurements, evidence and arithmetic
  BLUE   = seawater
  ORANGE also represents land use, transport and nitrogen deposition
  ORANGE = other possible drivers (barrier, forest loss, alternatives)
  GREY   = the mountain, the start level, labels
Scale on the mountain: 1 unit of height = 50 m, so 11 m = 0.22 units, 150 m = 3 units.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

PEAK = np.array([-3.4, 3.0, 0])
LFOOT = np.array([-6.2, -3.3, 0])
RFOOT = np.array([-0.6, -3.3, 0])
Y0 = -1.6           # start level of the isotherm and the species
U = 0.02            # height units per metre


def sl(y):
    return LFOOT[0] + (y - LFOOT[1]) * (PEAK[0] - LFOOT[0]) / (PEAK[1] - LFOOT[1])


def sr(y):
    return PEAK[0] + (PEAK[1] - y) * (RFOOT[0] - PEAK[0]) / (PEAK[1] - RFOOT[1])


def mountain():
    m = Polygon(LFOOT, PEAK, RFOOT, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12)
    return m


def iso(y, color=RED, dashed=True, w=5):
    a, b = np.array([sl(y) - 0.45, y, 0]), np.array([sr(y) + 0.3, y, 0])
    return DashedLine(a, b, color=color, stroke_width=w, dash_length=0.18) if dashed else Line(a, b, color=color, stroke_width=w)


def lbl_on(text, y, color, size=24):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.16, height=t.height + 0.1, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(back, t.move_to(back))
    g.move_to([sr(y) + 0.35 + g.width / 2, y, 0])
    return g


def dots(y, n=3, color=GREEN):
    xs = [sl(y) + 0.35, sl(y) + 0.65, sl(y) + 0.95]
    return VGroup(*[Dot([x, y + (0.08 if i == 1 else -0.06), 0], radius=0.12, color=color) for i, x in enumerate(xs[:n])])


def splabel(y, size=24):
    t = T("species", size, GREEN)
    back = Rectangle(width=t.width + 0.12, height=t.height + 0.08, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(back, t.move_to(back))
    return g.move_to([sl(y - 0.5) + 1.1, y - 0.5, 0])


def bracket(x, y0, y1, color):
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=4),
                  Line([x - 0.1, y0, 0], [x + 0.1, y0, 0], color=color, stroke_width=4),
                  Line([x - 0.1, y1, 0], [x + 0.1, y1, 0], color=color, stroke_width=4))


def panel_chip(text, color, size=24, w=None):
    c = chip(text, color, size=size)
    return c


def heading(text):
    return T(text, 34, font=TITLE_FONT).move_to([0, 3.15, 0])


def arrow(a, b, color=GREEN):
    return Arrow(a, b, color=color, buff=0, stroke_width=5)


def tree(x, y, scale=1):
    return VGroup(Line([x, y, 0], [x, y+0.8*scale, 0], color=GREY, stroke_width=4),
                  Polygon([x-0.4*scale,y+0.35*scale,0], [x,y+1.3*scale,0],
                          [x+0.4*scale,y+0.35*scale,0], color=GREEN, fill_opacity=0.3))


def backed_chip(text, color=GREEN, size=24):
    c = chip(text, color, size)
    back = Rectangle(width=c.width, height=c.height, stroke_width=0,
                     fill_color=BG, fill_opacity=1).move_to(c)
    return VGroup(back, c)


def prairie_plant(x, height):
    y = -1.8
    stalk = Line([x,y,0], [x,y+height,0], color=GREEN, stroke_width=4)
    leaves = VGroup(*[Ellipse(width=.55, height=.18, color=GREEN, fill_opacity=.4)
                       .rotate(angle).move_to([x+dx,y+height*f,0])
                       for dx,f,angle in [(-.2,.4,-.5),(.2,.65,.5)]])
    return VGroup(stalk, leaves)


def bar(width, x, y, color=GREEN):
    return Rectangle(width=width, height=0.5, stroke_width=0, fill_color=color,
                     fill_opacity=0.8).move_to([x+width/2,y,0])


class S00Title(TitleCard):
    LESSON = "Global change across scales"
    TITLE = "Species on the Move"


class S01Moving(SpokenScene):
    def construct(self):
        globe = VGroup(Circle(radius=2.35, color=GREY),
                       Ellipse(width=2.5,height=4.7,color=GREY),
                       Ellipse(width=4.7,height=1.1,color=GREY)).shift(LEFT*2.8)
        sp = VGroup(*[Dot([x,y,0], radius=.13,color=GREEN) for x,y in [(-4,0),(-2.8,.4),(-1.8,-.4)]])
        title = heading("Ranges are moving")
        self.at("As the climate warms")
        self.play(FadeIn(title),Create(globe),FadeIn(sp),run_time=.8)
        self.at("toward the poles")
        ars=VGroup(*[arrow(d.get_center(),d.get_center()+UP*h) for d,h in zip(sp,[.5,1.3,-1.1])])
        self.play(*[d.animate.shift(UP*h) for d,h in zip(sp,[.5,1.3,-1.1])],Create(ars),run_time=1)
        self.at("and up mountains")
        mt=mountain(); ds=dots(Y0)
        self.play(FadeOut(VGroup(globe,sp,ars)),Create(mt),FadeIn(ds),run_time=.7)
        self.play(Transform(ds,dots(Y0+1.2)),run_time=.8)
        self.at("by a median")
        nums=VGroup(T("Land medians / decade",26,GREY),M("~17 km poleward",30,GREEN),
                    M("11 m uphill",30,GREEN)).arrange(DOWN,buff=.35).move_to([3,1,0])
        self.play(FadeIn(nums),run_time=.6)
        self.at("Species vary a lot")
        varied=VGroup(*[Dot([sl(y)+.6,y,0],radius=.14,color=GREEN) for y in [-1.3,-.1,1.5]])
        self.play(Transform(ds,varied),FadeIn(T("Wide variation",26,YELLOW).move_to([3,-1,0])),run_time=.7)
        self.at("In the sea")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.4)
        sea=RoundedRectangle(width=11,height=3.5,color=BLUE,fill_opacity=.1).move_to([0,.3,0])
        sd=VGroup(*[Dot([-4,y,0],radius=.15,color=GREEN) for y in [-.6,.3,1.2]])
        self.play(FadeIn(heading("At sea: ~6× faster poleward")),Create(sea),FadeIn(sd),run_time=.6)
        self.play(sd.animate.shift(RIGHT*6),run_time=1.5)
        self.at("That reshuffling")
        together=T("New combinations of species",30,GREEN).move_to([0,-2.4,0])
        self.play(FadeIn(together),sd[0].animate.shift(UP*.5+LEFT),sd[2].animate.shift(DOWN*.4+RIGHT),run_time=.8)
        self.finish()


class S02Evidence(SpokenScene):
    def construct(self):
        cards=VGroup(*[chip("study",TEAL,24).move_to([x,y,0]) for x,y in [(-4,1.3),(-1.3,1.6),(1.4,1.1),(4,1.6)]])
        self.at("How do we know")
        self.play(FadeIn(heading("Many studies, one synthesis")),FadeIn(cards),run_time=.7)
        self.at("pooled published range shifts")
        axes=VGroup(arrow([-3,-1.6,0],[3.8,-1.6,0],GREY),arrow([-3,-1.6,0],[-3,2,0],GREY))
        labs=VGroup(T("warming →",24,RED).move_to([.4,-2.2,0]),T("range shift",24,GREEN).move_to([-4.5,1.8,0]))
        pts=VGroup(*[Dot([x,y,0],radius=.13,color=TEAL) for x,y in [(-2.2,-1),(-.8,-.5),(.5,.4),(2,.7),(3,1.4)]])
        self.play(ReplacementTransform(cards,pts),Create(axes),FadeIn(labs),run_time=.9)
        self.at("Shifts were biggest")
        self.play(Indicate(pts[-1],color=YELLOW,scale_factor=1.6),run_time=.8)
        self.at("roughly kept pace")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.3)
        mt=mountain(); ds=dots(Y0); line=iso(Y0)
        self.play(Create(mt),FadeIn(ds),Create(line),run_time=.6)
        note=T("Poleward: roughly kept pace",28,GREEN).move_to([3.1,2.6,0])
        self.play(FadeIn(note),run_time=.5)
        self.at("Uphill shifts mostly fell short")
        self.play(Transform(line,iso(Y0+2.4)),Transform(ds,dots(Y0+.8)),run_time=1)
        keys=VGroup(chip("isotherm",RED,24),chip("species",GREEN,24)).arrange(DOWN,buff=.3).move_to([3.1,.8,0])
        self.play(FadeIn(keys),Create(bracket(-2.9,Y0+.8,Y0+2.4,YELLOW)),run_time=.6)
        self.at("measure that shortfall")
        self.play(FadeIn(T("Measure the uphill shortfall",26,YELLOW).move_to([3.1,-1.5,0])),run_time=.6)
        self.finish()


class S03Consequences(SpokenScene):
    def construct(self):
        community=VGroup(Circle(radius=1.7,color=GREY).move_to([-2.5,.3,0]),Circle(radius=1.7,color=GREY).move_to([2.5,.3,0]))
        icons=VGroup(Dot([-3,.5,0],radius=.22,color=GREEN),Triangle(color=GREEN,fill_opacity=.5).scale(.25).move_to([-2,-.3,0]),
                     Square(side_length=.4,color=GREEN,fill_opacity=.5).move_to([2,.4,0]),Dot([3,-.3,0],radius=.22,color=GREEN))
        self.at("Why does it matter")
        self.play(FadeIn(heading("Communities reassemble")),Create(community),FadeIn(icons),run_time=.7)
        self.at("Species do not move together")
        self.play(icons[0].animate.shift(RIGHT*4.8),icons[2].animate.shift(LEFT*4.5),icons[1].animate.shift(UP*.8),run_time=1.3)
        self.at("Hosts and pathogens")
        host=chip("host",GREEN,26).move_to([-2,.3,0]); pathogen=chip("pathogen",ORANGE,26).move_to([2,.3,0])
        self.play(FadeOut(community),FadeOut(icons),FadeIn(host),FadeIn(pathogen),run_time=.6)
        self.at("can meet in new places")
        self.play(host.animate.shift(RIGHT*.6),pathogen.animate.shift(LEFT*.6),run_time=.8)
        self.at("food production")
        food=chip("food",ORANGE,28).move_to([-4,-2,0])
        self.play(FadeIn(food),run_time=.5)
        self.at("spread of disease")
        self.play(FadeIn(chip("disease",ORANGE,28).move_to([0,-2,0])),run_time=.5)
        self.at("how much carbon")
        self.play(FadeIn(chip("carbon",ORANGE,28).move_to([4,-2,0])),run_time=.5)
        self.finish()


class S04LandUse(SpokenScene):
    def construct(self):
        trees=VGroup(*[tree(x,-1.3) for x in [-4.7,-3.4,-2.1,-.8]])
        self.at("Climate is not acting alone")
        self.play(FadeIn(heading("Other drivers act alongside warming")),FadeIn(trees),run_time=.7)
        self.at("Clearing land for farms and towns")
        fields=VGroup(*[Rectangle(width=1.1,height=1,color=ORANGE,fill_opacity=.2).move_to([x,-.7,0]) for x in [-2.1,-.8]])
        self.play(ReplacementTransform(VGroup(trees[2],trees[3]),fields),run_time=1)
        self.at("One model estimate")
        b=bar(4,1,-.5); label=VGroup(T("Local species richness",26,GREEN),T("model estimate",22,GREY)).arrange(DOWN,buff=.15).move_to([3,1,0])
        self.play(FadeIn(label),GrowFromEdge(b,LEFT),run_time=.6)
        self.at("average loss")
        self.play(Transform(b,bar(4*.864,1,-.5)),FadeIn(M("−13.6%",34,YELLOW).move_to([3,-1.5,0])),run_time=.8)
        self.at("In warmer regions")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.3)
        mt=mountain(); ds=dots(Y0)
        cleared=Polygon(LFOOT,[-4,-.4,0],[-1.8,-.4,0],RFOOT,color=ORANGE,fill_opacity=.18)
        self.play(Create(mt),FadeIn(ds),FadeIn(cleared),FadeIn(T("Forest loss + warming",30,ORANGE).move_to([3,2,0])),run_time=.6)
        self.at("speed up uphill shifts")
        self.play(Transform(ds,dots(Y0+2)),run_time=.9)
        self.at("And species carried by people")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.3)
        lands=VGroup(Ellipse(width=2,height=3,color=GREY,fill_opacity=.12).move_to([-4.8,0,0]),Ellipse(width=2,height=3,color=GREY,fill_opacity=.12).move_to([4.8,0,0]))
        ship=VGroup(Polygon([-1,-.25,0],[1,-.25,0],[.6,-.65,0],[-.7,-.65,0],color=ORANGE,fill_opacity=.3),Rectangle(width=.8,height=.4,color=ORANGE).move_to([0,-.05,0])).shift(LEFT*2+DOWN*.4)
        plane=VGroup(Line(LEFT*.7,RIGHT*.7,color=ORANGE,stroke_width=5),Line([-.2,-.4,0],[.2,.4,0],color=ORANGE,stroke_width=5)).move_to([-2,1.4,0])
        cargo=VGroup(Dot(ship.get_center(),color=GREEN,radius=.12),Dot(plane.get_center(),color=GREEN,radius=.12))
        self.play(Create(lands),FadeIn(ship),FadeIn(plane),FadeIn(cargo),run_time=.6)
        self.play(ship.animate.shift(RIGHT*4),plane.animate.shift(RIGHT*4),cargo.animate.shift(RIGHT*4),run_time=1.3)
        self.at("threats linked to extinctions")
        self.play(FadeIn(T("Introduced species: extinction threats",28,ORANGE).move_to([0,-2.5,0])),run_time=.5)
        self.finish()


class S05Timing(SpokenScene):
    def construct(self):
        lines=VGroup(Line([-3.2,1,0],[5.2,1,0],color=GREY),Line([-3.2,-.6,0],[5.2,-.6,0],color=GREY))
        labs=VGroup(T("Bird laying",25,GREEN).move_to([-4.8,1,0]),T("Caterpillar peak",24,GREEN).move_to([-4.8,-.6,0]),T("earlier ← spring → later",24,GREY).move_to([.8,2.1,0]))
        bird=backed_chip("laying",GREEN,24).move_to([2,1,0]); food=backed_chip("food",GREEN,24).move_to([2,-.6,0])
        self.at("Warming also shifts timing")
        self.play(FadeIn(heading("Spring events shift unevenly")),Create(lines),FadeIn(labs),FadeIn(bird),FadeIn(food),run_time=.8)
        self.at("Many spring events now come earlier")
        self.play(bird.animate.shift(LEFT*.7),food.animate.shift(LEFT*.7),run_time=.8)
        self.at("not by the same amount")
        self.play(food.animate.shift(LEFT*2.5),run_time=.8)
        self.at("chicks can miss the peak")
        gap=VGroup(DashedLine([1.3,.65,0],[1.3,-1.4,0],color=YELLOW),
                   DashedLine([-1.2,-.95,0],[-1.2,-1.4,0],color=YELLOW),
                   DoubleArrow([-1.2,-1.4,0],[1.3,-1.4,0],buff=0,color=YELLOW))
        self.play(Create(gap),FadeIn(T("Food peaks before chicks need it",28,YELLOW).move_to([0,-2.1,0])),run_time=.7)
        self.at("In Dutch pied flycatchers")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.3)
        title=heading("Pied flycatcher populations")
        labels=VGroup(T("Early food peak",26,GREY).move_to([-3,1.8,0]),T("Late food peak",26,GREY).move_to([3,1.8,0]))
        a=bar(4,-5,0); b=bar(4,1,0)
        self.play(FadeIn(title),FadeIn(labels),FadeIn(a),FadeIn(b),run_time=.6)
        self.at("populations fell by about")
        self.play(Transform(a,bar(.4,-5,0)),FadeIn(M("~90% decline",30,YELLOW).move_to([-3,-1,0])),run_time=1)
        self.play(FadeIn(T("Weak decline at most",24,GREY).move_to([3,-1,0])),run_time=.4)
        self.at("Fewer chicks do not always")
        self.play(FadeIn(T("Fewer chicks ≠ always fewer birds",28,YELLOW).move_to([0,-2.5,0])),run_time=.6)
        self.finish()


class S06SeaAndNitrogen(SpokenScene):
    def construct(self):
        sea=Rectangle(width=11,height=3.5,color=BLUE,fill_opacity=.12).move_to([0,-.8,0])
        bubbles=VGroup(*[Circle(radius=.17,color=GREY).move_to([x,1.7,0]) for x in [-3,-1,1]])
        gas=chip("CO₂",GREY,28).move_to([-4.8,2.3,0])
        self.at("In the sea")
        self.play(Create(sea),FadeIn(bubbles),FadeIn(gas),run_time=.7)
        self.at("dissolved carbon dioxide")
        self.play(bubbles.animate.shift(DOWN*2.2),run_time=.8)
        self.at("lowers pH")
        ph=chip("pH ↓",YELLOW,28).move_to([-3,-1,0])
        self.play(FadeIn(ph),FadeOut(bubbles),run_time=.5)
        self.at("and the carbonate")
        carb=chip("carbonate ↓",YELLOW,28).move_to([.1,-1,0])
        # A shell silhouette, with no molecular geometry.
        shell=VGroup(Arc(radius=.9,start_angle=0,angle=PI,color=GREY),Line([-.9,0,0],[.9,0,0],color=GREY)).move_to([3.5,-1,0])
        self.play(FadeIn(carb),Create(shell),run_time=.6)
        self.at("On average")
        self.play(FadeIn(T("Calcification, growth, survival ↓ on average",26,GREY).move_to([0,2.9,0])),run_time=.5)
        self.at("but groups differ widely")
        self.play(FadeIn(T("Responses differ among groups",26,YELLOW).move_to([0,-3,0])),run_time=.5)
        self.at("On land")
        self.play(FadeOut(Group(*self.mobjects)),run_time=.3)
        ground=Line([-5.5,-1.8,0],[5.5,-1.8,0],color=GREY,stroke_width=4)
        plants=VGroup(*[prairie_plant(x,h) for x,h in zip([-4,-2,0,2,4],[.85,1.1,.7,1,.9])])
        nitrogen=VGroup(*[chip("N",ORANGE,22).move_to([x,1.3,0]) for x in [-3,0,3]])
        self.play(FadeIn(heading("Nitrogen deposition on prairie")),Create(ground),FadeIn(plants),run_time=.6)
        self.at("nitrogen from polluted air")
        self.play(FadeIn(nitrogen),run_time=.4)
        self.play(nitrogen.animate.shift(DOWN*1.6),run_time=.8)
        self.at("can cut plant diversity")
        self.play(FadeOut(nitrogen),plants[1].animate.stretch(2,1,about_edge=DOWN),plants[3].animate.stretch(2,1,about_edge=DOWN),plants[0].animate.set_opacity(.15),plants[4].animate.set_opacity(.15),run_time=.8)
        self.at("On Minnesota prairie")
        self.play(FadeIn(T("Minnesota prairie experiment",26,TEAL).move_to([0,2.2,0])),run_time=.5)
        self.at("species number by 17 percent")
        self.play(FadeIn(M("17% fewer species",34,YELLOW).move_to([0,-2.9,0])),run_time=.6)
        self.finish()


class S07Attribution(SpokenScene):
    def construct(self):
        mt=mountain(); sp=dots(Y0); lab=splabel(Y0)
        self.at("when a range moves uphill")
        self.play(Create(mt),FadeIn(sp),FadeIn(lab),run_time=.6)
        self.play(Transform(sp,dots(Y0+1.8)),Transform(lab,splabel(Y0+1.8)),run_time=.9)
        self.at("that shows a change happened")
        det=VGroup(chip("Detection",GREEN,30),T("A change happened",24,GREY)).arrange(DOWN,buff=.2).move_to([3.5,2.3,0])
        self.play(FadeIn(det),run_time=.6)
        self.at("It does not show the cause")
        q=T("Cause?",36,YELLOW).move_to([3.5,.7,0])
        self.play(FadeIn(q),run_time=.5)
        self.at("Attribution links the change")
        att=VGroup(chip("Attribution",YELLOW,30),T("Link a cause; test alternatives",24,GREY)).arrange(DOWN,buff=.2).move_to([3.5,.6,0])
        self.play(FadeOut(q),FadeIn(att),run_time=.6)
        w=chip("warming",RED,24).move_to([2,-1.2,0]); f=chip("forest loss",ORANGE,24).move_to([2,-2.4,0])
        aw=arrow(w.get_left(),[-2.8,.4,0],RED); af=arrow(f.get_left(),[-2.8,0,0],ORANGE)
        self.at("tests the alternatives")
        self.play(FadeIn(w),GrowArrow(aw),run_time=.5)
        self.at("such as forest loss")
        self.play(FadeIn(f),GrowArrow(af),run_time=.5)
        self.at("Test the alternatives before")
        self.play(Indicate(VGroup(w,f),color=YELLOW,scale_factor=1.08),run_time=.7)
        self.finish()


class S08End(EndCard):
    LINE = "Warming moves species poleward and uphill, reshaping communities."
