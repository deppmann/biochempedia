"""Size, scale and surface: bigger bodies lose surface  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = surface: outer area, exchange surfaces (outline of a cube, slab, fold, branches)
  ORANGE = volume (fill of a cube)
  YELLOW = energy use, metabolic rate
  TEAL   = diffusion (diffusion arrows, diffusion time)
  PURPLE = bulk flow
  RED    = the open question, a hedge ("a fit, not a law", "?")
  TEXT   = the two animals (mouse, human); GREY = axes, outlines, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array(a, float), np.array(b, float), buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def left_label(text, x, y, size=28, color=TEXT):
    t = T(text, size, color)
    return t.move_to([x, y, 0]).align_to([x, 0, 0], LEFT).set_y(y)


class S00Title(TitleCard):
    LESSON = "Size, Scale and Surface"
    TITLE = "Bigger bodies, less surface per volume"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """mouse and human; mass bar vs energy bar to the same scale; per-kg gap; Why?"""

    def construct(self):
        mouse = chip("30 g mouse", TEXT, size=30).move_to([-3.3, 3.0, 0])
        human = chip("70 kg adult human", TEXT, size=30).move_to([3.3, 3.0, 0])
        self.play(FadeIn(mouse, shift=DOWN * 0.2), run_time=0.6)
        self.at("kilogram human")
        self.play(FadeIn(human, shift=DOWN * 0.2), run_time=0.6)

        x0, L = -3.4, 9.4
        note = T("bars drawn to the same scale, mouse = 1", 22, GREY).move_to([0, 2.15, 0])
        # mass row
        y1 = 1.1
        l1 = left_label("mass", -6.3, y1)
        tick1 = Line([x0, y1 - 0.3, 0], [x0, y1 + 0.3, 0], color=TEXT, stroke_width=4)
        mtag = T("mouse = 1", 22, GREY).next_to(tick1, DOWN, buff=0.12).align_to([x0 - 0.1, 0, 0], LEFT)
        bar1 = Rectangle(width=L, height=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5)
        bar1.move_to([x0 + L / 2, y1, 0])
        lab1 = T("human: more than 2,000 times", 26, TEXT).move_to([x0 + L, y1 + 0.55, 0], aligned_edge=RIGHT)
        self.at("is more than", lead=0.0)
        self.play(FadeIn(note), FadeIn(l1), FadeIn(tick1), FadeIn(mtag), run_time=0.4)
        self.play(GrowFromEdge(bar1, LEFT), run_time=1.3)
        self.play(FadeIn(lab1), run_time=0.4)

        # energy row
        y2 = -0.55
        w2 = L * 340 / 2333
        l2 = left_label("energy per day", -6.3, y2)
        tick2 = Line([x0, y2 - 0.3, 0], [x0, y2 + 0.3, 0], color=TEXT, stroke_width=4)
        bar2 = Rectangle(width=w2, height=0.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5)
        bar2.move_to([x0 + w2 / 2, y2, 0])
        lab2 = T("human: about 340 times", 26, YELLOW).move_to([x0 + w2 + 0.25, y2, 0], aligned_edge=LEFT)
        self.at("burns only", lead=0.0)
        self.play(FadeIn(l2), FadeIn(tick2), run_time=0.3)
        self.play(GrowFromEdge(bar2, LEFT), run_time=1.0)
        self.play(FadeIn(lab2), run_time=0.3)

        perkg = T("per kilogram, the mouse burns about 7 times more", 30, YELLOW).move_to([0, -1.85, 0])
        self.at("each kilogram", lead=0.3)
        self.play(FadeIn(perkg, shift=UP * 0.15), run_time=0.7)
        why = T("Why?", 56, RED, font=TITLE_FONT).move_to([0, -3.0, 0])
        self.at("why", lead=0.1)
        self.play(FadeIn(why, scale=1.3), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Cube(SpokenScene):
    """ideal cube: double the side, area x4, volume x8, ratio 6/s halves from 0.6 to 0.3 per um."""

    def construct(self):
        s1, s2 = 1.1, 2.2
        base = -1.1
        sq1 = Square(s1, stroke_color=BLUE, stroke_width=6, fill_color=ORANGE, fill_opacity=0.35)
        sq1.move_to([-5.0, base + s1 / 2, 0])
        sq2 = Square(s2, stroke_color=BLUE, stroke_width=6, fill_color=ORANGE, fill_opacity=0.35)
        sq2.move_to([-2.7, base + s2 / 2, 0])
        t1 = T("side 10 um", 24).next_to(sq1, DOWN, buff=0.2)
        t2 = T("side 20 um", 24).next_to(sq2, DOWN, buff=0.2)
        cap = T("ideal cubes, drawn flat", 22, GREY).move_to([-3.85, -2.5, 0])
        surf = T("outline: surface", 26, BLUE).move_to([-3.85, 3.0, 0])
        vol = T("fill: volume", 26, ORANGE).move_to([-3.85, 2.45, 0])

        self.play(FadeIn(surf, shift=DOWN * 0.1), run_time=0.5)
        self.at("ideal cube")
        self.play(FadeIn(vol, shift=DOWN * 0.1), Create(sq1), FadeIn(t1), run_time=0.8)
        self.at("double its side")
        self.play(ReplacementTransform(sq1.copy(), sq2), FadeIn(t2), run_time=1.0)

        a_chip = chip("area x 4", BLUE, size=28).move_to([-5.0, 1.45, 0])
        v_chip = chip("volume x 8", ORANGE, size=28).move_to([-2.4, 1.45, 0])
        self.at("area grows")
        self.play(FadeIn(a_chip, scale=0.9), run_time=0.5)
        self.at("volume grows")
        self.play(FadeIn(v_chip, scale=0.9), run_time=0.5)

        ox, oy, W, H = 1.3, -2.6, 4.9, 4.6
        xs = lambda s: ox + W * s / 25.0
        ys = lambda r: oy + H * r / 0.8
        axes = VGroup(Line([ox, oy, 0], [ox + W, oy, 0], color=GREY, stroke_width=3),
                      Line([ox, oy, 0], [ox, oy + H, 0], color=GREY, stroke_width=3))
        xt = VGroup(*[M(str(v), 22, GREY).move_to([xs(v), oy - 0.3, 0]) for v in (10, 20)])
        yt = VGroup(*[M(str(v), 22, GREY).move_to([ox - 0.4, ys(v), 0]) for v in (0.3, 0.6)])
        xl = T("side s (um)", 22, GREY).move_to([ox + W / 2, oy - 0.72, 0])
        yl = T("ratio, per um", 22, GREY).move_to([ox + 1.0, oy + H + 0.25, 0])
        curve = VMobject(color=BLUE, stroke_width=5)
        ss = np.linspace(8, 24, 60)
        curve.set_points_smoothly([np.array([xs(s), ys(6 / s), 0]) for s in ss])
        p1 = Dot([xs(10), ys(0.6), 0], color=BLUE, radius=0.11)
        p2 = Dot([xs(20), ys(0.3), 0], color=BLUE, radius=0.11)
        l1 = M("0.6", 28, BLUE).next_to(p1, UR, buff=0.1)
        l2 = M("0.3", 28, BLUE).next_to(p2, UR, buff=0.1)
        form = M("ratio = 6 / s", 30, BLUE).move_to([ox + W / 2 + 0.3, oy + H + 0.85, 0])
        self.at("the surface area")
        self.play(FadeIn(axes), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(form), run_time=0.7)
        self.play(Create(curve), run_time=0.8)
        self.play(FadeIn(p1, scale=0.5), FadeIn(l1), run_time=0.4)
        self.at("halves")
        trav = p1.copy()
        self.play(Transform(trav, p2), FadeIn(l2), run_time=0.8)
        self.at("illustrative")
        self.play(FadeIn(cap), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Diffuse(SpokenScene):
    """t = L^2 / 2D on log axes: 10 um 0.05 s, 1 cm about 14 hours (D = 1,000 um^2 per s)."""

    def construct(self):
        ox, oy, W, H = -4.7, -2.7, 6.0, 5.0
        lx = lambda e: ox + W * e / 4.0            # e = log10 distance in um, 0..4
        ly = lambda e: oy + H * (e + 3) / 8.0      # e = log10 time in s, -3..5
        axes = VGroup(Line([ox, oy, 0], [ox + W + 0.2, oy, 0], color=GREY, stroke_width=3),
                      Line([ox, oy, 0], [ox, oy + H + 0.2, 0], color=GREY, stroke_width=3))
        xt = VGroup(*[T(t, 22, GREY).move_to([lx(e), oy - 0.32, 0]) for e, t in [(1, "10 um"), (2, "100 um")]],
                    T("1 cm", 22, GREY).move_to([lx(4), oy - 0.32, 0]))
        yt = VGroup(*[T(t, 22, GREY).move_to([ox - 0.7, ly(e), 0]) for e, t in
                      [(-2, "0.01 s"), (0, "1 s"), (2, "100 s"), (4, "10,000 s")]])
        xl = T("distance (log scale)", 22, GREY).move_to([ox + W / 2, oy - 0.8, 0])
        yl = T("time (log scale)", 22, GREY).move_to([ox + 0.5, oy + H + 0.35, 0])
        # opening demo: a crowd of dots spreads through a box (schematic, no structure)
        box = Rectangle(width=8.0, height=3.2, stroke_color=GREY, stroke_width=3).move_to([0, 0.3, 0])
        rng = np.random.RandomState(3)
        pts0 = [np.array([-3.7 + 0.5 * rng.rand(), 0.3 + 1.2 * (rng.rand() - 0.5), 0]) for _ in range(40)]
        pts1 = [np.array([-3.8 + 7.6 * rng.rand(), 0.3 + 3.0 * (rng.rand() - 0.5), 0]) for _ in range(40)]
        crowd = VGroup(*[Dot(p, color=TEAL, radius=0.09) for p in pts0])
        spread = VGroup(*[Dot(p, color=TEAL, radius=0.09) for p in pts1])
        mol = T("molecules spread from crowded to less crowded", 26, TEAL).move_to([0, -1.9, 0])
        self.play(Create(box), FadeIn(crowd), run_time=0.8)
        self.at("less crowded")
        self.play(FadeIn(mol), Transform(crowd, spread), run_time=2.0)
        self.at("simple model")
        self.play(FadeOut(VGroup(box, crowd, mol)), run_time=0.5)
        self.play(FadeIn(axes), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), run_time=0.8)

        form = M("t = L^2 / 2D", 32, TEAL).move_to([4.15, 0.9, 0])
        n1 = T("L: distance", 22, GREY).move_to([4.15, 0.2, 0])
        n2 = T("D: diffusion coefficient", 22, GREY).move_to([4.15, -0.25, 0])
        self.at("the distance squared")
        self.play(FadeIn(form, shift=UP * 0.1), FadeIn(n1), FadeIn(n2), run_time=0.7)
        line = Line([lx(0.15), ly(2 * 0.15 - 3.301), 0], [lx(4), ly(2 * 4 - 3.301), 0], color=TEAL, stroke_width=5)
        self.play(Create(line), run_time=1.1)
        sl = T("slope 2: time grows", 22, TEAL).move_to([ox + 1.6, oy + H - 0.6, 0])
        sl2 = T("with distance squared", 22, TEAL).move_to([ox + 1.6, oy + H - 1.05, 0])
        mdl = T("in this sketch (model):", 22, GREY).move_to([4.15, -1.5, 0])
        mdl2 = T("D = 1,000 um2 per s,", 22, GREY).move_to([4.15, -1.95, 0])
        mdl3 = T("small solute in water", 22, GREY).move_to([4.15, -2.4, 0])
        self.play(FadeIn(sl), FadeIn(sl2), FadeIn(mdl), FadeIn(mdl2), FadeIn(mdl3), run_time=0.6)

        d1 = Dot([lx(1), ly(np.log10(0.05)), 0], color=YELLOW, radius=0.12)
        l1 = T("10 um: about 0.05 s", 26, YELLOW).move_to([lx(1) + 0.3, ly(np.log10(0.05)) - 0.35, 0], aligned_edge=LEFT)
        self.at("takes about", nth=0)
        self.play(FadeIn(d1, scale=0.4), FadeIn(l1), run_time=0.6)
        d2 = Dot([lx(4), ly(np.log10(50000)), 0], color=YELLOW, radius=0.12)
        l2 = T("1 cm: about 14 hours", 26, YELLOW).move_to([lx(4) + 0.3, ly(np.log10(50000)), 0], aligned_edge=LEFT)
        self.at("takes about", nth=1)
        self.play(FadeIn(d2, scale=0.4), FadeIn(l2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def panel_head(text, sub, color, cx, cy):
    h = T(text, 30, color, weight=BOLD).move_to([cx - 2.8, cy + 1.25, 0], aligned_edge=LEFT)
    s = T(sub, 22, GREY).move_to([cx - 2.8, cy - 1.3, 0], aligned_edge=LEFT)
    return h, s


def branch(p, ang, length, depth, color=BLUE):
    d = np.array([np.cos(ang), np.sin(ang), 0.0])
    q = p + d * length
    out = [Line(p, q, color=color, stroke_width=3 + 2 * depth)]
    if depth > 0:
        out += branch(q, ang + 0.5, length * 0.72, depth - 1, color)
        out += branch(q, ang - 0.5, length * 0.72, depth - 1, color)
    return out


class S04Four(SpokenScene):
    """four schematic panels: flattening, folding, branching, bulk flow."""

    def construct(self):
        P = [(-3.4, 1.75), (3.4, 1.75), (-3.4, -1.85), (3.4, -1.85)]
        frames = [RoundedRectangle(corner_radius=0.15, width=6.4, height=3.3, stroke_color=GREY, stroke_width=2,
                                   stroke_opacity=0.5).move_to([x, y, 0]) for x, y in P]

        # 1 flattening
        cx, cy = P[0]
        slab = Rectangle(width=3.8, height=0.5, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to([cx + 0.4, cy, 0])
        ins = VGroup(*[arr([cx - 1.0 + 0.9 * i, cy + 0.95, 0], [cx - 1.0 + 0.9 * i, cy + 0.32, 0], TEAL) for i in range(4)],
                     *[arr([cx - 1.0 + 0.9 * i + 0.0, cy - 0.95, 0], [cx - 1.0 + 0.9 * i, cy - 0.32, 0], TEAL) for i in range(4)])
        ins.shift(RIGHT * 0.6)
        h1, s1 = panel_head("Flattening", "planarian flatworm, leaf blade", BLUE, cx, cy)
        # 2 folding
        cx, cy = P[1]
        box = Rectangle(width=3.8, height=1.0, stroke_color=GREY, stroke_width=2).move_to([cx + 0.4, cy - 0.1, 0])
        box.set_stroke(opacity=0.6)
        pts = [np.array([cx - 1.5 + 0.375 * i, cy - 0.1 + (0.4 if i % 2 else -0.4), 0]) for i in range(0, 17)]
        zig = VMobject(color=BLUE, stroke_width=5).set_points_as_corners(pts)
        zig.shift(RIGHT * 0.4 - RIGHT * 0.0)
        zig.stretch_to_fit_width(3.6).move_to(box)
        h2, s2 = panel_head("Folding", "alveoli, inside a leaf", BLUE, cx, cy)
        # 3 branching
        cx, cy = P[2]
        tree = VGroup(*branch(np.array([cx + 0.4, cy - 1.05, 0]), np.pi / 2, 0.95, 3))
        h3, s3 = panel_head("Branching", "airways, leaf veins (not to scale)", BLUE, cx, cy)
        # 4 bulk flow
        cx, cy = P[3]
        tube = Rectangle(width=3.0, height=0.55, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.25).move_to([cx - 0.5, cy, 0])
        flow = arr([cx - 1.7, cy, 0], [cx + 0.7, cy, 0], PURPLE, w=7, tip=0.28)
        tissue = Rectangle(width=0.9, height=1.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to([cx + 1.95, cy, 0])
        dif = VGroup(*[arr([cx + 1.05, cy + dy, 0], [cx + 1.45, cy + dy, 0], TEAL, w=4, tip=0.12) for dy in (-0.3, 0, 0.3)])
        h4, s4 = panel_head("Bulk flow", "blood, air, sap", PURPLE, cx, cy)
        cells = T("cells", 22, BLUE).move_to(tissue)

        self.play(*[Create(f) for f in frames], run_time=0.8)
        self.at("Flattening")
        self.play(FadeIn(h1), FadeIn(s1), GrowFromCenter(slab), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.1), run_time=0.9)
        self.at("Folding")
        self.play(FadeIn(h2), FadeIn(s2), Create(box), run_time=0.5)
        self.play(Create(zig), run_time=1.1)
        self.at("Branching")
        self.play(FadeIn(h3), FadeIn(s3), run_time=0.4)
        self.play(LaggedStart(*[Create(b) for b in tree], lag_ratio=0.08), run_time=1.6)
        self.at("Bulk flow")
        self.play(FadeIn(h4), FadeIn(s4), FadeIn(tube), run_time=0.5)
        self.play(GrowArrow(flow), FadeIn(tissue), FadeIn(cells), run_time=0.8)
        self.at("diffusion still")
        self.play(LaggedStart(*[GrowArrow(a) for a in dif], lag_ratio=0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Power(SpokenScene):
    """the fit: rate = 70 x M^0.75 kcal per day; totals; per-kg bars 168 vs 24."""

    def construct(self):
        form = M("rate = 70 x M^0.75", 44, YELLOW).move_to([0, 3.0, 0])
        unit = T("kcal per day, M in kg: a fit for mammals, basal", 26, GREY).move_to([0, 2.3, 0])
        self.at("widely quoted")
        self.play(FadeIn(form, shift=DOWN * 0.1), run_time=0.8)
        self.at("times mass")
        self.play(Indicate(form, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.at("kilocalories a day")
        self.play(FadeIn(unit, shift=UP * 0.1), run_time=0.6)

        ym, yh = 0.4, -1.3
        h_tot = T("total, kcal per day", 24, GREY).move_to([-0.7, 1.35, 0])
        h_kg = T("per kilogram, kcal per day", 24, GREY).move_to([3.9, 1.35, 0])
        mouse = chip("30 g mouse", TEXT, size=26)
        human = chip("70 kg adult human", TEXT, size=26)
        mouse.move_to([-6.3 + mouse.width / 2, ym, 0])
        human.move_to([-6.3 + human.width / 2, yh, 0])
        tm = M("about 5", 32, YELLOW).move_to([-0.7, ym, 0])
        th = M("about 1,700", 32, YELLOW).move_to([-0.7, yh, 0])
        scale = 2.3 / 168
        x0 = 1.7
        bm = Rectangle(width=168 * scale, height=0.7, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.45)
        bm.move_to([x0 + 168 * scale / 2, ym, 0])
        bh = Rectangle(width=24 * scale, height=0.7, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.45)
        bh.move_to([x0 + 24 * scale / 2, yh, 0])
        vm = M("about 168", 28, YELLOW).move_to([x0 + 168 * scale + 0.2, ym, 0], aligned_edge=LEFT)
        vh = M("about 24", 28, YELLOW).move_to([x0 + 24 * scale + 0.2, yh, 0], aligned_edge=LEFT)
        low = T("the exponent is below 1: rate per kilogram falls with size", 30, YELLOW).move_to([0, -2.8, 0])

        self.at("that gives")
        self.play(FadeIn(h_tot), FadeIn(mouse), run_time=0.5)
        self.play(FadeIn(tm, shift=UP * 0.1), run_time=0.5)
        self.at("adult human")
        self.play(FadeIn(human), run_time=0.4)
        self.play(FadeIn(th, shift=UP * 0.1), run_time=0.5)
        self.at("Per kilogram")
        self.play(FadeIn(h_kg), run_time=0.4)
        self.play(GrowFromEdge(bm, LEFT), FadeIn(vm), run_time=1.0)
        self.play(GrowFromEdge(bh, LEFT), FadeIn(vh), run_time=0.7)
        self.at("falls as animals")
        self.play(FadeIn(low, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the hedge: 3/4 is a fit; 2/3 (White and Seymour) makes 7 become 13; cause debated; then the rule."""

    def construct(self):
        b1 = chip("exponent 3/4: a fit, not a law", RED, size=36).move_to([0, 3.0, 0])
        self.play(FadeIn(b1, shift=DOWN * 0.15), run_time=0.7)

        x0, u = -3.2, 0.46      # 1 unit = rate per kilogram of the human
        yh, ym = 1.4, 0.0
        hl = left_label("human per kg", -6.3, yh, 28)
        ml = left_label("mouse per kg", -6.3, ym, 28)
        bh = Rectangle(width=u, height=0.6, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.45)
        bh.move_to([x0 + u / 2, yh, 0])
        bm = Rectangle(width=7 * u, height=0.6, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.45)
        bm.move_to([x0 + 3.5 * u, ym, 0])
        vh = M("1", 30, YELLOW).move_to([x0 + u + 0.2, yh, 0], aligned_edge=LEFT)
        vm = M("about 7", 30, YELLOW).move_to([x0 + 7 * u + 0.2, ym, 0], aligned_edge=LEFT)
        self.play(FadeIn(hl), FadeIn(ml), FadeIn(bh), FadeIn(vh), run_time=0.5)
        self.play(GrowFromEdge(bm, LEFT), FadeIn(vm), run_time=0.8)

        b2 = chip("if the exponent were 2/3 (White and Seymour, 2003)", RED, size=34).move_to([0, 3.0, 0])
        bm2 = Rectangle(width=13 * u, height=0.6, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.45)
        bm2.move_to([x0 + 6.5 * u, ym, 0])
        vm2 = M("about 13", 30, YELLOW).move_to([x0 + 13 * u + 0.2, ym, 0], aligned_edge=LEFT)
        ctl = T("mammals, body temperature and digestive state controlled", 24, GREY).move_to([0, 2.15, 0])
        ar = T("the lesson's arithmetic: (70 / 0.03)^(1/3)", 24, GREY).move_to([0, -0.9, 0])
        self.at("found a mammalian")
        self.play(ReplacementTransform(b1, b2), FadeOut(bm), FadeOut(vm), run_time=0.9)
        self.at("body temperature")
        self.play(FadeIn(ctl), run_time=0.4)
        self.at("advantage per kilogram")
        self.play(GrowFromEdge(bm2, LEFT), FadeIn(vm2), FadeIn(ar), run_time=1.0)
        deb = T("What causes the exponent? Still debated.", 34, RED).move_to([0, -1.6, 0])
        self.at("still debated")
        self.play(FadeIn(deb, shift=UP * 0.1), run_time=0.6)

        c1 = chip("larger body: surface falls behind volume", BLUE, size=34)
        c2 = chip("bulk flow carries material", PURPLE, size=34)
        c3 = chip("diffusion covers the last few micrometres", TEAL, size=34)
        rule = VGroup(c1, c2, c3).arrange(DOWN, buff=0.9).move_to([0, 0.0, 0])
        a1 = arr(c1.get_bottom(), c2.get_top(), GREY, w=6)
        a2 = arr(c2.get_bottom(), c3.get_top(), GREY, w=6)
        self.at("Keep this rule")
        self.play(FadeOut(VGroup(b2, ctl, ar, deb, hl, ml, bh, vh, bm2, vm2)), run_time=0.5)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.at("flow carries")
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        self.at("diffusion covers")
        self.play(GrowArrow(a2), FadeIn(c3, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Larger bodies lose surface per volume, so flow carries material."
