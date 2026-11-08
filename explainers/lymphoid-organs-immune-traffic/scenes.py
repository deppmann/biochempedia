"""Lymphoid organs and immune traffic: cells go around, exit sets the stay  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the lymphocyte (the cell that travels, and the thing counted)
  RED    = blood (blood vessels, the venule, entry from blood)
  BLUE   = lymph (lymphatic vessels, the thoracic duct, efferent lymph)
  PURPLE = the entry machinery (L-selectin, chemokine signal, LFA-1, ICAM)
  TEAL   = S1P and its receptor S1P1 (the exit machinery)
  ORANGE = exit blocked or slowed (cells lacking S1P1, CD69 removing S1P1, the slowed exit)
  GREEN  = the number of cells held (bars, the held count)
  GREY   = organ blocks, axes, labels, de-emphasized
Only labelled blocks, arrows, bars and plots. Numbers on screen are the lesson's own: more than 90 percent
(large animals, at rest); spleen exit rate constant 0.007 per min (fitted rat model); about 2.4 h spleen,
about 10 h subcutaneous node, about 26 s per pass in blood; held relative to blood 8.0 and 15.3 (model keeps
only blood, spleen and subcutaneous nodes). The two output curves in scenes 1 and 2 are sketches, not data.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CELL, BLOOD, LYMPH, ENTRY, S1P, BRAKE, HELD = YELLOW, RED, BLUE, PURPLE, TEAL, ORANGE, GREEN


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(np.array(a, float), np.array(b, float), buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def block(w, h, color=GREY, fill=0.10, at=(0, 0, 0), sw=3):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill).move_to(at)


def sblock(w, h, color=GREY, fill=0.10, at=(0, 0, 0), sw=3):
    """block with an opaque backing, so cells passing behind it are hidden."""
    back = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_width=0, fill_color=BG,
                            fill_opacity=1).move_to(at)
    return VGroup(back, block(w, h, color, fill, at, sw))


def xmark(pos, s=0.3, color=ORANGE):
    x, y = pos
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=7),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=7))


def cell(pos, r=0.2, op=0.9):
    return Circle(radius=r, stroke_color=CELL, stroke_width=2.5, fill_color=CELL, fill_opacity=op).move_to(pos)


def flow(sc, pts, n=4, total=2.0, r=0.13, fade=True):
    """Dots (cells) travelling along a polyline, one after another."""
    path = VMobject().set_points_as_corners([np.array(p, float) for p in pts])
    dots = VGroup(*[cell(pts[0], r) for _ in range(n)])
    for d in dots:
        d.set_opacity(0)
        d.set_z_index(-1)
    sc.add(dots)
    anims = [Succession(ApplyMethod(d.set_opacity, 1, run_time=0.01),
                        MoveAlongPath(d, path, rate_func=linear, run_time=1.0)) for d in dots]
    sc.play(LaggedStart(*anims, lag_ratio=0.28), run_time=total)
    if fade:
        sc.play(FadeOut(dots), run_time=0.2)
        sc.remove(dots)
    return dots


def axes_box(x0, y0, w, h, xlabel="days of drainage", ylabel="duct output"):
    """Hand-made axes (no LaTeX, no tick numbers: these are sketches). Returns (group, map(fx, fy) -> point)."""
    xa = Arrow([x0, y0, 0], [x0 + w, y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.16)
    ya = Arrow([x0, y0, 0], [x0, y0 + h, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.16)
    xl = T(xlabel, 22, GREY).next_to(xa, DOWN, buff=0.15)
    yl = T(ylabel, 22, GREY).move_to([x0 + 0.1, y0 + h + 0.33, 0]).align_to([x0 - 0.1, 0, 0], LEFT)
    g = VGroup(xa, ya, xl, yl)
    return g, (lambda fx, fy: np.array([x0 + 0.12 + fx * (w - 0.35), y0 + 0.1 + fy * (h - 0.4), 0]))


def curve(pts, color=CELL, w=5):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_smoothly([np.array(p, float) for p in pts])
    return m


class S00Title(TitleCard):
    LESSON = "Lymphoid organs and immune traffic"
    TITLE = "Cells go around, exit sets the stay"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """A drained duct runs short of lymphocytes; two ideas make two predictions: flat or empty."""

    def construct(self):
        cy = -0.2
        hdr = T("a rat, thoracic duct drained for a few days", 26, GREY).move_to([0, 3.1, 0])

        def two(a, b, col):
            return VGroup(T(a, 34, col), T(b, 34, col)).arrange(DOWN, buff=0.08)

        nodes = sblock(3.0, 2.4, GREY, 0.10, at=(-4.6, cy, 0))
        nl = two("lymph", "nodes", GREY).move_to(nodes)
        duct = sblock(3.0, 2.4, LYMPH, 0.14, at=(0.0, cy, 0))
        dl = two("thoracic", "duct", LYMPH).move_to(duct)
        coll = sblock(3.0, 2.4, LYMPH, 0.14, at=(4.6, cy, 0))
        cl = two("collected", "lymph", LYMPH).move_to(coll)
        a1 = arr([-3.05, cy, 0], [-1.55, cy, 0], LYMPH)
        a2 = arr([1.55, cy, 0], [3.05, cy, 0], LYMPH)
        path = [(-3.0, cy, 0), (3.0, cy, 0)]

        self.play(FadeIn(hdr), FadeIn(nodes), FadeIn(nl), FadeIn(duct), FadeIn(dl), GrowArrow(a1), GrowArrow(a2),
                  FadeIn(coll), FadeIn(cl), run_time=0.9)
        self.at("for a few days")
        flow(self, path, n=8, total=1.7, r=0.16)
        fewer = T("fewer lymphocytes", 28, CELL).move_to([4.6, cy - 1.2 - 0.5, 0])
        self.at("runs short")
        self.play(FadeIn(fewer, shift=UP * 0.1), run_time=0.4)
        flow(self, path, n=2, total=1.3, r=0.16)

        # the usual view: a question mark upstream of the nodes
        q = bchip("?", GREY, 40).move_to([-4.6, 2.0, 0])
        qa = DashedLine([-4.6, 1.6, 0], [-4.6, cy + 1.2 + 0.05, 0], color=GREY, stroke_width=3, dash_length=0.12)
        self.at("The usual view")
        self.play(FadeIn(q), Create(qa), run_time=0.5)
        made = bchip("made here", GREY, 30).move_to(q)
        self.at("nodes made")
        self.play(ReplacementTransform(q, made), run_time=0.5)

        # prediction panels
        stage = Group(hdr, nodes, nl, duct, dl, coll, cl, a1, a2, fewer, made, qa)
        titleA = VGroup(T("nodes make the cells,", 28, TEXT), T("release them once", 28, TEXT)).arrange(DOWN, buff=0.1)
        titleB = VGroup(T("the same cells", 28, TEXT), T("go around a loop", 28, TEXT)).arrange(DOWN, buff=0.1)
        titleA.move_to([-3.4, 2.7, 0]); titleB.move_to([3.4, 2.7, 0])
        axA, mA = axes_box(-5.7, -2.3, 4.7, 3.7)
        axB, mB = axes_box(1.1, -2.3, 4.7, 3.7)
        foot = T("lines are sketches, not data", 22, GREY).move_to([0, -3.35, 0])
        self.at("If so")
        self.play(FadeOut(stage), run_time=0.4)
        self.play(FadeIn(titleA), FadeIn(axA), run_time=0.6)
        flat = curve([mA(0, 0.85), mA(0.5, 0.85), mA(1, 0.85)])
        self.at("output should hold")
        self.play(Create(flat), run_time=1.0)
        lblA = T("roughly steady", 28, CELL).move_to(mA(0.55, 0.35))
        self.play(FadeIn(lblA), run_time=0.3)
        self.at("If the same cells")
        self.play(FadeIn(titleB), FadeIn(axB), FadeIn(foot), run_time=0.6)
        xs = np.linspace(0, 1, 14)
        fall = curve([mB(x, 0.12 + 0.73 * np.exp(-4.0 * x)) for x in xs])
        self.at("removing them")
        self.play(Create(fall), run_time=1.1)
        lblB = T("empties", 28, CELL).move_to(mB(0.62, 0.55))
        self.at("empty it")
        self.play(FadeIn(lblB), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Loop(SpokenScene):
    """Cannula: output falls; cells returned by vein: output recovers; the loop assembles as it is spoken."""

    def construct(self):
        duct = bchip("thoracic duct", LYMPH, 30).move_to([-0.9, 1.3, 0])
        node = bchip("lymphoid tissue", GREY, 30).move_to([-5.0, 1.3, 0])
        blood = block(8.2, 0.8, BLOOD, 0.18, at=(-2.2, -2.75, 0), sw=3)
        blood_lbl = T("blood", 30, BLOOD).move_to(blood)
        tee_y = -0.7
        down1 = Line([-0.9, 0.9, 0], [-0.9, tee_y, 0], color=LYMPH, stroke_width=5)
        down2 = arr([-0.9, tee_y, 0], [-0.9, -2.35, 0], LYMPH)
        branch = arr([-0.9, tee_y, 0], [0.45, tee_y, 0], LYMPH)
        cann = T("cannula", 22, GREY).move_to([-0.1, tee_y + 0.4, 0])
        coll = bchip("collected", LYMPH, 26).move_to([1.5, tee_y, 0])
        ret = arr([1.5, tee_y - 0.45, 0], [1.5, -2.35, 0], LYMPH)
        retl = T("back by vein", 22, LYMPH).move_to([0.35, -1.6, 0])
        up = arr([-5.0, -2.35, 0], [-5.0, 0.9, 0], BLOOD)
        eff = arr(node.get_right() + RIGHT * 0.05, duct.get_left() + LEFT * 0.05, LYMPH)
        efl = T("efferent lymph", 22, LYMPH).move_to([-3.1, 2.1, 0])
        ax, m = axes_box(3.1, -2.3, 3.1, 3.7, xlabel="days", ylabel="duct output")
        fall = curve([m(0.02 + 0.40 * x, 0.12 + 0.73 * np.exp(-3.6 * x)) for x in np.linspace(0, 1, 12)])
        low = 0.12 + 0.73 * np.exp(-3.6)
        rec = curve([m(0.55 + 0.42 * x, low + (0.82 - low) * (1 - np.exp(-4.0 * x))) for x in np.linspace(0, 1, 12)])
        mark = DashedLine(m(0.50, 0.0), m(0.50, 1.0), color=GREY, stroke_width=3, dash_length=0.12)
        marklbl = T("cells returned", 22, GREY).move_to([5.25, 1.38, 0])
        note = T("sketch, not data", 22, GREY).move_to([4.65, -3.35, 0])

        self.play(FadeIn(duct), Create(down1), run_time=0.7)
        self.at("a fine tube")
        self.play(GrowArrow(branch), FadeIn(cann), FadeIn(coll), run_time=0.7)
        self.at("collected lymph")
        self.play(FadeIn(ax), FadeIn(note), run_time=0.5)
        flow(self, [(-0.9, 0.9, 0), (-0.9, tee_y, 0), (0.45, tee_y, 0)], n=3, total=1.3)
        self.at("Output fell")
        self.play(Create(fall), run_time=1.2)
        self.at("returned the collected")
        self.play(FadeIn(blood), FadeIn(blood_lbl), Create(mark), FadeIn(marklbl), run_time=0.6)
        self.at("by vein")
        self.play(GrowArrow(ret), FadeIn(retl), run_time=0.4)
        self.at("output recovered")
        self.play(Create(rec), run_time=1.0)
        flow(self, [(1.5, tee_y - 0.45, 0), (1.5, -2.35, 0)], n=3, total=1.0)
        self.at("turned up again")
        flow(self, [(-0.9, 0.9, 0), (-0.9, tee_y, 0), (0.45, tee_y, 0)], n=4, total=1.5)
        self.at("going around")
        self.play(Indicate(duct, color=CELL, scale_factor=1.06), run_time=0.5)
        self.at("from blood")
        self.play(GrowArrow(up), run_time=0.6)
        self.at("tissue")
        self.play(FadeIn(node), run_time=0.5)
        self.at("into lymph")
        self.play(GrowArrow(eff), FadeIn(efl), run_time=0.6)
        self.at("back to blood")
        self.play(GrowArrow(down2), run_time=0.5)
        loop = [(-5.0, -2.35, 0), (-5.0, 1.3, 0), (-0.9, 1.3, 0), (-0.9, -2.35, 0)]
        flow(self, loop, n=3, total=3.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Entry(SpokenScene):
    """A node: two entrances (afferent lymph, high endothelial venules), one exit; then the entry sequence."""

    def construct(self):
        node = block(4.6, 3.2, GREY, 0.10, at=(0.5, 0.5, 0))
        nlbl = T("lymph node", 30, GREY).move_to([0.5, 1.7, 0])
        hev = arr([-1.0, -3.15, 0], [-1.0, -1.15, 0], BLOOD, w=10, tip=0.3)
        hevl = VGroup(T("high endothelial", 24, BLOOD), T("venule, from blood", 24, BLOOD)).arrange(DOWN, buff=0.08)
        hevl.move_to([-3.5, -2.2, 0])
        aff = arr([-5.9, 1.2, 0], [-1.85, 1.2, 0], LYMPH, w=3, tip=0.2)
        affl = T("afferent lymph from tissue", 22, LYMPH).move_to([-3.85, 1.7, 0])
        eff = arr([2.85, 0.5, 0], [6.1, 0.5, 0], LYMPH, w=6)
        effl = T("efferent lymphatic", 24, LYMPH).move_to([4.5, 1.05, 0])
        bar_w = 4.2
        bx0 = 1.7
        red = Rectangle(width=0.9 * bar_w, height=0.45, stroke_width=0, fill_color=BLOOD, fill_opacity=0.85)
        rest = Rectangle(width=0.1 * bar_w, height=0.45, stroke_width=0, fill_color=GREY, fill_opacity=0.5)
        sbar = VGroup(red, rest).arrange(RIGHT, buff=0).move_to([bx0 + bar_w / 2, -2.15, 0])
        sl1 = T("entered through the venules:", 24, TEXT).move_to([bx0 + bar_w / 2, -1.5, 0])
        sl2 = T("more than 90 percent", 28, BLOOD, weight=BOLD).move_to([bx0 + bar_w / 2, -2.8, 0])
        sl3 = T("large animals, at rest", 22, GREY).move_to([bx0 + bar_w / 2, -3.25, 0])

        self.play(FadeIn(node), FadeIn(nlbl), GrowArrow(hev), run_time=0.8)
        d = VGroup(*[cell([-1.0, -3.0 + 0.55 * i, 0], 0.13) for i in range(3)])
        self.play(FadeIn(d), run_time=0.3)
        self.at("quickly")
        self.play(*[dd.animate.move_to([-0.3 + 0.55 * i, 0.4 + 0.3 * (i % 2), 0]) for i, dd in enumerate(d)], run_time=1.4)
        self.at("across the walls")
        self.play(FadeIn(hevl), run_time=0.5)
        self.at("two entrances")
        self.play(Indicate(node, color=GREY, scale_factor=1.03), run_time=0.5)
        self.at("entrances", lead=-0.6)
        self.play(GrowArrow(aff), FadeIn(affl), run_time=0.6)
        self.at("these venules")
        self.play(Indicate(VGroup(hev, hevl), color=BLOOD, scale_factor=1.06), run_time=0.7)
        self.at("one exit")
        self.play(GrowArrow(eff), FadeIn(effl), run_time=0.6)
        self.at("of lymphocytes")
        self.play(FadeIn(sl1), FadeIn(sbar), FadeIn(sl2), FadeIn(sl3), run_time=0.7)

        # --- close-up of the venule wall ---------------------------------------------------
        lumen = Rectangle(width=12.4, height=3.2, stroke_width=0, fill_color=BLOOD, fill_opacity=0.12).move_to([0, 1.6, 0])
        wall = Rectangle(width=12.4, height=0.7, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.35).move_to([0, -0.35, 0])
        zone = Rectangle(width=12.4, height=2.5, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                         fill_opacity=0.06).move_to([0, -2.2, 0])
        lum_l = T("blood in the venule", 22, BLOOD).move_to([-4.7, 2.85, 0])
        wall_l = T("venule wall", 22, GREY).move_to([-5.3, -0.35, 0])
        inside = T("inside the node", 22, GREY).move_to([-5.0, -3.0, 0])
        flowa = arr([4.2, 2.85, 0], [5.9, 2.85, 0], BLOOD, w=4, tip=0.2)
        c = cell([-4.8, 1.5, 0], 0.55, 0.9)
        mark = Dot([-4.8, 1.5 + 0.38, 0], radius=0.08, color=BG)
        cg = VGroup(c, mark)
        lsel = bchip("L-selectin", ENTRY, 26).move_to([-4.8, 2.25, 0])
        self.at("tethers", lead=1.1)
        self.play(FadeOut(Group(node, nlbl, hev, hevl, aff, affl, eff, effl, sbar, sl1, sl2, sl3, d)), run_time=0.4)
        self.play(FadeIn(lumen), FadeIn(wall), FadeIn(zone), FadeIn(lum_l), FadeIn(wall_l), FadeIn(inside),
                  FadeIn(flowa), FadeIn(cg), run_time=0.6)
        self.at("cell")
        self.play(FadeIn(lsel, shift=DOWN * 0.1), run_time=0.3)
        self.play(cg.animate.move_to([-4.0, 0.55, 0]), lsel.animate.move_to([-4.0, 1.5, 0]), run_time=0.4)
        self.at("it rolls")
        self.play(cg.animate.shift(RIGHT * 3.5).rotate(-TAU * 1.2), lsel.animate.shift(RIGHT * 3.5),
                  run_time=0.9, rate_func=linear)
        chem = bchip("chemokine signal", ENTRY, 26).move_to([-1.0, 2.3, 0])
        lfa = bchip("LFA-1: low affinity", ENTRY, 26).move_to([4.3, 1.5, 0])
        ic1 = bchip("ICAM-1", ENTRY, 22).move_to([0.4, -0.35, 0])
        ic2 = bchip("ICAM-2", ENTRY, 22).move_to([1.9, -0.35, 0])
        self.at("signal")
        self.play(FadeIn(chem, shift=DOWN * 0.1), FadeIn(lfa), FadeIn(ic1), FadeIn(ic2), run_time=0.6)
        self.play(cg.animate.shift(RIGHT * 0.3).rotate(-TAU * 0.3), lsel.animate.shift(RIGHT * 0.3), run_time=0.4)
        lfa2 = bchip("LFA-1: high affinity", ENTRY, 26, fill_opacity=0.5).move_to([4.3, 1.5, 0])
        self.at("switches")
        self.play(ReplacementTransform(lfa, lfa2), run_time=0.4)
        self.at("grips")
        self.play(cg.animate.move_to([1.15, 0.55, 0]), lsel.animate.move_to([1.15, 1.5, 0]), run_time=0.4)
        g1 = Line(cg[0].get_bottom() + LEFT * 0.2, ic1.get_top() + RIGHT * 0.05, color=ENTRY, stroke_width=6)
        g2 = Line(cg[0].get_bottom() + RIGHT * 0.2, ic2.get_top() + LEFT * 0.05, color=ENTRY, stroke_width=6)
        self.play(Create(g1), Create(g2), ic1[1].animate.set_fill(ENTRY, 0.55), ic2[1].animate.set_fill(ENTRY, 0.55),
                  run_time=0.4)
        self.at("then crosses")
        self.play(FadeOut(Group(chem, lfa2, lsel, g1, g2)), cg.animate.move_to([1.15, -2.0, 0]), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Exit(SpokenScene):
    """S1P high in blood and lymph, low in the tissue; the cell carries S1P1; without S1P1 cells stay."""

    def construct(self):
        zb = block(3.6, 4.4, BLOOD, 0.0, at=(-4.2, 0.0, 0))
        zt = block(3.6, 4.4, GREY, 0.0, at=(0.0, 0.0, 0))
        zl = block(3.6, 4.4, LYMPH, 0.0, at=(4.2, 0.0, 0))
        names = [T("blood", 30, BLOOD).move_to([-4.2, 1.65, 0]), T("lymphoid tissue", 30, GREY).move_to([0.0, 1.65, 0]),
                 T("lymph", 30, LYMPH).move_to([4.2, 1.65, 0])]
        hi1 = T("S1P high", 28, S1P).move_to([-4.2, -1.65, 0])
        lo = T("S1P low", 28, S1P).move_to([0.0, -1.65, 0])
        hi2 = T("S1P high", 28, S1P).move_to([4.2, -1.65, 0])
        self.play(FadeIn(zb), FadeIn(zt), FadeIn(zl), *[FadeIn(n) for n in names], run_time=0.8)
        self.at("is high")
        self.play(zb.animate.set_fill(S1P, 0.35), zl.animate.set_fill(S1P, 0.35), zt.animate.set_fill(S1P, 0.06),
                  FadeIn(hi1), FadeIn(hi2), run_time=0.8)
        self.at("low inside")
        self.play(FadeIn(lo), run_time=0.4)
        c = cell([0.0, -0.1, 0], 0.5)
        rec = bchip("S1P1", S1P, 28).move_to([0.0, 0.8, 0])
        link = Line(rec.get_bottom(), c.get_top(), color=S1P, stroke_width=3)
        self.at("Lymphocytes carry")
        self.play(FadeIn(c), run_time=0.4)
        self.at("receptor for it")
        self.play(FadeIn(rec), Create(link), run_time=0.5)
        ex = VGroup(c, rec, link)
        self.play(ex.animate.shift(RIGHT * 4.2), run_time=1.2)
        exl = T("exit", 28, LYMPH).move_to([4.2, -0.95, 0])
        self.play(FadeIn(exl), run_time=0.3)

        # --- mice without S1P1 ------------------------------------------------------------
        t1 = VGroup(T("mice whose blood-forming", 26, TEXT), T("cells lack S1P1", 26, TEXT)).arrange(DOWN, buff=0.08)
        t2 = VGroup(T("S1P1-deficient T and B cells,", 26, TEXT), T("transferred into normal mice", 26, TEXT)).arrange(DOWN, buff=0.08)
        t1.move_to([-3.5, 2.7, 0]); t2.move_to([3.0, 2.7, 0])
        thy = block(4.4, 3.0, GREY, 0.10, at=(-3.5, 0.3, 0))
        org = block(4.4, 3.0, GREY, 0.10, at=(3.0, 0.3, 0))
        thyl = T("thymus", 30, GREY).move_to([-3.5, 1.35, 0])
        orgl = T("lymphoid organ", 30, GREY).move_to([3.0, 1.35, 0])
        stuck = []
        for cx in (-3.5, 3.0):
            cs = VGroup(*[cell([cx - 1.24 + 0.62 * (i % 5), 0.55 - 0.65 * (i // 5), 0], 0.24) for i in range(10)])
            stuck.append(cs)
        dsh1 = DashedLine([-1.3, 0.3, 0], [-0.1, 0.3, 0], color=BRAKE, stroke_width=6, dash_length=0.16)
        dsh2 = DashedLine([5.2, 0.3, 0], [6.2, 0.3, 0], color=BRAKE, stroke_width=6, dash_length=0.16)
        x1 = xmark((-0.7, 0.3)); x2 = xmark((5.7, 0.3))
        no1 = T("cannot leave", 26, BRAKE).move_to([-3.5, -1.6, 0])
        no2 = T("cannot leave", 26, BRAKE).move_to([3.0, -1.6, 0])
        self.at("In mice")
        self.play(FadeOut(VGroup(zb, zt, zl, *names, hi1, lo, hi2, ex, exl)), run_time=0.5)
        self.play(FadeIn(t1), FadeIn(thy), FadeIn(thyl), run_time=0.6)
        self.at("leave the")
        self.play(LaggedStart(*[FadeIn(x, scale=0.6) for x in stuck[0]], lag_ratio=0.1), run_time=1.0)
        self.play(Create(dsh1), FadeIn(x1), FadeIn(no1), run_time=0.5)
        self.at("transferred into normal mice")
        self.play(FadeIn(t2), FadeIn(org), FadeIn(orgl), run_time=0.6)
        self.at("could not leave", nth=1)
        self.play(LaggedStart(*[FadeIn(x, scale=0.6) for x in stuck[1]], lag_ratio=0.1), run_time=1.0)
        self.play(Create(dsh2), FadeIn(x2), FadeIn(no2), run_time=0.5)
        self.at("itself")
        final = T("the need is in the lymphocyte itself", 32, CELL, weight=BOLD).move_to([0, -2.75, 0])
        self.play(FadeIn(final, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Residence(SpokenScene):
    """Residence time = 1 / exit rate constant; spleen 0.007 per min -> 2.4 h; cells held relative to blood."""

    def construct(self):
        eq1 = VGroup(T("mean residence time =", 34, TEXT), M("1 / exit rate constant", 34, YELLOW)).arrange(RIGHT, buff=0.3)
        eq = VGroup(eq1, T("first-order (constant-fraction) exit", 22, GREY)).arrange(DOWN, buff=0.14)
        eq.move_to([0, 2.55, 0])
        eq_top = eq.copy().move_to([0, 2.95, 0])
        cx = [-4.2, 0.0, 4.2]
        # big spleen worked example (phase 1)
        B1 = T("spleen", 44, TEXT, weight=BOLD).move_to([0, 1.25, 0])
        B2 = T("exit rate constant", 30, GREY).move_to([0, 0.5, 0])
        B3 = M("0.007 per min", 46, TEXT).move_to([0, -0.35, 0])
        B4 = M("1 / 0.007 per min", 38, TEXT).move_to([0, -1.3, 0])
        B5 = VGroup(M("= 143 min, about", 38, YELLOW), M("2.4 h", 38, YELLOW, weight=BOLD)).arrange(RIGHT, buff=0.25).move_to([0, -2.1, 0])
        # column versions (phase 2)
        hb = T("blood", 30, BLOOD, weight=BOLD).move_to([cx[0], 2.0, 0])
        hs = T("spleen", 30, TEXT, weight=BOLD).move_to([cx[1], 2.0, 0])
        hn = VGroup(T("subcutaneous", 28, TEXT, weight=BOLD), T("nodes", 28, TEXT, weight=BOLD)).arrange(DOWN, buff=0.04).move_to([cx[2], 1.95, 0])
        s1 = T("exit rate constant", 22, GREY).move_to([cx[1], 1.4, 0])
        s2 = M("0.007 per min", 28, TEXT).move_to([cx[1], 1.0, 0])
        s3 = M("1 / 0.007 per min", 24, TEXT).move_to([cx[1], 0.55, 0])
        s4 = VGroup(M("= 143 min", 24, YELLOW), M("about 2.4 h", 30, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.12).move_to([cx[1], -0.1, 0])
        n1 = M("about 10 h", 30, YELLOW, weight=BOLD).move_to([cx[2], 0.9, 0])
        b1 = M("about 26 s", 30, YELLOW, weight=BOLD).move_to([cx[0], 1.2, 0])
        b2 = T("per pass", 22, GREY).move_to([cx[0], 0.8, 0])
        base = -2.4
        sc = 0.12
        vals = [1.0, 8.0, 15.3]
        bars = [Rectangle(width=1.5, height=v * sc, stroke_color=HELD, stroke_width=3, fill_color=HELD, fill_opacity=0.35)
                .move_to([x, base + v * sc / 2, 0]) for x, v in zip(cx, vals)]
        nums = [M(t, 28, HELD).move_to([x, base + v * sc + 0.35, 0]) for x, v, t in zip(cx, vals, ["1", "8.0", "15.3"])]
        axis = Line([-5.6, base, 0], [5.6, base, 0], color=GREY, stroke_width=3)
        held_l = VGroup(T("cells held at steady state,", 22, HELD), T("relative to blood = 1", 22, HELD)).arrange(DOWN, buff=0.06)
        held_l.move_to([cx[0], -0.75, 0])
        foot = VGroup(T("pool comparison omits other organs and cell loss;", 22, GREY),
                      T("blood transit uses the full model, including lung and liver", 22, GREY)).arrange(DOWN, buff=0.06).move_to([0, -3.1, 0])

        org = sblock(4.4, 2.4, GREY, 0.10, at=(-1.2, -0.2, 0))
        orgl = T("a lymphoid organ", 28, GREY).move_to([-1.2, 0.65, 0])
        ocells = VGroup(*[cell([-2.6 + 0.6 * (i % 4), -0.15 - 0.55 * (i // 4), 0], 0.2) for i in range(8)])
        oext = arr([1.0, -0.2, 0], [4.4, -0.2, 0], LYMPH, w=7)
        oextl = T("exit", 28, LYMPH).move_to([2.7, 0.25, 0])
        stay = T("how long a cell stays", 32, YELLOW).move_to([-1.2, -2.0, 0])
        og = Group(org, orgl, ocells, oext, oextl, stay)
        og.scale(1.3).move_to([0, -0.3, 0])
        oy = oext.get_start()[1]
        opath = [(oext.get_start()[0] - 1.4, oy, 0), (oext.get_end()[0] - 0.15, oy, 0)]
        self.play(FadeIn(org), FadeIn(orgl), FadeIn(ocells), GrowArrow(oext), FadeIn(oextl), run_time=0.8)
        self.at("how long a cell stays")
        self.play(FadeIn(stay, shift=UP * 0.1), run_time=0.4)
        flow(self, opath, n=3, total=0.9, r=0.2)
        self.at("The mean residence")
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.7)
        self.at("fitted")
        self.play(FadeOut(og), FadeIn(B1), FadeIn(B2), run_time=0.5)
        self.at("rate constant is")
        self.play(FadeIn(B3), run_time=0.5)
        self.at("That gives")
        self.play(FadeIn(B4, shift=UP * 0.1), run_time=0.5)
        self.at("hours")
        self.play(FadeIn(B5), run_time=0.6)
        self.at("nodes together hold")
        self.play(Transform(eq, eq_top), ReplacementTransform(B1, hs), ReplacementTransform(B2, s1),
                  ReplacementTransform(B3, s2), ReplacementTransform(B4, s3), ReplacementTransform(B5, s4),
                  FadeIn(hn), FadeIn(n1), run_time=1.0)
        self.at("and blood")
        self.play(FadeIn(hb), FadeIn(b1), FadeIn(b2), run_time=0.5)
        self.at("At steady state")
        self.play(FadeIn(axis), FadeIn(held_l), FadeIn(foot), run_time=0.5)
        self.at("the spleen holds")
        self.play(GrowFromEdge(bars[0], DOWN), FadeIn(nums[0]), run_time=0.4)
        self.play(GrowFromEdge(bars[1], DOWN), FadeIn(nums[1]), run_time=0.9)
        self.at("cells the")
        self.play(GrowFromEdge(bars[2], DOWN), FadeIn(nums[2]), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Draining(SpokenScene):
    """CD69 removes S1P1, exit slows: with entry unchanged, residence and cells held scale together."""

    def construct(self):
        node = block(4.0, 2.5, GREY, 0.10, at=(-2.2, 0.7, 0))
        nlbl = T("draining node", 26, GREY).move_to([-2.2, 1.55, 0])
        ent = arr([-6.1, 0.7, 0], [-4.25, 0.7, 0], BLOOD, w=6)
        entl = T("from blood", 22, BLOOD).move_to([-5.2, 1.15, 0])
        ext = arr([-0.15, 0.7, 0], [2.0, 0.7, 0], LYMPH, w=7)
        extl = T("exit", 24, LYMPH).move_to([1.0, 1.15, 0])
        xs = [-3.5, -2.95, -2.4, -1.85, -1.3, -0.75]
        dots1 = VGroup(*[cell([xs[i % 3], 0.95 - 0.5 * (i // 3), 0], 0.16) for i in range(6)])
        dots2 = VGroup(*[cell([xs[3 + i % 3], 0.95 - 0.5 * (i // 3), 0], 0.16) for i in range(6)])
        base = -2.5
        b1 = Rectangle(width=1.3, height=1.3, stroke_color=HELD, stroke_width=3, fill_color=HELD, fill_opacity=0.35).move_to([3.6, base + 0.65, 0])
        b2 = Rectangle(width=1.3, height=2.6, stroke_color=HELD, stroke_width=3, fill_color=HELD, fill_opacity=0.35).move_to([5.3, base + 1.3, 0])
        n1 = M("1", 28, HELD).move_to([3.6, base + 1.3 + 0.35, 0])
        n2 = M("2", 28, HELD).move_to([5.3, base + 2.6 + 0.35, 0])
        bl1 = T("before", 22, GREY).move_to([3.6, base - 0.35, 0])
        bl2 = T("if exit halved", 22, GREY).move_to([5.3, base - 0.35, 0])
        bt = VGroup(T("cells held in the node,", 24, HELD), T("relative to before", 24, HELD)).arrange(DOWN, buff=0.06).move_to([4.5, 1.25, 0])
        axis = Line([2.7, base, 0], [6.3, base, 0], color=GREY, stroke_width=3)
        zc = cell([-2.2, -1.95, 0], 0.5)
        zl = T("one lymphocyte, enlarged", 22, GREY).move_to([-2.2, -3.1, 0])
        s1p = bchip("S1P1", S1P, 26).move_to([-3.6, -1.95, 0])
        s1l = Line(s1p.get_right(), zc.get_left(), color=S1P, stroke_width=3)
        cd = bchip("CD69", BRAKE, 26).move_to([-0.2, -1.95, 0])
        c1 = bchip("if exit rate constant ÷ 2", BRAKE, 24)
        c2 = bchip("residence time × 2", CELL, 24)
        c3 = bchip("cells held × 2", HELD, 24)
        chain = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.85).move_to([0, 2.95, 0])
        note = T("a worked example, in this sketch", 22, GREY).move_to([0, 2.3, 0])
        k1 = arr(c1.get_right() + RIGHT * 0.04, c2.get_left() + LEFT * 0.04, GREY, w=4, tip=0.2)
        k2 = arr(c2.get_right() + RIGHT * 0.04, c3.get_left() + LEFT * 0.04, GREY, w=4, tip=0.2)

        self.play(FadeIn(node), FadeIn(nlbl), GrowArrow(ent), FadeIn(entl), GrowArrow(ext), FadeIn(extl), run_time=0.9)
        self.play(FadeIn(dots1), FadeIn(axis), FadeIn(b1), FadeIn(n1), FadeIn(bl1), FadeIn(bt), run_time=0.6)
        self.at("In mouse studies")
        self.play(FadeIn(zc), FadeIn(s1p), Create(s1l), FadeIn(zl), run_time=0.7)
        self.at("express")
        self.play(FadeIn(cd, shift=LEFT * 0.2), run_time=0.5)
        self.at("removes")
        self.play(cd.animate.move_to([-1.15, -1.95, 0]), run_time=0.4)
        self.play(FadeOut(s1p, shift=LEFT * 0.4), FadeOut(s1l), run_time=0.5)
        self.at("Entry from blood")
        self.play(Indicate(VGroup(ent, entl), color=BLOOD, scale_factor=1.08), run_time=0.7)
        self.at("exit slows")
        ext2 = arr([-0.15, 0.7, 0], [2.0, 0.7, 0], BRAKE, w=2.5, tip=0.14)
        extl2 = T("exit slows", 24, BRAKE).move_to([1.0, 1.15, 0])
        self.play(ReplacementTransform(ext, ext2), ReplacementTransform(extl, extl2), run_time=0.6)
        self.at("exit rate constant")
        self.play(FadeIn(c1), FadeIn(note), run_time=0.5)
        self.at("residence time")
        self.play(GrowArrow(k1), FadeIn(c2), run_time=0.5)
        self.at("number held")
        self.play(GrowArrow(k2), FadeIn(c3), run_time=0.4)
        self.play(FadeIn(dots2), GrowFromEdge(b2, DOWN), FadeIn(n2), FadeIn(bl2), run_time=0.9)
        self.at("is transient")
        ext3 = arr([-0.15, 0.7, 0], [2.0, 0.7, 0], LYMPH, w=7)
        extl3 = T("exit resumes", 24, LYMPH).move_to([1.0, 1.15, 0])
        b3 = Rectangle(width=1.3, height=1.3, stroke_color=HELD, stroke_width=3, fill_color=HELD, fill_opacity=0.35).move_to([5.3, base + 0.65, 0])
        n3 = M("1", 28, HELD).move_to([5.3, base + 1.3 + 0.35, 0])
        bl3 = T("exit resumes", 22, GREY).move_to([5.3, base - 0.35, 0])
        self.play(ReplacementTransform(ext2, ext3), ReplacementTransform(extl2, extl3), ReplacementTransform(b2, b3),
                  ReplacementTransform(n2, n3), ReplacementTransform(bl2, bl3), FadeOut(dots2), run_time=0.9)
        self.at("Keep this")
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=0.6)
        rule = VGroup(T("at steady state", 32, GREY), VGroup(T("cells held", 46, HELD, weight=BOLD), T("=", 46, TEXT),
                      T("entry × residence", 46, CELL, weight=BOLD)).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.35).move_to([0, 0.2, 0])
        self.at("cells held equal")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "At steady state, cells held equal entry times residence."
