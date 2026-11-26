"""How the Timer Breaks, chapter 2 of GTPase Switches: The Timer.

COLOR MAP from chapter 1: slate = GDP/off, gold = GTP/on,
teal = GEF/loading, clay-red = GAP/cutting. Blue is the membrane.
Purple marks cyclic AMP and downstream messenger clearance.
The traces model one loaded interval; their horizontal axis has no time units.
"""
from bp_parts import *
from bp_style import EndCard


SLATE = "#7F8998"
CLAY = "#C96E5C"
MESSENGER = "#B69BE3"
SWITCH_AT = (-1.2, -0.65, 0)
LOAD_AT, NORMAL_CUT, EARLY_CUT, LONG_CUT = 1.0, 5.65, 3.65, 11.0
TRACE_BOX = (-2.65, 5.8, 0.88, 2.08)
QUESTION = "What happens to the active interval?"
OPTIONS = ("longer", "shorter", "unchanged")
QUESTION_CARD = dict(y=-3.22, size=32, chip_size=30, max_w=10.0, color=TEXT)
LESSON_TITLE = "GTPase Switches: The Timer"


def membrane():
    return RoundedRectangle(
        width=12.4, height=0.42, corner_radius=0.18, stroke_color=BLUE,
        fill_color=BLUE, fill_opacity=0.28, stroke_width=3,
    ).move_to([0, 2.55, 0])


def receptor(on=True):
    color = TEAL if on else SLATE
    stalk = Line([-4.35, 2.5, 0], [-4.35, 1.3, 0], color=color, stroke_width=9)
    cup = Arc(radius=0.62, start_angle=PI, angle=PI, arc_center=[-4.35, 1.25, 0],
              color=color, stroke_width=9)
    ligand = Dot([-4.35 if on else -5.35, 3.15, 0], radius=0.22, color=TEAL)
    if not on:
        ligand.set_opacity(0.34)
    return VGroup(stalk, cup, ligand)


def protein_body(on, at=SWITCH_AT, width=None):
    color = GOLD if on else SLATE
    return RoundedRectangle(
        width=width or (4.4 if on else 3.8), height=2.55, corner_radius=0.34,
        stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.35,
    ).move_to(at)


def nucleotide(kind, at):
    loaded = kind != "GDP"
    color = GOLD if loaded else SLATE
    width = 1.94 if kind == "analogue" else 1.26
    core = boxed_label(kind, color, size=31, box=(width, 0.62), pad=0.11, fill_opacity=0.30)
    core.label.set_color(TEXT)
    tabs = VGroup(*[
        Square(0.27, color=color, stroke_width=3, fill_color=color, fill_opacity=0.45)
        for _ in range(3 if loaded else 2)
    ]).arrange(RIGHT, buff=0.12).next_to(core, DOWN, buff=0.13)
    token = VGroup(core, tabs).move_to(at)
    token.tabs = tabs
    return token


def switch(name="GTPase", on=True, kind=None, at=SWITCH_AT, width=None, ras=False):
    """The chapter-one protein and pocket, optionally tethered to the membrane."""
    position = np.asarray(at)
    color = GOLD if on else SLATE
    body = protein_body(on, at, width)
    nameplate = T(name, 34, color, weight=BOLD).move_to(position + UP * 0.83)
    token = nucleotide(kind or ("GTP" if on else "GDP"), position + DOWN * 0.33)
    group = VGroup(body, nameplate, token)
    group.body, group.nameplate, group.token = body, nameplate, token
    if ras:
        # Leave the activity plot unobstructed. The tether bends out to the membrane.
        edge = body.get_top() + LEFT * (body.width / 2 - 0.35)
        tether = Line(edge + UP * 0.02, [edge[0], 2.32, 0], color=BLUE, stroke_width=5)
        group.add_to_back(tether)
    return group


def schematic(at=(4.74, 3.18, 0)):
    return scope_tag(size=28, color=GREY).move_to(at)


def trace_plot(box=TRACE_BOX):
    return Plot(box=box, xr=(0, 10), yr=(0, 1), xticks=(), yticks=(),
                xlabel="", ylabel="", color=GREY, stroke=3)


def activity(plot, front, cut, shade=True):
    """Compute a two-state trace from its loading time and cutting time."""
    off, on = 0.13, 0.89
    if cut <= LOAD_AT:
        return VGroup(plot.curve(lambda t: off, x1=front, color=SLATE, width=5, n=2))
    start, end = min(LOAD_AT, front), min(cut, front)
    before = plot.curve(lambda t: off, x1=start, color=SLATE, width=5, n=2)
    result = VGroup(before)
    if front > LOAD_AT:
        corners = [
            plot.pt(LOAD_AT, off), plot.pt(LOAD_AT, on),
            plot.pt(end, on), plot.pt(end, off),
        ]
        if shade:
            result.add(Polygon(*corners, stroke_width=0, fill_color=GOLD, fill_opacity=0.28))
        result.add(VMobject(stroke_color=GOLD, stroke_width=7)
                   .set_points_as_corners(corners if front > cut else corners[:3]))
    if front > cut:
        result.add(plot.curve(lambda t: off, x0=cut, x1=front, color=SLATE, width=5, n=2))
    return result


def trace(front=0.35, cut=LONG_CUT, box=TRACE_BOX, tagged=True):
    axis = trace_plot(box)
    live = always_redraw(lambda: activity(
        axis, front.get_value() if isinstance(front, ValueTracker) else front,
        cut.get_value() if isinstance(cut, ValueTracker) else cut,
    ))
    parts = VGroup(axis, live)
    if tagged:
        parts.add(schematic())
    return parts


def loading_arrow(color=TEAL):
    return Arrow([-4.28, 0.49, 0], [-3.45, -0.18, 0], buff=0.11,
                 color=color, stroke_width=6, tip_length=0.21)


def cutting_arrow():
    return Arrow([1.18, -1.1, 0], [3.72, -1.1, 0], buff=0.09,
                 color=CLAY, stroke_width=7, tip_length=0.23)


def chevron(at, direction=1, size=0.25):
    c = np.asarray(at)
    return VMobject(stroke_color=CLAY, stroke_width=6).set_points_as_corners([
        c + [-size * direction, size, 0], c, c + [-size * direction, -size, 0],
    ])


def cutter(at):
    return Triangle(color=CLAY, stroke_width=3, fill_color=CLAY, fill_opacity=0.72
                    ).stretch_to_fit_width(0.37).stretch_to_fit_height(0.5).rotate(-PI / 2).move_to(at)


def stop_mark(at, color=CLAY):
    return Line(UP * 0.24, DOWN * 0.24, color=color, stroke_width=8).move_to(at)


def target(on=True, label="target", center=(4.35, -0.65, 0), radius=1.15):
    level = ValueTracker(0.82 if on else 0.18)
    gauge = dial(level, center, radius=radius, label=label,
                 color=GOLD if on else SLATE, fmt="ON" if on else "OFF", size=32)
    return gauge


def change_state(scene, current, replacement, *extra, run_time=1.2):
    """Change the protein, with each old label gone before its successor arrives."""
    scene.play(
        ReplacementTransform(current.body, replacement.body),
        swap(current.nameplate, replacement.nameplate, run_time=run_time),
        swap(current.token, replacement.token, run_time=run_time),
        *extra, run_time=run_time,
    )


def release_tab(scene, token, *extra, run_time=1.3):
    tab = token.tabs[-1]
    token.tabs.remove(tab)
    scene.add(tab)
    scene.play(FadeOut(tab, shift=DOWN * 0.33 + RIGHT * 0.54),
               *extra, run_time=run_time)
    scene.remove(tab)


def dial_strokes(gauge, opacity):
    """Dim the dial's strokes without filling its transparent arc."""
    for mark in gauge[:3]:
        mark.clear_updaters()
    return gauge[:3].animate.set_stroke(opacity=opacity)


class S00Hook(SpokenScene):
    def construct(self):
        front = ValueTracker(1.12)
        protein = switch()
        self.at("the first film")
        self.add(membrane(), receptor(), protein, trace(front, NORMAL_CUT))
        self.play(front.animate.set_value(5.60), run_time=3.95, rate_func=linear)
        self.at("cutting turned")
        release_tab(self, protein.token, run_time=0.65)
        off = switch(on=False)
        change_state(self, protein, off, front.animate.set_value(7.0), run_time=1.2)

        self.at("if cutting ends")
        on = switch()
        change_state(self, off, on, run_time=1.2)
        stem = Line([1.18, -0.66, 0], [2.6, -0.66, 0], color=CLAY, stroke_width=7)
        self.at("what happens")
        self.play(Create(stem), run_time=0.75)
        blocked = Arrow([2.6, -0.66, 0], [4.25, -0.23, 0], buff=0,
                        color=CLAY, stroke_width=6)
        fast = Arrow([2.6, -0.66, 0], [4.25, -2.06, 0], buff=0,
                     color=CLAY, stroke_width=6)
        barrier = stop_mark([4.24, -0.23, 0])
        self.at("blocks the cut")
        self.play(GrowArrow(blocked), run_time=0.62)
        self.play(FadeIn(barrier), FadeIn(T("blocked", 30, CLAY).move_to([5.32, -0.25, 0])),
                  run_time=0.4)
        self.at("speeds it up")
        self.play(GrowArrow(fast), run_time=0.65)
        speed = VGroup(chevron([4.55, -2.26, 0], size=0.16),
                       chevron([4.77, -2.26, 0], size=0.16))
        self.play(Create(speed),
                  FadeIn(T("accelerated", 30, CLAY).move_to([4.92, -2.85, 0])), run_time=0.75)
        self.at("same colors")
        self.play(on.body.animate.set_fill(GOLD, opacity=0.48), run_time=1.1)
        self.finish()


class S01Title(TitleCard):
    TITLE = "How the Timer Breaks"
    LESSON = LESSON_TITLE

    def construct(self):
        front = ValueTracker(5.25)
        self.add(membrane(), receptor(), switch(), trace(front, tagged=False),
                 schematic([4.85, 0.48, 0]))
        title = T(self.TITLE, 51, TEXT, font=TITLE_FONT).move_to([0.95, 3.3, 0])
        lesson = T(self.LESSON, 29, GREY).move_to([0.0, -2.91, 0])
        self.play(FadeIn(title), FadeIn(lesson), front.animate.set_value(7.2),
                  run_time=0.53, rate_func=linear)
        self.play(front.animate.set_value(10), run_time=1.40, rate_func=linear)


class S02Baseline(SpokenScene):
    def construct(self):
        front = ValueTracker(0.35)
        off, on = switch(on=False), switch()
        rec = receptor(False)
        self.at("begin with")
        self.add(membrane(), rec, off, trace(front, NORMAL_CUT))
        self.play(front.animate.set_value(0.96), run_time=2.6, rate_func=linear)
        self.at("teal loading event")
        load = loading_arrow()
        self.play(Transform(rec, receptor()), GrowArrow(load), run_time=0.9)
        self.at("starts a gold")
        change_state(self, off, on, front.animate.set_value(2.2), run_time=1.1)
        self.play(front.animate.set_value(4.1), run_time=1.3, rate_func=linear)
        self.at("intrinsic cutting")
        blade = cutter([-0.35, -2.83, 0]).rotate(PI / 2)
        self.play(FadeOut(load), FadeIn(blade), front.animate.set_value(4.85), run_time=0.55)
        self.play(blade.animate.move_to([-0.66, -1.65, 0]),
                  front.animate.set_value(5.62), run_time=1.35, rate_func=linear)
        self.at("final phosphate")
        release_tab(self, on.token, FadeOut(blade), run_time=1.1)
        self.at("leaving GDP")
        off = switch(on=False)
        change_state(self, on, off, front.animate.set_value(7.7), run_time=1.45)
        self.at("neutral reference")
        baseline = T("ordinary cycle", 31, TEXT).move_to([0, -2.93, 0])
        self.play(FadeIn(baseline), front.animate.set_value(10), run_time=2.1, rate_func=linear)
        self.finish()


class S03Analogue(SpokenScene):
    def construct(self):
        front = ValueTracker(0.35)
        off, on = switch(on=False), switch(kind="analogue")
        rec = receptor()
        free = nucleotide("GTP", [4.5, -0.65, 0])
        incoming = nucleotide("analogue", [4.5, -0.65, 0])
        for token in (free, incoming):
            token.scale(1.4)
            token[0].box.set_fill(GOLD, opacity=0.60)
        self.at("replace GTP")
        self.add(membrane(), rec, off, trace(front), free)
        self.play(swap(free, incoming, run_time=1.35), run_time=1.35)
        self.at("the protein can bind")
        self.play(incoming.animate.move_to([2.54, -0.98, 0]),
                  front.animate.set_value(0.9), run_time=1.5)
        self.at("cannot cut")
        blade = cutter([-0.30, -2.75, 0]).rotate(PI / 2)
        self.play(FadeOut(off.token, shift=DOWN * 0.55), run_time=0.6)
        self.play(incoming.animate.scale(1 / 1.4).shift(LEFT * 0.53), run_time=1.25)
        load = loading_arrow()
        self.at("loading still")
        self.play(GrowArrow(load), ReplacementTransform(off.body, on.body),
                  swap(off.nameplate, on.nameplate, run_time=1.7),
                  swap(incoming, on.token, run_time=1.7),
                  front.animate.set_value(2.45), run_time=1.7)
        self.at("nothing changes")
        self.play(front.animate.set_value(4.65), run_time=2.4, rate_func=linear)
        self.at("off event fails")
        self.play(FadeOut(load), FadeIn(blade),
                  front.animate.set_value(NORMAL_CUT), run_time=1.1)
        self.play(blade.animate.move_to([-0.70, -1.72, 0]),
                  front.animate.set_value(6.8), run_time=1.4, rate_func=linear)
        self.at("after receptor input")
        self.play(Transform(rec, receptor(False)), front.animate.set_value(10),
                  run_time=2.0, rate_func=linear)
        self.finish()


def messenger_dots(center=(4.35, -2.59, 0), color=MESSENGER):
    return VGroup(*[Dot(radius=0.105, color=color) for _ in range(12)]
                  ).arrange_in_grid(rows=2, cols=6, buff=(0.24, 0.17)).move_to(center)


class S04Toxin(SpokenScene):
    def construct(self):
        front = ValueTracker(1.3)
        gs = switch("Gs alpha")
        cyclase = target(label="adenylyl cyclase")
        self.at("cholera toxin")
        self.add(membrane(), receptor(False), gs, trace(front), cyclase)
        toxin = boxed_label("cholera toxin", CLAY, size=34, fill_opacity=0.40
                            ).move_to([-4.65, -2.72, 0])
        toxin.label.set_color(TEXT)
        self.play(FadeIn(toxin), run_time=0.7)
        self.play(toxin.animate.move_to([-3.85, -2.72, 0]),
                  front.animate.set_value(2.6), run_time=1.35, rate_func=linear)
        self.at("logic through")
        self.play(toxin.animate.move_to([-2.87, -2.72, 0]),
                  front.animate.set_value(3.9),
                  gs.body.animate.set_fill(opacity=0.47), run_time=1.75, rate_func=linear)
        self.at("modification obstructs")
        badge = VGroup(stop_mark([0.44, -1.31, 0]),
                       Arc(radius=0.34, start_angle=-PI / 2, angle=PI,
                           arc_center=[0.39, -1.31, 0], color=CLAY, stroke_width=4))
        self.play(FadeOut(toxin, shift=UP * 0.23), Create(badge),
                  front.animate.set_value(4.8), run_time=1.6, rate_func=linear)
        self.at("alpha's hydrolysis")
        self.play(front.animate.set_value(5.55), run_time=1.45, rate_func=linear)
        self.at("cyclase remains active")
        on_panel = RoundedRectangle(
            width=3.04, height=2.12, corner_radius=0.22, fill_color=GOLD,
            fill_opacity=0.24, stroke_width=0,
        ).move_to([4.35, -0.46, 0]).set_z_index(-1)
        activation = Arrow([1.18, -0.62, 0], [2.82, -0.62, 0], buff=0,
                           color=GOLD, stroke_width=6, tip_length=0.2)
        self.play(FadeIn(on_panel), GrowArrow(activation),
                  front.animate.set_value(6.9), run_time=1.55, rate_func=linear)
        self.at("cyclic amp stays")
        dots = messenger_dots()
        camp = T("cyclic AMP", 30, MESSENGER).move_to([4.35, -3.34, 0])
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.32) for d in dots], lag_ratio=0.23),
                  front.animate.set_value(8.1), run_time=1.65, rate_func=linear)
        self.play(FadeIn(camp), run_time=0.65)
        self.at("timer stalls downstream")
        self.play(front.animate.set_value(10), run_time=2.55, rate_func=linear)
        self.finish()


def predict_card():
    card = question_card(QUESTION, OPTIONS, **QUESTION_CARD)
    width = max(choice[0].width for choice in card.chips)
    height = max(choice[0].height for choice in card.chips)
    for choice in card.chips:
        choice[0].stretch_to_fit_width(width)
        choice[0].stretch_to_fit_height(height)
    card.chips.arrange(RIGHT, buff=0.32).move_to([0.6, 3.33, 0])
    card.rail = SurroundingRectangle(
        card.chips, buff=(0.07, 0.035), corner_radius=0.16, stroke_width=0,
        fill_color=GREY, fill_opacity=0.37,
    ).set_z_index(-1)
    card.add_to_back(card.rail)
    return card


def rgs_block():
    block = boxed_label("RGS", CLAY, size=38, box=(1.94, 1.04), fill_opacity=0.37)
    block.label.set_color(TEXT)
    return block.move_to([3.23, -1.1, 0])


def matched_reference():
    return T("Same starting state", 30, TEXT).move_to([-0.66, -2.7, 0])


def predict_world(front):
    protein = switch("G alpha")
    rgs = rgs_block()
    diagram = VGroup(membrane(), receptor(), protein, trace(front, EARLY_CUT, tagged=False),
                     schematic([4.85, 0.48, 0]), rgs)
    return diagram, protein, rgs


PREDICT_FRONT = 3.25


class S05Predict(SpokenScene):
    def construct(self):
        front = ValueTracker(0.55)
        world, _, rgs = predict_world(front)
        self.at("now add extra")
        self.add(*world[:-1])
        rgs.move_to([5.37, -2.46, 0])
        self.play(FadeIn(rgs), front.animate.set_value(1.02), run_time=1.4, rate_func=linear)
        self.at("already loaded")
        self.play(rgs.animate.move_to([3.23, -1.1, 0]), front.animate.set_value(2.05),
                  run_time=4.1, rate_func=linear)
        self.at("all other parts")
        note = matched_reference()
        self.play(FadeIn(note), front.animate.set_value(2.7), run_time=2.15, rate_func=linear)
        self.at("should its active")
        card = predict_card()
        self.play(FadeIn(card.question), run_time=0.65)
        self.at("grow longer")
        self.play(FadeOut(note), FadeIn(card.chips[0]), run_time=0.85)
        self.at("grow shorter")
        self.play(FadeIn(card.chips[1]), run_time=0.74)
        self.at("stay unchanged")
        self.play(FadeIn(card.chips[2]), front.animate.set_value(2.94),
                  run_time=1.2, rate_func=linear)
        self.play(FadeIn(card.rail), front.animate.set_value(PREDICT_FRONT),
                  run_time=0.86, rate_func=rate_functions.ease_in_cubic)
        self.finish()


class S06Pause(PredictPause):
    SECONDS = 4.5

    def construct(self):
        world, _, _ = predict_world(PREDICT_FRONT)
        self.add(world, predict_card())
        self.wait(self.SECONDS)


class S07Reveal(SpokenScene):
    def construct(self):
        front = ValueTracker(PREDICT_FRONT)
        world, protein, rgs = predict_world(front)
        card = predict_card()
        self.add(*world, card.rail, card.question, *card.chips)
        longer, shorter, unchanged = card.chips
        self.at("shorter")
        self.play(shorter[0].animate.set_fill(CLAY, opacity=0.63).set_stroke(CLAY, width=4),
                  FadeOut(longer), FadeOut(unchanged), run_time=0.65)
        self.at("accelerates cutting")
        self.play(FadeOut(card.question), FadeOut(shorter), FadeOut(card.rail), run_time=0.5)
        path = cutting_arrow().shift(DOWN * 0.88)
        chevrons = VGroup(chevron([1.62, -1.98, 0], size=0.2),
                          chevron([1.89, -1.98, 0], size=0.2))
        self.play(GrowArrow(path), rgs.animate.move_to([2.3, -1.1, 0]), run_time=0.75)
        self.play(FadeIn(chevrons), run_time=0.32)
        self.play(chevrons.animate.shift(RIGHT * 1.3), front.animate.set_value(3.56),
                  rgs.box.animate.set_fill(CLAY, opacity=0.57),
                  run_time=1.23, rate_func=linear)
        families = T("Gi and Gq", 31, CLAY).move_to([2.3, -0.22, 0])
        self.play(FadeIn(families), run_time=0.65)
        self.at("final phosphate leaves")
        off = switch("G alpha", on=False)
        release_tab(self, protein.token, FadeOut(chevrons),
                    front.animate.set_value(5.2), run_time=1.35)
        self.play(protein.body.animate.set_fill(SLATE, opacity=0.35), run_time=0.65)
        self.at("block returns to slate")
        change_state(self, protein, off, front.animate.set_value(7.1), run_time=1.65)
        self.at("family boundary matters")
        self.play(FadeOut(path), front.animate.set_value(10),
                  families.animate.set_color(TEXT),
                  rgs.box.animate.set_fill(CLAY, opacity=0.86), run_time=1.45, rate_func=linear)
        self.at("does not have")
        gs = boxed_label("Gs", SLATE, size=36, box=(1.88, 0.91),
                         fill_opacity=0.41).move_to([4.65, -2.27, 0])
        gs.label.set_color(TEXT)
        note = T("not this RGS target", 30, GREY).move_to([4.32, -3.07, 0])
        self.play(FadeIn(gs), run_time=0.55)
        self.play(FadeIn(note), run_time=0.65)
        self.finish()


def ras_gap(docked=True):
    gap = boxed_label("GAP", CLAY, size=38, box=(2.13, 0.90), fill_opacity=0.48)
    gap.label.set_color(TEXT)
    return gap.move_to([-1.2 if docked else -4.7, -2.55 if docked else -2.85, 0])


def g12v_alignment(offset=True):
    y = -0.62 if offset else -0.98
    return VGroup(
        chevron([0.46, y, 0], size=0.17),
        Line([0.62, -1.17, 0], [0.62, -0.79, 0], color=CLAY, stroke_width=5),
    )


def g12v_world():
    return switch("Ras G12V", ras=True)


class S08G12v(SpokenScene):
    def construct(self):
        front = ValueTracker(1.2)
        ras = g12v_world()
        self.at("raw's g12 v")
        self.add(membrane(), ras, trace(front))
        self.play(front.animate.set_value(4.6), run_time=3.0, rate_func=linear)
        gap = ras_gap(False)
        self.play(FadeIn(gap), run_time=0.65)
        self.at("gap may bind")
        self.play(gap.animate.move_to(ras_gap()),
                  ras.body.animate.set_fill(GOLD, opacity=0.52), run_time=1.02)
        misfit = g12v_alignment()
        self.at("catalytic arrangement fails")
        self.play(Create(misfit[1]), run_time=0.58)
        approaching = g12v_alignment(False)[0]
        self.play(FadeIn(approaching, shift=UP * 0.32), run_time=0.62)
        enlargement = misfit.copy().scale(3.1).move_to([3.65, -0.93, 0])
        self.play(Transform(approaching, misfit[0]), Create(enlargement),
                  run_time=1.25)
        self.at("catalytic failure")
        label = T("catalytic failure", 30, CLAY).move_to([3.78, -2.72, 0])
        self.play(FadeIn(label), front.animate.set_value(6.1), run_time=1.65, rate_func=linear)
        self.at("missing gap")
        self.play(gap[0].animate.set_fill(CLAY, opacity=0.40),
                  front.animate.set_value(6.6), run_time=1.0, rate_func=linear)
        self.at("therefore remains")
        self.play(front.animate.set_value(10), FadeOut(label), FadeOut(enlargement),
                  run_time=3.5, rate_func=linear)
        self.finish()


def q61_alignment():
    return VGroup(
        Line([4.97, -1.29, 0], [5.11, -1.05, 0], color=CLAY, stroke_width=5),
        Line([5.23, -0.89, 0], [5.36, -0.65, 0], color=CLAY, stroke_width=5),
        Line([5.29, -1.2, 0], [5.49, -1.2, 0], color=CLAY, stroke_width=5),
    )


class S09Q61(SpokenScene):
    def construct(self):
        front = ValueTracker(0.55)
        left = g12v_world()
        left.body.set_fill(GOLD, opacity=0.52)
        gap = ras_gap()
        gap[0].set_fill(CLAY, opacity=0.40)
        right = switch("Ras Q61", at=(3.6, -0.65, 0), width=3.95)
        self.add(membrane(), left, gap, g12v_alignment(), trace(10))
        self.at("shown beside it")
        self.play(FadeIn(right), run_time=0.95)
        self.at("weakens cutting")
        misfit = q61_alignment()
        self.play(Create(misfit[0]), Create(misfit[1]), run_time=0.8)
        self.at("without gap")
        no_gap = T("without GAP", 30, GREY).move_to([3.6, -2.55, 0])
        self.play(FadeIn(no_gap), run_time=0.65)
        self.at("both mutants")
        lower = trace(front, box=(-2.65, 5.8, -3.56, -3.10), tagged=False)
        self.add(lower)
        trace_names = VGroup(T("G12V", 28, GOLD).move_to([-4.45, 1.65, 0]),
                             T("Q61", 28, GOLD).move_to([-4.45, -3.29, 0]))
        self.play(FadeIn(trace_names), front.animate.set_value(9.25), run_time=3.05, rate_func=linear)
        self.at("damage the off")
        self.play(Create(misfit[2]), front.animate.set_value(10), run_time=1.05)
        self.at("detailed defects differ")
        caption_line = T("schematic mechanisms", 28, GREY).move_to([-0.7, 3.18, 0])
        self.play(FadeIn(caption_line), left.body.animate.set_fill(GOLD, opacity=0.31),
                  right.body.animate.set_fill(GOLD, opacity=0.26), run_time=0.8)
        self.finish()


class S10S17n(SpokenScene):
    def construct(self):
        protein = switch("Ras S17N", on=False, ras=True)
        self.at("dominant negative")
        front = ValueTracker(0.75)
        normal_body = g12v_world().body
        previous_trace = trace(10, tagged=False)
        self.add(membrane(), receptor(False), normal_body, previous_trace)
        self.play(ReplacementTransform(normal_body, protein.body), FadeOut(previous_trace),
                  FadeIn(protein.nameplate), FadeIn(protein.token), FadeIn(protein[0]),
                  FadeIn(trace(front, cut=LOAD_AT)), run_time=1.6)
        gtp = nucleotide("GTP", [5.02, -2.12, 0]).scale(1.43)
        gtp[0].box.set_fill(GOLD, opacity=0.60)
        self.play(FadeIn(gtp), run_time=0.9)
        self.play(gtp.animate.move_to([3.69, -1.48, 0]),
                  front.animate.set_value(2.2), run_time=2.2, rate_func=linear)
        self.at("binds GTP poorly")
        self.play(gtp.animate.move_to([1.65, -0.64, 0]), run_time=1.0)
        self.play(FadeOut(gtp, shift=RIGHT * 1.48), run_time=0.65)
        self.at("fails to activate")
        off = target(False, center=(4.35, -0.86, 0), radius=1.52)
        self.play(FadeIn(off), front.animate.set_value(4.4), run_time=1.45)
        self.at("failure sits on")
        load = loading_arrow()
        label = boxed_label("loading", TEAL, size=33, fill_opacity=0.29,
                            box=(2.34, 0.85)).move_to([-4.66, -1.29, 0])
        label.label.set_color(TEXT)
        self.play(GrowArrow(load), FadeIn(label), front.animate.set_value(6.7), run_time=1.3)
        brake = stop_mark(load.get_end(), color=TEAL).rotate(load.get_angle())
        self.play(FadeIn(brake), front.animate.set_value(7.5), run_time=0.78)
        self.at("may also hold")
        sos = boxed_label("SOS", TEAL, size=31, box=(1.3, 0.68)).move_to([-4.4, -2.66, 0])
        stop = np.array([-2.4, -2.66, 0])
        path = DashedLine([-3.56, -2.66, 0], stop, color=TEAL, stroke_width=5)
        may = T("may", 30, TEXT).move_to([-2.95, -2.22, 0])
        self.play(FadeOut(off), FadeOut(label), FadeIn(sos), Create(path), FadeIn(may),
                  run_time=0.55)
        self.play(FadeOut(path), FadeOut(may), run_time=0.27)
        self.play(sos.animate.move_to([-1.87, -2.66, 0]), run_time=0.88)
        self.at("away from normal")
        normal = boxed_label("normal Ras", SLATE, size=31, box=(2.31, 0.83)
                             ).move_to([4.06, -2.66, 0])
        no_sos = DashedLine([-0.98, -2.66, 0], [2.64, -2.66, 0], color=SLATE, stroke_width=4)
        may.move_to([0.83, -2.22, 0])
        barrier = stop_mark(no_sos.get_end(), color=TEAL)
        self.play(FadeIn(normal), FadeIn(may), Create(no_sos), GrowFromCenter(barrier),
                  front.animate.set_value(10), run_time=1.3)
        self.finish()


def cycle_state(on, at):
    color = GOLD if on else SLATE
    body = RoundedRectangle(width=2.8, height=2.36, corner_radius=0.28,
                            color=color, stroke_width=5, fill_opacity=0.43).move_to(at)
    name = T("On" if on else "Off", 34, TEXT, weight=BOLD).move_to(body.get_center() + UP * 0.72)
    return VGroup(body, name, nucleotide("GTP" if on else "GDP", body.get_center() + DOWN * 0.33))


def cycle():
    left = cycle_state(False, [-4.9, 0.03, 0])
    right = cycle_state(True, [4.9, 0.03, 0])
    load = CurvedArrow([-3.49, 1.43, 0], [3.49, 1.43, 0], angle=-0.39,
                       color=TEAL, stroke_width=7, tip_length=0.25)
    cut = CurvedArrow([3.49, -1.38, 0], [-3.49, -1.38, 0], angle=-0.39,
                      color=CLAY, stroke_width=7, tip_length=0.25)
    labels = VGroup(T("loading", 32, TEAL).move_to([0, 1.07, 0]),
                    T("cutting", 32, CLAY).move_to([0, -1.07, 0]))
    return VGroup(left, right), load, cut, labels


def sorted_cases():
    blockers = VGroup(*[boxed_label(label, CLAY, size=29)
                        for label in ("analogue", "toxin", "Ras G12V / Q61")]
                      ).arrange(RIGHT, buff=0.33).move_to([-2.1, -3.05, 0])
    rgs = boxed_label("RGS substrates", CLAY, size=29, pad=0.15,
                      fill_opacity=0.36).move_to([1.77, -0.35, 0])
    rgs.label.set_color(TEXT)
    s17n = boxed_label("Ras S17N", TEAL, size=31, fill_opacity=0.35).move_to([0, 2.82, 0])
    return blockers, rgs, s17n


class S11Sort(SpokenScene):
    def construct(self):
        states, load, cut, labels = cycle()
        blockers, rgs, s17n = sorted_cases()
        self.at("sort every case")
        self.add(states)
        self.play(Create(load), run_time=0.6)
        self.play(Create(cut), run_time=0.73)
        self.at("changed arrow")
        self.play(FadeIn(labels), run_time=0.7)
        self.at("analog")
        self.play(FadeIn(blockers[0], shift=UP * 0.62), run_time=0.68)
        self.at("toxin")
        self.play(FadeIn(blockers[1], shift=UP * 0.62), run_time=0.68)
        self.at("activating ras mutants")
        self.play(FadeIn(blockers[2], shift=UP * 0.62), run_time=0.75)
        self.at("obstruct cutting")
        bar = stop_mark(cut.point_from_proportion(0.83))
        branch_y = -2.34
        branch = VGroup(
            Line(bar.get_bottom(), [bar.get_x(), branch_y, 0], color=CLAY, stroke_width=3),
            Line([blockers[0].get_x(), branch_y, 0], [blockers[-1].get_x(), branch_y, 0],
                 color=CLAY, stroke_width=3),
            *[Line([chip.get_x(), branch_y, 0], chip.get_top() + UP * 0.12,
                   color=CLAY, stroke_width=3) for chip in blockers],
        )
        self.play(GrowFromCenter(bar), Create(branch), run_time=0.85)
        self.at("extra rgs accelerates")
        fast = VGroup(*[chevron(cut.point_from_proportion(f), -1, 0.18) for f in (0.25, 0.29)])
        pointer = Line(rgs.get_bottom() + DOWN * 0.12, [rgs.get_x(), -1.34, 0],
                       color=CLAY, stroke_width=3)
        self.play(FadeIn(rgs), Create(pointer), run_time=0.85)
        self.play(LaggedStart(*[Create(mark) for mark in fast], lag_ratio=0.6), run_time=1.35)
        self.at("dominant negative ras")
        self.play(FadeIn(s17n, shift=UP * 0.58), run_time=0.9)
        self.at("impairs loading")
        load_bar = Line(UP * 0.2, DOWN * 0.2, color=TEAL, stroke_width=8).move_to([0, 1.77, 0])
        self.play(GrowFromCenter(load_bar), run_time=0.85)
        self.at("one cycle can")
        self.play(states[0][0].animate.set_fill(SLATE, opacity=0.58),
                  ShowPassingFlash(load.copy().set_stroke(width=14), time_width=0.5),
                  run_time=1.3)
        self.play(states[1][0].animate.set_fill(GOLD, opacity=0.59),
                  ShowPassingFlash(cut.copy().set_stroke(width=14), time_width=0.5),
                  run_time=1.3)
        self.finish()


def scope_world(front, on=False, cleared=False, highlighted=False):
    mem = membrane()
    rec = receptor(on)
    protein = switch(on=True)
    gauge = target()
    dots = messenger_dots()
    if cleared:
        dots.set_opacity(0.23)
    chart = trace(front)
    load = loading_arrow()
    link = Arrow([1.22, -0.62, 0], [3.12, -0.62, 0], buff=0,
                 color=GOLD, stroke_width=6, tip_length=0.2)
    cut = Arrow([0.76, -1.96, 0], [0.18, -2.72, 0], buff=0,
                color=CLAY, stroke_width=7, tip_length=0.23)
    brake = stop_mark(cut.get_end()).rotate(cut.get_angle()).set_stroke(width=7)
    cut_label = T("cutting", 30, CLAY).move_to([1.65, -2.45, 0])
    if highlighted:
        load.set_opacity(0.38)
        link.set_stroke(opacity=0.48)
        cut.set_stroke(width=10, family=False)
        brake.set_stroke(width=8)
        for mark in gauge[:3]:
            mark.clear_updaters()
            mark.set_stroke(opacity=0.48)
    return mem, rec, protein, gauge, dots, chart, load, link, cut_label, cut, brake


class S12Scope(SpokenScene):
    def construct(self):
        front = ValueTracker(1.24)
        world = scope_world(front, on=True)
        _, rec, _, gauge, dots, _, load, link, _, cut, brake = world
        self.at("this classification")
        self.add(*world)
        self.play(front.animate.set_value(2.1), cut.animate.set_stroke(width=9, family=False),
                  run_time=2.05, rate_func=linear)
        self.at("exact shape")
        limit = T("direction of change", 32, TEXT).move_to([-1.8, -3.25, 0])
        self.play(FadeIn(limit), front.animate.set_value(3.7), run_time=2.5, rate_func=linear)
        self.at("receptor shutoff")
        self.play(Transform(rec, receptor(False)), load.animate.set_opacity(0.38),
                  front.animate.set_value(4.6), run_time=1.25)
        self.at("target kinetics")
        self.play(dial_strokes(gauge, 0.48), link.animate.set_stroke(opacity=0.48), run_time=0.76)
        self.at("messenger clearance")
        self.play(LaggedStart(*[d.animate.set_opacity(0.23) for d in dots], lag_ratio=0.11),
                  front.animate.set_value(7.25), run_time=2.35, rate_func=linear)
        self.at("limit visible")
        self.play(FadeOut(limit), front.animate.set_value(8.45), run_time=1.5, rate_func=linear)
        self.at("locate the change step")
        self.play(cut.animate.set_stroke(width=10, family=False),
                  brake.animate.set_stroke(width=8), run_time=0.9)
        self.at("judge the trace")
        self.play(front.animate.set_value(10), run_time=1.2, rate_func=linear)
        self.finish()


def control(level, name, color, center, radius):
    return dial(level, center=center, radius=radius, label=name, color=color, fmt="", size=32)


def cut_time(level):
    # Mean time on = 1 / cutting rate; the dial moves through illustrative rates.
    neutral_rate = 1 / (NORMAL_CUT - LOAD_AT)
    rate = neutral_rate * 1.9 ** (2 * level.get_value() - 1)
    return LOAD_AT + 1 / rate


class S13Close(SpokenScene):
    def construct(self):
        front = ValueTracker(10)
        world = scope_world(front, cleared=True, highlighted=True)
        self.at("lasting signal")
        self.add(*world)
        self.play(world[-2].animate.set_stroke(width=7, family=False), run_time=2.9)
        self.at("cycle is mapped")
        speed = ValueTracker(0.5)
        loading = ValueTracker(0.36)
        clearance = ValueTracker(0.47)
        l, c, r = (
            control(loading, "loading", TEAL, [-4.25, 1.17, 0], 0.96),
            control(speed, "cutting", CLAY, [0, 1.15, 0], 1.56),
            control(clearance, "clearance", MESSENGER, [4.25, 1.17, 0], 0.96),
        )
        axes = trace_plot(box=(-5.8, 5.8, -2.92, -0.43))
        band = always_redraw(lambda: activity(axes, 10, cut_time(speed)))
        tag = schematic([4.85, -3.37, 0])
        self.play(FadeOut(VGroup(*world)), run_time=0.55)
        self.play(FadeIn(VGroup(l, c, r, axes, band, tag)), run_time=0.75)
        self.at("loading increased")
        self.play(loading.animate.set_value(0.82), run_time=1.05)
        self.at("cutting slowed")
        self.play(speed.animate.set_value(0.08), run_time=1.0)
        self.at("clearance changed")
        self.play(clearance.animate.set_value(0.75), run_time=1.35)
        self.at("same map prevents")
        focus = T("GTP-bound interval", 32, GOLD).move_to([0, -3.39, 0])
        ordinary = axes.vline(NORMAL_CUT, color=SLATE, dashed=True)
        self.play(FadeIn(focus), Create(ordinary), run_time=1.2)
        self.at("the receptor automatically")
        self.play(dial_strokes(l, 0.26), FadeToColor(l[-1], GREY), run_time=1.65)
        self.at("position of the defect")
        self.play(speed.animate.set_value(0.90), run_time=2.45, rate_func=linear)
        self.finish()


class S14End(EndCard):
    LINE = "Block GTP cutting to prolong signaling; speed it to shorten signaling."
