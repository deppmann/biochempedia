"""A neuron must work to die  (Biochemistrypedia explainer, Developmental Neuroscience)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the neuron / a living cell
  YELLOW = NGF, the survival signal (and the brakes it applies)
  TEAL   = new gene expression: the drug that blocks it, c-Jun, the unknown new product
  ORANGE = pro-death BCL-2 family proteins (Bim, Bax)
  PINK   = cytochrome c
  PURPLE = CED-4 / Apaf-1 (and the apoptosome wheel)
  RED    = the killers (CED-3 / caspases) and death itself
  GREEN  = protective: CED-9 / Bcl-2, a caspase inhibitor, "survives"
  GREY   = mitochondrion outline, timelines, labels, dead or inactive things
  GOLD   = the "eat me" tag
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F28CB1"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dimchip(c, o=0.35):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def neuron(r=0.75, color=BLUE):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    stubs = VGroup()
    for ang in (150, 210, 90):
        v = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        stubs.add(Line(v * r, v * (r + 0.28), color=color, stroke_width=4))
    nuc = Circle(radius=r * 0.3, stroke_width=0, fill_color=color, fill_opacity=0.55)
    g = VGroup(body, stubs, nuc)
    g.body, g.stubs, g.nuc = body, stubs, nuc
    return g


def die(n, scale=0.7, color=GREY):
    """animation that turns a neuron into a shrunken, recoloured corpse (one animation: no clashes)."""
    return [n.animate.scale(scale).set_color(color)]


def ring_dots(center, radius=1.2, n=6, color=YELLOW, r=0.12):
    return VGroup(*[Dot(center + radius * np.array([np.cos(a), np.sin(a), 0]), radius=r, color=color)
                    for a in np.linspace(0, TAU, n, endpoint=False) + 0.3])


def xmark(center, s=0.22, color=RED, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


class S00Title(TitleCard):
    LESSON = "The death machinery in neurons"
    TITLE = "A neuron must work to die"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """NGF leaves: the neuron dies; block new protein and it dies later; a ? for what must be made."""

    def construct(self):
        y1, y2 = 1.7, -0.7
        nx = -5.3
        n1 = neuron(0.7).move_to([nx, y1, 0])
        d1 = ring_dots(n1.get_center(), 1.15)
        ngf = T("NGF", 26, YELLOW, weight=BOLD).next_to(d1, UP, buff=0.12)
        tl1 = Arrow([-3.4, y1, 0], [6.4, y1, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        lab1 = T("NGF removed", 26, GREY).move_to([-1.2, y1 + 0.55, 0])
        mk1 = Dot([-3.4, y1, 0], radius=0.14, color=TEXT)

        self.at("Take away")
        self.play(FadeIn(n1), FadeIn(d1), FadeIn(ngf), Create(tl1), run_time=0.8)
        self.at("nerve growth factor")
        self.play(Indicate(d1, color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.at("It dies")
        x1 = 0.4
        gone = [d.animate.shift((d.get_center() - n1.get_center()) * 1.2).set_opacity(0) for d in d1]
        self.play(FadeOut(ngf), FadeIn(lab1), *gone, run_time=0.5)
        self.play(mk1.animate.move_to([x1, y1, 0]), *die(n1), run_time=0.9)
        xm1 = xmark([x1, y1, 0])
        day = T("a day or two", 24, GREY).move_to([x1, y1 - 0.6, 0])
        self.play(Create(xm1), FadeIn(day), run_time=0.3)

        # --- the drug --------------------------------------------------------------------------
        n2 = neuron(0.7).move_to([nx, y2, 0])
        tl2 = Arrow([-3.4, y2, 0], [6.4, y2, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
        lab2 = T("NGF removed", 26, GREY).move_to([-1.2, y2 + 0.55, 0])
        mk2 = Dot([-3.4, y2, 0], radius=0.14, color=TEXT)
        drug = bchip("drug: no new protein", TEAL, 24).move_to([2.75, y2 + 0.78, 0])
        self.at("Now add a drug")
        self.play(FadeIn(n2), Create(tl2), FadeIn(lab2), FadeIn(mk2), run_time=0.6)
        self.at("stops it making")
        self.play(FadeIn(drug, shift=DOWN * 0.15), run_time=0.5)
        self.at("The death is delayed")
        x2 = 4.2
        self.play(mk2.animate.move_to([x2, y2, 0]), run_time=1.4, rate_func=linear)
        self.play(*die(n2), run_time=0.5)
        xm2 = xmark([x2, y2, 0])
        later = DashedLine([x1, y1 - 0.9, 0], [x1, y2 + 0.2, 0], color=GREY, stroke_width=3)
        dlay = T("later", 24, GREY).move_to([x2, y2 - 0.6, 0])
        self.play(Create(xm2), Create(later), FadeIn(dlay), run_time=0.4)

        # --- the puzzle ---------------------------------------------------------------------------
        q = bchip("?", TEAL, 44).move_to([nx, -2.9, 0])
        qlab = T("something new", 26, TEAL).next_to(q, RIGHT, buff=0.3)
        qa = arr(q.get_top(), [nx, y2 - 0.95, 0], TEAL)
        self.at("starving cell")
        self.play(Indicate(n2, color=GREY, scale_factor=1.0), run_time=0.5)
        self.at("make something")
        self.play(FadeIn(q, shift=UP * 0.2), GrowArrow(qa), FadeIn(qlab), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Worm(SpokenScene):
    """lineage tree readout + ced-3/ced-4 (killers) braked by ced-9."""

    def construct(self):
        root = np.array([-6.2, 0.0, 0.0])
        inner = [np.array([-4.5, 1.6, 0.0]), np.array([-4.5, -1.6, 0.0])]
        leaves_p = [np.array([-2.7, y, 0.0]) for y in (2.4, 0.8, -0.8, -2.4)]
        def edge(a, b, r=0.0):
            d = (b - a) / np.linalg.norm(b - a)
            return Line(a, b - d * r, color=GREY, stroke_width=4)

        lines = VGroup(edge(root, inner[0]), edge(root, inner[1]),
                       edge(inner[0], leaves_p[0], 0.3), edge(inner[0], leaves_p[1], 0.3),
                       edge(inner[1], leaves_p[2], 0.3), edge(inner[1], leaves_p[3], 0.3))
        stem = Dot(root, radius=0.12, color=GREY)

        def leaf(p, dies):
            c = Circle(radius=0.3, stroke_width=3.5).move_to(p)
            x = xmark(p, 0.2, RED, 5)
            g = VGroup(c, x)
            g.c, g.x = c, x
            set_leaf(g, dies, instant=True)
            return g

        def set_leaf(g, dies, instant=False):
            if instant:
                if dies:
                    g.c.set_stroke(GREY).set_fill(GREY, 0.12); g.x.set_opacity(1)
                else:
                    g.c.set_stroke(BLUE).set_fill(BLUE, 0.5); g.x.set_opacity(0)
                return None
            if dies:
                return [g.c.animate.set_stroke(GREY).set_fill(GREY, 0.12), g.x.animate.set_opacity(1)]
            return [g.c.animate.set_stroke(BLUE).set_fill(BLUE, 0.5), g.x.animate.set_opacity(0)]

        fate = [False, True, False, True]
        lv = [leaf(p, f) for p, f in zip(leaves_p, fate)]
        for g, f in zip(lv, fate):  # start all alive until the narrator says they die
            set_leaf(g, False, instant=True)

        self.at("transparent worm")
        self.play(Create(lines), FadeIn(stem), LaggedStart(*[FadeIn(g) for g in lv], lag_ratio=0.2), run_time=1.2)
        self.at("same named cells")
        self.play(Indicate(VGroup(lv[1], lv[3]), color=TEXT, scale_factor=1.2), run_time=0.7)
        self.at("die on schedule")
        self.play(*set_leaf(lv[1], True), *set_leaf(lv[3], True), run_time=0.7)

        # machinery
        c9 = bchip("ced-9", GREEN, 32).move_to([2.7, 2.6, 0])
        c3 = bchip("ced-3", RED, 32).move_to([0.9, 0.9, 0])
        c4 = bchip("ced-4", PURPLE, 32).move_to([4.5, 0.9, 0])
        dead = bchip("cell death", RED, 30).move_to([2.7, -1.3, 0])
        a3 = arr(c3.get_bottom(), dead.get_top() + LEFT * 0.4, RED)
        a4 = arr(c4.get_bottom(), dead.get_top() + RIGHT * 0.4, PURPLE)
        self.at("Two genes")
        self.play(FadeIn(c3, shift=DOWN * 0.2), FadeIn(c4, shift=DOWN * 0.2), run_time=0.6)
        self.at("needed for these deaths")
        self.play(GrowArrow(a3), GrowArrow(a4), FadeIn(dead), run_time=0.7)
        self.wait(self.beat(0.02))

        # --- without them: the cells live -------------------------------------------------------
        self.at("Without them")
        self.play(*dimchip(c3), *dimchip(c4), *dimchip(dead), a3.animate.set_opacity(0.2), a4.animate.set_opacity(0.2),
                  *set_leaf(lv[1], False), *set_leaf(lv[3], False), run_time=0.8)

        # --- reset to the normal state, add the brake ---------------------------------------------
        b3 = inhib([2.35, 2.2, 0], c3.get_top() + [0.1, 0.05, 0], GREEN)
        b4 = inhib([3.05, 2.2, 0], c4.get_top() + [-0.1, 0.05, 0], GREEN)
        self.at("third gene")
        self.play(*[m.animate.set_opacity(1) for m in (a3, a4)],
                  c3[1].animate.set_stroke(opacity=1).set_fill(RED, 0.16), c3[2].animate.set_opacity(1),
                  c4[1].animate.set_stroke(opacity=1).set_fill(PURPLE, 0.16), c4[2].animate.set_opacity(1),
                  dead[1].animate.set_stroke(opacity=1).set_fill(RED, 0.16), dead[2].animate.set_opacity(1),
                  *set_leaf(lv[1], True), *set_leaf(lv[3], True),
                  FadeIn(c9, shift=DOWN * 0.2), Create(b3), Create(b4), run_time=0.9)
        # --- lose ced-9: a cell that should live dies -----------------------------------------------
        self.at("cells that should live")
        cross = xmark(c9.get_center(), 0.35, RED, 7)
        self.play(*dimchip(c9, 0.3), FadeOut(b3), FadeOut(b4), Create(cross),
                  *set_leaf(lv[0], True), run_time=0.9)
        # --- remove ced-3 as well: those deaths stop ------------------------------------------------
        self.at("as well")
        cross3 = xmark(c3.get_center(), 0.4, RED, 7)
        self.play(*dimchip(c3, 0.3), Create(cross3), a3.animate.set_opacity(0.2), *set_leaf(lv[0], False),
                  *set_leaf(lv[1], False), *set_leaf(lv[3], False), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Match(SpokenScene):
    """worm genes map to mammalian counterparts; Bax has no clear worm partner."""

    def construct(self):
        xl, xr = -3.9, 3.7
        ys = [1.5, 0.0, -1.5, -3.0]
        hw = T("worm", 30, GREY, weight=BOLD).move_to([xl, 3.0, 0])
        hm = T("mammal", 30, GREY, weight=BOLD).move_to([xr, 3.0, 0])
        w = [bchip("ced-3", RED, 34).move_to([xl, ys[0], 0]),
             bchip("ced-4", PURPLE, 34).move_to([xl, ys[1], 0]),
             bchip("ced-9", GREEN, 34).move_to([xl, ys[2], 0])]
        m = [bchip("caspases", RED, 34).move_to([xr, ys[0], 0]),
             bchip("Apaf-1", PURPLE, 34).move_to([xr, ys[1], 0]),
             bchip("Bcl-2", GREEN, 34).move_to([xr, ys[2], 0])]
        ar = [arr([xl + 1.15, y, 0], [xr - 1.35, y, 0], c) for y, c in zip(ys[:3], (RED, PURPLE, GREEN))]
        notes = [T("similar to a protease", 24, GREY), T("related", 24, GREY), T("keeps cells alive", 24, GREY)]
        for t_, y in zip(notes, ys[:3]):
            t_.move_to([(xl + xr) / 2 + 0.1, y + 0.42, 0])

        self.at("Cloning connected")
        self.play(FadeIn(hw), FadeIn(hm), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in w], lag_ratio=0.25), run_time=1.2)
        self.at("protease")
        self.play(GrowArrow(ar[0]), FadeIn(m[0], shift=LEFT * 0.2), FadeIn(notes[0]), run_time=0.8)
        self.at("related to a mammalian")
        self.play(GrowArrow(ar[1]), FadeIn(m[1], shift=LEFT * 0.2), FadeIn(notes[1]), run_time=0.8)
        self.at("relative of")
        self.play(GrowArrow(ar[2]), FadeIn(m[2], shift=LEFT * 0.2), run_time=0.8)
        self.at("keeps cells alive")
        self.play(FadeIn(notes[2]), run_time=0.5)
        self.at("imperfect")
        bax = bchip("Bax", ORANGE, 34).move_to([xr, ys[3], 0])
        self.play(FadeIn(bax, shift=LEFT * 0.2), run_time=0.7)
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.0, height=0.85, stroke_color=GREY, stroke_width=3),
                              num_dashes=24).move_to([xl, ys[3], 0])
        none = T("none", 28, GREY).move_to([xl, ys[3], 0])
        self.at("no clear counterpart")
        self.play(Create(slot), FadeIn(none), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gate(SpokenScene):
    """the NGF signal falls; stress pathway, c-Jun, Bim; Bax opens the mitochondrion."""

    def construct(self):
        ch = [bchip("NGF signal", YELLOW, 26), bchip("stress pathway", GREY, 26),
              bchip("c-Jun", TEAL, 26), bchip("Bim", ORANGE, 26)]
        row = VGroup(*ch).arrange(RIGHT, buff=1.0).move_to([-0.5, 2.7, 0])
        fit(row)
        ar = [arr(ch[i].get_right(), ch[i + 1].get_left(), GREY, 4, 0.2) for i in range(3)]
        bim_note = T("pro-death relative of Bcl-2", 22, ORANGE).next_to(ch[3], DOWN, buff=0.18)
        # mitochondrion
        mc = np.array([-2.3, -1.3, 0])
        mito = RoundedRectangle(corner_radius=0.8, width=5.8, height=2.8, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.15).move_to(mc)
        mlab = T("mitochondrion", 24, GREY).move_to([mc[0], mc[1] - 1.75, 0])
        cyt = VGroup(*[Dot([mc[0] + dx, mc[1] + 0.35 + dy, 0], radius=0.19, color=PINK)
                       for dx in (-1.2, 0, 1.2) for dy in (0.25, -0.25)])
        clab = T("cytochrome c", 24, PINK).move_to([mc[0], mc[1] - 0.6, 0])

        self.at("Now return")
        self.play(FadeIn(mito), FadeIn(mlab), FadeIn(cyt), FadeIn(clab), run_time=0.8)
        # survival signal falls
        ngf_dots = VGroup(*[Dot(ch[0].get_top() + [dx, 0.3, 0], radius=0.11, color=YELLOW) for dx in (-0.5, 0, 0.5)])
        self.at("survival signal")
        self.play(FadeIn(ch[0]), FadeIn(ngf_dots), run_time=0.5)
        self.at("falls")
        self.play(ngf_dots.animate.shift(DOWN * 0.1).set_opacity(0), *dimchip(ch[0], 0.4), run_time=0.8)
        self.at("stress pathway")
        self.play(GrowArrow(ar[0]), FadeIn(ch[1], shift=RIGHT * 0.2), run_time=0.6)
        self.at("protein called")
        self.play(GrowArrow(ar[1]), FadeIn(ch[2], shift=RIGHT * 0.2), run_time=0.5)
        self.at("rises")
        self.play(Indicate(VGroup(*ch[2][1:]), color=TEAL, scale_factor=1.25), run_time=0.5)
        self.at("relatives of")
        self.play(GrowArrow(ar[2]), FadeIn(ch[3], shift=RIGHT * 0.2), FadeIn(bim_note), run_time=0.7)
        brace = Brace(VGroup(ch[2], ch[3]), DOWN, buff=0.7, color=TEAL)
        blab = T("new gene expression", 26, TEAL).next_to(brace, DOWN, buff=0.12)
        self.at("new gene expression")
        self.play(Create(brace), FadeIn(blab), run_time=0.7)

        # Bax opens the mitochondrion
        edge_x = mc[0] + 2.9
        gap = Rectangle(width=0.26, height=1.2, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([edge_x, mc[1], 0])
        bax = bchip("Bax", ORANGE, 28).move_to([edge_x + 1.3, mc[1] - 1.55, 0])
        bax_a = arr(bax.get_left() + [0.0, 0.05, 0], [edge_x + 0.1, mc[1] - 0.45, 0], ORANGE, 4, 0.2)
        self.at("Bax")
        self.play(FadeIn(bax, shift=LEFT * 0.3), GrowArrow(bax_a), run_time=0.6)
        self.play(FadeIn(gap), run_time=0.4)
        self.at("leave")
        outs = [[3.0, mc[1] + 0.55], [4.2, mc[1] + 0.55], [3.0, mc[1] - 0.05], [4.2, mc[1] - 0.05], [3.6, mc[1] + 1.05],
                [3.6, mc[1] - 0.65]]
        self.play(*[d.animate.move_to([o[0] + 0.6, o[1], 0]) for d, o in zip(cyt, outs)],
                  FadeOut(clab), run_time=1.6)
        clab2 = T("cytochrome c", 24, PINK).move_to([4.3, mc[1] - 1.7, 0])
        self.play(FadeIn(clab2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Cascade(SpokenScene):
    """cytochrome c + Apaf-1 -> apoptosome wheel -> caspase-9 -> caspase-3 -> the cell dismantled, tagged."""

    def construct(self):
        wc = np.array([-4.2, 0.4, 0.0])
        R = 1.65
        ring = [wc + R * np.array([np.cos(a), np.sin(a), 0]) for a in np.linspace(0, TAU, 7, endpoint=False) + np.pi / 2]
        scatter = [np.array(p) for p in ([-6.0, 2.4, 0], [-3.0, 3.0, 0], [-1.7, 1.2, 0], [-6.2, 0.0, 0],
                                         [-2.0, -1.0, 0], [-5.8, -2.0, 0], [-3.4, -2.6, 0])]
        subs = VGroup(*[Circle(radius=0.42, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to(p)
                        for p in scatter])
        cyt = VGroup(*[Dot(p + [0.5, -0.1, 0], radius=0.17, color=PINK) for p in scatter])
        # start: cytochrome c where the last scene left it
        cyt_start = [np.array([3.0 + (i % 3) * 0.6, -1.4 + (i // 3) * 0.6 - 0.3, 0]) for i in range(7)]
        dots = VGroup(*[Dot(p, radius=0.17, color=PINK) for p in cyt_start])
        clab = T("cytochrome c", 24, PINK).move_to([3.7, -2.5, 0])
        alab = T("Apaf-1", 26, PURPLE).move_to([-4.2, 2.65, 0])

        self.at("In the cytoplasm")
        self.play(FadeIn(dots), FadeIn(clab), run_time=0.5)
        self.at("binds")
        self.play(FadeIn(subs), FadeIn(alab), run_time=0.5)
        self.play(*[d.animate.move_to(p + [0.5, -0.1, 0] if False else p + (np.array([0.48, 0.0, 0]))) for d, p in zip(dots, scatter)],
                  FadeOut(clab), run_time=1.2)
        self.at("assembles into a wheel")
        self.play(*[s.animate.move_to(p) for s, p in zip(subs, ring)],
                  *[d.animate.move_to(p + (p - wc) / np.linalg.norm(p - wc) * 0.55) for d, p in zip(dots, ring)],
                  alab.animate.move_to([wc[0], wc[1] + 2.75, 0]), run_time=1.5)
        hub = Circle(radius=0.55, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.15).move_to(wc)
        spokes = VGroup(*[Line(wc + (p - wc) * 0.33, p - (p - wc) / np.linalg.norm(p - wc) * 0.42, color=PURPLE, stroke_width=3)
                          for p in ring])
        apo = T("apoptosome", 28, PURPLE, weight=BOLD).move_to([wc[0], wc[1] - 2.7, 0])
        self.at("apoptosome")
        self.play(Create(hub), Create(spokes), FadeOut(alab), FadeIn(apo), run_time=0.8)

        c9 = bchip("caspase-9", GREY, 28).move_to([0.2, 1.7, 0])
        c3 = bchip("caspase-3", GREY, 28).move_to([0.2, -0.6, 0])
        a1 = arr([wc[0] + 2.4, 1.3, 0], c9.get_left(), PURPLE)
        a2 = arr(c9.get_bottom(), c3.get_top(), RED)
        cell = neuron(1.25).move_to([4.7, 0.6, 0])
        a3 = arr(c3.get_right(), [cell.get_left()[0] - 0.55, 0.6, 0], RED)
        exe = T("executioner", 22, RED).next_to(c3, DOWN, buff=0.15)
        self.at("activates caspase")
        self.play(FadeIn(c9), GrowArrow(a1), run_time=0.5)
        self.play(c9[1].animate.set_stroke(RED).set_fill(RED, 0.2), c9[2].animate.set_color(RED), run_time=0.4)
        self.at("cuts and activates")
        self.play(GrowArrow(a2), FadeIn(c3), run_time=0.5)
        self.play(c3[1].animate.set_stroke(RED).set_fill(RED, 0.2), c3[2].animate.set_color(RED), FadeIn(exe), run_time=0.4)
        self.at("Executioner caspases dismantle")
        self.play(FadeIn(cell), GrowArrow(a3), run_time=0.5)
        self.play(*die(cell, 0.7, RED), run_time=1.0)
        tag = bchip("eat me", GOLD, 28).move_to([4.7, 2.15, 0])
        self.at("eat me")
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.6)
        self.play(Indicate(tag, color=GOLD, scale_factor=1.12), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Brakes(SpokenScene):
    """cytochrome c injected into three kinds of neurons; NGF brakes at more than one step."""

    def construct(self):
        xs = [-4.5, 0.0, 4.5]
        ny = -0.1

        def column(x, label, dots=False):
            n = neuron(0.8).move_to([x, ny, 0])
            lab = T(label, 24, TEXT, line_spacing=0.8).move_to([x, 2.95, 0])
            needle = Line([x, 2.2, 0], [x, 1.1, 0], color=GREY, stroke_width=5)
            drop = Dot([x, 1.05, 0], radius=0.17, color=PINK)
            g = VGroup(n, lab, needle)
            d = ring_dots(n.get_center(), 1.3, 6, YELLOW, 0.12) if dots else None
            return n, lab, needle, drop, d

        pc = [bchip("cytochrome c released", PINK, 30), bchip("caspases active", RED, 30), bchip("cell dies", GREY, 30)]
        VGroup(*pc).arrange(RIGHT, buff=1.1).move_to([0, -0.8, 0])
        pa = [arr(pc[0].get_right(), pc[1].get_left()), arr(pc[1].get_right(), pc[2].get_left())]
        self.play(FadeIn(VGroup(*pc, *pa)), run_time=0.6)
        # --- case 1: kept in NGF ---------------------------------------------------------------
        n1, l1, nd1, dr1, d1 = column(xs[0], "kept in NGF", True)
        legend = T("cytochrome c", 24, PINK).move_to([xs[0] + 1.75, 1.3, 0])
        self.at("injected")
        self.play(FadeOut(VGroup(*pc, *pa)), FadeIn(n1), FadeIn(d1), FadeIn(l1), FadeIn(nd1), FadeIn(dr1), FadeIn(legend), run_time=0.8)
        self.play(dr1.animate.move_to(n1.get_center() + UP * 0.1), run_time=0.7)
        ok1 = T("survives", 28, GREEN, weight=BOLD).move_to([xs[0], -1.9, 0])
        self.at("survived")
        self.play(FadeIn(ok1, shift=UP * 0.15), run_time=0.5)

        # --- case 2: deprived 15 to 20 hours -----------------------------------------------------------
        n2, l2, nd2, dr2, _ = column(xs[1], "no NGF for about\n15 to 20 hours")
        self.at("deprived of")
        self.play(FadeIn(n2), FadeIn(l2), FadeIn(nd2), FadeIn(dr2), run_time=0.7)
        self.play(dr2.animate.move_to(n2.get_center() + UP * 0.1), run_time=0.6)
        self.at("died after the injection")
        no2 = T("dies", 28, RED, weight=BOLD).move_to([xs[1], -1.9, 0])
        self.play(*die(n2), FadeIn(no2, shift=UP * 0.15), run_time=1.0)

        # --- case 3: caspase inhibitor ---------------------------------------------------------------
        n3, l3, nd3, dr3, _ = column(xs[2], "no NGF for about\n15 to 20 hours")
        inh = bchip("caspase inhibitor", GREEN, 24).move_to([xs[2], -2.9, 0])
        self.at("caspase inhibitor")
        self.play(FadeIn(n3), FadeIn(l3), FadeIn(nd3), FadeIn(dr3), FadeIn(inh, shift=UP * 0.15), run_time=0.5)
        self.play(dr3.animate.move_to(n3.get_center() + UP * 0.1), run_time=0.5)
        ok3 = T("survives", 28, GREEN, weight=BOLD).move_to([xs[2], -1.9, 0])
        self.at("prevented their death")
        self.play(FadeIn(ok3, shift=UP * 0.15), run_time=0.5)

        # --- the lesson: two brakes ----------------------------------------------------------------------
        allm = VGroup(n1, l1, nd1, dr1, d1, legend, ok1, n2, l2, nd2, dr2, no2, n3, l3, nd3, dr3, inh, ok3)
        c1 = bchip("cytochrome c released", PINK, 30)
        c2 = bchip("caspases active", RED, 30)
        c3 = bchip("cell dies", GREY, 30)
        VGroup(c1, c2, c3).arrange(RIGHT, buff=1.1).move_to([0, -0.8, 0])
        a12 = arr(c1.get_right(), c2.get_left(), GREY)
        a23 = arr(c2.get_right(), c3.get_left(), GREY)
        k1 = bchip("NGF", YELLOW, 32).move_to([c1.get_center()[0], 2.2, 0])
        k2 = bchip("NGF", YELLOW, 32).move_to([(c1.get_right()[0] + c2.get_left()[0]) / 2, 2.2, 0])
        b1 = inhib(k1.get_bottom(), c1.get_top(), YELLOW)
        b2 = inhib(k2.get_bottom(), (a12.get_center() + UP * 0.12), YELLOW)
        self.at("holds the death program")
        self.play(FadeOut(allm), run_time=0.6)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3), GrowArrow(a12), GrowArrow(a23), run_time=0.8)
        self.play(FadeIn(k1, shift=DOWN * 0.15), Create(b1), run_time=0.6)
        self.at("more than one step")
        self.play(FadeIn(k2, shift=DOWN * 0.15), Create(b2), run_time=0.6)
        self.at("Death is a program")
        self.play(Indicate(VGroup(*c1[1:], *c2[1:], *c3[1:]), color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Death is a program, held back at more than one step."
