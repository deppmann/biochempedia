"""A Badge Only You Wear  (chapter 2 of "Choosing a Partner: Layers, Self-Avoidance and Smell")

COLOR MAP (one colour per concept, whole chapter; ties to scenes.old.py: PURPLE = the focal neuron,
ORANGE = a neighbouring neuron with a different version)
  PURPLE = the focal neuron: its branches, its badge (the Dscam1 version it carries), its picks
  ORANGE = a neighbouring neuron and the different badge it carries
  TEAL   = the Dscam1 gene, exons, outer surface and isoforms (the machinery)
  GREEN  = bound / pulled together (identical isoforms binding)
  RED    = pushed apart, retreat, or Dscam1 / protocadherins missing
  GOLD   = "Predict" prompts and the current-model tag
  GREY   = neutral structure and credits; orange always denotes the neighbour
  TEXT   = labels
Experimental shared-isoform labels name the shared treatment; arbor colours still identify cells.
Badge = a small coloured dot; its colour is the version, its position is the branch that carries it.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# geometry helpers
def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def vm(pts, color, w=5, op=1.0):
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op, fill_opacity=0)
    m.set_points_smoothly(np.array([[p[0], p[1], 0.0] for p in pts]))
    return m


TWIGS = [(0.40, +1, 0.30), (0.62, -1, 0.28)]


def arbor(cx, cy, rx, ry, color, n=8, phase=0.2, tangle=0.0, lens=None, seed=3, a0=0.3, w=4.5, wob=0.07, tc=0.35):
    """A dendritic arbor: n primary branches spread evenly (tangle=0) with two twigs each.
    tangle > 1 bends every branch toward one direction so they cross and bundle.
    Returns VGroup(VGroup(branches...), soma). Same n and seed always give the same structure."""
    rs = np.random.RandomState(seed)
    lens = lens or [1.0] * n
    prim, twg = [], []
    for i in range(n):
        th0 = phase + 2 * np.pi * i / n
        psi = rs.uniform(0, 2 * np.pi)
        amp = wob * rs.uniform(0.7, 1.3)
        kk = rs.uniform(1.0, 1.8)
        dth = wrap(tc - th0)
        L = lens[i]

        def th(r, th0=th0, psi=psi, amp=amp, kk=kk, dth=dth):
            return th0 + amp * np.sin(2 * np.pi * r * kk + psi) + tangle * dth * sstep(0.1, 1.0, r)

        def pt(r, th=th):
            t = th(r)
            return np.array([cx + (a0 + rx * r) * np.cos(t), cy + (a0 + ry * r) * np.sin(t)])

        prim.append(vm([pt(r) for r in np.linspace(0, L, 7)], color, w))
        for (rt, side, lt) in TWIGS:
            r0 = rt * L
            base = pt(r0)
            phi = th(r0) + side * 0.6
            tp = []
            for t in np.linspace(0, 1, 5):
                ph = phi + side * 0.3 * t
                tp.append(base + np.array([rx * lt * L * t * np.cos(ph), ry * lt * L * t * np.sin(ph)]))
            twg.append(vm(tp, color, w * 0.7))
    soma = Circle(a0, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.45).move_to([cx, cy, 0])
    return VGroup(VGroup(*prim, *twg), soma)


def tips(a, which="all", n=8):
    br = list(a[0])
    if which == "prim":
        br = br[:n]
    elif which == "pt":          # primary tips and the second twig of each branch
        br = br[:n] + [br[n + 2 * i + 1] for i in range(n)]
    return [b.get_end() for b in br]


def badge(color, p, r=0.12):
    return Circle(r, stroke_color=TEXT, stroke_width=1.5, fill_color=color, fill_opacity=1).move_to(p)


def badges(a, color, which="pt", n=8, r=0.12):
    return VGroup(*[badge(color, p, r) for p in tips(a, which, n)])


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=6, tip_len=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip_len,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def path(pts, color, w=6):
    return vm([np.array(p, dtype=float) for p in pts], color, w)


def tipg(pts, color, w=6, r=0.13):
    return VGroup(path(pts, color, w), Circle(r, stroke_width=0, fill_color=color, fill_opacity=1).move_to([*pts[-1], 0]))


def txt_bg(m, pad=0.12):
    """Put a background-coloured box behind a label so lines never run through it."""
    return VGroup(Rectangle(width=m.width + 2 * pad, height=m.height + 2 * pad, stroke_width=0,
                            fill_color=BG, fill_opacity=0.9).move_to(m), m)


def head(shape, color, r=0.42):
    if shape == "sq":
        s = RoundedRectangle(corner_radius=0.08, width=2 * r, height=2 * r)
    elif shape == "circ":
        s = Circle(r)
    elif shape == "tri":
        s = Triangle().scale(r * 1.15).rotate(-PI / 2)
    elif shape == "dia":
        s = Square(2 * r * 0.82).rotate(PI / 4)
    elif shape == "pent":
        s = RegularPolygon(5).scale(r * 1.05)
    else:
        s = RegularPolygon(6).scale(r * 1.05)
    s.set_stroke(color, 3).set_fill(color, 0.45)
    return s


def unit(xh, color, shape, side, y0=0.0, ytop=2.0, ybot=-2.0):
    """One branch segment (bar) with a surface protein pointing at its partner. side=-1 left, +1 right."""
    bx = xh + side * 1.3
    bar = Line([bx, ybot, 0], [bx, ytop, 0], color=color, stroke_width=12)
    stem = Line([bx, y0, 0], [xh + side * 0.42, y0, 0], color=color, stroke_width=6)
    return VGroup(bar, stem, head(shape, color).move_to([xh, y0, 0]))


def pair(cx, gap, ca, sa, cb, sb):
    return VGroup(unit(cx - gap / 2 - 0.42, ca, sa, -1), unit(cx + gap / 2 + 0.42, cb, sb, +1))


def link(cx, y0=0.0):
    return Line([cx - 0.25, y0, 0], [cx + 0.25, y0, 0], color=GREEN, stroke_width=14)


# ---------------------------------------------------------------------------------------------
# the genotype table used in scenes 15-19
TY = {0: 2.45, 1: 1.45, 2: 0.25, 3: -0.95, 4: -2.35}
ROWS = {
    1: ("normal", "own: apart\nothers: overlap"),
    2: ("no Dscam1", "own: cross\nand bundle"),
    3: ("one cell +\nsingle isoform", "own: apart\nothers: overlap"),
    4: ("all cells: same\nsingle isoform", "predicted:\nneighbours avoid"),
}


def tab_head():
    return VGroup(T("genotype", 26, GREY).move_to([-5.2, TY[0], 0]), T("what happens", 26, GREY).move_to([-2.1, TY[0], 0]))


def tab_box(i):
    return Rectangle(width=6.2, height=1.5 if i == 4 else 1.15, stroke_color=GREY, stroke_width=1.5, fill_opacity=0).move_to([-3.6, TY[i], 0])


def tab_a(i):
    col = RED if i == 2 else TEXT
    return T(ROWS[i][0], 26, col, line_spacing=0.8).move_to([-5.2, TY[i], 0])


def tab_b(i):
    return T(ROWS[i][1], 26, TEXT, line_spacing=0.8).move_to([-2.1, TY[i], 0])


def qcell():
    return VGroup(DashedVMobject(Rectangle(width=2.9, height=1.2, stroke_color=GOLD, stroke_width=3, fill_opacity=0), num_dashes=40)
                  .move_to([-2.1, TY[4], 0]), T("?", 44, GOLD).move_to([-2.1, TY[4], 0]))


# panel arbors for the table scenes (right of the table)
def p_one(tangle=0.0):
    return arbor(3.4, 0.0, 3.0, 2.6, PURPLE, tangle=tangle)


def p_pair_p(tangle=0.0, cx=2.1, rx=1.8):
    return arbor(cx, 0.0, rx, 2.6, PURPLE, tangle=tangle, tc=2.8)


def p_pair_o(cx=4.6, rx=1.8):
    return arbor(cx, 0.0, rx, 2.6, ORANGE, phase=0.2 + np.pi / 8, seed=7)


# stage arbors for the two-neuron scenes
def big_p(**kw):
    return arbor(0.0, 0.2, 6.0, 2.75, PURPLE, **kw)


def duo_p(**kw):
    return arbor(-2.2, 0.0, 3.9, 2.8, PURPLE, **kw)


def duo_o(**kw):
    return arbor(2.2, 0.0, 3.9, 2.8, ORANGE, phase=0.2 + np.pi / 8, seed=7, **kw)


def iso_chip(x):
    return bchip("single isoform", PURPLE, 26).move_to([x, 3.3, 0])


def note(text, color=GREY, size=28, y=-3.55, x=0.0):
    return T(text, size, color).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
def countdown(scene):
    track=Line([-5.7,-3.73,0],[5.7,-3.73,0],color=GREY,stroke_width=4)
    bar=Line([-5.7,-3.73,0],[5.7,-3.73,0],color=GOLD,stroke_width=5)
    scene.add(track,bar)
    scene.play(bar.animate.stretch(0.001,0,about_point=[-5.7,-3.73,0]),run_time=scene.narration_s,rate_func=linear)


def rna_row(picked=True):
    line=Line([-5.8,-2.6,0],[5.8,-2.6,0],color=GREY,stroke_width=3)
    boxes=VGroup(*[Square(0.42,color=PURPLE if picked and i%2 else GREY,fill_color=PURPLE if picked and i%2 else GREY,fill_opacity=0.8).move_to([XS[i],-2.6,0]) for i in range(9)])
    return VGroup(line,boxes,T("messenger RNA: one from each cluster" if picked else "messenger RNA",28).move_to([0,-3.3,0]))


class S00Title(TitleCard):
    LESSON = "Choosing a Partner: Layers, Self-Avoidance and Smell"
    TITLE = "A Badge Only You Wear"


class S01Q(SpokenScene):
    def construct(self):
        pa, oa = duo_p(), duo_o()
        self.add(pa, note("one neuron's own branches", PURPLE))
        self.at("overlapping")
        self.play(FadeIn(oa), run_time=0.5)
        self.finish()


class S02Even(SpokenScene):
    def construct(self):
        pa, oa = duo_p(), duo_o()
        lab = note("one neuron's arbor", PURPLE)
        self.add(pa, oa, lab)
        self.at("take one")
        self.play(FadeOut(oa), Transform(pa, big_p()), run_time=0.6)
        self.at("spread evenly")
        self.play(pa.animate.set_stroke(width=6), run_time=0.5)
        self.at("without crossing")
        self.play(ReplacementTransform(lab, note("no crossings, no bundles")), run_time=0.25)
        self.finish()


def _fit(pts, ky=1.6):
    return [((x + 4) * 1.46 - 4.5, y * ky) for x, y in pts]


A_FAR = _fit([(-4, 0), (-3.2, 0.45), (-2.4, 0.8), (-1.6, 1.0), (-0.9, 1.05), (-0.4, 1.0)])
A_TOUCH = _fit([(-4, 0), (-3.2, 0.45), (-2.4, 0.8), (-1.5, 0.95), (-0.5, 0.6), (0.45, 0.14)])
A_APART = _fit([(-4, 0), (-3.2, 0.45), (-2.4, 0.9), (-1.4, 1.3), (-0.3, 1.9), (1.0, 2.5)], 1.2)


def mir(pts):
    return [(x, -y) for x, y in pts]


class S03Sa(SpokenScene):
    def construct(self):
        lab = T("self-avoidance", 44, font=TITLE_FONT).move_to([0,3.25,0])
        a = tipg([(-3,-0.2),(-1.7,0.5),(0,1.7),(2.6,2.3)], PURPLE, 9, 0.18)
        b = tipg([(-3,-0.2),(-1.7,-0.9),(0,-2),(2.6,-2.6)], PURPLE, 9, 0.18)
        self.add(Line([-5,-0.2,0],[-3,-0.2,0],color=PURPLE,stroke_width=9),lab,a,b, Circle(0.45,color=PURPLE,fill_opacity=0.5).move_to([-5.4,-0.2,0]))
        self.at("self avoidance")
        ta = tipg([(-3,-0.2),(-1,0.8),(1.5,0.6),(3,0)], PURPLE,9,0.18)
        tb = tipg([(-3,-0.2),(-1,-1.2),(1.5,-0.6),(3,0)], PURPLE,9,0.18)
        self.play(Transform(a,ta),Transform(b,tb),run_time=0.5)
        self.at("touch")
        ring=Circle(0.4,color=TEXT).move_to([3,0,0])
        self.add(ring)
        self.at("move apart")
        self.play(FadeOut(ring),Transform(a,tipg([(-3,-0.2),(-1,0.7),(1.5,1.8),(4,2.4)],PURPLE,9,0.18)),Transform(b,tipg([(-3,-0.2),(-1,-1),(1.5,-2),(4,-2.6)],PURPLE,9,0.18)),run_time=0.6)
        self.add(T("retreat",32,RED).move_to([3,0,0]))
        self.finish()
        self.wait(1.8)


class S04Fly(SpokenScene):
    def construct(self):
        patch=RoundedRectangle(width=12.8,height=6.1,corner_radius=0.3,color=GREY,fill_opacity=0.08)
        pa,oa=duo_p(),duo_o()
        for a in (pa,oa):
            a.scale(0.88).shift(UP*0.15)
        self.add(patch,pa,T("fly body wall",30,GREY).move_to([0,3.4,0]),T("one class",30,PURPLE).move_to([-3,-3.3,0]))
        self.at("other classes")
        self.play(FadeIn(oa),FadeIn(T("another class",30,ORANGE).move_to([3,-3.3,0])),run_time=0.6)
        self.finish()


class S05Me(SpokenScene):
    def construct(self):
        a=tipg([(-5.5,-1.8),(-3.5,-1.4),(-2,0),(0,0.3)],PURPLE,12,0.22)
        b=tipg([(5.5,1.8),(3.5,1.4),(2,0),(0,0.3)],ORANGE,12,0.22)
        self.add(a,b,T("contact",30).move_to([0,1.1,0]))
        self.at("must ask")
        self.play(FadeIn(T("is this me, or someone else?",40).move_to([0,-2.9,0])),run_time=0.3)
        self.at("is this me")
        self.play(FadeIn(T("?",80,GOLD).move_to([0,2.5,0])),run_time=0.25)
        self.finish()


def s06_pic(final=True):
    """The question picture: identical copies bind, different ones do not."""
    left = pair(-3.4, 1.0, PURPLE, "sq", PURPLE, "sq")
    right = pair(3.4, 0.7, PURPLE, "sq", ORANGE, "tri")
    return left, right


class S06Predict1(SpokenScene):
    def construct(self):
        h=T("Predict.",48,GOLD,font=TITLE_FONT).move_to([0,3.2,0])
        left,right=s06_pic()
        self.add(h,left,right)
        l1=T("identical: bind",28,GREEN).move_to([-3.4,-2.55,0])
        l2=T("different: no bind",28,GREY).move_to([3.4,-2.55,0])
        self.at("binds only")
        lk=link(-3.4)
        self.play(Transform(left,pair(-3.4,0,PURPLE,"sq",PURPLE,"sq")),FadeIn(l1),FadeIn(l2),run_time=0.4)
        self.add(lk)
        self.at("pull apart")
        ret=T("same = retreat",28,RED).move_to([-3.4,-2.55,0])
        self.play(FadeOut(lk),Transform(left,pair(-3.4,1.8,PURPLE,"sq",PURPLE,"sq")),ReplacementTransform(l1,ret),run_time=0.6)
        self.remove(lk)
        self.at("what must")
        self.play(FadeIn(T("What must the protein be like?",34).move_to([0,-3.25,0])),run_time=0.3)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        h = T("Predict.", 48, GOLD, font=TITLE_FONT).move_to([0, 3.1, 0])
        left = pair(-3.4, 1.8, PURPLE, "sq", PURPLE, "sq")
        right = pair(3.4, 0.7, PURPLE, "sq", ORANGE, "tri")
        l1 = T("same = retreat", 28, RED).move_to([-3.4, -2.55, 0])
        l2 = T("different: no bind", 26, GREY).move_to([3.4, -2.55, 0])
        q = T("What must the protein be like?", 34, TEXT).move_to([0, -3.25, 0])
        self.add(h, left, right, l1, l2, q)
        countdown(self)
        self.finish()


class S08Reveal1(SpokenScene):
    def construct(self):
        pa=big_p()
        bd=badges(pa,PURPLE)
        self.add(pa,bd,note("same badge on every branch: sister branches always match"))
        self.at("carry the same")
        self.play(bd.animate.set_stroke(PURPLE,3),run_time=0.4)
        self.finish()


class S09Reveal1b(SpokenScene):
    def construct(self):
        pa,oa=duo_p(),duo_o()
        self.add(pa,badges(pa,PURPLE),note("different badge: branches seldom match"))
        self.at("neighboring neurons")
        self.play(FadeIn(oa),run_time=0.35)
        self.at("different versions")
        self.play(FadeIn(badges(oa,ORANGE)),run_time=0.35)
        self.finish()


class S10Beat1(NarratedScene):
    def construct(self):
        pa, oa = duo_p(), duo_o()
        zone = Ellipse(width=2.4, height=5.2, stroke_color=TEXT, stroke_width=3).move_to([0, 0, 0])
        self.add(pa, oa, badges(pa, PURPLE), badges(oa, ORANGE), zone, note("different badges: their branches seldom match"))
        countdown(self)
        self.finish()


# ---------------------------------------------------------------------------------------------
SHAPES = ["sq", "circ", "tri", "dia", "pent", "hex"]


def iso_glyph(shape, color=TEAL, scale=1.0):
    stem = Line([0, -0.55, 0], [0, 0.0, 0], color=color, stroke_width=5)
    bar = Line([-0.5, -0.55, 0], [0.5, -0.55, 0], color=color, stroke_width=8)
    return VGroup(bar, stem, head(shape, color, 0.34).move_to([0, 0.34, 0])).scale(scale)


class S11Dscam(SpokenScene):
    def construct(self):
        gene=bchip("one gene: Dscam1 · Drosophila",TEAL,36).move_to([0,2.7,0])
        one=iso_glyph("sq",scale=2.5).move_to([0,-0.4,0])
        arrow=arr([0,2.05,0],[0,1.05,0],TEAL,4)
        self.add(gene,one,arrow,T("Schmucker, Zipursky and colleagues, 2000",26,GREY).move_to([0,-3.35,0]),T("isoforms: forms of one protein made from one gene",30).move_to([0,-2.25,0]))
        self.at("many isoforms")
        row=VGroup(*[iso_glyph(sh,scale=1.5).move_to([-4.8+1.92*k,-0.3,0]) for k,sh in enumerate(SHAPES)])
        links=VGroup(*[arr([0,2.05,0],[x,0.65,0],TEAL,3) for x in [-4.8,-2.88,-0.96,0.96,2.88,4.8]])
        self.play(ReplacementTransform(one,row),ReplacementTransform(arrow,links),run_time=0.4)
        self.finish()
        self.wait(1.5)


CL = [(12, 3), (48, 6), (33, 6), (2, 2)]
CELL = 0.34
GW, GAP = 0.55, 0.3
WID = [GW, 1.02, GW, 2.04, GW, 2.04, GW, 0.68, GW]
XS = []
_x = -(sum(WID) + GAP * 8) / 2
for _w in WID:
    XS.append(_x + _w / 2)
    _x += _w + GAP
ROW_Y = 0.75


def cgrid(n, cols, color=TEAL):
    rows = -(-n // cols)
    cells = []
    for k in range(n):
        r, c = divmod(k, cols)
        cells.append(Square(CELL * 0.86, stroke_width=1.5, stroke_color=color, fill_color=color, fill_opacity=0.35)
                     .move_to([(c - (cols - 1) / 2) * CELL, ((rows - 1) / 2 - r) * CELL, 0]))
    return VGroup(*cells)


def gblock(i):
    return Rectangle(width=GW, height=1.4, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.3).move_to([XS[i], ROW_Y, 0])


def grids():
    gs = []
    for k, (n, cols) in enumerate(CL):
        gs.append(cgrid(n, cols).move_to([XS[2 * k + 1], ROW_Y, 0]))
    return gs


def gcounts():
    out=VGroup()
    for k,(n,_) in enumerate(CL):
        x=XS[2*k+1]
        out.add(VGroup(M(str(n),28,TEAL).move_to([x,-0.96,0]),T("alternative\nexons",26,TEAL,line_spacing=0.8).move_to([x,-1.77,0])))
    return out


def exon_def():
    return T("exon: a stretch of a gene kept in the messenger RNA", 28, TEXT, t2c={"exon": TEAL}).move_to([0, 3.3, 0])


def final_row():
    """Backbone, grey exons and the four cluster grids (the s12 end state)."""
    back = Line([XS[0] - 0.5, 2.4, 0], [XS[-1] + 0.5, 2.4, 0], color=GREY, stroke_width=3)
    gb = VGroup(*[gblock(i) for i in (0, 2, 4, 6, 8)])
    return back, gb, grids()


class S12Exons(SpokenScene):
    def construct(self):
        self.add(exon_def())
        back,gb,gs=final_row()
        self.add(back,gb)
        self.at("a gene")
        self.play(FadeIn(T("gene",28,GREY).move_to([-5.7,2.7,0])),run_time=0.2)
        self.at("messenger rna")
        self.play(FadeIn(rna_row(False)),run_time=0.3)
        self.at("four of")
        self.play(FadeIn(VGroup(*gs)),run_time=0.5)
        self.at("alternatives")
        self.play(FadeIn(gcounts()),run_time=0.3)
        self.finish()


PICK = [5, 21, 10, 0]


class S12bOne(SpokenScene):
    def construct(self):
        back,gb,gs=final_row()
        strip=rna_row(False)
        self.add(exon_def(),back,gb,*gs,gcounts(),strip)
        self.at("one exon")
        self.play(*[gs[k][PICK[k]].animate.set_fill(PURPLE,1).set_stroke(PURPLE) for k in range(4)],ReplacementTransform(strip,rna_row(True)),run_time=0.7)
        self.finish()


class S13Count(SpokenScene):
    def construct(self):
        back,gb,gs=final_row()
        for k in range(4):
            gs[k][PICK[k]].set_fill(PURPLE,1).set_stroke(PURPLE)
        gene=VGroup(back,gb,*gs).scale(0.72).move_to([0,1.8,0])
        self.add(gene,rna_row(True).shift(UP*2.5))
        a=T("12 × 48 × 33 = 19,008  outer surfaces",36,TEAL).move_to([0,-1.8,0])
        b=T("19,008 × 2 = 38,016  isoforms in all",36,TEAL).move_to([0,-2.9,0])
        self.at("that gives")
        self.play(FadeIn(a),run_time=0.2)
        # Complete integers only; the two results remain together for over three seconds.
        self.at("outer surfaces")
        self.play(FadeIn(b),run_time=0.2)
        self.finish()


class S13bFourth(SpokenScene):
    def construct(self):
        band=Rectangle(width=12.4,height=1.1,color=GREY,fill_opacity=0.15).move_to([0,-0.3,0])
        outer=VGroup(*[RoundedRectangle(width=2,height=0.85,corner_radius=0.1,color=TEAL,fill_color=TEAL,fill_opacity=0.35).move_to([-2,y,0]) for y in [0.9,1.9,2.9]])
        tm=Rectangle(width=0.65,height=1.5,color=PURPLE,fill_color=PURPLE,fill_opacity=0.8).move_to([-2,-0.3,0])
        tail=Line([-2,-1.05,0],[-2,-2.9,0],color=TEAL,stroke_width=8)
        outer_label=T("outer part",34,TEAL).move_to([2.6,2,0])
        membrane_label=T("inside the membrane",30,PURPLE).move_to([2.6,-0.3,0])
        # Bracket all three extracellular blocks; stop both leaders before their labels.
        bracket=VGroup(Line([-0.8,0.475,0],[-0.6,0.475,0],color=TEAL,stroke_width=2),
                        Line([-0.6,0.475,0],[-0.6,3.325,0],color=TEAL,stroke_width=2),
                        Line([-0.8,3.325,0],[-0.6,3.325,0],color=TEAL,stroke_width=2))
        self.add(band,outer,tm,tail,bracket,outer_label,membrane_label,
                 T("membrane",28,GREY).move_to([-4.8,-0.3,0]))
        self.add(Line([-0.6,2,0],outer_label.get_left()+LEFT*0.2,color=TEAL,stroke_width=2),
                 Line([-1.65,-0.3,0],membrane_label.get_left()+LEFT*0.2,color=PURPLE,stroke_width=2))
        self.at("fourth cluster")
        self.play(FadeIn(T("fourth cluster: 2 versions",30,PURPLE).move_to([2,-1.6,0])),tm.animate.set_stroke(TEXT,5),run_time=0.4)
        self.at("does not change")
        self.play(Transform(outer_label,T("outer part\nunchanged",34,TEAL,line_spacing=0.8).move_to([2.6,2,0])),run_time=0.3)
        self.finish()


class S14Bind(SpokenScene):
    def construct(self):
        left=pair(-3.4,0.8,PURPLE,"sq",PURPLE,"sq")
        right=pair(3.4,0.7,PURPLE,"sq",ORANGE,"tri")
        l1=T("identical: bind",28,GREEN).move_to([-3.4,-2.55,0])
        self.add(left,right,T("same isoform",32,PURPLE).move_to([-3.4,3.1,0]),T("different isoforms",32,ORANGE).move_to([3.4,3.1,0]),T("Wojtowicz, Zipursky and colleagues, 2004",26,GREY).move_to([0,-3.45,0]),T("different: no bind",28,GREY).move_to([3.4,-2.55,0]))
        self.at("binds mainly")
        lk=link(-3.4)
        self.play(Transform(left,pair(-3.4,0,PURPLE,"sq",PURPLE,"sq")),FadeIn(l1),run_time=0.4)
        self.add(lk)
        self.at("matched branches")
        ret=T("same = retreat",36,RED).move_to([-3.4,-2.55,0])
        self.play(FadeOut(lk),ReplacementTransform(l1,ret),Transform(left,pair(-3.4,1.8,PURPLE,"sq",PURPLE,"sq")),GrowArrow(arr([-4.6,2.45,0],[-5.7,2.45,0],RED)),GrowArrow(arr([-2.2,2.45,0],[-1.1,2.45,0],RED)),run_time=0.6)
        self.remove(lk)
        self.at("same means")
        self.play(ret.animate.set_stroke(RED,0.6),run_time=0.25)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S15Null(SpokenScene):
    def construct(self):
        pa = p_one()
        hd, b1, a1, t1 = tab_head(), tab_box(1), tab_a(1), tab_b(1)
        self.add(hd,b1,a1,t1,pa)
        self.at("dscam1")
        b2, a2 = tab_box(2), tab_a(2)
        cr = T("three groups, 2007", 26, GREY).move_to([-3.6, -3.55, 0])
        self.play(FadeIn(b2), FadeIn(a2), FadeIn(cr), run_time=0.7)
        self.at("cross and")
        t2 = tab_b(2)
        self.play(Transform(pa, p_one(tangle=1.2)), FadeIn(t2), run_time=1.4)
        self.finish()


def rows_upto(n):
    out = []
    for i in range(1, n + 1):
        out += [tab_box(i), tab_a(i), tab_b(i)] if i < 4 else [tab_box(i), tab_a(i)]
    return out


class S16Single(SpokenScene):
    def construct(self):
        pa = p_one(tangle=1.2)
        self.add(tab_head(), *rows_upto(2), pa, T("three groups, 2007", 26, GREY).move_to([-3.6, -3.55, 0]), T("neighbour: normal",26,ORANGE).move_to([4.9,3.35,0]))
        self.at("take a")
        b3, a3 = tab_box(3), tab_a(3)
        oa = p_pair_o()
        self.play(FadeIn(b3), FadeIn(a3), Transform(pa, p_pair_p(tangle=1.2)), FadeIn(oa[1]), Create(oa[0], lag_ratio=0.03), run_time=0.9)
        nt = T("neighbour: normal", 26, ORANGE).move_to([4.9, 3.35, 0])
        self.at("lacks")
        c1 = bchip("no Dscam1", RED, 26).move_to([1.7, 3.3, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.6)
        self.at("single isoform")
        c2 = iso_chip(1.7)
        self.play(ReplacementTransform(c1, c2), Transform(pa, p_pair_p()), FadeIn(tab_b(3)), run_time=0.6)
        self.finish()


def s16_end():
    pa, oa = p_pair_p(), p_pair_o()
    c2 = iso_chip(1.7)
    nt = T("neighbour: normal", 26, ORANGE).move_to([4.9, 3.35, 0])
    return pa, oa, c2, nt


class S17Predict2(SpokenScene):
    def construct(self):
        pa, oa, c2, nt = s16_end()
        self.add(tab_head(), *rows_upto(3), pa, oa, c2, nt, T("three groups, 2007", 26, GREY).move_to([-3.6, -3.55, 0]))
        h = T("Predict.", 44, GOLD, font=TITLE_FONT).move_to([-3.6, 3.45, 0])
        self.play(FadeIn(h, shift=DOWN * 0.1), run_time=0.5)
        self.at("give every")
        b4, a4 = tab_box(4), tab_a(4)
        qc = qcell()
        self.play(FadeIn(b4), FadeIn(a4), FadeIn(qc), run_time=0.8)
        self.at("same single")
        c3 = iso_chip(5.2)
        self.play(FadeOut(nt),FadeIn(c3),run_time=0.35)
        self.at("what happens")
        q = T("What happens\nbetween neighbours?", 30, GOLD).move_to([3.4, -3.35, 0])
        self.play(FadeIn(q, shift=UP * 0.1), Indicate(qc[1], color=TEXT, scale_factor=1.4), run_time=0.9)
        self.finish()


def s17_end():
    pa, oa, c2, nt = s16_end()
    c3 = iso_chip(5.2)
    h = T("Predict.", 44, GOLD, font=TITLE_FONT).move_to([-3.6, 3.45, 0])
    q = T("What happens\nbetween neighbours?", 30, GOLD).move_to([3.4, -3.35, 0])
    return pa, oa, c2, c3, h, q


class S18Pause(NarratedScene):
    def construct(self):
        pa, oa, c2, c3, h, q = s17_end()
        self.add(tab_head(), *rows_upto(3), tab_box(4), tab_a(4), qcell(), pa, oa, c2, c3, h, q,
                 T("three groups, 2007", 26, GREY).move_to([-3.6, -3.55, 0]))
        countdown(self)
        self.finish()


class S19Reveal2(SpokenScene):
    def construct(self):
        pa,oa,c2,c3,h,q=s17_end()
        qc=qcell()
        self.add(tab_head(),*rows_upto(3),tab_box(4),tab_a(4),qc,pa,oa,c2,c3,T("Predicted",40,GOLD,font=TITLE_FONT).move_to([-3.6,3.45,0]),T("three groups, 2007",26,GREY).move_to([-3.6,-3.55,0]))
        self.at("cannot tell")
        self.play(FadeOut(qc),FadeIn(T(ROWS[4][1],26,GOLD,line_spacing=0.8).move_to([-2.1,TY[4],0])),run_time=0.35)
        self.at("the logic")
        self.play(Transform(pa,p_pair_p(cx=1.8,rx=1.2)),Transform(oa,p_pair_o(cx=5.0,rx=1.2)),run_time=0.6)
        self.finish()


class S20Hattori(SpokenScene):
    def construct(self):
        xs=np.linspace(-4.5,4.5,7)
        top=VGroup(*[Circle(0.23,color=TEXT).move_to([x,2,0]) for x in xs])
        bot=VGroup(*[Circle(0.23,color=TEXT).move_to([x,-2,0]) for x in xs])
        wires=VGroup(*[Line([x,1.77,0],[x,-1.77,0],color=GREY,stroke_width=4) for x in xs])
        lab=T("normal organisation",32).move_to([0,3.2,0])
        self.add(top,bot,wires,lab,T("neurons",28).move_to([-5.7,2,0]),T("targets",28).move_to([-5.7,-2,0]),T("schematic only",28,GOLD).move_to([0,-2.75,0]),T("Hattori, Demir and colleagues, 2007",26,GREY).move_to([0,-3.4,0]))
        self.at("only one")
        self.play(FadeOut(lab),FadeIn(T("only one outer surface",32,TEAL).move_to([0,3.2,0])),run_time=0.2)
        self.at("severely")
        perm=[4,2,6,0,5,1,3]
        tangled=VGroup(*[path([(x,1.77),(x*0.5,0.7),(xs[j]*0.5,-0.7),(xs[j],-1.77)],GREY,4) for x,j in zip(xs,perm)])
        self.play(Transform(wires,tangled),FadeIn(T("disorganised circuits",32).move_to([0,0,0]).add_background_rectangle(color=BG,opacity=1)),run_time=0.6)
        self.finish()


def two_badges(si, sj, cy=1.3):
    a = head(si, PURPLE, 1.2).move_to([-3.2, cy, 0])
    b = head(sj, ORANGE, 1.2).move_to([3.2, cy, 0])
    return a, b


class S21Which(SpokenScene):
    def construct(self):
        s1 = Circle(0.55, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.45).move_to([-3.2, -1.3, 0])
        s2 = Circle(0.55, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.45).move_to([3.2, -1.3, 0])
        a, b = two_badges("sq", "tri")
        st1 = Line([-3.2, -0.75, 0], [-3.2, 0.4, 0], color=PURPLE, stroke_width=6)
        st2 = Line([3.2, -0.75, 0], [3.2, 0.4, 0], color=ORANGE, stroke_width=6)
        self.add(s1,s2,st1,st2,a,b)
        self.at("carries")
        a2, b2 = two_badges("circ", "dia")
        self.play(Transform(a, a2), Transform(b, b2), run_time=0.6)
        self.at("matters little")
        a3, b3 = two_badges("hex", "sq")
        t1 = T("which isoform: matters little", 34, GREY).move_to([0, -2.6, 0])
        self.play(Transform(a, a3), Transform(b, b3), FadeIn(t1), run_time=0.25)
        self.at("differing from")
        ne = T("≠", 90, TEXT).move_to([0, 1.0, 0])
        t2 = T("being different from neighbours: matters", 34, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(ne, scale=0.6), FadeIn(t2, shift=UP * 0.1), run_time=0.8)
        self.at("what matters")
        self.play(FadeIn(T("different",48,GOLD).move_to([0,2.9,0])),run_time=0.3)
        self.finish()


class S22Beat2(NarratedScene):
    def construct(self):
        s1 = Circle(0.55, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.45).move_to([-3.2, -1.3, 0])
        s2 = Circle(0.55, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.45).move_to([3.2, -1.3, 0])
        a, b = two_badges("hex", "sq")
        st1 = Line([-3.2, -0.75, 0], [-3.2, 0.4, 0], color=PURPLE, stroke_width=6)
        st2 = Line([3.2, -0.75, 0], [3.2, 0.4, 0], color=ORANGE, stroke_width=6)
        ne = T("≠", 90, TEXT).move_to([0, 1.0, 0])
        t1 = T("which isoform: matters little", 34, GREY).move_to([0, -2.6, 0])
        t2 = T("being different from neighbours: matters", 34, TEXT).move_to([0, -3.4, 0])
        self.add(s1, s2, st1, st2, a, b, ne, t1, t2, T("different",48,GOLD).move_to([0,2.9,0]))
        self.finish()


# ---------------------------------------------------------------------------------------------
def bowl(cx, cy, w, h, color=GREY):
    ts = np.linspace(PI, 2 * PI, 40)
    pts = [(cx + w / 2 * np.cos(t), cy + h * np.sin(t)) for t in ts]
    return VGroup(vm(pts, color, 5), Line([cx - w / 2, cy, 0], [cx + w / 2, cy, 0], color=color, stroke_width=5))


def bowl_dots(cx, cy, w, h, r):
    counts = [10, 10, 9, 8, 6, 5]
    out = []
    for k, c in enumerate(counts):
        y = cy - 0.3 - k * (h - 0.5) / 5
        chord = w * np.sqrt(max(0.05, 1 - ((cy - y) / h) ** 2)) - 0.9
        xs = np.linspace(-chord / 2, chord / 2, c)
        for x in xs:
            out.append(np.array([cx + x, y, 0.0]))
    return out


def dot(p, color, r, fill=1.0, ring=None):
    return Circle(r, stroke_color=ring or color, stroke_width=3 if ring else 1.5, fill_color=color, fill_opacity=fill).move_to(p)


def draw48():
    perm=np.random.RandomState(5).permutation(48)
    return list(perm[:20]), list(perm[:8])+list(perm[20:32])


def bowl_scene(total=48):
    bw=bowl(0,2.0,10.2,4.4)
    pos=bowl_dots(0,2.0,10.2,4.4,0.16)
    ds=VGroup(*[dot(p,GREY,0.16,0.65) for p in pos])
    return bw,ds


class S23Why(SpokenScene):
    def construct(self):
        bw,ds=bowl_scene()
        title=T("Why thousands?",44,GOLD,font=TITLE_FONT).move_to([0,3.25,0])
        self.add(title,bw,ds,note("illustrative model, not a measured count",size=26))
        self.at("drawing about")
        picks=VGroup(*[dot([-4.2+0.44*k,2.65,0],PURPLE,0.13) for k in range(20)])
        self.play(TransformFromCopy(VGroup(*ds[:20]),picks),run_time=0.6)
        self.finish()


class S24Small(SpokenScene):
    def construct(self):
        bw,ds=bowl_scene()
        mine,nb=draw48()
        for i in mine:
            ds[i].set_fill(PURPLE,1).set_stroke(PURPLE,2)
        self.add(bw,ds,T("a bowl of 48 badges",36).move_to([0,3.3,0]),note("illustrative model, not a measured count",size=26))
        legend=VGroup(dot([0,0,0],PURPLE,0.13),T("yours",28,PURPLE),Circle(0.18,color=ORANGE),T("neighbour's",28,ORANGE),dot([0,0,0],GOLD,0.13),T("shared",28,GOLD)).arrange(RIGHT,buff=0.2).move_to([0,2.55,0])
        self.add(legend)
        self.add(T("8 of your 20 shared: about 40%",34,GOLD).move_to([0,-2.9,0]))
        self.at("a neighbor")
        rings=VGroup(*[Circle(0.24,color=ORANGE,stroke_width=4).move_to(ds[i]) for i in nb])
        self.play(FadeIn(rings),run_time=0.3)
        self.play(*[ds[i].animate.set_fill(GOLD,1).set_stroke(GOLD,2) for i in mine if i in nb],run_time=0.2)
        self.finish()


class S25Huge(SpokenScene):
    def construct(self):
        bw,_=bowl_scene()
        rs=np.random.RandomState(8)
        pts=[]
        while len(pts)<1200:
            x,y=rs.uniform(-4.95,4.95),rs.uniform(-2.3,1.85)
            if (x/5.1)**2+((y-2)/4.4)**2<0.95:
                pts.append([x,y,0])
        ds=VGroup(*[Dot(p,radius=0.025,color=GREY) for p in pts])
        self.add(bw,ds,T("a bowl of 19,008 badges",36).move_to([0,3.3,0]),T("not all badges shown",28,GREY).move_to([0,2.6,0]),note("illustrative model, not a measured count",size=26))
        self.add(T("about 0.1% of your badges shared",34).move_to([0,-2.9,0]))
        self.at("a neighbor")
        mine=VGroup(*[dot(p,PURPLE,0.11) for p in pts[:20]])
        nb=VGroup(*[Circle(0.15,color=ORANGE,stroke_width=3).move_to(p) for p in pts[20:40]])
        self.play(FadeIn(mine),FadeIn(nb),run_time=0.3)
        self.add(T("about 0.1% of your badges shared",34).move_to([0,-2.9,0]))
        self.finish()


class S26Slight(SpokenScene):
    def construct(self):
        self.add(T("Share of one neuron's badges also carried by…",34).move_to([0,3.2,0]))
        x0,w=-4.8,9.2
        for y,label,col in [(1.5,"sister branches",PURPLE),(-0.8,"neighbour (huge bowl)",ORANGE)]:
            self.add(T(label,30,col).move_to([0,y+0.65,0]),Rectangle(width=w,height=0.9,color=GREY).move_to([x0+w/2,y,0]))
        self.add(T("0%",26,GREY).move_to([x0,-1.65,0]),T("100%",26,GREY).move_to([x0+w,-1.65,0]))
        self.at("sister branches")
        bar=Rectangle(width=w,height=0.9,stroke_width=0,fill_color=PURPLE,fill_opacity=0.8).move_to([x0+w/2,1.5,0])
        self.play(GrowFromEdge(bar,LEFT),run_time=0.5)
        self.add(T("100%",30).move_to([5.3,1.5,0]))
        self.at("neighbor only")
        share=20/19008
        tiny=Rectangle(width=w*share,height=0.9,stroke_width=0,fill_color=ORANGE,fill_opacity=1).move_to([x0+w*share/2,-0.8,0])
        self.add(tiny,T("about 0.1%",30,ORANGE).move_to([-2.5,-0.8,0]),arr([-4,-0.05,0],[-4.8,-0.75,0],ORANGE,3))
        self.at("flies need")
        self.play(FadeIn(T("flies need thousands of isoforms to wire normally",30).move_to([0,-2.65,0])),run_time=0.3)
        self.add(T("Hattori and colleagues, 2009",26,GREY).move_to([0,-3.3,0]))
        self.finish()


def sb_cells(c0=PURPLE, c1=ORANGE, tangle=0.0, rx=2.2, xs=(-3.9, 0.0, 3.9), cy=-0.2, colors=None):
    cols = colors or [c1, c0, c1]
    return [arbor(x, cy, rx, 2.3, c, n=12, phase=0.1, tangle=tangle, seed=4 + k, wob=0.1) for k, (x, c) in enumerate(zip(xs, cols))]


class S27Mouse(SpokenScene):
    def construct(self):
        l, c, r = sb_cells()
        lab = T("mouse retina: starburst amacrine cells", 30, TEXT).move_to([0, 3.4, 0])
        self.add(lab,c)
        self.at("mouse")
        self.play(FadeIn(l),FadeIn(r),run_time=0.6)
        self.finish()


class S28Pcdh(SpokenScene):
    def construct(self):
        c=arbor(-1.4,-0.15,3.6,2.6,PURPLE,n=12,phase=0.1,seed=5,wob=0.1)
        label=bchip("gamma protocadherins",TEAL,32).move_to([0,3.25,0])
        cr=T("Lefebvre, Sanes and colleagues, 2012",26,GREY).move_to([0,-3.45,0])
        self.add(c,label,cr)
        self.at("adhesion proteins")
        sub=T("cadherin-family\nadhesion proteins",28,TEAL,line_spacing=0.9).move_to([4.55,1.3,0])
        self.add(sub)
        self.at("without them")
        self.play(ReplacementTransform(label,bchip("no protocadherins",RED,32).move_to([0,3.25,0])),FadeOut(sub),Transform(c,arbor(-1.4,-0.15,3.6,2.6,PURPLE,n=12,phase=0.1,seed=5,wob=0.1,tangle=1.2,tc=2.8)),run_time=0.6)
        self.finish()


class S29Same(SpokenScene):
    def construct(self):
        # Normal overlap is the comparison, with identity colour preserved for each cell.
        left=arbor(-2.6,0,3.1,2.6,PURPLE,n=12,seed=4)
        right=arbor(2.6,0,3.1,2.6,ORANGE,n=12,seed=5)
        lab=T("normal neighbours: overlapping arbors",34).move_to([0,3.3,0])
        self.add(left,right,lab)
        self.at("lacking")
        self.play(ReplacementTransform(lab,T("no protocadherins",34,RED).move_to([0,3.3,0])),Transform(left,arbor(-2.6,0,2.6,2.6,PURPLE,n=12,seed=4,tangle=1.2,tc=2.8)),Transform(right,arbor(2.6,0,2.6,2.6,ORANGE,n=12,seed=5,tangle=1.2)),run_time=0.5)
        self.at("same single isoform")
        self.clear()
        self.add(left,right,T("same single isoform in every cell",34,TEAL).move_to([0,3.3,0]))
        self.at("each arbor")
        self.play(Transform(left,arbor(-2.6,0,3.1,2.6,PURPLE,n=12,seed=4)),Transform(right,arbor(2.6,0,3.1,2.6,ORANGE,n=12,seed=5)),run_time=0.5)
        self.at("neighbors avoid")
        # Keep visible residual overlap: each horizontal extent includes the soma offset of 0.3.
        self.play(Transform(left,arbor(-2.6,0,2.65,2.6,PURPLE,n=12,seed=4)),Transform(right,arbor(2.6,0,2.65,2.6,ORANGE,n=12,seed=5)),run_time=0.6)
        self.add(T("overlap between neighbours falls sharply",32).move_to([0,-3.3,0]))
        self.finish()


class S30Combo(SpokenScene):
    def construct(self):
        shp = ["sq", "circ", "tri", "dia", "pent", "hex", "sq"]
        shq = ["sq", "hex", "tri", "circ", "pent", "dia", "tri"]
        xs = [-3.6 + 1.3 * k for k in range(7)]
        rowa = VGroup(*[head(s, PURPLE, 0.36).move_to([x, 1.2, 0]) for s, x in zip(shp, xs)])
        rowb = VGroup(*[head(s, ORANGE, 0.36).move_to([x, -1.2, 0]) for s, x in zip(shq, xs)])
        la = T("your cell", 26, PURPLE).move_to([-5.7, 1.2, 0])
        lb = T("neighbour", 26, ORANGE).move_to([-5.7, -1.2, 0])
        self.add(rowa,la)
        self.at("58 genes")
        g = T("7 of about 58 shown", 32, TEXT).move_to([-3.5, 3.3, 0])
        self.play(FadeIn(g, shift=DOWN * 0.1), run_time=0.6)
        self.at("recognition")
        self.play(FadeIn(rowb, lag_ratio=0.1), FadeIn(lb), run_time=1.0)
        self.at("whole combination")
        fa = RoundedRectangle(corner_radius=0.2, width=9.4, height=1.2, stroke_color=PURPLE, stroke_width=3).move_to([0.6, 1.2, 0])
        fb = RoundedRectangle(corner_radius=0.2, width=9.4, height=1.2, stroke_color=ORANGE, stroke_width=3).move_to([0.6, -1.2, 0])
        ne = T("≠", 70, TEXT).move_to([0.6, 0.0, 0])
        cm = bchip("current model", GOLD, 28).move_to([4.2, 3.3, 0])
        self.play(Create(fa), Create(fb), FadeIn(ne, scale=0.6), FadeIn(cm), run_time=0.5)
        self.add(T("a few shared isoforms are not enough:\nthe whole combination is compared",30,TEXT,line_spacing=0.8).move_to([0,-2.9,0]))
        self.at("not single")
        ls = VGroup(*[Line([xs[k], 0.8, 0], [xs[k], -0.8, 0], color=GREY, stroke_width=3) for k in (0, 2, 4)])
        self.play(Create(ls), run_time=0.6)
        self.finish()


class S31Take(SpokenScene):
    def construct(self):
        xs = (-4.4, -0.1, 4.5)
        # panel 1: a badge unique to one cell
        soma = Circle(0.6, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.45).move_to([xs[0], -0.3, 0])
        bd = head("hex", PURPLE, 0.8).move_to([xs[0], 2.1, 0])
        st = Line([xs[0], 0.3, 0], [xs[0], 1.05, 0], color=PURPLE, stroke_width=5)
        c1 = T("a label unique\nto one cell", 28, TEXT, line_spacing=0.8).move_to([xs[0], -2.0, 0])
        # panel 2: read as retreat
        a = tipg([(-0.9, -1.6), (-0.8, -0.8), (-0.5, 0.0), (-0.3, 0.9), (-0.14, 1.5)], PURPLE)
        b = tipg([(0.9, -1.6), (0.8, -0.8), (0.5, 0.0), (0.3, 0.9), (0.14, 1.5)], PURPLE)
        a2 = tipg([(-0.9, -1.6), (-1.1, -0.8), (-1.5, 0.0), (-1.9, 0.9), (-2.1, 1.5)], PURPLE)
        b2 = tipg([(0.9, -1.6), (1.1, -0.8), (1.5, 0.0), (1.9, 0.9), (2.1, 1.5)], PURPLE)
        r1, r2 = arr([-0.5, 2.7, 0], [-1.4, 2.7, 0], RED), arr([0.5, 2.7, 0], [1.4, 2.7, 0], RED)
        c2 = T("read as retreat", 28, RED).move_to([xs[1], -2.4, 0])
        # Complete takeaway card is present from the first frame; cues animate its meaning.
        arb = arbor(xs[2], 0.45, 1.55, 2.15, PURPLE)
        c3 = T("keeps that cell’s own\nbranches apart", 28, TEXT, line_spacing=0.8).move_to([xs[2], -3.05, 0])
        self.add(soma,st,bd,c1,a,b,r1,r2,c2,arb,c3)
        self.at("label unique")
        self.play(bd.animate.set_stroke(PURPLE,5),run_time=0.3)
        self.at("as retreat")
        self.play(Transform(a, a2), Transform(b, b2),run_time=0.7)
        self.at("keeps that")
        self.play(arb.animate.set_stroke(width=5),run_time=0.3)
        self.finish()


class S32End(EndCard):
    LINE = "A label unique to one cell, read as retreat, keeps that cell's own branches apart."

    def construct(self):
        line=T("A label unique to one cell,\nread as retreat,\nkeeps that cell's own branches apart.",42,font=TITLE_FONT,line_spacing=1.1)
        self.add(line,T("biochemistrypedia.com",28,TEAL).move_to([0,-2.6,0]))
        self.finish()
