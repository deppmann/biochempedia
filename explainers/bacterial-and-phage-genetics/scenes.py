"""Bacterial and phage genetics: time of entry becomes the map  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept, whole film)
  BLUE   = DNA: the chromosome ring and the map line
  PURPLE = a marker gene (a, b, c, d) wherever it appears
  ORANGE = the Hfr donor cell
  GREEN  = the recipient cell, and recombinant colonies
  GOLD   = F and the origin of transfer
  YELLOW = time and gaps, in minutes
  RED    = a missing ability, the blender break, absent
  GREY   = outlines, plates, labels
All numbers are the lesson's worked problem (a): Hfr 1 a 8, b 14, c 20, d 31 min; Hfr 2 d 4, c 15, b 21, a 27 min.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
DEG = 3.6                                   # degrees of ring per minute (100 minutes = 360 degrees)
T1 = {"a": 8, "b": 14, "c": 20, "d": 31}    # Hfr strain 1 times of entry
T2 = {"d": 4, "c": 15, "b": 21, "a": 27}    # Hfr strain 2 times of entry
GEN_ANG = {k: 90 - DEG * v for k, v in T1.items()}   # origin 1 at 90 degrees, clockwise


def pt(c, r, ang):
    a = np.radians(ang)
    return np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0])


def cell(color, w=4.4, h=4.0, cr=1.3, op=0.14):
    return RoundedRectangle(corner_radius=cr, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=op)


def gene_chip(name, size=26):
    return chip(name, PURPLE, size=size, pad=0.14)


def ring_with_genes(c, r, names="abcd", lab=0.42, size=26):
    ring = Circle(radius=r, stroke_color=BLUE, stroke_width=6).move_to(c)
    dots, labs = VGroup(), VGroup()
    for n in names:
        d = Dot(pt(c, r, GEN_ANG[n]), radius=0.11, color=PURPLE)
        l = T(n, size, PURPLE, weight=BOLD).move_to(pt(c, r + lab, GEN_ANG[n]))
        dots.add(d); labs.add(l)
    return ring, dots, labs


def small_pair(x, y, s=1.0):
    d = cell(ORANGE, 1.2 * s, 1.2 * s, 0.4 * s).move_to([x - 0.95 * s, y, 0])
    r = cell(GREEN, 1.2 * s, 1.2 * s, 0.4 * s).move_to([x + 0.95 * s, y, 0])
    b = Line(d.get_right(), r.get_left(), color=GREY, stroke_width=6)
    return VGroup(d, r, b)


def plate(x, y, w=3.4, h=1.9):
    e = Ellipse(width=w, height=h, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    return e


def colonies(x, y, n=6, seed=1):
    rng = np.random.RandomState(seed)
    ds = VGroup()
    while len(ds) < n:
        dx, dy = rng.uniform(-1.1, 1.1), rng.uniform(-0.5, 0.5)
        if (dx / 1.2) ** 2 + (dy / 0.6) ** 2 < 1:
            ds.add(Dot([x + dx, y + dy, 0], radius=0.11, color=GREEN))
    return ds


# --- timeline rows ---------------------------------------------------------------------------
def X(t):
    return -4.8 + 0.28 * t


def row(y, times, order):
    """line from 0 to 35 min with marker chips and their times. Returns dict of parts."""
    line = Line([X(0), y, 0], [X(35), y, 0], color=BLUE, stroke_width=6)
    chips, tl, sticks = {}, {}, {}
    for n in order:
        x = X(times[n])
        chips[n] = gene_chip(n).move_to([x, y + 0.62, 0])
        sticks[n] = Line([x, y, 0], [x, y + 0.3, 0], color=PURPLE, stroke_width=4)
        tl[n] = M(f"{times[n]} min", 24, YELLOW).move_to([x, y + 1.2, 0])
    return line, chips, tl, sticks


def brackets(y, xs, labels, color=YELLOW):
    g = VGroup()
    for (x0, x1), lb in zip(zip(xs[:-1], xs[1:]), labels):
        ln = VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                    Line([x0, y - 0.12, 0], [x0, y + 0.12, 0], color=color, stroke_width=4),
                    Line([x1, y - 0.12, 0], [x1, y + 0.12, 0], color=color, stroke_width=4))
        g.add(VGroup(ln, M(lb, 26, color).move_to([(x0 + x1) / 2, y - 0.38, 0])))
    return g


def origin_mark(x, y, direction):
    """gold dot on the line with a short arrow along it, pointing `direction` (+1 right, -1 left)."""
    dot = Dot([x, y, 0], radius=0.17, color=GOLD)
    ar = Arrow([x + 0.2 * direction, y, 0], [x + 0.95 * direction, y, 0], buff=0, color=GOLD, stroke_width=7,
               tip_length=0.22, max_tip_length_to_length_ratio=0.6)
    lb = T("origin", 22, GOLD).move_to([x, y - 0.45, 0])
    return VGroup(dot, ar, lb)


class S00Title(TitleCard):
    LESSON = "Bacterial and phage genetics"
    TITLE = "Time of entry becomes the map"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        c1 = cell(ORANGE, 3.0, 2.2, 0.9).move_to([-4.2, 2.1, 0])
        c2 = cell(GREEN, 3.0, 2.2, 0.9).move_to([4.2, 2.1, 0])
        t1 = T("strain 1", 26, ORANGE).move_to(c1)
        t2 = T("strain 2", 26, GREEN).move_to(c2)
        n1 = T("cannot make\nseveral nutrients", 24, RED, line_spacing=0.8).move_to([-4.2, 0.4, 0])
        n2 = T("cannot make\nseveral nutrients", 24, RED, line_spacing=0.8).move_to([4.2, 0.4, 0])
        # opening: the two things bacteria lack
        m1 = T("meiosis", 54, TEXT, font=TITLE_FONT).move_to([-3.0, 0.6, 0])
        m2 = T("zygote", 54, TEXT, font=TITLE_FONT).move_to([3.0, 0.6, 0])
        x1 = Line(m1.get_left() + LEFT * 0.2, m1.get_right() + RIGHT * 0.2, color=RED, stroke_width=9)
        x2 = Line(m2.get_left() + LEFT * 0.2, m2.get_right() + RIGHT * 0.2, color=RED, stroke_width=9)
        self.at("no meiosis")
        self.play(FadeIn(m1, shift=UP * 0.2), run_time=0.5)
        self.play(Create(x1), run_time=0.4)
        self.at("no zygote")
        self.play(FadeIn(m2, shift=UP * 0.2), run_time=0.5)
        self.play(Create(x2), run_time=0.4)
        self.at("E coli strains")
        self.play(FadeOut(VGroup(m1, m2, x1, x2)), run_time=0.3)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(t1), FadeIn(t2), run_time=0.5)

        pl = plate(0, -1.3, 3.8, 2.1)
        pl_lbl = T("plate with none of the nutrients", 24, GREY).move_to([0, -2.85, 0])
        a1 = Arrow([-2.6, 1.3, 0], [-0.9, -0.5, 0], buff=0, color=GREY, stroke_width=4)
        a2 = Arrow([2.6, 1.3, 0], [0.9, -0.5, 0], buff=0, color=GREY, stroke_width=4)
        self.at("were mixed")
        self.play(FadeIn(pl), GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        self.at("could not make")
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.6)
        col = colonies(0, -1.3, 5, seed=3)
        self.at("A few cells grew")
        self.play(LaggedStart(*[GrowFromCenter(d) for d in col], lag_ratio=0.2), FadeIn(pl_lbl), run_time=1.0)

        self.at("Neither strain alone")
        p1 = plate(-4.6, -1.3, 2.6, 1.5)
        p2 = plate(4.6, -1.3, 2.6, 1.5)
        z1 = M("0", 40, RED, weight=BOLD).move_to(p1)
        z2 = M("0", 40, RED, weight=BOLD).move_to(p2)
        l1 = T("strain 1 alone", 24, ORANGE).move_to([-4.6, -2.5, 0])
        l2 = T("strain 2 alone", 24, GREEN).move_to([4.6, -2.5, 0])
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(z1), FadeIn(z2), FadeIn(l1), FadeIn(l2), run_time=0.8)

        # the question: the two strains become donor and recipient of the next scene
        self.at("where did the genes")
        everything = VGroup(pl, pl_lbl, a1, a2, col, p1, p2, z1, z2, l1, l2, n1, n2)
        tc1 = cell(ORANGE, 4.4, 4.4, 1.4).move_to([-4.0, 0.15, 0])
        tc2 = cell(GREEN, 4.4, 4.4, 1.4).move_to([4.0, 0.15, 0])
        self.play(FadeOut(everything), ReplacementTransform(c1, tc1), ReplacementTransform(c2, tc2),
                  t1.animate.move_to([-4.0, -2.55, 0]), t2.animate.move_to([4.0, -2.55, 0]), run_time=1.0)
        ring = Circle(radius=1.25, stroke_color=BLUE, stroke_width=6).move_to([-4.0, 0.25, 0])
        self.play(Create(ring), run_time=0.6)
        q = T("?", 120, BLUE, weight=BOLD).move_to([0, 0.15, 0])
        self.at("get from one bacterium")
        dna = DashedLine([-1.7, 0.15, 0], [1.7, 0.15, 0], color=BLUE, stroke_width=6, dash_length=0.2)
        dl = T("DNA", 30, BLUE).move_to([0, -1.0, 0])
        self.play(Create(dna), FadeIn(q), FadeIn(dl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Hfr(SpokenScene):
    def construct(self):
        cd, cr_ = np.array([-4.0, 0.15, 0]), np.array([4.0, 0.15, 0])
        donor = cell(ORANGE, 4.4, 4.4, 1.4).move_to(cd)
        recip = cell(GREEN, 4.4, 4.4, 1.4).move_to(cr_)
        dl = T("donor", 28, ORANGE).move_to([-4.0, -2.55, 0])
        rl = T("recipient", 28, GREEN).move_to([4.0, -2.55, 0])
        ring, dots, labs = ring_with_genes(cd + np.array([0, 0.1, 0]), 1.25)
        # the donor's chromosome has no F yet
        self.add(donor, recip, dl, rl, ring, dots, labs)
        bridge = Line(donor.get_right() + [0.1, 0, 0], recip.get_left() - [0.1, 0, 0], color=GREY, stroke_width=10)
        self.at("touches a recipient")
        self.play(Create(bridge), run_time=0.6)
        self.at("passes DNA straight across")
        pulse = Dot(bridge.get_left(), radius=0.14, color=BLUE)
        self.play(FadeIn(pulse), run_time=0.15)
        self.play(pulse.animate.move_to(bridge.get_right()), run_time=0.7, rate_func=linear)
        self.play(FadeOut(pulse), run_time=0.15)

        # F
        fc = Circle(radius=0.32, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.25).move_to([-5.2, -1.5, 0])
        ft = T("F", 28, GOLD, weight=BOLD).move_to(fc)
        self.at("carries F")
        self.play(FadeIn(fc), FadeIn(ft), run_time=0.6)
        c0 = cd + np.array([0, 0.1, 0])
        f_arc = Arc(radius=1.25, start_angle=np.radians(70), angle=np.radians(40), arc_center=c0, color=GOLD, stroke_width=14)
        f_lbl = T("F", 28, GOLD, weight=BOLD).move_to(pt(c0, 1.7, 90))
        self.at("joins the chromosome")
        self.play(ReplacementTransform(VGroup(fc), f_arc), ReplacementTransform(ft, f_lbl), run_time=0.9)
        hfr = T("Hfr donor", 28, ORANGE, weight=BOLD).move_to(dl)
        # the origin arrow inside the ring
        og = Arrow(pt(c0, 0.9, 80), pt(c0, 0.9, 40), buff=0, color=GOLD, stroke_width=7, tip_length=0.2,
                   path_arc=-0.5, max_tip_length_to_length_ratio=0.6)
        self.at("called")
        self.play(ReplacementTransform(dl, hfr), run_time=0.5)
        self.at("Transfer starts inside")
        self.play(Indicate(f_arc, color=GOLD, scale_factor=1.15), FadeIn(og), run_time=0.8)

        # markers cross in order
        self.at("pulls the chromosome")
        landing = [2.9, 3.7, 4.5, 5.3]
        for n, x in zip("abcd", landing):
            ch = gene_chip(n)
            start = pt(c0, 1.25, GEN_ANG[n])
            ch.move_to(start)
            path = VMobject().set_points_as_corners([start, np.array([-1.9, 0.15, 0]), np.array([x, 0.15, 0])])
            self.add(ch)
            self.play(MoveAlongPath(ch, path), run_time=0.55, rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Blender(SpokenScene):
    def construct(self):
        head = T("Interrupted mating", 34, font=TITLE_FONT).to_edge(UP, buff=0.4)
        self.play(FadeIn(head), run_time=0.2)
        self.at("and Jacob")
        pairs = [small_pair(x, 0.7, 1.1) for x in (-4.2, 0.0, 4.2)]
        hl = T("Hfr donor", 24, ORANGE).next_to(pairs[0][0], DOWN, buff=0.2)
        rl = T("F− recipient", 24, GREEN).next_to(pairs[0][1], DOWN, buff=0.2)
        self.play(*[FadeIn(p, shift=UP * 0.2) for p in pairs], run_time=0.8)
        self.at("mixed")
        self.play(FadeIn(hl), FadeIn(rl), run_time=0.5)

        self.at("broke the pairs apart")
        cuts = VGroup()
        for p in pairs:
            m = p[2].get_center()
            cuts.add(VGroup(Line(m + [-0.3, 0.4, 0], m + [0.3, -0.4, 0], color=RED, stroke_width=8),
                            Line(m + [0.3, 0.4, 0], m + [-0.3, -0.4, 0], color=RED, stroke_width=8)))
        blender = chip("blender", RED, size=26).next_to(head, DOWN, buff=0.25)
        self.play(FadeIn(blender, shift=DOWN * 0.2), *[Create(c) for c in cuts], run_time=0.6)
        self.play(*[p[2].animate.set_opacity(0) for p in pairs],
                  *[p[0].animate.shift(LEFT * 0.3) for p in pairs], *[p[1].animate.shift(RIGHT * 0.3) for p in pairs],
                  FadeOut(cuts), FadeOut(hl), FadeOut(rl), run_time=0.6)

        self.at("plated the recipients")
        pe = plate(-3.9, 0.1, 3.4, 2.0)
        pl_ = plate(3.9, 0.1, 3.4, 2.0)
        e_l = T("earlier sample", 26, GREY).move_to([-3.9, -1.3, 0])
        l_l = T("later sample", 26, GREY).move_to([3.9, -1.3, 0])
        self.play(FadeOut(blender), FadeOut(VGroup(*[p[0] for p in pairs])), FadeOut(VGroup(*[p[1] for p in pairs])),
                  FadeIn(pe), FadeIn(pl_), FadeIn(e_l), FadeIn(l_l), run_time=0.8)
        self.at("only recombinants grow")
        note = T("only\nrecombinants\ngrow", 24, GREEN, line_spacing=0.8).move_to([0, 0.1, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("Each donor gene")
        z = T("marker a: absent", 26, RED).move_to([-3.9, -1.85, 0])
        col = colonies(3.9, 0.1, 6, seed=5)
        pres = T("marker a: present", 26, GREEN).move_to([3.9, -1.85, 0])
        self.play(FadeIn(z), LaggedStart(*[GrowFromCenter(d) for d in col], lag_ratio=0.15), FadeIn(pres), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Gaps(SpokenScene):
    def construct(self):
        y = 0.1
        lab = T("Hfr strain 1", 26, ORANGE).move_to([-5.5, y + 1.9, 0]).align_to([-6.2, 0, 0], LEFT)
        line, chips, tl, sticks = row(y, T1, "abcd")
        self.at("Take one")
        self.play(FadeIn(lab), Create(line), run_time=0.7)
        cues = {"a": "first appears", "b": "Marker B", "c": "marker C", "d": "marker D"}
        for n in "abcd":
            self.at(cues[n])
            ch = chips[n]
            ch.save_state()
            ch.shift(UP * 1.2).set_opacity(0)
            self.play(ch.animate.restore(), FadeIn(sticks[n]), run_time=0.5)
            self.play(FadeIn(tl[n], shift=DOWN * 0.1), run_time=0.3)
        self.at("steady rate")
        axl = T("minutes from the start of mating", 24, GREY).move_to([0.3, y - 0.6, 0])
        self.play(FadeIn(axl), run_time=0.5)
        self.at("time of entry")
        self.play(*[Indicate(tl[n], color=YELLOW, scale_factor=1.08) for n in "abcd"], run_time=0.9)
        self.at("is a position")
        pos = T("so time is position on the chromosome", 26, BLUE).move_to([0.3, y - 0.6, 0])
        self.play(Transform(axl, pos), line.animate.set_stroke(width=10), run_time=0.8)
        self.at("gaps")
        xs = [X(T1[n]) for n in "abcd"]
        br = brackets(y - 1.5, xs, ["6", "6", "11"])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in br], lag_ratio=0.4), run_time=1.3)
        unit = T("minutes", 24, YELLOW).move_to([X(33) + 0.3, y - 1.9, 0])
        self.play(FadeIn(unit), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reverse(SpokenScene):
    def construct(self):
        y1, y2 = 1.7, -1.4
        l1 = T("Hfr 1", 24, ORANGE).move_to([-5.65, y1, 0])
        l2 = T("Hfr 2", 24, ORANGE).move_to([-5.65, y2, 0])
        line1, chips1, tl1, st1 = row(y1, T1, "abcd")
        br1 = brackets(y1 - 0.95, [X(T1[n]) for n in "abcd"], ["6", "6", "11"])
        # strain 1 is carried over from the last scene
        self.add(l1, line1, *chips1.values(), *tl1.values(), *st1.values(), br1)
        self.wait(0.3)
        line2, chips2, tl2, st2 = row(y2, T2, "dcba")
        self.at("A second")
        self.play(FadeIn(l2), FadeIn(line2), run_time=0.2)
        cues = {"d": "gives D", "c": "C at", "b": "B at", "a": "and at"}
        for n in "dcba":
            self.at(cues[n], nth=0)
            self.play(FadeIn(chips2[n], shift=DOWN * 0.3), FadeIn(st2[n]), FadeIn(tl2[n]), run_time=0.45)
        self.at("order runs backwards")
        arr_ = Arrow([X(2), y2 - 1.0, 0], [X(33), y2 - 1.0, 0], buff=0, color=GREY, stroke_width=4)
        order_l = T("d, c, b, a", 26, PURPLE).move_to([0.2, y2 - 1.45, 0])
        self.play(Create(arr_), FadeIn(order_l), run_time=0.7)
        self.at("times differ")
        o1 = origin_mark(X(0), y1, 1)
        o2 = origin_mark(X(0), y2, 1)
        self.play(FadeIn(o1), FadeIn(o2), run_time=0.6)
        self.at("gaps are")
        self.play(FadeOut(arr_), FadeOut(order_l), run_time=0.3)
        br2 = brackets(y2 - 0.95, [X(T2[n]) for n in "dcba"], ["11", "6", "6"])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in br2], lag_ratio=0.4), run_time=1.2)

        # read in reverse: the row flips onto strain 1's map
        self.at("Read in reverse")
        self.play(FadeOut(br2), run_time=0.2)
        mir = lambda t: X(35 - t)
        anims = []
        for n in "dcba":
            x = mir(T2[n])
            anims += [chips2[n].animate.move_to([x, y2 + 0.62, 0]),
                      tl2[n].animate.move_to([x, y2 + 1.2, 0]),
                      st2[n].animate.move_to([x, y2 + 0.15, 0])]
        o2_new = origin_mark(X(35), y2, -1)
        anims.append(Transform(o2, o2_new))
        self.play(*anims, run_time=1.3)
        xs2 = [mir(T2[n]) for n in "abcd"]
        br2n = brackets(y2 - 0.95, xs2, ["6", "6", "11"])
        self.at("same map")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in br2n], lag_ratio=0.3), run_time=0.7)
        self.play(Indicate(br1, color=YELLOW, scale_factor=1.05), Indicate(br2n, color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.at("origin lies")
        self.play(Indicate(o2, color=GOLD, scale_factor=1.3), run_time=0.8)
        self.at("opposite orientation")
        self.play(Indicate(o2, color=GOLD, scale_factor=1.3), Indicate(o1, color=GOLD, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Circle(SpokenScene):
    def construct(self):
        c = np.array([-3.0, -0.1, 0])
        R = 2.5
        ring, dots, labs = ring_with_genes(c, R, lab=0.42)
        self.play(Create(ring), FadeIn(dots), FadeIn(labs), run_time=1.0)
        # Hfr 1: origin at 90 degrees, clockwise
        og1 = Dot(pt(c, R, 90), radius=0.2, color=GOLD)
        arc1 = Arc(radius=R - 0.3, start_angle=np.radians(90), angle=-np.radians(DEG * 33), arc_center=c, color=GOLD, stroke_width=7)
        arc1.add_tip(tip_length=0.25)
        # Hfr 2: origin 4 minutes beyond d, the other way round
        a2 = GEN_ANG["d"] - DEG * 4
        og2 = Dot(pt(c, R, a2), radius=0.2, color=GOLD)
        arc2 = Arc(radius=R - 0.6, start_angle=np.radians(a2), angle=np.radians(DEG * 28), arc_center=c, color=GOLD, stroke_width=7)
        arc2.add_tip(tip_length=0.25)
        k1 = chip("Hfr 1: a, b, c, d", GOLD, size=26).move_to([3.7, 2.0, 0])
        k2 = chip("Hfr 2: d, c, b, a", GOLD, size=26).move_to([3.7, 0.9, 0])
        ol1 = T("origin", 22, GOLD).move_to(pt(c, R + 0.5, 90))
        ol2 = T("origin", 22, GOLD).move_to(pt(c, R + 0.75, a2))
        self.at("different sites")
        self.play(FadeIn(og1), FadeIn(og2), FadeIn(ol1), FadeIn(ol2), run_time=0.6)
        self.at("overlapping orders")
        self.play(Create(arc1), FadeIn(k1), run_time=1.0)
        self.play(Create(arc2), FadeIn(k2), run_time=1.0)
        self.at("closed into a circle")
        self.play(Indicate(ring, color=BLUE, scale_factor=1.04), run_time=0.9)
        self.at("100 minutes")
        mins = T("about\n100 minutes", 30, YELLOW, line_spacing=0.8).move_to(c)
        self.play(FadeIn(mins), run_time=0.7)
        self.at("runs from")
        rng_ = M("0 to 100 minutes", 28, YELLOW).move_to([3.7, -0.5, 0])
        self.play(FadeIn(rng_, shift=UP * 0.1), run_time=0.7)
        self.at("Keep this rule")
        rule = T("The gaps are\nthe map.", 44, TEXT, font=TITLE_FONT, line_spacing=0.9).move_to([3.7, -2.2, 0])
        self.play(Write(rule), run_time=1.4)
        self.finish()


class S07End(EndCard):
    LINE = "The gaps between times of entry are the map."
