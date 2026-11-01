"""Radial glia: the cell stays, the nucleus travels  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the radial glial / neuroepithelial cell (body and fiber)
  YELLOW = the nucleus (the thing that moves)
  TEAL   = cell-cycle phase (ring, G1 / S / G2 / M, "copying DNA")
  GREEN  = a neuron
  PURPLE = kinesin Kif1a (basal motor)
  ORANGE = dynein (apical motor)
  PINK   = actomyosin (zebrafish retina)
  RED    = the open question
  GREY   = ventricle, pia, labels, historical reading, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB4"

CX = -1.8          # x of the single cell in scenes 3 to 6
BIGW = 2.4         # width of the single (zoomed) cell
NR = 0.70          # radius of the single cell's nucleus
Y_AP = -2.1        # nucleus at the apical end
Y_BA = 1.85        # nucleus in the basal ventricular zone (S phase)
RIGHT_OF_CELL = CX + BIGW / 2 + 0.5   # left edge for labels beside the cell
COLS = [-3.0, -1.8, -0.6, 0.6, 1.8, 3.0]


# ---------------------------------------------------------------- helpers
def wall():
    strip = Rectangle(width=9.6, height=0.44, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to([0, -3.22, 0])
    vlab = T("ventricle", 22, GREY).move_to(strip)
    pia = Rectangle(width=9.6, height=0.16, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([0, 3.16, 0])
    plab = T("pia", 24, GREY).move_to([5.5, 3.16, 0])
    return VGroup(strip, vlab, pia, plab)


def side_labels():
    a = T("apical", 26, GREY).move_to([-5.3, -2.5, 0])
    b = T("basal", 26, GREY).move_to([-5.3, 2.5, 0])
    return VGroup(a, b)


def cell(x, color=BLUE, width=1.0):
    c = RoundedRectangle(corner_radius=0.4, width=width, height=5.8, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.13).move_to([x, 0, 0])
    c.set_z_index(0)
    return c


def nuc(x, y, r=0.34):
    n = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85).move_to([x, y, 0])
    n.set_z_index(3)
    return n


def dumb(x, y, r=0.18, dx=0.22):
    g = VGroup(*[Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85)
                 .move_to([x + d, y, 0]) for d in (-dx, dx)])
    g.set_z_index(3)
    return g


def ring_of(x, y, r=0.34):
    c = Circle(radius=r + 0.09, stroke_color=TEAL, stroke_width=4).move_to([x, y, 0])
    c.set_z_index(4)
    return c


def bigcell():
    return cell(CX, width=BIGW)


def bignuc(y):
    return nuc(CX, y, NR)


def bigdumb(y):
    return dumb(CX, y, r=0.38, dx=0.44)


def beside(mob, y):
    """Place mob with its left edge just right of the big cell."""
    return mob.move_to([RIGHT_OF_CELL + mob.width / 2, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


RING_C = np.array([4.1, 0.2, 0])
RING_R = 1.3
# (name, start deg, span deg clockwise)
PHASES = [("G1", 60, -120), ("S", -60, -110), ("G2", -170, -100), ("M", 90, -30)]


def ring_arcs():
    arcs = {}
    for name, a0, span in PHASES:
        arcs[name] = Arc(radius=RING_R, start_angle=np.deg2rad(a0), angle=np.deg2rad(span), arc_center=RING_C,
                         stroke_color=TEAL, stroke_width=9).set_stroke(opacity=0.35)
    return arcs


def ring_labels():
    out = {}
    for name, a0, span in PHASES:
        mid = np.deg2rad(a0 + span / 2)
        p = RING_C + (RING_R + 0.6) * np.array([np.cos(mid), np.sin(mid), 0])
        out[name] = T(name, 28, TEAL, weight=BOLD).move_to(p)
    return out


def pt_on_ring(deg):
    return RING_C + RING_R * np.array([np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg)), 0])


# Additional notation: GOLD = permanent lineage mark; BLUE labelled chip = intermediate progenitor.

def neuron(x, y, r=0.28):
    return Circle(radius=r, stroke_color=GREEN, stroke_width=3,
                  fill_color=GREEN, fill_opacity=0.9).move_to([x, y, 0]).set_z_index(5)


def heading(text):
    return T(text, 30, TEXT, font=TITLE_FONT).move_to([0, 3.45, 0])


def opening():
    return VGroup(wall(), bigcell(), bignuc(Y_AP))


def roles():
    return VGroup(bchip("makes most cortical neurons", BLUE, 26).move_to([3.1, 1.25, 0]),
                  bchip("guides migrating neurons", GREEN, 26).move_to([3.1, -0.25, 0]))


class S00Title(TitleCard):
    LESSON = "The ventricular zone: radial glia as stem cells"
    TITLE = "Radial Glia Make Cortical Neurons"


class S01Puzzle(SpokenScene):
    def construct(self):
        stage = opening()
        n = neuron(CX + BIGW / 2, -0.6)
        labels = roles()
        scope = T("embryonic rodent cortex", 24, GREY).move_to([2.8, 2.65, 0])
        self.add(stage, n, scope)
        self.at("make most cortical neurons")
        self.play(FadeIn(labels[0]), run_time=0.6)
        self.at("guide migrating neurons")
        self.play(FadeIn(labels[1]), n.animate.set_y(1.8), run_time=1.1)
        self.at("main source")
        self.play(Indicate(stage[2], color=YELLOW), run_time=0.6)
        self.at("see the scaffold")
        self.play(Indicate(stage[1], color=BLUE, scale_factor=1.03), run_time=0.7)
        definition = T("progenitor: a cell that still divides", 26, BLUE).move_to([2.7, -1.5, 0])
        self.at("is a progenitor")
        self.play(FadeIn(definition), run_time=0.6)
        self.at("still divides")
        d = bigdumb(Y_AP)
        self.play(ReplacementTransform(stage[2], d), run_time=0.6)
        self.at("Its daughters")
        keep = bignuc(Y_AP)
        baby = neuron(CX + BIGW / 2, Y_AP)
        self.play(ReplacementTransform(d, keep), FadeIn(baby, scale=0.4), run_time=0.6)
        self.at("become neurons")
        self.play(baby.animate.set_y(-0.8), run_time=0.8)
        self.at("keeps making more")
        self.play(Indicate(keep, color=YELLOW), run_time=0.6)
        self.finish()


class S05Fate(SpokenScene):
    def construct(self):
        # Three persistent panel frames, with one animated experiment in focus at a time.
        xs = [-4.35, 0, 4.35]
        names = ["Mouse sorting\n& fate mapping", "Rat lineage\nimaging", "Rat recording\n& dye filling"]
        panels = VGroup(*[RoundedRectangle(width=4.05, height=5.5, corner_radius=0.15,
                            stroke_color=GREY, stroke_opacity=0.45).move_to([x, -0.1, 0]) for x in xs])
        titles = VGroup(*[T(name, 24, GREY).move_to([x, 2.15, 0]) for x, name in zip(xs, names)])
        self.add(heading("How do we know?"), panels, titles)
        rg = bchip("radial glia", BLUE, 24).move_to([-4.35, 0.85, 0])
        dish = Arc(radius=1.2, start_angle=PI, angle=PI, stroke_color=GREY).stretch(0.4, 1).move_to([-4.35, -1.4, 0])
        ns = VGroup(neuron(-4.8, -0.8), neuron(-3.9, -0.8))
        culture = T("culture", 24, GREY).move_to([-4.35, -2.15, 0])
        self.at("sorted radial glia")
        self.play(FadeIn(rg), titles[0].animate.set_color(TEXT), run_time=0.5)
        self.at("made neurons in culture")
        self.play(Create(dish), TransformFromCopy(rg, ns), FadeIn(culture), run_time=0.7)
        marked = VGroup(neuron(-4.9, -0.7), neuron(-3.8, -0.7))
        for n in marked:
            n.add(Dot(n.get_center(), radius=0.09, color=GOLD))
        in_vivo = T("in the animal\npermanent mark", 23, GOLD).move_to([-4.35, -1.9, 0])
        badge = Dot(rg.get_right() + LEFT * 0.17, radius=0.09, color=GOLD)
        self.at("Fate mapping")
        self.play(FadeOut(dish), FadeOut(ns), FadeOut(culture), FadeIn(badge), FadeIn(in_vivo), run_time=0.5)
        self.at("marked their descendants")
        self.play(TransformFromCopy(badge, marked), run_time=0.7)
        result = T("nearly all cortical\nprojection neurons", 22, GREEN).move_to([-4.35, -2.25, 0])
        self.at("Nearly all cortical")
        self.play(in_vivo.animate.set_y(-1.4), FadeIn(result), run_time=0.5)
        c = cell(-0.3, width=0.65).scale([1, 0.52, 1]).move_to([-0.3, -0.3, 0])
        nu = nuc(-0.3, -1.55, 0.25)
        self.at("In filmed rat slices")
        self.play(VGroup(rg, badge, marked, in_vivo, result).animate.set_opacity(0.6),
                  titles[1].animate.set_color(TEXT), FadeIn(c), FadeIn(nu), run_time=0.5)
        dd = dumb(-0.3, -1.55)
        daughter = neuron(0.025, -1.55, 0.22)
        self.at("divided and made neurons")
        self.play(ReplacementTransform(nu, dd), run_time=0.35)
        self.play(ReplacementTransform(dd, nuc(-0.3, -1.55, 0.25)), FadeIn(daughter), run_time=0.4)
        self.at("moved along")
        self.play(daughter.animate.set_y(0.8), run_time=1.0)
        filled = cell(4.35, width=0.7).scale([1, 0.52, 1]).move_to([4.35, -0.35, 0])
        soma = nuc(4.35, -0.8, 0.25)
        electrode = Line([5.8, 0.65, 0], [4.6, -0.7, 0], stroke_color=GREY, stroke_width=5)
        self.at("recordings also tied")
        self.play(titles[2].animate.set_color(TEXT), FadeIn(soma), Create(electrode), run_time=0.5)
        self.at("dividing precursors")
        self.play(ReplacementTransform(soma, dumb(4.35, -0.8)), run_time=0.5)
        self.at("to radial glial shape")
        self.play(DrawBorderThenFill(filled), run_time=0.8)
        self.finish()


class S08Routes(SpokenScene):
    def construct(self):
        head = heading("Rodent example lineages")
        direct = T("direct", 28, BLUE).move_to([-3.3, 2.5, 0])
        indirect = T("indirect", 28, BLUE).move_to([3.0, 2.5, 0])
        a = bchip("radial glia", BLUE, 24).move_to([-3.3, 1.55, 0])
        b = bchip("radial glia", BLUE, 24).move_to([3.0, 1.55, 0])
        self.add(head)
        self.at("two routes")
        self.play(FadeIn(direct), FadeIn(indirect), FadeIn(a), FadeIn(b), run_time=0.6)
        drg = bchip("radial glia", BLUE, 24).move_to([-4.85, 0.1, 0])
        dn = bchip("neuron", GREEN, 24).move_to([-1.9, 0.1, 0])
        da = VGroup(arr(a.get_bottom(), drg.get_top()), arr(a.get_bottom(), dn.get_top()))
        self.at("Direct neurogenesis")
        self.play(Create(da), TransformFromCopy(a, drg), TransformFromCopy(a, dn), run_time=0.8)
        irg = bchip("radial glia", BLUE, 24).move_to([1.35, 0.1, 0])
        ip = bchip("intermediate\nprogenitor", BLUE, 22).move_to([4.65, 0.1, 0])
        ia = VGroup(arr(b.get_bottom(), irg.get_top()), arr(b.get_bottom(), ip.get_top()))
        self.at("Indirect neurogenesis")
        self.play(Create(ia), TransformFromCopy(b, irg), TransformFromCopy(b, ip), run_time=0.8)
        # A compact physical inset makes loss of ventricular contact visible.
        foot = Line([3.5, -2.8, 0], [5.9, -2.8, 0], color=GREY)
        contact = Line([4.65, -1.35, 0], [4.65, -2.8, 0], color=BLUE, stroke_width=3)
        progenitor = Circle(radius=0.25, color=BLUE, fill_opacity=0.3).move_to([4.65, -1.35, 0])
        vl = T("ventricle", 22, GREY).move_to([4.65, -3.15, 0])
        self.at("leaves the ventricle")
        self.play(FadeIn(foot), FadeIn(vl), Create(contact), FadeIn(progenitor), run_time=0.4)
        self.play(FadeOut(contact), progenitor.animate.set_y(-0.75), run_time=0.6)
        svz = T("SVZ", 24, GREY).move_to([5.75, -0.85, 0])
        self.at("divides in the subventricular zone")
        self.play(FadeIn(svz), ReplacementTransform(progenitor, dumb(4.65, -0.75)), run_time=0.6)
        # Reset the physical inset before restoring the completed family tree.
        self.at("usually into two neurons")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in [head, direct, indirect, a, b, drg, dn, da, irg, ip, ia]], run_time=0.25)
        two = VGroup(bchip("neuron", GREEN, 22).move_to([3.3, -1.55, 0]),
                     bchip("neuron", GREEN, 22).move_to([5.4, -1.55, 0]))
        branches = VGroup(*[arr(ip.get_bottom(), n.get_top()) for n in two])
        note = T("Usually two in rodents; yields vary", 22, GREY).move_to([2.8, -2.4, 0])
        self.play(Create(branches), FadeIn(two), FadeIn(note), run_time=0.6)
        self.at("without spending")
        self.play(Indicate(irg[1:], color=BLUE), Indicate(drg[1:], color=BLUE), run_time=0.6)
        self.at("Human cortex")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.35)
        h = heading("Human cortex: outer radial glia")
        v = Line([-5.8, -2.65, 0], [5.8, -2.65, 0], color=GREY)
        vlabel = T("ventricle", 24, GREY).move_to([-4.5, -3.0, 0])
        outer = VGroup(Circle(radius=0.4, color=BLUE, fill_opacity=0.3).move_to([-2, 0.4, 0]),
                       Line([-2, 0.8, 0], [-2, 2.6, 0], color=BLUE, stroke_width=4))
        ol = T("outer radial glia", 26, BLUE).move_to([-2, -0.55, 0])
        self.play(FadeIn(h), FadeIn(v), FadeIn(vlabel), FadeIn(outer), FadeIn(ol), run_time=0.6)
        self.at("feed further progenitors")
        more = bchip("further progenitors", BLUE, 26).move_to([2.8, 0.4, 0])
        self.play(GrowArrow(arr([-1.4, 0.4, 0], more.get_left())), FadeIn(more), run_time=0.7)
        self.finish()


class S09Niche(SpokenScene):
    def construct(self):
        c, n = bigcell(), bignuc(Y_AP)
        v = Rectangle(width=9.6, height=0.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.15).move_to([0, -3.15, 0])
        pia = Line([-4.8, 3.1, 0], [4.8, 3.1, 0], color=GREY, stroke_width=5)
        bm = Line([-4.8, 2.92, 0], [4.8, 2.92, 0], color=GREY, stroke_width=3)
        feet = VGroup(Line([CX-0.8,-2.9,0],[CX+0.8,-2.9,0],color=BLUE,stroke_width=8),
                      Line([CX-0.8,2.9,0],[CX+0.8,2.9,0],color=BLUE,stroke_width=8))
        self.add(c,n,v,pia,bm)
        self.at("touch two niches")
        self.play(Create(feet), run_time=0.6)
        ap = VGroup(T("apical foot", 26, BLUE), T("ventricle + CSF", 26, GREY)).arrange(DOWN,buff=0.2).move_to([2.8,-2.2,0])
        self.at("The apical foot")
        self.play(FadeIn(ap), Indicate(feet[0], color=BLUE, scale_factor=1.1), run_time=0.6)
        gf = VGroup(*[Dot([x,-3.15,0],radius=0.075,color=TEAL) for x in [-3.8,-2.9,-1.8,-0.8,0.2,1.2]])
        gl = T("mouse CSF: growth factors", 25, TEAL).move_to([2.6,0,0])
        self.at("In mouse")
        self.play(FadeIn(gl), FadeIn(gf), run_time=0.5)
        self.at("support proliferation")
        self.play(ReplacementTransform(n, bigdumb(Y_AP)), run_time=0.7)
        ba = VGroup(T("basal foot",26,BLUE),T("basement membrane",26,GREY),T("beneath the pia",24,GREY)).arrange(DOWN,buff=0.18).move_to([2.8,1.9,0])
        self.at("The basal foot")
        self.play(FadeIn(ba), Indicate(feet[1],color=BLUE,scale_factor=1.1), run_time=0.7)
        baby = Circle(radius=0.3,color=BLUE,fill_opacity=0.3).move_to([0,-2.4,0])
        tether = Line([0,-2.7,0],[0,-2.9,0],color=BLUE,stroke_width=4)
        self.at("A daughter that leaves")
        self.play(FadeOut(gl),FadeIn(baby),Create(tether),run_time=0.5)
        self.at("loses apical contact")
        self.play(FadeOut(tether),baby.animate.move_to([0.2,-0.3,0]),run_time=0.8)
        self.finish()


class S10Output(SpokenScene):
    def construct(self):
        head = heading("Daughters that keep dividing")
        p = bchip("P: remain progenitors", BLUE, 28).move_to([-3.2,1.8,0])
        q = bchip("Q: quit the cycle", GREEN,28).move_to([3.2,1.8,0])
        eq = M("P + Q = 1",32).move_to([0,0.55,0])
        self.add(head)
        self.at("Call that fraction P")
        self.play(FadeIn(p),run_time=0.5)
        self.at("the fraction that quits")
        self.play(FadeIn(q),run_time=0.5)
        self.at("P plus Q")
        self.play(FadeIn(eq),run_time=0.5)
        def pool(count):
            return VGroup(*[Circle(radius=0.25,color=BLUE,fill_opacity=0.4).move_to([(i-(count-1)/2)*0.85,-1.55,0]) for i in range(count)])
        cells = pool(3)
        status = M("Q < 0.5",30).move_to([0,-0.45,0])
        self.at("Below Q equals")
        self.play(FadeIn(status),FadeIn(cells),run_time=0.4)
        self.at("the pool grows")
        self.play(Transform(cells,pool(5)),run_time=0.7)
        self.at("At 0 .5")
        self.play(Transform(status,M("Q = 0.5",30).move_to(status)),Transform(cells,pool(3)),run_time=0.45)
        self.at("it holds steady")
        # Renew the three members while keeping the pool count fixed.
        self.play(Indicate(cells,color=BLUE,scale_factor=1.05),run_time=0.55)
        self.at("Above it")
        self.play(Transform(status,M("Q > 0.5",30).move_to(status)),Transform(cells,pool(3)),run_time=0.4)
        self.at("it shrinks")
        self.play(Transform(cells,pool(2)),run_time=0.6)
        ip = bchip("Intermediate progenitors count in P",BLUE,26).move_to([0,-2.8,0])
        self.at("An intermediate progenitor")
        self.play(FadeIn(ip),run_time=0.6)
        self.at("In mouse cortex")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.4)
        self.add(heading("Mouse cortex: a longer cell cycle"))
        # Constant arc length per unit time: growing G1 increases total circumference.
        def clock(g1):
            spans = [g1, 1.0, 0.8, 0.3]
            total = sum(spans)
            rad = total / 3.1
            arcs, labs = VGroup(), VGroup()
            angle = PI/2
            for name,span in zip(["G1","S","G2","M"],spans):
                sweep = -TAU*span/total
                arcs.add(Arc(radius=rad,start_angle=angle,angle=sweep,arc_center=[-1.3,0,0],
                             stroke_color=TEAL,stroke_width=10,stroke_opacity=1 if name=="G1" else 0.45))
                mid = angle+sweep/2
                labs.add(T(name,26,TEAL).move_to([-1.3+(rad+0.4)*np.cos(mid),(rad+0.4)*np.sin(mid),0]))
                angle += sweep
            return VGroup(arcs,labs)
        ring = clock(1.3)
        self.play(Create(ring),run_time=0.6)
        self.at("cell cycle lengthens")
        self.play(Transform(ring,clock(2.8)),run_time=0.8)
        self.at("mostly in G1")
        label = T("added time: mostly G1",27,TEAL).move_to([3.4,0.4,0])
        self.play(FadeIn(label),run_time=0.5)
        self.finish()


class S03Lift(SpokenScene):
    def construct(self):
        # VZ-only view: the upper edge is basal VZ, not the pial surface.
        low = Line([-4.8,-2.9,0],[5.9,-2.9,0],color=GREY,stroke_width=5)
        ap = T("apical / ventricle",24,GREY).move_to([-3.6,-3.3,0])
        basal = T("basal VZ",24,GREY).move_to([-3.6,3.15,0])
        cells = VGroup(*[VGroup(cell(x),nuc(x,y)) for x,y in zip([-2.4,-1.2,0,1.2],[-1.7,1.7,-0.2,0.9])])
        self.add(low,ap,basal,cells)
        self.at("Picture a lift")
        c, main = bigcell(),bignuc(Y_AP)
        self.play(ReplacementTransform(cells,VGroup(c,main)),run_time=0.7)
        shaft = beside(T("cell = shaft",28,BLUE),1.7)
        car = beside(T("nucleus = car",28,YELLOW),0.8)
        self.at("The shaft is the cell")
        self.play(FadeIn(shaft),run_time=0.4)
        self.at("the car is the nucleus")
        self.play(FadeIn(car),run_time=0.4)
        arcs, labs = ring_arcs(),ring_labels()
        ring = VGroup(*arcs.values(),*labs.values(),T("cell cycle",24,GREY).move_to(RING_C))
        marker = Dot(pt_on_ring(60),radius=0.13,color=YELLOW)
        def lit(name):
            return [arcs[k].animate.set_stroke(opacity=1 if k==name else 0.35) for k in arcs]
        self.at("In G1")
        self.play(FadeOut(shaft),FadeOut(car),FadeIn(ring),FadeIn(marker),run_time=0.4)
        self.at("moves basally")
        self.play(main.animate.set_y(Y_BA),MoveAlongPath(marker,arcs["G1"]),*lit("G1"),run_time=0.9,rate_func=linear)
        self.at("S phase")
        rr = ring_of(CX,Y_BA,NR)
        self.play(Create(rr),MoveAlongPath(marker,arcs["S"]),*lit("S"),run_time=0.3,rate_func=linear)
        self.at("copies DNA")
        dna = T("copying DNA",25,TEAL).move_to([0.8,2.8,0])
        self.play(FadeIn(dna),run_time=0.4)
        self.at("In G2")
        self.play(FadeOut(dna),FadeOut(rr),MoveAlongPath(marker,arcs["G2"]),
                  main.animate.set_y(Y_AP),*lit("G2"),run_time=1.0,rate_func=linear)
        self.at("Mitosis happens")
        dd = bigdumb(Y_AP)
        self.play(ReplacementTransform(main,dd),MoveAlongPath(marker,arcs["M"]),*lit("M"),run_time=0.8)
        self.at("Nuclei at different heights")
        layer = VGroup(*[VGroup(cell(x),nuc(x,y)) for x,y in zip([-2.4,-1.2,0,1.2],[-1.7,1.7,-0.2,0.9])])
        self.play(FadeOut(ring),FadeOut(marker),FadeOut(c),FadeOut(dd),FadeIn(layer),run_time=0.6)
        self.at("single cell layer")
        tag = VGroup(T("one cell layer",28,BLUE),T("pseudostratified",26,GREY)).arrange(DOWN,buff=0.2).move_to([4.35,0.2,0])
        self.play(FadeIn(tag),run_time=0.5)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        stage = opening()
        n = neuron(CX+BIGW/2,0.0)
        labels = roles()
        scope = T("embryonic rodent cortex",24,GREY).move_to([2.8,2.65,0])
        self.add(stage,n,scope)
        self.at("Keep the main finding")
        self.play(Indicate(stage[1],color=BLUE,scale_factor=1.02),run_time=0.6)
        self.at("guide migrating neurons")
        self.play(FadeIn(labels[1]),n.animate.set_y(1.8),run_time=0.8)
        self.at("make most of them")
        baby = neuron(CX+BIGW/2,Y_AP)
        division = bigdumb(Y_AP)
        self.play(ReplacementTransform(stage[2],division),run_time=0.3)
        self.play(ReplacementTransform(division,bignuc(Y_AP)),FadeIn(baby,scale=0.4),FadeIn(labels[0]),run_time=0.4)
        self.play(baby.animate.set_y(-1.1),run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "In embryonic rodent cortex, radial glia both guide and make most neurons."
