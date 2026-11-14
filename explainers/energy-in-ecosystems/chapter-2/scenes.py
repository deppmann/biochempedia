"""Energy Flows, Matter Returns — Chesapeake Bay chapter 2.

COLOR MAP (kept throughout this chapter)
  GOLD/YELLOW = usable energy and sunlight
  GREEN       = living carbon, producer tissue, carbon path
  TEAL        = consumers
  BLUE        = decomposers
  RED         = dispersed heat
  GREY        = landscape, guides, and qualifications
"""
from bp_parts import *  # noqa: F401,F403


ENERGY = GOLD
CARBON = GREEN
CONSUMER = TEAL
DECOMP = BLUE
HEAT = RED


def arrow(a, b, color=GREY, width=6, dashed=False):
    """A consistent pathway arrow used throughout the Bay picture."""
    cls = DashedLine if dashed else Arrow
    kw = dict(color=color, stroke_width=width)
    if dashed:
        return cls(a, b, dash_length=0.16, **kw)
    return cls(a, b, buff=0.08, tip_length=0.22, **kw)


def fish(color=CONSUMER, scale=1.0):
    """Simple menhaden silhouette; intentionally not an anatomical diagram."""
    body = Ellipse(width=2.0, height=0.82, color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.18)
    tail = Polygon([-1.0, 0, 0], [-1.55, 0.52, 0], [-1.55, -0.52, 0],
                   color=color, stroke_width=4, fill_color=color, fill_opacity=0.18)
    eye = Dot([0.62, 0.15, 0], radius=0.055, color=TEXT)
    fin = Line([-0.15, -0.05, 0], [-0.55, -0.38, 0], color=color, stroke_width=4)
    return VGroup(tail, body, fin, eye).scale(scale)


def plankton_cluster(color=CARBON, scale=1.0):
    dots = VGroup(*[
        Circle(radius=r, color=color, stroke_width=3, fill_color=color, fill_opacity=0.20)
        for r in (0.22, 0.16, 0.20, 0.13, 0.17)
    ])
    for d, p in zip(dots, [(-0.55, 0.05), (-0.15, 0.32), (0.25, 0.0), (0.55, 0.28), (0.05, -0.35)]):
        d.move_to([p[0], p[1], 0])
    return dots.scale(scale)


def decomposer_cluster(scale=1.0):
    blobs = VGroup(*[
        Circle(radius=r, color=DECOMP, stroke_width=3, fill_color=DECOMP, fill_opacity=0.28)
        for r in (0.21, 0.17, 0.23, 0.15, 0.18)
    ])
    for d, p in zip(blobs, [(-0.52, 0), (-0.20, 0.25), (0.15, -0.02), (0.48, 0.22), (0.58, -0.20)]):
        d.move_to([p[0], p[1], 0])
    return blobs.scale(scale)


def bay_world(include_labels=True):
    """The carried Bay world: every continuing scene calls this exact builder."""
    sky = Rectangle(width=13.4, height=2.15, stroke_width=0, fill_color="#28556F",
                    fill_opacity=1).move_to([0, 2.62, 0])
    water = Rectangle(width=13.4, height=4.55, stroke_width=0, fill_color="#0A2635",
                      fill_opacity=1).move_to([0, -0.72, 0])
    bed = Polygon([-6.7, -2.72, 0], [-3.5, -2.50, 0], [0.3, -2.75, 0],
                  [3.4, -2.48, 0], [6.7, -2.70, 0], [6.7, -3.72, 0], [-6.7, -3.72, 0],
                  color=GREY, stroke_width=2, fill_color="#273238", fill_opacity=1)
    surface = VGroup(*[
        ArcBetweenPoints([-6.7 + 1.34 * i, 1.52, 0], [-5.36 + 1.34 * i, 1.52, 0],
                         angle=(-1) ** i * 0.10, color=TEAL, stroke_width=2,
                         stroke_opacity=0.60)
        for i in range(10)
    ])
    sun = VGroup(Circle(radius=0.48, color=ENERGY, stroke_width=5,
                        fill_color=ENERGY, fill_opacity=0.18),
                 *[Line(0.62 * np.array([np.cos(a), np.sin(a), 0]),
                        0.86 * np.array([np.cos(a), np.sin(a), 0]), color=ENERGY, stroke_width=3)
                   for a in np.linspace(0, TAU, 8, endpoint=False)]).move_to([-5.35, 2.72, 0])
    phy = plankton_cluster(scale=1.18).move_to([-4.15, -0.65, 0])
    zoo = plankton_cluster(color=CONSUMER, scale=0.78).move_to([-1.35, 0.05, 0])
    men = fish(scale=0.9).move_to([2.15, -0.20, 0])
    dec = decomposer_cluster(scale=1.05).move_to([1.95, -2.70, 0])
    motes = VGroup(*[Dot([x, y, 0], radius=0.035, color=TEAL).set_opacity(0.32)
                     for x, y in [(-5.8, .6), (-3.2, .15), (-.2, .85), (3.7, .45), (5.5, -.8),
                                  (-5.0, -1.8), (-1.8, -1.2), (4.5, -1.9)]])

    # Ambient motion is attached inside the builder so every reconstructed Bay feels identical.
    for i, m in enumerate(motes):
        m._drift = 0.0
        base = m.get_center().copy()
        def drift(mob, dt, base=base, i=i):
            mob._drift += dt
            mob.move_to(base + RIGHT * 0.16 * np.sin(0.55 * mob._drift + i)
                        + UP * 0.06 * np.sin(0.85 * mob._drift + 0.7 * i))
        m.add_updater(drift)
    bob(phy, amp=0.07, speed=0.8, seed=1)
    bob(zoo, amp=0.10, speed=1.0, seed=2)
    bob(men, amp=0.08, speed=0.9, seed=3)
    pulse(dec, base=3.2, amp=0.8, speed=1.4)

    world = VGroup(sky, water, bed, surface, sun, phy, zoo, men, dec, motes)
    world.sky, world.water, world.bed, world.surface = sky, water, bed, surface
    world.sun, world.phy, world.zoo, world.men, world.dec = sun, phy, zoo, men, dec
    if include_labels:
        labels = VGroup(
            T("phytoplankton", 28, CARBON).move_to([-4.15, -1.42, 0]),
            T("zooplankton", 28, CONSUMER).move_to([-1.35, 0.72, 0]),
            T("menhaden", 28, CONSUMER).move_to([2.15, 0.58, 0]),
            T("decomposers", 28, DECOMP).move_to([1.95, -3.35, 0]),
        )
        world.add(labels)
        world.labels = labels
    world.layout_ok = True  # landscape shapes intentionally sit behind their own labels
    return world


def trackers():
    """Small carried corner reminders: energy straight, carbon looping."""
    e = VGroup(Arrow([-4.15, 2.95, 0], [-2.55, 2.95, 0], buff=0, color=ENERGY,
                     stroke_width=6, tip_length=0.20),
               T("energy", 26, ENERGY).move_to([-3.35, 3.33, 0]))
    loop = VGroup(Arc(radius=0.45, start_angle=0.25, angle=TAU * 0.86,
                      arc_center=[5.35, 3.15, 0], color=CARBON, stroke_width=6),
                  Triangle(color=CARBON, fill_color=CARBON, fill_opacity=1).scale(0.10)
                  .rotate(-0.25).move_to([5.78, 3.05, 0]),
                  T("carbon", 26, CARBON).move_to([5.35, 2.48, 0]))
    return VGroup(e, loop)


def token(letter, color, at):
    c = Circle(radius=0.31, color=color, stroke_width=4, fill_color=color, fill_opacity=0.22).move_to(at)
    t = T(letter, 28, color, weight=BOLD).move_to(c)
    return VGroup(c, t)


def heat_ripples(center=(3.6, 0.2, 0), count=3):
    return VGroup(*[
        Arc(radius=0.55 + i * 0.42, start_angle=-0.25, angle=PI + 0.5,
            arc_center=center, color=HEAT, stroke_width=max(2, 6 - i),
            stroke_opacity=max(0.25, 0.9 - i * 0.22))
        for i in range(count)
    ])


def return_question_world():
    """Exact end frame for the predict scene and exact backdrop for its pause."""
    w = bay_world()
    w.remove(w.men)
    w.labels.remove(w.labels[2])
    dead = fish(scale=0.82).rotate(-0.10).move_to([1.9, -2.05, 0])
    c = token("C", CARBON, [1.58, -1.94, 0])
    e = token("E", ENERGY, [2.22, -1.94, 0])
    c.layout_ok = True  # tokens are deliberately shown inside the dead fish
    e.layout_ok = True
    p1 = CurvedArrow(c.get_left(), w.phy.get_bottom(), angle=-0.45, color=CARBON,
                     stroke_width=4, tip_length=0.20).set_stroke(opacity=0.62)
    p2 = CurvedArrow(e.get_right(), w.phy.get_right(), angle=0.65, color=ENERGY,
                     stroke_width=4, tip_length=0.20).set_stroke(opacity=0.62)
    p1 = DashedVMobject(p1, num_dashes=20)
    p2 = DashedVMobject(p2, num_dashes=20)
    qs = VGroup(T("?", 54, CARBON, weight=BOLD).move_to([-3.45, -1.58, 0]),
                T("?", 54, ENERGY, weight=BOLD).move_to([-2.95, 0.20, 0]))
    qs.layout_ok = True  # dotted possibilities deliberately terminate at these question marks
    q = question_card("Can decomposers return both paths?", y=2.55, color=TEXT,
                      size=34, max_w=7.5)
    g = VGroup(w, dead, c, e, p1, p2, qs, q)
    g.world, g.dead, g.c_token, g.e_token = w, dead, c, e
    g.paths, g.questions, g.card = VGroup(p1, p2), qs, q
    return g


def pathway_map():
    """The side-by-side schematic used in comparison and later scenes."""
    carbon_loop = VGroup(
        Circle(radius=1.70, color=CARBON, stroke_width=7).move_to([-3.2, -0.05, 0]),
        Triangle(color=CARBON, fill_color=CARBON, fill_opacity=1).scale(0.16)
        .rotate(-0.25).move_to([-1.58, -0.47, 0]),
        T("matter mostly cycles", 32, CARBON, weight=BOLD).move_to([-3.2, 2.34, 0]),
    )
    energy_path = VGroup(
        Arrow([0.75, -0.05, 0], [5.35, -0.05, 0], buff=0, color=ENERGY,
              stroke_width=10, tip_length=0.32),
        heat_ripples(center=[5.0, -0.05, 0], count=3),
        T("energy moves forward", 32, ENERGY, weight=BOLD).move_to([3.05, 2.34, 0]),
    )
    carbon_loop.layout_ok = True
    energy_path.layout_ok = True
    return VGroup(carbon_loop, energy_path)


class S00Hook(SpokenScene):
    def construct(self):
        w = bay_world()
        self.add(w)
        self.at("The energy pyramid")
        tissue = VGroup(
            Polygon([-5.5, -2.1, 0], [-3.9, 1.15, 0], [-2.3, -2.1, 0],
                    color=ENERGY, stroke_width=4, fill_color=ENERGY, fill_opacity=0.10),
            T("tissue branch", 30, ENERGY).move_to([-3.9, -2.35, 0]))
        self.play(FadeIn(tissue), run_time=1.3)
        self.at("What happens")
        q = T("?", 80, ENERGY, weight=BOLD).move_to([4.8, 0.15, 0])
        self.play(FadeOut(tissue), FadeIn(q, shift=UP * 0.2), run_time=1.0)
        self.at("Return to the same bay")
        self.play(Indicate(w.men, color=CONSUMER, scale_factor=1.10), run_time=1.0)
        self.at("Gold energy")
        e = token("E", ENERGY, [-3.85, -0.40, 0])
        c = token("C", CARBON, [-4.45, -0.40, 0])
        self.play(FadeOut(q), FadeIn(e), FadeIn(c), run_time=0.7)
        self.play(e.animate.move_to([1.85, -0.05, 0]), c.animate.move_to([1.35, -0.05, 0]), run_time=1.3)
        self.at("then separate")
        q1 = T("?", 72, ENERGY, weight=BOLD).move_to([4.7, 0.8, 0])
        q2 = T("?", 72, CARBON, weight=BOLD).move_to([4.7, -1.0, 0])
        self.play(e.animate.move_to([3.65, 0.8, 0]), c.animate.move_to([3.65, -1.0, 0]),
                  FadeIn(q1), FadeIn(q2), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Energy in Ecosystems"
    TITLE = "Energy Flows, Matter Returns"

    def construct(self):
        w = bay_world(include_labels=False).set_opacity(0.34)
        title = fit_text(self.TITLE, max_w=11.2, size=54, color=TEXT,
                         min_size=40, font=TITLE_FONT).move_to([0, 0.35, 0])
        lesson = T(self.LESSON.upper(), 24, TEAL).move_to([0, 1.12, 0])
        rule = Line([-1.4, -0.25, 0], [1.4, -0.25, 0], color=ENERGY, stroke_width=5)
        self.add(w)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=1.15)
        tr = trackers()
        self.play(FadeOut(lesson), FadeOut(title), FadeOut(rule), FadeIn(tr), run_time=0.75)
        self.finish()


class S02Forms(SpokenScene):
    def construct(self):
        w = bay_world()
        w.labels.remove(w.labels[3])  # decomposers not discussed here; keeps the caption clear
        tr = trackers()
        self.add(w, tr[0])
        self.at("Sunlight enters")
        beam = arrow(w.sun.get_bottom(), w.phy.get_top(), ENERGY, width=10)
        pulse_dot = Dot(w.sun.get_bottom(), radius=0.16, color=ENERGY)
        self.play(GrowArrow(beam), MoveAlongPath(pulse_dot, beam), run_time=2.0)
        self.at("Phytoplankton change")
        food = arrow(w.phy.get_right(), w.zoo.get_left(), ENERGY, width=10)
        self.play(Indicate(w.phy, color=CARBON, scale_factor=1.15), GrowArrow(food), run_time=1.7)
        self.at("Consumers change")
        food2 = arrow(w.zoo.get_right(), w.men.get_left(), ENERGY, width=9)
        self.play(GrowArrow(food2), run_time=1.2)
        self.at("movement")
        fin = CurvedArrow(w.men.get_top(), w.men.get_top() + [1.2, 0.45, 0], angle=-0.6,
                          color=TEXT, stroke_width=5, tip_length=0.18)
        self.play(Create(fin), w.men.animate.shift(RIGHT * 0.35), run_time=0.8)
        self.at("new tissue")
        patch = Ellipse(width=0.70, height=0.35, color=CARBON, stroke_width=3,
                        fill_color=CARBON, fill_opacity=0.35).move_to(w.men.get_center())
        self.play(GrowFromCenter(patch), run_time=0.7)
        self.at("red heat")
        heat = heat_ripples(center=w.men.get_center() + RIGHT * 0.7, count=4)
        self.play(LaggedStart(*[Create(r) for r in heat], lag_ratio=0.15),
                  FadeOut(w.labels[2]), run_time=1.3)
        self.at("Energy is never")
        forms = caption("radiant  →  chemical  →  movement, tissue, heat", size=30, color=ENERGY).move_to([0, -3.55, 0])
        forms.layout_ok = True  # caption sits on the seabed band, which is only a backdrop
        self.play(FadeIn(forms), run_time=0.8)
        self.at("It changes form")
        self.play(Indicate(VGroup(beam, food, food2), color=ENERGY, scale_factor=1.02),
                  run_time=1.4)
        self.finish()


class S03Heat(SpokenScene):
    def construct(self):
        w = bay_world()
        tr = trackers()
        w.labels.remove(w.labels[3])
        self.add(w, tr[0])
        self.at("Heat spreads")
        ripples = heat_ripples(center=[2.9, 0.1, 0], count=6)
        self.play(LaggedStart(*[Create(r) for r in ripples], lag_ratio=0.16),
                  FadeOut(w.labels[2]), run_time=1.8)
        lab = T("dispersed heat", 30, HEAT).move_to([-1.55, 2.45, 0])
        self.play(FadeIn(lab), ripples.animate.set_opacity(0.45).scale(1.18), run_time=1.0)
        self.at("No living thing")
        try_back = CurvedArrow([4.9, 1.3, 0], w.phy.get_top(), angle=0.8, color=HEAT,
                               stroke_width=4, tip_length=0.2)
        cross = VGroup(Line([-0.22, -0.22, 0], [0.22, 0.22, 0], color=HEAT, stroke_width=7),
                       Line([-0.22, 0.22, 0], [0.22, -0.22, 0], color=HEAT, stroke_width=7))
        cross.move_to([-3.0, 0.25, 0])
        self.play(Create(try_back), run_time=1.1)
        self.play(FadeOut(try_back), Create(cross), ripples.animate.shift(UP * 0.55).set_opacity(0.20), run_time=1.2)
        self.at("The gold path")
        gold = arrow([-5.65, 1.15, 0], [2.55, 1.15, 0], ENERGY, width=9)
        self.play(GrowArrow(gold), run_time=1.6)
        self.at("Nearly every ecosystem")
        self.play(FadeOut(cross), FadeOut(lab), ripples.animate.scale(1.15).set_opacity(0.10), run_time=1.1)
        self.at("In the bay")
        supply = T("new energy supply", 30, ENERGY).move_to([-2.2, 2.15, 0])
        beam = arrow(w.sun.get_bottom(), w.phy.get_top(), ENERGY, width=9)
        dot = Dot(w.sun.get_bottom(), radius=0.16, color=ENERGY)
        self.play(FadeIn(supply), GrowArrow(beam), MoveAlongPath(dot, beam), run_time=1.4)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        w = bay_world()
        w.labels.remove(w.labels[2])
        self.add(w, trackers())
        self.at("A menhaden dies")
        dead = w.men
        dead.clear_updaters()
        self.play(dead.animate.scale(0.91).rotate(-0.10).move_to([1.9, -2.05, 0]), run_time=1.4)
        self.at("blue decomposers")
        self.play(w.dec.animate.shift(UP * 0.25), Indicate(w.dec, color=DECOMP, scale_factor=1.12), run_time=1.0)
        c = token("C", CARBON, [1.58, -1.94, 0])
        e = token("E", ENERGY, [2.22, -1.94, 0])
        c.layout_ok = True  # deliberately embedded in the fish
        e.layout_ok = True
        self.play(FadeIn(c), FadeIn(e), run_time=0.6)
        self.at("Can they return")
        p1 = DashedVMobject(CurvedArrow(c.get_left(), w.phy.get_bottom(), angle=-0.45,
                                       color=CARBON, stroke_width=4, tip_length=0.20), num_dashes=20)
        p2 = DashedVMobject(CurvedArrow(e.get_right(), w.phy.get_right(), angle=0.65,
                                       color=ENERGY, stroke_width=4, tip_length=0.20), num_dashes=20)
        qs = VGroup(T("?", 54, CARBON, weight=BOLD).move_to([-3.45, -1.58, 0]),
                    T("?", 54, ENERGY, weight=BOLD).move_to([-2.95, 0.20, 0]))
        qs.layout_ok = True  # dotted possibilities deliberately end at the question marks
        self.play(Create(p1), Create(p2), FadeIn(qs), run_time=1.8)
        self.at("Hold both paths")
        q = question_card("Can decomposers return both paths?", y=2.55, color=TEXT,
                          size=34, max_w=7.5)
        self.play(FadeIn(q), Indicate(VGroup(c, e), scale_factor=1.10), run_time=1.0)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        g = return_question_world()
        self.add(g)
        # Alternate pulses preserve the unrevealed question while students think.
        self.play(Indicate(g.c_token, color=CARBON, scale_factor=1.15), run_time=1.1)
        self.play(Indicate(g.e_token, color=ENERGY, scale_factor=1.15), run_time=1.1)
        self.play(Indicate(g.c_token, color=CARBON, scale_factor=1.15), run_time=1.1)
        self.play(Indicate(g.e_token, color=ENERGY, scale_factor=1.15), run_time=1.1)
        self.wait(0.1)


class S06Reveal(SpokenScene):
    def construct(self):
        g = return_question_world()
        w = g.world
        self.add(g)
        breath = ValueTracker(0.0)
        breath.add_updater(lambda m, dt: m.increment_value(dt))
        halo = always_redraw(lambda: VGroup(
            Circle(radius=0.68 + 0.22 * np.sin(3.0 * breath.get_value()),
                   color=DECOMP, stroke_width=18, stroke_opacity=0.80),
            Circle(radius=0.46 + 0.15 * np.sin(3.0 * breath.get_value() + PI),
                   color=TEAL, stroke_width=12, stroke_opacity=0.65),
        ).move_to(w.dec.get_center() + UP * 0.40))
        self.add(breath, halo)
        self.at("Decomposers release")
        self.play(FadeOut(g.card), FadeOut(g.questions), FadeOut(g.paths), run_time=0.6)
        co2 = chip("carbon dioxide", CARBON, size=28).move_to([-3.70, -2.15, 0])
        self.play(ReplacementTransform(g.c_token, co2), run_time=1.4)
        self.at("Phytoplankton can take")
        up = arrow(co2.get_top(), w.phy.get_bottom(), CARBON, width=7)
        self.play(Create(up), run_time=1.4)
        self.play(Indicate(w.phy, color=CARBON, scale_factor=1.15), run_time=0.8)
        self.at("green path closes")
        back = CurvedArrow(w.phy.get_right(), g.dead.get_left(), angle=-0.55, color=CARBON,
                           stroke_width=7, tip_length=0.24)
        self.play(Create(back), run_time=1.2)
        loop_label = T("carbon loop", 30, CARBON, weight=BOLD).move_to([-2.0, 1.85, 0])
        self.play(FadeIn(loop_label), run_time=0.6)
        self.at("Energy does not")
        broken = DashedLine(g.e_token.get_left() + LEFT * 0.10, [-2.85, 0.25, 0], color=ENERGY,
                            stroke_width=5, dash_length=0.18)
        x = VGroup(Line([-.22, -.22, 0], [.22, .22, 0], color=HEAT, stroke_width=7),
                   Line([-.22, .22, 0], [.22, -.22, 0], color=HEAT, stroke_width=7)).move_to([-0.5, -0.85, 0])
        self.play(Create(broken), Create(x), run_time=1.0)
        self.at("Decomposers also respire")
        growth = Ellipse(width=0.80, height=0.52, color=DECOMP, stroke_width=4,
                         fill_color=DECOMP, fill_opacity=0.32).move_to([3.0, -2.55, 0])
        glab = VGroup(T("decomposer", 28, DECOMP), T("growth", 28, DECOMP)).arrange(DOWN, buff=0.08).move_to([4.55, -2.55, 0])
        heat = heat_ripples(center=[2.25, -1.65, 0], count=4)
        self.play(TransformFromCopy(g.e_token, growth), FadeIn(glab), run_time=1.1)
        self.play(Transform(g.e_token, heat), run_time=1.5)
        self.at("leaves the usable")
        self.play(heat.animate.scale(1.22).set_opacity(0.24).shift(UP * 0.55),
                  FadeOut(broken), FadeOut(x), run_time=1.3)
        self.finish()


class S07Compare(SpokenScene):
    def construct(self):
        w = bay_world(include_labels=False).set_opacity(0.72)
        w.sun.set_opacity(0)  # the sun would sit behind the "matter mostly cycles" label
        maps = pathway_map()
        self.add(w)
        self.at("Compare the maps")
        self.play(FadeIn(maps), run_time=1.2)
        current = VGroup(
            Arc(radius=1.70, start_angle=0.1, angle=1.15, arc_center=[-3.2, -0.05, 0],
                color=CARBON, stroke_width=18),
            Arc(radius=1.70, start_angle=PI + 0.1, angle=0.72, arc_center=[-3.2, -0.05, 0],
                color=CARBON, stroke_width=12),
        )
        current._turn = 0.0
        def circulate(mob, dt):
            mob.rotate(0.62 * dt, about_point=[-3.2, -0.05, 0])
        current.add_updater(circulate)
        self.add(current)
        schem = scope_tag("schematic", size=26)
        self.add(schem)
        self.at("Carbon atoms")
        beads = VGroup(*[Dot(radius=0.13, color=CARBON) for _ in range(4)])
        loop_path = Circle(radius=1.70).move_to([-3.2, -0.05, 0])
        for i, b in enumerate(beads):
            b.move_to(loop_path.point_from_proportion(i / 4))
        self.play(*[MoveAlongPath(b, loop_path, rate_func=linear) for b in beads], run_time=3.1)
        self.at("Some may be")
        buried = T("buried", 28, GREY).move_to([-5.15, -2.45, 0])
        away = T("carried away", 28, GREY).move_to([-1.65, -2.45, 0])
        self.play(beads[0].animate.move_to(buried.get_top() + UP * 0.20),
                  beads[1].animate.move_to(away.get_top() + UP * 0.20),
                  FadeIn(buried), FadeIn(away), run_time=1.2)
        self.at("Energy enters")
        pulses = VGroup(*[Dot(radius=0.16, color=ENERGY).move_to([0.9, -0.05, 0]) for _ in range(3)])
        self.play(LaggedStart(*[p.animate.shift(RIGHT * 4.1) for p in pulses], lag_ratio=0.35), run_time=2.4)
        self.at("Matter mostly cycles")
        self.play(Indicate(maps[0], color=CARBON, scale_factor=1.02), run_time=1.0)
        self.at("Energy moves forward")
        self.play(Indicate(maps[1], color=ENERGY, scale_factor=1.02), run_time=1.2)
        self.finish()


class S08Exception(SpokenScene):
    def construct(self):
        w = bay_world(include_labels=False).set_opacity(0.68)
        tr = trackers()
        middle = arrow([-2.0, 0.95, 0], [3.15, 0.95, 0], ENERGY, width=10)
        heat = heat_ripples(center=[3.2, 0.95, 0], count=3)
        sun_entry = chip("sunlight", ENERGY, size=32).move_to([-4.55, 0.95, 0])
        self.add(w, tr, sun_entry, middle, heat)
        self.at("Not every ecosystem")
        self.play(Indicate(sun_entry, color=ENERGY, scale_factor=1.10), run_time=1.0)
        self.at("Some deep sea vent")
        vent = chip("chemical energy\nat a deep-sea vent", ENERGY, size=28).move_to([-4.55, 0.95, 0])
        self.play(swap(sun_entry, vent, run_time=1.2), w.sun.animate.set_opacity(0))
        self.at("That changes the entrance")
        self.play(Indicate(vent, color=ENERGY, scale_factor=1.08), run_time=1.0)
        self.at("energy still disperses")
        self.play(heat.animate.scale(1.1).set_opacity(0.38), run_time=1.4)
        self.at("The bay picture")
        new_sun = chip("sunlight", ENERGY, size=32).move_to([-4.55, 0.95, 0])
        self.play(swap(vent, new_sun, run_time=1.0), w.sun.animate.set_opacity(0.68))
        tag = scope_tag("sunlit ecosystem", size=28, color=TEAL)
        self.play(FadeIn(tag), w.animate.set_opacity(0.60), run_time=1.1)
        self.finish()


class S09Budgets(SpokenScene):
    def construct(self):
        tr = trackers()
        panels = TwoPanel("feeding level A", "feeding level B", colors=(CONSUMER, CONSUMER),
                          top=2.0, bottom=-2.35, size=32)
        bars = VGroup(Rectangle(width=4.8, height=1.35, color=ENERGY, stroke_width=4,
                                fill_color=ENERGY, fill_opacity=0.22),
                      Rectangle(width=3.4, height=1.35, color=ENERGY, stroke_width=4,
                                fill_color=ENERGY, fill_opacity=0.22))
        panels.put(bars[0], "left")
        panels.put(bars[1], "right")
        self.add(tr)
        self.at("Ecologists test")
        self.play(FadeIn(panels), FadeIn(bars), run_time=1.3)
        self.at("They compare")
        match = VGroup(chip("same area", TEAL, 28), chip("same time", TEAL, 28)).arrange(RIGHT, buff=0.4).move_to([0, -2.85, 0])
        self.play(FadeIn(match), run_time=1.0)
        self.at("matching measurements")
        self.play(Indicate(VGroup(bars[0], bars[1]), color=ENERGY, scale_factor=1.03), run_time=1.1)
        self.at("Intake")
        intake = VGroup(chip("intake", ENERGY, 30).move_to([-3.25, -0.15, 0]),
                        chip("intake", ENERGY, 30).move_to([3.25, -0.15, 0]))
        self.play(FadeIn(intake), run_time=0.8)
        self.at("new tissue")
        tissue = VGroup(chip("new tissue / year", CARBON, 28).move_to([-3.25, -0.45, 0]),
                        chip("new tissue / year", CARBON, 28).move_to([3.25, -0.45, 0]))
        self.play(FadeOut(intake), FadeIn(tissue), run_time=0.8)
        self.at("standing biomass")
        biomass = VGroup(chip("biomass now", CONSUMER, 28).move_to([-3.25, -0.45, 0]),
                         chip("biomass now", CONSUMER, 28).move_to([3.25, -0.45, 0]))
        self.play(FadeOut(tissue), FadeIn(biomass), run_time=0.8)
        self.at("Mixing them")
        mismatch = VGroup(chip("intake", ENERGY, 28).move_to([-3.25, -0.45, 0]),
                          chip("biomass now", CONSUMER, 28).move_to([3.25, -0.45, 0]))
        warn = caption("do not divide mismatched measures", size=32, color=HEAT)
        self.play(FadeOut(biomass), FadeIn(mismatch), FadeOut(match), FadeIn(warn), run_time=1.0)
        self.finish()


class S10Variation(SpokenScene):
    def construct(self):
        w = bay_world(include_labels=False).set_opacity(0.68)
        tr = trackers()
        self.add(w, tr)
        self.at("Transfer percentages vary")
        track = Line([-3.9, 2.25, 0], [3.9, 2.25, 0], color=GREY, stroke_width=9)
        knob = Dot([-2.8, 2.25, 0], radius=0.22, color=TEXT)
        lab = T("conditions", 30, TEXT).move_to([0, 2.78, 0])
        self.play(Create(track), FadeIn(knob), FadeIn(lab), run_time=1.2)
        self.play(knob.animate.move_to([2.7, 2.25, 0]), run_time=2.0, rate_func=there_and_back)
        self.at("Temperature")
        factors = VGroup(*[chip(x, TEAL, 27) for x in ("temperature", "eaten", "digestion", "respiration")])
        factors.arrange(RIGHT, buff=0.25).move_to([0, 1.35, 0])
        self.play(FadeIn(factors[0], shift=UP * 0.1), run_time=0.45)
        self.at("what gets eaten")
        self.play(FadeIn(factors[1], shift=UP * 0.1), run_time=0.45)
        self.at("digestion")
        self.play(FadeIn(factors[2], shift=UP * 0.1), run_time=0.45)
        self.at("respiration")
        self.play(FadeIn(factors[3], shift=UP * 0.1), run_time=0.45)
        self.at("change the share")
        band = Rectangle(width=5.3, height=0.72, color=ENERGY, stroke_width=4,
                         fill_color=ENERGY, fill_opacity=0.55).move_to([0, -0.25, 0])
        heat = heat_ripples(center=[3.7, -0.75, 0], count=4)
        decomp_branch = arrow([0.2, -0.62, 0], [1.5, -2.2, 0], DECOMP, width=5)
        self.play(FadeIn(band), Create(decomp_branch), Create(heat), run_time=1.4)
        self.play(band.animate.stretch(0.58, 1), heat.animate.scale(1.18), run_time=1.1)
        self.at("does not turn energy")
        no_loop = VGroup(Circle(radius=0.85, color=ENERGY, stroke_width=5),
                         Line([-0.65, -0.65, 0], [0.65, 0.65, 0], color=HEAT, stroke_width=8)).move_to([-4.8, -1.45, 0])
        self.play(FadeOut(factors), FadeIn(no_loop), run_time=1.0)
        self.at("It changes how wide")
        self.play(knob.animate.move_to([3.0, 2.25, 0]), band.animate.stretch(1.75, 1),
                  heat.animate.scale(0.86), run_time=2.0)
        self.play(knob.animate.move_to([-2.6, 2.25, 0]), band.animate.stretch(0.58, 1),
                  heat.animate.scale(1.20), run_time=1.7)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        w = bay_world(include_labels=False).set_opacity(0.72)
        w.remove(w.men, w.phy, w.zoo)  # chips below stand in for the plankton
        men = fish(scale=1.25).move_to([0, 0.1, 0])
        title = T("one menhaden, two paths", 36, TEXT, weight=BOLD).move_to([0, 3.12, 0])
        self.add(w, title)
        self.at("Return to the osprey's fish")
        self.play(FadeIn(men), men.animate.shift(RIGHT * 0.35), run_time=1.2)
        self.at("Its carbon may")
        c = token("C", CARBON, [-0.35, 0.1, 0])
        self.play(FadeIn(c), run_time=0.6)
        dec = chip("decomposers", DECOMP, 28).move_to([-4.7, -1.65, 0])
        co2 = chip("carbon dioxide", CARBON, 28).move_to([-4.7, -0.2, 0])
        phy = chip("phytoplankton", CARBON, 28).move_to([-4.7, 1.2, 0])
        cpath = VGroup(CurvedArrow(men.get_left(), dec.get_right(), angle=-0.3, color=CARBON, stroke_width=6),
                       arrow(dec.get_top(), co2.get_bottom(), CARBON, 6),
                       arrow(co2.get_top(), phy.get_bottom(), CARBON, 6),
                       CurvedArrow(phy.get_right(), men.get_top(), angle=-0.3, color=CARBON, stroke_width=6))
        self.play(FadeIn(dec), Create(cpath[0]), run_time=0.9)
        self.at("carbon dioxide")
        self.play(FadeIn(co2), Create(cpath[1]), run_time=0.7)
        self.at("phytoplankton again")
        self.play(FadeIn(phy), Create(cpath[2]), Create(cpath[3]), run_time=1.0)
        self.at("Its energy can")
        e = token("E", ENERGY, [0.35, 0.1, 0])
        move = chip("movement", TEXT, 28).move_to([3.15, 1.55, 0])
        growth = chip("growth", CARBON, 28).move_to([3.15, 0.25, 0])
        self.play(FadeIn(e), FadeIn(move), FadeIn(growth),
                  Create(arrow(men.get_right(), move.get_left(), ENERGY, 6)),
                  Create(arrow(men.get_right(), growth.get_left(), ENERGY, 6)), run_time=1.2)
        self.at("before becoming")
        heat = heat_ripples(center=[4.45, -1.80, 0], count=4)
        self.play(TransformFromCopy(e, heat), run_time=1.3)
        self.at("The same organism")
        self.play(Indicate(men, color=TEXT, scale_factor=1.08), run_time=0.9)
        self.at("matter loop")
        self.play(Indicate(cpath, color=CARBON, scale_factor=1.02), run_time=0.8)
        self.at("forward energy path")
        self.play(Indicate(VGroup(move, growth, heat), color=ENERGY, scale_factor=1.03), run_time=1.0)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        w = bay_world(include_labels=False).set_opacity(0.64)
        w.sun.set_opacity(0)
        maps = pathway_map().scale(1.12).move_to([0, -0.15, 0])
        self.add(w)
        self.at("Keep paths separate")
        self.play(FadeIn(maps), run_time=1.3)
        current = VGroup(
            Arc(radius=1.90, start_angle=0.2, angle=1.05, arc_center=[-3.55, -0.20, 0],
                color=CARBON, stroke_width=20),
            Arc(radius=1.90, start_angle=PI + 0.2, angle=0.72, arc_center=[-3.55, -0.20, 0],
                color=CARBON, stroke_width=13),
        )
        def circulate(mob, dt):
            mob.rotate(0.68 * dt, about_point=[-3.55, -0.20, 0])
        current.add_updater(circulate)
        self.add(current)
        self.at("Energy flows")
        p = Dot([0.7, -0.20, 0], radius=0.18, color=ENERGY)
        path = Line([0.7, -0.20, 0], [5.65, -0.20, 0])
        self.play(MoveAlongPath(p, path, rate_func=linear), run_time=1.7)
        self.at("while matter cycles")
        c = Dot([-1.28, -0.20, 0], radius=0.18, color=CARBON)
        loop = Circle(radius=1.90).move_to([-3.55, -0.20, 0])
        self.play(MoveAlongPath(c, loop, rate_func=linear), run_time=2.0)
        self.finish()


class S13End(EndCard):
    LINE = "Energy flows through ecosystems, while matter cycles and can be reused."
