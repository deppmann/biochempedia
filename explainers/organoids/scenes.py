"""Organoids: self-organizing tissue, measured against fetal cortex  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = the starting skin cell (fibroblast)
  YELLOW = the four reprogramming factors
  TEAL   = pluripotent stem cells (and the ball of them before it organizes)
  BLUE   = radial glia / dividing progenitor zones
  PURPLE = intermediate progenitors
  GREEN  = early neurons
  RED    = limits: what dies, what is wrong, what is not modelled
  WHITE  = nuclei (TEXT colour)
  GREY   = outlines, gel, medium, tissue edges, controls and structure
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def cell(r, color, nuc=True):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)
    g = VGroup(body)
    if nuc:
        g.add(Circle(radius=r * 0.38, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.6))
    return g


def blob(R, center=ORIGIN, color=GREY, wob=0.09):
    f = lambda t: R * (1 + wob * np.sin(5 * t) + wob * 0.55 * np.sin(8 * t + 1.0)) * np.array([np.cos(t), np.sin(t), 0])
    b = ParametricFunction(f, t_range=[0, TAU], stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.16)
    return b.move_to(center)


def zones(center, R, scale):
    """three small blue progenitor zones inside a tissue of radius R."""
    offs = [(-0.38, 0.30), (0.40, 0.38), (0.0, -0.42)]
    return VGroup(*[Circle(radius=R * 0.30 * scale, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
                    .move_to(center + np.array([R * x, R * y, 0])) for x, y in offs])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def ghost(r, center, color):
    c = DashedVMobject(Circle(radius=r, stroke_color=color, stroke_width=3), num_dashes=24)
    return c.move_to(center)


def strike(mob, color=RED):
    return Line(mob.get_corner(DL) + 0.05 * UR, mob.get_corner(UR) - 0.05 * UR, color=color, stroke_width=5)


class S00Title(TitleCard):
    LESSON = "Brains in a Dish: Stem Cells and Organoids"
    TITLE = "Self-Organizing Tissue, Measured Against Fetal Cortex"


# ---------------------------------------------------------------------------------------------
class S01Skin(SpokenScene):
    """skin cell -> ? -> folded tissue; patient vs control progenitor zones; how far can it be trusted."""

    def construct(self):
        skin = cell(1.25, ORANGE).move_to([-4.3, 0.4, 0])
        skin_l = T("skin cells", 28, ORANGE).next_to(skin, DOWN, buff=0.3)
        qbox = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=3.6, height=3.4, stroke_color=GREY, stroke_width=3), num_dashes=40)
        qbox.move_to([3.3, 0.4, 0])
        qm = T("?", 90, GREY, weight=BOLD).move_to(qbox)
        a1 = arr([-2.7, 0.4, 0], [1.3, 0.4, 0], GREY)
        self.play(FadeIn(skin), FadeIn(skin_l), run_time=0.6)
        self.play(GrowArrow(a1), FadeIn(qbox), FadeIn(qm), run_time=0.7)

        self.at("grew")
        tis = blob(1.8, [3.3, 0.4, 0])
        tis_l = T("brain-like tissue in a dish", 28).move_to([3.3, -2.0, 0])
        self.play(FadeOut(qbox), FadeOut(qm), FadeIn(tis, scale=0.8), run_time=0.8)
        self.play(FadeIn(tis_l), run_time=0.4)

        self.at("a person with severe")
        pat_l = VGroup(T("a person with", 28, ORANGE), T("severe microcephaly", 28, ORANGE)).arrange(DOWN, buff=0.1).move_to([-4.3, -2.2, 0])
        self.play(FadeTransform(skin_l, pat_l), run_time=0.7)

        self.at("The zones of dividing")
        patient = blob(1.9, [-3.3, 0.5, 0])
        control = blob(1.9, [3.3, 0.5, 0])
        zp = zones(np.array([-3.3, 0.5, 0]), 1.9, 0.62)
        zc = zones(np.array([3.3, 0.5, 0]), 1.9, 1.0)
        zl = T("dividing progenitor zones", 28, BLUE).move_to([0, 3.1, 0])
        self.play(FadeOut(skin), FadeOut(pat_l), FadeOut(a1), FadeOut(tis_l),
                  ReplacementTransform(tis, control), FadeIn(patient, scale=0.9), run_time=1.0)
        self.play(FadeIn(zc, scale=0.5), FadeIn(zp, scale=0.5), FadeIn(zl), run_time=0.8)
        lp = T("patient", 28, ORANGE).move_to([-3.3, -1.9, 0])
        lc = T("control", 28, GREY).move_to([3.3, -1.9, 0])
        self.play(FadeIn(lp), FadeIn(lc), run_time=0.5)

        self.at("smaller than in tissue")
        self.play(Indicate(zp, color=BLUE, scale_factor=1.2), run_time=0.9)

        self.at("how far can")
        q = T("How far can the model be trusted?", 34).move_to([0, -3.1, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Reset(SpokenScene):
    """skin cell + four factors -> pluripotent cell that carries the patient's genome."""

    def construct(self):
        skin = cell(1.3, ORANGE).move_to([-4.8, 0.1, 0])
        skin_l = T("skin cell", 28, ORANGE).next_to(skin, DOWN, buff=0.3)
        tgt_pos = np.array([4.8, 0.1, 0])
        gh = ghost(1.3, tgt_pos, TEAL)
        gh_l = T("embryonic state", 28, TEAL).move_to([4.8, -1.8, 0])
        self.play(FadeIn(skin), FadeIn(skin_l), run_time=0.6)
        self.at("embryonic state")
        self.play(FadeIn(gh), FadeIn(gh_l), run_time=0.7)

        self.at("Four transcription factors")
        names = ["Oct4", "Sox2", "Klf4", "c-Myc"]
        chips = VGroup(*[chip(n, YELLOW, 28) for n in names]).arrange(RIGHT, buff=0.3).move_to([0, 2.7, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in chips], lag_ratio=0.25), run_time=1.4)

        self.at("proteins that bind")
        expl = T("proteins that bind DNA, turning genes on or off", 26, GREY).move_to([0, 1.7, 0])
        self.play(FadeIn(expl), run_time=0.6)

        self.at("In human skin cells")
        a = arr([-3.0, 0.1, 0], [3.0, 0.1, 0], YELLOW)
        self.play(GrowArrow(a), run_time=0.6)
        self.at("induced pluripotent")
        ips = cell(1.3, TEAL).move_to(tgt_pos)
        ips_l = VGroup(T("induced pluripotent", 28, TEAL), T("stem cell", 28, TEAL)).arrange(DOWN, buff=0.08).move_to([4.8, -2.0, 0])
        self.play(ReplacementTransform(skin.copy(), ips), FadeOut(gh), FadeTransform(gh_l, ips_l), run_time=1.2)

        self.at("every cell type")
        every = T("able to give rise to every cell type of the body", 26, TEAL).move_to([0, -3.2, 0])
        self.play(FadeIn(every), run_time=0.6)

        self.at("carries the patient's")
        gen = T("carries the patient's whole genome, mutation included", 26, TEAL).move_to([0, -3.2, 0])
        self.play(FadeOut(every), run_time=0.3)
        self.play(FadeIn(gen), Indicate(ips, color=TEAL, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
N_CELLS = 34
BALL_C = np.array([0.0, 0.25, 0.0])


def ball_points():
    k = np.arange(N_CELLS)
    r = 1.85 * np.sqrt((k + 0.5) / N_CELLS)
    th = k * 2.39996
    return [BALL_C + np.array([ri * np.cos(t), ri * np.sin(t), 0]) for ri, t in zip(r, th)]


def organized():
    """ring positions + colors for the same 34 cells, assigned by ball radius (center cells -> inner ring)."""
    bp = ball_points()
    order = sorted(range(N_CELLS), key=lambda i: np.linalg.norm(bp[i] - BALL_C))
    plan = [(10, 0.95, BLUE), (10, 1.55, PURPLE), (14, 2.15, GREEN)]
    out, s = {}, 0
    for n, rad, col in plan:
        grp = order[s:s + n]
        s += n
        grp = sorted(grp, key=lambda i: np.arctan2(bp[i][1] - BALL_C[1], bp[i][0] - BALL_C[0]))
        off = 0.3 if rad < 1.2 else 0.1
        for j, i in enumerate(grp):
            a = off + TAU * j / n
            out[i] = (BALL_C + rad * np.array([np.cos(a), np.sin(a), 0]), col)
    return out


class S03Organize(SpokenScene):
    """scattered cells -> ball -> gel droplet -> spinning flask -> the cells arrange themselves."""

    def construct(self):
        rng = np.random.default_rng(4)
        bp = ball_points()
        scat = []
        for i in range(N_CELLS):
            while True:
                p = np.array([rng.uniform(-5.6, 5.6), rng.uniform(-2.6, 3.1), 0])
                if all(np.linalg.norm(p - q) > 0.7 for q in scat):
                    break
            scat.append(p)
        dots = VGroup(*[Circle(radius=0.26, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to(p) for p in scat])
        lab = T("stem cells", 30, TEAL).move_to([0, -3.3, 0])
        self.play(FadeIn(dots, lag_ratio=0.05), FadeIn(lab), run_time=1.0)

        self.at("gathered into a ball")
        lab2 = T("a ball of cells", 30, TEAL).move_to([0, -3.3, 0])
        self.play(*[d.animate.move_to(bp[i]) for i, d in enumerate(dots)], FadeTransform(lab, lab2), run_time=1.2)

        self.at("steered toward neural")
        lab3 = T("steered toward neural tissue", 30).move_to([0, -3.3, 0])
        self.play(FadeTransform(lab2, lab3), run_time=0.6)

        self.at("droplet of gel")
        gel = Circle(radius=2.55, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to(BALL_C)
        gel_l = T("droplet of gel", 30, GREY).move_to([0, -3.3, 0])
        self.play(FadeIn(gel, scale=1.15), FadeTransform(lab3, gel_l), run_time=0.9)
        self.bring_to_front(dots)

        self.at("spinning flask")
        arcs = VGroup(*[Arc(radius=2.95, start_angle=s, angle=PI / 2.2, arc_center=BALL_C, stroke_color=GREY, stroke_width=6)
                        .add_tip(tip_length=0.28) for s in (0.4, 0.4 + PI)])
        fl_l = T("spinning flask: moving medium brings oxygen, nutrients", 28, GREY).move_to([0, -3.3, 0])
        fl_l.set_width(min(fl_l.width, 11.5)).move_to([0, -3.3, 0])
        self.play(FadeIn(arcs), FadeTransform(gel_l, fl_l), run_time=0.6)
        self.play(Rotating(arcs, angle=TAU * 0.9, about_point=BALL_C, rate_func=linear, run_time=2.2))

        self.at("arrange themselves")
        org = organized()
        cav = Circle(radius=0.55, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(BALL_C)
        anims = []
        for i, d in enumerate(dots):
            pos, col = org[i]
            anims.append(d.animate.move_to(pos).set_stroke(col).set_fill(col, 0.4))
        sa = T("the cells arrange themselves", 30).move_to([0, -3.3, 0])
        self.play(FadeOut(arcs), FadeTransform(fl_l, sa), *anims, run_time=2.0)
        self.play(FadeIn(cav, scale=0.4), run_time=0.5)

        self.at("idea behind every")
        so = T("self-organization", 40, font=TITLE_FONT).move_to([0, -3.3, 0])
        self.play(FadeTransform(sa, so), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Right(SpokenScene):
    """cross-section: radial glia around a cavity (nuclei move), intermediate progenitors, early neurons."""

    def construct(self):
        # carry-over from scene three, rebuilt in the same place
        org = organized()
        old = VGroup(Circle(radius=2.55, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14).move_to(BALL_C),
                     *[Circle(radius=0.26, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.4).move_to(p) for p, c in org.values()],
                     Circle(radius=0.55, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(BALL_C))
        self.add(old)

        C = BALL_C
        cav = Circle(radius=0.75, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(C)
        glia, nuclei, angs = VGroup(), VGroup(), []
        for j in range(12):
            a = TAU * j / 12 + 0.1
            e = Ellipse(width=0.38, height=1.0, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35)
            e.rotate(a - PI / 2).move_to(C + 1.3 * np.array([np.cos(a), np.sin(a), 0]))
            glia.add(e)
            angs.append(a)
        ips = VGroup(*[Circle(radius=0.28, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.4)
                       .move_to(C + 2.15 * np.array([np.cos(a), np.sin(a), 0])) for a in [TAU * j / 14 + 0.05 for j in range(14)]])
        neu = VGroup(*[Circle(radius=0.28, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4)
                       .move_to(C + 2.8 * np.array([np.cos(a), np.sin(a), 0])) for a in [TAU * j / 18 + 0.02 for j in range(18)]])
        for j, a in enumerate(angs):
            nuclei.add(Circle(radius=0.085, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(C + 1.3 * np.array([np.cos(a), np.sin(a), 0])))
        new = VGroup(cav, glia, ips, neu)
        self.at("regions form")
        self.play(FadeOut(old), FadeIn(new), run_time=0.8)
        shift = np.array([-2.6, -0.25, 0])
        self.play(new.animate.shift(shift), run_time=0.9)
        cen = lambda: cav.get_center()

        sw = lambda m, c: VGroup(m, c)
        leg_x = 1.2
        rows = [("radial glia", BLUE, 1.9), ("intermediate progenitors", PURPLE, 0.7), ("early neurons", GREEN, -0.5)]
        legs = []
        for name, col, y in rows:
            if name == "radial glia":
                sh = Ellipse(width=0.34, height=0.7, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35)
            else:
                sh = Circle(radius=0.22, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.4)
            sh.move_to([leg_x, y, 0])
            tx = T(name, 28, col).next_to(sh, RIGHT, buff=0.3)
            legs.append(VGroup(sh, tx))

        self.at("surround a")
        self.play(FadeIn(legs[0], shift=LEFT * 0.2), Indicate(glia, color=BLUE, scale_factor=1.06), run_time=0.9)
        self.at("cavity")
        cav_t = T("cavity", 22, GREY).move_to(cav.get_center())
        self.play(FadeIn(cav_t), run_time=0.5)

        self.at("Their nuclei")
        ph = ValueTracker(0)
        ph.add_updater(lambda m, dt: m.increment_value(dt * 2.4))
        self.add(ph)
        for j, n in enumerate(nuclei):
            a = angs[j]
            n.add_updater(lambda m, j=j, a=a: m.move_to(cen() + (1.3 + 0.27 * np.sin(ph.get_value() + j * 0.8)) * np.array([np.cos(a), np.sin(a), 0])))
        self.play(FadeIn(nuclei), run_time=0.5)

        self.at("Beyond them")
        self.play(FadeIn(legs[1], shift=LEFT * 0.2), Indicate(ips, color=PURPLE, scale_factor=1.05), run_time=0.9)
        self.at("further out")
        self.play(FadeIn(legs[2], shift=LEFT * 0.2), Indicate(neu, color=GREEN, scale_factor=1.04), run_time=0.9)

        self.at("comparison with developing")
        rule = Line([leg_x - 0.3, -1.4, 0], [6.1, -1.4, 0], color=GREY, stroke_width=2)
        t1 = T("The same broad classes are", 28).move_to([3.2, -2.0, 0])
        t2 = T("found in developing human cortex", 28).move_to([3.2, -2.6, 0])
        VGroup(t1, t2).set_width(min(max(t1.width, t2.width), 5.2))
        t1.move_to([3.4, -2.0, 0]); t2.move_to([3.4, -2.6, 0])
        self.play(Create(rule), FadeIn(t1), FadeIn(t2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Limits(SpokenScene):
    """four panels: no vessels / subtypes blur / stress genes / early and mid-fetal only."""

    def panel(self, cx, cy):
        return RoundedRectangle(corner_radius=0.2, width=6.0, height=3.2, stroke_color=GREY, stroke_width=2).set_stroke(opacity=0.6).move_to([cx, cy, 0])

    def construct(self):
        P = {1: (-3.2, 1.75), 2: (3.2, 1.75), 3: (-3.2, -1.7), 4: (3.2, -1.7)}
        frames = {k: self.panel(*v) for k, v in P.items()}
        heads = {2: T("subtypes blur", 28).move_to([P[2][0] - 1.5, P[2][1] + 1.1, 0]),
                 3: T("stress genes", 28).move_to([P[3][0] - 1.6, P[3][1] + 1.1, 0]),
                 4: T("what organoids model", 28).move_to([P[4][0], P[4][1] + 1.15, 0])}
        cx, cy = P[1]
        vc = chip("blood vessels", GREY, 24).move_to([cx - 1.5, cy + 1.05, 0])
        disc = Circle(radius=0.95, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to([cx - 1.6, cy - 0.45, 0])
        self.at("The match has limits")
        self.play(LaggedStart(*[Create(f) for f in frames.values()], lag_ratio=0.1), FadeIn(vc), FadeIn(disc),
                  *[FadeIn(h) for h in heads.values()], run_time=1.0)

        # panel 1: no vessels, center dies
        cx, cy = P[1]
        vx = strike(vc)
        self.at("no blood vessels")
        self.play(Create(vx), run_time=0.7)
        self.at("center of a large")
        core = Circle(radius=0.5, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.55).move_to(disc)
        cl = T("center often dies", 28, RED).move_to([cx + 1.4, cy - 0.45, 0])
        self.play(GrowFromCenter(core), FadeIn(cl), run_time=0.9)

        # panel 2: subtypes blur
        cx, cy = P[2]
        oc = cell(0.42, GREEN, nuc=False).move_to([cx - 2.0, cy - 0.35, 0])
        oc_l = T("organoid cell", 22, GREEN).next_to(oc, DOWN, buff=0.15)
        subs = VGroup(*[chip(f"subtype {s}", GREY, 22, pad=0.1) for s in "ABC"]).arrange(DOWN, buff=0.14).move_to([cx + 1.6, cy - 0.45, 0])
        ars = VGroup(*[arr(oc.get_right() + RIGHT * 0.1, s.get_left() + LEFT * 0.05, GREY, 4, 0.18) for s in subs])
        self.at("Finer cell subtypes")
        self.play(FadeIn(oc), FadeIn(oc_l), run_time=0.7)
        self.at("about equally")
        self.play(FadeIn(subs), LaggedStart(*[GrowArrow(a) for a in ars], lag_ratio=0.15), run_time=1.0)

        # panel 3: stress genes
        cx, cy = P[3]
        sch = T("schematic", 22, GREY).move_to([cx + 2.2, cy + 1.1, 0])
        base = cy - 0.75
        xs = [cx - 2.0, cx, cx + 2.0]
        hs = [0.7, 1.5, 0.65]
        cols = [GREY, RED, RED]
        names = ["fetal cortex", "organoid", "transplanted"]
        bars = [Rectangle(width=0.8, height=hs[i], stroke_color=cols[i], stroke_width=3, fill_color=cols[i], fill_opacity=0.45)
                .move_to([xs[i], base + hs[i] / 2, 0]) for i in range(3)]
        bl = [T(names[i], 22, GREY).move_to([xs[i], base - 0.35, 0]) for i in range(3)]
        ref = DashedVMobject(Line([xs[0] - 0.5, base + hs[0], 0], [xs[2] + 0.7, base + hs[0], 0], color=GREY, stroke_width=3), num_dashes=24)
        self.at("Stress genes")
        self.play(FadeIn(sch), FadeIn(ref), FadeIn(bl[0]), run_time=0.8)
        self.play(GrowFromEdge(bars[1], DOWN), FadeIn(bl[1]), run_time=0.8)
        self.at("fell after transplant")
        b3 = Rectangle(width=0.8, height=hs[1], stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.45).move_to([xs[2], base + hs[1] / 2, 0])
        self.add(b3)
        self.play(FadeIn(bl[2]), Transform(b3, bars[2]), run_time=1.0)

        # panel 4: stage
        cx, cy = P[4]
        w = [1.6, 1.6, 2.2]
        x0 = cx - sum(w) / 2
        segs, lab4 = [], []
        names4 = ["early fetal", "mid-fetal", "mature brain"]
        cols4 = [TEAL, TEAL, GREY]
        xx = x0
        for i in range(3):
            r = Rectangle(width=w[i], height=0.8, stroke_color=cols4[i], stroke_width=3, fill_color=cols4[i], fill_opacity=0.4 if i < 2 else 0.1)
            r.move_to([xx + w[i] / 2, cy - 0.25, 0])
            segs.append(r)
            lab4.append(T(names4[i], 22, cols4[i] if i < 2 else GREY).move_to(r))
            xx += w[i]
        self.at("model early")
        self.play(FadeIn(segs[0]), FadeIn(lab4[0]), FadeIn(segs[1]), FadeIn(lab4[1]), run_time=1.0)
        self.at("not a mature")
        nm = T("not modelled", 22, RED).move_to([segs[2].get_center()[0], cy - 1.0, 0])
        self.play(FadeIn(segs[2]), FadeIn(lab4[2]), segs[2].animate.set_stroke(RED), run_time=0.7)
        self.play(FadeIn(nm), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """four candidate causes -> lines by batch -> gene back -> the rule."""

    def tissue(self, c, R, zs):
        c = np.array(c, float)
        d = Circle(radius=R, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.16).move_to(c)
        return VGroup(d, zones(c, R * 1.1, zs))

    def construct(self):
        pat = self.tissue([-3.9, 0.3, 0], 1.7, 0.62)
        pat_l = T("patient: smaller zones", 28, ORANGE).move_to([-3.9, -2.4, 0])
        self.play(FadeIn(pat), FadeIn(pat_l), run_time=0.7)

        causes = ["the gene", "the rest of the person's genes", "a quirk of one cell line", "a bad batch"]
        chips = VGroup(*[chip(c, GREY if i else YELLOW, 26) for i, c in enumerate(causes)]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        chips.move_to([3.0, 0.3, 0])
        ars = [arr([chips[i].get_left()[0] - 0.1, chips[i].get_center()[1], 0], [-2.1, 0.3 + (chips[i].get_center()[1] - 0.3) * 0.35, 0],
                   GREY, 3, 0.18) for i in range(4)]
        for key, i in (("because of the gene", 0), ("rest of that person's", 1), ("quirk of one", 2), ("a bad batch", 3)):
            self.at(key)
            self.play(FadeIn(chips[i], shift=LEFT * 0.2), GrowArrow(ars[i]), run_time=0.6)

        # --- many lines, side by side, more than once
        self.at("So use several clones")
        self.play(*[FadeOut(m) for m in [pat, pat_l, chips, *ars]], run_time=0.6)
        xs = [-3.7, -2.0, -0.3, 1.9, 3.6, 5.3]
        ys = [0.8, -1.2]
        grid = VGroup()
        for r_i, y in enumerate(ys):
            for c_i, x in enumerate(xs):
                grid.add(self.tissue([x, y, 0], 0.78, 0.62 if c_i < 3 else 1.0))
        hp = T("patient clones", 26, ORANGE).move_to([-2.0, 2.1, 0])
        hc = T("controls from different people", 26, GREY).move_to([3.6, 2.1, 0])
        b1 = T("batch 1", 24, GREY).move_to([-5.7, 0.8, 0])
        b2 = T("batch 2", 24, GREY).move_to([-5.7, -1.2, 0])
        self.play(LaggedStart(*[FadeIn(g, scale=0.7) for g in grid[:6]], lag_ratio=0.1), FadeIn(hp), FadeIn(hc), FadeIn(b1), run_time=1.4)
        self.at("grown side by side")
        side = T("side by side", 28).move_to([0, -2.7, 0])
        self.play(FadeIn(side), run_time=0.4)
        self.at("more than once")
        self.play(LaggedStart(*[FadeIn(g, scale=0.7) for g in grid[6:]], lag_ratio=0.1), FadeIn(b2), run_time=1.2)

        # --- put the gene back / remove it
        self.at("Then put the gene back")
        self.play(*[FadeOut(m) for m in [grid, hp, hc, b1, b2, side]], run_time=0.6)
        p1 = self.tissue([-4.6, 1.2, 0], 1.0, 0.62)
        p1l = T("patient", 24, ORANGE).next_to(p1, DOWN, buff=0.1)
        gb = chip("put the gene back", YELLOW, 26).move_to([-0.7, 1.2, 0])
        a1 = arr([-3.3, 1.2, 0], [-2.7, 1.2, 0], YELLOW, 4, 0.2)
        a1b = arr([1.0, 1.2, 0], [1.9, 1.2, 0], YELLOW, 4, 0.2)
        p1_after = self.tissue([3.2, 1.2, 0], 1.0, 0.62)
        self.play(FadeIn(p1), FadeIn(p1l), run_time=0.5)
        self.play(FadeIn(gb), GrowArrow(a1), GrowArrow(a1b), FadeIn(p1_after), run_time=0.8)

        self.at("remove it from a control")
        p2 = self.tissue([-4.6, -1.8, 0], 1.0, 1.0)
        p2l = T("control", 24, GREY).next_to(p2, DOWN, buff=0.1)
        rm = chip("remove the gene", YELLOW, 26).move_to([-0.7, -1.8, 0])
        a2 = arr([-3.3, -1.8, 0], [-2.7, -1.8, 0], YELLOW, 4, 0.2)
        a2b = arr([1.0, -1.8, 0], [1.9, -1.8, 0], YELLOW, 4, 0.2)
        qd = DashedVMobject(Circle(radius=1.0, stroke_color=GREY, stroke_width=3), num_dashes=24).move_to([3.2, -1.8, 0])
        qq = T("?", 56, GREY, weight=BOLD).move_to(qd)
        self.play(FadeIn(p2), FadeIn(p2l), run_time=0.5)
        self.play(FadeIn(rm), GrowArrow(a2), GrowArrow(a2b), FadeIn(qd), FadeIn(qq), run_time=0.8)

        self.at("see whether the result")
        patch = DashedVMobject(Circle(radius=0.38, stroke_color=YELLOW, stroke_width=3), num_dashes=16).move_to([3.2 - 0.45, 1.2 + 0.3, 0])
        rg = VGroup(*[Ellipse(width=0.14, height=0.36, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.5)
                      .rotate(a).move_to(np.array([3.2 - 0.45, 1.2 + 0.3, 0]) + 0.17 * np.array([np.cos(a + PI / 2), np.sin(a + PI / 2), 0]))
                      for a in (0, 2.1, 4.2)])
        cap = T("more radial glia in the cells that received it", 24, BLUE).move_to([2.4, 0.0, 0])
        self.play(Create(patch), FadeIn(rg, scale=0.5), FadeIn(cap), run_time=1.0)

        self.at("Resemblance has to be")
        allm = [p1, p1l, gb, a1, a1b, p1_after, p2, p2l, rm, a2, a2b, qd, qq, patch, rg, cap]
        self.play(*[FadeOut(m) for m in allm], run_time=0.6)
        r1 = T("Resemblance has to be measured", 44, font=TITLE_FONT).move_to([0, 0.7, 0])
        r2 = T("A mutation is blamed only after the controls", 36, GOLD, font=TITLE_FONT).move_to([0, -0.6, 0])
        fit(r1, 11.8); fit(r2, 11.8)
        self.play(Write(r1), run_time=1.2)
        self.at("blamed only after")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Resemblance must be measured. Blame a mutation only after controls."
