"""Does a circuit need its protein later?  (Biochemistrypedia explainer, Disorders of the Synapse)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREY   = circuits, neurons, DNA, axes, structure
  GREEN  = working, typical, gene on
  RED    = symptoms, silenced gene, the blocking sequence, "built wrong"
  BLUE   = the MeCP2 protein (and the unnamed key protein of scene one)
  TEAL   = the MECP2 gene
  GOLD   = methyl tags on DNA
  YELLOW = tamoxifen and the question being asked
  PURPLE = the enzyme Cre
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"

NODES = [(-2, 1.3), (-2, -1.3), (0, 1.7), (0, 0), (0, -1.7), (2, 0.9), (2, -0.9)]
EDGES = [(0, 2), (0, 3), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6)]


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def make_circuit(center=(0, 0), scale=1.0, color=GREY):
    nodes = VGroup(*[Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color,
                            fill_opacity=0.3).move_to([x, y, 0]) for x, y in NODES])
    edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), color=GREY, stroke_width=4)
                     for a, b in EDGES])
    g = VGroup(edges, nodes)
    g.edges, g.nodes = edges, nodes
    g.scale(scale).move_to([center[0], center[1], 0])
    return g


def flow(scene, circ, color=GREEN, rt=0.9):
    """a pulse of dots runs along every connection"""
    dots = [Dot(e.get_start(), radius=0.1, color=color) for e in circ.edges]
    scene.add(*dots)
    scene.play(*[d.animate.move_to(e.get_end()) for d, e in zip(dots, circ.edges)], run_time=rt, rate_func=linear)
    scene.play(*[FadeOut(d) for d in dots], run_time=0.2)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def neuron(center, big=True):
    r = 0.55 if big else 0.38
    n = 5 if big else 3
    L = 1.4 if big else 0.9
    g = VGroup()
    for k in range(n):
        ang = np.radians(90 + 360 * k / n)
        d = np.array([np.cos(ang), np.sin(ang), 0])
        p0, p1 = d * r, d * (r + L)
        g.add(Line(p0, p1, color=GREY, stroke_width=5))
        if big:
            for s in (-1, 1):
                a2 = ang + s * np.radians(38)
                d2 = np.array([np.cos(a2), np.sin(a2), 0])
                g.add(Line(p1, p1 + d2 * 0.65, color=GREY, stroke_width=4))
    soma = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.4)
    g.add(soma)
    return g.move_to([center[0], center[1], 0])


class S00Title(TitleCard):
    LESSON = "Disorders of the synapse"
    TITLE = "Does a circuit need its protein later?"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        circ = make_circuit((0, 0.1), 1.35)
        built = T("built", 30, GREY).move_to([-5.2, 2.3, 0])
        self.at("A circuit has to be built")
        self.play(FadeIn(built), LaggedStart(*[FadeIn(n, scale=0.5) for n in circ.nodes], lag_ratio=0.12),
                  LaggedStart(*[Create(e) for e in circ.edges], lag_ratio=0.12), run_time=1.6)
        self.at("kept running")
        run = T("kept running", 30, GREEN).move_to([-5.0, 1.5, 0])
        self.play(circ.edges.animate.set_color(GREEN), circ.nodes.animate.set_color(GREEN), FadeIn(run), run_time=0.4)
        flow(self, circ)

        # without the protein
        self.at("built without")
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.9, height=0.9, stroke_color=BLUE,
                                               stroke_width=3), num_dashes=28).move_to([4.9, 1.5, 0])
        q = T("key protein?", 26, BLUE).move_to(slot)
        self.play(FadeOut(built), FadeOut(run), circ.edges.animate.set_color(GREY),
                  circ.nodes.animate.set_color(GREY), FadeIn(slot), FadeIn(q), run_time=0.7)
        self.at("in an adult")
        adult = T("adult", 30, GREY).move_to([-5.2, 2.3, 0])
        prot = bchip("key protein", BLUE, 26).move_to(slot)
        self.play(FadeIn(adult), FadeOut(q), FadeOut(slot), FadeIn(prot, scale=1.2), run_time=0.6)
        self.play(prot.animate.move_to([0, 0.1, 0]), run_time=0.7)
        self.at("undo the damage")
        qq = T("Can it undo the damage?", 38, YELLOW).move_to([0, -3.1, 0])
        self.play(FadeIn(qq, shift=UP * 0.15), run_time=0.5)

        # two possible answers
        self.at("built wrong")
        self.play(FadeOut(prot), FadeOut(qq), FadeOut(adult),
                  circ.animate.scale(1.0 / 1.35).move_to([-3.5, 0.6, 0]), run_time=0.8)
        wrong = Line(circ.nodes[0].get_center(), circ.nodes[4].get_center(), color=RED, stroke_width=5)
        wl = T("built wrong for good:\nstays wrong", 28, RED, line_spacing=0.8).move_to([-3.5, -2.2, 0])
        self.play(Create(wrong), FadeIn(wl), run_time=0.7)
        self.at("is sound")
        circ2 = make_circuit((3.5, 0.6), 1.0)
        sl = T("sound, needs the protein\nto keep working", 28, GREEN, line_spacing=0.8).move_to([3.5, -2.2, 0])
        self.play(FadeIn(circ2), FadeIn(sl), run_time=0.7)
        self.at("should recover")
        self.play(circ2.edges.animate.set_color(GREEN), circ2.nodes.animate.set_color(GREEN), run_time=0.4)
        flow(self, circ2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Rett(SpokenScene):
    def construct(self):
        self.at("Rett syndrome puts")
        head = bchip("girls with Rett syndrome", GREY, 28).move_to([0, 3.0, 0])
        self.play(FadeIn(head), run_time=0.5)
        green = RoundedRectangle(corner_radius=0.12, width=6.4, height=0.6, stroke_color=GREEN, stroke_width=3,
                                 fill_color=GREEN, fill_opacity=0.3).move_to([-2.7, 1.9, 0])
        red = RoundedRectangle(corner_radius=0.12, width=4.2, height=0.6, stroke_color=RED, stroke_width=3,
                               fill_color=RED, fill_opacity=0.3).move_to([3.6, 1.9, 0])
        gl = T("seem typical for many months", 26, GREEN).move_to([-2.7, 1.15, 0])
        rl = T("lose hand use\nand speech", 26, RED, line_spacing=0.8).move_to([3.6, 1.0, 0])
        self.at("seem to develop typically")
        self.play(GrowFromEdge(green, LEFT), FadeIn(gl), run_time=0.9)
        self.at("lose purposeful hand use")
        self.play(GrowFromEdge(red, LEFT), FadeIn(rl), run_time=0.8)

        # gene -> protein -> DNA
        dna = Line([-6.0, -2.3, 0], [6.0, -2.3, 0], color=GREY, stroke_width=8)
        tags = VGroup()
        xs = [-4.8, -2.4, 0.0, 2.4, 4.8]
        for x in xs:
            stem = Line([x, -2.3, 0], [x, -1.85, 0], color=GOLD, stroke_width=3)
            dot = Circle(radius=0.2, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.4).move_to([x, -1.65, 0])
            tags.add(VGroup(stem, dot))
        gene = bchip("M E C P 2 gene", TEAL, 28).move_to([-4.0, -0.2, 0])
        gene[2].become(T("MECP2 gene", 28, TEAL).move_to(gene[1]))
        prot = bchip("MeCP2 protein", BLUE, 28).move_to([0.3, -0.2, 0])
        self.at("gene called")
        self.play(FadeOut(gl), FadeOut(rl), green.animate.set_opacity(0.15), red.animate.set_opacity(0.15),
                  FadeIn(gene, scale=0.8), run_time=0.7)
        self.at("makes a protein")
        a1 = arr(gene.get_right(), prot.get_left(), BLUE)
        self.play(GrowArrow(a1), FadeIn(prot, shift=RIGHT * 0.2), run_time=0.7)
        self.at("binds")
        self.play(Create(dna), run_time=0.5)
        self.play(prot.animate.move_to([2.4, -0.7, 0]), FadeOut(a1), run_time=0.7)
        self.at("methyl groups")
        ml = T("methyl tags on cytosines", 26, GOLD).move_to([-2.2, -3.1, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tags], lag_ratio=0.1), FadeIn(ml), run_time=0.8)
        self.play(prot.animate.move_to([2.4, -1.1, 0]), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Mice(SpokenScene):
    def construct(self):
        self.at("Now look at mice")
        head = bchip("mice lacking the gene", GREY, 30).move_to([0, 3.0, 0])
        self.play(FadeIn(head), run_time=0.5)
        green = RoundedRectangle(corner_radius=0.14, width=6.4, height=0.9, stroke_color=GREEN, stroke_width=3,
                                 fill_color=GREEN, fill_opacity=0.3).move_to([-2.7, 1.5, 0])
        red = RoundedRectangle(corner_radius=0.14, width=4.2, height=0.9, stroke_color=RED, stroke_width=3,
                               fill_color=RED, fill_opacity=0.3).move_to([3.6, 1.5, 0])
        gl = T("typical for several weeks", 28, GREEN).move_to(green)
        rl = T("symptoms", 28, RED).move_to(red)
        ax = arr([-5.7, -0.1, 0], [-0.3, -0.1, 0], GREY)
        ax_l = T("time", 26, GREY).move_to([-3.0, -0.65, 0])
        self.play(GrowArrow(ax), FadeIn(ax_l), run_time=0.5)
        self.at("They appear typical")
        self.play(GrowFromEdge(green, LEFT), run_time=0.6)
        self.play(FadeIn(gl), run_time=0.3)
        self.at("Then they develop")
        self.play(GrowFromEdge(red, LEFT), run_time=0.4)
        self.play(FadeIn(rl), run_time=0.2)
        chips = [bchip("tremor", RED, 28), bchip("breathing changes", RED, 28), bchip("reduced movement", RED, 28)]
        ys = [-0.35, -1.45, -2.55]
        for c, y in zip(chips, ys):
            c.move_to([3.6, y, 0])
        self.at("tremor")
        self.play(FadeIn(chips[0], shift=DOWN * 0.15), run_time=0.4)
        self.at("breathing changes")
        self.play(FadeIn(chips[1], shift=DOWN * 0.15), run_time=0.4)
        self.at("reduced movement")
        self.play(FadeIn(chips[2], shift=DOWN * 0.15), run_time=0.4)

        self.at("Their neurons do not die")
        self.play(*[FadeOut(m) for m in (head, green, red, gl, rl, ax, ax_l, *chips)], run_time=0.5)
        top = T("neurons do not die in large numbers", 32, GREEN).move_to([0, 3.1, 0])
        n1 = neuron((-3.3, 0.25), True)
        n2 = neuron((3.3, 0.25), False)
        l1 = T("typical mouse", 28, GREY).move_to([-3.3, -2.75, 0])
        l2 = T("mouse lacking the gene", 28, RED).move_to([3.3, -2.75, 0])
        self.play(FadeIn(top), FadeIn(n1), FadeIn(n2), FadeIn(l1), FadeIn(l2), run_time=0.8)
        self.at("smaller")
        sm = T("smaller, simpler dendrites", 28, RED).move_to([3.3, -3.25, 0])
        self.play(Indicate(n2, color=RED, scale_factor=1.1), FadeIn(sm), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Switch(SpokenScene):
    def construct(self):
        nuc = Ellipse(width=9.2, height=5.2, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                      fill_opacity=0.08).move_to([0.6, -0.2, 0])
        nl = T("nucleus", 26, GREY).move_to([0.6, -2.4, 0])
        gene = RoundedRectangle(corner_radius=0.12, width=6.2, height=0.7, stroke_color=TEAL, stroke_width=3,
                                fill_color=TEAL, fill_opacity=0.35).move_to([0.6, -0.4, 0])
        gl = T("MECP2 gene", 28, TEAL).move_to([0.6, -1.3, 0])
        block = RoundedRectangle(corner_radius=0.1, width=1.7, height=1.0, stroke_color=RED, stroke_width=4,
                                 fill_color=BG, fill_opacity=1).move_to([0.6, -0.4, 0])
        bl = T("block", 26, RED).move_to(block)
        blk = VGroup(block, bl)
        state = T("gene silent", 30, RED, weight=BOLD).move_to([0.6, 1.3, 0])
        self.play(Create(nuc), FadeIn(nl), run_time=0.7)
        self.play(GrowFromEdge(gene, LEFT), FadeIn(gl), run_time=0.5)
        self.at("gene is silent")
        self.play(FadeIn(blk, scale=1.3), FadeIn(state), run_time=0.6)
        self.at("blocking sequence")
        self.play(Indicate(blk, color=RED, scale_factor=1.15), run_time=0.7)

        cre = bchip("Cre", PURPLE, 30).move_to([-5.45, -0.4, 0])
        cl = T("enzyme", 24, PURPLE).next_to(cre, DOWN, buff=0.2)
        self.at("also carry an enzyme")
        self.play(FadeIn(cre, shift=RIGHT * 0.2), FadeIn(cl), run_time=0.6)
        pill = RoundedRectangle(corner_radius=0.25, width=2.3, height=0.55, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.25).move_to([-5.0, 2.7, 0])
        pt = T("tamoxifen", 24, YELLOW).move_to(pill)
        pg = VGroup(pill, pt)
        self.at("enters the nucleus")
        self.play(cre.animate.move_to([-4.85, -0.4, 0]), FadeOut(cl), run_time=0.5)
        self.at("receives the drug")
        self.play(FadeIn(pg, shift=DOWN * 0.15), run_time=0.4)
        self.play(pg.animate.move_to([-5.45, 0.7, 0]), run_time=0.4)
        self.play(FadeOut(pg), cre[1].animate.set_stroke(YELLOW), run_time=0.2)
        self.play(cre.animate.move_to([-2.0, 0.6, 0]), run_time=0.7)
        self.at("removes the block")
        self.play(cre.animate.move_to([0.6, 0.6, 0]), run_time=0.5)
        self.play(blk.animate.shift(UP * 0.1), run_time=0.15)
        self.play(blk.animate.shift(UP * 2.2).set_opacity(0), run_time=0.8)
        self.at("comes back on")
        on = T("gene on", 30, GREEN, weight=BOLD).move_to([0.6, 1.3, 0])
        self.play(gene.animate.set_stroke(GREEN).set_fill(GREEN, 0.4), ReplacementTransform(state, on),
                  gl.animate.set_color(TEAL), FadeOut(cre), run_time=0.7)
        self.at("chooses when")
        self.play(Indicate(on, color=GREEN, scale_factor=1.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def symptom_y(x):
    base, top, end = -1.9, 1.9, -1.0
    if x <= 0.6:
        return base + (top - base) / (1 + np.exp(-(x + 2.6) * 2.2))
    y0 = base + (top - base) / (1 + np.exp(-(0.6 + 2.6) * 2.2))
    return end + (y0 - end) * np.exp(-(x - 0.6) / 1.3)


class S05Result(SpokenScene):
    def construct(self):
        x0, x1, ya = -5.4, 5.6, -2.4
        xaxis = arr([x0, ya, 0], [x1, ya, 0], GREY, w=4)
        yaxis = arr([x0, ya, 0], [x0, 3.0, 0], GREY, w=4)
        al = T("age", 26, GREY).move_to([-4.7, -2.9, 0])
        sl = T("symptoms", 26, GREY).move_to([-4.2, 3.2, 0])
        sch = T("schematic", 24, GREY).move_to([4.9, 3.3, 0])
        self.at("key test")
        self.play(GrowArrow(xaxis), GrowArrow(yaxis), FadeIn(al), FadeIn(sl), FadeIn(sch), run_time=0.9)
        rise = VMobject(color=RED, stroke_width=7)
        rise.set_points_smoothly([[x, symptom_y(x), 0] for x in np.linspace(-5.2, 0.6, 30)])
        fall = VMobject(color=RED, stroke_width=7)
        fall.set_points_smoothly([[x, symptom_y(x), 0] for x in np.linspace(0.6, 5.4, 30)])
        self.at("The team treated adult mice")
        self.play(Create(rise), run_time=2.0, rate_func=linear)
        self.at("already had symptoms")
        mk_l = DashedLine([0.6, ya, 0], [0.6, 3.0, 0], color=YELLOW, stroke_width=4)
        mk_t = T("tamoxifen", 26, YELLOW).move_to([0.6, 3.3, 0])
        band = Rectangle(width=5.0, height=5.4, stroke_width=0, fill_color=GREEN, fill_opacity=0.09).move_to([3.1, 0.3, 0])
        self.at("They gave")
        self.play(Create(mk_l), FadeIn(mk_t), run_time=0.6)
        self.at("which restored")
        rst = T("MeCP2 restored", 26, GREEN).move_to([3.1, -2.9, 0])
        self.play(FadeIn(band), FadeIn(rst), run_time=0.5)
        self.at("Many symptoms reversed")
        self.play(Create(fall), run_time=1.6)
        t1 = bchip("young adult mice", GREEN, 26).move_to([4.0, 2.55, 0])
        t2 = bchip("older adult mice", GREEN, 26).move_to([4.0, 1.5, 0])
        self.at("young adult mice")
        self.play(FadeIn(t1, shift=LEFT * 0.2), run_time=0.4)
        self.at("older adult mice")
        self.play(FadeIn(t2, shift=LEFT * 0.2), run_time=0.4)

        self.at("without the silenced gene")
        self.play(*[FadeOut(m) for m in (t1, t2)], FadeOut(rise), FadeOut(fall),
                   band.animate.set_fill(opacity=0.0), FadeOut(rst), run_time=0.5)
        flat = Line([-5.2, -1.9, 0], [5.4, -1.9, 0], color=GREY, stroke_width=7)
        fl = T("typical mice", 28, GREY).move_to([-3.0, -1.35, 0])
        self.play(Create(flat), FadeIn(fl), run_time=0.8)
        self.at("did nothing")
        nc = T("no change", 32, YELLOW, weight=BOLD).move_to([3.4, -1.35, 0])
        self.play(FadeIn(nc, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        circ = make_circuit((0, -0.1), 1.25)
        self.at("So in these mice")
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in circ.nodes], lag_ratio=0.1),
                  LaggedStart(*[Create(e) for e in circ.edges], lag_ratio=0.1), run_time=1.2)
        self.at("not permanently miswired")
        okl = T("not permanently miswired", 30, GREY).move_to([0, -3.15, 0])
        self.play(FadeIn(okl), run_time=0.4)
        self.at("formed without")
        wl = T("formed without MeCP2", 30, RED).move_to([0, -3.15, 0])
        self.play(ReplacementTransform(okl, wl), run_time=0.4)
        prot = bchip("MeCP2", BLUE, 28).move_to([0, 3.1, 0])
        pa = arr([0, 2.78, 0], [0, 2.45, 0], BLUE)
        self.at("worked again")
        self.play(FadeIn(prot, scale=1.2), run_time=0.4)
        self.play(GrowArrow(pa), run_time=0.4)
        wa = T("works again", 30, GREEN).move_to([0, -3.15, 0])
        self.play(circ.edges.animate.set_color(GREEN), circ.nodes.animate.set_color(GREEN),
                  ReplacementTransform(wl, wa), run_time=0.4)
        self.play(FadeOut(prot), FadeOut(pa), run_time=0.2)
        flow(self, circ)
        self.at("mouse result")
        mr = bchip("a mouse result", GREY, 28).move_to([3.6, 3.0, 0])
        self.play(FadeOut(wa), circ.animate.scale(0.85 / 1.25).move_to([-3.4, 0.2, 0]),
                  FadeIn(mr, shift=LEFT * 0.2), run_time=0.6)
        self.at("older person")
        op = bchip("older person", GREY, 28).move_to([2.4, 1.6, 0])
        qm = T("not known", 30, YELLOW, weight=BOLD).move_to([5.0, 1.6, 0])
        self.play(FadeIn(op), run_time=0.4)
        self.at("not known")
        self.play(FadeIn(qm, shift=LEFT * 0.1), run_time=0.5)

        # dose bar
        seg = []
        for x, w, c in [(1.7, 2.0, RED), (3.7, 0.8, GREEN), (4.5, 2.0, RED)]:
            seg.append(Rectangle(width=w, height=0.5, stroke_color=c, stroke_width=3, fill_color=c,
                                 fill_opacity=0.35).move_to([x + w / 2 - 0.0 - w / 2 + 0.0, -0.9, 0]))
        bar = VGroup(*seg).arrange(RIGHT, buff=0).move_to([3.6, -0.9, 0])
        dl = T("amount of MeCP2", 26, GREY).move_to([3.6, -0.3, 0])
        lo = T("too little", 24, RED).next_to(bar[0], DOWN, buff=0.2)
        hi = T("too much", 24, RED).next_to(bar[2], DOWN, buff=0.2)
        self.at("Too much")
        self.play(FadeIn(bar), FadeIn(dl), run_time=0.5)
        self.play(FadeIn(hi), FadeIn(lo), run_time=0.4)
        self.at("dose matters")
        self.play(Indicate(bar[1], color=GREEN, scale_factor=1.2), run_time=0.7)
        self.at("Circuits need some proteins")
        self.play(circ.edges.animate.set_color(GREEN), run_time=0.2)
        flow(self, circ, rt=1.1)
        flow(self, circ, rt=1.1)
        self.finish()


class S07End(EndCard):
    LINE = "Circuits need some proteins to keep running, not only to be built."
