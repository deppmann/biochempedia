"""The Two-Carbon Ledger — fatty-acid degradation explainer.

COLOR MAP (kept constant throughout)
  BLUE   fatty-acid carbon chain / water
  ORANGE coenzyme A handles
  YELLOW carnitine and moving attention cues
  PINK   reduced electron carriers (FADH2 and NADH)
  GREEN  acetyl-CoA and ATP earned
  RED    activation cost
  PURPLE workshop enzymes / processing wheel
  GREY   membranes, blood lane, supporting structure
  GOLD   the beta carbon and final 106 total

All chemistry is a labelled-block schematic.  No molecular structure is drawn.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


ORANGE = "#E8903A"
PINK = "#E26AA8"
PURPLE = "#B58CE0"


def chip(text, color=BLUE, size=28, pad=0.22, fill_opacity=0.16):
    """Readable label chip with an opaque dark field so workshop lines cannot cross its text."""
    label = T(text, size=size, color=color)
    box = RoundedRectangle(
        corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad,
        stroke_color=color, stroke_width=2.5, fill_color=BG, fill_opacity=0.94,
    )
    return VGroup(box, label.move_to(box))


def carbon_tile(n=None, size=0.54, color=BLUE, filled=False):
    box = RoundedRectangle(
        corner_radius=0.09, width=size, height=size,
        stroke_color=color, stroke_width=3,
        fill_color=color, fill_opacity=0.82 if filled else 0.18,
    )
    if n is None:
        return VGroup(box)
    lab = M(str(n), 28, BG if filled else color).move_to(box)
    return VGroup(box, lab)


def chain16(y=0.72, scale=1.0, numbered=True):
    """Canonical 16-carbon chain; every carried rebuild uses these coordinates."""
    tiles = VGroup(*[
        carbon_tile(i + 1 if numbered else None, size=0.54 * scale)
        for i in range(16)
    ])
    tiles.arrange_in_grid(rows=2, cols=8, buff=(0.12 * scale, 0.18 * scale))
    tiles.move_to([-1.25, y, 0])
    return tiles


def chain_row(count=16, y=1.35, width=10.6, numbered=True):
    s = min(0.62, (width - 0.15 * (count - 1)) / count)
    g = VGroup(*[carbon_tile(i + 1 if numbered else None, s) for i in range(count)])
    g.arrange(RIGHT, buff=0.15).move_to([0, y, 0])
    return g


def handle(text="CoA", color=ORANGE, size=28):
    return chip(text, color, size=size, pad=0.17)


def workshop_wheel(center=(0.0, -0.65, 0), radius=1.05, label=True):
    c = np.array(center, dtype=float)
    ring = Circle(radius=radius, stroke_color=PURPLE, stroke_width=6,
                  fill_color=PURPLE, fill_opacity=0.08).move_to(c)
    spokes = VGroup(*[
        Line(c + 0.25 * radius * np.array([np.cos(a), np.sin(a), 0]),
             c + 0.82 * radius * np.array([np.cos(a), np.sin(a), 0]),
             color=PURPLE, stroke_width=5)
        for a in (0, TAU / 3, 2 * TAU / 3)
    ])
    hub = Dot(c, radius=0.15, color=PURPLE)
    g = VGroup(ring, spokes, hub)
    if label:
        g.add(T("β-oxidation", 28, TEXT).move_to(c))
    return g


def add_slow_rotation(mob, speed=0.16):
    mob.add_updater(lambda m, dt: m.rotate(speed * dt))
    return mob


def matrix_motes(seed=1, count=58):
    rng = np.random.default_rng(seed)
    motes = VGroup()
    for _ in range(count):
        d = Dot(radius=float(rng.uniform(0.10, 0.15)), color=TEAL)
        d.set_opacity(float(rng.uniform(0.35, 0.60)))
        d.move_to([float(rng.uniform(-6.5, 6.5)), float(rng.uniform(-3.45, 3.45)), 0])
        d.vx = float(rng.uniform(0.75, 1.10))
        d.vy = float(rng.uniform(0.20, 0.45))

        def drift(m, dt):
            m.shift([m.vx * dt, m.vy * dt, 0])
            if m.get_x() > 6.7:
                m.shift(LEFT * 13.3)
            if m.get_y() > 3.6:
                m.shift(DOWN * 7.1)
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-8)
    return motes


def workshop_frame(seed=1, wheel_center=(0, -0.75, 0), wheel_radius=1.0):
    shell = RoundedRectangle(corner_radius=0.85, width=13.0, height=7.0,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.035)
    shell.set_z_index(-9)
    # Faint panel seams make the persistent world read as one full-frame workshop.
    grid = VGroup(
        *[DashedLine([x, -3.35, 0], [x, 3.35, 0], dash_length=0.18,
                     color=GREY, stroke_width=3.5).set_opacity(0.38) for x in (-5.2, -3.5, -1.75, 0, 1.75, 3.5, 5.2)],
        *[DashedLine([-6.25, y, 0], [6.25, y, 0], dash_length=0.18,
                     color=GREY, stroke_width=3.5).set_opacity(0.38) for y in (-2.25, -0.75, 0.75, 2.25)],
    ).set_z_index(-9)
    wheel = add_slow_rotation(workshop_wheel(wheel_center, wheel_radius, label=False))
    return VGroup(shell, grid, matrix_motes(seed), wheel), wheel


def counter_box(title, value="?", color=TEXT, width=2.7, height=1.25):
    box = RoundedRectangle(corner_radius=0.2, width=width, height=height,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.08)
    head = T(title, 28, color).move_to(box.get_top() + DOWN * 0.28)
    val = M(str(value), 40, color, weight=BOLD).move_to(box.get_bottom() + UP * 0.38)
    return VGroup(box, head, val)


def atp_gauge(value="?", center=(4.9, 0.75, 0), color=GREEN, width=2.35, height=4.7):
    c = np.array(center, dtype=float)
    body = RoundedRectangle(corner_radius=0.25, width=width, height=height,
                            stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.045).move_to(c)
    inner = Rectangle(width=width - 0.38, height=0.08, stroke_width=0,
                      fill_color=color, fill_opacity=0.75).move_to(body.get_bottom() + UP * 0.27)
    title = T("ATP total", 28, color).next_to(body, UP, buff=0.15)
    read = M(str(value), 40, color, weight=BOLD).move_to(c)
    return VGroup(body, inner, title, read)


def prediction_layout(with_timer=False):
    chain = chain_row(16, y=1.45, width=11.2)
    title = T("PALMITATE LEDGER", 34, TEAL, weight=BOLD).move_to([0, 3.1, 0])
    c1 = counter_box("turns", "?", PURPLE, 3.7, 1.55).move_to([-2.35, -1.15, 0])
    c2 = counter_box("acetyl-CoA", "?", GREEN, 3.7, 1.55).move_to([2.35, -1.15, 0])
    q = T("How many two-carbon units — after how many turns?", 30, TEXT)
    fit(q, 11.8).move_to([0, -2.55, 0])
    bracket = Brace(VGroup(chain[0], chain[1]), DOWN, color=YELLOW, buff=0.08)
    group = VGroup(title, chain, c1, c2, q, bracket)
    timer = None
    if with_timer:
        timer = Arc(radius=0.34, start_angle=PI / 2, angle=TAU - 0.15,
                    color=TEAL, stroke_width=5).move_to([5.75, -2.55, 0])
        group.add(timer)
    return group, chain, c1, c2, q, bracket, timer


def sweep_bracket(scene, bracket, chain, run_time=2.2):
    target = Brace(VGroup(chain[-2], chain[-1]), DOWN, color=YELLOW, buff=0.08)
    scene.play(Transform(bracket, target), run_time=run_time, rate_func=linear)


def acetyl_cart(label=True, scale=1.0):
    blocks = VGroup(carbon_tile(None, 0.42, GREEN, True), carbon_tile(None, 0.42, GREEN, True)).arrange(RIGHT, buff=0.05)
    coa = (handle("CoA", ORANGE, 36).scale(0.78) if label else
           RoundedRectangle(corner_radius=0.07, width=0.42, height=0.42,
                            stroke_color=ORANGE, stroke_width=3,
                            fill_color=ORANGE, fill_opacity=0.45))
    cart = VGroup(blocks, coa).arrange(RIGHT, buff=0.08).scale(scale)
    if label:
        lab = T("acetyl-CoA", 28, GREEN).next_to(cart, DOWN, buff=0.14)
        cart.add(lab)
    return cart


# -------------------------------------------------------------------------------------------------
class S00Hook(SpokenScene, TitleCard):
    LESSON = "Fatty acid degradation"
    TITLE = "The Two-Carbon Ledger"

    def construct(self):
        bg, wheel = workshop_frame(0, wheel_center=(0.25, -0.35, 0), wheel_radius=1.15)
        chain = chain16(y=1.0, scale=1.0)
        droplet = Circle(radius=1.05, color=BLUE, stroke_width=4,
                         fill_color=BLUE, fill_opacity=0.17).move_to([-5.25, 0.9, 0])
        droplet.add(T("fat", 30, BLUE).move_to(droplet))
        gauge = atp_gauge("?", center=(5.15, 0.15, 0), height=4.4)
        counters = VGroup(
            counter_box("turns", "?", PURPLE, 1.65, 1.0),
            counter_box("pairs", "?", PINK, 1.65, 1.0),
            counter_box("acetyl", "?", GREEN, 1.65, 1.0),
        ).arrange(RIGHT, buff=0.18).move_to([1.25, -2.75, 0])
        question = T("How can one fatty acid become roughly 106 ATP?", 38, TEXT)
        fit(question, 11.7).move_to([0, 3.12, 0])
        self.add(bg)
        self.play(FadeIn(droplet), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.08) for t in chain], lag_ratio=0.04),
                  run_time=1.6)
        self.at("become roughly")
        self.play(FadeIn(question, shift=DOWN * 0.12), FadeIn(gauge), run_time=0.8)
        self.play(Indicate(gauge[3], color=YELLOW, scale_factor=1.18), run_time=0.7)
        self.at("Watch")
        title = T(self.TITLE, 42, font=TITLE_FONT, color=GOLD).move_to(question)
        self.play(ReplacementTransform(question, title), chain.animate.shift(RIGHT * 0.8), run_time=1.0)
        self.at("chain enter")
        self.play(chain.animate.shift(RIGHT * 0.75 + DOWN * 0.1), Rotate(wheel, -PI / 2), run_time=1.2)
        self.at("then count")
        self.play(FadeIn(counters, shift=UP * 0.15),
                  LaggedStart(*[Indicate(c[0], color=c[0].get_color(), scale_factor=1.07) for c in counters], lag_ratio=0.25),
                  run_time=1.0)
        self.finish()


class S01Scope(SpokenScene):
    def construct(self):
        bg, wheel = workshop_frame(1, wheel_center=(1.15, -0.85, 0), wheel_radius=1.15)
        chain = chain16(y=1.0)
        gauge = atp_gauge("?", center=(5.15, 0.15, 0), height=4.4)
        schematic = T("schematic", 28, GREY).move_to([-5.35, -3.15, 0])
        self.add(bg, chain, gauge, schematic)
        self.at("simplest form")
        brace = Brace(chain, UP, color=BLUE, buff=0.15)
        scope = T("saturated · even chain", 32, BLUE).next_to(brace, UP, buff=0.13)
        self.play(GrowFromCenter(brace), FadeIn(scope, shift=DOWN * 0.1), run_time=0.9)
        self.at("Fat stores")
        dots = VGroup(*[Dot(chain[i].get_center(), radius=0.07, color=YELLOW) for i in range(0, 16, 2)])
        self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.1), run_time=0.8)
        self.at("electrons")
        self.play(LaggedStart(*[d.animate.move_to(wheel.get_center()) for d in dots], lag_ratio=0.08), run_time=1.8)
        self.play(FadeOut(dots), Indicate(gauge[0], color=GREEN, scale_factor=1.03), run_time=0.6)
        self.at("removing two carbons")
        pair_brace = Brace(VGroup(chain[0], chain[1]), DOWN, color=YELLOW, buff=0.12)
        pair_lab = T("two carbons", 28, YELLOW).next_to(pair_brace, DOWN, buff=0.1)
        self.play(GrowFromCenter(pair_brace), FadeIn(pair_lab), Rotate(wheel, -PI / 2), run_time=0.9)
        self.play(Indicate(VGroup(chain[0], chain[1]), color=YELLOW, scale_factor=1.06), run_time=0.7)
        self.at("First however")
        self.play(FadeOut(brace), FadeOut(scope), FadeOut(pair_brace), FadeOut(pair_lab), FadeOut(gauge),
                  chain.animate.shift(LEFT * 2.0), wheel.animate.shift(RIGHT * 1.2), run_time=1.3)
        self.at("reach the machinery")
        arrow = Arrow(chain.get_right() + RIGHT * 0.2, wheel.get_left() + LEFT * 0.15,
                      color=YELLOW, stroke_width=6, buff=0.05)
        self.play(GrowArrow(arrow), chain.animate.shift(RIGHT * 0.45), run_time=1.0)
        self.finish()


class S02Access(SpokenScene):
    def construct(self):
        bg, _ = workshop_frame(2, wheel_center=(5.25, -2.3, 0), wheel_radius=0.65)
        droplet = Circle(radius=1.15, color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to([-5.15, 1.35, 0])
        droplet.add(T("fat droplet", 28, BLUE).move_to(droplet))
        blood = VGroup(Line([-6.25, 0.0, 0], [0.15, 0.0, 0], color=RED, stroke_width=4),
                       Line([-6.25, -1.1, 0], [0.15, -1.1, 0], color=RED, stroke_width=4),
                       T("blood", 28, RED).move_to([-3.0, -1.48, 0]))
        chain = VGroup(*[carbon_tile(None, 0.4) for _ in range(8)]).arrange(RIGHT, buff=0.07).move_to([-4.1, 1.3, 0])
        self.add(bg, droplet, blood, T("schematic", 28, GREY).move_to([-5.25, -3.25, 0]))
        self.at("fat droplets release")
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in chain], lag_ratio=0.08),
                  droplet.animate.scale(1.04), run_time=1.2)
        self.play(chain.animate.move_to([-3.65, -0.55, 0]), droplet.animate.scale(1 / 1.04), run_time=1.2)
        self.at("Albumin")
        cart_box = RoundedRectangle(corner_radius=0.25, width=4.1, height=1.0,
                                    color=YELLOW, fill_color=YELLOW, fill_opacity=0.12, stroke_width=4).move_to(chain)
        albumin = T("albumin", 30, YELLOW).next_to(cart_box, UP, buff=0.15)
        wheels = VGroup(Dot(cart_box.get_corner(DL) + [0.55, -0.12, 0], 0.14, color=YELLOW),
                        Dot(cart_box.get_corner(DR) + [-0.55, -0.12, 0], 0.14, color=YELLOW))
        cart = VGroup(cart_box, albumin, wheels)
        self.play(FadeIn(cart, shift=UP * 0.1), run_time=0.7)
        self.at("energy using tissues")
        self.play(VGroup(cart, chain).animate.shift(RIGHT * 3.0), run_time=1.5)
        self.at("Activation")
        coa = handle("CoA", ORANGE, 28).next_to(chain, RIGHT, buff=0.08)
        toll = chip("ATP", RED, size=28).move_to([0.1, 1.25, 0])
        slot = RoundedRectangle(corner_radius=0.12, width=2.4, height=1.15, color=RED,
                                fill_color=RED, fill_opacity=0.08).move_to([1.2, 1.25, 0])
        self.play(FadeOut(cart), FadeIn(coa, shift=LEFT * 0.15), FadeIn(slot), FadeIn(toll), run_time=0.9)
        self.at("spends two")
        products = VGroup(chip("AMP", RED, 28), chip("P", RED, 28), chip("P", RED, 28)).arrange(RIGHT, buff=0.1).move_to(slot)
        cost = T("−2 ATP equivalents", 30, RED).next_to(slot, UP, buff=0.15)
        self.play(ReplacementTransform(toll, products), FadeIn(cost), run_time=1.0)
        self.at("Long chain cargo")
        outer = Rectangle(width=0.28, height=5.4, color=GREY, fill_color=GREY, fill_opacity=0.35).move_to([2.7, -0.2, 0])
        inner = Rectangle(width=0.28, height=5.4, color=GREY, fill_color=GREY, fill_opacity=0.35).move_to([4.25, -0.2, 0])
        labs = VGroup(T("outer", 28, GREY).next_to(outer, UP, buff=0.14), T("inner", 28, GREY).next_to(inner, UP, buff=0.14))
        self.play(FadeOut(blood), FadeOut(droplet), FadeOut(products), FadeOut(slot), FadeOut(cost),
                  FadeIn(outer), FadeIn(inner), FadeIn(labs),
                  VGroup(chain, coa).animate.move_to([1.65, -0.25, 0]), run_time=1.0)
        self.at("through the carnitine")
        carn = handle("carnitine", YELLOW, 28).move_to(coa)
        coa_out = coa.copy().move_to([1.55, -1.6, 0])
        self.play(ReplacementTransform(coa, carn), FadeIn(coa_out), run_time=0.65)
        cargo = VGroup(chain, carn)
        self.play(cargo.animate.move_to([3.45, -0.25, 0]), run_time=1.0)
        matrix_coa = handle("CoA", ORANGE, 28).move_to([5.55, -0.25, 0])
        self.play(FadeIn(matrix_coa), run_time=0.35)
        self.play(carn.animate.move_to([3.5, -1.55, 0]), matrix_coa.animate.next_to(chain, RIGHT, buff=0.08), run_time=0.55)
        self.play(carn.animate.move_to([2.0, -1.55, 0]), chain.animate.shift(RIGHT * 1.15), matrix_coa.animate.shift(RIGHT * 1.15), run_time=0.9)
        self.finish()


class S03Handle(SpokenScene):
    def construct(self):
        bg, wheel = workshop_frame(3, wheel_center=(2.85, 2.25, 0), wheel_radius=0.65)
        chain = chain_row(10, y=0.15, width=9.5)
        chain.shift(RIGHT * 0.7)
        coa = handle("CoA", ORANGE, 30).next_to(chain, LEFT, buff=0.1)
        conveyor = Line([-5.8, -0.65, 0], [5.8, -0.65, 0], color=GREY, stroke_width=7)
        schematic = T("schematic blocks", 28, GREY).move_to([-4.75, -3.2, 0])
        self.add(bg, conveyor, chain, coa, schematic)
        self.at("count from")
        cursor = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=1).scale(0.16).next_to(chain[0], DOWN, buff=0.05)
        self.play(FadeIn(cursor), run_time=0.35)
        self.play(cursor.animate.next_to(chain[1], DOWN, buff=0.05), run_time=0.45)
        self.play(cursor.animate.next_to(chain[2], DOWN, buff=0.05), run_time=0.45)
        self.at("Carbon 2")
        alpha = chip("α", TEXT, 32).next_to(chain[1], UP, buff=0.15)
        self.play(FadeIn(alpha, shift=DOWN * 0.1), cursor.animate.next_to(chain[1], DOWN, buff=0.05), run_time=0.65)
        self.at("carbon 3")
        beta = chip("β", GOLD, 32).next_to(chain[2], UP, buff=0.15)
        self.play(FadeIn(beta, shift=DOWN * 0.1), cursor.animate.next_to(chain[2], DOWN, buff=0.05), run_time=0.65)
        self.at("plain chain")
        jaws = VGroup(
            Line([0, 0, 0], [0.7, 0.45, 0], color=PURPLE, stroke_width=10),
            Line([0, 0, 0], [0.7, -0.45, 0], color=PURPLE, stroke_width=10),
        ).move_to(chain[2].get_center() + UP * 1.65)
        self.play(FadeOut(alpha), FadeOut(cursor), FadeIn(jaws, shift=DOWN * 0.2), run_time=0.6)
        self.at("no cutting handle")
        self.play(jaws.animate.shift(DOWN * 0.85), run_time=0.55)
        self.play(jaws.animate.shift(UP * 0.35 + RIGHT * 0.35).rotate(0.22), rate_func=there_and_back, run_time=0.65)
        self.at("Three moves")
        stations = VGroup(*[
            Circle(radius=0.55, color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.1)
            for _ in range(3)
        ])
        for i, s in enumerate(stations):
            a = PI / 2 + i * TAU / 3
            s.move_to(chain[2].get_center() + 1.65 * np.array([np.cos(a), np.sin(a), 0]))
            s.add(M(str(i + 1), 32, PURPLE).move_to(s))
        self.play(FadeOut(jaws), LaggedStart(*[FadeIn(s, scale=0.7) for s in stations], lag_ratio=0.2), run_time=1.0)
        self.at("rebuild the beta")
        self.play(Rotate(stations, -TAU / 3, about_point=chain[2].get_center()), beta.animate.set_color(YELLOW), run_time=1.2)
        self.at("bond beside it")
        mark = DashedLine(chain[1].get_right() + UP * 0.5, chain[1].get_right() + DOWN * 0.5, color=GOLD, stroke_width=5)
        self.play(Create(mark), Rotate(wheel, -PI / 2), run_time=0.8)
        self.finish()


class S04Prepare(SpokenScene):
    def construct(self):
        bg, wheel = workshop_frame(4, wheel_center=(0, 0.05, 0), wheel_radius=2.15)
        chain = chain_row(8, y=0.05, width=8.0)
        coa = handle("CoA", ORANGE, 28).next_to(chain, LEFT, buff=0.12)
        beta = chip("β", GOLD, 28).next_to(chain[2], UP, buff=0.12)
        station_labs = VGroup(
            chip("1", PURPLE, 32).move_to([-2.25, 2.65, 0]),
            chip("2", PURPLE, 32).move_to([2.25, 2.65, 0]),
            chip("3", PURPLE, 32).move_to([0, -2.65, 0]),
        )
        self.add(bg, chain, coa, beta, station_labs, T("schematic", 28, GREY).move_to([-5.25, -3.25, 0]))
        self.at("First oxidation")
        db = chip("double bond", YELLOW, 28).move_to(station_labs[0])
        self.play(ReplacementTransform(station_labs[0], db), Rotate(wheel, -TAU / 3), run_time=0.9)
        self.at("reduces FAD")
        fad = chip("FAD", PINK, 28).move_to([4.7, 2.25, 0])
        fadh = chip("FADH₂", PINK, 28).move_to([4.7, 2.25, 0])
        self.play(FadeIn(fad), run_time=0.35)
        self.play(ReplacementTransform(fad, fadh), fadh.animate.shift(DOWN * 0.55), run_time=0.7)
        self.at("Hydration")
        drop = VGroup(Circle(radius=0.18, color=BLUE, fill_color=BLUE, fill_opacity=0.75),
                      Triangle(color=BLUE, fill_color=BLUE, fill_opacity=0.75, stroke_width=0).scale(0.18).rotate(PI).shift(UP * 0.22))
        water = VGroup(drop, T("water", 28, BLUE)).arrange(DOWN, buff=0.12).move_to(station_labs[1])
        self.play(FadeOut(fadh), ReplacementTransform(station_labs[1], water), Rotate(wheel, -TAU / 3), run_time=0.8)
        self.at("placing an OH")
        oh = chip("OH", BLUE, 28).next_to(chain[2], DOWN, buff=0.15)
        self.play(water[0].animate.move_to(chain[2]), FadeOut(water[1]), FadeIn(oh), FadeOut(db), run_time=0.8)
        self.at("Second oxidation")
        ketone = chip("ketone handle", GOLD, 28).move_to(station_labs[2])
        self.play(ReplacementTransform(VGroup(oh, station_labs[2]), ketone), FadeOut(water[0]), Rotate(wheel, -TAU / 3), run_time=0.9)
        self.at("reduces NAD")
        nad = chip("NAD⁺", PINK, 28).move_to([4.7, 0.45, 0])
        nadh = chip("NADH", PINK, 28).move_to([4.7, 0.45, 0])
        self.play(FadeIn(nad), run_time=0.35)
        self.play(ReplacementTransform(nad, nadh), nadh.animate.shift(DOWN * 0.55), run_time=0.65)
        self.at("thiolase can cut")
        jaws = VGroup(Line([0, 0, 0], [0.75, 0.5, 0], color=PURPLE, stroke_width=11),
                       Line([0, 0, 0], [0.75, -0.5, 0], color=PURPLE, stroke_width=11)).move_to(chain[1].get_right() + UP * 0.95)
        self.play(FadeOut(nadh), FadeIn(jaws), ketone.animate.move_to(chain[2].get_center() + DOWN * 0.85), run_time=0.7)
        self.play(jaws.animate.shift(DOWN * 0.55).scale(0.82), run_time=0.65)
        self.finish()


class S05Rule(SpokenScene):
    def construct(self):
        bg, wheel = workshop_frame(5, wheel_center=(0.6, 0.0, 0), wheel_radius=1.75)
        chain = chain_row(16, y=0.1, width=10.2)
        old_coa = handle("CoA", ORANGE, 28).next_to(chain, LEFT, buff=0.08)
        fresh = handle("fresh CoA", ORANGE, 28).move_to([0.7, 2.7, 0])
        cut = DashedLine(chain[1].get_right() + UP * 0.55, chain[1].get_right() + DOWN * 0.55, color=GOLD, stroke_width=5)
        self.add(bg, chain, old_coa, cut)
        self.at("fresh coenzyme")
        arm = Arrow([3.0, 2.7, 0], fresh.get_right(), color=PURPLE, stroke_width=6, buff=0.1)
        self.play(FadeIn(fresh, shift=LEFT * 0.15), GrowArrow(arm), run_time=0.8)
        self.at("releases one")
        cart = acetyl_cart(True, 1.0).move_to([-3.8, -1.55, 0])
        shortened = VGroup(*[chain[i] for i in range(2, 16)])
        self.play(ReplacementTransform(VGroup(chain[0], chain[1], old_coa), cart),
                  fresh.animate.next_to(shortened, LEFT, buff=0.08), FadeOut(cut), FadeOut(arm), run_time=1.2)
        self.at("remaining chain")
        fourteen = T("14 carbons remain", 30, BLUE).move_to([-4.55, 2.45, 0])
        self.play(FadeIn(fourteen), cart.animate.shift(RIGHT * 7.6), run_time=1.25)
        self.at("returns to the first")
        loop = CurvedArrow(shortened.get_right() + UP * 0.15, shortened.get_left() + UP * 0.15,
                           angle=PI / 2, color=YELLOW, stroke_width=5)
        turn = counter_box("turns", "1", PURPLE, 2.2, 1.2).move_to([-4.8, 2.6, 0])
        self.play(FadeOut(fourteen), Create(loop), Rotate(wheel, -TAU), FadeIn(turn), run_time=1.2)
        self.at("converts chain length")
        self.play(FadeOut(loop), FadeOut(shortened), FadeOut(fresh), FadeOut(cart), run_time=0.6)
        columns = VGroup(
            counter_box("turns", "1", PURPLE, 2.6, 2.5),
            counter_box("carrier pairs", "1", PINK, 3.2, 2.5),
            counter_box("acetyl-CoA", "1", GREEN, 3.2, 2.5),
        ).arrange(RIGHT, buff=0.35).move_to([0.6, -0.1, 0])
        self.play(ReplacementTransform(turn, columns[0]), FadeOut(wheel), run_time=0.75)
        self.at("carrier pairs")
        self.play(FadeIn(columns[1], shift=UP * 0.15), run_time=0.65)
        self.at("and acetyl coenzyme")
        self.play(FadeIn(columns[2], shift=UP * 0.15), run_time=0.65)
        self.play(LaggedStart(*[Indicate(c, color=c[0].get_color(), scale_factor=1.03) for c in columns], lag_ratio=0.2), run_time=1.0)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        bg, _ = workshop_frame(6, wheel_center=(0, 0.25, 0), wheel_radius=0.45)
        layout, chain, c1, c2, question, bracket, _ = prediction_layout()
        toll = T("activation toll  −2", 28, RED).move_to([4.85, 3.1, 0])
        self.add(bg)
        self.at("Predict")
        self.play(FadeIn(layout[0]), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in chain], lag_ratio=0.035), run_time=1.0)
        self.at("16 carbon chain")
        self.play(FadeIn(bracket), sweep_bracket_animation(bracket, chain), run_time=2.0, rate_func=linear)
        self.at("after how many turns")
        self.play(FadeIn(c1, shift=UP * 0.12), FadeIn(c2, shift=UP * 0.12), run_time=0.75)
        self.at("Place your answer")
        self.play(FadeIn(question), FadeIn(toll), run_time=0.65)
        bracket.become(Brace(VGroup(chain[0], chain[1]), DOWN, color=YELLOW, buff=0.08))
        sweep_bracket(self, bracket, chain, 1.5)
        self.finish()


def sweep_bracket_animation(bracket, chain):
    target = Brace(VGroup(chain[-2], chain[-1]), DOWN, color=YELLOW, buff=0.08)
    return Transform(bracket, target)


class S07Think(Scene):
    def construct(self):
        config.background_color = BG
        bg, _ = workshop_frame(7, wheel_center=(0, 0.25, 0), wheel_radius=0.45)
        layout, chain, _, _, _, bracket, timer = prediction_layout(with_timer=True)
        toll = T("activation toll  −2", 28, RED).move_to([4.85, 3.1, 0])
        self.add(bg, layout, toll)
        self.play(Rotate(timer, -TAU), sweep_bracket_animation(bracket, chain), run_time=2.2, rate_func=linear)
        bracket.become(Brace(VGroup(chain[0], chain[1]), DOWN, color=YELLOW, buff=0.08))
        self.play(Rotate(timer, -TAU), sweep_bracket_animation(bracket, chain), run_time=2.3, rate_func=linear)


class S08Reveal(SpokenScene):
    def construct(self):
        bg, wheel = workshop_frame(8, wheel_center=(0, 0.25, 0), wheel_radius=0.45)
        layout, chain, c1, c2, question, bracket, _ = prediction_layout()
        self.add(bg, layout)
        self.at("Eight acetyl")
        groups = VGroup(*[
            SurroundingRectangle(VGroup(chain[2 * i], chain[2 * i + 1]), color=GREEN,
                                 buff=0.055, corner_radius=0.08, stroke_width=4)
            for i in range(8)
        ])
        self.play(FadeOut(bracket), LaggedStart(*[Create(g) for g in groups], lag_ratio=0.08),
                  Transform(c2[2], M("8", 40, GREEN, weight=BOLD).move_to(c2[2])), run_time=1.2)
        self.at("only seven")
        cuts = VGroup(*[
            Line(chain[2 * i + 1].get_right() + UP * 0.42, chain[2 * i + 1].get_right() + DOWN * 0.42,
                 color=YELLOW, stroke_width=4)
            for i in range(7)
        ])
        self.play(LaggedStart(*[Create(x) for x in cuts], lag_ratio=0.1),
                  Transform(c1[2], M("7", 40, PURPLE, weight=BOLD).move_to(c1[2])), run_time=1.2)
        self.at("Seven cuts")
        equation = M("7 cuts  →  8 pieces", 34, TEXT).move_to(question)
        self.play(ReplacementTransform(question, equation), LaggedStart(*[Indicate(g, color=GREEN, scale_factor=1.06) for g in groups], lag_ratio=0.08), run_time=1.2)
        self.at("last turn")
        final4 = VGroup(chain[-4], chain[-3], chain[-2], chain[-1])
        self.play(FadeOut(groups), FadeOut(cuts), FadeOut(equation), final4.animate.scale(1.35).move_to([0, 0.0, 0]),
                  FadeOut(VGroup(*chain[:-4])), run_time=0.9)
        two_carts = VGroup(acetyl_cart(False, 0.9), acetyl_cart(False, 0.9)).arrange(RIGHT, buff=0.65).move_to([0, 1.35, 0])
        self.play(Rotate(wheel, -TAU), ReplacementTransform(final4, two_carts), run_time=1.0)
        self.at("Therefore")
        self.play(FadeOut(two_carts), c1.animate.shift(LEFT * 1.35), c2.animate.shift(LEFT * 1.35), run_time=0.55)
        fcol = counter_box("FADH₂", "7", PINK, 2.4, 1.55).move_to([4.15, 0.55, 0])
        ncol = counter_box("NADH", "7", PINK, 2.4, 1.55).move_to([4.15, -1.45, 0])
        tokens_f = VGroup(*[Dot(wheel.get_center(), radius=0.09, color=PINK) for _ in range(7)])
        self.play(FadeIn(fcol), FadeIn(tokens_f), run_time=0.45)
        self.at("seven NADH")
        tokens_n = VGroup(*[Dot(wheel.get_center(), radius=0.09, color=PINK) for _ in range(7)])
        self.play(LaggedStart(*[d.animate.move_to(fcol.get_left() + LEFT * 0.15) for d in tokens_f], lag_ratio=0.08),
                  FadeIn(ncol), FadeIn(tokens_n), run_time=0.8)
        self.play(LaggedStart(*[d.animate.move_to(ncol.get_left() + LEFT * 0.15) for d in tokens_n], lag_ratio=0.08), run_time=0.7)
        self.finish()


class S09Total(SpokenScene):
    def construct(self):
        bg, _ = workshop_frame(9, wheel_center=(-4.7, -2.65, 0), wheel_radius=0.5)
        gauge = atp_gauge("0", center=(4.85, 0.15, 0), height=5.25)
        toll = chip("−2", RED, 30).move_to([4.85, -2.95, 0])
        pair_tokens = VGroup(*[VGroup(Dot(radius=0.11, color=PINK), Dot(radius=0.11, color=PINK)).arrange(RIGHT, buff=0.08) for _ in range(7)])
        pair_tokens.arrange_in_grid(rows=2, cols=4, buff=(0.35, 0.3)).move_to([-4.8, 1.75, 0])
        turbine = VGroup(Circle(radius=0.72, color=PINK, stroke_width=5),
                         VGroup(*[Line(ORIGIN, RIGHT * 0.55, color=PINK, stroke_width=5).rotate(i * TAU / 4) for i in range(4)]))
        turbine.move_to([-1.35, 1.65, 0])
        t_lab = T("oxidative\nphosphorylation", 28, PINK, line_spacing=0.75).next_to(turbine, DOWN, buff=0.15)
        self.add(bg, gauge, toll, pair_tokens)
        self.at("Each carrier pair")
        self.play(FadeIn(turbine), FadeIn(t_lab), run_time=0.65)
        self.at("about 4 ATP")
        four = M("× 4 ATP", 32, PINK).next_to(pair_tokens, DOWN, buff=0.2)
        self.play(FadeIn(four), Rotate(turbine[1], -TAU), run_time=0.9)
        self.at("Each acetyl")
        carts = VGroup(*[acetyl_cart(False, 0.58) for _ in range(8)]).arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.28)).move_to([-4.75, -1.25, 0])
        cycle = VGroup(Circle(radius=0.82, color=GREEN, stroke_width=5),
                       Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1, stroke_width=0).scale(0.12).rotate(-PI / 2).move_to([0.82, 0, 0]))
        cycle.move_to([-1.2, -1.25, 0])
        c_lab = T("citric acid cycle +\noxidative phosphorylation", 28, GREEN, line_spacing=0.75).next_to(cycle, DOWN, buff=0.14)
        self.play(FadeIn(carts), FadeIn(cycle), FadeIn(c_lab), run_time=0.75)
        self.at("about 10")
        ten = M("× 10 ATP", 32, GREEN).next_to(carts, DOWN, buff=0.15)
        self.play(FadeIn(ten), Rotate(cycle, -TAU), run_time=1.0)
        self.at("Seven pairs give")
        fill28 = Rectangle(width=gauge[1].width, height=1.2, stroke_width=0, fill_color=PINK, fill_opacity=0.72)
        fill28.move_to(gauge[0].get_bottom() + UP * (0.27 + 0.6))
        read28 = M("28", 42, PINK, weight=BOLD).move_to(gauge[3])
        self.play(LaggedStart(*[p.animate.move_to(turbine.get_center()) for p in pair_tokens], lag_ratio=0.06),
                  Rotate(turbine[1], -TAU), run_time=1.0)
        self.play(Transform(gauge[1], fill28), Transform(gauge[3], read28), FadeOut(pair_tokens), run_time=0.55)
        self.at("eight acetyl")
        fill108 = Rectangle(width=gauge[1].width, height=4.25, stroke_width=0, fill_color=GREEN, fill_opacity=0.72)
        fill108.move_to(gauge[0].get_bottom() + UP * (0.27 + 2.125))
        read108 = M("108", 42, GREEN, weight=BOLD).move_to(gauge[3])
        self.play(LaggedStart(*[c.animate.move_to(cycle.get_center()) for c in carts], lag_ratio=0.05), Rotate(cycle, -TAU), run_time=1.0)
        self.play(Transform(gauge[1], fill108), Transform(gauge[3], read108), FadeOut(carts), run_time=0.55)
        self.at("Subtract")
        self.play(toll.animate.move_to(gauge[3].get_center() + DOWN * 0.8), run_time=0.65)
        self.at("roughly 106")
        final_read = VGroup(M("≈ 106", 45, GOLD, weight=BOLD), T("ATP", 30, GOLD)).arrange(DOWN, buff=0.08).move_to(gauge[3])
        final_fill = fill108.copy().set_color(GOLD).stretch_to_fit_height(4.12).align_to(gauge[0].get_bottom() + UP * 0.27, DOWN)
        self.play(Transform(gauge[1], final_fill), ReplacementTransform(VGroup(gauge[3], toll), final_read),
                  Indicate(gauge[0], color=GOLD, scale_factor=1.02), run_time=1.0)
        self.finish()


class S10ScopeReturn(SpokenScene):
    def construct(self):
        bg, wheel = workshop_frame(10, wheel_center=(-3.8, -0.35, 0), wheel_radius=1.15)
        ribbon = chip("saturated · even · complete oxidation", BLUE, 30).move_to([0, 2.95, 0])
        gauge = atp_gauge("≈106", center=(5.4, 0.25, 0), color=GOLD, height=4.7)
        ledger = VGroup(counter_box("turns", "7", PURPLE, 2.1, 1.25),
                        counter_box("acetyl-CoA", "8", GREEN, 2.7, 1.25)).arrange(DOWN, buff=0.3).move_to([0.65, 0.25, 0])
        self.add(bg, ribbon, gauge, ledger)
        self.at("saturated")
        self.play(Indicate(ribbon, color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("burned completely")
        co2 = T("complete oxidation → CO₂", 30, TEXT).move_to([0.65, -2.1, 0])
        self.play(FadeIn(co2, shift=UP * 0.1), Rotate(wheel, -PI), run_time=0.9)
        self.at("Double bonds")
        side1_blocks = VGroup(*[carbon_tile(None, 0.35) for _ in range(5)]).arrange(RIGHT, buff=0.04).set_opacity(0.55)
        side1 = VGroup(side1_blocks, T("double bonds  ?", 28, GREY)).arrange(DOWN, buff=0.14).move_to([-4.7, 2.15, 0])
        self.play(FadeIn(side1, shift=RIGHT * 0.12), run_time=0.65)
        self.at("odd chains")
        side2_blocks = VGroup(*[carbon_tile(None, 0.35) for _ in range(5)]).arrange(RIGHT, buff=0.04).set_opacity(0.55)
        side2 = VGroup(side2_blocks, T("odd chains  ?", 28, GREY)).arrange(DOWN, buff=0.14).move_to([-4.7, -2.2, 0])
        self.play(FadeIn(side2, shift=RIGHT * 0.12), run_time=0.65)
        self.at("reusable rule")
        self.play(FadeOut(side1), FadeOut(side2), FadeOut(co2), FadeOut(ribbon), FadeOut(ledger), run_time=0.55)
        icon_wheel = workshop_wheel((-3.65, 0.0, 0), 0.75, False)
        wheel_lab = T("turns", 30, PURPLE).next_to(icon_wheel, DOWN, buff=0.18)
        carts = VGroup(acetyl_cart(False, 0.78), acetyl_cart(False, 0.78)).arrange(UP, buff=0.18).move_to([-0.55, 0.15, 0])
        carts_lab = T("acetyl-CoA", 30, GREEN).next_to(carts, DOWN, buff=0.18)
        cost = VGroup(chip("ATP", RED, 30), Arrow(LEFT * 0.3, RIGHT * 0.3, color=RED, buff=0), chip("AMP", RED, 30)).arrange(RIGHT, buff=0.15).move_to([2.35, 0.15, 0])
        cost_lab = T("activation toll  −2", 30, RED).next_to(cost, DOWN, buff=0.18)
        self.play(ReplacementTransform(wheel, icon_wheel), FadeIn(wheel_lab), FadeIn(carts), FadeIn(carts_lab), FadeIn(cost), FadeIn(cost_lab), run_time=1.0)
        self.at("Count the turns")
        self.play(Rotate(icon_wheel, -TAU), Indicate(wheel_lab, color=PURPLE, scale_factor=1.08), run_time=0.8)
        self.at("the acetyl")
        self.play(carts.animate.shift(UP * 0.18), rate_func=there_and_back, run_time=0.65)
        self.at("activation toll")
        self.play(Indicate(cost, color=RED, scale_factor=1.08), Indicate(gauge, color=GOLD, scale_factor=1.02), run_time=0.75)
        self.finish()


class S11End(EndCard):
    LINE = "Count the turns, the acetyl-CoA, and the activation toll."

    def construct(self):
        hexm = hex_mascot(1.35).move_to([0, 2.25, 0])
        line = T(self.LINE, 40, font=TITLE_FONT)
        fit(line, 11.7).move_to([0, 0.85, 0])
        wheel = add_slow_rotation(workshop_wheel((-3.2, -1.45, 0), 0.62, False), 0.28)
        carts = VGroup(acetyl_cart(False, 0.65), acetyl_cart(False, 0.65)).arrange(UP, buff=0.12).move_to([0, -1.45, 0])
        cost = VGroup(chip("ATP", RED, 28), Arrow(LEFT * 0.25, RIGHT * 0.25, color=RED, buff=0), chip("AMP", RED, 28)).arrange(RIGHT, buff=0.12).move_to([3.2, -1.45, 0])
        sub = T("biochemistrypedia.com", 28, TEAL).move_to([0, -3.2, 0])
        self.play(FadeIn(hexm, shift=UP * 0.15), FadeIn(line), run_time=0.9)
        self.play(FadeIn(wheel), FadeIn(carts), FadeIn(cost), FadeIn(sub), run_time=0.65)
        shoulder = hexm.arm.get_start()
        self.play(Rotate(hexm.arm, -0.55, about_point=shoulder), rate_func=there_and_back, run_time=0.55)
        self.play(carts.animate.shift(UP * 0.14), rate_func=there_and_back, run_time=0.65)
        self.play(Rotate(hexm.arm, -0.55, about_point=shoulder), rate_func=there_and_back, run_time=0.55)
        self.finish()
