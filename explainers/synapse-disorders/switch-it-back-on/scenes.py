"""Switch It Back On  (Disorders of the Synapse, chapter 3)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept; shared with scenes.old.py and the other chapters)
  GREY   = circuits, neurons, DNA, axes, structure, typical mice
  GREEN  = working, typical, improved symptoms (gene identity stays TEAL)
  RED    = symptoms, silenced gene, the blocking sequence, "built wrong"
  BLUE   = the MeCP2 protein (and the unnamed key protein of chapter one)
  TEAL   = the MECP2 gene (and the nucleus tag on the recurring synapse)
  GOLD   = methyl tags on DNA
  YELLOW = tamoxifen and the question being asked
  PURPLE = the enzyme Cre and its loxP sites
  ORANGE = excitation        PINK = inhibition
  COOL   = underactive forebrain (dim blue-grey)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E079B8"
COOL = "#7186A6"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def P(x, y):
    return np.array([x, y, 0.0])


def bar(x0, x1, y, h, color, op=0.3):
    return Rectangle(width=x1 - x0, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to(P((x0 + x1) / 2, y))


def mouse(center, s=1.0, color=GREY):
    body = Ellipse(width=2.0, height=1.15, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3)
    head = Ellipse(width=0.95, height=0.8, stroke_color=color, stroke_width=4, fill_color=color,
                   fill_opacity=0.3).move_to(P(1.05, 0.12))
    ear1 = Circle(radius=0.2, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3).move_to(P(0.9, 0.55))
    ear2 = Circle(radius=0.2, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3).move_to(P(1.2, 0.5))
    eye = Dot(P(1.3, 0.2), radius=0.05, color=color)
    tail = ArcBetweenPoints(P(-1.0, -0.1), P(-2.1, 0.5), angle=-1.2, color=color, stroke_width=4)
    g = VGroup(tail, body, head, ear1, ear2, eye)
    g.scale(s).move_to(P(*center))
    return g


def girl(center, s=1.0, color=GREY):
    head = Circle(radius=0.34, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3).move_to(P(0, 1.0))
    dress = Polygon(P(0, 0.55), P(-0.6, -0.5), P(0.6, -0.5), stroke_color=color, stroke_width=4,
                    fill_color=color, fill_opacity=0.3)
    l1 = Line(P(-0.2, -0.5), P(-0.2, -1.0), color=color, stroke_width=4)
    l2 = Line(P(0.2, -0.5), P(0.2, -1.0), color=color, stroke_width=4)
    g = VGroup(l1, l2, dress, head)
    g.scale(s).move_to(P(*center))
    return g


def person(center, s=1.0, color=GREY):
    head = Circle(radius=0.36, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3).move_to(P(0, 1.0))
    body = RoundedRectangle(corner_radius=0.3, width=1.2, height=1.5, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.3).move_to(P(0, -0.1))
    g = VGroup(body, head)
    g.scale(s).move_to(P(*center))
    return g


def neuron(center, kind="big"):
    r, n, L = (0.6, 5, 1.7) if kind == "big" else (0.34, 3, 0.8)
    g = VGroup()
    for k in range(n):
        ang = np.radians(90 + 360 * k / n)
        d = np.array([np.cos(ang), np.sin(ang), 0])
        p0, p1 = d * r, d * (r + L)
        g.add(Line(p0, p1, color=GREY, stroke_width=5))
        if kind == "big":
            for s in (-1, 1):
                a2 = ang + s * np.radians(38)
                d2 = np.array([np.cos(a2), np.sin(a2), 0])
                g.add(Line(p1, p1 + d2 * 0.7, color=GREY, stroke_width=4))
    soma = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.4)
    g.add(soma)
    return g.move_to(P(*center))


def make_circuit(center=(0, 0), scale=1.0, color=GREY):
    nodes_xy = [(-2, 1.3), (-2, -1.3), (0, 1.7), (0, 0), (0, -1.7), (2, 0.9), (2, -0.9)]
    edges_ix = [(0, 2), (0, 3), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6)]
    nodes = VGroup(*[Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color,
                            fill_opacity=0.3).move_to(P(x, y)) for x, y in nodes_xy])
    edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), buff=0.29, color=GREY, stroke_width=4)
                     for a, b in edges_ix])
    g = VGroup(edges, nodes)
    g.edges, g.nodes = edges, nodes
    g.scale(scale).move_to(P(*center))
    return g


def flow(scene, circ, color=GREEN, rt=0.9):
    dots = [Dot(e.get_start(), radius=0.1, color=color) for e in circ.edges]
    scene.add(*dots)
    scene.play(*[d.animate.move_to(e.get_end()) for d, e in zip(dots, circ.edges)], run_time=rt, rate_func=linear)
    scene.play(*[FadeOut(d) for d in dots], run_time=0.2)


class Grid:
    """The two-column grid of chapter one: restore late | delete late (one result row)."""

    def __init__(self, cx, cy, cw, hh=0.95, bh=1.8, heads=("restore late", "delete late"), hsize=30):
        self.cx, self.cw, self.hh, self.bh = cx, cw, hh, bh
        self.xs = [cx - cw / 2, cx + cw / 2]
        self.hy = cy + (bh + hh) / 2 - hh / 2
        self.by = cy - (bh + hh) / 2 + bh / 2
        self.head_cells = [Rectangle(width=cw, height=hh, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                     fill_opacity=0.14).move_to(P(x, self.hy)) for x in self.xs]
        self.body_cells = [Rectangle(width=cw, height=bh, stroke_color=GREY, stroke_width=3,
                                     fill_opacity=0).move_to(P(x, self.by)) for x in self.xs]
        self.heads = [T(h, hsize, TEXT).move_to(c) for h, c in zip(heads, self.head_cells)]
        self.frame = VGroup(*self.head_cells, *self.body_cells)

    def head_group(self, i):
        return VGroup(self.head_cells[i], self.heads[i])

    def yes(self, i, text=None, size=30, color=None):
        text = text or ("symptoms\nimprove" if i == 0 else "symptoms\nappear")
        color = color or (GREEN if i == 0 else RED)
        return T(text, size, color, weight=BOLD, line_spacing=0.9).move_to(self.body_cells[i])



# axes and curves for the symptom-score plots -------------------------------------------------
AX0, AX1, AYA, AYT = -5.6, 6.3, -2.7, 2.9
TAM_X1, TAM_X2 = 0.2, 2.6


def f_rise(x):
    # Illustrative logistic/exponential model from scenes.old.py; no measured scale.
    return -1.9 + 3.8 / (1 + np.exp(-(x + 2.6) * 2.2))


def f_fall(x, xt, end=-1.0):
    return end + (f_rise(xt) - end) * np.exp(-(x - xt) / 1.3)


def curve(fn, x0, x1, color=RED, n=40, w=7):
    c = VMobject(color=color, stroke_width=w)
    c.set_points_smoothly([P(x, fn(x)) for x in np.linspace(x0, x1, n)])
    return c


def plot_axes():
    xa = arr(P(AX0, AYA), P(AX1, AYA), GREY, w=4)
    ya = arr(P(AX0, AYA), P(AX0, AYT), GREY, w=4)
    yl = T("symptom score (illustrative)", 26, GREY).move_to(P(-3.5, 3.3))
    xl = T("time", 26, GREY).move_to(P(5.5, -3.2))
    return VGroup(xa, ya, yl, xl)


def tam_marker(x, label=True, top=2.65):
    ln = DashedLine(P(x, AYA), P(x, top), color=YELLOW, stroke_width=4)
    if not label:
        return VGroup(ln)
    return VGroup(ln, T("tamoxifen, adult", 26, YELLOW).move_to(P(x, top + 0.38)))


def pred_parts():
    head = T("Predict.", 40, YELLOW, weight=BOLD).move_to(P(4.4, 3.2))
    axes = plot_axes()
    rise = curve(f_rise, -5.2, TAM_X1)
    marker = tam_marker(TAM_X1)
    box = DashedVMobject(Rectangle(width=5.4, height=5.0, stroke_color=YELLOW, stroke_width=3),
                         num_dashes=44).move_to(P(3.4, 0.0))
    q = T("?", 64, YELLOW, weight=BOLD).move_to(P(1.4, -0.9))
    c1 = VGroup(bchip("built wrong for good", RED, 26).move_to(P(3.4, 1.0)),
                DashedVMobject(curve(lambda x: f_rise(TAM_X1), 0.8, 6, RED, w=3), num_dashes=24))
    c2 = VGroup(bchip("needs the protein to run", GREEN, 26).move_to(P(3.4, -1.9)),
                DashedVMobject(curve(lambda x: f_fall(x,TAM_X1), 0.8, 6, GREEN, w=3), num_dashes=24))
    return head, axes, rise, marker, box, q, c1, c2


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Disorders of the Synapse: Built, Then Kept"
    TITLE = "Switch It Back On"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        # the recurring synapse (sending side above, receiving side below), big on the left
        pre = RoundedRectangle(corner_radius=0.5, width=7.0, height=1.5, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.25).move_to(P(-2.6, 2.1))
        post = RoundedRectangle(corner_radius=0.5, width=7.0, height=1.5, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.25).move_to(P(-2.6, -0.2))
        scaf = bchip("scaffold", GREY, 26).move_to(P(-2.6, -0.2))
        syn = T("synapse", 28, GREY).move_to(P(-2.6, 3.3))
        nuc = Ellipse(width=2.8, height=1.2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                      fill_opacity=0.2).move_to(P(-2.6, -2.6))
        nl = T("nucleus tag", 26, TEAL).move_to(nuc)
        nt = VGroup(nuc, nl).set_opacity(0.3)
        tie = DashedLine(P(-2.6, -0.95), P(-2.6, -2.0), color=TEAL, stroke_width=3).set_opacity(0.3)
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.4, height=0.8, stroke_color=BLUE,
                                               stroke_width=3), num_dashes=24).move_to(P(-2.6, 0.95))
        slot_q = T("?", 34, BLUE, weight=BOLD).move_to(slot)
        # the switch, off
        track = RoundedRectangle(corner_radius=0.5, width=2.6, height=1.0, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.25).move_to(P(4.2, 0.2))
        knob = Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.8).move_to(P(3.5, 0.2))
        sw_l = T("protein", 28, BLUE).move_to(P(4.2, 1.5))
        offl = T("off", 26, GREY).move_to(P(4.2, -0.9))

        self.add(pre, post, scaf, syn, nt, tie)
        title = T("Switch It Back On", 32, TEXT, font=TITLE_FONT).move_to(P(3.6, 3.1))
        self.add(title)
        self.at("without one protein")
        self.play(Create(slot), FadeIn(slot_q), run_time=0.8)
        self.at("switch")
        self.play(FadeIn(track), FadeIn(knob), FadeIn(sw_l), FadeIn(offl), run_time=0.7)
        self.at("adult")
        on = T("on", 26, GREEN).move_to(P(4.2, -0.9))
        prot = bchip("protein", BLUE, 26).move_to(P(-2.6, 0.95))
        self.play(knob.animate.move_to(P(4.9, 0.2)).set_color(GREEN), track.animate.set_stroke(GREEN).set_fill(GREEN, 0.3),
                  ReplacementTransform(offl, on), FadeOut(slot), FadeOut(slot_q), FadeIn(prot, scale=1.2), run_time=0.8)
        self.at("undo the damage")
        qq = bchip("undo the damage?", YELLOW, 32).move_to(P(-2.6, -1.5))
        self.play(FadeIn(qq, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def timeline_base():
    ax = arr(P(-6.2, -3.0), P(6.4, -3.0), GREY, w=4)
    axl = T("time", 26, GREY).move_to(P(5.7, -3.4))
    return ax, axl


def rett_parts():
    hd = T("Rett syndrome", 38, TEXT, weight=BOLD).move_to(P(0, 3.15))
    g = girl((-4.8, -0.2), 2.1)
    ax = arr(P(-3.1,-2.65), P(6.2,-2.65), GREY, w=4)
    axl = T("time", 28, GREY).move_to(P(5.6,-3.15))
    green = bar(-3.0, 2.0, 1.35, 1.5, GREEN)
    gl = T("typical development", 28, GREEN).move_to(green)
    bk = Brace(green, DOWN, color=GREEN, buff=0.12)
    ml = T("many months", 28, GREEN).next_to(bk, DOWN, buff=0.14)
    return hd, g, ax, axl, green, gl, bk, ml


class S02Rett(SpokenScene):
    def construct(self):
        hd,g,ax,axl,green,gl,bk,ml=rett_parts()
        self.add(hd,g,ax,axl)
        self.at("develop typically")
        self.play(GrowFromEdge(green, LEFT), FadeIn(gl), run_time=0.6)
        self.at("many months")
        self.play(GrowFromCenter(bk), FadeIn(ml), run_time=0.4)
        self.finish()


class S03Loss(SpokenScene):
    def construct(self):
        self.add(*rett_parts())
        red = bar(2.0, 6.2, 1.35, 1.5, RED)
        label = T("lose purposeful\nhand use and speech", 27, RED).move_to(red)
        hand=bchip("hand use", GREEN, 28).move_to(P(2.1,-1.4))
        sp=bchip("speech", GREEN, 28).move_to(P(4.9,-1.4))
        self.add(hand,sp)
        self.at("Then")
        self.play(GrowFromEdge(red,LEFT),FadeIn(label),run_time=0.4)
        self.at("hand use")
        self.play(hand.animate.set_opacity(0.22),run_time=0.3)
        self.at("speech")
        self.play(sp.animate.set_opacity(0.22),run_time=0.3)
        self.wait(1.0)
        self.finish()



# ---------------------------------------------------------------------------------------------
class S04Gene(SpokenScene):
    def construct(self):
        a = Line(P(-1.5, 2.9), P(1.5, -2.9), color=GREY, stroke_width=34)
        b = Line(P(1.5, 2.9), P(-1.5, -2.9), color=GREY, stroke_width=34)
        for ln in (a, b):
            ln.set_cap_style(CapStyleType.ROUND)
        x = VGroup(a, b).move_to(P(-1.6, 0))
        x.set_opacity(0.55)
        # near the lower right end of the X
        mark = Rectangle(width=0.9, height=0.34, stroke_color=TEAL, stroke_width=2, fill_color=TEAL,
                         fill_opacity=1).rotate(np.arctan2(-5.8, 3.0) + PI / 2).move_to(P(-1.6 + 1.1, -2.25))
        ml = T("MECP2", 40, TEAL, weight=BOLD).move_to(P(3.0, -2.45))
        ld = Line(P(-1.6 + 1.5, -2.35), P(1.7, -2.45), color=TEAL, stroke_width=3)
        xl = T("X chromosome", 34, GREY).move_to(P(3.0, 1.8))
        schematic = T("position schematic", 28, GREY).move_to(P(3.0,-3.15))
        xlead = Line(P(0.0,2.0),P(1.1,1.8),color=GREY)
        self.at("Most cases")
        self.play(FadeIn(x, scale=0.9), run_time=1.0)
        self.at("mecp2")
        self.play(FadeIn(mark, scale=2.0), Create(ld), FadeIn(schematic), FadeIn(ml, shift=LEFT * 0.2), run_time=0.7)
        self.at("x chromosome")
        self.play(FadeIn(xl), Create(xlead), x.animate.set_opacity(0.8), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Protein(SpokenScene):
    def construct(self):
        ydna = -1.4
        dna = Line(P(-6.2, ydna), P(6.2, ydna), color=GREY, stroke_width=9)
        tags = VGroup()
        for xx in [-5.0, -2.5, 0.0, 2.5, 5.0]:
            stem = Line(P(xx, ydna), P(xx, ydna - 0.5), color=GOLD, stroke_width=4)
            dot = Circle(radius=0.22, stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                         fill_opacity=0.45).move_to(P(xx, ydna - 0.72))
            tags.add(VGroup(stem, dot))
        tl = T("methyl tags", 30, GOLD).move_to(P(0,3.05))
        bracket = VGroup(Line(P(-5,-2.4),P(-5,-3.05),color=GOLD),Line(P(5,-2.4),P(5,-3.05),color=GOLD),Line(P(-5,-3.05),P(5,-3.05),color=GOLD))
        tl.move_to(P(0,-3.5))
        prot = bchip("MeCP2", BLUE, 32).move_to(P(0.0, -2.5))
        genes = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.9, height=0.5, stroke_color=TEAL, stroke_width=3,
                                          fill_color=TEAL, fill_opacity=0.35).move_to(P(xx, ydna + 0.0))
                         for xx in (-4.0, 1.3, 4.0)])
        dials, needles = VGroup(), []
        for xx in (-4.0, 1.3, 4.0):
            ring = Circle(radius=0.6, stroke_color=GREY, stroke_width=4).move_to(P(xx, 1.0))
            nd = Line(P(xx, 1.0), P(xx, 1.5), color=TEXT, stroke_width=6)
            needles.append(nd)
            dials.add(ring, nd)
        link = VGroup(*[DashedLine(P(xx, ydna + 0.25), P(xx, 0.4), color=GREY, stroke_width=3)
                        for xx in (-4.0, 1.3, 4.0)])
        self.add(dna)
        self.at("protein")
        self.play(FadeIn(prot), run_time=0.3)
        self.at("binds")
        self.play(prot.animate.move_to(P(0,-2.5)), run_time=0.2)
        self.at("methylated")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tags], lag_ratio=0.1), FadeIn(tl), FadeIn(bracket), run_time=0.4)
        self.at("dna")
        self.play(Indicate(tags[2], color=BLUE), run_time=0.3)
        self.at("level")
        self.play(FadeIn(genes), FadeIn(dials), Create(link), run_time=0.6)
        self.at("many genes")
        self.play(needles[0].animate.rotate(-0.5, about_point=needles[0].get_start()),
                  needles[1].animate.rotate(0.55, about_point=needles[1].get_start()),
                  needles[2].animate.rotate(-0.45, about_point=needles[2].get_start()), run_time=0.5)
        self.wait(3.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Mice(SpokenScene):
    def construct(self):
        m = mouse((-3.0, -0.7), 1.95)
        ml = T("mice lacking the gene", 30, GREY).move_to(P(-3.4, -2.3))
        ax, axl = timeline_base()
        green = bar(-6.2, 0.6, 1.9, 1.2, GREEN)
        gl = T("typical for several weeks", 26, GREEN).move_to(green)
        red = bar(0.6, 6.4, 1.9, 1.2, RED)
        rl = T("symptoms", 28, RED).move_to(red)
        ch = [bchip("tremor", RED, 28), bchip("breathing changes", RED, 28), bchip("reduced movement", RED, 28)]
        for c, yy in zip(ch, (0.5, -0.6, -1.7)):
            c.move_to(P(3.6, yy))
        self.add(m, ml)
        self.play(GrowArrow(ax), FadeIn(axl), run_time=0.4)
        self.at("typical")
        self.play(GrowFromEdge(green, LEFT), run_time=1.2)
        self.play(FadeIn(gl), run_time=0.3)
        self.at("Then")
        self.play(GrowFromEdge(red, LEFT), run_time=0.6)
        self.play(FadeIn(rl), run_time=0.3)
        self.at("tremor")
        self.play(FadeIn(ch[0], shift=DOWN * 0.15), run_time=0.4)
        self.at("breathing changes")
        self.play(FadeIn(ch[1], shift=DOWN * 0.15), run_time=0.4)
        self.at("reduced movement")
        self.play(FadeIn(ch[2], shift=DOWN * 0.15), run_time=0.4)
        self.wait(3.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Neurons(SpokenScene):
    def construct(self):
        n1 = neuron((-3.3, 0.2), "big")
        n2 = neuron((3.3, 0.0), "small")
        l1 = T("typical mouse", 30, GREY).move_to(P(-3.3, -3.1))
        l2 = T("mouse lacking the gene", 30, GREY).move_to(P(3.3, -3.1))
        alive = T("alive", 44, GREEN, weight=BOLD).move_to(P(0, 3.2))
        alive2 = T("alive, but small", 44, GREEN, weight=BOLD).move_to(P(0, 3.2))
        self.add(n1,n2,l1,l2)
        self.at("smaller")
        self.play(FadeIn(alive2), Indicate(n2, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.at("simpler dendrites")
        self.play(n2.animate.set_color(GREEN), run_time=0.5)
        self.play(n2.animate.set_color(GREY), run_time=0.4)
        self.wait(3.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
GENE_Y = 0.65


def gene_bar():
    return Rectangle(width=10.4,height=1.8,stroke_color=TEAL,stroke_width=4,
                     fill_color=TEAL,fill_opacity=0.28).move_to(P(0,GENE_Y))


def block_piece():
    return Rectangle(width=2.8,height=1.8,stroke_color=RED,stroke_width=4,
                     fill_color=RED,fill_opacity=0.65).move_to(P(0,GENE_Y))


def lox_marks():
    out=VGroup()
    for xx in (-1.4,1.4):
        tri=Triangle(color=PURPLE,fill_opacity=1).scale(0.25).rotate(PI).move_to(P(xx,1.85))
        label=T("loxP",28,PURPLE).move_to(P(xx,2.4))
        out.add(VGroup(tri,label))
    return out


def nucleus():
    n=RoundedRectangle(width=12.3,height=5.5,corner_radius=0.6,stroke_color=GREY,
                       fill_color=GREY,fill_opacity=0.06).move_to(P(0,0.5))
    nl=T("nucleus",28,GREY).move_to(P(4.7,-1.65))
    return n,nl


class S08Built(SpokenScene):
    def construct(self):
        credit=T("Guy, Bird and colleagues, 2007",34,TEXT).move_to(P(0,3.1))
        gene=gene_bar(); block=block_piece()
        gl=T("MECP2 gene",34,TEAL).move_to(P(-3.4,2.1))
        bl=T("blocking sequence",30,RED).move_to(P(0,-0.9))
        self.add(credit,gene,block,gl,bl)
        self.at("silent")
        sil=bchip("gene silent",RED,36).move_to(P(0,-2.5))
        self.play(FadeIn(sil),gene.animate.set_fill(TEAL,0.1),run_time=0.5)
        self.finish()


class S09Cre(SpokenScene):
    def construct(self):
        n,nl=nucleus(); gene=gene_bar().set_fill(TEAL,0.1); block=block_piece()
        lox=lox_marks(); bl=T("blocking sequence",30,RED).move_to(P(0,-0.9))
        self.add(n,nl,gene,block,lox,bl)
        cre=bchip("Cre",PURPLE,38).move_to(P(-4.5,-3.0))
        cl=T("enzyme; waits outside the nucleus",28,PURPLE).move_to(P(0.4,-3.0))
        self.add(cre,cl)
        self.at("enzyme")
        self.play(Indicate(cre),run_time=0.35)
        self.finish()


class S10Tam(SpokenScene):
    def construct(self):
        n,nl=nucleus(); gene=gene_bar().set_fill(TEAL,0.1); block=block_piece(); lox=lox_marks()
        cre=bchip("Cre",PURPLE,38).move_to(P(-4.5,-3.0))
        self.add(n,nl,gene,block,lox,cre)
        pill=bchip("tamoxifen",YELLOW,36).move_to(P(0,-3.0))
        self.at("tamoxifen")
        self.play(FadeIn(pill,shift=RIGHT*0.8),run_time=0.35)
        self.at("given")
        self.play(pill.animate.move_to(P(-2.4,-3.0)),run_time=0.25)
        self.play(cre.animate.move_to(P(-2.6,-1.2)),run_time=0.5)
        self.at("cuts out the block")
        self.play(cre.animate.move_to(P(0,-0.7)),run_time=0.25)
        self.play(block.animate.shift(UP*1.0).set_opacity(0),FadeOut(lox),run_time=0.9)
        on=bchip("gene on",GREEN,40).move_to(P(0,-1.35))
        self.play(gene.animate.set_fill(TEAL,0.65),FadeOut(cre),FadeIn(on),run_time=0.4)
        self.wait(3.2)
        self.finish()



# ---------------------------------------------------------------------------------------------
class S11Pred(SpokenScene):
    def construct(self):
        head, axes, rise, marker, box, q, c1, c2 = pred_parts()
        self.at("Predict")
        self.play(FadeIn(head, shift=DOWN * 0.15), FadeIn(axes), run_time=0.7)
        self.play(Create(rise), run_time=0.9, rate_func=linear)
        self.at("built wrong")
        self.play(FadeIn(c1, shift=DOWN * 0.1), run_time=0.4)
        self.at("what does")
        self.play(Create(marker), run_time=0.5)
        self.at("sick adult")
        self.play(FadeIn(box), FadeIn(q), run_time=0.5)
        self.at("only needs")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.4)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        self.add(*pred_parts())
        self.finish()


# ---------------------------------------------------------------------------------------------
def recovery_parts():
    axes=plot_axes()
    rise=curve(f_rise,-5.2,TAM_X2)
    m1=tam_marker(TAM_X1)
    # Older-adult intervention has its own short marker, below the shared header.
    m2=tam_marker(TAM_X2,label=False,top=2.1)
    f1=curve(lambda x:f_fall(x,TAM_X1),TAM_X1,6.0)
    f2=DashedVMobject(curve(lambda x:f_fall(x,TAM_X2),TAM_X2,6.0),num_dashes=36)
    young=T("young adult mice",28,TEXT).move_to(P(-3.3,-3.3))
    yl=Line(P(-5.9,-3.3),P(-5.2,-3.3),color=RED,stroke_width=5)
    old=T("older adult mice",28,TEXT).move_to(P(3.2,-3.3))
    ol=DashedLine(P(0.6,-3.3),P(1.3,-3.3),color=RED,stroke_width=5)
    note=T("many symptoms\nimprove",26,GREY).move_to(P(4.7,-1.85))
    return axes,rise,m1,m2,f1,f2,young,yl,old,ol,note


class S13Rev(SpokenScene):
    def construct(self):
        ax,rise,m1,m2,f1,f2,young,yl,old,ol,note=recovery_parts()
        self.add(ax,rise,m1)
        self.at("reversed")
        self.play(Create(f1),run_time=0.6)
        self.at("young adult")
        self.play(FadeIn(young),Create(yl),run_time=0.25)
        self.at("older adult")
        self.play(Create(m2),FadeIn(old),Create(ol),Create(f2),FadeIn(note),run_time=0.7)
        self.wait(3.0)
        self.finish()


class S14Ctrl(SpokenScene):
    def construct(self):
        ax,rise,m1,m2,f1,f2,*_=recovery_parts()
        self.add(ax,m1,VGroup(rise,f1).set_stroke(opacity=0.50).set_fill(opacity=0))
        flat=curve(lambda x:-1.9,-5.2,6,color=GREY,w=8)
        label=T("typical mice plus tamoxifen",30,TEXT).move_to(P(-2.8,-1.4))
        self.add(flat,label)
        self.at("did nothing")
        nc=T("no change",34,YELLOW).move_to(P(3.7,-2.25))
        self.play(FadeIn(nc),run_time=0.3)
        self.wait(3.0)
        self.finish()



# ---------------------------------------------------------------------------------------------
class S15Mean(SpokenScene):
    def construct(self):
        circ = make_circuit((0, 0.5), 1.45)
        cl = T("formed without the protein", 26, TEXT).move_to(P(0, -2.7))
        g = Grid(3.45, 0.6, 3.1)
        note = bchip("not proof of\nnormal development", TEXT, 28).move_to(P(3.45, -2.3))
        self.add(circ)
        self.at("formed without")
        self.play(FadeIn(cl), run_time=0.5)
        self.at("work again")
        self.play(circ.edges.animate.set_color(GREEN), circ.nodes.animate.set_color(GREEN), run_time=0.3)
        flow(self, circ, rt=0.5)
        self.at("once it returns")
        self.play(circ.animate.scale(1.2 / 1.45).move_to(P(-3.4, 0.5)),
                  cl.animate.move_to(P(-3.4, -2.3)),
                  FadeIn(g.frame), FadeIn(g.heads[0]), run_time=0.6)
        self.play(FadeIn(g.yes(0), scale=1.3), run_time=0.5)
        self.at("That does not show")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.finish()


def adult_parts(deleted=False):
    m=mouse((0,-0.5),2.8)
    label=T("adult mouse",32,TEXT).move_to(P(0,1.1))
    gene=bar(-5.3,5.3,2.05,1.1,TEAL)
    gl=T("MECP2 gene",32,TEAL).move_to(P(-3.6,3.05))
    if deleted:
        gene=VGroup(bar(-5.3,-1.4,2.05,1.1,TEAL),bar(1.4,5.3,2.05,1.1,TEAL),
                    DashedVMobject(Rectangle(width=2.7,height=1.1,color=RED).move_to(P(0,2.05)),num_dashes=16))
    return m,label,gene,gl


def symptoms():
    return VGroup(*[bchip(t,RED,28).move_to(P(x,-2.75)) for t,x in
                   [("tremor",-4.8),("breathing changes",-0.5),("reduced movement",4.1)]])


class S16Other(SpokenScene):
    def construct(self):
        m,ml,gene,gl=adult_parts()
        credit=T("Zoghbi laboratory, 2011",32,TEXT).move_to(P(2.6,3.25))
        self.add(m,ml,gene,gl)
        self.at("2011")
        self.play(FadeIn(credit),run_time=0.35)
        self.at("deleted")
        new=adult_parts(True)[2]
        cut=bar(-1.3,1.3,2.05,1.1,TEAL)
        self.add(cut); self.remove(gene); self.add(new)
        self.play(cut.animate.shift(UP*1.1).set_opacity(0),run_time=0.6)
        dl=T("gene deleted",32,RED).move_to(P(0,-2.75))
        self.play(FadeIn(dl),run_time=0.3)
        self.finish()


class S17Rev2(SpokenScene):
    def construct(self):
        parts=adult_parts(True); self.add(*parts)
        ch=symptoms()
        self.at("symptoms")
        self.play(FadeIn(ch),run_time=0.4)
        self.at("protein is needed")
        # Preserve mouse and symptoms while introducing both explicit test outcomes.
        group=VGroup(parts[0],parts[2])
        self.play(group.animate.scale(0.56).move_to(P(0,-0.8)),
                  FadeOut(parts[1]),FadeOut(parts[3]),ch.animate.move_to(P(0,-2.75)),run_time=0.5)
        g=Grid(0,1.7,5.6,hh=0.8,bh=1.2)
        self.play(FadeIn(g.frame),*[FadeIn(h) for h in g.heads],FadeIn(g.yes(0)),FadeIn(g.yes(1)),run_time=0.45)
        self.wait(1.0)
        self.finish()


class S18Grid(SpokenScene):
    def construct(self):
        # Centred full-frame comparison replaces the previous split composition.
        g=Grid(0,0.65,5.7,hh=1.2,bh=3.4)
        self.add(g.frame,*g.heads,g.yes(0,size=36),g.yes(1,size=36))
        need=bchip("needed in adults",BLUE,32).move_to(P(2.85,-2.95))
        build=bchip("building role\nnot ruled out",TEXT,30).move_to(P(-2.85,-2.95))
        build[1].set_stroke(YELLOW, width=3)
        self.at("same way")
        self.play(Indicate(g.body_cells[0],color=GREEN,scale_factor=1),Indicate(g.body_cells[1],color=RED,scale_factor=1),run_time=0.5)
        self.at("adult circuit")
        a=arr(need.get_top()+RIGHT*1.5,g.body_cells[1].get_bottom()+RIGHT*1.5,BLUE)
        self.play(FadeIn(need),GrowArrow(a),run_time=0.4)
        self.at("building role")
        link=VGroup(
            Line(g.body_cells[0].get_bottom(),P(-2.85,-1.95),color=YELLOW,stroke_width=3),
            Line(g.body_cells[1].get_bottom(),P(2.85,-1.95),color=YELLOW,stroke_width=3),
            Line(P(-2.85,-1.95),P(2.85,-1.95),color=YELLOW,stroke_width=3),
            Line(P(-2.85,-1.95),build.get_top(),color=YELLOW,stroke_width=3))
        self.play(FadeIn(build),Create(link),run_time=0.4)
        self.finish()



# ---------------------------------------------------------------------------------------------
def balance(center, width=2.4):
    x,y=center
    beam=Line(P(x-width/2,y),P(x+width/2,y),color=GREY,stroke_width=6)
    fulc=Triangle(color=GREY,fill_opacity=0.4).scale(0.25).move_to(P(x,y-0.4))
    ex=T("excitation",26,ORANGE).move_to(P(x-width/2,y+0.95))
    inh=T("inhibition",26,PINK).move_to(P(x+width/2,y+0.95))
    return VGroup(beam,fulc,ex,inh)


class S19Region(SpokenScene):
    def construct(self):
        overview=balance((0,0),6)
        self.add(overview)
        self.at("shifts")
        self.play(Rotate(overview[0],0.22),run_time=0.5)
        fore=Ellipse(width=6.5,height=3.6,stroke_color=GREY,fill_color=GREY,fill_opacity=0.12).move_to(P(-2.7,1.3))
        stem=RoundedRectangle(width=1.2,height=2.3,corner_radius=0.35,stroke_color=GREY,
                              fill_color=GREY,fill_opacity=0.12).move_to(P(-1.5,-1.95))
        join=Line(P(-1.5,-0.5),P(-1.5,-0.8),color=GREY,stroke_width=4)
        fl=T("forebrain",32,TEXT).move_to(P(-3.4,1.7))
        sl=T("brainstem",30,TEXT).move_to(P(-4.15,-1.95))
        lead=Line(P(-2.8,-1.95),P(-2.15,-1.95),color=GREY,stroke_width=3)
        fb=balance((3.4,1.4),2.7); sb=balance((3.4,-1.6),2.7)
        self.at("in one brain")
        self.play(FadeOut(overview),FadeIn(fore),FadeIn(stem),Create(join),FadeIn(fl),FadeIn(sl),Create(lead),run_time=0.5)
        self.at("runs both ways")
        # Opposite tilts are visible as soon as both regional scales appear.
        fb[0].rotate(-0.3)
        sb[0].rotate(0.3)
        self.play(FadeIn(fb),FadeIn(sb),run_time=0.4)
        self.at("forebrain")
        self.play(fore.animate.set_fill(COOL,0.65).set_stroke(COOL),run_time=0.3)
        self.at("underactive")
        under=T("underactive",30,TEXT).move_to(P(-3.1,0.65))
        self.play(FadeIn(under),run_time=0.4)
        self.at("brainstem")
        self.play(stem.animate.set_fill(ORANGE,0.65).set_stroke(ORANGE),run_time=0.3)
        self.at("toward excitation")
        toward=T("toward excitation",30,ORANGE).move_to(P(2.8,-3.0))
        connector=Line(P(-0.85,-2.2),P(0.9,-2.9),color=ORANGE,stroke_width=3)
        self.play(FadeIn(toward),Create(connector),run_time=0.5)
        self.wait(3.0)
        self.finish()



def portrait_mouse(center):
    # Compact side-view silhouette for the species comparison; no stretched anatomy.
    body=Ellipse(width=3.0,height=2.6,color=GREY,fill_opacity=0.3)
    head=Ellipse(width=1.4,height=1.3,color=GREY,fill_opacity=0.3).move_to(P(1.2,0.65))
    ears=VGroup(*[Circle(radius=0.38,color=GREY,fill_opacity=0.3).move_to(P(x,1.4)) for x in (0.9,1.5)])
    eye=Dot(P(1.65,0.75),radius=0.065,color=GREY)
    tail=ArcBetweenPoints(P(-1.45,-0.3),P(-2.1,0.9),angle=-1.8,color=GREY,stroke_width=4)
    return VGroup(tail,body,head,ears,eye).scale_to_fit_height(3.8).move_to(P(*center))


class S20Lim1(SpokenScene):
    def construct(self):
        lim = T("One limit", 44, YELLOW, weight=BOLD).move_to(P(0, 3.1))
        m = portrait_mouse((-3.6, 0.1)).set_color(TEXT)
        ml = bchip("a mouse result", TEXT, 30).move_to(P(-3.7, -2.65))
        p = person((3.8, 0.1), 2.1)
        pl = T("older person", 32, GREY).move_to(P(3.8, -2.65))
        q = T("?", 90, YELLOW, weight=BOLD).move_to(P(0, 0.2))
        nk = T("not known", 38, YELLOW, weight=BOLD).move_to(P(0, -1.2))
        p.set_opacity(0.35)
        pl.set_opacity(0.35)
        q.set_fill(opacity=0).set_stroke(YELLOW,width=1.5,opacity=0.35)
        self.add(lim,m,ml,p,pl,q)
        self.at("older person")
        self.play(p.animate.set_opacity(1), pl.animate.set_opacity(1), run_time=0.6)
        self.at("not known")
        self.play(q.animate.set_fill(YELLOW,opacity=1).set_stroke(opacity=0), FadeIn(nk), run_time=0.5)
        self.wait(3.0)
        self.finish()


class S21Lim2(SpokenScene):
    def construct(self):
        lim=T("A second limit: dose",44,YELLOW,weight=BOLD).move_to(P(0,3.15))
        ax=T("amount of MeCP2 protein",32,TEXT).move_to(P(0,2.15))
        # Schematic range: translucent shoulders and dashed boundaries signal unknown edges.
        low=bar(-6.0,-2.0,0.4,2.1,RED,0.32).set_stroke(opacity=0)
        mid=bar(-2.0,1.7,0.4,2.1,GREEN,0.2).set_stroke(opacity=0)
        high=bar(1.7,6.0,0.4,2.1,RED,0.32).set_stroke(opacity=0)
        soft=VGroup()
        for edge, ca, cb in [(-2.0,RED,GREEN),(1.7,GREEN,RED)]:
            soft.add(bar(edge-0.7,edge+0.7,0.4,2.1,BG,1).set_stroke(opacity=0))
            for k in range(28):
                blend=interpolate_color(ManimColor(ca),ManimColor(cb),k/27)
                soft.add(bar(edge-0.7+k*0.05,edge-0.65+k*0.05,0.4,2.1,blend,0.28).set_stroke(opacity=0))
        labels=VGroup(T("too little",30,RED).move_to(low),T("working range",28,GREEN).move_to(mid),
                      T("too much\n(duplication)",30,RED).move_to(high))
        unknown=bchip("size not known",YELLOW,30).move_to(P(-0.15,-1.65))
        syn=bchip("a separate syndrome in males",RED,30).move_to(P(2.6,-3.0))
        self.add(lim,ax,low,mid,high,soft,labels,unknown)
        self.at("too much")
        self.play(Indicate(high,color=RED),run_time=0.4)
        self.at("separate syndrome")
        link=arr(high.get_bottom(),syn.get_top(),RED)
        self.play(FadeIn(syn),GrowArrow(link),run_time=0.4)
        self.finish()



class S22Take(SpokenScene):
    def construct(self):
        title = T("Built, then kept", 50, TEXT, font=TITLE_FONT).move_to(P(0, 3.15))
        g = Grid(0, 0.5, 4.6, hh=0.95, bh=1.7)
        rev = T("reversible?", 38, GREEN).move_to(P(g.xs[0], -2.2))
        need = T("still needed?", 38, BLUE).move_to(P(g.xs[1], -2.2))
        self.add(title,g.frame,*g.heads,rev,need)
        mice=T("late tests in mice",30,TEXT).move_to(P(0,-3.2))
        self.add(mice)
        self.at("some traits")
        self.play(FadeIn(g.yes(0), scale=1.3), run_time=0.5)
        self.at("reversed")
        self.play(Indicate(rev), run_time=0.4)
        self.at("some proteins")
        self.play(FadeIn(g.yes(1), scale=1.3), run_time=0.5)
        self.at("needed in adults")
        self.play(Indicate(need), run_time=0.4)
        self.at("the late tests")
        self.play(Indicate(g.head_group(0), color=YELLOW, scale_factor=1),
                  Indicate(g.head_group(1), color=YELLOW, scale_factor=1), run_time=0.9)
        self.finish()


class S23End(EndCard):
    LINE = "In mice, late tests show traits reversible\nand proteins still needed."
