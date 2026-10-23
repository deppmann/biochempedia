"""Evidence for Evolution  (Biochemistrypedia, grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = fossils and the fossil record
  ORANGE = bones as evidence (upper arm bone); the other bone types have their own colors, bones scene only
  PINK / PURPLE / TEAL = lower arm bones / wrist bones / finger bones (matching sets, bones scene only)
  GREEN  = DNA, the bases, "more similar"
  GOLD   = common ancestor, the shared family story
  YELLOW = differences, the open question
  RED    = extinct, gaps, no bones, "not a guess"
  GREY   = outlines, neutral parts
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PINK = "#E58FB5"
PURPLE = "#B58CD9"
TEAL_B = "#3FB8C0"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def scallop(hinge, r, col, fillop=0.3):
    """a scallop shell drawn as a ridged fan (schematic outline)."""
    hinge = np.array(hinge, dtype=float)
    a0, a1 = 35, 145
    fan = Sector(radius=r, start_angle=a0 * DEGREES, angle=(a1 - a0) * DEGREES, arc_center=hinge,
                 stroke_color=col, stroke_width=5, fill_color=col, fill_opacity=fillop)
    ridges = VGroup(*[Line(hinge + 0.25 * r * np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0]),
                           hinge + 0.95 * r * np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0]),
                           color=col, stroke_width=3) for a in np.linspace(a0 + 8, a1 - 8, 7)])
    ears = Polygon(hinge + LEFT * 0.35 * r, hinge + RIGHT * 0.35 * r, hinge + RIGHT * 0.25 * r + DOWN * 0.12 * r,
                   hinge + LEFT * 0.25 * r + DOWN * 0.12 * r, stroke_color=col, stroke_width=4,
                   fill_color=col, fill_opacity=fillop)
    return VGroup(fan, ridges, ears)


class S00Title(TitleCard):
    LESSON = "Evidence for Evolution"
    TITLE = "Three Kinds of Evidence Agree"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        rock = RoundedRectangle(corner_radius=0.2, width=4.6, height=3.2, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.15).move_to([-3.9, 0.55, 0])
        rl = T("rock", 26, GREY).move_to([-5.7, -0.8, 0])
        sh = scallop([-3.9, -0.35, 0], 2.1, BLUE, 0.3)
        hl = T("Virginia's state fossil", 32, BLUE, weight=BOLD).move_to([-3.9, 2.7, 0])
        self.at("state fossil is")
        self.play(FadeIn(rock), FadeIn(rl), FadeIn(hl, shift=DOWN * 0.1), run_time=0.6)
        self.play(GrowFromPoint(sh, [-3.9, -0.35, 0]), run_time=0.9)
        self.at("millions of years old")
        ol = T("millions of years old", 30, BLUE).move_to([-3.9, -1.5, 0])
        self.play(FadeIn(ol, shift=UP * 0.1), run_time=0.5)
        self.at("looks a lot like")
        lk = T("looks a lot\nlike", 30, YELLOW, weight=BOLD, line_spacing=0.8).move_to([0, 0.75, 0])
        ar = DoubleArrow([-1.0, 0.0, 0], [1.0, 0.0, 0], color=YELLOW, stroke_width=5, buff=0, tip_length=0.2)
        self.play(FadeIn(lk, scale=0.9), GrowFromCenter(ar), run_time=0.5)
        self.at("on a beach today")
        sh2 = scallop([3.9, -0.35, 0], 2.1, TEXT, 0.0)
        hl2 = T("scallop shell on a beach today", 30, TEXT, weight=BOLD).move_to([3.4, 2.7, 0])
        sand = Line([1.7, -0.55, 0], [6.1, -0.55, 0], color=GREY, stroke_width=4)
        self.play(FadeIn(hl2, shift=DOWN * 0.1), GrowFromPoint(sh2, [3.9, -0.35, 0]), Create(sand), run_time=0.8)
        self.at("How do scientists")
        q1 = T("How do scientists know that living things", 32, TEXT, weight=BOLD)
        q2 = T("have changed over time, and are related?", 32, YELLOW, weight=BOLD)
        q = VGroup(q1, q2).arrange(DOWN, buff=0.15).move_to([0, -2.85, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fossils(SpokenScene):
    def construct(self):
        fc = chip("fossil", BLUE, 34).move_to([-5.1, 3.0, 0])
        ft = T("remains or traces of a living thing from the past", 28, TEXT)
        ft.move_to([-3.85 + ft.width / 2, 3.0, 0])
        self.at("A fossil is")
        self.play(FadeIn(fc, scale=0.9), run_time=0.4)
        self.play(FadeIn(ft, shift=RIGHT * 0.15), run_time=0.7)
        ex = VGroup(*[chip(n, BLUE, 30) for n in ("shell", "bone", "tooth", "footprint")])
        ex.arrange(RIGHT, buff=0.5).move_to([0.2, 1.75, 0])
        self.at("Shells")
        self.play(FadeIn(ex[0], shift=UP * 0.1), run_time=0.35)
        self.at("bones")
        self.play(FadeIn(ex[1], shift=UP * 0.1), run_time=0.35)
        self.at("teeth")
        self.play(FadeIn(ex[2], shift=UP * 0.1), run_time=0.35)
        self.at("footprints")
        self.play(FadeIn(ex[3], shift=UP * 0.1), run_time=0.35)
        self.at("Fossils are rare")
        slots = VGroup(*[Square(side_length=0.7, stroke_color=GREY, stroke_width=3).move_to([-3.1 + 0.85 * i, 0.15, 0]) for i in range(9)])
        rc = chip("fossil record", BLUE, 30).move_to([-5.1, 0.15, 0])
        self.play(FadeIn(rc), Create(slots), run_time=0.9)
        self.at("all the fossils found")
        filled = [0, 1, 3, 6, 8]
        self.play(*[slots[i].animate.set_stroke(BLUE, 4).set_fill(BLUE, 0.5) for i in filled], run_time=0.8)
        self.at("has gaps")
        empty = [2, 4, 5, 7]
        for i in empty:
            slots[i].generate_target()
        self.play(*[slots[i].animate.set_stroke(RED, 4).set_fill(RED, 0.0) for i in empty], run_time=0.5)
        gl = T("gaps", 30, RED, weight=BOLD).move_to([5.2, 0.15, 0])
        self.play(FadeIn(gl, shift=LEFT * 0.1), run_time=0.4)
        self.at("many kinds of life")
        nl = T("many kinds of life that are not alive now", 28, BLUE).move_to([0, -1.2, 0])
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.6)
        self.at("A group is extinct")
        ec = chip("extinct", RED, 34).move_to([-3.9, -2.2, 0])
        et = T("no living members left", 28, TEXT)
        et.move_to([-2.45 + et.width / 2, -2.2, 0])
        self.play(FadeIn(ec, scale=0.9), run_time=0.4)
        self.at("no living members")
        self.play(FadeIn(et, shift=RIGHT * 0.15), run_time=0.5)
        self.at("Trilobites")
        tr = chip("trilobites", BLUE, 32).move_to([-1.3, -3.1, 0])
        ar = arr([-0.0, -3.1, 0], [1.1, -3.1, 0], RED, w=5)
        ex2 = T("extinct", 32, RED, weight=BOLD).move_to([2.3, -3.1, 0])
        self.play(FadeIn(tr, shift=UP * 0.1), run_time=0.4)
        self.play(GrowArrow(ar), FadeIn(ex2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Timeline(SpokenScene):
    def construct(self):
        x_of = lambda mya: -5.7 + (550 - mya) / 550 * 11.4
        y0 = 0.0
        bar = Line([x_of(550), y0, 0], [x_of(0), y0, 0], color=GREY, stroke_width=7)
        l0 = T("550 million years ago", 24, GREY).move_to([x_of(550) + 1.3, y0 - 0.5, 0])
        l1 = T("today", 24, GREY).move_to([x_of(0) - 0.3, y0 - 0.5, 0])
        self.at("Here is one")
        self.play(Create(bar), FadeIn(l0), FadeIn(l1), run_time=0.9)
        head = T("one well-known early fossil per group", 32, BLUE, weight=BOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        self.at("It is not the oldest")
        nt = chip("not the oldest one found", RED, 28).move_to([0, 2.15, 0])
        self.play(FadeIn(nt, shift=DOWN * 0.1), run_time=0.5)
        items = [
            (518, "Early fish", "Haikouichthys, China", "up", "Early fish", -1),
            (365, "Four-legged animals", "Ichthyostega, Greenland", "down", "legged animals", 0),
            (205, "Mammal relatives", "Morganucodon teeth", "up", "Mammal relatives", 0),
            (150, "Bird-like dinosaurs", "Archaeopteryx", "down", "like dinosaurs", 0),
        ]
        # label centers chosen to stay inside the frame and not touch each other
        centers = {518: -4.2, 365: -1.9, 205: 0.9, 150: 3.8}
        for mya, name, fossil, side, cue, _ in items:
            x = x_of(mya)
            self.at(cue)
            dot = Dot([x, y0, 0], radius=0.17, color=BLUE)
            t1 = T(name, 28, BLUE, weight=BOLD)
            t2 = T(f"about {mya} million years old", 24, TEXT)
            t3 = T(fossil, 22, GREY)
            lab = VGroup(t1, t2, t3).arrange(DOWN, buff=0.1)
            cx = centers[mya]
            if side == "up":
                lab.move_to([cx, 1.15, 0]); lab.set_y(1.05)
                con = Line([x, y0 + 0.17, 0], [min(max(x, lab.get_left()[0] + 0.1), lab.get_right()[0] - 0.1), lab.get_bottom()[1] - 0.05, 0], color=BLUE, stroke_width=3)
            else:
                lab.move_to([cx, -1.95, 0])
                con = Line([x, y0 - 0.17, 0], [min(max(x, lab.get_left()[0] + 0.1), lab.get_right()[0] - 0.1), lab.get_top()[1] + 0.05, 0], color=BLUE, stroke_width=3)
            self.play(GrowFromCenter(dot), Create(con), FadeIn(lab, shift=(DOWN if side == "up" else UP) * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def limb(cx, base_y, up_h, lo_h, up_w, fing_len, fing_w, spread, cols):
    """a front limb as labelled blocks: 1 upper bone, 2 lower bones, wrist bones, finger bones."""
    cu, cl, cw, cf = cols
    up = RoundedRectangle(corner_radius=0.08, width=up_w, height=up_h, stroke_color=cu, stroke_width=3,
                          fill_color=cu, fill_opacity=0.5).move_to([cx, base_y + up_h / 2, 0])
    y1 = base_y + up_h + 0.06
    lw = 0.34
    lo = VGroup(*[RoundedRectangle(corner_radius=0.06, width=lw, height=lo_h, stroke_color=cl, stroke_width=3,
                                   fill_color=cl, fill_opacity=0.5).move_to([cx + dx, y1 + lo_h / 2, 0]) for dx in (-0.24, 0.24)])
    y2 = y1 + lo_h + 0.06
    wr = VGroup(*[Square(side_length=0.3, stroke_color=cw, stroke_width=3, fill_color=cw, fill_opacity=0.5)
                  .move_to([cx + dx, y2 + 0.13, 0]) for dx in (-0.34, 0, 0.34)])
    y3 = y2 + 0.26 + 0.06
    fi = VGroup(*[RoundedRectangle(corner_radius=0.05, width=fing_w, height=fing_len, stroke_color=cf, stroke_width=3,
                                   fill_color=cf, fill_opacity=0.5).move_to([cx + k * spread, y3 + fing_len / 2, 0])
                  for k in (-2, -1, 0, 1, 2)])
    return VGroup(up, lo, wr, fi)


class S04Bones(SpokenScene):
    def construct(self):
        cols = (ORANGE, PINK, PURPLE, TEAL_B)
        base = -2.2
        # name, cx, dims (up_h, lo_h, up_w, fing_len, fing_w, spread), label, job
        specs = [
            ("human arm", -2.5, (1.15, 1.2, 0.6, 0.95, 0.2, 0.24), None),
            ("cat leg", -0.2, (1.0, 1.2, 0.55, 0.8, 0.2, 0.24), "walking"),
            ("whale flipper", 2.1, (0.8, 0.85, 0.75, 1.5, 0.26, 0.3), "swimming"),
            ("bat wing", 4.6, (0.95, 1.45, 0.5, 1.5, 0.15, 0.36), "flying"),
        ]
        lm = [limb(cx, base, *d, cols) for _, cx, d, _ in specs]
        legend = [("one upper\narm bone", ORANGE, 0), ("two lower\narm bones", PINK, 1),
                  ("wrist bones", PURPLE, 2), ("finger\nbones", TEAL_B, 3)]
        hum = lm[0]
        ys = [hum[0].get_center()[1], hum[1].get_center()[1], hum[2].get_center()[1], hum[3].get_center()[1] + 0.1]
        names = [T(n, 26, TEXT, weight=BOLD) for n, *_ in specs]
        for nm, (n, cx, d, job) in zip(names, specs):
            nm.move_to([cx, -2.85, 0])
        self.at("Your arm has")
        self.play(FadeIn(lm[0]), FadeIn(names[0]), run_time=0.6)
        self.play(*[m.animate.set_stroke(GREY, 3).set_fill(GREY, 0.12) for m in (hum[0], *hum[1], *hum[2], *hum[3])], run_time=0.01)
        labs = []
        for (txt, col, idx), cue in zip(legend, ["one upper arm bone", "two lower arm bones", "wrist bones", "finger bones"]):
            self.at(cue)
            l = T(txt, 24, col, weight=BOLD, line_spacing=0.8)
            l.move_to([-5.15, ys[idx], 0])
            ln = Line([l.get_right()[0] + 0.1, ys[idx], 0], [-3.1 if idx != 3 else -3.0, ys[idx], 0], color=col, stroke_width=2.5)
            parts = [hum[0]] if idx == 0 else (list(hum[1]) if idx == 1 else (list(hum[2]) if idx == 2 else list(hum[3])))
            self.play(FadeIn(l), Create(ln), *[p.animate.set_stroke(col, 3).set_fill(col, 0.5) for p in parts], run_time=0.5)
            labs += [l, ln]
        self.at("A cat's front leg")
        self.play(FadeIn(lm[1]), FadeIn(names[1]), run_time=0.5)
        self.at("a whale's flipper")
        self.play(FadeIn(lm[2]), FadeIn(names[2]), run_time=0.5)
        self.at("a bat's wing")
        self.play(FadeIn(lm[3]), FadeIn(names[3]), run_time=0.5)
        self.at("have the same set")
        self.play(*[Indicate(m, color=TEXT, scale_factor=1.04) for m in lm], run_time=0.9)
        self.at("The shapes differ")
        self.wait(0.3)
        self.at("and the jobs differ")
        jobs = []
        for (n, cx, d, job), nm in zip(specs, names):
            if job:
                j = T(job, 24, YELLOW).move_to([cx, -3.3, 0])
                jobs.append(j)
        self.play(*[FadeIn(j, shift=UP * 0.1) for j in jobs], run_time=0.6)
        self.at("A common ancestor is")
        ca = chip("common ancestor", GOLD, 32).move_to([-0.2, 3.1, 0])
        self.play(FadeIn(ca, scale=0.9), run_time=0.5)
        self.at("Two or more kinds")
        tops = [m.get_top()[1] for m in lm]
        bar = Line([-2.5, 2.35, 0], [4.6, 2.35, 0], color=GOLD, stroke_width=4)
        stem = Line([-0.2, ca.get_bottom()[1], 0], [-0.2, 2.35, 0], color=GOLD, stroke_width=4)
        drops = [Line([cx, 2.35, 0], [cx, tp + 0.1, 0], color=GOLD, stroke_width=4) for (_, cx, _, _), tp in zip(specs, tops)]
        self.play(Create(stem), Create(bar), run_time=0.5)
        self.play(*[Create(d) for d in drops], run_time=0.6)
        self.at("explains the match best")
        self.play(Indicate(ca, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def seq_row(letters, center, size=0.42, col=GREEN, fs=26):
    blocks = VGroup()
    for k, ch in enumerate(letters):
        r = Square(side_length=size, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.14)
        t = M(ch, fs, col).move_to(r)
        blocks.add(VGroup(r, t))
    blocks.arrange(RIGHT, buff=0.04).move_to(center)
    return blocks


class S05Dna(SpokenScene):
    def construct(self):
        base = "ATCGGATC"
        self.at("second check")
        dn = chip("DNA", GREEN, 38).move_to([-5.2, 3.05, 0])
        self.play(FadeIn(dn, scale=0.9), run_time=0.4)
        self.at("the order of the bases")
        row = seq_row(base, [0.0, 1.55, 0], size=0.72, fs=36)
        sl = T("a DNA sequence: the order of the bases", 28, GREEN).move_to([0, 2.55, 0])
        sk1 = T("sketch: made-up letters, not real DNA", 24, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(sk1), FadeIn(sl), LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in row], lag_ratio=0.12), run_time=1.0)
        self.at("Small changes in")
        row2 = seq_row("ATCGAATC", [0.0, -0.55, 0], size=0.72, fs=36)
        self.play(FadeIn(row2), run_time=0.4)
        self.play(row2[4][0].animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.3), row2[4][1].animate.set_color(YELLOW), run_time=0.5)
        cl = T("a small change", 26, YELLOW).move_to([0, -1.4, 0])
        self.play(FadeIn(cl), run_time=0.3)
        self.at("get passed on")
        ar = arr([0.0, 1.05, 0], [0.0, 0.0, 0], GREY, w=5, tip=0.2)
        po = T("passed on", 26, GREY).move_to([1.4, 0.5, 0])
        self.play(GrowArrow(ar), FadeIn(po), run_time=0.5)
        # tree part
        self.at("split from a common")
        self.play(FadeOut(VGroup(dn, row, sl, row2, cl, ar, po, sk1)), run_time=0.5)
        sk = T("sketch: made-up letters, not real DNA", 22, GREY).move_to([-3.1, 3.2, 0])
        self.play(FadeIn(sk), run_time=0.3)

        tipy = -0.2

        def pair(cx, ynode):
            node = Dot([cx, ynode, 0], radius=0.16, color=GOLD)
            tips = [[cx - 1.2, tipy, 0], [cx + 1.2, tipy, 0]]
            ed = VGroup(*[Line(node.get_center(), t, color=GOLD, stroke_width=4) for t in tips])
            t_dots = VGroup(*[Dot(t, radius=0.12, color=TEXT) for t in tips])
            return node, ed, t_dots

        nA, eA, dA = pair(-3.3, 1.3)
        nB, eB, dB = pair(3.3, 2.7)
        caL = T("common ancestor", 24, GOLD).next_to(nA, UP, buff=0.12)
        caR = T("common ancestor", 24, GOLD).next_to(nB, UP, buff=0.12)
        self.play(FadeIn(nB), FadeIn(caR), run_time=0.3)
        self.play(Create(eB), FadeIn(dB), run_time=0.5)
        bl = T("split long ago", 28, TEXT, weight=BOLD).move_to([3.3, -0.75, 0])
        self.play(FadeIn(bl), run_time=0.2)
        self.at("more recently")
        self.play(FadeIn(nA), FadeIn(caL), Create(eA), FadeIn(dA), run_time=0.5)
        al = T("split more recently", 28, TEXT, weight=BOLD).move_to([-3.3, -0.75, 0])
        self.play(FadeIn(al), run_time=0.2)
        rA = [seq_row("ATCGGATC", [-3.3, -1.5, 0], size=0.42, fs=24), seq_row("ATCGAATC", [-3.3, -1.98, 0], size=0.42, fs=24)]
        rB = [seq_row("ATCGGATC", [3.3, -1.5, 0], size=0.42, fs=24), seq_row("TTCAGCTA", [3.3, -1.98, 0], size=0.42, fs=24)]
        self.at("less time")
        tl = T("less time to collect changes", 24, GREEN).move_to([-3.3, -2.55, 0])
        self.play(FadeIn(VGroup(*rA)), rA[1][4][0].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.3), FadeIn(tl), run_time=0.4)
        self.play(FadeIn(VGroup(*rB)), *[rB[1][i][0].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.3) for i in (0, 3, 5, 7)],
                  FadeIn(T("more time to collect changes", 24, GREEN).move_to([3.3, -2.55, 0])), run_time=0.4)
        self.at("closer relatives")
        ms = T("more similar DNA", 30, GREEN, weight=BOLD).move_to([-3.3, -3.15, 0])
        ls = T("less similar DNA", 30, GREEN, weight=BOLD).move_to([3.3, -3.15, 0])
        self.play(FadeIn(ms, shift=UP * 0.1), FadeIn(ls, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Agree(SpokenScene):
    def construct(self):
        self.at("In science")
        th = chip("theory", TEAL_B, 36).move_to([-4.9, 3.0, 0])
        l1 = T("a well-tested explanation", 28, TEXT)
        l1.move_to([-3.5 + l1.width / 2, 3.3, 0])
        l2 = T("backed by many lines of evidence", 28, TEXT)
        l2.move_to([-3.5 + l2.width / 2, 2.7, 0])
        self.play(FadeIn(th, scale=0.9), run_time=0.4)
        self.at("tested explanation")
        self.play(FadeIn(l1, shift=RIGHT * 0.15), run_time=0.5)
        self.at("many lines of")
        self.play(FadeIn(l2, shift=RIGHT * 0.15), run_time=0.6)
        self.at("It is not")
        gs = chip("a guess", RED, 30).move_to([4.9, 3.0, 0])
        xs = Cross(gs, stroke_color=RED, stroke_width=5).scale(0.9)
        self.play(FadeIn(gs), run_time=0.3)
        self.play(Create(xs), run_time=0.4)
        self.at("The theory of evolution")
        self.play(FadeOut(VGroup(th, l1, l2, gs, xs)), run_time=0.4)
        te = chip("theory of evolution", TEAL_B, 38).move_to([0, 3.1, 0])
        t1 = T("living things change over time", 32, TEXT)
        t2 = T("and share common ancestors", 32, GOLD)
        tt = VGroup(t1, t2).arrange(DOWN, buff=0.12).move_to([0, 1.95, 0])
        self.play(FadeIn(te, scale=0.9), run_time=0.4)
        self.at("change over time")
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.at("share common")
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.5)
        self.at("It predicts")
        cf = chip("fossils", BLUE, 40).move_to([-4.2, 0.2, 0])
        cb = chip("bones", ORANGE, 40).move_to([0, 0.2, 0])
        cd = chip("DNA", GREEN, 40).move_to([4.2, 0.2, 0])
        self.at("that fossils")
        self.play(FadeIn(cf, shift=DOWN * 0.1), run_time=0.4)
        self.at("bones and")
        self.play(FadeIn(cb, shift=DOWN * 0.1), run_time=0.4)
        self.at("will tell", lead=0.5)
        self.play(FadeIn(cd, shift=DOWN * 0.1), run_time=0.4)
        self.at("Each one could")
        qs = []
        for c, col in ((cf, BLUE), (cb, ORANGE), (cd, GREEN)):
            bx = RoundedRectangle(corner_radius=0.12, width=3.2, height=1.0, stroke_color=YELLOW, stroke_width=3,
                                  fill_opacity=0).move_to([c.get_center()[0], -1.55, 0])
            bx = DashedVMobject(bx, num_dashes=30)
            q = T("a different story?", 24, YELLOW).move_to([c.get_center()[0], -1.55, 0])
            a = arr([c.get_center()[0], c.get_bottom()[1] - 0.1, 0], [c.get_center()[0], -1.0, 0], col, w=5, tip=0.2)
            qs.append(VGroup(bx, q, a))
        self.play(*[FadeIn(q) for q in qs], run_time=0.8)
        self.at("Instead, they agree")
        gold = chip("the same family story", GOLD, 38).move_to([0, -2.25, 0])
        arrs = [arr([c.get_center()[0] * 0.9, c.get_bottom()[1] - 0.1, 0], [c.get_center()[0] * 0.28, gold.get_top()[1] + 0.08, 0], col, w=5, tip=0.2)
                for c, col in ((cf, BLUE), (cb, ORANGE), (cd, GREEN))]
        self.play(*[FadeOut(q) for q in qs], run_time=0.4)
        self.play(*[GrowArrow(a) for a in arrs], FadeIn(gold, scale=0.9), run_time=0.8)
        self.at("how scientists know")
        ans = T("Three kinds of evidence agree.", 36, TEXT, weight=BOLD).move_to([0, -3.3, 0])
        self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Fossils, bones and DNA tell the same family story."
