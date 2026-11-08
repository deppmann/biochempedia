"""Animal body plans: characters describe, genes test  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the blastopore (first opening of the embryonic gut)
  GREEN  = mouth
  RED    = anus, and a crossed-out prediction
  BLUE   = Spiralia (and the animals in it once regrouped)
  ORANGE = Ecdysozoa (nematodes and arthropods once regrouped)
  TEAL   = independent evidence (genes, chromosomes)
  GOLD   = the film's take-home rule
  GREY   = grades, bins, outlines, de-emphasized labels
"""
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bin_box(w, h, color=GREY):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.07)


def cross(mob, color=RED):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=6),
                  Line(mob.get_corner(UR), mob.get_corner(DL), color=color, stroke_width=6))


# Additional anatomy colors: PURPLE = mesoderm; TEXT = gut; GREY = body wall/tissue.
MESO = "#B695E0"


def heading(text):
    return T(text, 34, font=TITLE_FONT).move_to([0, 3.15, 0])


def tube(name, segmented=False):
    body = RoundedRectangle(width=4.7, height=0.85, corner_radius=0.4,
                            color=GREY, fill_color=GREY, fill_opacity=0.15)
    g = VGroup(body)
    if segmented:
        for x in np.linspace(-1.8, 1.8, 9):
            g.add(Line([x, -.39, 0], [x, .39, 0], color=GREY, stroke_width=2))
    g.add(T(name, 28).next_to(body, UP, buff=.3))
    return g


def section(kind):
    """Schematic transverse sections: lumen distinct from the body cavity."""
    wall = Circle(1.0, color=GREY, fill_color=MESO, fill_opacity=.75, stroke_width=5)
    if kind == 0:
        cavity = Circle(.72, stroke_width=0, fill_color=MESO, fill_opacity=.75)
    else:
        cavity = Circle(.72, color=MESO, stroke_width=10, fill_color=BG, fill_opacity=1)
    gutwall = Circle(.32, color=MESO if kind != 1 else TEXT,
                     stroke_width=10 if kind != 1 else 3, fill_color=BG, fill_opacity=1)
    lumen = Circle(.20, stroke_width=0, fill_color=TEXT, fill_opacity=.65)
    return VGroup(wall, cavity, gutwall, lumen)


BIN_X = [-4.3, 0, 4.3]


def build_bins():
    names = ["acoelomate", "pseudocoelomate", "coelomate"]
    boxes = [bin_box(4.05, 4.2).move_to([x, -.15, 0]) for x in BIN_X]
    labels = [T(n, 26, weight=BOLD).move_to([x, 1.48, 0]) for x,n in zip(BIN_X,names)]
    return boxes, labels


def tree_lines():
    # An unresolved schematic of two groups; no tip-to-tip sister claims.
    g = VGroup(Line([-5.9,0,0],[-4.8,0,0],color=GREY),
               Line([-4.8,-.2,0],[-4.8,.2,0],color=GREY))
    for y,c in [(.2,ORANGE),(-.2,BLUE)]:
        g.add(Line([-4.8,y,0],[-3.6,y,0],color=c))
    return g


class S00Title(TitleCard):
    LESSON = "Animal body plans"
    TITLE = "Similar Bodies, Different Branches"


class S01Lead(SpokenScene):
    def construct(self):
        h = heading("Similar bodies … same branch?")
        n = tube("nematode").move_to([-3.4,.5,0])
        e = tube("earthworm", True).move_to([3.4,.5,0])
        self.at("A nematode")
        self.play(FadeIn(h), FadeIn(n), FadeIn(e), run_time=.7)
        guts = VGroup()
        for x in [-3.4,3.4]:
            guts.add(arr([x-2.15,.22,0],[x+2.15,.22,0],TEXT,w=4))
        self.at("with a gut")
        self.play(*[GrowArrow(a) for a in guts],run_time=.6)
        ends = VGroup(T("mouth",22,GREEN).move_to([-5.4,-.65,0]),
                      T("anus",22,RED).move_to([-1.35,-.65,0]),
                      T("mouth",22,GREEN).move_to([1.35,-.65,0]),
                      T("anus",22,RED).move_to([5.4,-.65,0]))
        self.at("from mouth")
        self.play(FadeIn(ends),run_time=.5)
        lines=tree_lines()
        n2=bchip("nematode",ORANGE,26).move_to([-1.8,1.1,0])
        e2=bchip("earthworm",BLUE,26).move_to([-1.8,-1.1,0])
        self.at("Yet gene comparisons")
        self.play(FadeOut(guts),FadeOut(ends),Transform(n,n2),Transform(e,e2),
                  Transform(h,heading("Gene comparisons separate them")),Create(lines),run_time=1)
        insect=bchip("insect",ORANGE,26).move_to([2,1.1,0])
        self.at("groups with insects")
        self.play(Create(Line([-3.6,.2,0],n.get_bottom(),color=ORANGE)),
                  Create(Line([-3.6,.2,0],insect.get_bottom(),color=ORANGE)),FadeIn(insect),run_time=.6)
        snail=bchip("snail",BLUE,26).move_to([1.6,-1.1,0])
        flat=bchip("flatworm",BLUE,26).move_to([4.5,-1.1,0])
        self.at("groups with snails")
        self.play(*[Create(Line([-3.6,-.2,0],c.get_top(),color=BLUE)) for c in [e,snail,flat]],FadeIn(snail),FadeIn(flat),run_time=.7)
        self.at("On their own")
        self.play(FadeIn(T("Body shape alone does not establish ancestry",28,GOLD).move_to([0,-2.8,0])),run_time=.7)
        self.finish()


class S02Grades(SpokenScene):
    def construct(self):
        h=heading("Libbie Hyman: sort by body cavity")
        boxes,labels=build_bins()
        self.at("Libby Hyman's")
        self.play(FadeIn(h),run_time=.6)
        self.at("by body cavity")
        self.play(*[Create(b) for b in boxes],run_time=.6)
        diagrams=[]
        for i,(phrase,name) in enumerate([("like a planarian","planarian"),("like a nematode","nematode"),("like the earthworm","earthworm")]):
            d=VGroup(section(i).move_to([BIN_X[i],0,0]),T(name,25).move_to([BIN_X[i],-1.45,0]))
            diagrams.append(d)
            self.at(phrase)
            self.play(FadeIn(labels[i]),FadeIn(d),run_time=.6)
        legend=VGroup(T("purple: mesoderm",22,MESO),T("white center: gut lumen",22,TEXT)).arrange(RIGHT,buff=.7).move_to([0,-2.7,0])
        self.at("lined entirely")
        self.play(FadeIn(legend),Indicate(diagrams[2][0][2],color=MESO),run_time=.7)
        self.at("a shared level")
        self.play(Transform(h,heading("Grade: shared level of organization")),run_time=.6)
        self.at("A clade is different")
        self.play(FadeOut(VGroup(*boxes,*labels,*diagrams,legend)),Transform(h,heading("Clade: ancestor + all descendants")),run_time=.6)
        root=Dot([-3,0,0],color=GOLD)
        branches=VGroup(*[Line([-3,0,0],[1,y,0],color=GOLD) for y in [-1.5,0,1.5]])
        tips=VGroup(*[Dot([1,y,0],color=GOLD) for y in [-1.5,0,1.5]])
        bracket=RoundedRectangle(width=7,height=4.3,corner_radius=.3,color=GOLD).move_to([-1,0,0])
        self.at("an ancestor")
        self.play(FadeIn(root),run_time=.3)
        self.at("all of its descendants")
        self.play(Create(branches),FadeIn(tips),Create(bracket),run_time=.7)
        self.finish()


class S03Test(SpokenScene):
    def construct(self):
        h=heading("1997: compare the 18S rRNA gene")
        boxes,labels=build_bins()
        chips=[bchip("flatworm",GREY,26).move_to([-4.3,0,0]),bchip("nematode",GREY,26).move_to([0,0,0]),bchip("annelid",GREY,26).move_to([4.3,0,0])]
        self.at("In 1997")
        self.play(FadeIn(h),*[Create(b) for b in boxes],*[FadeIn(l) for l in labels],*[FadeIn(c) for c in chips],run_time=.8)
        n=bchip("nematode",ORANGE,26).move_to([-1.8,1.1,0])
        a=bchip("arthropod",ORANGE,26).move_to([1.6,1.1,0])
        lines=tree_lines()
        lines.add(*[Line([-3.6,.2,0],c.get_bottom(),color=ORANGE) for c in [n,a]])
        self.at("Nematodes grouped with arthropods")
        self.play(FadeOut(VGroup(*boxes)),
                  Transform(labels[0],T("acoelomate",22,GREY).move_to([-1.8,-1.75,0])),
                  Transform(labels[1],T("pseudocoelomate",22,GREY).move_to([-1.8,1.75,0])),
                  Transform(labels[2],T("coelomate",22,GREY).move_to([1.6,-1.75,0])),
                  Transform(chips[1],n),
                  chips[0].animate.move_to([-1.8,-1.1,0]),chips[2].animate.move_to([1.6,-1.1,0]),FadeIn(a),Create(lines),run_time=.9)
        eco=T("Ecdysozoa",28,ORANGE,weight=BOLD).move_to([0,2.25,0])
        molt=T("moult a cuticle",25,ORANGE).move_to([4.5,1.1,0])
        self.at("Both molticuticle")
        self.play(FadeIn(molt),run_time=.5)
        self.at("so the group is called")
        self.play(FadeIn(eco),run_time=.5)
        self.at("Later analyses")
        self.play(Transform(h,heading("Many genes broadly support the grouping")),run_time=.6)
        spi=T("Spiralia",28,BLUE,weight=BOLD).move_to([0,-2.4,0])
        m=bchip("mollusc",BLUE,26).move_to([4.7,-1.1,0])
        self.at("They put flatworms inside")
        self.play(FadeIn(spi),Create(Line([-3.6,-.2,0],chips[0].get_top(),color=BLUE)),chips[0][1].animate.set_stroke(BLUE),chips[0][2].animate.set_color(BLUE),run_time=.5)
        self.at("with annelids and mollusks")
        self.play(FadeIn(m),*[Create(Line([-3.6,-.2,0],c.get_top(),color=BLUE)) for c in [chips[2],m]],chips[2][1].animate.set_stroke(BLUE),chips[2][2].animate.set_color(BLUE),run_time=.5)
        cavity=T("coelomate",22,GREY).move_to([4.7,-1.75,0])
        self.at("among relatives")
        self.play(FadeOut(molt),FadeIn(cavity),run_time=.6)
        self.at("So body cavity")
        self.play(FadeIn(T("Body cavity: a grade, not a clade",30,GOLD).move_to([0,-3.1,0])),run_time=.6)
        self.finish()


class S04Characters(SpokenScene):
    def construct(self):
        h=heading("Characters describe an animal")
        names=["symmetry","germ layers","body cavity","gut"]
        nav=VGroup(*[bchip(n,GREY,24).move_to([x,2.2,0]) for x,n in zip([-4.8,-1.6,1.6,4.8],names)])
        self.at("These characters")
        self.play(FadeIn(h),FadeIn(nav),run_time=.6)
        sponge=Polygon([-5,-.9,0],[-4.9,1,0],[-4.3,.6,0],[-3.8,1,0],[-3.3,-.7,0],color=GREY,fill_opacity=.2)
        radial=VGroup(Circle(.8,color=GREY),*[Line(ORIGIN,[.8*np.cos(t),.8*np.sin(t),0],color=GREY) for t in np.linspace(0,TAU,7)[:-1]]).move_to([0,0,0])
        bilateral=VGroup(Ellipse(width=1.5,height=2,color=GREY),DashedLine([0,-1,0],[0,1,0],color=TEXT)).move_to([4.2,0,0])
        sym=VGroup(sponge,radial,bilateral,*[T(n,24).move_to([x,-1.7,0]) for x,n in [(-4.2,"none: sponge"),(0,"radial"),(4.2,"bilateral")]])
        self.at("Symmetry")
        self.play(Indicate(nav[0],color=GOLD),FadeIn(sym),run_time=.6)
        two=VGroup(*[Rectangle(width=3,height=.35,color=c,fill_color=c,fill_opacity=.6).move_to([-3,y,0]) for y,c in [(.4,GREY),(-.4,TEXT)]],T("two layers",26).move_to([-3,-1.3,0]))
        three=VGroup(*[Rectangle(width=3,height=.35,color=c,fill_color=c,fill_opacity=.6).move_to([3,y,0]) for y,c in [(.65,GREY),(0,MESO),(-.65,TEXT)]],T("three layers",26).move_to([3,-1.3,0]))
        self.at("Germ layers")
        self.play(FadeOut(sym),Indicate(nav[1],color=GOLD),FadeIn(two),FadeIn(three),run_time=.6)
        ml=T("mesoderm",26,MESO).move_to([3,-2.1,0])
        self.at("middle layer")
        self.play(FadeIn(ml),Indicate(three[1],color=MESO),run_time=.5)
        cavities=VGroup(section(2).move_to([-3,0,0]),section(0).move_to([3,0,0]),T("cavity",26).move_to([-3,-1.6,0]),T("no body cavity",26).move_to([3,-1.6,0]))
        self.at("A body cavity")
        self.play(FadeOut(VGroup(two,three,ml)),FadeIn(cavities),Indicate(nav[2],color=GOLD),run_time=.6)
        plan=VGroup(Ellipse(width=6,height=2.2,color=GREY,fill_color=MESO,fill_opacity=.5),
                    Line([0,-1.1,0],[0,0,0],color=TEXT,stroke_width=12),
                    *[Line([0,0,0],[x,.65,0],color=TEXT,stroke_width=10) for x in [-1.7,0,1.7]])
        label=T("planarian: gut present, body cavity absent",28).move_to([0,-2.1,0])
        self.at("keep the gut apart")
        self.play(FadeOut(cavities),FadeIn(plan),FadeIn(label),Indicate(nav[3],color=GOLD),run_time=.6)
        self.at("Even a planarian")
        self.play(Indicate(VGroup(*plan[1:]),color=TEXT,scale_factor=1.08),run_time=.6)
        self.finish()


class S05Function(SpokenScene):
    def construct(self):
        h=heading("Body plans shape how an animal lives")
        worm=tube("earthworm",True).scale(2).move_to([0,.2,0])
        self.at("These characters")
        self.play(FadeIn(h),FadeIn(worm),run_time=.6)
        gut=arr([-4.4,-.1,0],[4.4,-.1,0],TEXT,w=10)
        food=Dot([-4.2,-.1,0],color=TEXT,radius=.12)
        self.at("moves food one way")
        self.play(GrowArrow(gut),FadeIn(food),run_time=.4)
        self.play(food.animate.move_to([4.1,-.1,0]),run_time=1.4)
        regions=VGroup(bchip("gizzard",TEXT,26).move_to([-2,-1.7,0]),bchip("intestine",TEXT,26).move_to([2.5,-1.7,0]))
        self.at("grinding gizzard")
        self.play(FadeIn(regions[0]),run_time=.4)
        self.at("long intestine")
        self.play(FadeIn(regions[1]),run_time=.4)
        self.at("A sealed")
        self.play(FadeOut(VGroup(worm,gut,food,regions)),Transform(h,heading("A sealed segment: hydrostatic skeleton")),run_time=.6)
        def cylinder(length,radius,x=0):
            body=Rectangle(width=length,height=2*radius,color=GREY,fill_color=GREY,fill_opacity=.22)
            ends=VGroup(*[Ellipse(width=.3,height=2*radius,color=GREY,fill_color=BG,fill_opacity=.5).move_to([v,0,0]) for v in [-length/2,length/2]])
            return VGroup(body,ends).move_to([x,0,0])
        seg=cylinder(2.8,1)
        self.play(FadeIn(seg),run_time=.5)
        const=T("constant fluid volume",28,GREY).move_to([0,-2,0])
        squeeze=VGroup(arr([0,1.8,0],[0,1.05,0],GREY),arr([0,-1.8,0],[0,-1.05,0],GREY))
        self.at("Squeeze it narrower")
        self.play(FadeIn(squeeze),run_time=.4)
        self.at("at constant volume")
        # V = pi*r²*L, so L grows as inverse radius squared.
        self.play(UpdateFromAlphaFunc(seg, lambda m,a: m.become(cylinder(2.8/(1-.25*a)**2,1-.25*a))),
                  FadeOut(squeeze),FadeIn(const),run_time=1.2)
        self.at("Waves of this")
        self.play(FadeOut(seg),FadeOut(const),run_time=.25)
        parts=VGroup(*[cylinder(1.25,.7,x) for x in [-3.8,-1.9,0,1.9,3.8]])
        soil=Line([-5,-1,0],[5.8,-1,0],color=GREY)
        anchors=VGroup(*[Line([x,-.65,0],[x-.2,-1,0],color=GREY) for x in [-3.8,-1.9,1.9,3.8]])
        self.play(FadeIn(parts),Create(soil),Create(anchors),run_time=.3)
        for i in [1,2,3]:
            dest=parts[i].get_center()
            anchor = anchors[1] if i == 1 else anchors[2] if i == 3 else None
            if anchor is not None:
                self.remove(anchor)
            self.play(UpdateFromAlphaFunc(parts[i], lambda m,a: m.become(cylinder(1.25/(1-.2*a)**2,.7*(1-.2*a)).move_to(dest))),run_time=.25)
            self.play(UpdateFromAlphaFunc(parts[i], lambda m,a: m.become(cylinder(1.25/(.8+.2*a)**2,.7*(.8+.2*a)).move_to(dest))),run_time=.25)
            if anchor is not None:
                self.add(anchor)
        self.play(parts.animate.shift(RIGHT*.7),anchors.animate.shift(RIGHT*.7),run_time=.5)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        h=heading("Test developmental rules, too")
        self.at("Old developmental rules")
        self.play(FadeIn(h),run_time=.6)
        sn=bchip("slipper snail embryo",TEAL,30).move_to([0,1.6,0])
        bl=bchip("blastopore",YELLOW,28).move_to([-2.5,0,0])
        mouth=bchip("mouth",GREEN,28).move_to([2.5,0,0])
        self.at("In a slipper snail")
        self.play(FadeIn(sn),run_time=.6)
        self.at("the blastopore becomes")
        self.play(FadeIn(bl),GrowArrow(arr(bl.get_right(),mouth.get_left(),YELLOW)),FadeIn(mouth),run_time=.7)
        caution=bchip("Fate varies among relatives",RED,28).move_to([0,-1.7,0])
        self.at("But blastopore fate varies")
        self.play(FadeIn(caution),run_time=.6)
        self.at("not a reliable test")
        self.play(Indicate(caution,color=RED),run_time=.6)
        self.at("To test a grouping")
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not h])),Transform(h,heading("Independent evidence tests ancestry")),run_time=.6)
        gene=bchip("many genes",TEAL,28).move_to([-3.6,1.2,0])
        chrom=bchip("genes sharing\nchromosomes",TEAL,28).move_to([-3.6,-1.1,0])
        tree=VGroup(Line([1,0,0],[2,0,0],color=GOLD),Line([2,-1.5,0],[2,1.5,0],color=GOLD),*[Line([2,y,0],[4.4,y,0],color=GOLD) for y in [-1.5,0,1.5]],*[Dot([4.4,y,0],color=GOLD) for y in [-1.5,0,1.5]])
        self.at("sample many genes")
        self.play(FadeIn(gene),Create(tree),GrowArrow(arr(gene.get_right(),[1,0,0],TEAL)),run_time=.7)
        self.at("which genes share chromosomes")
        self.play(FadeIn(chrom),GrowArrow(arr(chrom.get_right(),[1,0,0],TEAL)),run_time=.7)
        rule=T("Body-plan characters describe animals.",30,TEXT,font=TITLE_FONT).move_to([0,-2.5,0])
        rule2=T("Independent evidence tests their ancestry.",30,GOLD,font=TITLE_FONT).move_to([0,-3.2,0])
        self.at("Body plan characters")
        self.play(FadeIn(rule),run_time=.6)
        self.at("Independent evidence tests")
        self.play(FadeIn(rule2),run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "Body-plan characters describe animals;\nindependent evidence tests their ancestry."
