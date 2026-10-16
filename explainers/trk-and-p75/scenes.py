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
    TITLE = "One factor, two opposite messages"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        C = np.array([1.8, 0.2, 0])
        R = 2.3
        cell = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(C)
        self.at("mature nerve growth")
        d1 = dimer(-4.5, 0.2, 1.5)
        l1 = lab("mature NGF", BLUE, -4.5, 1.2, 28)
        g1 = VGroup(d1, l1)
        self.play(FadeIn(g1, scale=0.9), run_time=0.6)
        self.at("cultured sympathetic")
        nl = lab("cultured sympathetic neurons", GREY, 1.8, 3.1, 26)
        self.play(FadeIn(cell, scale=0.92), FadeIn(nl, shift=UP * 0.1), run_time=0.6)
        self.play(g1.animate.shift(RIGHT * 2.7), run_time=0.8)
        self.at("they survive")
        ok = chip("survives", GREEN, size=28).move_to([1.8, -3.2, 0])
        self.play(cell.animate.set_stroke(GREEN).set_fill(GREEN, 0.3), FadeIn(ok, shift=UP * 0.1), run_time=0.5)
        # --- case 2: reset the old answer in the same beat as the new factor comes in
        self.at("add the same protein")
        d2 = dimer(-4.5, 0.2, 1.5, tails=True)
        l2 = lab("same NGF, uncut", TEXT, -4.5, 2.3, 28)
        g2 = VGroup(d2, l2)
        self.play(cell.animate.set_stroke(GREY).set_fill(GREY, 0.12), FadeOut(ok), FadeOut(g1),
                  FadeIn(g2, shift=RIGHT * 0.3), run_time=0.6)
        self.at("Barbara Hempstead's")
        self.play(g2.animate.shift(RIGHT * 2.7), run_time=0.8)
        self.at("neurons died")
        bad = chip("dies", RED, size=28).move_to([1.8, -3.2, 0])
        self.play(cell.animate.set_stroke(RED).set_fill(RED, 0.3), FadeIn(bad, shift=UP * 0.1), run_time=0.5)
        self.at("How can one factor")
        self.play(cell.animate.set_stroke(GREY).set_fill(GREY, 0.12), FadeOut(bad), FadeOut(g2), run_time=0.5)
        self.at("opposite messages")
        a = chip("survives", GREEN, size=28).move_to([-2.0, 0.2, 0])
        b = chip("dies", RED, size=28).move_to([5.3, 0.2, 0])
        self.play(FadeIn(a, shift=RIGHT * 0.2), FadeIn(b, shift=LEFT * 0.2), run_time=0.5)
        self.at("receptors on the neuron")
        bars = VGroup()
        for deg in (55, 80, 105, 130):
            ang = deg * DEGREES
            p = C + R * np.array([np.cos(ang), np.sin(ang), 0])
            bar = RoundedRectangle(corner_radius=0.08, width=0.34, height=0.85, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.5).rotate(ang - PI / 2).move_to(p)
            bars.add(bar)
        q = lab("receptors?", GREY, 1.8, 3.3, 30)
        self.play(FadeOut(a), FadeOut(b), FadeOut(nl), FadeIn(bars, lag_ratio=0.2), FadeIn(q, shift=DOWN * 0.1),
                  run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
S = 1.2           # ligand scale on the membrane stage
HX = 0.6          # half spacing of a receptor pair under a dimer
RTOP = 1.35       # top of a receptor bar
DY = RTOP + 0.45  # dimer centre height when docked


class S02Trk(SpokenScene):
    def construct(self):
        mem = membrane()
        lo = T("outside", 22, GREY).move_to([-5.3, 0.6, 0])
        li = T("inside", 22, GREY).move_to([-5.3, -0.6, 0])
        self.at("two kinds of receptor")
        self.play(FadeIn(mem), FadeIn(lo), FadeIn(li), run_time=0.5)
        self.at("the first kind")
        rA, rB, rC = receptor(-3, PINK), receptor(0, PINK), receptor(3, PINK)
        la, lb, lc = lab("TrkA", PINK, -3, -2.3), lab("TrkB", PINK, 0, -2.3), lab("TrkC", PINK, 3, -2.3)
        head = lab("Trk receptors", PINK, 0, 3.2, 30)
        self.play(FadeIn(rA, shift=UP * 0.2), FadeIn(rB, shift=UP * 0.2), FadeIn(rC, shift=UP * 0.2),
                  FadeIn(head), run_time=0.7)
        self.play(FadeIn(la), FadeIn(lb), FadeIn(lc), run_time=0.4)
        self.at("particular factors")
        self.play(Indicate(rA.bar, color=PINK, scale_factor=1.08), Indicate(rB.bar, color=PINK, scale_factor=1.08),
                  Indicate(rC.bar, color=PINK, scale_factor=1.08), run_time=0.7)
        self.at("prefers", nth=1)
        d = dimer(-3, 2.5, S)
        nl = lab("NGF", BLUE, -3, 3.3, 26)
        ng = VGroup(d, nl)
        self.play(FadeIn(ng, shift=DOWN * 0.2), Indicate(rA.bar, color=PINK, scale_factor=1.12), run_time=0.7)
        self.at("is a dimer")
        self.play(Indicate(d, color=BLUE, scale_factor=1.12), run_time=0.6)
        self.at("two receptors together")
        rA2 = receptor(HX, PINK)
        two = lab("2 x TrkA", PINK, 0, -2.3, 26)
        self.play(FadeOut(head), FadeOut(rB), FadeOut(rC), FadeOut(la), FadeOut(lb), FadeOut(lc),
                  rA.animate.shift(RIGHT * (3 - HX)), FadeIn(rA2), FadeIn(two),
                  d.animate.move_to([0, DY, 0]), nl.animate.move_to([0, DY + 0.8, 0]), run_time=1.0)
        self.at("kinase domains")
        fL, fR = rA.foot.get_center(), rA2.foot.get_center()
        self.play(rA.foot.animate.set_fill(PINK, 0.9), rA2.foot.animate.set_fill(PINK, 0.9), run_time=0.4)
        self.at("phosphorylate each other")
        pL, pR = badge(fL), badge(fR)
        self.add(pL, pR)
        self.play(MoveAlongPath(pL, ArcBetweenPoints(fL, fR, angle=-PI / 2)),
                  MoveAlongPath(pR, ArcBetweenPoints(fR, fL, angle=-PI / 2)), run_time=0.9)
        self.at("survival branches")
        c1 = chip("Ras to ERK", GREEN, size=26).move_to([-2.9, -3.2, 0])
        c2 = chip("PI3K to Akt", GREEN, size=26).move_to([2.9, -3.2, 0])
        a1 = arr([-0.6, -1.95, 0], [-2.5, -2.85, 0], GREEN)
        a2 = arr([0.6, -1.95, 0], [2.5, -2.85, 0], GREEN)
        self.play(FadeIn(a1), FadeIn(a2), FadeIn(c1, shift=UP * 0.1), FadeIn(c2, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03P75(SpokenScene):
    def construct(self):
        mem = membrane()
        lo = T("outside", 22, GREY).move_to([-5.3, 0.6, 0])
        li = T("inside", 22, GREY).move_to([-5.3, -0.6, 0])
        trk = VGroup(*[receptor(x, PINK) for x in (-4.4, -3.4, -2.4)])
        trkl = lab("Trk", PINK, -3.4, -2.3)
        self.add(mem, lo, li, trk, trkl)
        self.at("The second kind")
        p = receptor(1.2, VIOLET, foot=False)
        pl = lab("p75", VIOLET, 1.2, -2.3, 28)
        self.play(FadeIn(p, shift=UP * 0.2), FadeIn(pl), run_time=0.6)
        self.at("binds all four")
        button = Circle(radius=0.22, stroke_color=VIOLET, stroke_width=3, fill_color=VIOLET, fill_opacity=0.9)
        button.move_to([1.2, 1.62, 0])
        names = ["NGF", "BDNF", "NT-3", "NT-4"]
        chips = VGroup(*[chip(n, BLUE, size=26).move_to([x, 3.0, 0]) for n, x in zip(names, (-1.4, 0.35, 2.05, 3.75))])
        self.play(FadeIn(button, scale=0.5), FadeIn(chips, lag_ratio=0.2), run_time=0.7)
        for c in chips:
            ring = Circle(radius=0.25, stroke_color=VIOLET, stroke_width=4).move_to(button)
            self.play(Indicate(c, color=BLUE, scale_factor=1.12), ring.animate.scale(3.2).set_stroke(opacity=0),
                      run_time=0.3)
            self.remove(ring)
        self.at("no kinase")
        nk = lab("no kinase", GREY, 1.2, -2.3, 26)
        self.play(ReplacementTransform(pl, nk), run_time=0.4)
        self.at("tumor necrosis factor")
        fam = chip("TNF receptor family", VIOLET, size=24).move_to([4.2, 1.9, 0])
        self.play(FadeIn(fam, shift=LEFT * 0.2), run_time=0.5)
        self.at("death receptor Fas")
        fas = chip("Fas", VIOLET, size=24).move_to([4.2, 1.0, 0])
        ln = Line(fam.get_bottom(), fas.get_top(), color=VIOLET, stroke_width=3)
        self.play(FadeIn(fas, shift=UP * 0.1), Create(ln), run_time=0.5)
        self.at("death domain")
        dd = Circle(radius=0.26, stroke_color=VIOLET, stroke_width=3, fill_color=VIOLET, fill_opacity=0.9)
        dd.move_to([1.2, -1.55, 0])
        ddl = lab("death domain", VIOLET, 1.2, -2.3, 26)
        self.play(FadeIn(dd, scale=0.4), ReplacementTransform(nk, ddl), run_time=0.5)
        self.at("locks cut")
        lk = lab("locks, cut for certain keys", PINK, -3.4, -2.3, 24)
        self.play(ReplacementTransform(trkl, lk), *[Indicate(r.bar, color=PINK, scale_factor=1.1) for r in trk],
                  run_time=0.8)
        self.at("doorbell")
        db = lab("doorbell", VIOLET, -0.4, 1.62, 26)
        self.play(FadeIn(db, shift=RIGHT * 0.1), run_time=0.4)
        self.at("any key can ring")
        for _ in range(2):
            ring = Circle(radius=0.25, stroke_color=VIOLET, stroke_width=4).move_to(button)
            self.play(ring.animate.scale(3.5).set_stroke(opacity=0), Indicate(button, color=VIOLET, scale_factor=1.5),
                      run_time=0.45)
            self.remove(ring)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cut(SpokenScene):
    def construct(self):
        C = np.array([-3.4, 0.3, 0])
        SS = 1.9
        CY = -0.4          # dimer body height
        cell = Circle(radius=2.7, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(C)
        self.at("Like most secreted")
        self.play(FadeIn(cell, scale=0.92), run_time=0.6)
        self.at("is made")
        d = dimer(C[0], CY, SS)
        self.play(FadeIn(d, scale=0.7), run_time=0.5)
        self.at("longer chain")
        tails = dimer(C[0], CY, SS, tails=True).tails
        self.play(*[GrowFromEdge(t, DOWN) for t in tails], run_time=0.6)
        d.add(*tails)
        self.at("extra stretch")
        pdl = lab("pro-domain", ORANGE, 0.3, 2.6, 28)
        pa = arr([-0.8, 2.55, 0], [C[0] + 0.95 + 0.25, 2.15, 0], ORANGE)
        self.play(FadeIn(pdl, shift=LEFT * 0.1), FadeIn(pa), Indicate(tails, color=ORANGE, scale_factor=1.15),
                  run_time=0.7)
        self.at("is called")
        nm = lab("proNGF", BLUE, C[0], CY - 1.15, 30)
        self.play(FadeIn(nm, shift=UP * 0.1), run_time=0.4)
        self.at("accepted view")
        guess = chip("trimmed inside the cell?", GREY, size=24).move_to([C[0], -3.15, 0])
        self.play(FadeIn(guess, shift=UP * 0.1), run_time=0.5)
        self.at("secrete")
        x = cross(guess.get_center())
        self.play(Create(x), run_time=0.3)
        self.play(FadeOut(guess), FadeOut(x), FadeOut(pdl), FadeOut(pa),
                  VGroup(d, nm).animate.shift(RIGHT * 6.6), run_time=1.0)
        self.at("outside the cell")
        out = lab("outside the cell", GREY, 3.2, -2.6, 26)
        self.play(FadeIn(out), run_time=0.4)
        self.at("plasmin")
        cx = d.bodies[0].get_center()[0]
        tl_l, tl_r = tails[0], tails[1]
        pc = chip("plasmin", GOLD, size=26).move_to([cx - 0.2, 3.0, 0])
        pca = arr([cx - 0.2, 2.65, 0], [tl_l.get_center()[0], tl_l.get_top()[1] + 0.05, 0], GOLD)
        self.play(FadeIn(pc, shift=DOWN * 0.1), FadeIn(pca), run_time=0.4)
        self.play(tl_l.animate.shift(LEFT * 1.0 + UP * 0.2).set_opacity(0.0), FadeOut(pca), run_time=0.6)
        self.at("matrix metalloproteinases")
        cxr = d.bodies[1].get_center()[0]
        mc = chip("MMPs", GOLD, size=26).move_to([cxr + 0.9, 3.0, 0])
        mca = arr([cxr + 0.9, 2.65, 0], [tl_r.get_center()[0], tl_r.get_top()[1] + 0.05, 0], GOLD)
        self.play(FadeIn(mc, shift=DOWN * 0.1), FadeIn(mca), run_time=0.4)
        self.play(tl_r.animate.shift(RIGHT * 1.0 + UP * 0.2).set_opacity(0.0), FadeOut(mca), run_time=0.6)
        mat = lab("mature NGF", BLUE, nm.get_center()[0], nm.get_center()[1], 30)
        self.play(ReplacementTransform(nm, mat), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Outcome(SpokenScene):
    def construct(self):
        cL, cR = -3.2, 3.2
        S5 = 1.0
        DY5 = RTOP + 0.375
        def mem_at(c):
            return Rectangle(width=5.9, height=0.36, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([c, 0, 0])
        def panel(c):
            tA = VGroup(receptor(c - 1.9 - HX, PINK), receptor(c - 1.9 + HX, PINK))
            p = receptor(c, VIOLET, foot=True)
            p.foot.set_fill(VIOLET, 0.9)
            return tA, p
        tAL, pL_ = panel(cL)
        tAR, pR_ = panel(cR)
        head = lab("cultured sympathetic neurons", GREY, 0, 3.45, 22)
        lA = lab("TrkA", PINK, cL - 1.9, -2.35, 24)
        lA2 = lab("TrkA", PINK, cR - 1.9, -2.35, 24)
        lP = lab("p75", VIOLET, cL - 0.7, -1.55, 24)
        lP2 = lab("p75", VIOLET, cR - 0.7, -1.55, 24)
        self.add(mem_at(cL), mem_at(cR), head, tAL, tAR, pL_, pR_, lA, lA2, lP, lP2)
        self.at("uncut")
        pro = dimer(cL + 0.6, DY5 + 0.35, S5, tails=True)
        prl = lab("proNGF", BLUE, cL + 0.6, 3.0, 26)
        self.play(FadeIn(pro, shift=DOWN * 0.2), FadeIn(prl), run_time=0.5)
        self.at("bound")
        self.play(pro.animate.move_to([cL + 0.6, DY5 + 0.0, 0]).shift(UP * 0.0), run_time=0.6)
        self.at("very little")
        vl = lab("very little", PINK, cL - 1.9, 1.95, 24)
        pf = badge(tAL[0].foot.get_center()).scale(0.7).set_opacity(0.35)
        self.play(FadeIn(vl, shift=DOWN * 0.1), FadeIn(pf), run_time=0.5)
        self.at("triggered apoptosis")
        sortL = receptor(cL + 2.3, YELLOW, foot=False)
        self.play(FadeIn(sortL, shift=UP * 0.2), run_time=0.4)
        dead = chip("apoptosis", RED, size=28).move_to([cL + 0.6, -3.2, 0])
        da = arr([cL + 0.3, -1.95, 0], [cL + 0.6, -2.85, 0], RED)
        self.play(pL_.foot.animate.set_stroke(RED).set_fill(RED, 0.9), FadeIn(da), FadeIn(dead, shift=UP * 0.1),
                  run_time=0.6)
        self.at("a partner")
        sl = lab("sortilin", YELLOW, cL + 2.3, -1.8, 24)
        self.play(FadeIn(sl), Indicate(sortL.bar, color=YELLOW, scale_factor=1.1), run_time=0.6)
        self.at("binds the")
        top_r = pro.tails[1].get_top()
        hook = ArcBetweenPoints(top_r, [cL + 2.3, RTOP + 0.05, 0], angle=-PI / 2, color=ORANGE, stroke_width=7)
        self.play(Create(hook), Indicate(pro.tails, color=ORANGE, scale_factor=1.1), run_time=0.7)
        # second, separate neuron of the same kind (right)
        self.at("kept", lead=0.9)
        sortR = receptor(cR + 2.3, YELLOW, foot=False)
        slR = lab("sortilin", YELLOW, cR + 2.3, -1.8, 24)
        mat = dimer(cR - 1.9, DY5 + 0.35, S5)
        ml = lab("mature NGF", BLUE, cR - 1.9, 2.75, 26)
        self.play(FadeIn(sortR), FadeIn(slR), FadeIn(mat), FadeIn(ml), run_time=0.6)
        self.at("the same kind")
        self.play(mat.animate.move_to([cR - 1.9, DY5, 0]), run_time=0.6)
        self.at("alive")
        fL, fR = tAR[0].foot.get_center(), tAR[1].foot.get_center()
        bL, bR = badge(fL), badge(fR)
        ok = chip("survives", GREEN, size=28).move_to([cR - 1.9, -3.2, 0])
        oa = arr([cR - 1.9, -1.95, 0], [cR - 1.9, -2.85, 0], GREEN)
        self.play(FadeIn(bL), FadeIn(bR), FadeIn(oa), FadeIn(ok, shift=UP * 0.1), run_time=0.6)
        self.at("cultured cells")
        sc = lab("shown in cultured cells and rodent injury models", GREY, 0, 3.45, 22)
        self.play(ReplacementTransform(head, sc), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        X = (-4.2, 0.0, 4.2)
        nums = VGroup(*[M(str(i + 1), 44, GREY).move_to([x, 2.9, 0]) for i, x in enumerate(X)])
        self.at("Three things decide")
        self.play(FadeIn(nums, lag_ratio=0.3), run_time=0.8)
        # column 1
        self.at("Was the factor cut")
        h1 = chip("cut or uncut?", ORANGE, size=26).move_to([X[0], 2.9, 0])
        pro = dimer(-5.4, 0.9, 0.9, tails=True)
        mat = dimer(-2.9, 0.9, 0.9)
        ar = arr([-4.45, 0.9, 0], [-3.85, 0.9, 0], GREY)
        l_u = lab("uncut", ORANGE, -5.4, -0.5, 24)
        l_c = lab("cut", BLUE, -2.9, -0.5, 24)
        self.play(ReplacementTransform(nums[0], h1), FadeIn(pro), run_time=0.5)
        self.play(FadeIn(ar), FadeIn(mat), FadeIn(l_u), FadeIn(l_c), run_time=0.6)
        # column 2
        self.at("which receptors does")
        h2 = chip("which receptors?", PINK, size=26).move_to([X[1], 2.9, 0])
        rT = receptor(-0.7, PINK, foot=False, h=2.2).shift(UP * 0.9)
        rP = receptor(0.7, VIOLET, foot=False, h=2.2).shift(UP * 0.9)
        lt, lp = lab("TrkA", PINK, -0.7, -0.5, 24), lab("p75", VIOLET, 0.7, -0.5, 24)
        self.play(ReplacementTransform(nums[1], h2), FadeIn(rT, shift=UP * 0.1), FadeIn(rP, shift=UP * 0.1),
                  FadeIn(lt), FadeIn(lp), run_time=0.8)
        # column 3
        self.at("how much of each")
        h3 = chip("how much of each?", GREY, size=26).move_to([X[2], 2.9, 0])
        def mini(x1, x2, hp, ht):
            base = Line([x1 - 0.45, -0.2, 0], [x2 + 0.45, -0.2, 0], color=GREY, stroke_width=3)
            tl = Rectangle(width=0.42, height=hp, stroke_color=VIOLET, stroke_width=3, fill_color=VIOLET,
                           fill_opacity=0.55).move_to([x1, -0.2 + hp / 2, 0])
            sh = Rectangle(width=0.42, height=ht, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                           fill_opacity=0.55).move_to([x2, -0.2 + ht / 2, 0])
            ll = VGroup(lab("p75", VIOLET, x1, -0.55, 22), lab("TrkA", PINK, x2, -0.55, 22))
            return VGroup(base, tl, sh, ll)
        cA = mini(2.8, 3.55, 1.8, 0.7)
        cB = mini(4.85, 5.6, 0.7, 1.8)
        vs = lab("vs", GREY, 4.2, 0.5, 24)
        cap = lab("ratio changes the response", GREY, 4.2, -1.1, 22)
        self.play(ReplacementTransform(nums[2], h3), FadeIn(cA), run_time=0.8)
        self.play(FadeIn(vs), FadeIn(cB), FadeIn(cap), run_time=0.7)
        self.at("precursor killing")
        note = lab("precursor killing in normal development: less clear", GREY, 0, -3.2, 24)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.at("Cut or uncut")
        res = chip("what the factor says", TEXT, size=32).move_to([0, -2.2, 0])
        arrs = VGroup(arr([X[0], -0.95, 0], [-1.7, -1.85, 0]), arr([X[1], -0.95, 0], [0, -1.85, 0]),
                      arr([X[2], -1.35, 0], [1.7, -1.85, 0]))
        self.play(FadeIn(arrs, lag_ratio=0.2), FadeIn(res, scale=0.9), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Cut or uncut, and which receptors: together set what the factor says."
