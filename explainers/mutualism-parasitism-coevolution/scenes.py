"""Coevolution Changes Both Partners — Biochemistrypedia.

COLOR MAP (preserved from the original film)
  GREEN  = algae / prey; shown or supported
  ORANGE = rotifers / predator
  YELLOW = measured change, selection and highlighted outcomes
  BLUE   = clonal diversity; flower / host population
  TEAL   = experimental evidence; moth / partner population
  RED    = limits, costs and missing evidence
  GREY   = axes, vessels, structure and de-emphasized elements
Curves are qualitative schematics, never measured data.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PERIOD = 30.0
PEAK0 = 10.0
TMAX = 90.0


class Plot:
    """Axis frame mapping day t (0..90) to screen x; value to screen y."""

    def __init__(self, x0, x1, yc, amp):
        self.x0, self.x1, self.yc, self.amp = x0, x1, yc, amp
        self.y_ax = yc - amp - 0.3

    def X(self, t):
        return self.x0 + (self.x1 - self.x0) * t / TMAX

    def val(self, t, lag=0.0):
        return np.cos(2 * np.pi * (t - PEAK0 - lag) / PERIOD)

    def P(self, t, lag=0.0):
        return np.array([self.X(t), self.yc + self.amp * self.val(t, lag), 0])

    def curve(self, lag, color, t0=0.0, t1=TMAX):
        return ParametricFunction(lambda t: self.P(t, lag), t_range=[t0, max(t1, t0 + 0.05), 0.5],
                                  color=color, stroke_width=5)

    def axis(self, ticks=(0, 30, 60, 90), size=22):
        line = Line([self.x0, self.y_ax, 0], [self.x1, self.y_ax, 0], color=GREY, stroke_width=3)
        g = VGroup(line)
        for t in ticks:
            g.add(Line([self.X(t), self.y_ax, 0], [self.X(t), self.y_ax - 0.12, 0], color=GREY, stroke_width=3))
            g.add(M(str(t), size, GREY).move_to([self.X(t), self.y_ax - 0.42, 0]))
        g.add(T("days", size, GREY).next_to(line, RIGHT, buff=0.12))
        return g

    def bracket(self, ta, tb, y, color=YELLOW):
        a, b = [self.X(ta), y, 0], [self.X(tb), y, 0]
        return VGroup(Line(a, b, color=color, stroke_width=4),
                      Line([a[0], y - 0.12, 0], [a[0], y + 0.12, 0], color=color, stroke_width=4),
                      Line([b[0], y - 0.12, 0], [b[0], y + 0.12, 0], color=color, stroke_width=4))

    def dot(self, t, lag, color, r=0.1):
        return Dot(self.P(t, lag), radius=r, color=color)


def tag(text="in this sketch: relative units"):
    return T(text, 22, GREY).move_to([6.2 - 0, 3.3, 0], aligned_edge=RIGHT)


def legend(x=-6.2, y=3.3, horizontal=False):
    a = VGroup(Dot(radius=0.1, color=GREEN), T("algae (prey)", 24, GREEN)).arrange(RIGHT, buff=0.15)
    b = VGroup(Dot(radius=0.1, color=ORANGE), T("rotifers (predator)", 24, ORANGE)).arrange(RIGHT, buff=0.15)
    if horizontal:
        g = VGroup(a, b).arrange(RIGHT, buff=0.7)
        return g.move_to([x, y, 0], aligned_edge=LEFT)
    g = VGroup(a, b).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    return g.move_to([x, y, 0], aligned_edge=UL).shift(DOWN * 0.3)


def glyph(kind, color=GREEN, r=0.14):
    if kind == "c":
        return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    if kind == "s":
        return Square(side_length=r * 1.8, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    return Triangle(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8).scale(r * 1.3)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)



def base_plot_group(plot, lag):
    return plot.axis(), plot.curve(0.0, GREEN), plot.curve(lag, ORANGE)


def label(text, x, y, color=TEXT, size=28):
    return T(text, size, color).move_to([x, y, 0])


def reciprocal():
    a = chip("flower population", BLUE, 26).move_to([-3.8, 0, 0])
    b = chip("moth population", TEAL, 26).move_to([3.8, 0, 0])
    up = arrow([-2.1, 0.65, 0], [2.1, 0.65, 0], YELLOW)
    dn = arrow([2.1, -0.65, 0], [-2.1, -0.65, 0], YELLOW)
    return VGroup(a, b, VGroup(up, label("selection", 0, 1.12, YELLOW, 24)),
                  VGroup(dn, label("evolutionary response", 0, -1.15, YELLOW, 24)))


def flower(depth=1.0):
    # A schematic cup: depth is the trait, not a molecular structure.
    cup = VMobject(color=BLUE, stroke_width=6).set_points_as_corners(
        [[-0.7, 0.65, 0], [-0.3, -depth, 0], [0.3, -depth, 0], [0.7, 0.65, 0]])
    stem = Line([0, -depth, 0], [0, -1.7, 0], color=BLUE, stroke_width=5)
    return VGroup(cup, stem)


def moth(length=1.0):
    wings = VGroup(*[Ellipse(width=0.7, height=1.0, color=TEAL, fill_opacity=0.2)
                      .rotate(a).move_to([x, 0.4, 0]) for a, x in [(-0.5, -0.4), (0.5, 0.4)]])
    body = Ellipse(width=0.22, height=0.8, color=TEAL, fill_opacity=0.8)
    tongue = Line([0, -0.4, 0], [0, -0.4-length, 0], color=TEAL, stroke_width=5)
    return VGroup(wings, body, tongue)


def balance(name, sign, x, y, color=YELLOW):
    axis = Line([x-1.1, y, 0], [x+1.1, y, 0], color=GREY, stroke_width=3)
    zero = Line([x, y-0.12, 0], [x, y+0.12, 0], color=GREY)
    pos = x + (0.75 if sign == "+" else -0.75)
    marker = Dot([pos, y, 0], radius=0.14, color=color)
    return VGroup(label(name, x, y+0.55, TEXT, 24), axis, zero, marker,
                  label("−", x-1.35, y, RED, 24), label("+", x+1.35, y, YELLOW, 24))


def qual_axes(x0, x1, y0, y1, bottom="generations", side="relative trait"):
    return VGroup(Line([x0,y0,0], [x1,y0,0], color=GREY),
                  Line([x0,y0,0], [x0,y1,0], color=GREY),
                  label(bottom, (x0+x1)/2, y0-0.45, GREY, 22),
                  label(side, (x0+x1)/2, y1+0.35, GREY, 22))


def line_curve(points, color):
    return VMobject(color=color, stroke_width=5).set_points_as_corners([[x,y,0] for x,y in points])


class S00Title(TitleCard):
    LESSON = "Mutualism, parasitism and coevolution"
    TITLE = "Coevolution Changes Both Partners"

    def construct(self):
        title = label(self.TITLE, 0, 2.5, TEXT, 43)
        diagram = reciprocal()
        self.play(FadeIn(title), FadeIn(diagram[:2]), run_time=0.6)
        self.play(Create(diagram[2]), run_time=0.5)
        self.play(Create(diagram[3]), run_time=0.5)
        self.finish()


class S01Reciprocal(SpokenScene):
    def construct(self):
        diagram = reciprocal()
        title = label("Reciprocal evolutionary change", 0, 2.9, TEXT, 36)
        self.add(diagram)
        self.at("Coevolution means")
        self.play(FadeIn(title), run_time=0.6)
        self.at("One species evolves")
        self.play(diagram[0].animate.set_fill(BLUE, opacity=0.4), run_time=0.7)
        self.at("That change alters selection")
        self.play(Indicate(diagram[2], scale_factor=1.05), run_time=0.7)
        self.at("which evolves in response")
        self.play(diagram[1].animate.set_fill(TEAL, opacity=0.4), Indicate(diagram[3]), run_time=0.7)
        self.at("Why does this matter")
        self.play(FadeOut(diagram), FadeOut(title), run_time=0.5)
        f, m = flower().move_to([-3.4, 0, 0]), moth().move_to([3.4, 0, 0])
        names = VGroup(label("flower depth", -3.4, 2.3, BLUE), label("moth tongue", 3.4, 2.3, TEAL))
        self.at("A flower and a moth")
        self.play(FadeIn(f), FadeIn(m), FadeIn(names), run_time=0.6)
        q = label("Matching traits: ?", 0, -2.7, RED, 32)
        self.at("A good fit alone")
        self.play(FadeIn(q), run_time=0.6)
        self.at("We need evidence")
        self.play(FadeOut(q), Transform(f, flower(1.5).move_to([-3.4,0,0])), run_time=0.4)
        a = VGroup(arrow([-1.9,0.4,0], [1.9,0.4,0], YELLOW),
                   label("across generations",0,1.1,YELLOW,24))
        self.play(Create(a), run_time=0.3)
        self.play(Transform(m,moth(1.5).move_to([3.4,0,0])), run_time=0.4)
        b = VGroup(arrow([1.9,-0.7,0],[-1.9,-0.7,0],YELLOW),
                   label("across generations",0,-1.3,YELLOW,24))
        self.play(Create(b), run_time=0.3)
        self.at("That is how we distinguish")
        self.play(FadeIn(label("Evidence: reciprocal evolutionary change",0,-2.9,TEAL,30)), run_time=0.7)
        self.finish()


class S02Outcomes(SpokenScene):
    def construct(self):
        head = label("Net fitness outcomes",0,3.1,TEXT,34)
        definition = label("fitness = survival and reproduction",0,2.2,GREY,26)
        self.at("First measure")
        self.play(FadeIn(head),run_time=0.5)
        self.at("Fitness means")
        self.play(FadeIn(definition),run_time=0.5)
        mutual = VGroup(label("Mutualism (+,+)",-3.3,1.1,YELLOW,30),
                        balance("partner A","+",-4.5,-0.3), balance("partner B","+",-1.5,-0.3))
        parasite = VGroup(label("Parasitism (+,−)",3.3,1.1,YELLOW,30),
                          balance("parasite","+",1.6,-0.3),balance("host","−",4.7,-0.3,RED))
        self.at("In mutualism")
        self.play(FadeIn(mutual),run_time=0.6)
        self.at("In parasitism")
        self.play(FadeIn(parasite),run_time=0.6)
        self.at("These are net outcomes")
        self.play(Indicate(head),run_time=0.5)
        self.at("A root fungus")
        self.play(FadeOut(mutual),FadeOut(parasite),FadeOut(definition),run_time=0.4)
        plant = chip("plant roots",BLUE,28).move_to([-3.7,1.0,0])
        fungus = chip("root fungus",TEAL,28).move_to([3.7,1.0,0])
        carbon=VGroup(arrow([-2,1.4,0],[2,1.4,0],GREY),label("carbon",0,1.9,GREY,24))
        nutrients=VGroup(arrow([2,0.5,0],[-2,0.5,0],GREY),label("soil nutrients",0,0,GREY,24))
        self.play(FadeIn(plant),FadeIn(fungus),run_time=0.4)
        self.at("takes carbon")
        self.play(Create(carbon),run_time=0.5)
        self.at("and supplies nutrients")
        self.play(Create(nutrients),run_time=0.5)
        soil=chip("poor soil",GREY,26).move_to([0,-2.7,0])
        pb=balance("plant: net benefit","+",-3.7,-1.65)
        fb=balance("fungus: carbon gain","+",3.7,-1.65)
        self.at("It can help")
        self.play(FadeIn(soil),FadeIn(pb),FadeIn(fb),run_time=0.6)
        self.at("and cost it")
        self.play(Transform(soil,chip("rich soil",GREY,26).move_to(soil)),
                  Transform(pb,balance("plant: net cost","−",-3.7,-1.65,RED)),run_time=0.8)
        self.at("The outcome depends")
        self.play(FadeIn(label("Soil example: plant-side outcome",0,-3.4,GREY,24)),run_time=0.5)
        self.finish()


class S03Sanctions(SpokenScene):
    def construct(self):
        heading=label("How mutualisms persist",0,3.0,TEXT,36)
        choice=chip("partner choice",TEAL,28).move_to([-3,1.5,0])
        sanction=chip("host sanctions",TEAL,28).move_to([3,1.5,0])
        self.at("How can mutualisms persist")
        self.play(FadeIn(heading),run_time=0.5)
        self.at("Partner choice")
        self.play(FadeIn(choice),run_time=0.5)
        self.at("and host sanctions")
        self.play(FadeIn(sanction),run_time=0.5)
        service=chip("service stops",GREY,28).move_to([-2.6,-0.7,0])
        fitness=chip("partner fitness falls",RED,28).move_to([2.6,-0.7,0])
        self.at("Sanctions reduce")
        self.play(FadeIn(service),GrowArrow(arrow([-0.8,-0.7,0],[0.6,-0.7,0],TEAL)),FadeIn(fitness),run_time=0.7)
        self.at("Rhizobia supply nitrogen")
        self.play(*[FadeOut(o) for o in list(self.mobjects)],run_time=0.4)
        plant=chip("legume",BLUE,28).move_to([-3.8,0.5,0])
        bacteria=chip("rhizobia",TEAL,28).move_to([3.8,0.5,0])
        n=VGroup(arrow([2,1,0],[-2,1,0],TEAL),label("nitrogen",0,1.5,TEAL,26))
        c=VGroup(arrow([-2,0,0],[2,0,0],GREY),label("carbon",0,-0.5,GREY,26))
        self.play(FadeIn(plant),FadeIn(bacteria),Create(n),run_time=0.6)
        self.at("in exchange for carbon")
        self.play(Create(c),run_time=0.5)
        self.at("In soybean")
        self.play(*[FadeOut(o) for o in list(self.mobjects)],run_time=0.4)
        head=label("Soybean nodules · same bacterial strain",0,3.0,TEXT,32)
        def nodule(x,gas):
            return VGroup(label(gas,x,2.0,GREY,26),
                Ellipse(width=2.0,height=1.4,color=GREY,fill_opacity=0.08).move_to([x,0.7,0]),
                VGroup(*[glyph("c",TEAL,0.16).move_to([x+dx,0.7,0]) for dx in [-0.5,0,0.5]]),
                label("rhizobia",x,-0.25,TEAL,24))
        left,right=nodule(-3.4,"air"),nodule(3.4,"air")
        nl=VGroup(arrow([-3.4,1.4,0],[-3.4,1.8,0],TEAL),label("nitrogen service",-3.4,-1.0,TEAL,24))
        nr=nl.copy().shift(RIGHT*6.8)
        self.play(FadeIn(head),FadeIn(left),FadeIn(right),FadeIn(nl),FadeIn(nr),run_time=0.6)
        self.at("but blocked nitrogen fixation")
        self.play(Transform(right[0],label("argon replaces nitrogen",3.4,2.0,YELLOW,24)),
                  FadeOut(nr),run_time=0.7)
        stopped=label("nitrogen service blocked",3.4,-1.0,RED,24)
        self.play(FadeIn(stopped),run_time=0.4)
        self.at("The bacteria reproduced less")
        result=VGroup(label("reproduction",-3.4,-2.0,TEAL,26),label("less reproduction",3.4,-2.0,RED,26))
        self.play(FadeIn(result),right[2].animate.scale(0.65),run_time=0.7)
        self.at("Changing the service")
        self.play(FadeIn(label("Soybean host sanction",0,-3.1,TEAL,32)),run_time=0.6)
        self.finish()


class S04Dynamics(SpokenScene):
    def construct(self):
        head=label("Two forms of reciprocal change",0,3.25,TEXT,34)
        self.at("For hosts and parasites")
        self.play(FadeIn(head),run_time=0.5)
        la=qual_axes(-5.8,-0.9,-1.7,1.5)
        ra=qual_axes(0.9,5.8,-1.7,1.5,side="host-type frequency")
        lh=label("Arms race",-3.35,2.5,YELLOW,30)
        rh=label("Fluctuating selection",3.35,2.5,YELLOW,30)
        host=line_curve([(-5.8,-1.3),(-4.6,-0.7),(-3.4,0),(-2.2,0.7)],BLUE)
        par=line_curve([(-5.8,-1.6),(-4.6,-1.1),(-3.4,-0.5),(-2.2,0.3)],TEAL)
        self.at("In an arms race")
        self.play(FadeIn(la),FadeIn(lh),run_time=0.5)
        self.at("host resistance")
        self.play(Create(host),FadeIn(label("resistance",-4.7,-2.9,BLUE,24)),run_time=0.7)
        self.at("and parasite infectivity")
        self.play(Create(par),FadeIn(label("infectivity",-2,-2.9,TEAL,24)),run_time=0.7)
        self.at("Escalation can slow or stop")
        self.play(Create(line_curve([(-2.2,0.7),(-1.5,0.9),(-0.9,0.9)],BLUE)),
                  Create(line_curve([(-2.2,0.3),(-1.5,0.5),(-0.9,0.5)],TEAL)),run_time=0.8)
        self.at("In fluctuating selection")
        self.play(FadeIn(ra),FadeIn(rh),run_time=0.5)
        def frequency(phase,color):
            return ParametricFunction(lambda t: [0.9+4.9*t,-0.1+1.05*np.cos(2*np.pi*t+phase),0],
                                      t_range=[0,1,0.01],color=color,stroke_width=5)
        ca,cb=frequency(0,BLUE),frequency(np.pi,TEAL)
        self.at("common host types")
        self.play(Create(ca),Create(cb),run_time=0.8)
        notice=label("common type attacked",3.35,-2.9,RED,24)
        marker=Dot([0.9,0.95,0],color=RED,radius=0.14)
        self.play(FadeIn(notice),FadeIn(marker),run_time=0.4)
        self.at("Rare types gain")
        self.play(marker.animate.move_to([3.35,0.95,0]),
                  Transform(notice,label("rare type gains",3.35,-2.9,TEAL,24)),run_time=0.8)
        self.at("then the advantage shifts again")
        self.play(marker.animate.move_to([5.8,0.95,0]),run_time=0.8)
        self.at("The contrast is")
        self.play(FadeOut(marker),FadeIn(label("escalation  /  changing advantage",0,-3.5,YELLOW,28)),run_time=0.5)
        self.finish()


class S05Timeshift(SpokenScene):
    def construct(self):
        head=label("Time-shift assay",0,3.15,TEXT,36)
        # Rows are parasite sampling times; columns are host sampling times.
        grid=VGroup()
        for x in [-1.5,0,1.5]:
            for y in [1.2,0,-1.2]:
                grid.add(Square(side_length=1.1,color=GREY,stroke_width=2).move_to([x,y,0]))
        headers=VGroup(*[label(t,x,2.2,GREY,24) for t,x in zip(["past","present","future"],[-1.5,0,1.5])],
            *[label(t,-3,y,GREY,24) for t,y in zip(["past","present","future"],[1.2,0,-1.2])],
            label("host sample",0,2.65,BLUE,22),label("parasite sample",-4.8,0,TEAL,22))
        self.at("A time shift assay")
        self.play(FadeIn(head),Create(grid),FadeIn(headers),run_time=0.7)
        self.at("from the past")
        self.play(grid[1].animate.set_fill(YELLOW,opacity=0.4),run_time=0.3)
        self.at("present and future")
        self.play(grid[4].animate.set_fill(YELLOW,opacity=0.4),grid[7].animate.set_fill(YELLOW,opacity=0.4),run_time=0.4)
        self.at("An arms race predicts")
        self.play(FadeOut(grid),FadeOut(headers),Transform(head,label("Predictions · not measured results",0,3.15,TEXT,32)),run_time=0.5)
        la=qual_axes(-5.5,-1,-1.3,1.5,bottom="host sampling time",side="relative infection")
        ra=qual_axes(1,5.5,-1.3,1.5,bottom="host sampling time",side="relative infection")
        labs=VGroup(*[label(t,x,-1.65,GREY,22) for t,x in zip(["past","present","future"],[-5.4,-3.25,-1.1])])
        labs2=labs.copy().shift(RIGHT*6.5)
        la[2].shift(DOWN*0.65)
        ra[2].shift(DOWN*0.65)
        self.play(FadeIn(la),FadeIn(labs),FadeIn(label("Arms race",-3.25,2.35,YELLOW,28)),run_time=0.4)
        self.at("parasites infect past")
        self.play(Create(line_curve([(-5.5,1.1),(-3.25,0),(-1,-1)],TEAL)),run_time=0.8)
        self.at("Fluctuating selection predicts")
        self.play(FadeIn(ra),FadeIn(labs2),FadeIn(label("Fluctuating selection",3.25,2.35,YELLOW,28)),run_time=0.4)
        peak=line_curve([(1,-0.7),(3.25,1.1),(5.5,-0.7)],TEAL)
        dip=line_curve([(1,0.8),(3.25,-1),(5.5,0.8)],BLUE)
        self.at("a peak or dip")
        self.play(Create(peak),Create(dip),run_time=0.7)
        self.at("with no steady trend")
        self.play(FadeIn(label("contemporary peak or dip; no steady trend",0,-3.0,YELLOW,28)),run_time=0.6)
        self.finish()


class S06Proof(SpokenScene):
    def construct(self):
        head=label("Rapid evolution changes population cycles",0,3.0,TEXT,34)
        rot=VGroup(Ellipse(width=0.75,height=0.45,color=ORANGE,fill_opacity=0.7),
                   label("rotifers",0,0.7,ORANGE,26)).move_to([-4.4,0.7,0])
        undef=VGroup(glyph("c",GREEN,0.4),label("undefended",0,-0.85,GREEN,26)).move_to([0,0.7,0])
        defended=VGroup(glyph("s",GREEN,0.4),label("defended",0,-0.85,GREEN,26)).move_to([4.4,0.7,0])
        self.at("Rapid evolution")
        self.play(FadeIn(head),run_time=0.5)
        self.at("In rotifers and algae")
        self.play(FadeIn(rot),FadeIn(undef),FadeIn(defended),run_time=0.5)
        graze=arrow([-3.6,0.8,0],[-1,0.8,0],ORANGE)
        self.at("grazing favors")
        self.play(GrowArrow(graze),undef[0].animate.scale(0.6),defended[0].animate.scale(1.4),run_time=0.7)
        cost=label("defence: poorer nutrient competitiveness",0,-1.5,TEAL,28)
        self.at("but defense costs")
        self.play(FadeIn(cost),run_time=0.6)
        self.at("As rotifers decline")
        self.play(rot[0].animate.scale(0.5),FadeOut(graze),run_time=0.6)
        self.at("undefended clones regain ground")
        self.play(undef[0].animate.scale(2),defended[0].animate.scale(0.6),run_time=0.7)
        self.at("Changing algal clonal diversity")
        self.play(*[FadeOut(o) for o in list(self.mobjects)],run_time=0.4)
        one=VGroup(glyph("c"),label("one clone",0,-0.6,BLUE,28)).move_to([-3.4,2.4,0])
        many=VGroup(VGroup(glyph("c"),glyph("s"),glyph("t")).arrange(RIGHT,buff=0.2),
                    label("several clones",0,-0.6,BLUE,28)).move_to([3.4,2.4,0])
        self.play(FadeIn(one),FadeIn(many),FadeIn(label("Schematic cycles",0,3.35,GREY,22)),run_time=0.5)
        # Reuse the original cosine drawing helper, with entirely qualitative axes.
        L,R=Plot(-5.8,-1.0,0.2,0.8),Plot(1,5.8,0.2,0.8)
        axes=VGroup(qual_axes(-5.8,-1,-1.1,1.25,"time","relative abundance"),
                    qual_axes(1,5.8,-1.1,1.25,"time","relative abundance"))
        curves=VGroup(L.curve(0,GREEN),L.curve(6,ORANGE),R.curve(0,GREEN),R.curve(13,ORANGE))
        # Different schematic cycle lengths, with no numerical phase claims.
        # Trim the stretched curves to the same panel width by sampling fewer times.
        curves[2].become(R.curve(0,GREEN,t1=69).stretch(90/69,0,about_point=[1,0,0]))
        curves[3].become(R.curve(13,ORANGE,t1=69).stretch(90/69,0,about_point=[1,0,0]))
        self.at("changed the cycles")
        self.play(FadeIn(axes),Create(curves),FadeIn(legend(-4.5,-2.2,True)),run_time=0.8)
        self.at("The manipulation and measured")
        evidence=label("Manipulation + measured trade-off",0,-3.0,TEAL,30)
        self.play(FadeIn(evidence),run_time=0.5)
        self.at("supported prey evolution")
        self.play(Transform(evidence,label("Prey evolution drives population dynamics",0,-3.0,GREEN,30)),run_time=0.6)
        self.at("Cycle timing alone")
        self.play(*[FadeOut(o) for o in list(self.mobjects)],run_time=0.5)
        timing=chip("cycle timing alone: not proof",RED,28).move_to([0,2.5,0])
        shown=chip("prey evolution shown",GREEN,30).move_to([-3.4,0.9,0])
        self.play(FadeIn(timing),FadeIn(shown),run_time=0.5)
        self.at("Predator evolution was not investigated")
        missing=chip("predator evolution\nnot investigated",GREY,26).move_to([3.4,0.9,0])
        self.play(FadeIn(missing),run_time=0.6)
        req=label("Coevolution needs evidence of change in both",0,-2.4,YELLOW,30)
        arrows=VGroup(arrow([-2,-0.4,0],[2,-0.4,0],YELLOW),
                      DashedLine([2,-1.1,0],[-2,-1.1,0],color=GREY),label("?",0,-1.55,RED,28))
        self.at("so this was not demonstrated coevolution")
        self.play(Create(arrows),FadeIn(req),run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Coevolution requires reciprocal evolutionary change."

    def construct(self):
        title=label(self.LINE,0,2.6,TEXT,36)
        diagram=reciprocal()
        sub=label("biochemistrypedia.com",0,-3,TEAL,22)
        self.play(FadeIn(title),FadeIn(diagram[:2]),run_time=0.6)
        self.play(Create(diagram[2:]),FadeIn(sub),run_time=0.7)
        self.finish()
