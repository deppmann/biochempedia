"""Drugs against a part: read the escape, design the next drug  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the kinase (body) and, in the grid, every kinase
  GOLD   = ATP and the phosphate it carries
  PINK   = a drug (solid wedge: capsule, imatinib, ponatinib)
  YELLOW = residue 315 and the contact it makes (the thing that changes)
  TEAL   = people and cells (patients, leukaemia cell, normal cell, blood)
  GREEN  = on / working / gets through
  RED    = off / blocked / does not get through
  GREY   = the pocket, DNA, labels

No molecular structures: a kinase is a rounded block with a pocket cut in it, a drug is a labelled wedge,
a residue is a small labelled block, ATP is a chip, a phosphate is a "P" badge, DNA is a row of letters.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#F08BB4"

POCKET = [(-2, 0.9), (2, 0.9), (2, -0.3), (0, -1.4), (-2, -0.3)]


def V(x, y):
    return np.array([x, y, 0.0])


class Kin(VGroup):
    """a kinase: a rounded block with a pocket in the top. k scales everything; pc is the pocket centre."""

    def __init__(self, cx, cy, k, stroke=BLUE):
        sw = max(1.2, 3 * k ** 0.5)
        bw, bh = 7.4 * k, 4.6 * k
        body = RoundedRectangle(corner_radius=0.9 * k, width=bw, height=bh, stroke_color=stroke, stroke_width=sw,
                                fill_color=BLUE, fill_opacity=0.14).move_to(V(cx, cy))
        pc = V(cx, cy + 0.16 * bh)
        pocket = Polygon(*[pc + k * V(x, y) for x, y in POCKET], stroke_color=GREY, stroke_width=max(1, sw - 1),
                         fill_color=BG, fill_opacity=1)
        super().__init__(body, pocket)
        self.body, self.pocket, self.pc, self.k = body, pocket, pc, k


def wedge(pc, k, hw=1.5, xo=0.0, yo=0.0):
    pts = [(-hw, 0.8), (hw, 0.8), (hw, -0.2), (0, -1.2), (-hw, -0.2)]
    return Polygon(*[pc + k * V(x + xo, y + yo) for x, y in pts], stroke_color=PINK, stroke_width=max(1, 2.5 * k ** 0.5),
                   fill_color=PINK, fill_opacity=0.92)


def wlabel(text, pc, k, xo=0.0, yo=0.0, size=24):
    return T(text, size, BG, weight=BOLD).move_to(pc + k * V(xo, 0.3 + yo))


def atp_chip(pc, k, xo=0.0, yo=0.0):
    return chip("ATP", GOLD, size=22, pad=0.12, fill_opacity=0.25).move_to(pc + k * V(xo, 0.15 + yo))


def pbadge(r=0.18):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", int(r * 120), BG, weight=BOLD).move_to(c))


def bump_of(pc, k, big=True):
    """residue 315: a small knob on the pocket wall (threonine) or a bulky block (isoleucine)."""
    if big:
        return RoundedRectangle(corner_radius=0.08, width=1.3 * k, height=0.7 * k, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.9).move_to(pc + k * V(-1.35, 0.5))
    return RoundedRectangle(corner_radius=0.06, width=0.4 * k, height=0.5 * k, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.9).move_to(pc + k * V(-1.85, 0.5))


def state(text, color, y):
    return T(text, 28, color, weight=BOLD).move_to(V(0, y))


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Drugs Against a Part"
    TITLE = "Read the Escape, Design the Next Drug"


# ---------------------------------------------------------------------------------------------
class S01Pocket(SpokenScene):
    """one kinase, a capsule aimed at it; then five hundred kinases with the same pocket."""

    def construct(self):
        K = Kin(0, -0.35, 1.0)
        pc, k = K.pc, K.k
        year = T("2001", 30, GREY).move_to(V(-5.2, 3.0))
        self.play(FadeIn(K), run_time=0.6)
        w = wedge(pc, k, yo=1.8)
        wl = wlabel("capsule", pc, k, yo=1.8)
        self.at("capsule was approved")
        self.play(FadeIn(year), FadeIn(w, shift=DOWN * 0.2), FadeIn(wl, shift=DOWN * 0.2), run_time=0.6)
        one = T("one enzyme", 28, TEXT).move_to(V(0, -3.15))
        self.at("aimed at one enzyme")
        self.play(w.animate.shift(DOWN * 1.8 * k), wl.animate.shift(DOWN * 1.8 * k), FadeIn(one), run_time=0.9)

        # the grid: 9 x 5 identical kinases, the first one turns into the middle one
        cells = {}
        for r in range(5):
            for c in range(9):
                cells[(r, c)] = Kin((c - 4) * 1.3, -0.35 + (2 - r) * 0.9, 0.17)
        mid = cells[(2, 4)]
        ws = wedge(mid.pc, mid.k)
        count = T("about 500 human kinases", 32, TEXT).move_to(V(0, 2.75))
        others = [v for kk, v in cells.items() if kk != (2, 4)]
        self.at("human kinases")
        self.play(ReplacementTransform(K, mid), ReplacementTransform(w, ws), FadeOut(wl), FadeOut(one),
                  FadeOut(year),
                  LaggedStart(*[FadeIn(o) for o in others], lag_ratio=0.03, run_time=1.4), FadeIn(count),
                  run_time=1.6)

        dots = {}
        for kk, v in cells.items():
            if kk == (2, 4):
                continue
            dots[kk] = Circle(radius=0.08, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(v.pc + v.k * V(0, 0.15))
        self.at("hold")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots.values()], lag_ratio=0.02, run_time=0.9))
        same = T("the same ATP pocket", 28, GOLD).move_to(V(0, -3.05))
        self.at("nearly the same pocket")
        self.play(FadeIn(same), run_time=0.4)

        hops = [Circle(radius=0.08, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(d.get_center()) for d in dots.values()]
        self.at("moves a phosphate")
        self.add(*hops)
        self.play(LaggedStart(*[h.animate.shift(UP * 0.5).set_opacity(0) for h in hops], lag_ratio=0.02, run_time=1.0))
        self.remove(*hops)

        spread = [(0, 0), (0, 3), (0, 6), (1, 1), (1, 5), (1, 8), (2, 1), (2, 7), (3, 2), (3, 5), (4, 0), (4, 4), (4, 8)]
        wedges = [wedge(cells[s].pc, cells[s].k) for s in spread]
        self.at("jam one pocket")
        self.play(Indicate(ws, color=TEXT, scale_factor=1.5), run_time=0.7)
        self.at("jam dozens")
        self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in wedges], lag_ratio=0.08, run_time=1.2))

        ask = T("how do you drug just one?", 32, YELLOW).move_to(V(0, 2.75))
        ring = SurroundingRectangle(mid, color=YELLOW, buff=0.1, stroke_width=4)
        self.at("how do you drug")
        self.play(FadeOut(count), FadeOut(same), *[FadeOut(x) for x in wedges + [ws]], run_time=0.6)
        self.play(FadeIn(ask), Create(ring), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Imatinib(SpokenScene):
    """the short list, BCR-ABL, imatinib in the ATP pocket, and who gets through."""

    def construct(self):
        # start from the grid of scene one, rebuilt in place
        cells = {}
        for r in range(5):
            for c in range(9):
                cells[(r, c)] = Kin((c - 4) * 1.3, -0.35 + (2 - r) * 0.9, 0.17)
        grid = VGroup(*cells.values())
        self.add(grid)

        # the list: 5 x 4 small kinases, top right
        mini = {}
        for r in range(4):
            for c in range(5):
                mini[(r, c)] = Kin(1.5 + c * 1.0, 2.9 - r * 0.78, 0.14)
        minig = VGroup(*mini.values())
        K = Kin(-3.4, -0.55, 0.8)
        pc, k = K.pc, K.k
        bcr = T("BCR-ABL", 30, TEXT, weight=BOLD).move_to(V(-3.4, -1.95))
        atp = atp_chip(pc, k)
        w = wedge(pc, k, yo=2.2)
        wl = wlabel("imatinib", pc, k, yo=2.2)
        self.wait(0.3)
        self.play(ReplacementTransform(grid, minig), FadeIn(K), FadeIn(atp), run_time=1.3)
        self.at("called imatinib")
        self.play(FadeIn(w, shift=DOWN * 0.2), FadeIn(wl, shift=DOWN * 0.2), run_time=0.5)
        lit = [(1, 3), (3, 0)]   # the PDGF receptor and KIT; the large kinase is ABL (as BCR-ABL)
        short = T("a short list, not hundreds", 26, PINK).move_to(V(3.5, -0.05))
        self.at("short list")
        self.play(*[mini[i].body.animate.set_stroke(PINK, 4) for i in lit], FadeIn(short), run_time=0.6)
        self.at("One of them is")
        self.play(FadeIn(bcr), Indicate(K.body, color=TEXT, scale_factor=1.03), run_time=0.7)
        on = T("always on", 30, GREEN, weight=BOLD).move_to(V(-3.4, -3.0))
        self.at("always on")
        self.play(K.body.animate.set_stroke(GREEN, 6), FadeIn(on), run_time=0.5)
        dis = T("drives chronic myeloid leukaemia", 26, TEAL).move_to(V(-3.4, 3.1))
        # the label sits above the hovering wedge's reach: wedge stays below it
        self.at("drives chronic")
        self.play(FadeIn(dis), run_time=0.5)
        inh = T("inhibited", 30, RED, weight=BOLD).move_to(on)
        self.at("Imatinib sits")
        self.play(FadeOut(on), K.body.animate.set_stroke(BLUE, 3), atp.animate.shift(LEFT * 1.6 + UP * 0.2).set_opacity(0),
                  w.animate.shift(DOWN * 2.2 * k), wl.animate.shift(DOWN * 2.2 * k), run_time=0.9)
        self.at("and inhibits it")
        self.play(K.body.animate.set_stroke(RED, 6), FadeIn(inh), run_time=0.5)

        c1 = chip("leukaemia cell", TEAL, size=26).move_to(V(3.7, -0.75))
        r1 = T("without BCR-ABL: most do not get through", 22, RED).next_to(c1, DOWN, buff=0.15)
        c2 = chip("normal cell", TEAL, size=26).move_to(V(3.7, -2.45))
        r2 = T("early tests:\nnormal colonies grew", 22, GREEN, line_spacing=0.9).next_to(c2, DOWN, buff=0.15)
        self.at("cells do not")
        self.play(FadeOut(short), FadeIn(c1), run_time=0.4)
        self.at("get through a")
        self.play(FadeIn(r1), run_time=0.4)
        self.at("early tests")
        self.play(FadeIn(c2), run_time=0.4)
        self.at("normal colonies")
        self.play(FadeIn(r2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Letter(SpokenScene):
    """relapse, the gene read from the blood, one DNA letter, one residue."""

    def construct(self):
        pat = chip("patients on imatinib", TEAL, size=26).move_to(V(-3.8, 3.0))
        self.play(FadeIn(pat), run_time=0.5)
        well = chip("well", GREEN, size=26).move_to(V(0.2, 3.0))
        rel = chip("relapse", RED, size=26).move_to(V(3.2, 3.0))
        a1 = Arrow(pat.get_right(), well.get_left(), buff=0.12, color=GREY, stroke_width=4, tip_length=0.2)
        a2 = Arrow(well.get_right(), rel.get_left(), buff=0.12, color=GREY, stroke_width=4, tip_length=0.2)
        self.at("got well")
        self.play(GrowArrow(a1), FadeIn(well), run_time=0.5)
        self.at("relapsed")
        self.play(GrowArrow(a2), FadeIn(rel), run_time=0.5)

        gene = Rectangle(width=8.4, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to(V(1.2, 1.2))
        glab = T("BCR-ABL gene", 26, GREY).next_to(gene, UP, buff=0.12)
        blood = chip("blood", TEAL, size=26).move_to(V(-5.0, 1.2))
        self.at("read the")
        self.play(FadeIn(gene), FadeIn(glab), run_time=0.5)
        ba = Arrow(blood.get_right(), gene.get_left(), buff=0.1, color=TEAL, stroke_width=4, tip_length=0.2)
        self.at("from their blood")
        self.play(FadeIn(blood), GrowArrow(ba), run_time=0.5)

        # zoom to the three letters
        spot = V(1.9, 1.2)
        letters = [M(ch, 100, TEXT, weight=BOLD) for ch in "ACT"]
        for i, l in enumerate(letters):
            l.move_to(V(-1.2 + 1.5 * i + 1.5, -0.7))
        row = VGroup(*letters)
        dna = T("DNA", 26, GREY).next_to(row, LEFT, buff=0.7)
        lines = VGroup(Line(spot + V(-0.1, -0.15), row.get_corner(UL) + V(-0.1, 0.1), color=GREY, stroke_width=2),
                       Line(spot + V(0.1, -0.15), row.get_corner(UR) + V(0.1, 0.1), color=GREY, stroke_width=2))
        mark = Rectangle(width=0.3, height=0.5, stroke_color=YELLOW, stroke_width=3).move_to(spot)
        self.at("had changed")
        self.play(Create(mark), Create(lines), FadeIn(row), FadeIn(dna), run_time=0.8)
        newT = M("T", 100, YELLOW, weight=BOLD).move_to(letters[1])
        self.at("had become")
        self.play(letters[1].animate.set_color(YELLOW), run_time=0.3)
        self.play(ReplacementTransform(letters[1], newT), run_time=0.6)

        thr = chip("threonine 315", YELLOW, size=28).move_to(V(0.3, -2.7))
        ile = chip("isoleucine 315", YELLOW, size=28).move_to(thr)
        self.at("replaces")
        self.play(FadeIn(thr, shift=UP * 0.1), run_time=0.5)
        self.at("with isoleucine")
        self.play(ReplacementTransform(thr, ile), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def residue_chip(text, color, size, center):
    return chip(text, color, size=size, pad=0.14).move_to(center)


class S04Contact(SpokenScene):
    """the contact that holds the drug; the bulkier residue pushes it out; the kinase still works."""

    def construct(self):
        K = Kin(-2.0, -0.4, 1.15)
        pc, k = K.pc, K.k
        w = wedge(pc, k, hw=1.5)
        wl = wlabel("imatinib", pc, k, size=26)
        knob = bump_of(pc, k, big=False)
        thr = residue_chip("Thr 315", YELLOW, 24, pc + k * V(-3.05, 0.5))
        tie = Line(thr.get_right(), knob.get_left(), color=YELLOW, stroke_width=3)
        contact = DashedLine(knob.get_right(), pc + k * V(-1.5, 0.5), color=YELLOW, stroke_width=4, dash_length=0.08)
        self.play(FadeIn(K), run_time=0.5)
        self.play(FadeIn(w), FadeIn(wl), FadeIn(knob), FadeIn(thr), FadeIn(tie), run_time=0.6)
        self.at("one of the contacts")
        self.play(Create(contact), Indicate(knob, color=TEXT, scale_factor=1.3), run_time=0.7)

        bump = bump_of(pc, k, big=True)
        ile = residue_chip("Ile 315", YELLOW, 24, pc + k * V(-3.05, 0.5))
        self.at("Isoleucine is bulkier")
        self.play(ReplacementTransform(knob, bump), ReplacementTransform(thr, ile), FadeOut(contact),
                  FadeOut(tie), run_time=0.9)
        tie2 = Line(ile.get_right(), bump.get_left(), color=YELLOW, stroke_width=3)
        self.add(tie2)
        no = T("no contact", 26, RED).move_to(pc + k * V(-1.2, -1.75))
        self.at("cannot make that contact")
        self.play(w.animate.shift(RIGHT * 0.4 * k + UP * 0.2 * k), wl.animate.shift(RIGHT * 0.4 * k + UP * 0.2 * k),
                  FadeIn(no), run_time=0.7)
        nb = T("drug no longer binds", 24, RED, weight=BOLD).move_to(V(4.4, -0.75))
        out = V(4.4 - pc[0], 1.6 - (pc[1] + 0.3 * k))   # the wedge label's centre goes to (4.1, 1.6)
        self.at("no longer binds")
        self.play(w.animate.shift(out - V(0.4 * k, 0.2 * k)).set_stroke(RED, 5),
                  wl.animate.shift(out - V(0.4 * k, 0.2 * k)), FadeOut(no), FadeIn(nb), run_time=0.9)

        note = T("reaction still works", 24, YELLOW).move_to(V(-2.0, -2.2))
        self.at("enzyme can")
        self.play(FadeIn(note), Indicate(bump, color=TEXT, scale_factor=1.1), run_time=0.6)
        atp = atp_chip(pc, k, xo=0.6)
        sub = chip("substrate", TEAL, size=24).move_to(V(4.4, -2.3))
        self.at("its reaction")
        self.play(FadeOut(wl), FadeOut(w), FadeOut(nb), FadeOut(note), FadeIn(atp, shift=DOWN * 0.3), FadeIn(sub), run_time=0.6)
        p = pbadge().move_to(atp.get_right() + RIGHT * 0.2)
        self.play(FadeIn(p, scale=0.5), K.body.animate.set_stroke(GREEN, 6), run_time=0.4)
        self.play(p.animate(path_arc=-1.0).move_to(sub.get_top() + UP * 0.3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Experiment(SpokenScene):
    """a relapse read as an experiment: one position changed, the rest left alone."""

    def construct(self):
        K = Kin(-2.8, -0.5, 0.95)
        pc, k = K.pc, K.k
        bump = bump_of(pc, k)
        ile = residue_chip("Ile 315", YELLOW, 24, pc + k * V(-3.0, 0.5))
        K.body.set_stroke(GREEN, 5)
        self.play(FadeIn(K), FadeIn(bump), FadeIn(ile), run_time=0.7)
        fail = T("failure", 56, RED, font=TITLE_FONT).move_to(V(0, 2.9))
        self.at("looks like a failure")
        self.play(FadeIn(fail, shift=UP * 0.1), run_time=0.5)
        cross = Line(fail.get_left() + LEFT * 0.1, fail.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        exp = T("experiment", 56, GREEN, font=TITLE_FONT).move_to(fail)
        self.at("as an experiment")
        self.play(ReplacementTransform(fail, exp), run_time=0.8)

        one = T("the one position the drug depended on", 24, YELLOW).move_to(V(-2.8, -3.1))
        self.at("one position")
        self.play(Indicate(bump, color=TEXT, scale_factor=1.25), FadeIn(one), run_time=0.8)
        rest = T("the rest of the enzyme: unchanged", 24, GREY).move_to(V(-2.8, -3.1))
        self.at("rest of")
        self.play(FadeOut(one), FadeIn(rest), Indicate(K.body, color=TEXT, scale_factor=1.03), run_time=0.8)

        l1 = T("the drug had been working\nthrough BCR-ABL", 30, GREEN, line_spacing=0.9).move_to(V(3.8, 0.6))
        l2 = T("the leukaemia\nstill needed it", 30, GREEN, line_spacing=0.9).move_to(V(3.8, -1.5))
        self.at("had been working")
        self.play(FadeIn(l1, shift=LEFT * 0.15), run_time=0.6)
        self.at("still needed")
        self.play(FadeIn(l2, shift=LEFT * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Next(SpokenScene):
    """the relapse specifies the next drug: a slim bond that passes residue 315."""

    def construct(self):
        K = Kin(0, -0.3, 1.1)
        pc, k = K.pc, K.k
        bump = bump_of(pc, k)
        ile = residue_chip("Ile 315", YELLOW, 24, pc + k * V(-3.0, 0.5))
        tie = Line(ile.get_right(), bump.get_left(), color=YELLOW, stroke_width=3)
        self.play(FadeIn(K), FadeIn(bump), FadeIn(ile), FadeIn(tie), run_time=0.7)
        spec = T("next drug: grip ABL without needing residue 315", 28, TEXT).move_to(V(0, 3.1))
        self.at("specification")
        self.play(FadeIn(spec, shift=DOWN * 0.1), run_time=0.6)

        hw, xo = 1.1, 0.8
        w = wedge(pc, k, hw=hw, xo=xo, yo=1.3)
        rod = Line(pc + k * V(xo - hw, -0.05 + 1.3), pc + k * V(-1.95, -0.05 + 1.3), color=PINK, stroke_width=5)
        tip = Dot(pc + k * V(-1.95, 1.25), radius=0.06, color=PINK)
        wl = wlabel("ponatinib", pc, k, xo=xo, yo=1.3, size=24)
        pon = VGroup(w, rod, tip)
        self.at("Punatinib was built")
        self.play(FadeIn(pon, shift=DOWN * 0.2), FadeIn(wl, shift=DOWN * 0.2), run_time=0.6)
        slim = T("slim carbon-\ncarbon triple\nbond", 24, PINK, line_spacing=0.9).move_to(V(-5.3, 1.9))
        slim = VGroup(slim, Line(V(-4.35, 1.9), pc + k * V(-1.95, 1.25), color=PINK, stroke_width=2))
        self.at("slim")
        self.play(FadeIn(slim), Indicate(rod, color=TEXT, scale_factor=1.3), run_time=0.6)
        self.at("sticks out")
        self.play(Indicate(bump, color=TEXT, scale_factor=1.15), pon.animate.shift(DOWN * 1.3 * k),
                  wl.animate.shift(DOWN * 1.3 * k), FadeOut(slim), run_time=1.0)
        inh = T("mutant kinase inhibited", 28, RED, weight=BOLD).move_to(V(0, -3.25))
        self.at("inhibits the mutant")
        self.play(K.body.animate.set_stroke(RED, 6), FadeIn(inh), run_time=0.5)
        rule = T("A relapse writes the specification for the next drug.", 30, GOLD, font=TITLE_FONT).move_to(V(0, -3.25))
        fit(rule, max_w=12)
        self.at("Keep this rule")
        self.play(FadeOut(inh), FadeOut(spec), run_time=0.4)
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "A relapse writes the specification for the next drug."
