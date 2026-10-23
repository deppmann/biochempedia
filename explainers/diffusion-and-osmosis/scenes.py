"""Diffusion and osmosis: water moves toward more dissolved particles  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole film)
  BLUE   = water (drops, water particles, the water in a glass or bowl)
  YELLOW = a dissolved substance that diffuses (food-colouring dye, oxygen)
  ORANGE = dissolved salt (the particles the model membrane holds back)
  GREEN  = living tissue and cells (cucumber, lettuce, cell outlines)
  TEAL   = vocabulary words and terms as they are defined
  GREY   = membranes, glass, outlines, neutral labels
  TEXT   = questions and the take-home line
Every dot is a labelled schematic particle. Nothing is a molecule; nothing is to scale.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


def vocab(text, size=36):
    return chip(text, TEAL, size=size)


def arr(a, b, color=GREY, w=6):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=0.28,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def P(x, y):
    return np.array([x, y, 0.0])


def dots(pts, color, r=0.1):
    return VGroup(*[Dot(P(*p) if len(p) == 2 else p, radius=r, color=color) for p in pts])


def grid_pts(rng, x0, x1, y0, y1, nx, ny, jit=0.35):
    out = []
    for i in range(nx):
        for j in range(ny):
            x = x0 + (i + 0.5) * (x1 - x0) / nx + rng.uniform(-jit, jit) * (x1 - x0) / nx
            y = y0 + (j + 0.5) * (y1 - y0) / ny + rng.uniform(-jit, jit) * (y1 - y0) / ny
            out.append((x, y))
    return out


def drift(mobs, targets, rt, amp=0.22, seed=1):
    """Move each dot to its target along a wobbly path (random movement with a net direction)."""
    rng = np.random.default_rng(seed)
    starts = [m.get_center().copy() for m in mobs]
    tg = [np.array(t if len(t) == 3 else (t[0], t[1], 0.0), float) for t in targets]
    ph = rng.uniform(0, 6.28, (len(mobs), 4))
    fr = rng.uniform(5, 11, (len(mobs), 2))

    def f(_m, a):
        p = a * a * (3 - 2 * a)
        env = np.sin(np.pi * a)
        for i, m in enumerate(mobs):
            w = np.array([np.cos(fr[i, 0] * a + ph[i, 0]) * amp * env, np.sin(fr[i, 1] * a + ph[i, 1]) * amp * env, 0])
            m.move_to(starts[i] + (tg[i] - starts[i]) * p + w)
    return UpdateFromAlphaFunc(VGroup(*mobs), f, run_time=rt, rate_func=linear)


def jiggle(mobs, rt, amp=0.08, seed=2, cycles=None):
    """Small random shaking in place; every dot is back where it started at the end."""
    rng = np.random.default_rng(seed)
    cycles = cycles or max(1.0, rt * 0.9)
    base = [m.get_center().copy() for m in mobs]
    ph = rng.uniform(0, 6.28, (len(mobs), 2))
    fr = rng.uniform(0.8, 1.6, (len(mobs), 2))

    def f(_m, a):
        env = min(1.0, a * 6, (1 - a) * 6)
        for i, m in enumerate(mobs):
            m.move_to(base[i] + amp * env * np.array([np.sin(2 * np.pi * cycles * fr[i, 0] * a + ph[i, 0]),
                                                      np.cos(2 * np.pi * cycles * fr[i, 1] * a + ph[i, 1]), 0]))
    return UpdateFromAlphaFunc(VGroup(*mobs), f, run_time=rt, rate_func=linear)


class SS(SpokenScene):
    def room(self, phrase, lead=0.2):
        return self.t_of(phrase) - lead - self.elapsed()

    def at_idle(self, phrase, mobs, amp=0.07, seed=0):
        """Keep the particles moving until the narrator reaches `phrase`, then sync to it."""
        rt = self.room(phrase)
        if rt > 0.5 and mobs:
            self.play(jiggle(list(mobs), rt, amp, seed=seed), run_time=rt)
        self.at(phrase)


def glass(cx, cy, w, h):
    water = Rectangle(width=w, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.16).move_to([cx, cy, 0])
    l, r, b = cx - w / 2, cx + w / 2, cy - h / 2
    outline = VMobject(color=GREY, stroke_width=6)
    outline.set_points_as_corners([P(l, cy + h / 2 + 0.25), P(l, b), P(r, b), P(r, cy + h / 2 + 0.25)])
    return VGroup(water, outline)


def tank(cx, cy, w, h):
    water = Rectangle(width=w, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.16).move_to([cx, cy, 0])
    outline = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=6, fill_opacity=0).move_to([cx, cy, 0])
    return water, outline


def memb(x, y0, y1):
    return DashedLine(P(x, y0), P(x, y1), dash_length=0.22, dashed_ratio=0.62, color=GREY, stroke_width=8)


class S00Title(TitleCard):
    LESSON = "Diffusion and osmosis"
    TITLE = "Water moves toward more dissolved salt"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SS):
    """cucumber slice + salt -> beads of water; limp lettuce in water -> crisp; the question."""

    def construct(self):
        lx, rx = -3.5, 3.2
        slab = RoundedRectangle(corner_radius=0.14, width=5.0, height=1.3, stroke_color=GREEN, stroke_width=6,
                                fill_color=GREEN, fill_opacity=0.22).move_to(P(lx, -1.0))
        slab_l = T("cucumber slices", 32, GREEN).move_to(P(lx, -2.1))
        salt_l = T("salt", 32, ORANGE).move_to(P(lx, 2.5))
        salt = dots([(lx - 2.0 + 0.5 * i, 1.7 + 0.3 * (i % 3)) for i in range(9)], ORANGE, 0.11)
        self.at("Sprinkle salt")
        self.play(FadeIn(slab), FadeIn(slab_l), FadeIn(salt), FadeIn(salt_l), run_time=0.6)
        self.play(*[d.animate.move_to(P(d.get_x(), -0.3)) for d in salt], run_time=1.0, rate_func=rush_into)

        beads = dots([(lx - 1.9 + 0.95 * i, 0.0) for i in range(5)], BLUE, 0.22)
        beads_l = T("drops of water", 32, BLUE).move_to(P(lx, 0.95))
        self.at_idle("drops of water", list(salt), 0.04, 1)
        self.play(FadeOut(salt_l), LaggedStart(*[GrowFromCenter(b) for b in beads], lag_ratio=0.25), FadeIn(beads_l), run_time=1.4)

        bowl = VMobject(color=GREY, stroke_width=7)
        bowl.set_points_as_corners([P(rx - 2.6, -0.2), P(rx - 1.9, -2.4), P(rx + 1.9, -2.4), P(rx + 2.6, -0.2)])
        water = Polygon(P(rx - 2.48, -0.6), P(rx - 1.9, -2.38), P(rx + 1.9, -2.38), P(rx + 2.48, -0.6),
                        stroke_width=0, fill_color=BLUE, fill_opacity=0.28)
        limp_pts = [P(rx, -2.2), P(rx, -0.5), P(rx - 0.2, 0.5), P(rx - 0.9, 0.95), P(rx - 1.7, 0.8)]
        crisp_pts = [P(rx, -2.2), P(rx, -0.5), P(rx, 0.6), P(rx, 1.3), P(rx, 1.95)]
        leaf = VMobject(color=GREEN, stroke_width=16).set_points_smoothly(limp_pts)
        leaf_l = T("limp lettuce", 32, GREEN).move_to(P(rx + 1.6, 1.5))
        bowl_l = T("plain cold water", 32, BLUE).move_to(P(rx, -2.95))
        self.at_idle("limp lettuce", list(salt) + list(beads), 0.04, 2)
        self.play(FadeIn(bowl), FadeIn(water), Create(leaf), FadeIn(leaf_l), FadeIn(bowl_l), run_time=1.0)
        leaf_new = VMobject(color=GREEN, stroke_width=16).set_points_smoothly(crisp_pts)
        crisp_l = T("crisp lettuce", 32, GREEN).move_to(P(rx + 1.75, 1.5))
        self.at_idle("turn crisp", list(salt) + list(beads), 0.04, 3)
        self.play(Transform(leaf, leaf_new), ReplacementTransform(leaf_l, crisp_l), run_time=1.6)

        q1 = T("Nobody pushes the water.", 36).move_to(P(0, 3.2))
        self.at("Nobody pushes the water")
        self.play(FadeIn(q1), run_time=0.5)
        q2 = T("The cells do not pump it.", 36).move_to(P(0, 3.2))
        self.at_idle("the cells do not pump", list(salt) + list(beads), 0.04, 4)
        self.play(ReplacementTransform(q1, q2), run_time=0.4)
        q3 = T("How does water move? Which way?", 40, YELLOW, weight=BOLD).move_to(P(0, 3.2))
        m1 = T("?", 80, YELLOW, weight=BOLD).move_to(P(lx, 2.2))
        m2 = T("?", 80, YELLOW, weight=BOLD).move_to(P(rx + 0.9, 2.3))
        self.at_idle("how does it move", list(salt) + list(beads), 0.04, 5)
        self.play(ReplacementTransform(q2, q3), FadeIn(m1), FadeIn(m2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
GL = dict(cx=0.0, cy=-0.45, w=11.6, h=4.9)
GX0, GX1 = GL["cx"] - GL["w"] / 2 + 0.4, GL["cx"] + GL["w"] / 2 - 0.4
GY0, GY1 = GL["cy"] - GL["h"] / 2 + 0.35, GL["cy"] + GL["h"] / 2 - 0.3


def even_targets(seed=11):
    return grid_pts(np.random.default_rng(seed), GX0, GX1, GY0, GY1, 9, 5, jit=0.3)


class S02Spread(SS):
    """a drop of dye lands, forms a crowded spot, then spreads."""

    def construct(self):
        g = glass(**GL)
        g_l = T("a glass of still water", 28, GREY).move_to(P(0, GL["cy"] - GL["h"] / 2 - 0.45))
        self.at("Drop food")
        self.play(FadeIn(g), FadeIn(g_l), run_time=0.7)
        cx, cy = -4.3, 1.0
        drop = Dot(P(cx, 3.1), radius=0.24, color=YELLOW)
        rng = np.random.default_rng(5)
        pts = []
        while len(pts) < 45:
            p = rng.uniform(-1, 1, 2)
            if np.hypot(*p) < 1:
                pts.append((cx + p[0] * 0.8, cy + p[1] * 0.65))
        cluster = dots(pts, YELLOW, 0.09)
        self.play(FadeIn(drop), run_time=0.2)
        self.play(drop.animate.move_to(P(cx, cy)), run_time=0.7, rate_func=rush_into)
        self.play(ReplacementTransform(drop, cluster), run_time=0.5)
        cl = list(cluster)

        spot = T("one spot", 30, YELLOW).move_to(P(cx, 2.55))
        self.at_idle("one spot", cl, 0.05)
        self.play(FadeIn(spot), run_time=0.4)

        conc = vocab("concentration", 36).move_to(P(0, 3.25))
        self.at_idle("Concentration is", cl, 0.05, 1)
        self.play(FadeIn(conc, shift=DOWN * 0.15), FadeOut(spot), run_time=0.5)
        note = T("how much of a substance is in a given space", 30, TEXT).move_to(P(0, 2.55))
        self.at_idle("how much of a substance", cl, 0.05, 2)
        self.play(FadeIn(note), run_time=0.6)

        high = T("high concentration", 28, YELLOW).move_to(P(cx + 0.6, cy - 1.25))
        box_h = DashedVMobject(Rectangle(width=2.4, height=1.9, stroke_color=YELLOW, stroke_width=3).move_to(P(cx, cy)), num_dashes=40)
        self.at_idle("Where the drop landed", cl, 0.05, 3)
        self.play(Create(box_h), FadeIn(high), run_time=0.7)
        low = T("low concentration", 28, YELLOW).move_to(P(4.0, cy - 1.25))
        box_l = DashedVMobject(Rectangle(width=2.4, height=1.9, stroke_color=YELLOW, stroke_width=3).move_to(P(4.0, cy)), num_dashes=40)
        self.at_idle("Far away", cl, 0.06, 4)
        self.play(Create(box_l), FadeIn(low), run_time=0.7)

        self.at_idle("always moving", cl, 0.06, 5)
        rt = max(1.0, self.room("More leave the crowded spot") - 0.2)
        self.play(jiggle(cl, rt, amp=0.12, seed=6), run_time=rt)
        self.at("More leave the crowded spot")
        self.play(FadeOut(box_h), FadeOut(box_l), FadeOut(high), FadeOut(low), FadeOut(note), run_time=0.4)
        rt = max(3.0, self.narration_s - self.elapsed() - 0.5)
        self.play(drift(cl, even_targets(), rt, amp=0.3, seed=3), run_time=rt)
        self.finish()


class S03Diffusion(SS):
    """same glass: crowded left to spread; once even, the dots still move, two equal arrows."""

    def construct(self):
        g = glass(**GL)
        rng = np.random.default_rng(7)
        left_pts = grid_pts(rng, GX0, -1.4, GY0, GY1, 8, 5, jit=0.3)
        right_pts = grid_pts(rng, 4.2, GX1, GY0, GY1, 1, 5, jit=0.3)
        ds = dots(left_pts + right_pts, YELLOW, 0.09)
        dl = list(ds)
        self.play(FadeIn(g), FadeIn(ds), run_time=0.6)
        term = vocab("diffusion", 38).move_to(P(0, 3.3))
        self.at("is the movement")
        self.play(FadeIn(term, shift=DOWN * 0.15), run_time=0.5)
        more = T("more concentrated", 30, YELLOW).move_to(P(-3.6, 2.6))
        self.at_idle("more concentrated", dl, 0.05)
        self.play(FadeIn(more), run_time=0.5)
        less = T("less concentrated", 30, YELLOW).move_to(P(3.9, 2.6))
        flow = arr(P(-1.5, 2.55), P(1.5, 2.55), YELLOW)
        self.at_idle("less concentrated", dl, 0.05, 1)
        self.play(GrowArrow(flow), FadeIn(less), run_time=0.6)
        rt = max(1.0, self.room("the dye is even") - 0.1)
        self.play(drift(dl, even_targets(21), rt, amp=0.25, seed=4), run_time=rt)

        self.at("the dye is even")
        self.play(FadeOut(more), FadeOut(less), FadeOut(flow), FadeOut(term), run_time=0.5)
        rt = max(1.0, self.room("Just as many move"))
        self.play(jiggle(dl, rt, amp=0.14, seed=5), run_time=rt)
        a1 = arr(P(-0.3, 2.65), P(-2.4, 2.65), YELLOW)
        a2 = arr(P(0.3, 2.65), P(2.4, 2.65), YELLOW)
        eq = T("same number each way", 32, TEXT).move_to(P(0, 3.3))
        self.at("Just as many move")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(eq), run_time=0.7)
        rt = max(1.0, self.room("stops changing"))
        self.play(jiggle(dl, rt, amp=0.14, seed=9), run_time=rt)
        stop = T("the colour stops changing", 34, TEXT).move_to(P(0, 3.3))
        self.at("stops changing")
        self.play(ReplacementTransform(eq, stop), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
TOP, BOT = 1.5, -2.0


class S04Membrane(SS):
    """dashed model membrane between blood and cell: water and oxygen cross, salt is held back, oxygen goes down its difference."""

    def construct(self):
        rng = np.random.default_rng(31)
        wl = dots(grid_pts(rng, -5.6, -0.5, BOT + 0.3, TOP - 0.3, 4, 3), BLUE, 0.1)
        wr = dots(grid_pts(rng, 0.5, 5.6, BOT + 0.3, TOP - 0.3, 4, 3), BLUE, 0.1)
        sl = dots([(-4.9, -1.5), (-2.9, 0.6), (-1.3, -0.4), (-3.6, 1.2)], ORANGE, 0.13)
        sr = dots([(1.3, 1.1), (3.0, -1.5), (4.8, 0.3), (2.2, 0.0)], ORANGE, 0.13)
        ol = dots(grid_pts(np.random.default_rng(2), -5.6, -0.6, BOT + 0.4, TOP - 0.4, 4, 3, 0.4), YELLOW, 0.11)
        orr = dots([(2.0, -1.0), (4.3, 1.0)], YELLOW, 0.11)
        allp = list(wl) + list(wr) + list(sl) + list(sr) + list(ol) + list(orr)
        m = memb(0, BOT - 0.25, TOP + 0.3)
        outl = Rectangle(width=12.0, height=TOP - BOT + 0.6, stroke_color=GREY, stroke_width=3, stroke_opacity=0.5).move_to(P(0, (TOP + BOT) / 2))
        blood = T("blood", 30, GREY).move_to(P(-3.0, 2.25))
        incell = T("inside a cell", 30, GREY).move_to(P(3.0, 2.25))
        mem_chip = vocab("cell membrane", 34).move_to(P(0, 3.15))
        self.at("The cell membrane")
        self.play(FadeIn(outl), Create(m), FadeIn(mem_chip), FadeIn(blood), FadeIn(incell), FadeIn(wl), FadeIn(wr),
                  FadeIn(sl), FadeIn(sr), FadeIn(ol), FadeIn(orr), run_time=1.2)
        thin = T("the thin layer around every cell", 28, TEXT).move_to(P(0, -3.0))
        self.at_idle("thin layer", allp, 0.07)
        self.play(FadeIn(thin), run_time=0.5)

        sp = vocab("selectively permeable", 32).move_to(P(0, 3.15))
        self.at_idle("selectively permeable", allp, 0.07, 1)
        self.play(ReplacementTransform(mem_chip, sp), FadeOut(thin), run_time=0.6)

        # water crosses both ways
        w_a, w_b = list(wl)[5], list(wl)[9]
        w_c = list(wr)[2]
        self.at_idle("lets some things through", allp, 0.07, 2)
        self.play(w_a.animate.move_to(P(1.5, w_a.get_y())), w_b.animate.move_to(P(2.2, w_b.get_y() - 0.2)),
                  w_c.animate.move_to(P(-1.5, w_c.get_y())), run_time=1.6)
        # salt held back
        s1, s2 = list(sl)[2], list(sr)[3]
        x1, x2 = s1.get_x(), s2.get_x()
        self.at_idle("holds back others", allp, 0.07, 3)
        self.play(s1.animate.move_to(P(-0.35, s1.get_y())), s2.animate.move_to(P(0.35, s2.get_y())), run_time=0.7)
        self.play(s1.animate.move_to(P(x1 - 0.5, s1.get_y() + 0.3)), s2.animate.move_to(P(x2 + 0.5, s2.get_y() - 0.3)), run_time=0.6)

        # who crosses
        easy = VGroup(T("crosses easily: ", 28, GREY), T("water", 28, BLUE), T(", ", 28, GREY), T("oxygen", 28, YELLOW), T(", ", 28, GREY),
                      T("carbon dioxide", 28, YELLOW)).arrange(RIGHT, buff=0.1, aligned_edge=DOWN).move_to(P(0, -2.95))
        self.at_idle("Water, oxygen and carbon dioxide", allp, 0.07, 4)
        self.play(FadeIn(easy), run_time=0.7)
        hard = VGroup(T("crosses much less easily: ", 28, GREY), T("salt", 28, ORANGE), T(", ", 28, GREY), T("sugar", 28, ORANGE)).arrange(RIGHT, buff=0.1, aligned_edge=DOWN).move_to(P(0, -3.45))
        self.at_idle("Many dissolved particles", allp, 0.07, 5)
        self.play(FadeIn(hard), run_time=0.7)

        # oxygen: down its difference
        dim_all = [wl, wr, sl, sr]
        more_o = T("more oxygen", 30, YELLOW).move_to(P(-3.0, 2.25))
        less_o = T("less oxygen", 30, YELLOW).move_to(P(3.0, 2.25))
        self.at_idle("Oxygen is more", allp, 0.07, 6)
        self.play(*[g.animate.set_opacity(0.2) for g in dim_all], FadeOut(easy), FadeOut(hard), FadeOut(blood), FadeOut(incell),
                  FadeOut(sp), FadeIn(more_o), FadeIn(less_o), run_time=0.7)
        mv = list(ol)[:5]
        tg = [P(1.2 + 0.9 * i, mv[i].get_y()) for i in range(5)]
        arrow = arr(P(-1.4, 2.7), P(1.4, 2.7), YELLOW)
        rest = [d for d in list(ol)[5:]] + list(orr)
        self.at_idle("inside a cell", rest, 0.07, 7)
        self.play(GrowArrow(arrow), drift(mv, tg, 3.0, amp=0.15, seed=6), run_time=3.0)
        self.finish()


class S05Osmosis(SS):
    """plain water | salty water. Net water crossing to the salty side; level rises."""

    def construct(self):
        w, h = 11.4, 4.2
        cy = -0.55
        hs = h - 0.6
        wat_l = Rectangle(width=w / 2, height=hs, stroke_width=0, fill_color=BLUE, fill_opacity=0.16)
        wat_l.move_to(P(-w / 4, cy - 0.3))
        wat_r = wat_l.copy().move_to(P(w / 4, cy - 0.3))
        out = Rectangle(width=w, height=h + 0.3, stroke_color=GREY, stroke_width=6).move_to(P(0, cy))
        m = memb(0, cy - h / 2 - 0.15, cy + h / 2 + 0.15)
        rng = np.random.default_rng(41)
        L_pts = grid_pts(rng, -5.4, -0.5, cy - 1.7, cy + 0.6, 5, 4)
        R_pts = grid_pts(rng, 0.5, 5.4, cy - 1.7, cy + 0.6, 5, 4)
        keep = [p for i, p in enumerate(R_pts) if i % 5 not in (1, 3)]
        wl = dots(L_pts, BLUE, 0.11)
        wr = dots(keep, BLUE, 0.11)
        salt = dots([(1.2, cy - 1.3), (2.0, cy + 0.3), (3.1, cy - 0.7), (4.2, cy + 0.4), (5.0, cy - 1.3), (2.5, cy - 1.6),
                     (3.8, cy - 0.1), (1.8, cy - 0.5)], ORANGE, 0.15)
        tl = T("plain water", 32, BLUE).move_to(P(-2.85, cy + h / 2 + 0.55))
        tr = T("salty water", 32, ORANGE).move_to(P(2.85, cy + h / 2 + 0.55))
        osm = vocab("osmosis", 42).move_to(P(0, 3.25))
        mdl = T("model, not to scale", 24, GREY).move_to(P(4.7, 3.3))
        self.add(mdl)
        self.at("is the movement")
        self.play(FadeIn(out), FadeIn(wat_l), FadeIn(wat_r), Create(m), FadeIn(wl), FadeIn(wr), FadeIn(osm, shift=DOWN * 0.15), run_time=1.0)
        wl_l, wr_l = list(wl), list(wr)
        allw = wl_l + wr_l
        self.at_idle("of water across", allw, 0.07)
        self.play(wl_l[7].animate.move_to(P(1.2, wl_l[7].get_y())), wr_l[3].animate.move_to(P(-1.2, wr_l[3].get_y())), run_time=1.2)

        self.at_idle("Dissolve salt in water", allw, 0.07, 1)
        self.play(FadeIn(tl), FadeIn(tr), LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in salt], lag_ratio=0.12), run_time=1.6)
        lessc = T("water: less concentrated", 28, BLUE).move_to(P(2.85, cy - h / 2 - 0.5))
        morec = T("water: more concentrated", 28, BLUE).move_to(P(-2.85, cy - h / 2 - 0.5))
        allp = allw + list(salt)
        self.at_idle("less concentrated", allp, 0.07, 2)
        self.play(FadeIn(lessc), FadeIn(morec), run_time=0.6)

        flow = arr(P(-1.6, 2.7), P(1.6, 2.7), BLUE, 9)
        flow_l = T("toward more dissolved salt", 30, BLUE).move_to(P(0, 3.25))
        movers = [wl_l[2], wl_l[6]]
        tg = [P(1.3 + 1.0 * i, movers[i].get_y() + (0.2 if i % 2 else -0.2)) for i in range(2)]
        self.at_idle("Water moves toward the side", allp, 0.07, 3)
        self.play(FadeOut(osm), run_time=0.3)
        self.play(GrowArrow(flow), FadeIn(flow_l), drift(movers, tg, 2.8, amp=0.12, seed=8), run_time=2.8)

        sdot = list(salt)[5]
        s_y = sdot.get_y()
        movers2 = [wl_l[3]]
        rest = [d for d in allp if d is not sdot and d not in movers and d not in movers2]
        self.at_idle("cannot follow", rest, 0.07, 4)
        self.play(sdot.animate.move_to(P(0.3, s_y)), run_time=0.7)
        self.play(sdot.animate.move_to(P(1.1, s_y + 0.2)), run_time=0.5)
        self.at_idle("keeps moving that way", rest, 0.07, 5)
        tg2 = [P(3.6, movers2[0].get_y())]
        new_r = Rectangle(width=w / 2, height=hs + 0.4, stroke_width=0, fill_color=BLUE, fill_opacity=0.16)
        new_r.move_to(wat_r.get_bottom() + UP * (hs + 0.4) / 2)
        new_l = Rectangle(width=w / 2, height=hs - 0.4, stroke_width=0, fill_color=BLUE, fill_opacity=0.16)
        new_l.move_to(wat_l.get_bottom() + UP * (hs - 0.4) / 2)
        self.play(drift(movers2, tg2, 2.0, amp=0.12, seed=9), Transform(wat_r, new_r), Transform(wat_l, new_l), run_time=2.0)

        note = T("our model membrane: holds back all the salt", 28, ORANGE).move_to(P(0, -3.2))
        self.at_idle("Our model membrane holds back", allp, 0.07, 6)
        self.play(FadeIn(note), FadeOut(morec), FadeOut(lessc), run_time=0.6)
        real = T("real membranes: some salt crosses, much more slowly", 28, GREY).move_to(P(0, -3.2))
        self.at_idle("Real ones let some through", allp, 0.07, 7)
        self.play(ReplacementTransform(note, real), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SS):
    """two cells: cucumber cell loses water to the salty outside, lettuce cell gains water from plain water."""

    def construct(self):
        cyp = 0.0
        pl = Rectangle(width=5.9, height=4.5, stroke_color=GREY, stroke_width=3, fill_color=BLUE, fill_opacity=0.1).move_to(P(-3.3, cyp))
        pr = Rectangle(width=5.9, height=4.5, stroke_color=GREY, stroke_width=3, fill_color=BLUE, fill_opacity=0.1).move_to(P(3.3, cyp))
        cl = RoundedRectangle(corner_radius=0.3, width=3.4, height=2.2, stroke_color=GREEN, stroke_width=7, fill_color=GREEN, fill_opacity=0.1).move_to(P(-3.3, cyp))
        cr = cl.copy().move_to(P(3.3, cyp))
        t_l = T("cucumber cell", 30, GREEN).move_to(P(-3.3, cyp + 2.78))
        t_r = T("lettuce cell", 30, GREEN).move_to(P(3.3, cyp + 2.78))
        ol = T("salty water outside", 28, ORANGE).move_to(P(-3.3, cyp - 2.7))
        orr = T("plain water outside", 28, BLUE).move_to(P(3.3, cyp - 2.7))
        in_l = dots([(-4.2, cyp + 0.4), (-3.4, cyp - 0.4), (-2.5, cyp + 0.3), (-3.3, cyp + 0.0), (-4.1, cyp - 0.4), (-2.6, cyp - 0.5)], BLUE, 0.11)
        out_salt_l = dots([(-5.6, cyp + 1.5), (-1.1, cyp + 1.5), (-5.6, cyp - 1.5), (-1.1, cyp - 1.5), (-3.3, cyp + 1.65), (-3.3, cyp - 1.6),
                           (-5.7, cyp + 0.2), (-0.9, cyp + 0.1)], ORANGE, 0.14)
        out_w_l = dots([(-5.3, cyp + 0.9), (-1.5, cyp - 0.8), (-5.2, cyp - 0.8)], BLUE, 0.11)
        in_r = dots([(2.6, cyp + 0.4), (3.3, cyp - 0.4), (4.1, cyp + 0.3)], BLUE, 0.11)
        in_salt_r = dots([(2.9, cyp + 0.0), (3.6, cyp + 0.4), (3.3, cyp - 0.7), (4.2, cyp - 0.4), (2.5, cyp - 0.5), (3.8, cyp - 0.05)], ORANGE, 0.14)
        out_w_r = dots([(1.2, cyp + 1.5), (5.4, cyp + 1.5), (1.2, cyp - 1.5), (5.4, cyp - 1.5), (3.3, cyp + 1.65), (3.3, cyp - 1.6),
                        (1.3, cyp + 0.3), (5.4, cyp + 0.2), (2.2, cyp + 1.6), (4.4, cyp - 1.6)], BLUE, 0.11)
        in_salt_l = dots([(-3.9, cyp + 0.0), (-2.7, cyp - 0.1), (-3.3, cyp + 0.6)], ORANGE, 0.14)
        idle1 = list(in_salt_l) + list(in_salt_r) + list(out_w_l) + list(out_w_r) + list(in_r)

        self.at("cucumber makes sense")
        self.play(FadeIn(pl), FadeIn(pr), FadeIn(cl), FadeIn(cr), FadeIn(t_l), FadeIn(t_r), FadeIn(in_l), FadeIn(in_r), FadeIn(in_salt_r), FadeIn(in_salt_l),
                  FadeIn(out_w_l), FadeIn(out_w_r), run_time=1.0)
        self.at("Salt outside")
        self.play(FadeIn(out_salt_l), FadeIn(ol), run_time=0.8)
        lessw = T("water outside: less concentrated", 26, BLUE).move_to(P(-3.3, cyp - 3.2))
        self.at_idle("less concentrated", idle1 + list(in_l), 0.06)
        self.play(FadeIn(lessw), run_time=0.5)
        mv = [in_l[0], in_l[2], in_l[4], in_l[5]]
        tgt = [P(-5.1, cyp + 0.35), P(-1.9, cyp + 1.0), P(-5.2, cyp - 1.0), P(-2.0, cyp - 1.15)]
        a_out = arr(P(-4.6, cyp + 1.85), P(-5.6, cyp + 1.85), BLUE, 7)
        a_out2 = arr(P(-2.0, cyp + 1.85), P(-1.0, cyp + 1.85), BLUE, 7)
        self.at_idle("so water leaves", idle1 + list(in_l), 0.06, 1)
        self.play(FadeIn(a_out), FadeIn(a_out2), drift(mv, tgt, 2.6, amp=0.1, seed=12), run_time=2.6)

        morep = T("more dissolved particles inside", 26, ORANGE).move_to(P(3.3, cyp - 3.2))
        rest = idle1 + [in_l[1], in_l[3]]
        self.at_idle("In lettuce", rest, 0.06, 2)
        self.play(FadeIn(orr), FadeIn(morep), FadeOut(lessw), run_time=0.7)
        mv2 = [out_w_r[0], out_w_r[3], out_w_r[6], out_w_r[7]]
        tgt2 = [P(2.9, cyp + 0.8), P(4.0, cyp - 0.85), P(2.6, cyp - 0.2), P(4.2, cyp + 0.2)]
        a_in = arr(P(1.6, cyp + 1.85), P(2.6, cyp + 1.85), BLUE, 7)
        a_in2 = arr(P(5.0, cyp + 1.85), P(4.0, cyp + 1.85), BLUE, 7)
        rest2 = [d for d in idle1 if d not in mv2] + [in_l[1], in_l[3]]
        self.at_idle("so water moves in", rest2, 0.06, 3)
        self.play(FadeIn(a_in), FadeIn(a_in2), drift(mv2, tgt2, 2.6, amp=0.1, seed=13), run_time=2.6)

        noe = T("the cells spend no energy", 32, TEXT).move_to(P(0, 3.25))
        self.at_idle("Neither time", rest2 + mv2, 0.06, 4)
        self.play(FadeOut(t_l), FadeOut(t_r), FadeOut(morep), FadeIn(noe), run_time=0.6)
        pas = vocab("passive transport", 36).move_to(P(0, 3.25))
        self.at_idle("passive transport", rest2 + mv2, 0.06, 5)
        self.play(ReplacementTransform(noe, pas), run_time=0.6)
        self.at_idle("toward more dissolved particles", rest2 + mv2 + list(out_salt_l), 0.06, 6)
        self.play(Indicate(out_salt_l, color=ORANGE, scale_factor=1.15), Indicate(in_salt_r, color=ORANGE, scale_factor=1.25), run_time=1.5)
        self.finish()


class S07End(EndCard):
    LINE = "Water moves toward more dissolved particles, and the cell spends no energy."
