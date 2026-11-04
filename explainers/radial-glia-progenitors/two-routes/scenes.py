"""Two Routes to a Neuron  (chapter 4 of the radial glia film series)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, shared by every chapter of this lesson; taken from scenes.old.py and chapter 1)
  BLUE   = the radial glial cell (body, fibre, foot); a radial glial daughter
  YELLOW = highlight / a tracking dot
  TEAL   = cell-cycle events (a dividing cell's ring), "proliferation"
  GREEN  = a neuron
  RED    = the open question, "?", a removed marker, the thing that fell
  GREY   = ventricle, pia, labels, a spent daughter, de-emphasised
  TEXT   = neutral white (headings, definitions)
  FLUID  = the ventricle's cerebrospinal fluid (a slate blue, kept apart from the cell blue)
  GOLD   = source tags; growth factors in the niche; the niche outline
  ORANGE = the intermediate progenitor and its marker Tbr2 (new here; ch2 uses ORANGE for dynein, not used in this chapter)
  PURPLE = outer radial glia (new here; ch2 uses PURPLE for kinesin, not used in this chapter)
  (the markers share their cell's colour: Pax6 blue, Tbr2 orange, Tbr1 green)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
FLUID = "#5B86B5"

NR = 0.62  # node radius in the lineage trees


# ---------------------------------------------------------------- helpers
def rect(x0, x1, y0, y1, color, op, stroke=0, stroke_op=1.0):
    r = Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=stroke, stroke_color=color,
                  fill_color=color, fill_opacity=op)
    if stroke:
        r.set_stroke(color, stroke, opacity=stroke_op)
    return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def circ(x, y, r, color=BLUE, op=0.35, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color,
                  fill_opacity=op).move_to([x, y, 0])


def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def lab(text, x, y, color=TEXT, size=22, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def lab_left(text, x, y, color=TEXT, size=22, **kw):
    t = T(text, size, color, **kw)
    return t.move_to([x + t.width / 2, y, 0])


def lab_right(text, x, y, color=TEXT, size=22, **kw):
    """Text whose right edge sits at x."""
    t = T(text, size, color, **kw)
    return t.move_to([x - t.width / 2, y, 0])


def dashed(mob, n=40):
    return DashedVMobject(mob, num_dashes=n)


def divcell(x, y, color, s=1.0):
    """A dividing cell: two daughter blobs inside a teal ring (a cartoon of mitosis)."""
    ring = Circle(radius=0.42 * s, stroke_color=TEAL, stroke_width=4).move_to([x, y, 0])
    return VGroup(ring, circ(x - 0.2 * s, y, 0.2 * s, color, 0.6), circ(x + 0.2 * s, y, 0.2 * s, color, 0.6))


def qnode(x, y, r=NR):
    c = Circle(radius=r, stroke_color=RED, stroke_width=4).move_to([x, y, 0])
    return VGroup(dashed(c, 18), T("?", 34, RED, weight=BOLD).move_to([x, y, 0]))


def strike(mob, color=RED, w=7):
    """A red cross over a mobject."""
    c = mob.get_center()
    hw, hh = mob.width / 2 + 0.12, mob.height / 2 + 0.12
    return VGroup(Line([c[0] - hw, c[1] + hh, 0], [c[0] + hw, c[1] - hh, 0], stroke_color=color, stroke_width=w),
                  Line([c[0] - hw, c[1] - hh, 0], [c[0] + hw, c[1] + hh, 0], stroke_color=color, stroke_width=w))


def marker_chip(name, color, size=30):
    return chip(name, color, size=size, pad=0.18)


class RGCell(VGroup):
    """The radial glial cell: apical foot, soma, long fibre, basal foot (a cartoon, no structure)."""

    def __init__(self, x=0.0, y0=-3.0, y1=3.3, ys=-2.3, k=1.0, color=BLUE, soma=True):
        sh = 0.9 * k
        afoot = Polygon([x - 0.32 * k, y0, 0], [x + 0.32 * k, y0, 0], [x + 0.12 * k, y0 + 0.3 * k, 0],
                        [x - 0.12 * k, y0 + 0.3 * k, 0], stroke_width=0, fill_color=color, fill_opacity=0.85)
        somam = RoundedRectangle(corner_radius=0.4 * k, width=1.15 * k, height=sh, stroke_color=color,
                                 stroke_width=3, fill_color=color, fill_opacity=0.35).move_to([x, ys, 0])
        top = ys + sh / 2
        fibre = Line([x, top, 0], [x, y1 - 0.3 * k, 0], stroke_color=color, stroke_width=8 * k)
        glow = Line([x, top, 0], [x, y1 - 0.3 * k, 0], stroke_color=color, stroke_width=24 * k, stroke_opacity=0.28)
        bfoot = Polygon([x - 0.12 * k, y1 - 0.3 * k, 0], [x + 0.12 * k, y1 - 0.3 * k, 0],
                        [x + 0.32 * k, y1, 0], [x - 0.32 * k, y1, 0], stroke_width=0,
                        fill_color=color, fill_opacity=0.85)
        parts = [glow, fibre, afoot, bfoot]
        gap_top, gap_bot = y0 + 0.3 * k, ys - sh / 2
        if gap_bot - gap_top > 0.02:  # a continuous cell: fibre from the apical foot up to the soma
            parts.insert(2, Line([x, gap_top, 0], [x, gap_bot, 0], stroke_color=color, stroke_width=8 * k))
        parts += ([somam] if soma else [])
        super().__init__(*parts)
        self.glow, self.fibre, self.soma, self.afoot, self.bfoot = glow, fibre, somam, afoot, bfoot


# ---------------------------------------------------------------- lineage trees
# Final layout (s03 end, s05, s14): direct tree at the left, indirect tree at the right.
def lpts(dx=0.0, dy=0.0):
    return dict(P=(-3.9 + dx, 1.5 + dy), R=(-5.7 + dx, -0.45 + dy), N=(-2.1 + dx, -0.45 + dy))


def rpts(dx=0.0, dy=0.0):
    return dict(P=(2.4 + dx, 1.5 + dy), R=(0.4 + dx, -0.45 + dy), I=(3.9 + dx, -0.45 + dy),
                N1=(2.7 + dx, -2.3 + dy), N2=(5.1 + dx, -2.3 + dy))


def nd(p, color, op=0.35, r=NR):
    return circ(p[0], p[1], r, color, op)


def edge(a, b, r=NR, color=GREY):
    a, b = np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0])
    d = (b - a) / np.linalg.norm(b - a)
    return arr(a + d * r, b - d * r, color)


def below(text, p, color, size=26):
    return lab(text, p[0], p[1] - NR - 0.32 - (0.15 if "\n" in text else 0), color, size, line_spacing=0.8)


def left_tree(dx=0.0, dy=0.0):
    p = lpts(dx, dy)
    d = {}
    d["head"] = T("direct", 34, TEXT, weight=BOLD).move_to([p["P"][0], p["P"][1] + 1.45, 0])
    d["pl"] = lab("radial glial cell", p["P"][0], p["P"][1] + NR + 0.27, BLUE)
    d["p"] = nd(p["P"], BLUE)
    d["e1"], d["e2"] = edge(p["P"], p["R"]), edge(p["P"], p["N"])
    d["r"], d["rl"] = nd(p["R"], BLUE), below("radial glial\ncell", p["R"], BLUE)
    d["n"], d["nl"] = nd(p["N"], GREEN, 0.85), below("neuron", p["N"], GREEN)
    return d


def right_tree(dx=0.0, dy=0.0, head=True):
    p = rpts(dx, dy)
    d = {}
    if head:
        d["head"] = T("indirect", 34, TEXT, weight=BOLD).move_to([p["P"][0], p["P"][1] + 1.45, 0])
    d["pl"] = lab("radial glial cell", p["P"][0], p["P"][1] + NR + 0.27, BLUE)
    d["p"] = nd(p["P"], BLUE)
    d["e1"], d["e2"] = edge(p["P"], p["R"]), edge(p["P"], p["I"])
    d["r"], d["rl"] = nd(p["R"], BLUE), below("radial glial\ncell", p["R"], BLUE)
    d["i"] = nd(p["I"], ORANGE)
    d["il"] = lab_left("intermediate\nprogenitor", p["I"][0] + NR + 0.12, p["I"][1], ORANGE, 26, line_spacing=0.8)
    d["e3"], d["e4"] = edge(p["I"], p["N1"]), edge(p["I"], p["N2"])
    d["n1"], d["n1l"] = nd(p["N1"], GREEN, 0.85), below("neuron", p["N1"], GREEN)
    d["n2"], d["n2l"] = nd(p["N2"], GREEN, 0.85), below("neuron", p["N2"], GREEN)
    return d


def group(d, keys=None):
    return VGroup(*[d[k] for k in (keys or d.keys())])


# ---------------------------------------------------------------- anatomy pieces
def mouse_icon(cx, cy, s=1.0):
    kw = dict(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
    body = Ellipse(width=2.6, height=1.6, **kw)
    head = Ellipse(width=1.3, height=1.1, **kw).shift([1.45, 0.1, 0])
    ear1 = Circle(radius=0.3, **kw).move_to([1.15, 0.7, 0])
    ear2 = Circle(radius=0.3, **kw).move_to([1.7, 0.66, 0])
    nose = Dot([2.1, 0.05, 0], radius=0.09, color=TEXT)
    eye = Dot([1.8, 0.2, 0], radius=0.07, color=TEXT)
    tail = ArcBetweenPoints([-1.3, -0.1, 0], [-2.9, 0.9, 0], angle=-1.2, stroke_color=GREY, stroke_width=5)
    return VGroup(tail, ear1, ear2, body, head, nose, eye).scale(s).move_to([cx, cy, 0])


def wall_bar(x0, x1, y, h=0.45, label=None, lx=None, size=26):
    band = rect(x0, x1, y - h / 2, y + h / 2, FLUID, 0.45)
    g = VGroup(band)
    if label:
        g.add(T(label, size, TEXT).move_to([lx if lx is not None else (x0 + x1) / 2, y, 0]))
    return g


def trail(points, color=YELLOW):
    p = VMobject(stroke_color=color)
    p.set_points_as_corners([[x, y, 0] for x, y in points])
    return p


def foot_poly(x, ybot, ytop, wb=0.64, wt=0.24, color=GREY, op=0.85):
    return Polygon([x - wb, ybot, 0], [x + wb, ybot, 0], [x + wt, ytop, 0], [x - wt, ytop, 0],
                   stroke_width=0, fill_color=color, fill_opacity=op)


def retract(foot, x, ytop):
    """Animation: an apical foot pulls back up into its cell."""
    return foot.animate.stretch(0.04, 1, about_point=np.array([x, ytop, 0]))


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "The Ventricular Zone: Radial Glia as Stem Cells"
    TITLE = "Two Routes to a Neuron"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), FadeIn(title), GrowFromCenter(rule),
                  run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(g), run_time=0.3)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        band = wall_bar(-6.6, 6.6, -3.45, 0.5, "ventricle", -5.2)
        cell = RGCell(x=-2.4, y0=-3.2, y1=3.4, ys=-2.1, k=1.6)
        self.add(band, cell)
        self.at("asymmetric division")
        left = circ(-2.4, -2.1, 0.62, BLUE, 0.35)
        right = circ(-2.4, -2.1, 0.62, BLUE, 0.35)
        self.play(ReplacementTransform(cell.soma, left), run_time=0.5)
        self.play(right.animate.move_to([-1.05, -2.1, 0]), run_time=0.7)
        self.at("keeps one daughter")
        rg = lab_right("radial glial cell", -3.3, -2.1, BLUE, 28)
        self.play(Indicate(left, color=BLUE, scale_factor=1.25), FadeIn(rg, shift=RIGHT * 0.2), run_time=0.9)
        box = dashed(RoundedRectangle(width=3.8, height=5.2, corner_radius=0.3, stroke_color=RED, stroke_width=4), 56)
        box.move_to([3.6, 0.2, 0])
        q = T("?", 190, RED, weight=BOLD).move_to([3.6, 0.15, 0])
        self.at("the other one")
        dq = qnode(-1.05, -2.1, 0.62)
        self.play(FadeOut(right), FadeIn(dq), run_time=0.4)
        self.play(Create(box), FadeIn(q, scale=0.6), GrowArrow(arr([-0.3, -1.8, 0], [1.6, -0.5, 0], RED, 5, 0.25)),
                  run_time=0.9)
        self.finish()


class S02Direct(SpokenScene):
    def construct(self):
        # carry-over: the s01 cell dissolves into the parent circle of the direct tree
        band = wall_bar(-6.6, 6.6, -3.45, 0.5, "ventricle", -5.2)
        cell = RGCell(x=-2.4, y0=-3.2, y1=3.4, ys=-2.1, k=1.6)
        self.add(band, cell)
        L = left_tree()
        Lgrp = group(L)
        Lgrp.scale(1.35).move_to([0, 0.15, 0])
        self.play(FadeOut(band), FadeOut(VGroup(cell.glow, cell.fibre, cell.afoot, cell.bfoot)),
                  ReplacementTransform(cell.soma, L["p"]), FadeIn(L["pl"]), run_time=0.9)
        self.at("direct neurogenesis")
        self.play(FadeIn(L["head"], shift=DOWN * 0.15), run_time=0.5)
        self.at("the radial glial cell")
        self.play(Indicate(L["p"], color=BLUE, scale_factor=1.25), run_time=0.7)
        self.at("divides into")
        self.play(GrowArrow(L["e1"]), GrowArrow(L["e2"]), run_time=0.7)
        self.at("another radial glial cell")
        self.play(FadeIn(L["r"], scale=0.5), FadeIn(L["rl"]), run_time=0.6)
        self.at("and a neuron")
        self.play(FadeIn(L["n"], scale=0.5), FadeIn(L["nl"]), run_time=0.6)
        self.finish()


class S03Indirect(SpokenScene):
    def construct(self):
        R = right_tree()
        Lg = group(left_tree())
        Lg.scale(1.35).move_to([0, 0.15, 0])
        Lt = group(left_tree())
        Lt.set_opacity(0.45)
        self.add(Lg)
        # same objects: the direct tree shrinks to its left slot, the indirect tree's parent appears
        self.play(Transform(Lg, Lt), FadeIn(R["p"], scale=0.5), FadeIn(R["pl"]),
                  FadeIn(R["head"], shift=DOWN * 0.15), run_time=0.7)
        self.at("second daughter")
        q = qnode(*rpts()["I"])
        self.play(GrowArrow(R["e1"]), GrowArrow(R["e2"]), FadeIn(R["r"], scale=0.5), FadeIn(R["rl"]),
                  FadeIn(q, scale=0.5), run_time=0.8)
        self.at("intermediate progenitor")
        self.play(ReplacementTransform(q, R["i"]), FadeIn(R["il"]), run_time=0.7)
        self.finish()


class S04Ip(SpokenScene):
    def construct(self):
        ventricle = wall_bar(-6.6, 6.6, -3.55, 0.5, "ventricle", -5.2)
        svz_band = rect(-6.6, 6.6, -0.9, 2.9, GREY, 0.14)
        rgx = -4.9
        rg = RGCell(x=rgx, y0=-3.3, y1=3.4, ys=-2.35, k=1.9)
        rg_label = lab_left("radial glial cell", rgx + 1.3, -2.35, BLUE, 28)
        ipx, ip_y0 = 0.0, -1.6
        ip = circ(ipx, ip_y0, 1.1, ORANGE, 0.4)
        foot = foot_poly(ipx, -3.3, ip_y0 - 0.65, 0.85, 0.3, ORANGE)
        foot_lab = lab_left("apical foot on the ventricle", ipx + 1.0, -2.85, TEXT, 24)
        ip_label = lab_left("intermediate\nprogenitor", ipx + 1.4, ip_y0 + 0.2, ORANGE, 28, line_spacing=0.8)
        self.add(svz_band, ventricle, rg, rg_label, foot, ip, ip_label, foot_lab)
        self.at("lets go of the ventricle")
        self.play(Indicate(foot, color=YELLOW, scale_factor=1.15), run_time=0.5)
        self.play(retract(foot, ipx, ip_y0 - 0.65), run_time=1.6)
        self.play(FadeOut(foot), FadeOut(foot_lab), run_time=0.15)
        self.at("moves into the")
        svl = lab_right("subventricular zone", 6.6, 2.65, GREY, 28)
        self.play(ip.animate.move_to([ipx, 1.0, 0]), ip_label.animate.move_to(
            [ip_label.get_center()[0], 1.2, 0]), run_time=1.5)
        self.play(FadeIn(svl), run_time=0.4)
        self.at("There it divides once more")
        ring = Circle(radius=1.35, stroke_color=TEAL, stroke_width=4).move_to([ipx, 1.0, 0])
        d1, d2 = circ(ipx - 0.55, 1.0, 0.7, ORANGE, 0.4), circ(ipx + 0.55, 1.0, 0.7, ORANGE, 0.4)
        self.play(FadeIn(ring), FadeOut(ip_label), ReplacementTransform(ip, VGroup(d1, d2)), run_time=0.7)
        self.at("rodent cortex")
        tag = lab("in rodent cortex", ipx, 2.65, GOLD, 28)
        self.play(FadeIn(tag), run_time=0.5)
        self.at("into two neurons")
        n1, n2 = circ(ipx - 2.1, 1.0, 0.8, GREEN, 0.85), circ(ipx + 2.1, 1.0, 0.8, GREEN, 0.85)
        self.play(FadeOut(ring), ReplacementTransform(d1, n1), ReplacementTransform(d2, n2), run_time=0.9)
        l1, l2 = lab("neuron", ipx - 2.1, -0.15, GREEN, 28), lab("neuron", ipx + 2.1, -0.15, GREEN, 28)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        self.finish()


class S05Noctor(SpokenScene):
    def construct(self):
        L, R = left_tree(), right_tree()
        self.add(group(L), group(R))
        self.at("filming rat slices")
        tag = lab("rat, embryonic day 16 to 19  |  Noctor and colleagues, 2004", 0, -3.7, GOLD, 28)
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.7)
        self.at("tracked both routes")
        pl, pr = lpts(), rpts()
        dot1, dot2 = Dot(radius=0.15, color=YELLOW).move_to([*pl["P"], 0]), Dot(radius=0.15, color=YELLOW).move_to([*pr["P"], 0])
        p1 = trail([pl["P"], pl["N"]])
        p2 = trail([pr["P"], pr["I"], pr["N1"]])
        self.add(dot1, dot2)
        self.play(MoveAlongPath(dot1, p1), MoveAlongPath(dot2, p2), run_time=1.6, rate_func=linear)
        self.play(FadeOut(dot1), FadeOut(dot2), run_time=0.3)
        self.at("most radial glial divisions")
        mark = T("most radial glial divisions: asymmetric (about 79 percent)", 26, TEXT).move_to([0, 3.55, 0])
        self.play(FadeIn(mark, shift=DOWN * 0.15), Indicate(VGroup(L["e1"], L["e2"]), color=YELLOW),
                  Indicate(VGroup(R["e1"], R["e2"]), color=YELLOW), run_time=1.0)
        self.finish()


class S06Nine(SpokenScene):
    def construct(self):
        head = T("about 9 in 10", 54, TEXT, weight=BOLD).move_to([0, 3.2, 0])
        sub = lab("of intermediate progenitor divisions gave two neurons", 0, 2.45, ORANGE, 30)
        xs, ys = [-4.8, -2.4, 0, 2.4, 4.8], [0.85, -1.3]
        tiles, tops, kids = [], [], []
        for k in range(10):
            x, y = xs[k % 5], ys[k // 5]
            box = RoundedRectangle(corner_radius=0.15, width=2.2, height=2.0, stroke_color=GREY, stroke_width=2.5,
                                   fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0])
            top = circ(x, y + 0.55, 0.3, ORANGE, 0.5)
            tiles.append(box)
            tops.append(top)
            if k < 9:
                n1, n2 = circ(x - 0.5, y - 0.5, 0.27, GREEN, 0.85), circ(x + 0.5, y - 0.5, 0.27, GREEN, 0.85)
                e1 = Line([x - 0.14, y + 0.28, 0], [x - 0.42, y - 0.24, 0], stroke_color=GREY, stroke_width=3)
                e2 = Line([x + 0.14, y + 0.28, 0], [x + 0.42, y - 0.24, 0], stroke_color=GREY, stroke_width=3)
                kids.append(VGroup(e1, e2, n1, n2))
        note = lab("illustration: one box = one division", 0, -2.85, GREY, 28)
        self.at("about nine in ten")
        self.play(FadeIn(head, shift=DOWN * 0.15),
                  LaggedStart(*[FadeIn(VGroup(tiles[k], tops[k]), scale=0.8) for k in range(10)], lag_ratio=0.06),
                  FadeIn(note), run_time=1.2)
        self.at("intermediate progenitor divisions")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.6)
        self.at("gave two neurons")
        self.play(LaggedStart(*[FadeIn(k) for k in kids], lag_ratio=0.12), run_time=1.3)
        self.at("but only 19")
        boxes = VGroup(*tiles, *tops, *kids)
        dots = VGroup(*[circ(-4.95 + 0.55 * i, -1.0, 0.2, ORANGE, 0.6, 2) for i in range(19)])
        n19 = lab("19 divisions seen away from the ventricle", 0, -1.85, TEXT, 32)
        self.play(boxes.animate.scale(0.75).move_to([0, 1.45, 0]).set_opacity(0.45), FadeOut(head), FadeOut(sub), FadeOut(note),
                  LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.04), FadeIn(n19), run_time=1.5)
        self.at("read it as rat")
        rat = chip("so read it as rat", GOLD, size=40)
        rat.move_to([0, -3.05, 0])
        self.play(FadeIn(rat, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S07Mouse(SpokenScene):
    def construct(self):
        m = mouse_icon(-3.9, 2.55, 0.85)
        ml = lab_left("mouse", -1.0, 2.55, TEXT, 40, weight=BOLD)
        cy = -0.5
        ip = circ(-4.6, cy, 0.9, ORANGE, 0.4)
        ipl = lab("intermediate\nprogenitors", -4.6, cy - 1.75, ORANGE, 28, line_spacing=0.8)
        ar = DashedLine([-3.5, cy, 0], [-0.9, cy, 0], stroke_color=ORANGE, stroke_width=6)
        ar.add_tip(tip_length=0.3)
        may = lab("may make", -2.2, cy + 0.5, TEXT, 30)
        fan = []
        for r, cnt, op in [(1.5, 3, 0.9), (2.7, 5, 0.75), (3.9, 7, 0.55)]:
            for a in np.linspace(-28, 28, cnt):
                fan.append(circ(0.2 + r * np.cos(np.radians(a)), cy + r * np.sin(np.radians(a)) * 0.95, 0.3, GREEN, op, 2))
        pile = VGroup(*fan)
        pl = lab("most cortical projection neurons", 2.9, -3.0, GREEN, 30)
        ps = lab("(projection neurons send long axons)", 2.9, -3.5, GREY, 26)
        self.at("in mouse")
        self.play(FadeIn(m, shift=DOWN * 0.15), FadeIn(ml), run_time=0.7)
        self.at("intermediate progenitors")
        self.play(FadeIn(ip, scale=0.5), FadeIn(ipl), run_time=0.6)
        self.at("may make")
        self.play(Create(ar), FadeIn(may), run_time=0.7)
        self.at("most cortical projection neurons")
        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in pile], lag_ratio=0.03), FadeIn(pl), run_time=1.2)
        self.play(FadeIn(ps), run_time=0.4)
        self.finish()


COLX = -1.6


def col_cells(big=True):
    """The three steps of the indirect route, one above the other: ventricle at the bottom, outward is up."""
    if big:
        ys, cx, r, nsz, csz, off = [-2.35, -0.2, 1.95], -0.5, 0.76, 38, 46, 3.5
    else:
        ys, cx, r, nsz, csz, off = [-2.65, -0.75, 1.15], COLX, 0.6, 28, 34, 2.7
    cols, names = [BLUE, ORANGE, GREEN], ["radial glia", "intermediate\nprogenitor", "young neuron"]
    cells = [circ(cx, y, r, c, 0.4 if c != GREEN else 0.85) for y, c in zip(ys, cols)]
    nms = [lab_right(n, cx - r - 0.25, y, c, nsz, line_spacing=0.8) for n, y, c in zip(names, ys, cols)]
    arrows = [arr([cx, ys[0] + r + 0.05, 0], [cx, ys[1] - r - 0.05, 0]), arr([cx, ys[1] + r + 0.05, 0], [cx, ys[2] - r - 0.05, 0])]
    band = wall_bar(-6.0, 3.0, -3.55, 0.45, "ventricle", -4.9) if not big else wall_bar(-6.4, 5.4, -3.5, 0.45, "ventricle", -5.2)
    chips = [marker_chip(n, c, csz).move_to([cx + off, y, 0]) for n, c, y in zip(["Pax6", "Tbr2", "Tbr1"], cols, ys)]
    return cells, nms, arrows, band, chips


def tf_card():
    box = RoundedRectangle(corner_radius=0.2, width=8.2, height=1.3, stroke_color=TEXT, stroke_width=3,
                           fill_color=BG, fill_opacity=0.95).move_to([0.0, 3.1, 0])
    t1 = T("transcription factors:", 30, TEXT, weight=BOLD)
    t2 = T("proteins that switch genes on or off", 30, TEXT)
    g = VGroup(t1, t2).arrange(DOWN, buff=0.15).move_to(box)
    return VGroup(box, g).scale(0.64).move_to([0.0, 3.4, 0])


class S08Markers(SpokenScene):
    def construct(self):
        cells, nms, arrows, band, chips = col_cells()
        card = tf_card()
        self.at("transcription factors")
        self.play(FadeIn(card, scale=0.9), run_time=0.7)
        self.at("mark the steps")
        self.play(FadeIn(band), FadeIn(cells[0], scale=0.5), run_time=0.4)
        self.play(GrowArrow(arrows[0]), FadeIn(cells[1], scale=0.5), run_time=0.5)
        self.play(GrowArrow(arrows[1]), FadeIn(cells[2], scale=0.5), run_time=0.5)
        self.at("marks radial glia")
        self.play(FadeIn(chips[0], scale=0.6), FadeIn(nms[0]), run_time=0.6)
        self.at("marks intermediate", lead=0.9)
        self.play(FadeIn(chips[1], scale=0.6), FadeIn(nms[1]), run_time=0.6)
        self.at("marks young neurons", lead=0.9)
        self.play(FadeIn(chips[2], scale=0.6), FadeIn(nms[2]), run_time=0.6)
        self.finish()


class S09Order(SpokenScene):
    def construct(self):
        cells, nms, arrows, band, chips = col_cells()
        card = tf_card()
        self.add(card, band, *cells, *arrows, *nms, *chips)
        self.at("appear in that order", lead=0.2)
        for c, ce in zip(chips, cells):
            ring = SurroundingRectangle(c, color=YELLOW, buff=0.12, stroke_width=6, corner_radius=0.1)
            self.play(FadeIn(ring), Indicate(c, color=YELLOW, scale_factor=1.3), Indicate(ce, color=YELLOW, scale_factor=1.25),
                      run_time=0.7)
            self.play(FadeOut(ring), run_time=0.15)
        self.at("move outward", lead=0.3)
        up = arr([5.2, -2.9, 0], [5.2, 2.2, 0], TEXT, 8, 0.35)
        out = T("outward", 34, TEXT).rotate(PI / 2).move_to([5.9, -0.4, 0])
        self.play(GrowArrow(up), FadeIn(out), run_time=0.9)
        self.finish()


class S10Labels(SpokenScene):
    def construct(self):
        cells, nms, arrows, band, chips = col_cells(big=False)
        self.add(band, *cells, *arrows, *nms, *chips)
        self.at("only labels")
        ql = lab_left("only labels?", 2.0, -0.75, RED, 42, weight=BOLD)
        self.play(FadeIn(ql, shift=LEFT * 0.2), Indicate(VGroup(*chips), color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.at("in 2008")
        yr = lab_left("2008", 2.4, 2.7, GOLD, 48, weight=BOLD)
        self.play(FadeIn(yr), run_time=0.5)
        self.at("two groups")
        a = lab_left("Arnold and colleagues", 2.4, 1.95, GOLD, 28)
        b = lab_left("Sessa and colleagues", 2.4, 1.4, GOLD, 28)
        self.play(FadeIn(a, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(b, shift=LEFT * 0.2), run_time=0.5)
        self.at("removed", lead=-0.2)
        x = strike(chips[1])
        rem = lab_left("Tbr2 removed", 2.0, -0.75, RED, 38, weight=BOLD)
        self.play(Create(x), FadeOut(ql), FadeIn(rem), chips[1].animate.set_opacity(0.55), run_time=0.7)
        self.at("developing mouse brain")
        mb = lab_right("in the developing mouse brain", 6.4, -1.9, TEXT, 28)
        self.play(FadeIn(mb), run_time=0.5)
        self.finish()


# ---- the counters (s11, s12, s13)
PW, PH, PY = 4.3, 5.3, -0.6
SLOT = 2.4          # x of the two panels in s11 and s12
Q_IFF = (0, 3.45)
Q_WHICH = (0, 2.75)


def make_panel(cx, kind):
    """kind 'v' = mitoses at the ventricle, 'a' = away from it. Returns dict of parts."""
    d = {}
    d["box"] = RoundedRectangle(corner_radius=0.2, width=PW, height=PH, stroke_color=GREY, stroke_width=3,
                                stroke_opacity=0.6).move_to([cx, PY, 0])
    title = "mitoses at\nthe ventricle" if kind == "v" else "mitoses away\nfrom it"
    d["title"] = T(title, 28, TEXT, weight=BOLD, line_spacing=0.8).move_to([cx, 1.45, 0])
    d["bar"] = rect(cx - 1.9, cx + 1.9, -2.9, -2.55, FLUID, 0.5)
    d["vl"] = lab("ventricle", cx, -3.07, GREY, 24)
    cy = -1.75 if kind == "v" else -0.85
    col = BLUE if kind == "v" else ORANGE
    d["cells"] = [divcell(cx + dx, cy, col, 1.25) for dx in (-1.2, 0, 1.2)]
    d["q"] = T("?", 70, RED, weight=BOLD).move_to([cx, 0.35, 0])
    d["cx"] = cx
    return d


def panel_parts(d, with_box=True):
    return VGroup(*(([d["box"]] if with_box else []) + [d["title"], d["bar"], d["vl"], *d["cells"], d["q"]]))


def question_lines():
    iff = lab("If Tbr2 is a step in the indirect route,", *Q_IFF, TEXT, 30)
    q = lab("which count should fall?", *Q_WHICH, RED, 40, weight=BOLD)
    return iff, q


class S11Predict(SpokenScene):
    def construct(self):
        PL, PR = make_panel(-SLOT, "v"), make_panel(SLOT, "a")
        cm = lab("count the mitoses", 0, 3.3, TEXT, 38, weight=BOLD)
        self.play(FadeIn(PL["box"]), FadeIn(PR["box"]), FadeIn(cm, shift=DOWN * 0.15), run_time=0.5)
        self.at("at the ventricle")
        self.play(FadeIn(panel_parts(PL, False), shift=RIGHT * 0.3), run_time=0.8)
        self.at("away from it")
        self.play(FadeIn(panel_parts(PR, False), shift=LEFT * 0.3), run_time=0.8)
        iff, q = question_lines()
        self.at("if tb")
        self.play(FadeOut(cm), FadeIn(iff, shift=DOWN * 0.15), run_time=0.6)
        self.at("which count should fall")
        self.play(FadeIn(q, shift=UP * 0.15), Indicate(PL["q"], color=RED), Indicate(PR["q"], color=RED), run_time=0.8)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        PL, PR = make_panel(-SLOT, "v"), make_panel(SLOT, "a")
        iff, q = question_lines()
        self.add(panel_parts(PL), panel_parts(PR), iff, q)
        pl = lab_left("pause and predict", -6.5, -3.52, YELLOW, 30, weight=BOLD)
        track = rect(-2.4, 6.3, -3.66, -3.38, GREY, 0.2)
        fill = rect(-2.4, 6.3, -3.66, -3.38, YELLOW, 0.9)
        self.add(pl, track)
        self.play(GrowFromEdge(fill, LEFT), run_time=self.beat(0.93), rate_func=linear)
        self.finish()


class S13Rev(SpokenScene):
    def construct(self):
        PL, PR = make_panel(-SLOT, "v"), make_panel(SLOT, "a")
        iff, q = question_lines()
        self.add(panel_parts(PL), panel_parts(PR), iff, q)
        self.at("ventricle went on")
        went = T("went on", 46, TEXT, weight=BOLD).move_to(PL["q"])
        self.play(FadeOut(iff), FadeOut(q), ReplacementTransform(PL["q"], went),
                  *[Indicate(c, color=YELLOW, scale_factor=1.12) for c in PL["cells"]], run_time=0.9)
        self.at("from it fell")
        fell = T("fell", 50, RED, weight=BOLD).move_to(PR["q"])
        self.play(ReplacementTransform(PR["q"], fell), PR["cells"][1].animate.set_opacity(0.15),
                  PR["cells"][2].animate.set_opacity(0.15), run_time=0.9)
        # third panel: fewer neurons, at readable size; the two counters slide over to make room
        self.at("fewer cortical neurons")
        left_g = VGroup(PL["box"], PL["title"], PL["bar"], PL["vl"], *PL["cells"], went)
        right_g = VGroup(PR["box"], PR["title"], PR["bar"], PR["vl"], *PR["cells"], fell)
        cx3 = 4.65
        box3 = RoundedRectangle(corner_radius=0.2, width=PW, height=PH, stroke_color=GREEN, stroke_width=3,
                                stroke_opacity=0.8).move_to([cx3, PY, 0])
        t3 = T("cortical\nneurons made", 28, TEXT, weight=BOLD, line_spacing=0.8).move_to([cx3, 1.45, 0])
        slots = []
        for i in range(8):
            x, y = cx3 - 1.2 + 0.8 * (i % 4), 0.3 - 1.05 * (i // 4)
            slots.append((x, y))
        solid = VGroup(*[circ(x, y, 0.33, GREEN, 0.85, 2) for x, y in slots[:5]])
        ghosts = VGroup(*[dashed(Circle(radius=0.33, stroke_color=GREY, stroke_width=3), 14).move_to([x, y, 0])
                          for x, y in slots[5:]])
        few = T("fewer", 46, GREEN, weight=BOLD).move_to([cx3, -2.2, 0])
        self.play(left_g.animate.shift([-2.25, 0, 0]), right_g.animate.shift([-SLOT, 0, 0]), run_time=0.6)
        self.play(FadeIn(box3), FadeIn(t3), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in solid], lag_ratio=0.1), FadeIn(ghosts), FadeIn(few),
                  run_time=1.0)
        self.finish()


class S14Pos(SpokenScene):
    def construct(self):
        # part 1: two clues point to the lost progenitor
        tl = lab("position of mitosis", -3.4, 3.3, TEXT, 32, weight=BOLD)
        bar = wall_bar(-6.0, -0.8, 0.3, 0.45, "ventricle", -3.4)
        cell = divcell(-3.4, 2.1, ORANGE, 1.5)
        left = VGroup(tl, bar, cell)
        self.at("position of mitosis")
        self.play(FadeIn(left, shift=RIGHT * 0.2), run_time=0.8)
        tr = lab("markers", 3.4, 3.3, TEXT, 32, weight=BOLD)
        ch = marker_chip("Tbr2", ORANGE, 48).move_to([3.4, 1.9, 0])
        right = VGroup(tr, ch)
        self.at("with the markers")
        self.play(FadeIn(right, shift=LEFT * 0.2), run_time=0.8)
        self.at("pointed to the lost progenitor")
        lost = qnode(0, -2.0, 0.8)
        lost[0].set_color(ORANGE)
        lt = lab("the lost progenitor", 0, -3.2, ORANGE, 34)
        a1 = arr([-3.4, -0.2, 0], [-0.7, -1.5, 0], TEXT, 5, 0.25)
        a2 = arr([3.4, 1.2, 0], [0.7, -1.4, 0], TEXT, 5, 0.25)
        self.play(FadeIn(a1), FadeIn(a2), run_time=0.6)
        self.play(FadeIn(lost, scale=0.5), FadeIn(lt), run_time=0.6)
        # part 2: the 2008 mutants
        self.at("in those mice")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        T_ = right_tree(dx=-4.9, dy=-0.1, head=False)
        pp = rpts(-4.9, -0.1)
        tree = group(T_)
        self.play(FadeIn(tree, shift=UP * 0.1), run_time=0.8)
        chp = marker_chip("Tbr2", ORANGE, 46).move_to([4.9, 2.6, 0])
        l1 = lab("In the 2008 mutants,", 4.9, 1.45, GOLD, 30)
        self.play(FadeIn(chp, scale=0.6), FadeIn(l1), run_time=0.5)
        self.at("was needed")
        x = strike(chp)
        low = VGroup(T_["e3"], T_["e4"], T_["n1"], T_["n2"], T_["n1l"], T_["n2l"])
        self.play(Create(x), low.animate.set_opacity(0.2), run_time=0.7)
        self.at("indirect route")
        fin = lab("Tbr2 was needed for\nthe indirect route", 4.9, 0.5, TEXT, 30, line_spacing=0.85)
        self.play(FadeIn(fin, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S15Orgs(SpokenScene):
    def construct(self):
        # primate wall (thick) at the left, mouse wall (thin) at the right, same width, bottoms level
        wa = rect(-6.7, -0.2, -3.25, 2.4, GREY, 0.12, stroke=3, stroke_op=0.6)
        ba = wall_bar(-6.7, -0.2, -3.45, 0.4, "ventricle", -5.3)
        la = lab("primate (human)", -3.45, 3.4, TEXT, 32, weight=BOLD)
        wb = rect(0.2, 6.7, -3.25, 2.4, GREY, 0.12, stroke=3, stroke_op=0.6)
        bb = wall_bar(0.2, 6.7, -3.45, 0.4, "ventricle", 1.6)
        lb = lab("mouse", 3.45, 3.4, TEXT, 32, weight=BOLD)
        sch = lab("schematic", 3.45, 1.9, GREY, 26)
        pos = [(-5.2, 1.7), (-4.0, 0.7), (-3.3, 1.7), (-2.3, 0.9), (-1.2, 1.8), (-0.8, 0.5), (-4.6, 0.2),
               (-2.9, 0.2), (-1.6, 1.0), (-3.8, 1.2), (-2.2, 1.7), (-0.6, 1.2)]
        cellsA = VGroup(*[circ(x, y, 0.3, PURPLE, 0.55, 3) for x, y in pos])
        cellsB = VGroup(circ(2.4, -1.3, 0.3, PURPLE, 0.55, 3), circ(4.6, -1.0, 0.3, PURPLE, 0.55, 3))
        self.add(wa, ba, wb, bb)
        self.at("primates have")
        self.play(FadeIn(la, shift=DOWN * 0.1), FadeIn(lb), FadeIn(sch), run_time=0.5)
        self.at("third progenitor")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cellsA], lag_ratio=0.08), run_time=1.5)
        pn = lab("a third progenitor", -3.45, 2.85, PURPLE, 28)
        pn_ptr = arr([-3.45, 2.65, 0], [-3.35, 2.0, 0], PURPLE, 3, 0.15)
        self.play(FadeIn(pn), FadeIn(pn_ptr), run_time=0.4)
        self.at("outer radial glia")
        self.play(Transform(pn, lab("outer radial glia", -3.45, 2.85, PURPLE, 28)), run_time=0.5)
        self.at("divide far from the ventricle")
        rings = VGroup(*[Circle(radius=0.45, stroke_color=TEAL, stroke_width=4).move_to([*pos[i], 0]) for i in (1, 3, 8)])
        far = DoubleArrow([-6.2, -3.0, 0], [-6.2, 0.0, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.22)
        fl = lab_left("far from the\nventricle", -5.95, -1.6, TEXT, 26, line_spacing=0.8)
        self.play(FadeIn(rings), FadeIn(far), FadeIn(fl), run_time=1.0)
        self.at("mouse has a few")
        self.play(FadeIn(cellsB, scale=0.4), run_time=0.6)
        self.play(Indicate(cellsB, color=PURPLE, scale_factor=1.25), run_time=0.7)
        self.at("humans have far more")
        self.play(FadeOut(rings), Indicate(cellsA, color=PURPLE, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---- the niche (s16 to s20)
CX = -1.2    # x of the radial glial cell in the niche scenes
KN = 2.0     # the cell is drawn thick here so it fills the frame
YS = -1.3    # soma height
Y0 = -2.7    # top of the cerebrospinal fluid band


def niche_stage():
    band = rect(-6.6, 6.6, -3.8, Y0, FLUID, 0.45)
    vl = T("ventricle", 26, TEXT).move_to([-5.4, -3.25, 0])
    pia = rect(-6.6, 6.6, 3.45, 3.6, GREY, 0.75)
    bm = Line([-6.6, 3.3, 0], [6.6, 3.3, 0], stroke_color=GREY, stroke_width=2)
    return band, vl, pia, bm


DOT_KEY = [(-0.3, -3.1), (-1.2, -3.2), (-2.1, -3.1), (3.0, -3.2)]


def niche_dots(n=16, seed=4):
    rs = np.random.RandomState(seed)
    pts = list(DOT_KEY) + [(rs.uniform(-3.9, 3.3), rs.uniform(-3.65, -2.95)) for _ in range(n - len(DOT_KEY))]
    return VGroup(*[Dot([x, y, 0], radius=0.15, color=GOLD) for x, y in pts])


def niche_cell(soma=True, y1=3.3):
    return RGCell(x=CX, y0=Y0, y1=y1, ys=YS, k=KN, soma=soma)


class S16Niche(SpokenScene):
    def construct(self):
        band, vl, pia, bm = niche_stage()
        cell = niche_cell()
        self.add(band, vl, pia, bm)
        self.play(FadeIn(cell, shift=UP * 0.3), run_time=0.6)
        self.at("give up")
        dau = circ(CX + 2.0, YS, 0.8, GREY, 0.25)
        dfoot = foot_poly(CX + 2.0, Y0, Y0 + 0.6, 0.64, 0.24, GREY, 0.6)
        gu = lab_left("give up?", CX + 3.0, YS, RED, 48, weight=BOLD)
        self.play(FadeIn(dau), FadeIn(dfoot), FadeIn(gu, shift=RIGHT * 0.2), run_time=0.7)
        self.at("a niche")
        box = dashed(RoundedRectangle(width=3.8, height=7.3, corner_radius=0.35, stroke_color=GOLD, stroke_width=4), 60)
        box.move_to([CX, -0.05, 0])
        nl = lab_left("niche", 1.0, 1.7, GOLD, 60, weight=BOLD)
        self.play(FadeIn(box), FadeOut(gu), FadeOut(dau), FadeOut(dfoot), FadeIn(nl), run_time=0.9)
        self.at("local setting")
        ls = lab_left("the local setting", 1.0, 0.6, TEXT, 34)
        self.play(FadeIn(ls, shift=UP * 0.1), run_time=0.5)
        self.at("keeps a stem cell a stem cell")
        ks = lab_left("that keeps a stem cell\na stem cell", 1.0, -0.55, TEXT, 34, line_spacing=0.85)
        self.play(FadeIn(ks, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S17Csf(SpokenScene):
    def construct(self):
        band, vl, pia, bm = niche_stage()
        cell = niche_cell()
        dots = niche_dots()
        self.add(band, vl, pia, bm, cell)
        self.at("apical foot")
        af = lab_right("apical foot", CX - 1.45, -1.95, BLUE, 30)
        pt = arr([CX - 1.4, -2.05, 0], [CX - 0.55, -2.45, 0], BLUE, 3, 0.15)
        self.play(Indicate(cell.afoot, color=YELLOW, scale_factor=1.4), FadeIn(af), FadeIn(pt), run_time=0.8)
        self.at("cerebrospinal fluid")
        cf = lab("cerebrospinal fluid", 5.1, -3.25, TEXT, 26)
        self.play(FadeIn(cf), run_time=0.5)
        self.at("in mouse")
        mouse_tag = chip("mouse", GREY, size=34).move_to([5.5, 2.3, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.05), FadeIn(mouse_tag), run_time=0.9)
        self.at("growth factors")
        gl = lab_left("growth factors", 0.6, -1.95, GOLD, 30)
        lead = arr([0.9, -2.2, 0], [-0.1, -2.95, 0], GOLD, 3, 0.15)
        flow = VGroup(arr([-0.3, -3.0, 0], [-0.8, -2.45, 0], GOLD, 4, 0.18),
                      arr([-1.2, -3.05, 0], [-1.2, -2.5, 0], GOLD, 4, 0.18),
                      arr([-2.1, -3.0, 0], [-1.65, -2.45, 0], GOLD, 4, 0.18))
        self.play(FadeIn(gl), FadeIn(lead), LaggedStart(*[FadeIn(a) for a in flow], lag_ratio=0.2), run_time=0.8)
        self.at("igf", lead=0.1)
        igf = marker_chip("including IGF2", GOLD, 32).move_to([4.0, -0.9, 0])
        ptr = arr([3.6, -1.3, 0], [3.05, -3.0, 0], GOLD, 3, 0.15)
        self.play(FadeIn(igf, scale=0.6), FadeIn(ptr), Indicate(dots[3], color=YELLOW, scale_factor=2.0), run_time=0.6)
        self.at("support proliferation")
        sp = lab_left("support proliferation", 0.6, 0.5, TEAL, 32)
        spa = arr([1.0, 0.2, 0], [CX + 1.15, YS + 0.3, 0], TEAL, 4, 0.2)
        self.play(FadeIn(sp), FadeIn(spa), Indicate(cell.soma, color=TEAL, scale_factor=1.12), run_time=0.8)
        self.finish()


class S18Bm(SpokenScene):
    def construct(self):
        band, vl, pia, bm = niche_stage()
        cell = niche_cell()
        dots = niche_dots().set_opacity(0.45)
        self.add(band, vl, pia, bm, cell, dots)
        self.at("basal foot")
        bf = lab_left("basal foot", 0.2, 1.0, BLUE, 34, weight=BOLD)
        bfp = arr([0.15, 1.25, 0], [CX + 0.5, 2.95, 0], BLUE, 5, 0.2)
        self.play(Indicate(cell.bfoot, color=YELLOW, scale_factor=1.5), FadeIn(bf), FadeIn(bfp), run_time=0.8)
        self.at("basement membrane")
        bml = lab_right("basement membrane", 6.5, 2.2, TEXT, 34, weight=BOLD)
        bmp = arr([5.0, 2.55, 0], [5.0, 3.25, 0], TEXT, 6, 0.22)
        self.play(Indicate(bm, color=YELLOW), FadeIn(bml), FadeIn(bmp), run_time=0.8)
        self.at("under the pia")
        pl = lab("pia", -5.6, 2.2, TEXT, 34, weight=BOLD)
        pp = arr([-5.6, 2.55, 0], [-5.6, 3.4, 0], TEXT, 6, 0.22)
        self.play(Indicate(pia, color=YELLOW), FadeIn(pl), FadeIn(pp), run_time=0.7)
        self.at("neighboring cells")
        nb = VGroup(RGCell(x=CX - 2.6, y0=Y0, y1=3.3, ys=YS, k=1.3), RGCell(x=CX + 2.6, y0=Y0, y1=3.3, ys=YS, k=1.3))
        nb.set_opacity(0.5)
        self.play(FadeOut(bf), FadeOut(bfp), FadeIn(nb), run_time=0.8)
        self.at("through notch")

        def contact(xa, xb, y):
            xm = (xa + xb) / 2
            return VGroup(Line([xa, y, 0], [xb, y, 0], stroke_color=TEXT, stroke_width=5),
                          Line([xa, y - 0.3, 0], [xa, y + 0.3, 0], stroke_color=TEXT, stroke_width=6),
                          Line([xb, y - 0.3, 0], [xb, y + 0.3, 0], stroke_color=TEXT, stroke_width=6),
                          Line([xm, y + 0.4, 0], [xm, y + 0.9, 0], stroke_color=TEXT, stroke_width=3),
                          lab("Notch", xm, y + 1.25, TEXT, 30, weight=BOLD))
        c1 = contact(CX + 1.15, CX + 2.6 - 0.75, YS)
        c2 = contact(CX - 2.6 + 0.75, CX - 1.15, YS)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.7)
        self.at("part of the setting")
        box = dashed(RoundedRectangle(width=7.6, height=7.3, corner_radius=0.35, stroke_color=GOLD, stroke_width=4), 90)
        box.move_to([CX - 0.1, -0.05, 0])
        self.play(FadeIn(box), run_time=0.9)
        self.finish()


def stage_with_dots():
    band, vl, pia, bm = niche_stage()
    return band, vl, pia, bm, niche_dots()


LX = CX + 2.0   # x of the leaving daughter before it goes
LR = 0.8        # radius of the two daughters
LEAVE_END = (CX + 3.4, 0.8)


class S19Leave(SpokenScene):
    def construct(self):
        band, vl, pia, bm, dots = stage_with_dots()
        cell = niche_cell()
        self.add(band, vl, pia, bm, cell, dots)
        self.at("asymmetric division")
        stay = circ(CX, YS, LR, BLUE, 0.35)
        leave = circ(CX, YS, LR, GREY, 0.3)
        lfoot = foot_poly(LX, Y0, Y0 + 0.6, 0.64, 0.24, GREY, 0.85)
        self.play(ReplacementTransform(cell.soma, stay), run_time=0.5)
        self.play(leave.animate.move_to([LX, YS, 0]), FadeIn(lfoot), run_time=0.7)
        self.at("the daughter that leaves")
        lt = lab_left("the daughter that leaves", LX + 1.1, YS, GREY, 30)
        self.play(Indicate(leave, color=TEXT, scale_factor=1.2), FadeIn(lt), run_time=0.9)
        self.at("lets go of the apical surface")
        self.play(retract(lfoot, LX, Y0 + 0.6), FadeOut(lt), run_time=1.2)
        self.play(FadeOut(lfoot), leave.animate.move_to([*LEAVE_END, 0]), run_time=1.7)
        self.at("fluid side of the niche")
        hl = SurroundingRectangle(band, color=GOLD, buff=0.04, stroke_width=6)
        self.play(FadeIn(hl), run_time=0.6)
        self.at("growth signals")
        gs = lab_left("growth signals stay behind", 0.6, -1.95, GOLD, 30)
        lead = arr([0.9, -2.2, 0], [-0.1, -2.95, 0], GOLD, 3, 0.15)
        self.play(FadeOut(hl), FadeIn(gs), FadeIn(lead), Indicate(dots, color=GOLD, scale_factor=1.3), run_time=0.9)
        self.finish()


class S20Stay(SpokenScene):
    def construct(self):
        band, vl, pia, bm, dots = stage_with_dots()
        cell = niche_cell(soma=False)
        stay = circ(CX, YS, LR, BLUE, 0.35)
        leave = circ(*LEAVE_END, LR, GREY, 0.3)
        self.add(band, vl, pia, bm, cell, stay, dots, leave)
        self.at("that stays")
        self.play(Indicate(stay, color=BLUE, scale_factor=1.25), run_time=0.6)
        self.at("keeps it")
        ring = Ellipse(width=2.0, height=1.1, stroke_color=YELLOW, stroke_width=7).move_to([CX, Y0 + 0.1, 0])
        t = lab_left("keeps its apical foot\nin the fluid", 0.6, -1.5, BLUE, 32, line_spacing=0.8)
        ta = arr([0.55, -1.75, 0], [CX + 0.95, Y0 + 0.2, 0], BLUE, 4, 0.2)
        self.play(FadeIn(ring, scale=1.3), Indicate(cell.afoot, color=YELLOW, scale_factor=1.5), FadeIn(t), FadeIn(ta),
                  run_time=0.7)
        self.finish()


class S21Notsame(SpokenScene):
    def construct(self):
        band, vl, pia, bm, dots = stage_with_dots()
        dots.set_opacity(0.6)
        svz = rect(-6.6, 6.6, -0.6, 2.2, GREY, 0.14)
        svl = lab_left("subventricular zone", -6.4, 1.8, GREY, 26)
        cell = RGCell(x=CX, y0=Y0, y1=2.4, ys=YS, k=KN, soma=False)
        stay = circ(CX, YS, LR, BLUE, 0.35)
        leave = circ(LX, YS, LR, GREY, 0.3)
        lfoot = foot_poly(LX, Y0, Y0 + 0.6, 0.64, 0.24, GREY, 0.85)
        self.add(svz, svl, band, vl, cell, stay, dots, leave, lfoot)
        ca = chip("loses apical contact", TEXT, size=28).move_to([-3.5, 3.3, 0])
        cb = chip("leaving", TEXT, size=28).move_to([3.4, 3.3, 0])
        link = DashedLine(ca.get_right() + RIGHT * 0.1, cb.get_left() + LEFT * 0.1, stroke_color=TEXT, stroke_width=4)
        ne = VGroup(Line([-0.4, 3.45, 0], [0.4, 3.45, 0], stroke_color=TEXT, stroke_width=7),
                    Line([-0.4, 3.15, 0], [0.4, 3.15, 0], stroke_color=TEXT, stroke_width=7),
                    Line([-0.2, 2.85, 0], [0.2, 3.75, 0], stroke_color=RED, stroke_width=7)).move_to([0.0, 3.3, 0])
        top = (2.2, 0.8)
        self.at("losing apical contact")
        self.play(FadeIn(ca, shift=DOWN * 0.15), retract(lfoot, LX, Y0 + 0.6), run_time=1.0)
        self.at("goes with")
        self.play(FadeOut(lfoot), FadeIn(cb, shift=DOWN * 0.15), FadeIn(link), leave.animate.move_to([*top, 0]),
                  run_time=1.5)
        self.at("not the same")
        self.play(FadeOut(link), FadeIn(ne, scale=0.6), run_time=0.6)
        self.at("an intermediate progenitor")
        ipl = lab_left("intermediate\nprogenitor", top[0] + LR + 0.55, top[1], ORANGE, 28, line_spacing=0.8)
        self.play(leave.animate.set_fill(ORANGE, opacity=0.4).set_stroke(ORANGE), FadeIn(ipl), run_time=0.8)
        self.at("has let go", lead=0.1)
        nof = lab("no apical foot", top[0], -1.15, TEXT, 32, weight=BOLD)
        self.play(FadeIn(nof, shift=UP * 0.1), Indicate(leave, color=ORANGE, scale_factor=1.12), run_time=0.7)
        self.at("still divides")
        ring = Circle(radius=1.15, stroke_color=TEAL, stroke_width=4).move_to([*top, 0])
        d1, d2 = circ(top[0] - 0.45, top[1], 0.55, ORANGE, 0.4), circ(top[0] + 0.45, top[1], 0.55, ORANGE, 0.4)
        self.play(FadeIn(ring), FadeOut(ipl), FadeOut(nof), ReplacementTransform(leave, VGroup(d1, d2)), run_time=0.7)
        self.at("once more")
        self.play(d1.animate.shift(LEFT * 0.7).set_fill(GREEN, opacity=0.85).set_stroke(GREEN),
                  d2.animate.shift(RIGHT * 0.7).set_fill(GREEN, opacity=0.85).set_stroke(GREEN), FadeOut(ring),
                  run_time=0.7)
        self.play(FadeIn(lab("neuron", top[0] - 1.15, top[1] - 0.95, GREEN, 26)),
                  FadeIn(lab("neuron", top[0] + 1.15, top[1] - 0.95, GREEN, 26)), run_time=0.4)
        self.finish()


class S22Take(SpokenScene):
    def construct(self):
        R_ = 0.72
        # row 1: direct
        y1 = 2.3
        sp1 = circ(-5.5, y1, R_, GREY, 0.3)
        spl1 = lab("spent daughter", -5.5, y1 + 1.15, GREY, 28)
        n1 = circ(-2.0, y1, R_, GREEN, 0.85)
        a1 = arr([-4.7, y1, 0], [-2.85, y1, 0], GREY, 6, 0.3)
        t1 = lab_left("direct: one neuron", -0.9, y1, GREEN, 38, weight=BOLD)
        # row 2: indirect
        y2 = -0.2
        sp2 = circ(-5.5, y2, R_, GREY, 0.3)
        ipc = circ(-2.4, y2, 0.8, ORANGE, 0.4)
        ipl = lab("intermediate progenitor", -3.6, y2 - 1.3, ORANGE, 28)
        a2 = arr([-4.7, y2, 0], [-3.3, y2, 0], GREY, 6, 0.3)
        m1 = circ(0.2, y2 + 0.95, R_, GREEN, 0.85)
        m2 = circ(0.2, y2 - 0.95, R_, GREEN, 0.85)
        a3 = arr([-1.75, y2 + 0.25, 0], [-0.6, y2 + 0.75, 0], GREY, 6, 0.3)
        a4 = arr([-1.75, y2 - 0.25, 0], [-0.6, y2 - 0.75, 0], GREY, 6, 0.3)
        t2 = lab_left("indirect: usually two\n(in rodent cortex)", 1.2, y2, GREEN, 38, weight=BOLD, line_spacing=0.85)
        self.at("a spent daughter")
        self.play(FadeIn(sp1, scale=0.5), FadeIn(spl1), FadeIn(sp2, scale=0.5), run_time=0.6)
        self.at("makes one neuron directly")
        self.play(GrowArrow(a1), FadeIn(n1, scale=0.5), FadeIn(t1), run_time=0.8)
        self.at("usually two through")
        self.play(GrowArrow(a2), FadeIn(ipc, scale=0.6), FadeIn(ipl), run_time=0.7)
        self.at("an intermediate progenitor")
        self.play(GrowArrow(a3), GrowArrow(a4), FadeIn(m1, scale=0.5), FadeIn(m2, scale=0.5), FadeIn(t2), run_time=0.9)
        self.at("follow its markers")
        my = -2.7
        mlabel = lab_left("markers:", -6.5, my, TEXT, 38, weight=BOLD)
        mk = VGroup(marker_chip("Pax6", BLUE, 40), marker_chip("Tbr2", ORANGE, 40), marker_chip("Tbr1", GREEN, 40)).arrange(RIGHT, buff=0.3)
        mk.move_to([-1.3, my, 0])
        self.play(FadeIn(mlabel), FadeIn(mk, shift=UP * 0.15), run_time=0.6)
        self.at("and divisions")
        dlabel = lab_left("divisions:", 1.7, my, TEXT, 38, weight=BOLD)
        dv = VGroup(divcell(5.7, my, ORANGE, 1.4))
        self.play(FadeIn(dlabel), FadeIn(dv, shift=UP * 0.15), run_time=0.6)
        self.at("tell which")
        fin = lab("markers and divisions tell you which route", 0, -3.6, YELLOW, 32, weight=BOLD)
        self.play(Indicate(VGroup(mk, dv), color=YELLOW, scale_factor=1.05), FadeIn(fin, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S23End(EndCard):
    LINE = "A spent daughter makes one neuron, or usually two through a progenitor."
