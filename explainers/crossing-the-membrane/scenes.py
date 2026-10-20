"""Crossing the membrane: water follows the salt  (Biochemistrypedia explainer, high school Biology)

COLOR MAP (one color per concept, whole video)
  BLUE   = water (arrows of water movement, distilled water, the water in the beakers)
  YELLOW = dissolved particles: salt, sodium and chloride ions (solute)
  PINK   = potassium ions
  TEAL   = oxygen (a small molecule that slips through the lipid layers)
  PURPLE = membrane proteins (channel, pump)
  GOLD   = ATP
  ORANGE = plant cell wall and the push on it (turgor pressure)
  GREEN  = plant tissue (cucumber slice, plant cell)
  RED    = lost / blocked / stopped
  GREY   = membranes, outlines, neutral labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E58FB5"
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
TEAL_O = "#3FB8C0"
WATER = BLUE


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def dot(color, pos, r=0.14, ring=False):
    d = Circle(radius=r, stroke_color=WHITE if ring else color, stroke_width=3 if ring else 1,
               fill_color=color, fill_opacity=1)
    return d.move_to([pos[0], pos[1], 0])


def lab(text, color=TEXT, size=24, **kw):
    return T(text, size, color, **kw)


def bar(y, x0=-5.9, x1=5.9, h=0.5, color=GREY):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def prot(x, y, w=0.8, h=1.5, color=PURPLE):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.45).move_to([x, y, 0])


def cross(center, s=0.22, color=RED):
    c = np.array([center[0], center[1], 0.0])
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=8),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=8))


class S00Title(TitleCard):
    LESSON = "Crossing the membrane"
    TITLE = "Water follows the salt"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        rng = np.random.RandomState(3)

        def beaker(x):
            glass = Rectangle(width=4.8, height=3.6, stroke_color=GREY, stroke_width=4).move_to([x, -0.4, 0])
            water = Rectangle(width=4.7, height=2.8, stroke_width=0, fill_color=WATER, fill_opacity=0.22)
            water.move_to([x, glass.get_bottom()[1] + 0.05 + 1.4, 0])
            return VGroup(glass, water)

        bl, br = beaker(-3.4), beaker(3.4)
        sl = RoundedRectangle(corner_radius=0.2, width=2.9, height=0.7, stroke_color=GREEN, stroke_width=4,
                              fill_color=GREEN, fill_opacity=0.5).move_to([-3.4, -0.9, 0])
        sr = sl.copy().move_to([3.4, -0.9, 0])
        cap_l = lab("cucumber slice", TEXT, 22).move_to(sl)
        cap_r = lab("cucumber slice", TEXT, 22).move_to(sr)
        t_l = lab("salty water", YELLOW, 32, weight=BOLD).move_to([-3.4, 1.8, 0])
        t_r = lab("distilled water", WATER, 32, weight=BOLD).move_to([3.4, 1.8, 0])
        pts = []
        while len(pts) < 11:
            p = (rng.uniform(-4.3, -2.5), rng.uniform(-2.0, 0.35))
            if abs(p[1] + 0.9) > 0.55 or abs(p[0] + 3.4) > 1.55:
                pts.append(p)
        salt = VGroup(*[dot(YELLOW, p, 0.1) for p in pts])

        self.at("cucumber slice")
        self.play(FadeIn(bl), FadeIn(br), FadeIn(sl), FadeIn(sr), FadeIn(cap_l), FadeIn(cap_r), run_time=0.7)
        self.at("salty water")
        self.play(FadeIn(t_l), LaggedStart(*[FadeIn(d, scale=0.5) for d in salt], lag_ratio=0.08), run_time=0.9)
        self.at("lighter")
        lt = lab("lighter", RED, 36, weight=BOLD).move_to([-3.4, -3.0, 0])
        da = arr([-4.7, -2.75, 0], [-4.7, -3.3, 0], RED)
        self.play(sl.animate.stretch(0.9, 0).stretch(0.8, 1).move_to([-3.4, -0.9, 0]), FadeIn(lt), GrowArrow(da), run_time=0.7)
        self.at("goes soft")
        soft = lab("and soft", RED, 36, weight=BOLD).next_to(lt, RIGHT, buff=0.25)
        self.play(FadeIn(soft), run_time=0.4)
        self.at("distilled water")
        self.play(FadeIn(t_r), run_time=0.5)
        self.at("heavier")
        ht = lab("heavier", WATER, 36, weight=BOLD).move_to([3.4, -3.0, 0])
        ua = arr([2.1, -3.3, 0], [2.1, -2.75, 0], WATER)
        self.play(sr.animate.stretch(1.2, 0).stretch(1.2, 1).move_to([3.4, -0.9, 0]), FadeIn(ht), GrowArrow(ua), run_time=0.7)

        # --- the edge of the cell -------------------------------------------------------------
        self.at("Something crossed")
        old = VGroup(bl, br, sl, sr, cap_l, cap_r, t_l, t_r, salt, lt, da, soft, ht, ua)
        mem = bar(0.5, -4.5, 4.5, 0.5)
        edge = lab("the edge of a cell", GREY, 26).move_to([0, 1.05, 0])
        self.play(FadeOut(old), run_time=0.5)
        self.play(FadeIn(mem), FadeIn(edge), run_time=0.5)
        self.at("opposite directions")
        a1 = arr([-2.1, 2.2, 0], [-2.1, -0.9, 0], GREY)
        a2 = arr([2.1, -0.9, 0], [2.1, 2.2, 0], GREY)
        q1 = lab("?", TEXT, 56, weight=BOLD).move_to([-2.8, 1.7, 0])
        q2 = lab("?", TEXT, 56, weight=BOLD).move_to([2.8, 1.7, 0])
        edge2 = lab("", GREY, 22)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(q1), FadeIn(q2), run_time=0.8)
        edge_b = lab("the edge of a cell", GREY, 26).move_to([0, -0.05, 0]).shift(DOWN * 0.0)
        self.at("How does a cell")
        qa = lab("How does a cell control what gets in and out?", TEXT, 34, weight=BOLD).move_to([0, -1.9, 0])
        fit(qa)
        self.play(FadeIn(qa, shift=UP * 0.15), run_time=0.7)
        self.at("lettuce wilt")
        qb = lab("Why does salt water make lettuce wilt?", YELLOW, 34, weight=BOLD).move_to([0, -2.8, 0])
        fit(qb)
        self.play(FadeIn(qb, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Membrane(SpokenScene):
    def construct(self):
        top = RoundedRectangle(corner_radius=0.12, width=11.8, height=0.46, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([0, 0.27, 0])
        bot = top.copy().move_to([0, -0.27, 0])
        mem = VGroup(top, bot)
        out_l = lab("outside", GREY, 26).move_to([-5.3, 1.5, 0])
        in_l = lab("inside", GREY, 26).move_to([-5.3, -1.5, 0])
        p1, p2 = prot(-3.9, 0), prot(5.0, 0)

        self.at("cell membrane")
        self.play(FadeIn(mem, scale=0.95), FadeIn(out_l), FadeIn(in_l), run_time=0.8)
        self.at("double layer")
        lbl = lab("double layer of phospholipids", TEXT, 28).move_to([0.6, -1.6, 0])
        br = BraceBetweenPoints([-5.9, -0.55, 0], [5.9, -0.55, 0], direction=DOWN, color=GREY).scale(0.6, about_point=[0, -0.55, 0])
        br.set_stroke(width=3)
        lbl.next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(lbl), run_time=0.7)
        self.at("with proteins in it")
        pl = lab("protein", PURPLE, 26).move_to([-3.9, 1.2, 0])
        pl2 = lab("protein", PURPLE, 26).move_to([5.0, 1.2, 0])
        self.play(FadeOut(lbl), FadeOut(br), FadeIn(p1, scale=0.6), FadeIn(p2, scale=0.6), FadeIn(pl), FadeIn(pl2), run_time=0.8)
        self.at("selectively permeable")
        title = lab("selectively permeable", TEXT, 42, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeOut(pl), FadeOut(pl2), FadeIn(title, shift=DOWN * 0.1), run_time=0.6)

        # oxygen passes
        self.at("Small molecules")
        ox = VGroup(dot(TEAL_O, [0, 0], 0.17), lab("oxygen", TEAL_O, 24)).arrange(RIGHT, buff=0.15).move_to([-0.2, 2.1, 0])
        self.play(FadeIn(ox, scale=0.7), run_time=0.4)
        self.at("slip through")
        self.play(ox.animate.move_to([-0.2, -2.1, 0]), run_time=1.3, rate_func=smooth)

        # ions bounce
        self.at("Charged ions")
        na = VGroup(dot(YELLOW, [0, 0], 0.17), lab("sodium", YELLOW, 24)).arrange(RIGHT, buff=0.12).move_to([1.8, 2.1, 0])
        cl = VGroup(dot(YELLOW, [0, 0], 0.17), lab("chloride", YELLOW, 24)).arrange(RIGHT, buff=0.12).move_to([3.1, 2.7, 0])
        self.play(FadeIn(na, scale=0.7), FadeIn(cl, scale=0.7), run_time=0.5)
        self.play(na.animate.shift(DOWN * 0.95), cl.animate.shift(DOWN * 0.95), run_time=0.6)
        xs = VGroup(cross([1.7, 0.95]), cross([3.0, 0.95]))
        self.play(FadeIn(xs), run_time=0.2)
        self.play(na.animate.shift(UP * 0.45), cl.animate.shift(UP * 0.45), FadeOut(xs), run_time=0.4)
        self.at("only through proteins")
        self.play(na.animate.move_to([-3.2, 1.4, 0]), cl.animate.move_to([4.2, 1.4, 0]), run_time=0.9)
        self.play(na.animate.move_to([-3.2, -1.4, 0]), cl.animate.move_to([4.2, -1.4, 0]), run_time=1.2)
        # dots pass through the protein: shift ahead of labels staying readable
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Passive(SpokenScene):
    def construct(self):
        rng = np.random.RandomState(7)
        mem = bar(0, -5.9, 5.9, 0.5)
        p = prot(4.3, 0, 0.9, 1.3)
        head = lab("passive transport", TEXT, 40, weight=BOLD).move_to([0, 3.15, 0])

        def spots(n, ylo, yhi, xlo=-3.4, xhi=2.6):
            out = []
            while len(out) < n:
                q = (rng.uniform(xlo, xhi), rng.uniform(ylo, yhi))
                if all((q[0] - o[0]) ** 2 + (q[1] - o[1]) ** 2 > 0.45 for o in out):
                    out.append(q)
            return out

        up = [dot(TEAL_O, q, 0.14) for q in spots(11, 0.7, 2.6)]
        dn = [dot(TEAL_O, q, 0.14) for q in spots(2, -2.6, -0.7)]
        many, few = VGroup(*up), VGroup(*dn)
        oxl = lab("oxygen", TEAL_O, 24).move_to([-3.9, 0.5, 0])

        self.at("Passive transport")
        self.play(FadeIn(mem), FadeIn(head), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in list(many) + list(few)], lag_ratio=0.05), run_time=0.9)
        self.at("more concentrated")
        more = lab("more", GREY, 28).move_to([-4.9, 2.3, 0])
        less = lab("fewer", GREY, 28).move_to([-4.9, -2.3, 0])
        big = arr([-5.8, 2.7, 0], [-5.8, -2.7, 0], GREY, w=8, tip=0.4)
        self.play(FadeIn(more), GrowArrow(big), run_time=0.5)
        self.at("less concentrated")
        self.play(FadeIn(less), run_time=0.4)
        self.at("uses no energy")
        ne = chip("no energy from the cell", GOLD, size=28).move_to([1.0, -3.1, 0])
        self.play(FadeIn(ne, shift=UP * 0.1), run_time=0.5)
        self.at("concentration gradient")
        h2 = lab("concentration gradient", TEXT, 40, weight=BOLD).move_to([0, 3.15, 0])
        self.play(ReplacementTransform(head, h2), run_time=0.5)
        self.at("move at random")
        for _ in range(2):
            self.play(*[d.animate.shift([rng.uniform(-0.35, 0.35), rng.uniform(-0.3, 0.3), 0]) for d in list(many) + list(few)],
                      run_time=0.55)
        self.at("more cross")
        # three crowded-side dots cross the lipid layers, nothing crosses back
        movers = [many[0], many[3], many[7]]
        self.play(*[m.animate.move_to([m.get_center()[0], -1.2 - 0.5 * i, 0]) for i, m in enumerate(movers)],
                  run_time=1.6, rate_func=smooth)
        self.at("Diffusion")
        h3 = lab("diffusion", TEXT, 40, weight=BOLD).move_to([0, 3.15, 0])
        self.play(ReplacementTransform(h2, h3), run_time=0.4)
        self.at("Facilitated diffusion")
        h4 = lab("facilitated diffusion", TEXT, 40, weight=BOLD).move_to([0, 3.15, 0])
        pl = lab("membrane protein", PURPLE, 24).move_to([4.3, -1.15, 0])
        ys = [dot(YELLOW, [3.6, 1.8], 0.14), dot(YELLOW, [4.3, 1.4], 0.14), dot(YELLOW, [5.0, 2.0], 0.14)]
        self.play(ReplacementTransform(h3, h4), FadeIn(p, scale=0.6), FadeIn(pl),
                  *[FadeIn(y_, scale=0.5) for y_ in ys], run_time=0.8)
        self.at("through a membrane protein")
        self.play(*[y_.animate.move_to([4.3, -1.8 - 0.05 * i, 0]) for i, y_ in enumerate(ys)], run_time=1.8, rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Osmosis(SpokenScene):
    def construct(self):
        # ---- part A: water across a membrane toward the solute side -------------------------
        wall = RoundedRectangle(corner_radius=0.1, width=0.4, height=4.4, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.35).move_to([0, -0.5, 0])
        sol_l = [(-5.0, 1.8), (-3.2, 1.0), (-4.2, -0.4), (-2.2, -1.1), (-5.1, -1.6), (-3.1, -2.2), (-1.5, 1.9)]
        sol_r = [(2.6, 1.0), (4.4, -1.4)]
        left = VGroup(*[dot(YELLOW, q, 0.14) for q in sol_l])
        right = VGroup(*[dot(YELLOW, q, 0.14) for q in sol_r])
        head = lab("osmosis", TEXT, 42, weight=BOLD).move_to([0, 3.15, 0])
        netw = lab("net movement of water", WATER, 32, weight=BOLD).move_to([0, 2.45, 0])
        self.at("Osmosis")
        self.play(FadeIn(wall), FadeIn(head), run_time=0.5)
        self.at("net movement of water")
        w1 = arr([1.0, -0.5, 0], [-1.0, -0.5, 0], WATER, w=10, tip=0.4)
        self.play(FadeIn(netw), run_time=0.5)
        self.at("selectively permeable membrane")
        sp = lab("selectively permeable membrane", GREY, 26).move_to([0, -2.95, 0])
        self.play(FadeIn(sp), run_time=0.4)
        self.at("On balance")
        more = lab("more solute", YELLOW, 28, weight=BOLD).move_to([-3.6, -2.95, 0])
        less = lab("less solute", YELLOW, 28, weight=BOLD).move_to([3.6, -2.95, 0])
        self.play(FadeOut(sp), FadeIn(left, lag_ratio=0.1), FadeIn(right), FadeIn(more), FadeIn(less), run_time=0.8)
        self.at("toward the side")
        self.play(GrowArrow(w1), run_time=0.7)
        self.at("less free water")
        lf = lab("less free water", WATER, 28).move_to([-3.6, 2.45, 0])
        self.play(FadeIn(lf), FadeOut(netw), run_time=0.5)

        # ---- part B: three cells ----------------------------------------------------------------
        self.at("Saltier outside")
        partA = VGroup(wall, left, right, more, less, w1, lf, head)
        self.play(FadeOut(partA), run_time=0.5)

        def ring_dots(cx, n, r=2.05):
            pts, k = [], 0
            angles = [a for a in range(0, 360, 20) if min(abs(a - b) % 360 if abs(a - b) % 360 <= 180 else 360 - abs(a - b) % 360
                                                              for b in (90, 210, 330)) > 26]
            sel = angles[:: max(1, len(angles) // n)][:n]
            return [dot(YELLOW, [cx + r * np.cos(np.radians(a)), 0.2 + r * np.sin(np.radians(a)), 0], 0.12) for a in sel]

        def inside(cx):
            return [dot(YELLOW, [cx + dx, 0.2 + dy, 0], 0.12) for dx, dy in [(-0.45, 0.35), (0.4, 0.4), (-0.35, -0.4), (0.45, -0.3)]]

        def cell(cx, r):
            return Circle(radius=r, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.18).move_to([cx, 0.2, 0])

        def ring_arrows(cx, kind):
            out = []
            for a in (90, 210, 330):
                u = np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
                c = np.array([cx, 0.2, 0]) + u * 1.45
                if kind == "out":
                    out.append(arr(c - u * 0.35, c + u * 0.35, WATER, w=8, tip=0.28))
                elif kind == "in":
                    out.append(arr(c + u * 0.35, c - u * 0.35, WATER, w=8, tip=0.28))
                else:
                    out.append(arr(c - u * 0.35 + np.array([-u[1], u[0], 0]) * 0.12, c + u * 0.35 + np.array([-u[1], u[0], 0]) * 0.12, WATER, w=6, tip=0.22))
                    out.append(arr(c + u * 0.35 - np.array([-u[1], u[0], 0]) * 0.12, c - u * 0.35 - np.array([-u[1], u[0], 0]) * 0.12, WATER, w=6, tip=0.22))
            return VGroup(*out)

        rbc = lab("red blood cells", GREY, 30).move_to([0, 3.15, 0])
        self.play(FadeIn(rbc), run_time=0.3)
        # hypertonic (left), hypotonic (middle), isotonic (right)
        xs = [-4.1, 0.0, 4.1]
        # hypertonic
        c1 = cell(xs[0], 1.15)
        d1o, d1i = VGroup(*ring_dots(xs[0], 11)), VGroup(*inside(xs[0]))
        self.play(FadeIn(c1), FadeIn(d1i), FadeIn(d1o, lag_ratio=0.1), run_time=0.8)
        self.at("and water leaves")
        t1 = lab("hypertonic", RED, 36, weight=BOLD).move_to([xs[0], -2.55, 0])
        s1 = lab("water leaves", WATER, 28).move_to([xs[0], -3.15, 0])
        a1 = ring_arrows(xs[0], "out")
        self.play(FadeIn(t1), FadeIn(s1), LaggedStart(*[GrowArrow(a) for a in a1], lag_ratio=0.15),
                  c1.animate.scale(0.82), run_time=1.0)
        # hypotonic
        self.at("Less salty outside")
        c2 = cell(xs[1], 1.15)
        d2o, d2i = VGroup(*ring_dots(xs[1], 2)), VGroup(*inside(xs[1]))
        self.play(FadeIn(c2), FadeIn(d2i), FadeIn(d2o), run_time=0.6)
        self.at("and water enters")
        t2 = lab("hypotonic", WATER, 36, weight=BOLD).move_to([xs[1], -2.55, 0])
        s2 = lab("water enters", WATER, 28).move_to([xs[1], -3.15, 0])
        a2 = ring_arrows(xs[1], "in")
        self.play(FadeIn(t2), FadeIn(s2), LaggedStart(*[GrowArrow(a) for a in a2], lag_ratio=0.15),
                  c2.animate.scale(1.2), run_time=1.0)
        # isotonic
        self.at("Equal is")
        c3 = cell(xs[2], 1.15)
        d3o, d3i = VGroup(*ring_dots(xs[2], 4)), VGroup(*inside(xs[2]))
        self.play(FadeIn(c3), FadeIn(d3i), FadeIn(d3o), run_time=0.6)
        self.at("both ways")
        t3 = lab("isotonic", GREY, 36, weight=BOLD).move_to([xs[2], -2.55, 0])
        s3 = lab("water crosses both ways", WATER, 24).move_to([xs[2], -3.15, 0])
        a3 = ring_arrows(xs[2], "both")
        self.play(FadeIn(t3), FadeIn(s3), LaggedStart(*[GrowArrow(a) for a in a3], lag_ratio=0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Active(SpokenScene):
    def construct(self):
        mem = bar(0, -5.9, 5.9, 0.5)
        pump = prot(0, 0, 1.3, 1.7)
        pl = lab("pump", PURPLE, 26).move_to([0, 0.0, 0])
        pump_group = VGroup(pump, pl)
        head = lab("active transport", TEXT, 40, weight=BOLD).move_to([0, 3.15, 0])
        # legend
        lg = VGroup(VGroup(dot(YELLOW, [0, 0], 0.14), lab("sodium ion", YELLOW, 24)).arrange(RIGHT, buff=0.15),
                    VGroup(dot(PINK, [0, 0], 0.14), lab("potassium ion", PINK, 24)).arrange(RIGHT, buff=0.15)
                    ).arrange(RIGHT, buff=0.8).move_to([0, -3.2, 0])
        fy_top = [(-5.0, 1.8), (-3.8, 2.5), (-4.4, 1.0), (3.6, 1.6), (4.8, 2.4), (5.2, 1.2)]
        fp_bot = [(-5.1, -1.8), (-3.9, -2.4), (-4.4, -1.0), (3.9, -2.3), (5.0, -1.4), (5.3, -2.5)]
        fixed = VGroup(*[dot(YELLOW, q) for q in fy_top], *[dot(PINK, q) for q in fp_bot])
        na = [dot(YELLOW, q, ring=True) for q in [(-0.8, -1.7), (0.0, -2.2), (0.8, -1.7)]]
        kk = [dot(PINK, q, ring=True) for q in [(-0.5, 1.8), (0.5, 2.1)]]
        atp = chip("ATP", GOLD, size=30).move_to([2.6, -1.1, 0])

        self.at("Active transport")
        self.play(FadeIn(mem), FadeIn(pump_group, scale=0.7), FadeIn(head), FadeIn(fixed), FadeIn(lg),
                  *[FadeIn(d) for d in na + kk], run_time=0.9)
        self.at("often from")
        self.play(FadeIn(atp, shift=LEFT * 0.2), run_time=0.5)
        self.at("against its concentration gradient")
        h2 = lab("against the concentration gradient", TEXT, 36, weight=BOLD).move_to([0, 3.15, 0])
        fit(h2)
        self.play(ReplacementTransform(head, h2), run_time=0.5)
        self.at("spends")
        self.play(atp.animate.move_to([0, -1.15, 0]).scale(0.9), run_time=0.6)
        self.play(Indicate(pump, color=GOLD, scale_factor=1.12), run_time=0.5)
        self.at("three sodium ions out")
        c1 = lab("3 out", YELLOW, 32, weight=BOLD).move_to([2.0, 1.2, 0])
        self.play(FadeIn(c1), *[d.animate.move_to([-0.6 + 0.6 * i, 1.7 + 0.35 * (i % 2), 0]) for i, d in enumerate(na)],
                  run_time=1.6, rate_func=smooth)
        self.at("two potassium ions in")
        c2 = lab("2 in", PINK, 32, weight=BOLD).move_to([-2.0, -1.2, 0])
        self.play(FadeIn(c2), *[d.animate.move_to([-0.35 + 0.7 * i, -1.9 - 0.35 * i, 0]) for i, d in enumerate(kk)],
                  run_time=1.6, rate_func=smooth)
        self.at("Both trips go uphill")
        h3 = lab("both trips go uphill", TEXT, 40, weight=BOLD).move_to([0, 3.15, 0])
        self.play(ReplacementTransform(h2, h3), FadeOut(atp), run_time=0.5)
        self.at("Without")
        atp2 = chip("no ATP", RED, size=30).move_to([0, -1.15, 0])
        self.play(FadeIn(atp2), pump.animate.set_stroke(RED).set_fill(RED, 0.25), pl.animate.set_color(RED), run_time=0.6)
        self.at("the pump stops")
        stop = lab("the pump stops", RED, 40, weight=BOLD).move_to([0, 3.15, 0])
        self.play(ReplacementTransform(h3, stop), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.25, width=3.8, height=2.6, stroke_color=GREEN, stroke_width=5,
                                fill_color=GREEN, fill_opacity=0.18).move_to([0, 0, 0])
        wall = RoundedRectangle(corner_radius=0.3, width=4.4, height=3.2, stroke_color=ORANGE, stroke_width=12,
                                fill_opacity=0).move_to([0, 0, 0])
        name = lab("cucumber cell", TEXT, 26).move_to([0, 0, 0])
        inn = VGroup(*[dot(YELLOW, q, 0.12) for q in [(-1.2, 0.8), (1.2, 0.8), (-1.2, -0.8), (1.2, -0.8)]])
        grid_l = [(x, y) for x in (-4.3, -5.3) for y in (-2.2, -0.8, 0.6, 2.0)]
        grid_r = [(x, y) for x in (4.3, 5.3) for y in (-2.2, -0.8, 0.6, 2.0)]
        out_d = VGroup(*[dot(YELLOW, q, 0.12) for q in grid_l + grid_r])
        keep = [0, 15]
        head = lab("salty water", YELLOW, 40, weight=BOLD).move_to([0, 3.15, 0])

        def side_arrows(kind):
            g = []
            for sgn in (-1, 1):
                for y in (0.7, -0.7):
                    a, b = [sgn * 2.55, y, 0], [sgn * 3.55, y, 0]
                    g.append(arr(a, b, WATER, w=8, tip=0.28) if kind == "out" else arr(b, a, WATER, w=8, tip=0.28))
            return VGroup(*g)

        self.at("back to the cucumber")
        self.play(FadeIn(cell), FadeIn(name), FadeIn(inn), run_time=0.6)
        self.at("The salty water")
        self.play(FadeIn(head), FadeIn(out_d, lag_ratio=0.05), run_time=0.8)
        self.at("hypertonic")
        h2 = lab("hypertonic to the cells", RED, 40, weight=BOLD).move_to([0, 3.15, 0])
        self.play(ReplacementTransform(head, h2), run_time=0.4)
        self.at("water left them")
        ao = side_arrows("out")
        self.play(LaggedStart(*[GrowArrow(a) for a in ao], lag_ratio=0.12), run_time=0.9)
        self.at("stiff wall")
        wl = lab("stiff cell wall", ORANGE, 28).move_to([0, 2.15, 0])
        self.play(FadeOut(ao), Create(wall), FadeIn(wl), run_time=0.8)
        self.at("Water flowing in")
        # fewer dots outside: water-like surroundings, arrows now point in
        dim = [out_d[i] for i in range(len(out_d)) if i not in keep]
        ai = side_arrows("in")
        press = VGroup(*[arr([x, 1.15, 0], [x, 1.6, 0], ORANGE, w=7, tip=0.2) for x in (-1.2, 1.2)],
                       *[arr([x, -1.15, 0], [x, -1.6, 0], ORANGE, w=7, tip=0.2) for x in (-1.2, 1.2)])
        lso = lab("less salty outside", WATER, 36, weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(lso), *[d.animate.set_opacity(0.0) for d in dim], FadeOut(h2), FadeOut(wl),
                  LaggedStart(*[GrowArrow(a) for a in ai], lag_ratio=0.1), run_time=0.9)
        self.at("press on the wall")
        self.play(LaggedStart(*[GrowArrow(a) for a in press], lag_ratio=0.1), run_time=0.7)
        self.at("turgor pressure")
        tp = lab("turgor pressure", ORANGE, 44, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(tp, shift=DOWN * 0.1), run_time=0.5)
        self.at("In salty water")
        h3 = lab("turgor lost", RED, 44, weight=BOLD).move_to([0, 3.0, 0])
        ao2 = side_arrows("out")
        self.play(FadeOut(lso), *[d.animate.set_opacity(1.0) for d in dim], FadeOut(ai), FadeOut(press),
                  ReplacementTransform(tp, h3), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in ao2], lag_ratio=0.1), run_time=0.7)
        self.at("goes soft")
        soft = lab("the slice goes soft", RED, 36, weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(soft, shift=UP * 0.1), run_time=0.5)
        self.at("Lettuce wilts")
        let = lab("lettuce wilts the same way", GREEN, 36, weight=BOLD).move_to([0, -3.0, 0])
        self.play(ReplacementTransform(soft, let), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "The membrane chooses what crosses; water moves toward more solute."
