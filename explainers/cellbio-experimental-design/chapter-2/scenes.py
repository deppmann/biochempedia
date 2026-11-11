"""Ruling Out the Dull Explanations: chapter 2 of the cell-biology experimental-design film.

Same look and colour map as chapter 1 (../scenes.py):
  BLUE cells/dish, GREEN reporter/green cells, GOLD decisions + tracked division + locks,
  RED a gap or problem, TEAL treatment, GREY structure.  All cell drawings are schematic.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from bp_style import *  # noqa: F401,F403

# ---- shared helpers (same look as chapter 1) -------------------------------------------------


def arrow(a, b, color=TEXT, width=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def bench_mat():
    return RoundedRectangle(corner_radius=0.38, width=13.6, height=7.5,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.15).set_z_index(-20)


def cell_icon(color=RED, radius=0.34):
    body = Circle(radius=radius, stroke_color=BLUE, stroke_width=4,
                  fill_color=BLUE, fill_opacity=0.12)
    return VGroup(body, Dot(radius=radius * 0.42, color=color))


def daughters(scale=1.0):
    a = cell_icon(RED, 0.27).shift(LEFT * 0.38)
    b = cell_icon(RED, 0.27).shift(RIGHT * 0.38)
    return VGroup(a, b).scale(scale)


def cells_in_dish(center, cols=9, rows=4, width=4.4, height=1.4, radius=0.08):
    out = VGroup()
    for i in range(cols * rows):
        c, r = i % cols, i // cols
        x = center[0] + (c - (cols - 1) / 2) * width / (cols - 1)
        y = center[1] + ((rows - 1) / 2 - r) * height / (rows - 1)
        body = Circle(radius=radius * 1.7, stroke_color=BLUE, stroke_width=2,
                      fill_color=BLUE, fill_opacity=0.13).move_to([x, y, 0])
        out.add(VGroup(body, Dot([x, y, 0], radius=radius, color=BLUE)))
    return out


def gently_drift(mob, amplitude=0.09, speed=0.9, direction=RIGHT):
    mob.drift_clock = 0.0
    mob.drift_offset = 0.0

    def update(m, dt):
        m.drift_clock += dt
        offset = amplitude * np.sin(speed * m.drift_clock)
        m.shift(direction * (offset - m.drift_offset))
        m.drift_offset = offset
    mob.add_updater(update)
    return mob


def pulse(mob, amp=0.06, speed=2.0):
    mob.pclock = 0.0
    mob.pscale = 1.0

    def update(m, dt):
        m.pclock += dt
        s = 1 + amp * np.sin(speed * m.pclock)
        m.scale(s / m.pscale)
        m.pscale = s
    mob.add_updater(update)
    return mob


def slot(label, width=3.7):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=0.78,
                           stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.08)
    return VGroup(box, T(label, 28, TEXT).move_to(box))


def lock3(y=3.15):
    out = VGroup()
    for lab in ("prediction", "endpoint", "independent unit"):
        s = slot(lab)
        sh = Arc(radius=0.16, start_angle=0, angle=PI, color=GOLD, stroke_width=5).next_to(s, UP, buff=-0.02)
        out.add(VGroup(s, sh))
    out.arrange(RIGHT, buff=0.3).move_to([0, y, 0])
    return out


DX = 3.5            # dish centres at +-DX
DISH_Y = 1.0
CELL_Y = 1.3
QPOS = [(-6.45, -1.0, 0), (6.45, -1.0, 0), (6.45, -2.6, 0)]


def qmarks():
    out = VGroup(*[T("?", 46, GOLD, weight=BOLD).move_to(p) for p in QPOS])
    for i, q in enumerate(out):
        gently_drift(q, amplitude=0.12, speed=1.1 + 0.2 * i, direction=UP)
    return out


def dish_pair(stretched_label="stretched", control_label="unstretched", ctrl=True, stretch=True):
    """The carried world: unstretched twin on the left, stretched dish on the right."""
    parts = {}
    for key, x, name in (("ctrl", -DX, control_label), ("str", DX, stretched_label)):
        if key == "ctrl" and not ctrl:
            continue
        frame = RoundedRectangle(corner_radius=0.5, width=5.4, height=3.0, stroke_color=BLUE,
                                 stroke_width=5, fill_color=BLUE, fill_opacity=0.05).move_to([x, DISH_Y, 0])
        cells = cells_in_dish((x, CELL_Y), rows=5, height=1.8)
        gently_drift(cells, amplitude=0.1, speed=1.2)
        lab = T(name, 28, TEXT, weight=BOLD).move_to([x, -0.12, 0])
        parts[key] = VGroup(frame, cells, lab)
    if stretch:
        ar = VGroup(*[arrow([DX + sx * 1.95, CELL_Y + sy * 0.5, 0], [DX + sx * 2.5, CELL_Y + sy * 0.95, 0], TEXT, 5, 0.18)
                      for sx in (-1, 1) for sy in (-1, 1)])
        parts["arrows"] = ar
    return parts


def row_y(i):
    return -1.1 - 0.5 * i


def row(text, i, color=GOLD, white=False):
    tick = Square(0.22, color=color, fill_color=color, fill_opacity=0.9)
    t = T(text, 28, TEXT if not white else WHITE)
    g = VGroup(tick, t).arrange(RIGHT, buff=0.22)
    g.move_to([0, row_y(i), 0])
    return g


ROWS = ["handling: matched", "medium: matched preparation", "vehicle: matched",
        "scoring: blind", "strain: measured", "positive control: run"]


def rows(n):
    return VGroup(*[row(ROWS[i], i) for i in range(n)])


def tracked_path(x0=-4.0, y=-2.7, length=3.2):
    line = Line([x0, y, 0], [x0 + length, y, 0], color=GOLD, stroke_width=6)
    d = daughters(1.0).move_to([x0 + length + 1.0, y, 0])
    return VGroup(line, d)


def check(p, color=GREEN):
    x, y = p[0], p[1]
    return VGroup(Line([x - 0.2, y, 0], [x - 0.05, y - 0.18, 0]), Line([x - 0.05, y - 0.18, 0], [x + 0.25, y + 0.22, 0])
                  ).set_stroke(color, 8)


# ---- scenes ---------------------------------------------------------------------------------


def big_dish():
    """Chapter 1's dish, large and central: the opening picture."""
    frame = RoundedRectangle(corner_radius=0.55, width=6.4, height=3.2, stroke_color=BLUE,
                             stroke_width=5, fill_color=BLUE, fill_opacity=0.05).move_to([0, 0.9, 0])
    cells = cells_in_dish((0, 0.9), cols=10, rows=5, width=5.2, height=2.2, radius=0.09)
    gently_drift(cells, amplitude=0.12, speed=1.2)
    ar = VGroup(*[arrow([sx * 2.4, 0.9 + sy * 0.8, 0], [sx * 3.0, 0.9 + sy * 1.3, 0], TEXT, 5, 0.18)
                  for sx in (-1, 1) for sy in (-1, 1)])
    return frame, cells, ar


class S01Hook(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        frame, cells, ar = big_dish()
        sch = T("schematic", 26, GREY).move_to([-5.4, -3.3, 0])
        self.play(FadeIn(frame), FadeIn(cells), run_time=0.9)
        self.at("stretch dishes")
        self.play(GrowFromCenter(ar), FadeIn(sch), run_time=1.0)
        self.at("tracked divisions")
        path = tracked_path(-3.6, -2.4, 3.0)
        self.play(Create(path[0]), run_time=1.0)
        self.play(FadeIn(path[1], shift=RIGHT * 0.2), run_time=0.7)

        self.at("what else")
        cand = VGroup()
        for lab, p in (("device", (-5.3, 1.0)), ("medium", (5.3, 1.0)), ("scope", (5.3, -2.3))):
            c = chip(lab, BLUE, 28)
            c.move_to([p[0], p[1], 0])
            q = T("?", 46, GOLD, weight=BOLD).next_to(c, UP, buff=0.12)
            cand.add(VGroup(c, q))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cand], lag_ratio=0.35), run_time=1.6)
        for c in cand:
            gently_drift(c[1], amplitude=0.12, speed=1.3, direction=UP)
        self.at("chapter 1")
        locks = lock3(3.15)
        locks.shift(UP * 1.4)
        self.play(*[c[0].animate.set_opacity(0.25) for c in cand], run_time=0.6)
        self.play(locks.animate.shift(DOWN * 1.4), run_time=1.0)
        self.at("the prediction")
        self.play(Indicate(locks[0], color=GOLD), run_time=0.7)
        self.play(Indicate(locks[1], color=GOLD), run_time=0.7)
        self.play(Indicate(locks[2], color=GOLD), run_time=0.7)
        self.at("a control")
        self.play(*[c.animate.scale(1.25) for c in cand], run_time=1.0)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Designing a cell biology experiment"
    TITLE = "Ruling Out the Dull Explanations"

    def construct(self):
        self.add(bench_mat())
        frame, cells, ar = big_dish()
        qs = qmarks()
        self.add(frame, cells, ar, qs)
        title = T(self.TITLE, 42, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        P = dish_pair()
        twin = P["ctrl"]
        twin.shift(LEFT * 8)
        self.add(twin)
        self.play(Write(title), run_time=0.45)
        tgt_f = RoundedRectangle(corner_radius=0.5, width=5.4, height=2.6).move_to([DX, DISH_Y, 0])
        self.play(frame.animate.become(P["str"][0].copy()),
                  cells.animate.move_to([DX, CELL_Y, 0]).scale(0.85),
                  ar.animate.become(P["arrows"].copy()),
                  twin.animate.shift(RIGHT * 8),
                  run_time=1.0)
        self.play(FadeOut(title), run_time=0.35)
        self.finish()


class S03Handling(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        P = dish_pair()
        qs = qmarks()
        self.add(qs)
        self.play(FadeIn(P["ctrl"]), FadeIn(P["str"]), FadeIn(P["arrows"]), run_time=0.8)
        chips = [chip(t, GOLD, 28) for t in ("assemble", "mount", "image")]
        xs = [-3.9, 0.0, 3.9]
        ycen = -2.3
        for c, x in zip(chips, xs):
            c.move_to([x, ycen, 0])
        arrs = [arrow([-2.4, ycen, 0], [-1.5, ycen, 0], GOLD), arrow([1.5, ycen, 0], [2.4, ycen, 0], GOLD)]
        self.at("look at what")
        dot = Dot([-5.9, ycen, 0], radius=0.17, color=GOLD)
        self.play(FadeIn(dot), run_time=0.5)
        self.at("someone assembled")
        self.play(FadeIn(chips[0]), dot.animate.move_to([xs[0] - 1.4, ycen, 0]), run_time=0.9)
        self.at("mounted it")
        self.play(FadeIn(chips[1]), GrowArrow(arrs[0]), dot.animate.move_to([xs[1] - 1.1, ycen, 0]), run_time=0.9)
        self.at("the microscope")
        self.play(FadeIn(chips[2]), GrowArrow(arrs[1]), dot.animate.move_to([xs[2] - 1.5, ycen, 0]), run_time=0.9)
        self.at("if the control")
        gap = VGroup(Line([-0.7, CELL_Y, 0], [0.7, CELL_Y, 0], color=RED, stroke_width=8),
                     Line([-0.7, CELL_Y - 0.2, 0], [-0.7, CELL_Y + 0.2, 0], color=RED, stroke_width=8),
                     Line([0.7, CELL_Y - 0.2, 0], [0.7, CELL_Y + 0.2, 0], color=RED, stroke_width=8))
        glab = T("handling", 28, RED, weight=BOLD).move_to([0, 2.8, 0])
        self.play(FadeIn(gap), FadeIn(glab), run_time=0.9)
        self.at("stretch now includes")
        self.play(Indicate(glab, color=RED, scale_factor=1.2), run_time=1.2)
        self.at("unstretched devices")
        cdot = Dot([-5.9, ycen - 0.55, 0], radius=0.17, color=BLUE)
        self.play(FadeIn(cdot), run_time=0.4)
        self.play(cdot.animate.move_to([xs[0] - 1.4, ycen - 0.55, 0]), Indicate(chips[0], color=BLUE), run_time=1.0)
        self.at("mounted and imaged")
        self.play(cdot.animate.move_to([xs[1] - 1.1, ycen - 0.55, 0]), Indicate(chips[1], color=BLUE), run_time=0.9)
        self.at("imaged identically")
        self.play(cdot.animate.move_to([xs[2] - 1.5, ycen - 0.55, 0]), Indicate(chips[2], color=BLUE),
                  gap.animate.scale(0.05).set_opacity(0), FadeOut(glab), run_time=1.0)
        r = row(ROWS[0], 0)
        self.play(FadeIn(r, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S04Medium(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        P = dish_pair()
        qs = qmarks()
        self.add(qs, P["ctrl"], P["str"], P["arrows"], rows(1))
        self.at("the medium raises")

        def bottle(x):
            b = RoundedRectangle(corner_radius=0.12, width=0.7, height=0.95, stroke_color=TEAL, stroke_width=4,
                                 fill_color=TEAL, fill_opacity=0.18).move_to([x, 3.2, 0])
            neck = Rectangle(width=0.28, height=0.22, color=TEAL, stroke_width=4).next_to(b, UP, buff=0)
            return VGroup(b, neck)
        bl, br = bottle(-1.7), bottle(1.7)
        bl.shift(UP * 1.5)
        br.shift(UP * 1.5)
        self.play(bl.animate.shift(DOWN * 1.5), br.animate.shift(DOWN * 1.5), run_time=1.2)
        self.at("wnt")
        wcell = cell_icon(GOLD, 0.3).move_to([3.0, 3.25, 0])
        block = Square(0.2, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to(wcell.get_top() + UP * 0.02)
        wl = T("Wnt3A L cell", 26, GOLD).next_to(wcell, RIGHT, buff=0.15)
        self.play(FadeIn(wcell), FadeIn(block), FadeIn(wl), run_time=0.9)
        self.play(arrow([2.7, 3.25, 0], [2.15, 3.25, 0], GOLD, 4, 0.15).animate.set_opacity(1).scale(1) if False else
                  Create(arrow([2.7, 3.25, 0], [2.1, 3.25, 0], GOLD, 4, 0.15)), run_time=0.5)
        self.at("the matched control")
        pcell = cell_icon(RED, 0.3).move_to([-6.2, 3.25, 0])
        pl = T("parental L cell", 26, TEXT).next_to(pcell, RIGHT, buff=0.15)
        self.play(FadeIn(pcell), FadeIn(pl), Create(arrow([-3.5, 3.25, 0], [-2.3, 3.25, 0], TEXT, 4, 0.15)), run_time=0.9)
        self.at("prepared the same way")
        d1 = Dot([1.7, 2.6, 0], radius=0.12, color=TEAL)
        d2 = Dot([-1.7, 2.6, 0], radius=0.12, color=TEAL)
        self.play(d1.animate.move_to([1.7, 1.7, 0]), d2.animate.move_to([-1.7, 1.7, 0]), run_time=1.0)
        r = row(ROWS[1], 1)
        self.play(FadeIn(r, shift=UP * 0.2), FadeOut(d1), FadeOut(d2), run_time=0.7)
        self.at("even that cannot")
        specks = VGroup()
        for b, xs in ((bl, -1.7), (br, 1.7)):
            for dx, dy, k in ((-0.12, -0.2, 0.09), (0.1, 0.0, 0.07), (-0.05, 0.2, 0.06)):
                specks.add(Polygon([xs + dx - k, -k + 3.2 + dy, 0], [xs + dx + k * 1.3, 3.2 + dy - k * 0.4, 0],
                                   [xs + dx, 3.2 + dy + k, 0], color=TEXT, fill_color=TEXT, fill_opacity=0.8, stroke_width=1))
        q = T("other differences?", 30, TEXT, weight=BOLD).move_to([0, -2.6, 0])
        self.play(FadeIn(specks), FadeIn(q), run_time=0.8)
        self.play(specks.animate.scale(1.5), rate_func=there_and_back, run_time=1.2)
        self.play(specks.animate.scale(1.5), rate_func=there_and_back, run_time=1.2)
        self.finish()


class S05Readout(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        cell = Circle(radius=2.5, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.1).move_to([-1.2, 0.3, 0])
        nuc = Circle(radius=1.9, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.12).move_to([-1.2, 0.3, 0])
        wl = T("Wnt3A dish", 30, TEXT, weight=BOLD).move_to([-1.2, 3.25, 0])
        sch = T("schematic", 26, GREY).move_to([-5.4, -3.3, 0])
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(wl), FadeIn(sch), run_time=1.0)
        self.at("topdgfp")
        gbox = Rectangle(width=0.8, height=3.4, color=GREEN, stroke_width=4).move_to([3.0, 0.4, 0])
        glab = T("TOPdGFP signal", 28, GREEN, weight=BOLD).move_to([3.0, 2.5, 0])
        tr = ValueTracker(0.04)
        fill = always_redraw(lambda: Rectangle(width=0.8, height=max(0.02, 3.4 * tr.get_value()), stroke_width=0,
                                               fill_color=GREEN, fill_opacity=0.85).move_to(
            [3.0, 0.4 - 1.7 + 1.7 * tr.get_value(), 0]))
        self.play(Create(gbox), FadeIn(glab), FadeIn(fill), run_time=1.0)
        self.at("green reporter")
        self.play(Indicate(glab, color=GREEN), run_time=0.9)
        self.at("beta catenin responsive sites")
        bar = Rectangle(width=2.6, height=0.18, color=GREY, fill_color=GREY, fill_opacity=0.9).move_to([-1.2, -0.35, 0])
        bar_l = T("responsive sites", 26, TEXT).move_to([-1.2, -0.8, 0])
        tcf = chip("TCF", GOLD, 26).move_to([-1.2, 0.13, 0])
        self.play(FadeIn(bar), FadeIn(bar_l), FadeIn(tcf), run_time=0.8)
        bc = chip("β-catenin", TEAL, 26).move_to([-1.2, 1.35, 0])
        self.play(FadeIn(bc, shift=UP * 0.3), run_time=0.7)
        self.play(bc.animate.next_to(tcf, UP, buff=0.0), run_time=1.0)
        self.at("its signal")
        self.play(tr.animate.set_value(0.85), run_time=6.5, rate_func=smooth)
        self.at("if it stays flat")
        ic = Circle(radius=0.8, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.1).move_to([4.6, -0.9, 0])
        ib = Rectangle(width=0.4, height=1.5, color=GREEN, stroke_width=3).move_to([5.8, -0.9, 0])
        tr2 = ValueTracker(0.12)
        ifill = always_redraw(lambda: Rectangle(width=0.4, height=1.5 * tr2.get_value(), stroke_width=0,
                                                fill_color=GREEN, fill_opacity=0.85).move_to(
            [5.8, -0.9 - 0.75 + 0.75 * tr2.get_value(), 0]))
        il = T("control medium", 26, TEXT, weight=BOLD).move_to([5.2, 0.45, 0])
        self.play(FadeIn(ic), FadeIn(ib), FadeIn(ifill), FadeIn(il), run_time=0.5)
        self.play(tr2.animate.set_value(0.16), run_time=0.7)
        self.play(tr2.animate.set_value(0.11), run_time=0.6)
        self.at("the medium may not")
        self.play(Indicate(ic, color=RED), il.animate.set_color(RED), run_time=1.2)
        self.finish()


def twin_world(n_rows=2):
    P = dish_pair()
    g = VGroup(P["ctrl"], P["str"], P["arrows"], rows(n_rows))
    return P, g


class S06Rule(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        qs = qmarks()
        P, g = twin_world(2)
        self.add(qs, g)
        path = tracked_path(3.2, -2.5, 0.0)
        path = VGroup(daughters(1.0).move_to([4.6, -1.9, 0]),
                      T("tracked division", 24, GOLD).move_to([4.3, -2.6, 0]))
        self.at("each of these")
        self.play(*[Indicate(r, color=GOLD) for r in g[3]], run_time=1.0)
        self.at("a good control")
        br = VGroup(Line([-3.4, row_y(0) + 0.3, 0], [-3.6, row_y(0) + 0.3, 0]),
                    Line([-3.6, row_y(0) + 0.3, 0], [-3.6, row_y(1) - 0.3, 0]),
                    Line([-3.6, row_y(1) - 0.3, 0], [-3.4, row_y(1) - 0.3, 0])).set_stroke(GOLD, 6)
        self.play(Create(br), run_time=1.0)
        self.at("except the one")
        r = row("stretch: yes / no", 2, WHITE, True)
        r[1].set_color(WHITE)
        self.play(FadeIn(r, shift=UP * 0.2), run_time=0.8)
        self.play(Indicate(r, color=WHITE, scale_factor=1.15), run_time=1.0)
        self.at("without that match")
        self.play(Indicate(br, color=RED), run_time=1.3)
        self.at("the dull explanation")
        self.play(qs[0].animate.set_opacity(0.2), run_time=0.8)
        self.at("the interesting one")
        self.play(qs[1].animate.set_opacity(0.2), run_time=0.8)
        self.at("then a difference")
        self.play(qs[2].animate.set_opacity(0.2), FadeIn(path), run_time=0.9)
        self.at("that step")
        a = arrow([2.0, row_y(2), 0], [3.8, -1.9, 0], GOLD, 6)
        self.play(GrowArrow(a), run_time=1.0)
        self.play(Indicate(path[0], color=GOLD), run_time=1.0)
        self.finish()


class S07DrugObserver(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        qs = qmarks()
        P, g = twin_world(2)
        self.add(qs, g)
        self.at("a drug control")
        pr = VGroup(
            RoundedRectangle(corner_radius=0.1, width=0.4, height=1.1, stroke_color=TEAL, stroke_width=4,
                             fill_color=TEAL, fill_opacity=0.15).rotate(-0.28).move_to([2.35, 3.0, 0]),
            Dot([2.1, 2.3, 0], radius=0.13, color=TEAL))
        tl = T("drug + solvent", 28, TEAL, weight=BOLD).move_to([4.6, 2.9, 0])
        self.play(FadeIn(pr), FadeIn(tl), run_time=0.9)
        self.play(pr[1].animate.move_to([2.1, 1.7, 0]), run_time=0.9)
        self.at("the drug solvent")
        pl = VGroup(
            RoundedRectangle(corner_radius=0.1, width=0.4, height=1.1, stroke_color=TEXT, stroke_width=4,
                             fill_color=TEXT, fill_opacity=0.1).rotate(-0.28).move_to([-4.65, 3.0, 0]),
            Dot([-4.9, 2.3, 0], radius=0.13, color=TEXT))
        ll = T("solvent only", 28, TEXT, weight=BOLD).move_to([-2.4, 2.9, 0])
        self.play(FadeIn(pl), FadeIn(ll), run_time=0.9)
        self.play(pl[1].animate.move_to([-4.9, 1.7, 0]), run_time=0.9)
        self.at("same concentration")
        r2 = row(ROWS[2], 2)
        self.play(FadeIn(r2, shift=UP * 0.2), FadeOut(pr[1]), FadeOut(pl[1]), run_time=0.8)
        self.at("whoever scores")
        head = Circle(radius=0.32, color=TEXT, stroke_width=4).move_to([4.3, -1.7, 0])
        body = RoundedRectangle(corner_radius=0.15, width=0.9, height=1.0, color=TEXT, stroke_width=4).next_to(head, DOWN, buff=0.05)
        scope = VGroup(Rectangle(width=0.5, height=0.8, color=BLUE, stroke_width=4),
                       Circle(radius=0.2, color=BLUE, stroke_width=3)).move_to([5.4, -2.2, 0])
        scorer = VGroup(head, body, scope)
        self.play(FadeIn(scorer), run_time=0.9)
        self.at("fixes positivity")
        bar = Rectangle(width=3.0, height=0.4, color=GREEN, fill_color=GREEN, fill_opacity=0.5).move_to([-4.7, -3.1, 0])
        tline = Line([-4.7, -3.55, 0], [-4.7, -2.65, 0], color=GOLD, stroke_width=7)
        tl2 = T("fixed in advance", 28, GOLD, weight=BOLD).move_to([-4.7, -2.2, 0])
        self.play(FadeIn(bar), run_time=0.6)
        self.play(Create(tline), FadeIn(tl2), run_time=1.0)
        self.at("before analysis")
        self.play(Indicate(tl2, color=GOLD), run_time=1.0)
        self.at("blind to condition")
        blind = Rectangle(width=0.75, height=0.14, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to(head.get_center())
        a, b = T("A", 40, TEXT, weight=BOLD).move_to([-DX, -0.12, 0]), T("B", 40, TEXT, weight=BOLD).move_to([DX, -0.12, 0])
        self.play(FadeIn(blind), Transform(P["ctrl"][2], a), Transform(P["str"][2], b), run_time=1.0)
        r3 = row(ROWS[3], 3)
        self.play(FadeIn(r3, shift=UP * 0.2), run_time=0.7)
        self.at("otherwise expectations")
        self.play(Indicate(scorer, color=RED), run_time=1.2)
        self.at("one borderline cell")
        bd = Dot([-4.2, -3.1, 0], radius=0.16, color=YELLOW)
        self.play(FadeIn(bd), run_time=0.4)
        self.play(bd.animate.move_to([-4.85, -3.1, 0]), run_time=1.0)
        self.play(bd.animate.move_to([-4.5, -3.1, 0]), run_time=1.0)
        self.finish()


class S08Strain(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        cx, cy, sq = -3.7, 0.2, 0.5
        outer = VGroup()
        for i in range(-4, 5):
            outer.add(Line([cx + i * sq, cy - 2.0, 0], [cx + i * sq, cy + 2.0, 0]))
        for j in range(-4, 5):
            outer.add(Line([cx - 2.0, cy + j * sq, 0], [cx + 2.0, cy + j * sq, 0]))
        outer.set_stroke(GREY, 2)
        mem = RoundedRectangle(corner_radius=0.3, width=4.6, height=4.6, stroke_color=BLUE, stroke_width=5,
                               fill_color=BLUE, fill_opacity=0.08).move_to([cx, cy, 0])
        ctr = VGroup(*[Square(sq, stroke_color=BLUE, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(
            [cx + (i - 1.5) * sq, cy + (j - 1) * sq, 0]) for i in range(4) for j in range(3)])
        sch = T("schematic", 26, GREY).move_to([cx, cy - 2.65, 0])
        self.play(FadeIn(mem), FadeIn(outer), run_time=0.9)
        self.add(ctr)
        gently_drift(outer, amplitude=0.03, speed=1.0, direction=UP)
        self.play(FadeIn(ctr), FadeIn(sch), run_time=0.6)
        ar = VGroup(*[arrow([cx + sx * 2.55, cy + sy * 2.1, 0], [cx + sx * 3.0, cy + sy * 2.5, 0], TEXT, 5, 0.18)
                      for sx in (-1, 1) for sy in (-1, 1)])
        self.at("measure the strain")
        self.play(GrowFromCenter(ar), ctr.animate.scale(1.35), run_time=1.6)
        self.at("analyze only")
        out = Rectangle(width=4 * sq * 1.35, height=3 * sq * 1.35, color=GOLD, stroke_width=6).move_to(ctr)
        ol = T("analyzed strained region", 26, GOLD, weight=BOLD).move_to([cx, cy + 2.85, 0])
        self.play(Create(out), FadeIn(ol), run_time=1.2)
        self.at("in the 2016")
        self.play(Indicate(out, color=GOLD), run_time=0.9)
        self.at("two biaxial devices")
        sc = 0.3
        l1 = T("live imager: about 8.5%", 26, TEXT).move_to([2.9, 1.5, 0])
        l2 = T("strain array: about 15%", 26, TEXT).move_to([2.9, 0.1, 0])
        l1.align_to([0.0, 0, 0], LEFT)
        l2.align_to([0.0, 0, 0], LEFT)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.8)
        self.at("about 8")
        b1 = Rectangle(width=0.01, height=0.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to([0, 0.95, 0])
        b1.align_to([0.0, 0, 0], LEFT)
        w1 = 8.5 * sc
        self.play(b1.animate.stretch_to_fit_width(w1, about_edge=LEFT) if False else
                  Transform(b1, Rectangle(width=w1, height=0.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to([w1 / 2, 0.95, 0])),
                  run_time=1.0)
        self.at("and 15")
        w2 = 15 * sc
        b2 = Rectangle(width=0.01, height=0.5, stroke_width=0, fill_color=PURPLE_B if False else ORANGE, fill_opacity=0.9).move_to([0.005, -0.45, 0])
        self.add(b2)
        self.play(Transform(b2, Rectangle(width=w2, height=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).move_to([w2 / 2, -0.45, 0])),
                  run_time=1.2)
        self.at("those results should not")
        dn = Line([0.0, 0.5, 0], [6.4, 0.5, 0], color=RED, stroke_width=8)
        dl = T("do not merge", 28, RED, weight=BOLD).move_to([3.4, -1.3, 0])
        self.play(Create(dn), FadeIn(dl), run_time=1.0)
        self.at("each device")
        r = row(ROWS[4], 4)
        r.move_to([3.2, -2.6, 0])
        self.play(FadeIn(r, shift=UP * 0.2), run_time=0.8)
        self.play(Indicate(b1, color=TEAL), Indicate(b2, color=ORANGE), run_time=1.2)
        self.finish()


ORANGE = "#F29E4C"


def predict_world():
    cell = Circle(radius=1.5, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.12).move_to([-3.6, 0.7, 0])
    nuc = Circle(radius=0.65, color=GREEN, fill_color=GREEN, fill_opacity=0.7, stroke_width=3).move_to(cell)
    pause = VGroup(*[Rectangle(width=0.2, height=0.7, color=TEXT, fill_color=TEXT, fill_opacity=1).move_to(
        [-5.7 + dx, 2.4, 0]) for dx in (-0.2, 0.2)])
    cl = T("stalled stretched cell", 28, TEXT, weight=BOLD).move_to([-3.6, -1.35, 0])
    field = Rectangle(width=4.6, height=3.0, color=GREY, stroke_width=4, fill_color="#05070b", fill_opacity=1).move_to([3.4, 0.7, 0])
    fl = T("DNA-damage marker", 28, GREEN, weight=BOLD).move_to([3.4, 2.65, 0])
    sch = T("schematic", 26, GREY).move_to([3.4, -1.1, 0])
    qc = VGroup(RoundedRectangle(corner_radius=0.2, width=9.2, height=0.95, stroke_color=GOLD, stroke_width=5,
                                 fill_color=GOLD, fill_opacity=0.12).move_to([0, -2.7, 0]),
                T("Blank marker = no damage?", 40, TEXT, weight=BOLD).move_to([0, -2.7, 0]))
    pulse(VGroup(cell, nuc), 0.04, 1.8)
    scan = Line([1.2, 0.7 - 1.5, 0], [1.2, 0.7 + 1.5, 0], color=GREEN, stroke_width=3).set_opacity(0.4)
    scan.sclock = 0.0

    def sweep(m, dt):
        m.sclock += dt
        x = 1.25 + 4.1 * ((m.sclock / 3.5) % 1.0)
        m.move_to([x, 0.7, 0])
    scan.add_updater(sweep)
    return cell, nuc, pause, cl, field, fl, sch, qc, scan


class S09Predict(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        cell, nuc, pause, cl, field, fl, sch, qc, scan = predict_world()
        self.at("now predict")
        self.play(FadeIn(VGroup(cell, nuc)), run_time=0.8)
        self.at("suppose stretch cells")
        self.play(FadeIn(pause), FadeIn(cl), run_time=0.9)
        self.at("suspect dna damage")
        self.play(Indicate(nuc, color=GREEN), run_time=1.2)
        self.at("you stain")
        self.play(FadeIn(field), FadeIn(fl), FadeIn(sch), run_time=0.9)
        self.add(scan)
        self.at("it stays blank")
        self.play(Indicate(field, color=GREY), run_time=1.5)
        self.at("does that blank")
        self.play(FadeIn(qc, shift=UP * 0.2), run_time=1.0)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        self.add(bench_mat())
        cell, nuc, pause, cl, field, fl, sch, qc, scan = predict_world()
        self.add(cell, nuc, pause, cl, field, fl, sch, qc, scan)
        self.wait(4.5)
        self.finish()


class S11Positive(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        field = Rectangle(width=4.6, height=2.6, color=GREY, stroke_width=4, fill_color="#05070b", fill_opacity=1).move_to([-3.5, 0.1, 0])
        fl = T("stretched dish: blank", 28, TEXT, weight=BOLD).move_to([-3.5, 1.8, 0])
        scan = Line([-5.8, -1.2, 0], [-5.8, 1.4, 0], color=GREEN, stroke_width=3).set_opacity(0.4)
        scan.sclock = 0.0

        def sweep(m, dt):
            m.sclock += dt
            m.move_to([-5.7 + 4.2 * ((m.sclock / 3.5) % 1.0), 0.1, 0])
        scan.add_updater(sweep)
        sch = T("schematic", 26, GREY).move_to([-3.5, -1.5, 0])
        self.add(field, fl, scan, sch)
        self.at("only if the assay")
        self.play(Indicate(field, color=GREY), run_time=1.0)
        self.at("ben ampile")
        dish = RoundedRectangle(corner_radius=0.3, width=4.6, height=0.9, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.08).move_to([3.5, 2.95, 0])
        dl = T("positive control: MMS", 26, TEXT, weight=BOLD).move_to(dish)
        grp = VGroup(dish, dl)
        grp.shift(RIGHT * 8)
        self.add(grp)
        self.play(grp.animate.shift(LEFT * 8), run_time=1.2)
        self.at("methylmethanesulfonate")
        pf = Rectangle(width=4.6, height=2.6, color=GREEN, stroke_width=4, fill_color="#05070b", fill_opacity=1).move_to([3.5, 0.5, 0])
        rng = np.random.default_rng(4)
        specks = VGroup(*[Dot([3.5 + rng.uniform(-2.1, 2.1), 0.5 + rng.uniform(-1.1, 1.1), 0], radius=rng.uniform(0.05, 0.1),
                              color=GREEN) for _ in range(30)])
        self.play(FadeIn(pf), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(s, scale=1.8) for s in specks], lag_ratio=0.04), run_time=1.8)
        gently_drift(specks, amplitude=0.05, speed=1.5, direction=UP)
        self.at("as a positive control")
        self.play(Indicate(grp, color=BLUE), run_time=1.0)
        self.at("it shows the assay")
        br = VGroup(Line([1.2, -1.0, 0], [1.2, -1.2, 0]), Line([1.2, -1.2, 0], [5.8, -1.2, 0]), Line([5.8, -1.2, 0], [5.8, -1.0, 0])).set_stroke(GOLD, 5)
        bl = T("assay detects this marker", 28, GOLD, weight=BOLD).move_to([3.5, -1.65, 0])
        self.play(Create(br), FadeIn(bl), run_time=1.2)
        self.at("detects damage")
        self.play(Indicate(specks, color=GREEN), run_time=1.0)
        self.at("even then")
        cards = VGroup()
        for x in (-3.5, 3.5):
            c = RoundedRectangle(corner_radius=0.15, width=4.2, height=0.7, stroke_color=TEXT, stroke_width=3,
                                 fill_color=TEXT, fill_opacity=0.08).move_to([x, -2.5, 0])
            cards.add(VGroup(c, T("other damage types?", 26, TEXT).move_to(c)))
        self.play(FadeIn(cards, shift=UP * 0.2), run_time=1.0)
        self.at("one missing marker")
        r = row(ROWS[5], 5)
        r.move_to([0, -3.3, 0])
        self.play(FadeIn(r, shift=UP * 0.2), run_time=0.8)
        self.play(*[Indicate(c, color=TEXT) for c in cards], run_time=1.5)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        self.add(bench_mat())
        P = dish_pair()
        qs = qmarks()
        self.add(qs)
        locks = lock3(3.15)
        locks.shift(UP * 1.2)
        self.play(FadeIn(P["ctrl"]), FadeIn(P["str"]), FadeIn(P["arrows"]), locks.animate.shift(DOWN * 1.2), run_time=1.2)
        self.at("unstretched twin")
        self.play(Indicate(P["ctrl"][0], color=BLUE), Indicate(P["str"][0], color=BLUE), run_time=1.0)
        self.at("they share")
        band = RoundedRectangle(corner_radius=0.25, width=12.0, height=0.7, stroke_color=GOLD, stroke_width=4,
                                fill_color=GOLD, fill_opacity=0.12).move_to([0, -1.05, 0])
        words = VGroup(*[T(w, 28, TEXT, weight=BOLD) for w in ("handling", "medium", "vehicle", "scoring")])
        words.arrange(RIGHT, buff=1.0).move_to(band)
        self.play(FadeIn(band), run_time=0.7)
        self.at("handling")
        self.play(FadeIn(words[0]), run_time=0.4)
        self.play(FadeOut(qs[0]), FadeIn(check(QPOS[0])), run_time=0.5)
        self.at("medium")
        self.play(FadeIn(words[1]), run_time=0.4)
        self.at("vehicle")
        self.play(FadeIn(words[2]), FadeOut(qs[1]), FadeIn(check(QPOS[1])), run_time=0.6)
        self.at("blinded score")
        self.play(FadeIn(words[3]), run_time=0.4)
        self.at("the strain itself")
        badge = T("stretch: measured versus zero", 30, WHITE, weight=BOLD).move_to([0, -2.05, 0])
        bb = SurroundingRectangle(badge, color=WHITE, buff=0.18, corner_radius=0.15, stroke_width=4)
        self.play(FadeIn(badge), Create(bb), FadeOut(qs[2]), FadeIn(check(QPOS[2])), run_time=1.0)
        self.at("only the stretch differs")
        self.play(Indicate(VGroup(badge, bb), color=WHITE, scale_factor=1.12), Indicate(P["str"][0], color=WHITE), run_time=1.3)
        self.at("now a difference")
        path = tracked_path(-5.0, -3.0, 3.0)
        self.play(Create(path[0]), run_time=1.0)
        self.play(FadeIn(path[1]), run_time=0.6)
        self.at("period watched")
        clock = VGroup(Circle(radius=0.4, color=GOLD, stroke_width=5),
                       Line(ORIGIN, UP * 0.28, color=GOLD, stroke_width=5), Line(ORIGIN, RIGHT * 0.2, color=GOLD, stroke_width=5)
                       ).move_to([1.8, -3.0, 0])
        cl = T("period watched", 28, GOLD, weight=BOLD).next_to(clock, RIGHT, buff=0.2)
        self.play(FadeIn(clock), FadeIn(cl), run_time=0.8)
        self.play(Rotate(clock[1], angle=-TAU, about_point=clock[0].get_center()), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "A good control differs from the treatment in one step only."
