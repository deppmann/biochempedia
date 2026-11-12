"""Why Does a Strawberry Swell?  (plant-reproduction, film 2 of the lesson)

COLOR MAP (same as film 1)
  MAGENTA blocks = maternal chromosome sets      TEAL blocks = paternal sets
  GREEN = embryo      CREAM = endosperm      BROWN = seed coat
  ORANGE = fruit wall / achene wall          PALE YELLOW = pollen
  GOLD = auxin paste      light grey = signal arrows      TEXT = plain labels
All plant drawings are flat schematic cartoons; sets are blocks, never molecules.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

MAG = "#E040C8"
PAT = TEAL
EMBC = GREEN
ENDC = "#E9D9A0"
COATC = "#A9744A"
FRUITC = "#F29E4C"
POLC = "#F7EC9A"
FLESH = "#E5484D"
YOUNGC = "#D5E5BD"
SIG = "#D5DAE4"
KX, KY = -2.4, -0.1


def P(x, y):
    return np.array([x, y, 0.0])


def blk(color, w=0.9, h=0.36):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2,
                            fill_color=color, fill_opacity=0.9)


def stack(cols, w=0.9, h=0.36, gap=0.07, empty=0):
    g = VGroup(*[blk(c, w, h) for c in cols])
    for _ in range(empty):
        g.add(DashedVMobject(RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=PAT, stroke_width=2.5), num_dashes=16))
    g.arrange(UP, buff=gap)
    return g


def legend():
    a = VGroup(blk(MAG, 0.5, 0.26), T("mother", 26, MAG)).arrange(RIGHT, buff=0.15)
    b = VGroup(blk(PAT, 0.5, 0.26), T("father", 26, PAT)).arrange(RIGHT, buff=0.15)
    g = VGroup(a, b).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    g.to_corner(UR, buff=0.3)
    return g


def motes(center, rx, ry, n=6, color=PAT, seed=1, size=0.05, op=0.55):
    rng = np.random.default_rng(seed)
    g = VGroup(*[Dot(radius=size, color=color).set_opacity(op) for _ in range(n)])
    ph = rng.uniform(0, 6.3, (n, 4))
    sp = rng.uniform(0.4, 0.9, (n, 2))
    g.t = 0.0

    def up(m, dt):
        m.t += dt
        for i, d in enumerate(m):
            d.move_to(center + P(rx * np.sin(sp[i, 0] * m.t + ph[i, 0]), ry * np.sin(sp[i, 1] * m.t + ph[i, 1])))
    g.add_updater(up)
    up(g, 0)
    return g


def amb(seed=1):
    return motes(P(0, 0), 6.2, 3.3, n=14, color=GREY, seed=seed, size=0.045, op=0.35)


def bob(m, amp=0.06, per=2.2, ph=0.0):
    base = m.get_center().copy()
    st = [ph]

    def up(mm, dt):
        st[0] += dt
        mm.move_to(base + P(amp * np.sin(6.283 * st[0] / per), amp * np.cos(6.283 * st[0] / (per * 1.3))))
    m.add_updater(up)
    return m


def lab(text, color=TEXT, size=30, **kw):
    return T(text, size, color, **kw)


def leader(a, b, color=GREY):
    return Line(a, b, color=color, stroke_width=2.5).set_opacity(0.9)


def schem():
    return lab("schematic", TEXT, 22).move_to(P(6.0, -3.55)).set_opacity(0.7)


class W(SpokenScene):
    def cue(self, phrase, *anims, rt=0.8, nth=0, lead=0.2):
        self.at(phrase, lead=lead, nth=nth)
        if anims:
            self.play(*anims, run_time=rt)

    def fill(self, phrase, *anims, nth=0, lead=0.2):
        rt = self.t_of(phrase, nth) - lead - self.elapsed()
        if anims:
            self.play(*anims, run_time=max(rt, 0.3))
        elif rt > 0.02:
            self.wait(rt)

    def hold(self, grp, f=1.035):
        rest = self.narration_s - self.elapsed()
        if rest > 0.5:
            self.play(grp.animate.scale(f), run_time=rest, rate_func=linear)


# ---------------------------------------------------------------------------------------------
# shared drawings
# ---------------------------------------------------------------------------------------------
def outline(w, h, t):
    c, s = np.cos(t), np.sin(t)
    return np.array([0.5 * w * s * (0.6 + 0.4 * (1 + c) / 2), 0.5 * h * c, 0.0])


def berry(c, w, h, fill, ach=True, skip=None):
    """A flat strawberry / receptacle cartoon: VGroup(body, glow layer, achenes)."""
    body = ParametricFunction(lambda t: c + outline(w, h, t), t_range=[0, TAU], stroke_color=fill,
                              stroke_width=3, fill_color=fill, fill_opacity=1)
    glow = body.copy().set_fill(opacity=0).set_stroke(opacity=0)
    achs = VGroup()
    if ach:
        k = w / 2.6
        for kk, n in ((0.82, 14), (0.55, 9), (0.28, 4)):
            for t in np.linspace(0.3, TAU - 0.3, n):
                p = c + kk * outline(w, h, t)
                if skip is not None:
                    sc, rx, ry = skip
                    if ((p[0] - sc[0]) / rx) ** 2 + ((p[1] - sc[1]) / ry) ** 2 < 1:
                        continue
                achs.add(Ellipse(width=0.11 * k, height=0.16 * k, stroke_color="#FFE9B0", stroke_width=1.5,
                                 fill_color=FRUITC, fill_opacity=1).move_to(p))
    return VGroup(body, glow, achs)


def swell(m, about, f=1.45, fill=FLESH):
    t = m.copy()
    t.scale(f, about_point=about)
    t[0].set_fill(fill).set_stroke(fill)
    return Transform(m, t)


RX = [-4.3, 0.0, 4.3]
RW, RH = 2.2, 2.55
RYC = -0.9
RBOT = RYC - RH / 2
GYC = RBOT + RH * 1.45 / 2


def young(i, ach=True):
    return berry(P(RX[i], RYC), RW, RH, YOUNGC, ach)


def grown(i, ach=True):
    return berry(P(RX[i], GYC), RW * 1.45, RH * 1.45, FLESH, ach)


def bottom(i):
    return P(RX[i], RBOT)


def bench():
    return Line(P(-6.4, -2.25), P(6.4, -2.25), color=GREY, stroke_width=6)


def kernel(c=P(KX, KY), w=4.6, h=6.0):
    fw = RoundedRectangle(corner_radius=1.9, width=w, height=h, stroke_width=0, fill_color=FRUITC, fill_opacity=1)
    co = RoundedRectangle(corner_radius=1.75, width=w - 0.3, height=h - 0.3, stroke_width=0, fill_color=COATC, fill_opacity=1)
    en = RoundedRectangle(corner_radius=1.6, width=w - 0.6, height=h - 0.6, stroke_width=0, fill_color=ENDC, fill_opacity=0.95)
    g = VGroup(fw, co, en).move_to(c)
    em = Ellipse(width=1.3, height=1.9, stroke_width=0, fill_color=EMBC, fill_opacity=1).rotate(-0.25).move_to(c + P(0.7, 0.9))
    g.add(em)
    return g


LSPEC = [([MAG, PAT], 0, "embryo", EMBC, "1 + 1", 1.9),
         ([MAG, MAG, PAT], 0, "endosperm", ENDC, "2 + 1", 0.1),
         ([MAG, MAG], 1, "coat and fruit wall", FRUITC, "2 + 0", -1.9)]


def ledger_group():
    K = kernel()
    K[3].move_to(P(KX + 0.7, KY + 1.0))
    rows = []
    tgts = [K[3].get_center() + P(0.3, 0.0), P(KX + 0.5, KY - 0.8), P(KX + 2.28, KY - 1.0)]
    for (cols, em, name, col, num, y), tg in zip(LSPEC, tgts):
        s = stack(cols, 0.8, 0.32, 0.06, empty=em).move_to(P(2.5, y))
        t = VGroup(lab(name, col, 28), T(num, 32, TEXT, font=MONO)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(s, RIGHT, buff=0.35)
        rows.append(VGroup(leader(tg, s.get_left() + LEFT * 0.1), s, t))
    return K, rows


MINI_C = P(-5.85, 2.95)


def mini_ledger():
    K = kernel()
    K[3].move_to(P(KX + 0.7, KY + 1.0))
    sts = [stack(c, 0.8, 0.32, 0.06, empty=e).move_to(P(2.5, y)) for c, e, _, _, _, y in LSPEC]
    g = VGroup(K, *sts)
    g.scale(0.26).move_to(MINI_C)
    return g


def tomato(c):
    body = Circle(radius=1.9, stroke_color="#D9822E", stroke_width=5, fill_color=FRUITC, fill_opacity=0.95).move_to(c)
    pk = VGroup(*[Ellipse(width=0.75, height=0.9, stroke_width=0, fill_color="#FFD9A8", fill_opacity=0.95)
                  .move_to(c + P(1.1 * np.cos(a), 1.1 * np.sin(a))) for a in (PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3)])
    stem = Line(c + P(0, 1.9), c + P(0, 2.3), color=GREY, stroke_width=7)
    return VGroup(body, pk, stem)


def idea_card():
    bub = RoundedRectangle(corner_radius=0.5, width=11.2, height=1.9, stroke_color=TEXT, stroke_width=3).set_stroke(opacity=0.6).move_to(P(0.9, 2.8))
    p = lab("pollination", POLC, 34).move_to(P(-2.6, 3.2))
    arr = Arrow(P(-1.0, 3.2), P(0.8, 3.2), color=TEXT, buff=0, stroke_width=6)
    r = lab("receptacle grows", TEXT, 34).move_to(P(3.3, 3.2))
    return VGroup(bub, p, arr, r)


def cross_at(pt):
    return VGroup(Line(pt + P(-0.35, 0.35), pt + P(0.35, -0.35)), Line(pt + P(-0.35, -0.35), pt + P(0.35, 0.35))).set_stroke(RED, 9)


def tweezers():
    return VGroup(Line(P(-0.12, 0), P(-0.45, 1.7)), Line(P(0.12, 0), P(0.45, 1.7))).set_stroke("#D0D5DD", 6)


def question_card():
    box = RoundedRectangle(corner_radius=0.3, width=9.8, height=1.1, stroke_color=GOLD, stroke_width=4, fill_color=BG, fill_opacity=0.9)
    q = lab("Stripped receptacle: grow or not?", TEXT, 38)
    return VGroup(box, q).move_to(P(0.9, 2.95))


def row_labels(texts, ys=(-2.8, -3.35)):
    out = VGroup()
    for i, (a, b) in enumerate(texts):
        out.add(VGroup(lab(a, TEXT, 28).move_to(P(RX[i], ys[0])), lab(b, TEXT, 34, weight=BOLD).move_to(P(RX[i], ys[1]))))
    return out


def sig_arrows_in(m, step=3):
    c = m[0].get_center()
    out = VGroup()
    for a in list(m[2])[::step]:
        p = a.get_center()
        out.add(Arrow(p, p + (c - p) * 0.45, color=SIG, buff=0, stroke_width=5, tip_length=0.16, max_tip_length_to_length_ratio=0.5))
    return out


def sig_arrows_edge(c, w, h, n=9):
    out = VGroup()
    for t in np.linspace(0.5, TAU - 0.5, n):
        p = c + 0.97 * outline(w, h, t)
        cc = c
        out.add(Arrow(p, p + (cc - p) * 0.28, color=SIG, buff=0, stroke_width=5, tip_length=0.16, max_tip_length_to_length_ratio=0.5))
    return out


def paste_tint(m):
    m[1].set_fill(GOLD, 0.4).set_stroke(GOLD, 5, 1)
    return m


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Double Fertilization: How a Flower Makes a Seed"
    TITLE = "Why Does a Strawberry Swell?"


# ---------------------------------------------------------------------------------------------
class S01Hook(W):
    def construct(self):
        self.add(amb(1))
        lg = legend()
        self.add(lg)
        c = P(-3.0, 0.2)
        b = berry(c, 4.2, 4.8, FLESH, ach=False)
        inner = ParametricFunction(lambda t: c + 0.8 * outline(4.2, 4.8, t), t_range=[0, TAU], stroke_width=0,
                                   fill_color="#F0868A", fill_opacity=1)
        core = Ellipse(width=1.0, height=1.3, stroke_width=0, fill_color="#FBE3D6", fill_opacity=1).move_to(c + P(0, 0.85))
        pits = VGroup(*[Ellipse(width=0.1, height=0.15, stroke_width=0, fill_color=FRUITC, fill_opacity=1)
                        .move_to(c + 0.93 * outline(4.2, 4.8, t)) for t in np.linspace(0.3, TAU - 0.3, 16)])
        half = VGroup(b, inner, core, pits)
        self.play(FadeIn(half, scale=0.9), run_time=1.0)
        st = stack([MAG, MAG], 1.0, 0.32, empty=1).move_to(c + P(0, -0.7))
        l1 = lab("mother's tissue", MAG, 30).move_to(P(-3.0, -2.85))
        l2 = lab("no father's set", PAT, 30).move_to(P(-3.0, -3.4))
        self.cue("red flesh", Indicate(b[0], color=WHITE, scale_factor=1.03), rt=1.0)
        self.cue("mother's own", FadeIn(st[:2]), FadeIn(l1), rt=0.9)
        self.cue("no chromosomes", FadeIn(st[2], scale=1.3), rt=0.7)
        self.cue("from the father", FadeIn(l2), Indicate(st[2], color=PAT, scale_factor=1.3), rt=0.9)
        fx, fy = 3.5, 0.6
        petals = VGroup(*[Ellipse(width=1.0, height=1.7, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.45)
                          .rotate(a - PI / 2).move_to(P(fx + 1.15 * np.cos(a), fy + 1.15 * np.sin(a)))
                          for a in np.linspace(PI / 2, PI / 2 + TAU, 5, endpoint=False)])
        stem = Line(P(fx, fy - 0.8), P(fx, -2.2), color=GREY, stroke_width=8)
        tip = Circle(radius=0.38, stroke_color="#A9BC84", stroke_width=3, fill_color=YOUNGC, fill_opacity=1).move_to(P(fx, fy))
        flower = VGroup(stem, petals, tip)
        self.cue("so why", FadeIn(flower, scale=0.8), rt=1.0)
        fl = VGroup(lab("not pollinated:", TEXT, 30), lab("no swelling", TEXT, 30)).arrange(DOWN, buff=0.12).move_to(P(fx, -2.9))
        self.cue("swell", half.animate.scale(1.05), rt=0.7)
        self.cue("only after", FadeIn(fl), half.animate.scale(1 / 1.05), rt=0.7)
        grains = VGroup(*[Circle(radius=0.14, stroke_color=POLC, stroke_width=2, fill_color=POLC, fill_opacity=0.9)
                          .move_to(P(fx - 1.6 + 0.8 * i, 2.6 - 0.2 * i)) for i in range(3)])
        q = lab("?", TEXT, 60, weight=BOLD).move_to(P(fx, 2.15))
        self.cue("pollinated", FadeIn(grains), FadeIn(q, scale=1.5), rt=0.6)
        self.play(*[g.animate.move_to(P(fx + 0.2 * (i - 1), fy + 0.2)) for i, g in enumerate(grains)], run_time=1.0)
        bob(q, 0.05)
        self.add(q)
        self.hold(VGroup(half, flower, fl))
        self.finish()


class S02Link(W):
    def construct(self):
        self.add(amb(2))
        lg = legend()
        self.add(lg)
        K, rows = ledger_group()
        self.cue("first film", FadeIn(K, scale=0.95), rt=1.0)
        self.cue("counted", FadeIn(rows[0], shift=LEFT * 0.2), Indicate(K[3], color=WHITE, scale_factor=1.15), rt=1.0)
        self.cue("sets in", FadeIn(rows[1], shift=LEFT * 0.2), Indicate(K[2], color=WHITE, scale_factor=1.02), rt=1.0)
        self.cue("seed coat", FadeIn(rows[2], shift=LEFT * 0.2), Indicate(K[0], color=WHITE, scale_factor=1.02), rt=1.0)
        self.cue("mother's tissue", Indicate(rows[2][1], color=MAG, scale_factor=1.15), rt=1.2)
        mini = mini_ledger()
        self.cue("this film asks", ReplacementTransform(K, mini[0]),
                 *[ReplacementTransform(rows[i][1], mini[i + 1]) for i in range(3)],
                 *[FadeOut(rows[i][0]) for i in range(3)], *[FadeOut(rows[i][2]) for i in range(3)], rt=1.4)
        q = lab("what tells her tissue to grow?", TEXT, 46)
        self.cue("tells her tissue", FadeIn(q, shift=UP * 0.2), rt=1.0)
        self.hold(q, 1.06)
        self.finish()


class S03Fruit(W):
    def construct(self):
        self.add(amb(3), mini_ledger(), schem())
        oc = P(-2.6, -0.3)
        ovary = Ellipse(width=4.4, height=5.6, stroke_color=FRUITC, stroke_width=8, fill_color=FRUITC, fill_opacity=0.15).move_to(oc)
        ovule = Ellipse(width=2.0, height=2.8, stroke_color=COATC, stroke_width=8, fill_color=COATC, fill_opacity=0.2).move_to(oc)
        endo = Ellipse(width=1.2, height=1.9, stroke_width=0, fill_color=ENDC, fill_opacity=0.95).move_to(oc + P(-0.1, -0.2))
        emb = Ellipse(width=0.6, height=0.85, stroke_width=0, fill_color=EMBC, fill_opacity=1).rotate(-0.3).move_to(oc + P(0.15, 0.35))
        self.play(FadeIn(ovary, scale=0.9), FadeIn(ovule, scale=0.8), run_time=1.2)
        self.cue("general rule", Indicate(ovule, color=WHITE, scale_factor=1.05), rt=1.0)
        top = lab("after fertilization", TEXT, 34).move_to(P(2.6, 3.2))
        self.cue("after fertilization", FadeIn(top), rt=0.7)
        l1 = lab("ovule → seed", TEXT, 36).move_to(P(3.5, 1.0))
        ld1 = leader(P(1.6, 1.0), oc + P(0.9, 0.5))
        self.cue("the ovule", FadeIn(l1), Create(ld1), Indicate(ovule, color=WHITE, scale_factor=1.06), rt=1.0)
        self.cue("becomes the seed", ovule.animate.set_fill(COATC, 0.9), FadeIn(endo), FadeIn(emb), rt=1.2)
        self.cue("most flowering", Indicate(ovary, color=FRUITC, scale_factor=1.03), rt=1.2)
        l2 = lab("ovary → fruit", FRUITC, 36).move_to(P(3.5, -1.3))
        ld2 = leader(P(1.6, -1.3), oc + P(1.9, -1.0))
        self.cue("the ovary around", FadeIn(l2), Create(ld2), rt=0.8)
        self.cue("becomes the fruit", ovary.animate.scale(1.18).set_fill(FRUITC, 0.5), rt=1.6)
        self.hold(VGroup(ovary, ovule, endo, emb))
        self.finish()


def dome_parts():
    DC = P(-3.4, -0.9)
    a, b = 2.5, 2.2
    pts = [DC + P(a * np.cos(t), b * np.sin(t)) for t in np.linspace(0, PI, 60)]
    dome = Polygon(*pts, stroke_color="#A9BC84", stroke_width=4, fill_color="#DDE6B8", fill_opacity=0.95)
    stalk = Rectangle(width=0.6, height=2.8, stroke_width=0, fill_color=GREY, fill_opacity=0.85).move_to(P(DC[0], -2.3))
    ovs = VGroup()
    for kk, n in ((0.9, 13), (0.63, 9), (0.36, 5)):
        for t in np.linspace(0.2, PI - 0.2, n):
            ovs.add(Ellipse(width=0.17, height=0.25, stroke_color="#FFE9B0", stroke_width=1.5, fill_color=FRUITC, fill_opacity=1)
                    .move_to(DC + P(kk * a * np.cos(t), kk * b * np.sin(t))))
    return DC, dome, stalk, ovs


class S04Flower(W):
    def construct(self):
        self.add(amb(4), mini_ledger(), schem())
        DC, dome, stalk, ovs = dome_parts()
        petals = VGroup(*[Ellipse(width=1.1, height=2.7, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.4)
                          .move_to(DC + P(0, 1.5)).rotate(a, about_point=DC) for a in (-1.3, -0.65, 0, 0.65, 1.3)])
        self.play(FadeIn(stalk), FadeIn(dome), FadeIn(petals, scale=0.9), run_time=0.7)
        self.cue("strawberry flower", Indicate(petals, color=WHITE, scale_factor=1.03), rt=1.2)
        self.cue("has many", *[p.animate.shift(DOWN * 1.2 + RIGHT * 0.3 * (i - 2)).rotate(0.3 * (i - 2)).set_opacity(0) for i, p in enumerate(petals)], rt=1.0)
        self.remove(petals)
        self.cue("separate ovaries", LaggedStart(*[FadeIn(o, scale=1.8) for o in ovs], lag_ratio=0.04, run_time=2.0), rt=2.0)
        ol = lab("many ovaries", FRUITC, 34).move_to(P(2.6, 2.0))
        self.fill("a dome", FadeIn(ol), Create(leader(P(0.6, 2.0), DC + P(1.9, 1.2))))
        self.cue("the dome is", dome.animate.set_fill(MAG, 0.55).set_stroke(MAG, 5), FadeOut(ol), rt=1.0)
        rl = lab("receptacle", MAG, 42).move_to(P(2.9, -0.2))
        self.cue("receptacle", FadeIn(rl), Create(leader(P(1.3, -0.2), DC + P(2.0, 0.0), MAG)), rt=0.8)
        r2 = lab("tip of the flower stalk", TEXT, 30).move_to(P(3.2, -1.0))
        self.cue("swollen tip", FadeIn(r2), Create(leader(P(0.9, -1.0), DC + P(0.3, -1.0))), Indicate(stalk, color=WHITE, scale_factor=1.06), rt=1.0)
        self.hold(VGroup(dome, ovs, stalk))
        self.finish()


class S05Achene(W):
    def construct(self):
        self.add(amb(5), mini_ledger(), schem())
        DC, dome, stalk, ovs = dome_parts()
        dome.set_fill(MAG, 0.55).set_stroke(MAG, 5)
        self.add(stalk, dome, ovs)
        self.cue("after fertilization", Indicate(ovs, color=WHITE, scale_factor=1.3), rt=1.4)
        speck = ovs[10]
        B = P(3.2, 0.25)
        bub = Circle(radius=2.55, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(B)
        wall = Ellipse(width=3.4, height=4.2, stroke_color=FRUITC, stroke_width=9, fill_color=FRUITC, fill_opacity=0.2).move_to(B)
        ln = VGroup(leader(speck.get_center(), B + 2.55 * P(np.cos(2.8), np.sin(2.8))),
                    leader(speck.get_center(), B + 2.55 * P(np.cos(3.5), np.sin(3.5))))
        self.cue("each ovary", speck.animate.scale(2.0).set_color(WHITE), Create(ln), FadeIn(bub), FadeIn(wall), rt=1.4)
        al = lab("achene: one fruit, one seed", FRUITC, 30).move_to(P(3.2, -2.95))
        self.cue("small dry fruit", FadeIn(al), Indicate(wall, color=WHITE, scale_factor=1.04), rt=1.0)
        endo = Ellipse(width=2.4, height=3.2, stroke_width=0, fill_color=ENDC, fill_opacity=0.95).move_to(B)
        emb = Ellipse(width=1.0, height=1.3, stroke_width=0, fill_color=EMBC, fill_opacity=1).rotate(-0.3).move_to(B + P(0.35, 0.8))
        self.cue("one seed", FadeIn(endo), FadeIn(emb), rt=1.0)
        s1 = stack([MAG, PAT], 0.6, 0.22, 0.05).move_to(emb)
        s2 = stack([MAG, MAG, PAT], 0.8, 0.24, 0.05).move_to(B + P(-0.3, -0.75))
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.8)
        self.cue("those specks", FadeOut(VGroup(bub, wall, endo, emb, s1, s2, ln, al)), speck.animate.scale(0.5).set_color(FRUITC), rt=1.0)
        tl = lab("true fruits", FRUITC, 38).move_to(P(3.2, 1.6))
        self.cue("true fruits", FadeIn(tl), Indicate(ovs, color=WHITE, scale_factor=1.3), rt=1.0)
        grp = VGroup(dome, ovs)
        t = grp.copy()
        t.scale(1.22, about_point=DC + P(0, 0.0))
        t[0].set_fill(FLESH, 1).set_stroke(FLESH, 4)
        fl = lab("flesh = receptacle", TEXT, 36).move_to(P(3.2, 1.6))
        self.cue("the red flesh", FadeOut(tl), Transform(grp, t), rt=1.6)
        st = stack([MAG, MAG], 0.9, 0.34, empty=1).move_to(P(3.2, 0.1))
        nm = T("2 + 0", 38, TEXT, font=MONO).move_to(P(3.2, -1.4))
        self.cue("swollen receptacle", FadeIn(fl), FadeIn(st), FadeIn(nm), rt=1.0)
        self.hold(VGroup(grp, stalk))
        self.finish()


class S05bAccessory(W):
    def construct(self):
        self.add(amb(6), mini_ledger(), schem())
        b = berry(P(0, 0.1), 3.8, 4.3, FLESH)
        self.play(FadeIn(b, scale=0.9), run_time=0.6)
        st = stack([MAG, MAG], 0.9, 0.32).move_to(P(0, -0.1))
        l2 = lab("flesh from receptacle", MAG, 30).move_to(P(0, -3.35))
        l1 = lab("accessory fruit", TEXT, 40).move_to(P(0, -2.85))
        self.cue("a fruit whose", Indicate(b[0], color=WHITE, scale_factor=1.03), rt=1.0)
        self.cue("flesh comes", FadeIn(st), FadeIn(l2), rt=1.0)
        self.cue("accessory fruit", FadeIn(l1, scale=1.2), rt=0.8)
        left = VGroup(b, st, l1, l2)
        self.fill("compare a tomato", Indicate(b[0], color=WHITE, scale_factor=1.02))
        self.cue("compare a tomato", left.animate.shift(LEFT * 3.5), rt=1.0)
        tm = tomato(P(3.5, 0.1))
        self.play(FadeIn(tm, scale=0.9), run_time=1.0)
        tl = lab("flesh from the ovary", FRUITC, 30).move_to(P(3.5, -2.85))
        self.cue("its flesh", FadeIn(tl), tm[0].animate.set_fill(FRUITC, 1), rt=1.0)
        st2 = stack([MAG, MAG], 0.8, 0.28).move_to(P(3.5, -0.2))
        self.cue("ovary itself", FadeIn(st2, scale=1.3), rt=0.9)
        self.hold(VGroup(left, tm, st2, tl))
        self.finish()


class S06Nitsch(W):
    def construct(self):
        self.add(amb(7), mini_ledger())
        bn = bench()
        self.play(Create(bn), run_time=0.8)
        yr = lab("1950", GOLD, 64, weight=BOLD).move_to(P(0.9, 2.9))
        self.cue("1950", FadeIn(yr, scale=1.3), rt=0.8)
        cap = lab("Jean Paul Nitsch, 1950", TEXT, 42).move_to(P(0.9, 2.9))
        self.cue("jean paul", ReplacementTransform(yr, cap), rt=1.0)
        row = [young(i) for i in range(3)]
        q = lab("?", TEXT, 56, weight=BOLD).move_to(P(RX[1], 0.9))
        self.cue("what makes", FadeIn(q, scale=1.4), rt=0.5)
        self.cue("the receptacle", *[FadeIn(r, scale=0.8) for r in row], rt=1.2)
        bob(q, 0.05)
        self.add(q)
        self.fill("young receptacles", Indicate(row[1][0], color=WHITE, scale_factor=1.05))
        self.cue("young receptacles", FadeOut(q), rt=0.4)
        tags = VGroup(*[lab("pollinated", POLC, 32).move_to(P(RX[i], -2.8)) for i in range(3)])
        self.cue("pollinated", FadeIn(tags), rt=0.9)
        self.cue("each studded", *[Indicate(r[2], color=WHITE, scale_factor=1.3) for r in row], rt=1.4)
        self.hold(VGroup(*row, tags, bn))
        self.finish()


class S07Idea(W):
    def construct(self):
        self.add(amb(8), mini_ledger(), bench())
        row = [young(i) for i in range(3)]
        self.add(*row)
        card = idea_card()
        self.cue("one idea", FadeIn(card[0]), rt=0.6)
        self.cue("grows on", FadeIn(card[1]), FadeIn(card[2]), FadeIn(card[3]), rt=0.9)
        self.cue("once the flower", swell(row[1], bottom(1)), rt=1.6)
        sec = lab("achenes irrelevant?", TEXT, 30).move_to(P(0.9, 2.45))
        self.cue("if so", FadeIn(sec, shift=UP * 0.15), rt=0.8)
        self.cue("achenes should not", row[1][2].animate.set_opacity(0.2), rt=1.0)
        self.hold(VGroup(*row, card, sec))
        self.finish()


class S08Predict(W):
    def construct(self):
        self.add(amb(9), mini_ledger(), bench())
        row = [young(i) for i in range(3)]
        self.add(*row)
        tw = tweezers().move_to(P(RX[1], 1.6))
        self.add(tw)
        c = P(RX[1], RYC)
        stops = [c + P(-0.6, 0.8), c + P(0.5, 0.5), c + P(-0.4, -0.1), c + P(0.5, -0.4), c + P(-0.2, -0.9), c + P(0.3, -1.0)]
        achs = list(row[1][2])
        self.at("removed every")
        self.play(AnimationGroup(
            Succession(*[tw.animate(run_time=0.5).move_to(s + P(0, 0.85)) for s in stops]),
            LaggedStart(*[a.animate.shift(UP * 0.7 + RIGHT * 0.2).set_opacity(0) for a in achs], lag_ratio=0.06, run_time=3.0)))
        self.play(FadeOut(tw), run_time=0.4)
        card = question_card()
        self.cue("if pollination alone", FadeIn(card, shift=DOWN * 0.2), rt=0.8)
        q = lab("?", TEXT, 60, weight=BOLD).move_to(P(RX[1], 0.9))
        self.cue("what would happen", FadeIn(q, scale=1.5), rt=0.6)
        bob(q, 0.06)
        self.add(q)
        self.cue("stripped receptacle", Indicate(row[1][0], color=WHITE, scale_factor=1.06), rt=1.0)
        self.hold(VGroup(*row, card))
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        self.add(amb(10), mini_ledger(), bench())
        row = [young(0), young(1, ach=False), young(2)]
        self.add(*row)
        self.add(question_card())
        q = lab("?", TEXT, 60, weight=BOLD).move_to(P(RX[1], 0.9))
        bob(q, 0.06)
        self.add(q)
        ring = Circle(radius=0.55, stroke_color=GREY, stroke_width=8).move_to(P(5.9, -3.1))
        arc = Arc(radius=0.55, start_angle=PI / 2, angle=-TAU, stroke_color=GOLD, stroke_width=8).move_to(P(5.9, -3.1))
        self.add(ring)
        self.play(Create(arc), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S10Reveal(W):
    def construct(self):
        self.add(amb(11), mini_ledger(), bench())
        row = [young(0), young(1, ach=False), young(2)]
        self.add(*row)
        card = idea_card()
        card[0].set_stroke(opacity=0.6)
        self.add(card)
        self.cue("did not enlarge", FadeIn(cross_at(P(-0.1, 3.2)), scale=1.5), rt=0.6)
        gl = [lab("grew", TEXT, 36, weight=BOLD).move_to(P(RX[i], -2.8)) for i in (0, 2)]
        self.cue("the intact receptacles", swell(row[0], bottom(0)), swell(row[2], bottom(2)), rt=1.8)
        sm = lab("stayed small", TEXT, 34, weight=BOLD).move_to(P(RX[1], -2.8))
        self.cue("but the stripped", FadeIn(gl[0]), FadeIn(gl[1]), FadeIn(sm), rt=0.8)
        self.cue("stayed small", Indicate(row[1][0], color=WHITE, scale_factor=1.06), rt=1.0)
        self.cue("growth needed", Indicate(row[0][2], color=WHITE, scale_factor=1.3), Indicate(row[2][2], color=WHITE, scale_factor=1.3), rt=1.6)
        self.cue("not just pollination", Indicate(card[1], color=POLC, scale_factor=1.15), rt=1.2)
        self.hold(VGroup(*row, card, *gl, sm))
        self.finish()


class S11Auxin(W):
    def construct(self):
        self.add(amb(12), mini_ledger(), bench())
        r0, r1, r2 = grown(0), young(1, ach=False), young(2)
        self.add(r0, r1, r2)
        self.at("next")
        self.play(*[a.animate.shift(UP * 0.7 + RIGHT * 0.2).set_opacity(0) for a in r2[2]], run_time=1.0)
        brush = VGroup(RoundedRectangle(corner_radius=0.08, width=0.55, height=0.3, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                       Line(P(0.15, 0.1), P(0.9, 0.9), color="#C9A97A", stroke_width=8)).move_to(P(RX[2] - 0.9, 0.7))
        self.cue("coated", FadeIn(brush), rt=0.3)
        c2 = P(RX[2], RYC)
        self.play(Succession(*[brush.animate(run_time=0.4).move_to(c2 + P(dx, dy)) for dx, dy in [(0.8, 0.5), (-0.7, 0.2), (0.7, -0.3), (-0.5, -0.7)]]))
        l1 = lab("auxin in paste", GOLD, 34).move_to(P(4.3, 2.4))
        self.cue("a paste", r2[1].animate.set_fill(GOLD, 0.45).set_stroke(GOLD, 5, 1), FadeOut(brush), FadeIn(l1), rt=1.0)
        l2 = lab("a plant hormone", GOLD, 28).move_to(P(4.3, 1.9))
        self.cue("plant hormone", FadeIn(l2), rt=0.8)
        self.cue("those receptacles", swell(r2, bottom(2)), rt=1.6)
        labs = row_labels([("intact", "grew"), ("stripped", "did not grow"), ("stripped + auxin", "grew")])
        self.play(FadeIn(labs), run_time=0.8)
        self.hold(VGroup(r0, r1, r2, labs, l1, l2))
        self.finish()


class S12Logic(W):
    def construct(self):
        self.add(amb(13), mini_ledger(), bench())
        r0, r1 = grown(0), young(1, ach=False)
        r2 = grown(2, ach=False)
        paste_tint(r2)
        self.add(r0, r1, r2)
        labs = row_labels([("intact", "grew"), ("stripped", "did not grow"), ("stripped + auxin", "grew")])
        self.add(labs)
        self.at("put the three")
        self.play(*[Indicate(labs[i], color=WHITE, scale_factor=1.12) for i in range(3)], run_time=2.0)
        al = sig_arrows_in(r0)
        sl = lab("signal", TEXT, 36).move_to(P(RX[0], -2.8))
        self.cue("developing achenes", FadeOut(labs), Indicate(r0[2], color=WHITE, scale_factor=1.3), rt=0.8)
        self.cue("growth signal", LaggedStart(*[GrowArrow(a) for a in al], lag_ratio=0.1, run_time=1.4), FadeIn(sl), rt=1.4)
        ar = sig_arrows_edge(r2[0].get_center(), RW * 1.45, RH * 1.45)
        ml = lab("auxin can mimic it", GOLD, 32).move_to(P(RX[2], -2.8))
        self.cue("applied", LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.1, run_time=1.4), rt=1.4)
        self.cue("stand in", FadeIn(ml), rt=0.8)
        self.hold(VGroup(r0, r1, r2, al, ar, sl, ml))
        self.finish()


class S13Limit(W):
    def construct(self):
        self.add(amb(14), mini_ledger(), bench())
        r0, r1 = grown(0), young(1, ach=False)
        r2 = grown(2, ach=False)
        paste_tint(r2)
        al = sig_arrows_in(r0)
        ar = sig_arrows_edge(r2[0].get_center(), RW * 1.45, RH * 1.45)
        sl = lab("signal", TEXT, 36).move_to(P(RX[0], -2.8))
        ml = lab("auxin can mimic it", GOLD, 32).move_to(P(RX[2], -2.8))
        self.add(r0, r1, r2, al, ar, sl, ml)
        self.fill("was enough", Indicate(r1[0], color=WHITE, scale_factor=1.03))
        self.cue("was enough", Indicate(r2, color=GOLD, scale_factor=1.04), rt=1.4)
        qm = lab("?", TEXT, 64, weight=BOLD).move_to(P(RX[0], -2.8))
        self.cue("natural signal", ReplacementTransform(sl, qm), rt=0.8)
        bx = RoundedRectangle(corner_radius=0.3, width=10.6, height=1.0, stroke_color=GOLD, stroke_width=4, fill_color=BG, fill_opacity=0.9).move_to(P(0.7, 2.95))
        bt = lab("auxin: sufficient, not shown to be the only signal", TEXT, 30).move_to(bx)
        self.cue("oxen alone", FadeIn(VGroup(bx, bt), shift=DOWN * 0.2), rt=0.9)
        self.fill("show how", Indicate(qm, color=WHITE, scale_factor=1.3))
        self.cue("show how", LaggedStart(*[Indicate(a, color=WHITE, scale_factor=1.4) for a in al], lag_ratio=0.12, run_time=1.8), rt=1.8)
        self.hold(VGroup(r0, r1, r2, al, ar, qm, ml))
        self.finish()


class S14Ledger(W):
    def construct(self):
        self.add(amb(15))
        mini = mini_ledger()
        self.add(mini)
        K, rows = ledger_group()
        self.cue("back to the ledger", ReplacementTransform(mini[0], K),
                 *[ReplacementTransform(mini[i + 1], rows[i][1]) for i in range(3)],
                 *[FadeIn(rows[i][0]) for i in range(3)], *[FadeIn(rows[i][2]) for i in range(3)], rt=1.5)
        self.cue("the flesh is", Indicate(rows[2][1], color=MAG, scale_factor=1.15), rt=1.0)
        c = P(-2.9, -0.2)
        b = berry(c, 4.6, 5.3, FLESH)
        st = stack([MAG, MAG], 0.9, 0.34, empty=1).move_to(P(3.2, 1.0))
        nm = T("2 + 0", 38, TEXT, font=MONO).move_to(P(3.2, -0.4))
        tl = lab("flesh: all mother", MAG, 34).move_to(P(3.2, 2.5))
        self.cue("all mother", Succession(FadeOut(VGroup(K, *rows), run_time=0.5), AnimationGroup(FadeIn(b, scale=0.9), FadeIn(st), FadeIn(nm), FadeIn(tl), run_time=0.7)), rt=1.2)
        self.cue("two magenta", Indicate(st, color=WHITE, scale_factor=1.15), rt=1.2)
        al = sig_arrows_in(b, 2)
        sl = lab("signal", TEXT, 36).move_to(P(1.4, -1.2))
        tgt = max(al, key=lambda a: a.get_center()[0])
        self.cue("in a normal fruit", Indicate(b[2], color=WHITE, scale_factor=1.3), rt=1.0)
        self.cue("a signal from", LaggedStart(*[GrowArrow(a) for a in al], lag_ratio=0.08, run_time=1.4), FadeIn(sl), Create(leader(P(0.9, -1.2), tgt.get_center())), rt=1.4)
        tube = VGroup(RoundedRectangle(corner_radius=0.1, width=0.9, height=0.4, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                      Rectangle(width=0.2, height=0.3, stroke_width=0, fill_color="#C9A97A", fill_opacity=1).shift(RIGHT * 0.55)).move_to(P(1.3, -2.5))
        al2 = lab("auxin can stand in", GOLD, 30).move_to(P(4.0, -2.5))
        self.cue("developing achenes", FadeIn(tube), FadeIn(al2), rt=0.9)
        self.hold(VGroup(b, al, st, nm))
        self.finish()


class S15Rule(W):
    def construct(self):
        self.add(amb(16), schem())
        c = P(-2.4, -0.1)
        patch_c = c + P(-1.1, -1.1)
        b = berry(c, 4.8, 5.5, FLESH, skip=(patch_c, 0.9, 0.7))
        patch = Ellipse(width=1.8, height=1.4, stroke_width=0, fill_color="#B83A44", fill_opacity=0.8).move_to(patch_c)
        self.play(FadeIn(b, scale=0.9), FadeIn(patch), run_time=1.2)
        cp = lab("strawberry, Nitsch 1950", TEXT, 32).move_to(P(3.4, 3.2))
        self.cue("one experiment", FadeIn(cp), rt=0.8)
        self.cue("accessory fruit", Indicate(b[0], color=WHITE, scale_factor=1.03), rt=1.2)
        rl = VGroup(lab("receptacle:", MAG, 34), lab("mother's tissue", MAG, 34)).arrange(DOWN, buff=0.12).move_to(P(3.4, 1.7))
        self.cue("the receptacle is", b[1].animate.set_fill(MAG, 0.4).set_stroke(MAG, 8, 1), FadeIn(rl), rt=1.2)
        al = lab("achenes", FRUITC, 36).move_to(P(3.4, -0.2))
        ach = max(list(b[2]), key=lambda a: a.get_center()[0])
        self.cue("the developing achenes", FadeIn(al), Create(leader(P(2.1, -0.2), ach.get_center(), FRUITC)),
                 Indicate(b[2], color=WHITE, scale_factor=1.4), rt=1.4)
        pl = lab("no achenes: stays small", TEXT, 30).move_to(P(-2.4, -3.4))
        self.cue("tell it to grow", FadeIn(pl), Create(leader(P(-3.4, -3.1), patch_c + P(0, -0.7))), Indicate(patch, color=WHITE, scale_factor=1.15), rt=1.2)
        self.hold(VGroup(b, patch))
        self.finish()


class S16End(EndCard):
    LINE = "The receptacle is the mother's, but the achenes tell it to grow."
