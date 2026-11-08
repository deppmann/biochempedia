"""Plant body and growth: how meristems keep a plant growing  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = new cells / the zone of division / the rate of new cells
  ORANGE = elongation / the zone of elongation / final cell length
  GREEN  = maturation / mature cells
  TEAL   = water in the vacuoles
  YELLOW = the result: root growth rate (equation, bars, tip movement)
  RED    = reserved for changed conditions (unused)
  WOOD   = secondary xylem / wood
  PINK   = phloem / transported sugars and amino acids
  BROWN  = cork; BLUE also marks dividing cambia / meristems
  GREY   = root cap, outlines, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
TEAL_W = "#3FB8C0"
BASE_X = 6.2


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def mix(c1, c2, a):
    return interpolate_color(ManimColor(c1), ManimColor(c2), a)


# ---------------------------------------------------------------------------------------------
# schematic root strip: tip at the LEFT, root cap, three zones (not to scale)
# ---------------------------------------------------------------------------------------------
class Strip:
    X0 = -5.2
    H = 2.4
    CAP = 0.9
    DIV = [0.7, 0.7, 0.7]
    EL = [0.7, 0.9, 1.1, 1.2]
    MAT = [1.7, 1.7]

    def __init__(self, y=0.5, colored=False, vac=0.2, hairs=False):
        H = self.H
        x = self.X0
        self.cap = RoundedRectangle(corner_radius=0.3, width=self.CAP, height=H * 0.9, stroke_color=GREY,
                                    stroke_width=3, fill_color=GREY, fill_opacity=0.25).move_to([x + self.CAP / 2, y, 0])
        x += self.CAP
        self.x_div0 = x
        self.div, self.divlines = VGroup(), VGroup()
        for w in self.DIV:
            r = Rectangle(width=w, height=H, stroke_width=2.5).move_to([x + w / 2, y, 0])
            self.div.add(r)
            self.divlines.add(Line([x + w / 2, y - H / 2, 0], [x + w / 2, y + H / 2, 0], stroke_width=2.5))
            x += w
        self.x_el0 = x
        self.el, self.vacs = VGroup(), VGroup()
        for w in self.EL:
            r = Rectangle(width=w, height=H, stroke_width=2.5).move_to([x + w / 2, y, 0])
            v = RoundedRectangle(corner_radius=0.12, width=w * vac * 3.2 / 3.2, height=H * 0.15 + H * 0.6 * vac,
                                 stroke_width=0, fill_color=TEAL_W, fill_opacity=0.5).move_to(r)
            v.full_w = w * 0.78
            v.full_h = H * 0.75
            self.el.add(r)
            self.vacs.add(v)
            x += w
        self.x_mat0 = x
        self.mat = VGroup()
        for w in self.MAT:
            r = Rectangle(width=w, height=H, stroke_width=2.5).move_to([x + w / 2, y, 0])
            self.mat.add(r)
            x += w
        self.x_end = x
        self.y = y
        self.hairs = VGroup()
        for r in self.mat:
            for k in (-0.4, 0.0, 0.4):
                cx = r.get_center()[0] + k * r.width * 0.9
                self.hairs.add(Line([cx, y + H / 2, 0], [cx, y + H / 2 + 0.45, 0], stroke_width=3.5),
                               Line([cx, y - H / 2, 0], [cx, y - H / 2 - 0.45, 0], stroke_width=3.5))
        self.set_colors(GREY, GREY, GREY)
        if colored:
            self.set_colors(BLUE, ORANGE, GREEN)
        self.hairs.set_color(GREEN)
        self.set_vac(vac)
        self.divlines.set_color(BLUE)
        self.show_hairs = hairs

    def set_colors(self, cd, ce, cm):
        for grp, c in ((self.div, cd), (self.el, ce), (self.mat, cm)):
            for r in grp:
                r.set_stroke(c).set_fill(c, 0.14)

    def set_vac(self, a):
        for v in self.vacs:
            w = v.full_w * (0.25 + 0.75 * a)
            h = v.full_h * (0.25 + 0.75 * a)
            v.become(RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_width=0,
                                      fill_color=TEAL_W, fill_opacity=0.5).move_to(v.get_center()))

    def body(self, with_divlines=True, with_vacs=True, with_hairs=None):
        g = VGroup(self.cap, self.div, self.el, self.mat)
        if with_divlines:
            g.add(self.divlines)
        if with_vacs:
            g.add(self.vacs)
        if with_hairs if with_hairs is not None else self.show_hairs:
            g.add(self.hairs)
        return g

    def zone_center(self, name):
        a, b = {"div": (self.x_div0, self.x_el0), "el": (self.x_el0, self.x_mat0), "mat": (self.x_mat0, self.x_end)}[name]
        return (a + b) / 2, a, b


# ---------------------------------------------------------------------------------------------
# the cell file used in the arithmetic scenes: tip at the left, base fixed at the right
# ---------------------------------------------------------------------------------------------
LONG, SHORT = 2.3, 0.115   # 300 and 15 micrometres at 1 : 20


class CellFile:
    def __init__(self, y=1.45, h=1.8, n_old=2):
        self.y, self.h = y, h
        self.cells = [(ValueTracker(1), LONG) for _ in range(n_old)]

    def add(self, final):
        t = (ValueTracker(0), final)
        self.cells.append(t)
        return t[0]

    def widths(self):
        return [SHORT + (L - SHORT) * v.get_value() for v, L in self.cells]

    def tip_x(self):
        return BASE_X - sum(self.widths())

    def build(self):
        g = VGroup()
        x = BASE_X
        for (v, L), w in zip(self.cells, self.widths()):
            a = v.get_value()
            col = mix(BLUE, ORANGE, a * 2) if a < 0.5 else mix(ORANGE, GREEN, a * 2 - 1)
            g.add(Rectangle(width=w, height=self.h, stroke_color=col, stroke_width=2.5, fill_color=col,
                            fill_opacity=0.2).move_to([x - w / 2, self.y, 0]))
            x -= w
        g.add(RoundedRectangle(corner_radius=0.25, width=0.5, height=self.h * 0.9, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.25).move_to([x - 0.25, self.y, 0]))
        g.add(Line([BASE_X, self.y - self.h / 2 - 0.15, 0], [BASE_X, self.y + self.h / 2 + 0.15, 0],
                   stroke_color=GREY, stroke_width=7))
        return g

    def mob(self):
        return always_redraw(self.build)


def bar_row(label, value, y, color=YELLOW):
    lab = T(label, 24, GREY).move_to([-6.0, y, 0], aligned_edge=LEFT)
    w = max(value * 0.8333, 0.05)
    bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=color, fill_opacity=0.85)
    bar.move_to([-3.4 + w / 2, y, 0])
    txt = M(f"{value:g} mm/day", 24, color).next_to(bar, RIGHT, buff=0.2)
    return lab, bar, txt


def footer(text="illustrative numbers, not a measured species"):
    return T(text, 22, GREY).move_to([0, -3.45, 0])


WOOD = "#BE9A70"
PINK = "#D995CE"
BROWN = "#A77B56"


def heading(text):
    return T(text, 32, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])


def oak():
    """A broad crown, woody trunk and visible root/shoot ends, all schematic."""
    trunk = Polygon([-0.55, -1.1, 0], [0.5, -1.1, 0], [0.28, 1.2, 0], [-0.25, 1.2, 0],
                    stroke_color=WOOD, fill_color=WOOD, fill_opacity=0.25)
    branches = VGroup(*[Line([0, 0.3, 0], [x, y, 0], color=WOOD, stroke_width=7)
                        for x, y in [(-1.4, 1.65), (0, 2.3), (1.5, 1.6)]])
    crown = VGroup(*[Ellipse(width=w, height=h, color=GREEN, fill_opacity=0.12).move_to([x,y,0])
                     for x,y,w,h in [(-1.3,1.6,2.2,1.6), (0,2.1,2.4,1.7), (1.3,1.6,2.3,1.7)]])
    roots = VGroup(*[VMobject(color=GREY, stroke_width=4).set_points_as_corners(
        [[0,-1.0,0],[x*0.45,-1.6,0],[x,-2.3,0]]) for x in [-1.8,0,1.8]])
    return VGroup(trunk, branches, crown, roots)


def tips():
    return VGroup(*[Dot([x,y,0], radius=0.10, color=BLUE)
                    for x,y in [(-1.4,1.65),(0,2.3),(1.5,1.6),(-1.8,-2.3),(0,-2.3),(1.8,-2.3)]])


def meristem_cells():
    return VGroup(*[RoundedRectangle(width=0.75,height=0.75,corner_radius=0.1,
                   color=BLUE,fill_opacity=0.18).move_to([x,y,0])
                   for y in [-0.45,0.45] for x in [-0.9,0,0.9]])


class S00Title(TitleCard):
    LESSON = "Plant body and growth"
    TITLE = "How Meristems Keep a Plant Growing"

    def construct(self):
        title = VGroup(T("How Meristems Keep", 44, font=TITLE_FONT),
                       T("a Plant Growing", 44, font=TITLE_FONT)).arrange(DOWN, buff=0.14).move_to([0,2.5,0])
        tree = oak().scale(0.63).move_to([0,-0.9,0])
        dots = tips().scale(0.63).move_to(tree)
        ring = Ellipse(width=0.8,height=0.3,color=BLUE).move_to([0,-1.0,0])
        self.play(FadeIn(title), FadeIn(tree), run_time=0.7)
        self.play(FadeIn(dots), ring.animate.stretch(1.35,0), run_time=0.6)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        tree = oak().shift(LEFT*3.1)
        title = heading("How Meristems Keep a Plant Growing")
        age = T("300-year-old oak",26,GREY).move_to([-3.1,-3.0,0])
        self.add(tree,title,age)
        self.at("new shoots and wood")
        shoots = tips().shift(LEFT*3.1)
        ring = Ellipse(width=1.05,height=0.42,color=BLUE,stroke_width=5).move_to([-3.1,-0.5,0])
        self.play(FadeIn(shoots),Create(ring),run_time=0.7)
        self.at("regions of dividing cells")
        cells = meristem_cells().move_to([2.8,0.8,0])
        link = arr([-1.5,1.6,0],[1.15,1.0,0],BLUE)
        self.play(GrowArrow(link),FadeIn(cells),run_time=0.7)
        self.at("called meristems")
        lab = T("meristems",32,BLUE,weight=BOLD).move_to([2.8,2.0,0])
        self.play(FadeIn(lab),run_time=0.5)
        self.at("supply new cells")
        splits = VGroup(*[Line(c.get_top(),c.get_bottom(),color=BLUE) for c in cells])
        self.play(LaggedStart(*[Create(l) for l in splits],lag_ratio=0.12),run_time=0.8)
        self.at("keep building their bodies")
        self.play(tree.animate.stretch(1.02,1,about_point=[-3.1,-1.1,0]),run_time=0.7)
        self.at("apical meristems")
        self.play(FadeOut(VGroup(cells,splits,link,lab)),run_time=0.4)
        ap = T("apical meristems\nroot + shoot tips",28,BLUE).move_to([2.7,1.4,0])
        length = arr([0.6,-0.7,0],[0.6,2.4,0],BLUE)
        ll = T("length",28,BLUE).move_to([2.0,-0.4,0])
        self.play(FadeIn(ap),GrowArrow(length),FadeIn(ll),Indicate(shoots,scale_factor=1.4),run_time=0.7)
        self.at("lateral meristems")
        lateral = T("lateral meristems\naround the woody stem",26,BLUE).move_to([2.8,-1.6,0])
        girth = DoubleArrow([-3.95,-0.7,0],[-2.25,-0.7,0],color=BLUE,buff=0)
        gl = T("girth",26,BLUE).next_to(lateral,DOWN,buff=0.3)
        self.play(FadeIn(lateral),GrowArrow(girth),FadeIn(gl),ring.animate.stretch(1.3,0),run_time=0.7)
        self.finish()


class S02Zones(SpokenScene):
    def construct(self):
        st = Strip(y=0.5)
        st.set_vac(0)
        self.add(st.body(with_divlines=False,with_vacs=False),
                 heading("From dividing cells to mature root"),
                 footer("one cell file • schematic, not to scale"))
        def zone(name,text,color):
            cx,a,b=st.zone_center(name)
            return VGroup(Line([a+0.05,-1.1,0],[b-0.05,-1.1,0],color=color,stroke_width=4),
                          T(text,26,color).move_to([cx,-2.0,0]))
        self.at("protective cap")
        cl=T("root cap",24,GREY).move_to([-4.75,2.3,0])
        self.play(FadeIn(cl),Indicate(st.cap),run_time=0.5)
        self.at("small cells divide")
        dz=zone("div","division\nmeristem",BLUE)
        self.play(st.div.animate.set_color(BLUE),FadeIn(dz),
                  LaggedStart(*[Create(l) for l in st.divlines],lag_ratio=0.2),run_time=0.7)
        self.at("zone of elongation")
        ez=zone("el","elongation",ORANGE)
        self.play(st.el.animate.set_color(ORANGE),FadeIn(ez),run_time=0.6)
        self.at("and lengthen")
        # Each cell grows longitudinally from a shortened outline to its full outline.
        full=st.el.copy()
        for c in st.el: c.stretch(0.6,0)
        self.play(Transform(st.el,full),run_time=0.6)
        self.at("water fills their vacuoles")
        vl=T("water fills vacuoles",24,TEAL_W).move_to([0,2.3,0])
        self.add(st.vacs)
        self.play(FadeIn(vl),*[v.animate.stretch(3.1,0).stretch(3.1,1) for v in st.vacs],run_time=1.0)
        self.at("zone of maturation")
        mz=zone("mat","maturation",GREEN)
        self.play(FadeOut(vl),st.mat.animate.set_color(GREEN),FadeIn(mz),run_time=0.6)
        self.at("final types")
        self.play(Indicate(st.mat,color=GREEN,scale_factor=1.03),run_time=0.5)
        self.at("root hairs appear")
        hl=T("root hairs on epidermis",24,GREEN).move_to([4.2,2.6,0])
        self.play(Create(st.hairs),FadeIn(hl),run_time=0.7)
        self.finish()


class S03Rule(SpokenScene):
    def construct(self):
        st=Strip(y=0.5,colored=True,vac=1,hairs=True)
        g=st.body().scale(0.8).move_to([0,-1.0,0])
        self.add(g,footer("one root cell file • schematic"))
        self.at("division supplies cells")
        self.play(Indicate(st.div,color=BLUE),run_time=0.7)
        self.at("elongation sets their length")
        self.play(Indicate(st.el,color=ORANGE),run_time=0.7)
        self.at("steady state")
        ss=T("Steady state • every cell file alike",26,GREY).move_to([0,3.25,0])
        self.play(FadeIn(ss),run_time=0.6)
        self.at("root growth rate equals")
        eq=T("root growth rate =",34,YELLOW,weight=BOLD).move_to([0,2.3,0])
        self.play(FadeIn(eq),run_time=0.5)
        self.at("new cells per file per hour")
        prod=T("new cells / file / hour",30,BLUE).move_to([-2.7,1.3,0])
        self.play(FadeIn(prod),run_time=0.6)
        self.at("times final cell length")
        times=T("×",34,TEXT).move_to([0.6,1.3,0])
        leng=T("final cell length",30,ORANGE).move_to([3.3,1.3,0])
        self.play(FadeIn(times),FadeIn(leng),run_time=0.6)
        self.at("illustrative numbers")
        note=footer("illustrative example • not a measured species")
        self.play(ReplacementTransform(self.mobjects[1],note),run_time=0.5)
        self.at("one cell per hour")
        n1=M("1 cell/h",30,BLUE).move_to([-3.7,-2.6,0])
        self.play(FadeIn(n1),run_time=0.5)
        self.at("times 300 micrometers")
        n2=M("× 300 µm",30,ORANGE).move_to([-0.4,-2.6,0])
        self.play(FadeIn(n2),run_time=0.5)
        self.at("gives 300")
        n3=M("= 300 µm/h",30,YELLOW).move_to([3.3,-2.6,0])
        self.play(FadeIn(n3),run_time=0.5)
        self.at("not from a measured species")
        self.play(Indicate(note,scale_factor=1.02),run_time=0.7)
        self.finish()


class S04Normal(SpokenScene):
    def construct(self):
        self.add(heading("A trunk grows from its cambia"))
        rings=VGroup(*[Circle(radius=r,color=c,fill_color=c,fill_opacity=1,stroke_width=3)
                       for r,c in [(2.25,BROWN),(2.0,PINK),(1.75,BLUE),(1.58,WOOD)]]).move_to([-2.4,-0.2,0])
        self.add(rings,T("trunk cross-section",24,GREY).move_to([-2.4,-2.9,0]))
        self.at("vascular cambium")
        vc=T("vascular cambium",28,BLUE).move_to([3.0,2.0,0])
        pointer=arr([1.0,1.8,0],[-0.75,0.3,0],BLUE)
        self.play(FadeIn(vc),GrowArrow(pointer),Indicate(rings[2],scale_factor=1.03),run_time=0.6)
        self.at("secondary xylem inward")
        inward=arr([0.9,0.8,0],[-1.4,0.0,0],WOOD)
        xl=T("secondary xylem\ninward",26,WOOD).move_to([3.0,0.8,0])
        self.play(GrowArrow(inward),FadeIn(xl),rings[3].animate.scale(1.05),run_time=0.6)
        self.at("secondary phloem outward")
        outward=arr([-0.6,-0.6,0],[1.0,-1.1,0],PINK)
        pl=T("secondary phloem\noutward",26,PINK).move_to([3.0,-1.0,0])
        self.play(GrowArrow(outward),FadeIn(pl),rings[1].animate.scale(1.035),run_time=0.6)
        self.at("is wood")
        wood=T("wood",30,WOOD,weight=BOLD).move_to([-2.4,-0.2,0])
        self.play(FadeIn(wood),run_time=0.5)
        self.at("a different meristem")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.5)
        self.add(heading("Magnified radial strip"),
                 T("inside ←",24,GREY).move_to([-5.2,2.3,0]),
                 T("→ outside",24,GREY).move_to([5.2,2.3,0]))
        # Tissue order from inside to outside. All strips share one radial axis.
        bands=VGroup()
        for a,b,c in [(-5.8,-2.4,WOOD),(-2.4,-2.15,BLUE),(-2.15,0.3,PINK),
                      (0.3,2.3,GREEN),(2.3,2.55,BLUE),(2.55,5.8,BROWN)]:
            bands.add(Rectangle(width=b-a,height=1.7,color=c,fill_color=c,fill_opacity=0.2).move_to([(a+b)/2,0.1,0]))
        labs=VGroup(T("wood",24,WOOD).move_to([-4.1,0.1,0]),
                    T("secondary\nphloem",24,PINK).move_to([-0.9,0.1,0]))
        vcl=T("vascular\ncambium",22,BLUE).move_to([-2.3,-1.55,0])
        self.play(FadeIn(bands[:3]),FadeIn(labs),FadeIn(vcl),run_time=0.5)
        self.at("the cork cambium")
        ccl=T("cork cambium",24,BLUE).move_to([2.4,1.65,0])
        self.play(FadeIn(bands[4]),FadeIn(ccl),run_time=0.5)
        self.at("makes cork outward")
        cork=T("cork",26,BROWN).move_to([4.15,0.1,0])
        ca=arr([2.7,1.0,0],[4.8,1.0,0],BROWN,w=3)
        self.play(FadeIn(bands[5]),FadeIn(cork),GrowArrow(ca),run_time=0.5)
        self.at("and living")
        ph=T("living\nphelloderm",23,GREEN).move_to([1.3,0.1,0])
        pa=arr([2.15,1.0,0],[0.55,1.0,0],GREEN,w=3)
        self.play(FadeIn(bands[3]),FadeIn(ph),GrowArrow(pa),run_time=0.5)
        self.at("these form the periderm")
        per=VGroup(Line([0.3,-1.0,0],[5.8,-1.0,0],color=GREY,stroke_width=4),
                   T("periderm",26,TEXT).move_to([3.1,-1.5,0]))
        self.play(FadeIn(per),run_time=0.5)
        self.at("replacing the epidermis")
        ep=T("replaces epidermis",24,GREY).move_to([3.1,-2.1,0])
        self.play(FadeIn(ep),run_time=0.5)
        self.at("bark is everything outside")
        bark=VGroup(Line([-2.1,-2.7,0],[5.8,-2.7,0],color=PINK,stroke_width=4),
                    T("bark: outside the vascular cambium",24,PINK).move_to([1.8,-3.2,0]))
        self.play(FadeIn(bark),run_time=0.6)
        self.at("includes living phloem")
        self.play(Indicate(bands[2],color=PINK,scale_factor=1.03),run_time=0.6)
        self.finish()


def plant():
    stem=RoundedRectangle(width=0.6,height=3.4,corner_radius=0.12,color=GREEN,fill_opacity=0.1)
    leaves=VGroup(Ellipse(width=2.0,height=0.9,color=GREEN,fill_opacity=0.15).rotate(0.45).move_to([1,1.1,0]),
                  Ellipse(width=2.0,height=0.9,color=GREEN,fill_opacity=0.15).rotate(-0.45).move_to([-1,0.4,0]))
    roots=VGroup(*[Line([0,-1.7,0],[x,-2.6,0],color=GREY,stroke_width=4) for x in [-1.3,0,1.3]])
    return VGroup(stem,leaves,roots)


def tissue_cells(color):
    return VGroup(RoundedRectangle(width=0.55,height=1.1,corner_radius=0.1,color=color,fill_opacity=0.15),
                  Circle(radius=0.3,color=color,fill_opacity=0.15).shift(RIGHT*0.95),
                  Polygon([1.5,-0.45,0],[2.15,-0.25,0],[2.0,0.5,0],[1.5,0.4,0],color=color,fill_opacity=0.15))


class S05Block(SpokenScene):
    def construct(self):
        p=plant().move_to([-3.7,-0.3,0])
        self.add(p,heading("Tissues connect the growing plant"))
        self.at("new cells build tissues")
        xs=tissue_cells(WOOD).move_to([2.5,1.1,0])
        ps=tissue_cells(PINK).move_to([2.5,-0.6,0])
        self.play(FadeIn(xs),FadeIn(ps),run_time=0.7)
        self.at("xylem and phloem")
        xl=T("xylem",28,WOOD).move_to([2.5,2.15,0])
        pl=T("phloem",28,PINK).move_to([2.5,-1.65,0])
        self.play(FadeIn(xl),FadeIn(pl),run_time=0.6)
        self.at("several cell types")
        types=T("several cell types in each tissue",24,GREY).move_to([2.5,-2.65,0])
        self.play(FadeIn(types),Indicate(xs),Indicate(ps),run_time=0.7)
        self.at("connect plant organs")
        paths=VGroup()
        for dx,col in [(-0.12,WOOD),(0.12,PINK)]:
            paths.add(VMobject(color=col,stroke_width=5).set_points_as_corners(
                [[-4.7+dx,-2.7,0],[-3.7+dx,-1.9,0],[-3.7+dx,0.8,0],[-2.7+dx,1.3,0]]))
            paths.add(Line([-3.7+dx,0.1,0],[-4.8+dx,0.4,0],color=col,stroke_width=5))
        self.play(Create(paths),run_time=0.7)
        self.at("xylem carries water")
        water=T("water",26,TEAL_W).move_to([-5.7,1.7,0])
        wa=arr([-4.25,-1.5,0],[-4.25,1.0,0],TEAL_W,w=4)
        self.play(FadeIn(water),GrowArrow(wa),run_time=0.6)
        self.at("phloem carries sugars")
        sugar=T("sugars + amino acids",25,PINK).move_to([-3.5,-3.3,0])
        packet=Dot([-2.8,1.2,0],radius=0.09,color=PINK)
        self.play(FadeIn(sugar),FadeIn(packet),run_time=0.3)
        self.play(packet.animate.move_to([-3.58,0.2,0]),run_time=0.6)
        self.play(packet.animate.move_to([-3.58,-1.8,0]),run_time=0.6)
        self.at("vascular tissue system")
        system=T("vascular tissue system",32,TEXT).move_to([2.5,-2.65,0])
        self.play(ReplacementTransform(types,system),FadeOut(packet),run_time=0.6)
        self.finish()


class S06Halve(SpokenScene):
    def construct(self):
        self.add(heading("A leaf gains carbon and loses water"))
        # Eudicot cross-section: upper surface, palisade, spongy layer and lower stoma.
        upper=Rectangle(width=10.8,height=0.3,color=GREEN,fill_opacity=0.15).move_to([0,2.3,0])
        lower=VGroup(Line([-5.4,-1.5,0],[-0.65,-1.5,0],color=GREEN,stroke_width=8),
                     Line([0.65,-1.5,0],[5.4,-1.5,0],color=GREEN,stroke_width=8))
        mes=VGroup(*[RoundedRectangle(width=1.0,height=1.25,corner_radius=0.18,color=GREEN,fill_opacity=0.1).move_to([x,1.45,0])
                     for x in [-4.6,-3.3,-2.0,-0.7,0.6,1.9,3.2,4.5]])
        spongy=VGroup(*[Ellipse(width=1.35,height=0.65,color=GREEN,fill_opacity=0.1).rotate(a).move_to([x,y,0])
                        for x,y,a in [(-4.4,-0.35,0.3),(-2.6,-0.7,-0.3),(-1.1,-0.2,0.4),(2.8,-0.6,0.2),(4.5,-0.1,-0.4)]])
        vein=VGroup(Ellipse(width=1.7,height=1.0,color=GREY).move_to([1.1,-0.05,0]),
                    RoundedRectangle(width=0.95,height=0.32,corner_radius=0.1,color=WOOD,fill_opacity=0.4).move_to([1.1,0.18,0]),
                    RoundedRectangle(width=0.95,height=0.32,corner_radius=0.1,color=PINK,fill_opacity=0.4).move_to([1.1,-0.25,0]))
        self.add(upper,lower,mes,spongy,vein)
        self.at("veins carry both tissues")
        vl=T("vein: xylem + phloem",24,TEXT).move_to([3.1,-2.2,0])
        ptr=arr([2.5,-1.9,0],[1.5,-0.65,0],GREY,w=3)
        self.play(FadeIn(vl),GrowArrow(ptr),run_time=0.5)
        self.at("chloroplasts in the mesophyll")
        chl=VGroup(*[Ellipse(width=0.22,height=0.12,color=GREEN,fill_opacity=0.8).move_to(c.get_center()+[dx,dy,0])
                     for c in mes for dx,dy in [(-0.25,0.25),(0.25,-0.25)]])
        ml=T("mesophyll + chloroplasts",24,GREEN).move_to([-2.9,-2.2,0])
        self.play(FadeIn(chl),FadeIn(ml),run_time=0.6)
        self.at("capture light")
        light=VGroup(*[arr([x,3.0,0],[x,2.55,0],YELLOW,w=3,tip=0.12) for x in [-3,0,3]])
        self.play(GrowArrow(light[0]),GrowArrow(light[1]),GrowArrow(light[2]),run_time=0.5)
        self.at("airspaces connect to stomata")
        air=T("air spaces",24,GREY).move_to([-3.4,0.35,0])
        path=VMobject(color=GREY,stroke_width=3).set_points_as_corners([[-2.2,0.2,0],[-1.5,-0.75,0],[0,-0.8,0],[0,-1.55,0]])
        guard=VGroup(Ellipse(width=0.45,height=0.65,color=GREEN,fill_opacity=0.4).move_to([-0.47,-1.5,0]),
                     Ellipse(width=0.45,height=0.65,color=GREEN,fill_opacity=0.4).move_to([0.47,-1.5,0]))
        self.play(FadeIn(air),Create(path),FadeIn(guard),run_time=0.7)
        self.at("pores opened and closed")
        gl=T("guard cells / stoma",24,GREEN).move_to([0,-2.8,0])
        self.play(FadeIn(gl),guard[0].animate.shift(RIGHT*0.25),guard[1].animate.shift(LEFT*0.25),run_time=0.5)
        self.at("an open stoma")
        self.play(guard[0].animate.shift(LEFT*0.25),guard[1].animate.shift(RIGHT*0.25),
                  FadeOut(gl),FadeOut(vl),FadeOut(ptr),FadeOut(ml),FadeOut(path),run_time=0.5)
        self.at("carbon dioxide in")
        co=VGroup(Line([-1.5,-3.0,0],[-0.13,-1.95,0],color=TEXT,stroke_width=4),
                  arr([-0.13,-1.95,0],[-0.13,-0.85,0],TEXT,w=4))
        cl=T("carbon dioxide in",24,TEXT).move_to([-3.3,-3.15,0])
        self.play(Create(co),FadeIn(cl),run_time=0.5)
        self.at("water vapor out")
        wa=VGroup(Line([0.13,-0.85,0],[0.13,-1.95,0],color=TEAL_W,stroke_width=4),
                  arr([0.13,-1.95,0],[1.8,-3.0,0],TEAL_W,w=4))
        wl=T("water vapour out",24,TEAL_W).move_to([3.5,-3.15,0])
        self.play(Create(wa),FadeIn(wl),run_time=0.5)
        self.at("the leaf gains carbon")
        # Make room for a readable whole plant while keeping the stoma and exchange arrows aligned.
        leaf=VGroup(upper,lower,mes,spongy,vein,chl,guard)
        little=plant().scale(0.8).move_to([5.1,0.25,0])
        connector=DashedLine([3.24,0.87,0],[4.3,0.99,0],color=GREY,stroke_width=4)
        self.play(FadeOut(light),leaf.animate.scale(0.6,about_point=[0,-1.5,0]),
                  air.animate.move_to([-2.2,-0.4,0]),FadeIn(little),Create(connector),run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Meristems supply cells; tips add length, cambia add girth."

    def construct(self):
        line=VGroup(T("Meristems supply cells;",36,font=TITLE_FONT),
                    T("tips add length, cambia add girth.",36,font=TITLE_FONT)).arrange(DOWN,buff=0.15).move_to([0,2.6,0])
        tree=oak().scale(0.65).shift(DOWN*0.9)
        dots=tips().scale(0.65).shift(DOWN*0.9)
        cambium=Ellipse(width=0.75,height=0.28,color=BLUE,stroke_width=4).move_to([0,-1.1,0])
        self.play(FadeIn(line),FadeIn(tree),run_time=0.6)
        self.play(FadeIn(dots),Create(cambium),run_time=0.5)
        self.finish()
