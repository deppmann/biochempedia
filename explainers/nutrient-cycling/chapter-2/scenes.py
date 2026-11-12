"""Nutrient cycling, film 2: Two Halves of One Lake (Biochemistrypedia explainer)

Same colour map as film 1 (../scenes.py):
  GOLD dashed line = the boundary     BLUE arrows = inputs crossing in
  RED arrows = outputs crossing out   GREY ring = the internal loop
  TEAL blocks = nitrogen (N)          GOLD blocks = phosphorus (P)
"""
import os
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

CLEAR = "#2B4A63"
ALGAE = "#3E9B4F"
BEAD = "#8EE07A"
NOTE = "schematic"


class Sc(SpokenScene):
    """SpokenScene plus film 1's faint field of drifting teal motes."""
    def setup(self):
        super().setup()
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        ms = VGroup()
        for _ in range(30):
            d = Dot(radius=rng.uniform(0.07, 0.14), color=TEAL).set_opacity(rng.uniform(0.25, 0.5))
            d.move_to([rng.uniform(-6.6, 6.6), rng.uniform(-3.6, 3.6), 0])
            d.v = (rng.uniform(-0.4, 0.4), rng.uniform(0.2, 0.6))

            def drift(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > 3.8:
                    m.shift(DOWN * 7.6)
                if abs(m.get_x()) > 6.7:
                    m.shift(LEFT * 13.4 * (1 if m.get_x() > 0 else -1))
            d.add_updater(drift)
            ms.add(d)
        ms.set_z_index(-10)
        self.add(ms)


# --- helpers copied from film 1 -----------------------------------------------------------------
def pulse(m, k=1.12, t=0.8):
    return m.animate.scale(k).set_run_time(t).set_rate_func(there_and_back)


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0.0, color=color, stroke_width=w,
                 tip_length=tip, max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=40)


def node(text, color=TEAL, size=30):
    lab = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.14, width=lab.width + 0.44, height=lab.height + 0.44, stroke_color=color,
                           stroke_width=3, fill_color=BG, fill_opacity=1)
    g = VGroup(box, lab.move_to(box))
    g.set_z_index(3)
    return g


def blk(color=TEAL, s=0.3):
    b = Square(s, stroke_width=0, fill_color=color, fill_opacity=1)
    b.set_z_index(1)
    return b


def flow(pts, n=3, period=4.0, color=TEAL, cols=None):
    """Blocks that keep sliding along a polyline (cols alternates colours)."""
    path = VMobject().set_points_as_corners([np.array(p, dtype=float) for p in pts])
    g = VGroup()
    for i in range(n):
        b = blk(cols[i % len(cols)] if cols else color)
        b.ph = i / n
        b.move_to(path.point_from_proportion(b.ph))

        def upd(m, dt, path=path, period=period):
            m.ph = (m.ph + dt / period) % 1.0
            m.move_to(path.point_from_proportion(m.ph))
        b.add_updater(upd)
        g.add(b)
    return g


def boundary():
    r = RoundedRectangle(corner_radius=0.3, width=9.4, height=6.0, stroke_color=GOLD, stroke_width=5).move_to([0, -0.3, 0])
    d = DashedVMobject(r, num_dashes=70, dashed_ratio=0.55)
    d.clk = 0.0

    def pulse_w(m, dt):
        m.clk += dt
        if not getattr(m, "hold", False):
            m.set_stroke(width=5 + 1.5 * np.sin(m.clk * 2.2))
    d.add_updater(pulse_w)
    return d


# --- lake pieces ---------------------------------------------------------------------------------
def water_rect(w, h, cx, cy, tr, r=0.8):
    m = RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color="#7FA7C4", stroke_width=2, fill_opacity=0.9)
    m.move_to([cx, cy, 0])
    m.set_z_index(-2)
    m.add_updater(lambda mm: mm.set_fill(interpolate_color(ManimColor(CLEAR), ManimColor(ALGAE), tr.get_value()), opacity=0.9))
    return m


def algae(x0, x1, y0, y1, n, tr, seed=1):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.06, 0.13), color=BEAD)
        d.home = np.array([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
        d.ph = rng.uniform(0, 6.28)
        d.clk = 0.0
        d.move_to(d.home)

        def u(m, dt):
            m.clk += dt
            m.move_to(m.home + np.array([0.18 * np.sin(m.clk * 0.7 + m.ph), 0.12 * np.cos(m.clk * 0.9 + m.ph), 0]))
            m.set_opacity(0.85 * min(1.0, tr.get_value() * 1.5))
        d.add_updater(u)
        g.add(d)
    g.set_z_index(-1)
    return g


def sky_band():
    band = Rectangle(width=9.4, height=0.8, stroke_width=0, fill_color=TEAL, fill_opacity=0.14).move_to([0, 3.4, 0])
    lab = T("air", 28, TEXT).move_to([-1.8, 3.4, 0])
    return VGroup(band, lab)


def dotted(x, y0, y1, color=TEAL, w=7):
    ln = DashedLine([x, y0, 0], [x, y1 + 0.2, 0], color=color, stroke_width=w, dash_length=0.18)
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.2).rotate(PI).move_to([x, y1 + 0.1, 0])
    return VGroup(ln, tip)


def xmark(x, y, s=0.28):
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=YELLOW, stroke_width=9),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=YELLOW, stroke_width=9)).set_z_index(4)


def lab(text, x, y, color=TEXT, size=28):
    return T(text, size, color).move_to([x, y, 0])


NP = [TEAL, GOLD]


def in_arrow(pts_a, pts_b, cols, w=7, n=4, period=3.0):
    """A blue input arrow plus a flow of blocks along it."""
    a = arr(pts_a, pts_b, BLUE, w)
    f = flow([pts_a, pts_b], n, period, cols=cols)
    return a, f


# side-view geometry (s01, s02, s14)
SW_X, SW_Y = 0.0, -1.0


def side_water(tr):
    return water_rect(8.8, 3.4, SW_X, SW_Y, tr, 0.8)


def side_inputs():
    """inflow (left), dust (top), fertilizer (right): each carries both N and P."""
    a1, f1 = in_arrow([-6.5, -0.4, 0], [-4.4, -0.4, 0], NP, 7, 3, 2.6)
    a2, f2 = in_arrow([0.3, 3.0, 0], [0.3, 0.8, 0], NP, 7, 4, 3.0)
    a3, f3 = in_arrow([6.5, -0.4, 0], [4.4, -0.4, 0], NP, 7, 3, 2.6)
    l1 = lab("inflow", -5.5, 0.3, BLUE)
    l2 = lab("dust", 1.05, 2.0, BLUE)
    l3 = lab("fertilizer", 5.85, 0.3, BLUE)
    return a1, f1, a2, f2, a3, f3, l1, l2, l3


def two_nodes():
    pn = node("P: inflow, dust, fertilizer", GOLD, 28).move_to([0, -0.4, 0])
    nn = node("N: those + fixation", TEAL, 28).move_to([0, -1.7, 0])
    return pn, nn


# =================================================================================================
class S00Title(TitleCard):
    LESSON = "Nutrient Cycling"
    TITLE = "Two Halves of One Lake"


class S01Link(Sc):
    def construct(self):
        tr = ValueTracker(0)
        wat, alg = side_water(tr), algae(-4.0, 4.0, -2.4, 0.4, 26, tr, 3)
        wb, sky = boundary(), sky_band()
        self.play(FadeIn(wat), Create(wb), FadeIn(sky), run_time=0.4)
        self.add(alg)
        self.at("Phosphorus has no major gas")
        pa = dotted(-4.2, 3.0, 1.0, GOLD)
        self.play(Create(pa), run_time=1.0)
        self.at("no microbe can fix it")
        xm = xmark(-4.2, 2.0)
        lp = lab("P: no major gas", -1.9, 2.0, GOLD)
        self.play(FadeIn(xm, scale=0.6), FadeIn(lp), run_time=0.8)
        self.at("Nitrogen can be fixed")
        na = dotted(4.2, 3.0, 1.0, TEAL)
        ln = lab("N fixation", 2.9, 2.0, TEAL)
        self.play(Create(na), FadeIn(ln), run_time=1.0)
        fl = flow([[4.2, 2.9, 0], [4.2, 1.1, 0]], 3, 3.0, TEAL)
        self.add(fl)
        self.at("when a lake turns green")
        self.play(tr.animate.set_value(1), run_time=1.8)
        self.at("which input should you cut")
        q = node("cut which input?", YELLOW, 32).move_to([0, -1.0, 0])
        self.play(FadeIn(q, scale=0.8), run_time=0.7)
        self.at("nitrogen or phosphorus")
        a1, f1 = in_arrow([-6.5, -0.2, 0], [-4.4, -0.2, 0], [TEAL], 7, 3, 2.4)
        a2, f2 = in_arrow([-6.5, -1.6, 0], [-4.4, -1.6, 0], [GOLD], 7, 3, 2.4)
        n1, n2 = lab("N input", -5.5, 0.3, TEAL), lab("P input", -5.5, -1.1, GOLD)
        self.play(GrowArrow(a1), FadeIn(n1), GrowArrow(a2), FadeIn(n2), run_time=1.0)
        self.add(f1, f2)
        self.finish()


class S02Doors(Sc):
    def construct(self):
        tr = ValueTracker(1)
        wat, alg = side_water(tr), algae(-4.0, 4.0, -2.4, 0.4, 26, tr, 3)
        wb, sky = boundary(), sky_band()
        self.add(wat, alg, wb, sky)
        a1, f1, a2, f2, a3, f3, l1, l2, l3 = side_inputs()
        self.at("as inputs")
        self.play(Indicate(wb, color=GOLD, scale_factor=1.0), run_time=1.0)
        self.at("inflowing water")
        self.play(GrowArrow(a1), FadeIn(l1), run_time=0.9)
        self.add(f1)
        self.at("dust")
        self.play(GrowArrow(a2), FadeIn(l2), run_time=0.9)
        self.add(f2)
        self.at("and fertilizer")
        self.play(GrowArrow(a3), FadeIn(l3), run_time=0.9)
        self.add(f3)
        self.at("Only nitrogen has a second kind")
        na = dotted(4.2, 3.0, 1.0, TEAL)
        ln = lab("N fixation", 2.9, 2.0, TEAL)
        self.play(Create(na), FadeIn(ln), run_time=1.2)
        fl = flow([[4.2, 2.9, 0], [4.2, 1.1, 0]], 3, 3.0, TEAL)
        self.add(fl)
        self.at("fixation from the air")
        self.play(Indicate(na, color=TEAL, scale_factor=1.0), Indicate(ln, color=TEAL), run_time=1.2)
        self.at("by microbes")
        pn, nn = two_nodes()
        self.play(FadeIn(pn, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(nn, shift=UP * 0.1), run_time=0.8)
        self.at("Which one sets")
        self.play(Indicate(pn, color=YELLOW, scale_factor=1.04), run_time=1.0)
        self.play(Indicate(nn, color=YELLOW, scale_factor=1.04), run_time=1.0)
        self.finish()


CANADA = [(-5.5, -0.5), (-5.0, 1.0), (-5.3, 2.2), (-3.5, 2.6), (-1.0, 2.4), (1.0, 1.9), (2.5, 2.3), (3.6, 1.2),
          (3.0, 0.2), (3.6, -0.6), (2.0, -1.2), (0.8, -1.6), (-1.5, -1.8), (-3.5, -1.7), (-5.2, -1.6)]
LAKES_POS = [(-4.5, 1.6), (-0.5, 2.0), (4.3, 1.6), (-4.5, -1.6), (-1.2, -0.4), (2.3, -0.9)]


def ellipse_lake(x, y, w=2.6, h=1.6, color=CLEAR):
    e = Ellipse(width=w, height=h, stroke_color="#7FA7C4", stroke_width=3, fill_color=color, fill_opacity=0.9)
    return e.move_to([x, y, 0])


class S03Schindler(Sc):
    def construct(self):
        mp = Polygon(*[[x + 1.0, y - 0.3, 0] for x, y in CANADA], stroke_color=GREY, stroke_width=4,
                     fill_color=GREY, fill_opacity=0.18)
        cn = lab("Canada", -3.4 + 1.0, 0.8, TEXT)
        sch = lab(NOTE, 5.4, -3.55, GREY, 22)
        self.play(FadeIn(mp), FadeIn(cn), FadeIn(sch), run_time=0.5)
        self.at("David Schindler")
        card = node("David W. Schindler, invited 1968", GOLD, 28).move_to([0, 3.3, 0])
        self.play(FadeIn(card, shift=DOWN * 0.1), run_time=0.9)
        self.at("whole lake experiments")
        self.play(Indicate(card, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.at("Northwestern Ontario")
        pin = VGroup(Line([0.6, -0.4, 0], [0.6, 0.35, 0], color=YELLOW, stroke_width=6),
                     Dot([0.6, 0.45, 0], radius=0.16, color=YELLOW)).set_z_index(3)
        pl = VGroup(lab("Experimental Lakes Area,", 0.6, -2.55, YELLOW), lab("northwestern Ontario", 0.6, -3.1, YELLOW))
        self.play(GrowFromPoint(pin, [0.6, -0.4, 0]), FadeIn(pl), run_time=1.0)
        self.play(Flash(Dot([0.6, 0.45, 0]), color=YELLOW, line_length=0.3), run_time=0.8)
        self.at("Small lakes were set aside")
        lakes = VGroup(*[ellipse_lake(x, y) for x, y in LAKES_POS])
        l226, l227 = lab("226", -1.2, -0.4, TEXT, 34), lab("227", 2.3, -0.9, TEXT, 34)
        ela = lab("Experimental Lakes Area", 0, 3.4, YELLOW)
        self.play(FadeOut(VGroup(mp, cn, pin, pl, card, sch)), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(k, scale=0.7) for k in lakes], lag_ratio=0.15), FadeIn(ela), run_time=1.6)
        self.play(FadeIn(l226), FadeIn(l227), run_time=0.6)
        self.at("whole ecosystems")
        self.play(*[Indicate(k, color=BLUE, scale_factor=1.06) for k in lakes], run_time=1.4)
        self.at("watched for years")
        self.play(Indicate(lakes[4], color=YELLOW, scale_factor=1.1), Indicate(lakes[5], color=YELLOW, scale_factor=1.1),
                  run_time=1.4)
        self.at("Short tests in bottles")
        body = RoundedRectangle(corner_radius=0.15, width=1.0, height=1.5, stroke_color=TEXT, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.35)
        neck = Rectangle(width=0.4, height=0.45, stroke_color=TEXT, stroke_width=4).next_to(body, UP, buff=0)
        bottle = VGroup(body, neck).move_to([-1.4, -0.3, 0]).set_z_index(4)
        bl = lab("bottle test", -1.4, -1.6, TEXT)
        self.play(VGroup(lakes, l226, l227).animate.set_opacity(0.12), FadeIn(bottle, scale=0.7), FadeIn(bl), run_time=1.0)
        self.at("miss slow changes")
        self.play(Indicate(bottle, color=YELLOW, scale_factor=1.08), run_time=1.2)
        self.at("rise in nitrogen fixation")
        ra = arr([2.3, -1.6, 0], [2.3, 1.3, 0], TEAL, 9)
        rl = lab("N fixation rising", 2.3, 1.8, TEAL)
        self.play(GrowArrow(ra), FadeIn(rl), run_time=2.0)
        self.finish()


# --- Lake 226 (top view) ---------------------------------------------------------------------------
AX, BX = -2.2, 2.2   # basin centres
LY = -1.0


def lake226(trB=None, trA=None, barrier=True):
    """Two basins of one lake, inside the gold boundary. Returns dict of mobjects."""
    trA = trA or ValueTracker(0)
    trB = trB or ValueTracker(0)
    wa = water_rect(4.3, 3.4, AX, LY, trA)
    wbb = water_rect(4.3, 3.4, BX, LY, trB)
    bar = Line([0, 0.8, 0], [0, -2.8, 0], color=TEXT, stroke_width=9).set_z_index(2)
    return dict(wa=wa, wb=wbb, bar=bar, trA=trA, trB=trB, bnd=boundary())


def nc_arrows():
    """N and C input arrows into both basins (carried through scenes 4-9)."""
    items = []
    for x, cols, col in [(-3.9, [TEAL], TEAL), (-1.4, [GREY], GREY), (1.4, [TEAL], TEAL), (4.0, [GREY], GREY)]:
        a, f = in_arrow([x, 3.0, 0], [x, 0.8, 0], cols, 7, 3, 2.8)
        a.set_color(BLUE)
        items.append((a, f))
    ls = [lab("N (nitrate)", -3.9, 3.45, TEAL), lab("C (sucrose)", -1.4, 3.45, GREY),
          lab("N (nitrate)", 1.4, 3.45, TEAL), lab("C (sucrose)", 4.0, 3.45, GREY)]
    # GREY text for sucrose would be low-contrast on the dark ground: draw it in TEXT
    ls[1].set_color(TEXT)
    ls[3].set_color(TEXT)
    return items, ls


def p_arrow():
    a, f = in_arrow([6.5, -1.2, 0], [4.4, -1.2, 0], [GOLD], 7, 3, 2.4)
    l = lab("P", 5.5, -0.65, GOLD, 34)
    return a, f, l


def basin_labels(recipe=True, p=True):
    g = VGroup(lab("basin A", AX, 0.15, TEXT), lab("basin B", BX, 0.15, TEXT))
    if recipe:
        g.add(lab("N + C", AX, -0.6, TEXT), lab("N + C + P" if p else "N + C", BX, -0.6, TEXT))
    return g


class S04226(Sc):
    def construct(self):
        w = lake226()
        self.add(w["wa"], w["wb"])
        self.play(Create(w["bnd"]), run_time=0.8)
        self.at("Lake 226")
        name = lab("Lake 226", -5.7, -1.0, YELLOW)
        self.play(FadeIn(name), run_time=0.6)
        self.at("divided by a barrier")
        self.play(Create(w["bar"]), run_time=1.4)
        self.at("two basins")
        bl = basin_labels(recipe=False)
        self.play(FadeIn(bl), run_time=0.8)
        self.at("Both basins received nitrogen")
        items, ls = nc_arrows()
        (a1, f1), (a2, f2), (a3, f3), (a4, f4) = items
        self.play(GrowArrow(a1), GrowArrow(a3), FadeIn(ls[0]), FadeIn(ls[2]), run_time=1.2)
        self.add(f1, f3)
        self.at("as nitrate")
        self.play(Indicate(ls[0], color=TEAL), Indicate(ls[2], color=TEAL), run_time=1.0)
        self.at("and carbon")
        self.play(GrowArrow(a2), GrowArrow(a4), FadeIn(ls[1]), FadeIn(ls[3]), run_time=1.2)
        self.add(f2, f4)
        self.at("sugar sucrose")
        self.play(Indicate(ls[1], color=YELLOW), Indicate(ls[3], color=YELLOW), run_time=1.0)
        self.finish()


def carried_226(trA=None, trB=None, with_p=False, recipe=True):
    """Rebuild the s04 picture exactly (same positions) and return the groups; flows are separate."""
    w = lake226(trB, trA)
    items, ls = nc_arrows()
    arrows = VGroup(*[a for a, f in items])
    flows = VGroup(*[f for a, f in items])
    name = lab("Lake 226", -5.7, -1.0, YELLOW)
    labs = VGroup(*ls)
    bl = basin_labels(recipe=recipe, p=with_p)
    if with_p:
        pa, pf, pl = p_arrow()
        arrows.add(pa)
        flows.add(pf)
        labs.add(pl)
    return w, arrows, flows, labs, bl, name


class S05P(Sc):
    def construct(self):
        w, arrows, flows, labs, bl, name = carried_226(recipe=False)
        self.add(w["wa"], w["wb"], w["bnd"], w["bar"], arrows, flows, labs, bl, name)
        self.at("One basin also received phosphorus")
        pa, pf, pl = p_arrow()
        self.play(GrowArrow(pa), FadeIn(pl), run_time=1.2)
        self.add(pf)
        self.play(FadeIn(lab("N + C + P", BX, -0.6, TEXT)), run_time=0.8)
        self.at("the other got none")
        self.play(FadeIn(lab("N + C", AX, -0.6, TEXT)), Indicate(bl[0], color=YELLOW), run_time=1.0)
        self.at("only difference")
        self.play(Indicate(pa, color=YELLOW, scale_factor=1.0), Indicate(pl, color=YELLOW), run_time=1.2)
        self.at("one element")
        ring = Circle(radius=0.6, stroke_color=YELLOW, stroke_width=6).move_to([5.5, -1.2, 0])
        self.play(Create(ring), run_time=0.8)
        self.play(Indicate(pa, color=GOLD, scale_factor=1.0), run_time=0.8)
        self.finish()


def question_card():
    a = T("Which half", 36, YELLOW)
    b = T("turns green?", 36, YELLOW)
    t = VGroup(a, b).arrange(DOWN, buff=0.12)
    box = RoundedRectangle(corner_radius=0.16, width=t.width + 0.5, height=t.height + 0.4, stroke_color=YELLOW,
                           stroke_width=3, fill_color=BG, fill_opacity=1)
    g = VGroup(box, t.move_to(box)).move_to([0, -1.6, 0])
    g.set_z_index(5)
    return g


def full_226(with_card=False, trA=None, trB=None):
    w, arrows, flows, labs, bl, name = carried_226(trA, trB, with_p=True)
    return w, VGroup(arrows, labs, bl, name), flows


class S06Predict(Sc):
    def construct(self):
        w, stat, flows = full_226()
        self.add(w["wa"], w["wb"], w["bnd"], w["bar"], stat, flows)
        self.at("plenty of nitrogen")
        arrows = stat[0]
        self.play(*[Indicate(arrows[i], color=TEAL, scale_factor=1.0) for i in (0, 2)], run_time=1.0)
        self.at("and carbon")
        self.play(*[Indicate(arrows[i], color=YELLOW, scale_factor=1.0) for i in (1, 3)], run_time=1.0)
        self.at("Only one had phosphorus")
        self.play(Indicate(arrows[4], color=GOLD, scale_factor=1.0), Indicate(stat[1][4], color=GOLD), run_time=1.2)
        self.at("Which half")
        self.play(FadeIn(question_card(), scale=0.85), run_time=0.8)
        self.finish()


class S07Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        w, stat, flows = full_226()
        self.add(w["wa"], w["wb"], w["bnd"], w["bar"], stat, flows, question_card())
        tr = ValueTracker(0)
        ring = Circle(radius=0.5, stroke_color=GREY, stroke_width=5).move_to([6.0, 1.5, 0])
        arc = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.001),
                                        stroke_color=YELLOW, stroke_width=8).move_to([6.0, 1.5, 0]))
        self.add(ring, arc)
        self.play(tr.animate.set_value(1), run_time=float(os.environ.get("KX_DURATION", "5")), rate_func=linear)


def blob_gauge():
    pass


class S08Reveal(Sc):
    def construct(self):
        trB = ValueTracker(0)
        w, stat, flows = full_226(trB=trB)
        alg = algae(0.4, 4.0, -2.5, 0.5, 22, trB, 5)
        self.add(w["wa"], w["wb"], w["bnd"], w["bar"], stat, flows, alg)
        self.at("Only the phosphorus basin")
        self.play(Indicate(stat[0][4], color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("It became highly eutrophic")
        self.play(trB.animate.set_value(1), run_time=2.2)
        self.at("rich in nutrients")
        he = node("highly eutrophic", GREEN, 30).move_to([BX, -1.7, 0])
        self.play(FadeIn(he, shift=UP * 0.1), run_time=0.8)
        self.at("dense with algae")
        self.play(Indicate(he, color=BEAD, scale_factor=1.05), run_time=1.0)
        cite = lab("Schindler, Science, 1974", -1.5, -3.6, GREY, 22)
        self.play(FadeIn(cite), run_time=0.6)
        self.at("The other basin stayed")
        self.play(Indicate(w["wa"], color=BLUE, scale_factor=1.02), run_time=1.2)
        self.finish()


def green_226():
    trB = ValueTracker(1)
    w, stat, flows = full_226(trB=trB)
    alg = algae(0.4, 4.0, -2.5, 0.5, 22, trB, 5)
    return w, stat, flows, alg


class S09Limit(Sc):
    def construct(self):
        w, stat, flows, alg = green_226()
        he = node("highly eutrophic", GREEN, 30).move_to([BX, -1.7, 0])
        self.add(w["wa"], w["wb"], w["bnd"], w["bar"], stat, flows, alg, he)
        self.at("nitrogen and carbon plentiful")
        arrows = stat[0]
        self.play(*[Indicate(arrows[i], color=YELLOW, scale_factor=1.0) for i in (0, 1, 2, 3)], run_time=1.4)
        self.at("phosphorus limited the algae")
        self.play(Indicate(arrows[4], color=GOLD, scale_factor=1.0), Indicate(stat[1][4], color=GOLD, scale_factor=1.4),
                  run_time=1.4)
        self.at("A nutrient is limiting")
        d1 = T("limiting nutrient:", 30, YELLOW)
        d2 = T("adding it alone raises production", 30, YELLOW)
        d = VGroup(d1, d2).arrange(DOWN, buff=0.15)
        dn = VGroup(RoundedRectangle(corner_radius=0.16, width=d.width + 0.5, height=d.height + 0.4,
                                     stroke_color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=1), d)
        d.move_to(dn[0])
        dn.move_to([0, -1.9, 0]).set_z_index(5)
        self.play(FadeOut(he), FadeIn(dn, shift=UP * 0.1), run_time=1.0)
        self.at("adding it on its own")
        self.play(Indicate(arrows[4], color=GOLD, scale_factor=1.0), run_time=1.0)
        self.at("raises production")
        self.play(Indicate(w["wb"], color=BEAD, scale_factor=1.02), run_time=1.2)
        self.finish()


# --- Lake 227 (top view, one lake) ------------------------------------------------------------------
NX, PX = -0.9, 2.6     # fertilizer arrow positions
FX = -4.4              # fixation arrow position (s11-s12)
TL_Y = -1.9            # timeline height


def lake227(tr, marker_x=-3.8):
    wat = water_rect(8.8, 3.4, 0, -1.0, tr, 0.8)
    alg = algae(-4.0, 4.0, -2.5, 0.4, 28, tr, 7)
    name = lab("Lake 227", -5.7, -1.0, YELLOW)
    return wat, alg, boundary(), name


def timeline(tx):
    line = Line([-3.8, TL_Y, 0], [3.8, TL_Y, 0], color=TEXT, stroke_width=5).set_z_index(2)
    tick = Line([0, TL_Y - 0.15, 0], [0, TL_Y + 0.15, 0], color=TEXT, stroke_width=5).set_z_index(2)
    l90 = lab("1990", 0, TL_Y - 0.5, TEXT, 28).set_z_index(2)
    mk = Dot([tx.get_value(), TL_Y, 0], radius=0.17, color=YELLOW).set_z_index(3)
    mk.add_updater(lambda m: m.move_to([tx.get_value(), TL_Y, 0]))
    return line, tick, l90, mk


class S10227(Sc):
    def construct(self):
        tr = ValueTracker(1)
        tx = ValueTracker(-3.8)
        wat, alg, wb, name = lake227(tr)
        self.add(wat, alg)
        self.play(Create(wb), run_time=0.8)
        self.at("Lake 227")
        self.play(FadeIn(name), run_time=0.6)
        self.at("with both nitrogen and phosphorus")
        na, nf = in_arrow([NX, 3.0, 0], [NX, 0.8, 0], [TEAL], 7, 3, 2.8)
        pa, pf = in_arrow([PX, 3.0, 0], [PX, 0.8, 0], [GOLD], 7, 3, 2.8)
        nl, pl = lab("N input", NX, 3.45, TEAL), lab("P input", PX, 3.45, GOLD)
        self.play(GrowArrow(na), FadeIn(nl), run_time=1.0)
        self.add(nf)
        self.play(GrowArrow(pa), FadeIn(pl), run_time=1.0)
        self.add(pf)
        self.at("for years")
        line, tick, l90, mk = timeline(tx)
        self.play(Create(line), FadeIn(mk), run_time=0.5)
        self.play(tx.animate.set_value(-0.3), run_time=1.2, rate_func=linear)
        self.at("Then the nitrogen fertilizer stopped")
        self.play(tx.animate.set_value(0), FadeIn(tick), FadeIn(l90), run_time=0.8)
        b1 = Line([-0.35, 2.35, 0], [0.35, 1.85, 0], color=YELLOW, stroke_width=8).shift(LEFT * 0.9 + UP * 0.0)
        b2 = Line([-0.35, 1.85, 0], [0.35, 2.35, 0], color=YELLOW, stroke_width=8).shift(LEFT * 0.9)
        b1.set_z_index(6)
        b2.set_z_index(6)
        self.play(Create(b1), Create(b2), run_time=0.5)
        self.play(Rotate(b1, 0.35), Rotate(b2, -0.35), run_time=0.4)
        self.play(na.animate.set_opacity(0.2), FadeOut(nf), FadeOut(b1), FadeOut(b2), nl.animate.set_opacity(0.4),
                  run_time=0.8)
        self.at("The phosphorus kept coming")
        self.play(Indicate(pa, color=GOLD, scale_factor=1.0), Indicate(pl, color=GOLD), run_time=1.2)
        self.finish()


def after_cut_227(tr, tx):
    wat, alg, wb, name = lake227(tr)
    na = arr([NX, 3.0, 0], [NX, 0.8, 0], BLUE, 7).set_opacity(0.2)
    nl = lab("N input", NX, 3.45, TEAL).set_opacity(0.4)
    pa, pf = in_arrow([PX, 3.0, 0], [PX, 0.8, 0], [GOLD], 7, 3, 2.8)
    pl = lab("P input", PX, 3.45, GOLD)
    line, tick, l90, mk = timeline(tx)
    return wat, alg, wb, name, na, nl, pa, pf, pl, line, tick, l90, mk


def strands(n, tr_op, seed=11):
    rng = random.Random(seed)
    g = VGroup()
    for i in range(n):
        s = VGroup(*[Dot(radius=0.12, color=BEAD) for _ in range(7)])
        for j, d in enumerate(s):
            d.move_to([j * 0.26 - 0.78, 0.1 * np.sin(j * 1.1 + i), 0])
        s.move_to([rng.uniform(-3.0, 3.0), rng.uniform(-2.5, 0.1), 0])
        s.v = rng.uniform(-0.25, 0.25)
        s.rot = rng.uniform(-0.2, 0.2)

        def u(m, dt, tr_op=tr_op):
            m.shift([m.v * dt, 0, 0])
            if abs(m.get_x()) > 3.1:
                m.v = -abs(m.v) * (1 if m.get_x() > 0 else -1)
            m.rotate(m.rot * dt)
            m.set_opacity(min(1.0, tr_op.get_value()))
        s.add_updater(u)
        g.add(s)
    g.set_z_index(0)
    return g


class S11Fixers(Sc):
    def construct(self):
        tr = ValueTracker(1)
        tx = ValueTracker(0)
        wat, alg, wb, name, na, nl, pa, pf, pl, line, tick, l90, mk = after_cut_227(tr, tx)
        self.add(wat, alg, wb, name, na, nl, pa, pf, pl, line, tick, l90, mk)
        self.at("With its nitrogen input cut")
        self.play(Indicate(nl, color=TEAL), run_time=1.2)
        self.at("you might expect the algae to fade")
        self.play(tr.animate.set_value(0.35), run_time=2.4)
        self.at("They did not")
        self.play(tr.animate.set_value(1), run_time=1.4)
        self.at("Cyanobacteria that fixed nitrogen")
        op = ValueTracker(0)
        st = strands(5, op)
        self.add(st)
        self.play(op.animate.set_value(1), run_time=1.6)
        cl = node("N-fixing cyanobacteria", BEAD, 28).move_to([0, -0.5, 0])
        self.play(FadeIn(cl, shift=UP * 0.1), run_time=0.8)
        self.at("took over")
        self.play(Indicate(st, color=BEAD, scale_factor=1.08), run_time=1.2)
        self.at("They fixed nitrogen from the air")
        fa = dotted(FX, 3.0, 0.8, TEAL, 6)
        fl = VGroup(lab("fixation", -2.95, 2.2, TEAL), lab("(an input)", -2.95, 1.7, TEAL))
        self.play(Create(fa), FadeIn(fl), FadeOut(cl), run_time=1.2)
        ff = flow([[FX, 2.9, 0], [FX, 0.9, 0]], 3, 3.0, TEAL)
        self.add(ff)
        self.at("an input that kept coming")
        fa2 = dotted(FX, 3.0, 0.8, TEAL, 14)
        self.play(Transform(fa, fa2), run_time=1.6)
        self.at("Its rate can still respond to phosphorus")
        self.play(Indicate(pa, color=GOLD, scale_factor=1.0), Indicate(fa, color=TEAL, scale_factor=1.0), run_time=1.6)
        self.at("and other conditions")
        self.play(Indicate(pa, color=GOLD, scale_factor=1.0), Indicate(fa, color=TEAL, scale_factor=1.0), run_time=1.4)
        self.finish()


class S12Stayed(Sc):
    def construct(self):
        tr = ValueTracker(1)
        tx = ValueTracker(0)
        wat, alg, wb, name, na, nl, pa, pf, pl, line, tick, l90, mk = after_cut_227(tr, tx)
        op = ValueTracker(1)
        st = strands(5, op)
        fa = dotted(FX, 3.0, 0.8, TEAL, 14)
        fl = VGroup(lab("fixation", -2.95, 2.2, TEAL), lab("(an input)", -2.95, 1.7, TEAL))
        ff = flow([[FX, 2.9, 0], [FX, 0.9, 0]], 3, 3.0, TEAL)
        self.add(wat, alg, wb, name, na, nl, pa, pf, pl, line, tick, l90, mk, st, fa, fl, ff)
        self.at("The lake stayed highly eutrophic")
        l05 = lab("2005", 3.8, TL_Y - 0.5, TEXT, 28)
        self.play(FadeIn(l05), tx.animate.set_value(3.8), run_time=3.8, rate_func=linear)
        self.at("Algae stayed as abundant")
        # gauges: both read the same clock, so algae follows phosphorus (schematic)
        clk = ValueTracker(0)
        clk.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))
        self.add(clk)
        lev = lambda: 0.62 + 0.10 * np.sin(1.3 * clk.get_value()) + 0.05 * np.sin(3.1 * clk.get_value())
        gx = (5.3, 6.2)
        boxes = VGroup(*[Rectangle(width=0.6, height=3.0, stroke_color=c, stroke_width=3).move_to([x, -1.0, 0])
                         for x, c in zip(gx, (GOLD, BEAD))])
        bars = VGroup(*[always_redraw(lambda x=x, c=c, k=k: Rectangle(
            width=0.6, height=max(0.05, 3.0 * lev() * k), stroke_width=0, fill_color=c, fill_opacity=0.9
        ).move_to([x, -2.5 + max(0.05, 3.0 * lev() * k) / 2, 0])) for x, c, k in zip(gx, (GOLD, BEAD), (1.0, 0.95))])
        gl = VGroup(lab("P", gx[0], 0.9, GOLD, 30), lab("algae", gx[1], 0.9, BEAD, 26))
        sch = lab(NOTE, 4.0, -3.6, GREY, 22)
        self.play(FadeIn(boxes), FadeIn(gl), FadeIn(sch), run_time=0.8)
        self.add(bars)
        self.at("as the phosphorus allowed")
        cite = lab("Schindler and colleagues, PNAS, 2008", -1.6, -3.6, GREY, 22)
        self.play(FadeIn(cite), Indicate(pa, color=GOLD, scale_factor=1.0), run_time=1.4)
        self.at("Fixation had made up")
        self.play(Indicate(fa, color=TEAL, scale_factor=1.0), Indicate(fl, color=TEAL), run_time=1.6)
        self.at("the missing nitrogen")
        self.play(Indicate(na, color=TEAL, scale_factor=1.0), Indicate(nl, color=TEAL), run_time=1.2)
        self.finish()


class S13Scope(Sc):
    def construct(self):
        tr = ValueTracker(1)
        wat = water_rect(8.8, 3.4, 0, -1.0, tr, 0.8)
        wb = boundary()
        al = algae(-4.0, 4.0, -2.5, 0.4, 28, tr, 7)
        self.add(wat, al, wb)
        self.at("These are small lakes")
        d227 = ellipse_lake(-3.7, -0.9, 0.7, 0.45, ALGAE)
        d226 = ellipse_lake(-4.7, -0.6, 0.7, 0.45, CLEAR)
        t226, t227 = lab("226", -4.7, -0.1, TEXT, 26), lab("227", -3.7, -1.5, TEXT, 26)
        self.play(FadeOut(wb), FadeOut(al), Transform(wat, d227), run_time=1.6)
        self.play(FadeIn(d226), FadeIn(t226), FadeIn(t227), run_time=0.8)
        self.at("one lake is not a replicate")
        self.play(Indicate(wat, color=YELLOW, scale_factor=1.3), run_time=1.0)
        tag = lab("two lakes, not all waters", 0, -3.4, YELLOW, 34)
        self.play(FadeIn(tag), run_time=0.8)
        self.at("Other lakes")
        pos = [(-1.5, 1.7), (1.2, 2.4), (3.6, 1.4), (-0.3, 0.1), (1.9, -0.4), (-2.0, -1.9), (0.7, -2.0)]
        others = VGroup(*[ellipse_lake(x, y, 1.3, 0.8, CLEAR) for x, y in pos])
        qs = VGroup(*[lab("?", x, y, YELLOW, 34) for x, y in pos])
        self.play(LaggedStart(*[FadeIn(o, scale=0.7) for o in others], lag_ratio=0.1), run_time=0.9)
        self.play(FadeIn(qs), run_time=0.3)
        self.at("many estuaries")
        est = Polygon([3.3, -1.0, 0], [5.8, -0.5, 0], [6.6, -1.5, 0], [5.4, -2.0, 0], [4.0, -1.9, 0],
                      stroke_color="#7FA7C4", stroke_width=3, fill_color="#2F6F7A", fill_opacity=0.9)
        el = lab("estuary", 5.0, -2.55, TEXT, 28)
        eq = lab("?", 5.0, -1.3, YELLOW, 34)
        self.play(FadeIn(est, scale=0.8), FadeIn(el), FadeIn(eq), run_time=1.2)
        self.at("can respond to nitrogen")
        nb = VGroup(blk(TEAL, 0.32).move_to([4.2, -0.4, 0]), blk(TEAL, 0.32).move_to([4.7, -0.1, 0]))
        self.play(FadeIn(nb), Indicate(est, color=TEAL, scale_factor=1.05), Indicate(others[2], color=TEAL, scale_factor=1.1),
                  run_time=1.6)
        self.at("co limited")
        everything = VGroup(wat, d226, t226, t227, tag, others, qs, est, el, eq, nb)
        self.play(FadeOut(everything), run_time=0.5)
        base = Line([-4.0, -2.2, 0], [4.0, -2.2, 0], color=TEXT, stroke_width=4)
        bx = [-2.7, -0.9, 0.9, 2.7]
        hs = [0.35, 0.45, 0.45, 3.6]
        cols = [GREY, TEAL, GOLD, BEAD]
        names = ["none", "N", "P", "N + P"]
        bars = [Rectangle(width=1.3, height=h, stroke_width=0, fill_color=c, fill_opacity=0.95)
                .move_to([x, -2.2 + h / 2, 0]) for x, h, c in zip(bx, hs, cols)]
        nms = VGroup(*[lab(n, x, -2.65, c if c != GREY else TEXT, 28) for n, x, c in zip(names, bx, cols)])
        yl = lab("algae", -4.9, 0.0, BEAD, 28)
        sch = lab(NOTE, 5.4, -3.6, GREY, 22)
        self.play(Create(base), FadeIn(nms), FadeIn(yl), FadeIn(sch), run_time=0.5)
        self.play(*[GrowFromEdge(b, DOWN) for b in bars[:3]], run_time=0.6)
        self.at("rising only when both")
        self.play(Indicate(nms[3], color=YELLOW), run_time=1.0)
        self.at("added together")
        self.play(GrowFromEdge(bars[3], DOWN), run_time=2.2)
        self.finish()


class S14Rule(Sc):
    def construct(self):
        tr = ValueTracker(1)
        wat, alg = side_water(tr), algae(-4.0, 4.0, -2.4, 0.4, 26, tr, 3)
        wb, sky = boundary(), sky_band()
        a1, f1, a2, f2, a3, f3, l1, l2, l3 = side_inputs()
        na = dotted(4.2, 3.0, 1.0, TEAL)
        ln = lab("N fixation", 2.9, 2.0, TEAL)
        nff = flow([[4.2, 2.9, 0], [4.2, 1.1, 0]], 3, 3.0, TEAL)
        pn, nn = two_nodes()
        self.add(wat, alg)
        self.play(Create(wb), FadeIn(sky), run_time=0.8)
        self.play(*[GrowArrow(a) for a in (a1, a2, a3)], FadeIn(l1), FadeIn(l2), FadeIn(l3), Create(na), FadeIn(ln),
                  run_time=1.2)
        self.add(f1, f2, f3, nff)
        self.at("phosphorus supply set")
        self.play(FadeIn(pn, shift=UP * 0.1), run_time=0.8)
        self.at("how much algae")
        self.play(Indicate(pn, color=GOLD, scale_factor=1.05), run_time=1.2)
        self.at("Fixers can make up missing nitrogen")
        self.play(FadeIn(nn, shift=UP * 0.1), Indicate(na, color=TEAL, scale_factor=1.0), Indicate(ln, color=TEAL),
                  run_time=1.4)
        self.at("No microbe can fix phosphorus")
        pa = dotted(-4.2, 3.0, 1.0, GOLD)
        xm = xmark(-4.2, 2.0)
        lp = lab("P: no major gas", -1.9, 2.0, GOLD)
        self.play(Create(pa), FadeIn(xm, scale=0.6), FadeIn(lp), run_time=1.4)
        self.play(Indicate(pn, color=GOLD, scale_factor=1.05), run_time=1.2)
        self.finish()


class S15End(EndCard):
    LINE = "Fixers can make up missing nitrogen; no microbe can fix phosphorus."
