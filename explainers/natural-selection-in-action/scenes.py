"""Natural selection in action  (Biochemistrypedia explainer, grade 7 Life Science)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
All moth counts and shares are an invented SKETCH (the film says "in this sketch"); no real data is drawn.

COLOR MAP (one color per concept, whole film)
  CREAM  = a pale moth
  DUSK   = a dark moth (purple-grey fill so it can be seen on the dark frame)
  SOOT   = sooty (dark) bark;  LICHEN = clean, pale bark
  BLUE   = the bird, and the ring that means "the bird spots this moth"
  RED    = eaten (cross)
  GREEN  = survivors, young, "more common"
  TEAL   = a science word being defined (label)
  GREY   = outlines, plain labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

CREAM = "#E8DDB5"
DUSK = "#4A3F5C"
DUSK_LINE = "#9B8DB5"
SOOT = "#2A2524"
LICHEN = "#B4AE98"
PX, PY = 0.0, -0.45          # wide panel centre


def moth(kind, scale=1.0):
    """A moth as a labelled-schematic shape: two wings and a body. No texture, no anatomy."""
    fill, line = (CREAM, "#FFF4D0") if kind == "pale" else (DUSK, DUSK_LINE)
    wl = Ellipse(width=0.52, height=0.30, fill_color=fill, fill_opacity=1, stroke_color=line, stroke_width=2).rotate(0.5).shift(LEFT * 0.22 + UP * 0.04)
    wr = Ellipse(width=0.52, height=0.30, fill_color=fill, fill_opacity=1, stroke_color=line, stroke_width=2).rotate(-0.5).shift(RIGHT * 0.22 + UP * 0.04)
    body = Ellipse(width=0.14, height=0.44, fill_color=fill, fill_opacity=1, stroke_color=line, stroke_width=2).shift(DOWN * 0.02)
    g = VGroup(wl, wr, body).scale(scale * 1.5)
    g.kind = kind
    return g


def panel(w, h, cx=PX, cy=PY, kind="soot"):
    fill = SOOT if kind == "soot" else LICHEN
    r = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=fill, fill_opacity=1).move_to([cx, cy, 0])
    return r


def bark_to(rect, kind):
    return rect.animate.set_fill(SOOT if kind == "soot" else LICHEN, 1)


def pulse_anim(group, k=1.25):
    """scale up and back, without recolouring anything"""
    return [m.animate.scale(k) for m in group]


def ring(m, color=BLUE, r=0.7):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_opacity=0).move_to(m.get_center())


def cross(m):
    c = m.get_center()
    return VGroup(Line(c + [-0.42, -0.42, 0], c + [0.42, 0.42, 0], color=RED, stroke_width=8),
                  Line(c + [-0.42, 0.42, 0], c + [0.42, -0.42, 0], color=RED, stroke_width=8))


def bird(scale=1.0):
    body = Ellipse(width=1.1, height=0.7, fill_color=BLUE, fill_opacity=0.9, stroke_color=BLUE, stroke_width=2)
    head = Circle(radius=0.24, fill_color=BLUE, fill_opacity=0.9, stroke_color=BLUE, stroke_width=2).shift(LEFT * 0.55 + UP * 0.2)
    beak = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI / 2).shift(LEFT * 0.86 + UP * 0.2)
    tail = Triangle(fill_color=BLUE, fill_opacity=0.9, stroke_width=0).scale(0.2).rotate(-PI / 2).shift(RIGHT * 0.62 + DOWN * 0.04)
    eye = Dot(head.get_center() + [-0.05, 0.05, 0], radius=0.04, color=BG)
    return VGroup(body, head, beak, tail, eye).scale(scale)


def place(kinds, pts, scale=1.0):
    return [moth(k, scale).move_to(p) for k, p in zip(kinds, pts)]


def grid_pts(w, h, cx, cy, cols=4, rows=3, jit=None):
    jit = jit or [(0.0, 0.0)] * (cols * rows)
    pts = []
    for r in range(rows):
        for c in range(cols):
            x = cx + (c - (cols - 1) / 2) * (w - 1.8) / (cols - 1)
            y = cy + ((rows - 1) / 2 - r) * (h - 1.5) / (rows - 1)
            j = jit[r * cols + c]
            pts.append(np.array([x + j[0], y + j[1], 0]))
    return pts


JIT = [(-.1, .05), (.1, -.1), (-.05, .1), (.1, 0), (.1, -.05), (-.1, .1), (.05, .05), (-.1, -.1), (.1, .05), (-.05, -.05), (.1, -.05), (-.1, .05)]
# 12 moths: pale/dark order, same for every scene that shows the one wood
KINDS12 = ["dark", "pale", "dark", "pale", "pale", "dark", "pale", "dark", "dark", "pale", "dark", "pale"]


class S00Title(TitleCard):
    LESSON = "Natural selection in action"
    TITLE = "Why some traits become common"


# ---------------------------------------------------------------------------------------------
class S01Moths(SpokenScene):
    def construct(self):
        P = panel(11.4, 4.4, 0, -0.35, "clean")
        pts8 = grid_pts(11.4, 4.4, 0, -0.35, cols=4, rows=2, jit=[(-.1, .1), (.15, -.1), (-.15, .1), (.1, 0), (.1, -.1), (-.1, .1), (.1, .1), (-.1, -.1)])
        head = T("Peppered moths", 40, font=TITLE_FONT).move_to([0, 2.75, 0])
        self.at("Peppered moths rest")
        self.play(FadeIn(P), Write(head), run_time=1.0)
        mix = ["pale", "dark", "pale", "pale", "dark", "pale", "pale", "dark"]
        ms = place(mix, pts8)
        pale_i = [i for i, k in enumerate(mix) if k == "pale"]
        dark_i = [i for i, k in enumerate(mix) if k == "dark"]
        lp = T("pale", 30, CREAM, weight=BOLD)
        ld = T("nearly black", 30, DUSK_LINE, weight=BOLD)
        self.at("Some are pale")
        self.play(LaggedStart(*[FadeIn(ms[i], scale=0.6) for i in pale_i], lag_ratio=0.15), run_time=1.0)
        lp.move_to([-3.6, -2.95, 0]); self.play(FadeIn(lp), run_time=0.3)
        self.at("nearly black")
        self.play(LaggedStart(*[FadeIn(ms[i], scale=0.6) for i in dark_i], lag_ratio=0.15), run_time=0.8)
        ld.move_to([3.2, -2.95, 0]); self.play(FadeIn(ld), run_time=0.3)

        # soot
        self.at("soot darkened")
        lab = T("sooty trees", 34, GREY, weight=BOLD).move_to([0, -2.95, 0])
        mostly_dark = ["dark", "dark", "pale", "dark", "dark", "dark", "dark", "dark"]
        ms2 = place(mostly_dark, pts8)
        self.play(FadeOut(VGroup(*ms)), FadeOut(lp), FadeOut(ld), bark_to(P, "soot"), FadeIn(lab), run_time=1.0)
        self.at("dark moths became common")
        self.play(FadeIn(VGroup(*ms2), scale=0.7), run_time=0.8)
        # clean
        self.at("Later the air got cleaner")
        lab2 = T("cleaner air, later", 34, GREY, weight=BOLD).move_to([0, -2.95, 0])
        self.play(bark_to(P, "clean"), FadeOut(VGroup(*ms2)), ReplacementTransform(lab, lab2), run_time=1.0)
        mostly_pale = ["pale", "pale", "dark", "pale", "pale", "pale", "pale", "pale"]
        ms3 = place(mostly_pale, pts8)
        self.at("dark moths became rare")
        self.play(FadeIn(VGroup(*ms3), scale=0.7), run_time=0.8)
        # the puzzle
        nm = T("No adult moth changed\nits wing colour", 48, TEXT, weight=BOLD).move_to([0, 0.0, 0])
        nmg = nm
        self.at("moth changed")
        self.play(FadeOut(VGroup(P, head, lab2, *ms3)), FadeIn(nmg), run_time=0.6)
        self.at("So why do some traits")
        q = T("Why do some traits become\nmore common over time?", 50, YELLOW, weight=BOLD, line_spacing=0.9)
        qg = q.move_to([0, 0.0, 0])
        self.play(FadeOut(nmg), run_time=0.3)
        self.play(FadeIn(qg, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Population(SpokenScene):
    def construct(self):
        W, H, CX, CY = 7.6, 4.6, -2.6, -0.3
        P = panel(W, H, CX, CY, "clean")
        P.set_fill(BG, 1)
        P.set_stroke(TEAL, 3)
        pts = grid_pts(W, H, CX, CY, jit=JIT)
        ms = place(KINDS12, pts)
        head = T("One wood", 36, font=TITLE_FONT).move_to([CX, 2.75, 0])
        self.at("The moths in one wood")
        self.play(Create(P), FadeIn(head), LaggedStart(*[FadeIn(m, scale=0.6) for m in ms], lag_ratio=0.04), run_time=0.8)
        pop = T("population", 40, TEAL, weight=BOLD).move_to([CX, -3.25, 0])
        self.at("are a population")
        self.play(FadeIn(pop, shift=UP * 0.1), P.animate.set_stroke(TEAL, 6), run_time=0.6)
        self.at("group of the same kind")
        self.play(*pulse_anim(ms, 1.12), rate_func=there_and_back, run_time=1.2)
        # not all the same
        self.at("not all the same")
        rings = []
        for i in (1, 0):
            rings.append(ring(ms[i], TEAL, 0.55))
        tp = T("pale", 28, CREAM, weight=BOLD).next_to(rings[0], DOWN, buff=0.05)
        td = T("dark", 28, DUSK_LINE, weight=BOLD).next_to(rings[1], DOWN, buff=0.05)
        self.at("Some moths are pale")
        self.play(Create(rings[0]), FadeIn(tp), run_time=0.5)
        self.at("some are dark")
        self.play(Create(rings[1]), FadeIn(td), run_time=0.5)
        # inherited
        self.at("is inherited")
        self.play(FadeOut(VGroup(*rings, tp, td)), run_time=0.3)
        rx = 3.55
        inh_head = T("inherited", 42, TEAL, weight=BOLD).move_to([rx + 1.4, 2.75, 0])
        inh_sub = T("in this model", 28, GREY).move_to([rx + 1.4, 2.2, 0])
        pa = moth("pale", 1.15).move_to([rx - 0.4, 0.75, 0])
        pb = moth("dark", 1.15).move_to([rx - 0.4, -1.35, 0])
        ya = moth("pale", 0.8).move_to([rx + 2.7, 0.75, 0])
        yb = moth("dark", 0.8).move_to([rx + 2.7, -1.35, 0])
        a1 = Arrow(pa.get_right() + [0.15, 0, 0], ya.get_left() + [-0.15, 0, 0], buff=0.05, color=GREEN, stroke_width=5)
        a2 = Arrow(pb.get_right() + [0.15, 0, 0], yb.get_left() + [-0.15, 0, 0], buff=0.05, color=GREEN, stroke_width=5)
        l1 = T("parent", 26, GREY).next_to(pa, UP, buff=0.3).shift(DOWN * 0.1)
        l2 = T("young", 26, GREEN).next_to(ya, UP, buff=0.3).shift(DOWN * 0.1)
        self.play(FadeIn(inh_head), FadeIn(inh_sub), FadeIn(pa), FadeIn(pb), FadeIn(l1), run_time=0.6)
        self.at("young moths have")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(ya, shift=RIGHT * 0.2), FadeIn(yb, shift=RIGHT * 0.2), FadeIn(l2), run_time=0.9)
        self.at("have their")
        self.play(*pulse_anim([pa, ya, pb, yb], 1.2), rate_func=there_and_back, run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Birds(SpokenScene):
    def construct(self):
        W, H, CX, CY = 7.6, 4.6, -2.6, -0.3
        P = panel(W, H, CX, CY, "clean")
        P.set_fill(BG, 1); P.set_stroke(TEAL, 3)
        pts = grid_pts(W, H, CX, CY, jit=JIT)
        ms = place(KINDS12, pts)
        self.add(P, *ms)
        # expand to the wide panel
        W2, H2 = 11.4, 4.4
        P2 = panel(W2, H2, PX, PY, "clean")
        pts2 = grid_pts(W2, H2, PX, PY, jit=JIT)
        self.at("Now add the environment")
        env = T("environment", 42, TEAL, weight=BOLD).move_to([0, 2.8, 0])
        self.play(Transform(P, P2), *[m.animate.move_to(p) for m, p in zip(ms, pts2)], FadeIn(env), run_time=1.0)
        # chips: bark, air, food, predators
        self.at("such as bark")
        names = ["bark", "air", "food", "predators"]
        chips = [chip(n, GREY, size=28) for n in names]
        row = VGroup(*chips).arrange(RIGHT, buff=0.4).move_to([0, 2.8, 0])
        self.play(FadeOut(env), run_time=0.2)
        self.play(FadeIn(chips[0], shift=DOWN * 0.1), run_time=0.4)
        self.at("air")
        self.play(FadeIn(chips[1], shift=DOWN * 0.1), run_time=0.3)
        self.at("food")
        self.play(FadeIn(chips[2], shift=DOWN * 0.1), run_time=0.3)
        self.at("and predators")
        self.play(FadeIn(chips[3], shift=DOWN * 0.1), run_time=0.3)
        self.at("Here the bark is dark and sooty")
        sl = T("dark, sooty bark", 34, GREY, weight=BOLD).move_to([0, -3.05, 0])
        sk = T("in this sketch (not real counts)", 26, GREY).move_to([0, 2.6, 0])
        self.play(FadeOut(row), bark_to(P, "soot"), FadeIn(sl), FadeIn(sk), run_time=0.9)
        # the bird
        br = bird(1.0).move_to([5.0, 2.55, 0])
        bl = T("bird", 28, BLUE).next_to(br, UP, buff=0.15)
        self.at("Birds spot")
        self.play(FadeIn(br), FadeIn(bl), run_time=0.5)
        self.wait(0.4)  # Keep the bird above the bark, clear of every moth.
        pale = [i for i, k in enumerate(KINDS12) if k == "pale"]
        rings = [ring(ms[i], BLUE) for i in pale]
        self.at("the pale moths stand out")
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.12), run_time=0.9)
        sw = T("pale moths stand out", 34, BLUE, weight=BOLD).move_to([0, -3.05, 0])
        self.play(FadeOut(sl), run_time=0.15)
        self.play(FadeIn(sw), run_time=0.15)
        # eat only pale moths; leave every dark moth untouched
        self.at("So birds find more pale")
        eat = pale[:4]
        crosses = []
        for i in eat:
            self.wait(0.35)
            x = cross(ms[i])
            self.play(FadeIn(x), run_time=0.15)
            crosses.append(x)
        self.at("Eaten moths have no young")
        gone = VGroup(*[ms[i] for i in eat], *crosses, *[r for r, i in zip(rings, pale)])
        lab = T("eaten: no young", 36, RED, weight=BOLD).move_to([0, -3.05, 0])
        self.play(FadeOut(gone), FadeOut(sw), FadeOut(sk), FadeOut(VGroup(br, bl)), FadeIn(lab), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Young(SpokenScene):
    def construct(self):
        W2, H2 = 11.4, 4.4
        P = panel(W2, H2, PX, PY, "soot")
        pts2 = grid_pts(W2, H2, PX, PY, jit=JIT)
        pale = [i for i, k in enumerate(KINDS12) if k == "pale"]
        eaten = set(pale[:4])  # Same four pale moths as scene 3.
        surv = [i for i in range(12) if i not in eaten]
        ms = {i: moth(KINDS12[i]).move_to(pts2[i]) for i in surv}
        self.add(P, *ms.values())
        self.at("The moths that are not eaten")
        rs = {i: ring(ms[i], GREEN, 0.58) for i in surv}
        sl = T("survivors", 36, GREEN, weight=BOLD).move_to([0, 2.8, 0])
        self.play(LaggedStart(*[Create(r) for r in rs.values()], lag_ratio=0.1), FadeIn(sl), run_time=1.0)
        # line the survivors up on a top row
        n = len(surv)
        xs = np.linspace(-4.6, 4.6, n)
        top_y, low_y = 0.8, -1.3
        self.at("live to reproduce")
        self.play(*[ms[i].animate.move_to([x, top_y, 0]) for i, x in zip(surv, xs)],
                  *[rs[i].animate.move_to([x, top_y, 0]) for i, x in zip(surv, xs)], run_time=1.0)
        self.at("To reproduce means")
        rl = T("reproduce = have young", 34, TEAL, weight=BOLD).move_to([0, 2.8, 0])
        self.play(ReplacementTransform(sl, rl), run_time=0.5)
        young = []
        arrows = []
        for i, x in zip(surv, xs):
            y = moth(KINDS12[i], 0.75).move_to([x, low_y, 0])
            a = Arrow([x, top_y - 0.42, 0], [x, low_y + 0.4, 0], buff=0.03, color=GREEN, stroke_width=4, tip_length=0.18)
            young.append(y); arrows.append(a)
        self.at("have young")
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(y)) for a, y in zip(arrows, young)], lag_ratio=0.12), run_time=1.0)
        yl = T("young", 30, GREEN, weight=BOLD).move_to([0, low_y - 0.85, 0])
        self.at("pass on genes")
        self.play(FadeIn(yl), *pulse_anim(young, 1.2), rate_func=there_and_back, run_time=0.9)
        nd = sum(1 for i in surv if KINDS12[i] == "dark")
        self.at("Most of the survivors here are dark")
        dk = [young[j] for j, i in enumerate(surv) if KINDS12[i] == "dark"]
        self.play(*pulse_anim(dk, 1.35), rate_func=there_and_back, run_time=1.0)
        gl = T("parents to young: one generation", 36, TEAL, weight=BOLD).move_to([0, -3.05, 0])
        self.at("One step from parents")
        self.play(FadeOut(rl), FadeIn(gl), run_time=0.6)
        self.at("is a generation")
        self.play(Indicate(gl, color=TEAL, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Frequency(SpokenScene):
    def construct(self):
        # four generations of a SKETCH population: 10 moths each, 4, 6, 8, 9 dark
        darks = [10, 11, 12, 13]
        N = 14
        pw, ph, gap = 2.7, 3.3, 0.45
        xs = [(k - 1.5) * (pw + gap) for k in range(4)]
        cy = 0.8
        panels, sets, labels, bars, fills = [], [], [], [], []
        for k, x in enumerate(xs):
            p = panel(pw, ph, x, cy, "soot")
            arr_ = [None] * N
            # place pale moths on spread-out cells
            pale_cells = [1, 12, 6, 9][: N - darks[k]]
            for c in range(N):
                arr_[c] = "pale" if c in pale_cells else "dark"
            ms = VGroup()
            for c in range(N):
                col, row = c % 2, c // 2
                ms.add(moth(arr_[c], 0.42).move_to([x + (col - 0.5) * 1.1, cy + (3 - row) * 0.46, 0]))
            lb = T(f"generation {k + 1}", 26, GREY).move_to([x, cy - ph / 2 - 0.3, 0])
            bo = Rectangle(width=pw, height=0.36, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to([x, -1.55, 0])
            bf = Rectangle(width=pw * darks[k] / N, height=0.36, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
            bf.align_to(bo, LEFT).align_to(bo, UP)
            panels.append(p); sets.append(ms); labels.append(lb); bars.append(bo); fills.append(bf)

        self.at("Repeat that for many generations")
        for k in range(4):
            self.play(FadeIn(panels[k]), FadeIn(sets[k], scale=0.8), FadeIn(labels[k]), run_time=0.55)
            if k == 0:
                self.wait(0.15)
        # selection arrow
        arrow = Arrow([xs[0] - 1.3, 2.8, 0], [xs[3] + 1.3, 2.8, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.3)
        self.at("matched the bark becomes more common")
        self.play(GrowArrow(arrow), run_time=0.8)
        # trait frequency
        tf = T("trait frequency", 36, TEAL, weight=BOLD).move_to([0, -2.1, 0])
        cap = T("share of dark moths, in this sketch (not real counts)", 24, GREY).move_to([0, -2.6, 0])
        self.at("trait frequency")
        self.play(FadeIn(tf), *[Create(b) for b in bars], run_time=0.7)
        self.at("In this sketch")
        self.play(FadeIn(cap), run_time=0.4)
        self.at("grows each generation")
        self.play(LaggedStart(*[GrowFromEdge(f, LEFT) for f in fills], lag_ratio=0.35), run_time=1.8)
        ns = T("natural selection", 36, TEAL, weight=BOLD).move_to([0, 3.3, 0])
        self.at("Natural selection shifts")
        self.play(FadeIn(ns, shift=DOWN * 0.1), Indicate(arrow, color=TEAL, scale_factor=1.04), run_time=0.7)
        self.at("It does not change any one moth")
        ng = T("no one moth changes", 34, TEXT, weight=BOLD).move_to([0, -3.15, 0])
        self.play(FadeIn(ng), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        P = panel(11.4, 3.9, PX, -0.1, "soot")
        pts = grid_pts(11.4, 3.9, PX, -0.1, cols=4, rows=2, jit=[(-.1, .1), (.15, -.1), (-.15, .1), (.1, 0), (.1, -.1), (-.1, .1), (.1, .1), (-.1, -.1)])
        mix = ["dark", "dark", "pale", "dark", "dark", "dark", "dark", "dark"]
        ms = place(mix, pts)
        dark_idx = [i for i, k in enumerate(mix) if k == "dark"]
        ns = T("natural selection", 44, TEAL, weight=BOLD).move_to([0, 2.7, 0])
        self.at("This is natural selection")
        self.play(FadeIn(P), FadeIn(VGroup(*ms), scale=0.8), FadeIn(ns), run_time=0.9)
        defn = T("traits that suit the environment:\nmore likely to survive and reproduce", 30, TEXT, line_spacing=0.9).move_to([0, -2.95, 0])
        self.at("Individuals with traits")
        self.play(FadeIn(defn), run_time=0.6)
        self.at("more likely to survive")
        self.play(*pulse_anim([ms[i] for i in dark_idx], 1.25), rate_func=there_and_back, run_time=1.0)
        ad = T("adaptation", 44, TEAL, weight=BOLD).move_to([0, 2.7, 0])
        self.at("is an adaptation")
        self.play(ReplacementTransform(ns, ad), run_time=0.6)
        sl = T("dark colour, sooty bark: adaptation", 32, GREEN, weight=BOLD).move_to([0, -2.7, 0])
        self.at("on sooty bark")
        self.play(FadeOut(defn), FadeIn(sl), run_time=0.5)
        # clean bark
        self.at("On clean, pale bark")
        cl = T("dark colour, clean bark: not an adaptation", 32, RED, weight=BOLD).move_to([0, -2.7, 0])
        ms_c = place(["pale", "pale", "dark", "pale", "pale", "pale", "pale", "pale"], pts)
        self.play(bark_to(P, "clean"), ReplacementTransform(sl, cl), FadeOut(VGroup(*ms)), FadeIn(VGroup(*ms_c)), run_time=1.0)
        ms = ms_c; dark_idx = [2]
        self.at("the same")
        self.play(*pulse_anim([ms[i] for i in dark_idx], 1.2), rate_func=there_and_back, run_time=0.9)
        # answer
        self.at("So why do some traits")
        q = T("Why do some traits become more common?", 40, YELLOW, weight=BOLD).move_to([0, 0.0, 0])
        self.play(FadeOut(VGroup(ad, cl, P, *ms)), FadeIn(q), run_time=0.6)
        self.at("Individuals with those traits")
        self.play(FadeOut(q), run_time=0.4)
        a1 = T("Individuals with those traits", 46, GREEN, weight=BOLD)
        a2 = T("survive and reproduce more often", 46, GREEN, weight=BOLD)
        ab = VGroup(a1, a2).arrange(DOWN, buff=0.15).move_to([0, 0.0, 0])
        self.play(FadeIn(ab, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Individuals with those traits survive and reproduce more often."
