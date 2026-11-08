"""Chapter 1, The Muscle Proposes, the Nerve Disposes (Building the Neuromuscular Junction)  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole chapter series; taken from scenes.old.py)
  BLUE   = acetylcholine receptors and their clusters (one cluster glyph all chapter: a triad of three dots)
  PURPLE = the motor neuron: axon and nerve terminal
  YELLOW = agrin (the nerve's clustering signal), always the same wavy strand
  TEAL   = Lrp4 (the agrin receptor on the muscle)
  GREEN  = MuSK, Dok7 and "protect / facilitate" (the shield)
  ORANGE = rapsyn (the scaffold under the receptors)
  RED    = acetylcholine, dispersal, "not there / not needed / lost"
  GREY   = muscle membrane and fibre, basal lamina, labels
  GOLD   = dates and the remembered old synaptic site (history marks only)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

NERVE, RECEPTOR, AGRIN, LRP4, MUSK, RAPSYN, ACH = PURPLE, BLUE, YELLOW, TEAL, GREEN, ORANGE, RED


# ---------------------------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cdim(c, o=0.45):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def strike(mob, color=RED, w=7):
    wd, h = mob.width, mob.height
    c = mob.get_center()
    return Line(c + np.array([-wd / 2, -h / 2, 0]), c + np.array([wd / 2, h / 2, 0]), color=color, stroke_width=w)


def arr(a, b, color=GREY, w=7, tip=0.28):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def cluster(x, y, s=2.0, color=RECEPTOR):
    """THE receptor cluster glyph for the whole chapter: a tight triad of three dots."""
    r = 0.10 * s
    off = 0.17 * s
    pts = [(-off, -off * 0.6), (off, -off * 0.6), (0, off * 0.9)]
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x + a, y + b, 0])
                    for a, b in pts])


DOT_R = 0.19


def rdot(x, y, r=DOT_R, color=RECEPTOR):
    return Dot([x, y, 0], radius=r, color=color)


def strand(cx, cy, L=2.2, color=AGRIN, w=8):
    """agrin: the same short wavy strand everywhere in the chapter"""
    s = ParametricFunction(lambda t: np.array([t, 0.1 * np.sin(t * 9.0), 0]), t_range=[-L / 2, L / 2],
                           color=color, stroke_width=w)
    return s.move_to([cx, cy, 0])


def lt(text, size, color, x, y, edge=LEFT, **kw):
    """a label whose left (or other) edge sits at x"""
    return T(text, size, color, **kw).move_to([x, y, 0], aligned_edge=edge)


# ---------------------------------------------------------------------------------------------
# fibre view: the muscle fibre seen from above, the nerve ending on top of it
# ---------------------------------------------------------------------------------------------
FIB_W, FIB_H, FIB_TOP = 12.6, 4.4, 0.8


def fibre(fill=0.12):
    return RoundedRectangle(corner_radius=0.25, width=FIB_W, height=FIB_H, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=fill).move_to([0, FIB_TOP - FIB_H / 2, 0])


def sheath():
    r = RoundedRectangle(corner_radius=0.25, width=FIB_W, height=FIB_H, stroke_color=GREY, stroke_width=4,
                         fill_opacity=0).move_to([0, FIB_TOP - FIB_H / 2, 0])
    return DashedVMobject(r, num_dashes=70)


def axon_line(x=0.0, top=3.8):
    return Line([x, top, 0], [x, 1.7, 0], color=NERVE, stroke_width=16)


def bulb(x=0.0):
    return Ellipse(width=3.0, height=1.0, stroke_color=NERVE, stroke_width=3, fill_color=NERVE,
                   fill_opacity=0.55).move_to([x, 1.2, 0])


def patch_pos():
    pts = []
    for y, n in [(-0.2, 7), (-0.62, 6), (-1.04, 5)]:
        for k in range(n):
            pts.append(((k - (n - 1) / 2) * 0.44, y))
    return pts  # 18 points


SPARSE = [(-5.5, -1.0), (-4.6, -2.7), (-3.0, -1.9), (-2.2, -3.1), (-1.3, -2.3),
          (1.9, -2.3), (3.3, -1.0), (4.2, -2.9), (5.3, -1.9), (5.6, -3.2)]


def home_pos():
    return patch_pos() + SPARSE  # 28 points


def even_pos():
    rng = np.random.RandomState(3)
    pts = []
    for r in range(4):
        for c in range(7):
            pts.append((-5.4 + 1.8 * c + rng.uniform(-0.25, 0.25), -0.85 - 0.78 * r + rng.uniform(-0.1, 0.1)))
    perm = np.random.RandomState(8).permutation(len(pts))
    return [pts[i] for i in perm]


def make_dots(positions):
    return VGroup(*[rdot(x, y) for x, y in positions])


def fibre_with_dots(scene, dots=True, nerve=True):
    fib = fibre()
    scene.add(fib)
    ax = bu = None
    if nerve:
        ax, bu = axon_line(0.0), bulb(0.0)
        scene.add(ax, bu)
    d = None
    if dots:
        d = make_dots(home_pos())
        scene.add(d)
    return fib, ax, bu, d


# receptor clusters (triads) on the fibre, used from s18 on
CL_POS = [(0.0, -0.9), (-2.6, -1.4), (2.7, -1.3), (-5.0, -1.7), (5.1, -1.8), (-1.4, -2.6), (1.5, -2.7),
          (-3.9, -3.0), (3.9, -3.1), (-5.3, -3.0)]


def cl_group(s=2.0):
    return VGroup(*[cluster(x, y, s) for x, y in CL_POS])


# ---------------------------------------------------------------------------------------------
# cross-section view: terminal, basal lamina, muscle membrane, inside of the fibre
# ---------------------------------------------------------------------------------------------
MUSK_X, LRP_X = 0.6, -1.8
LAM_Y, MEM_Y = 2.15, 0.5
STRAND_HOME = (2.6, LAM_Y)


def cs_term():
    term = RoundedRectangle(corner_radius=0.3, width=8.4, height=1.0, stroke_color=NERVE, stroke_width=3,
                            fill_color=NERVE, fill_opacity=0.35).move_to([0, 3.3, 0])
    return term, T("nerve terminal", 30, NERVE).move_to(term)


def cs_muscle():
    mem = RoundedRectangle(corner_radius=0.1, width=13.2, height=0.4, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.45).move_to([0, MEM_Y, 0])
    inter = Rectangle(width=13.2, height=4.1, stroke_width=0, fill_color=GREY, fill_opacity=0.08).move_to([0, -1.55, 0])
    return inter, mem


def cs_bl():
    return (DashedLine([-6.6, LAM_Y, 0], [6.6, LAM_Y, 0], color=GREY, stroke_width=3, dash_length=0.18),
            T("basal lamina", 28, GREY).move_to([5.3, 2.52, 0]))


def cs_labels():
    return (lt("muscle membrane", 26, GREY, -6.6, 1.0), lt("inside the\nmuscle fibre", 26, GREY, -6.5, -0.95, line_spacing=0.9))


def musk_block(fill=0.3):
    return RoundedRectangle(corner_radius=0.18, width=1.0, height=3.2, stroke_color=MUSK, stroke_width=3,
                            fill_color=MUSK, fill_opacity=fill).move_to([MUSK_X, -0.1, 0])


def _lrp_pts():
    return [(-1.3, 1.9), (1.3, 1.9), (1.3, 0.7), (0.35, 0.7), (0.35, -0.5), (-0.35, -0.5), (-0.35, 0.7), (-1.3, 0.7)]


def lrp4_block():
    p = Polygon(*[[LRP_X + a, b, 0] for a, b in _lrp_pts()], stroke_color=LRP4, stroke_width=3, fill_color=LRP4,
                fill_opacity=0.45)
    return p.round_corners(0.1)


def lrp4_slot():
    p = Polygon(*[[LRP_X + a, b, 0] for a, b in _lrp_pts()], stroke_color=TEXT, stroke_width=4, fill_opacity=0)
    return DashedVMobject(p.round_corners(0.1), num_dashes=70)


def musk_labels():
    return (T("MuSK", 36, MUSK).move_to([MUSK_X, -2.25, 0]),
            T("receptor tyrosine kinase", 28, MUSK).move_to([MUSK_X, -2.85, 0]))


def lrp_label():
    return T("Lrp4", 38, LRP4, weight=BOLD).move_to([LRP_X, 1.3, 0])


def rec_block(x):
    return RoundedRectangle(corner_radius=0.12, width=0.8, height=1.4, stroke_color=RECEPTOR, stroke_width=3,
                            fill_color=RECEPTOR, fill_opacity=0.55).move_to([x, 0.45, 0])


def rapsyn_bar(w=3.6, cx=4.1):
    return RoundedRectangle(corner_radius=0.1, width=w, height=0.3, stroke_color=RAPSYN, stroke_width=3,
                            fill_color=RAPSYN, fill_opacity=0.65).move_to([cx, -0.35, 0])


def build_cs(scene, bl=True, labels=True, strand_on=True):
    """the base stage; returns the objects so a scene can animate them"""
    inter, mem = cs_muscle()
    term, tl = cs_term()
    d = dict(inter=inter, mem=mem, term=term, tl=tl)
    base = [inter, mem, term, tl]
    if bl:
        b, bll = cs_bl()
        base += [b, bll]
        d.update(bl=b, bll=bll)
    if labels:
        m1, m2 = cs_labels()
        base += [m1, m2]
        d.update(ml1=m1, ml2=m2)
    scene.add(*base)
    if strand_on:
        st = strand(*STRAND_HOME)
        scene.add(st)
        d["st"] = st
    return d


def cs_full(scene):
    """the finished junction of s15: Lrp4, activated and boosted MuSK with Dok7, rapsyn under three receptors"""
    d = build_cs(scene, strand_on=False)
    lr, mk = lrp4_block(), musk_block(0.9)
    st = strand(LRP_X, 2.05)
    ll = lrp_label()
    m1, m2 = musk_labels()
    dok = bchip("Dok7", MUSK, 32).move_to([-0.95, -1.0, 0])
    tag, tagt = phos_tag()
    recs = VGroup(*[rec_block(x) for x in (3.0, 4.1, 5.2)])
    rl = T("acetylcholine receptors", 26, RECEPTOR).move_to([4.1, 1.75, 0])
    rap = rapsyn_bar()
    rapl = T("rapsyn", 34, RAPSYN).move_to([4.1, -0.95, 0])
    ar = arr([MUSK_X + 0.55, -0.35, 0], [2.3, -0.35, 0], MUSK, w=5, tip=0.2)
    parts = VGroup(lr, mk, st, ll, m1, m2, dok, tag, tagt, recs, rl, rap, rapl, ar)
    scene.add(parts)
    d.update(parts=parts)
    return d


def phos_tag():
    c = Circle(radius=0.26, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([1.75, -1.35, 0])
    p = T("P", 26, TEXT, weight=BOLD).move_to(c)
    t = lt("activated", 26, TEXT, 2.15, -1.35)
    return VGroup(c, p), t


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Building the Neuromuscular Junction: Agrin, Lrp4 and MuSK"
    TITLE = "The Muscle Proposes, the Nerve Disposes"

    def construct(self):
        # whole title legible from the first half second; no slow write-on
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(g), run_time=0.35)
        self.wait(2.2)
        self.play(FadeOut(g), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mouse():
    """one smooth outline (no overlapping parts): a newborn mouse in side view, facing left"""
    sty = dict(stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.16)
    pts = [(-2.45, -0.4), (-2.0, 0.1), (-1.6, 0.5), (-1.3, 1.05), (-0.95, 0.55), (-0.3, 0.85), (0.8, 1.0),
           (1.8, 0.65), (2.3, -0.1), (2.1, -0.8), (1.5, -0.95), (0.9, -1.05), (-0.5, -1.05), (-1.2, -1.0),
           (-1.8, -0.9), (-2.2, -0.75)]
    body = VMobject(**sty)
    body.set_points_smoothly([np.array([x, y, 0]) for x, y in pts] + [np.array([pts[0][0], pts[0][1], 0])])
    eye = Dot([-1.85, 0.05, 0], radius=0.09, color=GREY)
    tail = ParametricFunction(lambda t: np.array([2.25 + 1.9 * t, -0.05 + 0.5 * np.sin(3 * PI * t) * t, 0]),
                              t_range=[0, 1], color=GREY, stroke_width=5)
    g = VGroup(body, eye, tail)
    return g.scale(1.85).move_to([0, 0.25, 0])


class S01Q(SpokenScene):
    def construct(self):
        m = mouse()
        bx = 0.0
        ml = T("newborn mouse", 32, GREY).move_to([bx, -2.25, 0])
        self.at("newborn mouse")
        self.play(Create(m), FadeIn(ml), run_time=1.0)
        musk = bchip("MuSK", MUSK, 36).move_to([4.9, 2.5, 0])
        self.at("lacks the muscle")
        self.play(FadeIn(musk, shift=DOWN * 0.2), run_time=0.5)
        bar = strike(musk)
        cb = T("cannot breathe", 42, RED, weight=BOLD).move_to([bx, -3.0, 0])
        self.at("cannot breathe")
        self.play(Create(bar), *cdim(musk), FadeIn(cb), run_time=0.6)
        # the diaphragm: the fibre, with the motor axon arriving
        fib = fibre()
        ax = axon_line(0.0)
        axl = lt("motor axon", 30, NERVE, 0.7, 3.4)
        self.at("motor axons")
        self.play(FadeOut(m), FadeOut(ml), FadeOut(musk), FadeOut(bar), FadeOut(cb), FadeIn(fib), Create(ax), FadeIn(axl),
                  run_time=1.0)
        bu = bulb(0.0)
        self.at("reach the")
        self.play(FadeIn(bu, scale=0.8), run_time=0.4)
        dl = lt("diaphragm muscle fibre", 30, GREY, -6.0, -3.2)
        q = T("?", 130, TEXT, weight=BOLD).move_to([2.5, 1.85, 0])
        self.at("diaphragm")
        self.play(FadeIn(dl), FadeIn(q, scale=1.4), run_time=0.5)
        nj = T("no junction", 44, RED, weight=BOLD).move_to([-3.3, 1.9, 0])
        self.at("so why")
        self.play(FadeIn(nj, shift=RIGHT * 0.2), run_time=0.5)
        self.finish()


class S02Built(SpokenScene):
    def construct(self):
        fib, ax, bu = fibre(), axon_line(0.0), bulb(0.0)
        self.add(fib, ax, bu)
        tx = T("touching is not\na synapse", 46, TEXT, line_spacing=0.9).move_to([-3.6, 2.3, 0])
        self.add(tx)
        ring = Circle(radius=0.3, stroke_color=GREY, stroke_width=5).move_to([0, 0.75, 0])
        self.add(ring)
        self.at("touches a target")
        self.play(Indicate(bu, color=NERVE, scale_factor=1.1), ring.animate.scale(5).set_stroke(opacity=0.0),
                  run_time=0.9)
        self.finish()


class S03Sort(SpokenScene):
    def construct(self):
        fib, ax, bu = fibre(), axon_line(0.0), bulb(0.0)
        self.add(fib, ax, bu)
        hp = home_pos()
        patch = make_dots(hp[:18])
        sparse = make_dots(hp[18:])
        self.at("mature junction")
        self.play(Indicate(bu, color=NERVE, scale_factor=1.1), run_time=0.8)
        leg = rdot(-6.2, 2.3)
        legt = T("acetylcholine receptor", 30, RECEPTOR).next_to(leg, RIGHT, buff=0.25)
        self.at("acetylcholine receptors")
        self.play(FadeIn(leg, scale=1.5), FadeIn(legt), run_time=0.5)
        self.at("packed under")
        pk = T("packed", 30, RECEPTOR).move_to([0, -1.7, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in patch], lag_ratio=0.03), FadeIn(pk), run_time=0.8)
        nl = lt("nerve ending", 30, NERVE, 2.3, 1.3)
        self.at("nerve ending")
        self.play(FadeIn(nl), run_time=0.4)
        self.at("along the rest")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in sparse], lag_ratio=0.1), run_time=1.3)
        sp = T("sparse", 34, RECEPTOR).move_to([-4.0, -0.45, 0])
        self.at("sparse")
        self.play(FadeIn(sp), run_time=0.4)
        self.finish()


class S04Q(SpokenScene):
    def construct(self):
        fib, ax, bu, dots = fibre_with_dots(self)
        home, even = home_pos(), even_pos()
        self.at("sorting problem")
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dots, even)], run_time=1.3)
        q1 = lt("Where do they go?", 40, TEXT, -6.5, 2.9)
        q2 = lt("Who tells them?", 40, TEXT, -6.5, 2.0)
        self.add(q1, q2)
        self.at("where do the receptors go")
        # the dots hover, unsure, while the question is on screen
        rng = np.random.RandomState(5)
        self.play(*[d.animate.shift([rng.uniform(-0.25, 0.25), rng.uniform(-0.15, 0.15), 0]) for d in dots],
                  run_time=1.0, rate_func=there_and_back)
        self.at("who tells them")
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dots, home)], run_time=0.6)
        self.wait(3.3)
        self.finish()


class S05Frog(SpokenScene):
    def construct(self):
        fib, ax, bu, _ = fibre_with_dots(self, dots=False)
        fl = lt("frog muscle fibre", 30, GREY, -6.0, -3.2)
        self.at("frog muscle")
        self.play(FadeIn(fl), run_time=0.5)
        yr = lt("1978", 80, GOLD, -6.5, 3.1, font=TITLE_FONT)
        nm = lt("Sanes, Marshall\nand McMahan", 28, GREY, -6.5, 1.75, line_spacing=0.9)
        self.at("in 1978")
        self.play(FadeIn(yr, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(nm), run_time=0.5)
        self.at("fibers and nerve")
        self.play(Indicate(fib, color=GREY, scale_factor=1.02), Indicate(bu, color=NERVE, scale_factor=1.12), run_time=1.0)
        self.at("made to degenerate")
        self.play(fib.animate.set_stroke(RED).set_fill(RED, 0.3), bu.animate.set_stroke(RED).set_fill(RED, 0.55),
                  ax.animate.set_color(RED), fl.animate.set_color(RED), run_time=0.8)
        self.play(fib.animate.set_opacity(0.1), ax.animate.set_opacity(0.1), bu.animate.set_opacity(0.1), FadeOut(fl),
                  run_time=0.9)
        self.finish()


def old_site_mark():
    return Rectangle(width=2.4, height=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([0, 0.58, 0])


def leader(a, b, color=GREY, w=3):
    return Line(a, b, color=color, stroke_width=w)


class S06Sheath(SpokenScene):
    def construct(self):
        sh = sheath()
        lab = T("empty sheath of basal lamina", 28, GREY).move_to([0, -2.9, 0])
        ld = leader([0, -3.12, 0], [0, -3.57, 0])
        self.play(Create(sh), run_time=0.7)
        self.play(FadeIn(lab), Create(ld), run_time=0.4)
        mark = old_site_mark()
        mk_l = lt("old synaptic site", 28, GOLD, 1.9, -0.2)
        mk_d = leader([1.25, 0.52, 0], [1.85, -0.1, 0], GOLD)
        self.wait(0.9)
        self.play(FadeIn(mark, scale=1.4), FadeIn(mk_l), Create(mk_d), run_time=0.6)
        ax = axon_line(0.0)
        rl = lt("regenerating axon", 30, NERVE, 0.6, 2.9)
        self.at("regenerating axons")
        self.play(Create(ax), FadeIn(rl), run_time=2.0)
        bu = bulb(0.0)
        self.at("old synaptic")
        self.play(FadeIn(bu, scale=0.8), run_time=0.5)
        self.finish()


class S07Mark(SpokenScene):
    def construct(self):
        sh = sheath()
        ax, bu = axon_line(0.0), bulb(0.0)
        mark = old_site_mark()
        mk_l = lt("old synaptic site", 28, GOLD, 1.9, -0.2)
        mk_d = leader([1.25, 0.52, 0], [1.85, -0.1, 0], GOLD)
        lab = T("empty sheath of basal lamina", 28, GREY).move_to([0, -2.9, 0])
        ld = leader([0, -3.12, 0], [0, -3.57, 0])
        rl = lt("regenerating axon", 30, NERVE, 0.6, 2.9)
        self.add(sh, ax, bu, mark, mk_l, mk_d, lab, ld, rl)
        lab2 = T("basal lamina: the matrix around each fibre", 28, GREY).move_to([0, -2.9, 0])
        self.at("basal lamina")
        self.play(ReplacementTransform(lab, lab2), FadeOut(rl), run_time=0.7)

        def pulse():
            ring = Circle(radius=0.3, stroke_color=GOLD, stroke_width=6).move_to([0, 0.58, 0])
            return ring

        r1 = pulse()
        self.add(r1)
        self.at("remembered")
        self.play(Indicate(mark, color=GOLD, scale_factor=1.5), r1.animate.scale(5).set_stroke(opacity=0.0), run_time=0.8)
        r2 = pulse()
        self.add(r2)
        self.at("where the synapse")
        self.play(r2.animate.scale(5).set_stroke(opacity=0.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def ray():
    body = Polygon([-2.6, 0, 0], [0, 1.9, 0], [2.6, 0, 0], [0, -1.7, 0], stroke_color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=0.12).round_corners(0.6)
    tail = Line([0, -1.6, 0], [0, -2.8, 0], color=GREY, stroke_width=5)
    g = VGroup(body, tail)
    return g.shift(np.array([-4.1, 0.3, 0]))


class S08Agrin(SpokenScene):
    def construct(self):
        ys = [2.0, 0.65, -0.7, -2.05]
        gl = T("McMahan's group", 30, GREY).move_to([-4.1, 3.3, 0])
        r = ray()
        organs = VGroup(*[Ellipse(width=1.4, height=1.0, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                                  fill_opacity=0.3).move_to([x, 0.9, 0]) for x in (-5.0, -3.2)])
        self.play(FadeIn(r), FadeIn(organs), FadeIn(gl), run_time=0.6)
        ol = T("electric organ", 26, TEXT).move_to([-4.1, -0.3, 0])
        self.at("electric organ")
        self.play(FadeIn(ol), Indicate(organs, color=TEXT, scale_factor=1.1), run_time=0.7)
        rl = T("Torpedo ray", 30, GREY).move_to([-4.1, -3.2, 0])
        self.at("ray torpedo")
        self.play(FadeIn(rl), FadeOut(gl), run_time=0.4)
        chips = VGroup(*[chip(str(i + 1), TEXT, size=30).move_to([0.4, y, 0]) for i, y in enumerate(ys)])
        fl = T("fractions", 30, TEXT).move_to([0.4, 3.1, 0])
        fan = VGroup(*[arr([-1.4, 0.3, 0], [-0.1, y, 0], GREY, w=5, tip=0.2) for y in ys])
        self.wait(0.3)
        self.play(LaggedStart(*[GrowArrow(a) for a in fan], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(c, shift=LEFT * 0.6) for c in chips], lag_ratio=0.12), FadeIn(fl), run_time=1.0)
        cells = VGroup(*[Ellipse(width=3.0, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                 fill_opacity=0.14).move_to([4.6, y, 0]) for y in ys])
        cl = T("cultured muscle cells", 26, GREY).move_to([4.5, 3.1, 0])
        arrows = VGroup(*[arr([1.0, y, 0], [3.0, y, 0], GREY, w=5, tip=0.22) for y in ys])
        yr = T("1987", 56, GOLD, font=TITLE_FONT).move_to([-1.4, -3.2, 0])
        dots = VGroup(*[cluster(4.6 + dx, -2.05, 0.85) for dx in (-0.85, 0, 0.85)])
        rcl = T("receptor clusters", 30, RECEPTOR).move_to([4.6, -3.2, 0])
        self.at("in 1987")
        self.play(FadeIn(yr), FadeIn(cells), FadeIn(cl), run_time=0.3)
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.35)
        self.add(dots, rcl)
        self.play(chips[3][0].animate.set_stroke(AGRIN, 4), arrows[3].animate.set_color(AGRIN), run_time=0.2)
        ag = bchip("agrin", AGRIN, 30).move_to([0.4, -2.05, 0])
        agt = T("agrin", 56, AGRIN, font=TITLE_FONT).move_to([1.4, -3.2, 0])
        self.at("they named the")
        self.play(FadeOut(chips[3]), FadeIn(ag), FadeIn(agt), run_time=0.25)
        self.wait(1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Neural(SpokenScene):
    def construct(self):
        d = build_cs(self, bl=False, labels=False, strand_on=False)
        bl, bll = cs_bl()
        # lamina line and the stage are on screen from the first frame
        self.add(bl)
        st = strand(STRAND_HOME[0], 2.9, L=3.5, w=11)
        ag = T("neural agrin", 34, AGRIN).move_to([STRAND_HOME[0], 1.55, 0])
        self.add(st)
        self.at("send")
        self.play(st.animate.move_to([STRAND_HOME[0], 2.55, 0]), FadeIn(ag), run_time=0.65)
        self.at("into the basal lamina")
        self.play(st.animate.move_to([*STRAND_HOME, 0]), FadeIn(bll), run_time=0.65)
        self.finish()


class S10Musk(SpokenScene):
    def construct(self):
        d = build_cs(self, labels=False)
        mk = musk_block()
        ml, sub = musk_labels()
        self.at("lacking musk")
        self.play(FadeIn(mk, scale=0.7), FadeIn(ml), run_time=0.7)
        m1, m2 = cs_labels()
        self.at("a muscle receptor")
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.4)
        self.at("receptor tyrosine")
        self.play(FadeIn(sub), run_time=0.5)
        box = RoundedRectangle(corner_radius=0.15, width=3.6, height=3.3, stroke_color=TEXT, stroke_width=3,
                               fill_color=BG, fill_opacity=1).move_to([5.0, -1.8, 0])
        t0 = T("MuSK-null mouse", 26, TEXT).move_to([5.0, -0.5, 0])
        tt = RoundedRectangle(corner_radius=0.1, width=3.0, height=0.45, stroke_color=NERVE, stroke_width=3,
                              fill_color=NERVE, fill_opacity=0.35).move_to([5.0, -1.2, 0])
        mm = RoundedRectangle(corner_radius=0.08, width=3.2, height=0.25, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=0.45).move_to([5.0, -2.0, 0])
        nj = T("no junction", 32, RED, weight=BOLD).move_to([5.0, -2.85, 0])
        inset = VGroup(box, t0, tt, mm, nj)
        self.at("make no junctions")
        self.play(FadeIn(inset, shift=UP * 0.2), run_time=0.6)
        self.at("agrin acts")
        self.play(FadeOut(inset), Indicate(d["st"], color=AGRIN, scale_factor=1.3), run_time=0.7)
        cx = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=4.9, height=3.6, stroke_color=TEXT,
                                             stroke_width=4).move_to([-0.95, -0.05, 0]), num_dashes=48)
        cxl = T("complex", 30, TEXT).move_to([-1.9, -0.95, 0])
        self.at("a complex that")
        self.play(Create(cx), FadeIn(cxl), run_time=0.8)
        self.at("contains musk")
        self.play(Indicate(mk, color=MUSK, scale_factor=1.12), run_time=0.7)
        self.wait(0.3)
        self.play(FadeOut(cx), FadeOut(cxl), run_time=0.5)
        self.finish()


def q_text():
    return T("What kind of molecule would you look for?", 30, TEXT).move_to([0, -3.55, 0])


def question_frame(scene):
    d = build_cs(scene)
    mk = musk_block()
    ml, sub = musk_labels()
    gap = lrp4_slot()
    qm = T("?", 80, TEXT, weight=BOLD).move_to([LRP_X, 1.3, 0])
    qt = q_text()
    scene.add(mk, ml, sub, gap, qm, qt)
    d.update(mk=mk, ml=ml, sub=sub, gap=gap, qm=qm, qt=qt)
    return d


class S11Q(SpokenScene):
    def construct(self):
        d = build_cs(self)
        mk = musk_block()
        ml, sub = musk_labels()
        self.add(mk, ml, sub)
        st = d["st"]
        self.at("does not")
        self.play(st.animate.move_to([MUSK_X, 1.85, 0]), run_time=0.8)
        nb = lt("does not bind", 32, RED, 1.35, 1.0)
        self.play(FadeIn(nb), st.animate.shift(UP * 0.3), run_time=0.4)
        self.wait(0.3)
        self.play(st.animate.move_to([*STRAND_HOME, 0]), run_time=0.7)
        gap = lrp4_slot()
        qm = T("?", 80, TEXT, weight=BOLD).move_to([LRP_X, 1.3, 0])
        qt = q_text()
        self.at("what kind of")
        self.play(FadeOut(nb), Create(gap), FadeIn(qm, scale=1.3), run_time=0.8)
        self.at("would you look")
        self.play(FadeIn(qt, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        question_frame(self)
        self.finish()


class S13Lrp4(SpokenScene):
    def construct(self):
        d = question_frame(self)
        lr = lrp4_block()
        self.at("muscle surface")
        self.play(FadeOut(d["gap"]), FadeOut(d["qm"]), FadeOut(d["qt"]), FadeIn(lr, scale=0.6), run_time=0.9)
        self.at("binds agrin")
        self.play(d["st"].animate.move_to([LRP_X, 2.05, 0]), run_time=0.8)
        link = DoubleArrow([LRP_X + 0.4, -0.15, 0], [MUSK_X - 0.55, -0.15, 0], color=TEXT, stroke_width=6, tip_length=0.2,
                           buff=0.0)
        self.at("and joins")
        self.play(GrowFromCenter(link), Indicate(d["mk"], color=MUSK, scale_factor=1.05), run_time=0.8)
        ll = lrp_label()
        self.at("lrp4")
        self.play(FadeIn(ll), Indicate(lr, color=LRP4, scale_factor=1.06), run_time=0.8)
        self.finish()


class S14Test(SpokenScene):
    def construct(self):
        yr = T("2008", 64, GOLD, font=TITLE_FONT).move_to([0, 3.15, 0])
        cL, cR = np.array([-3.4, -0.1, 0]), np.array([3.4, -0.1, 0])
        left = Circle(radius=1.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to(cL)
        right = Circle(radius=1.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to(cR)
        self.play(FadeIn(yr), FadeIn(left), FadeIn(right), run_time=0.6)
        ll = T("non-muscle cell", 28, GREY).move_to(cL + DOWN * 2.35)
        lr = T("non-muscle cell", 28, GREY).move_to(cR + DOWN * 2.35)
        self.at("not muscle")
        self.play(FadeIn(ll), FadeIn(lr), run_time=0.4)

        def three(c, rot=0.0):
            return VGroup(*[strand(c[0] + dx, c[1] + 2.5, L=1.1).rotate(a) for dx, a in [(-1.5, 0.3), (0.0, 0.0), (1.5, -0.3)]])

        def slide_off(g, direction):
            return g.animate.shift(DOWN * 1.0 + RIGHT * direction * 2.4).rotate(direction * -0.9).set_opacity(0.0)

        fl, fr = three(cL), three(cR)
        self.at("neural agrin")
        self.play(FadeIn(fl, shift=DOWN * 0.3), FadeIn(fr, shift=DOWN * 0.3), run_time=0.3)
        self.play(fl.animate.shift(DOWN * 0.9), fr.animate.shift(DOWN * 0.9), run_time=0.4)
        self.play(slide_off(fl, -1), slide_off(fr, 1), run_time=0.6)
        self.remove(fl, fr)
        blocks = VGroup()
        for ang in (55, 90, 125):
            a = np.deg2rad(ang)
            p = cR + 1.7 * np.array([np.cos(a), np.sin(a), 0]) + 0.3 * np.array([np.cos(a), np.sin(a), 0])
            b = RoundedRectangle(corner_radius=0.08, width=0.45, height=0.9, stroke_color=LRP4, stroke_width=3,
                                 fill_color=LRP4, fill_opacity=0.55).rotate(a - PI / 2).move_to(p)
            blocks.add(b)
        lr2 = T("non-muscle cell + Lrp4", 28, TEAL).move_to(cR + DOWN * 2.35)
        self.at("they are given")
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in blocks], lag_ratio=0.1), ReplacementTransform(lr, lr2),
                  run_time=0.4)
        # the same agrin again: plain cell lets it go, Lrp4 cell holds it
        fl2 = three(cL)
        held = VGroup()
        for ang in (55, 90, 125):
            a = np.deg2rad(ang)
            p = cR + 2.55 * np.array([np.cos(a), np.sin(a), 0])
            held.add(strand(p[0], p[1], L=1.0).rotate(a - PI / 2))
        comers = VGroup(*[h.copy().shift(UP * 1.0).set_opacity(0.0) for h in held])
        self.add(comers)
        self.at("lrp4")
        self.play(FadeIn(fl2, shift=DOWN * 0.2), *[m.animate.become(h) for m, h in zip(comers, held)], run_time=0.8)
        nh = T("no agrin held", 32, RED, weight=BOLD).move_to(cL + DOWN * 3.0)
        hh = T("holds agrin", 32, AGRIN, weight=BOLD).move_to(cR + DOWN * 3.0)
        self.play(slide_off(fl2, -1), FadeIn(nh), FadeIn(hh), run_time=0.5)
        self.finish()


class S15Dok(SpokenScene):
    def construct(self):
        d = build_cs(self, strand_on=False)
        lr, mk = lrp4_block(), musk_block()
        st = strand(LRP_X, 2.05)
        ll = lrp_label()
        m1, m2 = musk_labels()
        self.add(lr, mk, st, ll, m1, m2)
        dok = bchip("Dok7", MUSK, 32).move_to([-3.3, -1.0, 0])
        self.at("doc7")
        self.play(FadeIn(dok), run_time=0.15)
        self.play(dok.animate.move_to([-0.95, -1.0, 0]), run_time=0.55)
        tag, tagt = phos_tag()
        self.at("binds activated")
        self.play(FadeIn(tag, scale=0.4), FadeIn(tagt), run_time=0.5)
        glow = RoundedRectangle(corner_radius=0.2, width=1.5, height=3.45, stroke_color=MUSK, stroke_width=14,
                                fill_opacity=0).move_to([MUSK_X, -0.1, 0]).set_stroke(opacity=0.0)
        self.add(glow)
        self.at("boosts it")
        self.play(mk.animate.set_fill(MUSK, 0.9), glow.animate.set_stroke(opacity=0.4), run_time=0.8)
        self.play(Indicate(mk, color=MUSK, scale_factor=1.06), run_time=0.5)
        recs = VGroup(*[rec_block(x) for x in (2.8, 4.4, 6.0)])
        rl = T("acetylcholine receptors", 26, RECEPTOR).move_to([4.4, 1.75, 0])
        self.at("wraps in")
        self.play(FadeIn(recs, shift=UP * 0.2), FadeIn(rl), run_time=0.7)
        rap = rapsyn_bar(w=3.9, cx=4.4)
        rapl = T("rapsyn", 34, RAPSYN).move_to([4.4, -0.95, 0])
        ar = arr([MUSK_X + 0.55, -0.35, 0], [2.3, -0.35, 0], MUSK, w=5, tip=0.2)
        self.at("scaffold under the membrane")
        self.play(GrowFromCenter(rap), FadeIn(rapl), run_time=0.7)
        self.play(GrowArrow(ar), run_time=0.5)
        self.at("holds the receptors")
        self.play(*[r.animate.move_to([x, 0.45, 0]) for r, x in zip(recs, (3.0, 4.1, 5.2))],
                  rl.animate.move_to([4.1, 1.75, 0]), rap.animate.stretch_to_fit_width(3.6).move_to([4.1, -0.35, 0]),
                  rapl.animate.move_to([4.1, -0.95, 0]), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
CH = dict(
    a=dict(x=-4.2, y=1.3, w=3.6, color=AGRIN, names=["neural agrin"], cap="signal"),
    b=dict(x=0.2, y=1.3, w=2.6, color=LRP4, names=["Lrp4"], cap="receptor"),
    c=dict(x=4.4, y=1.3, w=4.0, color=MUSK, names=["MuSK", "+", "Dok7"], cap="kinase + helper"),
    r=dict(x=4.4, y=-1.5, w=3.0, color=RAPSYN, names=["rapsyn"], cap="scaffold"),
    k=dict(x=-0.6, y=-1.5, w=5.0, color=RECEPTOR, names=["clustered receptors"], cap="result"),
)
CH_H = 2.2


def chain_link(key):
    s = CH[key]
    box = RoundedRectangle(corner_radius=0.2, width=s["w"], height=CH_H, stroke_color=s["color"], stroke_width=3,
                           fill_color=s["color"], fill_opacity=0.16).move_to([s["x"], s["y"], 0])
    nm = [T(n, 36, s["color"] if n != "+" else TEXT) for n in s["names"]]
    names = VGroup(*nm).arrange(RIGHT, buff=0.18).move_to([s["x"], s["y"] + 0.32, 0])
    cap = T(s["cap"], 32, GREY).move_to([s["x"], s["y"] - 0.5, 0])
    back = RoundedRectangle(corner_radius=0.2, width=s["w"], height=CH_H, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(box)
    return dict(box=box, names=names, parts=nm, cap=cap, all=VGroup(back, box, names, cap))


def chain_slot(key):
    s = CH[key]
    r = RoundedRectangle(corner_radius=0.2, width=s["w"], height=CH_H, stroke_color=GREY, stroke_width=3,
                         fill_opacity=0).move_to([s["x"], s["y"], 0])
    return DashedVMobject(r, num_dashes=40)


def chain_arrows():
    a, b, c, r, k = [CH[x] for x in "abcrk"]
    return [
        arr([a["x"] + a["w"] / 2 + 0.1, 1.3, 0], [b["x"] - b["w"] / 2 - 0.1, 1.3, 0]),
        arr([b["x"] + b["w"] / 2 + 0.1, 1.3, 0], [c["x"] - c["w"] / 2 - 0.1, 1.3, 0]),
        arr([5.5, 1.3 - CH_H / 2 - 0.1, 0], [5.5, -1.5 + CH_H / 2 + 0.1, 0]),
        arr([r["x"] - r["w"] / 2 - 0.1, -1.5, 0], [k["x"] + k["w"] / 2 + 0.1, -1.5, 0]),
    ]


class S16Chain(SpokenScene):
    def construct(self):
        d = cs_full(self)
        links = {k: chain_link(k) for k in "abcrk"}
        arrows = chain_arrows()
        slots = VGroup(*[chain_slot(k) for k in "abcrk"])
        everything = VGroup(d["parts"], d["inter"], d["mem"], d["bl"], d["bll"], d["term"], d["tl"], d["ml1"], d["ml2"])
        self.at("the chain")
        self.play(FadeOut(everything), FadeIn(slots), run_time=0.6)
        self.at("neural agrin")
        self.play(FadeIn(links["a"]["all"], shift=RIGHT * 0.2), run_time=0.6)
        self.at("lrp4")
        self.play(GrowArrow(arrows[0]), FadeIn(links["b"]["all"], shift=RIGHT * 0.2), run_time=0.6)
        self.at("musk with")
        self.play(GrowArrow(arrows[1]), FadeIn(links["c"]["all"], shift=RIGHT * 0.2), run_time=0.6)
        self.at("wraps in")
        self.play(GrowArrow(arrows[2]), FadeIn(links["r"]["all"], shift=DOWN * 0.2), run_time=0.6)
        self.at("then clustered")
        self.play(GrowArrow(arrows[3]), FadeIn(links["k"]["all"], shift=LEFT * 0.2), run_time=0.7)
        self.finish()


class S16Hold(NarratedScene):
    def construct(self):
        for k in "abcrk":
            self.add(chain_link(k)["all"])
        self.add(*chain_arrows())
        self.finish()


class S17Break(SpokenScene):
    def construct(self):
        links = {k: chain_link(k) for k in "abcrk"}
        arrows = chain_arrows()
        for k in "abcrk":
            self.add(links[k]["all"])
        self.add(*arrows)
        c = links["c"]
        m_word, d_word = c["parts"][0], c["parts"][2]
        bar_m = strike(m_word)
        bar_d = strike(d_word)
        self.at("musk or")
        self.play(Create(bar_m), m_word.animate.set_opacity(0.45), run_time=0.4)
        self.at("or doc")
        self.play(Create(bar_d), d_word.animate.set_opacity(0.45), c["box"].animate.set_stroke(RED), run_time=0.5)
        res1 = T("no junction", 36, RED, weight=BOLD).move_to([2.8, -0.15, 0])
        self.at("no junctions")
        self.play(FadeIn(res1, shift=UP * 0.1), run_time=0.5)
        # reset the first answer before the next case
        r = links["r"]
        bar_r = strike(r["box"])
        self.at("without")
        self.play(FadeOut(bar_m), FadeOut(bar_d), FadeOut(res1), m_word.animate.set_opacity(1.0),
                  d_word.animate.set_opacity(1.0), c["box"].animate.set_stroke(MUSK), run_time=0.4)
        self.play(Create(bar_r), r["names"].animate.set_opacity(0.45), r["box"].animate.set_stroke(RED), run_time=0.5)
        k = links["k"]
        small_fibre = RoundedRectangle(corner_radius=0.15, width=3.5, height=0.65,
                                       stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                       fill_opacity=0.12).move_to([4.4, -3.05, 0])
        dots = VGroup(*[rdot(4.4 + dx, -3.05 + dy, 0.10) for dx, dy in
                        [(-1.4, 0.10), (-0.85, -0.12), (-0.3, 0.13), (0.3, -0.10), (0.85, 0.12), (1.4, -0.12)]])
        cap = T("receptors made, never clustered", 32, RED, weight=BOLD).move_to([0.2, -3.6, 0])
        self.at("receptors are made")
        self.add(small_fibre, dots, cap)
        self.play(k["box"].animate.set_stroke(opacity=0.35).set_fill(opacity=0.04),
                  k["names"].animate.set_opacity(0.35), k["cap"].animate.set_opacity(0.35), run_time=0.3)
        self.wait(1.8)
        self.finish()


class S18Odd(SpokenScene):
    def construct(self):
        fib, ax, bu, _ = fibre_with_dots(self, dots=False)
        cls = cl_group()
        self.add(cls)
        ca = bchip("agrin", AGRIN, 36).move_to([-5.3, 3.2, 0])
        self.at("remove agrin")
        self.play(FadeIn(ca, scale=0.8), run_time=0.4)
        self.play(Create(strike(ca)), *cdim(ca), run_time=0.4)
        keep = [0, 3, 6]
        gone = [c for i, c in enumerate(cls) if i not in keep]
        kept = [cls[i] for i in keep]
        lab = lt("fewer, smaller clusters", 32, RECEPTOR, -6.5, 2.2)
        self.at("fewer smaller")
        self.play(*[FadeOut(c) for c in gone], *[c[2].animate.set_opacity(0.0) for c in kept], FadeIn(lab), run_time=1.0)
        self.play(*[Indicate(c, color=RECEPTOR, scale_factor=1.15) for c in kept], run_time=0.6)
        bm = Polygon([0, 1.2, 0], [0.8, 1.2, 0], [0.8, 0, 0], [0.4, 0.4, 0], [0, 0, 0], stroke_color=GOLD,
                     stroke_width=3, fill_color=GOLD, fill_opacity=0.9).move_to([6.2, 2.95, 0])
        ol = lt("hold this thought", 32, GOLD, 5.5, 2.95, edge=RIGHT)
        self.at("hold on")
        self.play(FadeIn(bm, shift=DOWN * 0.4), FadeIn(ol), run_time=0.6)
        self.finish()


class S19Rule(SpokenScene):
    def construct(self):
        head = T("THE IDEA FOR THIS LESSON", 30, GOLD, weight=BOLD).move_to([0, 2.3, 0])
        rule = Line(LEFT * 1.6, RIGHT * 1.6, color=GOLD, stroke_width=4).move_to([0, 1.65, 0])
        l1 = T("The muscle proposes;", 64, TEXT, font=TITLE_FONT).move_to([0, 0.35, 0])
        l2 = T("the nerve disposes.", 64, TEXT, font=TITLE_FONT).move_to([0, -1.0, 0])
        self.at("idea for this")
        self.play(FadeIn(head, shift=UP * 0.1), GrowFromCenter(rule), run_time=0.7)
        self.at("muscle proposes")
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.7)
        self.at("nerve disposes")
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S20Rule2(SpokenScene):
    def construct(self):
        fib = fibre()
        self.add(fib)
        nn = T("no motor axons", 42, NERVE).move_to([0, 1.35, 0])
        self.add(nn)
        cls = cl_group()
        self.at("builds clusters")
        for c in cls:
            self.play(FadeIn(c, scale=0.4), run_time=0.1)
        mach = bchip("the muscle's own machinery", MUSK, 30).move_to([3.6, 2.3, 0])
        self.at("its own machinery")
        self.play(FadeIn(mach, shift=RIGHT * 0.2), run_time=0.5)
        ax, bu = axon_line(0.0), bulb(0.0)
        ring = Circle(radius=0.85, stroke_color=TEXT, stroke_width=6).move_to([0, -0.9, 0])
        self.at("the nerve")
        self.play(FadeOut(nn), FadeOut(mach), FadeIn(ax), FadeIn(bu), run_time=0.6)
        self.at("decides which")
        self.play(FadeIn(ring), run_time=0.3)
        self.finish()


class S21Rule3(SpokenScene):
    def construct(self):
        fib, ax, bu = fibre(), axon_line(0.0), bulb(0.0)
        cls = cl_group()
        ring = Circle(radius=0.85, stroke_color=TEXT, stroke_width=6).move_to([0, -0.9, 0])
        self.add(fib, cls, ax, bu, ring)
        pat = strand(0.0, 0.42, L=2.6)
        agl = lt("agrin", 30, AGRIN, 1.9, 0.42)
        self.at("agrin held")
        self.play(FadeIn(pat, scale=0.6), FadeIn(agl), run_time=0.7)
        ml = T("more MuSK activity", 30, MUSK).move_to([-3.6, 0.35, 0])
        glow = Circle(radius=0.85, stroke_color=MUSK, stroke_width=8).move_to([0, -0.9, 0])
        mar = arr([-1.5, 0.15, 0], [-0.7, -0.4, 0], MUSK, w=5, tip=0.2)
        self.at("raises")
        self.play(FadeIn(ml), GrowArrow(mar), Transform(ring, glow), run_time=0.8)
        shield = RoundedRectangle(corner_radius=0.3, width=2.2, height=1.9, stroke_color=MUSK, stroke_width=8,
                                  fill_opacity=0).move_to([0, -0.9, 0])
        self.at("protects those")
        self.play(Transform(ring, shield), run_time=0.8)
        others = VGroup(*cls[1:])
        n = len(others)
        targets = [np.array([c.get_center()[0], c.get_center()[1] + 0.15, 0]) for c in others]
        starts = [(-2.0, 1.5), (2.0, 1.45), (-2.3, 1.15), (2.3, 1.1), (-2.0, 0.85), (2.0, 0.8), (-2.6, 1.4), (2.6, 1.3),
                  (-2.5, 0.9)]
        ach = VGroup(*[Circle(radius=0.14, stroke_width=0, fill_color=ACH, fill_opacity=0.95).move_to([x, y, 0])
                       for x, y in starts[:n]])
        acl = lt("acetylcholine", 32, ACH, 2.7, 2.2)
        acl_leader = leader([2.9, 1.9, 0], [2.0, 1.45, 0], ACH)
        self.at("acetylcholine")
        self.play(FadeIn(ach, scale=0.4), FadeIn(acl), Create(acl_leader), FadeOut(ml), FadeOut(mar), FadeOut(agl), run_time=0.7)
        self.at("disperses")
        self.play(FadeOut(acl_leader), *[a.animate.move_to(t) for a, t in zip(ach, targets)],
                  *[c.animate.scale(0.15).set_opacity(0.06) for c in others], run_time=0.65)
        self.play(FadeOut(ach), run_time=0.2)
        self.wait(1.5)
        self.finish()


class S22Take(SpokenScene):
    def construct(self):
        title = T("Takeaway", 38, GOLD, font=TITLE_FONT).move_to([0, 3.4, 0])
        ys = [1.85, -0.4, -2.6]

        def strip(y, dashed=False):
            r = RoundedRectangle(corner_radius=0.2, width=7.8, height=1.0, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.0 if dashed else 0.14).move_to([1.8, y, 0])
            return DashedVMobject(r, num_dashes=50) if dashed else r
        self.at("take away")
        self.play(FadeIn(title), run_time=0.5)
        ca = bchip("MuSK", MUSK, 34).move_to([-5.0, ys[0], 0])
        self.at("without")
        sa = strip(ys[0], dashed=True)
        self.play(FadeIn(ca), FadeIn(sa), run_time=0.4)
        self.play(Create(strike(ca)), *cdim(ca), run_time=0.4)
        self.at("cannot build")
        ja = T("no junction forms", 34, RED).move_to([1.8, ys[0] - 0.85, 0])
        self.at("no junction")
        self.play(FadeIn(ja, shift=UP * 0.1), run_time=0.5)
        cb = bchip("MuSK", MUSK, 34).move_to([-5.0, ys[1], 0])
        sb = strip(ys[1])
        xs = [-1.2, 0.0, 1.3, 2.6, 3.8, 4.8]
        clb = VGroup(*[cluster(x, ys[1] + dy, 1.4) for x, dy in zip(xs, [0.05, -0.1, 0.1, -0.05, 0.1, -0.08])])
        bl = T("the muscle builds clusters", 34, RECEPTOR).move_to([1.8, ys[1] - 0.85, 0])
        self.at("when it can")
        self.play(FadeIn(cb, scale=0.8), FadeIn(sb), LaggedStart(*[FadeIn(c, scale=0.4) for c in clb], lag_ratio=0.1),
                  FadeIn(bl), run_time=0.9)
        cc = bchip("nerve", NERVE, 34).move_to([-5.0, ys[2], 0])
        sc = strip(ys[2])
        clc = VGroup(*[cluster(x, ys[2] + dy, 1.4) for x, dy in zip(xs, [-0.12, -0.2, -0.1, -0.15, -0.1, -0.18])])
        nl = T("the nerve decides which stay", 34, NERVE).move_to([1.8, ys[2] - 0.85, 0])
        term = VGroup(Line([xs[2], ys[2] + 1.2, 0], [xs[2], ys[2] + 0.65, 0], color=NERVE, stroke_width=10),
                      Ellipse(width=2.1, height=0.65, stroke_color=NERVE, stroke_width=3, fill_color=NERVE,
                              fill_opacity=0.55).move_to([xs[2], ys[2] + 0.6, 0]))
        self.at("the nerve")
        self.play(FadeIn(cc, scale=0.8), FadeIn(sc), FadeIn(clc), FadeIn(nl), FadeIn(term), run_time=0.8)
        ring = Circle(radius=0.45, stroke_color=TEXT, stroke_width=5).move_to([xs[2], ys[2] - 0.15, 0])
        self.at("which clusters stay")
        self.play(*[c.animate.scale(0.12).set_opacity(0.04) for i, c in enumerate(clc) if i != 2],
                  FadeIn(ring), run_time=0.45)
        self.wait(3.0)
        self.finish()


class S23End(EndCard):
    LINE = "The muscle builds clusters; the nerve decides which stay."
