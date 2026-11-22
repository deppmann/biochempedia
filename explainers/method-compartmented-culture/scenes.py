"""Compartmented culture, drawn as a single overhead schematic.

Blue: apparatus. Grey: dividers. Teal: bath.
Purple: neurons and TrkA. Orange: NGF. Yellow: signalling.
Green: maintained structures. Red: loss or leakage. Gold: history and prediction.
"""
from bp_parts import *
from bp_style import EndCard

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
DRY = "#30374B"
BATH = "#205864"
LEFT_BATH = "#30516C"
RIGHT_BATH = "#226575"
MIXED = "#395E71"

LEFT_WALL, RIGHT_WALL = -1.70, 1.70
TOP, BOTTOM = 2.64, -2.44
EDGES = [-6.07, LEFT_WALL, RIGHT_WALL, 6.07]
QUESTION = "What happens to the left branches\nand to the same neuron's right branches?"

# The axon paths are cartoons, with each fork starting on its parent.
RIGHT_MAIN = [(0, 0.10), (0.68, 0.32), (1.34, 0.33), (2.20, 0.39),
              (3.14, 0.73), (4.04, 0.77), (5.12, 1.20)]
RIGHT_FORKS = [[(3.14, 0.73), (3.52, 0.22), (4.32, -0.19), (5.24, -0.35)],
               [(4.04, 0.77), (4.39, 1.42), (5.17, 1.84)],
               [(4.32, -0.19), (4.76, -0.81), (5.26, -1.12)]]
LEFT_MAIN = [(0, 0.10), (-0.69, -0.12), (-1.39, -0.20), (-2.13, -0.28),
             (-3.18, -0.65), (-4.07, -0.57), (-5.18, -1.13)]
LEFT_FORKS = [[(-3.18, -0.65), (-3.60, 0.08), (-4.32, 0.44), (-5.25, 0.56)],
              [(-4.07, -0.57), (-4.59, -1.40), (-5.19, -1.78)],
              [(-4.32, 0.44), (-4.63, 1.14), (-5.11, 1.55)]]


def point(x, y):
    return np.array([x, y, 0.0])


def fibre(coords, color=PURPLE, width=5):
    curve = VMobject(stroke_color=color, stroke_width=width)
    curve.set_points_smoothly([point(x, y) for x, y in coords])
    return curve


def axon(main, forks, color=PURPLE):
    return VGroup(fibre(main, color, 7), *(fibre(fork, color, 4.4) for fork in forks))


def box_at(x1, x2, y1, y2, fill, stroke=0, color=BLUE, radius=0.14):
    return RoundedRectangle(width=x2 - x1, height=y2 - y1, corner_radius=radius,
                            stroke_color=color, stroke_width=stroke, fill_color=fill,
                            fill_opacity=1).move_to(point((x1 + x2) / 2, (y1 + y2) / 2))


def cell(x, y, radius=0.53):
    outline = Polygon(*[point(a, b) for a, b in
                        [(-0.99, 0.05), (-0.56, 0.72), (-0.02, 1.04),
                         (0.68, 0.73), (1.02, 0.04), (0.57, -0.76),
                         (-0.13, -0.96), (-0.75, -0.62)]])
    outline.make_smooth()
    outline.scale(radius).move_to(point(x, y))
    outline.set_stroke(PURPLE, 3.5).set_fill("#76599D", 1)
    nucleus = Circle(radius=radius * 0.36, stroke_color="#E1C6FB", stroke_width=2.5,
                     fill_color="#4A3762", fill_opacity=1).move_to(point(x, y))
    return VGroup(outline, nucleus).set_z_index(3)


class CultureDish:
    """Rebuild one dish at fixed coordinates, with fluid and neurons layered over its floor."""

    def __init__(self):
        self.floor = box_at(-6.21, 6.21, BOTTOM, TOP, DRY, 4, radius=0.25)
        self.baths = VGroup(
            box_at(EDGES[0], EDGES[1], BOTTOM + 0.12, TOP - 0.12, LEFT_BATH),
            box_at(EDGES[1], EDGES[2], BOTTOM + 0.12, TOP - 0.12, BATH),
            box_at(EDGES[2], EDGES[3], BOTTOM + 0.12, TOP - 0.12, RIGHT_BATH),
        )
        self.uniform = box_at(-6.07, 6.07, BOTTOM + 0.12, TOP - 0.12, BATH, radius=0.18)
        self.walls = VGroup(*(self.wall(x) for x in (LEFT_WALL, RIGHT_WALL)))
        self.left = axon(LEFT_MAIN, LEFT_FORKS)
        self.right = axon(RIGHT_MAIN, RIGHT_FORKS)
        self.stump = fibre(LEFT_MAIN[:4], width=6)
        self.soma = cell(0, 0.10)
        self.neighbours = VGroup(cell(-0.43, 1.35, 0.29), cell(0.47, -1.17, 0.31))
        self.fields = [self.particles(i) for i in range(3)]

    @staticmethod
    def wall(x):
        return box_at(x - 0.12, x + 0.12, BOTTOM + 0.04, TOP - 0.04, "#516075",
                      2.7, GREY, radius=0.07)

    @staticmethod
    def particles(i):
        return particles(EDGES[i] + 0.33, EDGES[i + 1] - 0.33, -2.11, 2.28, seed=42 + i)

    def add_to(self, scene, *, divided=True, wet=(0, 1, 2), left=True, neighbours=True):
        scene.add(self.floor)
        if divided:
            scene.add(*(self.baths[i] for i in wet), *(self.fields[i] for i in wet), self.walls)
        else:
            scene.add(self.uniform, *self.fields)
        scene.add(self.left if left else self.stump, self.right, self.soma)
        if neighbours:
            scene.add(self.neighbours)

    def drain(self, scene, i, run_time=2.6):
        bath, field = self.baths[i], self.fields[i]
        field.clear_updaters()
        shallow = bath.copy().stretch_to_fit_height(0.04).align_to(bath, DOWN)
        scene.play(Transform(bath, shallow), FadeOut(field, shift=DOWN * 0.14),
                   run_time=run_time, rate_func=smooth)
        scene.remove(bath)


def particles(x1, x2, y1, y2, *, seed, n=27):
    """Drift NGF within its own bath. Reflections keep dots off walls and the rim."""
    rng = np.random.default_rng(seed)
    initial = rng.random((n, 2))
    velocities = rng.uniform(-0.23, 0.23, (n, 2))
    low = np.array([x1, y1])
    span = np.array([x2 - x1, y2 - y1])
    dots = VGroup(*(Dot(radius=r, color=ORANGE, fill_opacity=a, stroke_width=0)
                    for r, a in zip(rng.uniform(0.055, 0.104, n), rng.uniform(0.62, 0.94, n))))
    time = 0.0

    def drift(group, dt):
        nonlocal time
        time += dt
        locations = low + span * (1 - np.abs((initial + time * velocities) % 2 - 1))
        for dot, (x, y) in zip(group, locations):
            dot.move_to(point(x, y))

    drift(dots, 0)
    return dots.add_updater(drift)


def heading(text, color=TEXT, x=0, size=32):
    return T(text, size, color).move_to(point(x, 3.16))


def footer(text, color=TEXT):
    return caption(text, size=30, color=color, y=-3.09).set_x(0)


def forecast():
    return question_card(QUESTION, y=-3.15, size=30, max_w=11.6).set_x(0)


def wave(path, color=YELLOW, size=0.15):
    """A highlight on a path, used for a signal with unspecified carrier."""
    return VGroup(Dot(path.get_start(), radius=size * 1.9, color=color, fill_opacity=0.25),
                  Dot(path.get_start(), radius=size, color=color)).set_z_index(4)


def incoming_path():
    return fibre(RIGHT_MAIN[::-1])


def illuminate(soma):
    return soma[1].animate.set_stroke(YELLOW, 3).set_fill("#C19F43", 1)


class S01Hook(SpokenScene):
    def construct(self):
        dish = CultureDish()
        self.add(dish.floor, dish.uniform)
        self.at("When a neuron")
        self.play(GrowFromCenter(dish.soma), run_time=0.52)
        self.play(Create(dish.right), Create(dish.left), run_time=1.00)
        self.at("which end")
        marks = VGroup(T("?", 48, GOLD).move_to(point(0, 1.42)),
                       T("?", 48, GOLD).move_to(point(5.57, 1.83)))
        for i, mark in enumerate(marks):
            bob(mark, amp=0.13, speed=2.0, seed=i)
        self.play(FadeIn(marks), run_time=0.40)
        self.at("Developing sympathetic")
        self.play(FadeOut(marks), run_time=0.40)
        self.at("nerve growth factor", lead=0.85)
        self.play(*(FadeIn(f) for f in dish.fields), run_time=0.85)
        self.at("or NGF")
        key = footer("NGF", ORANGE)
        self.play(FadeIn(key), run_time=0.42)
        self.at("In an ordinary dish")
        self.play(FadeOut(key), run_time=0.32)
        self.at("one fluid bathes")
        self.play(dish.uniform.animate.set_fill("#2B6775"), run_time=2.0)
        self.at("So you cannot tell")
        self.play(dish.uniform.animate.set_fill(BATH), FadeIn(marks), run_time=1.2)
        self.play(FadeOut(marks), run_time=0.5)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Compartmented Culture"
    TITLE = "One Neuron in Separate Chambers"

    def construct(self):
        dish = CultureDish()
        dish.add_to(self, divided=False, neighbours=False)
        title = fit_text(self.TITLE, max_w=12.2, size=43, min_size=29,
                         font=TITLE_FONT).move_to(point(0, 3.22))
        self.play(FadeIn(title), run_time=0.42)
        self.wait(1.16)
        self.play(FadeOut(title), run_time=0.42)


class S03Chamber(SpokenScene):
    def construct(self):
        dish = CultureDish()
        dish.add_to(self, divided=False, neighbours=False)
        name = heading("Campenot, 1977", GOLD)
        self.at("1977")
        self.play(FadeIn(name), run_time=0.48)
        self.at("divided one dish", lead=0.45)
        self.play(FadeIn(dish.walls, shift=UP * 0.30), run_time=1.55)
        self.bring_to_front(dish.left, dish.right, dish.soma)
        self.at("barrier sealed")
        self.play(dish.walls.animate.set_stroke(TEXT, 4.0), run_time=0.75)
        self.play(dish.walls.animate.set_stroke(GREY, 2.7), run_time=0.95)
        self.at("central chamber")
        chambers = VGroup(heading("Side chamber", x=-3.92, size=29),
                          heading("Central chamber", size=29),
                          heading("Side chamber", x=3.92, size=29))
        self.play(swap(name, chambers), run_time=0.85)
        self.at("sympathetic cell bodies")
        self.play(FadeIn(dish.neighbours, shift=DOWN * 0.16), run_time=1.03)
        self.at("Their axons grow", lead=0.48)
        # Trace the existing paths under the newly installed seal.
        for side in (dish.left, dish.right):
            side.set_stroke(opacity=0.22)
        left, right = axon(LEFT_MAIN, LEFT_FORKS), axon(RIGHT_MAIN, RIGHT_FORKS)
        self.play(Create(left), Create(right), run_time=2.35)
        self.remove(dish.left, dish.right)
        self.at("the fluids stay apart")
        self.add(*dish.baths)
        self.bring_to_back(*dish.baths)
        self.bring_to_back(dish.floor)
        self.play(FadeOut(dish.uniform), FadeOut(chambers), run_time=1.20)
        self.at("each chamber's bath")
        self.play(dish.baths[0].animate.set_fill("#2B496A"),
                  dish.baths[2].animate.set_fill("#277382"), run_time=1.25)
        self.play(dish.baths[0].animate.set_fill(LEFT_BATH),
                  dish.baths[2].animate.set_fill(RIGHT_BATH), run_time=1.0)
        self.finish()


class S04PredictQ(SpokenScene):
    def construct(self):
        dish = CultureDish()
        dish.add_to(self)
        self.at("away from one side")
        left = footer("Left chamber", ORANGE)
        self.play(FadeIn(left), dish.baths[0].animate.set_fill("#3C5973"), run_time=1.12)
        self.at("Keep it on")
        keep = footer("NGF stays in centre and right", ORANGE)
        self.play(swap(left, keep), run_time=0.80)
        self.at("Drain it from", lead=0.45)
        self.play(FadeOut(keep), run_time=0.35)
        dish.drain(self, 0, run_time=2.2)
        self.at("What happens", lead=0.36)
        self.play(FadeIn(forecast()), run_time=0.55)
        self.finish()


class S05PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        dish = CultureDish()
        dish.add_to(self, wet=(1, 2))
        self.add(forecast())
        self.wait(float(os.environ["KX_DURATION"]))


def fragments(branches):
    pieces = VGroup()
    for branch in branches:
        for a, b in [(0.05, 0.23), (0.30, 0.48), (0.57, 0.71), (0.81, 0.91)]:
            piece = branch.copy().pointwise_become_partial(branch, a, b)
            pieces.add(piece)
    return pieces


class S06Outcomes(SpokenScene):
    def construct(self):
        dish = CultureDish()
        dish.add_to(self, wet=(1, 2))
        q = forecast()
        self.add(q)
        self.at("left axons")
        self.play(FadeOut(q), run_time=0.36)
        self.at("stop growing")
        bare = VGroup(fibre(LEFT_MAIN[3:], width=7), *[fibre(b, width=4.4) for b in LEFT_FORKS])
        self.remove(dish.left)
        self.add(dish.stump, bare)
        self.play(bare.animate.set_stroke(RED), run_time=0.85)
        self.at("later degenerate")
        pieces = fragments(bare)
        self.remove(bare)
        self.add(pieces)
        self.play(LaggedStart(*(FadeOut(piece, shift=point(-0.12, 0.17 * (-1)**i))
                                for i, piece in enumerate(pieces)), lag_ratio=0.16), run_time=3.0)
        self.at("branches next door")
        intact = footer("Right branches stay", GREEN)
        self.play(FadeIn(intact), dish.right.animate.set_stroke(GREEN), run_time=1.8)
        self.at("pruning in miniature")
        self.play(dish.right.animate.set_stroke(PURPLE), FadeOut(intact), run_time=1.55)
        self.at("drain the factor", lead=0.4)
        dish.drain(self, 1, run_time=2.45)
        self.at("only the axons", lead=0.1)
        self.play(dish.neighbours.animate.set_opacity(0.26), run_time=0.82)
        self.at("ends reach NGF", lead=0.3)
        path = incoming_path()
        self.play(MoveAlongPath(wave(path), path, remover=True,
                                rate_func=linear), run_time=1.84)
        self.at("many cell bodies", lead=0.25)
        survivor = dish.neighbours[0].copy().set_opacity(1)
        survivor[1].set_stroke(YELLOW, 3).set_fill("#C19F43", 1)
        self.play(illuminate(dish.soma), Transform(dish.neighbours[0], survivor), run_time=0.95)
        self.play(FadeIn(footer("Cell bodies survive", GREEN)), run_time=0.45)
        self.finish()


class S07GuidingIdea(SpokenScene):
    def construct(self):
        dish = CultureDish()
        dish.add_to(self, wet=(2,), left=False)
        dish.soma[1].set_stroke(YELLOW, 3).set_fill("#C19F43", 1)
        dish.neighbours[0][1].set_stroke(YELLOW, 3).set_fill("#C19F43", 1)
        dish.neighbours[1].set_opacity(0.26)
        survival = footer("Cell bodies survive", GREEN)
        self.add(survival)
        self.at("Separating the two")
        self.play(FadeOut(survival), FadeOut(dish.neighbours), run_time=0.65)
        self.at("where a signal acts")
        self.play(dish.walls[1].animate.set_stroke(TEXT, 4), run_time=1.2)
        self.at("whether it travels")
        focus = VGroup(dish.soma, dish.right, dish.stump)
        self.play(focus.animate.scale(1.08, about_point=ORIGIN),
                  dish.walls[1].animate.set_stroke(GREY, 2.7), run_time=1.55)
        def zoomed(coords):
            return [(1.08 * x, 1.08 * y) for x, y in coords]

        tip = zoomed(RIGHT_MAIN)[-1]
        receptor = RoundedRectangle(width=0.20, height=0.26, corner_radius=0.06,
                                    stroke_color=PURPLE, stroke_width=3,
                                    fill_color="#76599D", fill_opacity=1).move_to(point(*tip))
        protein = Dot(point(tip[0] - 0.29, tip[1] - 0.12), radius=0.11, color=YELLOW)
        halo = Circle(radius=0.32, color=YELLOW, stroke_width=3).move_to(protein)
        pulse(halo, base=4, amp=1.7, speed=3.0)
        growth = fibre(zoomed([RIGHT_MAIN[-1], (5.24, 1.24), (5.46, 1.40), (5.51, 1.61)]),
                       width=4)
        self.at("Axons grow only", lead=0.35)
        self.play(FadeIn(halo), run_time=0.48)
        self.play(Create(growth), run_time=2.45)
        local = footer("Local axon growth", PURPLE)
        self.play(FadeIn(local), run_time=0.45)
        self.at("Signaling proteins", lead=0.55)
        self.play(FadeIn(protein), FadeIn(receptor), run_time=0.55)
        self.at("the receptor at")
        work = footer("Signaling proteins at the tip", YELLOW)
        self.play(swap(local, work), run_time=0.80)
        self.at("that local work")
        self.play(protein.animate.scale(1.30), run_time=1.20, rate_func=there_and_back)
        self.at("Survival is the part")
        self.play(FadeOut(halo), FadeOut(protein), FadeOut(receptor), FadeOut(work),
                  dish.soma[1].animate.set_fill("#4A3762", 1), run_time=1.0)
        self.at("needs the nucleus")
        nucleus = footer("Nucleus", PURPLE)
        halo = Circle(radius=dish.soma[1].width / 2 + 0.13, color=PURPLE,
                      stroke_width=3).move_to(dish.soma[1])
        self.play(Create(halo), FadeIn(nucleus), run_time=0.80)
        self.at("only the tips touch")
        self.play(FadeOut(halo), FadeOut(nucleus), FadeOut(growth),
                  focus.animate.scale(1 / 1.08, about_point=ORIGIN), run_time=1.22)
        self.at("a signal must", lead=0.18)
        path = incoming_path()
        self.play(MoveAlongPath(wave(path), path, remover=True, rate_func=linear), run_time=1.55)
        self.play(illuminate(dish.soma), run_time=0.45)
        self.finish()


class S08ControlsLimits(SpokenScene):
    def construct(self):
        dish = CultureDish()
        dish.add_to(self, wet=(2,), left=False, neighbours=False)
        dish.soma[1].set_stroke(YELLOW, 3).set_fill("#C19F43", 1)
        self.add(dish.baths[1].set_fill(DRY))
        self.bring_to_back(dish.baths[1])
        self.bring_to_back(dish.floor)
        self.at("the seal leaks")
        gap = dish.walls[1].copy().stretch_to_fit_height(3.80).align_to(dish.walls[1], UP)
        gap.set_stroke(RED, 3.8)
        self.play(Transform(dish.walls[1], gap), run_time=0.55)
        self.at("fluids mix")
        leak = heading("Seal leak", RED)
        across = fibre([(4.8, -1.44), (2.6, -1.96), (1.78, -1.91), (0.76, -1.64),
                        (-0.70, -1.43)])
        self.play(FadeIn(leak), dish.baths[1].animate.set_fill(MIXED),
                  dish.baths[2].animate.set_fill(MIXED),
                  MoveAlongPath(wave(across, ORANGE), across, remover=True, rate_func=linear),
                  run_time=1.8)
        self.play(FadeOut(leak), Transform(dish.walls[1], dish.wall(RIGHT_WALL)),
                  dish.baths[1].animate.set_fill(DRY), dish.baths[2].animate.set_fill(RIGHT_BATH),
                  run_time=1.05)

        self.at("Putting a factor straight")
        drop = Dot(point(0, 2.05), radius=0.18, color=ORANGE)
        self.play(FadeIn(drop), run_time=0.35)
        self.play(drop.animate.move_to(point(0, 0.85)), run_time=1.2)
        self.at("bypasses the trip")
        arrow = Arrow(point(4.86, -1.14), point(0.95, -1.14), buff=0, color=YELLOW,
                      stroke_width=5)
        slash = Line(point(2.52, -1.46), point(3.08, -0.82), color=RED, stroke_width=8)
        direct = footer("Direct to the cell body", ORANGE)
        self.play(GrowArrow(arrow), FadeIn(direct), run_time=0.65)
        self.play(Create(slash), FadeOut(drop), run_time=0.48)
        self.at("Testing both sides")
        self.play(FadeOut(VGroup(arrow, slash, direct)), run_time=0.40)
        self.play(dish.soma[1].animate.set_fill("#4A3762", 1),
                  dish.right.animate.set_stroke(GREEN), run_time=1.45)
        self.at("signals sent home")
        path = incoming_path()
        self.play(dish.right.animate.set_stroke(PURPLE),
                  MoveAlongPath(wave(path), path, remover=True, rate_func=linear), run_time=1.55)

        self.at("NGF itself travels")
        ngf = heading("NGF itself?", YELLOW, x=3.65)
        faster = heading("Faster signal?", YELLOW, x=-2.75)
        self.play(FadeIn(ngf), MoveAlongPath(wave(path), path, remover=True, rate_func=linear),
                  run_time=1.76)
        self.at("a faster signal")
        self.play(FadeIn(faster), MoveAlongPath(wave(path), path, remover=True, rate_func=linear),
                  run_time=1.13)
        self.at("stays open")
        self.play(FadeOut(VGroup(ngf, faster)), run_time=0.6)
        self.at("every arriving signal")
        unresolved = footer("Is arrival enough?", GOLD)
        self.play(FadeIn(unresolved),
                  MoveAlongPath(wave(path), path, remover=True, rate_func=linear), run_time=1.70)
        self.finish()


MICRO_MAIN = [(-3.06, -0.46), (-2.35, -0.55), (-1.45, -0.55), (1.45, -0.55),
              (2.55, -0.56), (3.60, -0.34), (4.72, 0.16)]
MICRO_FORKS = [[(3.60, -0.34), (4.12, -0.80), (4.86, -1.12)],
               [(4.12, -0.80), (4.27, -1.32), (4.94, -1.49)],
               [(3.60, -0.34), (4.07, 0.45), (4.83, 0.77)]]
DENDRITES = [[(-3.06, -0.46), (-3.63, 0.04), (-4.05, 0.76), (-4.67, 1.22)],
             [(-3.63, 0.04), (-4.27, 0.20), (-4.91, 0.56)],
             [(-3.06, -0.46), (-3.63, -0.69), (-4.24, -1.04), (-4.93, -1.45)],
             [(-4.24, -1.04), (-4.75, -0.88), (-5.13, -0.68)]]


class MicrofluidicChamber:
    def __init__(self):
        self.plate = box_at(-5.70, 5.70, -2.30, 2.42, DRY, 4, radius=0.23)
        self.wells = VGroup(box_at(-5.51, -1.45, -2.08, 2.18, BATH),
                            box_at(1.45, 5.51, -2.08, 2.18, RIGHT_BATH))
        self.grooves = VGroup(*(box_at(-1.54, 1.54, y - 0.115, y + 0.115,
                                      "#38687F", radius=0.08)
                                for y in (-1.24, -0.90, -0.55, -0.20, 0.15)))
        self.dendrites = VGroup(*(fibre(coords, width=4.8) for coords in DENDRITES)).set_z_index(2)
        self.axon = axon(MICRO_MAIN, MICRO_FORKS).set_z_index(2)
        self.soma = cell(-3.06, -0.46)
        self.body = VGroup(self.dendrites, self.axon, self.soma)

    def geometry(self):
        return VGroup(self.plate, self.grooves, self.wells, self.body)

    @staticmethod
    def ngf():
        return particles(1.75, 5.27, -1.87, 1.94, seed=47, n=38).set_z_index(1)

    @staticmethod
    def receptor():
        return Square(side_length=0.24, color=PURPLE, fill_color=PURPLE, fill_opacity=1
                      ).move_to(point(*MICRO_MAIN[-1])).set_z_index(3)

    @staticmethod
    def tagged_dots():
        return VGroup(*(Dot(fibre(coords).point_from_proportion(t), radius=0.11, color=PURPLE)
                        for coords in DENDRITES for t in (0.63, 0.88))).set_z_index(4)

    @staticmethod
    def clusters():
        clusters = VGroup()
        for coords in (DENDRITES[0], DENDRITES[2], DENDRITES[3]):
            x, y = coords[-1]
            clusters.add(VGroup(*(Dot(point(x + dx, y + dy), radius=0.071, color=GREEN)
                                  for dx, dy in ((-0.16, 0.13), (-0.11, 0.30), (-0.30, 0.22)))))
        return clusters.set_z_index(4)


class S09Unlocked1(SpokenScene):
    def construct(self):
        dish = CultureDish()
        dish.add_to(self, wet=(2,), left=False, neighbours=False)
        unresolved = footer("Is arrival enough?", GOLD)
        self.add(unresolved)
        self.at("First")
        self.play(FadeOut(unresolved), run_time=0.33)
        campenot = heading("Campenot, 1977", GOLD)
        self.play(FadeIn(campenot), run_time=0.65)
        self.at("local axon growth", lead=0.4)
        lost = footer("Left axons degenerate", RED)
        bare = axon(LEFT_MAIN[3:], LEFT_FORKS, RED)
        self.play(FadeIn(bare), run_time=0.33)
        self.play(FadeOut(bare), FadeIn(lost), run_time=1.2)
        self.at("survival signals", lead=0.40)
        survives = footer("Axon NGF supports survival", GREEN)
        path = incoming_path()
        self.play(swap(lost, survives), MoveAlongPath(wave(path), path, remover=True, rate_func=linear),
                  run_time=1.66)
        self.play(illuminate(dish.soma), run_time=0.46)

        self.at("Second")
        self.play(FadeOut(VGroup(campenot, survives)), run_time=0.38)
        micro = MicrofluidicChamber()
        dish.fields[2].clear_updaters()
        self.play(ReplacementTransform(dish.floor, micro.plate),
                  FadeOut(VGroup(dish.baths[2], dish.fields[2], dish.stump)),
                  ReplacementTransform(dish.walls, micro.grooves),
                  ReplacementTransform(dish.right, micro.axon),
                  ReplacementTransform(dish.soma, micro.soma),
                  FadeIn(VGroup(micro.wells, micro.dendrites)), run_time=2.55)
        self.remove(micro.plate, micro.grooves, micro.axon, micro.soma, micro.wells, micro.dendrites)
        self.add(micro.geometry())
        self.play(FadeIn(heading("Noo Li Jeon", GOLD)), run_time=0.40)
        self.at("the microfluidic chamber")
        self.play(FadeIn(footer("Microfluidic chamber", BLUE)), run_time=0.45)
        self.finish()


class S09bUnlocked1b(SpokenScene):
    def construct(self):
        micro = MicrofluidicChamber()
        self.add(micro.geometry())
        footer_label = footer("Microfluidic chamber", BLUE)
        name = heading("Noo Li Jeon", GOLD)
        self.add(footer_label, name)
        self.at("Axons there got")
        self.play(FadeOut(name), run_time=0.32)
        field = micro.ngf()
        self.play(FadeIn(field, shift=LEFT * 0.14),
                  micro.wells[1].animate.set_fill("#2F7781"), run_time=0.88)
        self.at("their receptor")
        terminal = micro.receptor()
        self.play(GrowFromCenter(terminal), micro.wells[1].animate.set_fill(RIGHT_BATH),
                  run_time=0.92)
        self.at("carried a tag")
        flagged = footer("Flag-TrkA", PURPLE)
        self.play(swap(footer_label, flagged), run_time=0.67)
        self.at("Over six hours", lead=0.48)
        timer = ValueTracker(0)
        gauge = dial(timer, point(0, 1.39), radius=0.91, color=GOLD, size=28, fmt="{:.0f} h", scale=6)
        dots = micro.tagged_dots()
        self.play(FadeIn(gauge), run_time=0.48)
        self.play(timer.animate.set_value(1),
                  LaggedStart(*(GrowFromCenter(dot) for dot in dots), lag_ratio=0.35),
                  run_time=5.4, rate_func=linear)
        self.at("compared with clustering", lead=0.42)
        self.play(FadeOut(gauge), run_time=0.40)
        clusters = micro.clusters()
        compared = footer("Postsynaptic protein clusters", GREEN)
        self.play(LaggedStart(*(GrowFromCenter(c) for c in clusters), lag_ratio=0.40),
                  swap(flagged, compared), run_time=3.3)
        self.finish()


ACTIVE_INPUT = [(-4.32, 1.07), (-3.65, 0.98), (-2.5, 0.85), (-1.10, 0.83), (0.93, 0.80)]
LOW_INPUT = [(-4.32, -1.01), (-3.61, -0.97), (-2.88, -0.89), (-1.12, -0.81), (0.93, -0.80)]


class NerveMuscleChamber:
    def __init__(self):
        self.plate = box_at(-5.93, 5.93, -2.44, 2.64, DRY, 4, radius=0.24)
        self.wells = VGroup(box_at(-5.78, -1.22, -2.28, 2.47, BATH),
                            box_at(-1.22, 5.78, -2.28, 2.47, "#345165"))
        self.seal = box_at(-1.34, -1.10, -2.40, 2.60, "#516075", 2.6, GREY, radius=0.07)
        self.muscle = box_at(0.61, 5.31, -1.84, 1.87, "#69466E", 3.5,
                             PURPLE, radius=0.68)
        self.stripes = VGroup(*(Line(point(x, -1.47), point(x, 1.47),
                                     color="#8F6B96", stroke_width=2.0)
                               for x in (1.55, 2.16, 2.77, 3.38, 3.99, 4.60)))
        self.active = fibre(ACTIVE_INPUT, width=7).set_z_index(2)
        self.quiet = fibre(LOW_INPUT, width=7).set_z_index(2)
        self.cells = VGroup(cell(*ACTIVE_INPUT[0], 0.48), cell(*LOW_INPUT[0], 0.48))
        self.receptors = VGroup(self.cluster(0.80), self.cluster(-0.80))

    @staticmethod
    def cluster(y):
        return VGroup(*(Dot(point(x, y + dy), radius=0.085, color=PURPLE, stroke_width=0)
                        for x, dy in ((1.02, 0.23), (1.27, 0.23), (1.50, 0.16), (1.17, 0),
                                      (1.49, -0.03), (1.02, -0.23), (1.29, -0.23)))).set_z_index(4)

    def activity(self):
        """Show repeated activity travelling down the stimulated input to its synapse."""
        path = self.active
        glow = path.copy().set_stroke(YELLOW, width=31, opacity=0.54).set_z_index(1)
        core = path.copy().set_stroke(YELLOW, width=9, opacity=1).set_z_index(4)
        tip = Dot(radius=0.46, color=YELLOW, stroke_width=0).set_z_index(3)
        beat = VGroup(glow, core, tip)
        elapsed = 0.0

        def travel(group, dt):
            nonlocal elapsed
            elapsed += dt
            head = (elapsed / 2.80) % 1.0
            a, b = max(0.0, 1.4 * head - 0.45), min(1.0, 1.4 * head + 0.03)
            glow.pointwise_become_partial(path, a, b)
            core.pointwise_become_partial(path, a, b)
            brightness = np.sin(PI * head) ** 0.42
            glow.set_stroke(YELLOW, width=31, opacity=0.65 * brightness)
            core.set_stroke(YELLOW, width=9, opacity=brightness)
            tip.move_to(path.get_end() + RIGHT * 0.22)
            tip.set_fill(YELLOW, 0.6 * np.exp(-((head - 0.78) / 0.13)**2))

        travel(beat, 0)
        return beat.add_updater(travel)


class S10Unlocked2(SpokenScene):
    def construct(self):
        micro = MicrofluidicChamber()
        nm = NerveMuscleChamber()
        self.add(micro.geometry())
        ngf = micro.ngf()
        data = VGroup(ngf, micro.receptor(), micro.tagged_dots(), micro.clusters())
        previous = footer("Postsynaptic protein clusters", GREEN)
        self.add(data, previous)
        self.at("Nelson's laboratory", lead=0.48)
        who = heading("Phillip Nelson’s laboratory", GOLD)
        ngf.clear_updaters()
        self.play(FadeIn(who), FadeOut(data), FadeOut(previous), run_time=0.55)
        self.at("compartmented nerve muscle", lead=0.7)
        self.play(ReplacementTransform(micro.plate, nm.plate),
                  ReplacementTransform(micro.wells, nm.wells),
                  ReplacementTransform(micro.grooves, nm.seal),
                  ReplacementTransform(micro.axon, nm.active),
                  FadeOut(VGroup(micro.dendrites, micro.soma)),
                  FadeIn(nm.muscle), FadeIn(nm.stripes), FadeIn(nm.quiet), FadeIn(nm.cells),
                  run_time=2.45)
        self.remove(nm.plate, nm.wells, nm.seal, nm.muscle, nm.stripes, nm.active, nm.quiet, nm.cells)
        self.add(nm.plate, nm.wells, nm.seal, nm.muscle, nm.stripes, nm.active, nm.quiet, nm.cells)
        self.play(FadeIn(nm.receptors), run_time=0.68)
        stimulation = nm.activity()
        self.add(stimulation)

        self.at("kinase C", lead=0.35)
        pkc = footer("PKC", RED)
        self.play(FadeOut(who), FadeIn(pkc), run_time=0.70)
        self.at("heterosynaptic loss")
        self.play(nm.quiet.animate.set_stroke(RED),
                  nm.receptors[1].animate.set_color(RED), run_time=1.50)
        self.at("activity at one input", lead=0.36)
        self.play(LaggedStart(*(ShrinkToCenter(r) for r in nm.receptors[1]), lag_ratio=0.38),
                  run_time=2.05)
        self.at("less active neighbor")
        self.play(FadeOut(nm.quiet), FadeOut(pkc), run_time=1.5)
        self.at("kinase A", lead=0.25)
        pka = footer("PKA", GREEN)
        self.play(FadeIn(pka), run_time=0.45)
        self.at("stabilized the stimulated")
        self.play(nm.receptors[0].animate.set_color(GREEN), run_time=1.30)
        self.at("acted through")
        receptors = footer("Acetylcholine receptors", TEXT)
        self.play(swap(pka, receptors), run_time=0.85)
        self.at("receptor numbers")
        self.play(nm.receptors[0].animate.set_color(PURPLE), run_time=1.45)

        self.at("Dividing a neuron's bath", lead=0.52)
        dish = CultureDish()
        stimulation.clear_updaters()
        self.play(FadeOut(receptors), FadeOut(stimulation),
                  FadeOut(VGroup(nm.active, nm.cells, nm.muscle, nm.stripes, nm.receptors[0])),
                  run_time=0.40)
        self.play(ReplacementTransform(nm.plate, dish.floor),
                  ReplacementTransform(nm.wells, dish.baths[2]),
                  ReplacementTransform(nm.seal, dish.walls),
                  FadeIn(VGroup(dish.stump, dish.right, dish.soma)),
                  FadeIn(dish.fields[2]), run_time=1.62)
        self.at("where signals act")
        path = incoming_path()
        self.play(MoveAlongPath(wave(path), path, remover=True, rate_func=linear), run_time=2.17)
        self.play(illuminate(dish.soma), run_time=0.68)
        self.finish()


class S11End(EndCard):
    LINE = "Separate cell body and axon fluids to test where signals act."
