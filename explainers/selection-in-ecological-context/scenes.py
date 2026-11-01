"""Selection has an agent  (Biochemistrypedia explainer, Ecology and Evolution)

COLOR MAP (one color per concept, whole video)
  PALE_C = the pale morph (typica): dots, bars, share segment
  DARK_C = the dark morph (carbonaria): dots, bars, share segment
  RED    = birds (the agent) and every "not this" reading
  YELLOW = the relative daily survival number and the arithmetic on it
  TEAL   = the dark share among survivors (the result)
  GREY   = frames, axes, labels, the wood
  GREEN  = the directly witnessed attacks (legacy helper palette)
  BLUE   = trait axes, pools and shallow beaks
  TEAL   = inheritance and measured fitness patterns
  RED    = ecological agents (birds, wasps, drought)
  PALE_C / DARK_C = contrasting guppy patterns as well as moth morphs
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PALE_C = "#E9DFC0"
DARK_C = "#B07A45"
R = 0.909


def moth(color, s=1.0):
    w1 = Ellipse(width=0.62, height=0.34, fill_color=color, fill_opacity=0.95, stroke_color=TEXT, stroke_width=1.5).shift(LEFT * 0.3 + UP * 0.05).rotate(0.25)
    w2 = Ellipse(width=0.62, height=0.34, fill_color=color, fill_opacity=0.95, stroke_color=TEXT, stroke_width=1.5).shift(RIGHT * 0.3 + UP * 0.05).rotate(-0.25)
    b = Ellipse(width=0.16, height=0.5, fill_color=color, fill_opacity=1, stroke_color=TEXT, stroke_width=1.5).shift(DOWN * 0.03)
    return VGroup(w1, w2, b).scale(s)


def cluster(color, cx, cy, s=1.1, dx=1.5, dy=1.5):
    ms = VGroup(*[moth(color, s).move_to([cx + (i - 1) * dx, cy + (0.5 - j) * dy, 0]) for j in range(2) for i in range(3)])
    return ms


def bar(x, h, color, base=-2.5, w=1.4):
    return Rectangle(width=w, height=max(h, 0.02), fill_color=color, fill_opacity=0.9, stroke_color=TEXT, stroke_width=2).move_to([x, base + max(h, 0.02) / 2, 0])


def cross(mob, color=RED):
    return Line(mob.get_left() + LEFT * 0.1, mob.get_right() + RIGHT * 0.1, color=color, stroke_width=4).move_to(mob.get_center())


def share(t):
    return R ** t / (1 + R ** t)


# Simple silhouettes extend the original ellipse-based moth drawing style.
def bird(tail=0.7, color=RED):
    body = Ellipse(width=0.65, height=0.42, color=color, fill_opacity=1)
    head = Circle(radius=0.17, color=color, fill_opacity=1).shift(RIGHT * 0.32 + UP * 0.19)
    beak = Polygon([0.45, 0.23, 0], [0.72, 0.13, 0], [0.45, 0.06, 0], color=color, fill_opacity=1)
    feathers = VGroup(*[Line([-0.23 + d, -0.1, 0], [-0.48 + d, -tail, 0], color=color, stroke_width=7) for d in (-0.08, 0.08)])
    return VGroup(body, head, beak, feathers)


def fish(color):
    return VGroup(Ellipse(width=0.65, height=0.3, color=color, fill_opacity=0.9),
                  Polygon([-.28, 0, 0], [-.55, .22, 0], [-.55, -.22, 0], color=color, fill_opacity=0.9),
                  Dot([.2, .04, 0], radius=.035, color=BG))


def sun():
    return VGroup(Circle(radius=.3, color=RED, fill_opacity=.5),
                  *[Line(.42*np.array([np.cos(a), np.sin(a), 0]), .63*np.array([np.cos(a), np.sin(a), 0]), color=RED) for a in np.arange(0, TAU, TAU/8)])


def beak(deep=True):
    h = .46 if deep else .17
    return Polygon([-.45, h, 0], [.55, 0, 0], [-.45, -h, 0], color=DARK_C if deep else BLUE, fill_opacity=.85)


class S00Title(TitleCard):
    LESSON = "Natural selection in ecological context"
    TITLE = "Selection Has an Agent"


class S01Lead(SpokenScene):
    def construct(self):
        row = VGroup(*[moth(c).move_to([x, .9, 0]) for x,c in zip((-4.5,-1.5,1.5,4.5), (PALE_C,DARK_C,PALE_C,DARK_C))])
        head = T("Existing variation", 36).move_to([0, 3, 0])
        self.at("Natural selection starts")
        self.play(FadeIn(head), FadeIn(row), run_time=.8)
        agent = bird().move_to([0, 2.1, 0])
        self.at("a predator")
        self.play(FadeIn(agent), run_time=.5)
        self.at("a parasite")
        self.play(Transform(agent, chip("parasite", RED).move_to(agent)), run_time=.45)
        self.at("a rival")
        self.play(Transform(agent, chip("rival", RED).move_to(agent)), run_time=.45)
        self.at("a choosy mate")
        self.play(Transform(agent, chip("choosy mate", RED).move_to(agent)), run_time=.45)
        self.at("a drought")
        self.play(Transform(agent, sun().move_to(agent)), run_time=.45)
        young = VGroup(moth(PALE_C,.65).move_to([-3,-.8,0]),
                       moth(DARK_C,.65).move_to([0,-.8,0]), moth(DARK_C,.65).move_to([2,-.8,0]))
        self.at("leave more offspring")
        self.play(TransformFromCopy(row[0],young[0]), TransformFromCopy(row[1],young[1]), TransformFromCopy(row[3],young[2]), run_time=1)
        strip = chip("selection: one generation", YELLOW, 28).move_to([0,-2.25,0])
        self.at("That difference")
        self.play(FadeIn(strip), run_time=.7)
        inherit = chip("response: needs inheritance", TEAL, 28).move_to([0,-3.1,0])
        self.at("only if the variation")
        self.play(FadeIn(inherit), run_time=.7)
        self.at("the young of the survivors")
        self.play(Indicate(young, color=TEAL), run_time=.7)
        self.at("if the environment changes")
        self.play(Transform(agent, bird().move_to(agent)), FadeOut(young), run_time=.7)
        self.at("a different variant can win")
        self.play(row[0].animate.scale(1.3), row[2].animate.scale(1.3), row[1].animate.set_opacity(.35), row[3].animate.set_opacity(.35), run_time=.8)
        self.finish()


class S02Agent(SpokenScene):
    def construct(self):
        moths = VGroup(moth(PALE_C).move_to([-2,0,0]), moth(DARK_C).move_to([2,0,0]))
        labels = VGroup(T("pale",28,PALE_C).move_to([-2,-1,0]), T("dark",28,DARK_C).move_to([2,-1,0]))
        head=T("Peppered moth",36).move_to([0,3,0])
        self.at("Take the")
        self.play(FadeIn(head), FadeIn(moths), run_time=.7)
        self.at("a pale form")
        self.play(FadeIn(labels), run_time=.6)
        inherited=chip("inherited colour",TEAL,26).move_to([0,-2.5,0])
        self.at("the color is inherited")
        self.play(FadeIn(inherited), run_time=.6)
        trunks=VGroup(*[RoundedRectangle(width=4,height=3.6,corner_radius=.2,stroke_color=GREY,fill_color=c,fill_opacity=.8).move_to([x,0,0]) for x,c in ((-3.3,'#3A2A20'),(3.3,'#B9B79B'))])
        pair=VGroup(moth(PALE_C,.85).move_to([-4.2,0,0]),moth(DARK_C,.85).move_to([-2.4,0,0]),moth(PALE_C,.85).move_to([2.4,0,0]),moth(DARK_C,.85).move_to([4.2,0,0]))
        birds=VGroup(bird().move_to([-3.3,2.4,0]),bird().move_to([3.3,2.4,0]))
        self.at("Birds hunt")
        self.play(FadeOut(moths),FadeOut(labels),FadeOut(inherited),FadeIn(trunks),FadeIn(pair),FadeIn(birds),run_time=.9)
        barklabels=VGroup(T("sooty bark",28,GREY).move_to([-3.3,-2.3,0]),T("lichen-covered bark",28,GREY).move_to([3.3,-2.3,0]))
        self.at("Where pollution killed")
        self.play(FadeIn(barklabels),run_time=.6)
        self.at("dark moths matched")
        self.play(birds[0].animate.move_to(pair[0]),run_time=.6)
        self.play(FadeOut(pair[0]), birds[0].animate.move_to([-3.3,2.4,0]),run_time=.6)
        self.at("the dark form became common")
        self.play(Indicate(pair[1],color=YELLOW,scale_factor=1.3),run_time=.8)
        self.at("When the air cleaned up")
        self.play(birds[1].animate.move_to(pair[3]),run_time=.6)
        self.play(FadeOut(pair[3]),birds[1].animate.move_to([3.3,2.4,0]),run_time=.6)
        self.at("pale moths matched better")
        self.play(Indicate(pair[2],color=YELLOW,scale_factor=1.3),run_time=.8)
        self.at("Same moth same birds")
        self.play(Indicate(birds),run_time=.6)
        self.at("A different environment")
        rule=T("Environment changes which colour is favoured",30,TEAL).move_to([0,-3.2,0])
        self.play(FadeIn(rule),run_time=.7)
        self.finish()


class S03Measured(SpokenScene):
    def construct(self):
        # A location schematic, without a geographic scale.
        site=VGroup(Polygon([-.5,1.7,0],[.15,1.5,0],[-.05,.9,0],[.4,.5,0],[.55,-.1,0],[.95,-.6,0],[.55,-1.15,0],[-.2,-1.3,0],[-1,-1.5,0],[-.5,-.9,0],[-.8,-.4,0],[-.35,.05,0],[-.65,.7,0],color=GREY,fill_opacity=.12),Dot([.55,-.8,0],color=YELLOW),T("near Cambridge",28).move_to([0,-2,0])).move_to([-3.7,.7,0])
        ms=VGroup(moth(PALE_C).move_to([2,.9,0]),moth(DARK_C).move_to([4,.9,0]))
        self.at("How do you show it")
        self.play(FadeIn(site),run_time=.7)
        self.at("released live moths")
        self.play(FadeIn(ms,shift=LEFT),run_time=.8)
        years=chip("six years of releases",GREY,26).move_to([0,3,0])
        self.at("over six years")
        self.play(FadeIn(years),run_time=.6)
        agent=bird().move_to([3,2.3,0])
        missing=T("disappeared → presumed eaten",26,GREY).move_to([0,-1.8,0])
        self.at("recorded which disappeared")
        self.play(ms[1].animate.set_opacity(.2),FadeIn(agent),FadeIn(missing),run_time=.8)
        records=T("Cook and colleagues: analysis",28,GREY).move_to([0,-2.7,0])
        self.at("Cook and colleagues")
        self.play(FadeIn(records),run_time=.6)
        self.at("Each day")
        self.play(FadeOut(site),FadeOut(ms),FadeOut(years),FadeOut(agent),FadeOut(missing),FadeOut(records),run_time=.5)
        eq=chip("dark survival = 0.91 × pale",YELLOW,34).move_to([0,1.6,0])
        self.at("a dark moth survived")
        self.play(FadeIn(eq),run_time=.8)
        limits=T("relative • per day • one site",30,YELLOW).move_to([0,.2,0])
        self.at("That number is relative")
        self.play(FadeIn(limits),run_time=.7)
        component=chip("fitness component: survival",TEAL,28).move_to([0,-1.2,0])
        self.at("a measured fitness component")
        self.play(FadeIn(component),run_time=.7)
        tag=chip("agent: birds",RED,28).move_to([0,-2.5,0])
        self.at("with a named agent")
        self.play(FadeIn(tag),run_time=.7)
        self.finish()


class S04Modes(SpokenScene):
    def construct(self):
        ax=Axes(x_range=[0,1,.5],y_range=[0,1,.5],x_length=9,y_length=3.5,axis_config={"color":GREY,"include_ticks":False,"include_tip":False}).move_to([0,-.1,0])
        xlabel=T("trait: gall size",28,GREY).move_to([0,-2.6,0])
        ylabel=T("survival",28,TEAL).move_to([-5.1,2.55,0])
        title=T("Selection has a shape",36).move_to([0,3.2,0])
        self.at("Selection also")
        self.play(FadeIn(title),run_time=.6)
        self.at("Plot fitness")
        self.play(Create(ax),FadeIn(xlabel),FadeIn(ylabel),run_time=.8)
        curve=ax.plot(lambda x:.2+.65*np.sin(np.pi*x),x_range=[0,1],color=TEAL)
        wasp=VGroup(Ellipse(width=.6,height=.22,color=RED,fill_opacity=.8),
                    Ellipse(width=.35,height=.18,color=RED).shift(UP*.2),
                    Line([-.2,0,0],[-.4,-.4,0],color=RED),
                    T("wasps",26,RED).shift(RIGHT*1)).move_to([-3.2,2,0])
        birdtag=VGroup(bird().scale(.8),T("birds",26,RED).shift(RIGHT*1.1)).move_to([3.3,2,0])
        self.at("Wasps take")
        self.play(FadeIn(wasp),run_time=.6)
        self.at("birds open")
        self.play(FadeIn(birdtag),run_time=.6)
        self.at("galls survive best")
        self.play(Create(curve),run_time=.8)
        mode=T("Stabilizing selection",30,TEAL).move_to([0,-3.3,0])
        self.at("That is stabilizing")
        self.play(FadeIn(mode),run_time=.7)
        self.at("In crowded lake enclosures")
        newtitle=T("Sticklebacks in lake enclosures",34).move_to(title)
        self.play(Transform(title,newtitle),FadeOut(wasp),FadeOut(birdtag),FadeOut(curve),FadeOut(mode),Transform(xlabel,T("trait",28,GREY).move_to(xlabel)),Transform(ylabel,T("fitness proxy",26,TEAL).move_to(ylabel)),run_time=.7)
        dip=ax.plot(lambda x:.4+.35*(2*x-1)**2,x_range=[0,1],color=TEAL)
        self.at("at either extreme")
        self.play(Create(dip),run_time=.8)
        proxy=T("Stand-ins for reproductive success",26,GREY).move_to([0,2.25,0])
        self.at("on stand")
        self.play(FadeIn(proxy),run_time=.6)
        mode2=T("Disruptive selection",30,TEAL).move_to([0,-3.3,0])
        self.at("That is disruptive")
        self.play(FadeIn(mode2),run_time=.6)
        high=ax.plot(lambda x:.12+.63*(2*x-1)**2,x_range=[0,1],color=TEAL)
        crowd=T("More crowding → deeper dip",28,TEAL).move_to([0,1.5,0])
        self.at("crowding made it stronger")
        self.play(Transform(dip,high),FadeIn(crowd),run_time=.8)
        self.finish()


class S05RareMates(SpokenScene):
    def construct(self):
        title=T("Success depends on frequency",34).move_to([0,3,0])
        self.at("Sometimes the winner")
        self.play(FadeIn(title),run_time=.7)
        pools=VGroup(); fishes=[]
        for x,colors in ((-3.3,[PALE_C]*3+[DARK_C]),(3.3,[DARK_C]*3+[PALE_C])):
            pool=Ellipse(width=5.2,height=3.5,color=BLUE,fill_opacity=.08).move_to([x,0,0])
            group=VGroup(*[fish(c).move_to([x+dx,y,0]) for c,(dx,y) in zip(colors,[(-1,.6),(1,.6),(-1,-.6),(1,-.6)])])
            pools.add(VGroup(pool,group)); fishes.append(group)
        self.at("In Trinidad streams")
        self.play(FadeIn(pools),run_time=.8)
        rings=VGroup(*[Circle(radius=.62,color=YELLOW).move_to(g[3]) for g in fishes])
        self.at("rare in some pools")
        self.play(Create(rings),run_time=.7)
        result=T("Rare pattern: better estimated survival",28,TEAL).move_to([0,-2.65,0])
        self.at("Whichever pattern was rare")
        self.play(FadeIn(result),run_time=.7)
        self.at("selection can act through mating")
        self.play(FadeOut(pools),FadeOut(rings),FadeOut(result),Transform(title,T("Selection through mating",34).move_to(title)),run_time=.7)
        birds=VGroup(*[bird(tail=t,color=GREY).move_to([x,1,0]) for x,t in zip((-4,0,4),(.55,1.1,1.8))])
        labels=VGroup(*[T(t,26,GREY).move_to([x,-1.25,0]) for x,t in zip((-4,0,4),("shortened","normal","lengthened"))])
        self.at("shortened and lengthened")
        self.play(FadeIn(birds),FadeIn(labels),run_time=.9)
        # Schematic counts communicate direction, not the experiment's effect size.
        def nest():
            return VGroup(Arc(radius=.24,start_angle=PI,angle=PI,color=TEAL),
                          Ellipse(width=.13,height=.19,color=PALE_C,fill_opacity=.8).shift(DOWN*.06))
        nests=VGroup(*[VGroup(*[nest() for _ in range(n)]).arrange(RIGHT,buff=.16).move_to([x,-2.3,0]) for x,n in zip((-4,0,4),(1,2,3))])
        arrow=Arrow([-3.7,-3.05,0],[4.3,-3.05,0],color=TEAL,buff=0)
        note=T("More females nesting (schematic counts)",24,TEAL).move_to([0,-3.5,0])
        self.at("Males given longer tails")
        self.play(Indicate(birds[2],color=TEAL),run_time=.6)
        self.at("attracted more females")
        self.play(FadeIn(nests),GrowArrow(arrow),FadeIn(note),run_time=.8)
        self.finish()


class S06Response(SpokenScene):
    def construct(self):
        title=T("Selection: within one generation",34,YELLOW).move_to([0,3,0])
        shapes=VGroup(*[beak(d).move_to([x,1.6,0]) for x,d in zip((-4,-1.4,1.4,4),(False,True,False,True))])
        self.at("Each of these studies")
        self.play(FadeIn(title),FadeIn(shapes),run_time=.8)
        arrow=Arrow([0,-.4,0],[0,-1.7,0],color=TEAL,buff=0)
        gate=chip("only if inherited",TEAL,28).move_to([3,-1,0])
        self.at("the trait must be inherited")
        self.play(GrowArrow(arrow),FadeIn(gate),run_time=.7)
        young=VGroup(beak(True).scale(.75).move_to([-1,-2.5,0]),beak(True).scale(.75).move_to([1,-2.5,0]))
        self.at("the next generation")
        self.play(TransformFromCopy(shapes[1],young[0]),TransformFromCopy(shapes[3],young[1]),run_time=.8)
        drought=sun().move_to([-5.4,.2,0])
        sieve=VGroup(Line([-4.8,.5,0],[4.8,.5,0],color=GREY),*[Line([x,.5,0],[x,.1,0],color=GREY) for x in np.arange(-4.8,5,.6)])
        self.at("A drought does not create")
        self.play(FadeIn(drought),Create(sieve),run_time=.7)
        self.at("It removes more")
        self.play(shapes[0].animate.shift(DOWN*1.3).set_opacity(0),shapes[2].animate.shift(DOWN*1.3).set_opacity(0),shapes[1].animate.shift(DOWN*.6),shapes[3].animate.shift(DOWN*.6),run_time=.9)
        self.at("Selection sorts")
        self.play(Indicate(VGroup(shapes[1],shapes[3]),color=YELLOW),run_time=.7)
        self.at("inheritance carries")
        self.play(Indicate(arrow,color=TEAL),Indicate(young,color=TEAL),run_time=.7)
        self.finish()


class S07End(EndCard):
    LINE = "Selection sorts existing variation; inheritance carries the sorting forward."
