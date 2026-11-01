"""Vestibular system: two channels and conditional central cancellation  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = regular afferents; peripheral afferent input in the cancellation sketch
  PURPLE = irregular afferents / calyx ending
  YELLOW = the central vestibular-only neuron and its response
  GREEN  = self-generated (active) turn: the motor command, the expected feedback, cancellation
  ORANGE = passive turn (pushed from outside)
  TEAL   = neck proprioceptive feedback (the actual feedback)
  RED    = mismatch / cancellation failing
  GREY   = outlines, axes, de-emphasised
Traces and response heights are qualitative schematics, not measured data.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TEALN = "#3FB8C0"  # neck feedback (same value as TEAL, kept as its own concept)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def lines2(a, b, color, size=24):
    """a two-line label chip."""
    label = VGroup(T(a, size, color), T(b, size, color)).arrange(DOWN, buff=0.08)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 0.44, height=label.height + 0.4,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=box.width, height=box.height, stroke_width=0,
                            fill_color=BG, fill_opacity=1)
    g = VGroup(back, box, label)
    label.move_to(box)
    return g


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def head_icon(color, scale=1.0):
    """a head seen from above: circle with a nose triangle pointing up (forward)."""
    face = Circle(radius=0.62, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.18)
    nose = Triangle(stroke_width=0, fill_color=color, fill_opacity=0.9).scale(0.17)
    nose.move_to(face.get_top() + UP * 0.1)
    g = VGroup(face, nose)
    return g.scale(scale)


def turn_arrow(center, color, flip=False, r=0.98):
    arc = Arc(radius=r, start_angle=PI * 0.15, angle=PI * 0.7, color=color, stroke_width=5)
    arc.add_tip(tip_length=0.2)
    arc.move_arc_center_to(center)
    if flip:
        arc.flip(UP, about_point=center)
    return arc


def ticks(x0, x1, y, n, color, seed, h=0.32):
    """irregular spike ticks along a baseline."""
    rng = np.random.RandomState(seed)
    xs = np.sort(rng.uniform(x0 + 0.1, x1 - 0.1, n))
    base = Line([x0, y - h / 2, 0], [x1, y - h / 2, 0], color=GREY, stroke_width=2)
    tk = VGroup(*[Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=color, stroke_width=4) for x in xs])
    return base, tk


def bell(t, peak, mid=0.5, wid=0.17):
    return peak * np.exp(-(((t - mid) / wid) ** 2))


def make_axes(w, h, ymax, ytick_vals, xlabel, color=GREY):
    ax = Axes(x_range=[0, 1, 0.5], y_range=[0, ymax, ymax], x_length=w, y_length=h,
              axis_config={"color": color, "stroke_width": 3, "include_ticks": False, "include_tip": False},
              tips=False)
    labels = VGroup()
    for v in ytick_vals:
        p = ax.c2p(0, v)
        tk = Line(p + LEFT * 0.08, p + RIGHT * 0.08, color=color, stroke_width=3)
        lb = M(f"{v:g}", 22, GREY).next_to(tk, LEFT, buff=0.1)
        labels.add(tk, lb)
    xl = T(xlabel, 22, GREY).next_to(ax, DOWN, buff=0.15)
    return ax, labels, xl


def spike_train(x0, x1, y, positions, color, h=0.45):
    base = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3)
    marks = VGroup(*[Line([x0 + (x1-x0)*t, y, 0],
                             [x0 + (x1-x0)*t, y+h, 0], color=color, stroke_width=4)
                     for t in positions])
    return VGroup(base, marks)


def hair_cell(kind=1):
    """Anatomical schematic; grey hair cell, coloured afferent ending."""
    if kind == 2:
        body = RoundedRectangle(width=1.15, height=2.0, corner_radius=0.35,
                                stroke_color=GREY, fill_color=GREY, fill_opacity=0.16)
        ending = VGroup(*[Circle(radius=0.17, color=BLUE, fill_opacity=0.5)
                           .move_to([x, y, 0]) for x, y in [(-0.65,-0.45),(0.65,-0.45),(0,-1.08)]])
        ending.add(*[Line([x,y,0], [x, -1.65,0], color=BLUE, stroke_width=4)
                     for x,y in [(-0.65,-0.45),(0.65,-0.45),(0,-1.08)]])
    else:
        body = VMobject(stroke_color=GREY, fill_color=GREY, fill_opacity=0.16)
        body.set_points_smoothly([[-0.25,1,0],[-0.28,0.45,0],[-0.65,-0.15,0],
                                  [-0.55,-0.8,0],[0,-1,0],[0.55,-0.8,0],
                                  [0.65,-0.15,0],[0.28,0.45,0],[0.25,1,0]])
        body.close_path()
        cup = VMobject(stroke_color=PURPLE, stroke_width=9)
        cup.set_points_smoothly([[-0.75,0.65,0],[-0.9,-0.25,0],[-0.7,-1.1,0],
                                 [0,-1.3,0],[0.7,-1.1,0],[0.9,-0.25,0],[0.75,0.65,0]])
        ending = VGroup(cup, Line([0,-1.3,0],[0,-1.85,0],color=PURPLE,stroke_width=5))
    hairs = VGroup(*[Line([x,1,0],[x,1.45-abs(x)*0.8,0],color=GREY,stroke_width=3)
                     for x in [-0.22,-0.11,0,0.11,0.22]])
    return VGroup(body, hairs, ending)


def vesicles(x, y):
    ribbon = RoundedRectangle(width=0.13, height=0.38, corner_radius=0.04,
                              color=GREY, fill_opacity=0.6).move_to([x,y,0])
    packets = VGroup(*[Circle(radius=0.065, color=TEXT, fill_opacity=0.7)
                      .move_to([x+dx,y+dy,0]) for dx,dy in [(-0.19,-0.15),(-0.19,0.08),(0.19,-0.15),(0.19,0.08)]])
    return VGroup(ribbon, packets)


def eye_neck():
    eye = VGroup(Ellipse(width=1.15,height=0.55,color=TEXT),Circle(radius=0.18,color=TEXT))
    neck = VGroup(head_icon(TEXT,0.55).move_to([0,-1.0,0]),
                  Line([-0.2,-1.35,0],[-0.2,-1.8,0],color=TEXT),
                  Line([0.2,-1.35,0],[0.2,-1.8,0],color=TEXT))
    return VGroup(eye, neck)


class S00Title(TitleCard):
    LESSON = "Balance: vestibular hair cells and self-motion"
    TITLE = "Two Channels for One Head Turn"


class S01TwoChannels(SpokenScene):
    def construct(self):
        head = head_icon(TEXT,1.3).move_to([-4.8,2.15,0])
        turn = turn_arrow(head.get_center(),TEXT,r=1.08)
        ax = Axes(x_range=[0,1,1],y_range=[0,1.2,1],x_length=6.5,y_length=1.25,
                  tips=False,axis_config={"include_ticks":False,"stroke_color":GREY})
        ax.move_to([0.7,2.1,0])
        vel = ax.plot(lambda t: 0.5*(np.tanh((t-0.2)*25)-np.tanh((t-0.8)*25)),
                      x_range=[0,1,0.01],color=TEXT,stroke_width=4)
        vl = T("head velocity · schematic",24,GREY).move_to([0.7,3.25,0])
        self.at("Every head movement")
        self.play(FadeIn(head),Create(turn),Create(ax),FadeIn(vl),run_time=0.7)
        self.play(Rotate(head,-PI/3),Create(vel),run_time=1.2)
        split = VGroup(arr([-2.7,1.55,0],[-3.1,0.2,0],BLUE),
                       arr([-2.7,1.55,0],[-3.1,-1.45,0],PURPLE))
        self.at("two kinds")
        self.play(*[GrowArrow(a) for a in split],run_time=0.7)
        reg = spike_train(-2.6,2.8,0.1,np.linspace(0.02,0.98,14),BLUE)
        rl = lines2("regular","rate",BLUE).move_to([-4.9,-0.1,0])
        self.at("Regular afferents")
        self.play(FadeIn(rl),Create(reg),run_time=1.0)
        # A smooth density change follows the sustained velocity plateau.
        dense = np.array([0.02,0.15,0.24,0.30,0.36,0.42,0.48,0.54,0.60,0.66,0.72,0.80,0.90,0.98])
        self.at("sustained motion")
        self.play(Transform(reg,spike_train(-2.6,2.8,0.1,dense,BLUE)),run_time=1.0)
        irr = spike_train(-2.6,2.8,-1.55,[0.03,0.12,0.24,0.28,0.49,0.68,0.73,0.92],PURPLE)
        il = lines2("irregular","timing",PURPLE).move_to([-4.9,-1.8,0])
        self.at("Irregular afferents")
        self.play(FadeIn(il),Create(irr),run_time=0.8)
        self.at("rapid changes")
        self.play(Transform(irr,spike_train(-2.6,2.8,-1.55,
                   [0.03,0.19,0.20,0.215,0.24,0.47,0.73,0.78,0.79,0.815,0.83,0.98],PURPLE)),run_time=1.0)
        self.at("Two channels")
        self.play(Indicate(reg,color=BLUE),Indicate(irr,color=PURPLE),run_time=0.8)
        outputs = eye_neck().move_to([5.15,-0.5,0])
        links = VGroup(arr([3.0,0.2,0],[3.85,-0.45,0],BLUE),
                       arr([3.0,-1.4,0],[3.85,-0.45,0],PURPLE),
                       arr([3.85,-0.45,0],[4.5,0.15,0],GREY),
                       arr([3.85,-0.45,0],[4.5,-1.2,0],GREY))
        ol = T("gaze + posture",24,TEXT).move_to([4.95,-2.35,0])
        self.at("Together they feed")
        self.play(FadeIn(outputs),FadeIn(ol),*[GrowArrow(a) for a in links],run_time=0.9)
        self.finish()


class S02Map(SpokenScene):
    def construct(self):
        title = T("Where do the channels start?",36,font=TITLE_FONT).move_to([0,3.15,0])
        outer = Ellipse(width=7,height=3.8,color=GREY,fill_opacity=0.12)
        centre = Ellipse(width=3,height=2.6,color=PURPLE,fill_opacity=0.15)
        zones = VGroup(outer,centre,T("outer zone",24,BLUE).move_to([-2.35,0.7,0]),
                       T("central zone",24,PURPLE).move_to([0,0.45,0]))
        self.at("Where does each")
        self.play(FadeIn(title),FadeIn(zones),run_time=0.7)
        f1 = VMobject(color=BLUE,stroke_width=6).set_points_as_corners([[-5,-2,0],[-3.5,-1.7,0],[-2,-0.3,0]])
        f2 = VMobject(color=PURPLE,stroke_width=6).set_points_as_corners([[5,-2,0],[2.5,-1.7,0],[0,-0.3,0]])
        self.at("Recordings from single")
        self.play(Create(f1),Create(f2),run_time=1.0)
        self.at("traced back with dye")
        self.play(ShowPassingFlash(f1.copy().set_stroke(width=12)),
                  ShowPassingFlash(f2.copy().set_stroke(width=12)),run_time=1.0)
        c2 = hair_cell(2).move_to([-3,0,0])
        c1 = hair_cell(1).move_to([3,0,0])
        lab2 = lines2("outer zone · mostly regular","type II + boutons",BLUE,24).move_to([-3,2.45,0])
        lab1 = lines2("central zone · mostly irregular","type I + calyx",PURPLE,24).move_to([3,2.45,0])
        self.at("Regular fibers mostly")
        self.play(FadeOut(VGroup(zones,f1,f2,title)),FadeIn(lab2),run_time=0.6)
        self.at("type 2 hair cells")
        self.play(FadeIn(c2),run_time=0.7)
        self.at("bouton endings")
        self.play(Indicate(c2[2],color=BLUE),run_time=0.7)
        self.at("Irregular fibers mostly")
        self.play(FadeIn(lab1),run_time=0.6)
        self.at("type 1 cells")
        self.play(FadeIn(c1[:2]),run_time=0.7)
        self.at("ending called a calyx")
        self.play(Create(c1[2]),run_time=0.8)
        note = bchip("populations, not rules",GREY,26).move_to([0,-2.8,0])
        self.at("map holds for populations")
        self.play(FadeIn(note),run_time=0.7)
        self.finish()


class S03Calyx(SpokenScene):
    def construct(self):
        c2 = hair_cell(2).move_to([-3,0,0])
        c1 = hair_cell(1).move_to([3,0,0])
        lab2 = T("type II",28,BLUE).move_to([-3,2.45,0])
        lab1 = T("type I + calyx",28,PURPLE).move_to([3,2.45,0])
        self.at("The calyx is built")
        self.play(FadeIn(c2),FadeIn(c1),FadeIn(lab2),FadeIn(lab1),run_time=0.6)
        v2,v1 = vesicles(-3,-0.55),vesicles(3,-0.55)
        quantal = T("both release glutamate",26,TEXT).move_to([0,-2.75,0])
        self.at("Both hair cell types")
        self.play(FadeIn(v2),FadeIn(v1),FadeIn(quantal),run_time=0.6)
        self.at("release glutamate")
        self.play(v2[1].animate.shift(DOWN*0.35),v1[1].animate.shift(DOWN*0.35),run_time=0.7)
        mouse = T("mature mouse · release machinery missing",26,GREY).move_to([0,3.3,0])
        self.at("Yet a mature mouse")
        self.play(FadeIn(mouse),v1.animate.set_opacity(0.15),FadeOut(quantal),run_time=0.6)
        spikes = spike_train(1.3,4.7,-2.35,[0.05,0.3,0.36,0.62,0.9],PURPLE)
        self.at("still made its calyx fire")
        self.play(Create(spikes),Indicate(c1[2],color=PURPLE),run_time=0.8)
        missing = bchip("either release protein absent",GREY,24).move_to([0,-3.15,0])
        self.at("either of two proteins")
        self.play(FadeIn(missing),run_time=0.6)
        turtle = T("turtle · paired recordings · possible route",28,GREY).move_to([0,3.25,0])
        pair = hair_cell(1).move_to([-3.8,0.1,0])
        pips = VGroup(Polygon([-6,2.1,0],[-5.8,2.3,0],[-3.9,0.6,0],color=GREY,fill_opacity=0.2),
                      Polygon([-2.5,2.35,0],[-2.2,2.25,0],[-3.0,-0.2,0],color=GREY,fill_opacity=0.2))
        membranes = VGroup(Line([0,-1.7,0],[0,1.5,0],color=GREY,stroke_width=8),
                           Line([4,-1.7,0],[4,1.5,0],color=PURPLE,stroke_width=8))
        labels = VGroup(T("hair cell",24,GREY).move_to([0,2,0]),T("calyx",24,PURPLE).move_to([4,2,0]),
                        T("cleft · enlarged",24,GREY).move_to([2,-2.1,0]))
        self.at("Recordings in turtles")
        self.play(FadeOut(VGroup(c1,c2,lab1,lab2,v1,v2,mouse,missing,spikes)),
                  run_time=0.3)
        self.play(FadeIn(turtle),FadeIn(pair),FadeIn(pips),FadeIn(membranes),FadeIn(labels),run_time=0.5)
        fast = DoubleArrow([0.2,0.85,0],[3.8,0.85,0],buff=0,color=PURPLE,stroke_width=5)
        fl = T("current · fast",24,PURPLE).move_to([2,1.3,0])
        slow = DoubleArrow([0.2,-0.8,0],[3.8,-0.8,0],buff=0,color=PURPLE,stroke_width=4)
        sl = T("potassium · slower",24,PURPLE).move_to([2,-1.3,0])
        cloud = VGroup(*[Dot([0.4+i*0.35,-0.35+0.08*(i%2),0],radius=0.055,color=PURPLE) for i in range(8)])
        self.at("Current and potassium")
        self.play(GrowArrow(fast),FadeIn(fl),run_time=0.35)
        self.play(GrowArrow(slow),FadeIn(sl),FadeIn(cloud),run_time=0.7)
        self.play(cloud.animate.shift(RIGHT*0.6),run_time=0.8)
        no = T("no vesicles · no gap junctions",26,TEXT).move_to([0,-3.05,0])
        self.at("with no vesicles")
        self.play(FadeIn(no),run_time=0.6)
        self.at("little synaptic delay")
        self.play(Indicate(fast,color=PURPLE),run_time=0.65)
        self.finish()


class S04Built(SpokenScene):
    def construct(self):
        hypothesis = lines2("short delay → fast reflexes","proposed in reviews",PURPLE,28).move_to([0,0.5,0])
        self.at("Reviews propose")
        self.play(FadeIn(hypothesis),run_time=0.7)
        timeline = VGroup(arr([-5.6,2.2,0],[5.5,2.2,0],GREY),
                          T("young mouse",26,GREY).move_to([-4.8,2.8,0]),
                          T("maturing",26,TEXT).move_to([4.8,2.8,0]))
        self.at("channels form as")
        self.play(FadeOut(hypothesis),FadeIn(timeline),run_time=0.6)
        mem = Line([-4.8,-1.6,0],[-4.8,0.8,0],color=GREY,stroke_width=8)
        ml = T("K+ channels",24,TEXT).move_to([-4.8,1.25,0])
        chans = VGroup(*[RoundedRectangle(width=0.35,height=0.28,corner_radius=0.05,
                                         color=TEXT,fill_opacity=0.5).move_to([-4.8,y,0]) for y in [-1,-0.4,0.2]])
        ax = Axes(x_range=[0,1,1],y_range=[0,1,1],x_length=2,y_length=1.65,tips=False,
                  axis_config={"include_ticks":False,"color":GREY}).move_to([-1.6,-0.3,0])
        curve = ax.plot(lambda t:1-np.exp(-2*t),x_range=[0,1,0.02],color=TEXT)
        cl = T("hair-cell signal",24,TEXT).move_to([-1.6,1.25,0])
        cal = hair_cell(1).scale(0.65).move_to([1.55,-0.45,0])
        calab = T("type I → calyx",24,PURPLE).move_to([1.55,1.25,0])
        fibre = spike_train(3.6,5.9,-0.7,np.linspace(0,1,9),PURPLE)
        fl = T("fibre spikes",24,PURPLE).move_to([4.8,1.25,0])
        self.at("In young mice")
        self.play(Create(mem),Create(ax),Create(curve),FadeIn(cal),Create(fibre),FadeIn(VGroup(ml,cl,calab,fl)),run_time=0.6)
        self.at("new potassium channels")
        self.play(FadeIn(chans),run_time=0.6)
        self.at("speed up hair cell signals")
        self.play(Transform(curve,ax.plot(lambda t:1-np.exp(-9*t),x_range=[0,1,0.02],color=TEXT)),run_time=0.7)
        direct = arr([0.8,-1.65,0],[2.3,-1.65,0],PURPLE)
        self.at("make type 1 transmission")
        self.play(GrowArrow(direct),Indicate(cal[2],color=PURPLE),run_time=0.6)
        self.at("make afferent firing")
        self.play(Transform(fibre,spike_train(3.6,5.9,-0.7,[0.01,0.05,0.22,0.49,0.53,0.55,0.8,0.98],PURPLE)),run_time=0.7)
        h = head_icon(TEXT,1.3).move_to([-3.7,0,0])
        conductor = RoundedRectangle(width=0.5,height=0.8,corner_radius=0.1,color=TEXT,fill_opacity=0.3).move_to([-4.65,0,0])
        name = T("sound + bone vibration",30,TEXT).move_to([0,2.7,0])
        reg = spike_train(-0.8,4.7,0.5,np.linspace(0,1,12),BLUE).set_opacity(0.4)
        irr = spike_train(-0.8,4.7,-1,[0.02,0.18,0.2,0.21,0.5,0.7,0.73,0.77,0.98],PURPLE).set_opacity(0.4)
        labels = VGroup(T("regular",24,BLUE).move_to([1.8,1.2,0]),T("irregular",24,PURPLE).move_to([1.8,-1.7,0]))
        self.at("Clinicians use")
        self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.3)
        self.play(FadeIn(h),FadeIn(conductor),FadeIn(name),FadeIn(reg),FadeIn(irr),FadeIn(labels),run_time=0.4)
        self.at("Sound and vibration tests")
        self.play(Wiggle(conductor,rotation_angle=0.08),run_time=0.8)
        self.at("mostly drive")
        self.play(irr.animate.set_opacity(1),run_time=0.35)
        self.play(Indicate(irr,color=PURPLE),run_time=0.35)
        mostly = bchip("mostly irregular fibres",PURPLE,28).move_to([0,-2.9,0])
        self.play(FadeIn(mostly),run_time=0.4)
        self.finish()


class S05Cancel(SpokenScene):
    def construct(self):
        xl,xr = -3.3,3.3
        hl = head_icon(GREEN,1.25).move_to([xl,1.6,0])
        hr = head_icon(ORANGE,1.25).move_to([xr,1.6,0])
        al = turn_arrow(hl.get_center(),GREEN,r=1.0)
        ar = turn_arrow(hr.get_center(),ORANGE,r=1.0)
        tl = T("own turn",28,GREEN).move_to([xl,3.2,0])
        tr = T("passive turn",28,ORANGE).move_to([xr,3.2,0])
        bl,tkl = ticks(-5.4,-1.2,0,12,BLUE,3,h=0.4)
        br,tkr = ticks(1.2,5.4,0,12,BLUE,5,h=0.4)
        firing = T("afferents: both keep firing",26,BLUE).move_to([0,-0.6,0])
        self.at("Afferents fire")
        self.play(FadeIn(hl),FadeIn(tl),Create(al),Create(bl),Create(tkl),run_time=0.6)
        self.at("turn your head")
        self.play(Rotate(hl,-PI/4),run_time=0.5)
        self.at("something turns it")
        self.play(FadeIn(hr),FadeIn(tr),Create(ar),Create(br),Create(tkr),FadeIn(firing),run_time=0.3)
        self.play(Rotate(hr,-PI/4),run_time=0.3)
        base = Line([-5.6,-2.25,0],[5.6,-2.25,0],color=GREY)
        def response(x,height,color):
            return Rectangle(width=1.0,height=height,color=color,fill_opacity=0.4).move_to([x,-2.25+height/2,0])
        active = response(xl,0.18,YELLOW)
        passive = response(xr,1.05,YELLOW)
        tag = T("alert monkeys · Roy & Cullen",24,GREY).move_to([0,2.65,0])
        nl = T("vestibular-only neuron response · schematic",24,YELLOW).move_to([0,-2.75,0])
        self.at("In Alert Monkeys")
        self.play(FadeIn(tag),Create(base),FadeIn(nl),run_time=0.6)
        # Show the observed low active response only when it is spoken.
        self.at("responded much less")
        self.play(GrowFromEdge(passive,DOWN),FadeIn(active),run_time=0.8)
        match = bchip("match?",GREY,26).move_to([0,0.8,0])
        expected = bchip("prediction",GREEN,24).move_to([-1.65,1.65,0])
        actual = bchip("neck feedback",TEALN,24).move_to([1.65,1.65,0])
        links = VGroup(arr(expected.get_bottom(),match.get_top()+LEFT*0.25,GREEN),
                       arr(actual.get_bottom(),match.get_top()+RIGHT*0.25,TEALN))
        self.at("held only when")
        self.play(FadeOut(tag),FadeIn(match),
                  VGroup(hl,al,tl).animate.shift(LEFT*1.0),
                  VGroup(hr,ar,tr).animate.shift(RIGHT*1.0),run_time=0.5)
        self.at("neck feedback matched")
        self.play(FadeIn(actual),run_time=0.5)
        self.at("motor command predicted")
        self.play(FadeIn(expected),*[GrowArrow(a) for a in links],
                  Transform(match,bchip("match",GREEN,26).move_to(match)),run_time=0.65)
        self.at("When the match failed")
        self.play(Transform(match,bchip("mismatch",RED,26).move_to(match)),
                  FadeOut(active),run_time=0.4)
        self.at("response came back")
        restored = response(xl,1.05,YELLOW)
        self.play(GrowFromEdge(restored,DOWN),run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        title = T("Three ideas in order",34,font=TITLE_FONT).move_to([0,2.7,0])
        self.at("Keep three ideas")
        self.play(FadeIn(title),run_time=0.6)
        def row(n,text,y,color):
            badge = VGroup(Circle(radius=0.27,color=color,fill_opacity=0.16),M(str(n),24,color)).move_to([-5.9,y,0])
            badge[1].move_to(badge[0])
            label = T(text,28,color).next_to(badge,RIGHT,buff=0.35)
            return VGroup(badge,label)
        r1 = row(1,"Two channels",1.85,TEXT)
        reg = spike_train(-0.8,4.9,1.7,np.linspace(0,1,14),BLUE)
        irr = spike_train(-0.8,4.9,0.95,[0.02,0.17,0.2,0.21,0.5,0.7,0.73,0.77,0.98],PURPLE)
        r2 = row(2,"Calyx without vesicles",-0.4,PURPLE)
        calyx = hair_cell(1).scale(0.4).move_to([0.65,-0.4,0])
        direct = arr([1.45,-0.4,0],[4.9,-0.4,0],PURPLE)
        r3 = row(3,"Central cancelling",-1.9,YELLOW)
        match = bchip("neck feedback = prediction",GREEN,24).move_to([2.4,-1.9,0])
        self.at("ear splits head motion")
        rate = T("rate",24,BLUE).move_to([5.65,1.85,0])
        timing = T("timing",24,PURPLE).move_to([5.65,1.1,0])
        self.play(FadeIn(r1),Create(reg),FadeIn(rate),run_time=0.7)
        self.at("a fast channel")
        self.play(Create(irr),FadeIn(timing),run_time=0.6)
        self.at("calyx can drive")
        self.play(FadeIn(r2),FadeIn(calyx),run_time=0.6)
        self.at("without vesicles")
        self.play(GrowArrow(direct),run_time=0.6)
        self.at("thought to keep")
        self.play(ShowPassingFlash(direct.copy()),run_time=0.6)
        self.at("neurons tested")
        self.play(FadeIn(r3),run_time=0.6)
        self.at("neck feedback matched")
        self.play(FadeIn(match),run_time=0.6)
        last = T("You still feel your own turns",32,TEXT,font=TITLE_FONT).move_to([0,-3.1,0])
        self.at("You still feel")
        self.play(FadeIn(last),run_time=0.6)
        self.at("What changes is the reflex")
        self.play(Indicate(r3,color=YELLOW),run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "The ear splits head motion into a sustained and a fast channel."
