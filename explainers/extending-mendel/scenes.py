"""Same Boxes, New Labels (chapter 1 of Extending Mendel). One world: a 2x2 grid of equal boxes.
COLOURS: PURPLE purple flower, FRED red flower, PINK pink flower, PALE white flower, YELLOW yellow coat,
BLACKC black coat (white outline), RED = dies. Boxes and genotypes are WHITE (the fixed deal)."""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#F08CB0"
FRED = "#E04656"
PALE = "#D9DCE3"
BLACKC = "#262A34"
GC = np.array([0.0, -0.4, 0.0])
BS = 2.4


def bc(i):
    return GC + np.array([(-1 if i % 2 == 0 else 1) * BS / 2, (1 if i < 2 else -1) * BS / 2, 0])


def bob(m, amp=0.05, f=0.5, ph=0.0):
    m._bt = ph

    def up(mm, dt):
        old = np.sin(2 * np.pi * f * mm._bt) * amp
        mm._bt += dt
        mm.shift(UP * (np.sin(2 * np.pi * f * mm._bt) * amp - old))
    m.add_updater(up)
    return m


def pulse_fill(m, color, lo=0.05, hi=0.35, f=0.6):
    m._pt = 0.0

    def up(mm, dt):
        mm._pt += dt
        mm.set_fill(color, opacity=lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * f * mm._pt)))
    m.add_updater(up)
    return m


class Motes(VGroup):
    pass


class W(SpokenScene):
    """SpokenScene plus a few faint drifting motes so the world never sits dead."""

    def setup(self):
        super().setup()
        import random
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        motes = VGroup()
        for _ in range(16):
            d = Dot(radius=rng.uniform(0.03, 0.06), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.15, 0.3))
            d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
            d.v = (rng.uniform(-0.15, 0.15), rng.uniform(0.1, 0.3))

            def drift(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 4.0:
                    m.shift(DOWN * 8.0)
                if abs(m.get_x()) > 7.2:
                    m.shift(LEFT * 14.4 * np.sign(m.get_x()))
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)


def dot(kind, r=0.17):
    fills = {"yel": (YELLOW, YELLOW), "blk": (BLACKC, TEXT), "A": (BLUE, BLUE), "a": (GOLD, GOLD)}
    fc, sc = fills[kind]
    return Circle(radius=r, stroke_color=sc, stroke_width=3, fill_color=fc, fill_opacity=1)


def token(letter, r=0.3):
    d = dot(letter, r)
    return VGroup(d, T(letter, 30, BG, weight=BOLD).move_to(d))


def flower(color, s=1.0):
    petals = VGroup()
    for k in range(5):
        a = np.pi / 2 + k * 2 * np.pi / 5
        p = Circle(radius=0.28 * s, stroke_width=2, stroke_color=color, fill_color=color, fill_opacity=0.95)
        p.move_to(0.31 * s * np.array([np.cos(a), np.sin(a), 0]))
        petals.add(p)
    return VGroup(petals, Circle(radius=0.14 * s, stroke_width=0, fill_color=BG, fill_opacity=1))


def mouse(kind, s=1.0):
    col, edge = (YELLOW, YELLOW) if kind == "yel" else (BLACKC, TEXT)
    kw = dict(stroke_color=edge, stroke_width=2, fill_color=col, fill_opacity=1)
    body = Ellipse(width=1.3 * s, height=0.8 * s, **kw)
    head = Circle(radius=0.32 * s, **kw).move_to([0.62 * s, 0.12 * s, 0])
    ear = Circle(radius=0.15 * s, **kw).move_to([0.5 * s, 0.44 * s, 0])
    eye = Dot([0.72 * s, 0.18 * s, 0], radius=0.05 * s, color=BG if kind == "yel" else TEXT)
    tail = Line([-0.62 * s, 0, 0], [-1.0 * s, 0.25 * s, 0], stroke_color=edge, stroke_width=3)
    return VGroup(tail, body, head, ear, eye)


def pup(kind, r=0.38):
    col, edge = (YELLOW, YELLOW) if kind == "yel" else (BLACKC, TEXT)
    kw = dict(stroke_color=edge, stroke_width=2, fill_color=col, fill_opacity=1)
    body = Circle(radius=r, **kw)
    e1 = Circle(radius=r * 0.4, **kw).move_to([-r * 0.7, r * 0.8, 0])
    e2 = Circle(radius=r * 0.4, **kw).move_to([r * 0.7, r * 0.8, 0])
    eyes = VGroup(Dot([-r * 0.3, r * 0.1, 0], radius=r * 0.1, color=BG if kind == "yel" else TEXT),
                  Dot([r * 0.3, r * 0.1, 0], radius=r * 0.1, color=BG if kind == "yel" else TEXT))
    return VGroup(e1, e2, body, eyes)


PHEN = {"purple": (PURPLE, None, None), "white": (PALE, None, None), "red": (FRED, None, None),
        "pink": (PINK, None, None), "yellow": (YELLOW, None, None), "black": (TEXT, BLACKC, TEXT),
        "dies": (RED, None, None)}


def pchip(name, size=32):
    col, fill, tcol = PHEN[name]
    lab = T(name, size, tcol or col)
    box = RoundedRectangle(corner_radius=0.14, width=lab.width + 0.4, height=lab.height + 0.4, stroke_color=col,
                           stroke_width=2.5, fill_color=fill or col, fill_opacity=1 if fill else 0.2)
    return VGroup(box, lab.move_to(box))


def chip_at(i, name, size=32):
    return pchip(name, size).move_to(bc(i) + DOWN * 0.6)


def empty_chip(i):
    r = RoundedRectangle(corner_radius=0.14, width=1.9, height=0.8, stroke_color=GREY, stroke_width=2.5)
    return DashedVMobject(r, num_dashes=20).move_to(bc(i) + DOWN * 0.6)


def edge_label(kind, j):
    if kind == "text":
        return T("A" if j == 0 else "a", 44)
    k = "yel" if j == 0 else "blk"
    return VGroup(dot(k, 0.26), T("yellow" if j == 0 else "black", 26, YELLOW if j == 0 else TEXT)).arrange(DOWN, buff=0.08)


class Grid:
    def __init__(self, kind="text", geno=True):
        self.boxes = VGroup(*[Square(BS, stroke_color=TEXT, stroke_width=3).move_to(bc(i)) for i in range(4)])
        self.tops = VGroup(*[edge_label(kind, j).move_to([bc(j)[0], GC[1] + BS + 0.55, 0]) for j in range(2)])
        sx = GC[0] - BS - (0.45 if kind == "text" else 0.62)
        self.sides = VGroup(*[edge_label(kind, j).move_to([sx, bc(2 * j)[1], 0]) for j in range(2)])
        if kind == "text":
            gs = [T(s, 44) for s in ["AA", "Aa", "Aa", "aa"]]
        else:
            pr = [("yel", "yel"), ("yel", "blk"), ("yel", "blk"), ("blk", "blk")]
            gs = [VGroup(dot(a, 0.21), dot(b, 0.21)).arrange(RIGHT, buff=0.15) for a, b in pr]
        self.genos = VGroup(*[g.move_to(bc(i) + UP * 0.7) for i, g in enumerate(gs)])
        self.all = VGroup(self.boxes, self.tops, self.sides, self.genos)


def lock():
    body = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.85, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.3)
    sh = Arc(radius=0.33, start_angle=0, angle=PI, stroke_color=GOLD, stroke_width=7).next_to(body, UP, buff=-0.02)
    return VGroup(sh, body)


# --------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    TITLE = "Same Boxes, New Labels"
    LESSON = "Extending Mendel"


class S01Hook(W):
    def construct(self):
        m1 = mouse("yel", 1.2).move_to([-5.6, 2.0, 0])
        m2 = mouse("yel", 1.2)
        m2.rotate(PI, axis=UP)
        m2.move_to([-2.4, 2.0, 0])
        for k, m in enumerate((m1, m2)):
            bob(m, 0.05, 0.5, k)
        self.play(FadeIn(m1, shift=RIGHT * 0.3), FadeIn(m2, shift=LEFT * 0.3), run_time=1.6)
        counter = T("true-breeding yellow lines: 0", 30, YELLOW).move_to([3.4, 3.3, 0])
        xs = [-3.5, -2.1, -0.7, 0.7, 2.1, 3.5]

        def litter(y, kinds):
            g = VGroup(*[pup(k, 0.5).move_to([x, y, 0]) for x, k in zip(xs, kinds)])
            for i, p in enumerate(g):
                bob(p, 0.04, 0.4, i)
            return g
        self.at("Mate two yellow mice")
        self.play(m1.animate.shift(RIGHT * 0.3), m2.animate.shift(LEFT * 0.3), run_time=1.2)
        self.at("again and again")
        l1 = litter(0.9, ["yel", "yel", "blk", "yel", "blk", "yel"])
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.4) for p in l1], lag_ratio=0.2), run_time=2.2)
        self.at("One litter may be all yellow")
        l2 = litter(-0.6, ["yel"] * 6)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.4) for p in l2], lag_ratio=0.2), run_time=2.0)
        self.at("no yellow line ever stays yellow")
        l3 = litter(-2.1, ["yel", "blk", "yel", "yel", "yel", "blk"])
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.4) for p in l3], lag_ratio=0.15), FadeIn(counter), run_time=2.0)
        self.finish()


class S02Failure(W):
    def construct(self):
        tag = T("Lucien Cuénot, mouse crosses, early 1900s", 28, GREY).move_to([0, 3.2, 0])
        self.play(FadeIn(tag), run_time=1.0)
        q = T("Mendel failed?", 60, TEXT, font=TITLE_FONT).move_to([0, 0.6, 0])
        self.at("failure of Mendel's")
        self.play(Write(q), run_time=1.8)
        self.at("It was not")
        strike = Line(q.get_left() + LEFT * 0.2, q.get_right() + RIGHT * 0.2, color=RED, stroke_width=7).move_to(q)
        self.play(Create(strike), run_time=0.8)
        self.at("clue that inheritance")
        self.play(FadeOut(q), FadeOut(strike), run_time=0.8)
        b1 = RoundedRectangle(corner_radius=0.2, width=10, height=1.5, stroke_color=GOLD, fill_color=GOLD, fill_opacity=0.15).move_to([0, 0.9, 0])
        t1 = T("layer 1: the deal", 40, GOLD).move_to(b1)
        b2 = RoundedRectangle(corner_radius=0.2, width=10, height=1.5, stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.15).move_to([0, -1.0, 0])
        t2 = T("layer 2: the labels", 40, TEAL).move_to(b2)
        self.at("works in two layers")
        self.play(FadeIn(VGroup(b1, t1), shift=LEFT * 1.5), run_time=1.0)
        self.play(FadeIn(VGroup(b2, t2), shift=RIGHT * 1.5), run_time=1.0)
        self.finish()


class S03Deal(W):
    def construct(self):
        head = T("layer 1: the deal", 32, GOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(head), run_time=0.8)

        def cell(x):
            c = Circle(radius=1.3, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.06).move_to([x, 1.0, 0])
            ta = token("A", 0.4).move_to([x - 0.5, 1.0, 0])
            tb = token("a", 0.4).move_to([x + 0.5, 1.0, 0])
            return c, ta, tb
        c1, a1, b1 = cell(-3.6)
        c2, a2, b2 = cell(3.6)
        lab1 = T("parent", 28, GREY).move_to([-3.6, 2.5, 0])
        lab2 = T("parent", 28, GREY).move_to([3.6, 2.5, 0])
        self.play(FadeIn(VGroup(c1, a1, b1, lab1)), FadeIn(VGroup(c2, a2, b2, lab2)), run_time=1.5)
        self.at("At meiosis")
        self.play(Indicate(c1, scale_factor=1.08), Indicate(c2, scale_factor=1.08), run_time=1.2)
        self.at("separate into different gametes")
        g = [Circle(radius=0.7, stroke_color=TEXT, stroke_width=3).move_to(p) for p in
             [[-4.8, -0.9, 0], [-2.6, -0.9, 0], [2.6, -0.9, 0], [4.8, -0.9, 0]]]
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(lab1), FadeOut(lab2),
                  a1.animate.move_to(g[0].get_center()), b1.animate.move_to(g[1].get_center()),
                  a2.animate.move_to(g[2].get_center()), b2.animate.move_to(g[3].get_center()),
                  *[FadeIn(x) for x in g], run_time=2.2)
        child = Circle(radius=1.0, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12).move_to([0, -2.4, 0])
        self.at("each child gets one allele from each parent")
        ar1 = Arrow(g[1].get_bottom(), child.get_left() + UP * 0.35, buff=0.1, color=GREY)
        ar2 = Arrow(g[2].get_bottom(), child.get_right() + UP * 0.35, buff=0.1, color=GREY)
        self.play(FadeIn(child), Create(ar1), Create(ar2), run_time=1.2)
        self.play(b1.animate.move_to(child.get_center() + LEFT * 0.4), a2.animate.move_to(child.get_center() + RIGHT * 0.4), run_time=2.0)
        lc = T("child", 32, GREEN).move_to([2.3, -2.4, 0])
        self.play(FadeIn(lc), run_time=0.6)
        self.finish()


class S04Grid(W):
    def construct(self):
        G = Grid("text", geno=True)
        live(G, 0.1)
        self.at("Cross two parents")
        self.play(Create(G.boxes), run_time=1.8)
        self.play(FadeIn(G.tops), FadeIn(G.sides), run_time=1.2)
        self.at("Each parent passes on")
        halves = VGroup(*[T("1/2", 26, GOLD).next_to(G.tops[j], RIGHT, buff=0.12) for j in range(2)],
                        *[T("1/2", 26, GOLD).next_to(G.sides[j], LEFT, buff=0.12) for j in range(2)])
        self.play(LaggedStart(*[FadeIn(h, scale=1.2) for h in halves], lag_ratio=0.25), run_time=1.8)
        self.at("gametes meet at random")
        tag = T("fair deal: equal transmission, random meeting", 26, TEAL).move_to([0, -3.4, 0])
        self.play(FadeIn(tag), run_time=1.0)
        self.at("pairings fill four equally likely boxes")
        for b in G.boxes:
            b.set_fill(TEXT, opacity=0.0)
        self.play(LaggedStart(*[b.animate.set_fill(TEXT, opacity=0.12) for b in G.boxes], lag_ratio=0.3), run_time=1.8)
        self.at("One box gets two of the first allele")
        self.play(FadeIn(G.genos[0], scale=1.2), run_time=0.6)
        self.at("Two boxes get one of each")
        self.play(FadeIn(G.genos[1], scale=1.2), FadeIn(G.genos[2], scale=1.2), run_time=0.7)
        self.at("One box gets two of the second")
        self.play(FadeIn(G.genos[3], scale=1.2), run_time=0.6)
        ratio = M("1 : 2 : 1", 52, GOLD).move_to([4.6, -0.5, 0])
        self.play(FadeIn(ratio, shift=LEFT * 0.3), run_time=0.8)
        self.finish()


def live(G, base=0.12):
    for i, b in enumerate(G.boxes):
        b._pt = i * 1.3
        def up(mm, dt, base=base):
            mm._pt += dt
            if mm.get_fill_opacity() < 0.5 and mm.get_stroke_opacity() > 0:
                mm.set_fill(TEXT, opacity=base * (0.4 + 1.2 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.45 * mm._pt))))
        b.add_updater(up)
    for k, g in enumerate(list(G.genos) + list(G.tops) + list(G.sides)):
        bob(g, 0.05, 0.4, k * 0.37)


def bring_grid(sc, kind="text"):
    G = Grid(kind)
    for b in G.boxes:
        b.set_fill(TEXT, opacity=0.12)
    sc.add(G.all)
    live(G)
    return G


class S05Layer2(W):
    def construct(self):
        G = bring_grid(self)
        self.at("That deal is the part")
        lk = lock().move_to([4.7, 0.9, 0])
        lt = T("deal: fixed", 32, GOLD).move_to([4.7, -0.1, 0])
        self.play(FadeIn(lk, scale=0.6), FadeIn(lt), run_time=1.2)
        self.at("What changes is the label")
        chips = [empty_chip(i) for i in range(4)]
        for i, c in enumerate(chips):
            bob(c, 0.06, 0.6, i)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in chips], lag_ratio=0.2), run_time=1.5)
        self.finish()


class S06Peas(W):
    def construct(self):
        G = bring_grid(self)
        fl = flower(PURPLE, 2.0).move_to([-4.7, 0.3, 0])
        bob(fl, 0.08, 0.4)
        self.play(FadeIn(fl, scale=0.7), run_time=1.5)
        self.at("one purple allele is enough")
        c1 = chip_at(1, "purple")
        self.play(FadeIn(c1, scale=1.2), run_time=0.8)
        self.at("as purple as a plant with two")
        c0, c2 = chip_at(0, "purple"), chip_at(2, "purple")
        self.play(FadeIn(c0, scale=1.2), FadeIn(c2, scale=1.2), run_time=1.0)
        self.at("three boxes share one label")
        c3 = chip_at(3, "white")
        a, b = bc(0), bc(3)
        h = BS / 2 - 0.08
        L = Polygon([a[0] - h, a[1] + h, 0], [bc(1)[0] + h, a[1] + h, 0], [bc(1)[0] + h, GC[1] - 0.0, 0],
                    [GC[0], GC[1], 0], [GC[0], b[1] - h, 0], [a[0] - h, b[1] - h, 0], stroke_color=PURPLE, stroke_width=6)
        self.play(FadeIn(c3, scale=1.2), Create(L), run_time=2.0)
        lab = T("purple", 36, PURPLE).move_to([4.7, 0.7, 0])
        self.at("Mendel's familiar ratio")
        r = M("3 : 1", 52, GOLD).move_to([4.7, -0.5, 0])
        self.play(FadeIn(lab), FadeIn(r, shift=LEFT * 0.3), run_time=1.0)
        self.finish()


class S07Snap(W):
    def construct(self):
        G = bring_grid(self)
        red = flower(FRED, 1.5).move_to([-5.9, 2.3, 0])
        wh = flower(PALE, 1.5).move_to([-3.5, 2.3, 0])
        x = T("×", 44, GREY).move_to([-4.7, 2.3, 0])
        pk = flower(PINK, 1.5).move_to([-4.7, -0.7, 0])
        for k, f in enumerate((red, wh, pk)):
            bob(f, 0.06, 0.4, k)
        self.at("Cross red with white")
        self.play(FadeIn(red, shift=RIGHT * 0.3), FadeIn(wh, shift=LEFT * 0.3), FadeIn(x), run_time=1.6)
        self.at("every child is pink")
        ar = Arrow([-4.7, 1.3, 0], [-4.7, 0.45, 0], buff=0, color=GREY)
        lab = T("every F1 plant", 28, PINK).move_to([-4.7, -2.1, 0])
        self.play(Create(ar), FadeIn(pk, shift=DOWN * 0.3), FadeIn(lab), run_time=1.6)
        self.at("one red allele gives only a pink flower")
        for i in (1, 2):
            G.boxes[i].clear_updaters()
            G.boxes[i].set_fill(PINK, opacity=0.12)
        self.play(*[G.boxes[i].animate.set_fill(PINK, opacity=0.35) for i in (1, 2)], Indicate(pk, scale_factor=1.15, color=PINK), run_time=1.6)
        self.finish()


class S08Snap2(W):
    def construct(self):
        G = bring_grid(self)
        pk = flower(PINK, 1.8).move_to([-4.5, 0.2, 0])
        bob(pk, 0.06, 0.4)
        self.add(pk)
        self.at("pink plants pollinate themselves")
        sa = CurvedArrow(pk.get_top() + LEFT * 0.5 + UP * 0.1, pk.get_top() + RIGHT * 0.5 + UP * 0.1, angle=-PI * 0.9, color=PINK)
        self.play(Create(sa), run_time=1.4)
        self.at("Red and white come back")
        cr, cw = chip_at(0, "red"), chip_at(3, "white")
        self.play(FadeIn(cr, scale=1.2), FadeIn(cw, scale=1.2), run_time=1.0)
        self.at("Each box keeps its own label")
        cp1, cp2 = chip_at(1, "pink"), chip_at(2, "pink")
        self.play(FadeIn(cp1, scale=1.2), FadeIn(cp2, scale=1.2), run_time=1.0)
        rs = VGroup(T("1 red", 34, FRED), T("2 pink", 34, PINK), T("1 white", 34, PALE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.8, -0.3, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rs], lag_ratio=0.3), run_time=1.5)
        self.at("Nothing blended")
        bl = T("blending", 36, GREY).move_to([-4.5, -2.4, 0])
        st = Line(bl.get_left() + LEFT * 0.1, bl.get_right() + RIGHT * 0.1, color=RED, stroke_width=6).move_to(bl)
        self.play(FadeIn(bl), run_time=0.5)
        self.play(Create(st), run_time=0.6)
        self.play(FadeOut(bl), FadeOut(st), run_time=0.8)
        self.finish()


class S09Mouse(W):
    def construct(self):
        G = Grid("text")
        for b in G.boxes:
            b.set_fill(TEXT, opacity=0.12)
        self.add(G.all)
        live(G)
        self.at("Now the yellow mouse")
        M2 = Grid("dots")
        self.play(FadeOut(G.tops), FadeOut(G.sides), FadeOut(G.genos), run_time=0.7)
        self.play(FadeIn(M2.tops), FadeIn(M2.sides), FadeIn(M2.genos), run_time=1.0)
        m1 = mouse("yel", 1.3).move_to([-4.9, 1.1, 0])
        m2 = mouse("yel", 1.3).move_to([-4.9, -1.4, 0])
        bob(m1, 0.06, 0.5, 0), bob(m2, 0.06, 0.5, 1)
        self.play(FadeIn(m1, shift=RIGHT * 0.3), run_time=1.0)
        self.at("One yellow allele is enough")
        c1 = chip_at(1, "yellow")
        self.play(FadeIn(c1, scale=1.2), run_time=0.8)
        self.at("Mate two yellow mice")
        self.play(FadeIn(m2, shift=RIGHT * 0.3), run_time=1.0)
        self.at("same four boxes appear")
        c2, c3 = chip_at(2, "yellow"), chip_at(3, "black")
        pulse_fill(G.boxes[0], YELLOW, 0.08, 0.35, 0.5)
        self.play(FadeIn(c2, scale=1.2), FadeIn(c3, scale=1.2), run_time=1.2)
        self.finish()


def mouse_world(sc, chips=("yellow", "yellow", "black"), glow=True, dead=False):
    G = Grid("dots")
    for b in G.boxes:
        b.set_fill(TEXT, opacity=0.12)
    m1 = mouse("yel", 1.3).move_to([-4.9, 1.1, 0])
    m2 = mouse("yel", 1.3).move_to([-4.9, -1.4, 0])
    bob(m1, 0.06, 0.5, 0), bob(m2, 0.06, 0.5, 1)
    cs = [chip_at(1, chips[0]), chip_at(2, chips[1]), chip_at(3, chips[2])]
    sc.add(G.all, m1, m2, *cs)
    live(G)
    for k, c in enumerate(cs):
        bob(c, 0.04, 0.5, k)
    if glow:
        pulse_fill(G.boxes[0], YELLOW, 0.08, 0.35, 0.5)
    return G, m1, m2, cs


def card():
    t = VGroup(T("Two yellow alleles:", 28, GOLD), T("what label?", 28, GOLD)).arrange(DOWN, buff=0.15)
    r = RoundedRectangle(corner_radius=0.2, width=t.width + 0.6, height=t.height + 0.6, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.1)
    return VGroup(r, t.move_to(r)).move_to([4.7, 0.2, 0])


class S10Predict(W):
    def construct(self):
        mouse_world(self)
        cd = card()
        self.at("what label goes in the box")
        self.play(FadeIn(cd, shift=LEFT * 0.3), run_time=1.0)
        self.finish()


class S11Pause(W):
    def construct(self):
        mouse_world(self)
        cd = card()
        self.add(cd)
        ring = Circle(radius=0.4, stroke_color=GOLD, stroke_width=7).move_to([6.0, -3.1, 0])
        self.add(ring)
        self.play(Uncreate(ring), run_time=4.7, rate_func=linear)
        self.finish()


class S12Reveal(W):
    def construct(self):
        G, m1, m2, cs = mouse_world(self)
        cd = card()
        self.add(cd)
        self.at("That label is death")
        dies = chip_at(0, "dies")
        G.boxes[0].clear_updaters()
        self.play(FadeOut(cd), FadeIn(dies, scale=1.3), run_time=1.0)
        self.at("Two copies of the yellow allele")
        self.play(Indicate(G.genos[0], color=RED, scale_factor=1.25), run_time=1.4)
        self.at("very early before implantation")
        note = VGroup(T("very early:", 32, RED), T("before implantation", 32, RED)).arrange(DOWN, buff=0.12).move_to([4.7, 0.3, 0])
        self.play(FadeIn(note, shift=LEFT * 0.3), run_time=1.2)
        self.at("that box goes dark")
        dash = DashedVMobject(Square(BS, stroke_color=RED, stroke_width=3), num_dashes=24).move_to(bc(0))
        self.play(G.boxes[0].animate.set_fill(BG, opacity=0.9).set_stroke(opacity=0), FadeIn(dash),
                  dies.animate.set_opacity(0.45), G.genos[0].animate.set_opacity(0.3), FadeOut(note), run_time=2.0)
        self.finish()


def dead_world(sc):
    G, m1, m2, cs = mouse_world(sc, glow=False)
    dies = chip_at(0, "dies").set_opacity(0.45)
    G.boxes[0].set_fill(BG, opacity=0.9).set_stroke(opacity=0)
    G.genos[0].set_opacity(0.3)
    dash = DashedVMobject(Square(BS, stroke_color=RED, stroke_width=3), num_dashes=24).move_to(bc(0))
    sc.add(dies, dash)
    return G, m1, m2, cs


class S13Ratio(W):
    def construct(self):
        G, m1, m2, cs = dead_world(self)
        self.at("yellow outnumbers black")
        r1 = M("2 yellow : 1 black", 26, YELLOW).move_to([4.7, 1.2, 0])
        r2 = T("(among live pups)", 26, GREY).move_to([4.7, 0.55, 0])
        self.play(FadeIn(r1, shift=LEFT * 0.3), FadeIn(r2), run_time=1.2)
        self.at("every yellow pup is a heterozygote")
        for i in (1, 2):
            G.boxes[i].set_stroke(YELLOW, width=6)
        self.play(*[Indicate(G.boxes[i], color=YELLOW, scale_factor=1.05) for i in (1, 2)], run_time=1.4)
        pair = VGroup(dot("yel", 0.2), dot("blk", 0.2)).arrange(RIGHT, buff=0.2).move_to([4.6, -0.5, 0])
        het = T("heterozygote", 34, YELLOW).move_to([4.6, -1.2, 0])
        self.at("one yellow allele and one other")
        self.play(FadeIn(pair, scale=1.3), FadeIn(het), run_time=1.2)
        self.finish()


class S14Why(W):
    def construct(self):
        G, m1, m2, cs = dead_world(self)
        for i in (1, 2):
            G.boxes[i].set_stroke(YELLOW, width=6)
        self.at("no yellow mouse breeds true")
        ps = [pup("yel", 0.3).move_to([-3.2, -3.35, 0]), pup("yel", 0.3).move_to([-1.2, -3.35, 0]), pup("blk", 0.3).move_to([1.2, -3.35, 0])]
        for k, p in enumerate(ps):
            bob(p, 0.04, 0.4, k)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.3) for p in ps], lag_ratio=0.3), run_time=1.6)
        self.at("no yellow allele at all")
        ln = Line(ps[2].get_top() + UP * 0.05, bc(3) + DOWN * 1.2, color=TEXT, stroke_width=3)
        self.play(Create(ln), Indicate(G.boxes[3], color=TEXT, scale_factor=1.06), run_time=1.4)
        self.finish()


def sgrid(cx, cols, dead=False):
    s = 1.6
    boxes = VGroup()
    for i, c in enumerate(cols):
        x = cx + (-1 if i % 2 == 0 else 1) * s / 2
        y = -0.4 + (1 if i < 2 else -1) * s / 2
        sq = Square(s, stroke_color=TEXT, stroke_width=3, fill_color=c, fill_opacity=0.9).move_to([x, y, 0])
        if c == BLACKC:
            sq.set_fill(BLACKC, opacity=1)
        boxes.add(sq)
    if dead:
        boxes[0].set_fill(BG, opacity=0.9).set_stroke(opacity=0)
        boxes.add(DashedVMobject(Square(s, stroke_color=RED, stroke_width=3), num_dashes=20).move_to(boxes[0]))
    return boxes


def three_grids():
    gs = (sgrid(-4.2, [PURPLE, PURPLE, PURPLE, PALE]), sgrid(0, [FRED, PINK, PINK, PALE]),
            sgrid(4.2, [YELLOW, YELLOW, YELLOW, BLACKC], dead=True))
    for k, g in enumerate(gs):
        bob(g, 0.06, 0.4, k * 0.9)
    return gs


class S15Rule(W):
    def construct(self):
        gs = three_grids()
        self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in gs], lag_ratio=0.5), run_time=2.6)
        self.at("Inheritance deals the boxes")
        l1 = T("Inheritance deals the boxes.", 38).move_to([0, 3.0, 0])
        self.play(FadeIn(l1, shift=DOWN * 0.2), run_time=1.0)
        self.at("product does writes the labels")
        l2 = T("The gene products write the labels.", 38, TEAL).move_to([0, 2.3, 0])
        self.play(FadeIn(l2, shift=DOWN * 0.2), run_time=1.0)
        self.at("share a label")
        u1 = T("share a label", 28, PURPLE).move_to([-4.2, -2.55, 0])
        self.play(FadeIn(u1), Indicate(gs[0], scale_factor=1.05), run_time=1.0)
        self.at("keep their own")
        u2 = T("keep their own", 28, PINK).move_to([0, -2.55, 0])
        self.play(FadeIn(u2), Indicate(gs[1], scale_factor=1.05), run_time=1.0)
        self.at("one can be")
        u3 = T("dies: dropped", 28, RED).move_to([4.2, -2.55, 0])
        self.play(FadeIn(u3), Indicate(gs[2], scale_factor=1.05), run_time=1.0)
        self.finish()


class S16Scope(W):
    def construct(self):
        gs = three_grids()
        self.add(*gs)
        tag = T("scope: fair deal, unlinked genes, one label per box", 28, TEAL).move_to([0, 2.7, 0])
        fr = Rectangle(width=12.7, height=4.6, stroke_color=TEXT, stroke_width=3).move_to([0, -0.4, 0])
        self.at("This holds while the deal is fair")
        self.play(Create(fr), FadeIn(tag), run_time=4.0)
        self.at("gives only a chance of a trait")
        dl = DashedLine(fr.get_corner(DL), fr.get_corner(DR), color=GREY, stroke_width=4, dash_length=0.12)
        t1 = T("where the rule stops:", 28, GREY).move_to([0, -3.0, 0])
        t2 = T("a box with only a chance of a label", 28, GREY).move_to([0, -3.5, 0])
        self.play(Create(dl), FadeIn(t1), run_time=1.5)
        self.play(FadeIn(t2), run_time=1.0)
        self.finish()


class S17End(EndCard):
    LINE = "Inheritance deals the boxes; the gene products write the labels."
