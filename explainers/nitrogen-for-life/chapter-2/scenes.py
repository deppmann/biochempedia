"""Around the Loop, and Out of It — nitrogen-for-life, chapter 2.

COLOR MAP (shared throughout this chapter)
  GREY   = clasped nitrogen-gas pairs and structural outlines
  GREEN  = usable nitrogen and growing plants
  GOLD   = the clasp that makes nitrogen gas hard to use
  ORANGE = sugar and decomposer/bacterial activity
  BLUE   = soil water, rain, streams, and the Bay
  TEXT   = the followed atom's halo, fungi, animals, and main labels
  BROWN  = soil and tree trunks

All chemistry is schematic: dots, pairs, labels, and blocks only—no structures.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BROWN = "#8B6546"
SKY = "#9AA4B2"


def arrow(a, b, color=TEXT, width=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=width, tip_length=tip)


def atom(pos, halo=False, radius=0.11, color=GREEN):
    d = Dot(pos, radius=radius, color=color)
    if not halo:
        return d
    h = Circle(radius=radius * 2.25, color=TEXT, stroke_width=3).move_to(pos)
    h.layout_ok = True  # deliberate tracking halo around its own dot
    return VGroup(h, d)


def gas_pair(pos=(0, 0, 0), scale=1.0, halo_left=False):
    x, y, _ = pos
    left = Dot([x - .24 * scale, y, 0], radius=.13 * scale, color=GREY)
    right = Dot([x + .24 * scale, y, 0], radius=.13 * scale, color=GREY)
    bar = Line(left.get_center(), right.get_center(), color=GREY, stroke_width=5 * scale)
    clasp = RoundedRectangle(corner_radius=.05, width=.19 * scale, height=.25 * scale,
                             color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=.35).move_to(pos)
    g = VGroup(bar, clasp, left, right)
    if halo_left:
        h = Circle(radius=.28 * scale, color=TEXT, stroke_width=3).move_to(left)
        h.layout_ok = True
        g.add(h)
    return g


def leaf(pos=(0, 0, 0), width=2.4, angle=0.15):
    blade = Ellipse(width=width, height=width * .48, color=GREEN, stroke_width=5,
                    fill_color=GREEN, fill_opacity=.20).rotate(angle).move_to(pos)
    vein = Line(blade.get_left() + RIGHT * .15, blade.get_right() + LEFT * .15,
                color=GREEN, stroke_width=3).rotate(angle, about_point=blade.get_center())
    return VGroup(blade, vein)


def soybean(cx=-3.5, ground_y=-.55, height=2.7):
    stem = Line([cx, ground_y, 0], [cx, ground_y + height, 0], color=GREEN, stroke_width=8)
    leaves = VGroup(
        leaf([cx - .62, ground_y + 1.2, 0], 1.25, .35),
        leaf([cx + .62, ground_y + 1.65, 0], 1.25, -.35),
        leaf([cx, ground_y + 2.55, 0], 1.35, .05),
    )
    roots = VGroup(*[Line([cx, ground_y, 0], [cx + dx, -2.55, 0], color=BROWN, stroke_width=4)
                     for dx in (-1.0, -.45, .2, .85)])
    nodules = VGroup(*[Circle(radius=.16, color=ORANGE, stroke_width=3, fill_color=ORANGE,
                              fill_opacity=.32).move_to([cx + x, y, 0])
                       for x, y in [(-.82, -1.9), (-.25, -2.25), (.55, -1.75)]])
    return VGroup(stem, leaves, roots, nodules)


def corn(cx=3.3, ground_y=-.55, height=3.05):
    stem = Line([cx, ground_y, 0], [cx, ground_y + height, 0], color=GREEN, stroke_width=9)
    leaves = VGroup(
        leaf([cx - .75, ground_y + 1.05, 0], 1.55, .34),
        leaf([cx + .72, ground_y + 1.7, 0], 1.55, -.34),
        leaf([cx - .68, ground_y + 2.35, 0], 1.35, .3),
    )
    roots = VGroup(*[Line([cx, ground_y, 0], [cx + dx, -2.5, 0], color=BROWN, stroke_width=4)
                     for dx in (-1.0, -.5, 0, .55, 1.05)])
    return VGroup(stem, leaves, roots)


def soil_and_water():
    soil = Rectangle(width=13.0, height=2.25, stroke_width=0, fill_color=BROWN,
                     fill_opacity=.30).move_to([0, -1.68, 0])
    water = RoundedRectangle(corner_radius=.18, width=10.6, height=.55, color=BLUE,
                             stroke_width=3, fill_color=BLUE, fill_opacity=.18).move_to([0, -2.75, 0])
    return VGroup(soil, water)


def deer(pos=(2.7, .25, 0), scale=.95, resting=False):
    body = Ellipse(width=2.2, height=1.05, color=TEXT, stroke_width=4,
                   fill_color=BROWN, fill_opacity=.28)
    neck = Line([.85, .2, 0], [1.25, .85, 0], color=TEXT, stroke_width=7)
    head = Ellipse(width=.82, height=.48, color=TEXT, stroke_width=4,
                   fill_color=BROWN, fill_opacity=.28).move_to([1.5, .95, 0]).rotate(-.15)
    tail = Triangle(color=TEXT, fill_color=TEXT, fill_opacity=.8).scale(.18).rotate(.3).move_to([-1.15, .28, 0])
    legs = VGroup(*[Line([x, -.35, 0], [x + .05, -1.05, 0], color=TEXT, stroke_width=5)
                    for x in (-.65, .55)])
    g = VGroup(body, neck, head, tail, legs).scale(scale).move_to(pos)
    if resting:
        g.rotate(-.12).shift(DOWN * .35)
    return g


def bacteria_cluster(center=(0, 0, 0), color=ORANGE, n=5):
    offsets = [(-.65, .2, .25), (-.28, -.25, -.35), (.1, .18, .5), (.45, -.18, -.15), (.72, .28, .3)]
    return VGroup(*[RoundedRectangle(corner_radius=.10, width=.48, height=.22, color=color,
                                     stroke_width=3, fill_color=color, fill_opacity=.35)
                    .rotate(a).move_to(np.array(center) + [x, y, 0]) for x, y, a in offsets[:n]])


def farm_world(show_soy=True, show_corn=True, show_deer=True):
    """The carried Virginia farm cutaway, always at identical scale and coordinates."""
    sky = RoundedRectangle(corner_radius=.2, width=13, height=1.0, color=GREY,
                           stroke_width=3, fill_color=GREY, fill_opacity=.08).move_to([0, 3.0, 0])
    pairs = VGroup(*[gas_pair([x, 3.0 + .12 * np.sin(x), 0], .72) for x in (-5.2, -3.7, -2.1, -.5, 1.2, 2.9, 4.6)])
    pairs._drift_x = 0.0

    def drift(mob, dt):
        mob._drift_x += .28 * dt
        mob.shift(RIGHT * .28 * dt)
        if mob._drift_x > 1.5:
            mob.shift(LEFT * 1.5)
            mob._drift_x = 0.0
    pairs.add_updater(drift)
    base = soil_and_water()
    items = [sky, pairs, base]
    if show_soy:
        items.append(soybean())
    if show_corn:
        items.append(corn())
    if show_deer:
        items.append(deer([.2, .15, 0], .72))
    g = VGroup(*items)
    g.tag = scope_tag("schematic")
    return g


def protein_block(pos, atom_inside=True, scale=1.0):
    p = chip("protein", GREEN, size=30).scale(scale).move_to(pos).set_z_index(6)
    p[0].set_fill("#0f1117", opacity=.96)
    p.layout_ok = True  # protein label deliberately sits in its cartoon block inside leaf/body
    if atom_inside:
        a = atom(p.get_center() + DOWN * .38 * scale, True, .09 * scale).set_z_index(7)
        return VGroup(p, a)
    return p


def forest_floor(resting=True):
    ground = Rectangle(width=13, height=2.2, stroke_width=0, fill_color=BROWN,
                       fill_opacity=.30).move_to([0, -1.9, 0])
    trunks = VGroup(*[Line([x, -.8, 0], [x, 3.1, 0], color=BROWN, stroke_width=18)
                      for x in (-5.2, 4.9)])
    litter = VGroup(*[leaf([x, -1.05 - .12 * (i % 2), 0], .72, (-1) ** i * .25)
                      for i, x in enumerate((-4.1, -2.8, -1.4, .2, 1.7, 3.1, 4.1))])
    d = deer([-.25, -.25, 0], 1.0, resting=resting)
    return VGroup(ground, trunks, litter, d)


def decomposer_view(with_deer=True):
    world = forest_floor()
    if not with_deer:
        world[-1].set_opacity(.12)
    threads = VGroup(*[ArcBetweenPoints([x, -1.05, 0], [x + 1.1, -2.15, 0], angle=(-1) ** i * .6,
                                           color=TEXT, stroke_width=3)
                       for i, x in enumerate((-3.8, -2.4, -1.0, .5, 1.9, 3.2))])
    bugs = bacteria_cluster([2.7, -1.6, 0])
    return VGroup(world, threads, bugs)


def cycle_diagram(branch=False):
    labels = [chip("air", GREY, 28), chip("nodule", ORANGE, 26), chip("soybean", GREEN, 26),
              chip("deer", TEXT, 26), chip("decomposers", ORANGE, 24), chip("soil", BLUE, 26),
              chip("corn", GREEN, 26), chip("soggy soil", BLUE, 24)]
    angles = np.linspace(PI / 2, PI / 2 - TAU, len(labels), endpoint=False)
    pts = [np.array([4.3 * np.cos(a), 2.55 * np.sin(a), 0]) for a in angles]
    for lab, p in zip(labels, pts):
        lab.move_to(p)
    arrows = VGroup(*[Arrow(labels[i].get_center(), labels[(i + 1) % len(labels)].get_center(),
                            buff=.72, color=GREEN, stroke_width=4, tip_length=.16)
                      for i in range(len(labels))])
    arrows.layout_ok = True  # connector arrows deliberately terminate at their labelled cycle nodes
    center = T("nitrogen cycle", 36, TEXT, weight=BOLD)
    g = VGroup(arrows, *labels, center)
    if branch:
        bay = chip("Chesapeake Bay", BLUE, 26).move_to([5.1, -2.95, 0])
        leak = CurvedArrow([1.1, -2.3, 0], bay.get_left(), angle=-.35, color=BLUE, stroke_width=6,
                           tip_length=.22)
        g.add(leak, bay)
    return g


def moving_cycle_atom(radius=1.8, speed=.72):
    """The followed atom and a bright trace keep circulating while the rule lands."""
    a = atom([radius, 0, 0], True, .18)
    trace = Arc(radius=radius, start_angle=-.55, angle=.8, color=GREEN, stroke_width=10)
    tip = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1).scale(.13).rotate(-PI / 2)
    tip.move_to([radius, 0, 0])
    g = VGroup(trace, tip, a)
    g.layout_ok = True  # the animated tracer is the cycle path itself and passes behind node edges

    def orbit(mob, dt):
        mob.rotate(-speed * dt, about_point=ORIGIN)
    return g.add_updater(orbit)


def falling(rain, speed=.9, top=3.5, bottom=-3.2):
    """Loop already-drawn rain through the farm cutaway."""
    for i, drop in enumerate(rain):
        drop._rain_delay = i * .11

        def fall_one(mob, dt, top=top, bottom=bottom):
            mob.shift(DOWN * speed * dt)
            if mob.get_top()[1] < bottom:
                mob.shift(UP * (top - bottom))
        drop.add_updater(fall_one)
    return rain


class S00Title(TitleCard):
    LESSON = "Nitrogen for Life"
    TITLE = "Around the Loop, and Out of It"

    def construct(self):
        world = farm_world()
        glow = atom([-3.5, 2.0, 0], True, .12)
        world.set_opacity(.25)
        world.layout_ok = True  # deliberate farm cutaway behind the chapter title
        self.add(world, glow)
        super().construct()


class S01Hook(SpokenScene):
    def construct(self):
        lf = leaf([0, .65, 0], 6.2, .05)
        tracked = atom([0, .65, 0], True, .16)
        self.add(lf, tracked, scope_tag("schematic"))
        self.at("Once it is part")
        self.play(lf.animate.scale(1.03), run_time=.7, rate_func=there_and_back)
        self.at("is it there")
        q = question_card("Once it is in a leaf, is it there for good?", y=-2.85, max_w=10.8)
        self.play(FadeIn(q, shift=UP * .15), run_time=.7)
        self.at("keep on moving")
        self.play(tracked.animate.shift(RIGHT * 1.1), run_time=.8, rate_func=there_and_back)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        world = farm_world(show_corn=False, show_deer=False)
        self.add(world, world.tag)
        self.at("nitrogen gas stayed locked")
        focus = gas_pair([-1.0, 3.0, 0], 1.5, True)
        self.play(FadeIn(focus), run_time=.7)
        self.at("changer opened it")
        nodule = Circle(radius=.55, color=ORANGE, fill_color=ORANGE, fill_opacity=.18).move_to([-3.75, -2.0, 0])
        self.play(Transform(focus, focus.copy().move_to(nodule)), FadeIn(nodule), run_time=1.0)
        opened = VGroup(atom([-4.0, -2.0, 0], True), atom([-3.48, -2.0, 0]))
        self.play(ReplacementTransform(focus, opened), Flash(nodule, color=GOLD), run_time=.8)
        self.at("follow one atom")
        self.play(opened[0].animate.shift(UP * .45), run_time=.8)
        self.finish()


class S03Leaf(SpokenScene):
    def construct(self):
        world = farm_world(show_corn=False, show_deer=False)
        pair = gas_pair([-1.0, 3.0, 0], 1.35, True)
        self.add(world, world.tag, pair)
        self.at("one half of a gray pair")
        self.play(pair.animate.shift(LEFT * .35), run_time=.7, rate_func=there_and_back)
        self.at("A nodule changes it")
        self.play(pair.animate.move_to([-3.75, -2.0, 0]).scale(.75), run_time=1.1)
        usable = atom([-3.75, -2.0, 0], True)
        self.play(ReplacementTransform(pair, usable), Flash(usable, color=GOLD), run_time=.7)
        self.at("plant builds it")
        self.play(usable.animate.move_to([-4.0, 1.95, 0]), run_time=1.2)
        protein = protein_block([-5.55, 1.95, 0])
        self.play(ReplacementTransform(usable, protein), run_time=.8)
        self.finish()


class S04Deer(SpokenScene):
    def construct(self):
        soy = soybean(-3.0)
        lf_protein = protein_block([-5.4, 1.95, 0], scale=.85)
        d = deer([2.35, .15, 0], 1.1)
        bob(soy, amp=.13, speed=1.15)
        self.add(soil_and_water()[0], soy, lf_protein, d, scope_tag("schematic"))
        self.at("wanders over and eats")
        self.play(d.animate.shift(LEFT * 2.0), run_time=1.3)
        self.play(FadeOut(lf_protein), run_time=.5)
        self.at("digests the leaf's proteins")
        pieces = VGroup(*[Square(.28, color=GREEN, fill_color=GREEN, fill_opacity=.25)
                          .move_to([-1.2 + i * .4, .15 + .15 * (-1) ** i, 0]) for i in range(4)])
        self.play(FadeIn(pieces), run_time=.7)
        self.at("becomes part of a protein")
        body_p = protein_block([-.85, -.25, 0], scale=.78)
        self.play(ReplacementTransform(pieces, body_p), run_time=.9)
        self.at("Animals get nitrogen")
        cap = caption("Animals get nitrogen by eating.", color=TEXT)
        self.play(FadeIn(cap), d.animate.shift(RIGHT * .2), run_time=.8)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        floor = forest_floor()
        bob(floor[2], amp=.12, speed=1.2)
        self.add(floor, scope_tag("schematic"))
        self.at("dies in the woods")
        self.play(floor[-1].animate.rotate(-.08), run_time=.8)
        self.at("Is its nitrogen gone")
        q = question_card("Is the deer's nitrogen gone for good?", ["gone", "not gone"], y=-3.25)
        self.play(FadeIn(q), run_time=.8)
        self.at("Pause and decide")
        ring, run = countdown(1.0, center=[6.0, -2.35, 0])
        self.add(ring)
        self.play(run)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Is the deer's nitrogen gone for good?"
    OPTIONS = ["gone", "not gone"]
    CARD = {"y": -3.25}
    RING_AT = (6.0, -2.35, 0)
    SECONDS = 5.0

    def backdrop(self):
        return VGroup(forest_floor(), scope_tag("schematic"))


class S07Reveal(SpokenScene):
    def construct(self):
        view = decomposer_view()
        pulse(view[1], base=3.0, amp=1.1, speed=1.5)
        self.add(view, scope_tag("schematic"))
        self.at("not gone")
        ans = T("not gone", 38, GREEN, weight=BOLD).move_to([0, 2.8, 0])
        self.play(FadeIn(ans, scale=.8), run_time=.6)
        self.at("Decomposers go to work")
        self.play(Create(view[1]), FadeIn(view[2]), run_time=1.2)
        self.at("such as a fungus")
        names = T("decomposers: fungi and bacteria", 30, ORANGE, weight=BOLD).move_to([0, 2.2, 0])
        self.play(swap(ans, names), run_time=.8)
        self.at("breaks down dead things")
        definition = caption("decomposer: breaks down dead things and wastes", 28, TEXT)
        self.play(FadeIn(definition), run_time=.8)
        self.finish()


class S08Soil(SpokenScene):
    def construct(self):
        view = decomposer_view()
        droppings = VGroup(*[Dot([2.2 + i * .22, -.65, 0], radius=.1, color=BROWN) for i in range(3)])
        tracked = atom([-.75, -.3, 0], True)
        bob(view[1], amp=.14, speed=1.35)
        self.add(view, droppings, tracked, scope_tag("schematic"))
        self.at("break down the deer's body")
        self.play(view[0][-1].animate.set_opacity(.12), droppings.animate.set_opacity(.15),
                  view[1].animate.set_stroke(width=5), run_time=1.4)
        self.at("returns to the soil")
        water = soil_and_water()[1]
        self.play(FadeIn(water), tracked.animate.move_to([-.2, -2.75, 0]), run_time=1.1)
        self.at("one green dot")
        self.play(Indicate(tracked, color=GREEN, scale_factor=1.3), run_time=.8)
        self.finish()


class S09Corn(SpokenScene):
    def construct(self):
        base = soil_and_water()
        c = corn(1.4)
        tracked = atom([-.2, -2.75, 0], True)
        bob(c, amp=.13, speed=1.2)
        self.add(base, c, tracked, scope_tag("schematic"))
        self.at("root reaches it")
        root = Line([1.4, -.55, 0], [-.2, -2.75, 0], color=BROWN, stroke_width=6)
        self.play(Create(root), run_time=.9)
        self.play(tracked.animate.move_to([1.4, .4, 0]), run_time=1.0)
        self.at("Same atom")
        same = T("same atom, second plant", 32, TEXT, weight=BOLD).move_to([-3.35, 2.6, 0])
        self.play(FadeIn(same), run_time=.7)
        self.at("brand new protein")
        self.play(tracked.animate.move_to([.75, 1.95, 0]), run_time=.8)
        protein = protein_block([-1.05, 1.95, 0], scale=.9)
        self.play(ReplacementTransform(tracked, protein), run_time=.7)
        self.finish()


class S10Back(SpokenScene):
    def construct(self):
        base = soil_and_water()
        c = corn(1.4)
        tracked = atom([-.3, 1.95, 0], True)
        self.add(base, c, tracked, scope_tag("schematic"))
        self.at("corn plant dies")
        self.play(Rotate(c, -PI / 3, about_point=[1.4, -.55, 0]), run_time=1.0)
        self.at("Decomposers return")
        dec = bacteria_cluster([-.1, -1.25, 0])
        bob(dec, amp=.15, speed=1.35)
        self.play(FadeIn(dec), tracked.animate.move_to([-.5, -2.75, 0]), run_time=1.1)
        form1 = chip("usable form 1", GREEN, 26).move_to([-2.5, -1.55, 0])
        self.play(FadeIn(form1), run_time=.6)
        self.at("soil with oxygen")
        pockets = VGroup(*[Circle(radius=.18, color=TEXT, stroke_width=3).move_to([x, -1.2, 0])
                           for x in (1.3, 2.0, 2.7)])
        oxygen = T("oxygen", 28, TEXT).next_to(pockets, UP, buff=.15)
        self.play(FadeIn(pockets), FadeIn(oxygen), run_time=.7)
        self.at("other bacteria change it")
        other = bacteria_cluster([2.0, -2.0, 0], n=4)
        form2 = chip("usable form 2", GREEN, 26, fill_opacity=.9).move_to([4.2, -.55, 0]).set_z_index(5)
        self.play(tracked.animate.move_to([2.0, -2.0, 0]), FadeIn(other), run_time=.8)
        self.play(tracked.animate.move_to([3.55, -2.0, 0]), FadeIn(form2), FadeOut(form1), run_time=.8)
        self.finish()


class S10bGas(SpokenScene):
    def construct(self):
        base = soil_and_water()
        tracked = atom([3.55, -2.0, 0], True)
        form2 = chip("usable form 2", GREEN, 26, fill_opacity=.9).move_to([4.2, -.55, 0]).set_z_index(5)
        pockets = VGroup(*[Circle(radius=.18, color=TEXT, stroke_width=3).move_to([x, -1.15, 0])
                           for x in (1.3, 2.0, 2.7)])
        self.add(base, tracked, form2, pockets, scope_tag("schematic"))
        self.at("heavy rain soaks")
        rain = falling(VGroup(*[Line([x, 3.4, 0], [x - .18, 2.55, 0], color=BLUE, stroke_width=4)
                                for x in np.linspace(-5.5, 5.5, 12)]), bottom=-.35)
        self.play(Create(rain), base[0].animate.set_fill(BLUE, opacity=.35), FadeOut(pockets), run_time=1.2)
        self.at("little oxygen is left")
        low = chip("soggy soil: little oxygen", BLUE, 28, fill_opacity=.9).move_to([0, 2.1, 0]).set_z_index(5)
        self.play(FadeIn(low), run_time=.7)
        self.at("Different bacteria change")
        bugs = bacteria_cluster([1.7, -1.65, 0], color=BLUE)
        self.play(FadeIn(bugs), tracked.animate.move_to([1.7, -1.65, 0]), run_time=.9)
        self.at("back into nitrogen gas")
        pair = gas_pair([1.7, -1.65, 0], 1.05, True)
        self.play(ReplacementTransform(tracked, pair), FadeOut(form2), run_time=.8)
        self.at("rises into the air")
        self.play(pair.animate.move_to([1.7, 3.0, 0]), run_time=1.2)
        self.finish()


class S11Cycle(SpokenScene):
    def construct(self):
        cyc = cycle_diagram()
        tracked = moving_cycle_atom()
        self.add(cyc, tracked)
        self.at("through the soil")
        self.play(Create(cyc[0]), run_time=1.3)
        self.at("nitrogen cycle")
        self.play(FadeIn(cyc[-1], scale=.8), run_time=.7)
        self.at("At every step")
        self.play(Indicate(tracked, color=TEXT, scale_factor=1.25), run_time=.7)
        self.at("never made")
        n = ValueTracker(1)
        read_box = RoundedRectangle(corner_radius=.16, width=5.3, height=2.05, color=GREY,
                                    fill_color=BG, fill_opacity=.94).move_to([0, -.65, 0])
        read = VGroup(read_box, counter("1 atom: {:.0f}", n, at=[0, -.15, 0], size=30),
                      T("changed form", 28, GREEN).move_to([0, -.65, 0]),
                      T("never made • never destroyed", 26, TEXT).move_to([0, -1.12, 0])).set_z_index(5)
        self.play(FadeOut(cyc[-1]), FadeIn(read), run_time=.8)
        self.finish()


class S12Leak(SpokenScene):
    def construct(self):
        base = soil_and_water()
        c = corn(2.6)
        self.add(base, c, scope_tag("schematic"))
        self.at("far more fertilizer")
        bag = chip("fertilizer", GREEN, 30).rotate(-.25).move_to([-3.8, 2.1, 0])
        dots = VGroup(*[atom([-3.3 + .42 * (i % 6), 1.5 - .42 * (i // 6), 0]) for i in range(18)])
        self.play(FadeIn(bag), LaggedStart(*[FadeIn(d, shift=DOWN * .2) for d in dots], lag_ratio=.05), run_time=1.5)
        self.at("corn can take up")
        uptake = VGroup(*[dots[i] for i in (4, 5, 10, 11)])
        self.play(uptake.animate.move_to([2.6, -.6, 0]), run_time=.8)
        self.at("pool of green dots fills")
        pool_dots = VGroup(*[d for d in dots if d not in uptake])
        self.play(pool_dots.animate.arrange(RIGHT, buff=.14).scale(.75).move_to([-.6, -2.75, 0]), run_time=1.0)
        overflow = CurvedArrow([2.3, -2.75, 0], [5.3, -2.2, 0], angle=.35, color=GREEN, stroke_width=6)
        self.play(Create(overflow), run_time=.7)
        cap = caption("more than the corn can take up", color=GREEN, y=3.15)
        self.play(FadeIn(cap), run_time=.6)
        self.finish()


class S13Rain(SpokenScene):
    def construct(self):
        field = soil_and_water()
        extras = VGroup(*[atom([-2.4 + i * .45, -2.55, 0]) for i in range(9)])
        stream = CurvedArrow([1.8, -2.5, 0], [5.7, -1.0, 0], angle=.25, color=BLUE, stroke_width=18,
                             tip_length=.28)
        self.add(field, extras, scope_tag("schematic"))
        self.at("heavy rain falls")
        rain = falling(VGroup(*[Line([x, 3.4, 0], [x - .15, 2.55, 0], color=BLUE, stroke_width=4)
                                for x in np.linspace(-5.7, 5.7, 13)]), bottom=-.35)
        self.play(Create(rain), run_time=1.0)
        self.at("Water moving over")
        runoff = VGroup(*[arrow([x, -.65, 0], [x + 1.2, -.65, 0], BLUE, 5, .18) for x in (-4.8, -2.6, -.4)])
        down = VGroup(*[arrow([x, -.8, 0], [x, -2.25, 0], BLUE, 5, .18) for x in (-3.8, -1.6, .6)])
        self.play(*[GrowArrow(a) for a in runoff], *[GrowArrow(a) for a in down], run_time=1.1)
        self.at("carries the extra")
        self.play(Create(stream), extras.animate.move_to([4.4, -1.45, 0]).scale(.75), run_time=1.2)
        self.at("Chesapeake Bay")
        bay = chip("Chesapeake Bay", BLUE, 32).move_to([4.6, 1.2, 0])
        bay[0].set_fill(BG, opacity=.94)
        self.play(FadeIn(bay), run_time=.7)
        self.finish()


class S14Bloom(SpokenScene):
    def construct(self):
        bay = RoundedRectangle(corner_radius=.2, width=12, height=5.2, color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=.15).move_to([0, -.15, 0])
        surface = Line([-6, 2.45, 0], [6, 2.45, 0], color=BLUE, stroke_width=5)
        incoming = VGroup(*[atom([-5.3 + i * .38, 1.7 - .15 * (i % 2), 0]) for i in range(9)])
        self.add(bay, surface, incoming, scope_tag("schematic"))
        self.at("extra nitrogen feeds")
        self.play(incoming.animate.shift(RIGHT * 3.7), run_time=1.0)
        self.at("fast growth of algae")
        algae = VGroup(*[Dot([-4.9 + .45 * (i % 22), 2.05 - .28 * (i // 22), 0], radius=.12,
                                  color=GREEN) for i in range(66)])
        self.play(LaggedStart(*[FadeIn(a, scale=.3) for a in algae], lag_ratio=.015), run_time=1.8)
        label = T("algal bloom", 36, GREEN, weight=BOLD).move_to([0, .55, 0])
        self.play(FadeIn(label), run_time=.7)
        self.at("surface turns thick")
        layer = Rectangle(width=11.6, height=.75, stroke_width=0, fill_color=GREEN,
                          fill_opacity=.38).move_to([0, 1.85, 0])
        self.play(FadeIn(layer), algae.animate.set_opacity(.9), run_time=1.0)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        cyc = cycle_diagram(branch=False)
        tracked = moving_cycle_atom()
        self.add(cyc, tracked)
        self.at("goes around the loop")
        self.play(Indicate(tracked, color=TEXT, scale_factor=1.25), run_time=.7)
        self.at("never used up")
        rule = caption("never used up, but it can leave a field", color=GREEN)
        self.play(FadeIn(rule), run_time=.7)
        self.at("water can carry it")
        bay = chip("Chesapeake Bay", BLUE, 26).move_to([5.15, -2.35, 0])
        leak = CurvedArrow([1.0, -2.0, 0], bay.get_left(), angle=-.28, color=BLUE, stroke_width=6,
                           tip_length=.22)
        self.play(Create(leak), tracked.animate.move_to([3.7, -2.2, 0]), FadeIn(bay), run_time=1.2)
        self.finish()


class S16End(EndCard):
    LINE = "Nitrogen changes form around the loop but is never used up."
