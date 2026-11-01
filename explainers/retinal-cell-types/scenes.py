"""Retinal cell types: a count depends on its method  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = ganglion cells
  RED    = displaced amacrine cells, set aside
  YELLOW = imaging / light response / functional
  TEAL   = sequencing / expression (RNA)
  ORANGE = same-cell recording
  PURPLE = electron microscopy / shape / anatomical
  GOLD   = a supported type (the answer)
  GREEN  = mosaic
  GREY   = outlines, frames, de-emphasized
  TEXT   = neutral numbers
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def gcell(color=BLUE, s=1.0):
    """simple ganglion cell: soma, dendrites up, axon to the right."""
    soma = Circle(radius=0.28, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.35)
    parts = [soma]
    for dx in (-0.35, 0.0, 0.35):
        parts.append(Line([dx * 0.4, 0.26, 0], [dx * 1.2, 0.95, 0], color=color, stroke_width=4))
        parts.append(Line([dx * 1.2, 0.95, 0], [dx * 1.2 - 0.12, 1.25, 0], color=color, stroke_width=3))
        parts.append(Line([dx * 1.2, 0.95, 0], [dx * 1.2 + 0.12, 1.25, 0], color=color, stroke_width=3))
    parts.append(Line([0.28, 0, 0], [1.4, 0, 0], color=color, stroke_width=4))
    g = VGroup(*parts)
    g.scale(s)
    return g


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def card(num, label, color, size=44):
    c = chip(num, color, size=size)
    l = T(label, 24, color)
    return VGroup(c, l).arrange(DOWN, buff=0.2)


# Additional schematic helpers use the original line-and-soma drawing style.
def heading(text, color=TEXT):
    return T(text, 34, color, font=TITLE_FONT).move_to([0, 3.15, 0])


def eye():
    return VGroup(Ellipse(width=2.4, height=1.7, color=GREY),
                  Circle(radius=0.55, color=BLUE), Dot(radius=0.22, color=BLUE)).move_to([-1.7, 0, 0])


def landscape():
    box = Rectangle(width=2.5, height=1.8, color=GREY)
    sky = Rectangle(width=2.45, height=0.85, stroke_width=0, fill_color=BLUE, fill_opacity=0.16).shift(UP*0.43)
    ground = Rectangle(width=2.45, height=0.85, stroke_width=0, fill_color=GREEN, fill_opacity=0.25).shift(DOWN*0.43)
    horizon = Line([-1.23, 0, 0], [1.23, 0, 0], color=GREY)
    return VGroup(box, sky, ground, horizon).move_to([-5, 0, 0])


def feature_icon(kind, color=YELLOW):
    if kind == 0:
        return VGroup(Rectangle(width=0.35, height=0.65, fill_color=TEXT, fill_opacity=1, stroke_width=0).shift(LEFT*0.18),
                      Rectangle(width=0.35, height=0.65, fill_color=GREY, fill_opacity=0.3, stroke_width=0).shift(RIGHT*0.18))
    if kind == 1:
        return VGroup(Dot(LEFT*0.22, radius=0.13, color=color), arr([0,-0.2,0],[0.7,-0.2,0],color,3))
    return arr([0,-0.4,0],[0,0.4,0],color,4)


def strands():
    # Three representative strands stand for the dozens of feature channels.
    group = VGroup()
    for i, y in enumerate((1.5, 0, -1.5)):
        col = (YELLOW, BLUE, PURPLE)[i]
        path = CubicBezier([-.5,0,0], [1,0,0], [1,y,0], [4.3,y,0], color=col, stroke_width=4)
        icon = feature_icon(i, col).move_to([4.8,y,0])
        group.add(VGroup(path, icon))
    return group


def spikes(x, y, active=True, width=4.2):
    base = Line([x-width/2,y,0], [x+width/2,y,0], color=BLUE, stroke_width=3)
    ticks = VGroup(*[Line([x-width/2+0.3+k*0.38,y,0], [x-width/2+0.3+k*0.38,y+0.45,0], color=BLUE, stroke_width=3)
                     for k in range(10)]) if active else VGroup()
    return VGroup(base,ticks)


def motion_panel(x, label):
    frame = RoundedRectangle(width=5.4,height=2.2,corner_radius=0.12,color=GREY).move_to([x,0.6,0])
    texture = VGroup(*[Line([x+d,-0.25,0],[x+d,1.45,0],color=GREY,stroke_opacity=0.45)
                        for d in (-2,-1,0,1,2)])
    dot = Dot([x-1,0.6,0],radius=0.16,color=YELLOW)
    lab = T(label,24).move_to([x,2.15,0])
    return VGroup(frame,texture,dot,lab)


def mosaic(center=(0,0,0), spacing=0.85, rows=3, cols=5):
    # Reused radial arbor construction: overlapping fields, distinct spaced somata.
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            p = np.array(center)+[(c-(cols-1)/2)*spacing+(r%2)*spacing/2,
                                  (r-(rows-1)/2)*spacing*np.sqrt(3)/2,0]
            arbor = VGroup()
            for angle in np.linspace(0,TAU,6,endpoint=False):
                d=np.array([np.cos(angle),np.sin(angle),0]); j=p+0.45*spacing*d
                arbor.add(Line(p,j,color=GREEN,stroke_width=2))
                for off in (-0.4,0.4):
                    tip=j+0.33*spacing*np.array([np.cos(angle+off),np.sin(angle+off),0])
                    arbor.add(Line(j,tip,color=GREEN,stroke_width=2))
            cells.add(VGroup(arbor,Dot(p,radius=0.09,color=GREEN)))
    return cells


class S00Title(TitleCard):
    LESSON = "Forty kinds of ganglion cell"
    TITLE = "What the Eye Sends the Brain"


class S01Channels(SpokenScene):
    def construct(self):
        head=heading("Parallel channels out of the eye")
        e=eye(); field=landscape(); incoming=arr(field.get_right(),e.get_left(),GREY,3)
        cell=gcell(BLUE,1.05).move_to([2,0,0])
        lab=T("ganglion cell",26,BLUE).move_to([2,-1.6,0])
        self.at("Every signal")
        self.play(FadeIn(head),FadeIn(field),FadeIn(e),GrowArrow(incoming),run_time=0.7)
        self.at("through ganglion cells")
        self.play(FadeIn(cell),FadeIn(lab),run_time=0.6)
        nerve=Line(cell[-1].get_end(),[5.8,-0.5,0],color=BLUE,stroke_width=6)
        nl=T("optic nerve",26,GREY).move_to([4.9,-1.6,0])
        self.at("form the optic nerve")
        self.play(Create(nerve),FadeIn(nl),run_time=0.6)
        self.at("not a camera cable")
        self.play(FadeOut(VGroup(cell,lab,nerve,nl)),run_time=0.5)
        many=T("Mouse: more than 40 types",30,BLUE).move_to([0,-2.7,0])
        self.at("more than 40")
        self.play(FadeIn(many),run_time=0.5)
        ss=strands()
        self.at("different feature")
        self.play(*[Create(s[0]) for s in ss],run_time=0.8)
        self.at("local differences")
        self.play(FadeIn(ss[0][1]),run_time=0.4)
        self.at("small moving object")
        self.play(FadeIn(ss[1][1]),ss[1][1].animate.shift(RIGHT*0.35),run_time=0.6)
        self.at("motion in one direction")
        self.play(GrowArrow(ss[2][1]),run_time=0.5)
        self.at("Circuits inside the retina")
        self.play(Indicate(e,color=BLUE,scale_factor=1.08),run_time=0.8)
        self.finish()


class S02W3(SpokenScene):
    def construct(self):
        head=heading("W3: local change",BLUE)
        w=chip("W3",BLUE,34).move_to([3.8,0,0])
        self.at("Take the W3 cell")
        self.play(FadeIn(head),FadeIn(w),run_time=0.5)
        on=chip("ON",YELLOW,28).move_to([-4.7,1.4,0]); off=chip("OFF",YELLOW,28).move_to([-4.7,-1.4,0])
        a=chip("excitation",YELLOW,28).move_to([0,0,0])
        links=VGroup(arr(on.get_right(),a.get_left()+UP*.2,YELLOW),arr(off.get_right(),a.get_left()+DOWN*.2,YELLOW),arr(a.get_right(),w.get_left(),YELLOW))
        self.at("It pools excitation")
        self.play(FadeIn(on),FadeIn(off),FadeIn(a),Create(links),run_time=0.8)
        self.at("either sign excites it")
        self.play(Indicate(on),Indicate(off),Indicate(w,color=BLUE),run_time=0.8)
        am=chip("excitatory\namacrine",YELLOW,26).move_to(a)
        self.at("an excitatory amacrine cell")
        self.play(ReplacementTransform(a,am),run_time=0.6)
        sur=T("surround motion",26,GREY).move_to([0,2,0])
        suppress=VGroup(Line([-1.1,1.6,0],[-1.1,.7,0],color=GREY),Line([-1.35,.7,0],[-.85,.7,0],color=GREY),
                        Line([1.1,1.6,0],[3.8,.65,0],color=GREY),Line([3.55,.65,0],[4.05,.65,0],color=GREY))
        self.at("moves too")
        self.play(FadeIn(sur),Create(suppress),run_time=0.6)
        self.at("suppresses that excitation")
        self.play(am.animate.set_opacity(.3),links.animate.set_opacity(.3),run_time=0.5)
        self.at("inhibits the cell")
        self.play(w.animate.set_opacity(.35),run_time=0.5)
        left=motion_panel(-3.05,"Object moves; background still")
        right=motion_panel(3.05,"Whole scene moves")
        lt=spikes(-3.05,-1.7,True); rt=spikes(3.05,-1.7,False)
        wl=T("W3 spikes",24,BLUE).move_to([0,-2.7,0])
        self.at("So W3 fires")
        self.play(FadeOut(VGroup(on,off,am,w,links,sur,suppress)),FadeIn(left),FadeIn(right),FadeIn(wl),run_time=0.7)
        self.at("small object moving")
        self.play(left[2].animate.shift(RIGHT*2),Create(lt),run_time=1.3)
        wide=VGroup(Line([.8,-.65,0],[5.3,-.65,0],color=GREY,stroke_width=4),
                    *[Line([x,-.65,0],[x,-.2,0],color=GREY,stroke_width=3) for x in (1.1,2,3,4,5)])
        self.at("falls quiet")
        self.play(Create(rt),Create(wide),run_time=0.5)
        self.at("whole scene moves")
        self.play(right[1].animate.shift(RIGHT*.4),right[2].animate.shift(RIGHT*.4),wide.animate.set_color(YELLOW),run_time=1.0)
        self.finish()


class S03Jamb(SpokenScene):
    def construct(self):
        head=heading("JAM-B: one direction",BLUE)
        # Same soma and branching helper, with dendrites restricted to one side.
        cell=gcell(BLUE,1.9).move_to([-2,0,0]); tag=chip("OFF",YELLOW,26).move_to([-5,-1.9,0])
        self.at("A second channel")
        self.play(FadeIn(head),FadeIn(cell),run_time=.6)
        self.at("an OFF cell")
        self.play(FadeIn(tag),run_time=.4)
        # Stretch the upper branches sideways to make the asymmetry explicit.
        asymmetric=cell.copy()
        for branch in asymmetric[1:-1]:
            branch.shift(RIGHT*.7)
        # Preserve the soma connections when shifting the arbor tips.
        for i in (1,4,7):
            asymmetric[i].put_start_and_end_on(cell[i].get_start(),asymmetric[i].get_end())
        self.at("lopsided dendritic arbor")
        self.play(Transform(cell,asymmetric),run_time=.8)
        frame=T("motion across the retina",26,GREY).move_to([3.6,2,0])
        direction=arr([3.6,-1.6,0],[3.6,1.2,0],YELLOW)
        self.at("one direction of motion")
        self.play(FadeIn(frame),GrowArrow(direction),run_time=.6)
        bar=Line([-4.3,-1.1,0],[.6,-1.1,0],color=YELLOW,stroke_width=8)
        self.at("from the cell body")
        self.play(Create(bar),run_time=.3)
        self.at("toward the dendrites")
        self.play(bar.animate.shift(UP*2.4),run_time=1.0)
        ss=strands().shift(LEFT*1.5)
        # These channels carry colour and light level, rather than the motion
        # features illustrated by the reusable opening strands.
        ss[1][1].become(VGroup(*[Dot([3.1+d,0,0],radius=.11,color=c)
                                for d,c in zip((-.25,0,.25),(PURPLE,TEAL,YELLOW))]))
        ss[2][1].become(Circle(radius=.28,color=TEXT,fill_color=TEXT,fill_opacity=.65).move_to([3.3,-1.5,0]))
        labels=VGroup(*[T(t,26,c).move_to([4.6,y,0]) for t,c,y in zip(("contrast","colour","light level"),(YELLOW,TEAL,GREY),(1.5,0,-1.5))])
        self.at("Other channels report")
        self.play(FadeOut(VGroup(cell,tag,frame,direction,bar)),FadeIn(ss),FadeIn(labels),run_time=.7)
        gap=DashedLine([-2,-2.8,0],[2.8,-2.8,0],color=GREY)
        empty=T("no channel → information lost",26,GREY).move_to([0,-3.3,0])
        self.at("Information that no channel carries")
        self.play(Create(gap),FadeIn(empty),run_time=.7)
        self.finish()


class S04Type(SpokenScene):
    def construct(self):
        head=heading("What supports a type?",GOLD)
        self.at("How do we know")
        self.play(FadeIn(head),run_time=.6)
        cr=chip("response",YELLOW,30).move_to([-3.5,1.8,0])
        cs=chip("shape",PURPLE,30).move_to([-5,-1.2,0])
        ce=chip("expression",TEAL,30).move_to([-1.7,-1.2,0])
        self.at("shared light response")
        self.play(FadeIn(cr),run_time=.4)
        self.at("dendritic shape")
        self.play(FadeIn(cs),run_time=.4)
        self.at("gene expression profile")
        self.play(FadeIn(ce),run_time=.4)
        blob=VGroup(Circle(radius=.77,color=TEAL,fill_opacity=.2),T("cluster",24,TEAL)).move_to([3.5,1.6,0])
        note=T("not yet a type",26,TEAL).next_to(blob,DOWN,buff=.2)
        self.at("A cluster is not yet")
        self.play(FadeIn(blob),FadeIn(note),run_time=.6)
        ring=Circle(radius=.65,color=GOLD,stroke_width=5).move_to([-3.5,.15,0]); tl=T("type",28,GOLD).move_to(ring)
        links=VGroup(Line(cr.get_bottom(),ring.get_top(),color=GOLD),Line(cs.get_top(),ring.get_corner(DL),color=GOLD),Line(ce.get_top(),ring.get_corner(DR),color=GOLD))
        self.at("when these agree")
        self.play(Create(links),Create(ring),FadeIn(tl),run_time=.7)
        mos=mosaic((3.25,-1.1,0),.8,3,4)
        ml=T("spaced bodies; overlapping arbors",24,GREEN).move_to([2.7,-2.75,0])
        self.at("regular mosaic")
        self.play(FadeOut(VGroup(blob,note)),FadeIn(mos),FadeIn(ml),run_time=.7)
        caveat=T("Regularity can be weak",26,GREEN).move_to([2.8,1.6,0])
        self.at("though some real types")
        self.play(FadeIn(caveat),run_time=.5)
        self.finish()


def method_icon(kind,color):
    if kind==0:  # microscope
        return VGroup(Line([-.4,-.35,0],[.4,-.35,0],color=color,stroke_width=4),
                      Line([.2,-.35,0],[.2,.3,0],color=color,stroke_width=4),
                      Line([-.2,.35,0],[.2,.15,0],color=color,stroke_width=8))
    if kind==1:  # captured droplet, a schematic blob
        return VGroup(Circle(radius=.35,color=color),Dot(radius=.10,color=color))
    if kind==2:
        return VGroup(Line([-.4,.4,0],[.2,-.2,0],color=color,stroke_width=5),Circle(radius=.15,color=BLUE).shift(RIGHT*.3+DOWN*.3))
    return VGroup(Line([0,.4,0],[0,-.15,0],color=color,stroke_width=3),
                  Line([-.4,-.3,0],[.4,-.3,0],color=color,stroke_width=5),
                  arr([0,.3,0],[0,-.2,0],color,3))


class S05Census(SpokenScene):
    def construct(self):
        head=heading("Four methods, converging evidence")
        self.at("Each method counts")
        self.play(FadeIn(head),run_time=.6)
        cards=VGroup()
        for i,(num,label,col) in enumerate(zip(("≥ 32","46","42","≥ 35"),("imaging","sequencing","single-cell\nrecording","electron\nmicroscopy"),(YELLOW,TEAL,ORANGE,PURPLE))):
            c=card(num,label,col,40)
            icon=method_icon(i,col).next_to(c,UP,buff=.35)
            cards.add(VGroup(c,icon).move_to([-4.8+3.2*i,.65,0]))
        for cue,c in zip(("at least 32","Sequencing found","found 42","at least 35"),cards):
            self.at(cue)
            self.play(FadeIn(c,shift=UP*.2),run_time=.5)
        band=RoundedRectangle(width=12.4,height=.9,corner_radius=.15,color=GOLD,fill_color=GOLD,fill_opacity=.1).move_to([0,-1.8,0])
        self.at("These are not rival answers")
        self.play(cards.animate.move_to([0,1,0]),Create(band),run_time=.7)
        qual=T("method + resolution",28,GREY).move_to([0,-3,0])
        self.at("Each reflects")
        self.play(FadeIn(qual),run_time=.5)
        converge=VGroup(*[arr(c[0][1].get_bottom()+DOWN*.15,[x*.35,-1.3,0],col,3) for c,x,col in zip(cards,(-4.3,-1.45,1.45,4.3),(YELLOW,TEAL,ORANGE,PURPLE))])
        ans=T("about 45 types",34,GOLD).move_to(band)
        self.at("converging on about")
        self.play(Create(converge),FadeIn(ans),run_time=.8)
        self.finish()


class S06Primate(SpokenScene):
    def construct(self):
        head=heading("Mouse is not macaque")
        self.at("Mouse is not macaque")
        self.play(FadeIn(head),run_time=.5)
        array=VGroup()
        for x in (-4.8,-3.6,-2.4):
            cone=Triangle(color=YELLOW,fill_opacity=.25).scale(.22).rotate(PI).move_to([x,1.6,0])
            bp=Dot([x,.3,0],radius=.14,color=GREY)
            gc=Circle(radius=.2,color=BLUE,fill_opacity=.35).move_to([x,-1,0])
            lines=VGroup(Line([x,1.2,0],[x,.45,0],color=GREY),Line([x,.15,0],[x,-.8,0],color=BLUE))
            array.add(VGroup(cone,bp,gc,lines))
        labels=VGroup(T("cone",24,YELLOW).move_to([-.8,1.6,0]),T("bipolar",24,GREY).move_to([-.8,.3,0]),T("midget",24,BLUE).move_to([-.8,-1,0]))
        self.at("primate fovea")
        self.play(FadeIn(array),run_time=.6)
        self.at("through a bipolar cell")
        self.play(FadeIn(labels[1]),run_time=.4)
        self.at("a single cone")
        self.play(FadeIn(labels[0]),FadeIn(labels[2]),run_time=.5)
        self.at("private line supports sharp vision")
        pulse=Dot(array[1][0].get_center(),radius=.1,color=YELLOW)
        self.play(FadeIn(pulse),run_time=.2)
        self.play(pulse.animate.move_to(array[1][2]),run_time=.8)
        self.play(FadeOut(pulse),run_time=.2)
        pie=VGroup(Sector(radius=1.15,start_angle=PI/2,angle=TAU*.85,fill_color=BLUE,fill_opacity=.6,stroke_color=BG),
                   Sector(radius=1.15,start_angle=PI/2+TAU*.85,angle=TAU*.15,fill_color=GREY,fill_opacity=.4,stroke_color=BG)).move_to([3.6,.65,0])
        pl=T("Macaque foveal sample",25,GREY).move_to([3.6,2.25,0]); pct=T("≈ 85% midget",28,BLUE).move_to([3.6,-1.1,0])
        self.at("In the macaque fovea")
        self.play(FadeIn(pl),run_time=.4)
        self.at("about 85")
        self.play(FadeIn(pie),FadeIn(pct),run_time=.7)
        self.at("Shared ancestry")
        self.play(FadeOut(VGroup(array,labels,pie,pl,pct)),run_time=.5)
        sparse=VGroup(gcell(BLUE,1).move_to([-4.5,0,0]),gcell(BLUE,1).move_to([-2.6,0,0]))
        dense=mosaic((3.25,.2,0),.72,3,4).set_color(BLUE)
        labs=VGroup(T("Mouse alpha: sparse",28,BLUE).move_to([-3.5,2.2,0]),T("Primate midget: dense",28,BLUE).move_to([3.25,2.2,0]))
        rule=T("Shared ancestry ≠ shared size, frequency or job",28).move_to([0,-2.5,0])
        self.play(FadeIn(sparse),FadeIn(dense),FadeIn(labs),run_time=.7)
        self.at("does not mean")
        self.play(FadeIn(rule),run_time=.6)
        self.finish()


class S07Close(SpokenScene):
    def construct(self):
        head=heading("What the eye sends the brain")
        e=eye(); ss=strands()
        brain=VGroup(Ellipse(width=1.5,height=3.8,color=GREY),T("brain",26).rotate(PI/2)).move_to([5.65,0,0])
        self.at("So the eye")
        self.play(FadeIn(head),FadeIn(e),FadeIn(brain),run_time=.6)
        self.at("dozens of filtered versions")
        self.play(*[Create(s[0]) for s in ss],*[FadeIn(s[1]) for s in ss],run_time=.8)
        self.at("side by side")
        dots=VGroup(*[Dot([1,y,0],radius=.1,color=c) for y,c in zip((1.5,0,-1.5),(YELLOW,BLUE,PURPLE))])
        self.play(FadeIn(dots),run_time=.2)
        self.play(*[d.animate.move_to([5,y,0]) for d,y in zip(dots,(1.5,0,-1.5))],run_time=.9)
        self.play(FadeOut(dots),run_time=.2)
        line=T("The brain works with what the channels deliver.",30).move_to([0,-2.7,0])
        self.at("what those channels deliver")
        self.play(FadeIn(line),run_time=.6)
        self.finish()


class S08End(EndCard):
    LINE = "The eye sends the brain dozens of filtered versions of the scene."
