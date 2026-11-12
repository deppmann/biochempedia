"""One Cell, One Shipping Line (organelles-as-a-system, film 1).

THE WORLD (kept for the whole film): one beta cell, a straight shipping line at y = -0.1.
COLOUR MAP: NUCLEUS = deep blue; mRNA = purple; ROUGH ER = teal ribbons + dark dots; GOLGI = orange sacs;
VESICLES / insulin = gold; CELL MEMBRANE = grey; MITOCHONDRIA = red; ATP = yellow sparks.
Schematic, not to scale.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
NUCB = "#5B7CFA"
ORANGE = "#F29E4C"
RY = -0.1                                   # the shipping line
CELL_C = np.array([-0.5, -0.55, 0])
NUC_C = np.array([-4.5, RY, 0])
NUC_R = 1.4
ER_C = np.array([-0.8, RY, 0])
GO_C = np.array([2.5, RY, 0])
V1 = np.array([1.0, RY, 0])
V2 = np.array([4.2, RY, 0])
MEM = np.array([5.13, RY, 0])
LUM = np.array([-0.8, 0.225, 0])            # a gap inside the ER where the protein folds
RIBO = np.array([-1.3, 0.72, 0])            # the ribosome we follow
STOPS = ["nucleus", "ribosome", "vesicle", "Golgi", "vesicle", "membrane"]


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- parts
def cell_m():
    return Ellipse(width=11.4, height=5.4, stroke_color=GREY, stroke_width=8, fill_color=GREY,
                   fill_opacity=0.10).move_to(CELL_C)


def nuc_m():
    return Circle(radius=NUC_R, stroke_color=NUCB, stroke_width=6, fill_color=NUCB, fill_opacity=0.24).move_to(NUC_C)


def nuc_label():
    return T("nucleus", 26, "#A9BBFF").move_to(NUC_C + DOWN * 1.2).set_stroke(BG, 8, background=True)


def coil_f(t):
    return NUC_C + np.array([0.95 * np.sin(6 * np.pi * t + 0.3), 0.8 * np.sin(4 * np.pi * t), 0])


def coil_m(a=0.0, b=1.0, color=NUCB, w=6):
    return ParametricFunction(coil_f, t_range=[a, b], color=color, stroke_width=w)


GENE_AB = (0.60, 0.70)


def gene_m(w=10):
    return coil_m(*GENE_AB, color=GOLD, w=w)


def gene_pt():
    return coil_f(sum(GENE_AB) / 2)


def er_m(phase=0.0):
    rib = VGroup()
    for off in (0.65, 0.0, -0.65):
        rib.add(ParametricFunction(lambda x, o=off: P(x, RY + o + 0.1 * np.sin(2 * np.pi * (x + 0.8) / 0.8 + phase)),
                                   t_range=[-2.0, 0.4], color=TEAL, stroke_width=11))
    return rib


def er_live(scene, op=1.0, speed=1.0):
    tr = ValueTracker(0)
    tr.add_updater(lambda t, dt: t.increment_value(dt * speed))
    scene.add(tr)
    er = always_redraw(lambda: er_m(tr.get_value()).set_stroke(opacity=op))
    scene.add(er)
    return er


def dots_m():
    d = VGroup()
    for k in range(5):
        x = -1.8 + 0.5 * k + 0.1
        for y in (RY + 0.65 + 0.2, RY - 0.65 - 0.2):
            d.add(Dot(P(x, y), radius=0.09, color=BG).set_stroke(TEXT, 2.5).set_fill(BG, 1))
    return d


def golgi_m():
    g = VGroup()
    for i in range(5):
        x0 = 1.6 + 0.45 * i
        h = 0.95 - 0.1 * abs(i - 2)
        g.add(ParametricFunction(lambda t, x0=x0, h=h: P(x0 + 0.2 * (1 - (t / h) ** 2), RY + t), t_range=[-h, h],
                                 color=ORANGE, stroke_width=14))
    return g


def glow_m(pos, r=0.2, op=1.0):
    return VGroup(Circle(r * 2.2, stroke_width=0, fill_color=GOLD, fill_opacity=0.10 * op),
                  Circle(r * 1.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.18 * op),
                  Circle(r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.9 * op)).move_to(pos)


def ves_m(pos, prot=True):
    v = Circle(radius=0.28, stroke_color=GOLD, stroke_width=4.5, fill_color=GOLD, fill_opacity=0.13).move_to(pos)
    return VGroup(v, glow_m(pos, 0.1)) if prot else VGroup(v)


def lock_m(pos, s=1.0):
    body = RoundedRectangle(corner_radius=0.05, width=0.42 * s, height=0.34 * s, stroke_color=TEXT, stroke_width=2,
                            fill_color=TEXT, fill_opacity=0.9)
    sh = Arc(radius=0.13 * s, start_angle=0, angle=PI, stroke_color=TEXT, stroke_width=4.5).next_to(body, UP, buff=-0.01)
    return VGroup(sh, body).move_to(pos)


def spark_m(pos):
    return Star(n=4, outer_radius=0.15, inner_radius=0.06, color=YELLOW, fill_color=YELLOW, fill_opacity=1,
                stroke_width=1).move_to(pos)


def mito_m(pos):
    return Ellipse(width=1.5, height=0.72, stroke_color=RED, stroke_width=4.5, fill_color=RED, fill_opacity=0.28).move_to(pos)


MITO_POS = [P(-3.0, -2.45), P(2.0, -2.45)]
POOL_C = P(-0.4, -1.65)


def pool_m(w=6.6):
    return Ellipse(width=w, height=0.7, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.14).move_to(POOL_C)


def mito_label():
    return T("mitochondria", 26, RED).move_to(P(-0.5, -2.45))


def pool_label():
    return T("energy supply (schematic)", 24, YELLOW).move_to(POOL_C)


def mrna_m(c, L=0.9, w=6):
    return ParametricFunction(lambda t: c + P(t, 0.09 * np.sin(9 * t)), t_range=[-L / 2, L / 2], color=PURPLE, stroke_width=w)


def strip_m(lit=()):
    chips = [chip(s, PURPLE if i == 0 else GOLD, size=24, pad=0.12) for i, s in enumerate(STOPS)]
    items = []
    for i, c in enumerate(chips):
        if i:
            items.append(T("→", 24, GREY))
        items.append(c)
    g = VGroup(*items).arrange(RIGHT, buff=0.14).move_to(P(0, 3.4))
    g.chips = chips
    for i, c in enumerate(chips):
        _style(c, i in lit)
    return g


def _style(c, on):
    col = c[0].get_stroke_color()
    c[0].set_stroke(opacity=1 if on else 0.3, width=4 if on else 2.5).set_fill(col, 0.4 if on else 0.08)
    c[1].set_opacity(1 if on else 0.4)


def light(g, idx):
    out = []
    for i, c in enumerate(g.chips):
        on = i in idx
        col = c[0].get_stroke_color()
        out.append(c[0].animate.set_stroke(opacity=1 if on else 0.3, width=4 if on else 2.5).set_fill(col, 0.4 if on else 0.08))
        out.append(c[1].animate.set_opacity(1 if on else 0.4))
    return out


def route_purple():
    return Line(P(-3.1, RY), P(-2.0, RY), color=PURPLE, stroke_width=9)


def route_gold():
    return Line(P(0.4, RY), MEM, color=GOLD, stroke_width=8).set_z_index(-2)


def dashed_route():
    return VGroup(DashedLine(P(-3.1, RY), P(-2.0, RY), color=PURPLE, stroke_width=6, dash_length=0.12),
                  DashedLine(P(0.4, RY), MEM, color=GOLD, stroke_width=6, dash_length=0.12)).set_z_index(-2)


# ---------------------------------------------------------------- motion helpers
def bob(m, amp=0.08, period=2.2):
    m._bt = 0.0

    def u(mm, dt):
        a = np.sin(2 * np.pi * mm._bt / period)
        mm._bt += dt
        b = np.sin(2 * np.pi * mm._bt / period)
        mm.shift(UP * amp * (b - a))
    m.add_updater(u)
    return m


def breathe(m, amp=0.06, period=2.6):
    m._bt = 0.0
    m._cur = 1.0

    def u(mm, dt):
        mm._bt += dt
        tgt = 1 + amp * np.sin(2 * np.pi * mm._bt / period)
        mm.scale(tgt / mm._cur)
        mm._cur = tgt
    m.add_updater(u)
    return m


def motes(scene, n=26):
    rng = np.random.RandomState(7)
    g = VGroup()
    for i in range(n):
        d = Dot(radius=rng.uniform(0.07, 0.13), color=TEAL if i % 2 else GREY).set_opacity(0.55)
        d.move_to([rng.uniform(-5, 4), rng.uniform(-2.4, 1.9), 0])
        d.v = np.array([rng.uniform(-0.7, 0.7), rng.uniform(-0.5, 0.5), 0])

        def u(m, dt):
            m.shift(m.v * dt)
            p = m.get_center()
            if ((p[0] - CELL_C[0]) / 5.5) ** 2 + ((p[1] - CELL_C[1]) / 2.5) ** 2 > 1:
                m.v = -m.v
        d.add_updater(u)
        g.add(d)
    g.set_z_index(-1)
    scene.add(g)
    return g


def shimmer(m, lo=0.55, hi=1.0, period=2.0):
    m._st = 0.0

    def u(mm, dt):
        mm._st += dt
        mm.set_opacity(lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * mm._st / period)))
    m.add_updater(u)
    return m


def shimmer_fill(m, lo=0.08, hi=0.22, period=2.0):
    m._st = 0.0

    def u(mm, dt):
        mm._st += dt
        mm.set_fill(YELLOW, lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * mm._st / period)))
    m.add_updater(u)
    return m


def world(scene, nuc=True, with_motes=True):
    c, n, nl = cell_m(), nuc_m(), nuc_label()
    scene.add(c, n, nl)
    if with_motes:
        motes(scene)
    return c, n, nl


class Lit(SpokenScene):
    pass


# ================================================================ S00
class S00Title(TitleCard):
    LESSON = "Organelles as a System"
    TITLE = "One Cell, One Shipping Line"


# ================================================================ S01
class S01Question(SpokenScene):
    def construct(self):
        cm = cell_m()
        nm = nuc_m()
        self.play(Create(cm), FadeIn(nm), run_time=1.2)
        motes(self)
        nl = nuc_label()
        self.add(nl)
        self.at("never leaves")
        lk = lock_m(NUC_C + UP * 0.1, 1.6)
        gl = T("gene stays here", 28, TEXT).move_to(P(-4.2, 2.5))
        self.play(FadeIn(lk, scale=1.4), FadeIn(gl), run_time=0.9)
        self.play(Indicate(lk, scale_factor=1.15), run_time=1.0)
        self.at("how does insulin end up")
        glow = glow_m(P(6.0, RY), 0.38)
        ins = T("insulin", 28, GOLD).move_to(P(6.0, RY - 0.85))
        q = T("?", 110, GOLD, font=TITLE_FONT).move_to(P(0.2, RY))
        self.play(FadeIn(glow, scale=0.6), FadeIn(ins), FadeIn(q, scale=0.6), run_time=1.0)
        bob(q, 0.12, 1.8)
        breathe(glow, 0.1, 2.0)
        self.at("After a meal")
        plate = VGroup(Circle(0.3, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.1),
                       Circle(0.17, stroke_color=GREY, stroke_width=2)).move_to(P(3.3, 2.55))
        items = VGroup(Dot(P(3.22, 2.55), 0.07, color=GREEN), Dot(P(3.38, 2.6), 0.07, color=RED))
        sug = T("blood sugar", 26, TEXT).move_to(P(4.9, 2.55))
        ar = Arrow(P(6.2, 2.3), P(6.2, 2.85), buff=0, color=GOLD, stroke_width=6, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(plate), FadeIn(items), run_time=0.7)
        self.at("blood sugar rises")
        self.play(FadeIn(sug), GrowArrow(ar), run_time=0.9)
        self.at("beta cells")
        bl = T("beta cell", 28, GREY).move_to(P(-0.5, -3.55))
        self.play(FadeIn(bl), FadeOut(VGroup(plate, items, sug, ar)), run_time=0.8)
        self.at("release this")
        st = strip_m(())
        self.play(FadeIn(st, shift=DOWN * 0.2), Indicate(glow, scale_factor=1.3), run_time=1.0)
        self.finish()


# ================================================================ S02
class S02Line(SpokenScene):
    def construct(self):
        world(self)
        glow = glow_m(P(6.0, RY), 0.38)
        breathe(glow, 0.1, 2.0)
        ins = T("insulin", 28, GOLD).move_to(P(6.0, RY - 0.85))
        st = strip_m(())
        self.add(glow, ins, st)
        parts = VGroup(er_m(), dots_m(), golgi_m(), ves_m(V1), ves_m(V2)).set_opacity(0)
        self.add(parts)
        self.at("Here is the answer")
        dr = dashed_route()
        self.play(parts.animate.set_opacity(0.4), Create(dr), run_time=2.4)
        self.at("First")
        lab1 = T("copy of instructions", 28, PURPLE).move_to(P(-1.6, 1.4))
        strand = mrna_m(NUC_C + RIGHT * 1.0 + UP * RY * 0 + P(0, RY) - NUC_C, 0.7)
        strand.move_to(P(-3.1, RY))
        self.play(FadeIn(lab1), FadeIn(strand), run_time=0.6)
        self.play(strand.animate.move_to(P(-2.0, RY)), run_time=1.6)
        self.at("then the protein itself")
        lab2 = T("protein", 28, GOLD).move_to(P(2.0, 1.4))
        parcel = glow_m(P(-0.8, 0.225), 0.12)
        self.play(FadeIn(lab2), FadeOut(strand), FadeIn(parcel), run_time=0.6)
        for p in (P(0.4, RY), V1, P(2.5, RY), V2, MEM):
            self.play(parcel.animate.move_to(p), run_time=0.42, rate_func=linear)
        self.at("Each part can only")
        self.play(FadeOut(VGroup(lab1, lab2, parcel)), dr.animate.set_opacity(0.4), run_time=0.7)
        seq = [er_m, dots_m]
        stops = VGroup(parts[0], parts[2], parts[3], parts[4])
        for s in (parts[0], parts[3], parts[2], parts[4]):
            self.play(s.animate.set_opacity(1).scale(1.06), run_time=0.5)
            self.play(s.animate.set_opacity(0.4).scale(1 / 1.06), run_time=0.4)
        self.finish()


# ================================================================ S03
class S03Nucleus(SpokenScene):
    def construct(self):
        world(self)
        st = strip_m((0,))
        self.add(st)
        self.at("Start in the nucleus")
        self.play(Indicate(self.mobjects[1], color=NUCB, scale_factor=1.06), run_time=1.0)
        self.at("holds most")
        coil = coil_m()
        self.play(Create(coil), run_time=1.0)
        self.at("DNA")
        pt = min((coil_f(k / 400) for k in range(400)), key=lambda p: np.linalg.norm(p - P(-3.7, -0.6)))
        dna = T("DNA", 30, NUCB).move_to(P(-2.55, -1.25))
        dl = Line(dna.get_left() + LEFT * 0.05, pt, color=NUCB, stroke_width=2.5)
        self.play(FadeIn(dna), Create(dl), run_time=0.8)
        self.at("its instructions")
        self.play(coil.animate.set_stroke(width=7), rate_func=there_and_back, run_time=1.4)
        self.at("The gene for insulin")
        g = gene_m()
        gl = T("insulin gene", 30, GOLD).move_to(P(-0.9, 1.35))
        gline = Line(gl.get_left() + LEFT * 0.05, gene_pt() + RIGHT * 0.25, color=GOLD, stroke_width=2.5)
        self.play(Create(g), FadeIn(gl), Create(gline), run_time=1.2)
        shimmer(g, 0.6, 1.0, 1.6)
        self.at("one stretch of")
        self.play(Indicate(g, color=GOLD, scale_factor=1.2), run_time=1.2)
        self.at("But the gene itself")
        lk = lock_m(gene_pt() + UP * 0.1, 1.3)
        self.play(FadeIn(lk, scale=1.5), run_time=0.7)
        self.play(Indicate(lk, scale_factor=1.15), run_time=0.9)
        self.finish()


def nuc_with_gene(scene, lock=True):
    coil, g = coil_m(), gene_m()
    scene.add(coil, g)
    shimmer(g, 0.6, 1.0, 1.6)
    if lock:
        scene.add(lock_m(gene_pt() + UP * 0.1, 1.3))
    return coil, g


# ================================================================ S04
class S04Predict(SpokenScene):
    def construct(self):
        world(self)
        self.add(strip_m((0,)))
        nuc_with_gene(self, lock=False)
        self.at("Here is a puzzle")
        self.wait(1.2)
        self.at("The gene stays")
        lk = lock_m(gene_pt() + UP * 0.1, 1.3)
        self.play(FadeIn(lk, scale=1.5), run_time=0.7)
        self.at("So what leaves")
        ring_o = DashedVMobject(Ellipse(width=0.9, height=0.55, color=PURPLE, stroke_width=4), num_dashes=16).move_to(P(-2.55, RY))
        q = T("?", 90, GOLD, font=TITLE_FONT).move_to(P(-2.55, 1.0))
        self.play(FadeIn(ring_o), FadeIn(q, scale=0.6), run_time=1.0)
        bob(q, 0.1, 1.6)
        self.at("carrying its instructions")
        self.play(Indicate(ring_o, color=PURPLE, scale_factor=1.3), run_time=1.4)
        self.finish()


# ================================================================ S05
class S05Pause(SpokenScene):
    def construct(self):
        world(self)
        self.add(strip_m((0,)))
        nuc_with_gene(self, lock=False)
        self.add(lock_m(gene_pt() + UP * 0.1, 1.3))
        ring_o = DashedVMobject(Ellipse(width=0.9, height=0.55, color=PURPLE, stroke_width=4), num_dashes=16).move_to(P(-2.55, RY))
        q = T("?", 90, GOLD, font=TITLE_FONT).move_to(P(-2.55, 1.0))
        bob(q, 0.1, 1.6)
        shimmer(ring_o, 0.4, 1.0, 1.4)
        tr = ValueTracker(0)
        ctr = P(0.3, 1.15)
        base = Circle(0.5, color=GREY, stroke_width=5).move_to(ctr)
        arc = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.001),
                                        color=GOLD, stroke_width=8, arc_center=ctr))
        self.add(ring_o, q, base, arc)
        self.play(tr.animate.set_value(1), run_time=5.0, rate_func=linear)
        self.finish()


# ================================================================ S06
class S06Reveal(SpokenScene):
    def construct(self):
        world(self)
        self.add(strip_m((0,)))
        nuc_with_gene(self, lock=False)
        self.add(lock_m(gene_pt() + UP * 0.1, 1.3))
        er_live(self, 0.4)
        self.add(dots_m().set_stroke(opacity=0.4))
        self.at("A copy")
        self.wait(0.8)
        self.at("the cell copies the gene")
        strand = mrna_m(gene_pt(), 0.9)
        lab = T("messenger RNA (a copy)", 28, PURPLE).move_to(P(-0.7, 1.35))
        self.play(Create(strand), run_time=1.6)
        self.play(FadeIn(lab), Indicate(strand, color=PURPLE, scale_factor=1.15), run_time=1.0)
        self.at("leaves the nucleus")
        self.play(strand.animate.move_to(P(-2.55, RY)), run_time=2.0)
        self.at("carries the instructions")
        rp = route_purple()
        self.play(Create(rp), strand.animate.move_to(P(-2.05, RY)), run_time=2.2)
        self.finish()


# ================================================================ S07
class S07Ribosome(SpokenScene):
    def construct(self):
        world(self)
        st = strip_m((0,))
        self.add(st)
        coil = coil_m()
        g = gene_m()
        self.add(coil, g, lock_m(gene_pt() + UP * 0.1, 1.3), route_purple())
        er = er_live(self)
        dots = dots_m()
        self.add(dots)
        strand = mrna_m(P(-2.05, RY), 0.9)
        self.add(strand)
        self.at("ribosome on")
        self.play(*light(st, (1,)), run_time=0.4)
        big = Dot(RIBO, radius=0.2, color=BG).set_stroke(TEXT, 4).set_fill(BG, 1)
        rl = T("ribosome", 28, TEXT).move_to(RIBO + UP * 1.0 + LEFT * 0.9)
        self.play(FadeIn(big, scale=2.5), FadeIn(rl), run_time=0.9)
        self.at("The ER is")
        self.play(Indicate(dots, color=TEAL, scale_factor=1.3), run_time=1.2)
        self.at("folded membranes")
        erl = T("rough ER", 28, TEAL).move_to(P(-0.8, -1.5))
        self.play(FadeIn(erl), run_time=0.5)
        self.at("ribosomes dot")
        self.play(LaggedStart(*[Indicate(d, color=TEXT, scale_factor=1.7) for d in dots], lag_ratio=0.1), run_time=2.2)
        self.at("A ribosome reads")
        self.play(FadeOut(rl), strand.animate.move_to(RIBO + UP * 0.45 + LEFT * 0.0), run_time=1.6)
        self.at("links building blocks")
        path = lambda t: P(-1.3 + 0.22 * np.sin(2 * PI * t * 2.5), 0.95 + 1.0 * t)
        chain_line = ParametricFunction(path, t_range=[0, 1], color=GOLD, stroke_width=5)
        beads = VGroup(*[Dot(path(i / 8), radius=0.1, color=GOLD) for i in range(9)])
        cl = T("protein chain", 28, GOLD).move_to(P(0.5, 1.6))
        self.play(Create(chain_line), LaggedStart(*[FadeIn(b, scale=0.3) for b in beads], lag_ratio=0.25), FadeIn(cl), run_time=3.2)
        self.at("threads into")
        lum = lambda t: P(-1.5 + 1.4 * t, 0.225 + 0.08 * np.sin(2 * PI * t * 2))
        chain2 = ParametricFunction(lum, t_range=[0, 1], color=GOLD, stroke_width=5)
        beads2 = VGroup(*[Dot(lum(i / 8), radius=0.09, color=GOLD) for i in range(9)])
        self.play(Transform(chain_line, chain2), Transform(beads, beads2), FadeOut(cl), FadeOut(big),
                  strand.animate.move_to(P(-2.05, RY)), run_time=1.8)
        self.at("where it folds")
        prot = glow_m(LUM, 0.17)
        self.play(Transform(chain_line, prot), FadeOut(beads), run_time=1.4)
        self.play(Indicate(chain_line, color=GOLD, scale_factor=1.4), run_time=0.8)
        self.finish()


# ================================================================ S08
class S08Vesicle(SpokenScene):
    def construct(self):
        world(self)
        st = strip_m((1,))
        self.add(st, route_purple())
        self.add(coil_m(), gene_m(), lock_m(gene_pt() + UP * 0.1, 1.3))
        er_live(self)
        self.add(dots_m())
        prot = glow_m(LUM, 0.17)
        self.add(prot)
        breathe(prot, 0.15, 1.6)
        self.at("Now the protein")
        self.play(Indicate(prot, color=GOLD, scale_factor=1.5), run_time=1.2)
        self.at("A vesicle")
        self.play(*light(st, (2,)), run_time=0.4)
        vl = T("vesicle", 28, GOLD).move_to(P(1.0, 1.3))
        self.play(FadeIn(vl), run_time=0.6)
        self.at("buds off")
        bud = Circle(0.1, stroke_color=TEAL, stroke_width=4.5, fill_color=TEAL, fill_opacity=0.2).move_to(P(0.3, 0.225))
        self.play(FadeIn(bud), run_time=0.4)
        self.play(prot.animate.move_to(P(0.3, 0.225)), bud.animate.scale(2.8).set_stroke(GOLD).set_fill(GOLD, 0.13),
                  run_time=1.8)
        self.at("It carries")
        rg = route_gold()
        unit = VGroup(bud, prot)
        self.play(unit.animate.move_to(P(0.55, RY)), run_time=1.0)
        self.play(unit.animate.move_to(P(1.25, RY)), Create(Line(P(0.4, RY), P(1.25, RY), color=GOLD, stroke_width=6)),
                  run_time=1.2)
        self.at("Golgi apparatus")
        gg = golgi_m().set_opacity(0.5)
        self.add(gg)
        self.play(gg.animate.set_opacity(1), run_time=1.2)
        self.finish()


# ================================================================ S09
class S09Golgi(SpokenScene):
    def construct(self):
        world(self)
        st = strip_m((3,))
        self.add(st, route_purple())
        self.add(coil_m(), gene_m(), lock_m(gene_pt() + UP * 0.1, 1.3))
        er_live(self)
        self.add(dots_m())
        self.add(Line(P(0.4, RY), P(1.25, RY), color=GOLD, stroke_width=6))
        gg = golgi_m()
        self.add(gg)
        v = ves_m(P(1.25, RY))
        self.add(v)
        self.at("The Golgi is")
        gl = T("Golgi apparatus", 28, ORANGE).move_to(P(1.5, 1.25))
        self.play(FadeIn(gl), run_time=0.5)
        self.at("flat sacs")
        self.play(LaggedStart(*[Indicate(s, color=ORANGE, scale_factor=1.12) for s in gg], lag_ratio=0.25), run_time=2.0)
        self.at("It sorts")
        self.play(v.animate.move_to(P(1.6, RY)), run_time=0.4)
        pg = glow_m(P(1.6, RY), 0.1)
        self.play(FadeOut(v[0]), Transform(v[1], pg), run_time=0.2)
        for i in range(1, 5):
            self.play(v[1].animate.move_to(P(1.6 + 0.45 * i, RY)), run_time=0.25)
        self.at("packs it into new vesicles")
        cl = [ves_m(P(3.9, RY + 0.5)), ves_m(P(4.1, RY - 0.05)), ves_m(P(3.9, RY - 0.6))]
        self.play(FadeOut(v[1]), *[FadeIn(c, scale=0.4) for c in cl], run_time=1.4)
        for c in cl:
            bob(c, 0.05, 2.0 + 0.3 * cl.index(c))
        self.at("until it is needed")
        sr = T("stored, ready", 28, GOLD).move_to(P(3.2, -1.5))
        self.play(FadeIn(sr), run_time=0.6)
        self.finish()


# ================================================================ S10
class S10Release(SpokenScene):
    def construct(self):
        world(self)
        st = strip_m((4,))
        self.add(st, route_purple())
        self.add(coil_m(), gene_m(), lock_m(gene_pt() + UP * 0.1, 1.3))
        er_live(self)
        self.add(dots_m(), golgi_m())
        self.add(Line(P(0.4, RY), P(1.25, RY), color=GOLD, stroke_width=6))
        cl = [ves_m(P(3.9, RY + 0.5)), ves_m(P(4.1, RY - 0.05)), ves_m(P(3.9, RY - 0.6))]
        for i, c in enumerate(cl):
            bob(c, 0.05, 2.0 + 0.3 * i)
            self.add(c)
        self.at("At the last stop")
        self.play(*light(st, (4, 5)), run_time=0.4)
        self.at("a vesicle meets")
        tgt = cl[1]
        self.play(tgt.animate.move_to(P(4.87, RY)), run_time=1.6)
        self.at("The two membranes fuse")
        fl = T("vesicle fuses\nwith membrane", 28, GOLD).move_to(P(2.8, -1.5))
        self.play(FadeIn(fl), run_time=0.5)
        bulge = ArcBetweenPoints(P(5.13, 0.2), P(5.13, -0.4), angle=-PI * 0.9, color=GOLD, stroke_width=5)
        bulge.set_fill(GOLD, 0.13)
        self.play(FadeOut(tgt, scale=0.5), FadeIn(bulge), run_time=1.2)
        self.at("opens to the outside")
        gap = Line(P(5.13, 0.18), P(5.13, -0.38), color=BG, stroke_width=9)
        spill = glow_m(P(5.5, RY), 0.15)
        self.play(FadeIn(gap), FadeOut(bulge), FadeIn(spill, scale=0.5), run_time=0.9)
        self.play(spill.animate.move_to(P(6.0, RY)).scale(2.4), run_time=0.5)
        self.at("insulin is released")
        ins = T("insulin", 28, GOLD).move_to(P(6.0, RY - 0.95))
        self.play(FadeIn(ins), Indicate(spill, color=GOLD, scale_factor=1.25), run_time=1.2)
        breathe(spill, 0.08, 2.0)
        self.finish()


# ================================================================ S11
def full_route(scene, op=1.0):
    scene.add(coil_m(), gene_m(), lock_m(gene_pt() + UP * 0.1, 1.3), route_purple(), er_m(), dots_m(), golgi_m(), route_gold(),
              ves_m(V1), ves_m(V2))


class S11Atp(SpokenScene):
    def construct(self):
        world(self)
        st = strip_m(())
        self.add(st)
        grp = VGroup(coil_m(), gene_m(), route_purple(), dots_m(), golgi_m(), route_gold(), ves_m(V1), ves_m(V2))
        er = er_live(self)
        gl0 = glow_m(P(6.0, RY), 0.38)
        breathe(gl0, 0.1, 2.0)
        self.add(grp, gl0)
        self.at("Building a protein chain")
        self.play(Indicate(grp[3], color=TEAL, scale_factor=1.4), run_time=1.4)
        self.at("moving vesicles")
        self.play(Indicate(grp[6], color=GOLD, scale_factor=1.4), Indicate(grp[7], color=GOLD, scale_factor=1.4), run_time=1.4)
        self.at("comes as a TP")
        sp = VGroup(*[spark_m(p) for p in (P(-3.3, -1.6), P(-3.2, -1.9), P(2.2, -1.6), P(2.5, -1.85))])
        al = T("ATP", 30, YELLOW, weight=BOLD).move_to(P(-2.8, -1.2))
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in sp], lag_ratio=0.2), FadeIn(al), run_time=0.8)
        self.play(*[Rotate(s, angle=PI / 2) for s in sp], run_time=0.6)
        self.at("small molecule")
        self.play(Indicate(sp, color=YELLOW, scale_factor=1.5), run_time=1.5)
        self.at("Mitochondria release")
        ms = VGroup(*[mito_m(p) for p in MITO_POS])
        ml = mito_label()
        self.play(FadeIn(ms, shift=UP * 0.3), FadeIn(ml), run_time=1.2)
        self.at("from sugar")
        cube = VGroup(Square(0.3, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25),
                      T("sugar", 24, TEXT)).arrange(RIGHT, buff=0.12).move_to(P(-1.6, -1.75))
        self.play(FadeIn(cube), run_time=0.3)
        self.play(cube.animate.move_to(MITO_POS[0] + LEFT * 0.4).scale(0.6), run_time=0.7)
        self.play(FadeOut(cube), Indicate(ms[0], color=RED, scale_factor=1.2), run_time=0.4)
        self.at("store it in")
        pool = pool_m()
        pl = pool_label()
        streams = []
        for k, mp in enumerate(MITO_POS):
            for j in range(3):
                s = spark_m(mp + UP * 0.45)
                streams.append((s, [P(-3.3, -1.55), P(-3.0, -1.85), P(-2.8, -1.6), P(2.0, -1.6), P(2.4, -1.85), P(2.7, -1.6)][k * 3 + j]))
        self.add(*[s for s, _ in streams])
        self.play(FadeIn(pool), FadeIn(pl),
                  *[s.animate.move_to(t) for s, t in streams], run_time=2.0)
        shimmer_fill(pool)
        self.finish()


# ================================================================ S12
def energy(scene):
    ms = VGroup(*[mito_m(p) for p in MITO_POS])
    pool = pool_m()
    scene.add(ms, pool, pool_label(), mito_label())
    shimmer_fill(pool)
    return pool


class S12Whole(SpokenScene):
    def construct(self):
        world(self)
        st = strip_m(())
        self.add(st)
        self.add(glow_m(P(6.0, RY), 0.38))
        energy(self)
        parts = VGroup(coil_m(), gene_m(), er_m(), dots_m(), golgi_m(), ves_m(V1), ves_m(V2))
        self.add(parts)
        self.at("look at the whole")
        rp, rg = route_purple(), route_gold()
        self.play(Create(rp), run_time=0.6)
        self.play(Create(rg), run_time=1.0)
        self.at("The nucleus sends")
        self.play(*light(st, (0,)), Indicate(self.mobjects[1], color=NUCB, scale_factor=1.06), run_time=1.0)
        self.at("Then the protein moves")
        parcel = glow_m(P(-0.8, 0.225), 0.12)
        self.play(FadeIn(parcel), run_time=0.4)
        self.play(parcel.animate.move_to(P(0.4, RY)), run_time=0.8, rate_func=linear)
        self.at("Rough ER")
        self.play(*light(st, (1,)), Indicate(parts[2], color=TEAL, scale_factor=1.06), run_time=0.6)
        self.play(*light(st, (2,)), parcel.animate.move_to(V1), run_time=0.7)
        self.at("Golgi,")
        self.play(*light(st, (3,)), parcel.animate.move_to(GO_C), Indicate(parts[4], color=ORANGE, scale_factor=1.1), run_time=0.7)
        self.play(*light(st, (4,)), parcel.animate.move_to(V2), run_time=0.6)
        self.at("cell membrane")
        self.play(*light(st, (5,)), parcel.animate.move_to(MEM), run_time=0.9)
        self.finish()


# ================================================================ S13
class S13Order(SpokenScene):
    def construct(self):
        world(self)
        st = strip_m(())
        self.add(st, glow_m(P(6.0, RY), 0.38))
        parts = VGroup(coil_m(), gene_m(), er_m(), dots_m(), golgi_m(), ves_m(V1), ves_m(V2))
        self.add(parts, route_purple(), route_gold())
        self.at("Notice what a route")
        self.play(Indicate(parts[2], color=TEAL, scale_factor=1.05), run_time=1.5)
        self.at("Each part can only")
        cap = T("each part works only on what\nthe part before hands over", 28, TEXT, line_spacing=0.8).move_to(P(-0.4, -2.2))
        self.play(FadeIn(cap), run_time=0.7)
        hops = [(P(-3.1, RY), P(-2.0, RY), PURPLE), (P(0.4, RY), P(0.73, RY), GOLD), (P(1.27, RY), P(1.6, RY), GOLD),
                (P(3.45, RY), P(3.93, RY), GOLD), (P(4.47, RY), P(5.1, RY), GOLD)]
        arrows = VGroup(*[Arrow(a + UP * 0.45, b + UP * 0.45, buff=0, color=c, stroke_width=8, max_tip_length_to_length_ratio=0.5)
                          for a, b, c in hops])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.9), run_time=3.4)
        self.at("So every step depends")
        self.play(LaggedStart(*[Indicate(p, scale_factor=1.12) for p in (parts[2], parts[4], parts[5], parts[6])], lag_ratio=0.5),
                  run_time=2.4)
        self.finish()


# ================================================================ S14
class S14Answer(SpokenScene):
    def construct(self):
        cm, nm = cell_m(), nuc_m()
        self.add(cm, nm, nuc_label())
        motes(self)
        st = strip_m(())
        lk = lock_m(NUC_C + UP * 0.1, 1.6)
        glow = glow_m(P(6.0, RY), 0.38)
        breathe(glow, 0.1, 2.0)
        ins = T("insulin", 28, GOLD).move_to(P(6.0, RY - 0.85))
        gl = T("gene stays here", 28, TEXT).move_to(P(-4.2, 2.5))
        q = T("?", 110, GOLD, font=TITLE_FONT).move_to(P(0.2, RY))
        bob(q, 0.12, 1.8)
        self.add(st, lk, glow, ins, gl, q)
        self.at("how does insulin get out")
        self.play(Indicate(glow, scale_factor=1.3), run_time=1.2)
        self.at("No single part")
        self.play(FadeOut(q, scale=0.5), run_time=0.8)
        self.at("A copy of the gene")
        strand = mrna_m(P(-3.2, RY), 0.7)
        self.play(FadeIn(strand), Create(route_purple()), run_time=0.8)
        self.play(strand.animate.move_to(P(-2.1, RY)), FadeIn(VGroup(er_m(), dots_m())), *light(st, (0, 1)), run_time=1.6)
        self.at("and the protein is handed")
        parcel = glow_m(P(-0.8, 0.225), 0.12)
        self.play(FadeOut(strand), FadeIn(parcel), run_time=0.4)
        self.play(Create(route_gold()), parcel.animate.move_to(P(0.4, RY)), run_time=0.7)
        gg = golgi_m()
        v1, v2 = ves_m(V1, False), ves_m(V2, False)
        self.play(FadeIn(v1), FadeIn(gg), parcel.animate.move_to(V1), *light(st, (1, 2, 3)), run_time=0.7)
        self.play(parcel.animate.move_to(GO_C), run_time=0.5)
        self.play(FadeIn(v2), parcel.animate.move_to(V2), *light(st, (1, 2, 3, 4)), run_time=0.6)
        self.play(parcel.animate.move_to(MEM), *light(st, (0, 1, 2, 3, 4, 5)), run_time=0.6)
        self.at("Mitochondria supply")
        ms = VGroup(*[mito_m(p) for p in MITO_POS])
        pool = pool_m()
        self.play(FadeOut(parcel), FadeIn(ms, shift=UP * 0.3), FadeIn(mito_label()), FadeIn(pool), FadeIn(pool_label()), run_time=1.4)
        shimmer_fill(pool)
        self.finish()


# ================================================================ S15
class S15End(EndCard):
    LINE = "Each part can only work on what the part before hands over."
