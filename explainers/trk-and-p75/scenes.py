"""Trk receptors and p75: one factor, two opposite messages (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the neurotrophin (NGF) itself, mature or precursor body
  ORANGE = the pro-domain (the extra stretch at the front of proNGF)
  PINK   = Trk receptors (TrkA) and their kinase feet
  VIOLET = p75 (and the TNF-receptor family / Fas it belongs with)
  YELLOW = sortilin
  GOLD   = the cutting enzymes (plasmin, matrix metalloproteinases)
  GREEN  = survival
  RED    = death (apoptosis)
  GREY   = membrane, cells, outlines, unknowns, the scope notes
  TEXT   = phosphate badges and the final "what the factor says"
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E879B9"
ORANGE = "#F29E4C"
VIOLET = "#A98BE0"
GOLDC = GOLD


def membrane():
    return Rectangle(width=12.4, height=0.36, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, 0, 0])


def dimer(cx, cy, s=1.0, tails=False, color=BLUE):
    bodies, tl = [], []
    for sx in (-1, 1):
        b = Ellipse(width=0.95 * s, height=0.75 * s, stroke_color=color, stroke_width=3,
                    fill_color=color, fill_opacity=0.5).move_to([cx + sx * 0.5 * s, cy, 0])
        bodies.append(b)
        if tails:
            t = RoundedRectangle(corner_radius=0.1 * s, width=0.26 * s, height=0.8 * s, stroke_color=ORANGE,
                                 stroke_width=3, fill_color=ORANGE, fill_opacity=0.65)
            t.move_to([cx + sx * 0.5 * s, cy + 0.375 * s + 0.32 * s, 0])
            tl.append(t)
    g = VGroup(*bodies, *tl)
    g.bodies = VGroup(*bodies)
    g.tails = VGroup(*tl)
    return g


def receptor(x, color, foot=True, h=2.7):
    bar = RoundedRectangle(corner_radius=0.16, width=0.45, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.55).move_to([x, 0, 0])
    parts = [bar]
    ft = None
    if foot:
        ft = Circle(radius=0.26, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.4)
        ft.move_to([x, -h / 2 - 0.2, 0])
        parts.append(ft)
    g = VGroup(*parts)
    g.bar = bar
    g.foot = ft
    return g


def badge(pos):
    c = Circle(radius=0.2, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    return VGroup(c, T("P", 22, TEXT)).move_to(pos)


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def lab(text, color, x, y, size=26):
    return T(text, size, color).move_to([x, y, 0])


def cross(center, size=0.28, color=RED):
    cx, cy = center[0], center[1]
    return VGroup(Line([cx - size, cy - size, 0], [cx + size, cy + size, 0], color=color, stroke_width=7),
                  Line([cx - size, cy + size, 0], [cx + size, cy - size, 0], color=color, stroke_width=7))


class S00Title(TitleCard):
    LESSON = "Neurotrophins, Trk Receptors and p75"
    TITLE = "Neurotrophins Switch On Survival Signals"


# The original title/end cards and drawing helpers are retained verbatim.
S = 1.2
HX = 0.6
RTOP = 1.35
DY = RTOP + 0.45


def neuron(x, y, r=1.0):
    cell = Circle(radius=r, stroke_color=GREY, stroke_width=4,
                  fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    rec = receptor(x, PINK, h=1.0).shift(UP * (y + r))
    return VGroup(cell, rec)


def population(x, y, n=6, color=GREY):
    # Schematic counts, never quantitative knockout measurements.
    return VGroup(*[Circle(radius=0.18, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.35)
                   .move_to([x + (i % 3 - 1) * 0.55, y - (i // 3) * 0.55, 0])
                   for i in range(n)])


class S01Question(SpokenScene):
    def construct(self):
        target = chip("target", GREY, 30).move_to([-4.6, 1.6, 0])
        n = neuron(2.6, -0.5, 1.8)
        nl = lab("developing neuron", GREY, 2.6, -2.8, 28)
        factor = dimer(-4.6, 0.2, 1.0)
        fl = lab("neurotrophin", BLUE, -4.6, -0.7, 26)
        self.at("Many developing neurons")
        self.play(FadeIn(target), FadeIn(n), FadeIn(nl), run_time=0.6)
        self.at("a neurotrophin activates")
        self.play(FadeIn(factor), FadeIn(fl), run_time=0.4)
        self.play(factor.animate.move_to([2.6, 2.1, 0]), run_time=0.8)
        rl = lab("matching Trk", PINK, 5.2, 1.3, 26)
        self.play(FadeIn(rl), Indicate(n[1], color=PINK), run_time=0.5)
        self.at("are kinases")
        self.play(Indicate(n[1].foot, color=PINK), run_time=0.5)
        self.at("signals supporting survival")
        signal = chip("survival + growth", GREEN, 26).move_to([2.6, -0.8, 0])
        self.play(FadeIn(signal), n[0].animate.set_stroke(GREEN), run_time=0.6)
        self.at("its target supplies")
        a = arr([-3.5, 1.6, 0], [1.2, 2.1, 0], BLUE)
        self.play(GrowArrow(a), run_time=0.6)
        self.at("different groups of neurons")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        groups = VGroup()
        for x, f, r in [(-4.2, "NGF", "TrkA"), (0, "BDNF / NT-4", "TrkB"), (4.2, "NT-3", "TrkC")]:
            g = VGroup(neuron(x, -0.5), dimer(x, 1.7, 0.8),
                       lab(f, BLUE, x, 2.7), lab(r, PINK, x, -2.1),
                       lab("survival", GREEN, x, -3.0))
            groups.add(g)
        self.play(FadeIn(groups, lag_ratio=0.15), run_time=0.8)
        self.at("How does that survival")
        q = lab("How does the signal start?", TEXT, 0, 3.5, 30)
        self.play(FadeIn(q), run_time=0.5)
        self.finish()


class S02Trk(SpokenScene):
    def construct(self):
        self.at("Mammals make")
        head = lab("Four neurotrophins → three Trks", TEXT, 0, 3.3, 32)
        self.play(FadeIn(head), run_time=0.4)
        rows = VGroup()
        specs = [("NGF", "TrkA", 1.8), ("BDNF + NT-4", "TrkB", 0.1), ("NT-3", "TrkC", -1.6)]
        for cue, (f, r, y) in zip(["NGF prefers", "BDNF and NT4", "NT3 prefers"], specs):
            self.at(cue)
            row = VGroup(chip(f, BLUE, 28).move_to([-3.5, y, 0]),
                         arr([-1.4, y, 0], [2.0, y, 0], BLUE),
                         chip(r, PINK, 28).move_to([3.1, y, 0]))
            rows.add(row)
            self.play(FadeIn(row), run_time=0.6)
        self.at("and activates")
        weak = VGroup(*[DashedLine([-1.9, -1.35, 0], [2.3, y - 0.3, 0], color=BLUE,
                                   stroke_width=2, dash_length=0.13).add_tip(tip_length=0.16) for y in (1.8, 0.1)],
                      lab("weaker", BLUE, 0, -2.7, 24))
        self.play(FadeIn(weak), run_time=0.6)
        self.at("Each factor is a dimer")
        self.play(FadeOut(rows), FadeOut(weak), FadeOut(head), run_time=0.4)
        d = dimer(0, 2.0, S)
        dl = lab("two identical chains", BLUE, 0, 3.15, 28)
        mem = membrane()
        left, right = receptor(-2.8, PINK), receptor(2.8, PINK)
        self.play(FadeIn(d), FadeIn(dl), FadeIn(mem), FadeIn(left), FadeIn(right), run_time=0.6)
        self.at("It brings")
        self.play(left.animate.shift(RIGHT * 2.2), right.animate.shift(LEFT * 2.2),
                  d.animate.move_to([0, DY, 0]), run_time=0.9)
        self.at("Their kinase domains")
        self.play(left.foot.animate.set_fill(PINK, 0.9), right.foot.animate.set_fill(PINK, 0.9), run_time=0.4)
        self.at("phosphorylate each other")
        fL, fR = left.foot.get_center(), right.foot.get_center()
        pL, pR = badge(fL), badge(fR)
        self.add(pL, pR)
        self.play(MoveAlongPath(pL, ArcBetweenPoints(fL, fR, angle=-PI / 2)),
                  MoveAlongPath(pR, ArcBetweenPoints(fR, fL, angle=-PI / 2)), run_time=0.8)
        self.at("The phosphorylated tyrosines")
        self.play(Indicate(VGroup(pL, pR), color=TEXT), run_time=0.5)
        self.at("through RAS")
        c1 = chip("Ras → ERK", GREEN, 26).move_to([-2.9, -3.1, 0])
        c2 = chip("PI3K → Akt", GREEN, 26).move_to([2.9, -3.1, 0])
        a1 = arr([-0.6, -1.95, 0], [-2.5, -2.7, 0], GREEN)
        a2 = arr([0.6, -1.95, 0], [2.5, -2.7, 0], GREEN)
        self.play(GrowArrow(a1), FadeIn(c1), run_time=0.45)
        self.at("and PI3K")
        self.play(GrowArrow(a2), FadeIn(c2), run_time=0.45)
        self.finish()


class S02Targets(SpokenScene):
    def construct(self):
        target = chip("target", GREY, 30).move_to([0, 2.8, 0])
        pool = VGroup(*[dimer(x, 1.7, 0.5) for x in (-0.7, 0.7)])
        neurons = VGroup(neuron(-3.2, -0.9, 1.25), neuron(3.2, -0.9, 1.25))
        labels = VGroup(*[lab("matching Trk", PINK, x, -2.6, 24) for x in (-3.2, 3.2)])
        self.at("Targets make")
        self.play(FadeIn(target), FadeIn(neurons), FadeIn(labels), run_time=0.5)
        self.at("a limited amount")
        self.play(FadeIn(pool), run_time=0.5)
        self.play(pool[0].animate.move_to([-3.2, 1.1, 0]), run_time=0.7)
        enough = lab("enough → survives", GREEN, -3.2, -3.3, 26)
        self.play(neurons[0][0].animate.set_stroke(GREEN), FadeIn(enough), run_time=0.4)
        self.at("Neurons that fail")
        low = lab("insufficient support", GREY, 3.2, 1.5, 24)
        self.play(FadeIn(low), run_time=0.4)
        self.at("get enough dye")
        lost = lab("neuron lost", RED, 3.2, -3.3, 26)
        self.play(neurons[1].animate.set_opacity(0.12), FadeIn(lost), run_time=0.7)
        self.at("Which factor a population")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        f = chip("target's factor", BLUE, 30).move_to([-3.8, 1.5, 0])
        r = chip("neuron's Trk", PINK, 30).move_to([3.8, 1.5, 0])
        self.play(FadeIn(f), FadeIn(r), run_time=0.6)
        self.at("So the receptor map")
        result = chip("survival dependence", GREEN, 30).move_to([0, -1.8, 0])
        arrows = VGroup(arr([-3.8, 0.9, 0], [-1, -1.25, 0], BLUE),
                         arr([3.8, 0.9, 0], [1, -1.25, 0], PINK))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(result), run_time=0.7)
        self.finish()


class S02Knockouts(SpokenScene):
    def construct(self):
        self.at("Mouse knockouts test")
        heading = lab("Mouse neuron populations", TEXT, 0, 3.4, 32)
        cols = VGroup(lab("control", GREY, 1.0, 2.5), lab("knockout", RED, 4.8, 2.5))
        note = lab("schematic populations • counts are not measurements", GREY, 0, -3.4, 22)
        self.play(FadeIn(heading), FadeIn(cols), FadeIn(note), run_time=0.5)
        rows = VGroup()
        specs = [("Without NGF", "NGF / TrkA", "sympathetic; pain / heat", 1.3),
                 ("Without BDNF", "BDNF", "balance (vestibular)", -0.3),
                 ("Without NT3", "NT-3 / TrkC", "limb position", -1.9)]
        for cue, pair, kind, y in specs:
            self.at(cue)
            name = VGroup(lab(pair, BLUE, -4.2, y + 0.1, 26),
                          lab(kind, GREY, -4.2, y - 0.45, 22))
            control, ko = population(1, y), population(4.8, y)
            row = VGroup(name, control, ko)
            rows.add(row)
            self.play(FadeIn(row), run_time=0.35)
            # Loss is revealed on the subsequent population description.
            loss_cue = {"NGF / TrkA": "mice lose", "BDNF": "for balance", "NT-3 / TrkC": "report limb position"}[pair]
            self.at(loss_cue)
            lost_cells = [ko[i] for i in (1, 3, 4, 5)]
            self.play(*[FadeOut(c, scale=0.5) for c in lost_cells], run_time=0.6)
            ko.remove(*lost_cells)
        self.at("Different pairs give")
        self.play(*[Indicate(row[2], color=RED, scale_factor=1.1) for row in rows], run_time=0.7)
        self.finish()


class S03P75(SpokenScene):
    def construct(self):
        mem = membrane()
        p = receptor(0, VIOLET, foot=False)
        pl = lab("p75", VIOLET, 0, -2.3, 28)
        self.at("A shared receptor")
        self.play(FadeIn(mem), FadeIn(p), FadeIn(pl), run_time=0.5)
        self.at("binds all four")
        names = VGroup(*[chip(n, BLUE, 26).move_to([x, 3.1, 0])
                         for n, x in zip(["NGF", "BDNF", "NT-3", "NT-4"], [-4.5, -1.5, 1.5, 4.5])])
        self.play(FadeIn(names), run_time=0.5)
        for c in names:
            lig = dimer(c.get_x(), 2.3, 0.55)
            self.play(FadeIn(lig), run_time=0.1)
            self.play(lig.animate.move_to([0, 1.6, 0]), run_time=0.2)
            self.play(FadeOut(lig), run_time=0.1)
        self.at("It has no kinase")
        nk = lab("no kinase", GREY, 3.6, -1.3, 26)
        self.play(FadeIn(nk), run_time=0.4)
        self.at("tumor necrosis factor")
        fam = chip("TNF receptor family", VIOLET, 26).move_to([-3.9, 1.1, 0])
        self.play(FadeOut(names), FadeIn(fam), run_time=0.5)
        self.at("a death domain")
        dd = Circle(radius=0.26, stroke_color=VIOLET, fill_color=VIOLET, fill_opacity=0.9).move_to([0, -1.55, 0])
        ddl = lab("death domain", VIOLET, -3.7, -1.55, 26)
        self.play(FadeIn(dd), FadeIn(ddl), run_time=0.4)
        self.at("But its response depends")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        title = lab("p75: response depends on partners", TEXT, 0, 3.2, 32)
        self.play(FadeIn(title), run_time=0.4)
        self.at("it can raise")
        # Functional association only: no physical TrkA–p75 complex is asserted.
        left = VGroup(chip("p75", VIOLET, 28).move_to([-4.8, 1.0, 0]),
                      chip("TrkA", PINK, 28).move_to([-2.3, 1.0, 0]),
                      lab("with", GREY, -3.55, 1.0, 22),
                      lab("can raise NGF binding", BLUE, -3.5, -0.5, 26))
        self.play(FadeIn(left), run_time=0.5)
        self.at("it can carry")
        right = VGroup(chip("p75", VIOLET, 28).move_to([2.1, 1.0, 0]),
                       chip("sortilin", YELLOW, 28).move_to([4.9, 1.0, 0]),
                       lab("with", GREY, 3.4, 1.0, 22),
                       arr([3.5, 0.3, 0], [3.5, -1.3, 0], RED),
                       chip("can signal death", RED, 26).move_to([3.5, -2.0, 0]))
        self.play(FadeIn(right), run_time=0.6)
        self.finish()


class S05Outcome(SpokenScene):
    def construct(self):
        self.at("Precursor processing adds")
        heading = lab("Processing changes the signal", TEXT, 0, 3.3, 32)
        self.play(FadeIn(heading), run_time=0.4)
        self.at("starts as a longer chain")
        cell = Circle(radius=1.8, stroke_color=GREY, stroke_width=4,
                      fill_color=GREY, fill_opacity=0.12).move_to([-3.8, -0.3, 0])
        pro = dimer(-3.8, -0.3, 1.2, tails=True)
        nm = lab("proNGF", BLUE, -3.8, -2.5, 28)
        pd = lab("pro-domain", ORANGE, -3.8, 2.0, 26)
        self.play(FadeIn(cell), FadeIn(pro), FadeIn(nm), FadeIn(pd), run_time=0.6)
        self.at("Cells can")
        self.play(pro.animate.shift(RIGHT * 7.3), nm.animate.shift(RIGHT * 7.3),
                  pd.animate.shift(RIGHT * 7.3), run_time=0.8)
        self.at("In Hempstead's experiments")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        head = lab("cultured sympathetic neurons", GREY, 0, 3.55, 26)
        pro = dimer(-3.2, 1.6, 1.0, tails=True)
        prl = lab("uncut proNGF", BLUE, -3.2, 2.95, 26)
        p = receptor(-3.8, VIOLET)
        p.foot.set_fill(VIOLET, 0.9)
        pl = lab("p75", VIOLET, -4.6, -1.5, 24)
        mem = membrane()
        self.play(FadeIn(head), FadeIn(pro), FadeIn(prl), FadeIn(p), FadeIn(pl), FadeIn(mem), run_time=0.5)
        self.at("bound P75 tightly")
        self.play(pro.animate.shift(DOWN * 0.2), Indicate(p.bar, color=VIOLET), run_time=0.6)
        self.at("triggered apoptosis")
        dead = chip("apoptosis", RED, 28).move_to([-3.2, -3.1, 0])
        da = arr([-3.8, -1.95, 0], [-3.2, -2.65, 0], RED)
        self.play(FadeIn(dead), GrowArrow(da), run_time=0.5)
        self.at("Later work showed")
        sort = receptor(-2.3, YELLOW, foot=False)
        sl = lab("sortilin required", YELLOW, -1.9, -1.95, 24)
        self.play(FadeIn(sort), FadeIn(sl), run_time=0.5)
        self.at("Mature NGF supported")
        # Same membrane, a separate comparison on the right.
        mat = dimer(3.2, DY, 1.0)
        ml = lab("mature NGF", BLUE, 3.2, 2.95, 26)
        trks = VGroup(receptor(2.6, PINK), receptor(3.8, PINK))
        tl = lab("TrkA", PINK, 3.2, -2.2, 24)
        ok = chip("survival", GREEN, 28).move_to([3.2, -3.1, 0])
        self.play(FadeIn(mat), FadeIn(ml), FadeIn(trks), FadeIn(tl), run_time=0.5)
        self.play(FadeIn(badge(trks[0].foot.get_center())), FadeIn(badge(trks[1].foot.get_center())),
                  FadeIn(ok), run_time=0.5)
        self.at("Another group found")
        # Clear both experimental outcomes before introducing the alternative result.
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        alt = dimer(-3.3, 0.3, 1.3, tails=True)
        al = lab("uncut proNGF", BLUE, -3.3, 2.0, 28)
        ah = lab("another group's result", GREY, 0, 3.3, 28)
        self.play(FadeIn(alt), FadeIn(al), FadeIn(ah), run_time=0.5)
        self.at("could support survival too")
        weak = chip("weaker survival", GREEN, 30).move_to([3.2, 0.3, 0])
        wa = arr([-1.7, 0.3, 0], weak.get_left() + LEFT * 0.2, GREEN, w=2)
        self.play(GrowArrow(wa), FadeIn(weak), run_time=0.5)
        self.at("more weekly")
        wl = lab("weaker support", GREEN, 3.2, -0.7, 26)
        self.play(FadeIn(wl), run_time=0.4)
        self.at("The outcome depends")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        cut = chip("processing", ORANGE, 30).move_to([-3.5, 1.8, 0])
        balance = chip("receptor balance", PINK, 30).move_to([3.5, 1.8, 0])
        result = chip("outcome", TEXT, 34).move_to([0, -1.7, 0])
        self.play(FadeIn(cut), FadeIn(balance), run_time=0.4)
        self.play(GrowArrow(arr([-3.5, 1.15, 0], [-0.8, -1.1, 0], ORANGE)),
                  GrowArrow(arr([3.5, 1.15, 0], [0.8, -1.1, 0], PINK)), FadeIn(result), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Many developing neurons survive when the right neurotrophin activates its Trk receptor."
