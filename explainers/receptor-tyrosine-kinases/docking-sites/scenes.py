"""RTK section film: the tail becomes a set of docking sites  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = the receptor, its kinase and tail, the tyrosine tiles
  GOLD   = a phosphate (the "P" badge)
  GREEN  = kinase ON
  YELLOW = the residue the SH2 domain is reading
  PURPLE = Grb2 and its pathway (Ras, MAP kinase)
  ORANGE = PLC-gamma and its products (IP3, DAG)
  TEAL   = PI 3-kinase and its pathway (Akt)
  RED    = a site that cannot be phosphorylated (phenylalanine) / failure to dock
  GREY   = membrane, unknowns, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PTEAL = "#3FB8C0"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tile(txt, col=GREY, w=0.85, size=28, op=1.0):
    box = RoundedRectangle(corner_radius=0.12, width=w, height=w, stroke_color=col, stroke_width=2.5,
                           fill_color=interpolate_color(ManimColor(BG), ManimColor(col), 0.14 * op),
                           fill_opacity=1).set_stroke(opacity=op)
    return VGroup(box, T(txt, size, col).set_opacity(op).move_to(box))


def hi(t, col):
    """recolor a tile to col, keeping its fill opaque."""
    return [t[0].animate.set_stroke(col).set_fill(interpolate_color(ManimColor(BG), ManimColor(col), 0.2), 1),
            t[1].animate.set_color(col)]


def pbadge(r=0.23):
    c = Circle(radius=r, stroke_width=0, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def badge_on(t):
    return pbadge().move_to(t.get_corner(UR) + RIGHT * 0.1 + UP * 0.1)


def cup(label, color, width, teeth, size=26):
    body = RoundedRectangle(corner_radius=0.14, width=width, height=0.9, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.18)
    lab = T(label, size, color).move_to(body)
    ts = [Rectangle(width=0.3, height=0.35, stroke_width=0, fill_color=color, fill_opacity=0.9)
          .move_to(body.get_bottom() + RIGHT * dx + DOWN * 0.175) for dx in teeth]
    return VGroup(body, lab, *ts)


def place_cup(c, x, bottom):
    return c.move_to([x, bottom + c.height / 2, 0])


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Receptor Tyrosine Kinases"
    TITLE = "The tail's sequence picks the partner"


# =============================================================================================
class S01Tail(SpokenScene):
    def construct(self):
        mem = RoundedRectangle(corner_radius=0.12, width=11.5, height=0.3, stroke_width=0,
                               fill_color=GREY, fill_opacity=0.6).move_to([0, 3.05, 0])
        mlab = T("membrane", 22, GREY).move_to([-5.0, 2.6, 0])
        ks, helix = [], []
        for x in (-1.3, 1.3):
            k = RoundedRectangle(corner_radius=0.2, width=2.4, height=1.0, stroke_color=BLUE, stroke_width=3,
                                 fill_color=BLUE, fill_opacity=0.16).move_to([x, 1.7, 0])
            ks.append(k)
            helix.append(Line([x, 2.9, 0], [x, 2.2, 0], color=BLUE, stroke_width=5))
        klabs = [T("kinase", 24, BLUE).move_to(k) for k in ks]
        tails = [CubicBezier(np.array([-2.3, 1.3, 0]), np.array([-4.8, 0.3, 0]), np.array([-1.6, -1.0, 0]),
                             np.array([-3.7, -2.9, 0]), color=BLUE, stroke_width=4),
                 CubicBezier(np.array([2.3, 1.3, 0]), np.array([4.8, 0.3, 0]), np.array([1.6, -1.0, 0]),
                             np.array([3.7, -2.9, 0]), color=BLUE, stroke_width=4)]
        ys = []
        for t in tails:
            for p in (0.25, 0.55, 0.85):
                c = Circle(radius=0.27, stroke_color=BLUE, stroke_width=2.5, fill_color=BG, fill_opacity=1)
                c.move_to(t.point_from_proportion(p))
                ys.append(VGroup(c, T("Y", 24, BLUE).move_to(c)))
        self.play(FadeIn(mem), FadeIn(mlab), *[Create(h) for h in helix],
                  *[FadeIn(k) for k in ks], *[FadeIn(l) for l in klabs],
                  *[Create(t) for t in tails], *[FadeIn(y) for y in ys], run_time=0.5)

        self.at("kinases are on")
        newlabs = [T("kinase ON", 24, GREEN).move_to(k) for k in ks]
        self.play(*[k.animate.set_stroke(GREEN).set_fill(GREEN, 0.18) for k in ks],
                  *[Transform(l, n) for l, n in zip(klabs, newlabs)], run_time=0.7)

        self.at("add phosphate")
        badges = [pbadge().move_to(ks[0 if i < 3 else 1].get_bottom() + DOWN * 0.1) for i in range(6)]
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in badges], lag_ratio=0.1), run_time=0.7)
        self.play(*[b.animate.move_to(y[0].get_center() + RIGHT * 0.38 + UP * 0.3) for b, y in zip(badges, ys)],
                  run_time=1.6)

        self.at("flexible tails")
        self.play(*[Indicate(t, color=YELLOW, scale_factor=1.0) for t in tails], run_time=1.2)

        self.at("docking site")
        tag = btext("docking site", 28, GOLD)
        target = badges[4]
        tag.move_to(target.get_center() + RIGHT * 1.9 + UP * 0.1)
        ar = arr(tag.get_left() + LEFT * 0.0, target.get_center() + RIGHT * 0.3, GOLD, w=4, tip=0.2)
        self.play(FadeIn(tag), GrowArrow(ar), Indicate(target, color=GOLD, scale_factor=1.5), run_time=0.8)

        self.at("pick its partner")
        qs = []
        for x in (-0.9, 0, 0.9):
            c = Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15)
            qs.append(VGroup(c, T("?", 34, GREY).move_to(c)).move_to([x, -1.6, 0]))
        self.play(LaggedStart(*[FadeIn(q, shift=UP * 0.3) for q in qs], lag_ratio=0.2), run_time=1.0)
        self.finish()


# =============================================================================================
class S02Reader(SpokenScene):
    def construct(self):
        y0 = 0.1
        W, G, SZ = 1.1, 1.3, 32
        xa, xb = -3.7, 3.5
        tail = Line([-6.2, y0, 0], [6.2, y0, 0], color=BLUE, stroke_width=4)
        head = T("EGF receptor tail", 28, BLUE).move_to([-3.8, 3.1, 0])
        note = T("x = any residue", 22, GREY).move_to([4.6, 3.1, 0])
        a = [tile("Y", BLUE, W, SZ).move_to([xa - G, y0, 0]), tile("x", GREY, W, SZ).move_to([xa, y0, 0]),
             tile("N", GREY, W, SZ).move_to([xa + G, y0, 0])]
        pa = badge_on(a[0])
        la = M("1068", 24, GREY).move_to([xa - G, y0 - 0.95, 0])
        b = [tile("Y", BLUE, W, SZ).move_to([xb - G, y0, 0]), tile("...", GREY, W, SZ, op=0.45).move_to([xb, y0, 0]),
             tile("...", GREY, W, SZ, op=0.45).move_to([xb + G, y0, 0])]
        pb_ = badge_on(b[0])
        lb = M("992", 24, GREY).move_to([xb - G, y0 - 0.95, 0])
        top = y0 + W / 2
        grey = cup("SH2", GREY, 3.9, [-G, G], 28)
        place_cup(grey, xa, top + 0.7)
        self.play(Create(tail), FadeIn(head), FadeIn(note), *[FadeIn(t) for t in a + b], FadeIn(pa), FadeIn(pb_),
                  FadeIn(la), FadeIn(lb), FadeIn(grey, shift=DOWN * 0.2), run_time=0.5)
        self.at("domain binds a")
        self.play(grey.animate.shift(DOWN * 0.7), run_time=0.7)

        self.at("checks the few residues")
        self.play(*[x for t in a[1:] for x in hi(t, YELLOW)], run_time=0.5)

        self.at("sequence decides")
        self.play(*[Indicate(t, color=YELLOW, scale_factor=1.12) for t in a], run_time=1.0)

        self.at("receptor tail")
        self.play(Indicate(head, color=BLUE, scale_factor=1.1), Indicate(pa, color=GOLD, scale_factor=1.4), run_time=0.8)

        self.at("asparagine")
        ann = T("asparagine, two residues later", 24, YELLOW).move_to([-1.3, y0 - 0.95, 0])
        self.play(FadeIn(ann), Indicate(a[2], color=YELLOW, scale_factor=1.25), run_time=0.7)

        self.at("suits the")
        purple = cup("Grb2", PURPLE, 3.9, [-G, G], 28)
        place_cup(purple, xa, top)
        self.play(ReplacementTransform(grey, purple), run_time=0.6)

        self.at("which leads to")
        ras = bchip("Ras", PURPLE, 28).move_to([xa - G, -2.4, 0])
        ar1 = arr([xa - G, y0 - 1.3, 0], ras.get_top(), PURPLE, w=4, tip=0.2)
        self.play(GrowArrow(ar1), FadeIn(ras), run_time=0.7)
        self.at("kinase cascade")
        mk = bchip("MAP kinase cascade", PURPLE, 28).move_to([-1.0, -2.4, 0])
        ar2 = arr(ras.get_right(), mk.get_left(), PURPLE, w=4, tip=0.2)
        self.play(GrowArrow(ar2), FadeIn(mk), run_time=0.7)

        self.at("same tail")
        self.play(Indicate(b[0], color=GOLD, scale_factor=1.25), run_time=0.6)
        orange = cup("PLC-γ", ORANGE, 3.9, [-G], 28)
        place_cup(orange, xb, top + 0.7)
        self.play(FadeIn(orange, shift=DOWN * 0.2), run_time=0.3)
        self.play(orange.animate.shift(DOWN * 0.7), run_time=0.6)

        self.at("that enzyme makes")
        prod = bchip("IP3 and DAG", ORANGE, 28).move_to([xb, -2.4, 0])
        ar3 = arr([xb - G, y0 - 1.3, 0], [xb - G + 0.0, -2.1, 0], ORANGE, w=4, tip=0.2)
        self.play(GrowArrow(ar3), FadeIn(prod), run_time=0.7)
        self.finish()


# =============================================================================================
class S03Mix(SpokenScene):
    def construct(self):
        head = T("HER3 tail", 28, BLUE).move_to([-5.0, 3.2, 0])
        tail = Line([-6.2, 2.4, 0], [6.2, 2.4, 0], color=BLUE, stroke_width=4)
        dots = []
        for x in (-5, -3, -1, 1, 3, 5):
            c = Circle(radius=0.32, stroke_color=BLUE, stroke_width=2.5, fill_color=BG, fill_opacity=1).move_to([x, 2.4, 0])
            d = VGroup(c, T("Y", 26, BLUE).move_to(c))
            d.add(pbadge(0.2).move_to(c.get_center() + RIGHT * 0.4 + UP * 0.3))
            dots.append(d)
        self.play(Create(tail), FadeIn(head), run_time=0.5)
        self.at("six tyrosines")
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.12), run_time=1.2)

        y0 = -0.5
        W, G = 1.1, 1.3
        tiles = [tile("Y", BLUE, W, 32), tile("x", GREY, W, 32), tile("x", GREY, W, 32), tile("M", GREY, W, 32)]
        for i, t in enumerate(tiles):
            t.move_to([-1.95 + G * i, y0, 0])
        pbm = badge_on(tiles[0])
        each = T("each of the six", 26, GREY).move_to([-5.0, y0, 0])
        self.play(FadeIn(each), *[FadeIn(t) for t in tiles], FadeIn(pbm), run_time=0.6)
        self.at("methionine")
        ann = T("methionine, three residues later", 24, YELLOW).move_to([0, y0 - 1.0, 0])
        self.play(*hi(tiles[3], YELLOW), FadeIn(ann), run_time=0.6)

        self.at("suits the")
        teal = cup("PI 3-kinase", PTEAL, 5.0, [-1.95, 1.95], 28)
        place_cup(teal, 0, y0 + W / 2 + 0.45)
        self.play(FadeIn(teal, shift=DOWN * 0.2), run_time=0.3)
        self.play(teal.animate.shift(DOWN * 0.45), run_time=0.5)

        self.at("which leads to")
        akt = bchip("Akt", PTEAL, 28).move_to([0, -3.0, 0])
        ar = arr([0, y0 - 1.35, 0], akt.get_top(), PTEAL, w=4, tip=0.2)
        self.play(GrowArrow(ar), FadeIn(akt), run_time=0.6)

        self.at("several pathways")
        old = VGroup(head, tail, *dots, each, *tiles, pbm, ann, teal, ar, akt)
        hdr = T("one activated pair", 34).move_to([0, 2.8, 0])
        rows = []
        for i, (p, pc, t) in enumerate([("Grb2", PURPLE, "Ras, MAP kinase cascade"), ("PLC-γ", ORANGE, "IP3 and DAG"),
                                        ("PI 3-kinase", PTEAL, "Akt")]):
            y = 1.0 - 1.7 * i
            c1 = chip(p, pc, 32).move_to([-3.6, y, 0])
            c2 = chip(t, pc, 32).move_to([2.6, y, 0])
            ar_ = arr(c1.get_right() + RIGHT * 0.1, c2.get_left() + LEFT * 0.1, pc, w=4, tip=0.2)
            rows.append(VGroup(c1, ar_, c2))
        self.play(FadeOut(old), FadeIn(hdr), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), run_time=1.0)

        self.at("changes the mix")
        for r in rows:
            self.play(Indicate(r[0], color=r[0][0].get_color(), scale_factor=1.15), run_time=0.5)
        self.finish()


# =============================================================================================
class S04Test(SpokenScene):
    def construct(self):
        y0 = -0.8
        W = 1.1
        head = T("PDGF receptor tail: one chain", 28, BLUE).move_to([-3.0, 3.1, 0])
        note = T("sites drawn schematically", 22, GREY).move_to([4.2, -3.3, 0])
        tail = Line([-6.2, y0, 0], [6.2, y0, 0], color=BLUE, stroke_width=4)
        specs = [(-4.6, PURPLE, "g"), (-1.8, ORANGE, "p"), (1.4, PTEAL, "k1"), (4.2, PTEAL, "k2")]
        sites, pbs = {}, {}
        for x, col, key in specs:
            t = tile("Y", col, W, 32).move_to([x, y0, 0])
            sites[key] = t
            pbs[key] = badge_on(t)
        cy = 2.0
        chips = {"g": bchip("Grb2", PURPLE, 28).move_to([-4.6, cy, 0]),
                 "p": bchip("PLC-γ", ORANGE, 28).move_to([-1.8, cy, 0]),
                 "k": bchip("PI 3-kinase", PTEAL, 28).move_to([2.8, cy, 0])}
        links = {"g": Line(chips["g"].get_bottom(), sites["g"].get_top(), color=PURPLE, stroke_width=4),
                 "p": Line(chips["p"].get_bottom(), sites["p"].get_top(), color=ORANGE, stroke_width=4),
                 "k1": Line(chips["k"].get_bottom() + LEFT * 0.5, sites["k1"].get_top(), color=PTEAL, stroke_width=4),
                 "k2": Line(chips["k"].get_bottom() + RIGHT * 0.5, sites["k2"].get_top(), color=PTEAL, stroke_width=4)}
        self.play(Create(tail), FadeIn(head), FadeIn(note), run_time=0.5)
        self.play(*[FadeIn(s) for s in sites.values()], *[FadeIn(p) for p in pbs.values()], run_time=0.5)
        self.at("carries sites")
        self.play(*[FadeIn(c) for c in chips.values()], *[Create(l) for l in links.values()], run_time=1.2)

        self.at("one at a time")
        one = btext("tested one at a time", 26, GREY).move_to([2.8, -2.4, 0])
        self.play(FadeIn(one), run_time=0.5)

        self.at("changed a tyrosine")
        f = tile("F", RED, W, 32).move_to(sites["g"])
        flab = T("phenylalanine", 24, RED).move_to([-4.6, y0 - 1.0, 0])
        self.play(Transform(sites["g"], f), FadeOut(pbs["g"]), FadeOut(links["g"]), FadeIn(flab), run_time=0.7)

        self.at("cannot be phosphorylated")
        self.play(Indicate(sites["g"], color=RED, scale_factor=1.25), run_time=0.7)

        self.at("failed to dock")
        fail = btext("does not dock", 26, RED).move_to([-4.6, 0.7, 0])
        self.play(chips["g"][1].animate.set_stroke(opacity=0.35).set_fill(opacity=0.05),
                  chips["g"][2].animate.set_opacity(0.4), FadeIn(fail), run_time=0.7)

        self.at("still did")
        self.play(FadeOut(fail), Indicate(links["p"], color=GREEN, scale_factor=1.0), Indicate(links["k1"], color=GREEN, scale_factor=1.0),
                  Indicate(links["k2"], color=GREEN, scale_factor=1.0), run_time=0.9)

        self.at("two such tyrosines")
        self.play(FadeOut(flab), FadeOut(one), Transform(sites["g"], tile("Y", PURPLE, W, 32).move_to(sites["g"])),
                  FadeIn(pbs["g"]), Create(links["g"]),
                  chips["g"][1].animate.set_stroke(opacity=1).set_fill(opacity=0.16),
                  chips["g"][2].animate.set_opacity(1), run_time=0.5)
        self.play(Indicate(sites["k1"], color=PTEAL, scale_factor=1.3), Indicate(sites["k2"], color=PTEAL, scale_factor=1.3),
                  run_time=0.9)
        self.finish()


# =============================================================================================
class S05End(EndCard):
    LINE = "The sequence after each phosphotyrosine decides which protein binds."
