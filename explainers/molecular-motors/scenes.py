"""Grip, Swing, Let Go — molecular motors and cargo.

COLOR MAP
  BLUE   microtubule
  ORANGE kinesin-1
  PURPLE dynein
  GREEN  actin / ATP
  RED    myosin II
  YELLOW cargo
  GOLD   thick filament
  TEXT   cell, annotations, outlines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def microtubule(y=-1.15, width=12.2, tiles=16):
    """Polar tiled bar. Every chevron points toward the plus end."""
    bar = RoundedRectangle(width=width, height=1.24, corner_radius=0.24,
                           stroke_color=BLUE, stroke_width=4,
                           fill_color=BLUE, fill_opacity=0.58).move_to([0, y, 0])
    xs = np.linspace(-width / 2 + 0.42, width / 2 - 0.42, tiles)
    marks = VGroup(*[
        VGroup(Line([x - .18, y - .22, 0], [x + .10, y, 0]),
               Line([x + .10, y, 0], [x - .18, y + .22, 0]))
        .set_stroke(BLUE, 4) for x in xs
    ])
    return VGroup(bar, marks)


def actin(y=-1.15, width=12.2):
    return VGroup(
        Line([-width/2, y-.14, 0], [width/2, y-.14, 0], color=GREEN, stroke_width=11),
        Line([-width/2, y+.14, 0], [width/2, y+.14, 0], color=GREEN, stroke_width=11),
    )


def polarity(y=-1.9):
    return VGroup(T("−", 42, BLUE).move_to([-6.05, y, 0]),
                  T("← cell body", 28, TEXT).move_to([-4.75, y, 0]),
                  T("synapse →", 28, TEXT).move_to([4.65, y, 0]),
                  T("+", 42, BLUE).move_to([6.05, y, 0]))


def cargo(center=(0, 1.35, 0), radius=.58):
    return Circle(radius=radius, color=YELLOW, stroke_width=4,
                  fill_color=YELLOW, fill_opacity=.32).move_to(center)


def two_foot_motor(x=-3.4, track_y=-1.15, color=ORANGE, scale=1.0, with_cargo=True):
    """A deliberately schematic two-foot walker, not a molecular structure."""
    fy = track_y + .42
    feet = VGroup(*[
        RoundedRectangle(width=.72*scale, height=.34*scale, corner_radius=.13,
                         color=color, stroke_width=3, fill_color=color, fill_opacity=.45)
        .move_to([x+d*scale, fy, 0]) for d in (-.48, .48)
    ])
    hip = Dot([x, track_y+1.42*scale, 0], radius=.14*scale, color=color)
    legs = VGroup(*[Line(f.get_top(), hip.get_center(), color=color, stroke_width=5) for f in feet])
    stalk = Line(hip.get_center(), [x, track_y+2.05*scale, 0], color=color, stroke_width=6)
    parts = [feet, legs, hip, stalk]
    if with_cargo:
        parts.append(cargo((x, track_y+2.52*scale, 0), .48*scale))
    g = VGroup(*parts)
    g.feet, g.legs, g.hip, g.stalk = feet, legs, hip, stalk
    g.cargo = parts[-1] if with_cargo else None
    return g


def abstract_motor(x=3.4, track_y=-1.15, color=PURPLE):
    foot = RoundedRectangle(width=1.15, height=.48, corner_radius=.2, color=color,
                            stroke_width=3, fill_color=color, fill_opacity=.4).move_to([x, track_y+.46, 0])
    stem = Line(foot.get_top(), [x, track_y+1.65, 0], color=color, stroke_width=7)
    bead = cargo((x, track_y+2.08, 0), .42)
    return VGroup(foot, stem, bead)


def shimmer(track, color=TEXT):
    """A moving highlight tied to a track, keeping long explanatory holds alive."""
    d = RoundedRectangle(width=1.35, height=max(.82, track.height*.82), corner_radius=.12,
                         stroke_width=0, fill_color=color, fill_opacity=.72).move_to(track.get_left()+RIGHT*.8)
    d.t = 0.0
    left, width, y = track.get_left()[0]+.2, track.width-.4, track.get_center()[1]
    def move(m, dt):
        m.t = (m.t + dt*.12) % 1
        m.move_to([left + width*m.t, y, 0])
    d.add_updater(move)
    return d


def cycle_dial(center=(4.65, 2.15, 0), radius=1.18, size=25):
    ring = Circle(radius=radius, color=GREY, stroke_width=2).move_to(center)
    labs = VGroup(
        T("GRIP", size, ORANGE).move_to(np.array(center)+UP*radius),
        T("SWING", size, ORANGE).move_to(np.array(center)+RIGHT*radius),
        T("LET GO", size, ORANGE).move_to(np.array(center)+DOWN*radius),
        T("RE-COCK", size, ORANGE).move_to(np.array(center)+LEFT*radius),
    )
    pointer = Arrow(center, np.array(center)+UP*(radius-.18), buff=0, color=YELLOW,
                    stroke_width=4, tip_length=.18)
    return VGroup(ring, labs, pointer)


def question_world(idle=False):
    tr = actin(-1.55)
    motor = two_foot_motor(0, -1.55, RED, 1.12)
    motor.cargo.scale(1.3)
    label = T("myosin II", 30, RED).next_to(motor, LEFT, buff=.35)
    q = T("One myosin II, one vesicle: can it walk?", 36, TEXT).move_to([0, 3.0, 0])
    return tr, motor, label, q


class S00Title(TitleCard):
    LESSON = "Molecular Motors and Cargo"
    TITLE = "Grip, Swing, Let Go"

    def construct(self):
        soma = Ellipse(width=2.25, height=2.7, color=TEXT, stroke_width=3,
                       fill_color=TEXT, fill_opacity=.06).move_to([-5.2, -.65, 0])
        axon = Line([-4.2, -.65, 0], [5.5, -.65, 0], color=TEXT, stroke_width=8).set_opacity(.22)
        syn = Circle(.46, color=TEXT, fill_color=TEXT, fill_opacity=.07).move_to([5.85, -.65, 0])
        world = VGroup(soma, axon, syn).set_opacity(.30)
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = T(self.TITLE, 54, TEXT, font=TITLE_FONT)
        rule = Line(LEFT*1.2, RIGHT*1.2, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=.3).shift(UP*.8)
        self.add(world)
        self.play(FadeIn(card, shift=UP*.1), run_time=.6)
        self.wait(.7)
        self.play(FadeOut(card), world.animate.set_opacity(.65), run_time=.5)
        self.finish()


class S01Hook(SpokenScene):
    def construct(self):
        soma = Ellipse(width=2.35, height=3.0, color=TEXT, stroke_width=4,
                       fill_color=TEXT, fill_opacity=.08).move_to([-5.15, .15, 0])
        axon = Line([-4.05, .15, 0], [5.55, .15, 0], color=TEXT, stroke_width=10)
        syn = Circle(.55, color=TEXT, fill_color=TEXT, fill_opacity=.10).move_to([5.92, .15, 0])
        dim = VGroup(Line([-4.0,-1.18,0],[5.52,-1.18,0],color=GREY),
                     Line([-4,-1.34,0],[-4,-1.02,0],color=GREY), Line([5.52,-1.34,0],[5.52,-1.02,0],color=GREY),
                     T("up to 1 m (schematic)", 28, TEXT).move_to([.75,-1.68,0]))
        self.add(soma, axon, syn, dim)
        soma_base=soma.copy(); soma.phase=0.
        def breathe(m,dt):
            m.phase += dt
            m.become(soma_base.copy().scale(1+.045*np.sin(2.2*m.phase)))
        soma.add_updater(breathe)
        self.at("protein made")
        dot = Dot([-5.15,.15,0], radius=.29, color=YELLOW)
        dot.phase = 0.
        def jiggle(m, dt):
            m.phase += dt
            m.move_to([-5.15+.42*np.sin(5*m.phase), .15+.48*np.sin(7*m.phase), 0])
        dot.add_updater(jiggle)
        self.add(dot)
        self.at("Left to diffuse")
        diff = T("diffusion", 30, YELLOW).move_to([-5.0,2.15,0])
        self.play(FadeIn(diff), run_time=.4)
        self.at("take centuries")
        counter = M("~600 years", 42, YELLOW).move_to([-1.0,2.55,0])
        basis = T("GFP; 1 m", 28, TEXT).next_to(counter, DOWN, buff=.20)
        self.play(Write(counter), FadeIn(basis), run_time=.8)
        self.at("how does it get there")
        q = T("?", 82, YELLOW).move_to([5.9,1.45,0])
        self.play(GrowFromCenter(q), run_time=.55)
        self.at("hands it to a motor")
        dot.clear_updaters()
        soma.clear_updaters()
        close_track = microtubule(-1.3, 11.8)
        motor = two_foot_motor(-2.5,-1.3,ORANGE,.95)
        motor.cargo.become(cargo((-2.5,1.1,0),.48))
        self.play(FadeOut(VGroup(soma,axon,syn,dim,diff,counter,basis,q,dot)), run_time=.3)
        self.add(close_track, motor)
        self.play(Indicate(motor.feet, color=ORANGE), run_time=.65)
        self.finish()


class S02Track(SpokenScene):
    def construct(self):
        tr = microtubule(-1.2)
        glint = shimmer(tr[0], BLUE)
        self.add(tr, glint)
        self.at("road is a microtubule")
        self.play(Indicate(tr[0], color=BLUE, scale_factor=1.02), run_time=.8)
        self.at("road has a direction")
        self.play(LaggedStart(*[Indicate(m, color=TEXT, scale_factor=1.15) for m in tr[1]], lag_ratio=.05), run_time=1.2)
        self.play(LaggedStart(*[Indicate(m, color=YELLOW, scale_factor=1.12) for m in tr[1]], lag_ratio=.05), run_time=2.7)
        self.at("plus end out")
        ends = polarity(-2.05)
        self.play(FadeIn(ends), run_time=.65)
        self.at("Kientsin -1 walks")
        kin = two_foot_motor(-4.4,-1.2,ORANGE,1.02)
        kl = T("kinesin-1", 30, ORANGE).move_to([-4.4,2.2,0])
        self.play(FadeIn(kin), FadeIn(kl), run_time=.45)
        self.play(kin.animate.shift(RIGHT*4.0), run_time=1.8, rate_func=linear)
        self.at("Dining walks")
        dyn = abstract_motor(4.5,-1.2)
        dl = T("dynein", 30, PURPLE).move_to([4.5,2.2,0])
        self.play(FadeIn(dyn), FadeIn(dl), run_time=.4)
        self.play(dyn.animate.shift(LEFT*4.1), kin.animate.shift(RIGHT*1.5), run_time=2.1, rate_func=linear)
        self.finish()


class S03Cycle(SpokenScene):
    def construct(self):
        tr = microtubule(-2.15, 12.2, 12)
        foot = RoundedRectangle(width=2.15,height=.72,corner_radius=.25,color=ORANGE,stroke_width=5,
                                fill_color=ORANGE,fill_opacity=.42).move_to([-2.55,-1.48,0])
        neck = Line(foot.get_top(),[-2.55,.65,0],color=ORANGE,stroke_width=12)
        load = cargo((-2.55,1.35,0),.62)
        dial = cycle_dial((4.55,1.7,0),1.25,28)
        glint = shimmer(tr[0], BLUE)
        self.add(tr, foot, neck, load, dial, glint)
        self.at("Watch one foot")
        self.play(Indicate(foot, color=YELLOW), run_time=.7)
        self.at("grips the track")
        self.play(foot.animate.shift(DOWN*.30), Indicate(dial[1][0],color=YELLOW), run_time=.65)
        self.at("swings while gripping")
        self.play(Rotate(neck,angle=-.42,about_point=foot.get_top()), load.animate.shift(RIGHT*1.05),
                  Indicate(dial[1][1],color=YELLOW), Rotate(dial[2],-PI/2,about_point=dial[0].get_center()), run_time=1.2)
        self.at("pulls the motor forward")
        self.play(neck.animate.shift(RIGHT*.45), foot.animate.shift(RIGHT*.45), run_time=.6)
        self.at("lets go")
        self.play(foot.animate.shift(UP*.65), Indicate(dial[1][2],color=YELLOW),
                  Rotate(dial[2],-PI/2,about_point=dial[0].get_center()), run_time=.65)
        self.at("and recocks")
        self.play(Rotate(neck,angle=.42,about_point=neck.get_start()), foot.animate.shift(RIGHT*.6),
                  Indicate(dial[1][3],color=YELLOW), Rotate(dial[2],-PI/2,about_point=dial[0].get_center()), run_time=.8)
        self.at("one ATP")
        badge = chip("1 ATP per cycle",GREEN,28).move_to([1.6,2.8,0])
        self.play(FadeIn(badge), Rotate(dial[2],-2*PI,about_point=dial[0].get_center()), run_time=1.5, rate_func=linear)
        self.finish()


class S04Idea(SpokenScene):
    def construct(self):
        tr=microtubule(-1.25); ends=polarity(-2.08); glint=shimmer(tr[0],BLUE)
        kin=two_foot_motor(-3.7,-1.25,ORANGE,.95); dial=cycle_dial((4.75,2.25,0),1.0,28)
        self.add(tr,ends,kin,dial,glint)
        self.at("motor has feet")
        self.play(Indicate(kin.feet,color=YELLOW),run_time=.55)
        self.at("polar track")
        self.play(LaggedStart(*[Indicate(m,color=TEXT) for m in tr[1]],lag_ratio=.04),run_time=.9)
        self.at("each repeating")
        self.play(Rotate(dial[2],-2*PI,about_point=dial[0].get_center()),run_time=1.5,rate_func=linear)
        self.at("swing points")
        swing=CurvedArrow([-3.6,.05,0],[-2.25,.05,0],angle=-.6,color=ORANGE,stroke_width=5)
        self.play(Create(swing),kin.animate.shift(RIGHT*2.2),run_time=1.2)
        self.at("dining is less tidy")
        dyn=abstract_motor(3.4,-1.25); dl=T("dynein",28,PURPLE).move_to([1.9,2.55,0])
        self.play(FadeIn(dyn),FadeIn(dl),FadeOut(swing),run_time=.4)
        self.play(dyn.animate.shift(LEFT*2.2),kin.animate.shift(RIGHT*1.2),run_time=1.25,rate_func=linear)
        self.finish()


def binding_ticks(y=-1.82, xs=None):
    xs=np.arange(-5.6,5.7,.9) if xs is None else xs
    return VGroup(*[Line([x,y-.12,0],[x,y+.12,0],color=TEXT,stroke_width=2) for x in xs])


class S05TwoFeet(SpokenScene):
    def construct(self):
        tr=microtubule(-1.45,12.2,13); ticks=binding_ticks(-1.94); glint=shimmer(tr[0],BLUE)
        m=two_foot_motor(-3.6,-1.45,ORANGE,1.28); m.feet[0].set_color("#F6B66E"); m.feet[1].set_color(ORANGE)
        scale=T("binding sites: 8 nm apart",28,TEXT).move_to([0,-2.55,0])
        self.add(tr,ticks,m,scale,glint)
        self.at("has 2 feet")
        self.play(Indicate(m.feet,color=YELLOW),run_time=.7)
        self.at("back foot lets go")
        back=m.feet[0]; front=m.feet[1]
        self.play(back.animate.shift(UP*.85),run_time=.65)
        self.at("still gripping")
        self.play(Indicate(front,color=YELLOW),run_time=.55)
        self.at("swings and tips it past")
        path=ArcBetweenPoints(back.get_center(),back.get_center()+RIGHT*2.05+DOWN*.85,angle=-PI/2)
        self.play(MoveAlongPath(back,path),m.hip.animate.shift(RIGHT*.9),m.stalk.animate.shift(RIGHT*.9),m.cargo.animate.shift(RIGHT*.9),run_time=1.35)
        self.at("feet swap rolls")
        self.play(back.animate.set_color(ORANGE),front.animate.set_color("#F6B66E"),run_time=.45)
        path2=ArcBetweenPoints(front.get_center(),front.get_center()+RIGHT*2.05,angle=-PI/2)
        self.play(MoveAlongPath(front,path2),m.hip.animate.shift(RIGHT*.9),m.stalk.animate.shift(RIGHT*.9),m.cargo.animate.shift(RIGHT*.9),run_time=1.2)
        self.at("Think of walking")
        head=Dot([-4.7,2.55,0],radius=.20,color=TEXT); body=Line([-4.7,2.3,0],[-4.7,1.35,0],color=TEXT,stroke_width=5)
        legs=VGroup(Line([-4.7,1.35,0],[-5.2,.55,0],color=TEXT,stroke_width=5),Line([-4.7,1.35,0],[-4.2,.55,0],color=TEXT,stroke_width=5))
        walker=VGroup(head,body,legs); hipdot=Dot([-4.7,1.35,0],radius=.11,color=YELLOW)
        self.play(FadeOut(scale),FadeIn(walker),FadeIn(hipdot),run_time=.4)
        self.at("hips move one step")
        self.play(walker.animate.shift(RIGHT*2.0),hipdot.animate.shift(RIGHT*2.0),
                  Rotate(legs[0],angle=-1.0,about_point=legs[0].get_start()),run_time=1.3)
        self.finish()


class S06Numbers(SpokenScene):
    def construct(self):
        tr=microtubule(-1.45); ticks=binding_ticks(-1.94); m=two_foot_motor(-4,-1.45,ORANGE,1.12); glint=shimmer(tr[0],BLUE)
        self.add(tr,ticks,m,glint)
        self.at("cargo rides at the hips")
        hipbr=VGroup(Line([-4.0,2.22,0],[-3.1,2.22,0],color=YELLOW,stroke_width=4),
                     Line([-4.0,2.05,0],[-4.0,2.39,0],color=YELLOW,stroke_width=4),
                     Line([-3.1,2.05,0],[-3.1,2.39,0],color=YELLOW,stroke_width=4),
                     T("cargo / centre: 8 nm",30,YELLOW).move_to([-1.25,2.22,0]))
        self.play(FadeIn(hipbr),m.animate.shift(RIGHT*.9),run_time=1.0)
        self.at("Each foot moves")
        footbr=VGroup(Line([-3.6,-2.5,0],[-1.8,-2.5,0],color=ORANGE,stroke_width=4),
                      Line([-3.6,-2.67,0],[-3.6,-2.33,0],color=ORANGE,stroke_width=4),
                      Line([-1.8,-2.67,0],[-1.8,-2.33,0],color=ORANGE,stroke_width=4),
                      T("one head: ~16 nm",30,ORANGE).move_to([-2.7,-3.0,0]))
        self.play(FadeOut(hipbr),FadeIn(footbr),m.feet[0].animate.shift(RIGHT*1.8),run_time=1.1)
        self.at("low load")
        readout=VGroup(T("low load, in vitro",26,TEXT),M("steps: 0    ATP: 0",30,GREEN)).arrange(DOWN,buff=.18).move_to([3.9,2.4,0])
        self.play(FadeOut(footbr),FadeIn(readout),run_time=.4)
        self.at("each step costs")
        for n in (1,2,3):
            atp=chip("ATP",GREEN,28).move_to([m.get_x()+.2,2.65,0])
            new=M(f"steps: {n}    ATP: {n}",30,GREEN).move_to(readout[1])
            self.play(FadeIn(atp),m.animate.shift(RIGHT*.75),Transform(readout[1],new),run_time=.55)
            self.play(FadeOut(atp),run_time=.18)
        self.finish()


class S07Trick(SpokenScene):
    def construct(self):
        tr=microtubule(-1.35); m=two_foot_motor(-4.8,-1.35,ORANGE,.98); glint=shimmer(tr[0],BLUE)
        self.add(tr,m,glint)
        self.at("gripping foot nearly always stays on")
        note=T("nearly always one foot bound",30,ORANGE).move_to([0,2.75,0])
        self.play(FadeIn(note),Indicate(m.feet[0],color=YELLOW),run_time=.7)
        self.at("stepping foot lands")
        self.play(m.feet[1].animate.shift(RIGHT*.9),Indicate(m.feet[1],color=YELLOW),run_time=.65)
        self.at("about a hundred steps")
        self.play(FadeOut(note),m.animate.scale(.74).move_to([-5,-.05,0]),run_time=.7)
        counter=M("0 steps",40,ORANGE).move_to([0,2.65,0])
        bracket=VGroup(Line([-5.1,-2.5,0],[4.8,-2.5,0],color=TEXT),
                       T("under 1 micrometre",28,TEXT).move_to([0,-3,0]))
        self.play(FadeIn(counter),FadeIn(bracket),run_time=.35)
        for n in (20,40,60,80,100):
            new=M(f"{n} steps",40,ORANGE).move_to(counter)
            self.play(m.animate.shift(RIGHT*1.85),Transform(counter,new),run_time=.48,rate_func=linear)
        self.at("before it lets go")
        in_vitro=T("about 100 steps, in vitro",28,TEXT).move_to([0,1.8,0])
        self.play(m.animate.shift(UP*.9),FadeIn(in_vitro),run_time=.7)
        self.at("called processive")
        word=T("PROCESSIVE",48,ORANGE,weight=BOLD).move_to([0,.45,0])
        self.play(FadeIn(word),run_time=.35)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        blue=microtubule(-1.55)
        q=T("One myosin II, one vesicle: can it walk?",36,TEXT).move_to([0,3.0,0])
        self.add(blue,q)
        self.at("Muscle myosin 2")
        tr,m,label,_=question_world()
        self.play(ReplacementTransform(blue,tr),FadeIn(m),FadeIn(label),run_time=.8)
        self.add(shimmer(tr[0],GREEN))
        self.at("Could one molecule")
        self.play(Indicate(q,color=YELLOW),run_time=.55)
        self.at("all on its own")
        self.play(m.feet[0].animate.shift(UP*.22),m.feet[1].animate.shift(DOWN*.08),run_time=.55,rate_func=there_and_back)
        self.at("Pause and predict")
        self.play(Indicate(q,color=YELLOW),m.feet[1].animate.shift(UP*.22),run_time=.65,rate_func=there_and_back)
        self.finish()


class S09Hold(Scene):
    def construct(self):
        tr,m,label,q=question_world(True)
        self.add(tr,m,label,q,shimmer(tr[0],GREEN))
        for _ in range(3):
            self.play(m.feet[0].animate.shift(UP*.12),m.feet[1].animate.shift(DOWN*.06),run_time=.7,rate_func=there_and_back)
            self.play(m.feet[1].animate.shift(UP*.12),m.feet[0].animate.shift(DOWN*.06),run_time=.7,rate_func=there_and_back)


class S10Crowd(SpokenScene):
    def construct(self):
        tr,m,label,q=question_world(); self.add(tr,m,label,q,shimmer(tr[0],GREEN))
        cross=VGroup(Line([2.0,2.65,0],[5.7,3.25,0],color=RED,stroke_width=8),
                     Line([2.0,3.25,0],[5.7,2.65,0],color=RED,stroke_width=8))
        self.play(Create(cross),run_time=.45)
        self.at("spends most of its cycle off")
        self.play(m.feet[0].animate.shift(UP*.95),run_time=.9)
        self.play(m.feet[0].animate.shift(DOWN*.95),m.feet[1].animate.shift(UP*.95),run_time=.65)
        self.at("do not take turns")
        self.play(m.feet[0].animate.shift(UP*.95),m.feet[1].animate.shift(DOWN*.95),run_time=.65)
        self.at("falls away")
        fallen=T("one molecule falls away",32,RED).move_to([0,1.4,0])
        self.play(FadeOut(VGroup(q,cross,label)),m.animate.shift(DOWN*2.5).set_opacity(0),FadeIn(fallen),run_time=.9)
        self.at("works in crowds")
        thick=RoundedRectangle(width=11.7,height=.55,corner_radius=.12,color=GOLD,stroke_width=4,
                               fill_color=GOLD,fill_opacity=.3).move_to([0,-2.35,0])
        heads=VGroup(*[Line([x,-2.05,0],[x+.13,-1.45+(i%3)*.10,0],color=RED,stroke_width=5)
                       for i,x in enumerate(np.linspace(-5.4,5.4,20))])
        thicklab=T("thick filament",28,GOLD).move_to([0,-3.05,0])
        crowdlab=T("hundreds of heads",32,RED).move_to([0,1.55,0])
        self.play(FadeOut(fallen),FadeIn(thick),LaggedStart(*[Create(h) for h in heads],lag_ratio=.025),FadeIn(thicklab),run_time=1.1)
        self.at("hundreds of heads")
        self.play(FadeIn(crowdlab),LaggedStart(*[Indicate(heads[i],color=YELLOW) for i in range(0,20,3)],lag_ratio=.08),run_time=1.1)
        self.finish()


def sarcomere():
    zl=VGroup(Line([-5.8,-2.3,0],[-5.8,2.3,0],color=TEXT,stroke_width=7),
              Line([5.8,-2.3,0],[5.8,2.3,0],color=TEXT,stroke_width=7))
    thin=VGroup(Line([-5.8,.72,0],[-.7,.72,0],color=GREEN,stroke_width=8),
                Line([5.8,-.72,0],[.7,-.72,0],color=GREEN,stroke_width=8))
    thick=RoundedRectangle(width=7.0,height=.55,corner_radius=.1,color=GOLD,stroke_width=4,
                           fill_color=GOLD,fill_opacity=.28)
    heads=VGroup(*[Line([x,.25,0],[x+.18,.70,0],color=RED,stroke_width=4) for x in np.linspace(-3,3,11)],
                 *[Line([x,-.25,0],[x-.18,-.70,0],color=RED,stroke_width=4) for x in np.linspace(-3,3,11)])
    return zl,thin,thick,heads


class S11Muscle(SpokenScene):
    def construct(self):
        zl,thin,thick,heads=sarcomere(); dial=cycle_dial((4.15,2.45,0),.90,28)
        zlabs=VGroup(T("Z",28,TEXT).move_to([-6.15,2.65,0]),T("Z",28,TEXT).move_to([6.15,2.65,0]))
        self.add(zl,thin,thick,heads,zlabs,dial)
        self.add(shimmer(thin[0],GREEN),shimmer(thin[1],GREEN))
        self.at("crowd shortens muscle")
        self.play(Indicate(thick,color=YELLOW),run_time=1.0)
        self.at("Heads grip")
        self.play(LaggedStart(*[Indicate(heads[i],color=YELLOW) for i in range(0,len(heads),3)],lag_ratio=.05),run_time=1.0)
        self.at("swing, and let go")
        self.play(Rotate(dial[2],-2*PI,about_point=dial[0].get_center()),run_time=1.1,rate_func=linear)
        self.at("slide inward")
        overlap=VGroup(Rectangle(width=2.3,height=.35,stroke_width=0,fill_color=GREEN,fill_opacity=.16).move_to([-2.35,.72,0]),
                       Rectangle(width=2.3,height=.35,stroke_width=0,fill_color=GREEN,fill_opacity=.16).move_to([2.35,-.72,0]))
        self.play(FadeIn(overlap),thin[0].animate.shift(RIGHT*1.25),thin[1].animate.shift(LEFT*1.25),
                  zl[0].animate.shift(RIGHT*1.25),zl[1].animate.shift(LEFT*1.25),run_time=2.0,rate_func=linear)
        self.at("No filament gets shorter")
        brackets=VGroup(Line([-4.55,1.35,0],[.55,1.35,0],color=GREEN,stroke_width=3),
                        Line([-3.5,-1.35,0],[3.5,-1.35,0],color=GOLD,stroke_width=3),
                        T("same length",28,TEXT).move_to([0,-2.05,0]))
        self.play(FadeIn(brackets),run_time=.6)
        self.at("overlap more")
        self.play(overlap.animate.set_fill(opacity=.48).scale(1.35),run_time=.8)
        self.finish()


class S12Metre(SpokenScene):
    def construct(self):
        tr=microtubule(-1.25); ends=polarity(-2.1); glint=shimmer(tr[0],BLUE)
        bigcargo=cargo((-4.2,1.55,0),.78)
        motors=VGroup(*[two_foot_motor(-4.7+i*.62,-1.25,ORANGE,.65,False) for i in range(3)])
        group=VGroup(bigcargo,motors)
        self.add(tr,ends,group,glint)
        self.at("Back to the meter")
        self.play(Indicate(bigcargo,color=YELLOW),run_time=.7)
        self.at("carries several motors")
        self.play(Indicate(motors,color=YELLOW),group.animate.shift(RIGHT*1.2),run_time=.9)
        self.at("one lets go")
        self.play(motors[0].animate.shift(UP*.9).set_opacity(.35),group.animate.shift(RIGHT*1.3),run_time=.9)
        self.at("another still holds")
        self.play(motors[0].animate.shift(DOWN*.9).set_opacity(1),Indicate(VGroup(motors[1],motors[2]),color=YELLOW),
                  group.animate.shift(RIGHT*1.2),run_time=.9)
        self.at("still being worked out")
        note=T("in cells: open question",32,TEXT).move_to([0,2.85,0])
        self.play(FadeIn(note),group.animate.shift(RIGHT*1.4),run_time=1.1,rate_func=linear)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        top=microtubule(1.05,11.7); bottom=actin(-2.05,11.7); divider=Line([-6.2,-.55,0],[6.2,-.55,0],color=GREY,stroke_width=2)
        kin=two_foot_motor(-4.4,1.05,ORANGE,.48,False)
        thick=RoundedRectangle(width=7.5,height=.38,corner_radius=.1,color=GOLD,fill_color=GOLD,fill_opacity=.25).move_to([0,-2.75,0])
        heads=VGroup(*[Line([x,-2.55,0],[x+.12,-2.15,0],color=RED,stroke_width=4) for x in np.linspace(-3.4,3.4,14)])
        labels=VGroup(T("one foot down: walks alone",28,ORANGE).move_to([2.5,2.95,0]),
                      T("feet mostly off: a crowd",28,RED).move_to([2.5,-3.25,0]))
        dial=cycle_dial((-4.75,-.80,0),.80,28)
        self.add(top,bottom,divider,kin,thick,heads,labels,dial)
        self.add(shimmer(top[0],BLUE),shimmer(bottom[0],GREEN))
        self.at("repeating one small cycle")
        self.play(Rotate(dial[2],-2*PI,about_point=dial[0].get_center()),
                  LaggedStart(*[Indicate(m,color=TEXT,scale_factor=1.15) for m in top[1]],lag_ratio=.04),
                  LaggedStart(*[Indicate(h,color=YELLOW) for h in heads[::2]],lag_ratio=.06),
                  run_time=2.9,rate_func=linear)
        self.at("Keep a foot on the track")
        self.play(Indicate(kin.feet[0],color=YELLOW),kin.animate.shift(RIGHT*3.4),labels[0].animate.set_color(YELLOW),run_time=1.5,rate_func=linear)
        self.at("travel far")
        self.play(kin.animate.shift(RIGHT*1.3),run_time=.7,rate_func=linear)
        self.at("Let go too often")
        self.play(labels[0].animate.set_color(ORANGE),labels[1].animate.set_color(YELLOW),
                  LaggedStart(*[Indicate(heads[i],color=YELLOW) for i in range(0,14,2)],lag_ratio=.05),run_time=.9)
        self.at("crowd can pull")
        self.play(bottom.animate.shift(LEFT*1.2),heads.animate.shift(RIGHT*.5),run_time=1.1,rate_func=linear)
        self.finish()


class S14End(EndCard):
    LINE = "Keep one foot down to walk alone."

    def construct(self):
        tr=microtubule(-2.45,11.5); m=two_foot_motor(-4.5,-2.45,ORANGE,.48,False)
        world=VGroup(tr,m).set_opacity(.28)
        line=T("Grip, swing, let go, re-cock:",42,TEXT,font=TITLE_FONT)
        takeaway=T(self.LINE,42,ORANGE,font=TITLE_FONT)
        sub=T("biochemistrypedia.com",24,TEAL)
        card=VGroup(line,takeaway,sub).arrange(DOWN,buff=.38).shift(UP*.75)
        self.add(world)
        self.play(FadeIn(card),run_time=.65)
        self.play(m.animate.shift(RIGHT*7.5),run_time=2.3,rate_func=linear)
        self.finish()
