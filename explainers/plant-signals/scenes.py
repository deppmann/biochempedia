"""Auxin moves sideways, and the shoot bends  (Biochemistrypedia explainer, Organismal Biology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = light (lamp rays, the lit side)
  ORANGE = the signal that moves: auxin, or "something passes down"
  GREEN  = living plant tissue (seedlings, coleoptiles, flanks)
  BLUE   = mica and glass (things placed in the way or over the tip)
  GREY   = ground, the opaque cap, outlines, notes
  TEAL   = agar blocks
  PURPLE = the PIN carrier in the cell membrane
  RED    = the question, and a blocked signal
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
Z0, Z1 = 0.12, 0.62          # the zone below the tip where the bend forms


# ---------------------------------------------------------------------------------------------
# helpers: a stem is a band along a centre line whose heading turns inside the bend zone
# ---------------------------------------------------------------------------------------------
def _heading(s, bend, z0=Z0, z1=Z1):
    u = np.clip((s - z0) / (z1 - z0), 0, 1)
    return bend * (u * u * (3 - 2 * u))


def centre(base, h, bend, n=40, z0=Z0, z1=Z1):
    """centre line points, headings, from base up to the tip. bend > 0 leans LEFT (toward a lamp at left)."""
    pts, ths = [np.array(base, float)], [0.0]
    ds = h / n
    for i in range(1, n + 1):
        s = (i - 0.5) / n
        th = _heading(s, bend, z0, z1)
        d = np.array([-np.sin(th), np.cos(th), 0])
        pts.append(pts[-1] + d * ds)
        ths.append(_heading(i / n, bend, z0, z1))
    return pts, ths


def pose(base, h, bend, s, n=40, z0=Z0, z1=Z1):
    pts, ths = centre(base, h, bend, n, z0, z1)
    i = int(round(s * n))
    return pts[i], ths[i]


def band(base, h, bend, a, b, s0=0.0, s1=1.0, n=40, color=GREEN, op=0.28, sw=3, z0=Z0, z1=Z1):
    """polygon of the stem between lateral offsets a..b (left negative) and arc fractions s0..s1."""
    pts, ths = centre(base, h, bend, n, z0, z1)
    i0, i1 = int(round(s0 * n)), int(round(s1 * n))
    L, R = [], []
    for i in range(i0, i1 + 1):
        nx = np.array([np.cos(ths[i]), np.sin(ths[i]), 0])      # points to the right of the heading
        L.append(pts[i] + nx * a)
        R.append(pts[i] + nx * b)
    poly = Polygon(*(L + R[::-1]), stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)
    return poly


def stem(base, h, bend, w=0.56, **kw):
    return band(base, h, bend, -w / 2, w / 2, **kw)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rays(x, y, n=3, gap=0.62, length=0.8):
    return VGroup(*[arr([x, y + (i - (n - 1) / 2) * gap, 0], [x + length, y + (i - (n - 1) / 2) * gap, 0], YELLOW, w=5, tip=0.2)
                    for i in range(n)])


def ground(x, y, w=2.2):
    return Rectangle(width=w, height=0.18, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.4).move_to([x, y - 0.09, 0])


def label(txt, x, y, size=24, color=GREY, **kw):
    return T(txt, size, color, **kw).move_to([x, y, 0])


def rot_to(mob, th):
    return mob.rotate(th, about_point=mob.get_center())


def at_pose(mob, p, th):
    mob.move_to(p)
    mob.rotate(th, about_point=p)
    return mob


class S00Title(TitleCard):
    LESSON = "Plant hormones and responses"
    TITLE = "Auxin Moves Sideways, and the Shoot Bends"


# ---------------------------------------------------------------------------------------------
class S01Bend(SpokenScene):
    def construct(self):
        bx, by, h = 0.2, -2.3, 4.3
        gr = ground(bx, by, 2.6)
        s0 = stem([bx, by, 0], h, 0.0, w=0.6)
        name = label("oat seedling", bx, by - 0.55, 26)
        lamp_c = Circle(radius=0.38, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.85).move_to([-5.7, 0.7, 0])
        rs = rays(-5.1, 0.7, n=3, gap=0.7, length=1.5)
        lamp_l = label("lamp", -5.7, 1.4, 26, YELLOW)
        self.at("oat seedling")
        self.play(FadeIn(gr), FadeIn(s0), FadeIn(name), run_time=0.8)
        self.at("from one side")
        self.play(FadeIn(lamp_c), FadeIn(lamp_l), LaggedStart(*[GrowArrow(r) for r in rs], lag_ratio=0.25), run_time=1.0)
        self.at("bends toward")
        s1 = stem([bx, by, 0], h, 0.55, w=0.6)
        self.play(Transform(s0, s1), run_time=1.6)
        self.at("the tip")
        tp, _ = pose([bx, by, 0], h, 0.55, 1.0)
        tip_l = T("tip: light sensed", 26, YELLOW).move_to([tp[0] + 2.6, tp[1] + 0.25, 0])
        tip_a = arr([tip_l.get_left()[0] - 0.05, tip_l.get_left()[1], 0], [tp[0] + 0.5, tp[1] + 0.05, 0], YELLOW)
        self.play(FadeIn(tip_l), GrowArrow(tip_a), run_time=0.7)
        self.at("lower down")
        zp0, _ = pose([bx, by, 0], h, 0.55, Z0)
        zp1, _ = pose([bx, by, 0], h, 0.55, Z1)
        bxr = max(zp0[0], zp1[0]) + 0.75
        brace = Line([bxr, zp0[1], 0], [bxr, zp1[1], 0], color=GREEN, stroke_width=7)
        bl = T("the bend forms here", 26, GREEN).move_to([bxr + 0.35 + 1.45, (zp0[1] + zp1[1]) / 2, 0])
        self.play(Create(brace), FadeIn(bl), run_time=0.8)
        self.at("what carries")
        qx = bl.get_center()[0]
        q = arr([qx, tip_l.get_bottom()[1] - 0.15, 0], [qx, bl.get_top()[1] + 0.15, 0], RED)
        qm = T("?", 60, RED, weight=BOLD).next_to(q, RIGHT, buff=0.25)
        self.play(GrowArrow(q), FadeIn(qm, scale=0.7), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Darwin(SpokenScene):
    def construct(self):
        cs = [-4.2, 0.3, 4.8]
        base_y, h = -1.5, 3.0
        note = label("canary grass seedlings (Phalaris canariensis), lit from the left", 0, 3.2, 26)
        stems, grs, rs = [], [], []
        for c in cs:
            grs.append(ground(c, base_y, 1.8))
            stems.append(stem([c, base_y, 0], h, 0.0, w=0.5))
            rs.append(rays(c - 2.0, base_y + 1.9, n=3, gap=0.6, length=0.7))
        names = [label(t, c, base_y - 0.65, 26) for c, t in zip(cs, ["bare tip", "opaque cap", "glass tube"])]
        self.at("charles darwin")
        self.play(FadeIn(note), *[FadeIn(g) for g in grs], *[FadeIn(s) for s in stems], run_time=0.8)
        self.play(*[FadeIn(r) for r in rs], run_time=0.5)
        # bare: bends
        self.at("one side")
        self.play(FadeIn(names[0]), Transform(stems[0], stem([cs[0], base_y, 0], h, 0.5, w=0.5)), run_time=0.9)
        # opaque cap
        self.at("opaque cap")
        capp, capth = pose([cs[1], base_y, 0], h, 0.0, 1.0)
        cap = Rectangle(width=0.8, height=0.75, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.85)
        cap.move_to([capp[0], capp[1] - 0.1, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.3), FadeIn(names[1]), run_time=0.7)
        self.at("greatly reduced bending")
        b2 = 0.1
        p2, th2 = pose([cs[1], base_y, 0], h, b2, 1.0)
        self.play(Transform(stems[1], stem([cs[1], base_y, 0], h, b2, w=0.5)),
                  cap.animate.move_to([p2[0], p2[1] - 0.1, 0]).rotate(th2, about_point=[p2[0], p2[1] - 0.1, 0]), run_time=1.0)
        red_t = label("bending greatly reduced", cs[1], base_y + 3.4, 24, RED)
        # glass tube
        self.at("transparent glass")
        p3, _ = pose([cs[2], base_y, 0], h, 0.0, 0.88)
        tube = RoundedRectangle(corner_radius=0.18, width=0.85, height=1.1, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.18).move_to([cs[2], base_y + h - 0.35, 0])
        self.play(FadeIn(tube, shift=DOWN * 0.3), FadeIn(names[2]), run_time=0.7)
        self.at("did not stop")
        b3 = 0.5
        tp3, tth3 = pose([cs[2], base_y, 0], h, b3, 0.84)
        self.play(Transform(stems[2], stem([cs[2], base_y, 0], h, b3, w=0.5)),
                  tube.animate.move_to([tp3[0] - 0.1, tp3[1] + 0.2, 0]).rotate(tth3, about_point=[tp3[0] - 0.1, tp3[1] + 0.2, 0]),
                  run_time=1.2)
        self.at("light is sensed")
        c1 = T("light is sensed mainly near the tip", 28, YELLOW).move_to([0, -3.2, 0])
        self.play(FadeIn(c1), run_time=0.6)
        self.at("something passes down")
        sp, _ = pose([cs[0], base_y, 0], h, 0.5, 0.9)
        sp2, _ = pose([cs[0], base_y, 0], h, 0.5, 0.25)
        sa = arr([sp[0] + 0.75, sp[1], 0], [sp2[0] + 0.75, sp2[1], 0], ORANGE, w=6)
        sl = VGroup(T("something", 24, ORANGE), T("passes down", 24, ORANGE)).arrange(DOWN, buff=0.06).move_to([cs[0] + 1.75, base_y + 0.55, 0])
        self.play(GrowArrow(sa), FadeIn(sl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Mica(SpokenScene):
    def construct(self):
        cs = [-4.2, 0.3, 4.8]
        base_y, h = -1.5, 3.0
        note = label("oat (Avena sativa) coleoptiles, lit from the left", 0, 3.3, 26)
        defn = label("coleoptile: the sheath over a grass seedling's first leaf", 0, 2.7, 24)
        stems, grs, rs = [], [], []
        for c in cs:
            grs.append(ground(c, base_y, 1.8))
            stems.append(stem([c, base_y, 0], h, 0.0, w=0.5))
            rs.append(rays(c - 2.0, base_y + 0.6, n=3, gap=0.6, length=0.7))
        names = [label(t, c, base_y - 0.65, 24) for c, t in zip(cs, ["tip cut, set back", "mica, lit side", "mica, shaded side"])]
        self.at("worked with")
        self.play(FadeIn(note), run_time=0.5)
        self.at("coleoptoils")
        self.play(FadeIn(stems[0]), FadeIn(grs[0]), FadeIn(rs[0]), FadeIn(defn), run_time=0.7)
        # cut and set back
        self.at("cut off tips")
        cp, cth = pose([cs[0], base_y, 0], h, 0.0, 0.8)
        cut = Line([cp[0] - 0.4, cp[1], 0], [cp[0] + 0.4, cp[1], 0], color=RED, stroke_width=5)
        cut_l = label("cut", cs[0] - 0.75, cp[1], 24, RED)
        self.play(Create(cut), FadeIn(cut_l), FadeIn(names[0]), run_time=0.7)
        self.at("bent below the cut")
        b = 0.5
        self.play(Transform(stems[0], stem([cs[0], base_y, 0], h, b, w=0.5)), run_time=1.3)
        cp2, cth2 = pose([cs[0], base_y, 0], h, b, 0.8)
        self.play(cut.animate.move_to(cp2).rotate(cth2), cut_l.animate.move_to([cp2[0] - 0.75, cp2[1], 0]), run_time=0.01)
        self.at("crossed a wound")
        self.wait(0.3)
        # mica panels
        self.at("slid mica")
        self.play(*[FadeIn(g) for g in grs[1:]], *[FadeIn(s) for s in stems[1:]], *[FadeIn(r) for r in rs[1:]], run_time=0.6)
        mpos = 0.72

        def mica(c, side, bend):
            p, th = pose([c, base_y, 0], h, bend, mpos)
            m = Rectangle(width=0.55, height=0.1, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.9)
            off = side * 0.18
            m.move_to([p[0] + off, p[1], 0])
            m.rotate(th, about_point=p)
            return m
        m2 = mica(cs[1], -1, 0.0)
        m3 = mica(cs[2], +1, 0.0)
        ml2 = label("mica", cs[1] - 1.25, base_y + 0.72 * h + 0.35, 24, BLUE)
        ml3 = label("mica", cs[2] + 1.0, base_y + 0.72 * h, 24, BLUE)
        self.play(FadeIn(m2, shift=RIGHT * 0.3), FadeIn(ml2), FadeIn(m3, shift=LEFT * 0.3), FadeIn(ml3), run_time=0.8)
        self.at("dissolved chemicals")
        note2 = label("dissolved chemicals cannot cross mica", 0, -3.2, 26, BLUE)
        self.play(FadeIn(note2), FadeIn(names[1]), FadeIn(names[2]), run_time=0.6)
        self.at("lit side left bending intact")
        b2 = 0.5
        p2, th2 = pose([cs[1], base_y, 0], h, b2, mpos)
        self.play(Transform(stems[1], stem([cs[1], base_y, 0], h, b2, w=0.5)),
                  m2.animate.move_to([p2[0] - 0.18 * np.cos(th2), p2[1] - 0.18 * np.sin(th2), 0]).rotate(th2, about_point=p2),
                  ml2.animate.move_to([p2[0] - 1.25, p2[1] + 0.4, 0]), run_time=1.3)
        self.at("shaded side blocked")
        blk = T("no bending", 24, RED).move_to([cs[2], base_y + h + 0.55, 0])
        self.play(FadeIn(blk), run_time=0.5)
        self.at("runs down")
        def inside(c, bend, sf):
            p, th = pose([c, base_y, 0], h, bend, sf)
            return np.array([p[0] + 0.13 * np.cos(th), p[1] + 0.13 * np.sin(th), 0])
        my = base_y + mpos * h
        arr3 = arr([cs[2] + 0.13, base_y + 0.97 * h, 0], [cs[2] + 0.13, my + 0.1, 0], ORANGE, w=5, tip=0.16)
        x3 = VGroup(Line([cs[2] + 0.03, my + 0.25, 0], [cs[2] + 0.23, my + 0.05, 0], color=RED, stroke_width=5),
                    Line([cs[2] + 0.03, my + 0.05, 0], [cs[2] + 0.23, my + 0.25, 0], color=RED, stroke_width=5))
        arr2 = arr(inside(cs[1], b2, 0.97), inside(cs[1], b2, 0.3), ORANGE, w=5, tip=0.16)
        self.play(GrowArrow(arr2), GrowArrow(arr3), Create(x3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Agar(SpokenScene):
    def construct(self):
        base_y, h = -1.9, 2.6
        cA, cB, cC = -4.6, 0.5, 4.9
        note = label("oat coleoptiles, grown in the dark", 0, 3.3, 26)
        # --- A: tips on agar
        blockA = RoundedRectangle(corner_radius=0.08, width=2.0, height=0.45, stroke_color=TEAL, stroke_width=3,
                                  fill_color=TEAL, fill_opacity=0.3).move_to([cA, -0.6, 0])
        tips = VGroup(*[RoundedRectangle(corner_radius=0.15, width=0.4, height=0.9, stroke_color=GREEN, stroke_width=3,
                                         fill_color=GREEN, fill_opacity=0.3).move_to([cA + dx, -0.6 + 0.225 + 0.45, 0])
                        for dx in (-0.55, 0.0, 0.55)])
        lblA = label("cut tips on agar", cA, 1.2, 26)
        lblAg = label("agar", cA, -1.35, 24, TEAL)
        self.at("took the signal")
        self.play(FadeIn(note), run_time=0.5)
        dots = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([cA + dx, -0.6 + 0.2, 0])
                        for dx in (-0.55, 0.0, 0.55)])
        big = VGroup(blockA, tips, dots, lblA, lblAg)
        big.scale(1.6, about_point=[cA, -0.2, 0]).shift([-cA, 0.3, 0])
        self.at("cut tips")
        self.play(FadeIn(blockA), FadeIn(tips), FadeIn(lblA), FadeIn(lblAg), run_time=0.8)
        self.play(FadeIn(dots, shift=DOWN * 0.2), run_time=0.5)
        dots2 = VGroup(*[Circle(radius=0.09 * 1.6, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([0 + dx * 1.6, blockA.get_center()[1], 0])
                         for dx in (-0.7, -0.35, 0.0, 0.35, 0.7)])
        self.play(Transform(dots, dots2), run_time=0.7)
        self.at("then removed")
        self.play(FadeOut(tips), FadeOut(lblA), run_time=0.7)
        # --- B: decapitated coleoptile in the dark
        grB, grC = ground(cB, base_y, 1.8), ground(cC, base_y, 1.8)
        sB = stem([cB, base_y, 0], h, 0.0, w=0.5)
        sC = stem([cC, base_y, 0], h, 0.0, w=0.5)
        dark = label("in the dark", 0, -3.35, 26)
        self.at("in the dark")
        A = VGroup(blockA, dots, lblAg)
        self.play(A.animate.scale(1 / 1.6, about_point=blockA.get_center()).move_to([cA, -0.6, 0]).shift(DOWN * 0.0),
                  FadeIn(grB), FadeIn(sB), FadeIn(dark), run_time=1.0)
        self.at("one side")
        topB = base_y + h
        blkB = blockA.copy()
        dotsB = dots.copy()
        grp = VGroup(blkB, dotsB)
        self.play(grp.animate.scale(0.5).move_to([cB + 0.2, topB + 0.12, 0]), run_time=1.1)
        a_in = arr([cB + 0.3, topB - 0.05, 0], [cB + 0.3, topB - 1.0, 0], ORANGE, w=5)
        # curved away from the block (block on the right, bend to the left)
        self.at("curved away")
        bb = 0.5
        tpB, thB = pose([cB, base_y, 0], h, bb, 1.0)
        self.play(Transform(sB, stem([cB, base_y, 0], h, bb, w=0.5)),
                  grp.animate.move_to([tpB[0] + 0.2 * np.cos(thB), tpB[1] + 0.12 * np.cos(thB) + 0.2 * np.sin(thB) * 0 + 0.0, 0]).rotate(thB, about_point=[tpB[0], tpB[1], 0]),
                  run_time=1.4)
        lbB = label("curves away from the block", cB, 2.75, 26, GREEN)
        self.play(FadeIn(lbB), run_time=0.5)
        # --- C: plain agar
        self.at("plain agar")
        grpC = VGroup(RoundedRectangle(corner_radius=0.08, width=1.0, height=0.22, stroke_color=TEAL, stroke_width=3,
                                       fill_color=TEAL, fill_opacity=0.3))
        grpC.move_to([cC + 0.2, topB + 0.12, 0])
        self.play(FadeIn(grC), FadeIn(sC), FadeIn(grpC), run_time=0.7)
        lbC = label("plain agar: no curve", cC, 2.75, 26, GREY)
        self.play(FadeIn(lbC), run_time=0.5)
        self.at("sped elongation")
        sp = T("a substance from the tips entered the agar", 26, ORANGE).move_to([0, -2.75, 0])
        self.play(FadeIn(sp), run_time=0.6)
        self.at("identified later")
        idl = T("auxin was identified later, by others", 26, TEXT).move_to([0, -2.75, 0])
        self.play(FadeOut(sp), run_time=0.3)
        self.play(FadeIn(idl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Sideways(SpokenScene):
    def construct(self):
        bx, by, h = -0.9, -2.3, 3.9
        w = 1.7
        lamp_r = rays(-4.7, 0.0, n=3, gap=0.9, length=1.0)
        lamp_l = label("light", -4.2, 1.5, 26, YELLOW)
        gr = ground(bx, by, 3.0)
        left0 = band([bx, by, 0], h, 0.0, -w / 2, 0.0)
        right0 = band([bx, by, 0], h, 0.0, 0.0, w / 2)
        ll = label("lit flank", bx - 0.85, by - 0.5, 24, YELLOW)
        sl = label("shaded flank", bx + 0.85, by - 0.5, 24, GREY)
        sl.shift(RIGHT * 0.4)
        self.at("why does")
        self.play(FadeIn(gr), FadeIn(left0), FadeIn(right0), FadeIn(lamp_r), FadeIn(lamp_l), FadeIn(ll), FadeIn(sl), run_time=1.0)

        def blob(x, y):
            return Circle(radius=0.13, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([x, y, 0])
        top_y = by + h - 0.7
        ys = [top_y, top_y - 0.6, top_y - 1.2, top_y - 1.8]
        blobs_l = VGroup(*[blob(bx - 0.42, y) for y in ys])
        blobs_r = VGroup(*[blob(bx + 0.25, y) for y in ys])
        al = label("auxin", bx + 2.7, top_y - 0.6, 28, ORANGE)
        al_a = arr([al.get_left()[0] - 0.05, al.get_left()[1], 0], [bx + 0.95, top_y - 0.6, 0], ORANGE, w=3, tip=0.16)
        self.at("hypothesis says")
        self.play(FadeIn(blobs_l), FadeIn(blobs_r), FadeIn(al), FadeIn(al_a), run_time=0.8)
        self.at("sideways toward")
        side = arr([bx - 0.5, ys[0] + 0.55, 0], [bx + 0.5, ys[0] + 0.55, 0], ORANGE, w=6)
        self.play(GrowArrow(side),
                  *[blobs_l[i].animate.move_to([bx + 0.62, ys[i] - 0.3, 0]) for i in (0, 1, 2)],
                  run_time=1.6)
        self.at("elongates faster")
        fa = arr([bx + 1.2, by + 0.5, 0], [bx + 1.2, by + 2.2, 0], GREEN, w=6)
        fl = VGroup(T("shaded flank", 24, GREEN), T("grows faster", 24, GREEN)).arrange(DOWN, buff=0.06).move_to([bx + 2.45, by + 1.35, 0])
        self.play(GrowArrow(fa), FadeIn(fl), run_time=0.7)
        self.at("bends toward")
        bb = 0.5
        left1 = band([bx, by, 0], h, bb, -w / 2, 0.0)
        right1 = band([bx, by, 0], h, bb, 0.0, w / 2)
        self.play(Transform(left0, left1), Transform(right0, right1), FadeOut(side), FadeOut(blobs_l), FadeOut(blobs_r),
                  FadeOut(al), FadeOut(al_a), FadeOut(fa), FadeOut(fl), run_time=1.4)
        # PIN cell
        cx, cy = 3.6, 0.5
        self.at("carrier called")
        self.play(*[m.animate.shift(LEFT * 1.5) for m in (gr, left0, right0, lamp_r, lamp_l, ll, sl)], run_time=0.6)
        cell = RoundedRectangle(corner_radius=0.2, width=3.0, height=2.4, stroke_color=GREEN, stroke_width=3,
                                fill_color=GREEN, fill_opacity=0.12).move_to([cx, cy, 0])
        cap = VGroup(T("a cell of the", 24, GREY), T("Arabidopsis hypocotyl", 24, GREY)).arrange(DOWN, buff=0.06).move_to([cx, cy + 2.0, 0])
        self.play(FadeIn(cell), FadeIn(cap), run_time=0.7)
        self.at("one face")
        pin = RoundedRectangle(corner_radius=0.1, width=0.3, height=1.1, stroke_color=PURPLE, stroke_width=3,
                               fill_color=PURPLE, fill_opacity=0.7).move_to([cx + 1.5, cy, 0])
        pl = label("PIN3 carrier", cx + 0.35, cy - 1.75, 26, PURPLE)
        pl_a = arr([cx + 1.0, cy - 1.5, 0], [cx + 1.5, cy - 0.6, 0], PURPLE, w=3, tip=0.16)
        self.play(FadeIn(pin), FadeIn(pl), GrowArrow(pl_a), run_time=0.7)
        self.at("repositioning them")
        ds = VGroup(*[blob(cx - 0.7 + 0.4 * k, cy) for k in range(3)])
        out = arr([cx + 0.7, cy, 0], [cx + 2.6, cy, 0], ORANGE, w=6)
        self.play(FadeIn(ds), GrowArrow(out), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        base_y = -2.2
        u = 1.15                        # 0.03 mg per L = one unit of height
        bw = 1.9
        c1, c2 = -3.0, 0.0
        head = label("illustrative numbers, not a real experiment", -1.0, 3.3, 28, TEXT)
        sub = label("auxin from agar blocks, in mg per L", -1.8, 2.7, 24, GREY)
        base = Line([-4.4, base_y, 0], [1.4, base_y, 0], color=GREY, stroke_width=3)
        lit = Rectangle(width=bw, height=1 * u, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.28).move_to([c1, base_y + 0.5 * u, 0])
        sha = Rectangle(width=bw, height=2 * u, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.6).move_to([c1, base_y + 2.0 * u, 0])
        t_lit = M("0.03", 26, TEXT).move_to(lit)
        t_sha = M("0.06", 26, TEXT).move_to(sha)
        k_lit = label("lit half", c1 - bw / 2 - 0.95, base_y + 0.5 * u, 24, YELLOW)
        k_sha = label("shaded half", c1 - bw / 2 - 1.1, base_y + 2.0 * u, 24, GREY)
        cap1 = VGroup(T("lit from one side,", 24, GREY), T("split tip", 24, GREY)).arrange(DOWN, buff=0.08).move_to([c1, base_y - 0.65, 0])
        dk = Rectangle(width=bw, height=3 * u, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.45).move_to([c2, base_y + 1.5 * u, 0])
        t_dk = M("0.09", 26, TEXT).move_to(dk)
        cap2 = VGroup(T("kept in the dark,", 24, GREY), T("whole tips", 24, GREY)).arrange(DOWN, buff=0.08).move_to([c2, base_y - 0.65, 0])
        # schematic of the split tip (each half drains into its own block)
        dx = 4.2
        tipb = RoundedRectangle(corner_radius=0.15, width=2.0, height=0.9, stroke_color=GREEN, stroke_width=3,
                                fill_color=GREEN, fill_opacity=0.3).move_to([dx, 1.0, 0])
        barrier = Line([dx, 1.55, 0], [dx, 0.0, 0], color=BLUE, stroke_width=5)
        ag1 = RoundedRectangle(corner_radius=0.06, width=0.9, height=0.3, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.3).move_to([dx - 0.55, 0.2, 0])
        ag2 = ag1.copy().move_to([dx + 0.55, 0.2, 0])
        sr = rays(dx - 2.5, 1.0, n=3, gap=0.4, length=0.9)
        d_cap = VGroup(T("tip split by a barrier,", 24, GREY), T("each half into its own block", 24, GREY)).arrange(DOWN, buff=0.06).move_to([dx, 2.45, 0])
        d_l = label("lit half", dx - 0.95, -0.3, 24, YELLOW)
        d_s = label("shaded half", dx + 1.0, -0.3, 24, GREY)
        diag = VGroup(tipb, barrier, ag1, ag2, sr, d_cap, d_l, d_s)
        self.at("worked bioassay")
        self.play(FadeIn(head), FadeIn(diag), run_time=0.8)
        self.at("illustrative")
        self.play(FadeIn(sub), FadeIn(base), FadeIn(cap1), FadeIn(cap2), run_time=0.7)
        self.at("lit half")
        self.play(FadeIn(lit), FadeIn(t_lit), FadeIn(k_lit), run_time=0.7)
        self.at("shaded half")
        self.play(FadeIn(sha), FadeIn(t_sha), FadeIn(k_sha), run_time=0.7)
        self.at("kept in the dark")
        self.play(FadeIn(dk), FadeIn(t_dk), run_time=0.8)
        self.at("same total")
        eq = DashedLine([c1 - bw / 2 - 0.1, base_y + 3 * u, 0], [c2 + bw / 2 + 0.1, base_y + 3 * u, 0], color=TEXT, stroke_width=3)
        eqt = T("same total", 26, TEXT).next_to(eq, UP, buff=0.15)
        self.play(Create(eq), FadeIn(eqt), run_time=0.8)
        self.at("did not destroy")
        self.play(FadeOut(diag), run_time=0.3)
        g1 = VGroup(T("light did not destroy auxin", 28, TEXT), T("on the lit side:", 28, TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        g2 = VGroup(T("it moved auxin to", 28, ORANGE), T("the shaded side", 28, ORANGE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        g = VGroup(g1, g2).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        g.move_to([0, 0, 0]).align_to([1.65, 0, 0], LEFT).shift(UP * 1.2)
        g2.set_opacity(0)
        self.play(FadeIn(g1), run_time=0.8)
        self.at("it moved")
        self.play(g2.animate.set_opacity(1), run_time=0.6)
        self.at("growth follows")
        rule = VGroup(T("each flank's growth follows", 28, GREEN), T("its auxin level;", 28, GREEN),
                      T("the curve is the difference", 28, GREEN)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        rule.align_to([1.65, 0, 0], LEFT).move_to([0, -1.5, 0], coor_mask=[0, 1, 0])
        self.play(FadeIn(rule), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Each flank's growth follows its auxin level; the curve is the difference."
