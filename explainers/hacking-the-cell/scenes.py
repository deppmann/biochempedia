"""Hacking the cell: tools behind a stop, chosen by Cre  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  PURPLE = the reporter (GCaMP) and its gene
  BLUE   = the actuator (channelrhodopsin-2), its gene, and the blue light that opens it
  YELLOW = Cre, the enzyme that cuts
  GOLD   = the loxP sites (small triangles pointing the way the site points)
  RED    = the stop signal
  PINK   = calcium
  WHITE  = cations (plain dots)
  GREEN  = on: a gene being read, a cell that glows or fires
  GREY   = cells, DNA, silent genes, labels
No molecular structures: genes are blocks on a line, enzymes and tools are labelled chips,
cells are circles or rounded boxes, loxP sites are triangles.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
TEAL = PURPLE   # reporter colour in this film (house teal is too close to the actuator blue)
PINK = "#F08BB4"


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


# --- the six-cell tissue (scenes 1 and 6) --------------------------------------------------
GRID = [(-3.6, 1.45), (0, 1.45), (3.6, 1.45), (-3.6, -1.45), (0, -1.45), (3.6, -1.45)]
CHOSEN = 4   # bottom middle
CR = 1.2


def tissue():
    cells = VGroup(*[Circle(radius=CR, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([x, y, 0])
                     for x, y in GRID])
    return cells


def lit(c):
    return [c.animate.set_stroke(GREEN).set_fill(GREEN, 0.55)]


def dark(c):
    return [c.animate.set_stroke(GREY).set_fill(GREY, 0.15)]


# --- a gene row: [loxP] [stop] [loxP] [gene] -------------------------------------------------
def tri(x, y, s=0.5):
    t = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1, stroke_width=1).scale(s / 2).rotate(-PI / 2)
    return t.move_to([x, y, 0])


def gene_block(x, y, text, color, w=4.2, h=0.9, size=28):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.1).move_to([x, y, 0])
    lbl = T(text, size, color).move_to(box)
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(box)
    g = VGroup(back, box, lbl)
    g.box, g.lbl = box, lbl
    return g


def stop_block(x, y, w=2.4, h=0.9, size=28):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=RED, stroke_width=3,
                           fill_color=RED, fill_opacity=0.3).move_to([x, y, 0])
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(box)
    return VGroup(back, box, T("stop", size, RED, weight=BOLD).move_to(box))


def gene_on(g, color):
    return [g.box.animate.set_stroke(GREEN).set_fill(GREEN, 0.45), g.lbl.animate.set_color(GREEN)]


def row(y, text, color):
    line = Line([-6.0, y, 0], [6.0, y, 0], color=GREY, stroke_width=5)
    g_ = gene_block(2.6, y, text, color)
    stop = stop_block(-3.4, y)
    t1, t2 = tri(-5.0, y), tri(-1.8, y)
    r = VGroup(line, g_, stop, t1, t2)
    r.line, r.gene, r.stop, r.t1, r.t2 = line, g_, stop, t1, t2
    return r


ROW1, ROW2 = 1.35, -1.35


class S00Title(TitleCard):
    LESSON = "Hacking the Cell"
    TITLE = "Tools behind a stop, chosen by Cre"


class S01Problem(SpokenScene):
    def construct(self):
        cells = tissue()
        ch = cells[CHOSEN]
        self.play(FadeIn(cells), run_time=0.5)
        self.at("one type of neuron")
        tag = T("one neuron type", 24, TEXT).next_to(ch, DOWN, buff=0.1)
        ring = Circle(radius=CR + 0.12, color=TEXT, stroke_width=3).move_to(ch)
        self.play(Create(ring), FadeIn(tag), run_time=0.5)
        self.at("glows")
        self.play(*lit(ch), run_time=0.5)
        self.at("with light")
        self.play(ring.animate.set_stroke(BLUE, 6), run_time=0.4)
        self.play(Indicate(ring, color=BLUE, scale_factor=1.1), run_time=0.5)
        self.at("a promoter that every cell reads")
        pl = chip("promoter active in every cell", GOLD, size=24)
        pl.move_to([0, 3.15, 0]) if False else None
        lab = T("promoter + GFP gene: read in every cell", 24, GREEN).move_to([0, 3.15, 0])
        self.play(FadeIn(lab), FadeOut(tag), run_time=0.3)
        self.at("green mouse")
        self.play(*[a for c in cells for a in lit(c)], ring.animate.set_stroke(GREEN, 3), run_time=0.7)
        self.at("one cell type")
        how = chip("how?", GREY, size=28).move_to([0, -3.1, 0])
        tag = T("one neuron type", 24, TEXT).next_to(ch, DOWN, buff=0.1).shift(DOWN * 0.0)
        self.play(*[a for i, c in enumerate(cells) if i != CHOSEN for a in dark(c)], FadeOut(lab),
                  ring.animate.set_stroke(TEXT, 3), run_time=0.6)
        self.at("nowhere else")
        self.play(FadeIn(how, shift=UP * 0.2), run_time=0.4)
        self.finish()


class S02Tools(SpokenScene):
    def construct(self):
        L, R = -3.3, 3.3
        CY = -0.6
        def cellbox(x):
            return RoundedRectangle(corner_radius=0.5, width=5.6, height=4.2, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.15).move_to([x, CY, 0])
        cl, cr = cellbox(L), cellbox(R)
        self.play(FadeIn(cl), FadeIn(cr), run_time=0.5)
        self.at("a reporter")
        hl = chip("reporter", TEAL, size=30).move_to([L - 1.5, 2.0, 0])
        self.play(FadeIn(hl), run_time=0.4)
        self.at("changes its light")
        ca = chip("calcium", PINK, size=26).move_to([L - 2.1, -3.15, 0])
        self.play(FadeIn(ca), run_time=0.3)
        self.play(ca.animate.move_to([L, CY - 1.2, 0]), run_time=0.7)
        self.play(cl.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), run_time=0.5)
        self.at("calcium reporter")
        gc = chip("GCaMP", TEAL, size=30).move_to([L, CY + 0.7, 0])
        self.play(FadeIn(gc), run_time=0.4)

        self.at("an actuator")
        hr = chip("actuator", BLUE, size=30).move_to([R - 1.5, 2.0, 0])
        self.play(FadeIn(hr), run_time=0.4)
        self.at("is an actuator")
        px, top = R + 1.5, cr.get_top()[1]
        door = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.3, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.7).move_to([px, top, 0])
        cn = chip("channelrhodopsin-2", BLUE, size=24).move_to([R - 0.5, CY + 0.7, 0])
        self.play(FadeIn(door), FadeIn(cn), run_time=0.5)
        self.at("blue light")
        bl = arr([px, 3.4, 0], [px, top + 0.2, 0], BLUE, w=7)
        bt = T("blue light", 24, BLUE).move_to([px - 1.3, 3.0, 0])
        self.play(GrowArrow(bl), FadeIn(bt), run_time=0.5)
        self.at("opens its pore")
        self.play(door.animate.shift(RIGHT * 0.9).set_opacity(0.0), run_time=0.5)
        self.at("Casions flow")
        ions = VGroup(*[Circle(radius=0.14, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.9)
                        .move_to([px - 0.35 + 0.35 * i, top + 0.8, 0]) for i in range(3)])
        lab = T("cations", 22, TEXT).move_to([px + 0.0, top + 1.2, 0]).shift(RIGHT * 0.0)
        lab.move_to([px - 1.9, top + 0.8, 0]) if False else None
        self.play(FadeIn(ions), run_time=0.3)
        self.play(ions.animate.shift(DOWN * 3.0), run_time=0.8)
        ct = T("cations", 22, TEXT).next_to(ions, LEFT, buff=0.2)
        self.play(FadeIn(ct), run_time=0.2)
        self.at("the neuron fires")
        fire = T("fires", 30, GREEN, weight=BOLD).move_to([R - 0.5, -1.9, 0])
        self.play(cr.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), FadeIn(fire), run_time=0.4)
        self.play(Indicate(cr, color=GREEN, scale_factor=1.04), run_time=0.5)
        self.finish()


class S03Stop(SpokenScene):
    def construct(self):
        r1 = row(ROW1, "reporter gene", TEAL)
        self.play(Create(r1.line), FadeIn(r1.gene), run_time=0.6)
        self.at("a stop signal")
        self.play(FadeIn(r1.stop, shift=DOWN * 0.3), run_time=0.5)
        self.at("two sites called")
        lbl1 = T("loxP", 24, GOLD).next_to(r1.t1, DOWN, buff=0.35)
        lbl2 = T("loxP", 24, GOLD).next_to(r1.t2, DOWN, buff=0.35)
        self.play(FadeIn(r1.t1, shift=RIGHT * 0.3), FadeIn(r1.t2, shift=LEFT * 0.3), FadeIn(lbl1), FadeIn(lbl2), run_time=0.6)
        self.at("point the same way")
        self.play(Indicate(r1.t1, color=TEXT, scale_factor=1.5), Indicate(r1.t2, color=TEXT, scale_factor=1.5), run_time=0.7)
        self.at("actuator gene")
        r2 = row(ROW2, "actuator gene", BLUE)
        self.play(Create(r2.line), FadeIn(r2.gene), FadeIn(r2.stop), FadeIn(r2.t1), FadeIn(r2.t2), run_time=0.8)
        self.at("neither gene is read")
        s1 = T("silent", 24, GREY).next_to(r1.gene, DOWN, buff=0.15)
        s2 = T("silent", 24, GREY).next_to(r2.gene, DOWN, buff=0.15)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.4)
        self.finish()


class S04Cre(SpokenScene):
    def construct(self):
        r1, r2 = row(ROW1, "reporter gene", TEAL), row(ROW2, "actuator gene", BLUE)
        l1 = [T("loxP", 24, GOLD).next_to(r1.t1, DOWN, buff=0.35), T("loxP", 24, GOLD).next_to(r1.t2, DOWN, buff=0.35)]
        s1 = T("silent", 24, GREY).next_to(r1.gene, DOWN, buff=0.15)
        s2 = T("silent", 24, GREY).next_to(r2.gene, DOWN, buff=0.15)
        self.add(r1, r2, *l1, s1, s2)
        self.at("an enzyme")
        c1 = chip("Cre", YELLOW, size=30).move_to([-3.4, ROW1 + 1.4, 0])
        c2 = chip("Cre", YELLOW, size=30).move_to([-3.4, ROW2 + 1.4 - 0.2, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.3), FadeIn(c2, shift=DOWN * 0.3), run_time=0.5)
        self.at("cuts and rejoins")
        self.play(Indicate(c1, color=YELLOW, scale_factor=1.15), Indicate(c2, color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.at("removes what lies between")
        self.play(*[m.animate.shift(UP * 0.9).set_opacity(0.0) for r in (r1, r2) for m in (r.stop, r.t1, r.t2)],
                  *[FadeOut(l) for l in l1], run_time=0.8)
        self.at("the stop is cut out")
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.6)
        self.at("cut is permanent")
        a1 = arr([0.6, ROW1 + 0.75, 0], [4.6, ROW1 + 0.75, 0], GREEN, w=6)
        a2 = arr([0.6, ROW2 + 0.75, 0], [4.6, ROW2 + 0.75, 0], GREEN, w=6)
        rd1 = T("read", 24, GREEN).move_to(s1)
        rd2 = T("read", 24, GREEN).move_to(s2)
        self.play(*gene_on(r1.gene, TEAL), *gene_on(r2.gene, BLUE), FadeOut(s1), FadeOut(s2), FadeIn(rd1), FadeIn(rd2),
                  GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        self.at("its descendants")
        d = T("that cell and its descendants can read it", 26, GREY).move_to([0, -3.25, 0])
        self.play(FadeIn(d), run_time=0.5)
        self.finish()


def mini(ox, y, text, color):
    t1, t2 = tri(ox - 2.1, y, 0.4), tri(ox - 0.55, y, 0.4)
    st = stop_block(ox - 1.32, y, w=0.95, h=0.7, size=22)
    g_ = gene_block(ox + 1.3, y, text, color, w=1.9, h=0.7, size=22)
    line = Line([ox - 2.4, y, 0], [ox + 2.25, y, 0], color=GREY, stroke_width=4)
    r = VGroup(line, t1, t2, st, g_)
    r.stop, r.gene, r.t1, r.t2 = st, g_, t1, t2
    return r


class S05Address(SpokenScene):
    def construct(self):
        xs = (-3.3, 3.3)
        boxes = [RoundedRectangle(corner_radius=0.5, width=5.9, height=5.4, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.15).move_to([x, -0.2, 0]) for x in xs]
        heads = [T("one cell type", 26, TEXT).move_to([xs[0], 3.05, 0]), T("every other cell", 26, TEXT).move_to([xs[1], 3.05, 0])]
        rows = {}
        for i, x in enumerate(xs):
            rows[i] = (mini(x, -0.1, "reporter", TEAL), mini(x, -1.7, "actuator", BLUE))
        self.play(*[FadeIn(b) for b in boxes], *[FadeIn(h) for h in heads],
                  *[FadeIn(r) for i in rows for r in rows[i]], run_time=0.7)
        self.at("make it from a promoter")
        cre = chip("Cre", YELLOW, size=30).move_to([xs[0], 1.55, 0])
        self.play(FadeIn(cre, shift=DOWN * 0.3), run_time=0.5)
        self.at("cuts out the stops")
        self.play(*[m.animate.shift(UP * 0.7).set_opacity(0.0) for r in rows[0] for m in (r.stop, r.t1, r.t2)],
                  Indicate(cre, color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.at("makes both proteins")
        self.play(*gene_on(rows[0][0].gene, TEAL), *gene_on(rows[0][1].gene, BLUE),
                  boxes[0].animate.set_stroke(GREEN), run_time=0.6)
        self.at("most other cells")
        ghost = chip("Cre", GREY, size=30).move_to([xs[1], 1.55, 0])
        self.play(FadeIn(ghost), run_time=0.3)
        self.play(Create(strike(ghost)), run_time=0.3)
        self.at("stay in place")
        self.play(*[Indicate(r.stop, color=RED, scale_factor=1.12) for r in rows[1]], run_time=0.7)
        self.finish()


def s05_end():
    xs = (-3.3, 3.3)
    g = VGroup()
    for i, x in enumerate(xs):
        b = RoundedRectangle(corner_radius=0.5, width=5.9, height=5.4, stroke_color=GREEN if i == 0 else GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.15).move_to([x, -0.2, 0])
        g.add(b, T("one cell type" if i == 0 else "every other cell", 26, TEXT).move_to([x, 3.05, 0]))
        for y, tx, col in ((-0.1, "reporter", TEAL), (-1.7, "actuator", BLUE)):
            r = mini(x, y, tx, col)
            if i == 0:
                r.remove(r.stop, r.t1, r.t2)
                r.gene.box.set_stroke(GREEN).set_fill(GREEN, 0.45)
                r.gene.lbl.set_color(GREEN)
                g.add(r)
            else:
                g.add(r)
        c = chip("Cre", YELLOW if i == 0 else GREY, size=30).move_to([x, 1.55, 0])
        g.add(c)
        if i == 1:
            g.add(strike(c))
    return g


class S06Mouse(SpokenScene):
    def construct(self):
        def part(txt, color):
            t = T(txt, 26, color)
            b = RoundedRectangle(corner_radius=0.16, width=3.7, height=1.7, stroke_color=color, stroke_width=3,
                                 fill_color=color, fill_opacity=0.16)
            return VGroup(b, t.move_to(b))
        p1 = part("Cre\nin a gene only your\nneuron type reads", YELLOW)
        p2 = part("reporter\nbehind a stop", TEAL)
        p3 = part("actuator\nbehind a stop", BLUE)
        parts = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.5).move_to([0, 0.3, 0])
        prev = s05_end()
        self.add(prev)
        self.wait(0.5)
        self.at("breed three parts")
        self.play(FadeOut(prev), run_time=0.3)
        self.play(FadeIn(T("breed three parts together", 28, GREY).move_to([0, 2.2, 0])), run_time=0.4)
        self.at("The first is Kree")
        self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.5)
        self.at("the second is")
        self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.5)
        self.at("the third is")
        self.play(FadeIn(p3, shift=UP * 0.2), run_time=0.5)
        self.at("cells that make")
        cells = tissue()
        ch = cells[CHOSEN]
        rep = chip("reporter", TEAL, size=22).move_to(ch.get_center() + UP * 0.38)
        act = chip("actuator", BLUE, size=22).move_to(ch.get_center() + DOWN * 0.38)
        for m in self.mobjects:
            pass
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        self.play(FadeIn(cells), run_time=0.5)
        self.at("remove the stops")
        self.play(*lit(ch), FadeIn(rep), FadeIn(act), run_time=0.7)
        self.at("both proteins")
        self.play(Indicate(ch, color=GREEN, scale_factor=1.06), run_time=0.7)
        self.at("keep this rule")
        rule = T("tools wait behind stops; only cells that make Cre remove them", 26, TEXT)
        fit(rule, max_w=11.8)
        rule.move_to([0, -3.2, 0])
        self.play(FadeIn(rule), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Tools wait behind stops. Only cells that make Cre remove them."
