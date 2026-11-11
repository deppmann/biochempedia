"""Where Could Life Hide? — a continuous laboratory film.

COLOR MAP
  GREEN       living material, cells, fermentation products
  BLUE        inorganic / lifeless starting material
  RED / GOLD  the claimed vital force and its last hiding place
  YELLOW      experimental action, heat, controls
  TEAL        evidence established by an experiment
  TEXT/GREY   laboratory structure and neutral labels

Every substance is a labelled block or schematic region; no molecular structure is drawn.
"""
import math
import random

from bp_style import *  # noqa: F401,F403


# ---------- one fixed laboratory world ----------

CELL_X = -4.25
FLASK_X = 4.25
BENCH_Y = -2.72
WALL_X = 0.0


def lab_backdrop():
    """The same high-contrast nineteenth-century laboratory wall in every scene."""
    wall = Rectangle(width=13.35, height=6.25, stroke_width=0,
                     fill_color="#262B35", fill_opacity=1).move_to([0, 0.28, 0])
    dado = Line([-6.65, -2.35, 0], [6.65, -2.35, 0], color=GREY, stroke_width=3).set_opacity(0.45)
    crown = Line([-6.65, 3.17, 0], [6.65, 3.17, 0], color=GREY, stroke_width=3).set_opacity(0.35)
    g = VGroup(wall, dado, crown).set_z_index(-20)
    return g


class LabSpokenScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(lab_backdrop())


def schematic():
    return T("SCHEMATIC", 22, GREY, weight=BOLD).move_to([5.72, -3.42, 0])


def bench():
    top = Line([-6.3, BENCH_Y, 0], [6.3, BENCH_Y, 0], color=GREY, stroke_width=5)
    legs = VGroup(
        Line([-5.65, BENCH_Y, 0], [-5.65, -3.55, 0], color=GREY, stroke_width=5),
        Line([5.65, BENCH_Y, 0], [5.65, -3.55, 0], color=GREY, stroke_width=5),
    )
    return VGroup(top, legs).set_opacity(0.7)


def yeast_cell(scale=1.0, center=(CELL_X, -0.25, 0)):
    body = Ellipse(width=3.35, height=4.5, color=GREEN, stroke_width=5,
                   fill_color=GREEN, fill_opacity=0.10)
    inner = Ellipse(width=1.15, height=0.82, color=GREEN, stroke_width=3,
                    fill_color=GREEN, fill_opacity=0.14).shift(UP * 0.45 + LEFT * 0.25)
    label = T("YEAST CELL", 30, GREEN, weight=BOLD).next_to(body, DOWN, buff=0.18)
    g = VGroup(body, inner, label).scale(scale).move_to(center)
    return g


def lab_flask(center=(FLASK_X, -0.55, 0), scale=1.0, liquid=BLUE):
    outline = VMobject(color=TEXT, stroke_width=5)
    outline.set_points_as_corners([
        [-0.45, 2.1, 0], [-0.45, 0.75, 0], [-1.5, -1.55, 0],
        [-1.35, -1.8, 0], [1.35, -1.8, 0], [1.5, -1.55, 0],
        [0.45, 0.75, 0], [0.45, 2.1, 0],
    ])
    lip = Line([-0.62, 2.1, 0], [0.62, 2.1, 0], color=TEXT, stroke_width=6)
    fluid = Polygon([-1.34, -1.45, 0], [1.34, -1.45, 0], [0.95, -0.55, 0],
                    [-0.95, -0.55, 0], stroke_width=0, fill_color=liquid, fill_opacity=0.35)
    g = VGroup(fluid, outline, lip).scale(scale).move_to(center)
    return g


class RisingBubbles(VGroup):
    """A steady schematic bubble stream whose motion is visible during spoken holds."""
    def __init__(self, cx=FLASK_X, y0=-1.75, y1=1.35, width=1.5, n=11,
                 color=GREEN, seed=7, speed=0.24):
        super().__init__()
        rng = random.Random(seed)
        self.cx, self.y0, self.y1, self.width = cx, y0, y1, width
        self.phase = [rng.random() for _ in range(n)]
        self.xoff = [rng.uniform(-width / 2, width / 2) for _ in range(n)]
        self.rate = [rng.uniform(speed * 0.8, speed * 1.2) for _ in range(n)]
        self.clock = 0.0
        for _ in range(n):
            self.add(Circle(radius=rng.uniform(0.055, 0.11), color=color,
                            stroke_width=2.5, fill_color=color, fill_opacity=0.12))
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    def _place(self):
        span = self.y1 - self.y0
        for i, bubble in enumerate(self.submobjects):
            f = (self.phase[i] + self.clock * self.rate[i]) % 1
            bubble.move_to([self.cx + self.xoff[i] + 0.06 * math.sin(9 * f + i),
                            self.y0 + span * f, 0])
            opacity = min(1, f * 7) * min(1, (1 - f) * 7)
            bubble.set_stroke(opacity=opacity).set_fill(opacity=0.12 * opacity)

    def _advance(self, dt):
        self.clock += dt
        self._place()


class OrbitSpecks(VGroup):
    def __init__(self, center=(CELL_X, -0.2, 0), rx=1.15, ry=1.55, n=7,
                 color=GOLD, speed=0.30, seed=4):
        super().__init__()
        rng = random.Random(seed)
        self.center, self.rx, self.ry, self.speed = np.array(center), rx, ry, speed
        self.phase = [rng.random() * TAU for _ in range(n)]
        self.clock = 0
        for _ in range(n):
            self.add(Dot(radius=0.075, color=color))
        self._place()
        self.add_updater(lambda m, dt: m._advance(dt))

    def _place(self):
        for dot, p in zip(self.submobjects, self.phase):
            a = p + self.clock * self.speed
            dot.move_to(self.center + [self.rx * math.cos(a), self.ry * math.sin(a), 0])

    def _advance(self, dt):
        self.clock += dt
        self._place()


def life_wall(height=5.55, label="LIFE\nREQUIRED?"):
    bar = RoundedRectangle(width=0.62, height=height, corner_radius=0.16,
                           color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.16)
    lab = T(label, 30, GOLD, weight=BOLD, line_spacing=0.78).rotate(PI / 2)
    lab.move_to(bar)
    return VGroup(bar, lab).move_to([WALL_X, -0.05, 0])


def crack_on_wall():
    return VMobject(color=RED, stroke_width=6).set_points_as_corners([
        [0.02, 2.35, 0], [-0.18, 1.45, 0], [0.16, 0.65, 0],
        [-0.20, -0.25, 0], [0.14, -1.15, 0], [-0.08, -2.25, 0],
    ])


def ruler(lit=0):
    names = ("MAKE MOLECULE", "START LIFELESS", "REMOVE CELLS")
    parts = VGroup()
    for i, name in enumerate(names):
        color = TEAL if i < lit else GREY
        box = RoundedRectangle(width=3.75, height=1.45, corner_radius=0.14,
                               color=color, stroke_width=4,
                               fill_color=TEAL, fill_opacity=0.16 if i < lit else 0.02)
        num = M(str(i + 1), 32, color, weight=BOLD).move_to(box.get_top() + DOWN * 0.34)
        lab = T(name, 28, color, weight=BOLD).move_to(box.get_bottom() + UP * 0.37)
        parts.add(VGroup(box, num, lab))
    parts.arrange(RIGHT, buff=0.22).move_to([0, -0.78, 0])
    title = T("HOW FAR DOES THE EVIDENCE REACH?", 32, TEXT, weight=BOLD).move_to([0, 2.9, 0])
    return VGroup(title, parts)


def test_card(name, pos, width=3.5):
    cell_lab = T("CELL", 28, GREY)
    chem_lab = T("CHEMICAL", 28, GREY)
    cells = RoundedRectangle(width=cell_lab.width + 0.28, height=0.72,
                             corner_radius=0.1, color=GREY, stroke_width=2)
    chem = RoundedRectangle(width=chem_lab.width + 0.28, height=0.72,
                            corner_radius=0.1, color=GREY, stroke_width=2)
    windows = VGroup(cells, chem).arrange(RIGHT, buff=0.18)
    width = max(width, windows.width + 0.38)
    box = RoundedRectangle(width=width, height=2.05, corner_radius=0.18,
                           color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.07)
    title = T(name, 28, YELLOW, weight=BOLD).move_to(box.get_top() + DOWN * 0.32)
    windows.move_to(box.get_bottom() + UP * 0.55)
    labs = VGroup(cell_lab.move_to(cells), chem_lab.move_to(chem))
    return VGroup(box, title, windows, labs).move_to(pos)


def tiny_scraps():
    scraps = VGroup(*[Ellipse(width=0.22, height=0.12, color=GREEN, fill_color=GREEN,
                              fill_opacity=0.7, stroke_width=2) for _ in range(2)])
    scraps[0].move_to([4.0, 0.9, 0]); scraps[1].move_to([4.48, 1.22, 0])
    return scraps


# ---------- scenes ----------

class S01Hook(LabSpokenScene):
    def construct(self):
        b = bench(); cell = yeast_cell(); flask = lab_flask(); wall = life_wall()
        specks = OrbitSpecks(); failed = RisingBubbles(color=GREY, n=5, speed=0.10)
        failed.set_opacity(0.45)
        self.play(FadeIn(b), GrowFromCenter(cell), FadeIn(schematic()), run_time=0.9)
        self.play(FadeIn(specks), run_time=0.5)
        self.at("special force")
        self.play(Create(wall[0]), run_time=0.8)
        self.play(FadeIn(flask), FadeIn(failed), run_time=0.8)
        self.play(failed.animate.set_opacity(0), flask[0].animate.set_fill(opacity=0.18), run_time=1.2)
        self.at("many early")
        self.play(Write(wall[1]), run_time=0.9)
        self.at("called it")
        vital = T("VITAL FORCE", 34, RED, weight=BOLD).move_to([0, 2.98, 0])
        self.play(FadeIn(vital, shift=DOWN * 0.12),
                  wall[0].animate.set_stroke(RED).set_fill(RED, opacity=0.18), run_time=0.8)
        self.play(Indicate(specks, color=GOLD, scale_factor=1.05), run_time=1.1)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Vitalism"
    TITLE = "Where Could Life Hide?"

    def construct(self):
        self.add(lab_backdrop())
        wall = life_wall(); wall[1].set_opacity(0)
        specks = OrbitSpecks(center=(0, -0.1, 0), rx=0.24, ry=2.2, n=9, speed=0.45)
        title = T(self.TITLE.upper(), 48, TEXT, font=TITLE_FONT, weight=BOLD)
        fit(title, 11.2, 1.4); title.move_to([0, 0.15, 0])
        self.add(wall[0], specks)
        self.play(Write(title), run_time=0.9)
        q = T("?", 54, GOLD, font=TITLE_FONT, weight=BOLD).move_to([0, 3.05, 0])
        self.play(ReplacementTransform(title, q), run_time=0.75)
        self.finish()


class S03Wall(LabSpokenScene):
    def construct(self):
        b = bench(); wall = life_wall(); cell = yeast_cell()
        cell[0].stretch(1.25, 0)
        cell[1].set_opacity(0)
        specks = OrbitSpecks(center=(CELL_X, 0.35, 0), rx=0.62, ry=0.34)
        belt = VGroup(Line([2.3, -1.72, 0], [6.05, -1.72, 0], color=GREY, stroke_width=7),
                      T("INORGANIC", 28, BLUE, weight=BOLD).move_to([4.18, -2.15, 0]))
        self.add(b, wall, cell, specks, belt, schematic())
        self.play(ShowPassingFlash(belt[0].copy().set_stroke(BLUE, 12), time_width=0.7),
                  run_time=1.5)
        self.at("rocks and salts")
        rocks = chip("ROCKS + SALTS", BLUE, 30).move_to([3.75, -1.15, 0])
        self.play(FadeIn(rocks, shift=RIGHT * 0.3), run_time=0.7)
        self.play(rocks.animate.shift(RIGHT * 0.7), run_time=1.2, rate_func=linear)
        self.play(ShowPassingFlash(belt[0].copy().set_stroke(BLUE, 12), time_width=0.7),
                  run_time=1.2)
        self.at("sugar fat")
        organics = chip("SUGAR · FAT · UREA", GREEN, 28).move_to([-4.25, -0.72, 0])
        self.play(FadeIn(organics, scale=0.9), run_time=0.7)
        self.play(Rotate(organics, angle=0.13, about_point=cell[0].get_center(), rate_func=there_and_back), run_time=1.5)
        self.play(cell.animate.scale(1.035), run_time=0.9, rate_func=there_and_back)
        self.at("only life")
        taller = life_wall(6.35)
        self.play(Transform(wall, taller), specks.animate.set_opacity(1), run_time=1.1)
        self.play(rocks.animate.shift(RIGHT * 0.55),
                  Rotate(organics, angle=-0.13, about_point=cell[0].get_center(), rate_func=there_and_back),
                  run_time=1.8)
        self.finish()


class S04Wohler(LabSpokenScene):
    def construct(self):
        b = bench(); wall = life_wall(6.35); cell = yeast_cell(); flask = lab_flask()
        salt = chip("AMMONIUM CYANATE", BLUE, 28).move_to([3.15, 1.85, 0])
        swirl = OrbitSpecks(center=(FLASK_X, -0.8, 0), rx=0.75, ry=0.45, n=7,
                           color=BLUE, speed=0.8, seed=11)
        self.add(b, wall, cell, flask, salt, schematic())
        self.at("tried to make")
        salt_block = RoundedRectangle(width=1.55, height=0.52, corner_radius=0.1,
                                      color=BLUE, fill_color=BLUE, fill_opacity=0.28).move_to(salt)
        self.play(ReplacementTransform(salt, salt_block), run_time=0.45)
        self.play(salt_block.animate.move_to([3.9, 0.9, 0]).rotate(-0.22), run_time=1.0)
        self.play(FadeOut(salt_block, shift=DOWN * 0.7), FadeIn(swirl), run_time=0.8)
        self.at("urea crystallized")
        crystals = VGroup(*[Square(side_length=0.30, color=GREEN,
                                   fill_color=GREEN, fill_opacity=0.7).stretch(1.35, 1).rotate(PI / 4)
                            for _ in range(7)])
        for c, p in zip(crystals, [(3.7,-1.55),(4.05,-1.45),(4.4,-1.52),(4.72,-1.4),
                                   (3.9,-1.12),(4.3,-1.12),(4.58,-1.03)]): c.move_to([*p,0])
        urea = chip("UREA", GREEN, 30).move_to([5.55, 0.25, 0])
        self.play(FadeOut(swirl), FadeIn(crystals, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(urea, shift=UP * 0.12), run_time=0.6)
        self.at("without a body")
        self.play(cell.animate.shift(LEFT * 3.2).set_opacity(0), run_time=1.0)
        self.at("wall cracked")
        crack = crack_on_wall()
        self.play(Create(crack), FadeOut(wall[1]),
                  wall[0].animate.set_stroke(opacity=0.55), run_time=0.9)
        self.play(crystals.animate.shift(UP * 0.07), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S05Loophole(LabSpokenScene):
    def construct(self):
        b = bench(); wall = life_wall(6.35); wall[1].set_opacity(0)
        crack = crack_on_wall(); flask = lab_flask()
        urea = chip("UREA", GREEN, 30).move_to([5.55, 0.25, 0])
        cyanate = chip("AMMONIUM CYANATE", BLUE, 28).move_to([2.2, 2.25, 0])
        source = chip("BLOOD · HORN · HOOF", GREEN, 28).move_to([-4.25, 1.25, 0])
        ribbon = CubicBezier(source.get_right(), [-1.5,1.25,0], [0.5,2.2,0], cyanate.get_left(),
                             color=RED, stroke_width=4)
        spark = Star(n=4, outer_radius=0.16, inner_radius=0.06, color=GOLD,
                     fill_color=GOLD, fill_opacity=1).move_to(source.get_right())
        self.add(b, wall, crack, flask, urea, schematic())
        # Show the provenance chain before naming it, and keep the large ribbon moving.
        self.play(FadeIn(cyanate), Create(ribbon), run_time=1.4)
        self.play(FadeIn(source, shift=RIGHT * 0.2),
                  ShowPassingFlash(ribbon.copy().set_stroke(GOLD, 11), time_width=0.6), run_time=1.3)
        self.play(source.animate.shift(DOWN * 0.34), run_time=0.9, rate_func=there_and_back)
        provenance_world = VGroup(b, wall, crack, flask, urea, cyanate, source, ribbon)
        self.play(provenance_world.animate.shift(RIGHT * 0.14), run_time=1.0, rate_func=there_and_back)
        self.at("traced to animal")
        self.add(spark)
        self.play(MoveAlongPath(spark, ribbon), run_time=1.6, rate_func=linear)
        self.play(spark.animate.move_to([0.02, 0.3, 0]), run_time=0.8)
        self.at("a skeptic")
        patch = RoundedRectangle(width=0.68, height=3.7, corner_radius=0.15, color=RED,
                                 fill_color=RED, fill_opacity=0.12, stroke_width=4).move_to([0,-0.2,0])
        tag = T("LOOPHOLE", 30, RED, weight=BOLD).rotate(0.06).move_to([1.25, 0.35, 0])
        self.play(FadeIn(patch), FadeOut(crack), FadeIn(tag, shift=UP * 0.2), run_time=0.9)
        self.play(ShowPassingFlash(ribbon.copy().set_stroke(GOLD, 9), time_width=0.5), run_time=1.5)
        self.finish()


class S06Rule(LabSpokenScene):
    def construct(self):
        r = ruler(1); spark = Star(n=4, outer_radius=0.18, inner_radius=0.07, color=GOLD,
                                  fill_color=GOLD, fill_opacity=1)
        spark.move_to(r[1][0].get_top() + UP * 0.45)
        trace = Dot(radius=0.12, color=GOLD).move_to(r[1][2].get_top() + UP * 0.55)
        self.play(FadeIn(r[0]), LaggedStart(*[GrowFromCenter(x) for x in r[1]], lag_ratio=0.18), run_time=1.4)
        self.play(Circumscribe(r[1][0], color=TEAL, stroke_width=7), run_time=1.2)
        self.play(r[1][1].animate.shift(UP * 0.10), run_time=0.7, rate_func=there_and_back)
        self.at("remove life")
        self.play(FadeIn(trace),
                  spark.animate.move_to(trace.get_center() + UP * 0.75),
                  r.animate(rate_func=there_and_back).shift(RIGHT * 0.14), run_time=1.4)
        self.at("prove it is gone")
        lens = Circle(radius=0.42, color=TEAL, stroke_width=5).move_to(trace)
        handle = Line(lens.get_corner(DR), lens.get_corner(DR) + [0.55,-0.55,0], color=TEAL, stroke_width=6)
        cross = Cross(stroke_color=RED, stroke_width=6).scale(0.24).move_to(trace)
        self.play(Create(lens), GrowFromPoint(handle, lens.get_corner(DR)),
                  r.animate(rate_func=there_and_back).shift(LEFT * 0.14), run_time=0.7)
        self.play(Create(cross), trace.animate.set_opacity(0.2),
                  r.animate(rate_func=there_and_back).shift(RIGHT * 0.14), run_time=0.9)
        self.at("only as far")
        reach = Line(r[1][0].get_left(), r[1][0].get_right(), color=TEAL, stroke_width=8)
        self.play(Create(reach), spark.animate.move_to(r[1][1].get_top() + UP * 0.45), run_time=1.2)
        self.play(spark.animate.shift(RIGHT * 0.25), run_time=0.8, rate_func=there_and_back)
        self.play(VGroup(lens, handle).animate.shift(LEFT * 0.3), run_time=1.1, rate_func=there_and_back)
        self.play(VGroup(r, lens, handle, cross, trace, reach).animate.shift(DOWN * 0.12),
                  run_time=1.0, rate_func=there_and_back)
        self.finish()


class S07Kolbe(LabSpokenScene):
    def construct(self):
        r = ruler(1); r.scale(0.78); r[0].set_opacity(0); r[1].move_to([0, -2.72, 0])
        furnace = Circle(radius=0.65, color=RED, stroke_width=8).move_to([-2.15, 1.2, 0])
        pipe = VMobject(color=GREY, stroke_width=12).set_points_as_corners([
            [-1.45,1.2,0], [0.0,1.2,0], [0.0,0.4,0], [2.15,0.4,0]])
        charcoal = chip("CHARCOAL", BLUE, 28).move_to([-5.25, 1.7, 0])
        sulfur = chip("SULFUR", BLUE, 28).move_to([-5.25, 0.7, 0])
        self.add(r, charcoal, sulfur, furnace, schematic())
        self.play(charcoal.animate.shift(RIGHT * 0.32), sulfur.animate.shift(RIGHT * 0.32), run_time=1.2)
        self.play(furnace.animate.scale(1.12), run_time=0.7, rate_func=there_and_back)
        self.at("built acetic acid")
        pellets = VGroup(
            RoundedRectangle(width=0.72, height=0.28, corner_radius=0.08,
                             color=BLUE, fill_color=BLUE, fill_opacity=0.35),
            RoundedRectangle(width=0.72, height=0.28, corner_radius=0.08,
                             color=BLUE, fill_color=BLUE, fill_opacity=0.35),
        )
        pellets[0].move_to(charcoal); pellets[1].move_to(sulfur)
        self.play(ReplacementTransform(charcoal, pellets[0]),
                  ReplacementTransform(sulfur, pellets[1]), run_time=0.6)
        self.play(pellets[0].animate.move_to([-2.15,1.38,0]),
                  pellets[1].animate.move_to([-2.15,1.02,0]), run_time=1.0)
        cs = chip("CARBON DISULFIDE", BLUE, 28).move_to([0.25, 2.35, 0])
        self.play(FadeOut(pellets), FadeIn(cs, shift=RIGHT * 0.2), run_time=0.8)
        self.play(Create(pipe), run_time=0.8)
        power_label = T("POWER", 28, YELLOW, weight=BOLD)
        power_box = RoundedRectangle(width=power_label.width + 0.3, height=0.72,
                                     corner_radius=0.12, color=YELLOW,
                                     fill_color=YELLOW, fill_opacity=0.15)
        battery = VGroup(power_box, power_label.move_to(power_box)).move_to([1.05, 1.75, 0])
        acid = chip("ACETIC ACID", GREEN, 28).move_to([3.65, 0.4, 0])
        self.play(FadeOut(cs), FadeIn(battery),
                  ShowPassingFlash(pipe.copy().set_stroke(YELLOW, 18), time_width=0.6),
                  run_time=1.4)
        self.play(FadeIn(acid, shift=RIGHT * 0.3), run_time=0.7)
        self.play(acid.animate.shift(RIGHT * 0.45), run_time=0.9, rate_func=there_and_back)
        self.at("counted those starting")
        lifeless = T("LIFELESS INPUTS", 28, BLUE, weight=BOLD).move_to([-4.55, 2.75, 0])
        self.play(FadeIn(lifeless, shift=DOWN * 0.1), run_time=0.7)
        self.at("second segment")
        target = ruler(2); target.scale(0.78); target[0].set_opacity(0); target[1].move_to([0, -2.72, 0])
        self.play(Transform(r, target), FadeOut(lifeless), FadeOut(acid),
                  FadeOut(battery), FadeOut(pipe), FadeOut(furnace), run_time=0.9)
        self.play(r[1][1].animate.shift(UP * 0.14),
                  run_time=1.1, rate_func=there_and_back)
        self.play(r.animate.shift(LEFT * 0.14), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S08CellClaim(LabSpokenScene):
    def construct(self):
        r = ruler(2); r.scale(0.68); r[0].set_opacity(0); r[1].move_to([0, -3.02, 0])
        cell = yeast_cell(scale=0.9, center=(0, 0.35, 0))
        cell[1].set_opacity(0); cell[2].set_opacity(0)
        yeast_label = T("YEAST CELL", 30, GREEN, weight=BOLD).move_to([0, 2.7, 0])
        specks = OrbitSpecks(center=(0.45, 1.05, 0), rx=0.34, ry=0.24)
        sugar_in = chip("SUGAR", GREEN, 28).move_to([-0.5, 0.62, 0])
        rotor = VGroup(Circle(radius=0.72, color=YELLOW, stroke_width=5),
                       *[Line([0,0,0], [0.62*math.cos(a),0.62*math.sin(a),0],
                              color=YELLOW, stroke_width=3) for a in np.linspace(0, TAU, 8, endpoint=False)])
        rotor.move_to([0.45, -0.18, 0])
        fermentation = T("FERMENTATION", 28, YELLOW, weight=BOLD).move_to([0, -1.78, 0])
        wheel = VGroup(rotor, fermentation)
        outside = chip("SUGAR", GREEN, 28).move_to([4.55, 0.3, 0])
        bubbles = RisingBubbles(cx=0.72, y0=-0.2, y1=2.35, width=0.5, n=7, seed=14)
        self.add(r, cell, yeast_label, specks, sugar_in, schematic())
        self.play(cell[0].animate.scale(1.05), run_time=1.1, rate_func=there_and_back)
        self.play(cell[1].animate.shift(RIGHT * 0.35), run_time=1.0, rate_func=there_and_back)
        self.play(VGroup(r, cell, specks, sugar_in).animate.shift(RIGHT * 0.14),
                  run_time=1.0, rate_func=there_and_back)
        self.at("fermentation appeared")
        self.play(FadeIn(wheel), FadeIn(bubbles), run_time=0.8)
        self.play(Rotate(wheel[0], angle=PI, rate_func=linear),
                  cell.animate.scale(1.045), run_time=1.8, rate_func=there_and_back)
        self.at("sugar to alcohol")
        self.play(FadeIn(outside, shift=LEFT * 0.2), run_time=0.7)
        self.play(cell.animate.shift(LEFT * 0.24), run_time=1.1, rate_func=there_and_back)
        self.at("could not be separated")
        fence = Circle(radius=2.45, color=RED, stroke_width=7).move_to([0,0.25,0])
        self.play(FadeOut(yeast_label), FadeOut(fermentation), run_time=0.35)
        self.play(Create(fence), run_time=0.65)
        self.play(Rotate(wheel[0], angle=PI, rate_func=linear),
                  cell.animate.scale(1.04), run_time=1.6, rate_func=there_and_back)
        self.finish()


class S09Buchner(LabSpokenScene):
    def construct(self):
        mortar = ArcBetweenPoints([-2.5,-0.6,0], [2.5,-0.6,0], angle=PI/2,
                                  color=TEXT, stroke_width=8).shift(UP * 1.1)
        pestle = RoundedRectangle(width=0.42, height=3.2, corner_radius=0.18, color=GREY,
                                  fill_color=GREY, fill_opacity=0.35).rotate(-0.55).move_to([0.65,1.15,0])
        cells = VGroup(*[Circle(radius=0.38, color=GREEN, fill_color=GREEN, fill_opacity=0.2)
                         for _ in range(5)])
        grains = VGroup(*[Dot(radius=0.085, color=YELLOW) for _ in range(12)])
        rng = random.Random(21)
        for m in [*cells, *grains]: m.move_to([rng.uniform(-1.35,1.35), rng.uniform(-0.15,0.75),0])
        self.add(mortar, pestle, cells, grains, schematic())
        self.play(Rotate(pestle, angle=0.55, about_point=[0,-0.15,0], rate_func=there_and_back),
                  cells.animate.shift(RIGHT * 0.35), grains.animate.shift(LEFT * 0.3), run_time=1.5)
        self.at("pressed out a juice")
        press = VGroup(Rectangle(width=3.4, height=0.32, color=GREY, fill_color=GREY, fill_opacity=0.5),
                       Line([0,2.9,0],[0,1.1,0], color=GREY, stroke_width=12)).move_to([-3.95,0.65,0])
        flask = lab_flask(center=(3.85,-0.75,0), scale=0.88, liquid=GOLD)
        stream = CubicBezier([-2.4,0.2,0], [-1.0,-0.4,0], [1.8,0.3,0], [3.55,-0.3,0],
                             color=GOLD, stroke_width=10)
        press.shift(UP * 1.0)
        self.play(FadeOut(VGroup(pestle,cells,grains)), FadeIn(press), FadeIn(flask), Create(stream), run_time=1.2)
        self.play(press.animate.shift(DOWN * 1.0), mortar.animate.scale(0.94), run_time=1.0)
        self.at("added sugar")
        sugar = chip("SUGAR", GREEN, 28).move_to([3.85,1.8,0])
        self.play(FadeIn(sugar), sugar.animate.move_to([3.85,-0.35,0]).scale(0.7), run_time=1.0)
        self.play(press.animate.shift(DOWN * 0.45), mortar.animate.scale(0.96),
                  run_time=0.9, rate_func=there_and_back)
        self.at("bubbles rose")
        bubbles = RisingBubbles(cx=3.85, y0=-1.75, y1=1.25, width=1.2, n=10, seed=22)
        scraps = tiny_scraps()
        self.play(FadeIn(bubbles), FadeIn(scraps), FadeOut(stream), FadeOut(sugar), run_time=0.8)
        self.play(flask.animate.scale(1.055), scraps.animate.shift(UP * 0.16),
                  run_time=1.2, rate_func=there_and_back)
        self.at("living scraps survived")
        circle = Ellipse(width=1.25, height=1.15, color=RED, stroke_width=5).move_to([4.22,1.02,0])
        q = T("?", 52, GOLD, font=TITLE_FONT, weight=BOLD).move_to([5.25,1.55,0])
        self.play(Create(circle), FadeIn(q, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


class S10Predict(LabSpokenScene):
    def construct(self):
        flask = lab_flask(center=(0,-0.35,0), scale=0.82, liquid=GOLD)
        bubbles = RisingBubbles(cx=0, y0=-1.25, y1=1.35, width=1.0, n=8, seed=31, speed=0.14)
        scraps = VGroup(*[Ellipse(width=0.20, height=0.11, color=GREEN, fill_color=GREEN,
                                  fill_opacity=0.7) for _ in range(2)])
        scraps[0].move_to([-0.25,0.85,0]); scraps[1].move_to([0.3,1.08,0])
        question = T("WHAT DISTINGUISHES CELLS FROM A CHEMICAL?", 31, TEXT, weight=BOLD).move_to([0,3.2,0])
        self.add(flask, bubbles, scraps, schematic())
        self.play(Write(question), run_time=0.8)
        self.play(VGroup(flask, scraps).animate.scale(1.06), run_time=1.0, rate_func=there_and_back)
        self.play(Circumscribe(question, color=TEAL, stroke_width=7), run_time=1.0)
        cards = [test_card("WARM", (-4.65,0.8,0), 3.2),
                 test_card("FILTER", (-3.5,-2.1,0), 3.2),
                 test_card("ANTISEPTIC", (3.5,-2.1,0), 3.5)]
        self.at("warming")
        self.play(FadeIn(cards[0], shift=RIGHT * 0.2), run_time=0.65)
        self.at("cell trapping filter")
        self.play(FadeIn(cards[1], shift=UP * 0.2), run_time=0.65)
        self.at("an antiseptic")
        self.play(FadeIn(cards[2], shift=UP * 0.2), run_time=0.65)
        self.play(scraps.animate.shift(UP * 0.15), run_time=1.2, rate_func=there_and_back)
        self.finish()


class S11PredictHold(Scene):
    def construct(self):
        flask = lab_flask(center=(0,-0.35,0), scale=0.82, liquid=GOLD)
        bubbles = RisingBubbles(cx=0, y0=-1.25, y1=1.35, width=1.0, n=8, seed=31, speed=0.14)
        scraps = VGroup(*[Ellipse(width=0.20, height=0.11, color=GREEN, fill_color=GREEN,
                                  fill_opacity=0.7) for _ in range(2)])
        scraps[0].move_to([-0.25,0.85,0]); scraps[1].move_to([0.3,1.08,0])
        question = T("WHAT DISTINGUISHES CELLS FROM A CHEMICAL?", 31, TEXT, weight=BOLD).move_to([0,3.2,0])
        cards = [test_card("WARM", (-4.65,0.8,0), 3.2),
                 test_card("FILTER", (-3.5,-2.1,0), 3.2),
                 test_card("ANTISEPTIC", (3.5,-2.1,0), 3.5)]
        self.add(lab_backdrop(), flask, bubbles, scraps, question, *cards, schematic())
        for card in cards:
            self.play(ShowPassingFlash(card[0].copy().set_stroke(TEAL, 8), time_width=0.7), run_time=1.25)
        self.wait(0.75)


class S12Controls(LabSpokenScene):
    def construct(self):
        title = T("THREE CONTROLS", 34, TEXT, weight=BOLD).move_to([0,3.2,0])
        cards = [test_card("WARM", (-4.45,0.65,0), 3.6),
                 test_card("FILTER", (0,0.65,0), 3.6),
                 test_card("ANTISEPTIC", (4.45,0.65,0), 3.75)]
        self.add(title, *cards, schematic())
        self.at("warming stopped")
        self.play(cards[0][2][0].animate.set_fill(RED, opacity=0.35),
                  cards[0][2][1].animate.set_fill(RED, opacity=0.35),
                  cards[0][3][0].animate.set_color(RED),
                  cards[0][3][1].animate.set_color(RED), run_time=0.8)
        self.at("could stop either")
        self.play(cards[0].animate.shift(UP * 0.16), run_time=0.8, rate_func=there_and_back)
        self.at("could not decide")
        undecided = T("CANNOT DECIDE", 28, RED, weight=BOLD).move_to([-4.45,-0.85,0])
        self.play(FadeIn(undecided, shift=UP * 0.1), run_time=0.7)
        self.play(cards[0].animate.scale(1.045), run_time=0.9, rate_func=there_and_back)
        self.at("filtered juice")
        mesh = VGroup(*[Line([-0.65+i*0.22,-1.45,0],[-0.65+i*0.22,-0.75,0], color=TEAL, stroke_width=2)
                        for i in range(7)])
        caught = Circle(radius=0.22, color=GREEN, fill_color=GREEN,
                        fill_opacity=0.25).move_to([-0.5,-1.03,0])
        pass_arrow = Arrow([0.55,-0.78,0],[0.55,-1.75,0], color=GOLD, buff=0, stroke_width=5)
        mini_bubbles = RisingBubbles(cx=0.55, y0=-2.75, y1=-1.78, width=0.6, n=6, seed=40)
        self.play(cards[1][0].animate.set_fill(TEAL, opacity=0.22), FadeIn(mesh), FadeIn(caught),
                  GrowArrow(pass_arrow), FadeIn(mini_bubbles), run_time=1.1)
        self.play(cards[1].animate.shift(UP * 0.22), run_time=0.9, rate_func=there_and_back)
        self.at("treated with chloroform")
        drops = VGroup(*[Dot(radius=0.11, color=YELLOW) for _ in range(3)])
        for d, x in zip(drops, [4.15,4.45,4.75]): d.move_to([x,-0.85,0])
        scraps = VGroup(*[Ellipse(width=0.18,height=0.1,color=GREEN) for _ in range(2)])
        scraps[0].move_to([4.25,-1.35,0]); scraps[1].move_to([4.7,-1.25,0])
        cross = Cross(stroke_color=RED, stroke_width=5).scale(0.28).move_to([4.47,-1.3,0])
        right_bubbles = RisingBubbles(cx=4.45, y0=-2.75, y1=-1.65, width=0.7, n=6, seed=41)
        self.play(FadeIn(drops, shift=DOWN*0.2), FadeIn(scraps), run_time=0.7)
        self.play(cards[2][0].animate.set_fill(TEAL, opacity=0.22), Create(cross),
                  FadeIn(right_bubbles), run_time=1.0)
        self.play(cards[2].animate.scale(1.045), run_time=0.9, rate_func=there_and_back)
        self.at("together those controls")
        bracket = Brace(VGroup(cards[1],cards[2]), DOWN, color=TEAL)
        verdict = T("NO LIVING CELLS", 30, TEAL, weight=BOLD).next_to(bracket, DOWN, buff=0.12)
        apparatus = VGroup(undecided, mesh, caught, pass_arrow, mini_bubbles,
                           drops, scraps, cross, right_bubbles)
        self.play(FadeOut(apparatus), GrowFromCenter(bracket),
                  FadeIn(verdict, shift=UP*0.1), run_time=0.9)
        self.play(ShowPassingFlash(Line([-1.7,-2.75,0],[6.0,-2.75,0], color=TEAL, stroke_width=8), time_width=0.7), run_time=1.4)
        self.finish()


class S13Result(LabSpokenScene):
    def construct(self):
        r = ruler(2).scale(0.82).shift(LEFT * 0.65)
        wall = life_wall(3.5).move_to([5.15,0.85,0])
        flask = lab_flask(center=(5.55,-2.0,0), scale=0.48)
        cell_trace = Circle(radius=0.18, color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.15)
        cell_trace.move_to(r[1][2].get_top() + UP * 0.42)
        spark = Star(n=4, outer_radius=0.16, inner_radius=0.06, color=GOLD,
                     fill_color=GOLD, fill_opacity=1).move_to(cell_trace.get_center() + RIGHT * 0.65)
        self.add(r, wall, flask, cell_trace, spark, schematic())
        self.at("removed the cell")
        cross = Cross(stroke_color=RED, stroke_width=6).scale(0.25).move_to(cell_trace)
        self.play(Create(cross), run_time=0.7)
        self.play(r[1][2].animate.shift(UP * 0.32), run_time=1.0, rate_func=there_and_back)
        self.play(VGroup(r, wall, flask, cell_trace, spark, cross).animate.shift(LEFT * 0.14),
                  run_time=1.0, rate_func=there_and_back)
        self.at("final segment")
        target = ruler(3).scale(0.82).shift(LEFT * 0.65)
        self.play(Transform(r, target), FadeOut(cross), FadeOut(cell_trace), run_time=1.0)
        self.play(r[1][2].animate.shift(UP * 0.16), run_time=0.8, rate_func=there_and_back)
        self.at("across 70 years")
        sweep = Line(r[1].get_left(), r[1].get_right(), color=TEAL, stroke_width=10)
        self.play(Create(sweep), run_time=1.1)
        for part in r[1]:
            path = Line(part.get_top(), wall.get_center(), color=TEAL)
            pulse = Dot(radius=0.10, color=TEAL).move_to(path.get_start())
            self.add(pulse)
            self.play(MoveAlongPath(pulse,path), run_time=0.7)
            self.remove(pulse)
        self.at("became unnecessary")
        bubbles = RisingBubbles(cx=5.55, y0=-2.4, y1=1.45, width=0.7, n=8, seed=51)
        self.play(FadeOut(wall, scale=1.2), FadeOut(spark), run_time=0.5)
        self.play(FadeIn(bubbles), run_time=0.5)
        self.finish()


class S14Course(LabSpokenScene):
    def construct(self):
        platform = RoundedRectangle(width=11.7, height=1.25, corner_radius=0.18, color=TEAL,
                                    stroke_width=4, fill_color=TEAL, fill_opacity=0.12).move_to([0,-2.15,0])
        label = T("ORDINARY CHEMISTRY", 32, TEAL, weight=BOLD).move_to(platform)
        rock = chip("ROCK", BLUE, 28).move_to([-4.9,-0.75,0])
        salt = chip("SALT", BLUE, 28).move_to([-2.85,-0.75,0])
        cell = yeast_cell(scale=0.45, center=(-0.4,-0.45,0))
        cell[2].set_opacity(0)
        cell_lab = T("YEAST", 28, GREEN, weight=BOLD).move_to([-0.4, 0.85, 0])
        flask = lab_flask(center=(3.8,-0.25,0), scale=0.62, liquid=GOLD)
        bubbles = RisingBubbles(cx=3.8, y0=-1.05, y1=1.15, width=0.8, n=8, seed=61)
        self.add(platform, label, rock, salt, cell, cell_lab, flask, bubbles)
        self.play(Indicate(platform, color=TEAL, scale_factor=1.015), run_time=0.9)
        self.play(rock.animate(rate_func=there_and_back).shift(UP * 0.1),
                  salt.animate(rate_func=there_and_back).shift(UP * 0.1),
                  cell.animate(rate_func=there_and_back).shift(UP * 0.1),
                  flask.animate(rate_func=there_and_back).shift(UP * 0.1), run_time=1.3)
        self.at("reactions can be isolated")
        self.play(flask.animate.shift(UP*0.55), bubbles.animate.shift(UP*0.55), run_time=0.8)
        self.at("measured")
        counter_box = RoundedRectangle(width=2.1,height=1.2,corner_radius=0.12,color=YELLOW,
                                       fill_color=YELLOW,fill_opacity=0.08).move_to([5.25,2.25,0])
        counter = M("8 bubbles", 28, YELLOW).move_to(counter_box)
        link = Arrow([4.45,1.2,0], counter_box.get_bottom() + LEFT * 0.3,
                     color=YELLOW,buff=0.1,stroke_width=4)
        self.play(GrowArrow(link), FadeIn(counter_box), FadeIn(counter), run_time=0.8)
        self.at("explained")
        elbow = Line(counter_box.get_left(), [2.35, 2.25, 0], color=TEAL, stroke_width=5)
        back = Arrow([2.35, 2.25, 0], platform.get_top()+RIGHT*1.4,
                     color=TEAL, buff=0.12, stroke_width=5)
        self.play(Create(elbow), GrowArrow(back),
                  ShowPassingFlash(platform.copy().set_stroke(TEAL,10), time_width=0.7), run_time=1.1)
        self.at("requires proving life")
        rule = T("REMOVE LIFE  →  PROVE IT IS GONE", 32, TEXT, weight=BOLD).move_to([0,3.15,0])
        self.play(FadeIn(rule, shift=DOWN*0.12), run_time=0.8)
        self.play(bubbles.animate.shift(UP*0.08), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S15End(EndCard):
    LINE = "Testing a claim that chemistry needs life requires proving life is gone."

    def construct(self):
        self.add(lab_backdrop())
        b = bench().set_opacity(0.3)
        flask = lab_flask(center=(5.25,-0.95,0), scale=0.52, liquid=GOLD).set_opacity(0.65)
        bubbles = RisingBubbles(cx=5.25, y0=-1.75, y1=0.55, width=0.65, n=8, seed=71)
        hexm = hex_mascot(1.55).move_to([-5.25,-0.85,0])
        line = T("TESTING A CLAIM THAT CHEMISTRY NEEDS LIFE\nREQUIRES PROVING LIFE IS GONE.",
                 32, TEXT, font=TITLE_FONT, weight=BOLD, line_spacing=0.9)
        fit(line, 8.0, 1.6); line.move_to([0,0.75,0])
        rule = Line([-2.3,-0.55,0],[2.3,-0.55,0],color=GOLD,stroke_width=4)
        self.add(b, flask, bubbles)
        self.play(FadeIn(hexm,shift=UP*0.15),FadeIn(line,shift=UP*0.12),GrowFromCenter(rule),run_time=0.9)
        shoulder = hexm.arm.get_start()
        for _ in range(2):
            self.play(Rotate(hexm.arm,angle=-0.5,about_point=shoulder),rate_func=there_and_back,run_time=0.35)
        self.finish()
