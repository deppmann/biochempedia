"""The Switch Inside the Molecule  (Biochemistrypedia: Protein binding & allostery, chapter 4)

COLOR MAP (one color per concept, whole series; same as chapters 1-3)
  BLUE   = the T (tense, weak-grip) shape
  GREEN  = the R (relaxed, tight-grip) shape; "carries O2"
  YELLOW = O2, the ligand
  RED    = a cross (cannot carry oxygen)
  TEAL   = 2,3-BPG (later chapters)
  GOLD   = call-outs, bonds being counted, salt bridges, step badges, the odds dial needle events
  TEXT   = neutral labels (histidines);  GREY = secondary labels, leader lines, axes
  Added here: ACOL (pink) = alpha chains; BCOL (lavender) = beta chains (chain identity, never a state);
  HEME (orange) = the heme ring; IRON (silver) = the iron; HELIX (violet) = the F helix;
  WATER (pale blue) = a water molecule, used only as a size ruler.
NO molecular structures are drawn: a flat disk stands for the heme seen at a tilt, two slabs with a gap
for the heme seen edge-on, chips for the histidines, a labelled cylinder for the F helix, blocks for chains.
Model numbers (the lesson's one illustrative two-state fit): R site K = 0.37 torr, T site K = 110 torr,
T outnumbers R 1.7e7 to 1 with no O2 bound. So each bound O2 multiplies the R:T odds by 110/0.37 = 297,
and the R:T odds with i oxygens bound are 297**i / 1.7e7. The s15 dial and the s16 bar are computed from that.
Geometry: proximal His below the ring, O2 above. Deoxy iron sits out of the plane on the His side, so the
move on binding is UP, into the plane.
"""
import numpy as np

from bp_style import *

HEME = "#E8935A"
IRON = "#C9CED6"
HELIX = "#C792EA"
WATER = "#7FB3D5"
ACOL = "#F49AC1"
BCOL = "#AEB8F7"
GREEK = "Georgia"

CX, RY = -0.5, 0.5           # centre of the heme on screen (same in s03-s11)
FACE_W, FACE_H = 8.0, 3.3    # heme seen at a tilt
SLAB_H, GAP = 0.45, 0.70     # heme seen edge-on: two slabs and the central hole
FE_HI, FE_LO = 0.42, 0.29    # high-spin iron is too big for the gap; low-spin fits
DROP = 0.80                  # drawn out-of-plane offset (0.4 angstrom, not to scale)
FBOND = 1.95                 # same, in the face view (taller ring)
BOND = 1.70                  # iron centre to the top of the proximal His chip
L_FIT, K_RATIO = 1.7e7, 110 / 0.37


def r_odds(i):
    return K_RATIO ** i / L_FIT


# ------------------------------------------------------------------ small pieces
def o2(r=0.32):
    c = Circle(radius=r, color=YELLOW, fill_opacity=1, stroke_width=0)
    return VGroup(c, T("O₂", 24, BG, weight=BOLD).move_to(c))


def leader(lab, pt, buff=0.08):
    pt = np.array([pt[0], pt[1], 0.0])
    cands = [lab.get_left(), lab.get_right(), lab.get_top(), lab.get_bottom()]
    s = min(cands, key=lambda p: np.linalg.norm(p - pt))
    d = pt - s
    n = np.linalg.norm(d)
    return Line(s + d / n * buff, pt, color=GREY, stroke_width=2.5)


def opaque_chip(text, color=TEXT, size=28):
    c = chip(text, color, size)
    bg = RoundedRectangle(corner_radius=0.14, width=c.width, height=c.height, stroke_width=0,
                          fill_color=BG, fill_opacity=1).move_to(c)
    return VGroup(bg, c)


def badge(n):
    return chip(f"Step {n} of 4", GOLD, 28).move_to([-5.0, 3.3, 0])


def tag(s, color):
    return chip(s, color, 34).move_to([5.9, 3.3, 0])


def face_ring(cx=CX, cy=RY, w=FACE_W, h=FACE_H):
    r = Ellipse(width=w, height=h, stroke_color=HEME, stroke_width=3, fill_color=HEME, fill_opacity=0.28)
    hole = Ellipse(width=0.1 * w, height=0.1 * h, stroke_color=HEME, stroke_width=1.5, fill_color=BG,
                   fill_opacity=0.95)
    return VGroup(r, hole).move_to([cx, cy, 0])


def side_ring():
    w = FACE_W / 2 - GAP / 2
    l = RoundedRectangle(corner_radius=0.12, width=w, height=SLAB_H, stroke_color=HEME, stroke_width=3,
                         fill_color=HEME, fill_opacity=0.4).move_to([CX - GAP / 2 - w / 2, RY, 0])
    r = l.copy().move_to([CX + GAP / 2 + w / 2, RY, 0])
    return VGroup(l, r)


def fe_static(pos, r=0.36):
    p = np.array([pos[0], pos[1], 0.0])
    c = Circle(radius=r, stroke_width=0, fill_color=IRON, fill_opacity=1).move_to(p)
    return VGroup(c, T("Fe", 22, BG, weight=BOLD).move_to(p))


def container():
    box = RoundedRectangle(corner_radius=0.3, width=12.3, height=7.3, stroke_color=ACOL, stroke_width=3,
                           fill_color=ACOL, fill_opacity=0.06).move_to([0, 0.15, 0])
    lab = T("one α chain", 28, ACOL, font=GREEK).move_to([-5.0, -3.1, 0])
    return VGroup(box, lab)


def heme_labels():
    hl = T("heme", 30, HEME).move_to([-4.7, 2.7, 0])
    pl = VGroup(T("protoporphyrin IX", 28, HEME), T("ring", 28, HEME)).arrange(DOWN, buff=0.08).move_to([4.2, -1.8, 0])
    a = FACE_W / 2, FACE_H / 2
    p1 = [CX + a[0] * np.cos(2.3), RY + a[1] * np.sin(2.3)]
    p2 = [CX + a[0] * np.cos(-0.75), RY + a[1] * np.sin(-0.75)]
    return VGroup(hl, leader(hl, p1)), VGroup(pl, leader(pl, p2))


# ------------------------------------------------------------------ tetramer blocks
def tet(c=(0, 0), bs=1.6, gx=0.5, gy=0.25, fill=BLUE, op=0.2, lsize=40, letters=True):
    """[0] = left dimer (alpha over beta), [1] = right dimer (beta over alpha). Block = (rect, letter)."""
    c = np.array([c[0], c[1], 0.0])
    dx, dy = bs / 2 + gx / 2, bs / 2 + gy / 2

    def b(lab, x, y):
        r = RoundedRectangle(corner_radius=0.12 * bs, width=bs, height=bs, stroke_color=fill, stroke_width=3,
                             fill_color=fill, fill_opacity=op)
        g = VGroup(r)
        if letters:
            g.add(T(lab, lsize, ACOL if lab == "α" else BCOL, font=GREEK).move_to(r))
        return g.move_to(c + np.array([x, y, 0]))

    return VGroup(VGroup(b("α", -dx, dy), b("β", -dx, -dy)), VGroup(b("β", dx, dy), b("α", dx, -dy)))


def dim_out(d, buff=0.15):
    return SurroundingRectangle(d, color=GREY, buff=buff, corner_radius=0.2, stroke_width=2.5)


def recolor(blocks, color, op=0.2):
    return [b[0].animate.set_stroke(color).set_fill(color, op) for b in blocks]


def blocks_of(t):
    return [b for d in t for b in d]


# ------------------------------------------------------------------ heme stage (s03-s11)
class HemeScene(SpokenScene):
    def fe_live(self, dy=0.0, r=0.36):
        self.fy, self.fr = ValueTracker(dy), ValueTracker(r)
        fe = fe_static([CX, RY + dy], r).set_z_index(6)

        def up(m):
            p = np.array([CX, RY + self.fy.get_value(), 0])
            m[0].become(Circle(radius=self.fr.get_value(), stroke_width=0, fill_color=IRON, fill_opacity=1).move_to(p))
            m[1].move_to(p)

        fe.add_updater(up)
        self.fe = fe
        return fe

    def fe_pos(self):
        return np.array([CX, RY + self.fy.get_value(), 0])

    def his_live(self, text="proximal His", top_y=None, dx=0.0):
        h = opaque_chip(text, TEXT, 28).set_z_index(5)
        self.hy = ValueTracker(top_y if top_y is not None else RY - DROP - BOND)
        self.hx = ValueTracker(dx)
        h.add_updater(lambda m: m.move_to([CX + self.hx.get_value(), self.hy.get_value() - m.height / 2, 0]))
        h.update()
        self.his = h
        bond = Line(ORIGIN, UP, color=GREY, stroke_width=5).set_z_index(4)
        bond.add_updater(lambda m: m.put_start_and_end_on(self.fe_pos(), h.get_top()))
        bond.update()
        self.bond = bond
        return h, bond

    def o2_live(self, pos):
        ox = o2().move_to(pos).set_z_index(7)
        lk = Line(ORIGIN, UP, color=YELLOW, stroke_width=5).set_z_index(5)
        lk.add_updater(lambda m: m.put_start_and_end_on(self.fe_pos(), ox.get_center()))
        lk.update()
        return ox, lk


O2_FACE = np.array([CX + 1.0, RY + 2.35, 0])
O2_SIDE = np.array([CX + 0.55, RY + 1.25, 0])


# ------------------------------------------------------------------ cards
class S00Title(TitleCard):
    LESSON = "Protein Binding and Allostery: How Hemoglobin Loads and Delivers Oxygen"
    TITLE = "The Switch Inside the Molecule"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = fit(T(self.LESSON.upper(), size=22, color=GREY), max_w=10.5)
        title = T(self.TITLE, size=56, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.34).move_to(ORIGIN)
        self.play(FadeIn(brand), FadeIn(lesson), FadeIn(title, shift=UP * 0.1), GrowFromCenter(rule), run_time=0.8)
        self.wait(1.7)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()


class S21End(EndCard):
    LINE = "A tiny shift at one iron, levered through a helix, raises the odds that the whole molecule turns to R."

    def construct(self):
        l1 = T("A tiny shift at one iron, levered through a helix,", size=44, font=TITLE_FONT)
        l2 = T("raises the odds that the whole molecule turns to R.", size=44, font=TITLE_FONT)
        line = VGroup(l1, l2).arrange(DOWN, buff=0.28)
        fit(line, max_w=12.0)
        sub = T("biochemistrypedia.com", size=24, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(sub), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ s01: the question, zoom into one heme
class S01Q(SpokenScene):
    def construct(self):
        q = T("Why does R grip harder?", 46).move_to([0, 3.15, 0])
        tT = tet((-3.4, -0.1), 1.5, 0.4, fill=BLUE, lsize=40)
        tR = tet((3.4, -0.1), 1.5, 0.4, fill=GREEN, lsize=40)
        lT = T("T", 44, BLUE).move_to([-3.4, -2.55, 0])
        lR = T("R", 44, GREEN).move_to([3.4, -2.55, 0])
        # a tiny heme inside T's top-left alpha block: the zoom target
        blk = tT[0][0]
        small = VGroup(face_ring(0, 0, 1.1, 0.42), T("Fe", 22, WHITE, weight=BOLD)).move_to(blk[0].get_center() + DOWN * 0.35)
        blk[1].shift(UP * 0.2)
        self.play(FadeIn(q), FadeIn(tT), FadeIn(tR), FadeIn(lT), FadeIn(lR), FadeIn(small), run_time=0.8)
        self.at("hold oxygen better")
        oR = VGroup(*[o2().move_to(b[0].get_corner(UR) + np.array([-0.05, -0.05, 0])) for b in blocks_of(tR)])
        oT = o2().move_to(tT[1][0][0].get_corner(UR) + np.array([-0.05, -0.05, 0]))
        gR = T("tight grip", 30, GREEN).next_to(lR, RIGHT, buff=0.35)
        gT = T("weak grip", 30, BLUE).next_to(lT, RIGHT, buff=0.35)
        self.play(LaggedStart(*[FadeIn(o, scale=0.5) for o in oR], lag_ratio=0.15), FadeIn(oT, scale=0.5),
                  FadeIn(gR), run_time=0.9)
        self.play(oT.animate.shift(RIGHT * 0.9 + UP * 0.6).set_opacity(0), FadeIn(gT), run_time=0.9)
        self.remove(oT)
        self.at("answer starts")
        box = container()[0]
        big = VGroup(face_ring(), fe_static([CX, RY], 0.36).set_z_index(6))
        p = blk[0].get_center()
        others = VGroup(tT[0][1], tT[1], tR, lT, lR, gT, gR, oR, blk[1])
        self.play(others.animate.scale(4, about_point=p).set_opacity(0), ReplacementTransform(blk[0], box),
                  ReplacementTransform(small, big), FadeOut(q), run_time=1.2)
        self.remove(others)
        self.at("smaller than")
        fe = big[1]
        arr = DoubleArrow([CX + 0.75, RY - 0.45, 0], [CX + 0.75, RY + 0.45, 0], color=GOLD, buff=0,
                          stroke_width=6, tip_length=0.16, max_tip_length_to_length_ratio=0.3).set_z_index(7)
        lab = T("moves less than an atom's width", 30, GOLD).move_to([CX + 0.75, -1.75, 0])
        ld = leader(lab, arr.get_bottom())
        self.play(fe.animate.shift(DOWN * 0.3), FadeIn(arr), run_time=0.5)
        self.play(fe.animate.shift(UP * 0.3), FadeIn(lab), Create(ld), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ s02: four chains, two dimers
class S02Parts(SpokenScene):
    def construct(self):
        t = tet((0, 0.35), 2.25, 1.2, 0.3, fill=GREY, op=0.12, lsize=64)
        rects = VGroup(*[b[0] for b in blocks_of(t)])
        al = [t[0][0], t[1][1]]
        be = [t[0][1], t[1][0]]
        self.play(FadeIn(rects, scale=0.95), run_time=0.7)
        self.at("four chains")
        self.play(LaggedStart(*[Indicate(r, color=TEXT, scale_factor=1.04) for r in rects], lag_ratio=0.2), run_time=0.9)
        self.at("two alpha")
        self.play(*[b[0].animate.set_stroke(ACOL).set_fill(ACOL, 0.18) for b in al], *[Write(b[1]) for b in al],
                  run_time=0.55)
        self.at("two beta")
        self.play(*[b[0].animate.set_stroke(BCOL).set_fill(BCOL, 0.18) for b in be], *[Write(b[1]) for b in be],
                  run_time=0.55)
        self.at("pair up")
        oL, oR = dim_out(t[0]), dim_out(t[1])
        self.play(Create(oL), Create(oR), run_time=0.8)
        self.at("dimers")
        lL = T("αβ dimer", 32, TEXT, font=GREEK).next_to(oL, DOWN, buff=0.2)
        lR = T("αβ dimer", 32, TEXT, font=GREEK).next_to(oR, DOWN, buff=0.2)
        self.play(FadeIn(lL, shift=UP * 0.1), FadeIn(lR, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ s03: heme
class S03Heme(HemeScene):
    def construct(self):
        t = tet((0, 0.35), 2.25, 1.2, 0.3, fill=GREY, op=0.12, lsize=64)
        for b in (t[0][0], t[1][1]):
            b[0].set_stroke(ACOL).set_fill(ACOL, 0.18)
        for b in (t[0][1], t[1][0]):
            b[0].set_stroke(BCOL).set_fill(BCOL, 0.18)
        self.add(t)
        box = container()
        others = VGroup(t[0][1], t[1], t[0][0][1])
        self.play(FadeOut(others), ReplacementTransform(t[0][0][0], box[0]), run_time=0.8)
        self.play(FadeIn(box[1]), run_time=0.3)
        self.at("one heme")
        rg = face_ring()
        hl, pl = heme_labels()
        self.play(GrowFromCenter(rg), run_time=0.6)
        self.play(FadeIn(hl[0]), Create(hl[1]), run_time=0.4)
        self.at("ring protoporphyrin")
        self.play(Indicate(rg[0], color=HEME, scale_factor=1.04), FadeIn(pl[0]), Create(pl[1]), run_time=0.8)
        self.at("iron at")
        fe = fe_static([CX, RY]).set_z_index(6)
        self.play(GrowFromCenter(fe), run_time=0.5)
        self.play(Indicate(fe, color=GOLD, scale_factor=1.3), run_time=0.6)
        self.finish()


N_POS = [(-2.3, 0.0), (2.3, 0.0), (-0.8, 0.98), (0.8, -0.98)]


def n_parts():
    pts = [np.array([CX + x, RY + y, 0]) for x, y in N_POS]
    ns = VGroup(*[Circle(radius=0.24, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(p) for p in pts])
    nt = VGroup(*[T("N", 24, BG, weight=BOLD).move_to(p) for p in pts])
    bonds = VGroup(*[Line([CX, RY, 0], p, color=GOLD, stroke_width=6, buff=0.0) for p in pts])
    return pts, VGroup(ns, nt).set_z_index(5), bonds.set_z_index(3)


# ------------------------------------------------------------------ s04: five bonds
class S04Bonds(HemeScene):
    def construct(self):
        box = container()
        rg = face_ring()
        hl, pl = heme_labels()
        fe = self.fe_live(0.0, 0.36)
        self.add(box, rg, hl, pl, fe)
        pts, ns, bonds = n_parts()
        self.wait(0.3)
        self.at("four bonds")
        self.play(LaggedStart(*[Create(b) for b in bonds], lag_ratio=0.2), run_time=0.9)
        self.at("nitrogens")
        self.play(LaggedStart(*[FadeIn(VGroup(ns[0][i], ns[1][i]), scale=1.4) for i in range(4)], lag_ratio=0.15),
                  run_time=0.7)
        self.at("fifth bond")
        h, bond = self.his_live("His", top_y=RY - FBOND)
        bond.clear_updaters()
        bond.put_start_and_end_on(np.array([CX, RY, 0]), h.get_top()).set_color(GOLD)
        self.play(Create(bond), run_time=0.7)
        self.at("histidine below")
        self.play(FadeIn(h, shift=UP * 0.15), run_time=0.5)
        self.at("proximal histidine")
        h2 = opaque_chip("proximal His", TEXT, 28).move_to(h).set_z_index(5)
        h.clear_updaters()
        self.play(ReplacementTransform(h, h2), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ s05: sixth site, distal His
class S05Sixth(HemeScene):
    def construct(self):
        box = container()
        rg = face_ring()
        hl, pl = heme_labels()
        fe = self.fe_live(0.0, 0.36)
        pts, ns, bonds = n_parts()
        h, bond = self.his_live("proximal His", top_y=RY - FBOND)
        self.add(box, rg, hl, pl, bonds, ns, fe, h, bond)
        self.wait(0.15)
        self.at("sixth site")
        slot = DashedVMobject(Circle(radius=0.32, color=YELLOW, stroke_width=4), num_dashes=14).move_to(O2_FACE)
        sline = DashedLine([CX, RY, 0], O2_FACE, color=YELLOW, stroke_width=3).set_opacity(0.6)
        sl = T("sixth site: empty", 30, YELLOW).move_to([CX - 2.0, 3.2, 0])
        sld = leader(sl, slot.get_left() + LEFT * 0.05)
        self.play(Create(slot), Create(sline), FadeIn(sl), Create(sld), run_time=0.8)
        self.at("for oxygen")
        ox, lk = self.o2_live(O2_FACE + np.array([3.0, 0.9, 0]))
        lk.set_opacity(0)
        self.add(ox)
        self.play(ox.animate.move_to(O2_FACE), FadeOut(sl), FadeOut(sld), run_time=0.7)
        self.add(lk)
        lk.set_opacity(1)
        self.remove(slot, sline)
        self.at("distal histidine")
        dh = opaque_chip("distal His", TEXT, 28).move_to(O2_FACE + np.array([2.3, 0.3, 0])).set_z_index(5)
        self.play(FadeIn(dh, shift=DOWN * 0.15), run_time=0.6)
        self.at("hydrogen bonds")
        hb = DashedLine(dh.get_left() + DOWN * 0.1, ox.get_center() + np.array([0.24, 0.2, 0]), color=GOLD,
                        stroke_width=5, dash_length=0.09)
        hbl = T("hydrogen bond", 28, GOLD).move_to([4.5, 1.9, 0])
        hbd = leader(hbl, hb.get_center())
        self.play(Create(hb), FadeIn(hbl), Create(hbd), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ s06: ferrous vs ferric
class S06Ferrous(SpokenScene):
    def construct(self):
        lx, rx, y = -3.3, 3.3, 0.9

        def heme_at(x):
            return VGroup(face_ring(x, y, 6.0, 2.4), fe_static([x, y], 0.36).set_z_index(6))

        hL = heme_at(lx)
        oxL = o2().move_to([lx + 0.8, y + 1.7, 0]).set_z_index(7)
        lkL = Line([lx, y, 0], oxL.get_center(), color=YELLOW, stroke_width=5).set_z_index(5)
        self.add(hL, lkL, oxL)
        self.wait(0.1)
        self.at("iron must stay")
        self.play(Indicate(hL[1], color=GOLD, scale_factor=1.3), run_time=0.6)
        self.at("in its")
        labL = T("Fe²⁺", 52, GREEN, weight=BOLD).move_to([lx, -1.15, 0])
        self.play(FadeIn(labL, shift=UP * 0.1), run_time=0.5)
        self.at("oxidized")
        hR = heme_at(rx)
        hR[1][0].set_fill("#6E7584", 1)
        labR = T("Fe³⁺", 52, GREY, weight=BOLD).move_to([rx, -1.15, 0])
        self.play(FadeIn(hR), run_time=0.5)
        self.play(FadeIn(labR, shift=UP * 0.1), run_time=0.4)
        self.at("methemoglobin")
        mh = T("methemoglobin", 34, RED).next_to(labR, DOWN, buff=0.3)
        self.play(FadeIn(mh), run_time=0.5)
        self.at("cannot carry")
        slot = DashedVMobject(Circle(radius=0.32, color=RED, stroke_width=4), num_dashes=14).move_to([rx + 0.8, y + 1.7, 0])
        cross = VGroup(Line(UL * 0.22, DR * 0.22), Line(UR * 0.22, DL * 0.22)).set_stroke(RED, 6).move_to(slot)
        no = T("no O₂", 32, RED).next_to(slot, RIGHT, buff=0.3)
        ok = T("carries O₂", 32, GREEN).next_to(labL, DOWN, buff=0.3)
        self.play(Create(slot), Create(cross), FadeIn(no), FadeIn(ok), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ s07: step 1, side view, iron out of plane
def side_labels():
    up = T("O₂ side", 28, YELLOW).move_to([CX - 2.4, RY + 0.75, 0])
    dn = T("proximal side", 28, TEXT).move_to([CX - 2.4, RY - 0.75, 0])
    hm = T("heme, edge-on", 28, HEME).move_to([CX + 2.4, RY + 0.75, 0])
    return VGroup(up, dn, hm)


def bracket_parts():
    xr = CX + FACE_W / 2
    top = DashedLine([xr + 0.1, RY, 0], [xr + 1.0, RY, 0], color=GREY, stroke_width=3)
    low = DashedLine([CX + FE_HI + 0.1, RY - DROP, 0], [xr + 1.0, RY - DROP, 0], color=GREY, stroke_width=3)
    br = DoubleArrow([xr + 0.75, RY - DROP, 0], [xr + 0.75, RY, 0], color=GOLD, buff=0, stroke_width=6,
                     tip_length=0.14, max_tip_length_to_length_ratio=0.4)
    lb = M("0.4 Å", 30, GOLD).move_to([xr + 1.75, RY - DROP / 2, 0])
    ns = T("not to scale", 24, GREY).next_to(lb, DOWN, buff=0.15)
    return top, low, br, lb, ns


def spin_label(txt, color, fe_pt):
    lab = T(txt, 28, color).move_to([CX + 2.6, RY - 1.35, 0])
    return VGroup(lab, leader(lab, fe_pt))


def halo():
    return Rectangle(width=GAP + 0.04, height=SLAB_H + 0.18, stroke_color=GOLD, stroke_width=4).move_to([CX, RY, 0])


class S07Step1(HemeScene):
    def construct(self):
        rg = face_ring()
        fe = self.fe_live(0.0, 0.36)
        h, bond = self.his_live("proximal His", top_y=RY - FBOND)
        self.add(rg, fe, h, bond)
        self.play(FadeIn(badge(1)), run_time=0.4)
        sl = side_labels()
        self.play(ReplacementTransform(rg, side_ring()), self.fr.animate.set_value(FE_HI), run_time=1.0)
        self.play(FadeIn(sl), run_time=0.4)
        self.at("tea")
        self.play(FadeIn(tag("T", BLUE), scale=1.3), self.fy.animate.set_value(-DROP),
                  self.hy.animate.set_value(RY - DROP - BOND), run_time=0.9)
        self.at("high spin")
        sp = spin_label("high-spin iron", TEXT, [CX + FE_HI * 0.8, RY - DROP - 0.2])
        self.play(FadeIn(sp[0]), Create(sp[1]), run_time=0.5)
        self.at("too big")
        tb = T("too big for the hole", 30, GOLD).move_to([CX, RY + 2.0, 0])
        ar = Arrow(tb.get_bottom(), [CX, RY + SLAB_H / 2 + 0.15, 0], color=GOLD, buff=0.1, stroke_width=5)
        self.play(FadeIn(tb), GrowArrow(ar), Indicate(fe[0], color=GOLD, scale_factor=1.15), run_time=0.7)
        self.at("ring's hole")
        hal = halo()
        self.play(Create(hal), run_time=0.5)
        self.at("sits about")
        top, low, br, lb, ns = bracket_parts()
        self.play(Create(top), Create(low), run_time=0.3)
        self.at("about 0")
        self.play(GrowFromCenter(br), FadeIn(lb), FadeIn(ns), run_time=0.6)
        self.at("toward the histidine")
        self.play(Indicate(h, color=GOLD, scale_factor=1.08), run_time=0.7)
        self.finish()


def s07_state(sc, with_tb=True):
    sc.add(side_ring())
    fe = sc.fe_live(-DROP, FE_HI)
    h, bond = sc.his_live("proximal His", top_y=RY - DROP - BOND)
    top, low, br, lb, ns = bracket_parts()
    sp = spin_label("high-spin iron", TEXT, [CX + FE_HI * 0.8, RY - DROP - 0.2])
    sl = side_labels()
    sc.add(fe, h, bond, sl, sp, badge(1), tag("T", BLUE), top, low, br, lb, ns)
    out = dict(fe=fe, h=h, bond=bond, top=top, low=low, br=br, lb=lb, ns=ns, sp=sp, sl=sl)
    if with_tb:
        tb = T("too big for the hole", 30, GOLD).move_to([CX, RY + 2.0, 0])
        ar = Arrow(tb.get_bottom(), [CX, RY + SLAB_H / 2 + 0.15, 0], color=GOLD, buff=0.1, stroke_width=5)
        hal = halo()
        sc.add(tb, ar, hal)
        out.update(tb=tb, ar=ar, hal=hal)
    return out


# ------------------------------------------------------------------ s08: the 0.4 A shift next to a water molecule
class S08Scale(HemeScene):
    def construct(self):
        st = s07_state(self)
        U = 0.8                                   # 0.4 angstrom on this ruler; water ~2.8 angstrom = 7 U
        x0 = -7 * U / 2
        keep = st["br"]
        rest = [m for m in self.mobjects if m is not keep]
        seg0 = Rectangle(width=U - 0.05, height=0.42, stroke_width=0, fill_color=GOLD, fill_opacity=0.95)
        seg0.move_to([x0 + U / 2, -0.75, 0])
        self.play(*[FadeOut(m) for m in rest], ReplacementTransform(keep, seg0), run_time=0.7)
        l04 = M("0.4 Å", 30, GOLD).next_to(seg0, LEFT, buff=0.3)
        water = Ellipse(width=7 * U, height=2.2, stroke_color=WATER, stroke_width=3, fill_color=WATER,
                        fill_opacity=0.22).move_to([0, 1.05, 0])
        wt = T("H₂O", 44, WATER, weight=BOLD).move_to(water)
        self.play(FadeIn(l04), run_time=0.2)
        self.at("a seventh")
        segs = VGroup(*[Rectangle(width=U - 0.05, height=0.42, stroke_width=0, fill_color=GOLD,
                                  fill_opacity=0.95 if i % 2 == 0 else 0.5).move_to([x0 + U / 2 + i * U, -0.75, 0])
                        for i in range(1, 7)])
        self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.15) for s_ in segs], lag_ratio=0.18), run_time=1.0)
        self.at("water molecule")
        wl = T("one water molecule", 30, WATER).next_to(water, UP, buff=0.2)
        brc = BraceBetweenPoints([x0, -1.1, 0], [-x0, -1.1, 0], direction=DOWN, color=GREY)
        bl = M("about 2.8 Å  (7 × 0.4 Å)", 30, TEXT).next_to(brc, DOWN, buff=0.15)
        self.play(FadeIn(water), FadeIn(wt), FadeIn(wl), run_time=0.5)
        self.play(GrowFromCenter(brc), FadeIn(bl), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ s09: oxygen binds, iron shrinks and rises
class S09Drop(HemeScene):
    def construct(self):
        st = s07_state(self)
        self.at("oxygen binds")
        ox, lk = self.o2_live(O2_SIDE + np.array([3.6, 1.4, 0]))
        self.add(ox)
        self.play(ox.animate.move_to(O2_SIDE), FadeOut(st["tb"]), FadeOut(st["ar"]), run_time=0.9)
        self.play(Create(lk), run_time=0.3)
        self.at("low spin")
        sp2 = spin_label("low-spin iron", GREEN, [CX + FE_HI * 0.8, RY - DROP - 0.2])
        self.play(ReplacementTransform(st["sp"][0], sp2[0]), run_time=0.5)
        self.at("shrinks")
        sm = T("shrinks", 28, GREEN).next_to(sp2[0], DOWN, buff=0.15)
        self.play(self.fr.animate.set_value(FE_LO), FadeIn(sm), run_time=0.6)
        self.at("rises into the plane")
        up = Arrow([CX + FACE_W / 2 + 0.75, RY - DROP - 0.1, 0], [CX + FACE_W / 2 + 0.75, RY + 0.1, 0], color=GOLD,
                   buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.3)
        lb2 = M("up 0.4 Å", 28, GOLD).next_to(up, RIGHT, buff=0.2)
        self.play(self.fy.animate.set_value(0.0), ReplacementTransform(st["br"], up), FadeOut(st["low"]),
                  ReplacementTransform(st["lb"], lb2), FadeOut(st["sp"][1]), run_time=1.1)
        self.finish()


# ------------------------------------------------------------------ s10: step 2, histidine follows
class S10Step2(HemeScene):
    def construct(self):
        self.add(side_ring())
        fe = self.fe_live(0.0, FE_LO)
        h, bond = self.his_live("proximal His", top_y=RY - DROP - BOND)
        ox, lk = self.o2_live(O2_SIDE)
        sl = side_labels()
        sp = T("low-spin iron", 28, GREEN).move_to([CX + 2.6, RY - 1.35, 0])
        self.add(fe, h, bond, ox, lk, sl, sp, tag("T", BLUE), halo())
        b1 = badge(1)
        self.add(b1)
        self.play(ReplacementTransform(b1, badge(2)), run_time=0.5)
        self.at("iron is bonded")
        bond.set_color(GOLD)
        bl = T("bond pulled long", 28, GOLD).move_to([CX - 2.6, RY - 1.55, 0])
        bld = leader(bl, [CX - 0.08, RY - 1.2, 0])
        self.play(Indicate(bond, color=GOLD, scale_factor=1.0), FadeIn(bl), Create(bld), run_time=0.7)
        self.at("proximal histidine")
        self.play(Indicate(h, color=GOLD, scale_factor=1.12), run_time=0.6)
        self.at("histidine follows")
        y0 = RY - DROP - BOND
        arr = Arrow([CX + 1.9, y0 - 0.45, 0], [CX + 1.9, y0 + DROP - 0.25, 0], color=GOLD, buff=0, stroke_width=7,
                    max_tip_length_to_length_ratio=0.35)
        al = T("pulled up (not to scale)", 28, GOLD).next_to(arr, RIGHT, buff=0.25)
        self.play(self.hy.animate.set_value(y0 + DROP), GrowArrow(arr), FadeIn(al), FadeOut(bl), FadeOut(bld),
                  run_time=1.0)
        self.play(bond.animate.set_color(GREY), run_time=0.3)
        self.finish()


# ------------------------------------------------------------------ s11: step 3, the F helix presses on a neighbour
class S11Step3(HemeScene):
    def construct(self):
        self.add(side_ring())
        fe = self.fe_live(0.0, FE_LO)
        y_his = RY - BOND
        h, bond = self.his_live("proximal His", top_y=y_his)
        ox, lk = self.o2_live(O2_SIDE)
        sl = side_labels()
        self.add(fe, h, bond, ox, lk, sl, tag("T", BLUE), badge(3))
        nb = RoundedRectangle(corner_radius=0.3, width=2.9, height=3.5, stroke_color=BLUE, stroke_width=3,
                              fill_color=BLUE, fill_opacity=0.14)
        nbl = VGroup(T("neighboring", 28, TEXT), T("subunit", 28, TEXT)).arrange(DOWN, buff=0.06)
        nbb = T("β", 60, BCOL, font=GREEK)
        nbg = VGroup(nb, nbl.move_to(nb.get_center() + UP * 0.9), nbb.move_to(nb.get_center() + DOWN * 0.5))
        nbg.move_to([4.85, -1.65, 0])
        self.play(FadeIn(nbg), run_time=0.6)
        self.at("sits on a helix")
        hbot = h.get_bottom()[1]
        cyl = RoundedRectangle(corner_radius=0.36, width=7.4, height=0.78, stroke_color=HELIX, stroke_width=3,
                               fill_color=HELIX, fill_opacity=0.85).move_to([CX - 0.35, hbot - 0.5, 0]).set_z_index(2)
        bands = VGroup(*[Line(UP * 0.36, DOWN * 0.36, color=BG, stroke_width=2).set_opacity(0.35)
                         .move_to([x, cyl.get_center()[1], 0]) for x in np.arange(CX - 3.55, CX + 3.2, 0.55)]).set_z_index(3)
        stem = Line([CX, hbot, 0], [CX, cyl.get_top()[1], 0], color=TEXT, stroke_width=6).set_z_index(3)
        hel = VGroup(cyl, bands, stem)
        self.play(GrowFromEdge(cyl, LEFT), run_time=0.8)
        self.play(FadeIn(bands), Create(stem), run_time=0.3)
        self.at("f helix")
        fl = T("F helix", 32, BG, weight=BOLD).move_to(cyl.get_center() + LEFT * 2.2).set_z_index(4)
        hel.add(fl)
        self.play(FadeIn(fl), run_time=0.4)
        self.at("helix shifts")
        sh = 0.95
        gap = nbg.get_left()[0] - cyl.get_right()[0]
        self.play(hel.animate.shift(RIGHT * min(sh, gap)), self.hx.animate.set_value(min(sh, gap)), run_time=0.9)
        self.at("presses on")
        cp = np.array([cyl.get_right()[0] + 0.02, cyl.get_center()[1], 0])
        flash = Circle(radius=0.35, color=GOLD, stroke_width=6).move_to(cp)
        pl = T("presses", 30, GOLD).move_to([cp[0] - 0.3, cp[1] - 1.05, 0])
        self.play(Create(flash), FadeIn(pl), Rotate(nbg, angle=-6 * DEGREES, about_point=nbg.get_corner(DR)),
                  hel.animate.shift(RIGHT * 0.15), self.hx.animate.increment_value(0.15), run_time=0.8)
        self.play(FadeOut(flash), run_time=0.3)
        self.finish()


# ------------------------------------------------------------------ s12-s13: dimer rotation and salt bridges
C4 = np.array([0.0, -0.25, 0])
BS4, GX4 = 2.4, 1.9


def big_tet():
    t = tet((C4[0], C4[1]), BS4, GX4, 0.3, fill=BLUE, lsize=60)
    for b in blocks_of(t):
        b[1].shift(UP * 0.35)
    left, right = VGroup(t[0], dim_out(t[0])), VGroup(t[1], dim_out(t[1]))
    return t, left, right


def bridge_set(t, right):
    """Two salt bridges in the gap between the dimers; their right ends ride on the right dimer."""
    ys = [C4[1] - 0.5, C4[1] - 2.05]
    xl = t[0][0][0].get_right()[0] + 0.15
    xr = t[1][0][0].get_left()[0] - 0.15
    anchors = VGroup(*[Dot([xr, y, 0], radius=0.001).set_opacity(0) for y in ys])
    right.add(anchors)
    bars = VGroup()
    for y, a in zip(ys, anchors):
        bar = Line([xl, y, 0], a.get_center(), color=GOLD, stroke_width=9)
        bar.add_updater(lambda m, y=y, a=a: m.put_start_and_end_on(np.array([xl, y, 0]), a.get_center()))
        bars.add(bar)
    lab = VGroup(T("salt", 28, GOLD), T("bridges", 28, GOLD)).arrange(DOWN, buff=0.05).move_to([0, C4[1] - 1.28, 0])
    return bars, lab


def helix_push(t):
    a = t[0][0]
    hc = RoundedRectangle(corner_radius=0.18, width=1.85, height=0.42, stroke_width=0, fill_color=HELIX,
                          fill_opacity=0.9).move_to(a[0].get_center() + DOWN * 0.62)
    ht = T("F helix", 24, BG, weight=BOLD).move_to(hc)
    arr = Arrow(hc.get_right() + LEFT * 0.05, [t[1][0][0].get_left()[0] + 0.35, hc.get_center()[1], 0], color=HELIX,
                buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.25).set_z_index(3)
    return VGroup(hc, ht), arr


def angle_marks(rc, ang):
    r0, r1, ra = 2.85, 3.85, 3.5
    up = np.array([0, 1, 0])
    rot = np.array([-np.sin(ang), np.cos(ang), 0])
    ref = DashedLine(rc + up * r0, rc + up * r1, color=TEXT, stroke_width=5)
    new = Line(rc + rot * r0, rc + rot * r1, color=GOLD, stroke_width=7)
    arc = Arc(radius=ra, start_angle=PI / 2, angle=ang, arc_center=rc, color=GOLD, stroke_width=7)
    lab = T("about 15°", 36, GOLD).move_to(rc + np.array([1.6, 3.45, 0]))
    return VGroup(ref, new, arc, lab)


class S12Step4(SpokenScene):
    def construct(self):
        t, left, right = big_tet()
        bars, blab = bridge_set(t, right)
        hchip, harr = helix_push(t)
        self.add(left, right, bars, badge(4), tag("T", BLUE))
        self.play(FadeIn(hchip), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(blab), Indicate(bars, color=GOLD, scale_factor=1.0), run_time=0.6)
        self.at("perutz's classic")
        pl = T("Perutz's classic account", 30, GREY).move_to([0, -3.55, 0])
        self.play(FadeIn(pl), run_time=0.5)
        self.at("this is levered")
        self.play(GrowArrow(harr), run_time=0.7)
        self.at("rotation of one dimer")
        rc = right[0].get_center()
        ang = 15 * DEGREES
        self.play(Rotate(right, angle=ang, about_point=rc), FadeOut(harr), run_time=1.4)
        self.at("about 15")
        am = angle_marks(rc, ang)
        self.play(Create(am[0]), Create(am[1]), run_time=0.4)
        self.play(Create(am[2]), FadeIn(am[3]), run_time=0.6)
        self.finish()


class S13Bridges(SpokenScene):
    def construct(self):
        t, left, right = big_tet()
        bars, blab = bridge_set(t, right)
        rc = right[0].get_center()
        right.rotate(15 * DEGREES, about_point=rc)
        for b in bars:
            b.update()
        tg = tag("T", BLUE)
        hchip, _ = helix_push(t)
        self.add(left, right, bars, blab, hchip, tg)
        self.wait(0.1)
        self.at("salt bridges")
        self.play(Indicate(bars, color=YELLOW, scale_factor=1.0), Indicate(blab, color=GOLD), run_time=0.7)
        self.at("brake")
        pieces = VGroup()
        for b in bars:
            b.clear_updaters()
            s, e = b.get_start(), b.get_end()
            m = (s + e) / 2
            pieces.add(Line(s, m - (m - s) * 0.12, color=GOLD, stroke_width=9),
                       Line(m + (e - m) * 0.12, e, color=GOLD, stroke_width=9))
        self.remove(bars)
        self.add(pieces)
        self.play(*[p.animate.shift((LEFT if i % 2 == 0 else RIGHT) * 0.25 + DOWN * 0.1).set_opacity(0)
                    for i, p in enumerate(pieces)], FadeOut(blab), run_time=0.7)
        self.remove(pieces)
        self.at("moves toward")
        tr = tag("R", GREEN)
        self.play(*recolor(blocks_of(t), GREEN), FadeOut(tg, scale=0.6), run_time=0.6)
        self.play(FadeIn(tr, scale=1.3), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------ s14: why T binds weakly
CHAIN = ["iron shifts", "F helix shifts", "dimer rotates"]
CHAIN_COL = [IRON, HELIX, BLUE]


class S14WhyT(SpokenScene):
    def construct(self):
        c = np.array([-2.9, 0.35, 0])
        t = tet((c[0], c[1]), 2.2, 1.65, 0.3, fill=BLUE, lsize=56)
        outs = VGroup(dim_out(t[0]), dim_out(t[1]))
        ys = [c[1] + 0.8, c[1] - 1.6]
        xl, xr = t[0][0][0].get_right()[0] + 0.15, t[1][0][0].get_left()[0] - 0.15
        bars = VGroup(*[Line([xl, y, 0], [xr, y, 0], color=GOLD, stroke_width=9) for y in ys])
        blab = VGroup(T("salt", 26, GOLD), T("bridges", 26, GOLD)).arrange(DOWN, buff=0.04).move_to([c[0], c[1] - 0.4, 0])
        tg = tag("T", BLUE)
        chips = VGroup(*[chip(s, col, 32) for s, col in zip(CHAIN, CHAIN_COL)])
        for ch, y in zip(chips, (2.3, 0.45, -1.4)):
            ch.move_to([4.5, y, 0])
        arrs = VGroup(*[Arrow(chips[i].get_bottom(), chips[i + 1].get_top(), color=GREY, buff=0.1, stroke_width=5)
                        for i in (0, 1)])
        self.add(t, outs, bars, blab, tg)
        self.play(FadeIn(chips), FadeIn(arrs), run_time=0.7)
        self.at("those salt bridges")
        self.play(Indicate(bars, color=YELLOW, scale_factor=1.0), Indicate(blab, color=GOLD), run_time=0.7)
        self.at("resist")
        src = np.array([outs[1].get_right()[0] + 0.15, c[1], 0])
        brakes, rl = VGroup(), VGroup()
        for ch in chips:
            end = ch.get_left() + LEFT * 0.12
            ln = Line(src, end, color=GOLD, stroke_width=5)
            d = (end - src) / np.linalg.norm(end - src)
            nrm = np.array([-d[1], d[0], 0])
            cap = Line(end + nrm * 0.3, end - nrm * 0.3, color=GOLD, stroke_width=8)
            brakes.add(VGroup(ln, cap))
            rl.add(T("resist", 26, GOLD).move_to(src + (end - src) * 0.62 + nrm * 0.36))
        self.play(LaggedStart(*[Create(b) for b in brakes], lag_ratio=0.15), run_time=0.6)
        self.play(FadeIn(rl), run_time=0.3)
        self.at("chain of movements")
        self.play(Wiggle(chips[0], scale_value=1.05, rotation_angle=0.03 * TAU), run_time=0.8)
        self.play(Wiggle(chips[1], scale_value=1.03), Wiggle(chips[2], scale_value=1.03), run_time=0.6)
        self.at("that is why")
        res = T("T resists, so a heme in T binds O₂ weakly", 36, WHITE).move_to([0, -3.3, 0])
        self.play(FadeIn(res), run_time=0.3)
        self.finish()


# ------------------------------------------------------------------ s15: gear train out, odds dial in
def gear(R, n, phase=0.0, tooth=0.17, color="#B7BECB"):
    pts = []
    for k in range(n):
        a0 = phase + 2 * PI * k / n
        w = PI / n
        for a, r in ((a0 - w * 0.5, R + tooth), (a0 + w * 0.5, R + tooth), (a0 + w * 0.62, R - tooth),
                     (a0 + w * 1.38, R - tooth)):
            pts.append([r * np.cos(a), r * np.sin(a), 0])
    g = Polygon(*pts, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    hub = Circle(radius=0.12, color=color, fill_opacity=1, stroke_width=0)
    return VGroup(g, hub)


LO, HI = -8.0, 3.0


def dial_angle(x):
    return PI * (1 - (x - LO) / (HI - LO))


class S15Odds(SpokenScene):
    def construct(self):
        R1, R2 = 1.4, 1.0
        xs = [-2.4, 0.0, 2.4]
        gy = 0.35
        g1 = gear(R1, 14, 0.0).move_to([xs[0], gy, 0])
        g2 = gear(R2, 10, PI - PI / 10).move_to([xs[1], gy, 0])
        g3 = gear(R1, 14, PI).move_to([xs[2], gy, 0])
        glabs = VGroup(*[T(s, 28, col).move_to([x, gy - R - 0.65, 0]) for s, col, x, R in
                         zip(["iron", "F helix", "dimer"], CHAIN_COL, xs, (R1, R2, R1))])
        gt = T("a gear train: every move forced", 32, GREY).move_to([0, 2.75, 0])
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3), FadeIn(glabs), FadeIn(gt), run_time=0.35)
        a = PI / 3
        self.play(Rotate(g1, a, about_point=g1.get_center()), Rotate(g2, -a * R1 / R2, about_point=g2.get_center()),
                  Rotate(g3, a, about_point=g3.get_center()), run_time=1.2, rate_func=linear)
        self.at("gear train")
        cross = VGroup(Line([-4.2, -1.6, 0], [4.2, 2.3, 0]), Line([-4.2, 2.3, 0], [4.2, -1.6, 0])).set_stroke(RED, 6)
        nl = T("looser than a gear train", 32, RED).move_to([0, 2.75, 0])
        self.play(Create(cross), ReplacementTransform(gt, nl), run_time=0.4)
        gone = VGroup(g1, g2, g3, glabs, cross, nl)
        # odds dial, log scale, positions from the two-state fit
        ctr, rad = np.array([0.0, -1.85, 0]), 3.3
        n = 44
        segs = VGroup(*[Arc(radius=rad, start_angle=PI - i * PI / n, angle=-PI / n, arc_center=ctr, stroke_width=14,
                            color=interpolate_color(ManimColor(BLUE), ManimColor(GREEN), i / (n - 1))) for i in range(n)])
        ticks = VGroup()
        for x in range(int(LO), int(HI) + 1):
            th = dial_angle(x)
            d = np.array([np.cos(th), np.sin(th), 0])
            ticks.add(Line(ctr + d * (rad + 0.12), ctr + d * (rad + (0.45 if x == 0 else 0.3)), color=TEXT,
                           stroke_width=4 if x == 0 else 2.5))
        th0 = dial_angle(0)
        even = T("even odds", 26, TEXT).move_to(ctr + np.array([np.cos(th0), np.sin(th0), 0]) * (rad + 0.85))
        tl = T("T favored", 28, BLUE).move_to(ctr + LEFT * rad + DOWN * 0.45)
        rl = T("R favored", 28, GREEN).move_to(ctr + RIGHT * rad + DOWN * 0.45)
        ttl = T("odds of R", 30, GOLD).move_to(ctr + DOWN * 0.55)
        note = T("log scale, one illustrative fit", 24, GREY).move_to([4.3, -3.3, 0])
        xs_i = [np.log10(r_odds(i)) for i in range(5)]
        nv = ValueTracker(xs_i[0])

        def needle():
            th = dial_angle(nv.get_value())
            return Line(ctr, ctr + 2.75 * np.array([np.cos(th), np.sin(th), 0]), color=TEXT, stroke_width=8)

        nd = always_redraw(needle)
        hub = Dot(ctr, radius=0.15, color=TEXT)
        fes = VGroup(*[fe_static([0, 0], 0.3) for _ in range(4)]).arrange(RIGHT, buff=0.45)
        fel = T("iron shifts:", 28, TEXT)
        frow = VGroup(fel, fes).arrange(RIGHT, buff=0.4).move_to([0, 3.2, 0])
        for f in fes:
            f[0].set_fill(GREY, 0.45)
        self.play(LaggedStart(FadeOut(gone, run_time=0.3),
                              AnimationGroup(FadeIn(segs), FadeIn(ticks), FadeIn(even), FadeIn(tl), FadeIn(rl),
                                             FadeIn(ttl), FadeIn(hub), FadeIn(nd), FadeIn(frow), FadeIn(note)),
                              lag_ratio=0.75), run_time=0.75)
        for i, cue in enumerate(["iron shift", "raises the odds", "the switch", "rather than"]):
            self.at(cue)
            self.play(fes[i][0].animate.set_fill(GOLD, 1), nv.animate.set_value(xs_i[i + 1]), run_time=0.4)
        self.at("forcing it")
        ft = T("raised, not forced", 34, TEXT).move_to([-1.6, -3.3, 0])
        self.play(FadeIn(ft, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ s16: population bar nudges toward R
def fmt_odds(i):
    r = r_odds(i)

    def sig(v):
        v = float(f"{v:.2g}")
        return f"{v:,.0f}" if v >= 10 else f"{v:g}"

    return f"R : T  ≈  1 : {sig(1 / r)}" if r < 1 else f"R : T  ≈  {sig(r)} : 1"


class S16Fits(SpokenScene):
    def construct(self):
        W, H, Y = 11.0, 1.6, 1.35
        fr = ValueTracker(r_odds(0) / (1 + r_odds(0)))

        def bar():
            f = fr.get_value()
            tw, rw = W * (1 - f), W * f
            tr = Rectangle(width=max(tw, 0.001), height=H, stroke_width=0, fill_color=BLUE, fill_opacity=0.75)
            rr = Rectangle(width=max(rw, 0.001), height=H, stroke_width=0, fill_color=GREEN, fill_opacity=0.85)
            tr.move_to([-W / 2 + tw / 2, Y, 0])
            rr.move_to([W / 2 - rw / 2, Y, 0])
            fr_ = Rectangle(width=W, height=H, stroke_color=GREY, stroke_width=2).move_to([0, Y, 0])
            return VGroup(tr, rr, fr_)

        b = always_redraw(bar)
        tl = T("T", 40, BLUE).move_to([-W / 2 + 0.25, Y + 1.15, 0])
        rl = T("R", 40, GREEN).move_to([W / 2 - 0.25, Y + 1.15, 0])
        ttl = T("share of molecules in each shape", 30, TEXT).move_to([0, Y + 1.15, 0])
        mt = T("mostly T", 32, BG, weight=BOLD).move_to([-W / 2 + 1.4, Y, 0])
        slots = VGroup(*[DashedVMobject(Circle(radius=0.34, color=YELLOW, stroke_width=4), num_dashes=14)
                         for _ in range(4)]).arrange(RIGHT, buff=0.55).move_to([1.4, -0.65, 0])
        sc = T("O₂ bound:", 30, TEXT).next_to(slots, LEFT, buff=0.45)
        od = M(fmt_odds(0), 32, TEXT).move_to([0, -1.75, 0])
        note = T("one illustrative two-state fit", 24, GREY).move_to([0, -2.45, 0])
        self.add(b, tl, rl, ttl, mt, slots, sc, od, note)
        self.wait(0.1)
        self.at("fits")
        self.play(Indicate(VGroup(tl, rl), color=GOLD, scale_factor=1.1), run_time=0.7)
        for i, (cue, rt) in enumerate([("each oxygen", 0.5), ("bound", 0.3), ("makes r", 0.3), ("more likely", 0.4)]):
            self.at(cue)
            k = i + 1
            f = r_odds(k) / (1 + r_odds(k))
            anims = [FadeIn(o2(0.34).move_to(slots[i]), scale=0.5), fr.animate.set_value(f),
                     Transform(od, M(fmt_odds(k), 32, TEXT).move_to([0, -1.75, 0]))]
            if k == 3:
                anims.append(FadeOut(mt))
            self.play(*anims, run_time=rt)
        self.at("not")
        nc = T("more likely, not certain", 36, GOLD).move_to([0, -3.2, 0])
        self.play(FadeIn(nc, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ s17: the two end points
class S17Perutz(SpokenScene):
    def construct(self):
        bl = RoundedRectangle(corner_radius=0.3, width=5.7, height=6.6, stroke_color=BLUE, stroke_width=3,
                              fill_color=BLUE, fill_opacity=0.05).move_to([-3.45, -0.15, 0])
        br = RoundedRectangle(corner_radius=0.3, width=5.7, height=6.6, stroke_color=GREEN, stroke_width=3,
                              fill_color=GREEN, fill_opacity=0.05).move_to([3.45, -0.15, 0])
        hT = T("deoxy · T", 36, BLUE).move_to([-3.45, 2.65, 0])
        hR = T("oxy · R", 36, GREEN).move_to([3.45, 2.65, 0])
        tT = tet((-3.45, 0.1), 2.0, 0.6, 0.22, fill=BLUE, lsize=56)
        tR = tet((3.45, 0.1), 2.0, 0.6, 0.22, fill=GREEN, lsize=56)
        pT = T("PDB 2HHB", 34, WHITE, weight=BOLD).move_to([-3.45, -2.6, 0])
        pR = T("PDB 1HHO", 34, WHITE, weight=BOLD).move_to([3.45, -2.6, 0])
        self.add(bl, br, hT, hR, tT, tR, pT, pR)
        self.wait(0.1)
        self.at("two endpoints")
        self.play(Indicate(bl, color=BLUE, scale_factor=1.02), Indicate(br, color=GREEN, scale_factor=1.02), run_time=0.8)
        self.at("deoxy")
        self.play(Indicate(tT, color=BLUE, scale_factor=1.04), run_time=0.6)
        self.at("oxyhemoglobin")
        rc = tR[1].get_center()
        self.play(Rotate(tR[1], angle=15 * DEGREES, about_point=rc), run_time=0.9)
        self.at("side by side")
        ar = DoubleArrow([-0.55, 0.1, 0], [0.55, 0.1, 0], color=GOLD, buff=0, stroke_width=8, tip_length=0.25)
        self.play(GrowFromCenter(ar), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ s18: two textbook models
def mini(states, c, tile=0.3, gap=0.05):
    g = VGroup(*[Square(side_length=tile, stroke_width=1.5, stroke_color=GREEN if s else BLUE,
                        fill_color=GREEN if s else BLUE, fill_opacity=0.7) for s in states])
    g.arrange_in_grid(2, 2, buff=gap).move_to([c[0], c[1], 0])
    return g


def quad(c, tile=1.45, gap=0.2):
    g = VGroup(*[RoundedRectangle(corner_radius=0.14, width=tile, height=tile, stroke_color=BLUE, stroke_width=3,
                                  fill_color=BLUE, fill_opacity=0.22) for _ in range(4)])
    g.arrange_in_grid(2, 2, buff=gap).move_to([c[0], c[1], 0])
    return g


class S18Models(SpokenScene):
    def construct(self):
        lx, rx, qy, sy = -3.6, 3.4, 0.6, -1.85
        a, b = quad((lx, qy)), quad((rx, qy))
        histA = [mini([0, 0, 0, 0], (lx - 0.7, sy))]
        histB = [mini([0, 0, 0, 0], (rx - 2.4, sy))]
        self.add(a, b, histA[0], histB[0])
        self.wait(0.2)
        self.at("switch together")
        ha = VGroup(T("all together", 36, TEXT), T("concerted", 30, TEXT)).arrange(DOWN, buff=0.12).move_to([lx, 2.9, 0])
        aa = Arrow([lx - 0.3, sy, 0], [lx + 0.3, sy, 0], color=GREY, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        mA = mini([1, 1, 1, 1], (lx + 0.7, sy))
        self.play(FadeIn(ha), *[x.animate.set_stroke(GREEN).set_fill(GREEN, 0.22) for x in a], run_time=0.6)
        self.play(GrowArrow(aa), FadeIn(mA), run_time=0.35)
        self.at("one at a time")
        hb = VGroup(T("one at a time", 36, TEXT), T("sequential", 30, TEXT)).arrange(DOWN, buff=0.12).move_to([rx, 2.9, 0])
        self.play(FadeIn(hb), run_time=0.35)
        for k in range(4):
            st = [1 if j <= k else 0 for j in range(4)]
            x = rx - 2.4 + 1.2 * (k + 1)
            ar = Arrow([x - 0.82, sy, 0], [x - 0.38, sy, 0], color=GREY, buff=0, stroke_width=4,
                       max_tip_length_to_length_ratio=0.35)
            self.play(b[k].animate.set_stroke(GREEN).set_fill(GREEN, 0.22), GrowArrow(ar),
                      FadeIn(mini(st, (x, sy))), run_time=0.28)
            self.wait(0.12)
        self.at("real hemoglobin")
        q = T("?", 120, GOLD, weight=BOLD).move_to([-0.05, 0.55, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.at("textbook model")
        line = T("real hemoglobin fits neither one perfectly", 34, TEXT).move_to([0, -3.0, 0])
        self.play(FadeIn(line, shift=UP * 0.1), run_time=0.6)
        self.at("perfectly")
        bt = T("real hemoglobin sits between the two", 28, GREY).move_to([0, -3.5, 0])
        self.play(Indicate(q, color=GOLD, scale_factor=1.2), FadeIn(bt), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ s19: concerted overall, each subunit flexes
class S19Tertiary(SpokenScene):
    def construct(self):
        c = np.array([0.0, 0.1, 0])
        bs = 2.45
        t = tet((c[0], c[1]), bs, 0.9, 0.3, fill=BLUE, lsize=60)
        left, right = VGroup(t[0], dim_out(t[0])), VGroup(t[1], dim_out(t[1]))
        tg = tag("T", BLUE)
        self.add(left, right, tg)
        self.wait(0.2)
        self.at("concerted")
        lab = T("overall switch: all at once", 32, GOLD).move_to([-1.5, 3.3, 0])
        rc = right[0].get_center()
        self.play(FadeIn(lab), *recolor(blocks_of(t), GREEN), FadeOut(tg), run_time=0.6)
        self.play(Rotate(right, angle=15 * DEGREES, about_point=rc), FadeIn(tag("R", GREEN), scale=1.3), run_time=0.7)
        self.at("own shape")
        lab2 = T("each subunit's own shape shifts too", 34, TEXT).move_to([0, -3.5, 0])
        self.play(FadeIn(lab2), run_time=0.5)
        self.at("as it binds")
        # each subunit tilts and squashes by its own amount, with its own O2 chip
        specs = [(6, [[1.08, 0.12], [0, 0.9]]), (-6, [[0.92, -0.12], [0, 1.08]]),
                 (-6, [[1.08, -0.12], [0, 0.9]]), (6, [[0.92, 0.12], [0, 1.08]])]
        anims = []
        for blk, (deg, m) in zip(blocks_of(t), specs):
            ctr = blk[0].get_center()
            ox = o2(0.3).move_to(ctr + np.array([0.78 * bs / 2, 0.78 * bs / 2, 0]))
            anims.append(AnimationGroup(FadeIn(ox, scale=0.5),
                                        blk[0].animate.rotate(deg * DEGREES, about_point=ctr)
                                        .apply_matrix(m, about_point=ctr)))
        self.play(LaggedStart(*anims, lag_ratio=0.3), run_time=1.4)
        self.finish()


# ------------------------------------------------------------------ s20: the take-home
class S20Take(SpokenScene):
    def construct(self):
        words = ["iron shifts", "F helix shifts", "odds of R rise"]
        cols = [IRON, HELIX, GOLD]
        ch = VGroup(*[chip(w, c, 36) for w, c in zip(words, cols)]).arrange(RIGHT, buff=0.9).move_to([0, 2.8, 0])
        ar = VGroup(*[Arrow(ch[i].get_right(), ch[i + 1].get_left(), color=GREY, buff=0.1, stroke_width=6) for i in (0, 1)])
        c = np.array([0.0, -1.05, 0])
        bs = 1.9
        t = tet((c[0], c[1]), bs, 0.8, 0.25, fill=BLUE, lsize=52)
        left, right = VGroup(t[0], dim_out(t[0], 0.1)), VGroup(t[1], dim_out(t[1], 0.1))
        outline = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=t.width + 1.7, height=t.height + 0.7,
                                                  stroke_color=GOLD, stroke_width=4), num_dashes=60).move_to(c + UP * 0.05)
        wl = T("whole molecule", 30, GOLD).move_to([-5.3, -1.05, 0])
        wld = leader(wl, [c[0] - (t.width + 1.7) / 2, c[1], 0])
        tg = chip("T", BLUE, 34).move_to([5.3, -1.05, 0])
        self.add(left, right, tg)
        self.wait(0.1)
        self.at("tiny shift")
        self.play(FadeIn(ch[0], shift=DOWN * 0.1), run_time=0.6)
        self.at("levered through")
        self.play(GrowArrow(ar[0]), FadeIn(ch[1]), run_time=0.7)
        self.at("raises the odds")
        self.play(GrowArrow(ar[1]), FadeIn(ch[2]), run_time=0.7)
        self.at("whole molecule")
        rc = right[0].get_center()
        tr = chip("R", GREEN, 34).move_to(tg)
        self.play(Rotate(right, angle=15 * DEGREES, about_point=rc), *recolor(blocks_of(t), GREEN),
                  ReplacementTransform(tg, tr), FadeIn(outline), FadeIn(wl), Create(wld), run_time=0.8)
        self.finish()
