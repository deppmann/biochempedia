"""Why sprouting peas warm a thermos.

COLOUR MAP: glucose/stored energy GOLD; oxygen BLUE; carbon dioxide GREY;
water CYAN; cell work GREEN; thermal energy ORANGE; mitochondria PURPLE;
cells CREAM.  All pictures are schematic and no molecular structures are drawn.
"""
from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CYAN = "#4FC3C9"
CREAM = "#F3E7C9"
GLUCOSE, OXYGEN, CO2, WATER, WORK, HEAT, MITO, CELL = GOLD, BLUE, GREY, CYAN, GREEN, ORANGE, PURPLE, CREAM


def arrow(a, b, color=TEXT, width=5):
    a = Arrow(a, b, buff=0.08, color=color, stroke_width=width, tip_length=0.22)
    a.layout_ok = True  # deliberate pathway connector; endpoints are checked visually
    return a


def glucose_block(text="glucose", size=26):
    return chip(text, GLUCOSE, size=size)


def oxygen_dots(center, n=5, spread=0.48):
    return VGroup(*[Dot(np.array(center) + [spread * (i - (n - 1) / 2), 0.13 * ((i % 2) * 2 - 1), 0],
                              radius=0.11, color=OXYGEN) for i in range(n)])


def water_drop(center, scale=1.0):
    d = VGroup(Circle(radius=0.20, color=WATER, fill_color=WATER, fill_opacity=0.75),
               Triangle(color=WATER, fill_color=WATER, fill_opacity=0.75).scale(0.20).shift(UP * 0.22))
    return d.scale(scale).move_to(center)


def cell_picture(center=(0, 0.15, 0), width=9.8, height=5.2):
    shell = RoundedRectangle(corner_radius=0.65, width=width, height=height, stroke_color=CELL,
                             stroke_width=5, fill_color=CELL, fill_opacity=0.10).move_to(center)
    return bob(shell, amp=0.055, speed=1.9)


def mitochondrion(center=(2.4, 0.2, 0), scale=1.0):
    outer = Ellipse(width=3.2 * scale, height=1.75 * scale, color=MITO, stroke_width=5,
                    fill_color=MITO, fill_opacity=0.15).move_to(center)
    x, y, _ = center
    folds = VGroup(*[
        ArcBetweenPoints([x - 1.1 * scale + i * 0.52 * scale, y + 0.43 * scale, 0],
                         [x - 0.86 * scale + i * 0.52 * scale, y - 0.43 * scale, 0],
                         angle=(-1) ** i * 1.2, color=MITO, stroke_width=3)
        for i in range(5)
    ])
    return VGroup(outer, folds)


def thermos(center_x, pea_color, label, level, crossed=False):
    body = RoundedRectangle(corner_radius=0.3, width=4.4, height=5.05, color=GREY, stroke_width=5,
                            fill_color=GREY, fill_opacity=0.10).move_to([center_x, -0.15, 0])
    neck = RoundedRectangle(corner_radius=0.1, width=2.1, height=0.4, color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.2).move_to([center_x, 2.55, 0])
    peas = VGroup(*[Circle(radius=0.24, color=pea_color, fill_color=pea_color, fill_opacity=0.72)
                     .move_to([center_x - 1.15 + (i % 5) * 0.56, -1.95 + (i // 5) * 0.52, 0])
                     for i in range(15)])
    if pea_color != GREY:
        bob(peas, amp=0.075, speed=2.1, seed=1)
    tube = RoundedRectangle(corner_radius=0.12, width=0.35, height=3.1, color=GREY, stroke_width=3)
    tube.move_to([center_x, 0.42, 0])
    bulb = Circle(radius=0.31, color=GREY, stroke_width=3, fill_color=HEAT, fill_opacity=1)
    bulb.move_to([center_x, -1.25, 0])
    fluid = always_redraw(lambda: Rectangle(width=0.17, height=max(0.05, level.get_value() + 1.2),
                                              stroke_width=0, fill_color=HEAT, fill_opacity=1)
                            .move_to([center_x, (-1.2 + level.get_value()) / 2, 0]))
    title = T(label, 30, pea_color, weight=BOLD).move_to([center_x, 3.2, 0])
    g = VGroup(body, neck, peas, tube, bulb, fluid, title)
    if crossed:
        g.add(Line([center_x - 1.35, -2.15, 0], [center_x + 1.35, -0.55, 0], color=RED, stroke_width=8))
    return g


def thermos_pair(left_level=None, right_level=None, crossed=False):
    left_level = left_level or ValueTracker(-0.2)
    right_level = right_level or ValueTracker(-0.2)
    return VGroup(thermos(-3.75, CELL, "sprouting peas", left_level),
                  thermos(3.75, GREY, "boiled, cooled peas", right_level, crossed=crossed))


def pathway_world(include_products=True):
    cell = cell_picture(width=12.4)
    core = RoundedRectangle(corner_radius=0.3, width=4.3, height=2.0, color=MITO, stroke_width=5,
                            fill_color=MITO, fill_opacity=0.15).move_to([0, 0.15, 0])
    title = T("cellular respiration", 27, MITO, weight=BOLD).move_to(core)
    core.layout_ok = True  # the label is intentionally centred on its process block
    title.layout_ok = True
    pulse(core, base=5.0, amp=2.0, speed=2.2)
    bob(core, amp=0.075, speed=1.8)
    gl = glucose_block().move_to([-5.1, 1.25, 0])
    ox = chip("oxygen", OXYGEN, 26).move_to([-5.1, -1.15, 0])
    ins = VGroup(arrow(gl.get_right(), [-2.25, 0.7, 0], GLUCOSE),
                 arrow(ox.get_right(), [-2.25, -0.4, 0], OXYGEN))
    g = VGroup(cell, core, title, gl, ox, ins)
    bases = [np.array([-1.2 + i * 0.48, 0.48 - (i % 2) * 0.65, 0]) for i in range(6)]
    activity = VGroup(*[Dot(p, radius=0.09, color=GLUCOSE if i % 2 == 0 else OXYGEN)
                        for i, p in enumerate(bases)])
    activity.clock = 0.0
    def flow(m, dt):
        m.clock += dt
        for i, (d, p) in enumerate(zip(m, bases)):
            d.move_to(p + [0.18 * np.sin(2.4 * m.clock + i), 0.12 * np.cos(2.0 * m.clock + i), 0])
    activity.add_updater(flow)
    g.add(activity)
    if include_products:
        products = VGroup(chip("carbon dioxide", CO2, 25).move_to([4.65, 1.5, 0]),
                          chip("water", WATER, 26).move_to([4.65, 0.1, 0]),
                          chip("released energy", GLUCOSE, 25).move_to([4.65, -1.35, 0]))
        outs = VGroup(*[arrow([2.25, y, 0], p.get_left(), col) for y, p, col in
                        zip((0.85, 0.15, -0.6), products, (CO2, WATER, GLUCOSE))])
        g.add(products, outs)
    return g


def gear(center=(3.75, 1.0, 0), color=WORK, radius=0.78):
    ring = Annulus(inner_radius=radius * 0.48, outer_radius=radius * 0.78, color=color,
                   fill_color=color, fill_opacity=0.65, stroke_width=3).move_to(center)
    teeth = VGroup(*[Rectangle(width=0.23, height=0.38, color=color, fill_color=color, fill_opacity=0.8)
                      .move_to(np.array(center) + radius * 0.86 * np.array([np.cos(a), np.sin(a), 0])).rotate(a)
                      for a in np.linspace(0, TAU, 8, endpoint=False)])
    g = VGroup(ring, teeth)
    g.add_updater(lambda m, dt: m.rotate(0.32 * dt))
    return g


def heat_particles(center=(3.75, -1.2, 0), n=12):
    bases = [np.array(center) + [(i % 6 - 2.5) * 0.38, (i // 6 - 0.5) * 0.5, 0] for i in range(n)]
    dots = VGroup(*[Dot(p, radius=0.095, color=HEAT) for p in bases])
    dots.clock = 0.0
    def jitter(m, dt):
        m.clock += dt
        for i, (d, p) in enumerate(zip(m, bases)):
            d.move_to(p + 0.14 * np.array([np.sin(7 * m.clock + i), np.cos(8.3 * m.clock + i * 1.7), 0]))
    return dots.add_updater(jitter)


def energy_fork(with_question=False):
    src = glucose_block("released energy", 28).move_to([-4.35, 0, 0])
    joint = Dot([-1.2, 0, 0], radius=0.17, color=GLUCOSE)
    work = gear([2.7, 1.15, 0])
    heat = heat_particles([2.7, -1.15, 0])
    work_lab = T("cell work", 30, WORK, weight=BOLD).move_to([4.85, 1.15, 0])
    heat_lab = T("warmth", 30, HEAT, weight=BOLD).move_to([5.2, -1.15, 0])
    paths = VGroup(arrow(src.get_right(), joint.get_center(), GLUCOSE),
                   arrow(joint.get_center(), work.get_left(), WORK),
                   arrow(joint.get_center(), heat.get_left(), HEAT))
    return VGroup(src, joint, paths, work, heat, work_lab, heat_lab)


PREDICT_Q = "Where will the released energy go?"
PREDICT_OPTIONS = ["cell work", "warmth", "both"]


class S00Hook(SpokenScene):
    TITLE = "Why Do Sprouting Peas Get Warm?"
    LESSON = "Releasing energy from food"
    def construct(self):
        L, R = ValueTracker(-0.25), ValueTracker(-0.25)
        pair = thermos_pair(L, R)
        self.play(FadeIn(pair), run_time=0.7)
        self.add(scope_tag())
        self.at("Both thermoses begin")
        room = DashedLine([-6.0, -0.25, 0], [6.0, -0.25, 0], color=GREY, stroke_width=3)
        room_lab = T("room temperature", 22, GREY).move_to([0, -0.62, 0])
        self.play(Create(room), FadeIn(room_lab), run_time=0.7)
        self.at("Only one contains")
        self.play(Indicate(pair[0][2], color=GREEN, scale_factor=1.05), run_time=0.8)
        self.at("Watch the warmth rise")
        self.play(L.animate.set_value(1.25), run_time=3.5, rate_func=smooth)
        self.finish()


class S01Stored(SpokenScene):
    def construct(self):
        mini = thermos(-5.25, CELL, "", ValueTracker(0.7)).scale(0.52).move_to([-5.25, 0.25, 0])
        cell = cell_picture([1.55, 0.2, 0], 8.7, 5.4)
        self.play(FadeIn(mini), TransformFromCopy(mini[2][7], cell), run_time=1.0)
        self.add(scope_tag())
        self.at("food molecules store energy")
        store = chip("food molecules", CELL, 28).move_to([0.3, 2.11, 0])
        self.play(FadeIn(store), run_time=0.6)
        self.at("fuel we will follow")
        blocks = VGroup(*[glucose_block().move_to([-0.1 + i * 1.75, 1.1, 0]) for i in range(3)])
        self.play(TransformFromCopy(store, blocks[0]), FadeIn(blocks[1:], shift=RIGHT * 0.3), run_time=1.0)
        self.at("Glucose is a sugar")
        glow = SurroundingRectangle(blocks, color=GLUCOSE, buff=0.2, stroke_width=5)
        self.play(Create(glow), run_time=0.7)
        self.at("Plants make glucose")
        sun = Circle(radius=0.45, color=YELLOW, fill_color=YELLOW, fill_opacity=0.8).move_to([-1.3, -1.35, 0])
        leaf = Ellipse(width=1.35, height=0.65, color=GREEN, fill_color=GREEN, fill_opacity=0.55).rotate(0.35).move_to([0.45, -1.35, 0])
        strip = VGroup(sun, arrow(sun.get_right(), leaf.get_left(), YELLOW), leaf,
                       arrow(leaf.get_right(), [2.45, -1.35, 0], GREEN), glucose_block().move_to([3.25, -1.35, 0]))
        self.play(LaggedStart(*[FadeIn(x) for x in strip], lag_ratio=0.15), run_time=1.4)
        self.at("Cells must release")
        pulse(cell)
        self.play(blocks.animate.shift(DOWN * 0.55), FadeOut(glow), run_time=1.2)
        self.finish()


class S02Pathway(SpokenScene):
    def construct(self):
        w = pathway_world(False)
        self.play(FadeIn(w[0]), FadeIn(w[1]), Write(w[2]), run_time=0.8)
        self.add(scope_tag())
        self.at("Glucose and oxygen")
        self.play(FadeIn(w[3:5]), GrowArrow(w[5][0]), GrowArrow(w[5][1]), run_time=1.0)
        self.at("Carbon dioxide and water")
        prods = VGroup(chip("carbon dioxide", CO2, 25).move_to([4.65, 1.5, 0]),
                       chip("water", WATER, 26).move_to([4.65, 0.1, 0]))
        outs = VGroup(arrow([1.75, 0.8, 0], prods[0].get_left(), CO2), arrow([1.75, 0.1, 0], prods[1].get_left(), WATER))
        self.play(Create(outs), FadeIn(prods, shift=RIGHT * 0.25), run_time=1.0)
        self.at("along with released energy")
        en = chip("released energy", GLUCOSE, 25).move_to([4.65, -1.35, 0])
        ae = arrow([1.75, -0.55, 0], en.get_left(), GLUCOSE)
        self.play(GrowArrow(ae), FadeIn(en, shift=RIGHT * 0.25), run_time=0.8)
        self.at("Oxygen is a gas")
        self.play(Indicate(w[4], color=OXYGEN), run_time=0.8)
        self.at("Carbon dioxide is a gas")
        self.play(Indicate(prods[0], color=CO2), run_time=0.8)
        self.finish()


class S03Where(SpokenScene):
    def construct(self):
        cell = cell_picture()
        steps = VGroup(*[Circle(radius=0.22, color=GLUCOSE, fill_color=GLUCOSE, fill_opacity=0.7)
                         .move_to([-4.5 + i * 0.75, 0.25, 0]) for i in range(10)])
        mito = mitochondrion([2.4, 0.25, 0], 1.35)
        bob(mito, amp=0.075, speed=1.9)
        self.play(FadeIn(cell), LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.08), run_time=1.2)
        self.add(scope_tag())
        self.at("first steps occur")
        cyt = T("cytoplasm", 30, CELL).move_to([-3.25, 1.35, 0])
        self.play(FadeIn(cyt), Indicate(steps[:3], color=CELL), run_time=0.8)
        self.at("Most of the work")
        self.play(FadeIn(mito, scale=0.8), steps[3:].animate.set_color(MITO), run_time=1.1)
        ml = T("mitochondrion", 30, MITO, weight=BOLD).move_to([2.4, -1.2, 0])
        self.play(FadeIn(ml), run_time=0.5)
        self.at("Plant and animal cells")
        icons = VGroup(chip("plant cell", CELL, 24), chip("animal cell", CELL, 24), chip("fungus cell", CELL, 24)).arrange(RIGHT, buff=0.25).move_to([0, -2.0, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in icons[:2]], lag_ratio=0.2), run_time=0.8)
        self.at("Fungus cells usually")
        self.play(FadeIn(icons[2], shift=UP * 0.2), run_time=0.6)
        self.finish()


class S03bPlantParts(SpokenScene):
    def construct(self):
        cell = cell_picture()
        chl = Ellipse(width=3.1, height=1.65, color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.16).move_to([-2.8, 0.45, 0])
        mito = mitochondrion([2.8, 0.45, 0], 0.95)
        bob(chl, seed=1); bob(mito, seed=2)
        self.play(FadeIn(cell), FadeIn(chl), FadeIn(mito), run_time=0.8)
        self.add(scope_tag())
        self.at("Do not confuse")
        labs = VGroup(T("chloroplast", 31, GREEN, weight=BOLD).move_to([-2.8, 1.75, 0]),
                      T("mitochondrion", 31, MITO, weight=BOLD).move_to([2.8, 1.75, 0]))
        self.play(FadeIn(labs), run_time=0.7)
        self.at("Chloroplasts let a plant")
        sun = Circle(radius=0.36, color=YELLOW, fill_color=YELLOW, fill_opacity=0.8).move_to([-5.1, 0.45, 0])
        gl = glucose_block().move_to([-0.2, 0.45, 0])
        self.play(FadeIn(sun), GrowArrow(arrow(sun.get_right(), chl.get_left(), YELLOW)), run_time=0.7)
        self.play(GrowArrow(arrow(chl.get_right(), gl.get_left(), GREEN)), FadeIn(gl), run_time=0.7)
        self.at("Mitochondria let plant")
        self.play(GrowArrow(arrow(gl.get_right(), mito.get_left(), GLUCOSE)), run_time=0.8)
        self.at("release stored food energy")
        out = VGroup(arrow(mito.get_right(), [5.45, 0.9, 0], WORK), arrow(mito.get_right(), [5.45, -0.3, 0], HEAT))
        self.play(Create(out), run_time=0.9)
        self.at("both kinds of organelle")
        self.play(Indicate(VGroup(chl, mito), color=CELL, scale_factor=1.03), run_time=0.9)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        fork = energy_fork()
        self.play(FadeIn(fork[0]), GrowArrow(fork[2][0]), FadeIn(fork[1]), run_time=0.8)
        self.add(scope_tag())
        self.at("Where will that energy")
        self.play(Create(fork[2][1:]), run_time=0.8)
        self.at("power cell work")
        self.play(FadeIn(fork[3]), FadeIn(fork[5]), run_time=0.7)
        self.at("leave as warmth")
        self.play(FadeIn(fork[4]), FadeIn(fork[6]), run_time=0.7)
        self.at("or do both")
        self.play(Indicate(VGroup(fork[3], fork[4]), color=GLUCOSE, scale_factor=1.05), run_time=0.7)
        self.at("Make your prediction")
        q = question_card(PREDICT_Q, PREDICT_OPTIONS)
        self.play(FadeIn(q), run_time=0.6)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = PREDICT_Q
    OPTIONS = PREDICT_OPTIONS
    SECONDS = 4.5
    def backdrop(self):
        tag = T("schematic", 24, GREY).move_to([5.75, 3.45, 0])
        return VGroup(energy_fork(), tag)


class S06Reveal(SpokenScene):
    def construct(self):
        fork = energy_fork()
        self.add(fork, scope_tag())
        self.play(Indicate(VGroup(fork[3], fork[4]), color=GLUCOSE, scale_factor=1.07), run_time=0.8)
        self.at("One branch powers")
        self.play(Rotate(fork[3], angle=PI, run_time=2.0, rate_func=linear))
        self.at("building new cell parts")
        part = RoundedRectangle(corner_radius=0.12, width=1.0, height=0.62, color=WORK, stroke_width=4,
                                fill_color=WORK, fill_opacity=0.35).move_to([5.55, 1.15, 0])
        self.play(FadeOut(fork[5]), TransformFromCopy(fork[3], part), run_time=0.8)
        self.at("Another becomes thermal energy")
        box = RoundedRectangle(corner_radius=0.2, width=3.1, height=1.35, color=HEAT, stroke_width=3).move_to([2.7, -1.15, 0])
        self.play(Create(box), run_time=0.7)
        self.at("motion of particles")
        self.play(fork[4].animate.scale(1.18), run_time=1.2)
        self.at("always leaves")
        self.play(ShowPassingFlash(fork[2][2].copy().set_stroke(width=12), run_time=1.5), run_time=1.5)
        self.finish()


class S07Energy(SpokenScene):
    def construct(self):
        stored = glucose_block("stored energy", 30).move_to([-3.9, 0.6, 0])
        new = T("new energy", 34, RED, weight=BOLD).move_to([2.6, 2.1, 0])
        cross = Cross(new, stroke_color=RED, stroke_width=7)
        new.layout_ok = True
        cross.layout_ok = True  # intentional strike-through
        self.play(FadeIn(stored), FadeIn(new), Create(cross), run_time=0.8)
        self.add(scope_tag())
        self.at("changed energy")
        work = chip("cell work", WORK, 28).move_to([2.7, 0.9, 0])
        heat = chip("thermal energy", HEAT, 28).move_to([2.7, -0.8, 0])
        self.play(ReplacementTransform(stored.copy(), work), ReplacementTransform(stored, heat), FadeOut(new), FadeOut(cross), run_time=1.1)
        self.at("thermos slows")
        L, R = ValueTracker(-0.2), ValueTracker(-0.2)
        pair = thermos_pair(L, R).scale(0.88).move_to([0, -0.05, 0])
        pulse(pair[0][0], base=5.0, amp=2.2, speed=2.0)
        self.play(FadeOut(work), FadeOut(heat), FadeIn(pair), run_time=0.9)
        sparks = heat_particles([-3.75, -0.05, 0], n=12).scale(0.8)
        self.play(FadeIn(sparks), run_time=0.5)
        self.at("living pea cells keep respiring")
        self.play(L.animate.set_value(1.2), sparks.animate.shift(UP * 1.2), run_time=3.0)
        self.finish()


class S08Breathing(SpokenScene):
    def construct(self):
        tp = TwoPanel("breathing: lungs", "respiration: cells", colors=(GREY, MITO))
        lung_l = Ellipse(width=1.4, height=2.1, color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12)
        lungs = VGroup(lung_l.copy().move_to([-4.15, 0.45, 0]), lung_l.copy().move_to([-2.35, 0.45, 0]))
        cell = RoundedRectangle(corner_radius=0.45, width=4.5, height=2.5, color=CELL, stroke_width=5,
                                fill_color=CELL, fill_opacity=0.06)
        core = RoundedRectangle(corner_radius=0.25, width=3.5, height=1.2, color=MITO, stroke_width=5,
                                fill_color=MITO, fill_opacity=0.16)
        label = T("cellular respiration", 23, MITO, weight=BOLD).move_to(core)
        core.layout_ok = True
        label.layout_ok = True
        path = VGroup(cell, core, label)
        pulse(core, base=5.0, amp=2.0, speed=2.2)
        tp.put(lungs, "left"); tp.put(path, "right"); lungs.shift(UP * 0.3); path.shift(UP * 0.3)
        self.play(FadeIn(tp), FadeIn(lungs), FadeIn(path), run_time=0.9)
        self.add(scope_tag())
        self.at("moves air into")
        self.play(lungs.animate.scale(1.12), run_time=1.0, rate_func=there_and_back)
        for i, lung in enumerate(lungs):
            bob(lung, amp=0.08, speed=1.8, seed=i)
        self.at("brings oxygen in")
        oxy = oxygen_dots([-5.6, 1.45, 0], 4)
        co2 = chip("carbon dioxide", CO2, 24).move_to([-3.25, -1.75, 0])
        self.play(oxy.animate.move_to([-3.25, 0.9, 0]), FadeIn(co2), run_time=1.1)
        self.at("Respiration happens inside cells")
        self.play(Indicate(path, color=MITO, scale_factor=1.04), run_time=0.9)
        self.at("organisms without lungs")
        no_lungs = VGroup(chip("seed", CELL, 26), chip("yeast", CELL, 26)).arrange(RIGHT, buff=0.35).move_to([3.25, -1.85, 0])
        self.play(FadeIn(no_lungs, shift=UP * 0.2), run_time=0.8)
        self.finish()


class S09Control(SpokenScene):
    def construct(self):
        L, R = ValueTracker(-0.2), ValueTracker(-0.2)
        pair = thermos_pair(L, R, crossed=True)
        pulse(pair[0][0], base=5.0, amp=2.4, speed=2.0)
        self.play(FadeIn(pair), run_time=0.8)
        self.add(scope_tag())
        room = DashedLine([-6.1, -0.2, 0], [6.1, -0.2, 0], color=GREY, stroke_width=3)
        self.play(Create(room), run_time=0.6)
        self.at("living cells that keep")
        glows = VGroup(*[Circle(radius=0.33, color=HEAT, stroke_width=4).move_to(p.get_center()) for p in pair[0][2][::3]])
        for i, glow in enumerate(glows):
            pulse(glow, base=4.0, amp=2.0, speed=2.2 + 0.12 * i)
        self.play(LaggedStart(*[Create(x) for x in glows], lag_ratio=0.12), run_time=1.4)
        self.at("Boiling killed")
        dead = T("no living cells", 28, RED, weight=BOLD).move_to([2.9, -3.1, 0])
        self.play(FadeIn(dead), run_time=0.7)
        self.at("do not respire")
        self.play(Indicate(pair[1][7], color=RED, scale_factor=1.05), run_time=0.8)
        self.at("thermometer stays")
        self.play(L.animate.set_value(1.25), Indicate(pair[1][3], color=GREY), run_time=3.0)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        w = pathway_world()
        self.play(FadeIn(w), run_time=0.8)
        self.add(scope_tag())
        self.at("Respiration releases")
        rule = fit_text("Respiration releases stored food energy for cell work and as thermal energy.", max_w=12.6, size=26, color=TEXT, max_lines=1).move_to([0, 3.3, 0])
        self.play(Write(rule), run_time=2.3)
        self.at("explains the warmth")
        self.play(ShowPassingFlash(w[-1][-1].copy().set_stroke(width=11), run_time=1.3), run_time=1.3)
        self.at("temperature")
        temp = chip("temperature", HEAT, 25).move_to([-3.2, -3.05, 0])
        self.play(FadeIn(temp, shift=UP * 0.2), run_time=0.5)
        self.at("oxygen")
        oxy = chip("oxygen", OXYGEN, 25).move_to([0, -3.05, 0])
        self.play(FadeIn(oxy, shift=UP * 0.2), run_time=0.5)
        self.at("sugar")
        sug = glucose_block("glucose", 25).move_to([3.2, -3.05, 0])
        self.play(FadeIn(sug, shift=UP * 0.2), run_time=0.5)
        self.at("change its rate")
        for i, x in enumerate((temp, oxy, sug)):
            bob(x, seed=i)
        self.play(Indicate(VGroup(temp, oxy, sug), color=GLUCOSE, scale_factor=1.03), run_time=0.8)
        self.finish()


class S11End(EndCard):
    LINE = "Respiration releases stored food energy for cell work and as thermal energy."
