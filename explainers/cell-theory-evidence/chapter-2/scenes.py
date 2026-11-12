"""Where Do New Cells Come From? (cell theory evidence, film 2).

Same world as film 1: dark ground, cream "microscope view" panels, dark-BLUE (INK) cell outlines,
GOLD = light microscope. New here: GREEN = plant tissue, PINK = animal tissue,
TEAL = fluid model, ORANGE = division model. Anything not computed is labelled schematic.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

CREAM = "#EDE4D0"
INK = "#1F4FA8"
ORANGE = "#F28C28"
PLANT_BG = "#CFE5C4"
ANIMAL_BG = "#F3D2DA"
PINKT = "#F08FA8"
GREENT = "#6CCB8A"
LEFT_X, RIGHT_X = -3.7, 3.7
PW, PH, PCY = 5.0, 3.9, -0.3


def breathe(m, amp=0.03, per=3.2, phase=0.0):
    m._bs, m._bt = 1.0, 0.0

    def f(mob, dt):
        mob._bt += dt
        s = 1 + amp * math.sin(2 * math.pi * mob._bt / per + phase)
        mob.scale(s / mob._bs)
        mob._bs = s
    m.add_updater(f)
    return m


def shimmer(m, amp=0.25, per=2.4):
    m._st = 0.0

    def f(mob, dt):
        mob._st += dt
        mob.set_stroke(opacity=1 - amp + amp * math.sin(2 * math.pi * mob._st / per))
    m.add_updater(f)
    return m


def lm_icon(h=1.4, color=GOLD):
    kw = dict(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    base = Rectangle(width=1.0, height=0.14, **kw).shift(DOWN * 0.7)
    pillar = Rectangle(width=0.14, height=1.1, **kw).shift(RIGHT * 0.3 + DOWN * 0.15)
    stage = Rectangle(width=0.6, height=0.07, **kw).shift(LEFT * 0.1 + DOWN * 0.35)
    tube = Rectangle(width=0.26, height=0.85, **kw).rotate(0.35).shift(LEFT * 0.05 + UP * 0.15)
    eyep = Rectangle(width=0.16, height=0.22, **kw).rotate(0.35).shift(RIGHT * 0.14 + UP * 0.66)
    return VGroup(base, pillar, stage, tube, eyep).scale_to_fit_height(h)


def cell_style(m, r=1.0):
    return m.set_stroke(INK, 4).set_fill("#F7F0DF", 1)


def plant_tissue(c, w=PW, h=PH):
    panel = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREENT, stroke_width=6,
                             fill_color=PLANT_BG, fill_opacity=1).move_to(c)
    cw, ch = 0.78, 0.6
    cells = VGroup()
    rows = int((h - 0.4) / ch)
    for j in range(rows):
        y = c[1] - (h - 0.4) / 2 + ch / 2 + j * ch
        off = (cw / 2) if j % 2 else 0
        for i in range(-8, 9):
            x = c[0] + i * cw + off
            if abs(x - c[0]) + cw / 2 < w / 2 - 0.2:
                cells.add(Rectangle(width=cw, height=ch, stroke_color=INK, stroke_width=3.5, fill_opacity=0).move_to([x, y, 0]))
    panel.set_z_index(0)
    cells.set_z_index(2)
    g = VGroup(panel, cells)
    g.panel, g.cells = panel, cells
    g.mark = cells[len(cells) // 2 + 1]
    return g


def animal_tissue(c, w=PW, h=PH):
    panel = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=PINKT, stroke_width=6,
                             fill_color=ANIMAL_BG, fill_opacity=1).move_to(c)
    rng = np.random.RandomState(4)
    cells = VGroup()
    dx, dy = 0.86, 0.74
    rows = int((h - 0.5) / dy)
    for j in range(rows):
        y = c[1] - (h - 0.5) / 2 + dy / 2 + j * dy
        off = (dx / 2) if j % 2 else 0
        for i in range(-8, 9):
            x = c[0] + i * dx + off
            if abs(x - c[0]) + 0.35 < w / 2 - 0.15:
                p = np.array([x + rng.uniform(-0.05, 0.05), y + rng.uniform(-0.04, 0.04), 0])
                cell = VGroup(Circle(radius=0.31, stroke_color=INK, stroke_width=3.5, fill_color="#FBEFF2", fill_opacity=1),
                              Dot(radius=0.07, color=INK)).move_to(p)
                cells.add(cell)
    panel.set_z_index(0)
    cells.set_z_index(2)
    g = VGroup(panel, cells)
    g.panel, g.cells = panel, cells
    g.mark = cells[len(cells) // 2 + 1][0]
    return g


def stack_behind(c, w, h, color, sx):
    return VGroup(*[RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=4,
                                     fill_color=color, fill_opacity=0.5 - 0.15 * k).move_to(c + np.array([sx * 0.16 * k, 0.16 * k, 0]))
                    for k in (2, 1)])


def peanut(c, r, s, ang=0.0):
    """One cell pinching in two (schematic): s from 0 (round) to 1 (two lobes)."""
    a, b = r * (1 + 0.6 * s), r * (1 - 0.2 * s)
    pts = []
    for th in np.linspace(0, TAU, 90, endpoint=False):
        f = 1 - 0.97 * s * (1 - math.cos(th) ** 2) ** 1.6
        x, y = a * math.cos(th), b * math.sin(th) * f
        pts.append([x * math.cos(ang) - y * math.sin(ang), x * math.sin(ang) + y * math.cos(ang), 0])
    m = VMobject().set_points_as_corners(pts + [pts[0]])
    return cell_style(m).move_to(c)


def disc(c, r):
    return cell_style(Circle(radius=r)).move_to(c)


def ss(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def div_mobs(c, R, p):
    """Division loop at phase p in 0..1: 1 cell -> pinch -> 2 -> pinch -> 4 (schematic)."""
    c = np.array(c, dtype=float)
    out = []
    if p < 0.4:
        out.append(peanut(c, R, ss((p - 0.1) / 0.3)))
    elif p < 0.6:
        sep = 0.8 * R + 0.35 * R * ss((p - 0.4) / 0.15)
        out += [disc(c + RIGHT * sep, 0.8 * R), disc(c + LEFT * sep, 0.8 * R)]
    elif p < 0.9:
        s = ss((p - 0.6) / 0.22)
        sep = 1.15 * R
        for sx in (-1, 1):
            out.append(peanut(c + RIGHT * sx * sep, 0.8 * R, s, ang=PI / 2))
    elif p < 0.97:
        sep = 1.15 * R
        for sx in (-1, 1):
            for sy in (-1, 1):
                out.append(disc(c + np.array([sx * sep, sy * 0.64 * R, 0]), 0.64 * R))
    else:
        sep = 1.15 * R
        k = 1 - (p - 0.97) / 0.03
        for sx in (-1, 1):
            for sy in (-1, 1):
                out.append(disc(c + np.array([sx * sep, sy * 0.64 * R, 0]), 0.64 * R * max(k, 0.05)))
    return VGroup(*out)


def arrows_for(c, R, p):
    """Orange arrows from parent to daughters, shown while the first split happens."""
    a = ss((p - 0.36) / 0.08) * (1 - ss((p - 0.62) / 0.08))
    g = VGroup()
    if a > 0.02:
        for sx in (-1, 1):
            g.add(Arrow(np.array(c) + RIGHT * sx * 0.2 * R, np.array(c) + RIGHT * sx * 2.35 * R, color=ORANGE, stroke_width=7,
                        buff=0, tip_length=0.28).set_opacity(a))
    return g


def clock_tracker(scene, period, on=None):
    tr = ValueTracker(0.0)
    tr._on = True if on is None else on

    def f(m, dt):
        if m._on:
            m.set_value((m.get_value() + dt / period) % 1.0)
    tr.add_updater(f)
    scene.add(tr)
    return tr


def division_loop(c, R, tr):
    return always_redraw(lambda: VGroup(div_mobs(c, R, tr.get_value()), arrows_for(c, R, tr.get_value())))


def specks(c, w, h, g, n=18, ring=(0, 0), ring_r=0.6, seed=1):
    """TEAL specks drifting in a pool; as g goes 0 -> 1 they gather into a ring and a new cell hardens."""
    rng = np.random.RandomState(seed)
    anchors = [(rng.uniform(-w / 2 + 0.3, w / 2 - 0.3), rng.uniform(-h / 2 + 0.3, h / 2 - 0.3), rng.uniform(0, 6.28)) for _ in range(n)]
    clk = {"t": 0.0}
    base = Mobject()
    base.add_updater(lambda m, dt: clk.__setitem__("t", clk["t"] + dt))

    def build():
        gv = g.get_value()
        grp = VGroup()
        t = clk["t"]
        for i, (ax, ay, ph) in enumerate(anchors):
            dx = 0.28 * math.sin(t * 0.9 + ph)
            dy = 0.22 * math.cos(t * 0.7 + ph * 1.3)
            th = TAU * i / n
            tx, ty = ring[0] + ring_r * math.cos(th), ring[1] + ring_r * math.sin(th)
            e = ss(gv)
            x, y = (1 - e) * (ax + dx) + e * tx, (1 - e) * (ay + dy) + e * ty
            grp.add(Dot(radius=0.1, color=TEAL).move_to(c + np.array([x, y, 0])))
        h = ss((gv - 0.55) / 0.4)
        if h > 0.01:
            cell = Circle(radius=ring_r * 0.95, stroke_color=INK, stroke_width=6, fill_color="#F7F0DF", fill_opacity=h)
            cell.set_stroke(opacity=h).move_to(c + np.array([ring[0], ring[1], 0]))
            grp.add(cell)
        return grp
    return base, always_redraw(build)


def pool(c, w, h):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=TEAL, stroke_width=5,
                            fill_color=TEAL, fill_opacity=0.22).move_to(c)


def loop_profile(p):
    if p < 0.15:
        return 0.0
    if p < 0.65:
        return (p - 0.15) / 0.5
    if p < 0.88:
        return 1.0
    return max(0.0, 1 - (p - 0.88) / 0.1)


class S(SpokenScene):
    def rt(self, cue, lead=0.2, mn=0.4):
        return max(mn, self.t_of(cue) - lead - self.elapsed())

    def upto(self, cue, *anims, lead=0.2, mn=0.4):
        r = self.rt(cue, lead, mn)
        if anims:
            self.play(AnimationGroup(*anims, run_time=r))
        else:
            self.wait(r)


class S00Title(TitleCard):
    LESSON = "The Cell Theory and Its Evidence"
    TITLE = "Where Do New Cells Come From?"


class S01Question(S):
    def construct(self):
        names = ["made of cells", "cell: basic unit", "arise from pre-existing cells", "metabolism in cells",
                 "DNA passed on", "same basic make-up"]
        rows = VGroup()
        for i, n in enumerate(names):
            box = RoundedRectangle(corner_radius=0.14, width=6.1, height=0.74, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.12)
            t = T(f"{i + 1}  {n}", 28, TEXT).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
            rows.add(VGroup(box, t))
        rows.arrange(DOWN, buff=0.14).move_to([-3.6, 0.2, 0])
        head = T("the six ideas of the cell theory", 28, TEXT).move_to([-3.6, 3.25, 0])
        self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.15, run_time=1.2))
        self.at("every cell comes")
        r3 = rows[2]
        self.play(r3[0].animate.set_stroke(ORANGE, 6).set_fill(ORANGE, 0.3), r3[1].animate.set_color(ORANGE), run_time=0.9)
        shimmer(r3[0], 0.3, 2.0)
        self.at("The first scientists")
        others = VGroup(*[rows[i] for i in (0, 1, 3, 4, 5)])
        self.play(others.animate.set_opacity(0.35), r3.animate.scale(1.1, about_point=r3.get_left()), run_time=2.0)
        self.upto("So where did", Indicate(r3, color=ORANGE, scale_factor=1.04))
        q = VGroup(T("?", 150, ORANGE, weight=BOLD), T("where do new", 36, TEXT), T("cells come from?", 36, TEXT)).arrange(DOWN, buff=0.12).move_to([3.9, 1.2, 0])
        self.play(FadeIn(q, shift=LEFT * 0.3), run_time=1.0)
        breathe(q[0], 0.06, 2.4)
        self.upto("By the", Indicate(q[1:], color=YELLOW, scale_factor=1.06))
        mic = lm_icon(1.9).move_to([3.9, -1.7, 0])
        lab = T("1830s: improved microscopes", 28, GOLD).move_to([3.4, -3.3, 0])
        self.play(FadeIn(mic, shift=LEFT * 1.5), FadeIn(lab, shift=LEFT * 1.0), run_time=1.5)
        breathe(mic, 0.04, 2.6)
        self.at("The argument")
        self.play(Indicate(mic, color=GOLD, scale_factor=1.15), run_time=1.6)
        self.finish()


class S02Compare(S):
    def construct(self):
        plant = plant_tissue([LEFT_X, PCY, 0])
        animal = animal_tissue([RIGHT_X, PCY, 0])
        hl = VGroup(T("1838 Schleiden", 32, GREENT, weight=BOLD), T("plant tissue", 30, GREENT)).arrange(DOWN, buff=0.08).move_to([LEFT_X, 2.75, 0])
        hr = VGroup(T("1839 Schwann", 32, PINKT, weight=BOLD), T("tadpole cartilage", 30, PINKT)).arrange(DOWN, buff=0.08).move_to([RIGHT_X, 2.75, 0])
        self.at("Matthias")
        self.play(FadeIn(plant.panel), FadeIn(hl, shift=DOWN * 0.15), run_time=0.8)
        self.play(LaggedStart(*[Create(c) for c in plant.cells], lag_ratio=0.03, run_time=3.2))
        for i, c in enumerate(plant.cells):
            if i % 4 == 0:
                breathe(c, 0.05, 2.6 + 0.1 * (i % 5), i)
        self.at("1839")
        self.play(FadeIn(animal.panel), FadeIn(hr, shift=DOWN * 0.15), run_time=0.8)
        self.upto("such as", LaggedStart(*[FadeIn(c, scale=0.6) for c in animal.cells], lag_ratio=0.035, run_time=3.0), mn=1.0)
        for i, c in enumerate(animal.cells):
            if i % 4 == 0:
                breathe(c[0], 0.05, 2.7 + 0.1 * (i % 5), i)
        self.upto("He found", Indicate(animal.panel, color=PINKT, scale_factor=1.02))
        self.at("same cellular plan")
        pl, an = plant.mark, animal.mark
        self.play(Indicate(pl, color=YELLOW, scale_factor=1.9), Indicate(an, color=YELLOW, scale_factor=1.9), run_time=1.6)
        sb = stack_behind([LEFT_X, PCY, 0], PW, PH, GREENT, -1)
        sa = stack_behind([RIGHT_X, PCY, 0], PW, PH, PINKT, 1)
        for s in (sb, sa):
            s.set_z_index(-1)
        lab = T("many plant and animal tissues compared (examples)", 28, TEXT).move_to([0, -3.2, 0])
        self.play(FadeIn(sb, shift=DOWN * 0.1), FadeIn(sa, shift=DOWN * 0.1), FadeIn(lab), run_time=1.2)
        self.finish()


class S03Comparison(S):
    def construct(self):
        plant = plant_tissue([LEFT_X, PCY, 0])
        animal = animal_tissue([RIGHT_X, PCY, 0])
        sb = stack_behind([LEFT_X, PCY, 0], PW, PH, GREENT, -1)
        sa = stack_behind([RIGHT_X, PCY, 0], PW, PH, PINKT, 1)
        for s in (sb, sa):
            s.set_z_index(-1)
        for i, c in enumerate(plant.cells):
            if i % 4 == 0:
                breathe(c, 0.05, 2.6 + 0.1 * (i % 5), i)
        for i, c in enumerate(animal.cells):
            if i % 4 == 0:
                breathe(c[0], 0.05, 2.7 + 0.1 * (i % 5), i)
        mic = lm_icon(0.9).move_to([-5.9, 3.1, 0])
        self.add(plant, animal, sb, sa, mic)
        lab = T("comparison was the key step", 38, TEXT, weight=BOLD).move_to([0.6, 3.1, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), mic.animate.set_opacity(0.25), run_time=1.4)
        eq = T("=", 100, YELLOW, weight=BOLD).move_to([0, 0.75, 0])
        self.upto("Many kinds", FadeIn(eq, scale=1.4))
        self.play(Indicate(sb, color=GREENT, scale_factor=1.02), Indicate(sa, color=PINKT, scale_factor=1.02), run_time=1.4)
        self.upto("showed one shared", Indicate(eq, color=YELLOW, scale_factor=1.2))
        pc = plant.mark.copy()
        ac = animal.mark.copy()
        backdrop = Circle(radius=0.85, stroke_color=INK, stroke_width=4, fill_color=CREAM, fill_opacity=1).move_to([0, -0.85, 0])
        shared = RoundedRectangle(corner_radius=0.3, width=1.1, height=1.1, stroke_color=INK, stroke_width=7,
                                  fill_color="#F7F0DF", fill_opacity=1).move_to([0, -0.85, 0])
        self.play(pc.animate.move_to([-0.2, -0.85, 0]).scale(1.3), ac.animate.move_to([0.2, -0.85, 0]).scale(1.3),
                  FadeIn(backdrop), run_time=1.1)
        self.play(FadeOut(pc), FadeOut(ac), FadeIn(shared), run_time=0.5)
        tag = VGroup(T("one shared", 28, YELLOW), T("plan", 28, YELLOW)).arrange(DOWN, buff=0.05).move_to([0, -2.35, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.6)
        shimmer(shared, 0.3, 2.0)
        breathe(backdrop, 0.03, 2.8)
        self.at("That was evidence")
        ev = T("plants and animals alike: made of cells", 32, TEXT).move_to([0, -3.35, 0])
        self.play(FadeIn(ev, shift=UP * 0.1), Indicate(plant.panel, color=GREENT, scale_factor=1.03),
                  Indicate(animal.panel, color=PINKT, scale_factor=1.03), run_time=2.4)
        self.finish()


class S04Fluid(S):
    def construct(self):
        c = np.array([0.0, -0.3, 0.0])
        pl = pool(c, 9.0, 3.6)
        g = ValueTracker(0.0)
        base, sp = specks(c, 9.0, 3.6, g, n=18, ring=(0, 0), ring_r=0.8)
        self.play(FadeIn(pl), run_time=0.8)
        self.add(base, sp)
        self.at("also thought")
        lab = T("structureless fluid", 36, TEAL, weight=BOLD).move_to([0, 2.15, 0])
        self.upto("structureless", FadeIn(lab, shift=DOWN * 0.1), mn=0.8)
        self.at("Picture a crystal")
        self.play(g.animate.set_value(1.0), run_time=self.rt("No cell divides", 0.3, 2.0), rate_func=smooth)
        self.at("No cell divides")
        nd = T("no cell divides", 38, TEAL, weight=BOLD).move_to([0, -2.75, 0])
        self.play(FadeIn(nd, shift=UP * 0.1), run_time=1.0)
        self.upto("Schladen proposed", Indicate(nd, color=TEAL, scale_factor=1.08))
        lt = chip("plants: Schleiden", GREENT, 30).move_to([-4.0, 3.25, 0])
        self.play(FadeIn(lt, shift=DOWN * 0.15), run_time=0.8)
        self.upto("Schwann extended", Indicate(lt, color=GREENT, scale_factor=1.1))
        rt_ = chip("animals: Schwann", PINKT, 30).move_to([4.0, 3.25, 0])
        self.play(FadeIn(rt_, shift=DOWN * 0.15), run_time=0.8)
        old = T("fluid idea: historical, wrong", 32, TEAL).move_to([0, -3.4, 0])
        self.play(FadeIn(old, shift=UP * 0.1), Indicate(rt_, color=PINKT, scale_factor=1.1), run_time=1.5)
        self.finish()


class S05Models(S):
    def construct(self):
        div = Line([0, 3.7, 0], [0, -3.0, 0], color=GREY, stroke_width=2)
        hl = T("fluid model", 40, TEAL, weight=BOLD).move_to([-3.4, 3.0, 0])
        hr = T("division model", 40, ORANGE, weight=BOLD).move_to([3.4, 3.0, 0])
        self.play(Create(div), run_time=0.6)
        self.at("models")
        self.play(FadeIn(hl, shift=DOWN * 0.15), FadeIn(hr, shift=DOWN * 0.15), run_time=1.0)
        lc = np.array([-3.4, 0.1, 0.0])
        rc = np.array([3.4, 0.1, 0.0])
        pl = pool(lc, 5.6, 3.6)
        g = ValueTracker(0.0)
        base, sp = specks(lc, 5.6, 3.6, g, n=16, ring=(0, 0), ring_r=0.7, seed=3)
        lt = clock_tracker(self, 7.0, on=False)
        g.add_updater(lambda m: m.set_value(loop_profile(lt.get_value())))
        self.at("fluid model")
        self.play(FadeIn(pl), run_time=0.8)
        self.add(base, sp)
        lt._on = True
        self.upto("and no cell", Indicate(hl, color=TEAL, scale_factor=1.1))
        nd = T("no cell divides", 32, TEAL).move_to([-3.4, -2.2, 0])
        self.play(FadeIn(nd, shift=UP * 0.1), run_time=0.8)
        self.upto("In the division", Indicate(nd, color=TEAL, scale_factor=1.08))
        panel = RoundedRectangle(corner_radius=0.25, width=5.6, height=3.6, stroke_color=ORANGE, stroke_width=5,
                                 fill_color=CREAM, fill_opacity=1).move_to(rc)
        rtr = clock_tracker(self, 7.0, on=False)
        loop = division_loop(rc, 0.9, rtr)
        self.play(FadeIn(panel), run_time=0.8)
        self.add(loop)
        self.at("one existing")
        rtr._on = True
        st = T("one cell splits in two", 32, ORANGE).move_to([3.4, -2.2, 0])
        self.play(FadeIn(st, shift=UP * 0.1), run_time=0.8)
        sch = T("schematic", 28, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(sch), run_time=0.6)
        self.finish()


def predict_boxes():
    bl = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.3, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.1).move_to([-3.2, -1.35, 0])
    br = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.3, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.1).move_to([3.2, -1.35, 0])
    tl = T("if fluid model:", 32, TEAL, weight=BOLD).move_to([-3.2, -0.05, 0])
    tr_ = T("if division model:", 32, ORANGE, weight=BOLD).move_to([3.2, -0.05, 0])
    return bl, br, tl, tr_


def tissue_panel():
    c = np.array([0.0, 1.85, 0.0])
    panel = RoundedRectangle(corner_radius=0.2, width=8.4, height=2.1, stroke_color=GREY, stroke_width=4, fill_color=CREAM, fill_opacity=1).move_to(c)
    pts = [(-3.3, 0.35), (-2.0, -0.5), (-0.9, 0.4), (0.4, -0.35), (1.5, 0.45), (2.7, -0.3), (3.5, 0.5), (-2.9, -0.55), (0.0, 0.5)]
    cells = VGroup(*[Circle(radius=0.34, stroke_color=INK, stroke_width=4, fill_color="#F7F0DF", fill_opacity=1).move_to(c + np.array([x, y, 0]))
                     for x, y in pts])
    head = T("a growing tissue (schematic)", 28, TEXT).move_to([0, 3.4, 0])
    return panel, cells, head


class S06Predict(S):
    def construct(self):
        panel, cells, head = tissue_panel()
        self.play(FadeIn(panel), FadeIn(head), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cells], lag_ratio=0.25, run_time=2.4))
        for i, c in enumerate(cells):
            breathe(c, 0.06, 2.4 + 0.2 * (i % 3), i)
        self.at("What would each")
        bl, br, tl, tr_ = predict_boxes()
        q1 = T("?", 120, TEAL, weight=BOLD).move_to([-3.2, -1.5, 0])
        q2 = T("?", 120, ORANGE, weight=BOLD).move_to([3.2, -1.5, 0])
        self.play(FadeIn(bl), FadeIn(br), FadeIn(tl), FadeIn(tr_), run_time=0.9)
        self.play(FadeIn(q1, scale=0.5), FadeIn(q2, scale=0.5), run_time=0.8)
        breathe(q1, 0.1, 1.6)
        breathe(q2, 0.1, 1.6, 1.0)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        panel, cells, head = tissue_panel()
        bl, br, tl, tr_ = predict_boxes()
        q1 = T("?", 120, TEAL, weight=BOLD).move_to([-3.2, -1.5, 0])
        q2 = T("?", 120, ORANGE, weight=BOLD).move_to([3.2, -1.5, 0])
        for i, c in enumerate(cells):
            breathe(c, 0.06, 2.4 + 0.2 * (i % 3), i)
        breathe(q1, 0.1, 1.6)
        breathe(q2, 0.1, 1.6, 1.0)
        self.add(panel, cells, head, bl, br, tl, tr_, q1, q2)
        tmr = ValueTracker(0.0)
        ring = always_redraw(lambda: VGroup(
            Circle(radius=0.38, stroke_color=GREY, stroke_width=3).move_to([6.1, 3.2, 0]),
            Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * max(0.001, 1 - tmr.get_value()), stroke_color=YELLOW, stroke_width=9).move_arc_center_to([6.1, 3.2, 0])))
        self.add(ring)
        self.play(tmr.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        self.finish()


class S08Reveal(S):
    def construct(self):
        panel, cells, head = tissue_panel()
        bl, br, tl, tr_ = predict_boxes()
        for i, c in enumerate(cells):
            breathe(c, 0.06, 2.4 + 0.2 * (i % 3), i)
        q1 = T("?", 120, TEAL, weight=BOLD).move_to([-3.2, -1.5, 0])
        q2 = T("?", 120, ORANGE, weight=BOLD).move_to([3.2, -1.5, 0])
        self.add(panel, cells, head, bl, br, tl, tr_, q1, q2)
        # fluid box
        lc = np.array([-3.2, -1.4, 0.0])
        pl = pool(lc, 4.8, 1.7)
        g = ValueTracker(0.0)
        base, sp = specks(lc, 4.8, 1.7, g, n=14, ring=(0, 0), ring_r=0.5, seed=5)
        self.play(FadeOut(q1), FadeIn(pl), run_time=0.8)
        self.add(base, sp)
        self.upto("with no", g.animate.set_value(1.0), mn=1.5)
        nd = T("no cell divided", 32, TEAL, weight=BOLD).move_to([-3.2, -2.7, 0])
        self.play(FadeIn(nd, shift=UP * 0.1), run_time=0.8)
        self.upto("The division model", Indicate(bl, color=TEAL, scale_factor=1.02))
        # counter
        ctr = {"n": 1}

        def counter(n):
            return VGroup(T("cells", 30, TEXT), M(str(n), 48, ORANGE, weight=BOLD)).arrange(RIGHT, buff=0.25).move_to([5.6, 3.35, 0])
        cobj = counter(1)
        self.play(FadeOut(q2), FadeIn(cobj), run_time=0.8)
        xs = [-1.8, -0.6, 0.6, 1.8]
        frames = []
        for x in xs:
            fr = RoundedRectangle(corner_radius=0.1, width=1.1, height=1.1, stroke_color=ORANGE, stroke_width=3, fill_color=CREAM, fill_opacity=1).move_to([3.2 + x, -1.3, 0])
            frames.append(fr)
        pcs = [0.0, 0.34, 0.5, 0.9]
        contents = []
        for x, p in zip(xs, pcs):
            m = div_mobs([3.2 + x, -1.3, 0], 0.27, p)
            contents.append(m)
        self.upto("a series", FadeIn(frames[0]))
        st = T("a series of stages", 32, ORANGE, weight=BOLD).move_to([3.2, -2.7, 0])
        self.play(FadeIn(st, shift=UP * 0.1), FadeIn(frames[0]), FadeIn(contents[0]), run_time=1.0)
        self.upto("One cell", Indicate(frames[0], color=YELLOW, scale_factor=1.12))
        self.play(FadeIn(frames[1]), FadeIn(contents[1]), run_time=0.8)
        self.at("in two")
        n2 = counter(2)
        self.play(FadeIn(frames[2]), FadeIn(contents[2]), Transform(cobj, n2), run_time=1.0)
        self.at("then its")
        n4 = counter(4)
        self.play(FadeIn(frames[3]), FadeIn(contents[3]), Transform(cobj, n4), run_time=1.2)
        self.upto("Watching over time", Indicate(frames[3], color=YELLOW, scale_factor=1.12))
        clk = VGroup(Circle(radius=0.3, stroke_color=TEXT, stroke_width=4),
                     Line(ORIGIN, UP * 0.2, color=TEXT, stroke_width=4), Line(ORIGIN, RIGHT * 0.14, color=TEXT, stroke_width=4))
        clk.move_to([-0.9, -3.45, 0])
        ot = T("over time", 30, TEXT).move_to([0.45, -3.45, 0])
        self.play(FadeIn(clk), FadeIn(ot), run_time=0.8)
        hand = clk[1]
        hand.add_updater(lambda m, dt: m.rotate(-1.4 * dt, about_point=clk[0].get_center()))
        self.finish()


class S09Remak(S):
    def construct(self):
        y0 = -3.4
        tl = Line([-6.2, y0, 0], [6.2, y0, 0], color=GREY, stroke_width=5)
        self.play(Create(tl), run_time=0.8)
        d1 = Dot([-3.3, y0, 0], radius=0.14, color=ORANGE)
        e1 = VGroup(T("1852 Remak", 32, ORANGE, weight=BOLD), T("new cells form by division", 28, TEXT)).arrange(DOWN, buff=0.06).move_to([-3.3, -2.65, 0])
        self.play(FadeIn(d1, scale=2), FadeIn(e1, shift=UP * 0.1), run_time=0.9)
        # growing division panel
        pc = np.array([0.0, 0.55, 0.0])
        icon_c = np.array([-3.3, -1.7, 0.0])
        mini = VGroup(disc(icon_c + LEFT * 0.3, 0.28), disc(icon_c + RIGHT * 0.3, 0.28))
        mini.set_stroke(ORANGE, 5)
        self.upto("new cells form", FadeIn(mini, scale=0.5), mn=0.8)
        panel = RoundedRectangle(corner_radius=0.25, width=10.6, height=4.1, stroke_color=ORANGE, stroke_width=6, fill_color=CREAM, fill_opacity=1).move_to(pc)
        rtr = clock_tracker(self, 8.0)
        loop = division_loop(pc, 1.05, rtr)
        self.play(FadeOut(mini), GrowFromCenter(panel), run_time=1.6)
        self.add(loop)
        self.at("In 1855")
        d2 = Dot([3.3, y0, 0], radius=0.14, color=ORANGE)
        self.play(FadeIn(d2, scale=2), run_time=0.8)
        e2 = VGroup(T("1855 Virchow", 32, ORANGE, weight=BOLD), T("spread the idea widely", 28, TEXT)).arrange(DOWN, buff=0.06).move_to([3.3, -2.65, 0])
        self.upto("Rudolf", Indicate(d2, color=YELLOW, scale_factor=2))
        self.play(FadeIn(e2, shift=UP * 0.1), run_time=0.9)
        self.at("Every cell comes")
        big = T("Every cell comes from a cell", 44, ORANGE, weight=BOLD).move_to([0, 3.3, 0])
        self.play(Write(big), run_time=2.0)
        self.upto("Remack's", Indicate(big, color=YELLOW, scale_factor=1.04))
        self.play(Indicate(e1, color=YELLOW, scale_factor=1.12), run_time=1.5)
        self.at("Virchow made")
        self.play(Indicate(e2, color=YELLOW, scale_factor=1.12), run_time=1.5)
        self.finish()


class S10Dropped(S):
    def construct(self):
        # teal fluid-model panel (left slot) and the kept core (right slot)
        slotL, slotR = np.array([-3.6, 0.1, 0.0]), np.array([3.6, 0.1, 0.0])
        tp = VGroup(RoundedRectangle(corner_radius=0.25, width=5.4, height=3.8, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.18),
                    T("fluid model", 38, TEAL, weight=BOLD).shift(UP * 1.25)).move_to(slotL)
        g = ValueTracker(0.0)
        lt = clock_tracker(self, 7.0)
        g.add_updater(lambda m: m.set_value(loop_profile(lt.get_value())))
        base, sp = specks(slotL + DOWN * 0.45, 4.6, 2.2, g, n=14, ring=(0, 0), ring_r=0.55, seed=2)
        core = VGroup(RoundedRectangle(corner_radius=0.25, width=5.4, height=3.8, stroke_color=INK, stroke_width=5, fill_color=CREAM, fill_opacity=1),
                      RoundedRectangle(corner_radius=0.3, width=1.5, height=1.5, stroke_color=INK, stroke_width=8, fill_color="#F7F0DF", fill_opacity=1).shift(UP * 0.2),
                      T("one shared plan", 30, INK, weight=BOLD).shift(DOWN * 1.3)).move_to(slotR)
        self.add(tp, base, sp, core)
        shimmer(core[1], 0.3, 2.0)
        breathe(core[1], 0.04, 2.6)
        self.upto("so it was", Indicate(tp, color=TEAL, scale_factor=1.03), mn=0.8)
        slash = Line(slotL + np.array([-2.7, 1.9, 0]), slotL + np.array([2.7, -1.9, 0]), color=RED, stroke_width=12)
        self.play(Create(slash), run_time=0.8)
        old = VGroup(tp, slash)
        self.play(FadeOut(sp), old.animate.shift(LEFT * 10), run_time=1.3, rate_func=smooth)
        self.remove(base, sp)
        self.at("The core stayed")
        head = T("the cell theory, corrected", 38, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(head, shift=DOWN * 0.15), core.animate.scale(1.04), run_time=1.0)
        ck = T("core kept", 34, GREEN, weight=BOLD).move_to([3.6, -2.35, 0])
        self.upto("plants and animals", FadeIn(ck, shift=UP * 0.1))
        self.play(Indicate(core, color=GREEN, scale_factor=1.04), run_time=2.0)
        self.at("A corrected idea")
        op = VGroup(RoundedRectangle(corner_radius=0.25, width=5.4, height=3.8, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.18),
                    T("every cell comes", 38, ORANGE, weight=BOLD).shift(UP * 0.7),
                    T("from a cell", 38, ORANGE, weight=BOLD).shift(UP * 0.1)).move_to(slotL + LEFT * 9)
        tag = VGroup(T("corrected idea,", 28, ORANGE), T("replacing the fluid idea", 28, ORANGE)).arrange(DOWN, buff=0.05).move_to(slotL + LEFT * 9 + DOWN * 1.1)
        grp = VGroup(op, tag)
        self.play(grp.animate.shift(RIGHT * 9), run_time=2.2, rate_func=smooth)
        self.upto("Cells come from", Indicate(op, color=ORANGE, scale_factor=1.03))
        self.play(Indicate(op[1:], color=YELLOW, scale_factor=1.08), run_time=1.5)
        self.finish()


class S11Theory(S):
    def construct(self):
        bc = np.array([1.9, 0.4, 0.0])
        box = RoundedRectangle(corner_radius=0.2, width=4.5, height=1.7, stroke_color=YELLOW, stroke_width=6, fill_color=YELLOW, fill_opacity=0.12).move_to(bc)
        bt = T("scientific theory", 36, YELLOW, weight=BOLD).move_to(bc)
        self.play(FadeIn(box, scale=0.8), FadeIn(bt), run_time=1.2)
        breathe(box, 0.02, 3.0)
        self.upto("well tested", Indicate(box, color=YELLOW, scale_factor=1.05), mn=1.0)
        chips = [chip("plant tissues", GREENT, 30), chip("animal tissues", PINKT, 30), chip("cells dividing", ORANGE, 30)]
        ys = [2.1, 0.4, -1.3]
        arrs = []
        for ch, y in zip(chips, ys):
            ch.move_to([-4.6, y, 0])
            arrs.append(Arrow(ch.get_right() + RIGHT * 0.1, [bc[0] - 2.3, bc[1] + (y - bc[1]) * 0.4, 0], color=TEXT, stroke_width=5, buff=0.05, tip_length=0.25))
        self.at("tied to")
        for ch, a in zip(chips, arrs):
            self.play(FadeIn(ch, shift=RIGHT * 0.2), GrowArrow(a), run_time=0.8)
            self.wait(0.3)
        self.upto("When strong", Indicate(box, color=YELLOW, scale_factor=1.04))
        tag = chip("fluid idea", TEAL, 30).move_to([bc[0], 2.1, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=1.0)
        self.upto("it can be", Indicate(tag, color=TEAL, scale_factor=1.1))
        eraser = VGroup(RoundedRectangle(corner_radius=0.08, width=1.0, height=0.6, stroke_color=TEXT, stroke_width=3, fill_color="#E58AA0", fill_opacity=1),
                        Rectangle(width=0.35, height=0.6, stroke_width=0, fill_color=GREY, fill_opacity=1).shift(RIGHT * 0.33)).move_to(tag.get_center() + RIGHT * 3.2 + UP * 0.2)
        self.play(FadeIn(eraser), run_time=0.4)
        self.play(eraser.animate.move_to(tag.get_center() + LEFT * 1.6), tag.animate.set_opacity(0.0), run_time=1.6)
        self.play(FadeOut(eraser), run_time=0.4)
        self.at("Being revised")
        bub = RoundedRectangle(corner_radius=0.3, width=3.6, height=1.0, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([bc[0], -2.6, 0])
        gt = T("just a guess", 32, TEXT).move_to(bub)
        self.play(FadeIn(bub), FadeIn(gt), run_time=0.9)
        x = Line(bub.get_corner(UL) + DR * 0.1, bub.get_corner(DR) + UL * 0.1, color=RED, stroke_width=10)
        self.play(Create(x), run_time=1.0)
        self.finish()


class S12Scope(S):
    def construct(self):
        st = VGroup(T("every cell comes", 42, ORANGE, weight=BOLD), T("from a cell", 42, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([-3.4, 2.5, 0])
        self.play(FadeIn(st, shift=DOWN * 0.15), run_time=1.0)
        shimmer(st[0], 0.2, 2.2)
        shimmer(st[1], 0.2, 2.2)
        sep = DashedLine([0.7, 3.5, 0], [0.7, -3.4, 0], color=GREY, stroke_width=3)
        self.upto("Every cell comes", Create(sep), mn=1.0)
        self.at("Every cell comes")
        panel = animal_tissue([-3.4, -0.45, 0], 5.6, 3.0)
        for i, c in enumerate(panel.cells):
            if i % 3 == 0:
                breathe(c[0], 0.06, 2.4 + 0.1 * (i % 4), i)
        self.play(FadeIn(panel.panel), LaggedStart(*[FadeIn(c, scale=0.6) for c in panel.cells], lag_ratio=0.05, run_time=2.4))
        self.upto("living today", Indicate(panel.panel, color=PINKT, scale_factor=1.02), lead=0.0)
        tg = chip("cells living today", TEXT, 30).move_to([-3.4, -2.75, 0])
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.8)
        self.at("How the very first")
        qm = T("?", 200, GREY, weight=BOLD).move_to([3.9, 0.9, 0])
        qm.set_opacity(0.0)
        self.play(qm.animate.set_opacity(0.85), run_time=1.5)
        t0 = {"t": 0.0}

        def bob(m, dt):
            t0["t"] += dt
            m.move_to([3.9 + 0.12 * math.sin(t0["t"] * 0.8), 0.9 + 0.18 * math.sin(t0["t"] * 1.3), 0])
        qm.add_updater(bob)
        lab = VGroup(T("the very first cells:", 30, TEXT), T("a separate question", 30, TEXT)).arrange(DOWN, buff=0.08).move_to([3.9, -1.6, 0])
        self.upto("that scientists", FadeIn(lab, shift=UP * 0.1), mn=1.0)
        self.at("that scientists")
        self.play(Indicate(lab, color=YELLOW, scale_factor=1.06), run_time=2.0)
        self.finish()


class S13End(EndCard):
    LINE = "A theory keeps what evidence supports and drops what it does not."
