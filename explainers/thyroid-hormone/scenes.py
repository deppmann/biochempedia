"""Thyroid hormone: tissues decide what T4 becomes  (Biochemistrypedia explainer, Physiology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = T4 (thyroxine, the prohormone)
  GREEN  = T3 (the active hormone), "on", "normal", "same result"
  RED    = reverse T3, "off", inactive, the crossed-out gland, a fall
  YELLOW = an iodine atom (the small "I" badge) and the open question
  PURPLE = deiodinase enzymes (D1, D2, D3)
  ORANGE = radioactive label (the tracer)
  TEAL   = the thyroid hormone receptor
  PINK   = the MCT8 transporter
  GREY   = glands, tissues, cells, blood, outlines, de-emphasized text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color=GREY, fill=0.10, sw=3, pos=(0, 0)):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill).move_to([pos[0], pos[1], 0])


def gland(pos, label="thyroid", w=3.0, h=1.5):
    b = box(w, h, GREY, 0.14, pos=pos)
    return VGroup(b, T(label, 32, TEXT).move_to(b))


def badge(pos):
    c = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=1)
    return VGroup(c, T("I", 28, BG, weight=BOLD).move_to(c)).move_to([pos[0], pos[1], 0])


def ring_block():
    """T4 as a labelled block with two named zones. Not a structure: just 'outer ring' and 'inner ring'."""
    o = box(7.0, 3.4, BLUE, 0.10, 4, pos=(0, 0.6))
    name = T("T4", 40, BLUE, weight=BOLD).move_to([0, 1.9, 0])
    zo = box(3.0, 1.9, GREY, 0.0, 2.5, pos=(-1.75, 0.3))
    zi = box(3.0, 1.9, GREY, 0.0, 2.5, pos=(1.75, 0.3))
    lo = T("outer ring", 28, TEXT).move_to([-1.75, -0.15, 0])
    li = T("inner ring", 28, TEXT).move_to([1.75, -0.15, 0])
    g = VGroup(o, name, zo, zi, lo, li)
    g.o, g.name, g.zo, g.zi = o, name, zo, zi
    return g


OUTER_BADGE = (-1.75, 0.75)
INNER_BADGE = (1.75, 0.75)


class S00Title(TitleCard):
    LESSON = "The thyroid and metabolic rate"
    TITLE = "Tissues decide what T4 becomes"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """No thyroid, only T4 taken, T3 in the blood: where from?"""

    def construct(self):
        g = gland([-4.6, 2.0])
        cross = VGroup(Line(g[0].get_corner(UL), g[0].get_corner(DR), color=RED, stroke_width=5),
                       Line(g[0].get_corner(UR), g[0].get_corner(DL), color=RED, stroke_width=5))
        removed = T("removed", 28, RED).next_to(g, DOWN, buff=0.2)
        self.at("thyroid removed")
        self.play(FadeIn(g), run_time=0.5)
        self.play(Create(cross), FadeIn(removed), run_time=0.6)

        blood = box(9.6, 2.2, GREY, 0.08, pos=(1.5, -1.2))
        blood_l = T("blood", 28, GREY).move_to([-2.5, -0.5, 0])
        t4 = bchip("T4", BLUE, 38).move_to([-5.3, -1.2, 0])
        t4_l = T("only T4 taken", 24, BLUE).next_to(t4, DOWN, buff=0.2)
        a1 = arr([-4.5, -1.2, 0], [-3.1, -1.2, 0], BLUE)
        self.at("take only thyroxine")
        self.play(FadeIn(t4), FadeIn(t4_l), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(blood), FadeIn(blood_l), run_time=0.6)

        t3 = bchip("T3", GREEN, 40).move_to([3.4, -1.2, 0])
        self.at("the more active hormone")
        self.play(FadeIn(t3, scale=0.8), run_time=0.6)

        q = T("?", 64, YELLOW, weight=BOLD).move_to([0.2, -1.2, 0])
        qa = DashedLine([0.7, -1.2, 0], [2.7, -1.2, 0], color=YELLOW, stroke_width=4, dash_length=0.18)
        self.at("Where does it come")
        self.play(FadeIn(q, scale=0.7), Create(qa), run_time=0.7)

        src = DashedLine([-3.0, 1.6, 0], [3.1, -0.4, 0], color=RED, stroke_width=4, dash_length=0.2)
        src_l = T("gland as the only source", 24, RED).move_to([2.9, 1.4, 0])
        self.at("the only source")
        self.play(Create(src), FadeIn(src_l), run_time=0.8)
        none_l = T("no T3 expected", 28, RED, weight=BOLD).move_to([3.4, 0.7, 0])
        self.at("there should be none")
        self.play(FadeIn(none_l), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Prohormone(SpokenScene):
    """The gland secretes mostly T4; at the receptor T4 grips weakly and T3 grips strongly."""

    def construct(self):
        g = gland([-4.6, 2.0])
        t4 = bchip("T4", BLUE, 40).move_to([-2.2, 2.0, 0])
        most = T("mostly", 26, BLUE).next_to(t4, UP, buff=0.15)
        self.at("secretes mostly")
        self.play(FadeIn(g), run_time=0.5)
        self.play(FadeIn(t4, shift=RIGHT * 0.4), FadeIn(most), run_time=0.6)

        cell = box(7.7, 4.6, GREY, 0.07, pos=(2.45, -0.6))
        cell_l = T("inside the cell", 24, GREY).move_to([0.6, 1.3, 0])
        rec = box(3.0, 2.8, TEAL, 0.25, 4, pos=(4.6, -0.7))
        rec_l = T("thyroid hormone\nreceptor", 22, TEAL, line_spacing=0.8).move_to(rec)
        self.at("thyroid hormone receptor")
        self.play(FadeIn(cell), FadeIn(cell_l), run_time=0.5)
        self.play(FadeIn(rec), FadeIn(rec_l), FadeOut(most), run_time=0.6)

        self.at("much more")
        self.play(t4.animate.move_to([2.35, -1.5, 0]), run_time=1.0)
        gap = DashedLine([2.95, -1.5, 0], [3.08, -1.5, 0], color=GREY, stroke_width=2, dash_length=0.05)
        weak = T("weaker grip", 24, BLUE).move_to([1.8, -2.25, 0])
        self.play(FadeIn(weak), Create(gap), run_time=0.4)

        t3 = bchip("T3", GREEN, 36).move_to([0.2, 0.05, 0])
        self.at("than")
        self.play(FadeIn(t3, scale=0.8), run_time=0.4)
        self.play(t3.animate.move_to([2.35, 0.05, 0]), run_time=0.7)
        grip = Line([2.9, 0.05, 0], [3.1, 0.05, 0], color=GREEN, stroke_width=10)
        strong = T("stronger grip", 24, GREEN).move_to([1.7, 0.7, 0])
        self.play(Create(grip), FadeIn(strong), run_time=0.4)

        pro = T("prohormone", 24, BLUE).move_to([0.0, -1.5, 0])
        self.at("best treated")
        self.play(FadeIn(pro, shift=RIGHT * 0.2), run_time=0.5)

        tr = T("regulates transcription", 22, TEAL).move_to([4.6, -2.5, 0])
        self.at("regulate transcription")
        self.play(FadeIn(tr), run_time=0.5)
        self.at("the form that acts")
        self.play(Indicate(t3, color=GREEN, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rings(SpokenScene):
    """Three deiodinases. Outer ring iodine off: T3 on. Inner ring iodine off: reverse T3 off."""

    def construct(self):
        head = T("Three deiodinases: each removes one iodine", 30, GREY).move_to([0, 3.3, 0])
        blk = ring_block()
        d1 = bchip("D1", PURPLE, 30).move_to([-2.6, -2.1, 0])
        d2 = bchip("D2", PURPLE, 30).move_to([-0.9, -2.1, 0])
        d3 = bchip("D3", PURPLE, 30).move_to([1.75, -2.1, 0])
        self.at("three enzymes")
        self.play(FadeIn(blk), run_time=0.7)
        self.play(FadeIn(head), LaggedStart(FadeIn(d1), FadeIn(d2), FadeIn(d3), lag_ratio=0.3), run_time=1.0)

        # ---- case A: outer ring ------------------------------------------------------
        a1 = arr([-2.6, -1.7, 0], [-2.2, -0.55, 0], PURPLE)
        a2 = arr([-0.9, -1.7, 0], [-1.3, -0.55, 0], PURPLE)
        b = badge(OUTER_BADGE)
        self.at("remove an iodine")
        self.play(GrowArrow(a1), GrowArrow(a2), Indicate(d1, color=PURPLE), Indicate(d2, color=PURPLE), run_time=0.7)
        self.at("outer ring of")
        self.play(blk.zo.animate.set_stroke(YELLOW, 4), FadeIn(b, scale=0.6), run_time=0.5)
        io = T("iodine", 24, YELLOW)
        new3 = T("T3", 40, GREEN, weight=BOLD).move_to(blk.name)
        self.at("That makes")
        self.play(b.animate.move_to([-5.2, 2.7, 0]), blk.zo.animate.set_stroke(GREY, 2.5),
                  Transform(blk.name, new3), blk.o.animate.set_stroke(GREEN).set_fill(GREEN, 0.10), run_time=0.9)
        io.next_to(b, DOWN, buff=0.1)
        self.play(FadeIn(io), run_time=0.3)
        on_tag = bchip("active: on", GREEN, 30).move_to([0, -3.1, 0])
        self.at("switches the hormone on")
        self.play(FadeIn(on_tag, shift=UP * 0.2), run_time=0.5)

        # ---- reset to the neutral state together with the new case ----------------------
        a3 = arr([1.75, -1.7, 0], [1.75, -0.55, 0], PURPLE)
        b2 = badge(INNER_BADGE)
        t4n = T("T4", 40, BLUE, weight=BOLD).move_to([0, 1.9, 0])
        self.at("removes an iodine")
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(b), FadeOut(io), FadeOut(on_tag),
                  Transform(blk.name, t4n), blk.o.animate.set_stroke(BLUE).set_fill(BLUE, 0.10),
                  GrowArrow(a3), Indicate(d3, color=PURPLE), run_time=0.8)
        self.at("inner ring instead")
        self.play(blk.zi.animate.set_stroke(YELLOW, 4), FadeIn(b2, scale=0.6), run_time=0.5)
        io2 = T("iodine", 24, YELLOW)
        newr = T("reverse T3", 34, RED, weight=BOLD).move_to([0, 1.9, 0])
        self.at("reverse")
        self.play(b2.animate.move_to([5.2, 2.7, 0]), blk.zi.animate.set_stroke(GREY, 2.5),
                  Transform(blk.name, newr), blk.o.animate.set_stroke(RED).set_fill(RED, 0.10), run_time=0.9)
        io2.next_to(b2, DOWN, buff=0.1)
        self.play(FadeIn(io2), run_time=0.3)
        off_tag = bchip("inactive: off", RED, 30).move_to([0, -3.1, 0])
        self.at("which is inactive")
        self.play(FadeIn(off_tag, shift=UP * 0.2), run_time=0.5)

        # ---- the rule ---------------------------------------------------------------------
        self.at("The ring that loses")
        on2 = bchip("outer ring: on", GREEN, 28).move_to([-2.4, -3.1, 0])
        off2 = bchip("inner ring: off", RED, 28).move_to([2.4, -3.1, 0])
        self.play(FadeOut(off_tag), FadeOut(b2), FadeOut(io2), FadeOut(a3),
                  Transform(blk.name, t4n.copy()), blk.o.animate.set_stroke(BLUE).set_fill(BLUE, 0.10),
                  blk.zo.animate.set_stroke(GREEN, 4), blk.zi.animate.set_stroke(RED, 4), run_time=0.8)
        self.at("on or off")
        self.play(FadeIn(on2), FadeIn(off2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Tracer(SpokenScene):
    """Braverman, Ingbar and Sterling: labelled T4 in, labelled T3 out; two controls."""

    def construct(self):
        head = T("Braverman, Ingbar and Sterling, 1970", 30, GREY).move_to([0, 3.3, 0])
        self.at("Braverman")
        self.play(FadeIn(head), run_time=0.5)

        pat = box(3.6, 1.8, GREY, 0.12, pos=(-4.7, 1.9))
        pat_t = VGroup(T("13 patients", 28, TEXT), T("treated with T4", 26, BLUE)).arrange(DOWN, buff=0.12).move_to(pat)
        self.at("patients treated")
        self.play(FadeIn(pat), FadeIn(pat_t), run_time=0.6)

        note = VGroup(T("all but two athyreotic", 22, GREY), T("(no functioning thyroid)", 22, GREY),
                      T("or hypothyroid", 22, GREY)).arrange(DOWN, buff=0.1).move_to([-4.7, 0.25, 0])
        self.at("All but two")
        self.play(FadeIn(note), run_time=0.6)

        ser = box(3.6, 1.8, GREY, 0.12, pos=(0.9, 1.9))
        ser_t = VGroup(T("serum", 28, TEXT), T("separated by", 22, GREY), T("chromatography", 22, GREY)).arrange(DOWN, buff=0.06).move_to(ser)
        tr = bchip("T4", BLUE, 30).move_to([-2.1, 1.9, 0])
        trl = T("labelled", 22, ORANGE).next_to(tr, UP, buff=0.15)
        dot = Circle(radius=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(tr[1].get_corner(UR))
        self.at("They gave")
        self.play(FadeIn(tr, shift=RIGHT * 0.3), FadeIn(trl), FadeIn(dot), run_time=0.6)
        a1 = arr([-1.6, 1.9, 0], [-1.0, 1.9, 0], GREY)
        self.at("separated")
        self.play(FadeIn(ser), FadeIn(ser_t), GrowArrow(a1), run_time=0.7)

        res = box(2.4, 1.8, GREEN, 0.12, pos=(5.1, 1.9))
        res_t = VGroup(T("labelled", 22, ORANGE), T("T3", 40, GREEN, weight=BOLD)).arrange(DOWN, buff=0.08).move_to(res)
        a2 = arr([2.8, 1.9, 0], [3.8, 1.9, 0], GREEN)
        self.at("appeared")
        self.play(GrowArrow(a2), FadeIn(res), FadeIn(res_t), run_time=0.7)

        c1 = box(6.0, 2.4, GREY, 0.08, pos=(-3.2, -2.25))
        c1_t = VGroup(T("purified tracer", 28, TEXT), T("less than 0.1 percent T3", 26, TEXT),
                      T("same result", 28, GREEN, weight=BOLD)).arrange(DOWN, buff=0.15).move_to(c1)
        self.at("A specially")
        self.play(FadeIn(c1), FadeIn(c1_t[0]), run_time=0.5)
        self.at("held less than")
        self.play(FadeIn(c1_t[1]), run_time=0.4)
        self.at("gave the same result")
        self.play(FadeIn(c1_t[2]), run_time=0.4)

        c2 = box(6.0, 2.4, GREY, 0.08, pos=(3.2, -2.25))
        c2_t = VGroup(T("2 more patients: T4 into a vein", 26, TEXT), T("gut bypassed", 26, TEXT),
                      T("labelled T3 still appeared", 28, GREEN, weight=BOLD)).arrange(DOWN, buff=0.15).move_to(c2)
        self.at("In two more patients")
        self.play(FadeIn(c2), FadeIn(c2_t[0]), run_time=0.5)
        self.at("bypassing")
        self.play(FadeIn(c2_t[1]), run_time=0.4)
        self.at("still appeared")
        self.play(FadeIn(c2_t[2]), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Result(SpokenScene):
    """Conversion outside the thyroid, in humans; what was not shown; the later, approximate figure."""

    def construct(self):
        head = T("conversion outside the thyroid, in humans", 30, GREY).move_to([0, 3.3, 0])
        g = gland([-4.9, 1.7], w=2.6, h=1.4)
        tis = box(6.4, 1.9, GREY, 0.10, pos=(2.0, 1.7))
        tis_l = T("human tissues outside the thyroid", 24, GREY).move_to([2.0, 2.4, 0])
        t4 = bchip("T4", BLUE, 30).move_to([-2.75, 1.7, 0])
        self.at("ruled in conversion")
        self.play(FadeIn(head), FadeIn(g), FadeIn(tis), FadeIn(tis_l), run_time=0.7)
        self.play(FadeIn(t4), run_time=0.3)
        self.play(t4.animate.move_to([0.0, 1.45, 0]), run_time=0.8)
        t3 = bchip("T3", GREEN, 30).move_to([3.7, 1.45, 0])
        arrow = arr([0.8, 1.45, 0], [3.0, 1.45, 0], GREEN)
        self.play(GrowArrow(arrow), FadeIn(t3, scale=0.8), run_time=0.7)

        u1 = bchip("enzyme: ?", GREY, 28).move_to([-4.3, -0.3, 0])
        u2 = bchip("organ: ?", GREY, 28).move_to([-1.5, -0.3, 0])
        ul = T("not identified", 24, GREY).move_to([-2.9, -1.0, 0])
        self.at("did not identify")
        self.play(FadeIn(u1), FadeIn(u2), FadeIn(ul), run_time=0.6)
        u3 = bchip("how much T3: ?", GREY, 28).move_to([3.1, -0.3, 0])
        ul3 = T("not measured", 24, GREY).move_to([3.1, -1.0, 0])
        self.at("did not measure")
        self.play(FadeIn(u3), FadeIn(ul3), run_time=0.6)

        cap = T("share of T3 made outside the thyroid", 26, TEXT).move_to([0, -1.75, 0])
        outl = RoundedRectangle(corner_radius=0.1, width=10.0, height=0.7, stroke_color=GREY, stroke_width=3).move_to([0, -2.4, 0])
        fill = Rectangle(width=8.0, height=0.7, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
        fill.align_to(outl, LEFT).align_to(outl, UP)
        fl = T("roughly 80 percent", 26, BG, weight=BOLD).move_to(fill)
        self.at("Later work")
        self.play(*[m.animate.set_opacity(0.3) for m in (u1, u2, u3, ul, ul3)], FadeIn(cap), FadeIn(outl), run_time=0.5)
        self.play(GrowFromEdge(fill, LEFT), run_time=0.8)
        self.play(FadeIn(fl), run_time=0.3)
        ap = T("approximate: later work, healthy people with enough iodine", 24, GREY).move_to([0, -3.15, 0])
        self.at("approximate estimate")
        self.play(FadeIn(ap), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Cell(SpokenScene):
    """MCT8 lets hormone in, D2 makes T3 inside the cell; plasma and cell T3 may differ; the mouse; the rule."""

    def construct(self):
        mem = RoundedRectangle(corner_radius=0.1, width=0.35, height=4.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([-1.6, 0.6, 0])
        cell = box(7.9, 4.4, GREY, 0.07, pos=(2.35, 0.6))
        blood_l = T("blood", 28, GREY).move_to([-4.0, 2.4, 0])
        cell_l = T("cell", 28, GREY).move_to([0.3, 2.4, 0])
        t4 = bchip("T4", BLUE, 36).move_to([-4.2, 0.6, 0])
        self.at("diffuse into cells")
        self.play(FadeIn(cell), FadeIn(mem), FadeIn(blood_l), FadeIn(cell_l), FadeIn(t4), run_time=0.7)
        mct = box(0.8, 1.3, PINK, 0.4, 3, pos=(-1.6, 0.6))
        mct_l = T("MCT8", 26, PINK).move_to([-2.5, 1.7, 0])
        self.at("transporters")
        self.play(FadeIn(mct), FadeIn(mct_l), run_time=0.5)
        self.play(t4.animate.move_to([1.2, 0.6, 0]), run_time=1.2)

        d2 = bchip("D2", PURPLE, 32).move_to([4.2, 1.6, 0])
        da = arr([3.6, 1.35, 0], [2.0, 0.75, 0], PURPLE)
        t3 = bchip("T3", GREEN, 36).move_to([1.2, 0.6, 0])
        self.at("Inside the cell")
        self.play(FadeIn(d2), run_time=0.4)
        self.at("makes")
        self.play(GrowArrow(da), Transform(t4, t3), run_time=0.8)

        sa = bchip("T3 in plasma", GREEN, 26).move_to([-2.9, -2.7, 0])
        sm = T("need not match", 28, GREY).move_to([0.15, -2.7, 0])
        sb = bchip("T3 in the cell", GREEN, 26).move_to([3.5, -2.7, 0])
        self.at("need not match")
        self.play(FadeIn(sa), FadeIn(sb), run_time=0.5)
        self.play(FadeIn(sm), run_time=0.4)

        # ---- the mouse ---------------------------------------------------------------------
        title = T("Mice lacking D2, in the cold", 42, TEXT).move_to([0, 2.8, 0])
        rows = []
        specs = [("body temperature", "fell", RED, 1.1), ("brown fat heat", "less", RED, -0.4), ("plasma T3", "normal", GREEN, -1.9)]
        for lab, res, col, y in specs:
            l = T(lab, 38, TEXT)
            l.move_to([1.2 - l.width / 2, y, 0])
            if col == RED:
                ic = arr([2.1, y + 0.4, 0], [2.1, y - 0.4, 0], RED, w=8)
            else:
                ic = VGroup(Line([1.8, y + 0.1, 0], [2.4, y + 0.1, 0], color=GREEN, stroke_width=7),
                            Line([1.8, y - 0.1, 0], [2.4, y - 0.1, 0], color=GREEN, stroke_width=7))
            c = bchip(res, col, 38)
            c.move_to([2.9 + c.width / 2, y, 0])
            rows.append((l, ic, c))
        self.at("In mice lacking")
        self.play(*[FadeOut(m) for m in (cell, mem, blood_l, cell_l, t4, mct, mct_l, d2, da, sa, sm, sb)], run_time=0.6)
        self.play(FadeIn(title), run_time=0.4)
        self.at("body temperature fell")
        self.play(FadeIn(rows[0][0]), GrowArrow(rows[0][1]), FadeIn(rows[0][2]), run_time=0.6)
        self.at("brown fat made less heat")
        self.play(FadeIn(rows[1][0]), GrowArrow(rows[1][1]), FadeIn(rows[1][2]), run_time=0.6)
        self.at("was normal")
        self.play(FadeIn(rows[2][0]), FadeIn(rows[2][1]), FadeIn(rows[2][2]), run_time=0.6)

        # ---- the rule ------------------------------------------------------------------------
        blk = ring_block()
        self.at("Keep the rule")
        self.play(*[FadeOut(m) for m in [title] + [x for r in rows for x in r]], run_time=0.5)
        self.play(FadeIn(blk), run_time=0.6)
        self.at("loses its iodine")
        self.play(blk.zo.animate.set_stroke(GREEN, 4), blk.zi.animate.set_stroke(RED, 4), run_time=0.5)
        on = bchip("on", GREEN, 36).move_to([-1.75, -2.1, 0])
        off = bchip("off", RED, 36).move_to([1.75, -2.1, 0])
        self.at("on or off")
        self.play(FadeIn(on), FadeIn(off), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "The ring that loses its iodine decides: on or off."
