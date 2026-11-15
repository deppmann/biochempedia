"""Access, Then Assembly — eukaryotic gene regulation.

COLOR MAP
  BLUE    DNA
  GOLD    nucleosomes / chromatin packing
  TEXT    promoter and transcription machinery
  TEAL    enhancer DNA
  GREEN   regulators, coactivators, and remodellers
  MAGENTA DNA-methylation tags (reserved; not used by this script)
  GREY    RNA and secondary annotation
"""
from bp_parts import *  # noqa: F401,F403
import os
import random

MAGENTA = "#D66BA0"
RNA = "#B8C0CC"
DNA_Y = 0.15
PROM_X = 3.65
ENH_X = -4.25


class AmbientMixin:
    """A restrained, deterministic field of drifting light behind the carried gene world."""
    def setup(self):
        super().setup()
        rng = random.Random(os.environ.get("KX_SCENE_ID", "gene regulation"))
        motes = VGroup()
        for _ in range(88):
            d = Dot(radius=rng.uniform(0.070, 0.105),
                    color=rng.choice([BLUE, TEAL, GOLD]))
            d.set_opacity(rng.uniform(0.40, 0.60))
            d.move_to([rng.uniform(-6.6, 6.6), rng.uniform(-3.55, 3.55), 0])
            d.velocity = np.array([rng.uniform(0.18, 0.36), rng.uniform(-0.07, 0.07), 0])

            def drift(m, dt):
                m.shift(m.velocity * dt)
                if m.get_x() > 6.75:
                    m.shift(LEFT * 13.5)
                if m.get_y() > 3.65:
                    m.shift(DOWN * 7.3)
                elif m.get_y() < -3.65:
                    m.shift(UP * 7.3)
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-20)
        self.add(motes)


class FilmSpoken(AmbientMixin, SpokenScene):
    pass


class FilmPause(AmbientMixin, PredictPause):
    pass


def opaque_block(text, color, width=None, size=28, fill=0.22):
    """A chip with an opaque ground, safe to place over the DNA ribbon."""
    lab = T(text, size, color)
    w = max(width or 0, lab.width + 1.40)
    box = RoundedRectangle(corner_radius=0.14, width=w, height=0.82,
                           stroke_color=color, stroke_width=3,
                           fill_color=BG, fill_opacity=1)
    tint = RoundedRectangle(corner_radius=0.14, width=w, height=0.82,
                            stroke_width=0, fill_color=color, fill_opacity=fill)
    g = VGroup(box, tint, lab.move_to(box))
    g.box = box
    return g


def promoter(x=PROM_X, y=DNA_Y):
    r = RoundedRectangle(corner_radius=0.08, width=1.35, height=0.48,
                         stroke_color=TEXT, stroke_width=4,
                         fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    r.set_fill(TEXT, opacity=0.18)
    return r


def enhancer(x=ENH_X, y=DNA_Y):
    r = RoundedRectangle(corner_radius=0.08, width=2.2, height=0.50,
                         stroke_color=TEAL, stroke_width=4,
                         fill_color=BG, fill_opacity=1).move_to([x, y, 0])
    r.set_fill(TEAL, opacity=0.24)
    return r


def nucleosome(x, y=DNA_Y, labelled=False):
    return opaque_block("nucleosome" if labelled else "", GOLD,
                        width=2.15 if labelled else 1.05,
                        size=26, fill=0.30).move_to([x, y + 1.15, 0])


def machinery(x=PROM_X, y=1.25, text="RNA polymerase II"):
    return opaque_block(text, TEXT, width=2.65, size=26, fill=0.12).move_to([x, y, 0])


def factor(kind="round", x=ENH_X, y=1.10):
    if kind == "round":
        shape = Circle(radius=0.37, stroke_color=GREEN, stroke_width=4,
                       fill_color=GREEN, fill_opacity=0.32)
    else:
        shape = RegularPolygon(3, radius=0.50, stroke_color=GREEN, stroke_width=4,
                               fill_color=GREEN, fill_opacity=0.32).rotate(PI)
    return shape.move_to([x, y, 0])


def rna_stream(x0=4.45, count=6, spread=2.0, y0=0.15):
    """Pale RNA strokes moving steadily rightward; schematic, not molecular."""
    strokes = VGroup()
    for i in range(count):
        y = y0 + (i - (count - 1) / 2) * 0.27
        s = Line([x0 + (i % 3) * 0.42, y, 0],
                 [x0 + 0.46 + (i % 3) * 0.42, y, 0],
                 color=RNA, stroke_width=6)
        s.phase = i * 0.31
        s.base_x = s.get_x()

        def drift(m, dt, lo=x0, width=spread):
            m.phase += dt * 0.55
            m.set_x(lo + (m.phase % width))
        s.add_updater(drift)
        strokes.add(s)
    return strokes


def gene_world(*, covered=False, factors=True, mediator=False, rna=0,
               labels=False, nucleosomes=True, arc=False):
    """The carried gene: every continuing scene calls this exact builder."""
    if arc:
        dna = CubicBezier(np.array([-6.0, DNA_Y, 0]), np.array([-2.5, 2.35, 0]),
                          np.array([1.4, 2.35, 0]), np.array([5.9, DNA_Y, 0]),
                          color=BLUE, stroke_width=8)
    else:
        dna = Line([-6.0, DNA_Y, 0], [5.9, DNA_Y, 0], color=BLUE, stroke_width=8)
    enh, prom = enhancer(), promoter()
    if covered:
        prom.set_opacity(0)
    g = VGroup(dna, enh, prom)
    g.dna, g.enh, g.prom = dna, enh, prom
    g.nucs = VGroup()
    if nucleosomes:
        for x in (-1.85, 0.35):
            g.nucs.add(nucleosome(x))
        if covered:
            g.nucs.add(nucleosome(PROM_X, labelled=True))
        g.add(g.nucs)
    g.factors = VGroup()
    if factors:
        g.factors.add(factor("round", ENH_X - 0.48), factor("triangle", ENH_X + 0.48))
        g.add(g.factors)
    if mediator:
        med = opaque_block("Mediator", GREEN, width=1.85, size=26).move_to([0.7, 2.15, 0])
        pol = machinery(y=1.35)
        bridge = VGroup(
            Line(g.factors.get_top(), med.get_left() + LEFT * 0.08, color=GREEN, stroke_width=4),
            Line(med.get_right() + RIGHT * 0.08, pol.get_left(), color=GREEN, stroke_width=4),
        )
        g.add(bridge, med, pol)
        g.med, g.pol = med, pol
    if labels:
        el = T("enhancer", 28, TEAL).move_to([ENH_X, -0.65, 0])
        pl = T("promoter", 28, TEXT).move_to([PROM_X, -0.65, 0])
        g.add(el, pl)
    if rna:
        g.rna = rna_stream(count=rna)
        g.add(g.rna)
    return g


def small_gene(cx, cy, active=True, missing=False, repressor=False):
    dna = Line([cx - 2.2, cy, 0], [cx + 2.15, cy, 0], color=BLUE, stroke_width=7)
    enh = RoundedRectangle(corner_radius=0.06, width=1.1, height=0.40,
                           stroke_color=TEAL, stroke_width=3,
                           fill_color=TEAL, fill_opacity=0.25).move_to([cx - 1.35, cy, 0])
    prom = RoundedRectangle(corner_radius=0.06, width=0.7, height=0.40,
                            stroke_color=TEXT, stroke_width=3,
                            fill_color=TEXT, fill_opacity=0.18).move_to([cx + 1.25, cy, 0])
    f1, f2 = factor("round", cx - 1.62, cy + 0.75), factor("triangle", cx - 1.08, cy + 0.75)
    f1.scale(0.8), f2.scale(0.8)
    g = VGroup(dna, enh, prom, f1)
    if missing:
        q = T("?", 38, GREEN).move_to([cx - 1.08, cy + 0.75, 0])
        g.add(q)
    else:
        g.add(f2)
    if repressor:
        rep = opaque_block("repressor?", GREEN, width=1.75, size=24, fill=0.02)
        rep.move_to([cx + 0.05, cy + 1.25, 0])
        g.add(rep)
    if active:
        g.add(rna_stream(cx + 1.75, count=4, spread=0.9, y0=cy))
    return g


def split_cells(*, kidney_missing=False, kidney_repressor=False):
    tp = TwoPanel("liver cell", "kidney cell", colors=(TEAL, GOLD), top=3.0, bottom=-2.45)
    left = small_gene(-3.3, 0.15, active=True)
    right = small_gene(3.3, 0.15, active=False, missing=kidney_missing, repressor=kidney_repressor)
    nuclei = VGroup(
        Ellipse(width=5.3, height=3.5, stroke_color=TEAL, stroke_width=3,
                fill_color=TEAL, fill_opacity=0.04).move_to([-3.3, 0.2, 0]),
        Ellipse(width=5.3, height=3.5, stroke_color=GOLD, stroke_width=3,
                fill_color=GOLD, fill_opacity=0.04).move_to([3.3, 0.2, 0]),
    )
    return VGroup(tp, nuclei, left, right)


def predict_backdrop():
    w = gene_world(covered=True, factors=True, nucleosomes=True, arc=True)
    w.shift(UP * 0.62)
    a = boxed_label("regulators present", GREEN, size=28).move_to([-2.15, -1.65, 0])
    b = boxed_label("promoter covered", GOLD, size=28).move_to([2.15, -1.65, 0])
    pulse(a.box, base=3.0, amp=1.3, speed=2.0)
    pulse(b.box, base=3.0, amp=1.3, speed=2.0)
    return VGroup(w, a, b)


class S00Hook(FilmSpoken):
    def construct(self):
        world = split_cells()
        self.play(FadeIn(world[0]), FadeIn(world[1]), run_time=0.8)
        self.at("Watch one gene")
        self.play(FadeIn(world[2]), FadeIn(world[3]), run_time=1.2)
        same = T("same DNA sequence", 32, BLUE).move_to([0, 3.42, 0])
        self.at("sequence matches")
        self.play(FadeIn(same, shift=DOWN * 0.12), run_time=0.6)
        many = T("many RNA", 30, RNA).move_to([-3.3, -2.05, 0])
        few = T("almost none", 30, RNA).move_to([3.3, -2.05, 0])
        self.at("many messenger")
        self.play(FadeIn(many), run_time=0.5)
        self.at("other makes almost none")
        self.play(FadeIn(few), run_time=0.5)
        rule = caption("Selective use — not missing genes", color=TEXT)
        self.at("puzzle is not")
        self.play(FadeOut(VGroup(many, few)), FadeIn(rule), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = split_cells()
        world.set_opacity(0.38)
        title = T("Access, Then Assembly", 54, TEXT, font=TITLE_FONT)
        back = RoundedRectangle(corner_radius=0.20, width=title.width + 0.8,
                                height=title.height + 0.55, stroke_color=GOLD,
                                stroke_width=3, fill_color=BG, fill_opacity=0.94)
        self.add(world)
        self.play(FadeOut(world), FadeIn(VGroup(back, title)), run_time=0.55)
        self.wait(0.7)
        self.play(FadeOut(VGroup(back, title)), run_time=0.55)
        self.finish()


class S02Packed(FilmSpoken):
    def construct(self):
        dna = Line([-6.0, DNA_Y, 0], [5.9, DNA_Y, 0], color=BLUE, stroke_width=8)
        self.play(Create(dna), run_time=0.8)
        self.at("packed into chromatin")
        nucs = VGroup(nucleosome(-4.25, labelled=True), nucleosome(-0.35, labelled=True),
                      nucleosome(3.55, labelled=True))
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.25) for n in nucs], lag_ratio=0.18), run_time=1.5)
        prom = promoter(y=-0.58)
        self.add(prom)
        self.bring_to_front(nucs[-1])
        toggle = boxed_label("open / shut?", GREY, size=30).move_to([0, 2.55, 0])
        self.at("Packing does not")
        self.play(FadeIn(toggle), run_time=0.5)
        cond = boxed_label("conditional", GOLD, size=34).move_to(toggle)
        self.at("access conditional")
        self.play(swap(toggle, cond), run_time=0.7)
        pol = machinery(x=4.35, y=2.70, text="machinery")
        self.at("Proteins must reach")
        self.play(FadeIn(pol), run_time=0.5)
        self.play(pol.animate.shift(LEFT * 0.65), rate_func=there_and_back, run_time=1.2)
        hard = caption("Harder to read — not impossible", color=GOLD)
        self.at("harder not impossible")
        self.play(FadeOut(cond), FadeIn(hard), run_time=0.7)
        self.finish()


class S03Remodel(FilmSpoken):
    def construct(self):
        world = gene_world(covered=True, factors=False, labels=True)
        pol = machinery(x=4.65, y=2.55)
        self.add(world, pol)
        rem = opaque_block("remodeller", GREEN, width=2.0).move_to([0.5, 3.05, 0])
        self.play(FadeIn(rem), run_time=0.6)
        covered = world.nucs[-1]
        self.at("gold block slides aside")
        self.play(covered.animate.move_to([1.60, -1.50, 0]), run_time=1.3)
        self.at("promoter becomes reachable")
        self.play(world.prom.animate.set_opacity(1), pol.animate.move_to([PROM_X, 1.35, 0]), run_time=1.0)
        pioneer = opaque_block("pioneer factor", GREEN, width=2.2, size=25)
        pioneer.move_to([-1.85, 2.20, 0])
        self.at("pioneer factors")
        self.play(FadeIn(pioneer, shift=DOWN * 0.2), run_time=0.7)
        access = boxed_label("access", TEXT, size=28).move_to([-1.5, 2.65, 0])
        binding = boxed_label("binding", GREEN, size=28).move_to([1.5, 2.65, 0])
        arrows = VGroup(
            CurvedArrow(access.get_right(), binding.get_left(), angle=-0.5, color=GREEN),
            CurvedArrow(binding.get_left() + DOWN * 0.25, access.get_right() + DOWN * 0.25,
                        angle=-0.5, color=TEXT),
        )
        self.at("influence each other")
        self.play(FadeOut(rem), FadeOut(pioneer), FadeIn(access), FadeIn(binding), Create(arrows), run_time=1.0)
        self.at("promoter stays fixed")
        self.play(Indicate(world.prom, color=TEXT),
                  world.nucs[0].animate.shift(RIGHT * 0.35),
                  world.nucs[1].animate.shift(LEFT * 0.35), run_time=1.1)
        self.finish()


class S04Enhancer(FilmSpoken):
    def construct(self):
        world = gene_world(covered=False, factors=False, nucleosomes=False, labels=True, arc=True)
        self.add(world)
        access = caption("Access is one requirement", color=TEXT)
        self.play(FadeIn(access), run_time=0.5)
        self.at("teal enhancer")
        self.play(Indicate(world.enh, color=TEAL, scale_factor=1.08), run_time=0.8)
        factors = VGroup(factor("round", ENH_X - 0.48), factor("triangle", ENH_X + 0.48))
        self.at("transcription factors bind")
        self.play(FadeIn(factors, shift=DOWN * 0.25), run_time=0.8)
        co = opaque_block("coactivator", GREEN, width=1.9, size=25).move_to([-3.0, 2.55, 0])
        self.at("and recruit")
        self.play(FadeIn(co, shift=RIGHT * 0.25), run_time=0.7)
        med = opaque_block("Mediator", GREEN, width=1.8, size=26).move_to([0.0, 2.25, 0])
        pol = machinery(x=4.25, y=2.85)
        links = VGroup(Arrow(co.get_center(), med.get_center(), buff=1.25, color=GREEN, stroke_width=4),
                       Arrow(med.get_center(), pol.get_center(), buff=1.55, color=GREEN, stroke_width=4))
        self.at("Mediator helps connect")
        self.play(FadeIn(med), Create(links[0]), run_time=0.7)
        self.play(FadeIn(pol), Create(links[1]), run_time=0.7)
        caveat = caption("usual picture; directness debated", size=28, color=GREY)
        self.at("at the promoter")
        self.play(swap(access, caveat), run_time=0.7)
        dna_lab = boxed_label("enhancer = DNA", TEAL, size=30).move_to([-4.2, -1.35, 0])
        self.at("enhancer itself")
        self.play(FadeIn(dna_lab), run_time=0.7)
        self.finish()


class S05Predict(FilmSpoken):
    def construct(self):
        back = predict_backdrop()
        self.play(FadeIn(back[0]), run_time=0.8)
        self.at("factors are present")
        self.play(FadeIn(back[1]), run_time=0.5)
        self.at("nucleosome still covers")
        self.play(FadeIn(back[2]), run_time=0.5)
        q = question_card("Strong transcription guaranteed?", y=-3.05, size=34)
        self.at("strong transcription guaranteed")
        self.play(FadeIn(q), run_time=0.7)
        self.at("both requirements")
        self.play(Indicate(back[1], color=GREEN), Indicate(back[2], color=GOLD), run_time=1.0)
        self.finish()


class S06Pause(FilmPause):
    QUESTION = "Strong transcription guaranteed?"
    SECONDS = 4.5
    CARD = {"y": -3.05, "size": 34}

    def backdrop(self):
        return predict_backdrop()


class S07Reveal(FilmSpoken):
    def construct(self):
        world = gene_world(covered=True, factors=True, nucleosomes=True, arc=True)
        world.shift(UP * 0.25)
        self.add(world)
        ans = boxed_label("not yet", GOLD, size=38).move_to([0, -2.45, 0])
        self.play(FadeIn(ans), run_time=0.6)
        scope = scope_tag("simplified case · schematic")
        self.add(scope)
        info = boxed_label("regulatory information", GREEN, size=28).move_to([-2.7, -1.35, 0])
        self.at("supply regulatory information")
        self.play(FadeIn(info), run_time=0.6)
        rem = opaque_block("remodeller", GREEN, width=1.9, size=25).move_to([-1.3, 2.75, 0])
        recruit = Arrow(info.get_top(), rem.get_left(), buff=0.12, color=GREEN, stroke_width=4)
        self.at("recruit a remodeler")
        self.play(GrowArrow(recruit), FadeIn(rem), run_time=0.8)
        covered = world.nucs[-1]
        self.at("shifts the nucleosome")
        self.play(rem.animate.move_to([0.9, 2.75, 0]), covered.animate.move_to([2.05, -1.10, 0]), run_time=1.4)
        world.prom.set_opacity(1)
        med = opaque_block("Mediator", GREEN, width=1.7, size=24).move_to([0.0, 2.55, 0])
        pol = machinery(x=4.25, y=2.75)
        stream = rna_stream(count=5)
        self.at("assembled regulators")
        self.play(FadeOut(ans), FadeOut(rem), FadeIn(med), FadeIn(pol), run_time=0.8)
        self.at("raise transcription")
        self.play(FadeIn(stream), run_time=0.8)
        self.finish()


def docking_world():
    dna = Line([-5.8, -0.15, 0], [5.7, -0.15, 0], color=BLUE, stroke_width=8)
    sites = VGroup(
        Circle(radius=0.48, color=TEAL, stroke_width=4).move_to([-3.9, -0.15, 0]),
        RegularPolygon(3, radius=0.60, color=TEAL, stroke_width=4).rotate(PI).move_to([-2.45, -0.15, 0]),
        Square(side_length=0.88, color=TEAL, stroke_width=4).move_to([-0.9, -0.15, 0]),
    )
    prom = promoter(3.6, -0.15)
    return VGroup(dna, sites, prom), sites


class S08Combinations(FilmSpoken):
    def construct(self):
        base, sites = docking_world()
        self.play(FadeIn(base), run_time=0.8)
        committee = T("a regulatory committee", 36, TEAL).move_to([0, 2.85, 0])
        self.at("Picture a committee")
        self.play(FadeIn(committee), run_time=0.6)
        one = factor("round", -3.9, 0.95)
        trickle = rna_stream(4.3, count=2, spread=0.8, y0=-0.15)
        self.at("One factor alone")
        self.play(FadeIn(one, shift=DOWN * 0.25), FadeIn(trickle), run_time=0.8)
        one2 = factor("triangle", -2.45, 0.95)
        trickle2 = rna_stream(4.3, count=2, spread=0.8, y0=-0.15)
        self.at("may do little")
        self.play(FadeOut(one), FadeOut(trickle), FadeIn(one2, shift=DOWN * 0.25), FadeIn(trickle2), run_time=0.8)
        pair = VGroup(factor("round", -3.9, 0.95), factor("triangle", -2.45, 0.95))
        stream = rna_stream(4.15, count=7, spread=1.4, y0=-0.15)
        self.at("Two together")
        self.play(FadeOut(one2), FadeOut(trickle2), FadeIn(pair), run_time=0.8)
        self.at("machinery effectively")
        self.play(FadeIn(stream), run_time=0.8)
        cells = VGroup(boxed_label("cell 1", GREEN), boxed_label("cell 2", GREEN),
                       boxed_label("cell 3", GREEN)).arrange(RIGHT, buff=0.6).move_to([0, -2.2, 0])
        self.at("Different cells")
        self.play(FadeIn(cells), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S09CellTypes(FilmSpoken):
    def construct(self):
        world = split_cells()
        self.play(FadeIn(world), run_time=0.9)
        same = T("same DNA", 34, BLUE).move_to([0, 3.42, 0])
        self.at("DNA still matches")
        self.play(FadeIn(same), run_time=0.6)
        coincide = boxed_label("factors + access", GREEN, size=26).move_to([-3.3, -2.85, 0])
        self.at("factors and accessible")
        self.play(FadeIn(coincide), run_time=0.7)
        missing_world = split_cells(kidney_missing=True)
        self.at("may be missing")
        self.play(ReplacementTransform(world, missing_world), run_time=0.9)
        miss = T("may be missing", 28, GREEN).move_to([3.3, -2.85, 0])
        self.play(FadeIn(miss), run_time=0.5)
        rep = opaque_block("repressor?", GREEN, width=1.8, size=25, fill=0.02).move_to([4.75, 1.25, 0])
        also = T("also fits", 28, GREY).next_to(rep, UP, buff=0.20).shift(RIGHT * 0.30)
        self.at("repressor could also")
        self.play(FadeIn(rep), FadeIn(also), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


def reporter_construct():
    dna = Line([-5.6, 0, 0], [4.8, 0, 0], color=BLUE, stroke_width=7)
    pieces = VGroup(*[
        RoundedRectangle(corner_radius=0.06, width=1.15, height=0.68,
                         stroke_color=TEAL, stroke_width=4,
                         fill_color=TEAL, fill_opacity=0.25).move_to([-4.5 + 1.35 * i, 0, 0])
        for i in range(3)
    ])
    prom = promoter(0.55, 0)
    bulb = Circle(radius=0.58, color=RNA, stroke_width=4,
                  fill_color=RNA, fill_opacity=0.12).move_to([3.5, 0.25, 0])
    lamp = VGroup(bulb, T("reporter", 28, RNA).move_to([3.5, -0.75, 0]))
    return VGroup(dna, pieces, prom, lamp), pieces, lamp


class S10ReporterScope(FilmSpoken):
    def construct(self):
        construct, pieces, lamp = reporter_construct()
        self.play(FadeIn(construct), run_time=0.9)
        label = boxed_label("reporter assay", RNA, size=32).move_to([0, 2.65, 0])
        self.at("beside a promoter")
        self.play(FadeIn(label), run_time=0.5)
        necessity = boxed_label("necessity", TEAL, size=30).move_to(label)
        self.at("necessity")
        self.play(swap(label, necessity), pieces[0].animate.shift(UP * 1.25),
                  lamp[0].animate.set_fill(RNA, opacity=0.04), run_time=0.9)
        suff = boxed_label("sufficiency", TEAL, size=30).move_to(label)
        self.at("sufficiency")
        self.play(swap(necessity, suff), pieces[0].animate.move_to([-1.5, 0, 0]),
                  FadeOut(pieces[1]), FadeOut(pieces[2]),
                  lamp[0].animate.set_fill(RNA, opacity=0.25), run_time=0.9)
        coop = boxed_label("cooperation", TEAL, size=30).move_to(label)
        self.at("Combining pieces")
        self.play(swap(suff, coop), FadeIn(pieces[1]), pieces[1].animate.move_to([-0.2, 0, 0]),
                  lamp[0].animate.set_fill(RNA, opacity=0.65), run_time=0.9)
        orient = boxed_label("orientation", TEAL, size=30).move_to(label)
        arrow = Arrow([-2.0, -1.1, 0], [-0.8, -1.1, 0], color=TEAL, stroke_width=4)
        self.at("reversing one")
        self.play(swap(coop, orient), Rotate(pieces[0], PI), GrowArrow(arrow), run_time=0.9)
        native = boxed_label("outside native setting", GOLD, size=30).move_to([0, -2.35, 0])
        chromosome = Ellipse(width=10.5, height=3.8, stroke_color=GREY,
                             stroke_width=3, fill_color=GREY, fill_opacity=0.03)
        self.at("native setting")
        self.play(FadeOut(arrow), FadeOut(orient), FadeIn(chromosome), FadeIn(native),
                  construct.animate.shift(DOWN * 0.2), run_time=1.0)
        delete = boxed_label("delete here", GOLD, size=30).move_to([2.4, 2.65, 0])
        mark = Arrow(delete.get_bottom(), [1.65, 0.45, 0], buff=0.10, color=GOLD, stroke_width=4)
        self.at("genomic deletion")
        self.play(FadeIn(delete), GrowArrow(mark), run_time=0.8)
        self.finish()


class S11Rule(FilmSpoken):
    def construct(self):
        world = gene_world(covered=True, factors=True, nucleosomes=True, arc=True)
        self.play(FadeIn(world), run_time=0.8)
        self.at("Chromatin changes reachability")
        access = boxed_label("access", GOLD, size=32).move_to([-2.2, -2.15, 0])
        self.play(FadeIn(access), world.nucs[-1].animate.move_to([4.75, -1.10, 0]), run_time=1.0)
        world.prom.set_opacity(1)
        assembly = boxed_label("assembly", GREEN, size=32).move_to([2.2, -2.15, 0])
        rem = opaque_block("remodeller", GREEN, width=1.9, size=24).move_to([-0.6, 2.55, 0])
        self.at("regulators change recruitment")
        self.play(FadeIn(assembly), FadeIn(rem), run_time=0.8)
        target = np.array([0, -0.85, 0])
        arrows = VGroup(Arrow(access.get_top(), target + LEFT * 0.2, buff=0.12, color=GOLD),
                        Arrow(assembly.get_top(), target + RIGHT * 0.2, buff=0.12, color=GREEN))
        stream = rna_stream(4.25, count=6, spread=1.5, y0=0.15)
        self.at("Neither layer")
        self.play(Create(arrows), run_time=0.8)
        self.at("Together they make")
        self.play(FadeIn(stream), run_time=0.8)
        rule = caption("Gene use is conditional on cell state", color=TEXT)
        self.at("conditional on cell state")
        self.play(FadeIn(rule), run_time=0.7)
        self.finish()


class S12End(EndCard):
    LINE = "Gene output depends on accessible DNA and the regulators present."
