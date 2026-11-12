"""Adaptive immunity: Receptors First, Antigen Chooses (chapter 1 film).

COLOUR MAP: V segments BLUE, D segments GREEN, J segments ORANGE; ordinary lymphocytes GREY; the
selected clone GOLD; antigen RED; yellow outline = "picked" highlight. Cells are circles, receptors are
simple notched shapes, DNA is a row of cards: no molecular structures.
"""
import math
import random
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
LIGHT = "#C9CED8"

# receptor tip shapes: (sides, start angle); 0 sides = circle
TIPS = [(3, math.pi / 2), (4, math.pi / 4), (5, math.pi / 2), (6, 0), (0, 0), (3, -math.pi / 2), (4, 0)]
MATCH = 2   # the pentagon is the tip the antigen fits


def bob(m, amp=0.05, speed=1.3, phase=None):
    """Slow ambient drift so a held frame is never dead."""
    m._bt = 0.0
    m._bo = np.zeros(3)
    ph = random.random() * 6.28 if phase is None else phase

    def up(mm, dt):
        mm._bt += dt
        o = np.array([amp * 0.6 * math.sin(mm._bt * speed * 0.8 + ph), amp * math.sin(mm._bt * speed + ph * 1.7), 0])
        mm.shift(o - mm._bo)
        mm._bo = o
    m.add_updater(up)
    return m


def drift(m, vec, dur):
    """Move m by vec over dur seconds, in the background (an updater), so cues can fire meanwhile."""
    m._dr = 0.0
    v = np.array(vec, dtype=float)

    def up(mm, dt):
        step = min(dt, dur - mm._dr)
        if step > 0:
            mm.shift(v * step / dur)
            mm._dr += step
    m.add_updater(up)
    return m


def tip_mob(k, size, color=LIGHT, fill=0.45):
    n, a = TIPS[k % len(TIPS)]
    m = Circle(radius=size * 0.85) if n == 0 else RegularPolygon(n=n, radius=size, start_angle=a)
    return m.set_stroke(color, 4).set_fill(color, fill)


class Cell(VGroup):
    """Lymphocyte: round body, short stalk, shaped receptor tip."""

    def __init__(self, x, y, k, r=0.65, color=GREY):
        super().__init__()
        self.r, self.k = r, k
        self.body = Circle(radius=r).set_stroke(color, 4).set_fill(color, 0.28).move_to([x, y, 0])
        top = self.body.get_center() + UP * r
        self.stalk = Line(top, top + UP * r * 0.45).set_stroke(color, 4)
        self.tip = tip_mob(k, r * 0.5, LIGHT if color == GREY else color).move_to(top + UP * (r * 0.45 + r * 0.42))
        self.add(self.body, self.stalk, self.tip)

    def gold(self):
        return AnimationGroup(self.body.animate.set_stroke(GOLD, 5).set_fill(GOLD, 0.55),
                              self.stalk.animate.set_stroke(GOLD, 5), self.tip.animate.set_stroke(GOLD, 5).set_fill(GOLD, 0.8))


class Antigen(VGroup):
    """Small red spiky antigen with a pentagon tab (the shape the matching receptor fits)."""

    def __init__(self, R=0.5, tab=0.3, k=MATCH):
        super().__init__()
        self.star = Star(n=7, outer_radius=R, inner_radius=R * 0.62, color=RED).set_fill(RED, 0.75).set_stroke(RED, 3)
        self.tab = tip_mob(k, tab, RED, 0.9).move_to(self.star.get_center() + DOWN * (R + tab * 0.2))
        self.add(self.tab, self.star)
        self.set_z_index(3)


def goto_tip(ant, tip, gap=0.0):
    """Shift vector that puts the antigen's tab `gap` above the tip's centre."""
    return tip.get_center() + UP * gap - ant.tab.get_center()


def crowd_row(xs, ks, y, r=0.65):
    return VGroup(*[bob(Cell(x, y, k, r), 0.05) for x, k in zip(xs, ks)])


K = 1.3   # the render is small on screen: scale every label up from the nominal size


def lab(text, size=30, color=TEXT, **kw):
    return T(text, size=size * K, color=color, **kw)


def chp(text, color=BLUE, size=26):
    return chip(text, color, size * K)


# ---------------------------------------------------------------- gene-segment rows (shared by s06-s10)
ROW_Y = {"V": 1.5, "D": 0.0, "J": -1.5}
ROW_N = {"V": 13, "D": 10, "J": 6}
ROW_C = {"V": BLUE, "D": GREEN, "J": ORANGE}
ROW_X0 = -5.0
PITCH = 0.72
COUNT = {"V": "V: 40", "D": "D: 23", "J": "J: 6"}


def card(c, w=0.62, h=1.0):
    return Rectangle(width=w, height=h).set_stroke(c, 3).set_fill(c, 0.4)


def build_rows():
    cards = {k: VGroup(*[card(ROW_C[k]).move_to([ROW_X0 + PITCH * i, ROW_Y[k], 0]) for i in range(ROW_N[k])]) for k in "VDJ"}
    letters = {k: lab(k, 40, ROW_C[k], weight=BOLD).move_to([-6.05, ROW_Y[k], 0]) for k in "VDJ"}
    counts = {k: M(COUNT[k], 30 * K, ROW_C[k]).move_to([5.45, ROW_Y[k], 0]) for k in "VDJ"}
    return cards, letters, counts


def corner_cell():
    return Cell(-6.1, 2.85, 0, r=0.38)


def gene_title():
    return lab("antibody heavy-chain genes", 30).move_to([0.8, 3.2, 0])


PICKS = [("V", 7), ("D", 4), ("J", 2)]


def highlight(card_mob, on=True):
    return card_mob.animate.set_stroke(YELLOW, 6).set_fill(YELLOW, 0.3)


def unhighlight(card_mob, k):
    return card_mob.animate.set_stroke(ROW_C[k], 3).set_fill(ROW_C[k], 0.4)


def vdj_bar(scale=1.0, n=1):
    """A little V-D-J combination: blue, green, orange blocks side by side."""
    g = VGroup(*[Rectangle(width=0.22, height=0.16).set_stroke(c, 1.5).set_fill(c, 0.7) for c in (BLUE, GREEN, ORANGE)])
    g.arrange(RIGHT, buff=0)
    return g.scale(scale)


def fan_bars(n, seed, rx=5.8, ry=2.0, cy=0.2, mind=0.5):
    rng = random.Random(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        x, y = rng.uniform(-rx, rx), rng.uniform(-ry, ry)
        if (x / rx) ** 2 + (y / ry) ** 2 > 1:
            continue
        if all((x - a) ** 2 + (y - b) ** 2 > mind ** 2 for a, b in pts):
            pts.append((x, y))
    g = VGroup()
    for x, y in pts:
        b = vdj_bar(1.0)
        b.rotate(rng.uniform(-0.5, 0.5)).move_to([x, y + cy, 0])
        g.add(b)
    return g


def answer_cards():
    a = chp("add: 40 + 23 + 6 = ?", TEXT, 24)
    m = chp("multiply: 40 x 23 x 6 = ?", YELLOW, 24)
    tot = a.width + m.width + 0.4
    a.move_to([-tot / 2 + a.width / 2, -3.1, 0])
    m.move_to([tot / 2 - m.width / 2, -3.1, 0])
    return a, m


def cycle_picks(scene, cards, sets, per=0.9):
    """Highlight one card from each row, then release it, for each (v, d, j) set: motion while the question hangs."""
    for v, d, j in sets:
        sel = [("V", v), ("D", d), ("J", j)]
        scene.play(*[highlight(cards[k][i]) for k, i in sel], run_time=per * 0.45)
        scene.wait(per * 0.3)
        scene.play(*[unhighlight(cards[k][i], k) for k, i in sel], run_time=per * 0.25)


# ================================================================ scenes
class S00Title(TitleCard):
    TITLE = "Receptors First, Antigen Chooses"
    LESSON = "Adaptive Immunity"


class S01Hook(SpokenScene):
    def construct(self):
        xs = [-5.4, -3.6, -1.8, 0, 1.8, 3.6, 5.4]
        ks = [0, 1, 3, 4, 2, 5, 6]
        row = crowd_row(xs, ks, -1.9, 0.78)
        v = Antigen(0.8, 0.39).move_to([-6.0, 1.9, 0])
        bob(v, 0.05)
        drift(v, goto_tip(v, row[4].tip, 1.0), 8.4)
        self.add(v)
        self.play(FadeIn(v), LaggedStart(*[GrowFromCenter(c) for c in row], lag_ratio=0.1), run_time=1.6)
        self.at("never met")
        label = lab("never met before", 32, RED)
        label.add_updater(lambda m: m.next_to(v, UP, buff=0.25))
        self.play(FadeIn(label), run_time=0.5)
        self.at("how could it")
        q = lab("?", 100, YELLOW, weight=BOLD)
        q.add_updater(lambda m: m.next_to(v, RIGHT, buff=0.6))
        self.play(FadeIn(q, scale=1.4), Indicate(row[4].tip, color=YELLOW, scale_factor=1.6), run_time=1.0)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.finish()


def key_set():
    shelf = Line([0.5, -1.4, 0], [6.5, -1.4, 0]).set_stroke(LIGHT, 4)
    keys = VGroup()
    for x, k in zip([1.3, 2.7, 4.1, 5.5], [0, 3, 2, 5]):
        stem = Rectangle(width=0.2, height=1.2).set_stroke(LIGHT, 3).set_fill(GREY, 0.5).move_to([x, -0.8, 0])
        keys.add(VGroup(stem, tip_mob(k, 0.4).move_to([x, 0.1, 0])))
    return shelf, keys


class S02Two(SpokenScene):
    def construct(self):
        div = Line([0, -3.6, 0], [0, 3.6, 0]).set_stroke(GREY, 2)
        l1 = lab("instructive idea", 32).move_to([-3.4, 3.3, 0])
        l2 = lab("selection", 32).move_to([3.4, 3.3, 0])
        a1 = Antigen(0.7, 0.42).move_to([-5.9, -0.2, 0])
        blob = Circle(radius=1.5).set_stroke(LIGHT, 4).set_fill(GREY, 0.45).move_to([-2.8, -0.2, 0])
        bob(a1, 0.06)
        bob(blob, 0.04)
        self.play(Create(div), FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.play(FadeIn(a1), FadeIn(blob), run_time=1.0)
        self.at("a soft general")
        clay = lab("clay", 34).move_to(blob)
        self.play(FadeIn(clay), run_time=0.6)
        self.at("fold itself")
        blob.clear_updaters()
        a1.clear_updaters()
        self.play(a1.animate.move_to([-4.15, -0.2, 0]), run_time=1.2)
        bite = Difference(blob, Circle(radius=0.8).move_to([-4.15, -0.2, 0]))
        bite.set_stroke(LIGHT, 4).set_fill(GREY, 0.45)
        self.play(Transform(blob, bite), clay.animate.shift(RIGHT * 0.5), run_time=1.6)
        self.add(a1)
        self.at("or receptors could")
        shelf, keys = key_set()
        self.play(Create(shelf), LaggedStart(*[GrowFromEdge(k, DOWN) for k in keys], lag_ratio=0.4), run_time=2.0)
        self.at("and the antigen")
        a2 = Antigen(0.7, 0.4).move_to([1.0, 2.4, 0])
        self.play(FadeIn(a2), run_time=0.4)
        head = keys[2][1]
        self.play(a2.animate.shift(goto_tip(a2, head, 1.4)), run_time=1.0, rate_func=smooth)
        self.at("fits")
        self.play(a2.animate.shift(goto_tip(a2, head, 0.0)), head.animate.set_stroke(YELLOW, 6), run_time=0.5)
        self.finish()


class S03Terms(SpokenScene):
    def construct(self):
        cell = bob(Cell(-3.6, -0.5, 2, r=1.5), 0.05)
        ant = Antigen(0.8, 0.4).move_to([4.2, 2.0, 0])
        bob(ant, 0.07)
        self.play(GrowFromCenter(cell), FadeIn(ant), run_time=1.2)
        drift(ant, [0.6, -0.9, 0], 9.0)
        self.at("lymphocytes")
        l1 = VGroup(lab("lymphocyte", 34), lab("(B cell or T cell)", 28)).arrange(DOWN, buff=0.12).move_to([-3.6, -3.05, 0])
        a1 = Arrow(l1.get_top(), cell.body.get_bottom() + DOWN * 0.02, buff=0.1, color=TEXT, stroke_width=4)
        self.play(FadeIn(l1), GrowArrow(a1), run_time=0.9)
        self.at("receptor")
        l2 = lab("receptor", 34).move_to([0.2, 2.9, 0])
        a2 = Arrow(l2.get_left(), cell.tip.get_right(), buff=0.12, color=TEXT, stroke_width=4)
        self.play(FadeIn(l2), GrowArrow(a2), Indicate(cell.tip, color=YELLOW, scale_factor=1.5), run_time=1.0)
        self.at("antigen")
        l3 = lab("antigen", 34, RED)
        l3.add_updater(lambda m: m.next_to(ant, DOWN, buff=0.45))
        self.play(FadeIn(l3), Indicate(ant, color=RED, scale_factor=1.25), run_time=1.0)
        self.finish()


class S04Burnet(SpokenScene):
    def construct(self):
        shelf, keys = key_set()
        a2 = Antigen(0.7, 0.4)
        a2.shift(goto_tip(a2, keys[2][1], 0.0))
        blob = Circle(radius=1.5).set_stroke(LIGHT, 4).set_fill(GREY, 0.45).move_to([-2.8, -0.2, 0])
        bite = Difference(blob, Circle(radius=0.8).move_to([-4.15, -0.2, 0])).set_stroke(LIGHT, 4).set_fill(GREY, 0.45)
        a1 = Antigen(0.7, 0.42).move_to([-4.15, -0.2, 0])
        clay = lab("clay", 34).move_to([-2.3, -0.2, 0])
        div = Line([0, -3.6, 0], [0, 3.6, 0]).set_stroke(GREY, 2)
        l1 = lab("instructive idea", 32).move_to([-3.4, 3.3, 0])
        l2 = lab("selection", 32).move_to([3.4, 3.3, 0])
        old = VGroup(div, bite, a1, clay, l1, l2)
        self.add(old, shelf, keys, a2)
        keys[2][1].set_stroke(YELLOW, 6)
        bob(a2, 0.04)
        self.at("macfarlane burnett")
        cap = lab("Macfarlane Burnet, 1957", 34).move_to([0, 3.3, 0])
        self.play(FadeOut(old), run_time=0.5)
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.6)
        self.at("second answer")
        self.play(Indicate(keys, color=TEXT, scale_factor=1.06), run_time=1.0)
        self.at("clonal selection")
        cs = lab("clonal selection", 38, GOLD, weight=BOLD).move_to([0, 2.4, 0])
        self.play(Write(cs), run_time=1.0)
        self.at("nearly every")
        a2.clear_updaters()
        self.play(FadeOut(VGroup(shelf, keys, a2)), run_time=0.6)
        xs = [-5.4, -3.6, -1.8, 0, 1.8, 3.6, 5.4]
        row = crowd_row(xs, [0, 1, 3, 4, 2, 5, 6], -0.6, 0.78)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in row], lag_ratio=0.12), run_time=1.4)
        self.at("receptors of one shape")
        t1 = lab("one receptor shape each", 34).move_to([0, -2.7, 0])
        self.play(FadeIn(t1), LaggedStart(*[Indicate(c.tip, color=YELLOW, scale_factor=1.35) for c in row], lag_ratio=0.15), run_time=2.0)
        self.at("before it meets")
        t2 = lab("made before antigen", 34, YELLOW).move_to([0, -2.7, 0])
        ant = Antigen(0.7, 0.4).move_to([6.2, 2.6, 0])
        bob(ant, 0.06)
        self.play(FadeTransform(t1, t2), FadeIn(ant), run_time=0.8)
        drift(ant, [-1.2, -0.3, 0], 2.5)
        self.finish()


class S05Problem(SpokenScene):
    def construct(self):
        box = Rectangle(width=5.0, height=3.4).set_stroke(TEXT, 4).set_fill(GREY, 0.2).move_to([-4.2, 0.0, 0])
        g1 = lab("genome", 36, TEXT, weight=BOLD)
        g2 = M("about 20,000", 30 * K, YELLOW)
        g3 = lab("protein-coding genes", 22)
        gt = VGroup(g1, g2, g3).arrange(DOWN, buff=0.25).move_to(box)
        self.at("but the human genome")
        self.play(Create(box), FadeIn(gt), run_time=1.2)
        self.at("receptor shapes")
        rng = random.Random(4)
        cloud = VGroup()
        pts = []
        while len(pts) < 32:
            x, y = rng.uniform(1.2, 6.4), rng.uniform(-2.3, 2.3)
            if all((x - a) ** 2 + (y - b) ** 2 > 0.8 ** 2 for a, b in pts):
                pts.append((x, y))
        for x, y in pts:
            m = tip_mob(rng.randrange(7), 0.3, LIGHT, 0.4).move_to([x, y, 0])
            bob(m, 0.1)
            cloud.add(m)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in cloud], lag_ratio=0.04), run_time=1.6)
        lc = lab("millions of receptors", 30, YELLOW).move_to([3.7, 3.3, 0])
        self.play(FadeIn(lc), run_time=0.6)
        self.at("so how can it")
        ar = Arrow([-1.5, 0.0, 0], [0.7, 0.0, 0], buff=0, color=TEXT, stroke_width=8)
        q = lab("?", 100, YELLOW, weight=BOLD).move_to([-0.4, 1.0, 0])
        self.play(GrowArrow(ar), FadeIn(q, scale=1.5), run_time=0.8)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.finish()


class S06Segments(SpokenScene):
    def construct(self):
        cell = bob(Cell(0, -0.3, 3, r=1.6), 0.05)
        self.play(GrowFromCenter(cell), run_time=1.2)
        self.at("developing b cell")
        dl = lab("developing B cell", 34).move_to([0, -2.95, 0])
        self.play(FadeIn(dl), run_time=0.6)
        self.at("heavy chain")
        self.play(Indicate(cell.tip, color=BLUE, scale_factor=1.6), run_time=1.2)
        self.at("the tip of that chain")
        cell.clear_updaters()
        small = Cell(-6.1, 2.85, 3, r=0.38)
        bar = Rectangle(width=11.6, height=0.9).set_stroke(LIGHT, 3).set_fill(GREY, 0.45).move_to([0.2, 0.0, 0])
        title = gene_title()
        self.play(Transform(cell, small), FadeOut(dl), FadeIn(bar), FadeIn(title), run_time=1.4)
        self.at("not encoded as one piece")
        sweep = Rectangle(width=0.9, height=0.92).set_stroke(width=0).set_fill(TEXT, 0.55).move_to([-5.0, 0.0, 0])
        self.add(sweep)
        self.play(sweep.animate.move_to([5.4, 0.0, 0]), run_time=2.6, rate_func=linear)
        self.remove(sweep)
        self.at("short stretches")
        cards, letters, counts = build_rows()
        allc = VGroup(*[c for k in "VDJ" for c in cards[k]])
        self.play(FadeOut(bar), LaggedStart(*[GrowFromCenter(c) for c in allc], lag_ratio=0.05), run_time=2.2)
        self.at("gene segments")
        self.play(Indicate(allc, color=TEXT, scale_factor=1.04), run_time=1.6)
        self.at("three rows")
        sweep2 = Rectangle(width=0.5, height=4.2).set_stroke(width=0).set_fill(TEXT, 0.25).move_to([-5.0, 0.0, 0])
        self.add(sweep2)
        self.play(sweep2.animate.move_to([4.0, 0.0, 0]), run_time=1.7, rate_func=linear)
        self.remove(sweep2)
        self.at("v segments")
        self.play(FadeIn(letters["V"]), FadeIn(counts["V"]), Indicate(cards["V"], color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("d segments")
        self.play(FadeIn(letters["D"]), FadeIn(counts["D"]), Indicate(cards["D"], color=GREEN, scale_factor=1.05), run_time=0.8)
        self.at("j segments")
        self.play(FadeIn(letters["J"]), FadeIn(counts["J"]), Indicate(cards["J"], color=ORANGE, scale_factor=1.06), run_time=0.8)
        note = lab("illustrative human counts", 26).move_to([0, -3.1, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


class S07Draw(SpokenScene):
    def construct(self):
        cards, letters, counts = build_rows()
        cell = corner_cell()
        title = gene_title()
        allc = VGroup(*[c for k in "VDJ" for c in cards[k]])
        self.add(allc, *letters.values(), *counts.values(), cell, title)
        for c in allc:
            bob(c, 0.02, 1.0)
        sel = {k: cards[k][i] for k, i in PICKS}
        self.at("picks")
        self.play(highlight(sel["V"]), run_time=0.5)
        self.at("1d")
        self.play(highlight(sel["D"]), run_time=0.5)
        self.at("1j")
        self.play(highlight(sel["J"]), run_time=0.5)
        self.at("enzymes cut")
        cuts = VGroup()
        for c in sel.values():
            for dx in (-0.34, 0.34):
                cuts.add(DashedLine(c.get_center() + [dx, 0.6, 0], c.get_center() + [dx, -0.6, 0], color=TEXT, stroke_width=5))
        self.play(Create(cuts), run_time=0.8)
        self.wait(0.8)
        self.at("cell joins")
        others = VGroup(*[c for k in "VDJ" for i, c in enumerate(cards[k]) if (k, i) not in PICKS])
        for c in allc:
            c.clear_updaters()
        self.play(FadeOut(others, shift=DOWN * 0.3), FadeOut(cuts), FadeOut(title), FadeOut(VGroup(*letters.values(), *counts.values())), run_time=1.2)
        bar = VGroup(sel["V"], sel["D"], sel["J"])
        targets = [[-0.93, 1.6, 0], [0.0, 1.6, 0], [0.93, 1.6, 0]]
        self.play(*[m.animate.scale(1.5).move_to(t) for m, t in zip(bar, targets)], run_time=1.4)
        for m in bar:
            m.set_stroke(m.get_stroke_color(), 3)
        bar_s = VGroup(*bar)
        self.play(*[unhighlight(sel[k], k) for k in "VDJ"], run_time=0.3)
        self.at("joined piece")
        bl = lab("heavy chain tip", 34).move_to([0, 3.0, 0])
        self.play(FadeIn(bl), Indicate(bar_s, color=TEXT, scale_factor=1.1), run_time=1.0)
        self.at("encodes the tip")
        self.play(FadeOut(bl), cell.animate.scale(3.0).move_to([0, -1.8, 0]), run_time=1.4)
        self.play(FadeOut(cell.tip), bar_s.animate.scale(0.4).move_to(cell.tip.get_center()), run_time=1.2)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        cards, letters, counts = build_rows()
        cell = corner_cell()
        title = gene_title()
        allc = VGroup(*[c for k in "VDJ" for c in cards[k]])
        self.add(allc, *letters.values(), *counts.values(), cell, title)
        note = lab("illustrative human counts", 26)
        note.move_to([0, -2.5, 0])
        self.at("illustrative")
        self.play(FadeIn(note), Indicate(VGroup(*counts.values()), color=TEXT, scale_factor=1.12), run_time=1.0)
        self.at("takes one segment")
        cycle_picks(self, cards, [(3, 6, 1), (10, 2, 4), (6, 8, 3)], per=1.0)
        self.at("do the choices")
        a, m = answer_cards()
        self.play(FadeOut(note), FadeIn(a, shift=UP * 0.2), FadeIn(m, shift=UP * 0.2), run_time=0.8)
        self.play(Indicate(a, color=TEXT, scale_factor=1.06), run_time=0.7)
        self.play(Indicate(m, color=YELLOW, scale_factor=1.06), run_time=0.7)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        cards, letters, counts = build_rows()
        cell = corner_cell()
        title = gene_title()
        a, m = answer_cards()
        allc = VGroup(*[c for k in "VDJ" for c in cards[k]])
        self.add(allc, *letters.values(), *counts.values(), cell, title, a, m)
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.34, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()), color=YELLOW, stroke_width=7).move_to([6.35, -3.0, 0]))
        self.add(ring)
        self.play(tr.animate.set_value(0.999), run_time=self.narration_s - 0.5, rate_func=linear)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        cards, letters, counts = build_rows()
        cell = corner_cell()
        title = gene_title()
        a, m = answer_cards()
        allc = VGroup(*[c for k in "VDJ" for c in cards[k]])
        self.add(allc, *letters.values(), *counts.values(), cell, title, a, m)
        self.at("they multiply")
        a2 = chp("add: 40 + 23 + 6 = 69", TEXT, 24).move_to(a)
        self.play(FadeOut(VGroup(allc, *letters.values(), *counts.values(), cell, title)), Transform(a, a2), a.animate.set_opacity(0.4), run_time=1.0)
        m.set_z_index(2)
        self.play(m[0].animate.set_fill(YELLOW, 0.4), Indicate(m, color=YELLOW, scale_factor=1.05), run_time=0.8)
        fan = fan_bars(70, 11)
        order = list(range(len(fan)))
        random.Random(2).shuffle(order)
        self.at("every v")
        m2 = chp("multiply: 40 x 23 = 920", YELLOW, 24).move_to(m)
        first = VGroup(*[fan[i] for i in order[:24]])
        self.play(Transform(m, m2), LaggedStart(*[GrowFromCenter(b) for b in first], lag_ratio=0.05), run_time=1.8)
        self.at("every such pair")
        m3 = chp("multiply: 920 x 6 = 5,520", YELLOW, 24).move_to(m)
        second = VGroup(*[fan[i] for i in order[24:]])
        self.play(Transform(m, m3), LaggedStart(*[GrowFromCenter(b) for b in second], lag_ratio=0.03), run_time=2.4)
        self.at("thousands of")
        l1 = lab("5,520 V-D-J combinations", 34, YELLOW).move_to([0, 3.4, 0])
        self.play(FadeIn(l1), run_time=0.6)
        self.at("variable region")
        l2 = lab("(heavy-chain variable region)", 26).move_to([0, 2.85, 0])
        self.play(FadeIn(l2), Indicate(fan, color=TEXT, scale_factor=1.03), run_time=1.0)
        self.finish()


class S11More(SpokenScene):
    def construct(self):
        fan = fan_bars(70, 11)
        l1 = lab("5,520 V-D-J combinations", 34, YELLOW).move_to([0, 3.4, 0])
        l2 = lab("(heavy-chain variable region)", 26).move_to([0, 2.85, 0])
        self.add(fan, l1, l2)
        self.at("only one chain")
        self.play(Indicate(fan, color=TEXT, scale_factor=1.04), run_time=1.2)
        self.at("light chains")
        c1 = chp("light chain: V + J only", ORANGE, 22).move_to([-3.4, -2.45, 0])
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.8)
        self.at("t cells build")
        c2 = chp("T cells: own segments", TEAL, 22).move_to([3.4, -2.45, 0])
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.8)
        self.at("imprecise joins")
        c3 = chp("imprecise joins  x", YELLOW, 22).move_to([-3.4, -3.35, 0])
        self.play(FadeIn(c3, shift=UP * 0.2), run_time=0.8)
        self.at("chain pairing")
        c4 = chp("chain pairing  x", YELLOW, 22).move_to([3.4, -3.35, 0])
        self.play(FadeIn(c4, shift=UP * 0.2), run_time=0.8)
        self.at("multiply the variety")
        more = fan_bars(150, 23, mind=0.3)
        l3 = lab("millions of shapes, before any antigen", 34, YELLOW).move_to([0, 3.3, 0])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in more], lag_ratio=0.02), FadeOut(VGroup(l1, l2)), run_time=2.2)
        self.play(FadeIn(l3), run_time=0.8)
        self.finish()


class S12Shop(SpokenScene):
    def construct(self):
        xs = [-6.0 + 1.5 * i for i in range(9)]
        ys = [1.9, 0.0, -1.9]
        rng = random.Random(9)
        cells = VGroup(*[Cell(x, y - 0.3, rng.randrange(7), r=0.45) for y in ys for x in xs])
        shoes = VGroup()
        for c in cells:
            x, y = c.body.get_center()[:2]
            k = c.k
            sole = RoundedRectangle(corner_radius=0.06, width=1.1, height=0.2).set_stroke(LIGHT, 3).set_fill(GREY, 0.6)
            h1, h2 = 0.2 + 0.1 * (k % 3), 0.34 + 0.07 * (k % 4)
            up = Polygon([-0.52, 0, 0], [-0.52, h1, 0], [0.0, h2, 0], [0.52, 0.16, 0], [0.52, 0, 0]).set_stroke(LIGHT, 3).set_fill(GREY, 0.4)
            up.next_to(sole, UP, buff=0)
            sh = VGroup(sole, up).move_to([x, y + 0.1, 0])
            shoes.add(sh)
        for c in cells:
            bob(c, 0.05)
        cells.scale(2.4)
        self.add(cells)
        self.play(cells.animate.scale(1 / 2.4), run_time=1.6)
        self.at("vast crowd")
        l1 = lab("a vast crowd of lymphocytes", 30).move_to([0, 3.5, 0])
        self.play(FadeIn(l1), run_time=0.6)
        self.at("each with its own")
        self.play(LaggedStart(*[Indicate(c.tip, color=YELLOW, scale_factor=1.5) for c in cells[:9]], lag_ratio=0.1), run_time=1.6)
        self.at("shoe shop")
        shelves = VGroup(*[Line([-6.7, y - 0.45, 0], [6.7, y - 0.45, 0]).set_stroke(LIGHT, 5) for y in ys])
        l2 = lab("a shoe shop", 34, YELLOW).move_to([0, 3.5, 0])
        keep = cells.copy()
        for c in cells:
            c.clear_updaters()
        self.play(FadeOut(cells), FadeIn(shoes), FadeIn(shelves), FadeTransform(l1, l2), run_time=1.6)
        self.at("waiting for")
        l3 = lab("waiting for the right customer", 30).move_to([0, 3.5, 0])
        self.play(FadeTransform(l2, l3), run_time=0.6)
        self.play(LaggedStart(*[Indicate(s, color=YELLOW, scale_factor=1.15) for s in list(shoes)[::3][:9]], lag_ratio=0.2), run_time=1.6)
        self.play(FadeOut(shoes), FadeOut(shelves), FadeIn(keep), run_time=1.4)
        self.finish()


ROW13_Y = -1.3
X13 = [-5.5, -3.3, -1.1, 1.1, 3.3, 5.5]
K13 = [0, 1, 3, 4, 2, 5]


class S13Arrive(SpokenScene):
    def construct(self):
        row = crowd_row(X13, K13, ROW13_Y, 0.85)
        self.add(row)
        ant = Antigen(0.75, 0.425).move_to([-6.0, 2.3, 0])
        bob(ant, 0.04)
        self.at("antigen arrives")
        self.play(FadeIn(ant), run_time=0.5)
        self.at("drifts past")
        ant.clear_updaters()
        for i in range(3):
            self.play(ant.animate.shift(goto_tip(ant, row[i].tip, 1.3)), run_time=0.6)
            self.play(ant.animate.shift(DOWN * 1.0), row[i].animate.shift(DOWN * 0.08), run_time=0.35)
            self.play(ant.animate.shift(UP * 1.2).rotate(0.4), row[i].animate.shift(UP * 0.08), run_time=0.45)
            self.play(ant.animate.rotate(-0.4), run_time=0.25)
        self.at("it binds only")
        self.play(ant.animate.shift(goto_tip(ant, row[4].tip, 1.3)), run_time=1.2)
        self.play(ant.animate.shift(goto_tip(ant, row[4].tip, 0.0)), run_time=0.7)
        row[4].add(ant)
        self.at("already fit")
        self.play(row[4].gold(), Indicate(row[4], color=GOLD, scale_factor=1.12), run_time=1.2)
        self.at("t cells need")
        n1 = lab("T cells: antigen must be displayed", 26).move_to([0, -3.05, 0])
        n2 = lab("on another cell (see text)", 26).move_to([0, -3.55, 0])
        self.play(FadeIn(n1), FadeIn(n2), run_time=1.0)
        self.play(Indicate(row[4], color=GOLD, scale_factor=1.1), run_time=1.0)
        self.finish()


class S14Clone(SpokenScene):
    def construct(self):
        row = crowd_row(X13, K13, ROW13_Y, 0.85)
        g = row[4]
        g.clear_updaters()
        self.add(row)
        g.body.set_stroke(GOLD, 5).set_fill(GOLD, 0.55)
        g.stalk.set_stroke(GOLD, 5)
        g.tip.set_stroke(GOLD, 5).set_fill(GOLD, 0.8)
        cx = [-0.55, 0.75, 2.05, 3.35]
        yB, yA = 1.1, 2.45
        B = [np.array([x, yB, 0]) for x in cx]
        A = [np.array([x, yA, 0]) for x in cx]

        def kid(p):
            c = Cell(p[0], p[1], 2, r=0.33, color=GOLD)
            c.body.set_fill(GOLD, 0.55)
            return c
        self.at("those cells divide")
        c0 = g.body.get_center()
        self.play(g.animate.scale(0.5, about_point=c0).shift(B[3] - c0), run_time=1.2)
        stage1 = [kid(B[2])]
        self.play(*[GrowFromPoint(c, g.body.get_center()) for c in stage1], run_time=0.9)
        self.at("descendants")
        stage2 = [kid(A[3]), kid(A[2])]
        self.play(*[GrowFromPoint(c, B[3 - i]) for i, c in enumerate(stage2)], run_time=1.0)
        self.at("form a clone")
        stage3 = [kid(B[1]), kid(B[0]), kid(A[1]), kid(A[0])]
        self.play(LaggedStart(*[GrowFromPoint(c, B[2]) for c in stage3], lag_ratio=0.2), run_time=1.4)
        cl = lab("clone", 38, GOLD, weight=BOLD).move_to([5.5, 2.0, 0])
        self.play(FadeIn(cl), run_time=0.6)
        self.at("all starting with")
        l2 = lab("same receptor", 28, GOLD).move_to([-3.6, 2.0, 0])
        allk = [g] + stage1 + stage2 + stage3
        self.play(FadeIn(l2), LaggedStart(*[Indicate(c.tip, color=YELLOW, scale_factor=1.6) for c in allk], lag_ratio=0.1), run_time=1.8)
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        left = Cell(-3.7, -0.3, 2, r=1.1, color=GOLD)
        left.body.set_fill(GOLD, 0.55)
        left.tip.set_fill(GOLD, 0.8)
        right = left.copy().shift(RIGHT * 7.4)
        ant = Antigen(0.8, 0.55).move_to([6.5, 2.0, 0])
        ant.shift(np.array([6.4, 0, 0]) - ant.tab.get_center() + np.array([0, right[2].get_center()[1], 0]))
        for m in (left, right):
            bob(m, 0.04)
        l_a = lab("before antigen", 30).move_to([-3.7, -2.2, 0])
        self.play(GrowFromCenter(left), run_time=1.0)
        self.add(right)
        self.play(FadeIn(l_a), FadeIn(right), FadeIn(ant), run_time=0.8)
        self.at("mold that receptor")
        self.play(ant.animate.shift(goto_tip(ant, right[2], 0.0)), run_time=1.0)
        right.add(ant)
        l_b = lab("at first contact", 30).move_to([3.7, -2.2, 0])
        self.play(FadeIn(l_b), run_time=0.5)
        self.at("it existed before")
        eq = lab("=", 90, YELLOW, weight=BOLD).move_to([0, 0.5, 0])
        nm = VGroup(lab("not molded", 30, YELLOW), lab("by antigen", 30, YELLOW)).arrange(DOWN, buff=0.1).move_to([0, -0.7, 0])
        self.play(FadeIn(eq, scale=1.4), FadeIn(nm), run_time=1.0)
        self.play(Indicate(left.tip, color=TEXT, scale_factor=1.4), Indicate(right[2], color=TEXT, scale_factor=1.4), run_time=1.2)
        self.at("the antigen chooses")
        blob = Circle(radius=0.7).set_stroke(LIGHT, 4).set_fill(GREY, 0.45).move_to([-2.4, -3.0, 0])
        ctext = lab("clay: instructive idea", 28).move_to([1.5, -3.0, 0])
        cross = VGroup(Line([-3.2, -2.3, 0], [-1.6, -3.7, 0]), Line([-3.2, -3.7, 0], [-1.6, -2.3, 0])).set_stroke(RED, 9)
        self.play(FadeOut(VGroup(l_a, l_b)), FadeIn(blob), FadeIn(ctext), run_time=0.8)
        self.at("does not shape")
        self.play(Create(cross), run_time=0.9)
        self.finish()


class S16End(EndCard):
    LINE = "Receptors come first; the antigen only chooses which cells multiply."
