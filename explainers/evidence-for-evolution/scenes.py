"""Evidence for evolution: many kinds of evidence, one history  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  ORANGE = sedimentary rock layers
  BLUE   = fossils and bones (leg bones, hip bones)
  YELLOW = dates and time (dated volcanic layers, older/younger arrow)
  PURPLE = the radioactive starting atom (s03) and the dolphin embryo (s05)
  PINK   = the product atom (s03)
  TEAL   = DNA blocks
  RED    = a difference between DNA copies, a gap, a question
  GOLD   = an inserted piece of DNA
  GREEN  = land-walking ancestors, the shared history, the answer
  GREY   = outlines, body outlines, neutral labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#E39B5B"
PURPLE = "#B58CD9"
PINK = "#EE8FB8"


def layer(w, h, color=ORANGE, op=0.28):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op)


def block_row(n, side=0.34, gap=0.05, color=TEAL, red=(), gold=()):
    bl = []
    for i in range(n):
        c = RED if i in red else (GOLD if i in gold else color)
        bl.append(Square(side, stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.45))
    return VGroup(*bl).arrange(RIGHT, buff=gap)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar_chip(text, color, size=24):
    return chip(text, color, size=size, pad=0.14)


class S00Title(TitleCard):
    LESSON = "Evidence for evolution"
    TITLE = "Many kinds of evidence, one history"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        ys = [-0.95, -0.05, 0.85, 1.75]
        stack = VGroup(*[layer(4.8, 0.9).move_to([-3.9, y, 0]) for y in ys])
        for i, l in enumerate(stack):
            l.set_fill(ORANGE, 0.22 + 0.04 * (i % 2))
        stack_lbl = T("rock layers", 28, ORANGE).next_to(stack, UP, buff=0.25)
        place = T("Pakistan and Egypt", 26, GREY).next_to(stack, DOWN, buff=0.2)
        self.at("Rocks in Pakistan and Egypt")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in stack], lag_ratio=0.2), FadeIn(stack_lbl),
                  FadeIn(place), run_time=1.4)
        leg = bar_chip("leg bones", BLUE, 28).move_to(stack[1])
        fl = T("fossil whale", 28, BLUE).move_to([0.0, -0.05, 0])
        self.at("fossil whales with leg bones")
        self.play(FadeIn(leg, scale=0.8), FadeIn(fl), run_time=0.7)
        body = RoundedRectangle(corner_radius=0.6, width=4.8, height=3.2, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.08).move_to([3.9, 0.4, 0])
        blbl = T("living whale", 28, GREY).next_to(body, UP, buff=0.25)
        hip = bar_chip("hip bones", BLUE, 24).move_to(body.get_center() + RIGHT * 1.2 + DOWN * 0.4)
        small = T("small, inside the body", 26, BLUE).next_to(body, DOWN, buff=0.2)
        self.at("Living whales still carry")
        self.play(FadeIn(body), FadeIn(blbl), run_time=0.7)
        self.at("small hip bones")
        self.play(FadeIn(hip, scale=0.8), FadeIn(small), run_time=0.7)
        walk = bar_chip("land mammal", GREEN, 30).move_to([0.0, -3.0, 0])
        q1 = arr([-3.9, -2.05, 0], walk.get_left(), RED, 4)
        q2 = arr([3.9, -2.05, 0], walk.get_right(), RED, 4)
        qm1 = T("?", 36, RED, weight=BOLD).move_to(q1.get_center() + UP * 0.4)
        qm2 = T("?", 36, RED, weight=BOLD).move_to(q2.get_center() + UP * 0.4)
        self.at("related to animals that walked")
        self.play(FadeIn(walk, shift=UP * 0.2), GrowArrow(q1), GrowArrow(q2),
                  FadeIn(qm1), FadeIn(qm2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Layers(SpokenScene):
    def construct(self):
        cx = -3.2
        ys = [-2.2, -0.75, 0.7, 2.15]
        layers = [layer(6.0, 1.3, ORANGE, 0.22 + 0.05 * (i % 2)).move_to([cx, y, 0]) for i, y in enumerate(ys)]
        fos = [bar_chip("fossil", BLUE, 26).move_to(l.get_center() + LEFT * 1.2 * (1 if i % 2 else -1)) for i, l in enumerate(layers)]
        big = bar_chip("fossil", BLUE, 44).move_to([cx, 0.4, 0])
        cap = T("preserved remains or traces", 28, BLUE).next_to(big, DOWN, buff=0.4)
        cap2 = T("of a living thing", 28, BLUE).next_to(cap, DOWN, buff=0.1)
        self.at("A fossil is")
        self.play(FadeIn(big, scale=0.8), FadeIn(cap), FadeIn(cap2), run_time=0.6)
        self.at("builds up in layers")
        self.play(FadeOut(cap), FadeOut(cap2), ReplacementTransform(big, fos[0]), FadeIn(layers[0]), run_time=0.5)
        for i in (1, 2, 3):
            self.play(FadeIn(layers[i], shift=DOWN * 0.3), FadeIn(fos[i]), run_time=0.35)
        sed = T("sedimentary rock", 26, ORANGE).next_to(layers[3], UP, buff=0.12)
        self.add(sed)
        self.at("undisturbed stack")
        nu = T("undisturbed stack", 24, GREY).next_to(layers[0], DOWN, buff=0.1)
        self.play(FadeIn(nu), run_time=0.3)
        self.at("the bottom layer came first")
        first = T("laid down first", 26, YELLOW).move_to([2.0, -2.2, 0])
        self.play(layers[0].animate.set_stroke(YELLOW, 6), FadeIn(first, shift=LEFT * 0.2), run_time=0.5)
        self.at("older")
        ar = arr([0.6, -1.5, 0], [0.6, 2.2, 0], YELLOW, 7)
        old = T("older", 26, YELLOW).move_to([1.6, -1.0, 0])
        young = T("younger", 26, YELLOW).move_to([1.8, 1.9, 0])
        self.play(GrowArrow(ar), FadeIn(old), FadeIn(young), run_time=0.8)
        rd = chip("relative dating", YELLOW, size=32).move_to([4.5, 0.7, 0])
        no = T("an order,", 28).next_to(rd, DOWN, buff=0.35)
        no2 = T("not an age in years", 28).next_to(no, DOWN, buff=0.1)
        self.at("relative dating")
        self.play(FadeIn(rd, scale=0.9), run_time=0.5)
        self.at("an order")
        self.play(FadeIn(no), FadeIn(no2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Dating(SpokenScene):
    def construct(self):
        head = T("an age in years", 36, font=TITLE_FONT).to_edge(UP, buff=0.5)
        self.at("Radioactive dating")
        self.play(Write(head), run_time=1.0)
        # --- ratio bar ---------------------------------------------------------------------
        W, H = 9.0, 1.3
        left, y = -4.5, 0.3
        f = ValueTracker(1.0)  # fraction of starting atom left

        def start_bar():
            w = max(W * f.get_value(), 1e-3)
            return Rectangle(width=w, height=H, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                             fill_opacity=0.55).move_to([left + w / 2, y, 0])

        def prod_bar():
            w = max(W * (1 - f.get_value()), 1e-3)
            r = Rectangle(width=w, height=H, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                          fill_opacity=0.55).move_to([left + W - w / 2, y, 0])
            r.set_opacity(0 if w < 0.02 else 1)
            return r
        sb, pb = always_redraw(start_bar), always_redraw(prod_bar)
        outline = Rectangle(width=W, height=H, stroke_color=GREY, stroke_width=3).move_to([left + W / 2, y, 0])
        mineral = T("a mineral", 26, GREY).next_to(outline, UP, buff=0.25)
        self.at("Certain minerals hold radioactive atoms")
        self.play(FadeIn(outline), FadeIn(mineral), FadeIn(sb), run_time=0.7)
        l_start = bar_chip("starting atom", PURPLE, 28).move_to([-2.6, -1.0, 0])
        self.play(FadeIn(l_start), run_time=0.5)
        self.add(pb)
        self.at("change into other atoms")
        l_prod = bar_chip("product", PINK, 28).move_to([2.9, -1.0, 0])
        self.play(f.animate.set_value(0.65), FadeIn(l_prod), run_time=1.6)
        steady = T("steady rate", 28, TEXT).move_to([0, -2.2, 0])
        self.at("at a steady rate")
        self.play(FadeIn(steady), run_time=0.4)
        self.at("Measuring the starting atom left")
        self.play(Indicate(l_start, color=PURPLE, scale_factor=1.15), run_time=0.8)
        self.at("the product built up")
        self.play(f.animate.set_value(0.4), Indicate(l_prod, color=PINK, scale_factor=1.15), run_time=1.2)
        tm = T("time since the mineral formed", 30, YELLOW).move_to([0, -3.1, 0])
        sk = T("in this sketch", 24, GREY).move_to([left + W - 1.0, y + 1.2, 0])
        self.at("time since the mineral formed")
        self.play(FadeIn(tm, shift=UP * 0.15), FadeIn(sk), run_time=0.6)
        # --- bracketing a fossil ----------------------------------------------------------
        grp = VGroup(outline, mineral, l_start, l_prod, steady, tm, sk, sb, pb)
        self.at("Volcanic layers above and below a fossil")
        sb.clear_updaters(); pb.clear_updaters()
        self.play(FadeOut(grp), run_time=0.6)
        self.remove(sb, pb)
        cx = -2.2
        ash_t = layer(6.6, 1.3, YELLOW, 0.3).move_to([cx, 1.5, 0])
        mid = layer(6.6, 2.0, ORANGE, 0.25).move_to([cx, -0.15, 0])
        ash_b = layer(6.6, 1.3, YELLOW, 0.3).move_to([cx, -1.8, 0])
        fos = bar_chip("fossil", BLUE, 34).move_to(mid)
        t_lbl = T("volcanic layer", 28, YELLOW).move_to(ash_t)
        b_lbl = T("volcanic layer", 28, YELLOW).move_to(ash_b)
        d_t = chip("date", YELLOW, size=28).move_to([cx + 4.4, 1.5, 0])
        d_b = chip("date", YELLOW, size=28).move_to([cx + 4.4, -1.8, 0])
        self.play(FadeIn(mid), FadeIn(fos), run_time=0.5)
        self.play(FadeIn(ash_t, shift=DOWN * 0.2), FadeIn(t_lbl), FadeIn(ash_b, shift=UP * 0.2), FadeIn(b_lbl), run_time=0.8)
        self.at("two dates")
        self.play(FadeIn(d_t), FadeIn(d_b), run_time=0.6)
        br = Brace(VGroup(d_b, d_t), direction=RIGHT, color=GREEN)
        ans = T("the fossil's age", 28, GREEN).next_to(br, RIGHT, buff=0.2)
        ans2 = T("falls between", 28, GREEN).next_to(ans, DOWN, buff=0.1)
        ans2.align_to(ans, LEFT)
        self.at("falls between them")
        self.play(GrowFromCenter(br), FadeIn(ans), FadeIn(ans2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Dna(SpokenScene):
    def construct(self):
        # ---- copying ---------------------------------------------------------------------------
        r0 = block_row(10, 0.5, 0.07).move_to([0.5, 1.8, 0])
        r1 = block_row(10, 0.5, 0.07).move_to([0.5, -0.1, 0])
        r2 = block_row(10, 0.5, 0.07, red=(6,)).move_to([0.5, -2.0, 0])
        l0 = T("DNA", 30, TEAL).next_to(r0, LEFT, buff=0.4)
        l1 = T("copy", 30, TEAL).next_to(r1, LEFT, buff=0.4)
        l2 = T("copy of the copy", 26, TEAL).next_to(r2, LEFT, buff=0.4)
        a1 = arr([0.5, 1.35, 0], [0.5, 0.45, 0], GREY)
        a2 = arr([0.5, -0.55, 0], [0.5, -1.45, 0], GREY)
        self.at("DNA gives a second kind of evidence")
        self.play(FadeIn(r0), FadeIn(l0), run_time=0.7)
        self.at("When DNA is copied")
        self.play(GrowArrow(a1), FadeIn(r1, shift=DOWN * 0.2), FadeIn(l1), run_time=0.8)
        r1b = block_row(10, 0.5, 0.07, red=(6,)).move_to(r1)
        chg = T("a small change", 26, RED).next_to(r1, RIGHT, buff=0.15)
        chg.move_to([r1.get_right()[0] - 1.0, 0.6, 0])
        self.at("small changes sometimes happen")
        self.play(Transform(r1, r1b), FadeIn(chg), run_time=0.8)
        self.at("some are passed on")
        self.play(GrowArrow(a2), FadeIn(r2, shift=DOWN * 0.2), FadeIn(l2), run_time=0.8)
        # ---- two cases ----------------------------------------------------------------------
        old = VGroup(r0, r1, r2, l0, l1, l2, a1, a2, chg)
        self.at("Two species that split")
        self.play(FadeOut(old), run_time=0.6)

        def case(cx, anc_y, reds, title, tcol):
            ra = block_row(8, 0.32, 0.04).move_to([cx - 1.55, -0.6, 0])
            rb = block_row(8, 0.32, 0.04, red=reds).move_to([cx + 1.55, -0.6, 0])
            la = T("species A", 24).next_to(ra, DOWN, buff=0.15)
            lb = T("species B", 24).next_to(rb, DOWN, buff=0.15)
            anc = bar_chip("common ancestor", GREEN, 24).move_to([cx, anc_y, 0])
            ba = Line(anc.get_bottom(), ra.get_top() + UP * 0.05, color=GREEN, stroke_width=4)
            bb = Line(anc.get_bottom(), rb.get_top() + UP * 0.05, color=GREEN, stroke_width=4)
            ti = T(title, 30, tcol).move_to([cx, 3.2, 0])
            return VGroup(ra, rb, la, lb, anc, ba, bb, ti), ti, anc, ba, bb, ra, rb, la, lb

        gL, tiL, ancL, baL, bbL, raL, rbL, laL, lbL = case(-3.3, 1.2, (), "split recently", GREEN)
        # left case: shared blocks first, differences appear later
        rbL_diff = block_row(8, 0.32, 0.04, red=(5,)).move_to(rbL)
        self.at("split from a common ancestor recently")
        self.play(FadeIn(tiL), FadeIn(ancL), Create(baL), Create(bbL), FadeIn(raL), FadeIn(rbL), FadeIn(laL), FadeIn(lbL), run_time=1.2)
        few = T("few differences", 28, RED).move_to([-3.3, -1.8, 0])
        self.at("less time to collect differences")
        self.play(Transform(rbL, rbL_diff), FadeIn(few), run_time=0.8)
        gR, tiR, ancR, baR, bbR, raR, rbR, laR, lbR = case(3.3, 2.4, (1, 2, 4, 6), "split long ago", RED)
        self.at("So, for matching stretches of DNA")
        self.play(FadeIn(tiR), FadeIn(ancR), Create(baR), Create(bbR), FadeIn(raR), FadeIn(rbR), FadeIn(laR), FadeIn(lbR), run_time=1.2)
        many = T("more differences", 28, RED).move_to([3.3, -1.8, 0])
        self.play(FadeIn(many), run_time=0.5)
        note = T("made-up example, not real data", 24, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.at("more similar sequences")
        self.play(Indicate(VGroup(raL, rbL), color=GREEN, scale_factor=1.06), run_time=0.8)
        self.at("a more recent common ancestor")
        self.play(Indicate(ancL, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Fields(SpokenScene):
    def construct(self):
        PW, PH = 6.1, 3.2
        cs = [(-3.15, 1.75), (3.15, 1.75), (-3.15, -1.75), (3.15, -1.75)]

        def panel(c, title, col):
            fr = RoundedRectangle(corner_radius=0.2, width=PW, height=PH, stroke_color=GREY, stroke_width=3).move_to([c[0], c[1], 0])
            tt = T(title, 28, col, weight=BOLD).move_to([c[0], c[1] + PH / 2 - 0.33, 0])
            return fr, tt

        def lines(texts, col=TEXT, size=22, at=(0, 0)):
            g = VGroup(*[T(t, size, col) for t in texts]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            return g.move_to([at[0], at[1], 0])

        # panel 1: fossils
        c1 = cs[0]
        f1, t1 = panel(c1, "Fossils", BLUE)
        st = VGroup(*[layer(1.9, 0.55).move_to([c1[0] - 1.9, c1[1] - 0.55 + 0.57 * i - 0.2, 0]) for i in range(3)])
        lg = bar_chip("leg bones", BLUE, 22).move_to(st[1])
        tx1 = lines(["whale fossils with legs,", "in layers tens of millions", "of years old"], at=(c1[0] + 1.0, c1[1] - 0.2))
        self.at("Legged whale fossils lie in layers")
        self.play(FadeIn(f1), FadeIn(t1), FadeIn(st), run_time=0.6)
        self.play(FadeIn(lg, scale=0.8), FadeIn(tx1), run_time=0.7)

        # panel 2: anatomy
        c2 = cs[1]
        f2, t2 = panel(c2, "Anatomy", BLUE)
        vd = lines(["vestigial: a reduced body part that", "has lost all or most of the job", "it did in ancestors"], size=22, at=(c2[0], c2[1] + 0.4))
        for m in vd:
            m.set_x(c2[0])
        self.at("A vestigial structure")
        self.play(FadeIn(f2), FadeIn(t2), FadeIn(vd), run_time=0.7)
        body = RoundedRectangle(corner_radius=0.35, width=2.7, height=1.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([c2[0] - 1.6, c2[1] - 0.95, 0])
        bl = T("whale", 22, GREY).move_to(body.get_left() + RIGHT * 0.55)
        hip = bar_chip("hip bones", BLUE, 22).move_to(body.get_right() + LEFT * 0.8)
        self.at("small hip bones")
        self.play(FadeIn(body), FadeIn(bl), FadeIn(hip, scale=0.8), run_time=0.7)
        nt = lines(["not useless:", "in males, they anchor", "mating muscles"], col=GREEN, at=(c2[0] + 1.4, c2[1] - 0.95))
        self.at("does not mean useless")
        self.play(FadeIn(nt, shift=UP * 0.1), run_time=0.7)

        # panel 3: embryo
        c3 = cs[2]
        f3, t3 = panel(c3, "Embryos", PURPLE)
        sub = T("pantropical spotted dolphin", 22, GREY).move_to([c3[0], c3[1] + 0.8, 0])
        eb = RoundedRectangle(corner_radius=0.35, width=1.8, height=1.0, stroke_color=PURPLE, stroke_width=3,
                              fill_color=PURPLE, fill_opacity=0.18).move_to([c3[0] - 1.15, c3[1] - 0.3, 0])
        el = T("embryo", 22, PURPLE).move_to([c3[0] - 0.55, c3[1] - 1.05, 0])
        bud = Rectangle(width=0.5, height=0.3, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                        fill_opacity=0.9).move_to([eb.get_left()[0] - 0.25, eb.get_bottom()[1] + 0.3, 0])
        bud_lbl = T("hind-limb bud", 22, PURPLE).move_to([c3[0] - 1.95, c3[1] + 0.42, 0])
        et = lines(["buds stop growing", "and break down", "around the fifth week"], at=(c3[0] + 1.45, c3[1] - 0.3))
        et.set_x(c3[0] + 1.45)
        self.at("spotted dolphin embryos")
        self.play(FadeIn(f3), FadeIn(t3), FadeIn(sub), FadeIn(eb), FadeIn(el), run_time=0.7)
        self.at("hindlimb")
        self.play(FadeIn(bud, shift=RIGHT * 0.3), FadeIn(bud_lbl), run_time=0.6)
        self.at("break down")
        self.play(FadeIn(et), run_time=0.5)
        self.play(bud.animate.scale(0.05).set_opacity(0), FadeOut(bud_lbl), run_time=1.2)

        # panel 4: DNA
        c4 = cs[3]
        f4, t4 = panel(c4, "DNA", TEAL)
        rw = block_row(8, 0.3, 0.04, gold=(4,)).move_to([c4[0] + 0.7, c4[1] + 0.3, 0])
        rh = block_row(8, 0.3, 0.04, gold=(4,)).move_to([c4[0] + 0.7, c4[1] - 0.4, 0])
        lw = T("whales", 22).next_to(rw, LEFT, buff=0.25)
        lh = T("hippos", 22).next_to(rh, LEFT, buff=0.25)
        ins = T("insertion at the same spot", 22, GOLD).move_to([c4[0], c4[1] - 1.1, 0])
        self.at("DNA insertions at the same spots")
        self.play(FadeIn(f4), FadeIn(t4), FadeIn(rw), FadeIn(rh), FadeIn(lw), FadeIn(lh), run_time=0.8)
        self.play(FadeIn(ins), Indicate(VGroup(rw[4], rh[4]), color=GOLD, scale_factor=1.3), run_time=0.8)
        self.at("They share a common ancestor")
        ca = T("a common ancestor", 24, GREEN).move_to(ins)
        self.play(FadeOut(ins), FadeIn(ca), Indicate(VGroup(rw, rh), color=GREEN, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        names = [("Fossils", BLUE), ("Anatomy", BLUE), ("Embryos", PURPLE), ("DNA", TEAL)]
        chips = [chip(n, c, size=34).move_to([-4.6, 2.25 - 1.25 * i, 0]) for i, (n, c) in enumerate(names)]
        self.at("Each field could have contradicted")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chips], lag_ratio=0.25), run_time=1.5)
        qs = [T("?", 34, RED, weight=BOLD).next_to(c, RIGHT, buff=0.4) for c in chips]
        self.play(*[FadeIn(q) for q in qs], run_time=0.5)
        box = RoundedRectangle(corner_radius=0.2, width=6.0, height=4.0, stroke_color=GREEN, stroke_width=4,
                               fill_color=GREEN, fill_opacity=0.1).move_to([2.7, 0.375, 0])
        arrs = [arr(c.get_right() + RIGHT * 0.1, [box.get_left()[0] - 0.1, 0.375 + (1.5 - i) * 0.7, 0], GREEN, 4)
                for i, c in enumerate(chips)]
        self.at("For whales, they agree")
        self.play(*[FadeOut(q) for q in qs], FadeIn(box), *[GrowArrow(a) for a in arrs], run_time=1.0)
        ind = T("independent kinds of evidence", 28, TEXT).move_to([2.7, 1.9, 0])
        self.at("independent kinds of evidence")
        self.play(FadeIn(ind), run_time=0.6)
        hist = T("one history of", 38, GREEN, weight=BOLD).move_to([2.7, 0.8, 0])
        hist2 = T("common descent", 38, GREEN, weight=BOLD).next_to(hist, DOWN, buff=0.15)
        self.at("one history of common descent")
        self.play(FadeIn(hist), FadeIn(hist2), run_time=0.8)
        th = chip("theory: a well-tested explanation", YELLOW, size=26).move_to([2.7, -2.0, 0])
        self.at("theory of evolution")
        self.play(FadeIn(th, shift=UP * 0.15), run_time=0.7)
        fin = T("Whales descend from ancestors that walked on land", 36, GREEN, weight=BOLD)
        fit(fin, max_w=12.0)
        fin.move_to([0, -3.25, 0])
        self.at("Whales descend from ancestors")
        self.play(FadeIn(fin, shift=UP * 0.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Independent kinds of evidence point to one history of common descent."
