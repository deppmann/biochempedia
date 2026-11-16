"""How a membrane writes an address.

COLOR MAP (shared with chapter 1)
  BLUE   = proteins and protein readers
  YELLOW = lipid tails / grip
  RED    = positive charge and mutation/block marks
  GREEN  = address lipids and their visible signal
  PURPLE = writer and eraser enzymes
  GREY   = membrane and neutral geometry

Everything is schematic: lipids are badges over hidden tail strokes, never molecular structures.
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
CYTOSOL = "#202838"
MEM_Y = 1.25


def membrane(width=12.2, y=MEM_Y):
    """The carried plasma membrane, rebuilt at one scale and position."""
    return RoundedRectangle(
        corner_radius=0.12, width=width, height=0.72,
        stroke_color=GREY, stroke_width=3,
        fill_color=GREY, fill_opacity=0.24,
    ).move_to([0, y, 0])


def cytosol_field(width=12.4, top=0.88, bottom=-3.35):
    """A quiet, full-height cytosolic field that keeps the carried world visually substantial."""
    return RoundedRectangle(
        corner_radius=0.18, width=width, height=top - bottom,
        stroke_width=0, fill_color=CYTOSOL, fill_opacity=1,
    ).move_to([0, (top + bottom) / 2, 0]).set_z_index(-5)


def region_glow(x, width=3.2, opacity=0.18, y=MEM_Y):
    return RoundedRectangle(
        corner_radius=0.16, width=width, height=0.68,
        stroke_color=GREEN, stroke_width=0,
        fill_color=GREEN, fill_opacity=opacity,
    ).move_to([x, y, 0])


def lipid(x, kind="PIP2", y=MEM_Y, bright=False, scale=1.0):
    """A labelled head badge and two featureless hidden tails."""
    col = GREEN if kind == "PIP3" else GREY
    head = boxed_label(kind, col, size=28 / scale, pad=0.16 / scale,
                       fill_opacity=0.22 if bright else 0.10)
    head.label.set_color(TEXT)
    head.scale(scale).move_to([x, y - 0.02, 0])
    tails = VGroup(
        Line([x - 0.13 * scale, y + 0.38, 0], [x - 0.13 * scale, y + 0.76, 0], color=YELLOW, stroke_width=5),
        Line([x + 0.13 * scale, y + 0.38, 0], [x + 0.13 * scale, y + 0.76, 0], color=YELLOW, stroke_width=5),
    ).set_opacity(0.75)
    g = VGroup(tails, head)
    g.head, g.tails = head, tails
    return g


def enzyme(text, x=0, y=2.75, size=27):
    return boxed_label(text, PURPLE, size=size, pad=0.2, fill_opacity=0.22).move_to([x, y, 0])


def plain_protein(x, y=-0.65, name="protein", scale=1.0):
    body = RoundedRectangle(
        corner_radius=0.34, width=2.25, height=1.05,
        stroke_color=BLUE, stroke_width=4,
        fill_color=BLUE, fill_opacity=0.2,
    )
    lab = T(name, 30 / scale, BLUE, weight=BOLD).move_to(body)
    return VGroup(body, lab).scale(scale).move_to([x, y, 0])


def cup_protein(x, y=-0.75, name="reporter", scale=1.0, cup_color=BLUE):
    """The lesson's action-shape: a cup that can close around a lipid head."""
    body = plain_protein(0, 0, name=name)
    body.remove(body[1])
    lab = T(name, 30 / scale, BLUE, weight=BOLD).move_to(body[0])
    body[0].stretch_to_fit_width(max(2.25, lab.width + 0.55))
    body.add(lab)
    cup = Arc(radius=0.42, start_angle=PI, angle=PI, color=cup_color, stroke_width=7)
    cup.rotate(PI).move_to([0, 0.78, 0])
    g = VGroup(body, cup).scale(scale).move_to([x, y, 0])
    g.body, g.cup = body, cup
    return g


def two_region_world(reporter_x=0, reporter_y=-0.85, cup=False):
    """The carried predict/reader world, identical in scenes 5--8."""
    mem = VGroup(cytosol_field(), membrane())
    left = region_glow(-3.25, 4.6, 0.16)
    lipids = VGroup(
        lipid(-4.25, "PIP3", bright=True, scale=0.86),
        lipid(-3.25, "PIP3", bright=True, scale=0.86),
        lipid(-2.25, "PIP3", bright=True, scale=0.86),
        lipid(2.25, "PIP2", scale=0.86),
        lipid(3.25, "PIP2", scale=0.86),
        lipid(4.25, "PIP2", scale=0.86),
    )
    rep = cup_protein(reporter_x, reporter_y) if cup else plain_protein(reporter_x, reporter_y, "reporter")
    return VGroup(mem, left, lipids, rep), rep


def question_world(with_question=True):
    world, rep = two_region_world()
    labels = VGroup(
        T("PIP3 region", 30, GREEN, weight=BOLD).move_to([-3.25, 2.55, 0]),
        T("PIP2 region", 30, GREY, weight=BOLD).move_to([3.25, 2.55, 0]),
    )
    qmark = T("?", 62, GOLD, weight=BOLD).next_to(rep, DOWN, buff=0.2)
    g = VGroup(world, labels, qmark)
    if with_question:
        q = question_card("Where should a matching reader accumulate?", y=-3.22, max_w=9.8)
        g.add(q)
    return g


def writer_reader_eraser_row():
    w = enzyme("writer", -4.1, 0.2, 30)
    lipid_badge = boxed_label("address", GREEN, size=30, pad=0.22, fill_opacity=0.25).move_to([-1.35, 0.2, 0])
    r = cup_protein(1.5, -0.15, "reader", scale=0.8)
    e = enzyme("eraser", 4.4, 0.2, 30)
    a1 = Arrow(w.get_right(), lipid_badge.get_left(), buff=0.18, color=GREY, stroke_width=4, tip_length=0.18)
    a2 = Arrow(lipid_badge.get_right(), r.get_left(), buff=0.18, color=GREY, stroke_width=4, tip_length=0.18)
    a3 = Arrow(r.get_right(), e.get_left(), buff=0.18, color=GREY, stroke_width=4, tip_length=0.18)
    return VGroup(w, a1, lipid_badge, a2, r, a3, e)


import math


def drift(mob, amp=0.14, w=2.4, phase=0.0, sway=0.08):
    """Ambient drift: keeps a protein gently moving while the narrator talks."""
    clock = [phase]
    def _u(m, dt):
        clock[0] += dt
        m.shift(UP * amp * w * math.cos(w * clock[0]) * dt
                + RIGHT * sway * w * 0.7 * math.cos(w * 0.7 * clock[0] + 1.0) * dt)
    mob.add_updater(_u)
    return mob


class S00Hook(SpokenScene):
    def construct(self):
        mem = membrane(y=1.55)
        regions = VGroup(*[
            RoundedRectangle(corner_radius=0.12, width=3.55, height=0.72, stroke_width=2,
                             stroke_color=GREY, fill_opacity=0).move_to([x, 1.55, 0])
            for x in (-4.0, 0, 4.0)
        ])
        proteins = VGroup(*[plain_protein(x, -0.55, "protein", 0.72) for x in (-4.0, 0, 4.0)])
        title = fit_text("How does a protein choose one membrane region?", max_w=11.2,
                         size=40, color=TEXT).move_to([0, -2.65, 0])
        schematic = scope_tag("schematic")
        self.play(FadeIn(cytosol_field(top=1.18)), FadeIn(mem), FadeIn(regions), run_time=0.7)
        self.at("leaves newly made")
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in proteins], lag_ratio=0.18), run_time=1.1)
        for i, p in enumerate(proteins):
            drift(p, phase=i * 1.3)
        self.at("without grip")
        self.play(*[p.animate.shift(DOWN * 0.18) for p in proteins], run_time=0.6, rate_func=there_and_back)
        self.at("move a protein")
        self.play(proteins[1].animate.shift(RIGHT * 1.0), run_time=1.2)
        self.at("without changing")
        self.play(proteins[1].animate.shift(LEFT * 1.0), run_time=0.8)
        self.at("How does")
        self.play(FadeIn(title, shift=UP * 0.15), FadeIn(schematic), run_time=0.7)
        glow = region_glow(-4.0, 3.55, 0.08, y=1.55)
        self.at("one membrane region")
        self.play(FadeIn(glow), run_time=0.7)
        self.at("membrane itself")
        self.play(glow.animate.set_fill(GREEN, 0.28),
                  proteins[0].animate.shift(UP * 0.6), run_time=1.8)
        self.at("changing address")
        self.play(glow.animate.scale(1.08).set_opacity(0.8), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Lipids as Anchors and Addresses"
    TITLE = "How a Membrane Writes an Address"


class S02Lipids(SpokenScene):
    def construct(self):
        mem = membrane(width=11.7, y=0.7)
        heads = VGroup(*[lipid(x, "PIP2", y=0.7, scale=1.0) for x in (-3.5, -1.75, 0, 1.75, 3.5)])
        head_label = T("head groups face the cytosol", 30, GREEN).move_to([0, -0.55, 0])
        tails_label = T("tails stay buried", 30, YELLOW).move_to([0, 2.55, 0])
        self.play(FadeIn(cytosol_field(top=0.35)), FadeIn(mem), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.15) for h in heads], lag_ratio=0.1), run_time=1.0)
        self.at("head groups facing")
        self.play(FadeIn(head_label, shift=UP * 0.12), run_time=0.6)
        self.play(heads.animate.shift(RIGHT * 0.18), run_time=1.2, rate_func=there_and_back)
        enz = enzyme("enzyme", -4.6, -1.75)
        plus = boxed_label("+ phosphate", PURPLE, size=26, pad=0.16).move_to([-1.6, -1.75, 0])
        minus = boxed_label("− phosphate", PURPLE, size=26, pad=0.16).move_to([1.6, -1.75, 0])
        self.at("Enzymes can")
        self.play(FadeIn(enz, shift=RIGHT * 0.2), run_time=0.5)
        self.at("add or remove")
        self.play(enz.animate.move_to([-3.8, -1.75, 0]), FadeIn(plus), FadeIn(minus), run_time=1.0)
        badges = VGroup(*[Circle(0.11, color=GREEN, fill_color=GREEN, fill_opacity=1).next_to(heads[i].head, DOWN, buff=0.06)
                         for i in (1, 2, 3)])
        self.play(LaggedStart(*[FadeIn(b, scale=0.3) for b in badges], lag_ratio=0.18), run_time=0.8)
        self.at("tails stay buried")
        self.play(FadeOut(VGroup(enz, plus, minus)), FadeIn(tails_label),
                  *[Indicate(h.tails, color=YELLOW, scale_factor=1.05) for h in heads], run_time=0.9)
        self.at("exposed head group")
        self.play(heads[2].head.animate.set_stroke(GREEN, 5).set_fill(GREEN, 0.3), run_time=0.8)
        reader = cup_protein(0, -2.05, "reader", scale=0.72)
        self.at("proteins can recognize")
        self.play(FadeOut(head_label), FadeIn(reader, shift=UP * 0.25), reader.animate.shift(UP * 0.45), run_time=1.2)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Writer(SpokenScene):
    def construct(self):
        mem = membrane()
        xs = (-3.8, -1.9, 0, 1.9, 3.8)
        p2 = VGroup(*[lipid(x, "PIP2", scale=0.9) for x in xs])
        self.add(cytosol_field(), mem, p2, scope_tag("schematic"))
        kinase = enzyme("PI3-kinase", -4.4, 2.65, 28)
        spot = Circle(1.35, color=PURPLE, stroke_width=0, fill_color=PURPLE, fill_opacity=0.08).move_to([-4.4, 1.55, 0])
        self.at("PI3 kinase")
        self.play(FadeIn(spot), FadeIn(kinase, shift=DOWN * 0.2), run_time=0.7)
        writer = T("writer", 30, PURPLE, weight=BOLD).move_to([-4.4, 3.35, 0])
        self.at("is the rider")
        self.play(FadeIn(writer, shift=DOWN * 0.1), run_time=0.5)
        self.at("recruited and activated")
        self.play(kinase.animate.shift(DOWN * 0.25), spot.animate.set_fill(PURPLE, 0.22), run_time=0.8)
        new = []
        self.at("converts membrane")
        for i, x in enumerate(xs[:3]):
            p3 = lipid(x, "PIP3", bright=True, scale=0.9)
            new.append(p3)
            self.play(kinase.animate.set_x(x), spot.animate.set_x(x),
                      ReplacementTransform(p2[i], p3), run_time=0.75)
        local = region_glow(-1.9, 5.8, 0.16)
        self.at("Production can be local")
        self.play(FadeIn(local), run_time=0.7)
        self.at("one membrane region")
        self.play(local.animate.set_fill(GREEN, 0.3), run_time=1.1)
        self.at("before another")
        self.play(Indicate(p2[-1], color=GREY, scale_factor=1.05), run_time=0.6)
        self.finish()


class S04Dynamic(SpokenScene):
    def construct(self):
        mem = membrane()
        band = region_glow(-3.5, 2.3, 0.25).stretch_to_fit_height(1.6)
        pips = VGroup(*[lipid(x, "PIP3", bright=True, scale=0.82) for x in (-4.3, -3.2, -2.1)])
        writer = enzyme("production", -4.4, 2.75, 26)
        eraser = enzyme("removal", 4.4, 2.75, 26)
        self.add(cytosol_field(), mem, band, pips, writer, scope_tag("schematic"))
        self.at("does not stay")
        self.play(pips[2].animate.shift(RIGHT * 1.4), band.animate.stretch_to_fit_width(4.5), run_time=1.3)
        spread = T("spread →", 30, GREEN, weight=BOLD).move_to([0.2, -1.15, 0])
        self.at("diffuse sideways")
        self.play(FadeIn(spread), pips[1].animate.shift(RIGHT * 1.1), pips[2].animate.shift(RIGHT * 1.5),
                  band.animate.stretch_to_fit_width(6.4).set_x(-2.0), run_time=1.7)
        self.at("phosphatases remove")
        self.play(FadeIn(eraser, shift=LEFT * 0.2), run_time=0.6)
        p2 = lipid(0.2, "PIP2", scale=0.78)
        self.play(eraser.animate.set_x(0.2), ReplacementTransform(pips[2], p2), run_time=1.0)
        prod_lab = T("production", 28, PURPLE).move_to([-4.4, 3.5, 0])
        rem_lab = T("removal", 28, PURPLE).move_to([3.4, 3.5, 0])
        self.at("production spread and removal")
        self.play(FadeOut(spread), FadeIn(prod_lab), FadeIn(rem_lab),
                  band.animate.stretch_to_fit_width(5.0).set_x(-0.8), run_time=1.4)
        self.at("address can therefore move")
        self.play(band.animate.shift(RIGHT * 1.7), writer.animate.shift(RIGHT * 1.7), run_time=1.8)
        dynamic = T("dynamic address", 42, GREEN, weight=BOLD).move_to([0, -1.3, 0])
        fixed = T("not a fixed postal code", 30, GREY).move_to([0, -2.15, 0])
        self.at("dynamic address")
        self.play(FadeIn(dynamic, shift=UP * 0.15), run_time=0.7)
        self.at("fixed postal code")
        self.play(FadeIn(fixed), band.animate.stretch_to_fit_width(3.8), run_time=1.0)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world, rep = two_region_world()
        self.play(FadeIn(world[0]), FadeIn(world[1]), run_time=0.6)
        self.at("two membrane regions")
        self.play(FadeIn(world[2]), run_time=0.8)
        self.at("blue reporter")
        self.play(FadeIn(rep, shift=UP * 0.2), run_time=0.6)
        bob(rep, amp=0.10, speed=1.5)
        labels = VGroup(
            T("PIP3 region", 30, GREEN, weight=BOLD).move_to([-3.25, 2.55, 0]),
            T("PIP2 region", 30, GREY, weight=BOLD).move_to([3.25, 2.55, 0]),
        )
        self.at("Only one region")
        self.play(FadeIn(labels), run_time=0.7)
        qmark = T("?", 62, GOLD, weight=BOLD).next_to(rep, DOWN, buff=0.2)
        self.at("Where should")
        self.play(FadeIn(qmark, scale=0.5), run_time=0.6)
        q = question_card("Where should a matching reader accumulate?", y=-3.22, max_w=9.8)
        self.at("matching reader accumulate")
        self.play(FadeIn(q), run_time=0.7)
        self.at("Keep watching")
        self.play(rep.animate.shift(LEFT * 0.75), qmark.animate.shift(LEFT * 0.75), run_time=1.0, rate_func=there_and_back)
        self.add(scope_tag("schematic"))
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Where should a matching reader accumulate?"
    SECONDS = 4.5
    CARD = {"y": -3.22, "max_w": 9.8}

    def backdrop(self):
        g = question_world(with_question=False)
        rep = g[0][-1]
        bob(rep, amp=0.10, speed=1.5)
        g.add(T("schematic", 24, GREY).move_to([-5.7, -3.35, 0]))
        return g


class S07Reader(SpokenScene):
    def construct(self):
        world, rep = two_region_world(cup=True)
        labels = VGroup(
            T("PIP3 region", 30, GREEN, weight=BOLD).move_to([-3.25, 2.55, 0]),
            T("PIP2 region", 30, GREY, weight=BOLD).move_to([3.25, 2.55, 0]),
        )
        self.add(world, labels, scope_tag("schematic"))
        self.at("accumulates at")
        drift(rep, amp=0.07, sway=0.05)
        self.play(rep.animate.move_to([-3.25, -0.35, 0]), run_time=1.2)
        self.play(rep.animate.shift(RIGHT * 0.5), run_time=2.3, rate_func=there_and_back)
        ph = T("PH domain", 30, BLUE, weight=BOLD).move_to([0, -2.75, 0])
        self.at("pleckstrin homology domain")
        self.play(rep.animate.scale(1.08), FadeIn(ph), run_time=0.8, rate_func=there_and_back)
        self.at("shortened to")
        self.play(ph.animate.scale(1.15), run_time=0.6, rate_func=there_and_back)
        self.at("Drawn as a cup")
        self.play(rep.cup.animate.set_stroke(width=10), run_time=0.7)
        self.at("grips a compatible")
        self.play(rep.animate.shift(UP * 0.2), run_time=0.9)
        copies = VGroup(cup_protein(-5.0, -1.55, scale=0.62), cup_protein(-1.5, -1.55, scale=0.62))
        self.at("recruits the attached")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.5) for c in copies], lag_ratio=0.25), run_time=1.1)
        for i, c in enumerate(copies):
            drift(c, amp=0.1, phase=i * 1.7)
        self.play(*[c.animate.shift(UP * 0.45) for c in copies], run_time=0.8)
        self.finish()


class S08Akt(SpokenScene):
    def construct(self):
        mem = membrane()
        glow = region_glow(-3.3, 4.8, 0.07)
        pips = VGroup(*[lipid(x, "PIP3", bright=True, scale=0.82) for x in (-4.45, -3.25, -2.05)])
        akt = cup_protein(-2.7, -1.55, "Akt", scale=0.82)
        haze = RoundedRectangle(corner_radius=0.5, width=4.5, height=2.35, stroke_width=0,
                                fill_color=GREEN, fill_opacity=0.13).move_to([3.35, -1.15, 0])
        gfp = T("PH–GFP reporter", 28, GREEN, weight=BOLD).move_to([3.45, -2.65, 0])
        self.add(cytosol_field(), mem, glow, pips, akt, haze, gfp, scope_tag("schematic"))
        self.at("Akt uses")
        self.play(Indicate(akt.cup, color=BLUE, scale_factor=1.15), run_time=0.7)
        self.play(akt.animate.shift(RIGHT * 1.2), run_time=3.8, rate_func=there_and_back)
        self.at("remain in the cytosol")
        self.play(akt.animate.shift(RIGHT * 0.6), run_time=1.0, rate_func=there_and_back)
        self.at("address rises")
        self.play(glow.animate.set_fill(GREEN, 0.3), run_time=1.2)
        self.at("Akt is recruited")
        self.play(akt.animate.move_to([-3.3, -0.05, 0]), run_time=1.3)
        rim = Line([1.2, 0.83, 0], [5.55, 0.83, 0], color=GREEN, stroke_width=12).set_opacity(0.75)
        self.at("green fluorescent")
        self.play(haze.animate.set_opacity(0.55), run_time=0.7)
        self.at("movement visible")
        self.play(ReplacementTransform(haze, rim), run_time=1.2)
        self.finish()


class S09Eraser(SpokenScene):
    def construct(self):
        mem = membrane()
        band = region_glow(-2.8, 5.4, 0.28).stretch_to_fit_height(1.6)
        xs = (-4.5, -3.3, -2.1, -0.9)
        p3s = VGroup(*[lipid(x, "PIP3", bright=True, scale=0.82) for x in xs])
        akt = cup_protein(-3.2, -0.05, "Akt", scale=0.74)
        rim = Line([0.4, 0.83, 0], [4.8, 0.83, 0], color=GREEN, stroke_width=12).set_opacity(0.75)
        self.add(cytosol_field(), mem, band, p3s, akt, rim, scope_tag("schematic"))
        pten = enzyme("PTEN", -5.1, 2.65, 30)
        self.at("PTEN is")
        self.play(FadeIn(pten, shift=RIGHT * 0.2), run_time=0.6)
        eraser_lab = T("eraser", 30, PURPLE, weight=BOLD).move_to([-5.1, 3.35, 0])
        self.at("an eraser")
        self.play(FadeIn(eraser_lab), run_time=0.5)
        self.at("removes the phosphate")
        replacements = []
        for i, x in enumerate(xs):
            p2 = lipid(x, "PIP2", scale=0.82)
            replacements.append(p2)
            self.play(pten.animate.set_x(x), ReplacementTransform(p3s[i], p2),
                      band.animate.set_fill(GREEN, max(0.04, 0.24 - i * 0.05)), run_time=0.72)
        self.at("address fades")
        self.play(FadeOut(band), rim.animate.set_opacity(0.12), run_time=1.0)
        self.at("lose that contact")
        self.play(akt.animate.shift(DOWN * 0.85), run_time=1.0)
        self.at("return toward")
        self.play(akt.animate.shift(RIGHT * 1.5), FadeOut(rim), run_time=1.1)
        self.finish()


class S10Evidence(SpokenScene):
    def construct(self):
        world, reporter = two_region_world(reporter_x=-3.25, reporter_y=-0.2, cup=True)
        self.add(world, scope_tag("schematic"))
        evidence = T("evidence", 42, GOLD, weight=BOLD).move_to([0, -2.55, 0])
        self.at("reporter is evidence")
        self.play(FadeIn(evidence, shift=UP * 0.15), run_time=0.7)
        direct = T("not a direct photograph", 30, GREY).move_to([0, -3.15, 0])
        self.at("not a direct photograph")
        self.play(FadeIn(direct), run_time=0.7)
        self.play(reporter.animate.shift(RIGHT * 0.7), run_time=2.2, rate_func=there_and_back)
        self.at("binding preference")
        self.play(Indicate(reporter.cup, color=RED, scale_factor=1.15), run_time=0.7)
        self.at("competing contacts")
        self.play(reporter.animate.shift(RIGHT * 0.7), run_time=0.8, rate_func=there_and_back)
        self.at("cell shape")
        self.play(world[0].animate.stretch_to_fit_width(11.4), run_time=0.8, rate_func=there_and_back)
        self.play(FadeOut(VGroup(world, evidence, direct)), run_time=0.5)
        control1 = VGroup(cup_protein(0, 0, "reader", scale=0.62), T("binding pocket", 28, TEXT)).arrange(DOWN, buff=0.24)
        mark = T("×", 48, RED, weight=BOLD).move_to(control1[0].get_top() + RIGHT * 0.55)
        control1.add(mark).move_to([-4.2, 0.1, 0])
        control2 = VGroup(enzyme("writer", 0, 0, 28), T("blocked writer", 28, TEXT)).arrange(DOWN, buff=0.35).move_to([0, 0.1, 0])
        blocked = T("×", 46, RED, weight=BOLD).next_to(control2[0], UR, buff=0.05)
        control2.add(blocked)
        bars = VGroup(Rectangle(width=0.65, height=1.8, color=GREEN, fill_color=GREEN, fill_opacity=0.45),
                      Rectangle(width=0.65, height=1.8, color=RED, fill_color=RED, fill_opacity=0.45)).arrange(RIGHT, buff=0.3)
        control3 = VGroup(bars, T("imaging geometry", 28, TEXT)).arrange(DOWN, buff=0.3).move_to([4.2, 0.1, 0])
        heading = T("controls", 42, GOLD, weight=BOLD).move_to([0, 3.0, 0])
        self.at("Controls must test")
        self.play(FadeIn(heading), run_time=0.5)
        self.at("binding pocket")
        self.play(FadeIn(control1, shift=UP * 0.15), run_time=0.7)
        self.at("the writer")
        self.play(FadeIn(control2, shift=UP * 0.15), run_time=0.7)
        self.at("imaging geometry")
        self.play(FadeIn(control3, shift=UP * 0.15), run_time=0.7)
        self.add(T("schematic", 24, GREY).move_to([-5.7, -3.35, 0]))
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        grip_panel = RoundedRectangle(corner_radius=0.22, width=5.3, height=1.55, stroke_width=0,
                                      fill_color=YELLOW, fill_opacity=0.12).move_to([-3.1, 2.55, 0])
        address_panel = RoundedRectangle(corner_radius=0.22, width=5.3, height=1.55, stroke_width=0,
                                         fill_color=GREEN, fill_opacity=0.12).move_to([3.0, 2.55, 0])
        grip = T("GRIP", 54, YELLOW, weight=BOLD).move_to(grip_panel)
        address = T("ADDRESS", 54, GREEN, weight=BOLD).move_to(address_panel)
        divider = Line([0, 3.0, 0], [0, 2.05, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(grip_panel), FadeIn(address_panel), FadeIn(grip), FadeIn(address), Create(divider), run_time=0.8)
        self.at("address half")
        self.play(address.animate.scale(1.12), run_time=0.7, rate_func=there_and_back)
        rule = caption("Lipids supply grip, address, or both.", size=38, color=TEXT, y=-3.05)
        self.at("Lipids control")
        self.play(FadeIn(rule, shift=UP * 0.15), grip_panel.animate.shift(DOWN * 0.22),
                  address_panel.animate.shift(DOWN * 0.22), run_time=0.9, rate_func=there_and_back)
        self.at("supplying grip")
        self.play(grip.animate.scale(1.12), grip_panel.animate.set_fill(YELLOW, 0.3),
                  run_time=0.8, rate_func=there_and_back)
        self.at("address or both")
        self.play(address.animate.scale(1.10), address_panel.animate.set_fill(GREEN, 0.3),
                  run_time=0.8, rate_func=there_and_back)
        row = writer_reader_eraser_row().move_to([0, -0.1, 0])
        self.at("Writing and erasing")
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.08) for m in row], lag_ratio=0.09), run_time=1.6)
        self.at("readers gather")
        self.play(row[4].animate.shift(UP * 0.35), row[2].animate.set_fill(GREEN, 0.45), run_time=1.0)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        mem = membrane(width=11.3, y=-0.85).set_stroke(width=0)
        patch = region_glow(0, 4.0, 0.25, y=-0.85)
        writer = enzyme("writer", -4.2, 1.55, 32)
        reader = cup_protein(0, 1.35, "reader", scale=0.72)
        eraser = enzyme("eraser", 4.2, 1.55, 32)
        self.play(FadeIn(cytosol_field(width=11.5, top=-1.1)), FadeIn(mem), FadeIn(patch), run_time=0.6)
        self.at("read a lipid signal")
        self.play(FadeIn(writer), FadeIn(reader), FadeIn(eraser), run_time=0.8)
        process = T("read the process", 40, GOLD, weight=BOLD).move_to([0, 3.05, 0])
        self.at("as a process")
        self.play(FadeIn(process), run_time=0.6)
        self.at("where the writer acts")
        self.play(writer.animate.move_to([-1.65, 0.35, 0]), patch.animate.set_fill(GREEN, 0.35), run_time=1.0)
        self.at("which domain recognizes")
        self.play(reader.animate.move_to([0, -1.75, 0]), run_time=1.0)
        self.at("which eraser removes")
        self.play(eraser.animate.move_to([1.65, 0.35, 0]), patch.animate.set_fill(GREEN, 0.08), run_time=1.0)
        row = writer_reader_eraser_row().move_to([0, 0.0, 0])
        self.at("Those three answers")
        self.play(FadeOut(VGroup(mem, patch, writer, reader, eraser)), run_time=0.4)
        self.play(FadeIn(row), run_time=0.5)
        outcome = caption("predict the changing recruitment pattern", size=34, color=GREEN, y=-2.55)
        self.at("predict the changing")
        self.play(FadeIn(outcome, shift=UP * 0.15), row[4].animate.shift(UP * 0.25), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "Writers, readers, and erasers turn membrane lipids into changing addresses."
