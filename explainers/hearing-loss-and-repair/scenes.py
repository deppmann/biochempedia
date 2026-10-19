"""Hidden hearing loss: a normal threshold does not count synapses  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = inner hair cell, ribbon and its vesicle pool (the synapse count)
  GREEN  = auditory nerve fibre and its terminal
  RED    = lost / missing / not equal / crossed out
  YELLOW = threshold (the test, in dB)
  TEAL   = proxy measures (SP/AP, ABR, EFR)
  ORANGE = noise exposure
  PURPLE = transmitter, and the complaint
  GOLD   = the bound (37 dB or more)
  GREY   = axes, outlines, de-emphasized
  TEXT   = neutral labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dashed_arr(a, b, color=GREY, w=4):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    body = DashedLine(a, b - d * 0.2, color=color, stroke_width=w, dash_length=0.15)
    tip = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.13)
    tip.rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(b - d * 0.1)
    return VGroup(body, tip)


def unit(cx, cy, s=1.0):
    """One sketch ribbon synapse: ribbon + a few vesicles above a nerve terminal."""
    rib = RoundedRectangle(corner_radius=0.05, width=0.16 * s, height=0.5 * s, stroke_color=BLUE,
                           stroke_width=3, fill_color=BLUE, fill_opacity=0.9).move_to([cx, cy + 0.22 * s, 0])
    ves = VGroup(*[Circle(radius=0.055 * s, stroke_width=0, fill_color=BLUE, fill_opacity=0.7)
                   .move_to([cx + dx * s, cy + dy * s, 0])
                   for dx, dy in [(-0.2, 0.32), (0.2, 0.32), (-0.2, 0.1), (0.2, 0.1)]])
    term = RoundedRectangle(corner_radius=0.12 * s, width=0.72 * s, height=0.34 * s, stroke_color=GREEN,
                            stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to([cx, cy - 0.32 * s, 0])
    ghost = DashedVMobject(RoundedRectangle(corner_radius=0.12 * s, width=0.72 * s, height=0.34 * s,
                                            stroke_color=RED, stroke_width=3).move_to(term), num_dashes=18)
    ghost.set_color(RED)
    g = VGroup(rib, ves, term)
    g.rib, g.ves, g.term, g.ghost = rib, ves, term, ghost
    return g


def lose(u):
    return [FadeOut(u.rib), FadeOut(u.ves), ReplacementTransform(u.term, u.ghost)]


def level_axis(x, y0, y1):
    ax = Arrow([x, y0, 0], [x, y1, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    up = T("louder", 22, GREY).next_to(ax.get_end(), RIGHT, buff=0.12)
    dn = T("quieter", 22, GREY).next_to(ax.get_start(), RIGHT, buff=0.12)
    return VGroup(ax, up, dn)


class S00Title(TitleCard):
    LESSON = "Hidden hearing loss, gene therapy and regeneration"
    TITLE = "A normal threshold counts nothing"


# -------------------------------------------------------------------------------------------
class S01Normal(SpokenScene):
    """A yellow threshold stays put while half the sketch synapses are lost."""

    def construct(self):
        mouse = chip("in male CBA/CaJ mice", TEXT, size=26).move_to([-2.6, 3.1, 0])
        noise = chip("loud noise", ORANGE, size=26).move_to([1.7, 3.1, 0])
        arrow = arr(mouse.get_right(), noise.get_left(), GREY, w=4)
        self.at("male")
        self.play(FadeIn(mouse, shift=DOWN * 0.2), run_time=0.5)
        self.at("loud noise")
        self.play(GrowArrow(arrow), FadeIn(noise, shift=LEFT * 0.2), run_time=0.5)

        # left: the test
        head_l = T("Hearing threshold", 30, YELLOW).move_to([-3.3, 1.9, 0])
        axis = level_axis(-5.8, -2.4, 1.2)
        line = Line([-4.9, -0.5, 0], [-1.7, -0.5, 0], color=YELLOW, stroke_width=7)
        lab = T("threshold", 26, YELLOW).next_to(line, UP, buff=0.15)
        status = chip("back to normal", TEXT, size=28).move_to([-2.5, -2.8, 0])
        self.at("hearing thresholds")
        self.play(FadeIn(head_l), Create(axis), run_time=0.6)
        self.play(Create(line), FadeIn(lab), run_time=0.5)
        self.play(FadeIn(status, shift=UP * 0.2), run_time=0.4)

        # right: the synapses
        head_r = T("Ribbon synapses (in this sketch)", 28, BLUE).move_to([3.3, 1.9, 0])
        pos = [(3.3 + dx, y) for y in (0.55, -1.35) for dx in (-2.25, -0.75, 0.75, 2.25)]
        units = [unit(x, y, 1.5) for x, y in pos]
        self.at("Yet the cochlea")
        self.play(FadeIn(head_r), LaggedStart(*[FadeIn(u, scale=0.8) for u in units], lag_ratio=0.1), run_time=1.4)
        self.at("about half")
        lost_ids = [1, 3, 4, 6]
        self.play(*[a for i in lost_ids for a in lose(units[i])], run_time=1.2)
        note = T("about half lost at one place", 26, RED).move_to([3.3, -2.9, 0])
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.5)

        q = T("?", 80, TEXT, weight=BOLD).move_to([0.0, -0.4, 0])
        self.at("How can the test")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("quietest sound")
        self.play(Indicate(line, color=YELLOW, scale_factor=1.12), Indicate(lab, color=YELLOW), run_time=0.9)
        self.at("carry the rest")
        keep = [units[i] for i in (0, 2, 5, 7)]
        self.play(*[Indicate(u, color=BLUE, scale_factor=1.15) for u in keep], run_time=0.9)
        self.finish()


# -------------------------------------------------------------------------------------------
class S02Ribbon(SpokenScene):
    """Inner hair cell, ribbon, vesicle pool, nerve terminal."""

    def construct(self):
        cx = -2.0
        cell = RoundedRectangle(corner_radius=0.5, width=6.2, height=2.3, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.16).move_to([cx, 2.15, 0])
        clab = T("inner hair cell", 32, BLUE).move_to([cx, 2.4, 0])
        self.at("inner hair cell")
        self.play(FadeIn(cell, scale=0.9), FadeIn(clab), run_time=0.8)

        term = RoundedRectangle(corner_radius=0.3, width=3.6, height=0.9, stroke_color=GREEN, stroke_width=4,
                                fill_color=GREEN, fill_opacity=0.3).move_to([cx, -0.95, 0])
        fibre = Line([cx, -1.4, 0], [cx, -3.1, 0], color=GREEN, stroke_width=8)
        flab = T("auditory nerve fibre", 28, GREEN).next_to(fibre, RIGHT, buff=0.2).shift(DOWN * 0.1)
        drops = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
                         .move_to([cx + dx, 0.85, 0]) for dx in (-0.9, -0.45, 0.45, 0.9)])
        self.at("releases transmitter")
        self.play(FadeIn(term, shift=UP * 0.3), Create(fibre), run_time=0.7)
        self.add(drops)
        self.play(*[d.animate.shift(DOWN * 1.4).set_opacity(0.0) for d in drops], run_time=1.6, rate_func=linear)
        tlab = T("transmitter", 26, PURPLE).move_to([cx + 3.6, 0.0, 0])
        self.at("auditory nerve")
        self.play(FadeIn(flab), FadeIn(tlab), run_time=0.5)

        rib = RoundedRectangle(corner_radius=0.08, width=0.36, height=1.1, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.95).move_to([cx, 0.45, 0])
        rlab = T("ribbon", 30, BLUE).move_to([cx - 2.6, 0.45, 0])
        rline = Line([cx - 2.0, 0.45, 0], [cx - 0.25, 0.45, 0], color=BLUE, stroke_width=2)
        self.at("at ribbon synapses")
        self.play(FadeOut(tlab), GrowFromEdge(rib, UP), run_time=0.8)
        self.play(FadeIn(rlab), Create(rline), run_time=0.5)
        self.at("dense structure")
        self.play(Indicate(rib, color=BLUE, scale_factor=1.12), run_time=0.8)

        pts = [(-0.5, 0.8), (0.5, 0.8), (-0.8, 0.45), (0.8, 0.45), (-0.5, 0.05), (0.5, 0.05), (-1.05, 0.8), (1.05, 0.05)]
        ves = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color=BLUE, fill_opacity=0.7).move_to([cx + dx, dy, 0])
                       for dx, dy in pts])
        vlab = T("pool of vesicles", 26, BLUE).move_to([cx + 3.0, 0.2, 0])
        vline = Line([cx + 1.75, 0.2, 0], [cx + 1.15, 0.1, 0], color=BLUE, stroke_width=2)
        self.at("larger pool")
        self.play(LaggedStart(*[FadeIn(v, scale=0.3) for v in ves], lag_ratio=0.12), FadeIn(vlab), Create(vline),
                  run_time=1.4)

        thr = chip("threshold", YELLOW, size=30).move_to([4.7, 2.3, 0])
        ne = T("≠", 60, RED, weight=BOLD).move_to([4.7, 1.25, 0])
        cnt = chip("synapse count", BLUE, size=30).move_to([4.7, 0.2, 0])
        self.at("does not count")
        self.play(FadeIn(thr, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(ne, scale=0.6), FadeIn(cnt, shift=UP * 0.2), run_time=0.6)
        self.finish()


# -------------------------------------------------------------------------------------------
class S03Noise(SpokenScene):
    """Threshold back to the old value at two weeks; ribbon count about half at eight weeks."""

    def construct(self):
        cols = [-2.3, 1.4, 4.4]
        heads = [T(t, 28, TEXT) for t in ("before noise", "2 weeks", "8 weeks")]
        for h, x in zip(heads, cols):
            h.move_to([x, 2.35, 0])
        lab_thr = T("Threshold", 26, YELLOW).move_to([-5.2, 1.1, 0])
        lab_rib = VGroup(T("Ribbons,", 26, BLUE), T("32 kHz place", 26, BLUE)).arrange(DOWN, buff=0.08).move_to([-5.2, -1.9, 0])
        k1 = Line([cols[0] - 0.9, 1.0, 0], [cols[0] + 0.9, 1.0, 0], color=YELLOW, stroke_width=8)
        bar1 = Rectangle(width=1.2, height=2.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5)
        bar1.move_to([cols[0], -3.1 + 1.1, 0])
        ctrl = T("control", 24, BLUE).next_to(bar1, UP, buff=0.12)
        self.at("tested this")
        self.play(FadeIn(heads[0]), FadeIn(lab_thr), FadeIn(lab_rib), run_time=0.6)
        self.play(Create(k1), GrowFromEdge(bar1, DOWN), FadeIn(ctrl), run_time=0.9)

        noise = chip("noise: 8 to 16 kHz, 100 dB SPL, 2 hours", ORANGE, size=26).move_to([0.5, 3.15, 0])
        self.at("played noise")
        self.play(FadeIn(noise, shift=DOWN * 0.2), run_time=0.6)

        k2 = Line([cols[1] - 0.9, 1.0, 0], [cols[1] + 0.9, 1.0, 0], color=YELLOW, stroke_width=8)
        same = DashedLine(k1.get_right(), k2.get_left(), color=YELLOW, stroke_width=3)
        back = T("back to the old value", 24, YELLOW).next_to(same, DOWN, buff=0.12)
        self.at("two weeks")
        self.play(FadeIn(heads[1]), run_time=0.4)
        self.play(Create(same), Create(k2), run_time=0.8)
        self.play(FadeIn(back), run_time=0.4)
        intact = T("hair cells intact", 26, BLUE).move_to([cols[1] - 0.3, -2.0, 0])
        self.at("hair cells were intact")
        self.play(FadeIn(intact, shift=UP * 0.15), run_time=0.5)

        bar3 = Rectangle(width=1.2, height=1.1, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.5)
        bar3.move_to([cols[2], -3.1 + 0.55, 0])
        ghost = DashedVMobject(Rectangle(width=1.2, height=1.1, stroke_color=RED, stroke_width=3)
                               .move_to([cols[2], -3.1 + 1.65, 0]), num_dashes=24).set_color(RED)
        self.at("But at eight weeks")
        self.play(FadeIn(heads[2]), GrowFromEdge(bar3, DOWN), run_time=0.9)
        low = T("about 50% below control", 24, RED).move_to([cols[2] - 0.3, -0.45, 0])
        self.at("below control")
        self.play(Create(ghost), FadeIn(low), run_time=0.8)

        deg = VGroup(T("the nerve", 24, GREEN), T("degenerated later", 24, GREEN)).arrange(DOWN, buff=0.06).move_to([cols[2] + 0.4, 1.05, 0])
        self.at("degenerated later")
        self.play(FadeIn(deg, shift=UP * 0.15), run_time=0.6)
        self.finish()


# -------------------------------------------------------------------------------------------
def dots(n_rows, n_cols, r=0.09, gap=0.27, color=TEXT):
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.9)
                    .move_to([c * gap, -rw * gap, 0]) for rw in range(n_rows) for c in range(n_cols)]).center()


class S04People(SpokenScene):
    """No living synapse count; two proxy studies."""

    def construct(self):
        box = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=4.2, height=2.8, stroke_color=BLUE,
                                              stroke_width=4), num_dashes=40).set_color(BLUE).move_to([3.0, 0.5, 0])
        qm = T("?", 110, BLUE, weight=BOLD).move_to(box)
        blab = T("synapse count in a living person", 26, BLUE).next_to(box, DOWN, buff=0.25)
        self.at("no living synapse count")
        self.play(Create(box), FadeIn(qm, scale=0.6), FadeIn(blab), run_time=1.0)

        prox = [chip(t, TEAL, size=30) for t in ("SP/AP ratio", "ABR", "EFR")]
        grp = VGroup(*prox).arrange(DOWN, buff=0.4).move_to([-3.6, 0.5, 0])
        plab = T("proxies", 28, TEAL).next_to(grp, UP, buff=0.3)
        self.at("two studies used proxies")
        self.play(FadeIn(plab), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in prox], lag_ratio=0.25), run_time=1.2)
        arrows = [dashed_arr([-1.9, p.get_center()[1], 0], [0.7, 0.5 + 0.4 * (1 - i), 0], TEAL) for i, p in enumerate(prox)]
        self.play(*[Create(a) for a in arrows], run_time=0.8)

        # --- card A -------------------------------------------------------------------
        self.at("young adults")
        self.play(*[FadeOut(m) for m in (box, qm, blab, grp, plab, *arrows)], run_time=0.6)
        fa = RoundedRectangle(corner_radius=0.2, width=6.1, height=6.1, stroke_color=GREY, stroke_width=2).move_to([-3.3, -0.05, 0])
        ha = T("34 young adults", 30, TEXT).move_to([-3.3, 2.5, 0])
        da = dots(2, 17, r=0.08, gap=0.3).move_to([-3.3, 1.75, 0])
        self.play(Create(fa), FadeIn(ha), FadeIn(da), run_time=0.8)
        b_lo = Rectangle(width=1.3, height=1.0, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.3)
        b_hi = Rectangle(width=1.3, height=1.7, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.6)
        b_lo.move_to([-4.3, -0.1 - 0.35, 0])
        b_hi.move_to([-2.3, -0.1 - 0.0, 0]).align_to(b_lo, DOWN)
        b_lo.align_to([0, -1.0, 0], DOWN); b_hi.align_to([0, -1.0, 0], DOWN)
        l_lo = T("lower-risk", 22, GREY).next_to(b_lo, DOWN, buff=0.12)
        l_hi = T("higher-risk", 22, TEXT).next_to(b_hi, DOWN, buff=0.12)
        sk = T("SP/AP ratio, in this sketch", 22, TEAL).move_to([-3.3, 1.0, 0])
        self.at("group had")
        self.play(FadeIn(sk), GrowFromEdge(b_lo, DOWN), GrowFromEdge(b_hi, DOWN), FadeIn(l_lo), FadeIn(l_hi), run_time=1.0)
        cons = T("authors: consistent with selective neural loss", 22, TEAL).move_to([-3.3, -2.0, 0])
        fit(cons, max_w=5.6)
        self.at("consistent with selective")
        self.play(FadeIn(cons, shift=UP * 0.1), run_time=0.5)
        cav = T("but thresholds at 10 to 16 kHz were also raised", 22, YELLOW).move_to([-3.3, -2.65, 0])
        fit(cav, max_w=5.6)
        self.at("raised thresholds")
        self.play(FadeIn(cav, shift=UP * 0.1), run_time=0.5)

        # --- card B -------------------------------------------------------------------
        fb = RoundedRectangle(corner_radius=0.2, width=6.1, height=6.1, stroke_color=GREY, stroke_width=2).move_to([3.3, -0.05, 0])
        hb = T("A second study", 30, TEXT).move_to([3.3, 2.5, 0])
        d1 = dots(1, 16, r=0.1, gap=0.33).move_to([3.3, 1.45, 0])
        l1 = T("16 with trouble hearing speech in noise", 22, PURPLE).next_to(d1, UP, buff=0.18)
        fit(l1, max_w=5.6)
        d2 = dots(1, 16, r=0.1, gap=0.33).move_to([3.3, 0.0, 0])
        l2 = T("16 matched controls", 22, GREY).next_to(d2, UP, buff=0.18)
        self.at("A second study compared")
        self.play(Create(fb), FadeIn(hb), run_time=0.6)
        self.play(FadeIn(d1), FadeIn(l1), run_time=0.5)
        self.play(FadeIn(d2), FadeIn(l2), run_time=0.5)
        res = T("no association with ABR or EFR", 24, TEAL).move_to([3.3, -1.3, 0])
        self.at("no association")
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.5)
        hedge = T("measures may not be sensitive enough", 22, GREY).move_to([3.3, -2.3, 0])
        self.at("might not be sensitive")
        self.play(FadeIn(hedge, shift=UP * 0.1), run_time=0.5)
        self.finish()


# -------------------------------------------------------------------------------------------
class S05Ceiling(SpokenScene):
    """The censored number: baseline above the 95 dB ceiling, 58 dB at week 26."""

    def construct(self):
        def X(db):
            return -5.5 + (db - 50) * (11.0 / 60.0)

        y0 = 0.6
        head = T("ABR threshold, dB (one child)", 28, YELLOW).move_to([0, 3.3, 0])
        axis = Line([X(50), y0, 0], [X(110), y0, 0], color=GREY, stroke_width=4)
        ticks = VGroup(*[VGroup(Line([X(d), y0 - 0.1, 0], [X(d), y0 + 0.1, 0], color=GREY, stroke_width=3),
                                M(str(d), 22, GREY).move_to([X(d), y0 - 0.38, 0])) for d in range(50, 111, 10)])
        self.play(FadeIn(head), Create(axis), FadeIn(ticks), run_time=0.8)

        zone = Rectangle(width=X(110) - X(95), height=1.9, stroke_width=0, fill_color=RED, fill_opacity=0.14)
        zone.move_to([(X(95) + X(110)) / 2, y0 + 0.95, 0])
        hatch = VGroup(*[Line([X(95) + 0.15 * i, y0 + 0.02, 0], [min(X(95) + 0.15 * i + 0.5, X(110)), y0 + 0.52, 0],
                              color=RED, stroke_width=2, stroke_opacity=0.5) for i in range(0, 17)])
        ceil = Line([X(95), y0 - 0.3, 0], [X(95), y0 + 1.95, 0], color=TEXT, stroke_width=5)
        ctxt = T("95 dB test ceiling", 24, TEXT).next_to(ceil, UP, buff=0.12).shift(LEFT * 0.9)
        nm = T("not measured", 22, RED).move_to([(X(95) + X(110)) / 2, y0 + 1.55, 0])
        base = Circle(radius=0.2, stroke_color=YELLOW, stroke_width=5, fill_opacity=0).move_to([X(103), y0 + 0.75, 0])
        bq = T("?", 28, YELLOW, weight=BOLD).move_to(base)
        blab = T("baseline: above 95", 22, YELLOW).move_to([X(103) + 0.1, y0 + 1.45, 0])
        fit(blab, max_w=2.3)
        self.at("baseline")
        self.play(FadeIn(base), FadeIn(bq), run_time=0.5)
        self.play(FadeIn(blab), run_time=0.4)

        self.at("decibel test ceiling")
        self.play(Create(ceil), FadeIn(ctxt), FadeIn(zone), run_time=0.9)

        wk = Dot([X(58), y0, 0], radius=0.17, color=YELLOW)
        wlab = T("week 26: 58 dB", 24, YELLOW).next_to(wk, UP, buff=0.25)
        move = dashed_arr([X(103) - 0.3, y0 + 0.75, 0], [X(58) + 0.3, y0 + 0.12, 0], YELLOW)
        self.at("At week")
        self.play(FadeIn(wk, scale=2.0), FadeIn(wlab), run_time=0.6)
        self.play(Create(move), run_time=0.7)

        by = -0.95
        br = VGroup(Line([X(58), by, 0], [X(95), by, 0], color=GOLD, stroke_width=6),
                    Line([X(58), by - 0.15, 0], [X(58), by + 0.15, 0], color=GOLD, stroke_width=6),
                    Line([X(95), by - 0.15, 0], [X(95), by + 0.15, 0], color=GOLD, stroke_width=6))
        more = dashed_arr([X(95), by, 0], [X(110), by, 0], GOLD, w=6)
        blabel = T("37 dB", 32, GOLD, weight=BOLD).move_to([(X(58) + X(95)) / 2, by - 0.5, 0])
        mlabel = T("or more", 28, GOLD).move_to([(X(95) + X(110)) / 2, by - 0.5, 0])
        self.at("improvement was")
        self.play(Create(br), run_time=0.7)
        self.play(FadeIn(blabel), Create(more), FadeIn(mlabel), run_time=0.7)
        lb = T("a lower bound", 30, GOLD).move_to([0, -2.15, 0])
        self.at("lower bound")
        self.play(FadeIn(lb, shift=UP * 0.15), run_time=0.5)

        pct = chip("percentage of hearing restored", TEXT, size=26).move_to([0, -3.3, 0])
        cross = VGroup(Line(pct.get_corner(UL), pct.get_corner(DR), color=RED, stroke_width=7),
                       Line(pct.get_corner(DL), pct.get_corner(UR), color=RED, stroke_width=7))
        self.play(FadeOut(lb), run_time=0.01)
        pct.move_to([0, -2.95, 0]); cross.move_to(pct)
        self.at("percentage of hearing restored")
        self.play(FadeIn(pct), run_time=0.4)
        self.play(Create(cross), run_time=0.5)
        self.finish()


# -------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """Complaint, lesion, test; threshold vs synapses; proxy vs count; ceiling vs exact."""

    def construct(self):
        def neq(a, b, ya, sym="≠", col=RED):
            s = T(sym, 44, col, weight=BOLD)
            g = VGroup(a, s, b).arrange(RIGHT, buff=0.4).move_to([0, ya, 0])
            return g, s

        comp = chip("complaint", PURPLE, size=30)
        les = chip("proposed lesion", BLUE, size=30)
        tst = chip("validated test", YELLOW, size=30)
        s1 = T("≠", 44, RED, weight=BOLD)
        s2 = T("≠", 44, RED, weight=BOLD)
        row1 = VGroup(comp, s1, les, s2, tst).arrange(RIGHT, buff=0.35).move_to([0, 2.6, 0])
        self.at("A complaint")
        self.play(FadeIn(comp, shift=DOWN * 0.2), run_time=0.5)
        self.at("proposed lesion")
        self.play(FadeIn(s1), FadeIn(les, shift=DOWN * 0.2), run_time=0.5)
        self.at("validated test")
        self.play(FadeIn(s2), FadeIn(tst, shift=DOWN * 0.2), run_time=0.5)

        a = chip("normal threshold", YELLOW, size=28)
        b = chip("intact synapses", BLUE, size=28)
        row2, _ = neq(a, b, 1.0)
        self.at("normal threshold did not")
        self.play(FadeIn(row2, shift=UP * 0.15), run_time=0.7)
        mice = T("in these mice", 24, GREY).next_to(row2, DOWN, buff=0.12)
        self.play(FadeIn(mice), run_time=0.3)

        c = chip("proxy", TEAL, size=28)
        d = chip("synapse count", BLUE, size=28)
        row3, _ = neq(c, d, -0.5)
        self.at("A proxy is not")
        self.play(FadeIn(row3, shift=UP * 0.15), run_time=0.7)

        e = chip("value past the ceiling", YELLOW, size=28)
        f = chip("a bound", GOLD, size=28)
        row4, _ = neq(e, f, -1.8, sym="=", col=GOLD)
        g = T("not an exact change", 24, GOLD).next_to(row4, DOWN, buff=0.12)
        self.at("A value past the ceiling")
        self.play(FadeIn(row4, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(g), run_time=0.3)

        q = T("What does this number count, and what does it leave out?", 32, TEXT, font=TITLE_FONT)
        fit(q, max_w=11.8)
        q.move_to([0, -3.3, 0])
        self.at("ask what a number")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Ask what a number counts, and what it leaves out."
