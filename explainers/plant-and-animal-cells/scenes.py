"""Plant and animal cells: a full vacuole holds a plant up  (Biochemistrypedia grade 7 Life Science film)

COLOR MAP (one color per concept, whole film)
  GREY    = cell membrane, outlines, leader lines, de-emphasized things
  PURPLE  = nucleus
  PINK    = mitochondria
  TEAL    = endoplasmic reticulum
  BLUE    = vacuole and water
  ORANGE  = cell wall
  GREEN   = chloroplasts
  YELLOW  = radiant energy
  GOLD    = sugar (glucose)
  RED     = absent / limp / not so (no bones, no walls, limp)
  CELERY  = the celery stalk itself (scene 1 only)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E86FA8"
CELERY = "#A9C98A"

CW, CH = 4.0, 5.0       # cell width and height
CY = -0.4               # cell centre height
AX, PX = -4.1, 4.1      # animal / plant cell centre x
ROWS = {"nucleus": 1.5, "membrane": 0.75, "mito": 0.0, "cytoplasm": -0.75, "er": -1.5, "vacuole": -2.25}


def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ghost(w, h, color=GREY, r=0.14):
    box = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=2.5)
    return DashedVMobject(box, num_dashes=28).set_color(color)


class Cell:
    """a schematic cell: outline, cytoplasm tint and organelles, all positioned from local coordinates."""

    def __init__(self, kind, cx, cy=CY, k=1.0):
        self.kind, self.cx, self.cy, self.k = kind, cx, cy, k
        self.s = 1 if kind == "animal" else -1       # +1: the cell sits left of the label column, so "inner" is +x
        self.r = 1.1 if kind == "animal" else 0.3
        self.out = RoundedRectangle(corner_radius=self.r * k, width=CW * k, height=CH * k, stroke_color=GREY,
                                    stroke_width=4).move_to(self.pt(0, 0))
        self.parts = {}

    def pt(self, dx, dy):
        return np.array([self.cx + self.k * dx, self.cy + self.k * dy, 0.0])

    # -- organelles (local coordinates relative to the cell centre; "near" side faces the label column)
    def add_nucleus(self):
        m = Circle(radius=0.45 * self.k, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3)
        m.move_to(self.pt(self.s * 0.8, 1.9)); self.parts["nucleus"] = m; return m

    def add_mito(self):
        g = VGroup()
        for dx, dy in ((self.s * 0.85, 0.4), (-self.s * 0.9, -1.4)):
            g.add(Ellipse(width=1.1 * self.k, height=0.55 * self.k, stroke_color=PINK, stroke_width=3,
                          fill_color=PINK, fill_opacity=0.3).move_to(self.pt(dx, dy)))
        self.parts["mito"] = g; return g

    def add_cyto(self):
        m = RoundedRectangle(corner_radius=self.r * self.k, width=CW * self.k, height=CH * self.k, stroke_width=0,
                             fill_color=GREY, fill_opacity=0.13).move_to(self.pt(0, 0))
        self.parts["cytoplasm"] = m; return m

    def add_er(self):
        g = VGroup()
        for dy in (0.13, -0.13):
            f = lambda t, dy=dy: np.array([t, 0.1 * np.sin(t * 9.0) + dy, 0.0]) * self.k
            c = ParametricFunction(f, t_range=[-0.65, 0.65, 0.02], color=TEAL, stroke_width=4)
            g.add(c)
        g.move_to(self.pt(self.s * 0.85, -1.1)); self.parts["er"] = g; return g

    def add_vacuole(self):
        m = Circle(radius=0.32 * self.k, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35)
        m.move_to(self.pt(self.s * 0.85, -1.85)); self.parts["vacuole"] = m; return m

    def add_chloroplasts(self):
        g = VGroup()
        for dx, dy in ((0.85, 1.6), (1.15, 0.7), (0.75, -0.2)):
            g.add(Ellipse(width=1.1 * self.k, height=0.6 * self.k, stroke_color=GREEN, stroke_width=3,
                          fill_color=GREEN, fill_opacity=0.3).move_to(self.pt(dx, dy)))
        self.parts["chloroplast"] = g; return g

    def add_wall(self, m=0.2):
        w = RoundedRectangle(corner_radius=(self.r + m) * self.k, width=(CW + 2 * m) * self.k,
                             height=(CH + 2 * m) * self.k, stroke_color=ORANGE, stroke_width=9).move_to(self.pt(0, 0))
        self.parts["wall"] = w; return w

    def fill_basic(self):
        return [self.add_cyto(), self.add_nucleus(), self.add_mito(), self.add_er(), self.add_vacuole()]

    def group(self):
        return VGroup(self.out, *self.parts.values())

    # leader targets (absolute) on the side facing the label column
    def target(self, key):
        s = self.s
        rel = {"nucleus": (s * (0.8 + 0.45), 1.9), "membrane": (s * 2.0, 1.15), "mito": (s * (0.85 + 0.55), 0.4),
               "cytoplasm": (s * 1.15, -0.35), "er": (s * (0.85 + 0.65), -1.1), "vacuole": (s * (0.85 + 0.32), -1.85)}[key]
        return self.pt(*rel)


def titles(a, p):
    ta = T("animal cell", 28).move_to([a.cx, 2.75, 0])
    tp = T("plant cell", 28).move_to([p.cx, 2.75, 0])
    return ta, tp


class S00Title(TitleCard):
    LESSON = "Plant cells and animal cells"
    TITLE = "A full vacuole holds a plant up"


# ---------------------------------------------------------------------------------------------
class S01Celery(SpokenScene):
    """limp celery, water, crisp celery; drinking water does not stiffen a body; two questions."""

    def construct(self):
        base = np.array([-3.2, -1.55, 0])
        L = 3.4
        glass = VMobject(stroke_color=GREY, stroke_width=5)
        glass.set_points_as_corners([[-4.15, -0.85, 0], [-4.0, -2.75, 0], [-2.4, -2.75, 0], [-2.25, -0.85, 0]])
        d = ValueTracker(1.0)

        def make_stalk():
            dd = d.get_value()
            n = 50
            s = np.linspace(0, L, n)
            th = np.pi / 2 - dd * 1.45 * (s / L) ** 1.6
            ds = L / (n - 1)
            x = base[0] + np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * ds)])
            y = base[1] + np.concatenate([[0], np.cumsum(np.sin(th[:-1]) * ds)])
            m = VMobject(stroke_color=CELERY, stroke_width=24, cap_style=CapStyleType.ROUND)
            m.set_points_as_corners([[a, b, 0] for a, b in zip(x, y)])
            return m

        stalk = always_redraw(make_stalk)
        water = Rectangle(width=1.5, height=0.01, stroke_width=0, fill_color=BLUE, fill_opacity=0.45)
        water.move_to([-3.2, -2.75 + 0.005, 0])
        water_lbl = T("water", 26, BLUE).move_to([-3.2, -3.3, 0])

        self.add(stalk, glass)
        limp = T("limp", 40, RED, weight=BOLD).move_to([-3.2, 2.6, 0])
        self.at("limp and bendy")
        self.play(FadeIn(limp, shift=DOWN * 0.15), run_time=0.5)
        self.at("Put it in water")
        self.play(FadeIn(water_lbl), water.animate.stretch_to_fit_height(1.45, about_edge=DOWN).set_fill(BLUE, 0.45),
                  run_time=1.0)
        crisp = T("crisp", 40, TEXT, weight=BOLD).move_to([-3.2, 2.6, 0])
        self.at("crisp again")
        self.add(water)
        self.play(d.animate.set_value(0.0), FadeOut(limp), FadeIn(crisp), run_time=1.6)

        # you drink water: the body does not get stiffer
        body = RoundedRectangle(corner_radius=0.2, width=3.6, height=2.0, stroke_color=GREY, stroke_width=4).move_to([3.3, 1.5, 0])
        body_l = T("your body", 32).move_to(body.get_center() + UP * 0.35)
        body_s = T("not stiffer", 28, RED).move_to(body.get_center() + DOWN * 0.4)
        drink = chip("water", BLUE, 28).move_to([3.3, -1.3, 0])
        a_in = arr(drink.get_top() + UP * 0.05, body.get_bottom(), BLUE)
        self.at("You drink water")
        self.play(FadeIn(body), FadeIn(body_l), FadeIn(drink, shift=UP * 0.2), run_time=0.7)
        self.play(GrowArrow(a_in), run_time=0.6)
        self.at("does not stiffen")
        self.play(FadeIn(body_s, shift=UP * 0.1), run_time=0.5)

        nob = chip("no bones", RED, 30).move_to([-5.0, 0.2, 0])
        self.at("no bones")
        self.play(FadeIn(nob, shift=RIGHT * 0.2), run_time=0.6)

        # the two questions
        q1 = T("How does a plant stand up?", 44, font=TITLE_FONT).move_to([0, 1.0, 0])
        q2 = T("How are its cells different from yours?", 44, font=TITLE_FONT).move_to([0, -0.9, 0])
        fit(q2, max_w=12.0)
        self.at("how does a plant stand up")
        self.play(*[FadeOut(m) for m in (stalk, glass, water, water_lbl, crisp, body, body_l, body_s, drink, a_in, nob)],
                  run_time=0.6)
        self.play(Write(q1), run_time=1.2)
        self.at("how are its cells")
        self.play(Write(q2), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Shared(SpokenScene):
    """the six parts both kinds of cell share."""

    def construct(self):
        A, P = Cell("animal", AX), Cell("plant", PX)
        ta, tp = titles(A, P)
        self.play(Create(A.out), Create(P.out), FadeIn(ta), FadeIn(tp), run_time=1.4)

        head = chip("organelle", TEXT, 28).move_to([0, 2.55, 0])
        self.at("an organelle")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)

        def label(text, color, key):
            return T(text, 24, color).move_to([0, ROWS[key], 0])

        def leaders(lab, key, color):
            out = VGroup()
            for c in (A, P):
                tgt = c.target(key)
                edge = lab.get_left() + LEFT * 0.1 if c is A else lab.get_right() + RIGHT * 0.1
                edge[1] = lab.get_center()[1]
                tgt = np.array([tgt[0], lab.get_center()[1], 0.0])
                out.add(Line(edge, tgt, color=color, stroke_width=2.5), Dot(tgt, radius=0.06, color=color))
            return out

        def show(key, text, color, phrase, mobs_for, run=0.9):
            lab = label(text, color, key)
            ld = leaders(lab, key, color)
            self.at(phrase)
            anims = [FadeIn(lab, shift=DOWN * 0.1), Create(ld)]
            for m in mobs_for:
                anims.append(FadeIn(m, scale=0.8))
            self.play(*anims, run_time=run)
            return lab

        n = [A.add_nucleus(), P.add_nucleus()]
        show("nucleus", "nucleus", PURPLE, "The nucleus holds", n)
        self.play(*[Indicate(m, color=PURPLE, scale_factor=1.25) for m in n], run_time=0.6)

        lab = label("cell membrane", GREY, "membrane")
        ld = leaders(lab, "membrane", GREY)
        self.at("The cell membrane")
        self.play(FadeIn(lab, shift=DOWN * 0.1), Create(ld), A.out.animate.set_stroke(TEXT, 7), P.out.animate.set_stroke(TEXT, 7), run_time=0.6)
        self.play(A.out.animate.set_stroke(GREY, 4), P.out.animate.set_stroke(GREY, 4), run_time=0.6)

        m = [A.add_mito(), P.add_mito()]
        show("mito", "mitochondria", PINK, "Mitochondria release", m)
        self.play(*[Indicate(x, color=PINK, scale_factor=1.2) for x in m], run_time=0.6)

        cy = [A.add_cyto(), P.add_cyto()]
        show("cytoplasm", "cytoplasm", GREY, "The cytoplasm is", cy)

        er = [A.add_er(), P.add_er()]
        show("er", "endoplasmic reticulum", TEAL, "The endoplasmic reticulum is", er)

        va = [A.add_vacuole(), P.add_vacuole()]
        show("vacuole", "vacuole", BLUE, "A vacuole is", va)
        self.finish()


# ---------------------------------------------------------------------------------------------
def stage_cells(scene, wall=True, dim_animal=False):
    A, P = Cell("animal", AX), Cell("plant", PX)
    A.fill_basic(); P.fill_basic()
    if wall:
        P.add_wall()
    ta, tp = titles(A, P)
    scene.add(A.out, P.out, *A.parts.values(), *P.parts.values(), ta, tp)
    return A, P, ta, tp


class S03Wall(SpokenScene):
    """the first added part: the cell wall, outside the membrane."""

    def construct(self):
        A, P, ta, tp = stage_cells(self, wall=False)
        w = P.add_wall()
        w_ghost = None
        ys = [1.9, 0.9, -0.1]
        boxes = [ghost(2.9, 0.7, GREY).move_to([0, y, 0]) for y in ys]
        qs = [T("?", 30, GREY).move_to([0, y, 0]) for y in ys]
        self.at("three more")
        self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(q)) for b, q in zip(boxes, qs)], lag_ratio=0.25), run_time=1.2)
        wallchip = chip("cell wall", ORANGE, 28).move_to([0, ys[0], 0])
        a_w = arr([1.25, ys[0], 0], [PX - 2.2 + 0.02, ys[0], 0], ORANGE)
        self.at("the cell wall")
        self.play(ReplacementTransform(VGroup(boxes[0], qs[0]), wallchip), Create(w), run_time=1.4)
        self.play(GrowArrow(a_w), run_time=0.5)
        self.at("stiff layer")
        self.play(Indicate(w, color=ORANGE, scale_factor=1.03), run_time=0.8)
        mem = T("cell membrane", 24, GREY).move_to([0, -1.1, 0])
        a_m = arr([mem.get_right()[0] + 0.1, -1.1, 0], [PX - 2.0 + 0.04, -1.1, 0], GREY)
        self.at("outside the cell membrane")
        self.play(FadeIn(mem), GrowArrow(a_m), run_time=0.7)
        sup = T("supports and\nprotects the cell", 24, TEXT, line_spacing=0.8).move_to([0, -2.1, 0])
        self.at("supports and protects")
        self.play(FadeIn(sup, shift=UP * 0.1), run_time=0.7)
        gw = DashedVMobject(RoundedRectangle(corner_radius=(A.r + 0.15), width=CW + 0.3, height=CH + 0.3, stroke_color=ORANGE,
                                             stroke_width=7).move_to(A.pt(0, 0)), num_dashes=60)
        no = T("no cell wall", 28, RED, weight=BOLD).move_to([A.cx, -3.5, 0])
        self.at("Animal cells have")
        self.play(Create(gw), run_time=0.8)
        self.play(FadeIn(no, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def zoom_plant(scene):
    """cells as the last scene left them; animal cell and column leave, plant cell moves left and grows."""
    A, P, ta, tp = stage_cells(scene, wall=True)
    K, X, Y = 1.15, -3.25, -0.3
    return A, P, ta, tp, K, X, Y


class S04Chloroplast(SpokenScene):
    """the second added part: chloroplasts capture radiant energy and make sugar; mitochondria release energy from it."""

    def construct(self):
        A, P, ta, tp, K, X, Y = zoom_plant(self)
        ys = [1.9, 0.9, -0.1]
        wallchip = chip("cell wall", ORANGE, 28).move_to([0, ys[0], 0])
        b2, b3 = ghost(2.9, 0.7, GREY).move_to([0, ys[1], 0]), ghost(2.9, 0.7, GREY).move_to([0, ys[2], 0])
        q2, q3 = T("?", 30, GREY).move_to([0, ys[1], 0]), T("?", 30, GREY).move_to([0, ys[2], 0])
        no = T("no cell wall", 28, RED, weight=BOLD).move_to([A.cx, -3.5, 0])
        extras = VGroup(wallchip, b2, b3, q2, q3, no)
        self.add(extras)
        grp = P.group()
        # the camera move: animal cell and column leave, plant cell grows and moves left
        self.at("second part")
        self.play(FadeOut(VGroup(A.group(), ta, extras)), FadeOut(tp),
                  grp.animate.scale(K).move_to([X, Y, 0]), run_time=1.1)
        P.cx, P.cy, P.k = X, Y, K
        tp2 = T("plant cell", 28).move_to([X, 3.3, 0])
        self.add(tp2)

        ch = P.add_chloroplasts()
        mi = P.parts["mito"][1]
        chl = chip("chloroplasts", GREEN, 28).move_to([3.5, 2.75, 0])
        lead = Line(chl.get_left() + LEFT * 0.05, ch[0].get_right() + RIGHT * 0.03 + UP * 0.1, color=GREEN, stroke_width=2.5)
        self.at("chloroplast")
        self.play(FadeIn(ch, scale=0.7), FadeIn(chl, shift=LEFT * 0.2), Create(lead), run_time=1.0)

        rad = T("radiant energy", 28, YELLOW).move_to([3.5, 0.5, 0])
        rays = VGroup(*[arr([0.9, c.get_center()[1], 0], c.get_right() + RIGHT * 0.08, YELLOW, w=6) for c in ch])
        self.at("capture radiant energy")
        self.play(LaggedStart(*[GrowArrow(r) for r in rays], lag_ratio=0.25), FadeIn(rad, shift=LEFT * 0.15), run_time=1.2)
        self.play(*[Indicate(c, color=GREEN, scale_factor=1.2) for c in ch], run_time=0.7)

        sug = chip("sugar (glucose)", GOLD, 28).move_to([3.5, -0.7, 0])
        dots = VGroup(*[Dot(c.get_center(), radius=0.15, color=GOLD) for c in ch])
        self.at("make sugar")
        self.play(FadeIn(sug, shift=LEFT * 0.2), FadeIn(dots, scale=0.4), run_time=0.7)

        gc = T("in green cells", 26, GREEN).move_to([3.5, 2.05, 0])
        self.at("green cells")
        self.play(FadeIn(gc), run_time=0.5)

        mc = chip("mitochondria", PINK, 28).move_to([3.5, -1.75, 0])
        lm = Line(mc.get_left() + LEFT * 0.05, mi.get_right() + RIGHT * 0.04, color=PINK, stroke_width=2.5)
        self.at("still have mitochondria")
        self.play(FadeIn(mc, shift=LEFT * 0.2), Create(lm), Indicate(mi, color=PINK, scale_factor=1.25), run_time=0.9)
        rel = T("release energy from the sugar", 24, TEXT).move_to([3.5, -2.65, 0])
        self.at("release energy from")
        self.play(FadeIn(rel, shift=UP * 0.1), LaggedStart(*[d.animate.move_to(mi.get_center()) for d in dots], lag_ratio=0.2),
                  run_time=1.1)
        self.play(FadeOut(dots), Indicate(mi, color=PINK, scale_factor=1.25), run_time=0.5)
        dn = T("day and night", 28, TEXT, weight=BOLD).move_to([3.5, -3.3, 0])
        self.at("day and night")
        self.play(FadeIn(dn, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def stalk_rows(base, L, d, water, n=8, cw=0.8):
    """a stalk made of rows of two small walled cells; d = droop (0 straight), water = vacuole size (0..1)."""
    dd, f = d.get_value(), water.get_value()
    N = 60
    s = np.linspace(0, L, N)
    th = np.pi / 2 - dd * 1.3 * (s / L) ** 1.6
    ds = L / (N - 1)
    x = base[0] + np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * ds)])
    y = base[1] + np.concatenate([[0], np.cumsum(np.sin(th[:-1]) * ds)])
    rh = L / n
    g = VGroup()
    for i in range(n):
        si = (i + 0.5) * rh
        px, py, pt = np.interp(si, s, x), np.interp(si, s, y), np.interp(si, s, th)
        row = VGroup()
        for off in (-cw / 2, cw / 2):
            wallr = Rectangle(width=cw, height=rh * 0.96, stroke_color=ORANGE, stroke_width=3.5)
            vac = Rectangle(width=cw * 0.8 * f, height=rh * 0.8 * f, stroke_width=0, fill_color=BLUE, fill_opacity=0.5)
            c = VGroup(wallr, vac).shift(RIGHT * off)
            row.add(c)
        row.rotate(pt - np.pi / 2, about_point=ORIGIN).move_to([px, py, 0])
        g.add(row)
    return g


class S05Vacuole(SpokenScene):
    """the third added part: the large central vacuole fills, presses on the wall, and holds the plant firm."""

    def construct(self):
        K, X, Y = 1.15, -3.25, -0.3
        P = Cell("plant", X, Y, K)
        P.fill_basic(); P.add_wall(); P.add_chloroplasts()
        tp2 = T("plant cell", 28).move_to([X, 3.3, 0])
        self.add(P.out, *P.parts.values(), tp2)
        self.at("third part")
        self.play(*[FadeOut(P.parts[k]) for k in ("nucleus", "mito", "er", "cytoplasm", "chloroplast")], run_time=0.8)
        small = P.parts["vacuole"]
        inner_w, inner_h = CW * K - 0.5, CH * K - 0.5
        big = RoundedRectangle(corner_radius=0.35, width=inner_w * 0.8, height=inner_h * 0.8, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.3).move_to(P.pt(0, 0))
        cv = chip("large central vacuole", BLUE, 28).move_to([3.4, 1.9, 0])
        lead = Line(cv.get_left() + LEFT * 0.05, P.pt(1.55, 1.2) + [0, 0, 0], color=BLUE, stroke_width=2.5)
        big_edge = P.pt(0.8 * (CW / 2 - 0.25) * 1.0, 1.2)
        lead = Line(cv.get_left() + LEFT * 0.05, np.array([P.pt(0, 0)[0] + inner_w * 0.4 - 0.1, P.pt(0, 1.2)[1], 0]), color=BLUE, stroke_width=2.5)
        self.at("one big")
        self.play(ReplacementTransform(small, big), FadeIn(cv, shift=LEFT * 0.2), Create(lead), run_time=1.4)
        self.at("fills most")
        self.play(Indicate(big, color=BLUE, scale_factor=1.04), run_time=0.8)
        wt = T("water", 28, BLUE).move_to([3.4, 0.5, 0])
        self.at("stores water")
        self.play(FadeIn(wt, shift=LEFT * 0.2), run_time=0.5)

        # water moves in, the vacuole fills and presses
        drops = VGroup(*[Dot([P.pt(2.35, 0)[0] + 0.9, P.pt(0, dy)[1], 0], radius=0.15, color=BLUE) for dy in (1.2, 0.0, -1.2)])
        fb = RoundedRectangle(corner_radius=0.35, width=(CW * K - 0.3) - 0.1, height=(CH * K - 0.3) - 0.1, stroke_color=BLUE,
                              stroke_width=4, fill_color=BLUE, fill_opacity=0.55).move_to(P.pt(0, 0))
        self.at("water moves")
        self.play(FadeIn(drops), run_time=0.4)
        self.play(*[d.animate.move_to(P.pt(0.3, dy)).scale(1.0) for d, dy in zip(drops, (1.2, 0.0, -1.2))], run_time=1.3)
        self.play(FadeOut(drops), run_time=0.3)
        self.at("vacuole fills")
        self.play(Transform(big, fb), run_time=1.0)
        # pressure arrows
        out_arrows, back_arrows = VGroup(), VGroup()
        for (px, py, dx, dy) in ((0, 1, 0, 1), (0, -1, 0, -1), (1, 0, 1, 0), (-1, 0, -1, 0)):
            cx0 = P.pt(0, 0)
            ex = CW * K / 2 * abs(dx) + 0.0
            ey = CH * K / 2 * abs(dy)
            base_pt = cx0 + np.array([dx * (CW * K / 2 - 0.05), dy * (CH * K / 2 - 0.05), 0])
            out_arrows.add(arr(base_pt - np.array([dx, dy, 0]) * 0.75, base_pt - np.array([dx, dy, 0]) * 0.02, BLUE, w=6))
            wall_pt = cx0 + np.array([dx * (CW * K / 2 + 0.3), dy * (CH * K / 2 + 0.3), 0])
            if dx != 0:
                back_arrows.add(arr(wall_pt + np.array([dx, dy, 0]) * 0.7, wall_pt, ORANGE, w=6))
        pr = T("presses out", 26, BLUE).move_to([3.4, -0.6, 0])
        self.at("full vacuole presses")
        self.play(LaggedStart(*[GrowArrow(a) for a in out_arrows], lag_ratio=0.15), FadeIn(pr), run_time=1.0)
        pb = T("pushes back", 26, ORANGE).move_to([3.4, -1.5, 0])
        self.at("pushes back")
        self.play(LaggedStart(*[GrowArrow(a) for a in back_arrows], lag_ratio=0.15), FadeIn(pb), run_time=1.0)
        firm = T("firm", 40, TEXT, weight=BOLD).move_to([3.4, -2.6, 0])
        self.at("gets firm")
        self.play(FadeIn(firm, shift=UP * 0.15), run_time=0.6)

        # a stalk of firm cells
        d, wtr = ValueTracker(0.0), ValueTracker(1.0)
        base = np.array([3.0, -3.4, 0])
        stalk = always_redraw(lambda: stalk_rows(base, 5.3, d, wtr))
        sl = T("firm stalk", 30, TEXT, weight=BOLD).move_to([3.0, 2.6, 0])
        self.at("Many firm cells")
        self.play(FadeOut(VGroup(cv, lead, wt, pr, pb, firm)), run_time=0.5)
        self.add(stalk)
        self.play(FadeIn(stalk), run_time=0.6)
        self.at("firm stalk")
        self.play(FadeIn(sl), run_time=0.4)
        limp = T("limp", 30, RED, weight=BOLD).move_to([3.0, 2.6, 0])
        self.at("lose water")
        self.play(wtr.animate.set_value(0.3), big.animate.scale(0.45).set_fill(BLUE, 0.3), FadeOut(VGroup(out_arrows, back_arrows)),
                  run_time=1.6)
        self.at("goes limp")
        self.play(d.animate.set_value(1.0), FadeOut(sl), FadeIn(limp), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """plant: stiff walls and full vacuoles; you: no walls, a skeleton; the three added parts."""

    def construct(self):
        head = T("How does a plant stand up without a skeleton?", 34, font=TITLE_FONT).move_to([0, 3.2, 0])
        fit(head, max_w=12.2)
        self.play(Write(head), run_time=1.8)

        # plant cell icon
        pc = np.array([-3.4, 0.55, 0])
        wall = RoundedRectangle(corner_radius=0.3, width=3.2, height=3.2, stroke_color=ORANGE, stroke_width=10).move_to(pc)
        vac = RoundedRectangle(corner_radius=0.3, width=2.7, height=2.7, stroke_color=BLUE, stroke_width=3,
                               fill_color=BLUE, fill_opacity=0.45).move_to(pc)
        ob = VGroup(*[arr(pc + np.array([dx, dy, 0]) * 0.55, pc + np.array([dx, dy, 0]) * 1.2, BLUE, w=7) for dx, dy in
                      ((0, 1), (0, -1), (1, 0), (-1, 0))])
        pl = T("plant cell", 28).move_to([-3.4, 2.5, 0])
        cap_w = T("stiff wall", 26, ORANGE).move_to([-3.4, -1.45, 0])
        cap_v = T("full vacuole", 26, BLUE).move_to([-3.4, -1.9, 0])
        self.at("stiff walls")
        self.play(FadeIn(pl), Create(wall), FadeIn(cap_w), run_time=1.0)
        self.at("full vacuoles press")
        self.play(FadeIn(vac), FadeIn(cap_v), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in ob], lag_ratio=0.15), run_time=0.8)

        # your body: no walls, a skeleton
        body = RoundedRectangle(corner_radius=0.25, width=3.6, height=3.5, stroke_color=GREY, stroke_width=4).move_to([3.4, 0.55, 0])
        bl = T("your body", 28).move_to([3.4, 2.5, 0])
        cell = RoundedRectangle(corner_radius=0.5, width=1.8, height=1.2, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.15).move_to([3.4, -0.1, 0])
        nowall = T("your cells: no walls", 26, RED).move_to([3.4, -1.45, 0])
        self.at("Your cells have no walls")
        self.play(FadeIn(bl), Create(body), run_time=0.6)
        self.play(FadeIn(cell), FadeIn(nowall, shift=UP * 0.1), run_time=0.7)
        sk = chip("skeleton of bones", TEXT, 26).move_to([3.4, 1.35, 0])
        self.at("skeleton of bones")
        self.play(FadeIn(sk, shift=DOWN * 0.1), run_time=0.7)

        # the three added parts
        add = T("plant cells add", 26, GREY).move_to([0, -2.55, 0])
        c1 = chip("cell wall", ORANGE, 26)
        c2 = chip("chloroplasts", GREEN, 26)
        c3 = chip("large central vacuole", BLUE, 26)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.4).move_to([0, -3.3, 0])
        self.at("Plant cells add")
        self.play(FadeIn(add), run_time=0.4)
        self.at("a cell wall")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("chloroplasts", nth=0)
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.5)
        self.at("central vacuole")
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Full vacuoles press on stiff walls. The cell gets firm."
