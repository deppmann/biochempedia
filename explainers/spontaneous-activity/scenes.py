"""Timing Is the Address (chapter 1 of Activity Before Experience: Spontaneous Retinal Waves)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film; same as scenes.old.py)
  BLUE   = cells and axons of the left eye (and the retina in the opening scenes)
  ORANGE = cells and axons of the right eye
  YELLOW = firing: a spike, a burst, a wave
  PURPLE = the thalamic (target) cell
  GREEN  = strengthened / kept
  RED    = weakened / pushed out
  GREY   = structure, outlines, labels, silence
  PINK-to-TEAL ramp = position on the Eph / ephrin gradients (only in the gradient scenes)
  GOLD   = the missing half: competition (one heading)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BLUE_D = "#2B7A92"
GRAD_A = "#E86AA6"
GRAD_B = "#3FB8C0"


def ramp(k):
    return interpolate_color(ManimColor(GRAD_A), ManimColor(GRAD_B), float(np.clip(k, 0, 1)))


def cell(x, y, color=BLUE, r=0.3, op=0.25, sw=3):
    c = Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)
    return c.move_to([x, y, 0])


def lit_updater(cells, tracker, color, halfw=0.5):
    for c in cells:
        def upd(m, color=color):
            on = abs(m.get_x() - tracker.get_value()) < halfw
            m.set_fill(YELLOW if on else color, opacity=1.0 if on else 0.25)
            m.set_stroke(YELLOW if on else color)
        c.add_updater(upd)


def unlit(cells, color, op=0.25):
    for c in cells:
        c.clear_updaters()
        c.set_fill(color, opacity=op).set_stroke(color)


def sweep_band(tracker, h, y, halfw=0.9, lo=-6.3, hi=6.3):
    band = Rectangle(width=2 * halfw, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.14)

    def upd(m):
        x = tracker.get_value()
        a, b = max(x - halfw, lo), min(x + halfw, hi)
        if b - a < 0.02:
            m.set_opacity(0.0)
        else:
            m.set_opacity(1.0)
            m.set_fill(YELLOW, 0.14)
            m.stretch_to_fit_width(b - a)
            m.move_to([(a + b) / 2, y, 0])
    band.add_updater(upd)
    return band


def flash(scene, sel, color=BLUE, rt=0.2, hold=0.3):
    scene.play(*[c.animate.set_fill(YELLOW, 1.0).set_stroke(YELLOW) for c in sel], run_time=rt)
    scene.play(*[c.animate.set_fill(color, 0.25).set_stroke(color) for c in sel], run_time=hold)


CAP = "#C9CED6"   # notes and captions: grey-white, readable on the dark ground


def retina_big(op=0.2):
    cols, rows, sp = 11, 5, 1.0
    cy = -0.15
    cells = VGroup(*[cell((i - (cols - 1) / 2) * sp, cy + (j - (rows - 1) / 2) * sp, BLUE, 0.33, op)
                     for j in range(rows) for i in range(cols)])
    outline = RoundedRectangle(corner_radius=0.6, width=cols * sp + 0.9, height=rows * sp + 0.8,
                               stroke_color=GREY, stroke_width=3).move_to([0, cy, 0])
    return outline, cells


def sweep_cells(scene, cells, x0, x1, rt, h, y, color=BLUE, halfw=1.0):
    tr = ValueTracker(x0)
    band = sweep_band(tr, h, y, halfw, -5.45, 5.45)
    lit_updater(cells, tr, color, halfw)
    scene.add(band)
    scene.play(tr.animate.set_value(x1), run_time=rt, rate_func=linear)
    scene.remove(band)
    unlit(cells, color)


class S00Title(TitleCard):
    LESSON = "Activity Before Experience: Spontaneous Retinal Waves"
    TITLE = "Timing Is the Address"

    def construct(self):
        # plain fades only: the Write-on produced garbled letters
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=self.beat(0.35))
        self.wait(self.beat(0.2))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


# --------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        outline, cells = retina_big(0.12)
        lab = T("retina of a newborn ferret", 34, TEXT).move_to([0, 3.4, 0])
        sub = T("eyes not yet open", 30, CAP).move_to([0, -3.5, 0])
        self.play(FadeIn(outline), FadeIn(lab), FadeIn(cells, lag_ratio=0.02), run_time=0.9)
        rng = np.random.RandomState(3)
        sel0 = [cells[i] for i in rng.choice(len(cells), 3, replace=False)]
        self.at("eyes have not")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)
        flash(self, sel0, BLUE, 0.3, 0.5)
        self.at("Even so")
        self.at("its retina is firing")
        for _ in range(3):
            sel = [cells[i] for i in rng.choice(len(cells), 8, replace=False)]
            flash(self, sel, BLUE, 0.22, 0.3)
        self.finish()


class S02Bursts(SpokenScene):
    def construct(self):
        outline, cells = retina_big(0.12)
        lab0 = T("retina of a newborn ferret", 34, TEXT).move_to([0, 3.4, 0])
        sub = T("eyes not yet open", 30, CAP).move_to([0, -3.5, 0])
        self.add(outline, cells, lab0, sub)
        self.at("ganglion cells")
        lab2 = T("ganglion cells: the retina's output neurons", 32, CAP).move_to([0, -3.35, 0])
        tgt = cells[16]
        ptr = Arrow([tgt.get_x(), -3.15, 0], [tgt.get_x(), tgt.get_y() - 0.42, 0], buff=0, color=BLUE, stroke_width=4, tip_length=0.2)
        self.play(FadeOut(sub), run_time=0.25)
        self.play(FadeIn(lab2), FadeIn(ptr), run_time=0.2)
        self.play(Indicate(tgt, color=YELLOW, scale_factor=1.4), run_time=0.4)
        unlit(cells, BLUE, 0.2)
        self.at("fire bursts")
        sel = [cells[i] for i in (16, 17, 27, 28, 29, 39)]
        flash(self, sel, BLUE, 0.2, 0.25)
        flash(self, sel, BLUE, 0.2, 0.25)
        self.at("sweep across")
        rt = max(1.5, self.narration_s + 0.2 - self.elapsed())
        sweep_cells(self, cells, -6.9, 6.9, rt, 5.4, -0.15)
        self.finish()


class S03Why(SpokenScene):
    def construct(self):
        outline, cells = retina_big(0.2)
        self.add(outline, cells)
        ro = RoundedRectangle(corner_radius=0.5, width=4.5, height=5.0, stroke_color=GREY, stroke_width=3).move_to([-4.2, 0.3, 0])
        rc = VGroup(*[cell(-4.2 + (i - 1.5) * 1.0, 0.3 + (j - 1.5) * 1.0, BLUE, 0.34, 0.2) for j in range(4) for i in range(4)])
        rl = T("retina", 30, GREY).move_to([-4.2, 3.2, 0])
        nerve = Arrow([-1.85, 0.0, 0], [2.5, 0.0, 0], buff=0, color=GREY, stroke_width=10, tip_length=0.35)
        nl = T("optic nerve", 30, CAP).move_to([0.3, -0.65, 0])
        brain = RoundedRectangle(corner_radius=0.5, width=4.0, height=5.0, stroke_color=GREY, stroke_width=3).move_to([4.6, 0, 0])
        bl = T("brain", 30, CAP).move_to([4.6, 3.0, 0])
        ro.shift(DOWN * 0.3)
        rc.shift(DOWN * 0.3)
        rl.set_y(3.0)
        self.remove(outline, cells)
        self.add(ro, rc, rl, nerve, nl, brain, bl)
        self.play(rc.animate.set_fill(BLUE, 0.05).set_stroke(GREY, opacity=0.5), run_time=0.3)
        self.at("seen")
        sil = T("a minute or two of silence", 28, CAP).move_to([-4.2, -2.85, 0])
        self.play(FadeIn(sil), run_time=0.4)
        self.at("Why send")
        self.play(Indicate(nerve, color=YELLOW), run_time=0.5)
        self.at("to the brain")
        q = T("?", 130, TEXT, weight=BOLD).move_to([0.3, 1.5, 0])
        self.play(Write(q), run_time=0.5)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=0.6)
        self.finish()


# --------------------------------------------------------------------------------------------
class S04Draft(SpokenScene):
    def construct(self):
        ys = [2.4 - 0.8 * k for k in range(7)]
        rx = -4.6
        rcells = VGroup(*[cell(rx, y, ramp(k / 6), 0.3, 0.85, 3) for k, y in enumerate(ys)])
        rpanel = RoundedRectangle(corner_radius=0.35, width=1.7, height=6.0, stroke_color=GREY, stroke_width=3).move_to([rx, 0, 0])
        rl = T("retina", 30, GREY).move_to([rx, 3.4, 0])
        tpanel = RoundedRectangle(corner_radius=0.35, width=5.4, height=6.0, stroke_color=GREY, stroke_width=3).move_to([3.4, 0, 0])
        tl = T("thalamus, in the brain", 30, GREY).move_to([3.4, 3.4, 0])
        land = VGroup(*[Circle(radius=0.28, stroke_color=ramp(k / 6), stroke_width=3, fill_color=ramp(k / 6), fill_opacity=0.85).move_to([3.4, y, 0])
                        for k, y in enumerate(ys)])
        rng = np.random.RandomState(8)
        axons = VGroup()
        for k, y in enumerate(ys):
            pts = [[rx + 0.34, y, 0], [rx + 2.0, y + rng.uniform(-0.12, 0.12), 0], [0.2, y + rng.uniform(-0.12, 0.12), 0], [3.4 - 0.3, y + rng.uniform(-0.08, 0.08), 0]]
            a = VMobject(stroke_color=ramp(k / 6), stroke_width=5)
            a.set_points_smoothly([np.array(p) for p in pts])
            axons.add(a)
        lab = T("Eph and ephrin gradients: a rough first map", 30, TEXT).move_to([0, -3.5, 0])
        self.add(lab, tpanel, tl, land, rpanel, rl, rcells)
        self.at("wiring itself")
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.15), run_time=1.5)
        self.at("Molecules have drawn")
        self.play(*[Indicate(m, scale_factor=1.3, color=m.get_fill_color()) for m in list(rcells) + list(land)], run_time=1.0)
        self.at("rough first map")
        self.play(Indicate(lab, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
def thal_panel(cx, w=6.2, h=5.6, cy=-0.1):
    return RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])


class S05Overlap(SpokenScene):
    def construct(self):
        pL = thal_panel(-3.4)
        pR = thal_panel(3.4)
        tl = T("thalamus", 32, GREY).move_to([0, 3.4, 0])
        n = 12
        rng = np.random.RandomState(5)
        pos = []
        tries = 0
        while len(pos) < 2 * n:
            tries += 1
            p = np.array([rng.uniform(-5.8, -1.0), rng.uniform(-2.3, 1.8), 0])
            if all(np.linalg.norm(p - q) > (0.68 if tries < 5000 else 0.5) for q in pos):
                pos.append(p)
        order = rng.permutation(2 * n)
        db = VGroup(*[Dot(pos[i], radius=0.24, color=BLUE) for i in order[:n]])
        do = VGroup(*[Dot(pos[i], radius=0.24, color=ORANGE) for i in order[n:]])
        leg = VGroup(Dot(radius=0.15, color=BLUE), T("left eye's axons", 28, BLUE), Dot(radius=0.15, color=ORANGE),
                     T("right eye's axons", 28, ORANGE)).arrange(RIGHT, buff=0.2).move_to([0, -3.5, 0])
        st = T("early: overlap", 32, TEXT).move_to([-3.4, 2.3, 0])
        st2 = T("adult: separate", 32, TEXT).move_to([3.4, 2.3, 0])
        div = DashedLine([0.6, -0.1, 0], [6.2, -0.1, 0], color=GREY, stroke_width=2)
        ab = VGroup(*[Dot([1.1 + 0.85 * (i % 6) + 0.4, 1.25 if i < 6 else 0.5, 0], radius=0.24, color=BLUE) for i in range(n)])
        ao = VGroup(*[Dot([1.1 + 0.85 * (i % 6) + 0.4, -0.7 if i < 6 else -1.45, 0], radius=0.24, color=ORANGE) for i in range(n)])
        self.play(FadeIn(pL), run_time=0.3)
        self.at("thalamus")
        self.play(FadeIn(tl), run_time=0.4)
        self.at("eyes axons")
        self.play(FadeIn(db, lag_ratio=0.05), FadeIn(do, lag_ratio=0.05), FadeIn(leg), run_time=1.0)
        self.at("at first overlap")
        self.play(FadeIn(st), run_time=0.5)
        self.play(FadeIn(pR), Create(div), run_time=0.6)
        self.at("Later")
        self.play(FadeIn(st2), FadeIn(ab, lag_ratio=0.06), FadeIn(ao, lag_ratio=0.06), run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
SXS = [-2.2 + 0.8 * k for k in range(10)]   # cell x positions in the one-eye strips (label sits inside, left)
AXC, BXC = SXS[1], SXS[2]                    # the two neighbours
BARX0, BARX1 = -6.0, 6.0


def strip(y, h, color, label, hot=(), cr=0.3, lab_y=None, lab_x=-4.6):
    outline = RoundedRectangle(corner_radius=0.4, width=12.8, height=h, stroke_color=GREY, stroke_width=3).move_to([0, y, 0])
    cs = []
    cy = y if lab_y is None else y - 0.45
    for k, x in enumerate(SXS):
        if k in hot:
            cs.append(cell(x, cy, color, cr, 0.55, 4))
        else:
            cs.append(cell(x, cy, color, cr, 0.1, 2).set_stroke(color, opacity=0.4))
    lab = T(label, 26, color).move_to([lab_x, y if lab_y is None else lab_y, 0])
    return outline, VGroup(*cs), cs, lab


def grad_bar(y, h):
    n = 80
    w = (BARX1 - BARX0) / n
    return VGroup(*[Rectangle(width=w + 0.01, height=h, stroke_width=0, fill_color=ramp(i / (n - 1)), fill_opacity=1
                              ).move_to([BARX0 + w * (i + 0.5), y, 0]) for i in range(n)])


def build_s06(big=True):
    d = {}
    if big:
        d["outline"], d["cells"], cs, d["lab"] = strip(1.9, 2.4, BLUE, "left eye: retina", hot=(1, 2), cr=0.34, lab_y=2.65)
        cy, bar_y, bar_h = cs[1].get_y(), -0.55, 0.9
        d["A"], d["B"] = cs[1], cs[2]
        top = cy - 0.34
        d["br"] = DoubleArrow([AXC, 2.15, 0], [BXC, 2.15, 0], buff=0, color=TEXT, stroke_width=3, tip_length=0.1)
        d["brl"] = T("20 µm apart", 26, TEXT).move_to([-1.0, 2.65, 0])
        d["bar"] = grad_bar(bar_y, bar_h)
        d["barl"] = T("Eph and ephrin gradients", 28, TEXT).move_to([3.4, -1.5, 0])
        end_y = bar_y + bar_h / 2 + 0.25
        d["lines"] = VGroup(*[Line([x, top, 0], [x, end_y, 0], color=BLUE, stroke_width=4) for x in (AXC, BXC)])
        d["tris"] = VGroup(*[Triangle(color=BLUE, fill_opacity=1, stroke_width=0).scale(0.16).rotate(PI).move_to([x, end_y, 0]) for x in (AXC, BXC)])
        d["same"] = VGroup(T("both read nearly", 32, TEXT), T("the same value", 32, TEXT)).arrange(DOWN, buff=0.12).move_to([3.4, -2.55, 0])
    else:
        d["outline"], d["cells"], cs, d["lab"] = strip(2.85, 1.3, BLUE, "left eye: retina", hot=(1, 2), cr=0.3)
        d["A"], d["B"] = cs[1], cs[2]
        bar_y, bar_h = 0.6, 0.7
        d["bar"] = grad_bar(bar_y, bar_h)
        d["barl"] = T("Eph and ephrin gradients", 28, TEXT).move_to([3.4, 1.6, 0])
        d["lines"] = VGroup(*[Line([x, 2.5, 0], [x, bar_y + bar_h / 2 + 0.25, 0], color=BLUE, stroke_width=4) for x in (AXC, BXC)])
        d["tris"] = VGroup(*[Triangle(color=BLUE, fill_opacity=1, stroke_width=0).scale(0.16).rotate(PI).move_to([x, bar_y + bar_h / 2 + 0.25, 0]) for x in (AXC, BXC)])
        d["same"] = VGroup(T("both read nearly", 28, TEXT), T("the same value", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([3.4, -0.35, 0])
    d["cs"] = cs
    d["nums"] = VGroup(T("1", 26, TEXT, weight=BOLD).move_to(cs[1]), T("2", 26, TEXT, weight=BOLD).move_to(cs[2]))
    if big:
        Group(d["outline"], d["cells"], d["lab"], d["nums"], d["br"], d["brl"]).shift(DOWN * 0.9)
        for line, c in zip(d["lines"], (d["A"], d["B"])):
            line.put_start_and_end_on(c.get_bottom(), line.get_end())
    return d


class S06Problem(SpokenScene):
    def construct(self):
        d = build_s06(True)
        self.add(d["outline"], d["cells"], d["lab"], d["bar"])
        self.at("side by side")
        self.play(FadeIn(d["nums"]), GrowFromCenter(d["br"]), FadeIn(d["brl"]), run_time=0.8)
        self.at("sit at")
        self.play(Indicate(d["bar"], scale_factor=1.02), run_time=0.7)
        self.at("almost the same")
        self.play(Create(d["lines"]), FadeIn(d["tris"]), run_time=0.8)
        self.at("on the gradients")
        self.play(FadeIn(d["barl"]), FadeIn(d["same"], shift=UP * 0.1), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S07Third(SpokenScene):
    def construct(self):
        big = build_s06(True)
        old = Group(big["outline"], big["cells"], big["lab"], big["nums"], big["br"], big["brl"], big["bar"], big["barl"],
                    big["lines"], big["tris"], big["same"])
        self.add(old)
        d = build_s06(False)
        base = Group(d["outline"], d["cells"], d["lab"], d["nums"], d["bar"], d["barl"], d["lines"], d["tris"])
        out2, cells2, cs2, lab2 = strip(-1.7, 1.3, ORANGE, "right eye: retina", hot=(1,), cr=0.3)
        C = cs2[1]
        bar_bot = 0.6 - 0.35
        line3 = Line([AXC, -1.4, 0], [AXC, bar_bot - 0.25, 0], color=ORANGE, stroke_width=4)
        tri3 = Triangle(color=ORANGE, fill_opacity=1, stroke_width=0).scale(0.16).move_to([AXC, bar_bot - 0.25, 0])
        c3 = T("3", 26, TEXT, weight=BOLD).move_to(C)
        same3 = VGroup(T("all three read nearly", 28, TEXT), T("the same value", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([3.4, -0.35, 0])
        tag = chip("eye tag", ORANGE, 28, 0.14).move_to([AXC, -3.3, 0])
        tagl = Line([AXC, -2.35, 0], [AXC, tag.get_top()[1], 0], color=ORANGE, stroke_width=3)
        tagt = VGroup(T("molecular cues differ", 28, TEXT), T("somewhat between the eyes", 28, TEXT)).arrange(DOWN, buff=0.08).move_to([3.7, -3.1, 0])
        self.play(FadeOut(old), FadeIn(base), FadeIn(out2), FadeIn(cells2), FadeIn(lab2), run_time=0.6)
        self.at("matching point")
        self.play(Indicate(C, color=ORANGE, scale_factor=1.3), FadeIn(c3), Create(line3), FadeIn(tri3), run_time=0.9)
        self.play(ReplacementTransform(d["same"], same3) if False else FadeIn(same3), run_time=0.6)
        self.at("molecular cues")
        self.play(FadeIn(tag, shift=UP * 0.15), Create(tagl), run_time=0.7)
        self.at("differ somewhat")
        self.play(FadeIn(tagt, shift=UP * 0.1), run_time=0.7)
        self.at("It still has to")
        everything = Group(base, out2, cells2, lab2, line3, tri3, c3, same3, tag, tagl, tagt)
        panel = RoundedRectangle(corner_radius=0.5, width=11.4, height=5.6, stroke_color=GREY, stroke_width=3).move_to([0, -0.1, 0])
        top = T("left eye's territory", 28, BLUE).move_to([-3.6, 2.2, 0])
        bot = T("right eye's territory", 28, ORANGE).move_to([-3.6, -2.4, 0])
        div = DashedLine([-5.5, -0.1, 0], [5.5, -0.1, 0], color=GREY, stroke_width=2)
        pl = T("thalamus", 30, GREY).move_to([4.6, 3.35, 0])
        pa = VGroup(Dot([-0.7, 1.05, 0], radius=0.3, color=BLUE), T("1", 26, BG, weight=BOLD).move_to([-0.7, 1.05, 0]))
        pb = VGroup(Dot([0.7, 1.05, 0], radius=0.3, color=BLUE), T("2", 26, BG, weight=BOLD).move_to([0.7, 1.05, 0]))
        pc = VGroup(Dot([0.0, -1.35, 0], radius=0.3, color=ORANGE), T("3", 26, BG, weight=BOLD).move_to([0.0, -1.35, 0]))
        same_l = DashedLine([0.0, 0.6, 0], [0.0, -0.95, 0], color=GREY, stroke_width=2)
        self.play(FadeOut(everything), run_time=0.6)
        self.play(FadeIn(panel), FadeIn(pl), FadeIn(top), FadeIn(bot), Create(div), FadeIn(pa), FadeIn(pb), run_time=0.9)
        self.at("different territory")
        self.play(Create(same_l), FadeIn(pc, scale=1.6), run_time=0.8)
        self.at("cues alone")
        warn = T("the cues alone do not finish the job", 32, TEXT).move_to([0, -3.45, 0])
        self.play(FadeIn(warn, shift=UP * 0.1), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
class S08Timing(SpokenScene):
    def construct(self):
        cells = VGroup(*[cell((i - 7) * 0.8, 0.75 + (j - 2) * 0.92, BLUE, 0.32) for j in range(5) for i in range(15)])
        outline = RoundedRectangle(corner_radius=0.5, width=12.8, height=4.7, stroke_color=GREY, stroke_width=3).move_to([0, 0.75, 0])
        lab = T("left eye: retina", 30, BLUE).move_to([0, 3.5, 0])
        self.play(FadeIn(outline), FadeIn(cells, lag_ratio=0.01), FadeIn(lab), run_time=1.2)
        self.at("Watch a wave")
        v = 2.5
        tr = ValueTracker(-6.9)
        band = sweep_band(tr, 4.5, 0.75, 0.9)
        lit_updater(cells, tr, BLUE, 0.9)
        self.add(band)

        def leg(cue, *extra):
            target = self.t_of(cue) - 0.2
            dt = max(0.1, target - self.elapsed())
            self.play(tr.animate.set_value(tr.get_value() + v * dt), *extra, run_time=dt, rate_func=linear)
        speed = M("about 100 µm per second", 42, YELLOW).move_to([0, -2.0, 0])
        leg("100 micrometers")
        leg("a second", FadeIn(speed, shift=UP * 0.1))
        box = Rectangle(width=1.6, height=0.7, stroke_color=GREY, stroke_width=2, fill_color=YELLOW, fill_opacity=0.1).move_to([-5.3, -3.15, 0])
        tks = VGroup(*[Line([-5.95 + 0.14 * k + 0.1, -3.4, 0], [-5.95 + 0.14 * k + 0.1, -2.9, 0], color=YELLOW, stroke_width=4)
                       for k in range(0, 10) if k % 2 == 0 or k in (5, 7)])
        note = T("a burst lasts a few seconds: we take 2 s", 30, TEXT).move_to([0.9, -3.15, 0])
        rt = max(0.5, self.narration_s + 0.2 - self.elapsed())
        self.play(tr.animate.set_value(tr.get_value() + v * 0.6), FadeIn(box), FadeIn(tks), FadeIn(note), run_time=0.6, rate_func=linear)
        self.play(tr.animate.set_value(tr.get_value() + v * max(0.1, rt - 0.6)), run_time=max(0.1, rt - 0.6), rate_func=linear)
        self.remove(band)
        unlit(cells, BLUE)
        self.finish()


# --------------------------------------------------------------------------------------------
# rasters for s09-s13
class RS:
    def __init__(self, x0, k):
        self.x0, self.k = x0, k

    def tx(self, t):
        return self.x0 + self.k * t


R4 = RS(-4.9, 2.6)     # 0 to 4 s across the frame
R12 = RS(-4.9, 0.9)    # 0 to 12 s across the frame
STRIPX = [-2.2, -1.4, -0.6, 0.2, 3.0, 3.8, 4.6, 5.4]   # cell 1 = index 1, cell 2 = index 2, cell 3 = index 5
STRIP_Y = 3.4


def make_burst(rs, t0, y, seed, color=BLUE, n=8, dur=2.0, h=0.8):
    rng = np.random.RandomState(seed)
    ts = np.sort(rng.uniform(t0 + 0.08, t0 + dur - 0.08, n))
    box = Rectangle(width=rs.k * dur, height=h + 0.2, stroke_color=color, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.08
                    ).move_to([rs.tx(t0 + dur / 2), y, 0])
    ticks = VGroup(*[Line([rs.tx(t), y - h / 2, 0], [rs.tx(t), y + h / 2, 0], color=YELLOW, stroke_width=4) for t in ts])
    return box, ticks, ts


def row_label(txt, y, color):
    return T(txt, 34, color, weight=BOLD).move_to([-5.85, y, 0])


def base_line(rs, y, tmax):
    return Line([rs.x0 - 0.15, y - 0.55, 0], [rs.tx(tmax), y - 0.55, 0], color=GREY, stroke_width=1, stroke_opacity=0.5)


def axis_t(rs, y, ticks, tmax, title, title_t):
    line = Arrow([rs.x0 - 0.2, y, 0], [rs.tx(tmax), y, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    g = VGroup(line)
    for t, l in ticks:
        g.add(Line([rs.tx(t), y - 0.08, 0], [rs.tx(t), y + 0.08, 0], color=GREY, stroke_width=3),
              T(l, 26, GREY).move_to([rs.tx(t), y - 0.4, 0]))
    g.add(T(title, 26, GREY).move_to([rs.tx(title_t), y - 0.4, 0]))
    return g


def axis12(y=-1.85):
    return axis_t(R12, y, [(t, str(t)) for t in range(0, 13, 2)], 12.6, "s", 12.3)


def top_strip(hl, label="left eye: retina"):
    outline = RoundedRectangle(corner_radius=0.4, width=12.8, height=0.8, stroke_color=GREY, stroke_width=3).move_to([0, STRIP_Y, 0])
    lab = T(label, 26, BLUE).move_to([-4.6, STRIP_Y, 0])
    cs, g = {}, VGroup()
    for k, x in enumerate(STRIPX):
        if k in hl:
            c = cell(x, STRIP_Y, BLUE, 0.27, 0.55, 4)
        else:
            c = cell(x, STRIP_Y, BLUE, 0.27, 0.1, 2).set_stroke(BLUE, opacity=0.4)
        cs[k] = c
        g.add(c)
    nums = VGroup(*[T(lbl, 26, TEXT, weight=BOLD).move_to(cs[k].get_center()) for k, lbl in hl.items()])
    bx = 1.6
    brk = VGroup(Rectangle(width=0.5, height=0.7, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([bx, STRIP_Y, 0]),
                 Line([bx - 0.18, STRIP_Y - 0.3, 0], [bx - 0.02, STRIP_Y + 0.3, 0], color=GREY, stroke_width=4),
                 Line([bx + 0.05, STRIP_Y - 0.3, 0], [bx + 0.21, STRIP_Y + 0.3, 0], color=GREY, stroke_width=4))
    return outline, g, cs, nums, lab, brk


def lit_when(cell_m, tr, t0, t1, base=BLUE, op=0.55):
    def upd(m):
        on = t0 <= tr.get_value() <= t1
        m.set_fill(YELLOW if on else base, opacity=1.0 if on else op)
        m.set_stroke(YELLOW if on else base)
    cell_m.add_updater(upd)


def reveal_at(mob, tr, t):
    fo = float(mob.get_fill_opacity())
    mob.set_stroke(opacity=0.0)
    mob.set_fill(opacity=0.0)

    def upd(m):
        on = tr.get_value() >= t
        m.set_stroke(opacity=1.0 if on else 0.0)
        m.set_fill(opacity=fo if on else 0.0)
    mob.add_updater(upd)


def bracket_h(x0, x1, y, color=TEXT, tick=0.12, sw=3):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=sw),
                  Line([x0, y - tick, 0], [x0, y + tick, 0], color=color, stroke_width=sw),
                  Line([x1, y - tick, 0], [x1, y + tick, 0], color=color, stroke_width=sw))


Y9 = {"1": 1.5, "2": -0.2}


def raster9_static(scene):
    """the finished s09 picture, 0 to 4 s axis"""
    rs = R4
    outline, strip, cs, nums, lab, brk = top_strip({1: "1", 2: "2"})
    r1, r2 = row_label("1", Y9["1"], BLUE), row_label("2", Y9["2"], BLUE)
    bl = VGroup(base_line(rs, Y9["1"], 4.2), base_line(rs, Y9["2"], 4.2))
    ax = axis_t(rs, -1.5, [(t, str(t)) for t in range(5)], 4.3, "s", 4.1)
    b1, k1, t1 = make_burst(rs, 0.0, Y9["1"], 1)
    b2, k2, t2 = make_burst(rs, 0.2, Y9["2"], 2)
    return dict(outline=outline, strip=strip, cs=cs, nums=nums, lab=lab, brk=brk, r1=r1, r2=r2, bl=bl, ax=ax,
                b1=b1, k1=k1, b2=b2, k2=k2, t1=t1, t2=t2)


class S09Near(SpokenScene):
    def construct(self):
        rs = R4
        d = raster9_static(self)
        cs = d["cs"]
        br = DoubleArrow([cs[1].get_x(), 2.5, 0], [cs[2].get_x(), 2.5, 0], buff=0, color=TEXT, stroke_width=3, tip_length=0.1)
        brl = T("20 µm apart", 26, TEXT).move_to([0.9, 2.5, 0])
        info = VGroup(T("bursts start 0.2 s apart", 30, TEXT), T("each burst lasts 2 s", 30, TEXT)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.9, 0.65, 0])
        self.add(d["outline"], d["strip"], d["nums"], d["lab"], d["brk"])
        self.at("Two cells")
        self.play(GrowFromCenter(br), FadeIn(brl), FadeIn(d["r1"]), FadeIn(d["r2"]), FadeIn(d["bl"]), FadeIn(d["ax"]), run_time=0.9)
        self.at("fire almost")
        tr = ValueTracker(-0.3)
        for m, t in list(zip(d["k1"], d["t1"])) + list(zip(d["k2"], d["t2"])):
            reveal_at(m, tr, t)
        reveal_at(d["b1"], tr, 0.0)
        reveal_at(d["b2"], tr, 0.2)
        lit_when(cs[1], tr, 0.0, 2.0)
        lit_when(cs[2], tr, 0.2, 2.2)
        self.add(d["b1"], d["b2"], d["k1"], d["k2"])
        self.play(tr.animate.set_value(2.5), run_time=1.5, rate_func=linear)
        for m in list(d["k1"]) + list(d["k2"]) + [d["b1"], d["b2"], cs[1], cs[2]]:
            m.clear_updaters()
        cs[1].set_fill(BLUE, 0.55).set_stroke(BLUE)
        cs[2].set_fill(BLUE, 0.55).set_stroke(BLUE)
        self.at("overlap almost")
        ov = Rectangle(width=rs.k * 1.8, height=2.9, stroke_width=0, fill_color=TEXT, fill_opacity=0.16).move_to([rs.tx(1.1), 0.65, 0])
        brk2 = bracket_h(rs.tx(0.2), rs.tx(2.0), -2.45)
        bl2 = T("1.8 s of 2 s overlap", 30, TEXT, weight=BOLD).move_to([rs.tx(1.1), -2.9, 0])
        self.add(ov, brk2, bl2, info)
        eq = M("overlap: (2 − 0.2) ÷ 2 = 90 percent", 32, TEXT).move_to([0, -3.5, 0])
        self.at("completely")
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.6)
        self.finish()


Y10 = {"1": 1.2, "2": 0.05, "3": -1.1}


def build_s10_base(scene, crossfade_from_s09=True):
    rs = R12
    outline, strip, cs, nums, lab, brk = top_strip({1: "1", 2: "2"})
    r1, r2 = row_label("1", Y10["1"], BLUE), row_label("2", Y10["2"], BLUE)
    bl = VGroup(*[base_line(rs, Y10[k], 12.4) for k in "123"])
    ax = axis12()
    b1, k1, t1 = make_burst(rs, 0.0, Y10["1"], 1, h=0.6)
    b2, k2, t2 = make_burst(rs, 0.2, Y10["2"], 2, h=0.6)
    ov = Rectangle(width=rs.k * 1.8, height=1.9, stroke_width=0, fill_color=TEXT, fill_opacity=0.16).move_to([rs.tx(1.1), 0.625, 0])
    new = Group(r1, r2, bl, ax, b1, b2, k1, k2, ov)
    if crossfade_from_s09:
        d = raster9_static(scene)
        cs9 = d["cs"]
        for k in (1, 2):
            cs9[k].set_fill(BLUE, 0.55).set_stroke(BLUE)
        old = Group(d["r1"], d["r2"], d["bl"], d["ax"], d["b1"], d["b2"], d["k1"], d["k2"])
        scene.add(outline, strip, nums, lab, brk, old)
        scene.play(FadeOut(old), FadeIn(new), run_time=0.3)
    else:
        scene.add(outline, strip, nums, lab, brk, new)
    return outline, strip, cs, nums, ov, brk


class S10Far(SpokenScene):
    def construct(self):
        rs = R12
        outline, strip, cs, nums, ov, brk = build_s10_base(self)
        xa, xc = cs[1].get_x(), cs[5].get_x()
        arrow = Arrow([xa, 2.3, 0], [xc + 0.5, 2.3, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.22)
        wl = T("wave direction", 28, YELLOW).move_to([-3.6, 2.62, 0])
        dist = M("1,000 µm", 28, TEXT).move_to([4.2, 2.68, 0])
        ns = T("not to scale", 26, CAP).move_to([1.6, 2.68, 0])
        r3 = row_label("3", Y10["3"], BLUE)
        b3, k3, t3 = make_burst(rs, 10.0, Y10["3"], 3, h=0.6)
        eq = M("1,000 µm ÷ 100 µm/s = 10 s", 32, TEXT).move_to([0, -2.9, 0])
        self.at("A cell a")
        self.play(GrowArrow(arrow), FadeIn(wl), FadeIn(ns), run_time=0.4)
        self.at("millimeter farther")
        n3 = T("3", 26, TEXT, weight=BOLD).move_to(cs[5].get_center())
        self.play(cs[5].animate.set_fill(BLUE, 0.55).set_stroke(BLUE, width=4), FadeIn(dist), FadeIn(r3), FadeIn(n3), run_time=0.6)
        self.at("fires ten seconds")
        tr = ValueTracker(2.4)
        for m, t in zip(k3, t3):
            reveal_at(m, tr, t)
        reveal_at(b3, tr, 10.0)
        lit_when(cs[5], tr, 10.0, 12.0)
        cur = Line([0, 1.8, 0], [0, -1.55, 0], color=TEXT, stroke_width=2, stroke_opacity=0.6)
        cur.add_updater(lambda m: m.move_to([rs.tx(tr.get_value()), 0.1, 0]))
        self.add(b3, k3, cur)
        self.play(tr.animate.set_value(12.4), run_time=1.1, rate_func=linear)
        for m in list(k3) + [b3, cs[5], cur]:
            m.clear_updaters()
        cs[5].set_fill(BLUE, 0.55).set_stroke(BLUE)
        self.remove(cur)
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.4)
        # the key caveat from the lesson, big and held
        brk200 = bracket_h(rs.tx(0), rs.tx(2.0), 1.88, color=YELLOW)
        note = T("200 µm = 2 s lag: along this path, overlap ends", 30, TEXT, weight=BOLD).move_to([0, -3.45, 0])
        lagl = T("2 s lag", 26, YELLOW).next_to(brk200, RIGHT, buff=0.2)
        self.play(FadeIn(note, shift=UP * 0.1), Create(brk200), FadeIn(lagl), run_time=0.6)
        self.at("do not overlap")
        nov = T("no overlap", 40, TEXT, weight=BOLD).move_to([rs.tx(6.1), 0.05, 0])
        self.play(FadeOut(ov), FadeIn(nov), run_time=0.7)
        self.finish()


# --------------------------------------------------------------------------------------------
def two_strips():
    g = {}
    for side, cx, col, name in (("L", -3.3, BLUE, "left eye: retina"), ("R", 3.3, ORANGE, "right eye: retina")):
        out = RoundedRectangle(corner_radius=0.4, width=6.2, height=0.8, stroke_color=GREY, stroke_width=3).move_to([cx, STRIP_Y, 0])
        cs = []
        for k in range(7):
            x = cx + (k - 3) * 0.8
            hot = (side == "L" and k in (2, 3)) or (side == "R" and k == 2)
            cs.append(cell(x, STRIP_Y, col, 0.27, 0.55 if hot else 0.1, 4 if hot else 2).set_stroke(col, opacity=1 if hot else 0.4))
        lab = T(name, 26, col).move_to([cx, 2.58, 0])
        g[side] = (out, VGroup(*cs), cs, lab)
    return g


def pq1_frame(scene):
    rs = R12
    g = two_strips()
    nums = VGroup(T("1", 26, TEXT, weight=BOLD).move_to(g["L"][2][2].get_center()),
                  T("2", 26, TEXT, weight=BOLD).move_to(g["L"][2][3].get_center()),
                  T("R", 26, TEXT, weight=BOLD).move_to(g["R"][2][2].get_center()))
    r1, r2 = row_label("1", Y10["1"], BLUE), row_label("2", Y10["2"], BLUE)
    bl = VGroup(*[base_line(rs, Y10[k], 12.4) for k in "123"])
    ax = axis12(-1.85)
    b1, k1, t1 = make_burst(rs, 0.0, Y10["1"], 1, h=0.6)
    b2, k2, t2 = make_burst(rs, 0.2, Y10["2"], 2, h=0.6)
    scene.add(g["L"][0], g["L"][1], g["L"][3], r1, r2, bl, ax, b1, b2, k1, k2, nums[0], nums[1])
    return g, nums, bl, ax, (b1, k1, b2, k2, r1, r2)


def pq1_extra(g, nums):
    rR = row_label("R", Y10["3"], ORANGE)
    qm = T("?", 100, TEXT, weight=BOLD).move_to([R12.tx(6.0), Y10["3"], 0])
    qt = T("same point, other eye: does it overlap?", 34, TEXT).move_to([0, -3.3, 0])
    return rR, qm, qt


class S11Pq1(SpokenScene):
    def construct(self):
        g, nums, bl, ax, rest = pq1_frame(self)
        rR, qm, qt = pq1_extra(g, nums)
        self.add(g["R"][0], g["R"][1], g["R"][3], qt)
        self.at("Now predict")
        self.at("What about a cell")
        self.play(Indicate(g["R"][2][2], color=YELLOW, scale_factor=1.35), FadeIn(nums[2]), FadeIn(rR), run_time=0.9)
        self.at("other eye")
        self.play(Write(qm), run_time=0.6)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        g, nums, bl, ax, rest = pq1_frame(self)
        rR, qm, qt = pq1_extra(g, nums)
        self.add(g["R"][0], g["R"][1], g["R"][3], nums[2], rR, qm, qt)
        self.finish()


def chance_times():
    """32 bursts per row over 50 minutes (a burst every minute or two); the other eye's bursts are unrelated,
    and exactly one lands within 2 s of the first eye's."""
    tA = np.linspace(60, 2910, 32)
    tD = tA + 35.0
    tD[16] = tA[16] + 0.6
    return tA, tD



class S13Rev1(SpokenScene):
    def construct(self):
        rs = R12
        g, nums, bl, ax, rest = pq1_frame(self)
        b1, k1, b2, k2, r1, r2 = rest
        rR, qm, qt = pq1_extra(g, nums)
        self.add(g["R"][0], g["R"][1], g["R"][3], nums[2], rR, qm, qt)
        self.at("Its waves are")
        bR, kR, tR = make_burst(rs, 6.5, Y10["3"], 7, color=ORANGE, h=0.6)
        self.play(FadeOut(qm), FadeOut(qt), FadeIn(bR), FadeIn(kR), run_time=0.8)
        self.at("so it matches")
        LS = 10.8 / 3000.0
        xm = lambda s: R12.x0 + LS * s
        line = Arrow([R12.x0 - 0.2, -1.85, 0], [xm(3000) + 0.4, -1.85, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        axl = VGroup(line)
        for m in range(0, 51, 10):
            axl.add(Line([xm(60 * m), -1.93, 0], [xm(60 * m), -1.77, 0], color=GREY, stroke_width=3),
                    T(str(m) if m < 50 else "50 min", 26, GREY).move_to([xm(60 * m) + (0.0 if m < 50 else 0.25), -2.25, 0]))
        tA, tD = chance_times()

        def bars(times, y):
            return VGroup(*[Line([xm(t), y - 0.4, 0], [xm(t), y + 0.4, 0], color=YELLOW, stroke_width=4) for t in times])
        long1, long2, longR = bars(tA, Y10["1"]), bars(tA + 0.2, Y10["2"]), bars(tD, Y10["3"])
        zl = T("zoom out: 50 minutes", 34, TEXT, weight=BOLD).move_to([0, 2.1, 0])
        old = Group(b1, k1, b2, k2, bR, kR, ax)
        self.play(FadeOut(old), FadeIn(axl), FadeIn(long1), FadeIn(long2), FadeIn(longR), FadeIn(zl), run_time=1.3)
        mk = T("each bar is one 2 s burst, drawn wider than scale", 26, CAP).move_to([0, -2.8, 0])
        self.play(FadeIn(mk), run_time=0.4)
        self.at("a few percent")
        xo = [xm(a) for a in tA for b in tD if abs(a - b) < 2.0][0]
        circ = RoundedRectangle(corner_radius=0.07, width=0.18, height=1.95, stroke_color=TEXT, stroke_width=5).move_to([xo, -0.525, 0])
        lab = T("overlap only by chance: 1 burst in 32, a few percent", 30, TEXT, weight=BOLD).move_to([0, -3.4, 0])
        self.play(FadeIn(circ), FadeIn(lab), run_time=0.25)
        self.finish()


# --------------------------------------------------------------------------------------------
def wave_light(cells, o, a, tr, base=BLUE):
    for c in cells:
        def upd(m, c=c):
            d = m.get_center()[:2] - o[:2]
            r = float(np.hypot(*d))
            ang = float(np.arctan2(d[1], d[0]))
            dang = abs((ang - a + np.pi) % (2 * np.pi) - np.pi)
            on = dang < 0.65 and abs(r - tr.get_value()) < 0.6
            m.set_fill(YELLOW if on else base, opacity=1.0 if on else 0.15)
            m.set_stroke(YELLOW if on else base)
        c.add_updater(upd)


class S14Caution(SpokenScene):
    def construct(self):
        cx, cy = -1.7, 0.0
        outline = RoundedRectangle(corner_radius=0.6, width=9.6, height=6.6, stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])
        cells = VGroup(*[cell(cx + (i - 5.5) * 0.8, cy + (j - 3) * 0.8 - 0.1, BLUE, 0.22, 0.15, 2) for j in range(7) for i in range(12)])
        lab = T("left eye: retina", 28, BLUE).move_to([cx - 3.3, 3.0, 0])
        waves = [((-5.6, -1.9), 25, 2.8), ((-0.6, 2.4), -100, 2.5), ((2.2, -1.2), 170, 2.6)]
        self.play(FadeIn(outline), FadeIn(cells), FadeIn(lab), run_time=0.3)
        keep = []
        cues = ["But waves start", "many places", "varying directions"]
        for (org, ang, rmax), cue in zip(waves, cues):
            self.at(cue)
            o = np.array([org[0], org[1], 0.0])
            a = np.radians(ang)
            tr = ValueTracker(0.1)

            def fronts(o=o, a=a, tr=tr):
                g = VGroup()
                for off, op in ((0.0, 1.0), (0.75, 0.65), (1.5, 0.35)):
                    r = tr.get_value() - off
                    if r > 0.08:
                        g.add(Arc(radius=r, start_angle=a - 0.62, angle=1.24, arc_center=o, color=YELLOW, stroke_width=7, stroke_opacity=op))
                return g
            arcs = always_redraw(fronts)
            dot = Dot(o, radius=0.2, color=YELLOW)
            wave_light(cells, o, a, tr)
            self.add(dot, arcs)
            self.play(tr.animate.set_value(rmax), run_time=0.65, rate_func=linear)
            arcs.clear_updaters()
            unlit(cells, BLUE, 0.15)
            keep += [dot, arcs]
        ang8 = np.radians(np.arange(0, 360, 45))
        val = np.array([1.0, 1.0, 0.15, 0.15, 0.15, 0.15, 0.15, 1.0])
        rc = np.array([5.0, 0.9, 0])
        spokes = VGroup(*[Arrow(rc, rc + np.array([np.cos(a), np.sin(a), 0]) * 1.45, buff=0, color=TEXT,
                                stroke_width=2 if v < 0.5 else 10, tip_length=0.2) for a, v in zip(ang8, val)])
        rl = VGroup(T("wave directions", 26, CAP), T("bold = more frequent", 24, CAP)).arrange(DOWN, buff=0.22).move_to([5.0, -1.3, 0])
        self.play(FadeIn(spokes, lag_ratio=0.1), FadeIn(rl), run_time=1.0)
        self.finish()


# --------------------------------------------------------------------------------------------
def match_curve(d):
    """mean overlap of two 1-3 s bursts (2 s on average) for a pair d apart, wave speed 100 um/s, wave direction uniform"""
    th = np.linspace(0, np.pi / 2, 361)[None, :]
    Ls = np.linspace(100.0, 300.0, 41)[:, None]      # burst length (s) x 100 um/s
    return float(np.mean(np.maximum(0.0, 1.0 - d * np.cos(th) / Ls)))


class S15Match(SpokenScene):
    def construct(self):
        rng = np.random.RandomState(12)
        y = -0.9
        g = VGroup()
        for t0 in np.sort(rng.uniform(-5.2, 4.4, 9)):
            for t in t0 + np.sort(rng.uniform(0, 0.7, 4)):
                g.add(Line([t, y - 0.5, 0], [t, y + 0.5, 0], color=YELLOW, stroke_width=5))
        base = Line([-5.8, y - 0.65, 0], [5.8, y - 0.65, 0], color=GREY, stroke_width=1.5)
        one = T("one cell's firing times", 32, TEXT).move_to([0, y - 1.3, 0])
        chip_p = chip("position", TEAL, 50, 0.3).move_to([0, 2.9, 0])
        arr = DashedLine([0, y + 0.8, 0], [0, 2.1, 0], color=GREY, stroke_width=5)
        cross = VGroup(Line([-0.7, 0.3, 0], [0.7, 1.5, 0], color=RED, stroke_width=12), Line([-0.7, 1.5, 0], [0.7, 0.3, 0], color=RED, stroke_width=12))
        self.play(FadeIn(g, lag_ratio=0.02), Create(base), run_time=0.7)
        self.at("position is carried")
        self.play(FadeIn(chip_p), Create(arr), run_time=0.8)
        self.at("one cell's timing")
        self.play(FadeIn(one), Create(cross), run_time=0.7)
        self.at("but by how")
        ax = Axes(x_range=[0, 800, 200], y_range=[0, 1, 0.5], x_length=9.2, y_length=4.7, tips=False,
                  axis_config={"include_numbers": False, "include_ticks": True, "color": GREY, "stroke_width": 3}
                  ).move_to([1.0, 0.0, 0])
        xl = VGroup(*[T(str(v), 26, GREY).move_to(ax.c2p(v, 0) + DOWN * 0.4) for v in (0, 200, 400, 600, 800)])
        yl = VGroup(*[T(s_, 26, GREY).move_to(ax.c2p(0, v) + LEFT * 0.4) for s_, v in (("0", 0), ("0.5", 0.5), ("1", 1))])
        xt = T("distance apart (µm)", 28, TEXT).move_to(ax.c2p(400, 0) + DOWN * 0.95)
        yt = T("match of firing, 0 to 1", 28, TEXT).rotate(PI / 2).move_to([ax.c2p(0, 0.5)[0] - 1.35, ax.c2p(0, 0.5)[1], 0])
        self.play(FadeOut(VGroup(g, base, one, chip_p, arr, cross)), run_time=0.4)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt), run_time=0.8)
        self.at("firing matches")
        curve = ax.plot(lambda d: match_curve(d), x_range=[0, 800, 8], color=GREEN, stroke_width=7)
        area = ax.get_area(curve, x_range=[0, 800], color=GREEN, opacity=0.2)
        self.play(Create(curve), FadeIn(area), run_time=1.0)
        self.at("over many waves")
        note = VGroup(T("schematic, not data", 30, TEXT, weight=BOLD),
                      T("averaged over many waves:", 28, TEXT),
                      T("fades smoothly, no sharp edge", 28, TEXT),
                      T("waves start anywhere,", 26, CAP),
                      T("so the cutoff blurs", 26, CAP)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(ax.c2p(590, 0.66))
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)
        self.finish()


# --------------------------------------------------------------------------------------------
HA, HB = np.array([-3.5, -0.5, 0]), np.array([3.5, -0.5, 0])
HR = 1.6


def hebb_cells():
    A = Circle(radius=HR, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.25).move_to(HA)
    B = Circle(radius=HR, stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.25).move_to(HB)
    la = T("A", 64, BLUE, weight=BOLD).move_to(HA)
    lb = T("B", 64, PURPLE, weight=BOLD).move_to(HB)
    ax = Line(HA + RIGHT * HR, HB + LEFT * (HR + 0.0), color=GREY, stroke_width=6)
    bout = Circle(radius=0.28, stroke_color=GREY, fill_color=GREY, fill_opacity=0.5, stroke_width=2).move_to(HB + LEFT * (HR + 0.28))
    return A, B, la, lb, ax, bout


class S16Hebb(SpokenScene):
    def construct(self):
        A, B, la, lb, ax, bout = hebb_cells()
        tl = T("target cell", 30, PURPLE).move_to(HB + DOWN * 2.2)
        al = T("one of its inputs", 30, BLUE).move_to(HA + DOWN * 2.2)
        self.at("How could")
        self.play(FadeIn(B), FadeIn(lb), FadeIn(tl), run_time=0.6)
        self.play(FadeIn(A), FadeIn(la), Create(ax), FadeIn(bout), FadeIn(al), run_time=0.7)
        self.at("that match")
        self.play(Indicate(ax, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("In 1949")
        yr = T("1949", 44, GOLD, font=TITLE_FONT).move_to([0, 3.35, 0])
        self.play(FadeIn(yr, shift=DOWN * 0.1), run_time=0.7)
        self.at("Donald Hebb")
        nm = T("Donald Hebb", 54, TEXT, font=TITLE_FONT).move_to([0, 2.55, 0])
        sub = T("psychologist", 30, CAP).move_to([0, 1.8, 0])
        self.play(FadeIn(nm, shift=DOWN * 0.1), FadeIn(sub), run_time=0.8)
        self.finish()


def phrase(words, size, y, colors=None):
    ws = VGroup(*[T(w, size, (colors or {}).get(w.strip(",."), TEXT)) for w in words]).arrange(RIGHT, buff=0.2)
    return ws


class S17Rule(SpokenScene):
    def construct(self):
        A, B, la, lb, ax, bout = hebb_cells()
        self.add(A, B, la, lb, ax, bout)
        cols = {"A": BLUE, "B": PURPLE}
        lab = T("Hebb's rule, in paraphrase", 30, GREY, font=TITLE_FONT).move_to([0, 3.55, 0])
        l1 = phrase("When A repeatedly takes part in firing B,".split(), 38, 0, cols)
        l1.move_to([0, 2.8, 0])
        l2 = phrase("A becomes more effective at firing B.".split(), 38, 0, cols)
        l2.move_to([0, 2.05, 0])
        # word groups: l1 = When A | repeatedly takes part | in firing B,
        g1, g2, g3 = VGroup(*l1[0:2]), VGroup(*l1[2:5]), VGroup(*l1[5:])
        self.play(FadeIn(lab), run_time=0.6)

        def repeat(k):
            dot = Dot(HA + RIGHT * HR, radius=0.2, color=YELLOW)
            n = T(str(k), 34, YELLOW, weight=BOLD).move_to([0, 0.5, 0])
            self.add(dot)
            self.play(A.animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW), FadeIn(n), run_time=0.1)
            self.play(dot.animate.move_to(HB + LEFT * HR), A.animate.set_fill(BLUE, 0.25).set_stroke(BLUE), run_time=0.25, rate_func=linear)
            self.remove(dot)
            self.play(B.animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW), run_time=0.08)
            self.play(B.animate.set_fill(PURPLE, 0.25).set_stroke(PURPLE), FadeOut(n), run_time=0.15)
        self.at("when cell A")
        self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.4)
        self.at("repeatedly takes part")
        self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.3)
        repeat(1)
        self.at("firing cell B")
        self.play(FadeIn(g3, shift=UP * 0.1), run_time=0.2)
        repeat(2)
        repeat(3)
        self.at("becomes more effective")
        self.play(FadeIn(l2, shift=UP * 0.1), ax.animate.set_stroke(GREEN, width=20), bout.animate.scale(2.0).set_fill(GREEN, 0.9).set_stroke(GREEN), run_time=0.7)
        self.at("effective at firing")
        self.play(A.animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW), run_time=0.2)
        self.play(B.animate.set_fill(YELLOW, 1.0).set_stroke(YELLOW).scale(1.08), A.animate.set_fill(BLUE, 0.25).set_stroke(BLUE), run_time=0.4)
        self.play(B.animate.scale(1 / 1.08).set_fill(PURPLE, 0.25).set_stroke(PURPLE), run_time=0.4)
        self.finish()


# --------------------------------------------------------------------------------------------
class Geo:
    def __init__(self, cc, cr, src, bp, k, lab_x):
        self.cc, self.cr, self.src, self.bp, self.k, self.lab_x = np.array(cc), cr, src, bp, k, lab_x


BIG = Geo([1.4, 0.2, 0], 2.0, {"L": np.array([-5.8, 2.4, 0.0]), "R": np.array([-5.8, -2.0, 0.0])},
          {"L": np.array([-1.2, 2.1, 0.0]), "R": np.array([-1.2, -1.7, 0.0])}, 1.25, 4.85)
SMALL = Geo([2.9, 1.7, 0], 1.25, {"L": np.array([-5.8, 2.9, 0.0]), "R": np.array([-5.8, 0.6, 0.0])},
            {"L": np.array([-0.4, 2.75, 0.0]), "R": np.array([-0.4, 0.65, 0.0])}, 0.75, 5.7)
ANG = {"L": [100, 125, 150], "R": [210, 235, 260]}
ECOL = {"L": BLUE, "R": ORANGE}


def bdir(a):
    r = np.radians(a)
    return np.array([np.cos(r), np.sin(r), 0.0])


def eye_syn(eye, s, geo=BIG, rings=False):
    """branches + boutons of one eye's inputs. s = strength: 1.0 baseline, 1.5 strengthened, 0 gone"""
    g = VGroup()
    if s < 0.08:
        return g
    s = min(s, 1.8)
    col = ECOL[eye]
    r = float(np.clip((0.24 + 0.2 * (s - 1.0)) * geo.k, 0.04, 0.5))
    w = float(np.clip(4 + 7 * (s - 1.0), 0.8, 16)) * (0.6 + 0.4 * geo.k)
    lowc = col
    if s < 1.0:
        lowc = interpolate_color(ManimColor(RED), ManimColor(col), float(np.clip((s - 0.2) / 0.8, 0, 1)))
    for a in ANG[eye]:
        P = geo.cc + (geo.cr + r) * bdir(a)
        g.add(Line(geo.bp[eye], geo.cc + geo.cr * bdir(a), color=lowc, stroke_width=w))
        g.add(Circle(radius=r, stroke_color=lowc, stroke_width=3, fill_color=lowc, fill_opacity=0.9).move_to(P))
        if rings and s > 1.04:
            g.add(Circle(radius=(r + 0.1) * 0.85, stroke_color=GREEN, stroke_width=4, stroke_opacity=float(min(1, (s - 1.0) * 4))).move_to(P))
    return g


def cell_lab(lines, color, geo=BIG, size=26):
    return VGroup(*[T(t, size, color) for t in lines]).arrange(DOWN, buff=0.08).move_to([geo.lab_x, geo.cc[1], 0])


def stage_static(geo=BIG):
    cellm = Circle(radius=geo.cr, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.28).move_to(geo.cc)
    cl = cell_lab(["thalamic", "cell"], PURPLE, geo)
    trunks = VGroup(*[Line(geo.src[e], geo.bp[e], color=ECOL[e], stroke_width=4) for e in "LR"],
                    *[Circle(radius=0.3, stroke_color=ECOL[e], stroke_width=3, fill_color=ECOL[e], fill_opacity=0.35).move_to(geo.src[e]) for e in "LR"])
    ll = T("left eye", 28, BLUE).move_to(geo.src["L"] + UP * 0.65)
    lr = T("right eye", 28, ORANGE).move_to(geo.src["R"] + DOWN * 0.65)
    return cellm, cl, trunks, ll, lr


def fire_eye(scene, eye, geo=BIG, rt=0.8, drive=None, syn=None):
    dots, anims = [], []
    for a in ANG[eye]:
        P = geo.cc + geo.cr * bdir(a)
        path = VMobject().set_points_as_corners([geo.src[eye], geo.bp[eye], P])
        d = Dot(geo.src[eye], radius=0.14, color=YELLOW)
        dots.append(d)
        anims.append(MoveAlongPath(d, path, rate_func=linear))
    scene.add(*dots)
    scene.play(*anims, run_time=rt)
    scene.remove(*dots)
    boutons = [m for m in (syn or []) if isinstance(m, Circle) and m.get_fill_opacity() > 0.5]
    col = ECOL[eye]
    anims2 = [b.animate.set_fill(YELLOW, 1.0).set_stroke(YELLOW) for b in boutons]
    if drive is not None:
        anims2.append(drive.animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW))
    if anims2:
        scene.play(*anims2, run_time=0.15)
        back = [b.animate.set_fill(col, 0.9).set_stroke(col) for b in boutons]
        if drive is not None:
            back.append(drive.animate.set_fill(PURPLE, 0.28).set_stroke(PURPLE))
        scene.play(*back, run_time=0.3)


QT = "what happens to the right eye's inputs?"


def prediction_loop(scene, sl, sr, cellm):
    clock = ValueTracker(0)
    clock.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(clock)
    for idx, eye in enumerate("LR"):
        for angle in ANG[eye]:
            path = VMobject().set_points_as_corners([BIG.src[eye], BIG.bp[eye], BIG.cc + BIG.cr * bdir(angle)])
            dot = Dot(radius=0.14, color=YELLOW)
            def upd(m, path=path, idx=idx):
                phase = (clock.get_value() % 4.8) - idx * 2.4
                m.set_opacity(1 if 0 <= phase < 2.2 else 0)
                m.move_to(path.point_from_proportion(float(np.clip(phase / 2.2, 0, 1))))
            dot.add_updater(upd)
            scene.add(dot)


class S18Pq2(SpokenScene):
    def construct(self):
        cellm, cl, trunks, ll, lr = stage_static()
        sl, sr = eye_syn("L", 1.0), eye_syn("R", 1.0)
        qt = T(QT, 34, TEXT).move_to([0, -3.0, 0])
        self.add(cellm, cl, trunks, ll, lr, sl, sr)
        prediction_loop(self, sl, sr, cellm)
        self.at("Predict")
        self.play(FadeIn(qt), run_time=0.25)
        self.finish()


class S19Pause(NarratedScene):
    def construct(self):
        cellm, cl, trunks, ll, lr = stage_static()
        qt = T(QT, 34, TEXT).move_to([0, -3.0, 0])
        sl, sr = eye_syn("L", 1.0), eye_syn("R", 1.0)
        self.add(cellm, cl, trunks, ll, lr, sl, sr, qt)
        prediction_loop(self, sl, sr, cellm)
        self.finish()


class S20Rev2(SpokenScene):
    def construct(self):
        cellm, cl, trunks, ll, lr = stage_static()
        sL, sR = ValueTracker(1.0), ValueTracker(1.0)
        synL = always_redraw(lambda: eye_syn("L", sL.get_value(), BIG, True))
        synR = always_redraw(lambda: eye_syn("R", sR.get_value(), BIG, True))
        qt = T(QT, 34, TEXT).move_to([0, -3.4, 0])
        self.add(cellm, cl, trunks, ll, lr, synL, synR, qt)
        self.at("If they are")
        self.play(FadeOut(qt), run_time=0.4)
        self.at("fire the cell")
        fire_eye(self, "L", BIG, 0.55, drive=cellm)
        fire_eye(self, "R", BIG, 0.55, drive=cellm)
        self.at("strengthen too")
        self.play(sL.animate.set_value(1.5), sR.animate.set_value(1.5), run_time=1.2)
        self.at("Hebb's rule only")
        lab = T("Hebb alone: everything strengthens", 36, GREEN).move_to([0, 3.5, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.7)
        self.at("stays binocular")
        bino = cell_lab(["binocular:", "driven by", "both eyes"], PURPLE)
        self.play(FadeOut(cl), FadeIn(bino), run_time=0.8)
        self.finish()


class S21Second(SpokenScene):
    def construct(self):
        cellm, cl, trunks, ll, lr = stage_static()
        self.add(cellm, trunks, ll, lr, eye_syn("L", 1.5, BIG, True), eye_syn("R", 1.5, BIG, True))
        bino = cell_lab(["binocular:", "driven by", "both eyes"], PURPLE)
        self.add(bino)
        hebb = T("Hebb's rule: strengthening", 36, GREEN).move_to([0, 3.5, 0])
        self.add(hebb)
        part1 = T("the missing half:", 42, GOLD, weight=BOLD)
        word = T("competition", 42, GOLD, weight=BOLD)
        q = T("?", 42, GOLD, weight=BOLD)
        full = VGroup(part1.copy(), word.copy()).arrange(RIGHT, buff=0.25).move_to([0, 3.5, 0])
        part1.move_to(full[0])
        word.move_to(full[1])
        q.move_to(full[1].get_left() + RIGHT * 0.15)
        self.at("second half")
        self.play(FadeOut(hebb), run_time=0.3)
        self.play(FadeIn(part1), FadeIn(q), run_time=0.5)
        self.at("Competition")
        self.play(FadeOut(q), run_time=0.15)
        self.play(FadeIn(word), run_time=0.4)
        self.play(Indicate(word, color=GOLD, scale_factor=1.12), run_time=0.6)
        self.finish()


# --------------------------------------------------------------------------------------------
BAR_Y3 = -2.0
BSC = 0.9


def bar_group(trL, trR, y=BAR_Y3, scale=BSC, cx=0.0, h=1.0, size=30, lab=True):
    def f():
        L, R = max(trL.get_value(), 0.0), max(trR.get_value(), 0.0)
        tot = L + R
        x0 = cx - tot * scale / 2
        g = VGroup()
        if L > 0.01:
            g.add(Rectangle(width=L * scale, height=h, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.75).move_to([x0 + L * scale / 2, y, 0]))
        if R > 0.01:
            g.add(Rectangle(width=R * scale, height=h, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.75).move_to([x0 + L * scale + R * scale / 2, y, 0]))
        if lab and L * scale > 1.0:
            g.add(M(f"{L:.1f}", size, TEXT).move_to([x0 + L * scale / 2, y, 0]))
        if lab and R * scale > 1.0:
            g.add(M(f"{R:.1f}", size, TEXT).move_to([x0 + L * scale + R * scale / 2, y, 0]))
        return g
    return always_redraw(f)


def static_bar(L, R, y, cx, scale, h=0.55, size=24):
    tot = L + R
    x0 = cx - tot * scale / 2
    return VGroup(Rectangle(width=L * scale, height=h, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.75).move_to([x0 + L * scale / 2, y, 0]),
                  Rectangle(width=R * scale, height=h, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.75).move_to([x0 + L * scale + R * scale / 2, y, 0]),
                  M(f"{L:.2f}", size, TEXT).move_to([x0 + L * scale / 2, y, 0]),
                  M(f"{R:.2f}", size, TEXT).move_to([x0 + L * scale + R * scale / 2, y, 0]))


def budget_outline(y=BAR_Y3):
    return DashedVMobject(Rectangle(width=10.0 * BSC, height=1.35, stroke_color=CAP, stroke_width=3).move_to([0, y, 0]), num_dashes=60)


class S22Budget(SpokenScene):
    def construct(self):
        G = SMALL
        cellm, cl, trunks, ll, lr = stage_static(G)
        trL, trR = ValueTracker(5.5), ValueTracker(4.5)
        synL = always_redraw(lambda: eye_syn("L", 0.3 * trL.get_value(), G))
        synR = always_redraw(lambda: eye_syn("R", 0.3 * trR.get_value(), G))
        bino = cell_lab(["binocular:", "driven by", "both eyes"], PURPLE, G)
        self.add(cellm, trunks, ll, lr, synL, synR, bino)
        bar = bar_group(trL, trR, scale=1.02, h=1.3, size=36)
        outl = budget_outline().stretch_to_fit_width(10.2).stretch_to_fit_height(1.6)
        bl = T("fixed budget: 10 units", 30, TEXT, weight=BOLD).move_to([0, BAR_Y3 + 1.45, 0])
        self.at("Picture the")
        self.wait(0.2)
        self.at("fixed budget")
        self.add(bar)
        self.play(FadeIn(outl), FadeIn(bl), run_time=0.9)
        self.at("Each round")
        toy = T("toy model: equal amounts taken back each round", 28, CAP).move_to([0, -3.55, 0])
        self.play(FadeIn(toy), run_time=0.6)
        self.at("both eyes grow")
        xL = lambda L, R: (-(L + R) * BSC / 2 + L * BSC / 2)
        gl = T("+1.1", 32, GREEN, weight=BOLD).move_to([xL(6.6, 5.4), BAR_Y3 + 0.95, 0])
        gr = T("+0.9", 32, GREEN, weight=BOLD).move_to([-(12) * BSC / 2 + 6.6 * BSC + 5.4 * BSC / 2, BAR_Y3 + 0.95, 0])
        grow = T("after growth: 12 units", 32, GREEN, weight=BOLD).move_to([0, BAR_Y3 - 1.0, 0])
        self.play(trL.animate.set_value(6.6), trR.animate.set_value(5.4), FadeIn(gl), FadeIn(gr), FadeIn(grow), run_time=1.0)
        self.at("same amount")
        ml = T("-1", 32, RED, weight=BOLD).move_to([xL(6.6, 5.4), BAR_Y3 + 0.95, 0])
        mr = T("-1", 32, RED, weight=BOLD).move_to(gr.get_center())
        self.play(FadeOut(gl), FadeOut(gr), FadeIn(ml), FadeIn(mr), run_time=0.5)
        self.at("taken back")
        back = T("after take-back: 10 units", 32, TEXT, weight=BOLD).move_to([0, BAR_Y3 - 1.0, 0])
        self.play(FadeOut(grow), run_time=0.15)
        self.play(trL.animate.set_value(5.6), trR.animate.set_value(4.4), FadeIn(back), run_time=0.85)
        self.play(FadeOut(ml), FadeOut(mr), run_time=0.4)
        self.finish()


class S23Ahead(SpokenScene):
    def construct(self):
        cx, sc = 1.2, 0.8
        ys = [1.2, 0.0, -1.2]
        vals = [(5.5, 4.5)]
        for _ in range(2):
            L, R = vals[-1]
            vals.append((round(1.2 * L - 1, 3), round(1.2 * R - 1, 3)))
        rows = [static_bar(vals[i][0], vals[i][1], ys[i], cx, sc, 0.8, 28) for i in range(3)]
        labs = [T(s_, 28, CAP).move_to([-5.2, y, 0]) for s_, y in zip(("start", "round 1", "round 2"), ys)]
        toy = T("a toy model, not a measurement", 28, CAP).move_to([0, -3.0, 0])
        cl = T("left eye: +1.1 growth, -1.0 taken back = +0.1", 30, BLUE).move_to([0, 3.2, 0])
        cr = T("right eye: +0.9 growth, -1.0 taken back = -0.1", 30, ORANGE).move_to([0, 2.5, 0])
        self.at("The eye that")
        self.play(FadeIn(rows[0]), FadeIn(labs[0]), FadeIn(toy), run_time=0.8)
        self.at("gains more")
        self.play(FadeIn(cl, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(cr, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(rows[1], shift=UP * 0.1), FadeIn(labs[1]), run_time=0.7)
        self.at("so it pulls")
        self.play(FadeIn(rows[2], shift=UP * 0.1), FadeIn(labs[2]), run_time=0.8)
        self.at("further ahead")
        self.play(*[Indicate(rows[i][2], color=YELLOW, scale_factor=1.25) for i in range(3)], run_time=0.9)
        self.finish()


def rounds_seq():
    L, R = 5.5, 4.5
    out = [(L, R)]
    for _ in range(40):
        L2, R2 = 1.2 * L - 1, 1.2 * R - 1
        if R2 <= 0:
            out.append((10.0, 0.0))
            break
        L, R = L2, R2
        out.append((L, R))
    return out


class S24Out(SpokenScene):
    def construct(self):
        G = SMALL
        seq = rounds_seq()
        n_end = len(seq) - 1
        cellm, cl, trunks, ll, lr = stage_static(G)
        trL, trR = ValueTracker(seq[2][0]), ValueTracker(seq[2][1])
        k = ValueTracker(2.0)

        def interp(i, which):
            i = float(np.clip(i, 0, n_end))
            a = int(np.floor(i))
            b = min(a + 1, n_end)
            return seq[a][which] * (1 - (i - a)) + seq[b][which] * (i - a)
        trL.add_updater(lambda m: m.set_value(interp(k.get_value(), 0)))
        trR.add_updater(lambda m: m.set_value(interp(k.get_value(), 1)))
        synL = always_redraw(lambda: eye_syn("L", 0.3 * trL.get_value(), G))
        synR = always_redraw(lambda: eye_syn("R", 0.3 * trR.get_value(), G))
        bino = cell_lab(["binocular:", "driven by", "both eyes"], PURPLE, G)
        bar = bar_group(trL, trR)
        outl = budget_outline()
        bl = T("fixed budget: 10 units", 30, TEXT, weight=BOLD).move_to([0, BAR_Y3 + 1.45, 0])
        counter = always_redraw(lambda: T(f"round {int(round(k.get_value()))}", 40, YELLOW, weight=BOLD).move_to([-4.8, BAR_Y3 + 1.45, 0]))
        real = T("real ferret: graded shift, not all-or-none", 30, CAP).move_to([0, -3.55, 0])
        toy = T("toy model: each eye grows by 20 percent, then 1 unit is taken back from each", 26, CAP).move_to([0, -3.1, 0])
        self.add(cellm, trunks, ll, lr, synL, synR, bino, outl, bar, bl, counter, real, toy, trL, trR, k)
        self.at("In this toy model")
        self.play(k.animate.set_value(n_end), run_time=max(1.5, self.t_of("pushed out") + 0.4 - self.elapsed()), rate_func=linear)
        trL.clear_updaters()
        trR.clear_updaters()
        trL.set_value(10.0)
        trR.set_value(0.0)
        end = cell_lab(["driven by", "one eye", "(toy model)"], PURPLE, G)
        self.play(FadeOut(bino), FadeIn(end), run_time=0.5)
        self.finish()


class S24bRatio(SpokenScene):
    def construct(self):
        sc = 0.5
        yl = [1.9, 1.05, 0.2, -0.65]
        left, right = [], []
        L, R = 5.5, 4.5
        for i in range(4):
            left.append((L, R))
            L, R = 1.2 * L - 1, 1.2 * R - 1
        pr = []
        L, R = 5.5, 4.5
        for i in range(4):
            pr.append((L, R))
            L, R = 1.2 * L, 1.2 * R
            k = 10.0 / (L + R)
            L, R = L * k, R * k
        hL = T("equal amount taken back", 30, TEXT).move_to([-3.4, 3.05, 0])
        hR = T("rescaled in proportion", 30, TEXT).move_to([3.4, 3.05, 0])
        rl = VGroup(*[T(s_, 26, CAP).move_to([0, y, 0]) for s_, y in zip(("start", "1", "2", "3"), yl)])
        rtitle = T("round", 26, CAP).move_to([0, 2.55, 0])
        Lbars = VGroup(*[static_bar(a, b, y, -3.4, sc, 0.6, 22) for (a, b), y in zip(left, yl)])
        Rbars = VGroup(*[static_bar(a, b, y, 3.4, sc, 0.6, 22) for (a, b), y in zip(pr, yl)])
        cap_l = T("left share keeps growing", 28, BLUE).move_to([-3.4, -1.7, 0])
        cap_r = T("proportional rescaling: no winner", 28, TEXT).move_to([3.4, -1.7, 0])
        toy = T("a toy model, not a measurement", 26, CAP).move_to([0, -3.0, 0])
        self.add(hL, rtitle, rl, Lbars, cap_l, toy)
        self.at("Rescale both eyes")
        self.play(FadeIn(hR), run_time=0.6)
        self.at("instead")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in Rbars], lag_ratio=0.35), run_time=1.8)
        self.at("never changes")
        self.play(FadeIn(cap_r, shift=UP * 0.1), run_time=0.7)
        self.at("kind of sharing")
        self.play(Indicate(hL, color=TEXT, scale_factor=1.1), Indicate(hR, color=TEXT, scale_factor=1.1), run_time=0.9)
        self.finish()


# --------------------------------------------------------------------------------------------
class S25Take(SpokenScene):
    def construct(self):
        TC = np.array([3.9, -0.5, 0])
        TR_ = 1.8
        tgt = Circle(radius=TR_, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.28).move_to(TC)
        tl = T("target cell", 30, PURPLE).move_to(TC + DOWN * 2.35)
        rows = [("S", 1.0, BLUE, "strong input"), ("K", -0.4, BLUE, "in step"), ("O", -1.8, ORANGE, "out of step")]
        ins, boxes, ticks, axons, labs = {}, {}, {}, {}, {}
        for ri, (key, y, col, txt) in enumerate(rows):
            ins[key] = cell(-6.0, y, col, 0.34, 0.3, 4)
            boxes[key] = Rectangle(width=3.8, height=0.85, stroke_color=GREY, stroke_width=2).move_to([-3.6, y, 0])
            offs = 0.0 if key != "O" else 0.45
            tt = [t + offs for t in (0.3, 0.9, 1.5, 2.1, 2.7, 3.3)]
            ticks[key] = VGroup(*[Line([-5.5 + t, y - 0.27, 0], [-5.5 + t, y + 0.27, 0], color=YELLOW, stroke_width=4) for t in tt if t < 3.65])
            aa = np.radians(180 - 32 * (1 - ri))
            tp = TC + TR_ * np.array([np.cos(aa), np.sin(aa), 0])
            axons[key] = Line([-1.7, y, 0], tp, color=col, stroke_width=4)
            labs[key] = T(txt, 26, CAP).move_to([-3.6, y - 0.72, 0])
        title = T("Timing is the address", 54, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        rule = Line(LEFT * 2.2, RIGHT * 2.2, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.12)
        comp = T("inputs compete", 36, CAP, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(tgt), FadeIn(tl), *[FadeIn(ins[k]) for k in ins], *[FadeIn(axons[k]) for k in axons],
                  *[FadeIn(boxes[k]) for k in boxes], *[FadeIn(ticks[k]) for k in ticks], run_time=0.9)
        self.at("timing is the")
        self.play(FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=1.0)
        self.at("A cell keeps")
        self.play(Indicate(tgt, color=PURPLE, scale_factor=1.08), run_time=0.7)
        self.at("that fire in step")
        self.play(FadeIn(labs["K"]), FadeIn(labs["S"]), FadeIn(labs["O"]), run_time=0.8)
        self.at("with its strong")
        self.play(axons["S"].animate.set_stroke(GREEN, width=10), axons["K"].animate.set_stroke(GREEN, width=10), run_time=0.7)
        self.at("crowd out")
        self.add(comp)
        self.play(FadeOut(axons["O"]), FadeOut(ins["O"]), FadeOut(ticks["O"]),
                  FadeOut(boxes["O"]), FadeOut(labs["O"]), run_time=0.5)
        self.finish()


class S26End(EndCard):
    LINE = "Timing is the address: a cell keeps the inputs that fire in step with its other strong inputs, and they crowd out the rest."

    def construct(self):
        a = T("Timing is the address: a cell keeps the inputs that", 38, TEXT, font=TITLE_FONT)
        b = T("fire in step with its other strong inputs,", 38, TEXT, font=TITLE_FONT)
        c = T("and they crowd out the rest.", 38, TEXT, font=TITLE_FONT)
        sub = T("biochemistrypedia.com", size=24, color=TEAL)
        g = VGroup(a, b, c).arrange(DOWN, buff=0.28)
        fit(g, max_w=12.2)
        VGroup(g, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(g, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
