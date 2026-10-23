"""Inherited or Acquired?  (Biochemistrypedia, grade 7 Life Science explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = genes, sex cells, inherited traits
  ORANGE = acquired traits (scar, dyed hair, muscles from exercise)
  YELLOW = the environment (soil, light, water, food, temperature) and the open question
  BLUE   = blue hydrangea flowers (and the blue zone of the soil pH bar)
  PINK   = pink hydrangea flowers (and the pink zone of the bar)
  PURPLE = aluminum taken up by the roots
  SOIL   = soil (brown)
  RED    = "does not reach the offspring"
  GREY   = outlines, neutral parts
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E58FB5"
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SOIL = "#9C7A52"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def flower(center, r=0.27, col=GREY, filled=False):
    """a hydrangea flower head: a round cluster of small florets (schematic)."""
    g = VGroup(Circle(radius=r).move_to(center))
    for k in range(6):
        a = k * 60 * DEGREES
        g.add(Circle(radius=r).move_to(np.array(center) + 1.8 * r * np.array([np.cos(a), np.sin(a), 0])))
    g.set_stroke(col, 3).set_fill(col, 0.55 if filled else 0.0)
    return g


def recolor(g, col):
    return g.animate.set_stroke(col, 3).set_fill(col, 0.6)


def soil_box(center, w=3.4, h=0.9, label=None, size=26):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=SOIL, stroke_width=4,
                         fill_color=SOIL, fill_opacity=0.35).move_to(center)
    if label is None:
        return VGroup(r)
    return VGroup(r, T(label, size, TEXT).move_to(r))


class S00Title(TitleCard):
    LESSON = "Inherited or acquired?"
    TITLE = "Genes Pass On, Scars Do Not"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        bush = Ellipse(width=3.0, height=1.1, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([0, 2.85, 0])
        bl = T("one hydrangea bush", 30, TEXT).next_to(bush, RIGHT, buff=0.35)
        self.at("Take two cuttings")
        self.play(FadeIn(bush, scale=0.9), FadeIn(bl), run_time=0.6)
        cut = [Line([x, 1.95, 0], [x, 1.15, 0], color=GREY, stroke_width=7) for x in (-0.45, 0.45)]
        self.play(*[Create(c) for c in cut], run_time=0.6)
        self.at("Plant them")
        gl = soil_box([-3.8, -1.15, 0], w=4.0, h=1.0, label="garden 1", size=30)
        gr = soil_box([3.8, -1.15, 0], w=4.0, h=1.0, label="garden 2", size=30)
        tgt = [[-3.8, -0.25, 0], [3.8, -0.25, 0]]
        self.play(*[c.animate.move_to(t) for c, t in zip(cut, tgt)], FadeIn(gl), FadeIn(gr), run_time=1.3)
        cl = T("cutting", 26, GREY).move_to([-5.05, -0.15, 0])
        cr = T("cutting", 26, GREY).move_to([5.05, -0.15, 0])
        self.play(FadeIn(cl), FadeIn(cr), run_time=0.3)
        self.at("When they bloom")
        fl = flower([-3.8, 1.0, 0], r=0.34)
        fr = flower([3.8, 1.0, 0], r=0.34)
        self.play(GrowFromPoint(fl, [-3.8, 0.15, 0]), GrowFromPoint(fr, [3.8, 0.15, 0]), run_time=0.8)
        self.at("one can be blue")
        self.play(recolor(fl, BLUE), run_time=0.5)
        bt = T("blue", 32, BLUE, weight=BOLD).move_to([-3.8, -2.05, 0])
        self.play(FadeIn(bt), run_time=0.3)
        self.at("the other pink")
        self.play(recolor(fr, PINK), run_time=0.5)
        pt = T("pink", 32, PINK, weight=BOLD).move_to([3.8, -2.05, 0])
        self.play(FadeIn(pt), run_time=0.3)
        self.at("same genes")
        gc = chip("same genes", GREEN, 32).move_to([0, 1.0, 0])
        l1 = Line([-2.8, 1.0, 0], [gc.get_left()[0] - 0.05, 1.0, 0], color=GREEN, stroke_width=3)
        l2 = Line([2.8, 1.0, 0], [gc.get_right()[0] + 0.05, 1.0, 0], color=GREEN, stroke_width=3)
        self.play(FadeIn(gc, scale=0.9), Create(l1), Create(l2), run_time=0.7)
        self.at("where does the difference")
        q = T("?", 110, YELLOW, weight=BOLD).move_to([0, -0.5, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.at("Are all my traits")
        eq = T("Are all my traits from my genes,\nor do some come from how I live?", 30, TEXT, weight=BOLD, line_spacing=0.9).move_to([0, -3.0, 0])
        self.play(FadeIn(eq, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02TwoKinds(SpokenScene):
    def construct(self):
        div = DashedLine([0, 3.4, 0], [0, -3.4, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        self.add(div)
        hl = T("inherited trait", 42, GREEN, weight=BOLD).move_to([-3.2, 3.0, 0])
        self.at("Some traits are inherited")
        self.play(FadeIn(hl, shift=DOWN * 0.1), run_time=0.5)
        self.at("passed from parents")
        pa = chip("parents", GREY, 34).move_to([-5.0, 1.1, 0])
        of = chip("offspring", GREY, 34).move_to([-1.75, 1.1, 0])
        ar = arr([pa.get_right()[0] + 0.1, 1.1, 0], [of.get_left()[0] - 0.1, 1.1, 0], GREEN, w=7)
        self.play(FadeIn(pa), FadeIn(of), GrowArrow(ar), run_time=0.8)
        self.at("through genes")
        gc = chip("genes", GREEN, 32).move_to([(pa.get_right()[0] + of.get_left()[0]) / 2, 2.05, 0])
        self.play(FadeIn(gc, shift=DOWN * 0.1), run_time=0.4)
        dot = Dot(pa.get_right() + RIGHT * 0.2, radius=0.14, color=GREEN)
        self.play(FadeIn(dot), run_time=0.15)
        self.play(dot.animate.move_to(of.get_left() + LEFT * 0.2), run_time=0.6)
        self.play(FadeOut(dot), run_time=0.15)
        self.at("Eye color")
        ec = chip("eye color", GREEN, 36).move_to([-3.2, -1.0, 0])
        self.play(FadeIn(ec, shift=UP * 0.1), run_time=0.5)
        self.play(Indicate(VGroup(*ec[1:]), color=GREEN, scale_factor=1.1), run_time=0.5)
        hr = T("acquired trait", 42, ORANGE, weight=BOLD).move_to([3.3, 3.0, 0])
        self.at("Other traits are acquired")
        self.play(FadeIn(hr, shift=DOWN * 0.1), run_time=0.5)
        self.at("gets during its life")
        lt = chip("a living thing", GREY, 34).move_to([3.3, 1.45, 0])
        ar2 = arr([3.3, 0.8, 0], [3.3, -0.1, 0], ORANGE, w=7)
        dl = T("during its life", 28, ORANGE).move_to([4.7, 0.35, 0], aligned_edge=LEFT)
        dl.move_to([3.65 + dl.width / 2, 0.35, 0])
        self.play(FadeIn(lt), GrowArrow(ar2), FadeIn(dl), run_time=0.8)
        self.at("A scar")
        c1 = chip("scar", ORANGE, 32).move_to([3.3, -0.75, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("dyed hair")
        c2 = chip("dyed hair", ORANGE, 32).move_to([3.3, -1.75, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at("muscles built by exercise")
        c3 = chip("muscles built by exercise", ORANGE, 32).move_to([3.3, -2.75, 0])
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Why(SpokenScene):
    def construct(self):
        body = RoundedRectangle(corner_radius=0.35, width=7.4, height=5.8, stroke_color=GREY, stroke_width=5,
                                fill_color=GREY, fill_opacity=0.08).move_to([-2.6, 0.1, 0])
        bl = T("parent", 30, GREY).move_to([-5.55, 2.55, 0])
        self.at("Why can't a scar")
        self.play(FadeIn(body, scale=0.95), FadeIn(bl), run_time=0.7)
        self.at("A new animal grows")
        circ = Circle(radius=1.2, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.14).move_to([-1.0, 0.7, 0])
        sl = T("sex cells", 32, GREEN, weight=BOLD).move_to([-1.0, -0.9, 0])
        off = RoundedRectangle(corner_radius=0.2, width=2.9, height=2.4, stroke_color=GREY, stroke_width=5,
                               fill_color=GREY, fill_opacity=0.08).move_to([4.8, 0.7, 0])
        ol = T("offspring", 32, GREY).move_to(off)
        self.play(FadeIn(circ, scale=0.8), FadeIn(sl), run_time=0.5)
        self.play(FadeIn(off), FadeIn(ol), run_time=0.4)
        self.at("carry the parent's genes")
        gc = chip("genes", GREEN, 30).move_to(circ)
        ar = arr([0.35, 0.7, 0], [3.25, 0.7, 0], GREEN, w=7)
        al = T("genes", 28, GREEN).move_to([2.3, 1.2, 0])
        self.play(FadeIn(gc, scale=0.8), run_time=0.4)
        self.play(GrowArrow(ar), FadeIn(al), run_time=0.5)
        skin = VGroup(*[Square(side_length=0.6, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.12)
                        .move_to([-5.6 + 0.66 * i, 1.45 - 0.66 * j, 0]) for i in range(3) for j in range(2)])
        skl = T("skin cells", 28, ORANGE).next_to(skin, DOWN, buff=0.2)
        self.at("A scar changes skin cells")
        self.play(FadeIn(skin), FadeIn(skl), run_time=0.5)
        scar = Line(skin[1].get_corner(UL) + LEFT * 0.1 + UP * 0.12, skin[4].get_corner(DR) + RIGHT * 0.1 + DOWN * 0.12,
                    color=ORANGE, stroke_width=8)
        sct = T("scar", 28, ORANGE, weight=BOLD).move_to([-3.1, 1.15, 0])
        self.play(Create(scar), FadeIn(sct), skin.animate.set_fill(ORANGE, 0.4), run_time=0.6)
        mus = VGroup(*[RoundedRectangle(corner_radius=0.12, width=2.0, height=0.38, stroke_color=ORANGE, stroke_width=3,
                                        fill_color=ORANGE, fill_opacity=0.12).move_to([-4.8, -0.65 - 0.48 * j, 0]) for j in range(3)])
        mul = T("muscle cells", 28, ORANGE).next_to(mus, DOWN, buff=0.2)
        self.at("Lifting weights changes muscle cells")
        self.play(FadeIn(mus), FadeIn(mul), run_time=0.5)
        self.play(mus.animate.set_fill(ORANGE, 0.4), run_time=0.4)
        self.at("Neither changes the genes")
        un = T("genes not changed", 26, GREEN).move_to([-1.0, -1.65, 0])
        self.play(Indicate(gc, color=GREEN, scale_factor=1.15), FadeIn(un), run_time=0.8)
        self.at("So neither reaches")
        cs = chip("scar", ORANGE, 30).move_to([4.8, 2.65, 0])
        cm = chip("muscles", ORANGE, 30).move_to([4.8, -1.55, 0])
        self.play(FadeIn(cs), FadeIn(cm), run_time=0.4)
        xs = Cross(Square(side_length=0.42), stroke_color=RED, stroke_width=7).move_to([cs.get_left()[0] - 0.4, cs.get_center()[1], 0])
        xm = Cross(Square(side_length=0.42), stroke_color=RED, stroke_width=7).move_to([cm.get_left()[0] - 0.4, cm.get_center()[1], 0])
        self.play(Create(xs), Create(xm), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Environment(SpokenScene):
    def construct(self):
        lt2 = RoundedRectangle(corner_radius=0.2, width=4.2, height=2.2, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.1).move_to([0, 0.35, 0])
        ltl = T("a living thing", 28, GREY).move_to([0, 1.1, 0])
        gn = chip("genes", GREEN, 34).move_to([0, 0.05, 0])
        self.at("Genes are not")
        self.play(FadeIn(lt2), FadeIn(ltl), FadeIn(gn), run_time=0.7)
        self.at("The environment")
        env = DashedVMobject(RoundedRectangle(corner_radius=0.4, width=12.4, height=6.4, stroke_color=YELLOW, stroke_width=4), num_dashes=90)
        env.move_to([0, 0.0, 0])
        el = T("environment", 34, YELLOW, weight=BOLD).move_to([-4.2, 2.65, 0])
        self.play(Create(env), FadeIn(el), run_time=1.0)
        specs = [("soil", [-4.8, 0.35, 0]), ("light", [0, 2.45, 0]), ("water", [4.8, 0.35, 0]),
                 ("food", [-3.5, -2.05, 0]), ("temperature", [3.5, -2.05, 0])]
        chips, arrows = [], []
        for name, pos in specs:
            c = chip(name, YELLOW, 34).move_to(pos)
            if name == "light":
                a = arr([0, pos[1] - c.height / 2 - 0.05, 0], [0, 1.55, 0], YELLOW, w=5)
            elif name == "soil":
                a = arr([pos[0] + c.width / 2 + 0.08, 0.35, 0], [-2.2, 0.35, 0], YELLOW, w=5)
            elif name == "water":
                a = arr([pos[0] - c.width / 2 - 0.08, 0.35, 0], [2.2, 0.35, 0], YELLOW, w=5)
            elif name == "food":
                a = arr([-2.7, -1.6, 0], [-1.6, -0.8, 0], YELLOW, w=5)
            else:
                a = arr([2.7, -1.6, 0], [1.6, -0.8, 0], YELLOW, w=5)
            arrows.append(a); chips.append(c)
        for (name, pos), c, a in zip(specs, chips, arrows):
            self.at(name if name != "soil" else "Soil")
            self.play(FadeIn(c, scale=0.9), GrowArrow(a), run_time=0.45)
        self.at("Many traits depend")
        self.play(*[FadeOut(m) for m in [env, el, *chips, *arrows]], run_time=0.5)
        grp = VGroup(lt2, ltl, gn)
        self.play(grp.animate.scale(0.9).move_to([0, 1.9, 0]), run_time=0.5)
        row_g = chip("genes", GREEN, 36)
        row_p = T("+", 40, TEXT)
        row_e = chip("environment", YELLOW, 36)
        row_a = T("=", 40, TEXT)
        row_t = chip("many traits", TEXT, 36)
        row = VGroup(row_g, row_p, row_e, row_a, row_t).arrange(RIGHT, buff=0.3).move_to([0, -1.5, 0])
        self.at("genes and the environment")
        self.play(FadeIn(VGroup(row_g, row_p, row_e), shift=UP * 0.1), run_time=0.6)
        self.at("together")
        self.play(FadeIn(row_a), FadeIn(row_t, scale=0.9), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Hydrangea(SpokenScene):
    def construct(self):
        tag = T("a color-changing bigleaf hydrangea", 28, GREY).move_to([0, 3.3, 0])
        soil = soil_box([-4.5, 1.6, 0], w=3.4, h=1.3, label=None)
        sl = T("acidic soil", 30, TEXT).move_to(soil)
        roots = chip("roots", GREY, 32).move_to([0.2, 1.6, 0])
        fl = flower([5.0, 1.6, 0], r=0.4)
        fll = T("flowers", 28, GREY).move_to([5.0, 0.3, 0])
        a1 = arr([-2.7, 1.6, 0], [roots.get_left()[0] - 0.08, 1.6, 0], PURPLE, w=6)
        a2 = arr([roots.get_right()[0] + 0.08, 1.6, 0], [3.75, 1.6, 0], GREY, w=6)
        self.at("Back to the hydrangea")
        self.play(FadeIn(tag), FadeIn(soil), FadeIn(sl), FadeIn(roots), FadeIn(fl), FadeIn(fll), run_time=0.8)
        self.at("acidic soil lets")
        al = chip("aluminum", PURPLE, 28)
        al.move_to([-4.5, 2.65, 0])
        self.play(FadeIn(al, shift=DOWN * 0.1), GrowArrow(a1), run_time=0.5)
        self.at("take up more aluminum")
        self.play(al.animate.move_to([-1.6, 2.65, 0]), run_time=0.6)
        self.play(al.animate.move_to([0.2, 2.65, 0]), run_time=0.5)
        self.at("The aluminum helps")
        self.play(GrowArrow(a2), run_time=0.4)
        self.at("make the flowers blue")
        self.play(recolor(fl, BLUE), run_time=0.5)
        self.at("In less acidic soil")
        self.play(FadeOut(al), a1.animate.set_color(GREY), run_time=0.4)
        self.at("the flowers are pink")
        sl2 = T("less acidic soil", 30, TEXT).move_to(soil)
        self.play(ReplacementTransform(sl, sl2), recolor(fl, PINK), a2.animate.set_color(GREY), run_time=0.5)

        def X(ph):
            return -5.0 + (ph - 5.0) * 5.0
        y = -1.2
        h = 0.7
        blue = Rectangle(width=X(5.5) - X(5.0), height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to([(X(5.0) + X(5.5)) / 2, y, 0])
        mid = Rectangle(width=X(5.9) - X(5.6), height=h, stroke_width=0).move_to([(X(5.6) + X(5.9)) / 2, y, 0])
        mid.set_fill(interpolate_color(ManimColor(BLUE), ManimColor(PINK), 0.5), 0.85)
        bands = VGroup()
        n = 10
        for k in range(n):
            x0 = X(6.0) + k * (X(6.5) - X(6.0)) / n
            bands.add(Rectangle(width=(X(6.5) - X(6.0)) / n, height=h, stroke_width=0, fill_color=PINK,
                                fill_opacity=0.4 + 0.45 * k / (n - 1)).move_to([x0 + (X(6.5) - X(6.0)) / n / 2, y, 0]))
        bands.add(Rectangle(width=X(7.0) - X(6.5), height=h, stroke_width=0, fill_color=PINK, fill_opacity=0.85).move_to([(X(6.5) + X(7.0)) / 2, y, 0]))
        axis = Line([X(5.0), y - h / 2 - 0.06, 0], [X(7.0), y - h / 2 - 0.06, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for ph in (5.0, 5.5, 6.0, 6.5):
            ticks.add(Line([X(ph), y - h / 2 - 0.06, 0], [X(ph), y - h / 2 - 0.2, 0], color=GREY, stroke_width=3))
            ticks.add(M(f"{ph:.1f}", 28, TEXT).move_to([X(ph), y - h / 2 - 0.55, 0]))
        axl = T("soil pH", 30, TEXT, weight=BOLD).move_to([X(7.0) - 0.2, y - h / 2 - 0.55, 0])
        cap = T("color-changing hydrangeas, Virginia extension guide", 22, GREY).move_to([0, -3.3, 0])
        self.at("Gardeners measure")
        self.play(FadeIn(axl), Create(axis), FadeIn(ticks), FadeIn(cap), run_time=0.8)
        self.at("A lower number")
        low = arr([X(5.5), -2.75, 0], [X(5.0), -2.75, 0], GREY, w=5)
        lowt = T("lower pH: more acidic soil", 28, TEXT)
        low.move_to([X(5.0) + 0.6, -2.75, 0])
        lowt.next_to(low, RIGHT, buff=0.2)
        self.play(GrowArrow(low), FadeIn(lowt), run_time=0.5)
        self.at("gives blue")
        bt = T("blue", 30, BLUE, weight=BOLD).move_to([blue.get_center()[0], y + 0.65, 0])
        self.play(FadeIn(blue, scale=[0.1, 1, 1]), FadeIn(bt), run_time=0.5)
        self.at("In between")
        mt = T("in between", 28, TEXT).move_to([mid.get_center()[0] + 0.1, y + 0.65, 0])
        self.play(FadeIn(mid, scale=[0.1, 1, 1]), FadeIn(mt), run_time=0.5)
        self.at("Above about")
        pt = T("pink", 30, PINK, weight=BOLD).move_to([X(6.75), y + 0.65, 0])
        self.play(FadeIn(bands), FadeIn(pt), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        no = T("Are all my traits from my genes?  No.", 40, TEXT, weight=BOLD).move_to([0, 3.1, 0])
        self.at("So, are all")
        self.play(FadeIn(no, shift=DOWN * 0.1), run_time=0.6)
        ya = 1.4
        g1 = chip("genes", GREEN, 34)
        pb = chip("blue", BLUE, 32)
        pp = chip("pink", PINK, 32)
        poss = VGroup(pb, pp).arrange(DOWN, buff=0.25)
        box = RoundedRectangle(corner_radius=0.2, width=poss.width + 0.6, height=poss.height + 0.5, stroke_color=GREEN, stroke_width=3).move_to(poss)
        pos_g = VGroup(box, poss)
        pos_g.move_to([-0.3, ya, 0])
        g1.move_to([-4.8, ya, 0])
        gar = arr([g1.get_right()[0] + 0.1, ya, 0], [box.get_left()[0] - 0.1, ya, 0], GREEN, w=6)
        self.at("from my genes")
        self.play(FadeIn(g1), run_time=0.5)
        self.at("No")
        self.play(GrowArrow(gar), FadeIn(pos_g), run_time=0.8)
        pl = T("colors the genes allow", 26, GREEN).move_to([-0.3, box.get_bottom()[1] - 0.3, 0])
        self.play(FadeIn(pl), run_time=0.3)
        self.at("the genes set which colors")
        self.play(Indicate(pos_g, color=GREEN, scale_factor=1.05), run_time=0.8)
        soil = chip("soil", YELLOW, 34).move_to([4.7, ya, 0])
        sar = arr([soil.get_left()[0] - 0.1, ya, 0], [box.get_right()[0] + 0.1, ya, 0], YELLOW, w=6)
        self.at("The soil helps decide")
        self.play(FadeIn(soil), GrowArrow(sar), run_time=0.6)
        self.at("one appears")
        self.play(Indicate(VGroup(*pb[:]), color=BLUE, scale_factor=1.1), run_time=0.6)
        self.play(Indicate(VGroup(*pp[:]), color=PINK, scale_factor=1.1), run_time=0.6)
        yb = -1.2
        hg = chip("many genes", GREEN, 32)
        hp = T("+", 38, TEXT)
        hf = chip("food and health", YELLOW, 32)
        ha = T("=", 38, TEXT)
        hh = chip("height", TEXT, 32)
        VGroup(hg, hp, hf, ha, hh).arrange(RIGHT, buff=0.3).move_to([0, yb, 0])
        self.at("Your height")
        self.play(FadeIn(VGroup(hg, hp, hf), shift=UP * 0.1), run_time=0.6)
        self.at("while you grow")
        self.play(FadeIn(ha), FadeIn(hh, scale=0.9), run_time=0.5)
        yc = -2.7
        cg = chip("coded in genes: can be inherited", GREEN, 28).move_to([-3.2, yc, 0])
        co = chip("scar, dyed hair, learned skill", ORANGE, 28).move_to([3.2, yc, 0])
        self.at("Traits coded in genes")
        self.play(FadeIn(cg, shift=UP * 0.1), run_time=0.5)
        self.at("A scar")
        self.play(FadeIn(co, shift=UP * 0.1), run_time=0.5)
        nt = T("not passed to offspring", 26, RED).move_to([3.2, yc - 0.65, 0])
        x = Cross(Square(side_length=0.36), stroke_color=RED, stroke_width=6).move_to([nt.get_left()[0] - 0.35, nt.get_center()[1], 0])
        self.at("cannot be passed")
        self.play(Create(x), FadeIn(nt), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Genes can be passed on. Scars and skills cannot."
