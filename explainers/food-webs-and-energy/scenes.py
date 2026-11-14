"""Follow the Energy Arrows — Chesapeake Bay food-web explainer.

COLOR MAP (organisms keep their own colour; colour never encodes consumer order)
  GOLD   sunlight and stored energy
  GREEN  phytoplankton
  BLUE   zooplankton and water
  ORANGE menhaden
  PURPLE osprey
  TEAL   larger fish
  GREY   decomposers, matter, and neutral structure
  RED    heat
"""
from bp_parts import *  # noqa: F401,F403


ENERGY = GOLD
PHY = GREEN
ZOO = BLUE
MEN = ORANGE
OSP = PURPLE
BIG = TEAL
DEC = GREY
HEAT = RED


def fish_icon(color=MEN, scale=1.0, direction=1):
    """A labelled-cartoon-free fish silhouette, not an anatomical drawing."""
    body = Ellipse(width=1.35, height=0.62, color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.32)
    tail = Polygon([-.58, 0, 0], [-1.08, .43, 0], [-1.08, -.43, 0],
                   color=color, stroke_width=4, fill_color=color, fill_opacity=0.25)
    eye = Dot([.38, .11, 0], radius=.045, color=TEXT)
    g = VGroup(tail, body, eye)
    if direction < 0:
        g.flip(UP)
    return g.scale(scale)


def osprey_icon(scale=1.0):
    wings = Polygon([-1.05, 0, 0], [-.35, .48, 0], [0, .12, 0],
                    [.35, .48, 0], [1.05, 0, 0], [0, -.30, 0],
                    color=OSP, stroke_width=4, fill_color=OSP, fill_opacity=.28)
    body = Ellipse(width=.52, height=.82, color=OSP, stroke_width=4,
                   fill_color=OSP, fill_opacity=.35).rotate(-.10)
    beak = Polygon([.15, .38, 0], [.55, .25, 0], [.20, .12, 0],
                   color=ENERGY, fill_color=ENERGY, fill_opacity=.75)
    return VGroup(wings, body, beak).scale(scale)


def phytoplankton_icon(scale=1.0):
    pts = [(-.45, .18), (-.12, .42), (.28, .34), (.47, .02), (.12, -.35), (-.32, -.27)]
    return VGroup(*[Circle(radius=.18, color=PHY, stroke_width=3,
                          fill_color=PHY, fill_opacity=.38).move_to([x, y, 0])
                    for x, y in pts]).scale(scale)


def zooplankton_icon(scale=1.0):
    bodies = VGroup(*[Ellipse(width=.48, height=.25, color=ZOO, stroke_width=3,
                             fill_color=ZOO, fill_opacity=.35).move_to(p)
                      for p in ((-.35, .24, 0), (.20, .10, 0), (-.05, -.28, 0))])
    feelers = VGroup(Line([-.56, .30, 0], [-.82, .48, 0], color=ZOO, stroke_width=2),
                     Line([.42, .16, 0], [.72, .35, 0], color=ZOO, stroke_width=2))
    return VGroup(bodies, feelers).scale(scale)


def packet(radius=.16):
    return Dot(radius=radius, color=ENERGY).set_stroke(ENERGY, 4)


def water_field():
    water = Rectangle(width=13.2, height=5.8, color=ZOO, stroke_width=2,
                      fill_color=ZOO, fill_opacity=.14).move_to([0, -.35, 0])
    waves = VGroup()
    for j, y in enumerate((2.28, 1.82)):
        points = []
        for x in np.linspace(-6.4, 6.4, 90):
            points.append([x, y + .07 * np.sin(2.2 * x + j), 0])
        w = VMobject(color=ZOO, stroke_width=3, stroke_opacity=.55)
        w.set_points_as_corners(points)
        waves.add(w)
    pulse(waves, base=2.0, amp=.8, speed=1.4)
    bob(waves[0], amp=.13, speed=1.05, seed=0)
    bob(waves[1], amp=.10, speed=1.27, seed=1)
    current = VGroup()
    for i in range(18):
        d = Dot([-6.1 + (i % 9) * 1.45, -2.35 + (i // 9) * 3.55 + .12 * (i % 3), 0],
                radius=.070, color=ZOO).set_opacity(.48)
        d.v = .22 + .025 * (i % 4)

        def drift(mob, dt):
            mob.shift(RIGHT * mob.v * dt)
            if mob.get_x() > 6.35:
                mob.shift(LEFT * 12.7)
        d.add_updater(drift)
        current.add(d)
    floor = Line([-6.5, -3.02, 0], [6.5, -3.02, 0], color=DEC, stroke_width=4)
    return VGroup(water, waves, current, floor)


def bay_world(labels=False, include_big=False):
    """The one carried Chesapeake world, rebuilt at identical coordinates."""
    water = water_field()
    sun = Circle(radius=.42, color=ENERGY, stroke_width=4, fill_color=ENERGY,
                 fill_opacity=.45).move_to([-5.65, 3.02, 0])
    rays = VGroup(*[Line(sun.get_center() + .55 * v, sun.get_center() + 1.0 * v,
                         color=ENERGY, stroke_width=4)
                    for v in (DOWN, DR, RIGHT)])
    phy = phytoplankton_icon(1.05).move_to([-4.15, 1.35, 0])
    zoo = zooplankton_icon(1.15).move_to([-2.15, .15, 0])
    men = VGroup(*[fish_icon(MEN, .72).move_to([-.15 + .80 * (i % 2),
                                                .55 - .62 * (i // 2), 0])
                   for i in range(4)])
    osp = osprey_icon(.86).move_to([4.65, 2.25, 0])
    dec = VGroup(*[Dot([x, -2.62 + .10 * np.sin(3 * x), 0], radius=.09, color=DEC)
                   for x in np.linspace(-3.5, 3.3, 18)])
    big = fish_icon(BIG, 1.05, -1).move_to([4.05, -.75, 0])
    g = VGroup(water, sun, rays, phy, zoo, men, osp, dec)
    if include_big:
        g.add(big)
    g.water, g.sun, g.rays = water, sun, rays
    g.phy, g.zoo, g.men, g.osp, g.dec, g.big = phy, zoo, men, osp, dec, big
    if labels:
        labs = VGroup(T("phytoplankton", 28, PHY).next_to(phy, UP, buff=.14),
                      T("zooplankton", 28, ZOO).next_to(zoo, DOWN, buff=.12),
                      T("menhaden", 28, MEN).next_to(men, DOWN, buff=.12),
                      T("osprey", 28, OSP).next_to(osp, UP, buff=.12))
        if include_big:
            labs.add(T("larger fish", 28, BIG).next_to(big, DOWN, buff=.12))
        g.add(labs)
        g.labels = labs
    return g


CHAIN_X = (-4.8, -1.6, 1.6, 4.8)
CHAIN_Y = .40


def double_dashed(a, b):
    line = DashedLine(a, b, color=DEC, stroke_width=5, dash_length=.15)
    u = (np.array(b) - np.array(a)) / np.linalg.norm(np.array(b) - np.array(a))
    left = Triangle(color=DEC, fill_color=DEC, fill_opacity=1).scale(.14).rotate(-PI / 2)
    right = Triangle(color=DEC, fill_color=DEC, fill_opacity=1).scale(.14).rotate(PI / 2)
    left.move_to(np.array(a) + .18 * u)
    right.move_to(np.array(b) - .18 * u)
    return VGroup(line, left, right)


def chain_world(doubles=False, arrows=False, names=False, moving=True):
    """The carried chain used without positional drift in s04–s07."""
    bg = water_field()
    icons = [phytoplankton_icon(1.22), zooplankton_icon(1.35),
             fish_icon(MEN, 1.15), osprey_icon(.92)]
    for icon, x in zip(icons, CHAIN_X):
        icon.move_to([x, CHAIN_Y, 0])
    if moving:
        for i, icon in enumerate(icons):
            bob(icon, amp=.035 + .008 * i, speed=1.2 + .15 * i, seed=i)
    g = VGroup(bg, *icons)
    g.bg, g.phy, g.zoo, g.men, g.osp = bg, *icons
    links = VGroup()
    for i in range(3):
        a = [CHAIN_X[i] + 1.0, CHAIN_Y, 0]
        b = [CHAIN_X[i + 1] - 1.0, CHAIN_Y, 0]
        if doubles:
            links.add(double_dashed(a, b))
        elif arrows:
            links.add(Arrow(a, b, buff=0, color=ENERGY, stroke_width=8, tip_length=.24))
    if len(links):
        g.add(links)
    g.links = links
    if names:
        labels = VGroup(*[T(n, 28, c).move_to([x, -1.03, 0])
                          for n, c, x in zip(("phytoplankton", "zooplankton", "menhaden", "osprey"),
                                             (PHY, ZOO, MEN, OSP), CHAIN_X)])
        g.add(labels)
        g.labels = labels
    return g


def web_arrows(world, color=ENERGY, width=6):
    """Food-to-eater links in the fixed Bay geometry."""
    p, z, m, o, b = (world.phy.get_center(), world.zoo.get_center(), world.men.get_center(),
                      world.osp.get_center(), world.big.get_center())
    return VGroup(
        CurvedArrow(p + RIGHT * .55, z + LEFT * .45, angle=-.18, color=color, stroke_width=width),
        CurvedArrow(z + RIGHT * .48, m + LEFT * .55, angle=.14, color=color, stroke_width=width),
        CurvedArrow(m + UR * .38, o + DL * .62, angle=-.18, color=color, stroke_width=width),
        CurvedArrow(p + DR * .35, m + UL * .48, angle=.22, color=color, stroke_width=width),
        CurvedArrow(m + RIGHT * .55, b + LEFT * .72, angle=-.18, color=color, stroke_width=width),
    )


def web_world(with_arrows=True):
    w = bay_world(include_big=True)
    arrs = web_arrows(w) if with_arrows else VGroup()
    w.add(arrs)
    w.arrows = arrs
    return w


class S00Hook(SpokenScene, TitleCard):
    LESSON = "Food webs and energy"
    TITLE = "Follow the Energy Arrows"

    def construct(self):
        world = bay_world()
        caught = fish_icon(MEN, .78).move_to([4.65, 1.38, 0])
        world.osp.move_to([4.65, 2.55, 0])
        self.at("An osprey lifts")
        self.play(FadeIn(world, lag_ratio=.03), run_time=.9)
        self.play(FadeIn(caught), caught.animate.shift(UP * .42),
                  world.osp.animate.shift(UP * .18), run_time=1.2)
        glow = packet(.18).move_to(caught.get_center())
        question = fit_text("Where did this energy begin?", max_w=7.7, size=40,
                            color=ENERGY, font=TITLE_FONT).move_to([-.35, 2.92, 0])
        self.at("Where did the energy")
        self.play(FadeIn(glow, scale=.4), Write(question), run_time=1.1)
        self.play(Indicate(glow, color=ENERGY, scale_factor=1.7), run_time=.8)
        trail_path = CurvedArrow(caught.get_center() + LEFT * .25,
                                 world.phy.get_center() + RIGHT * .25,
                                 angle=.35, color=ENERGY, stroke_width=5)
        trail = DashedVMobject(trail_path, num_dashes=18)
        self.at("Follow one glowing")
        self.play(Create(trail), run_time=2.2, rate_func=linear)
        self.play(MoveAlongPath(glow, trail_path), run_time=1.8, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Food webs and energy"
    TITLE = "Follow the Energy Arrows"

    def construct(self):
        world = bay_world()
        bob(world.men, amp=.04, speed=1.3)
        band = Rectangle(width=13.4, height=1.65, fill_color=BG, fill_opacity=.82,
                         stroke_width=0)
        title = T(self.TITLE, 54, font=TITLE_FONT)
        self.add(world)
        self.play(FadeIn(band), Write(title), run_time=.7)
        self.wait(.7)
        self.play(FadeOut(band), FadeOut(title), run_time=.6)
        self.finish()


class S02World(SpokenScene):
    def construct(self):
        world = bay_world()
        self.add(world)
        border = RoundedRectangle(corner_radius=.18, width=12.7, height=6.55,
                                  color=TEXT, stroke_width=4)
        eco = T("ecosystem", 38, TEXT).move_to([-4.9, 3.42, 0])
        eco.add_background_rectangle(BG, opacity=.9, buff=.12)
        eco.layout_ok = True  # intended label tab on the ecosystem bracket
        self.at("The bay is an ecosystem")
        self.play(Create(border), FadeIn(eco), run_time=1.1)
        self.play(Indicate(VGroup(world.phy, world.zoo, world.men, world.water),
                           color=TEXT, scale_factor=1.02), run_time=1.0)
        thermo = VGroup(Line([4.95, -.9, 0], [4.95, .65, 0], color=HEAT, stroke_width=10),
                        Circle(radius=.24, color=HEAT, fill_color=HEAT, fill_opacity=.75)
                        .move_to([4.95, -1.05, 0]))
        abiotic = chip("abiotic", ENERGY, size=32).move_to([3.85, 1.48, 0])
        abiotic.layout_ok = True
        self.at("Light water and temperature")
        self.play(FadeIn(thermo, shift=UP * .2), Indicate(world.sun, color=ENERGY),
                  Indicate(world.water, color=ZOO), run_time=1.1)
        self.play(FadeIn(abiotic), run_time=.6)
        feather = Arc(radius=.34, start_angle=-1.1, angle=2.2, color=OSP,
                      stroke_width=5).move_to([3.55, -.55, 0])
        waste = Dot([2.75, -1.1, 0], radius=.13, color=DEC)
        biotic = chip("biotic", PHY, size=32).move_to([3.55, -.05, 0])
        biotic.layout_ok = True
        self.at("Organisms their parts")
        self.play(FadeOut(thermo), FadeOut(abiotic), FadeIn(feather), FadeIn(waste),
                  Indicate(VGroup(world.phy, world.zoo, world.men, world.osp), color=PHY),
                  run_time=1.2)
        self.play(FadeIn(biotic), run_time=.6)
        self.at("A change in either kind")
        self.play(Indicate(border, color=ENERGY, scale_factor=.98),
                  world.men.animate.shift(RIGHT * .30), run_time=1.3)
        self.finish()


class S03Source(SpokenScene):
    def construct(self):
        world = bay_world()
        self.add(world)
        trail = DashedVMobject(CurvedArrow(world.men.get_center(), world.sun.get_center(),
                                          angle=-.35, color=ENERGY, stroke_width=5), num_dashes=18)
        self.at("The trail ends")
        self.play(Create(trail), run_time=1.5)
        self.play(FadeOut(trail), world.phy.animate.scale(2.1).move_to([0, .35, 0]),
                  FadeOut(VGroup(world.zoo, world.men, world.osp)), run_time=1.2)
        producer = T("producer", 34, PHY).move_to([0, -1.28, 0])
        self.at("They are producers")
        self.play(FadeIn(producer, shift=UP * .15), run_time=.7)
        ray = Arrow([-4.85, 2.65, 0], [-.85, .80, 0], buff=0, color=ENERGY,
                    stroke_width=9, tip_length=.25)
        store = chip("stored food", ENERGY, size=30).move_to([.20, .36, 0])
        store.layout_ok = True
        self.at("That stored energy")
        self.play(GrowArrow(ray), run_time=.9)
        self.play(FadeIn(store, scale=.6), run_time=.7)
        self.play(Indicate(store, color=ENERGY, scale_factor=1.12), run_time=.8)
        nearby = VGroup(*[phytoplankton_icon(.56).move_to(p)
                          for p in ((-3.0, 1.25, 0), (2.7, 1.20, 0), (3.2, -.55, 0))])
        for i, p in enumerate(nearby):
            bob(p, amp=.05, speed=1.25, seed=i)
        self.at("Most ecosystems need")
        self.play(FadeIn(nearby, lag_ratio=.18), run_time=.9)
        self.play(Indicate(ray, color=ENERGY, scale_factor=1.03), run_time=.8)
        self.finish()


class S04Path(SpokenScene):
    def construct(self):
        world = chain_world(names=True, moving=False)
        self.add(world.bg)
        self.at("A zooplankton eats")
        self.play(FadeIn(world.phy), FadeIn(world.zoo), FadeIn(world.labels[:2]), run_time=.8)
        p = packet().move_to(world.phy)
        self.add(p)
        self.play(world.zoo.animate.shift(LEFT * .32), p.animate.move_to(world.zoo), run_time=.9)
        self.play(world.zoo.animate.shift(RIGHT * .32), run_time=.35)
        self.at("A menhaden eats")
        self.play(FadeIn(world.men), FadeIn(world.labels[2]), run_time=.45)
        self.play(world.men.animate.shift(LEFT * .35), p.animate.move_to(world.men), run_time=.9)
        self.play(world.men.animate.shift(RIGHT * .35), run_time=.35)
        self.at("An osprey catches")
        self.play(FadeIn(world.osp), FadeIn(world.labels[3]), run_time=.45)
        self.play(world.osp.animate.shift(LEFT * .35), p.animate.move_to(world.osp), run_time=.9)
        self.play(world.osp.animate.shift(RIGHT * .35), run_time=.35)
        self.at("Each eater receives")
        self.play(Indicate(VGroup(world.zoo, world.men, world.osp), color=ENERGY,
                           scale_factor=1.08), run_time=1.1)
        self.at("The packet changes location")
        path = VMobject().set_points_as_corners([[x, CHAIN_Y, 0] for x in CHAIN_X])
        self.play(MoveAlongPath(p, path), run_time=2.0, rate_func=linear)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = chain_world(doubles=True, moving=True)
        self.add(world.bg, world.phy, world.zoo, world.men, world.osp)
        p = packet(.18).move_to(world.phy)
        pulse(p, base=4, amp=2, speed=3)
        self.add(p)
        self.at("The arrows are missing")
        self.play(LaggedStart(*[Create(a) for a in world.links], lag_ratio=.18), run_time=1.2)
        q = question_card("Which way does energy move?", ["toward the food", "toward the eater"],
                          y=-2.65, size=34, chip_size=28)
        q.question.layout_ok = True  # intended text over the water/background floor band
        self.at("If each arrow shows")
        self.play(FadeIn(q.chips), run_time=.7)
        self.play(FadeIn(q.question), run_time=.7)
        self.at("Choose before anything moves")
        self.play(Indicate(q.chips, color=ENERGY, scale_factor=1.03), run_time=.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which way does energy move?"
    OPTIONS = ["toward the food", "toward the eater"]
    CARD = {"y": -2.65, "size": 34, "chip_size": 28}
    RING_AT = (6.0, -2.7, 0)
    SECONDS = 4.5

    def backdrop(self):
        world = chain_world(doubles=True, moving=True)
        p = packet(.18).move_to(world.phy)
        pulse(p, base=4, amp=2, speed=3)
        return VGroup(world, p)

    def construct(self):
        self.add(self.backdrop())
        q = question_card(self.QUESTION, self.OPTIONS, y=-2.65, size=34, chip_size=28)
        q.question.layout_ok = True  # same designed bottom-band overlay as s05
        self.add(q)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        world = chain_world(arrows=True, moving=False)
        self.add(world.bg, world.phy, world.zoo, world.men, world.osp)
        self.at("Arrows point from food")
        self.play(LaggedStart(*[GrowArrow(a) for a in world.links], lag_ratio=.16), run_time=1.2)
        p = packet(.18).move_to(world.phy)
        self.add(p)
        route = VMobject().set_points_as_corners([[x, CHAIN_Y, 0] for x in CHAIN_X])
        self.play(MoveAlongPath(p, route), run_time=2.2, rate_func=linear)
        label = chip("one food chain", ENERGY, size=34).move_to([0, -1.55, 0])
        label.layout_ok = True
        self.at("This straight route")
        self.play(FadeIn(label, shift=UP * .15), run_time=.7)
        outline = RoundedRectangle(corner_radius=.20, width=12.4, height=2.55,
                                   color=ENERGY, stroke_width=5).move_to([0, .35, 0])
        self.at("It is one path")
        self.play(FadeIn(Rectangle(width=13.3, height=5.8, color=BG, fill_color=BG,
                                   fill_opacity=.25, stroke_width=0).move_to([0, -.35, 0])),
                  Create(outline), run_time=.9)
        self.play(ShowPassingFlash(outline.copy().set_stroke(width=12), time_width=.45),
                  run_time=2.0)
        self.at("Read every arrow")
        reread = packet(.15).move_to(world.phy)
        self.add(reread)
        self.play(MoveAlongPath(reread, route), run_time=3.0, rate_func=linear)
        self.finish()


class S08Web(SpokenScene):
    def construct(self):
        world = web_world(with_arrows=False)
        world.remove(world.big)
        self.add(world)
        base = web_arrows(world)[:3]
        self.add(base)
        chain_label = chip("food chain", ENERGY, size=32).move_to([0, -2.35, 0])
        chain_label.layout_ok = True
        self.add(chain_label)
        self.at("Menhaden can also eat")
        direct = web_arrows(world)[3]
        self.play(Create(direct), run_time=1.1)
        p1 = packet(.14).move_to(world.phy)
        self.add(p1)
        self.play(MoveAlongPath(p1, direct.copy()), run_time=1.1, rate_func=linear)
        self.at("Larger fish can eat")
        to_big = web_arrows(world)[4]
        self.play(FadeIn(world.big), Create(to_big), run_time=1.0)
        p2 = packet(.14).move_to(world.men)
        self.add(p2)
        self.play(MoveAlongPath(p2, to_big.copy()), run_time=1.0, rate_func=linear)
        self.at("New arrows join")
        self.play(Indicate(VGroup(base, direct, to_big), color=ENERGY, scale_factor=1.02), run_time=.9)
        web_label = chip("food web", ENERGY, size=36).move_to(chain_label)
        web_label.layout_ok = True
        self.at("Linked food chains")
        self.play(swap(chain_label, web_label), run_time=.8)
        self.at("That web reveals")
        self.play(world.zoo.animate.shift(DOWN * .20),
                  world.men.animate.shift(RIGHT * .22), run_time=1.0)
        self.play(world.zoo.animate.shift(UP * .20), world.men.animate.shift(LEFT * .22),
                  run_time=.7)
        self.finish()


class S09Orders(SpokenScene):
    def construct(self):
        world = web_world()
        self.add(world)
        long_route = VGroup(*[world.arrows[i].copy().set_color(ENERGY).set_stroke(width=10)
                              for i in (0, 1, 2)])
        blocks3 = VGroup(*[chip(str(i), ENERGY, size=38) for i in (1, 2, 3)])
        blocks3.arrange(RIGHT, buff=.28).move_to([0, -1.9, 0])
        for b in blocks3:
            b.layout_ok = True
        self.at("On the longer path")
        self.play(Create(long_route), LaggedStart(*[FadeIn(b, shift=UP * .15) for b in blocks3],
                                                  lag_ratio=.20), run_time=1.3)
        self.play(Indicate(world.osp, color=OSP, scale_factor=1.18), run_time=.7)
        short_route = VGroup(world.arrows[3].copy().set_stroke(width=10),
                             world.arrows[2].copy().set_stroke(width=10))
        blocks2 = VGroup(*[chip(str(i), ENERGY, size=38) for i in (1, 2)])
        blocks2.arrange(RIGHT, buff=.28).move_to([0, -1.9, 0])
        for b in blocks2:
            b.layout_ok = True
        self.at("On a shorter path")
        self.play(FadeOut(long_route), FadeOut(blocks3), Create(short_route),
                  FadeIn(blocks2), run_time=1.1)
        self.at("The animal stays")
        self.play(Indicate(world.osp, color=OSP, scale_factor=1.18), run_time=.9)
        self.at("Its order depends")
        self.play(Indicate(short_route, color=ENERGY, scale_factor=1.03), run_time=.9)
        rule = caption("Consumer order is a position on one route.", color=TEXT, y=-1.9)
        rule.layout_ok = True  # intended caption over the carried Bay background
        self.at("Consumer order describes")
        self.play(FadeOut(blocks2), FadeIn(rule), run_time=.8)
        self.finish()


class S10Decomposers(SpokenScene):
    def construct(self):
        world = bay_world()
        self.add(world)
        starts = [world.phy.get_center(), world.zoo.get_center(),
                  world.men.get_center(), world.osp.get_center()]
        colors = [PHY, ZOO, MEN, OSP]
        pieces = VGroup(*[Square(.18, color=c, fill_color=c, fill_opacity=.65).move_to(s)
                          for s, c in zip(starts, colors)])
        self.at("Dead matter and wastes")
        self.play(FadeIn(pieces), run_time=.5)
        targets = [[-2.5 + i * 1.45, -2.55, 0] for i in range(4)]
        self.play(*[p.animate.move_to(t) for p, t in zip(pieces, targets)], run_time=1.4,
                  rate_func=linear)
        routes = VGroup(*[DashedLine(s, t, color=DEC, stroke_width=4, dash_length=.16)
                          for s, t in zip(starts, targets)])
        dec_label = T("decomposers", 32, DEC).move_to([-4.95, -2.2, 0])
        self.at("Dashed roots lead")
        self.play(LaggedStart(*[Create(r) for r in routes], lag_ratio=.15),
                  FadeIn(dec_label), run_time=1.2)
        specks = VGroup(*[packet(.08).move_to(s) for s in starts])
        self.add(specks)
        self.play(*[s.animate.move_to(t) for s, t in zip(specks, targets)], run_time=3.2,
                  rate_func=linear)
        loop = CurvedArrow([-2.75, -2.72, 0], [-.65, -2.72, 0], angle=-PI / 2,
                           color=DEC, stroke_width=5)
        self.at("Their work returns matter")
        self.play(Create(loop), run_time=1.0)
        onward = Arrow([2.1, -2.60, 0], [5.6, -2.60, 0], color=ENERGY,
                       stroke_width=7, tip_length=.24)
        self.play(GrowArrow(onward),
                  *[s.animate.move_to([4.6 + .20 * i, -2.60, 0]) for i, s in enumerate(specks)],
                  run_time=1.2)
        self.at("The decomposer branch")
        self.play(LaggedStart(*[Indicate(r, color=DEC, scale_factor=1.02)
                                for r in routes], lag_ratio=.16), run_time=1.3)
        self.finish()


class S11Narrowing(SpokenScene):
    def construct(self):
        world = web_world()
        self.add(world)
        starts = [world.phy.get_center() + UP * .25 + RIGHT * .12 * i for i in range(4)]
        packets = VGroup(*[packet(.22).move_to(s) for s in starts])
        self.at("Now watch each feeding")
        self.play(FadeIn(packets, lag_ratio=.15), run_time=.7)
        self.play(Indicate(world.phy, color=ENERGY, scale_factor=1.12), run_time=.7)
        continuing = packets[0]
        side = VGroup(packets[1], packets[2], packets[3])
        self.at("Much energy follows")
        self.play(side.animate.move_to(world.dec.get_center()).scale(.65),
                  continuing.animate.move_to(world.zoo).scale(.78), run_time=1.3)
        heat1 = VGroup(*[Arc(radius=.22 + .10 * i, start_angle=.2, angle=1.4,
                            color=HEAT, stroke_width=4).move_to(world.zoo.get_center() + RIGHT * .75)
                         for i in range(3)])
        self.play(FadeIn(heat1, lag_ratio=.15),
                  continuing.animate.move_to(world.men).scale(.72), run_time=1.2)
        self.at("Energy has not disappeared")
        down = DashedLine(world.men.get_center(), world.dec.get_center(), color=DEC,
                          stroke_width=4, dash_length=.15)
        heat2 = heat1.copy().move_to(world.men.get_center() + RIGHT * .9)
        self.play(Create(down), FadeIn(heat2), run_time=.8)
        self.play(continuing.animate.move_to(world.osp).scale(.65), run_time=1.1)
        rule = caption("less available at each step", size=36, color=ENERGY, y=-1.85)
        rule.shift(LEFT * 3.2)
        rule.layout_ok = True  # intended caption over the carried Bay background
        self.at("At each feeding step")
        self.play(FadeIn(rule), run_time=.7)
        self.play(Indicate(VGroup(world.phy, world.zoo, world.men, world.osp),
                           color=ENERGY, scale_factor=1.03), run_time=1.2)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        world = web_world()
        self.add(world)
        ray = Arrow(world.sun.get_center() + DR * .35, world.phy.get_center() + UL * .35,
                    color=ENERGY, stroke_width=7, tip_length=.22)
        p = packet(.20).move_to(world.sun)
        self.add(p)
        self.at("The Osprey's energy")
        self.play(GrowArrow(ray), p.animate.move_to(world.phy), run_time=1.0)
        route = VMobject().set_points_as_corners([world.phy.get_center(), world.zoo.get_center(),
                                                  world.men.get_center(), world.osp.get_center()])
        self.play(MoveAlongPath(p, route), run_time=2.0, rate_func=linear)
        self.play(p.animate.scale(.34), run_time=.35)
        self.at("A food web shows")
        branch_packets = VGroup(packet(.12).move_to(world.phy), packet(.12).move_to(world.men))
        self.add(branch_packets)
        self.play(MoveAlongPath(branch_packets[0], world.arrows[3].copy()),
                  MoveAlongPath(branch_packets[1], world.arrows[4].copy()), run_time=1.4,
                  rate_func=linear)
        heat = VGroup(*[Arc(radius=.18 + .09 * i, start_angle=.1, angle=1.5,
                           color=HEAT, stroke_width=4).move_to([2.9, 1.25, 0]) for i in range(3)])
        downward = DashedLine(world.men.get_center(), world.dec.get_center(), color=DEC,
                              stroke_width=4, dash_length=.15)
        self.at("The shrinking packet")
        self.play(FadeIn(heat, lag_ratio=.12), Create(downward),
                  Indicate(p, color=ENERGY, scale_factor=1.6), run_time=1.1)
        school = VGroup(*[fish_icon(MEN, .45).move_to([-.55 + .55 * (i % 4),
                                                       -.15 - .42 * (i // 4), 0])
                          for i in range(8)])
        self.at("The web maps routes")
        self.play(Transform(world.men, school), FadeOut(branch_packets), run_time=1.1)
        self.play(Indicate(world.arrows, color=ENERGY, scale_factor=1.02), run_time=.9)
        self.finish()


class S13End(EndCard):
    LINE = "At each feeding step, less energy is available to the next level."
