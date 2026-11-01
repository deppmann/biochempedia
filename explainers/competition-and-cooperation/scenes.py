"""Competition and cooperation: who gets the food, who shares it  (Biochemistrypedia explainer, grade 7 Life Science)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
All shapes are labelled schematic blocks. Cell numbers are NOT counts (a note on screen says so).

COLOR MAP (one color per concept, whole video)
  BLUE    = kind A of paramecium, and members of one species (robins) in the examples
  ORANGE  = kind B of paramecium, and the second animal in the competition sketch
  GREEN   = food and other resources (bacteria, food, water, light, minerals, liquid food)
  TEAL    = cooperation (honeybees, sharing)
  RED     = fight, limits, "not enough", "gone", limiting factors
  YELLOW  = a vocabulary word being defined (chip label)
  VIOLET  = rabbits       PINK = foxes
  GREY    = tubes, outlines, plants, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
VIOLET = "#A78BFA"
PINK = "#E070B8"
TEAL_C = "#3FB8C0"


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tube(cx, cy, w, h, color=GREY):
    return RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.10).move_to([cx, cy, 0])


def slots(cx, cy, w, h, n, seed, dmin, fixed=(), margin=0.4):
    rng = np.random.default_rng(seed)
    pts = [np.array(p, float) for p in fixed]
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        p = np.array([cx + rng.uniform(-w / 2 + margin, w / 2 - margin), cy + rng.uniform(-h / 2 + margin, h / 2 - margin)])
        if all(np.hypot(*(p - q)) > dmin for q in pts):
            pts.append(p)
    return pts


def cell(p, color, s=1.0, ang=0.0):
    e = Ellipse(width=0.8 * s, height=0.46 * s, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.5)
    return e.rotate(ang).move_to([p[0], p[1], 0])


def bee(p, s=1.0, ang=0.0, color=None):
    c = color or TEAL_C
    body = Ellipse(width=0.8 * s, height=0.46 * s, stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.5)
    st = [Line([x * s, -0.2 * s, 0], [x * s, 0.2 * s, 0], stroke_color=BG, stroke_width=4) for x in (-0.12, 0.1)]
    return VGroup(body, *st).rotate(ang).move_to([p[0], p[1], 0])


def bact(p, r=0.1):
    return Dot([p[0], p[1], 0], radius=r, color=GREEN)


def cells_at(pts, color, seed=0, s=1.0):
    rng = np.random.default_rng(seed)
    return [cell(p, color, s, rng.uniform(-0.6, 0.6)) for p in pts]


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Competition and Cooperation"
    TITLE = "Who Gets the Food? Who Shares It?"


# ---------------------------------------------------------------------------------------------
class S01Tube(SpokenScene):
    def construct(self):
        TX, TY, TW, TH = -0.9, -0.2, 7.8, 5.0
        P = slots(TX, TY, TW, TH, 26, 11, 0.92)
        a_pts, b_pts, f_pts = P[0:10], P[10:16], P[16:26]
        year = T("G. F. Gause: counts published 1934", 26, GREY).move_to([-3.9, 3.4, 0])
        note = T("schematic, not real counts", 24, GREY).move_to([4.3, 3.4, 0])
        tb = tube(TX, TY, TW, TH)
        self.at("scientist named")
        self.play(FadeIn(year), FadeIn(tb, scale=0.95), FadeIn(note), run_time=0.9)
        A = cells_at(a_pts, BLUE, 1)
        B = cells_at(b_pts, ORANGE, 2)
        Fd = [bact(p) for p in f_pts]
        chA = chip("kind A", BLUE, size=34).move_to([5.0, 1.5, 0])
        chB = chip("kind B", ORANGE, size=34).move_to([5.0, 0.4, 0])
        self.at("two kinds")
        self.play(*[FadeIn(c, scale=0.6) for c in A[:4] + B[:4]], FadeIn(chA), FadeIn(chB), run_time=0.9)
        lab_p = T("paramecium: one cell, swims in water", 30, TEXT).move_to([TX, -3.2, 0])
        self.at("are tiny")
        self.play(FadeIn(lab_p, shift=UP * 0.1), Indicate(VGroup(*A[:4], *B[:4]), color=YELLOW, scale_factor=1.15), run_time=1.0)
        chF = VGroup(chip("bacteria", GREEN, size=34), T("(their food)", 24, GREEN)).arrange(DOWN, buff=0.12).move_to([5.0, -1.0, 0])
        self.at("ate bacteria")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in Fd], lag_ratio=0.05), FadeIn(chF), run_time=1.0)
        # each kind alone
        self.at("grew well")
        self.play(*[FadeOut(m) for m in (tb, lab_p, chA, chB, chF, *A[:4], *B[:4], *Fd)], run_time=0.5)
        tl = tube(-3.45, -0.5, 5.6, 4.6)
        tr = tube(3.45, -0.5, 5.6, 4.6)
        pl = slots(-3.45, -0.5, 5.6, 4.6, 14, 21, 0.95)
        pr = slots(3.45, -0.5, 5.6, 4.6, 14, 22, 0.95)
        AL = cells_at(pl[:8], BLUE, 3) + [bact(p) for p in pl[8:14]]
        BL = cells_at(pr[:8], ORANGE, 4) + [bact(p) for p in pr[8:14]]
        la = T("kind A alone", 34, BLUE).move_to([-3.45, 2.3, 0])
        lb = T("kind B alone", 34, ORANGE).move_to([3.45, 2.3, 0])
        self.play(FadeIn(tl), FadeIn(tr), FadeIn(la), FadeIn(lb), LaggedStart(*[FadeIn(m, scale=0.4) for m in AL + BL], lag_ratio=0.03), run_time=1.0)
        # together
        self.at("Together")
        self.play(*[FadeOut(m) for m in (tl, tr, la, lb, *AL, *BL)], run_time=0.5)
        tb = tube(TX, TY, TW, TH)
        lt = T("A and B together", 34, TEXT).move_to([TX, 2.85, 0])
        self.play(FadeIn(tb), FadeIn(lt), *[FadeIn(c) for c in A[:4] + B[:4]], *[FadeIn(d) for d in Fd], run_time=0.6)
        self.at("stayed common")
        self.play(*[FadeIn(c, scale=0.4) for c in A[4:10] + B[4:6]], run_time=1.0)
        la2 = T("kind A: common", 30, BLUE).move_to([-3.4, -3.2, 0])
        self.play(FadeIn(la2), run_time=0.4)
        self.at("shrank")
        gone = B[1:5]
        lb2 = T("kind B: a small number", 30, ORANGE).move_to([2.2, -3.2, 0])
        self.play(*[FadeOut(c, shift=DOWN * 0.1) for c in gone], FadeIn(lb2), run_time=1.0)
        # the question
        self.at("the question")
        self.play(*[FadeOut(m) for m in (tb, lt, la2, lb2, year, note, *A[:4], *A[4:10], *B[:1], *B[5:6], *Fd)], run_time=0.5)
        q = T("Why do some living things fight over food,", 46, font=TITLE_FONT).move_to([0, 2.5, 0])
        q2 = T("while others share it?", 46, font=TITLE_FONT).move_to([0, 1.6, 0])
        fit(VGroup(q, q2), max_w=12.0)
        self.at("Why do some")
        self.play(Write(q), run_time=0.9)
        self.play(Write(q2), run_time=0.5)
        c1 = chip("fight over food?", RED, size=44).move_to([-3.4, -1.0, 0])
        c2 = chip("share food?", TEAL_C, size=44).move_to([3.6, -1.0, 0])
        self.at("fight over")
        self.play(FadeIn(c1, scale=0.8), run_time=0.5)
        self.at("share it")
        self.play(FadeIn(c2, scale=0.8), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Compete(SpokenScene):
    def construct(self):
        m = chip("matter", GREEN, size=48).move_to([-3.0, 2.0, 0])
        e = chip("energy", GREEN, size=48).move_to([3.0, 2.0, 0])
        self.at("matter and energy")
        self.play(FadeIn(m, shift=DOWN * 0.2), FadeIn(e, shift=DOWN * 0.2), run_time=0.8)
        food = chip("food", GREEN, size=48).move_to([-4.0, -1.0, 0])
        an = chip("animal", BLUE, size=48).move_to([4.0, -1.0, 0])
        a1 = arr(food.get_right(), an.get_left(), GREEN, w=8, tip=0.3)
        both = T("matter + energy", 34, GREEN).move_to([0, -0.3, 0])
        self.at("Animals get both")
        self.play(FadeIn(food), FadeIn(an), GrowArrow(a1), run_time=0.8)
        self.play(FadeIn(both, shift=DOWN * 0.1), Indicate(VGroup(m, e), color=YELLOW, scale_factor=1.1), run_time=0.8)
        # competition
        self.at("Competition happens")
        self.play(*[FadeOut(x) for x in (m, e, food, an, a1, both)], run_time=0.5)
        term = chip("competition", YELLOW, size=44).move_to([0, 3.0, 0])
        self.play(FadeIn(term, scale=0.8), run_time=0.5)
        x1 = chip("animal", BLUE, size=46).move_to([-4.3, 0.4, 0])
        x2 = chip("animal", ORANGE, size=46).move_to([4.3, 0.4, 0])
        fd = chip("food", GREEN, size=46).move_to([0, 0.4, 0])
        l1 = arr(x1.get_right(), fd.get_left(), GREY, w=7, tip=0.28)
        l2 = arr(x2.get_left(), fd.get_right(), GREY, w=7, tip=0.28)
        self.at("same resource")
        self.play(FadeIn(x1), FadeIn(x2), FadeIn(fd), GrowArrow(l1), GrowArrow(l2), run_time=0.9)
        rs = T("the same resource", 34, GREEN).move_to([0, -0.9, 0])
        self.play(FadeIn(rs), run_time=0.4)
        ne = T("not enough for all", 48, RED).move_to([0, -2.4, 0])
        self.at("not enough")
        self.play(FadeIn(ne, shift=UP * 0.1), Indicate(fd, color=RED, scale_factor=1.2), run_time=0.8)
        # five things animals compete for
        self.at("compete for")
        self.play(*[FadeOut(x) for x in (x1, x2, fd, l1, l2, rs, ne)], run_time=0.5)
        cf = chip("food", GREEN, size=44).move_to([-4.0, 1.6, 0])
        cw = chip("water", GREEN, size=44).move_to([0, 1.6, 0])
        cs = chip("shelter", GREEN, size=44).move_to([4.0, 1.6, 0])
        ct = chip("territory", GREEN, size=44).move_to([-2.2, 0.1, 0])
        cm = chip("mates", GREEN, size=44).move_to([2.2, 0.1, 0])
        self.play(FadeIn(cf, scale=0.8), run_time=0.4)
        self.at("water")
        self.play(FadeIn(cw, scale=0.8), run_time=0.4)
        self.at("shelter")
        self.play(FadeIn(cs, scale=0.8), run_time=0.4)
        self.at("territory")
        self.play(FadeIn(ct, scale=0.8), run_time=0.4)
        self.at("mates")
        self.play(FadeIn(cm, scale=0.8), run_time=0.4)
        # territory
        self.at("Territory is")
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=6.2, height=2.3, stroke_color=GREEN, stroke_width=4),
                             num_dashes=44).move_to([1.6, -2.3, 0])
        owner = chip("animal", BLUE, size=38).move_to([1.6, -2.5, 0])
        tl = T("territory", 28, GREEN).move_to([1.6, -1.55, 0])
        self.play(Create(box), FadeIn(owner), FadeIn(tl), Indicate(ct, color=YELLOW, scale_factor=1.15), run_time=1.0)
        out = chip("other animal", ORANGE, size=30).move_to([-4.3, -2.3, 0])
        self.at("keeps others")
        self.play(FadeIn(out), out.animate.move_to([-3.0, -2.3, 0]), run_time=0.6)
        self.play(out.animate.move_to([-4.3, -2.3, 0]), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Quiet(SpokenScene):
    def construct(self):
        TX, TY, TW, TH = -2.5, -0.4, 7.0, 4.9
        a0, bq, b0 = (TX - 1.6, TY + 0.2), (TX, TY + 0.2), (TX + 1.6, TY + 0.2)
        P = slots(TX, TY, TW, TH, 22, 5, 0.95, fixed=[a0, bq, b0])
        A_pts = [a0] + P[3:7]
        B_pts = [b0] + P[7:11]
        F_pts = P[11:22]
        tb = tube(TX, TY, TW, TH)
        A = cells_at(A_pts, BLUE, 6)
        B = cells_at(B_pts, ORANGE, 7)
        F = [bact(p) for p in F_pts]
        dq = bact(bq, r=0.13)
        title = T("competition is often quiet", 40, font=TITLE_FONT).move_to([0, 3.35, 0])
        self.at("often quiet")
        self.play(FadeIn(tb), *[FadeIn(c) for c in A + B], *[FadeIn(d) for d in F], FadeIn(dq), FadeIn(title), run_time=1.0)
        fw = T("fight", 56, RED).move_to([3.8, 1.6, 0])
        cr = Cross(fw, stroke_color=TEXT, stroke_width=6)
        self.at("Nobody has to")
        self.play(FadeIn(fw), Create(cr), run_time=0.8)
        sb = T("the same bacteria", 36, GREEN).move_to([3.8, 0.1, 0])
        self.at("ate the same")
        self.play(FadeIn(sb, shift=LEFT * 0.1), Indicate(VGroup(*F, dq), color=TEXT, scale_factor=1.6), run_time=1.0)
        gone = T("gone", 36, RED).move_to([bq[0], bq[1] - 0.8, 0])
        self.at("eat")
        self.play(dq.animate.move_to([a0[0] + 0.25, a0[1], 0]).scale(0.5), run_time=0.8)
        self.play(FadeOut(dq), A[0].animate.set_fill(opacity=0.9), run_time=0.3)
        hole = DashedVMobject(Circle(radius=0.3, stroke_color=RED, stroke_width=3), num_dashes=10).move_to([bq[0], bq[1], 0])
        self.at("gone for")
        self.play(Create(hole), FadeIn(gone, shift=DOWN * 0.1), run_time=0.7)
        self.wait(0.4)
        # population
        self.at("population is")
        self.play(*[FadeOut(x) for x in (fw, cr, sb, gone, hole)], run_time=0.4)
        rings = VGroup(*[Circle(radius=0.42, stroke_color=YELLOW, stroke_width=3).move_to(c.get_center()) for c in A])
        pc = chip("population", YELLOW, size=40).move_to([3.8, 1.9, 0])
        pt = VGroup(T("all members of", 30, TEXT), T("one species", 30, BLUE), T("in one area", 30, TEXT)).arrange(DOWN, buff=0.18).move_to([3.8, 0.0, 0])
        self.play(Create(rings), FadeIn(pc), FadeIn(pt), A[0].animate.set_fill(opacity=0.5), run_time=1.0)
        # robins
        self.at("often compete")
        self.play(*[FadeOut(x) for x in (tb, rings, pc, pt, title, *A, *B, *F)], run_time=0.5)
        lawn = Rectangle(width=12.0, height=4.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.10).move_to([0, -0.4, 0])
        ll = T("one lawn", 28, GREY).move_to([-5.0, -2.35, 0])
        r1 = chip("robin", BLUE, size=48).move_to([-4.0, 0.7, 0])
        r2 = chip("robin", BLUE, size=48).move_to([4.0, 0.7, 0])
        wm = chip("worm", GREEN, size=48).move_to([0, -1.1, 0])
        ar1 = arr(r1.get_right(), wm.get_top() + LEFT * 0.4, GREY, w=7, tip=0.28)
        ar2 = arr(r2.get_left(), wm.get_top() + RIGHT * 0.4, GREY, w=7, tip=0.28)
        mem = T("members of one population", 38, BLUE).move_to([0, 3.1, 0])
        self.play(FadeIn(lawn), FadeIn(ll), FadeIn(r1), FadeIn(r2), FadeIn(mem), run_time=0.7)
        self.at("worms")
        self.play(FadeIn(wm), GrowArrow(ar1), GrowArrow(ar2), run_time=0.8)
        # plants
        self.at("Plants compete")
        self.play(*[FadeOut(x) for x in (lawn, ll, r1, r2, wm, ar1, ar2, mem)], run_time=0.5)
        soil = Rectangle(width=11.0, height=2.2, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.18).move_to([0, -2.4, 0])
        sl = T("soil", 26, GREY).move_to([-5.0, -3.2, 0])
        plants = VGroup()
        for x in (-3.4, 3.4):
            stem = Rectangle(width=0.26, height=3.9, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.5).move_to([x, -1.0, 0])
            leaf = Rectangle(width=2.8, height=0.46, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.5).move_to([x, 1.0, 0])
            plants.add(stem, leaf)
        pl = T("plants", 34, TEXT).move_to([0, 1.0, 0])
        self.play(FadeIn(soil), FadeIn(sl), FadeIn(plants), FadeIn(pl), run_time=0.8)
        lc = chip("light", GREEN, size=38).move_to([0, 2.9, 0])
        al = [arr(lc.get_bottom() + LEFT * 0.5, [-2.5, 1.5, 0], GREEN, w=7), arr(lc.get_bottom() + RIGHT * 0.5, [2.5, 1.5, 0], GREEN, w=7)]
        self.at("for light")
        self.play(FadeIn(lc), *[GrowArrow(a) for a in al], run_time=0.7)
        wc = chip("water", GREEN, size=34).move_to([0, -1.9, 0])
        aw = [arr(wc.get_left(), [-3.2, -1.9, 0], GREEN, w=7), arr(wc.get_right(), [3.2, -1.9, 0], GREEN, w=7)]
        self.at("water")
        self.play(FadeIn(wc), *[GrowArrow(a) for a in aw], run_time=0.6)
        mc = chip("minerals", GREEN, size=34).move_to([0, -3.0, 0])
        am = [arr(mc.get_left(), [-3.2, -3.0, 0], GREEN, w=7), arr(mc.get_right(), [3.2, -3.0, 0], GREEN, w=7)]
        self.at("minerals")
        self.play(FadeIn(mc), *[GrowArrow(a) for a in am], run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cooperate(SpokenScene):
    def construct(self):
        CX, CY, CW, CH = 0.0, -0.7, 12.0, 4.6
        colony = tube(CX, CY, CW, CH, TEAL_C)
        px = [(-3.6, -1.5), (0.0, -1.5), (3.6, -1.5)]
        bees_p = slots(CX, CY, CW, CH, 40, 8, 1.05, margin=0.6)
        bees_p = [p for p in bees_p if all(np.hypot(p[0] - q[0], p[1] - q[1]) > 1.5 for q in px)][:24]
        rng = np.random.default_rng(3)
        bees = [bee(p, 1.4, rng.uniform(-0.5, 0.5)) for p in bees_p]
        key = [bee(q, 1.4) for q in px]
        mid = [bee(p, 2.2) for p in ((-3.2, 0.4), (-3.2, -1.6), (0.0, 0.4), (0.0, -1.6), (3.2, 0.4), (3.2, -1.6))]
        self.play(*[FadeIn(b, scale=0.5) for b in mid], run_time=0.8)
        term = chip("cooperation", YELLOW, size=36).move_to([-4.5, 2.9, 0])
        self.at("Cooperation is")
        self.play(FadeIn(term, scale=0.8), run_time=0.5)
        ins = [arr([-4.9, -0.6, 0], [-3.9, -0.1, 0], TEAL_C, w=8), arr([4.9, -0.6, 0], [3.9, -0.1, 0], TEAL_C, w=8)]
        self.at("work together")
        self.play(*[GrowArrow(a) for a in ins], run_time=0.6)
        self.at("honey")
        self.play(*[FadeOut(x) for x in (*mid, *ins)], FadeIn(colony), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in bees + key], lag_ratio=0.03), run_time=1.2)
        cl = T("honeybee colony: tens of thousands of bees", 32, TEAL_C).move_to([0, -3.4, 0])
        self.at("tens of thousands")
        self.play(FadeIn(cl, shift=UP * 0.1), run_time=0.6)
        top = sorted([b for b in bees if b.get_center()[1] > 0.0], key=lambda b: b.get_center()[0])
        b_left = min(top, key=lambda b: abs(b.get_center()[0] + 0.3))
        b_right = min(top, key=lambda b: abs(b.get_center()[0] - 3.9))
        j1 = chip("caring for young", TEAL_C, size=30).move_to([-0.3, 2.9, 0])
        j2 = chip("guarding the hive", TEAL_C, size=30).move_to([3.9, 2.9, 0])
        self.at("different jobs")
        self.play(Indicate(VGroup(*bees[:12]), color=YELLOW, scale_factor=1.2), run_time=0.8)
        self.at("caring for young")
        self.play(FadeIn(j1), Indicate(b_left, color=YELLOW, scale_factor=1.8), run_time=0.7)
        self.at("guarding the hive")
        self.play(FadeIn(j2), Indicate(b_right, color=YELLOW, scale_factor=1.8), run_time=0.7)
        # pass liquid food
        self.at("pass liquid food")
        lf = T("liquid food", 32, GREEN).move_to([0, -3.4, 0])
        self.play(FadeOut(j1), FadeOut(j2), FadeOut(cl), run_time=0.4)
        drop = Dot([px[0][0], px[0][1] + 0.5, 0], radius=0.2, color=GREEN)
        self.play(FadeIn(drop, scale=0.4), FadeIn(lf), run_time=0.4)
        self.play(drop.animate.move_to([px[1][0], px[1][1] + 0.5, 0]), run_time=0.8)
        self.at("bee to bee")
        self.play(drop.animate.move_to([px[2][0], px[2][1] + 0.5, 0]), run_time=0.8)
        self.play(FadeOut(drop), FadeOut(lf), run_time=0.3)
        bars = VGroup()
        for q, h in zip(px, (0.3, 1.5, 0.8)):
            bars.add(Rectangle(width=0.7, height=h, stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=0.5)
                     .move_to([q[0], q[1] + 0.6 + h / 2, 0]))
        ne = T("the shares are not always equal", 34, GREEN).move_to([0, -3.4, 0])
        self.at("not always equal")
        self.play(*[b.animate.set_opacity(0.2) for b in bees], GrowFromEdge(bars, DOWN), FadeIn(ne), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Limits(SpokenScene):
    def construct(self):
        OFF = 3.2
        term = chip("limiting factor", YELLOW, size=40).move_to([-3.2 + OFF, 3.15, 0])
        place = tube(-3.2 + OFF, 0.2, 4.8, 3.6)
        pts = slots(-3.2 + OFF, 0.2, 4.8, 3.6, 8, 31, 1.0)
        pop = cells_at(pts, BLUE, 4)
        pl = T("one species in a place", 30, GREY).move_to([-3.2 + OFF, -2.1, 0])
        self.at("limiting factor")
        self.play(FadeIn(term, scale=0.8), FadeIn(place), *[FadeIn(c) for c in pop], FadeIn(pl), run_time=0.8)
        pr = [arr([-6.3 + OFF, 0.2, 0], [-5.65 + OFF, 0.2, 0], RED, w=9), arr([-0.1 + OFF, 0.2, 0], [-0.75 + OFF, 0.2, 0], RED, w=9),
              arr([-3.2 + OFF, 2.6, 0], [-3.2 + OFF, 2.05, 0], RED, w=9)]
        self.at("limits how many")
        self.play(*[GrowArrow(a) for a in pr], run_time=0.8)
        hm = T("how many can live here?", 34, TEXT).move_to([-3.2 + OFF, -3.1, 0])
        self.play(FadeIn(hm), run_time=0.5)
        left = VGroup(term, place, *pop, pl, *pr, hm)
        bh = chip("biotic factor", YELLOW, size=36).move_to([3.9, 3.1, 0])
        self.at("biotic factor")
        self.play(left.animate.shift(LEFT * OFF), run_time=0.6)
        self.play(FadeIn(bh, scale=0.8), run_time=0.4)
        living = T("a living part", 30, TEXT).move_to([3.9, 2.25, 0])
        self.at("a living part")
        self.play(FadeIn(living), run_time=0.4)
        c1 = chip("food", RED, size=34).move_to([2.6, 1.3, 0])
        c2 = chip("disease", RED, size=34).move_to([5.0, 1.3, 0])
        self.at("like food")
        self.play(FadeIn(c1, scale=0.8), run_time=0.4)
        self.at("disease")
        self.play(FadeIn(c2, scale=0.8), run_time=0.4)
        ah = chip("abiotic factor", YELLOW, size=36).move_to([3.9, 0.0, 0])
        self.at("abiotic factor")
        self.play(FadeIn(ah, scale=0.8), run_time=0.5)
        nl = T("a nonliving part", 30, TEXT).move_to([3.9, -0.85, 0])
        self.at("living part", nth=1)
        self.play(FadeIn(nl), run_time=0.4)
        c3 = chip("water", RED, size=34).move_to([2.7, -1.8, 0])
        c4 = chip("temperature", RED, size=34).move_to([3.9, -2.9, 0])
        self.at("like water")
        self.play(FadeIn(c3, scale=0.8), run_time=0.4)
        self.at("temperature")
        self.play(FadeIn(c4, scale=0.8), run_time=0.4)
        # community
        self.at("A community")
        self.play(*[FadeOut(x) for x in (left, bh, living, c1, c2, ah, nl, c3, c4)], run_time=0.5)
        cm = chip("community", YELLOW, size=40).move_to([0, 3.15, 0])
        area = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=12.2, height=5.4, stroke_color=GREY, stroke_width=3),
                              num_dashes=64).move_to([0, -0.3, 0])
        rp = slots(-3.7, -0.2, 4.6, 3.2, 6, 41, 1.0)
        fp = [(2.9, 0.4), (4.7, 0.4), (3.8, -1.1)]
        rab = cells_at(rp, VIOLET, 5, s=1.3)
        fox = cells_at(fp, PINK, 6, s=2.0)
        rl = T("rabbits", 36, VIOLET).move_to([-3.7, -2.4, 0])
        fl = T("foxes", 36, PINK).move_to([3.7, -2.4, 0])
        self.play(FadeIn(cm, scale=0.8), Create(area), run_time=0.7)
        self.play(*[FadeIn(c) for c in rab + fox], FadeIn(rl), FadeIn(fl), run_time=0.8)
        link = arr([-1.3, -0.1, 0], [1.3, -0.1, 0], GREY, w=7)
        link2 = arr([1.3, -0.6, 0], [-1.3, -0.6, 0], GREY, w=7)
        self.at("interact")
        self.play(GrowArrow(link), GrowArrow(link2), run_time=0.7)
        # disease
        self.at("a disease killed")
        self.play(FadeOut(link), FadeOut(link2), run_time=0.3)
        dz = chip("disease", RED, size=34).move_to([-3.7, 1.9, 0])
        self.play(FadeIn(dz, shift=DOWN * 0.1), run_time=0.4)
        self.play(*[FadeOut(c, shift=DOWN * 0.1) for c in rab[1:5]], run_time=0.9)
        self.at("that eat rabbits")
        eat = arr([-1.5, -0.3, 0], [1.3, -0.3, 0], VIOLET, w=7)
        self.play(GrowArrow(eat), run_time=0.6)
        self.at("less food")
        lessf = T("less food", 38, RED).move_to([3.7, 1.9, 0])
        self.play(FadeIn(lessf, shift=DOWN * 0.1), Indicate(VGroup(*fox), color=RED, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        q = T("Why fight over food, or share it?", 48, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("So why")
        self.play(Write(q), run_time=0.9)
        # row 1: compete
        a = cell((-5.4, 1.5), BLUE, 1.5)
        b = cell((-3.1, 1.5), ORANGE, 1.5)
        f = bact((-4.25, 1.5), r=0.18)
        i1 = VGroup(a, b, f, arr([-4.85, 1.5, 0], [-4.5, 1.5, 0], GREY, w=4, tip=0.14), arr([-3.65, 1.5, 0], [-4.0, 1.5, 0], GREY, w=4, tip=0.14))
        t1 = T("Compete for the same limited resource", 32, TEXT).move_to([1.7, 1.75, 0])
        t1b = T("often without any fight", 28, GREY).move_to([1.7, 1.1, 0])
        self.at("Some compete")
        self.play(FadeIn(i1), FadeIn(t1, shift=LEFT * 0.2), run_time=0.8)
        self.at("without any fight")
        self.play(FadeIn(t1b), run_time=0.6)
        # row 2: cooperate
        bs = [bee((-5.6 + 1.5 * k, -0.2), 1.5) for k in range(3)]
        d = Dot([-5.1, 0.25, 0], radius=0.15, color=GREEN)
        t2 = T("Cooperate: work together", 32, TEXT).move_to([1.7, -0.2, 0])
        self.at("Others cooperate")
        self.play(*[FadeIn(x) for x in bs], FadeIn(t2, shift=LEFT * 0.2), FadeIn(d), run_time=0.7)
        self.play(d.animate.move_to([-3.6, 0.25, 0]), run_time=0.5)
        self.play(FadeOut(d), run_time=0.2)
        # row 3: limits
        box = tube(-4.3, -2.0, 3.6, 1.7)
        pts = [(-5.1, -1.8), (-4.3, -2.3), (-3.5, -1.8), (-3.1, -2.3)]
        dots = cells_at(pts, BLUE, 7, s=0.9)
        pr = [arr([-6.3, -2.0, 0], [-5.85, -2.0, 0], RED, w=7, tip=0.16), arr([-2.3, -2.0, 0], [-2.75, -2.0, 0], RED, w=7, tip=0.16)]
        t3 = T("Limiting factors set how many", 32, TEXT).move_to([1.7, -1.75, 0])
        t3b = T("living and nonliving", 28, GREY).move_to([1.7, -2.4, 0])
        self.at("limiting factors")
        self.play(FadeIn(box), *[FadeIn(c) for c in dots], *[GrowArrow(x) for x in pr], FadeIn(t3, shift=LEFT * 0.2), run_time=0.9)
        self.at("nonliving")
        self.play(FadeIn(t3b), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Compete for limited resources, or cooperate to meet needs."
