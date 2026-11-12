"""Cells divide: Copy first, then share (chapter 1 film, level-up)

COLOUR MAP: chromosomes RED, BLUE, GREEN, YELLOW; cell membrane PEACH; nucleus pale GREY;
counters white on charcoal. All cells are schematic cartoons.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PEACH = "#F2B38C"
NUC = "#B8BCC4"
CHAR = "#2B2F36"
CH = [RED, BLUE, GREEN, YELLOW]
CX, CY = -0.5, 0.0
CW0, CH0 = 6.4, 5.0      # cell before it grows
CW1, CH1 = 7.0, 5.5      # cell after growing in interphase
NR0, NR1 = 2.0, 2.15
XS = [-1.4, -0.45, 0.5, 1.45]
YS = [0.1, -0.1, 0.1, -0.1]
HS = [2.3, 3.0, 2.8, 2.2]
ROW_Y = [1.875, 0.625, -0.625, -1.875]
SCATTER = [(-2.0, 1.2), (1.6, 1.4), (-1.4, -1.3), (1.9, -0.9)]
STAGES = ["prophase", "metaphase", "anaphase", "telophase"]
PY = [y * 0.7 for y in [1.875, 0.625, -0.625, -1.875]]
DAUGH = [CX - 1.9, CX + 1.9]
COMPACT_Y = [0.99, 0.33, -0.33, -0.99]


# ------------------------------------------------------------------ helpers
def bob(m, amp=0.05, sp=1.3, ph=0.0):
    m._t = ph

    def u(mob, dt):
        mob._t += dt
        mob.shift(np.array([0.6 * amp * sp * np.cos(0.8 * sp * mob._t + 1.0),
                            amp * sp * np.cos(sp * mob._t), 0]) * dt)
    m.add_updater(u)
    return m


def motes(cx, cy, rx, ry, n=12, color=PEACH, seed=1):
    import random
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        a, r = rng.uniform(0, TAU), rng.uniform(0, 0.9)
        d = Dot(radius=0.05, color=color).set_opacity(0.45)
        d.move_to([cx + rx * r * np.cos(a), cy + ry * r * np.sin(a), 0])
        d.v = np.array([rng.uniform(-0.35, 0.35), rng.uniform(-0.35, 0.35), 0])

        def u(m, dt, cx=cx, cy=cy, rx=rx, ry=ry):
            m.shift(m.v * dt)
            p = m.get_center()
            if ((p[0] - cx) / rx) ** 2 + ((p[1] - cy) / ry) ** 2 > 0.85:
                m.v = -m.v
        d.add_updater(u)
        g.add(d)
    return g


def cell_mob(w, h, cx=CX, cy=CY):
    return Ellipse(width=w, height=h, stroke_color=PEACH, stroke_width=6,
                   fill_color=PEACH, fill_opacity=0.10).move_to([cx, cy, 0])


def nuc_mob(r, cx=CX, cy=CY):
    return Circle(radius=r, stroke_color=NUC, stroke_width=4,
                  fill_color=NUC, fill_opacity=0.20).move_to([cx, cy, 0])


def thread(x, y, h, color, w=6):
    return ParametricFunction(lambda t: np.array([x + 0.07 * np.sin(2.4 * t), y + t, 0]),
                              t_range=[-h / 2, h / 2, 0.05], color=color, stroke_width=w)


def singles(cx=CX, cy=CY, k=1.0):
    return [thread(cx + XS[i] * k, cy + YS[i] * k, HS[i] * k, CH[i]) for i in range(4)]


def pair(i, cx=CX, cy=CY, k=1.0, sep=0.13):
    x, y, h = cx + XS[i] * k, cy + YS[i] * k, HS[i] * k
    a = thread(x - sep * k, y, h, CH[i])
    b = thread(x + sep * k, y, h, CH[i])
    d = Dot([x, y, 0], radius=0.09, color=TEXT)
    return VGroup(a, b, d)


def counter(label, val, y, extra=""):
    r = RoundedRectangle(corner_radius=0.1, width=3.5, height=0.62, fill_color=CHAR, fill_opacity=1,
                         stroke_color=GREY, stroke_width=1.5)
    t = T(f"{label}: {val}{extra}", 24)
    g = VGroup(r, t)
    return g.move_to([4.95, y, 0])


def cards(y):
    r = RoundedRectangle(corner_radius=0.1, width=3.5, height=0.62, fill_color=CHAR, fill_opacity=1,
                         stroke_color=GREY, stroke_width=1.5)
    return VGroup(r, T("?", 34, YELLOW, weight=BOLD)).move_to([4.95, y, 0])


def strip(lit=0):
    g = VGroup()
    for i, nm in enumerate(STAGES):
        on = i < lit
        r = RoundedRectangle(corner_radius=0.08, width=3.0, height=0.56,
                             stroke_color=YELLOW if on else GREY, stroke_width=2.5,
                             fill_color=YELLOW, fill_opacity=0.3 if on else 0.0)
        t = T(nm, 24, YELLOW if on else TEXT)
        g.add(VGroup(r, t))
    g.arrange(RIGHT, buff=0.2).move_to([0, -3.4, 0])
    return g


def light(box):
    return [box[0].animate.set_fill(YELLOW, 0.3).set_stroke(YELLOW), box[1].animate.set_color(YELLOW)]


def chev(color, apex, pos, s=1.0):
    m = VMobject().set_points_as_corners([[-apex * .18, .55, 0], [apex * .18, 0, 0], [-apex * .18, -.55, 0]])
    m.set_stroke(color, 16 * max(s, 0.7))
    m.scale(s).move_to([pos[0], pos[1], 0])
    return m


def xmark(color, pos, s=0.85):
    left = chev(color, 1, (-.2 * s, 0), s)
    right = chev(color, -1, (.2 * s, 0), s)
    d = Dot(radius=0.1 * s, color=color)
    g = VGroup(left, right, d)
    g.move_to([pos[0], pos[1], 0])
    return g


def tick(pos):
    m = VMobject().set_points_as_corners([[-.14, 0, 0], [-.03, -.12, 0], [.16, .16, 0]])
    return m.set_stroke(TEXT, 7).move_to([pos[0], pos[1], 0])


def knee(scrape=1.0, healed=False):
    skin = Ellipse(width=8, height=4.8, stroke_color=PEACH, stroke_width=6, fill_color=PEACH, fill_opacity=0.35).move_to([0, 0.5, 0])
    cap = Arc(radius=1.6, start_angle=PI * 1.1, angle=PI * 0.8, stroke_color=PEACH, stroke_width=5, fill_opacity=0).move_to([0, 1.0, 0])
    if healed:
        sc = Ellipse(width=2.2 * scrape, height=1.3 * scrape, stroke_color="#F6A5B0", stroke_width=3,
                     fill_color="#F6A5B0", fill_opacity=0.7).move_to([0, 0.3, 0])
    else:
        sc = Ellipse(width=2.2 * scrape, height=1.3 * scrape, stroke_color=RED, stroke_width=4,
                     fill_color=RED, fill_opacity=0.55).move_to([0, 0.3, 0])
    return VGroup(skin, cap, sc)


def tissue():
    rows, cols = [1.5, 0.0, -1.5], [-5.8, -4.6, -3.4, -2.2, 2.2, 3.4, 4.6, 5.8]
    cells = {}
    for ri, y in enumerate(rows):
        for ci, x in enumerate(cols):
            cells[(ri, ci)] = RoundedRectangle(corner_radius=0.16, width=1.05, height=1.3, stroke_color=PEACH,
                                               stroke_width=4, fill_color=PEACH, fill_opacity=0.22).move_to([x, y, 0])
    return cells


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "How Cells Divide"
    TITLE = "Copy First, Then Share"


class S01Hook(SpokenScene):
    def construct(self):
        k = knee(1.0)
        bob(k, 0.04)
        self.play(FadeIn(k, scale=0.9), run_time=1.3)
        sq = VGroup(*[Square(0.5, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0)
                      for _ in range(14)]).arrange(RIGHT, buff=0.3).move_to([0, -3.35, 0])
        self.at("and new skin")
        self.play(FadeIn(sq), run_time=0.4)
        newsc = Ellipse(width=0.4, height=0.25, stroke_color="#F6A5B0", stroke_width=3,
                        fill_color="#F6A5B0", fill_opacity=0.7).move_to([0, 0.3, 0])
        self.play(LaggedStart(*[s.animate.set_fill(TEAL, 0.7) for s in sq], lag_ratio=0.15, run_time=2.0),
                  Transform(k[2], newsc, run_time=2.0))
        self.at("about")
        lab = T("1 to 2 weeks", 34, TEAL, weight=BOLD).move_to([0, -2.6, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.6)
        self.at("where did those")
        q = T("?", 110, YELLOW, weight=BOLD).move_to([0, 0.35, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.8)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.finish()


class S02Answer(SpokenScene):
    def construct(self):
        k = knee(0.15, healed=True)
        cells = tissue()
        allc = VGroup(*cells.values())
        allc.scale(0.15, about_point=[0, 0.3, 0]).set_opacity(0)
        self.add(k, allc)
        self.play(k.animate.scale(6, about_point=[0, 0.3, 0]).set_opacity(0),
                  allc.animate.scale(1 / 0.15, about_point=[0, 0.3, 0]).set_opacity(1), run_time=1.8)
        self.remove(k)
        for c in cells.values():
            bob(c, 0.03, ph=np.random.rand() * 6)
        self.at("skin cells")
        back = [cells[(r, c)] for r in range(3) for c in (1, 6)]
        lab_d = [T("divide", 32, YELLOW, weight=BOLD).move_to([-4.6, 2.85, 0]),
                 T("divide", 32, YELLOW, weight=BOLD).move_to([4.6, 2.85, 0])]
        self.play(*[c.animate.set_stroke(YELLOW) for c in back], *[FadeIn(l) for l in lab_d], run_time=0.8)
        self.at("each one")
        news = []
        pairs = []
        for c in back:
            p = c.get_center()
            c1 = RoundedRectangle(corner_radius=0.12, width=0.5, height=1.3, stroke_color=YELLOW, stroke_width=4,
                                  fill_color=PEACH, fill_opacity=1).move_to(p + LEFT * 0.28)
            c2 = c1.copy().move_to(p + RIGHT * 0.28)
            pairs.append(VGroup(c1, c2))
            news.append(ReplacementTransform(c, VGroup(c1, c2)))
        self.play(*news, run_time=1.0)
        self.play(*[Indicate(p, color=YELLOW) for p in pairs], run_time=0.8)
        self.play(*[c.animate.set_stroke(PEACH) for p in pairs for c in p], FadeOut(VGroup(*lab_d)), run_time=0.6)
        self.at("some cells")
        front = [cells[(r, c)] for r in range(3) for c in (3, 4)]
        lab_c = T("crawl in", 32, YELLOW, weight=BOLD).move_to([0, 2.85, 0])
        self.play(*[c.animate.set_stroke(YELLOW) for c in front], FadeIn(lab_c), run_time=0.8)
        self.at("crawl")
        anims = []
        for r in range(3):
            anims.append(cells[(r, 3)].animate.stretch_to_fit_width(1.9).move_to([-1.775, cells[(r, 3)].get_y(), 0]))
            anims.append(cells[(r, 4)].animate.stretch_to_fit_width(1.9).move_to([1.775, cells[(r, 4)].get_y(), 0]))
        self.play(*anims, run_time=2.2)
        self.at("every new cell")
        lab_n = T("every new cell comes from a cell", 32, TEXT).move_to([0, -2.95, 0])
        self.play(FadeOut(lab_c), *[c.animate.set_stroke(PEACH) for c in front], FadeIn(lab_n), run_time=0.6)
        self.play(*[Indicate(p, color=YELLOW) for p in pairs[:3] + pairs[3:]], run_time=1.5)
        self.finish()


class S03Question(SpokenScene):
    def construct(self):
        px, py = -3.6, 0.0
        parent = cell_mob(4.4, 3.6, px, py)
        nuc = nuc_mob(0.9, px, py + 0.2)
        mt = motes(px, py, 2.0, 1.6, 10)
        self.play(FadeIn(parent), FadeIn(nuc), FadeIn(mt), run_time=1.0)
        q = T("?", 90, YELLOW, weight=BOLD).move_to([px, 2.5, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.at("most cells")
        full = T("full set", 32, YELLOW, weight=BOLD).move_to([px, -1.2, 0])
        self.play(FadeIn(full), nuc.animate.set_stroke(YELLOW, 6), run_time=0.9)
        self.at("when one cell")
        d1 = cell_mob(3.0, 2.6, 3.4, 1.7)
        d2 = cell_mob(3.0, 2.6, 3.4, -1.7)
        a1 = Arrow([-1.2, 0.3, 0], [1.8, 1.5, 0], color=TEXT, buff=0.1, stroke_width=6)
        a2 = Arrow([-1.2, -0.3, 0], [1.8, -1.5, 0], color=TEXT, buff=0.1, stroke_width=6)
        self.play(Create(a1), Create(a2), FadeIn(d1, scale=0.8), FadeIn(d2, scale=0.8), run_time=1.5)
        self.at("how does each")
        boxes = VGroup()
        for yy in (1.7, -1.7):
            bx = DashedVMobject(Rectangle(width=2.2, height=1.0, color=YELLOW, stroke_width=4), num_dashes=24).move_to([3.4, yy + 0.2, 0])
            lb = T("full set?", 28, YELLOW).move_to([3.4, yy + 0.2, 0])
            boxes.add(bx, lb)
        self.play(FadeIn(boxes, lag_ratio=0.3), run_time=1.5)
        self.play(Indicate(boxes, color=YELLOW, scale_factor=1.08), run_time=1.2)
        self.finish()


class S04Chromosomes(SpokenScene):
    def construct(self):
        px, py = -3.6, 0.0
        parent = cell_mob(4.4, 3.6, px, py)
        nuc = nuc_mob(0.9, px, py + 0.2)
        d1, d2 = cell_mob(3.0, 2.6, 3.4, 1.7), cell_mob(3.0, 2.6, 3.4, -1.7)
        mt = motes(CX, CY, 2.8, 2.2, 14)
        self.add(parent, nuc, d1, d2)
        self.play(FadeOut(VGroup(d1, d2)), Transform(parent, cell_mob(CW0, CH0)), Transform(nuc, nuc_mob(NR0)),
                  FadeIn(mt), run_time=1.5)
        self.at("chromosomes")
        th = singles()
        for t in th:
            t.shift(UP * 0.8).set_opacity(0)
        self.add(*th)
        self.play(LaggedStart(*[t.animate.shift(DOWN * 0.8).set_opacity(1) for t in th], lag_ratio=0.3), run_time=1.6)
        for t in th:
            bob(t, 0.04, ph=np.random.rand() * 6)
        self.at("inside the nucleus")
        lab = T("nucleus", 32, TEXT).move_to([-5.4, 1.3, 0])
        ln = Line(lab.get_right() + RIGHT * 0.1, [CX - 1.6, 1.3, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(lab), Create(ln), run_time=0.8)
        self.at("our model cell")
        c1, c2 = counter("chromosomes", 4, 3.1), counter("copies", 4, 2.35)
        self.play(FadeOut(lab), FadeOut(ln), FadeIn(c1, shift=LEFT * 0.3), FadeIn(c2, shift=LEFT * 0.3), run_time=0.9)
        self.at("four of them")
        self.play(Indicate(c1, color=YELLOW, scale_factor=1.08), run_time=0.8)
        for nm, i in (("red", 0), ("blue", 1), ("green", 2), ("yellow", 3)):
            self.at(nm, lead=0.1)
            self.play(Indicate(th[i], color=CH[i], scale_factor=1.15), run_time=0.45)
        note = T("typical human body cell:\n46 chromosomes", 24, TEXT, line_spacing=0.8).move_to([4.95, 1.2, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.finish()


class S05Cycle(SpokenScene):
    def construct(self):
        s = 0.62
        cell = cell_mob(CW0, CH0)
        nuc = nuc_mob(NR0)
        th = VGroup(*singles())
        world = VGroup(cell, nuc, th)
        mt = motes(CX, CY, 2.8 * s, 2.2 * s, 8)
        self.add(world, mt)
        self.play(world.animate.scale(s, about_point=[CX, CY, 0]), run_time=1.2)
        R = 2.9
        C = np.array([CX, CY, 0])
        interphase = Arc(radius=R, start_angle=60 * DEGREES, angle=290 * DEGREES, color=TEAL, stroke_width=9).move_arc_center_to(C)
        mitosis = Arc(radius=R, start_angle=-10 * DEGREES, angle=70 * DEGREES, color=YELLOW, stroke_width=9).move_arc_center_to(C)
        self.at("cell cycle")
        ring = Circle(radius=R, color=TEXT, stroke_width=6).move_to(C)
        self.play(Create(ring), run_time=1.3)
        self.at("two main parts")
        self.play(ReplacementTransform(ring, VGroup(interphase, mitosis)), run_time=1.0)
        tr = ValueTracker(0)
        dot = Dot(radius=0.16, color=TEXT)
        path = Circle(radius=R).move_to(C).rotate(60 * DEGREES, about_point=C)
        dot.add_updater(lambda m: m.move_to(path.point_from_proportion(tr.get_value() % 1.0)))
        dot.move_to(path.point_from_proportion(0))
        self.at("interphase")
        l1 = T("interphase", 34, TEAL, weight=BOLD).move_to([-5.2, 0, 0])
        self.play(FadeIn(l1), FadeIn(dot), run_time=0.6)
        self.play(tr.animate.set_value(0.8), rate_func=linear, run_time=2.2)
        self.at("then comes mitosis")
        l2 = T("mitosis", 34, YELLOW, weight=BOLD).move_to([4.5, 1.6, 0])
        self.play(FadeIn(l2), run_time=0.6)
        self.play(tr.animate.set_value(1.0), rate_func=linear, run_time=1.4)
        self.at("when the cell divides")
        nt = T("schematic, not to scale", 26, TEXT).move_to([4.2, -3.2, 0])
        self.play(FadeIn(nt), tr.animate.set_value(1.8), rate_func=linear, run_time=3.0)
        self.finish()


class S06Interphase(SpokenScene):
    def construct(self):
        s = 0.62
        cell = cell_mob(CW0, CH0)
        nuc = nuc_mob(NR0)
        th = singles()
        world = VGroup(cell, nuc, *th)
        mt = motes(CX, CY, 2.8, 2.2, 14)
        world.scale(s, about_point=[CX, CY, 0])
        self.add(world)
        self.play(world.animate.scale(1 / s, about_point=[CX, CY, 0]), FadeIn(mt), run_time=1.0)
        for t in th:
            bob(t, 0.04, ph=np.random.rand() * 6)
        c1 = counter("chromosomes", 4, 3.1, " ?")
        c2 = counter("copies", 4, 2.35)
        card = cards(2.35)
        self.at("busy")
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(card), run_time=0.8)
        self.at("grows bigger")
        self.play(Transform(cell, cell_mob(CW1, CH1)), Transform(nuc, nuc_mob(NR1)), run_time=1.6)
        self.at("copies every one", lead=0.3)
        A, B, D = [], [], []
        for i in range(4):
            a = th[i]
            b = a.copy()
            self.add(b)
            d = Dot([CX + XS[i], CY + YS[i], 0], radius=0.09, color=TEXT)
            A.append(a); B.append(b); D.append(d)
            self.play(a.animate.shift(LEFT * 0.13), b.animate.shift(RIGHT * 0.13), FadeIn(d, scale=0.3), run_time=0.8)
            if i < 3:
                self.wait(0.1)
            bob(b, 0.04, ph=np.random.rand() * 6)
        self.at("joined to it")
        self.play(*[Indicate(d, color=YELLOW, scale_factor=2.0) for d in D], run_time=1.2)
        self.at("both stay thin")
        self.play(*[Indicate(t, color=CH[i % 4], scale_factor=1.1) for i, t in enumerate(A)], run_time=1.5)
        self.finish()


def interphase_world(mt_seed=3):
    cell = cell_mob(CW1, CH1)
    nuc = nuc_mob(NR1)
    P = [pair(i) for i in range(4)]
    return cell, nuc, P


class S07Predict(SpokenScene):
    def construct(self):
        cell, nuc, P = interphase_world()
        mt = motes(CX, CY, 2.8, 2.2, 14)
        c1 = counter("chromosomes", 4, 3.1, " ?")
        c2 = counter("copies", 4, 2.35)
        card = cards(2.35)
        self.add(cell, nuc, mt, *P, c1, c2, card)
        self.at("look at the counter", lead=0)
        self.play(Indicate(c1, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.at("before copying")
        self.play(*[p[0].animate.shift(RIGHT * 0.13) for p in P], *[p[1].animate.shift(LEFT * 0.13) for p in P],
                  *[FadeOut(p[2]) for p in P], run_time=1.2)
        self.at("now each one")
        self.play(*[p[0].animate.shift(LEFT * 0.13) for p in P], *[p[1].animate.shift(RIGHT * 0.13) for p in P],
                  *[FadeIn(p[2]) for p in P], run_time=1.2)
        for p in P:
            bob(p, 0.04, ph=np.random.rand() * 6)
        self.at("does the cell")
        q = RoundedRectangle(corner_radius=0.12, width=3.5, height=2.4, fill_color=CHAR, fill_opacity=1,
                             stroke_color=YELLOW, stroke_width=3)
        qt = T("After copying:\n4 chromosomes\nor 8?", 28, YELLOW, line_spacing=0.9)
        qc = VGroup(q, qt.move_to(q)).move_to([4.95, -1.0, 0])
        self.play(FadeIn(qc, shift=LEFT * 0.5), run_time=0.8)
        self.at("or eight", lead=0.3)
        self.play(*[Indicate(p, color=YELLOW, scale_factor=1.05) for p in P], run_time=1.5)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        cell, nuc, P = interphase_world()
        mt = motes(CX, CY, 2.8, 2.2, 14)
        c1 = counter("chromosomes", 4, 3.1, " ?")
        card = cards(2.35)
        q = RoundedRectangle(corner_radius=0.12, width=3.5, height=2.4, fill_color=CHAR, fill_opacity=1,
                             stroke_color=YELLOW, stroke_width=3)
        qt = T("After copying:\n4 chromosomes\nor 8?", 28, YELLOW, line_spacing=0.9)
        qc = VGroup(q, qt.move_to(q)).move_to([4.95, -1.0, 0])
        self.add(cell, nuc, mt, *P, c1, card, qc)
        tr = ValueTracker(0.001)
        ring = Circle(radius=0.38, color=GREY, stroke_width=5).move_to([4.95, -3.0, 0])
        arc = always_redraw(lambda: Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * tr.get_value(),
                                        color=YELLOW, stroke_width=7).move_arc_center_to([4.95, -3.0, 0]))
        self.add(ring, arc)
        self.play(tr.animate.set_value(1.0), rate_func=linear, run_time=4.6)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        cell, nuc, P = interphase_world()
        mt = motes(CX, CY, 2.8, 2.2, 14)
        c1 = counter("chromosomes", 4, 3.1, " ?")
        c2 = counter("copies", 4, 2.35)
        card = cards(2.35)
        q = RoundedRectangle(corner_radius=0.12, width=3.5, height=2.4, fill_color=CHAR, fill_opacity=1,
                             stroke_color=YELLOW, stroke_width=3)
        qc = VGroup(q, T("After copying:\n4 chromosomes\nor 8?", 28, YELLOW, line_spacing=0.9).move_to(q)).move_to([4.95, -1.0, 0])
        self.add(cell, nuc, mt, *P, c1, c2, card, qc)
        n1 = counter("chromosomes", 4, 3.1)
        n2 = counter("copies", 8, 2.35)
        self.play(FadeOut(qc, shift=UP * 0.5), FadeOut(card), Transform(c1, n1), Transform(c2, n2), run_time=1.2)
        self.at("a copied chromosome")
        red = P[0]
        orig = red.get_center().copy()
        others = VGroup(*P[1:])
        self.play(others.animate.set_opacity(0.2), red.animate.scale(1.5).move_to([CX, 0, 0]),
                  nuc.animate.set_opacity(0.5), run_time=1.5)
        self.at("one chromosome", lead=0.3)
        box = RoundedRectangle(corner_radius=0.2, width=1.1, height=4.9, stroke_color=TEXT, stroke_width=4).move_to([CX, 0, 0])
        one = T("one chromosome", 34, TEXT, weight=BOLD).move_to([CX - 0.0, -2.95, 0])
        self.play(Create(box), FadeIn(one), run_time=1.0)
        self.at("made of two")
        cl = T("copy", 32, YELLOW, weight=BOLD).move_to([CX - 4.7, 0.9, 0])
        cr = T("copy", 32, YELLOW, weight=BOLD).move_to([CX + 4.7, 0.9, 0])
        ll = Arrow(cl.get_right(), red[0].get_center() + UP * 0.9 + LEFT * 0.05, buff=0.1, color=YELLOW, stroke_width=4)
        lr = Arrow(cr.get_left(), red[1].get_center() + UP * 0.9 + RIGHT * 0.05, buff=0.1, color=YELLOW, stroke_width=4)
        self.play(FadeIn(cl), Create(ll), run_time=0.8)
        self.play(FadeIn(cr), Create(lr), run_time=0.8)
        self.at("joined together", lead=0.4)
        self.play(Indicate(red[2], color=YELLOW, scale_factor=3), run_time=1.5)
        self.at("so the cell")
        self.play(FadeOut(VGroup(cl, cr, ll, lr, box, one)), others.animate.set_opacity(1),
                  red.animate.scale(1 / 1.5).move_to(orig), nuc.animate.set_opacity(1), run_time=1.4)
        for p in P:
            bob(p, 0.04, ph=np.random.rand() * 6)
        self.at("four chromosomes", lead=0.1)
        self.play(Indicate(c1, color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.at("eight")
        self.play(Indicate(c2, color=YELLOW, scale_factor=1.1), run_time=1.2)
        self.finish()


class S10Prophase(SpokenScene):
    def construct(self):
        cell, nuc, P = interphase_world()
        mt = motes(CX, CY, 2.8, 2.2, 14)
        c1, c2 = counter("chromosomes", 4, 3.1), counter("copies", 8, 2.35)
        self.add(cell, nuc, mt, *P, c1, c2)
        for p in P:
            bob(p, 0.04, ph=np.random.rand() * 6)
        self.at("now mitosis")
        st = strip(0)
        self.play(FadeIn(st, shift=UP * 0.3), run_time=1.0)
        self.at("its four stages", lead=0.1)
        self.play(LaggedStart(*[Indicate(b, color=YELLOW, scale_factor=1.06) for b in st], lag_ratio=0.5), run_time=2.4)
        self.at("in prophase", lead=0.1)
        self.play(*light(st[0]), run_time=0.7)
        self.at("the chromosomes coil")
        Xs = [xmark(CH[i], (CX + SCATTER[i][0], CY + SCATTER[i][1])) for i in range(4)]
        self.play(*[ReplacementTransform(P[i], Xs[i]) for i in range(4)], FadeOut(nuc), run_time=2.6)
        for x in Xs:
            bob(x, 0.05, ph=np.random.rand() * 6)
        self.at("each pair")
        self.play(*[Indicate(x, color=CH[i], scale_factor=1.25) for i, x in enumerate(Xs)], run_time=2.0)
        self.finish()


def stage_base(scene, lit, counters=True):
    cell = cell_mob(CW1, CH1)
    mt = motes(CX, CY, 2.8, 2.2, 14)
    st = strip(lit)
    scene.add(cell, mt, st)
    cs = []
    if counters:
        cs = [counter("chromosomes", 4, 3.1), counter("copies", 8, 2.35)]
        scene.add(*cs)
    return cell, st, cs


class S11Metaphase(SpokenScene):
    def construct(self):
        cell, st, cs = stage_base(self, 1)
        Xs = [xmark(CH[i], (CX + SCATTER[i][0], CY + SCATTER[i][1])) for i in range(4)]
        self.add(*Xs)
        for x in Xs:
            bob(x, 0.05, ph=np.random.rand() * 6)
        self.at("metaphase", lead=0.1)
        self.play(*light(st[1]), run_time=0.7)
        self.at("line up in a row", lead=0.1)
        mid = DashedLine([CX, 2.7, 0], [CX, -2.7, 0], color=TEXT, stroke_width=3)
        self.play(Create(mid), run_time=0.9)
        for x in Xs:
            x.clear_updaters()
        self.play(*[x.animate.move_to([CX, ROW_Y[i], 0]) for i, x in enumerate(Xs)], run_time=2.6)
        for x in Xs:
            bob(x, 0.03, ph=np.random.rand() * 6)
        self.at("red", lead=0.1)
        for i in range(4):
            self.play(Indicate(Xs[i], color=CH[i], scale_factor=1.25), run_time=0.35)
        self.at("side by side")
        self.play(*[Indicate(x, scale_factor=1.12) for x in Xs], run_time=1.0)
        self.finish()


class S12Anaphase(SpokenScene):
    def construct(self):
        cell, st, cs = stage_base(self, 2)
        mid = DashedLine([CX, 2.7, 0], [CX, -2.7, 0], color=TEXT, stroke_width=3)
        Xs = [xmark(CH[i], (CX, ROW_Y[i])) for i in range(4)]
        self.add(mid, *Xs)
        self.at("anaphase", lead=0.1)
        self.play(*light(st[2]), run_time=0.7)
        self.at("the two copies")
        self.play(FadeOut(VGroup(*cs)), FadeOut(mid), *[x[0].animate.shift(LEFT * 0.2) for x in Xs],
                  *[x[1].animate.shift(RIGHT * 0.2) for x in Xs], *[FadeOut(x[2]) for x in Xs], run_time=1.2)
        self.at("pulled apart")
        self.play(*[x[0].animate.shift(LEFT * 0.7) for x in Xs], *[x[1].animate.shift(RIGHT * 0.7) for x in Xs], run_time=1.8)
        self.at("one copy of each")
        self.play(*[x[0].animate.move_to([CX - 2.1, PY[i], 0]).rotate(PI) for i, x in enumerate(Xs)],
                  *[x[1].animate.move_to([CX + 2.1, PY[i], 0]).rotate(PI) for i, x in enumerate(Xs)], run_time=2.6)
        self.play(*[Indicate(x[0], color=CH[i], scale_factor=1.2) for i, x in enumerate(Xs)],
                  *[Indicate(x[1], color=CH[i], scale_factor=1.2) for i, x in enumerate(Xs)], run_time=1.2)
        self.finish()


def pole_chevs():
    L = [chev(CH[i], -1, (CX - 2.1, PY[i]), 0.85) for i in range(4)]
    R = [chev(CH[i], 1, (CX + 2.1, PY[i]), 0.85) for i in range(4)]
    return L, R


class S13Telophase(SpokenScene):
    def construct(self):
        cell, st, _ = stage_base(self, 3, counters=False)
        L, R = pole_chevs()
        self.add(*L, *R)
        self.at("telophase", lead=0.1)
        self.play(*light(st[3]), run_time=0.7)
        self.at("two new nuclei")
        self.play(*[L[i].animate.scale(0.55).move_to([DAUGH[0], COMPACT_Y[i], 0]) for i in range(4)],
                  *[R[i].animate.scale(0.55).move_to([DAUGH[1], COMPACT_Y[i], 0]) for i in range(4)], run_time=1.4)
        nl, nr = nuc_mob(1.5, DAUGH[0]), nuc_mob(1.5, DAUGH[1])
        self.play(FadeIn(nl), FadeIn(nr), run_time=1.0)
        self.at("then the cell splits")
        d1, d2 = cell_mob(3.6, 4.0, DAUGH[0]), cell_mob(3.6, 4.0, DAUGH[1])
        self.play(ReplacementTransform(cell, VGroup(d1, d2)), run_time=2.6)
        self.at("daughter")
        l1 = T("daughter cell", 30, TEXT, weight=BOLD).move_to([DAUGH[0], -2.55, 0])
        l2 = T("daughter cell", 30, TEXT, weight=BOLD).move_to([DAUGH[1], -2.55, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.7)
        self.play(d1.animate.shift(LEFT * 0.0).set_stroke(YELLOW), d2.animate.set_stroke(YELLOW), run_time=0.8)
        self.finish()


class S14Count(SpokenScene):
    def construct(self):
        mt = motes(CX, CY, 3.2, 2.0, 12)
        d1, d2 = cell_mob(3.6, 4.0, DAUGH[0]), cell_mob(3.6, 4.0, DAUGH[1])
        nl, nr = nuc_mob(1.5, DAUGH[0]), nuc_mob(1.5, DAUGH[1])
        L = [chev(CH[i], -1, (DAUGH[0], COMPACT_Y[i]), 0.55) for i in range(4)]
        R = [chev(CH[i], 1, (DAUGH[1], COMPACT_Y[i]), 0.55) for i in range(4)]
        self.add(mt, d1, d2, nl, nr, *L, *R)
        for i, m in enumerate(L + R):
            bob(m, 0.03, ph=i)
        self.at("count each daughter", lead=0.3)
        self.wait(0.6)
        self.at("cell", lead=0.0)
        cl = counter("chromosomes", 4, -2.95).move_to([DAUGH[0], -2.95, 0])
        cr = counter("chromosomes", 4, -2.95).move_to([DAUGH[1], -2.95, 0])
        self.play(FadeIn(cl, shift=UP * 0.2), FadeIn(cr, shift=UP * 0.2), run_time=0.8)
        ticks = []
        for nm, i in (("red", 0), ("blue", 1), ("greens", 2), ("yellow", 3)):
            self.at(nm, lead=0.15)
            a, b = tick((DAUGH[0] + 0.7, COMPACT_Y[i])), tick((DAUGH[1] + 0.7, COMPACT_Y[i]))
            ticks += [a, b]
            self.play(Create(a), Create(b), run_time=0.3)
        self.at("four chromosomes", lead=0.1)
        self.play(Indicate(cl, color=YELLOW, scale_factor=1.1), Indicate(cr, color=YELLOW, scale_factor=1.1), run_time=1.2)
        self.at("that is the same set")
        par = cell_mob(2.6, 0.95, CX, 3.3).set_opacity(0.6)
        pt = M("4", 34, TEXT).move_to(par)
        eq = [T("=", 44, YELLOW, weight=BOLD).move_to([x, 2.5, 0]) for x in DAUGH]
        self.play(FadeIn(par), FadeIn(pt), run_time=0.8)
        self.play(*[FadeIn(e) for e in eq], run_time=0.8)
        self.play(Indicate(par, color=YELLOW, scale_factor=1.1), *[Indicate(e, scale_factor=1.3) for e in eq], run_time=1.5)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        lx, rx = -3.3, 3.3
        div = Line([0, 3.5, 0], [0, -3.5, 0], color=GREY, stroke_width=3)
        cl = cell_mob(5.6, 4.6, lx, -0.2)
        cr = cell_mob(5.6, 4.6, rx, -0.2)
        th = [thread(lx + XS[i] * 0.95, -0.2 + YS[i], HS[i] * 0.8, CH[i]) for i in range(4)]
        mt = VGroup(motes(lx, -0.2, 2.4, 1.9, 8, seed=5), motes(rx, -0.2, 2.4, 1.9, 8, seed=6))
        self.play(Create(div), FadeIn(cl), FadeIn(cr), FadeIn(mt), *[FadeIn(t) for t in th], run_time=1.4)
        for t in th:
            bob(t, 0.04, ph=np.random.rand() * 6)
        self.at("copy first")
        l1 = T("copy first", 36, YELLOW, weight=BOLD).move_to([lx, 2.95, 0])
        self.play(FadeIn(l1, shift=DOWN * 0.2), run_time=0.6)
        self.at("then share")
        l2 = T("then share", 36, YELLOW, weight=BOLD).move_to([rx, 2.95, 0])
        Xs = [xmark(CH[i], (rx, -0.2 + [1.5, 0.5, -0.5, -1.5][i]), 0.8) for i in range(4)]
        self.play(FadeIn(l2, shift=DOWN * 0.2), LaggedStart(*[FadeIn(x, scale=0.6) for x in Xs], lag_ratio=0.3), run_time=1.4)
        for x in Xs:
            bob(x, 0.03, ph=np.random.rand() * 6)
        self.at("copying makes")
        for i in range(4):
            b = th[i].copy()
            self.add(b)
            d = Dot([lx + XS[i] * 0.95, -0.2 + YS[i], 0], radius=0.09, color=TEXT)
            self.play(th[i].animate.shift(LEFT * 0.12), b.animate.shift(RIGHT * 0.12), FadeIn(d), run_time=0.6)
            self.wait(0.15)
        self.at("sharing sends")
        for x in Xs:
            x.clear_updaters()
        d1, d2 = cell_mob(2.8, 3.6, rx - 1.5, -0.2), cell_mob(2.8, 3.6, rx + 1.5, -0.2)
        self.play(*[x[2].animate.set_opacity(0) for x in Xs],
                  *[x[0].animate.move_to([rx - 1.5, -0.2 + [1.5, 0.5, -0.5, -1.5][i] * 0.8, 0]).rotate(PI) for i, x in enumerate(Xs)],
                  *[x[1].animate.move_to([rx + 1.5, -0.2 + [1.5, 0.5, -0.5, -1.5][i] * 0.8, 0]).rotate(PI) for i, x in enumerate(Xs)],
                  ReplacementTransform(cr, VGroup(d1, d2)), run_time=3.2)
        self.at("nothing is missing")
        self.play(Indicate(d1, color=YELLOW, scale_factor=1.05), Indicate(d2, color=YELLOW, scale_factor=1.05),
                  Indicate(cl, color=YELLOW, scale_factor=1.03), run_time=1.5)
        self.finish()


class S16Scope(SpokenScene):
    def construct(self):
        cell = cell_mob(6.4, 5.0, 0, 0)
        nuc = nuc_mob(1.7, 0, 0)
        th = [thread(XS[i] * 0.8, YS[i], HS[i] * 0.8, CH[i]) for i in range(4)]
        mt = motes(0, 0, 2.8, 2.2, 10)
        big = VGroup(cell, nuc, *th)
        k = knee(0.45, healed=True)
        k.scale(0.12, about_point=ORIGIN)
        self.add(big, mt, k)
        self.play(big.animate.scale(0.12).set_opacity(0), FadeOut(mt),
                  k.animate.scale(1 / 0.12 * 0.85, about_point=ORIGIN).shift(LEFT * 1.8), run_time=2.6)
        sc = k[2]
        glow = Ellipse(width=2.0, height=1.2, stroke_color="#F6A5B0", stroke_width=4).move_to(sc.get_center())
        self.play(Indicate(sc, color="#F6A5B0", scale_factor=1.3), Create(glow), run_time=1.2)
        self.at("mistakes")
        note = T("normal division; mistakes can happen", 26, TEXT).move_to([-1.8, -3.1, 0])
        self.play(FadeIn(note), run_time=0.8)
        self.play(Indicate(glow, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.at("normal division")
        ins = VGroup()
        for yy in (1.5, -1.0):
            c = cell_mob(2.6, 1.9, 4.9, yy)
            ins.add(c)
            for i in range(4):
                ins.add(chev(CH[i], 1, (4.9 - 0.9 + i * 0.6, yy), 0.5))
        self.play(FadeIn(ins, lag_ratio=0.05), run_time=1.4)
        self.at("a full set")
        fl = T("full set each", 28, YELLOW, weight=BOLD).move_to([4.9, 2.9, 0])
        self.play(FadeIn(fl), Indicate(ins, color=YELLOW, scale_factor=1.05), run_time=1.5)
        self.finish()


class S17End(EndCard):
    LINE = "Copy first, then share: each new cell gets one of each."
