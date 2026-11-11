"""Order the Relay, Find the Brake  (itch, chapter 2).

Colour map as chapter 1: histamine gold, chloroquine blue, itch-route neurons teal,
pain-related output red, inhibition purple, neutral tissue white.
One world: skin strip (left), teal afferent, a dorsal-horn cross-section (centre), schematic gauges (right).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

HIST = "#F2B632"
CHLQ = BLUE
PURP = "#B58CD9"
PAIN = RED
NEUT = TEXT


def lab(text, size=28, color=TEXT, **kw):
    return T(text, size=size, color=color, weight=BOLD, **kw)


def sub(text, size=26, color=TEXT, **kw):
    return T(text, size=size, color=color, **kw)


class Flow(VGroup):
    """Drifting droplets along a line; limit cuts the stream, level fades it."""

    def __init__(self, p0, p1, color, n=4, speed=0.2, r=0.08, wob=0.1, seed=0, level=1.0):
        super().__init__()
        self.p0 = np.array([p0[0], p0[1], 0.0], float)
        self.p1 = np.array([p1[0], p1[1], 0.0], float)
        self.limit = 1.0
        self.level = level
        self.t = 0.0
        self.speed = speed
        self.wob = wob
        rng = np.random.RandomState(seed)
        self.ph = [(i + rng.rand() * 0.5) / n for i in range(n)]
        self.off = rng.rand(n) * 6.28
        for _ in range(n):
            self.add(Dot(radius=r, color=color, stroke_width=0))
        self.add_updater(Flow._upd)
        Flow._upd(self, 0)

    def _upd(self, dt=0):
        self.t += dt
        d = self.p1 - self.p0
        perp = np.array([-d[1], d[0], 0.0])
        perp = perp / (np.linalg.norm(perp) + 1e-9)
        for i, m in enumerate(self.submobjects):
            u = (self.ph[i] + self.t * self.speed) % 1.0
            m.move_to(self.p0 + d * u + perp * self.wob * np.sin(self.off[i] + self.t * 2.0))
            op = (np.sin(np.pi * u) ** 0.5) * (1.0 if u <= self.limit else 0.0) * self.level
            m.set_opacity(float(op))


def fl_to(fl, level, rt=1.0):
    l0 = fl.level
    return UpdateFromAlphaFunc(fl, lambda m, a: setattr(m, "level", l0 + (level - l0) * a), run_time=rt)


class Gauge(VGroup):
    def __init__(self, color, w=2.6, h=0.5, v=0.8):
        super().__init__()
        self.tr = ValueTracker(v)
        self.box = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_opacity=0)
        self.fill = Rectangle(width=w * max(v, 0.012), height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
        self.fill.align_to(self.box, LEFT)
        self.add(self.box, self.fill)
        self.add_updater(Gauge._upd)

    def _upd(self):
        v = max(self.tr.get_value(), 0.012)
        self.fill.stretch_to_fit_width(self.box.width * v)
        self.fill.align_to(self.box, LEFT)


def xmark(mob, color=RED, w=7, r=None):
    r = r or 0.5 * min(mob.width, mob.height) + 0.1
    c = mob.get_center()
    return VGroup(Line(c + np.array([-r, -r, 0]), c + np.array([r, r, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-r, r, 0]), c + np.array([r, -r, 0]), color=color, stroke_width=w)).set_z_index(8)


def dashed(mob, n=36, **kw):
    return DashedVMobject(mob, num_dashes=n, **kw)


# ---------------------------------------------------------------- the carried world
GX = 5.3   # gauge column


def horn_outline():
    return RoundedRectangle(corner_radius=0.5, width=6.8, height=5.4, stroke_color=GREY, stroke_width=3,
                            fill_color=TEXT, fill_opacity=0.07).move_to([0.2, 0, 0])


def skin_strip():
    r = Rectangle(width=0.6, height=6.4, stroke_color=GREY, stroke_width=3, fill_color=TEXT, fill_opacity=0.12).move_to([-6.5, 0, 0])
    l = sub("skin", 28).rotate(PI / 2).move_to([-6.5, 0, 0])
    return r, l


def afferent():
    line = Line([-6.2, 0, 0], [-3.0, 0, 0], color=TEAL, stroke_width=5)
    term = Circle(radius=0.28, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.5).move_to([-2.8, 0, 0])
    return line, term


CELL_XY = [(-1.0 + 0.9 * (i % 2), 1.6 - 0.8 * (i // 2)) for i in range(10)]
SURV = [0, 5, 8]


def npra_cells(survivors_only=False):
    cs = VGroup()
    for i, (x, y) in enumerate(CELL_XY):
        c = Circle(radius=0.3, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.18).move_to([x, y, 0])
        cs.add(c)
    return cs


def ghost_cells():
    g = VGroup()
    for i, (x, y) in enumerate(CELL_XY):
        if i not in SURV:
            g.add(dashed(Circle(radius=0.3, color=GREY, stroke_width=2).move_to([x, y, 0]), 12).set_opacity(0.55))
    return g


def grpr_cell(x=2.5, y=0.0):
    return Circle(radius=0.75, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.18).move_to([x, y, 0])


def grp_block(x=2.5, y=1.7):
    b = RoundedRectangle(corner_radius=0.08, width=0.5, height=0.6, stroke_color=TEXT, stroke_width=2,
                         fill_color=TEXT, fill_opacity=0.95).move_to([x, y, 0])
    b.set_z_index(5)
    return b


def scratch_gauge(v):
    g = Gauge(TEAL, 2.6, 0.5, v).move_to([GX, 1.2, 0])
    h = VGroup(lab("scratching", 28), sub("schematic", 22, GREY)).arrange(DOWN, buff=0.06).move_to([GX, 0.3, 0])
    return g, h


def pain_gauge(v=0.7):
    g = Gauge(PAIN, 2.6, 0.5, v).move_to([GX, -1.7, 0])
    h = lab("measured pain", 28, PAIN).move_to([GX, -2.45, 0])
    return g, h


def nppb_flow(level=1.0, seed=3):
    return Flow([-2.5, 0], [-1.4, 0], TEAL, n=4, seed=seed, r=0.1, level=level, speed=0.35, wob=0.05)


def nppb_path():
    return DashedLine([-2.5, 0, 0], [-1.5, 0, 0], color=TEAL, stroke_width=4, dash_length=0.12)


def mouse(s=1.0, color=TEXT):
    body = Ellipse(width=1.3, height=0.8, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3)
    head = Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3).move_to([0.75, 0.15, 0])
    ear = Circle(radius=0.14, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3).move_to([0.72, 0.5, 0])
    tail = ArcBetweenPoints([-0.65, 0, 0], [-1.35, 0.4, 0], angle=-1.2, color=color, stroke_width=3)
    return VGroup(body, head, ear, tail).scale(s)


def human(s=1.0, color=TEXT):
    head = Circle(radius=0.3, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3).move_to([0, 0.95, 0])
    body = RoundedRectangle(corner_radius=0.3, width=0.9, height=1.4, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.3).move_to([0, 0, 0])
    return VGroup(head, body).scale(s)


def chain_chip(text, color, x, y=-3.25):
    c = chip(text, color, size=28, pad=0.15)
    c.move_to([x, y, 0])
    return c


def chain():
    xs = [-5.0, -2.1, 0.8, 3.1]
    names = [("Nppb", TEAL), ("NPRA cells", TEXT), ("GRP", TEXT), ("GRPR", TEXT)]
    chips = [chain_chip(n, c, x) for (n, c), x in zip(names, xs)]
    arrows = []
    for a, b in zip(chips[:-1], chips[1:]):
        arrows.append(DashedLine(a.get_right() + RIGHT * 0.05, b.get_left() + LEFT * 0.05, color=TEXT, stroke_width=4,
                                 dash_length=0.1).add_tip(tip_length=0.2))
    return chips, arrows


def sweep():
    """A faint band that crosses the dorsal horn again and again, so a held frame still moves."""
    b = Rectangle(width=0.9, height=5.2, stroke_width=0, fill_color=TEAL, fill_opacity=0.22).move_to([-3.0, 0, 0])
    b.t = 0.0

    def upd(m, dt):
        m.t += dt
        u = (m.t / 5.0) % 1.0
        m.move_to([-3.0 + 6.6 * u, 0, 0])
        m.set_fill(opacity=0.22 * np.sin(np.pi * u) ** 0.7)
    b.add_updater(upd)
    return b


# ================================================================ s00
def ch1_world():
    skin = Rectangle(width=4.35, height=7.0, stroke_color=GREY, stroke_width=3, fill_color=TEXT, fill_opacity=0.08).move_to([-4.575, 0, 0])
    sk_l = sub("skin", 28).move_to([-5.2, 3.2, 0])
    cord = RoundedRectangle(corner_radius=0.25, width=2.4, height=6.0, stroke_color=GREY, stroke_width=3,
                            fill_color=TEXT, fill_opacity=0.08).move_to([5.4, 0, 0])
    ns = VGroup()
    for y in (1.5, 0.0, -1.5):
        fork = VGroup(*[Line([-2.7, y, 0], [-3.5, y + dy, 0], color=TEAL, stroke_width=4) for dy in (0.32, 0, -0.32)])
        axon = Line([-2.7, y, 0], [-0.42, y, 0], color=TEAL, stroke_width=4)
        soma = Circle(radius=0.42, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.35).move_to([0, y, 0])
        cen = Line([0.42, y, 0], [4.2, y, 0], color=TEAL, stroke_width=4)
        ns.add(VGroup(fork, axon, cen, soma))
    return skin, sk_l, cord, ns


class S00Link(TitleCard, SpokenScene):
    LESSON = "Itch: A Sense of Its Own"
    TITLE = "Order the Relay, Find the Brake"

    def construct(self):
        skin, sk_l, cord, ns = ch1_world()
        flows = VGroup()
        for i, y in enumerate((1.5, 0.0, -1.5)):
            flows.add(Flow([-5.6, y + 0.5], [-3.5, y + 0.12], HIST, seed=i), Flow([-5.6, y - 0.5], [-3.5, y - 0.12], CHLQ, seed=10 + i))
        self.add(skin, sk_l, cord, ns, flows)
        self.at("chapter")
        self.play(Indicate(ns, color=TEAL, scale_factor=1.05), run_time=2.0)
        self.at("once those neurons")
        self.play(*[Indicate(n[3], color=TEAL, scale_factor=1.5) for n in ns], run_time=1.6)
        q = lab("How is the spinal relay ordered?", 38, TEXT).move_to([2.0, 3.3, 0])
        self.at("how can experiments")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.8)
        self.at("spinal")
        self.play(Indicate(cord, color=TEAL, scale_factor=1.04), run_time=1.4)
        title = T(self.TITLE, 40, TEXT, font=TITLE_FONT).move_to([2.0, 3.3, 0])
        self.at("carry the same", lead=1.5)
        self.play(FadeOut(q), run_time=0.35)
        self.play(FadeIn(title), run_time=0.45)
        self.at("carry the same")
        # transform the chapter 1 picture into the dorsal-horn world
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        self.play(FadeOut(title), FadeOut(flows), FadeOut(ns[0]), FadeOut(ns[2]), FadeOut(sk_l),
                  ReplacementTransform(skin, s_r), ReplacementTransform(cord, horn), run_time=1.6)
        self.play(FadeIn(s_l), ReplacementTransform(ns[1], VGroup(aff, term)), run_time=1.4)
        dh = lab("dorsal horn", 30, TEXT).move_to([0.2, 3.3, 0])
        cells = npra_cells()
        self.at("dorsal horn")
        self.play(FadeIn(dh, shift=DOWN * 0.1), FadeIn(cells, lag_ratio=0.1), run_time=1.4)
        fl = nppb_flow(0.0)
        self.add(fl, sweep())
        self.play(FadeOut(dh), fl_to(fl, 0.0, 0.1), run_time=0.5)
        self.finish()


# ================================================================ s01
class S01KnockoutRescue(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        g, h = scratch_gauge(0.8)
        self.add(g.tr)
        self.add(s_r, s_l, horn, aff, term, cells, g, h)
        self.add(sweep())
        fl = nppb_flow(0.0)
        self.add(fl)
        self.at("afferent")
        self.play(Indicate(VGroup(aff, term), color=TEAL, scale_factor=1.05), fl_to(fl, 1.0, 1.0), run_time=1.0)
        nl = lab("Nppb", 30, TEAL).move_to([-2.0, 0.7, 0])
        path = nppb_path()
        self.at("nppb")
        self.play(FadeIn(nl, shift=DOWN * 0.1), Create(path), run_time=0.9)
        self.at("without nppb")
        xm = xmark(nl, r=0.4)
        self.play(FadeIn(xm), fl_to(fl, 0.0, 1.2), run_time=1.2)
        self.at("almost all")
        self.play(g.tr.animate.set_value(0.08), run_time=2.6)
        syr_barrel = Rectangle(width=0.5, height=0.7, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.15).move_to([1.0, 3.2, 0])
        syr_plunger = VGroup(Line([1.0, 3.55, 0], [1.0, 3.75, 0], color=TEXT, stroke_width=4), Line([0.8, 3.75, 0], [1.2, 3.75, 0], color=TEXT, stroke_width=4))
        syr_needle = Line([1.0, 2.85, 0], [1.0, 2.35, 0], color=TEXT, stroke_width=3)
        syr = VGroup(syr_barrel, syr_plunger, syr_needle).shift(DOWN * 0.35)
        il = lab("injected Nppb", 28, TEAL).move_to([-1.2, 3.3, 0])
        self.at("injecting")
        self.play(FadeOut(xm), FadeOut(nl), FadeIn(syr, shift=DOWN * 0.3), FadeIn(il), run_time=1.2)
        inj = Flow([1.0, 2.4], [0.0, 1.0], TEAL, n=5, seed=8, r=0.1, level=0.0, speed=0.35, wob=0.08)
        self.add(inj)
        self.at("around the cord")
        self.play(fl_to(inj, 1.0, 1.0), run_time=1.0)
        self.at("evoked scratching")
        self.play(g.tr.animate.set_value(0.75), Indicate(cells, color=TEAL, scale_factor=1.05), run_time=2.6)
        up = Rectangle(width=3.7, height=0.8, color=YELLOW, stroke_width=5).move_to([-4.2, 0.0, 0])
        self.at("the missing signal")
        self.play(Create(up), run_time=1.0)
        gc = grpr_cell()
        self.at("downstream machinery")
        self.play(FadeOut(up), FadeOut(syr), FadeOut(il), FadeIn(gc), run_time=1.0)
        self.play(Indicate(gc, color=TEXT, scale_factor=1.15), Indicate(g, color=TEAL, scale_factor=1.06), run_time=1.8)
        self.finish()


# ================================================================ s02
class S02Predict(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        gc = grpr_cell()
        g, h = scratch_gauge(0.75)
        self.add(g.tr)
        fl = nppb_flow(1.0)
        self.add(s_r, s_l, horn, aff, term, cells, gc, g, h, fl)
        self.add(sweep())
        gh = ghost_cells()
        gone = VGroup(*[cells[i] for i in range(10) if i not in SURV])
        pc = lab("about 70% removed", 30, YELLOW).move_to([-0.55, -2.3, 0])
        self.at("researchers")
        self.play(FadeOut(gone), FadeIn(gh), run_time=1.4)
        self.at("70")
        self.play(FadeIn(pc, shift=UP * 0.1), g.tr.animate.set_value(0.4), run_time=1.2)
        nl = lab("NPRA cells", 28, TEXT).move_to([-0.55, 2.3, 0])
        self.at("carrying")
        self.play(FadeIn(nl, shift=DOWN * 0.1), Indicate(VGroup(*[cells[i] for i in SURV]), color=TEXT, scale_factor=1.3), run_time=1.4)
        rl = lab("Nppb receptor", 28, TEAL).move_to([-0.55, 2.3, 0])
        self.at("these cells carry")
        self.play(FadeOut(pc), FadeOut(nl), run_time=0.5)
        self.play(FadeIn(rl), Indicate(fl, color=TEAL), run_time=1.1)
        gb = grp_block()
        gl = lab("GRP", 28, TEXT).move_to([2.5, 2.4, 0])
        q = lab("Can GRP bypass this loss?", 34, TEXT).move_to([0.2, 3.3, 0])
        self.at("if grp")
        self.play(FadeOut(rl), FadeIn(gb, shift=DOWN * 0.2), FadeIn(gl), run_time=0.9)
        gb.add_updater(lambda m, dt: m.shift(UP * 0.0))
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)
        self.at("should added")
        self.play(gb.animate.shift(DOWN * 0.12), Indicate(gc, color=TEXT, scale_factor=1.08), run_time=1.6)
        self.play(gb.animate.shift(UP * 0.12), run_time=1.0)
        self.finish()


# ================================================================ s03
class S03Pause(NarratedScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        gh = ghost_cells()
        gone = VGroup(*[cells[i] for i in range(10) if i not in SURV])
        gc = grpr_cell()
        g, h = scratch_gauge(0.4)
        self.add(g.tr)
        fl = nppb_flow(1.0)
        gb = grp_block()
        gl = lab("GRP", 28, TEXT).move_to([2.5, 2.4, 0])
        q = lab("Can GRP bypass this loss?", 34, TEXT).move_to([0.2, 3.3, 0])
        self.add(s_r, s_l, horn, aff, term, *[cells[i] for i in SURV], gh, gc, g, h, fl, gb, gl, q)
        self.add(sweep())
        self.play(gb.animate.shift(DOWN * 0.45), run_time=self.beat(0.9), rate_func=linear)
        self.finish()


# ================================================================ s04
class S04Bypass(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        surv = VGroup(*[cells[i] for i in SURV])
        gh = ghost_cells()
        gc = grpr_cell()
        g, h = scratch_gauge(0.4)
        self.add(g.tr)
        fl = nppb_flow(1.0)
        gb = grp_block(2.5, 1.25)
        gl = lab("GRP", 28, TEXT).move_to([2.5, 2.4, 0])
        q = lab("Can GRP bypass this loss?", 34, TEXT).move_to([0.2, 3.3, 0])
        self.add(s_r, s_l, horn, aff, term, surv, gh, gc, g, h, fl, gb, gl, q)
        self.add(sweep())
        rain = Flow([2.5, 1.0], [2.5, 0.3], TEXT, n=3, seed=5, r=0.08, level=0.0, speed=0.4, wob=0.1)
        self.add(rain)
        self.play(FadeOut(q), gb.animate.move_to([2.5, 0.95, 0]), run_time=0.7)
        self.at("still evoked")
        self.play(g.tr.animate.set_value(0.8), fl_to(rain, 1.0, 1.0), Indicate(gc, color=TEXT, scale_factor=1.12), run_time=2.0)
        chips, arrows = chain()
        fo = lab("functional order, not wiring", 32, YELLOW).move_to([0.2, 3.3, 0])
        self.at("simplest order")
        self.play(FadeIn(fo, shift=DOWN * 0.1), run_time=0.8)
        self.at("sensory nppb")
        self.play(FadeIn(chips[0]), Indicate(VGroup(aff, term), color=TEAL), run_time=1.0)
        self.at("then npra")
        self.play(Create(arrows[0]), FadeIn(chips[1]), Indicate(surv, color=TEXT, scale_factor=1.3), run_time=1.4)
        self.at("grp and")
        self.play(Create(arrows[1]), FadeIn(chips[2]), Indicate(gb, color=TEXT, scale_factor=1.4), run_time=1.0)
        self.at("grpr follow")
        self.play(Create(arrows[2]), FadeIn(chips[3]), Indicate(gc, color=TEXT, scale_factor=1.15), run_time=1.2)
        arc = ArcBetweenPoints([-2.6, 0.4, 0], [1.75, 0.5, 0], angle=-1.1, color=YELLOW, stroke_width=6)
        arc.set_stroke(YELLOW, 6)
        arc.add_tip(tip_length=0.25)
        self.at("bypassed")
        self.play(Create(arc), run_time=1.6)
        self.at("proposed upstream")
        self.play(Indicate(gh, color=YELLOW, scale_factor=1.1), run_time=1.6)
        self.finish()


# ================================================================ s04b
class S04bGrpr(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        surv = VGroup(*[cells[i] for i in SURV])
        gh = ghost_cells()
        gc = grpr_cell()
        g, h = scratch_gauge(0.8)
        self.add(g.tr)
        fl = nppb_flow(1.0)
        gb = grp_block(2.5, 0.95)
        gl = lab("GRP", 28, TEXT).move_to([2.5, 2.4, 0])
        rain = Flow([2.5, 1.0], [2.5, 0.3], TEXT, n=3, seed=5, r=0.08, level=1.0, speed=0.4, wob=0.1)
        chips, arrows = chain()
        self.add(s_r, s_l, horn, aff, term, surv, gh, gc, g, h, fl, gb, gl, rain, *chips, *arrows)
        self.add(sweep())
        self.play(FadeOut(VGroup(*chips, *arrows)), Indicate(gc, color=TEXT, scale_factor=1.12), run_time=1.0)
        gl2 = lab("GRPR", 28, TEXT).move_to([2.5, -1.2, 0])
        self.at("later grpr")
        self.play(FadeIn(gl2), run_time=0.8)
        mut = dashed(Circle(radius=0.75, color=PURP, stroke_width=5).move_to([2.5, 0, 0]), 20)
        ml = lab("mutant", 28, PURP).move_to([2.5, -1.2, 0])
        self.at("grpr mutant")
        self.play(FadeOut(gl2), FadeIn(mut), FadeIn(ml), gc.animate.set_fill(PURP, 0.2), run_time=1.2)
        self.at("scratched")
        self.play(g.tr.animate.set_value(0.35), fl_to(rain, 0.4, 1.5), run_time=2.0)
        rl = lab("removed", 28, RED).move_to([2.5, -1.2, 0])
        self.at("removing grpr")
        self.play(FadeOut(gc), FadeOut(mut), FadeOut(ml), FadeIn(rl), fl_to(rain, 0.0, 1.0), run_time=1.4)
        self.at("lowered scratching")
        self.play(g.tr.animate.set_value(0.12), run_time=2.0)
        pg, pl = pain_gauge(0.7)
        self.add(pg.tr)
        self.at("measured pain")
        self.play(FadeIn(pg), FadeIn(pl), run_time=1.0)
        self.play(Indicate(pg, color=PAIN, scale_factor=1.08), run_time=1.6)
        self.finish()


# ================================================================ s05
class S05Limits(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        surv = VGroup(*[cells[i] for i in SURV])
        gh = ghost_cells()
        gc = grpr_cell()
        gb = grp_block(2.5, 0.95)
        gl = lab("GRP", 28, TEXT).move_to([2.5, 2.4, 0])
        fl = nppb_flow(1.0)
        rain = Flow([2.5, 1.0], [2.5, 0.3], TEXT, n=3, seed=5, r=0.08, level=1.0, speed=0.4, wob=0.1)
        chips, arrows = chain()
        g, h = scratch_gauge(0.8)
        self.add(g.tr)
        self.add(s_r, s_l, horn, aff, term, surv, gh, gc, gb, gl, fl, rain, g, h)
        self.add(sweep())
        fo = lab("functional order", 34, YELLOW).move_to([0.2, 3.3, 0])
        self.play(FadeOut(g), FadeOut(h), FadeIn(VGroup(*chips, *arrows)), FadeIn(fo, shift=DOWN * 0.1), run_time=1.2)
        self.at("direct synapses")
        self.play(*[Indicate(a, color=YELLOW, scale_factor=1.15) for a in arrows], run_time=2.0)
        q1 = lab("?", 54, YELLOW).move_to([-2.8, 0.85, 0])
        sl1 = lab("sensory", 28, TEAL).move_to([-4.4, 0.85, 0])
        sp = dashed(Circle(radius=0.32, color=PURP, stroke_width=4).move_to([1.2, 1.7, 0]), 12)
        q2 = lab("?", 54, YELLOW).move_to([1.2, 2.3, 0])
        sl2 = lab("spinal", 28, PURP).move_to([0.0, 2.3, 0])
        self.at("did not identify")
        self.play(FadeIn(q1), FadeIn(sl1), run_time=0.8)
        self.play(FadeIn(sp), FadeIn(q2), FadeIn(sl2), run_time=1.0)
        self.play(Indicate(gb, color=TEXT, scale_factor=1.4), run_time=1.4)
        mo = mouse(1.0).move_to([-4.6, 1.9, 0])
        ml = lab("mouse", 28, TEXT).move_to([-4.6, 2.9, 0])
        bound = dashed(RoundedRectangle(corner_radius=0.3, width=10.2, height=7.4, color=YELLOW, stroke_width=4).move_to([-0.9, 0, 0]), 70)
        self.at("one supported")
        self.play(FadeOut(q1), FadeOut(sl1), FadeOut(q2), FadeOut(sl2), FadeOut(sp), FadeIn(mo), FadeIn(ml), Create(bound), run_time=1.8)
        hu = human(1.0).move_to([5.3, 0.3, 0])
        hl = lab("human", 28, TEXT).move_to([5.3, -1.0, 0])
        self.at("or a human")
        self.play(FadeIn(hu, shift=LEFT * 0.3), FadeIn(hl), run_time=1.2)
        self.play(Indicate(hu, color=YELLOW, scale_factor=1.1), run_time=1.4)
        self.finish()


# ================================================================ s06
class S06Brake(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        surv = VGroup(*[cells[i] for i in SURV])
        gh = ghost_cells()
        gc = grpr_cell()
        g, h = scratch_gauge(0.6)
        self.add(g.tr)
        fl = nppb_flow(1.0)
        rain = Flow([2.5, 1.0], [2.5, 0.3], TEXT, n=3, seed=5, r=0.08, level=1.0, speed=0.4, wob=0.1)
        self.add(s_r, s_l, horn, aff, term, surv, gh, gc, g, h, fl, rain)
        self.add(sweep())
        self.play(Indicate(g, color=TEAL, scale_factor=1.05), run_time=1.6)
        pc = Circle(radius=0.4, stroke_color=PURP, stroke_width=4, fill_color=PURP, fill_opacity=0.45).move_to([1.6, 2.0, 0])
        pl = lab("Bhlhb5-dependent", 28, PURP).move_to([1.2, 3.3, 0])
        piv = np.array([4.0, 1.7, 0.0])
        axon = Line([2.0, 2.0, 0], piv, color=PURP, stroke_width=4)
        lever = Line(piv, piv + RIGHT * 2.4, color=PURP, stroke_width=10)
        lever.rotate(0.7, about_point=piv)
        post = Dot(piv, radius=0.12, color=PURP)
        self.at("bhlhb", lead=1.2)
        self.play(FadeIn(pc), run_time=0.8)
        self.play(FadeIn(pl, shift=DOWN * 0.1), run_time=0.8)
        self.at("provide inhibition")
        self.play(FadeIn(axon), FadeIn(post), FadeIn(lever), run_time=0.6)
        self.play(Rotate(lever, angle=-0.7, about_point=piv), g.tr.animate.set_value(0.3), run_time=1.6)
        self.at("mice missing")
        self.play(FadeOut(pl), pc.animate.set_stroke(GREY, 3).set_fill(GREY, 0.1), FadeOut(axon), run_time=1.2)
        self.at("scratched excessively")
        self.play(Rotate(lever, angle=0.7, about_point=piv), g.tr.animate.set_value(0.95), run_time=2.2)
        same = lab("same input", 28, TEAL).move_to([-4.4, 0.9, 0])
        self.at("removing a")
        self.play(Indicate(g, color=TEAL, scale_factor=1.07), run_time=1.6)
        self.at("incoming itch")
        self.play(FadeIn(same), Indicate(VGroup(aff, term, fl), color=TEAL, scale_factor=1.05), run_time=1.8)
        self.finish()


# ================================================================ s07
class S07Mechanical(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        surv = VGroup(*[cells[i] for i in SURV])
        gh = ghost_cells()
        gc = grpr_cell()
        g, h = scratch_gauge(0.95)
        self.add(g.tr)
        fl = nppb_flow(1.0)
        self.add(s_r, s_l, horn, aff, term, surv, gh, gc, g, h, fl)
        self.add(sweep())
        ML, CL = 1.4, -0.3
        mech = Line([-6.2, ML, 0], [3.6, ML, 0], color=TEAL, stroke_width=5)
        chem = Line([-6.2, CL, 0], [3.6, CL, 0], color=TEAL, stroke_width=5)
        cc = Circle(radius=0.6, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.18).move_to([1.6, CL, 0])
        gm = Gauge(TEAL, 2.6, 0.45, 0.95).move_to([GX, ML, 0])
        gcm = Gauge(TEAL, 2.6, 0.45, 0.5).move_to([GX, CL, 0])
        gp = Gauge(PAIN, 2.6, 0.45, 0.6).move_to([GX, -1.9, 0])
        self.add(gm.tr, gcm.tr, gp.tr)
        # filament in, light touch
        fil = Line([-6.0, 2.3, 0], [-5.4, 1.7, 0], color=TEXT, stroke_width=6)
        fil.add_updater(lambda m, dt: m.shift(DOWN * 0.0))
        win = Flow([-5.9, ML], [-0.3, ML], TEXT, n=6, seed=21, r=0.07, level=0.0, speed=0.18, wob=0.05)
        wout = Flow([0.7, ML], [3.4, ML], TEXT, n=4, seed=22, r=0.07, level=0.0, speed=0.18, wob=0.05)
        gold = Flow([-5.9, CL + 0.2], [0.8, CL + 0.2], HIST, n=5, seed=23, level=0.0, speed=0.14)
        blue = Flow([-5.9, CL - 0.2], [0.8, CL - 0.2], CHLQ, n=5, seed=24, level=0.0, speed=0.14)
        cout1 = Flow([2.3, CL + 0.15], [3.4, CL + 0.15], HIST, n=2, seed=25, level=0.0, speed=0.14)
        cout2 = Flow([2.3, CL - 0.15], [3.4, CL - 0.15], CHLQ, n=2, seed=26, level=0.0, speed=0.14)
        self.add(win, wout, gold, blue, cout1, cout2)
        self.play(FadeOut(term), FadeOut(surv), FadeOut(gh), FadeOut(fl), FadeOut(h), FadeOut(gc), FadeOut(g),
                  ReplacementTransform(aff, mech), run_time=1.0)
        self.add(chem, cc)
        lt = lab("light touch", 28, TEXT).move_to([-4.3, 3.1, 0])
        self.play(Create(chem), FadeIn(cc), FadeIn(gcm), FadeIn(gm), FadeIn(fil, shift=DOWN * 0.1), FadeIn(lt),
                  fl_to(win, 1.0, 1.0), fl_to(wout, 1.0, 1.0), fl_to(gold, 1.0, 1.0), fl_to(blue, 1.0, 1.0),
                  fl_to(cout1, 1.0, 1.0), fl_to(cout2, 1.0, 1.0), run_time=1.2)
        gate = Circle(radius=0.4, stroke_color=PURP, stroke_width=5, fill_color=PURP, fill_opacity=0.5).move_to([0.2, ML, 0])
        npl = lab("NPY-lineage", 28, PURP).move_to([0.2, 2.2, 0])
        self.at("removing or silencing")
        self.play(FadeIn(gate), fl_to(wout, 0.25, 1.2), gm.tr.animate.set_value(0.3), FadeOut(lt), run_time=1.4)
        self.at("npy")
        self.play(FadeIn(npl, shift=DOWN * 0.1), run_time=0.8)
        ml = lab("mechanical", 28, TEAL).move_to([GX, ML + 0.6, 0])
        self.at("increased mechanical")
        self.play(FadeOut(gate), FadeOut(npl), fl_to(wout, 1.0, 1.4), FadeIn(ml), gm.tr.animate.set_value(0.92), run_time=2.0)
        cl = lab("chemical", 28, HIST).move_to([GX, CL + 0.55, 0])
        pl = lab("pain", 28, PAIN).move_to([GX, -1.35, 0])
        self.at("tested chemical")
        self.play(FadeIn(cl), FadeIn(gp), run_time=0.8)
        self.at("pain did not")
        self.play(FadeIn(pl), Indicate(gcm, color=HIST, scale_factor=1.06), Indicate(gp, color=PAIN, scale_factor=1.06), run_time=1.8)
        self.at("survived")
        self.play(Indicate(gm, color=TEAL, scale_factor=1.07), run_time=0.9)
        gl = lab("GRPR", 28, TEXT).move_to([1.6, -1.25, 0])
        self.at("grpr cell")
        self.play(FadeIn(gl), run_time=0.6)
        xm = xmark(cc, r=0.5)
        self.at("ablation")
        self.play(FadeIn(xm), run_time=0.8)
        self.finish()


# ================================================================ s08
class SpikeTrain(VGroup):
    def __init__(self, x0, x1, y, color, n, gain, seed, hmax=0.7):
        super().__init__()
        self.x0, self.x1, self.y, self.hmax = x0, x1, y, hmax
        self.gain = ValueTracker(gain)
        self.t = 0.0
        rng = np.random.RandomState(seed)
        self.pos = np.sort(rng.rand(n))
        self.hs = 0.45 + 0.55 * rng.rand(n)
        self.base = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3)
        self.spikes = VGroup(*[Line([0, y, 0], [0, y + 0.1, 0], color=color, stroke_width=5) for _ in range(n)])
        self.add(self.base, self.spikes)
        self.add_updater(SpikeTrain._upd)
        SpikeTrain._upd(self, 0)

    def _upd(self, dt=0):
        self.t += dt
        W = self.x1 - self.x0
        gain = self.gain.get_value()
        for p, h, s in zip(self.pos, self.hs, self.spikes):
            u = (p + 0.06 * self.t) % 1.0
            x = self.x0 + u * W
            s.put_start_and_end_on([x, self.y, 0], [x, self.y + self.hmax * h * gain, 0])


class S08Scratch(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        aff, term = afferent()
        cells = npra_cells()
        surv = VGroup(*[cells[i] for i in SURV])
        gc = grpr_cell()
        fl = nppb_flow(1.0)
        world = VGroup(s_r, horn, aff, term, surv, gc)
        self.add(world, s_l, fl)
        paw = VGroup(Ellipse(width=0.9, height=0.75, stroke_width=0, fill_color=PURP, fill_opacity=0.95),
                     *[Circle(radius=0.17, stroke_width=0, fill_color=PURP, fill_opacity=0.95).move_to([dx, dy, 0])
                       for dx, dy in [(-0.45, 0.55), (-0.15, 0.72), (0.15, 0.72), (0.45, 0.55)]]).move_to([5.6, 0.2, 0])
        self.at("scratching can")
        self.play(FadeOut(s_l), FadeOut(fl), world.animate.scale(0.32).move_to([-5.0, -2.6, 0]), FadeIn(paw), run_time=1.3)
        up = Line([-3.5, -2.2, 0], [-2.8, -2.2, 0], color=TEAL, stroke_width=5)
        up2 = Line([-2.8, -2.2, 0], [-2.8, 2.5, 0], color=TEAL, stroke_width=5)
        upf = Flow([-2.8, -2.2], [-2.8, 2.5], TEAL, n=6, seed=31, r=0.09, speed=0.25, wob=0.05)
        self.play(Create(up), Create(up2), run_time=0.8)
        self.add(upf)
        arc = ArcBetweenPoints([5.4, -0.4, 0], [-3.6, -2.7, 0], angle=0.5, color=PURP, stroke_width=6)
        arc.add_tip(tip_length=0.25)
        hdr = lab("primate recording", 30, TEXT).move_to([1.0, 3.3, 0])
        sk = sub("schematic", 24, GREY).move_to([5.5, 3.3, 0])
        LX0, LX1 = -2.4, 3.9
        st_b = SpikeTrain(LX0, LX1, 2.4, TEXT, 8, 0.6, 1)
        st_h = SpikeTrain(LX0, LX1, 0.85, HIST, 16, 1.0, 2)
        st_c = SpikeTrain(LX0, LX1, -0.7, PAIN, 16, 0.9, 3)
        self.add(st_b.gain, st_h.gain, st_c.gain)
        self.at("primate recordings")
        self.play(FadeIn(hdr, shift=DOWN * 0.1), FadeIn(sk), FadeIn(st_b), FadeIn(st_h), FadeIn(st_c), run_time=1.5)
        hdr2 = lab("spinothalamic neurons", 30, TEAL).move_to([1.0, 3.3, 0])
        lh = lab("histamine", 28, HIST).move_to([-4.6, 0.95, 0])
        self.at("suppressed histamine")
        self.play(Create(arc), FadeIn(lh), run_time=1.0)
        self.play(st_h.gain.animate.set_value(0.25), Indicate(paw, color=PURP, scale_factor=1.2), run_time=1.6)
        self.at("spinothalamic")
        self.play(Transform(hdr, hdr2), run_time=0.5)
        lb = lab("baseline", 28, TEXT).move_to([-4.6, 2.5, 0])
        lc = lab("capsaicin", 28, PAIN).move_to([-4.6, -0.6, 0])
        self.at("it spared")
        self.play(FadeOut(arc), run_time=0.6)
        self.at("baseline and")
        self.play(FadeIn(lb), Indicate(st_b, color=TEXT, scale_factor=1.03), run_time=1.0)
        self.at("capsaicin")
        self.play(FadeIn(lc), Indicate(st_c, color=PAIN, scale_factor=1.03), run_time=1.4)
        note = lab("a firing recording, not a sensation", 32, YELLOW).move_to([0.6, -3.3, 0])
        self.at("firing measurement")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=1.0)
        self.play(Indicate(note, color=YELLOW, scale_factor=1.04), run_time=1.6)
        self.finish()


# ================================================================ s09
class S09Rule(SpokenScene):
    def construct(self):
        s_r, s_l = skin_strip()
        horn = horn_outline()
        self.add(s_r, s_l, horn)
        self.add(sweep())
        afs = VGroup()
        flows = VGroup()
        for i, y in enumerate((1.0, 0.0, -1.0)):
            afs.add(Line([-6.2, y, 0], [-3.0, y, 0], color=TEAL, stroke_width=5),
                    Circle(radius=0.22, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.5).move_to([-2.8, y, 0]))
            flows.add(Flow([-6.1, y + 0.3], [-3.3, y + 0.1], HIST, n=3, seed=40 + i, level=1.0),
                      Flow([-6.1, y - 0.3], [-3.3, y - 0.1], CHLQ, n=3, seed=50 + i, level=1.0))
        self.add(afs, flows)
        cells = npra_cells()
        gc = grpr_cell()
        gb = grp_block(2.5, 0.95)
        rain = Flow([2.5, 1.0], [2.5, 0.3], TEXT, n=3, seed=5, r=0.08, level=1.0, speed=0.4, wob=0.1)
        relay = VGroup(DashedLine([-2.5, 0, 0], [-1.45, 0, 0], color=TEAL, stroke_width=4, dash_length=0.12),
                       DashedLine([0.2, 0, 0], [1.7, 0, 0], color=TEXT, stroke_width=4, dash_length=0.12).add_tip(tip_length=0.2))
        g1 = Circle(radius=0.3, stroke_color=PURP, stroke_width=4, fill_color=PURP, fill_opacity=0.45).move_to([1.6, 2.1, 0])
        g2 = Circle(radius=0.3, stroke_color=PURP, stroke_width=4, fill_color=PURP, fill_opacity=0.45).move_to([1.6, -2.1, 0])
        gg, gh = scratch_gauge(0.6)
        self.add(gg.tr)
        self.add(gg, gh)
        self.play(FadeIn(cells, lag_ratio=0.08), FadeIn(relay), FadeIn(gc), FadeIn(gb), run_time=2.0)
        self.add(rain)
        self.play(FadeIn(g1), FadeIn(g2), run_time=1.0)
        # steps
        def rect(w, h, x, y):
            return RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=YELLOW, stroke_width=6).move_to([x, y, 0])
        br = rect(2.6, 3.8, -5.0, 0.0)
        tl = lab("trigger", 32, HIST).move_to([0.2, 3.3, 0])
        self.at("trigger")
        self.play(Create(br), FadeIn(tl), run_time=0.7)
        tl2 = lab("recruited population", 32, TEAL).move_to([0.2, 3.3, 0])
        self.at("recruited population")
        self.play(br.animate.become(rect(1.0, 3.0, -2.9, 0.0)), Transform(tl, tl2), run_time=0.8)
        tl3 = lab("spinal route", 32, TEXT).move_to([0.2, 3.3, 0])
        self.at("spinal")
        self.play(br.animate.become(rect(5.0, 3.6, 0.9, 0.0)), Transform(tl, tl3), run_time=1.0)
        tl4 = lab("inhibition", 32, PURP).move_to([0.2, 3.3, 0])
        br2 = rect(1.0, 1.0, 1.6, -2.1)
        self.at("inhibition")
        self.play(br.animate.become(rect(1.0, 1.0, 1.6, 2.1)), Transform(tl, tl4), Create(br2), run_time=1.0)
        self.at("use perturbations")
        self.play(FadeOut(br2), br.animate.become(rect(1.4, 1.2, -2.0, 0.0)), FadeOut(tl), run_time=1.0)
        self.play(br.animate.become(rect(1.8, 1.2, 0.95, 0.0)), run_time=1.1)
        self.play(br.animate.become(rect(1.4, 1.2, 3.4, 0.0)), run_time=1.1)
        fo = lab("functional order, not complete wiring", 36, YELLOW).move_to([0.0, -3.3, 0])
        self.at("functional order")
        self.play(FadeOut(br), FadeIn(fo, shift=UP * 0.1), run_time=1.0)
        self.play(Indicate(fo, color=YELLOW, scale_factor=1.04), run_time=1.6)
        self.finish()


# ================================================================ s10
class S10End(EndCard):
    LINE = "Do not mistake functional order for complete wiring."
