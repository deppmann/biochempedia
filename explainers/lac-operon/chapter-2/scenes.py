"""Does the mutation stay or travel? — lac-operon chapter 2.

COLOR MAP (kept exactly from chapter 1)
  BLUE   = lacZ / lac genes
  RED    = lac repressor and lacI; also a blocking clamp
  GOLD   = operator
  YELLOW = inducer
  PURPLE = RNA polymerase
  GREEN  = reporter output / transcription on
  GREY   = DNA, cell, labels, inactive or broken parts

The two-rail cell is built only by partial_diploid(), so every continuing
scene has the same scale and landmark positions.
"""
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B58CD9"

CELL_W, CELL_H = 13.0, 5.0
RAIL_X0, RAIL_X1 = -5.35, 4.75
UPPER_Y, LOWER_Y = 1.15, -1.15
XI, XO, XZ, XLAMP = -4.15, -1.55, 0.75, 4.15


def locus_block(text, x, y, width, color, fill=0.24, size=28):
    box = RoundedRectangle(
        corner_radius=0.1, width=width, height=0.82,
        stroke_color=color, stroke_width=3,
        fill_color=color, fill_opacity=fill,
    ).move_to([x, y, 0])
    return VGroup(box, T(text, size, color).move_to(box))


def lamp(y, state="neutral"):
    colors = {"neutral": GREY, "off": GREY, "basal": GREEN, "on": GREEN}
    opacity = {"neutral": 0.08, "off": 0.02, "basal": 0.22, "on": 0.9}[state]
    col = colors[state]
    bulb = Circle(radius=0.42, stroke_color=col, stroke_width=4,
                  fill_color=col, fill_opacity=opacity).move_to([XLAMP, y, 0])
    rays = VGroup(*[
        Line(
            bulb.get_center() + 0.52 * np.array([np.cos(a), np.sin(a), 0]),
            bulb.get_center() + 0.72 * np.array([np.cos(a), np.sin(a), 0]),
            color=col, stroke_width=3,
        ) for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    rays.set_opacity(0.0 if state in ("neutral", "off") else (0.25 if state == "basal" else 0.95))
    return VGroup(bulb, rays)


def fracture(x, y, color=TEXT):
    return VMobject(stroke_color=color, stroke_width=4).set_points_as_corners([
        [x - 0.12, y + 0.36, 0], [x + 0.04, y + 0.12, 0],
        [x - 0.08, y - 0.06, 0], [x + 0.13, y - 0.34, 0],
    ])


def cross_over(mob, color=RED):
    return VGroup(
        Line(mob.get_corner(UL) + DR * 0.06, mob.get_corner(DR) + UL * 0.06,
             color=color, stroke_width=6),
        Line(mob.get_corner(UR) + DL * 0.06, mob.get_corner(DL) + UR * 0.06,
             color=color, stroke_width=6),
    )


def repressor(pos=(0, 0, 0), scale=1.0, open_clamp=False, label=False):
    """The same two-lobed gripping cartoon used in chapter 1."""
    l = RoundedRectangle(corner_radius=0.13, width=0.48, height=1.0,
                         stroke_color=RED, stroke_width=3,
                         fill_color=RED, fill_opacity=0.42)
    r = l.copy()
    l.shift(LEFT * 0.22)
    r.shift(RIGHT * 0.22)
    if open_clamp:
        l.rotate(0.28, about_point=l.get_bottom())
        r.rotate(-0.28, about_point=r.get_bottom())
    lobes = VGroup(l, r).scale(scale).move_to(pos)
    if not label:
        return lobes
    lab = T("repressor", 28, RED).next_to(lobes, RIGHT, buff=0.2)
    return VGroup(lobes, lab)


def operator_clamp(y, open_clamp=False):
    return repressor([XO, y + 0.95, 0], scale=0.72, open_clamp=open_clamp)


def inducer_badge(pos):
    dot = Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3,
                 fill_color=YELLOW, fill_opacity=0.9).move_to(pos)
    return VGroup(dot, T("inducer", 28, YELLOW).next_to(dot, RIGHT, buff=0.28))


def make_rail(y, name, i_state="normal", op_state="normal",
              reporter="Z+", lamp_state="neutral"):
    gaps = [
        (RAIL_X0, XI - 0.78),
        (XI + 0.78, XO - 0.52),
        (XO + 0.52, XZ - 0.93),
        (XZ + 0.93, XLAMP - 0.55),
    ]
    line = VGroup(*[Line([a, y, 0], [b, y, 0], color=GREY, stroke_width=7) for a, b in gaps])
    rail_name = boxed_label(name, color=GREY, size=24, pad=0.12,
                            fill_opacity=0.08).move_to([-5.02, y + 0.8, 0])
    i_text = "lacI+" if i_state == "normal" else "lacI−"
    igene = locus_block(i_text, XI, y, 1.35, RED)
    op_text = "O+" if op_state == "normal" else "Oc"
    op = locus_block(op_text, XO, y, 0.82, GOLD, size=26)
    rep_col = BLUE if reporter == "Z+" else GREY
    z = locus_block(reporter, XZ, y, 1.62, rep_col)
    light = lamp(y, lamp_state)
    g = VGroup(line, rail_name, igene, op, z, light)
    g.line, g.name_label, g.igene, g.op, g.reporter, g.lamp = line, rail_name, igene, op, z, light
    if i_state == "broken":
        g.icrack = fracture(XI - 0.75, y, TEXT)
        g.add(g.icrack)
    if op_state == "altered":
        g.crack = fracture(XO - 0.55, y, TEXT)
        g.add(g.crack)
    return g


def cell_outline():
    cell = RoundedRectangle(corner_radius=0.65, width=CELL_W, height=CELL_H,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.15).move_to([0, 0.15, 0])
    cell._breath_t = 0.0

    def breathe(mob, dt):
        mob._breath_t += dt
        phase = np.sin(1.15 * mob._breath_t)
        mob.set_stroke(width=3.2 + 1.25 * phase)
        mob.set_fill(opacity=0.15 + 0.018 * phase)

    cell.add_updater(breathe)
    return cell


def partial_diploid(upper=None, lower=None, roam=False):
    """The carried two-rail world; callers only choose the genetic state."""
    upper = upper or {}
    lower = lower or {}
    cell = cell_outline()
    top = make_rail(UPPER_Y, "chromosome", **upper)
    bottom = make_rail(LOWER_Y, "F′ lac copy", **lower)
    g = VGroup(cell, top, bottom)
    g.cell, g.upper, g.lower = cell, top, bottom
    if roam:
        free = repressor([4.9, 0.0, 0], scale=0.8)
        g.free = free
        g.add(free)
        bob(free, amp=0.12, speed=1.4, seed=2)
    return g


def hook_world():
    w = partial_diploid(
        upper={"i_state": "broken", "lamp_state": "on"},
        lower={"op_state": "altered", "lamp_state": "on"},
    )
    q = T("?", 76, TEXT, weight=BOLD).move_to([0, 2.08, 0])
    no_inducer = chip("no inducer", YELLOW, 28).move_to([3.0, 2.22, 0])
    w.add(q, no_inducer)
    w.question, w.no_inducer = q, no_inducer
    pulse(w.upper.lamp[0], base=4, amp=1.5, speed=2.1)
    pulse(w.lower.lamp[0], base=4, amp=1.5, speed=2.4)
    return w


def predict_world(roam=True):
    return partial_diploid(
        upper={"i_state": "normal", "op_state": "altered", "reporter": "Z−", "lamp_state": "off"},
        lower={"i_state": "broken", "op_state": "normal", "reporter": "Z+", "lamp_state": "neutral"},
        roam=roam,
    )


class S01Hook(SpokenScene):
    def construct(self):
        cell = cell_outline()
        rail = make_rail(0, "one lac copy", lamp_state="neutral")
        clamp = operator_clamp(0)
        self.play(FadeIn(cell), Create(rail.line), FadeIn(rail.op), FadeIn(rail.reporter),
                  FadeIn(rail.name_label), run_time=0.8)
        self.at("repressor moving")
        self.play(FadeIn(clamp, shift=UP * 0.35), run_time=0.45)
        self.play(clamp.animate.shift(UP * 1.15), run_time=0.7)
        self.play(clamp.animate.shift(DOWN * 1.15), run_time=0.7)

        final = hook_world()
        self.at("broken repressor")
        self.play(FadeOut(VGroup(cell, rail, clamp)), FadeIn(final.cell),
                  FadeIn(final.upper), run_time=0.8)
        self.at("broken operator")
        self.play(FadeIn(final.lower), run_time=0.8)
        self.at("both look constitutive")
        self.play(FadeIn(final.no_inducer), FadeIn(final.upper.lamp),
                  FadeIn(final.lower.lamp), run_time=0.7)
        self.at("how can another")
        self.play(FadeIn(final.question, scale=0.7), run_time=0.5)
        self.play(Wiggle(final.question, scale_value=1.08, rotation_angle=0.03 * TAU), run_time=0.8)
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        w = hook_world()
        w.question.set_opacity(0.2)
        title = fit_text("Does the Mutation Stay or Travel?", max_w=9.5, size=44,
                         color=TEXT, max_lines=2, font=TITLE_FONT)
        title.move_to([0.0, 3.18, 0])
        self.add(w)
        self.play(FadeOut(w.question), FadeOut(w.no_inducer), run_time=0.35)
        self.play(Write(title), run_time=0.55)
        self.add(scope_tag("schematic"))
        self.play(FadeOut(title), run_time=0.8)
        self.finish()


class S03Partial(SpokenScene):
    def construct(self):
        cell = cell_outline()
        chromosome = Ellipse(width=7.6, height=3.9, color=GREY, stroke_width=6).move_to([-1.1, 0.1, 0])
        fprime = Ellipse(width=2.8, height=1.7, color=GREY, stroke_width=6).move_to([3.45, 0.15, 0])
        lac_a = locus_block("lac region", -1.1, 0.75, 2.0, BLUE)
        lac_b = locus_block("F′ lac", 3.45, 0.15, 1.5, BLUE)
        self.play(FadeIn(cell), Create(chromosome), run_time=0.8)
        self.at("F' lac copy")
        self.play(Create(fprime), FadeIn(lac_a), FadeIn(lac_b), run_time=0.9)

        world = partial_diploid()
        self.at("partial diploid")
        self.play(ReplacementTransform(VGroup(chromosome, lac_a), world.upper),
                  ReplacementTransform(VGroup(fprime, lac_b), world.lower), run_time=1.3)
        self.at("only for that region")
        region = VGroup(
            SurroundingRectangle(VGroup(world.upper.op, world.upper.reporter), color=BLUE, buff=0.18, stroke_width=3),
            SurroundingRectangle(VGroup(world.lower.op, world.lower.reporter), color=BLUE, buff=0.18, stroke_width=3),
        )
        self.play(Create(region), run_time=0.7)
        self.play(FadeOut(region), run_time=0.5)
        self.at("Each rail carries")
        self.play(LaggedStart(Indicate(world.upper.op, color=GOLD), Indicate(world.lower.op, color=GOLD), lag_ratio=0.3), run_time=0.9)
        self.at("lacZ reporter")
        self.play(LaggedStart(Indicate(world.upper.reporter, color=BLUE), Indicate(world.lower.reporter, color=BLUE), lag_ratio=0.3), run_time=0.9)
        shared = repressor([0, 2.05, 0], scale=0.82, label=True)
        self.at("same pool")
        self.play(FadeIn(shared, shift=DOWN * 0.2), run_time=0.6)
        self.play(shared.animate.shift(RIGHT * 2.0), run_time=0.7)
        self.play(shared.animate.shift(LEFT * 4.0), run_time=0.9)
        self.finish()


class S04Method(SpokenScene):
    def construct(self):
        world = partial_diploid(roam=True)
        self.add(world)
        ring = Circle(radius=1.02, color=GREEN, stroke_width=6).move_to(world.lower.reporter)
        checklist = Ledger([
            ("1", "reporter", GREEN),
            ("2", "linked operator", GOLD),
            ("3", "reachable repressor", RED),
        ], top_left=(-3.0, 3.58), title="read in this order", row_h=0.5,
           key_w=0.6, width=6.0, size=28)
        self.at("Read the reporter")
        self.play(Create(ring), FadeIn(checklist), checklist.reveal(0), run_time=0.8)
        self.at("working lacC")
        self.play(ring.animate.move_to(world.lower.reporter), Indicate(world.lower.reporter, color=GREEN), run_time=0.7)
        self.at("Then check")
        self.play(ring.animate.set_color(GOLD).move_to(world.lower.op).scale(0.72),
                  checklist.reveal(1), run_time=0.8)
        self.at("Finally ask")
        self.play(FadeOut(ring), checklist.reveal(2),
                  Indicate(world.free, color=RED), run_time=0.8)
        self.at("can reach that operator")
        self.play(world.free.animate.move_to([XO, LOWER_Y + 0.75, 0]), run_time=1.1)
        self.at("prevents a broken reporter")
        self.play(Indicate(world.upper.reporter, color=GREY), run_time=0.6)
        self.play(Wiggle(world.upper.reporter, scale_value=1.05, rotation_angle=0.02 * TAU), run_time=0.7)
        self.finish()


class S05Product(SpokenScene):
    def construct(self):
        world = partial_diploid(
            upper={"i_state": "broken", "lamp_state": "neutral"},
            lower={"i_state": "normal", "lamp_state": "neutral"},
        )
        self.add(world.cell, world.upper, world.lower)
        self.at("no working repressor")
        self.play(Indicate(world.upper.igene, color=RED), run_time=0.7)

        r1 = repressor([XI + 0.5, LOWER_Y + 1.15, 0], scale=0.75)
        r2 = r1.copy().shift(RIGHT * 0.55 + UP * 0.35)
        self.at("other rail makes")
        self.play(FadeIn(r1, shift=UP * 0.25), FadeIn(r2, shift=UP * 0.25), run_time=0.8)
        self.at("diffuses through")
        self.play(r1.animate.move_to([-2.7, 0.05, 0]),
                  r2.animate.move_to([-1.8, 0.05, 0]), run_time=0.8, rate_func=linear)
        self.play(r1.animate.move_to([0.4, 2.3, 0]),
                  r2.animate.move_to([2.0, 0.0, 0]), run_time=0.8, rate_func=linear)
        self.play(r1.animate.move_to([XO, UPPER_Y + 0.95, 0]),
                  r2.animate.move_to([2.0, 0.0, 0]), run_time=0.7, rate_func=linear)
        self.play(r2.animate.move_to([XO, LOWER_Y + 0.95, 0]), run_time=0.7, rate_func=linear)
        self.at("missing product arrives")
        arrows = VGroup(
            CurvedArrow([-3.4, 2.25, 0], [-2.1, 2.05, 0], angle=-0.3, color=RED),
            CurvedArrow([-3.4, 0.15, 0], [-2.1, -0.15, 0], angle=0.3, color=RED),
        )
        self.play(Create(arrows), run_time=0.8)
        complemented = caption("The product from the other copy complements lacI−.", color=RED)
        self.at("defect is complemented")
        self.play(FadeIn(complemented), run_time=0.6)
        self.at("is recessive")
        self.play(Indicate(world.upper.igene, color=RED), run_time=0.7)

        ind1 = inducer_badge([-0.55, UPPER_Y + 1.05, 0])
        ind2 = inducer_badge([0.8, LOWER_Y + 0.72, 0])
        self.at("Inducer can still")
        self.play(FadeOut(VGroup(arrows, complemented)), FadeIn(ind1), FadeIn(ind2), run_time=0.7)
        self.play(r1.animate.shift(RIGHT * 1.0).rotate(0.28),
                  r2.animate.shift(RIGHT * 1.0).rotate(-0.28), run_time=1.0)
        self.finish()


class S06Cis(SpokenScene):
    def construct(self):
        world = partial_diploid(
            upper={"op_state": "normal", "reporter": "Z+", "lamp_state": "neutral"},
            lower={"op_state": "normal", "reporter": "Z+", "lamp_state": "basal"},
            roam=True,
        )
        clamp = operator_clamp(LOWER_Y)
        self.add(world, clamp)
        altered = make_rail(UPPER_Y, "chromosome", op_state="altered", reporter="Z+", lamp_state="on")
        self.at("change an operator")
        self.play(Transform(world.upper.op, altered.op), FadeIn(altered.crack), run_time=0.8)
        self.at("never leaves its rail")
        anchor = Line([XO, UPPER_Y - 0.82, 0], [XO, UPPER_Y - 0.52, 0], color=GOLD, stroke_width=5)
        self.play(Create(anchor), run_time=0.6)
        self.at("No other copy")
        self.play(world.free.animate.move_to([XO, UPPER_Y + 0.9, 0]), run_time=0.9)
        self.play(Wiggle(world.free, scale_value=1.06, rotation_angle=0.04 * TAU), run_time=0.6)
        self.at("site cannot diffuse")
        local = CurvedArrow([XO - 0.25, UPPER_Y - 0.45, 0], [XZ - 0.6, UPPER_Y - 0.45, 0],
                            angle=0.35, color=GOLD, stroke_width=5)
        self.play(Create(local), run_time=0.7)
        self.at("working reporter escapes")
        self.play(Transform(world.upper.lamp, altered.lamp), run_time=0.8)
        pulse(world.upper.lamp[0], base=4, amp=1.8, speed=2.2)
        self.at("normal operator remains")
        self.play(Indicate(world.lower.op, color=GOLD), run_time=0.6)
        ind = inducer_badge([0.5, LOWER_Y + 1.0, 0])
        self.at("remains inducible")
        self.play(FadeIn(ind), clamp.animate.shift(RIGHT * 1.0).rotate(-0.25), run_time=0.9)
        self.play(world.lower.lamp[0].animate.set_fill(GREEN, opacity=0.9),
                  world.lower.lamp[1].animate.set_opacity(0.95), run_time=0.7)
        self.finish()


class S07Predict(SpokenScene):
    QUESTION = "Will the reporter remain controllable by inducer?"

    def construct(self):
        world = predict_world(roam=True)
        self.play(FadeIn(world), run_time=0.7)
        self.at("only working reporter")
        self.play(Indicate(world.lower.reporter, color=GREEN), run_time=0.8)
        self.at("normal operator")
        self.play(Indicate(world.lower.op, color=GOLD), run_time=0.7)
        self.at("comes from the other")
        self.play(Indicate(world.upper.igene, color=RED), run_time=0.6)
        self.play(world.free.animate.move_to([0.1, 2.25, 0]), run_time=0.8)
        q = question_card(self.QUESTION, y=-3.25, size=30)
        self.at("Will the reporter")
        self.play(FadeIn(q.question), run_time=0.6)
        self.play(Wiggle(world.lower.lamp, scale_value=1.08, rotation_angle=0.02 * TAU), run_time=0.8)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Will the reporter remain controllable by inducer?"
    SECONDS = 4.5
    CARD = {"y": -3.25, "size": 30}

    def backdrop(self):
        return predict_world(roam=True)


class S09Reveal(SpokenScene):
    def construct(self):
        world = predict_world(roam=False)
        rep = repressor([0.0, 2.25, 0], scale=0.8)
        self.add(world, rep)
        yes = T("YES", 42, GREEN, weight=BOLD).move_to([3.0, 3.15, 0])
        self.play(FadeIn(yes, scale=0.7), run_time=0.5)
        self.at("repressor reaches")
        self.play(rep.animate.move_to([XO, LOWER_Y + 0.95, 0]), run_time=1.2, rate_func=linear)
        self.at("Without inducer")
        basal = lamp(LOWER_Y, "basal")
        self.play(Transform(world.lower.lamp, basal), FadeOut(yes), run_time=0.7)
        basal_label = T("low basal", 28, GREEN).next_to(world.lower.lamp, UP, buff=0.2)
        self.at("low basal level")
        self.play(FadeIn(basal_label), run_time=0.6)

        ind = inducer_badge([0.3, LOWER_Y + 1.2, 0])
        self.at("With inducer")
        self.play(FadeOut(basal_label), run_time=0.25)
        self.play(FadeIn(ind), run_time=0.35)
        self.at("clamp opens")
        self.play(rep.animate.shift(RIGHT * 1.0).rotate(0.3), run_time=0.8)
        self.play(FadeOut(ind), run_time=0.25)
        pol = locus_block("RNA pol", -3.0, LOWER_Y + 0.98, 1.55, PURPLE, size=26)
        self.play(FadeIn(pol), run_time=0.4)
        self.play(pol.animate.move_to([3.0, LOWER_Y + 0.98, 0]), run_time=1.2, rate_func=linear)
        on = lamp(LOWER_Y, "on")
        self.play(Transform(world.lower.lamp, on), FadeOut(pol), run_time=0.7)
        self.at("inducible for active")
        result = caption("Active enzyme: inducible", color=GREEN)
        self.play(FadeIn(result), run_time=0.6)
        self.at("altered operator")
        self.play(Indicate(world.upper.op, color=GOLD), run_time=0.6)
        self.at("broken reporter")
        self.play(Indicate(world.upper.reporter, color=GREY), run_time=0.6)
        self.finish()


class S10Swap(SpokenScene):
    def construct(self):
        world = predict_world(roam=False)
        world.lower.lamp.become(lamp(LOWER_Y, "on"))
        self.add(world)
        top_z = world.upper.reporter
        bottom_z = world.lower.reporter
        self.at("Swap the reporters")
        self.play(top_z.animate.move_to([XZ, LOWER_Y, 0]),
                  bottom_z.animate.move_to([XZ, UPPER_Y, 0]), run_time=1.5)
        self.at("operators fixed")
        self.play(Indicate(world.upper.op, color=GOLD), Indicate(world.lower.op, color=GOLD), run_time=0.7)
        self.at("working reporter sits")
        self.play(Indicate(bottom_z, color=GREEN), run_time=0.7)
        top_on = lamp(UPPER_Y, "on")
        self.play(Transform(world.upper.lamp, top_on),
                  Transform(world.lower.lamp, lamp(LOWER_Y, "off")), run_time=0.7)
        absent = chip("inducer absent", YELLOW, 28).move_to([-2.1, -3.12, 0])
        present = chip("inducer present", YELLOW, 28).move_to([2.0, -3.12, 0])
        self.at("with or without")
        self.play(FadeIn(absent), run_time=0.45)
        self.play(FadeIn(present), run_time=0.45)
        pulse(world.upper.lamp[0], base=4, amp=2, speed=2.3)
        bracket = BraceBetweenPoints([XO - 0.4, UPPER_Y - 0.65, 0],
                                     [XZ + 0.8, UPPER_Y - 0.65, 0], color=GOLD, direction=DOWN)
        cis = T("linked", 28, GOLD).next_to(bracket, DOWN, buff=0.12)
        self.at("phenotype follows")
        self.play(FadeOut(VGroup(absent, present)), GrowFromCenter(bracket), FadeIn(cis), run_time=0.8)
        self.at("linkage to the DNA site")
        self.play(Indicate(VGroup(world.upper.op, bottom_z), color=GOLD), run_time=0.8)
        no_travel = T("not a travelling signal", 30, GREY).move_to([2.9, -3.12, 0])
        self.at("not a signal")
        self.play(FadeIn(no_travel), run_time=0.6)
        self.finish()


class S11Special(SpokenScene):
    def construct(self):
        world = partial_diploid(roam=False)
        rep = repressor([1.35, 2.0, 0], scale=0.78)
        self.add(world, rep)
        never = T("No purified repressor needed", 32, TEXT).move_to([-1.2, 3.15, 0])
        self.at("never needed")
        self.play(FadeIn(never), run_time=0.7)
        outline = DashedVMobject(SurroundingRectangle(rep, color=RED, buff=0.22, stroke_width=3), num_dashes=20)
        inferred = T("inferred from genetics", 28, RED).move_to([-1.2, 3.15, 0])
        self.at("Geneticists mapped")
        self.play(FadeOut(never), Create(outline), FadeIn(inferred), run_time=0.9)
        arrows = VGroup(DoubleArrow([2.75, -0.35, 0], [2.75, 1.75, 0],
                                    buff=0, color=RED, stroke_width=4, tip_length=0.18))
        self.at("traveling product")
        self.play(Create(arrows), rep.animate.shift(RIGHT * 0.7), run_time=1.0)
        isolated = boxed_label("isolated later: a protein", color=RED, size=28).move_to([-1.2, 3.15, 0])
        self.at("later isolated")
        self.play(FadeOut(inferred), FadeIn(isolated), FadeOut(outline), run_time=0.8)
        self.at("found a protein")
        self.play(Indicate(rep, color=RED), run_time=0.7)
        same = caption("The genetic rules did not change.", color=TEXT)
        self.at("rules did not change")
        self.play(FadeIn(same), Indicate(arrows, color=RED), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


def cis_panel():
    rail = VGroup(Line([-2.1, 0, 0], [-1.5, 0, 0], color=GREY, stroke_width=7),
                  Line([-0.5, 0, 0], [0.0, 0, 0], color=GREY, stroke_width=7),
                  Line([1.5, 0, 0], [2.1, 0, 0], color=GREY, stroke_width=7))
    op = locus_block("Oc", -1.0, 0, 0.8, GOLD, size=26)
    z = locus_block("Z+", 0.75, 0, 1.3, BLUE)
    br = BraceBetweenPoints([-1.4, -0.62, 0], [1.4, -0.62, 0], color=GOLD, direction=DOWN)
    lab = T("cis: stays linked", 28, GOLD).next_to(br, DOWN, buff=0.12)
    return VGroup(rail, op, fracture(-1.42, 0), z, br, lab)


def trans_panel():
    rails = VGroup(Line([-2.1, 0.65, 0], [2.1, 0.65, 0], color=GREY, stroke_width=7),
                   Line([-2.1, -0.65, 0], [2.1, -0.65, 0], color=GREY, stroke_width=7))
    rep = repressor([0, 0, 0], scale=0.75)
    arrows = VGroup(CurvedArrow([-1.5, 0.45, 0], [1.4, -0.45, 0], angle=-0.45, color=RED),
                    CurvedArrow([-1.5, -0.45, 0], [1.4, 0.45, 0], angle=0.45, color=RED))
    lab = T("trans: reaches both", 28, RED).move_to([0, -1.45, 0])
    return VGroup(rails, arrows, rep, lab)


class S12Rule(SpokenScene):
    def construct(self):
        panels = TwoPanel("local DNA site", "shared cellular product", colors=(GOLD, RED),
                          top=3.0, bottom=-2.25, size=32)
        left, right = cis_panel(), trans_panel()
        panels.put(left, "left")
        panels.put(right, "right")
        self.play(FadeIn(panels), run_time=0.7)
        self.at("location into evidence")
        self.play(FadeIn(left), FadeIn(right), run_time=0.8)
        self.at("stays linked")
        self.play(Indicate(left, color=GOLD), run_time=0.8)
        self.at("control site")
        self.play(Indicate(left[1], color=GOLD), run_time=0.6)
        self.at("reaches both rails")
        self.play(Indicate(right[1], color=RED), run_time=0.8)
        self.at("diffusible regulator")
        self.play(right[2].animate.shift(UP * 0.75), run_time=0.6)
        self.play(right[2].animate.shift(DOWN * 1.5), run_time=0.8)
        bob(right[2], amp=0.09, speed=1.6, seed=3)
        self.at("separates a local")
        rule = caption("Local DNA site  ↔  shared cellular product", color=TEXT)
        self.play(FadeIn(rule), run_time=0.7)
        first = boxed_label("WORKING REPORTER FIRST", color=GREEN, size=30).move_to([0, -3.02, 0])
        self.at("Always read")
        self.play(FadeOut(rule), FadeIn(first, shift=UP * 0.15), run_time=0.7)
        self.play(Indicate(first, color=GREEN), run_time=0.8)
        self.finish()


class S13End(EndCard):
    LINE = "DNA sites act in cis; diffusible regulators can act in trans."
