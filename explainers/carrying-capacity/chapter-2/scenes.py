"""Did the Limit Move? — carrying capacity, chapter 2.

COLOR MAP (kept from chapter 1 and the chapter-2 script)
  TEAL   population size and crab cartoons
  GOLD   carrying capacity, food, and the central question
  GREEN  shelter / marsh habitat
  RED    lasting loss and unresolved causes
  GREY   water, structure, axes, and neutral labels

The creek and paired gauge are rebuilt only through the builders below, so their
landmarks remain fixed whenever the film returns to them. All plotted population
paths are computed logistic-model curves in schematic units.
"""
from bp_parts import *

CRAB = TEAL
CAPACITY = GOLD
SHELTER = GREEN
CHALLENGE = RED


def crab(scale=1.0):
    """A labelled-cartoon-free crab silhouette, not a count."""
    body = Ellipse(width=0.55, height=0.34, color=CRAB, stroke_width=3,
                   fill_color=CRAB, fill_opacity=0.35)
    claws = VGroup(Arc(radius=0.16, start_angle=0.2, angle=2.5, color=CRAB),
                   Arc(radius=0.16, start_angle=0.45, angle=2.5, color=CRAB))
    claws[0].move_to([-0.38, 0.10, 0]); claws[1].move_to([0.38, 0.10, 0])
    legs = VGroup(*[Line([sx * 0.18, -0.12, 0], [sx * (0.32 + 0.08*i), -0.27, 0],
                               color=CRAB, stroke_width=2)
                    for sx in (-1, 1) for i in range(2)])
    return VGroup(legs, claws, body).scale(scale)


def grass_clump(scale=1.0):
    blades = VGroup(*[ArcBetweenPoints([x, 0, 0], [x + bend, 0.85 + 0.08*i, 0],
                                      angle=(-0.25 if bend < 0 else 0.25), color=SHELTER,
                                      stroke_width=7)
                      for i, (x, bend) in enumerate([(-0.28, -0.18), (-0.12, 0.05),
                                                     (0.05, -0.05), (0.22, 0.18)])])
    return blades.scale(scale)


def creek_world(center=(-1.65, 0.0, 0), width=8.7, height=5.1, crabs=5,
                shelter="full", cold=False, built=False):
    """The carried creek picture. Attributes expose only objects scenes animate."""
    c = np.array(center, dtype=float)
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.35,
                             stroke_color=GREY, stroke_width=3,
                             fill_color="#173543", fill_opacity=0.55).move_to(c)
    shore_y = c[1] - height * 0.22
    mud = Rectangle(width=width - 0.10, height=height * 0.27, stroke_width=0,
                    fill_color="#574532", fill_opacity=0.75).move_to([c[0], c[1]-height*0.355, 0])
    water = VGroup(*[Line([c[0]-width*0.44, c[1]+0.75-i*0.52, 0],
                          [c[0]+width*0.44, c[1]+0.75-i*0.52, 0],
                          color=GREY, stroke_width=2).set_opacity(0.32)
                     for i in range(4)])
    grasses = VGroup()
    if shelter == "full":
        xs = (-0.37, -0.13, 0.13, 0.37)
    elif shelter == "low":
        xs = (-0.37, 0.37)
    else:
        xs = ()
    for i, fx in enumerate(xs):
        g = grass_clump(0.72).move_to([c[0] + fx*width, shore_y+0.18, 0])
        grasses.add(g)
    food = VGroup(*[Dot([c[0]-2.8+0.75*i, c[1]+1.55+0.12*(i%2), 0],
                              radius=0.075, color=CAPACITY) for i in range(8)])
    crab_group = VGroup()
    spots = [(-2.6,-1.25), (-1.35,-0.82), (0,-1.35), (1.25,-0.82), (2.55,-1.25)]
    for x, y in spots[:crabs]:
        crab_group.add(crab(0.82).move_to([c[0]+x*width/8.7, c[1]+y*height/5.1, 0]))
    extras = VGroup()
    if cold:
        wash = Rectangle(width=width-0.12, height=height-0.12, stroke_width=0,
                         fill_color="#C7E8F3", fill_opacity=0.13).move_to(c)
        def flake(x, y):
            return VGroup(Line([-0.11,0,0],[0.11,0,0],color="#DDF4FF",stroke_width=3),
                          Line([0,-0.11,0],[0,0.11,0],color="#DDF4FF",stroke_width=3)).move_to([x,y,0])
        flakes = VGroup(*[flake(c[0]-2.8+i*1.1, c[1]+1.25-0.25*(i%2)) for i in range(6)])
        extras.add(wash, flakes)
    if built:
        wall = Rectangle(width=width*0.48, height=0.58, color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.5).move_to([c[0]+width*0.22, shore_y+0.1, 0])
        extras.add(wall)
    world = VGroup(frame, mud, water, food, grasses, crab_group, extras)
    world.frame, world.water, world.food = frame, water, food
    world.grasses, world.crabs, world.extras = grasses, crab_group, extras
    return world


def animate_creek(world):
    """Subtle continuous current and grass motion; visible but not distracting."""
    for i, line in enumerate(world.water):
        bob(line, amp=0.045, speed=0.8 + 0.13*i, seed=i)
    for i, g in enumerate(world.grasses):
        bob(g, amp=0.035, speed=1.0 + 0.1*i, seed=i+2)
    for i, d in enumerate(world.food):
        bob(d, amp=0.08, speed=0.8 + 0.12*i, seed=i)
    # A broad, very faint shimmer keeps long explanatory beats visually alive.
    world.frame._shimmer_t = 0.0
    def shimmer(mob, dt):
        mob._shimmer_t += dt
        mob.set_fill(opacity=0.55 + 0.065*np.sin(1.8*mob._shimmer_t))
    world.frame.add_updater(shimmer)
    return world


def paired_gauge(pop=0.66, cap=0.82, center=(4.65, 0.0, 0), height=4.8,
                 labels=True):
    """One shared scale with independently moving teal and gold markers."""
    pop_t, cap_t = ValueTracker(pop), ValueTracker(cap)
    c = np.array(center, dtype=float)
    y0, y1 = c[1]-height/2, c[1]+height/2
    track = RoundedRectangle(width=2.6, height=height+0.35, corner_radius=0.18,
                             stroke_color=GREY, stroke_width=3, fill_color=GREY,
                             fill_opacity=0.035).move_to(c)
    track._glow_t = 0.0
    def gauge_glow(mob, dt):
        mob._glow_t += dt
        mob.set_fill(opacity=0.035 + 0.025*np.sin(1.7*mob._glow_t))
    track.add_updater(gauge_glow)
    scale = Line([c[0], y0, 0], [c[0], y1, 0], color=GREY, stroke_width=8)
    def mark(tr, color, side):
        return always_redraw(lambda: VGroup(
            Line([c[0]-0.66, y0+height*tr.get_value(), 0],
                 [c[0]+0.66, y0+height*tr.get_value(), 0], color=color, stroke_width=8),
            Triangle(color=color, fill_color=color, fill_opacity=1).scale(0.13).rotate(
                -PI/2 if side < 0 else PI/2).move_to(
                [c[0]+side*0.86, y0+height*tr.get_value(), 0])))
    pm, km = mark(pop_t, CRAB, -1), mark(cap_t, CAPACITY, 1)
    g = VGroup(track, scale, pm, km)
    if labels:
        pl = T("population now", 28, CRAB).rotate(PI/2).move_to([c[0]-1.72, c[1], 0])
        kl = T("supported over time", 28, CAPACITY).rotate(-PI/2).move_to([c[0]+1.72, c[1], 0])
        g.add(pl, kl)
    g.pop_t, g.cap_t = pop_t, cap_t
    return g


def mini_case(center, crabs=3, shelter="full", cold=False):
    return creek_world(center=center, width=5.7, height=3.7, crabs=crabs,
                       shelter=shelter, cold=cold)


R = 0.75
N0 = 1.0
def logistic(t, K):
    return K / (1 + (K/N0 - 1) * np.exp(-R*t))


class S01Hook(SpokenScene):
    def construct(self):
        world = animate_creek(creek_world(center=(-1.7, -0.2, 0), width=8.7, height=5.5))
        gauge = paired_gauge(center=(4.75, -0.2, 0), height=5.0)
        self.at("The first film")
        self.play(FadeIn(world), run_time=1.1)
        self.at("But when a crab count falls")
        question = fit_text("What moved — population, capacity, or both?", 11.8, 38,
                            color=CAPACITY).move_to([0, 3.35, 0])
        self.play(FadeIn(question), world.crabs[-1].animate.set_opacity(0),
                  world.crabs[-2].animate.set_opacity(0), run_time=1.3)
        self.at("Return to the same creek")
        self.play(FadeIn(gauge), run_time=1.0)
        self.at("follow a pair of trackers")
        self.play(gauge.pop_t.animate.set_value(0.48), run_time=2.0)
        self.at("teal for population size")
        self.play(Indicate(gauge[2], color=CRAB, scale_factor=1.0), run_time=1.0)
        self.at("gold for carrying capacity")
        self.play(Indicate(gauge[3], color=CAPACITY, scale_factor=1.0), run_time=1.0)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Populations and Carrying Capacity"
    TITLE = "Did the Limit Move?"


class S03TwoTrackers(SpokenScene):
    def construct(self):
        gauge = paired_gauge(pop=0.68, cap=0.86, center=(-3.5, -0.15, 0), height=5.5)
        case = animate_creek(mini_case((2.65, -0.25, 0), crabs=3, shelter="full"))
        tag = scope_tag("schematic")
        self.at("Population size means")
        self.play(FadeIn(gauge), gauge.pop_t.animate.set_value(0.42), run_time=1.5)
        self.at("Carrying capacity means")
        self.play(FadeIn(case), gauge.cap_t.animate.set_value(0.88), run_time=1.8)
        self.at("The trackers can move together")
        self.play(gauge.pop_t.animate.set_value(0.65), gauge.cap_t.animate.set_value(0.72), run_time=2.0)
        self.at("but they are not")
        self.play(gauge.pop_t.animate.set_value(0.30), run_time=1.5)
        self.at("A low population")
        low = T("same low population", 30, CRAB).move_to([2.65, 2.45, 0])
        self.play(FadeIn(low), gauge.pop_t.animate.set_value(0.25), run_time=1.1)
        self.at("either a high")
        self.play(gauge.cap_t.animate.set_value(0.86), run_time=1.3)
        self.at("or low capacity")
        sparse = mini_case((2.65, -0.25, 0), crabs=3, shelter="low")
        animate_creek(sparse)
        self.play(ReplacementTransform(case, sparse), gauge.cap_t.animate.set_value(0.42),
                  FadeIn(tag), run_time=1.5)
        self.finish()


class S04BriefEvent(SpokenScene):
    def construct(self):
        world = animate_creek(creek_world(center=(-1.65, -0.2, 0), width=8.7, height=5.5))
        gauge = paired_gauge(center=(4.75, -0.2, 0), height=5.0)
        self.at("Begin with a brief cold event")
        self.play(FadeIn(world), FadeIn(gauge), run_time=1.0)
        cold = animate_creek(creek_world(center=(-1.65, -0.2, 0), width=8.7, height=5.5,
                                         crabs=3, cold=True))
        self.at("Some teal crabs disappear")
        self.play(ReplacementTransform(world, cold), gauge.pop_t.animate.set_value(0.42), run_time=1.5)
        self.at("Food space and shelter remain")
        self.play(Indicate(cold.food, color=CAPACITY, scale_factor=1.0),
                  Indicate(cold.grasses, color=SHELTER, scale_factor=1.0), run_time=1.3)
        self.at("gold support level stays put")
        self.play(Indicate(gauge[3], color=CAPACITY, scale_factor=1.0), run_time=1.2)
        label = caption("brief event · support assumed unchanged", 28, TEXT, y=-3.48)
        self.at("The population may grow back")
        clear = animate_creek(creek_world(center=(-1.65, -0.2, 0), width=8.7, height=5.5, crabs=3))
        self.play(ReplacementTransform(cold, clear), FadeIn(label),
                  gauge.pop_t.animate.set_value(0.70), run_time=3.0, rate_func=smooth)
        self.finish()


class S05LastingChange(SpokenScene):
    def construct(self):
        world = animate_creek(creek_world(center=(-3.55, 0.1, 0), width=6.0, height=5.0))
        self.at("Now change the creek")
        self.play(FadeIn(world), run_time=1.0)
        lost = animate_creek(creek_world(center=(-3.55, 0.1, 0), width=6.0, height=5.0,
                                        crabs=4, shelter="low"))
        self.at("Remove much of the green shelter")
        self.play(ReplacementTransform(world, lost), run_time=1.5)
        bare = T("fewer hiding places", 30, CHALLENGE).move_to([-3.55, 2.95, 0])
        self.at("Young crabs have fewer")
        self.play(FadeIn(bare), run_time=0.9)
        P = Plot(box=(-0.25, 5.95, -1.95, 2.35), xr=(0, 8), yr=(0, 10),
                 xticks=[0, 4, 8], yticks=[(0,"0"), (5,"5"), (9,"9")],
                 xlabel="time", ylabel="population")
        old_k, new_k = P.hline(9, "old support", CAPACITY), P.hline(5, "lower support", CAPACITY)
        t = ValueTracker(0.01)
        live = P.live_curve(lambda x: logistic(x, 5), t, color=CRAB, width=7)
        self.at("environment supports fewer crabs")
        self.play(Create(P), FadeIn(old_k), run_time=1.2)
        self.at("gold carrying capacity tracker moves down")
        self.play(ReplacementTransform(old_k, new_k), run_time=1.4)
        self.add(live)
        self.at("population growth now slows")
        self.play(t.animate.set_value(8), run_time=3.0, rate_func=linear)
        self.play(FadeIn(scope_tag("computed model · habitat schematic")), run_time=0.5)
        self.finish()


def prediction_backdrop():
    panels = TwoPanel("brief event", "lasting shelter loss", colors=(GREY, CHALLENGE),
                      top=3.0, bottom=-1.75)
    left = animate_creek(mini_case((-3.3, 0.25, 0), crabs=3, shelter="full", cold=True))
    right = animate_creek(mini_case((3.3, 0.25, 0), crabs=3, shelter="low"))
    qs = VGroup(T("?", 62, CAPACITY).move_to([-3.3, 1.65, 0]),
                T("?", 62, CAPACITY).move_to([3.3, 1.65, 0]))
    return VGroup(panels, left, right, qs)


PREDICT_Q = "Can the count alone tell whether carrying capacity moved?"


class S06Predict(SpokenScene):
    def construct(self):
        back = prediction_backdrop()
        self.at("Here is the prediction")
        self.play(FadeIn(back[0]), run_time=0.8)
        self.at("Both windows now show")
        self.play(FadeIn(back[1]), FadeIn(back[2]), run_time=1.1)
        self.at("The left followed")
        self.play(Indicate(back[1], color=GREY, scale_factor=1.0), run_time=0.8)
        self.at("The right lost shelter")
        self.play(Indicate(back[2].grasses, color=SHELTER, scale_factor=1.0), run_time=0.9)
        self.at("Can the count alone")
        self.play(FadeIn(back[3]), run_time=0.9)
        q = question_card(PREDICT_Q, y=-3.0, size=30)
        self.at("Hold your answer")
        self.play(FadeIn(q), run_time=0.8)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = PREDICT_Q
    SECONDS = 4.5
    CARD = {"y": -3.0, "size": 30}
    def backdrop(self):
        return prediction_backdrop()


class S08Reveal(SpokenScene):
    def construct(self):
        back = prediction_backdrop()
        self.add(back[0], back[1], back[2])
        high = T("support stayed high", 28, CAPACITY).move_to([-3.3, -2.25, 0])
        low = T("support moved lower", 28, CAPACITY).move_to([3.3, -2.25, 0])
        self.at("Now the same abundance")
        self.play(FadeIn(high), FadeIn(low), run_time=1.2)
        self.at("scientists need evidence")
        self.play(FadeOut(VGroup(back[0], back[1], back[2], high, low)), run_time=0.7)
        line = Arrow([-5.6, 0, 0], [5.6, 0, 0], color=GREY, stroke_width=4, buff=0)
        evidence = VGroup(*[chip(x, col, 25) for x, col in
                            [("food", CAPACITY), ("habitat", SHELTER), ("predators", CHALLENGE),
                             ("weather", GREY), ("survival", CRAB)]])
        evidence.arrange(RIGHT, buff=0.24).move_to([0, 1.0, 0]); fit(evidence, 12.2)
        bob(evidence, amp=0.07, speed=1.1)
        glass = VGroup(Circle(radius=0.42, color=TEXT, stroke_width=5),
                       Line([0.3,-0.3,0], [0.8,-0.8,0], color=TEXT, stroke_width=6)).move_to([-5.0, 0, 0])
        self.play(Create(line), FadeIn(evidence), FadeIn(glass), run_time=1.1)
        self.at("across time")
        self.play(glass.animate.move_to([5.0, 0, 0]), run_time=3.0, rate_func=linear)
        count = chip("count = population size", CRAB, 32).move_to([0, 1.1, 0])
        unknowns = VGroup(chip("capacity = ?", CAPACITY, 30), chip("cause = ?", CHALLENGE, 30)).arrange(RIGHT, buff=0.8).move_to([0, -1.0, 0])
        bob(count, amp=0.07, speed=1.2)
        bob(unknowns, amp=0.07, speed=1.0, seed=2)
        self.at("The count shows population size")
        self.play(FadeOut(VGroup(line, evidence, glass)), FadeIn(count), run_time=1.0)
        self.at("It does not measure carrying capacity")
        self.play(FadeIn(unknowns[0]), run_time=1.0)
        self.at("or identify which limiting factor")
        self.play(FadeIn(unknowns[1]), run_time=1.0)
        self.finish()


class S09Survey(SpokenScene):
    def construct(self):
        bay = RoundedRectangle(width=11.8, height=5.2, corner_radius=0.6, color=GREY,
                               stroke_width=3, fill_color="#173543", fill_opacity=0.5).move_to([0,0.25,0])
        bay._glow_t = 0.0
        def bay_glow(mob, dt):
            mob._glow_t += dt
            mob.set_fill(opacity=0.5 + 0.06*np.sin(1.5*mob._glow_t))
        bay.add_updater(bay_glow)
        sites = VGroup(*[Dot([x,y,0], radius=0.09, color=CRAB) for x,y in
                         [(-4,1.3),(-2.7,-.5),(-1.2,1.6),(.4,-.7),(1.8,1.1),(3.5,-.4),(4.6,1.5)]])
        dredge = VGroup(Rectangle(width=1.0, height=0.55, color=TEAL),
                        Line([0,0.28,0],[0,1.15,0],color=TEAL,stroke_width=4)).move_to([-4,1.3,0])
        self.at("winter dredge survey")
        self.play(FadeIn(bay), FadeIn(sites), FadeIn(dredge), run_time=1.0)
        self.at("Crews sample buried crabs")
        self.play(dredge.animate.move_to([3.5,-0.4,0]), run_time=3.0, rate_func=linear)
        estimate = chip("Bay-wide estimate", CRAB, 36).move_to([0,0.4,0])
        bob(estimate, amp=0.08, speed=1.1)
        self.at("build a Bay wide estimate")
        self.play(FadeOut(VGroup(bay, sites, dredge)), FadeIn(estimate), run_time=1.1)
        exact = T("not an exact count", 30, GREY).move_to([0,-0.8,0])
        self.at("not an exact count")
        self.play(FadeIn(exact), run_time=0.8)
        arrows = VGroup(Arrow([-3.6,-2.1,0],[-3.6,1.9,0],color=TEXT),
                        Arrow([3.6,1.9,0],[3.6,-2.1,0],color=TEXT))
        groups = VGroup(T("reported group", 28, TEXT).next_to(arrows[0], DOWN),
                        T("reported group", 28, TEXT).next_to(arrows[1], DOWN))
        bob(arrows, amp=0.07, speed=1.0)
        self.at("reported groups rose or fell")
        self.play(FadeOut(exact), FadeIn(arrows), FadeIn(groups), run_time=1.5)
        qs = VGroup(chip("capacity?", CAPACITY, 30), chip("cause?", CHALLENGE, 30)).arrange(RIGHT, buff=0.6).move_to([0,-2.8,0])
        bob(qs, amp=0.07, speed=1.0)
        self.at("cannot show why")
        self.play(FadeOut(VGroup(arrows, groups)), run_time=0.5)
        self.play(FadeIn(qs), run_time=0.6)
        self.finish()


class S10People(SpokenScene):
    def construct(self):
        world = animate_creek(creek_world(center=(-1.65,-0.2,0), width=8.7, height=5.5))
        gauge = paired_gauge(center=(4.75,-0.2,0), height=5.0)
        self.at("lasting gain in food")
        self.play(FadeIn(world), FadeIn(gauge), gauge.cap_t.animate.set_value(0.92), run_time=1.6)
        lost = animate_creek(creek_world(center=(-1.65,-0.2,0), width=8.7, height=5.5,
                                        crabs=5, shelter="low"))
        self.at("Lasting habitat loss")
        self.play(ReplacementTransform(world, lost), gauge.cap_t.animate.set_value(0.48), run_time=1.6)
        self.at("People can affect both trackers")
        basket = chip("harvest", TEXT, 30).move_to([1.4, 2.4, 0])
        self.play(FadeIn(basket), run_time=0.8)
        self.at("Harvest removes individuals")
        self.play(lost.crabs[-1].animate.move_to(basket).set_opacity(0),
                  lost.crabs[-2].animate.move_to(basket).set_opacity(0),
                  gauge.pop_t.animate.set_value(0.42), run_time=1.8)
        built = animate_creek(creek_world(center=(-1.65,-0.2,0), width=8.7, height=5.5,
                                         crabs=3, shelter="low", built=True))
        self.at("shoreline building can remove marsh")
        self.play(FadeOut(basket), ReplacementTransform(lost, built),
                  gauge.cap_t.animate.set_value(0.34), run_time=1.8)
        note = caption("removing individuals ≠ proof support changed", 28, TEXT, y=-3.48)
        self.at("does not automatically prove")
        self.play(FadeIn(note), gauge.pop_t.animate.set_value(0.30), run_time=1.2)
        self.play(FadeIn(scope_tag("schematic")), run_time=0.4)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        world = animate_creek(creek_world(center=(-1.65,-0.2,0), width=8.7, height=5.5))
        gauge = paired_gauge(center=(4.75,-0.2,0), height=5.0)
        self.at("Return to the paired trackers")
        self.play(FadeIn(world), FadeIn(gauge), run_time=0.9)
        cold = animate_creek(creek_world(center=(-1.65,-0.2,0), width=8.7, height=5.5,
                                         crabs=3, cold=True))
        self.at("brief shock moved the teal")
        self.play(ReplacementTransform(world, cold), gauge.pop_t.animate.set_value(0.38), run_time=1.4)
        lost = animate_creek(creek_world(center=(-1.65,-0.2,0), width=8.7, height=5.5,
                                         crabs=3, shelter="low"))
        self.at("Lasting shelter loss")
        self.play(ReplacementTransform(cold, lost), gauge.cap_t.animate.set_value(0.42), run_time=1.5)
        P = Plot(box=(-5.7,5.7,-1.8,2.3), xr=(0,8), yr=(0,10), xticks=[0,4,8],
                 yticks=[(0,"0"),(5,"5"),(10,"10")], xlabel="time", ylabel="value")
        path = P.curve(lambda t: 5 + 2*np.sin(0.9*t), color=CRAB, width=7)
        self.at("whenever a graph rises or falls")
        self.play(FadeOut(VGroup(lost,gauge)), run_time=0.65)
        self.play(Create(P), Create(path), run_time=1.35)
        qs = VGroup(chip("what changed?", CAPACITY, 30), chip("how long?", CAPACITY, 30),
                    chip("what evidence?", CAPACITY, 30)).arrange(RIGHT,buff=0.45).move_to([0,-3.28,0])
        self.at("Ask what changed")
        self.play(FadeIn(qs[0]), run_time=0.8)
        self.at("how long it lasted")
        self.play(FadeIn(qs[1]), run_time=0.8)
        self.at("what evidence measured it")
        self.play(FadeIn(qs[2]), run_time=0.8)
        self.play(FadeOut(qs), run_time=0.7)
        self.finish()


class S12End(EndCard):
    LINE = "Lasting changes in resources or conditions can move carrying capacity."
