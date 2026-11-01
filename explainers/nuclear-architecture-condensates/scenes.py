"""Nuclear architecture and membraneless compartments: change the amount, watch the bodies.

COLOR MAP (one color per concept, whole video)
  BLUE   = the protein (dots) and the dense bodies it forms
  PURPLE = chromatin: chromosome territories, binding sites, the bead chain
  TEAL   = the phase-separation hypothesis and its prediction
  YELLOW = the saturation concentration (the threshold)
  GREEN  = protein A (fits the prediction)
  ORANGE = protein B (does not fit it)
  RED    = a problem: the missing membrane, "cannot tell"
  GREY   = nucleus outline, axes, de-emphasized things
  TEXT   = neutral marks (the total on the plot, the amount arrow)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

C_SAT, C_DENSE = 1.0, 50.0


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def nucleus(c, r):
    return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to(c)


def pdot(p, color=BLUE, r=0.075):
    return Dot(p, radius=r, color=color)


def ring_points(n, c, r_in, r_out, seed, gap=0.3):
    """n points in an annulus around c, kept at least `gap` apart."""
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        a = rng.uniform(0, TAU)
        r = np.sqrt(rng.uniform(r_in ** 2, r_out ** 2))
        p = np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0])
        if all(np.linalg.norm(p - q) > gap for q in pts):
            pts.append(p)
    return pts


def cluster_points(n, c, step=0.15):
    """golden-spiral packing: a tight round cluster of n points."""
    return [np.array([c[0] + step * np.sqrt(k + 0.5) * np.cos(k * 2.4),
                      c[1] + step * np.sqrt(k + 0.5) * np.sin(k * 2.4), 0]) for k in range(n)]


def phi_of(total):
    return max(0.0, (total - C_SAT) / (C_DENSE - C_SAT))


def body(c, R, phi, **kw):
    return Circle(radius=max(R * np.sqrt(phi), 0.001), stroke_color=BLUE, stroke_width=3,
                  fill_color=BLUE, fill_opacity=0.55).move_to(c)


# the concentration plot used in scenes 3, 5 (same place both times)
O = np.array([-5.0, -2.5, 0.0])
U = 0.62   # scene units per micromolar


def P(x, y):
    return O + np.array([x * U, y * U, 0])


def make_axes():
    g = VGroup()
    g.add(Line(P(0, 0), P(8.4, 0), color=GREY, stroke_width=3), Line(P(0, 0), P(0, 8.2), color=GREY, stroke_width=3))
    for v in (2, 4, 6, 8):
        g.add(Line(P(v, 0), P(v, 0) + DOWN * 0.1, color=GREY, stroke_width=2),
              M(str(v), 22, GREY).move_to(P(v, 0) + DOWN * 0.34))
        g.add(Line(P(0, v), P(0, v) + LEFT * 0.1, color=GREY, stroke_width=2),
              M(str(v), 22, GREY).move_to(P(0, v) + LEFT * 0.34))
    g.add(T("total protein, µM", 24, TEXT).move_to(P(4.2, 0) + DOWN * 0.75))
    yl = T("protein outside the bodies, µM", 24, TEXT).rotate(PI / 2).move_to(P(0, 4.1) + LEFT * 0.95)
    g.add(yl)
    return g


def model_curve(upto=8.0):
    pts = [P(0, 0), P(C_SAT, C_SAT)] + ([P(upto, C_SAT)] if upto > C_SAT else [])
    if upto <= C_SAT:
        pts = [P(0, 0), P(upto, upto)]
    m = VMobject(stroke_color=TEAL, stroke_width=6)
    m.set_points_as_corners(pts)
    return m


def out_of(t):
    return min(t, C_SAT)


class S00Title(TitleCard):
    LESSON = "Nuclear architecture and membraneless compartments"
    TITLE = "A Nucleus Without Walls"



# Three territories are painted regions, not membrane enclosures.
def map_parts():
    c = np.array([-2.8, 0, 0])
    terrs = VGroup(*[Ellipse(width=w, height=h, stroke_width=0,
                    fill_color=PURPLE, fill_opacity=op).rotate(a * DEGREES).move_to(c + [x,y,0])
        for x,y,w,h,a,op in [(-1.1,.6,2.6,2.9,20,.18),(1.0,.8,2.5,2.7,-15,.3),(.1,-1.3,3.2,2.0,5,.42)]])
    nu = Circle(radius=.65, stroke_color=BLUE, stroke_width=3,
                fill_color=BLUE, fill_opacity=.55).move_to(c + [.1,.1,0])
    small = VGroup(*[Circle(radius=.17, stroke_color=BLUE, fill_color=BLUE,
                       fill_opacity=.55).move_to(c + v) for v in [[-1.9,-.6,0],[1.7,-.5,0]]])
    return nucleus(c,3.05), terrs, nu, small


class S01Map(SpokenScene):
    def construct(self):
        nuc, terrs, nu, small = map_parts()
        self.at("A nucleus")
        self.play(Create(nuc), run_time=.7)
        note = T("No internal membranes",28,RED).move_to([3.6,2.6,0])
        self.at("no membranes")
        self.play(FadeIn(note),run_time=.6)
        lab = T("Chromosome territories",28,PURPLE).move_to([3.6,1.45,0])
        self.at("Each chromosome")
        self.play(FadeIn(terrs),FadeIn(lab),run_time=1.0)
        active = T("Open, active",28,PURPLE).move_to([3.6,.45,0])
        quiet = T("Closed, quiet",28,PURPLE).move_to([3.6,-.25,0])
        self.at("and open")
        self.play(FadeIn(active),terrs[0].animate.set_fill(opacity=.3),run_time=.7)
        self.at("closed quiet")
        self.play(FadeIn(quiet),terrs[2].animate.set_fill(opacity=.5),run_time=.7)
        bodies = T("Small nuclear bodies",28,BLUE).move_to([3.6,-1.3,0])
        self.at("Membraneless bodies")
        self.play(FadeOut(active),FadeOut(quiet),FadeOut(lab),FadeIn(small),FadeIn(bodies),run_time=.7)
        nl = T("Nucleolus",32,BLUE,weight=BOLD).move_to([3.6,1.1,0])
        job = T("Ribosomal RNA\n+ subunit assembly",26,TEXT,line_spacing=1).move_to([3.6,0,0])
        self.at("The largest")
        self.play(GrowFromCenter(nu),FadeIn(nl),run_time=.7)
        self.at("which makes")
        self.play(FadeIn(job),run_time=.7)
        q = T("Together without walls?",30,TEXT,weight=BOLD).move_to([3.6,-2.65,0])
        self.at("So what holds")
        self.play(FadeOut(note),FadeIn(q),Indicate(nu,color=BLUE),run_time=.9)
        self.finish()


class S02Nucleolus(SpokenScene):
    def construct(self):
        c=np.array([-2.5,0,0])
        outer=Circle(radius=2.75,stroke_color=BLUE,stroke_width=3,fill_color=BLUE,fill_opacity=.22).move_to(c)
        middle=Circle(radius=1.8,stroke_color=BLUE,stroke_width=3,fill_color=BLUE,fill_opacity=.46).move_to(c)
        inner=Circle(radius=.8,stroke_color=GREY,stroke_width=3,fill_color=BG,fill_opacity=1).move_to(c)
        layers=VGroup(outer,middle,inner)
        ids=VGroup(T("FC",26,TEXT).move_to(c),T("DFC",26,TEXT).move_to(c+[0,1.3,0]),T("GC",26,TEXT).move_to(c+[0,2.28,0]))
        detail=T("Inside → out",32,TEXT).move_to([3.6,2.6,0])
        self.at("Read the nucleolus")
        self.play(FadeIn(layers),FadeIn(ids),FadeIn(detail),run_time=.8)
        fc=T("FC · fibrillar centre\nRibosomal genes",26,TEXT,line_spacing=1).move_to([3.6,1.1,0])
        dfc=T("DFC · dense fibrillar\nRNA processing",26,TEXT,line_spacing=1).move_to([3.6,1.1,0])
        gc=T("GC · granular component\nSubunit assembly",26,TEXT,line_spacing=1).move_to([3.6,1.1,0])
        self.at("holds the ribosomal")
        self.play(FadeIn(fc),Indicate(inner,color=TEXT,scale_factor=1.05),run_time=.7)
        self.at("Around it")
        self.play(ReplacementTransform(fc,dfc),Indicate(middle,color=BLUE,scale_factor=1.03),run_time=.8)
        self.at("The outer granular")
        self.play(ReplacementTransform(dfc,gc),Indicate(outer,color=BLUE,scale_factor=1.03),run_time=.8)
        sub=chip("subunit",BLUE,24).move_to(c+[2.15,-.6,0])
        self.at("before export")
        self.play(FadeIn(sub),run_time=.3)
        self.play(sub.animate.move_to([3.6,-.7,0]),run_time=.9)
        frog=T("Frog oocytes",28,TEXT).move_to([3.6,-1.65,0])
        liquids=T("Two coexisting liquids\nwithout mixing",26,BLUE,line_spacing=1).move_to([3.6,-2.65,0])
        self.at("In frog oocytes")
        self.play(FadeOut(sub),FadeIn(frog),run_time=.5)
        self.at("two liquids")
        self.play(FadeIn(liquids),run_time=.8)
        self.finish()

class S03Proposal(SpokenScene):
    """three ways to make a bright spot; all look the same; they differ when the amount changes."""

    def construct(self):
        cxs = [-4.2, 0.0, 4.2]
        cy, R = 0.9, 1.95
        nucs = [nucleus(np.array([x, cy, 0]), R) for x in cxs]
        labs = [T("phase separation", 26, TEAL), T("binding clustered sites", 26, PURPLE), T("bridging chromatin", 26, PURPLE)]
        for l, x in zip(labs, cxs):
            l.move_to([x, cy - R - 0.4, 0])

        # panel 1: dots demix into a drop
        c1 = np.array([cxs[0], cy, 0])
        start1 = ring_points(20, c1, 0.0, R - 0.3, 3, gap=0.3)
        tgt1 = cluster_points(14, c1 + np.array([0.25, 0.2, 0]), 0.14)
        d1 = VGroup(*[pdot(p) for p in start1])
        # panel 2: dots pile onto a cluster of sites on a DNA line
        c2 = np.array([cxs[1], cy, 0])
        line2 = Line(c2 + LEFT * (R - 0.15), c2 + RIGHT * (R - 0.15), color=PURPLE, stroke_width=4)
        sites = VGroup(*[Square(0.17, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.9).move_to(c2 + np.array([0.28 + 0.2 * (k - 2), 0, 0]))
                         for k in range(5)])
        start2 = ring_points(12, c2 + np.array([0, 0.0, 0]), 0.0, R - 0.3, 5, gap=0.32)
        start2 = [p for p in start2 if abs(p[1] - c2[1]) > 0.22][:10]
        d2 = VGroup(*[pdot(p) for p in start2])
        tgt2 = [c2 + np.array([0.28 + 0.2 * (k - 2), 0.2 + 0.0, 0]) for k in range(5)] + \
               [c2 + np.array([0.28 + 0.2 * (k - 2), -0.2, 0]) for k in range(4)]
        # panel 3: bead chain collapses
        c3 = np.array([cxs[2], cy, 0])
        xs = np.linspace(-R + 0.3, R - 0.3, 14)
        beads_start = [c3 + np.array([x, 0.45 * np.sin(1.7 * x + 0.5), 0]) for x in xs]
        beads_end = cluster_points(14, c3, 0.13)
        beads = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(p) for p in beads_start])
        chain = VMobject(stroke_color=PURPLE, stroke_width=3)
        chain.set_points_as_corners(beads_start)
        bridge = VGroup(*[pdot(beads_start[i] + np.array([0, 0.15, 0])) for i in (3, 7, 10)])

        self.at("One proposal")
        self.play(Create(nucs[0]), FadeIn(d1), FadeIn(labs[0]), run_time=0.8)
        self.at("Molecules with many")
        self.play(*[d1[k].animate.move_to(tgt1[k]) for k in range(14)], run_time=1.1)
        halo1 = Circle(radius=0.65, stroke_width=0, fill_color=BLUE, fill_opacity=0.28).move_to(c1 + [0.25, 0.2, 0])
        self.play(FadeIn(halo1), run_time=0.5)
        self.at("a bright spot")
        self.play(Create(nucs[1]), Create(nucs[2]), FadeIn(line2), FadeIn(sites),
                  FadeIn(d2), FadeIn(chain), FadeIn(beads), FadeIn(bridge), run_time=0.8)

        self.at("clustered sites")
        self.play(FadeIn(labs[1]), run_time=0.3)
        self.play(*[d2[k].animate.move_to(tgt2[k]) for k in range(min(len(d2), len(tgt2)))], run_time=1.1)

        self.at("bridge chromatin")
        self.play(FadeIn(labs[2]), run_time=0.3)
        self.play(*[beads[k].animate.move_to(beads_end[k]) for k in range(14)],
                  Transform(chain, VMobject(stroke_color=PURPLE, stroke_width=3).set_points_as_corners(beads_end)),
                  *[bridge[j].animate.move_to(beads_end[i]) for j, i in enumerate((3, 7, 10))], run_time=1.2)

        self.at("change the amount")
        arrow = Arrow(LEFT * 3.2, RIGHT * 3.2, color=TEXT, stroke_width=6, buff=0).move_to([0, -3.1, 0])
        al = T("change the amount of protein", 26, TEXT).next_to(arrow, UP, buff=0.12)
        self.play(GrowArrow(arrow), FadeIn(al), run_time=0.9)
        self.finish()



class S04Threshold(SpokenScene):
    def construct(self):
        axes=make_axes()
        thr=DashedLine(P(0,1),P(8.4,1),color=YELLOW,stroke_width=3)
        tl=T("threshold: 1 µM",24,YELLOW).move_to(P(5,1)+UP*.45)
        total=ValueTracker(.2)
        curve=always_redraw(lambda:model_curve(max(.001,total.get_value())))
        marker=always_redraw(lambda:Dot(P(total.get_value(),out_of(total.get_value())),radius=.1,color=TEXT))
        frame=Rectangle(width=5.4,height=1.15,stroke_color=GREY,stroke_width=3).move_to([3.4,.4,0])
        def dense():
            width=5.4*phi_of(total.get_value())
            return Rectangle(width=max(.001,width),height=1.15,stroke_width=0,fill_color=BLUE,
                             fill_opacity=.65 if width>.002 else 0).move_to([.7+width/2,.4,0])
        bar=always_redraw(dense)
        title=T("Nuclear volume",28,TEXT).move_to([3.4,1.55,0])
        outside=T("outside",26,YELLOW).move_to([3.7,.4,0])
        self.at("Phase separation")
        self.play(FadeIn(axes),Create(frame),FadeIn(title),run_time=.8)
        self.at("predicts a threshold")
        self.play(Create(thr),FadeIn(tl),run_time=.6)
        self.add(curve,marker,bar)
        self.at("Below a saturation")
        self.play(total.animate.set_value(.85),run_time=1.2)
        no=T("No bodies",28,GREY).move_to([3.4,-.8,0])
        self.at("no bodies form")
        self.play(FadeIn(no),run_time=.5)
        self.at("Above it")
        self.play(FadeOut(no),total.animate.set_value(1.2),run_time=.5)
        self.at("extra protein")
        self.play(total.animate.set_value(8),run_time=2,rate_func=linear)
        self.at("concentration outside stays")
        self.play(FadeIn(outside),Indicate(thr,color=YELLOW,scale_factor=1),run_time=.9)
        made=T("Made-up data",26,GREY).move_to([3.4,2.65,0])
        two=T("total 2 µM · bodies ≈2%",26,BLUE).move_to([3.4,-.85,0])
        eight=T("total 8 µM · bodies ≈14%",26,BLUE).move_to([3.4,-.85,0])
        self.at("With made")
        self.play(FadeIn(made),total.animate.set_value(2),run_time=.6)
        self.at("bodies fill about")
        self.play(FadeIn(two),run_time=.6)
        self.at("and about")
        self.play(total.animate.set_value(8),ReplacementTransform(two,eight),run_time=1.2)
        fixed=T("outside ≈1 µM",28,YELLOW).move_to([3.4,-1.85,0])
        self.at("while the outside")
        self.play(FadeIn(fixed),run_time=.7)
        self.finish()


def test_plot(cx):
    origin=np.array([cx-1.8,-1.6,0])
    def xy(x,y): return origin+np.array([x*.46,y*.46,0])
    axes=VGroup(Line(xy(0,0),xy(8.4,0),color=GREY),Line(xy(0,0),xy(0,7),color=GREY),
                T("total protein",24,TEXT).move_to([cx,-2.2,0]),
                T("outside concentration",24,TEXT).move_to([cx,2,0]))
    return axes,xy


class S05Test(SpokenScene):
    def construct(self):
        left,p=test_plot(-3.3)
        right,q=test_plot(3.3)
        head=T("Change protein · measure inside and outside",30,TEXT).move_to([0,3.15,0])
        self.at("So the test")
        self.play(FadeIn(head),run_time=.7)
        self.at("Change the amount")
        self.play(FadeIn(left),FadeIn(right),run_time=.7)
        # Two schematic concentration responses; points advance with the total.
        flat=Line(p(1,1),p(8,1),color=TEAL,stroke_width=6)
        rise=Line(q(0,0),q(8,5.8),color=PURPLE,stroke_width=6)
        fl=T("Fits phase separation",28,TEAL).move_to([-3.3,-3.1,0])
        rl=T("Fits binding sites better",28,PURPLE).move_to([3.3,-3.1,0])
        self.at("If the outside")
        self.play(Create(flat),run_time=.9)
        self.at("that fits phase")
        self.play(FadeIn(fl),run_time=.5)
        self.at("If it rises")
        self.play(Create(rise),run_time=1)
        ratio=T("Constant fraction outside",24,PURPLE).move_to([3.3,2.55,0])
        self.at("a constant fraction")
        self.play(FadeIn(ratio),run_time=.6)
        self.at("that fits binding")
        self.play(FadeIn(rl),run_time=.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        names=["round shapes","fusion","fluorescence recovery","hexanediol"]
        chips=VGroup(*[chip(n,TEXT,28).move_to([x,y,0]) for n,(x,y) in zip(names,[(-3.2,1.8),(3.2,1.8),(-3.2,.1),(3.2,.1)])])
        verdict=T("Cannot tell these models apart",36,RED,weight=BOLD).move_to([0,-1.7,0])
        for cue,obj in zip(["Round shapes","fusion","fluorescence recovery","and hexandial"],chips):
            self.at(cue)
            self.play(FadeIn(obj),run_time=.35)
        self.at("cannot tell")
        self.play(FadeIn(verdict),run_time=.6)
        fail=VGroup(chip("Fails the test",ORANGE,30),T("May still phase separate\nas part of a mixture",28,TEXT,line_spacing=1)).arrange(DOWN,buff=.5).move_to([0,.5,0])
        passed=VGroup(chip("Passes the test",GREEN,30),T("Does its job require the body?\nStill unproven",28,TEXT,line_spacing=1)).arrange(DOWN,buff=.5).move_to([0,.5,0])
        self.at("A protein that fails")
        self.play(FadeOut(chips),FadeOut(verdict),FadeIn(fail),run_time=.6)
        self.at("A protein that passes")
        self.play(ReplacementTransform(fail,passed),run_time=.7)
        nuc,terrs,nu,small=map_parts()
        diagram=VGroup(nuc,terrs,nu,small).scale(.78).move_to([-4.1,0,0]).set_opacity(.32)
        lines=VGroup(*[T(s,30,TEXT) for s in ["1  What is there?","2  What does it do?","3  How does it form?","4  Does form matter for its job?"]]).arrange(DOWN,buff=.5,aligned_edge=LEFT).move_to([2.65,0,0])
        self.at("Keep the order")
        self.play(FadeOut(passed),FadeIn(diagram),run_time=.5)
        for cue,line in zip(["What is there","what it does","how it forms","whether its form"],lines):
            self.at(cue)
            self.play(FadeIn(line,shift=UP*.1),run_time=.3)
        self.finish()


class S07End(EndCard):
    LINE = "The nucleus is organized without walls: territories, sorted chromatin, membraneless bodies."
