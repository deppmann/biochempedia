"""Nociceptors and the sodium channels of pain: blocking a channel is not silencing a neuron.

COLOR MAP (one color per concept, whole film)
  YELLOW = the gene (SCN9A)
  ORANGE = Nav1.7
  TEAL   = Nav1.8, its current, and its fitted curve
  PURPLE = Nav1.9
  RED    = loss: broken copy, blocker, blocked fraction
  GREEN  = the measured fraction of current that remains (marked points)
  TEXT   = the control spike trace (before the blocker)
  GREY   = membranes, axes, tags, sketch labels
"""
import numpy as np
from scipy.interpolate import PchipInterpolator
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TEAL_C = "#3FB8C0"
KD = 0.38


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 1))


def mem_bar(cx, cy, w, h=0.34):
    return RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([cx, cy, 0])


def chan(text, color, cx, cy, size=30):
    """a labelled channel chip that straddles a membrane bar (opaque backing)."""
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    g = VGroup(back, *c)
    return g.move_to([cx, cy, 0])


def cross(mob, color=RED, w=6):
    r = mob.width / 2 * 0.8
    c = mob.get_center()
    return VGroup(Line(c + np.array([-r, r, 0]) * 0.8, c + np.array([r, -r, 0]) * 0.8, color=color, stroke_width=w),
                  Line(c + np.array([-r, -r, 0]) * 0.8, c + np.array([r, r, 0]) * 0.8, color=color, stroke_width=w))


def tag(lines, color=GREY, size=24, w=3.9):
    t = VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, buff=0.1)
    return fit(t, max_w=w, max_h=3)


# fitted curve and its axes (shared by s03 and s04) -------------------------------------------
def frac(c):
    return 1.0 / (1.0 + c / KD)


def make_axes():
    ax = Axes(x_range=[-1, 2, 1], y_range=[0, 1, 0.5], x_length=6.6, y_length=4.8,
              axis_config={"color": GREY, "stroke_width": 3, "include_ticks": True, "include_tip": False},
              tips=False)
    ax.shift(LEFT * 3.0 + DOWN * 0.5)
    xl = VGroup(*[T(s, 22, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v, s in [(-1, "0.1"), (0, "1"), (1, "10"), (2, "100")]])
    yl = VGroup(*[T(s, 22, GREY).next_to(ax.c2p(-1, v), LEFT, buff=0.15) for v, s in [(0, "0"), (0.5, "0.5"), (1, "1")]])
    xt = T("drug concentration (nM, log scale)", 24, GREY).next_to(ax, DOWN, buff=0.6)
    yt = T("fraction of maximal current", 24, GREY).next_to(ax.c2p(-1, 1), UP, buff=0.3).align_to(ax.c2p(-1, 1), LEFT)
    curve = ax.plot(lambda x: frac(10 ** x), x_range=[-1, 2, 0.01], color=TEAL_C, stroke_width=6, use_smoothing=False)
    return ax, VGroup(xl, yl, xt, yt), curve


def dot_at(ax, c, color):
    return Dot(ax.c2p(np.log10(c), frac(c)), radius=0.11, color=color)


def spike_fn(drug):
    if not drug:
        pts = [(0, 0), (0.45, 0.02), (0.62, 0.30), (0.78, 1.0), (0.95, 0.74), (1.15, 0.46),
               (1.5, 0.40), (1.85, 0.02), (2.1, -0.14), (2.6, 0.0), (3.0, 0.0)]
    else:
        pts = [(0, 0), (0.45, 0.02), (0.62, 0.30), (0.78, 0.68), (0.95, 0.48), (1.15, 0.28),
               (1.5, 0.24), (1.85, 0.0), (2.1, -0.10), (2.6, 0.0), (3.0, 0.0)]
    x, y = zip(*pts)
    return PchipInterpolator(x, y)


def train(drug, n, gap=3.0):
    f = spike_fn(drug)
    xs, ys = [], []
    for k in range(n):
        t = np.linspace(0, gap, 60, endpoint=False)
        xs.extend(t + k * gap)
        ys.extend(np.clip(f(np.minimum(t, 3.0)), -1, 2))
    return np.array(xs), np.array(ys)


# Shared qualitative drawings; no numerical measurements are implied.
def heading(text, color=TEXT):
    return T(text, 32, color, font=TITLE_FONT).move_to([0, 3.05, 0])


def trace(points, color=TEXT, width=5):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [np.array([x, y, 0]) for x, y in points])


def gate(cx, cy, opened=False, color=ORANGE):
    # A pore between two bars; the crossbar swings aside to open.
    sides = VGroup(Line([cx-.5, cy-.55, 0], [cx-.5, cy+.55, 0], color=color, stroke_width=5),
                   Line([cx+.5, cy-.55, 0], [cx+.5, cy+.55, 0], color=color, stroke_width=5))
    bar = Line([cx-.48, cy, 0], [cx+.48, cy, 0], color=color, stroke_width=6)
    if opened:
        bar.rotate(PI/2, about_point=[cx-.48, cy, 0])
    return VGroup(sides, bar)


def pedigree(n):
    label = T(f"Family {n}", 26, GREY).move_to([0, .7, 0])
    people = VGroup(Square(.24, color=GREY).move_to([-.4, .2, 0]),
                    Circle(.12, color=GREY).move_to([.4, .2, 0]),
                    Square(.24, color=GREY).move_to([0, -.55, 0]))
    links = VGroup(Line([-.28,.2,0],[.28,.2,0],color=GREY),
                   Line([0,.2,0],[0,-.43,0],color=GREY))
    return VGroup(label, people, links)


class S00Title(TitleCard):
    LESSON = "Nociceptors and the sodium channels of pain"
    TITLE = "Blocking a Channel Is Not Silence"


class S01Families(SpokenScene):
    def construct(self):
        gene = chip("SCN9A", YELLOW, 40).move_to([0, 2.15, 0])
        loss = chip("pain loss", RED, 32).move_to([-3.6, -.25, 0])
        pain = chip("severe pain syndromes", ORANGE, 30).move_to([3.2, -.25, 0])
        branches = VGroup(arr(gene.get_bottom(), loss.get_top(), YELLOW),
                          arr(gene.get_bottom(), pain.get_top(), YELLOW))
        self.at("Inherited changes")
        self.play(FadeIn(gene), run_time=.6)
        self.at("remove pain")
        self.play(GrowArrow(branches[0]), FadeIn(loss), run_time=.7)
        self.at("cause severe")
        self.play(GrowArrow(branches[1]), FadeIn(pain), run_time=.7)
        evidence = T("human genetic evidence", 30, TEXT).move_to([0, -1.75, 0])
        target = VGroup(Circle(.36, color=RED), Circle(.17, color=RED),
                        T("drug target", 28, RED).move_to([1.7,0,0])).move_to([0,-2.9,0])
        self.at("strong causal evidence")
        self.play(FadeIn(evidence), run_time=.6)
        self.at("target it with")
        self.play(FadeIn(target), run_time=.6)
        fams = VGroup(*[pedigree(i) for i in (1,2,3)]).arrange(RIGHT, buff=1.5).move_to([0, 1.65, 0])
        place = heading("Three families in northern Pakistan")
        self.at("Three families")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.3)
        self.play(FadeIn(fams), FadeIn(place), run_time=.5)
        no_pain = T("members who had never experienced pain", 30, TEXT).move_to([0,-.35,0])
        self.at("never experienced pain")
        self.play(FadeIn(no_pain), run_time=.6)
        c1, c2 = chip("SCN9A copy 1", YELLOW, 28), chip("SCN9A copy 2", YELLOW, 28)
        copies = VGroup(c1,c2).arrange(RIGHT,buff=.9).move_to([-2.2,-2,0])
        broken = VGroup(copies, cross(c1), cross(c2))
        self.at("two broken copies")
        self.play(FadeIn(copies), run_time=.4)
        self.play(Create(broken[1]), Create(broken[2]), run_time=.5)
        nav = chan("Nav1.7", ORANGE, 4,-2,32)
        link = arr(copies.get_right(),nav.get_left(),YELLOW)
        self.at("the gene for")
        self.play(GrowArrow(link),FadeIn(nav),run_time=.7)
        ax = Axes(x_range=[0,4,1],y_range=[-.4,1,1],x_length=8,y_length=2.4,
                  axis_config={"color":GREY,"include_ticks":False,"include_tip":False},tips=False).move_to([0,-.65,0])
        cap=tag(["Mutant human Nav1.7 channels", "expressed in cultured cells"],TEXT,28,11).move_to([0,2.25,0])
        bg=T("background",24,GREY).next_to(ax.c2p(4,0),UP,buff=.25).shift(LEFT*.9)
        flat=Line(ax.c2p(0,0),ax.c2p(4,0),color=RED,stroke_width=5)
        self.at("In cultured cells")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        self.play(FadeIn(ax),FadeIn(cap),FadeIn(bg),run_time=.4)
        self.at("no current above")
        result=T("no current above background",32,RED).move_to([0,-2.8,0])
        self.play(Create(flat),FadeIn(result),run_time=.8)
        self.finish()


class S01Variants(SpokenScene):
    def construct(self):
        gene=chip("SCN9A",YELLOW,36).move_to([0,2.85,0])
        intro=T("Different variants → different pain phenotypes",30,TEXT).move_to([0,-2.9,0])
        self.at("Other variants")
        self.play(FadeIn(gene),run_time=.5)
        left=tag(["Primary erythermalgia"],ORANGE,28,5.8).move_to([-3.4,1.8,0])
        right=tag(["Paroxysmal extreme", "pain disorder"],ORANGE,27,5.8).move_to([3.35,1.8,0])
        self.at("cause pain syndromes")
        self.play(FadeIn(left),FadeIn(right),run_time=.7)
        g1=gate(-3.4,.25)
        l1=tag(["opens at more negative voltages"],ORANGE,24,6).move_to([-3.4,-1,0])
        self.at("Some channels open")
        self.play(FadeIn(g1),run_time=.4)
        self.play(Transform(g1,gate(-3.4,.25,True)),FadeIn(l1),run_time=.7)
        slow=T("slow closing",26,ORANGE).move_to([-3.4,-1.8,0])
        self.at("close more slowly")
        self.play(Transform(g1,gate(-3.4,.25)),FadeIn(slow),run_time=1.2)
        g2=gate(3.35,.25,True)
        l2=tag(["impaired fast inactivation"],ORANGE,24,6).move_to([3.35,-1,0])
        self.at("Others fail to")
        self.play(FadeIn(g2),FadeIn(l2),run_time=.6)
        flow=arr([3.35,1,0],[3.35,-.5,0],ORANGE,4)
        current=T("persistent sodium current",26,ORANGE).move_to([3.35,-1.8,0])
        self.at("leaving persistent")
        self.play(GrowArrow(flow),FadeIn(current),run_time=.7)
        self.at("different channel defects")
        self.play(FadeIn(intro),Indicate(gene,scale_factor=1.08),run_time=.7)
        self.finish()


class S02Channels(SpokenScene):
    def construct(self):
        title=heading("Nociceptor membrane • schematic")
        mem=mem_bar(0,1.3,12,.42)
        cs=VGroup(chan("Nav1.7",ORANGE,-4,1.3,34),chan("Nav1.8",TEAL_C,0,1.3,34),chan("Nav1.9",PURPLE,4,1.3,34))
        self.at("No -suscepter")
        self.play(FadeIn(title),FadeIn(mem),FadeIn(cs),run_time=.9)
        spike=trace([(-5,-1.7),(-4,-1.7),(-3.7,-1.4),(-3.45,.1),(-3.1,-1.9),(-2.7,-1.7),(-1,-1.7)])
        sl=T("contribute to the spike",26,TEXT).move_to([-3,-2.5,0])
        self.at("The first two")
        self.play(Create(spike),FadeIn(sl),Indicate(VGroup(cs[0],cs[1]),scale_factor=1.08),run_time=.8)
        rest=trace([(1,-1.6),(2,-1.6),(2.8,-1.4),(3.5,-1.5),(4.3,-1.25),(5.6,-1.4)],PURPLE)
        rl=tag(["mainly resting potential", "and subthreshold excitability"],PURPLE,25,5.8).move_to([3.4,-2.65,0])
        self.at("mainly sets resting")
        self.play(Create(rest),FadeIn(rl),run_time=.8)
        rule=heading("More channel function ≠ more firing")
        self.at("More channel function")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        self.play(FadeIn(rule),run_time=.4)
        who=tag(["Human Nav1.9 variants expressed", "in rat sensory neurons • schematic"],PURPLE,28,12).move_to([0,1.9,0])
        dep=trace([(-5.6,-.3),(-4.3,-.3),(-3.7,.5),(-2.5,.5),(-1.3,.5)],PURPLE)
        dep_label=tag(["sustained", "depolarization"],PURPLE,26,4).move_to([-3.5,-1.2,0])
        avail=tag(["other sodium channels", "less available"],GREY,27,5).move_to([3,.35,0])
        arrow=arr([-1,.35,0],[.5,.35,0],PURPLE)
        impaired=T("spike generation impaired",30,RED).move_to([0,-2.65,0])
        self.at("Some human")
        self.play(FadeIn(who),run_time=.6)
        self.at("variants depolarized")
        self.play(Create(dep),FadeIn(dep_label),GrowArrow(arrow),FadeIn(avail),run_time=1)
        self.at("to impair spike")
        self.play(FadeIn(impaired),run_time=.6)
        self.finish()


class S02Drug(SpokenScene):
    def construct(self):
        hd=heading("Clinical trials: different pain conditions")
        self.at("The drug story")
        self.play(FadeIn(hd),run_time=.6)
        pf=chip("PF-05089771 • Nav1.7 blocker",ORANGE,30).move_to([0,1.65,0])
        cond=T("painful diabetic neuropathy",30,TEXT).move_to([0,.5,0])
        result=tag(["No significant improvement", "versus placebo"],TEXT,32,11).move_to([0,-1.2,0])
        self.at("A selective")
        self.play(FadeIn(pf),FadeIn(cond),run_time=.7)
        self.at("did not significantly")
        self.play(FadeIn(result),run_time=.7)
        drug=chip("suzetrigine",RED,34).move_to([-2.8,1.65,0])
        nav=chan("Nav1.8",TEAL_C,2.8,1.65,34)
        block=inhib(drug.get_right(),nav.get_left())
        surgery=T("postoperative pain • both phase 3 trials",30,TEXT).move_to([0,.35,0])
        relief=T("Pain relief versus placebo",38,TEAL_C).move_to([0,-.85,0])
        self.at("Susatrogen blocks")
        self.play(FadeOut(pf),FadeOut(cond),FadeOut(result),run_time=.3)
        self.play(FadeIn(drug),FadeIn(nav),Create(block),run_time=.5)
        self.at("It reduced pain")
        self.play(FadeIn(surgery),FadeIn(relief),run_time=.8)
        separate=tag(["Different pain conditions", "No direct comparison of targets"],GREY,28,12).move_to([0,-2.6,0])
        self.at("These were different")
        self.play(FadeIn(separate),run_time=.7)
        opioid=tag(["Neither trial demonstrated superiority", "over hydrocodone / acetaminophen"],TEXT,28,12).move_to([0,-2.6,0])
        self.at("Neither surgery trial")
        self.play(ReplacementTransform(separate,opioid),run_time=.8)
        approval=chip("US approval • January 2025",TEAL_C,32).move_to([0,.55,0])
        indication=tag(["Moderate-to-severe acute pain", "in adults"],TEXT,32,12).move_to([0,-1,0])
        self.at("Approval in the")
        self.play(FadeOut(hd),FadeOut(drug),FadeOut(nav),FadeOut(block),FadeOut(surgery),FadeOut(opioid),
                  relief.animate.move_to([0,2.3,0]),FadeIn(approval),run_time=.8)
        self.at("for moderate to")
        self.play(FadeIn(indication),run_time=.7)
        self.finish()


class S04Identity(SpokenScene):
    def construct(self):
        hd=heading("Neurons have several kinds of identity")
        self.at("The neurons themselves")
        self.play(FadeIn(hd),run_time=.6)
        center=np.array([0,-.1,0])
        axes=VGroup(Line([-3,-.1,0],[3,-.1,0],color=GREY),
                    Line([-1.7,-1.9,0],[1.7,1.7,0],color=GREY),
                    Line([-1.7,1.7,0],[1.7,-1.9,0],color=GREY))
        labels=VGroup(T("molecular label",28,YELLOW).move_to([-4.45,-.1,0]),
                      T("conduction class",28,TEXT).move_to([2.9,2,0]),
                      T("functional state",28,TEAL_C).move_to([2.9,-2.2,0]))
        self.at("A molecular label")
        self.play(Create(axes[0]),FadeIn(labels[0]),run_time=.5)
        self.at("a conduction class")
        self.play(Create(axes[1]),FadeIn(labels[1]),run_time=.5)
        self.at("a functional state")
        self.play(Create(axes[2]),FadeIn(labels[2]),run_time=.5)
        rule=T("A label does not fix stimulus function",30,TEXT).move_to([0,-3.05,0])
        self.at("A label does")
        self.play(FadeIn(rule),run_time=.6)
        dot=Dot(center,radius=.12,color=TEAL_C)
        self.at("can change state")
        self.play(FadeIn(dot),run_time=.2)
        self.play(dot.animate.move_to([1.25,-1.43,0]),Indicate(labels[2],scale_factor=1.06),run_time=.8)
        who=tag(["Cultured mouse CHRNA3-positive sensory neurons", "Separate soma-indentation conditions • schematic", "NGF = nerve growth factor"],TEXT,26,12.6).move_to([0,2.75,0])
        panels=[]
        for x,name in zip([-4.2,0,4.2],["Before NGF","After NGF","NGF + PIEZO2 KD"]):
            title=T(name,26,TEXT).move_to([x,1.5,0])
            soma=Circle(.48,color=GREY,fill_color=GREY,fill_opacity=.12).move_to([x,.35,0])
            probe=Line([x,1.12,0],[x,.91,0],color=TEXT,stroke_width=5)
            base=Line([x-1.5,-1.4,0],[x+1.5,-1.4,0],color=GREY,stroke_width=2)
            panels.append(VGroup(title,soma,probe,base))
        baseline=trace([(-5.7,-1.4),(-4.5,-1.4),(-4.2,-1.46),(-3.9,-1.4),(-2.7,-1.4)],GREY)
        induced=trace([(-1.5,-1.4),(-.4,-1.4),(-.3,-2.5),(.1,-1.7),(.6,-1.4),(1.5,-1.4)],TEXT)
        prevented=trace([(2.7,-1.4),(3.9,-1.4),(4.2,-1.46),(4.5,-1.4),(5.7,-1.4)],GREY)
        captions=[T("nearly no current",24,GREY).move_to([-4.2,-2.85,0]),
                  T("induced current",24,TEXT).move_to([0,-2.85,0]),
                  tag(["induction prevented", "KD = knockdown"],GREY,24,4).move_to([4.2,-2.85,0])]
        self.at("In cultured mouse")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.25)
        self.play(FadeIn(who),FadeIn(panels[0]),run_time=.35)
        self.play(panels[0][2].animate.shift(DOWN*.18),Create(baseline),FadeIn(captions[0]),run_time=.5)
        self.at("nerve growth factor")
        self.play(FadeIn(panels[1]),run_time=.4)
        self.at("brought out mechanical")
        self.play(panels[1][2].animate.shift(DOWN*.18),Create(induced),FadeIn(captions[1]),run_time=.7)
        self.at("that required")
        self.play(FadeIn(panels[2]),run_time=.4)
        self.play(panels[2][2].animate.shift(DOWN*.18),Create(prevented),FadeIn(captions[2]),run_time=.7)
        self.finish()


class S05Neuron(SpokenScene):
    def construct(self):
        hd=heading("Smaller point: one human-neuron recording study")
        self.at("One smaller point")
        self.play(FadeIn(hd),run_time=.6)
        who=T("Dissociated adult human sensory neurons • schematic",26,TEXT).move_to([0,2.25,0])
        def tr_axes(cy):
            return Axes(x_range=[0,15,1],y_range=[-.3,1.1,1],x_length=7,y_length=1.6,
                        axis_config={"color":GREY,"stroke_width":2,"include_ticks":False,"include_tip":False},tips=False).move_to([-2.1,cy,0])
        a1,a2=tr_axes(.8),tr_axes(-1.6)
        x1,y1=train(False,5)
        # Identical individual spike shapes: this scene only claims a firing-frequency effect.
        x2,y2=train(False,3,gap=5)
        c=a1.plot_line_graph(x1,y1,line_color=TEXT,add_vertex_dots=False,stroke_width=4)["line_graph"]
        d=a2.plot_line_graph(x2,y2,line_color=RED,add_vertex_dots=False,stroke_width=4)["line_graph"]
        before=T("before",28,TEXT).move_to([4,.8,0])
        after=tag(["suzetrigine", "reduced firing", "still present"],RED,27,4).move_to([4,-1.6,0])
        self.at("In dissociated adult")
        self.play(FadeIn(who),FadeIn(a1),FadeIn(before),Create(c),run_time=.9)
        self.at("generally reduced")
        self.play(FadeIn(a2),FadeIn(after),Create(d),run_time=1.2)
        rule=T("Channel block ≠ neuronal silence",32,TEXT).move_to([0,-3.15,0])
        self.at("Blocking a channel")
        self.play(FadeIn(rule),run_time=.6)
        cards=VGroup(*[chip(t,col,27) for t,col in [("Inherited variants",YELLOW),("Neuronal recordings",TEXT),("Clinical pain relief",TEAL_C)]]).arrange(DOWN,buff=.6).move_to([0,-.1,0])
        end=heading("Three distinct kinds of evidence")
        self.at("The clinical trials")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.3)
        self.play(FadeIn(end),LaggedStart(*[FadeIn(m,shift=UP*.15) for m in cards],lag_ratio=.2),run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "A channel calculation is not neuronal silence."
