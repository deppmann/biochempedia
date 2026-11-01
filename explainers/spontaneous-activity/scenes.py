"""Retinal waves: inputs that fire in step are kept  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = cells and axons of one eye (and the retina in the opening scenes)
  ORANGE = cells and axons of the other eye
  YELLOW = firing: a spike, a burst, a wave
  PURPLE = the thalamic cell (the target)
  GREEN  = strengthened / kept
  RED    = weakened
  GREY   = structure, outlines, labels, silence
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BLUE_D = "#2B7A92"
ORANGE_D = "#A8631F"


def cell(x, y, color=BLUE, r=0.3):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
    return c.move_to([x, y, 0])


def lit_updater(cells, tracker, color, halfw=0.5):
    for c in cells:
        def upd(m, color=color):
            on = abs(m.get_x() - tracker.get_value()) < halfw
            m.set_fill(YELLOW if on else color, opacity=1.0 if on else 0.25)
            m.set_stroke(YELLOW if on else color)
        c.add_updater(upd)


def unlit(cells, color):
    for c in cells:
        c.clear_updaters()
        c.set_fill(color, opacity=0.25).set_stroke(color)


def sweep_band(tracker, h, y):
    band = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.14)
    band.add_updater(lambda m: m.move_to([tracker.get_value(), y, 0]))
    return band


def seg_end(p, q, r):
    """point on the circle of radius r about q, toward p."""
    p, q = np.array(p, float), np.array(q, float)
    d = (p - q) / np.linalg.norm(p - q)
    return q + d * r


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Activity before experience: spontaneous retinal waves"
    TITLE = "Inputs that fire in step are kept"


# --------------------------------------------------------------------------------------------
class S01Wave(SpokenScene):
    """a retina fires in waves before the eyes open; the question: why send this to the brain?"""

    def construct(self):
        cols, rows, sp = 10, 5, 0.74
        gx, gy = -2.35, 0.95
        cells = VGroup(*[cell(gx + (i - (cols - 1) / 2) * sp, gy + (j - (rows - 1) / 2) * sp, BLUE, 0.24)
                         for j in range(rows) for i in range(cols)])
        outline = RoundedRectangle(corner_radius=0.5, width=cols * sp + 0.5, height=rows * sp + 0.45,
                                   stroke_color=GREY, stroke_width=3).move_to([gx, gy, 0])
        head = T("newborn ferret: eyes not yet open", 26, GREY).move_to([gx, 3.2, 0])
        tr = ValueTracker(gx - 4.3)
        band = sweep_band(tr, rows * sp + 0.3, gy)

        self.at("A newborn")
        self.play(FadeIn(outline), FadeIn(head), FadeIn(cells, lag_ratio=0.02), run_time=1.2)
        self.at("retina is already firing")
        lit_updater(cells, tr, BLUE)
        self.add(band)
        self.play(tr.animate.set_value(gx + 4.3), run_time=2.4, rate_func=linear)
        self.remove(band)
        unlit(cells, BLUE)
        tr.set_value(gx - 4.3)

        self.at("Ganglion cells")
        head2 = T("ganglion cells: the retina's output neurons", 26, BLUE).move_to([gx, 3.2, 0])
        self.play(ReplacementTransform(head, head2), Indicate(cells, color=BLUE, scale_factor=1.12), run_time=1.0)

        self.at("Each burst sweeps")
        lit_updater(cells, tr, BLUE)
        self.add(band)
        self.play(tr.animate.set_value(gx + 4.3), run_time=2.4, rate_func=linear)
        self.remove(band)
        unlit(cells, BLUE)

        # timeline: bursts a few seconds long, a minute or two apart
        self.at("minute or two")
        by = -2.0
        base = Line([-6.3, by, 0], [1.6, by, 0], color=GREY, stroke_width=3)
        rng = np.random.RandomState(4)

        def burst(x0):
            return VGroup(*[Line([x, by, 0], [x, by + 0.65, 0], color=YELLOW, stroke_width=4)
                            for x in x0 + np.sort(rng.uniform(0, 0.9, 7))])
        b1, b2 = burst(-5.9), burst(-0.9)
        gap = DoubleArrow([-4.6, by - 0.3, 0], [-1.2, by - 0.3, 0], color=GREY, stroke_width=3, buff=0,
                          tip_length=0.18)
        gap_l = T("silence: a minute or two", 24, GREY).move_to([-2.9, by - 0.75, 0])
        burst_l = T("burst: a few seconds", 24, YELLOW).move_to([-5.0, by - 1.3, 0])
        self.play(Create(base), FadeIn(b1), FadeIn(burst_l), run_time=0.8)
        self.play(GrowFromCenter(gap), FadeIn(gap_l), run_time=0.7)
        self.play(FadeIn(b2), run_time=0.4)

        self.at("Nothing is being seen")
        self.play(Indicate(outline, color=GREY, scale_factor=1.03), run_time=0.8)
        self.at("why send this pattern")
        nerve = Arrow([gx + cols * sp / 2 + 0.35, gy, 0], [3.9, gy, 0], buff=0, color=GREY, stroke_width=5)
        nerve_l = T("optic nerve", 24, GREY).next_to(nerve, UP, buff=0.12)
        brain = RoundedRectangle(corner_radius=0.3, width=2.4, height=2.4, stroke_color=GREY, stroke_width=3
                                 ).move_to([5.2, gy, 0])
        q = T("?", 90, TEXT, weight=BOLD).move_to(brain)
        brain_l = T("brain", 28, GREY).next_to(brain, DOWN, buff=0.2)
        self.play(GrowArrow(nerve), FadeIn(nerve_l), run_time=0.7)
        self.play(FadeIn(brain), FadeIn(brain_l), Write(q), run_time=0.8)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S02Timing(SpokenScene):
    """the wave passes cells in a row; neighbours fire close together, a far cell fires late."""

    def construct(self):
        xs = [-5.6, -4.9, -4.2, -0.5, 5.2]
        cy = 2.3
        cells = VGroup(*[cell(x, cy, BLUE, 0.28) for x in xs])
        nums = VGroup(*[T(str(i + 1), 24, GREY).move_to([x, cy + 0.72, 0]) for i, x in enumerate(xs)])
        strip = Line([-6.4, cy, 0], [6.4, cy, 0], color=GREY, stroke_width=2).set_z_index(-1)
        retina_l = T("retina: position", 24, GREY).move_to([1.9, cy + 0.95, 0])
        # raster
        ry = [0.9, 0.2, -0.5, -1.2, -1.9]
        x0, k = -3.0, 0.6
        rows_l = VGroup(*[T(str(i + 1), 24, GREY).move_to([-4.0, y, 0]) for i, y in enumerate(ry)])
        guides = VGroup(*[Line([-3.5, y, 0], [4.6, y, 0], color=GREY, stroke_width=1, stroke_opacity=0.5) for y in ry])
        tr = ValueTracker(-6.6)
        ticks = VGroup()
        for i, (x, y) in enumerate(zip(xs, ry)):
            tx = x0 + (x - xs[0]) * k
            for d in (0.0, 0.1, 0.2):
                t = Line([tx + d, y - 0.22, 0], [tx + d, y + 0.22, 0], color=YELLOW, stroke_width=5)
                t.add_updater(lambda m, x=x: m.set_stroke(opacity=1.0 if tr.get_value() > x - 0.3 else 0.0))
                ticks.add(t)
        axis = Arrow([-3.5, -2.55, 0], [4.9, -2.55, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        axis_l = T("time (schematic)", 24, GREY).next_to(axis, DOWN, buff=0.15).align_to(axis, RIGHT)
        band = sweep_band(tr, 1.0, cy)

        self.at("The wave moves")
        self.play(FadeIn(strip), FadeIn(cells), FadeIn(nums), FadeIn(retina_l), run_time=0.8)
        self.play(FadeIn(guides), FadeIn(rows_l), GrowArrow(axis), FadeIn(axis_l), run_time=0.8)
        self.add(ticks)
        lit_updater(cells, tr, BLUE, halfw=0.45)
        self.add(band)
        self.play(tr.animate.set_value(6.7), run_time=3.6, rate_func=linear)
        self.remove(band)
        unlit(cells, BLUE)
        for t in ticks:
            t.clear_updaters()

        self.at("Cells near each other")
        near = SurroundingRectangle(VGroup(*ticks[0:9]), color=TEXT, buff=0.12, corner_radius=0.1, stroke_width=3)
        near_l = T("close in time", 26, TEXT).next_to(near, RIGHT, buff=0.25)
        self.play(Create(near), FadeIn(near_l), Indicate(cells[0:3], color=YELLOW), run_time=0.9)
        self.at("Cells far apart")
        far = SurroundingRectangle(ticks[12:15], color=GREY, buff=0.12, corner_radius=0.1, stroke_width=3)
        far_l = T("far apart in time", 26, GREY).next_to(far, LEFT, buff=0.25)
        self.play(Create(far), FadeIn(far_l), Indicate(cells[4], color=GREY), run_time=0.9)
        self.at("So when a cell fires")
        self.play(FadeOut(near), FadeOut(near_l), FadeOut(far), FadeOut(far_l), run_time=0.5)
        when = T("when", 36, YELLOW, weight=BOLD)
        where = T("where", 36, BLUE, weight=BOLD)
        eq = T("reflects", 26, GREY)
        back = Rectangle(width=5.4, height=0.9, stroke_width=0, fill_color=BG, fill_opacity=0.0).move_to([0, 1.55, 0])
        when.move_to([-1.9, 1.55, 0])
        eq.move_to([0.0, 1.55, 0])
        where.move_to([1.9, 1.55, 0])
        grp = VGroup(back, when, eq, where)
        self.play(FadeIn(grp), run_time=0.6)
        self.play(Indicate(where, color=BLUE, scale_factor=1.25), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
def build_stage():
    """three inputs and one thalamic cell, the same place in S03 and S04."""
    d = {}
    d["a1"] = cell(-5.4, 1.7, BLUE, 0.32)
    d["a2"] = cell(-5.4, 0.5, BLUE, 0.32)
    d["b1"] = cell(-5.4, -1.7, ORANGE, 0.32)
    d["la"] = T("one eye", 26, BLUE).move_to([-5.4, 2.6, 0])
    d["lb"] = T("other eye", 26, ORANGE).move_to([-5.4, -0.95, 0])
    d["tgt"] = Circle(radius=0.9, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.28
                      ).move_to([3.4, 0, 0])
    d["lt"] = T("thalamic cell", 26, PURPLE).move_to([3.4, -1.5, 0])
    d["lth"] = T("thalamus", 26, GREY).move_to([3.4, 1.55, 0])
    tp = d["tgt"].get_center()
    for k, col in (("a1", BLUE), ("a2", BLUE), ("b1", ORANGE)):
        s = d[k].get_center()
        a = s + (tp - s) / np.linalg.norm(tp - s) * 0.34
        b = seg_end(s, tp, 0.9)
        d["w" + k] = Line(a, b, color=col, stroke_width=4)
    return d


def fire(scene, st, keys, drive=True, rt=0.9):
    dots = [Dot(st["w" + k].get_start(), radius=0.13, color=YELLOW) for k in keys]
    scene.add(*dots)
    scene.play(*[st[k].animate.set_fill(YELLOW, 1.0).set_stroke(YELLOW) for k in keys], run_time=0.15)
    anims = []
    for k, dot in zip(keys, dots):
        col = BLUE if k.startswith("a") else ORANGE
        anims += [dot.animate.move_to(st["w" + k].get_end()), st[k].animate.set_fill(col, 0.25).set_stroke(col)]
    scene.play(*anims, run_time=rt, rate_func=linear)
    scene.remove(*dots)
    if drive:
        scene.play(Indicate(st["tgt"], color=YELLOW, scale_factor=1.12), run_time=0.5)


class S03TwoEyes(SpokenScene):
    def construct(self):
        st = build_stage()
        self.at("Now follow the signal")
        self.play(FadeIn(st["a1"]), FadeIn(st["a2"]), FadeIn(st["b1"]), FadeIn(st["la"]), FadeIn(st["lb"]), run_time=0.9)
        self.at("Axons from")
        self.play(*[Create(st["w" + k]) for k in ("a1", "a2", "b1")], run_time=1.0)
        self.at("reach the thalamus")
        self.play(FadeIn(st["tgt"]), FadeIn(st["lth"]), run_time=0.8)
        self.at("two eyes overlap")
        fire(self, st, ["a1", "a2"], drive=False, rt=1.0)
        fire(self, st, ["b1"], drive=False, rt=1.0)
        self.at("One thalamic cell")
        self.play(FadeIn(st["lt"]), Indicate(st["tgt"], color=PURPLE, scale_factor=1.12), run_time=0.8)
        self.at("cells of one")
        fire(self, st, ["a1", "a2"])
        self.at("and from the other eye")
        fire(self, st, ["b1"], drive=False)
        self.at("largely independent")
        fire(self, st, ["a1", "a2"])
        fire(self, st, ["b1"], drive=False)
        self.at("own schedule")
        fire(self, st, ["a1", "a2"])
        self.wait(0.2)
        fire(self, st, ["b1"], drive=False)
        self.finish()


class S04Hebb(SpokenScene):
    def construct(self):
        A = Circle(radius=0.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to([-3.2, 0.3, 0])
        B = Circle(radius=0.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to([3.2, 0.3, 0])
        la = T("cell A", 30, GREY).next_to(A, DOWN, buff=0.3)
        lb = T("cell B", 30, GREY).next_to(B, DOWN, buff=0.3)
        link = Line(A.get_right(), B.get_left(), color=GREY, stroke_width=3)

        self.at("proposed a rule")
        self.play(FadeIn(A), FadeIn(B), FadeIn(la), FadeIn(lb), Create(link), run_time=1.0)
        self.at("repeatedly takes part")
        for i in range(3):
            dot = Dot(A.get_right(), radius=0.14, color=YELLOW)
            self.add(dot)
            self.play(dot.animate.move_to(B.get_left()), Indicate(A, color=YELLOW, scale_factor=1.12),
                      link.animate.set_stroke(GREEN, width=3 + 2.5 * (i + 1)), run_time=0.7, rate_func=linear)
            self.remove(dot)
            self.play(Indicate(B, color=YELLOW, scale_factor=1.12), run_time=0.4)
        self.at("apply the rule")
        self.play(FadeOut(VGroup(A, B, la, lb, link)), run_time=0.6)
        st = build_stage()
        self.play(*[FadeIn(st[k]) for k in ("a1", "a2", "b1", "la", "lb", "tgt", "lt", "lth", "wa1", "wa2", "wb1")], run_time=0.8)
        self.at("same wave")
        fire(self, st, ["a1", "a2"])
        self.at("they are strengthened")
        lbl_s = T("strengthened", 28, GREEN, weight=BOLD).move_to([-1.0, 2.2, 0])
        self.play(st["wa1"].animate.set_stroke(GREEN, width=10), st["wa2"].animate.set_stroke(GREEN, width=10),
                  FadeIn(lbl_s), run_time=0.9)
        self.at("rarely helps")
        fire(self, st, ["b1"], drive=False)
        self.at("it is weakened")
        lbl_w = T("weakened", 28, RED, weight=BOLD).move_to([-1.0, -2.2, 0])
        self.play(st["wb1"].animate.set_stroke(RED, width=1.5, opacity=0.5), FadeIn(lbl_w), run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------------------------
class S05Sort(SpokenScene):
    def construct(self):
        px, py, pw, ph = -0.8, 0.35, 8.6, 4.5
        panel = RoundedRectangle(corner_radius=0.3, width=pw, height=ph, stroke_color=GREY, stroke_width=3).move_to([px, py, 0])
        pl = T("thalamus", 26, GREY).move_to([px, py + ph / 2 + 0.4, 0])
        n = 18

        def snake(y1, y2):
            pts = []
            xs = [px - 3.2 + 0.8 * i for i in range(9)]
            for i in range(9):
                pts.append([xs[i], y1, 0])
            for i in range(9):
                pts.append([xs[8 - i], y2, 0])
            return pts
        tb = snake(py + 1.55, py + 0.85)
        to = snake(py - 0.85, py - 1.55)

        def shade(c0, c1, k):
            return interpolate_color(ManimColor(c0), ManimColor(c1), k / (n - 1))
        rng = np.random.RandomState(11)
        pos = []
        while len(pos) < 2 * n:
            p = np.array([rng.uniform(px - pw / 2 + 0.4, px + pw / 2 - 0.4), rng.uniform(py - ph / 2 + 0.4, py + ph / 2 - 0.4), 0])
            if all(np.linalg.norm(p - q) > 0.62 for q in pos):
                pos.append(p)
        dots_b = VGroup(*[Dot(pos[i], radius=0.2, color=shade(BLUE, BLUE_D, i)) for i in range(n)])
        dots_o = VGroup(*[Dot(pos[n + i], radius=0.2, color=shade(ORANGE, ORANGE_D, i)) for i in range(n)])

        leg = VGroup(Dot(radius=0.14, color=BLUE), T("one eye", 24, BLUE), Dot(radius=0.14, color=ORANGE), T("other eye", 24, ORANGE)
                     ).arrange(RIGHT, buff=0.2).move_to([px, py - ph / 2 - 0.4, 0])
        self.play(FadeIn(panel), FadeIn(pl), FadeIn(dots_b), FadeIn(dots_o), FadeIn(leg), run_time=0.3)
        self.at("Repeat this")
        self.play(Indicate(VGroup(dots_b, dots_o), scale_factor=1.05, color=YELLOW), run_time=0.8)
        self.at("separate territories")
        div = DashedLine([px - pw / 2 + 0.2, py, 0], [px + pw / 2 - 0.2, py, 0], color=GREY, stroke_width=2)
        self.play(*[dots_b[i].animate.move_to(tb[i]) for i in range(n)],
                  *[dots_o[i].animate.move_to(to[i]) for i in range(n)],
                  FadeOut(leg), Create(div), run_time=3.0)
        self.at("next to each other")
        hl = SurroundingRectangle(VGroup(dots_b[0], dots_b[1], dots_b[2]), color=TEXT, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.play(Create(hl), run_time=0.6)
        self.play(hl.animate.move_to(VGroup(dots_b[3], dots_b[4], dots_b[5]).get_center()), run_time=0.7)
        self.play(FadeOut(hl), run_time=0.3)
        self.at("two kinds of information")
        self.play(Indicate(panel, color=GREY, scale_factor=1.02), run_time=0.7)
        self.at("Which eye")
        arr = DoubleArrow([px + pw / 2 + 0.5, py + 1.2, 0], [px + pw / 2 + 0.5, py - 1.2, 0], color=TEXT, stroke_width=4, buff=0, tip_length=0.2)
        lw = T("which eye", 26, TEXT).next_to(arr, RIGHT, buff=0.15)
        self.play(GrowFromCenter(arr), FadeIn(lw), run_time=0.8)
        self.at("roughly where")
        ar2 = Arrow([px - 3.6, py - ph / 2 - 0.35, 0], [px + 3.6, py - ph / 2 - 0.35, 0], color=TEXT, stroke_width=4, buff=0, tip_length=0.2)
        lw2 = T("where in that eye", 26, TEXT).next_to(ar2, DOWN, buff=0.12)
        self.play(GrowArrow(ar2), FadeIn(lw2), run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------------------------
class S06Pattern(SpokenScene):
    def construct(self):
        cxn, cxk = -3.3, 3.3
        pw = 5.6

        def panel(cx, title, tcol):
            h = T(title, 30, tcol, weight=BOLD).move_to([cx, 3.05, 0])
            box = RoundedRectangle(corner_radius=0.25, width=pw, height=2.35, stroke_color=GREY, stroke_width=2
                                   ).move_to([cx, 1.6, 0])
            return h, box
        hn, bn = panel(cxn, "normal mouse", TEXT)
        hk, bk = panel(cxk, "beta2 knockout", TEXT)
        ry = [2.3, 1.95, 1.6, 1.25, 0.9]

        def ticks_norm(cx):
            rng = np.random.RandomState(2)
            g = VGroup()
            for y in ry:
                for b in (-1.9, 0.6):
                    x0 = cx + b + rng.uniform(-0.1, 0.1)
                    for d in (0.0, 0.25, 0.5):
                        g.add(Line([x0 + d, y - 0.12, 0], [x0 + d, y + 0.12, 0], color=YELLOW, stroke_width=4))
            return g

        def ticks_ko(cx):
            rng = np.random.RandomState(5)
            g = VGroup()
            for y in ry:
                for x in np.sort(rng.uniform(cx - pw / 2 + 0.3, cx + pw / 2 - 0.3, 17)):
                    g.add(Line([x, y - 0.12, 0], [x, y + 0.12, 0], color=YELLOW, stroke_width=3))
            return g

        tn, tk = ticks_norm(cxn), ticks_ko(cxk)
        slot_n = T("waves: neighbours in step", 24, GREY).move_to([cxn, 0.2, 0])

        def zone(cx, sigma, peak):
            ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.1, 1], x_length=5.0, y_length=1.9, tips=False,
                      axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 2}
                      ).move_to([cx, -1.45, 0])
            g = ax.plot(lambda x: peak * np.exp(-((x - 5) ** 2) / (2 * sigma ** 2)), x_range=[0, 10], color=BLUE, stroke_width=5)
            fill = ax.get_area(g, x_range=[0, 10], color=BLUE, opacity=0.25)
            lab = VGroup(T("axon endings in midbrain, day 8", 24, GREY), T("schematic", 24, GREY)).arrange(DOWN, buff=0.1).move_to([cx, -3.0, 0])
            return ax, g, fill, lab
        axn, gn, fn, ln = zone(cxn, 0.65, 1.0)
        axk, gk, fk, lk = zone(cxk, 2.0, 0.34)

        qa = chip("amount of activity?", GREY, 30)
        qb = chip("pattern of activity?", YELLOW, 30)
        qs = VGroup(qa, qb).arrange(RIGHT, buff=0.8).move_to([0, 0.6, 0])
        self.at("amount of activity")
        self.play(FadeIn(qa, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(qb, shift=UP * 0.2), run_time=0.6)

        self.at("lacking the")
        self.play(FadeOut(qs), FadeIn(hn), FadeIn(hk), FadeIn(bn), FadeIn(bk), run_time=0.8)
        self.at("no waves")
        slot_k = T("no waves", 24, GREY).move_to([cxk, 0.2, 0])
        self.play(FadeIn(tn), FadeIn(slot_n), FadeIn(slot_k), run_time=0.7)
        self.at("fired at high rates")
        slot_k2 = T("many spikes", 24, YELLOW).move_to([cxk, 0.2, 0])
        self.play(FadeIn(tk, lag_ratio=0.01), ReplacementTransform(slot_k, slot_k2), run_time=1.4)
        self.at("without correlation")
        slot_k3 = T("not in step", 24, RED).move_to([cxk, 0.2, 0])
        self.play(ReplacementTransform(slot_k2, slot_k3), run_time=0.5)
        self.at("stayed broad")
        self.play(FadeIn(axn), FadeIn(axk), FadeIn(ln), FadeIn(lk), run_time=0.3)
        self.play(Create(gn), FadeIn(fn), Create(gk), FadeIn(fk), run_time=0.8)
        self.at("Later work")
        slot_k4 = T("lacks normal waves", 24, GREY).move_to([cxk, 0.2, 0])
        self.play(ReplacementTransform(slot_k3, slot_k4), run_time=0.6)
        self.at("lack normal waves")
        self.play(Indicate(slot_k4, color=TEXT, scale_factor=1.1), run_time=0.7)
        self.at("Keep the rule")
        self.play(FadeOut(VGroup(hn, hk, bn, bk, tn, tk, slot_n, slot_k4, axn, gn, fn, ln, axk, gk, fk, lk)), run_time=0.7)
        r1 = chip("fire in step: kept", GREEN, 40)
        r2 = chip("out of step: weakened", RED, 40)
        rr = VGroup(r1, r2).arrange(DOWN, buff=0.7).move_to([0, 0, 0])
        self.at("fire")
        self.play(FadeIn(r1, shift=UP * 0.2), run_time=0.6)
        self.at("the rest are weakened")
        self.play(FadeIn(r2, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Inputs that fire in step are kept; the rest are weakened."
