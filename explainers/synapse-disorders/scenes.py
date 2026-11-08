"""Built, Then Kept (chapter 1 of Disorders of the Synapse). Timed to the spoken words in audio/words.json.

COLOR MAP (one color per concept, whole film; chapters 2 and 3 reuse it)
  GREY   = circuits, neurons, membranes, axes, structure, genes in the cloud
  GREEN  = working, typical, gene on, restoring helps
  RED    = symptoms, gene off, miswired ("built wrong"), harm
  BLUE   = scaffold / build-and-hold proteins (job 1) and the missing synapse protein
  ORANGE = translation: ribosomes, how much protein (job 2)
  PURPLE = nucleus and gene choice (job 3)
  AMBER  = built but not kept
  GOLD   = the building window; "build"
  YELLOW = the question being asked, the highlighted row or column
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
TEAL = "#F29E55"  # translation, deliberately distinct from blue job 1
AMBER = "#EBC46A"
X0 = 1.2   # synapse x offset once the tag column is on screen (scenes 4 to 7)

NODES = [(-2, 1.3), (-2, -1.3), (0, 1.7), (0, 0), (0, -1.7), (2, 0.9), (2, -0.9)]
EDGES = [(0, 2), (0, 3), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6)]


# ---------------------------------------------------------------- helpers
def make_circuit(center=(0, 0), scale=1.0, color=GREY, fill=0.3):
    nodes = VGroup(*[Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color,
                            fill_opacity=fill).move_to([x, y, 0]) for x, y in NODES])
    edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), color=color, stroke_width=4)
                     for a, b in EDGES])
    g = VGroup(edges, nodes)
    g.edges, g.nodes = edges, nodes
    g.scale(scale).move_to([center[0], center[1], 0])
    return g


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dchip(text, color=BLUE, size=24):
    """a dashed 'missing' chip"""
    t = T(text, size, color)
    box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=t.width + 0.44, height=t.height + 0.44,
                                          stroke_color=color, stroke_width=3), num_dashes=24)
    back = RoundedRectangle(corner_radius=0.14, width=t.width + 0.44, height=t.height + 0.44, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(box)
    return VGroup(back, box, t.move_to(box))


def xmark(c, size=0.28, w=7):
    return VGroup(Line(c + [-size, size, 0], c + [size, -size, 0], color=RED, stroke_width=w),
                  Line(c + [-size, -size, 0], c + [size, size, 0], color=RED, stroke_width=w))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def lab(text, color, xl, y, size=24):
    t = T(text, size, color)
    return t.move_to([xl + t.width / 2, y, 0])


def lead(p1, p2, color=GREY):
    return Line([p1[0], p1[1], 0], [p2[0], p2[1], 0], color=color, stroke_width=2.5)


def pulse(scene, circ, color=GREEN, rt=0.9):
    dots = [Dot(e.get_start(), radius=0.1, color=color) for e in circ.edges]
    scene.add(*dots)
    scene.play(*[d.animate.move_to(e.get_end()) for d, e in zip(dots, circ.edges)], run_time=rt, rate_func=linear)
    scene.play(*[FadeOut(d) for d in dots], run_time=0.2)


# ---------------------------------------------------------------- the synapse (same shape in every scene)
class Syn:
    def __init__(self, x0=0.0):
        self.x0 = x0
        st = dict(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.15)
        self.pre = RoundedRectangle(corner_radius=0.35, width=6.4, height=1.7, **st).move_to([x0, 2.55, 0])
        self.post = RoundedRectangle(corner_radius=0.35, width=6.4, height=2.4, **st).move_to([x0, -0.7, 0])
        bs = dict(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.45)
        self.nrx = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.7, height=0.6, **bs).move_to([x0 + dx, 1.4, 0])
                            for dx in (-1.6, 1.6)])
        self.nlg = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.7, height=0.6, **bs).move_to([x0 + dx, 0.8, 0])
                            for dx in (-1.6, 1.6)])
        self.scaf = RoundedRectangle(corner_radius=0.15, width=5.0, height=0.6, **bs).move_to([x0, -0.1, 0])
        self.recs = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.4, height=0.6, stroke_color=TEXT,
                                              stroke_width=3, fill_color=TEXT, fill_opacity=0.35
                                              ).move_to([x0 + dx, 0.5, 0]) for dx in (-2.8, 0, 2.8)])
        ys = [-0.95, -1.45, -0.95, -1.45, -0.95, -1.45]
        xs = [-2.2, -1.2, -0.2, 0.8, 1.8, 2.6]
        self.ribo = VGroup(*[Circle(radius=0.17, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                                    fill_opacity=0.6).move_to([x0 + x, y, 0]) for x, y in zip(xs, ys)])

    def base(self):
        return VGroup(self.pre, self.post)

    def full(self, ribo=False, recs=True):
        g = VGroup(self.pre, self.post, self.nrx, self.nlg, self.scaf)
        if recs:
            g.add(self.recs)
        if ribo:
            g.add(self.ribo)
        return g

    def glow(self, which, color):
        for part in which:
            part.set_stroke(color).set_fill(color, 0.5)

    def labels(self, which=("nrx", "nlg", "scaf")):
        x0, xl = self.x0, self.x0 + 3.55
        d = {}
        if "nrx" in which:
            d["nrx"] = VGroup(lead([xl - 0.1, 1.4], [x0 + 1.97, 1.4]), lab("neurexin", TEXT, xl, 1.4))
        if "nlg" in which:
            d["nlg"] = VGroup(lead([xl - 0.1, 0.8], [x0 + 1.97, 0.8]), lab("neuroligin", TEXT, xl, 0.8))
        if "scaf" in which:
            d["scaf"] = VGroup(lead([xl - 0.1, -0.1], [x0 + 2.52, -0.1]), lab("scaffold", TEXT, xl, -0.1))
        if "recs" in which:
            d["recs"] = VGroup(lead([x0 - 3.45, 0.5], [x0 - 3.05, 0.5]),
                               lab("receptors", TEXT, x0 - 5.35, 0.5))
        if "ribo" in which:
            d["ribo"] = VGroup(lead([xl - 0.1, -1.2], [x0 + 2.85, -1.2]), lab("ribosomes", TEAL, xl, -1.2))
        return d


# ---------------------------------------------------------------- the three tags (left column)
TAGY = [1.4, -0.1, -1.5]
TAGTXT = ["1  build and hold", "2  protein amount", "3  gene choice"]
TAGCOL = [BLUE, TEAL, PURPLE]


def tag_chip(i, size=26):
    c = bchip(TAGTXT[i], TAGCOL[i], size)
    return c.move_to([0, 0, 0]).align_to([-6.65, 0, 0], LEFT).set_y(TAGY[i])


def tag_circle(i):
    c = VGroup(Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1),
               T(str(i + 1), 28, GREY))
    c[1].move_to(c[0])
    return c.move_to([-6.25, TAGY[i], 0])


# ---------------------------------------------------------------- grid of tests
COLX = {1: -1.05, 2: 4.05}
COLW, ROWH = 4.9, 1.6
ROWY = [1.7, 0.0, -1.7]
HDRY = 3.1
ROWNAME = ["build only", "upkeep only", "both"]


def grid_cells():
    cs = VGroup()
    for r in range(3):
        for c in (1, 2):
            cs.add(RoundedRectangle(corner_radius=0.15, width=COLW, height=ROWH, stroke_color=GREY,
                                    stroke_width=2.5, fill_opacity=0).move_to([COLX[c], ROWY[r], 0]))
    return cs


def hdr(c):
    return T("restore late" if c == 1 else "delete late", 34, TEXT, weight=BOLD).move_to([COLX[c], HDRY, 0])


def rowlabels():
    return VGroup(*[T(n, 28, GREY).move_to([-5.0, ROWY[i], 0]) for i, n in enumerate(ROWNAME)])


def cell_txt(r, c, text, color, size=34):
    return T(text, size, color).move_to([COLX[c], ROWY[r], 0])


def row3_help():
    t = T("may help:", 26, GREEN).move_to([COLX[1], ROWY[2] + 0.38, 0])
    chips = VGroup(chip("full", GREEN, 26, pad=0.15), chip("partial", GREEN, 26, pad=0.15),
                   chip("none", GREEN, 26, pad=0.15)).arrange(RIGHT, buff=0.12).move_to([COLX[1], ROWY[2] - 0.32, 0])
    return t, chips


def row_box(r):
    return RoundedRectangle(corner_radius=0.15, width=13.0, height=ROWH + 0.1, stroke_color=TEXT,
                            stroke_width=3.5, fill_opacity=0).move_to([0.05, ROWY[r], 0])


def filled(upto=3, row3=True):
    """static filled cells for rows 0..upto-1 (list of mobjects)"""
    out = []
    if upto >= 1:
        out += [cell_txt(0, 1, "no effect", GREY), cell_txt(0, 2, "no effect", GREY)]
    if upto >= 2:
        out += [cell_txt(1, 1, "helps", GREEN), cell_txt(1, 2, "harms", RED)]
    if upto >= 3:
        t, ch = row3_help()
        out += [t, ch, cell_txt(2, 2, "harms", RED)]
    return out


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "Disorders of the Synapse"
    TITLE = "Built, Then Kept"


def gene_cluster(i, compact=False):
    center = [-4.3 + 4.3*i, 0.0, 0] if not compact else [-5.0, TAGY[i], 0]
    n = (34, 33, 33)[i]
    return VGroup(*[Dot([center[0]+(j%7-3)*0.25, center[1]+(j//7-2)*0.28, 0],
                       radius=0.08, color=TAGCOL[i]) for j in range(n)])


def job_stage():
    # One large synapse and a contiguous dendrite; the stage stays fixed across jobs.
    syn = Syn(1.5)
    syn.full().scale(0.88, about_point=[1.5, 1.0, 0]).shift(UP*0.1)
    syn.glow([syn.nrx, syn.nlg, syn.scaf], BLUE)
    dend = RoundedRectangle(width=6.1, height=1.2, corner_radius=0.2,
        stroke_color=GREY, fill_color=GREY, fill_opacity=0.1).move_to([1.5,-2.1,0])
    rib = VGroup(*[Circle(radius=0.22, color=TEAL, fill_opacity=0.55).move_to([x,-2.1,0])
                  for x in (0.0, 1.1, 2.2)])
    rl = T("ribosomes",26,TEAL).move_to([3.6,-2.1,0])
    dl = T("dendrite",26,GREY).move_to([3.5,-2.95,0])
    nuc = Ellipse(width=2.1,height=1.55,color=PURPLE,stroke_width=5,
                  fill_color=PURPLE,fill_opacity=0.45).move_to([-2.8,-2.55,0])
    glow = VGroup(*[Ellipse(width=2.1+d,height=1.55+d,stroke_color=PURPLE,
                            stroke_width=8,stroke_opacity=0.09).move_to(nuc)
                    for d in (0.12,0.26,0.40)])
    nl = T("nucleus",26,PURPLE).move_to([-2.8,-3.62,0])
    return syn, VGroup(dend,dl), VGroup(rib,rl), VGroup(glow,nuc,nl)


def jobs(scene, done=0):
    syn, dend, rib, nuc = job_stage()
    scene.add(syn.full(), dend)
    if done>=2: scene.add(rib)
    if done>=3: scene.add(nuc)
    scene.job_tokens=[]
    for i in range(3):
        token=tag_chip(i) if i<done else gene_cluster(i,True)
        scene.job_tokens.append(token)
        scene.add(token)
    return syn,dend,rib,nuc


class S01Q(SpokenScene):
    def construct(self):
        syn=Syn(0)
        syn.full().stretch(1.35,0).scale(1.08).shift(DOWN*0.65)
        labels=VGroup(T("neurexin",26).move_to([5.65,1.55,0]),
                      T("neuroligin",26).move_to([5.65,0.75,0]),
                      T("receptors",26).move_to([-5.55,-0.1,0]),
                      T("scaffold",26,BLUE).move_to([5.65,-0.85,0]))
        leaders=VGroup(Line(syn.nrx[-1].get_right(),labels[0].get_left(),color=GREY),
                        Line(syn.nlg[-1].get_right(),labels[1].get_left(),color=GREY),
                        Line(labels[2].get_right(),syn.recs[0].get_left(),color=GREY),
                        Line(syn.scaf.get_right(),labels[3].get_left(),color=GREY))
        self.add(syn.base())
        self.at("built in development")
        self.play(FadeIn(syn.nrx,shift=DOWN*0.3),FadeIn(syn.nlg,shift=UP*0.3),
                  FadeIn(VGroup(*labels[:2],*leaders[:2])),run_time=0.45)
        self.wait(0.25)
        self.play(FadeIn(syn.recs),FadeIn(labels[2]),Create(leaders[2]),run_time=0.4)
        self.wait(0.25)
        self.play(GrowFromCenter(syn.scaf),FadeIn(labels[3]),Create(leaders[3]),run_time=0.4)
        self.wait(0.3)
        self.at("born without")
        cross=xmark(syn.scaf.get_center(),0.3)
        q=T("?",52,YELLOW).move_to([0,3.5,0])
        self.play(syn.scaf.animate.set_stroke(BLUE).set_fill(BLUE,0.08),Create(cross),FadeIn(q),run_time=0.5)
        self.at("wrong for good")
        self.play(FadeIn(T("wrong for good?",38,YELLOW).move_to([0,-3.5,0])),run_time=0.4)
        self.finish()


class S02Dx(SpokenScene):
    def construct(self):
        board=RoundedRectangle(width=6.2,height=6.1,corner_radius=0.2,color=GREY).move_to([-3.2,0,0])
        title=T("behaviour",36).move_to([-3.2,2.5,0])
        rows=VGroup()
        for y,txt in zip((1.2,-0.2,-1.6),("social communication","repeated behaviours","developmental history")):
            rows.add(VGroup(Square(0.35,color=GREY).move_to([-5.7,y,0]),T(txt,26).move_to([-3.0,y,0])))
        icons=[]
        # A helix is a test icon, not a molecular structure: two unconnected sine curves.
        helix=VGroup(*[ParametricFunction(lambda t,k=k: np.array([0.32*np.sin(5*t+k),t,0]),
                        t_range=[-0.5,0.5],color=GREY) for k in (0,PI)])
        tube=VGroup(Line([-0.25,0.5,0],[-0.25,-0.3,0],color=GREY),
                    Arc(radius=0.25,start_angle=PI,angle=PI,color=GREY).shift(DOWN*0.3),
                    Line([0.25,-0.3,0],[0.25,0.5,0],color=GREY))
        scan=VGroup(Circle(radius=0.5,color=GREY),Rectangle(width=1.2,height=0.18,color=GREY).shift(DOWN*0.5))
        for y,icon,txt in zip((2,0,-2),(helix,tube,scan),("gene test","blood test","scan")):
            icon.move_to([1.1,y,0]); label=T(txt,30,GREY).move_to([3.5,y,0])
            icons.append(VGroup(icon,label))
        self.add(board,title,rows,*icons)
        self.at("from behavior")
        self.play(*[Create(VMobject(color=GREEN,stroke_width=5).set_points_as_corners(
            [r[0].get_center()+v for v in (np.array([-0.12,0,0]),np.array([0,-0.12,0]),np.array([0.2,0.15,0]))])) for r in rows],run_time=0.5)
        for cue,obj in zip(("from a gene","blood","scan test"),icons):
            self.at(cue)
            self.play(Create(xmark(obj[0].get_center(),0.6)),run_time=0.35)
        self.finish()


class S03Genes(SpokenScene):
    def construct(self):
        rng=np.random.default_rng(7)
        clusters=[gene_cluster(i) for i in range(3)]
        dots=VGroup(*[d for g in clusters for d in g])
        targets=[d.get_center().copy() for d in dots]
        for d in dots: d.move_to([rng.uniform(-5.8,5.8),rng.uniform(-2.3,2.7),0]).set_color(GREY)
        self.add(dots,T("about 100 genes",44).move_to([0,-3.1,0]))
        self.at("strong evidence")
        self.play(*[d.animate.shift([0.12*np.sin(i),0.15*np.cos(i),0]) for i,d in enumerate(dots)],run_time=0.45)
        self.at("in autism")
        self.play(*[d.animate.move_to(pos).set_color(TAGCOL[0 if i<34 else 1 if i<67 else 2])
                    for i,(d,pos) in enumerate(zip(dots,targets))],run_time=0.65)
        self.finish()


class S04Job1(SpokenScene):
    def construct(self):
        clusters=[gene_cluster(i) for i in range(3)]
        self.add(*clusters)
        self.at("three jobs")
        syn,dend,rib,nuc=job_stage()
        self.play(*[Transform(c,gene_cluster(i,True)) for i,c in enumerate(clusters)],FadeIn(syn.full()),FadeIn(dend),run_time=0.6)
        self.at("build and hold")
        self.play(FadeOut(clusters[0],scale=0.05),FadeIn(tag_chip(0)),run_time=0.35)
        labels=VGroup(T("neurexin",26,BLUE).move_to([5.5,1.9,0]),T("neuroligin",26,BLUE).move_to([5.5,1.1,0]),
                      T("scaffold",26,BLUE).move_to([5.5,-0.4,0]))
        leaders=VGroup(Line(syn.nrx[-1].get_right(),labels[0].get_left(),color=BLUE),
                       Line(syn.nlg[-1].get_right(),labels[1].get_left(),color=BLUE),
                       Line(syn.scaf.get_right(),labels[2].get_left(),color=BLUE))
        self.play(FadeIn(leaders),FadeIn(labels),Indicate(syn.scaf,color=BLUE,scale_factor=1),run_time=0.6)
        self.finish()


class S05Job2(SpokenScene):
    def construct(self):
        syn,dend,rib,nuc=jobs(self,1)
        self.at("how much protein")
        self.play(FadeOut(self.job_tokens[1],scale=0.05),FadeIn(tag_chip(1)),FadeIn(rib),run_time=0.35)
        proteins=VGroup(*[Square(0.18,color=TEAL,fill_opacity=1).move_to([x,-1.85,0]) for x in (0,1.1,2.2)])
        self.add(proteins)
        self.play(*[p.animate.shift(UP*1.2) for p in proteins],rib[0].animate.set_fill(TEAL,1),run_time=0.6)
        self.play(FadeOut(proteins),run_time=0.2)
        self.finish()


class S06Job3(SpokenScene):
    def construct(self):
        syn,dend,rib,nuc=jobs(self,2)
        self.at("which genes")
        self.play(FadeOut(self.job_tokens[2],scale=0.05),FadeIn(tag_chip(2)),FadeIn(nuc),run_time=0.3)
        route=VMobject().set_points_as_corners(
            [[-1.75,-2.55,0],[-0.8,-2.1,0],[1.5,-2.1,0],[1.5,-1.2,0],[1.5,-0.3,0]])
        self.add(route.copy().set_stroke(PURPLE,width=4,opacity=0.65))
        self.at("the neuron uses")
        pulses=VGroup(*[Dot(route.get_start(),radius=0.16,color=PURPLE) for _ in range(3)])
        self.add(pulses)
        self.play(LaggedStart(*[MoveAlongPath(d,route) for d in pulses],lag_ratio=0.28),
                  Indicate(nuc[1],color=PURPLE,scale_factor=1.05),run_time=1.1)
        # Keep the message trail visible after the short spoken sentence.
        self.play(*[d.animate.move_to(route.point_from_proportion(t))
                    for d,t in zip(pulses,(0.25,0.55,0.85))],run_time=0.2)
        self.finish()


class S07Meet(SpokenScene):
    def construct(self):
        syn,dend,rib,nuc=jobs(self,3)
        self.at("meet at the synapse")
        arrows=VGroup(arr([-2.5,1.4,0],syn.nlg[0].get_left(),BLUE),
                      arr([-2.5,-0.1,0],rib[0][0].get_top(),TEAL),
                      VGroup(VMobject(color=PURPLE,stroke_width=5).set_points_as_corners(
                          [[-1.75,-2.55,0],[-0.8,-2.1,0],[1.5,-2.1,0]]),
                          arr([1.5,-2.1,0],syn.scaf.get_bottom(),PURPLE)))
        self.play(FadeIn(arrows),run_time=0.4)
        self.at("Each can change")
        note=T("three ways that can change one synapse",26).move_to([0,3.55,0])
        self.play(FadeIn(note),run_time=0.3)
        self.at("what it is made of")
        parts=VGroup(T("scaffold",26,BLUE).move_to([5.5,-0.4,0]),T("receptors",26).move_to([5.5,0.6,0]))
        part_leaders=VGroup(Line(syn.scaf.get_right(),parts[0].get_left(),color=BLUE),
                            Line(syn.recs[-1].get_right(),parts[1].get_left(),color=GREY))
        self.add(part_leaders,parts)
        changed=VGroup(T("scaffold parts",26,BLUE).move_to(parts[0]),
                       T("receptor parts",26).move_to(parts[1]))
        new_leaders=VGroup(Line(syn.scaf.get_right(),changed[0].get_left(),color=BLUE),
                           Line(syn.recs[-1].get_right(),changed[1].get_left(),color=GREY))
        self.play(Transform(parts,changed),Transform(part_leaders,new_leaders),syn.scaf.animate.set_fill(BLUE,0.8),
                  syn.recs.animate.set_fill(TEXT,0.65),run_time=0.4)
        self.at("how strongly it responds")
        self.play(Indicate(syn.recs,color=YELLOW,scale_factor=1.12),run_time=0.65)
        self.play(syn.recs.animate.set_fill(TEXT,0.8),run_time=0.25)
        self.finish()


# ---------------------------------------------------------------- mouse and timeline
def mouse(center, sc=1.0, color=GREY):
    body = Ellipse(width=1.7, height=0.9, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3)
    head = Ellipse(width=0.75, height=0.55, stroke_color=color, stroke_width=4, fill_color=color,
                   fill_opacity=0.3).move_to([0.95, 0.1, 0])
    ear = Circle(radius=0.2, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3).move_to([0.82, 0.42, 0])
    eye = Dot([1.1, 0.2, 0], radius=0.05, color=TEXT)
    tail = ArcBetweenPoints([-0.85, 0.0, 0], [-1.7, -0.2, 0], angle=-1.2, color=color, stroke_width=4)
    g = VGroup(tail, body, head, ear, eye)
    return g.scale(sc).move_to([center[0], center[1], 0])


class S08Mouse(SpokenScene):
    def construct(self):
        axis = arr([-6.1, 0.1, 0], [6.4, 0.1, 0], GREY, w=5)
        birth = T("birth", 28, GREY).move_to([-5.3, -0.55, 0])
        self.add(axis,birth,T("age",30,GREY).move_to([0,-0.55,0]))
        self.add(T("early building → later symptoms",36).move_to([0,-3.2,0]))
        self.at("early")
        win = Rectangle(width=5.2, height=2.8, stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                        fill_opacity=0.22).move_to([-5.45 + 2.6, 1.5, 0])
        wl = T("building", 34, GOLD).move_to(win)
        self.play(GrowFromEdge(win, LEFT), FadeIn(wl), run_time=1.0)
        self.at("windows that close")
        win2 = Rectangle(width=4.5, height=2.8, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.12).move_to([-5.45 + 2.25, 1.5, 0])
        self.play(Transform(win, win2), Transform(wl,T("window closes",30,GREY).move_to(win2)), run_time=1.0)
        self.at("Picture a mouse")
        m = mouse([-3.5, -1.6], 1.65)
        self.play(FadeIn(m, shift=UP * 0.2), run_time=0.5)
        self.at("without one synapse protein")
        d = dchip("one synapse protein", BLUE, 26).move_to([1.0, -2.4, 0])
        sl = xmark(np.array([3.5, -2.4, 0]), 0.28)
        self.play(FadeIn(d), run_time=0.4)
        self.play(Create(sl), run_time=0.3)
        self.at("with symptoms")
        mk = DashedLine([4.9, 0.1, 0], [4.9, 2.5, 0], color=RED, stroke_width=5)
        sy = bchip("symptoms", RED, 30).move_to([4.9, 3.0, 0])
        self.play(Create(mk), FadeIn(sy, shift=DOWN * 0.15), run_time=0.7)
        self.at("young adulthood")
        ya = T("young adulthood", 26, GREY).move_to([4.6, -0.6, 0])
        self.play(FadeIn(ya), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- two histories
def panel(cx, cy, s=1.0, frame_color=GREY):
    frame = RoundedRectangle(corner_radius=0.25, width=6.1, height=6.1, stroke_color=frame_color, stroke_width=4,
                             fill_color=GREY, fill_opacity=0.05)
    circ = make_circuit((0, 0), 1.1, GREY)
    pc = dchip("no protein", BLUE, 26).move_to([0, 2.6, 0])
    g = VGroup(frame, circ, pc)
    g.frame, g.circ, g.pc = frame, circ, pc
    g.scale(s, about_point=ORIGIN).shift([cx, cy, 0])
    return g


A_POS, B_POS, PY = (-3.3, 0.0), (3.3, 0.0), 0.0


def wrong_edges(circ):
    return VGroup(*[Line(circ.nodes[a].get_center(), circ.nodes[b].get_center(), color=RED, stroke_width=6)
                    for a, b in ((1, 2), (4, 5))])


class S09H1(SpokenScene):
    def construct(self):
        p = panel(0, 0.0, 1.0, GOLD)
        under = T("built wrong", 38, RED).move_to([0, -2.5, 0])
        title=T("history 1: building",34,GOLD).move_to([0,3.4,0])
        self.add(p.frame,p.circ.copy().set_opacity(0.18),title)
        self.at("the protein was needed")
        self.play(FadeIn(p.pc, shift=DOWN * 0.2), run_time=0.5)
        self.at("to build the circuit")
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in p.circ.nodes], lag_ratio=0.1),
                  LaggedStart(*[Create(e) for e in p.circ.edges], lag_ratio=0.1), run_time=1.5)
        self.at("was built wrong")
        w = wrong_edges(p.circ)
        self.play(LaggedStart(*[Create(e) for e in w], lag_ratio=0.4), run_time=0.55)
        self.play(FadeIn(under),run_time=0.35)
        self.at("window has closed")
        cl = T("window closed", 30, GREY).move_to([0, 3.4, 0])
        self.remove(title)
        shutters=VGroup(Line([-3.05,3.05,0],[0,3.05,0],color=GOLD,stroke_width=10),Line([3.05,3.05,0],[0,3.05,0],color=GOLD,stroke_width=10))
        self.play(p.frame.animate.set_stroke(GREY),Create(shutters), FadeIn(cl), run_time=0.6)
        self.finish()


class S10H2(SpokenScene):
    def construct(self):
        pa = panel(0, 0.0, 1.0, GREY)
        pa.circ.set_color(GREY)
        w = wrong_edges(pa.circ)
        under = T("built wrong", 38, RED).move_to([0, -2.5, 0])
        grp = VGroup(pa, w)
        self.add(grp, under)
        self.play(grp.animate.shift([A_POS[0], A_POS[1], 0]),
                  under.animate.scale(32 / 38).move_to([A_POS[0], -2.5, 0]), run_time=0.8)
        self.at("circuit was built well")
        pb = panel(*B_POS, 1.0, GREY)
        well=T("built well",32,GREEN).move_to([B_POS[0],-2.5,0])
        self.play(FadeIn(pb.frame),FadeIn(well),FadeIn(pb.pc),run_time=0.3)
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in pb.circ.nodes], lag_ratio=0.1),
                  LaggedStart(*[Create(e) for e in pb.circ.edges], lag_ratio=0.1), run_time=1.0)
        self.play(pb.circ.edges.animate.set_color(GREEN), pb.circ.nodes.animate.set_color(GREEN), run_time=0.4)
        self.at("but it cannot run")
        self.play(pb.circ.edges.animate.set_stroke(opacity=0.25), pb.circ.nodes.animate.set_fill(opacity=0.1),
                  run_time=0.5)
        self.at("without the protein")
        ub = T("built, not kept", 32, AMBER).move_to([B_POS[0], -2.5, 0])
        self.play(ReplacementTransform(well,ub),run_time=0.3)
        for _ in range(2):
            self.play(pb.circ.edges.animate.set_stroke(opacity=0.7), run_time=0.25)
            self.play(pb.circ.edges.animate.set_stroke(opacity=0.2), run_time=0.35)
        self.finish()


def two_panels(scene):
    pa = panel(*A_POS, 1.0, GREY)
    pa.circ.set_color(GREY)
    w = wrong_edges(pa.circ)
    pb = panel(*B_POS, 1.0, GREY)
    pb.circ.edges.set_color(GREEN).set_stroke(opacity=0.25)
    pb.circ.nodes.set_color(GREEN).set_fill(opacity=0.1)
    ua = T("built wrong", 32, RED).move_to([A_POS[0], -2.5, 0])
    ub = T("built, not kept", 32, AMBER).move_to([B_POS[0], -2.5, 0])
    scene.add(pa, w, pb, ua, ub)
    return pa, pb, ua, ub


class S11Same(SpokenScene):
    def construct(self):
        pa, pb, ua, ub = two_panels(self)
        self.at("symptoms look")
        sy = bchip("same symptoms", RED, 30).move_to([0, -3.5, 0])
        self.play(FadeIn(sy, shift=UP * 0.15), run_time=0.5)
        self.at("the same either way")
        a1 = arr([A_POS[0] + 0.5, -2.6, 0], [-1.6, -3.2, 0], RED)
        a2 = arr([B_POS[0] - 0.5, -2.6, 0], [1.6, -3.2, 0], RED)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- predict
def switch(color, on):
    pill = RoundedRectangle(corner_radius=0.75, width=3.0, height=1.5, stroke_color=color, stroke_width=5,
                            fill_color=color, fill_opacity=0.25)
    knob = Circle(radius=0.55, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9)
    knob.move_to(pill.get_right() + LEFT * 0.75 if on else pill.get_left() + RIGHT * 0.75)
    return VGroup(pill, knob)


def pred_static(scene, sw_on=False, handle_i=5):
    sw=switch(GREEN if sw_on else RED,sw_on).scale(1.45).move_to([-3.4,0.2,0])
    return dict(pred=T("Predict.",54,YELLOW).move_to([0,3.05,0]),sw=sw,
        gl=T("gene",32).move_to([-3.4,1.85,0]),
        onoff=T("on" if sw_on else "off",32,GREEN if sw_on else RED).move_to([-3.4,-1.4,0]),
        line=Line([0.6,0.2,0],[5.9,0.2,0],color=GREY,stroke_width=6),
        ticks=VGroup(*[Line([x,-0.05,0],[x,0.45,0],color=GREY) for x in np.linspace(0.6,5.9,6)]),
        handle=Circle(radius=0.4,color=TEXT,fill_opacity=1).move_to([np.linspace(0.6,5.9,6)[handle_i],0.2,0]),
        al=T("age: early → late",32).move_to([3.3,1.85,0]),
        histories=VGroup(bchip("built wrong?",RED,28).move_to([-3.2,-2.35,0]),
                         bchip("built, not kept?",AMBER,28).move_to([3.2,-2.35,0])),
        q=T("Which two late experiments tell these apart?",32,YELLOW).move_to([0,-3.35,0]))


class S12Pred(SpokenScene):
    def construct(self):
        o=pred_static(self,False,0)
        self.add(o['pred'],o['histories'],o['line'],o['ticks'],o['al'],o['handle'])
        self.at("switch the gene")
        self.play(FadeIn(o['sw']),FadeIn(o['gl']),FadeIn(o['onoff']),run_time=0.3)
        self.at("gene on")
        self.play(Transform(o['sw'],switch(GREEN,True).scale(1.45).move_to([-3.4,0.2,0])),
                  Transform(o['onoff'],T("on",32,GREEN).move_to([-3.4,-1.4,0])),run_time=0.3)
        self.at("or off")
        self.play(Transform(o['sw'],switch(RED,False).scale(1.45).move_to([-3.4,0.2,0])),
                  Transform(o['onoff'],T("off",32,RED).move_to([-3.4,-1.4,0])),run_time=0.3)
        self.at("at any age")
        self.add(o['line'],o['ticks'],o['al'],o['handle'])
        self.play(o['handle'].animate.move_to([3.25,0.2,0]),
                  Transform(o['sw'],switch(GREEN,True).scale(1.45).move_to([-3.4,0.2,0])),
                  Transform(o['onoff'],T("on",32,GREEN).move_to([-3.4,-1.4,0])),run_time=0.55)
        self.play(o['handle'].animate.move_to([5.9,0.2,0]),
                  Transform(o['sw'],switch(RED,False).scale(1.45).move_to([-3.4,0.2,0])),
                  Transform(o['onoff'],T("off",32,RED).move_to([-3.4,-1.4,0])),run_time=0.55)
        self.at("late experiments")
        self.play(FadeIn(o['q']),run_time=0.3)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        self.add(*pred_static(self).values())
        ring=Circle(radius=0.32,color=GREY).move_to([0,0.2,0])
        progress=Arc(radius=0.32,start_angle=PI/2,angle=-TAU+0.01,color=YELLOW,stroke_width=6).move_to(ring)
        self.add(ring)
        self.play(Create(progress),run_time=4.8,rate_func=linear)
        self.wait(0.2)


# ---------------------------------------------------------------- the grid
def test_intro():
    boxes=VGroup(*[RoundedRectangle(width=5.5,height=4.9,corner_radius=0.2,color=GREY).move_to([x,-0.4,0]) for x in (-3.1,3.1)])
    return boxes


class S14T1(SpokenScene):
    def construct(self):
        boxes=test_intro()
        self.add(boxes)
        self.at("put the gene back")
        self.play(FadeIn(T("restore late",34,weight=BOLD).move_to([-3.1,2.7,0])),run_time=0.3)
        sw=switch(GREEN,True).move_to([-3.1,0.2,0])
        self.play(FadeIn(sw),FadeIn(T("after symptoms",30).move_to([-3.1,-1.6,0])),run_time=0.4)
        self.finish()


class S15T2(SpokenScene):
    def construct(self):
        self.add(test_intro(),T("restore late",34,weight=BOLD).move_to([-3.1,2.7,0]),
                 switch(GREEN,True).move_to([-3.1,0.2,0]),T("after symptoms",30).move_to([-3.1,-1.6,0]))
        self.at("take it away")
        self.play(FadeIn(T("delete late",34,weight=BOLD).move_to([3.1,2.7,0])),
                  FadeIn(switch(RED,False).move_to([3.1,0.2,0])),run_time=0.4)
        self.at("typical mouse")
        self.play(FadeIn(T("typical mouse",30).move_to([3.1,-1.6,0])),run_time=0.3)
        self.at("after its circuit")
        self.play(FadeIn(T("after building",30).move_to([3.1,-2.35,0])),run_time=0.3)
        self.finish()


def grid_base(scene, upto=0):
    cells = grid_cells()
    scene.add(cells, hdr(1), hdr(2), *[rowlabels()[i] for i in range(upto)], *filled(upto))
    return cells


class S16Build(SpokenScene):
    def construct(self):
        grid_base(self)
        self.at("only to build")
        box = row_box(0)
        self.play(FadeIn(rowlabels()[0]),Create(box), run_time=0.5)
        self.at("damage cannot be repaired")
        note = T("if the damage cannot be repaired", 28, GREY).move_to([0, -3.15, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.at("both tests")
        self.play(FadeIn(cell_txt(0, 1, "no effect", GREY)), FadeIn(cell_txt(0, 2, "no effect", GREY)), run_time=0.5)
        self.finish()


class S17Keep(SpokenScene):
    def construct(self):
        grid_base(self, 1)
        self.add(T("if the damage cannot be repaired",28,GREY).move_to([0,-3.15,0]))
        box = row_box(0)
        self.add(box)
        self.at("keeps the circuit running")
        self.play(FadeIn(rowlabels()[1]),box.animate.move_to([0.05, ROWY[1], 0]), run_time=0.5)
        self.at("restoring it helps")
        self.play(FadeIn(cell_txt(1, 1, "helps", GREEN), scale=1.2), run_time=0.4)
        self.at("removing it harms")
        self.play(FadeIn(cell_txt(1, 2, "harms", RED), scale=1.2), run_time=0.4)
        self.finish()


class S18Both(SpokenScene):
    def construct(self):
        grid_base(self, 2)
        self.add(T("if the damage cannot be repaired",28,GREY).move_to([0,-3.15,0]))
        box = row_box(1)
        self.add(box)
        self.at("does both")
        self.play(FadeIn(rowlabels()[2]),box.animate.move_to([0.05, ROWY[2], 0]), run_time=0.5)
        t, chips = row3_help()
        self.at("restoring it may help")
        self.play(FadeIn(t), run_time=0.4)
        self.at("fully")
        self.play(FadeIn(chips[0], scale=0.8), run_time=0.3)
        self.at("partly")
        self.play(FadeIn(chips[1], scale=0.8), run_time=0.3)
        self.at("not at all")
        self.play(FadeIn(chips[2], scale=0.8), run_time=0.3)
        self.at("Removing it still")
        self.play(FadeIn(cell_txt(2, 2, "harms", RED), scale=1.2), run_time=0.4)
        self.finish()


def recap_grid():
    # Leave a band between each heading and its cells for its own question.
    g=VGroup(grid_cells(),rowlabels(),*filled(3))
    for cell in g[0]:
        y=cell.get_y()
        cell.stretch(0.78,1).set_y(y*0.78-0.35)
    for label in g[1]:
        label.set_y(label.get_y()*0.78-0.35)
    for content in g[2:]:
        content.set_y(content.get_y()*0.78-0.35)
    h1,h2=hdr(1).set_y(3.0),hdr(2).set_y(3.0)
    return g,h1,h2


def grid_footnote():
    return T("Assumes the gene returns or goes in enough cells.",28).move_to([0,-3.25,0])


class S19Need(SpokenScene):
    def construct(self):
        brain=Ellipse(width=7.2,height=5.3,color=GREY,fill_opacity=0.08).move_to([-2.5,-0.25,0])
        rng=np.random.default_rng(3)
        pts=[]
        while len(pts)<70:
            x,y=rng.uniform(-3.1,3.1),rng.uniform(-2.2,2.2)
            if (x/3.1)**2+(y/2.2)**2<1: pts.append([x-2.5,y-0.25,0])
        cells=VGroup(*[Dot(p,radius=0.1,color=GREEN if i in (5,14,27,41,52,63) else GREY) for i,p in enumerate(pts)])
        title=T("brain section, gene restored late",30).move_to([-2.0,3.1,0])
        restored=T("green: gene restored",28,GREEN).move_to([-2.5,-3.2,0])
        h1,h2=hdr(1),hdr(2)
        mini=VGroup(h1,h2).scale(0.8).move_to([0,2.4,0])
        r1=SurroundingRectangle(h1,color=YELLOW,buff=0.15)
        self.add(brain,cells,title,restored)
        self.at("A failed rescue")
        self.play(Indicate(VGroup(*[cells[i] for i in (5,14,27,41,52,63)]),scale_factor=1.2),run_time=0.4)
        chips=[bchip(txt,GREY,28).move_to([4.35,y,0]) for txt,y in zip(
            ("too few cells?","wrong level?","too short?","window closed?"),(2,0.6,-0.8,-2.2))]
        for cue,c in zip(("too few cells","wrong level","too briefly","window may have closed"),chips):
            self.at(cue)
            if any(x is not c for x in chips):
                for old in chips:
                    if old in self.mobjects:
                        old[1].set_stroke(GREY).set_fill(GREY,0.16)
                        old[2].set_color(GREY)
            c[1].set_stroke(YELLOW).set_fill(YELLOW,0.16)
            c[2].set_color(YELLOW)
            self.play(FadeIn(c),run_time=0.35)
        self.wait(0.5)
        # Restore is the failed rescue test; show it first before the deletion question.
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.25)
        g,h1,h2=recap_grid()
        r1=SurroundingRectangle(h1,color=YELLOW,buff=0.15)
        self.add(g,h1,h2,grid_footnote(),r1)
        self.at("Deletion asks")
        r2=SurroundingRectangle(h2,color=YELLOW,buff=0.15)
        self.play(FadeOut(r1),FadeIn(r2),run_time=0.3)
        self.at("You need both")
        self.play(FadeIn(r1),run_time=0.3)
        self.finish()


class S20Rule(SpokenScene):
    def construct(self):
        idea=T("Built, then kept.",64,font=TITLE_FONT).move_to([0,2.2,0])
        positions=(-4.2,0,4.2)
        labels=("build","keep","both")
        colors=(GOLD,GREEN,TEXT)
        chips=[]
        for x,txt,col in zip(positions,labels,colors):
            box=RoundedRectangle(width=3.3,height=1.55,corner_radius=0.2,color=col,fill_opacity=0.15)
            chips.append(VGroup(box,T(txt,42,col).move_to(box)).move_to([x,-0.15,0]))
        links=VGroup(Line([-2.55,-0.15,0],[-1.65,-0.15,0],color=GREY),
                     Line([1.65,-0.15,0],[2.55,-0.15,0],color=GREY))
        for c in chips:
            c[0].set_stroke(opacity=0.45).set_fill(opacity=0.08)
            c[1].set_opacity(0.45)
        self.add(idea,links,*chips)
        self.at("built")
        self.play(Indicate(idea,color=GOLD,scale_factor=1.02),run_time=0.4)
        self.at("then kept")
        self.play(FadeIn(T("Two late tests, read trait by trait.",32,YELLOW).move_to([0,-2.3,0])),run_time=0.35)
        for cue,c in zip(("to build a circuit","to keep it running","or both"),chips):
            self.at(cue)
            self.play(c[0].animate.set_stroke(opacity=1,width=5).set_fill(opacity=0.2),
                      c[1].animate.set_opacity(1),run_time=0.35)
        self.wait(1.0)
        self.finish()


class S21Take(SpokenScene):
    def construct(self):
        g,h1,h2=recap_grid()
        self.add(g,h1,h2)
        r1=SurroundingRectangle(h1,color=YELLOW,buff=0.15,stroke_width=4)
        r2=SurroundingRectangle(h2,color=YELLOW,buff=0.15,stroke_width=4)
        l1=T("can the trait recover?",28,YELLOW).move_to([COLX[1],2.04,0])
        l2=T("does the adult circuit still need it?",26,YELLOW).move_to([COLX[2],2.04,0])
        fit(l2,max_w=4.9)
        self.at("restore the gene")
        self.play(FadeIn(r1),run_time=0.25)
        self.at("delete it")
        self.play(FadeOut(r1),FadeIn(r2),run_time=0.25)
        self.at("One asks")
        self.play(FadeOut(r2),FadeIn(r1),FadeIn(l1),run_time=0.25)
        self.at("The other asks")
        self.play(FadeOut(r1),FadeOut(l1),FadeIn(r2),FadeIn(l2),run_time=0.25)
        self.at("still needs it")
        self.play(FadeIn(T("Neither rules out building.",30).move_to([0,-3.25,0])),run_time=0.3)
        self.finish()


class S22End(EndCard):
    LINE = "Restore late tests recovery; delete late tests whether adults still need it."

    def construct(self):
        line=T("Restore late tests recovery;\ndelete late tests whether adults still need it.",40,font=TITLE_FONT,line_spacing=1.2)
        fit(line,max_w=12.2)
        sub=T("biochemistrypedia.com",26,TEAL)
        VGroup(line,sub).arrange(DOWN,buff=0.65)
        self.play(FadeIn(line),run_time=0.6)
        self.play(FadeIn(sub),run_time=0.3)
        self.finish()
