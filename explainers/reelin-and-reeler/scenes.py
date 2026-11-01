"""Reelin and the reeler mouse: one missing protein, a cortex built wrong  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  ORANGE = the first-born neurons (the first thin sheet)
  BLUE   = the next-born neurons
  GREEN  = the last-born neurons
  YELLOW = Reelin and the Cajal-Retzius cells that make it
  TEAL   = the two receptors (ApoER2, VLDLR)
  PURPLE = Dab1, the adaptor
  PINK   = the Src-family kinases (Fyn and Src)
  GOLD   = a phosphate group (the little "P" badge)
  RED    = the reeler problem: a block, a stop, a missing runner
  GREY   = tissue, membranes, outlines, labels
  WHITE  = the baton in the relay picture
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E8789F"

SL_W, SL_H = 4.4, 5.7
TOP, BOT = 2.85, -2.85
DR = 0.17
LA = [-1.8, -1.08, -0.36, 0.36, 1.08, 1.8]      # lanes for waves one and three
LB = [-1.44, -0.72, 0.0, 0.72, 1.44]             # lanes for wave two
LSUB = [-1.44, 0.0, 1.44]

# resting rows in the normal cortex
Y_CR, Y_LATE, Y_EARLY, Y_SUB = 2.58, 1.45, 0.35, -0.8
Y_START = -2.55


def neuron(x, y, color):
    return Circle(radius=DR, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.65).move_to([x, y, 0])


def wave(cx, lanes, y, color):
    return VGroup(*[neuron(cx + l, y, color) for l in lanes])


def slab(cx, with_vz=True):
    body = Rectangle(width=SL_W, height=SL_H, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.07).move_to([cx, 0, 0])
    g = VGroup(body)
    if with_vz:
        vz = Rectangle(width=SL_W, height=0.55, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to([cx, BOT + 0.275, 0])
        g.add(vz)
    return g


def lab(text, color=GREY, size=26):
    return T(text, size, color)


def left_of(mob, x, y):
    return mob.move_to([x, y, 0]).align_to([x, 0, 0], LEFT)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w))


def pbadge(size=0.2):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def normal_final(cx, tint_cr=True):
    """the finished normal cortex, rebuilt in the same place."""
    cr = VGroup(*[neuron(cx + LA[i], Y_CR, YELLOW if tint_cr else ORANGE) for i in (0, 2, 4)])
    late = wave(cx, LA, Y_LATE, GREEN)
    early = wave(cx, LB, Y_EARLY, BLUE)
    sub = wave(cx, LSUB, Y_SUB, ORANGE)
    return cr, late, early, sub


class S00Title(TitleCard):
    LESSON = "Reelin and the reeler mouse"
    TITLE = "One Missing Protein, A Cortex Built Wrong"


# Each wave is one grouped visual object; cell dots retain the old drawing style.
def disordered(cx, y, color, lanes=LA):
    rng = np.random.RandomState(int((y + 4) * 100))
    return VGroup(*[neuron(cx + x + rng.uniform(-.12, .12), y + rng.uniform(-.42, .42), color) for x in lanes])


def dim(c, o=0.35):
    return [c[0].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[1].animate.set_opacity(o)]


def undim(c):
    return [c[0].animate.set_stroke(opacity=1).set_fill(opacity=0.16), c[1].animate.set_opacity(1)]


class S01Reeler(SpokenScene):
    def construct(self):
        reelin = chip("Reelin", YELLOW, 34).move_to([0, 2.9, 0])
        self.at("Rhelan")
        self.play(FadeIn(reelin), run_time=.5)
        purpose = lab("neuronal positioning", TEXT, 32).move_to([0, 1.7, 0])
        self.at("proper places")
        self.play(FadeIn(purpose), run_time=.5)
        # A large mouse silhouette with ears, snout, paws and a curling tail.
        body = Ellipse(width=1.1, height=.55, color=TEXT, fill_opacity=.65)
        head = Circle(radius=.23, color=TEXT, fill_opacity=.65).shift(RIGHT*.58+UP*.15)
        ears = VGroup(*[Circle(radius=.14, color=TEXT, fill_color=BG, fill_opacity=1).shift(RIGHT*x+UP*.38) for x in (.43,.65)])
        snout = Ellipse(width=.28, height=.16, color=TEXT, fill_opacity=.65).shift(RIGHT*.78+UP*.08)
        eye = Dot([.67,.2,0], radius=.035, color=BG)
        nose = Dot([.91,.08,0], radius=.035, color=PINK)
        paws = VGroup(*[Ellipse(width=.22,height=.09,color=TEXT,fill_opacity=.8).shift(RIGHT*x+DOWN*.28) for x in (-.3,.33)])
        tail = CubicBezier([-.52,-.02,0],[-1.35,-.45,0],[-1.5,.65,0],[-.95,.55,0],color=PINK,stroke_width=4)
        mouse = VGroup(tail,body,paws,head,ears,snout,eye,nose).scale(2.5).move_to([-3.5, .2, 0])
        mouse_pose = mouse.copy()
        def reel(mob, alpha):
            mob.become(mouse_pose.copy().rotate(.2*np.sin(6*PI*alpha)))
            mob.shift(RIGHT*(.9*alpha)+UP*(.35*np.sin(6*PI*alpha)))
        missing = lab("reeler: Reelin missing", RED, 28).move_to([-3.1, -2, 0])
        self.at("A mouse without")
        self.play(FadeOut(purpose), FadeIn(mouse), FadeIn(missing), run_time=.5)
        self.at("reels as it walks")
        self.play(UpdateFromAlphaFunc(mouse,reel), run_time=1.5)
        outline = VMobject(stroke_color=TEXT,stroke_width=4,fill_color=GREY,fill_opacity=.15)
        outline.set_points_smoothly([[-1.4,0,0],[-1.25,.65,0],[-.7,1,0],[0,1.1,0],[.8,.9,0],[1.35,.4,0],[1.3,-.35,0],[.7,-.8,0],[0,-1,0],[-.8,-.8,0],[-1.4,0,0]])
        folds = VGroup(*[ArcBetweenPoints([x,-.65,0],[x,.7,0],angle=-.6,color=GREY,stroke_width=3) for x in (-.85,-.4,.05,.5,.95)])
        cerebellum = VGroup(outline,folds).move_to([3.2,.2,0])
        cb = chip("small cerebellum", GREY, 28).move_to([3.2, -1.9, 0])
        self.at("Its cerebellum")
        self.play(FadeIn(cerebellum), run_time=.3)
        self.play(cerebellum.animate.scale(.6), FadeIn(cb), run_time=.6)
        self.at("its cortical layers")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.3)
        sn,sr=slab(-3.8),slab(3.8)
        n=VGroup(*normal_final(-3.8,False))
        r=VGroup(disordered(3.8,2.1,ORANGE),disordered(3.8,1.1,BLUE,LB),disordered(3.8,-.1,GREEN))
        labels=VGroup(lab("normal",TEXT,28).move_to([-3.8,3.25,0]),lab("reeler: no Reelin",RED,28).move_to([3.8,3.25,0]))
        self.play(FadeIn(VGroup(sn,sr)),FadeIn(n),FadeIn(r),FadeIn(labels),run_time=.8)
        self.at("The problem is placement")
        msg=lab("placement",RED,30).move_to([0,1.8,0]);self.play(FadeIn(msg),run_time=.4)
        # Identical schedules under the two cortices, with identical birth-order colors.
        schedules=VGroup()
        for cx in (-3.8,3.8):
            row=VGroup(*[neuron(0,0,c) for c in (ORANGE,BLUE,GREEN)]).arrange(RIGHT,buff=.55).move_to([cx,-3.25,0])
            schedules.add(row)
        self.at("made on schedule")
        self.play(FadeIn(schedules),run_time=.5)
        self.at("settle in the wrong order")
        self.play(Indicate(r,scale_factor=1.05),run_time=.7)
        self.finish()


class S02Waves(SpokenScene):
    def construct(self):
        cx=-3.9; sl=slab(cx)
        vz=left_of(lab("ventricular zone",GREY,26),-1.2,-2.58)
        surf=left_of(lab("surface",GREY,26),-1.2,2.7)
        pre=wave(cx,LA,Y_START,ORANGE)
        self.at("Normally")
        self.play(FadeIn(sl),FadeIn(vz),FadeIn(surf),FadeIn(pre),run_time=.5)
        self.at("neurons climb")
        self.play(pre.animate.set_y(2.1),run_time=2)
        status=left_of(lab("preplate: first thin sheet",ORANGE,28),-1.2,2.1)
        self.at("first ones form")
        self.play(FadeIn(status),run_time=.5)
        blue=wave(cx,LB,Y_START,BLUE)
        self.at("The next wave")
        self.play(FadeIn(blue),run_time=.2)
        self.play(blue.animate.set_y(2.1),run_time=.9)
        up=VGroup(*[pre[i] for i in (0,2,4)])
        down=[pre[i] for i in (1,3,5)]
        self.at("splits it")
        self.play(*[m.animate.set_y(Y_CR) for m in up],
                  *[m.animate.move_to([cx+x,Y_SUB,0]) for m,x in zip(down,LSUB)],
                  blue.animate.set_y(Y_EARLY),FadeOut(status),run_time=.9)
        green=wave(cx,LA,Y_START,GREEN)
        self.at("Each new wave")
        self.play(FadeIn(green),run_time=.2)
        self.play(green.animate.set_y(Y_LATE),run_time=1.5)
        deep=left_of(lab("early-born: deep",BLUE,28),-1.2,Y_EARLY)
        late=left_of(lab("late-born: near surface",GREEN,28),-1.2,Y_LATE)
        self.at("end up deep")
        self.play(FadeIn(deep),Indicate(blue),run_time=.6)
        self.at("end up near")
        self.play(FadeIn(late),Indicate(green),run_time=.6)
        self.finish()


class S03Inverted(SpokenScene):
    def construct(self):
        cxn,cxr=-3.9,3.9
        normal=VGroup(slab(cxn),*normal_final(cxn,False))
        sr=slab(cxr)
        labels=VGroup(lab("normal",TEXT,28).move_to([cxn,3.25,0]),lab("reeler",RED,28).move_to([cxr,3.25,0]))
        sched=VGroup()
        for cx in (cxn,cxr):
            sched.add(VGroup(*[neuron(0,0,c) for c in (ORANGE,BLUE,GREEN)]).arrange(RIGHT,buff=.55).move_to([cx,-3.25,0]))
        self.at("Birth dating")
        self.play(FadeIn(normal),FadeIn(sr),FadeIn(labels),run_time=.5)
        self.at("same schedule")
        self.play(FadeIn(sched),run_time=.5)
        pre=disordered(cxr,2.2,ORANGE)
        status=lab("unsplit",RED,26).move_to([0,2.2,0])
        self.at("fails to split")
        self.play(FadeIn(pre),FadeIn(status),run_time=.5)
        r2=wave(cxr,LB,Y_START,BLUE);r3=wave(cxr,LA,Y_START,GREEN)
        self.at("Later waves")
        self.play(FadeIn(r2),run_time=.2)
        self.play(Transform(r2,disordered(cxr,1.1,BLUE,LB)),run_time=.9)
        self.at("stop beneath")
        self.play(FadeIn(r3),run_time=.2)
        self.play(Transform(r3,disordered(cxr,-.1,GREEN)),run_time=1.1)
        self.at("tend to sit")
        self.play(Indicate(r2,scale_factor=1.08),run_time=.5)
        self.at("neurons deep")
        self.play(Indicate(r3,scale_factor=1.08),run_time=.5)
        self.at("needed for normal layering")
        self.play(Indicate(normal,scale_factor=1.03),run_time=.7)
        self.finish()


class S04Pathway(SpokenScene):
    def construct(self):
        mem=RoundedRectangle(corner_radius=.1,width=11,height=.34,stroke_color=GREY,fill_color=GREY,fill_opacity=.35).move_to([0,.7,0])
        sides=VGroup(lab("outside",GREY,24).move_to([-4.7,1.25,0]),lab("inside neuron",GREY,24).move_to([-4.5,.15,0]))
        reelin=chip("Reelin",YELLOW,30).move_to([0,2.8,0])
        recs=VGroup(*[RoundedRectangle(corner_radius=.2,width=.6,height=1.4,stroke_color=TEAL,stroke_width=4,fill_color=TEAL,fill_opacity=.3).move_to([x,.7,0]) for x in (-1.9,1.9)])
        rlabels=VGroup(*[lab(n,TEAL,28).move_to([x,1.85,0]) for x,n in ((-3.0,"ApoER2"),(3.0,"VLDLR"))])
        self.at("How does the signal")
        self.play(FadeIn(mem),FadeIn(sides),run_time=.5)
        self.at("binds two")
        self.play(FadeIn(reelin),FadeIn(recs),FadeIn(rlabels),run_time=.6)
        binding=VGroup(*[Line([x*.25,2.45,0],[x,1.4,0],color=YELLOW,stroke_width=4) for x in (-1.9,1.9)])
        self.at("lipoprotein receptors")
        self.play(Create(binding),run_time=.6)
        dab=chip("Dab1",PURPLE,30).move_to([0,-1,0]);kin=chip("Fyn and Src",PINK,28).move_to([-3,-1,0])
        self.at("Inside the kinase's")
        self.play(FadeIn(dab),FadeIn(kin),run_time=.5)
        pb=pbadge().move_to(dab.get_corner(UR)+[.08,.08,0])
        self.at("add phosphate")
        destination=pb.get_center().copy()
        pb.move_to(kin.get_right()+RIGHT*.25)
        self.play(FadeIn(pb),run_time=.2)
        self.play(pb.animate.move_to(destination),Indicate(kin),run_time=.6)
        eff=chip("effectors",TEXT,28).move_to([3,-1,0]);ea=arr(dab.get_right(),eff.get_left(),PURPLE)
        self.at("recruits effectors")
        self.play(GrowArrow(ea),FadeIn(eff),run_time=.6)
        cull=chip("Cullin 5",GREY,28).move_to([-3,-2.65,0]);ub=chip("ubiquitin",GREY,24).move_to([0,-2.65,0])
        self.at("then helps mark")
        self.play(FadeOut(kin),FadeIn(cull),FadeIn(ub),run_time=.5)
        self.at("for destruction")
        self.play(ub.animate.shift(UP*.7),run_time=.4)
        self.play(FadeOut(dab,scale=.2),FadeOut(pb,scale=.2),FadeOut(ub,scale=.2),FadeOut(ea),run_time=.6)
        self.at("limiting the signal")
        self.play(eff.animate.set_opacity(.25),run_time=.5)
        self.finish()


class S05Relay(SpokenScene):
    def construct(self):
        names=[("Reelin",YELLOW),("two receptors",TEAL),("Dab1",PURPLE)]
        chips=[chip(n,c,30).move_to([x,1.1,0]) for (n,c),x in zip(names,(-4,0,4))]
        arrows=VGroup(*[arr(chips[i].get_right(),chips[i+1].get_left()) for i in (0,1)])
        baton=Dot([-4,2.1,0],radius=.16,color=TEXT)
        self.at("Remove a runner")
        self.play(*[FadeIn(c) for c in chips],FadeIn(arrows),FadeIn(baton),run_time=.5)
        missing=cross(chips[1].get_top()+UP*1.15,size=.22);result=lab("baton never arrives",RED,30).move_to([0,-1,0])
        self.at("the baton never arrives")
        self.play(baton.animate.move_to([0,2.1,0]),Create(missing),FadeIn(result),run_time=.6)
        x0=cross(chips[0].get_top()+UP*1.15,size=.22);x2=cross(chips[2].get_top()+UP*1.15,size=.22)
        self.at("Mice without")
        self.play(FadeOut(missing),FadeOut(result),Create(x0),*dim(chips[0]),run_time=.4)
        self.at("without DAB1")
        self.play(FadeOut(x0),*undim(chips[0]),Create(x2),*dim(chips[2]),run_time=.4)
        self.at("without both receptors")
        self.play(FadeOut(x2),*undim(chips[2]),Create(missing),*dim(chips[1]),run_time=.4)
        result=lab("matching layering defects",RED,30).move_to([0,-1,0])
        self.at("matching defects")
        self.play(FadeIn(result),run_time=.4)
        self.at("suggests one pathway")
        self.play(FadeOut(missing),*undim(chips[1]),Indicate(arrows),run_time=.5)
        self.at("Biochemistry gives the order")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        # Qualitative comparisons, deliberately no invented numerical scale.
        baseline=-1.8
        def bar(x,h):
            return Rectangle(width=.9,height=h,stroke_color=PURPLE,fill_color=PURPLE,fill_opacity=.55).move_to([x,baseline+h/2,0])
        bars=[bar(x,1.5) for x in (-4.9,-2.5,1.85,4.25)]
        labels=VGroup(lab("total Dab1",PURPLE,30).move_to([-3.7,2.4,0]),lab("phosphorylated Dab1",PURPLE,30).move_to([3.05,2.4,0]),lab("qualitative comparison",GREY,30).move_to([0,3.25,0]))
        for x,t in zip((-4.9,-2.5,1.85,4.25),("normal","no Reelin","normal","no Reelin")):
            labels.add(lab(t,GREY if t=="normal" else RED,30).move_to([x,-2.3,0]))
        self.play(FadeIn(labels),FadeIn(bars[0]),FadeIn(bars[2]),run_time=.6)
        self.at("have more")
        bars[1]=bar(-2.5,2.8)
        self.play(GrowFromEdge(bars[1],DOWN),run_time=.6)
        self.at("less phosphorylated")
        bars[3]=bar(4.25,.55)
        self.play(GrowFromEdge(bars[3],DOWN),run_time=.6)
        self.finish()


class S05Source(SpokenScene):
    def construct(self):
        cx=-3.9;cr,late,early,sub=normal_final(cx,False)
        ctx=VGroup(slab(cx),cr,early,sub)
        self.at("Where does")
        self.play(FadeIn(ctx),run_time=.5)
        band=Rectangle(width=SL_W,height=.55,stroke_color=YELLOW,fill_color=YELLOW,fill_opacity=.12).move_to([cx,Y_CR,0])
        source=left_of(lab("Cajal-Retzius cells",YELLOW,28),-1.2,3.05)
        mz=left_of(lab("marginal zone",YELLOW,28),-1.2,2.35)
        cp=left_of(lab("cortical plate",GREY,26),-1.2,.8)
        self.at("In the developing cortex")
        self.play(FadeIn(band),FadeIn(cp),run_time=.5)
        self.at("cells secrete")
        self.play(cr.animate.set_color(YELLOW),FadeIn(source),run_time=.4)
        particles=VGroup(*[Dot([cx+x,Y_CR,0],radius=.08,color=YELLOW) for x in (-1.8,-.36,1.08)])
        tag=chip("Reelin",YELLOW,28).move_to([2.3,1.45,0])
        self.play(FadeIn(particles),FadeIn(tag),run_time=.3)
        self.play(particles.animate.shift(DOWN*.38+RIGHT*.25),run_time=.6)
        self.at("the marginal zone")
        self.play(FadeIn(mz),run_time=.4)
        self.at("each new wave")
        late.set_y(Y_START)
        self.play(FadeIn(late),run_time=.2)
        self.play(late.animate.set_y(Y_LATE),run_time=1.2)
        self.finish()


class S06Open(SpokenScene):
    def construct(self):
        header=lab("stage-dependent actions: one view",TEXT,32).move_to([0,3.2,0])
        pathway=VGroup(chip("Reelin",YELLOW,26),chip("Dab1",PURPLE,26),chip("Rap1",TEXT,26)).arrange(RIGHT,buff=.5).move_to([0,2.2,0])
        soma=Circle(radius=.34,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.65).move_to([-2,-1,0])
        processes=VGroup(*[Line(soma.get_center(),soma.get_center()+np.array([.9*np.cos(a),.9*np.sin(a),0]),color=BLUE,stroke_width=4) for a in (0,1.5,3,4.5)])
        plate=Rectangle(width=5,height=.4,stroke_color=GREY,fill_color=GREY,fill_opacity=.2).move_to([0,.8,0])
        plabel=lab("cortical plate",GREY,26).move_to([3.9,.8,0])
        orient=lab("orientation",BLUE,30).move_to([0,-2.8,0])
        self.at("On one view")
        self.play(FadeIn(header),FadeIn(soma),Create(processes),FadeIn(plate),FadeIn(plabel),run_time=.5)
        self.at("Signaling through")
        self.play(FadeIn(pathway),run_time=.6)
        self.at("linked to orienting")
        self.play(FadeIn(orient),run_time=.5)
        leading=Line([-2,-.66,0],[-1.3,.6,0],color=BLUE,stroke_width=5)
        self.play(ReplacementTransform(processes,leading),soma.animate.shift(RIGHT*.3+UP*.3),run_time=.8)
        adhesion=chip("N-cadherin adhesion",TEXT,28).move_to([2.6,-1.4,0])
        contact=Line([-1.3,.6,0],[-.9,.6,0],color=TEXT,stroke_width=8)
        self.at("adhesion through")
        self.play(FadeIn(adhesion),Create(contact),run_time=.6)
        self.at("In the final step")
        self.play(FadeOut(VGroup(soma,leading,plate,plabel,orient,adhesion,contact)),run_time=.4)
        mz=Rectangle(width=8,height=.65,stroke_color=YELLOW,fill_color=YELLOW,fill_opacity=.12).move_to([0,.9,0])
        mzlabel=lab("marginal zone",YELLOW,26).move_to([0,1.45,0])
        body=Circle(radius=.36,color=BLUE,fill_opacity=.65).move_to([0,-1.7,0])
        process=Line([0,-1.34,0],[0,.9,0],color=BLUE,stroke_width=5)
        label=lab("somal translocation",BLUE,30).move_to([0,-3,0])
        self.at("somal translocation")
        self.play(FadeIn(mz),FadeIn(mzlabel),FadeIn(body),Create(process),FadeIn(label),run_time=.6)
        anchor=Circle(radius=.14,color=BLUE,fill_opacity=1).move_to([0,.9,0])
        self.at("anchors its leading process")
        self.play(FadeIn(anchor,scale=.5),run_time=.6)
        self.at("pulls its cell body up")
        self.play(body.animate.set_y(.05),Transform(process,Line([0,.41,0],[0,.9,0],color=BLUE,stroke_width=5)),run_time=1.2)
        support=lab("without glial support",GREY,26).move_to([3.4,-1.4,0])
        self.at("without glial support")
        self.play(FadeIn(support),run_time=.5)
        self.at("The effect depends")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.4)
        final=VGroup(slab(-3.9),*normal_final(-3.9))
        stages=VGroup(lab("orientation",BLUE,30),lab("adhesion",TEXT,30),lab("final movement",BLUE,30)).arrange(DOWN,buff=.65).move_to([2.1,.5,0])
        self.at("Orientation")
        self.play(FadeIn(final),FadeIn(stages[0]),run_time=.5)
        self.at("adhesion and")
        self.play(FadeIn(stages[1]),run_time=.4)
        self.at("that final movement")
        self.play(FadeIn(stages[2]),run_time=.5)
        self.at("take their places")
        self.play(Indicate(final,scale_factor=1.03),run_time=.6)
        self.finish()


class S07End(EndCard):
    LINE = "Reeler mice make neurons on time, but they settle out of order."
