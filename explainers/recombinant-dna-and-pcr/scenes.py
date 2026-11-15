"""From DNA Fragment to Verified Clone.

COLOR MAP
  GREY   original DNA, cells, outlines, unresolved panels
  YELLOW insert DNA and compatible ends
  BLUE   plasmids, plasmid copies, and ligase
  GREEN  supported results and evidence
  RED    unresolved or mismatched results
"""
from bp_parts import *


def lab_stage():
    stage = RoundedRectangle(width=13.2, height=6.35, corner_radius=0.32,
                             stroke_width=0, fill_color="#1D2B36",
                             fill_opacity=0.94).move_to([0, -0.05, 0])
    stage.set_z_index(-10)
    return stage


def lab_motes(seed):
    rng = np.random.default_rng(seed)
    motes = VGroup()
    zones = [(2.2, 5.15, -2.65, -1.05), (-5.6, -1.45, 1.55, 3.0),
             (-4.7, -2.4, 0.65, 1.65), (-5.0, 5.2, -0.25, 0.9),
             (1.0, 5.2, 1.35, 2.65), (-4.7, -1.45, -1.6, -0.55),
             (-3.3, 2.8, -2.55, -1.45), (-6.1, -4.65, -1.85, -1.05)]
    blocked = lambda x, y: any(x0 < x < x1 and y0 < y < y1 for x0, x1, y0, y1 in zones)
    for _ in range(140):
        d = Dot(radius=rng.uniform(0.07, 0.11),
                color=rng.choice([GREY, TEAL, BLUE])).set_opacity(rng.uniform(0.35, 0.55))
        while True:
            x, y = rng.uniform(-6.05, 5.05), rng.uniform(-2.70, 2.70)
            if not blocked(x, y):
                break
        d.move_to([x, y, 0])
        d.v = np.array([rng.uniform(-0.34, 0.34), rng.uniform(0.35, 0.65), 0])

        def drift(m, dt):
            m.shift(m.v * dt)
            x, y = m.get_x(), m.get_y()
            if blocked(x, y):
                m.move_to([-6.0, -2.70, 0])
            if m.get_y() > 2.75:
                m.shift(DOWN * 5.4)
            elif m.get_y() < -2.75:
                m.shift(UP * 5.4)
            if m.get_x() > 5.1:
                m.shift(LEFT * 11.1)
            elif m.get_x() < -6.1:
                m.shift(RIGHT * 11.1)
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-9)
    return motes


def lab_scanlines():
    """A faint periodic field whose motion survives the 320 px film audit."""
    spacing = 0.38
    lines = VGroup(*[
        Rectangle(width=13.0, height=0.10, stroke_width=0,
                  fill_color=TEAL, fill_opacity=0.16).move_to([0, -2.85 + i * spacing, 0])
        for i in range(17)
    ])
    lines._offset = 0.0

    def drift(g, dt):
        dy = 0.65 * dt
        g.shift(UP * dy)
        g._offset += dy
        if g._offset >= spacing:
            g.shift(DOWN * spacing)
            g._offset -= spacing
    lines.add_updater(drift)
    lines.set_z_index(-8)
    return lines


class FilmScene(SpokenScene):
    """Shared dark lab field: a full carried world with continuous quiet motion."""

    def setup(self):
        super().setup()
        self.add(lab_stage())
        self.add(lab_scanlines())

        # A restrained moving field is part of the landscape style. It keeps spoken
        # holds alive without adding a biological claim or competing with the picture.
        self.add(lab_motes(sum(ord(c) for c in self.__class__.__name__)))


def slow_turn(mob, speed=0.10):
    """Keep a circular subject alive during a spoken hold."""
    return mob.add_updater(lambda m, dt: m.rotate(speed * dt))


def breathe(mob, amount=0.08, speed=2.0, seed=0.0):
    """A stable opacity breath; unlike scaling, it never changes the layout."""
    mob._breath_t = seed

    def update(m, dt):
        m._breath_t += dt
        m.set_opacity(0.82 + amount * np.sin(speed * m._breath_t))
    return mob.add_updater(update)


def plasmid(center=ORIGIN, radius=1.55, insert=True, question=False, color=BLUE):
    """The carried plasmid schematic, rebuilt at the same scale and position."""
    c = np.array(center, dtype=float)
    if insert:
        left = Arc(radius=radius, start_angle=0.30, angle=TAU - 0.94,
                   arc_center=c, color=color, stroke_width=12)
        ins = Arc(radius=radius, start_angle=-0.64, angle=0.94,
                  arc_center=c, color=YELLOW, stroke_width=13)
        g = VGroup(left, ins)
    else:
        g = VGroup(Circle(radius=radius, color=color, stroke_width=12).move_to(c))
    if question:
        back = Circle(radius=0.38 * radius, stroke_width=0, fill_color=BG,
                      fill_opacity=0.92).move_to(c)
        q = T("?", 58, RED, weight=BOLD).move_to(c)
        breathe(q, amount=0.16, speed=2.8)
        g.add(back, q)
    return g


def open_plasmid(center=ORIGIN, radius=2.05):
    """An opened version of the same circle with a visible cloning gap."""
    c = np.array(center, dtype=float)
    body = Arc(radius=radius, start_angle=0.46, angle=TAU - 0.92,
               arc_center=c, color=BLUE, stroke_width=13)
    p1 = body.get_start()
    p2 = body.get_end()
    e1 = Rectangle(width=0.55, height=0.30, color=YELLOW,
                   fill_color=YELLOW, fill_opacity=1, stroke_width=0).move_to(p1)
    e2 = Rectangle(width=0.55, height=0.30, color=YELLOW,
                   fill_color=YELLOW, fill_opacity=1, stroke_width=0).move_to(p2)
    return VGroup(body, e1, e2)


def bacterium(center=ORIGIN, scale=1.0, has_plasmid=False, insert=True):
    """A labelled-cartoon-free cell silhouette, not a molecular drawing."""
    c = np.array(center, dtype=float)
    cell = RoundedRectangle(width=2.5 * scale, height=1.45 * scale,
                            corner_radius=0.70 * scale, color=GREY,
                            stroke_width=5, fill_color=GREY,
                            fill_opacity=0.13).move_to(c)
    g = VGroup(cell)
    if has_plasmid:
        g.add(plasmid(c, radius=0.36 * scale, insert=insert))
    return g


def colony(center, radius=0.65, question=False, insert=None):
    c = np.array(center, dtype=float)
    disk = Circle(radius=radius, color=GREEN, stroke_width=5,
                  fill_color=GREEN, fill_opacity=0.34).move_to(c)
    inner = VGroup()
    if insert is not None:
        inner = plasmid(c, radius=radius * 0.38, insert=insert)
    g = VGroup(disk, inner)
    if question:
        q = T("?", 40, RED, weight=BOLD).next_to(disk, UP, buff=0.12)
        back = Circle(radius=0.30, stroke_width=0, fill_color=BG,
                      fill_opacity=0.92).move_to(q)
        breathe(q, amount=0.15, speed=2.5, seed=c[0])
        g.add(back, q)
    return g


def plate_world(show_cells=True, show_colonies=False, reveal=False):
    """The carried selective plate used by selection and prediction."""
    plate = Ellipse(width=11.4, height=5.35, color=GREY, stroke_width=5,
                    fill_color="#172027", fill_opacity=0.75).move_to([0, -0.15, 0])
    label = boxed_label("antibiotic", TEAL, size=28).move_to([-4.7, 2.75, 0])
    g = VGroup(plate, label)
    if show_cells:
        pts = [(-3.9, 0.9), (-2.0, -0.9), (0.0, 1.0), (2.1, -0.8), (4.0, 0.75)]
        flags = [False, True, False, True, False]
        cells = VGroup(*[bacterium([x, y, 0], 0.42, flag, insert=(i == 1))
                         for i, ((x, y), flag) in enumerate(zip(pts, flags))])
        g.add(cells)
        g.cells = cells
    if show_colonies:
        a = colony([-2.25, 0, 0], 0.95, question=not reveal,
                   insert=True if reveal else None)
        b = colony([2.25, 0, 0], 0.95, question=not reveal,
                   insert=False if reveal else None)
        g.add(a, b)
        g.colonies = VGroup(a, b)
    return g


def prediction_world(with_question=True):
    """Exact carried frame for the spoken prediction and silent pause."""
    a = colony([-2.15, -0.85, 0], 0.92, question=True)
    b = colony([2.15, -0.85, 0], 0.92, question=True)
    stem = Line([0, -0.05, 0], [0, 0.75, 0], color=GREY, stroke_width=5)
    fork = VGroup(stem,
                  Line([0, 0.75, 0], [-2.45, 1.55, 0], color=GREY, stroke_width=5),
                  Line([0, 0.75, 0], [2.45, 1.55, 0], color=GREY, stroke_width=5))
    shield = boxed_label("antibiotic again", BLUE, size=28).move_to([-3.25, 2.05, 0])
    inspect = boxed_label("inspect plasmid DNA", GREY, size=28).move_to([2.75, 2.05, 0])
    shield.box.set_fill(BG, 0.95); inspect.box.set_fill(BG, 0.95)
    g = VGroup(a, b, fork, shield, inspect)
    if with_question:
        q = question_card("Which observation separates empty vector from intended construct?",
                          y=-3.15, max_w=11.0, size=28)
        g.add(q)
    return g


def gel(center=ORIGIN, result=True):
    """A schematic size gel with fixed, labelled expected positions."""
    c = np.array(center, dtype=float)
    box = RoundedRectangle(width=5.8, height=4.6, corner_radius=0.18,
                           color=GREY, stroke_width=4,
                           fill_color="#111B24", fill_opacity=0.9).move_to(c)
    xs = [c[0] - 1.75, c[0], c[0] + 1.75]
    wells = VGroup(*[Rectangle(width=0.68, height=0.22, color=GREY,
                              fill_color=GREY, fill_opacity=0.35).move_to([x, c[1] + 1.42, 0])
                     for x in xs])
    labs = VGroup(T("ladder", 24, GREY).move_to([xs[0], c[1] + 1.82, 0]),
                  T("A", 28, TEXT).move_to([xs[1], c[1] + 1.82, 0]),
                  T("B", 28, TEXT).move_to([xs[2], c[1] + 1.82, 0]))
    ladder = VGroup(*[Line([xs[0] - 0.28, c[1] + y, 0], [xs[0] + 0.28, c[1] + y, 0],
                               color=GREY, stroke_width=6)
                      for y in [1.15, 0.55, -0.15, -0.9, -1.45]])
    expected = VGroup(
        DashedLine([c[0] - 0.55, c[1] + 0.55, 0], [c[0] + 2.15, c[1] + 0.55, 0],
                   color=GREEN, stroke_width=2, dash_length=0.12),
        DashedLine([c[0] - 0.55, c[1] - 0.9, 0], [c[0] + 2.15, c[1] - 0.9, 0],
                   color=GREEN, stroke_width=2, dash_length=0.12))
    expected.set_opacity(0.45)
    g = VGroup(box, wells, labs, ladder, expected)
    if result:
        bands = VGroup(
            Line([xs[1] - 0.34, c[1] + 0.55, 0], [xs[1] + 0.34, c[1] + 0.55, 0], color=GREEN, stroke_width=10),
            Line([xs[1] - 0.34, c[1] - 0.9, 0], [xs[1] + 0.34, c[1] - 0.9, 0], color=GREEN, stroke_width=10),
            Line([xs[2] - 0.34, c[1] - 0.15, 0], [xs[2] + 0.34, c[1] - 0.15, 0], color=RED, stroke_width=10))
        g.add(bands)
        g.bands = bands
    return g


def sequence_map(center=ORIGIN, colored=False):
    c = np.array(center, dtype=float)
    parts = [("left junction", 2.7), ("insert", 4.3), ("right junction", 2.7)]
    total = sum(w for _, w in parts)
    x = c[0] - total / 2
    blocks = VGroup()
    for i, (name, width) in enumerate(parts):
        col = GREEN if colored else (YELLOW if i == 1 else GREY)
        rect = RoundedRectangle(width=width, height=1.15, corner_radius=0.12,
                                color=col, stroke_width=4, fill_color=col,
                                fill_opacity=0.15).move_to([x + width / 2, c[1], 0])
        lab = T(name, 28, col).move_to(rect)
        blocks.add(VGroup(rect, lab))
        x += width + 0.12
    return blocks


class S00Hook(FilmScene):
    def construct(self):
        cell = bacterium([0, -0.45, 0], scale=2.25)
        col = colony([0, 2.45, 0], radius=0.28)
        p = plasmid([0, -0.45, 0], radius=1.10, insert=True, question=True)
        self.play(FadeIn(cell, scale=0.92), run_time=0.7)
        self.at("A colony has survived")
        self.play(GrowFromCenter(col), run_time=1.1)
        bob(col, amp=0.06, speed=1.6)
        self.at("Does it carry")
        self.play(FadeIn(p, scale=0.8), run_time=0.8)
        self.at("Survival is encouraging")
        self.play(col.animate.scale(1.8), run_time=1.2)
        self.at("only one question")
        self.play(Indicate(p[-1], color=RED, scale_factor=1.25), run_time=0.8)
        self.at("Follow one candidate insert")
        path = CurvedArrow([-4.8, -2.7, 0], [4.8, -2.7, 0], angle=-0.18,
                           color=GREEN, stroke_width=6)
        self.play(Create(path), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Recombinant DNA, Cloning and PCR"
    TITLE = "From DNA Fragment to Verified Clone"


class S02Boundaries(FilmScene):
    def construct(self):
        op = open_plasmid([-1.1, 0, 0], 2.35)
        ins = VGroup(
            Line([3.7, 0.44, 0], [5.7, 0.44, 0], color=YELLOW, stroke_width=13),
            Rectangle(width=0.55, height=0.30, color=YELLOW, fill_color=YELLOW,
                      fill_opacity=1, stroke_width=0).move_to([3.7, 0.44, 0]),
            Rectangle(width=0.55, height=0.30, color=YELLOW, fill_color=YELLOW,
                      fill_opacity=1, stroke_width=0).move_to([5.7, 0.44, 0]))
        self.at("Start with a blue plasmid")
        self.play(Create(op[0]), FadeIn(op[1:]), run_time=1.0)
        self.at("yellow DNA insert")
        self.play(FadeIn(ins, shift=LEFT * 0.3), run_time=0.7)
        self.at("Matching restriction cuts")
        site = boxed_label("restriction site", GREY, size=28).move_to([-1.0, 3.0, 0])
        leads = VGroup(Line(site.get_bottom() + LEFT * 0.35, op[1].get_center() + UP * 0.12,
                            color=GREY, stroke_width=3),
                       Line(site.get_bottom() + RIGHT * 0.35, op[2].get_center() + UP * 0.12,
                            color=GREY, stroke_width=3))
        self.play(FadeIn(site), Create(leads), run_time=0.7)
        self.at("exposed bases can pair")
        joined = plasmid([-1.1, 0, 0], radius=2.35, insert=True)
        self.play(FadeOut(site), FadeOut(leads), Transform(VGroup(op, ins), joined), run_time=1.5)
        self.at("DNA ligase seals")
        lig1 = boxed_label("ligase", BLUE, size=28).move_to([3.15, -1.35, 0])
        lig2 = boxed_label("ligase", BLUE, size=28).move_to([3.15, 1.35, 0])
        self.play(FadeIn(lig1), FadeIn(lig2), run_time=0.5)
        self.play(lig1.animate.shift(LEFT * 0.45),
                  lig2.animate.shift(LEFT * 0.45), run_time=1.0)
        self.at("recombinant candidate")
        ok = T("candidate", 30, GREEN).move_to([-1.1, 0, 0])
        self.play(FadeOut(lig1), FadeOut(lig2), FadeIn(ok), run_time=0.6)
        self.at("other products can form")
        empty = plasmid([4.55, -0.7, 0], radius=0.85, insert=False)
        empty_lab = T("empty vector", 28, RED).next_to(empty, DOWN, buff=0.25)
        self.play(FadeIn(empty), FadeIn(empty_lab), run_time=0.8)
        slow_turn(empty, 0.12)
        self.at("Compatibility permits a join")
        rule = caption("Compatible does not mean verified.", color=TEXT)
        self.play(FadeIn(rule), run_time=0.6)
        self.finish()


class S03Vector(FilmScene):
    def construct(self):
        p = plasmid([0, -0.1, 0], radius=2.2, insert=True, question=True)
        self.play(FadeIn(p), run_time=0.7)
        origin = boxed_label("origin", BLUE, size=28).move_to([-4.45, 1.8, 0])
        marker = boxed_label("selectable marker", GREEN, size=28).move_to([4.25, 1.8, 0])
        site = boxed_label("cloning site", YELLOW, size=28).move_to([3.7, -2.15, 0])
        site.box.set_fill(BG, 0.95)
        self.at("carries an origin")
        self.play(FadeIn(origin, shift=RIGHT * 0.3), run_time=0.6)
        self.at("selectable marker")
        self.play(FadeIn(marker, shift=LEFT * 0.3), run_time=0.6)
        self.at("cloning site")
        self.play(FadeIn(site, shift=UP * 0.3), run_time=0.6)
        self.at("origin lets the host copy")
        d1 = plasmid([-4.4, -1.15, 0], 0.53, insert=True)
        d2 = plasmid([-3.25, -1.15, 0], 0.53, insert=True)
        d1.move_to([0, -0.1, 0]); d2.move_to([0, -0.1, 0])
        self.play(FadeIn(d1, scale=0.6), FadeIn(d2, scale=0.6), run_time=0.35)
        self.play(d1.animate.move_to([-4.4, -1.15, 0]),
                  d2.animate.move_to([-3.25, -1.15, 0]), run_time=0.65)
        slow_turn(d1, 0.16); slow_turn(d2, -0.14)
        self.at("marker can let")
        shield = RegularPolygon(5, radius=0.62, color=GREEN, stroke_width=5,
                                fill_color=GREEN, fill_opacity=0.22).move_to([4.25, 0.35, 0])
        self.play(GrowFromCenter(shield), run_time=0.7)
        self.at("cloning site holds")
        self.play(Indicate(p[1], color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("none reads the insert's complete sequence")
        self.play(Indicate(p[-1], color=RED, scale_factor=1.25), run_time=1.0)
        self.finish()


class S04Transform(FilmScene):
    def construct(self):
        cells = VGroup(bacterium([-4.4, 1.45, 0], 0.85), bacterium([0, 1.45, 0], 0.85),
                       bacterium([4.4, 1.45, 0], 0.85))
        p = plasmid([-4.4, 3.0, 0], 0.48, insert=True)
        self.play(FadeIn(cells), FadeIn(p), run_time=0.8)
        self.at("enters bacteria by transformation")
        with_p = bacterium([-4.4, 1.45, 0], 0.85, True, True)
        self.play(Transform(cells[0], with_p), p.animate.move_to([-4.4, 1.45, 0]).scale(0.6),
                  run_time=1.1)
        self.remove(p)
        self.at("Only some cells take up")
        self.play(Indicate(cells[0], color=BLUE, scale_factor=1.05), run_time=0.7)
        self.at("Those cells divide")
        daughters = VGroup(bacterium([-5.0, -0.35, 0], 0.66, True, True),
                           bacterium([-3.45, -0.35, 0], 0.66, True, True))
        self.play(TransformFromCopy(cells[0], daughters[0]),
                  TransformFromCopy(cells[0], daughters[1]), run_time=1.0)
        self.at("copying the plasmid")
        grand = VGroup(bacterium([-5.6, -1.85, 0], 0.48, True, True),
                       bacterium([-4.45, -1.85, 0], 0.48, True, True),
                       bacterium([-3.3, -1.85, 0], 0.48, True, True),
                       bacterium([-2.15, -1.85, 0], 0.48, True, True))
        self.play(LaggedStart(*[TransformFromCopy(daughters[i // 2], grand[i]) for i in range(4)],
                              lag_ratio=0.12), run_time=1.2)
        self.at("Cells with no plasmid")
        self.play(cells[1].animate.shift(DOWN * 1.6), cells[2].animate.shift(DOWN * 1.6), run_time=0.8)
        self.at("tube now contains several possibilities")
        mix = VGroup(daughters, grand, cells[1], cells[2])
        self.play(mix.animate.shift(RIGHT * 1.25), run_time=1.0)
        self.at("narrow the population")
        plate = Ellipse(width=11.5, height=1.0, color=GREY, stroke_width=5).move_to([0, -3.0, 0])
        self.play(Create(plate), mix.animate.shift(DOWN * 0.35), run_time=1.0)
        self.finish()


class S05Selection(FilmScene):
    def construct(self):
        world = plate_world(show_cells=True)
        self.play(FadeIn(world[0]), FadeIn(world[1]), run_time=0.8)
        self.at("whether a cell probably carries")
        self.play(LaggedStartMap(FadeIn, world.cells, lag_ratio=0.12), run_time=1.0)
        self.at("Spread the cells on antibiotic")
        self.play(Indicate(world[1], color=TEAL, scale_factor=1.06), run_time=0.7)
        self.at("Plasmid-free cells stop growing")
        free = VGroup(world.cells[0], world.cells[2], world.cells[4])
        self.play(free.animate.set_opacity(0.16), run_time=1.0)
        self.at("Marker-bearing cells form colonies")
        ca = colony([-2.0, -0.65, 0], 0.25, question=False, insert=True)
        cb = colony([2.15, -0.55, 0], 0.25, question=False, insert=False)
        self.play(FadeOut(world.cells[1]), FadeOut(world.cells[3]), FadeIn(ca), FadeIn(cb), run_time=0.5)
        self.play(ca.animate.scale(3.3), cb.animate.scale(3.3), run_time=1.4)
        self.at("empty vector can carry")
        qa = T("?", 42, RED, weight=BOLD).next_to(ca, UP, buff=0.12)
        qb = T("?", 42, RED, weight=BOLD).next_to(cb, UP, buff=0.12)
        self.play(FadeIn(qa), FadeIn(qb), run_time=0.6)
        breathe(qa, 0.14, 2.4); breathe(qb, 0.14, 2.4, 1.2)
        self.at("Survival enriches")
        cap = caption("Survival says plasmid, not which construct.", color=TEXT)
        self.play(FadeIn(cap), run_time=0.7)
        self.finish()


class S06Predict(FilmScene):
    def construct(self):
        a = colony([-2.15, -0.85, 0], 0.92, question=True)
        b = colony([2.15, -0.85, 0], 0.92, question=True)
        self.at("Several colonies remain")
        self.play(FadeIn(a), FadeIn(b), run_time=0.8)
        self.at("Which next observation")
        stem = Line([0, -0.05, 0], [0, 0.75, 0], color=GREY, stroke_width=5)
        fork = VGroup(stem,
                      Line([0, 0.75, 0], [-2.45, 1.55, 0], color=GREY, stroke_width=5),
                      Line([0, 0.75, 0], [2.45, 1.55, 0], color=GREY, stroke_width=5))
        self.play(Create(fork), run_time=0.7)
        shield = boxed_label("antibiotic again", BLUE, size=28).move_to([-3.25, 2.05, 0])
        inspect = boxed_label("inspect plasmid DNA", GREY, size=28).move_to([2.75, 2.05, 0])
        shield.box.set_fill(BG, 0.95); inspect.box.set_fill(BG, 0.95)
        self.play(FadeIn(shield), FadeIn(inspect), run_time=0.8)
        self.at("Hold the plate in mind")
        q = question_card("Which observation separates empty vector from intended construct?",
                          y=-3.15, max_w=11.0, size=28)
        self.play(FadeIn(q), run_time=0.6)
        self.at("evidence about the DNA")
        self.play(Indicate(a[-1], color=RED), Indicate(b[-1], color=RED), run_time=0.8)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Which observation separates empty vector from intended construct?"
    OPTIONS = ()
    SECONDS = 4.5
    CARD = {"y": -3.15, "max_w": 11.0, "size": 28}

    def backdrop(self):
        return VGroup(lab_stage(), lab_motes(707), lab_scanlines(),
                      prediction_world(with_question=False))


class S08Screen(FilmScene):
    def construct(self):
        panel = boxed_label("inspect plasmid DNA", GREY, size=28,
                            box=(4.0, 0.75)).move_to([0, 3.15, 0])
        self.play(FadeIn(panel), run_time=0.5)
        self.at("Screening inspects")
        self.play(panel.box.animate.set_fill(GREY, 0.26), run_time=0.6)
        samples = VGroup(colony([-5.2, 1.15, 0], 0.53), colony([-5.2, -1.05, 0], 0.53))
        self.play(FadeIn(samples), run_time=0.6)
        self.at("colony PCR or restriction digest")
        tubes = VGroup(boxed_label("sample A", BLUE, size=26).move_to([-3.55, 1.15, 0]),
                       boxed_label("sample B", BLUE, size=26).move_to([-3.55, -1.05, 0]))
        self.play(FadeIn(tubes[0], shift=RIGHT * 0.3),
                  FadeIn(tubes[1], shift=RIGHT * 0.3), run_time=0.9)
        self.at("expected sizes")
        g = gel([2.1, -0.15, 0], result=False)
        self.play(FadeIn(g), run_time=0.8)
        tag = scope_tag("schematic")
        self.play(FadeIn(tag), run_time=0.4)
        self.at("matching pattern moves")
        bands = VGroup(
            Line([1.76, 0.4, 0], [2.44, 0.4, 0], color=GREEN, stroke_width=10),
            Line([1.76, -1.05, 0], [2.44, -1.05, 0], color=GREEN, stroke_width=10),
            Line([3.51, -0.3, 0], [4.19, -0.3, 0], color=RED, stroke_width=10))
        self.play(LaggedStartMap(Create, bands, lag_ratio=0.25), run_time=1.1)
        self.at("size is not sequence")
        q = T("?", 40, RED, weight=BOLD).move_to([-0.35, 0.25, 0])
        self.play(FadeIn(q), run_time=0.5)
        breathe(q, 0.15, 2.4)
        self.at("Screening changes the odds")
        cap = caption("Matching size narrows candidates; it is not proof.", color=TEXT)
        self.play(FadeOut(samples), FadeOut(tubes), FadeIn(cap), run_time=0.7)
        self.finish()


class S09Sequence(FilmScene):
    def construct(self):
        p = plasmid([0, 0.35, 0], 2.0, insert=True, question=True)
        self.play(FadeIn(p), run_time=0.7)
        self.at("Sequence both junctions")
        seqmap = sequence_map([0, 0.35, 0], colored=False)
        self.play(FadeOut(p), run_time=0.45)
        self.play(FadeIn(seqmap, shift=RIGHT * 0.2), run_time=0.75)
        scan = Triangle(color=GREEN, stroke_width=4, fill_color=GREEN,
                        fill_opacity=0.7).scale(0.18).rotate(PI)
        scan.move_to([seqmap[0].get_left()[0] + 0.12, 1.25, 0])
        self.at("test the bases and orientation")
        self.play(FadeIn(scan), run_time=0.3)
        self.play(scan.animate.move_to([seqmap[2].get_right()[0] - 0.12, 1.25, 0]),
                  run_time=2.0, rate_func=linear)
        self.at("correct sequence supports")
        for block in seqmap:
            self.play(block[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.18),
                      block[1].animate.set_color(GREEN), run_time=0.35)
        self.play(FadeOut(scan), run_time=0.2)
        self.at("Expression is a separate question")
        promoter = boxed_label("promoter", GREY, size=28).move_to([-2.1, -2.0, 0])
        lamp = VGroup(Circle(radius=0.55, color=GREY, stroke_width=4,
                             fill_color=BG, fill_opacity=0.92),
                      T("?", 36, RED, weight=BOLD)).move_to([0.1, -2.0, 0])
        expr = T("expression?", 28, GREY).move_to([2.05, -2.0, 0])
        self.play(FadeIn(promoter), FadeIn(lamp), FadeIn(expr), run_time=0.7)
        breathe(lamp[-1], 0.15, 2.5)
        self.at("needs a working promoter")
        self.play(Indicate(promoter, color=GREY, scale_factor=1.04), run_time=0.7)
        self.at("Each result earns only")
        cap = caption("Claim only what the measurement supports.", color=TEXT)
        self.play(FadeIn(cap), run_time=0.7)
        self.finish()


class S10Close(FilmScene):
    def construct(self):
        y = 0.25
        xs = [-5.35, -2.75, -0.15, 2.45, 5.05]
        icons = VGroup()
        ends = VGroup(Line([xs[0] - 0.75, y + 0.2, 0], [xs[0] - 0.05, y + 0.2, 0], color=YELLOW, stroke_width=10),
                      Line([xs[0] + 0.05, y - 0.2, 0], [xs[0] + 0.75, y - 0.2, 0], color=YELLOW, stroke_width=10))
        cells = VGroup(bacterium([xs[1] - 0.35, y, 0], 0.38, True),
                       bacterium([xs[1] + 0.45, y, 0], 0.38, True))
        plate = VGroup(Ellipse(width=1.9, height=1.1, color=GREY, stroke_width=3).move_to([xs[2], y, 0]),
                       Dot([xs[2] - 0.35, y, 0], radius=0.16, color=GREEN),
                       Dot([xs[2] + 0.35, y + 0.15, 0], radius=0.16, color=GREEN))
        mini_gel = VGroup(RoundedRectangle(width=1.6, height=1.9, corner_radius=0.1, color=GREY, stroke_width=3).move_to([xs[3], y, 0]),
                          Line([xs[3] - 0.35, y + 0.3, 0], [xs[3] + 0.35, y + 0.3, 0], color=GREEN, stroke_width=7),
                          Line([xs[3] - 0.35, y - 0.4, 0], [xs[3] + 0.35, y - 0.4, 0], color=GREEN, stroke_width=7))
        seq = VGroup(*[Rectangle(width=0.55, height=0.8, color=GREEN, stroke_width=3,
                                 fill_color=GREEN, fill_opacity=0.15).move_to([xs[4] + (i - 1) * 0.58, y, 0])
                       for i in range(3)])
        labels = VGroup(T("join", 26, YELLOW), T("copy", 26, BLUE), T("select", 26, GREEN),
                        T("screen", 26, GREEN), T("sequence", 26, GREEN))
        for lab, x in zip(labels, xs):
            lab.move_to([x, -1.45, 0])
        self.at("chain now makes sense")
        self.play(FadeIn(labels), run_time=0.7)
        self.at("Compatible ends create")
        self.play(FadeIn(ends), run_time=0.7); icons.add(ends)
        self.at("Transformation and growth")
        self.play(FadeIn(cells), run_time=0.7); icons.add(cells)
        self.at("Selection removes")
        self.play(FadeIn(plate), run_time=0.7); icons.add(plate)
        self.at("Screening narrows")
        self.play(FadeIn(mini_gel), run_time=0.7); icons.add(mini_gel)
        self.at("Sequencing tests")
        self.play(FadeIn(seq), run_time=0.7); icons.add(seq)
        line = VMobject(color=GREEN, stroke_width=7)
        line.set_points_as_corners([[xs[0], -2.2, 0], [xs[1], -2.2, 0], [xs[2], -2.2, 0],
                                    [xs[3], -2.2, 0], [xs[4], -2.2, 0]])
        uncertainty = T("uncertainty", 28, RED).move_to([0, 2.75, 0])
        self.play(FadeIn(uncertainty), Create(line), run_time=1.2)
        self.at("Cloning succeeds by combining")
        verified = plasmid([0, 0.25, 0], 2.0, insert=True, question=False)
        badge = T("verified construct", 32, GREEN).move_to([0, -2.2, 0])
        self.play(FadeOut(labels), FadeOut(icons), FadeOut(line), FadeOut(uncertainty), run_time=0.55)
        self.play(FadeIn(verified, scale=0.7), FadeIn(badge), run_time=0.65)
        slow_turn(verified, 0.10)
        self.at("one inference at a time")
        self.play(Indicate(badge, color=GREEN, scale_factor=1.04), run_time=0.7)
        self.finish()


class S11End(EndCard):
    LINE = "Selection finds plasmids; screening narrows candidates;\nsequencing identifies the construct."
