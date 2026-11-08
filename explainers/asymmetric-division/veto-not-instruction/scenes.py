"""Chapter 4 — A Veto, Not an Instruction.

COLOR MAP inherited from scenes.old.py:
YELLOW = Numb; TEAL = Notch / signal; RED = block;
GREY = cells / Notch-off state; VIOLET = inner branch;
ORANGE = outer branch; BLUE = renewal; GREEN = differentiation;
GOLD = apical polarity; TEXT = other cargo / neutral labels.
This chapter's specified comparison uses GREY/TEAL for off/on states,
not branch identity (hair and neuron both have a Notch-off state).
"""
from bp_style import *

GREY = "#B8C0CE"  # readable helper labels and Notch-off cells
ORANGE = "#F29E4C"
VIOLET = "#A98BE0"
LESSON = "Asymmetric Division: Numb and the Neuroblast"

# Geometry helpers reused from the reference film.
def cell(c, r, color=GREY, op=.14):
    return Circle(radius=r, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=op).move_to(c)


def crescent(center, r, span=2, w=12):
    return Arc(radius=r, start_angle=PI-span/2, angle=span,
               arc_center=center, color=YELLOW, stroke_width=w)


def arr(a, b, color=TEAL, w=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=.22,
                 max_tip_length_to_length_ratio=.5)


def label(s, x=0, y=3.1, color=TEXT, size=30):
    return T(s, size=size, color=color).move_to([x,y,0])


def cross(m):
    return Cross(m, stroke_color=RED, stroke_width=6)


def node(s, x, y, r=.8, on=False, numb=False, size=24):
    c = cell([x,y,0], r, TEAL if on else GREY)
    g = VGroup(c, label(s,x,y,size=size))
    if numb:
        g.add(crescent([x,y,0],r,w=9))
    return g


def signal_cross(center):
    x,y,z=center
    return VGroup(Line([x-.25,y-.3,0],[x+.25,y+.3,0],color=RED,stroke_width=6),
                  Line([x-.25,y+.3,0],[x+.25,y-.3,0],color=RED,stroke_width=6))


def question_pair():
    return VGroup(node("Numb",-2.7,0,1.9,numb=True,size=32),
                  node("Notch on",2.7,0,1.9,on=True,size=32))


def table(n=3):
    heads=VGroup(label("Division",-4.9,2.75,size=26),
                 label("Numb daughter",-.9,2.95,YELLOW,27),
                 label("Notch off",-.9,2.45,GREY,26),
                 label("Sister · Notch on",3.8,2.75,TEAL,27))
    rows=VGroup()
    for i,(div,a,b) in enumerate((("First","inner precursor","outer precursor"),
                                  ("Outer precursor","hair cell","socket cell"),
                                  ("Inner precursor","neuron","sheath cell"))):
        y=1.35-i*1.75
        row=VGroup(label(div,-4.9,y,size=26),
                   RoundedRectangle(width=3.7,height=1.45,corner_radius=.2,
                       color=GREY,fill_color=GREY,fill_opacity=.16).move_to([-.9,y,0]),
                   VGroup(label(a,-.55,y+.22,size=26),label("Notch-off",-.55,y-.36,GREY,26),
                          crescent([-2,y,0],.52,w=8)),
                   RoundedRectangle(width=3.7,height=1.45,corner_radius=.2,
                       color=TEAL,fill_color=TEAL,fill_opacity=.16).move_to([3.8,y,0]),
                   label(b,3.8,y,size=26))
        rows.add(row)
    return heads,rows


def veto():
    c=cell([-2.7,0,0],2.35)
    signal=arr([-.1,.65,0],[-3.6,.65,0])
    numb=VGroup(crescent([-2.7,0,0],2.35),label("Numb",-3.1,-1.5,YELLOW,28))
    stop=signal_cross([-2.1,.65,0])
    return c,signal,numb,stop


def absent_slot(x,y):
    return VGroup(DashedVMobject(RoundedRectangle(width=1.8,height=.65,corner_radius=.1,
                     color=TEAL).move_to([x,y,0]),num_dashes=18),
                  label("no Notch",x,y,TEAL,26))


def grid(result=False, singles=True):
    title=label("MP2 lineage",0,3.15,size=32)
    rows=VGroup()
    for i,name in enumerate(("Wild type","Notch mutant","Numb mutant","Double mutant")):
        y=2.05-i*1.5
        g=VGroup(label(name,-3.9,y,size=28))
        known=i==0 or (singles and i<3) or (result and i==3)
        if known:
            kinds=(False,True) if i==0 else ((True,True) if i==2 else (False,False))
            for j,on in enumerate(kinds):
                g.add(node("vMP2" if on else "dMP2",.1+j*3,y,.64,on=on,
                           numb=(i==0 and j==0),size=26))
        else:
            g.add(RoundedRectangle(width=5,height=1.2,corner_radius=.15,color=GREY).move_to([1.6,y,0]),
                  label("?",1.6,y,size=34))
        rows.add(g)
    return VGroup(title,rows)


def prediction():
    # Focus on the unknown row, with the two mechanisms large enough to read.
    title=label("What should a fly lacking both make?",0,3.05,size=33)
    unknown=VGroup(label("Double mutant",0,1.95,size=29),
        node("?",-1.4,.45,1.05,size=44),node("?",1.4,.45,1.05,size=44))
    a=VGroup(label("Instruction?",-3,-1.3,size=30),
             chip("no Numb note",GREY,27).move_to([-3,-2.15,0]))
    b=VGroup(label("Veto?",3,-1.3,size=30),absent_slot(3,-2.15),
             label("nothing to block?",3,-2.9,size=26))
    return VGroup(title,unknown,a,b)


def result_link():
    # Teal outlines join only the Notch-mutant row and the double-mutant row.
    def frame(y):
        return RoundedRectangle(width=4.7,height=1.38,corner_radius=.2,color=TEAL,
                                stroke_width=4).move_to([1.6,y,0])
    return VGroup(frame(.55),frame(-2.45),
                  label("same",5.5,.55,TEAL,27),label("same",5.5,-2.45,TEAL,27))


def verdict():
    return label("Veto fits · instruction fails",0,-3.4,size=28)


def mp2_pair():
    return VGroup(node("dMP2",-2,-1,1.25,numb=True,size=30),
                  node("vMP2",2,-1,1.25,on=True,size=30))


class S00Title(TitleCard):
    LESSON = LESSON
    TITLE = "A Veto, Not an Instruction"
    def construct(self):
        g=VGroup(T("BIOCHEMISTRYPEDIA",22,TEAL),
                 T(self.LESSON,24),VGroup(T("A Veto,",48,font=TITLE_FONT),T("Not an Instruction",48,font=TITLE_FONT)).arrange(DOWN,buff=.12),
                 Line(LEFT*1.3,RIGHT*1.3,color=GOLD,stroke_width=4)).arrange(DOWN,buff=.4)
        self.play(FadeIn(g),run_time=.6)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        p=question_pair(); self.add(p)
        self.at("goes into the daughter")
        self.play(Indicate(p[0],color=YELLOW,scale_factor=1.02),run_time=.5)
        self.at("does not hear")
        self.play(FadeIn(label("Notch off",-2.7,-2.5,GREY,28)),run_time=.4)
        self.at("is numb an instruction")
        self.play(FadeIn(label("Instruction — or veto?",0,3.1,size=38)),run_time=.5)
        self.finish()


class S02Facts(SpokenScene):
    def construct(self):
        tree=VGroup(node("mother",-3.5,2.1,.8,size=26),
             Line([-3.5,1.3,0],[-5.2,-.45,0],color=GREY),
             Line([-3.5,1.3,0],[-1.8,-.45,0],color=GREY),
             node("Numb",-5.2,-1.65,1.25,numb=True,size=28),
             node("Notch on",-1.8,-1.65,1.25,on=True,size=28))
        self.add(tree,label("Two facts",2.7,2.7,size=34))
        self.at("at each division")
        self.play(FadeIn(label("1. Notch chooses\nbetween sisters",2.8,1,TEAL,30)),run_time=.45)
        self.at("goes into one daughter")
        self.play(Indicate(tree[3],color=YELLOW),
                  FadeIn(label("2. Numb enters\nonly one sister",2.8,-1.35,YELLOW,30)),run_time=.5)
        self.finish()


class S03Table1(SpokenScene):
    def construct(self):
        h,r=table()
        self.add(h,*[VGroup(row[0],row[1],row[3]) for row in r])
        self.at("put them side by side")
        self.play(Indicate(h,color=TEXT,scale_factor=1.02),run_time=.4)
        self.at("at the first division")
        self.play(FadeIn(r[0][2]),FadeIn(r[0][4]),run_time=.5)
        self.at("does not hear")
        self.play(r[0][1].animate.set_stroke(YELLOW,5),run_time=.4)
        self.finish()


class S04Table2(SpokenScene):
    def construct(self):
        h,r=table(); r[0][1].set_stroke(YELLOW,5)
        self.add(h,r[0],*[VGroup(row[0],row[1],row[3]) for row in r[1:]])
        self.at("at the outer")
        self.play(FadeIn(r[1][2]),FadeIn(r[1][4]),run_time=.5)
        self.at("at the inner")
        self.play(FadeIn(r[2][2]),FadeIn(r[2][4]),run_time=.5)
        self.finish()


class S05Pattern(SpokenScene):
    def construct(self):
        h,r=table(); self.add(h,r)
        self.at("the numb daughter")
        self.play(*[VGroup(row[3],row[4]).animate.set_opacity(.3) for row in r],
                  *[row[1].animate.set_stroke(YELLOW,6).set_fill(YELLOW,.22) for row in r],run_time=.6)
        tag=label("all Notch-off",-.9,-3.25,YELLOW,28)
        self.play(FadeIn(tag),run_time=.3)
        self.at("two readings fit")
        self.remove(tag)
        self.add(label("Instruction?             Veto?",0,-3.25,size=30))
        self.finish()


class S06Instruction(SpokenScene):
    def construct(self):
        C=[-1.9,0,0]; NC=[-1.4,-.6,0]
        c=cell(C,2.9); nuc=cell(NC,1.35)
        carrier=crescent(C,2.9)
        numb_label=label("Numb",-6.1,0,YELLOW,28)
        self.add(c,nuc,carrier,numb_label)
        self.at("is an instruction")
        note=chip("names a fate",YELLOW,27).move_to([-1.4,1.7,0])
        self.play(FadeIn(label("Instruction?",3.9,2.5,size=34)),FadeIn(note),run_time=.4)
        self.at("it tells the cell")
        mini=crescent([-1.4,2.35,0],.38,span=2.4,w=9).rotate(-PI/2,about_point=[-1.4,2.35,0])
        self.play(ReplacementTransform(carrier,mini),run_time=.35)
        pack=VGroup(mini,note)
        self.play(pack.animate.shift(DOWN*2.5),run_time=.55)
        self.at("a cell without")
        self.play(FadeOut(pack),
                  ReplacementTransform(numb_label,label("no Numb",-6.1,0,GREY,28)),
                  FadeIn(label("no Numb note",3.9,.9,size=30)),run_time=.4)
        self.at("cannot take that fate")
        fate=chip("that fate",GREY,28).move_to(NC)
        self.play(FadeIn(fate),run_time=.25)
        self.play(Create(cross(fate)),run_time=.25)
        self.finish()


class S07Veto(SpokenScene):
    def construct(self):
        c,s,n,x=veto(); self.add(c,n)
        self.at("is a veto")
        self.play(FadeIn(label("Veto?",2.8,2.5,size=36)),run_time=.4)
        self.at("carries no message")
        self.play(FadeIn(label("No fate note",2.8,1.05,size=30)),run_time=.4)
        self.at("blocks notch",lead=.12)
        self.play(GrowArrow(s),Create(x),FadeIn(label("Notch signal",-2.7,2.95,TEAL,27)),
                  FadeIn(label("Notch response\nblocked",2.8,-1,TEAL,32)),run_time=.45)
        self.finish()


class S08Veto2(SpokenScene):
    def construct(self):
        p=VGroup(node("Numb",-2.7,0,1.9,numb=True,size=30),node("No Notch",2.7,0,1.9,size=30))
        self.at("then a cell")
        self.play(FadeIn(p[0]),run_time=.4)
        self.at("a cell without")
        self.play(FadeIn(p[1]),run_time=.4)
        self.at("would take")
        self.play(FadeIn(label("Same Notch-off fate",0,-2.8,GREY,34)),run_time=.4)
        self.finish()


class S09Both(SpokenScene):
    def construct(self):
        self.add(label("Numb mutant · both models agree",0,3.15,size=32))
        panels=VGroup()
        for x,title in ((-3.25,"Instruction"),(3.25,"Veto")):
            panel=VGroup(label(title,x,2.25,size=30),
                crescent([x-1.8,1.1,0],.35,w=9),signal_cross([x-1.8,1.1,0]),
                label("no Numb",x+.3,1.1,GREY,27),
                node("Notch on",x-1.15,-.85,1.1,on=True,size=26),
                node("Notch on",x+1.15,-.85,1.1,on=True,size=26))
            panels.add(panel)
        self.add(panels)
        self.at("every daughter hears")
        arrows=VGroup(*[arr([x, .6,0],[x,.1,0]) for x in (-4.4,-2.1,2.1,4.4)])
        self.play(*[GrowArrow(a) for a in arrows],run_time=.45)
        self.at("take notch away")
        self.play(FadeIn(label("Now remove Notch too",0,-2.85,TEAL,32)),run_time=.45)
        self.finish()


class S10Double(SpokenScene):
    def construct(self):
        c=node("Double\nmutant",0,1,1.25,size=28)
        absent=VGroup(crescent([-3,1,0],.45),signal_cross([-3,1,0]),
                      label("no Numb",-3,-.05,size=27))
        missing=VGroup(arr([3.8,1,0],[1.5,1,0]),signal_cross([2.7,1,0]),
                       label("no Notch",3,2.1,TEAL,27))
        self.add(c,absent,missing,label("Which single mutant?",0,3.15,size=34))
        self.at("which single mutant")
        candidates=VGroup(chip("Notch mutant: dMP2 + dMP2",GREY,26).move_to([-3,-1.4,0]),
                          chip("Numb mutant: vMP2 + vMP2",TEAL,26).move_to([3,-1.4,0]))
        self.play(FadeIn(candidates),run_time=.5)
        self.at("epistasis analysis",lead=0)
        self.play(FadeIn(chip("epistasis analysis",TEXT,34).move_to([0,-2.9,0])),run_time=.4)
        self.finish()


class S11Mp2b(SpokenScene):
    def construct(self):
        cord=RoundedRectangle(width=8.6,height=5.5,corner_radius=.65,color=GREY,fill_opacity=.04).shift(DOWN*.25)
        bands=VGroup(*[Line([-4.1,y,0],[4.1,y,0],color=GREY,stroke_opacity=.25) for y in (-2.65,1.95)])
        mother=node("MP2",0,.55,1.1,size=32); self.add(mother)
        self.at("a precursor in")
        self.play(FadeIn(cord),FadeIn(bands),FadeIn(label("Fly CNS · schematic nerve cord",0,3.15,size=29)),run_time=.5)
        self.at("it makes")
        cleavage=DashedLine([0,-.5,0],[0,1.6,0],color=TEXT)
        self.play(mother[0].animate.stretch(1.65,0),FadeOut(mother[1]),Create(cleavage),run_time=.35)
        self.play(ReplacementTransform(mother[0],VGroup(cell([-2,-1,0],1.25),cell([2,-1,0],1.25,TEAL))),
                  FadeOut(cleavage),run_time=.6)
        self.at("dmp2")
        self.play(FadeIn(label("dMP2",-2,-1,size=30)),Create(crescent([-2,-1,0],1.25)),run_time=.35)
        self.at("and vmp2")
        self.play(FadeIn(label("vMP2",2,-1,size=30)),run_time=.35)
        self.finish()


class S11bOutside(SpokenScene):
    def construct(self):
        p=VGroup(node("dMP2",-2.6,-1,1.25,numb=True,size=30),
                 node("vMP2",2.6,-1,1.25,on=True,size=30))
        self.add(p,label("MP2 lineage",0,-3.25,size=28))
        pill=VGroup(RoundedRectangle(width=5.2,height=1.05,corner_radius=.5,color=GREY,
                                     fill_color=GREY,fill_opacity=.14).move_to([2.6,2.45,0]),
                    label("cells outside the lineage",2.6,2.45,size=26))
        self.at("comes from cells")
        self.play(FadeIn(pill),run_time=.4)
        self.at("outside the lineage")
        self.play(GrowArrow(arr([2.6,1.9,0],[2.6,.4,0])),
                  FadeIn(label("Notch signal",4.55,1.15,TEAL,27)),run_time=.4)
        self.at("not from the sister")
        forbidden=arr([-1.1,-1,0],[1.1,-1,0]).set_opacity(.6)
        self.play(GrowArrow(forbidden),FadeIn(label("not from\nthe sister",0,-1.85,size=26)),run_time=.4)
        self.play(Create(signal_cross([0,-1,0])),run_time=.25)
        self.finish()


class S12Single(SpokenScene):
    def construct(self):
        g=grid(singles=False); self.add(g)
        full=grid()
        self.at("notch mutants make")
        self.remove(g[1][1])
        self.play(FadeIn(full[1][1]),run_time=.5)
        self.at("numb mutants make")
        self.remove(g[1][2])
        self.play(FadeIn(full[1][2]),run_time=.5)
        self.finish()


class S13Predict(SpokenScene):
    def construct(self):
        p=prediction(); self.add(p[0],p[1])
        self.at("what should a fly")
        self.play(Indicate(p[1],color=YELLOW,scale_factor=1.03),run_time=.45)
        self.at("is an instruction")
        self.play(FadeIn(p[2]),run_time=.4)
        self.at("if it is a veto")
        self.play(FadeIn(p[3]),run_time=.4)
        self.finish()


class S14Pause(Scene):
    def construct(self):
        self.camera.background_color=BG
        self.add(prediction())
        ring=Circle(radius=.5,color=GREY).move_to([5.5,.5,0]); self.add(ring)
        for i in range(5,0,-1):
            count=label(str(i),5.5,.5,size=30); self.add(count)
            arc=Arc(radius=.5,start_angle=PI/2,angle=TAU*i/5,color=YELLOW,stroke_width=7).move_arc_center_to([5.5,.5,0])
            self.add(arc); self.wait(1); self.remove(count,arc)


class S15InstrPred(SpokenScene):
    def construct(self):
        self.add(label("Double mutant, if Numb is an instruction",0,3.1,size=32),
                 node("dMP2",1.7,-.25,1.85,size=38),
                 label("no Notch",1.7,-2.7,TEAL,28))
        missing=VGroup(crescent([-3,1.2,0],.7),signal_cross([-3,1.2,0]),
                       label("no Numb note",-3,-.1,size=30))
        self.at("were an instruction")
        self.play(FadeIn(missing),run_time=.4)
        self.at("could make no",lead=0)
        self.play(Create(signal_cross([4.25,-.25,0])),
                  FadeIn(label("could make no dMP2",0,-3.35,size=31)),run_time=.4)
        self.finish()


def receptor_slot(x,y):
    # Empty receptor slot sitting on a cell edge.
    return DashedVMobject(RoundedRectangle(width=1.1,height=.42,corner_radius=.08,
                          color=TEAL,stroke_width=4).move_to([x,y,0]),num_dashes=14)


class S16VetoPred(SpokenScene):
    def construct(self):
        cy=.7; xs=(-2.2,2.2); r=1.0
        self.add(label("Double mutant, if Numb is a veto",0,3.15,size=32),
                 node("dMP2",xs[0],cy,r,size=30),node("dMP2",xs[1],cy,r,size=30))
        for x in xs:
            self.add(receptor_slot(x,cy+r),label("no Notch",x,cy+r+.55,TEAL,26))
        ghost=crescent([-5.4,1.3,0],.45).set_opacity(.45)
        self.add(ghost,signal_cross([-5.4,1.3,0]),label("no Numb",-5.4,.55,YELLOW,27))
        self.at("nothing to block")
        self.play(FadeIn(label("nothing to block",0,-.75,size=31)),run_time=.4)
        self.at("should look like")
        bx=[Line([x,cy-r-.02,0],[x,-1.55,0],color=TEAL,stroke_width=4) for x in xs]
        join=Line([xs[0],-1.55,0],[xs[1],-1.55,0],color=TEAL,stroke_width=4)
        stem=arr([0,-1.55,0],[0,-2.15,0],TEAL,4)
        self.play(*[Create(b) for b in bx],Create(join),GrowArrow(stem),run_time=.4)
        self.play(FadeIn(chip("Notch mutant: dMP2, dMP2",GREY,28).move_to([0,-2.65,0])),
                  FadeIn(label("same as",1.3,-1.9,TEAL,27)),run_time=.4)
        self.finish()


class S17Result(SpokenScene):
    def construct(self):
        g=grid(); g[0].become(label("Spana and Doe · 1996",0,3.25,size=30)); self.add(g)
        self.at("found two",lead=0)
        target=grid(result=True)[1][-1]
        self.remove(g[1][-1])
        self.play(FadeIn(target),Create(result_link()),g[1][2].animate.set_opacity(.3),run_time=.4)
        self.finish()


class S18Beat(Scene):
    def construct(self):
        self.camera.background_color=BG
        g=grid(result=True); g[0].become(label("Spana and Doe · 1996",0,3.25,size=30))
        g[1][2].set_opacity(.3)
        self.add(g,result_link(),verdict()); self.wait(2.5)


class S19Meaning(SpokenScene):
    def construct(self):
        self.add(label("Veto",0,3.15,size=38),
                 node("dMP2",-3.9,.4,1.35,size=30),node("dMP2",-.8,.4,1.35,size=30),
                 label("no Numb needed to make dMP2",-2.3,-1.6,size=28))
        panel=VGroup(node("",4,.4,1.55,numb=True),label("Numb",4,-.65,YELLOW,28))
        self.add(panel)
        self.at("only to stop")
        self.play(GrowArrow(arr([5.9,.8,0],[3.1,.8,0])),Create(signal_cross([4.2,.8,0])),
                  FadeIn(label("Notch",4,2.45,TEAL,27)),
                  FadeIn(label("Numb is needed only to stop Notch",0,-2.95,size=32)),run_time=.45)
        self.finish()


class S20Rule(SpokenScene):
    def construct(self):
        C=[-2.7,-.55,0]
        c=cell(C,2.2)
        top=Arc(radius=2.2,start_angle=PI/2-1,angle=2,arc_center=C,color=YELLOW,stroke_width=12)
        self.add(c,top,label("Numb",-2.7,-.9,YELLOW,28))
        card=RoundedRectangle(width=6,height=5.8,corner_radius=.25,color=GREY).move_to([3.3,0,0])
        self.add(card,label("The rule",3.3,2.4,size=34))
        self.at("the daughter that")
        f1=label("The daughter that\ninherits Numb",3.3,1.1,YELLOW,30)
        self.play(FadeIn(f1),run_time=.4)
        self.at("cannot hear notch")
        sig=arr([-2.7,3.0,0],[-2.7,1.8,0])
        f2=label("cannot hear Notch,",3.3,-.3,TEAL,30)
        self.play(GrowArrow(sig),Create(signal_cross([-2.7,2.4,0])),
                  FadeIn(label("Notch",-4.1,2.6,TEAL,27)),FadeIn(f2),run_time=.4)
        self.at("so it takes")
        f3=label("so it takes the Notch-off\nfate of that division.",3.3,-1.85,size=29)
        self.play(FadeIn(f3),f1.animate.set_color(TEXT),f2.animate.set_color(TEXT),run_time=.5)
        self.finish()


def off_trio():
    return VGroup(node("inner\nprecursor",-4.2,0,1.55,numb=True,size=28),
                  node("hair cell",0,0,1.55,numb=True,size=28),
                  node("dMP2",4.2,0,1.55,numb=True,size=30))


class S21Side(SpokenScene):
    def construct(self):
        self.add(label("Notch-off side",0,3,YELLOW,36))
        p=off_trio()
        self.add(*[VGroup(n[0],n[2]) for n in p],
                 *[label(t,x,-2.25,size=28) for t,x in zip(("division 1","division 2","CNS"),(-4.2,0,4.2))])
        self.at("not a fate")
        self.play(*[Indicate(n[2],color=YELLOW,scale_factor=1.03) for n in p],run_time=.5)
        for cue,i in (("the inner precursor",0),("the hair cell",1),("or dmp2",2)):
            self.at(cue)
            self.play(FadeIn(p[i][1]),run_time=.4)
        self.finish()


class S22Differentiate(SpokenScene):
    def construct(self):
        ytop,ybot,r=1.5,-1.3,1.2
        self.add(label("Sisters leave the stem-cell state",0,3.3,size=32),
                 label("Notch-off",-5.3,ytop,GREY,26),label("Notch on",-5.3,ybot,TEAL,26))
        xs=(-2.2,1.3,4.8)
        off=VGroup(*[node(t,x,ytop,r,numb=True,size=26) for t,x in zip(("inner\nprecursor","hair cell","dMP2"),xs)])
        self.add(off)
        partners=VGroup(*[node(t,x,ybot,r,on=True,size=26) for t,x in zip(("outer\nprecursor","socket cell","vMP2"),xs)])
        self.at("both sisters go")
        self.play(FadeIn(partners),run_time=.5)
        self.play(FadeIn(label("precursors divide once more",xs[0],-3.2,size=26)),run_time=.4)
        self.at("not the stem")
        self.play(FadeIn(label("none is a stem cell",3.0,-3.2,size=28)),run_time=.4)
        self.finish()


class S23Ptb(SpokenScene):
    def construct(self):
        protein=RoundedRectangle(width=11.4,height=2.15,corner_radius=.3,color=YELLOW,
                                  fill_color=YELLOW,fill_opacity=.12).move_to([0,.9,0])
        domain=RoundedRectangle(width=3.2,height=1.75,corner_radius=.18,color=YELLOW,
                                fill_color=YELLOW,fill_opacity=.45).move_to([-3.9,.9,0])
        self.add(protein,domain,label("PTB",-3.9,.9,YELLOW,40),label("Numb",1.4,.9,YELLOW,38))
        self.at("needs its")
        self.play(Indicate(domain,color=YELLOW,scale_factor=1.04),run_time=.35)
        self.at("binding domain")
        self.play(Create(Line([-3.9,.025,0],[-3.9,-.8,0],color=YELLOW,stroke_width=4)),
                  FadeIn(label("phosphotyrosine-binding (PTB) domain",-1.9,-1.15,size=29)),
                  FadeIn(chip("PTB reference · PDB 1DDM",GREY,26).move_to([0,2.85,0])),run_time=.35)
        self.at("to block notch")
        arrow=arr([-4,-2.55,0],[-1,-2.55,0])
        self.play(GrowArrow(arrow),Create(signal_cross([-2.5,-2.55,0])),
                  FadeIn(label("needed to block Notch",2.1,-2.55,TEAL,30)),run_time=.35)
        self.finish()


class S24Ptb2(SpokenScene):
    def construct(self):
        c=cell([-2.6,0,0],2.2); self.add(c)
        cres=crescent([-2.6,0,0],2.2)
        self.at("it does not need")
        self.play(FadeIn(label("Numb without PTB",2.5,2.5,YELLOW,30)),run_time=.4)
        self.at("to form its crescent")
        self.play(Create(cres),run_time=.6)
        self.at("reaching one side")
        self.play(FadeIn(label("Crescent still forms",2.5,.9,YELLOW,28)),run_time=.4)
        self.at("vetoing notch")
        receptor=RoundedRectangle(width=.26,height=1.25,corner_radius=.08,color=TEAL,
                                   fill_color=TEAL,fill_opacity=.6).move_to([-.35,.4,0])
        self.play(FadeIn(receptor),GrowArrow(arr([-.4,.4,0],[-1.7,.4,0])),
                  FadeIn(label("Notch stays on",2.5,-.5,TEAL,30)),run_time=.45)
        self.at("are separate jobs")
        self.play(FadeIn(label("Positioning ≠ vetoing",2.5,-2,size=28)),run_time=.4)
        self.finish()


class S25Takeaway(SpokenScene):
    def construct(self):
        c,s,n,x=veto(); signal_label=label("Notch",-2.7,2.95,TEAL,27)
        self.add(c,n,s,x,signal_label)
        self.at("is a veto")
        blocks=label("Numb blocks Notch",2.7,2,TEAL,33)
        self.play(FadeIn(blocks),run_time=.35)
        self.at("not an instruction")
        self.play(FadeIn(label("It does not name a fate",2.7,.9,size=30)),run_time=.35)
        self.at("without notch")
        self.play(FadeOut(s),FadeOut(x),FadeOut(signal_label),FadeOut(blocks),
                  FadeIn(absent_slot(-2.2,.65)),run_time=.35)
        self.at("there is nothing",lead=.9)
        self.play(FadeIn(label("no Notch:\nnothing to veto",2.7,-.4,size=32)),run_time=.35)
        self.finish()


class S26End(EndCard):
    LINE = "Numb is a veto, not an instruction."
