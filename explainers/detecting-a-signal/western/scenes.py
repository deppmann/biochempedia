"""Detecting a signal, section film: sort by size (SDS-PAGE), then ask an antibody (western blot,
phosphospecific antibody, and its limits).  Timed to the spoken words with self.at("...").

COLOR MAP (one color per concept, whole video)
  YELLOW = the protein you want to follow (your protein)
  GREY   = other proteins, gel, membrane, labels, structure
  TEAL   = the negative charge that SDS coats on proteins; the second antibody
  BLUE   = the (first) antibody
  GREEN  = a detected band / the light the enzyme makes
  GOLD   = a phosphate (the little "P" badge)
  RED    = a limit of the method
No molecular structures: proteins are dots and rods, antibodies are labelled blocks,
a gel or blot is a plain rectangle and bands are bars.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BG_ = BG
LENS = [1.5, 1.3, 1.1, 0.95, 0.8, 0.65, 0.5, 0.4]   # class lengths, largest first
YK = 3                                              # the yellow (your protein) class
GCY = -0.2                                          # gel centre y
GW, GH = 3.2, 5.2


def rel_y(k):
    return 1.5 - k * 0.5286


def pbadge(r=0.2):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def rod(length, color=GREY, h=0.14, charged=True):
    return RoundedRectangle(corner_radius=h / 2, width=length, height=h, stroke_color=TEAL if charged else color,
                            stroke_width=2 if charged else 0, fill_color=color, fill_opacity=0.95)


def bar(w, h, color, op=0.95):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=op)


def gel_frame(cx, cy, s=1.0):
    outline = Rectangle(width=GW * s, height=GH * s, stroke_color=GREY, stroke_width=3,
                        fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])
    well = Rectangle(width=2.0 * s, height=0.3 * s, stroke_color=GREY, stroke_width=2,
                     fill_color=BG, fill_opacity=1).move_to([cx, cy + (GH / 2 - 0.4) * s, 0])
    return VGroup(outline, well)


def band_set(cx, cy, s=1.0, op=0.95):
    out = VGroup()
    for k, L in enumerate(LENS):
        col = YELLOW if k == YK else GREY
        out.add(bar(L * s, 0.16 * s, col, op).move_to([cx, cy + rel_y(k) * s, 0]))
    return out


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dock_above(chipm, target, gap=0.02):
    return chipm.animate.move_to(target.get_top() + UP * (chipm.height / 2 + gap))


class S00Title(TitleCard):
    LESSON = "Detecting a signal"
    TITLE = "Sort by size, then ask an antibody"


# ---------------------------------------------------------------------------------------------
class S01Sort(SpokenScene):
    def construct(self):
        rs = np.random.RandomState(3)
        classes = rs.permutation([i % 8 for i in range(24)])
        bx, by = 0.0, 0.2
        box = RoundedRectangle(corner_radius=0.15, width=3.5, height=3.5, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.08).move_to([bx, by, 0])
        cells = [[bx + (c - 1) * 1.1, by + 1.4 - r * 0.4] for r in range(8) for c in range(3)]
        dots, rods_box = [], []
        for i, (x, y) in enumerate(cells):
            k = int(classes[i])
            col = YELLOW if k == YK else GREY
            dots.append(Circle(radius=0.07 + 0.12 * LENS[k] / 1.5, stroke_width=0, fill_color=col,
                               fill_opacity=0.95).move_to([x, y, 0]))
            r = rod(LENS[k] * 0.55, col).move_to([x, y, 0])
            rods_box.append(r)
        lbl_ext = T("cell extract", 24, GREY).next_to(box, DOWN, buff=0.15)

        self.at("A cell extract")
        self.play(FadeIn(box), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), FadeIn(lbl_ext),
                  run_time=1.2)
        leg_y = VGroup(Circle(radius=0.1, stroke_width=0, fill_color=YELLOW, fill_opacity=1), T("your protein (one kind)", 24, YELLOW))
        leg_y.arrange(RIGHT, buff=0.15)
        leg_y.next_to(lbl_ext, DOWN, buff=0.12)
        self.at("follow just one")
        yel = [d for d, kk in zip(dots, classes) if kk == YK]
        self.play(FadeIn(leg_y), *[Indicate(d, color=YELLOW, scale_factor=1.8) for d in yel], run_time=1.0)

        tag = T("SDS-PAGE", 34, TEXT, weight=BOLD).move_to([bx, 3.1, 0])
        self.at("This step is called")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)

        sds = chip("SDS + heat", TEAL, 24).move_to([bx, 2.4, 0])
        self.at("Heat the extract")
        self.play(FadeIn(sds, shift=DOWN * 0.15), run_time=0.5)
        self.at("unfolds each protein")
        self.play(*[Transform(d, r) for d, r in zip(dots, rods_box)], run_time=1.2)
        leg_c = VGroup(Line(LEFT * 0.15, RIGHT * 0.15, color=TEAL, stroke_width=5), T("negative charge", 24, TEAL))
        leg_c.arrange(RIGHT, buff=0.15).next_to(leg_y, DOWN, buff=0.12)
        self.at("negative charge")
        self.play(FadeIn(leg_c), *[Indicate(d, color=TEAL, scale_factor=1.15) for d in dots[:6]], run_time=0.8)

        # --- the gel ----------------------------------------------------------------------
        gcx = 2.4
        gel = gel_frame(gcx, GCY)
        minus = T("−", 40, TEXT, weight=BOLD).move_to([gcx, GCY + GH / 2 + 0.4, 0])
        plus = T("+", 40, TEXT, weight=BOLD).move_to([gcx, GCY - GH / 2 - 0.4, 0])
        self.at("Pull the mixture")
        left = VGroup(box, lbl_ext, leg_y, leg_c, tag, *dots)
        self.play(FadeOut(sds), left.animate.shift(LEFT * 4.5), run_time=0.6)
        self.play(FadeIn(gel), FadeIn(minus), FadeIn(plus), run_time=0.3)
        well_y = GCY + GH / 2 - 0.4
        moves = []
        for d, kk in zip(dots, classes):
            moves.append(d.animate.move_to([gcx + rs.uniform(-0.1, 0.1), well_y + rs.uniform(-0.04, 0.04), 0])
                         .scale(1 / 0.55))
        self.play(*moves, run_time=1.0)
        fld = arr([0.3, 1.6, 0], [0.3, -2.0, 0], TEXT)
        fld_t = T("electric\nfield", 24, TEXT, line_spacing=0.8).next_to(fld, LEFT, buff=0.15)
        self.at("electric field")
        self.play(GrowArrow(fld), FadeIn(fld_t), run_time=0.4)
        large = T("large", 24, GREY).move_to([gcx + 2.55, GCY + rel_y(0), 0])
        small = T("small", 24, GREY).move_to([gcx + 2.55, GCY + rel_y(7), 0])
        self.play(FadeIn(large), FadeIn(small), run_time=0.3)
        self.at("Small proteins travel")
        self.play(*[d.animate.move_to([gcx, GCY + rel_y(int(kk)), 0]) for d, kk in zip(dots, classes)],
                  run_time=2.8, rate_func=linear)
        self.play(Indicate(small, color=TEXT, scale_factor=1.25), Indicate(large, color=TEXT, scale_factor=1.25),
                  run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Find(SpokenScene):
    def construct(self):
        s = 0.9
        gcx, mcx = -4.8, -0.9
        gel = gel_frame(gcx, GCY, s)
        gbands = band_set(gcx, GCY, s)
        g_lbl = T("gel", 24, GREY).move_to([gcx, GCY + GH / 2 * s + 0.4, 0])
        self.add(gel, gbands)
        tag = T("Western blot", 34, TEXT, weight=BOLD).move_to([2.8, 3.1, 0])
        self.play(FadeIn(g_lbl), run_time=0.5)
        self.at("western blot")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)

        mem = Rectangle(width=GW * s, height=GH * s, stroke_color=GREY, stroke_width=3,
                        fill_color=TEXT, fill_opacity=0.12).move_to([mcx, GCY, 0])
        m_lbl = T("membrane", 24, GREY).move_to([mcx, GCY + GH / 2 * s + 0.4, 0])
        mbands = band_set(mcx, GCY, s)
        a = arr([gcx + GW / 2 * s + 0.1, GCY, 0], [mcx - GW / 2 * s - 0.1, GCY, 0], TEXT)
        move_t = T("move", 22, TEXT).next_to(a, UP, buff=0.12)
        self.at("Move the sorted")
        self.play(FadeIn(mem), FadeIn(m_lbl), GrowArrow(a), FadeIn(move_t), run_time=0.6)
        self.play(*[ReplacementTransform(gb.copy(), mb) for gb, mb in zip(gbands, mbands)], run_time=1.2)

        yb = mbands[YK]
        ab1 = chip("antibody", BLUE, 24).move_to([4.5, 2.2, 0]).set_z_index(3)
        self.at("soak the membrane")
        self.play(FadeIn(ab1), run_time=0.4)
        self.play(ab1.animate.next_to(yb, RIGHT, buff=0.04), run_time=1.3)
        ab2 = chip("second antibody", TEAL, 24).move_to([4.2, 2.2, 0]).set_z_index(3)
        self.at("A second antibody")
        self.play(FadeIn(ab2), run_time=0.4)
        self.play(ab2.animate.next_to(ab1.copy().next_to(yb, RIGHT, buff=0.04), RIGHT, buff=0.04), run_time=1.1)
        enz = VGroup(Circle(radius=0.22, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=1),
                     T("E", 22, BG, weight=BOLD))
        enz[1].move_to(enz[0])
        enz.next_to(ab2, UP, buff=0.05)
        enz_t = T("enzyme", 22, GREEN).next_to(enz, RIGHT, buff=0.12)
        self.at("carries an enzyme")
        self.play(FadeIn(enz, scale=0.5), FadeIn(enz_t), run_time=0.6)
        halo = Rectangle(width=yb.width + 0.14, height=0.5, stroke_color=GREEN, stroke_width=3,
                         fill_color=GREEN, fill_opacity=0.35).move_to(yb)
        light_t = T("light or colour", 24, GREEN).next_to(ab2, DOWN, buff=0.4)
        self.at("an enzyme that makes light")
        self.play(FadeIn(halo), FadeIn(light_t), run_time=0.7)
        self.at("marks where")
        self.play(Indicate(halo, color=GREEN, scale_factor=1.15), run_time=0.8)
        one = T("a band at one size", 28, TEXT).move_to([3.4, -2.2, 0])
        self.at("band at one size")
        self.play(*[b.animate.set_opacity(0.15) for b in mbands if b is not yb], FadeIn(one), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def blot(cx, cy, w, h, ops, title, lanes=("before signal", "after signal")):
    frame = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=TEXT, fill_opacity=0.12)
    frame.move_to([cx, cy, 0])
    bands, lbls = VGroup(), VGroup()
    for i, (op, nm) in enumerate(zip(ops, lanes)):
        x = cx + (i - 0.5) * (w / 2)
        bands.add(bar(w / 2 * 0.62, 0.3, GREEN, op).move_to([x, cy, 0]))
        lbls.add(T(nm, 22, GREY).move_to([x, cy - h / 2 - 0.3, 0]))
    t = T(title, 24, BLUE).move_to([cx, cy + h / 2 + 0.35, 0])
    return frame, bands, lbls, t


class S03Site(SpokenScene):
    def construct(self):
        ab = chip("antibody", BLUE, 32).move_to([-4.6, 2.2, 0])
        self.at("One antibody")
        self.play(FadeIn(ab), run_time=0.5)
        piece = bar(2.0, 0.4, GREY, 0.9).move_to([0.3, -0.3, 0])
        p0 = pbadge(0.3).move_to(piece.get_left() + RIGHT * 0.5 + UP * 0.5)
        pl = T("short piece, one phosphate", 28, GREY).next_to(piece, DOWN, buff=0.3)
        self.at("short piece")
        self.play(FadeIn(piece), FadeIn(pl), run_time=0.5)
        self.play(FadeIn(p0, scale=0.5), run_time=0.4)
        self.play(dock_above(ab, p0), run_time=1.0)
        self.wait(0.6)

        # two whole proteins: with and without the phosphate
        pa = bar(4.4, 0.4, GREY, 0.9).move_to([-3.4, -0.5, 0])
        pb = bar(4.4, 0.4, GREY, 0.9).move_to([3.4, -0.5, 0])
        pa_p = pbadge(0.3).move_to(pa.get_top() + LEFT * 0.9 + UP * 0.3)
        la = T("with phosphate", 28, GOLD).next_to(pa, DOWN, buff=0.4)
        lb = T("no phosphate", 28, GREY).next_to(pb, DOWN, buff=0.4)
        self.at("chosen so that")
        self.play(FadeOut(piece), FadeOut(pl), FadeOut(p0), ab.animate.move_to([0, 1.5, 0]),
                  FadeIn(pa), FadeIn(pb), FadeIn(pa_p), FadeIn(la), FadeIn(lb), run_time=1.0)
        self.at("binds only")
        self.play(dock_above(ab, pa_p), run_time=0.8)
        self.play(Indicate(pa_p, color=GOLD, scale_factor=1.4), run_time=0.5)
        self.at("when the phosphate is present")
        self.play(Indicate(la, color=GOLD, scale_factor=1.15), run_time=0.6)
        self.wait(0.3)

        # blots
        all_a = VGroup(ab, pa, pb, pa_p, la, lb)
        f1, b1, l1, t1 = blot(-3.2, 0.4, 5.4, 3.0, [0.25, 0.95], "phosphospecific antibody")
        f2, b2, l2, t2 = blot(3.2, 0.4, 5.4, 3.0, [0.8, 0.8], "whole-protein antibody")
        ex = T("idealised example", 22, GREY).move_to([0, -3.2, 0])
        self.at("A blot with it")
        self.play(FadeOut(all_a), FadeIn(f1), FadeIn(t1), FadeIn(l1), run_time=0.7)
        self.play(FadeIn(b1), run_time=0.5)
        self.at("from cells")
        self.play(FadeIn(ex), run_time=0.4)
        self.at("same samples")
        self.play(FadeIn(f2), FadeIn(t2), FadeIn(l2), run_time=0.6)
        self.play(FadeIn(b2), run_time=0.5)
        q = T("more phosphate, or more protein?", 30, TEXT).move_to([0, -2.4, 0])
        self.at("Otherwise you cannot")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Limits(SpokenScene):
    def construct(self):
        L, R, TOPY, BOTY = -3.2, 3.2, 1.75, -1.75

        def title(txt, px, py):
            return T(txt, 26, TEXT, weight=BOLD).move_to([px, py + 1.25, 0])

        # panel 1: an unsuspected site
        t1 = title("Cannot find an unsuspected site", L, TOPY)
        pbody = bar(4.6, 0.4, GREY, 0.9).move_to([L, TOPY - 0.7, 0])
        pA = pbadge(0.27).move_to([L - 1.5, TOPY - 0.7 + 0.45, 0])
        pB = VGroup(DashedVMobject(Circle(radius=0.27, stroke_color=RED, stroke_width=3), num_dashes=12), T("?", 24, RED, weight=BOLD)).move_to([L + 1.5, TOPY - 0.7 + 0.45, 0])
        pB[1].move_to(pB[0])
        abx = chip("antibody", BLUE, 26)
        abx.move_to(pA.get_top() + UP * (abx.height / 2 + 0.02))
        lA = T("known site", 24, GREY).move_to([L - 1.5, TOPY - 1.3, 0])
        lB = T("site nobody suspected", 24, RED).move_to([L + 1.5, TOPY - 1.3, 0])
        # panel 2: darker, not what fraction
        t2 = title("Darker, not what fraction", R, TOPY)
        band = bar(1.6, 0.4, GREEN, 0.3).move_to([R - 2.1, TOPY - 0.4, 0])
        lband = T("darker", 24, GREEN).move_to([R - 2.1, TOPY - 1.0, 0])
        dots = VGroup(*[VGroup(Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                                      fill_opacity=0.9), T("?", 22, BG, weight=BOLD)) for _ in range(6)])
        for d in dots:
            d[1].move_to(d[0])
        dots.arrange(RIGHT, buff=0.1).move_to([R + 1.45, TOPY - 0.4, 0])
        ldots = T("what fraction carry\nthe phosphate?", 24, RED, line_spacing=0.8).move_to([R + 1.45, TOPY - 1.15, 0])
        # panel 3: wrong protein, control sample
        t3 = title("Can bind the wrong protein", L, BOTY)
        wp = bar(1.9, 0.3, GREY, 0.9).move_to([L - 1.8, BOTY - 0.45, 0])
        abw = chip("antibody", BLUE, 26)
        abw.move_to(wp.get_top() + UP * (abw.height / 2 + 0.02))
        lw = T("wrong protein", 22, RED).move_to([L - 1.8, BOTY - 0.95, 0])
        ctl = Rectangle(width=1.1, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=TEXT,
                        fill_opacity=0.12).move_to([L + 1.8, BOTY - 0.1, 0])
        lc = T("sample with the protein\nor phosphate missing", 22, GREY, line_spacing=0.8).next_to(ctl, DOWN, buff=0.15)
        # panel 4: a blot averages millions of cells
        t4 = title("Averages millions of cells", R, BOTY)
        rs = np.random.RandomState(5)
        cells = VGroup()
        for i in range(18):
            x = R - 2.2 + (i % 6) * 0.42 + rs.uniform(-0.05, 0.05)
            y = BOTY + 0.15 - (i // 6) * 0.42 + rs.uniform(-0.05, 0.05)
            cells.add(Circle(radius=0.16, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35)
                      .move_to([x, y, 0]))
        ar = arr([R + 0.5, BOTY - 0.1, 0], [R + 1.3, BOTY - 0.1, 0], TEXT)
        band4 = bar(1.2, 0.3, GREEN, 0.95).move_to([R + 2.2, BOTY - 0.1, 0])
        lcell = T("millions of cells", 22, GREY).move_to([R - 1.2, BOTY - 1.1, 0])
        lone = T("one band", 22, GREEN).move_to([R + 2.2, BOTY - 0.7, 0])

        self.at("An antibody has limits")
        self.wait(0.3)
        self.at("answers the question")
        self.play(FadeIn(t1), FadeIn(pbody), FadeIn(pA), FadeIn(lA), run_time=0.8)
        self.play(FadeIn(abx, shift=DOWN * 0.1), run_time=0.5)
        self.at("a site nobody suspected")
        self.play(FadeIn(pB), FadeIn(lB), run_time=0.9)
        self.play(Indicate(pB, color=RED, scale_factor=1.3), run_time=0.5)
        self.at("got darker")
        self.play(FadeIn(t2), FadeIn(band), FadeIn(lband), run_time=0.6)
        self.play(band.animate.set_fill(GREEN, 0.95), run_time=0.8)
        self.at("what fraction of the molecules")
        self.play(FadeIn(dots), FadeIn(ldots), run_time=0.8)
        self.at("bind the wrong protein")
        self.play(FadeIn(t3), FadeIn(wp), FadeIn(lw), run_time=0.5)
        self.play(FadeIn(abw, shift=DOWN * 0.1), run_time=0.5)
        self.at("a careful blot includes")
        self.play(FadeIn(ctl), FadeIn(lc), run_time=0.8)
        self.at("averages millions")
        self.play(FadeIn(t4), FadeIn(cells), FadeIn(lcell), run_time=0.7)
        self.play(GrowArrow(ar), FadeIn(band4), FadeIn(lone), run_time=0.8)
        self.finish()


class S05End(EndCard):
    LINE = "Blot the same samples for the whole protein as well."
