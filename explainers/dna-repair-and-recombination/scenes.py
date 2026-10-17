"""DNA repair and recombination: DNA holds its information twice  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the original (template, old) DNA strand and the chromosomes
  GREEN  = newly made or repaired DNA (new strand, refilled bases, new synthesis)
  RED    = the wrong base, the lesion, the mismatch, the break
  YELLOW = repair proteins at work (glycosylase, polymerase, ligase, MutS, Ku, Rad51 ...)
  ORANGE = the methyl mark on GATC
  PURPLE = ultraviolet light
  GREY   = not yet known / outlines / de-emphasized
DNA is drawn as letter tiles on a backbone line (two strands, paired by short rungs), never as
a molecular structure.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=YELLOW, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def slash(x, y, color=YELLOW, s=0.26):
    return Line([x - s * 0.55, y + s, 0], [x + s * 0.55, y - s, 0], color=color, stroke_width=7)


class Duplex:
    """Two strands of letter tiles on backbone lines. Index i is a column. side 't' = top strand, 'b' = bottom.

    Parts are kept in lists so a scene can lift one tile out, cut one backbone segment, or put
    new tiles in: tile[side][i], conn[side][i], node[side][i], seg[side][i] (node i to i+1), rung[i].
    """

    def __init__(s, top, bot, cx=0.0, cy=0.0, tcol=BLUE, bcol=BLUE, tc=None, bc=None, tdy=None,
                 sp=1.05, tw=0.9, th=0.8, ty=0.8, by=1.75, fs=34, norung=()):
        s.n = len(top)
        s.cx, s.cy, s.sp, s.tw, s.th, s.ty, s.by, s.fs = cx, cy, sp, tw, th, ty, by, fs
        s.col = {"t": tcol, "b": bcol}
        s.dy = tdy or {}
        tc, bc = tc or {}, bc or {}
        s.over = {"t": tc, "b": bc}
        s.letters = {"t": list(top), "b": list(bot)}
        s.tile = {"t": [], "b": []}
        s.conn = {"t": [], "b": []}
        s.node = {"t": [], "b": []}
        s.seg = {"t": [], "b": []}
        s.rung = []
        for side in "tb":
            for i, ch in enumerate(s.letters[side]):
                s.node[side].append(s.mk_node(side, i))
                if ch is None:
                    s.tile[side].append(None)
                    s.conn[side].append(None)
                else:
                    s.tile[side].append(s.mk_tile(side, i, ch, s.over[side].get(i, s.col[side])))
                    s.conn[side].append(s.mk_conn(side, i))
            for i in range(s.n - 1):
                s.seg[side].append(s.mk_seg(side, i))
        for i in range(s.n):
            if i in norung or s.letters["t"][i] is None or s.letters["b"][i] is None:
                s.rung.append(None)
            else:
                s.rung.append(s.mk_rung(i))
        parts = []
        for side in "tb":
            parts += s.seg[side] + s.conn[side]
        parts += s.rung
        for side in "tb":
            parts += s.node[side]
        for side in "tb":
            parts += s.tile[side]
        s.all = VGroup(*[p for p in parts if p is not None])

    def X(s, i):
        return s.cx + (i - (s.n - 1) / 2) * s.sp

    def ytile(s, side, i):
        return s.cy + (s.ty + s.dy.get(i, 0) if side == "t" else -s.ty)

    def ynode(s, side, i):
        return s.cy + (s.by + s.dy.get(i, 0) if side == "t" else -s.by)

    def mk_tile(s, side, i, ch, color):
        r = RoundedRectangle(corner_radius=0.1, width=s.tw, height=s.th, stroke_color=color, stroke_width=3,
                             fill_color=color, fill_opacity=0.16)
        t = T(ch, s.fs, color, weight=BOLD)
        g = VGroup(r, t)
        g.move_to([s.X(i), s.ytile(side, i), 0])
        return g

    def mk_conn(s, side, i):
        sign = 1 if side == "t" else -1
        y1 = s.ynode(side, i)
        y2 = s.ytile(side, i) + sign * s.th / 2
        return Line([s.X(i), y1, 0], [s.X(i), y2, 0], color=s.col[side], stroke_width=3)

    def mk_node(s, side, i):
        return Dot([s.X(i), s.ynode(side, i), 0], radius=0.09, color=s.col[side])

    def mk_seg(s, side, i, color=None):
        return Line([s.X(i), s.ynode(side, i), 0], [s.X(i + 1), s.ynode(side, i + 1), 0],
                    color=color or s.col[side], stroke_width=5)

    def mk_rung(s, i, color=GREY, w=3):
        y1 = s.ytile("t", i) - s.th / 2
        y2 = s.ytile("b", i) + s.th / 2
        return Line([s.X(i), y1, 0], [s.X(i), y2, 0], color=color, stroke_width=w)

    def ghost(s, side, i):
        r = RoundedRectangle(corner_radius=0.1, width=s.tw, height=s.th, stroke_color=GREY, stroke_width=3)
        return DashedVMobject(r, num_dashes=18).move_to([s.X(i), s.ytile(side, i), 0])

    def column(s, side, i):
        """tile + connector + node of one position (what a base is)."""
        return VGroup(*[m for m in (s.tile[side][i], s.conn[side][i], s.node[side][i]) if m is not None])


def helix_curves(x0, x1, yc, amp=0.6, period=1.5, color=BLUE, w=7, phase=0.0):
    """Two plain parallel bars (a double-stranded piece of DNA), not a drawn helix."""
    off = amp * 0.4
    mk = lambda y: Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=w * 1.1).set_cap_style(CapStyleType.ROUND)
    return VGroup(mk(yc + off), mk(yc - off))


def wave_arrow(x, y0, y1, color=PURPLE):
    n = abs(y0 - y1)
    w = ParametricFunction(lambda t: np.array([x + 0.14 * np.sin(14 * t), y0 + (y1 - y0) * t, 0]),
                           t_range=[0, 1, 0.01], color=color, stroke_width=5)
    tip = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.16)
    tip.rotate(PI)
    tip.move_to([x, y1 + 0.05, 0])
    return VGroup(w, tip)


class S00Title(TitleCard):
    LESSON = "DNA repair and recombination"
    TITLE = "DNA holds its information twice"


# ---------------------------------------------------------------------------------------------
class S01Uracil(SpokenScene):
    """C·G turns into U·G; replication puts A opposite U; the next round leaves A·T; then one wrong base in a long row."""

    def construct(self):
        kw = dict(cx=-2.6, sp=0.78, tw=0.62, th=0.56, ty=0.42, by=0.8, fs=26)
        r1 = Duplex(list("AGTCGAT"), list("TCAGCTA"), cy=2.35, **kw)
        r2 = Duplex(list("AGTUGAT"), list("TCAACTA"), cy=0.0, bcol=GREEN, tc={3: RED}, **kw)
        r3 = Duplex(list("TCAACTA"), list("AGTTGAT"), cy=-2.35, tcol=GREEN, bcol=GREEN, **kw)
        self.play(FadeIn(r1.all), run_time=0.9)

        self.at("amino group")
        self.play(Indicate(r1.tile["t"][3], color=TEXT, scale_factor=1.3), run_time=0.9)
        self.at("turn into uracil")
        u = r1.mk_tile("t", 3, "U", RED)
        lab1 = T("cytosine becomes uracil", 26, RED).move_to([2.6, 2.35, 0], aligned_edge=LEFT)
        lab1.align_to([0.9, 0, 0], LEFT)
        self.play(ReplacementTransform(r1.tile["t"][3], u), FadeIn(lab1, shift=LEFT * 0.2), run_time=0.7)

        self.at("Uracil pairs")
        lab1b = T("uracil pairs with adenine", 26, TEXT).align_to([0.9, 0, 0], LEFT).set_y(1.5)
        self.play(FadeIn(lab1b, shift=LEFT * 0.2), Indicate(u, color=RED, scale_factor=1.3), run_time=0.7)

        self.at("next replication")
        a1 = arr([-2.6, 1.5, 0], [-2.6, 0.95, 0], GREY)
        lab2 = T("replication puts an A opposite U", 26, TEXT).align_to([0.9, 0, 0], LEFT).set_y(0.0)
        self.play(GrowArrow(a1), FadeIn(r2.all), FadeIn(lab2, shift=LEFT * 0.2), run_time=1.0)

        self.at("the round after")
        a2 = arr([-2.6, -0.85, 0], [-2.6, -1.4, 0], GREY)
        lab3 = T("replication again: an A·T pair", 26, TEXT).align_to([0.9, 0, 0], LEFT).set_y(-2.35)
        self.play(GrowArrow(a2), FadeIn(r3.all), FadeIn(lab3, shift=LEFT * 0.2), run_time=1.0)

        self.at("AT pair")
        self.play(Indicate(r3.tile["t"][3], color=TEXT, scale_factor=1.3),
                  Indicate(r3.tile["b"][3], color=TEXT, scale_factor=1.3), run_time=0.8)

        self.at("mutation made")
        box = RoundedRectangle(corner_radius=0.12, width=0.9, height=1.75, stroke_color=RED, stroke_width=5)
        box.move_to([r3.X(3), r3.cy, 0])
        mut = T("a mutation", 28, RED, weight=BOLD).next_to(lab3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(Create(box), FadeIn(mut), run_time=0.8)

        self.at("find a few")
        left = [r1.all, u, lab1, lab1b, a1, r2.all, lab2, a2, r3.all, lab3, box, mut]
        row = VGroup(*[Square(0.36, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.25)
                       for _ in range(27)]).arrange(RIGHT, buff=0.08).move_to([0, 0.1, 0])
        bad = Square(0.36, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.7).move_to(row[17])
        self.play(*[FadeOut(m) for m in left], run_time=0.3)
        self.play(LaggedStart(*[FadeIn(q) for q in row], lag_ratio=0.02), run_time=0.6)
        self.play(Transform(row[17], bad), run_time=0.2)
        lab_bad = T("a few wrong bases", 30, RED).next_to(row[17], UP, buff=0.8)
        pt = arr(lab_bad.get_bottom() + DOWN * 0.05, row[17].get_top() + UP * 0.05, RED)
        self.play(FadeIn(lab_bad), GrowArrow(pt), run_time=0.3)
        self.at("among billions")
        lab_ok = T("billions of right ones", 30, BLUE).next_to(row, DOWN, buff=0.7)
        self.play(FadeIn(lab_ok, shift=UP * 0.15), run_time=0.6)
        self.at("right ones")
        q = T("?", 110, TEXT, weight=BOLD).move_to([0, 2.6, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Partner(SpokenScene):
    """Base excision repair: glycosylase flips U out, a nick, polymerase copies the partner, ligase seals."""

    def construct(self):
        d = Duplex(list("TAGCUATGC"), list("ATCGGTACG"), cy=-0.5, tc={4: RED}, sp=1.05)
        x4 = d.X(4)
        yb_top = d.ynode("t", 4)
        self.play(FadeIn(d.all), run_time=0.9)

        self.at("information twice")
        tag_t = T("damaged\nstrand", 22, GREY).move_to([-5.85, d.ytile("t", 0), 0])
        tag_b = T("partner\nstrand", 22, GREY).move_to([-5.85, d.ytile("b", 0), 0])
        self.play(FadeIn(tag_t), FadeIn(tag_b),
                  Indicate(VGroup(*[t for t in d.tile["t"] if t is not d.tile["t"][4]]), color=TEXT, scale_factor=1.06),
                  Indicate(VGroup(*d.tile["b"]), color=TEXT, scale_factor=1.06), run_time=1.0)

        self.at("one strand is damaged")
        sq = SurroundingRectangle(d.tile["t"][4], color=RED, buff=0.12, stroke_width=5)
        self.play(Create(sq), run_time=0.5)

        self.at("copies the partner")
        self.play(Indicate(VGroup(*d.tile["b"]), color=GREEN, scale_factor=1.06), run_time=0.9)

        self.at("glycosylase flips")
        dome = Sector(radius=1.0, angle=PI, start_angle=0, stroke_color=YELLOW, stroke_width=5,
                      fill_color=YELLOW, fill_opacity=0.18).move_to([x4, yb_top + 0.35 + 0.5, 0])
        dome.align_to([0, yb_top + 0.35, 0], DOWN)
        gly = bchip("glycosylase", YELLOW, 26).move_to([x4, dome.get_top()[1] + 0.45, 0])
        utile = d.tile["t"][4]
        self.play(FadeOut(sq), FadeIn(dome), FadeIn(gly), run_time=0.5)
        self.play(FadeOut(d.conn["t"][4]), FadeOut(d.rung[4]),
                  utile.animate.move_to([x4, yb_top + 0.35 + 0.5, 0]),
                  run_time=0.9)

        self.at("cuts it from its sugar")
        ghost = d.ghost("t", 4)
        self.play(Indicate(utile, color=RED, scale_factor=1.1), FadeIn(ghost), run_time=0.5)
        self.play(FadeOut(dome), FadeOut(utile), FadeOut(gly), run_time=0.6)

        self.at("nicks the backbone")
        xm = (d.X(3) + d.X(4)) / 2
        enz = bchip("enzyme", YELLOW, 26).move_to([x4 - 2.4, yb_top + 1.5, 0])
        ar_e = arr(enz.get_bottom() + DOWN * 0.02, [xm - 0.1, yb_top + 0.35, 0], YELLOW)
        cut = slash(xm, yb_top)
        self.play(FadeIn(enz), GrowArrow(ar_e), run_time=0.4)
        self.play(FadeOut(d.seg["t"][3]), Create(cut), run_time=0.4)

        self.at("polymerase inserts")
        pol = bchip("polymerase", YELLOW, 26).move_to([x4 + 2.2, yb_top + 1.5, 0])
        ar_p = arr(pol.get_bottom() + DOWN * 0.02, [x4 + 0.1, d.ytile("t", 4) + d.th / 2 + 0.12, 0], YELLOW)
        self.play(FadeOut(enz), FadeOut(ar_e), FadeOut(cut), FadeIn(pol), GrowArrow(ar_p), run_time=0.5)
        newt = d.mk_tile("t", 4, "C", GREEN)
        newc = d.mk_conn("t", 4)
        self.play(FadeIn(newt, scale=0.6), FadeIn(newc), FadeOut(ghost), run_time=0.7)

        self.at("using the partner")
        rg = d.mk_rung(4, GREEN, 6)
        self.play(Create(rg), Indicate(d.tile["b"][4], color=TEXT, scale_factor=1.15), run_time=0.8)

        self.at("ligase seals")
        lig = bchip("ligase", YELLOW, 26).move_to(pol)
        seal = d.mk_seg("t", 3, GREEN)
        self.play(FadeOut(pol), FadeOut(ar_p), FadeIn(lig), run_time=0.4)
        self.play(Create(seal), Flash(seal.get_center(), color=YELLOW, flash_radius=0.4), run_time=0.7)
        self.play(FadeOut(lig), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Bulky(SpokenScene):
    """UV makes a dimer that bends the helix; NER cuts both sides, removes a piece, polymerase refills, ligase seals."""

    def construct(self):
        top, bot = list("GACGTTCAGC"), list("CTGCAAGTCG")
        d = Duplex(top, bot, cy=-0.4, sp=0.98)
        bent = Duplex(top, bot, cy=-0.4, sp=0.98, tc={4: RED, 5: RED}, tdy={3: -0.12, 4: -0.35, 5: -0.35, 6: -0.12})
        self.add(d.all)
        at_x = (d.X(4) + d.X(5)) / 2
        top_y = d.ynode("t", 4)

        self.at("Ultraviolet light")
        ws = VGroup(*[wave_arrow(at_x + dx, 3.5, top_y + 0.55) for dx in (-0.9, 0, 0.9)])
        uv = T("UV light", 28, PURPLE).move_to([at_x + 2.6, 2.7, 0])
        self.play(FadeIn(ws, shift=DOWN * 0.3), FadeIn(uv), run_time=1.0)

        self.at("joins two neighboring")
        bridge = Rectangle(width=0.28, height=0.3, stroke_width=0, fill_color=RED, fill_opacity=1)
        bridge.move_to([at_x, d.ytile("t", 4), 0])
        dimer = T("dimer", 28, RED).move_to([at_x, top_y + 0.65, 0])
        self.play(*[m.animate.set_stroke(RED).set_fill(RED, 0.16) for m in (d.tile["t"][4][0], d.tile["t"][5][0])],
                  *[d.tile["t"][i][1].animate.set_color(RED) for i in (4, 5)],
                  FadeOut(ws), FadeOut(uv), run_time=0.8)

        self.at("dimer that")
        self.play(FadeIn(bridge, scale=0.5), FadeIn(dimer), run_time=0.6)

        self.at("bends the helix")
        self.play(Transform(d.all, bent.all), bridge.animate.shift(DOWN * 0.35), run_time=0.9)

        self.at("senses the bend")
        y_hi = top_y + 0.22
        y_lo = d.cy + d.ty - 0.35 - d.th / 2 - 0.12
        sense = Rectangle(width=d.X(6) - d.X(3) + 0.95, height=y_hi - y_lo, stroke_color=YELLOW, stroke_width=4)
        sense.move_to([at_x, (y_hi + y_lo) / 2, 0])
        xer = bchip("excision repair", YELLOW, 26).move_to([at_x + 3.7, 2.9, 0])
        self.play(Create(sense), FadeIn(xer), run_time=0.7)

        self.at("cuts the damaged")
        c1 = slash((d.X(2) + d.X(3)) / 2, top_y, YELLOW)
        c2 = slash((d.X(6) + d.X(7)) / 2, top_y, YELLOW)
        self.play(FadeOut(d.seg["t"][2]), Create(c1), run_time=0.5)

        self.at("on both sides")
        self.play(FadeOut(d.seg["t"][6]), Create(c2), run_time=0.5)

        self.at("removes a short piece")
        piece = VGroup(*[m for i in range(3, 7) for m in (d.tile["t"][i], d.conn["t"][i], d.node["t"][i], d.rung[i])],
                       *[d.seg["t"][i] for i in (3, 4, 5)], bridge, sense, dimer)
        self.play(piece.animate.shift(UP * 0.9).set_opacity(0), FadeOut(c1), FadeOut(c2), FadeOut(xer), run_time=1.0)

        self.at("polymerase fills")
        pol = bchip("polymerase", YELLOW, 26).move_to([at_x, 2.9, 0])
        news = []
        for i in range(3, 7):
            news.append(VGroup(d.mk_tile("t", i, top[i], GREEN), d.mk_conn("t", i), d.mk_node("t", i),
                               d.mk_rung(i, GREEN, 4)))
        self.play(FadeIn(pol), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(n, scale=0.7) for n in news], lag_ratio=0.25), run_time=1.4)
        gseg = [d.mk_seg("t", i, GREEN) for i in (3, 4, 5)]
        self.play(*[Create(g) for g in gseg], run_time=0.5)

        self.at("ligase seals")
        lig = bchip("ligase", YELLOW, 26).move_to(pol)
        s2, s6 = d.mk_seg("t", 2, GREEN), d.mk_seg("t", 6, GREEN)
        self.play(FadeOut(pol), FadeIn(lig), run_time=0.3)
        self.play(Create(s2), Create(s6), Flash(s2.get_center(), color=YELLOW, flash_radius=0.4),
                  Flash(s6.get_center(), color=YELLOW, flash_radius=0.4), run_time=0.7)
        self.play(FadeOut(lig), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Mismatch(SpokenScene):
    """G opposite T: which is wrong? The new strand, found by missing methyl on GATC; MutS, MutL, MutH; strand removed and rebuilt."""

    def construct(self):
        top, bot = list("CGATCATGCA"), list("GCTAGTATGT")
        # bottom letters: complement of the top, except column 7 (G over T)
        bot = [{"A": "T", "T": "A", "G": "C", "C": "G"}[c] for c in top]
        bot[7] = "T"
        kw = dict(cy=0.1, sp=0.95, tw=0.8, th=0.7, ty=0.72, by=1.6, fs=30, norung=(7,))
        d = Duplex(top, bot, tcol=GREY, bcol=GREY, **kw)
        db = Duplex(top, bot, tcol=BLUE, bcol=GREEN, **kw)
        self.add(d.all)
        x7, ymid = d.X(7), d.cy
        qm = T("?", 40, RED, weight=BOLD).move_to([x7, ymid, 0])
        wrong_t = d.tile["t"][7]
        wrong_b = d.tile["b"][7]

        self.at("paired wrongly")
        self.play(wrong_t[0].animate.set_stroke(RED), wrong_t[1].animate.set_color(RED),
                  wrong_b[0].animate.set_stroke(RED), wrong_b[1].animate.set_color(RED),
                  FadeIn(qm, scale=0.6), run_time=0.7)

        self.at("Neither is damaged")
        self.play(Indicate(VGroup(wrong_t, wrong_b), color=TEXT, scale_factor=1.1), run_time=0.9)

        self.at("new strand")
        tag_t = T("template", 22, BLUE).move_to([-5.75, d.ytile("t", 0), 0])
        tag_b = T("new\nstrand", 22, GREEN).move_to([-5.75, d.ytile("b", 0), 0])
        self.play(Transform(d.all, db.all), FadeIn(tag_t), FadeIn(tag_b), run_time=0.9)

        self.at("In E. coli")
        ecoli = T("E. coli", 28, GREY, slant=ITALIC).move_to([-5.2, 3.0, 0])
        self.play(FadeIn(ecoli), run_time=0.5)

        self.at("carries methyl")
        box = Rectangle(width=4 * d.sp + 0.1, height=2 * (d.ty + d.th / 2) + 0.2, stroke_color=TEXT,
                        stroke_width=2).move_to([(d.X(1) + d.X(4)) / 2, d.cy, 0])
        xa = d.X(2)
        yb_top = d.ynode("t", 2)
        me = VGroup(Circle(radius=0.27, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.9),
                    T("Me", 22, BG, weight=BOLD)).move_to([xa, yb_top + 0.7, 0])
        stem = Line([xa, yb_top + 0.43, 0], [xa, yb_top, 0], color=ORANGE, stroke_width=3)
        gatc = T("GATC", 26, TEXT)
        gatc.move_to([xa + 0.5 + gatc.width / 2, yb_top + 0.7, 0])
        self.play(FadeIn(me, scale=0.6), Create(stem), run_time=0.6)

        self.at("GATC sites")
        self.play(Create(box), FadeIn(gatc), run_time=0.6)

        self.at("briefly unmethylated")
        xb = d.X(3)
        yb_bot = d.ynode("b", 3)
        empty = DashedVMobject(Circle(radius=0.27, stroke_color=ORANGE, stroke_width=3), num_dashes=12)
        empty.move_to([xb, yb_bot - 0.7, 0])
        unm = T("unmethylated", 24, ORANGE).next_to(empty, RIGHT, buff=0.25)
        self.play(FadeIn(empty), FadeIn(unm), run_time=0.6)

        self.at("binds the mismatch")
        muts = bchip("MutS", YELLOW, 26).move_to([x7, -3.0, 0])
        a_s = arr(muts.get_top() + UP * 0.02, [x7, -1.5, 0], YELLOW)
        self.play(FadeIn(muts, shift=UP * 0.3), GrowArrow(a_s), run_time=0.7)

        self.at("joins it")
        mutl = bchip("MutL", YELLOW, 26).move_to([x7 + 3.2, -3.0, 0])
        self.play(mutl.animate.move_to([x7 + 1.7, -3.0, 0]), run_time=0.7)

        self.at("nicks the")
        xm = (d.X(2) + d.X(3)) / 2
        muth = bchip("MutH", YELLOW, 26).move_to([-3.4, -3.0, 0])
        a_h = arr(muth.get_top() + UP * 0.02, [xm - 0.15, yb_bot - 0.25, 0], YELLOW)
        cut = slash(xm, yb_bot)
        self.play(FadeIn(muth, shift=UP * 0.3), GrowArrow(a_h), run_time=0.5)
        self.play(FadeOut(d.seg["b"][2]), Create(cut), run_time=0.4)

        self.at("removed past")
        cols = range(3, 9)
        piece = VGroup(*[m for i in cols for m in (d.tile["b"][i], d.conn["b"][i], d.node["b"][i], d.rung[i]) if m is not None],
                       *[d.seg["b"][i] for i in range(3, 9)], empty, unm)
        self.play(FadeOut(muts), FadeOut(mutl), FadeOut(muth), FadeOut(a_s), FadeOut(a_h), FadeOut(cut),
                  FadeOut(qm), piece.animate.shift(DOWN * 0.9).set_opacity(0), run_time=1.0)

        self.at("rebuilt")
        corr = {"A": "T", "T": "A", "G": "C", "C": "G"}
        news = [VGroup(d.mk_tile("b", i, corr[top[i]], GREEN), d.mk_conn("b", i), d.mk_node("b", i)) for i in cols]
        news[4].add(d.mk_rung(7, GREEN, 4))
        segs = [d.mk_seg("b", i, GREEN) for i in range(2, 9)]
        self.play(LaggedStart(*[FadeIn(n, scale=0.7) for n in news], lag_ratio=0.2), run_time=1.3)
        self.play(*[Create(sg) for sg in segs], run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Break(SpokenScene):
    """Both strands cut: the copy option is gone. Rope: knot the ends or splice. Ku rings grip ends; a ligase joins; no template."""

    def construct(self):
        d = Duplex(list("GATCGGCA"), list("CTAGCCGT"), cy=0.0, sp=1.1)
        self.add(d.all)
        ax = 5.6
        carrow = arr([ax, -1.5, 0], [ax, 1.5, 0], GREEN, w=7)
        carrow_lab = T("copy the\npartner", 24, GREEN).move_to([ax, 2.4, 0])
        self.play(GrowArrow(carrow), FadeIn(carrow_lab), run_time=0.7)

        self.at("removes the copying")
        left = VGroup(*[m for i in range(0, 4) for m in (d.tile["t"][i], d.tile["b"][i], d.conn["t"][i], d.conn["b"][i],
                                                          d.node["t"][i], d.node["b"][i], d.rung[i])],
                      *[d.seg["t"][i] for i in range(0, 3)], *[d.seg["b"][i] for i in range(0, 3)])
        right = VGroup(*[m for i in range(4, 8) for m in (d.tile["t"][i], d.tile["b"][i], d.conn["t"][i], d.conn["b"][i],
                                                           d.node["t"][i], d.node["b"][i], d.rung[i])],
                       *[d.seg["t"][i] for i in range(4, 7)], *[d.seg["b"][i] for i in range(4, 7)])
        xmid = (d.X(3) + d.X(4)) / 2
        crossed = VGroup(Line([ax - 0.4, -0.4, 0], [ax + 0.4, 0.4, 0], color=RED, stroke_width=9),
                         Line([ax - 0.4, 0.4, 0], [ax + 0.4, -0.4, 0], color=RED, stroke_width=9))
        self.play(FadeOut(d.seg["t"][3]), FadeOut(d.seg["b"][3]),
                  left.animate.shift(LEFT * 0.5), right.animate.shift(RIGHT * 0.5),
                  Create(crossed, lag_ratio=0), carrow.animate.set_opacity(0.4), carrow_lab.animate.set_opacity(0.4),
                  run_time=0.9)
        cuts = VGroup(slash(xmid, d.cy + d.by, RED, 0.3), slash(xmid, d.cy - d.by, RED, 0.3))
        self.play(FadeIn(cuts, scale=1.4), run_time=0.4)

        self.at("Picture a rope")
        RY = 0.7
        self.play(FadeOut(VGroup(left, right, cuts, crossed, carrow, carrow_lab)), run_time=0.5)
        rl = helix_curves(-6.0, -0.45, RY, amp=0.8, period=1.8)
        rr = helix_curves(0.45, 6.0, RY, amp=0.8, period=1.8)
        self.play(Create(rl, lag_ratio=0), Create(rr, lag_ratio=0), run_time=0.9)

        self.at("knot the ends")
        knot = Ellipse(width=1.0, height=1.6, stroke_color=YELLOW, stroke_width=8).move_to([0, RY, 0])
        self.play(rl.animate.shift(RIGHT * 0.45), rr.animate.shift(LEFT * 0.45), run_time=0.6)
        self.play(Create(knot), run_time=0.4)

        self.at("splice in")
        sister = helix_curves(-6.0, 6.0, -2.1, amp=0.8, period=1.8, color=BLUE)
        sister.set_stroke(opacity=0.55)
        brk = DashedVMobject(Rectangle(width=2.4, height=1.6, stroke_color=YELLOW, stroke_width=4), num_dashes=40)
        brk.move_to([0, -2.1, 0])
        up = arr([0, -0.95, 0], [0, -0.2, 0], YELLOW, w=6)
        self.play(FadeOut(knot), rl.animate.shift(LEFT * 0.45), rr.animate.shift(RIGHT * 0.45),
                  FadeIn(sister), run_time=0.7)
        self.play(Create(brk), GrowArrow(up), run_time=0.7)

        self.at("end joining knots")
        nhej = T("non-homologous end joining", 30, TEXT).move_to([0, 2.9, 0])
        self.play(FadeOut(sister), FadeOut(brk), FadeOut(up), FadeIn(nhej, shift=DOWN * 0.15), run_time=0.7)

        self.at("grips each end")
        ku1 = Ellipse(width=0.6, height=1.5, stroke_color=YELLOW, stroke_width=8).move_to([-0.6, RY, 0])
        ku2 = Ellipse(width=0.6, height=1.5, stroke_color=YELLOW, stroke_width=8).move_to([0.6, RY, 0])
        kul = T("Ku", 30, YELLOW, weight=BOLD).move_to([0, RY + 1.75, 0])
        self.play(FadeIn(ku1, scale=0.7), FadeIn(ku2, scale=0.7), FadeIn(kul), FadeOut(nhej), run_time=0.9)

        self.at("ligase joins")
        lig = bchip("ligase", YELLOW, 26).move_to([0, RY + 1.75, 0])
        self.play(FadeOut(kul), FadeIn(lig), run_time=0.3)
        self.play(rl.animate.shift(RIGHT * 0.45), rr.animate.shift(LEFT * 0.45),
                  ku1.animate.shift(RIGHT * 0.3), ku2.animate.shift(LEFT * 0.3), run_time=0.7)
        self.play(FadeOut(ku1), FadeOut(ku2), Flash([0, RY, 0], color=YELLOW, flash_radius=0.7), run_time=0.5)

        self.at("uses no template")
        nt = T("no template", 30, GREY).move_to([0, -1.0, 0])
        self.play(FadeIn(nt, shift=UP * 0.15), FadeOut(lig), run_time=0.6)

        self.at("needed trimming")
        jb = DashedVMobject(Rectangle(width=1.6, height=1.6, stroke_color=RED, stroke_width=4), num_dashes=36)
        jb.move_to([0, RY, 0])
        self.play(Create(jb), run_time=0.7)

        self.at("gained or lost")
        gl = T("a few bases may be gained or lost", 28, RED).move_to([0, -2.1, 0])
        self.play(FadeIn(gl, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Splice(SpokenScene):
    """Homologous recombination: trim to tails, Rad51 coats, tail invades the sister, synthesis copies what was lost; the rule."""

    def construct(self):
        yb = 2.0
        ys = -1.7
        hs = 0.32
        lw = 8

        def line(x0, x1, y, color=BLUE):
            return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=lw).set_cap_style(CapStyleType.ROUND)

        lu = line(-6.0, -0.5, yb + hs)
        ll = line(-6.0, -0.5, yb - hs)
        ru = line(0.5, 6.0, yb + hs)
        rl_ = line(0.5, 6.0, yb - hs)
        brk_lab = T("break", 26, RED).move_to([0, yb + 1.2, 0])
        self.play(Create(VGroup(lu, ll, ru, rl_), lag_ratio=0), FadeIn(brk_lab), run_time=0.8)

        self.at("matching rope")
        su = line(-6.0, 6.0, ys + hs)
        sl = line(-6.0, 6.0, ys - hs)
        self.play(Create(VGroup(su, sl), lag_ratio=0), run_time=0.8)

        self.at("trim the ends")
        self.play(FadeOut(brk_lab),
                  ll.animate.put_start_and_end_on([-6.0, yb - hs, 0], [-2.0, yb - hs, 0]),
                  ru.animate.put_start_and_end_on([2.0, yb + hs, 0], [6.0, yb + hs, 0]),
                  run_time=0.9)
        tails_lab = T("single-stranded tails", 26, TEXT).move_to([0, yb + 1.2, 0])
        self.play(FadeIn(tails_lab), run_time=0.4)

        self.at("Rad51 coats")
        coat_l = Line([-2.0, yb + hs, 0], [-0.5, yb + hs, 0], color=YELLOW, stroke_width=18, stroke_opacity=0.45)
        coat_r = Line([0.5, yb - hs, 0], [2.0, yb - hs, 0], color=YELLOW, stroke_width=18, stroke_opacity=0.45)
        rad = bchip("Rad51", YELLOW, 28).move_to([0, yb + 1.2, 0])
        self.play(FadeIn(coat_l), FadeIn(coat_r), ReplacementTransform(tails_lab, rad), run_time=0.8)

        self.at("invades a matching")
        start = np.array([-2.0, yb + hs, 0])
        end = np.array([-1.0, ys, 0])
        path = CubicBezier(start, start + np.array([1.6, 0.0, 0]), end + np.array([-0.9, 1.8, 0]), end)
        inv = path.copy().set_stroke(BLUE, lw)
        coat_inv = path.copy().set_stroke(YELLOW, 18, opacity=0.45)
        self.play(lu.animate.put_start_and_end_on([-6.0, yb + hs, 0], [-2.0, yb + hs, 0]), FadeOut(coat_l),
                  FadeIn(inv), FadeIn(coat_inv), run_time=1.0)
        tip = Dot(end, radius=0.1, color=GREEN)
        note = T("one end shown invading", 24, GREY).move_to([-4.0, 0.2, 0])
        self.play(FadeIn(note), run_time=0.4)

        self.at("primes synthesis")
        newdna = Line(end, [2.0, ys, 0], color=GREEN, stroke_width=10)
        self.play(FadeIn(tip), run_time=0.2)
        self.play(Create(newdna), run_time=1.3)

        self.at("lost at the break")
        lost = T("copying what was lost", 28, GREEN).move_to([3.2, ys + 1.0, 0])
        self.play(FadeIn(lost, shift=UP * 0.15), run_time=0.5)

        self.at("sister chromatid")
        sis = T("sister chromatid", 30, BLUE).move_to([-3.7, ys - 1.2, 0])
        self.play(FadeIn(sis, shift=UP * 0.15), run_time=0.5)

        self.at("One rule runs")
        everything = [note, lu, ll, ru, rl_, su, sl, coat_r, rad, inv, coat_inv, tip, newdna, lost, sis]
        self.play(*[FadeOut(m) for m in everything], run_time=0.6)
        hx = helix_curves(-4.4, 4.4, 0.7, amp=1.0, period=2.2, color=BLUE, w=10)
        self.play(Create(hx, lag_ratio=0), run_time=0.9)
        self.at("held twice")
        twice = T("the information, held twice", 44, TEXT, font=TITLE_FONT).move_to([0, -1.8, 0])
        self.play(FadeIn(twice, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "One rule runs through almost all repair:\nthe information is held twice."
