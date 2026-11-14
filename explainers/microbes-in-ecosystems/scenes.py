"""Who Unlocks the Matter? — microbes in ecosystems.

COLOR MAP (kept for the whole film)
  PALE_BLUE = nitrogen gas paired dots
  GREEN     = ammonium (inside the nodule only)
  TEAL      = fixed nitrogen carried through the plant
  GOLD      = plant sugar / mutual benefit
  ORANGE    = phosphorus / enzyme action
  PURPLE    = bacteria
  TEXT      = fungal threads
  RED       = harmful particles / illness
  GREY      = locked matter and neutral structure

All pictures are schematic labelled cartoons, never molecular structures.
"""
from bp_parts import *  # noqa: F401,F403


PALE_BLUE = "#9DD9F3"
PURPLE = "#B58CD9"
ORANGE_M = "#F29E4C"
BROWN = "#A67C52"
SOIL = "#70513C"
DARK_GREY = "#667078"


class ActiveSpokenScene(SpokenScene):
    """Shared ecosystem stage: a filled field and slow matter drift behind each spoken scene.

    The field makes the diagram the dominant picture rather than thin marks on black.  The neutral
    motes are visual texture, not an extra biological species or molecule.
    """
    def setup(self):
        super().setup()
        stage = RoundedRectangle(corner_radius=0.32, width=13.15, height=7.05,
                                 stroke_color=DARK_GREY, stroke_width=2,
                                 fill_color="#26343D", fill_opacity=1).set_z_index(-30)
        stage.layout_ok = True  # intentional full-frame background field
        rng = np.random.default_rng(sum(ord(c) for c in os.environ.get("KX_SCENE_ID", "scene")))
        motes = VGroup()
        for _ in range(96):
            m = Dot(radius=0.07, color=GREY).set_opacity(0.52)
            m.move_to([rng.uniform(-6.25, 6.25), rng.uniform(-3.25, 3.25), 0])
            m.v = np.array([rng.uniform(-0.75, 0.75), rng.uniform(0.55, 1.0), 0])

            def drift(mob, dt):
                mob.shift(mob.v * dt)
                if mob.get_y() > 3.35:
                    mob.shift(DOWN * 6.65)
                if mob.get_x() > 6.35:
                    mob.shift(LEFT * 12.65)
                elif mob.get_x() < -6.35:
                    mob.shift(RIGHT * 12.65)
            m.add_updater(drift)
            m.layout_ok = True  # intentional background texture may drift behind labels
            motes.add(m)
        motes.set_z_index(-29)
        self.add(stage, motes)


def arrow(a, b, color=GREY, width=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.4)


def bacterium(at=ORIGIN, color=PURPLE, scale=1.0):
    return RoundedRectangle(corner_radius=0.16 * scale, width=0.65 * scale,
                            height=0.25 * scale, stroke_color=color, stroke_width=2,
                            fill_color=color, fill_opacity=0.75).rotate(0.18).move_to(at)


def paired_nitrogen(at=ORIGIN, scale=1.0):
    a = Dot(radius=0.11 * scale, color=PALE_BLUE).shift(LEFT * 0.13 * scale)
    b = Dot(radius=0.11 * scale, color=PALE_BLUE).shift(RIGHT * 0.13 * scale)
    return VGroup(a, b).move_to(at)


def padlock(at=ORIGIN, scale=1.0, opened=False):
    body = RoundedRectangle(corner_radius=0.09, width=0.58, height=0.48,
                            stroke_color=GREY, fill_color=GREY, fill_opacity=0.35,
                            stroke_width=3).move_to(DOWN * 0.16)
    shackle = Arc(radius=0.22, start_angle=0, angle=PI, color=GREY,
                  stroke_width=4).move_to(UP * 0.08)
    if opened:
        shackle.rotate(-0.7, about_point=shackle.get_right()).shift(RIGHT * 0.08)
    return VGroup(body, shackle).scale(scale).move_to(at)


def tracker(states=(False, False, False)):
    """The carried locked→usable tracker, always at exactly the same coordinates."""
    line = Line([-5.6, -3.15, 0], [5.6, -3.15, 0], color=GREY, stroke_width=5)
    left = T("locked", 28, GREY).move_to([-5.55, -3.52, 0])
    right = T("usable", 28, TEAL).move_to([5.45, -3.52, 0])
    xs = [-3.6, 0, 3.6]
    icons = VGroup(*[padlock([5.0 if ok else x, -3.15, 0], 0.58, ok)
                     for x, ok in zip(xs, states)])
    g = VGroup(line, left, right, icons)
    g.icons = icons
    return g


def soil_band():
    soil = Rectangle(width=13.4, height=2.7, stroke_width=0,
                     fill_color=SOIL, fill_opacity=0.42).move_to([0, -2.15, 0])
    surface = Line([-6.7, -0.8, 0], [6.7, -0.8, 0], color=BROWN, stroke_width=4)
    return VGroup(soil, surface)


def soybean_world(with_people=True):
    """Wide cut-away field used for the opening question."""
    soil = soil_band()
    stem = Line([-2.7, -0.8, 0], [-2.7, 2.15, 0], color=GREEN, stroke_width=12)
    leaves = VGroup(
        Ellipse(1.2, 0.52, color=GREEN, fill_color=GREEN, fill_opacity=0.55).rotate(0.35).move_to([-3.2, 1.5, 0]),
        Ellipse(1.2, 0.52, color=GREEN, fill_color=GREEN, fill_opacity=0.55).rotate(-0.35).move_to([-2.2, 1.1, 0]),
        Ellipse(1.0, 0.46, color=GREEN, fill_color=GREEN, fill_opacity=0.55).rotate(0.25).move_to([-3.1, 0.5, 0]))
    roots = VGroup(Line([-2.7, -0.8, 0], [-3.4, -2.25, 0], color=GOLD, stroke_width=6),
                   Line([-2.7, -0.8, 0], [-2.0, -2.3, 0], color=GOLD, stroke_width=6),
                   Line([-2.7, -1.15, 0], [-1.35, -1.7, 0], color=GOLD, stroke_width=4))
    plant = VGroup(stem, leaves, roots)
    if not with_people:
        return VGroup(soil, plant)
    # A deer and teenager are simple, clearly distinct cartoons.
    deer = VGroup(Ellipse(1.45, 0.75, color=BROWN, fill_color=BROWN, fill_opacity=0.38),
                  Circle(0.38, color=BROWN, fill_color=BROWN, fill_opacity=0.38).move_to([0.85, 0.48, 0]),
                  *[Line([x, -0.25, 0], [x, -0.78, 0], color=BROWN, stroke_width=5) for x in (-0.45, 0.35)])
    deer.move_to([0.2, 0.0, 0])
    head = Circle(0.34, color=TEXT).move_to([3.75, 1.45, 0])
    body = Line([3.75, 1.1, 0], [3.75, 0.0, 0], color=TEXT, stroke_width=8)
    limbs = VGroup(Line([3.75, 0.85, 0], [3.1, 0.35, 0], color=TEXT, stroke_width=5),
                   Line([3.75, 0.85, 0], [4.35, 0.35, 0], color=TEXT, stroke_width=5),
                   Line([3.75, 0.0, 0], [3.25, -0.75, 0], color=TEXT, stroke_width=5),
                   Line([3.75, 0.0, 0], [4.25, -0.75, 0], color=TEXT, stroke_width=5))
    person = VGroup(head, body, limbs)
    labels = VGroup(T("soybean", 28, GREEN).move_to([-2.7, 2.65, 0]),
                    T("deer", 28, BROWN).move_to([0.2, 1.0, 0]),
                    T("you", 28, TEXT).move_to([3.75, 2.15, 0]))
    return VGroup(soil, plant, deer, person, labels)


def root_world():
    """Root and nodules, shared without drift by predict and pause."""
    root = VMobject(color=GOLD, stroke_width=13).set_points_smoothly(
        [[-5.7, 2.15, 0], [-3.1, 1.75, 0], [-1.0, 0.75, 0], [0.5, -0.8, 0], [1.1, -2.25, 0]])
    branches = VGroup(Line([-2.1, 1.35, 0], [-3.35, -0.25, 0], color=GOLD, stroke_width=7),
                      Line([-0.35, 0.15, 0], [1.65, 0.55, 0], color=GOLD, stroke_width=7),
                      Line([0.35, -0.7, 0], [-1.35, -1.8, 0], color=GOLD, stroke_width=7))
    nodules = VGroup(*[Circle(0.42, color=PURPLE, fill_color=PURPLE, fill_opacity=0.28, stroke_width=4).move_to(p)
                       for p in [(-3.1, 0.0, 0), (1.5, 0.5, 0), (-1.2, -1.75, 0)]])
    glow = Circle(0.58, color=GOLD, stroke_width=3).move_to(nodules[1]).set_opacity(0.65)
    pulse(glow, base=2.5, amp=1.5, speed=2.2)
    return VGroup(root, branches, nodules, glow)


def nodule_world():
    """Close nodule used unchanged through fixation and mutualism."""
    root = RoundedRectangle(corner_radius=0.18, width=2.0, height=6.2,
                            color=GOLD, fill_color=GOLD, fill_opacity=0.16,
                            stroke_width=7).move_to([-2.7, 0, 0])
    nod = Circle(1.65, color=PURPLE, fill_color=SOIL, fill_opacity=0.55,
                 stroke_width=5).move_to([-0.8, -0.2, 0])
    rods = VGroup(*[bacterium(p, scale=0.78) for p in [(-1.35, 0.45, 0), (-0.55, 0.65, 0),
                                                        (-0.05, 0.05, 0), (-1.25, -0.35, 0),
                                                        (-0.45, -0.75, 0), (-1.3, -1.0, 0)]])
    return VGroup(root, nod, rods)


def dead_stem_world():
    ground = soil_band()
    stem = RoundedRectangle(corner_radius=0.16, width=8.8, height=0.72,
                            color=BROWN, fill_color=BROWN, fill_opacity=0.46,
                            stroke_width=4).rotate(-0.08).move_to([-0.6, -0.15, 0])
    return VGroup(ground, stem)


def gut_world():
    outer = RoundedRectangle(corner_radius=0.75, width=8.8, height=4.8,
                             color=GREY, stroke_width=8).move_to([0, 0.25, 0])
    inner = RoundedRectangle(corner_radius=0.55, width=7.7, height=3.65,
                             color=DARK_GREY, stroke_width=4).move_to([0, 0.25, 0])
    return VGroup(outer, inner)


def vine_world():
    """Grapevine and cut-away water tube, shared by pathogen/host scenes."""
    stem = Line([-3.0, -2.55, 0], [-3.0, 2.5, 0], color=GOLD, stroke_width=18)
    tube = RoundedRectangle(corner_radius=0.2, width=1.0, height=5.2,
                            color=PALE_BLUE, stroke_width=5).move_to([-3.0, 0, 0])
    leaves = VGroup(*[Ellipse(1.55, 0.75, color=GREEN, fill_color=GREEN, fill_opacity=0.5)
                       .rotate(a).move_to(p) for p, a in [((-4.15, 1.8, 0), 0.4), ((-1.85, 1.15, 0), -0.4),
                                                        ((-4.1, 0.2, 0), 0.3), ((-1.8, -1.0, 0), -0.3)]])
    return VGroup(stem, tube, leaves)


def ecoli_panels():
    tp = TwoPanel("most strains: quiet", "harmful strain", colors=(TEAL, RED), top=3.0, bottom=-2.45)
    gut = RoundedRectangle(corner_radius=0.5, width=4.2, height=2.5, color=GREY, stroke_width=6)
    rods_l = VGroup(*[bacterium(p, scale=0.8) for p in [(-0.8, 0.4, 0), (0, 0.15, 0), (0.7, -0.35, 0)]])
    left = VGroup(gut, rods_l, T("E. coli", 28, PURPLE).move_to([0, -1.05, 0]))
    tp.put(left, "left")
    glass = VGroup(Line([-1.2, 1.0, 0], [-0.85, -1.15, 0], color=PALE_BLUE, stroke_width=5),
                   Line([1.2, 1.0, 0], [0.85, -1.15, 0], color=PALE_BLUE, stroke_width=5),
                   Line([-0.85, -1.15, 0], [0.85, -1.15, 0], color=PALE_BLUE, stroke_width=5))
    rod = bacterium([0, 0.1, 0], scale=1.05)
    extra = Square(0.32, color=RED, fill_color=RED, fill_opacity=0.7).next_to(rod, RIGHT, buff=0.02)
    right = VGroup(glass, rod, extra, T("extra genes", 28, RED).move_to([0, -1.45, 0]))
    tp.put(right, "right")
    return tp, left, right


class S00Title(TitleCard):
    LESSON = "Microbes in Ecosystems"
    TITLE = "Who Unlocks the Matter?"


class S01Question(ActiveSpokenScene):
    def construct(self):
        world = soybean_world()
        self.play(FadeIn(world), run_time=0.8)
        gases = VGroup(*[paired_nitrogen(p) for p in [(-5.4, 2.7, 0), (-4.3, 1.9, 0), (-1.1, 2.65, 0),
                                                              (1.6, 2.4, 0), (5.0, 2.7, 0)]])
        for i, g in enumerate(gases):
            bob(g, amp=0.08, speed=1.2, seed=i)
        self.at("Every protein")
        self.play(LaggedStart(*[FadeIn(g) for g in gases], lag_ratio=0.12), run_time=1.0)
        needs = T("proteins + DNA need nitrogen", 30, PALE_BLUE).move_to([1.2, 3.25, 0])
        self.at("needs nitrogen")
        self.play(FadeIn(needs), run_time=0.5)
        air = T("nitrogen gas", 30, PALE_BLUE).move_to([-4.65, 3.25, 0])
        self.at("mostly nitrogen gas")
        self.play(FadeIn(air), gases.animate.shift(RIGHT * 0.22), run_time=0.8)
        inhaled = VGroup(*[paired_nitrogen(p, 0.8) for p in [(-2.7, 2.15, 0), (0.6, 0.55, 0), (3.6, 1.35, 0)]])
        self.at("why can't")
        self.play(TransformFromCopy(gases[:3], inhaled), run_time=0.7)
        self.play(inhaled.animate.shift(RIGHT * 0.75), run_time=0.7)
        q = T("?", 84, GOLD, weight=BOLD).move_to([5.7, 2.6, 0])
        self.at("single breath")
        self.play(GrowFromCenter(q), run_time=0.6)
        self.finish()


class S02Locked(ActiveSpokenScene):
    def construct(self):
        gas = VGroup(*[paired_nitrogen(p, 1.15) for p in [(-4.8, 1.1, 0), (-4.0, 1.65, 0), (-3.5, 0.7, 0)]])
        gas_lab = T("nitrogen gas", 30, PALE_BLUE).move_to([-4.15, 2.5, 0])
        self.add(gas, gas_lab)
        self.at("Nitrogen gas is locked")
        lock1 = padlock([-4.15, -0.45, 0], 1.05)
        self.play(GrowFromCenter(lock1), run_time=0.6)
        no_build = T("plants and animals\ncannot build with it", 28, TEXT).move_to([-4.15, -1.65, 0])
        self.at("cannot build")
        self.play(FadeIn(no_build), run_time=0.5)
        leaf = Ellipse(2.0, 0.8, color=BROWN, fill_color=BROWN, fill_opacity=0.55).rotate(0.35).move_to([0, 1.0, 0])
        self.at("Two other stores")
        self.play(FadeIn(leaf, shift=DOWN * 0.2), run_time=0.6)
        leaf_lab = T("dead leaf", 30, BROWN).move_to([0, 2.0, 0])
        lock2 = padlock([0, -0.35, 0], 1.0)
        self.at("dead leaf")
        self.play(FadeIn(leaf_lab), GrowFromCenter(lock2), run_time=0.6)
        gut = RoundedRectangle(corner_radius=0.55, width=3.1, height=2.6, color=GREY, stroke_width=6).move_to([4.3, 0.65, 0])
        fiber = VMobject(color=GOLD, stroke_width=7).set_points_smoothly([[3.4, 0.2, 0], [4.0, 1.3, 0], [4.7, 0.1, 0], [5.2, 1.2, 0]])
        self.at("The other is fiber")
        self.play(Create(gut), Create(fiber), run_time=0.8)
        fiber_lab = T("fiber", 30, GOLD).move_to([4.3, 2.35, 0])
        lock3 = padlock([4.3, -1.15, 0], 1.0)
        self.play(FadeIn(fiber_lab), GrowFromCenter(lock3), run_time=0.6)
        tr = tracker()
        self.at("cannot digest")
        self.play(FadeIn(tr), run_time=0.8)
        self.finish()


class S03Predict(ActiveSpokenScene):
    def construct(self):
        roots = root_world()
        self.play(FadeIn(roots), run_time=0.7)
        self.at("who could possibly")
        q = question_card("Who can use nitrogen gas?", ["plants", "animals", "some microbes"],
                          chips_at=[3.75, 0.5, 0], y=-3.12)
        self.play(FadeIn(q.question), run_time=0.5)
        self.at("Make your guess")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in q.chips], lag_ratio=0.18), run_time=0.9)
        for c in q.chips:
            pulse(c[0], base=2.5, amp=1.2, speed=2.0)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Who can use nitrogen gas?"
    OPTIONS = ["plants", "animals", "some microbes"]
    CHIPS_AT = [3.75, 0.5, 0]
    CARD = {"y": -3.12}

    def backdrop(self):
        return root_world()


class S05Reveal(ActiveSpokenScene):
    def construct(self):
        world = nodule_world()
        self.add(world)
        answer = chip("some microbes", PURPLE, 30).move_to([4.35, 2.75, 0])
        self.at("Some bacteria can")
        self.play(FadeIn(answer), Indicate(world[2], color=PURPLE), run_time=0.8)
        nodlab = T("root nodule", 30, PURPLE).move_to([0.35, 2.55, 0])
        self.at("small bumps")
        self.play(FadeIn(nodlab), run_time=0.5)
        gas = VGroup(*[paired_nitrogen(p) for p in [(3.7, 1.4, 0), (4.5, 0.9, 0), (3.8, 0.25, 0)]])
        ain = arrow([3.25, 0.7, 0], [1.05, 0.15, 0], PALE_BLUE)
        self.at("turn nitrogen gas")
        self.play(FadeIn(gas), GrowArrow(ain), run_time=0.7)
        self.play(gas.animate.shift(LEFT * 2.25), run_time=0.8)
        ammonium = VGroup(*[Dot(p, radius=0.13, color=GREEN) for p in [(0.2, 0.65, 0), (0.55, -0.15, 0), (0.0, -0.7, 0)]])
        ammonium_lab = T("ammonium", 30, GREEN).move_to([2.2, -1.1, 0])
        self.at("into ammonium")
        self.play(ReplacementTransform(gas, ammonium), FadeIn(ammonium_lab), run_time=0.8)
        fixed = VGroup(*[Dot(radius=0.13, color=TEAL).move_to(p) for p in [(-2.7, -1.5, 0), (-2.7, -0.4, 0), (-2.7, 0.7, 0)]])
        up = arrow([-2.7, -2.2, 0], [-2.7, 2.6, 0], TEAL)
        fixed_lab = T("fixed nitrogen", 30, TEAL).move_to([-4.6, 1.65, 0])
        self.at("plant can use")
        self.play(TransformFromCopy(ammonium, fixed), GrowArrow(up), FadeIn(fixed_lab), run_time=0.8)
        self.play(fixed.animate.shift(UP * 1.0), run_time=0.7)
        fixlab = T("nitrogen fixation", 38, TEXT, weight=BOLD).move_to([2.6, -2.2, 0])
        self.at("called nitrogen fixation")
        self.play(FadeIn(fixlab), run_time=0.6)
        self.finish()


class S06Trade(ActiveSpokenScene):
    def construct(self):
        world = nodule_world()
        self.add(world)
        up = arrow([-2.7, -2.25, 0], [-2.7, 2.6, 0], TEAL)
        up_lab = T("fixed nitrogen", 28, TEAL).move_to([-5.05, 0.75, 0])
        self.add(up, up_lab)
        sun = Circle(0.45, color=GOLD, fill_color=GOLD, fill_opacity=0.45).move_to([-5.5, 2.6, 0])
        rays = VGroup(*[Line(sun.get_center(), sun.get_center() + 0.8 * d, color=GOLD, stroke_width=3)
                        for d in (UP, DOWN, LEFT, RIGHT, UR, UL, DR, DL)])
        self.at("plant pays them back")
        self.play(FadeIn(sun), Create(rays), run_time=0.7)
        down = arrow([-1.9, 2.65, 0], [-1.9, -2.3, 0], GOLD)
        sugars = VGroup(*[Dot(radius=0.13, color=GOLD).move_to([-1.9, y, 0]) for y in (1.7, 0.7, -0.3)])
        sugar_lab = T("plant sugar", 30, GOLD).move_to([0.2, 2.55, 0])
        self.at("Sugar made in the leaves")
        self.play(GrowArrow(down), FadeIn(sugars), FadeIn(sugar_lab), run_time=0.8)
        self.play(sugars.animate.shift(DOWN * 1.0), run_time=0.8)
        self.at("Each partner gets")
        badge = VGroup(arrow([0.8, 0.6, 0], [4.7, 0.6, 0], TEAL),
                       arrow([4.7, -0.5, 0], [0.8, -0.5, 0], GOLD))
        self.play(LaggedStart(*[GrowArrow(a) for a in badge], lag_ratio=0.3), run_time=0.9)
        mutual = chip("mutualism: both benefit", GOLD, 30).move_to([3.0, -1.75, 0])
        self.at("called mutualism")
        self.play(FadeIn(mutual, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07Decomposers(ActiveSpokenScene):
    def construct(self):
        world = dead_stem_world()
        upright = Line([-0.6, -0.8, 0], [-0.6, 2.8, 0], color=GREEN, stroke_width=12)
        self.add(soil_band(), upright)
        self.at("soybean dies")
        self.play(upright.animate.rotate(-PI / 2, about_point=[-0.6, -0.8, 0]).set_color(BROWN), run_time=1.0)
        self.remove(upright)
        self.add(world[1])
        rods = VGroup(*[bacterium(p) for p in [(-3.0, 0.55, 0), (-1.5, 0.25, 0), (0.4, 0.55, 0)]])
        fungi = VGroup(*[VMobject(color=TEXT, stroke_width=4).set_points_smoothly(pts) for pts in [
            [[1.2, -0.2, 0], [1.7, 0.7, 0], [2.3, 1.25, 0]],
            [[1.7, 0.7, 0], [2.5, 0.45, 0], [3.2, 0.8, 0]],
            [[2.3, 1.25, 0], [2.8, 1.85, 0], [3.5, 1.55, 0]]]])
        self.at("Bacteria and fungi grow")
        self.play(LaggedStart(*[FadeIn(r) for r in rods], lag_ratio=0.15),
                  LaggedStart(*[Create(f) for f in fungi], lag_ratio=0.18), run_time=1.1)
        enzyme = chip("enzymes", ORANGE_M, 28).move_to([-3.9, 2.4, 0])
        scissors = VGroup(*[T("✂", 34, ORANGE_M).move_to(p) for p in [(-2.4, 1.25, 0), (-0.7, 1.0, 0), (1.0, 1.2, 0)]])
        self.at("release enzymes")
        self.play(FadeIn(enzyme), LaggedStart(*[FadeIn(s) for s in scissors], lag_ratio=0.15), run_time=0.8)
        big = VGroup(*[Square(0.62, color=BROWN, fill_color=BROWN, fill_opacity=0.65).move_to([x, -0.05, 0]) for x in (-1.1, -0.45, 0.2)])
        small = VGroup(*[Square(0.27, color=ORANGE_M, fill_color=ORANGE_M, fill_opacity=0.7).move_to(p)
                         for p in [(-1.0, -0.05, 0), (-0.55, -0.15, 0), (-0.15, 0.05, 0), (0.3, -0.1, 0)]])
        self.at("large molecules")
        self.play(FadeIn(big), run_time=0.5)
        self.at("into smaller ones")
        self.play(ReplacementTransform(big, small), run_time=0.8)
        self.at("Nutrients return")
        self.play(small.animate.shift(DOWN * 1.55), run_time=0.8)
        lab = T("decomposers", 38, PURPLE, weight=BOLD).move_to([3.9, 2.6, 0])
        self.at("microbes are decomposers")
        self.play(FadeIn(lab), run_time=0.5)
        self.finish()


class S08Gut(ActiveSpokenScene):
    def construct(self):
        gut = gut_world()
        self.play(Create(gut), run_time=0.8)
        gutlab = T("large intestine", 30, GREY).move_to([0, 3.05, 0])
        self.at("inside you")
        self.play(FadeIn(gutlab), run_time=0.4)
        rods = VGroup(*[bacterium(p) for p in [(-2.8, 0.9, 0), (-1.7, -0.6, 0), (0.2, 1.0, 0), (1.6, -0.5, 0)]])
        fiber = VMobject(color=GOLD, stroke_width=8).set_points_smoothly([[-2.4, 0, 0], [-1.1, 1.1, 0], [0, -0.2, 0], [1.2, 0.85, 0], [2.5, -0.1, 0]])
        self.at("Bacteria in your large intestine")
        self.play(LaggedStart(*[FadeIn(r) for r in rods], lag_ratio=0.14), Create(fiber), run_time=1.0)
        self.at("by fermentation")
        self.play(LaggedStart(*[Indicate(r, color=PURPLE) for r in rods], lag_ratio=0.15), run_time=0.8)
        # Cross out a small O2 tag only; a cross through "no oxygen needed" read as its opposite.
        o2 = chip("O₂", GREY, 28)
        no_o = VGroup(o2, T("no oxygen needed", 28, GREY)).arrange(RIGHT, buff=0.3).move_to([3.7, -2.9, 0])
        cross = Cross(o2, stroke_color=RED, stroke_width=5)
        # Deliberate strike-through: the visual note explicitly calls for a crossed-out oxygen tag.
        for part in cross.family_members_with_points():
            part.layout_ok = True
        self.at("without oxygen")
        self.play(FadeIn(no_o), Create(cross), run_time=0.6)
        acids = VGroup(*[Square(0.28, color=TEAL, fill_color=TEAL, fill_opacity=0.8).move_to(p)
                         for p in [(-0.7, 0.2, 0), (0, 0.25, 0), (0.7, 0.15, 0)]])
        acids_lab = T("small acids", 30, TEAL).move_to([0, -1.1, 0])
        self.at("make small acids")
        self.play(ReplacementTransform(fiber, acids), FadeIn(acids_lab), run_time=0.8)
        wall_arrow = arrow([0.8, 0.1, 0], [3.7, 0.1, 0], TEAL)
        self.at("absorb for energy")
        self.play(GrowArrow(wall_arrow), acids.animate.shift(RIGHT * 2.6), run_time=0.8)
        self.finish()


class S09Handon(ActiveSpokenScene):
    def construct(self):
        tp = TwoPanel("nodule", "dead stem", colors=(TEAL, ORANGE_M), top=3.0, bottom=-0.2)
        # A third wide panel below keeps the three cases readable without shrinking them.
        lower = RoundedRectangle(corner_radius=0.18, width=12.8, height=2.1, color=GOLD, stroke_width=2.5).move_to([0, -1.55, 0])
        lower_head = T("gut fiber", 30, GOLD).move_to([-5.35, -0.75, 0])
        self.play(FadeIn(tp), FadeIn(lower), FadeIn(lower_head), run_time=0.7)
        locks = VGroup(padlock([-3.2, 1.15, 0], 1.0, True), padlock([3.2, 1.15, 0], 1.0, True), padlock([-3.2, -1.55, 0], 1.0, True))
        self.at("Three locked stores")
        self.play(LaggedStart(*[FadeIn(l) for l in locks], lag_ratio=0.18), run_time=0.9)
        microbes = VGroup(bacterium([-1.8, 1.15, 0]), bacterium([4.55, 1.15, 0]), bacterium([-1.8, -1.55, 0]))
        self.at("three microbes")
        self.play(LaggedStart(*[FadeIn(m) for m in microbes], lag_ratio=0.16), run_time=0.8)
        outs = VGroup(arrow([-1.2, 1.15, 0], [0.5, 1.15, 0], TEAL),
                      arrow([5.0, 1.15, 0], [6.1, 1.15, 0], ORANGE_M),
                      arrow([-1.2, -1.55, 0], [1.2, -1.55, 0], TEAL))
        self.at("handed on")
        self.play(LaggedStart(*[GrowArrow(a) for a in outs], lag_ratio=0.2), run_time=1.0)
        cap = caption("unlock, then hand it on", size=34, color=TEXT, y=-3.25)
        self.at("life depends on microbes")
        self.play(FadeIn(cap), run_time=0.6)
        self.finish()


class S10Pathogen(ActiveSpokenScene):
    def construct(self):
        vine = vine_world()
        self.play(FadeIn(vine), run_time=0.8)
        title = T("grapevine", 30, GREEN).move_to([-3.0, 3.15, 0])
        self.at("look at a grapevine")
        self.play(FadeIn(title), run_time=0.4)
        rods = VGroup(*[bacterium(p, scale=0.8) for p in [(-3.0, 1.2, 0), (-3.0, 0.55, 0), (-3.0, -0.1, 0), (-3.0, -0.75, 0)]])
        xlab = T("Xylella", 30, PURPLE).move_to([0.0, 1.5, 0])
        self.at("bacterium called Xylella")
        self.play(LaggedStart(*[FadeIn(r) for r in rods], lag_ratio=0.13), FadeIn(xlab), run_time=1.0)
        block = Rectangle(width=0.82, height=0.55, color=PURPLE, fill_color=PURPLE, fill_opacity=0.75).move_to([-3.0, -0.25, 0])
        self.at("blocks them")
        self.play(GrowFromCenter(block), vine[2].animate.set_color(BROWN), run_time=0.8)
        one = arrow([-1.9, -1.85, 0], [3.8, -1.85, 0], DARK_GREY, width=7)
        vine_lab = T("vine", 28, GREEN).move_to([-1.35, -2.35, 0])
        bact_lab = T("bacterium", 28, PURPLE).move_to([3.3, -2.35, 0])
        self.at("arrow runs one way")
        self.play(GrowArrow(one), FadeIn(vine_lab), FadeIn(bact_lab), run_time=0.8)
        path = chip("pathogen", RED, 34).move_to([3.6, 0.3, 0])
        self.at("is a pathogen")
        self.play(FadeIn(path), run_time=0.6)
        self.finish()


class S11Host(ActiveSpokenScene):
    def construct(self):
        vine = vine_world()
        vine[2].set_color(BROWN)
        rods = VGroup(*[bacterium(p, scale=0.8) for p in [(-3.0, 1.2, 0), (-3.0, 0.55, 0), (-3.0, -0.1, 0), (-3.0, -0.75, 0)]])
        self.add(vine, rods)
        outline = SurroundingRectangle(vine, color=GREEN, buff=0.22, stroke_width=4)
        self.at("The host")
        self.play(Create(outline), run_time=0.7)
        host = chip("host", GREEN, 34).move_to([1.2, 2.55, 0])
        self.play(FadeIn(host), run_time=0.4)
        harm = arrow([-1.85, 0.15, 0], [4.1, 0.15, 0], DARK_GREY, width=7)
        harm_lab = T("host → pathogen", 30, DARK_GREY).move_to([1.1, 0.75, 0])
        self.at("grows inside its host")
        self.play(GrowArrow(harm), FadeIn(harm_lab), run_time=0.8)
        self.at("harms it")
        self.play(Indicate(vine[2], color=RED), run_time=0.7)
        returned = arrow([4.1, -1.25, 0], [-1.85, -1.25, 0], GREY, width=4)
        self.at("gets nothing useful back")
        self.play(Create(returned), run_time=0.5)
        self.play(Create(Cross(returned, stroke_color=RED, stroke_width=6)), run_time=0.5)
        self.finish()


class S12Ecoli(ActiveSpokenScene):
    def construct(self):
        tp, left, right = ecoli_panels()
        self.play(FadeIn(tp), run_time=0.7)
        prompt = T("helper or harm?", 34, TEXT, weight=BOLD).move_to([0, 3.45, 0])
        self.at("helper or a harm")
        self.play(FadeIn(prompt), run_time=0.5)
        self.at("Take E coli")
        self.play(FadeIn(left), run_time=0.7)
        quiet = T("large intestine", 28, GREY).move_to([-3.25, -1.9, 0])
        self.at("live quietly")
        self.play(FadeIn(quiet), run_time=0.5)
        self.at("Other strains")
        self.play(FadeIn(right), run_time=0.7)
        self.at("extra genes")
        self.play(Indicate(right[2], color=RED), run_time=0.7)
        stomach = Circle(0.58, color=RED).move_to([4.9, -1.5, 0])
        sick = T("sick", 28, RED).move_to([4.9, -2.25, 0])
        into = arrow([3.0, -0.2, 0], [4.45, -1.15, 0], RED)
        self.at("food or water")
        self.play(GrowArrow(into), FadeIn(stomach), run_time=0.7)
        self.at("get sick")
        self.play(FadeIn(sick), run_time=0.4)
        rule = caption("which strain, and where it lives", size=32, color=GOLD)
        self.play(FadeIn(rule), run_time=0.5)
        self.finish()


class S13Rule(ActiveSpokenScene):
    def construct(self):
        left = RoundedRectangle(corner_radius=0.22, width=5.7, height=5.5, color=TEAL, stroke_width=3).move_to([-3.6, 0.25, 0])
        right = RoundedRectangle(corner_radius=0.22, width=5.7, height=5.5, color=RED, stroke_width=3).move_to([3.6, 0.25, 0])
        self.play(FadeIn(left), FadeIn(right), run_time=0.6)
        locks = VGroup(*[padlock([-4.8 + 1.2 * i, 1.35, 0], 0.78, True) for i in range(3)])
        self.at("Some microbes unlock")
        self.play(LaggedStart(*[FadeIn(l) for l in locks], lag_ratio=0.15), run_time=0.8)
        hand = arrow([-5.0, -0.1, 0], [-2.25, -0.1, 0], TEAL)
        self.at("hand it on")
        self.play(GrowArrow(hand), run_time=0.6)
        life = fit_text("unlock + hand on\nlife depends on them", max_w=4.8, size=32, color=TEAL).move_to([-3.6, -1.25, 0])
        self.at("Life depends on them")
        self.play(FadeIn(life), run_time=0.5)
        vine = vine_world().scale(0.52).move_to([3.0, 0.65, 0])
        self.at("Pathogens cause disease")
        self.play(FadeIn(vine), run_time=0.7)
        harm = arrow([2.1, -1.0, 0], [5.2, -1.0, 0], DARK_GREY)
        path = T("pathogen: harms its host", 30, RED).move_to([3.6, -1.7, 0])
        self.play(GrowArrow(harm), FadeIn(path), run_time=0.7)
        decide = caption("strain and place can decide", size=34, color=GOLD)
        self.at("depend on its strain")
        self.play(FadeIn(decide), run_time=0.6)
        self.finish()


class S14End(EndCard):
    LINE = "Microbes that unlock matter feed life; pathogens cause disease in their hosts."
