"""Ordering Genes with Double Mutants, timed to the supplied word alignment.

COLOR MAP (from the patch-clamp palette)
  BLUE / TEAL = the carried cell-fate diagram and its structural tracks
  GREY = an empty gate slot or inactive branch
  PURPLE = the brake, CED-9
  ORANGE = the killer, CED-3
  BLUE = CED-4; TEAL = EGL-1; RED = death; GREEN = survival
  YELLOW = flow or cargo; GOLD = questions, historical dates and the rule
"""

from bp_parts import *  # noqa: F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BODY = "#234150"
RIM = "#396778"
LANE = "#345767"
SOCKET = "#18303C"
TRACK_Y = -0.10
BRAKE_X, KILLER_X = -2.45, 0.80
FATE_X = 4.45
LIVE_Y, DEAD_Y = 1.07, -1.06

QUESTION = "Die without the brake, or live without the killer?"
CARD = {"y": 3.12, "size": 34, "max_w": 11.3}
GENE_COLORS = {"ced-9": PURPLE, "ced-3": ORANGE, "CED-9": PURPLE, "CED-3": ORANGE,
               "CED-4": BLUE, "EGL-1": TEAL}


def xy(x, y=TRACK_Y):
    return np.array([x, y, 0.0])


def arrow(a, b, color=GREY, width=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=0.20,
                 max_tip_length_to_length_ratio=0.35)


def top(text, color=TEXT, size=34):
    return fit_text(text, max_w=11.4, size=size, color=color, min_size=28).move_to(xy(0, 3.12))


def take_home(text, color=GOLD):
    return caption(text, size=32, color=color, y=-2.92).move_to(xy(0, -2.92))


def contour(yeast=False):
    """Cubic outlines share their endpoints with the track and morph into each other."""
    if yeast:
        start = (-6.20, -0.15)
        bends = [
            ((-6.18, 1.65), (-4.22, 2.64), (-1.80, 2.54)),
            ((0.2, 2.59), (1.90, 2.14), (2.92, 1.32)),
            ((4.35, 2.13), (6.29, 1.48), (6.27, -0.07)),
            ((6.27, -1.47), (4.32, -2.21), (2.92, -1.46)),
            ((1.66, -2.24), (-0.12, -2.57), (-2.15, -2.50)),
            ((-4.65, -2.53), (-6.10, -1.81), start),
        ]
    else:
        start = (-6.20, -0.15)
        bends = [
            ((-6.20, 1.56), (-4.73, 2.44), (-2.56, 2.54)),
            ((-0.65, 2.73), (1.08, 2.21), (2.92, 2.21)),
            ((4.33, 2.27), (5.13, 1.95), (6.27, 0.67)),
            ((6.07, -1.42), (5.55, -1.91), (2.92, -2.14)),
            ((1.30, -2.24), (-0.05, -2.61), (-2.15, -2.50)),
            ((-4.34, -2.47), (-6.13, -1.61), start),
        ]
    outline = VMobject()
    outline.start_new_path(xy(*start))
    for a, b, end in bends:
        outline.add_cubic_bezier_curve_to(xy(*a), xy(*b), xy(*end))
    outline.close_path()
    return outline.set_fill(BODY, opacity=0.91).set_stroke(RIM, width=3)


def branch(y):
    path = VMobject()
    path.start_new_path(xy(2.65))
    path.add_cubic_bezier_curve_to(xy(3.30), xy(3.29, y), xy(3.68, y))
    return path.set_stroke(LANE, width=10)


def cell_at(p, color=TEAL, radius=0.46):
    cell = VGroup(
        Circle(radius=radius, color=color, stroke_width=3, fill_color=color, fill_opacity=0.26),
        Dot(radius=radius * 0.34, color=color),
    ).move_to(p)
    return cell


def breathe(shell):
    """Gently cycle the illumination of the carried diagram during narration."""
    phase = 0.0

    def update(outline, dt):
        nonlocal phase
        phase += dt * TAU / 4.8
        outline.set_fill(opacity=0.83 + 0.08 * np.cos(phase))
        outline.set_stroke(width=3 + 0.85 * np.sin(phase))

    shell.add_updater(update)


def world(fates=True, yeast=False, moving=True):
    """Rebuild the carried stage, cell, track and fate readout in fixed coordinates."""
    shell = contour(yeast)
    lane = Line(xy(-5.12), xy(2.65 if fates else 5.95), color=LANE, stroke_width=11)
    cell = cell_at(xy(-5.17))
    tracks = VGroup(lane, branch(LIVE_Y), branch(DEAD_Y)) if fates else VGroup(lane)
    frame = VGroup(shell, tracks)
    if fates:
        lives = boxed_label("Lives", GREEN, 30, box=(1.43, 0.65), pad=0.14).move_to(xy(FATE_X, LIVE_Y))
        dies = boxed_label("Dies", RED, 30, box=(1.43, 0.65), pad=0.14).move_to(xy(FATE_X, DEAD_Y))
        frame.add(lives, dies)
        frame.lives, frame.dies = lives, dies
    frame.shell, frame.tracks, frame.cell = shell, tracks, cell
    if moving:
        breathe(shell)
    return frame


def gate(x, color, name=None, missing=False, y=TRACK_Y, role=None, width=1.38):
    """A gate has a fixed socket and a removable two-piece plug."""
    socket = RoundedRectangle(width=width, height=1.62, corner_radius=0.22, stroke_color=color,
                              stroke_width=2.6, fill_color=SOCKET, fill_opacity=1).move_to(xy(x, y))
    halves = VGroup()
    width_scale = width / 1.38
    for side in (-1, 1):
        halves.add(RoundedRectangle(width=0.49 * width_scale, height=1.25, corner_radius=0.11,
                                    stroke_color=color, stroke_width=1.6,
                                    fill_color=color, fill_opacity=0.48).move_to(xy(x + side * 0.28 * width_scale, y)))
    if missing:
        socket.set_stroke(color=GREY, width=2.2)
    label = T(name, 32, color).move_to(xy(x, y + 1.16)) if name else VGroup()
    role_label = T(role, 28, color).move_to(xy(x, y - 1.16)) if role else VGroup()
    frame = VGroup(socket, label, role_label)
    if not missing:
        frame.add(halves)
    frame.socket, frame.halves, frame.label, frame.role = socket, halves, label, role_label
    return frame


def genes(missing=(), roles=False):
    return VGroup(gate(BRAKE_X, PURPLE, "ced-9", missing="ced-9" in missing, role="Brake" if roles else None),
                  gate(KILLER_X, ORANGE, "ced-3", missing="ced-3" in missing, role="Killer" if roles else None))


def break_gates(scene, *gates, run_time=1.1):
    animations = []
    for g in gates:
        animations.extend([
            g.socket.animate.set_stroke(color=GREY, width=2.2),
            FadeOut(g.halves[0], shift=LEFT * 0.43 + DOWN * 0.80),
            FadeOut(g.halves[1], shift=RIGHT * 0.43 + DOWN * 0.80),
        ])
    scene.play(*animations, run_time=run_time)
    # The plugs belong to the gate group as well as to the removal animations.
    for g in gates:
        g.halves.remove(*list(g.halves))
        g.remove(g.halves)


def restored_gate(scene, old, x, color):
    fresh = gate(x, color)
    old.halves = fresh.halves
    old.add(old.halves)
    scene.play(FadeIn(old.halves, shift=UP * 0.18), old.socket.animate.set_stroke(color, width=2.6),
               run_time=0.70)


def inhibit(x1, x2, color=PURPLE, y=TRACK_Y):
    return VGroup(Line(xy(x1, y), xy(x2, y), color=color, stroke_width=5),
                  Line(xy(x2, y - 0.29), xy(x2, y + 0.29), color=color, stroke_width=5))


def order_arrow(x1=BRAKE_X, x2=KILLER_X):
    return arrow(xy(x1, -1.83), xy(x2, -1.83), BLUE)


def flow(stop=2.62, color=YELLOW, start=-4.56, speed=1.75, count=6, tracks_y=TRACK_Y, moving=True):
    """One packet stream. Changing its endpoint makes packets queue at a gate."""
    endpoint = stop if isinstance(stop, ValueTracker) else ValueTracker(stop)
    packets = VGroup(*[Dot(radius=0.18 if i % 2 == 0 else 0.105, color=color)
                       for i in range(count)])
    phase = 0.0

    def advance(group, dt):
        nonlocal phase
        phase += dt * speed
        limit = endpoint.get_value()
        for i, packet in enumerate(group):
            s = (phase + i * 0.83) % (max(limit - start, 0.20) + 0.85)
            x = start + min(s, limit - start) - max(s - (limit - start), 0) * 0.55
            packet.move_to(xy(x, tracks_y + 0.18 * np.sin(phase * 2.1 + i * 1.8)))
            packet.set_opacity(0.45 + 0.55 * np.sin(s * 1.1 + i) ** 2)

    advance(packets, 0)
    if moving:
        packets.add_updater(advance)
    return packets


def living_cell(scene, frame, survives, run_time=1.65):
    """Follow the curved decision branch and stop immediately before its badge."""
    y, color = (LIVE_Y, GREEN) if survives else (DEAD_Y, RED)
    p = VMobject()
    p.start_new_path(xy(2.66))
    p.add_cubic_bezier_curve_to(xy(3.12), xy(3.15, y), xy(3.45, y))
    result = cell_at(p.get_start(), color, radius=0.21)
    scene.add(result)
    scene.play(MoveAlongPath(result, p, rate_func=smooth),
               (frame.lives if survives else frame.dies).box.animate.set_fill(color, opacity=0.20).set_stroke(color, width=5.2),
               run_time=run_time)
    bob(result, amp=0.08, speed=3.0)
    return result


def set_live(frame):
    frame.lives.box.set_fill(GREEN, opacity=0.20).set_stroke(GREEN, width=5.2)
    return cell_at(xy(3.45, LIVE_Y), GREEN, radius=0.21)


def unknown():
    return VGroup(*(gate(x, BLUE, "?") for x in (BRAKE_X, KILLER_X)))


def question_mark():
    return T("?", 54, GOLD, weight=BOLD).move_to(xy(FATE_X))


def prediction():
    frame = world(moving=False)
    gates = genes(missing=("ced-9", "ced-3"))
    mark = question_mark()
    queue = flow(KILLER_X - 0.80, moving=False)
    return frame, gates, mark, queue, question_card(QUESTION, **CARD)


def single_badge(gene, survives, x):
    fate, color = ("Lives", GREEN) if survives else ("Dies", RED)
    return boxed_label(f"{gene} loss  ·  {fate}", color, 29, pad=0.18).move_to(xy(x, -2.94))


class S01Hook(SpokenScene):
    def construct(self):
        frame = world()
        gates = unknown()
        packets = flow()
        pulse(frame.cell[0], base=4, amp=2.0, speed=3.3)
        self.add(frame, frame.cell, gates, packets, scope_tag(size=28, color=TEXT))

        self.at("but which acts first")
        prompt = top("Which gene acts first?", GOLD)
        self.play(FadeIn(prompt), run_time=0.55)

        self.at("In hermaphrodite")
        species = top("Hermaphrodite C. elegans")
        self.play(swap(prompt, species, run_time=0.66))
        total = ValueTracker(0)
        read = counter("{:,.0f} somatic cells", total, xy(0, -2.92), 33, BLUE, mono=False)
        self.at("development makes", lead=0.9)
        self.add(read)
        self.play(total.animate.set_value(1090), run_time=1.8, rate_func=rate_functions.ease_out_quad)
        read.clear_updaters()

        self.at("The same 131", lead=0.55)
        loss = take_home("1,090 − 131", RED)
        self.play(swap(read, loss, run_time=0.45))
        routed = living_cell(self, frame, False, run_time=1.60)
        self.at("leaving 959", lead=0.45)
        alive = take_home("1,090 − 131 = 959 living cells", GREEN)
        self.play(swap(loss, alive, run_time=0.55))
        survivor = living_cell(self, frame, True, run_time=1.55)

        self.at("Reproducible death alone")
        self.play(FadeOut(alive), FadeOut(species), run_time=0.75)
        self.at("so geneticists test")
        self.play(FadeOut(routed), FadeOut(survivor),
                  frame.lives.box.animate.set_fill(GREEN, opacity=0.16).set_stroke(GREEN, width=2.5),
                  frame.dies.box.animate.set_fill(RED, opacity=0.16).set_stroke(RED, width=2.5),
                  *(g.socket.animate.set_stroke(YELLOW, width=4.2) for g in gates), run_time=0.8)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Epistasis Analysis"
    TITLE = "Ordering Genes with Double Mutants"

    def construct(self):
        frame = world()
        gates = unknown()
        for g in gates:
            g.socket.set_stroke(YELLOW, width=4.2)
        track = VGroup(frame, frame.cell, gates, flow())
        self.add(track)
        frame.shell.set_fill("#1B2E39", opacity=0.91).set_stroke("#2C4A58", width=3)
        frame.tracks.set_stroke("#2B4654")
        title = fit_text(self.TITLE, size=48, min_size=36, max_w=12, font=TITLE_FONT).move_to(xy(0, 3.09))
        lesson = T(self.LESSON.upper(), 28, GOLD).move_to(xy(0, -2.94))
        self.play(FadeIn(title), FadeIn(lesson), run_time=0.47)
        self.wait(1.40)


class S03SingleMutants(SpokenScene):
    def construct(self):
        frame = world()
        brake, killer = gate(BRAKE_X, PURPLE), gate(KILLER_X, ORANGE)
        limit = ValueTracker(BRAKE_X - 0.77)
        packets = flow(limit)
        self.add(frame, frame.cell, brake, killer, packets, scope_tag(size=28, color=TEXT))
        self.at("Start with loss")
        heading = top("Loss of function")
        self.play(FadeIn(heading), run_time=0.55)
        self.at("activity is reduced")
        self.play(brake.halves.animate.set_fill(PURPLE, opacity=0.15), run_time=1.35)
        self.at("A null mutant")
        null_title = top("Null mutant")
        self.play(swap(heading, null_title, run_time=0.55),
                  brake.halves.animate.set_fill(PURPLE, opacity=0).set_stroke(opacity=0.32),
                  run_time=0.55)
        self.at("has none left")
        no_activity = take_home("No activity")
        self.play(FadeIn(no_activity), run_time=0.55)

        self.at("Losing said 9", lead=0.54)
        n9 = T("ced-9", 32, PURPLE).move_to(xy(BRAKE_X, 1.06))
        self.play(FadeIn(n9), FadeOut(null_title), FadeOut(no_activity),
                  brake.halves.animate.set_fill(PURPLE, opacity=0.48).set_stroke(opacity=1), run_time=0.37)
        self.at("removes a break", lead=0.40)
        break_gates(self, brake, run_time=0.83)
        self.play(limit.animate.set_value(2.65), run_time=0.70)
        self.at("so killing follows", lead=0.38)
        outcome = living_cell(self, frame, False)
        self.play(FadeOut(outcome), frame.dies.box.animate.set_fill(RED, opacity=0.16).set_stroke(RED, width=2.5),
                  limit.animate.set_value(BRAKE_X - 0.77), run_time=0.45)
        restored_gate(self, brake, BRAKE_X, PURPLE)
        self.at("Losing said 3", lead=0.35)
        n3 = T("ced-3", 32, ORANGE).move_to(xy(KILLER_X, 1.06))
        self.play(FadeIn(n3), run_time=0.37)
        self.at("removes the killer", lead=0.36)
        break_gates(self, killer, run_time=0.90)
        self.at("so doomed cells live", lead=0.36)
        outcome = living_cell(self, frame, True)
        self.at("Single mutants name")
        first, second = single_badge("ced-9", False, -2.0), single_badge("ced-3", True, 2.0)
        q = top("Which comes first?", GOLD)
        self.play(FadeIn(first), FadeIn(second), FadeIn(q), run_time=0.55)
        self.at("not their order", lead=0.73)
        self.play(FadeOut(n9), FadeOut(n3), FadeOut(outcome), run_time=0.27)
        self.play(brake.animate(path_arc=-2.1).shift(RIGHT * (KILLER_X - BRAKE_X)),
                  killer.animate(path_arc=-2.1).shift(LEFT * (KILLER_X - BRAKE_X)), run_time=1.19)
        n9.move_to(xy(KILLER_X, 1.06))
        n3.move_to(xy(BRAKE_X, 1.06))
        self.play(FadeIn(n9), FadeIn(n3), run_time=0.30)
        self.finish()


class S04DoubleSetup(SpokenScene):
    def construct(self):
        frame = world()
        flipped = VGroup(gate(KILLER_X, PURPLE, "ced-9"), gate(BRAKE_X, ORANGE, "ced-3", missing=True))
        badges = VGroup(single_badge("ced-9", False, -2.0), single_badge("ced-3", True, 2.0))
        title = top("Which comes first?", GOLD)
        self.add(frame, frame.cell, flipped, badges, title, flow(BRAKE_X - 0.77), scope_tag(size=28, color=TEXT))
        self.at("put both mutations")
        self.play(badges[0].animate.move_to(xy(-1.90, -2.94)),
                  badges[1].animate.move_to(xy(1.90, -2.94)), run_time=0.75)
        self.at("into one worm")
        break_gates(self, flipped[0], run_time=0.58)
        both = take_home("ced-9 loss  +  ced-3 loss")
        self.play(swap(badges, both), FadeOut(title), run_time=0.73)
        self.at("making a double mutant")
        tag = top("Double mutant")
        self.play(FadeIn(tag), run_time=0.67)

        self.at("Suppose said 9", lead=0.9)
        self.play(FadeOut(flipped), FadeOut(both), FadeOut(tag), run_time=0.38)
        brake, killer = genes(roles=True)
        hypothesis = top("Suppose this is the order", GOLD)
        self.play(FadeIn(brake), FadeIn(killer), FadeIn(hypothesis), run_time=0.63)
        self.at("holding back said", lead=0.6)
        bar = inhibit(BRAKE_X + 0.72, KILLER_X - 0.78)
        self.play(Create(bar), run_time=1.10)
        self.at("acts downstream")
        downstream = arrow(xy(KILLER_X + 0.73), xy(2.64), ORANGE)
        danger = frame.tracks[2].copy().set_stroke(ORANGE, width=4)
        self.play(GrowArrow(downstream), Create(danger), run_time=1.15)
        self.at("normally prevents")
        self.play(FadeOut(hypothesis), run_time=0.48)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        frame, _, mark, queue, question = prediction()
        breathe(frame.shell)
        brake, killer = genes(roles=True)
        bar = inhibit(BRAKE_X + 0.72, KILLER_X - 0.78)
        downstream = arrow(xy(KILLER_X + 0.73), xy(2.64), ORANGE)
        limit = ValueTracker(BRAKE_X - 0.77)
        packets = flow(limit)
        danger = frame.tracks[2].copy().set_stroke(ORANGE, width=4)
        self.add(frame, frame.cell, brake, killer, bar, downstream, danger, packets, scope_tag(size=28, color=TEXT))

        self.at("remove both genes")
        self.play(FadeOut(bar), FadeOut(downstream), FadeOut(danger),
                  FadeOut(brake.role), FadeOut(killer.role), run_time=0.55)
        self.at("breaking the break", lead=0.65)
        break_gates(self, brake, killer, run_time=1.26)
        self.play(limit.animate.set_value(KILLER_X - 0.80), run_time=1.30)
        self.at("Predict what happens")
        self.play(FadeIn(mark, scale=0.70), run_time=0.52)
        self.at("Do they die", lead=0.75)
        self.play(FadeIn(question), run_time=0.62)
        self.play(Indicate(frame.dies.label, color=RED, scale_factor=1.06), run_time=1.65)
        self.at("or live because")
        self.play(Indicate(frame.lives.label, color=GREEN, scale_factor=1.06), run_time=1.65)
        self.at("gone too", lead=-1.40)
        self.remove(packets)
        frame.shell.clear_updaters()
        frame.shell.set_fill(opacity=0.91).set_stroke(width=3)
        self.add(queue)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD
    SECONDS = 4.5

    def construct(self):
        frame, gates, mark, queue, question = prediction()
        halo = Ellipse(width=2.42, height=0.97, stroke_width=0, fill_color=GOLD,
                       fill_opacity=0).move_to(mark)
        halo.add_updater(lambda glow, dt: glow.set_fill(
            opacity=0.53 * np.sin(PI * self.elapsed() / self.SECONDS) ** 2
        ))
        center = Circle(radius=0.35, stroke_width=0, fill_opacity=1,
                        fill_color=interpolate_color(ManimColor(BG), ManimColor(BODY), 0.91)).move_to(mark)
        self.add(frame, frame.cell, gates, queue, halo, center, mark, question, scope_tag(size=28, color=TEXT))
        self.wait(self.SECONDS)


class S07Reveal(SpokenScene):
    def construct(self):
        frame, gates, mark, queue, question = prediction()
        self.add(frame, frame.cell, gates, mark, queue, question, scope_tag(size=28, color=TEXT))
        self.at("The double mutant", lead=0)
        breathe(frame.shell)
        self.play(FadeOut(question), FadeOut(mark), FadeOut(queue), run_time=0.64)
        self.at("mutant lives", lead=0.44)
        result = living_cell(self, frame, True, run_time=2.42)
        self.at("matching the said")
        match = single_badge("ced-3", True, 0)
        self.play(FadeIn(match), run_time=0.66)
        self.at("Removing the killer")
        self.play(FadeOut(match), gates[1].socket.animate.set_stroke(ORANGE, width=4), run_time=1.05)
        self.at("cancels the effect")
        self.play(gates[0].socket.animate.set_stroke(PURPLE, width=3), run_time=1.30)
        self.at("works through the killer")
        order = order_arrow()
        self.play(GrowArrow(order), run_time=1.2)
        self.at("That is epistasis")
        banner = take_home("Epistasis: later gene wins")
        self.play(FadeIn(banner), run_time=0.65)
        self.at("When two losses")
        left = single_badge("ced-9", False, -2)
        right = single_badge("ced-3", True, 2)
        self.play(swap(banner, VGroup(left, right)), run_time=0.9)
        self.at("usually shows the later")
        self.play(swap(VGroup(left, right), banner),
                  gates[1].socket.animate.set_stroke(ORANGE, width=6), run_time=0.92)
        self.finish()


class S08Guardrails(SpokenScene):
    def construct(self):
        frame = world()
        brake, killer = genes(missing=("ced-9", "ced-3"))
        brake.socket.set_stroke(PURPLE, width=3)
        killer.socket.set_stroke(ORANGE, width=6)
        order = order_arrow()
        result = set_live(frame)
        bob(result, amp=0.09, speed=3.0)
        pulse(order, base=5, amp=1.6, speed=2.0)
        banner = take_home("Epistasis: later gene wins")
        self.add(frame, frame.cell, brake, killer, order, result, banner, scope_tag(size=28, color=TEXT))
        self.at("Two limits keep")
        self.play(FadeOut(banner), killer.socket.animate.set_stroke(GREY, width=2.2), run_time=1.1)
        self.at("expects a linear pathway")
        linear_title = top("Linear pathway")
        self.play(FadeIn(linear_title), brake.socket.animate.set_stroke(GREY, width=2.2), run_time=0.75)
        self.at("and opposite loss")
        left = single_badge("ced-9", False, -2.0)
        right = single_badge("ced-3", True, 2.0)
        self.play(FadeIn(left), FadeIn(right), run_time=0.70)

        self.at("use strong loss")
        clear = top("Strong loss of function")
        self.play(swap(linear_title, clear), run_time=0.80)
        self.at("or null mutants")
        null_title = top("Null: no activity")
        self.play(swap(clear, null_title), run_time=0.70)
        self.at("because leftover activity")
        leftover = top("Leftover activity", GOLD)
        partial_plugs = VGroup(brake.halves[0], killer.halves[0])
        partial_plugs.set_fill(opacity=0.25).set_stroke(opacity=0.55)
        self.play(swap(null_title, leftover), FadeIn(partial_plugs), run_time=0.7)
        self.at("can blur", lead=0.38)
        mark = question_mark()
        result.save_state()
        self.play(FadeIn(mark, scale=0.80), result.animate.fade(0.65),
                  frame.lives.box.animate.set_fill(GREEN, opacity=0.16).set_stroke(GREEN, width=2.5),
                  run_time=0.55)
        self.at("Comparing the double mutant")
        compare = top("Double mutant: Lives", GREEN)
        self.play(swap(leftover, compare), FadeOut(partial_plugs), FadeOut(mark),
                  Restore(result),
                  frame.lives.box.animate.set_fill(GREEN, opacity=0.20).set_stroke(GREEN, width=5.2),
                  run_time=0.65)
        self.at("to both single mutants")
        self.play(left.animate.move_to(xy(-1.95, -2.94)), right.animate.move_to(xy(1.95, -2.94)),
                  run_time=0.85)
        self.at("phenotype truly wins")
        self.play(Indicate(right.label, color=GREEN, scale_factor=1.08), run_time=1.45)
        self.finish()


class S09ContactLimit(SpokenScene):
    def construct(self):
        frame = world()
        result = set_live(frame)
        bob(result, amp=0.09, speed=3.3)
        former = genes(missing=("ced-9", "ced-3"))
        order = order_arrow()
        title = top("Double mutant: Lives", GREEN)
        badges = VGroup(single_badge("ced-9", False, -1.95), single_badge("ced-3", True, 1.95))
        self.add(frame, frame.cell, former, result, order, title, badges, scope_tag(size=28, color=TEXT))

        self.at("genetic order does")
        self.play(FadeOut(former), FadeOut(title), FadeOut(badges),
                  order.animate.put_start_and_end_on(xy(-3.05, -1.88), xy(1.97, -1.88)), run_time=1.1)
        distinction = top("Order and contact", GOLD)
        self.play(FadeIn(distinction), run_time=0.60)
        self.at("The textbook cartoon", lead=0.72)
        ced9 = gate(-3.05, PURPLE, "CED-9")
        ced4 = gate(-0.98, BLUE, "CED-4")
        ced3 = gate(1.97, ORANGE, "CED-3")
        self.play(FadeIn(ced9, shift=RIGHT * 0.3), FadeIn(ced4), FadeIn(ced3), run_time=0.85)
        self.at("holding CED 4", lead=0.35)
        clasp = DashedLine(xy(-2.32), xy(-1.70), dash_length=0.10,
                           dashed_ratio=0.56, color=PURPLE, stroke_width=5)
        self.play(Create(clasp), run_time=0.70)
        self.at("switches on CED")
        activation = arrow(xy(-0.22), xy(1.18), BLUE)
        self.play(GrowArrow(activation), run_time=0.85)
        self.at("The phenotype stand")
        self.play(Indicate(frame.lives.label, color=GREEN, scale_factor=1.06), run_time=1.05)
        self.at("mechanism stays less settled")
        self.play(FadeOut(clasp), FadeOut(activation), run_time=1.60)
        self.at("A 2024 study")
        assays = top("2024 assays", GOLD)
        self.play(swap(distinction, assays), run_time=0.85)
        self.at("mutants that cannot bind")
        self.play(ced9.animate.shift(LEFT * 0.46), ced4.animate.shift(RIGHT * 0.30), run_time=1.95)
        self.at("still protected cells")
        self.play(Indicate(frame.lives.label, color=GREEN, scale_factor=1.08), run_time=1.65)
        self.finish()


WORM_X = (-3.95, -2.10, -0.25, 1.60)
WORM_GATE_WIDTH = 1.18
RELEASED_RESTRAINT_OPACITY = 0.62


def pathway_four():
    return VGroup(*(gate(x, GENE_COLORS[name], name, width=WORM_GATE_WIDTH)
                    for x, name in zip(WORM_X, ("EGL-1", "CED-9", "CED-4", "CED-3"))))


def worm_links():
    pad = WORM_GATE_WIDTH / 2 + 0.06
    block = inhibit(WORM_X[0] + pad, WORM_X[1] - pad, TEAL)
    restraint = inhibit(WORM_X[1] + pad, WORM_X[2] - pad)
    activation = arrow(xy(WORM_X[2] + pad), xy(WORM_X[3] - pad), BLUE)
    return block, restraint, activation


class S10UnlockedWorm(SpokenScene):
    def construct(self):
        frame = world()
        result = set_live(frame)
        old = VGroup(gate(-3.51, PURPLE, "CED-9"), gate(-0.68, BLUE, "CED-4"), gate(1.97, ORANGE, "CED-3"))
        order = arrow(xy(-3.05, -1.88), xy(1.97, -1.88), BLUE)
        assays = top("2024 assays", GOLD)
        self.add(frame, frame.cell, result, old, order, assays, scope_tag(size=28, color=TEXT))
        self.at("Within those limits")
        self.play(FadeOut(result), FadeOut(order), FadeOut(assays),
                  frame.lives.box.animate.set_fill(GREEN, opacity=0.16).set_stroke(GREEN, width=2.5), run_time=0.77)
        egl, brake, ced4_target, ced3_target = pathway_four()
        self.play(Transform(old[1], ced4_target), Transform(old[2], ced3_target),
                  FadeOut(old[0]), run_time=1.70)

        self.at("In 1986")
        stamp = top("1986", GOLD, 39)
        self.play(FadeIn(stamp), run_time=0.55)
        self.at("reported two cell death")
        self.play(old[1].halves.animate.set_fill(BLUE, opacity=0.72),
                  old[2].halves.animate.set_fill(ORANGE, opacity=0.72), run_time=1.15)
        self.at("CED 3 and CED")
        self.play(Indicate(old[2].label, color=ORANGE, scale_factor=1.07),
                  Indicate(old[1].label, color=BLUE, scale_factor=1.07), run_time=1.9)
        self.at("laboratory combined mutations")
        ced4, ced3 = old[1:]
        self.play(FadeOut(stamp), FadeIn(egl, shift=LEFT * 0.45), FadeIn(brake, shift=LEFT * 0.40), run_time=1.65)
        self.at("to order four genes")
        block, restraint, activation = worm_links()
        self.play(Create(restraint), ced4.halves.animate.set_fill(BLUE, opacity=0.30), run_time=1.15)

        self.at("EGL 1 blocks", lead=0.35)
        self.play(Create(block), brake.halves.animate.set_fill(PURPLE, opacity=0.20), run_time=0.95)
        self.at("holds back CED", lead=0.4)
        self.play(restraint.animate.set_opacity(RELEASED_RESTRAINT_OPACITY),
                  ced4.halves.animate.set_fill(BLUE, opacity=0.72), run_time=1.30)
        self.at("In turn CED 4", lead=0.35)
        self.play(GrowArrow(activation), run_time=0.62)
        self.at("switches on CED", lead=0.23)
        self.play(ced3.halves.animate.set_fill(ORANGE, opacity=0.78), run_time=0.46)
        living_cell(self, frame, False, run_time=1.45)
        self.finish()


YEAST_X = (-2.70, -0.36, 1.98)


def yeast_gate(x, name="SEC"):
    return gate(x, BLUE, name)


class S11UnlockedYeast(SpokenScene):
    def construct(self):
        frame = world()
        old = pathway_four()
        block, restraint, activation = worm_links()
        restraint.set_opacity(RELEASED_RESTRAINT_OPACITY)
        frame.dies.box.set_fill(RED, opacity=0.20).set_stroke(RED, width=5.2)
        dead = cell_at(xy(3.45, DEAD_Y), RED, radius=0.21)
        old[1].halves.set_fill(PURPLE, opacity=0.20)
        old[2].halves.set_fill(BLUE, opacity=0.72)
        old[3].halves.set_fill(ORANGE, opacity=0.78)
        self.add(frame, frame.cell, old, dead, block, restraint, activation, scope_tag(size=28, color=TEXT))

        self.at("Double mutants also")
        yeast = world(fates=False, yeast=True)
        self.play(FadeOut(old), FadeOut(block), FadeOut(restraint), FadeOut(activation), FadeOut(dead),
                  FadeOut(frame.lives), FadeOut(frame.dies), FadeOut(frame.tracks[1]), FadeOut(frame.tracks[2]),
                  Transform(frame.shell, yeast.shell), Transform(frame.tracks[0], yeast.tracks[0]), run_time=1.7)
        gates = VGroup(*(yeast_gate(x) for x in YEAST_X))
        self.at("yeast secretion", lead=0.50)
        self.play(FadeIn(gates, shift=RIGHT * 0.20), FadeOut(frame.cell), run_time=0.9)
        self.at("In 1980")
        year = top("1980", GOLD, 39)
        self.play(FadeIn(year), run_time=0.67)
        self.at("found 188 clones", lead=0.40)
        clones = take_home("188 clones", BLUE)
        self.play(FadeIn(clones), run_time=0.65)
        self.at("trapped the enzyme")
        queue = flow(YEAST_X[0] - 0.76, start=-5.42, count=8, speed=1.5)
        cargo_label = T("Invertase", 29, YELLOW).move_to(xy(-4.55, 0.72))
        self.add(queue)
        self.play(FadeIn(cargo_label), run_time=0.62)
        self.at("37 degrees Celsius", lead=0.38)
        temp = T("37 °C", 30, ORANGE).move_to(xy(-4.50, -0.99))
        self.play(FadeIn(temp), run_time=0.70)
        self.at("into 23 groups")
        groups = take_home("188 clones → 23 groups", BLUE)
        self.play(swap(clones, groups), run_time=0.75)

        self.at("Their sec numbers")
        # SEC12 (ER exit), SEC18 (vesicle fusion), SEC1 (terminal fusion).
        # Specific gates are representative landmarks, not the entire order of 23 groups.
        scrambled = ["SEC1", "SEC12", "SEC18"]
        for g, name, x in zip(gates, scrambled, YEAST_X):
            label = T(name, 32, BLUE).move_to(xy(x, 1.06))
            self.play(swap(g.label, label, run_time=0.36))
            g.remove(g.label)
            g.add(label)
            g.label = label
        self.at("so 1981 double mutants")
        later = top("1981  ·  Double mutants", GOLD)
        self.play(swap(year, later), FadeOut(temp), FadeOut(groups), run_time=0.76)
        self.at("ordered those handoffs", lead=0.50)
        # Lift the numbers clear while the three gate bodies change places.
        self.play(*(FadeOut(g.label) for g in gates), run_time=0.22)
        for g in gates:
            g.remove(g.label)
        offsets = (YEAST_X[2] - YEAST_X[0], YEAST_X[0] - YEAST_X[1], YEAST_X[1] - YEAST_X[2])
        self.play(*(g.animate(path_arc=angle).shift(RIGHT * dx)
                    for g, angle, dx in zip(gates, (2.35, 1.18, 1.18), offsets)), run_time=1.50)
        for g in gates:
            g.label.move_to(g.socket.get_center() + UP * 1.16)
        self.play(*(FadeIn(g.label) for g in gates), run_time=0.28)
        self.at("Combine two mutations")
        routing = flow(5.71, start=-5.42, count=9, speed=2.1)
        self.remove(queue)
        self.add(routing)
        self.at("winning outcome maps")
        starts = (-5.36, *(x + 0.77 for x in YEAST_X))
        ends = (*(x - 0.77 for x in YEAST_X), 5.82)
        handoffs = [arrow(xy(a), xy(b), GOLD) for a, b in zip(starts, ends)]
        self.play(LaggedStart(*(GrowArrow(a) for a in handoffs), lag_ratio=0.35), run_time=1.55)
        self.finish()


class S12End(EndCard):
    LINE = "Combine opposite mutants in a pathway: the later gene usually wins."
