"""Human evolutionary history: African origins and encounters  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the sampled African genome / P1 (and the African populations)
  YELLOW = the sampled Eurasian genome / P2 (and the ancestors of Eurasians)
  ORANGE = Neanderthal, Neanderthal-like segments, gene flow
  PURPLE = old population structure (the alternative history)
  GREEN  = D (the statistic) and the "clue" it gives
  TEAL   = time, recombination, segment length (the test)
  RED    = "no" (a crossed-out reading)
  PINK   = Denisovan ancestry
  GREY   = ancestral alleles, chromosomes, fossils, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E78AC3"
SAFE_L, SAFE_R = -6.3, 6.3


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def site(derived, col, letter=None, size=0.5):
    """one site of a genome: filled = derived allele (B), hollow = ancestral allele (A)."""
    s = Square(size, stroke_color=col if derived else GREY, stroke_width=3,
               fill_color=col, fill_opacity=0.85 if derived else 0)
    g = VGroup(s)
    if letter:
        g.add(T(letter, 22, BG if derived else GREY, weight=BOLD).move_to(s))
    return g


def genome_row(y, derived, col, name, name_col, n=12, x0=-3.0, dx=0.78):
    sqs = VGroup(*[site(i in derived, col).move_to([x0 + i * dx, y, 0]) for i in range(n)])
    lab = T(name, 26, name_col)
    lab.move_to([x0 - 0.55 - lab.width / 2, y, 0])
    return VGroup(sqs, lab)


def card(pattern, title):
    """a four-row ABBA / BABA pattern card: African, Eurasian, Neanderthal, chimpanzee."""
    taxa = [("African", BLUE), ("Eurasian", YELLOW), ("Neanderthal", ORANGE), ("Chimpanzee", GREY)]
    rows = VGroup()
    for (name, col), a in zip(taxa, pattern):
        lab = T(name, 22, col)
        sq = site(a == "B", col, a)
        lab.next_to(sq, LEFT, buff=0.2)
        rows.add(VGroup(lab, sq))
    for i, r in enumerate(rows):                       # align the squares in one column
        r.shift(RIGHT * (rows[0][1].get_center()[0] - r[1].get_center()[0]))
    rows.arrange(DOWN, buff=0.14, aligned_edge=RIGHT)
    t = T(title, 28, TEXT, weight=BOLD).next_to(rows, UP, buff=0.22)
    return VGroup(t, rows)


def bars(h1, h2, base, x1, x2, n1=None, n2=None, w=1.3):
    b1 = Rectangle(width=w, height=h1, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.7)
    b2 = Rectangle(width=w, height=h2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.7)
    b1.move_to([x1, base + h1 / 2, 0]); b2.move_to([x2, base + h2 / 2, 0])
    g = VGroup(b1, b2)
    if n1:
        g.add(M(n1, 30, YELLOW).next_to(b1, UP, buff=0.12), M(n2, 30, BLUE).next_to(b2, UP, buff=0.12))
    return g


def dscale(x0, x1, y, val=None):
    """the D scale from -1 to +1; returns group and a function giving the x for a value."""
    xs = lambda v: x0 + (v + 1) / 2 * (x1 - x0)
    line = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=4)
    ticks = VGroup(*[Line([xs(v), y - 0.12, 0], [xs(v), y + 0.12, 0], color=GREY, stroke_width=3) for v in (-1, 0, 1)])
    labs = VGroup(M("-1", 22, GREY).move_to([xs(-1), y - 0.42, 0]), M("0", 22, GREY).move_to([xs(0), y - 0.42, 0]),
                  M("+1", 22, GREY).move_to([xs(1), y - 0.42, 0]))
    return VGroup(line, ticks, labs), xs


def marker(x, y):
    tri = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1, stroke_width=0).scale(0.2).rotate(PI)
    tri.move_to([x, y + 0.3, 0])
    return tri


def chrom(y, x0=-5.3, x1=5.3, h=0.7):
    return RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.25).move_to([(x0 + x1) / 2, y, 0])


def blocks(y, spans, h=0.7):
    return VGroup(*[Rectangle(width=b - a, height=h - 0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95)
                    .move_to([(a + b) / 2, y, 0]) for a, b in spans])


def blob(label, col, pos, r=0.5, below=True, size=24):
    c = Circle(radius=r, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.3).move_to(pos)
    t = T(label, size, col)
    t.next_to(c, DOWN if below else UP, buff=0.15)
    return VGroup(c, t)


# New helpers extend the old schematic drawing vocabulary.
def heading(text, col=TEXT):
    return T(text, 32, col, font=TITLE_FONT).move_to([0, 3.2, 0])


def thread(points, col=BLUE):
    return VMobject(stroke_color=col, stroke_width=5).set_points_smoothly(
        [np.array([x, y, 0]) for x, y in points])


def africa():
    # Deliberately schematic coast: geography locates evidence, not inferred routes.
    pts = [(-2.7,2.4),(-1.1,2.8),(0.4,2.3),(1.2,1.3),(2.0,0.9),
           (1.1,0.3),(0.9,-1.0),(-0.3,-2.6),(-0.9,-1.6),(-1.4,0.0),
           (-2.6,0.3),(-3.2,1.3)]
    return Polygon(*[[x,y,0] for x,y in pts], stroke_color=GREY,
                   fill_color=GREY, fill_opacity=0.1, stroke_width=3)


def world():
    outlines = [
        [(-6,1.8),(-5,2.4),(-3.5,2),(-3.3,1),(-4.3,.2),(-5,.6)],
        [(-4.1,.1),(-2.9,-.5),(-3.1,-1.7),(-3.7,-2.7),(-4,-1.1)],
        [(-1.4,1.1),(-.2,1.4),(.7,.4),(.1,-1.6),(-.5,-2),(-1.2,-.4)],
        [(-1.1,1.5),(-.4,2.3),(1.3,2.5),(3,2.1),(5.6,1.6),(4.7,.6),
         (3.1,.3),(2.6,-.4),(1.6,.8),(.2,1.1)],
        [(3.8,-1.5),(5,-1.1),(5.8,-1.8),(4.8,-2.3),(3.9,-2.1)]]
    return VGroup(*[Polygon(*[[x,y,0] for x,y in ps], stroke_color=GREY,
                           stroke_width=2, fill_color=GREY, fill_opacity=.12) for ps in outlines])


def skull(pos, elongated=True, scale=1):
    # Schematic lateral skull; no reconstructed anatomical detail is implied.
    vault = Ellipse(width=2.2 if elongated else 1.65, height=1.25,
                    color=GREY, fill_color=GREY, fill_opacity=.12)
    face = VMobject(color=GREY, stroke_width=4).set_points_as_corners(
        [[.65,.35,0],[1.02,.05,0],[.86,-.12,0],[.92,-.5,0],[.3,-.65,0]])
    jaw = Line([.3,-.65,0],[-.25,-.35,0],color=GREY,stroke_width=4)
    return VGroup(vault, face, jaw).scale(scale).move_to(pos)


def person(pos, col=TEXT):
    head = Circle(radius=.14, color=col, fill_opacity=.8)
    body = Line([0,-.2,0],[0,-.7,0],color=col,stroke_width=5)
    limbs = VGroup(Line([-.23,-.4,0],[.23,-.4,0],color=col,stroke_width=4),
                   Line([0,-.7,0],[-.2,-1,0],color=col,stroke_width=4),
                   Line([0,-.7,0],[.2,-1,0],color=col,stroke_width=4))
    return VGroup(head, body, limbs).move_to(pos)


def ancestry_bar(y, spans, x0=-5.3, x1=5.3, h=.7):
    return VGroup(chrom(y,x0,x1,h),blocks(y,spans,h))


class S00Title(TitleCard):
    LESSON = "Human evolutionary history"
    TITLE = "Our African Origin and the Humans We Met"

    def construct(self):
        brand=T("BIOCHEMISTRYPEDIA",22,TEAL,weight=BOLD)
        lesson=T(self.LESSON.upper(),22,GREY)
        title=fit(T(self.TITLE,54,font=TITLE_FONT),max_w=11.5)
        rule=Line(LEFT*1.2,RIGHT*1.2,color=GOLD,stroke_width=4)
        group=VGroup(brand,lesson,title,rule).arrange(DOWN,buff=.32)
        self.play(FadeIn(brand),FadeIn(lesson),run_time=self.beat(.25))
        self.play(Write(title),GrowFromCenter(rule),run_time=self.beat(.35))
        self.wait(self.beat(.2))
        self.play(FadeOut(group),run_time=self.beat(.2))
        self.finish()


class S01Origin(SpokenScene):
    def construct(self):
        coast = africa().shift(LEFT*1.3)
        title = heading("Homo sapiens · Africa",BLUE)
        self.at("Our species")
        self.play(Create(coast),FadeIn(title),run_time=.8)
        self.at("Not in one place")
        north = Dot([-3.1,2,0],color=BLUE,radius=.12)
        east = Dot([-.7,.1,0],color=BLUE,radius=.12)
        self.play(FadeIn(north,scale=2),FadeIn(east,scale=2),run_time=.5)
        self.at("north Africa")
        nl = T("Jebel Irhoud\nabout 300,000 years",22,BLUE).move_to([-4.9,2.95,0])
        self.play(Flash(north,color=BLUE),FadeIn(nl),run_time=.6)
        self.at("east Africa")
        el = T("Omo\nat least 233,000 years",24,BLUE).move_to([2,0,0])
        self.play(Flash(east,color=BLUE),FadeIn(el),run_time=.6)
        self.at("populations that split")
        paths = VGroup(thread([(-3.1,2),(-2.7,1),(-1.8,1),(-.7,.1)]),
                       thread([(-3.1,2),(-1.6,1.7),(-1.4,.5),(-.7,.1)]))
        self.play(Create(paths),run_time=1)
        self.at("merged again")
        self.play(Indicate(east,color=BLUE),run_time=.6)
        self.at("Later some")
        self.play(FadeOut(VGroup(nl,el,paths,north,east)),
                  ReplacementTransform(coast,world()),
                  ReplacementTransform(title,heading("Descendants spread and met other humans")),run_time=.7)
        route = thread([(-.5,.3),(.4,1.6),(2,1.4),(4,1)],YELLOW)
        self.at("spread across the world")
        self.play(Create(route),run_time=1)
        self.at("met Neanderthals")
        ne = thread([(1.4,2.3),(2,1.4),(2.7,1.6),(3.3,1.2)],ORANGE)
        de = thread([(3.9,2.1),(3.3,1.2),(3.7,1.4),(4,1)],PINK)
        labs=VGroup(T("Neanderthal",24,ORANGE).move_to([.8,2.7,0]),
                    T("Denisovan",24,PINK).move_to([4.3,2.7,0]))
        self.play(Create(ne),Create(de),FadeIn(labs),run_time=.8)
        self.at("had children")
        braid=VGroup(thread([(2.6,1.3),(3,.9),(3.5,1.3),(4,.9)],ORANGE),
                     thread([(2.6,1.1),(3,1.4),(3.5,1),(4,1.2)],PINK))
        self.play(Create(braid),run_time=.7)
        self.at("Pieces of that")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        bar=ancestry_bar(0,[(-3,-2.6),(1,1.35)])
        pink=blocks(0,[(3,3.35)]).set_color(PINK)
        self.play(FadeIn(bar),FadeIn(pink),FadeIn(heading("Inherited pieces · people today")),run_time=.7)
        self.finish()


class S02Fossils(SpokenScene):
    def construct(self):
        title=heading("Fossil dates need care")
        left=T("Jebel Irhoud · Morocco",26,BLUE).move_to([-3.3,2.3,0])
        bone=skull([-3.5,.8,0])
        flints=VGroup(*[Polygon([x,-.9,0],[x+.4,-.8,0],[x+.15,-.45,0],
                               color=GOLD,fill_opacity=.4) for x in [-4.7,-4,-3.3]])
        flabel=T("heated flints · dated",24,GOLD).move_to([-3.6,-1.5,0])
        self.at("Fossil dates")
        self.play(FadeIn(title),run_time=.5)
        self.at("in Morocco")
        self.play(FadeIn(left),Create(bone),run_time=.6)
        self.at("flints heated by fire")
        self.play(FadeIn(flints),FadeIn(flabel),run_time=.6)
        self.at("face looks like ours")
        face_label=T("modern-looking face",22,BLUE).move_to([-3.4,-2.2,0])
        self.play(bone[1].animate.set_color(BLUE),FadeIn(face_label),run_time=.5)
        self.at("brain case is more elongated")
        vault_label=T("elongated braincase",22,TEAL).move_to([-3.4,-2.8,0])
        self.play(bone[0].animate.set_stroke(TEAL,5),FadeIn(vault_label),run_time=.6)
        self.at("At Omo")
        right=T("Omo · Ethiopia",26,BLUE).move_to([3.1,2.3,0])
        strata=VGroup(*[Rectangle(width=5,height=.8,stroke_color=GREY,stroke_width=1,
                                  fill_color=GREY,fill_opacity=.1+.04*i).move_to([3,y,0])
                        for i,y in enumerate([1.15,.35,-.45,-1.25])])
        fossil=skull([2.8,-.5,0],False,.48)
        self.play(FadeIn(right),FadeIn(strata),FadeIn(fossil),run_time=.7)
        self.at("dated ash lies above")
        ash=Rectangle(width=5,height=.16,fill_color=TEXT,fill_opacity=.9,stroke_width=0).move_to([3,.8,0])
        ashlabel=T("dated ash",24,TEXT).move_to([3,1.65,0])
        self.play(FadeIn(ash),FadeIn(ashlabel),run_time=.5)
        self.at("fossil is at least")
        arrow=Arrow([5.15,.7,0],[5.15,-.65,0],buff=0,color=TEAL)
        bound=T("at least that old",24,TEAL).move_to([3,-2.2,0])
        self.play(GrowArrow(arrow),FadeIn(bound),run_time=.6)
        self.at("Ask what was dated")
        self.play(ReplacementTransform(title,heading("What was dated? Where did it lie?")),run_time=.6)
        self.finish()


class S03Clue(SpokenScene):
    def construct(self):
        self.at("How do we know")
        title=heading("How do we know about the meetings?")
        self.play(FadeIn(title),run_time=.6)
        af=genome_row(1.8,{0,5},BLUE,"Sampled African",BLUE,n=8,x0=-1.8,dx=.9)
        eu=genome_row(.6,{1,2,4,6},YELLOW,"Sampled Eurasian",YELLOW,n=8,x0=-1.8,dx=.9)
        ne=genome_row(-.6,{0,1,2,4,6},ORANGE,"Neanderthal",ORANGE,n=8,x0=-1.8,dx=.9)
        self.at("Sampled genomes")
        self.play(FadeIn(af),FadeIn(eu),FadeIn(ne),run_time=.7)
        matches=VGroup(*[Line([-1.8+i*.9,.3,0],[-1.8+i*.9,-.3,0],color=YELLOW,stroke_width=5) for i in [1,2,4,6]])
        self.at("share more variants")
        self.play(LaggedStart(*[Create(m) for m in matches],lag_ratio=.15),run_time=1)
        scale,xs=dscale(-3,3,-2.2)
        pointer=marker(xs(0),-2.2)
        dl=T("D",30,GREEN).move_to([-4,-2.2,0])
        self.at("A test called")
        self.play(FadeIn(scale),FadeIn(pointer),FadeIn(dl),run_time=.6)
        self.at("that surplus")
        self.play(pointer.animate.move_to([xs(.45),-1.9,0]),run_time=.6)
        self.at("not a percentage")
        note=T("not % ancestry",26,RED).move_to([0,-3.1,0])
        self.play(FadeIn(note),run_time=.5)
        self.at("On its own")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        clue=chip("D: a clue, not proof",GREEN,30).move_to([0,2.6,0])
        self.play(FadeIn(clue),run_time=.6)
        self.at("old structure inside Africa")
        panel=RoundedRectangle(width=7,height=2.5,color=PURPLE,fill_opacity=.06).move_to([-1,0,0])
        cells=VGroup(*[Circle(radius=.52,color=BLUE,fill_opacity=.16).move_to([x,0,0]) for x in [-3,-1,1]])
        label=T("subdivided ancestral population",24,PURPLE).move_to([-1,1.6,0])
        question=T("?",50,PURPLE).move_to([3,0,0])
        self.play(Create(panel),FadeIn(cells),FadeIn(label),FadeIn(question),run_time=.7)
        self.at("Stronger evidence")
        self.play(FadeOut(VGroup(panel,cells,label,question)),run_time=.4)
        clock=VGroup(Circle(radius=1.1,color=TEAL),Line(ORIGIN,[0,.75,0],color=TEAL),Line(ORIGIN,[.6,-.2,0],color=TEAL))
        ar=Arrow([-3,0,0],[-1.5,0,0],color=TEAL)
        time=T("Time tests the clue",30,TEAL).move_to([0,-2,0])
        self.play(GrowArrow(ar),Create(clock),FadeIn(time),run_time=.7)
        self.finish()


class S04Segments(SpokenScene):
    def construct(self):
        title=heading("Recombination shortens inherited pieces",TEAL)
        bar=ancestry_bar(.8,[(-4,4)])
        self.at("Every generation")
        self.play(FadeIn(title),FadeIn(bar),run_time=.6)
        ticks=VGroup(*[Line([x,.25,0],[x,1.35,0],color=TEAL,stroke_width=3) for x in [-2,0,2]])
        self.at("recombination cuts")
        self.play(Create(ticks),run_time=.7)
        shorter=blocks(.8,[(-4,-2.2),(-1.9,-.2),(.1,1.8),(2.1,4)])
        self.at("into shorter pieces")
        self.play(ReplacementTransform(bar[1],shorter),run_time=.7)
        self.at("Ust Ishim")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        lab=heading("Ust'-Ishim · western Siberia",TEAL)
        date=T("about 45,000 years ago",26,TEAL).move_to([0,2.5,0])
        self.play(FadeIn(lab),FadeIn(date),run_time=.6)
        old=ancestry_bar(1,[(-4.8,-2.4),(.4,2.8)])
        now=ancestry_bar(-.4,[(x,x+.6) for x in [-4.9,-3.6,-2.3,-1,.3,1.6,2.9,4.2]])
        labels=VGroup(T("Ust'-Ishim",24,TEAL).move_to([0,1.7,0]),T("present day",24,GREY).move_to([0,-1.1,0]))
        self.at("His Neanderthal segments")
        self.play(FadeIn(old),FadeIn(now),FadeIn(labels),run_time=.7)
        self.at("longer than ours")
        self.play(Indicate(old[1],color=ORANGE),run_time=.6)
        self.at("From their length")
        axis=Line([-5.4,-2.2,0],[5.4,-2.2,0],color=GREY)
        ust=Dot([-1,-2.2,0],color=TEAL)
        schematic=T("schematic · segment lengths only",22,GREY).move_to([0,-1.55,0])
        self.play(FadeIn(schematic),run_time=.25)
        present=T("present",22,GREY).move_to([5,-2.65,0])
        bracket=VGroup(Line([-2.85,-1.9,0],[-2,-1.9,0],color=ORANGE,stroke_width=7),
                       Line([-2.85,-2.05,0],[-2.85,-1.75,0],color=ORANGE),
                       Line([-2,-2.05,0],[-2,-1.75,0],color=ORANGE),
                       DashedLine([-2,-1.9,0],[-1,-1.9,0],color=ORANGE))
        infer=T("inferred gene flow · 7,000–13,000 years before him",24,ORANGE).move_to([-.5,-3.2,0])
        ulabel=T("45,000",22,TEAL).move_to([-1,-2.65,0])
        self.play(Create(axis),FadeIn(ust),FadeIn(present),FadeIn(ulabel),run_time=.6)
        self.at("inferred gene flow")
        self.play(Create(bracket),FadeIn(infer),run_time=.7)
        self.at("Cave in Bulgaria")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        title=heading("Bacho Kiro Cave · Bulgaria",TEAL)
        people=VGroup(*[person([x,1.2,0]) for x in [-3,0,3]])
        bars3=VGroup(*[ancestry_bar(-.3,[(-1.2,1.2)],x0=-1.4,x1=1.4,h=.45).shift(RIGHT*x) for x in [-3,0,3]])
        self.play(FadeIn(title),FadeIn(people),FadeIn(bars3),run_time=.6)
        self.at("only a few generations")
        self.play(FadeIn(T("Neanderthal ancestors · a few generations back",28,ORANGE).move_to([0,-2,0])),run_time=.6)
        self.finish()


class S05Hybrid(SpokenScene):
    def construct(self):
        title=heading("Denisova Cave · Siberia",PINK)
        cave=VMobject(color=GREY,fill_color=GREY,fill_opacity=.15).set_points_as_corners(
            [[-4,-1,0],[-3.7,1,0],[-2.6,2,0],[-1.3,1.1,0],[-1,-1,0],[-1.8,-1,0],[-2,0,0],[-2.8,.4,0],[-3.2,-1,0],[-4,-1,0]])
        fragment=RoundedRectangle(width=.45,height=1.1,corner_radius=.17,color=TEXT,fill_opacity=.25).rotate(-.4).move_to([2,0,0])
        flabel=T("finger bone · DNA",26,PINK).move_to([2,-1.4,0])
        self.at("Denisovans are known")
        self.play(FadeIn(title),Create(cave),run_time=.7)
        self.at("a finger bone")
        self.play(FadeIn(fragment),FadeIn(flabel),run_time=.6)
        self.at("Another fragment")
        other=Polygon([1.7,-.3,0],[2.2,-.2,0],[2.4,.4,0],[1.8,.5,0],color=TEXT,fill_opacity=.25)
        self.play(ReplacementTransform(fragment,other),FadeOut(flabel),run_time=.5)
        self.at("Denisova 11")
        name=T("Denisova 11",30,TEXT).move_to([2,-1.4,0])
        self.play(FadeIn(name),run_time=.5)
        self.at("came from a child")
        self.play(FadeOut(VGroup(cave,other,name)),run_time=.4)
        child=person([0,-.2,0])
        childlabel=T("Denisova 11",26,TEXT).move_to([0,-1.15,0])
        self.play(FadeIn(child),FadeIn(childlabel),run_time=.5)
        self.at("Neanderthal mother")
        mother=blob("Neanderthal mother",ORANGE,[-3.6,1.6,0],r=.35,below=False)
        ma=Arrow([-3.3,1.2,0],[-.4,.35,0],color=ORANGE,buff=.15)
        self.play(FadeIn(mother),GrowArrow(ma),run_time=.5)
        self.at("Denisovan father")
        father=blob("Denisovan father",PINK,[3.6,1.6,0],r=.35,below=False)
        pa=Arrow([3.3,1.2,0],[.4,.35,0],color=PINK,buff=.15)
        self.play(FadeIn(father),GrowArrow(pa),run_time=.5)
        self.at("At sites where")
        paired=VGroup(*[VGroup(site(True,ORANGE,size=.42).move_to([x,-2,0]),
                                     site(True,PINK,size=.42).move_to([x,-2.6,0]))
                       for x in np.linspace(-2.8,2.8,8)])
        self.play(FadeIn(paired),run_time=.6)
        self.at("one version of each")
        self.play(Indicate(paired,color=TEXT,scale_factor=1.06),run_time=.6)
        self.at("Archaic groups mixed")
        self.play(ReplacementTransform(title,heading("Archaic groups mixed with each other, too")),run_time=.6)
        self.finish()


class S06Legacy(SpokenScene):
    def construct(self):
        m=world()
        title=heading("Inherited DNA still matters")
        self.at("Some of that")
        self.play(FadeIn(title),Create(m),run_time=.7)
        mel=Dot([5.4,-.9,0],color=PINK,radius=.12)
        label=T("sampled Melanesians",24,PINK).move_to([3.8,-2.8,0])
        share=VGroup(Rectangle(width=4,height=.35,color=GREY,fill_opacity=.2),
                     Rectangle(width=.2,height=.35,color=PINK,fill_opacity=1).shift(LEFT*1.9)).move_to([2.8,-2.1,0])
        pct=T("inferred 4–6% Denisovan ancestry",24,PINK).move_to([2.8,-3.3,0])
        self.at("sampled Melanesians")
        self.play(FadeIn(mel),FadeIn(label),FadeIn(share),run_time=.6)
        self.at("Denisovan ancestry")
        self.play(FadeIn(pct),run_time=.5)
        self.at("In Tibetans")
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)],run_time=.4)
        plateau=Polygon([-6,-1.4,0],[-5,-.7,0],[-4,1,0],[-2,1,0],[-1,-.4,0],[0,-1.4,0],
                        stroke_color=GREY,fill_color=GREY,fill_opacity=.12)
        title=heading("Tibetans · high altitude")
        self.play(Create(plateau),FadeIn(title),run_time=.6)
        self.at("a version of EPAS1")
        epas=chip("EPAS1 haplotype",PINK,28).move_to([-3,1.9,0])
        response=T("low-oxygen response",22,TEXT).move_to([-3,-.7,0])
        self.play(FadeIn(epas),run_time=.5)
        self.at("a gene in the low oxygen response")
        self.play(FadeIn(response),run_time=.6)
        self.at("probably came from")
        origin=T("probably Denisovan\nor a related group",24,PINK).move_to([-3,-2.5,0])
        self.play(FadeIn(origin),run_time=.6)
        base=Line([1,-1.6,0],[5.5,-1.6,0],color=GREY)
        freq=Rectangle(width=1,height=.45,color=PINK,fill_opacity=.7).move_to([3.2,-1.375,0])
        flabel=T("frequency",24,PINK).move_to([3.2,-2.1,0])
        self.at("and rose because")
        self.play(Create(base),FadeIn(freq),FadeIn(flabel),run_time=.5)
        self.play(freq.animate.stretch_to_fit_height(2.7).move_to([3.2,-.25,0]),run_time=1)
        self.at("adaptive introgression")
        self.play(ReplacementTransform(title,heading("Adaptive introgression",PINK)),run_time=.6)
        self.at("All people alive today")
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)],run_time=.4)
        title=heading("One species · Homo sapiens",BLUE)
        rows=VGroup(*[VGroup(chrom(y,-4.5,4.5,.42),
                            VGroup(*[site(True,TEXT,size=.22).move_to([x,y,0]) for x in [-3.8,-2.5,-1.2,.1,1.4,2.7,4]]),
                            site(True,[BLUE,YELLOW,TEAL,PINK][i],size=.22).move_to([[-3.2,-1.9,.8,3.35][i],y,0]))
                      for i,y in enumerate([1.65,.65,-.35,-1.35])])
        self.play(FadeIn(title),FadeIn(rows),run_time=.7)
        self.at("Most common variants")
        self.play(LaggedStart(*[Indicate(r[1],color=TEXT,scale_factor=1.04) for r in rows],lag_ratio=.1),run_time=.8)
        shared=T("Most common variants are shared worldwide",26,TEXT).move_to([0,-2.35,0])
        self.play(FadeIn(shared),run_time=.5)
        self.at("genetic variation does not divide")
        clusters=VGroup(*[Ellipse(width=10.1,height=2.2,color=BLUE,stroke_opacity=.35,fill_opacity=.025).move_to([x,y,0])
                          for x,y in [(-.25,.8),(.25,-.4)]])
        self.play(Create(clusters),FadeIn(T("Variation has no discrete racial boundaries",26,TEXT).move_to([0,-3.15,0])),run_time=.8)
        self.finish()


class S07End(EndCard):
    LINE = "We arose in Africa and mixed with Neanderthals and Denisovans."
