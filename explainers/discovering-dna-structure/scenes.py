"""How the DNA model was built (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = DNA bases (the A, T, G, C blocks)
  GREY   = backbones, outlines, structure, labels
  PURPLE = evidence (base amounts, X-ray spots, the facts the model was fitted to)
  TEAL   = sequencing (the copies and the order they reveal)
  YELLOW = the question, the numbers of the opening, the reference sequence
  GREEN  = what a model shows / what held up
  ORANGE = what a model leaves out / not yet proved
  GOLD   = title rule only
Only labelled blocks, bars and arrows. No molecule is drawn. Nothing here is a photograph.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def base(letter, w=0.8, h=0.66, size=30, color=BLUE):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.22)
    return VGroup(box, T(letter, size, TEXT, weight=BOLD).move_to(box))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar_v(x, y0, y1, w=0.16, color=GREY):
    return Rectangle(width=w, height=abs(y1 - y0), stroke_color=color, stroke_width=2,
                     fill_color=color, fill_opacity=0.55).move_to([x, (y0 + y1) / 2, 0])


def tag(text, color, size=26):
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 0.4, height=t.height + 0.26, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=0.12)
    return VGroup(box, t.move_to(box))


class S00Title(TitleCard):
    LESSON = "How the DNA model was built"
    TITLE = "Every DNA model leaves something out"


# ----------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        # --- top: 13 years ---
        hgp = T("HUMAN GENOME PROJECT", 26, GREY).move_to([0, 3.15, 0])
        yrs = T("about 13 years", 52, YELLOW, weight=BOLD).move_to([0, 2.35, 0])
        line = Line([-5, 1.5, 0], [5, 1.5, 0], color=YELLOW, stroke_width=10)
        t0 = T("1990", 24, GREY).move_to([-5, 1.05, 0])
        t1 = T("2003", 24, GREY).move_to([5, 1.05, 0])
        self.at("Human Genome Project")
        self.play(FadeIn(hgp), run_time=0.5)
        self.at("about 13 years")
        self.play(FadeIn(yrs, shift=UP * 0.1), Create(line), FadeIn(t0), run_time=1.2)
        self.play(FadeIn(t1), run_time=0.3)
        # --- genome definition ---
        gdef = T("genome = all the DNA in one set of chromosomes", 28, TEXT).move_to([0, 0.0, 0])
        self.at("A genome is all")
        self.play(FadeIn(gdef, shift=UP * 0.1), run_time=0.7)
        # --- bottom: 525 dollars ---
        lab = T("2022 estimate", 26, GREY).move_to([0, -1.1, 0])
        usd = T("about 525 dollars", 52, YELLOW, weight=BOLD).move_to([0, -1.9, 0])
        sub = T("to read a human-sized genome", 28, TEXT).move_to([0, -2.75, 0])
        self.at("By 2022")
        self.play(FadeIn(lab), run_time=0.4)
        self.at("about 525")
        self.play(FadeIn(usd, shift=UP * 0.1), FadeIn(sub), run_time=0.9)
        # --- the question ---
        q = T("What changed?", 64, YELLOW, weight=BOLD).move_to([0, 0.2, 0])
        self.at("What changed")
        self.play(FadeOut(VGroup(hgp, yrs, line, t0, t1, gdef, lab, usd, sub)), run_time=0.5)
        self.play(FadeIn(q, scale=0.9), run_time=0.6)
        # --- pencil vs DNA ---
        q2 = T("What changed?", 36, YELLOW, weight=BOLD).move_to([0, 3.1, 0])
        body = Rectangle(width=3.0, height=0.7, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.25)
        tip = Triangle(stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.25).rotate(PI / 2 + PI).scale(0.35)
        tip.next_to(body, RIGHT, buff=0)
        pencil = VGroup(body, tip).move_to([-3.4, 0.7, 0])
        plab = T("a pencil", 34, GREEN, weight=BOLD).move_to([-3.4, -0.4, 0])
        psub = T("you can look at it", 28, TEXT).move_to([-3.4, -1.1, 0])
        dbox = RoundedRectangle(corner_radius=0.14, width=3.4, height=0.7, stroke_color=PURPLE, stroke_width=4,
                                fill_color=PURPLE, fill_opacity=0.12).move_to([3.4, 0.7, 0])
        dq = T("?", 30, PURPLE, weight=BOLD).move_to(dbox)
        dlab = T("DNA", 34, PURPLE, weight=BOLD).move_to([3.4, -0.4, 0])
        self.at("Nobody has seen")
        self.play(ReplacementTransform(q, q2), FadeIn(pencil), FadeIn(plab), FadeIn(psub),
                  FadeIn(dbox), FadeIn(dq), FadeIn(dlab), run_time=1.0)
        ev = chip("evidence", PURPLE, size=30).move_to([2.2, -1.5, 0])
        mo = chip("models", PURPLE, size=30).move_to([4.6, -1.5, 0])
        self.at("evidence and models")
        self.play(FadeIn(ev, shift=UP * 0.1), FadeIn(mo, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Models(SpokenScene):
    def construct(self):
        mdef = T("model = a simplified picture that helps explain something real", 28, TEXT).move_to([0, 3.0, 0])
        mdef = fit(mdef, max_w=12.2)
        self.at("A model is")
        self.play(FadeIn(mdef, shift=UP * 0.1), run_time=1.0)

        # four bases
        row = VGroup(*[base(l, w=0.9) for l in "ATGC"]).arrange(RIGHT, buff=0.25).move_to([0, 3.0, 0])
        blab = T("the four bases", 24, GREY).next_to(row, RIGHT, buff=0.4)
        grp = VGroup(row, blab).move_to([0, 3.0, 0])
        self.at("DNA has four bases")
        self.play(FadeOut(mdef), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in row], lag_ratio=0.2), FadeIn(blab), run_time=1.4)

        # ladder (left)
        cx = -3.45
        lb_l, lb_r = cx - 1.05, cx + 1.05
        bl = bar_v(lb_l, 1.5, -1.5)
        br = bar_v(lb_r, 1.5, -1.5)
        rungs = VGroup()
        for y, (a, b) in zip([0.9, 0.0, -0.9], [("A", "T"), ("G", "C"), ("T", "A")]):
            ba = base(a, w=0.95, h=0.7).move_to([cx - 0.475, y, 0])
            bb = base(b, w=0.95, h=0.7).move_to([cx + 0.475, y, 0])
            rungs.add(VGroup(ba, bb))
        ladder = VGroup(bl, br, rungs)
        llab = T("flat ladder model", 28, TEXT, weight=BOLD).move_to([cx, -2.0, 0])
        self.at("A flat ladder model")
        self.play(FadeIn(bl), FadeIn(br), FadeIn(llab), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(r, scale=0.9) for r in rungs], lag_ratio=0.25), run_time=0.9)
        tshow1 = tag("shows: which bases pair up", GREEN, 24).move_to([cx, -2.7, 0])
        self.at("shows which bases pair")
        self.play(FadeIn(tshow1, shift=UP * 0.1), *[Indicate(r, color=GREEN, scale_factor=1.05) for r in rungs], run_time=0.9)
        tout1 = tag("leaves out: the twist", ORANGE, 24).move_to([cx, -3.4, 0])
        self.at("leaves out the twist")
        self.play(FadeIn(tout1, shift=UP * 0.1), run_time=0.7)

        # letter string (right)
        cx2 = 3.45
        letters = VGroup(*[base(l, w=0.62, h=0.62, size=28) for l in "ATTGCC"]).arrange(RIGHT, buff=0.08).move_to([cx2, 0.0, 0])
        slab = T("string of letters", 28, TEXT, weight=BOLD).move_to([cx2, -2.0, 0])
        self.at("A string of letters")
        self.play(FadeIn(slab), LaggedStart(*[FadeIn(b, scale=0.8) for b in letters], lag_ratio=0.15), run_time=1.2)
        tshow2 = tag("shows: base order", GREEN, 24).move_to([cx2, -2.7, 0])
        self.at("shows base order")
        self.play(FadeIn(tshow2, shift=UP * 0.1), run_time=0.7)
        tout2 = tag("leaves out: the shape", ORANGE, 24).move_to([cx2, -3.4, 0])
        self.at("leaves out the shape")
        self.play(FadeIn(tout2, shift=UP * 0.1), run_time=0.7)

        final = T("Every model hides something.", 44, ORANGE, weight=BOLD).move_to([0, 3.0, 0])
        self.at("Every model hides")
        self.play(FadeOut(grp), run_time=0.3)
        self.play(FadeIn(final, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Evidence(SpokenScene):
    def construct(self):
        head = T("three kinds of evidence", 38, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        self.at("three kinds of evidence")
        self.play(Write(head), run_time=1.0)

        def card(cx):
            return RoundedRectangle(corner_radius=0.2, width=6.1, height=5.9, stroke_color=PURPLE, stroke_width=3,
                                    fill_color=PURPLE, fill_opacity=0.06).move_to([cx, -0.15, 0])

        # --- 1: base amounts ---
        c1 = card(-3.3)
        h1 = T("1  Base amounts", 34, PURPLE, weight=BOLD).move_to([-3.3, 2.35, 0])
        self.at("First, base amounts")
        self.play(Create(c1), FadeIn(h1), run_time=0.9)
        sm = T("in a DNA sample", 28, GREY).move_to([-3.3, 1.65, 0])
        self.at("In a DNA sample")
        self.play(FadeIn(sm), run_time=0.5)

        def eq_row(a, b, y):
            ba = base(a, w=1.15, h=0.85, size=38).move_to([-4.55, y, 0])
            ap = T("≈", 56, YELLOW, weight=BOLD).move_to([-3.3, y, 0])
            bb = base(b, w=1.15, h=0.85, size=38).move_to([-2.05, y, 0])
            return VGroup(ba, ap, bb)

        r1 = eq_row("A", "T", 0.55)
        r2 = eq_row("G", "C", -0.85)
        self.at("close to the amount of T")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.8)
        self.at("to C")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.8)
        cl = T("amounts are close", 28, TEXT).move_to([-3.3, -2.0, 0])
        self.play(FadeIn(cl), run_time=0.5)

        # --- 2: X-ray ---
        c2 = card(3.3)
        h2 = T("2  X-ray patterns", 34, PURPLE, weight=BOLD).move_to([3.3, 2.35, 0])
        self.at("ray patterns")
        self.play(Create(c2), FadeIn(h2), run_time=0.9)
        fibre = Rectangle(width=0.5, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([1.15, 1.2, 0])
        flab = T("DNA fibers", 22, GREY).move_to([1.35, 0.25, 0])
        film = Rectangle(width=2.7, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([4.6, 1.2, 0])
        film_lbl = T("spots on film", 22, GREY).move_to([4.6, 0.32, 0])
        sk = T("simplified sketch, not the real pattern", 20, ORANGE).move_to([3.3, -0.12, 0])
        xr = VGroup(*[arr([1.5, 1.2 + dy, 0], [3.1, 1.2 + dy * 1.4, 0], PURPLE, 3, 0.15) for dy in (-0.3, 0, 0.3)])
        self.at("through DNA fibers")
        self.play(FadeIn(fibre), FadeIn(flab), LaggedStart(*[GrowArrow(a) for a in xr], lag_ratio=0.2), run_time=1.0)
        spots = VGroup(*[Dot([4.6 + dx, 1.2 + dy, 0], radius=0.07, color=PURPLE) for dx in (-0.8, 0, 0.8) for dy in (-0.45, 0, 0.45)])
        self.at("make spots on film")
        self.play(FadeIn(film), FadeIn(film_lbl), FadeIn(sk), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(sp, scale=2) for sp in spots], lag_ratio=0.08), run_time=0.9)
        dim_ = DoubleArrow([3.8, 1.65, 0], [3.8, 1.2, 0], color=YELLOW, buff=0, stroke_width=4, tip_length=0.13)
        spc = T("spacing of the spots", 24, YELLOW).move_to([3.3, -0.58, 0])
        self.at("Their spacing")
        self.play(GrowFromCenter(dim_), FadeIn(spc), run_time=0.7)
        # helix width (two parallel bars, not a molecule)
        w1 = bar_v(1.5, -0.8, -1.7, w=0.1)
        w2 = bar_v(3.0, -0.8, -1.7, w=0.1)
        wa = DoubleArrow([1.58, -1.25, 0], [2.92, -1.25, 0], color=YELLOW, buff=0, stroke_width=4, tip_length=0.14)
        wl = T("about 2 nm wide", 26, YELLOW, weight=BOLD).move_to([4.75, -1.25, 0])
        hl = T("a helix, a coil", 24, GREY).move_to([2.25, -2.05, 0])
        self.at("a helix, a coil")
        self.play(FadeIn(hl), FadeIn(w1), FadeIn(w2), run_time=0.6)
        self.at("about 2 nanometers wide")
        self.play(GrowFromCenter(wa), FadeIn(wl), run_time=0.7)
        tg = tag("shape clues, not a photo of the bases", ORANGE, 22)
        tg = fit(tg, max_w=5.6).move_to([3.3, -2.65, 0])
        self.at("It gave shape clues")
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S04Helix(SpokenScene):
    def construct(self):
        head = T("3  Model building", 38, PURPLE, weight=BOLD).move_to([0, 3.15, 0])
        self.at("Third, model building")
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.7)
        e1 = chip("base amounts", PURPLE, size=28).move_to([-4.3, 1.5, 0])
        e2 = chip("X-ray patterns", PURPLE, size=28).move_to([-4.3, 0.3, 0])
        e3 = chip("known chemistry", PURPLE, size=28).move_to([-4.3, -0.9, 0])
        wc = chip("Watson and Crick", YELLOW, size=30).move_to([3.0, 0.3, 0])
        self.at("Watson and Crick")
        self.play(FadeIn(wc, shift=LEFT * 0.2), run_time=0.7)
        arrows = [arr(e.get_right(), wc.get_left() + UP * (0.3 * k), PURPLE, 4, 0.18) for e, k in ((e1, 1), (e2, 0), (e3, -1))]
        self.at("fitted these facts together")
        self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.2) for e in (e1, e2, e3)], lag_ratio=0.2),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.6)

        # --- the model ---
        hd = T("the double helix, 1953", 38, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        bl = bar_v(-1.4, 2.3, -1.3)
        br = bar_v(1.4, 2.3, -1.3)
        rungs = VGroup()
        for y, (a, b) in zip([1.5, 0.5, -0.5], [("A", "T"), ("G", "C"), ("T", "A")]):
            rungs.add(VGroup(base(a, w=1.3, h=0.85, size=36).move_to([-0.65, y, 0]), base(b, w=1.3, h=0.85, size=36).move_to([0.65, y, 0])))
        self.at("the double helix")
        self.play(FadeOut(VGroup(e1, e2, e3, wc, *arrows, head)), run_time=0.5)
        self.play(FadeIn(hd), run_time=0.4)
        self.play(FadeIn(bl, shift=UP * 0.2), FadeIn(br, shift=UP * 0.2), run_time=0.8)
        s1 = T("strand", 24, GREY).move_to([-1.4, 2.65, 0])
        s2 = T("strand", 24, GREY).move_to([1.4, 2.65, 0])
        self.at("two strands coiled")
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.5)
        cwarn = tag("coil left out of this flat drawing", ORANGE, 22).move_to([4.0, 1.9, 0])
        self.at("coiled around each other")
        self.play(FadeIn(cwarn, shift=UP * 0.1), run_time=0.7)
        la = T("backbones\noutside", 28, GREY, weight=BOLD, line_spacing=0.9).move_to([-4.9, 0.5, 0])
        laa = arr([-3.7, 0.5, 0], [-1.55, 0.5, 0], GREY, 4, 0.18)
        self.at("backbones outside")
        self.play(FadeIn(la), GrowArrow(laa), run_time=0.7)
        ra = T("bases inside", 28, BLUE, weight=BOLD).move_to([0, -2.15, 0])
        raa = arr([0, -1.8, 0], [0, -1.0, 0], BLUE, 4, 0.18)
        self.at("bases inside")
        self.play(FadeIn(ra), GrowArrow(raa), LaggedStart(*[FadeIn(r, scale=0.9) for r in rungs], lag_ratio=0.2), run_time=1.2)
        bp = T("base pairing", 32, GREEN, weight=BOLD).move_to([4.3, 0.5, 0])
        bp2 = T("A with T,  G with C", 28, GREEN).move_to([4.3, -0.1, 0])
        self.at("Base pairing is the rule")
        self.play(FadeIn(bp), run_time=0.5)
        self.at("A pairs with T")
        self.play(FadeIn(bp2), Indicate(rungs[0], color=GREEN, scale_factor=1.06), run_time=0.8)
        self.play(Indicate(rungs[1], color=GREEN, scale_factor=1.06), run_time=0.6)
        st = tag("unproved", ORANGE, 32).move_to([0, -2.6, 0])
        self.at("They called the model unproved")
        self.play(FadeOut(cwarn), FadeOut(ra), FadeOut(raa), FadeIn(st, shift=UP * 0.1), run_time=0.7)
        st2 = tag("later tests supported it", GREEN, 32).move_to([0, -2.6, 0])
        self.at("Later tests supported it")
        self.play(ReplacementTransform(st, st2), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    def construct(self):
        # left: the 1977 method
        h = T("DNA sequencing: reading the order of bases", 32, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        h = fit(h, max_w=12.2)
        self.at("Knowing the shape")
        self.play(FadeIn(h, shift=UP * 0.1), run_time=0.8)
        yr = T("1977  Sanger and colleagues", 28, TEAL, weight=BOLD).move_to([-3.4, 2.35, 0])
        self.at("In 1977")
        self.play(FadeIn(yr, shift=UP * 0.1), run_time=0.7)
        seq = "ATGC"
        rows = VGroup()
        x0 = -5.3
        for k in range(4):
            r = VGroup()
            for j in range(k + 1):
                last = (j == k)
                r.add(base(seq[j], w=0.8, h=0.62, size=26, color=TEAL if last else BLUE))
            r.arrange(RIGHT, buff=0.06)
            r.move_to([x0 + r.width / 2, 1.4 - 0.85 * k, 0])
            rows.add(r)
        self.at("It stops copies")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), run_time=1.6)
        t_end = tag("each copy stops at a base", TEAL, 24).move_to([-3.4, -2.2, 0])
        self.at("at each kind of base")
        self.play(FadeIn(t_end, shift=UP * 0.1), run_time=0.6)
        ends = VGroup(*[r[-1] for r in rows])
        self.at("The lengths of the copies")
        self.play(Indicate(ends, color=TEAL, scale_factor=1.12), run_time=1.0)
        out = T("order read:  A T G C", 30, TEAL, weight=BOLD).move_to([-3.4, -2.2, 0])
        ex = T("made-up example, not real data", 22, GREY).move_to([-3.4, -3.0, 0])
        self.at("reveal the order")
        self.play(ReplacementTransform(t_end, out), FadeIn(ex), run_time=0.8)

        # right: the project
        hp = T("Human Genome Project", 28, YELLOW, weight=BOLD).move_to([3.5, 2.35, 0])
        pl = Line([1.2, 1.5, 0], [5.8, 1.5, 0], color=YELLOW, stroke_width=10)
        p0 = T("1990", 24, GREY).move_to([1.2, 1.05, 0])
        p1 = T("2003", 24, GREY).move_to([5.8, 1.05, 0])
        self.at("From 1990 to 2003")
        self.play(FadeIn(hp), Create(pl), FadeIn(p0), FadeIn(p1), run_time=1.2)
        imp = T("mostly improved versions\nof the 1977 method", 26, TEXT, line_spacing=0.9).move_to([3.5, 0.2, 0])
        self.at("mostly used improved versions")
        self.play(FadeIn(imp, shift=UP * 0.1), run_time=0.8)
        ref = chip("reference sequence", YELLOW, size=30).move_to([3.5, -1.2, 0])
        self.at("a reference sequence")
        self.play(FadeIn(ref, scale=0.9), run_time=0.7)
        std = T("a standard to compare against", 26, TEXT).move_to([3.5, -2.1, 0])
        self.at("a standard to compare against")
        self.play(FadeIn(std, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        q = T("So what changed?", 56, YELLOW, weight=BOLD).move_to([0, 3.0, 0])
        self.at("So what changed")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.8)

        def line(txt, col, y):
            c = chip(txt, col, size=28)
            return c.move_to([0, y, 0])

        l1 = line("The double helix model still holds", GREEN, 1.7)
        self.at("The double helix model still holds")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.8)
        l2 = line("Sequencing added the letters, and how they differ between people", TEAL, 0.5)
        l2 = fit(l2, max_w=12.2)
        l2.move_to([0, 0.5, 0])
        self.at("Sequencing added the letters")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.9)
        l3 = line("Reading DNA costs far less", YELLOW, -0.8)
        self.at("reading DNA costs far less")
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=0.7)
        l4 = line("Biologists can compare many people and species", BLUE, -2.3)
        self.at("compare many people")
        self.play(FadeIn(l4, shift=UP * 0.1), Create(arr(l3.get_bottom(), l4.get_top(), GREY, 4, 0.18)), run_time=0.9)
        rule = T("Every model shows some things and hides others.", 34, ORANGE, weight=BOLD)
        rule = fit(rule, max_w=12.2).move_to([0, -3.3, 0])
        self.at("Keep this rule")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Every model shows some things and hides others."
