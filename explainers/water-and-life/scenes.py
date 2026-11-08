"""Water and Life: why water warms so slowly  (Biochemistrypedia high school Biology explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = water (water molecules, the Bay, the water bar)
  PURPLE = the slightly negative (oxygen) end
  ORANGE = the slightly positive (hydrogen) end
  TEAL   = attraction between molecules (hydrogen bonds, cohesion, adhesion lines)
  RED    = air at the buoy (the air bar)
  PINK   = air over land (closing sketch only, not buoy data)
  YELLOW = energy added (joules)
  SAND   = dry sand
  GREY   = outlines, labels, covalent bars, other materials (fibre, strider, salt)
  TEXT   = vocabulary words on screen
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SAND = "#C9A66B"
LAND = "#E58BC4"   # air over land (schematic), distinct from the buoy air (RED)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def block(label, pos, color=BLUE, side=1.0, size=44, fill=0.25):
    sq = RoundedRectangle(corner_radius=0.16, width=side, height=side, stroke_color=color, stroke_width=4,
                          fill_color=color, fill_opacity=fill)
    t = T(label, size, TEXT, weight=BOLD).move_to(sq)
    g = VGroup(sq, t).move_to(pos)
    return g


def recolor_block(b, color):
    return [b[0].animate.set_stroke(color).set_fill(color, 0.3)]


def bond_bar(a, b, color=TEXT, w=9):
    d = b.get_center() - a.get_center()
    d = d / np.linalg.norm(d)
    p0 = a.get_center() + d * (a[0].width / 2)
    p1 = b.get_center() - d * (b[0].width / 2)
    return Line(p0, p1, color=color, stroke_width=w)


def dashed(p0, p1, color=TEAL, w=5):
    return DashedLine(p0, p1, color=color, stroke_width=w, dash_length=0.12, dashed_ratio=0.55)


def pill(w=0.8, h=0.32):
    """A small water molecule, schematic: outlined capsule, purple (O) end on the left, orange (H) end on the right."""
    body = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.18)
    sq = h * 0.6
    o = Square(side_length=sq, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(body.get_left() + RIGHT * (sq * 0.9))
    hh = Square(side_length=sq, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(body.get_right() + LEFT * (sq * 0.9))
    return VGroup(body, o, hh)


def label(text, pos, color=TEXT, size=26, weight=NORMAL):
    return T(text, size, color, weight=weight).move_to(pos)


def vocab(text, pos):
    return T(text, 40, TEXT, weight=BOLD).move_to(pos)


def water_molecule(center, s=1.0, charged=False):
    """Three labelled blocks (O, H, H) and two covalent bars. Returns a VGroup with .O .Hl .Hr .bl .br."""
    O = block("O", center + np.array([0, -1.0, 0]) * s, PURPLE if charged else GREY, side=1.0 * s, size=int(44 * s))
    Hl = block("H", center + np.array([-2.0, 1.0, 0]) * s, ORANGE if charged else GREY, side=0.9 * s, size=int(40 * s))
    Hr = block("H", center + np.array([2.0, 1.0, 0]) * s, ORANGE if charged else GREY, side=0.9 * s, size=int(40 * s))
    bl, br = bond_bar(O, Hl), bond_bar(O, Hr)
    g = VGroup(bl, br, O, Hl, Hr)
    g.O, g.Hl, g.Hr, g.bl, g.br = O, Hl, Hr, bl, br
    return g


def bar_chart(x_air, x_water, base_y, k, air_h=8.0, water_h=1.4):
    air = Rectangle(width=1.4, height=air_h * k, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.4)
    air.move_to([x_air, base_y + air_h * k / 2, 0])
    wat = Rectangle(width=1.4, height=water_h * k, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
    wat.move_to([x_water, base_y + water_h * k / 2, 0])
    return air, wat


class S00Title(TitleCard):
    LESSON = "Water and life"
    TITLE = "Why Water Warms So Slowly"


# ---------------------------------------------------------------------------------------------
class S01Buoy(SpokenScene):
    """Two bars from one Bay buoy: air about 8 C, water under 1.5 C; then the question."""

    def construct(self):
        base_y, k = -2.6, 0.57
        head = T("Chesapeake Bay buoy, Stingray Point, Virginia", 26, GREY).to_edge(UP, buff=0.5)
        base = Line([-6.2, base_y, 0], [0.4, base_y, 0], color=GREY, stroke_width=3)
        air, wat = bar_chart(-4.3, -1.5, base_y, k)
        air_lbl = label("air", [-4.3, base_y - 0.4, 0], RED, 28)
        wat_lbl = label("water", [-1.5, base_y - 0.4, 0], BLUE, 28)
        axis = T("change in temperature over one July day", 22, GREY).move_to([-3.0, base_y - 0.95, 0])
        self.at("On a July day")
        self.play(FadeIn(head), Create(base), run_time=0.6)
        self.play(FadeIn(air_lbl), FadeIn(wat_lbl), FadeIn(axis), run_time=0.4)
        air_v = M("about 8 °C", 30, RED).move_to([-4.3, base_y + 8 * k + 0.4, 0])
        self.at("warmed by about")
        self.play(GrowFromEdge(air, DOWN), run_time=1.2)
        self.play(FadeIn(air_v), run_time=0.3)
        wat_v = M("less than 1.5 °C", 26, BLUE).move_to([-1.5, base_y + 1.4 * k + 0.5, 0])
        self.at("just under the buoy")
        self.play(GrowFromEdge(wat, DOWN), run_time=0.6)
        self.play(FadeIn(wat_v), run_time=0.3)
        q1 = T("Why does water", 38, TEXT, weight=BOLD)
        q1b = T("behave so strangely?", 38, TEXT, weight=BOLD)
        q2 = T("How does that keep", 34, TEAL)
        q2b = T("living things alive?", 34, TEAL)
        qa = VGroup(q1, q1b).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        qb = VGroup(q2, q2b).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        VGroup(qa, qb).arrange(DOWN, aligned_edge=LEFT, buff=0.8).move_to([3.6, 0.2, 0])
        self.at("Why does water behave")
        self.play(FadeIn(qa, shift=LEFT * 0.2), run_time=0.6)
        self.at("keep living things alive")
        self.play(FadeIn(qb, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Polar(SpokenScene):
    """O and H blocks, covalent bars, shared electrons pulled to oxygen, charges appear, polar."""

    def construct(self):
        c = np.array([0, -0.2, 0])
        m = water_molecule(c, 1.0, charged=False)
        O, Hl, Hr = m.O, m.Hl, m.Hr
        o_lbl = label("oxygen atom", O.get_center() + DOWN * 1.0, TEXT, 26)
        hl_lbl = label("hydrogen", Hl.get_center() + LEFT * 1.55, TEXT, 26)
        hr_lbl = label("hydrogen", Hr.get_center() + RIGHT * 1.55, TEXT, 26)
        self.at("A water molecule")
        self.play(FadeIn(O, scale=0.8), run_time=0.4)
        self.play(FadeIn(Hl, scale=0.8), FadeIn(Hr, scale=0.8), FadeIn(o_lbl), FadeIn(hl_lbl), FadeIn(hr_lbl), run_time=0.6)
        self.at("covalent bonds")
        self.play(Create(m.bl), Create(m.br), run_time=0.6)
        cov = vocab("covalent bond", [0, -3.2, 0])
        self.play(Indicate(VGroup(m.bl, m.br), color=YELLOW, scale_factor=1.0), FadeIn(cov), run_time=0.8)
        sub = T("atoms share electrons", 28, GREY).move_to([0, -3.2, 0])
        self.at("atoms share")
        self.play(ReplacementTransform(cov, sub), run_time=0.4)
        # shared electrons pulled toward oxygen (arrows along the bars)
        def toward(a, b):
            d = b.get_center() - a.get_center()
            d = d / np.linalg.norm(d)
            mid = (a.get_center() + b.get_center()) / 2
            return Arrow(mid - d * 0.5 + np.array([-d[1], d[0], 0]) * 0.4,
                         mid + d * 0.55 + np.array([-d[1], d[0], 0]) * 0.4, buff=0, color=YELLOW, stroke_width=8,
                         tip_length=0.3, max_tip_length_to_length_ratio=0.5)
        a1, a2 = toward(Hl, O), toward(Hr, O)
        self.at("pulls the shared electrons")
        pull = T("electrons pulled toward oxygen", 28, YELLOW).move_to([0, -3.2, 0])
        self.play(GrowArrow(a1), GrowArrow(a2), ReplacementTransform(sub, pull), run_time=0.7)
        neg = T("slightly −", 30, PURPLE, weight=BOLD).move_to(O.get_center() + DOWN * 1.0)
        self.at("slightly negative")
        self.play(*recolor_block(O, PURPLE), ReplacementTransform(o_lbl, neg), run_time=0.6)
        pos_l = T("slightly +", 30, ORANGE, weight=BOLD).move_to(Hl.get_center() + UP * 0.95)
        pos_r = T("slightly +", 30, ORANGE, weight=BOLD).move_to(Hr.get_center() + UP * 0.95)
        self.at("slightly positive")
        self.play(*recolor_block(Hl, ORANGE), *recolor_block(Hr, ORANGE), FadeIn(pos_l), FadeIn(pos_r), run_time=0.6)
        polar = vocab("polar", [0, 3.0, 0]).scale(1.3)
        self.at("A molecule like that")
        self.play(FadeOut(pull), FadeIn(polar, scale=0.8), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Bond(SpokenScene):
    """Two molecules; a dashed hydrogen bond between H of one and O of the neighbor; it flickers; weaker than covalent."""

    def construct(self):
        m1 = water_molecule(np.array([-3.4, -0.3, 0]), 0.9, charged=True)
        O2 = block("O", np.array([1.0, 0.6, 0]), PURPLE, side=0.9, size=40)
        H2a = block("H", O2.get_center() + np.array([0.9, 1.8, 0]), ORANGE, side=0.8, size=36)
        H2b = block("H", O2.get_center() + np.array([0.9, -1.8, 0]), ORANGE, side=0.8, size=36)
        m2 = VGroup(bond_bar(O2, H2a), bond_bar(O2, H2b), O2, H2a, H2b)
        leg = VGroup(chip("slightly negative", PURPLE, 26), chip("slightly positive", ORANGE, 26)).arrange(RIGHT, buff=0.5)
        leg.move_to([0, -3.15, 0])
        self.at("Opposite charges attract")
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(leg), run_time=0.8)
        p0 = m1.Hr.get_right() + RIGHT * 0.05
        p1 = O2.get_left() + LEFT * 0.05
        hb = dashed(p0, p1, TEAL, 7)
        self.at("drawn to the oxygen")
        self.play(Create(hb), Indicate(VGroup(m1.Hr[0], O2[0]), color=TEAL, scale_factor=1.25), run_time=0.9)
        hb_lbl = vocab("hydrogen bond", [-1.7, 1.95, 0]).set_color(TEAL)
        self.at("is a hydrogen bond")
        self.play(FadeIn(hb_lbl, shift=DOWN * 0.1), run_time=0.5)
        self.at("form and break")
        for _ in range(3):
            self.play(FadeOut(hb), run_time=0.22)
            self.play(Create(hb), run_time=0.28)
        self.at("much weaker")
        solid = Line(m1.bl.get_start(), m1.bl.get_end(), color=YELLOW, stroke_width=12)
        cov_lbl = T("covalent bond: inside one molecule", 24, YELLOW).move_to([-4.0, -2.3, 0])
        weak = T("hydrogen bond: much weaker", 24, TEAL).move_to([2.8, -2.3, 0])
        self.play(FadeOut(hb_lbl), FadeIn(cov_lbl), Create(solid), FadeIn(weak), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Stick(SpokenScene):
    """Three panels: solvent (salt pulled apart), cohesion + surface tension (strider), adhesion (paper fibre)."""

    def construct(self):
        # ---- panel 1: solvent ----
        def sq(sign, pos):
            return block(sign, np.array(pos), ORANGE if sign == "+" else PURPLE, side=0.7, size=32, fill=0.3)
        cx, cy = -5.6, -0.9
        crystal = VGroup(sq("+", [cx - 0.35, cy + 0.35, 0]), sq("−", [cx + 0.35, cy + 0.35, 0]),
                         sq("−", [cx - 0.35, cy - 0.35, 0]), sq("+", [cx + 0.35, cy - 0.35, 0]))
        cry_lbl = label("salt crystal", [cx, -1.9, 0], GREY, 26)
        t1 = vocab("solvent", [-4.4, 2.9, 0])
        self.at("A solvent")
        self.play(FadeIn(t1, shift=DOWN * 0.1), FadeIn(crystal), FadeIn(cry_lbl), run_time=0.7)

        def oriented_pill(center, toward):
            p = pill(0.95, 0.4)
            d = np.array(toward, float) - np.array(center, float)
            p.rotate(np.arctan2(d[1], d[0])).move_to(center)   # right (orange H) end points at the particle
            return p
        part = crystal[1]
        dest = np.array([-3.6, 0.9, 0])
        pills = VGroup(*[oriented_pill(dest + 1.05 * np.array([np.cos(a), np.sin(a), 0]), dest)
                         for a in (np.pi / 2, 0.0, -np.pi / 2)])
        part_lbl = label("charged particle", [-3.3, -1.15, 0], GREY, 24)
        self.at("pull salt apart")
        self.play(part.animate.move_to(dest), run_time=1.0)
        self.play(FadeIn(pills, scale=0.8), FadeIn(part_lbl), run_time=0.6)

        # ---- panel 2: cohesion / surface tension ----
        xs = [-1.35, 0.0, 1.35]
        rows = [0.3, -0.8, -1.9]
        mols = VGroup(*[pill(0.95, 0.4).move_to([x, y, 0]) for y in rows for x in xs])
        lines = VGroup()
        for y in rows:
            for i in range(2):
                lines.add(dashed([xs[i] + 0.48, y, 0], [xs[i + 1] - 0.48, y, 0], TEAL, 4))
        for x in xs:
            for y0, y1 in ((rows[0], rows[1]), (rows[1], rows[2])):
                lines.add(dashed([x, y0 - 0.22, 0], [x, y1 + 0.22, 0], TEAL, 4))
        water_lbl = label("water", [0, -2.7, 0], BLUE, 26)
        t2 = vocab("cohesion", [0.0, 2.9, 0])
        self.at("Cohesion is")
        self.play(FadeIn(t2, shift=DOWN * 0.1), FadeIn(mols), FadeIn(water_lbl), run_time=0.6)
        self.play(Create(lines), run_time=0.8)
        t2b = T("surface tension", 34, TEXT, weight=BOLD).move_to([0.0, 2.3, 0])
        surf = Line([-2.0, 0.62, 0], [2.0, 0.62, 0], color=YELLOW, stroke_width=5)
        self.at("surface tension")
        self.play(FadeIn(t2b, shift=DOWN * 0.1), Create(surf), run_time=0.6)
        strider = VGroup(RoundedRectangle(corner_radius=0.12, width=2.3, height=0.6, stroke_color=GREY,
                                          stroke_width=3, fill_color=GREY, fill_opacity=0.35),
                         T("water strider", 24, TEXT))
        strider[1].move_to(strider[0])
        strider.move_to([0, 1.2, 0])
        self.at("water strider")
        self.play(FadeIn(strider, shift=DOWN * 0.3), run_time=0.6)

        # ---- panel 3: adhesion ----
        t3 = vocab("adhesion", [4.6, 2.9, 0])
        fibre = Rectangle(width=0.45, height=4.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4)
        fibre.move_to([3.6, 0.0, 0])
        fib_lbl = label("paper fibre", [3.9, -3.0, 0], GREY, 26)
        pool = Rectangle(width=3.2, height=0.8, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.25)
        pool.move_to([4.6, -2.0, 0])
        def vpill(y):
            p = pill(0.95, 0.4)
            p.rotate(-PI / 2).move_to([4.5, y, 0])
            return p
        col = VGroup(vpill(-1.0), vpill(0.2))
        self.at("Adhesion is")
        self.play(FadeIn(t3, shift=DOWN * 0.1), FadeIn(pool), FadeIn(fibre), FadeIn(fib_lbl), FadeIn(col), run_time=0.7)
        sticks = VGroup(*[dashed([3.85, y, 0], [4.3, y, 0], TEAL, 5) for y in (-1.0, 0.2)])
        self.at("different substance")
        self.play(Create(sticks), run_time=0.5)
        new = vpill(-1.0)
        self.at("such as paper")
        self.play(col.animate.shift(UP * 1.2), sticks.animate.shift(UP * 1.2), run_time=1.0)
        self.play(FadeIn(new, shift=UP * 0.2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Heat(SpokenScene):
    """Specific heat bars (4.18 vs 0.8), energy into hydrogen bonds, then 836.8 J: water +2 C, sand about +10 C."""

    def construct(self):
        # ---- A: specific heat bars ----
        head = T("energy to warm 1 gram by 1 °C", 32, TEXT, weight=BOLD).move_to([0, 2.7, 0])
        sub = T("joules", 24, GREY).next_to(head, DOWN, buff=0.15)
        x0, k = -2.6, 1.55
        w_bar = Rectangle(width=4.18 * k, height=1.1, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
        w_bar.move_to([x0 + 4.18 * k / 2, 0.7, 0])
        s_bar = Rectangle(width=0.8 * k, height=1.1, stroke_color=SAND, stroke_width=3, fill_color=SAND, fill_opacity=0.4)
        s_bar.move_to([x0 + 0.8 * k / 2, -0.8, 0])
        w_lbl = label("liquid water", [x0 - 0.2 - 1.45, 0.7, 0], BLUE, 32)
        s_lbl = label("dry sand", [x0 - 0.2 - 1.05, -0.8, 0], SAND, 32)
        w_val = M("4.18", 38, BLUE).next_to(w_bar, RIGHT, buff=0.3)
        s_val = M("about 0.8", 34, SAND).next_to(s_bar, RIGHT, buff=0.3)
        self.at("Specific heat is")
        self.play(FadeIn(head), FadeIn(sub), run_time=0.6)
        self.at("For liquid water")
        self.play(FadeIn(w_lbl), GrowFromEdge(w_bar, LEFT), run_time=0.9)
        self.play(FadeIn(w_val), run_time=0.3)
        self.at("For dry sand")
        self.play(FadeIn(s_lbl), GrowFromEdge(s_bar, LEFT), run_time=0.6)
        self.play(FadeIn(s_val), run_time=0.3)
        A = VGroup(head, sub, w_bar, s_bar, w_lbl, s_lbl, w_val, s_val)

        # ---- B: energy goes into hydrogen bonds ----
        row = VGroup(*[pill(1.8, 0.7).move_to([x, 0.3, 0]) for x in (-3.0, 0.0, 3.0)])
        hbs = VGroup(dashed([-2.0, 0.3, 0], [-0.9, 0.3, 0], TEAL, 7), dashed([0.9, 0.3, 0], [2.0, 0.3, 0], TEAL, 7))
        e_arrows = VGroup(*[Arrow([x, 2.6, 0], [x, 1.2, 0], buff=0, color=YELLOW, stroke_width=7, tip_length=0.25)
                            for x in (-3.0, 0.0, 3.0)])
        e_lbl = T("added energy", 30, YELLOW).move_to([4.9, 2.0, 0])
        hb_lbl = T("hydrogen bonds", 32, TEAL).move_to([0, -0.9, 0])
        self.at("Part of the energy")
        self.play(FadeOut(A), run_time=0.4)
        self.play(FadeIn(row), Create(hbs), FadeIn(hb_lbl), run_time=0.6)
        self.play(GrowArrow(e_arrows[0]), GrowArrow(e_arrows[1]), GrowArrow(e_arrows[2]), FadeIn(e_lbl), run_time=0.6)
        self.at("stretching and breaking")
        self.play(row[0].animate.shift(LEFT * 0.7), row[2].animate.shift(RIGHT * 0.7),
                  hbs[0].animate.become(dashed([-2.7, 0.3, 0], [-0.9, 0.3, 0], TEAL, 7)),
                  hbs[1].animate.become(dashed([0.9, 0.3, 0], [2.7, 0.3, 0], TEAL, 7)), run_time=0.9)
        self.play(hbs[1].animate.set_opacity(0.15), run_time=0.5)
        less = T("less of it shows up as a rise in temperature", 32, TEXT).move_to([0, -2.1, 0])
        self.at("less of it shows")
        self.play(FadeIn(less, shift=UP * 0.15), run_time=0.6)
        B = VGroup(row, hbs, e_arrows, e_lbl, hb_lbl, less)

        # ---- C: same energy, two columns ----
        base_y, kk = -1.9, 0.45
        wx, sx = -3.0, 3.0
        base = Line([-6.0, base_y, 0], [6.0, base_y, 0], color=GREY, stroke_width=3)
        w_col = Rectangle(width=1.5, height=2 * kk, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
        w_col.move_to([wx, base_y + kk, 0])
        s_col = Rectangle(width=1.5, height=10 * kk, stroke_color=SAND, stroke_width=3, fill_color=SAND, fill_opacity=0.4)
        s_col.move_to([sx, base_y + 5 * kk, 0])
        w_name = label("100 g water", [wx, base_y - 0.4, 0], BLUE, 28)
        s_name = label("100 g dry sand", [sx, base_y - 0.4, 0], SAND, 28)
        e1 = chip("836.8 J in", YELLOW, 28).move_to([wx, base_y - 1.15, 0])
        e2 = chip("836.8 J in", YELLOW, 28).move_to([sx, base_y - 1.15, 0])
        w_up = M("warms by 2 °C", 28, BLUE).move_to([wx, base_y + 2 * kk + 0.55, 0])
        s_up = M("warms by about 10 °C", 28, SAND).move_to([sx, base_y + 10 * kk + 0.5, 0])
        self.at("that")
        self.play(FadeOut(B), run_time=0.4)
        self.play(Create(base), FadeIn(w_name), FadeIn(s_name), FadeIn(e1), run_time=0.6)
        self.at("warms by")
        self.play(GrowFromEdge(w_col, DOWN), run_time=0.7)
        self.play(FadeIn(w_up), run_time=0.3)
        self.at("would warm dry sand")
        self.play(FadeIn(e2), run_time=0.4)
        self.at("sand by about")
        self.play(GrowFromEdge(s_col, DOWN), run_time=1.0)
        self.play(FadeIn(s_up), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """One gram -> whole object -> the Bay; swings sketch; then the chain polar -> hydrogen bonds -> warms slowly."""

    def construct(self):
        gram = chip("1 gram: specific heat", BLUE, 28).move_to([-3.6, 0.0, 0])
        self.at("Heat capacity is")
        self.play(FadeIn(gram, scale=0.9), run_time=0.5)
        bay = Rectangle(width=6.4, height=4.6, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15)
        bay.move_to([-3.2, 0.2, 0])
        obj_lbl = T("whole object: heat capacity", 26, BLUE).move_to([-3.2, 2.0, 0])
        self.at("whole object")
        self.play(FadeOut(gram), GrowFromCenter(bay), FadeIn(obj_lbl), run_time=1.0)
        bay_lbl = T("the Bay", 34, BLUE, weight=BOLD).move_to([-3.2, 2.0, 0])
        self.at("big body of water")
        self.play(ReplacementTransform(obj_lbl, bay_lbl), run_time=0.5)
        big = chip("enormous heat capacity", BLUE, 28).move_to([-3.2, 0.9, 0])
        self.at("enormous heat capacity")
        self.play(FadeIn(big, scale=0.9), run_time=0.5)
        slow = T("changes temperature slowly", 28, TEXT).move_to([-3.2, 0.0, 0])
        self.at("changes temperature slowly")
        self.play(FadeIn(slow, shift=UP * 0.1), run_time=0.5)
        fish = chip("fish", GREY, 26)
        crabs = chip("crabs", GREY, 26)
        grass = chip("grasses", GREY, 26)
        life = VGroup(fish, crabs, grass).arrange(RIGHT, buff=0.3).move_to([-3.2, -1.3, 0])
        self.at("fish crabs and grasses")
        self.play(FadeIn(fish, shift=UP * 0.1), run_time=0.3)
        self.play(FadeIn(crabs, shift=UP * 0.1), run_time=0.3)
        self.play(FadeIn(grass, shift=UP * 0.1), run_time=0.3)
        # schematic: swings
        base_y, k = -2.6, 0.5
        base = Line([1.4, base_y, 0], [6.2, base_y, 0], color=GREY, stroke_width=3)
        air, wat = bar_chart(2.6, 5.0, base_y, k, air_h=7.0, water_h=2.0)
        air.set_stroke(LAND).set_fill(LAND, 0.4)
        air_l = label("air above them", [2.6, base_y - 0.4, 0], LAND, 24)
        wat_l = label("Bay water", [5.0, base_y - 0.4, 0], BLUE, 24)
        cap = T("daily swing, usually", 24, GREY).move_to([3.8, 1.5, 0])
        cap2 = T("schematic, not to scale", 22, GREY).move_to([3.8, 2.0, 0])
        self.at("gentler daily swings")
        self.play(Create(base), FadeIn(air_l), FadeIn(wat_l), FadeIn(cap), FadeIn(cap2), run_time=0.5)
        self.play(GrowFromEdge(wat, DOWN), GrowFromEdge(air, DOWN), run_time=0.9)
        # chain
        everything = VGroup(bay, bay_lbl, big, slow, life, base, air, wat, air_l, wat_l, cap, cap2)
        c1 = chip("water is polar", PURPLE, 26)
        c2 = chip("hydrogen bonds", TEAL, 26)
        c3 = chip("helps explain slow warming", BLUE, 26)
        chain = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.9).move_to([0, 0.3, 0])
        fit(chain, max_w=12.2)
        a1 = arr_between(c1, c2)
        a2 = arr_between(c2, c3)
        self.at("Water is polar")
        self.play(FadeOut(everything), run_time=0.5)
        self.play(FadeIn(c1, scale=0.9), run_time=0.5)
        self.at("Hydrogen bonds hold")
        self.play(GrowArrow(a1), FadeIn(c2, shift=RIGHT * 0.2), run_time=0.6)
        self.at("warms slowly")
        self.play(GrowArrow(a2), FadeIn(c3, shift=RIGHT * 0.2), run_time=0.6)
        self.finish()


def arr_between(a, b):
    return Arrow(a.get_right() + RIGHT * 0.05, b.get_left() + LEFT * 0.05, buff=0.05, color=GREY, stroke_width=6,
                 tip_length=0.25, max_tip_length_to_length_ratio=0.5)


class S07End(EndCard):
    LINE = "Hydrogen bonds help explain why water warms slowly."
