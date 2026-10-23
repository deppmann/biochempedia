"""Producers, consumers and decomposers: decomposers send matter around again  (Biochemistrypedia explainer, grade 7 Life Science)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = producers (tree, acorns as plant parts)
  BLUE   = consumers (deer)
  PURPLE = decomposers (fungi, bacteria, worms, millipedes) and their chemicals
  TAN    = dead matter (fallen leaves, dead plants, dead animals, wastes)
  ORANGE = nutrients (in the soil)
  YELLOW = sunlight / energy in
  RED    = heat leaving
  TEXT   = sugar, matter-loop arrows
  GREY   = ground, soil, outlines, carbon dioxide, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TAN = "#B8946A"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ground(y=-2.9, h=0.5):
    return Rectangle(width=12.6, height=h, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                     fill_opacity=0.3).move_to([0, y, 0])


def tree(x, base_y, s=1.0):
    """trunk + canopy, as plain shapes. base_y is the top of the ground."""
    th = 1.8 * s
    trunk = Rectangle(width=0.4 * s, height=th, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                      fill_opacity=0.5).move_to([x, base_y + th / 2, 0])
    canopy = Circle(radius=1.35 * s, stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                    fill_opacity=0.3).move_to([x, base_y + th + 0.75 * s, 0])
    g = VGroup(trunk, canopy)
    g.canopy, g.trunk = canopy, trunk
    return g


def leaf(x, y, ang=0.0, s=1.0):
    return Ellipse(width=0.42 * s, height=0.2 * s, stroke_color=TAN, stroke_width=2, fill_color=TAN,
                   fill_opacity=0.8).move_to([x, y, 0]).rotate(ang)


def layer(cx, k, w=3.4, base=-2.65):
    return RoundedRectangle(corner_radius=0.08, width=w, height=0.32, stroke_color=TAN, stroke_width=2,
                            fill_color=TAN, fill_opacity=0.55).move_to([cx, base + 0.16 + 0.34 * k, 0])


def sun(x, y, r=0.45):
    return Circle(radius=r, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.7).move_to([x, y, 0])


def ndots(pts, color=ORANGE, r=0.14):
    return VGroup(*[Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.8)
                    .move_to([p[0], p[1], 0]) for p in pts])


class S00Title(TitleCard):
    LESSON = "Producers, consumers and decomposers"
    TITLE = "Decomposers send matter around again"


# ---------------------------------------------------------------------------------------------
class S01Leaves(SpokenScene):
    def construct(self):
        gr = ground()
        tr = tree(-4.4, -2.65, 1.15)
        self.at("In autumn")
        self.play(FadeIn(gr), FadeIn(tr), run_time=0.7)
        rng = np.random.default_rng(3)
        xs = rng.uniform(-2.6, -0.1, 14)
        ys = rng.uniform(0.2, 2.8, 14)
        fall = VGroup(*[leaf(x, y, rng.uniform(-1, 1), 1.3) for x, y in zip(xs, ys)])
        pile = [layer(-1.35, 0, 2.8)]
        self.at("drop their leaves")
        self.play(FadeIn(fall, lag_ratio=0.05), tr.canopy.animate.set_fill(GREEN, 0.1), run_time=0.6)
        self.play(*[f.animate.move_to([x, -2.62, 0]) for f, x in zip(fall, xs)], run_time=1.4, rate_func=smooth)
        self.play(ReplacementTransform(fall, pile[0]), run_time=0.5)
        self.at("every year")
        self.play(tr.canopy.animate.set_fill(GREEN, 0.3), run_time=0.4)
        fall2 = VGroup(*[leaf(x, y, rng.uniform(-1, 1), 1.3) for x, y in zip(xs, ys)])
        self.play(FadeIn(fall2, lag_ratio=0.04), tr.canopy.animate.set_fill(GREEN, 0.1), run_time=0.4)
        self.play(*[f.animate.move_to([x, -2.1, 0]) for f, x in zip(fall2, xs)], run_time=1.0)
        pile.append(layer(-1.35, 1, 2.8))
        self.play(ReplacementTransform(fall2, pile[1]), run_time=0.4)
        self.at("stack higher")
        up = arr([0.6, -2.3, 0], [0.6, 0.2, 0], TAN, w=7)
        self.play(GrowArrow(up), run_time=0.5)
        for k in (2, 3, 4):
            pile.append(layer(-1.35, k, 2.8))
            self.play(FadeIn(pile[-1], shift=DOWN * 0.2), tr.canopy.animate.set_fill(GREEN, 0.3 if k == 3 else 0.12), run_time=0.45)
        self.at("So where do")
        q1 = T("Where do the\nfallen leaves go?", 44, font=TITLE_FONT).move_to([3.9, 1.6, 0])
        self.play(FadeOut(up), Write(q1), run_time=1.4)
        self.at("What would happen")
        q2 = T("What if nothing\nbroke them down?", 40, font=TITLE_FONT, color=TAN).move_to([3.9, -0.7, 0])
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Jobs(SpokenScene):
    def construct(self):
        gr = ground()
        tr = tree(-4.4, -2.65, 1.1)
        head = T("Three jobs", 46, font=TITLE_FONT).move_to([2.4, 2.8, 0])
        self.play(FadeIn(gr), FadeIn(tr), run_time=0.8)
        self.at("three jobs")
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.6)
        sn = sun(-6.0, 2.7)
        sl = T("sunlight", 26, YELLOW).next_to(sn, RIGHT, buff=0.15)
        c = tr.canopy.get_center()
        ar = arr([-5.4, 2.4, 0], [c[0] - 0.7, c[1] + 0.85, 0], YELLOW, w=7)
        ptag = chip("producer", GREEN, size=32).move_to([-2.0, -1.5, 0])
        self.at("A producer")
        self.play(FadeOut(head), FadeIn(ptag, shift=LEFT * 0.2), run_time=0.6)
        self.at("captures energy from sunlight")
        self.play(FadeIn(sn, scale=0.7), FadeIn(sl), GrowArrow(ar), run_time=0.9)
        sug = chip("sugar (glucose)", TEXT, size=30).move_to([-0.6, 1.1, 0])
        a2 = arr([c[0] + 1.4, c[1] - 0.1, 0], [sug.get_left()[0], 1.1, 0], TEXT, w=6)
        self.at("stores it in sugar")
        self.play(GrowArrow(a2), FadeIn(sug, shift=RIGHT * 0.2), run_time=0.8)
        lst = T("trees  grasses  mosses", 30, GREEN).move_to([0.2, 2.5, 0])
        self.at("Trees grasses and mosses")
        self.play(FadeIn(lst, shift=DOWN * 0.1), run_time=0.7)
        ctag = chip("consumer", BLUE, size=32).move_to([5.0, 0.6, 0])
        self.at("A consumer gets energy")
        self.play(FadeIn(ctag, shift=UP * 0.2), run_time=0.7)
        ac = chip("acorns", GREEN, size=30).move_to([2.0, -0.8, 0])
        dr = chip("deer", BLUE, size=30).move_to([5.0, -0.8, 0])
        ae = arr(ac.get_right(), dr.get_left(), TEXT, w=6)
        eat = T("eats", 26, GREY).move_to([3.5, -0.3, 0])
        self.at("A deer eating acorns")
        self.play(FadeIn(ac, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(dr, shift=LEFT * 0.2), GrowArrow(ae), FadeIn(eat), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Decomposer(SpokenScene):
    def construct(self):
        dead = [bchip("dead plants", TAN, 30).move_to([-4.2, 2.5, 0]),
                bchip("dead animals", TAN, 30).move_to([0, 2.5, 0]),
                bchip("wastes", TAN, 30).move_to([4.2, 2.5, 0])]
        dec = chip("decomposer", PURPLE, size=42).move_to([0, 0.5, 0])
        arrs = [arr(d.get_bottom() + DOWN * 0.02, dec.get_top() + [(-1.6, 0, 0), (0, 0, 0), (1.6, 0, 0)][i], TAN, w=5)
                for i, d in enumerate(dead)]
        self.at("A decomposer breaks down")
        self.play(FadeIn(dec, scale=0.9), run_time=0.6)
        self.at("dead plants")
        self.play(FadeIn(dead[0], shift=DOWN * 0.15), GrowArrow(arrs[0]), run_time=0.5)
        self.at("dead animals")
        self.play(FadeIn(dead[1], shift=DOWN * 0.15), GrowArrow(arrs[1]), run_time=0.5)
        self.at("and wastes")
        self.play(FadeIn(dead[2], shift=DOWN * 0.15), GrowArrow(arrs[2]), run_time=0.5)
        fu = chip("fungi", PURPLE, size=38).move_to([-2.6, -1.9, 0])
        ba = chip("bacteria", PURPLE, size=38).move_to([2.6, -1.9, 0])
        a1 = arr(dec.get_bottom() + [-0.5, 0, 0], fu.get_top(), PURPLE, w=5)
        a2 = arr(dec.get_bottom() + [0.5, 0, 0], ba.get_top(), PURPLE, w=5)
        self.at("The main decomposers")
        self.play(FadeIn(fu, shift=UP * 0.15), FadeIn(ba, shift=UP * 0.15), GrowArrow(a1), GrowArrow(a2), run_time=0.9)
        self.at("A fungus has")
        self.play(*[FadeOut(m) for m in (*dead, dec, *arrs, a1, a2, ba)], fu.animate.move_to([100, 0, 0]), run_time=0.6)
        # fungus mechanism
        body = RoundedRectangle(corner_radius=0.5, width=3.6, height=3.0, stroke_color=PURPLE, stroke_width=4,
                                fill_color=PURPLE, fill_opacity=0.15).move_to([3.6, -0.3, 0])
        fl = T("fungus", 36, PURPLE).move_to([3.6, 0.8, 0])
        nm = T("no mouth", 30, GREY).move_to([3.6, -2.4, 0])
        lf = RoundedRectangle(corner_radius=0.2, width=3.4, height=1.5, stroke_color=TAN, stroke_width=3,
                              fill_color=TAN, fill_opacity=0.55).move_to([-3.2, -0.3, 0])
        lfl = T("dead leaf", 28, TAN).next_to(lf, UP, buff=0.2)
        self.play(FadeIn(body), FadeIn(fl), FadeIn(lf), FadeIn(lfl), run_time=0.7)
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.5)
        self.at("It releases chemicals")
        chem = VGroup(*[Circle(radius=0.11, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.9)
                        .move_to([1.75, -0.3 + dy, 0]) for dy in (-0.45, 0, 0.45)])
        cl = T("chemicals", 26, PURPLE).move_to([0.2, 0.75, 0])
        self.play(FadeIn(chem), FadeIn(cl), run_time=0.4)
        self.play(chem.animate.shift(LEFT * 2.6), run_time=1.0)
        self.at("break down the leaf")
        pcs = VGroup(*[Rectangle(width=0.48, height=0.4, stroke_color=TAN, stroke_width=2, fill_color=TAN, fill_opacity=0.7)
                       .move_to([-4.3 + 0.8 * (i % 3), 0.05 - 0.6 * (i // 3) - 0.1, 0]) for i in range(6)])
        self.play(FadeOut(chem), FadeOut(cl), ReplacementTransform(lf, pcs), run_time=0.9)
        out = T("outside its body", 28, GREY).move_to([-1.2, -2.4, 0])
        self.at("outside its body")
        self.play(FadeIn(out, shift=UP * 0.1), run_time=0.5)
        self.at("takes in the small pieces")
        self.play(*[p.animate.move_to([3.1 + 0.5 * (i % 3) - 0.5, -0.4 - 0.5 * (i // 3), 0]) for i, p in enumerate(pcs)],
                  FadeOut(lfl), run_time=1.5)
        self.play(*[p.animate.scale(0.5) for p in pcs], run_time=0.4)
        self.at("Worms and millipedes")
        self.play(*[FadeOut(m) for m in (body, fl, nm, out, pcs)], run_time=0.5)
        lf2 = RoundedRectangle(corner_radius=0.2, width=4.4, height=1.6, stroke_color=TAN, stroke_width=3,
                               fill_color=TAN, fill_opacity=0.55).move_to([0, -1.0, 0])
        lf2l = T("dead leaf", 28, TAN).next_to(lf2, DOWN, buff=0.2)
        wm = chip("worms, millipedes", PURPLE, size=34).move_to([0, 2.1, 0])
        self.play(FadeIn(lf2), FadeIn(lf2l), FadeIn(wm, shift=DOWN * 0.15), run_time=0.7)
        self.at("tearing dead leaves")
        bits = VGroup(*[Rectangle(width=0.62, height=0.5, stroke_color=TAN, stroke_width=2, fill_color=TAN, fill_opacity=0.7)
                        .move_to([-2.4 + 0.8 * (i % 7), -1.0 + 0.0 - 0.7 * (i // 7) + 0.35, 0]) for i in range(14)])
        self.play(wm.animate.move_to([0, 0.9, 0]), run_time=0.5)
        self.play(ReplacementTransform(lf2, bits), run_time=1.0)
        sm = T("smaller bits", 30, TAN).move_to([0, -2.4, 0])
        self.at("smaller bits")
        self.play(FadeOut(lf2l), FadeIn(sm), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Nutrients(SpokenScene):
    def construct(self):
        gy = -0.3
        soil = Rectangle(width=12.6, height=3.0, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                         fill_opacity=0.16).move_to([0, gy - 1.5, 0])
        surf = Line([-6.3, gy, 0], [6.3, gy, 0], color=GREY, stroke_width=4)
        sl = T("soil", 28, GREY).move_to([-5.7, -3.05, 0])
        tr = tree(-4.0, gy, 1.0)
        roots = VGroup(Line([-4.0, gy, 0], [-4.7, -1.5, 0], color=GREY, stroke_width=4),
                       Line([-4.0, gy, 0], [-4.0, -1.9, 0], color=GREY, stroke_width=4),
                       Line([-4.0, gy, 0], [-3.3, -1.5, 0], color=GREY, stroke_width=4))
        lf = RoundedRectangle(corner_radius=0.15, width=2.2, height=0.5, stroke_color=TAN, stroke_width=3,
                              fill_color=TAN, fill_opacity=0.6).move_to([0, gy + 0.27, 0])
        lfl = T("leaf", 26, TAN).move_to([1.8, gy + 0.55, 0])
        dec = chip("fungi, bacteria", PURPLE, size=28).move_to([0, -1.3, 0])
        self.at("As decomposers break down")
        self.play(FadeIn(soil), FadeIn(surf), FadeIn(sl), FadeIn(tr), FadeIn(roots), FadeIn(lf), FadeIn(lfl), run_time=0.9)
        self.play(FadeIn(dec, shift=UP * 0.2), run_time=0.5)
        self.play(lf.animate.stretch(0.6, 0).set_opacity(0.5), run_time=0.8)
        pts = [(-2.3, -1.0), (-2.7, -1.5), (-2.0, -1.8), (-2.2, -2.2), (-3.0, -1.9)]
        nd = ndots(pts)
        nl = T("nutrients", 30, ORANGE).move_to([-1.8, -2.85, 0])
        ar = arr(dec.get_left(), [-1.5, -1.3, 0], ORANGE, w=5)
        self.at("nutrients go back")
        self.play(GrowArrow(ar), FadeIn(nd, lag_ratio=0.15), FadeIn(nl), FadeOut(lfl), FadeOut(lf), run_time=1.2)
        d1 = T("A nutrient is a substance,", 26, ORANGE)
        d2 = T("such as nitrogen, that living", 26, ORANGE)
        d3 = T("things need to grow.", 26, ORANGE)
        dfn = VGroup(d1, d2, d3).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([3.4, 2.6, 0])
        self.at("A nutrient is a substance")
        self.play(FadeIn(dfn, shift=DOWN * 0.1), run_time=0.9)
        self.at("Plant roots take up")
        tips = [(-4.7, -1.5), (-4.0, -1.9), (-3.3, -1.5)]
        self.play(*[nd[i].animate.move_to([tips[i % 3][0], tips[i % 3][1], 0]) for i in range(5)], FadeOut(nl), FadeOut(ar), run_time=1.2)
        up = arr([-2.9, -1.3, 0], [-2.9, 0.5, 0], ORANGE, w=6)
        use = T("used again", 28, ORANGE).move_to([-1.7, 0.9, 0])
        self.at("use them again")
        self.play(GrowArrow(up), FadeIn(use), tr.canopy.animate.set_fill(GREEN, 0.5), FadeOut(nd), run_time=0.9)
        co = bchip("carbon dioxide", GREY, size=30).move_to([3.7, 0.9, 0])
        cu = arr([0.9, -0.9, 0], [2.4, 0.7, 0], GREY, w=6)
        self.at("carbon dioxide")
        self.play(GrowArrow(cu), FadeIn(co, shift=UP * 0.2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Without(SpokenScene):
    def construct(self):
        gy = -0.3
        soil = Rectangle(width=12.6, height=3.0, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                         fill_opacity=0.16).move_to([0, gy - 1.5, 0])
        surf = Line([-6.3, gy, 0], [6.3, gy, 0], color=GREY, stroke_width=4)
        sl = T("soil", 28, GREY).move_to([-5.7, -3.05, 0])
        tr = tree(-4.0, gy, 1.0)
        roots = VGroup(Line([-4.0, gy, 0], [-4.7, -1.5, 0], color=GREY, stroke_width=4),
                       Line([-4.0, gy, 0], [-4.0, -1.9, 0], color=GREY, stroke_width=4),
                       Line([-4.0, gy, 0], [-3.3, -1.5, 0], color=GREY, stroke_width=4))
        dec = chip("fungi, bacteria", PURPLE, size=28).move_to([0, -1.3, 0])
        pts = [(-2.3, -1.0), (-2.7, -1.5), (-2.0, -1.8), (-2.2, -2.2), (-3.0, -1.9)]
        nd = ndots(pts)
        nl = T("nutrients in the soil", 28, ORANGE).move_to([-1.4, -2.85, 0])
        self.play(FadeIn(soil), FadeIn(surf), FadeIn(sl), FadeIn(tr), FadeIn(roots), FadeIn(dec), FadeIn(nd), FadeIn(nl), run_time=0.8)
        self.at("take the decomposers away")
        x1 = Line(dec.get_corner(UL), dec.get_corner(DR), color=GREY, stroke_width=6)
        x2 = Line(dec.get_corner(UR), dec.get_corner(DL), color=GREY, stroke_width=6)
        self.play(Create(x1), Create(x2), dec.animate.set_opacity(0.35), run_time=0.7)
        pile = [RoundedRectangle(corner_radius=0.08, width=2.6, height=0.3, stroke_color=TAN, stroke_width=2,
                                 fill_color=TAN, fill_opacity=0.55).move_to([0.2, gy + 0.15 + 0.32 * k, 0]) for k in range(5)]
        self.at("Dead leaves would pile up")
        for p in pile:
            self.play(FadeIn(p, shift=DOWN * 0.3), run_time=0.35)
        pl = T("dead leaves pile up", 28, TAN).move_to([3.4, 0.7, 0])
        self.play(FadeIn(pl), run_time=0.4)
        self.at("Fewer nutrients")
        self.play(FadeOut(nd[3]), FadeOut(nd[4]), run_time=0.8)
        gl = T("plants may grow less", 28, GREEN).move_to([0.4, 2.3, 0])
        self.at("plants may grow less")
        self.play(tr.canopy.animate.scale(0.95).set_fill(GREEN, 0.22), FadeIn(gl), run_time=2.4)
        self.at("Producers consumers")
        self.play(*[FadeOut(m) for m in (soil, surf, sl, tr, roots, dec, x1, x2, nd[0], nd[1], nd[2], nl, *pile, pl, gl)], run_time=0.6)
        pr = chip("producers", GREEN, size=36).move_to([0, 2.2, 0])
        co = chip("consumers", BLUE, size=36).move_to([-4.0, -1.7, 0])
        de = chip("decomposers", PURPLE, size=36).move_to([4.0, -1.7, 0])
        l1 = DoubleArrow(pr.get_bottom() + [-0.6, -0.05, 0], co.get_top() + [0.5, 0.05, 0], color=GREY, stroke_width=5, buff=0.05, tip_length=0.2)
        l2 = DoubleArrow(pr.get_bottom() + [0.6, -0.05, 0], de.get_top() + [-0.5, 0.05, 0], color=GREY, stroke_width=5, buff=0.05, tip_length=0.2)
        l3 = DoubleArrow(co.get_right(), de.get_left(), color=GREY, stroke_width=5, buff=0.08, tip_length=0.2)
        self.play(FadeIn(pr, scale=0.9), FadeIn(co, scale=0.9), FadeIn(de, scale=0.9), run_time=0.6)
        self.at("are linked")
        self.play(GrowArrow(l1), GrowArrow(l2), GrowArrow(l3), run_time=0.8)
        self.at("A change in one group")
        self.play(Indicate(de, color=PURPLE, scale_factor=1.25), run_time=0.8)
        self.at("reaches the others")
        self.play(l2.animate.set_color(PURPLE), l3.animate.set_color(PURPLE), run_time=0.4)
        self.play(Indicate(pr, color=GREEN, scale_factor=1.2), Indicate(co, color=BLUE, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Around(SpokenScene):
    def construct(self):
        P = {"pr": [-4.3, 0.9, 0], "co": [0, 2.3, 0], "dm": [4.3, 0.9, 0], "de": [2.5, -2.4, 0], "nu": [-2.5, -2.4, 0]}
        pr = chip("producers", GREEN, size=30).move_to(P["pr"])
        co = chip("consumers", BLUE, size=30).move_to(P["co"])
        dm = chip("dead matter", TAN, size=30).move_to(P["dm"])
        de = chip("decomposers", PURPLE, size=30).move_to(P["de"])
        nu = chip("nutrients", ORANGE, size=30).move_to(P["nu"])
        nodes = {"pr": pr, "co": co, "dm": dm, "de": de, "nu": nu}

        def link(a, b, **kw):
            A, B = nodes[a], nodes[b]
            d = (B.get_center() - A.get_center())
            d = d / np.linalg.norm(d)
            def edge(n, v):
                w, h = n.width / 2, n.height / 2
                t = min(w / max(abs(v[0]), 1e-6), h / max(abs(v[1]), 1e-6))
                return n.get_center() + v * (t + 0.1)
            return arr(edge(A, d), edge(B, -d), TEXT, w=4, tip=0.2)
        links = [link("pr", "co"), link("co", "dm"), link("pr", "dm"), link("dm", "de"), link("de", "nu"), link("nu", "pr")]
        self.at("Matter goes")
        self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in nodes.values()], lag_ratio=0.12),
                  LaggedStart(*[GrowArrow(l) for l in links], lag_ratio=0.12), run_time=1.3)
        # a dot of matter travels pr -> dm -> de -> nu -> pr
        path = Polygon(*[np.array(P[k], float) + np.array([0, -0.75 if k == "pr" else 0, 0]) for k in ("pr", "dm", "de", "nu")],
                       color=TEXT, stroke_width=0)
        dot = Dot(radius=0.14, color=TEXT).move_to(path.get_start())
        ml = T("matter goes around", 28, TEXT).move_to([0, -0.4, 0])
        self.at("around and around")
        self.play(FadeIn(dot), FadeIn(ml), run_time=0.3)
        self.play(MoveAlongPath(dot, path), run_time=2.0, rate_func=linear)
        self.at("Energy does not")
        el = T("energy does not", 28, YELLOW).move_to([0, -1.1, 0])
        self.play(FadeOut(dot), FadeIn(el), run_time=0.4)
        sn = sun(-6.0, 2.9, 0.38)
        sa = arr([-5.7, 2.5, 0], [pr.get_left()[0] - 0.05, pr.get_top()[1] - 0.05, 0], YELLOW, w=6)
        self.at("Energy enters as sunlight")
        self.play(FadeIn(sn, scale=0.7), GrowArrow(sa), run_time=0.7)
        h1 = arr([5.2, 1.7, 0], [5.7, 2.5, 0], RED, w=6, tip=0.2)
        hl1 = T("energy leaves as heat", 24, RED).move_to([4.5, 3.0, 0])
        self.at("leaves as heat")
        self.play(GrowArrow(h1), FadeIn(hl1), run_time=0.8)
        self.at("So where do")
        self.play(*[FadeOut(m) for m in (sn, sa, h1, hl1, ml, el)], run_time=0.6)
        a1 = T("Broken down by decomposers", 32, PURPLE).move_to([0, -0.2, 0])
        a2 = T("Nutrients go back to the soil", 32, ORANGE).move_to([0, -1.0, 0])
        self.at("Fungi bacteria")
        self.play(FadeIn(a1, shift=UP * 0.1), Indicate(de, color=PURPLE, scale_factor=1.2), run_time=0.8)
        self.at("the nutrients go back")
        self.play(FadeIn(a2, shift=UP * 0.1), links[4].animate.set_color(ORANGE), links[5].animate.set_color(ORANGE),
                  Indicate(nu, color=ORANGE, scale_factor=1.2), run_time=0.9)
        self.at("take them up again")
        self.play(Indicate(pr, color=GREEN, scale_factor=1.25), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Nutrients go back into the soil, where trees take them up again."
