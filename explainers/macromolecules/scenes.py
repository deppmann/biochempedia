"""Macromolecules: Take It Apart, Build It Again (Biochemistrypedia high school Biology film)

COLOUR MAP: simple sugar = GOLD hexagon; amino acid = BLUE bead; nucleotide = GREEN bead with tab;
fatty acid = ORANGE wavy tail; glycerol = ORANGE comb; water = light-blue bent V; links = grey bars.
Counters (top right) track links and waters. Blocks are labelled cartoons, never structures.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

AMINO = "#4C7DFF"
WATER = "#A8E6FF"
ORANGE = "#F29E4C"
GUT = "#E58FA0"
CELL_C = np.array([3.0, -0.5, 0.0])


# ------------------------------------------------------------------ helpers
def wiggle(m, amp=0.06, w=1.6, seed=0.0):
    """slow ambient motion that composes with other animations (adds only the change in offset)."""
    m._wo = np.zeros(3)
    m._wt = seed * 3.1

    def u(mm, dt):
        mm._wt += dt
        off = np.array([0.6 * amp * np.cos(w * mm._wt * 0.8 + seed), amp * np.sin(w * mm._wt + seed * 2), 0])
        mm.shift(off - mm._wo)
        mm._wo = off
    m.add_updater(u)
    return m


def wig_all(mobs, amp=0.06):
    for i, m in enumerate(mobs):
        wiggle(m, amp, 1.4 + 0.15 * (i % 4), i * 0.9)


def sugar(r=0.45, label=None):
    back = RegularPolygon(6, radius=r, start_angle=0, stroke_width=0, fill_color=BG, fill_opacity=1)
    front = RegularPolygon(6, radius=r, start_angle=0, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.4)
    g = VGroup(back, front)
    if label:
        g.add(T(label, 28, TEXT).move_to(front))
    g.set_z_index(2)
    return g


def amino(letter="", r=0.4, tint=None):
    c = tint or AMINO
    back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1)
    front = Circle(radius=r, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.4)
    g = VGroup(back, front)
    if letter:
        g.add(T(letter, 26, TEXT).move_to(front))
    g.set_z_index(2)
    return g


def nuc(r=0.4):
    back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1)
    front = Circle(radius=r, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4)
    tab = Rectangle(width=0.22, height=0.26, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.7)
    tab.move_to(front.get_top() + UP * 0.1)
    g = VGroup(back, front, tab)
    g.set_z_index(2)
    return g


def fatty_group(scale=1.0):
    comb = VGroup(Line([0, 0.55, 0], [0, -0.55, 0]), *[Line([0, y, 0], [0.35, y, 0]) for y in (0.5, 0, -0.5)])
    comb.set_stroke(ORANGE, 6)
    tails = VGroup(*[ParametricFunction(lambda t, y=y: np.array([0.35 + t, y + 0.1 * np.sin(7 * t), 0]), t_range=[0, 1.0, 0.02],
                                        color=ORANGE, stroke_width=5) for y in (0.5, 0, -0.5)])
    g = VGroup(comb, tails).scale(scale)
    return g, comb, tails


def vee(dashed=False, s=1.4):
    v = VMobject()
    v.set_points_as_corners([[-0.2, 0.22, 0], [0, 0, 0], [0.2, 0.22, 0]])
    v.set_stroke(WATER, 6)
    if dashed:
        g = VGroup(DashedVMobject(v, num_dashes=6), Dot(radius=0.08, color=WATER).set_opacity(0.7))
    else:
        g = VGroup(v, Dot(radius=0.09, color=WATER))
    g.scale(s)
    g.set_z_index(3)
    return g


def mk_bar(a, b, w=9):
    l = Line(a.get_center(), b.get_center(), color=GREY, stroke_width=w)
    l.add_updater(lambda m, a=a, b=b: m.put_start_and_end_on(a.get_center(), b.get_center()))
    l.set_z_index(1)
    return l


class Chain:
    def __init__(self, blocks, w=9):
        self.blocks = blocks
        self.bars = [mk_bar(a, b, w) for a, b in zip(blocks, blocks[1:])]
        self.group = VGroup(*self.bars, *self.blocks)

    def build(self, lag=0.3):
        an = []
        for i, b in enumerate(self.blocks):
            parts = [FadeIn(b, scale=0.6)]
            if i > 0:
                parts.insert(0, FadeIn(self.bars[i - 1]))
            an.append(AnimationGroup(*parts))
        return LaggedStart(*an, lag_ratio=lag)

    def mid(self, j):
        return (self.blocks[j].get_center() + self.blocks[j + 1].get_center()) / 2


class Counters:
    def __init__(self, a=5, b=0, label2="waters"):
        self.a, self.b, self.l2 = ValueTracker(a), ValueTracker(b), label2

        def row(tr, lab, y):
            def mk():
                v = tr.get_value()
                s = "?" if v < 0 else str(int(round(v)))
                g = VGroup(T(lab(), 26, TEXT), M(s, 30, WATER)).arrange(RIGHT, buff=0.3)
                g.move_to([6.7 - g.width / 2, y, 0])
                return g
            return always_redraw(mk)
        self.rows = VGroup(row(self.a, lambda: "links", 3.45), row(self.b, lambda: self.l2, 2.9))
        self.box_pt = np.array([5.0, 3.2, 0])

    def pulse_rect(self):
        return Rectangle(width=3.6, height=1.2, stroke_color=YELLOW, stroke_width=4).move_to(self.box_pt)


def tally(center=(-4.1, 0.4)):
    cx, cy = center
    box = Rectangle(width=4.2, height=3.2, stroke_color=WATER, stroke_width=3, fill_color=WATER, fill_opacity=0.06).move_to([cx, cy, 0])
    title = T("water missing", 28, WATER).move_to([cx, cy + 1.25, 0])
    sub = T("counted from free blocks", 24, TEXT).move_to([cx, cy - 1.95, 0])
    slots = [np.array([cx + (c - 1) * 1.2, cy + 0.35 - r * 1.0, 0]) for r in range(2) for c in range(3)]
    return VGroup(box, title, sub), slots


def cell_mob():
    return Ellipse(width=7.6, height=5.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.22).move_to(CELL_C)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "What Am I Made Of?"
    TITLE = "Take It Apart, Build It Again"


def sandwich():
    top = RoundedRectangle(corner_radius=0.4, width=3.8, height=0.9, fill_color="#C8934F", fill_opacity=1, stroke_color="#E0B070", stroke_width=3)
    turk = RoundedRectangle(corner_radius=0.2, width=3.6, height=0.55, fill_color="#E8A3A0", fill_opacity=1, stroke_color="#F2C0BD", stroke_width=3)
    bot = RoundedRectangle(corner_radius=0.3, width=3.8, height=0.7, fill_color="#C8934F", fill_opacity=1, stroke_color="#E0B070", stroke_width=3)
    g = VGroup(top, turk, bot).arrange(DOWN, buff=0.08).scale(1.65)
    return g


def wheat():
    stem = Line([0, 0, 0], [0, 1.1, 0], color=GOLD, stroke_width=5)
    grains = VGroup(*[Ellipse(width=0.16, height=0.34, fill_color=GOLD, fill_opacity=0.8, stroke_width=0).rotate(a).move_to([x, y, 0])
                      for y in (0.5, 0.75, 1.0) for x, a in ((-0.14, 0.5), (0.14, -0.5))])
    return VGroup(stem, grains)


def bird():
    body = Ellipse(width=1.0, height=0.6, fill_color="#C97B4A", fill_opacity=1, stroke_width=0)
    head = Circle(radius=0.2, fill_color="#C97B4A", fill_opacity=1, stroke_width=0).move_to([0.5, 0.25, 0])
    beak = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.1).rotate(-PI / 2).move_to([0.74, 0.25, 0])
    tail = Polygon([-0.45, 0, 0], [-0.85, 0.25, 0], [-0.85, -0.1, 0], fill_color="#C97B4A", fill_opacity=1, stroke_width=0)
    return VGroup(tail, body, head, beak)


class S01Hook(SpokenScene):
    def construct(self):
        sw = sandwich().move_to([-3.7, -0.4, 0])
        head = Circle(radius=0.75, stroke_color=TEXT, stroke_width=5)
        torso = RoundedRectangle(corner_radius=0.9, width=2.9, height=3.3, stroke_color=TEXT, stroke_width=5)
        teen = VGroup(head, torso).arrange(DOWN, buff=0.15).scale(1.3).move_to([4.5, -0.2, 0])
        arrow_line = DashedLine([-0.1, -0.5, 0], [2.2, -0.5, 0], color=GREY, stroke_width=6, dash_length=0.22)
        tip = Triangle(fill_color=GREY, fill_opacity=1, stroke_width=0).scale(0.17).rotate(-PI / 2).move_to([2.35, -0.5, 0])
        q = T("?", 150, GOLD, weight=BOLD).move_to([1.1, 0.8, 0])
        wh = wheat().scale(1.3).move_to([-5.6, 2.7, 0])
        wl = T("wheat", 28, TEXT).next_to(wh, RIGHT, buff=0.15)
        bd = bird().scale(1.3).move_to([-2.6, 2.7, 0])
        bl = T("bird", 28, TEXT).next_to(bd, RIGHT, buff=0.15)
        wig_all([sw, teen, q], 0.07)
        wig_all([wh, bd], 0.05)
        self.wait(0.2)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in sw], lag_ratio=0.25), run_time=1.4)
        self.at("part of you")
        self.play(FadeIn(teen, shift=LEFT * 0.4), Create(arrow_line), FadeIn(tip), run_time=1.4)
        self.at("wheat plant")
        self.play(FadeIn(wh, scale=0.5), FadeIn(wl), run_time=0.7)
        self.at("a bird")
        self.play(FadeIn(bd, scale=0.5), FadeIn(bl), run_time=0.7)
        self.at("turn into part")
        self.play(FadeIn(q, scale=0.4), run_time=0.9)
        self.finish()


STARCH_Y = 1.7
PROT_Y = -1.5
STARCH_X = lambda i: -4.4 + 1.75 * i
PROT_X = lambda i: -4.5 + 1.5 * i
LETTERS = ["A", "K", "L", "S", "G", "V", "T"]


def starch_chain(final=True):
    bl = [sugar(0.6).move_to([STARCH_X(i), STARCH_Y, 0]) for i in range(6)]
    return Chain(bl)


def protein_chain():
    bl = [amino(LETTERS[i], 0.5).move_to([PROT_X(i), PROT_Y, 0]) for i in range(7)]
    return Chain(bl)


class S02Chains(SpokenScene):
    def construct(self):
        bread = VGroup(RoundedRectangle(corner_radius=0.7, width=6.2, height=3.6, fill_color="#C8934F", fill_opacity=1,
                                        stroke_color="#E0B070", stroke_width=5),
                       RoundedRectangle(corner_radius=0.6, width=5.2, height=2.7, fill_color="#E6C48A", fill_opacity=1, stroke_width=0))
        bread.move_to([0, 0.2, 0])
        bl = T("bread", 40, BG, weight=BOLD).move_to(bread)
        bread.add(bl)
        starch = Chain([sugar(0.65).move_to([STARCH_X(i), 0.5, 0]) for i in range(6)])
        wig_all(starch.blocks, 0.06)
        wiggle(bread, 0.06)
        self.play(FadeIn(bread, scale=0.5), run_time=1.0)
        self.play(bread.animate.scale(1.25), run_time=1.6)
        self.at("Its starch")
        slab = T("starch", 40, GOLD, weight=BOLD).move_to([0, 1.8, 0])
        self.play(FadeOut(bread), starch.build(0.3), FadeIn(slab), run_time=2.3)
        self.at("Now zoom into the turkey")
        turkey = VGroup(RoundedRectangle(corner_radius=0.5, width=6.4, height=2.4, fill_color="#E8A3A0", fill_opacity=1,
                                         stroke_color="#F2C0BD", stroke_width=5),
                        T("turkey", 40, BG, weight=BOLD)).move_to([0, -1.5, 0])
        wiggle(turkey, 0.06)
        self.play(*[starch.blocks[i].animate.move_to([STARCH_X(i), STARCH_Y, 0]) for i in range(6)],
                  slab.animate.move_to([0, 2.95, 0]), FadeIn(turkey, scale=0.5), run_time=1.5)
        self.play(turkey.animate.scale(1.15), run_time=1.2)
        prot = protein_chain()
        wig_all(prot.blocks, 0.06)
        self.at("Its proteins")
        self.play(FadeOut(turkey), prot.build(0.3), run_time=2.6)
        pl = T("protein: amino acids of many kinds", 30, AMINO, weight=BOLD).move_to([0, -2.7, 0])
        self.at("amino acids of many kinds")
        self.play(FadeIn(pl), run_time=0.8)
        self.finish()


def coil_pts(n=6):
    out = []
    for i in range(n):
        a = np.radians(110 - 62 * i)
        r = 2.4 - 0.22 * i
        out.append([r * np.cos(a), -0.4 + r * np.sin(a) * 0.95, 0])
    return out


class S03Words(SpokenScene):
    def construct(self):
        st = starch_chain()
        wig_all(st.blocks, 0.06)
        self.add(st.group)
        self.wait(0.3)
        self.at("monomer")
        ring = Circle(radius=0.8, stroke_color=YELLOW, stroke_width=5).move_to(st.blocks[0])
        ml = T("monomer", 36, YELLOW, weight=BOLD).move_to([STARCH_X(0), 0.45, 0])
        self.play(Create(ring), FadeIn(ml), run_time=0.9)
        self.at("polymer")
        rect = RoundedRectangle(corner_radius=0.4, width=10.4, height=1.9, stroke_color=TEAL, stroke_width=5).move_to([0, STARCH_Y, 0])
        pl = T("polymer", 36, TEAL, weight=BOLD).move_to([0, 2.95, 0])
        self.play(FadeIn(rect, scale=1.05), FadeIn(pl), run_time=1.0)
        self.at("beads on a necklace", lead=0.5)
        self.play(FadeOut(ring), FadeOut(ml), FadeOut(rect), FadeOut(pl), run_time=0.4)
        arc = ArcBetweenPoints([-4.2, 1.7, 0], [4.2, 1.7, 0], angle=PI * 0.8, color=GREY, stroke_width=3)
        arc.flip(RIGHT).move_to([0, 0.5, 0]) if False else None
        arc = ArcBetweenPoints([4.2, 1.2, 0], [-4.2, 1.2, 0], angle=-PI * 0.7).set_stroke(GREY, 3)
        beads = VGroup(*[Circle(radius=0.2, fill_color=TEXT, fill_opacity=0.9, stroke_width=0).move_to(arc.point_from_proportion(p))
                         for p in np.linspace(0.04, 0.96, 9)])
        nl = VGroup(arc, beads)
        wiggle(nl, 0.05)
        self.play(Create(arc), LaggedStart(*[FadeIn(b, scale=0.4) for b in beads], lag_ratio=0.12), run_time=1.6)
        self.at("real chains fold")
        tag = T("the analogy breaks: chains fold", 30, YELLOW).move_to([0, -3.3, 0])
        pts = coil_pts()
        self.play(FadeOut(nl), *[st.blocks[i].animate.move_to(pts[i]) for i in range(6)], run_time=2.6)
        self.play(FadeIn(tag), run_time=0.7)
        self.finish()


class S04Gut(SpokenScene):
    def construct(self):
        gut = RoundedRectangle(corner_radius=0.8, width=12.4, height=3.6, stroke_color=GUT, stroke_width=4,
                               fill_color=GUT, fill_opacity=0.2).move_to([0, -0.4, 0])
        gl = T("gut", 32, GUT, weight=BOLD).move_to([-5.7, 1.0, 0])
        ch = Chain([sugar(0.6).move_to([-4.75 + 1.9 * i, -0.5, 0]) for i in range(6)], w=12)
        wig_all(ch.blocks, 0.06)
        cn = Counters(5, 0)
        self.play(FadeIn(gut), FadeIn(gl), ch.build(0.25), FadeIn(cn.rows), run_time=2.2)
        self.at("water molecule")
        w = vee(False, 1.6).move_to([1.5, 2.0, 0])
        wl = T("H2O", 28, WATER).next_to(w, RIGHT, buff=0.15)
        wiggle(w, 0.06)
        self.play(FadeIn(w, scale=0.5), FadeIn(wl), run_time=0.8)
        self.at("slips into one link")
        tgt = ch.mid(4) + UP * 0.05
        self.play(w.animate.move_to(tgt), wl.animate.move_to(tgt + RIGHT * 1.1 + UP * 0.9), run_time=1.3)
        self.at("link breaks")
        self.play(FadeOut(ch.bars[4]), FadeOut(w, scale=0.3), FadeOut(wl),
                  ch.blocks[5].animate.move_to([5.4, 0.5, 0]),
                  cn.a.animate.set_value(4), cn.b.animate.set_value(1), run_time=1.4)
        self.at("hydrolysis")
        lab = T("hydrolysis = splitting with water", 32, WATER, weight=BOLD).move_to([0, -2.9, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=1.0)
        self.at("One water, one broken link")
        self.play(ShowPassingFlash(cn.pulse_rect().set_stroke(YELLOW, 6), time_width=1.0), run_time=1.5)
        self.finish()


def predict_frame():
    ch = Chain([sugar(0.78, str(i + 1)).move_to([-5.25 + 2.1 * i, 0.0, 0]) for i in range(6)], w=12)
    card = chip("Waters needed?", YELLOW, size=46).move_to([0, 2.6, 0])
    cn = Counters(-1, -1)
    return ch, card, cn


class S05Predict(SpokenScene):
    def construct(self):
        ch, card, cn = predict_frame()
        wig_all(ch.blocks, 0.06)
        self.add(cn.rows)
        self.play(ch.build(0.3), run_time=2.6)
        self.at("How many water")
        self.play(FadeIn(card, scale=0.8), run_time=0.9)
        self.play(ShowPassingFlash(cn.pulse_rect().set_stroke(YELLOW, 5), time_width=1.0), run_time=1.5)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        ch, card, cn = predict_frame()
        wig_all(ch.blocks, 0.06)
        self.add(ch.group, card, cn.rows)
        t = ValueTracker(0)
        ring = Circle(radius=0.5, stroke_color=GREY, stroke_width=3).move_to([6.0, -3.1, 0])
        arc = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=max(0.01, 2 * PI * (1 - t.get_value())),
                                        stroke_color=YELLOW, stroke_width=8).move_to([6.0, -3.1, 0]))
        self.add(ring, arc)
        self.play(t.animate.set_value(1), run_time=5.0, rate_func=linear)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        ch, card, cn = predict_frame()
        wig_all(ch.blocks, 0.06)
        self.add(ch.group, card, cn.rows)
        big = T("5", 130, GOLD, weight=BOLD).move_to([0, 2.55, 0])
        self.play(FadeOut(card), FadeIn(big, scale=0.4), run_time=0.8)
        self.at("Six blocks")
        self.play(cn.a.animate.set_value(5), cn.b.animate.set_value(0), run_time=0.3)
        for b in ch.bars:
            self.play(ShowPassingFlash(b.copy().set_stroke(YELLOW, 16), time_width=1.0), run_time=0.55)
        self.at("Each water breaks one link")
        for j in range(5):
            m = ch.mid(j)
            w = vee(False, 1.5).move_to(m + UP * 1.5)
            self.play(FadeIn(w, scale=0.6), run_time=0.15)
            self.play(w.animate.move_to(m + UP * 0.1), run_time=0.2)
            self.play(FadeOut(ch.bars[j]), FadeOut(w, scale=0.3), cn.a.animate.set_value(4 - j),
                      cn.b.animate.set_value(j + 1), run_time=0.2)
        self.at("one water per link")
        txt = T("6 blocks, 5 links, 5 waters", 36, WATER, weight=BOLD).move_to([0, -2.7, 0])
        offs = [0.9, -0.9, 0.8, -0.8, 0.9, -0.9]
        self.play(FadeIn(txt, shift=UP * 0.2), *[b.animate.shift(UP * offs[i]) for i, b in enumerate(ch.blocks)], run_time=2.6)
        self.finish()


class S08Travel(SpokenScene):
    def construct(self):
        vessel = Rectangle(width=6.5, height=2.2, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.15).move_to([-4.05, -0.5, 0])
        vl = T("blood vessel", 28, RED, weight=BOLD).move_to([-4.0, 1.0, 0])
        cell = cell_mob()
        cl = T("body cell", 32, TEXT, weight=BOLD).move_to([3.0, 1.75, 0])
        targets = [(1.0, -1.7), (2.3, 0.6), (3.6, -1.9), (4.9, 0.4), (5.6, -1.2), (1.4, -0.4), (2.9, -0.7), (4.2, -0.9), (5.3, 1.1), (3.4, 1.0)]
        parts = VGroup()
        for i, (tx, ty) in enumerate(targets):
            p = sugar(0.4) if i % 2 == 0 else amino("", 0.37)
            p.move_to([-0.2 - 0.75 * i, -0.5 + (0.35 if i % 3 == 0 else -0.35 if i % 3 == 1 else 0), 0])

            def mv(m, dt, tx=tx, ty=ty):
                if m.get_x() < tx:
                    m.shift(RIGHT * 0.95 * dt)
                else:
                    m.shift(UP * (ty - m.get_y()) * dt * 0.9)
            p.add_updater(mv)
            parts.add(p)
        self.add(vessel, cell)
        self.add(parts)
        self.play(FadeIn(vl), run_time=0.6)
        self.at("cells")
        self.play(FadeIn(cl), run_time=0.8)
        self.at("job turns around")
        self.play(Indicate(cell, color=YELLOW, scale_factor=1.03), run_time=1.5)
        self.at("builds new ones")
        self.play(Indicate(cell, color=YELLOW, scale_factor=1.03), run_time=1.5)
        self.finish()


SCATTER4 = [(1.2, 1.0), (4.9, 0.9), (1.6, -1.8), (5.0, -1.7)]
SCATTER6 = [(1.1, 1.1), (3.0, 1.4), (5.0, 1.0), (1.3, -1.8), (3.2, -2.0), (5.0, -1.7)]


def row_pt(i, n, y=0.3):
    return np.array([3.0 + (i - (n - 1) / 2) * (1.2 if n > 4 else 1.5), y, 0])


class S09Build(SpokenScene):
    def construct(self):
        cell = cell_mob()
        beads = [amino(LETTERS[i], 0.5).move_to([*SCATTER4[i], 0]) for i in range(4)]
        wig_all(beads, 0.12)
        cn = Counters(0, 0, "waters short")
        self.add(cell, cn.rows)
        self.play(*[FadeIn(b, scale=0.5) for b in beads], run_time=0.9)
        self.at("join into new chains")
        self.play(*[b.animate.move_to(row_pt(i, 4)) for i, b in enumerate(beads)], run_time=1.3)
        bars = [mk_bar(a, b, 10) for a, b in zip(beads, beads[1:])]
        for j, bar in enumerate(bars):
            self.play(Create(bar), cn.a.animate.set_value(j + 1), run_time=0.5)
            self.wait(0.15)
        self.at("Compare")
        tb, slots = tally()
        self.play(FadeIn(tb, shift=RIGHT * 0.3), run_time=1.0)
        self.at("One water's worth")
        for j in range(3):
            m = (beads[j].get_center() + beads[j + 1].get_center()) / 2
            v = vee(True, 1.4).move_to(m + UP * 0.9)
            self.play(FadeIn(v, scale=0.5), ShowPassingFlash(bars[j].copy().set_stroke(YELLOW, 16), time_width=1.0), run_time=0.4)
            self.play(v.animate.move_to(slots[j]), cn.b.animate.set_value(j + 1), run_time=0.9)
        self.at("dehydration synthesis")
        l1 = T("dehydration synthesis", 32, GREEN, weight=BOLD)
        l2 = T("making by removing water", 28, TEXT)
        lab = VGroup(l1, l2).arrange(DOWN, buff=0.15).move_to([-4.1, -2.75, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=1.0)
        self.finish()


class S10Back(SpokenScene):
    def construct(self):
        cell = cell_mob()
        tb, slots = tally()
        bl = [sugar(0.5).move_to([*SCATTER6[i], 0]) for i in range(6)]
        wig_all(bl, 0.12)
        cn = Counters(0, 0, "waters short")
        self.add(cell, tb, cn.rows)
        self.add(*bl)
        self.at("Breaking a chain")
        chip1 = T("breaking 6 blocks: 5 waters", 30, WATER, weight=BOLD).move_to([-3.6, 3.3, 0])
        self.play(FadeIn(chip1, shift=DOWN * 0.2), run_time=0.8)
        self.at("A chain of six built")
        self.play(FadeOut(chip1), bl[0].animate.move_to(row_pt(0, 6)), run_time=0.5)
        bars = []
        for j in range(1, 6):
            self.play(bl[j].animate.move_to(row_pt(j, 6)), run_time=0.3)
            bar = mk_bar(bl[j - 1], bl[j], 10)
            bars.append(bar)
            m = (bl[j - 1].get_center() + bl[j].get_center()) / 2
            v = vee(True, 1.4).move_to(m + UP * 0.9)
            self.play(Create(bar), FadeIn(v, scale=0.5), cn.a.animate.set_value(j), run_time=0.2)
            self.play(v.animate.move_to(slots[j - 1]), cn.b.animate.set_value(j), run_time=0.35)
        self.at("One per link either way")
        t1 = T("build 6 blocks:", 32, TEXT, weight=BOLD)
        t2 = T("5 links, 5 waters", 32, WATER, weight=BOLD)
        lab = VGroup(t1, t2).arrange(DOWN, buff=0.15).move_to([-4.1, -2.75, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=1.0)
        self.finish()


class S11Energy(SpokenScene):
    def construct(self):
        xs = [-5.1, -1.7, 1.7, 5.1]
        fg, comb, tails = fatty_group(1.2)
        blocks = [sugar(0.7), amino("", 0.6), nuc(0.6), fg]
        for b, x in zip(blocks, xs):
            b.move_to([x, 1.2, 0])
        wig_all(blocks, 0.06)
        bolt = Polygon([0.12, 0.45, 0], [-0.2, -0.05, 0], [0.0, -0.05, 0], [-0.12, -0.45, 0], [0.22, 0.1, 0], [0.02, 0.1, 0])
        icons = [bolt, Star(5, outer_radius=0.42), Square(0.6).rotate(PI / 4), Triangle().scale(0.42)]
        icons = VGroup(*icons)
        for ic, x in zip(icons, xs):
            ic.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.35).move_to([x, -1.1, 0])
        wig_all(icons, 0.05)
        arrows = VGroup(*[Arrow([x, -0.6, 0], [x, 0.25, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.2) for x in xs])
        self.wait(0.2)
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.5), run_time=2.8)
        self.at("takes energy")
        self.play(LaggedStart(*[FadeIn(i, scale=0.5) for i in icons], lag_ratio=0.3), run_time=1.6)
        self.at("In cells")
        lab = T("a different route for each kind of molecule", 32, TEXT, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.2), run_time=0.8)
        self.at("its own energy")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=1.6)
        self.at("So the real steps")
        self.play(FadeOut(VGroup(*blocks, icons, arrows, lab)), run_time=0.8)
        # part B: one join, other product leaves, tally still adds a V
        tb, slots = tally((4.3, 0.4))
        a = sugar(0.65).move_to([-4.6, 0.3, 0])
        b = sugar(0.65).move_to([-2.2, 0.3, 0])
        wig_all([a, b], 0.08)
        self.play(FadeIn(a, scale=0.5), FadeIn(b, scale=0.5), FadeIn(tb), run_time=1.0)
        bar = mk_bar(a, b, 10)
        self.play(Create(bar), run_time=0.7)
        self.at("other products")
        op = Circle(radius=0.22, fill_color=GREY, fill_opacity=1, stroke_color=TEXT, stroke_width=2).move_to([-3.3, 0.3, 0])
        opl = T("other product", 30, TEXT, weight=BOLD)
        self.add(op)
        self.play(op.animate.move_to([-1.3, 2.4, 0]), run_time=1.0)
        opl.next_to(op, RIGHT, buff=0.2)
        self.play(FadeIn(opl), run_time=0.3)
        self.at("not water")
        v = vee(True, 1.4).move_to([-3.3, 0.9, 0])
        self.play(FadeIn(v, scale=0.5), run_time=0.3)
        self.play(v.animate.move_to(slots[0]), run_time=1.0)
        self.at("bookkeeping")
        cap = T("real steps differ; the atom count holds", 32, YELLOW, weight=BOLD).move_to([-1.0, -2.8, 0])
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.9)
        self.at("Taking apart adds water")
        self.play(FadeOut(VGroup(a, b, bar, op, opl, tb, v, cap)), run_time=0.7)
        top = Arc(radius=1.7, start_angle=PI, angle=-PI, color=WATER, stroke_width=8).add_tip(tip_length=0.3)
        bot = Arc(radius=1.7, start_angle=0, angle=-PI, color=GOLD, stroke_width=8).add_tip(tip_length=0.3)
        tl = T("take apart (add water)", 34, WATER, weight=BOLD).move_to([0, 2.7, 0])
        dot = Dot(radius=0.14, color=YELLOW)
        dot.t = 0.0

        def orb(m, dt):
            m.t += dt * 1.1
            m.move_to([1.7 * np.cos(PI - m.t), 1.7 * np.sin(PI - m.t), 0])
        dot.add_updater(orb)
        self.play(Create(top), FadeIn(tl), FadeIn(dot), run_time=1.8)
        self.at("A built chain is one water short")
        bl = T("build (one water short per link)", 34, GOLD, weight=BOLD).move_to([0, -2.7, 0])
        self.play(Create(bot), FadeIn(bl), run_time=1.8)
        self.finish()


class S12Reuse(SpokenScene):
    def construct(self):
        order = [2, 4, 0, 5, 1, 6, 3]   # bottom row: index into LETTERS
        topc = Chain([amino(LETTERS[i], 0.5).move_to([-4.8 + 1.6 * i, 1.4, 0]) for i in range(7)])
        botc = Chain([amino(LETTERS[order[i]], 0.5).move_to([-4.8 + 1.6 * i, -1.4, 0]) for i in range(7)])
        wig_all(topc.blocks, 0.05)
        wig_all(botc.blocks, 0.05)
        bl = T("your new protein", 32, AMINO, weight=BOLD).move_to([0, -2.6, 0])
        tl = T("turkey protein", 32, AMINO, weight=BOLD).move_to([0, 2.6, 0])
        self.wait(0.1)
        self.play(botc.build(0.25), FadeIn(bl), run_time=2.4)
        self.at("from the turkeys", lead=1.8)
        self.play(topc.build(0.2), FadeIn(tl), run_time=1.8)
        traced = [0, 1, 2]
        arrows = VGroup(*[Arrow(topc.blocks[k].get_center() + DOWN * 0.5, botc.blocks[order.index(k)].get_center() + UP * 0.5,
                                buff=0.05, color=YELLOW, stroke_width=5, tip_length=0.2) for k in traced])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.4), run_time=1.6)
        self.at("does not become")
        self.play(topc.group.animate.set_opacity(0.35), run_time=1.0)
        self.at("Its blocks are reused")
        copies = [topc.blocks[k].copy().set_opacity(1) for k in traced]
        self.add(*copies)
        self.play(topc.group.animate.set_opacity(1.0),
                  *[c.animate.move_to(botc.blocks[order.index(k)].get_center()) for c, k in zip(copies, traced)], run_time=2.0)
        self.play(*[FadeOut(c) for c in copies], *[Indicate(botc.blocks[order.index(k)], color=YELLOW) for k in traced], run_time=1.0)
        self.finish()


class S13Four(SpokenScene):
    def construct(self):
        xs = [-5.1, -1.7, 1.7, 5.1]
        sg = sugar(0.7).move_to([xs[0], 1.7, 0])
        am = amino("", 0.6).move_to([xs[1], 1.7, 0])
        nu = nuc(0.6).move_to([xs[2], 1.7, 0])
        fg, comb, tails = fatty_group(1.2)
        fg.move_to([xs[3], 1.7, 0])
        l_sg = T("simple sugar", 28, GOLD, weight=BOLD).move_to([xs[0], 0.6, 0])
        l_am = T("amino acid", 28, AMINO, weight=BOLD).move_to([xs[1], 0.6, 0])
        l_nu = T("nucleotide", 28, GREEN, weight=BOLD).move_to([xs[2], 0.6, 0])
        l_fa = VGroup(T("fatty acids", 28, ORANGE, weight=BOLD), T("+ glycerol", 28, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.08).move_to([xs[3], 0.5, 0])
        wig_all([sg, am, nu, fg], 0.07)
        boxes = []
        for x, name, c in zip(xs, ["carbohydrates", "proteins", "nucleic acids", "lipids"], [GOLD, AMINO, GREEN, ORANGE]):
            r = RoundedRectangle(corner_radius=0.15, width=3.2, height=1.2, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.1)
            t = T(name, 28, TEXT, weight=BOLD)
            boxes.append(VGroup(r, t).move_to([x, -1.9, 0]))
        self.wait(0.2)
        self.at("simple sugars")
        self.play(FadeIn(sg, shift=DOWN * 0.4), FadeIn(l_sg), run_time=0.9)
        self.at("amino acids")
        self.play(FadeIn(am, shift=DOWN * 0.4), FadeIn(l_am), run_time=0.9)
        self.at("nucleotides")
        self.play(FadeIn(nu, shift=DOWN * 0.4), FadeIn(l_nu), run_time=0.9)
        self.at("fatty acids")
        self.play(FadeIn(tails, shift=DOWN * 0.4), run_time=0.9)
        self.at("glycerol")
        self.play(FadeIn(comb, shift=DOWN * 0.4), FadeIn(l_fa), run_time=0.9)
        self.at("four classes")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.3) for b in boxes], lag_ratio=0.35), run_time=2.4)
        self.at("The text sorts out")
        for b in boxes:
            self.play(Indicate(b, color=YELLOW, scale_factor=1.06), run_time=0.7)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        gut = RoundedRectangle(corner_radius=0.7, width=5.6, height=3.0, stroke_color=GUT, stroke_width=4,
                               fill_color=GUT, fill_opacity=0.2).move_to([-4.0, -0.5, 0])
        gl = T("gut", 28, GUT, weight=BOLD).move_to([-6.0, 0.5, 0])
        cell = cell_mob()
        ch = Chain([sugar(0.5).move_to([-4.0 + (i - 1.5) * 1.4, -0.5, 0]) for i in range(4)], w=10)
        wig_all(ch.blocks, 0.07)
        cn = Counters(3, 0, "waters")
        self.add(cn.rows)
        self.play(FadeIn(gut), FadeIn(gl), FadeIn(cell), ch.build(0.25), run_time=1.8)
        self.at("block by block")
        self.play(Indicate(cell, color=YELLOW, scale_factor=1.02), run_time=1.5)
        self.at("adds one water")
        for j in range(3):
            m = ch.mid(j)
            w = vee(False, 1.4).move_to(m + UP * 1.3)
            self.play(w.animate.move_to(m + UP * 0.05), run_time=0.3)
            self.play(FadeOut(ch.bars[j]), FadeOut(w, scale=0.3), cn.a.animate.set_value(2 - j), cn.b.animate.set_value(j + 1), run_time=0.3)
        pts = [(1.3, 0.9), (4.9, 0.8), (1.6, -1.9), (4.7, -1.8)]
        self.play(*[b.animate.move_to([*pts[i], 0]) for i, b in enumerate(ch.blocks)], run_time=1.6)
        self.at("Counted from its free blocks")
        tb, slots = tally()
        cn.l2 = "waters short"
        self.play(FadeOut(gut), FadeOut(gl), FadeIn(tb), cn.b.animate.set_value(0), run_time=0.9)
        self.at("each new chain")
        self.play(ch.blocks[0].animate.move_to(row_pt(0, 4)), run_time=0.3)
        for j in range(1, 4):
            self.play(ch.blocks[j].animate.move_to(row_pt(j, 4)), run_time=0.3)
            bar = mk_bar(ch.blocks[j - 1], ch.blocks[j], 10)
            m = (ch.blocks[j - 1].get_center() + ch.blocks[j].get_center()) / 2
            v = vee(True, 1.4).move_to(m + UP * 0.9)
            self.play(Create(bar), FadeIn(v, scale=0.5), cn.a.animate.set_value(j), run_time=0.15)
            self.play(v.animate.move_to(slots[j - 1]), cn.b.animate.set_value(j), run_time=0.3)
        self.finish()


class S15End(EndCard):
    LINE = "Each link: one water added to break, one water short when built."
