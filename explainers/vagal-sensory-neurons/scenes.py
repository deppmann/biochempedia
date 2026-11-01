"""Vagal sensory neurons: a label is not a type  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = (periwinkle) the P2ry1-labelled set (airway protection afferents)
  YELLOW = the Npy2r-labelled set
  GREEN  = the Piezo2-positive stretch neurons, and "function" once tied
  RED    = breathing / inspiration halted
  TEAL   = light (optogenetic drive)
  ORANGE = the light-gated channel
  PINK   = an open question, candidate or hypothesis
  GREY   = nerve, structure, unlabelled cells, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BLUE = "#7C9CFF"   # P2ry1 set (distinct from the teal of light)
PURPLE = "#E58BC4"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cell(color=GREY, r=0.36, pos=(0, 0)):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28).move_to([pos[0], pos[1], 0])


def membrane(cx, cy, w=4.0, h=0.3):
    return RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([cx, cy, 0])


def tube(x0, x1, y, h=1.0):
    return RoundedRectangle(corner_radius=0.3, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.15).move_to([(x0 + x1) / 2, y, 0])


def strand(x0, x1, y, color, w=9):
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w)


def breathing(x0, w, yc, t_light, amp0, per0, amp1, per1, t_end=8.5, color=BLUE, sx=None):
    pts = []
    n = 500
    phase = 0.0
    prev_t = 0.0
    for i in range(n + 1):
        t = t_end * i / n
        if t < t_light:
            amp, per = amp0, per0
        else:
            amp, per = amp1, per1
        phase += 2 * np.pi * (t - prev_t) / per
        prev_t = t
        pts.append([x0 + w * t / t_end, yc + amp * np.sin(phase), 0])
    m = VMobject(stroke_color=color, stroke_width=5)
    m.set_points_smoothly([np.array(p) for p in pts[::5]])
    return m


# Additional colours keep new gut populations distinct from the airway sets.
# ORANGE = Oxtr intestinal afferents; GOLD = Glp1r gastric afferents;
# TEXT = GPR65 afferents and chemical-route labels; PURPLE = uncertainty.


def heading(text):
    return T(text, 30).move_to([0, 3.15, 0])


def organ(name, pos, compact=False):
    x, y = pos
    if name == "lung":
        shape = VGroup(*[Ellipse(width=0.7, height=1.15, color=GREY,
                                  fill_opacity=0.12).move_to([x+d, y, 0]) for d in [-0.4, 0.4]])
        shape.add(Line([x,y+0.9,0],[x,y+0.3,0],color=GREY))
    elif name == "artery" and compact:
        shape = VGroup(
            Line([x-0.75,y+0.28,0],[x+0.65,y+0.28,0],color=GREY,stroke_width=4),
            Line([x-0.75,y-0.28,0],[x+0.65,y-0.28,0],color=GREY,stroke_width=4),
            Ellipse(width=0.3,height=0.56,color=GREY,stroke_width=4).move_to([x+0.65,y,0]))
    elif name == "gut" and compact:
        shape = VMobject(stroke_color=GREY,stroke_width=5)
        shape.set_points_smoothly([np.array([x+dx,y+dy,0]) for dx,dy in
            [(-0.7,0.38),(0.55,0.38),(0.7,0.16),(-0.55,0.1),
             (-0.7,-0.15),(0.55,-0.22),(0.7,-0.4)]])
    elif name == "artery":
        shape = tube(x-0.85,x+0.85,y,0.65)
    else:
        shape = VGroup(*[ArcBetweenPoints([x-0.85,y+d,0],[x+0.85,y+d,0],
                             angle=(-1 if i%2 else 1)*PI/2, color=GREY, stroke_width=4)
                         for i,d in enumerate([-0.35,0.1,0.55])])
    if compact and name == "lung":
        shape.scale(0.65,about_point=np.array([x,y,0]))
    return VGroup(shape,T(name,24,GREY).move_to([x,y-(0.8 if compact else 1.05),0]))


def overview(y=0):
    a=chip("organs",GREY,26).move_to([-4.9,y,0])
    b=chip("sensory populations",GREEN,26).move_to([-0.2,y,0])
    c=chip("brainstem",GREY,26).move_to([4.7,y,0])
    return VGroup(a,b,c,arr(a.get_right(),b.get_left(),GREEN),arr(b.get_right(),c.get_left(),GREEN))


class S00Title(TitleCard):
    LESSON = "Vagal sensory neurons"
    TITLE = "One Nerve, Many Sensory Lines"


class S01Question(SpokenScene):
    def construct(self):
        self.at("the vagus carries")
        title=heading("Many specialised sensory lines")
        nerve=tube(-1.4,2.0,0,5.8)
        nerve_label=T("vagus nerve",24,GREY).move_to([0.3,2.6,0])
        target=chip("brainstem",GREY,26).move_to([4.9,0,0])
        self.play(FadeIn(title),FadeIn(nerve),FadeIn(nerve_label),FadeIn(target),run_time=0.6)
        routes=VGroup()
        for name,y,col,cue,desc in [
            ("lung",2.0,BLUE,"some report","inflation / irritants"),
            ("artery",-0.1,GREEN,"others report","arterial stretch"),
            ("gut",-2.2,ORANGE,"gut stretch","stretch / food")]:
            self.at(cue)
            o=organ(name,(-5.2,y+0.3),compact=True)
            label=T(desc,22,col).move_to([0.3,y*0.57+0.5,0])
            path=arr([-4.1,y,0],[3.6,y*0.25,0],col)
            routes.add(VGroup(o,label,path))
            self.play(FadeIn(o),FadeIn(label),GrowArrow(path),run_time=0.65)
            self.play(ShowPassingFlash(path.copy().set_stroke(width=10)),run_time=0.5)
        self.at("these signals help")
        jobs=T("breathing     •     blood pressure     •     feeding",26).move_to([0,-3.3,0])
        self.play(FadeIn(jobs),run_time=0.5)
        self.at("so the question")
        self.play(FadeOut(routes),FadeOut(nerve),FadeOut(nerve_label),FadeOut(target),FadeOut(jobs),run_time=0.4)
        qs=VGroup(*[chip(t,PURPLE,26).move_to([x,0.8,0]) for t,x in
                    [("what is reported?",-4.5),("which force sensor?",0),("where does it land?",4.5)]])
        self.play(FadeIn(qs),run_time=0.6)
        self.at("we follow the mouse evidence")
        route=overview(-1.6)
        self.play(FadeIn(T("mouse evidence",24,GREY).move_to([0,2.2,0])),FadeIn(route),run_time=0.6)
        self.finish()


class S02Gut(SpokenScene):
    def construct(self):
        self.at("start in the gut")
        h=heading("Gut sensory populations • awake mice")
        wall=tube(-5.8,-1.8,0.2,2.4)
        end=VGroup(Line([-5.3,-0.55,0],[-2.3,-0.55,0],color=ORANGE,stroke_width=6),
                   Arc(radius=0.55,start_angle=0,angle=PI,color=ORANGE).move_to([-3.8,-0.2,0]))
        label=T("intestinal stretch endings • Oxtr",24,ORANGE).move_to([-3.8,1.9,0])
        self.play(FadeIn(h),FadeIn(wall),run_time=0.5)
        self.at("activating intestinal stretch")
        self.play(Create(end),FadeIn(label),wall.animate.stretch(1.12,1),run_time=0.8)
        result=chip("feeding: strong suppression",ORANGE,25).move_to([3.1,0.2,0])
        link=arr([-1.5,0.2,0],result.get_left(),ORANGE)
        self.at("strongly suppressed feeding")
        self.play(GrowArrow(link),FadeIn(result),Indicate(end,color=ORANGE),run_time=0.7)
        self.at("activating gastric afferents")
        self.play(Transform(label,T("gastric stretch endings • Glp1r",24,GOLD).move_to(label)),
                  end.animate.set_color(GOLD),FadeOut(result),FadeOut(link),run_time=0.6)
        self.at("suppressed it more")
        result=chip("feeding: weaker suppression",GOLD,25).move_to([3.1,0.2,0])
        link=arr([-1.5,0.2,0],result.get_left(),GOLD)
        self.play(FadeIn(result),GrowArrow(link),run_time=0.6)
        self.at("gpr65 afferents")
        self.play(FadeOut(result),FadeOut(link),FadeOut(end),
                  Transform(label,T("intestinal villous endings • GPR65",24,TEXT).move_to(label)),run_time=0.5)
        villi=VGroup(*[Arc(radius=0.28,start_angle=0,angle=PI,color=TEXT).move_to([x,0.2,0])
                      for x in [-4.8,-3.8,-2.8]])
        self.play(Create(villi),run_time=0.5)
        self.at("responded to intestinal food")
        food=chip("intestinal food",TEXT,24).move_to([-3.8,-1.7,0])
        response=T("sensory response",28,TEXT).move_to([3.1,0.6,0])
        self.play(FadeIn(food),GrowArrow(arr([-3.8,-1.3,0],[-3.8,-0.2,0],TEXT)),
                  FadeIn(response),Indicate(villi,color=TEXT),run_time=0.7)
        self.at("but activating them")
        outcome=VGroup(T("activation → feeding:",28,TEXT),
                       T("no measurable change",28,TEXT,weight=BOLD),
                       T("in tested assays",28,TEXT,weight=BOLD)).arrange(DOWN,buff=0.22).move_to([3.1,-1.2,0])
        self.play(FadeIn(outcome),run_time=0.6)
        self.at("chemical signals also")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not h],run_time=0.5)
        lining=membrane(-4.6,0,2.8)
        secretor=cell(TEXT,0.4,(-4.6,0))
        a=VGroup(T("gut lining",28,TEXT),
                 T("enteroendocrine cell",28,TEXT)).arrange(DOWN,buff=0.24).move_to([-4.6,-1.3,0])
        hormone=chip("gut hormone",TEXT,26).move_to([0,0,0])
        terminal=chip("vagal terminal",GREEN,26).move_to([4.6,0,0])
        self.play(FadeIn(lining),FadeIn(secretor),FadeIn(a),run_time=0.5)
        self.at("hormones released")
        self.play(FadeIn(hormone),GrowArrow(arr([-3,0,0],hormone.get_left(),TEXT)),run_time=0.6)
        self.play(FadeIn(terminal),GrowArrow(arr(hormone.get_right(),terminal.get_left(),TEXT)),run_time=0.6)
        self.at("including cholecystokinin")
        self.play(Transform(hormone,chip("cholecystokinin",TEXT,26).move_to(hormone)),run_time=0.5)
        self.play(ShowPassingFlash(Line([-3,0,0],[3.2,0,0],color=TEXT,stroke_width=8)),run_time=0.8)
        self.finish()


class S03Light(SpokenScene):
    def construct(self):
        self.at("airway populations")
        h=heading("Airway populations • anaesthetized mice")
        self.play(FadeIn(h),run_time=0.5)
        panels=[]
        for cx,col,name in [(-3.4,BLUE,"P2ry1"),(3.4,YELLOW,"Npy2r")]:
            lab=chip(name+" afferents",col,26).move_to([cx,2.1,0])
            baseline=Line([cx-2.7,0.6,0],[cx+2.7,0.6,0],color=GREY,stroke_width=1)
            light=VGroup(Rectangle(width=2.86,height=0.16,stroke_width=0,fill_color=TEAL,fill_opacity=1).move_to([cx+1.27,-0.5,0]),
                         T("light on",22,TEAL).move_to([cx+1.27,-0.95,0]))
            panels.append((lab,baseline,light))
        self.at("light on p2ry1")
        self.play(FadeIn(panels[0][0]),Create(panels[0][1]),FadeIn(panels[0][2]),run_time=0.6)
        self.at("suppressed breathing")
        tr1=breathing(-6.1,5.4,0.6,4,0.55,2,0.03,2,color=BLUE)
        out1=T("breathing suppressed",25,BLUE).move_to([-3.4,-1.7,0])
        self.play(Create(tr1),FadeIn(out1),run_time=0.8)
        self.at("light on npy2r")
        self.play(FadeIn(panels[1][0]),Create(panels[1][1]),FadeIn(panels[1][2]),run_time=0.6)
        self.at("rapid shallow breathing")
        tr2=breathing(0.7,5.4,0.6,4,0.55,2,0.2,0.8,color=YELLOW)
        out2=T("rapid shallow breathing",25,YELLOW).move_to([3.4,-1.7,0])
        sketch=T("schematic breathing traces",22,GREY).move_to([0,-2.6,0])
        self.play(Create(tr2),FadeIn(out2),FadeIn(sketch),run_time=0.8)
        self.at("driving p2ry1")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not h],run_time=0.5)
        driver=chip("P2ry1 activation",BLUE,28).move_to([0,1.8,0])
        self.play(FadeIn(driver),run_time=0.5)
        # Vocal folds are two bars that close; swallowing moves a bolus downward;
        # expiration moves an arrow outward. All are schematic outputs.
        folds=VGroup(Line([-4.9,0.3,0],[-4.9,-0.6,0],color=BLUE,stroke_width=8),
                      Line([-4.1,0.3,0],[-4.1,-0.6,0],color=BLUE,stroke_width=8))
        self.at("closed vocal folds")
        self.play(Create(folds),FadeIn(T("vocal folds close",24,BLUE).move_to([-4.5,-1.4,0])),run_time=0.4)
        self.play(folds[0].animate.shift(RIGHT*0.3),folds[1].animate.shift(LEFT*0.3),run_time=0.5)
        self.at("swallowing")
        bolus=Dot([0,0.3,0],radius=0.16,color=BLUE)
        self.play(FadeIn(bolus),FadeIn(T("swallowing",24,BLUE).move_to([0,-1.4,0])),run_time=0.3)
        self.play(bolus.animate.shift(DOWN*1.1),run_time=0.5)
        self.at("expiratory reflexes")
        self.play(GrowArrow(arr([3.5,-0.2,0],[5.4,-0.2,0],BLUE)),
                  FadeIn(T("expiration",24,BLUE).move_to([4.5,-1.4,0])),run_time=0.6)
        self.at("light shows")
        tag=chip("activation: sufficiency",TEAL,26).move_to([0,-2.5,0])
        self.play(FadeIn(tag),run_time=0.5)
        self.at("it does not identify")
        self.play(Transform(tag,chip("natural stimulus?",PURPLE,26).move_to(tag)),run_time=0.6)
        self.finish()


class S04Stop(SpokenScene):
    def construct(self):
        self.at("lung inflation")
        h=heading("Lung inflation reflex")
        lung=organ("lung",(-4.8,0.5))
        halt=chip("inspiration halts",RED,28).move_to([4.3,0.5,0])
        link=arr([-3.4,0.5,0],halt.get_left(),GREEN)
        self.play(FadeIn(h),FadeIn(lung),run_time=0.5)
        self.at("halt inspiration")
        self.play(lung[0].animate.scale(1.2),GrowArrow(link),FadeIn(halt),run_time=0.7)
        self.at("deleting piezo 2")
        deletion=chip("adult sensory neurons: Piezo2 deletion",GREEN,26).move_to([0,-1.7,0])
        self.play(FadeIn(deletion),run_time=0.5)
        self.at("impaired this inflation reflex")
        self.play(Transform(halt,chip("reflex impaired",RED,28).move_to(halt)),link.animate.set_opacity(0.3),run_time=0.7)
        self.at("arterial pressure sensing")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.5)
        h=heading("Baroreflex • anaesthetized mice")
        source=chip("pressure rises",GREY,26).move_to([-4.4,1.9,0])
        heart=chip("heart slows",GREEN,26).move_to([4.4,1.9,0])
        reflex=arr(source.get_right(),heart.get_left(),GREEN)
        context=T("nodose + petrosal neurons",24,GREY).move_to([0,0.8,0])
        normal=T("intact reflex",22,GREY).move_to([0,2.35,0])
        self.play(FadeIn(h),FadeIn(source),FadeIn(heart),GrowArrow(reflex),FadeIn(context),FadeIn(normal),run_time=0.7)
        self.at("deleting both")
        double=chip("Piezo1 + Piezo2 deletion",GREEN,25).move_to([-3.5,-0.5,0])
        self.play(FadeIn(double),run_time=0.5)
        self.at("abolished the")
        loss=T("baroreflex abolished",26,RED).move_to([3.6,-0.5,0])
        self.play(FadeIn(loss),run_time=0.5)
        self.at("neither single deletion")
        singles=VGroup(T("Piezo1 deletion",25,GREEN).move_to([-3.5,-1.4,0]),
                       T("Piezo2 deletion",25,GREEN).move_to([-3.5,-2.2,0]),
                       T("no detectable change",24,GREY).move_to([3.6,-1.4,0]),
                       T("no detectable change",24,GREY).move_to([3.6,-2.2,0]))
        self.play(FadeIn(singles),run_time=0.7)
        self.at("this shows a collective")
        caveat=T("Population requirement ≠ both channels in every neuron",24,PURPLE).move_to([0,-3.2,0])
        self.play(FadeIn(caveat),run_time=0.6)
        self.finish()


class S05Brainstem(SpokenScene):
    def construct(self):
        self.at("where do these signals")
        h=heading("Sensory routes into the brainstem")
        medulla=RoundedRectangle(width=7.0,height=5.3,corner_radius=0.45,
                                  color=GREY,fill_opacity=0.1).move_to([2.8,-0.25,0])
        self.play(FadeIn(h),FadeIn(medulla),run_time=0.5)
        organs=T("organ sensory\nstrands",24,GREY).move_to([-5.2,1.6,0])
        self.at("vagal sensory axons")
        self.play(FadeIn(organs),run_time=0.5)
        nts=chip("NTS",GREEN,30).move_to([2.5,1.4,0])
        strands=VGroup(*[arr([-3.8,1.3+d,0],[1.4,1.4+d*0.2,0],col)
                        for d,col in [(-0.5,BLUE),(0,GREEN),(0.5,ORANGE)]])
        self.at("nucleus of the solitary tract")
        fullname=T("nucleus of the solitary tract\nprimary target",22,GREEN).move_to([2.5,0.35,0])
        self.play(FadeIn(nts),Create(strands),FadeIn(fullname),run_time=0.7)
        self.at("in the medulla")
        self.play(FadeIn(T("medulla",24,GREY).move_to([4.9,1.9,0])),run_time=0.5)
        self.at("processes the input")
        self.play(ShowPassingFlash(strands.copy().set_stroke(width=9)),Indicate(nts,color=GREEN),run_time=0.8)
        self.at("take a different route")
        j=T("jugular afferents",24,BLUE).move_to([-4.9,-1.0,0])
        pt=chip("paratrigeminal nucleus",BLUE,24).move_to([2.5,-1.1,0])
        self.play(FadeIn(j),GrowArrow(arr([-3.3,-1.1,0],pt.get_left(),BLUE)),FadeIn(pt),run_time=0.7)
        self.at("some gut afferents")
        gut=T("some gut afferents",24,ORANGE).move_to([-4.9,-2.3,0])
        ap=chip("area postrema",ORANGE,25).move_to([2.5,-2.3,0])
        self.play(FadeIn(gut),GrowArrow(arr([-3.2,-2.3,0],ap.get_left(),ORANGE)),FadeIn(ap),run_time=0.7)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        self.at("a smaller closing point")
        h=heading("A smaller point")
        neuron=cell(GREY,0.65,(-2.3,0.8))
        axon=strand(-1.65,1.4,0.8,GREY,5)
        self.play(FadeIn(h),FadeIn(neuron),Create(axon),run_time=0.5)
        self.at("a genetic label")
        label=chip("genetic label: a handle",BLUE,26).move_to([-3.4,2.0,0])
        self.play(FadeIn(label),neuron.animate.set_stroke(BLUE),run_time=0.5)
        self.at("it does not by itself")
        sensor=chip("sensing molecule?",PURPLE,26).move_to([4.0,0.8,0])
        self.play(FadeIn(sensor),run_time=0.5)
        self.at("senses stretch or food")
        route=overview(-2.0)
        self.play(FadeIn(route),run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "In mice, the vagus carries many specialised sensory lines."
