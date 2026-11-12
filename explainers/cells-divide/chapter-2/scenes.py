"""Cells divide, chapter 2: A Photo That Tells Time (film 2 of 2, level-up)

COLOUR MAP (same as chapter 1): chromosomes RED, BLUE, GREEN, YELLOW (thin thread before copying,
two joined threads after copying, thick compact X once coiled); cell membrane PEACH; nucleus pale GREY;
plant cell wall DARK GREEN; tally bars TEAL; counters white on charcoal. All cells are schematic cartoons.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PEACH = "#F2B38C"
NUC = "#B8BCC4"
CHAR = "#2B2F36"
DGREEN = "#3C9A52"
PURPLE = "#A070D8"
CH = [RED, BLUE, GREEN, YELLOW]
CX, CY = -0.5, 0.0
CW0, CH0 = 6.4, 5.0
NR0 = 2.0
XS = [-1.4, -0.45, 0.5, 1.45]
YS = [0.1, -0.1, 0.1, -0.1]
HS = [2.3, 3.0, 2.8, 2.2]
ROW_Y = [1.875, 0.625, -0.625, -1.875]
SCATTER = [(-2.0, 1.2), (1.6, 1.4), (-1.4, -1.3), (1.9, -0.9)]
STAGES = ["prophase", "metaphase", "anaphase", "telophase"]


# ------------------------------------------------------------------ helpers (chapter 1 look)
def bob(m, amp=0.05, sp=1.3, ph=0.0):
    m._t = ph

    def u(mob, dt):
        mob._t += dt
        mob.shift(np.array([0.6 * amp * sp * np.cos(0.8 * sp * mob._t + 1.0),
                            amp * sp * np.cos(sp * mob._t), 0]) * dt)
    m.add_updater(u)
    return m


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


# ------------------------------------------------------------------ helpers (chapter 2)
def flash(scene, t=0.45):
    r = Rectangle(width=14.4, height=8.2, fill_color=WHITE, fill_opacity=0.92, stroke_width=0).set_z_index(50)
    scene.add(r)
    scene.play(FadeOut(r), run_time=t)


def mini_x(color, x, y, d=0.1):
    return VGroup(Line([x - d, y - d, 0], [x + d, y + d, 0]), Line([x - d, y + d, 0], [x + d, y - d, 0])).set_stroke(color, 5)


def plant_cell(cx, cy, w, h, state=0):
    """Small boxy plant cell: DARK GREEN wall, PEACH membrane. state 0 interphase (grey nucleus),
    1 prophase (coiled X, scattered), 2 metaphase (row), 3 anaphase (two groups), 4 telophase."""
    wall = Rectangle(width=w, height=h, stroke_color=DGREEN, stroke_width=4, fill_color=DGREEN, fill_opacity=0.14)
    mem = RoundedRectangle(corner_radius=0.12, width=w - 0.16, height=h - 0.16, stroke_color=PEACH, stroke_width=2.5,
                           fill_color=PEACH, fill_opacity=0.10)
    g = VGroup(wall, mem)
    d = 0.1 * min(w / 1.25, h / 1.1)
    if state == 0:
        g.add(Circle(radius=0.3 * min(w, h) / 1.1, stroke_color=NUC, stroke_width=3, fill_color=NUC, fill_opacity=0.25))
    elif state == 1:
        for i, (dx, dy) in enumerate([(-.3, .22), (.28, .25), (-.22, -.24), (.3, -.18)]):
            g.add(mini_x(CH[i], dx * w / 1.25, dy * h / 1.1, d))
    elif state == 2:
        for i, y in enumerate([.3, .1, -.1, -.3]):
            g.add(mini_x(CH[i], 0, y * h / 1.1, d))
    elif state == 3:
        for i in range(4):
            g.add(Line([(-.27 + i * .18) * w / 1.25, .24 * h / 1.1, 0], [(-.27 + i * .18) * w / 1.25, .36 * h / 1.1, 0]).set_stroke(CH[i], 5))
            g.add(Line([(-.27 + i * .18) * w / 1.25, -.24 * h / 1.1, 0], [(-.27 + i * .18) * w / 1.25, -.36 * h / 1.1, 0]).set_stroke(CH[i], 5))
    else:
        for s in (1, -1):
            g.add(Circle(radius=0.17 * min(w, h) / 1.1, stroke_color=NUC, stroke_width=3, fill_color=NUC, fill_opacity=0.25).shift(UP * s * .27 * h / 1.1))
        g.add(Line([-w / 2 + .1, 0, 0], [w / 2 - .1, 0, 0]).set_stroke(DGREEN, 4))
    return g.move_to([cx, cy, 0])


GRID_STATES = [[0, 0, 0, 1, 0, 0],
               [0, 2, 0, 0, 0, 4],
               [0, 0, 3, 0, 1, 0],
               [4, 0, 0, 0, 2, 0]]
GW, GH = 1.25, 1.1
GCY = 0.15


def make_grid(cy=GCY):
    cells = VGroup()
    for r in range(4):
        for c in range(6):
            cells.add(plant_cell((c - 2.5) * GW, cy + (1.5 - r) * GH, GW, GH, GRID_STATES[r][c]))
    return cells


def photo_frame(cy=GCY, color=TEXT):
    return Rectangle(width=6 * GW + 0.35, height=4 * GH + 0.35, stroke_color=color, stroke_width=6).move_to([0, cy, 0])


def figure(x, y, color=BLUE, s=1.0):
    return VGroup(Dot([x, y + 0.2 * s, 0], radius=0.12 * s, color=color),
                  Line([x, y + 0.08 * s, 0], [x, y - 0.2 * s, 0]).set_stroke(color, 7 * s))


def clock_face(cx, cy, r, color=TEXT):
    face = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=CHAR, fill_opacity=1).move_to([cx, cy, 0])
    hand = Line([cx, cy, 0], [cx, cy + r * 0.78, 0]).set_stroke(YELLOW, 4)
    hand.face = face
    return VGroup(face, hand)


def spin(clock, speed, phase=0.0):
    clock[1].rotate(-phase, about_point=clock[0].get_center())

    def u(m, dt):
        m.rotate(-speed * dt, about_point=clock[0].get_center())
    clock[1].add_updater(u)
    return clock


def freeze(*mobs):
    for m in mobs:
        for s in m.family_members_with_points() if hasattr(m, "family_members_with_points") else [m]:
            s.clear_updaters()
        m.clear_updaters()


# school world (same place in S03 and S04)
ROOMS = [(x, y) for y in (1.7, -1.3) for x in (-3.8, 0.0, 3.8)]


def school():
    rng = random.Random(7)
    building = Rectangle(width=11.6, height=5.4, stroke_color=GREY, stroke_width=4, fill_color=CHAR, fill_opacity=0.5).move_to([0, 0.2, 0])
    rooms, clocks, figs = VGroup(), [], VGroup()
    for k, (rx, ry) in enumerate(ROOMS):
        rooms.add(Rectangle(width=3.5, height=2.0, stroke_color=GREY, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.08).move_to([rx, ry, 0]))
        clocks.append(clock_face(rx + 1.35, ry + 0.68, 0.3))
        for j in range(6):
            figs.add(figure(rx - 1.1 + (j % 3) * 0.55 + rng.uniform(-.08, .08), ry - 0.35 + (j // 3) * 0.7, BLUE))
    walkers = VGroup(*[figure(-3.0 + i * 3.2, 0.2, YELLOW) for i in range(3)])
    return building, rooms, clocks, figs, walkers


def build_school(live=True):
    b, rooms, clocks, figs, walkers = school()
    g = VGroup(b, rooms, *clocks, figs, walkers)
    if live:
        for i, c in enumerate(clocks):
            spin(c, 0.8 + 0.55 * i, phase=i * 1.3)
        for i, f in enumerate(figs):
            bob(f, 0.04, ph=i * 0.7)
        for i, w in enumerate(walkers):
            def u(m, dt, i=i):
                m.shift(RIGHT * 0.9 * dt)
                if m.get_x() > 5.2:
                    m.shift(LEFT * 10.4)
            w.add_updater(u)
    return g, b, rooms, clocks, figs, walkers


BY = -0.5


def stage_bars(yA=BY):
    A = Rectangle(width=5.6, height=1.1, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.45).move_to([-2.6, yA, 0])
    B = Rectangle(width=2.8, height=1.1, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.45).move_to([3.0, yA, 0])
    la = T("Stage A", 36, TEXT, weight=BOLD).move_to(A)
    lb = T("Stage B", 36, TEXT, weight=BOLD).move_to(B)
    ll = T("time A = 2 x time B", 32, TEAL).move_to([0.2, -2.7, 0])
    return A, B, la, lb, ll


def qcard(text="In a snapshot, more A or more B?"):
    r = RoundedRectangle(corner_radius=0.14, width=9.4, height=1.1, fill_color=CHAR, fill_opacity=1, stroke_color=YELLOW, stroke_width=3)
    return VGroup(r, T(text, 32, YELLOW).move_to(r)).move_to([0, 2.7, 0])


def drop_sim(seed_n=45):
    for seed in range(1, 400):
        rng = random.Random(seed)
        pts = []
        for _ in range(seed_n):
            if rng.random() < 2 / 3:
                pts.append(("A", rng.uniform(-5.4, 0.2)))
            else:
                pts.append(("B", rng.uniform(1.6, 4.4)))
        a = sum(1 for p in pts if p[0] == "A")
        if 1.8 <= a / (seed_n - a) <= 2.2 and a % 2 == 1:
            return pts
    return pts


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "How Cells Divide"
    TITLE = "A Photo That Tells Time"


class S01Hook(SpokenScene):
    def construct(self):
        clock = clock_face(-2.8, 0.5, 2.2)
        ticks = VGroup(*[Line(np.array([-2.8, .5, 0]) + 2.0 * np.array([np.sin(a), np.cos(a), 0]),
                              np.array([-2.8, .5, 0]) + 2.15 * np.array([np.sin(a), np.cos(a), 0])).set_stroke(TEXT, 4)
                         for a in np.arange(0, TAU, TAU / 12)])
        spin(clock, 1.6)
        ground = Line([0.8, -2.0, 0], [5.8, -2.0, 0]).set_stroke(GREY, 4)
        ball = Dot(radius=0.5, color=YELLOW).move_to([3.3, 0, 0])
        ball.t = 0.0

        def bounce(m, dt):
            m.t += dt
            m.move_to([3.3 + 0.9 * np.sin(0.9 * m.t), -1.5 + 2.6 * abs(np.sin(2.0 * m.t)), 0])
        ball.add_updater(bounce)
        self.play(FadeIn(clock), FadeIn(ticks), FadeIn(ground), FadeIn(ball), run_time=0.8)
        self.at("a photo freezes")
        flash(self, 0.35)
        freeze(clock, ball)
        frame = Rectangle(width=12.4, height=6.2, stroke_color=TEXT, stroke_width=8).move_to([0, 0.35, 0])
        self.play(Create(frame), run_time=1.3)
        self.at("nothing in it moves")
        self.play(Indicate(ball, color=YELLOW, scale_factor=1.15), Indicate(clock[1], color=YELLOW), run_time=1.2)
        self.at("where would the time")
        dim = [m.animate.set_opacity(0.3) for m in (clock, ticks, ball, ground, frame)]
        card = RoundedRectangle(corner_radius=0.2, width=7.4, height=2.2, fill_color=CHAR, fill_opacity=1, stroke_color=YELLOW, stroke_width=4)
        q = VGroup(card, T("how long?", 80, YELLOW, weight=BOLD).move_to(card)).move_to([0, 0.35, 0])
        self.play(*dim, FadeIn(q, scale=0.7), run_time=0.9)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        cell = cell_mob(CW0, CH0)
        nuc = nuc_mob(NR0)
        th = singles()
        st = strip(0)
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(VGroup(*th)), FadeIn(st), run_time=0.7)
        for t in th:
            bob(t, 0.04, ph=np.random.rand() * 6)
        self.at("through the cycle")
        P = [pair(i) for i in range(4)]
        for t in th:
            t.clear_updaters()
        self.play(*[ReplacementTransform(th[i], P[i]) for i in range(4)], run_time=0.7)
        self.at("step by step")
        Xs = [xmark(CH[i], (CX + SCATTER[i][0], CY + SCATTER[i][1])) for i in range(4)]
        self.play(*light(st[0]), *[ReplacementTransform(P[i], Xs[i]) for i in range(4)], FadeOut(nuc), run_time=0.8)
        for i in range(4):
            rowx = [xmark(CH[j], (CX, CY + ROW_Y[j] * 0.8)) for j in range(4)]
        self.play(*light(st[1]), *[Xs[i].animate.move_to([CX, CY + ROW_Y[i] * 0.8, 0]) for i in range(4)], run_time=0.5)
        self.at("in order")
        self.play(*light(st[2]), *[Xs[i].animate.move_to([CX + (-1.5 if i % 2 else 1.5) * 0 + (i - 1.5) * 0.9, CY + (1.2 if i < 2 else -1.2), 0]) for i in range(4)], run_time=0.9)
        self.play(*light(st[3]), run_time=0.7)
        self.at("a stained root tip")
        flash(self)
        freeze(*Xs)
        self.remove(cell, st, *Xs)
        grid = make_grid()
        fr = photo_frame()
        self.add(grid, fr)
        self.play(grid.animate.scale(1.04, about_point=[0, GCY, 0]), run_time=2.0)
        self.at("only a snapshot")
        lab = T("snapshot", 40, YELLOW, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), grid.animate.scale(1.02, about_point=[0, GCY, 0]), run_time=1.5)
        self.finish()


class S03School(SpokenScene):
    def construct(self):
        g, b, rooms, clocks, figs, walkers = build_school(live=False)
        sch = T("schematic", 24, GREY).move_to([-5.4, 3.45, 0])
        self.play(FadeIn(b), FadeIn(rooms, lag_ratio=0.1), FadeIn(figs, lag_ratio=0.02), FadeIn(walkers), FadeIn(sch), run_time=1.6)
        for i, f in enumerate(figs):
            bob(f, 0.04, ph=i * 0.7)
        for i, w in enumerate(walkers):
            def u(m, dt):
                m.shift(RIGHT * 0.9 * dt)
                if m.get_x() > 5.2:
                    m.shift(LEFT * 10.4)
            w.add_updater(u)
        self.at("no shared bell")
        lab = T("no shared bell", 34, YELLOW, weight=BOLD).move_to([0, -3.2, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.7)
        self.at("each student keeps")
        for i, c in enumerate(clocks):
            spin(c, 0.8 + 0.55 * i, phase=i * 1.3)
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in clocks], lag_ratio=0.2), run_time=1.4)
        self.at("snap a photo")
        flash(self, 0.35)
        freeze(*figs, *walkers, *[c[1] for c in clocks])
        fr = Rectangle(width=12.0, height=6.0, stroke_color=TEXT, stroke_width=8).move_to([0, 0.2, 0])
        self.play(Create(fr), FadeOut(lab), run_time=1.0)
        self.at("most students are in class")
        lab2 = T("most: in class", 34, YELLOW, weight=BOLD).move_to([0, -3.2, 0])
        self.play(FadeIn(lab2), *[r.animate.set_stroke(YELLOW, 4) for r in rooms], Indicate(figs, color=YELLOW, scale_factor=1.1), run_time=1.5)
        self.at("only a few are in the hallway")
        halo = Rectangle(width=11.4, height=0.95, stroke_color=YELLOW, stroke_width=5).move_to([0, 0.2, 0])
        lab3 = T("few: hallway", 34, YELLOW, weight=BOLD).move_to([0, -3.2, 0])
        self.play(*[r.animate.set_stroke(GREY, 2.5) for r in rooms], Create(halo), ReplacementTransform(lab2, lab3), Indicate(walkers, color=YELLOW, scale_factor=1.2), run_time=1.5)
        self.at("why")
        why = T("Why?", 80, YELLOW, weight=BOLD).move_to([0, 0.2, 0])
        bgbox = RoundedRectangle(corner_radius=0.2, width=3.8, height=1.7, fill_color=CHAR, fill_opacity=1, stroke_color=YELLOW, stroke_width=4).move_to(why)
        self.play(FadeIn(VGroup(bgbox, why), scale=0.6), run_time=0.7)
        self.play(Indicate(why, color=YELLOW, scale_factor=1.2), run_time=0.9)
        self.finish()


class S04School2(SpokenScene):
    def construct(self):
        g, b, rooms, clocks, figs, walkers = build_school(live=False)
        fr = Rectangle(width=12.0, height=6.0, stroke_color=TEXT, stroke_width=8).move_to([0, 0.2, 0])
        self.add(g, fr)
        for i, f in enumerate(figs):
            bob(f, 0.02, ph=i * 0.7)
        self.play(VGroup(g, fr).animate.scale(0.65).move_to([0, 1.5, 0]), run_time=1.2)
        Y = -1.3
        blocks, hall = VGroup(), VGroup()
        for p in range(4):
            x0 = -5.8 + p * 2.9
            blocks.add(Rectangle(width=2.2, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5).move_to([x0 + 1.1, Y, 0]))
            hall.add(Rectangle(width=0.7, height=0.7, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.6).move_to([x0 + 2.55, Y, 0]))
        both = VGroup(*[m for p in range(4) for m in (blocks[p], hall[p])])
        self.play(LaggedStart(*[GrowFromEdge(m, LEFT) for m in both], lag_ratio=0.2), run_time=2.0)
        l1 = T("class", 32, BLUE, weight=BOLD).move_to([-4.7, -2.1, 0])
        l2 = T("hallway", 32, YELLOW, weight=BOLD).move_to([-2.0, -2.1, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.8)
        self.at("so at any random moment")
        rng = random.Random(11)
        cnt = {"c": 0, "h": 0}
        for k in range(12):
            x = rng.uniform(-5.8, 5.8)
            in_class = ((x + 5.8) % 2.9) < 2.2
            col = BLUE if in_class else YELLOW
            d = Dot([x, -0.5, 0], radius=0.18, color=col)
            n = cnt["c" if in_class else "h"]
            cnt["c" if in_class else "h"] += 1
            tx = (-4.6 + (n % 8) * 0.44) if in_class else (3.6 + (n % 4) * 0.44)
            ty = -3.4 + (n // 8 if in_class else n // 4) * 0.44
            self.add(d)
            self.play(d.animate.move_to([x, Y + 0.55, 0]), run_time=0.2)
            self.play(d.animate.move_to([tx, ty, 0]), run_time=0.15)
            self.wait(0.1)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        A, B, la, lb, ll = stage_bars()
        self.at("stage A lasts")
        self.play(GrowFromEdge(A, LEFT), FadeIn(la), run_time=1.0)
        self.at("as long as")
        self.play(GrowFromEdge(B, LEFT), FadeIn(lb), run_time=1.0)
        self.play(FadeIn(ll, shift=UP * 0.2), run_time=0.8)
        self.at("in a random snapshot")
        card = qcard()
        self.play(FadeIn(card, shift=DOWN * 0.3), run_time=0.8)
        self.at("which stage will you see")
        self.play(Indicate(A, color=YELLOW, scale_factor=1.04), Indicate(B, color=YELLOW, scale_factor=1.04), run_time=1.4)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        A, B, la, lb, ll = stage_bars()
        card = qcard()
        self.add(A, B, la, lb, ll, card)
        tr = ValueTracker(0.001)
        ring = Circle(radius=0.38, color=GREY, stroke_width=5).move_to([5.9, -3.0, 0])
        arc = always_redraw(lambda: Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * tr.get_value(),
                                        color=YELLOW, stroke_width=7).move_arc_center_to([5.9, -3.0, 0]))
        self.add(ring, arc)
        a1 = Succession(Wait(0.4), Indicate(card, color=YELLOW, scale_factor=1.04, run_time=1.2), Wait(0.6), Indicate(A, color=YELLOW, scale_factor=1.03, run_time=1.2), Indicate(B, color=YELLOW, scale_factor=1.05, run_time=1.0))
        self.play(a1, tr.animate.set_value(1.0), rate_func=linear, run_time=4.6)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        A, B, la, lb, ll = stage_bars()
        self.add(A, B, la, lb, ll)
        self.at("stage a")
        self.play(Indicate(A, color=YELLOW, scale_factor=1.04), Indicate(la, color=YELLOW), run_time=1.2)
        pts = drop_sim(45)
        nA = sum(1 for p in pts if p[0] == "A")
        nB = len(pts) - nA
        cA, cB = [0], [0]
        ta = always_redraw(lambda: T(f"A: {cA[0]}", 40, TEXT, weight=BOLD).move_to([-2.6, -1.7, 0]))
        tb = always_redraw(lambda: T(f"B: {cB[0]}", 40, TEXT, weight=BOLD).move_to([3.0, -1.7, 0]))
        sim = T("computed: random moments", 24, GREY).move_to([0, -3.4, 0])
        self.add(ta, tb)
        self.play(FadeIn(sim), run_time=0.4)
        self.at("about twice as many")
        stacks = {}
        for k, (s, x) in enumerate(pts):
            bx = round(x / 0.28)
            key = (s, bx)
            n = stacks.get(key, 0)
            stacks[key] = n + 1
            d = Dot([bx * 0.28, 3.4, 0], radius=0.11, color=YELLOW)
            self.add(d)
            self.play(d.animate.move_to([bx * 0.28, 0.2 + 0.22 * n, 0]), run_time=0.1, rate_func=linear)
            if s == "A":
                cA[0] += 1
            else:
                cB[0] += 1
        self.at("to hold more of them")
        two = T("about 2 : 1", 56, YELLOW, weight=BOLD).move_to([0, 2.9, 0])
        self.play(FadeIn(two, scale=0.7), run_time=0.8)
        self.play(Indicate(two, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


class S08Onion(SpokenScene):
    def construct(self):
        studs = VGroup(*[figure(-4.0 + i * 2.0, 0, BLUE, 2.4) for i in range(5)])
        cells = VGroup(*[plant_cell(-4.0 + i * 2.0, 0.1, 1.6, 1.5, [0, 1, 0, 2, 0][i]) for i in range(5)])
        self.play(FadeIn(studs, lag_ratio=0.1), run_time=0.9)
        for i, f in enumerate(studs):
            bob(f, 0.05, ph=i)
        self.at("cells")
        for f in studs:
            f.clear_updaters()
        self.play(*[ReplacementTransform(studs[i], cells[i]) for i in range(5)], run_time=1.2)
        self.at("set an onion")
        self.play(FadeOut(cells), run_time=0.6)
        glass = Rectangle(width=4.8, height=3.4, stroke_color=TEXT, stroke_width=5, fill_color=BLUE, fill_opacity=0.18).move_to([-1.0, -1.6, 0])
        onion = VGroup(Circle(radius=1.5, stroke_color="#C79BE0", stroke_width=5, fill_color="#C79BE0", fill_opacity=0.5),
                       Triangle(stroke_color="#C79BE0", stroke_width=5, fill_color="#C79BE0", fill_opacity=0.5).scale(0.4).shift(UP * 1.75),
                       ).move_to([-1.0, 1.3, 0])
        self.play(FadeIn(onion, shift=DOWN * 0.4), Create(glass), run_time=1.2)
        self.at("roots grow down")
        roots = VGroup()
        ends = [(-2.4, -3.0), (-1.7, -3.15), (-1.0, -3.2), (-0.3, -3.1), (0.4, -2.95)]
        for i, (ex, ey) in enumerate(ends):
            sx = -2.0 + i * 0.5
            r = ParametricFunction(lambda t, sx=sx, ex=ex, ey=ey: np.array([sx + (ex - sx) * t + 0.12 * np.sin(5 * t), -0.1 + (ey + 0.1) * t, 0]),
                                   t_range=[0, 1, 0.02], color=TEXT, stroke_width=6)
            roots.add(r)
        bubbles = VGroup()
        rng = random.Random(3)
        for _ in range(9):
            d = Dot(radius=0.06, color=TEXT).set_opacity(0.4).move_to([rng.uniform(-3.1, 1.1), rng.uniform(-3.2, -0.2), 0])
            d.v = rng.uniform(0.2, 0.5)

            def ub(m, dt):
                m.shift(UP * m.v * dt)
                if m.get_y() > -0.15:
                    m.shift(DOWN * 3.0)
            d.add_updater(ub)
            bubbles.add(d)
        self.add(bubbles)
        self.play(LaggedStart(*[Create(r) for r in roots], lag_ratio=0.2), run_time=2.6)
        self.at("near each root tip")
        tip = Circle(radius=0.55, stroke_color=YELLOW, stroke_width=6).move_to([-1.0, -3.0, 0])
        self.play(Create(tip), run_time=0.8)
        self.at("cells divide often")
        lab = T("tips: cells divide often", 34, YELLOW, weight=BOLD)
        lab.move_to([3.6, 0.0, 0])
        lab = VGroup(T("tips:", 40, YELLOW, weight=BOLD), T("cells divide", 40, YELLOW, weight=BOLD), T("often", 40, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.15).move_to([4.0, -0.4, 0])
        ln = Line([1.8, -0.9, 0], [-0.4, -2.7, 0]).set_stroke(YELLOW, 3)
        self.play(FadeIn(lab, shift=LEFT * 0.3), Create(ln), run_time=1.0)
        self.play(Indicate(tip, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.finish()


class S09Stain(SpokenScene):
    def construct(self):
        tip = VMobject().set_points_as_corners([[-0.6, 2.5, 0], [0.6, 2.5, 0], [0.55, -1.0, 0], [0, -2.5, 0], [-0.55, -1.0, 0], [-0.6, 2.5, 0]])
        tip.set_stroke(TEXT, 5).set_fill(TEXT, 0.85)
        tip.move_to([-2.0, 0.2, 0])
        self.play(FadeIn(tip, shift=UP * 0.3), run_time=0.6)
        dropper = VGroup(Rectangle(width=0.4, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4),
                         Triangle(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).scale(0.2).rotate(PI)).arrange(DOWN, buff=0).move_to([-2.0, 3.2, 0])
        self.at("stained")
        self.add(dropper)
        for _ in range(2):
            d = Dot(radius=0.13, color=PURPLE).move_to([-2.0, 2.6, 0])
            self.add(d)
            self.play(d.animate.move_to([-2.0, 2.0 - 0.1, 0]), run_time=0.2)
            self.play(FadeOut(d), run_time=0.05)
        self.play(tip.animate.set_fill(PURPLE, 0.85).set_stroke(PURPLE), FadeOut(dropper), run_time=0.8)
        self.at("chromosomes show up")
        specks = VGroup(*[mini_x(CH[i % 4], -2.0 + (-0.2 if i % 2 else 0.2), 1.9 - i * 0.55, 0.12) for i in range(7)])
        self.play(LaggedStart(*[FadeIn(s, scale=2) for s in specks], lag_ratio=0.1), run_time=1.0)
        self.at("under a microscope")
        base = RoundedRectangle(corner_radius=0.1, width=3.4, height=0.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([4.2, -3.2, 0])
        pil = Rectangle(width=0.5, height=3.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([5.4, -1.4, 0])
        tube = Rectangle(width=0.9, height=2.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).rotate(0.12).move_to([4.2, 0.9, 0])
        lens = Rectangle(width=0.5, height=0.5, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.5).move_to([4.2, -0.65, 0])
        stage = Rectangle(width=2.6, height=0.22, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([4.2, -1.9, 0])
        scope = VGroup(base, pil, tube, lens, stage)
        self.play(FadeIn(scope, shift=LEFT * 0.4), run_time=0.5)
        tipg = VGroup(tip, specks)
        self.play(tipg.animate.rotate(PI / 2).scale(0.45).move_to([4.2, -1.65, 0]), run_time=0.9)
        self.at("each cell is caught")
        grid = make_grid()
        fr = photo_frame()
        self.play(FadeOut(scope), FadeOut(tipg), FadeIn(grid, scale=0.6), Create(fr), run_time=1.3)
        lab = T("schematic, not the real counts", 28, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(lab), run_time=0.6)
        hot = VGroup(*[c for c in grid if len(c) > 3 or len(c) == 3 and False])
        pick = [grid[i] for i in (3, 7, 14, 16, 22, 23)]
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.15) for c in pick], run_time=1.6)
        self.finish()


class S10Sort(SpokenScene):
    def construct(self):
        grid = make_grid()
        fr = photo_frame()
        self.add(grid, fr)
        self.play(grid.animate.scale(1.03, about_point=[0, GCY, 0]), run_time=1.0)
        self.at("what its chromosomes look like")
        pick = [grid[i] for i in (3, 7, 14, 16, 22, 23)]
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.15) for c in pick], run_time=1.6)
        self.at("thick coiled chromosomes")
        self.play(grid.animate.set_opacity(0.18), fr.animate.set_opacity(0.18), run_time=0.5)
        bigP = plant_cell(-2.8, 0.6, 4.4, 3.6, 0)
        bigP.remove(bigP[-1])
        Xp = VGroup(*[xmark(CH[i], (-2.8 + SCATTER[i][0] * 0.55, 0.6 + SCATTER[i][1] * 0.6), 0.7) for i in range(4)])
        pop = VGroup(bigP, Xp)
        self.play(FadeIn(pop, scale=0.5), run_time=1.0)
        for x in Xp:
            bob(x, 0.04, ph=np.random.rand() * 6)
        self.at("not yet in a row")
        nr = T("not in a row", 32, YELLOW, weight=BOLD).move_to([-2.8, 2.85, 0])
        self.play(FadeIn(nr), run_time=0.4)
        binP = VGroup(RoundedRectangle(corner_radius=0.12, width=4.2, height=0.9, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.15),
                      T("prophase", 34, TEAL, weight=BOLD)).move_to([-3.0, -3.1, 0])
        binM = VGroup(RoundedRectangle(corner_radius=0.12, width=4.2, height=0.9, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.15),
                      T("metaphase", 34, TEAL, weight=BOLD)).move_to([3.0, -3.1, 0])
        self.play(FadeIn(binP), FadeIn(binM), run_time=0.4)
        self.at("mean prophase")
        for x in Xp:
            x.clear_updaters()
        self.play(FadeOut(nr), pop.animate.scale(0.2).move_to([-3.0, -3.1, 0]).set_opacity(0), binP[0].animate.set_fill(TEAL, 0.5), run_time=1.3)
        self.at("a row across the middle")
        bigM = plant_cell(2.8, 0.6, 4.4, 3.6, 0)
        bigM.remove(bigM[-1])
        Xm = VGroup(*[xmark(CH[i], (2.8, 0.6 + ROW_Y[i] * 0.6), 0.7) for i in range(4)])
        popm = VGroup(bigM, Xm)
        self.play(FadeIn(popm, scale=0.5), run_time=1.0)
        line = DashedLine([2.8, 2.4, 0], [2.8, -1.2, 0], color=YELLOW, stroke_width=4)
        self.play(Create(line), run_time=0.7)
        self.at("means metaphase")
        self.play(FadeOut(line), popm.animate.scale(0.2).move_to([3.0, -3.1, 0]).set_opacity(0), binM[0].animate.set_fill(TEAL, 0.5), run_time=1.1)
        self.finish()


def tally_grid(cx=-3.0, cy=0.5, size=0.8, cols=9, rows=4):
    blocks = VGroup()
    for i in range(cols * rows):
        r, c = divmod(i, cols)
        blocks.add(Square(size * 0.88, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.1).move_to(
            [cx + (c - (cols - 1) / 2) * size, cy + ((rows - 1) / 2 - r) * size, 0]))
    return blocks


class S11Prophase(SpokenScene):
    def construct(self):
        big = plant_cell(-3.0, 0.5, 5.0, 4.0, 0)
        big.remove(big[-1])
        Xp = VGroup(*[xmark(CH[i], (-3.0 + SCATTER[i][0] * 0.65, 0.5 + SCATTER[i][1] * 0.7), 0.75) for i in range(4)])
        lab = T("prophase", 44, TEAL, weight=BOLD).move_to([4.0, 0.5, 0])
        self.play(FadeIn(big), FadeIn(Xp), FadeIn(lab), run_time=1.0)
        for x in Xp:
            bob(x, 0.05, ph=np.random.rand() * 6)
        self.at("real counts")
        rc = T("real counts", 34, YELLOW, weight=BOLD).move_to([4.0, -1.0, 0])
        self.play(FadeIn(rc, shift=UP * 0.2), run_time=0.7)
        self.at("in one set of 36")
        for x in Xp:
            x.clear_updaters()
        blocks = tally_grid()
        self.play(FadeOut(big), FadeOut(Xp), FadeOut(rc), FadeIn(blocks, lag_ratio=0.03), run_time=1.6)
        allt = T("36 cells in all", 32, TEXT).move_to([-3.0, -2.2, 0])
        self.at("photographed onion cells")
        self.play(FadeIn(allt), run_time=0.7)
        self.at("ten were in prophase")
        n = ValueTracker(0)
        cnt = always_redraw(lambda: M(str(int(round(n.get_value()))), 110, TEAL, weight=BOLD).move_to([4.0, 1.8, 0]))
        self.add(cnt)
        for i in range(10):
            self.play(blocks[i].animate.set_fill(TEAL, 0.85).set_stroke(TEAL), n.animate.set_value(i + 1), run_time=0.13)
        self.at("the coiled stage")
        self.play(Indicate(lab, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


class S12Percent(SpokenScene):
    def construct(self):
        blocks = tally_grid()
        for i in range(10):
            blocks[i].set_fill(TEAL, 0.85).set_stroke(TEAL)
        cnt = M("10", 110, TEAL, weight=BOLD).move_to([4.0, 1.8, 0])
        lab = T("prophase", 44, TEAL, weight=BOLD).move_to([4.0, 0.5, 0])
        allt = T("36 cells in all", 32, TEXT).move_to([-3.0, -2.2, 0])
        self.add(blocks, cnt, lab, allt)
        self.wait(0.3)
        pie = VGroup()
        PC, PR = np.array([-3.5, 0.2, 0]), 2.7
        for i in range(36):
            on = i < 10
            pie.add(Sector(radius=PR, start_angle=PI / 2 - i * TAU / 36, angle=-TAU / 36, arc_center=PC,
                           stroke_color=BG, stroke_width=2, fill_color=TEAL if on else GREY, fill_opacity=0.85 if on else 0.2))
        self.at("turn that count")
        self.play(FadeOut(cnt), FadeOut(allt), FadeOut(lab), ReplacementTransform(blocks, pie), run_time=2.4)
        self.at("follow the steps")
        lines = [M("10 / 36", 44, TEXT), M("≈ 0.28", 44, TEXT), M("≈ 28 percent", 44, TEAL, weight=BOLD)]
        for i, l in enumerate(lines):
            l.move_to([3.9, 1.6 - i * 1.2, 0])
        self.play(Write(lines[0]), run_time=1.1)
        self.at("about", nth=0)
        self.play(Write(lines[1]), run_time=1.0)
        self.at("of the cells")
        self.play(Write(lines[2]), run_time=1.3)
        self.play(Indicate(VGroup(*pie[:10]), color=YELLOW, scale_factor=1.04), run_time=1.0)
        self.finish()


def clock_world(scene, pie_state=None):
    C = np.array([-3.5, 0.2, 0])
    R = 2.7
    face = Circle(radius=R, stroke_color=TEXT, stroke_width=5, fill_color=CHAR, fill_opacity=1).move_to(C)
    ticks = VGroup()
    for k in range(24):
        a = PI / 2 - k * TAU / 24
        L = 0.3 if k % 6 == 0 else 0.15
        ticks.add(Line(C + (R - L) * np.array([np.cos(a), np.sin(a), 0]), C + R * np.array([np.cos(a), np.sin(a), 0])).set_stroke(TEXT, 4))
    nums = VGroup(*[T(t, 26, TEXT).move_to(C + (R - 0.65) * np.array([np.cos(PI / 2 - k * TAU / 4), np.sin(PI / 2 - k * TAU / 4), 0])) for k, t in enumerate(["24", "6", "12", "18"])]).set_z_index(5)
    return C, R, face, ticks, nums


class S13Time(SpokenScene):
    def construct(self):
        # carry the pie from S12 in the same place
        pie = VGroup()
        PC, PR = np.array([-3.5, 0.2, 0]), 2.7
        for i in range(36):
            on = i < 10
            pie.add(Sector(radius=PR, start_angle=PI / 2 - i * TAU / 36, angle=-TAU / 36, arc_center=PC,
                           stroke_color=BG, stroke_width=2, fill_color=TEAL if on else GREY, fill_opacity=0.85 if on else 0.2))
        self.add(pie)
        C, R, face, ticks, nums = clock_world(self)
        self.play(Indicate(VGroup(*pie[:10]), color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.at("assume one cycle")
        self.play(FadeOut(pie), FadeIn(face), FadeIn(ticks), FadeIn(nums), run_time=1.2)
        self.at("24 hours")
        asm = T("assumed: 24 hours", 36, YELLOW, weight=BOLD).move_to([3.9, 2.9, 0])
        self.play(FadeIn(asm, shift=LEFT * 0.3), run_time=0.8)
        tr = ValueTracker(0)
        hand = always_redraw(lambda: Line(C, C + (R - 0.2) * np.array([np.sin(tr.get_value()), np.cos(tr.get_value()), 0])).set_stroke(YELLOW, 7))
        wedge = always_redraw(lambda: Sector(radius=R - 0.05, start_angle=PI / 2, angle=-max(tr.get_value(), 0.001), arc_center=C,
                                              stroke_width=0, fill_color=TEAL, fill_opacity=0.8))
        self.add(wedge, hand)
        self.play(tr.animate.set_value(TAU), rate_func=linear, run_time=1.3)
        self.play(tr.animate.set_value(0.001), run_time=0.3)
        self.at("take each stage's share")
        self.play(tr.animate.set_value(100 * DEGREES), rate_func=smooth, run_time=1.8)
        steps = [M("28 percent of 24 hours", 32, TEXT).move_to([3.7, 1.7, 0])]
        self.at("its share of the time")
        self.play(Write(steps[0]), run_time=1.5)
        self.at("then prophase lasts")
        res = M("= about 7 hours", 44, TEAL, weight=BOLD).move_to([3.7, 0.4, 0])
        self.play(Write(res), run_time=1.5)
        self.play(Indicate(res, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.finish()


class S14Limits(SpokenScene):
    def construct(self):
        C, R, face, ticks, nums = clock_world(self)
        wedge = Sector(radius=R - 0.05, start_angle=PI / 2, angle=-100 * DEGREES, arc_center=C, stroke_width=0, fill_color=TEAL, fill_opacity=0.8)
        hand = Line(C, C + (R - 0.2) * np.array([np.sin(100 * DEGREES), np.cos(100 * DEGREES), 0])).set_stroke(YELLOW, 7)
        asm = T("assumed: 24 hours", 36, YELLOW, weight=BOLD).move_to([3.9, 2.9, 0])
        st = M("28 percent of 24 hours", 32, TEXT).move_to([3.7, 1.7, 0])
        res = M("= about 7 hours", 44, TEAL, weight=BOLD).move_to([3.7, 0.4, 0])
        self.add(face, ticks, nums, wedge, hand, asm, st, res)
        self.at("rough guide")
        res2 = M("= about 7 hours?", 44, YELLOW, weight=BOLD).move_to([3.7, 0.4, 0])
        self.play(ReplacementTransform(res, res2), Indicate(wedge, color=YELLOW, scale_factor=1.02), run_time=1.2)

        def note(text, y, rot):
            bx = Rectangle(width=5.6, height=1.5, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.95)
            lines = VGroup(*[T(s, 28, "#222222", weight=BOLD) for s in text]).arrange(DOWN, buff=0.1).move_to(bx)
            return VGroup(bx, lines).rotate(rot).move_to([3.7, y, 0])
        self.at("only 36 photos")
        n1 = note(["only 36 photos;", "how picked? unknown"], -1.1, 0.04)
        n1.scale(1.5).set_opacity(0)
        self.play(n1.animate.scale(1 / 1.5).set_opacity(1), run_time=0.5, rate_func=rush_into)
        self.play(Indicate(n1, color=GOLD, scale_factor=1.04), run_time=0.8)
        self.at("and the 24 hours")
        n2 = note(["24 hours: assumed,", "not measured"], -3.0, -0.04)
        n2.scale(1.5).set_opacity(0)
        self.play(n2.animate.scale(1 / 1.5).set_opacity(1), run_time=0.5, rate_func=rush_into)
        self.play(Indicate(asm, color=GOLD, scale_factor=1.08), Indicate(face, color=YELLOW, scale_factor=1.02), run_time=1.0)
        self.at("not measured")
        self.play(Indicate(n2, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        grid = make_grid()
        fr = photo_frame()
        self.play(FadeIn(grid), Create(fr), run_time=0.9)
        for i, c in enumerate(grid):
            for m in c[2:]:
                bob(m, 0.02, ph=i * 0.4)
        self.at("many fairly picked cells")
        ch1 = chip("many cells", TEAL, 30).move_to([-4.4, -3.25, 0])
        self.play(FadeIn(ch1, shift=UP * 0.2), run_time=0.6)
        self.at("fairly picked")
        ch2 = chip("fairly picked", TEAL, 30).move_to([0, -3.25, 0])
        self.play(FadeIn(ch2, shift=UP * 0.2), run_time=0.6)
        flash(self, 0.3)
        self.at("dividing out of step")
        picks = [1, 4, 8, 15, 19, 22]
        clocks = []
        for j, i in enumerate(picks):
            cc = grid[i].get_center()
            ck = clock_face(cc[0] + 0.38, cc[1] + 0.3, 0.2)
            spin(ck, 1.0 + 0.7 * j, phase=j)
            clocks.append(ck)
        oos = T("out of step", 40, YELLOW, weight=BOLD).move_to([0, 3.3, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in clocks], lag_ratio=0.15), FadeIn(oos), run_time=1.2)
        self.at("steadily growing root")
        ch3 = chip("steady growth", TEAL, 30).move_to([4.4, -3.25, 0])
        self.play(FadeIn(ch3, shift=UP * 0.2), run_time=0.6)
        flash(self, 0.3)
        self.wait(0.5)
        flash(self, 0.3)
        self.at("then a longer stage")
        for c in clocks:
            freeze(c)
        self.play(*[FadeOut(m) for m in (grid, fr, oos, ch1, ch2, ch3, *clocks)], run_time=0.5)
        C = np.array([0, 0.15, 0])
        Rr = 2.6
        spans = [("I", 200), ("P", 50), ("M", 40), ("A", 30), ("T", 40)]
        arcs = VGroup()
        a0 = 90.0
        bounds = []
        for k, (nm, sp) in enumerate(spans):
            arcs.add(Arc(radius=Rr, start_angle=(a0 - 1.5) * DEGREES, angle=-(sp - 3) * DEGREES, color=TEAL if k == 0 else YELLOW, stroke_width=14).move_arc_center_to(C))
            bounds.append((a0, a0 - sp))
            a0 -= sp
        note = T("schematic arcs; computed: random moments", 24, GREY).move_to([0, -3.7, 0])
        rng = random.Random(5)
        stacks = {}
        mid = T("longer stage,\nmore cells", 34, TEXT, line_spacing=0.9).move_to(C)
        self.play(Create(arcs), FadeIn(note), FadeIn(mid), run_time=0.8)
        for k in range(44):
            deg = rng.uniform(0, 360)
            a = np.deg2rad(90 - deg)
            bnum = int(deg // 6)
            n = stacks.get(bnum, 0)
            stacks[bnum] = n + 1
            ang = np.deg2rad(90 - bnum * 6 - 3)
            rr = Rr + 0.3 + 0.2 * n
            col = TEAL if deg < 200 else YELLOW
            d = Dot(C, radius=0.1, color=col)
            self.add(d)
            self.play(d.animate.move_to(C + rr * np.array([np.cos(ang), np.sin(ang), 0])), run_time=0.1, rate_func=linear)
        self.at("rough guide to its time")
        rg = chip("rough guide", YELLOW, 38).move_to([0, -0.0, 0])
        self.play(FadeOut(mid), FadeIn(rg, scale=0.7), run_time=0.7)
        self.play(Indicate(rg, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


class S16Handoff(SpokenScene):
    def construct(self):
        names = ["interphase", "prophase", "metaphase", "anaphase", "telophase"]
        ys = [2.4, 1.2, 0.0, -1.2, -2.4]
        rows = []
        for nm, y in zip(names, ys):
            l = T(nm, 34, TEXT, weight=BOLD)
            l.move_to([-3.0 - l.width / 2 + 0.0, y, 0])
            l.set_x(-2.6 - l.width / 2)
            bar = Rectangle(width=6.2, height=0.8, stroke_color=TEAL, stroke_width=4, fill_opacity=0).move_to([0.8 + 3.1 - 2.6 + 0.0, y, 0])
            bar.align_to([-2.2, 0, 0], LEFT)
            rows.append((l, bar))
        l, bar = rows[1]
        fillb = Rectangle(width=6.2 * 10 / 36, height=0.8, stroke_width=0, fill_color=TEAL, fill_opacity=0.85).align_to(bar, LEFT).align_to(bar, UP)
        pct = M("≈ 28%", 28, TEXT).move_to(bar.get_right() + RIGHT * 1.0)
        self.play(FadeIn(l), Create(bar), FadeIn(fillb), FadeIn(pct), run_time=1.2)
        self.play(Indicate(fillb, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.at("four more are waiting")
        qs = VGroup()
        anims = []
        for k in (0, 2, 3, 4):
            ll, bb = rows[k]
            q = T("?", 44, YELLOW, weight=BOLD).move_to(bb.get_right() + RIGHT * 0.7)
            qs.add(q)
            anims.append(AnimationGroup(FadeIn(ll), Create(bb), FadeIn(q)))
        self.play(LaggedStart(*anims, lag_ratio=0.35), run_time=2.2)
        self.at("the biggest question")
        self.play(*[Indicate(q, color=YELLOW, scale_factor=1.4) for q in qs], run_time=1.4)
        self.at("now count the rest")
        pen = VGroup(Rectangle(width=1.5, height=0.28, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.9),
                     Triangle(stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.9).scale(0.17).rotate(PI / 2 + PI)).arrange(LEFT, buff=0)
        pen.rotate(0.7).move_to([5.9, -3.0, 0])
        pen.t = 0.0

        def wig(m, dt):
            m.t += dt
            m.shift(np.array([np.cos(8 * m.t) * 0.4, np.sin(8 * m.t) * 0.15, 0]) * dt * 3)
        pen.add_updater(wig)
        self.play(FadeIn(pen, shift=LEFT * 0.4), run_time=0.8)
        self.finish()


class S17End(EndCard):
    LINE = "Out of step, a longer stage tends to hold more cells."
