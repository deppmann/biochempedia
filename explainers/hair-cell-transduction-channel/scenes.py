"""What counts as proof of a channel  (Biochemistrypedia explainer, Sensory Systems)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the candidate protein, TMC1 (a labelled schematic block, never a structure)
  TEAL   = partner proteins (TMIE, LHFPL5, CIB2) and "a partner"
  PURPLE = the other things that could be needed (trafficking factor, anchor, enzyme)
  YELLOW = ions and the current they carry (the meter fill, the calcium dots)
  TEXT   = other ions, and what the experimenter does (chips: gene removed, gene back)
  ORANGE = the cysteine-reactive reagent
  PINK   = an engineered or altered residue (a small badge on the channel block)
  GREEN  = what an experiment shows
  RED    = what an experiment cannot show / leaves open
  GREY   = membranes, outlines, rods, the ladder when not in use
  GOLD   = title rule only
Everything is a labelled schematic; the meters are "in this sketch" and carry no numbers.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F2789F"

LX = -4.3                     # ladder centre x
RUNGS = ["Localization", "Requirement", "Rescue", "Permeation", "Accessibility", "Purified"]
RUNG_Y = [-2.75 + 1.1 * i for i in range(6)]
STX = 2.65                    # stage centre x (right of the ladder)
MX = 2.6                      # channel x in the membrane scenes


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def rung(name, w=2.7, size=22):
    lab = T(name, size, GREY)
    h = lab.height + 0.34
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                           fill_color=GREY, fill_opacity=0.16)
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(back, box, lab.move_to(box))


def rstate(r, st):
    """animations that set a rung to 'dim', 'seen' or 'on'."""
    if st == "dim":
        return [r[1].animate.set_stroke(GREY, opacity=0.35).set_fill(GREY, 0.05), r[2].animate.set_color(GREY).set_opacity(0.45)]
    if st == "seen":
        return [r[1].animate.set_stroke(GREY, opacity=1).set_fill(GREY, 0.16), r[2].animate.set_color(TEXT).set_opacity(0.9)]
    return [r[1].animate.set_stroke(BLUE, opacity=1).set_fill(BLUE, 0.3), r[2].animate.set_color(BLUE).set_opacity(1)]


def make_ladder():
    rails = VGroup(*[Line([LX + sx * 1.6, -3.3, 0], [LX + sx * 1.6, 3.3, 0], color=GREY, stroke_width=6) for sx in (-1, 1)])
    rs = [rung(n).move_to([LX, y, 0]) for n, y in zip(RUNGS, RUNG_Y)]
    return rails, rs


def static_ladder(states):
    """the ladder drawn in place at the start of a scene; states = list of 'dim'/'seen'/'on'."""
    rails, rs = make_ladder()
    for r, st in zip(rs, states):
        if st == "dim":
            r[1].set_stroke(GREY, opacity=0.35).set_fill(GREY, 0.05); r[2].set_color(GREY).set_opacity(0.45)
        elif st == "seen":
            r[2].set_color(TEXT).set_opacity(0.9)
        else:
            r[1].set_stroke(BLUE).set_fill(BLUE, 0.3); r[2].set_color(BLUE)
    return rails, rs


def header(text, y=3.15, x=STX):
    return T(text, 22, GREY).move_to([x, y, 0])


def sc_lines(shows, cannot, y=-2.85, x0=-0.95):
    a = T("shows: " + shows, 22, GREEN)
    b = T("cannot show: " + cannot, 22, RED)
    a.move_to([x0, y, 0], aligned_edge=LEFT)
    b.move_to([x0, y - 0.5, 0], aligned_edge=LEFT)
    return a, b


def fchip(text, color=TEXT, size=24, pad=0.2):
    c = chip(text, color, size=size, pad=pad)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def hair_cell(c, s):
    """a labelled hair-cell sketch: cell body, three rods (stereocilia), one tip link, the candidate dot at
    the lower end of the tip link.  c = centre of the body, s = scale."""
    P = lambda dx, dy: np.array([c[0] + s * dx, c[1] + s * dy, 0.0])
    body = RoundedRectangle(corner_radius=0.35 * s, width=3.4 * s, height=1.4 * s, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.15).move_to(c)
    rods = []
    for x, h in zip((-0.9, 0.0, 0.9), (1.3, 2.0, 2.7)):
        rods.append(RoundedRectangle(corner_radius=0.1 * s, width=0.26 * s, height=h * s, stroke_color=GREY, stroke_width=4,
                                     fill_color=GREY, fill_opacity=0.15).move_to(P(x, 0.7 + h / 2)))
    link = Line(P(-0.9, 2.0), P(-0.13, 2.62), color=TEXT, stroke_width=3)
    dot = Circle(radius=0.14 * s, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=1).move_to(P(-0.9, 1.97))
    cell = VGroup(*rods, body)
    return cell, link, dot, P


def meter(label, cx, cy, frac=1.0, w=4.0, size=24):
    lab = T(label, size, TEXT).move_to([cx, cy + 0.5, 0])
    out = Rectangle(width=w, height=0.46, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, cy, 0])
    fill = meter_fill(cx, cy, frac, w)
    return VGroup(lab, out, fill)


def meter_fill(cx, cy, frac, w=4.0):
    ww = max(w * frac - 0.1, 0.02)
    r = Rectangle(width=ww, height=0.36, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9 if frac > 0 else 0.0)
    r.move_to([cx - w / 2 + 0.05 + ww / 2, cy, 0])
    return r


def membrane(y=0.0, x0=-1.0, x1=6.2, mx=MX, gap=0.9, h=0.7):
    left = Rectangle(width=(mx - gap) - x0, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
    left.move_to([(x0 + mx - gap) / 2, y, 0])
    right = Rectangle(width=x1 - (mx + gap), height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
    right.move_to([(x1 + mx + gap) / 2, y, 0])
    return VGroup(left, right)


def channel_block(y=0.0, mx=MX, color=BLUE, hh=1.3):
    l = RoundedRectangle(corner_radius=0.08, width=0.55, height=hh, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.4).move_to([mx - 0.65, y, 0])
    r = RoundedRectangle(corner_radius=0.08, width=0.55, height=hh, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.4).move_to([mx + 0.65, y, 0])
    return VGroup(l, r)


def ion(kind, x, y):
    if kind == "ca":
        return Circle(radius=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, y, 0])
    return Circle(radius=0.14, stroke_width=0, fill_color=TEXT, fill_opacity=0.9).move_to([x, y, 0])


def ion_path(d, passes, k, mx=MX, y=0.0):
    p0 = d.get_center()
    if passes:
        pts = [p0, np.array([mx, y + 0.95, 0]), np.array([mx, y, 0]),
               np.array([mx + (p0[0] - mx) * 0.8, y - 1.3 - 0.22 * (k % 3), 0])]
    else:
        pts = [p0, np.array([mx + (p0[0] - mx) * 0.35, y + 0.95, 0]), p0 + UP * 0.45]
    return VMobject().set_points_as_corners(pts)


def flow(sc, specs, rt=2.2, y=0.0, y_top=1.5):
    """specs = list of (kind, x_offset, passes).  Dots appear above the membrane, then run (or are turned back)."""
    dots = []
    for i, (k, dx, ok) in enumerate(specs):
        dots.append(ion(k, MX + dx, y_top + 0.3 * (i % 3)))
    sc.play(*[FadeIn(d, scale=0.6) for d in dots], run_time=0.3)
    sc.play(LaggedStart(*[MoveAlongPath(d, ion_path(d, s[2], i, y=y), rate_func=linear)
                          for i, (d, s) in enumerate(zip(dots, specs))], lag_ratio=0.2), run_time=rt)
    sc.play(*[FadeOut(d) for d in dots], run_time=0.3)


def legend(y=-2.4, x0=-0.95, cys=False):
    a = ion("ca", x0 + 0.14, y); la = T("calcium", 22, YELLOW).next_to(a, RIGHT, buff=0.2)
    b = ion("o", x0 + 2.2, y); lb = T("other ions", 22, TEXT).next_to(b, RIGHT, buff=0.2)
    g = VGroup(a, la, b, lb)
    if cys:
        c = Circle(radius=0.17, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to([x0 + 4.9, y, 0])
        cl = T("C", 20, BG, weight=BOLD).move_to(c)
        lc = T("cysteine", 22, PINK).next_to(c, RIGHT, buff=0.2)
        g.add(c, cl, lc)
    return g


NORMAL = [("ca", -0.8, True), ("o", -0.4, True), ("ca", 0.0, True), ("o", 0.4, True), ("ca", 0.8, True), ("o", 0.0, True)]
REDUCED = [("ca", -0.8, False), ("o", -0.4, True), ("ca", 0.0, True), ("o", 0.4, True), ("ca", 0.8, False), ("o", 0.0, True)]
FEW = [("ca", -0.8, False), ("o", -0.4, True), ("ca", 0.0, False), ("o", 0.4, False), ("ca", 0.8, False), ("o", 0.0, False)]


class S00Title(TitleCard):
    LESSON = "The Hair Cell's Transduction Channel"
    TITLE = "What Counts as Proof of a Channel"


# ---------------------------------------------------------------------------------------------
class S01Gene(SpokenScene):
    """gene missing -> current meter empties; the protein is in the right place; the question; three other things."""

    def construct(self):
        s = 1.3
        cell, link, dot, P = hair_cell(np.array([-2.7, -1.75, 0]), s)
        lab_cell = T("hair cell", 26, GREY).move_to(cell[-1])
        lab_link = T("tip link", 24, TEXT).move_to(P(-1.95, 2.6))
        lead_link = Line(lab_link.get_right() + RIGHT * 0.05, P(-0.55, 2.33), color=GREY, stroke_width=2)
        lab_prot = T("protein", 24, BLUE).move_to(P(-2.0, 1.35))
        lead_prot = Line(lab_prot.get_right() + RIGHT * 0.05, dot.get_center() + LEFT * 0.17, color=GREY, stroke_width=2)

        m = meter("conventional current", 3.3, 1.8, 1.0)
        sk = T("in this sketch", 22, GREY).move_to([3.3, 1.1, 0])
        self.at("hair cell")
        self.play(FadeIn(cell), FadeIn(lab_cell), run_time=0.4)
        self.play(Create(link), FadeIn(lab_link), Create(lead_link), run_time=0.4)
        self.play(FadeIn(m), FadeIn(sk), run_time=0.3)

        gone = fchip("gene removed", TEXT, 24).move_to([3.3, 0.4, 0])
        self.at("gene is missing")
        self.play(FadeIn(gone, shift=DOWN * 0.1), Transform(m[2], meter_fill(3.3, 1.8, 0.0)), run_time=0.8)

        self.at("right place")
        self.play(FadeIn(dot, scale=0.5), FadeIn(lab_prot), Create(lead_prot), run_time=0.4)
        self.play(Indicate(dot, color=BLUE, scale_factor=1.6), run_time=0.5)

        q = T("Is the protein the channel?", 36, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.at("Is that enough")
        self.play(Write(q), run_time=1.0)

        self.at("required for a current")
        self.play(Indicate(m[1], color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("forming the pore")
        self.play(Indicate(dot, color=BLUE, scale_factor=1.6), run_time=0.7)

        s1 = fchip("trafficking factor", PURPLE, 24).move_to([3.4, -0.5, 0])
        s2 = fchip("anchor", PURPLE, 24).move_to([3.4, -1.4, 0])
        s3 = fchip("lipid-modifying enzyme", PURPLE, 24).move_to([3.4, -2.3, 0])
        need = T("could all be needed", 22, PURPLE).move_to([3.4, -3.1, 0])
        self.at("trafficking factor")
        self.play(FadeIn(s1, shift=LEFT * 0.2), run_time=0.5)
        self.at("anchor")
        self.play(FadeIn(s2, shift=LEFT * 0.2), run_time=0.5)
        self.at("lipid")
        self.play(FadeIn(s3, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(need), run_time=0.4)

        any1 = fchip("any one removed", TEXT, 24).move_to([3.3, 0.4, 0])
        self.at("Deleting any")
        self.play(Transform(gone, any1), run_time=0.6)
        self.at("silence the cell")
        self.play(Indicate(VGroup(s1, s2, s3), color=PURPLE, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ladder(SpokenScene):
    """the ladder of evidence; localization; requirement and rescue on the current meter."""

    def construct(self):
        rails, rs = make_ladder()
        for r in rs:
            r[1].set_stroke(GREY, opacity=0.35).set_fill(GREY, 0.05); r[2].set_color(GREY).set_opacity(0.45)
        self.play(Create(rails), run_time=0.6)
        self.at("ladder of evidence")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rs], lag_ratio=0.15), run_time=1.0)

        self.at("rules out")
        self.play(LaggedStart(*[Indicate(r[1], color=TEXT, scale_factor=1.05) for r in rs], lag_ratio=0.2), run_time=1.3)
        hd = header("in neonatal mouse hair cells", y=3.4)
        cell, link, dot, P = hair_cell(np.array([0.5, -1.15, 0]), 1.0)
        lab_prot = T("protein", 22, BLUE).move_to(P(-2.0, 1.4))
        lead_prot = Line(lab_prot.get_right() + RIGHT * 0.05, dot.get_center() + LEFT * 0.15, color=GREY, stroke_width=2)
        lab_link = T("tip link", 22, TEXT).move_to(P(-0.1, 3.55))
        lead_link = Line(lab_link.get_bottom() + DOWN * 0.03, P(-0.5, 2.3), color=GREY, stroke_width=2)

        self.at("first rung")
        self.play(*rstate(rs[0], "on"), FadeIn(cell), Create(link), FadeIn(dot), run_time=0.7)
        self.at("lower end")
        self.play(FadeIn(lab_prot), Create(lead_prot), FadeIn(lab_link), Create(lead_link), run_time=0.5)
        self.play(Indicate(dot, color=BLUE, scale_factor=1.8), run_time=0.7)

        m = meter("conventional current", 4.5, 1.7, 1.0, w=3.4, size=22)
        sk = T("in this sketch", 22, GREY).move_to([4.5, 0.15, 0])
        self.at("requirement")
        self.play(*rstate(rs[0], "seen"), *rstate(rs[1], "on"), FadeIn(hd), FadeIn(m), FadeIn(sk), run_time=0.6)
        self.at("rescue")
        self.play(*rstate(rs[1], "seen"), *rstate(rs[2], "on"), run_time=0.4)
        gone = fchip("both genes removed", TEXT, 22).move_to([4.5, 0.75, 0])
        self.at("lacking both")
        self.play(FadeIn(gone, shift=DOWN * 0.1), Transform(m[2], meter_fill(4.5, 1.7, 0.0, w=3.4)), run_time=0.5)
        self.at("is gone")
        self.play(Indicate(m[1], color=GREY, scale_factor=1.05), run_time=0.6)
        back = fchip("either gene back", TEXT, 22).move_to([4.5, 0.75, 0])
        self.at("either gene back")
        self.play(Transform(gone, back), Transform(m[2], meter_fill(4.5, 1.7, 1.0, w=3.4)), run_time=0.9)

        a, b = sc_lines("the proteins are in the pathway", "pore versus a needed factor", y=-2.95)
        self.at("pathway")
        self.play(FadeIn(a), run_time=0.5)
        self.at("does not separate")
        self.play(FadeIn(b), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Permeation(SpokenScene):
    """a changed residue: calcium crosses less; single-channel current is smaller; a partner could do the same."""

    def construct(self):
        rails, rs = static_ladder(["seen", "seen", "seen", "dim", "dim", "dim"])
        self.add(rails, *rs)
        hd = header("excised neonatal mouse inner hair cells", y=3.4)
        mem = membrane()
        ch = channel_block()
        lab = T("TMC1", 22, BLUE).move_to([0.2, -1.0, 0])
        lead = Line([0.75, -0.92, 0], [MX - 0.75, -0.66, 0], color=GREY, stroke_width=2)
        leg = legend(y=-2.4)
        self.at("changes the protein")
        self.play(*rstate(rs[2], "seen"), *rstate(rs[3], "on"), FadeIn(hd), FadeIn(mem), FadeIn(ch), FadeIn(lab), Create(lead),
                  run_time=0.7)
        comp = T("comparison cells", 22, GREY).move_to([-1.0, 1.1, 0], aligned_edge=LEFT)
        self.play(FadeIn(leg), FadeIn(comp), run_time=0.4)
        flow(self, NORMAL, rt=1.6)

        badge = Circle(radius=0.2, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to([MX - 0.65, 0.78, 0])
        blab = T("one residue\nchanged", 22, PINK).move_to([-1.0, 1.15, 0], aligned_edge=LEFT)
        blead = Line([0.95, 1.0, 0], [MX - 0.85, 0.82, 0], color=GREY, stroke_width=2)
        self.at("altered residue")
        self.play(FadeOut(comp), FadeIn(badge, scale=0.4), FadeIn(blab), Create(blead), run_time=0.5)

        self.at("inner hair cells")
        self.play(Indicate(badge, color=PINK, scale_factor=1.5), run_time=0.8)
        self.at("calcium permeability")
        flow(self, REDUCED, rt=1.6)

        bar = meter("single channel\ncurrent", 5.0, 1.55, 1.0, w=2.4, size=22)
        bar[0].move_to([5.0, 2.45, 0])
        inside = T("comparison", 22, BG, weight=BOLD).move_to([5.0, 1.55, 0])
        sk = T("in this sketch", 22, GREY).move_to([5.0, 0.95, 0])
        self.at("Single channel")
        self.play(FadeIn(bar), FadeIn(inside), FadeIn(sk), run_time=0.5)
        inside2 = T("altered", 22, BG, weight=BOLD).move_to([3.8 + 0.05 + (2.4 * 0.55 - 0.1) / 2, 1.55, 0])
        self.at("smaller")
        self.play(Transform(bar[2], meter_fill(5.0, 1.55, 0.55, w=2.4)), Transform(inside, inside2), run_time=0.8)

        a, b = sc_lines("the sequence changes which ions pass", "a partner could do the same", y=-2.95)
        self.at("which ions pass")
        self.play(FadeIn(a), run_time=0.5)
        partner = fchip("partner", TEAL, 22).move_to([5.0, -1.0, 0])
        pl = Line([MX + 0.95, -0.55, 0], partner.get_left(), color=GREY, stroke_width=2)
        self.at("a partner")
        self.play(FadeIn(partner, shift=UP * 0.2), Create(pl), run_time=0.5)
        self.play(Indicate(partner[1:], color=TEAL), run_time=0.6)
        self.play(FadeIn(b), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Access(SpokenScene):
    """current already flowing; the reagent arrives outside and reacts with the engineered cysteine."""

    def construct(self):
        YM = -0.3
        rails, rs = static_ladder(["seen", "seen", "seen", "seen", "dim", "dim"])
        self.add(rails, *rs)
        hd = header("mouse hair cells lacking both TMC1 and TMC2", y=3.4)
        mem = membrane(y=YM)
        tl = T("TMC1", 22, BLUE).move_to([3.55, YM - 1.05, 0])
        tll = Line([3.45, YM - 0.9, 0], [MX + 0.75, YM - 0.68, 0], color=GREY, stroke_width=2)
        ch = channel_block(y=YM)
        badge = Circle(radius=0.22, stroke_width=0, fill_color=PINK, fill_opacity=1).move_to([MX + 0.65, YM + 0.82, 0])
        blab = T("C", 22, BG, weight=BOLD).move_to(badge)
        cys = VGroup(badge, blab)
        leg = legend(y=-2.4, cys=True)

        self.at("accessibility test")
        self.play(*rstate(rs[3], "seen"), *rstate(rs[4], "on"), FadeIn(hd), run_time=0.5)
        self.play(FadeIn(mem), FadeIn(ch), FadeIn(tl), Create(tll), run_time=0.5)

        st1 = fchip("1  current present", GREEN, 22).move_to([0.6, 2.7, 0])
        st2 = fchip("2  reagent added", ORANGE, 22).move_to([4.6, 2.7, 0])
        stp = Arrow(st1.get_right(), st2.get_left(), buff=0.12, color=GREY, stroke_width=4, tip_length=0.2)
        self.at("already carry current")
        self.play(FadeIn(st1), FadeIn(leg), run_time=0.4)
        flow(self, NORMAL, rt=1.5, y=YM, y_top=1.15)

        while self.t_of("substitution") - 0.2 - self.elapsed() > 2.6:
            flow(self, NORMAL, rt=1.5, y=YM, y_top=1.15)
        self.at("substitution")
        self.play(FadeIn(cys, scale=0.4), run_time=0.4)

        rg = fchip("reagent", ORANGE, 24).move_to([5.0, 1.65, 0])
        rg_note = T("cannot cross the membrane", 22, ORANGE).move_to([4.9, 1.15, 0])
        self.at("cannot cross the membrane")
        self.play(FadeIn(st2), GrowArrow(stp), FadeIn(rg, shift=DOWN * 0.2), FadeIn(rg_note), run_time=0.8)

        self.at("reacts")
        self.play(FadeOut(rg_note), rg.animate.move_to([5.0, 0.95, 0]), run_time=0.6)
        link = Line([5.0 - rg[1].width / 2, 0.95, 0], badge.get_center() + RIGHT * 0.22 + UP * 0.1, color=ORANGE, stroke_width=4)
        self.play(Create(link), Indicate(badge, color=ORANGE, scale_factor=1.6), run_time=0.6)

        self.at("changed the permeation")
        flow(self, FEW, rt=1.4, y=YM, y_top=1.15)
        chg = T("permeation\nchanged", 22, ORANGE).move_to([0.2, YM - 1.0, 0])
        self.play(FadeIn(chg), run_time=0.3)

        a, b = sc_lines("not altered synthesis or delivery", "the protein without its partners", y=-2.95)
        self.at("existed before")
        self.play(Indicate(st1[1:], color=GREEN, scale_factor=1.08), run_time=0.6)
        self.at("synthesis or delivery")
        self.play(FadeIn(a), run_time=0.4)
        part = fchip("native partners", TEAL, 22).move_to([5.0, YM - 1.0, 0])
        pl = Line(part.get_left(), [MX + 0.95, YM - 0.5, 0], color=GREY, stroke_width=2)
        self.at("native partners")
        self.play(FadeIn(part, shift=UP * 0.2), Create(pl), run_time=0.5)
        self.play(FadeIn(b), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Complex(SpokenScene):
    """purified protein in a liposome responds to pressure; then the complex, and transduction without TMIE."""

    def construct(self):
        rails, rs = static_ladder(["seen", "seen", "seen", "seen", "seen", "dim"])
        self.add(rails, *rs)
        hd = header("purified and reconstituted: no hair cell", y=3.4)
        cx, cy, R = 0.9, -0.2, 1.7
        ring = Circle(radius=R, stroke_color=GREY, stroke_width=8, fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])
        ch = channel_block(y=cy + R, mx=cx, hh=1.2)
        lab_l = T("liposome", 26, GREY).move_to([cx, cy, 0])
        lab_p = T("truncated turtle TMC1", 22, BLUE).move_to([2.45, 2.15, 0], aligned_edge=LEFT)
        lead_p = Line([2.4, 2.1, 0], [cx + 0.95, cy + R + 0.2, 0], color=GREY, stroke_width=2)
        self.at("Purified truncated")
        self.play(*rstate(rs[4], "seen"), *rstate(rs[5], "on"), FadeIn(hd), run_time=0.5)
        self.play(Create(ring), FadeIn(lab_l), run_time=0.7)
        self.at("liposomes")
        self.play(FadeIn(ch, scale=0.5), run_time=0.5)
        self.play(FadeIn(lab_p), Create(lead_p), run_time=0.4)
        m = meter("channel activity", 4.55, 0.6, 0.0, w=3.0, size=22)
        angs = (np.pi * 0.8, np.pi, np.pi * 1.2, np.pi * 1.4, np.pi * 1.6)
        arrs = VGroup(*[Arrow(np.array([cx + (R + 0.75) * np.cos(a), cy + (R + 0.75) * np.sin(a), 0]),
                              np.array([cx + (R + 0.3) * np.cos(a), cy + (R + 0.3) * np.sin(a), 0]),
                              buff=0, color=TEXT, stroke_width=5, tip_length=0.2) for a in angs])
        pr = T("applied pressure", 22, TEXT).move_to([cx, cy - R - 1.0, 0])
        self.at("applied pressure")
        self.play(FadeIn(m), FadeIn(arrs), FadeIn(pr), run_time=0.5)
        self.play(Transform(m[2], meter_fill(4.55, 0.6, 0.8, w=3.0)), ring.animate.scale(0.94), run_time=0.8)
        self.play(ring.animate.scale(1 / 0.94), run_time=0.3)
        nm = T("not mammalian,\nnot a native complex", 22, RED).move_to([4.55, -1.5, 0])
        self.at("not mammalian")
        self.play(FadeIn(nm), run_time=0.5)

        # --- the complex ------------------------------------------------------------------
        self.at("complex of proteins")
        self.play(FadeOut(VGroup(ring, ch, lab_l, lab_p, lead_p, m, arrs, pr, nm)), run_time=0.5)
        row = [fchip("TMIE", TEAL, 26), fchip("TMC1", BLUE, 26), fchip("LHFPL5", TEAL, 26), fchip("CIB2", TEAL, 26)]
        grp = VGroup(*row).arrange(RIGHT, buff=0.3).move_to([STX + 0.1, 1.0, 0])
        box = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=grp.width + 0.6, height=grp.height + 0.7, stroke_color=GREY,
                                              stroke_width=3).move_to(grp), num_dashes=50)
        cl = T("proposed partners", 24, GREY).next_to(box, DOWN, buff=0.15)
        hd2 = header("mouse cochlear outer hair cells", y=3.4)
        self.play(Transform(hd, hd2), run_time=0.01)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in row], lag_ratio=0.25), Create(box), FadeIn(cl), run_time=1.2)

        m2 = meter("transduction", STX + 0.1, -1.5, 1.0, w=4.0, size=24)
        sk = T("in this sketch", 22, GREY).move_to([STX + 0.1, -2.3, 0])
        self.at("support transduction")
        self.play(FadeIn(m2), FadeIn(sk), run_time=0.4)
        self.play(row[0].animate.shift(UP * 1.5), run_time=0.7)
        wo = T("without TMIE", 22, TEAL).next_to(row[0], RIGHT, buff=0.3)
        self.play(FadeIn(wo), Transform(m2[2], meter_fill(STX + 0.1, -1.5, 0.0, w=4.0)), run_time=0.6)
        self.at("partners")
        self.play(Indicate(VGroup(row[2][1:], row[3][1:]), color=TEAL, scale_factor=1.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the whole ladder, each rung with what it leaves open; force coupling is still a question."""

    OPEN = ["that it conducts", "that it is the pore", "pore identity", "a partner could change it",
            "the protein without partners", "the native complex, force coupling"]

    def construct(self):
        rails, rs = static_ladder(["seen", "seen", "seen", "seen", "seen", "on"])
        self.add(rails, *rs)
        self.at("No single paper")
        self.play(*rstate(rs[5], "seen"), run_time=0.3)

        lo = T("what each rung leaves open", 24, RED).move_to([-2.45, 3.3, 0], aligned_edge=LEFT)
        ro = [T(self.OPEN[i], 24, RED).move_to([-2.45, RUNG_Y[i], 0], aligned_edge=LEFT) for i in range(6)]
        self.at("every rung")
        self.play(FadeOut(rails), FadeIn(lo), LaggedStart(*[FadeIn(ro[i], shift=RIGHT * 0.15) for i in range(5, -1, -1)],
                                                         lag_ratio=0.2), run_time=1.8)

        tl = fchip("tip link", TEXT, 24).move_to([5.1, 1.2, 0])
        pore = fchip("pore", BLUE, 24).move_to([5.1, -0.9, 0])
        ar = Arrow(tl.get_bottom(), pore.get_top(), buff=0.1, color=GREY, stroke_width=4, tip_length=0.2)
        qm = T("?", 40, RED, weight=BOLD).next_to(ar, RIGHT, buff=0.15)
        qt = T("how does force\nreach it?", 22, RED).move_to([5.1, -2.1, 0])
        self.at("complete ladder")
        self.play(LaggedStart(*[Indicate(ro[i], color=RED, scale_factor=1.05) for i in range(5, -1, -1)], lag_ratio=0.2), run_time=1.6)
        self.at("tip link reaches")
        self.play(FadeIn(tl), GrowArrow(ar), FadeIn(pore), FadeIn(qm), run_time=0.8)
        self.play(FadeIn(qt), run_time=0.4)

        self.at("ruled out")
        self.play(LaggedStart(*[Indicate(rs[i][1], color=BLUE, scale_factor=1.06) for i in range(6)], lag_ratio=0.15), run_time=1.4)
        self.at("leaves open")
        self.play(Indicate(lo, color=RED, scale_factor=1.1), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Ask what each experiment ruled out, and what it left open."
