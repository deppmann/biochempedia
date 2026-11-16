"""How One Mark Finds Its Reader.

COLOR MAP (one colour per concept, throughout)
  BLUE  = receptors, tails, host proteins, and other protein partners
  GOLD  = phosphate marks
  TEAL  = binding domains / readers
  GREEN = a neighbouring motif that fits the reader
  RED   = a poorer contact (never an impossible or rejected site)

All pictures are schematic. Proteins are blocks or lines; no molecular structures are drawn.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


def phosphate_badge(r=0.25):
    disc = Circle(radius=r, color=GOLD, stroke_width=3,
                  fill_color=GOLD, fill_opacity=1)
    return VGroup(disc, T("P", 24, BG, weight=BOLD).move_to(disc))


def residue_row(colors=(GREEN, GREEN, GREEN), scale=1.0):
    blocks = VGroup(*[
        RoundedRectangle(corner_radius=0.08, width=0.48, height=0.48,
                         color=c, stroke_width=3, fill_color=c, fill_opacity=0.55)
        for c in colors
    ]).arrange(RIGHT, buff=0.12)
    return blocks.scale(scale)


def tail_world(y=0.0, badge_x=(-3.7, -1.4, 1.0, 3.5), motifs=False):
    """The carried receptor-tail picture, rebuilt at the same size and position."""
    pts = [[-5.8, y + 0.05, 0], [-4.2, y + 0.25, 0], [-2.5, y - 0.15, 0],
           [-0.7, y + 0.18, 0], [1.2, y - 0.18, 0], [3.1, y + 0.16, 0], [5.7, y, 0]]
    line = VMobject(stroke_color=BLUE, stroke_width=9, fill_opacity=0)
    line.set_points_smoothly(pts)
    badges = VGroup(*[phosphate_badge().move_to([x, y + (0.42 if i % 2 == 0 else -0.44), 0])
                      for i, x in enumerate(badge_x)])
    g = VGroup(line, badges)
    if motifs:
        rows = VGroup(*[residue_row((GREEN, GREEN, GREEN) if i == 2 else (RED, GREY, RED), 0.68)
                        .move_to([x + 0.8, y + (0.42 if i % 2 == 0 else -0.44), 0])
                        for i, x in enumerate(badge_x)])
        g.add(rows)
        g.motifs = rows
    g.line, g.badges = line, badges
    return g


def sh2_reader(center=ORIGIN, scale=1.0, label=True, label_dir=UP):
    """A two-contact SH2 clamp: round phosphate pocket plus shallow motif groove."""
    pocket = Arc(radius=0.72, start_angle=45 * DEGREES, angle=270 * DEGREES,
                 color=TEAL, stroke_width=10).rotate(PI).shift(LEFT * 0.72)
    groove = Arc(radius=0.85, start_angle=200 * DEGREES, angle=140 * DEGREES,
                 color=TEAL, stroke_width=10).shift(RIGHT * 0.72 + DOWN * 0.12)
    bridge = Line([-0.15, 0.53, 0], [0.25, 0.53, 0], color=TEAL, stroke_width=10)
    core = VGroup(pocket, groove, bridge).scale(scale)
    g = VGroup(core)
    if label:
        lab = boxed_label("SH2", TEAL, size=28, fill_opacity=0.22).next_to(core, label_dir, buff=0.2)
        g.add(lab)
        g.label = lab
    g.move_to(center)
    g.pocket, g.groove = pocket, groove
    return g


def target_strip(y=-1.0, fit_pattern=True, scale=1.0):
    px = -1.15 * scale
    gap = max(0.34, 0.36 * scale)
    line = VGroup(Line([-3.2 * scale, y, 0], [px - gap, y, 0], color=BLUE, stroke_width=8),
                  Line([px + gap, y, 0], [3.2 * scale, y, 0], color=BLUE, stroke_width=8))
    p = phosphate_badge(max(0.24, 0.28 * scale)).move_to([px, y, 0])
    cols = (GREEN, GREEN, GREEN) if fit_pattern else (RED, GREY, RED)
    row = residue_row(cols, max(0.72, scale)).move_to([0.55 * scale, y, 0])
    return VGroup(line, p, row)


def prediction_world(add_question=False):
    """Exact shared layout for predict, pause, and reveal."""
    upper = target_strip(1.55, False)
    lower = target_strip(-0.55, True)
    reader = sh2_reader([4.45, 0.55, 0], 0.82)
    labels = VGroup(T("upper tail", 28, BLUE).move_to([-4.65, 1.55, 0]),
                    T("lower tail", 28, BLUE).move_to([-4.65, -0.55, 0]))
    world = VGroup(upper, lower, reader, labels, scope_tag())
    if add_question:
        world.add(question_card("Which tail retains the reader longer?", y=-3.15, max_w=10.5))
    return world


def host_block(text, center, shape="rect"):
    if shape == "scaffold":
        body = Polygon([-2.0, -0.75, 0], [1.45, -0.75, 0], [2.0, 0, 0],
                       [1.45, 0.75, 0], [-2.0, 0.75, 0], color=BLUE,
                       stroke_width=4, fill_color=BLUE, fill_opacity=0.16)
    else:
        body = RoundedRectangle(corner_radius=0.28, width=4.0, height=1.5,
                                color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.16)
    body.move_to(center)
    lab = T(text, 30, BLUE).move_to(body)
    return VGroup(body, lab)


class Film(SpokenScene):
    def setup(self):
        super().setup()
        # One shared diagram world: a broad cellular field that breathes continuously while
        # the narrated contact is being assembled.  It keeps long explanatory holds alive
        # without adding another biological claim or another labelled object.
        stage = RoundedRectangle(corner_radius=0.28, width=12.45, height=6.55,
                                 stroke_width=0, fill_color=BLUE, fill_opacity=0.15)
        stage.set_z_index(-20)
        stage._field_t = 0.0

        def breathe(mob, dt):
            mob._field_t += dt
            mob.set_fill(BLUE, opacity=0.15 + 0.08 * np.sin(2.4 * mob._field_t))

        stage.add_updater(breathe)
        self.add(stage)

    def done(self):
        self.finish()


class S01Hook(Film):
    def construct(self):
        world = tail_world(-0.25)
        receptor = boxed_label("receptor tail", BLUE, size=28).move_to([-4.7, 2.65, 0])
        self.play(Create(world.line), FadeIn(receptor), run_time=0.9)
        self.at("phosphatirasein marks")
        self.play(LaggedStart(*[FadeIn(b, scale=0.3) for b in world.badges], lag_ratio=0.18), run_time=1.5)
        reader = sh2_reader([0, 2.0, 0], 0.7)
        q = T("?", 72, GOLD, weight=BOLD).next_to(reader, RIGHT, buff=0.35)
        self.at("How can")
        self.play(FadeIn(reader, shift=DOWN * 0.25), FadeIn(q, scale=0.6), run_time=0.8)
        path = ArcBetweenPoints([-2.5, 1.35, 0], [3.3, 1.2, 0], angle=-0.35)
        self.play(MoveAlongPath(reader, path), q.animate.shift(RIGHT * 3.3 + DOWN * 0.2), run_time=2.4)
        self.add(scope_tag())
        bob(world, amp=0.045, speed=1.4)
        self.at("among all the others")
        self.play(LaggedStart(*[Indicate(b, color=GOLD, scale_factor=1.18)
                                for b in world.badges], lag_ratio=0.15), run_time=1.1)
        self.done()


class S02Title(TitleCard):
    LESSON = "Protein Interaction Modules"
    TITLE = "How One Mark Finds Its Reader"


class S03Marks(Film):
    def construct(self):
        tail = VGroup(Line([-5.4, -0.25, 0], [-1.88, -0.25, 0], color=BLUE, stroke_width=10),
                      Line([-0.92, -0.25, 0], [5.4, -0.25, 0], color=BLUE, stroke_width=10))
        patch = Circle(radius=0.43, color=BLUE, stroke_width=4,
                       fill_color=BLUE, fill_opacity=0.18).move_to([-1.4, -0.25, 0])
        self.play(Create(tail), FadeIn(patch), run_time=0.8)
        self.at("Phosphate changes")
        p = phosphate_badge(0.34).move_to(patch)
        self.play(FadeIn(p, scale=0.25), patch.animate.set_stroke(GOLD), run_time=0.8)
        alone = T("mark alone", 28, GOLD).next_to(patch, DOWN, buff=0.55)
        self.play(FadeIn(alone), run_time=0.5)
        self.at("It becomes useful")
        reader = sh2_reader([-1.4, 1.45, 0], 0.78)
        self.play(FadeIn(reader, shift=UP * 0.25), FadeOut(alone), run_time=0.8)
        self.play(reader.animate.shift(DOWN * 0.2), run_time=0.7)
        self.at("brings its host")
        host = host_block("host protein", [2.7, 1.55, 0])
        tether = Line(reader.get_right(), host.get_left(), color=TEAL, stroke_width=7)
        self.play(FadeIn(host, shift=LEFT * 0.35), Create(tether), run_time=1.0)
        connection = T("connection", 30, GREEN).move_to([1.0, -1.45, 0])
        self.play(FadeIn(connection, shift=UP * 0.15), run_time=0.5)
        self.at("A kinase")
        kinase = boxed_label("kinase", BLUE, size=28).move_to([-4.3, 2.5, 0])
        self.play(FadeIn(kinase), run_time=0.5)
        self.play(Indicate(p, color=GOLD), run_time=0.6)
        self.at("phosphatase")
        phosphatase = boxed_label("phosphatase", BLUE, size=28).move_to([-4.15, 1.45, 0])
        self.play(swap(kinase, phosphatase), run_time=0.7)
        self.play(reader.animate.shift(UP * 0.55), run_time=0.45)
        self.play(FadeOut(p, scale=0.25), patch.animate.set_stroke(BLUE), run_time=0.7)
        self.done()


class S04FirstJob(Film):
    def construct(self):
        reader = sh2_reader([0.1, 1.0, 0], 1.4)
        self.play(FadeIn(reader, scale=0.85), run_time=0.8)
        self.at("first binding pocket")
        pocket_label = T("phosphate pocket", 30, TEAL).move_to([-4.25, 2.9, 0])
        arrow = Arrow(pocket_label.get_right(), reader.get_left() + RIGHT * 0.1,
                      buff=0.3, color=TEAL, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(pocket_label), GrowArrow(arrow), run_time=0.7)
        ptyr = VGroup(phosphate_badge(0.34), T("pY", 30, GOLD).move_to([0, -0.8, 0]))
        ptyr.move_to([-4.5, -0.7, 0])
        self.at("phosphatirosine")
        self.play(FadeIn(ptyr), run_time=0.5)
        self.play(ptyr[0].animate.move_to(reader.get_left() + RIGHT * 0.7 + DOWN * 0.1), run_time=1.0)
        self.at("Positively charged")
        pluses = VGroup(*[T("+", 30, TEAL, weight=BOLD).move_to([-2.35, 0.1 + i * 0.5, 0])
                          for i in range(3)])
        self.play(LaggedStart(*[FadeIn(x) for x in pluses], lag_ratio=0.2), run_time=0.8)
        self.play(Indicate(ptyr[0], color=GOLD), run_time=0.7)
        self.at("Unmodified")
        tyr = VGroup(Circle(radius=0.34, color=BLUE, stroke_width=4),
                     T("Y", 28, BLUE, weight=BOLD)).move_to([4.1, -0.7, 0])
        self.play(FadeIn(tyr), run_time=0.5)
        self.play(tyr.animate.move_to([1.0, -1.15, 0]), run_time=0.8)
        self.at("lacks that phosphate")
        cross = T("×", 62, RED, weight=BOLD).move_to(tyr)
        self.play(FadeIn(cross, scale=0.5), tyr.animate.shift(RIGHT * 2.6), run_time=0.9)
        poorer = T("contact missing", 28, RED).next_to(tyr, DOWN, buff=0.3)
        self.play(FadeIn(poorer), run_time=0.5)
        self.done()


class S05SecondJob(Film):
    def construct(self):
        reader = sh2_reader([0, 0.75, 0], 1.35)
        p = phosphate_badge(0.34).move_to([-1.0, 0.55, 0])
        sites = VGroup(*[target_strip(0, fit_pattern=(i == 1), scale=0.55).move_to([-3.9, y, 0])
                         for i, y in enumerate([1.3, 0.0, -1.3])])
        self.add(reader, p)
        self.at("whether tyrosine")
        yes = boxed_label("phosphorylated?", GOLD, size=28).move_to([-4.3, 2.65, 0])
        self.play(FadeIn(yes), Indicate(p, color=GOLD), run_time=0.8)
        self.at("cannot identify")
        self.play(FadeIn(sites, shift=RIGHT * 0.2), FadeOut(yes), run_time=0.9)
        same = T("same P", 28, GOLD).move_to([-4.3, 2.65, 0])
        self.play(FadeIn(same), run_time=0.5)
        self.at("neighboring surface")
        groove_label = T("neighbouring groove", 30, TEAL).move_to([3.9, 2.6, 0])
        arrow = Arrow(groove_label.get_bottom(), [1.05, 1.05, 0], buff=0.12,
                      color=TEAL, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(groove_label), GrowArrow(arrow), run_time=0.7)
        motif = residue_row().move_to([0.7, -0.3, 0])
        self.at("residues beside")
        self.play(FadeIn(motif, shift=RIGHT * 0.2), run_time=0.6)
        self.play(motif.animate.shift(UP * 0.62), run_time=0.8)
        self.at("another layer")
        pref = boxed_label("preference", GREEN, size=30).move_to([4.45, -1.5, 0])
        self.play(FadeIn(pref, scale=0.8), run_time=0.6)
        self.at("Different SH2 domains")
        alt = sh2_reader([4.3, 0.25, 0], 0.68)
        alt.groove.set_color(BLUE)
        self.play(FadeIn(alt, shift=LEFT * 0.2), FadeOut(pref), run_time=0.7)
        self.play(Transform(alt.groove, alt.groove.copy().stretch(0.7, 0)), run_time=0.8)
        self.done()


class S06Compare(Film):
    def construct(self):
        reader = sh2_reader([2.7, 0.6, 0], 1.05)
        self.add(reader)
        self.at("tests both features")
        both = VGroup(T("P", 30, GOLD, weight=BOLD), T("+", 32, TEXT),
                      T("pattern", 30, GREEN)).arrange(RIGHT, buff=0.25).move_to([-3.6, 2.7, 0])
        self.play(FadeIn(both), run_time=0.6)
        tails = [target_strip(0, ok, scale=0.72).move_to([-3.0, -0.9, 0])
                 for ok in (False, True, False)]
        self.at("Several tails")
        self.play(FadeIn(tails[0], shift=RIGHT * 0.3), run_time=0.6)
        self.play(tails[0].animate.shift(RIGHT * 3.0), run_time=0.8)
        self.at("patterns differ")
        self.play(FadeOut(tails[0], shift=DOWN * 0.3), FadeIn(tails[1], shift=RIGHT * 0.3), run_time=0.7)
        self.at("Matching blocks")
        self.play(tails[1].animate.shift(RIGHT * 3.0 + UP * 0.2), run_time=0.9)
        fit_lab = boxed_label("stronger fit", GREEN, size=28).move_to([-3.7, -2.15, 0])
        self.play(FadeIn(fit_lab), Indicate(reader.groove, color=GREEN), run_time=0.7)
        self.at("poor fits")
        self.play(FadeOut(tails[1]), FadeOut(fit_lab), FadeIn(tails[2]), run_time=0.6)
        self.play(tails[2].animate.shift(RIGHT * 2.5), run_time=0.7)
        self.play(tails[2].animate.shift(LEFT * 2.5 + DOWN * 0.4), run_time=0.7)
        poorer = T("poorer fit → release", 28, RED).move_to([-3.5, -2.15, 0])
        self.play(FadeIn(poorer), run_time=0.5)
        self.at("Sarc family")
        family = VGroup(boxed_label("Src-family SH2", TEAL, size=28),
                        boxed_label("another SH2", BLUE, size=28)).arrange(DOWN, buff=0.35).move_to([3.95, -2.25, 0])
        self.play(FadeOut(poorer), FadeIn(family, shift=UP * 0.2), run_time=0.8)
        self.play(family[0].animate.set_color(GREEN), family[1].animate.set_color(GOLD), run_time=0.8)
        self.done()


class S07Rule(Film):
    def construct(self):
        target = target_strip(0, True, scale=1.15).move_to([-2.4, -0.65, 0])
        reader = sh2_reader([1.2, 0.65, 0], 1.15)
        host = host_block("host protein", [4.35, 0.55, 0]).scale(0.85, about_point=[4.35, 0.55, 0])
        self.add(target, reader, host)
        self.at("Here is the rule")
        rule = fit_text("Reusable binding domains turn recognized motifs or lipids\ninto protein connections.",
                        max_w=11.5, size=34, color=TEXT, min_size=28).move_to([0, 2.65, 0])
        self.play(Write(rule), run_time=1.0)
        self.at("protein connections")
        link = pulse(Line(reader.get_right(), host.get_left(), color=GREEN, stroke_width=9),
                     base=9, amp=2, speed=2.5)
        self.play(Create(link), run_time=0.8)
        self.at("phosphorylation enables")
        self.play(Indicate(target[1], color=GOLD), run_time=0.7)
        self.at("sequence context")
        self.play(Indicate(target[2], color=GREEN), run_time=0.7)
        choose = T("enables + chooses", 30, GREEN).move_to([0, -2.25, 0])
        self.play(FadeIn(choose), run_time=0.5)
        self.at("domain binds")
        binds = boxed_label("binding", TEAL, size=30).move_to([-4.7, 1.3, 0])
        self.play(FadeIn(binds), run_time=0.5)
        self.at("does not catalyze")
        not_rxn = boxed_label("not catalysis", RED, size=28).move_to([-4.5, 0.15, 0])
        self.play(FadeIn(not_rxn), FadeOut(binds), run_time=0.6)
        self.play(Indicate(link, color=GREEN, scale_factor=1.02), run_time=0.7)
        self.done()


class S08Predict(Film):
    def construct(self):
        upper = target_strip(1.55, False)
        lower = target_strip(-0.55, True)
        labels = VGroup(T("upper tail", 28, BLUE).move_to([-4.65, 1.55, 0]),
                        T("lower tail", 28, BLUE).move_to([-4.65, -0.55, 0]))
        self.add(upper, lower, labels, scope_tag())
        self.at("Predict before")
        reader = sh2_reader([4.45, 0.55, 0], 0.82)
        self.play(FadeIn(reader, shift=LEFT * 0.3), run_time=0.7)
        self.at("Both tails")
        self.play(Indicate(upper[1], color=GOLD), Indicate(lower[1], color=GOLD), run_time=0.8)
        self.at("Only the lower")
        self.play(Indicate(lower[2], color=GREEN), run_time=0.8)
        self.at("Which tail")
        q = question_card("Which tail retains the reader longer?", y=-3.15, max_w=10.5)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.at("Watch both parts")
        self.play(Indicate(reader.pocket, color=GOLD), Indicate(reader.groove, color=GREEN), run_time=0.9)
        bob(reader, amp=0.05, speed=1.7)
        self.done()


class S09Pause(PredictPause):
    QUESTION = "Which tail retains the reader longer?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "max_w": 10.5}
    RING_AT = (-6.0, 2.9, 0)

    def backdrop(self):
        world = prediction_world(False)
        bob(world[0], amp=0.035, speed=1.4)
        bob(world[1], amp=0.035, speed=1.4, seed=2)
        bob(world[2], amp=0.05, speed=1.7, seed=1)
        return world


class S10Reveal(Film):
    def construct(self):
        world = prediction_world(False)
        upper, lower, reader = world[0], world[1], world[2]
        self.add(world)
        self.at("lower tail")
        self.play(reader.animate.move_to([2.25, -0.05, 0]), run_time=1.0)
        self.at("both contacts")
        self.play(Indicate(lower[1], color=GOLD), run_time=0.55)
        self.play(Indicate(lower[2], color=GREEN), run_time=0.55)
        strong = boxed_label("stronger retention", GREEN, size=28).move_to([4.65, -1.55, 0])
        self.at("more strongly")
        self.play(FadeIn(strong, shift=UP * 0.15), run_time=0.6)
        self.at("upper tail still")
        self.play(Indicate(upper[1], color=GOLD), run_time=0.7)
        self.at("neighboring pattern")
        poor = boxed_label("poorer fit", RED, size=28).move_to([0.15, 2.65, 0])
        self.play(FadeIn(poor), Indicate(upper[2], color=RED), run_time=0.7)
        self.at("Another SH2")
        alt = sh2_reader([4.45, 0.45, 0], 0.82)
        alt.groove.set_color(BLUE)
        self.play(FadeOut(strong), FadeIn(alt, shift=LEFT * 0.2), run_time=0.7)
        self.at("different pattern")
        self.play(Indicate(upper[2], color=BLUE), alt.groove.animate.stretch(0.7, 0), run_time=0.8)
        self.done()


class S11Portable(Film):
    def construct(self):
        host1 = host_block("enzyme host", [-3.7, 1.25, 0])
        host2 = host_block("scaffold host", [3.65, 1.25, 0], "scaffold")
        reader = sh2_reader([-3.7, -0.2, 0], 0.72, label_dir=LEFT)
        target = target_strip(0, True, scale=0.75).move_to([-3.7, -2.05, 0])
        tether = Line(host1.get_bottom(), reader.get_top(), color=BLUE, stroke_width=7)
        self.add(host1, reader, tether, target, scope_tag())
        self.at("keeps this binding")
        self.play(reader.animate.shift(DOWN * 0.25), target.animate.shift(UP * 0.25), run_time=0.7)
        self.at("Detach the reader")
        self.play(FadeOut(tether), reader.animate.shift(DOWN * 0.45), run_time=0.7)
        self.at("different host")
        self.play(FadeIn(host2, shift=LEFT * 0.3), run_time=0.6)
        self.play(reader.animate.move_to([3.65, -0.05, 0]), run_time=1.0)
        tether2 = Line(host2.get_bottom(), [3.65, 0.5, 0], color=BLUE, stroke_width=7)
        self.play(Create(tether2), run_time=0.5)
        self.at("preferred target")
        self.play(target.animate.move_to([3.65, -2.05, 0]), run_time=1.0)
        self.play(target.animate.shift(UP * 0.35), reader.animate.shift(DOWN * 0.15), run_time=0.7)
        same = boxed_label("same target", GREEN, size=28).move_to([0, -2.55, 0])
        self.play(FadeIn(same), run_time=0.5)
        self.at("different cellular activity")
        activity = VGroup(*[Dot(radius=0.11, color=BLUE).move_to([4.8 + 0.4 * i, 2.4, 0])
                            for i in range(3)])
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in activity], lag_ratio=0.25), run_time=0.8)
        self.play(activity.animate.shift(DOWN * 0.55), run_time=0.7)
        self.done()


class S12Context(Film):
    def construct(self):
        reader = sh2_reader([0, 0.1, 0], 0.9)
        self.add(reader, scope_tag())
        self.at("Preference is not destiny")
        title = T("preference ≠ destiny", 38, GOLD, weight=BOLD).move_to([0, 2.85, 0])
        self.play(FadeIn(title, scale=0.85), run_time=0.7)
        filters = []
        specs = [("location", [-4.4, 1.55, 0]), ("abundance", [4.35, 1.55, 0]),
                 ("timing", [-4.4, -1.25, 0]), ("host context", [4.25, -1.25, 0])]
        for text, pos in specs:
            filters.append(boxed_label(text, BLUE, size=28).move_to(pos))
        self.at("Location")
        self.play(FadeIn(filters[0], shift=RIGHT * 0.2), run_time=0.5)
        self.at("abundance")
        self.play(FadeIn(filters[1], shift=LEFT * 0.2), run_time=0.5)
        self.at("timing")
        self.play(FadeIn(filters[2], shift=RIGHT * 0.2), run_time=0.5)
        self.at("rest of the host")
        self.play(FadeIn(filters[3], shift=LEFT * 0.2), run_time=0.6)
        candidates = VGroup(*[boxed_label(f"partner {c}", BLUE, size=24)
                              for c in "ABC"]).arrange(RIGHT, buff=0.25).move_to([0, -2.35, 0])
        self.play(FadeIn(candidates, shift=UP * 0.2), run_time=0.7)
        self.at("domain narrows")
        self.play(FadeOut(candidates[2], shift=DOWN * 0.2), run_time=0.7)
        self.at("context narrows")
        self.play(FadeOut(candidates[1], shift=DOWN * 0.2), run_time=0.5)
        self.play(candidates[0].animate.move_to([0, -2.25, 0]), run_time=0.4)
        self.at("never reaches")
        barrier = DashedLine([-1.7, -1.4, 0], [1.7, -1.4, 0], color=RED, stroke_width=5)
        self.play(Create(barrier), run_time=0.5)
        self.play(candidates[0].animate.shift(LEFT * 2.7), Indicate(reader, color=RED), run_time=0.9)
        self.done()


class S13OtherReaders(Film):
    def construct(self):
        sh2 = sh2_reader([0, 0.35, 0], 1.15)
        target = target_strip(-1.5, True, scale=0.85)
        self.add(sh2, target, scope_tag())
        self.at("Other modules")
        family = T("same recognition logic", 36, TEAL).move_to([0, 2.75, 0])
        self.play(FadeIn(family), run_time=0.6)
        self.at("SH3 reads")
        sh3_shape = VGroup(Arc(radius=1.1, start_angle=200 * DEGREES, angle=140 * DEGREES,
                              color=TEAL, stroke_width=11),
                           boxed_label("SH3", TEAL, size=28).move_to([0, 1.45, 0]))
        proline = residue_row((GREEN, GREEN, GREEN, GREEN)).move_to([0, -0.45, 0])
        self.play(ReplacementTransform(sh2, sh3_shape), FadeOut(target), FadeIn(proline), run_time=1.0)
        self.play(proline.animate.shift(UP * 0.55), run_time=0.7)
        pro_lab = T("proline-rich motif", 30, GREEN).move_to([0, -2.25, 0])
        self.play(FadeIn(pro_lab), run_time=0.5)
        self.at("some pH domains")
        pocket = VGroup(Arc(radius=1.0, start_angle=35 * DEGREES, angle=290 * DEGREES,
                            color=TEAL, stroke_width=11).rotate(PI),
                        boxed_label("PH", TEAL, size=28).move_to([0, 1.45, 0]))
        membrane = RoundedRectangle(corner_radius=0.12, width=10.5, height=0.42,
                                    color=BLUE, stroke_width=4, fill_color=BLUE,
                                    fill_opacity=0.28).move_to([0, -1.55, 0])
        lipids = VGroup(*[Circle(radius=0.16, color=(GREEN if i == 5 else BLUE),
                                fill_color=(GREEN if i == 5 else BLUE), fill_opacity=0.75)
                          .move_to([-4.5 + i * 0.9, -1.25, 0]) for i in range(11)])
        self.play(ReplacementTransform(sh3_shape, pocket), FadeOut(VGroup(proline, pro_lab)),
                  FadeIn(membrane), FadeIn(lipids), run_time=1.0)
        self.at("membrane lipids")
        self.play(Indicate(lipids[5], color=GREEN), pocket.animate.shift(DOWN * 0.55), run_time=0.8)
        self.at("recognition still")
        connection = pulse(Line([0, -0.25, 0], [0, -1.1, 0], color=GREEN, stroke_width=9),
                           base=9, amp=2, speed=2.5)
        self.play(Create(connection), run_time=0.7)
        self.at("connection is")
        lab = T("connection to membrane", 30, GREEN).move_to([3.8, -2.35, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.6)
        self.done()


class S14End(EndCard):
    LINE = "Reusable binding domains turn recognized motifs or lipids into protein connections."
