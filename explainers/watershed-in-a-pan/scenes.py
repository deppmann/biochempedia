"""A watershed in a pan: we all live downstream  (Biochemistrypedia, Biology Together film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Everything drawn is a schematic: side views and from-above sketches, none to scale.

COLOR MAP (one color per concept, whole film)
  BLUE   = water (rain, runoff, streams, rivers, the bay, a puddle)
  TAN    = a ridge (the high ground that splits one watershed from the next)
  GREEN  = a watershed (the land that drains to one place)
  ORANGE = things the water picks up and carries (soil, litter, pet waste, lawn fertilizer)
  GREY   = land, outlines, labels, de-emphasized
  GOLD   = the title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

TAN = "#C9A27A"
ORANGE = "#F29E4C"
LAND = "#8B93A1"
FLOOR = -3.4          # bottom of the land blocks
XL, XR = -6.3, 6.3    # left and right edge of the land blocks


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def P(x, y):
    return np.array([x, y, 0.0])


def land_poly(f, n=61, color=LAND, op=0.25):
    xs = np.linspace(XL, XR, n)
    pts = [P(x, f(x)) for x in xs] + [P(XR, FLOOR), P(XL, FLOOR)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=op)


def surf_line(f, n=61, color="#B8BFCC", w=5):
    xs = np.linspace(XL, XR, n)
    return VMobject().set_points_as_corners([P(x, f(x)) for x in xs]).set_stroke(color, w).set_fill(opacity=0)


def region(f, xa, xb, color=GREEN, op=0.28, n=40):
    xs = np.linspace(xa, xb, n)
    pts = [P(x, f(x)) for x in xs] + [P(xb, FLOOR), P(xa, FLOOR)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=op)


def pool(f, xa, xb, level, color=BLUE, op=0.75, n=60):
    """water sitting in a low spot: between the surface and a flat level."""
    xs = [x for x in np.linspace(xa, xb, n) if f(x) < level]
    xl, xr = xs[0], xs[-1]
    pts = [P(x, f(x)) for x in xs] + [P(xr, level), P(xl, level)]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=op)


def path_on(f, xa, xb, lift=0.14, n=50):
    xs = np.linspace(xa, xb, n)
    return VMobject().set_points_as_corners([P(x, f(x) + lift) for x in xs])


def trail(f, xa, xb, color=BLUE, w=6, lift=0.2):
    """a blue line along the surface with an arrowhead at its far end."""
    xs = np.linspace(xa, xb, 40)
    pts = [P(x, f(x) + lift) for x in xs]
    ln = VMobject().set_points_as_corners(pts).set_stroke(color, w).set_fill(opacity=0)
    d = pts[-1] - pts[-4]
    ang = np.arctan2(d[1], d[0])
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.2).rotate(ang - PI / 2)
    tip.move_to(pts[-1])
    return VGroup(ln, tip)


def drop(pos, r=0.11):
    return Dot(pos, radius=r, color=BLUE)


def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def note(text, pos, size=22):
    return T(text, size, GREY).move_to(pos)


# --- the paper landscape (side view) used in scenes 2 and 3 ------------------------------------
def _g(x, c, w):
    return np.exp(-((x - c) / w) ** 2)


def H(x):
    return -0.9 + 2.6 * _g(x, 0.2, 1.3) + 1.2 * _g(x, -5.8, 1.6) + 0.35 * _g(x, 2.9, 0.7) - 0.10 * x


def HILL(x):
    return 1.45 * H(x) - 0.2


def FLAT(x):
    return -0.8 + 0.0 * x


_xs = np.linspace(XL, XR, 2001)
RIDGE_X = float(_xs[(_xs > -1) & (_xs < 1.5)][np.argmax(HILL(_xs[(_xs > -1) & (_xs < 1.5)]))])
_lv = _xs[(_xs > -5) & (_xs < -0.8)]
VALLEY_X = float(_lv[np.argmin(HILL(_lv))])
VALLEY_Y = float(HILL(VALLEY_X))
BAY_LEVEL = float(HILL(XR)) + 0.55


def paper_pools(valley_level=None, bay_level=None):
    out = []
    if valley_level is not None:
        out.append(pool(HILL, -5.0, -0.8, VALLEY_Y + valley_level))
    if bay_level is not None:
        out.append(pool(HILL, 2.5, XR, float(HILL(XR)) + bay_level))
    return out


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "A Watershed in a Pan"
    TITLE = "We all live downstream"


# ---------------------------------------------------------------------------------------------
class S01Rain(SpokenScene):
    """a sloping street, a question mark, drops fall; some soak in; the rest runs downhill into a puddle."""

    def construct(self):
        def SY(x):
            return 1.9 - 0.4177 * (x - XL) if x < 1.6 else -1.4

        land = land_poly(SY)
        surf = surf_line(SY)
        street = path_on(SY, -5.4, 1.2, lift=0.0).set_stroke("#5B6270", 16).set_fill(opacity=0)
        street_lbl = note("your street", P(-3.3, -0.35), 26)
        q = T("?", 110, BLUE, weight=BOLD).move_to(P(3.9, -0.55))
        title = T("Where does the rain go?", 34, font=TITLE_FONT).move_to(P(3.2, 2.5))

        self.at("Where does rain go")
        self.play(FadeIn(land), Create(surf), FadeIn(street), FadeIn(street_lbl), run_time=0.6)
        self.play(Write(title), FadeIn(q, scale=0.8), run_time=0.7)

        # rain lands on the street
        self.at("lands on your street")
        xs = [-5.0, -4.2, -3.4, -2.6, -1.8, -1.0, -0.2]
        falls = [drop(P(x, 3.0)) for x in xs]
        self.add(*falls)
        self.play(LaggedStart(*[d.animate.move_to(P(x, SY(x) + 0.14)) for d, x in zip(falls, xs)], lag_ratio=0.1),
                  run_time=1.0, rate_func=linear)
        self.play(*[FadeOut(d) for d in falls], run_time=0.2)

        # the puddle replaces the question
        puddle0 = Ellipse(width=1.3, height=0.22, fill_color=BLUE, fill_opacity=0.8, stroke_width=0).move_to(P(3.9, -1.3))
        self.at("Watch a puddle")
        self.play(FadeOut(title), ReplacementTransform(q, puddle0), run_time=0.7)

        # water moving downhill
        down = trail(SY, -5.0, 3.1, lift=0.3)
        runners = [drop(P(x, SY(x) + 0.14)) for x in (-4.6, -3.2, -1.8)]
        self.at("moving downhill")
        self.add(*runners)
        self.play(Create(down[0]), FadeIn(down[1]), *[MoveAlongPath(r, path_on(SY, x, 3.5)) for r, x in zip(runners, (-4.6, -3.2, -1.8))],
                  run_time=1.0, rate_func=linear)
        puddle1 = Ellipse(width=2.2, height=0.3, fill_color=BLUE, fill_opacity=0.8, stroke_width=0).move_to(P(3.9, -1.3))
        self.play(*[FadeOut(r) for r in runners], Transform(puddle0, puddle1), run_time=0.25)

        # some soaks in
        self.at("Some rain soaks")
        self.play(FadeOut(down), run_time=0.3)
        sx = [-5.0, -4.3, -3.6]
        sd = [drop(P(x, 3.0)) for x in sx]
        self.add(*sd)
        self.play(LaggedStart(*[d.animate.move_to(P(x, SY(x) + 0.14)) for d, x in zip(sd, sx)], lag_ratio=0.15),
                  run_time=0.9, rate_func=linear)
        soak = note("some soaks into the ground", P(-3.9, -1.5), 24)
        self.play(*[d.animate.shift(DOWN * 0.8).set_opacity(0) for d in sd], FadeIn(soak), run_time=0.9)

        # ground full or hard -> the rest runs off
        self.at("full or hard")
        full = note("ground full or hard", P(-3.9, -1.5), 24)
        self.play(ReplacementTransform(soak, full), run_time=0.5)
        rx = [-5.0, -4.2, -3.4, -2.6, -1.8, -1.0]
        self.at("the rest runs")
        rd = [drop(P(x, 3.0)) for x in rx]
        self.add(*rd)
        self.play(LaggedStart(*[d.animate.move_to(P(x, SY(x) + 0.14)) for d, x in zip(rd, rx)], lag_ratio=0.1),
                  run_time=0.9, rate_func=linear)
        down2 = trail(SY, -5.0, 3.1, lift=0.3)
        self.play(Create(down2[0]), FadeIn(down2[1]),
                  *[MoveAlongPath(d, path_on(SY, x, 3.6)) for d, x in zip(rd, rx)], run_time=1.6, rate_func=linear)
        puddle2 = Ellipse(width=3.4, height=0.42, fill_color=BLUE, fill_opacity=0.8, stroke_width=0).move_to(P(3.9, -1.25))
        self.play(*[FadeOut(d) for d in rd], Transform(puddle0, puddle2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Paper(SpokenScene):
    """flat paper crumples into hills and valleys; a low corner becomes the bay; a ridge; drops run both ways."""

    def construct(self):
        flat_land, flat_surf = land_poly(FLAT), surf_line(FLAT)
        land, surf = land_poly(HILL), surf_line(HILL)
        scale_note = note("the paper from the side: a sketch, not to scale", P(-3.7, -3.2), 22)

        self.at("In the activity")
        self.play(FadeIn(flat_land), Create(flat_surf), FadeIn(scale_note), run_time=0.8)
        self.at("crumples paper")
        self.play(Transform(flat_land, land), Transform(flat_surf, surf), run_time=1.6)
        hv = note("hill", P(-5.3, float(HILL(-5.6)) + 0.45), 26)
        vv = note("valley", P(VALLEY_X, VALLEY_Y - 0.55), 26)
        self.at("hills and")
        self.play(FadeIn(hv), run_time=0.3)
        self.at("valleys")
        self.play(FadeIn(vv), run_time=0.3)

        # the bay
        bay = pool(HILL, 2.5, XR, float(HILL(XR)) + 0.1)
        bay_big = pool(HILL, 2.5, XR, float(HILL(XR)) + 0.55)
        self.at("One low corner")
        self.play(FadeIn(bay), run_time=0.4)
        self.at("blue and called")
        self.play(Transform(bay, bay_big), run_time=0.8)
        bay_lbl = T("the bay", 28, BLUE).move_to(P(5.0, float(HILL(XR)) + 1.1))
        self.at("called the bay")
        self.play(FadeIn(bay_lbl, shift=DOWN * 0.1), run_time=0.4)

        # the ridge
        ridge = path_on(HILL, RIDGE_X - 0.9, RIDGE_X + 0.9, lift=0.05).set_stroke(TAN, 12).set_fill(opacity=0)
        ridge_lbl = T("ridge", 30, TAN, weight=BOLD).move_to(P(RIDGE_X - 1.75, float(HILL(RIDGE_X)) - 0.05))
        self.at("The high ground")
        self.play(FadeOut(hv), FadeOut(vv), Create(ridge), run_time=0.6)
        self.at("called a ridge")
        self.play(FadeIn(ridge_lbl, shift=DOWN * 0.1), run_time=0.4)

        # one side, then the other
        lx, rx = RIDGE_X - 0.5, RIDGE_X + 0.5
        d1 = drop(P(lx, 3.3))
        self.at("on one side")
        self.add(d1)
        self.play(d1.animate.move_to(P(lx, float(HILL(lx)) + 0.14)), run_time=0.8, rate_func=linear)
        self.at("flows one way")
        t1 = trail(HILL, lx, VALLEY_X + 0.35)
        self.play(MoveAlongPath(d1, path_on(HILL, lx, VALLEY_X)), Create(t1[0]), FadeIn(t1[1]), run_time=1.1, rate_func=linear)
        vp = pool(HILL, -5.0, -0.8, VALLEY_Y + 0.3)
        self.play(FadeOut(d1), FadeIn(vp), run_time=0.4)

        d2 = drop(P(rx, 3.3))
        self.at("on the other side")
        self.add(d2)
        self.play(d2.animate.move_to(P(rx, float(HILL(rx)) + 0.14)), run_time=0.8, rate_func=linear)
        self.at("the other way")
        t2 = trail(HILL, rx, 4.2)
        self.play(MoveAlongPath(d2, path_on(HILL, rx, 4.6)), Create(t2[0]), FadeIn(t2[1]), run_time=1.3, rate_func=linear)
        self.play(FadeOut(d2), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Watershed(SpokenScene):
    """the same paper: land draining to one place is green; the ridge splits two; two low spots, two watersheds."""

    def construct(self):
        land, surf = land_poly(HILL), surf_line(HILL)
        scale_note = note("the paper from the side: a sketch, not to scale", P(-3.7, -3.2), 22)
        vp = pool(HILL, -5.0, -0.8, VALLEY_Y + 0.3)
        bay = pool(HILL, 2.5, XR, float(HILL(XR)) + 0.55)
        ridge = path_on(HILL, RIDGE_X - 0.9, RIDGE_X + 0.9, lift=0.05).set_stroke(TAN, 12).set_fill(opacity=0)
        ridge_lbl = T("ridge", 30, TAN, weight=BOLD).move_to(P(RIDGE_X - 1.75, float(HILL(RIDGE_X)) - 0.05))
        self.add(land, surf, scale_note, vp, bay, ridge, ridge_lbl)

        # land that drains to one place
        right = region(HILL, RIDGE_X, XR)
        left = region(HILL, XL, RIDGE_X)
        wr = T("one watershed", 30, GREEN, weight=BOLD).move_to(P(3.4, 2.6))
        wl = T("the next watershed", 30, GREEN, weight=BOLD).move_to(P(-4.1, 2.9))
        flows = VGroup(*[trail(HILL, a, b, w=4, lift=0.2) for a, b in ((RIDGE_X + 0.6, 2.2), (2.6, 4.4))])
        self.at("All the land that drains")
        self.play(FadeIn(right), run_time=0.6)
        self.at("to the same stream")
        self.play(*[Create(f[0]) for f in flows], *[FadeIn(f[1]) for f in flows], run_time=0.9)
        self.at("is called a watershed")
        self.play(FadeIn(wr, shift=DOWN * 0.1), run_time=0.5)

        # a ridge splits
        split = DashedLine(P(RIDGE_X, float(HILL(RIDGE_X)) - 0.1), P(RIDGE_X, FLOOR), color=TAN, stroke_width=5)
        self.at("A ridge splits")
        self.play(FadeOut(flows), Create(split), run_time=0.7)
        self.at("one watershed from the next")
        self.play(FadeIn(left), FadeIn(wl, shift=DOWN * 0.1), run_time=0.7)

        # two low spots
        ls1 = bchip("low spot", BLUE, 24).move_to(P(VALLEY_X, VALLEY_Y + 1.15))
        ls2 = bchip("low spot", BLUE, 24).move_to(P(4.6, float(HILL(XR)) + 1.3))
        a1 = arr(ls1.get_bottom(), P(VALLEY_X, VALLEY_Y + 0.4), BLUE, w=4, tip=0.18)
        a2 = arr(ls2.get_bottom(), P(4.6, float(HILL(XR)) + 0.55), BLUE, w=4, tip=0.18)
        self.at("pools in more than")
        self.play(FadeIn(ls1), GrowArrow(a1), run_time=0.5)
        self.at("one low spot")
        self.play(FadeIn(ls2), GrowArrow(a2), run_time=0.5)
        self.at("has more than one watershed")
        self.play(Indicate(wr, color=GREEN, scale_factor=1.15), Indicate(wl, color=GREEN, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Downstream(SpokenScene):
    """from above: little streams join bigger streams and a river to the bay; things ride the water; a storm drain."""

    def construct(self):
        J1, J2, J3 = P(-2.1, 0.55), P(0.6, -0.45), P(1.7, -1.3)
        A = [P(-5.1, 2.6), P(-3.6, 1.7), J1]
        B = [P(-5.1, 0.9), P(-3.6, 0.8), J1]
        D = [P(-5.1, -0.9), P(-3.7, -0.5), J1]
        C = [P(0.4, 2.6), P(0.2, 1.2), J2]
        BIG = [J1, J2]
        RIV = [J2, J3, P(2.2, -1.65)]
        E = [P(-3.3, -2.45), P(-1.0, -2.3), P(1.15, -0.9)]
        # the E creek joins the river at the first third of the river line

        def line(pts, w, color=BLUE):
            return VMobject().set_points_as_corners(pts).set_stroke(color, w).set_fill(opacity=0)

        bay = Ellipse(width=5.2, height=2.3, fill_color=BLUE, fill_opacity=0.55, stroke_color=BLUE, stroke_width=3).move_to(P(3.6, -2.3))
        bay_lbl = T("the low corner", 26, BLUE).move_to(P(4.8, -0.62))
        small = [line(p, 3) for p in (A, B, D, C)]
        big = line(BIG, 6)
        river = line(RIV, 10)

        self.at("Little streams join")
        self.play(*[Create(s) for s in small], run_time=1.0)
        lbl1 = note("little streams", P(-4.1, 3.3), 24)
        self.play(FadeIn(lbl1), run_time=0.3)
        self.at("bigger streams")
        self.play(Create(big), run_time=0.7)
        lbl2 = note("bigger stream", P(-1.2, 0.95), 24)
        self.play(FadeIn(lbl2), run_time=0.3)
        self.at("join rivers")
        self.play(Create(river), FadeIn(bay), FadeIn(bay_lbl), run_time=0.9)
        lbl3 = note("river", P(-0.3, -1.0), 24)
        self.play(FadeIn(lbl3), run_time=0.3)

        sk = note("schematic, from above, not to scale", P(-2.6, -3.4), 22)
        self.play(FadeIn(sk), run_time=0.3)

        # it picks things up
        self.at("it picks things up")
        self.play(FadeOut(VGroup(lbl1, lbl2, lbl3)), run_time=0.4)
        specs = [("soil", A[0], A + [RIV[0], RIV[1], P(2.7, -2.0)]),
                 ("litter", B[0], B + [RIV[0], RIV[1], P(3.5, -2.0)]),
                 ("lawn fertilizer", D[0], D + [RIV[0], RIV[1], P(4.4, -2.0)]),
                 ("pet waste", C[0], C + [RIV[1], P(3.2, -2.9)])]
        chips = []
        for text, pos, _ in specs:
            c = bchip(text, ORANGE, 22)
            c.move_to(pos).shift(RIGHT * (c.width / 2 - 0.05) if text != "pet waste" else ORIGIN)
            chips.append(c)
        self.at("Soil litter")
        self.play(FadeIn(chips[0], scale=0.8), run_time=0.35)
        self.wait(0.15)
        self.play(FadeIn(chips[1], scale=0.8), run_time=0.35)
        self.at("pet waste")
        self.play(FadeIn(chips[3], scale=0.8), run_time=0.35)
        self.at("lawn fertilizer")
        self.play(FadeIn(chips[2], scale=0.8), run_time=0.35)

        # ride downstream
        self.at("can all go along")
        t_end = self.t_of("end up downstream") - self.elapsed() - 0.3
        t_end = max(2.0, t_end)
        # end positions inside the bay, in two rows
        ends = [P(2.2, -1.95), P(3.3, -1.95), P(3.7, -2.7), P(4.7, -1.95)]
        moves = []
        for (text, pos, pts), c, e in zip(specs, chips, ends):
            pth = VMobject().set_points_as_corners([pos] + pts[1:-1] + [e])
            moves.append(MoveAlongPath(c, pth))
        self.play(*moves, run_time=t_end, rate_func=smooth)
        self.at("end up downstream")
        self.play(*[c.animate.scale(1.1) for c in chips], run_time=0.3)
        self.play(*[c.animate.scale(1 / 1.1) for c in chips], run_time=0.3)

        # storm drain
        drain = bchip("storm drain", GREY, 24).move_to(P(-5.0, -2.45))
        pipe = line([drain.get_right() + RIGHT * 0.03, P(-3.3, -2.45)], 8, GREY)
        creek = line(E, 4)
        self.at("storm drains carry")
        self.play(FadeIn(drain), Create(pipe), run_time=0.5)
        self.at("straight to a creek")
        creek_lbl = note("creek", P(-1.9, -1.95), 24)
        self.play(Create(creek), FadeIn(creek_lbl), run_time=1.0)
        drop_ = drop(E[0], r=0.14)
        self.at("without cleaning it")
        self.play(MoveAlongPath(drop_, VMobject().set_points_as_corners(E)), run_time=1.0, rate_func=linear)
        self.play(FadeOut(drop_), run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Virginia(SpokenScene):
    """schematic bar of where Virginia's land drains: more than half to the Bay, the rest south or west."""

    def construct(self):
        title = T("Where Virginia's land drains", 40, font=TITLE_FONT).move_to(P(0, 3.3))
        W, Hh = 11.4, 1.7
        yb = 1.5
        wb = W * 0.55   # drawn visibly over half; only the words "more than half" are shown, no number
        outline = RoundedRectangle(corner_radius=0.2, width=W, height=Hh, stroke_color=GREY, stroke_width=3).move_to(P(0, yb))
        x0 = -W / 2
        bar_bay = Rectangle(width=wb, height=Hh - 0.1, stroke_width=0, fill_color=BLUE, fill_opacity=0.4).move_to(P(x0 + wb / 2 + 0.05, yb))
        bar_rest = Rectangle(width=W - wb - 0.1, height=Hh - 0.1, stroke_width=0, fill_color=LAND, fill_opacity=0.3).move_to(P(x0 + wb + (W - wb) / 2 - 0.05, yb))
        lbl_all = T("all the land in Virginia", 26, GREY).move_to(P(0, yb + 1.05))
        lbl_bay = T("more than half", 36, BLUE, weight=BOLD).move_to(bar_bay)
        lbl_rest = T("the rest", 36, TEXT).move_to(bar_rest)
        sch = note("a sketch, not to scale", P(0, -3.15), 24)

        self.at("More than half")
        self.play(FadeIn(title), Create(outline), FadeIn(lbl_all), FadeIn(sch), run_time=0.8)
        self.play(FadeIn(bar_bay), FadeIn(lbl_bay), run_time=0.7)
        bay_chip = bchip("Chesapeake Bay", BLUE, 30).move_to(P(bar_bay.get_center()[0], -0.85))
        self.at("Chesapeake Bay")
        self.play(GrowArrow(arr(bar_bay.get_bottom() + DOWN * 0.1, bay_chip.get_top(), BLUE)), FadeIn(bay_chip), run_time=0.7)

        # the rest
        xr = bar_rest.get_center()[0]
        south = bchip("south: the sounds of North Carolina", BLUE, 22).move_to(P(2.4, -0.85))
        west = bchip("west: toward the Gulf of Mexico", BLUE, 22).move_to(P(2.4, -2.0))
        self.at("Most of the rest")
        self.play(FadeIn(bar_rest), FadeIn(lbl_rest), run_time=0.6)
        self.at("south to the")
        self.play(GrowArrow(arr(P(2.4, yb - 0.95), south.get_top(), BLUE)), FadeIn(south), run_time=0.7)
        self.at("or west toward")
        elbow = Line(P(5.35, yb - 0.95), P(5.35, -2.0), color=BLUE, stroke_width=5)
        self.play(Create(elbow), run_time=0.4)
        self.play(GrowArrow(arr(P(5.35, -2.0), west.get_right(), BLUE)), FadeIn(west), run_time=0.5)

        # a map helps
        mp = bchip("a map of Virginia's watersheds", GREY, 28).move_to(P(-2.4, -3.1))
        town = bchip("your town", TEXT, 26).move_to(P(2.9, -3.1))
        self.at("A map of")
        self.play(FadeOut(sch), FadeIn(mp, shift=UP * 0.15), run_time=0.6)
        self.at("find your town")
        self.play(GrowArrow(arr(mp.get_right(), town.get_left(), GREY)), FadeIn(town), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """your yard, creek, river, bay: the path of the rain; we all live downstream; safety notes on the page."""

    def construct(self):
        yard = bchip("your yard", GREY, 36).move_to(P(-4.5, 2.0))
        creek = bchip("creek", BLUE, 36).move_to(P(-1.4, 0.5))
        river = bchip("river", BLUE, 36).move_to(P(1.9, -1.0))
        bay = bchip("the Bay", BLUE, 36).move_to(P(5.0, -2.4))
        std = bchip("Virginia grade 4 standard", GREY, 34).move_to(P(0, 2.4))
        quote = T("we all live downstream", 60, font=TITLE_FONT).move_to(P(0, 0.0))
        saf = bchip("the safety notes are on the page", GREY, 30).move_to(P(-2.6, -2.9))

        cond = bchip("if your home is in\nthe Bay watershed", BLUE, 28).move_to(P(3.8, 0.75))
        m1 = bchip("model a watershed", GREY, 28).move_to(P(-3.0, 1.2))
        m2 = bchip("name the one they live in", GREY, 28).move_to(P(2.6, 1.2))
        self.at("standard asks")
        self.play(FadeIn(std, shift=DOWN * 0.1), run_time=0.5)
        self.at("model a watershed")
        self.play(FadeIn(m1, shift=DOWN * 0.1), run_time=0.4)
        self.at("name the one")
        self.play(FadeIn(m2, shift=DOWN * 0.1), run_time=0.4)
        self.at("we all live downstream")
        self.play(Write(quote), run_time=1.4)

        # the path
        a1 = arr(yard.get_right(), creek.get_top() + LEFT * 0.3, BLUE)
        a2 = arr(creek.get_right(), river.get_top() + LEFT * 0.3, BLUE)
        a3 = arr(river.get_right(), bay.get_top() + LEFT * 0.3, BLUE)
        self.at("Bay watershed")
        self.play(FadeOut(VGroup(std, m1, m2)), quote.animate.scale(0.65).move_to(P(3.4, 2.45)), run_time=0.6)
        self.play(FadeIn(cond), run_time=0.4)
        self.at("runs off your yard")
        self.play(FadeIn(yard, shift=DOWN * 0.1), run_time=0.5)
        self.at("can reach it")
        ghost = DashedVMobject(bay[1].copy().set_fill(opacity=0), num_dashes=30).set_color(BLUE)
        self.play(Create(ghost), run_time=0.5)
        self.at("through creeks")
        self.play(GrowArrow(a1), FadeIn(creek), run_time=0.7)
        self.at("and rivers")
        self.play(GrowArrow(a2), FadeIn(river), run_time=0.7)
        self.play(GrowArrow(a3), FadeOut(ghost), FadeIn(bay), run_time=0.7)

        # trace it on a map
        self.at("can trace")
        dot = Dot(yard.get_right(), radius=0.16, color=GOLD)
        self.play(FadeIn(dot), run_time=0.2)
        for pt in (creek.get_top() + LEFT * 0.3, river.get_top() + LEFT * 0.3, bay.get_top() + LEFT * 0.3):
            self.play(dot.animate.move_to(pt), run_time=0.7, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.2)

        # one idea for a younger child
        put = bchip("what we put on the land", ORANGE, 26).move_to(P(-4.0, -0.55))
        pdot = Dot(P(-4.5, 2.0), radius=0.2, color=ORANGE)
        self.at("what we put")
        self.play(FadeIn(put, shift=UP * 0.1), run_time=0.5)
        self.at("reach the water")
        pth = VMobject().set_points_as_corners([yard.get_right(), a1.get_end(), a2.get_start(), a2.get_end(), a3.get_start(), a3.get_end()])
        pdot.move_to(yard.get_right())
        self.play(FadeIn(pdot), run_time=0.15)
        self.play(MoveAlongPath(pdot, pth), run_time=1.6, rate_func=linear)
        self.at("The safety notes")
        self.play(FadeOut(put), FadeOut(pdot), FadeIn(saf, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "We all live downstream."
