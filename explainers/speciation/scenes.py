"""Speciation: how barriers between species grow  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept, whole video)
  BLUE   = gene flow (the band, the arrow, the gene-flow-left numbers)
  ORANGE = a reproductive barrier, its strength (RI) and the credit it earns (the blocked share)
  GREEN  = total isolation
  YELLOW = highlight (the zygote line, the stretch of gene flow a barrier acts on)
  RED    = a flower of M. cardinalis; the struck-out raw sum
  PINK   = a flower of M. lewisii
  GREY   = labels, the gene flow not yet blocked in the credit bar
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#F29CC3"
FRED = "#D7263D"

YB = 0.6                      # centre line of the gene-flow band
H = 2.4                       # band height for gene flow 1.00
G = [-3.9, -0.4, 3.1]         # gate x positions
XS = [-6.2, G[0], G[1], G[2], 6.2]
XMID = [(XS[j] + XS[j + 1]) / 2 for j in range(4)]
LX0 = -3.9                    # left end of the credit bar (10 wide)
LY = -2.1                     # credit bar y
ORDER_A = [("Ecogeographic", 0.60), ("Pollinator", 0.90), ("Hybrid fertility", 0.50)]
ORDER_B = [("Pollinator", 0.90), ("Ecogeographic", 0.60), ("Hybrid fertility", 0.50)]


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def R(x0, x1, y0, y1, color, fo, sw=0):
    w = max(x1 - x0, 0.002)
    h = max(y1 - y0, 0.002)
    r = Rectangle(width=w, height=h, stroke_width=sw, stroke_color=color, fill_color=color, fill_opacity=fo)
    return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def flower(color, r=1.3):
    petals = [Circle(radius=0.5 * r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
              .move_to([0.62 * r * np.cos(a), 0.62 * r * np.sin(a), 0]) for a in np.arange(5) * TAU / 5 + PI / 2]
    mid = Circle(radius=0.3 * r, stroke_width=0, fill_color=GOLD, fill_opacity=1)
    return VGroup(*petals, mid)


def dyn(order, k):
    """Everything that depends on how many barriers have acted (k of 3)."""
    ri = [r for _, r in order]
    f, cur = [1.0], 1.0
    for i in range(3):
        if i < k:
            cur *= 1 - ri[i]
        f.append(cur)
    band = [R(XS[j], XS[j + 1], YB - H * f[j] / 2, YB + H * f[j] / 2, BLUE, 0.55, sw=1.5) for j in range(4)]
    gates = [VGroup(R(G[i] - .17, G[i] + .17, YB + H * f[i + 1] / 2, YB + H * f[i] / 2, ORANGE, .9),
                    R(G[i] - .17, G[i] + .17, YB - H * f[i] / 2, YB - H * f[i + 1] / 2, ORANGE, .9)) for i in range(3)]
    ac = [ri[i] * f[i] if i < k else 0.0 for i in range(3)]
    rem = 1 - sum(ac)
    led, x = [], LX0
    for i, a in enumerate(ac):
        led.append(R(x, x + 10 * a, LY - .25, LY + .25, ORANGE, [.9, .55, .9][i]))
        x += 10 * a
    led.append(R(x, LX0 + 10, LY - .25, LY + .25, GREY, .35))
    vals = [M(f"{f[j]:.2f}", 26, BLUE).move_to([XMID[j], -0.95, 0]) if j <= k else None for j in range(4)]
    acl, cum = [], 0.0
    for i in range(3):
        if i < k:
            acl.append(M(f"{ac[i]:.2f}", 24, ORANGE).move_to([LX0 + 10 * (cum + ac[i] / 2), -2.7 if i < 2 else -3.1, 0]))
        else:
            acl.append(None)
        cum += ac[i]
    return dict(band=band, gates=gates, led=led, vals=vals, acl=acl, f=f, ac=ac)


def names_of(order, k_ri=3):
    names = [bchip(n, ORANGE, 28).move_to([G[i], 3.0, 0]) for i, (n, _) in enumerate(order)]
    ris = [M(f"RI = {r:.2f}", 24, ORANGE).move_to([G[i], 2.2, 0]) for i, (_, r) in enumerate(order)]
    return names, ris


def statics():
    gene = T("gene flow", 26, TEXT).move_to([XMID[0], YB, 0])
    cred = T("credit", 24, ORANGE).move_to([-5.2, LY, 0])
    tag = T("illustrative numbers", 22, GREY).move_to([-3.9, -3.1, 0])
    return gene, cred, tag


def add_state(sc, d, k):
    for m in d["band"] + d["gates"] + d["led"]:
        sc.add(m)
    for m in d["vals"] + d["acl"]:
        if m is not None:
            sc.add(m)


def go(cur, new):
    """animations that bring the state `cur` to `new`; mutates cur so later calls keep working."""
    anims = []
    for key in ("band", "gates", "led"):
        for a, b in zip(cur[key], new[key]):
            anims.append(Transform(a, b))
    for key in ("vals", "acl"):
        for i, (a, b) in enumerate(zip(cur[key], new[key])):
            if a is None and b is not None:
                anims.append(FadeIn(b)); cur[key][i] = b
            elif a is not None and b is None:
                anims.append(FadeOut(a)); cur[key][i] = None
            elif a is not None and b is not None:
                anims.append(Transform(a, b))
    return anims


def hl(d, j):
    return SurroundingRectangle(d["band"][j], color=YELLOW, buff=0.08, stroke_width=4)


def qboxes():
    return [bchip("?", ORANGE, 60).move_to([x, -0.7, 0]) for x in (-1.3, 0, 1.3)]


# Schematic organisms, never molecular structures.
def fish(color=BLUE, benthic=False):
    body = Ellipse(width=1.05, height=0.56 if benthic else 0.34,
                   color=color, fill_opacity=0.65, stroke_width=2.5)
    tail = Polygon([-.48, 0, 0], [-.85, .25, 0], [-.85, -.25, 0],
                   color=color, fill_opacity=0.65, stroke_width=2.5)
    eye = Dot([.32, .06, 0], radius=.035, color=BG)
    return VGroup(body, tail, eye)


def bee():
    body = Ellipse(width=.6, height=.36, color=GOLD, fill_opacity=.9)
    wings = VGroup(*[Ellipse(width=.3, height=.4, color=GREY, fill_opacity=.3)
                     .move_to([x, .22, 0]) for x in (-.12, .12)])
    stripes = VGroup(*[Line([x, -.14, 0], [x, .14, 0], color=BG, stroke_width=4)
                       for x in (-.1, .08)])
    return VGroup(wings, body, stripes)


def bird():
    body = Ellipse(width=.65, height=.3, color=GREY, fill_opacity=.8)
    wing = Polygon([0, .02, 0], [-.3, .65, 0], [.2, .1, 0], color=GREY, fill_opacity=.6)
    beak = Line([.3, 0, 0], [.8, .05, 0], color=GREY, stroke_width=3)
    return VGroup(body, wing, beak)


def heading(text):
    return T(text, 34, font=TITLE_FONT).move_to([0, 3.05, 0])


class S00Title(TitleCard):
    LESSON = "Speciation"
    TITLE = "How Barriers Between Species Grow"

    def construct(self):
        title = T(self.TITLE, 44, font=TITLE_FONT).move_to([0, 1.65, 0])
        fit(title, max_w=12.2)
        flowers = VGroup(flower(PINK, .85).move_to([-2, -.9, 0]),
                         flower(FRED, .85).move_to([2, -.9, 0]))
        lesson = T(self.LESSON.upper(), 22, GREY).move_to([0, 2.65, 0])
        self.play(FadeIn(lesson), FadeIn(title), GrowFromCenter(flowers), run_time=.8)
        self.finish()


class S01Lead(SpokenScene):
    def construct(self):
        f1 = flower(PINK).move_to([-4.3, .3, 0])
        f2 = flower(FRED).move_to([4.3, .3, 0])
        self.at("Two")
        self.play(GrowFromCenter(f1), GrowFromCenter(f2), run_time=.7)
        arrow = DoubleArrow([-2.6, .8, 0], [2.6, .8, 0], color=BLUE,
                            stroke_width=6, buff=0, tip_length=.25)
        by = T("crossed by hand", 26, GREY).move_to([0, 1.5, 0])
        seed = VGroup(Ellipse(width=.3, height=.45, color=GOLD, fill_opacity=.8),
                      T("hybrid seed", 24, GREY).move_to([0, -.6, 0])).move_to([0, -.45, 0])
        self.at("crossed by hand")
        self.play(GrowFromCenter(arrow), FadeIn(by), run_time=.6)
        self.at("hybrid seed")
        self.play(GrowFromCenter(seed), run_time=.5)
        b1 = VGroup(bee(), T("bumblebees", 24, GREY).shift(UP * .8)).move_to([-4.3, 2.6, 0])
        b2 = VGroup(bird(), T("hummingbirds", 24, GREY).shift(UP * .9)).move_to([4.3, 2.6, 0])
        self.at("bumblebees")
        self.play(FadeIn(b1, shift=DOWN * .2), run_time=.5)
        self.at("hummingbirds")
        self.play(FadeIn(b2, shift=DOWN * .2), run_time=.5)
        band = R(-2.6, 2.6, -.4, .4, BLUE, .55)
        flow = T("gene flow in the wild", 26, BLUE).move_to([0, -1.2, 0])
        self.at("Yet in the wild")
        self.play(FadeOut(arrow), FadeOut(by), FadeOut(seed), FadeIn(band), FadeIn(flow), run_time=.6)
        self.at("almost no genes")
        self.play(Transform(band, R(-2.6, 2.6, -.025, .025, BLUE, .6)), run_time=.8)
        barrier = bchip("barriers to gene flow", ORANGE, 26).move_to([0, -2.3, 0])
        self.at("barriers that cut")
        self.play(FadeIn(barrier), run_time=.6)
        self.at("different places")
        self.play(f1.animate.shift(LEFT * .3), f2.animate.shift(RIGHT * .3), run_time=.7)
        self.at("different pollinators")
        self.play(Indicate(b1, scale_factor=1.05), Indicate(b2, scale_factor=1.05), run_time=.6)
        self.finish()


class S02Barriers(SpokenScene):
    def construct(self):
        title = heading("Reproductive barriers reduce gene flow")
        chips = [bchip(n, ORANGE, 26).move_to([x, .4, 0])
                 for n, x in zip(("habitat", "pollinator", "hybrid fertility"), (-4.7, -1.7, 4.1))]
        self.at("A reproductive barrier")
        self.play(FadeIn(title), run_time=.6)
        line = DashedLine([1.2, -1.6, 0], [1.2, 2.4, 0], color=YELLOW, stroke_width=4)
        z = T("zygote", 26, YELLOW).move_to([1.2, -2, 0])
        before = T("before the zygote", 30).move_to([-3.1, 1.9, 0])
        after = T("after", 30).move_to([4.1, 1.9, 0])
        self.at("sorted by when")
        self.play(Create(line), FadeIn(z), run_time=.7)
        self.at("Where the plants grow")
        self.play(FadeIn(chips[0], shift=RIGHT * .3), run_time=.6)
        self.at("pollinators visit them")
        self.play(FadeIn(chips[1], shift=RIGHT * .3), run_time=.6)
        self.at("act before")
        self.play(FadeIn(before), run_time=.5)
        self.at("the fertilized egg")
        self.play(Indicate(z, color=YELLOW, scale_factor=1.08), run_time=.5)
        self.at("Low hybrid fertility")
        self.play(FadeIn(chips[2], shift=RIGHT * .3), FadeIn(after), run_time=.6)
        note = T("No single barrier is complete", 26, GREY).move_to([0, -3, 0])
        self.at("No single barrier")
        self.play(FadeIn(note), run_time=.6)
        glow = RoundedRectangle(width=6.5, height=2.9, corner_radius=.2,
                                color=ORANGE, fill_opacity=.07).move_to([-3.15, .8, 0]).set_z_index(-1)
        self.at("most of the isolation")
        self.play(Create(glow), run_time=.7)
        self.finish()


class S03Adaptation(SpokenScene):
    def construct(self):
        title = heading("Barriers grow from adaptation")
        slope = Polygon([-6, -2.5, 0], [5.8, 2, 0], [6, -2.5, 0],
                        color=GREY, fill_opacity=.08, stroke_width=3)
        red = flower(FRED, .65).move_to([-3.8, -1.1, 0])
        pink = flower(PINK, .65).move_to([3.3, 1.5, 0])
        self.at("These barriers")
        self.play(FadeIn(title), Create(slope), run_time=.7)
        self.at("lower elevations")
        self.play(GrowFromCenter(red), run_time=.6)
        self.at("higher ones")
        self.play(GrowFromCenter(pink), run_time=.6)
        b = bee().move_to([1.7, 2.2, 0])
        h = bird().move_to([-5.4, -.3, 0])
        self.at("suits bumblebees")
        self.play(FadeIn(b), b.animate.move_to([2.4, 1.9, 0]), run_time=.6)
        self.at("suits hummingbirds")
        self.play(FadeIn(h), h.animate.move_to([-4.8, -.6, 0]), run_time=.6)
        habitat = bchip("habitat", ORANGE, 26).move_to([0, -.9, 0])
        pollinator = bchip("pollinator", ORANGE, 26).move_to([3.5, -.9, 0])
        self.at("plants rarely meet")
        self.play(FadeIn(habitat, shift=DOWN * .4), run_time=.6)
        self.at("carries little pollen")
        self.play(b.animate.shift(LEFT * .3), h.animate.shift(RIGHT * .3),
                  FadeIn(pollinator, shift=DOWN * .4), run_time=.7)
        rule = T("Isolation is a side effect", 30, GREEN).move_to([0, -3.15, 0])
        self.at("Isolation is a side effect")
        self.play(FadeIn(rule), run_time=.6)
        self.at("ecological speciation")
        self.play(Transform(title, heading("Ecological speciation")), run_time=.6)
        self.finish()


class S04Sticklebacks(SpokenScene):
    def construct(self):
        title = heading("Does isolation follow ecology?")
        lakes, bottom, water = [], [], []
        for x in (-4.3, 0, 4.3):
            outline = Ellipse(width=3.1, height=3.4, color=GREY, fill_opacity=.05).move_to([x, .25, 0])
            lakes.append(outline)
            bottom.append(fish(ORANGE, True).move_to([x, -.7, 0]))
            water.append(fish(BLUE).move_to([x, 1, 0]))
        lakegroup = VGroup(*lakes)
        fishgroup = VGroup(*bottom, *water)
        legend = VGroup(T("bottom-feeding", 25, ORANGE), T("open-water", 25, BLUE)).arrange(RIGHT, buff=1).move_to([0, -2.4, 0])
        self.at("How do we know")
        self.play(FadeIn(title), run_time=.6)
        self.at("Lakes in British Columbia")
        self.play(Create(lakegroup), run_time=.8)
        self.at("a bottom feeding")
        self.play(FadeIn(VGroup(*bottom)), run_time=.6)
        self.at("an open water")
        self.play(FadeIn(VGroup(*water)), FadeIn(legend), run_time=.6)
        self.at("arisen on its own")
        self.play(LaggedStart(*[Indicate(l, color=GREY, scale_factor=1.03) for l in lakes], lag_ratio=.15), run_time=.8)
        breaks = VGroup()
        for x in (-4.3, 0, 4.3):
            breaks.add(DashedLine([x, -.25, 0], [x, .55, 0], color=RED),
                       Line([x-.18, .05, 0], [x+.18, .25, 0], color=RED, stroke_width=5))
        note = T("different forms: rarely mate", 26, RED).move_to([0, -3.2, 0])
        self.at("different forms rarely mated")
        self.play(Create(breaks), FadeIn(note), run_time=.8)
        links = VGroup(*[Line([a, y, 0], [b, y, 0], color=GREEN, stroke_width=4)
                         for y in (-.7, 1) for a, b in ((-3.5, -.85), (.85, 3.45))]).set_z_index(-1)
        self.at("from different lakes")
        self.play(FadeOut(breaks), FadeOut(note), Create(links), run_time=.6)
        result = T("same form across lakes: mate readily", 26, GREEN).move_to([0, -3.2, 0])
        self.at("mated readily")
        self.play(FadeIn(result), run_time=.5)
        self.at("Isolation followed ecology")
        self.play(Transform(title, heading("Isolation followed ecology")), run_time=.6)
        self.finish()


class S05Combine(SpokenScene):
    def construct(self):
        title = heading("Each barrier acts on what remains")
        d = dyn(ORDER_A, 0)
        band = VGroup(*d['band'])
        gates = VGroup(*d['gates'])
        labels = VGroup(*[T(n, 24, ORANGE).move_to([x, 2.15, 0])
                         for n, x in zip(("habitat", "pollinator", "hybrid fertility"), G)])
        flow = T("gene flow", 26, BLUE).move_to([-5, -1.35, 0])
        self.at("Barriers act in sequence")
        self.play(FadeIn(title), GrowFromEdge(band, LEFT), FadeIn(labels), FadeIn(flow), run_time=.8)
        self.add(gates)
        self.at("Each one can only block")
        d1 = dyn(ORDER_A, 1)
        self.play(*[Transform(a,b) for a,b in zip(d['band'],d1['band'])],
                  *[Transform(a,b) for a,b in zip(d['gates'],d1['gates'])], run_time=.8)
        self.at("earlier barriers left behind")
        for k in (2,3):
            nxt = dyn(ORDER_A, k)
            self.play(*[Transform(a,b) for a,b in zip(d['band'],nxt['band'])],
                      *[Transform(a,b) for a,b in zip(d['gates'],nxt['gates'])], run_time=.55)
        assumption = T("if barriers act independently", 24, GREY).move_to([0, -1.6, 0])
        formula = M("1 − (1 − RI1) × (1 − RI2) × (1 − RI3)", 28, GREEN).move_to([0, -2.6, 0])
        self.at("if they act independently")
        self.play(FadeOut(flow), FadeIn(assumption), run_time=.5)
        self.at("fractions that get through multiply")
        product = M("(1 − RI1) × (1 − RI2) × (1 − RI3)", 28, BLUE).move_to([0, -2.6, 0])
        self.play(FadeIn(product), run_time=.6)
        self.at("total isolation is")
        self.play(ReplacementTransform(product, formula), run_time=.6)
        raw = M("RI1 + RI2 + RI3", 26, ORANGE).move_to([0, -1.6, 0])
        strike = Line(raw.get_left()+LEFT*.15, raw.get_right()+RIGHT*.15, color=RED, stroke_width=5)
        self.at("Never just add")
        self.play(FadeOut(assumption), FadeIn(raw), Create(strike), run_time=.6)
        self.at("more than one")
        self.play(Indicate(raw, color=RED, scale_factor=1.04), run_time=.5)
        self.finish()


class S06Where(SpokenScene):
    def construct(self):
        title = heading("Where is separate from how")
        panels = VGroup(*[RoundedRectangle(width=3.8, height=3.2, corner_radius=.2, color=GREY)
                          .move_to([x, .3, 0]) for x in (-4.3, 0, 4.3)])
        dots = VGroup(*[Dot([x+dx, y, 0], radius=.12, color=BLUE)
                        for x in (-4.3, 0, 4.3) for dx,y in ((-.9,0),(-.6,.9),(.6,.9),(.9,0))])
        split = R(-4.55, -4.05, -1.25, 1.85, GREY, .65)
        names = VGroup(T("split population", 24), T("dispersal", 24), T("one area",24))
        for n,x in zip(names,(-4.3,0,4.3)): n.move_to([x,-1.95,0])
        self.at("Where speciation happens")
        self.play(FadeIn(title), Create(panels), FadeIn(dots), run_time=.8)
        self.at("can split a population")
        self.play(GrowFromCenter(split), FadeIn(names[0]), run_time=.6)
        island = Ellipse(width=1.1, height=1.4, color=GREY).move_to([.95,.4,0])
        crossing = Arrow([-.9,.2,0],[.5,.2,0],color=BLUE,buff=.05,stroke_width=3)
        self.at("allopatric speciation")
        self.play(Create(island), GrowArrow(crossing), FadeIn(names[1]),
                  dots[4].animate.move_to([1.1, .45, 0]), run_time=.6)
        self.at("diverge in one place")
        self.play(*[dots[i].animate.set_color(ORANGE) for i in (10,11)],FadeIn(names[2]),run_time=.6)
        warning=T("Living together does not prove a sympatric start",26,YELLOW).move_to([0,-3,0])
        self.at("Living together today")
        self.play(FadeIn(warning),run_time=.6)
        crater=Circle(radius=1.65,color=GREY,fill_opacity=.06).move_to([2,.25,0])
        source=Ellipse(width=3.7,height=2.1,color=GREY,fill_opacity=.06).move_to([-3.9,.25,0])
        pair=VGroup(fish(BLUE).move_to([1.6,.8,0]),fish(ORANGE,True).move_to([2.3,-.4,0]))
        label=T("Nicaragua: crater lake",26).move_to([2,-2,0])
        self.at("For crater lake cichlids")
        self.play(*[FadeOut(m) for m in (panels,dots,split,names,island,crossing,warning)],
                  Transform(title,heading("Divergence inside the lake")),Create(crater),Create(source),FadeIn(pair),FadeIn(label),run_time=.8)
        evidence=T("supported by genome-wide models",25,GREY).move_to([0,-3,0])
        self.at("models supported divergence")
        self.play(FadeIn(evidence),run_time=.6)
        inflow=Arrow([-1.9,.3,0],[.25,.3,0],color=BLUE,stroke_width=2,buff=.05,tip_length=.16)
        flowlabel=T("some genes from outside",24,BLUE).move_to([-2,1.9,0])
        self.at("some genes arriving")
        self.play(GrowArrow(inflow),FadeIn(flowlabel),run_time=.7)
        self.finish()


class S07Polyploidy(SpokenScene):
    def construct(self):
        title=heading("A faster route: whole-genome doubling")
        parents=VGroup(bchip("parent",PINK,28).move_to([-4.6,1.3,0]),
                       bchip("parent",FRED,28).move_to([-4.6,-1.3,0]))
        arrows=VGroup(*[Arrow([-3.5,y,0],[-1.5,0,0],buff=.15,color=GREY) for y in (1.3,-1.3)])
        hybrid=bchip("hybrid",GREY,28).move_to([-.4,0,0])
        # Abstract cards stand for a whole genome, not chromosomes or molecular structures.
        genome=bchip("genome",YELLOW,24).move_to([-.4,-1.3,0])
        self.at("There is also")
        self.play(FadeIn(title),run_time=.6)
        self.at("In plants especially")
        self.play(FadeIn(parents),run_time=.6)
        self.at("a hybrid can")
        self.play(GrowArrow(arrows[0]),GrowArrow(arrows[1]),FadeIn(hybrid),FadeIn(genome),run_time=.6)
        doubled=VGroup(bchip("genome",YELLOW,24).move_to([3.5,-.6,0]),
                       bchip("genome",YELLOW,24).move_to([3.5,-1.5,0]))
        self.at("double its whole genome")
        self.play(ReplacementTransform(genome,doubled),run_time=.8)
        poly=bchip("polyploid lineage",GREEN,26).move_to([3.5,.7,0])
        self.at("new polyploid lineage")
        self.play(FadeIn(poly),run_time=.6)
        barrier=VGroup(Line([1.3,-2,0],[1.3,-.25,0],color=ORANGE,stroke_width=6),
                       Line([1.3,.3,0],[1.3,2,0],color=ORANGE,stroke_width=6))
        note=T("partly isolated • one generation",26,ORANGE).move_to([0,-2.7,0])
        self.at("partly isolated")
        self.play(Create(barrier),FadeIn(note),run_time=.6)
        self.at("Either way")
        self.play(*[FadeOut(m) for m in (parents,arrows,hybrid,doubled,barrier,note)],
                  poly.animate.move_to([0,0,0]),run_time=.7)
        rule=T("Barriers cut gene flow",36,ORANGE).move_to([0,1.5,0])
        self.at("Barriers cut gene flow")
        self.play(FadeOut(title),FadeIn(rule),run_time=.6)
        path=Arrow([0,-.5,0],[3,-1.8,0],color=GREEN,buff=.1)
        own=T("evolves on its own",30,GREEN).move_to([3,-2.5,0])
        self.at("a new lineage evolves")
        self.play(GrowArrow(path),FadeIn(own),run_time=.7)
        self.finish()


class S08End(EndCard):
    LINE = "Barriers cut gene flow; a new lineage evolves on its own."
