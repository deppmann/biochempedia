"""Two Facts in One Cell  (adult neurogenesis, chapter 1)

COLOR MAP (one color per concept, shared by all chapters)
  BLUE   = neurons (cells known to be neurons)
  GREY   = structure, other / dividing / unidentified cells, axes, cards
  YELLOW = the DNA label (thymidine, BrdU, grains) = the birth record
  GREEN  = neuron identity (NeuN stain)
  ORANGE = young-neuron marker (doublecortin): a state
  PURPLE = the hippocampus / dentate gyrus
  TEAL   = antibody
  RED    = unknown / missing (question marks)
  TEXT   = DNA (chromosomes), rule text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

# ---------------------------------------------------------------- helpers

def chromo(h=0.6, color=TEXT, w=0.17):
    return RoundedRectangle(corner_radius=w / 2, width=w, height=h, stroke_width=0,
                            fill_color=color, fill_opacity=1)


def body(r, color=GREY, op=0.2):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op)


def neuron(r=0.55, color=BLUE):
    """soma + dendrites + axon; returns VGroup(soma, dendrites_and_axon)"""
    soma = body(r, color, 0.22)
    br = VGroup()
    for angle in (0.3, 1.2, 2.2, 3.0):
        d = np.array([np.cos(angle), np.sin(angle), 0])
        tip = d * (r * 1.75)
        br.add(Line(d * r, tip, color=color, stroke_width=4))
        br.add(Line(tip, tip + 0.35 * r * np.array([np.cos(angle + 0.6), np.sin(angle + 0.6), 0]), color=color, stroke_width=3))
    br.add(Line(DOWN * r, DOWN * (r * 1.85), color=color, stroke_width=4))
    return VGroup(soma, br)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def grains(center, r, n=9, rad=0.07, color=YELLOW):
    pts = []
    for k in range(n):
        a = k * 2.399963
        rr = r * 0.8 * np.sqrt((k + 0.5) / n)
        pts.append(Dot(np.array([center[0] + rr * np.cos(a), center[1] + rr * np.sin(a), 0]), radius=rad, color=color))
    return VGroup(*pts)



def dg_arc(r, center, n=13, dot_color=GREY, dot_r=0.13, sw=26):
    arc = Arc(radius=r, start_angle=-0.2*PI, angle=1.4*PI,
              stroke_color=PURPLE, stroke_width=sw).set_stroke(opacity=0.45)
    arc.move_arc_center_to(np.array([*center, 0]))
    dots = VGroup(*[Dot(arc.get_arc_center()+r*np.array([np.cos(a),np.sin(a),0]),
                       radius=dot_r,color=dot_color)
                    for a in np.linspace(-0.2*PI,1.2*PI,n)])
    return VGroup(arc,dots)


def dna(c, h=0.7, gap=0.48):
    return VGroup(*[chromo(h,w=0.15).move_to([c[0]+x,c[1],0]) for x in (-gap,0,gap)])


def mature():
    n=neuron(1.2).move_to([3.4,0.05,0])
    return VGroup(n,dna(n[0].get_center(),0.65,0.4))


def daughters():
    return VGroup(*[VGroup(body(1.03).move_to([-3.5,y,0]),dna((-3.5,y),0.65,0.4))
                    for y in (1.2,-1.2)])


def copy_labels():
    return VGroup(T("dividing cell",28,TEXT).move_to([-3.5,-2.75,0]),
                  T("finished neuron",28,BLUE).move_to([3.4,-2.75,0]))


def squares(c, size=0.16):
    return VGroup(*[Square(side_length=size,stroke_width=0,fill_color=YELLOW,fill_opacity=1)
                    .move_to([c[0]+x,c[1]+y,0]) for x,y in [(-0.4,0.16),(0,-0.12),(0.4,0.17)]])


def pair():
    nuc=body(2.45,GREY,0.23).move_to([-0.7,-0.35,0])
    glia=Ellipse(width=1.9,height=4.5,stroke_color=GREY,stroke_width=4,
                 fill_color=GREY,fill_opacity=0.23).move_to([2.45,-0.35,0])
    return VGroup(nuc,glia,grains(nuc.get_center(),1.85,11,0.13))


def prediction():
    pr=pair()
    title=T("Pause and predict",30,TEAL).move_to([0,3.25,0])
    q=T("Is the labelled cell a neuron?",36).move_to([0,2.55,0])
    lab=T("labelled",28,YELLOW).move_to([-4.9,0.5,0])
    lead=arrow(lab.get_right(),[-2.2,0.2,0],YELLOW,3)
    return VGroup(pr,title,q,lab,lead)


def box(x,color,w=5.6,h=4.7):
    return RoundedRectangle(corner_radius=0.2,width=w,height=h,
        stroke_color=color,stroke_width=3,fill_color=color,fill_opacity=0.07).move_to([x,0.15,0])


def evidence_card():
    left=box(-3.05,YELLOW); right=box(3.05,GREEN)
    a=T("birth record",36,YELLOW).move_to([-3.05,1.85,0])
    b=T("neuron identity",36,GREEN).move_to([3.05,1.85,0])
    gr=grains([-3.05,0],1.5,9,0.12)
    tick=VGroup(Line([-1.7,-1.4,0],[-1.4,-1.7,0]),Line([-1.4,-1.7,0],[-0.9,-1.1,0])).set_color(TEXT).set_stroke(width=6)
    return VGroup(left,a,gr,tick),VGroup(right,b)


def rule_base():
    head=T("A neuron counts as new only when",34).move_to([0,3.1,0])
    boxes=VGroup(box(-3.05,GREY),box(3.05,GREY))
    bracket=VGroup(Line([-5.8,-2.5,0],[5.8,-2.5,0]),
                   Line([-5.8,-2.5,0],[-5.8,-2.25,0]),Line([5.8,-2.5,0],[5.8,-2.25,0])).set_stroke(TEXT,3)
    same=T("two facts in the same cells",34).move_to([0,-3.1,0])
    return VGroup(head,boxes,bracket,same)


def birth_content():
    title=T("birth record",36,YELLOW).move_to([-3.05,1.85,0])
    timeline=VGroup(arrow([-5,0.7,0],[-1.1,0.7,0],YELLOW,4),
                   Line([-4.6,0.4,0],[-4.6,1,0],color=YELLOW,stroke_width=5),
                   T("DNA copied at a known time",26,YELLOW).move_to([-3.05,0.05,0]))
    born=T("most likely born\nthen or later",30,YELLOW).move_to([-3.05,-1.2,0])
    return VGroup(title,timeline,born)


def identity_content():
    title=T("neuron identity",36,GREEN).move_to([3.05,1.85,0])
    n=neuron(0.66,GREEN).move_to([3.05,0.1,0])
    caption=T("neuron protein (NeuN)",28,GREEN).move_to([3.05,-1.55,0])
    return VGroup(title,n,caption)


def full_rule():
    base=rule_base(); base[1][0].set_stroke(YELLOW);base[1][1].set_stroke(GREEN)
    return VGroup(base,birth_content(),identity_content())


def stain_card():
    c=np.array([1.4,0,0])
    soma=body(2.65,GREEN,0.12).move_to(c)
    nuc=body(1.45,YELLOW,0.1).move_to(c).set_fill(GREEN,0.45)
    dots=grains(c,1.4,14,0.11)
    bl=T("BrdU",34,YELLOW).move_to([-4.55,1.15,0])
    nl=T("NeuN",34,GREEN).move_to([-4.55,-0.7,0])
    cap=T("neuron protein",28,GREEN).move_to([-4.55,-1.35,0])
    l1=Line(bl.get_right()+RIGHT*0.1,[0.1,0.7,0],color=YELLOW,stroke_width=3)
    l2=Line(nl.get_right()+RIGHT*0.1,[-1.25,-0.5,0],color=GREEN,stroke_width=3)
    return VGroup(soma,nuc,dots,bl,nl,cap,l1,l2)


class S00Title(TitleCard):
    LESSON="Two Places the Adult Brain Still Makes Neurons"
    TITLE="Two Facts in One Cell"


class S01Q(SpokenScene):
    def construct(self):
        brain=Ellipse(width=11.8,height=5.6,color=GREY,fill_color=GREY,fill_opacity=0.08)
        dg=dg_arc(2.4,[0,0]); dg[1][8].set_color(YELLOW)
        label=T("hippocampus",30,PURPLE).move_to([0,-3.3,0])
        self.add(brain,dg,label)
        self.at("adult brain")
        self.play(FadeIn(T("adult rat brain · schematic",28,TEXT).move_to([0,3.35,0])),run_time=0.4)
        self.at("how would you")
        q=T("?",80,RED).move_to([4.4,0.5,0])
        self.play(FadeIn(q),Indicate(dg[1][8],color=YELLOW),run_time=0.7)
        self.finish()


class S02Rule(SpokenScene):
    def construct(self):
        head=T("The old rule",30,TEXT).move_to([0,3.25,0])
        clause=T("the neurons you are born with",36).move_to([0,2.55,0])
        row=VGroup(*[neuron(0.45).move_to([x,1.15,0]) for x in (-5,-3,-1,1,3,5)])
        self.add(head,row)
        self.at("neurons you are born")
        self.play(FadeIn(clause),run_time=0.4)
        later=row.copy().shift(DOWN*3.0)
        time=arrow([-5.8,-0.5,0],[5.8,-0.5,0],TEXT,4)
        age=T("age",28,TEXT).move_to([0,-0.1,0])
        keep=T("are the neurons you keep",36).move_to([0,-3.25,0])
        self.at("are the ones")
        # Fade in a clean second row; moving copies briefly doubled the outlines.
        self.play(Create(time),FadeIn(age),FadeIn(later),FadeIn(keep),run_time=0.35)
        self.finish()


class S03Copy(SpokenScene):
    def construct(self):
        b=body(2.15).move_to([-3.5,0,0]); ch=dna((-3.5,0),1.1,0.85)
        n=mature(); labels=copy_labels()
        self.add(b,ch,n,labels)
        twin=ch.copy().shift(RIGHT*0.25)
        self.at("copies its")
        self.play(TransformFromCopy(ch,twin),run_time=0.55)
        self.at("before it divides")
        ds=daughters()
        # Each of the three original bars and three copied bars enters one daughter.
        self.play(Transform(b,VGroup(ds[0][0],ds[1][0])),
                  Transform(ch,ds[0][1]),Transform(twin,ds[1][1]),run_time=0.9)
        self.at("does not copy")
        note=T("no new copy of DNA",28,TEXT).move_to([3.4,3.15,0])
        self.play(FadeIn(note),Indicate(n[1],scale_factor=1.15,color=TEXT),run_time=0.6)
        self.finish()


class S04Label(SpokenScene):
    def construct(self):
        ds=daughters(); n=mature()
        self.add(ds,n,copy_labels(),T("no new copy of DNA",28,TEXT).move_to([3.4,3.15,0]))
        tag=chip("tagged thymidine",YELLOW,30).move_to([-3.5,3.2,0])
        sub=T("a DNA building block",28,TEXT).move_to([0,-3.4,0])
        self.at("tagged thymidine")
        self.play(FadeIn(tag),run_time=0.4)
        self.at("building block")
        self.play(FadeIn(sub),run_time=0.35)
        # Reuse the two daughters without resetting the preceding division.
        targets=VGroup(squares((-3.5,1.2),size=0.23),squares((-3.5,-1.2),size=0.23))
        self.at("cells copying")
        blocks=[b for group in targets for b in group]
        for b in blocks:
            target=b.get_center(); b.move_to(tag.get_bottom()+DOWN*0.2)
            self.add(b);self.play(b.animate.move_to(target),run_time=0.15)
        self.at("build it in")
        self.play(FadeOut(sub),run_time=0.2)
        self.play(FadeIn(T("no label",28,TEXT).move_to([3.4,-3.35,0])),run_time=0.35)
        self.finish()


class S05Halve(SpokenScene):
    def construct(self):
        def cell(x,y,f):
            c=body(0.65).move_to([x,y,0])
            gauge=Rectangle(width=1.05,height=0.2,color=GREY,stroke_width=2).move_to([x,y-0.16,0])
            fill=Rectangle(width=1.01*f,height=0.14,stroke_width=0,fill_color=YELLOW,fill_opacity=1)
            fill.move_to(gauge.get_left()+RIGHT*(0.02+fill.width/2))
            return VGroup(c,gauge,fill)
        top=cell(0,2.55,1)
        key=T("yellow bar = label in the DNA",28,YELLOW).move_to([0,3.5,0])
        self.add(top,key,T("full",28,YELLOW).move_to([-4.8,2.55,0]))
        halves=VGroup(*[cell(x,0.3,0.5) for x in (-2.4,2.4)])
        links=VGroup(*[Line([0,1.9,0],[x,0.95,0],color=GREY) for x in (-2.4,2.4)])
        self.at("divide again")
        self.play(Create(links),TransformFromCopy(top,halves),run_time=0.7)
        self.at("each daughter")
        self.play(FadeIn(T("about half",28,YELLOW).move_to([-4.8,0.3,0])),run_time=0.3)
        quarters=VGroup(*[cell(x,-2.15,0.25) for x in (-3.6,-1.2,1.2,3.6)])
        lines=VGroup(*[Line([px,-0.35,0],[x,-1.5,0],color=GREY) for px,xs in [(-2.4,(-3.6,-1.2)),(2.4,(1.2,3.6))] for x in xs])
        self.at("about half")
        self.play(Create(lines),TransformFromCopy(halves,quarters),run_time=0.7)
        self.play(FadeIn(T("about a quarter",28,YELLOW).move_to([0,-3.25,0])),run_time=0.3)
        self.finish()


class S06Later(SpokenScene):
    def construct(self):
        axis=arrow([-6,-1.3,0],[6,-1.3,0],TEXT,6)
        given=chip("label given",YELLOW,32).move_to([-3.9,-0.3,0])
        tick=Line([-3.9,-0.95,0],[-3.9,-1.65,0],color=YELLOW,stroke_width=7)
        n=neuron(1.15).move_to([1.6,1,0]);sq=squares(n[0].get_center())
        self.add(axis,tick,given,n,sq,T("time",28,TEXT).move_to([5.6,-1.85,0]))
        self.at("strongly labeled")
        lab=T("strongly labelled\nneuron",30,BLUE).move_to([4.9,-0.15,0])
        self.play(FadeIn(lab),Create(DashedLine(n[0].get_bottom(),[1.6,-1.3,0],color=GREY)),run_time=0.55)
        self.at("most likely")
        self.play(Create(arrow([-3.9,-2.4,0],[6,-2.4,0],YELLOW,6)),
                  FadeIn(T("most likely born: that day, or later",30,YELLOW).move_to([0,-3.15,0])),run_time=0.6)
        self.finish()


class S06bRepair(SpokenScene):
    def construct(self):
        n=neuron(1.25).move_to([-3.3,0.1,0]);ch=dna(n[0].get_center(),0.8,0.5)
        dc=body(2.15).move_to([3.3,0.1,0]);dch=dna((3.3,0.1),0.8,0.5)
        self.add(n,ch,dc,dch)
        spot=ch[0].get_center()+UP*0.2
        pale="#F5E89A"
        dot=Dot(spot,radius=0.07,color=pale)
        rep=T("repair",30,TEXT).move_to([-3.3,2.95,0])
        lead=Line(rep.get_bottom(),spot+UP*0.12,color=pale,stroke_width=2)
        self.at("dna repair")
        self.play(FadeIn(rep),Create(lead),FadeIn(dot),run_time=0.4)
        self.at("a dying cell")
        self.play(dc.animate.set_stroke(opacity=0.5),dch.animate.set_opacity(0.5),
                  FadeIn(T("dying cell",30,TEXT).move_to([3.3,2.95,0])),run_time=0.4)
        self.at("can add label")
        self.play(FadeIn(Dot(dch[0].get_center()+UP*0.2,radius=0.07,color=pale)),run_time=0.3)
        self.add(T("non-dividing neuron",28,BLUE).move_to([-3.3,-2.65,0]))
        self.at("studies need")
        self.play(FadeIn(T("faint label, no division · controls needed",30).move_to([0,-3.35,0])),run_time=0.4)
        self.finish()


class S07Altman(SpokenScene):
    def construct(self):
        dg=dg_arc(2.25,[-3.6,0.2]);dg[1][8].set_color(YELLOW)
        pr=pair().scale(0.78).move_to([3.1,0.15,0])
        circle=Ellipse(width=6.3,height=5.6,color=GREY,stroke_width=2).move_to([3.1,0.15,0])
        link=DashedLine(dg[1][8].get_center(),circle.get_left(),color=YELLOW)
        self.add(dg,pr,circle,link)
        self.at("joseph altman")
        self.play(FadeIn(T("Altman, 1960s · tritiated thymidine",28,TEXT).move_to([0,-3.4,0])),run_time=0.4)
        self.at("found labeled")
        self.play(FadeIn(T("grains = label",28,YELLOW).move_to([3.3,-2.95,0])),run_time=0.35)
        self.at("dentate gyrus")
        self.play(FadeIn(T("dentate gyrus",30,PURPLE).move_to([-3.6,3.15,0])),
                  FadeIn(T("section, magnified",28,TEXT).move_to([3.3,3.15,0])),run_time=0.4)
        self.finish()


class S08Pred(SpokenScene):
    def construct(self):
        self.add(prediction());self.at("pause and predict");self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        self.add(prediction());self.finish()


class S10Rev1(SpokenScene):
    def construct(self):
        pr=pair();self.add(pr)
        self.at("the light microscope")
        self.play(FadeIn(T("light microscope",30,TEXT).move_to([0,3.45,0])),run_time=0.3)
        self.at("could not tell")
        bracket=VGroup(Line([-2.95,2.15,0],[3.4,2.15,0]),Line([-2.95,2.15,0],[-2.95,1.95,0]),Line([3.4,2.15,0],[3.4,1.95,0])).set_stroke(RED,3)
        self.play(Create(bracket),FadeIn(T("?  Which one holds the grains?",30,RED).move_to([0,2.75,0])),run_time=0.4)
        self.at("a glial cell")
        self.play(FadeIn(T("glial cell",30,TEXT).move_to([2.45,-3.15,0])),run_time=0.3)
        self.at("a neuron")
        self.play(FadeIn(T("neuron",30,BLUE).move_to([-0.7,-3.15,0])),run_time=0.3)
        self.finish()


class S11Rev2(SpokenScene):
    def construct(self):
        a,b=evidence_card();self.add(a)
        self.at("no identity")
        self.play(FadeIn(b),run_time=0.5)
        self.at("set aside")
        # Lower fill and stroke separately: never turn a translucent fill opaque.
        self.play(a[0].animate.set_fill(opacity=0.025).set_stroke(opacity=0.35),
                  b[0].animate.set_fill(opacity=0.025).set_stroke(opacity=0.35),
                  *[m.animate.set_opacity(0.4) for m in [*a[1:],*b[1:]]],
                  FadeIn(T("claims largely set aside for years",32,TEXT).move_to([0,-3.15,0])),run_time=0.6)
        self.finish()


class S12Beat(NarratedScene):
    def construct(self):
        a,b=evidence_card()
        for group in (a,b):
            group[0].set_fill(opacity=0.025).set_stroke(opacity=0.35)
            for m in group[1:]:m.set_opacity(0.4)
        self.add(a,b,T("claims largely set aside for years",32,TEXT).move_to([0,-3.15,0]));self.finish()


class S13Em(SpokenScene):
    def construct(self):
        n=neuron(1.5,GREY).move_to([0,-0.05,0])
        gr=grains(n[0].get_center(),1.15,12,0.1)
        em=chip("electron microscope view",TEXT,30).move_to([0,3.35,0])
        cred=T("Kaplan and Hinds, 1977 · rat",28,TEXT).move_to([0,-3.4,0])
        self.add(n,gr,em,cred)
        self.at("showed that")
        self.play(Indicate(gr,color=YELLOW,scale_factor=1.1),run_time=0.4)
        self.at("were neurons")
        label=T("labelled cell\n= neuron",32,YELLOW).move_to([-4.7,-1.25,0])
        leader=Line(label.get_right()+RIGHT*0.1,n[0].get_left()+DOWN*0.5,color=YELLOW,stroke_width=3)
        attachment=n[1][0].point_from_proportion(0.6)
        spine_tip=attachment+UP*0.55
        spine=VGroup(Line(attachment,spine_tip),Circle(radius=0.13).move_to(spine_tip)).set_color(BLUE)
        feat=T("neuron features",28,BLUE).move_to([4.5,2.1,0])
        pointer=Line(feat.get_left(),spine_tip+RIGHT*0.18,color=BLUE,stroke_width=3)
        self.play(n.animate.set_color(BLUE),FadeIn(label),Create(leader),FadeIn(spine),FadeIn(feat),Create(pointer),run_time=0.7)
        self.finish()


class S14Brdu(SpokenScene):
    def construct(self):
        def block(x,name,tag):
            bd=RoundedRectangle(width=4.6,height=4.2,corner_radius=0.25,color=YELLOW,
                fill_color=YELLOW,fill_opacity=0.12).move_to([x,-0.5,0])
            nm=T(name,36,YELLOW).move_to([x,-1.3,0])
            tab=chip(tag,TEXT,28).move_to([x,0.6,0])
            return VGroup(bd,nm,tab)
        th=block(-3.5,"thymidine","methyl");br=block(3.5,"BrdU","bromine")
        self.add(th)
        self.at("then came")
        self.play(FadeIn(br),Create(arrow([-1.15,-0.5,0],[1.15,-0.5,0],YELLOW,4)),run_time=0.5)
        self.at("a thymidine")
        self.play(FadeIn(T("same shape · bromine in place of methyl",30,TEXT).move_to([0,3.1,0])),run_time=0.5)
        ab=VGroup(Line([0,0,0],[0.7,0,0]),Line([0,0,0],[-0.4,0.4,0]),Line([0,0,0],[-0.4,-0.4,0])).set_color(TEAL).set_stroke(width=6).move_to([5.85,0.6,0])
        self.at("antibody")
        self.play(FadeIn(ab),FadeIn(T("antibody",28,TEAL).move_to([4.8,2.05,0])),run_time=0.4)
        self.play(ab.animate.shift(LEFT*0.7),run_time=0.5)
        self.finish()


class S15Two(SpokenScene):
    def construct(self):
        card=stain_card();card[0].set_stroke(GREY).set_fill(GREY,0.12);card[1].set_fill(GREY,0.15).set_stroke(GREY)
        self.add(card[0],card[1])
        self.at("stained twice")
        self.play(FadeIn(card[2]),FadeIn(card[3]),Create(card[6]),card[1].animate.set_stroke(YELLOW),run_time=0.6)
        self.at("neuron protein")
        self.play(card[0].animate.set_stroke(GREEN).set_fill(GREEN,0.12),card[1].animate.set_fill(GREEN,0.45),
                  FadeIn(card[4]),FadeIn(card[5]),Create(card[7]),run_time=0.6)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        self.add(stain_card());self.finish()


class S17R1(SpokenScene):
    def construct(self):
        base=rule_base()
        placeholders=VGroup(birth_content()[0],identity_content()[0]).set_color(GREY).set_opacity(0.55)
        self.add(base[1],placeholders)
        self.at("a neuron counts")
        self.play(FadeIn(base[0]),run_time=0.4)
        self.at("same cells")
        self.play(Create(base[2]),FadeIn(base[3]),run_time=0.5)
        self.finish()


class S18R2(SpokenScene):
    def construct(self):
        base=rule_base();bc=birth_content();ic=identity_content()
        placeholders=VGroup(bc[0].copy(),ic[0].copy()).set_color(GREY).set_opacity(0.55)
        self.add(base,placeholders)
        self.at("birth record")
        self.play(base[1][0].animate.set_stroke(YELLOW),ReplacementTransform(placeholders[0],bc[0]),run_time=0.4)
        self.at("copied at")
        self.play(FadeIn(bc[1]),run_time=0.5)
        self.at("most likely")
        self.play(FadeIn(bc[2]),run_time=0.5)
        self.at("neuron identity")
        self.play(base[1][1].animate.set_stroke(GREEN),
                  ReplacementTransform(placeholders[1],ic[0]),FadeIn(ic[1:]),run_time=0.5)
        self.finish()


class S19R3(SpokenScene):
    def construct(self):
        rule=full_rule();self.add(rule)
        # Reflow at the third fact: keep the two established facts together on the left.
        self.at("a young neuron marker")
        left=VGroup(
            T("A neuron counts as new only when",34).move_to([0,3.1,0]),
            box(-4.25,YELLOW,w=3.8),box(0,GREEN,w=3.8),
            T("birth record",30,YELLOW).move_to([-4.25,1.85,0]),
            T("DNA copied at\na known time",28,YELLOW).move_to([-4.25,0.6,0]),
            arrow([-5.6,-0.25,0],[-2.9,-0.25,0],YELLOW,4),
            T("most likely born\nthen or later",26,YELLOW).move_to([-4.25,-1.25,0]),
            T("neuron identity",28,GREEN).move_to([0,1.85,0]),
            neuron(0.65,GREEN).move_to([0,0.1,0]),
            T("neuron protein\n(NeuN)",26,GREEN).move_to([0,-1.6,0]),
            T("two facts in the same cells",30).move_to([-2.1,-3.1,0]),
            Line([-6.1,-2.5,0],[1.9,-2.5,0],color=TEXT,stroke_width=3),
            Line([-6.1,-2.5,0],[-6.1,-2.3,0],color=TEXT,stroke_width=3),
            Line([1.9,-2.5,0],[1.9,-2.3,0],color=TEXT,stroke_width=3))
        self.play(Transform(rule,left),run_time=0.6)
        bx=RoundedRectangle(width=3.8,height=4.7,corner_radius=0.2,color=ORANGE,
            fill_color=ORANGE,fill_opacity=0.07).move_to([4.25,0.15,0])
        title=T("young-neuron\nmarker",28,ORANGE).move_to([4.25,1.65,0])
        self.play(FadeIn(bx),FadeIn(title),run_time=0.35)
        self.at("such as")
        self.play(FadeIn(T("doublecortin",30,ORANGE).move_to([4.25,0.15,0])),run_time=0.35)
        self.at("tells you")
        self.play(FadeIn(T("a state",28).move_to([4.25,-0.75,0])),run_time=0.3)
        self.at("not when")
        self.play(FadeIn(T("not a birth date",28).move_to([4.25,-1.6,0])),run_time=0.3)
        self.finish()


class S20Take(SpokenScene):
    def construct(self):
        card=stain_card()
        cap=T("two facts in the same cells",36).move_to([0,-3.3,0])
        # The closing evidence is already visible when the first spoken word starts.
        self.add(card,cap)
        self.at("two facts")
        self.play(Indicate(card[2],color=YELLOW,scale_factor=1.05),run_time=0.4)
        self.finish()


class S21End(EndCard):
    LINE="New neuron: a birth record and neuron identity in the same cells."
    def construct(self):
        line=VGroup(*[T(text,36) for text in ("New neuron:","a birth record and neuron identity","in the same cells.")]).arrange(DOWN,buff=0.2)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=TEAL,stroke_width=3)
        site=T("biochemistrypedia.com",26,TEAL)
        card=VGroup(line,rule,site).arrange(DOWN,buff=0.45).move_to(ORIGIN)
        self.add(card)
        self.finish()
