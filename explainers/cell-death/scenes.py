"""Cell death and clearance: ask every dying cell two questions  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = phosphatidylserine (the lipid heads)
  BLUE   = annexin V (the lipid question and its readout)
  ORANGE = propidium iodide and the stained DNA (the membrane question and its readout)
  GREEN  = apoptotic cell / the clearest apoptotic signal
  RED    = leak, secondary necrosis, the double-positive puzzle
  GREY   = membranes, outlines, labels, the necrosis-from-the-start cell
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"

# ---- stage geometry for the membrane scenes (s02 to s04) ----
MX0, MX1 = -6.2, 2.2
LIP_X = np.linspace(-5.4, 1.4, 8)
BLOB_X = [LIP_X[0], LIP_X[2], LIP_X[4]]
HOLES = [-0.057, 0.914]
HOLE_W = 0.46
PI_X = [LIP_X[1], LIP_X[3], -0.057, 0.914]
OUT_Y, IN_Y = 0.19, -0.19     # leaflet bar centres
BAR_H = 0.34
DNA_C = np.array([-2.0, -2.0, 0])


def bar_piece(x0, x1, y):
    return RoundedRectangle(corner_radius=0.06, width=x1 - x0, height=BAR_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.4).move_to([(x0 + x1) / 2, y, 0])


def bars_full():
    return VGroup(bar_piece(MX0, MX1, OUT_Y), bar_piece(MX0, MX1, IN_Y))


def bars_holed():
    edges = [MX0]
    for h in HOLES:
        edges += [h - HOLE_W / 2, h + HOLE_W / 2]
    edges.append(MX1)
    g = VGroup()
    for y in (OUT_Y, IN_Y):
        for i in range(0, len(edges), 2):
            g.add(bar_piece(edges[i], edges[i + 1], y))
    return g


def lipid_head(x, y):
    return Circle(radius=0.22, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([x, y, 0])


def annexin_blob(x, y):
    return RoundedRectangle(corner_radius=0.2, width=0.66, height=0.56, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.45).move_to([x, y, 0])


def pi_dot(x, y):
    return Circle(radius=0.17, stroke_color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.95).move_to([x, y, 0])


def dna_blob(lit=False):
    c = ORANGE if lit else GREY
    box = RoundedRectangle(corner_radius=0.5, width=3.0, height=1.05, stroke_color=c, stroke_width=3.5,
                           fill_color=c, fill_opacity=0.35 if lit else 0.1).move_to(DNA_C)
    lab = T("DNA", 26, c if lit else GREY).move_to(box)
    return VGroup(box, lab)


def readout(name, sign, color):
    on = sign == "+"
    c = color if on else GREY
    label = T(f"{name}  {'+' if on else '−'}", 28, c, weight=BOLD if on else NORMAL)
    box = RoundedRectangle(corner_radius=0.14, width=3.0, height=0.8, stroke_color=c, stroke_width=3,
                           fill_color=c, fill_opacity=0.2 if on else 0.05)
    return VGroup(box, label.move_to(box))


def legend_row(mark, text, color):
    return VGroup(mark, T(text, 22, color)).arrange(RIGHT, buff=0.22)


def stage_labels():
    a = T("outside the cell", 24, GREY).move_to([-4.2, 3.1, 0])
    b = T("inside the cell", 24, GREY).move_to([-4.6, -3.1, 0])
    return VGroup(a, b)


def panel_items(readA="−", readB="−"):
    ra = readout("annexin V", readA, BLUE).move_to([4.5, -0.9, 0])
    rb = readout("PI", readB, ORANGE).move_to([4.5, -2.0, 0])
    return ra, rb


def legend():
    r1 = legend_row(lipid_head(0, 0).scale(0.9), "phosphatidylserine", YELLOW)
    r2 = legend_row(annexin_blob(0, 0).scale(0.8), "annexin V", BLUE)
    r3 = legend_row(pi_dot(0, 0), "propidium iodide", ORANGE)
    g = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    g.move_to([4.5, 2.0, 0])
    return g, r1, r2, r3


def membrane_stage(lipids_out=False, holed=False, lit=False, blobs_bound=False):
    """Rebuild the membrane stage in the same place for each scene."""
    bars = bars_holed() if holed else bars_full()
    ly = 0.58 if lipids_out else -0.58
    lips = VGroup(*[lipid_head(x, ly) for x in LIP_X])
    blobs = VGroup(*[annexin_blob(x, 1.08 if blobs_bound else 2.0) for x in BLOB_X])
    dots = VGroup(*[pi_dot(x, 2.5) for x in PI_X])
    dna = dna_blob(lit)
    return bars, lips, blobs, dots, dna


# ---- plot helpers (s05, s06) ----
PC = np.array([-1.5, 0.3, 0])
QW, QH = 3.6, 2.9
COUNTS = {"BL": "5,800", "BR": "2,900", "TR": "1,000", "TL": "300"}


def qcentre(k):
    dx = -1 if k in ("BL", "TL") else 1
    dy = -1 if k in ("BL", "BR") else 1
    return PC + np.array([dx * QW / 2, dy * QH / 2, 0])


def quad_box(k):
    tint = {"BL": GREY, "BR": GREEN, "TR": RED, "TL": ORANGE}[k]
    return Rectangle(width=QW, height=QH, stroke_color=GREY, stroke_width=3, fill_color=tint,
                     fill_opacity=0.10).move_to(qcentre(k))


def plot_frame():
    boxes = {k: quad_box(k) for k in COUNTS}
    g = VGroup(*boxes.values())
    xl = T("annexin V  −", 24, BLUE).move_to(PC + np.array([-QW / 2, -QH - 0.4, 0]))
    xr = T("annexin V  +", 24, BLUE).move_to(PC + np.array([QW / 2, -QH - 0.4, 0]))
    yt = T("PI  +", 24, ORANGE).move_to(PC + np.array([-QW - 0.7, QH / 2, 0]))
    yb = T("PI  −", 24, ORANGE).move_to(PC + np.array([-QW - 0.7, -QH / 2, 0]))
    return boxes, VGroup(g, xl, xr, yt, yb)


def count_mob(k, opacity=1.0):
    c = qcentre(k)
    m = M(COUNTS[k], 42, TEXT).move_to(c + np.array([0.3, -0.35, 0]))
    return m.set_opacity(opacity)


def cell_dot(color, text=None, size=0.26):
    d = Circle(radius=size, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.55)
    if text:
        return VGroup(d, T(text, 24, TEXT, weight=BOLD).move_to(d))
    return d


def dot_legend(color, text, y, mark_text=None):
    mark = cell_dot(color, mark_text, size=0.22)
    lab = T(text, 22, color)
    g = VGroup(mark, lab).arrange(RIGHT, buff=0.2)
    g.move_to([4.5, y, 0])
    g.set_x(2.95 + g.width / 2)
    return g


def dot_pos(k, dx=0.0, dy=0.0):
    return qcentre(k) + np.array([-1.15 + dx, 0.85 + dy, 0])


# ---- cell-level schematics: outlines, labelled chips, never molecular structures ----
def cell_at(x=0, y=0, r=1.1, color=GREY):
    membrane = Circle(radius=r, stroke_color=color, stroke_width=4,
                      fill_color=color, fill_opacity=0.08)
    nucleus = Circle(radius=r * 0.32, stroke_color=color, stroke_width=3,
                     fill_color=color, fill_opacity=0.25).shift(UR * r * 0.15)
    return VGroup(membrane, nucleus).move_to([x, y, 0])


def heading(text, color=TEXT):
    return T(text, 34, color, font=TITLE_FONT).move_to([0, 3.0, 0])


def arrow_between(a, b, color=GREY):
    return Arrow(a.get_right(), b.get_left(), buff=0.18, color=color,
                 stroke_width=4, tip_length=0.2)


def lineage(x):
    # A representative branch, not a count of the worm's whole lineage.
    root = cell_dot(GREY).move_to([x, 1.2, 0])
    live = cell_dot(GREY).move_to([x-0.8, -0.2, 0])
    doomed = cell_dot(GREEN).move_to([x+0.8, -0.2, 0])
    branches = VGroup(Line(root.get_bottom(), live.get_top(), color=GREY),
                      Line(root.get_bottom(), doomed.get_top(), color=GREY))
    return VGroup(root, branches, live, doomed)


class S00Title(TitleCard):
    LESSON = "Cell death and clearance"
    TITLE = "Cell Death Is a Genetic Program"


class S01Ask(SpokenScene):
    def construct(self):
        c = cell_at(-2.8, 0, 1.8)
        q = T("?", 90, TEXT).move_to([2.5, 0, 0])
        self.at("Why would a body")
        self.play(FadeIn(c), FadeIn(q), run_time=0.5)
        title = heading("A normal genetic program")
        self.at("Death is a normal")
        self.play(FadeIn(title), c.animate.scale(0.65).set_color(GREEN),
                  FadeOut(q), run_time=0.8)
        cas = chip("caspases", GREEN, 28).move_to([2.8, 1.1, 0])
        protein = RoundedRectangle(width=2.6, height=0.5, color=GREY).move_to([2.8, -0.4, 0])
        pl = T("protein", 24, GREY).move_to([2.8, -1.3, 0])
        self.at("Apoptosis uses")
        self.play(FadeIn(cas), FadeIn(protein), FadeIn(pl), run_time=0.5)
        halves = VGroup(*[RoundedRectangle(width=1.15, height=0.5, color=GREY).move_to([x, -0.4, 0]) for x in (2.0, 3.6)])
        self.at("proteins that cut")
        self.play(ReplacementTransform(protein, halves), cas.animate.shift(DOWN*0.35), run_time=0.7)
        self.at("Cell loss balances")
        self.play(FadeOut(VGroup(c, cas, halves, pl)), run_time=0.3)
        division = VGroup(cell_at(-4.5, 0, 0.7), cell_at(-2.7, 0, 0.7))
        removal = cell_at(3.4, 0, 0.8, GREEN)
        balance = T("balances", 28, TEXT)
        labs = VGroup(T("cell division", 26, GREY).move_to([-3.6, -1.4, 0]),
                      T("cell loss", 26, GREEN).move_to([3.4, -1.4, 0]))
        self.play(FadeIn(division, scale=0.6), FadeIn(removal), FadeIn(balance), FadeIn(labs), run_time=0.6)
        self.play(removal.animate.scale(0.35).set_opacity(0.2), run_time=0.5)
        self.at("In the hermaphrodite worm")
        self.play(FadeOut(VGroup(division, removal, balance, labs, title)), run_time=0.35)
        title = heading("Hermaphrodite worm: fixed cell fates")
        worm = Ellipse(width=6.8, height=3.3, color=GREY, stroke_width=4).move_to([0, 0.5, 0])
        tree = lineage(0)
        self.play(FadeIn(title), Create(worm), FadeIn(tree), run_time=0.7)
        count = T("131 cells die on schedule", 30, GREEN).move_to([0, -2.3, 0])
        self.at("131 cells die")
        self.play(FadeIn(count), tree[3].animate.scale(0.3).set_opacity(0.2), run_time=0.7)
        self.at("The same cells die")
        self.play(worm.animate.shift(LEFT*3.4).scale(0.7), tree.animate.shift(LEFT*3.4), run_time=0.4)
        other = lineage(3.4)
        other[3].scale(0.3).set_opacity(0.2)
        worm2 = Ellipse(width=4.76, height=2.31, color=GREY, stroke_width=4).move_to([3.4, 0.5, 0])
        self.play(FadeIn(worm2), FadeIn(other), run_time=0.6)
        self.at("In healthy tissue")
        self.play(FadeOut(VGroup(title, worm, tree, worm2, other, count)), run_time=0.4)
        dead = cell_at(-1.5, 0, 0.55, GREEN)
        eater = cell_at(2.6, 0, 1.7)
        label = heading("Prompt clearance in healthy tissue")
        self.play(FadeIn(dead), FadeIn(eater), FadeIn(label), run_time=0.5)
        self.at("dead cells are cleared")
        self.play(eater.animate.move_to([0, 0, 0]), dead.animate.move_to([-0.4, 0, 0]), run_time=0.7)
        self.play(FadeOut(dead, scale=0.2), run_time=0.4)
        self.finish()


class S02Healthy(SpokenScene):
    def construct(self):
        h = heading("Repeated pattern → genetic test")
        wt = cell_at(-3.1, 0, 1.1, GREEN)
        mutant = cell_at(3.1, 0, 1.1, GREEN)
        wl = T("wild type", 28, GREY).move_to([-3.1, 1.9, 0])
        ml = T("same identified cell", 26, GREY).move_to([3.1, 1.9, 0])
        self.at("But a repeated pattern")
        self.play(FadeIn(h), FadeIn(wt), FadeIn(mutant), FadeIn(wl), FadeIn(ml), run_time=0.6)
        self.at("The test is")
        new = T("ced-3 or ced-4 mutant", 26, GREY).move_to(ml)
        self.play(ReplacementTransform(ml, new), run_time=0.6)
        self.at("Without SED 3")
        self.play(wt.animate.scale(0.25).set_opacity(0.2), run_time=0.6)
        self.at("die survive")
        outcomes = VGroup(T("dies", 28, GREEN).move_to([-3.1,-2,0]),
                          T("survives",28,GREEN).move_to([3.1,-2,0]))
        self.play(FadeIn(outcomes), Indicate(mutant, color=GREEN), run_time=0.5)
        self.at("Some even differentiate")
        processes = VGroup(Line([2.0,0,0],[1.1,0.4,0],color=GREEN),
                           Line([4.2,0,0],[5.1,-0.4,0],color=GREEN))
        self.play(Create(processes), ReplacementTransform(outcomes[1], T("survives + differentiates",24,GREEN).move_to([3.1,-2,0])), run_time=0.6)
        self.at("The death itself")
        self.play(Indicate(mutant, color=GREEN), run_time=0.5)
        self.at("turned out to be")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        ced3 = chip("CED-3: caspase", GREEN, 30).move_to([-3.1, 1.2, 0])
        self.play(FadeIn(ced3), run_time=0.5)
        self.at("protects cells")
        ced9 = chip("CED-9: protects cells", GREY, 30).move_to([3.0, 1.2, 0])
        self.play(FadeIn(ced9), run_time=0.5)
        self.at("Worm genetics")
        bridge = T("worm genetics → human death machinery", 30, TEXT).move_to([0,-1,0])
        self.play(FadeIn(bridge, shift=UP*0.2), run_time=0.7)
        self.at("In apoptosis")
        self.play(FadeOut(VGroup(ced3,ced9,bridge)),run_time=0.35)
        c = cell_at(0,0,2.0,GREEN)
        h = heading("Apoptosis")
        self.play(FadeIn(c),FadeIn(h),run_time=0.4)
        self.at("cells shrink")
        self.play(c.animate.scale(0.7),run_time=0.6)
        self.at("their nuclei fragment")
        frags = VGroup(*[Circle(radius=0.19,color=GREEN,fill_opacity=0.5).move_to([x,y,0]) for x,y in [(-0.4,0.2),(0.2,0.3),(0,-0.3)]])
        self.play(ReplacementTransform(c[1],frags),run_time=0.6)
        self.at("their membranes stay")
        note = T("membrane intact until late",28,GREY).move_to([0,-2.4,0])
        self.play(Indicate(c[0],color=GREY),FadeIn(note),run_time=0.6)
        self.finish()


class S03Flip(SpokenScene):
    def construct(self):
        c = cell_at(0,0,1.5)
        h = heading("Necrotic appearance")
        self.at("Necrotic looks")
        self.play(FadeIn(c),FadeIn(h),run_time=0.5)
        self.at("Swelling and rupture")
        self.play(c.animate.scale(1.25),run_time=0.6)
        broken = Arc(radius=1.875,start_angle=0.3,angle=TAU-0.7,color=RED,stroke_width=5)
        self.play(ReplacementTransform(c[0],broken),run_time=0.5)
        self.at("Necroptosis needs")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.3)
        titles = VGroup(*[T(t,27,GREY).move_to([x,2.2,0]) for t,x in zip(["Necroptosis","Pyroptosis","Ferroptosis"],[-4.4,0,4.4])])
        a = chip("RIPK3",GREY,26).move_to([-4.4,0.9,0])
        b = chip("MLKL",GREY,26).move_to([-4.4,-1.1,0])
        ar = Arrow(a.get_bottom(),b.get_top(),buff=0.15,color=GREY)
        self.play(FadeIn(titles[0]),FadeIn(a),GrowArrow(ar),FadeIn(b),run_time=0.7)
        self.at("uses gastrum")
        pore = VGroup(Line([-1.6,0,0],[-0.4,0,0],color=GREY,stroke_width=9),
                      Line([0.4,0,0],[1.6,0,0],color=GREY,stroke_width=9))
        porelab = T("gasdermin pores",24,GREY).move_to([0,-1.1,0])
        self.play(FadeIn(titles[1]),Create(pore),FadeIn(porelab),run_time=0.6)
        self.at("Ferroptosis depends")
        iron = chip("iron",GREY,26).move_to([4.4,0.9,0])
        lipid = T("severe lipid\nperoxidation",24,GREY).move_to([4.4,-1.1,0])
        ar2 = Arrow(iron.get_bottom(),lipid.get_top(),buff=0.15,color=GREY)
        self.play(FadeIn(titles[2]),FadeIn(iron),GrowArrow(ar2),FadeIn(lipid),run_time=0.7)
        self.at("These are distinct")
        note = T("Separate regulated routes",30,TEXT).move_to([0,-2.8,0])
        self.play(FadeIn(note),run_time=0.5)
        self.at("Appearance names")
        self.play(ReplacementTransform(note,T("Appearance names an endpoint",30,TEXT).move_to(note)),run_time=0.5)
        self.at("To identify the cause")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.3)
        h=heading("Test the machinery")
        machine=chip("machinery",GREY,30).move_to([-3.3,0.6,0])
        read=chip("death readout",GREY,30).move_to([3.3,0.6,0])
        ar=arrow_between(machine,read)
        self.play(FadeIn(h),FadeIn(machine),GrowArrow(ar),FadeIn(read),run_time=0.6)
        self.at("perturb the machinery")
        cross=Cross(machine,stroke_color=RED,stroke_width=5)
        self.play(Create(cross),run_time=0.45)
        self.at("see whether the death")
        self.play(FadeIn(T("Does death change?",32,TEXT).move_to([0,-1.6,0])),run_time=0.6)
        self.finish()


class S04Leak(SpokenScene):
    def construct(self):
        c=cell_at(-3.0,0,1.2,GREEN)
        ph=cell_at(3.4,0,1.8)
        ph[1].shift(RIGHT*0.6 + UP*0.35)
        h=heading("Clearance")
        pl=T("phagocyte",26,GREY).move_to([3.4,-2.4,0])
        self.at("Now follow the cleanup")
        self.play(FadeIn(c),FadeIn(h),run_time=0.5)
        self.at("A dying cell calls")
        self.play(FadeIn(ph),FadeIn(pl),run_time=0.5)
        channel=chip("PANX1",GREY,22).move_to([-1.8,0,0])
        cas=T("caspases open PANX1",25,GREEN).move_to([-3,2,0])
        nts=VGroup(*[Dot([-1.3,y,0],radius=0.09,color=GREY) for y in [-0.4,0,0.4]])
        self.at("Caspases open channels")
        self.play(FadeIn(channel),FadeIn(cas),run_time=0.5)
        self.at("that release nucleotides")
        signal=T("nucleotides: find me",24,GREY).move_to([0,-2.9,0])
        self.play(FadeIn(nts),FadeIn(signal),run_time=0.25)
        self.play(nts.animate.shift(RIGHT*2.4),ph.animate.shift(LEFT*0.5),run_time=0.6)
        lips=VGroup(*[lipid_head(-3+0.95*np.cos(a),0.95*np.sin(a)) for a in [PI/2,PI,3*PI/2]])
        self.at("The cell also exposes")
        self.play(FadeOut(VGroup(channel,cas,nts,signal)),FadeIn(lips),run_time=0.4)
        ps=T("phosphatidylserine (PS)",26,YELLOW).move_to([-2.6,2.1,0])
        self.play(FadeIn(ps),*[l.animate.move_to([-3+1.35*np.cos(a),1.35*np.sin(a),0]) for l,a in zip(lips,[PI/2,PI,3*PI/2])],run_time=0.7)
        self.at("That is an eat")
        eat=T("eat me",28,YELLOW).move_to([-3,-2.1,0])
        self.play(FadeIn(eat),run_time=0.5)
        self.at("A phagocyte recognizes")
        self.play(ph.animate.move_to([-0.5,0,0]),FadeOut(pl),run_time=0.6)
        self.at("engulfs it")
        self.play(FadeOut(VGroup(ps,eat,lips)),c.animate.scale(0.5).move_to([-0.8,0,0]),ph.animate.move_to([0,0,0]),run_time=0.65)
        phagosome=Circle(radius=0.8,color=GREY).move_to([-0.8,0,0])
        pglabel=T("phagosome",22,GREY).move_to([-0.8,-1.25,0])
        lys=Circle(radius=0.35,color=GREY,fill_color=GREY,fill_opacity=0.3).move_to([2.8,-0.6,0])
        lyslabel=T("lysosome",22,GREY).move_to([3.0,-1.4,0])
        self.play(Create(phagosome),FadeIn(pglabel),run_time=0.3)
        self.at("and digests it")
        self.play(FadeIn(lys),FadeIn(lyslabel),run_time=0.25)
        self.at("in lysosomes")
        self.play(lys.animate.move_to([-0.1,-0.3,0]),FadeOut(VGroup(pglabel,lyslabel)),run_time=0.5)
        self.play(FadeOut(VGroup(c,phagosome,lys),scale=0.2),run_time=0.4)
        self.at("In culture")
        self.play(FadeOut(VGroup(h,ph)),run_time=0.3)
        h=heading("Culture: no phagocyte")
        c=cell_at(0,0,1.5,GREEN)
        self.play(FadeIn(h),FadeIn(c),run_time=0.5)
        self.at("generally become leaky")
        broken=Arc(radius=1.5,start_angle=0.3,angle=TAU-0.7,color=RED,stroke_width=4)
        leaking=VGroup(*[Dot([1.6,y,0],color=RED,radius=0.09) for y in [-0.2,0,0.2]])
        self.play(ReplacementTransform(c[0],broken),FadeIn(leaking),run_time=0.4)
        self.play(leaking.animate.shift(RIGHT*1.4),run_time=0.4)
        self.at("secondary necrosis")
        self.play(FadeIn(T("secondary necrosis",30,RED).move_to([0,-2.6,0])),run_time=0.5)
        self.finish()


class S05Plot(SpokenScene):
    def construct(self):
        bars,lips,blobs,dots,dna=membrane_stage(lipids_out=True)
        # Reuse the film's yellow PS, blue annexin and orange dye schematics.
        lips=VGroup(lips[0],lips[2],lips[4])
        dots=VGroup(dots[2],dots[3])
        lab=stage_labels()
        self.at("How do we measure")
        self.play(FadeIn(bars),FadeIn(lips),FadeIn(lab),run_time=0.5)
        self.at("binds phosphatidylserine")
        al=T("annexin V",28,BLUE).move_to([4.3,2,0])
        ps=T("accessible PS",26,YELLOW).move_to([4.3,0.8,0])
        self.play(FadeIn(blobs),FadeIn(al),FadeIn(ps),run_time=0.4)
        self.at("reachable from outside")
        self.play(*[b.animate.move_to([b.get_x(),1.08,0]) for b in blobs],run_time=0.6)
        self.at("Propidium iodide")
        pil=T("propidium iodide",26,ORANGE).move_to([4.3,-0.6,0])
        self.play(FadeIn(dots),FadeIn(dna),FadeIn(pil),run_time=0.5)
        self.at("Its entry means")
        self.play(ReplacementTransform(bars,bars_holed()),run_time=0.3)
        self.play(*[d.animate.move_to([d.get_x(),-0.8,0]) for d in dots],run_time=0.7)
        self.play(*[d.animate.move_to(DNA_C+np.array([dx,0,0])) for d,dx in zip(dots,[-1,1])],ReplacementTransform(dna,dna_blob(True)),run_time=0.5)
        self.at("Neither marker tells")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.3)
        boxes,frame=plot_frame()
        self.play(FadeIn(frame),run_time=0.5)
        puzzle=T("One box, two histories",26,RED).move_to([4.5,2.7,0])
        self.play(FadeIn(puzzle),run_time=0.4)
        self.at("Cells positive for both")
        self.play(boxes["TR"].animate.set_fill(RED,0.25),run_time=0.4)
        late=cell_dot(GREEN).move_to([3.1,0.8,0])
        ll=T("late apoptotic",24,GREEN).move_to([4.5,1.5,0])
        self.at("late apoptotic")
        self.play(FadeIn(late),FadeIn(ll),run_time=0.25)
        self.play(late.animate.move_to(dot_pos("TR")),run_time=0.5)
        nec=cell_dot(GREY).move_to([3.1,-1.1,0])
        nl=T("necrotic from\nthe start",24,GREY).move_to([4.5,-0.4,0])
        self.at("or necrotic")
        self.play(FadeIn(nec),FadeIn(nl),run_time=0.25)
        self.play(nec.animate.move_to(dot_pos("TR",dy=-0.65)),run_time=0.5)
        self.finish()


class S06Time(SpokenScene):
    def construct(self):
        boxes,frame=plot_frame()
        self.add(frame)
        tm=T("follow time →",28,TEXT).move_to([4.4,2.6,0])
        d=cell_dot(GREEN).move_to(dot_pos("BL"))
        self.at("So combine markers")
        self.play(FadeIn(tm),FadeIn(d),run_time=0.5)
        p0,p1,p2=dot_pos("BL"),dot_pos("BR"),dot_pos("TR")
        self.at("expose the lipid")
        t1=Line(p0,p1,color=GREEN,stroke_width=4)
        self.play(Create(t1),d.animate.move_to(p1),boxes["BR"].animate.set_fill(GREEN,0.2),run_time=0.7)
        al=T("apoptosis",27,GREEN).move_to([4.5,1.4,0])
        self.play(FadeIn(al),run_time=0.3)
        self.at("they leak")
        t2=Line(p1,p2,color=GREEN,stroke_width=4)
        self.play(Create(t2),d.animate.move_to(p2),run_time=0.7)
        self.at("can do that too")
        n=cell_dot(GREY).move_to(p0+DOWN*0.4)
        nl=T("necroptosis\ncan do this too",24,GREY).move_to([4.5,-0.1,0])
        path=VMobject(color=GREY,stroke_width=4).set_points_as_corners([p0+DOWN*0.4,p1+DOWN*0.4,p2+RIGHT*0.85])
        self.play(FadeIn(n),FadeIn(nl),run_time=0.3)
        self.play(Create(path),MoveAlongPath(n,path),run_time=0.7)
        self.at("A time course helps")
        note=T("informative",27,TEXT).move_to([4.5,-1.6,0])
        self.play(FadeIn(note),run_time=0.4)
        self.at("cannot settle the mechanism")
        self.play(ReplacementTransform(note,T("insufficient alone",25,RED).move_to(note)),run_time=0.5)
        self.at("One marker reports")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.35)
        rule=heading("One marker reports one event")
        self.play(FadeIn(rule),run_time=0.5)
        spine=VGroup(chip("genetic program",GREY,26),chip("distinct machinery",GREY,26),chip("recognition + clearance",GREY,26)).arrange(RIGHT,buff=0.5).move_to([0,0.7,0])
        self.at("Genetic control")
        self.play(FadeIn(spine[0]),run_time=0.5)
        self.at("distinct machinery")
        self.play(FadeIn(spine[1]),run_time=0.5)
        self.at("and clearance")
        self.play(FadeIn(spine[2]),run_time=0.5)
        measures=VGroup(readout("annexin V","+",BLUE),readout("PI","+",ORANGE)).arrange(RIGHT,buff=0.5).move_to([0,-1.5,0])
        ml=T("complementary measurements",25,TEXT).move_to([0,-2.6,0])
        self.at("behind the signal")
        self.play(FadeIn(measures),FadeIn(ml),run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Cell death is a genetic program, with distinct machinery and fast clearance."
