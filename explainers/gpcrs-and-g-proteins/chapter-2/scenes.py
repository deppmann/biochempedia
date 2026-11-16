"""Above, At, or Below Basal — chapter 2.

COLOR MAP (carried from chapter 1)
  BLUE    receptor
  GOLD    agonist / ligand
  PURPLE  G-alpha
  TEAL    beta-gamma
  GREY    GDP, membrane, structure
  GREEN   GTP and response
  TEXT    neutral antagonist edge
  RED     inverse agonist edge
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
RECEPTOR_XS = (-5.35, -4.20, -3.05, -1.90, -0.75, 0.40)
MEMBRANE_Y = 0.65
BASAL, HIGH, LOW = 0.42, 0.82, 0.13
METER_X, METER_BOTTOM, METER_HEIGHT = 4.35, -2.25, 4.75


def receptor(x=0, active=False, scale=1.0, color=BLUE):
    """A labelled-cartoon receptor; the cytoplasmic ends open in the active shape."""
    top = MEMBRANE_Y + 1.36 * scale
    bars = VGroup()
    for sign in (-1, 1):
        bar = RoundedRectangle(
            corner_radius=0.12 * scale, width=0.30 * scale, height=2.55 * scale,
            stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.32,
        ).move_to([x + sign * 0.19 * scale, top - 1.28 * scale, 0])
        if active:
            bar.rotate(sign * 0.18, about_point=np.array([x + sign * 0.19 * scale, top, 0]))
        bars.add(bar)
    pocket = Arc(radius=0.27 * scale, start_angle=PI, angle=PI, color=color,
                 stroke_width=4, arc_center=[x, top + 0.01 * scale, 0])
    return VGroup(bars, pocket)


def ligand(x, y, edge=GOLD, fill=None, scale=1.0):
    """A plain ligand block, never a molecular structure."""
    fill = edge if fill is None else fill
    return RoundedRectangle(
        corner_radius=0.12, width=0.48 * scale, height=0.34 * scale,
        stroke_color=edge, stroke_width=4, fill_color=fill, fill_opacity=0.55,
    ).move_to([x, y, 0])


def meter(level=BASAL, x=METER_X, title="schematic response", show_basal=True, width=1.15):
    """Shared response meter. The tracker and fill are returned for live animation."""
    tracker = ValueTracker(level)
    frame = RoundedRectangle(
        corner_radius=0.12, width=width, height=METER_HEIGHT, stroke_color=GREY,
        stroke_width=3, fill_color=BG, fill_opacity=0.15,
    ).move_to([x, METER_BOTTOM + METER_HEIGHT / 2, 0])

    def make_fill():
        h = max(0.04, tracker.get_value() * (METER_HEIGHT - 0.12))
        return Rectangle(width=width - 0.12, height=h, stroke_width=0,
                         fill_color=GREEN, fill_opacity=0.78).move_to(
            [x, METER_BOTTOM + 0.06 + h / 2, 0]
        )

    fill = always_redraw(make_fill)
    ttl = T(title, 28, TEXT).move_to([x, 2.95, 0])
    zero = T("zero", 24, GREY).next_to(frame, DOWN, buff=0.14)
    static = VGroup(frame, ttl, zero)
    basal_line = VGroup()
    if show_basal:
        yy = METER_BOTTOM + 0.06 + BASAL * (METER_HEIGHT - 0.12)
        line = DashedLine([x - width / 2 - 0.20, yy, 0], [x + width / 2 + 0.20, yy, 0],
                          color=GOLD, stroke_width=4, dash_length=0.13)
        lab = T("basal activity", 28, GOLD).move_to([x - 1.80, yy - 0.52, 0])
        basal_line.add(line, lab)
    return static, fill, basal_line, tracker


def receptor_world(active=(1, 4), level=BASAL, ligands=None, show_basal=True):
    """The carried receptor population, rebuilt at identical coordinates in every scene."""
    membrane = RoundedRectangle(
        corner_radius=0.12, width=7.45, height=0.54, stroke_color=GREY,
        stroke_width=3, fill_color=GREY, fill_opacity=0.23,
    ).move_to([-2.48, MEMBRANE_Y, 0])
    receptors = VGroup(*[receptor(x, i in active) for i, x in enumerate(RECEPTOR_XS)])
    gas = VGroup(*[
        boxed_label("Gα", PURPLE, size=24, box=(0.72, 0.48), pad=0.10).move_to([x, -1.18, 0])
        for x in RECEPTOR_XS
    ])
    static, fill, basal_line, tracker = meter(level=level, show_basal=show_basal)
    ligs = VGroup()
    for i, edge, fill_col in (ligands or []):
        ligs.add(ligand(RECEPTOR_XS[i], MEMBRANE_Y + 1.47, edge=edge, fill=fill_col))
    world = VGroup(membrane, receptors, gas, static, fill, basal_line, ligs)
    return world, receptors, gas, static, fill, basal_line, tracker, ligs


def hook_world():
    """The exact picture carried from the spoken hook into the predict pause and title."""
    membrane = RoundedRectangle(corner_radius=0.12, width=5.2, height=0.58, stroke_color=GREY,
                                stroke_width=3, fill_color=GREY, fill_opacity=0.23).move_to([-2.2, 0.45, 0])
    rec = receptor(-2.2, True, scale=1.45)
    static, fill, basal_line, tracker = meter(level=BASAL, x=3.0, show_basal=False, width=1.3)
    ys = [METER_BOTTOM + (METER_HEIGHT - 0.12) * v for v in (HIGH, BASAL, LOW)]
    destinations = VGroup(*[
        VGroup(DashedLine([3.80, y, 0], [5.05, y, 0], color=GREY, stroke_width=3),
               T("?", 38, GOLD).move_to([5.42, y, 0])) for y in ys
    ])
    question = question_card("Where can a ligand move the response?", y=-3.18, size=34, max_w=10.8)
    return VGroup(membrane, rec, static, fill, destinations), rec, tracker, destinations, question


def pulse_to_galpha(x, color=PURPLE):
    return Arrow([x, -0.25, 0], [x, -0.87, 0], buff=0.04, color=color,
                 stroke_width=5, tip_length=0.16)


def shimmer_fill(mob, color=GREY, base=0.20, amp=0.12, speed=6.0, phase=0.0):
    """Keep a large assay panel visibly live while its measured endpoint holds steady."""
    mob._shimmer_t = phase

    def update(m, dt):
        m._shimmer_t += dt
        m.set_fill(color, opacity=base + amp * np.sin(speed * m._shimmer_t))
    return mob.add_updater(update)


class S01Hook(SpokenScene):
    def construct(self):
        world, rec, tr, destinations, question = hook_world()
        self.play(FadeIn(world[0]), FadeIn(world[1]), run_time=0.8)
        self.at("followed a receptor")
        g = boxed_label("Gα", PURPLE, size=28, box=(0.9, 0.58)).move_to([-2.2, -1.65, 0])
        self.play(FadeIn(g), GrowArrow(pulse_to_galpha(-2.2)), run_time=0.7)
        self.at("empty receptor already signals")
        self.play(FadeIn(world[2]), FadeIn(world[3]), tr.animate.set_value(BASAL), run_time=1.2)
        self.play(Transform(rec, receptor(-2.2, False, scale=1.45)), run_time=0.45)
        self.play(Transform(rec, receptor(-2.2, True, scale=1.45)), run_time=0.45)
        self.at("where can a ligand")
        self.play(FadeIn(destinations), FadeIn(question), run_time=0.9)
        self.finish()


class S02Predict(PredictPause):
    QUESTION = "Where can a ligand move the response?"
    SECONDS = 4.5
    CARD = {"y": -3.18, "size": 34, "max_w": 10.8}

    def backdrop(self):
        world, rec, tr, destinations, question = hook_world()
        pulse(destinations, base=3.0, amp=1.2, speed=2.0)
        bob(rec, amp=0.055, speed=1.7)
        return world


class S03Title(TitleCard):
    LESSON = "GPCRs and Trimeric G Proteins"
    TITLE = "Above, At, or Below Basal"

    def construct(self):
        world, rec, tr, destinations, question = hook_world()
        world[2].remove(world[2][1])
        world.set_opacity(0.36)
        self.add(world)
        bob(rec, amp=0.045, speed=1.6)
        title = T(self.TITLE, 44, TEXT, font=TITLE_FONT).move_to([-1.55, 3.18, 0])
        rule = Line([-3.25, 2.70, 0], [0.15, 2.70, 0], color=GOLD, stroke_width=5)
        self.play(FadeIn(title, shift=UP * 0.12), GrowFromCenter(rule), run_time=0.65)
        self.finish()


class S04Basal(SpokenScene):
    def construct(self):
        world, rs, gas, static, fill, basal_line, tr, ligs = receptor_world(active=(), level=0.02)
        self.play(FadeIn(world[0]), FadeIn(rs), run_time=0.9)
        bob(rs, amp=0.10, speed=2.0)
        self.at("every binding pocket is empty")
        empty = T("all pockets empty", 30, BLUE).move_to([-2.48, 3.05, 0])
        self.play(FadeIn(empty), LaggedStart(*[Indicate(r, color=BLUE, scale_factor=1.03) for r in rs], lag_ratio=0.12), run_time=1.2)
        self.at("sample less active")
        self.play(Transform(rs[1], receptor(RECEPTOR_XS[1], True)), run_time=0.7)
        self.play(Transform(rs[4], receptor(RECEPTOR_XS[4], True)), run_time=0.7)
        self.play(Transform(rs[1], receptor(RECEPTOR_XS[1], False)), run_time=0.6)
        self.at("active shapes engage")
        self.play(FadeIn(gas), GrowArrow(pulse_to_galpha(RECEPTOR_XS[4])), run_time=0.8)
        self.play(Transform(rs[1], receptor(RECEPTOR_XS[1], True)), GrowArrow(pulse_to_galpha(RECEPTOR_XS[1])), run_time=0.8)
        self.at("population produces basal")
        self.play(FadeOut(empty), FadeIn(static), FadeIn(fill), tr.animate.set_value(BASAL), run_time=1.5)
        self.at("starting signal becomes")
        self.play(FadeIn(basal_line), Indicate(basal_line, color=GOLD, scale_factor=1.02), run_time=1.1)
        self.play(Transform(rs[4], receptor(RECEPTOR_XS[4], False)), run_time=0.7)
        self.finish()


class S05Agonist(SpokenScene):
    def construct(self):
        world, rs, gas, static, fill, basal_line, tr, ligs = receptor_world(active=(1, 4), level=BASAL)
        self.add(world)
        bob(rs, amp=0.10, speed=2.0)
        self.at("raises signaling above")
        path = Arrow([5.75, -0.25, 0], [5.75, 1.55, 0], buff=0, color=GOLD, stroke_width=6, tip_length=0.22)
        self.play(GrowArrow(path), run_time=0.8)
        self.at("favors the more active")
        self.play(Transform(rs[0], receptor(RECEPTOR_XS[0], True)),
                  Transform(rs[3], receptor(RECEPTOR_XS[3], True)), run_time=1.0)
        self.at("Gold agonist blocks")
        agonists = VGroup(*[ligand(RECEPTOR_XS[i], 3.0, GOLD) for i in (0, 1, 3, 4)])
        self.play(FadeIn(agonists, shift=DOWN * 0.2), run_time=0.7)
        self.play(*[a.animate.move_to([RECEPTOR_XS[i], MEMBRANE_Y + 1.47, 0]) for a, i in zip(agonists, (0, 1, 3, 4))], run_time=1.2)
        self.at("More receptors remain")
        pulses = VGroup(*[pulse_to_galpha(RECEPTOR_XS[i]) for i in (0, 1, 3, 4)])
        self.play(LaggedStart(*[GrowArrow(a) for a in pulses], lag_ratio=0.15), run_time=1.1)
        self.at("meter rises")
        self.play(tr.animate.set_value(HIGH), run_time=1.4)
        label = boxed_label("agonist", GOLD, size=30).move_to([2.55, 2.15, 0])
        self.play(FadeIn(label), FadeOut(path), run_time=0.7)
        self.at("measured effect")
        self.play(Indicate(VGroup(fill, label), color=GOLD, scale_factor=1.01), run_time=1.0)
        self.finish()


class S06Antagonist(SpokenScene):
    def construct(self):
        world, rs, gas, static, fill, basal_line, tr, ligs = receptor_world(active=(1, 4), level=BASAL)
        self.add(world)
        bob(rs, amp=0.10, speed=2.1)
        self.at("neutral antagonist behaves")
        state = boxed_label("neutral antagonist", TEXT, size=30).move_to([-2.5, -2.55, 0])
        self.play(FadeIn(state), run_time=0.7)
        self.at("leaves basal signaling")
        self.play(Indicate(basal_line, color=GOLD, scale_factor=1.02), run_time=0.9)
        self.at("another ligand arrives")
        blockers = VGroup(*[ligand(x, 2.75, edge=TEXT, fill=BG) for x in RECEPTOR_XS[:5]])
        self.play(FadeIn(blockers), run_time=0.6)
        self.at("blocks occupy the pockets")
        self.play(*[b.animate.move_to([x, MEMBRANE_Y + 1.47, 0]) for b, x in zip(blockers, RECEPTOR_XS[:5])], run_time=1.2)
        self.at("incoming agonist finds")
        incoming = VGroup(*[ligand(x, 3.05, GOLD) for x in RECEPTOR_XS])
        self.play(FadeIn(incoming, shift=DOWN * 0.15), run_time=0.6)
        bounce = [a.animate.shift(UP * 0.45 + (LEFT if i % 2 else RIGHT) * 0.18) for i, a in enumerate(incoming[:5])]
        self.play(*bounce, incoming[5].animate.move_to([RECEPTOR_XS[5], MEMBRANE_Y + 1.47, 0]),
                  Transform(rs[5], receptor(RECEPTOR_XS[5], True)), run_time=1.1)
        self.play(incoming[:5].animate.shift(RIGHT * 0.28), GrowArrow(pulse_to_galpha(RECEPTOR_XS[5])), run_time=0.9)
        bob(incoming[:5], amp=0.055, speed=1.2)
        self.at("meter stays near basal")
        self.play(tr.animate.set_value(BASAL + 0.035), run_time=1.2)
        self.play(tr.animate.set_value(BASAL), run_time=0.6)
        self.at("Neutral describes")
        self.play(Indicate(VGroup(state, basal_line), color=TEXT, scale_factor=1.01), run_time=1.0)
        self.finish()


class S07Inverse(SpokenScene):
    def construct(self):
        world, rs, gas, static, fill, basal_line, tr, ligs = receptor_world(active=(1, 4), level=BASAL)
        self.add(world)
        bob(rs, amp=0.10, speed=2.0)
        self.at("moves the response below")
        arrow = Arrow([5.75, -0.2, 0], [5.75, -1.55, 0], buff=0, color=RED, stroke_width=6, tip_length=0.22)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.at("favors the less active")
        self.play(Transform(rs[1], receptor(RECEPTOR_XS[1], False)), run_time=0.8)
        self.at("Red edged ligand blocks")
        inv = VGroup(*[ligand(RECEPTOR_XS[i], 2.85, edge=RED, fill=BG) for i in (0, 1, 2, 4, 5)])
        self.play(FadeIn(inv), run_time=0.6)
        self.play(*[a.animate.move_to([RECEPTOR_XS[i], MEMBRANE_Y + 1.47, 0]) for a, i in zip(inv, (0, 1, 2, 4, 5))], run_time=1.1)
        self.play(Transform(rs[4], receptor(RECEPTOR_XS[4], False)), run_time=0.7)
        self.at("Fewer receptors engage")
        self.play(FadeOut(gas[0]), FadeOut(gas[2]), FadeOut(gas[3]), FadeOut(gas[5]), run_time=0.8)
        self.at("meter falls")
        self.play(tr.animate.set_value(LOW), run_time=1.5)
        label = boxed_label("inverse agonist", RED, size=30).move_to([1.95, -1.55, 0])
        self.play(FadeIn(label), FadeOut(arrow), run_time=0.7)
        self.at("signaling direction")
        self.play(Indicate(VGroup(fill, label), color=RED, scale_factor=1.01), run_time=1.0)
        self.finish()


def zero_panel(title, edge, ligand_name):
    panel = RoundedRectangle(corner_radius=0.18, width=5.9, height=5.25,
                             stroke_color=edge, stroke_width=3).move_to(ORIGIN)
    head = fit_text(title, max_w=5.0, size=30, color=edge).move_to([0, 2.15, 0])
    mem = Rectangle(width=4.3, height=0.48, stroke_color=GREY, stroke_width=2,
                    fill_color=GREY, fill_opacity=0.22).move_to([0, 0.38, 0])
    recs = VGroup(receptor(-0.7, False, scale=0.95), receptor(0.7, True, scale=0.95)).shift(UP * -0.27)
    ligs = VGroup(ligand(-0.7, 1.75, edge=edge, fill=BG), ligand(0.7, 1.75, edge=edge, fill=BG)).shift(DOWN * 0.27)
    zero = VGroup(Line([-1.25, -1.68, 0], [1.25, -1.68, 0], color=GREEN, stroke_width=8),
                  T("zero response", 30, GREEN).move_to([0, -2.10, 0]))
    return VGroup(panel, head, mem, recs, ligs, zero)


class S08Assay(SpokenScene):
    def construct(self):
        self.at("remove measurable basal")
        panels = TwoPanel("neutral antagonist", "inverse agonist", colors=(TEXT, RED), top=3.0, bottom=-2.45)
        self.play(FadeIn(panels), run_time=0.8)
        left = zero_panel("", TEXT, "neutral")
        right = zero_panel("", RED, "inverse")
        panels.put(left, "left"), panels.put(right, "right")
        # Panel frames and headings already come from TwoPanel.
        left[0].set_opacity(0); left[1].set_opacity(0)
        right[0].set_opacity(0); right[1].set_opacity(0)
        self.at("meter starts at zero")
        self.play(FadeIn(left[2:]), FadeIn(right[2:]), run_time=1.0)
        bob(left[3], amp=0.11, speed=2.0)
        bob(right[3], amp=0.11, speed=2.2, seed=2)
        self.at("neutral antagonist cannot")
        self.play(left[4][0].animate.move_to(left[3][0].get_top() + UP * 0.12), run_time=0.8)
        self.at("Neither can an inverse")
        self.play(right[4][0].animate.move_to(right[3][0].get_top() + UP * 0.12), run_time=0.8)
        self.at("they look the same")
        brace = BraceBetweenPoints([-3.0, -2.0, 0], [3.0, -2.0, 0], direction=DOWN, color=GOLD)
        same = T("indistinguishable here", 30, GOLD).next_to(brace, DOWN, buff=0.12)
        self.play(Create(brace), FadeIn(same), run_time=0.9)
        self.at("requires a receptor system")
        self.play(Indicate(VGroup(left[5], right[5]), color=GREEN, scale_factor=1.02), run_time=1.1)
        self.finish()


def comparison_meter(x, endpoint, color, title):
    frame = RoundedRectangle(corner_radius=0.14, width=2.15, height=4.35, stroke_color=GREY,
                             stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([x, 0.05, 0])
    yb = 0.75
    basal = DashedLine([x - 0.82, yb, 0], [x + 0.82, yb, 0], color=GOLD, stroke_width=4)
    end_y = -1.75 + 3.55 * endpoint
    change = Arrow([x, yb - 0.05, 0], [x, end_y, 0], buff=0.04, color=color,
                   stroke_width=7, tip_length=0.20)
    head = fit_text(title, max_w=2.5, size=29, color=color, max_lines=2).move_to([x, 2.65, 0])
    return VGroup(frame, basal, change, head)


class S09Model(SpokenScene):
    def construct(self):
        self.at("intermediate changes")
        full = comparison_meter(-2.15, 0.06, RED, "larger inverse effect")
        partial = comparison_meter(2.15, 0.27, GOLD, "carazolol")
        self.play(FadeIn(full[0:2]), FadeIn(partial[0:2]), run_time=0.8)
        self.play(GrowArrow(full[2]), GrowArrow(partial[2]), run_time=1.3)
        pulse(full[2], base=7.0, amp=1.4, speed=1.7)
        pulse(partial[2], base=7.0, amp=1.4, speed=1.9)
        pulse(full[0], base=3.0, amp=1.5, speed=1.55)
        pulse(partial[0], base=3.0, amp=1.5, speed=1.75)
        shimmer_fill(full[0], phase=0.0)
        shimmer_fill(partial[0], phase=0.7)
        self.at("saturating concentration")
        sats = VGroup(boxed_label("saturating", TEXT, size=26).move_to([-2.55, -2.55, 0]),
                      boxed_label("saturating", TEXT, size=26).move_to([2.55, -2.55, 0]))
        self.play(FadeIn(sats), run_time=0.7)
        self.at("Carizalol")
        self.play(FadeIn(partial[3]), run_time=0.6)
        beta = boxed_label("beta-2 receptor", BLUE, size=28).move_to([4.95, 1.68, 0])
        car = ligand(4.95, 0.85, edge=GOLD, fill=BG, scale=1.25)
        self.play(FadeIn(beta), FadeIn(car), run_time=0.8)
        self.at("partial inverse agonist")
        tag = T("partial inverse\nagonist", 28, RED, line_spacing=0.75).move_to([5.05, -0.38, 0])
        self.play(FadeIn(tag), run_time=0.7)
        self.at("without producing the full")
        self.play(FadeOut(sats), FadeOut(tag), run_time=0.35)
        bracket = BraceBetweenPoints([1.22, -2.02, 0], [3.08, -2.02, 0], direction=DOWN, color=GOLD)
        eff = T("partial efficacy", 28, GOLD).next_to(bracket, DOWN, buff=0.12)
        self.play(Create(bracket), FadeIn(eff), run_time=0.8)
        self.at("Efficacy means")
        self.play(Indicate(partial[2], color=GOLD, scale_factor=1.02), run_time=1.0)
        self.at("not incomplete binding")
        self.play(Indicate(car, color=GOLD, scale_factor=1.18), run_time=0.9)
        self.finish()


def ensemble_receptor(x):
    outlines = VGroup()
    for dx, opacity in ((-0.10, 0.28), (0, 0.80), (0.10, 0.28)):
        r = receptor(x + dx, active=(dx >= 0), scale=1.05)
        r.set_opacity(opacity)
        outlines.add(r)
    return outlines


class S10Model(SpokenScene):
    def construct(self):
        frame = RoundedRectangle(corner_radius=0.22, width=12.1, height=6.25, stroke_color=GREY,
                                 stroke_width=3).move_to([0, 0.15, 0])
        self.play(FadeIn(frame), run_time=0.6)
        pulse(frame, base=3.0, amp=1.4, speed=1.6)
        self.at("useful first model")
        rigid = VGroup(receptor(-4.8, False, scale=1.25), receptor(-3.45, True, scale=1.25))
        self.play(FadeIn(rigid), run_time=0.8)
        self.at("not a claim")
        ensembles = VGroup(ensemble_receptor(-4.8), ensemble_receptor(-3.45))
        self.play(ReplacementTransform(rigid, ensembles), run_time=1.1)
        self.at("sample ensembles")
        ens_lab = boxed_label("ensemble", BLUE, size=30).move_to([-4.15, -1.92, 0])
        self.play(FadeIn(ens_lab), run_time=0.7)
        self.at("one response in one cell")
        context = VGroup(boxed_label("one cell", TEAL, size=28), boxed_label("one response", GREEN, size=28))
        context.arrange(DOWN, buff=0.26).move_to([-0.85, 0.05, 0])
        self.play(FadeIn(context, shift=RIGHT * 0.15), run_time=0.8)
        self.at("may class differently")
        a = comparison_meter(2.15, 0.23, GOLD, "measured response A")
        b = comparison_meter(4.65, 0.23, GOLD, "measured response B")
        a.remove(a[3]); b.remove(b[3])
        a.scale(0.82); b.scale(0.82)
        ah = fit_text("measured response A", max_w=2.15, size=26, color=GOLD, max_lines=2).move_to([2.15, 2.55, 0])
        bh = fit_text("measured response B", max_w=2.15, size=26, color=GOLD, max_lines=2).move_to([4.65, 2.55, 0])
        a.add(ah); b.add(bh)
        self.play(FadeIn(a), run_time=0.8)
        self.play(FadeIn(b), run_time=0.8)
        same_lig = ligand(0.25, -2.12, edge=GOLD, fill=BG, scale=1.25)
        lig_lab = T("same ligand", 28, GOLD).next_to(same_lig, DOWN, buff=0.16)
        self.play(FadeIn(same_lig), FadeIn(lig_lab), run_time=0.7)
        self.at("Keep the meter and assay")
        self.play(Indicate(frame, color=GOLD, scale_factor=1.0), run_time=1.1)
        self.add(scope_tag("schematic"))
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        static, fill, basal_line, tr = meter(level=BASAL, x=0, title="schematic response", show_basal=True, width=1.45)
        basal_line[-1].move_to([-1.75, -2.80, 0])
        self.play(FadeIn(static), FadeIn(fill), FadeIn(basal_line), run_time=0.8)
        self.at("three questions")
        recs = VGroup(receptor(-4.65, False, scale=1.25), receptor(-3.25, True, scale=1.25))
        self.play(FadeIn(recs), run_time=0.7)
        bob(recs, amp=0.10, speed=2.0)
        pulse(static[0], base=3.0, amp=1.4, speed=1.7)
        self.at("raise signaling above")
        up = Arrow([1.25, -0.22, 0], [2.25, 1.65, 0], color=GOLD, stroke_width=6, tip_length=0.22)
        up_lab = boxed_label("agonist", GOLD, size=28).move_to([3.35, 2.45, 0])
        self.play(GrowArrow(up), tr.animate.set_value(HIGH), run_time=1.1)
        pulse(up, base=6.0, amp=1.2, speed=1.7)
        self.play(FadeIn(up_lab), run_time=0.5)
        self.at("leave basal unchanged")
        tr.set_value(BASAL)
        level = Arrow([1.25, -0.22, 0], [2.75, -0.22, 0], color=TEXT, stroke_width=6, tip_length=0.22)
        blocker = ligand(3.20, -0.22, edge=TEXT, fill=BG)
        level_lab = boxed_label("neutral antagonist", TEXT, size=28).move_to([4.65, 0.72, 0])
        self.play(GrowArrow(level), FadeIn(blocker), run_time=0.9)
        pulse(level, base=6.0, amp=1.2, speed=1.9)
        self.play(FadeIn(level_lab), run_time=0.5)
        self.at("lower signaling below")
        down = Arrow([1.25, -0.22, 0], [2.25, -1.65, 0], color=RED, stroke_width=6, tip_length=0.22)
        down_lab = boxed_label("inverse agonist", RED, size=28).next_to(down.get_end(), RIGHT, buff=0.20)
        self.play(GrowArrow(down), tr.animate.set_value(LOW), run_time=1.1)
        pulse(down, base=6.0, amp=1.2, speed=2.1)
        self.play(FadeIn(down_lab), run_time=0.5)
        self.at("Those observations'")
        self.play(Indicate(VGroup(up_lab, level_lab, down_lab), color=GOLD, scale_factor=1.01), run_time=1.1)
        self.at("without pretending")
        self.play(FadeOut(VGroup(static, fill, basal_line, recs, up, up_lab, level, blocker,
                                 level_lab, down, down_lab)), run_time=1.0)
        self.finish()


class S12End(EndCard):
    LINE = "Basal activity separates agonists, neutral antagonists, and inverse agonists."
