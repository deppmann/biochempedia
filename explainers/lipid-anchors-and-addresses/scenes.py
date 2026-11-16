"""Why one farnesyl tail is usually not enough.

COLOR MAP
  BLUE   proteins
  YELLOW lipid tails / membrane grip
  RED    positive charge
  GREEN  address cues / long residence
  PURPLE enzymes
  GREY   membrane and neutral geometry

All pictures are schematic cartoons; no molecular structures are shown.
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
CYTOSOL = "#202838"
MEM_Y = 1.35
BODY_Y = -0.55


def gentle_drift(mob, amp=0.07, speed=1.7, phase=0.0, sideways=0.025):
    """Small continuous movement that preserves the object's intended centre."""
    clock = [phase]

    def update(m, dt):
        clock[0] += dt
        m.shift(UP * amp * speed * np.cos(speed * clock[0]) * dt)
        m.shift(RIGHT * sideways * speed * np.cos(0.71 * speed * clock[0] + 0.8) * dt)

    mob.add_updater(update)
    return mob



def ambient_motes(n=14, y0=-2.2, y1=0.1, x0=-4.6, x1=4.6, seed=3):
    """Slow drifting motes in the cytosol: honest ambient motion for held beats."""
    rng = np.random.default_rng(seed)
    motes = VGroup()
    for _ in range(n):
        d = Dot(radius=0.2, color=GREY).set_opacity(0.3)
        d.move_to([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
        ph = rng.uniform(0, 6.28)
        sp = rng.uniform(0.5, 0.9)
        clock = [ph]

        def upd(m, dt, clock=clock, sp=sp):
            clock[0] += dt
            m.shift(RIGHT * 1.1 * sp * dt * np.cos(0.8 * clock[0]) + UP * 0.8 * sp * dt * np.sin(1.1 * clock[0]))

        d.add_updater(upd)
        motes.add(d)
    band = Rectangle(width=12.2, height=0.45, stroke_width=0, fill_color=WHITE, fill_opacity=0.07)
    band.move_to([0, -3.0, 0])
    bc = [0.0]

    def sweep(m, dt):
        bc[0] += dt
        m.move_to([0, -3.0 + 3.9 * ((bc[0] / 7.0) % 1.0), 0])

    band.add_updater(sweep)
    motes.add(band)
    motes.set_z_index(-4)
    return motes


def membrane(y=MEM_Y, width=12.4):
    return RoundedRectangle(
        corner_radius=0.12, width=width, height=0.72,
        stroke_color=GREY, stroke_width=3,
        fill_color=GREY, fill_opacity=0.28,
    ).move_to([0, y, 0])


def cytosol_field(top=0.97, bottom=-3.42):
    return RoundedRectangle(
        corner_radius=0.18, width=12.55, height=top - bottom,
        stroke_width=0, fill_color=CYTOSOL, fill_opacity=1,
    ).move_to([0, (top + bottom) / 2, 0]).set_z_index(-5)


def tail(x, body_top=0.08, top=MEM_Y - 0.05, color=YELLOW, width=0.28):
    h = top - body_top
    return RoundedRectangle(
        corner_radius=width / 2, width=width, height=h,
        stroke_color=color, stroke_width=2.5,
        fill_color=color, fill_opacity=0.9,
    ).move_to([x, body_top + h / 2, 0])


def plus_patch(x, y=0.03, scale=1.0):
    pad = RoundedRectangle(
        corner_radius=0.1, width=1.4 * scale, height=0.4 * scale,
        stroke_color=RED, stroke_width=2.5, fill_color=RED, fill_opacity=0.85,
    ).move_to([x, y, 0])
    marks = VGroup(*[
        T("+", 25, BG, weight=BOLD).move_to([x + dx * scale, y, 0])
        for dx in (-0.44, 0, 0.44)
    ])
    return VGroup(pad, marks)


def ras(x=0, name="Ras", y=BODY_Y, contacts=1, patch=False, scale=1.0):
    """The carried Ras block. Contacts are rebuilt at identical landmarks."""
    body = RoundedRectangle(
        corner_radius=0.36 * scale, width=2.55 * scale, height=1.2 * scale,
        stroke_color=BLUE, stroke_width=4,
        fill_color=BLUE, fill_opacity=0.22,
    ).move_to([x, y, 0])
    label = T(name, 30, BLUE, weight=BOLD).move_to(body)
    top = body.get_top()[1]
    tails = VGroup()
    offsets = {-1: (-0.62,), 0: (), 1: (-0.62,), 2: (-0.62, 0.62), 3: (-0.75, 0, 0.75)}[contacts]
    for dx in offsets:
        tails.add(tail(x + dx * scale, top, MEM_Y - 0.05, width=0.28 * scale))
    g = VGroup(tails, body, label)
    g.body, g.label, g.tails = body, label, tails
    if patch:
        pg = plus_patch(x + 0.22 * scale, top + 0.30, scale)
        g.add(pg)
        g.patch = pg
    return g


def negative_lipids(x0=-1.8, x1=1.8, y=MEM_Y - 0.39):
    return VGroup(*[T("−", 29, RED, weight=BOLD).move_to([x, y, 0])
                    for x in np.linspace(x0, x1, 6)])


def schematic_world(protein=None, question=None):
    """The original carried membrane world used throughout the film."""
    protein = protein or ras()
    world = VGroup(cytosol_field(), membrane(), protein)
    world.add(T("cytosol", 28, TEXT).move_to([-5.25, -2.70, 0]))
    world.add(scope_tag("schematic"))
    if question:
        world.add(fit_text(question, max_w=8.8, size=34, color=GOLD).move_to([0, -2.55, 0]))
    return world


def time_strip(long=False, y=-2.15):
    axis = Line([-4.8, y, 0], [4.8, y, 0], color=GREY, stroke_width=4)
    ticks = VGroup(*[Line([x, y - 0.13, 0], [x, y + 0.13, 0], color=GREY, stroke_width=3)
                     for x in (-3.5, -0.8, 1.9)])
    visits = VGroup()
    if long:
        visits.add(Line([-3.9, y + 0.34, 0], [4.2, y + 0.34, 0], color=GREEN, stroke_width=10))
    else:
        for x in (-3.5, -0.8, 1.9):
            visits.add(Line([x - 0.3, y + 0.34, 0], [x + 0.3, y + 0.34, 0], color=YELLOW, stroke_width=10))
    label = T("membrane visits", 28, TEXT).move_to([0, y - 0.48, 0])
    return VGroup(axis, ticks, visits, label)


PREDICT_QUESTION = "Will a second contact make visits brief or much longer?"


def predict_world(with_card=True):
    r = ras(y=-0.68)
    world = schematic_world(r)
    strip = time_strip(False, -1.92)
    slot = DashedVMobject(
        RoundedRectangle(corner_radius=0.13, width=0.34, height=1.25).move_to([0.62, 0.64, 0]),
        num_dashes=20,
    ).set_color(GOLD).set_stroke(width=3)
    qmark = T("?", 42, GOLD, weight=BOLD).move_to(slot)
    g = VGroup(world, strip, slot, qmark)
    gentle_drift(r, amp=0.035, speed=1.8)
    if with_card:
        g.add(question_card(PREDICT_QUESTION, y=-3.23, max_w=10.0))
    return g


def cases_world():
    """The same three Ras cases, used unchanged in the case and control scenes."""
    mem = membrane()
    field = cytosol_field()
    n = ras(-4.25, "N-Ras", contacts=2, scale=0.72)
    h = ras(-1.25, "H-Ras", contacts=3, scale=0.72)
    k = ras(3.75, "K-Ras4B", contacts=1, patch=True, scale=0.86)
    divider = DashedLine([1.25, -2.45, 0], [1.25, 2.72, 0], color=GREY, stroke_width=2)
    left = T("farnesyl + palmitate", 30, YELLOW, weight=BOLD).move_to([-2.8, 2.55, 0])
    right = T("farnesyl + positive patch", 30, RED, weight=BOLD).move_to([3.9, 2.55, 0])
    return VGroup(field, mem, divider, n, h, k, left, right, scope_tag("schematic")), n, h, k


def cell_loop_world():
    cell = Ellipse(width=11.3, height=6.25, color=GREY, stroke_width=3,
                   fill_color=CYTOSOL, fill_opacity=0.6).move_to([0, -0.05, 0])
    golgi = VGroup(*[
        Arc(radius=0.55 + i * 0.22, start_angle=-1.15, angle=2.3,
            color=GREEN, stroke_width=6).stretch(1.6, 0).move_to([-3.0, 0.2, 0])
        for i in range(3)
    ])
    glabel = T("Golgi", 30, GREEN, weight=BOLD).move_to([-3.0, -1.18, 0])
    pm = T("plasma membrane", 28, TEXT).move_to([0, 3.42, 0])
    loop = VMobject(color=GREY, stroke_width=3).set_points_smoothly([
        [-3.0, 0.9, 0], [-0.8, 2.25, 0], [3.5, 1.55, 0], [3.6, -1.35, 0],
        [0.4, -2.45, 0], [-2.6, -1.55, 0], [-3.0, 0.9, 0],
    ])
    return VGroup(cell, golgi, glabel, pm, scope_tag("schematic")), loop


class S00Hook(SpokenScene):
    def construct(self):
        r = ras(0, contacts=0, y=-0.65)
        world = schematic_world(r)
        no_tm = VGroup(
            DashedLine([0.9, 0.1, 0], [0.9, 2.35, 0], color=BLUE, stroke_width=4),
            Line([0.48, 1.02, 0], [1.32, 1.86, 0], color=RED, stroke_width=8),
            Line([0.48, 1.86, 0], [1.32, 1.02, 0], color=RED, stroke_width=8),
        )
        question = fit_text("What keeps Ras at the inner face?", max_w=8.8, size=38, color=GOLD).move_to([0, -2.55, 0])
        self.play(FadeIn(world), run_time=0.7)
        self.at("no segment")
        self.play(Create(no_tm), run_time=0.8)
        self.at("What keeps")
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.6)
        first = T("1  attach lipid", 30, YELLOW).move_to([-3.1, 2.55, 0])
        second = T("2  stay in bilayer", 30, GREEN).move_to([3.0, 2.55, 0])
        self.at("two parts")
        self.play(FadeOut(no_tm), FadeIn(first), FadeIn(second), run_time=0.8)
        newtail = tail(-0.62, r.body.get_top()[1])
        self.at("lipid must join")
        self.play(GrowFromEdge(newtail, DOWN), run_time=0.9)
        self.remove(newtail)
        r.tails.add(newtail)
        gentle_drift(r.tails, amp=0.025, speed=2.1)
        self.at("remain in a bilayer")
        self.play(Indicate(newtail, color=TEXT, scale_factor=1.06), run_time=0.9)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Lipids as Anchors and Addresses"
    TITLE = "Why One Farnesyl Tail Is Usually Not Enough"


class S02TwoBonds(SpokenScene):
    def construct(self):
        r = ras(y=-0.62)
        self.add(schematic_world(r), ambient_motes())
        clasp = Circle(0.14, color=PURPLE, stroke_width=6).move_to([-0.62, r.body.get_top()[1], 0])
        cov = T("covalent bond", 32, PURPLE, weight=BOLD).move_to([-3.6, -1.52, 0])
        contact = T("membrane contact", 32, YELLOW, weight=BOLD).move_to([3.5, 2.5, 0])
        self.at("separate two interactions")
        self.play(FadeIn(cov), FadeIn(contact), run_time=0.8)
        self.at("covalent bond")
        self.play(Create(clasp), Indicate(r.tails, color=PURPLE, scale_factor=1.04), run_time=0.8)
        self.at("much weaker")
        self.play(Indicate(r.tails, color=YELLOW, scale_factor=1.08), run_time=0.7)
        self.at("repeatedly enters")
        for _ in range(2):
            self.play(r.animate.shift(DOWN * 1.25), run_time=0.85)
            self.play(r.animate.shift(UP * 1.25), run_time=0.85)
        steady = T("clasp stays closed", 30, PURPLE).move_to([3.65, -2.45, 0])
        self.at("covalent bond can last")
        self.play(FadeIn(steady), Indicate(clasp, color=TEXT), run_time=0.8)
        self.at("does not mean")
        self.play(r.animate.shift(DOWN * 1.25), run_time=1.0)
        self.play(r.animate.shift(UP * 1.25), run_time=1.0)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        r = ras(y=-0.68)
        base = schematic_world(r)
        strip = time_strip(False, -1.92)
        self.add(base)
        self.at("sample the membrane")
        self.play(FadeIn(strip), run_time=0.7)
        for _ in range(2):
            self.play(r.animate.shift(DOWN * 0.48), run_time=0.45)
            self.play(r.animate.shift(UP * 0.48), run_time=0.45)
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.13, width=0.34, height=1.25)
                              .move_to([0.62, 0.64, 0]), num_dashes=20).set_color(GOLD).set_stroke(width=3)
        qm = T("?", 42, GOLD, weight=BOLD).move_to(slot)
        self.at("second contact")
        self.play(FadeIn(slot), FadeIn(qm), run_time=0.6)
        q = question_card(PREDICT_QUESTION, y=-3.23, max_w=10.0)
        self.at("Will its visits")
        self.play(FadeIn(q), run_time=0.6)
        gentle_drift(r, amp=0.035, speed=1.8)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = PREDICT_QUESTION
    SECONDS = 4.5
    CARD = {"y": -3.23, "max_w": 10.0}
    RING_AT = (-5.85, 2.55, 0)

    def backdrop(self):
        return predict_world(False)


class S05Reveal(SpokenScene):
    def construct(self):
        r = ras(y=-0.68)
        world = schematic_world(r)
        short = time_strip(False, -1.92)
        self.add(world, short, ambient_motes(seed=5))
        long = time_strip(True, -1.92)
        second = tail(0.62, r.body.get_top()[1])
        self.at("visits become longer")
        self.play(ReplacementTransform(short, long), GrowFromEdge(second, DOWN), run_time=1.1)
        self.remove(second)
        r.tails.add(second)
        self.at("Both contacts")
        self.play(r.tails[0].animate.shift(DOWN * 0.12), run_time=0.45, rate_func=there_and_back)
        self.play(r.tails[1].animate.shift(DOWN * 0.12), run_time=0.45, rate_func=there_and_back)
        rare = T("both must release", 32, GREEN, weight=BOLD).move_to([0, 2.52, 0])
        self.at("coincidence is rarer")
        self.play(FadeIn(rare), run_time=0.6)
        self.at("second lipid")
        self.play(Indicate(second, color=TEXT, scale_factor=1.08), run_time=0.8)
        patch = plus_patch(0.22, r.body.get_top()[1] + 0.30)
        neg = negative_lipids(1.15, 2.55, y=MEM_Y - 0.54)
        self.at("positive patch")
        self.play(FadeOut(second), FadeIn(patch), FadeIn(neg), run_time=0.8)
        self.at("negative lipids")
        self.play(patch.animate.shift(UP * 0.08), neg.animate.shift(DOWN * 0.04),
                  run_time=0.7, rate_func=there_and_back)
        self.finish()


class S06RasCases(SpokenScene):
    def construct(self):
        world, n, h, k = cases_world()
        base = VGroup(world[0], world[1], world[2], world[-1])
        self.add(base)
        self.at("H Ras and N Ras")
        self.play(FadeIn(world[3]), FadeIn(world[4]), FadeIn(world[6]), run_time=1.0)
        self.at("K Ras 4B")
        self.play(FadeIn(world[5]), FadeIn(world[7]), run_time=0.9)
        self.at("farnesyl supplies")
        self.play(Indicate(n.tails[0], color=TEXT), Indicate(h.tails[0], color=TEXT),
                  Indicate(k.tails[0], color=TEXT), run_time=1.0)
        self.at("not identical addresses")
        self.play(world[6].animate.set_opacity(0.55), world[7].animate.set_opacity(0.55),
                  run_time=0.7, rate_func=there_and_back)
        self.at("two ways")
        self.play(h.animate.shift(UP * 0.08), k.animate.shift(UP * 0.08), run_time=0.8, rate_func=there_and_back)
        self.finish()


class S07Energy(SpokenScene):
    def construct(self):
        left = ras(-4.65, "Ras", contacts=2, scale=0.8)
        self.add(cytosol_field(), membrane(), left, scope_tag("computed"), ambient_motes(n=8, x0=-4.8, x1=-1.5, y0=-2.2, y1=0.0, seed=7))
        plot = Plot(
            box=(-0.6, 5.75, -1.55, 2.2), xr=(0, 1.6), yr=(1, 16),
            xticks=[(0.7, "0.7"), (1.4, "1.4")], yticks=[(1, "1"), (10, "10")],
            xlabel="free-energy contribution (kcal/mol)", ylabel="equilibrium effect",
            size=24, label_size=25,
        )
        # At room temperature, factor = exp(delta-G / RT), RT about 0.593 kcal/mol.
        fn = lambda dg: np.exp(dg / 0.593)
        tracker = ValueTracker(0.02)
        curve = plot.live_curve(fn, tracker, color=GREEN, width=7)
        dot = plot.dot(lambda: tracker.get_value(), lambda: fn(tracker.get_value()), color=GREEN)
        self.at("change so large")
        self.play(FadeIn(plot), run_time=0.7)
        self.add(curve, dot)
        self.at("free energy contributions add")
        self.play(left.tails[0].animate.set_stroke(width=6), left.tails[1].animate.set_stroke(width=6),
                  run_time=0.8, rate_func=there_and_back)
        self.at("grows exponentially")
        self.play(tracker.animate.set_value(1.4), run_time=3.2, rate_func=linear)
        mark = VGroup(plot.vline(1.4, color=YELLOW), plot.hline(10.6, color=GREEN),
                      T("1.4 kcal/mol → about 10-fold", 28, TEXT).move_to([3.05, 3.18, 0]))
        self.at("thermodynamic effect")
        self.play(FadeIn(mark), run_time=0.8)
        self.at("computed curve")
        self.play(Indicate(curve, color=TEXT, scale_factor=1.0), run_time=1.0)
        self.finish()


class S08Control(SpokenScene):
    def construct(self):
        world, n, h, k = cases_world()
        self.add(world)
        strong = caption("two contacts: strong hold", color=GREEN)
        self.at("creates control")
        self.play(FadeIn(strong), run_time=0.6)
        self.at("Remove palmitate")
        self.play(FadeOut(h.tails[-1]), run_time=0.8)
        self.at("weaken a positive patch")
        self.play(k.patch.animate.set_opacity(0.18), run_time=0.8)
        weak = caption("one contact: weak sampling", color=YELLOW)
        self.at("strong hold becomes weak")
        self.play(swap(strong, weak), h.animate.shift(DOWN * 0.35), k.animate.shift(DOWN * 0.35), run_time=1.0)
        self.at("switch in location")
        self.play(h.animate.shift(UP * 0.35), k.animate.shift(UP * 0.35), run_time=0.7)
        self.play(h.animate.shift(DOWN * 0.35), k.animate.shift(DOWN * 0.35), run_time=0.7)
        self.at("without breaking")
        self.play(Indicate(h.tails[0], color=TEXT), Indicate(k.tails[0], color=TEXT), run_time=0.9)
        self.finish()


class S09Palmitate(SpokenScene):
    def construct(self):
        world, path = cell_loop_world()
        self.add(world)
        h = ras(-3.0, "H-Ras", y=1.62, contacts=0, scale=0.72)
        farnesyl = tail(-3.42, h.body.get_top()[1], top=h.body.get_top()[1] + 0.8, width=0.2)
        h.tails.add(farnesyl)
        enzyme = boxed_label("enzyme", PURPLE, size=28, fill_opacity=0.22).move_to([0, -1.55, 0])
        second = tail(-2.55, h.body.get_top()[1], top=h.body.get_top()[1] + 0.8, width=0.2)
        self.at("remove and replace")
        self.play(FadeIn(h), FadeIn(enzyme), run_time=0.8)
        self.at("goes on mainly")
        self.play(GrowFromEdge(second, DOWN), run_time=0.8)
        self.remove(second)
        h.tails.add(second)
        vesicle = Circle(0.5, color=GREY, fill_color=GREY, fill_opacity=0.18).move_to([-0.7, 2.08, 0])
        self.at("Golgi")
        self.play(FadeOut(enzyme), h.animate.move_to([-0.7, 0.82, 0]), FadeIn(vesicle), run_time=1.4)
        self.play(h.animate.move_to([3.35, 0.72, 0]), vesicle.animate.move_to([3.35, 1.82, 0]), run_time=2.0)
        self.at("come off on any membrane")
        self.play(FadeOut(second), run_time=0.8)
        self.at("Pharnacil remains")
        self.play(Indicate(h.tails[0], color=TEXT), run_time=0.8)
        self.at("tightly trapped")
        self.play(h.animate.shift(UP * 0.18), run_time=0.7, rate_func=there_and_back)
        self.at("loosely sampling")
        self.play(h.animate.move_to([0.3, -2.0, 0]), run_time=1.8)
        self.play(h.animate.shift(LEFT * 1.0), run_time=0.7)
        self.play(h.animate.shift(RIGHT * 2.0), run_time=0.9)
        self.at("changes residence")
        self.play(h.animate.shift(LEFT * 1.0), run_time=0.8)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        one = ras(-2.5, "H-Ras", contacts=1)
        two = ras(2.5, "H-Ras", contacts=2)
        tag = scope_tag("membrane targeting")
        self.add(cytosol_field(), membrane(), one, two, tag, ambient_motes(seed=9))
        grip = boxed_label("GRIP", YELLOW, size=38, fill_opacity=0.2).move_to([-2.5, 2.55, 0])
        address = boxed_label("ADDRESS", GREEN, size=38, fill_opacity=0.04).move_to([2.5, 2.55, 0])
        self.at("grip half")
        self.play(FadeIn(grip), FadeIn(address), run_time=0.8)
        self.at("grip address or both")
        self.play(grip.animate.set_fill(YELLOW, 0.32), address.animate.set_stroke(GREEN, 4), run_time=0.9)
        self.at("within this membrane")
        self.play(Indicate(tag, color=TEXT), run_time=0.5)
        short = T("brief encounter", 30, YELLOW).move_to([-2.5, -2.35, 0])
        long = T("regulated residence", 30, GREEN).move_to([2.5, -2.35, 0])
        self.at("second signal")
        self.play(FadeIn(short), FadeIn(long), run_time=0.7)
        self.at("brief encounter")
        self.play(one.animate.shift(DOWN * 0.55), run_time=0.65)
        self.play(one.animate.shift(UP * 0.55), run_time=0.65)
        self.at("regulated membrane residence")
        self.play(two.animate.shift(UP * 0.08), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        cards = VGroup(
            boxed_label("1  membrane contact?", YELLOW, size=30, fill_opacity=0.15),
            boxed_label("2  strengthening signal?", GREEN, size=30, fill_opacity=0.15),
            boxed_label("3  removal or opposition?", PURPLE, size=30, fill_opacity=0.15),
        ).arrange(DOWN, buff=0.38).move_to([-2.2, 0.2, 0])
        self.at("three questions")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cards], lag_ratio=0.22), run_time=1.3)
        for phrase, card in (("Which contact", cards[0]), ("Which additional", cards[1]), ("what can remove", cards[2])):
            self.at(phrase)
            self.play(Indicate(card, color=TEXT, scale_factor=1.03), run_time=0.8)
        r = ras(3.75, contacts=2, scale=0.95)
        mem = RoundedRectangle(corner_radius=0.12, width=4.8, height=0.72, stroke_color=GREY,
                               stroke_width=3, fill_color=GREY, fill_opacity=0.28).move_to([3.75, MEM_Y, 0])
        self.at("answers predict")
        self.play(FadeIn(mem), FadeIn(r), run_time=1.0)
        self.at("switch that can change")
        self.play(r.tails[-1].animate.set_opacity(0.1), r.animate.shift(DOWN * 0.35), run_time=1.0)
        self.play(r.animate.shift(UP * 0.35), r.tails[-1].animate.set_opacity(1), run_time=1.0)
        self.finish()


class S12End(EndCard):
    LINE = "A second signal turns weak membrane contact into a regulated hold."
