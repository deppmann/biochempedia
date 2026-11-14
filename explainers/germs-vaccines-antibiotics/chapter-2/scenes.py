"""The Few That Survive — chapter 2 of Germs, Vaccines and Antibiotics.

COLOR MAP (shared with chapter 1)
  TEAL     sensitive bacteria / the microbe curve
  GOLD     an attack on microbes: immune defense or antibiotic hit
  ORANGE   resistant bacteria
  PINK     a person's cell
  PURPLE   viruses
  INK      labels and outlines on the warm paper ground

All population pictures are schematic.  The dish, its cell locations, and the day
counter are rebuilt by field_world(), at the same scale and position in every scene.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


PAPER = "#F6E9D3"
INK = "#292522"
PALE = "#E9B7B7"
PURPLE = "#7656A8"
ORANGE_RESIST = "#E87D32"
SOFT = "#B7A996"


def paper():
    """Warm chapter background, behind every hand-drawn scene."""
    r = Rectangle(width=14.3, height=8.1, stroke_width=0, fill_color=PAPER, fill_opacity=1)
    r.set_z_index(-100)
    r.layout_ok = True
    return r


def label(text, size=30, color=INK, **kwargs):
    return T(text, size=size, color=color, **kwargs)


def drug_mark(at, scale=1.0):
    """A gold impact mark, not a molecule."""
    a = Line(UL * 0.22, DR * 0.22, color=GOLD, stroke_width=8)
    b = Line(DL * 0.22, UR * 0.22, color=GOLD, stroke_width=8)
    return VGroup(a, b).scale(scale).move_to(at)


def sensitive(at, radius=0.34, outline=False):
    c = Circle(radius=radius, stroke_color=TEAL, stroke_width=3,
               fill_color=TEAL, fill_opacity=0 if outline else 0.88).move_to(at)
    if outline:
        c.set_stroke(opacity=0.35)
    return c


def resistant(at, size=0.62):
    return RoundedRectangle(corner_radius=0.11, width=size, height=size,
                            stroke_color=ORANGE_RESIST, stroke_width=3,
                            fill_color=ORANGE_RESIST, fill_opacity=0.92).move_to(at)


def keep_alive(mobs, amp=.12):
    """Continuous, gentle cell drift during narration (never used in the predict pause)."""
    for i, mob in enumerate(mobs):
        bob(mob, amp=amp, speed=4.0 + .18 * (i % 5), seed=i)
    return mobs


def breathe(mob, amp=.018, speed=3.2):
    """A large subject gently changes size so a spoken hold stays visually alive."""
    mob._breath_t = 0.0
    base_h = mob.height

    def update(m, dt):
        m._breath_t += dt
        m.set_height(base_h * (1 + amp * np.sin(speed * m._breath_t)))
    return mob.add_updater(update)


FIELD_POS = [
    (-4.8, 1.7), (-3.6, 1.8), (-2.4, 1.65), (-1.2, 1.8), (0.0, 1.65), (1.2, 1.8), (2.4, 1.65), (3.6, 1.8), (4.8, 1.7),
    (-5.1, 0.55), (-3.9, 0.45), (-2.7, 0.60), (-1.35, 0.42), (0.0, 0.58), (1.35, 0.42), (2.7, 0.60), (3.9, 0.45), (5.1, 0.55),
    (-4.7, -0.65), (-3.45, -0.78), (-2.15, -0.62), (-0.8, -0.80), (0.8, -0.80), (2.15, -0.62), (3.45, -0.78), (4.7, -0.65),
]
RES_IDX = (4, 12, 16, 21)


def day_box(day="0"):
    box = RoundedRectangle(corner_radius=0.14, width=2.1, height=0.82,
                           stroke_color=INK, stroke_width=3, fill_color=PAPER, fill_opacity=1)
    txt = M(f"DAY  {day}", size=30, color=INK).move_to(box)
    return VGroup(box, txt).move_to([5.25, 3.22, 0])


def field_world(state="mixed", day="0", dead=False, full_count=26):
    """The one carried population world used from s04 through s09."""
    dish = RoundedRectangle(corner_radius=1.0, width=11.6, height=3.75,
                            stroke_color=INK, stroke_width=4,
                            fill_color="#AFCFC8", fill_opacity=0.95).move_to([0, 0.48, 0])
    cells = VGroup()
    ghosts = VGroup()
    if dead:
        for i, p in enumerate(FIELD_POS):
            if i not in RES_IDX:
                ghosts.add(sensitive([*p, 0], outline=True))
    if state == "mixed":
        for i, p in enumerate(FIELD_POS[:full_count]):
            cells.add(resistant([*p, 0]) if i in RES_IDX else sensitive([*p, 0]))
    elif state == "survivors":
        for i in RES_IDX:
            cells.add(resistant([*FIELD_POS[i], 0]))
    elif state == "resistant":
        for p in FIELD_POS[:full_count]:
            cells.add(resistant([*p, 0]))
    g = VGroup(dish, ghosts, cells, day_box(day))
    g.dish, g.ghosts, g.cells, g.day = dish, ghosts, cells, g[-1]
    return g


def field_key():
    s = sensitive([-1.7, -2.23, 0], radius=0.18)
    sl = label("sensitive", 28, TEAL).next_to(s, RIGHT, buff=0.15)
    r = resistant([1.35, -2.23, 0], size=0.38)
    rl = label("resistant", 28, ORANGE_RESIST).next_to(r, RIGHT, buff=0.15)
    return VGroup(s, sl, r, rl)


def bacteria_picture():
    wall = RoundedRectangle(corner_radius=1.0, width=6.0, height=3.35,
                            stroke_color=TEAL, stroke_width=12,
                            fill_color=TEAL, fill_opacity=0.13).move_to([-2.6, 0.15, 0])
    inside = RoundedRectangle(corner_radius=0.78, width=5.35, height=2.7,
                              stroke_color=INK, stroke_width=2).move_to(wall)
    pts = [(-4.4, .65), (-3.55, -.45), (-2.7, .72), (-1.75, -.35), (-.95, .45), (-3.9, -.9), (-2.55, -.65), (-1.45, .85)]
    ribs = VGroup(*[Dot([x, y, 0], radius=0.11, color=INK) for x, y in pts])
    g = VGroup(wall, inside, ribs)
    g.wall, g.ribs = wall, ribs
    return g


def host_picture():
    cell = RoundedRectangle(corner_radius=1.15, width=7.3, height=4.65,
                            stroke_color=PALE, stroke_width=9,
                            fill_color=PALE, fill_opacity=0.35).move_to([1.2, 0.1, 0])
    rib_pos = [(-1.35, .55), (-.5, -.75), (.45, .85), (1.2, -.25), (2.1, .55), (3.0, -.65), (3.8, .3)]
    ribs = VGroup(*[Dot([x, y, 0], radius=.12, color=INK) for x, y in rib_pos])
    viruses = VGroup(*[RegularPolygon(6, radius=.22, color=PURPLE, fill_color=PURPLE, fill_opacity=.9,
                                      stroke_width=2).move_to(p) for p in [(-.7, .15, 0), (.4, -.2, 0), (1.65, .42, 0)]])
    g = VGroup(cell, ribs, viruses)
    g.cell, g.ribs, g.viruses = cell, ribs, viruses
    return g


def mini_race():
    axes = VGroup(Line([-1.7, -1.05, 0], [1.55, -1.05, 0], color=INK, stroke_width=3),
                  Line([-1.7, -1.05, 0], [-1.7, 1.35, 0], color=INK, stroke_width=3))
    curve = VMobject(stroke_color=TEAL, stroke_width=7)
    curve.set_points_smoothly([[-1.55, -.9, 0], [-.9, -.55, 0], [-.2, .45, 0], [.5, 1.05, 0], [1.3, .35, 0]])
    defense = Rectangle(width=.42, height=1.9, stroke_color=GOLD, stroke_width=3,
                        fill_color=GOLD, fill_opacity=.72).move_to([1.95, -.1, 0])
    return VGroup(axes, curve, defense)


class S00Title(TitleCard):
    LESSON = "Germs, Vaccines and Antibiotics"
    TITLE = "The Few That Survive"

    def construct(self):
        bg = paper()
        brand = label("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD)
        lesson = label(self.LESSON.upper(), 24, INK)
        title = label(self.TITLE, 56, INK, font=TITLE_FONT)
        rule = Line(LEFT * 1.5, RIGHT * 1.5, color=GOLD, stroke_width=6)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=.32)
        self.add(bg)
        self.play(FadeIn(brand), FadeIn(lesson), run_time=.55)
        self.play(Write(title), GrowFromCenter(rule), run_time=1.15)
        self.wait(.7)
        self.play(FadeOut(g), run_time=.55)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        self.add(paper())
        race = mini_race().scale(.72).move_to([-4.55, 1.55, 0])
        race_box = RoundedRectangle(corner_radius=.18, width=4.3, height=2.65, color=SOFT, stroke_width=3).move_to(race)
        self.play(Create(race_box), Create(race), run_time=1.0)
        breathe(VGroup(race_box, race), .022, 3.5)
        self.at("but an antibiotic")
        bottle = VGroup(RoundedRectangle(corner_radius=.22, width=2.1, height=2.55, stroke_color=GOLD,
                                         stroke_width=5, fill_color=GOLD, fill_opacity=.16),
                        label("antibiotic", 28, GOLD)).move_to([0, .75, 0])
        crowd = VGroup(*[sensitive([3.0 + (i % 3) * .8, 1.45 - (i // 3) * .75, 0], .23) for i in range(9)])
        race.clear_updaters(recursive=True)
        race_box.clear_updaters(recursive=True)
        self.play(race.animate.scale(.58).move_to([-5.0, 2.35, 0]),
                  race_box.animate.scale(.58).move_to([-5.0, 2.35, 0]),
                  FadeIn(bottle, shift=LEFT), FadeIn(crowd), run_time=1.3)
        keep_alive(crowd, .10)
        breathe(bottle, .025, 3.8)
        self.at("kills almost every")
        marks = VGroup(*[drug_mark(c.get_center(), .75) for c in crowd[:-2]])
        self.play(LaggedStart(*[FadeIn(m, scale=.4) for m in marks], lag_ratio=.07), run_time=.8)
        self.play(LaggedStart(*[FadeOut(c, scale=.2) for c in crowd[:-2]], lag_ratio=.05),
                  FadeOut(marks), run_time=1.0)
        self.at("how can the infection")
        q = label("How can it come back?", 44, INK, font=TITLE_FONT).move_to([1.4, -1.65, 0])
        self.play(Write(q), run_time=.85)
        self.at("what the drug needs")
        target = label("What does the drug hit?", 32, GOLD).move_to([1.4, -2.65, 0])
        self.play(FadeIn(target, shift=UP*.12), Indicate(bottle, color=GOLD), run_time=.8)
        self.finish()


class S02Target(SpokenScene):
    def construct(self):
        self.add(paper())
        bact = bacteria_picture()
        self.play(FadeIn(bact, scale=.88), run_time=.9)
        breathe(bact, .018, 3.4)
        self.at("kills bacteria")
        name = label("bacterium", 34, TEAL).move_to([-2.6, 2.45, 0])
        self.play(FadeIn(name), bact.animate.shift(UP*.06), run_time=.6)
        self.at("something to hit")
        hit = drug_mark([1.0, 1.95, 0], 1.25)
        self.play(FadeIn(hit, scale=.3), run_time=.55)
        self.at("block the building")
        wall_l = label("cell wall", 30, TEAL).move_to([3.8, 1.35, 0])
        arrow1 = Arrow(wall_l.get_left(), bact.wall.get_right()+UP*.7, buff=.15, color=INK, stroke_width=4)
        block = label("wall building blocked", 30, GOLD).move_to([3.7, .55, 0])
        self.play(FadeIn(wall_l), GrowArrow(arrow1), hit.animate.move_to(bact.wall.get_right()+UP*.7), run_time=.85)
        self.play(FadeIn(block), run_time=.45)
        self.at("Others jam")
        hit2 = drug_mark(bact.ribs[3].get_center(), 1.0)
        ribs_l = label("ribosomes", 30, INK).move_to([3.8, -.55, 0])
        arrow2 = Arrow(ribs_l.get_left(), bact.ribs[3].get_center(), buff=.15, color=INK, stroke_width=4)
        self.play(FadeIn(hit2, scale=.3), FadeIn(ribs_l), GrowArrow(arrow2), run_time=.8)
        self.at("cannot make proteins")
        jam = label("ribosomes jammed", 30, GOLD).move_to([3.8, -1.42, 0])
        stopped = label("growth stops", 34, INK, weight=BOLD).move_to([-2.6, -2.25, 0])
        self.play(FadeIn(jam), bact.animate.set_opacity(.35), FadeIn(stopped), run_time=.9)
        self.finish()


class S03Virus(SpokenScene):
    def construct(self):
        self.add(paper())
        host = host_picture()
        self.play(FadeIn(host.cell, scale=.9), run_time=.75)
        breathe(host.cell, .02, 3.5)
        self.at("look at a virus")
        self.play(FadeIn(host.viruses, scale=.3), run_time=.65)
        keep_alive(host.viruses, .08)
        vl = label("virus", 32, PURPLE).move_to([-2.5, 2.6, 0])
        self.play(FadeIn(vl), run_time=.4)
        self.at("no cell wall")
        no_parts = label("no cell wall • no ribosomes of its own", 30, INK).move_to([0, -2.65, 0])
        self.play(FadeIn(no_parts, shift=UP*.1), run_time=.65)
        self.at("inside one of your cells")
        your = label("YOUR CELL", 32, PALE, weight=BOLD).move_to([1.2, 2.72, 0])
        self.play(FadeIn(your), host.viruses.animate.shift(RIGHT*.35), run_time=.75)
        self.at("uses that cell's ribosomes")
        self.play(FadeIn(host.ribs), run_time=.7)
        rib_l = label("your cell's ribosomes", 28, INK).move_to([1.2, -1.5, 0])
        self.play(FadeIn(rib_l), Indicate(host.ribs, color=INK), run_time=.7)
        self.at("no bacterial part")
        marks = VGroup(*[drug_mark([-4.8 + i*.75, .6-i*.2, 0], .8) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=.12), run_time=.65)
        self.play(marks.animate.shift(RIGHT*10).set_opacity(0), run_time=1.15)
        self.at("do not treat colds")
        tag = chip("colds, flu: no bacterial target", GOLD, size=30, fill_opacity=.08).move_to([0, -2.65, 0])
        self.play(FadeOut(no_parts), FadeIn(tag), run_time=.7)
        self.finish()


class S04Field(SpokenScene):
    def construct(self):
        self.add(paper())
        world = field_world("mixed", "0")
        self.play(Create(world.dish), FadeIn(world.day), run_time=.75)
        self.at("large population")
        self.play(LaggedStart(*[FadeIn(c, scale=.3) for c in world.cells], lag_ratio=.025), run_time=1.2)
        keep_alive(world.cells)
        self.at("Most are sensitive")
        key = field_key()
        self.play(FadeIn(key[:2]), run_time=.55)
        self.at("few may already")
        res_cells = VGroup(*[world.cells[i] for i in RES_IDX])
        self.play(FadeIn(key[2:]), Indicate(res_cells, color=ORANGE_RESIST, scale_factor=1.55), run_time=.9)
        self.at("lets them survive")
        gene = chip("survival gene — already there", ORANGE_RESIST, size=28, fill_opacity=.08).move_to([0, -2.9, 0])
        self.play(FadeOut(key), FadeIn(gene), run_time=.7)
        self.at("These are resistant")
        self.play(Indicate(res_cells, color=ORANGE_RESIST, scale_factor=1.45), run_time=.7)
        self.finish()


class S05Drug(SpokenScene):
    def construct(self):
        self.add(paper())
        world = field_world("mixed", "0")
        key = field_key()
        self.add(world, key, scope_tag("schematic: a drug that kills", color=INK))
        keep_alive(world.cells)
        self.at("ability of some bacteria")
        res_cells = VGroup(*[world.cells[i] for i in RES_IDX])
        self.play(Indicate(res_cells, color=ORANGE_RESIST, scale_factor=1.45), run_time=.8)
        self.at("Start the drug")
        sweep1 = VGroup(*[drug_mark([-5.0+i*1.0, 1.75, 0], .72) for i in range(11)])
        self.play(LaggedStart(*[FadeIn(m, scale=.3) for m in sweep1], lag_ratio=.04), run_time=.8)
        self.play(Transform(world.day, day_box("1")), run_time=.35)
        self.at("kills the sensitive")
        sensitive_cells = VGroup(*[c for i, c in enumerate(world.cells) if i not in RES_IDX])
        first = VGroup(*list(sensitive_cells)[:8])
        self.play(LaggedStart(*[FadeOut(c, scale=.15) for c in first], lag_ratio=.06), FadeOut(sweep1), run_time=1.0)
        self.at("Round after round")
        remaining = VGroup(*list(sensitive_cells)[8:])
        sweep2 = VGroup(*[drug_mark([-5.0+i*1.0, .15, 0], .72) for i in range(11)])
        self.play(LaggedStart(*[FadeIn(m, scale=.3) for m in sweep2], lag_ratio=.04),
                  Transform(world.day, day_box("2")), run_time=.8)
        self.play(LaggedStart(*[FadeOut(c, scale=.15) for c in remaining], lag_ratio=.045), run_time=1.0)
        self.at("orange ones survive")
        hits = VGroup(*[drug_mark(c.get_center(), .7) for c in res_cells])
        self.play(FadeIn(hits), FadeOut(sweep2), run_time=.5)
        self.play(FadeOut(hits), res_cells.animate.shift(UP*.05), run_time=.65)
        self.at("resist the drug")
        tag = chip("resists the drug", ORANGE_RESIST, size=28, fill_opacity=.08).move_to([0, -2.55, 0])
        self.play(FadeOut(key), FadeIn(tag), Transform(world.day, day_box("3")), run_time=.7)
        self.finish()


def survivor_backdrop(day="3"):
    return VGroup(paper(), field_world("survivors", day, dead=True))


class S06Predict(SpokenScene):
    QUESTION = "When it grows back, what will it be made of?"

    def construct(self):
        back = survivor_backdrop()
        self.add(back)
        keep_alive(back[1].cells, .16)
        breathe(back[1].dish, .012, 3.4)
        self.at("every teal cell is gone")
        self.play(Indicate(back[1].ghosts, color=TEAL, scale_factor=1.02), run_time=.7)
        self.at("few orange cells remain")
        self.play(Indicate(back[1].cells, color=ORANGE_RESIST, scale_factor=1.5), run_time=.8)
        self.at("empty space around")
        self.play(back[1].cells.animate.shift(UP*.06), run_time=.65)
        self.at("population grows back")
        q = question_card(self.QUESTION, color=ORANGE_RESIST, size=32, y=-3.05)
        self.play(FadeIn(q.question, shift=UP*.1), run_time=.75)
        self.at("what will it be made")
        self.play(Indicate(q.question, color=ORANGE_RESIST, scale_factor=1.05), run_time=.65)
        self.play(q.question.animate.scale(1.025), run_time=.8)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "When it grows back, what will it be made of?"
    CARD = {"color": ORANGE_RESIST, "size": 32, "y": -3.05}
    RING_AT = (6.0, -3.05, 0)
    SECONDS = 5.0

    def backdrop(self):
        return survivor_backdrop()


class S08Reveal(SpokenScene):
    def construct(self):
        self.add(paper())
        world = field_world("survivors", "3", dead=True)
        self.add(world, scope_tag("schematic", color=INK))
        keep_alive(world.cells)
        breathe(world.dish, .01, 3.2)
        self.at("Resistant cells")
        answer = label("RESISTANT CELLS", 42, ORANGE_RESIST, weight=BOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(answer, scale=.85), Indicate(world.cells, color=ORANGE_RESIST, scale_factor=1.5), run_time=.85)
        self.at("competition gone")
        self.play(FadeOut(world.ghosts), Transform(world.day, day_box("4")), run_time=.75)
        targets = [i for i in range(len(FIELD_POS)) if i not in RES_IDX]
        stage1 = targets[:8]
        born1 = VGroup()
        for j, i in enumerate(stage1):
            src = world.cells[j % len(world.cells)].get_center()
            born1.add(resistant(src).scale(.78))
        self.at("orange cells divide")
        self.add(born1)
        self.play(*[c.animate.scale(1/.78).move_to([*FIELD_POS[i], 0]) for c, i in zip(born1, stage1)],
                  Transform(world.day, day_box("5")), run_time=1.25)
        keep_alive(born1)
        rest = targets[8:]
        born2 = VGroup()
        sources = list(world.cells) + list(born1)
        for j, i in enumerate(rest):
            born2.add(resistant(sources[j % len(sources)].get_center()).scale(.78))
        self.at("fill the space")
        self.add(born2)
        self.play(*[c.animate.scale(1/.78).move_to([*FIELD_POS[i], 0]) for c, i in zip(born2, rest)],
                  Transform(world.day, day_box("7")), run_time=1.45)
        keep_alive(born2)
        self.at("did not create them")
        no_create = label("drug did not create resistance", 30, INK).move_to([0, -2.35, 0])
        self.play(FadeIn(no_create), run_time=.65)
        self.at("there before the drug")
        tag = chip("there before the drug", ORANGE_RESIST, size=28, fill_opacity=.08).move_to([0, -2.85, 0])
        self.play(FadeOut(no_create), FadeIn(tag), Indicate(world.cells[0], color=ORANGE_RESIST), run_time=.75)
        self.at("removed their competition")
        self.play(Circumscribe(VGroup(world.cells, born1, born2), color=ORANGE_RESIST, fade_out=True), run_time=.85)
        self.finish()


class S09Selection(SpokenScene):
    def construct(self):
        self.add(paper())
        world = field_world("resistant", "7")
        self.add(world, scope_tag("schematic", color=INK))
        keep_alive(world.cells)
        self.at("natural selection")
        banner = chip("NATURAL SELECTION", ORANGE_RESIST, size=34, fill_opacity=.08).move_to([0, 3.15, 0])
        self.play(FadeIn(banner, shift=DOWN*.1), run_time=.7)
        self.at("helpful trait survive")
        trait = label("resistance → more survivors", 32, ORANGE_RESIST).move_to([0, -2.35, 0])
        self.play(FadeIn(trait), world.cells.animate.shift(UP*.05), run_time=.75)
        self.at("drug did the selecting")
        marks = VGroup(*[drug_mark([-4+i*1.0, .45, 0], .65) for i in range(9)])
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=.04), run_time=.65)
        self.play(FadeOut(marks), run_time=.4)
        self.at("did not choose")
        choice = label("no choice — just survivors", 30, INK).move_to([0, -2.85, 0])
        self.play(FadeIn(choice), run_time=.55)
        self.at("person did not become")
        person = VGroup(Circle(.38, color=INK, stroke_width=4).move_to([-4.8, -.2, 0]),
                        Line([-4.8, -.6, 0], [-4.8, -1.7, 0], color=INK, stroke_width=5),
                        Line([-4.8, -.9, 0], [-5.35, -1.35, 0], color=INK, stroke_width=5),
                        Line([-4.8, -.9, 0], [-4.25, -1.35, 0], color=INK, stroke_width=5))
        not_r = label("person: not resistant", 28, INK).move_to([-4.75, -2.2, 0])
        self.play(FadeOut(trait), FadeOut(choice), FadeIn(person), FadeIn(not_r), run_time=.75)
        self.at("The bacteria did", nth=1)
        yes = label("BACTERIA ✓", 34, ORANGE_RESIST, weight=BOLD).move_to([2.5, -2.35, 0])
        self.play(FadeIn(yes), Indicate(world.cells, color=ORANGE_RESIST), run_time=.75)
        self.finish()


class S10Transfer(SpokenScene):
    def construct(self):
        self.add(paper())
        donor = resistant([-3.4, .35, 0], size=1.25)
        neighbor = sensitive([0, .35, 0], radius=.62)
        far = sensitive([4.4, .35, 0], radius=.62)
        self.play(FadeIn(donor), FadeIn(neighbor), FadeIn(far), run_time=.8)
        keep_alive(VGroup(donor, neighbor, far), .17)
        breathe(VGroup(donor, neighbor, far), .018, 3.8)
        self.at("one more route")
        route = label("A resistance gene can move", 38, INK, font=TITLE_FONT).move_to([0, 2.8, 0])
        self.play(Write(route), run_time=.7)
        self.at("pass a resistance gene")
        gene = chip("resistance gene", ORANGE_RESIST, size=28, fill_opacity=.1).scale(.86).move_to([-3.4, 1.35, 0])
        self.play(FadeIn(gene, scale=.4), run_time=.5)
        self.play(gene.animate.move_to([0, 1.35, 0]), run_time=1.15)
        self.at("another bacterium")
        self.play(Indicate(neighbor, color=TEAL, scale_factor=1.25), run_time=.55)
        self.at("now survives the drug")
        new_neighbor = resistant(neighbor.get_center(), size=1.25)
        mark = drug_mark(neighbor.get_center(), 1.5)
        self.play(ReplacementTransform(neighbor, new_neighbor), FadeOut(gene), FadeIn(mark), run_time=.65)
        self.play(FadeOut(mark), run_time=.4)
        self.at("resistance can spread")
        gene2 = chip("resistance gene", ORANGE_RESIST, size=28, fill_opacity=.1).scale(.86).move_to([0, 1.35, 0])
        self.play(FadeIn(gene2, scale=.4), gene2.animate.move_to([4.4, 1.35, 0]), run_time=1.15)
        self.at("never met the drug")
        never = label("never saw the drug", 30, INK).move_to([4.4, -1.1, 0])
        new_far = resistant(far.get_center(), size=1.25)
        self.play(ReplacementTransform(far, new_far), FadeOut(gene2), FadeIn(never), run_time=.75)
        self.finish()


def mini_field(kind, center):
    frame = RoundedRectangle(corner_radius=.4, width=3.55, height=3.35, stroke_color=SOFT, stroke_width=3).move_to(center)
    pos = [center + np.array([x, y, 0]) for y in (.75, 0, -.75) for x in (-1.05, -.35, .35, 1.05)]
    cells = VGroup()
    for i, p in enumerate(pos):
        if kind == "mixed":
            cells.add(resistant(p, .38) if i in (3, 8) else sensitive(p, .2))
        elif kind == "sweep":
            if i in (3, 8): cells.add(resistant(p, .38))
            elif i % 2: cells.add(sensitive(p, .2, outline=True))
        else:
            cells.add(resistant(p, .38))
    return VGroup(frame, cells)


class S11Rule(SpokenScene):
    def construct(self):
        self.add(paper())
        centers = [np.array([-4.25, .45, 0]), np.array([0, .45, 0]), np.array([4.25, .45, 0])]
        fields = [mini_field(k, c) for k, c in zip(("mixed", "sweep", "orange"), centers)]
        heads = VGroup(label("mixed", 30, TEAL).move_to([-4.25, 2.55, 0]),
                       label("drug", 30, GOLD).move_to([0, 2.55, 0]),
                       label("survivors grow", 30, ORANGE_RESIST).move_to([4.25, 2.55, 0]))
        self.play(FadeIn(fields[0]), FadeIn(heads[0]), run_time=.75)
        for f in fields:
            keep_alive(f[1], .07)
        self.at("not a cure")
        self.play(Indicate(fields[0], color=INK, scale_factor=1.03), run_time=.6)
        self.at("survivors grow back")
        self.play(FadeIn(fields[1]), FadeIn(heads[1]), run_time=.75)
        marks = VGroup(*[drug_mark([-.9+i*.45, .45, 0], .55) for i in range(5)])
        self.play(FadeIn(marks), run_time=.4)
        self.at("favor any resistant")
        self.play(FadeOut(marks), FadeIn(fields[2]), FadeIn(heads[2]), run_time=.8)
        self.at("An antibiotic spares")
        rule = caption("An antibiotic spares resistant bacteria,", size=32, color=INK, y=-2.65)
        self.play(Write(rule), run_time=.9)
        self.at("survivors can take over")
        rule2 = label("and the survivors can take over.", 32, ORANGE_RESIST).move_to([0, -3.2, 0])
        self.play(Write(rule2), Indicate(fields[2], color=ORANGE_RESIST), run_time=.9)
        self.finish()


class S12End(EndCard):
    LINE = "An antibiotic spares resistant bacteria, and the survivors can take over."
