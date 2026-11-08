"""Organism problems: five problems and complementary questions  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept, whole film)
  GREEN  = carbon / gas taken in (CO2 in the leaf, oxygen in the lung)
  BLUE   = water / water vapour lost
  PURPLE = stomata and guard cells (and stomatal density)
  YELLOW = the efficiency ratio and the answers drawn from it
  RED    = caution (not proof) and the claim that is wrong
  GREY   = outlines, waxy layer, chest, leaf cells, labels
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CO2 = "C O₂"


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def box(w, h, color=GREY, fill=0.0, r=0.12, sw=3):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill)


def mchip(text, color, size=26, pad=0.22):
    """chip with a multi-line label"""
    lab = T(text, size=size, color=color, line_spacing=0.9)
    b = box(lab.width + 2 * pad, lab.height + 2 * pad, color, 0.14, r=0.16, sw=2.5)
    return VGroup(b, lab.move_to(b))


class Stoma(VGroup):
    """Block cross-section of a leaf surface: waxy layer with one pore between two guard cells,
    leaf cells below. Not to scale. s = overall scale, cx, cy = centre of the waxy layer."""

    def __init__(self, cx=0, cy=0, s=1.0, half=5.5, depth=3.6, opened=True):
        super().__init__()
        self.s, self.cx, self.cy = s, cx, cy
        self.open_half = 0.5 * s
        self.wax_h = 0.34 * s
        gx = 1.3 * s
        L = (half - 1.3) * s
        self.wax_l = box(L, self.wax_h, GREY, 0.45, r=0.05).move_to([cx - gx - L / 2, cy, 0])
        self.wax_r = box(L, self.wax_h, GREY, 0.45, r=0.05).move_to([cx + gx + L / 2, cy, 0])
        self.inner = box(2 * half * s, depth * s, GREY, 0.07, r=0.05, sw=2.5).move_to(
            [cx, cy - self.wax_h / 2 - depth * s / 2, 0])
        gw, gh = 0.8 * s, 0.95 * s
        gap = self.open_half if opened else 0.02
        self.gl = box(gw, gh, PURPLE, 0.45, r=0.3 * s).move_to([cx - gap - gw / 2, cy - 0.25 * s, 0])
        self.gr = box(gw, gh, PURPLE, 0.45, r=0.3 * s).move_to([cx + gap + gw / 2, cy - 0.25 * s, 0])
        self.add(self.inner, self.wax_l, self.wax_r, self.gl, self.gr)

    def close_anims(self):
        gw = 0.8 * self.s
        return [self.gl.animate.move_to([self.cx - 0.02 - gw / 2, self.gl.get_center()[1], 0]),
                self.gr.animate.move_to([self.cx + 0.02 + gw / 2, self.gr.get_center()[1], 0])]


def ratio_text(top="carbon gained", bot="water lost", size=30):
    t = T(top, size, GREEN)
    b = T(bot, size, BLUE)
    ln = Line(LEFT * max(t.width, b.width) / 2, RIGHT * max(t.width, b.width) / 2, color=YELLOW, stroke_width=4)
    g = VGroup(t, ln, b).arrange(DOWN, buff=0.12)
    return g


def leaf_card(name, carbon, water, x, eff_text, res, color=YELLOW, y0=2.7):
    title = T(name, 30, GREY, weight=BOLD).move_to([x, y0, 0])
    c = mchip(carbon, GREEN, 26).move_to([x, y0 - 1.1, 0])
    w = mchip(water, BLUE, 26).move_to([x, y0 - 2.2, 0])
    res_t = VGroup(T(eff_text, 30, YELLOW), T(res, 24, YELLOW)).arrange(DOWN, buff=0.1).move_to([x, y0 - 3.4, 0])
    return title, c, w, res_t


# The organism icons and limb diagrams are schematic, never to scale.
ITEMS = ["Energy and materials", "Exchange / transport / wastes",
         "Internal stability", "Defense", "Lineage continuation"]


def plant():
    stem = Line([0, -0.7, 0], [0, 0.95, 0], color=GREY, stroke_width=4)
    leaves = VGroup(*[Ellipse(width=0.65, height=0.22, color=GREY, fill_opacity=0.2)
                     .rotate(a).move_to([x, y, 0])
                     for x, y, a in [(-0.27, 0.1, -0.5), (0.27, 0.45, 0.5)]])
    grain = VGroup(*[Ellipse(width=0.23, height=0.35, color=GREY, fill_opacity=0.2)
                    .move_to([x, y, 0]) for x, y in [(-0.12, 0.85), (0.12, 1.1), (0, 1.35)]])
    roots = VGroup(*[Line([0, -0.7, 0], [x, -1.15, 0], color=GREY) for x in [-0.5, 0, 0.5]])
    return VGroup(stem, leaves, grain, roots)


def bee():
    body = Ellipse(width=1.3, height=0.65, color=GREY, fill_opacity=0.2)
    wings = VGroup(*[Ellipse(width=0.7, height=0.42, color=GREY).rotate(a).move_to([x, 0.45, 0])
                    for x, a in [(-0.25, -0.6), (0.25, 0.6)]])
    head = Circle(radius=0.24, color=GREY).move_to([0.8, 0.1, 0])
    stripes = VGroup(*[Line([x, -0.25, 0], [x, 0.25, 0], color=GREY) for x in [-0.25, 0, 0.25]])
    return VGroup(body, wings, head, stripes)


def human():
    return VGroup(Circle(radius=0.25, color=GREY).move_to([0, 0.9, 0]),
                  Line([0, 0.65, 0], [0, -0.3, 0], color=GREY, stroke_width=5),
                  Line([-0.6, 0, 0], [0, 0.4, 0], color=GREY, stroke_width=5),
                  Line([0, 0.4, 0], [0.6, 0, 0], color=GREY, stroke_width=5),
                  Line([-0.45, -1.1, 0], [0, -0.3, 0], color=GREY, stroke_width=5),
                  Line([0, -0.3, 0], [0.45, -1.1, 0], color=GREY, stroke_width=5))


def organisms():
    g = VGroup()
    for icon, name, y in [(plant(), "barley plant", 1.65), (bee(), "honeybee", -0.15), (human(), "human", -1.95)]:
        icon.scale(0.48).move_to([4.7, y + 0.15, 0])
        label = T(name, 24, GREY).move_to([4.7, y - 0.7, 0])
        g.add(VGroup(icon, label))
    return g


def checklist(empty=False, x=-2.1):
    rows = VGroup()
    for i, label in enumerate(ITEMS):
        sq = Square(side_length=0.3, color=GREY, stroke_width=2).move_to([x - 3.5, 1.9 - i * 0.92, 0])
        row = VGroup(sq)
        if not empty:
            row.add(T(label, 26, GREY).next_to(sq, RIGHT, buff=0.23))
        rows.add(row)
    return rows


class S00Title(TitleCard):
    LESSON = "What an organism has to do"
    TITLE = "What an Organism Has to Do"

    def construct(self):
        title = T(self.TITLE, 43, font=TITLE_FONT).move_to([0, 3.05, 0])
        self.play(FadeIn(title), FadeIn(checklist(empty=True)), FadeIn(organisms()), run_time=0.8)
        self.finish()


class S08Checklist(SpokenScene):
    def construct(self):
        head = T("A teaching checklist", 36, font=TITLE_FONT).move_to([0, 3.1, 0])
        empty, full, org = checklist(True), checklist(), organisms()
        self.at("Every multicellular organism")
        self.play(FadeIn(head), FadeIn(empty), FadeIn(org), run_time=0.65)
        for i, cue in enumerate(["Get energy", "Exchange and move", "Keep its inside", "Resist damage", "And leave descendants"]):
            self.at(cue)
            self.play(ReplacementTransform(empty[i], full[i]), run_time=0.55)
        self.at("This checklist connects")
        # A shared bracket connects the whole checklist to all three organisms.
        links = VGroup(*[Line([1.8, y, 0], [2.25, y, 0], color=GREY)
                         for y in [1.9, 0.98, 0.06, -0.86, -1.78]],
                       Line([2.25, -1.78, 0], [2.25, 1.9, 0], color=GREY),
                       *[Line([2.25, y, 0], [3.65, y, 0], color=GREY) for y in [1.8, 0, -1.8]])
        self.play(Create(links), run_time=0.8)
        self.at("Every solution carries")
        cost = T("Every solution carries a cost", 30, YELLOW).move_to([0, -3.05, 0])
        self.play(FadeIn(cost), run_time=0.6)
        self.at("how it solves")
        self.play(Indicate(full, color=YELLOW, scale_factor=1.02), run_time=0.8)
        self.at("how its solutions evolved")
        self.play(Indicate(org, color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.finish()


class S09Jobs(SpokenScene):
    def construct(self):
        rows = checklist(x=-2.1)
        title = T("A teaching checklist", 34, font=TITLE_FONT).move_to([0, 3.1, 0])
        self.add(rows, title)
        stage = VGroup()
        extras = []
        def show(i, new):
            nonlocal stage
            self.play(rows.animate.set_color(GREY), FadeOut(stage),
                      *[FadeOut(m) for m in extras], run_time=0.2)
            extras.clear()
            self.play(rows[i].animate.set_color(YELLOW), FadeIn(new), run_time=0.5)
            stage = new
        self.at("Plants capture light")
        pl = plant().move_to([4.5, 0.1, 0])
        light = VGroup(T("light", 25, GREY).move_to([3.2, 2, 0]), arr([3.3, 1.6, 0], [4.1, 0.8, 0], GREY))
        show(0, VGroup(pl, light))
        self.at("water and minerals")
        root_in = VGroup(T("water + minerals", 22, BLUE).move_to([4.3, -2.1, 0]),
                         arr([4.5, -1.8, 0], [4.5, -0.85, 0], BLUE))
        self.play(FadeIn(root_in), run_time=0.6); extras.append(root_in)
        self.at("Materials must reach")
        cells = VGroup(*[box(0.65, 0.8, GREY, 0.1).move_to([x, 0.2, 0]) for x in [3.1, 4.25, 5.4]])
        incoming = arr([2.7, 1.6, 0], [5.6, 1.6, 0], GREY)
        show(1, VGroup(cells, incoming, T("to every cell", 24, GREY).move_to([4.3, 2.2, 0])))
        self.at("wastes must leave")
        waste = VGroup(arr([4.25, -0.4, 0], [4.25, -1.6, 0], GREY), T("wastes out", 24, GREY).move_to([4.25, -2.15, 0]))
        self.play(FadeIn(waste), run_time=0.5); extras.append(waste)
        self.at("Homeostasis keeps")
        boundary = box(3.2, 2.8, GREY, 0.05).move_to([4.25, 0, 0])
        band = box(2.5, 0.5, YELLOW, 0.1).move_to([4.25, 0, 0])
        dot = Dot([3.6, 0, 0], color=GREY)
        show(2, VGroup(boundary, band, dot, T("relatively stable", 23, GREY).move_to([4.25, -2, 0])))
        self.play(dot.animate.shift(RIGHT * 1.2), run_time=0.8)
        self.at("Defense resists")
        shield = Polygon([3, 1.2, 0], [5.5, 1.2, 0], [5.25, -0.7, 0], [4.25, -1.5, 0], [3.25, -0.7, 0], color=GREY)
        threat = arr([2.6, 0.2, 0], [3.1, 0.2, 0], RED)
        show(3, VGroup(shield, threat, T("damage / invasion", 22, GREY).move_to([4.25, -2.15, 0])))
        self.at("Reproduction continues")
        line = VGroup(mchip("lineage", GREY, 26).move_to([4.25, 1.7, 0]),
                      arr([4.25, 1.1, 0], [4.25, -0.1, 0], GREY),
                      mchip("descendants", GREY, 24).move_to([4.25, -0.65, 0]))
        show(4, line)
        self.at("worker can help")
        self.play(FadeOut(stage), run_time=0.25)
        worker = bee().scale(0.65).move_to([3.1, 0.7, 0])
        relatives = VGroup(bee().scale(0.4).move_to([5.3, 0.9, 0]), bee().scale(0.4).move_to([5.3, -0.2, 0]))
        self.play(FadeIn(worker), FadeIn(relatives), GrowArrow(arr([3.9, 0.5, 0], [4.65, 0.5, 0], GREY)),
                  FadeIn(T("worker helps raise\nclose relatives", 24, GREY).move_to([4.3, -1.8, 0])), run_time=0.7)
        self.finish()


class S01Pore(SpokenScene):
    def construct(self):
        head = VGroup(*[T(label, 22, YELLOW if i == 1 else GREY).move_to([x, 3.3, 0])
                        for i, (x, label) in enumerate(zip([-5, -2.5, 0, 2.5, 5],
                        ["Energy", "Exchange", "Stability", "Defense", "Lineage"]))])
        st = Stoma(0, 0.45, 1, depth=3.0)
        wax = T("waxy layer", 25, GREY).move_to([-4.2, 1.05, 0])
        wet = Line([-4.6, -1.5, 0], [4.6, -1.5, 0], color=BLUE, stroke_width=6)
        cells = T("wet internal cell walls", 26, BLUE).move_to([0, -2.3, 0])
        self.at("A barley leaf")
        self.play(FadeIn(head), FadeIn(st), FadeIn(wax), FadeIn(wet), FadeIn(cells), run_time=0.7)
        self.at("Carbon dioxide enters")
        ain = arr([-0.25, 2.4, 0], [-0.25, -1.1, 0], GREEN)
        cin = T(f"{CO2} in", 28, GREEN).move_to([-2.3, 2.3, 0])
        self.play(GrowArrow(ain), FadeIn(cin), run_time=0.7)
        self.at("tiny pores called stomata")
        gl = T("guard cells / stoma", 25, PURPLE).move_to([3.7, 1.3, 0])
        self.play(FadeIn(gl), Indicate(VGroup(st.gl, st.gr), color=PURPLE), run_time=0.6)
        self.at("Water vapor leaves")
        aout = arr([0.25, -1.35, 0], [0.25, 2.4, 0], BLUE)
        wout = T("water vapour out", 28, BLUE).move_to([3.3, 2.3, 0])
        self.play(GrowArrow(aout), FadeIn(wout), run_time=0.7)
        self.at("both things happen")
        self.play(Indicate(ain, color=GREEN), Indicate(aout, color=BLUE), run_time=0.7)
        self.finish()


class S02Lung(SpokenScene):
    def construct(self):
        st = Stoma(-3.6, 0.4, 0.5, depth=5)
        leaf = VGroup(st, T("barley leaf", 28, GREY).move_to([-3.6, 3.1, 0]),
                      arr([-3.8, 2.3, 0], [-3.8, -0.7, 0], GREEN), arr([-3.4, -0.7, 0], [-3.4, 2.3, 0], BLUE))
        self.add(leaf)
        chest = box(5.5, 5.5, GREY).move_to([3.5, -0.1, 0])
        lung = box(4.6, 3.5, GREY, 0.07).move_to([3.5, -0.4, 0])
        sac = box(3.5, 1.8, BLUE, 0.08).move_to([3.5, -0.8, 0])
        airway = VGroup(Line([3.25, 2.4, 0], [3.25, 0.2, 0], color=BLUE, stroke_width=4),
                        Line([3.75, 2.4, 0], [3.75, 0.2, 0], color=BLUE, stroke_width=4))
        labels = VGroup(T("lung inside chest", 27, GREY).move_to([3.5, 3.1, 0]),
                        T("air-sac lining: wet film", 24, BLUE).move_to([3.5, -2.3, 0]))
        self.at("Your lungs face")
        self.play(FadeIn(chest), FadeIn(lung), FadeIn(labels[0]), run_time=0.7)
        self.at("Gas must dissolve")
        gas = arr([2.7, 0.6, 0], [2.7, -1.3, 0], GREEN)
        self.play(FadeIn(sac), FadeIn(airway), FadeIn(labels[1]), GrowArrow(gas), run_time=0.7)
        self.at("before entering cells")
        self.play(Indicate(sac, color=BLUE, scale_factor=1.03), run_time=0.6)
        self.at("A wet surface")
        loss = arr([4.1, -0.6, 0], [4.1, 2.45, 0], BLUE)
        self.play(GrowArrow(loss), run_time=0.65)
        self.at("In ordinary")
        # The airway wall supplies moisture on entry and recovers some on exit.
        note = T("airways moisten air;\nrecover some water out", 22, BLUE).move_to([0, -3.2, 0])
        recovered = arr([4.05, 1.1, 0], [3.75, 1.1, 0], BLUE, w=4, tip=0.12)
        self.play(FadeIn(note), GrowArrow(recovered), run_time=0.6)
        self.at("each breath carries")
        out = T("water still leaves", 24, BLUE).move_to([-3.6, -2.7, 0])
        self.play(FadeIn(out), Indicate(loss, color=BLUE), run_time=0.7)
        self.at("Neither solution escapes")
        self.play(Indicate(leaf, color=YELLOW, scale_factor=1.02), Indicate(chest, color=YELLOW, scale_factor=1.02), run_time=0.7)
        self.finish()


class S03Ratio(SpokenScene):
    def construct(self):
        eq = T("water-use efficiency =", 32, YELLOW)
        fr = ratio_text(size=32)
        formula = VGroup(eq, fr).arrange(RIGHT, buff=0.4).move_to([0, 2.3, 0])
        self.at("Water use efficiency")
        self.play(FadeIn(formula), run_time=0.7)
        self.at("Here are made")
        note = T("Illustrative leaves — not barley data", 27, GREY).move_to([0, 0.6, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.at("Leaf A gains")
        carbon = mchip(f"Leaf A: 20 µmol {CO2}\nper m² per s", GREEN, 27).move_to([-3.3, -0.8, 0])
        self.play(FadeIn(carbon), run_time=0.65)
        self.at("and loses")
        water = mchip("5 mmol H₂O\nper m² per s", BLUE, 27).move_to([3.3, -0.8, 0])
        self.play(FadeIn(water), run_time=0.65)
        self.at("Its efficiency is")
        result = VGroup(T("20 / 5 = 4.0", 43, YELLOW), T(f"µmol {CO2} per mmol H₂O", 26, YELLOW)).arrange(DOWN, buff=0.15).move_to([0, -2.6, 0])
        self.play(FadeIn(result, scale=1.05), run_time=0.65)
        self.finish()


def comparison_card(name, carbon, water, result, x):
    return VGroup(T(name, 30, GREY, weight=BOLD).move_to([x, 2.8, 0]),
                  mchip(f"{carbon} µmol {CO2} per m² per s", GREEN, 23).move_to([x, 1.6, 0]),
                  mchip(f"{water} mmol H₂O per m² per s", BLUE, 23).move_to([x, 0.5, 0]),
                  VGroup(T(result, 37, YELLOW), T(f"µmol {CO2} per mmol H₂O", 22, YELLOW)).arrange(DOWN, buff=0.13).move_to([x, -0.85, 0]))


class S04Leafb(SpokenScene):
    def construct(self):
        a = comparison_card("Leaf A", 20, 5, "20 / 5 = 4.0", -3.3)
        b = comparison_card("Leaf B", 16, 3, "16 / 3 = 5.3", 3.3)
        note = T("Illustrative values — not barley data", 23, GREY).move_to([0, -3.35, 0])
        self.add(a, note)
        self.at("Leaf B gains")
        self.play(FadeIn(b[0]), FadeIn(b[1]), run_time=0.5)
        self.at("and loses")
        self.play(FadeIn(b[2]), run_time=0.5)
        self.at("Its efficiency is")
        self.play(FadeIn(b[3]), run_time=0.5)
        self.at("When water is scarce")
        case = T("Water scarce: B keeps more water per unit carbon", 27, YELLOW).move_to([0, -2.3, 0])
        self.play(FadeIn(case), Indicate(b[3], color=YELLOW), run_time=0.65)
        self.at("When water is plentiful")
        new = T("Water plentiful, carbon limits growth: A gains more", 27, YELLOW).move_to([0, -2.3, 0])
        self.play(ReplacementTransform(case, new), run_time=0.6)
        self.at("gains more")
        self.play(Indicate(a[1], color=GREEN), run_time=0.6)
        self.finish()


def limb(kind):
    # Shared one / two / wrist / digits layout, reshaped in each lineage.
    length, spread = {"human arm": (1.0, 0.45), "bat wing": (0.8, 1.0), "whale flipper": (0.55, 0.65)}[kind]
    upper = Line([0, 1.1, 0], [0, 0.4, 0], color=GREY, stroke_width=9)
    lower = VGroup(*[Line([x, 0.4, 0], [x, 0.4-length, 0], color=GREY, stroke_width=6) for x in [-0.12, 0.12]])
    y = 0.4-length
    wrist = VGroup(*[Dot([x, y-0.13, 0], radius=0.07, color=GREY) for x in [-0.16, 0, 0.16]])
    digits = VGroup(*[Line([0, y-0.22, 0], [spread*d, y-0.8-0.2*(2-abs(d)), 0], color=GREY, stroke_width=3) for d in [-2,-1,0,1,2]])
    return VGroup(upper, lower, wrist, digits)


class S06Rule(SpokenScene):
    def construct(self):
        title = T("Why do structures fit what they do?", 35, font=TITLE_FONT).move_to([0, 3.05, 0])
        self.at("Why do structures")
        self.play(FadeIn(title), run_time=0.6)
        def population(xs):
            return VGroup(*[box(0.55, 0.6 + 0.14*k, GREY, 0.14).move_to([x, 0.5, 0]) for x,k in xs])
        first = population([(-4.8,0),(-3.9,1),(-3,2)])
        later = population([(1.6,0),(2.5,2),(3.4,2),(4.3,2)])
        self.at("Natural selection acts")
        self.play(FadeIn(first), FadeIn(T("inherited variation", 26, GREY).move_to([-3.9, -0.6, 0])), run_time=0.65)
        self.at("Over generations")
        timeline = arr([-1.7, 0.5, 0], [0.7, 0.5, 0], GREY)
        self.play(GrowArrow(timeline), FadeIn(later), run_time=0.7)
        self.at("greater reproductive success")
        success = T("greater reproductive success", 26, YELLOW).move_to([2.8, -0.6, 0])
        self.play(FadeIn(success), run_time=0.6)
        self.at("can become more common")
        self.play(*[later[i].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.25) for i in [1,2,3]], run_time=0.7)
        self.at("But the fit")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not title], run_time=0.5)
        sub = T("The fit is never perfect", 30, YELLOW).move_to([0, 1.9, 0])
        self.play(FadeIn(sub), run_time=0.5)
        self.at("link gains to costs")
        trade = VGroup(mchip("carbon gain", GREEN, 28).move_to([-3.6, 0.2, 0]),
                       mchip("water loss", BLUE, 28).move_to([3.6, 0.2, 0]),
                       DoubleArrow([-1.8,0.2,0],[1.8,0.2,0], color=YELLOW))
        self.play(FadeIn(trade), run_time=0.6)
        self.at("Selection works with")
        self.play(FadeOut(trade), FadeOut(sub), run_time=0.3)
        ancestry = T("Inherited structures, reshaped", 28, GREY).move_to([0, 2, 0])
        limbs = VGroup(*[VGroup(limb(k).move_to([x, -0.05, 0]), T(k, 25, GREY).move_to([x, -2.1, 0]))
                         for x,k in [(-4,"human arm"),(0,"bat wing"),(4,"whale flipper")]])
        initial = VGroup(*[VGroup(limb("human arm").move_to([x, -0.05, 0]),
                              T(k, 25, GREY).move_to([x, -2.1, 0]))
                            for x,k in [(-4,"human arm"),(0,"bat wing"),(4,"whale flipper")]])
        self.play(FadeIn(ancestry), FadeIn(initial), run_time=0.35)
        self.play(ReplacementTransform(initial, limbs), run_time=0.7)
        self.at("Some changes spread")
        self.play(FadeOut(limbs), FadeOut(ancestry), run_time=0.3)
        chance = mchip("chance", GREY, 32).move_to([-3, 0.3, 0])
        self.play(FadeIn(chance), run_time=0.5)
        self.at("some features are")
        byproduct = mchip("by-products", GREY, 32).move_to([3, 0.3, 0])
        self.play(FadeIn(byproduct), run_time=0.5)
        self.at("Evolution has no")
        rule = T("No preconceived ideal", 36, YELLOW).move_to([0, -2, 0])
        self.play(FadeIn(rule), run_time=0.7)
        self.finish()


class S10Questions(SpokenScene):
    def construct(self):
        title = T("Complementary questions", 37, font=TITLE_FONT).move_to([0, 3.2, 0])
        left = T("PROXIMATE", 28, GREY).move_to([-3.3, 2.25, 0])
        right = T("ULTIMATE", 28, GREY).move_to([3.3, 2.25, 0])
        self.at("We also need")
        self.play(FadeIn(title), run_time=0.6)
        self.at("Mechanism asks")
        mech = mchip("Mechanism\nguard-cell movement", GREY, 26).move_to([-3.3, 0.85, 0])
        self.play(FadeIn(left), FadeIn(mech), run_time=0.6)
        guards = VGroup(box(0.25,0.5,PURPLE,0.3).move_to([-3.5,-0.15,0]),box(0.25,0.5,PURPLE,0.3).move_to([-3.1,-0.15,0]))
        self.at("open and close")
        self.play(FadeIn(guards), run_time=0.2)
        self.play(guards[0].animate.shift(LEFT*0.2), guards[1].animate.shift(RIGHT*0.2), run_time=0.35)
        self.play(guards[0].animate.shift(RIGHT*0.2), guards[1].animate.shift(LEFT*0.2), run_time=0.35)
        self.at("Development asks")
        dev = mchip("Development\ngenes → stomatal number", GREY, 26).move_to([-3.3, -1.5, 0])
        self.play(FadeOut(guards), FadeIn(dev), run_time=0.6)
        self.at("Adaptive significance asks")
        adapt = mchip("Adaptive significance\nsurvival + reproduction\nin an environment", GREY, 25).move_to([3.3, 0.65, 0])
        self.play(FadeIn(right), FadeIn(adapt), run_time=0.6)
        self.at("History asks")
        hist = mchip("History\nchanges across a lineage", GREY, 26).move_to([3.3, -1.5, 0])
        self.play(FadeIn(hist), run_time=0.6)
        self.at("The first pair")
        self.play(left.animate.set_color(YELLOW), run_time=0.4)
        lifetime = T("organism’s lifetime", 25, YELLOW).move_to([-3.3,-2.8,0])
        self.play(FadeIn(lifetime), run_time=0.4)
        self.at("The second concerns")
        evo = T("evolution", 25, YELLOW).move_to([3.3,-2.8,0])
        self.play(right.animate.set_color(YELLOW), FadeIn(evo), run_time=0.5)
        self.at("A full account")
        # Collapse the examples into the two questions and restore all five problems.
        self.play(FadeOut(VGroup(title,mech,dev,adapt,hist,lifetime,evo)),
                  left.animate.move_to([-2.4,-2.7,0]), right.animate.move_to([2.4,-2.7,0]), run_time=0.5)
        frame = VGroup(*[T(label, 24, GREY).move_to([0, 2.6-i*0.85, 0]) for i,label in enumerate(ITEMS)])
        self.play(FadeIn(frame), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Every organism solves the same problems, and each solution has a cost."
    def construct(self):
        title = T(self.LINE, 43, font=TITLE_FONT).move_to([0,3.05,0])
        fit(title, max_w=12.5)
        self.play(FadeIn(title), FadeIn(checklist()), FadeIn(organisms()), run_time=0.7)
        self.finish()
