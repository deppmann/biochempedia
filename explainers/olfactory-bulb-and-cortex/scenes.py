"""Same address, different message: sister mitral/tufted cells (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = sister cell 1 (and its spikes, bars)
  YELLOW = sister cell 2 (and its spikes, bars)
  TEAL   = shared input: glomeruli, receptor neurons, links and cortical activity
  GREEN  = rate (mean spike count), learned meaning and reward
  ORANGE = timing against the breath; aversive outcome
  PURPLE = granule cell and its inhibition (bar-ended arrows)
  GOLD   = tracer and experimental light
  GREY   = labels, axes, breath curve, electrodes, de-emphasized
  RED    = only the strike-through "no"
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
C1, C2 = BLUE, YELLOW

LAYOUT = {
    "big": dict(glom=(-4.2, 0.3), gr=0.95, rec=[(-5.4, -2.2), (-4.2, -2.3), (-3.0, -2.2)],
                recend=[(-4.8, -0.55), (-4.2, -0.65), (-3.6, -0.55)], rect=(-4.2, -2.8),
                s1=(0.2, 1.8), s2=(0.2, -1.0), sr=0.42, d1e=(-3.4, 0.95), d2e=(-3.4, -0.3),
                axend=3.2, n1=(0.2, 2.55), n2=(0.2, -1.7), ctx=(5.0, 0.4)),
    "side": dict(glom=(-5.0, 0.1), gr=0.95, rec=[(-5.9, -1.95), (-5.0, -2.05), (-4.1, -1.95)],
                 recend=[(-5.45, -0.75), (-5.0, -0.85), (-4.55, -0.75)], rect=(-5.0, -2.5),
                 s1=(-2.6, 1.3), s2=(-2.6, -1.1), sr=0.38, d1e=(-4.2, 0.75), d2e=(-4.2, -0.55),
                 axend=-1.3, n1=(-2.6, 1.95), n2=(-2.6, -1.75), ctx=(5.0, 0.4)),
}


def bez(a, b, bend):
    a, b = np.array(list(a)[:2] + [0.]), np.array(list(b)[:2] + [0.])
    m = (a + b) / 2
    c1 = a + (m - a) * 0.6 + np.array([0, bend, 0])
    c2 = b + (m - b) * 0.6 + np.array([0, bend * 0.3, 0])
    return CubicBezier(a, c1, c2, b, stroke_width=5)


def build(kind="big", names=True):
    L = LAYOUT[kind]
    p = {}
    p["glom"] = Circle(radius=L["gr"], stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.2).move_to([*L["glom"], 0])
    p["glom_t"] = T("glomerulus", 22, TEAL).move_to(p["glom"])
    p["rec"] = VGroup(*[Line([*a, 0], [*b, 0], color=TEAL, stroke_width=4) for a, b in zip(L["rec"], L["recend"])])
    p["rec_t"] = T("receptor neurons", 22, TEAL).move_to([*L["rect"], 0])
    for i, (col, key, ekey) in enumerate([(C1, "s1", "d1e"), (C2, "s2", "d2e")], start=1):
        c = np.array([*L[key], 0])
        p[f"s{i}"] = Circle(radius=L["sr"], stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.25).move_to(c)
        d = bez(c + LEFT * L["sr"], L[ekey], 0.35 if i == 1 else -0.35).set_color(col)
        p[f"d{i}"] = d
        p[f"a{i}"] = Arrow(c + RIGHT * L["sr"], [L["axend"], L[key][1], 0], buff=0.0, color=col, stroke_width=5,
                           tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        p[f"n{i}"] = T(f"sister {i}", 22, col).move_to([*L["n1" if i == 1 else "n2"], 0])
    p["ctx"] = chip("piriform cortex", GREY, size=22, pad=0.18).move_to([*L["ctx"], 0])
    return p


def parts(p, keys):
    return VGroup(*[p[k] for k in keys])


STRUCT = ["rec", "glom", "glom_t", "rec_t", "s1", "s2", "d1", "d2", "a1", "a2"]


def morph_to_side(scene, big, run_time):
    side = build("side")
    anims = []
    for k in STRUCT + ["n1", "n2"]:
        anims.append(Transform(big[k], side[k]))
    return anims


def ticks(x0, x1, y, phases, color, h=0.5):
    return VGroup(*[Line([x0 + (x1 - x0) * ph, y - h / 2, 0], [x0 + (x1 - x0) * ph, y + h / 2, 0], color=color, stroke_width=5)
                    for ph in phases])


def cluster(c, n=4, step=0.045):
    return [c + (i - (n - 1) / 2) * step for i in range(n)]


def tag(text="adult anaesthetized mice"):
    return T(text, 22, GREY).move_to([-2.2, -3.3, 0])


def strike(mob, color=RED):
    return Line(mob.get_corner(DL) + np.array([0.04, 0.04, 0]), mob.get_corner(UR) + np.array([-0.04, -0.04, 0]), color=color, stroke_width=6)


def timing_panel():
    x0, x1 = 1.5, 6.0
    ph = np.linspace(0, 1, 80)
    pts = [[x0 + (x1 - x0) * t, 1.0 + 0.4 * np.sin(2 * np.pi * t - np.pi / 2), 0] for t in ph]
    breath = VMobject(color=GREY, stroke_width=4).set_points_smoothly([np.array(q) for q in pts])
    y1, y2 = -0.1, -1.25
    r1 = Line([x0, y1 - 0.35, 0], [x1, y1 - 0.35, 0], color=C1, stroke_width=2, stroke_opacity=0.5)
    r2 = Line([x0, y2 - 0.35, 0], [x1, y2 - 0.35, 0], color=C2, stroke_width=2, stroke_opacity=0.5)
    l1 = T("sister 1", 22, C1).move_to([0.3, y1, 0])
    l2 = T("sister 2", 22, C2).move_to([0.3, y2, 0])
    ax = Arrow([x0, -1.95, 0], [x1, -1.95, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.18)
    axl = T("one respiration cycle", 22, GREY).move_to([(x0 + x1) / 2, -2.3, 0])
    return dict(x0=x0, x1=x1, y1=y1, y2=y2, breath=breath, r1=r1, r2=r2, l1=l1, l2=l2, ax=ax, axl=axl)


def spike_rows(P, ph1, ph2):
    return (ticks(P["x0"], P["x1"], P["y1"], cluster(ph1), C1), ticks(P["x0"], P["x1"], P["y2"], cluster(ph2), C2))



# Population panels are schematic, with no measured values implied.
POSITIONS = [(-1.8, .75), (-.7, 1.0), (.5, .65), (1.7, 1.0),
             (-1.5, -.65), (-.25, -.3), (.8, -.9), (1.8, -.3)]
ACTIVE = (0, 3, 5, 6)


def sheet(x=3.5, y=.2, title="piriform cortex"):
    border = RoundedRectangle(width=5.1, height=3.5, corner_radius=.22,
                              color=GREY, stroke_width=3).move_to([x,y,0])
    cells = VGroup(*[Dot([x+a,y+b,0], radius=.12, color=GREY).set_opacity(.4)
                     for a,b in POSITIONS])
    label = T(title, 26, GREY).move_to([x,y+2.2,0])
    return VGroup(border, cells, label)


def activity(cells, indices=ACTIVE):
    return [d.animate.set_color(TEAL if i in indices else GREY).set_opacity(1 if i in indices else .4)
            for i,d in enumerate(cells)]


def bulb_row():
    circles = VGroup(*[Circle(radius=.3, color=TEAL, stroke_width=3,
                       fill_color=TEAL, fill_opacity=.08).move_to([-5.65+i*.82,.4,0])
                       for i in range(5)])
    label = T("bulb glomeruli",26,TEAL).move_to([-4,2.4,0])
    return VGroup(circles,label)


def bridge():
    return Arrow([-1.8,.4,0],[.7,.4,0], color=TEAL, buff=.1, stroke_width=5)


class S00Title(TitleCard):
    LESSON = "From Glomeruli to Piriform Cortex"
    TITLE = "A Map In, a Pattern Out"


class S01Lead(SpokenScene):
    def construct(self):
        b=bulb_row()
        self.at("Every smell starts")
        self.play(FadeIn(b),run_time=.7)
        receptors=VGroup(*[Line([-5.0+i*.5,-1.5,0],[-4.83,.05,0],color=TEAL,stroke_width=4)
                            for i in range(3)])
        rl=T("one receptor type",22,TEAL).move_to([-4.5,-2.1,0])
        self.at("receptor neurons")
        self.play(Create(receptors),FadeIn(rl),run_time=.9)
        self.at("converge on")
        self.play(Indicate(b[0][1],color=TEAL,scale_factor=1.25),run_time=.8)
        self.at("a fixed pattern")
        self.play(*[b[0][i].animate.set_fill(TEAL,.8) for i in (0,1,3)],run_time=.7)
        c=sheet()
        a=bridge()
        self.at("does not keep")
        self.play(FadeIn(c),GrowArrow(a),run_time=.8)
        self.at("switches on")
        self.play(*activity(c[1]),run_time=.8)
        od=chip("odour A",TEAL,22).move_to([3.5,-2.25,0])
        self.at("Yet the scattered pattern")
        self.play(FadeIn(od),run_time=.5)
        self.at("chemically alike")
        self.play(Transform(od,chip("related odour B",TEAL,22).move_to(od)),
                  *activity(c[1],(0,2,3,5)),run_time=.8)
        learned=chip("learned",GREEN,24).move_to([3.5,-3.15,0])
        self.at("can learn")
        self.play(FadeIn(learned),run_time=.6)
        self.at("change from bulb")
        self.play(Indicate(a,color=TEAL,scale_factor=1.08),run_time=.7)
        self.finish()


class S02Dispersed(SpokenScene):
    def construct(self):
        c=sheet(0,.0)
        self.at("Stetler and Axel")
        self.play(FadeIn(c),run_time=.7)
        self.at("One odor")
        self.play(*activity(c[1]),run_time=.9)
        self.at("then traced the output")
        self.play(FadeOut(c),run_time=.5)
        gl=Circle(radius=.55,color=TEAL,fill_color=TEAL,fill_opacity=.2).move_to([-5.3,0,0])
        gt=T("one glomerulus",22,TEAL).move_to([-5.2,-1.1,0])
        self.play(FadeIn(gl),FadeIn(gt),run_time=.6)
        self.at("a single glomerulus")
        self.play(gl.animate.set_fill(GOLD,.7),run_time=.6)
        top=sheet(2.5,1.55)
        bottom=sheet(2.5,-2.0,"cortical amygdala")
        # Shorter panels leave room for labels between them.
        for s in (top,bottom):
            s[0].stretch_to_fit_height(2.15)
            s[1].stretch(.65,1)
            s[2].move_to(s[0].get_top()+UP*.4)
        self.at("the axons spread diffusely")
        fan=VGroup(*[bez((-4.75,0),d.get_center()[:2],.35).set_color(GOLD).set_stroke(width=2)
                      for d in top[1]])
        self.play(FadeIn(top),Create(fan),run_time=.9)
        self.at("the cortical amygdala")
        self.play(FadeIn(bottom[0]),FadeIn(bottom[2]),run_time=.6)
        patches=VGroup(*[Ellipse(width=.9,height=.55,color=GOLD,fill_color=GOLD,fill_opacity=.55)
                         .move_to([x,-2,0]) for x in (1,4)])
        patch_ax=VGroup(*[bez((-4.75,0),(x,-2),-.5).set_color(GOLD).set_stroke(width=2) for x in (1,4)])
        self.at("made tidy patches")
        self.play(Create(patch_ax),FadeIn(patches),run_time=.8)
        self.at("scattering belongs")
        self.play(Indicate(top[0],color=TEAL,scale_factor=1.03),run_time=.8)
        self.finish()


def similarity_grid(x, cortical=False, lit=False):
    cells=VGroup()
    for r in range(4):
        for c in range(4):
            same=r//2==c//2
            opacity=(.85 if r==c else (.75 if cortical else .4) if same else .08) if lit else .04
            cells.add(Square(side_length=.72,color=GREY,stroke_width=1,
                      fill_color=TEAL,fill_opacity=opacity).move_to([x+(c-1.5)*.75,.5+(1.5-r)*.75,0]))
    letters=VGroup(*[T(l,22,GREY).move_to([x+(i-1.5)*.75,2.45,0]) for i,l in enumerate("ABCD")],
                   *[T(l,22,GREY).move_to([x-1.95,.5+(1.5-i)*.75,0]) for i,l in enumerate("ABCD")])
    return VGroup(cells,letters)


class S03Geometry(SpokenScene):
    def construct(self):
        q=T("Chemistry lost in the scatter?",34).move_to([0,3.1,0])
        self.at("Is chemistry lost")
        self.play(FadeIn(q),run_time=.6)
        left=similarity_grid(-3.4)
        right=similarity_grid(3.4)
        labels=VGroup(T("bulb boutons",26,TEAL).move_to([-3.4,-1.65,0]),
                      T("piriform neurons",26,TEAL).move_to([3.4,-1.65,0]))
        note=T("Odour pairs A–B and C–D are related • schematic",22,GREY).move_to([0,-2.35,0])
        self.at("compared bulb inputs")
        self.play(FadeOut(q),FadeIn(left),FadeIn(right),FadeIn(labels),FadeIn(note),run_time=.8)
        self.at("related population patterns")
        self.play(Transform(left,similarity_grid(-3.4,lit=True)),
                  Transform(right,similarity_grid(3.4,lit=True)),run_time=.8)
        self.at("more tightly")
        self.play(Transform(right,similarity_grid(3.4,cortical=True,lit=True)),run_time=.8)
        similar=chip("similarity",TEAL,26).move_to([-1.7,-3.15,0])
        place=chip("place",GREY,26).move_to([1.7,-3.15,0])
        self.at("map of similarity")
        self.play(FadeIn(similar),run_time=.6)
        self.at("not of place")
        self.play(FadeIn(place),Create(strike(place)),run_time=.6)
        self.at("wherever the cells sit")
        self.play(Indicate(similar,color=TEAL,scale_factor=1.06),run_time=.7)
        self.finish()


class S04Meaning(SpokenScene):
    def construct(self):
        c=sheet(-3.5,.4)
        links=VGroup(*[bez(c[1][i].get_center()[:2],c[1][j].get_center()[:2],.3)
                        .set_color(TEAL).set_stroke(width=2) for i,j in [(0,5),(5,3),(3,6),(6,0)]])
        self.at("Puriform neurons")
        self.play(FadeIn(c),Create(links),run_time=.8)
        store=T("experience?",26,GREY).move_to([-3.5,-2.1,0])
        self.at("thought to store experience")
        self.play(FadeIn(store),run_time=.6)
        light=T("light",24,GOLD).move_to([-3.5,3.2,0])
        beam=Polygon([-4.1,2.8,0],[-5.6,-.7,0],[-1.4,-.7,0],[-2.9,2.8,0],
                     stroke_width=0,fill_color=GOLD,fill_opacity=.12)
        self.at("with light")
        self.play(FadeOut(store),FadeIn(light),FadeIn(beam),*activity(c[1]),run_time=.7)
        # Alternative training cases: the whole result is replaced together.
        drop=VMobject(color=GREEN,fill_color=GREEN,fill_opacity=.5)
        drop.start_new_path(np.array([0,.4,0]))
        drop.add_cubic_bezier_curve_to(np.array([-.12,.15,0]),np.array([-.45,-.15,0]),np.array([0,-.3,0]))
        drop.add_cubic_bezier_curve_to(np.array([.45,-.15,0]),np.array([.12,.15,0]),np.array([0,.4,0]))
        drop.close_path()
        drop.move_to([2.0,1.1,0])
        reward=VGroup(drop,T("reward",26,GREEN).move_to([3.4,1.1,0]))
        toward=Arrow([5.6,-.1,0],[1.8,-.1,0],buff=0,color=GREEN)
        approach=VGroup(toward,T("approach",26,GREEN).move_to([3.6,-.75,0]))
        self.at("Paired with a reward")
        self.play(FadeIn(reward),run_time=.6)
        self.at("learned one")
        self.play(FadeIn(approach),run_time=.6)
        shock=VGroup(VMobject(color=ORANGE,stroke_width=5).set_points_as_corners(
                     [[1.95,1.6,0],[1.65,1.1,0],[2.05,1.1,0],[1.8,.6,0]]),
                     T("shock",26,ORANGE).move_to([3.4,1.1,0]))
        away=VGroup(Arrow([1.8,-.1,0],[5.6,-.1,0],buff=0,color=ORANGE),
                    T("avoid",26,ORANGE).move_to([3.6,-.75,0]))
        self.at("Paired with a shock")
        self.play(FadeOut(reward),FadeOut(approach),FadeIn(shock),run_time=.6)
        self.at("learned the opposite")
        self.play(FadeIn(away),run_time=.6)
        meaning=chip("learned meaning",GREEN,26).move_to([3.5,-2,0])
        self.at("gain learned meaning")
        self.play(FadeOut(shock),FadeOut(away),FadeIn(meaning),run_time=.7)
        # Simple profile of a nose; the question mark withholds a percept claim.
        nose=VMobject(color=GREY,stroke_width=4).set_points_as_corners(
             [[1.5,-2.65,0],[1.7,-3.05,0],[2.1,-3.2,0],[1.7,-3.35,0]])
        unsure=T("smell?",26,GREY).move_to([3.6,-3,0])
        self.at("not the same")
        self.play(FadeIn(nose),FadeIn(unsure),run_time=.6)
        self.finish()


def inhibition(a,b):
    a,b=np.array(a),np.array(b)
    d=(b-a)/np.linalg.norm(b-a)
    perp=np.array([-d[1],d[0],0])*.18
    return VGroup(Line(a,b,color=PURPLE,stroke_width=4),Line(b-perp,b+perp,color=PURPLE,stroke_width=5))


class S05Bulb(SpokenScene):
    def construct(self):
        title=T("The bulb shapes cortical input",32).move_to([0,3.1,0])
        self.at("The bulb shapes")
        self.play(FadeIn(title),run_time=.6)
        g=VGroup(Circle(radius=.4,color=PURPLE,fill_color=PURPLE,fill_opacity=.25).move_to([0,0,0]),
                 T("granule / interneuron",22,PURPLE).move_to([0,-.9,0]))
        self.at("Granule cells")
        self.play(FadeIn(g),run_time=.6)
        p=build("side")
        # Reuse the original sister-cell circles and dendrite curves, mirrored at right.
        cell1=VGroup(p["s1"].copy().move_to([-4,1,0]),T("mitral / tufted",22,C1).move_to([-4,1.9,0]))
        cell2=VGroup(p["s2"].copy().move_to([4,1,0]),T("neighbour",22,C2).move_to([4,1.9,0]))
        dendrites=VGroup(bez((-3.6,1),(-.5,.3),.2).set_color(C1),
                         bez((3.6,1),(.5,.3),.2).set_color(C2))
        self.at("mitral and tufted cells")
        self.play(FadeIn(cell1),FadeIn(cell2),Create(dendrites),run_time=.8)
        ex=Arrow([-2.8,.7,0],[-.5,.25,0],color=C1,buff=0,stroke_width=4)
        back=inhibition([-.5,-.15,0],[-2.8,.3,0])
        glut=T("glutamate →",22,C1).move_to([-2.1,1.35,0])
        gaba=T("GABA",22,PURPLE).move_to([-2.1,-.6,0])
        reciprocal=VGroup(ex,back,glut,gaba)
        self.at("reciprocal synapses")
        self.play(Create(ex),FadeIn(glut),run_time=.5)
        self.play(Create(back),FadeIn(gaba),run_time=.5)
        lateral=inhibition([.5,-.15,0],[2.8,.3,0])
        il=T("bar ends: inhibition",22,PURPLE).move_to([3,-.6,0])
        self.at("recurrent and lateral inhibition")
        self.play(Create(lateral),FadeIn(il),run_time=.7)
        circuit=VGroup(title,g,cell1,cell2,dendrites,reciprocal,lateral,il)
        caveat=chip("Timing does not identify the synapse",GREY,26).move_to([0,2.8,0])
        self.at("Timing matters too")
        self.play(FadeOut(circuit),FadeIn(caveat),run_time=.7)
        self.at("do not show which synapses")
        self.play(Indicate(caveat,color=GREY,scale_factor=1.02),run_time=.6)
        p=build("side")
        left=parts(p,["glom","glom_t","s1","s2","d1","d2","n1","n2"])
        P=timing_panel()
        graph=VGroup(*[P[k] for k in ("breath","r1","r2","l1","l2","ax","axl")])
        tg=tag("anaesthetized mice").move_to([-3.8,-3.1,0])
        self.at("Sister cells that share")
        self.play(FadeOut(caveat),FadeIn(left),FadeIn(tg),FadeIn(graph),run_time=.7)
        rate=chip("mean rates: correlated",GREEN,24).move_to([3.4,2.8,0])
        sketch=T("schematic spikes",22,GREY).move_to([3.4,2.05,0])
        self.at("correlated average rates")
        self.play(FadeIn(rate),FadeIn(sketch),run_time=.6)
        t1,t2=spike_rows(P,.23,.69)
        self.at("fired at different moments")
        self.play(Create(t1),Create(t2),run_time=.8)
        self.at("A shared address")
        msg=T("Shared input • different timing",26,ORANGE).move_to([2.8,-3.15,0])
        self.play(FadeIn(msg),run_time=.7)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        b=bulb_row()
        for i in (0,1,3):
            b[0][i].set_fill(TEAL,.8)
        c=sheet()
        for i in ACTIVE:
            c[1][i].set_color(TEAL).set_opacity(1)
        a=bridge()
        self.at("So the bulb")
        self.play(FadeIn(b),run_time=.6)
        self.at("cortex turns it")
        self.play(GrowArrow(a),FadeIn(c),run_time=.7)
        meaning=chip("likeness + learned meaning",GREEN,24).move_to([3.5,-2.35,0])
        self.at("keeps chemical likeness")
        self.play(FadeIn(meaning),run_time=.7)
        self.at("drifts over weeks")
        # Cells stay in place; response membership changes across weeks.
        self.play(*activity(c[1],(1,3,5,7)),run_time=.7)
        self.play(*activity(c[1],(0,2,5,7)),run_time=.7)
        readout=chip("stable readout?",GREY,28).move_to([0,-3.2,0])
        self.at("What stays stable")
        self.play(FadeIn(readout),run_time=.7)
        self.at("an open question")
        self.play(Indicate(readout,color=GREY,scale_factor=1.04),run_time=.7)
        self.finish()


class S07End(EndCard):
    LINE = "A map in, a scattered pattern out that still tracks chemical likeness."
