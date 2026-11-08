"""Proneural genes and lateral inhibition, chapter 1: Equal Cells, One Winner  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, shared by every chapter of this lesson; taken from scenes.old.py)
  GREEN  = proneural activity, and the neural-precursor fate (cell rim / fill: stronger green = more achaete)
  YELLOW = Delta (not used in this chapter)
  BLUE   = Notch (chips, signals between cells, the "picking" box)
  RED    = E(spl) repressor and inhibition arrows (here only the red cross that removes Notch)
  GREY   = cells, embryo and notum outlines, cells that are held back (mid grey, never black)
  LG     = light grey, for labels that need to read clearly on the dark ground
  GOLD   = questions, the question mark, the year
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PRO, NOT, ASK = GREEN, BLUE, GOLD
LG = "#C3CAD6"

ST = dict(
    neutral=dict(stroke_color=GREY, stroke_width=4, stroke_opacity=1, fill_color=GREY, fill_opacity=0.08),
    rim=dict(stroke_color=GREEN, stroke_width=5, stroke_opacity=0.8, fill_color=GREY, fill_opacity=0.08),
    comp=dict(stroke_color=GREEN, stroke_width=5, stroke_opacity=1, fill_color=GREEN, fill_opacity=0.25),
    win=dict(stroke_color=GREEN, stroke_width=7, stroke_opacity=1, fill_color=GREEN, fill_opacity=0.65),
    held=dict(stroke_color=GREY, stroke_width=4, stroke_opacity=0.85, fill_color=GREY, fill_opacity=0.14),
    ring=dict(stroke_color=GREY, stroke_width=3, stroke_opacity=0.85, fill_color=GREY, fill_opacity=0.10),
    tint=dict(stroke_color=GREEN, stroke_width=3, stroke_opacity=0.45, fill_color=GREEN, fill_opacity=0.10),
    clus=dict(stroke_color=GREEN, stroke_width=4, stroke_opacity=1, fill_color=GREEN, fill_opacity=0.5),
    strong=dict(stroke_color=GREEN, stroke_width=4, stroke_opacity=1, fill_color=GREEN, fill_opacity=0.9),
    low=dict(stroke_color=GREEN, stroke_width=4, stroke_opacity=0.6, fill_color=GREEN, fill_opacity=0.2),
    epi=dict(stroke_color=LG, stroke_width=4, stroke_opacity=1, fill_color=GREY, fill_opacity=0.25),
)


def arr(a, b, color=TEXT, w=5, tip=0.22):
    return Arrow(np.array(a, float), np.array(b, float), buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5)


def lab(text, size=26, color=LG, **kw):
    return T(text, size, color, **kw)


# ------------------------------------------------------------------ the five-cell cluster
CL = {"A": (-0.95, 0.0), "B": (0.95, 0.0), "C": (0, 1.6), "D": (-1.95, -1.5), "E": (1.95, -1.5)}
SC = 1.1
CCY = -0.3


def cluster(cx=0.0, cy=CCY, sc=SC, style="neutral"):
    d = {}
    for k, (x, y) in CL.items():
        d[k] = Circle(radius=0.85 * sc).move_to([cx + x * sc, cy + (y - 0.05) * sc, 0]).set_style(**ST[style])
    return d


def gv(d):
    return VGroup(*d.values())


# ------------------------------------------------------------------ embryo cross-section (map 1)
EA, EB, ECY = 4.7, 2.7, -0.2
NR = 48


def _ring():
    th = np.linspace(0, 2 * np.pi, 6001) - np.pi / 2
    x, y = EA * np.cos(th), EB * np.sin(th)
    s = np.r_[0, np.cumsum(np.hypot(np.diff(x), np.diff(y)))]
    out = []
    for i in range(NR):
        k = min(int(np.searchsorted(s, s[-1] * i / NR)), len(th) - 2)
        ang = np.arctan2(EB * np.cos(th[k]), -EA * np.sin(th[k]))
        out.append((x[k], y[k] + ECY, ang))
    return out


RING = _ring()


def md(i):
    return i % NR


VENT = [[md(i) for i in c] for c in ((-6, -5, -4), (-1, 0, 1), (4, 5, 6))]
OTHER = [[md(i) for i in c] for c in ((13, 14, 15), (19, 20, 21), (27, 28, 29), (34, 35, 36))]
CLUS = VENT + OTHER
NEURO = [md(i) for i in range(-7, 8)]
P0 = np.array([0.0, ECY - EB, 0.0])       # bottom of the ring in world coordinates
CTR = np.array([0.0, ECY, 0.0])
INNER = [md(i) for i in range(-6, 7)]     # the underside cells kept in the zoomed views
ZK, ZT = 1.85, (0.0, -2.5)                # zoomed view of the underside: scale, where the bottom point sits


class Emb:
    """The embryo ring, built directly at a view (scale k; the ring's bottom point sits at T)."""

    def __init__(self, k=1.0, T=None, only=None):
        self.k = k
        self.T = P0.copy() if T is None else np.array([T[0], T[1], 0.0])
        self.ids = list(range(NR)) if only is None else list(only)
        self.yolk = Ellipse(width=2 * (EA - 0.4) * k, height=2 * (EB - 0.4) * k).move_to(self.S(CTR)).set_style(
            stroke_color=GREY, stroke_width=2, stroke_opacity=0.3, fill_color=GREY, fill_opacity=0.03)
        self.c = {i: Circle(radius=0.24 * k).move_to(self.pos(i)).set_style(**ST["ring"]) for i in self.ids}
        self.cap = {}
        for n, cl in enumerate(CLUS):
            if all(i in self.c for i in cl):
                pts = np.mean([self.pos(i) for i in cl], axis=0)
                self.cap[n] = RoundedRectangle(corner_radius=0.37 * k, width=1.74 * k, height=0.76 * k,
                                               stroke_color=GREEN, stroke_width=3, stroke_opacity=0.8,
                                               fill_opacity=0).rotate(RING[cl[1]][2]).move_to(pts)

    def S(self, w):
        return self.T + self.k * (np.array(w, float) - P0)

    def pos(self, i):
        return self.S([RING[i][0], RING[i][1], 0.0])

    def inward(self, i, d):
        p = self.pos(i)
        v = self.S(CTR) - p
        return p + v / np.linalg.norm(v) * d

    def flat(self, i, w=1.0, h=0.36, style="epi"):
        return Ellipse(width=w, height=h).rotate(RING[i][2]).move_to(self.pos(i)).set_style(**ST[style])

    def style_neuro(self):
        for i in NEURO:
            if i in self.c:
                self.c[i].set_style(**ST["tint"])

    def style_clusters(self, style="clus"):
        for cl in CLUS:
            for i in cl:
                if i in self.c:
                    self.c[i].set_style(**ST[style])

    def mobs(self, caps=True, yolk=True):
        return ([self.yolk] if yolk else []) + list(self.c.values()) + (list(self.cap.values()) if caps else [])


def ring_near(x, y):
    d = [np.hypot(RING[i][0] - x, RING[i][1] - y) for i in range(NR)]
    return int(np.argmin(d))


def emb_title():
    return lab("cross-section of a fly embryo", 26).move_to([0, 3.4, 0])


def emb_ecto():
    i = ring_near(3.2, 1.9)
    p = np.array([RING[i][0], RING[i][1], 0])
    c = lab("ectoderm", 26).move_to([5.45, 2.75, 0])
    a = arr([4.55, 2.62, 0], p + np.array([0.3, 0.14, 0]), LG, 3, 0.18)
    return VGroup(c, a)


def emb_vne():
    return chip("ventral neuroectoderm", GREEN, size=26, pad=0.14).move_to([0, -1.85, 0])


def tabs(active=None):
    names = ["1  Embryo", "2  Notum", "3  Neural tube"]
    xs = [-4.5, 0, 4.5]
    g = VGroup()
    for n, (nm, x) in enumerate(zip(names, xs), 1):
        on = (n == active)
        col = TEXT if on else GREY
        c = chip(nm, col, size=26, pad=0.14, fill_opacity=0.22 if on else 0.05)
        if not on:
            c.set_opacity(0.7)
        g.add(c.move_to([x, 3.4, 0]))
    return g


def xmark(center, size=0.38, w=7):
    c = np.array(center, float)
    s = size
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=RED, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=RED, stroke_width=w))


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Proneural Genes and Lateral Inhibition"
    TITLE = "Equal Cells, One Winner"

    def construct(self):
        # same card as the house title, but it hands over to the first cluster of s01 instead of ending on a blank frame
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(Write(title), GrowFromCenter(rule), run_time=self.beat(0.35))
        self.wait(self.beat(0.2))
        self.play(FadeOut(g), run_time=0.4)
        self.play(FadeIn(gv(cluster(-2.7, -0.3, 1.2))), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        cl = cluster(-2.7, -0.3, 1.2)
        g = gv(cl)
        grp = lab("a small group of cells", 28).move_to([3.6, 2.75, 0])
        ga = arr([2.0, 2.45, 0], [-0.2, 1.6, 0], LG, 3, 0.18)
        self.add(g)     # the cluster is already there: the title card handed it over
        self.play(FadeIn(grp, shift=LEFT * 0.2), GrowArrow(ga), run_time=0.9)
        self.at("all equal")
        self.play(*[Indicate(c, color=TEXT, scale_factor=1.07) for c in g], run_time=0.9)
        self.at("everyone could become")
        self.play(*[c.animate.set_style(**ST["rim"]) for c in g], run_time=0.6)
        self.at("nerve cell")
        nc = chip("nerve cell", GREEN, size=34).move_to([3.7, 1.0, 0])
        na = arr([2.4, 0.9, 0], [-0.4, 0.35, 0], GREEN, 4, 0.2)
        self.play(FadeIn(nc, shift=LEFT * 0.25), GrowArrow(na), run_time=0.5)
        self.at("why does only one")
        q = T("Why does\nonly one?", 64, GOLD, TITLE_FONT).move_to([3.6, -1.6, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.4)
        self.at("only one")
        self.play(Indicate(q, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s02_end_state():
    E = Emb()
    E.style_neuro()
    E.style_clusters("clus")
    labs = [emb_title(), emb_ecto(), emb_vne()]
    return E, labs


class S02Embryo(SpokenScene):
    def construct(self):
        E = Emb()
        self.add(E.yolk)
        self.at("fly embryo")
        ttl = emb_title()
        self.play(LaggedStart(*[GrowFromCenter(c) for c in E.c.values()], lag_ratio=0.025), FadeIn(ttl, shift=DOWN * 0.1),
                  run_time=1.5)
        self.at("cells that will make")
        eco = emb_ecto()
        self.play(FadeIn(eco), run_time=0.5)
        self.at("nervous system")
        vne = emb_vne()
        self.play(*[E.c[i].animate.set_style(**ST["tint"]) for i in NEURO], FadeIn(vne, shift=UP * 0.1), run_time=0.9)
        self.at("small groups")
        self.play(*[E.c[i].animate.set_style(**ST["clus"]) for cl in CLUS for i in cl],
                  *[Create(c) for c in E.cap.values()], run_time=1.0)
        self.finish()


class S03Usually(SpokenScene):
    def construct(self):
        E, labs = s02_end_state()
        self.add(*E.mobs(), *labs)
        trio = VGroup(*[E.c[i] for i in VENT[1]])
        rest = VGroup(E.yolk, *[E.c[i] for i in E.ids if i not in VENT[1]], *E.cap.values())
        kz = 4.25
        piv = E.pos(0)
        tgt = np.array([0.0, CCY, 0.0])
        sh = tgt - piv
        big = cluster(0, CCY, SC)
        self.play(*[FadeOut(m) for m in labs], run_time=0.3)    # labels go before the zoom, so no cell strikes through them
        self.play(rest.animate.scale(kz, about_point=piv).shift(sh).set_opacity(0),
                  trio.animate.scale(kz, about_point=piv).shift(sh), run_time=0.9)
        self.remove(rest)
        view = lab("one cluster,\nseen from above", 30, TEXT, line_spacing=1.0).move_to([-4.6, 0.3, 0])
        self.play(ReplacementTransform(trio[0], big["A"]), ReplacementTransform(trio[1], big["C"]),
                  ReplacementTransform(trio[2], big["B"]), GrowFromCenter(big["D"]), GrowFromCenter(big["E"]),
                  FadeIn(view), run_time=0.6)
        self.at("become a neural precursor")
        chp = chip("neural precursor", GREEN, size=28).move_to([4.7, 2.5, 0])
        self.play(*[c.animate.set_style(**ST["rim"]) for c in big.values()], FadeIn(chp, shift=LEFT * 0.2), run_time=0.7)
        self.at("usually only one")
        a = arr(chp.get_left() + LEFT * 0.08, big["C"].get_right() + RIGHT * 0.05 + UP * 0.05, GREEN)
        self.play(big["C"].animate.set_style(**ST["win"]), *[big[k].animate.set_style(**ST["held"]) for k in "ABDE"],
                  GrowArrow(a), FadeOut(view), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
TIE_BY, TIE_L, TIE_PY, TIE_R = 1.9, 3.4, -0.5, 0.935


def tie_scale():
    """The balance, drawn flat (as s04 leaves it): post, base, beam, pivot, pans."""
    by, L, py = TIE_BY, TIE_L, TIE_PY
    post = Line([0, by, 0], [0, -2.6, 0], color=GREY, stroke_width=8)
    base = Polygon([-1.1, -2.9, 0], [1.1, -2.9, 0], [0, -2.5, 0], stroke_color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=0.25)
    beam = Line([-L, by, 0], [L, by, 0], color=TEXT, stroke_width=9)
    piv = Dot([0, by, 0], radius=0.14, color=TEXT)
    hangs = VGroup()
    for s_ in (-1, 1):
        cx = s_ * L
        hangs.add(Line([cx, by, 0], [cx - 1.6, py, 0], color=GREY, stroke_width=3),
                  Line([cx, by, 0], [cx + 1.6, py, 0], color=GREY, stroke_width=3),
                  Line([cx - 1.6, py, 0], [cx + 1.6, py, 0], color=TEXT, stroke_width=6))
    return post, base, beam, piv, hangs


class S04Tie(SpokenScene):
    def construct(self):
        # open on the cluster exactly as s03 left it, then carry two of its cells onto the scale
        big = cluster(0, CCY, SC)
        big["C"].set_style(**ST["win"])
        for k in "ABDE":
            big[k].set_style(**ST[ "held"])
        chp = chip("neural precursor", GREEN, size=28).move_to([4.7, 2.5, 0])
        a = arr(chp.get_left() + LEFT * 0.08, big["C"].get_right() + RIGHT * 0.05 + UP * 0.05, GREEN)
        self.add(gv(big), chp, a)
        by, L, py, r = TIE_BY, TIE_L, TIE_PY, TIE_R
        post, base, beam, piv, hangs = tie_scale()
        cA, cB = big["A"], big["B"]
        swing = VGroup(beam, piv, hangs, cA, cB)
        self.play(FadeOut(chp), FadeOut(a), big["C"].animate.set_style(**ST["held"]),
                  FadeOut(big["D"]), FadeOut(big["E"]),
                  cA.animate.move_to([-L, py + r, 0]).set_style(**ST["neutral"]),
                  cB.animate.move_to([L, py + r, 0]).set_style(**ST["neutral"]),
                  FadeIn(post), FadeIn(base), Create(beam), FadeIn(piv), FadeIn(hangs), run_time=0.8)
        self.play(FadeOut(big["C"]), run_time=0.2)
        self.at("start equal")
        self.play(Indicate(cA, color=TEXT, scale_factor=1.12), Indicate(cB, color=TEXT, scale_factor=1.12), run_time=0.9)
        self.at("break the tie")
        q = T("?", 110, GOLD, TITLE_FONT).move_to([0, 3.0, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.play(Rotate(swing, 0.035, about_point=[0, by, 0]), run_time=0.35)
        self.play(Rotate(swing, -0.07, about_point=[0, by, 0]), run_time=0.5)
        self.play(Rotate(swing, 0.035, about_point=[0, by, 0]), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
CX2 = 1.6


def step_card(y, text, color, dim=False):
    m = chip(text, color, size=28, pad=0.2)
    m.move_to([-6.4 + m.width / 2, y, 0])
    if dim:
        m.set_opacity(0.45)
    return m


class S05Twosteps(SpokenScene):
    def construct(self):
        cl = cluster(CX2, CCY)
        g = gv(cl)
        # open on the balance exactly as s04 leaves it, and turn its two cells into the cluster
        post, base, beam, piv, hangs = tie_scale()
        cA = Circle(radius=TIE_R).move_to([-TIE_L, TIE_PY + TIE_R, 0]).set_style(**ST["neutral"])
        cB = Circle(radius=TIE_R).move_to([TIE_L, TIE_PY + TIE_R, 0]).set_style(**ST["neutral"])
        qm = T("?", 110, GOLD, TITLE_FONT).move_to([0, 3.0, 0])
        old = VGroup(post, base, beam, piv, hangs, qm)
        self.add(old, cA, cB)
        self.play(FadeOut(old), ReplacementTransform(cA, cl["A"]), ReplacementTransform(cB, cl["B"]),
                  LaggedStart(*[GrowFromCenter(cl[k]) for k in "CDE"], lag_ratio=0.15), run_time=1.0)
        self.at("two steps")
        s1 = step_card(0.9, "1  competence", GREEN)
        s2 = step_card(-0.7, "2  selection", NOT, dim=True)
        self.play(FadeIn(s1, shift=RIGHT * 0.2), FadeIn(s2, shift=RIGHT * 0.2), run_time=0.7)
        self.at("genes make a group")
        box = DashedVMobject(SurroundingRectangle(g, buff=0.2, corner_radius=0.35, color=GREEN, stroke_width=4),
                             num_dashes=44)
        chp = chip("proneural genes", GREEN, size=28).move_to([CX2, 3.2, 0])
        a = arr([CX2, 2.9, 0], [CX2, 2.6, 0], GREEN, 4, 0.16)
        self.play(FadeIn(chp, shift=DOWN * 0.1), GrowArrow(a), Create(box), run_time=0.9)
        self.at("able to become neural")
        self.play(*[c.animate.set_style(**ST["comp"]) for c in g], Indicate(s1, color=GREEN, scale_factor=1.08),
                  run_time=1.1)
        self.finish()


S6K = 0.55      # the cells shrink a little so the Notch arrows fit between them


class S06Twosteps2(SpokenScene):
    def construct(self):
        cl = cluster(CX2, CCY, style="comp")
        g = gv(cl)
        s1, s2 = step_card(0.9, "1  competence", GREEN, dim=True), step_card(-0.7, "2  selection", NOT)
        self.add(g, s1, s2)
        self.play(*[c.animate.scale(S6K) for c in g], run_time=0.5)
        rr = 0.935 * S6K
        pairs = [("A", "B"), ("A", "C"), ("B", "C"), ("A", "D"), ("B", "E")]
        cen = np.mean([c.get_center() for c in g], axis=0)
        sig, nl = VGroup(), VGroup()
        for p, q in pairs:
            a, b = cl[p].get_center(), cl[q].get_center()
            u = (b - a) / np.linalg.norm(b - a)
            m = (a + b) / 2
            sig.add(DoubleArrow(a + u * (rr + 0.07), b - u * (rr + 0.07), buff=0, color=TEXT, stroke_width=8,
                                tip_length=0.26, max_tip_length_to_length_ratio=0.5))
            n = np.array([-u[1], u[0], 0.0])
            if (p, q) == ("A", "B"):
                n = np.array([0.0, -1.0, 0.0])
            elif np.dot(n, m - cen) < 0:
                n = -n
            off = 0.85 if (p, q) == ("A", "B") else 0.95
            nl.add(T("Notch", 28, NOT, weight=BOLD).move_to(m + n * off))
        self.at("signal to each other")
        self.play(LaggedStart(*[GrowFromCenter(x) for x in sig], lag_ratio=0.1), run_time=0.9)
        self.at("through notch")
        self.play(sig.animate.set_color(NOT), FadeIn(nl, shift=UP * 0.05), run_time=0.6)
        self.at("one wins")
        self.play(cl["C"].animate.set_style(**ST["win"]), *[cl[k].animate.set_style(**ST["held"]) for k in "ABDE"],
                  FadeOut(sig), FadeOut(nl), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def map1_state(flat=False):
    """The zoomed underside with three neuroblasts dropped in, as s07 leaves it."""
    E = Emb(ZK, ZT, only=INNER)
    E.style_neuro()
    E.style_clusters("clus")
    for cl in VENT:
        i = cl[1]
        E.c[i].move_to(E.inward(i, 2.4)).scale(1.35).set_style(**ST["strong"])
    if flat:
        for cl in VENT:
            for i in (cl[0], cl[2]):
                E.c[i] = E.flat(i)
    return E


NB_CHIP_Y = 1.45


class S07Map1(SpokenScene):
    def construct(self):
        E, labs = s02_end_state()
        vne = labs[2]
        self.add(*E.mobs(), vne)
        self.at("three maps")
        tb = tabs(None)
        self.play(FadeIn(tb, shift=DOWN * 0.15), run_time=0.8)
        gin = VGroup(*[E.c[i] for i in INNER], *[E.cap[n] for n in (0, 1, 2)])
        gout = VGroup(E.yolk, *[E.c[i] for i in E.ids if i not in INNER], *[E.cap[n] for n in range(3, 7)])
        T2 = np.array([ZT[0], ZT[1], 0.0])
        # everything that would cross the tab chips or the label goes first; then the underside zooms alone
        self.at("embryo's underside", lead=0.75)
        self.play(FadeOut(gout), FadeOut(vne), run_time=0.45)
        self.play(gin.animate.scale(ZK, about_point=P0).shift(T2 - P0), Transform(tb, tabs(1)), run_time=1.2)
        Z = Emb(ZK, ZT, only=INNER)
        self.at("one cell from each cluster")
        mids = [cl[1] for cl in VENT]
        self.play(*[Indicate(E.c[i], color=GREEN, scale_factor=1.4) for i in mids], run_time=1.0)
        self.at("moves inward")
        self.play(*[E.c[i].animate.move_to(Z.inward(i, 2.4)).scale(1.35).set_style(**ST["strong"]) for i in mids],
                  run_time=1.2)
        self.at("neuroblast")
        nb = chip("neuroblast", GREEN, size=30).move_to([0, NB_CHIP_Y, 0])
        a = arr([0, NB_CHIP_Y - 0.4, 0], [0, 0.65, 0], GREEN, 4, 0.2)
        self.play(FadeIn(nb, shift=DOWN * 0.1), GrowArrow(a), run_time=0.7)
        self.finish()


class S08Map1b(SpokenScene):
    def construct(self):
        E = map1_state()
        nb = chip("neuroblast", GREEN, size=30).move_to([0, NB_CHIP_Y, 0])
        a = arr([0, NB_CHIP_Y - 0.4, 0], [0, 0.65, 0], GREEN, 4, 0.2)
        tb = tabs(1)
        self.add(*E.mobs(yolk=False), nb, a, tb)
        self.at("a neuroblast is")
        self.play(*[Indicate(E.c[cl[1]], color=GREEN, scale_factor=1.2) for cl in VENT], run_time=0.9)
        self.at("neural stem cell")
        nb2 = chip("neuroblast: neural stem cell", GREEN, size=30).move_to([0, NB_CHIP_Y, 0])
        self.play(Transform(nb, nb2), run_time=0.7)
        self.at("rest of the cluster")
        rest = [i for cl in VENT for i in (cl[0], cl[2])]
        self.play(*[Indicate(E.c[i], color=LG, scale_factor=1.25) for i in rest], run_time=0.9)
        self.at("becomes epidermis")
        self.play(*[Transform(E.c[i], E.flat(i)) for i in rest], *[FadeOut(E.cap[n]) for n in (0, 1, 2)], run_time=0.5)
        self.at("epidermis")
        ep = chip("epidermis", LG, size=30).move_to([-5.2, 0.55, 0])
        i0 = VENT[0][0]
        tip = E.pos(i0) + np.array([0.0, 0.3, 0])
        epa = arr([-5.45, 0.15, 0], tip, LG, 4, 0.2)
        self.play(FadeIn(ep, shift=RIGHT * 0.2), GrowArrow(epa), run_time=0.6)
        self.at("the skin")
        ep2 = lab("(the skin)", 30, LG).move_to([-5.2, 1.25, 0])
        self.play(FadeIn(ep2, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
NCY = -0.4
OFFS = [(-0.38, 0.0), (0.38, 0.0), (0.0, 0.5)]
BRIS = 0.45
ROWS = [(0.7, (-2.5, -0.8, 0.8, 2.5)), (-1.2, (-2.7, -0.9, 0.9, 2.7)), (-2.75, (-1.2, 1.2))]
SITES = [(x, y) for y, xs in ROWS for x in xs]
SOP_SITE = (2.5, 0.7)


def notum_body():
    return Ellipse(width=8.0, height=5.8).move_to([0, NCY, 0]).set_style(
        stroke_color=GREY, stroke_width=4, stroke_opacity=1, fill_color=GREY, fill_opacity=0.06)


def site_cells(x, y, style="comp"):
    return VGroup(*[Circle(radius=0.25).move_to([x + dx, y + dy, 0]).set_style(**ST[style]) for dx, dy in OFFS])


def bristle(x, y, w=5):
    return Line([x, y + 0.5 + 0.25, 0], [x, y + 0.5 + 0.25 + BRIS, 0], color=TEXT, stroke_width=w)


def notum_label():
    t = lab("notum:\nback of the\nfly's thorax", 28, TEXT, line_spacing=1.0).move_to([-5.3, 1.4, 0])
    a = arr([-4.2, 1.4, 0], [-3.5, 1.4, 0], TEXT, 4, 0.2)
    return VGroup(t, a)


def sop_label():
    t = lab("sensory organ\nprecursor\n(SOP)", 26, GREEN, line_spacing=1.0).move_to([4.7, 2.1, 0])
    a = arr([3.6, 1.45, 0], [2.85, 1.3, 0], GREEN, 4, 0.2)
    return VGroup(t, a)


def small_ticks():
    rs = np.random.RandomState(4)
    g = VGroup()
    for x in np.arange(-3.4, 3.5, 0.47):
        xx = x + rs.uniform(-0.1, 0.1)
        y = rs.uniform(0.12, 0.26)
        g.add(Line([xx, y, 0], [xx + rs.uniform(-0.03, 0.03), y + 0.13, 0], color=GREY, stroke_width=3).set_opacity(0.6))
    for x in list(np.arange(-3.3, -2.0, 0.42)) + list(np.arange(2.2, 3.4, 0.42)):
        xx = x + rs.uniform(-0.08, 0.08)
        y = rs.uniform(-2.4, -2.2)
        g.add(Line([xx, y, 0], [xx, y + 0.13, 0], color=GREY, stroke_width=3).set_opacity(0.6))
    return g


class S09Map2(SpokenScene):
    def construct(self):
        E = map1_state(flat=True)
        tb = tabs(1)
        self.add(*E.mobs(caps=False, yolk=False), tb)
        body = notum_body()
        nl = notum_label()
        self.play(*[FadeOut(m) for m in E.mobs(caps=False, yolk=False)], Transform(tb, tabs(2)), FadeIn(body, scale=0.9),
                  FadeIn(nl), run_time=0.9)
        cls = [site_cells(x, y, "comp") for x, y in SITES]
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cls], lag_ratio=0.08), run_time=1.6)
        self.at("small clusters")
        self.play(*[Indicate(c, color=GREEN, scale_factor=1.15) for c in cls], run_time=0.8)
        self.at("large bristles")
        gb = VGroup(*[bristle(x, y) for x, y in SITES])
        st = small_ticks()
        self.play(LaggedStart(*[Create(b) for b in gb], lag_ratio=0.06), FadeIn(st), run_time=1.0)
        self.at("each gives one")
        self.play(*[c[2].animate.set_style(**ST["win"]) for c in cls],
                  *[c[i].animate.set_style(**ST["held"]) for c in cls for i in (0, 1)], run_time=1.0)
        self.at("sensory organ precursor")
        j = SITES.index(SOP_SITE)
        sl = sop_label()
        self.play(FadeIn(sl[0], shift=LEFT * 0.2), GrowArrow(sl[1]), Indicate(cls[j][2], color=TEXT, scale_factor=1.6),
                  run_time=0.8)
        self.finish()


def stripes():
    bands, dots, ticks = VGroup(), VGroup(), VGroup()
    for x in (-3.3, 0.0, 3.3):
        bands.add(RoundedRectangle(corner_radius=0.5, width=2.2, height=5.7, stroke_color=GREEN, stroke_width=4,
                                   stroke_opacity=0.75, fill_color=GREEN, fill_opacity=0.12).move_to([x, 0.05, 0]))
        for r in range(8):
            for dx in (-0.5, 0.5):
                y = 2.0 - r * 0.6
                dots.add(Circle(radius=0.2).move_to([x + dx, y, 0]).set_style(**ST["clus"]))
                ticks.add(Line([x + dx, y + 0.2, 0], [x + dx, y + 0.2 + 0.36, 0], color=TEXT, stroke_width=4).set_opacity(0.85))
    return bands, dots, ticks


class S10Map2b(SpokenScene):
    def construct(self):
        tb = tabs(2)
        body = notum_body()
        nl = notum_label()
        j = SITES.index(SOP_SITE)
        cls = [site_cells(x, y, "comp") for x, y in SITES]
        for c in cls:
            c[2].set_style(**ST["win"])
            c[0].set_style(**ST["held"])
            c[1].set_style(**ST["held"])
        gb = VGroup(*[bristle(x, y) for x, y in SITES])
        st = small_ticks()
        sl = sop_label()
        self.add(body, nl, *cls, gb, st, sl, tb)
        sop = Circle(radius=1.0).move_to([0, 0.0, 0]).set_style(**ST["win"])
        l = Circle(radius=0.75).move_to([-2.4, -0.55, 0]).set_style(**ST["held"])
        r = Circle(radius=0.75).move_to([2.4, -0.55, 0]).set_style(**ST["held"])
        zoom = VGroup(l, r, sop)     # same child order as the site (held, held, winner) so each cell morphs into its own
        others = [body, nl, gb, st, sl] + [c for k, c in enumerate(cls) if k != j]
        self.play(*[FadeOut(m) for m in others], ReplacementTransform(cls[j], zoom), run_time=0.6)
        self.at("builds one bristle")
        bri = Polygon([-0.14, 1.0, 0], [0.14, 1.0, 0], [0.03, 2.7, 0], stroke_width=0, fill_color=TEXT, fill_opacity=0.9)
        blab = T("bristle", 28, TEXT).move_to([1.5, 2.2, 0])
        self.play(GrowFromPoint(bri, [0, 1.0, 0]), FadeIn(blab), run_time=0.9)
        self.at("its neuron")
        axon = Line([0, -1.75, 0], [0, -3.1, 0], color=GREEN, stroke_width=7)
        soma = Circle(radius=0.34).move_to([0, -1.45, 0]).set_style(**ST["strong"])
        nlab = T("neuron", 28, GREEN).move_to([1.5, -2.3, 0])
        self.play(GrowFromCenter(soma), Create(axon), FadeIn(nlab), run_time=1.0)
        self.at("the rest become")
        self.play(Indicate(l, color=TEXT, scale_factor=1.15), Indicate(r, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.at("epidermis")
        fl = Ellipse(width=2.2, height=0.6).move_to(l.get_center()).set_style(**ST["epi"])
        fr = Ellipse(width=2.2, height=0.6).move_to(r.get_center()).set_style(**ST["epi"])
        el = chip("epidermis", LG, size=28).move_to([-4.9, 0.6, 0])
        ea = arr([-4.1, 0.25, 0], [-3.1, -0.3, 0], LG, 4, 0.2)
        self.play(Transform(l, fl), Transform(r, fr), FadeIn(el, shift=RIGHT * 0.2), GrowArrow(ea), run_time=0.9)
        self.at("small bristles")
        bands, dots, ticks = stripes()
        sb = lab("small bristles", 30, TEXT).move_to([0, -3.3, 0])
        self.play(*[FadeOut(m) for m in (sop, l, r, bri, blab, soma, axon, nlab, el, ea)], FadeIn(sb), run_time=0.4)
        self.play(FadeIn(dots), FadeIn(ticks), run_time=0.6)
        self.at("broader stripes")
        sb2 = lab("small bristles: broader stripes, many precursors", 30, TEXT).move_to([0, -3.3, 0])
        self.play(FadeOut(sb), run_time=0.25)
        self.play(FadeIn(bands), FadeIn(sb2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
TCY = -0.35
NW = 32
TIN = (0.8, 1.45)
TOUT = (3.6, 2.95)


def tpt(t, f):
    return [(TIN[0] + f * (TOUT[0] - TIN[0])) * np.cos(t), TCY + (TIN[1] + f * (TOUT[1] - TIN[1])) * np.sin(t), 0]


def tube(fill=0.08, color=GREY):
    wedges = VGroup()
    for k in range(NW):
        t0, t1 = 2 * np.pi * k / NW, 2 * np.pi * (k + 1) / NW
        pts = [tpt(t0, 0), tpt(t0, 1), tpt(t1, 1), tpt(t1, 0)]
        wedges.add(Polygon(*pts, stroke_color=GREY, stroke_width=2.5, stroke_opacity=0.85,
                           fill_color=color, fill_opacity=fill).scale(0.93))
    return wedges


class S11Map3(SpokenScene):
    def construct(self):
        tb = tabs(2)
        bands, dots, ticks = stripes()
        sb2 = lab("small bristles: broader stripes, many precursors", 30, TEXT).move_to([0, -3.3, 0])
        self.add(bands, dots, ticks, sb2, tb)
        self.play(*[FadeOut(m) for m in (bands, dots, ticks, sb2)], Transform(tb, tabs(3)), run_time=0.4)
        self.at("third map")
        wd = tube()
        self.play(LaggedStart(*[FadeIn(w, scale=0.9) for w in wd], lag_ratio=0.02), run_time=0.9)
        self.at("vertebrate neural tube")
        lum = lab("lumen", 26).move_to([0, TCY, 0])
        nlab = chip("neural tube", TEXT, size=28).move_to([-5.1, 1.5, 0])
        la = arr([-3.8, 1.35, 0], [-2.7, 0.9, 0], LG, 3, 0.18)
        self.play(FadeIn(lum), FadeIn(nlab), GrowArrow(la), run_time=0.7)
        self.at("there", lead=0.7)
        prog = VGroup()
        for t in (0.3, np.pi - 0.3, np.pi + 0.3, -0.3):
            prog.add(Circle(radius=0.27).move_to(tpt(t, 0.13)).set_style(**ST["strong"]))
        pl = chip("progenitors", GREEN, size=28).move_to([5.2, 0.9, 0])
        pa = arr([4.1, 0.75, 0], np.array(tpt(0.3, 0.13)) + np.array([0.4, 0.05, 0]), GREEN, 3, 0.18)
        self.play(FadeIn(prog, scale=0.6), FadeIn(pl, shift=LEFT * 0.2), GrowArrow(pa), run_time=0.45)
        # one cell divides in front of the label, and the 'progenitors' chip stays on screen the whole time
        self.at("the cells are", lead=0.65)
        div = []
        for p in (prog[0], prog[1]):
            c = p.get_center()
            c1 = Circle(radius=0.25).move_to(c + UP * 0.1).set_style(**ST["strong"])
            c2 = Circle(radius=0.25).move_to(c + DOWN * 0.1).set_style(**ST["strong"])
            div.append((p, c1, c2))
        self.play(*[p.animate.stretch(1.5, 1).set_fill(GREEN, 1.0) for p, *_ in div], run_time=0.3)
        for p, c1, c2 in div:
            self.remove(p)
            self.add(c1, c2)
        self.play(*[c1.animate.shift(UP * 0.4) for p, c1, c2 in div], *[c2.animate.shift(DOWN * 0.4) for p, c1, c2 in div],
                  run_time=0.5)
        self.at("already neural")
        an = chip("already neural", GREEN, size=26).move_to([5.05, -1.5, 0])
        aa = arr([3.85, -1.35, 0], [3.0, -0.8, 0], GREEN, 3, 0.18)
        self.play(*[w.animate.set_fill(GREEN, 0.3) for w in wd], FadeIn(an, shift=LEFT * 0.2), GrowArrow(aa), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Casting(SpokenScene):
    def construct(self):
        E = Emb(ZK, ZT, only=INNER)
        tb = tabs(3)
        wd = tube(0.3, GREEN)
        self.add(wd, tb)
        self.play(FadeOut(wd), Transform(tb, tabs(1)),
                  LaggedStart(*[GrowFromCenter(c) for c in E.c.values()], lag_ratio=0.03), run_time=0.7)
        self.at("step one")
        st = T("Step 1", 38, GREEN, TITLE_FONT).move_to([-5.6, 2.3, 0])
        self.play(FadeIn(st, shift=DOWN * 0.1), run_time=0.5)
        self.at("gene first comes on")
        mid = VENT[1]
        self.play(*[E.c[i].animate.set_style(**ST["comp"]) for i in mid], run_time=1.0)
        self.at("whole cluster")
        self.play(Create(E.cap[1]), *[Indicate(E.c[i], color=GREEN, scale_factor=1.15) for i in mid], run_time=0.9)
        self.at("think of it")
        cc = chip("casting call", GREEN, size=36).move_to([0, 1.3, 0])
        ea = lab("everyone auditions", 30, TEXT).move_to([0, 0.5, 0])
        ar = arr([0, 0.1, 0], [0, -1.7, 0], GREEN, 4, 0.2)
        self.play(FadeIn(cc, shift=DOWN * 0.1), FadeIn(ea), GrowArrow(ar), run_time=0.8)
        self.at("casting call")
        self.play(*[E.c[i].animate.set_style(**ST["win"]) for i in mid], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
RING_CL = [(1, 2, 3), (6, 7, 8), (12, 13, 14), (18, 19, 20)]


def mini_ring(cx, cy, w=3.0, h=2.5, n=22, stage=1):
    """A small embryo for the staged series: stage 1 nothing lit, 2 two clusters, 3 four clusters, 4 one bright cell each."""
    body = Ellipse(width=w, height=h).move_to([cx, cy, 0]).set_style(
        stroke_color=GREY, stroke_width=3, stroke_opacity=0.8, fill_color=GREY, fill_opacity=0.06)
    cells = []
    for k, t in enumerate(np.linspace(0, 2 * np.pi, n, endpoint=False)):
        c = Circle(radius=0.14).move_to([cx + (w / 2 - 0.12) * np.cos(t), cy + (h / 2 - 0.12) * np.sin(t), 0])
        c.set_style(**ST["ring"])
        for ci, cl in enumerate(RING_CL):
            if k in cl and (stage == 2 and ci in (0, 2) or stage == 3 or stage == 4):
                c.set_style(**ST["comp"] if stage < 4 else (ST["win"] if k == cl[1] else ST["low"]))
        cells.append(c)
    return VGroup(body, VGroup(*cells))


class S13Rg(SpokenScene):
    def construct(self):
        yr = T("1993", 110, GOLD, TITLE_FONT).move_to([0, 0.6, 0])
        self.play(FadeIn(yr, scale=0.85), run_time=0.4)
        self.at("mar ruiz gomez", lead=0.9)
        self.play(yr.animate.scale(0.5).move_to([-5.0, 3.2, 0]), run_time=0.6)
        names = T("Mar Ruiz-Gómez and Alain Ghysen", 36, TEXT, TITLE_FONT).move_to([1.5, 3.2, 0])
        self.play(FadeIn(names, shift=LEFT * 0.2), run_time=0.6)
        xs = [-4.95, -1.65, 1.65, 4.95]
        self.at("followed the", lead=0.3)
        # four staged embryos, built left to right; each stage label arrives with its embryo
        embs = []
        for n, x in enumerate(xs):
            e = mini_ring(x, -0.5, stage=n + 1)
            sl = lab(f"stage {n + 1}", 30, TEXT).move_to([x, -2.1, 0])
            embs.append((e, sl))
            self.play(GrowFromCenter(e), FadeIn(sl, shift=UP * 0.1), run_time=0.42)
        # the gene chip is anchored to the series with a bracket and an arrow
        br = VGroup(Line([-6.4, 1.05, 0], [6.4, 1.05, 0], color=GREEN, stroke_width=4),
                    Line([-6.4, 1.05, 0], [-6.4, 0.8, 0], color=GREEN, stroke_width=4),
                    Line([6.4, 1.05, 0], [6.4, 0.8, 0], color=GREEN, stroke_width=4))
        gen = chip("achaete", GREEN, size=40).move_to([0, 2.0, 0])
        ga = arr([0, 1.62, 0], [0, 1.1, 0], GREEN, 5, 0.2)
        self.play(FadeIn(gen, shift=DOWN * 0.1), Create(br), GrowArrow(ga), run_time=0.6)
        self.at("staged fly embryos")
        ta = arr([-6.0, -2.85, 0], [6.0, -2.85, 0], LG, 4, 0.2)
        tl = lab("time", 28).move_to([5.3, -3.3, 0])
        self.play(GrowArrow(ta), FadeIn(tl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
RCY = 0.15
RSC = 1.05


def time_axis():
    ax = arr([-4.6, -3.05, 0], [4.6, -3.05, 0], LG, 4, 0.2)
    e = lab("early", 28, GOLD).move_to([-5.4, -2.45, 0])
    la = lab("later", 28, GOLD).move_to([5.4, -2.45, 0])
    return ax, e, la


class S14Rg2(SpokenScene):
    def construct(self):
        gen = chip("achaete", GREEN, size=30).move_to([-4.9, 3.2, 0])
        cl = cluster(0, RCY, RSC)
        g = gv(cl)
        ax, e, la = time_axis()
        self.add(gen)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in g], lag_ratio=0.06), FadeIn(ax), run_time=0.5)
        mark = Dot([-4.2, -3.05, 0], radius=0.17, color=GOLD)
        self.at("came on")
        self.play(*[c.animate.set_style(**ST["comp"]) for c in g], FadeIn(e), FadeIn(mark, scale=0.6), run_time=0.7)
        self.at("clusters of a few")
        self.play(*[Indicate(c, color=GREEN, scale_factor=1.06) for c in g], run_time=0.6)
        self.at("later")
        self.play(mark.animate.move_to([4.2, -3.05, 0]), FadeIn(la), run_time=0.6)
        self.at("one cell in each cluster")
        self.play(cl["C"].animate.set_style(**ST["win"]), *[cl[k].animate.set_style(**ST["low"]) for k in "ABDE"],
                  run_time=1.3)
        self.at("much more")
        rna = chip("achaete RNA", GREEN, size=28).move_to([4.9, 2.1, 0])
        a = arr([rna.get_left()[0] - 0.12, 2.0, 0], cl["C"].get_right() + RIGHT * 0.05, GREEN, 4, 0.2)
        self.play(FadeIn(rna, shift=LEFT * 0.2), GrowArrow(a), run_time=0.5)
        # a brightness pulse in the cell's own green (no white flash)
        self.play(cl["C"].animate.set_fill(GREEN, 1.0).scale(1.1), run_time=0.3)
        self.play(cl["C"].animate.set_fill(GREEN, 0.65).scale(1 / 1.1), run_time=0.4)
        self.finish()


class S15Rg3(SpokenScene):
    def construct(self):
        gen = chip("achaete", GREEN, size=30).move_to([-4.9, 3.2, 0])
        cl = cluster(0, RCY, RSC)
        cl["C"].set_style(**ST["win"])
        for k in "ABDE":
            cl[k].set_style(**ST["low"])
        ax, e, la = time_axis()
        rna = chip("achaete RNA", GREEN, size=28).move_to([4.9, 2.1, 0])
        a = arr([rna.get_left()[0] - 0.12, 2.0, 0], cl["C"].get_right() + RIGHT * 0.05, GREEN, 4, 0.2)
        mark = Dot([4.2, -3.05, 0], radius=0.17, color=GOLD)
        self.add(gen, gv(cl), ax, e, la, mark, rna, a)
        self.at("neural progenitor")
        npg = chip("neural progenitor", GREEN, size=28).move_to([4.8, 0.6, 0])
        a2 = arr([npg.get_left()[0] - 0.12, 0.6, 0], cl["C"].get_right() + RIGHT * 0.1 + DOWN * 0.3, GREEN, 4, 0.2)
        self.play(FadeIn(npg, shift=LEFT * 0.2), GrowArrow(a2), run_time=0.8)
        self.at("first state", lead=0.5)
        S = 1.1
        early_c = cluster(-3.5, -0.25, S, "comp")
        late_c = cluster(3.5, -0.25, S, "low")
        late_c["C"].set_style(**ST["win"])
        # old labels leave completely first, then the cluster splits into the early and the later state
        self.play(*[FadeOut(m) for m in (rna, a, npg, a2, gen, ax, e, la, mark)], FadeOut(gv(cl)), run_time=0.35)
        self.play(*[FadeIn(late_c[k]) for k in late_c], *[FadeIn(early_c[k]) for k in early_c], run_time=0.4)
        self.at("competent")
        c1 = chip("competent", GREEN, size=34).move_to([-3.5, 3.25, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.6)
        self.at("the second")
        c2 = chip("determined", GREEN, size=34).move_to([3.5, 3.25, 0])
        self.play(FadeIn(c2, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def nonotch(center=(0.9, 0.7), size=40):
    nn = chip("No Notch", NOT, size=size, pad=0.25).move_to([center[0], center[1], 0])
    x = xmark([nn.get_left()[0] - 0.7, center[1], 0], 0.36)
    return nn, x


def gold_outlines(sw=4):
    ph = VGroup()
    for cl in CLUS:
        i = cl[1]
        px, py, ang = RING[i]
        ph.add(DashedVMobject(Ellipse(width=1.9, height=0.95, color=GOLD, stroke_width=sw).rotate(ang).move_to([px, py, 0]),
                              num_dashes=22))
    return ph


def predict_frame(E=None, k=1.0):
    E = E or Emb()
    pred = T("Predict.", 40, GOLD, TITLE_FONT).move_to([-5.4, 3.4, 0])
    nn, x = nonotch()
    q = T("What happens to the clusters?", 38, TEXT).move_to([1.7, 3.4, 0])
    ph, qm = gold_outlines(), VGroup()
    for cl in CLUS:
        qm.add(T("?", 30, GOLD, TITLE_FONT).move_to(E.inward(cl[1], 0.85)))
    return E, pred, nn, x, q, ph, qm


class S16Predict(SpokenScene):
    def construct(self):
        E, pred, nn, x, q, ph, qm = predict_frame()
        self.add(E.yolk)
        self.play(LaggedStart(*[FadeIn(c) for c in E.c.values()], lag_ratio=0.01), FadeIn(pred, shift=DOWN * 0.1),
                  run_time=1.2)
        self.at("take notch away")
        self.play(FadeIn(nn, shift=DOWN * 0.1), run_time=0.5)
        self.play(Create(x), run_time=0.5)
        self.at("what happens")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.7)
        self.at("clusters")
        self.play(Create(ph), FadeIn(qm), run_time=0.9)
        self.finish()


class S17Pause(NarratedScene):
    def construct(self):
        E, pred, nn, x, q, ph, qm = predict_frame()
        self.add(*E.mobs(caps=False), pred, nn, x, q, ph, qm)
        t = ValueTracker(0.001)
        ctr = np.array([0.0, -0.9, 0.0])
        face = Circle(radius=0.8, stroke_color=TEXT, stroke_width=6).move_to(ctr)
        knob = Rectangle(width=0.26, height=0.14, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(ctr + UP * 0.95)
        self.add(face, knob)
        sec = always_redraw(lambda: Sector(radius=0.8, start_angle=PI / 2, angle=-max(0.001, t.get_value()) * TAU,
                                           arc_center=ctr, color=GOLD, fill_opacity=0.55, stroke_width=0))
        self.add(sec)
        self.play(t.animate.set_value(0.999), run_time=4.1, rate_func=linear)
        sec.clear_updaters()
        # hand over to s18: question, timer and the Notch tag leave, then the embryo settles at the right
        gr = VGroup(E.yolk, *E.c.values(), ph, qm)
        sh = S18_SHIFT
        self.play(*[FadeOut(m) for m in (pred, nn, x, q, face, knob, sec)], run_time=0.3)
        self.play(gr.animate.scale(RK, about_point=CTR).shift(sh), run_time=0.55)
        self.finish()


RK = 0.62


def small_ring(cx, cy):
    return Emb(RK, (cx, cy - RK * (CTR - P0)[1]))


S18_SHIFT = np.array([3.4, 0.35, 0.0]) - CTR


class S18Reveal(SpokenScene):
    def construct(self):
        E, pred, nn, x, q, ph, qm = predict_frame()
        # open exactly where s17 ends: the no-Notch embryo already small on the right
        cx_r, cy = 3.4, 0.35
        gr = VGroup(E.yolk, *E.c.values(), ph, qm)
        gr.scale(RK, about_point=CTR).shift(S18_SHIFT)
        self.add(gr)
        L = small_ring(-cx_r, cy)
        for cl in CLUS:
            for i in cl:
                L.c[i].set_style(**ST["low"])
            L.c[cl[1]].set_style(**ST["win"])
        ln = chip("normal", LG, size=30).move_to([-cx_r, -1.95, 0])
        rn_chip, rn_x = nonotch((cx_r + 0.35, -1.95), 30)
        rn_x.move_to([rn_chip.get_left()[0] - 0.5, -1.95, 0]).scale(0.8)
        self.play(FadeIn(L.yolk), FadeIn(VGroup(*L.c.values())), FadeIn(ln), FadeIn(rn_chip), FadeIn(rn_x), run_time=0.35)
        self.at("clusters still form")
        self.play(*[E.c[i].animate.set_style(**ST["comp"]) for cl in CLUS for i in cl], FadeOut(ph), FadeOut(qm),
                  run_time=0.8)
        self.at("normal places")
        R = small_ring(cx_r, cy)
        outl = VGroup()
        for ring_ in (L, R):
            for cl in CLUS:
                i = cl[1]
                px, py = ring_.pos(i)[:2]
                outl.add(DashedVMobject(Ellipse(width=1.9 * RK, height=0.95 * RK, color=GOLD, stroke_width=3)
                                        .rotate(RING[i][2]).move_to([px, py, 0]), num_dashes=16))
        same = lab("same places", 32, GOLD).move_to([0, -3.0, 0])
        self.play(Create(outl), FadeIn(same, shift=UP * 0.1), run_time=0.9)
        self.at("but high")
        msg = T("high achaete no longer limited to one cell", 32, GREEN).move_to([0, 3.2, 0])
        self.play(*[E.c[i].animate.set_style(**ST["strong"]) for cl in CLUS for i in cl], FadeIn(msg, shift=UP * 0.1),
                  run_time=1.0)
        self.at("no longer limited")
        side = [E.c[i] for cl in CLUS for i in (cl[0], cl[2])]
        self.play(*[m.animate.set_fill(GREEN, 1.0).scale(1.5) for m in side], run_time=0.4)
        self.play(*[m.animate.set_fill(GREEN, 0.9).scale(1 / 1.5) for m in side], run_time=0.5)
        self.finish()


def place_card(cx, cy, title, sub, sub2, color):
    box = RoundedRectangle(corner_radius=0.25, width=6.0, height=2.85, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.12)
    return VGroup(box, T(title, 50, color, TITLE_FONT).shift(UP * 0.85), T(sub, 34, TEXT).shift(DOWN * 0.0),
                  T(sub2, 32, TEXT).shift(DOWN * 0.85)).move_to([cx, cy, 0])


class S19Reveal2(SpokenScene):
    def construct(self):
        E = Emb()
        for cl in CLUS:
            for i in cl:
                E.c[i].set_style(**ST["strong"])
        nn, x = nonotch((-2.3, 3.4), 34)
        x.move_to([nn.get_left()[0] - 0.6, 3.4, 0])
        ph = gold_outlines()
        self.add(*E.mobs(caps=False), nn, x)
        self.at("does not place")
        self.play(Create(ph), Indicate(nn, color=NOT, scale_factor=1.1), run_time=0.9)
        self.at("narrows them")
        n2 = chip("Notch", NOT, size=34, pad=0.25).move_to(nn.get_center())
        self.play(FadeOut(x), FadeOut(nn), FadeIn(n2),
                  LaggedStart(*[AnimationGroup(E.c[cl[1]].animate.set_style(**ST["win"]),
                                               E.c[cl[0]].animate.set_style(**ST["low"]),
                                               E.c[cl[2]].animate.set_style(**ST["low"])) for cl in CLUS],
                              lag_ratio=0.18), run_time=1.5)
        self.at("placing")
        gr = VGroup(E.yolk, *E.c.values(), ph)
        pl = place_card(3.45, 1.75, "Placing", "regulatory DNA", "which cells may", GREEN)
        pk = place_card(3.45, -1.5, "Picking", "Notch", "which one does", NOT)
        self.play(gr.animate.scale(RK, about_point=CTR).shift(np.array([-3.4, 0.2, 0]) - CTR), FadeOut(n2),
                  FadeIn(pl, shift=LEFT * 0.3), run_time=0.8)
        self.at("picking")
        self.play(FadeIn(pk, shift=LEFT * 0.3), run_time=0.6)
        self.at("separate events")
        sep = Line([0.45, 0.125, 0], [6.45, 0.125, 0], color=GOLD, stroke_width=5)
        self.play(Create(sep), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
PZ = [(1.85, GREEN), (-0.1, NOT), (-2.05, LG)]


def card(y, n, color):
    box = RoundedRectangle(corner_radius=0.25, width=11.4, height=1.75, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.10).move_to([0, y, 0])
    num = VGroup(Circle(radius=0.5, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.15),
                 T(str(n), 40, GOLD, TITLE_FONT)).move_to([-4.85, y, 0])
    return box, num


def s19_end():
    """Everything on screen when s19 ends (narrowed embryo at the left, the two cards, the gold line)."""
    E = Emb()
    for cl in CLUS:
        E.c[cl[1]].set_style(**ST["win"])
        E.c[cl[0]].set_style(**ST["low"])
        E.c[cl[2]].set_style(**ST["low"])
    gr = VGroup(E.yolk, *E.c.values(), gold_outlines())
    gr.scale(RK, about_point=CTR).shift(np.array([-3.4, 0.2, 0]) - CTR)
    pl = place_card(3.45, 1.75, "Placing", "regulatory DNA", "which cells may", GREEN)
    pk = place_card(3.45, -1.5, "Picking", "Notch", "which one does", NOT)
    sep = Line([0.45, 0.125, 0], [6.45, 0.125, 0], color=GOLD, stroke_width=5)
    return VGroup(gr, pl, pk, sep)


class S20Puzzles(SpokenScene):
    def construct(self):
        cs = [card(y, n + 1, c) for n, (y, c) in enumerate(PZ)]
        for b, n in cs:
            b.set_stroke(opacity=0.35).set_fill(opacity=0.04)
        old = s19_end()          # open on the last frame of s19 and clear it before the cards come in
        self.add(old)
        hd = T("Three puzzles", 44, GOLD, TITLE_FONT).move_to([0, 3.4, 0])
        self.play(AnimationGroup(FadeOut(old, run_time=0.4),
                                 Succession(Wait(0.25),
                                            AnimationGroup(FadeIn(hd, shift=DOWN * 0.1),
                                                           LaggedStart(*[AnimationGroup(FadeIn(b), GrowFromCenter(n)) for b, n in cs],
                                                                       lag_ratio=0.25), run_time=1.0))))
        self.at("who may")
        y = PZ[0][0]
        t1 = T("Who may become neural?", 42, GREEN).move_to([-3.7, y, 0], aligned_edge=LEFT)
        k1 = lab("MAY", 28, GREEN).move_to([5.2, y, 0], aligned_edge=RIGHT)
        self.play(cs[0][0].animate.set_stroke(opacity=1).set_fill(opacity=0.12), FadeIn(t1, shift=RIGHT * 0.2), FadeIn(k1),
                  run_time=0.7)
        self.at("who does")
        y = PZ[1][0]
        t2 = T("Who does?", 42, NOT).move_to([-3.7, y, 0], aligned_edge=LEFT)
        k2 = lab("DOES", 28, NOT).move_to([5.2, y, 0], aligned_edge=RIGHT)
        self.play(cs[1][0].animate.set_stroke(opacity=1).set_fill(opacity=0.12), FadeIn(t2, shift=RIGHT * 0.2), FadeIn(k2),
                  run_time=0.7)
        self.at("does the logic")
        y = PZ[2][0]
        t3 = T("Does the logic carry over\nto vertebrates?", 34, TEXT, line_spacing=1.1).move_to([-3.7, y, 0], aligned_edge=LEFT)
        self.play(cs[2][0].animate.set_stroke(opacity=1).set_fill(opacity=0.12), FadeIn(t3, shift=RIGHT * 0.2), run_time=0.8)
        self.at("vertebrates")
        k3 = lab("VERTEBRATES", 28, LG).move_to([5.2, y, 0], aligned_edge=RIGHT)
        self.play(FadeIn(k3, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


def s20_end():
    cs = [card(y, n + 1, c) for n, (y, c) in enumerate(PZ)]
    for b, n in cs:
        b.set_stroke(opacity=1).set_fill(opacity=0.12)
    y0, y1, y2 = PZ[0][0], PZ[1][0], PZ[2][0]
    return VGroup(T("Three puzzles", 44, GOLD, TITLE_FONT).move_to([0, 3.4, 0]), *[VGroup(b, n) for b, n in cs],
                  T("Who may become neural?", 42, GREEN).move_to([-3.7, y0, 0], aligned_edge=LEFT),
                  lab("MAY", 28, GREEN).move_to([5.2, y0, 0], aligned_edge=RIGHT),
                  T("Who does?", 42, NOT).move_to([-3.7, y1, 0], aligned_edge=LEFT),
                  lab("DOES", 28, NOT).move_to([5.2, y1, 0], aligned_edge=RIGHT),
                  T("Does the logic carry over\nto vertebrates?", 34, TEXT, line_spacing=1.1).move_to([-3.7, y2, 0], aligned_edge=LEFT),
                  lab("VERTEBRATES", 28, LG).move_to([5.2, y2, 0], aligned_edge=RIGHT))


def s21_end():
    L = cluster(-3.4, 0.4, 0.9, "comp")
    R = cluster(3.4, 0.4, 0.9, "held")
    R["C"].set_style(**ST["win"])
    return VGroup(gv(L), gv(R), T("In the fly", 34, GOLD, TITLE_FONT).move_to([0, 3.3, 0]),
                  T("proneural factors", 34, GREEN).move_to([-3.4, -2.2, 0]),
                  T("say who may", 42, GREEN, TITLE_FONT).move_to([-3.4, -3.0, 0]),
                  T("Notch", 34, NOT).move_to([3.4, -2.2, 0]),
                  T("says who does", 42, NOT, TITLE_FONT).move_to([3.4, -3.0, 0]))


class S21Takeaway(SpokenScene):
    def construct(self):
        L = cluster(-3.4, 0.4, 0.9)
        R = cluster(3.4, 0.4, 0.9)
        old = s20_end()      # open on the last frame of s20; it fades while the two clusters come up
        self.add(old)
        self.play(FadeOut(old, run_time=0.5),
                  Succession(Wait(0.2), LaggedStart(*[FadeIn(c) for c in list(L.values()) + list(R.values())], lag_ratio=0.05,
                                                   run_time=0.7)))
        self.at("in the fly")
        hd = T("In the fly", 34, GOLD, TITLE_FONT).move_to([0, 3.3, 0])
        self.play(FadeIn(hd, shift=DOWN * 0.1), run_time=0.6)
        self.at("factors say")
        n1 = T("proneural factors", 34, GREEN).move_to([-3.4, -2.2, 0])
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.6)
        self.at("cells may become neural")
        r1 = T("say who may", 42, GREEN, TITLE_FONT).move_to([-3.4, -3.0, 0])
        self.play(*[c.animate.set_style(**ST["comp"]) for c in L.values()], FadeIn(r1, shift=UP * 0.1), run_time=0.9)
        self.at("notch says")
        n2 = T("Notch", 34, NOT).move_to([3.4, -2.2, 0])
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.6)
        self.at("which one does")
        r2 = T("says who does", 42, NOT, TITLE_FONT).move_to([3.4, -3.0, 0])
        self.play(R["C"].animate.set_style(**ST["win"]), *[R[k].animate.set_style(**ST["held"]) for k in "ABDE"],
                  FadeIn(r2, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S22End(EndCard):
    LINE = "Proneural factors say which cells may.\nNotch says which one does."

    def construct(self):
        # open on the last frame of s21, clear it, and bring the take-home line in with no blank beat
        old = s21_end()
        self.add(old)
        line = T(self.LINE, size=40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.4)
        self.play(AnimationGroup(FadeOut(old, run_time=0.5),
                                 Succession(Wait(0.25), FadeIn(line, shift=UP * 0.15, run_time=0.45))))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
