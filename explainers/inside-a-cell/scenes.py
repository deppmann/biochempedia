"""Inside a cell: the parts work as one team  (Biochemistrypedia, grade 7 Life Science explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = nucleus (and the instructions it holds)
  TEAL   = cell membrane / the cell outline
  CYTO   = cytoplasm (pale blue-grey fill and label)
  PURPLE = endoplasmic reticulum
  ORANGE = mitochondria (and cellular respiration)
  PINK   = vacuole
  SAND   = the fat drop in a white fat cell
  GREEN  = sugar (glucose) / food, and photosynthesis
  YELLOW = energy released
  TEXT   = proteins and fats (the product), plain labels
  RED    = trouble / stopped
  GOLD   = the word "metabolism"
  GREY   = neutral, not yet named parts
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"
SAND = "#E6D9A8"
CYTO = "#8FB0D0"
MEM = TEAL


# ---------------------------------------------------------------------------------------------
# shapes (all simple outlined schematics)
# ---------------------------------------------------------------------------------------------
def nucleus_shape(center, r=0.75, col=BLUE):
    return Circle(radius=r, stroke_color=col, stroke_width=5, fill_color=col, fill_opacity=0.28).move_to([*center, 0])


def er_shape(center, width=1.6, col=PURPLE, sw=6):
    g = VGroup()
    for i, dy in enumerate((-0.27, 0.0, 0.27)):
        h = width / 1.6
        f = ParametricFunction(lambda t, i=i, h=h: np.array([t, 0.1 * h * np.sin(5 / h * t + i * 1.3), 0]),
                               t_range=[-0.8 * h, 0.8 * h], stroke_color=col, stroke_width=sw)
        g.add(f.shift(UP * dy * h))
    return g.move_to([*center, 0])


def mito_shape(center, ang=0, w=0.95, h=0.42, col=ORANGE, sw=4):
    m = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=col, stroke_width=sw,
                         fill_color=col, fill_opacity=0.3)
    return m.rotate(ang * DEGREES).move_to([*center, 0])


def vacuole_shape(center, r=0.45, col=PINK):
    return Circle(radius=r, stroke_color=col, stroke_width=5, fill_color=col, fill_opacity=0.25).move_to([*center, 0])


def cell_body(w=5.8, h=5.0):
    return Ellipse(width=w, height=h, stroke_color=MEM, stroke_width=7, fill_color=CYTO, fill_opacity=0.14)


# generic animal cell: part positions on a 5.8 x 5.0 ellipse centred on the origin
POS = {"nucleus": (-0.9, 0.8), "er": (1.2, 0.9), "vacuole": (-1.7, -0.9), "m1": (1.1, -1.15), "m2": (-0.2, -1.55)}


def generic_parts(col_all=None):
    P = {}
    P["body"] = cell_body()
    P["nucleus"] = nucleus_shape(POS["nucleus"], col=col_all or BLUE)
    P["er"] = er_shape(POS["er"], col=col_all or PURPLE)
    P["vacuole"] = vacuole_shape(POS["vacuole"], col=col_all or PINK)
    P["mito"] = VGroup(mito_shape(POS["m1"], 20, col=col_all or ORANGE), mito_shape(POS["m2"], -12, col=col_all or ORANGE))
    return P


LABELS = {
    "nucleus": ("nucleus", "holds the\ninstructions", BLUE, "L", 1.9),
    "vacuole": ("vacuole", "stores water,\nfood and wastes", PINK, "L", -0.1),
    "membrane": ("cell membrane", "controls what\nenters and leaves", MEM, "L", -1.9),
    "er": ("endoplasmic\nreticulum", "makes and moves\nproteins and fats", PURPLE, "R", 1.8),
    "cyto": ("cytoplasm", "jelly-like fluid\nholds the parts", CYTO, "R", -0.05),
    "mito": ("mitochondria", "release energy\nfrom food", ORANGE, "R", -1.9),
}
TARGET = {"nucleus": (-0.9, 0.8, 0.75), "er": (1.2, 0.9, 0.6), "vacuole": (-1.7, -0.9, 0.45), "mito": (1.1, -1.15, 0.5),
          "cyto": (1.95, -0.1, 0.0), "membrane": (-2.38, -1.43, 0.0)}


def mklabel(key, x=3.45):
    name, sub, col, side, ly = LABELS[key]
    L = side == "L"
    n = T(name, 28, col, weight=BOLD)
    s = T(sub, 22, TEXT)
    g = VGroup(n, s).arrange(DOWN, aligned_edge=RIGHT if L else LEFT, buff=0.08)
    g.move_to([-x if L else x, ly, 0], aligned_edge=RIGHT if L else LEFT)
    tx, ty, r = TARGET[key]
    c = np.array([tx, ty, 0.0])
    start = np.array([g.get_right()[0] + 0.12 if L else g.get_left()[0] - 0.12, n.get_center()[1], 0.0])
    d = start - c
    end = c + d / np.linalg.norm(d) * r
    line = Line(start, end, color=col, stroke_width=2.5)
    dot = Dot(end, radius=0.07, color=col)
    out = VGroup(g, line, dot)
    out.txt = g
    return out


def build_heart(center, s=1.0):
    rect = RoundedRectangle(corner_radius=0.7, width=5.2, height=2.9, stroke_color=MEM, stroke_width=6,
                            fill_color=CYTO, fill_opacity=0.14)
    nuc = nucleus_shape((0, 0), r=0.42)
    caps = VGroup()
    rng = np.random.RandomState(4)
    for xi in (-1.9, -0.95, 0.0, 0.95, 1.9):
        for yi in (-0.8, 0.0, 0.8):
            if (xi == 0.0 and yi == 0.0) or (xi in (0.95, 1.9) and yi == 0.0):
                continue
            caps.add(mito_shape((xi, yi), rng.uniform(-28, 28), w=0.78, h=0.34, sw=3))
    er = er_shape((1.45, 0.0), width=1.3, sw=5)
    g = VGroup(rect, nuc, caps)
    g.rect, g.nuc, g.caps, g.er = rect, nuc, caps, er
    g.er_g = VGroup(er)
    full = VGroup(g, er)
    full.core = g
    full.rect, full.nuc, full.caps, full.er = rect, nuc, caps, er
    full.scale(s).move_to([*center, 0])
    return full


def build_fat(center, s=1.0):
    R = 1.7
    ring = Circle(radius=R, stroke_color=MEM, stroke_width=6, fill_color=CYTO, fill_opacity=0.14)
    drop = Circle(radius=1.28, stroke_color=SAND, stroke_width=4, fill_color=SAND, fill_opacity=0.4)
    def rimpt(a, d=1.50):
        return np.array([d * np.cos(a * DEGREES), d * np.sin(a * DEGREES)])
    nuc = nucleus_shape(rimpt(150), r=0.12)
    caps = VGroup(mito_shape(rimpt(35), 35 + 90, w=0.34, h=0.15, sw=2), mito_shape(rimpt(255), 255 + 90, w=0.34, h=0.15, sw=2))
    er = er_shape((0, 0), width=0.36, sw=3).rotate((320 + 90) * DEGREES).move_to([*rimpt(320, 1.43), 0])
    full = VGroup(ring, drop, nuc, caps, er)
    full.ring, full.drop, full.nuc, full.caps, full.er = ring, drop, nuc, caps, er
    full.scale(s).move_to([*center, 0])
    return full


def dimto(mob, o):
    """animations that scale the stroke and fill opacity of every part of mob by o (never fills a line)."""
    return [m.animate.set_stroke(opacity=m.get_stroke_opacity() * o).set_fill(opacity=m.get_fill_opacity() * o)
            for m in mob.family_members_with_points()]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S00Title(TitleCard):
    LESSON = "Inside a cell"
    TITLE = "Cell Parts Work as One Team"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        top = T("Your heart at rest: about 60 to 100 beats a minute", 30)
        top.move_to([0, 3.05, 0])
        heart = build_heart((-3.6, 0.35))
        heart.er.set_stroke(opacity=0)
        fat = build_fat((3.7, 0.35))
        fat.er.set_stroke(opacity=0)
        # the heart cell without mitochondria and the fat cell without its drop first
        caps_h = heart.caps
        caps_h.set_opacity(0)
        fat_drop_target = fat.drop.copy()
        fat.drop.scale(0.05)
        fat.drop.set_opacity(0)
        hl = T("heart muscle cell", 28).move_to([-3.6, -1.55, 0])
        fl = T("white fat cell", 28).move_to([3.7, -1.55, 0])
        self.at("At rest")
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.6)
        self.at("beats")
        self.play(FadeIn(VGroup(heart.rect, heart.nuc), scale=0.9), FadeIn(hl), run_time=0.6)
        self.play(heart.rect.animate.scale(1.05), rate_func=there_and_back, run_time=0.35)
        self.play(heart.rect.animate.scale(1.05), rate_func=there_and_back, run_time=0.35)
        self.at("tiny parts")
        for c in caps_h:
            c.set_opacity(1)
            c.set_fill(ORANGE, 0.3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in caps_h], lag_ratio=0.08), run_time=1.0)
        ml = T("mitochondria", 28, ORANGE, weight=BOLD).move_to([-3.6, 2.35, 0])
        top_row = [c for c in caps_h if c.get_center()[1] > heart.rect.get_center()[1] + 0.3]
        pick = min(top_row, key=lambda c: abs(c.get_center()[0] - ml.get_center()[0]))
        tgt = pick.get_top()
        ml.move_to([tgt[0], 2.35, 0])
        ln = Line(ml.get_bottom() + DOWN * 0.05, tgt + UP * 0.02, color=ORANGE, stroke_width=2.5)
        self.at("called")
        self.play(FadeIn(ml, shift=DOWN * 0.1), Create(ln), run_time=0.5)
        self.at("white fat cell")
        self.play(FadeIn(VGroup(fat.ring, fat.nuc, fat.caps), scale=0.9), FadeIn(fl), run_time=0.6)
        self.at("one big drop")
        fat.drop.set_opacity(1)
        fat.drop.set_stroke(SAND, 4).set_fill(SAND, 0.4)
        self.play(Transform(fat.drop, fat_drop_target), run_time=1.3)
        dl = T("fat drop", 26, BG, weight=BOLD).move_to(fat.drop.get_center())
        self.play(FadeIn(dl), run_time=0.4)
        q1 = T("What are the parts inside a cell?", 32).move_to([0, -2.55, 0])
        q2 = T("How do they work together to keep it alive?", 32, YELLOW).move_to([0, -3.15, 0])
        self.at("what are the parts")
        self.play(FadeOut(top), FadeIn(q1, shift=UP * 0.1), run_time=0.6)
        self.at("how do they work")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Organelles(SpokenScene):
    def construct(self):
        P = generic_parts(col_all=GREY)
        body = P["body"]
        self.at("Many cells")
        self.play(Create(body), run_time=0.9)
        self.play(LaggedStart(FadeIn(P["nucleus"], scale=0.6), FadeIn(P["er"], scale=0.6), FadeIn(P["vacuole"], scale=0.6),
                              FadeIn(P["mito"], scale=0.6), lag_ratio=0.35), run_time=2.0)
        chip_o = chip("organelles: small parts, special jobs", TEXT, size=26).move_to([0, 3.05, 0])
        self.at("small part")
        self.play(FadeIn(chip_o, shift=DOWN * 0.1), run_time=0.6)
        self.at("special job")
        self.play(*[Indicate(P[k], color=YELLOW, scale_factor=1.15) for k in ("nucleus", "er", "vacuole", "mito")], run_time=0.9)
        # nucleus
        lab_n = mklabel("nucleus")
        self.at("The nucleus holds")
        self.play(FadeOut(chip_o), P["nucleus"].animate.set_color(BLUE), FadeIn(lab_n), run_time=0.7)
        # membrane
        lab_m = mklabel("membrane")
        self.at("The cell membrane")
        self.play(body.animate.set_stroke(TEAL, 10), FadeIn(lab_m), run_time=0.6)
        self.play(body.animate.set_stroke(TEAL, 7), run_time=0.3)
        a_in = arr([-0.5, 3.35, 0], [-0.5, 2.0, 0], GREY, w=6)
        a_out = arr([0.5, 2.0, 0], [0.5, 3.35, 0], GREY, w=6)
        t_in = T("enters", 26, TEXT).next_to(a_in, LEFT, buff=0.2).set_y(3.0)
        t_out = T("leaves", 26, TEXT).next_to(a_out, RIGHT, buff=0.2).set_y(3.0)
        self.at("controls what enters")
        self.play(GrowArrow(a_in), FadeIn(t_in), run_time=0.5)
        self.at("leaves")
        self.play(GrowArrow(a_out), FadeIn(t_out), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03More(SpokenScene):
    def construct(self):
        P = generic_parts(col_all=GREY)
        P["nucleus"].set_color(BLUE)
        P["body"].set_stroke(TEAL, 7)
        lab_n, lab_m = mklabel("nucleus"), mklabel("membrane")
        self.add(P["body"], P["nucleus"], P["er"], P["vacuole"], P["mito"], lab_n, lab_m)
        lab_c = mklabel("cyto")
        self.at("The cytoplasm")
        self.play(P["body"].animate.set_fill(CYTO, 0.4), FadeIn(lab_c), run_time=0.7)
        self.at("holds the organelles")
        self.play(*[Indicate(P[k], color=YELLOW, scale_factor=1.12) for k in ("nucleus", "er", "vacuole", "mito")], run_time=0.9)
        self.play(P["body"].animate.set_fill(CYTO, 0.14), run_time=0.3)
        lab_e = mklabel("er")
        self.at("The endoplasmic")
        self.play(P["er"].animate.set_color(PURPLE), FadeIn(lab_e), run_time=0.7)
        self.at("folded membranes")
        self.play(P["er"].animate.stretch(1.25, 1), rate_func=there_and_back, run_time=0.8)
        # proteins and fats leave the ER
        chips = VGroup(*[Square(0.2, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to(P["er"].get_center() + RIGHT * 0.4 + UP * dy)
                         for dy in (0.15, -0.1, -0.35)])
        self.at("make and move")
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in chips], lag_ratio=0.3), run_time=0.7)
        self.play(LaggedStart(*[c.animate.shift(RIGHT * 0.65 + DOWN * 0.1) for c in chips], lag_ratio=0.3), run_time=0.9)
        self.play(FadeOut(chips), run_time=0.4)
        lab_v = mklabel("vacuole")
        self.at("is a sack")
        self.play(P["vacuole"].animate.set_color(PINK), FadeIn(lab_v), run_time=0.7)
        # water, food and wastes go into the vacuole
        dots = VGroup(*[Dot(radius=0.1, color=c).move_to(P["vacuole"].get_center() + np.array([-0.2 - 0.0, 0, 0]) + v)
                        for c, v in ((TEXT, np.array([-0.15, 0.95, 0])), (TEXT, np.array([-0.2, 0.75, 0])), (TEXT, np.array([0.25, 0.9, 0])))])
        words = (0, 1, 2)
        self.at("stores water")
        for i, (d, w) in enumerate(zip(dots, words)):
            d.move_to(P["vacuole"].get_center() + np.array([1.2 + 0.25 * (i % 2), 0.5 - 0.28 * i, 0]))
        self.play(FadeIn(dots), run_time=0.4)
        self.play(*[d.animate.move_to(P["vacuole"].get_center() + np.array([-0.2 + 0.2 * i, 0.12 - 0.12 * (i % 2), 0])) for i, d in enumerate(dots)], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Energy(SpokenScene):
    def construct(self):
        P = generic_parts()
        P["body"].set_stroke(TEAL, 7)
        grp = VGroup(P["body"], P["nucleus"], P["er"], P["vacuole"], P["mito"])
        self.add(grp)
        others = VGroup(P["body"], P["nucleus"], P["er"], P["vacuole"], P["mito"][0])
        m2 = P["mito"][1]
        mlabel = T("mitochondria", 28, ORANGE, weight=BOLD).move_to([-0.2, -3.05, 0])
        mline = Line(mlabel.get_top() + UP * 0.05, m2.get_bottom() + DOWN * 0.02, color=ORANGE, stroke_width=2.5)
        self.at("Mitochondria release")
        self.play(*dimto(others, 0.3), FadeIn(mlabel), Create(mline), Indicate(m2, color=YELLOW, scale_factor=1.3), run_time=0.9)
        sugar = chip("sugar\n(glucose)", GREEN, size=24).move_to([-5.3, -1.55, 0])
        a1 = arr([-4.2, -1.55, 0], [-0.85, -1.55, 0], GREEN, w=6)
        note = T("food", 24, GREEN).next_to(sugar, UP, buff=0.15)
        self.at("One kind of food")
        self.play(FadeIn(sugar, shift=RIGHT * 0.2), FadeIn(note), run_time=0.6)
        self.play(GrowArrow(a1), run_time=0.6)
        en = chip("energy the\ncell can use", YELLOW, size=24).move_to([5.0, -1.55, 0])
        a2 = arr([0.3, -1.55, 0], [3.6, -1.55, 0], YELLOW, w=6)
        self.at("release that energy")
        self.play(sugar.animate.move_to(m2.get_center()).scale(0.3).set_opacity(0), FadeOut(a1), FadeOut(note), run_time=1.0)
        self.play(Indicate(m2, color=YELLOW, scale_factor=1.3), run_time=0.6)
        self.at("a form the cell")
        self.play(GrowArrow(a2), FadeIn(en, shift=RIGHT * 1.2), run_time=1.2)
        # metabolism
        grp2 = VGroup(grp, mlabel, mline, sugar, a1, note, en, a2)
        met = T("metabolism", 56, GOLD, weight=BOLD, font=TITLE_FONT).move_to([0, 2.6, 0])
        defn = T("all the interactions among\nmolecules in the cell", 32).next_to(met, DOWN, buff=0.3)
        self.at("Metabolism means")
        self.play(FadeOut(grp2), FadeIn(met, shift=DOWN * 0.1), run_time=0.7)
        self.at("all the interactions")
        self.play(FadeIn(defn, shift=DOWN * 0.1), run_time=0.7)
        pc = chip("photosynthesis", GREEN, size=30).move_to([-3.5, -1.4, 0])
        rc = chip("cellular respiration", ORANGE, size=30).move_to([3.5, -1.4, 0])
        ap = arr([-1.8, 0.1, 0], [-3.3, -0.75, 0], GOLD, w=5)
        ar = arr([1.8, 0.1, 0], [3.3, -0.75, 0], GOLD, w=5)
        two = T("two examples", 28, GOLD).move_to([0, -2.9, 0])
        self.at("Photosynthesis")
        self.play(GrowArrow(ap), FadeIn(pc, shift=DOWN * 0.15), run_time=0.7)
        self.at("cellular respiration")
        self.play(GrowArrow(ar), FadeIn(rc, shift=DOWN * 0.15), run_time=0.7)
        self.at("two examples")
        self.play(FadeIn(two), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Team(SpokenScene):
    def construct(self):
        nuc = nucleus_shape((-4.4, 0.5), r=0.85)
        er = er_shape((0.0, 0.5), width=2.8, sw=7)
        mito = mito_shape((0.0, -2.1), 0, w=1.8, h=0.8, sw=5)
        nl = T("nucleus", 30, BLUE, weight=BOLD).next_to(nuc, UP, buff=0.4)
        el = T("endoplasmic reticulum", 30, PURPLE, weight=BOLD).next_to(er, UP, buff=0.55)
        ml = T("mitochondria", 30, ORANGE, weight=BOLD).next_to(mito, RIGHT, buff=0.35)
        box = DashedVMobject(RoundedRectangle(corner_radius=0.4, width=12.2, height=6.4, stroke_color=GREY, stroke_width=3).move_to([0, 0.2, 0]),
                             num_dashes=90)
        sysl = T("one system", 28, GREY).move_to([5.0, 3.15, 0])
        sysl_back = Rectangle(width=sysl.width + 0.3, height=0.4, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(sysl)
        self.at("The parts work")
        self.play(FadeIn(nuc, scale=0.7), FadeIn(er, scale=0.7), FadeIn(mito, scale=0.7), FadeIn(nl), FadeIn(el), FadeIn(ml), run_time=0.9)
        self.at("one system")
        self.play(Create(box), FadeIn(sysl_back), FadeIn(sysl), run_time=0.9)
        # instructions travel to the ER
        a_i = arr([-3.45, 0.5, 0], [-1.65, 0.5, 0], BLUE, w=6)
        ins = chip("instructions", BLUE, size=24).move_to([-2.5, -0.4, 0])
        self.at("Instructions from the nucleus")
        self.play(FadeIn(ins, shift=UP * 0.1), GrowArrow(a_i), run_time=0.7)
        self.play(ins.animate.move_to([-1.5, 0.5, 0]).scale(0.55).set_opacity(0), run_time=0.8)
        out = chip("proteins and fats", TEXT, size=24).move_to([4.2, 0.5, 0])
        a_o = arr([1.7, 0.5, 0], [2.7, 0.5, 0], TEXT, w=6)
        self.at("makes and moves")
        self.play(Indicate(er, color=YELLOW, scale_factor=1.1), GrowArrow(a_o), FadeIn(out, shift=RIGHT * 0.2), run_time=0.8)
        a_e = arr([0.0, -1.6, 0], [0.0, -0.4, 0], YELLOW, w=7)
        el_e = T("energy", 28, YELLOW).next_to(a_e, RIGHT, buff=0.2)
        self.at("release the energy")
        self.play(Indicate(mito, color=YELLOW, scale_factor=1.15), GrowArrow(a_e), FadeIn(el_e), run_time=0.8)
        gr = T("growth and repair", 26, TEXT).move_to([4.2, -0.4, 0])
        self.at("supports growth")
        self.play(FadeIn(gr, shift=UP * 0.1), run_time=0.6)
        # trouble in one part
        bad = T("trouble in one part", 28, RED).next_to(mito, LEFT, buff=0.4)
        self.at("trouble in one")
        self.play(mito.animate.set_color(RED), FadeOut(a_e), FadeOut(el_e), FadeIn(bad), run_time=0.7)
        slow = T("growth and repair\nslow down", 26, RED).move_to([4.2, -0.6, 0])
        self.at("slows many")
        self.play(Transform(gr, slow), *dimto(out, 0.4), *dimto(a_o, 0.4), *dimto(er, 0.45), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        heart = build_heart((-3.5, 1.0), 0.95)
        fat = build_fat((3.7, 1.0), 1.05)
        heart.er.set_stroke(opacity=0)
        fat.er.set_stroke(opacity=0)
        dl = T("fat drop", 28, BG, weight=BOLD).move_to(fat.drop.get_center())
        hl = T("heart muscle cell", 28).move_to([-3.5, -1.2, 0])
        fl = T("white fat cell", 28).move_to([3.7, -1.2, 0])
        self.at("Look again")
        self.play(FadeIn(heart), FadeIn(fat), FadeIn(dl), FadeIn(hl), FadeIn(fl), run_time=0.9)
        names = [("nucleus", BLUE), ("cell membrane", MEM), ("cytoplasm", CYTO), ("endoplasmic reticulum", PURPLE), ("mitochondria", ORANGE)]
        col = VGroup(*[chip(n, c, size=22, pad=0.18) for n, c in names]).arrange(RIGHT, buff=0.12).move_to([0, -2.3, 0])

        def flash(*mobs):
            return [Indicate(m, color=YELLOW, scale_factor=1.12) for m in mobs]

        self.at("a nucleus")
        self.play(FadeIn(col[0], shift=UP * 0.2), *flash(heart.nuc, fat.nuc), run_time=0.6)
        self.at("a cell membrane")
        self.play(FadeIn(col[1], shift=UP * 0.2), *flash(heart.rect, fat.ring), run_time=0.6)
        self.at("cytoplasm")
        self.play(FadeIn(col[2], shift=UP * 0.2), heart.rect.animate.set_fill(CYTO, 0.4), fat.ring.animate.set_fill(CYTO, 0.4), run_time=0.6)
        self.play(heart.rect.animate.set_fill(CYTO, 0.14), fat.ring.animate.set_fill(CYTO, 0.14), run_time=0.3)
        self.at("endoplasmic reticulum")
        self.play(FadeIn(col[3], shift=UP * 0.2), heart.er.animate.set_stroke(opacity=1), fat.er.animate.set_stroke(opacity=1), run_time=0.7)
        self.at("and mitochondria")
        self.play(FadeIn(col[4], shift=UP * 0.2), *flash(heart.caps, fat.caps), run_time=0.6)
        self.at("very different")
        self.play(FadeOut(col), run_time=0.5)
        # heart works without a break
        hw = T("works without a break", 28, TEXT).move_to([-3.5, -1.2, 0])
        self.at("works without a break")
        self.play(Transform(hl, hw), run_time=0.4)
        self.play(heart.core.animate.scale(1.05), rate_func=there_and_back, run_time=0.35)
        self.play(heart.core.animate.scale(1.05), rate_func=there_and_back, run_time=0.35)
        self.at("fill a large share")
        self.play(*flash(heart.caps), run_time=0.9)
        fs = T("stores fat", 28, TEXT).move_to([3.7, -1.2, 0])
        self.at("stores fat")
        self.play(Transform(fl, fs), run_time=0.4)
        self.at("One fat drop")
        self.play(Indicate(fat.drop, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("thin rim")
        rim = Annulus(inner_radius=1.4, outer_radius=1.78, stroke_width=0, fill_color=YELLOW, fill_opacity=0.22).move_to(fat.ring.get_center())
        self.play(FadeIn(rim), run_time=0.4)
        self.play(FadeOut(rim), run_time=0.4)
        q1 = T("Different jobs, different amounts of each part", 32).move_to([0, -2.4, 0])
        q2 = T("Together, the parts keep the cell alive", 32, YELLOW).move_to([0, -3.1, 0])
        self.at("different jobs")
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.6)
        self.at("keep the cell alive")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Cells with different jobs hold different amounts of each part."
