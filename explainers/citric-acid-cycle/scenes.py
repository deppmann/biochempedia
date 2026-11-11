"""Follow the Electrons — citric-acid-cycle teaching film.

COLOR MAP
  BLUE   carbon platform / cycle road
  YELLOW incoming acetyl group
  GOLD   electrons and electron flow
  TEAL   empty and loaded electron carriers
  GREEN  direct GTP payout / open flow
  RED    oxygen target / blocked flow
  GREY   carbon dioxide and supporting structure

All chemistry is represented with labelled blocks and schematic machinery; no
molecular structures are drawn.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403


CYCLE_C = np.array([-1.65, -0.25, 0.0])
CYCLE_R = 2.45
CHAIN_X = 4.55
ROAD_W = 18


def point_on_cycle(deg, radius=CYCLE_R, center=CYCLE_C):
    a = math.radians(deg)
    return center + np.array([radius * math.cos(a), radius * math.sin(a), 0.0])


def block(text, color, size=28, width=None, fill=0.18):
    item = chip(text, color=color, size=max(28, size), pad=0.2, fill_opacity=fill)
    if width and item.width < width:
        item[0].stretch_to_fit_width(width)
    return item


def electron_pair(scale=1.0):
    return VGroup(
        Dot(radius=0.105 * scale, color=GOLD),
        Dot(radius=0.105 * scale, color=GOLD),
    ).arrange(RIGHT, buff=0.10 * scale)


def carrier(label="NAD+", loaded=False, size=26):
    c = block(label, TEAL, size=size, fill=0.32 if loaded else 0.06)
    if loaded:
        pair = electron_pair(0.65).move_to(c[0])
        pair.shift(DOWN * 0.25)
        return VGroup(c, pair)
    return c


def cycle_road():
    base = Circle(
        radius=CYCLE_R,
        color=BLUE,
        stroke_width=28,
        stroke_opacity=0.62,
        fill_color=BLUE,
        fill_opacity=0.16,
    ).move_to(CYCLE_C)
    moving = DashedVMobject(
        Circle(radius=CYCLE_R, color=BLUE, stroke_width=8).move_to(CYCLE_C),
        num_dashes=28,
        dashed_ratio=0.5,
    )
    moving.add_updater(lambda m, dt: m.rotate(-0.17 * dt, about_point=CYCLE_C))
    sweep = Arc(
        radius=CYCLE_R,
        start_angle=PI / 2,
        angle=0.72,
        arc_center=CYCLE_C,
        color=TEXT,
        stroke_width=15,
        stroke_opacity=0.72,
    )
    sweep.add_updater(lambda m, dt: m.rotate(-0.32 * dt, about_point=CYCLE_C))
    flow_band = AnnularSector(
        inner_radius=0.65,
        outer_radius=CYCLE_R - 0.22,
        angle=0.62,
        start_angle=0.35,
        arc_center=CYCLE_C,
        fill_color=BLUE,
        fill_opacity=0.22,
        stroke_width=0,
    )
    flow_band.add_updater(lambda m, dt: m.rotate(-1.35 * dt, about_point=CYCLE_C))
    return VGroup(base, moving, sweep, flow_band)


def orbiting_electrons(n=8, phase=0, radius=CYCLE_R, center=CYCLE_C, speed=22):
    driver = ValueTracker(phase)
    driver.add_updater(lambda m, dt: m.increment_value(speed * dt))
    dots = VGroup(*[Dot(radius=0.105, color=GOLD) for _ in range(n)])
    for i, dot in enumerate(dots):
        dot.add_updater(
            lambda m, i=i: m.move_to(
                point_on_cycle(driver.get_value() - i * 360 / n, radius=radius, center=center)
            )
        )
    return driver, dots


def platform_station(text="oxaloacetate · 4C"):
    # The station is tied to the bottom of the road without sitting on its stroke.
    return block(text, BLUE, 28, fill=0.28).move_to(CYCLE_C + DOWN * 3.05)


def acetyl_cart():
    return block("acetyl group · 2C", YELLOW, 28, fill=0.28).move_to([-5.15, 1.95, 0])


def cart_stop(deg):
    """A labelled cart position just outside the road, clear of its stroke."""
    return point_on_cycle(deg, radius=CYCLE_R + 1.0)


def chain_lane(label=True):
    lane = RoundedRectangle(
        corner_radius=0.2,
        width=2.2,
        height=5.45,
        stroke_color=TEAL,
        stroke_width=5,
        fill_color=TEAL,
        fill_opacity=0.14,
    ).move_to([CHAIN_X, -0.15, 0])
    flow = DashedLine(
        [CHAIN_X, 2.15, 0], [CHAIN_X, -2.25, 0],
        color=GOLD, stroke_width=8, dash_length=0.25,
    )
    flow.add_updater(lambda m, dt: m.shift(DOWN * 0.22 * dt) if m.get_y() > -0.3 else m.shift(UP * 0.22 * dt))
    parts = VGroup(lane, flow)
    if label:
        lab = T("electron\ntransport\nchain", 28, TEAL, weight=BOLD, line_spacing=0.82).move_to([CHAIN_X, 0.2, 0])
        parts.add(lab)
    return parts


def compact_world(with_chain=False, electrons=8):
    road = cycle_road()
    station = platform_station()
    driver, dots = orbiting_electrons(electrons)
    world = VGroup(road, station, dots)
    if with_chain:
        world.add(chain_lane())
    return world, driver


def gate_at(deg, label="?"):
    # Gates sit outside the roadway so their labels never collide with the road.
    p = point_on_cycle(deg, radius=CYCLE_R + 0.9)
    gate = RoundedRectangle(
        corner_radius=0.12, width=1.45, height=0.72,
        stroke_color=GOLD, stroke_width=4,
        fill_color=BG, fill_opacity=1,
    ).move_to(p)
    lab = T(label, 28, GOLD, weight=BOLD).move_to(gate)
    return VGroup(gate, lab)


def oxygen_off_icon(target):
    """A compact no-oxygen mark beside the target; it never crosses the label."""
    ring = Circle(radius=0.27, color=RED, stroke_width=5)
    slash = Line(UL * 0.18, DR * 0.18, color=RED, stroke_width=5)
    return VGroup(ring, slash).next_to(target, LEFT, buff=0.18)


def prompt_group(answer="?"):
    prompt = T("How many loading steps?", 36, TEXT, weight=BOLD)
    box = RoundedRectangle(
        corner_radius=0.18, width=1.5, height=1.15,
        stroke_color=GOLD, stroke_width=5,
        fill_color=BG, fill_opacity=0.95,
    )
    ans = T(answer, 52, GOLD, weight=BOLD).move_to(box)
    return VGroup(prompt, VGroup(box, ans)).arrange(DOWN, buff=0.28).move_to(CYCLE_C)


class S00Hook(SpokenScene, TitleCard):
    LESSON = "The citric acid cycle"
    TITLE = "Follow the Electrons"

    def construct(self):
        road = cycle_road()
        schematic = T("SCHEMATIC", 28, TEXT, weight=BOLD).to_corner(UL, buff=0.45)
        station = platform_station()
        cart = acetyl_cart()
        atp = block("ATP?", GREEN, 26, fill=0.12).move_to(point_on_cycle(105, CYCLE_R - 0.55))
        atp_path = Circle(radius=CYCLE_R - 0.55).move_to(CYCLE_C).set_stroke(opacity=0)
        self.play(Create(road[0]), FadeIn(schematic), run_time=0.8)
        self.add(road[1])
        self.play(FadeIn(atp, scale=0.7), MoveAlongPath(atp, atp_path), run_time=2.1, rate_func=linear)

        self.at("what is it actually doing")
        self.play(atp.animate.move_to([0.35, -0.25, 0]), run_time=0.55)

        self.at("Follow the electrons")
        driver, dots = orbiting_electrons(8, phase=160, speed=24)
        self.add(driver)
        self.play(FadeOut(atp), LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.06), run_time=0.8)

        self.at("acetyl group enters")
        self.play(FadeIn(cart, shift=RIGHT * 0.4), run_time=0.5)
        self.play(cart.animate.move_to(cart_stop(145)), run_time=1.0, rate_func=smooth)

        self.at("oxalocitate waits")
        self.play(FadeIn(station, scale=0.8), run_time=0.55)
        self.play(Indicate(station, color=BLUE, scale_factor=1.06), run_time=0.7)

        self.at("ready to carry")
        self.play(cart.animate.move_to(cart_stop(115)), run_time=0.8)
        self.finish()


class S01Title(Scene):
    def construct(self):
        config.background_color = BG
        road = cycle_road()
        station = platform_station()
        cart = acetyl_cart().move_to(cart_stop(115))
        driver, dots = orbiting_electrons(8, phase=125, speed=24)
        veil = Rectangle(width=13.5, height=3.1, fill_color=BG, fill_opacity=0.86, stroke_width=0)
        title = T("FOLLOW THE ELECTRONS", 54, TEXT, font=TITLE_FONT, weight=BOLD)
        rule = Line(LEFT * 2.0, RIGHT * 2.0, color=GOLD, stroke_width=5).next_to(title, DOWN, buff=0.28)
        self.add(road, station, cart, driver, dots)
        self.play(FadeIn(veil), Write(title), GrowFromCenter(rule), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(VGroup(veil, title, rule)), run_time=0.45)


class S02Budget(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        cart = acetyl_cart().move_to(cart_stop(115))
        driver, dots = orbiting_electrons(8, phase=135, speed=18)
        self.add(road, station, cart, driver, dots)

        self.at("electron budget")
        counter = VGroup(T("ELECTRON BUDGET", 28, TEXT, weight=BOLD), M("8 electrons", 42, GOLD)).arrange(DOWN, buff=0.12).move_to(CYCLE_C)
        self.play(FadeIn(counter, scale=0.8), cart.animate.scale(1.08), run_time=0.65)

        self.at("two carbons eventually")
        old1 = block("CO₂", GREY, 28).move_to([2.0, 1.0, 0])
        self.play(FadeIn(old1, shift=RIGHT * 0.4), cart.animate.move_to(cart_stop(45)), run_time=0.8)

        self.at("not during that same turn")
        old2 = block("CO₂", GREY, 28).move_to([1.95, -1.5, 0])
        self.play(FadeIn(old2, shift=RIGHT * 0.4), Indicate(cart, color=YELLOW), run_time=0.75)
        self.play(FadeOut(VGroup(old1, old2)), run_time=0.35)

        self.at("releases eight electrons")
        self.play(LaggedStart(*[Indicate(d, color=GOLD, scale_factor=1.5) for d in dots], lag_ratio=0.05), run_time=1.1)

        self.at("four pairs")
        pairs = VGroup(*[electron_pair(1.15) for _ in range(4)]).arrange(RIGHT, buff=0.42).move_to([0.0, 2.85, 0])
        self.play(ReplacementTransform(dots.copy(), pairs), FadeOut(counter), run_time=1.0)
        self.play(pairs.animate.shift(RIGHT * 0.3), run_time=0.7, rate_func=there_and_back)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        cart = acetyl_cart().move_to(cart_stop(110))
        driver, dots = orbiting_electrons(8, phase=165, speed=19)
        self.add(road, station, cart, driver, dots)

        self.at("predict the machinery")
        questions = VGroup(*[gate_at(a, "?") for a in (155, 55, -35, -135)])
        self.play(LaggedStart(*[FadeIn(q, scale=0.7) for q in questions], lag_ratio=0.12), run_time=1.0)

        self.at("Eight electrons must leave")
        self.play(LaggedStart(*[Indicate(d, color=GOLD) for d in dots], lag_ratio=0.05), run_time=0.8)

        self.at("How many carrier loading steps")
        prompt = prompt_group("?")
        self.play(FadeIn(prompt[0], shift=DOWN * 0.15), FadeIn(prompt[1], scale=0.7), run_time=0.8)
        self.finish()


class S04Think(Scene):
    def construct(self):
        config.background_color = BG
        road = cycle_road()
        station = platform_station()
        cart = acetyl_cart().move_to(cart_stop(110))
        driver, dots = orbiting_electrons(8, phase=165, speed=18)
        questions = VGroup(*[gate_at(a, "?") for a in (155, 55, -35, -135)])
        prompt = prompt_group("?")
        self.add(road, station, cart, driver, dots, questions, prompt)
        self.wait(1.85)
        self.play(prompt[1][1].animate.scale(1.18), run_time=0.35, rate_func=there_and_back)
        self.wait(2.3)


class S05Pairs(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        driver, dots = orbiting_electrons(8, phase=165, speed=17)
        gates = VGroup(*[gate_at(a, "?") for a in (155, 55, -35, -135)])
        prompt = prompt_group("?")
        self.add(road, station, driver, dots, gates, prompt)

        self.at("4")
        answer = T("4", 54, GOLD, weight=BOLD).move_to(prompt[1][1])
        labels = ["NAD+", "NAD+", "FAD", "NAD+"]
        new_gates = VGroup(*[gate_at(a, lab) for a, lab in zip((155, 55, -35, -135), labels)])
        self.play(Transform(prompt[1][1], answer), Transform(gates, new_gates), run_time=0.8)
        self.play(FadeOut(prompt), run_time=0.4)

        self.at("four dehydrogenase steps")
        self.play(LaggedStart(*[Indicate(g, color=GOLD, scale_factor=1.08) for g in gates], lag_ratio=0.18), run_time=1.2)

        self.at("each collecting one electron pair")
        pair_movers = [electron_pair().move_to(point_on_cycle(a + 17)) for a in (155, 55, -35, -135)]
        for p, g in zip(pair_movers, gates):
            self.play(FadeIn(p), p.animate.move_to(g), run_time=0.36)

        self.at("Three pairs load")
        loaded = VGroup(
            carrier("NADH", True).move_to([-4.55, 3.25, 0]),
            carrier("NADH", True).move_to([-1.65, 3.25, 0]),
            carrier("NADH", True).move_to([2.3, 3.25, 0]),
        )
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in loaded], lag_ratio=0.18),
            FadeOut(VGroup(*pair_movers)),
            run_time=1.1,
        )

        self.at("One pair reduces FAD")
        fad_gate = gates[2]
        badge = block("enzyme-bound FAD", TEAL, 28, fill=0.28).move_to([4.45, 1.2, 0])
        self.play(FadeOut(loaded), FadeIn(badge, shift=UP * 0.2), Indicate(fad_gate, color=TEAL), run_time=0.8)

        self.at("inside complex II")
        complex_label = T("Complex II", 28, TEAL, weight=BOLD).next_to(badge, UP, buff=0.22)
        self.play(FadeIn(complex_label), run_time=0.45)

        self.at("built into the chain")
        chain = block("electron transport chain", TEAL, 28, width=3.35, fill=0.12).move_to([4.45, -0.75, 0])
        pair_out = electron_pair().move_to(badge)
        arr = Arrow(badge.get_bottom(), chain.get_top(), color=GOLD, stroke_width=5, buff=0.16)
        self.play(FadeIn(chain, shift=UP * 0.2), GrowArrow(arr), pair_out.animate.move_to(chain), run_time=0.9)
        self.finish()


class S06Handoff(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        gates = VGroup(*[gate_at(a, lab) for a, lab in zip((155, 55, -35, -135), ("NAD+", "NAD+", "FAD", "NAD+"))])
        chain = chain_lane()
        self.add(road, station, gates)

        self.at("guiding idea")
        self.play(FadeIn(chain, shift=LEFT * 0.25), run_time=0.75)
        loop = VMobject(color=GOLD, stroke_width=7).set_points_smoothly([
            point_on_cycle(100, radius=1.75), [-0.1, 2.95, 0], [3.0, 2.95, 0], [5.95, 1.8, 0],
            [5.95, -2.75, 0], [2.7, -2.75, 0], [0.7, -1.55, 0], point_on_cycle(-120, radius=1.55),
        ])

        self.at("cycle loads electron carriers")
        loaded = VGroup(*[carrier("NADH", True).move_to(p) for p in ([-2.85, 0.9, 0], [-0.55, 0.8, 0], [-2.75, -1.15, 0])])
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in loaded], lag_ratio=0.15), run_time=0.9)

        self.at("transport chain empties them")
        self.remove(gates)
        self.play(Create(loop), loaded.animate.arrange(DOWN, buff=0.25).move_to([2.55, 0.15, 0]), run_time=1.1)
        empties = VGroup(*[carrier("NAD+", False).move_to([2.55, y, 0]) for y in (0.9, 0.05, -0.8)])
        self.play(ReplacementTransform(loaded, empties), run_time=0.7)

        self.at("returns for another load")
        self.play(empties.animate.arrange(DOWN, buff=0.23).move_to(CYCLE_C), run_time=1.1, path_arc=-0.6)

        self.at("Enzyme bound FAD")
        fad = block("enzyme-bound FAD", TEAL, 28, fill=0.28).move_to(CYCLE_C)
        pair = electron_pair().move_to(fad)
        self.play(FadeOut(empties), FadeIn(fad), FadeIn(pair), run_time=0.6)

        self.at("passes its electrons onward")
        self.play(pair.animate.move_to([CHAIN_X, -1.45, 0]), run_time=0.9)

        self.at("ready again")
        self.play(fad.animate.set_fill(TEAL, opacity=0.06), FadeOut(pair), run_time=0.55)
        self.finish()


class S07Tally(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        driver, dots = orbiting_electrons(8, phase=120, speed=21)
        self.add(road, station, driver, dots)
        panel = RoundedRectangle(corner_radius=0.22, width=4.5, height=3.65, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.94).move_to(CYCLE_C)
        title = T("per acetyl-CoA", 28, TEXT, weight=BOLD).move_to(panel.get_top() + DOWN * 0.38)

        self.at("After one turn")
        self.play(FadeIn(panel, scale=0.75), FadeIn(title), run_time=0.7)

        self.at("3NADH")
        nadh = block("3 NADH", TEAL, 36, fill=0.32).move_to(CYCLE_C + UP * 0.55)
        self.play(FadeIn(nadh, shift=UP * 0.2), run_time=0.6)

        self.at("1FADH2")
        fadh = block("1 FADH₂", TEAL, 34, fill=0.32).move_to(CYCLE_C + DOWN * 0.38)
        self.play(FadeIn(fadh, shift=UP * 0.2), run_time=0.6)

        self.at("1GTP")
        gtp = block("1 GTP", GREEN, 27, fill=0.28).move_to([-5.0, -2.8, 0])
        tray = RoundedRectangle(corner_radius=0.15, width=1.65, height=0.95, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.06).move_to(gtp)
        self.play(FadeIn(tray), FadeIn(gtp), run_time=0.65)

        self.at("releases two carbon dioxide")
        co2s = VGroup(block("CO₂", GREY, 27), block("CO₂", GREY, 27)).arrange(DOWN, buff=0.3).move_to([1.65, -0.25, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.4) for c in co2s], lag_ratio=0.22), run_time=0.8)

        self.at("direct payout is tiny")
        self.play(FadeOut(co2s), Indicate(gtp, color=GREEN), Indicate(nadh, color=TEAL), Indicate(fadh, color=TEAL), run_time=0.85)

        self.at("carrier's energy")
        self.play(LaggedStart(Indicate(nadh, color=GOLD), Indicate(fadh, color=GOLD), lag_ratio=0.25), run_time=0.9)

        self.at("make most a TP")
        arrow = Arrow(panel.get_right(), [5.2, -0.25, 0], color=GOLD, stroke_width=6, buff=0.15)
        most = block("most ATP", GOLD, 32, fill=0.22).next_to(arrow, RIGHT, buff=0.15)
        self.play(GrowArrow(arrow), FadeIn(most, scale=0.75), run_time=0.75)
        self.finish()


class S08Platform(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        sweep = Arc(radius=CYCLE_R, start_angle=-PI / 2, angle=0.7, arc_center=CYCLE_C, color=BLUE, stroke_width=11)
        sweep.add_updater(lambda m, dt: m.rotate(-0.33 * dt, about_point=CYCLE_C))
        acetyl = block("2C", YELLOW, 34, fill=0.3).move_to([-5.05, -2.7, 0])
        self.add(road, station, sweep)

        self.at("carbon path goes")
        self.play(FadeIn(acetyl, shift=RIGHT * 0.3), run_time=0.45)
        six = block("6C", BLUE, 42, fill=0.3).move_to(point_on_cycle(-65, radius=1.35))
        self.play(acetyl.animate.move_to(CYCLE_C + DOWN * 1.2), station.animate.scale(1.04), run_time=0.6)

        self.at("six carbons")
        self.play(ReplacementTransform(VGroup(acetyl, station), six), run_time=0.65)

        self.at("to five")
        five = block("5C", BLUE, 42, fill=0.3).move_to(point_on_cycle(15, radius=1.35))
        co1 = block("CO₂", GREY, 27).move_to([1.85, 1.65, 0])
        self.play(Transform(six, five, path_arc=0.55), FadeIn(co1, shift=RIGHT * 0.35), run_time=0.8)

        self.at("to four")
        four = block("4C", BLUE, 42, fill=0.3).move_to(point_on_cycle(105, radius=1.35))
        co2 = block("CO₂", GREY, 27).move_to([-0.1, 3.1, 0])
        self.play(Transform(six, four, path_arc=0.55), FadeIn(co2, shift=UP * 0.3), run_time=0.8)

        self.at("oxaloacetate again")
        regenerated = platform_station("oxaloacetate · regenerated")
        self.play(Transform(six, regenerated, path_arc=0.9), run_time=1.0)

        self.at("simplest form")
        hedge = T("in its simplest form", 28, TEXT).move_to(CYCLE_C + DOWN * 1.45)
        self.play(FadeIn(hedge, shift=DOWN * 0.15), FadeOut(VGroup(co1, co2)), run_time=0.65)

        self.at("does not consume it")
        self.play(Indicate(six, color=BLUE, scale_factor=1.07), run_time=0.8)
        self.finish()


class S09Oxygen(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        gates = VGroup(*[gate_at(a, lab) for a, lab in zip((155, 55, -35, -135), ("NAD+", "NAD+", "FAD", "NAD+"))])
        chain = chain_lane()
        target = block("O₂ · final acceptor", RED, 28, fill=0.24).move_to([CHAIN_X, -3.35, 0])
        self.add(road, station, gates, chain)

        self.at("none of the cycle")
        self.play(Circumscribe(gates, color=BLUE, fade_out=True), run_time=0.8)

        self.at("why does removing oxygen")
        self.play(FadeIn(target, shift=UP * 0.2), run_time=0.55)
        cross = oxygen_off_icon(target)
        self.play(Create(cross), run_time=0.45)

        self.at("chain needs oxygen")
        self.play(FadeOut(cross), Indicate(target, color=RED), run_time=0.65)
        pair = electron_pair(1.2).move_to([CHAIN_X, 2.0, 0])
        self.add(pair)
        self.play(pair.animate.move_to(target), run_time=1.1)
        self.remove(pair)

        self.at("Without oxygen")
        self.play(Create(cross), run_time=0.45)

        self.at("traffic backs up")
        queue = VGroup(*[electron_pair(1.0).move_to([CHAIN_X, y, 0]) for y in (-2.25, -1.35, -0.45, 0.45, 1.35)])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in queue], lag_ratio=0.13), run_time=0.9)

        self.at("carriers stay loaded")
        loaded = VGroup(*[carrier("NADH", True, 24).move_to([2.65, y, 0]) for y in (1.4, 0.35, -0.7)])
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in loaded], lag_ratio=0.15), run_time=0.9)
        self.play(queue.animate.arrange(DOWN, buff=0.08).move_to([CHAIN_X, -0.45, 0]), run_time=0.8)
        self.finish()


class S10Stall(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        gates = VGroup(*[gate_at(a, lab) for a, lab in zip((155, 55, -35, -135), ("NAD+", "NAD+", "FAD", "NAD+"))])
        chain = chain_lane()
        target = block("O₂ · final acceptor", RED, 28, fill=0.24).move_to([CHAIN_X, -3.35, 0])
        cross = oxygen_off_icon(target)
        self.add(road, station, gates, chain, target, cross)

        self.at("Loaded carriers cannot accept")
        blockers = VGroup(*[
            carrier("loaded", True, 28).move_to(point_on_cycle(a, radius=1.25))
            for a in (155, 55, -35, -135)
        ])
        incoming = VGroup(*[electron_pair(0.9).move_to(point_on_cycle(a + 20)) for a in (155, 55, -35, -135)])
        self.play(LaggedStart(*[FadeIn(b, scale=0.7) for b in blockers], lag_ratio=0.12), FadeIn(incoming), run_time=1.0)
        self.play(incoming.animate.scale(0.8), run_time=0.45, rate_func=there_and_back)

        self.at("four dehydrogenases stall")
        self.play(LaggedStart(*[Indicate(g, color=YELLOW, scale_factor=1.05) for g in gates], lag_ratio=0.16), run_time=1.0)

        self.at("roundabout slows")
        self.play(road[1].animate.set_opacity(0.28), incoming.animate.set_opacity(0.35), run_time=1.1)

        self.at("required indirectly")
        self.play(FadeOut(cross), target.animate.set_fill(RED, opacity=0.35), run_time=0.65)

        self.at("recycling route open")
        self.play(FadeOut(blockers), incoming.animate.move_to([CHAIN_X, -2.2, 0]), run_time=1.0)
        empties = VGroup(*[carrier("NAD+", False, 28).move_to([2.55, y, 0]) for y in (1.2, 0.2, -0.8)])
        self.play(FadeIn(empties), road[1].animate.set_opacity(1), run_time=0.7)
        self.finish()


class S11Demand(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        chain = chain_lane()
        driver, dots = orbiting_electrons(6, phase=110, speed=14)
        self.add(road, station, chain, driver, dots)

        self.at("links fuel use to demand")
        dial_center = np.array([0.75, 2.55, 0])
        dial = Arc(radius=0.85, start_angle=PI, angle=-PI, color=TEXT, stroke_width=8).move_to(dial_center)
        low = T("low", 28, TEXT).next_to(dial, LEFT, buff=0.16)
        high = T("high", 28, TEXT).next_to(dial, RIGHT, buff=0.16)
        needle = Arrow(dial_center, dial_center + UP * 0.75, buff=0, color=GOLD, stroke_width=7, tip_length=0.22)
        title = T("DEMAND", 28, GOLD, weight=BOLD).move_to([0.75, 1.55, 0])
        self.play(Create(dial), FadeIn(VGroup(low, high, title)), GrowArrow(needle), run_time=0.9)

        self.at("chain empties carriers faster")
        self.play(Rotate(needle, angle=-1.0, about_point=dial_center), run_time=0.8)
        driver.clear_updaters()
        driver.add_updater(lambda m, dt: m.increment_value(35 * dt))
        fast_pairs = VGroup(*[electron_pair().move_to([CHAIN_X, y, 0]) for y in (1.6, 0.7, -0.2)])
        self.play(LaggedStart(*[p.animate.shift(DOWN * 2.1) for p in fast_pairs], lag_ratio=0.12), run_time=0.9)

        self.at("returns")
        empties = VGroup(*[carrier("NAD+", False, 28).move_to([2.55, y, 0]) for y in (1.3, 0.3, -0.7)])
        self.play(FadeIn(empties), empties.animate.move_to(CYCLE_C), run_time=1.0, path_arc=-0.6)

        self.at("NADH accumulates")
        self.play(FadeOut(empties), Rotate(needle, angle=1.55, about_point=dial_center), run_time=0.75)
        loaded = VGroup(*[carrier("NADH", True, 28).move_to([2.55, y, 0]) for y in (1.3, 0.4, -0.5, -1.4)])
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in loaded], lag_ratio=0.12), run_time=0.85)

        self.at("slow the cycle")
        driver.clear_updaters()
        driver.add_updater(lambda m, dt: m.increment_value(5 * dt))
        self.play(road[1].animate.set_opacity(0.38), run_time=0.75)

        self.at("control points come next")
        nxt = block("next: control points", TEXT, 28, fill=0.12).move_to([1.8, -3.25, 0])
        self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.65)
        self.play(Rotate(needle, angle=-0.35, about_point=dial_center), run_time=0.65, rate_func=there_and_back)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        road = cycle_road()
        station = platform_station()
        cart = acetyl_cart().move_to(cart_stop(125))
        chain = chain_lane()
        driver, dots = orbiting_electrons(8, phase=145, speed=22)
        self.add(road, station, cart, chain, driver, dots)

        self.at("not mainly an ATP mint")
        atp = block("ATP?", GREEN, 25, fill=0.12).move_to([0.3, 0.2, 0])
        self.play(FadeIn(atp, scale=0.7), run_time=0.45)
        self.play(atp.animate.move_to([0.35, -0.9, 0]), run_time=0.55)

        self.at("electron loading roundabout")
        loads = VGroup(*[carrier("loaded", True, 28).move_to(point_on_cycle(a, radius=1.3)) for a in (145, 65, -20, -115)])
        self.play(FadeOut(atp), LaggedStart(*[FadeIn(c, scale=0.7) for c in loads], lag_ratio=0.15), run_time=0.9)

        self.at("reusable platform")
        returned = block("4C", BLUE, 30, fill=0.3).move_to([-4.8, -2.5, 0])
        return_slot = station.get_left() + LEFT * 0.65
        self.play(FadeIn(returned), returned.animate.move_to(return_slot), run_time=0.85)
        self.play(Indicate(station, color=BLUE), FadeOut(returned), run_time=0.55)

        self.at("Follow the electrons")
        loop = VMobject(color=GOLD, stroke_width=8).set_points_smoothly([
            point_on_cycle(105, radius=1.7), [-0.05, 2.95, 0], [3.0, 2.95, 0], [5.95, 1.8, 0],
            [5.95, -2.7, 0], [2.7, -2.7, 0], [0.6, -1.45, 0], point_on_cycle(-125, radius=1.5),
        ])
        self.play(Create(loop), loads.animate.arrange(DOWN, buff=0.25).move_to([2.55, 0.0, 0]), run_time=1.1)

        self.at("chain drains them")
        empties = VGroup(*[carrier("empty", False, 28).move_to([2.55, y, 0]) for y in (1.2, 0.4, -0.4, -1.2)])
        self.play(ReplacementTransform(loads, empties), run_time=0.75)

        self.at("for reuse")
        self.play(empties.animate.arrange(DOWN, buff=0.2).move_to(CYCLE_C), run_time=0.95, path_arc=-0.55)
        self.finish()


class S13End(EndCard):
    LINE = "The cycle loads carriers; the electron transport chain empties them."

    def construct(self):
        road = cycle_road()
        station = platform_station()
        chain = chain_lane(label=False)
        driver, dots = orbiting_electrons(2, phase=120, speed=24)
        shade = Rectangle(width=13.6, height=3.15, fill_color=BG, fill_opacity=0.9, stroke_width=0)
        line = T(self.LINE, 37, TEXT, font=TITLE_FONT, weight=BOLD)
        fit(line, max_w=10.9)
        hexm = hex_mascot(1.15).move_to([-5.65, -0.9, 0])
        pair = electron_pair(1.2).move_to([CHAIN_X, 1.9, 0])
        self.add(road, station, chain, driver, dots)
        self.play(FadeIn(shade), FadeIn(line, shift=UP * 0.15), FadeIn(hexm), run_time=0.65)
        self.add(pair)
        shoulder = hexm.arm.get_start()
        self.play(pair.animate.move_to([CHAIN_X, -2.0, 0]), Rotate(hexm.arm, angle=-0.55, about_point=shoulder), run_time=0.75)
        self.play(Rotate(hexm.arm, angle=0.55, about_point=shoulder), run_time=0.35)
        self.wait(1.75)
