"""Speciation: barriers act on what remains  (Biochemistrypedia explainer)

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


class S00Title(TitleCard):
    LESSON = "Speciation"
    TITLE = "Barriers act on what remains"


def qboxes():
    return [bchip("?", ORANGE, 60).move_to([x, -0.7, 0]) for x in (-1.3, 0, 1.3)]


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        f1 = flower(PINK).move_to([-4.3, 0.5, 0])
        f2 = flower(FRED).move_to([4.3, 0.5, 0])
        n1 = T("Mimulus lewisii", 26, PINK, slant=ITALIC).move_to([-4.3, -1.5, 0])
        n2 = T("M. cardinalis", 26, FRED, slant=ITALIC).move_to([4.3, -1.5, 0])
        self.at("Two monkey")
        self.play(GrowFromCenter(f1), GrowFromCenter(f2), FadeIn(n1), FadeIn(n2), run_time=1.0)
        arrow = DoubleArrow([-2.6, 0.9, 0], [2.6, 0.9, 0], color=BLUE, stroke_width=6, buff=0, tip_length=0.25)
        by = T("crossed by hand", 24, GREY).move_to([0, 1.3, 0])
        seed = T("hybrid seed", 24, GREY).move_to([0, 0.45, 0])
        self.at("crossed by hand")
        self.play(GrowFromCenter(arrow), FadeIn(by), run_time=0.8)
        self.at("hybrid seed")
        self.play(FadeIn(seed), run_time=0.5)
        b1 = bchip("bumblebees", GREY, 24).move_to([-4.3, 2.9, 0])
        b2 = bchip("hummingbirds", GREY, 24).move_to([4.3, 2.9, 0])
        self.at("bumblebees")
        self.play(FadeIn(b1, shift=DOWN * 0.2), run_time=0.5)
        self.at("hummingbirds")
        self.play(FadeIn(b2, shift=DOWN * 0.2), run_time=0.5)
        bar = R(-0.12, 0.12, 0.45, 1.35, ORANGE, 0.9)
        big = M("99.87%", 54, GREEN).move_to([0, 2.5, 0])
        sub = T("of gene flow blocked (estimated average)", 22, GREEN).move_to([0, 1.95, 0])
        self.at("estimated to block")
        self.play(FadeOut(by), FadeOut(seed), arrow.animate.set_opacity(0.3), GrowFromCenter(bar), FadeIn(big), FadeIn(sub), run_time=1.0)
        q = qboxes()
        self.at("holds them apart")
        self.play(*[FadeIn(b, scale=0.6) for b in q], lag_ratio=0.2, run_time=1.0)
        self.play(Indicate(VGroup(*q), color=ORANGE, scale_factor=1.12), run_time=0.8)
        self.finish()


class S02Barriers(SpokenScene):
    def construct(self):
        q = qboxes()
        for b in q:
            self.add(b)
        flow = Arrow([-6.2, YB, 0], [6.2, YB, 0], color=BLUE, stroke_width=8, buff=0, tip_length=0.3)
        flow.set_z_index(-1)
        flbl = T("gene flow", 26, BLUE).move_to([-5.2, YB - 0.75, 0])
        self.at("reproductive barrier")
        names = [bchip(n, ORANGE, 28).move_to([G[i], YB, 0]) for i, (n, _) in enumerate(ORDER_A)]
        boxes_to = [bchip("?", ORANGE, 60).move_to([G[i], YB, 0]) for i in range(3)]
        self.play(*[ReplacementTransform(a, b) for a, b in zip(q, boxes_to)], run_time=0.9)
        self.at("reduces gene flow")
        self.play(GrowFromEdge(flow, LEFT), FadeIn(flbl), run_time=0.9)
        zl = DashedLine([1.2, -1.2, 0], [1.2, 3.1, 0], color=YELLOW, stroke_width=4)
        dot = Dot([1.2, -0.7, 0], color=YELLOW, radius=0.14)
        zt = T("zygote", 26, YELLOW).move_to([1.2, -1.6, 0])
        pre = T("before the zygote", 32, TEXT).move_to([-2.5, 2.35, 0])
        pre2 = T("prezygotic", 24, GREY).move_to([-2.5, 1.8, 0])
        post = T("after the zygote", 32, TEXT).move_to([3.8, 2.35, 0])
        post2 = T("postzygotic", 24, GREY).move_to([3.8, 1.8, 0])
        self.at("sorted by when")
        self.play(Create(zl), FadeIn(dot), FadeIn(zt), run_time=0.9)
        self.at("Where the plants grow")
        self.play(ReplacementTransform(boxes_to[0], names[0]), FadeIn(pre), FadeIn(pre2), run_time=0.7)
        self.at("which pollinators")
        self.play(ReplacementTransform(boxes_to[1], names[1]), run_time=0.7)
        self.at("fertilized egg")
        self.play(Indicate(zt, color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.at("Low fertility")
        self.play(ReplacementTransform(boxes_to[2], names[2]), FadeIn(post), FadeIn(post2), run_time=0.7)
        self.at("several barriers")
        self.play(*[Indicate(n, color=ORANGE, scale_factor=1.12) for n in names], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03First(SpokenScene):
    def construct(self):
        names = [bchip(n, ORANGE, 28).move_to([G[i], YB, 0]) for i, (n, _) in enumerate(ORDER_A)]
        flow = Arrow([-6.2, YB, 0], [6.2, YB, 0], color=BLUE, stroke_width=8, buff=0, tip_length=0.3)
        flow.set_z_index(-1)
        self.add(flow, *names)
        names2, ris = names_of(ORDER_A)
        gene, cred, tag = statics()
        d0 = dyn(ORDER_A, 0)
        d0["band"] = [R(XS[j], XS[j + 1], YB - H / 2, YB + H / 2, BLUE, 0.55, sw=1.5) for j in range(4)]
        self.at("Barriers act in sequence")
        self.play(*[n.animate.move_to([G[i], 3.0, 0]) for i, n in enumerate(names)],
                  FadeOut(flow), *[GrowFromEdge(b, LEFT) for b in d0["band"]], FadeIn(gene), run_time=1.2)
        self.add(*d0["gates"], *d0["led"])
        self.play(FadeIn(d0["vals"][0]), run_time=0.4)
        self.at("earlier barriers")
        self.play(Indicate(d0["band"][0], color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.at("illustrative")
        self.play(FadeIn(tag), FadeIn(cred), FadeIn(d0["led"][3]), run_time=0.7)
        self.at("barrier blocks")
        self.play(Indicate(d0["led"][3], color=ORANGE, scale_factor=1.0), run_time=0.6)
        self.at("The first barrier")
        self.play(Indicate(names[0], color=ORANGE, scale_factor=1.12), FadeIn(ris[0]), run_time=0.8)
        d1 = dyn(ORDER_A, 1)
        self.at("gets credit")
        # the gate closes and the credit appears together
        self.play(*go(d0, d1), run_time=1.2)
        self.finish()


class S04Next(SpokenScene):
    def construct(self):
        names, ris = names_of(ORDER_A)
        gene, cred, tag = statics()
        d = dyn(ORDER_A, 1)
        self.add(*names, ris[0], gene, cred, tag)
        add_state(self, d, 1)
        self.at("pollinator barrier")
        self.play(Indicate(names[1], color=ORANGE, scale_factor=1.12), FadeIn(ris[1]), run_time=0.8)
        box = hl(d, 1)
        eq1 = M("0.90 × 0.40", 28, TEXT).move_to([G[1] + 0.2, 1.65, 0])
        self.at("acts only on")
        self.play(Create(box), FadeIn(eq1), run_time=0.8)
        eq1b = M("0.90 × 0.40 = 0.36", 28, TEXT).move_to([G[1] + 0.2, 1.65, 0])
        d2 = dyn(ORDER_A, 2)
        self.at("It blocks")
        self.play(Transform(eq1, eq1b), *go(d, d2), run_time=1.2)
        self.at("hybrid fertility")
        self.play(FadeOut(box), FadeOut(eq1), Indicate(names[2], color=ORANGE, scale_factor=1.12), FadeIn(ris[2]), run_time=0.8)
        box2 = hl(d, 2)
        eq2 = M("0.50 × 0.04", 28, TEXT).move_to([G[2] + 0.2, 1.65, 0])
        self.at("acts on the")
        self.play(Create(box2), FadeIn(eq2), run_time=0.8)
        eq2b = M("0.50 × 0.04 = 0.02", 28, TEXT).move_to([G[2] + 0.2, 1.65, 0])
        d3 = dyn(ORDER_A, 3)
        self.at("It blocks", nth=1)
        self.play(Transform(eq2, eq2b), *go(d, d3), run_time=1.2)
        self.finish()


class S05Total(SpokenScene):
    def construct(self):
        names, ris = names_of(ORDER_A)
        gene, cred, tag = statics()
        d = dyn(ORDER_A, 3)
        self.add(*names, *ris, gene, cred, tag)
        add_state(self, d, 3)
        y = 1.65
        lbl = M("left =", 28, TEXT).move_to([-1.7, y, 0])
        f1 = M("0.40", 28, TEXT).next_to(lbl, RIGHT, buff=0.25)
        f2 = M("× 0.10", 28, TEXT).next_to(f1, RIGHT, buff=0.2)
        f3 = M("× 0.50", 28, TEXT).next_to(f2, RIGHT, buff=0.2)
        res = M("= 0.02", 28, TEXT).next_to(f3, RIGHT, buff=0.2)
        self.at("minus what")
        self.play(FadeIn(lbl), run_time=0.5)
        self.at("Multiply what")
        self.play(FadeIn(f1), run_time=0.5)
        self.at("times")
        self.play(FadeIn(f2), run_time=0.5)
        self.at("times", nth=1)
        self.play(FadeIn(f3), run_time=0.5)
        self.at("That is")
        self.play(FadeIn(res), run_time=0.5)
        x1 = LX0 + 9.6
        brace = Line([LX0, -1.75, 0], [x1, -1.75, 0], color=GREEN, stroke_width=6)
        tot = T("total isolation", 26, GREEN)
        totn = M("0.98", 30, GREEN)
        grp = VGroup(tot, totn).arrange(RIGHT, buff=0.25).move_to([(LX0 + x1) / 2, -1.45, 0])
        self.at("so total isolation")
        self.play(Create(brace), FadeIn(grp), run_time=0.9)
        sm = M("0.60 + 0.90 + 0.50 = 2.00", 28, ORANGE).move_to([1.6, y, 0])
        self.at("Do not add")
        self.play(FadeOut(VGroup(lbl, f1, f2, f3, res)), FadeIn(sm), run_time=0.7)
        strike = Line(sm.get_left() + LEFT * 0.1, sm.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        note = T("not a fraction of gene flow", 24, RED).move_to([2.2, 1.1, 0])
        self.at("which means nothing")
        self.play(Create(strike), FadeIn(note), run_time=0.8)
        self.finish()


class S06Order(SpokenScene):
    def construct(self):
        names, ris = names_of(ORDER_A)
        gene, cred, tag = statics()
        d = dyn(ORDER_A, 3)
        self.add(*names, *ris, gene, cred, tag)
        add_state(self, d, 3)
        x1 = LX0 + 9.6
        brace = Line([LX0, -1.75, 0], [x1, -1.75, 0], color=GREEN, stroke_width=6)
        tot = T("total isolation", 26, GREEN)
        totn = M("0.98", 30, GREEN)
        grp = VGroup(tot, totn).arrange(RIGHT, buff=0.25).move_to([(LX0 + x1) / 2, -1.45, 0])
        self.add(brace, grp)
        self.at("swap the first two")
        # swap the two chips and reset every result to neutral in the same animation
        d0 = dyn(ORDER_B, 0)
        d0["band"] = [R(XS[j], XS[j + 1], YB - H / 2, YB + H / 2, BLUE, 0.55, sw=1.5) for j in range(4)]
        self.play(names[0].animate.move_to([G[1], 3.0, 0]), names[1].animate.move_to([G[0], 3.0, 0]),
                  ris[0].animate.move_to([G[1], 2.2, 0]), ris[1].animate.move_to([G[0], 2.2, 0]),
                  FadeOut(brace), FadeOut(grp), *go(d, d0), run_time=1.3)
        self.at("pollinator barrier acts first")
        self.play(*go(d, dyn(ORDER_B, 1)), Indicate(names[1], color=ORANGE, scale_factor=1.12), run_time=1.1)
        self.at("gets only")
        self.play(*go(d, dyn(ORDER_B, 2)), Indicate(names[0], color=ORANGE, scale_factor=1.12), run_time=1.1)
        self.at("Hybrid fertility still")
        self.play(*go(d, dyn(ORDER_B, 3)), Indicate(names[2], color=ORANGE, scale_factor=1.12), run_time=1.1)
        brace2 = Line([LX0, -1.75, 0], [x1, -1.75, 0], color=GREEN, stroke_width=6)
        tot2 = VGroup(T("total isolation", 26, GREEN), M("0.98", 30, GREEN)).arrange(RIGHT, buff=0.25).move_to([(LX0 + x1) / 2, -1.45, 0])
        self.at("total is still")
        self.play(Create(brace2), FadeIn(tot2), run_time=0.9)
        self.at("position as well")
        self.play(Indicate(d["led"][0], color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Barriers act on what remains; order moves credit, not the total."
