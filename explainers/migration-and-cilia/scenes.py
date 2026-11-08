"""Sliding becomes bending  (Biochemistrypedia explainer, Cell Biology: migration and cilia)

COLOR MAP (one color per concept, whole video)
  BLUE   = A-tubule / the outer doublets (the thing that is pushed and bent)
  PURPLE = B-tubule
  TEAL   = mucus (opening scene only)
  GREY   = membranes, the central pair, basal body, anchor, labels
  YELLOW = dynein arms and their push
  ORANGE = the links between doublets (they resist sliding)
  GOLD   = ATP
  RED    = failure: missing arms, no movement, trypsin cut
  GREEN  = it works: the motors slide
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
D = 0.7          # distance between the two strips (centre to centre)
STRIP_W = 20


# ----------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.45, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=8),
                  Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=8))


def _P(s, k, off):
    """point at arc length s along a centre line of curvature k, offset along the inward normal."""
    if abs(k) < 1e-5:
        return np.array([s, off, 0.0])
    c = np.array([np.sin(k * s) / k, (1 - np.cos(k * s)) / k, 0.0])
    n = np.array([-np.sin(k * s), np.cos(k * s), 0.0])
    return c + off * n


def pair(origin, k=0.0, slide=0.0, L=10.0, ties=(1.8, 4.0, 6.2, 8.4), tie_op=1.0, tie_col=ORANGE,
         top=BLUE, bot=BLUE, anchor=True):
    """two strips (doublets / card), glued at the base (left) and tied along their length.
    top strip = inner side of the bend, so pushing it toward the tip curves the pair upward."""
    o = np.array(origin, float)
    ft, fb = 1 - k * D / 2, 1 + k * D / 2
    g = VGroup()
    b = ParametricFunction(lambda u: o + _P(u / fb, k, -D / 2), t_range=[0, L, 0.05], color=bot, stroke_width=STRIP_W)
    t = ParametricFunction(lambda u: o + _P(u / ft, k, D / 2), t_range=[slide, L + slide, 0.05], color=top,
                           stroke_width=STRIP_W)
    g.add(b, t)
    if tie_op > 0.01:
        for u in ties:
            g.add(Line(o + _P(u / ft, k, D / 2), o + _P(u / fb, k, -D / 2), color=tie_col, stroke_width=5)
                  .set_stroke(opacity=tie_op))
    if anchor:
        g.add(RoundedRectangle(corner_radius=0.06, width=0.3, height=D + 0.5, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.55).move_to(o + [-0.15, 0, 0]))
    return g


def doublet(ra=0.38, a_col=BLUE, b_col=PURPLE, rot=0.0, w=3.0):
    """cross-section of one outer doublet: complete A circle plus an incomplete B arc fused to it.
    rot = direction (radians) in which the B arc sits, from the A centre."""
    rb = ra * 0.8
    dist = ra + rb * 0.45
    cb = np.array([np.cos(rot), np.sin(rot), 0]) * dist
    away = np.degrees(rot)
    B = Arc(radius=rb, start_angle=np.radians(away - 115), angle=np.radians(230), stroke_color=b_col,
            stroke_width=w).move_arc_center_to(cb)
    back = Circle(radius=ra, stroke_width=0, fill_color=BG, fill_opacity=1)
    A = Circle(radius=ra, stroke_color=a_col, stroke_width=w, fill_color=a_col, fill_opacity=0.3)
    return VGroup(B, back.move_to(A), A)


def dim_d(d, o=0.25):
    """dim a doublet without filling its open B arc."""
    return [d[0].animate.set_stroke(opacity=o), d[2].animate.set_stroke(opacity=o).set_fill(opacity=0.3 * o)]


def label(text, color=GREY, size=26, **kw):
    return T(text, size, color, **kw)


# ----------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Cell shape, migration and cilia"
    TITLE = "Sliding becomes bending"


# ----------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """sperm and airway cilia both fail; a question box asks what they share; it is a machine without dynein arms."""

    def construct(self):
        # sperm (left)
        head = Ellipse(width=0.95, height=0.62, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3)
        head.move_to([-5.6, 0.7, 0])
        tail = ParametricFunction(lambda t: np.array([-5.1 + t, 0.7 + 0.28 * np.sin(2.4 * t), 0]),
                                  t_range=[0, 2.3, 0.05], color=GREY, stroke_width=5)
        sperm = VGroup(head, tail)
        sperm_lbl = label("sperm tail", GREY, 28).move_to([-4.3, -0.55, 0])
        sperm_x = cross([-4.3, 0.7, 0], 0.55)
        no_swim = label("does not swim", RED, 26).move_to([-4.3, -1.15, 0])

        # airway cilia (right)
        bar = RoundedRectangle(corner_radius=0.08, width=3.3, height=0.3, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([4.6, -0.2, 0])
        cil = VGroup(*[Line([3.15 + 0.6 * i, -0.05, 0], [3.15 + 0.6 * i, 0.8, 0], color=GREY, stroke_width=5)
                       for i in range(6)])
        mucus = Ellipse(width=3.2, height=0.6, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                        fill_opacity=0.3).move_to([4.6, 1.15, 0])
        mu_l = label("mucus", TEAL, 24).move_to(mucus)
        airway = VGroup(bar, cil, mucus, mu_l)
        air_lbl = label("airway cilia", GREY, 28).move_to([4.6, -0.85, 0])
        air_x = cross([4.6, 0.35, 0], 0.4)
        no_clear = label("mucus is not cleared", RED, 26).move_to([4.6, -1.45, 0])

        self.at("Four men")
        self.play(FadeIn(sperm, shift=DOWN * 0.1), FadeIn(sperm_lbl), run_time=0.6)
        self.at("could not swim")
        self.play(Create(sperm_x), FadeIn(no_swim), run_time=0.6)
        self.at("Three of them")
        self.play(FadeIn(airway, shift=DOWN * 0.1), FadeIn(air_lbl), run_time=0.6)
        self.at("clear mucus")
        self.play(Create(air_x), FadeIn(no_clear), run_time=0.6)

        box = RoundedRectangle(corner_radius=0.2, width=2.4, height=2.0, stroke_color=GREY, stroke_width=3.5)
        box.move_to([0, 0.4, 0])
        q = T("?", 72, GREY).move_to(box)
        a1 = arr([-2.6, 0.45, 0], [-1.3, 0.45, 0], GREY)
        a2 = arr([2.7, 0.45, 0], [1.3, 0.45, 0], GREY)
        self.at("lacked small projections")
        self.play(Create(box), FadeIn(q), GrowArrow(a1), GrowArrow(a2), run_time=0.7)

        arms_box = RoundedRectangle(corner_radius=0.2, width=2.4, height=2.0, stroke_color=RED, stroke_width=3.5,
                                    fill_color=RED, fill_opacity=0.12).move_to(box)
        arms_t = T("no dynein\narms", 28, RED, line_spacing=0.8).move_to(box)
        self.at("dynein arms")
        self.play(ReplacementTransform(box, arms_box), ReplacementTransform(q, arms_t),
                  a1.animate.set_color(RED), a2.animate.set_color(RED), run_time=0.7)

        one = T("one missing part", 34, RED, weight=BOLD).move_to([0, -2.5, 0])
        two = T("two failures, two organs", 30, TEXT).move_to([0, -3.15, 0])
        self.at("One missing part")
        self.play(FadeIn(one, shift=UP * 0.1), run_time=0.5)
        self.at("two failures")
        self.play(FadeIn(two, shift=UP * 0.1), run_time=0.5)

        mach = T("shared\nmachine", 30, TEXT, line_spacing=0.8).move_to(box)
        self.at("share a machine")
        self.play(FadeOut(arms_t), FadeIn(mach),
                  arms_box.animate.set_stroke(TEXT).set_fill(TEXT, 0.08),
                  a1.animate.set_color(TEXT), a2.animate.set_color(TEXT), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Axoneme(SpokenScene):
    """cross-section: nine doublets, central pair, zoom to A and B tubules, then side view with basal body."""

    def construct(self):
        cx, cy, R = -3.2, 0.1, 2.5
        ring = Circle(radius=R + 0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06)
        ring.move_to([cx, cy, 0])
        ring_lbl = label("axoneme", GREY, 32).move_to([3.7, 2.7, 0])

        self.play(Create(ring), run_time=1.5)
        self.at("same axoneme")
        self.play(FadeIn(ring_lbl), run_time=0.5)
        ring_lbl2 = label("a cylinder of microtubules,\nseen end on", GREY, 28, line_spacing=0.8).move_to([3.7, 2.4, 0])
        self.at("cylinder of microtubules")
        self.play(ReplacementTransform(ring_lbl, ring_lbl2), ring.animate.set_stroke(TEXT), run_time=0.6)

        dbl = []
        for k in range(9):
            a = np.radians(90 + 40 * k)
            ctr = np.array([cx + R * np.cos(a), cy + R * np.sin(a), 0])
            rot = np.arctan2(-np.cos(a), np.sin(a))          # B arc on the clockwise side
            d = doublet(0.4, rot=rot, w=3)
            d.shift(ctr - d[2].get_center())
            dbl.append(d)
        self.at("outer doublets")
        self.play(FadeOut(ring_lbl2), LaggedStart(*[FadeIn(d, scale=0.6) for d in dbl], lag_ratio=0.08), run_time=1.1)
        lab9 = chip("9 outer doublets", BLUE, 28).move_to([3.9, 2.4, 0])
        near = dbl[7][2].get_center()
        lead9 = Line(lab9.get_left() + [-0.05, -0.15, 0], near + [0.5, 0.15, 0], color=BLUE, stroke_width=3)
        self.play(FadeIn(lab9), Create(lead9), run_time=0.3)

        cp = VGroup(*[Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4)
                      .move_to([cx + dx, cy, 0]) for dx in (-0.32, 0.32)])
        labcp = chip("central pair", GREY, 28).move_to([3.9, 0.9, 0])
        leadcp = Line(labcp.get_left() + [-0.05, -0.1, 0], [cx + 0.7, cy - 0.1, 0], color=GREY, stroke_width=3)
        self.at("central pair")
        self.play(FadeIn(cp, scale=0.5), FadeIn(labcp), Create(leadcp), run_time=0.6)
        nine2 = M("9 + 2", 40, TEXT).move_to([3.9, -0.5, 0])
        self.play(FadeIn(nine2, shift=UP * 0.1), run_time=0.3)

        # zoom on one doublet: complete A, incomplete B
        z = doublet(0.95, rot=0.0, w=4)
        z.shift(np.array([3.5, 0.9, 0]) - z[2].get_center())
        za = T("A-tubule: complete", 28, BLUE).move_to([3.9, -0.9, 0])
        zb = T("B-tubule: incomplete", 28, PURPLE).move_to([3.9, -1.6, 0])
        self.at("Each doublet")
        self.play(FadeOut(VGroup(lab9, lead9, labcp, leadcp, nine2)),
                  *[a for d in dbl for a in dim_d(d)], cp.animate.set_opacity(0.25),
                  ring.animate.set_stroke(opacity=0.4).set_fill(opacity=0.03), run_time=0.4)
        self.play(FadeIn(z, scale=0.5), FadeIn(za, shift=UP * 0.1), run_time=0.5)
        self.at("incomplete")
        self.play(FadeIn(zb, shift=UP * 0.1), run_time=0.4)

        # side view: basal body
        mem = RoundedRectangle(corner_radius=0.1, width=4.0, height=0.3, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([3.9, -1.2, 0])
        axo = RoundedRectangle(corner_radius=0.3, width=1.1, height=3.9, stroke_color=BLUE, stroke_width=3.5,
                               fill_color=BLUE, fill_opacity=0.15).move_to([3.5, 0.9, 0])
        axo_l = label("axoneme", BLUE, 28).next_to(axo, RIGHT, buff=0.25)
        bb = chip("basal body", GREY, 26).move_to([3.5, -2.05, 0])
        cell_l = label("inside the cell", GREY, 24).move_to([3.5, -3.0, 0])
        self.at("basal body")
        self.play(FadeOut(VGroup(z, za, zb)), run_time=0.4)
        self.play(FadeIn(mem), GrowFromEdge(axo, DOWN), FadeIn(axo_l), run_time=0.8)
        self.play(FadeIn(bb, shift=UP * 0.1), FadeIn(cell_l), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Arms(SpokenScene):
    """side view of two doublets: arms on the A-tubule act on the next B-tubule and push it toward the tip."""

    def construct(self):
        x0, x1 = -5.6, 4.4
        lo_y, hi_y = -0.9, 0.9
        lo = RoundedRectangle(corner_radius=0.15, width=x1 - x0, height=0.5, stroke_color=BLUE, stroke_width=3.5,
                              fill_color=BLUE, fill_opacity=0.3).move_to([(x0 + x1) / 2, lo_y, 0])
        hi = RoundedRectangle(corner_radius=0.15, width=x1 - x0, height=0.5, stroke_color=PURPLE, stroke_width=3.5,
                              fill_color=PURPLE, fill_opacity=0.3).move_to([(x0 + x1) / 2, hi_y, 0])
        a_l = label("A-tubule of one doublet", BLUE, 26).move_to([-0.3, -1.65, 0])
        base_l = label("base", GREY, 26).move_to([-5.0, -2.35, 0])
        tip_l = label("tip", GREY, 26).move_to([3.8, -2.35, 0])
        s = ValueTracker(0.0)

        foot_y, head_y = lo_y + 0.25, hi_y - 0.25
        outer_x = [-4.4 + 1.9 * i for i in range(5)]
        inner_x = [-3.75 + 1.9 * i for i in range(5)]

        def arm(x, r):
            fx = x
            hx = x + s.get_value()
            op = 1.0 if r > 0.17 else 0.55
            g = VGroup(Line([fx, foot_y, 0], [hx, head_y, 0], color=YELLOW, stroke_width=9 if r > 0.17 else 6),
                       Circle(radius=r, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([hx, head_y - r * 0.4, 0]))
            return g.set_opacity(op)

        arms = VGroup(*[always_redraw(lambda x=x: arm(x, 0.2)) for x in outer_x],
                      *[always_redraw(lambda x=x: arm(x, 0.14)) for x in inner_x])
        upper = VGroup(hi)
        upper.add_updater(lambda m: None)
        hi_pos = hi.get_center().copy()
        hi.add_updater(lambda m: m.move_to(hi_pos + [s.get_value(), 0, 0]))

        self.at("Along each")
        self.play(FadeIn(lo), FadeIn(a_l), FadeIn(base_l), FadeIn(tip_l), run_time=0.7)
        self.add(hi)
        self.play(FadeIn(hi), run_time=0.01)
        self.at("two rows")
        self.add(arms)
        self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.15) for a in arms], lag_ratio=0.12), run_time=1.2)
        leg_o = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1),
                       T("outer row", 22, YELLOW)).arrange(RIGHT, buff=0.15)
        leg_i = VGroup(Circle(radius=0.14, stroke_width=0, fill_color=YELLOW, fill_opacity=0.55),
                       T("inner row", 22, YELLOW)).arrange(RIGHT, buff=0.15)
        leg = VGroup(leg_o, leg_i).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([5.0, 0.0, 0])
        leg.shift([6.2 - leg.get_right()[0], 0, 0])
        self.play(FadeIn(leg), run_time=0.4)

        miss = T("absent from the four men's cilia", 28, RED).move_to([0, -3.05, 0])
        self.at("These are the arms")
        self.play(FadeIn(miss, shift=UP * 0.1), Indicate(arms, color=YELLOW, scale_factor=1.1), run_time=0.9)

        b_l = label("B-tubule of the next doublet", PURPLE, 26).move_to([-0.3, 1.75, 0])
        self.at("motor head")
        self.play(FadeOut(miss), FadeIn(b_l), run_time=0.5)

        minus = VGroup(arr([-4.6, 2.55, 0], [-5.9, 2.55, 0], PURPLE), T("minus end, at the base", 24, PURPLE))
        minus[1].move_to([-3.1, 2.55, 0])
        minus[0].put_start_and_end_on([-4.85, 2.55, 0], [-5.9, 2.55, 0])
        self.at("minus end")
        self.play(FadeIn(minus), run_time=0.6)

        push = VGroup(arr([-0.4, 2.55, 0], [1.5, 2.55, 0], YELLOW, w=7), T("pushed toward the tip", 24, YELLOW))
        push[1].move_to([3.55, 2.55, 0])
        self.at("toward the tip")
        self.play(FadeIn(push), s.animate.set_value(1.4), run_time=2.0, rate_func=smooth)
        self.finish()


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
class S04Cards(SpokenScene):
    """two card strips, glued at one end and tied along their length: pushing one makes the pair curve."""

    def construct(self):
        o = np.array([-5.4, -2.0, 0])
        K = ValueTracker(0.0)
        pair_m = always_redraw(lambda: pair(o, k=K.get_value()))
        q = T("Why does pushing make a bend?", 36, font=TITLE_FONT).move_to([0, 3.05, 0])
        self.at("Why does pushing")
        self.play(Write(q), run_time=1.4)
        self.at("two strips of card")
        self.add(pair_m)
        self.play(FadeIn(pair_m), run_time=0.6)
        lb_top = label("doublet", BLUE, 26).move_to(o + [3.0, 0.95, 0])
        lb_bot = label("neighbouring doublet", BLUE, 26).move_to(o + [5.5, -0.95, 0])
        self.play(FadeIn(lb_top), FadeIn(lb_bot), run_time=0.4)
        glue = label("glued at one end", GREY, 26).move_to(o + [1.4, -1.25, 0])
        self.at("glued together")
        self.play(FadeIn(glue, shift=UP * 0.1), run_time=0.5)
        ties_l = label("tied loosely", ORANGE, 26).move_to(o + [7.2, 0.95, 0])
        self.at("tied loosely")
        self.play(FadeIn(ties_l, shift=DOWN * 0.1), run_time=0.5)

        push = arr(o + [1.0, 1.7, 0], o + [3.2, 1.7, 0], YELLOW, w=9)
        push_l = label("push", YELLOW, 32).next_to(push, UP, buff=0.12)
        self.at("Push one strip")
        self.play(FadeOut(lb_top), FadeOut(lb_bot), FadeOut(glue), FadeOut(ties_l),
                  FadeIn(push), FadeIn(push_l), run_time=0.5)
        self.at("cannot slide apart")
        self.play(K.animate.set_value(0.08), FadeOut(push), FadeOut(push_l), run_time=2.2, rate_func=smooth)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S05Cut(SpokenScene):
    """the bend, then trypsin cuts the links and the pushed doublet slides out straight."""

    def construct(self):
        o = np.array([-5.4, -1.9, 0])
        K = ValueTracker(0.0)
        SL = ValueTracker(0.0)
        TO = ValueTracker(1.0)
        TC = ValueTracker(0.0)       # 0 orange links ... 1 red links
        AN = ValueTracker(1.0)
        pair_m = always_redraw(lambda: pair(o, k=K.get_value(), slide=SL.get_value(), tie_op=TO.get_value(),
                                            anchor=AN.get_value() > 0.5,
                                            tie_col=interpolate_color(ManimColor(ORANGE), ManimColor(RED), TC.get_value())))
        self.add(pair_m)
        self.play(FadeIn(pair_m), run_time=0.01)

        anch = label("anchored base", GREY, 26).move_to(o + [1.0, -1.2, 0])
        self.at("base is anchored")
        self.play(FadeIn(anch, shift=UP * 0.1), run_time=0.5)
        links = label("links", ORANGE, 30).move_to(o + [7.2, 0.95, 0])
        self.at("links resist")
        self.play(FadeIn(links, shift=DOWN * 0.1), run_time=0.5)
        push = arr(o + [1.0, 1.7, 0], o + [3.2, 1.7, 0], YELLOW, w=9)
        push_l = label("dynein pushes", YELLOW, 28).next_to(push, UP, buff=0.12)
        self.at("becomes a bend")
        self.play(FadeOut(links), FadeIn(push), FadeIn(push_l), run_time=0.4)
        self.play(K.animate.set_value(0.08), FadeOut(push), FadeOut(push_l), run_time=1.8, rate_func=smooth)
        bend_l = label("bend", TEXT, 36, weight=BOLD).move_to([1.5, 2.6, 0])
        self.play(FadeIn(bend_l), run_time=0.4)

        # reset and cut
        self.at("took the resistance away")
        self.play(FadeOut(bend_l), FadeOut(anch), K.animate.set_value(0.0), run_time=0.8)
        tr = chip("trypsin", RED, size=30).move_to([-2.8, 1.5, 0])
        cut_l = label("cuts the links", RED, 28).next_to(tr, RIGHT, buff=0.3)
        self.at("digested")
        self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(cut_l), TC.animate.set_value(1.0), run_time=0.7)
        self.play(TO.animate.set_value(0.0), AN.animate.set_value(0.0), run_time=0.5)
        self.play(FadeOut(tr), FadeOut(cut_l), run_time=0.3)
        atp = chip("ATP", GOLD, size=30).move_to([-3.4, 1.5, 0])
        push2 = arr(o + [1.0, 1.7, 0], o + [3.2, 1.7, 0], YELLOW, w=9)
        push2_l = label("dynein pushes", YELLOW, 28).next_to(push2, UP, buff=0.12)
        self.at("added")
        self.play(FadeIn(atp, shift=DOWN * 0.1), run_time=0.4)
        self.play(FadeIn(push2), FadeIn(push2_l), atp.animate.move_to(o + [4.5, 1.2, 0]), run_time=0.8)
        df = RoundedRectangle(corner_radius=0.2, width=11.4, height=2.2, stroke_color=GREY, stroke_width=3).move_to(o + [4.7, 0.0, 0])
        df_l = label("dark-field view", GREY, 26).next_to(df, DOWN, buff=0.12).align_to(df, LEFT)
        self.at("dark")
        self.play(Create(df), FadeIn(df_l), run_time=0.8)
        self.at("slid apart")
        self.play(SL.animate.set_value(1.5), FadeOut(atp), FadeOut(df), FadeOut(df_l), run_time=1.2, rate_func=smooth)
        slid = label("the doublets slide apart", GREEN, 32).move_to([0.6, -3.1, 0])
        self.play(FadeIn(slid), run_time=0.3)

        same = label("microtubules keep their length", TEXT, 30).move_to([0.6, 2.9, 0])
        self.at("shorten microtubules")
        self.play(FadeOut(push2), FadeOut(push2_l), FadeIn(same, shift=DOWN * 0.1), run_time=0.5)
        self.at("slides them")
        self.play(Indicate(slid, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S06Test(SpokenScene):
    """the sliding test and what each outcome means; ends on the bend rule."""

    def construct(self):
        steps = VGroup(chip("isolate axonemes", BLUE, 28), chip("cut the links", ORANGE, 28),
                       chip("add ATP", GOLD, 28)).arrange(RIGHT, buff=1.0).move_to([0, 2.6, 0])
        arrs = VGroup(arr(steps[0].get_right(), steps[1].get_left(), GREY), arr(steps[1].get_right(), steps[2].get_left(), GREY))
        head = T("a paralysed flagellum", 28, GREY).move_to([0, 3.4, 0])
        self.at("This gives a test")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        self.at("Isolate the")
        self.play(FadeIn(steps[0], shift=RIGHT * 0.2), run_time=0.5)
        self.at("cut the links")
        self.play(GrowArrow(arrs[0]), FadeIn(steps[1], shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(arrs[1]), FadeIn(steps[2], shift=RIGHT * 0.2), run_time=0.5)

        lx, rx = -3.3, 3.5
        left_h = chip("doublets slide apart", GREEN, 28).move_to([lx, 1.1, 0])
        right_h = chip("no sliding", RED, 28).move_to([rx, 1.1, 0])
        l_mini = pair(np.array([lx - 2.0, -0.15, 0]), k=0.0, slide=1.4, L=3.4, ties=(), anchor=False, top=GREEN, bot=BLUE)
        r_mini = pair(np.array([rx - 1.7, -0.15, 0]), k=0.0, slide=0.0, L=3.4, ties=(), anchor=False, top=RED, bot=RED)
        self.at("slide apart")
        self.play(FadeIn(left_h, shift=DOWN * 0.1), FadeIn(l_mini), run_time=0.7)
        l_res = chip("some motors work", GREEN, 30).move_to([lx, -1.25, 0])
        self.at("motors work")
        self.play(FadeIn(l_res, shift=DOWN * 0.1), run_time=0.5)
        l_why = T("fault is in regulating the motors\nor turning sliding into bending", 25, TEXT,
                  line_spacing=0.85).move_to([lx, -2.35, 0])
        self.at("If they are")
        self.play(FadeIn(l_why), run_time=0.6)
        l_where = T("radial spokes, central pair,\nnexin-dynein regulatory complex", 25, GREY,
                    line_spacing=0.85).move_to([lx, -3.25, 0])
        self.at("radial spokes")
        self.play(FadeIn(l_where), run_time=0.6)

        r_res = chip("suspect the dynein arms", RED, 28).move_to([rx, -1.25, 0])
        r_why = T("missing or inactive", 26, TEXT).move_to([rx, -2.1, 0])
        self.at("do not slide")
        self.play(FadeIn(right_h, shift=DOWN * 0.1), FadeIn(r_mini), run_time=0.7)
        self.play(FadeIn(r_res, shift=DOWN * 0.1), FadeIn(r_why), run_time=0.6)

        # the rule
        self.at("A bend is sliding")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        eq_a = pair(np.array([-6.0, -0.1, 0]), k=0.0, slide=1.0, L=3.0, ties=(), anchor=False, top=YELLOW)
        sl_l = label("sliding", YELLOW, 36, weight=BOLD).move_to([-4.4, -1.2, 0])
        plus = T("+", 60, TEXT).move_to([-1.7, -0.1, 0])
        eq_b = pair(np.array([-0.9, -0.1, 0]), k=0.0, slide=0.0, L=3.0, ties=(0.8, 1.9), anchor=True, top=BLUE)
        lk_l = label("links resist", ORANGE, 36, weight=BOLD).move_to([0.6, -1.2, 0])
        eq = T("=", 60, TEXT).move_to([3.0, -0.1, 0])
        bent = pair(np.array([3.6, -1.5, 0]), k=0.3, slide=0.0, L=2.6, ties=(0.8, 1.9), anchor=True, top=BLUE)
        bd_l = label("bend", TEXT, 36, weight=BOLD).move_to([5.0, 1.4, 0])
        self.play(FadeIn(eq_a), FadeIn(sl_l), run_time=0.5)
        self.play(FadeIn(plus), FadeIn(eq_b), FadeIn(lk_l), run_time=0.5)
        self.play(FadeIn(eq), FadeIn(bent), FadeIn(bd_l), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "A bend is sliding that the links resist."
