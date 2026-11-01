"""Cell identity, cell state and disease: a mutant clone wins by fate, not speed (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE    progenitor cell (a basal cell that divides); the starting count of progenitors
  GREEN   differentiating cell (moves up and is shed); "consistent" tick
  PURPLE  competitive clones around an early lesion (mouse model)
  YELLOW  Notch1-mutant cell or clone, and the grown progenitor count of the clone
  RED     cancer / malignant, the crossed-out idea, the early lesion
  GREY    structure, frames, neutral labels
  TEAL    T-cell identity; RNA measurements
  TEXT    all other labels and state symbols (state never changes identity colour)
"""
import random
from bp_style import *


PURPLE = "#B58CE0"


# ---------- helpers ----------
def dot(color, r=0.28, fo=0.45, sw=2.5):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fo)


def cell_grid(cols, rows, sp, center):
    cells = VGroup(*[dot(GREY, r=sp * 0.43, fo=0.18, sw=2) for _ in range(cols * rows)])
    cells.arrange_in_grid(rows=rows, cols=cols, buff=sp * 0.14).move_to(center)
    return cells


def stack(center, mut_cols=(), mut_top=0):
    """Epithelium side view: row 0 = basal progenitors (blue), rows above = differentiating (green)."""
    sp = 0.84
    g = VGroup()
    basal, diff = VGroup(), VGroup()
    for c in range(5):
        col = YELLOW if c in mut_cols else BLUE
        d = dot(col, r=0.34).move_to(center + RIGHT * (c - 2) * sp + DOWN * 1.7)
        basal.add(d)
    for r in range(1, 5):
        for c in range(5):
            d = dot(GREEN, r=0.34, fo=0.4).move_to(center + RIGHT * (c - 2) * sp + DOWN * 1.7 + UP * r * sp)
            diff.add(d)
    return basal, diff


def pair(a, b, c0, gap=0.7, r=0.22):
    x, y = dot(a, r=r), dot(b, r=r)
    x.move_to(c0 + LEFT * gap / 2)
    y.move_to(c0 + RIGHT * gap / 2)
    return VGroup(x, y)


def division_row(y, left_col, right_col, label, x0=-0.6):
    parent = dot(BLUE, r=0.26).move_to(RIGHT * x0 + UP * y)
    arrow = Arrow(parent.get_right() + RIGHT * 0.1, RIGHT * (x0 + 1.5) + UP * y, buff=0, color=GREY, stroke_width=3,
                  max_tip_length_to_length_ratio=0.3)
    kids = pair(left_col, right_col, RIGHT * (x0 + 2.4) + UP * y)
    lab = T(label, size=24).next_to(kids, RIGHT, buff=0.4)
    lab.align_to(RIGHT * 2.9, LEFT)
    return VGroup(parent, arrow, kids, lab)


def cross(mob, color=RED):
    a = Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=7)
    b = Line(mob.get_corner(UR), mob.get_corner(DL), color=color, stroke_width=7)
    return VGroup(a, b)


def strike(mob, color=RED):
    return Line(mob.get_left() + LEFT * 0.05, mob.get_right() + RIGHT * 0.05, color=color, stroke_width=7)


def tick(color=GREEN):
    return VMobject(color=color, stroke_width=8).set_points_as_corners(
        [LEFT * 0.22 + UP * 0.0, LEFT * 0.06 + DOWN * 0.18, RIGHT * 0.26 + UP * 0.22])


# Small schematic groups are single visual units; identity colours never encode state.
def heading(text):
    return T(text, size=34, font=TITLE_FONT).move_to(UP * 3.15)


def cells(colors, positions, r=0.38):
    return VGroup(*[dot(c, r=r).move_to(p) for c, p in zip(colors, positions)])


def barcode(label, pos):
    return chip(label, GREY, size=22, pad=0.12).move_to(pos)


def cycle_symbol(pos):
    a = Arc(radius=0.18, start_angle=0.3, angle=5.2, color=TEXT, stroke_width=3)
    a.add_tip(tip_length=0.09)
    return a.move_to(pos)


def clear(scene, *keep):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects) if m not in keep], run_time=0.35)


class S00Title(TitleCard):
    LESSON = "Cell Identity, Cell State and Disease"
    TITLE = "Cell Identity, Cell State and Disease"


class S01Identity(SpokenScene):
    def construct(self):
        h = heading("What is inside a tissue?")
        outline = RoundedRectangle(width=5, height=3.4, corner_radius=0.7, color=GREY)
        pts = [[-1.4,0.65,0],[0,0.65,0],[1.4,0.65,0],[-1.4,-0.65,0],[0,-0.65,0],[1.4,-0.65,0]]
        tissue = cells([TEAL,RED,GREY,TEAL,RED,GREY], pts)
        self.at("A tissue")
        self.play(FadeIn(h), Create(outline), FadeIn(tissue), run_time=0.8)
        self.at("reveals a mixture")
        self.play(FadeOut(outline), *[c.animate.move_to([[-4,0.65,0],[0,0.65,0],[4,0.65,0],[-4,-0.65,0],[0,-0.65,0],[4,-0.65,0]][i]) for i,c in enumerate(tissue)], run_time=1)
        self.at("A type is")
        lab = T("T-cell identity", 28, TEAL).move_to([-4,1.9,0])
        self.play(FadeIn(lab), Indicate(VGroup(tissue[0],tissue[3]), color=TEAL), run_time=0.6)
        self.at("A state is")
        syms = VGroup(cycle_symbol(tissue[0].get_center()), T("!",26).move_to(tissue[3]))
        states = T("cycling / stress", 24).move_to([-4,-1.8,0])
        self.play(FadeIn(syms), FadeIn(states), run_time=0.6)
        self.at("In melanoma")
        clear(self)
        h = heading("One melanoma: malignant identity")
        mal = cells([RED]*6, pts, r=0.43)
        self.play(FadeIn(h), FadeIn(mal), run_time=0.6)
        self.at("differed in")
        cycling = VGroup(*[cycle_symbol(mal[i].get_center()) for i in range(3)])
        self.play(FadeIn(cycling), run_time=0.55)
        self.at("separate clusters")
        dest = [[-3.8,0.6,0],[-2.6,0.6,0],[-3.2,-0.6,0],[2.6,0.6,0],[3.8,0.6,0],[3.2,-0.6,0]]
        self.play(*[m.animate.move_to(p) for m,p in zip(mal,dest)], *[cycling[i].animate.move_to(dest[i]) for i in range(3)], run_time=0.8)
        tags = VGroup(T("cycling state?",26).move_to([-3.2,-1.8,0]),T("other cycle state?",26).move_to([3.2,-1.8,0]))
        self.at("different states")
        self.play(FadeIn(tags), run_time=0.5)
        self.at("needs an explanation")
        self.play(FadeIn(T("provisional annotations",26,GREY).move_to(DOWN*2.8)),run_time=0.5)
        self.finish()


class S01Matrix(SpokenScene):
    def construct(self):
        tissue = cells([TEAL,GREY,TEAL,GREY], [[-.5,.5,0],[.5,.5,0],[-.5,-.5,0],[.5,-.5,0]])
        self.add(tissue)
        self.at("Separate the cells")
        self.play(*[c.animate.move_to([x,1.5,0]) for c,x in zip(tissue,[-4.5,-1.5,1.5,4.5])],run_time=0.8)
        rna = VGroup(*[VGroup(*[chip("RNA",TEAL,22,pad=.1).move_to([x,y,0]) for y in [0,-.75]]) for x in [-4.5,-1.5,1.5,4.5]])
        tags = VGroup(*[VGroup(*[barcode(b,[x+.85,y,0]) for y in [0,-.75]]) for x,b in zip([-4.5,-1.5,1.5,4.5],["A","B","C","D"])])
        self.at("Tag each")
        self.play(FadeIn(rna),FadeIn(tags),run_time=.7)
        self.at("sequence and count")
        self.play(FadeOut(tissue),rna.animate.shift(UP*.4),tags.animate.shift(UP*.4),run_time=.5)
        self.at("The matrix has")
        clear(self)
        h=heading("Genes × cells: captured RNA counts")
        vals=[[8,1,7,1],[6,0,5,1],[0,7,1,6]]
        mat=VGroup(*[VGroup(*[VGroup(Rectangle(width=.8,height=.65,color=GREY,fill_color=TEAL,fill_opacity=.08+.06*vals[j][i]),M(str(vals[j][i]),22)).move_to([-1.5+i,1-j*.8,0]) for j in range(3)]) for i in range(4)])
        cols=VGroup(*[T(b,24).move_to([-1.5+i,1.75,0]) for i,b in enumerate("ABCD")])
        axes=VGroup(T("cells",26).move_to([0,2.35,0]),T("genes",26).move_to([-3.2,.2,0]))
        self.play(FadeIn(h),FadeIn(mat),FadeIn(cols),FadeIn(axes),run_time=.65)
        self.at("Group similar cells")
        self.play(mat[1].animate.shift(RIGHT),mat[2].animate.shift(LEFT),cols[1].animate.shift(RIGHT),cols[2].animate.shift(LEFT),run_time=.6)
        self.at("annotate their clusters")
        known=VGroup(T("known profiles",24,GREY).move_to([4.5,1.8,0]))
        for i, pattern in enumerate([[.8,.7,.1],[.1,.1,.8]]):
            for j, level in enumerate(pattern):
                known.add(Rectangle(width=.7,height=.65,stroke_color=GREY,fill_color=TEAL,fill_opacity=level).move_to([4+i,1-j*.8,0]))
        known.add(T("compare patterns",22,GREY).move_to([4.5,-1.3,0]))
        groups=VGroup(*[SurroundingRectangle(VGroup(mat[a],mat[b]),buff=.08,color=GREY) for a,b in [(0,2),(1,3)]])
        provisional=T("cluster annotations remain provisional",26).move_to([0,-2,0])
        self.play(FadeIn(known),Create(groups),FadeIn(provisional),run_time=.7)
        self.finish()


class S02Validation(SpokenScene):
    def construct(self):
        h=heading("A cluster can be an artifact")
        two=pair(TEAL,GREY,LEFT*3,gap=1.2,r=.5)
        tag=barcode("shared barcode",[-3,-1.3,0])
        hybrid=chip("hybrid profile?",GREY,28).move_to([2.8,0,0])
        self.at("But a cluster")
        self.play(FadeIn(h),FadeIn(two),run_time=.7)
        self.at("Two cells")
        self.play(FadeIn(tag),run_time=.5)
        self.at("share a barcode")
        self.play(TransformFromCopy(two,hybrid),run_time=.6)
        self.at("Sample handling")
        clear(self)
        h=heading("One identity, different handling")
        batch=cells([TEAL]*4,[[-.8,.5,0],[.8,.5,0],[-.8,-.5,0],[.8,-.5,0]])
        labs=VGroup(T("batch A",26,GREY).move_to([-3.2,-1.7,0]),T("batch B",26,GREY).move_to([3.2,-1.7,0]))
        self.play(FadeIn(h),FadeIn(batch),run_time=.5)
        self.at("separate cells")
        self.play(*[c.animate.shift(LEFT*2.4 if i%2==0 else RIGHT*2.4) for i,c in enumerate(batch)],FadeIn(labs),run_time=.7)
        self.at("Check annotations")
        clear(self)
        ann=chip("annotation?",GREY,28).move_to([-3.3,1.6,0])
        ev=chip("independent evidence",GREEN,28).move_to([2.7,1.6,0])
        self.play(FadeIn(ann),FadeIn(ev),run_time=.6)
        self.at("RNA does not")
        mismatch=T("RNA ≠ protein",32).move_to([0,0,0])
        self.play(FadeIn(mismatch),run_time=.5)
        self.at("measures surface proteins")
        clear(self)
        h=heading("CITE-seq: RNA + surface protein")
        cell=dot(TEAL,r=.95).move_to([-2.7,-.3,0])
        # Antibody is a labelled chip, with a separate DNA tag; no molecule drawing.
        protein=chip("surface protein",GREY,22).move_to([-.4,-.3,0])
        antibody=chip("antibody",GREEN,24).move_to([-.4,1,0])
        dna=chip("DNA tag",GREY,22).next_to(antibody,RIGHT,buff=.3)
        rna=chip("RNA",TEAL,26).move_to(cell)
        readout=VGroup(T("protein readout",26,GREEN),T("RNA readout",26,TEAL)).arrange(DOWN,buff=.45).move_to([4,-1.1,0])
        self.play(FadeIn(h),FadeIn(cell),FadeIn(protein),FadeIn(antibody),FadeIn(dna),FadeIn(rna),run_time=.7)
        self.at("alongside RNA")
        self.play(Indicate(dna,color=GREY),Indicate(rna,color=TEAL),FadeIn(readout),run_time=.6)
        self.at("the same cell")
        self.play(Indicate(cell,color=TEAL),run_time=.5)
        self.finish()


class S03Lineage(SpokenScene):
    def construct(self):
        h=heading("Inferred pseudotime")
        path=DashedLine([-4,-1,0],[4,1,0],color=GREY)
        sampled=cells([GREY]*4,[[-4,-1,0],[-1.4,-.35,0],[1.4,.35,0],[4,1,0]],r=.42)
        note=T("different sampled cells",28).move_to(DOWN*2.3)
        self.at("An expression path")
        self.play(FadeIn(h),Create(path),FadeIn(sampled),run_time=.8)
        self.at("does not track")
        self.play(FadeIn(note),run_time=.5)
        self.at("Sequencing destroys")
        self.play(*[FadeOut(c,scale=.3) for c in sampled],run_time=.6)
        self.at("Inherited barcodes")
        clear(self)
        h=heading("Inherited barcode links sisters")
        parent=dot(BLUE,.4).move_to([0,1.7,0])
        sisters=pair(BLUE,BLUE,[0,.1,0],gap=5,r=.4)
        branches=VGroup(Line([0,1.3,0],[-2.5,.5,0],color=GREY),Line([0,1.3,0],[2.5,.5,0],color=GREY))
        tags=VGroup(*[barcode("A",p) for p in [[.8,1.7,0],[-1.6,.1,0],[3.4,.1,0]]])
        self.play(FadeIn(h),FadeIn(parent),Create(branches),FadeIn(sisters),FadeIn(tags),run_time=.7)
        self.at("linking sisters")
        seq=chip("sequence RNA",TEAL,24).move_to([-3,-1.4,0])
        kids=pair(BLUE,BLUE,[2.5,-1.5,0],gap=1.5,r=.35)
        kt=VGroup(*[barcode("A",p) for p in [[1.75,-2.3,0],[3.25,-2.3,0]]])
        self.play(ReplacementTransform(sisters[0],seq),TransformFromCopy(sisters[1],kids),FadeIn(kt),run_time=.7)
        self.at("In mouse blood")
        context=T("mouse blood progenitors",26,GREY).move_to([0,-3.1,0])
        self.play(FadeIn(context),run_time=.5)
        self.at("shared fate biases")
        clear(self)
        h=heading("Similar RNA can hide different futures")
        profiles=VGroup(chip("similar RNA",TEAL,28).move_to([-3,1.2,0]),chip("similar RNA",TEAL,28).move_to([3,1.2,0]))
        fates=VGroup(chip("fate bias A",GREY,26).move_to([-3,-1,0]),chip("fate bias B",GREY,26).move_to([3,-1,0]))
        arrows=VGroup(*[Arrow(p.get_bottom(),f.get_top(),color=GREY,buff=.15) for p,f in zip(profiles,fates)])
        self.play(FadeIn(h),FadeIn(profiles),FadeIn(fates),Create(arrows),run_time=.7)
        self.at("Perturbation tests cause")
        clear(self)
        h=heading("Test a cause")
        candidate=chip("candidate",GREY,28).move_to([-4,0,0])
        self.play(FadeIn(h),FadeIn(candidate),run_time=.4)
        self.at("block a candidate")
        x=cross(candidate)
        self.play(Create(x),run_time=.4)
        self.at("check the outcome")
        outcome=chip("check outcome",GREY,28).move_to([0,0,0])
        self.play(FadeIn(outcome),run_time=.4)
        self.at("then restore it")
        restored=chip("restore candidate",GREY,28).move_to([4,0,0])
        self.play(FadeIn(restored),run_time=.4)
        self.finish()


class S04Composition(SpokenScene):
    def construct(self):
        h=heading("A mixture can change the bulk signal")
        # Same per-cell fill and RNA mark for each identity in both conditions.
        def mixture(x,cols):
            g=VGroup()
            for i,c in enumerate(cols):
                body=dot(c,.35).move_to([x+(i%2-.5)*1.1,.9-(i//2)*1.1,0])
                mark=Line(body.get_center()+DOWN*.16,body.get_center()+UP*(.18 if c==TEAL else -.02),color=TEXT,stroke_width=5)
                g.add(VGroup(body,mark))
            return g
        left=mixture(-3,[TEAL,GREY,GREY,GREY])
        right=mixture(3,[TEAL,GREY,GREY,GREY])
        names=VGroup(T("mixture before",26).move_to([-3,2,0]),T("mixture after",26).move_to([3,2,0]))
        self.at("A bulk measurement")
        self.play(FadeIn(h),FadeIn(left),FadeIn(right),FadeIn(names),run_time=.7)
        self.at("stays fixed")
        fixed=T("per-cell expression stays fixed",26).move_to([0,-1.5,0])
        self.play(FadeIn(fixed),run_time=.5)
        self.at("More cells expressing")
        self.play(Transform(right,mixture(3,[TEAL,TEAL,TEAL,GREY])),run_time=.7)
        baseline=Line([-4.8,-3,0],[4.8,-3,0],color=GREY)
        bars=VGroup(Rectangle(width=1.1,height=.45,fill_color=GREY,fill_opacity=.8,stroke_width=0).move_to([-3,-3,0],aligned_edge=DOWN),Rectangle(width=1.1,height=.45,fill_color=GREY,fill_opacity=.8,stroke_width=0).move_to([3,-3,0],aligned_edge=DOWN))
        self.at("raise the tissue average")
        self.play(Create(baseline),FadeIn(bars),run_time=.3)
        self.play(bars[1].animate.stretch_to_fit_height(1).move_to([3,-3,0],aligned_edge=DOWN),run_time=.5)
        self.at("data separate")
        self.play(Transform(fixed,T("same within-type levels; changed proportions",26).move_to([0,-1.5,0])),run_time=.5)
        self.at("losing fragile cells")
        clear(self)
        h=heading("Dissociation can bias proportions")
        fragile=mixture(-2,[TEAL,TEAL,GREY,GREY])
        label=T("fragile cells lost",28,GREY).move_to([3,1,0])
        caution=T("measured mixture ≠ original mixture",28).move_to([0,-2,0])
        self.play(FadeIn(h),FadeIn(fragile),run_time=.4)
        self.play(FadeOut(fragile[0],shift=UP*.6),FadeOut(fragile[1],shift=UP*.6),FadeIn(label),run_time=.7)
        self.at("bias the measured")
        self.play(FadeIn(caution),run_time=.5)
        self.finish()


class S02Balance(SpokenScene):
    def construct(self):
        h=heading("Balance cell gain and loss")
        # Reuse the original epithelial stack, with fewer cells visible at once.
        basal,upper=stack(LEFT*3.4)
        diff=VGroup(upper[10],upper[12],upper[14])
        basal=VGroup(basal[0],basal[2],basal[4])
        floor=Line([-5.7,-2.3,0],[-1.1,-2.3,0],color=GREY)
        system=T("mouse oesophagus",26,GREY).move_to([-3.4,2.3,0])
        self.at("Tissue health")
        self.play(FadeIn(h),Create(floor),FadeIn(basal),FadeIn(diff),run_time=.7)
        self.at("In mouse")
        self.play(FadeIn(system),run_time=.4)
        self.at("progenitors divide")
        kids=pair(BLUE,BLUE,[-3.4,-1.7,0],gap=.8,r=.3)
        self.play(ReplacementTransform(basal[1],kids),run_time=.6)
        self.at("daughters differentiate")
        lab=T("differentiate",28,GREEN).move_to([3,.3,0])
        self.play(kids[1].animate.set_color(GREEN).set_fill(GREEN,.4).shift(UP*1.6),FadeIn(lab),run_time=.65)
        self.at("cells are shed")
        self.play(FadeOut(diff,shift=UP*.8),run_time=.65)
        self.at("In crowded")
        clear(self)
        h=heading("Crowding-driven live-cell extrusion")
        system=T("MDCK cultured sheets / zebrafish epidermis",26,GREY).move_to([0,2.2,0])
        sheet=cells([GREY]*5,[[x,-.8,0] for x in [-3,-1.5,0,1.5,3]],r=.58)
        floor=Line([-4,-1.5,0],[4,-1.5,0],color=GREY)
        self.play(FadeIn(h),FadeIn(system),FadeIn(sheet),Create(floor),run_time=.6)
        self.at("living cells")
        live=T("living",26).move_to([0,.25,0])
        self.play(FadeIn(live),run_time=.3)
        self.at("squeezed out")
        self.play(sheet[0].animate.shift(RIGHT*.6),sheet[1].animate.shift(RIGHT*.4),sheet[3].animate.shift(LEFT*.4),sheet[4].animate.shift(LEFT*.6),sheet[2].animate.shift(UP*1.4),live.animate.shift(UP*1.4),run_time=.65)
        self.at("then die")
        dead=T("death outside the sheet",26,GREY).move_to([0,.55,0])
        self.play(FadeOut(live),FadeOut(sheet[2],scale=.3),FadeIn(dead),run_time=.6)
        self.at("Cell interactions")
        self.play(Indicate(VGroup(sheet[1],sheet[3]),color=GREY),run_time=.7)
        self.finish()


class S03Fate(SpokenScene):
    def construct(self):
        h=heading("Smaller point: mouse Notch1 clones")
        c=LEFT*3.5
        basal,diff=stack(c)
        diff=VGroup(diff[10],diff[12],diff[14])
        floor=Line([-5.7,-2.3,0],[-1.3,-2.3,0],color=GREY)
        self.at("A smaller point")
        self.play(FadeIn(h),FadeIn(basal),FadeIn(diff),Create(floor),run_time=.7)
        self.at("In mouse")
        system=T("mouse oesophagus",24,GREY).move_to([-3.5,1.8,0])
        self.play(FadeIn(system),run_time=.4)
        self.at("mutant clones expanded")
        self.play(basal[2].animate.set_color(YELLOW).set_fill(YELLOW,.5),run_time=.3)
        self.play(*[basal[i].animate.set_color(YELLOW).set_fill(YELLOW,.5) for i in [1,3]],run_time=.5)
        self.at("without dividing faster")
        rate=chip("division timing unchanged",GREY,26).move_to([2.8,1.5,0])
        self.play(FadeIn(rate),run_time=.5)
        pr=pair(BLUE,GREEN,[2.8,-.1,0],gap=1.2,r=.4)
        fate=T("daughter fates",26).move_to([2.8,.65,0])
        self.at("Tracking was consistent")
        self.play(FadeIn(pr),FadeIn(fate),run_time=.5)
        self.at("more progenitor daughters")
        self.play(Transform(pr[1],dot(BLUE,.4).move_to(pr[1])),run_time=.6)
        self.at("fewer differentiating")
        cons=T("consistent with a fate shift",24,GREY).move_to([2.8,-1.25,0])
        self.play(FadeIn(cons),run_time=.5)
        title=T("Cell Identity, Cell State and Disease",32,font=TITLE_FONT).move_to([0,-3,0])
        self.at("ones")
        self.play(FadeIn(title),run_time=.5)
        self.finish()


class S07End(EndCard):
    LINE = "A tissue is a mixture of types and states, not one average."
