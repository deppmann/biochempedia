"""Nutrient cycling: The Loop Inside the Line (Biochemistrypedia explainer)

COLOUR MAP (same in the lesson and both films)
  GOLD dashed line = the boundary     BLUE arrows = inputs crossing in
  RED arrows = outputs crossing out   GREY ring of arrows = the internal loop
  TEAL blocks = nitrogen              GREEN = trees
"""
import os
import numpy as np
from bp_style import *  # noqa: F401,F403

MINUS = "−"
SOIL_P = np.array([-2.6, -0.5, 0.0])
AMM_P = np.array([2.6, -0.5, 0.0])
TRE_P = np.array([2.6, 1.6, 0.0])
LEA_P = np.array([-2.6, 1.6, 0.0])
CTR = np.array([5.5, 3.05, 0.0])
NOTE = "illustrative numbers · kg N per hectare per year"


class Sc(SpokenScene):
    """SpokenScene plus a faint field of drifting teal motes, so a held frame is never dead."""
    def setup(self):
        super().setup()
        import random
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


def flow(pts, n=3, period=4.0, color=TEAL):
    """Teal blocks that keep sliding along a polyline: motion that never needs a cue."""
    path = VMobject().set_points_as_corners([np.array(p, dtype=float) for p in pts])
    g = VGroup()
    for i in range(n):
        b = blk(color)
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


def ground():
    return Rectangle(width=9.4, height=0.4, stroke_width=0, fill_color=GREY, fill_opacity=0.25).move_to([0, -3.1, 0])


class Counter:
    def __init__(self, v0=0):
        self.tr = ValueTracker(v0)
        self.box = RoundedRectangle(corner_radius=0.15, width=2.5, height=1.25, stroke_color=GOLD, stroke_width=3,
                                    fill_color=BG, fill_opacity=1).move_to(CTR)
        self.unit = T("kg N / hectare", 22, GREY).move_to(CTR + DOWN * 0.38)
        tr = self.tr

        def fmt(v):
            r = int(round(v))
            return "0" if r == 0 else f"{r:+d}"
        self.val = always_redraw(lambda: M(fmt(tr.get_value()), 38, GOLD).move_to(CTR + UP * 0.17))
        self.static = VGroup(self.box, self.unit)

    def set(self, v, t=0.8):
        return self.tr.animate.set_value(v).set_run_time(t)


# --- shared pieces ----------------------------------------------------------------------------
def in_arrows():
    a1 = arr([-3.6, 3.7, 0], [-3.6, 2.1, 0], BLUE, 7)
    a2 = arr([-0.4, 3.7, 0], [-0.4, 2.1, 0], BLUE, 7)
    l1 = T("8 deposition", 28, BLUE).move_to([-2.05, 3.3, 0])
    l2 = T("6 fixation", 28, BLUE).move_to([0.8, 3.3, 0])
    return a1, a2, l1, l2


def in_flows():
    return VGroup(flow([[-3.6, 3.6, 0], [-3.6, 2.2, 0]], 3, 3.0), flow([[-0.4, 3.6, 0], [-0.4, 2.2, 0]], 3, 3.0))


def out_arrows():
    s = arr([3.4, 0.55, 0], [6.4, 0.55, 0], RED, 7)
    g = arr([3.9, 1.9, 0], [3.9, 3.5, 0], RED, 7)
    ls = T("3 stream", 28, RED).move_to([5.8, 1.1, 0])
    lg = T("2 gas", 28, RED).move_to([2.95, 3.2, 0])
    return s, g, ls, lg


def out_flows():
    return VGroup(flow([[3.5, 0.55, 0], [6.3, 0.55, 0]], 3, 3.0, TEAL), flow([[3.9, 2.0, 0], [3.9, 3.4, 0]], 2, 3.0))


def ring_arrows(w=6, tip=0.25):
    return VGroup(arr([-1.1, -0.5, 0], [1.3, -0.5, 0], GREY, w, tip),    # soil -> ammonium
                  arr([2.6, 0.0, 0], [2.6, 1.1, 0], GREY, w, tip),        # ammonium -> trees
                  arr([1.85, 1.6, 0], [-1.1, 1.6, 0], GREY, w, tip),      # trees -> leaves
                  arr([-2.6, 1.1, 0], [-2.6, 0.0, 0], GREY, w, tip))      # leaves -> soil


RING_SEG = [([-1.0, -0.5, 0], [1.2, -0.5, 0]), ([2.6, 0.05, 0], [2.6, 1.05, 0]),
            ([1.8, 1.6, 0], [-1.0, 1.6, 0]), ([-2.6, 1.05, 0], [-2.6, 0.05, 0])]


def seg_flow(i, n=2, period=2.6):
    a, b = RING_SEG[i]
    return flow([a, b], n, period)


def tree(x, base, h=0.9, w=0.7, color=GREEN, trunk=0.3):
    t = Rectangle(width=0.14, height=trunk, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([x, base + trunk / 2, 0])
    c = Polygon([x - w / 2, base + trunk, 0], [x + w / 2, base + trunk, 0], [x, base + trunk + h, 0], stroke_width=0,
                fill_color=color, fill_opacity=0.85)
    return VGroup(t, c)


def log(x, y=-2.78, w=0.9):
    return Rectangle(width=w, height=0.24, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([x, y, 0])


STAND_X = [-4.0 + 1.33 * i for i in range(7)]
PILE = [(0.3 * (i % 4 - 1.5), 0.0 + 0.3 * (i // 4)) for i in range(8)]
PILE_JIT = [(-0.35, 0.1), (0.2, -0.05), (-0.1, 0.3), (0.45, 0.0), (-0.5, -0.1), (0.1, 0.35), (0.55, 0.2), (-0.3, 0.25)]


# --- cartoon valley of scenes 1 and 2 -----------------------------------------------------------
def cartoon():
    gr = Rectangle(width=13.2, height=0.4, stroke_width=0, fill_color=GREY, fill_opacity=0.25).move_to([0, -2.7, 0])
    trees = VGroup(*[tree(x, -2.5, h=3.0, w=1.8, trunk=0.5) for x in (-5.4, -3.4, -1.4)])
    stumps = VGroup(*[Rectangle(width=1.0, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([x, -2.25, 0]) for x in (1.0, 3.2, 5.4)])
    logs = VGroup(*[Rectangle(width=1.2, height=0.3, stroke_width=0, fill_color="#B08A5A", fill_opacity=0.95).move_to([x, -2.35, 0]) for x in (2.1, 4.3)])
    xs = np.linspace(0.2, 6.6, 40)
    spts = [[x, -3.4 + 0.12 * np.sin(2.5 * x), 0] for x in xs]
    stream = VMobject(stroke_color=RED, stroke_width=12).set_points_as_corners([np.array(p) for p in spts])
    return gr, trees, stumps, logs, stream, spts


# =================================================================================================
class S00Title(TitleCard):
    LESSON = "Nutrient Cycling"
    TITLE = "The Loop Inside the Line"


class S01Question(Sc):
    def construct(self):
        gr, trees, stumps, logs, stream, spts = cartoon()
        self.play(FadeIn(gr), LaggedStart(*[GrowFromPoint(t, t.get_bottom()) for t in trees], lag_ratio=0.2),
                  FadeIn(stumps), FadeIn(logs), Create(stream), run_time=1.6)
        fl = flow(spts, 3, 6.0)
        self.add(fl)
        lf = T("forest", 28).move_to([-3.4, 1.7, 0])
        self.add(lf)
        self.at("come from")
        q = T("?", 140, YELLOW, weight=BOLD).move_to([3.4, 1.2, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.at("cut a forest")
        lc = T("cut, regrowth suppressed", 28).move_to([3.4, -0.4, 0])
        self.play(FadeIn(lc, shift=UP * 0.1), Indicate(stumps, color=YELLOW), run_time=1.2)
        self.at("far more nitrogen")
        more = flow(spts, 8, 4.0)
        nl = T("nitrogen", 28, TEAL).move_to([5.3, -1.6, 0])
        self.play(stream.animate.set_stroke(width=22), FadeIn(more), FadeIn(nl), run_time=1.2)
        self.finish()


class S02Boundary(Sc):
    def construct(self):
        gr, trees, stumps, logs, stream, spts = cartoon()
        fl = flow(spts, 8, 4.0)
        self.add(gr, trees, stumps, logs, stream, fl)
        self.at("logs stayed")
        self.play(logs.animate.shift(UP * 0.35).set_run_time(0.7).set_rate_func(there_and_back), run_time=1.4)
        self.at("find the source")
        wg, wb = ground(), boundary()
        self.play(FadeOut(VGroup(gr, trees, stumps, logs, stream, fl)), FadeIn(wg), run_time=1.2)
        self.at("keep accounts")
        c = Counter(0)
        self.play(FadeIn(c.static), run_time=0.8)
        self.add(c.val)
        self.at("a bank")
        self.play(pulse(c.box, 1.15), run_time=1.0)
        self.at("draw a line")
        self.play(Create(wb), run_time=2.0)
        lb = T("boundary", 28, GOLD).move_to([0, 0.55, 0])
        self.play(FadeIn(lb), run_time=0.5)
        self.finish()


class S03PoolFlux(Sc):
    def construct(self):
        wg, wb = ground(), boundary()
        c = Counter(0)
        self.add(wg, wb, c.static, c.val)
        soil = node("soil organic N", TEAL).move_to(SOIL_P)
        amm = node("ammonium, nitrate", TEAL, 26).move_to(AMM_P)
        tre = node("trees", GREEN).move_to(TRE_P)
        self.play(Indicate(wb, color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("pools")
        self.play(FadeIn(soil, shift=UP * 0.15), FadeIn(amm, shift=UP * 0.15), run_time=1.0)
        self.play(pulse(soil), pulse(amm), run_time=1.0)
        self.at("the trees")
        self.play(FadeIn(tre, shift=UP * 0.15), pulse(tre), run_time=1.0)
        self.at("pool is like a bank")
        cap1 = T("pool = amount (kg per hectare)", 28, TEAL).move_to([0, -1.7, 0])
        self.play(FadeIn(cap1), pulse(soil), pulse(amm), Indicate(tre, color=GREEN), run_time=1.5)
        self.at("a flux")
        cap2 = T("flux = kg per hectare per year", 28, YELLOW).move_to([0, -1.7, 0])
        a = arr([2.6, 0.0, 0], [2.6, 1.1, 0], YELLOW, 8)
        self.play(ReplacementTransform(cap1, cap2), GrowArrow(a), run_time=1.0)
        fl = flow([[2.6, 0.05, 0], [2.6, 1.05, 0]], 2, 2.0)
        self.add(fl)
        self.play(Indicate(a, color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.at("withdrawal")
        self.play(Indicate(a, color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.finish()


def pools():
    return (node("soil organic N", TEAL).move_to(SOIL_P), node("ammonium, nitrate", TEAL, 26).move_to(AMM_P),
            node("trees", GREEN).move_to(TRE_P))


class S04Inputs(Sc):
    def construct(self):
        wg, wb = ground(), boundary()
        c = Counter(0)
        soil, amm, tre = pools()
        self.add(wg, wb, c.static, c.val, soil, amm, tre)
        tag = T(NOTE, 22, GREY).move_to([-2.2, -3.62, 0])
        self.add(tag)
        self.play(wb.animate.set_stroke(width=9), run_time=0.8)
        self.play(wb.animate.set_stroke(width=5), run_time=0.8)
        self.at("from the air")
        a1, a2, l1, l2 = in_arrows()
        self.play(GrowArrow(a1), run_time=1.2)
        f1 = flow([[-3.6, 3.6, 0], [-3.6, 2.2, 0]], 3, 3.0)
        self.add(f1)
        self.at("deposit 8")
        self.play(FadeIn(l1, shift=RIGHT * 0.1), run_time=0.8)
        self.at("microbes fix")
        self.play(GrowArrow(a2), run_time=1.0)
        f2 = flow([[-0.4, 3.6, 0], [-0.4, 2.2, 0]], 3, 3.0)
        self.add(f2)
        self.at("six more")
        self.play(FadeIn(l2, shift=RIGHT * 0.1), run_time=0.8)
        self.finish()


class S05Outputs(Sc):
    def construct(self):
        wg, wb = ground(), boundary()
        c = Counter(0)
        soil, amm, tre = pools()
        a1, a2, l1, l2 = in_arrows()
        tag = T(NOTE, 22, GREY).move_to([-2.2, -3.62, 0])
        self.add(wg, wb, c.static, c.val, soil, amm, tre, a1, a2, l1, l2, tag, in_flows())
        self.play(Indicate(wb, color=GOLD, scale_factor=1.0), run_time=1.2)
        s, g, ls, lg = out_arrows()
        self.at("the stream carries three")
        self.play(GrowArrow(s), run_time=1.0)
        self.add(flow([[3.5, 0.55, 0], [6.3, 0.55, 0]], 3, 3.0))
        self.play(FadeIn(ls), run_time=0.6)
        self.at("microbes release two")
        self.play(GrowArrow(g), run_time=1.0)
        self.add(flow([[3.9, 2.0, 0], [3.9, 3.4, 0]], 2, 3.0))
        self.play(FadeIn(lg), run_time=0.6)
        self.finish()


class S06Rule(Sc):
    def construct(self):
        wg, wb = ground(), boundary()
        c = Counter(0)
        soil, amm, tre = pools()
        a1, a2, l1, l2 = in_arrows()
        s, g, ls, lg = out_arrows()
        tag = T(NOTE, 22, GREY).move_to([-2.2, -3.62, 0])
        self.add(wg, wb, c.static, c.val, soil, amm, tre, a1, a2, l1, l2, s, g, ls, lg, tag, in_flows(), out_flows())
        self.play(Indicate(VGroup(a1, a2), color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.play(Indicate(VGroup(s, g), color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.at("change in stock")
        e1 = T("change in stock", 30)
        e2 = T("=", 30)
        e3 = T("inputs", 30, BLUE)
        e4 = T(MINUS, 30)
        e5 = T("outputs", 30, RED)
        eq = VGroup(e1, e2, e3, e4, e5).arrange(RIGHT, buff=0.25).move_to([0, -1.7, 0])
        self.play(FadeIn(e1), run_time=0.4)
        self.at("inputs")
        self.play(FadeIn(e2), FadeIn(e3), run_time=0.3)
        self.at("minus")
        self.play(FadeIn(e4), run_time=0.2)
        self.at("outputs")
        self.play(FadeIn(e5), run_time=0.3)
        self.at("this forest gains")
        n1 = T("14", 34, BLUE)
        n2 = T(MINUS, 34)
        n3 = T("5", 34, RED)
        n4 = T("=", 34)
        n5 = T("+9", 34, GOLD)
        n6 = T("per year", 30, GREY)
        sm = VGroup(n1, n2, n3, n4, n5, n6).arrange(RIGHT, buff=0.25).move_to([0, -2.5, 0])
        self.play(LaggedStart(*[FadeIn(x) for x in sm[:5]], lag_ratio=0.3), run_time=1.2)
        self.at("each year")
        self.play(FadeIn(n6), c.set(9, 0.8), run_time=0.8)
        self.at("the line and the year")
        self.play(wb.animate.set_stroke(width=9), run_time=0.4)
        self.play(wb.animate.set_stroke(width=5), run_time=0.4)
        self.at("and the year")
        self.play(Indicate(n6, color=YELLOW), run_time=0.6)
        self.at("must be stated")
        self.play(c.set(18, 0.8))
        self.at("before any adding")
        self.play(c.set(27, 0.8))
        self.finish()


def ring_nodes(amm_label="ammonium"):
    return (node("soil organic N", TEAL).move_to(SOIL_P), node(amm_label, TEAL).move_to(AMM_P),
            node("trees", GREEN).move_to(TRE_P), node("falling leaves", GREEN).move_to(LEA_P))


class S07Loop(Sc):
    def construct(self):
        wg, wb = ground(), boundary()
        c = Counter(27)
        soil, amm, tre = pools()
        a1, a2, l1, l2 = in_arrows()
        s, g, ls, lg = out_arrows()
        outs = VGroup(a1, a2, l1, l2, s, g, ls, lg, in_flows(), out_flows())
        self.add(wg, wb, c.static, c.val, soil, amm, tre, outs)
        self.at("never crosses the line")
        amm2 = node("ammonium", TEAL).move_to(AMM_P)
        self.play(FadeOut(outs), ReplacementTransform(amm, amm2), run_time=1.5)
        ring = ring_arrows()
        lea = node("falling leaves", GREEN).move_to(LEA_P)
        self.at("decomposers release")
        dec = T("decomposers", 28, GREY).move_to([0.1, -1.1, 0])
        self.play(GrowArrow(ring[0]), FadeIn(dec), run_time=1.0)
        self.add(seg_flow(0))
        self.at("dead leaves")
        self.play(FadeIn(lea, shift=DOWN * 0.15), pulse(lea), run_time=1.0)
        self.at("trees take it up")
        self.play(GrowArrow(ring[1]), run_time=0.8)
        self.add(seg_flow(1))
        self.at("grow leaves")
        self.play(GrowArrow(ring[2]), run_time=0.8)
        self.add(seg_flow(2))
        self.at("drop them again")
        self.play(GrowArrow(ring[3]), run_time=0.8)
        self.add(seg_flow(3))
        self.finish()


def ring_world(counter_v, amm_label="ammonium"):
    wg, wb = ground(), boundary()
    c = Counter(counter_v)
    soil, amm, tre, lea = ring_nodes(amm_label)
    return wg, wb, c, soil, amm, tre, lea


class S08Size(Sc):
    def construct(self):
        wg, wb, c, soil, amm, tre, lea = ring_world(27)
        ring = ring_arrows()
        self.add(wg, wb, c.static, c.val, soil, amm, tre, lea, ring, *[seg_flow(i) for i in range(4)])
        self.at("that loop moves about")
        ring2 = ring_arrows(16, 0.5)
        self.play(Transform(ring, ring2), run_time=1.5)
        self.at("90")
        n = M("90", 52, TEXT).move_to([0.1, 0.95, 0])
        u = T("kg N / hectare / year", 24, GREY).move_to([0.1, 0.25, 0])
        self.play(FadeIn(n, scale=0.8), FadeIn(u), run_time=1.0)
        self.at("biggest flux")
        b90 = Rectangle(width=0.8, height=0.01, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([6.35, -3.2, 0], aligned_edge=DOWN)
        b90 = Rectangle(width=0.8, height=4.2, stroke_width=0, fill_color=GREY, fill_opacity=1).move_to([6.35, -3.2 + 2.1, 0])
        t90 = M("90", 30).move_to([6.35, 1.25, 0])
        nm90 = T("loop", 24, GREY).move_to([6.35, -3.55, 0])
        self.play(GrowFromEdge(b90, DOWN), FadeIn(t90), FadeIn(nm90), run_time=1.5)
        self.at("far bigger")
        self.play(Indicate(b90, color=YELLOW, scale_factor=1.0), run_time=1.0)
        self.at("inputs together")
        ia = arr([-2.0, 3.7, 0], [-2.0, 2.1, 0], BLUE, 6)
        il = M("14", 30, BLUE).move_to([-1.2, 3.2, 0])
        b14 = Rectangle(width=0.8, height=0.65, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to([5.2, -3.2 + 0.325, 0])
        t14 = M("14", 30, BLUE).move_to([5.2, -2.35, 0])
        nm14 = T("inputs", 24, BLUE).move_to([5.2, -3.55, 0])
        self.play(GrowArrow(ia), FadeIn(il), GrowFromEdge(b14, DOWN), FadeIn(t14), FadeIn(nm14), run_time=1.5)
        self.add(flow([[-2.0, 3.6, 0], [-2.0, 2.2, 0]], 2, 3.0))
        self.finish()


class S09Cancel(Sc):
    def construct(self):
        wg, wb, c, soil, amm, tre, lea = ring_world(27)
        ring = ring_arrows(16, 0.5)
        n = M("90", 52, TEXT).move_to([0.1, 0.95, 0])
        u = T("kg N / hectare / year", 24, GREY).move_to([0.1, 0.25, 0])
        self.add(wg, wb, c.static, c.val, soil, amm, tre, lea, ring, n, u, *[seg_flow(i) for i in range(4)])
        self.at("the counter never")
        self.play(pulse(c.box, 1.15), c.set(36, 0.8), run_time=1.2)
        self.at("nitrogen leaving one pool")
        a = M(MINUS + "90", 34, RED).move_to([-2.6, -1.6, 0])
        self.play(FadeIn(a, shift=DOWN * 0.1), pulse(soil), run_time=1.0)
        self.at("enters another pool")
        b = M("+90", 34, BLUE).move_to([2.6, -1.6, 0])
        self.play(FadeIn(b, shift=DOWN * 0.1), pulse(amm), run_time=1.0)
        self.at("those transfers cancel")
        fin = VGroup(M(MINUS + "90", 34, RED), M("+", 34), M("90", 34, BLUE), M("=", 34), M("0", 38, GOLD)).arrange(RIGHT, buff=0.3).move_to([0, -1.9, 0])
        self.play(ReplacementTransform(VGroup(a, b), fin), run_time=1.5)
        self.at("is bookkeeping")
        self.play(Indicate(fin, color=YELLOW), run_time=1.2)
        self.at("does not mean the loop is small")
        self.play(Indicate(ring, color=YELLOW, scale_factor=1.0), Indicate(n, color=YELLOW), c.set(45, 0.8), run_time=1.5)
        self.finish()


def felled():
    return VGroup(*[log(x) for x in STAND_X])


class S10Predict(Sc):
    def construct(self):
        wg, wb, c, soil, amm, tre, lea = ring_world(45)
        ring = ring_arrows(16, 0.5)
        n = M("90", 52, TEXT).move_to([0.1, 0.95, 0])
        u = T("kg N / hectare / year", 24, GREY).move_to([0.1, 0.25, 0])
        fls = [seg_flow(i) for i in range(4)]
        self.add(wg, wb, c.static, c.val, soil, amm, tre, lea, ring, n, u, *fls)
        trees = VGroup(*[tree(x, -2.9) for x in STAND_X])
        self.play(FadeIn(trees), run_time=0.5)
        self.at("cut the trees")
        lg = felled()
        self.play(ReplacementTransform(trees, lg), run_time=1.2)
        lab = T("trees left on site", 28, GREY).move_to([0, -2.2, 0])
        self.play(FadeIn(lab), run_time=0.5)
        self.at("keep new plants")
        for _ in range(2):
            self.play(ring[1].animate.set_opacity(0.15), tre.animate.set_opacity(0.4), fls[1].animate.set_opacity(0.1), run_time=0.2)
            self.play(ring[1].animate.set_opacity(1), tre.animate.set_opacity(1), fls[1].animate.set_opacity(1), run_time=0.2)
        self.play(ring[1].animate.set_opacity(0.15), tre.animate.set_opacity(0.4), FadeOut(fls[1]), FadeOut(fls[2]),
                  ring[2].animate.set_opacity(0.15), run_time=0.6)
        self.at("does the loop simply stop")
        q = VGroup(T("stop, or", 38, YELLOW), T("go somewhere?", 38, YELLOW)).arrange(DOWN, buff=0.12).move_to([0.1, 0.55, 0])
        self.play(FadeOut(n), FadeOut(u), FadeIn(q), run_time=0.8)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        wg, wb, c, soil, amm, tre, lea = ring_world(45)
        ring = ring_arrows(16, 0.5)
        ring[1].set_opacity(0.15)
        ring[2].set_opacity(0.15)
        tre.set_opacity(0.4)
        lg = felled()
        lab = T("trees left on site", 28, GREY).move_to([0, -2.2, 0])
        q = VGroup(T("stop, or", 38, YELLOW), T("go somewhere?", 38, YELLOW)).arrange(DOWN, buff=0.12).move_to([0.1, 0.55, 0])
        bg = Circle(radius=0.5, stroke_color=GREY, stroke_width=3).move_to([5.7, 0.4, 0])
        arc = Circle(radius=0.5, stroke_color=YELLOW, stroke_width=8).move_to([5.7, 0.4, 0])
        self.add(wg, wb, c.static, c.val, soil, amm, tre, lea, ring, lg, lab, q, bg, seg_flow(0), seg_flow(3))
        self.play(Create(arc), run_time=5.0, rate_func=linear)
        self.finish()


class S12Reveal(Sc):
    def construct(self):
        wg, wb, c, soil, amm, tre, lea = ring_world(45)
        ring = ring_arrows(16, 0.5)
        ring[2].set_opacity(0.15)
        tre.set_opacity(0.4)
        lg = felled()
        self.add(wg, wb, c.static, c.val, soil, amm, tre, lea, ring, lg, seg_flow(0), seg_flow(3))
        self.at("goes somewhere")
        self.play(Indicate(ring[0], color=YELLOW, scale_factor=1.0), run_time=1.2)
        self.at("decomposers keep releasing")
        self.play(FadeOut(ring[1]), run_time=0.4)
        pile = VGroup()
        for i, (dx, dy) in enumerate(PILE):
            b = blk(TEAL, 0.24).move_to(AMM_P + np.array([dx, 0.55 + dy, 0]))
            pile.add(b)
            self.play(FadeIn(b, shift=LEFT * 0.4), run_time=0.35)
            self.wait(0.2)
        self.at("microbes turn the extra")
        self.play(Indicate(pile, color=YELLOW), run_time=1.2)
        self.at("into nitrate")
        nit = node("nitrate", TEAL).move_to(AMM_P)
        self.play(ReplacementTransform(amm, nit), run_time=1.0)
        self.at("soil holds weakly")
        parts = VGroup(*[Circle(radius=0.22, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([2.6 + dx, -1.5, 0]) for dx in (-0.8, 0, 0.8)])
        self.play(FadeIn(parts), run_time=0.6)
        self.play(*[b.animate.shift(np.array([PILE_JIT[i][0], PILE_JIT[i][1] - 0.2, 0])) for i, b in enumerate(pile)], run_time=1.5)
        self.finish()


def pile_static():
    g = VGroup()
    for i, (dx, dy) in enumerate(PILE):
        g.add(blk(TEAL, 0.24).move_to(AMM_P + np.array([dx + PILE_JIT[i][0], 0.55 + dy + PILE_JIT[i][1] - 0.2, 0])))
    return g


class S13Leak(Sc):
    def construct(self):
        wg, wb, c, soil, amm, tre, lea = ring_world(45, "nitrate")
        ring = ring_arrows(16, 0.5)
        ring[1].set_opacity(0)
        ring[2].set_opacity(0.15)
        tre.set_opacity(0.4)
        lg = felled()
        pile = pile_static()
        self.add(wg, wb, c.static, c.val, soil, amm, tre, lea, ring, lg, pile, seg_flow(0), seg_flow(3))
        self.at("breaks open")
        self.play(Indicate(pile, color=YELLOW), run_time=1.0)
        self.at("spills across the line")
        red = arr([3.4, -1.0, 0], [6.4, -2.6, 0], RED, 26, 0.6)
        self.play(GrowArrow(red), run_time=1.5)
        self.at("nitrate pours out")
        lab = T("stream nitrate", 28, RED).move_to([5.1, -3.55, 0])
        fl = flow([[3.5, -1.0, 0], [6.3, -2.55, 0]], 9, 2.5)
        self.play(FadeOut(pile), FadeIn(fl), FadeIn(lab), run_time=1.0)
        self.at("the counter turns negative")
        sch = T("schematic", 22, GREY).move_to([5.5, 2.0, 0])
        self.play(c.set(-40, 1.8), FadeIn(sch), run_time=1.8)
        self.finish()


def stream_valley(x, thick, flows_n, color=RED):
    pass


class S14Hubbard(Sc):
    def construct(self):
        def vb(cx):
            r = RoundedRectangle(corner_radius=0.3, width=5.4, height=3.6, stroke_color=GOLD, stroke_width=5).move_to([cx, 0.3, 0])
            return DashedVMobject(r, num_dashes=50, dashed_ratio=0.55)
        vl, vr = vb(-3.4), vb(3.4)
        stumps = VGroup(*[Rectangle(width=0.6, height=0.35, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([-3.4 + dx, -1.2, 0]) for dx in (-1.8, -0.6, 0.6, 1.8)])
        trs = VGroup(*[tree(3.4 + dx, -1.45, h=1.3, w=0.9, trunk=0.35) for dx in (-1.8, -0.6, 0.6, 1.8)])
        ll = T("cut, regrowth suppressed", 28).move_to([-3.4, 2.55, 0])
        lr = T("uncut reference", 28).move_to([3.4, 2.55, 0])
        self.play(Create(vl), Create(vr), run_time=1.5)
        self.play(FadeIn(stumps), FadeIn(trs), FadeIn(ll), FadeIn(lr), run_time=1.0)
        self.at("hubbard")
        pin = VGroup(Circle(radius=0.16, stroke_width=0, fill_color=RED, fill_opacity=1),
                     Triangle(stroke_width=0, fill_color=RED, fill_opacity=1).scale(0.14).rotate(PI).shift(DOWN * 0.2)).move_to([-3.0, 3.3, 0])
        pt = T("Hubbard Brook, New Hampshire", 28, GOLD).move_to([0.3, 3.3, 0])
        self.play(FadeIn(pin, shift=DOWN * 0.2), FadeIn(pt), run_time=1.0)
        self.at("the stream from their cut watershed")
        cut = arr([-3.4, -1.5, 0], [-3.4, -3.4, 0], RED, 8, 0.4)
        self.play(GrowArrow(cut), run_time=0.9)
        self.add(flow([[-3.4, -1.55, 0], [-3.4, -3.3, 0]], 3, 3.0))
        self.at("far more nitrate")
        cut2 = arr([-3.4, -1.5, 0], [-3.4, -3.4, 0], RED, 26, 0.6)
        self.play(Transform(cut, cut2), run_time=1.0)
        self.add(flow([[-3.4, -1.55, 0], [-3.4, -3.3, 0]], 7, 2.5))
        nl = T("nitrate", 28, RED).move_to([-1.75, -2.3, 0])
        self.play(FadeIn(nl), run_time=0.5)
        self.at("and calcium")
        cl = T("calcium", 28, RED).move_to([-1.75, -2.95, 0])
        self.play(FadeIn(cl), run_time=0.5)
        self.at("than the uncut one")
        un = arr([3.4, -1.5, 0], [3.4, -3.4, 0], RED, 5, 0.3)
        self.play(GrowArrow(un), run_time=0.8)
        self.add(flow([[3.4, -1.55, 0], [3.4, -3.3, 0]], 1, 3.0))
        sc = T("schematic; direction, not size", 24, GREY).move_to([0, -3.62, 0])
        self.play(FadeIn(sc), run_time=0.5)
        self.finish()


class S15Meaning(Sc):
    def construct(self):
        wg, wb, c, soil, amm, tre, lea = ring_world(-40, "nitrate")
        ring = ring_arrows(10, 0.4)
        ring[1].set_opacity(0.15)
        ring[2].set_opacity(0.15)
        tre.set_opacity(0.4)
        lg = felled()
        self.add(wg, wb, c.static, c.val, soil, amm, tre, lea, ring, lg, seg_flow(0), seg_flow(3))
        ba = arr([-3.6, 3.7, 0], [-3.6, 2.1, 0], BLUE, 7)
        bl = T("rain input", 28, BLUE).move_to([-2.2, 3.3, 0])
        self.play(GrowArrow(ba), FadeIn(bl), run_time=0.8)
        self.add(flow([[-3.6, 3.6, 0], [-3.6, 2.2, 0]], 3, 3.0))
        self.at("no more nitrogen")
        p1 = T("rain input unchanged", 28, BLUE)
        p2 = T("; the loop leaked out", 28, RED)
        line = VGroup(p1, p2).arrange(RIGHT, buff=0.05).move_to([0, -3.62, 0])
        self.play(Indicate(ba, color=YELLOW, scale_factor=1.0), FadeIn(p1), run_time=1.0)
        self.at("recycled nitrogen was leaving")
        red = arr([3.4, -1.0, 0], [6.4, -2.6, 0], RED, 26, 0.6)
        self.play(GrowArrow(red), FadeIn(p2), run_time=1.2)
        self.add(flow([[3.5, -1.0, 0], [6.3, -2.55, 0]], 8, 2.5))
        self.at("a store changes only across")
        self.play(wb.animate.set_stroke(width=10), run_time=0.8)
        self.play(wb.animate.set_stroke(width=5), run_time=0.8)
        self.at("the broken loop crossed it")
        ring_c = Circle(radius=0.55, stroke_color=YELLOW, stroke_width=6).move_to([4.7, -1.8, 0])
        self.play(Create(ring_c), run_time=0.8)
        self.play(Indicate(red, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.finish()


class S16End(EndCard):
    LINE = "Stores change only across the boundary; a broken loop can cross it."
