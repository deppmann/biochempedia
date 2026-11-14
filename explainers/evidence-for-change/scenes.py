"""What the Rocks Still Show — a single carried riverbank world.

COLOUR MAP
    GOLD  fossils and fossil-bearing observations
    BLUE  matching body structures (reserved for the following film)
    TEAL  DNA/protein sequences (reserved for the following film)
    GREEN supported comparisons and inferences
    GREY  missing or uncertain evidence

All fossil silhouettes are schematic teaching icons, not reconstructions.  The timeline dates are
the four values in the lesson table; no curve or quantitative relationship is sketched.
"""
from bp_parts import *


ROCK = "#6F5A49"
ROCK_LIGHT = "#92765C"
WATER = "#367A96"
SAND = "#B99A68"


def shell(hinge=ORIGIN, radius=1.0, color=GOLD, changed=0.0, fill=0.28):
    """Large, readable scallop icon; ``changed`` alters its outline without implying ancestry."""
    hinge = np.array(hinge, dtype=float)
    left = 31 + changed * 5
    right = 149 - changed * 3
    fan = Sector(radius=radius, start_angle=left * DEGREES,
                 angle=(right - left) * DEGREES, arc_center=hinge,
                 stroke_color=color, stroke_width=5, fill_color=color,
                 fill_opacity=fill)
    ridges = VGroup(*[
        Line(hinge + radius * 0.18 * np.array([np.cos(a), np.sin(a), 0]),
             hinge + radius * (0.90 - 0.03 * changed) * np.array([np.cos(a), np.sin(a), 0]),
             color=color, stroke_width=2.8)
        for a in np.linspace((left + 9) * DEGREES, (right - 9) * DEGREES, 7)
    ])
    ears = Line(hinge + LEFT * radius * 0.38, hinge + RIGHT * radius * 0.38,
                color=color, stroke_width=5)
    return VGroup(fan, ridges, ears)


def bone_icon(color=GOLD):
    shaft = RoundedRectangle(corner_radius=0.14, width=1.25, height=0.36,
                             stroke_color=color, stroke_width=4,
                             fill_color=color, fill_opacity=0.25)
    ends = VGroup(Dot(LEFT * 0.62, radius=0.25, color=color),
                  Dot(RIGHT * 0.62, radius=0.25, color=color)).set_opacity(0.85)
    return VGroup(shaft, ends).rotate(0.18)


def tooth_icon(color=GOLD):
    return Polygon([-0.48, 0.42, 0], [0.48, 0.42, 0], [0.22, -0.55, 0],
                   [0, -0.22, 0], [-0.22, -0.55, 0], color=color,
                   stroke_width=4, fill_color=color, fill_opacity=0.25)


def footprint_icon(color=GOLD):
    sole = Ellipse(width=0.55, height=1.05, color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.22).rotate(-0.25)
    toes = VGroup(*[Dot([x, 0.66 + 0.08 * abs(x), 0], radius=0.11, color=color)
                    for x in (-0.28, -0.09, 0.10, 0.29)])
    return VGroup(sole, toes)


def trilobite(color=GOLD):
    body = Ellipse(width=1.15, height=1.7, stroke_color=color, stroke_width=4,
                   fill_color=color, fill_opacity=0.23)
    head = Arc(radius=0.42, start_angle=0, angle=PI, color=color, stroke_width=4).shift(UP * 0.42)
    ribs = VGroup(*[Line([-0.43, y, 0], [0.43, y, 0], color=color, stroke_width=2.5)
                    for y in np.linspace(-0.48, 0.32, 5)])
    spine = Line([0, -0.68, 0], [0, 0.68, 0], color=color, stroke_width=2.5)
    return VGroup(body, head, ribs, spine)


def moving_water(y=2.75, width=12.2):
    """A broad river with a slow current; the updater persists while narration lands."""
    river = Rectangle(width=width, height=0.9, stroke_color=WATER, stroke_width=3,
                      fill_color=WATER, fill_opacity=0.50).move_to([0, y, 0])
    waves = VGroup(*[
        Line([-5.8 + i * 1.55, y + 0.08 * (-1) ** i, 0],
             [-4.85 + i * 1.55, y + 0.08 * (-1) ** i, 0],
            color=TEXT, stroke_width=3.5).set_opacity(0.72)
        for i in range(8)
    ])
    waves._phase = 0.0

    def drift(mob, dt):
        mob._phase += dt
        mob.shift(RIGHT * 1.20 * dt)
        if mob.get_left()[0] > -5.25:
            mob.shift(LEFT * 1.55)

    waves.add_updater(drift)
    return VGroup(river, waves)


def grains(n=12, box=(-5.7, 5.7, -2.6, 2.1), color=SAND, speed=0.12):
    rng = np.random.default_rng(17 + n)
    dots = VGroup(*[
        Dot([rng.uniform(box[0], box[1]), rng.uniform(box[2], box[3]), 0],
            radius=rng.uniform(0.045, 0.075), color=color).set_opacity(0.68)
        for _ in range(n)
    ])
    dots._t = 0.0

    def fall(mob, dt):
        mob._t += dt
        mob.shift(DOWN * speed * dt + RIGHT * 0.025 * np.sin(mob._t) * dt)
        for d in mob:
            if d.get_y() < box[2]:
                d.shift(UP * (box[3] - box[2]))

    dots.add_updater(fall)
    return dots


def shimmer_band(y=0.0, width=9.2, color=GREY):
    """A persistent scan across an explicitly uncertain interval."""
    mark = Rectangle(width=0.85, height=0.88, stroke_width=0,
                     fill_color=color, fill_opacity=0.20).move_to([-width / 2, y, 0])
    mark._left = -width / 2
    mark._right = width / 2
    mark._scan_t = 0.0

    def scan(mob, dt):
        mob._scan_t += dt
        mob.shift(RIGHT * 0.90 * dt)
        mob.set_fill(color, opacity=0.12 + 0.43 * (0.5 + 0.5 * np.sin(6.0 * mob._scan_t)))
        if mob.get_left()[0] > mob._right:
            mob.shift(LEFT * (width + mob.width))

    mark.add_updater(scan)
    return mark


def breathe_fill(mob, color, lo=0.12, hi=0.34, speed=1.7):
    """Keep a named block active while its explanatory sentence lands."""
    mob._breathe_t = 0.0

    def breathe(m, dt):
        m._breathe_t += dt
        opacity = lo + (hi - lo) * (0.5 + 0.5 * np.sin(speed * m._breathe_t))
        m.set_fill(color, opacity=opacity)

    return mob.add_updater(breathe)


def riverbank(with_fossils=True, with_gaps=True, label=True):
    """The carried world, rebuilt at exactly the same scale and coordinates."""
    layer_specs = [
        (-2.55, 0.70, ROCK), (-1.75, 0.64, ROCK_LIGHT), (-1.00, 0.62, ROCK),
        (-0.27, 0.62, ROCK_LIGHT), (0.47, 0.62, ROCK), (1.18, 0.58, ROCK_LIGHT),
    ]
    layers = VGroup(*[
        Rectangle(width=11.9 - 0.15 * i, height=h, stroke_color=SAND,
                  stroke_width=2, fill_color=c, fill_opacity=0.66).move_to([0, y, 0])
        for i, (y, h, c) in enumerate(layer_specs)
    ])
    water = moving_water()
    bank = VGroup(layers, water)
    bank.layers = layers
    bank.water = water
    bank.shells = VGroup()
    if with_fossils:
        fossils = VGroup(shell([-3.7, -2.82, 0], 0.62),
                         shell([1.3, -1.25, 0], 0.56, changed=0.35),
                         shell([-0.5, 0.20, 0], 0.50, changed=0.65))
        bank.add(fossils)
        bank.shells = fossils
    bank.gaps = VGroup()
    if with_gaps:
        gs = VGroup(
            Rectangle(width=11.75, height=0.18, stroke_width=0, fill_color=BG,
                      fill_opacity=1).move_to([0, -1.38, 0]),
            Rectangle(width=11.55, height=0.16, stroke_width=0, fill_color=BG,
                      fill_opacity=1).move_to([0, 0.12, 0]),
        )
        bank.add(gs)
        bank.gaps = gs
    if label:
        tag = T("Virginia riverbank, schematic", 28, TEXT).move_to([-3.75, 1.86, 0])
        bank.add(tag)
        bank.tag = tag
    erosion = DashedLine([5.82, -2.86, 0], [5.82, 1.55, 0], color=SAND,
                         stroke_width=5, dash_length=0.16).set_opacity(0.70)
    pulse(erosion, base=5.0, amp=1.8, speed=1.7)
    erosion._sway_t = 0.0
    erosion._sway_x = erosion.get_x()

    def erode(mob, dt):
        mob._sway_t += dt
        mob.set_x(mob._sway_x + 0.18 * np.sin(5.0 * mob._sway_t))

    erosion.add_updater(erode)
    bank.add(erosion, grains(16, box=(-5.7, 5.7, -2.6, 1.48), speed=0.19))
    return bank


def title_over_bank():
    bank = riverbank()
    veil = Rectangle(width=13.2, height=2.0, stroke_width=0, fill_color=BG,
                     fill_opacity=0.80).move_to([0, 0.25, 0])
    lesson = T("EVIDENCE FOR CHANGE", 24, TEAL, weight=BOLD).move_to([0, 0.72, 0])
    title = T("What the Rocks Still Show", 50, TEXT, font=TITLE_FONT).move_to([0, 0.05, 0])
    rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).move_to([0, -0.48, 0])
    return bank, VGroup(veil, lesson, title, rule)


def observed_pair(include_question=False):
    """Shared exact frame for prediction, pause, and reveal."""
    lower = RoundedRectangle(corner_radius=0.12, width=9.7, height=1.35,
                             stroke_color=SAND, stroke_width=3,
                             fill_color=ROCK, fill_opacity=0.72).move_to([0, -1.38, 0])
    upper = RoundedRectangle(corner_radius=0.12, width=9.7, height=1.35,
                             stroke_color=SAND, stroke_width=3,
                             fill_color=ROCK_LIGHT, fill_opacity=0.72).move_to([0, 1.38, 0])
    low_shell = shell([-2.2, -1.58, 0], 0.95)
    high_shell = shell([2.2, 1.15, 0], 0.95, changed=0.75)
    missing = Rectangle(width=9.7, height=1.10, stroke_color=GREY, stroke_width=3,
                        fill_color=GREY, fill_opacity=0.10).move_to([0, 0, 0])
    missing_label = T("missing layer", 30, GREY).move_to(missing)
    missing_label.layout_ok = True  # deliberate label inside its own uncertainty band
    pair = VGroup(lower, upper, missing, low_shell, high_shell, missing_label)
    pair.lower, pair.upper = lower, upper
    pair.low_shell, pair.high_shell = low_shell, high_shell
    pair.missing, pair.missing_label = missing, missing_label
    pair.add(grains(7, box=(-4.7, 4.7, -1.95, 1.95), speed=0.035))
    pair.add(shimmer_band())
    if include_question:
        pair.add(question_card("Does a gap erase the observed pattern?", y=-3.15, max_w=10.6))
    return pair


def branch_tree(color=GREY, at=(3.8, -0.2, 0), scale=1.0):
    x, y, _ = at
    lines = VGroup(Line([x, y - 1.3, 0], [x, y + 0.35, 0]),
                   Line([x, y - 0.35, 0], [x - 0.9, y + 0.7, 0]),
                   Line([x, y - 0.05, 0], [x + 0.9, y + 1.0, 0]),
                   Line([x - 0.9, y + 0.7, 0], [x - 1.35, y + 1.25, 0]),
                   Line([x - 0.9, y + 0.7, 0], [x - 0.45, y + 1.25, 0]))
    lines.set_stroke(color, width=5)
    return lines.scale(scale, about_point=np.array(at))


class S00Hook(TitleCard, SpokenScene):
    def construct(self):
        bank = riverbank(with_fossils=False, with_gaps=False)
        # Begin with the world already moving, then let the gaps interrupt it.
        self.play(FadeIn(bank.layers), FadeIn(bank.water), run_time=0.7)
        self.at("record full of gaps")
        self.play(FadeIn(bank.tag), run_time=0.35)
        gaps = VGroup(
            Rectangle(width=11.75, height=0.18, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, -1.38, 0]),
            Rectangle(width=11.55, height=0.16, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, 0.12, 0]))
        self.play(FadeIn(gaps), run_time=0.6)
        self.at("A fossil scallop")
        fossil = shell([-3.7, -2.82, 0], 0.62)
        self.play(GrowFromPoint(fossil, [-3.7, -2.82, 0]), run_time=0.8)
        self.at("Above it")
        self.play(Indicate(bank.water, color=TEXT, scale_factor=1.01), run_time=0.6)
        sea = T("once a shallow sea", 30, WATER).move_to([2.9, 1.84, 0])
        self.at("once beneath")
        self.play(FadeIn(sea, shift=DOWN * 0.12), run_time=0.5)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        bank, title = title_over_bank()
        self.add(bank)
        self.play(FadeIn(title[0]), FadeIn(title[1]), Write(title[2]), GrowFromCenter(title[3]), run_time=1.1)
        self.finish()


class S02FossilForms(SpokenScene):
    def construct(self):
        sea = Rectangle(width=13, height=2.0, stroke_color=WATER, stroke_width=3,
                        fill_color=WATER, fill_opacity=0.40).move_to([0, 2.25, 0])
        floor = Rectangle(width=13, height=3.9, stroke_color=SAND, stroke_width=3,
                          fill_color=ROCK, fill_opacity=0.48).move_to([0, -0.72, 0])
        self.add(sea, floor, grains(15, speed=0.10), scope_tag("schematic"))
        main_shell = shell([-4.5, -0.2, 0], 1.15)
        self.play(GrowFromPoint(main_shell, [-4.5, -0.2, 0]), run_time=0.7)
        self.at("preserved remains")
        definition = caption("Fossil: preserved remains or traces of past life", color=GOLD)
        self.play(FadeIn(definition, shift=UP * 0.1), run_time=0.45)
        icons = [bone_icon(), tooth_icon(), footprint_icon()]
        for obj, pos, cue in zip(icons, ([-1.6, -0.05, 0], [1.3, -0.05, 0], [4.3, -0.05, 0]),
                                 ("bones", "teeth", "footprints")):
            obj.move_to(pos)
            self.at(cue)
            self.play(FadeIn(obj, shift=UP * 0.18), run_time=0.4)
        soft = VGroup(*[Circle(radius=0.22 + i * 0.04, color=GREY, fill_color=GREY,
                              fill_opacity=0.24).move_to([-2.2 + i * 1.0, 1.45, 0]) for i in range(5)])
        self.at("Most remains")
        self.play(FadeIn(soft), run_time=0.35)
        self.at("rot or are eaten")
        self.play(FadeOut(soft, shift=RIGHT * 1.0), run_time=0.8)
        self.at("Hard parts")
        self.play(Indicate(VGroup(main_shell, *icons), color=GOLD, scale_factor=1.04), run_time=0.6)
        sand = Rectangle(width=3.1, height=0.70, stroke_width=0, fill_color=SAND,
                         fill_opacity=0.72).move_to([-4.5, -0.60, 0])
        self.at("quick burial")
        self.play(FadeIn(sand, shift=DOWN * 0.6), main_shell.animate.shift(DOWN * 0.35), run_time=0.8)
        self.at("chance stays small")
        rare = T("rare", 40, GREY, weight=BOLD).move_to([4.6, -1.65, 0])
        self.play(FadeIn(rare), FadeOut(VGroup(*icons)), run_time=0.5)
        self.finish()


class S03Record(SpokenScene):
    def construct(self):
        bank = riverbank(with_fossils=False, with_gaps=False)
        buried = shell([-3.7, -2.82, 0], 0.62)
        self.add(bank, buried)
        heading = T("fossil record", 36, GOLD, weight=BOLD).move_to([0, 3.45, 0])
        self.at("make the fossil record")
        self.play(FadeIn(heading), run_time=0.5)
        more = VGroup(shell([1.3, -1.25, 0], 0.56, changed=0.35),
                      shell([-0.5, 0.20, 0], 0.50, changed=0.65),
                      trilobite().scale(0.38).move_to([3.7, 1.15, 0]))
        self.play(LaggedStart(*[GrowFromCenter(x) for x in more], lag_ratio=0.25), run_time=1.2)
        gaps = VGroup(
            Rectangle(width=11.75, height=0.18, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, -1.38, 0]),
            Rectangle(width=11.55, height=0.16, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, 0.12, 0]))
        self.at("record has gaps")
        self.play(FadeIn(gaps), run_time=0.7)
        gap_label = T("gap: missing details", 28, GREY).move_to([3.0, 0.14, 0])
        gap_label.layout_ok = True  # deliberately labels the gap it sits within
        self.at("some details are missing")
        self.play(FadeIn(gap_label, shift=LEFT * 0.15), run_time=0.5)
        self.at("does not make")
        self.play(gaps[0].animate.stretch(2.0, 1), gaps[1].animate.stretch(2.0, 1),
                  Indicate(VGroup(buried, more), color=GOLD, scale_factor=1.02), run_time=0.9)
        self.at("pattern can survive")
        bracket = Brace(VGroup(buried, more[1]), LEFT, color=GREEN)
        self.play(GrowFromCenter(bracket), run_time=0.5)
        self.finish()


class S04Patterns(SpokenScene):
    def construct(self):
        bank = riverbank()
        self.add(bank)
        arrow = Arrow([-6.25, -2.7, 0], [-6.25, 1.55, 0], color=GREEN,
                      stroke_width=6, tip_length=0.28)
        # labels start right of the arrow line and stay below the riverbank tag (ship check 2026-11-13)
        older = T("older", 28, GREEN)
        older.move_to([-6.05 + older.width / 2, -2.55, 0])
        younger = T("younger", 28, GREEN)
        younger.move_to([-6.05 + younger.width / 2, 1.18, 0])
        older.layout_ok = True  # stratigraphic labels intentionally sit on the bank
        younger.layout_ok = True
        self.play(GrowArrow(arrow), FadeIn(older), FadeIn(younger), run_time=0.8)
        inset = RoundedRectangle(corner_radius=0.16, width=3.15, height=2.15,
                                 stroke_color=GREY, stroke_width=3, fill_color=BG,
                                 fill_opacity=0.94).move_to([4.55, 0.75, 0])
        inset_title = fit_text("older rock, western Virginia", max_w=2.75, size=28,
                               color=TEXT, max_lines=2).move_to([4.55, 1.40, 0])
        tri = trilobite().scale(0.40).move_to([4.55, 0.25, 0])
        self.at("only in older rock")
        self.play(FadeIn(inset), FadeIn(inset_title), GrowFromCenter(tri), run_time=0.7)
        self.at("changed forms")
        forms = VGroup(*[shell([-2.5 + i * 1.8, -1.85 + i * 0.65, 0], 0.42,
                                    changed=i * 0.25) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in forms], lag_ratio=0.25), run_time=0.9)
        sea_overlay = Rectangle(width=11.7, height=4.15, stroke_width=0,
                                fill_color=WATER, fill_opacity=0.24).move_to([0, -0.50, 0])
        self.at("environment that is gone")
        self.play(FadeIn(sea_overlay), run_time=0.5)
        self.play(FadeOut(sea_overlay, shift=DOWN * 0.4), run_time=0.8)
        self.at("changes build history")
        self.play(Indicate(VGroup(arrow, *bank.shells), color=GREEN, scale_factor=1.01), run_time=0.7)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        lower = RoundedRectangle(corner_radius=0.12, width=9.7, height=1.35,
                                 stroke_color=SAND, stroke_width=3, fill_color=ROCK,
                                 fill_opacity=0.72).move_to([0, -0.68, 0])
        upper = RoundedRectangle(corner_radius=0.12, width=9.7, height=1.35,
                                 stroke_color=SAND, stroke_width=3, fill_color=ROCK_LIGHT,
                                 fill_opacity=0.72).move_to([0, 0.68, 0])
        middle = RoundedRectangle(corner_radius=0.08, width=9.7, height=0.85,
                                  stroke_color=SAND, stroke_width=3, fill_color=SAND,
                                  fill_opacity=0.48).move_to([0, 0, 0])
        low_shell = shell([-2.2, -0.88, 0], 0.95)
        high_shell = shell([2.2, 0.45, 0], 0.95, changed=0.75)
        self.add(lower, upper, middle, low_shell, high_shell)
        self.at("remove one band")
        self.play(middle.animate.shift(RIGHT * 8),
                  lower.animate.shift(DOWN * 0.70), low_shell.animate.shift(DOWN * 0.70),
                  upper.animate.shift(UP * 0.70), high_shell.animate.shift(UP * 0.70), run_time=1.0)
        missing = Rectangle(width=9.7, height=1.10, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.10)
        missing_label = T("missing layer", 30, GREY).move_to(missing)
        missing_label.layout_ok = True
        shimmer = shimmer_band()
        self.play(FadeIn(missing), FadeIn(missing_label), FadeIn(shimmer), run_time=0.4)
        missing_label._t = 0.0
        def _bob(mob, dt):
            missing_label._t += dt
            k = np.sin(2.2 * missing_label._t)
            missing.set_fill(GREY, opacity=0.18 + 0.12 * k)
            missing_label.set_opacity(0.75 + 0.25 * k)
            low_shell.set_opacity(0.8 + 0.2 * np.sin(2.2 * missing_label._t + 1.5))
            high_shell.set_opacity(0.8 + 0.2 * np.sin(2.2 * missing_label._t + 1.5))
        missing_label.add_updater(_bob)
        self.at("lower layer holds")
        self.play(Indicate(low_shell, color=GOLD, scale_factor=1.06), run_time=0.5)
        self.at("upper layer holds")
        self.play(Indicate(high_shell, color=GOLD, scale_factor=1.06), run_time=0.5)
        self.at("Does the missing band")
        q = question_card("Does a gap erase the observed pattern?", y=-3.15, max_w=10.6)
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.55)
        self.at("Think before")
        self.play(missing.animate.set_fill(GREY, opacity=0.18), run_time=0.5, rate_func=there_and_back)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Does a gap erase the observed pattern?"
    OPTIONS = ()
    SECONDS = 4.5
    CARD = {"y": -3.15, "max_w": 10.6}

    def backdrop(self):
        return observed_pair(False)


class S07Reveal(SpokenScene):
    def construct(self):
        pair = observed_pair(False)
        self.add(pair)
        no = T("NO", 48, GREEN, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(no, scale=1.15), run_time=0.45)
        self.at("compare the fossils")
        left_brace = BraceBetweenPoints(pair.low_shell.get_top(), [0, -0.58, 0], color=GREEN)
        right_brace = BraceBetweenPoints([0, 0.58, 0], pair.high_shell.get_bottom(), color=GREEN)
        self.play(GrowFromCenter(left_brace), GrowFromCenter(right_brace), run_time=0.8)
        obs1 = T("observed", 28, GREEN).next_to(pair.low_shell, RIGHT, buff=1.4).shift(DOWN * 0.25)
        obs2 = T("observed", 28, GREEN).next_to(pair.high_shell, LEFT, buff=1.4).shift(UP * 0.25)
        self.play(FadeIn(obs1), FadeIn(obs2), run_time=0.5)
        self.at("limits what we know")
        unknown = T("unknown details", 30, GREY).move_to(pair.missing)
        unknown.layout_ok = True
        self.play(swap(pair.missing_label, unknown), run_time=0.55)
        self.at("keep it gray")
        self.play(pair.missing.animate.set_fill(GREY, opacity=0.22), run_time=0.5)
        self.at("both observations and uncertainty")
        pulse(left_brace, base=5, amp=1.5, speed=2.0)
        pulse(right_brace, base=5, amp=1.5, speed=2.0)
        honest = caption("observations + uncertainty", color=GREEN)
        self.play(FadeIn(honest, shift=UP * 0.1), run_time=0.5)
        self.at("Limits stay visible")
        self.play(Indicate(unknown, color=GREY, scale_factor=1.06), run_time=0.6)
        self.finish()


def timeline_base():
    x_of = lambda mya: -5.75 + (550 - mya) / 550 * 11.5
    bar = Line([x_of(550), -0.25, 0], [x_of(0), -0.25, 0], color=GREY, stroke_width=7)
    labels = VGroup(T("550 million years ago", 28, GREY).move_to([-4.55, -0.78, 0]),
                    T("today", 28, GREY).move_to([5.38, -0.78, 0]))
    return x_of, VGroup(bar, labels)


class S08Timeline(SpokenScene):
    def construct(self):
        bank = riverbank()
        self.add(bank)
        x_of, base = timeline_base()
        self.play(FadeOut(bank), Rotate(base, angle=0.02), FadeIn(base), run_time=0.75)
        title = T("examples, schematic branches", 34, GOLD, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(title), run_time=0.4)
        data = [(518, "fish"), (365, "four-legged\nanimals"),
                (205, "mammal\nrelatives"), (150, "bird-like\ndinosaurs")]
        branches = VGroup()
        labels = VGroup()
        cues = ("Fish", "four-legged animals", "mammal relatives", "bird-like dinosaurs")
        for i, ((age, name), cue) in enumerate(zip(data, cues)):
            x = x_of(age)
            h = 1.05 + 0.33 * (i % 2)
            stem = Line([x, -0.25, 0], [x, -0.25 + h, 0], color=GOLD, stroke_width=5)
            dot = Dot([x, -0.25 + h, 0], radius=0.13, color=GOLD)
            lab = VGroup(T(name, 28, GOLD, weight=BOLD, line_spacing=0.8),
                         M(f"{age} million years", 24, TEXT)).arrange(DOWN, buff=0.10)
            centers = [(-5.05, 1.55), (-1.4, 2.20), (0.30, -1.70), (4.65, 2.20)]
            lab.move_to([centers[i][0], centers[i][1], 0])
            self.at(cue)
            self.play(Create(stem), GrowFromCenter(dot), FadeIn(lab, shift=UP * 0.1), run_time=0.55)
            branches.add(stem, dot)
            labels.add(lab)
        pulse(base[0], base=7, amp=2.0, speed=1.6)
        scan = Rectangle(width=0.28, height=4.6, stroke_width=0, fill_color=GOLD,
                         fill_opacity=0.16).move_to([-5.6, 0.35, 0])
        scan._x0 = -5.6

        def scan_time(mob, dt):
            mob.shift(RIGHT * 1.15 * dt)
            if mob.get_x() > 5.6:
                mob.set_x(mob._x0)

        scan.add_updater(scan_time)
        scan.set_z_index(-1)
        self.add(scan)
        self.at("not one ladder")
        staircase = VGroup(*[Line([-5.55 + i * 0.90, -2.65 + i * 0.20, 0],
                                    [-4.75 + i * 0.90, -2.65 + i * 0.20, 0], color=GREY,
                                    stroke_width=5) for i in range(4)])
        cross = Cross(staircase, stroke_color=GREEN, stroke_width=6)
        self.play(FadeIn(staircase), run_time=0.35)
        self.play(Create(cross), FadeOut(staircase), run_time=0.55)
        self.at("examples, not ancestors")
        note = caption("examples — not ancestors", color=GREEN)
        self.play(FadeOut(cross), FadeIn(note), Indicate(branches, color=GREEN, scale_factor=1.01), run_time=0.6)
        self.finish()


class S09EvidenceJobs(SpokenScene):
    def construct(self):
        bank = riverbank()
        self.add(bank)
        jobs = [("existence", [-4.75, 3.45, 0]), ("extinction", [-1.65, 3.45, 0]),
                ("change", [1.35, 3.45, 0]), ("environment", [4.65, 3.45, 0])]
        job_labels = VGroup()
        for (word, pos), cue in zip(jobs, ("existence", "extinction", "change", "past environments")):
            lab = T(word, 30, GREEN, weight=BOLD).move_to(pos)
            job_labels.add(lab)
            self.at(cue)
            self.play(FadeIn(lab, shift=DOWN * 0.12), run_time=0.35)
            self.play(Indicate(bank.shells, color=GOLD, scale_factor=1.015), run_time=0.28)
        self.at("some claims and not others")
        self.play(FadeOut(job_labels), run_time=0.4)
        focus = shell([-2.6, -0.7, 0], 1.25)
        bob(focus, amp=0.12, speed=4.0)
        self.play(FadeOut(bank), FadeIn(focus), run_time=0.6)
        old_sea = VGroup(Rectangle(width=5.2, height=2.2, stroke_color=WATER, stroke_width=3,
                                   fill_color=WATER, fill_opacity=0.22).move_to([-2.6, -0.5, 0]),
                         T("old sea", 32, WATER).move_to([-2.6, 0.9, 0]))
        self.at("place life in an old sea")
        self.play(FadeIn(old_sea), run_time=0.55)
        tree = branch_tree(at=(3.8, -0.1, 0))
        pulse(tree, base=5.0, amp=1.5, speed=1.7)
        qs = VGroup(*[T("?", 38, GREY).move_to(p) for p in ([2.5, 1.45, 0], [3.8, 1.75, 0], [5.1, 1.45, 0])])
        self.at("cannot name every branch")
        self.play(Create(tree), FadeIn(qs), run_time=0.7)
        self.at("clear scope")
        self.play(FadeIn(scope_tag("this fossil alone")), run_time=0.4)
        self.finish()


class S10Theory(SpokenScene):
    def construct(self):
        panels = TwoPanel("observations", "explanation", colors=(GOLD, GREEN), top=3.0, bottom=-2.5)
        self.play(FadeIn(panels), run_time=0.6)
        obs = VGroup(shell(radius=0.55), trilobite().scale(0.33),
                     shell(radius=0.45, changed=0.7), T("past sea", 28, WATER)).arrange_in_grid(2, 2, buff=0.45)
        panels.put(obs, "left")
        self.play(LaggedStart(*[FadeIn(x) for x in obs], lag_ratio=0.2), run_time=0.9)
        theory = chip("evolution: tested explanation", GREEN, 30)
        panels.put(theory, "right")
        self.at("well-tested explanation")
        self.play(FadeIn(theory, scale=0.92), run_time=0.55)
        obs_brace = Brace(obs, RIGHT, color=GREEN)
        link = Arrow(obs_brace.get_right(), theory.get_left(), buff=0.15, color=GREEN,
                     stroke_width=4, tip_length=0.18)
        links = VGroup(obs_brace, link)
        self.at("many lines of evidence")
        self.play(GrowFromCenter(obs_brace), GrowArrow(link), run_time=0.8)
        pulse(theory[0], base=2.5, amp=1.2, speed=1.8)
        breathe_fill(theory[0], GREEN, lo=0.08, hi=0.55, speed=6.0)
        rule = caption("populations change + share ancestors", color=GREEN)
        self.at("populations change")
        self.play(FadeIn(rule), run_time=0.45)
        new = RoundedRectangle(corner_radius=0.14, width=3.0, height=1.1,
                               stroke_color=GREY, stroke_width=3).move_to([4.6, -1.65, 0])
        new_lab = T("new evidence", 28, GREY).move_to(new)
        new_lab.layout_ok = True
        self.at("new evidence can test")
        self.play(FadeIn(new, shift=LEFT * 0.2), FadeIn(new_lab, shift=LEFT * 0.2), run_time=0.55)
        test_arrow = Arrow(theory.get_bottom(), new.get_top(), color=GREEN, stroke_width=4,
                           tip_length=0.18, buff=0.15)
        q = T("?", 36, GREEN).next_to(test_arrow, LEFT, buff=0.1)
        self.play(GrowArrow(test_arrow), FadeIn(q), run_time=0.5)
        self.at("makes it testable")
        self.play(Indicate(new, color=GREEN, scale_factor=1.03), run_time=0.55)
        self.finish()


def sequence_strip():
    letters = "A  T  G  C"
    box = RoundedRectangle(corner_radius=0.12, width=2.15, height=0.72,
                           stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                           fill_opacity=0.12)
    txt = M(letters, 25, TEAL).move_to(box)
    txt.layout_ok = True  # text is intentionally contained by its sequence-strip icon
    return VGroup(box, txt)


class S11Return(SpokenScene):
    def construct(self):
        bank = riverbank(with_fossils=False, with_gaps=True)
        fossil = shell([-3.4, -0.75, 0], 1.25)
        self.add(bank)
        self.play(GrowFromCenter(fossil), run_time=0.65)
        self.at("living thing and an ancient sea")
        ancient = T("life + ancient sea", 32, GREEN).move_to([-3.4, -2.30, 0])
        ancient.layout_ok = True  # label is deliberately anchored to its fossil-bearing layer
        self.play(FadeIn(ancient), run_time=0.5)
        modern = shell([0.0, 1.55, 0], 1.05, color=TEXT, fill=0.08)
        bob(modern, amp=0.06, speed=1.5)
        self.at("living scallops")
        self.play(FadeIn(modern, shift=LEFT * 0.25), run_time=0.65)
        self.at("which organisms share branches")
        tree = branch_tree(at=(4.25, -0.10, 0), scale=0.9)
        qs = VGroup(*[T("?", 34, GREY).move_to(p) for p in ([3.15, 1.2, 0], [4.2, 1.55, 0], [5.25, 1.2, 0])])
        for qmark in qs:
            qmark.layout_ok = True  # unresolved branch marks sit over the landscape
        self.play(Create(tree), FadeIn(qs), run_time=0.7)
        bone = bone_icon(BLUE).scale(0.95).move_to([2.3, -2.0, 0])
        seq = sequence_strip().move_to([4.9, -2.0, 0])
        self.at("Bones and sequences")
        self.play(FadeIn(bone, shift=UP * 0.15), FadeIn(seq, shift=UP * 0.15), run_time=0.55)
        arrows = VGroup(Arrow(bone.get_top(), [3.55, -0.65, 0], buff=0.12, color=BLUE, tip_length=0.16),
                        Arrow(seq.get_top(), [4.85, -0.65, 0], buff=0.12, color=TEAL, tip_length=0.16))
        self.at("test that next")
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.55)
        self.at("question continues")
        self.play(Indicate(qs, color=GREY, scale_factor=1.08), run_time=0.5)
        self.finish()


class S12Scope(SpokenScene):
    def construct(self):
        bank = riverbank()
        self.add(bank)
        self.at("record is incomplete")
        self.play(Indicate(bank.gaps, color=GREY, scale_factor=1.0), run_time=0.55)
        limit = caption("Every claim keeps its limits", color=GREY)
        self.play(FadeIn(limit), run_time=0.45)
        self.at("observed fossils remain evidence")
        self.play(Indicate(bank.shells, color=GOLD, scale_factor=1.06), FadeOut(limit), run_time=0.7)
        outline = SurroundingRectangle(VGroup(bank.layers, bank.shells), color=GREEN,
                                       stroke_width=5, buff=0.10)
        self.at("Across many layers")
        self.play(Create(outline), run_time=0.75)
        sea = Rectangle(width=11.8, height=4.2, stroke_width=0, fill_color=WATER,
                        fill_opacity=0.20).move_to([0, -0.5, 0])
        self.at("life and environments changed")
        self.play(FadeIn(sea), run_time=0.55)
        self.play(FadeOut(sea, shift=DOWN * 0.35), bank.water.animate.set_fill(WATER, opacity=0.62), run_time=0.75)
        self.at("through time")
        self.play(Indicate(outline, color=GREEN, scale_factor=1.0), run_time=0.5)
        self.finish()


class S13End(EndCard):
    LINE = "Fossils reveal life's change through time, even with gaps."
