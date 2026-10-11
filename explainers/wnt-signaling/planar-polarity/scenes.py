"""Frizzled and the Fly Wing's Hairs  (Biochemistrypedia section film, Wnt signaling lesson)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a normal cell's hair (and the normal-cell label)
  RED    = lacking frizzled (the patch), and ruled out (crossed-out chips)
  YELLOW = misdirected hairs
  TEAL   = the Frizzled protein
  PURPLE = Wnt
  ORANGE = the actin bundle
  GREY   = cells, membrane, labels
  TEXT   = rings around the neighbours being asked about

No molecular structures: the sheet is a grid of cells (idealised, not to scale), hairs are arrows,
Frizzled is a labelled blob on a membrane bar.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

S = 0.95          # cell pitch
NC, NR = 10, 5
BAND = (4, 5)     # columns of the patch
BROWS = (1, 2)    # rows of the (small) patch
TIPC, OTHC = 6, 3  # tip-side column, other-side column


def pos(c, r):
    return np.array([(c - (NC - 1) / 2) * S, (2 - r) * S - 0.2, 0.0])


def make_cell(c, r):
    return Square(S * 0.88, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.10).move_to(pos(c, r))


def make_hair(c, r, color=BLUE):
    p = pos(c, r)
    return Arrow(p + [-0.27, 0, 0], p + [0.27, 0, 0], buff=0, color=color, stroke_width=6, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.6)


def sheet(skip_hairs=False):
    cells = [[make_cell(c, r) for c in range(NC)] for r in range(NR)]
    hairs = [[make_hair(c, r) for c in range(NC)] for r in range(NR)]
    return cells, hairs


def side_labels():
    base = T("base", 24, GREY).move_to([-5.6, -0.2, 0])
    tip = T("tip", 24, GREY).move_to([5.55, -0.2, 0])
    return base, tip


def col_box(c, color=TEXT):
    w, h = S * 0.98, len(BROWS) * S + 0.05
    r = Rectangle(width=w, height=h, stroke_width=3)
    r = DashedVMobject(r, num_dashes=30).set_color(color)
    return r.move_to((pos(c, BROWS[0]) + pos(c, BROWS[-1])) / 2)


def qmark(c, r):
    return T("?", 40, YELLOW, weight=BOLD).move_to(pos(c, r))


def patch_label():
    nf = chip("no frizzled", RED, size=24).move_to([0, -3.05, 0])
    ln = DashedLine([0, pos(4, 2)[1] - 0.45, 0], nf.get_top(), color=RED, stroke_width=3)
    return nf, ln


def flat(m):
    return VGroup(*[x for row in m for x in row])


def static_sheet(scene, band=False, mis=False, boxes=False):
    """Rebuild the sheet in the state a previous scene ended in; returns (cells, hairs, extras)."""
    cells, hairs = sheet()
    base, tip = side_labels()
    scene.add(flat(cells), base, tip)
    for r in range(NR):
        for c in range(NC):
            if band and c in BAND and r in BROWS:
                cells[r][c].set_fill(RED, 0.35).set_stroke(RED)
            else:
                scene.add(hairs[r][c])
    if mis:
        for r in BROWS:
            scene.remove(hairs[r][TIPC])
            scene.add(qmark(TIPC, r))
    ex = []
    if boxes:
        for c in (OTHC, TIPC):
            b = col_box(c); scene.add(b); ex.append(b)
    return cells, hairs, (base, tip, ex)


class S00Title(TitleCard):
    LESSON = "Wnt Signaling"
    TITLE = "Frizzled and the Fly Wing's Hairs"


class S01Hairs(SpokenScene):
    def construct(self):
        cells, hairs = sheet()
        base, tip = side_labels()
        self.play(LaggedStart(*[FadeIn(c) for c in flat(cells)], lag_ratio=0.02), run_time=1.3)
        self.at("Each cell grows one hair")
        self.play(LaggedStart(*[GrowArrow(h) for h in flat(hairs)], lag_ratio=0.02), run_time=1.6)
        self.at("points toward the")
        self.play(FadeIn(base), FadeIn(tip, shift=LEFT * 0.2),
                  *[Indicate(hairs[r][NC - 1], color=BLUE, scale_factor=1.3) for r in range(NR)], run_time=1.2)
        self.at("planar cell polarity")
        lab = chip("planar cell polarity (PCP)", TEAL, size=26).move_to([0, 3.0, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), run_time=0.8)
        self.at("see the whole sheet")
        ring = SurroundingRectangle(cells[2][4], color=TEXT, buff=0.04, stroke_width=4)
        others = VGroup(*[cells[r][c] for r in range(NR) for c in range(NC) if (r, c) != (2, 4)],
                        *[hairs[r][c] for r in range(NR) for c in range(NC) if (r, c) != (2, 4)])
        self.play(Create(ring), others.animate.set_opacity(0.25), run_time=1.0)
        self.at("which way to point")
        q = chip("which way?", YELLOW, size=26).move_to([0, 3.0, 0])
        self.play(ReplacementTransform(lab, q), Rotate(hairs[2][4], angle=2 * PI * 1.5, about_point=pos(4, 2)),
                  run_time=2.2)
        self.finish()


class S02Patch(SpokenScene):
    def construct(self):
        cells, hairs, (base, tip, _) = static_sheet(self)
        self.at("University of Virginia")
        uva = chip("University of Virginia, 1987", TEAL, size=24)
        vin = chip("Charles Vinson", GREY, size=24)
        ad = chip("Paul Adler", GREY, size=24)
        row = VGroup(uva).move_to([0, 3.0, 0])
        self.play(FadeIn(uva, shift=DOWN * 0.15), run_time=0.7)
        self.at("Charles Vinson")
        both = VGroup(uva, vin, ad).arrange(RIGHT, buff=0.3).move_to([0, 3.0, 0])
        self.play(uva.animate.move_to(both[0]), FadeIn(vin.move_to(both[1])), FadeIn(ad.move_to(both[2])),
                  run_time=0.8)
        self.at("made patches")
        anims = []
        for r in BROWS:
            for c in BAND:
                anims += [cells[r][c].animate.set_fill(RED, 0.35).set_stroke(RED), FadeOut(hairs[r][c])]
        self.play(*anims, run_time=1.0)
        nf, nln = patch_label()
        note = T("(patch hairs not shown)", 22, GREY).move_to([3.7, -3.05, 0])
        self.play(FadeIn(nf, shift=UP * 0.15), Create(nln), FadeIn(note), run_time=0.8)
        self.at("The rest of each wing was normal")
        self.wait(0.6)
        self.at("beside a patch notice")
        bo, bt = col_box(OTHC), col_box(TIPC)
        nn = T("normal neighbours?", 28, TEXT).move_to([0, 3.0, 0])
        self.play(FadeOut(both), Create(bo), Create(bt), FadeIn(nn), run_time=1.0)
        self.finish()


class S03Seen(SpokenScene):
    def construct(self):
        cells, hairs, (base, tip, boxes) = static_sheet(self, band=True, boxes=True)
        nf, nln = patch_label()
        note = T("(patch hairs not shown)", 22, GREY).move_to([3.7, -3.05, 0])
        self.add(nf, nln, note)
        self.at("on the tip side")
        self.play(Indicate(boxes[1], color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.at("grew misdirected hairs")
        qs = [qmark(TIPC, r) for r in BROWS]
        self.play(*[FadeOut(hairs[r][TIPC]) for r in BROWS], *[FadeIn(q, scale=0.5) for q in qs], run_time=1.0)
        mis = chip("misdirected", YELLOW, size=24).move_to([pos(TIPC, 0)[0] + 0.35, 3.0, 0])
        self.play(FadeIn(mis, shift=DOWN * 0.15), run_time=0.6)
        self.at("on the other side")
        self.play(Indicate(boxes[0], color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("did not")
        norm = chip("normal", BLUE, size=24).move_to([pos(OTHC, 0)[0] - 0.35, 3.0, 0])
        self.play(FadeIn(norm, shift=DOWN * 0.15), run_time=0.6)
        nd = T("(direction not shown)", 22, GREY).move_to([-3.7, -3.05, 0])
        self.play(FadeIn(nd), run_time=0.5)
        self.at("but on one side only")
        self.play(Indicate(mis, color=YELLOW, scale_factor=1.12), Indicate(norm, color=BLUE, scale_factor=1.12),
                  run_time=1.2)
        self.finish()


class S04Cloned(SpokenScene):
    def construct(self):
        cells, hairs, (base, tip, boxes) = static_sheet(self, band=True, mis=True, boxes=True)
        nf, nln = patch_label()
        self.add(nf, nln)
        self.at("Two years later")
        later = chip("Adler's laboratory, two years later", TEAL, size=24).move_to([-2.2, 3.0, 0])
        gene = chip("frizzled", TEAL, size=34).move_to([-3.2, 0.9, 0])
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(later), run_time=0.8)
        self.at("cloned frizzled")
        self.play(FadeIn(gene, scale=0.8), run_time=0.7)
        self.at("membrane protein")
        bar = Rectangle(width=5.4, height=0.3, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                        fill_opacity=0.5).move_to([-3.2, 0.9, 0])
        blob = RoundedRectangle(corner_radius=0.3, width=0.9, height=1.6, stroke_color=TEAL, stroke_width=4,
                                fill_color=TEAL, fill_opacity=0.35).move_to([-3.2, 0.9, 0])
        lab = T("seven-pass membrane protein", 24, TEAL).move_to([-3.2, 2.2, 0])
        fz = T("Frizzled", 28, TEAL, weight=BOLD).move_to([-3.2, -0.2, 0])
        self.play(FadeOut(gene), GrowFromCenter(bar), FadeIn(blob, scale=0.6), run_time=1.0)
        self.play(FadeIn(lab, shift=DOWN * 0.1), FadeIn(fz), run_time=0.7)
        self.at("receptor family")
        wr = chip("Wnt receptor family", PURPLE, size=24).move_to([2.0, 0.9, 0])
        self.play(FadeIn(wr, shift=LEFT * 0.1), run_time=0.6)
        self.at("named for untidy hairs")
        tag = T("named for untidy\nhairs on a fly", 24, TEXT).move_to([2.0, -0.35, 0])
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.8)
        self.at("does not use")
        bc, tc = chip("β-catenin", GREY, size=26), chip("TCF", GREY, size=26)
        pair = VGroup(bc, tc).arrange(RIGHT, buff=0.4).move_to([3.3, 2.5, 0])
        self.play(FadeIn(pair), run_time=0.6)
        crs = [Line(m.get_corner(DL), m.get_corner(UR), color=RED, stroke_width=7) for m in (bc, tc)]
        self.play(*[Create(x) for x in crs], run_time=0.6)
        self.at("actin bundle")
        cell = Square(1.3, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.10).move_to([-0.2, -2.45, 0])
        spot = Circle(0.2, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.8).move_to(
            cell.get_right() + LEFT * 0.2)
        act = chip("actin bundle", ORANGE, size=24).move_to([3.6, -1.9, 0])
        ln = Line(act.get_left() + DOWN * 0.1, spot.get_top() + UP * 0.02, color=ORANGE, stroke_width=3)
        self.play(FadeIn(cell), FadeIn(spot, scale=0.5), run_time=0.6)
        self.play(FadeIn(act), Create(ln), run_time=0.6)
        self.at("becomes its hair")
        hair = Arrow(spot.get_right(), spot.get_right() + RIGHT * 1.5, buff=0, color=BLUE, stroke_width=7,
                     tip_length=0.25).shift(RIGHT * 0.02)
        self.play(GrowArrow(hair), run_time=1.0)
        self.finish()


class S05End(EndCard):
    LINE = "The gene that points the wing's hairs encodes Frizzled."
