"""Tangential migration: interneurons take the long way round (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  ORANGE = inhibitory interneuron (the travelling cell)
  BLUE   = excitatory pyramidal neuron and its dividing precursors, made in the cortex's own wall
  TEAL   = the chemokine CXCL12
  PURPLE = its receptor CXCR4 (the little tab on the cell)
  YELLOW = the dye (the label that marks cells)
  RED    = missing / blocked (Dlx1 and Dlx2 gone, no CXCR4)
  GREY   = tissue: cortical wall, meninges, ganglionic eminence, radial glial fibre
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"

WALL_X0, WALL_X1 = -2.6, 6.2
WALL_Y0, WALL_Y1 = -2.6, 2.5
LANE_TOP, LANE_DEEP = 2.15, -1.75
X0, X1 = -2.3, 2.8            # where streams run
EMI = np.array([-4.5, -1.0, 0])


def wall():
    w = Rectangle(width=WALL_X1 - WALL_X0, height=WALL_Y1 - WALL_Y0, stroke_color=GREY, stroke_width=3,
                  fill_color=GREY, fill_opacity=0.10).move_to([(WALL_X0 + WALL_X1) / 2, (WALL_Y0 + WALL_Y1) / 2, 0])
    men = RoundedRectangle(corner_radius=0.08, width=WALL_X1 - WALL_X0, height=0.2, stroke_color=GREY, stroke_width=2,
                           fill_color=GREY, fill_opacity=0.5).move_to([(WALL_X0 + WALL_X1) / 2, 2.75, 0])
    lab = T("meninges", 22, GREY).move_to([4.6, 3.2, 0])
    return VGroup(w, men, lab)


def eminence(with_label=True):
    e = Ellipse(width=3.0, height=2.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.22).move_to(EMI)
    rnd = random.Random(4)
    prog = VGroup(*[Circle(radius=0.1, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.7)
                    .move_to(EMI + [rnd.uniform(-1.0, 1.0), rnd.uniform(-0.8, 0.8), 0]) for _ in range(7)])
    g = VGroup(e, prog)
    g.e, g.prog = e, prog
    if with_label:
        g.lab = T("ganglionic eminences", 22, GREY).move_to([-4.5, -2.75, 0])
    return g


def legend():
    a = chip("inhibitory", ORANGE, 24).move_to([-4.5, 2.45, 0])
    b = chip("excitatory", BLUE, 24).move_to([-4.5, 1.7, 0])
    return VGroup(a, b)


def lanes(op=0.12):
    ls = []
    for y in (LANE_TOP, LANE_DEEP):
        ls.append(RoundedRectangle(corner_radius=0.3, width=X1 - X0 + 0.5, height=0.62, stroke_color=ORANGE, stroke_width=1.5,
                                   stroke_opacity=0.5, fill_color=ORANGE, fill_opacity=op).move_to([(X0 + X1) / 2, y, 0]))
    return VGroup(*ls)


def cell(color=ORANGE, r=0.17, tab=False, stroke=None):
    c = Circle(radius=r, stroke_color=stroke or color, stroke_width=2 if not stroke else 4, fill_color=color, fill_opacity=0.9)
    g = VGroup(c)
    g.c = c
    g.tab = None
    if tab:
        t = RoundedRectangle(corner_radius=0.03, width=0.09, height=0.2, stroke_color=PURPLE, stroke_width=1,
                             fill_color=PURPLE, fill_opacity=1).move_to(c.get_right() + RIGHT * 0.04)
        g.tab = t
        g.add(t)
    g.vis = 1.0
    g.tabvis = 1.0
    return g


def set_vis(g, o):
    g.c.set_fill(opacity=0.9 * o).set_stroke(opacity=o)
    if g.tab is not None:
        g.tab.set_fill(opacity=o * g.tabvis).set_stroke(opacity=o * g.tabvis)


def streamer(g, speed):
    g.speed = speed

    def up(m, dt):
        m.shift(RIGHT * m.speed * dt)
        x = m.get_center()[0]
        if x > X1:
            m.shift(LEFT * (X1 - X0))
            x = m.get_center()[0]
        set_vis(m, max(0.0, min(1.0, (x - X0) / 0.5, (X1 - x) / 0.5)))
    g.add_updater(up)
    return g


def stream_cells(tab=False):
    """steady stream cells in both lanes; positions staggered, as when the story continues."""
    out = []
    for y, xs, sp in ((LANE_TOP, (-1.9, -0.6, 0.7, 2.0), 1.0), (LANE_DEEP, (-1.5, -0.2, 1.1, 2.4), 0.9)):
        for x in xs:
            g = cell(tab=tab).move_to([x, y, 0])
            streamer(g, sp)
            out.append(g)
    return out


def teal_dots(seed=2):
    rnd = random.Random(seed)
    ds = []
    for y in (LANE_TOP, LANE_DEEP):
        for i in range(14):
            ds.append(Dot([rnd.uniform(X0 - 0.2, X1 + 0.1), y + rnd.uniform(-0.38, 0.38), 0], radius=0.06, color=TEAL))
    return VGroup(*ds)


def stop_updaters(cells):
    for c in cells:
        c.clear_updaters()


class S00Title(TitleCard):
    LESSON = "Tangential migration"
    TITLE = "Interneurons take the long way round"


# ---------------------------------------------------------------------------------------------
class S01Where(SpokenScene):
    def construct(self):
        w = wall()
        leg = legend()
        inh = VGroup(*[cell().move_to(p) for p in ([-1.4, 0.5, 0], [0.2, -0.3, 0], [1.4, 0.9, 0], [2.7, -0.5, 0],
                                                   [4.0, 0.3, 0], [4.9, 1.1, 0], [3.6, -1.2, 0])])
        self.play(FadeIn(w), FadeIn(leg[0]), LaggedStart(*[FadeIn(c, scale=0.5) for c in inh], lag_ratio=0.15), run_time=1.2)
        self.at("The excitatory neurons are")
        xs = [-0.9, 0.6, 2.1, 3.1]
        pyr = VGroup(*[cell(BLUE).move_to([x, -2.3, 0]) for x in xs])
        self.play(FadeIn(leg[1]), LaggedStart(*[FadeIn(p, scale=0.5) for p in pyr], lag_ratio=0.2), run_time=0.9)
        self.at("They are made in the wall")
        self.wait(0.3)
        self.at("climb straight out")
        self.play(LaggedStart(*[p.animate.move_to([p.get_center()[0], 1.6, 0]) for p in pyr], lag_ratio=0.15), run_time=2.0)
        q = T("?", 80, YELLOW, weight=BOLD).move_to(EMI)
        qa = DashedLine([-3.6, -1.0, 0], [-2.7, -1.0, 0], color=YELLOW, stroke_width=4)
        self.at("So where do")
        self.play(FadeIn(q, scale=0.6), Create(qa), Indicate(inh, color=ORANGE, scale_factor=1.25), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Origin(SpokenScene):
    def construct(self):
        w, leg = wall(), legend()
        inh = VGroup(*[cell().move_to(p) for p in ([-1.4, 0.5, 0], [0.2, -0.3, 0], [1.4, 0.9, 0], [2.7, -0.5, 0],
                                                   [4.0, 0.3, 0], [4.9, 1.1, 0], [3.6, -1.2, 0])])
        q = T("?", 80, YELLOW, weight=BOLD).move_to(EMI)
        qa = DashedLine([-3.6, -1.0, 0], [-2.7, -1.0, 0], color=YELLOW, stroke_width=4)
        pyr = VGroup(*[cell(BLUE).move_to([x, 1.6, 0]) for x in (-0.9, 0.6, 2.1, 3.1)])
        self.add(w, leg, inh, pyr, q, qa)
        em = eminence()
        self.at("swellings called")
        self.play(ReplacementTransform(q, em.e), FadeOut(qa), FadeIn(em.lab), run_time=0.9)
        self.at("temporary zones")
        self.play(FadeIn(em.prog, scale=0.5), run_time=0.7)
        self.at("packed with dividing")
        self.play(Indicate(em.prog, color=GREY, scale_factor=1.3), run_time=0.9)
        # dye
        patch = Circle(radius=0.5, stroke_width=0, fill_color=YELLOW, fill_opacity=0.5).move_to(EMI + [0.2, 0, 0])
        dye_l = T("dye", 24, YELLOW).move_to([-4.5, 0.85, 0])
        self.at("dye placed there")
        self.play(FadeIn(patch, scale=0.4), FadeIn(dye_l), run_time=0.6)
        starts = [[-4.4, -0.7, 0], [-4.2, -1.0, 0], [-4.4, -1.3, 0]]
        lab = VGroup(*[cell(stroke=YELLOW).move_to(p) for p in starts])
        self.at("labels some cells")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in lab], lag_ratio=0.2), run_time=0.8)
        ends = [[-1.0, -1.25, 0], [-1.7, -1.5, 0], [-2.2, -1.75, 0]]
        self.at("run sideways")
        self.play(LaggedStart(*[c.animate.move_to(e) for c, e in zip(lab, ends)], lag_ratio=0.2), run_time=2.4)
        # mutant case: reset, then show
        chipm = T("no Dlx1, no Dlx2", 24, RED).move_to([-4.5, 0.95, 0])
        mut = VGroup(*[cell().move_to(p) for p in ([-4.1, -0.7, 0], [-3.9, -1.1, 0], [-4.1, -1.5, 0])])
        self.at("lacking both")
        ghosts = VGroup(*[DashedVMobject(Circle(radius=0.17, color=RED, stroke_width=2.5), num_dashes=10).move_to(c)
                          for c in inh])
        miss = T("missing interneurons", 22, RED).move_to([4.4, -2.2, 0])
        self.play(FadeOut(VGroup(patch, dye_l, lab, inh)), FadeIn(chipm), FadeIn(mut), run_time=0.9)
        xmark = VGroup(Line([-3.0, -0.8, 0], [-2.6, -1.2, 0], color=RED, stroke_width=6),
                       Line([-3.0, -1.2, 0], [-2.6, -0.8, 0], color=RED, stroke_width=6)).move_to([-2.75, -1.0, 0])
        self.at("make no such trip")
        self.play(*[c.animate.move_to([-3.4, y, 0]) for c, y in zip(mut, (-0.6, -1.0, -1.4))], FadeIn(xmark), run_time=1.0)
        self.play(FadeIn(ghosts), FadeIn(miss), Indicate(pyr, color=BLUE, scale_factor=1.2), run_time=0.9)
        few = VGroup(cell().move_to([0.2, -0.3, 0]), cell().move_to([2.7, -0.5, 0]))
        self.at("few inhibitory neurons")
        self.play(FadeIn(few, scale=0.5), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Streams(SpokenScene):
    def construct(self):
        w, leg, em = wall(), legend(), eminence()
        self.add(w, leg, em, em.lab)
        fibre = Line([2.3, WALL_Y0, 0], [2.3, WALL_Y1, 0], color=GREY, stroke_width=3)
        flab = T("radial glial fibre", 22, GREY).move_to([4.6, -0.6, 0])
        pyr = cell(BLUE).move_to([2.3, -2.3, 0])
        self.at("A pyramidal neuron")
        self.play(FadeIn(fibre), FadeIn(flab), FadeIn(pyr, scale=0.5), run_time=0.8)
        self.at("right angles")
        self.play(pyr.animate.move_to([2.3, 1.3, 0]), run_time=2.0)
        inter = cell().move_to([X0, 0.2, 0])
        harrow = Arrow([-1.9, -0.2, 0], [1.4, -0.2, 0], buff=0, color=ORANGE, stroke_width=4, tip_length=0.2)
        self.at("An interneuron moves parallel")
        self.play(FadeOut(pyr), FadeIn(inter, scale=0.5), run_time=0.6)
        self.play(inter.animate.move_to([1.6, 0.2, 0]), GrowArrow(harrow), run_time=2.0)
        self.at("with no")
        self.play(FadeOut(fibre), FadeOut(flab), run_time=0.6)
        harrow2 = Arrow([-1.9, -0.2, 0], [4.6, -0.2, 0], buff=0, color=ORANGE, stroke_width=4, tip_length=0.2)
        self.at("to follow")
        self.play(inter.animate.move_to([4.8, 0.2, 0]), Transform(harrow, harrow2), run_time=2.2, rate_func=linear)
        ls = lanes()
        cells = stream_cells()
        for c in cells:
            set_vis(c, 0)
        self.at("Inside the cortex")
        self.play(FadeOut(harrow), FadeOut(inter), FadeIn(ls), run_time=0.8)
        self.add(*cells)
        sup = T("superficial stream", 22, ORANGE).move_to([4.6, LANE_TOP, 0])
        deep = T("deep stream", 22, ORANGE).move_to([4.6, LANE_DEEP, 0])
        self.at("One runs just beneath")
        self.play(FadeIn(sup), Indicate(ls[0], color=ORANGE, scale_factor=1.06), run_time=0.9)
        self.at("The other runs deep")
        self.play(FadeIn(deep), Indicate(ls[1], color=ORANGE, scale_factor=1.06), run_time=0.9)
        plate = T("cortical plate", 22, GREY).move_to([4.6, 0.2, 0])
        one = cell().move_to([-0.3, 0.1, 0])
        self.at("Between them")
        self.play(FadeIn(plate), run_time=0.6)
        self.at("holds few")
        self.play(FadeIn(one, scale=0.5), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Chemokine(SpokenScene):
    def construct(self):
        w, em = wall(), eminence()
        ls = lanes()
        cells = stream_cells()
        self.add(w, em, ls, *cells)
        c12 = chip("CXCL12", TEAL, 24).move_to([-4.5, 2.45, 0])
        c4 = chip("CXCR4", PURPLE, 24).move_to([-4.5, 1.7, 0])
        dots = teal_dots()
        dive = DashedLine([0.0, LANE_TOP - 0.35, 0], [0.0, 0.4, 0], color=GREY, stroke_width=4).add_tip(tip_length=0.2)
        self.at("Why do cells stay")
        self.play(Create(dive), run_time=0.7)
        self.at("at once")
        self.wait(0.4)
        gen = chip("chemokine", TEAL, 24).move_to([-4.5, 2.45, 0])
        self.at("Chemokines are small")
        self.play(FadeOut(dive), FadeIn(gen), run_time=0.7)
        self.at("One chemokine")
        self.play(ReplacementTransform(gen, c12), run_time=0.7)
        self.at("lines both streams")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.03), run_time=1.6)
        # meninges source
        men_dots = VGroup(*[Dot([x, 2.75, 0], radius=0.06, color=TEAL) for x in np.linspace(-2.3, 3.0, 12)])
        self.at("The meninges make it")
        self.play(FadeIn(men_dots, scale=0.3), Indicate(w[1], color=TEAL, scale_factor=1.02), run_time=0.9)
        prec = VGroup()
        for x in (-1.6, -0.2, 1.2, 2.6):
            prec.add(VGroup(cell(BLUE, 0.13).move_to([x - 0.16, -2.32, 0]), cell(BLUE, 0.13).move_to([x + 0.16, -2.32, 0])))
        self.at("dividing precursors")
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in prec], lag_ratio=0.2), run_time=1.0)
        # receptor tabs on the stream cells
        for c in cells:
            c.tabvis = 0.0
        tabs = []
        for c in cells:
            t = cell(tab=True)
            c.tab = t.tab
            c.add(t.tab)
            c.tab.set_fill(opacity=0).set_stroke(opacity=0)
            c.tab.move_to(c.c.get_right() + RIGHT * 0.04)
            tabs.append(c.tab)
        self.at("its receptor")
        for c in cells:
            c.tabvis = 1.0
        self.play(FadeIn(c4), run_time=0.8)
        self.wait(0.6)
        # chamber assay
        self.at("In a chamber assay")
        main = VGroup(w, em, em.lab, ls, dots, men_dots, prec, c12, c4, *cells)
        stop_updaters(cells)
        self.play(FadeOut(main), run_time=0.7)
        self.remove(*cells)

        def chamber(cx):
            up = Rectangle(width=4.6, height=2.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([cx, 1.3, 0])
            lo = Rectangle(width=4.6, height=2.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([cx, -1.0, 0])
            mem = DashedLine([cx - 2.3, 0.15, 0], [cx + 2.3, 0.15, 0], color=GREY, stroke_width=4)
            return VGroup(up, lo, mem)
        rnd = random.Random(8)

        def cells_up(cx):
            return VGroup(*[cell().move_to([cx + dx, 1.3 + dy, 0]) for dx, dy in
                            ((-1.5, 0.4), (-0.7, -0.4), (0.1, 0.5), (0.9, -0.3), (1.6, 0.35))])

        def dots_in(cx, y0, y1, n):
            return VGroup(*[Dot([cx + rnd.uniform(-2.1, 2.1), rnd.uniform(y0, y1), 0], radius=0.06, color=TEAL) for _ in range(n)])
        chA = chamber(-3.3)
        cA = cells_up(-3.3)
        dA = dots_in(-3.3, -2.0, -0.2, 16)
        lA = T("chemokine below", 24, TEAL).move_to([-3.3, -2.75, 0])
        self.play(FadeIn(chA), FadeIn(cA), FadeIn(dA, scale=0.3), FadeIn(lA), run_time=0.9)
        self.at("moved toward it")
        self.play(LaggedStart(*[c.animate.move_to([c.get_center()[0], -0.6 - 0.25 * i, 0]) for i, c in enumerate(cA)],
                              lag_ratio=0.12), run_time=1.0)
        chB = chamber(3.3)
        cB = cells_up(3.3)
        dB = VGroup(dots_in(3.3, 0.5, 2.3, 8), dots_in(3.3, -2.0, -0.2, 8))
        lB = T("equal on both sides", 24, TEAL).move_to([3.3, -2.75, 0])
        self.at("but not when")
        self.play(FadeIn(chB), FadeIn(cB), run_time=0.6)
        self.at("equally on both sides")
        self.play(FadeIn(dB, scale=0.3), FadeIn(lB), run_time=0.7)
        self.play(Indicate(cB, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Leave(SpokenScene):
    def construct(self):
        w, em = wall(), eminence()
        ls, dots = lanes(), teal_dots()
        cells = stream_cells(tab=True)
        self.add(w, em, ls, dots, *cells)
        nochip = T("no CXCR4", 24, RED).move_to([-4.5, 1.7, 0])
        self.at("Take away the receptor")
        # the stream updater rewrites tab opacity every frame from tabvis, so fade tabvis itself
        tr = ValueTracker(1.0)
        for c in cells:
            c.add_updater(lambda m, tr=tr: (setattr(m, "tabvis", tr.get_value()), set_vis(m, m.c.get_stroke_opacity())))
        self.play(FadeIn(nochip), tr.animate.set_value(0.0), run_time=0.8)
        # reset to the mutant starting state: new cells entering at the left edge
        stop_updaters(cells)
        mut = []
        for y, tgt in ((LANE_TOP, 0.6), (LANE_DEEP, -0.5)):
            for k in range(3):
                mut.append((cell().move_to([X0 - 0.1 - 0.0 * k, y, 0]), y, tgt, k))
        self.play(FadeOut(VGroup(*cells)), *[FadeIn(m[0], scale=0.5) for m in mut], run_time=0.7)
        self.remove(*cells)
        self.at("leave their streams")
        self.play(*[m[0].animate(rate_func=linear).move_to([-1.2 + 0.0, m[1], 0]) for m in mut], run_time=1.2)
        self.at("enter the cortical plate")
        self.play(*[m[0].animate.move_to([-1.2 + 0.55 * m[3], m[2] + (0.3 if m[1] > 0 else -0.3) * m[3] * 0.3, 0]) for m in mut], run_time=1.4)
        ref = DoubleArrow([X0, -2.95, 0], [X1, -2.95, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.15)
        short = DoubleArrow([X0, -3.35, 0], [-0.1, -3.35, 0], buff=0, color=ORANGE, stroke_width=4, tip_length=0.15)
        l1 = T("normal spread", 22, GREY).move_to([4.6, -2.95, 0])
        l2 = T("less spread", 22, ORANGE).move_to([4.6, -3.35, 0])
        self.at("spread less widely")
        self.play(GrowFromCenter(ref), FadeIn(l1), run_time=0.6)
        self.play(GrowFromCenter(short), FadeIn(l2), run_time=0.7)
        # normal case
        norm = stream_cells(tab=True)
        self.at("Normally")
        self.play(FadeOut(VGroup(*[m[0] for m in mut], ref, short, l1, l2, nochip)), run_time=0.7)
        for c in norm:
            set_vis(c, 0)
        self.add(*norm)
        self.at("stop answering")
        # the hero is one of the stream cells: it keeps pace with its lane, so nothing overlaps
        top = [c for c in norm[:4] if c.get_center()[0] > -1.8]
        hero = min(top, key=lambda c: abs(c.get_center()[0] + 1.2))
        hero.clear_updaters()
        hero.t, hero.turn = 0.0, False

        def hero_up(m, dt):
            m.t += dt
            if not m.turn:
                m.shift(RIGHT * 1.0 * dt)
            elif m.get_center()[1] > 0.4:
                m.shift((RIGHT * 0.45 + DOWN * 0.9) * dt)
            m.tabvis = max(0.0, 1.0 - m.t / 0.8)
            set_vis(m, 1.0)
        hero.add_updater(hero_up)
        ring = Circle(radius=0.32, stroke_color=ORANGE, stroke_width=3).move_to(hero)
        ring.add_updater(lambda r: r.move_to(hero))
        self.play(Create(ring), run_time=0.6)
        self.at("to leave a stream")
        self.wait(0.3)
        self.at("turns into the plate")
        hero.turn = True
        self.wait(1.7)
        ring.clear_updaters()
        hero.clear_updaters()
        self.play(FadeOut(ring), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        w, em = wall(), eminence(with_label=False)
        ls, dots = lanes(), teal_dots()
        self.add(w, em, ls, dots)
        hero = cell(tab=True).move_to(EMI + [0.2, 0, 0])
        c1 = chip("born outside", GREY, 24).move_to([-4.5, -3.15, 0])
        c2 = chip("held by CXCL12", TEAL, 24).move_to([0.2, -3.15, 0])
        c3 = chip("stops answering", ORANGE, 24).move_to([4.2, -3.15, 0])
        self.at("series of decisions")
        self.play(FadeIn(hero, scale=0.5), run_time=0.6)
        self.at("born outside")
        self.play(FadeIn(c1), hero.animate.move_to([-3.2, -1.3, 0]), run_time=1.0)
        self.at("travel sideways")
        self.play(hero.animate.move_to([-2.3, LANE_DEEP, 0]), run_time=0.5)
        self.play(hero.animate.move_to([0.3, LANE_DEEP, 0]), run_time=1.5, rate_func=linear)
        self.at("keeps them in")
        self.play(FadeIn(c2), *[Indicate(d, color=TEAL, scale_factor=1.8) for d in dots], run_time=1.0)
        self.at("Keep this rule")
        self.wait(0.2)
        self.at("stop answering")
        self.play(FadeIn(c3), hero.tab.animate.set_opacity(0), Indicate(hero.c, color=ORANGE, scale_factor=1.4), run_time=0.8)
        self.play(hero.animate.move_to([2.0, 0.3, 0]), run_time=1.3)
        self.finish()


class S07End(EndCard):
    LINE = "A chemokine keeps interneurons in their lanes until they stop answering."
