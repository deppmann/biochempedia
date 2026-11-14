"""Why Growth Bends — one creek world and one computed model.

COLOR MAP
  TEAL = crab population and population curves
  GOLD = food and carrying capacity
  GREEN = shelter
  RED = living challenges
  COLD = cold water / nonliving challenge
  GREY = axes and supporting structure
"""
from bp_parts import *

ORANGE = "#F29E4C"
COLD = "#86CFE8"
CRAB = TEAL
K = 100.0
R = 0.72
N0 = 5.0


def exponential(t):
    """Made-up stated rule: N starts at 5 and multiplies by 1.55 each step."""
    return N0 * 1.55 ** t


def logistic(t):
    """Lesson equation dN/dt=rN(1-N/K), evaluated in closed form."""
    return K / (1 + (K / N0 - 1) * np.exp(-R * t))


def crab(scale=1.0, color=CRAB):
    body = Ellipse(width=0.62, height=0.35, stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.3)
    eyes = VGroup(Dot([-0.14, 0.16, 0], 0.035, color=color),
                  Dot([0.14, 0.16, 0], 0.035, color=color))
    legs = VGroup(*[Line([sx * .22, -.08, 0], [sx * (.42 + .08*i), -.25 + .04*i, 0],
                               color=color, stroke_width=2)
                    for sx in (-1, 1) for i in range(3)])
    claws = VGroup(Arc(radius=.12, start_angle=0, angle=PI, color=color).shift(LEFT*.42+UP*.08),
                   Arc(radius=.12, start_angle=0, angle=PI, color=color).shift(RIGHT*.42+UP*.08))
    return VGroup(legs, claws, body, eyes).scale(scale)


def creek_world(compact=False, crowded=False, cold=False):
    """The carried creek picture; all creek scenes call this builder."""
    left, right = (-6.25, -0.35) if compact else (-6.45, 6.45)
    width = right-left
    water = Rectangle(width=width, height=5.45, stroke_width=0,
                      fill_color="#12394A", fill_opacity=.72).move_to([(left+right)/2, .15, 0])
    sand = Polygon([left,-2.35,0], [right,-2.35,0], [right,-3.1,0], [left,-3.1,0],
                   fill_color="#8A6E45", fill_opacity=.72, stroke_width=0)
    waves = VGroup(*[ArcBetweenPoints([left+.25, y, 0], [right-.25, y, 0], angle=.035,
                                      color=COLD, stroke_width=2).set_opacity(.22)
                     for y in (-1.5, -.55, .45, 1.45, 2.35)])
    # Grass is shelter, drawn as blades rooted in the same sandy bottom.
    grass = VGroup(*[CubicBezier([x,-2.35,0], [x-.18,-1.85,0], [x+.18,-1.35,0], [x+.06,-.8,0])
                     .set_stroke(GREEN, 5) for x in np.linspace(left+.55, left+1.8, 6)])
    food = VGroup(*[Dot([left+2.0+(i%4)*.62, -1.75+(i//4)*.45, 0], .07, color=GOLD)
                    for i in range(8)])
    if compact:
        base = [[left+2.0,-.65,0], [left+3.05,.1,0], [left+4.05,-.9,0], [left+4.9,.4,0]]
    elif crowded:
        base = [[-.9,-.65,0], [-.25,-.25,0], [.35,-.72,0], [.85,-.2,0], [1.35,-.78,0], [1.85,-.25,0], [2.35,-.7,0]]
    else:
        base = [[-3.4,-.55,0], [-1.9,.15,0], [-.2,-.75,0], [1.55,.05,0], [3.15,-.65,0]]
    crabs = VGroup(*[crab(.78).move_to(p) for p in base])
    cold_band = Rectangle(width=.55, height=5.45, stroke_width=0, fill_color=COLD,
                          fill_opacity=.35).move_to([right-.275,.15,0]) if cold else VGroup()
    world = VGroup(water, waves, sand, grass, food, crabs, cold_band)
    world.water, world.waves, world.sand = water, waves, sand
    world.grass, world.food, world.crabs, world.cold = grass, food, crabs, cold_band
    return world


def animate_creek(world):
    for i, c in enumerate(world.crabs):
        bob(c, amp=.13, speed=1.2+.12*i, seed=i)
    for i, blade in enumerate(world.grass):
        pulse(blade, base=4.5, amp=.8, speed=1.0+.08*i)
    for i, wave in enumerate(world.waves):
        pulse(wave, base=3.0, amp=2.0, speed=1.1+.09*i)


def shimmer(curve, speed=1.4):
    """Continuous motion for a curve while the curve itself is the subject."""
    curve._shimmer_t = 0.0
    def update(mob, dt):
        mob._shimmer_t += dt
        mob.set_stroke(width=6.5 + 2.5*np.sin(speed*mob._shimmer_t),
                       opacity=.78 + .2*np.sin(speed*mob._shimmer_t+.7))
    curve.add_updater(update)
    return curve


def runner(P, fn, x1=10.0, period=3.6, color=GOLD):
    """Ambient motion: a sweeping marker with a drop line and a glow ring travels along a curve."""
    g = VGroup(Line(ORIGIN, UP, stroke_width=5, color=color), Dot(radius=.17, color=color), Circle(.34, color=color, stroke_width=4))
    g._rt = 0.0
    def upd(m, dt):
        m._rt += dt
        f = (m._rt % period) / period
        x = (x1() if callable(x1) else x1) * f
        top = P.pt(x, fn(x)); base = P.pt(x, 0)
        m[0].put_start_and_end_on(base, top)
        m[1].move_to(top)
        m[2].move_to(top).scale_to_fit_width(.5 + .3*np.sin(6*m._rt))
    g.add_updater(upd)
    for o in g: o.layout_ok = True
    g.layout_ok = True
    return g

def growth_plot(box=(-.05, 6.15, -2.15, 2.45)):
    return Plot(box=box, xr=(0, 10), yr=(0, 115), xticks=[0,5,10],
                yticks=[(0,"0"),(50,"50"),(100,"100")], xlabel="time", ylabel="population size")


def model_plot():
    return growth_plot(box=(-5.75, 5.55, -2.35, 2.55))


def predict_backdrop():
    w = creek_world(compact=True)
    P = growth_plot()
    curve = shimmer(P.curve(exponential, x0=0, x1=6.8, color=CRAB))
    animate_creek(w)
    return VGroup(w, P, curve)


class S01Hook(SpokenScene):
    def construct(self):
        w = creek_world()
        animate_creek(w)
        q = fit_text("Why does fast growth bend?", 10.5, 42, GOLD).move_to([0,3.25,0])
        self.at("Why does fast population")
        self.play(FadeIn(w), FadeIn(q, shift=DOWN*.12), run_time=1.0)
        self.at("Watch a Chesapeake creek")
        corner = T("Why does growth bend?", 28, GOLD).move_to([-4.55,3.25,0])
        self.play(ReplacementTransform(q, corner), run_time=.7)
        self.at("The water keeps moving")
        self.play(LaggedStart(*[Indicate(x, scale_factor=1.0, color=COLD) for x in w.waves], lag_ratio=.08), run_time=1.5)
        self.at("food and hiding places")
        self.play(Indicate(w.food, color=GOLD, scale_factor=1.08), Indicate(w.grass, color=GREEN, scale_factor=1.04), run_time=1.1)
        predator = Arrow([6.0,1.6,0],[4.7,.8,0], color=RED, stroke_width=6)
        disease = Circle(.45, color=RED, stroke_width=5).move_to([-1.2,.0,0]).set_opacity(.75)
        self.at("Predators and disease")
        self.play(GrowArrow(predator), Create(disease), run_time=.8)
        n = ValueTracker(5)
        track = Readout([("population", lambda:n.get_value(), "{:2.0f}", CRAB)], at=[4.05,2.55,0], widest=[12])
        self.at("Something in this picture")
        self.play(FadeIn(track), n.animate.set_value(9), run_time=1.8)
        self.play(FadeIn(scope_tag("schematic")), run_time=.3)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Carrying Capacity"
    TITLE = "Why Growth Bends"


class S03Population(SpokenScene):
    def construct(self):
        w = creek_world(cold=True)
        animate_creek(w)
        boundary = RoundedRectangle(width=6.0, height=2.25, corner_radius=.25, color=CRAB,
                                    stroke_width=4).move_to([.3,-.25,0])
        poplab = T("population", 30, CRAB).next_to(boundary, UP, buff=.12)
        self.at("A population is all")
        self.play(FadeIn(w), Create(boundary), run_time=.9)
        self.play(FadeIn(poplab), run_time=.45)
        self.at("Teal crab symbols")
        self.play(*[c.animate.move_to([-.9+(i%3)*.65,-.55+(i//3)*.65,0]) for i,c in enumerate(w.crabs)], run_time=1.1)
        self.at("Gold food and green shelter")
        self.play(w.food.animate.shift(RIGHT*1.2+UP*.25), w.grass.animate.shift(RIGHT*1.0), run_time=1.0)
        predator = Arrow([5.5,1.5,0],[3.5,.65,0], color=RED, stroke_width=6)
        disease = Circle(.42,color=RED,stroke_width=5).move_to([2.35,-.25,0])
        self.at("Red arrows show")
        self.play(GrowArrow(predator), Create(disease), run_time=.8)
        self.at("A pale blue band")
        self.play(Indicate(w.cold, color=COLD, scale_factor=1.0), run_time=1.0)
        legend = VGroup(T("population",24,CRAB),T("food",24,GOLD),T("shelter",24,GREEN),
                        T("living challenges",24,RED),T("cold water",24,COLD)).arrange(DOWN,aligned_edge=LEFT,buff=.12).move_to([-4.9,1.55,0])
        # This is deliberately a legend printed over its own dim water panel.
        for item in legend:
            item.layout_ok = True
        self.at("Together these living")
        self.play(FadeOut(poplab), FadeIn(legend, shift=RIGHT*.15), run_time=1.1)
        self.finish()


class S04Exponential(SpokenScene):
    def construct(self):
        w = creek_world(compact=True)
        animate_creek(w)
        P = growth_plot()
        t = ValueTracker(0)
        live = P.live_curve(exponential,t,color=CRAB)
        dot = P.dot(lambda:t.get_value(),lambda:exponential(t.get_value()),color=TEXT,ring=CRAB)
        rule = T("N × 1.55 each step", 26, CRAB).move_to([3.1,3.15,0])
        self.at("Start with a small population")
        self.play(FadeIn(w), Create(P), run_time=1.0)
        self.at("same fraction each step")
        self.play(FadeIn(rule), run_time=.55)
        self.add(live,dot)
        self.add(runner(P,exponential,x1=lambda:max(t.get_value(),.3)))
        self.at("so the number added grows")
        self.play(t.animate.set_value(4.2), run_time=2.0, rate_func=linear)
        label = T("exponential growth",30,CRAB).move_to([4.25,2.85,0])
        self.at("That pattern is exponential")
        self.play(ReplacementTransform(rule,label), run_time=.6)
        self.at("bends upward like")
        self.play(t.animate.set_value(6.8), run_time=2.5, rate_func=linear)
        self.at("This model is schematic")
        self.play(FadeIn(scope_tag("computed model · schematic")), run_time=.5)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        self.add(back)
        self.at("Now predict")
        q = question_card("What makes the curve bend?", ["resources gone", "limits strengthen sooner"], chips_at=[3.6,.15,0])
        for item in q.chips:
            item.layout_ok = True  # answer text belongs inside its choice path
        self.play(FadeIn(q.question), run_time=.55)
        self.at("Must the food")
        self.play(FadeIn(q.chips[0], shift=LEFT*.15), run_time=.55)
        self.at("Or can crowding")
        self.play(FadeIn(q.chips[1], shift=LEFT*.15), run_time=.55)
        self.at("Keep your answer")
        self.play(Indicate(q.question,color=GOLD,scale_factor=1.02), run_time=.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "What makes the curve bend?"
    OPTIONS = ["resources gone", "limits strengthen sooner"]
    CHIPS_AT = [3.6,.15,0]
    SECONDS = 4.5
    def backdrop(self):
        return predict_backdrop()

    def construct(self):
        self.add(self.backdrop())
        q = question_card(self.QUESTION, self.OPTIONS, chips_at=self.CHIPS_AT)
        for item in q.chips:
            item.layout_ok = True
        self.add(q)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S07Crowding(SpokenScene):
    def construct(self):
        w = creek_world(crowded=True)
        animate_creek(w)
        self.at("Crowding means more crabs")
        self.play(FadeIn(w), run_time=.9)
        target = w.food[3].get_center()
        self.at("Competition grows")
        self.play(w.crabs[2].animate.move_to(target+LEFT*.25), w.crabs[3].animate.move_to(target+RIGHT*.25), run_time=1.0)
        ring = Circle(.2,color=RED,stroke_width=5).move_to(w.crabs[2])
        self.at("Disease may spread")
        self.play(Create(ring), ring.animate.scale(4.0).move_to(w.crabs[4]).set_opacity(0), run_time=1.4)
        pred = Arrow([6.1,1.35,0],[1.8,.1,0],color=RED,stroke_width=7)
        self.at("predators may find")
        self.play(GrowArrow(pred), run_time=1.0)
        young = crab(.42).move_to([-.1,1.25,0])
        self.at("Fewer young survive")
        self.play(FadeIn(young), FadeOut(young,shift=DOWN*.2), run_time=1.1)
        n = ValueTracker(7)
        ro = Readout([("population",lambda:n.get_value(),"{:4.1f}",CRAB)],at=[3.95,2.5,0],widest=[12])
        self.at("The population can still grow")
        self.play(FadeIn(ro), n.animate.set_value(9), run_time=3.4, rate_func=linear)
        self.at("before every resource disappears")
        self.play(Indicate(VGroup(w.food,w.grass),scale_factor=1.02), run_time=.8)
        self.finish()


class S08Capacity(SpokenScene):
    def construct(self):
        P = model_plot()
        j = P.curve(exponential,x0=0,x1=6.8,color=CRAB)
        s = shimmer(P.curve(logistic,color=CRAB))
        self.at("In the simplest limited growth")
        self.play(Create(P), Create(j), run_time=1.1)
        self.at("turns the jay into")
        self.play(ReplacementTransform(j,s), run_time=2.1)
        self.at("approaches carrying capacity")
        k = P.hline(K,"carrying capacity",GOLD)
        self.add(runner(P,logistic,period=4.0))
        self.play(Create(k), run_time=1.0)
        definition = fit_text("Largest population this environment can support over time",10.8,28,GOLD).move_to([0,3.25,0])
        self.at("Carrying capacity is the largest")
        self.play(FadeIn(definition), run_time=.9)
        self.at("with its resources and challenges")
        self.play(Indicate(k,color=GOLD,scale_factor=1.0), run_time=.9)
        self.at("a level approached")
        self.play(FadeOut(definition), FadeIn(scope_tag("computed model")), run_time=.7)
        self.finish()


class S09ReadCurve(SpokenScene):
    def construct(self):
        P = model_plot(); curve=shimmer(P.curve(logistic,color=CRAB)); k=P.hline(K,"carrying capacity",GOLD)
        t=ValueTracker(0); dot=P.dot(lambda:t.get_value(),lambda:logistic(t.get_value()),color=TEXT,ring=CRAB)
        self.add(runner(P,logistic,period=4.5))
        self.at("Read the ess shaped")
        self.play(Create(P),Create(curve),Create(k),FadeIn(dot),run_time=1.0)
        initial=T("initial",28,CRAB).move_to([-2.6,3.15,0])
        self.at("Growth starts slowly")
        self.play(FadeIn(initial),t.animate.set_value(2.5),run_time=2.5,rate_func=linear)
        faster=T("faster",28,CRAB).move_to([0,3.15,0])
        self.at("Then numbers rise faster")
        self.play(FadeOut(initial),FadeIn(faster),t.animate.set_value(6.0),run_time=3.0,rate_func=linear)
        slowing=T("slowing",28,CRAB).move_to([4.2,3.15,0])
        self.at("Finally growth slows")
        self.play(FadeOut(faster),FadeIn(slowing),t.animate.set_value(10),run_time=3.0,rate_func=linear)
        births=T("births  ≈  deaths",32,TEXT).move_to([0,3.15,0])
        self.at("births and deaths")
        self.play(FadeIn(births),run_time=.7)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        P=model_plot(); model=shimmer(P.curve(logistic,color=CRAB)); k=P.hline(K,None,GOLD)
        klab=T("carrying capacity",26,GOLD).move_to([4.55,3.15,0])
        self.at("The computed line")
        self.play(Create(P),Create(model),Create(k),FadeIn(klab),run_time=1.0)
        self.add(runner(P,logistic,period=4.0))
        real=lambda t: logistic(t)+(4.0*np.sin(2.3*t) if t>6 else 0)
        self.at("In real populations")
        rcurve=P.curve(real,color=TEXT,width=3,opacity=.55)
        self.play(Create(rcurve),FadeOut(klab),run_time=2.0)
        rlab=T("real population · schematic",24,TEXT).move_to([2.6,2.5,0]).set_opacity(.7)
        self.at("size can move up and down")
        self.play(FadeIn(rlab),Indicate(rcurve,scale_factor=1.0),run_time=1.2)
        eq=fit_text("dynamic equilibrium = balance kept by ongoing change",8.6,28,CRAB).move_to([1.0,3.3,0])
        self.at("That balance kept")
        self.play(FadeIn(eq),run_time=.8)
        self.at("Real populations may also")
        over=P.curve(lambda t: logistic(t)+(18*np.exp(-.5*(t-7)) if t>7 else 0),x0=6.8,color=RED,width=3,opacity=.35)
        decline=P.curve(lambda t: logistic(t)-(11*(t-7) if t>7 else 0),x0=6.8,color=GREEN,width=3,opacity=.35)
        wobble=P.curve(real,x0=6.8,color=COLD,width=3,opacity=.35)
        labs=VGroup(T("overshoot · schematic",24,RED),T("decline · schematic",24,GREEN),T("wobble · schematic",24,COLD)).arrange(DOWN,aligned_edge=LEFT,buff=.12).move_to([-3.9,.75,0])
        self.play(FadeOut(eq),Create(over),run_time=.7)
        self.play(Create(decline),run_time=.7)
        self.play(Create(wobble),FadeIn(labs),run_time=.7)
        self.at("useful model")
        self.play(FadeOut(VGroup(over,decline,wobble,labs,rcurve,rlab)),Indicate(model,color=CRAB,scale_factor=1.0),run_time=1.1)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        w=creek_world(crowded=True); animate_creek(w)
        n=ValueTracker(7); ro=Readout([("population",lambda:n.get_value(),"{:4.1f}",CRAB)],at=[3.9,2.75,0],widest=[12])
        kline=DashedLine([-5.5,2.35,0],[3.2,2.35,0],color=GOLD,stroke_width=3)
        self.at("Return to the creek")
        self.play(FadeIn(w),FadeIn(ro),Create(kline),run_time=1.0)
        self.at("More crabs made")
        share=VGroup(*[Arrow(p,p+DOWN*.55,color=GOLD,stroke_width=3,buff=.05) for p in ([-1.0,1.2,0],[0,1.2,0],[1,1.2,0])])
        self.play(FadeIn(share),run_time=.8)
        self.at("several challenges grew stronger")
        reds=VGroup(Circle(.42,color=RED).move_to([.2,-.3,0]),Arrow([5.7,1.3,0],[2.1,.1,0],color=RED,stroke_width=7))
        self.play(Create(reds),run_time=1.0)
        self.at("Those limits reduced growth")
        self.play(n.animate.set_value(8.4),run_time=3.2,rate_func=linear)
        self.at("That is why")
        bend=ArcBetweenPoints([-2.6,2.65,0],[1.2,2.4,0],angle=-.8,color=CRAB,stroke_width=7)
        self.play(Create(bend),run_time=.9)
        self.at("whether the support level")
        self.play(Indicate(kline,color=GOLD,scale_factor=1.0),run_time=.8)
        self.finish()


class S12End(EndCard):
    LINE = "Limits slow population growth near carrying capacity."
