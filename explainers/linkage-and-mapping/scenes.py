"""When Four Classes Refuse to Be Equal.

COLOR MAP
  BLUE   = the A--B homologue and segments inherited from it
  YELLOW = the a--b homologue and segments inherited from it
  GREEN  = parental classes
  RED    = recombinant classes and crossover sites
  TEAL   = recombination frequency and genetic-map distance
  GREY   = tester material, outlines, and de-emphasised structure
"""
from bp_parts import *


DOM, REC = BLUE, YELLOW
BIN_XS = (-4.8, -1.6, 1.6, 4.8)
BIN_NAMES = ("A  B", "a  b", "A  b", "a  B")
BIN_COLORS = (GREEN, GREEN, RED, RED)


def chromosome(y, color, alleles, left=-5.4, right=5.4, marker_x=(-2.7, 2.7), height=0.52):
    """The carried chromosome picture, rebuilt at identical coordinates in every scene."""
    bar = RoundedRectangle(corner_radius=0.22, width=right-left, height=height,
                           stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.88).move_to([(left+right)/2, y, 0])
    pulse(bar, base=2.5, amp=1.2, speed=2.0)
    marks = VGroup()
    for x, a in zip(marker_x, alleles):
        marks.add(Circle(radius=0.14, color=BG, fill_color=BG, fill_opacity=1).move_to([x, y, 0]))
        marks.add(T(a, 30, TEXT, weight=BOLD).move_to([x, y + 0.48, 0]))
    return VGroup(bar, marks)


def homologues(marker_x=(-2.7, 2.7), ys=(2.35, 1.35)):
    return VGroup(chromosome(ys[0], DOM, ("A", "B"), marker_x=marker_x),
                  chromosome(ys[1], REC, ("a", "b"), marker_x=marker_x))


def allele_tile(name, colors, width=1.6, height=0.62):
    left = Rectangle(width=width/2, height=height, stroke_width=0,
                     fill_color=colors[0], fill_opacity=0.92)
    right = Rectangle(width=width/2, height=height, stroke_width=0,
                      fill_color=colors[1], fill_opacity=0.92).next_to(left, RIGHT, buff=0)
    lab = T(name, 32, BG, weight=BOLD).move_to(VGroup(left, right))
    return VGroup(left, right, lab)


def four_tiles(y=0.45):
    specs = (("A  B", (DOM, DOM)), ("a  b", (REC, REC)),
             ("A  b", (DOM, REC)), ("a  B", (REC, DOM)))
    return VGroup(*[allele_tile(n, c).move_to([x, y, 0]) for x, (n, c) in zip(BIN_XS, specs)])


def bins(heights=(1.5, 1.5, 0.65, 0.65), base=-2.45, max_h=1.55, labels=True):
    """Four schematic offspring bins at fixed positions."""
    g = VGroup()
    for x, name, col, h in zip(BIN_XS, BIN_NAMES, BIN_COLORS, heights):
        outline = Rectangle(width=1.75, height=max_h, stroke_color=col, stroke_width=3,
                            fill_opacity=0).move_to([x, base + max_h/2, 0])
        pulse(outline, base=3, amp=0.9, speed=1.8)
        fill = Rectangle(width=1.58, height=max(0.04, h), stroke_width=0,
                         fill_color=col, fill_opacity=0.72).move_to([x, base + h/2, 0])
        one = VGroup(outline, fill)
        if labels:
            one.add(T(name, 28, col, weight=BOLD).move_to([x, base - 0.38, 0]))
        g.add(one)
    return g


def live_bins(trackers, base=-2.45, max_h=1.55):
    outlines = bins((0, 0, 0, 0), base=base, max_h=max_h)
    for one in outlines:
        one[1].set_opacity(0)
    fills = VGroup(*[
        always_redraw(lambda x=x, tr=tr, col=col: Rectangle(
            width=1.58, height=max(0.04, tr.get_value()), stroke_width=0,
            fill_color=col, fill_opacity=0.72).move_to([x, base + max(0.04, tr.get_value())/2, 0]))
        for x, tr, col in zip(BIN_XS, trackers, BIN_COLORS)
    ])
    return outlines, fills


def four_chromatids(marker_x=(-2.7, 2.7), ys=(2.72, 1.70, 0.85, 0.0)):
    cs = VGroup(chromosome(ys[0], DOM, ("A", "B"), marker_x=marker_x, height=0.38),
                chromosome(ys[1], DOM, ("A", "B"), marker_x=marker_x, height=0.38),
                chromosome(ys[2], REC, ("a", "b"), marker_x=marker_x, height=0.38),
                chromosome(ys[3], REC, ("a", "b"), marker_x=marker_x, height=0.38))
    # Label only the outside chromatids. The middle pair retains the identical marker dots,
    # while the letters stay clear of the tightly spaced bars.
    cs[0][1][1].shift(UP*0.20); cs[0][1][3].shift(UP*0.20)
    cs[1][1][1].set_opacity(0); cs[1][1][3].set_opacity(0)
    cs[2][1][1].set_opacity(0); cs[2][1][3].set_opacity(0)
    cs[3][1][1].shift(DOWN*1.05); cs[3][1][3].shift(DOWN*1.05)
    return cs


def interval_world(question=False):
    """The final frame of the predict scene and the opening frame of its pause/reveal."""
    chroms = four_chromatids(marker_x=(-3.6, 3.6), ys=(2.65, 1.92, 1.19, 0.46))
    bs = bins((0.85, 0.85, 0.42, 0.42), base=-2.25, max_h=1.18)
    q = T("?", 64, GOLD, weight=BOLD).move_to([3.2, -0.55, 0])
    return VGroup(chroms, bs, q) if question else VGroup(chroms, bs)


def fraction_picture():
    num = T("both recombinant classes", 34, RED, weight=BOLD).move_to([0, 0.72, 0])
    rule = Line([-3.4, 0.18, 0], [3.4, 0.18, 0], color=TEXT, stroke_width=4)
    den = T("all offspring", 34, TEXT, weight=BOLD).move_to([0, -0.40, 0])
    rf = M("RF =", 46, TEAL).next_to(rule, LEFT, buff=0.45)
    return VGroup(num, rule, den, rf)


def short_ruler():
    band = RoundedRectangle(corner_radius=0.24, width=9.5, height=0.72, stroke_width=0,
                            fill_color=TEAL, fill_opacity=0.18).move_to([0, 0, 0])
    line = Line([-4.6, 0, 0], [4.6, 0, 0], color=TEAL, stroke_width=10)
    pulse(line, base=10, amp=2, speed=2.2)
    ticks = VGroup(*[Line([x, -0.22, 0], [x, 0.22, 0], color=TEXT, stroke_width=4)
                     for x in np.linspace(-4.6, 4.6, 11)])
    ends = VGroup(T("0", 26, TEXT).move_to([-4.6, -0.5, 0]),
                  T("short interval", 28, TEAL).move_to([4.0, -0.55, 0]))
    title = T("genetic map", 34, TEAL, weight=BOLD).move_to([0, 0.62, 0])
    return VGroup(band, line, ticks, ends, title)


class S01Hook(SpokenScene):
    def construct(self):
        hs = homologues()
        bs = bins((0, 0, 0, 0))
        self.play(FadeIn(hs, shift=DOWN*0.12), FadeIn(bs), run_time=0.8)
        self.at("A blue chromosome")
        self.play(Indicate(hs[0], color=DOM, scale_factor=1.02),
                  Indicate(hs[1], color=REC, scale_factor=1.02), run_time=0.8)
        self.at("Each carries")
        self.play(Indicate(VGroup(hs[0][1], hs[1][1]), color=TEXT, scale_factor=1.08), run_time=0.8)
        tiles = four_tiles(0.35)
        self.at("Their allele combinations")
        self.play(FadeIn(tiles[0], shift=DOWN*0.2), FadeIn(tiles[1], shift=DOWN*0.2), run_time=0.8)
        self.at("yet the offspring")
        grown = bins()
        self.play(FadeIn(tiles[2:]), run_time=0.8)
        self.play(Transform(bs, grown), run_time=1.0)
        for tile, target in zip(tiles, bs):
            self.play(tile.animate.move_to(target[0].get_top()+UP*0.25).scale(0.72), run_time=0.32)
        tag = scope_tag("schematic")
        self.add(tag)
        self.at("The puzzle")
        self.play(Indicate(VGroup(bs[0], bs[1]), color=GREEN, scale_factor=1.04),
                  Indicate(VGroup(bs[2], bs[3]), color=RED, scale_factor=1.04), run_time=1.0)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Linkage and mapping"
    TITLE = "When Four Classes Refuse to Be Equal"


class S03Testcross(SpokenScene):
    def construct(self):
        tiles = four_tiles(2.05)
        head = T("heterozygote gametes", 32, BLUE, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=DOWN*0.15) for t in tiles], lag_ratio=0.12), run_time=1.0)
        self.at("The heterozygote")
        self.play(LaggedStart(*[Indicate(t, color=TEXT, scale_factor=1.06) for t in tiles[:2]], lag_ratio=0.25), run_time=1.0)
        self.at("It can also")
        self.play(LaggedStart(*[Indicate(t, color=TEXT, scale_factor=1.06) for t in tiles[2:]], lag_ratio=0.25), run_time=1.0)
        testers = VGroup(*[allele_tile("a  b", (GREY, GREY), height=0.5).move_to([x, 0.7, 0]) for x in BIN_XS])
        tester_lab = T("tester always gives a  b", 30, GREY).move_to([0, 1.22, 0])
        self.at("The tester always")
        self.play(FadeIn(tester_lab), LaggedStart(*[FadeIn(t, shift=UP*0.15) for t in testers], lag_ratio=0.1), run_time=1.0)
        offspring = bins((0.48, 0.48, 0.48, 0.48), base=-2.15, max_h=0.95)
        self.at("Each offspring")
        self.play(FadeIn(offspring), run_time=0.6)
        self.play(LaggedStart(*[AnimationGroup(tiles[i].animate.move_to([BIN_XS[i], -0.5, 0]).scale(0.78),
                                                testers[i].animate.move_to([BIN_XS[i], -0.95, 0]).scale(0.78))
                                for i in range(4)], lag_ratio=0.15), run_time=1.6)
        readable = caption("offspring class = heterozygote gamete", color=TEAL)
        self.play(FadeIn(readable), run_time=0.7)
        self.finish()


class S03bPattern(SpokenScene):
    def construct(self):
        tr = [ValueTracker(0.25) for _ in range(4)]
        outlines, fills = live_bins(tr, base=-1.85, max_h=2.35)
        exp = T("independent expectation", 32, GREY).move_to([0, 2.85, 0])
        equal = DashedLine([-5.8, 0.15, 0], [5.8, 0.15, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(exp), FadeIn(outlines), Create(equal), run_time=1.0)
        self.add(fills)
        self.at("feed every bin equally")
        self.play(*[v.animate.set_value(1.15) for v in tr], run_time=1.5, rate_func=linear)
        inherited = VGroup(allele_tile("A  B", (DOM, DOM), width=1.1), allele_tile("a  b", (REC, REC), width=1.1))
        inherited.arrange(RIGHT, buff=0.3).move_to([0, 2.15, 0])
        self.at("Instead")
        self.play(swap(exp, T("observed pattern", 32, TEXT).move_to(exp)), FadeIn(inherited), run_time=0.8)
        self.at("fill two bins faster")
        self.play(tr[0].animate.set_value(2.15), tr[1].animate.set_value(2.15),
                  tr[2].animate.set_value(1.35), tr[3].animate.set_value(1.35), run_time=1.8)
        br = BraceBetweenPoints([-5.7, -2.25, 0], [-0.7, -2.25, 0], direction=DOWN, color=GREEN)
        lab = T("linkage pattern", 30, GREEN, weight=BOLD).next_to(br, DOWN, buff=0.12)
        self.at("signature of linkage")
        self.play(GrowFromCenter(br), FadeIn(lab), run_time=0.8)
        shared = caption("linked loci share a chromosome", color=BLUE)
        self.at("Linked means")
        self.play(FadeOut(VGroup(br, lab)), FadeIn(shared), run_time=0.7)
        self.play(Indicate(inherited, color=TEXT, scale_factor=1.06), run_time=0.9)
        self.finish()


class S04Phase(SpokenScene):
    def construct(self):
        hs = homologues()
        self.play(FadeIn(hs), run_time=0.8)
        self.at("Big A with big B")
        self.play(Indicate(hs[0], color=DOM, scale_factor=1.03), run_time=0.8)
        self.at("Little a with little b")
        self.play(Indicate(hs[1], color=REC, scale_factor=1.03), run_time=0.8)
        br = VGroup(Line([-5.35, 0.82, 0], [5.35, 0.82, 0], color=GREEN, stroke_width=4),
                    Line([-5.35, 0.82, 0], [-5.35, 1.02, 0], color=GREEN, stroke_width=4),
                    Line([5.35, 0.82, 0], [5.35, 1.02, 0], color=GREEN, stroke_width=4))
        parental = T("inherited = parental", 30, GREEN, weight=BOLD).move_to([0, 0.42, 0])
        self.at("Those are parental")
        self.play(GrowFromCenter(br), FadeIn(parental), run_time=0.8)
        bs = bins((1.35, 1.35, 0.55, 0.55), base=-2.45, max_h=1.55)
        self.at("even before counting")
        self.play(FadeIn(bs[0]), FadeIn(bs[1]), run_time=0.8)
        mixed = VGroup(allele_tile("A  b", (DOM, REC)), allele_tile("a  B", (REC, DOM)))
        mixed[0].move_to([1.6, -0.12, 0]); mixed[1].move_to([4.8, -0.12, 0])
        self.at("The mixed combinations")
        self.play(FadeIn(mixed), FadeIn(bs[2]), FadeIn(bs[3]), run_time=0.9)
        self.play(mixed[0].animate.move_to([1.6, -1.18, 0]).scale(0.75),
                  mixed[1].animate.move_to([4.8, -1.18, 0]).scale(0.75), run_time=0.9)
        phase = T("phase = the inherited arrangement", 30, TEAL).move_to([0, 0.45, 0])
        self.at("This inherited arrangement")
        self.play(FadeOut(VGroup(br, parental)), FadeIn(phase), run_time=0.8)
        self.at("Class size can support")
        self.play(Indicate(VGroup(bs[0], bs[1]), color=GREEN, scale_factor=1.03), run_time=0.8)
        self.at("phase defines it")
        self.play(Indicate(hs, color=TEAL, scale_factor=1.02), run_time=0.9)
        self.finish()


class S05Crossover(SpokenScene):
    def construct(self):
        cs = four_chromatids()
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT*0.15) for c in cs], lag_ratio=0.12), run_time=1.1)
        four = T("four chromatids", 30, TEXT).move_to([4.75, 3.25, 0])
        self.at("four chromatids")
        self.play(FadeIn(four), run_time=0.6)
        x = 0.0
        cross = Cross(Circle(radius=0.22), stroke_color=RED, stroke_width=5).move_to([x, 1.275, 0])
        self.at("A crossover joins")
        self.play(Indicate(VGroup(cs[1], cs[2]), color=RED, scale_factor=1.02), FadeIn(cross), run_time=0.9)
        cut1 = cs[1][0].copy(); cut2 = cs[2][0].copy()
        # Product bars preserve origin colour on either side of the exchange.
        prod1 = VGroup(Rectangle(width=5.4, height=0.38, stroke_width=0, fill_color=DOM, fill_opacity=0.9).move_to([-2.7, 1.70, 0]),
                       Rectangle(width=5.4, height=0.38, stroke_width=0, fill_color=REC, fill_opacity=0.9).move_to([2.7, 1.70, 0]))
        prod2 = VGroup(Rectangle(width=5.4, height=0.38, stroke_width=0, fill_color=REC, fill_opacity=0.9).move_to([-2.7, 0.85, 0]),
                       Rectangle(width=5.4, height=0.38, stroke_width=0, fill_color=DOM, fill_opacity=0.9).move_to([2.7, 0.85, 0]))
        labs = VGroup(T("A", 28, TEXT, weight=BOLD).move_to([-2.7, 2.16, 0]), T("b", 28, TEXT, weight=BOLD).move_to([2.7, 2.16, 0]),
                      T("a", 28, TEXT, weight=BOLD).move_to([-2.7, 0.39, 0]), T("B", 28, TEXT, weight=BOLD).move_to([2.7, 0.39, 0]))
        self.at("segments trade places")
        self.play(FadeOut(cs[1]), FadeOut(cs[2]), FadeIn(prod1), FadeIn(prod2), FadeIn(labs), run_time=1.2)
        self.at("Two chromatids keep")
        self.play(Indicate(VGroup(cs[0], cs[3]), color=GREEN, scale_factor=1.02), run_time=0.8)
        self.at("The exchanged chromatids")
        self.play(Indicate(VGroup(prod1, prod2), color=RED, scale_factor=1.02), FadeOut(cross), run_time=0.9)
        bs = bins((0.4, 0.4, 0.4, 0.4), base=-2.45, max_h=0.88)
        self.at("feed the recombinant bins")
        self.play(FadeIn(bs), run_time=0.6)
        products = four_tiles(-0.55)
        self.play(LaggedStart(*[products[i].animate.move_to([BIN_XS[i], -1.15, 0]).scale(0.72) for i in range(4)],
                              lag_ratio=0.15), run_time=1.5)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        cs = four_chromatids(marker_x=(-3.6, 0.8), ys=(2.65, 1.92, 1.19, 0.46))
        self.add(cs)
        right_marks = VGroup(*[c[1][2] for c in cs], cs[0][1][3], cs[3][1][3])
        self.at("slide the right marker")
        self.play(right_marks.animate.shift(RIGHT*2.8), run_time=1.8, rate_func=smooth)
        sparks = VGroup(*[Star(5, outer_radius=0.16, inner_radius=0.07, color=RED,
                              fill_color=RED, fill_opacity=0.9).move_to([x, y, 0])
                          for x, y in zip((-2.5, -0.8, 1.0, 2.5), (2.28, 1.55, 0.82, 2.28))])
        self.at("crossover positions")
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in sparks], lag_ratio=0.22), run_time=1.4)
        bs = bins((0.85, 0.85, 0.42, 0.42), base=-2.25, max_h=1.18)
        self.play(FadeIn(bs), run_time=0.6)
        qmark = T("?", 64, GOLD, weight=BOLD).move_to([3.2, -0.55, 0])
        q = question_card("Which pair of bins should claim a larger share?", y=-3.28, max_w=10.7)
        self.at("Which pair of bins")
        self.play(FadeIn(qmark, scale=0.6), FadeIn(q), run_time=0.9)
        self.at("Hold the chromosome")
        self.play(Indicate(VGroup(cs, qmark), color=GOLD, scale_factor=1.01), run_time=0.9)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        world = interval_world(question=True)
        q = question_card("Which pair of bins should claim a larger share?", y=-3.28, max_w=10.7)
        scan = Line([-3.6, 0.20, 0], [-3.6, 2.25, 0], color=GOLD, stroke_width=3).set_opacity(0.75)
        self.add(world, q, scan)
        self.play(scan.animate.shift(RIGHT*7.2), run_time=4.5, rate_func=linear)
        self.finish()


class S08Reveal(SpokenScene):
    def construct(self):
        world = interval_world(question=True)
        self.add(world)
        self.at("The recombinant pair grows")
        self.play(FadeOut(world[2]), world[1][2][1].animate.stretch_to_fit_height(0.92).shift(UP*0.25),
                  world[1][3][1].animate.stretch_to_fit_height(0.92).shift(UP*0.25), run_time=1.2)
        sparks = VGroup(*[Star(5, outer_radius=0.15, inner_radius=0.06, color=RED,
                              fill_color=RED, fill_opacity=0.9).move_to([x, 2.2-(i%3)*0.72, 0])
                          for i, x in enumerate(np.linspace(-3.0, 3.0, 7))])
        self.at("offers more places")
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in sparks], lag_ratio=0.12), run_time=1.5)
        bob(sparks, amp=0.12, speed=1.7)
        rare = T("second crossover: rare here", 28, GREY).move_to([0, 3.35, 0])
        self.at("a second crossover")
        self.play(FadeIn(rare), run_time=0.7)
        self.at("few exchanges stay hidden")
        self.play(FadeOut(sparks[1::2]), Indicate(sparks[::2], color=RED, scale_factor=1.12), run_time=0.9)
        frac = fraction_picture()
        self.at("The recombinant share")
        self.play(FadeOut(VGroup(world, sparks, rare)), FadeIn(frac), run_time=1.1)
        pulse(frac[1], base=4, amp=1.5, speed=2.0)
        self.add(scope_tag("short interval"))
        self.at("estimate of genetic map distance")
        self.play(Indicate(frac, color=TEAL, scale_factor=1.03), run_time=0.9)
        self.finish()


class S09Ruler(SpokenScene):
    def construct(self):
        frac = fraction_picture()
        pulse(frac[1], base=4, amp=1.5, speed=2.0)
        frac._t = 0.0
        frac._prev = 1.0
        def sway(m, dt):
            m._t += dt
            k = 1 + 0.025*np.sin(1.6*m._t)
            m.scale(k/m._prev, about_point=m.get_center())
            m._prev = k
        frac.add_updater(sway)
        self.add(frac)
        self.at("Add both recombinant classes")
        self.play(Indicate(frac[0], color=RED, scale_factor=1.05), run_time=0.9)
        self.at("dividing by all offspring")
        self.play(Indicate(frac[2], color=TEXT, scale_factor=1.05), run_time=0.9)
        pct = M("× 100%", 44, TEAL).next_to(frac, RIGHT, buff=0.45)
        self.at("as a percentage")
        self.play(FadeIn(pct, shift=LEFT*0.15), run_time=0.7)
        ruler = short_ruler().move_to([0, 1.05, 0])
        self.at("estimates centimorgans")
        self.play(FadeOut(VGroup(frac, pct)), FadeIn(ruler), run_time=1.2)
        dna = VGroup(RoundedRectangle(corner_radius=0.18, width=8.2, height=0.55,
                                     stroke_color=GREY, stroke_width=3, fill_color=GREY,
                                     fill_opacity=0.28).move_to([0, -1.55, 0]),
                     T("fixed DNA length", 30, GREY).move_to([0, -2.16, 0]))
        neq = T("≠", 58, RED, weight=BOLD).move_to([0, -0.72, 0])
        pulse(dna[0], base=3, amp=1.6, speed=2.5)
        neq._t = 0.0
        def bob(m, dt):
            m._t += dt
            m.move_to([0, -0.72 + 0.07*np.sin(3*m._t), 0])
            m.set_fill(opacity=0.75 + 0.25*np.sin(3*m._t))
        neq.add_updater(bob)
        dna[0].fill_opacity = 0.28
        def breathe(m, dt):
            m._u = getattr(m, "_u", 0.0) + dt
            m.set_fill(GREY, opacity=0.28 + 0.14*np.sin(2*m._u))
        dna[0].add_updater(breathe)
        self.at("does not measure")
        self.play(FadeIn(neq), FadeIn(dna), run_time=0.9)
        regions = T("region and sex can change the conversion", 30, TEXT).move_to([0, -2.95, 0])
        self.at("Different chromosome regions")
        self.play(FadeIn(regions), run_time=0.8)
        self.at("physical spacing differently")
        self.play(ruler.animate.stretch(0.82, 0), dna.animate.stretch(1.08, 0), run_time=1.0)
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        hs = homologues(marker_x=(-2.7, 2.7), ys=(2.65, 1.6))
        self.play(FadeIn(hs), run_time=0.7)
        step = T("1  Read the parents", 32, BLUE, weight=BOLD).move_to([0, 3.35, 0])
        self.at("Read the parents")
        self.play(FadeIn(step), Indicate(hs, color=TEXT, scale_factor=1.02), run_time=0.8)
        classes = four_tiles(0.25)
        step2 = T("2  Name classes from phase", 32, GREEN, weight=BOLD).move_to(step)
        self.at("Name the parental")
        self.play(swap(step, step2), FadeOut(hs), FadeIn(classes), run_time=1.0)
        merged = allele_tile("recombinants", (RED, RED), width=3.4, height=0.72).move_to([0, 0.25, 0])
        step3 = T("3  Add recombinants ÷ total", 32, RED, weight=BOLD).move_to(step)
        self.at("Add the recombinant classes")
        self.play(swap(step2, step3), FadeOut(classes), FadeIn(merged), run_time=1.0)
        total = T("all offspring", 30, TEXT).move_to([0, -0.75, 0])
        rule = Line([-2.2, -0.30, 0], [2.2, -0.30, 0], color=TEXT, stroke_width=4)
        self.at("then divide")
        self.play(FadeIn(rule), FadeIn(total), run_time=0.8)
        ruler = short_ruler().move_to([0, -0.25, 0])
        step4 = T("4  Use the short-interval ruler", 32, TEAL, weight=BOLD).move_to(step)
        self.at("Only then")
        self.play(swap(step3, step4), FadeOut(VGroup(merged, rule, total)), FadeIn(ruler), run_time=1.1)
        hidden = T("What if crossovers hide one another?", 30, GOLD).move_to([0, -2.0, 0])
        self.at("The next question")
        self.play(FadeIn(hidden), run_time=0.8)
        self.play(FadeOut(VGroup(step4, hidden)), ruler.animate.move_to(ORIGIN), run_time=0.9)
        self.finish()


class S11End(EndCard):
    LINE = "For short intervals, recombination frequency estimates map distance."
