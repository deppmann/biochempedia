"""Enzymes at work: Count the Working Sites (film 1 of 2, Biochemistrypedia explainer).

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOUR MAP (one colour per concept, whole film and film 2)
  BLUE   = enzyme (catalase); the working-sites counter
  ORANGE = substrate (hydrogen peroxide)
  GREEN  = products
  GREY   = denatured (bent) enzyme, outlines
  YELLOW = speed-per-site gauge
  PURPLE = rate bar
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
TAN = "#C9A66B"
LIVER = "#B5604A"

ENZ_PTS = [(-1.8, -1.0), (1.8, -1.0), (1.8, 1.0), (0.65, 1.0), (0.45, 0.2), (-0.45, 0.2), (-0.65, 1.0), (-1.8, 1.0)]
ENZ_BAD = [(-1.9, -1.1), (1.7, -0.8), (2.0, 0.7), (0.95, 0.9), (0.85, 0.55), (0.35, 0.5), (0.0, 0.95), (-1.6, 1.1)]
FIT = 0.58          # pocket centre above the block centre, in block units


def enzyme(s=1.0, color=BLUE, pts=ENZ_PTS, fill=0.35, sw=4):
    p = Polygon(*[np.array([x, y, 0.0]) for x, y in pts], stroke_color=color, stroke_width=sw,
                fill_color=color, fill_opacity=fill).round_corners(0.12)
    return p.scale(s)


def wedge(s=1.0, color=ORANGE, narrow=1.0):
    w = 0.6 * narrow
    pts = [(-w, 0.37), (w, 0.37), (0.4 * narrow, -0.37), (-0.4 * narrow, -0.37)]
    p = Polygon(*[np.array([x, y, 0.0]) for x, y in pts], stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.8).round_corners(0.06)
    return p.scale(s)


def products(center, s=1.0):
    a = Circle(radius=0.26 * s, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.8)
    b = Circle(radius=0.34 * s, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5)
    g = VGroup(a, b).arrange(RIGHT, buff=0.08)
    return g.move_to(center)


def swim(m, ax=0.25, ay=0.18, sp=1.0, ph=0.0, rot=0.0):
    """Gentle drifting that never fights an animation: it moves by changes in a sine offset."""
    m._tt = 0.0
    m._off = np.zeros(3)

    def u(mm, dt):
        mm._tt += dt
        t = mm._tt * sp + ph
        off = np.array([ax * np.sin(t), ay * np.cos(1.3 * t), 0.0])
        mm.shift(off - mm._off)
        mm._off = off
        if rot:
            mm.rotate(rot * dt * np.cos(t))
    m.add_updater(u)
    return m


def lab(text, size=30, color=TEXT, pos=ORIGIN, **kw):
    return T(text, size=size, color=color, **kw).move_to(pos)


# ---------------------------------------------------------------------------------------------
# one big enzyme, used in scenes 3 to 5
# ---------------------------------------------------------------------------------------------
ES = 1.55
EC = np.array([0.0, -0.25, 0.0])
POCKET = EC + np.array([0.0, FIT * ES, 0.0])
QUEUE = np.array([-4.6, 0.3, 0.0])


def big_enzyme():
    e = enzyme(ES).move_to(EC)
    name = lab("catalase", 34, TEXT, EC + DOWN * 0.65)
    return e, name


class Film(SpokenScene):
    pass


# ---------------------------------------------------------------------------------------------
# title
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Enzymes at Work"
    TITLE = "Count the Working Sites"


# ---------------------------------------------------------------------------------------------
# s01: the potato fizzes
# ---------------------------------------------------------------------------------------------
class S01Question(Film):
    def construct(self):
        GX, GW, GTOP, GBOT = -2.8, 4.4, 2.2, -3.0
        LIQ = 1.3
        glass = RoundedRectangle(corner_radius=0.35, width=GW, height=GTOP - GBOT, stroke_color=TEXT, stroke_width=5,
                                 fill_opacity=0).move_to([GX, (GTOP + GBOT) / 2, 0])
        liquid = Rectangle(width=GW - 0.2, height=LIQ - GBOT - 0.1, stroke_width=0, fill_color=ORANGE,
                           fill_opacity=0.22).move_to([GX, (LIQ + GBOT + 0.1) / 2, 0])
        gl = lab("hydrogen peroxide", 28, ORANGE, [GX, -3.45, 0])
        SX, SW, STOP = 3.9, 2.8, 0.7
        sglass = RoundedRectangle(corner_radius=0.3, width=SW, height=STOP - GBOT, stroke_color=TEXT, stroke_width=5,
                                  fill_opacity=0).move_to([SX, (STOP + GBOT) / 2, 0])
        sliq = Rectangle(width=SW - 0.2, height=0.0 + (-0.1 - GBOT - 0.1) + 0.1, stroke_width=0, fill_color=ORANGE,
                         fill_opacity=0.22).move_to([SX, (-0.1 + GBOT + 0.1) / 2, 0])
        sl = lab("no potato: slow", 28, TEXT, [SX, -3.45, 0])
        potato = Ellipse(width=2.3, height=1.3, stroke_color=TAN, stroke_width=4, fill_color=TAN,
                         fill_opacity=0.9).move_to([GX, 3.2, 0])
        spots = VGroup(*[Dot(radius=0.06, color="#8C7040") for _ in range(5)])
        for d, (dx, dy) in zip(spots, [(-0.6, 0.15), (-0.1, -0.25), (0.4, 0.2), (0.7, -0.1), (-0.3, 0.3)]):
            d.move_to(potato.get_center() + [dx, dy, 0])
        potato = VGroup(potato, spots)

        on = ValueTracker(0.0)
        foam = ValueTracker(0.0)
        # bubbles
        bubbles = VGroup()
        rng = np.random.RandomState(3)
        for i in range(16):
            r = float(rng.uniform(0.07, 0.15))
            b = Circle(radius=r, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35)
            b.p = i / 16.0
            b.bx = float(rng.uniform(GX - 1.5, GX + 1.5))
            b.sp = float(rng.uniform(0.28, 0.42))
            b.ph = float(rng.uniform(0, 6))

            def ub(m, dt):
                m.p = (m.p + dt * m.sp * on.get_value()) % 1.0
                y = -2.0 + m.p * (LIQ - -2.0)
                m.move_to([m.bx + 0.12 * np.sin(8 * m.p + m.ph), y, 0])
                m.set_stroke(opacity=min(1, on.get_value() * 2)).set_fill(opacity=0.35 * min(1, on.get_value() * 2))
            b.add_updater(ub)
            bubbles.add(b)
        # foam head
        foams = VGroup()
        for i in range(10):
            c = Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.5)
            c.fx = GX - 1.8 + i * 0.4
            c.fy = LIQ + 0.12 + 0.08 * (i % 2)
            c.r0 = 0.17 + 0.04 * (i % 3)

            def uf(m, dt):
                target = max(m.r0 * foam.get_value(), 0.001)
                m.scale(target / (m.width / 2))
                m.move_to([m.fx, m.fy + 0.3 * (m.width / 2) * 0.3, 0])
                m.set_stroke(opacity=min(1.0, foam.get_value() * 3))
            c.add_updater(uf)
            foams.add(c)
        # one slow bubble in the side glass
        side = VGroup()
        for i in range(2):
            b = Circle(radius=0.1, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35)
            b.p = i * 0.5

            def us(m, dt):
                m.p = (m.p + dt * 0.19) % 1.0
                m.move_to([SX + 0.15 * np.sin(6 * m.p), -2.7 + m.p * 2.5, 0])
            b.add_updater(us)
            side.add(b)

        self.play(Create(glass), Create(sglass), FadeIn(liquid), FadeIn(sliq), FadeIn(gl), run_time=1.0)
        self.add(foams, bubbles, side)
        self.add(potato)
        self.at("slice")
        self.play(potato.animate.move_to([GX, -2.3, 0]), run_time=1.3, rate_func=rush_into)
        self.play(potato.animate.shift(UP * 0.1), run_time=0.4)
        swim(potato, ax=0.05, ay=0.04, sp=2.0)
        self.at("fizzes")
        self.play(on.animate.set_value(1.0), foam.animate.set_value(1.0), run_time=2.0)
        self.at("something in the potato")
        ring = SurroundingRectangle(potato, color=TEXT, buff=0.18, corner_radius=0.2, stroke_width=4)
        self.play(Create(ring), run_time=0.7)
        self.at("never used up")
        q = lab("used up?", 48, TEXT, [GX, 3.05, 0])
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.7)
        self.at("hydrogen peroxide breaks down alone")
        self.play(FadeOut(ring), FadeIn(sl), run_time=0.6)
        self.at("the bubbles are oxygen")
        og = lab("oxygen gas", 32, GREEN, [0.9, 1.3, 0])
        arr = Arrow(og.get_left() + LEFT * 0.05, [GX + 1.3, 0.3, 0], buff=0.1, color=GREEN, stroke_width=5)
        self.play(FadeIn(og), GrowArrow(arr), FadeOut(q), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s02: catalase, an enzyme
# ---------------------------------------------------------------------------------------------
class S02Catalase(Film):
    def construct(self):
        px, py = -4.3, 0.5
        pot = Ellipse(width=4.4, height=4.0, stroke_color=TAN, stroke_width=5, fill_color=TAN, fill_opacity=0.35).move_to([px, py, 0])
        cells = VGroup()
        for gx in (-1.5, -0.5, 0.5, 1.5):
            for gy in (-1.0, 0.0, 1.0):
                if (gx / 2.2) ** 2 + (gy / 1.8) ** 2 < 0.9:
                    cells.add(RoundedRectangle(corner_radius=0.18, width=0.88, height=0.88, stroke_color=TAN, stroke_width=3,
                                               fill_color=TAN, fill_opacity=0.12).move_to([px + gx, py + gy, 0]))
        potato = VGroup(pot, cells)
        plab = lab("potato cells", 28, TAN, [px, -2.05, 0])
        liver = Ellipse(width=3.0, height=2.4, stroke_color=LIVER, stroke_width=5, fill_color=LIVER, fill_opacity=0.5).move_to([5.1, 0.5, 0])
        liver.rotate(0.25)
        llab = lab("liver cells", 28, LIVER, [5.1, -1.2, 0])
        big = enzyme(0.8).move_to([0.55, 0.5, 0])
        bname = lab("catalase (an enzyme)", 30, BLUE, [0.55, -0.95, 0])
        # little blue blocks inside cells
        minis = VGroup()
        for gx, gy in [(-0.5, 0.0), (0.5, 1.0), (-1.5, -1.0), (1.5, 0.0), (0.5, -1.0)]:
            minis.add(enzyme(0.17).move_to([px + gx, py + gy, 0]))
        lminis = VGroup(*[enzyme(0.17).move_to([5.1 + dx, 0.5 + dy, 0]) for dx, dy in [(-0.7, 0.3), (0.5, 0.5), (0.0, -0.4), (0.8, -0.2)]])
        for m in list(minis) + list(lminis):
            swim(m, ax=0.04, ay=0.04, sp=2.2, ph=float(np.random.RandomState(1).rand() * 6))
        lines = VGroup(Line(minis[0].get_center() + RIGHT * 0.3, big.get_left() + LEFT * 0.05, color=BLUE, stroke_width=3))

        self.play(FadeIn(pot), FadeIn(cells), FadeIn(plab), run_time=0.6)
        swim(potato, ax=0.04, ay=0.04, sp=1.1)
        self.at("catalase")
        self.play(FadeIn(minis, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(big, scale=0.8), Create(lines), run_time=0.8)
        swim(big, ax=0.06, ay=0.06, sp=1.4)
        self.play(FadeIn(bname), run_time=0.6)
        self.at("liver cells")
        self.play(FadeIn(liver), FadeIn(llab), run_time=0.7)
        self.play(FadeIn(lminis, lag_ratio=0.25), run_time=0.9)
        self.at("an enzyme is a molecule")
        self.play(Indicate(big, color=BLUE, scale_factor=1.12), run_time=1.0)
        self.at("almost always a protein")
        self.play(Indicate(bname, color=BLUE, scale_factor=1.05), run_time=1.0)
        self.at("that speeds up")
        eq = VGroup(T("hydrogen peroxide", 32, ORANGE), T("→", 32, TEXT), T("water + oxygen", 32, GREEN)).arrange(RIGHT, buff=0.3)
        eq.move_to([0.55, -3.0, 0])
        self.play(FadeIn(eq, shift=UP * 0.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s03: one catalase does one reaction
# ---------------------------------------------------------------------------------------------
class S03Cycle(Film):
    def construct(self):
        enz, name = big_enzyme()
        ghost = enzyme(ES).move_to(EC).set_fill(opacity=0).set_stroke(GREY, 3, opacity=0.7)
        A = wedge(ES).move_to(QUEUE + UP * 1.7)
        B = wedge(ES).move_to(QUEUE + DOWN * 0.3)
        swim(A, 0.3, 0.2, 0.9, 0.0)
        swim(B, 0.3, 0.2, 0.8, 2.0)
        slab = lab("substrate:\nhydrogen peroxide", 28, ORANGE, QUEUE + UP * 3.0)

        self.play(FadeIn(enz, scale=0.9), FadeIn(name), run_time=1.2)
        self.add(ghost)
        swim(enz, 0.0, 0.0)
        self.at("its substrate")
        self.play(FadeIn(A), FadeIn(B), FadeIn(slab), run_time=1.0)
        self.at("the substrate drifts")
        self.play(A.animate.move_to(POCKET + UP * 1.5 + LEFT * 0.4), run_time=1.5, rate_func=smooth)
        sl = lab("active site", 32, TEXT, [4.0, 1.9, 0])
        sar = Arrow(sl.get_left() + LEFT * 0.05, POCKET + RIGHT * 0.9, buff=0.1, color=TEXT, stroke_width=5)
        self.at("active site")
        self.play(FadeIn(sl), GrowArrow(sar), A.animate.move_to(POCKET + UP * 0.5), run_time=0.7)
        self.play(A.animate.move_to(POCKET), FadeOut(slab), run_time=0.8, rate_func=smooth)
        self.at("a small pocket")
        self.play(Indicate(sl, color=TEXT, scale_factor=1.12), run_time=0.8)
        self.at("there it is turned")
        self.play(Indicate(A, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.at("into products")
        prod = products(POCKET, 1.3)
        self.play(ReplacementTransform(A, prod), FadeOut(sl), FadeOut(sar), run_time=1.0)
        self.at("water and oxygen")
        plab = lab("water + oxygen", 32, GREEN, POCKET + UP * 1.3)
        eq = VGroup(T("hydrogen peroxide", 30, ORANGE), T("→", 30, TEXT), T("water + oxygen", 30, GREEN)).arrange(RIGHT, buff=0.3)
        eq.move_to([0, -3.2, 0])
        self.play(FadeIn(plab), FadeIn(eq, shift=UP * 0.15), run_time=1.0)
        swim(prod, 0.0, 0.05, 2.0)
        self.at("the products leave")
        self.play(prod.animate.move_to([3.9, 2.4, 0]), plab.animate.move_to([3.9, 3.2, 0]), run_time=1.3)
        self.play(FadeOut(plab), prod.animate.set_opacity(0), run_time=0.4)
        self.at("the enzyme is unchanged")
        un = lab("same enzyme, unchanged", 32, BLUE, EC + DOWN * 1.95)
        self.play(ghost.animate.set_stroke(TEXT, 6, opacity=1.0), FadeIn(un), run_time=0.8)
        self.play(ghost.animate.set_stroke(GREY, 3, opacity=0.7), run_time=0.8)
        self.play(Indicate(enz, color=BLUE, scale_factor=1.04), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s04: the next one, and the next: a catalyst
# ---------------------------------------------------------------------------------------------
class S04Catalyst(Film):
    def construct(self):
        enz, name = big_enzyme()
        B = wedge(ES).move_to(QUEUE + DOWN * 0.3)
        swim(B, 0.3, 0.2, 0.8, 2.0)
        extra = wedge(ES).move_to(QUEUE + UP * 1.7)
        swim(extra, 0.3, 0.2, 0.9, 0.0)
        count = [0]

        def tally():
            return T(f"molecules changed: {count[0]}", 32, ORANGE).move_to([6.5, 3.25, 0], aligned_edge=RIGHT)
        tl = tally()
        self.add(enz, name, B, extra)
        self.play(FadeIn(tl), run_time=0.4)

        state = {"w": B, "q": extra}

        def cycle(d):
            w = state["w"]
            self.play(w.animate.move_to(POCKET), run_time=max(0.1, 0.45 * d), rate_func=smooth)
            pr = products(POCKET, ES)
            count[0] += 1
            new_tl = tally()
            self.play(ReplacementTransform(w, pr), Transform(tl, new_tl), run_time=max(0.07, 0.15 * d))
            nxt = wedge(ES).move_to(QUEUE + UP * 1.7)
            swim(nxt, 0.3, 0.2, 0.9, count[0])
            self.play(FadeOut(pr, shift=RIGHT * 2.5 + UP * 1.0), state["q"].animate.move_to(QUEUE + DOWN * 0.3),
                      FadeIn(nxt), run_time=max(0.1, 0.4 * d))
            state["w"] = state["q"]
            state["q"] = nxt

        # the first two slowly, matching the words
        self.at("then it takes in")
        cycle(1.2)
        self.at("and the next")
        cycle(1.2)
        self.at("the same enzyme")
        cycle(1.0)
        cycle(1.0)
        d = 0.9
        t_cat = self.t_of("that makes it a catalyst") - 0.2
        while self.elapsed() < t_cat - 0.5:
            cycle(d)
            d = max(0.45, d - 0.1)
        self.at("that makes it a catalyst")
        cl = lab("catalyst: not used up", 36, BLUE, EC + DOWN * 1.95)
        self.play(FadeIn(cl, shift=UP * 0.1), run_time=0.7)
        end = self.narration_s - 0.5
        while self.elapsed() < end - 0.9:
            cycle(0.45)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s05: shape and charges fit
# ---------------------------------------------------------------------------------------------
class S05Fit(Film):
    def construct(self):
        enz, name = big_enzyme()
        circ = Circle(radius=1.15, stroke_color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=0.12).move_to([-4.6, 2.3, 0])
        bar = RoundedRectangle(corner_radius=0.2, width=3.0, height=0.6, stroke_color=TEXT, stroke_width=5,
                               fill_color=TEXT, fill_opacity=0.12).move_to([4.6, 1.5, 0])
        W = wedge(ES).move_to([-4.6, 0.4, 0])
        wl = lab("hydrogen peroxide", 28, ORANGE, [-4.7, -0.7, 0])
        for m, p in ((circ, 0.0), (bar, 1.5), (W, 3.0)):
            swim(m, 0.2, 0.15, 0.9, p)
        self.add(enz, name)
        self.play(FadeIn(circ), FadeIn(bar), FadeIn(W), FadeIn(wl), run_time=0.6)
        # the round shape tries first
        self.at("why does this pocket")
        rim = EC[1] + ES
        self.play(circ.animate.move_to([0, rim + 1.15 + 0.04, 0]), run_time=1.0, rate_func=smooth)
        olab = lab("other molecules", 30, TEXT, [4.6, 0.2, 0])
        self.play(circ.animate.shift(UP * 0.15), FadeIn(olab), run_time=0.2)
        self.play(circ.animate.move_to([-4.6, 2.3, 0]), run_time=0.6, rate_func=smooth)
        self.play(bar.animate.move_to([0, rim + 0.3 + 0.04, 0]), run_time=0.8, rate_func=smooth)
        self.play(bar.animate.shift(UP * 0.12), run_time=0.15)
        self.play(bar.animate.move_to([4.6, 1.5, 0]), run_time=0.6, rate_func=smooth)
        self.at("the active site's shape")
        outline = Polygon(*[EC + np.array([x * ES, y * ES, 0]) for x, y in [(-0.65, 1.0), (-0.45, 0.2), (0.45, 0.2), (0.65, 1.0)]],
                          stroke_color=TEXT, stroke_width=7, fill_opacity=0).set_stroke(TEXT, 7)
        self.play(Create(outline), FadeOut(olab), run_time=0.6)
        self.play(FadeOut(outline), run_time=0.3)
        self.at("electric charges")
        marks = VGroup(lab("+", 40, TEXT, EC + np.array([-1.05 * ES + 0.25, 0.55 * ES + 0.1, 0])),
                       lab("–", 40, TEXT, EC + np.array([1.05 * ES - 0.25, 0.55 * ES + 0.1, 0])),
                       lab("+", 40, TEXT, EC + np.array([0.0, 0.12 * ES - 0.1, 0])))
        self.play(FadeIn(marks, lag_ratio=0.3), run_time=0.6)
        wm = VGroup(lab("–", 36, BG, [0, 0, 0]), lab("+", 36, BG, [0, 0, 0]), lab("–", 36, BG, [0, 0, 0]))
        W.clear_updaters()
        self.play(W.animate.move_to([-4.2, 0.5, 0]), run_time=0.5)
        wm[0].move_to(W.get_center() + LEFT * 0.5 + UP * 0.05)
        wm[1].move_to(W.get_center() + RIGHT * 0.5 + UP * 0.05)
        wm[2].move_to(W.get_center() + DOWN * 0.18)
        wm[2].set_opacity(0)
        wg = VGroup(W, wm)
        self.play(FadeIn(wm[0]), FadeIn(wm[1]), FadeOut(wl), run_time=0.4)
        self.at("fit only certain")
        fl = lab("shape and charges fit", 34, TEXT, [0, -2.75, 0])
        self.play(wg.animate.move_to(POCKET + UP * 1.2), FadeIn(fl), run_time=0.8)
        self.play(wg.animate.move_to(POCKET), run_time=0.8, rate_func=smooth)
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.5) for m in list(marks[:2]) + list(wm[:2])], run_time=0.7)
        self.at("so each enzyme")
        self.play(FadeOut(fl), FadeOut(marks), wg.animate.move_to([-4.6, 0.4, 0]).set_opacity(0.0), run_time=1.5, rate_func=smooth)
        self.remove(wg)
        self.at("one reaction")
        ol = lab("usually one reaction", 34, BLUE, [0, -2.75, 0])
        self.play(FadeIn(ol), run_time=0.6)
        self.at("or a few similar")
        S = wedge(ES, narrow=0.9).move_to([-4.6, -0.2, 0])
        swim(S, 0.2, 0.15, 1.0)
        sl = lab("or a few similar ones", 34, ORANGE, [0, -2.75, 0])
        self.play(FadeIn(S), FadeOut(ol), FadeIn(sl), run_time=0.7)
        S.clear_updaters()
        self.play(S.animate.move_to(POCKET + UP * 0.9 + LEFT * 0.1), run_time=1.0)
        self.play(S.animate.move_to(POCKET + DOWN * 0.03), run_time=1.0, rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the energy graph (s06, s07)
# ---------------------------------------------------------------------------------------------
YL, YR = -0.3, -1.6


def curve_y(x, hh):
    sig = 1.0 / (1.0 + np.exp(-(x - 0.6) / 0.9))
    return YL + (YR - YL) * sig + hh * np.exp(-((x + 0.1) / 1.5) ** 2)


def hump_top(hh):
    xs = np.linspace(-1.5, 1.5, 61)
    return max(curve_y(x, hh) for x in xs)


def make_ball(Hh, x0, color=ORANGE, ph=0.0):
    b = Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)
    b.xt = ValueTracker(x0)
    b._tt = ph

    def u(m, dt):
        m._tt += dt
        x = m.xt.get_value() + 0.1 * np.sin(5.0 * m._tt + ph)
        y = curve_y(x, Hh.get_value()) + 0.28 + 0.1 * abs(np.sin(3.2 * m._tt + ph))
        m.move_to([x, y, 0])
        c = GREEN if x > 1.6 else ORANGE
        m.set_stroke(c).set_fill(c, 0.9)
    b.add_updater(u)
    return b


def graph_frame():
    ya = Line([-6.2, -2.6, 0], [-6.2, 3.1, 0], color=TEXT, stroke_width=4)
    xa = Line([-6.2, -2.6, 0], [6.4, -2.6, 0], color=TEXT, stroke_width=4)
    yl = lab("energy", 28, TEXT, [-6.55, 0.3, 0]).rotate(PI / 2)
    xl = lab("reaction progress", 28, TEXT, [0.1, -3.1, 0])
    tag = lab("schematic", 28, TEXT, [5.5, 3.4, 0])
    return VGroup(ya, xa, yl, xl, tag)


class S06Hill(Film):
    def construct(self):
        Hh = ValueTracker(3.2)
        col = ValueTracker(0.0)
        frame = graph_frame()
        curve = always_redraw(lambda: ParametricFunction(lambda t: np.array([t, curve_y(t, Hh.get_value()), 0.0]),
                                                         t_range=[-6.0, 6.2], stroke_width=7,
                                                         color=interpolate_color(ManimColor(TEXT), ManimColor(BLUE), col.get_value())))
        # activation-energy arrow
        AX = -2.7

        def act_arrow():
            top = hump_top(Hh.get_value())
            a = DoubleArrow([AX, YL, 0], [AX, top, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.2)
            d = DashedLine([AX, top, 0], [-0.1, top, 0], color=TEXT, stroke_width=3)
            return VGroup(a, d)
        self.play(Create(frame), run_time=1.0)
        self.play(Create(curve), run_time=1.6)
        balls = [make_ball(Hh, -5.1, ph=0.0), make_ball(Hh, -4.4, ph=1.0), make_ball(Hh, -3.7, ph=2.1)]
        self.at("picture a ball")
        self.play(FadeIn(VGroup(*balls)), run_time=0.8)
        self.at("pushed over a hill")
        b0 = balls[2]
        self.play(b0.xt.animate.set_value(-0.9), run_time=1.3, rate_func=smooth)
        self.play(b0.xt.animate.set_value(-3.0), run_time=0.8, rate_func=smooth)
        self.at("rolls down")
        self.play(b0.xt.animate.set_value(5.0), run_time=2.3, rate_func=smooth)
        self.at("activation energy")
        aa = act_arrow()
        alab = lab("activation\nenergy", 30, TEXT, [-4.3, 1.4, 0])
        self.play(FadeIn(aa), FadeIn(alab), run_time=0.9)
        arrow_live = always_redraw(act_arrow)
        self.remove(aa)
        self.add(arrow_live)
        self.at("like that hill")
        self.play(Indicate(alab, color=TEXT, scale_factor=1.12), run_time=1.0)
        self.at("an enzyme does not add")
        bolt = Polygon([0.15, 0.5, 0], [-0.2, 0.0, 0], [0.0, 0.0, 0], [-0.15, -0.5, 0], [0.25, 0.1, 0], [0.05, 0.1, 0],
                       stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.9).scale(1.1).move_to([-4.7, -1.2, 0])
        xx = VGroup(Line([-0.5, -0.5, 0], [0.5, 0.5, 0], color=RED, stroke_width=8), Line([-0.5, 0.5, 0], [0.5, -0.5, 0], color=RED, stroke_width=8)).move_to(bolt)
        nl = lab("no energy added", 28, TEXT, [-4.2, -2.2, 0])
        self.play(FadeIn(bolt), FadeIn(nl), run_time=0.5)
        self.play(Create(xx), run_time=0.6)
        el = chip("enzyme", BLUE, 30)
        el.move_to([3.4, 2.5, 0])
        self.play(FadeIn(el), col.animate.set_value(1.0), run_time=1.0)
        self.at("it lowers the hill")
        ghost = DashedVMobject(ParametricFunction(lambda t: np.array([t, curve_y(t, 3.2), 0.0]), t_range=[-2.4, 2.4], stroke_width=4, color=GREY), num_dashes=40)
        self.add(ghost)
        self.play(Hh.animate.set_value(1.6), FadeOut(bolt), FadeOut(xx), FadeOut(nl), run_time=2.2, rate_func=smooth)
        self.play(Indicate(alab, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.finish()


class S07More(Film):
    def construct(self):
        Hh = ValueTracker(1.6)
        frame = graph_frame()
        curve = always_redraw(lambda: ParametricFunction(lambda t: np.array([t, curve_y(t, Hh.get_value()), 0.0]),
                                                         t_range=[-6.0, 6.2], stroke_width=7, color=BLUE))
        rate = ValueTracker(0.14)
        nvis = ValueTracker(2.0)
        crossed = [0]
        balls = VGroup()
        N = 9
        for i in range(N):
            b = Circle(radius=0.28, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.9)
            b.p = i / N
            b.i = i
            b.done = False
            b.hop = 0.5 * i

            def u(m, dt):
                vis = m.i < nvis.get_value()
                m.p = (m.p + dt * rate.get_value()) % 1.0 if vis else m.p
                x = -5.4 + 11.0 * m.p
                y = curve_y(x, Hh.get_value()) + 0.28 + 0.1 * abs(np.sin(6 * m.p * 5 + m.hop))
                m.move_to([x, y, 0])
                c = GREEN if x > 1.6 else ORANGE
                a = 0.0 if not vis else min(1.0, m.p * 8, (1 - m.p) * 8)
                m.set_stroke(c, opacity=a).set_fill(c, 0.9 * a)
                if x > 1.6 and not m.done:
                    m.done = True
                    crossed[0] += 1
                if x <= 1.6:
                    m.done = False
            b.add_updater(u)
            balls.add(b)

        def counter():
            return T(f"crossed the hill: {crossed[0]}", 32, GREEN).move_to([-6.5, 3.3, 0], aligned_edge=LEFT)
        cnt = always_redraw(counter)
        self.add(frame, curve, balls)
        self.add(cnt)
        self.wait(0.1)
        self.at("many more")
        self.play(rate.animate.set_value(0.5), nvis.animate.set_value(9.0), run_time=1.8)
        self.at("the hill is a graph")
        tg = lab("a graph, not a place", 34, TEXT, [0.3, 2.3, 0])
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the tube world (s08 to s13)
# ---------------------------------------------------------------------------------------------
TUBE_C = np.array([-2.0, -0.95, 0.0])
GAUGE_C = np.array([5.0, 2.3, 0.0])
GAUGE_R = 1.1
BAR_X, BAR_BASE, BAR_H, BAR_W = 6.0, -3.0, 3.0, 1.0
BS = 0.5
SLOTS = [np.array([-5.0 + 2.05 * i, -0.35 if r == 0 else -2.25, 0.0]) for r in (0, 1) for i in range(4)]


class World:
    pass


def counter_text(n):
    return T(f"working sites: {n} of 8", 32, BLUE).move_to([-6.5, 3.4, 0], aligned_edge=LEFT)


def tube_world(scene, n=8, bad=None, gauge=True, bar=True, eq=True, counter=True, flash=True, speed=0.5, wedges=True, add=True):
    w = World()
    w.tube = RoundedRectangle(corner_radius=0.5, width=8.6, height=4.3, stroke_color=GREY, stroke_width=5,
                              fill_color=GREY, fill_opacity=0.1).move_to(TUBE_C)
    w.blocks = []
    for i, p in enumerate(SLOTS):
        if bad == i:
            b = enzyme(BS, GREY, ENZ_BAD, 0.4).move_to(p)
            b.flash_on = False
        else:
            b = enzyme(BS).move_to(p)
            b.flash_on = flash
        b.fp = 0.9 + 0.37 * i
        b._ft = 0.3 * i
        b.base = 0.35

        def uf(m, dt):
            m._ft += dt
            if m.flash_on:
                ph = (m._ft % (2.0 + 0.2 * (m.fp % 1))) / 0.45
                pulse = max(0.0, 1 - ph)
                m.set_fill(BLUE, 0.35 + 0.55 * pulse)
                m.set_stroke(BLUE, 4 + 3 * pulse)
        b.add_updater(uf)
        w.blocks.append(b)
    w.wedges = []
    if wedges:
        for i in range(8):
            wd = wedge(BS)
            wd.move_to([-4.2 + 1.85 * (i % 4), -1.3 if i < 4 else 0.68, 0])
            swim(wd, 0.45, 0.12, 0.7 + 0.1 * i, i * 1.3)
            w.wedges.append(wd)
    w.nt = ValueTracker(float(n))
    w.st = ValueTracker(speed)
    w.counter = counter_text(n)
    # gauge
    arc = Arc(radius=GAUGE_R, start_angle=0, angle=PI, stroke_color=YELLOW, stroke_width=7).move_to(GAUGE_C, aligned_edge=DOWN)
    arc.move_to(GAUGE_C + UP * GAUGE_R * 0.64)
    arc = Arc(radius=GAUGE_R, start_angle=0, angle=PI, stroke_color=YELLOW, stroke_width=7, arc_center=GAUGE_C)
    needle = Line(GAUGE_C, GAUGE_C + UP * GAUGE_R * 0.85, color=YELLOW, stroke_width=7)

    def un(m):
        th = PI * (1 - w.st.get_value())
        m.put_start_and_end_on(GAUGE_C, GAUGE_C + GAUGE_R * 0.85 * np.array([np.cos(th), np.sin(th), 0]))
    needle.add_updater(un)
    hub = Dot(GAUGE_C, radius=0.1, color=YELLOW)
    w.glabel = lab("speed per site", 28, YELLOW, GAUGE_C + DOWN * 0.55)
    w.gauge = VGroup(arc, needle, hub)
    # rate bar
    outline = Rectangle(width=BAR_W, height=BAR_H, stroke_color=PURPLE, stroke_width=4, fill_opacity=0).move_to([BAR_X, BAR_BASE + BAR_H / 2, 0])

    def bar_fill():
        h = max(BAR_H * (w.nt.get_value() / 8.0) * (w.st.get_value() / 0.5), 0.001)
        return Rectangle(width=BAR_W - 0.08, height=h, stroke_width=0, fill_color=PURPLE, fill_opacity=0.9).move_to(
            [BAR_X, BAR_BASE + h / 2 + 0.0, 0])
    w.barfill = always_redraw(bar_fill)
    w.bar = VGroup(outline)
    w.blab = lab("rate", 28, PURPLE, [BAR_X, -3.45, 0])
    # equation
    parts = [T("rate", 30, PURPLE), T("=", 30, TEXT), T("working sites", 30, BLUE), T("×", 30, TEXT), T("speed of each site", 30, YELLOW)]
    w.eqparts = parts
    w.eq = VGroup(*parts).arrange(RIGHT, buff=0.2).move_to([-1.6, 2.6, 0])
    if add:
        scene.add(w.tube, *w.blocks, *w.wedges)
        if counter:
            scene.add(w.counter)
        if gauge:
            scene.add(w.gauge, w.glabel)
        if bar:
            scene.add(w.bar, w.barfill, w.blab)
        if eq:
            scene.add(w.eq)
    return w


class S08Tube(Film):
    def construct(self):
        # start from the one big enzyme, then pull back
        enz, name = big_enzyme()
        wd = wedge(ES).move_to(POCKET)
        self.add(enz, name, wd)
        w = tube_world(self, counter=False, gauge=False, bar=False, eq=False, add=False)
        first = w.blocks[0]
        self.wait(0.4)
        self.at("pull back")
        self.play(enz.animate.scale(BS / ES).move_to(SLOTS[0]), FadeOut(name), FadeOut(wd),
                  Create(w.tube), *[FadeIn(b) for b in w.blocks[1:]], *[FadeIn(x) for x in w.wedges], run_time=1.8, rate_func=smooth)
        self.remove(enz)
        self.add(first)
        self.at("one per block")
        note = lab("simplified: 1 block = 1 site", 28, TEXT, [-2.0, -3.52, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.at("two things set")
        self.wait(0.1)
        self.at("first")
        self.play(FadeIn(w.counter, shift=RIGHT * 0.2), run_time=0.8)
        self.at("still in the shape")
        self.play(Indicate(w.counter, color=BLUE, scale_factor=1.06), run_time=0.9)
        self.at("second")
        self.play(FadeIn(w.gauge), FadeIn(w.glabel), run_time=0.9)
        self.at("how much product")
        self.play(w.st.animate.set_value(0.58), run_time=0.7)
        self.play(w.st.animate.set_value(0.42), run_time=0.7)
        self.play(w.st.animate.set_value(0.5), run_time=0.6)
        self.finish()


class S09Rule(Film):
    def construct(self):
        w = tube_world(self, bar=False, eq=False)
        note = lab("simplified: 1 block = 1 site", 28, TEXT, [-2.0, -3.52, 0])
        self.add(note)
        p = w.eqparts
        w.nt.set_value(0.0)
        self.at("the rate is the two")
        self.add(w.barfill)
        self.play(FadeIn(w.bar), FadeIn(w.blab), w.nt.animate.set_value(8.0), run_time=1.6)
        self.play(Write(p[0]), Write(p[1]), run_time=0.8)
        self.at("working sites")
        self.play(Write(p[2]), run_time=0.8)
        self.play(Write(p[3]), run_time=0.4)
        self.at("speed of each")
        self.play(Write(p[4]), run_time=1.0)
        self.play(w.st.animate.set_value(0.58), run_time=0.5)
        self.play(w.st.animate.set_value(0.5), run_time=0.5)
        self.at("a site makes product")
        b3 = w.blocks[2]
        b3.flash_on = False
        b3.set_fill(BLUE, 0.12).set_stroke(BLUE, 4)
        W3 = w.wedges[2]
        self.play(Indicate(b3, color=BLUE, scale_factor=1.2), run_time=0.9)
        self.at("while a substrate sits")
        W3.clear_updaters()
        self.play(W3.animate.move_to(b3.get_center() + UP * FIT * BS), run_time=1.3, rate_func=smooth)
        b3.flash_on = True
        b3._ft = 0.0
        self.play(Indicate(b3, color=BLUE, scale_factor=1.2), run_time=0.7)
        self.at("so temperature")
        chips = [chip(t, GREY, 28) for t in ("temperature", "pH", "substrate")]
        row = VGroup(*chips).arrange(RIGHT, buff=0.5).move_to([-1.6, 1.7, 0])
        for c in chips:
            c[1].set_color(TEXT)
        self.play(FadeIn(row, shift=UP * 0.15), run_time=0.8)

        def arrow_up(c, target):
            return Arrow(c.get_top(), [target.get_center()[0], 2.3, 0], buff=0.05, color=TEXT, stroke_width=4,
                         max_tip_length_to_length_ratio=0.5, tip_length=0.15)
        self.at("temperature")
        c0 = chips[0]
        self.play(c0[0].animate.set_stroke(TEXT, 4).set_fill(TEXT, 0.2), GrowArrow(arrow_up(c0, p[2])), GrowArrow(arrow_up(c0, p[4])), run_time=0.8)
        self.at("ph")
        c1 = chips[1]
        self.play(c1[0].animate.set_stroke(TEXT, 4).set_fill(TEXT, 0.2), GrowArrow(arrow_up(c1, p[2])), GrowArrow(arrow_up(c1, p[4])), run_time=0.8)
        self.at("the amount of substrate")
        c2 = chips[2]
        self.play(c2[0].animate.set_stroke(ORANGE, 4).set_fill(ORANGE, 0.2), GrowArrow(arrow_up(c2, p[4])), run_time=0.8)
        self.at("each turn one dial")
        self.play(Indicate(w.counter, color=BLUE, scale_factor=1.06), Indicate(w.glabel, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


class S10Predict(Film):
    def construct(self):
        w = tube_world(self)
        self.at("suppose one active site")
        bad = enzyme(BS, GREY, ENZ_BAD, 0.4).move_to(SLOTS[5])
        old = w.blocks[5]
        old.flash_on = False
        self.at("bent out of shape")
        self.play(Transform(old, bad), run_time=1.4)
        old.flash_on = False
        # a wedge bounces off it
        wd = w.wedges[5]
        wd.clear_updaters()
        top = SLOTS[5] + UP * 0.75
        self.at("no longer fits")
        for _ in range(2):
            self.play(wd.animate.move_to(top + UP * 0.55), run_time=0.5)
            self.play(wd.animate.move_to(top + UP * 0.02), run_time=0.4, rate_func=rush_into)
            self.play(wd.animate.move_to(top + UP * 0.8 + RIGHT * 0.5), run_time=0.4, rate_func=rush_from)
        swim(wd, 0.35, 0.22, 0.9, 0.0)
        self.at("what happens")
        q1 = lab("?", 56, TEXT, w.counter.get_right() + RIGHT * 0.4)
        q2 = lab("?", 56, TEXT, [BAR_X, BAR_BASE + BAR_H + 0.4, 0])
        self.play(FadeIn(q1), FadeIn(q2), run_time=0.5)
        self.play(Indicate(q1, color=TEXT, scale_factor=1.4), run_time=0.7)
        self.at("to the rate")
        self.play(Indicate(q2, color=TEXT, scale_factor=1.4), run_time=0.7)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        w = tube_world(self, bad=5)
        q1 = lab("?", 56, TEXT, w.counter.get_right() + RIGHT * 0.4)
        q2 = lab("?", 56, TEXT, [BAR_X, BAR_BASE + BAR_H + 0.4, 0])
        self.add(q1, q2)
        ptxt = lab("Predict: counter? rate bar?", 36, TEXT, [-2.0, 1.75, 0])
        self.add(ptxt)
        ring_bg = Circle(radius=0.38, stroke_color=GREY, stroke_width=5).move_to([4.4, 0.4, 0])
        tt = ValueTracker(0.0)
        ring = always_redraw(lambda: Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * max(tt.get_value(), 0.001),
                                         stroke_color=TEXT, stroke_width=7, arc_center=[4.4, 0.4, 0]))
        self.add(ring_bg, ring)
        self.play(tt.animate.set_value(1.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S12Reveal(Film):
    def construct(self):
        w = tube_world(self, bad=5)
        q1 = lab("?", 56, TEXT, w.counter.get_right() + RIGHT * 0.4)
        q2 = lab("?", 56, TEXT, [BAR_X, BAR_BASE + BAR_H + 0.4, 0])
        self.add(q1, q2)
        self.at("the counter drops")
        self.wait(0.2)
        self.at("seven of eight")
        self.play(Transform(w.counter, counter_text(7)), FadeOut(q1), run_time=0.8)
        self.at("that site is not working")
        self.play(Indicate(w.blocks[5], color=GREY, scale_factor=1.3), run_time=1.0)
        self.at("so the rate bar")
        self.play(w.nt.animate.set_value(7.0), FadeOut(q2), run_time=1.2)
        bt = BAR_BASE + BAR_H * 7 / 8
        bracket = VGroup(Line([BAR_X - 0.65, bt, 0], [BAR_X - 0.65, BAR_BASE + BAR_H, 0], color=PURPLE, stroke_width=5),
                         Line([BAR_X - 0.65, bt, 0], [BAR_X - 0.45, bt, 0], color=PURPLE, stroke_width=5),
                         Line([BAR_X - 0.65, BAR_BASE + BAR_H, 0], [BAR_X - 0.45, BAR_BASE + BAR_H, 0], color=PURPLE, stroke_width=5))
        bl = lab("1/8 of\nthe rate", 28, PURPLE, [4.35, BAR_BASE + BAR_H - 0.1, 0])
        self.at("shrinks by an eighth")
        self.play(FadeIn(bracket), FadeIn(bl), run_time=0.8)
        self.at("the other seven sites")
        sp = lab("speed per site:\nunchanged", 28, GREEN, GAUGE_C + DOWN * 0.8)
        self.play(Transform(w.glabel, sp), Indicate(w.gauge, color=YELLOW, scale_factor=1.05), run_time=1.0)
        self.at("run just as fast")
        self.play(*[Indicate(b, color=BLUE, scale_factor=1.15) for i, b in enumerate(w.blocks) if i != 5], run_time=1.2)
        self.finish()


class S13Close(Film):
    def construct(self):
        w = tube_world(self, n=7, bad=5)
        self.remove(w.tube)  # carried: the rebuilt state of film 12 is below, we start from it
        self.add(w.tube)
        w.counter.become(counter_text(7))
        w.glabel.become(lab("speed per site:\nunchanged", 28, GREEN, GAUGE_C + DOWN * 0.8))
        everything = [w.tube, *w.blocks, *w.wedges, w.counter, w.gauge, w.glabel, w.bar, w.barfill, w.blab, w.eq]
        self.wait(0.2)
        self.play(*[FadeOut(m) for m in everything], run_time=0.8)
        for m in everything:
            self.remove(m)
        # side by side
        lx, rx, cy = -3.6, 3.6, 0.2
        badb = enzyme(1.5, GREY, ENZ_BAD, 0.4).move_to([lx, cy, 0])
        goodb = enzyme(1.5).move_to([rx, cy, 0])
        swim(badb, 0.05, 0.05, 1.5)
        # a wedge bounces off the bent block, again and again
        wb = wedge(1.5).move_to([lx, cy + 2.4, 0])
        wb._tt = 0.0
        topb = cy + 1.1 * 1.5 + 0.35

        def ub(m, dt):
            m._tt += dt
            ph = (m._tt % 2.4) / 2.4
            y = topb + 0.1 + 0.9 * abs(np.cos(PI * ph * 1.0))
            m.move_to([lx - 0.1 + 0.25 * np.sin(1.4 * m._tt), y, 0])
        wb.add_updater(ub)
        # the working block cycles
        wg = wedge(1.5).move_to([rx, cy + 2.5, 0])
        pg = products([rx, cy + 0.6, 0], 1.5)
        wg._tt = 0.0
        pocket_y = cy + FIT * 1.5

        def ug(m, dt):
            m._tt += dt
            ph = (m._tt % 3.0) / 3.0
            if ph < 0.4:
                m.move_to([rx, cy + 2.5 - (2.5 - FIT * 1.5) * smooth(ph / 0.4), 0])
                m.set_opacity(1)
                pg.set_opacity(0)
                goodb.set_fill(BLUE, 0.35)
            elif ph < 0.55:
                m.move_to([rx, pocket_y, 0])
                m.set_opacity(1)
                pg.set_opacity(0)
                goodb.set_fill(BLUE, 0.35 + 0.5 * (ph - 0.4) / 0.15)
            else:
                m.set_opacity(0)
                q = (ph - 0.55) / 0.45
                pg.move_to([rx + 1.2 * q, pocket_y + 0.4 + 1.6 * q, 0])
                pg.set_opacity(1 - q)
                goodb.set_fill(BLUE, 0.35)
        wg.add_updater(ug)
        nl = lab("not working", 40, TEXT, [lx, -2.1, 0])
        gl = lab("working", 40, BLUE, [rx, -2.1, 0])
        self.play(FadeIn(badb), FadeIn(goodb), run_time=1.0)
        self.add(wb, wg, pg)
        self.at("does not work slowly")
        self.play(FadeIn(nl, shift=UP * 0.1), FadeIn(gl, shift=UP * 0.1), run_time=0.8)
        self.at("it does not work at all")
        self.play(Indicate(nl, color=TEXT, scale_factor=1.15), run_time=1.0)
        self.at("anything that bends")
        grp = [badb, goodb, wb, wg, pg, nl, gl]
        w2 = tube_world(self, n=7, bad=5, add=False)
        w2.glabel = lab("speed per site:\nunchanged", 28, GREEN, GAUGE_C + DOWN * 0.8)
        w2.counter = counter_text(7)
        for m in grp:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in grp], run_time=0.6)
        self.add(w2.tube, *w2.blocks, *w2.wedges, w2.counter, w2.gauge, w2.glabel, w2.bar, w2.barfill, w2.blab, w2.eq)
        w2.nt.set_value(7.0)
        self.add(*[FadeIn(m).mobject for m in []])
        self.at("lowers the count")
        self.play(Indicate(w2.counter, color=BLUE, scale_factor=1.12), run_time=1.0)
        self.finish()


class S14End(EndCard):
    LINE = "Rate = working active sites × speed of each site."
