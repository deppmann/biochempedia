"""Plant nutrition: peas borrow nitrogen from bacteria  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = the pea (a legume) and its tissues
  ORANGE = the oat (a cereal)
  BLUE   = nitrogen taken from air (nitrogen gas, ammonia) and the nitrogen gauges
  YELLOW = nitrate in the nutrient solution / soil
  PURPLE = rhizobia, bacteroids, nodules (the living partner)
  TEAL   = leghemoglobin, the plant protein that buffers oxygen
  PINK   = nitrogenase, the bacterial enzyme
  RED    = oxygen
  GOLD   = carbon supplied by the plant (sucrose, malate)
  GREY   = sand, pots, outlines, "none / nothing happened"
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SAND = "#A89A7C"
PINK = "#E58FB6"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dot(color, x, y, r=0.13):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to([x, y, 0])


# ---- a pot of sand with a plant, drawn as blocks -------------------------------------------
def pot(cx, top=-0.4, w=3.2, h=1.8):
    return Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=SAND,
                     fill_opacity=0.28).move_to([cx, top - h / 2, 0])


def plant(cx, color, height, top=-0.4, nodules=0.0, nod_color=PURPLE):
    """Fixed submobject order so Transform works: stem, leafA, leafB, leafC, 3 roots, 3 nodules."""
    fr = min(height, 2.4) / 2.4
    stem = Line([cx, top, 0], [cx, top + height, 0], color=color, stroke_width=10)
    lw, lh = 0.4 + 0.7 * fr, 0.2 + 0.12 * fr
    ya = top + height * 0.55
    la = RoundedRectangle(corner_radius=0.08, width=lw, height=lh, stroke_color=color, stroke_width=2,
                          fill_color=color, fill_opacity=0.55).move_to([cx - lw / 2 - 0.04, ya, 0])
    lb = RoundedRectangle(corner_radius=0.08, width=lw, height=lh, stroke_color=color, stroke_width=2,
                          fill_color=color, fill_opacity=0.55).move_to([cx + lw / 2 + 0.04, ya + 0.12 * height, 0])
    lc = RoundedRectangle(corner_radius=0.08, width=lw * 0.9, height=lh, stroke_color=color, stroke_width=2,
                          fill_color=color, fill_opacity=0.55).move_to([cx, top + height + lh / 2 + 0.04, 0])
    ends = [(-0.95, -1.3), (0.0, -1.5), (0.95, -1.3)]
    roots = [Line([cx, top, 0], [cx + dx, top + dy, 0], color=color, stroke_width=5) for dx, dy in ends]
    nods = [Circle(radius=0.2, stroke_color=nod_color, stroke_width=2 if nodules else 0, fill_color=nod_color,
                   fill_opacity=0.95 if nodules else 0).move_to([cx + dx, top + dy, 0]) for dx, dy in ends]
    return VGroup(stem, la, lb, lc, *roots, *nods)


def grow(old, new):
    """Transform a plant to a new height; nodule circles fade in on their own (no size glitch)."""
    anims = [Transform(a, b) for a, b in zip(old[:7], new[:7])]
    anims += [n.animate.set_fill(PURPLE, 0.95).set_stroke(PURPLE, 2, 1) for n in old[7:]] if new[7].get_fill_opacity() > 0 else []
    return anims


def gauge(cx, base=-3.0, hgt=3.0, level=0.0, w=0.5):
    frame = Rectangle(width=w, height=hgt, stroke_color=GREY, stroke_width=3).move_to([cx, base + hgt / 2, 0])
    hh = max(level * hgt, 0.001)
    fill = Rectangle(width=w - 0.06, height=hh, stroke_width=0, fill_color=BLUE,
                     fill_opacity=0.9).move_to([cx, base + hh / 2, 0])
    g = VGroup(frame, fill)
    g.frame, g.fill = frame, fill
    g.base, g.hgt, g.cx, g.w = base, hgt, cx, w
    return g


def level_to(g, level, color=BLUE):
    hh = max(level * g.hgt, 0.001)
    new = Rectangle(width=g.w - 0.06, height=hh, stroke_width=0, fill_color=color, fill_opacity=0.9)
    new.move_to([g.cx, g.base + hh / 2, 0])
    return Transform(g.fill, new)


def seedmark(g, level, text="seed"):
    y = g.base + level * g.hgt
    ln = Line([g.cx - g.w / 2 - 0.12, y, 0], [g.cx + g.w / 2 + 0.12, y, 0], color=YELLOW, stroke_width=4)
    lb = T(text, 22, YELLOW).next_to(ln, RIGHT, buff=0.1)
    return VGroup(ln, lb)


class S00Title(TitleCard):
    LESSON = "Soil, nutrients and partners"
    TITLE = "Peas borrow nitrogen from bacteria"


# ---------------------------------------------------------------------------------------------
class S01Pots(SpokenScene):
    def construct(self):
        px, ox, top = -3.6, 2.6, -0.3
        pp, op = pot(px, top), pot(ox, top)
        pl = T("pea, sterilised sand", 26, GREEN, weight=BOLD).next_to(pp, DOWN, buff=0.2)
        ol = T("oat, sterilised sand", 26, ORANGE, weight=BOLD).next_to(op, DOWN, buff=0.2)
        pea = plant(px, GREEN, 0.7, top)
        oat = plant(ox, ORANGE, 0.7, top)
        gp = gauge(px + 2.2, -3.0, 3.0, 0.08)
        go = gauge(ox + 2.2, -3.0, 3.0, 0.08)
        gl = VGroup(T("nitrogen in plant", 22, BLUE).move_to([(gp.cx + go.cx) / 2, -3.2, 0]),
                    T("schematic: 'many times more', not a measured ratio", 22, GREY).move_to([(gp.cx + go.cx) / 2, -3.6, 0]))
        self.at("a pea plant")
        self.play(FadeIn(pp), FadeIn(op), FadeIn(pl), FadeIn(ol), run_time=0.8)
        self.play(FadeIn(pea), FadeIn(oat), run_time=0.5)
        self.at("no nitrogen")
        sol = bchip("solution: no nitrogen", YELLOW, 26).move_to([(px + ox) / 2 + 0.1, 2.5, 0])
        a1 = arr([sol.get_left()[0] + 0.3, 2.2, 0], [px + 0.3, 1.3, 0], YELLOW)
        a2 = arr([sol.get_right()[0] - 0.3, 2.2, 0], [ox - 0.3, 1.3, 0], YELLOW)
        self.play(FadeIn(sol, shift=DOWN * 0.15), GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        self.at("a little soil extract")
        ext = bchip("soil extract", PURPLE, 24).move_to([px - 0.2, 1.7, 0])
        self.play(FadeIn(ext, shift=DOWN * 0.2), FadeOut(a1), run_time=0.6)
        self.play(ext.animate.move_to([px, top + 0.55, 0]), FadeIn(gp), FadeIn(go), FadeIn(gl),
                  FadeOut(sol), FadeOut(a2), run_time=0.8)
        sm = seedmark(gp, 0.08)
        self.play(FadeIn(sm), FadeOut(ext), run_time=0.3)
        self.at("many times more nitrogen")
        pea2 = plant(px, GREEN, 2.2, top, nodules=1.0)
        self.play(*grow(pea, pea2), level_to(gp, 0.95), run_time=2.0)
        self.at("starves")
        oat2 = plant(ox, ORANGE, 0.5, top)
        self.play(*grow(oat, oat2), level_to(go, 0.06, BLUE), run_time=0.8)
        self.at("Nitrogen gas")
        gas = VGroup(*[T("N2 gas", 26, BLUE).move_to([x, 3.35 - (i % 2) * 0.5, 0])
                       for i, x in enumerate([-5.4, -3.2, -1.0, 1.2, 3.4, 5.6])])
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.2) for g in gas], lag_ratio=0.12), run_time=1.2)
        self.at("So why can one use it")
        q = T("?", 72, YELLOW, weight=BOLD).move_to([(px + ox) / 2 + 0.1, 1.0, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Oats(SpokenScene):
    def construct(self):
        cx, top = -0.6, -0.3
        pp = pot(cx, top, w=4.2)
        oat = plant(cx, ORANGE, 0.5, top)
        lbl = T("oat", 30, ORANGE, weight=BOLD).next_to(pp, DOWN, buff=0.2)
        g = gauge(cx + 3.5, -3.0, 3.0, 0.06)
        gl = T("nitrogen in plant", 22, BLUE).move_to([cx + 3.5, -3.3, 0])
        head = T("Bernburg, published 1888", 30, font=TITLE_FONT).to_edge(UP, buff=0.4)
        self.at("Hermann")
        self.play(Write(head), FadeIn(pp), FadeIn(oat), FadeIn(lbl), FadeIn(g), FadeIn(gl), run_time=1.0)
        self.at("every mineral element")
        sol = bchip("every mineral element, no nitrogen", YELLOW, 26).move_to([cx, 2.55, 0])
        self.play(FadeIn(sol, shift=DOWN * 0.15), run_time=0.6)
        self.at("as far as the nitrate")
        steps = [(0.9, 0.3), (1.4, 0.55), (1.9, 0.8)]
        for i, (ph, lv) in enumerate(steps):
            n = bchip("nitrate", YELLOW, 24).move_to([cx + 2.0, 1.0, 0])
            self.play(FadeIn(n, shift=DOWN * 0.15), run_time=0.35)
            self.play(n.animate.move_to([cx + 1.0, top - 0.4, 0]), run_time=0.45)
            self.play(*grow(oat, plant(cx, ORANGE, ph, top)), level_to(g, lv), FadeOut(n), run_time=0.7)
        note = T("growth follows the nitrate given", 28, ORANGE).move_to([cx, 2.55, 0])
        self.play(FadeOut(sol), run_time=0.2)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Extract(SpokenScene):
    def construct(self):
        xs, top = [-4.2, 0.0, 4.2], -0.5
        pots = [pot(x, top, w=2.8, h=1.8) for x in xs]
        names = [T("no extract", 28, GREY), T("live extract", 28, PURPLE), T("heated extract", 28, GREY)]
        for n, x in zip(names, xs):
            n.move_to([x, 2.4, 0])
        peas = [plant(x, GREEN, 0.7, top) for x in xs]
        gs = [gauge(x + 1.8, -2.8, 2.4, 0.06, w=0.4) for x in xs]
        gl = [T("nitrogen\ngain", 22, BLUE, line_spacing=0.6).move_to([x + 1.8, -3.2, 0]) for x in xs]
        self.at("Now the peas")
        self.play(*[FadeIn(p) for p in pots], *[FadeIn(p) for p in peas], *[FadeIn(n) for n in names],
                  *[FadeIn(g) for g in gs], *[FadeIn(g) for g in gl], run_time=1.0)
        self.at("With no extract")
        tag0 = T("no nodules", 28, GREY).move_to([xs[0], -2.75, 0])
        self.play(Indicate(names[0], color=GREY), run_time=0.5)
        self.at("no nodules")
        self.play(FadeIn(tag0), run_time=0.4)
        self.at("Given a little extract")
        drop = bchip("extract", PURPLE, 24).move_to([xs[1], 1.6, 0])
        self.play(FadeIn(drop, shift=DOWN * 0.1), run_time=0.4)
        self.play(drop.animate.move_to([xs[1] + 1.0, top + 0.5, 0]), run_time=0.6)
        self.at("formed nodules")
        grown = plant(xs[1], GREEN, 1.9, top, nodules=1.0)
        self.play(*grow(peas[1], grown), FadeOut(drop), run_time=0.9)
        tag1 = T("nodules", 28, PURPLE).move_to([xs[1], -2.75, 0])
        self.play(FadeIn(tag1), run_time=0.3)
        self.at("swellings on the roots")
        self.play(Indicate(VGroup(*peas[1][7:]), color=PURPLE, scale_factor=1.25), run_time=0.8)
        self.at("gained much nitrogen from the air")
        self.play(level_to(gs[1], 0.9), run_time=1.2)
        self.at("heated first")
        drop3 = bchip("extract", GREY, 24).move_to([xs[2], 1.6, 0])
        self.play(FadeIn(drop3, shift=DOWN * 0.1), run_time=0.3)
        cross = Cross(drop3, stroke_color=GREY, stroke_width=4, scale_factor=1.0)
        self.play(Create(cross), run_time=0.3)
        self.play(FadeOut(drop3), FadeOut(cross), run_time=0.3)
        tag2 = T("no nodules", 28, GREY).move_to([xs[2], -2.75, 0])
        self.at("no nodules and no gain")
        self.play(FadeIn(tag2), run_time=0.4)
        self.at("A living agent")
        box = bchip("a living agent from soil, tied to the nodules", PURPLE, 28).move_to([0, 3.2, 0])
        self.play(FadeOut(names[1]), FadeIn(box, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
CELL_C = [1.4, -0.2, 0]
ROOT_X = -4.8


def nodule_cell():
    cell = RoundedRectangle(corner_radius=0.25, width=6.0, height=3.4, stroke_color=PURPLE, stroke_width=4,
                            fill_color=PURPLE, fill_opacity=0.08).move_to(CELL_C)
    lbl = T("nodule cell", 24, PURPLE).move_to([1.4, -2.25, 0])
    return VGroup(cell, lbl)


def root_block():
    root = RoundedRectangle(corner_radius=0.2, width=2.8, height=3.4, stroke_color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.12).move_to([ROOT_X, -0.2, 0])
    return VGroup(root, T("root cell", 24, GREEN).move_to([ROOT_X, -2.25, 0]))


class S04Nodule(SpokenScene):
    def construct(self):
        head = T("Beijerinck, same year: bacteria isolated from nodules", 26, GREY).to_edge(UP, buff=0.4)
        root = root_block()
        nod = nodule_cell()
        self.at("did not name")
        self.play(FadeIn(head), FadeIn(root), FadeIn(nod), run_time=1.0)
        self.at("rhizobia")
        rh = bchip("rhizobium", PURPLE, 28).move_to([ROOT_X, 2.4, 0])
        self.play(FadeIn(rh, shift=DOWN * 0.2), run_time=0.5)
        self.at("They enter the root")
        self.play(rh.animate.move_to([ROOT_X, 0.5, 0]), run_time=0.8)
        self.at("Inside nodule cells")
        self.play(rh.animate.move_to([-0.2, 0.5, 0]), run_time=0.9)
        self.at("bacteroids")
        bac = bchip("bacteroid", PURPLE, 28).move_to([-0.2, 0.5, 0])
        self.play(ReplacementTransform(rh, bac), run_time=0.7)
        self.at("an enzyme called nitrogenase")
        enz = bchip("nitrogenase", PINK, 26).move_to([2.5, 0.5, 0])
        arrb = arr(bac.get_right(), enz.get_left(), PURPLE, 4)
        self.play(GrowArrow(arrb), FadeIn(enz, shift=LEFT * 0.2), run_time=0.7)
        self.at("reduces nitrogen gas to ammonia")
        n2 = bchip("nitrogen gas", BLUE, 26).move_to([2.5, 2.4, 0])
        a_in = arr([2.5, 2.05, 0], [2.5, 0.95, 0], BLUE, 5)
        nh = bchip("ammonia", BLUE, 26).move_to([2.5, -1.0, 0])
        a_out = arr([2.5, 0.05, 0], [2.5, -0.55, 0], BLUE, 5)
        self.play(FadeIn(n2, shift=DOWN * 0.2), GrowArrow(a_in), run_time=0.6)
        self.play(GrowArrow(a_out), FadeIn(nh, shift=DOWN * 0.2), run_time=0.6)
        self.at("The root itself makes no")
        none = bchip("no nitrogenase", GREY, 24).move_to([ROOT_X, -0.7, 0])
        self.play(FadeIn(none, scale=0.9), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Oxygen(SpokenScene):
    def construct(self):
        root = root_block()
        nod = nodule_cell()
        bac = bchip("bacteroid", PURPLE, 28).move_to([-0.2, 0.5, 0])
        enz = bchip("nitrogenase", PINK, 26).move_to([2.3, 0.5, 0])
        self.play(FadeIn(root), FadeIn(nod), FadeIn(bac), FadeIn(enz), run_time=0.8)
        self.at("the plant supplies carbon")
        suc = bchip("sucrose", GOLD, 26).move_to([ROOT_X, 2.4, 0])
        self.play(FadeIn(suc, shift=DOWN * 0.2), run_time=0.5)
        self.at("Sucrose from the leaves")
        self.play(suc.animate.move_to([ROOT_X, 1.0, 0]), run_time=0.7)
        self.at("converted to malate")
        mal = bchip("malate", GOLD, 26).move_to([ROOT_X, 0.5, 0])
        self.play(ReplacementTransform(suc, mal), run_time=0.7)
        self.at("fuels the bacteroids")
        am = arr([ROOT_X + 1.15, 0.5, 0], bac.get_left() + LEFT * 0.05, GOLD, 4)
        self.play(GrowArrow(am), run_time=0.5)
        self.play(Indicate(bac, color=GOLD), run_time=0.7)
        self.at("Oxygen damages")
        g = gauge(5.7, -1.5, 2.4, 0.05, w=0.4)
        gl = T("free O2", 22, RED).move_to([5.7, -1.85, 0])
        self.play(FadeIn(g), FadeIn(gl), run_time=0.4)
        o2a = bchip("O2", RED, 24).move_to([3.9, 2.4, 0])
        o2b = bchip("O2", RED, 24).move_to([2.6, 2.4, 0])
        self.play(FadeIn(o2a, shift=DOWN * 0.1), FadeIn(o2b, shift=DOWN * 0.1), run_time=0.4)
        self.play(o2a.animate.move_to([2.3, -0.35, 0]), o2b.animate.move_to([-0.3, -0.35, 0]),
                  level_to(g, 0.9, RED), run_time=0.9)
        wl = T("without\nleghemoglobin", 22, RED, line_spacing=0.6).move_to([5.7, 1.45, 0])
        self.play(FadeIn(wl), Indicate(enz, color=RED, scale_factor=1.1), run_time=0.7)
        self.at("yet the bacteroids respire")
        self.play(Indicate(bac, color=RED, scale_factor=1.1), run_time=0.7)
        self.at("leghemoglobin")
        leg = bchip("leghemoglobin", TEAL, 26).move_to([1.0, -1.3, 0])
        self.play(FadeIn(leg, shift=UP * 0.2), FadeOut(wl), run_time=0.6)
        self.at("binds oxygen")
        self.play(o2a.animate.move_to([1.0, -1.3, 0]).set_opacity(0), o2b.animate.move_to([1.0, -1.3, 0]).set_opacity(0),
                  level_to(g, 0.2, RED), run_time=1.0)
        low = T("low,\nsteady", 22, RED, line_spacing=0.6).move_to([5.7, 1.4, 0])
        self.play(FadeIn(low), run_time=0.3)
        self.at("keep oxygen out")
        o3 = bchip("O2", RED, 24).move_to([3.9, 2.4, 0])
        self.play(FadeIn(o3), run_time=0.2)
        self.play(o3.animate.move_to([1.0, -1.3, 0]).set_opacity(0), run_time=1.0)
        self.at("In Lotus")
        head = T("Lotus japonicus: leghemoglobin silenced", 26, GREY).to_edge(UP, buff=0.4)
        crossleg = Cross(leg, stroke_color=GREY, stroke_width=4)
        self.play(FadeIn(head), FadeOut(low), leg.animate.set_opacity(0.35), Create(crossleg), run_time=0.6)
        self.at("raised free oxygen")
        self.play(level_to(g, 0.95, RED), run_time=0.9)
        self.at("fixation stopped")
        crossenz = Cross(enz, stroke_color=GREY, stroke_width=4)
        stop = T("fixation stops", 28, GREY).move_to([2.3, 2.3, 0])
        self.play(enz.animate.set_opacity(0.35), Create(crossenz), FadeIn(stop), run_time=0.7)
        self.at("grew normally only when given")
        mn = bchip("grew normally only with mineral nitrogen", BLUE, 26).move_to([0.8, -3.15, 0])
        self.play(FadeIn(mn, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        ox, px, top = -3.4, 3.2, 0.4
        oatp, peap = pot(ox, top, w=3.4), pot(px, top, w=3.4)
        oat = plant(ox, ORANGE, 1.5, top)
        pea = plant(px, GREEN, 1.7, top, nodules=1.0)
        ol = T("oat", 30, ORANGE, weight=BOLD).next_to(oatp, DOWN, buff=0.2)
        pl = T("pea, with a bacterial partner", 28, GREEN, weight=BOLD).next_to(peap, DOWN, buff=0.2)
        self.at("Oats and barley have no nodules")
        no = T("no nodules", 28, GREY).move_to([ox, 3.15, 0])
        self.play(FadeIn(oatp), FadeIn(oat), FadeIn(ol), FadeIn(no), run_time=0.9)
        self.at("nitrate and ammonium")
        c1 = bchip("nitrate", YELLOW, 24).move_to([ox - 0.7, top - 0.55, 0])
        c2 = bchip("ammonium", YELLOW, 24).move_to([ox + 0.5, top - 1.25, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.2), FadeIn(c2, shift=DOWN * 0.2), run_time=0.8)
        self.at("oats had only the nitrate")
        self.play(FadeOut(c2), Indicate(c1, color=YELLOW), run_time=0.8)
        self.at("A plant cannot make an element")
        r1 = T("A plant cannot make an element.", 34, TEXT, font=TITLE_FONT).move_to([0, -2.45, 0])
        self.play(Write(r1), run_time=1.2)
        self.at("alone or with a partner")
        ol2 = T("oat, alone", 30, ORANGE, weight=BOLD).next_to(oatp, DOWN, buff=0.2)
        self.play(FadeIn(peap), FadeIn(pea), FadeIn(pl), ReplacementTransform(ol, ol2), run_time=0.7)
        gas = bchip("nitrogen gas", BLUE, 24).move_to([px, 3.15, 0])
        ag = arr([px, 2.82, 0], [px, 2.45, 0], BLUE, 4)
        self.play(FadeIn(gas), GrowArrow(ag), run_time=0.7)
        r2 = T("It must take each one in, alone or with a partner.", 32, GOLD, font=TITLE_FONT).move_to([0, -3.15, 0])
        self.play(Write(r2), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Peas borrow nitrogen from bacteria; oats had only their nitrate."
