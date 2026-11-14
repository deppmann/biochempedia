from bp_parts import *


# COLOR MAP: genes/alleles BLUE; environment GREEN; acquired changes GOLD;
# routes to offspring TEAL; stopped routes RED; other structures GREY.
PINK = "#E58FB5"
SOIL = "#9C7A52"


def gene_card(center=ORIGIN, scale=1.0):
    """The one carried gene-card picture, always rebuilt at the same proportions."""
    box = RoundedRectangle(
        corner_radius=0.08, width=0.72, height=0.92,
        stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18,
    )
    bars = VGroup(*[
        Line(LEFT * 0.21, RIGHT * (0.18 if i == 2 else 0.23), color=BLUE, stroke_width=3)
        .shift(UP * (0.23 - 0.21 * i))
        for i in range(3)
    ])
    return VGroup(box, bars).scale(scale).move_to(center)


def gene_cards(center=ORIGIN, scale=1.0, count=3, spacing=0.38):
    cards = VGroup(*[gene_card(scale=scale) for _ in range(count)])
    cards.arrange(RIGHT, buff=-0.72 * scale + spacing)
    return cards.move_to(center)


def mouse(center=(-3.6, 0, 0), scale=1.0, young=False, scar=False, genes=True):
    """The carried mouse picture used by every mouse scene."""
    s = scale * (0.72 if young else 1.0)
    col = GREY
    body = Ellipse(width=4.2, height=2.55, stroke_color=col, stroke_width=5,
                   fill_color=col, fill_opacity=0.30)
    head = Circle(radius=0.92, stroke_color=col, stroke_width=5,
                  fill_color=col, fill_opacity=0.30).move_to(body.get_right() + LEFT * 0.1 + UP * 0.42)
    ear = Circle(radius=0.34, stroke_color=col, stroke_width=4,
                 fill_color=col, fill_opacity=0.28).move_to(head.get_center() + UP * 0.72 + LEFT * 0.25)
    eye = Dot(head.get_center() + RIGHT * 0.25 + UP * 0.12, radius=0.07, color=TEXT)
    nose = Dot(head.get_right() + RIGHT * 0.04 + DOWN * 0.08, radius=0.08, color=PINK)
    legs = VGroup(*[
        Line([x, -1.0, 0], [x - 0.12, -1.42, 0], color=col, stroke_width=6)
        for x in (-1.15, 0.85)
    ])
    tail = ArcBetweenPoints(body.get_left() + RIGHT * 0.1, body.get_left() + LEFT * 1.15 + UP * 0.75,
                            angle=-1.25, color=col, stroke_width=5)
    g = VGroup(tail, legs, body, head, ear, eye, nose)
    if scar:
        mark = VGroup(
            Line([-0.55, 0.42, 0], [0.55, -0.22, 0], color=GOLD, stroke_width=9),
            *[Line([x - 0.16, y - 0.15, 0], [x + 0.16, y + 0.15, 0], color=GOLD, stroke_width=5)
              for x, y in ((-0.27, 0.25), (0.04, 0.07), (0.33, -0.1))],
        )
        g.add(mark)
        g.scar = mark
    if genes:
        cards = gene_cards([-0.6, -0.38, 0], scale=0.62, count=3, spacing=0.32)
        g.add(cards)
        g.cards = cards
    g.scale(s).move_to(center)
    return g


def eye_icon(center):
    outline = Ellipse(width=1.65, height=0.78, color=BLUE, stroke_width=4).move_to(center)
    return VGroup(outline, Circle(radius=0.27, color=BLUE, stroke_width=4).move_to(center),
                  Dot(center, radius=0.10, color=BLUE))


def acquired_icons():
    scar = VGroup(Line([-0.45, 0.2, 0], [0.45, -0.2, 0], color=GOLD, stroke_width=8),
                  Line([-0.18, -0.13, 0], [0.02, 0.19, 0], color=GOLD, stroke_width=4))
    hair = VGroup(Arc(radius=0.5, start_angle=0, angle=PI, color=GOLD, stroke_width=8),
                  *[Line([x, 0, 0], [x - 0.08, -0.52, 0], color=GOLD, stroke_width=5)
                    for x in (-0.38, -0.12, 0.14, 0.4)])
    keys = VGroup(*[Rectangle(width=0.28, height=0.8, color=GOLD, stroke_width=3)
                    .shift(RIGHT * (i - 2) * 0.28) for i in range(5)])
    muscle = VGroup(Arc(radius=0.52, start_angle=0.15, angle=2.5, color=GOLD, stroke_width=8),
                    Line([-0.42, -0.4, 0], [0.55, -0.4, 0], color=GOLD, stroke_width=8))
    row = VGroup(scar, hair, keys, muscle).arrange(RIGHT, buff=0.65)
    return row


def cell_region(center, label, color, kind):
    ring = Circle(radius=1.18, color=color, stroke_width=5, fill_color=color, fill_opacity=0.28).move_to(center)
    if kind == "skin":
        picture = VGroup(*[Square(0.34, color=GOLD, stroke_width=2).shift(RIGHT * (i - 1) * 0.38 + UP * (j - .5) * 0.38)
                           for i in range(3) for j in range(2)]).move_to(center)
        picture.add(Line(center + LEFT * .55 + UP * .38, center + RIGHT * .55 + DOWN * .38,
                         color=GOLD, stroke_width=7))
    elif kind == "muscle":
        picture = VGroup(*[RoundedRectangle(corner_radius=.08, width=1.35, height=.22,
                                            color=GOLD, stroke_width=3).shift(UP * (i - 1) * .32)
                           for i in range(3)]).move_to(center)
    else:
        picture = gene_cards(center, scale=.62, count=3, spacing=.31)
    lab = T(label, 28, color).next_to(ring, DOWN, buff=.15)
    return VGroup(ring, picture, lab)


def cell_map(with_young=True):
    skin = cell_region([-4.55, 1.25, 0], "skin cells", GOLD, "skin")
    muscle = cell_region([-4.55, -1.85, 0], "muscle cells", GOLD, "muscle")
    sex = cell_region([-1.25, -0.35, 0], "sex cells", BLUE, "sex")
    parts = VGroup(skin, muscle, sex)
    if with_young:
        baby = mouse([4.75, -0.15, 0], scale=.72, young=True, scar=False, genes=False)
        route = Arrow([0.15, -0.35, 0], [3.15, -0.25, 0], buff=0, color=TEAL,
                      stroke_width=7, tip_length=.28)
        parts.add(route, baby)
        parts.baby, parts.route = baby, route
    parts.skin, parts.muscle, parts.sex = skin, muscle, sex
    return parts


def gate(color=GREY, center=ORIGIN, opened=False):
    x, y, _ = center
    posts = VGroup(Line([x-.45, y-.75, 0], [x-.45, y+.75, 0], color=color, stroke_width=7),
                   Line([x+.45, y-.75, 0], [x+.45, y+.75, 0], color=color, stroke_width=7))
    bar = Line([x-.45, y+.55, 0], [x+.45, y+.55 if not opened else y+1.18, 0],
               color=color, stroke_width=7)
    return VGroup(posts, bar)


def route_test(revealed=False):
    scar = acquired_icons()[0].copy().scale(.8).move_to([-5.25, .9, 0])
    cards = gene_cards([-5.25, -1.05, 0], scale=.68, count=2, spacing=.38)
    top_gate = gate(RED if revealed else GREY, [-1.7, .9, 0])
    bottom_gate = gate(TEAL if revealed else GREY, [-1.7, -1.05, 0], opened=revealed)
    top_lane = RoundedRectangle(corner_radius=.28, width=7.0, height=1.35, stroke_width=0,
                                fill_color=GOLD, fill_opacity=.27).move_to([-1.15,.9,0])
    bot_lane = RoundedRectangle(corner_radius=.28, width=7.0, height=1.35, stroke_width=0,
                                fill_color=BLUE, fill_opacity=.27).move_to([-1.15,-1.05,0])
    top_path = VGroup(top_lane, Line([-4.55, .9, 0], [-2.25, .9, 0], color=GOLD, stroke_width=6))
    bot_path = VGroup(bot_lane, Line([-4.55, -1.05, 0], [-2.25, -1.05, 0], color=BLUE, stroke_width=6))
    baby = mouse([4.65, -.15, 0], scale=.70, young=True, scar=False, genes=False)
    q = question_card("Which path reaches the young?", y=-3.12, size=32)
    g = VGroup(top_path, bot_path, scar, cards, top_gate, bottom_gate, baby, q)
    g.scar, g.cards, g.top_gate, g.bottom_gate, g.baby, g.question = scar, cards, top_gate, bottom_gate, baby, q
    return g


def flower_head(center, color=GREY, scale=1.0):
    petals = VGroup()
    for r, n in ((0.0, 1), (.35, 7), (.67, 11)):
        for i in range(n):
            a = TAU * i / n
            c = np.array(center) + r * np.array([np.cos(a), np.sin(a), 0])
            petals.add(Circle(radius=.22, color=color, stroke_width=3,
                              fill_color=color, fill_opacity=.45).move_to(c))
    return petals.scale(scale)


def plant(center=ORIGIN, flower_color=GREY, scale=1.0, cards=True):
    """The carried plant/cutting picture used throughout the second half."""
    c = np.array(center, dtype=float)
    stem = Line(c + DOWN * 1.4, c + UP * 1.05, color=GREEN, stroke_width=8)
    leaves = VGroup(
        Ellipse(width=1.15, height=.5, color=GREEN, stroke_width=4,
                fill_color=GREEN, fill_opacity=.38).rotate(.35).move_to(c + LEFT*.58 + DOWN*.25),
        Ellipse(width=1.15, height=.5, color=GREEN, stroke_width=4,
                fill_color=GREEN, fill_opacity=.38).rotate(-.35).move_to(c + RIGHT*.58 + UP*.18),
    )
    roots = VGroup(*[Line(c + DOWN*1.35, c + DOWN*1.8 + RIGHT*x, color=SOIL, stroke_width=4)
                     for x in (-.55, -.25, .25, .55)])
    head = flower_head(c + UP*1.45, flower_color, .9)
    g = VGroup(roots, stem, leaves, head)
    g.head = head
    if cards:
        gc = gene_cards(c + LEFT*1.35 + DOWN*.95, scale=.50, count=2, spacing=.29)
        g.add(gc)
        g.cards = gc
    return g.scale(scale, about_point=c)


def environment_world():
    p = plant([0, -.1, 0], scale=1.2)
    ring = Circle(radius=2.75, color=GREEN, stroke_width=5,
                  fill_color=GREEN, fill_opacity=.16).move_to([0, .05, 0])
    soil = RoundedRectangle(corner_radius=.12, width=4.3, height=.68, color=SOIL, stroke_width=4,
                            fill_color=SOIL, fill_opacity=.28).move_to([0, -2.22, 0])
    sun = VGroup(Circle(radius=.42, color=GREEN, stroke_width=4),
                 *[Line(UP*.56, UP*.78, color=GREEN, stroke_width=3).rotate(i*PI/4, about_point=ORIGIN)
                   for i in range(8)]).move_to([-2.0, 1.95, 0])
    drop = VGroup(Circle(radius=.24, color=GREEN, fill_color=GREEN, fill_opacity=.2),
                  Triangle(color=GREEN, fill_color=GREEN, fill_opacity=.2).scale(.28).shift(UP*.27)).move_to([2.0, 1.95, 0])
    food = T("food", 28, GREEN).move_to([-2.15, -.65, 0])
    temp = VGroup(Line([2.0,-.8,0],[2.0,.0,0],color=GREEN,stroke_width=5),
                  Circle(radius=.22,color=GREEN,fill_color=GREEN,fill_opacity=.3).move_to([2.0,-.92,0]))
    return VGroup(ring, soil, p, sun, drop, food, temp)


def cutting_pair(left_color=GREY, right_color=GREY, soils=False):
    left = plant([-3.35, .15, 0], left_color, scale=.92)
    right = plant([3.35, .15, 0], right_color, scale=.92)
    g = VGroup(left, right)
    g.left, g.right = left, right
    if soils:
        sl = RoundedRectangle(corner_radius=.12, width=3.65, height=.75, color=GREEN, stroke_width=4,
                              fill_color=GREEN, fill_opacity=.13).move_to([-3.35,-2.0,0])
        sr = sl.copy().move_to([3.35,-2.0,0])
        g.add(sl, sr)
        g.soil_left, g.soil_right = sl, sr
    return g


def sway(mob, amp=.09, speed=3.2, seed=0):
    """A gentle continuous plant sway about its roots."""
    mob._sway_t = seed * .7
    mob._sway_a = 0.0
    pivot = mob.get_bottom().copy()

    def update(m, dt):
        m._sway_t += dt
        angle = amp * np.sin(speed * m._sway_t)
        m.rotate(angle - m._sway_a, about_point=pivot)
        m._sway_a = angle
    return mob.add_updater(update)


def flow(dots, start, end, speed=.35, seed=0.0):
    """Dots stream continuously from start to end and wrap, so a held shot keeps moving."""
    start=np.array(start,float); end=np.array(end,float)
    n=len(dots)
    dots._ft=seed
    def u(g,dt):
        g._ft+=dt*speed
        for i,d in enumerate(g):
            f=(g._ft+i/n)%1.0
            d.move_to(start+(end-start)*f)
    return dots.add_updater(u)


class S00Hook(SpokenScene):
    def construct(self):
        parent = mouse([-3.45, -.05, 0], scale=1.05, scar=False, genes=True)
        baby = mouse([4.65, -.35, 0], scale=.78, young=True, scar=False, genes=False)
        question = T("?", 120, GOLD, weight=BOLD).move_to([1.3, .85, 0])
        self.play(FadeIn(parent), FadeIn(baby), run_time=.8)
        bob(parent, amp=.11, speed=4.0)
        bob(baby, amp=.12, speed=4.5, seed=2)
        self.at("gain a scar")
        marked = mouse([-3.45, -.05, 0], scale=1.05, scar=True, genes=True)
        self.play(ReplacementTransform(parent, marked), run_time=.8)
        bob(marked, amp=.20, speed=5.2, seed=1)
        self.at("Why is a baby")
        self.play(FadeIn(question, scale=.5), run_time=.6)
        self.at("Follow the gold mark")
        self.play(Indicate(marked.scar, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.at("Then follow the blue")
        stream = marked.cards.copy()
        self.add(stream)
        self.play(stream.animate.move_to([1.25, -.55, 0]), run_time=1.8, rate_func=linear)
        self.play(stream.animate.move_to([3.3, -.45, 0]), run_time=1.2, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Inherited or acquired?"
    TITLE = "What Can Cross a Generation?"

    def construct(self):
        bg = VGroup(mouse([-4.9, -.8, 0], scale=.62, scar=True, genes=True),
                    mouse([5.0, -.9, 0], scale=.55, young=True, scar=False, genes=False),
                    gene_cards([2.8, -.75, 0], scale=.4, count=3, spacing=.25)).set_opacity(.18)
        self.add(bg)
        super().construct()


class S02TwoSources(SpokenScene):
    def construct(self):
        parent = mouse([-4.6, 0, 0], scale=.72, scar=True, genes=True)
        young = mouse([4.9, 1.35, 0], scale=.52, young=True, scar=False, genes=False)
        inherited = Arrow([-2.65,.65,0], [3.55,1.28,0], color=TEAL, stroke_width=7, tip_length=.28)
        acquired = ArcBetweenPoints([-2.7,-.55,0], [2.7,-1.65,0], angle=.15, color=GOLD, stroke_width=7)
        self.play(FadeIn(parent), FadeIn(young), run_time=.7)
        bob(parent, amp=.11, speed=4.0)
        bob(young, amp=.12, speed=4.5, seed=2)
        self.at("passes from parent")
        self.play(GrowArrow(inherited), run_time=1.0)
        self.at("through genes")
        gl = T("inherited", 36, BLUE, weight=BOLD).move_to([.2,1.42,0])
        self.play(FadeIn(gl), run_time=.4)
        self.at("develops during life")
        self.play(Create(acquired), run_time=1.0)
        al = T("acquired", 36, GOLD, weight=BOLD).move_to([.1,-.55,0])
        self.play(FadeIn(al), run_time=.4)
        self.at("Eye color")
        eye = eye_icon([3.9, 2.45, 0])
        self.play(FadeIn(eye, scale=.7), run_time=.6)
        self.at("A scar")
        icons = acquired_icons().move_to([2.35,-2.25,0])
        self.play(LaggedStart(*[FadeIn(i, shift=UP*.12) for i in icons], lag_ratio=.18), run_time=2.3)
        self.at("These labels describe")
        self.play(Indicate(VGroup(parent, young), color=TEXT, scale_factor=1.025), run_time=1.1)
        self.at("not whether genes")
        self.play(Indicate(VGroup(gl, al), color=TEXT, scale_factor=1.04), run_time=1.0)
        self.finish()


class S03CellMap(SpokenScene):
    def construct(self):
        world = cell_map(with_young=True)
        self.play(FadeIn(world.skin), FadeIn(world.muscle), FadeIn(world.sex), run_time=1.0)
        bob(world.skin, amp=.10, speed=4.0)
        bob(world.muscle, amp=.11, speed=4.5, seed=2)
        bob(world.sex, amp=.10, speed=5.0, seed=4)
        self.at("offspring begin from sex cells")
        self.play(GrowArrow(world.route), FadeIn(world.baby), run_time=1.2)
        bob(world.baby, amp=.11, speed=4.3, seed=1)
        self.at("Those cells carry")
        self.play(Indicate(world.sex[1], color=BLUE, scale_factor=1.12), run_time=.9)
        self.at("Skin cells can heal")
        ripple1 = Circle(radius=.25, color=GOLD).move_to(world.skin[1])
        self.play(ripple1.animate.scale(4).set_opacity(0), run_time=1.2)
        self.remove(ripple1)
        self.at("Muscle cells can grow")
        self.play(world.muscle[1].animate.scale([1.15,1.25,1]), run_time=1.1)
        self.at("Those body cell changes")
        ripples = VGroup(Circle(radius=.3,color=GOLD).move_to(world.skin),
                         Circle(radius=.3,color=GOLD).move_to(world.muscle))
        self.play(*[r.animate.scale(3.2).set_opacity(0) for r in ripples], run_time=1.3)
        self.at("do not change the genes")
        self.play(Indicate(world.sex[1], color=BLUE, scale_factor=1.08), run_time=1.0)
        self.at("inside the sex cells")
        self.play(world.route.animate.set_stroke(width=10), run_time=.8, rate_func=there_and_back)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = route_test()
        self.play(FadeIn(world.scar), FadeIn(world.cards), run_time=.7)
        bob(world.scar, amp=.12, speed=4.2)
        bob(world.cards, amp=.12, speed=4.7, seed=2)
        self.at("beside different paths")
        self.play(Create(world[0]), Create(world[1]), FadeIn(world.top_gate), FadeIn(world.bottom_gate),
                  FadeIn(world.baby), run_time=1.2)
        bob(world.baby, amp=.22, speed=5.5, seed=1)
        self.at("Which path can reach")
        self.play(FadeIn(world.question), run_time=.6)
        self.at("Keep watching both")
        self.wait(1.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which path reaches the young?"
    SECONDS = 4.5

    def backdrop(self):
        w = route_test()
        bob(w.scar, amp=.12, speed=4.2)
        bob(w.cards, amp=.12, speed=4.7, seed=2)
        bob(w.baby, amp=.22, speed=5.5, seed=1)
        return VGroup(*w[:-1])


class S06Reveal(SpokenScene):
    def construct(self):
        world = route_test()
        self.add(*world[:-1])
        bob(world.baby, amp=.22, speed=5.5, seed=1)
        open_gate = gate(TEAL, [-1.7,-1.05,0], opened=True)
        self.at("blue cards pass")
        self.play(ReplacementTransform(world.bottom_gate, open_gate), run_time=.6)
        self.play(world.cards.animate.move_to([1.0,-1.05,0]), run_time=1.0, rate_func=linear)
        self.at("continue into the young")
        self.play(world.cards.animate.move_to([4.4,-.45,0]).scale(.7), run_time=1.2, rate_func=linear)
        self.at("scar reaches a red stop")
        red_gate = gate(RED, [-1.7,.9,0])
        stop = Cross(Square(.52), stroke_color=RED, stroke_width=7).move_to([-2.45,.9,0])
        self.play(ReplacementTransform(world.top_gate, red_gate), world.scar.animate.move_to([-2.95,.9,0]),
                  Create(stop), run_time=1.1)
        self.at("Gene coded traits")
        rule = caption("Gene-coded traits can pass on; ordinary changes gained during life cannot.",
                       size=28, color=TEXT)
        self.play(FadeIn(rule, shift=UP*.12), run_time=.7)
        self.at("Ordinary changes")
        self.play(Indicate(VGroup(world.scar, stop), color=RED, scale_factor=1.05), run_time=1.0)
        self.at("Ordinary means body changes")
        self.play(world.scar.animate.shift(UP*.08), run_time=.7, rate_func=there_and_back)
        self.at("shown here")
        self.play(FadeOut(rule), run_time=.6)
        self.finish()


class S07Environment(SpokenScene):
    def construct(self):
        world = environment_world()
        plant_obj = world[2]
        self.play(FadeIn(plant_obj), run_time=.7)
        bob(plant_obj, amp=.22, speed=5.5)
        self.at("environment is everything")
        self.play(Create(world[0]), run_time=1.1)
        env_label = T("environment", 34, GREEN, weight=BOLD).move_to([0,3.15,0])
        self.play(FadeIn(env_label), run_time=.4)
        self.at("Soil")
        self.play(FadeIn(world[1], shift=UP*.15), run_time=.5)
        self.at("light")
        self.play(FadeIn(world[3], scale=.7), run_time=.45)
        world[3].add_updater(lambda m, dt: m.rotate(.65 * dt))
        self.at("water")
        self.play(FadeIn(world[4], shift=UP*.15), run_time=.45)
        self.at("food")
        self.play(FadeIn(world[5]), run_time=.4)
        self.at("temperature")
        self.play(FadeIn(world[6]), run_time=.5)
        self.at("Genes and environment")
        self.play(Indicate(VGroup(plant_obj.cards, world[0]), color=TEAL, scale_factor=1.04), run_time=1.0)
        self.at("shape the phenotype")
        phenotype = T("phenotype", 30, TEXT).move_to([4.15,2.45,0])
        arrow = Arrow([3.35,2.2,0], [1.45,1.55,0], buff=0, color=TEXT, stroke_width=4, tip_length=.22)
        self.play(GrowArrow(arrow), FadeIn(phenotype), plant_obj.head.animate.set_stroke(BLUE), run_time=1.1)
        self.finish()


class S08Variation(SpokenScene):
    def construct(self):
        plants = VGroup(plant([-4.5,-.25,0], BLUE, .72), plant([-1.5,-.25,0], PINK, .86),
                        plant([1.5,-.25,0], BLUE, 1.0), plant([4.5,-.25,0], PINK, .78))
        self.play(LaggedStart(*[FadeIn(p, shift=UP*.2) for p in plants], lag_ratio=.15), run_time=1.4)
        for i, p in enumerate(plants):
            bob(p, amp=.10 + .01*i, speed=4.0 + .35*i, seed=i)
        self.at("differences among living things")
        self.play(plants[0].animate.scale(.92), plants[2].animate.scale(1.08), run_time=1.0)
        self.at("inherited alleles")
        self.play(Indicate(VGroup(plants[0].cards, plants[2].cards), color=BLUE, scale_factor=1.08), run_time=1.0)
        self.at("environments differ")
        rings = VGroup(*[Circle(radius=1.35, color=GREEN, stroke_width=3).move_to(p.get_center()+UP*.15) for p in plants[1::2]])
        self.play(Create(rings), run_time=1.0)
        self.at("Many traits reflect both")
        overlap = VGroup(Circle(radius=1.45,color=BLUE,fill_color=BLUE,fill_opacity=.09).shift(LEFT*.62),
                         Circle(radius=1.45,color=GREEN,fill_color=GREEN,fill_opacity=.09).shift(RIGHT*.62)).move_to([0,1.85,0])
        self.play(FadeOut(rings), FadeIn(overlap), run_time=1.0)
        self.at("Matching gene sets")
        self.play(Indicate(VGroup(*[p.cards for p in plants]), color=BLUE, scale_factor=1.05), run_time=1.1)
        self.at("different surroundings")
        self.play(plants[1].animate.shift(UP*.12), plants[3].animate.shift(DOWN*.12), run_time=1.2)
        self.at("different visible results")
        self.play(plants[0].head.animate.set_fill(BLUE,.55), plants[1].head.animate.set_fill(PINK,.55),
                  plants[2].head.animate.set_fill(BLUE,.55), plants[3].head.animate.set_fill(PINK,.55), run_time=1.1)
        self.at("tracing a cause")
        trace = Arrow([-2.4,-2.85,0], [2.4,-2.85,0], color=TEAL, stroke_width=7, tip_length=.3)
        self.play(GrowArrow(trace), run_time=1.0)
        self.at("genes only box")
        boxes = VGroup(chip("genes only", BLUE, 28), chip("environment only", GREEN, 28)).arrange(RIGHT,buff=.55).move_to([0,-2.7,0])
        self.play(FadeOut(trace), FadeIn(boxes), run_time=.8)
        self.at("environment only box")
        self.play(FadeOut(boxes[0], shift=LEFT*1.5), FadeOut(boxes[1], shift=RIGHT*1.5), run_time=1.0)
        tag = scope_tag("flower differences schematic", size=24)
        self.play(FadeIn(tag), run_time=.4)
        self.finish()


class S09Hydrangea(SpokenScene):
    def construct(self):
        pair = cutting_pair(GREY, GREY, soils=True)
        self.play(FadeIn(pair), run_time=.9)
        bob(pair.left, amp=.11, speed=4.0)
        bob(pair.right, amp=.12, speed=4.5, seed=2)
        sway(pair.left, seed=0)
        sway(pair.right, seed=2)
        self.at("blue gene cards stay the same")
        self.play(Indicate(VGroup(pair.left.cards, pair.right.cards), color=BLUE, scale_factor=1.08), run_time=1.0)
        self.at("acidic soil")
        pulse_ring = Circle(radius=.5, color=GREEN, stroke_width=4).move_to(pair.right.head.get_center())
        pulse_ring._t = 0.0
        def _ring(m, dt):
            m._t += dt
            f = (m._t * .5) % 1.0
            m.set_width(.8 + 1.4 * f).move_to(pair.right.head.get_center()).set_stroke(opacity=.7 * (1 - f))
        pulse_ring.add_updater(_ring)
        self.add(pulse_ring)
        acidic = T("acidic soil", 30, GREEN).move_to([-3.35,-2.65,0])
        less = T("less acidic soil", 30, GREEN).move_to([3.35,-2.65,0])
        self.play(FadeIn(acidic), FadeIn(less), run_time=.7)
        self.at("take up more aluminum")
        dots = VGroup(*[Dot([-4.05+i*.28,-1.9,0], radius=.08, color=TEXT) for i in range(6)])
        al = T("aluminum", 26, TEXT).move_to([-5.25,-1.25,0])
        self.play(FadeIn(dots), FadeIn(al), run_time=.5)
        self.play(dots.animate.move_to([-3.35,-.25,0]), run_time=1.3)
        flow(dots, [-3.35,-1.9,0], [-3.35,.6,0], speed=.3)
        self.at("flowers become blue")
        self.play(pair.left.head.animate.set_stroke(BLUE).set_fill(BLUE,.5), run_time=1.2)
        self.at("give pink flowers")
        self.play(pair.right.head.animate.set_stroke(PINK).set_fill(PINK,.5), run_time=1.2)
        self.at("soil changes the phenotype")
        self.play(Indicate(VGroup(pair.soil_left, pair.left.head, pair.soil_right, pair.right.head),
                           color=GREEN, scale_factor=1.03), run_time=1.0)
        self.at("not the cutting's genes")
        self.play(Indicate(VGroup(pair.left.cards, pair.right.cards), color=BLUE, scale_factor=1.08), run_time=1.0)
        self.add(scope_tag("color response is schematic", size=24))
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        pair = cutting_pair(BLUE, PINK, soils=True)
        self.add(pair)
        bob(pair.left, amp=.11, speed=4.0)
        bob(pair.right, amp=.12, speed=4.5, seed=2)
        sway(pair.left, seed=0)
        sway(pair.right, seed=2)
        possible = VGroup(flower_head([-1.0,2.65,0], BLUE, .42), flower_head([1.0,2.65,0], PINK, .42))
        bracket = SurroundingRectangle(possible, color=BLUE, buff=.25, corner_radius=.12)
        self.at("colors are possible")
        self.play(FadeIn(possible), Create(bracket), run_time=.9)
        self.at("soil helps decide")
        arrows = VGroup(Arrow([-3.35,-1.65,0],[-3.35,1.35,0],color=GREEN,stroke_width=5,tip_length=.24),
                        Arrow([3.35,-1.65,0],[3.35,1.35,0],color=GREEN,stroke_width=5,tip_length=.24))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=1.0)
        self.at("matching genes")
        self.play(Indicate(VGroup(pair.left.cards,pair.right.cards),color=BLUE,scale_factor=1.08),run_time=1.0)
        self.at("matching phenotypes")
        self.play(Indicate(VGroup(pair.left.head,pair.right.head),color=TEXT,scale_factor=1.06),run_time=1.0)
        self.at("Phenotype tells what appears")
        phen = T("phenotype = what appears", 30, TEXT).move_to([0,-2.9,0])
        self.play(FadeIn(phen), run_time=.6)
        self.at("First trace the cause")
        self.play(FadeOut(phen), arrows.animate.set_color(TEAL), run_time=.8)
        self.at("enter the gene route")
        route = Arrow([-1.2,-1.25,0],[5.65,-1.25,0],color=TEAL,stroke_width=7,tip_length=.3)
        seed = Circle(radius=.32,color=TEAL,fill_color=TEAL,fill_opacity=.18).move_to([5.95,-1.25,0])
        self.play(GrowArrow(route), FadeIn(seed), run_time=1.1)
        rd = VGroup(*[Dot(radius=.09, color=TEAL) for _ in range(6)])
        self.add(rd)
        flow(rd, [-1.2,-1.25,0], [5.65,-1.25,0], speed=.25)
        self.at("to offspring")
        self.play(pair.left.cards.copy().animate.move_to([5.9,-1.25,0]).scale(.65), run_time=1.1)
        self.finish()


class S11End(EndCard):
    LINE = "Gene-coded traits can pass on; ordinary changes gained during life cannot."
