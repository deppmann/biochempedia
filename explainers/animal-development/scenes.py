"""Animal development: cleavage divides without growing  (Biochemistrypedia explainer)

All numbers are the lesson's worked problem (invented round values): 1.000 nL zygote, five
synchronous equal divisions, no growth, no cell loss, spherical cells.

COLOR MAP (one color per concept, whole video)
  BLUE   = cells / cytoplasm (zygote and blastomeres)
  GREEN  = volume (conserved)
  TEAL   = membrane (surface area)
  ORANGE = nuclei
  GOLD   = yolk
  YELLOW = the number or question being highlighted
  RED    = "no growth" (crossed out)
  GREY   = outlines, labels, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BW, BH = 7.4, 4.6   # the zygote block (schematic volume), width x height


def grid(nx, ny, cx=0.0, cy=0.0, w=BW, h=BH, gap=0.08, color=BLUE, op=0.28):
    cw, ch = w / nx, h / ny
    g = VGroup()
    for j in range(ny):
        for i in range(nx):
            x = cx - w / 2 + cw * (i + 0.5)
            y = cy + h / 2 - ch * (j + 0.5)
            r = RoundedRectangle(corner_radius=min(0.12, cw / 4, ch / 4), width=cw - gap, height=ch - gap,
                                 stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=op).move_to([x, y, 0])
            g.add(r)
    return g


def dashed_outline(cx=0.0, cy=0.0, w=BW, h=BH, color=GREY):
    r = Rectangle(width=w + 0.2, height=h + 0.2, stroke_color=color, stroke_width=2.5).move_to([cx, cy, 0])
    return DashedVMobject(r, num_dashes=60)


def cross(mob, color=RED):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=6),
                  Line(mob.get_corner(DL), mob.get_corner(UR), color=color, stroke_width=6))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dbar(x0, x1, y, color=YELLOW):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                  Line([x0, y - 0.15, 0], [x0, y + 0.15, 0], color=color, stroke_width=4),
                  Line([x1, y - 0.15, 0], [x1, y + 0.15, 0], color=color, stroke_width=4))


SEQ = [(1, 1), (2, 1), (2, 2), (4, 2), (4, 4), (8, 4)]


class S00Title(TitleCard):
    LESSON = "Animal development"
    TITLE = "Cleavage divides without growing"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        cy = 0.0
        outline = dashed_outline(0, cy)
        g = grid(1, 1, 0, cy)
        zl = T("one zygote", 28, BLUE).move_to([0, 3.0, 0])
        self.at("One fertilized egg")
        self.play(FadeIn(g, scale=0.9), FadeIn(outline), FadeIn(zl), run_time=0.8)
        self.at("divides again")
        for nx, ny in SEQ[1:4]:
            ng = grid(nx, ny, 0, cy)
            self.play(ReplacementTransform(g, ng), run_time=0.6)
            g = ng
            self.wait(0.15)
        note = T("same outline: same total size", 24, GREY).move_to([0, -3.1, 0])
        self.at("do not grow")
        gc = chip("growth between divisions", RED, 26).move_to([0, 3.0, 0])
        gx = cross(gc)
        self.play(ReplacementTransform(zl, gc), FadeIn(note), run_time=0.6)
        self.play(Create(gx), run_time=0.5)
        self.at("where does the material")
        qs = VGroup(*[T("?", 40, YELLOW, weight=BOLD).move_to(c.get_center()) for c in g])
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.08), run_time=1.0)
        self.at("the egg itself")
        self.play(FadeOut(qs), g.animate.set_stroke(GREEN).set_fill(GREEN, 0.28), outline.animate.set_color(GREEN),
                  run_time=0.8)
        self.at("Cleavage is")
        lab = T("cleavage", 34, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(FadeOut(gc), FadeOut(gx), FadeIn(lab), g.animate.set_stroke(BLUE).set_fill(BLUE, 0.28),
                  outline.animate.set_color(GREY), run_time=0.7)
        self.at("each small cell")
        pick = g[0]
        bl = chip("a blastomere", BLUE, 26).move_to([-5.4, 3.0, 0])
        ar = arr(bl.get_right(), pick.get_corner(UL) + LEFT * 0.02 + UP * 0.02, BLUE, w=4)
        self.play(FadeOut(note), FadeIn(bl), GrowArrow(ar), Indicate(pick, color=YELLOW, scale_factor=1.12),
                  run_time=0.8)
        self.at("What does that do")
        q1 = chip("cell size?", BLUE, 28).move_to([-2.5, -3.1, 0])
        q2 = chip("membrane?", TEAL, 28).move_to([2.5, -3.1, 0])
        self.play(FadeIn(q1, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(q2, shift=UP * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Count(SpokenScene):
    def construct(self):
        cy = 0.0
        outline = dashed_outline(0, cy)
        g = grid(1, 1, 0, cy)
        lab_t = T("worked example: invented round numbers", 26, GREY).move_to([0, -3.1, 0])
        self.at("Here is a worked example")
        self.play(FadeIn(g, scale=0.9), FadeIn(outline), FadeIn(lab_t), run_time=0.8)
        self.at("block of volume")
        vol = M("1.000 nL", 40, GREEN).move_to(g.get_center())
        zyg = T("zygote", 26, BLUE).move_to([0, 3.1, 0])
        self.play(Write(vol), FadeIn(zyg), g.animate.set_stroke(GREEN).set_fill(GREEN, 0.2), run_time=0.8)
        count = M("cells: 1", 34, YELLOW).move_to([-4.4, 3.1, 0])
        self.at("Each division doubles")
        dbl = M("x 2", 40, YELLOW).move_to([4.6, 3.1, 0])
        ng = grid(2, 1, 0, cy)
        c2 = M("cells: 2", 34, YELLOW).move_to(count)
        self.play(FadeOut(vol), FadeOut(zyg), FadeOut(lab_t), ReplacementTransform(g, ng),
                  FadeIn(dbl, scale=0.8), FadeIn(count), run_time=0.9)
        g = ng
        self.play(Transform(count, c2), run_time=0.3)
        self.at("five synchronous")
        span = self.t_of("with no growth") - self.t_of("five synchronous")
        step = max(0.3, min(1.4, span / 4 - 0.35))
        for k, (nx, ny) in enumerate(SEQ[2:], start=2):
            ng = grid(nx, ny, 0, cy)
            nc = M(f"cells: {2 ** (k)}", 34, YELLOW).move_to(count)
            self.play(ReplacementTransform(g, ng), Transform(count, nc), run_time=step)
            g = ng
            self.wait(0.2)
        note = T("no growth, no cell loss", 26, RED).move_to([0, -3.1, 0])
        self.at("with no growth")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.4)
        self.at("to the fifth power")
        eq = M("2^5 = 32", 44, YELLOW).move_to([0, 3.1, 0])
        self.play(FadeOut(dbl), Write(eq), run_time=0.7)
        self.at("blastomeres")
        self.play(Indicate(g, color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Volume(SpokenScene):
    def construct(self):
        cx0, cy = 0.0, 0.0
        g = grid(8, 4, cx0, cy)
        outline = dashed_outline(cx0, cy)
        eq0 = M("2^5 = 32", 44, YELLOW).move_to([0, 3.1, 0])
        self.add(g, outline, eq0)
        self.at("Volume is shared")
        tot = M("1.000 nL in all", 36, GREEN).move_to([0, 3.1, 0])
        self.play(ReplacementTransform(eq0, tot), g.animate.set_stroke(GREEN).set_fill(GREEN, 0.2),
                  outline.animate.set_color(GREEN), run_time=0.7)
        self.at("shared among")
        self.play(LaggedStart(*[Indicate(c, color=YELLOW, scale_factor=1.15) for c in g], lag_ratio=0.03), run_time=1.4)
        self.at("for each cell")
        shift = LEFT * 2.4
        self.play(g.animate.shift(shift), outline.animate.shift(shift), tot.animate.shift(shift), run_time=0.7)
        pick = g[11].copy()
        big = RoundedRectangle(corner_radius=0.2, width=2.2, height=2.7, stroke_color=GREEN, stroke_width=4,
                               fill_color=GREEN, fill_opacity=0.3).move_to([5.0, 0.2, 0])
        lbl = M("31.25 pL", 34, GREEN).next_to(big, DOWN, buff=0.3)
        one = T("one blastomere", 26, BLUE).next_to(big, UP, buff=0.25)
        self.play(ReplacementTransform(pick, big), FadeIn(lbl, shift=UP * 0.1), FadeIn(one), run_time=0.9)
        self.at("of that size")
        times = VGroup(T("32 cells,", 24, YELLOW), T("each 31.25 pL", 24, YELLOW)).arrange(DOWN, buff=0.1).move_to([2.7, 0.2, 0])
        self.play(FadeIn(times, scale=0.8), run_time=0.5)
        eq = M("32 x 0.03125 nL = 1.000 nL", 28, GREEN).move_to([-2.4, -3.1, 0])
        self.play(Write(eq), run_time=1.0)
        self.at("Dividing made many cells")
        self.play(Indicate(g, color=YELLOW, scale_factor=1.03), Indicate(eq, color=YELLOW), FadeOut(times), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Size(SpokenScene):
    def construct(self):
        k = 0.034
        D1, D2 = 124 * k, 39 * k
        c1 = Circle(radius=D1 / 2, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to([-3.6, 0.6, 0])
        c2 = Circle(radius=D2 / 2, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to([3.8, 0.6, 0])
        t1 = T("zygote", 28, BLUE).move_to([-3.6, 3.3, 0])
        t2 = T("one blastomere of 32", 28, BLUE).move_to([3.8, 3.3, 0])
        g = grid(8, 4, 0, 0)
        self.add(g)
        self.at("as spheres")
        self.play(FadeOut(g), FadeIn(c1, scale=0.8), FadeIn(c2, scale=0.8), FadeIn(t1), FadeIn(t2), run_time=1.0)
        note = T("idealised spheres, drawn to scale", 24, GREY).move_to([0, -3.45, 0])
        self.play(FadeIn(note), run_time=0.3)
        self.at("diameter follows")
        f = M("d = 2 x (3V / 4pi)^(1/3)", 30, YELLOW).move_to([0, -2.95, 0])
        self.play(Write(f), run_time=1.1)
        self.at("is about")
        b1 = dbar(-3.6 - D1 / 2, -3.6 + D1 / 2, 0.6 - D1 / 2 - 0.35)
        l1 = M("124 um", 32, YELLOW).next_to(b1, DOWN, buff=0.15)
        l1.move_to([-3.6, l1.get_center()[1], 0])
        self.play(Create(b1), FadeIn(l1), run_time=0.8)
        self.at("Each")
        b2 = dbar(3.8 - D2 / 2, 3.8 + D2 / 2, 0.6 - D2 / 2 - 0.35)
        l2 = M("39 um", 32, YELLOW).next_to(b2, DOWN, buff=0.15)
        self.play(Create(b2), FadeIn(l2), run_time=0.8)
        self.at("That is smaller")
        r = VGroup(M("124 / 39", 32, YELLOW), M("= 32^(1/3)", 32, YELLOW), M("= 3.17", 40, YELLOW)).arrange(DOWN, buff=0.25).move_to([0.1, 0.6, 0])
        self.play(FadeOut(f), FadeOut(note), FadeIn(r, shift=DOWN * 0.1), run_time=0.8)
        self.at("which is")
        self.play(Indicate(r, color=GREEN), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Membrane(SpokenScene):
    def construct(self):
        base_y = -2.6
        OFF = 3.6
        x1, x2 = -5.0 + OFF, -2.6 + OFF
        h1 = 1.1
        h2 = h1 * 3.17
        ax = Line([-6.2 + OFF, base_y, 0], [-1.4 + OFF, base_y, 0], color=GREY, stroke_width=3)
        cap = T("membrane area", 28, TEAL).move_to([-3.8 + OFF, 3.1, 0])
        self.at("Smaller cells")
        b1 = Rectangle(width=1.8, height=h1, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4)
        b1.move_to([x1, base_y + h1 / 2, 0])
        n1 = T("zygote", 24, BLUE).next_to(ax, DOWN, buff=0.15).set_x(x1)
        v1 = M("48,400 um2", 24, TEAL).next_to(b1, UP, buff=0.12)
        self.play(Create(ax), FadeIn(cap), FadeIn(b1), FadeIn(n1), FadeIn(v1), run_time=0.9)
        self.at("Added up")
        b2 = Rectangle(width=1.8, height=h2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4)
        b2.move_to([x2, base_y + h2 / 2, 0])
        n2 = T("32 cells", 24, BLUE).next_to(ax, DOWN, buff=0.15).set_x(x2)
        v2 = M("153,500 um2", 24, TEAL).next_to(b2, UP, buff=0.12)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(n2), run_time=1.0)
        self.play(FadeIn(v2), run_time=0.3)
        self.at("times the membrane")
        mult = M("x 3.17", 44, YELLOW).move_to([-5.0 + OFF, 0.3, 0])
        self.play(FadeIn(mult, scale=0.8), run_time=0.6)
        pcx, pcy = 3.5, 0.0
        blk = RoundedRectangle(corner_radius=0.15, width=5.4, height=3.6, stroke_color=GREEN, stroke_width=3,
                               fill_color=BLUE, fill_opacity=0.18).move_to([pcx, pcy, 0])
        self.at("no new cytoplasm")
        left = VGroup(ax, cap, b1, n1, v1, b2, n2, v2, mult)
        cl = T("same cytoplasm, 1.000 nL", 26, GREEN).next_to(blk, UP, buff=0.25)
        self.play(left.animate.shift(LEFT * OFF), FadeIn(blk), FadeIn(cl), run_time=0.9)
        self.at("number of nuclei")
        n_dot = Dot(radius=0.2, color=ORANGE).move_to(blk.get_center())
        nl = T("nuclei: 1", 28, ORANGE).next_to(blk, DOWN, buff=0.25)
        self.play(FadeIn(n_dot, scale=0.5), FadeIn(nl), run_time=0.6)
        dots = VGroup()
        for j in range(4):
            for i in range(8):
                dots.add(Dot(radius=0.13, color=ORANGE).move_to([pcx - 2.2 + i * (4.4 / 7), pcy + 1.2 - j * (2.4 / 3), 0]))
        nl2 = T("nuclei: 32", 28, ORANGE).move_to(nl)
        self.play(ReplacementTransform(n_dot, dots), Transform(nl, nl2), run_time=1.1)
        self.at("same cytoplasm")
        self.play(Indicate(blk, color=GREEN, scale_factor=1.03), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        def circ(x, y, r=0.7, color=BLUE):
            return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.28).move_to([x, y, 0])
        ax_, bx_, cx_ = -4.3, 0.0, 4.3
        A = VGroup(*[circ(ax_ + dx, 0.7 + dy) for dx in (-0.75, 0.75) for dy in (-0.75, 0.75)])
        At = T("equal, synchronous", 26, BLUE).move_to([ax_, 3.0, 0])
        Al = M("1, 2, 4, 8, ...", 28, YELLOW).move_to([ax_, -2.0, 0])
        self.at("These numbers assume")
        self.play(FadeIn(A, scale=0.8), FadeIn(At), run_time=0.7)
        self.play(FadeIn(Al), run_time=0.4)
        B = VGroup(circ(bx_ - 0.75, -0.0), circ(bx_ + 0.75, -0.0), circ(bx_, 1.3))
        Bt = T("mouse embryo", 26, BLUE).move_to([bx_, 3.0, 0])
        Bl = T("3 cells or 5 can occur", 26, YELLOW).move_to([bx_, -2.0, 0])
        self.at("A real mouse embryo")
        self.play(FadeIn(B, scale=0.8), FadeIn(Bt), run_time=0.7)
        self.at("not synchronous")
        self.play(FadeIn(Bl), run_time=0.5)
        yolk = RoundedRectangle(corner_radius=0.2, width=3.8, height=2.2, stroke_color=GOLD, stroke_width=3,
                                fill_color=GOLD, fill_opacity=0.28).move_to([cx_, -0.2, 0])
        disc = grid(12, 2, cx_, 1.3, w=2.6, h=0.5, gap=0.03)
        Ct = T("birds", 26, BLUE).move_to([cx_, 3.0, 0])
        Cy = T("yolk, undivided", 24, GOLD).move_to(yolk.get_center())
        Cd = T("disc of cells on the yolk", 24, BLUE).next_to(disc, UP, buff=0.12)
        Cl = T("only a disc cleaves", 26, YELLOW).move_to([cx_, -2.0, 0])
        self.at("Yolk matters")
        self.play(FadeIn(yolk), FadeIn(Cy), run_time=0.6)
        self.at("In birds")
        self.play(FadeIn(disc, scale=0.9), FadeIn(Ct), FadeIn(Cd), FadeIn(Cl), run_time=0.8)
        self.at("Keep this rule")
        allp = VGroup(A, At, Al, B, Bt, Bl, yolk, disc, Ct, Cy, Cd, Cl)
        self.play(FadeOut(allp), run_time=0.6)
        rule = T("Cleavage divides without growth", 48, font=TITLE_FONT).move_to([0, 1.9, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        c1 = chip("more cells", BLUE, 34).move_to([-3.3, 0.2, 0])
        c2 = chip("smaller cells", BLUE, 34).move_to([3.3, 0.2, 0])
        c3 = chip("more total membrane", TEAL, 34).move_to([-3.3, -1.5, 0])
        c4 = chip("same total volume", GREEN, 34).move_to([3.3, -1.5, 0])
        self.at("cells shrink")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.5)
        self.at("their number")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("total membrane")
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(c4, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "In equal, synchronous cleavage without growth: cells shrink, membrane rises."
