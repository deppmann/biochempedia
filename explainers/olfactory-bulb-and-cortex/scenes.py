"""Same address, different message: sister mitral/tufted cells (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = sister cell 1 (and its spikes, bars)
  YELLOW = sister cell 2 (and its spikes, bars)
  TEAL   = shared input: the glomerulus, receptor neurons, the link between sisters
  GREEN  = rate (mean spike count) and the "looks like copies" reading
  ORANGE = timing against the breath
  PURPLE = granule cell and its inhibition (bar-ended arrows)
  GOLD   = light used to find the parent glomerulus
  GREY   = labels, axes, breath curve, electrodes, de-emphasized
  RED    = only the strike-through "no"
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
C1, C2 = BLUE, YELLOW

LAYOUT = {
    "big": dict(glom=(-4.2, 0.3), gr=0.95, rec=[(-5.4, -2.2), (-4.2, -2.3), (-3.0, -2.2)],
                recend=[(-4.8, -0.55), (-4.2, -0.65), (-3.6, -0.55)], rect=(-4.2, -2.8),
                s1=(0.2, 1.8), s2=(0.2, -1.0), sr=0.42, d1e=(-3.4, 0.95), d2e=(-3.4, -0.3),
                axend=3.2, n1=(0.2, 2.55), n2=(0.2, -1.7), ctx=(5.0, 0.4)),
    "side": dict(glom=(-5.0, 0.1), gr=0.95, rec=[(-5.9, -1.95), (-5.0, -2.05), (-4.1, -1.95)],
                 recend=[(-5.45, -0.75), (-5.0, -0.85), (-4.55, -0.75)], rect=(-5.0, -2.5),
                 s1=(-2.6, 1.3), s2=(-2.6, -1.1), sr=0.38, d1e=(-4.2, 0.75), d2e=(-4.2, -0.55),
                 axend=-1.3, n1=(-2.6, 1.95), n2=(-2.6, -1.75), ctx=(5.0, 0.4)),
}


def bez(a, b, bend):
    a, b = np.array(list(a)[:2] + [0.]), np.array(list(b)[:2] + [0.])
    m = (a + b) / 2
    c1 = a + (m - a) * 0.6 + np.array([0, bend, 0])
    c2 = b + (m - b) * 0.6 + np.array([0, bend * 0.3, 0])
    return CubicBezier(a, c1, c2, b, stroke_width=5)


def build(kind="big", names=True):
    L = LAYOUT[kind]
    p = {}
    p["glom"] = Circle(radius=L["gr"], stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.2).move_to([*L["glom"], 0])
    p["glom_t"] = T("glomerulus", 22, TEAL).move_to(p["glom"])
    p["rec"] = VGroup(*[Line([*a, 0], [*b, 0], color=TEAL, stroke_width=4) for a, b in zip(L["rec"], L["recend"])])
    p["rec_t"] = T("receptor neurons", 22, TEAL).move_to([*L["rect"], 0])
    for i, (col, key, ekey) in enumerate([(C1, "s1", "d1e"), (C2, "s2", "d2e")], start=1):
        c = np.array([*L[key], 0])
        p[f"s{i}"] = Circle(radius=L["sr"], stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.25).move_to(c)
        d = bez(c + LEFT * L["sr"], L[ekey], 0.35 if i == 1 else -0.35).set_color(col)
        p[f"d{i}"] = d
        p[f"a{i}"] = Arrow(c + RIGHT * L["sr"], [L["axend"], L[key][1], 0], buff=0.0, color=col, stroke_width=5,
                           tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        p[f"n{i}"] = T(f"sister {i}", 22, col).move_to([*L["n1" if i == 1 else "n2"], 0])
    p["ctx"] = chip("piriform cortex", GREY, size=22, pad=0.18).move_to([*L["ctx"], 0])
    return p


def parts(p, keys):
    return VGroup(*[p[k] for k in keys])


STRUCT = ["rec", "glom", "glom_t", "rec_t", "s1", "s2", "d1", "d2", "a1", "a2"]


def morph_to_side(scene, big, run_time):
    side = build("side")
    anims = []
    for k in STRUCT + ["n1", "n2"]:
        anims.append(Transform(big[k], side[k]))
    return anims


def ticks(x0, x1, y, phases, color, h=0.5):
    return VGroup(*[Line([x0 + (x1 - x0) * ph, y - h / 2, 0], [x0 + (x1 - x0) * ph, y + h / 2, 0], color=color, stroke_width=5)
                    for ph in phases])


def cluster(c, n=4, step=0.045):
    return [c + (i - (n - 1) / 2) * step for i in range(n)]


def tag(text="adult anaesthetized mice"):
    return T(text, 22, GREY).move_to([-2.2, -3.3, 0])


def strike(mob, color=RED):
    return Line(mob.get_corner(DL) + np.array([0.04, 0.04, 0]), mob.get_corner(UR) + np.array([-0.04, -0.04, 0]), color=color, stroke_width=6)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "From Glomeruli to Piriform Cortex"
    TITLE = "Same Address, Different Message"


class S01Question(SpokenScene):
    def construct(self):
        p = build("big")
        self.at("cells in the mouse")
        self.play(FadeIn(p["s1"], scale=0.6), FadeIn(p["s2"], scale=0.6), run_time=0.6)
        self.at("one glomerulus")
        self.play(Create(p["d1"]), Create(p["d2"]), FadeIn(p["glom"], scale=0.7), FadeIn(p["glom_t"]), run_time=1.0)
        self.at("receptor neurons converge")
        self.play(Create(p["rec"]), FadeIn(p["rec_t"]), run_time=0.9)
        self.at("called sisters")
        self.play(FadeIn(p["n1"]), FadeIn(p["n2"]), Create(p["a1"]), Create(p["a2"]), run_time=0.8)
        self.at("same message")
        q1 = chip("?", C1, size=34, pad=0.2).move_to([3.7, 1.8, 0])
        q2 = chip("?", C2, size=34, pad=0.2).move_to([3.7, -1.0, 0])
        self.play(FadeIn(q1, scale=0.5), FadeIn(q2, scale=0.5), run_time=0.7)
        self.at("only an address")
        self.play(Indicate(VGroup(p["glom"], p["glom_t"]), color=TEAL, scale_factor=1.15), run_time=1.0)
        self.finish()


class S02Sisters(SpokenScene):
    def construct(self):
        p = build("big")
        self.add(*[p[k] for k in STRUCT + ["n1", "n2"]])
        for q, y, c in [("?", 1.8, C1), ("?", -1.0, C2)]:
            pass
        self.at("Mitral and tufted")
        m1 = T("mitral or tufted cell", 22, GREY).move_to([0.2, 3.05, 0])
        m2 = T("mitral or tufted cell", 22, GREY).move_to([0.2, -2.2, 0])
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.6)
        self.at("output neurons")
        self.play(*[Indicate(p[k], color=WHITE, scale_factor=1.2) for k in ("a1", "a2")], FadeIn(p["ctx"]), run_time=1.0)
        self.at("primary dendrite")
        self.play(p["d1"].animate.set_stroke(width=10), p["d2"].animate.set_stroke(width=10), run_time=0.6)
        pd = T("one primary dendrite", 22, GREY).move_to([-1.6, 0.4, 0])
        self.play(FadeIn(pd), run_time=0.4)
        self.at("sister cells")
        link = DashedLine([0.2, 1.38, 0], [0.2, -0.58, 0], color=TEAL, stroke_width=4)
        lab = T("sisters", 24, TEAL).move_to([1.15, 0.4, 0])
        self.play(Create(link), FadeIn(lab), run_time=0.7)
        self.at("recorded sisters")
        e1 = VGroup(Line([1.3, 2.55, 0], [0.5, 1.95, 0], color=GREY, stroke_width=5), Dot([0.5, 1.95, 0], radius=0.07, color=GREY))
        e2 = VGroup(Line([1.4, -1.9, 0], [0.5, -1.3, 0], color=GREY, stroke_width=5), Dot([0.5, -1.3, 0], radius=0.07, color=GREY))
        el = T("electrodes", 22, GREY).move_to([2.7, -1.85, 0])
        tg = tag()
        pass
        self.play(Create(e1), Create(e2), FadeIn(el), run_time=0.7)
        self.at("in adult")
        self.play(FadeIn(tg), run_time=0.5)
        self.at("used light")
        rings = VGroup(*[Circle(radius=1.0 + 0.3 * i, color=GOLD, stroke_width=4, stroke_opacity=0.9 - 0.25 * i).move_to(p["glom"]) for i in range(3)])
        lt = T("light", 24, GOLD).move_to([-5.7, 1.9, 0])
        self.play(FadeIn(lt), LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3), run_time=1.0)
        self.at("parent glomerulus")
        self.play(Indicate(VGroup(p["glom"], p["glom_t"]), color=TEAL, scale_factor=1.12), run_time=0.8)
        self.play(FadeOut(rings), FadeOut(lt), run_time=0.4)
        self.at("by their input")
        self.play(Indicate(VGroup(p["d1"], p["d2"], p["glom"]), color=TEAL, scale_factor=1.05), run_time=0.8)
        self.at("how they responded")
        r = chip("response to odours", GREY, size=22, pad=0.16).move_to([4.7, 2.7, 0])
        self.play(FadeIn(r), run_time=0.4)
        x = strike(r)
        self.play(Create(x), run_time=0.4)
        self.finish()


class S03Rate(SpokenScene):
    def construct(self):
        p = build("big")
        self.add(*[p[k] for k in STRUCT + ["n1", "n2"]])
        tg = tag()
        self.add(tg)
        m = [T("mitral or tufted cell", 22, GREY).move_to([0.2, 3.05, 0]), T("mitral or tufted cell", 22, GREY).move_to([0.2, -2.2, 0])]
        # start of scene: the circuit slides to the left, extras fade
        self.play(*morph_to_side(self, p, 0.9), run_time=0.9)
        self.at("counting mean spikes")
        base = Line([0.3, -2.0, 0], [6.0, -2.0, 0], color=GREY, stroke_width=3)
        yax = Line([0.3, -2.0, 0], [0.3, 2.2, 0], color=GREY, stroke_width=3)
        ttl = T("mean spike count", 26, GREEN).move_to([3.2, 3.2, 0])
        sub = T("relative units, in this sketch", 22, GREY).move_to([3.2, 2.8, 0])
        xs = [1.5, 3.2, 4.9]
        labs = [T(f"odour {n}", 22, GREY).move_to([x, -2.4, 0]) for n, x in zip("ABC", xs)]
        labs = [T(t, 22, GREY).move_to([x, -2.4, 0]) for t, x in zip(["odour A", "odour B", "odour C"], xs)]
        self.play(Create(base), Create(yax), FadeIn(ttl), FadeIn(sub), *[FadeIn(l) for l in labs], run_time=0.9)
        self.at("rate for each")
        self.play(Indicate(VGroup(*labs), color=GREEN, scale_factor=1.1), run_time=0.7)
        self.at("rates of the two sisters")
        h1, h2 = [0.9, 2.0, 1.4], [1.0, 1.85, 1.5]
        unit = 1.5
        bars = []
        for x, a, b in zip(xs, h1, h2):
            for dx, h, col in [(-0.3, a, C1), (0.3, b, C2)]:
                bar = Rectangle(width=0.5, height=h * unit, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.35)
                bar.move_to([x + dx, -2.0 + h * unit / 2, 0])
                bars.append(bar)
        grow = [GrowFromEdge(b, DOWN) for b in bars]
        self.play(*grow, run_time=1.4)
        self.at("vary together")
        mid = VGroup(bars[2], bars[3])
        self.play(Indicate(mid, color=WHITE, scale_factor=1.12), run_time=0.9)
        self.at("identical information")
        badge = chip("rates: correlated", GREEN, size=26).move_to([3.2, 1.95, 0])
        self.play(FadeIn(badge, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


def timing_panel():
    x0, x1 = 1.5, 6.0
    ph = np.linspace(0, 1, 80)
    pts = [[x0 + (x1 - x0) * t, 1.0 + 0.4 * np.sin(2 * np.pi * t - np.pi / 2), 0] for t in ph]
    breath = VMobject(color=GREY, stroke_width=4).set_points_smoothly([np.array(q) for q in pts])
    y1, y2 = -0.1, -1.25
    r1 = Line([x0, y1 - 0.35, 0], [x1, y1 - 0.35, 0], color=C1, stroke_width=2, stroke_opacity=0.5)
    r2 = Line([x0, y2 - 0.35, 0], [x1, y2 - 0.35, 0], color=C2, stroke_width=2, stroke_opacity=0.5)
    l1 = T("sister 1", 22, C1).move_to([0.3, y1, 0])
    l2 = T("sister 2", 22, C2).move_to([0.3, y2, 0])
    ax = Arrow([x0, -1.95, 0], [x1, -1.95, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.18)
    axl = T("one respiration cycle", 22, GREY).move_to([(x0 + x1) / 2, -2.3, 0])
    return dict(x0=x0, x1=x1, y1=y1, y2=y2, breath=breath, r1=r1, r2=r2, l1=l1, l2=l2, ax=ax, axl=axl)


def spike_rows(P, ph1, ph2):
    return (ticks(P["x0"], P["x1"], P["y1"], cluster(ph1), C1), ticks(P["x0"], P["x1"], P["y2"], cluster(ph2), C2))


class S04Timing(SpokenScene):
    def construct(self):
        p = build("side")
        self.add(*[p[k] for k in STRUCT + ["n1", "n2"]])
        tg = tag()
        self.add(tg)
        P = timing_panel()
        self.at("spike timing")
        ttl = T("spike timing", 26, ORANGE).move_to([3.4, 3.2, 0])
        sub = T("in this sketch", 22, GREY).move_to([3.4, 2.8, 0])
        self.play(FadeIn(ttl), FadeIn(sub), FadeIn(P["l1"]), FadeIn(P["l2"]), Create(P["r1"]), Create(P["r2"]), run_time=0.8)
        self.at("respiration cycle")
        self.play(Create(P["breath"]), FadeIn(P["ax"]), FadeIn(P["axl"]), run_time=1.2)
        self.at("rhythm of the animal's")
        dot = Dot(P["breath"].get_start(), radius=0.1, color=ORANGE)
        self.play(MoveAlongPath(dot, P["breath"]), run_time=1.6, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.2)
        self.at("change the timing")
        t1a, t2a = spike_rows(P, 0.22, 0.66)
        od = chip("odour A", GREY, size=24).move_to([3.4, 2.0, 0])
        self.play(FadeIn(od), LaggedStart(*[Create(t) for t in list(t1a) + list(t2a)], lag_ratio=0.12), run_time=1.0)
        self.at("differently")
        t1b, t2b = spike_rows(P, 0.5, 0.12)
        od2 = chip("odour B", GREY, size=24).move_to([3.4, 2.0, 0])
        self.play(Transform(od, od2), Transform(t1a, t1b), Transform(t2a, t2b), run_time=1.2)
        self.at("same number of spikes")
        same = chip("same spike count", GREEN, size=24).move_to([3.4, -3.1, 0])
        self.play(FadeIn(same, scale=0.8), run_time=0.5)
        self.at("did not treat")
        nc = chip("by timing: not copies", ORANGE, size=24).move_to([3.4, -3.1, 0])
        self.play(ReplacementTransform(same, nc), run_time=0.7)
        self.finish()


class S05Cautions(SpokenScene):
    def construct(self):
        p = build("side")
        self.add(*[p[k] for k in STRUCT + ["n1", "n2"]])
        c_rate = chip("rate: correlated", GREEN, size=26)
        c_time = chip("timing: different", ORANGE, size=26)
        row = VGroup(c_rate, c_time).arrange(RIGHT, buff=0.4).move_to([2.9, 2.7, 0])
        self.at("two cell types")
        self.play(FadeIn(row, shift=DOWN * 0.1), run_time=0.7)
        self.at("different breath phases")
        self.play(Indicate(c_rate, color=GREEN), Indicate(c_time, color=ORANGE), run_time=1.0)
        self.at("Around the output cells")
        self.play(FadeOut(row), run_time=0.4)
        self.at("interneurons such as granule")
        g = Circle(radius=0.4, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.25).move_to([0.6, 0.1, 0])
        gl = T("granule cell", 22, PURPLE).move_to([2.2, 0.1, 0])
        self.play(FadeIn(g, scale=0.6), FadeIn(gl), run_time=0.7)
        self.at("reciprocal synapses")
        arrows = VGroup()
        for sgn, col in [(1, C1), (-1, C2)]:
            def Y(y):
                return y if sgn == 1 else 0.2 - y
            stub = Line([-2.5, Y(0.95), 0], [-2.05, Y(1.0), 0], color=col, stroke_width=6)
            ex = Arrow([-2.05, Y(0.95), 0], [0.2, Y(0.42), 0], buff=0.0, color=col, stroke_width=4, tip_length=0.18)
            tail, tip = np.array([0.28, Y(0.52), 0]), np.array([-2.05, Y(1.1), 0])
            ih = Line(tail, tip, color=PURPLE, stroke_width=4)
            d = (tip - tail) / np.linalg.norm(tip - tail)
            perp = np.array([-d[1], d[0], 0])
            cap = Line(tip + perp * 0.2, tip - perp * 0.2, color=PURPLE, stroke_width=6)
            arrows.add(stub, ex, ih, cap)
        leg = VGroup(T("arrow: excites   bar: inhibits", 22, GREY).move_to([1.6, -2.4, 0]), T("dendrodendritic synapses", 22, GREY).move_to([0.9, -1.6, 0]))
        self.play(Create(arrows), FadeIn(leg), run_time=1.3)
        self.at("which synapses made them")
        q = chip("?", GREY, size=34, pad=0.2).move_to([-1.0, 0.1, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.at("granule cell inhibition")
        self.play(Indicate(VGroup(g, gl), color=PURPLE, scale_factor=1.15), run_time=0.9)
        self.at("Awaken")
        an = chip("awake mouse", GREY, size=24).move_to([3.9, 2.3, 0])
        self.play(FadeIn(an, shift=DOWN * 0.1), run_time=0.5)
        self.at("diverse responses")
        aw = chip("awake M72 sisters: diverse", GREY, size=24)
        aw[0].set_stroke(opacity=0.8)
        aw.move_to([3.9, 0.9, 0])
        self.play(FadeIn(aw, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        p = build("side")
        self.add(*[p[k] for k in STRUCT + ["n1", "n2"]])
        tg = tag()
        self.add(tg)
        P = timing_panel()
        self.at("shared address")
        addr = chip("shared address", TEAL, size=22, pad=0.18).move_to([-4.9, 1.95, 0])
        self.play(FadeIn(addr, shift=DOWN * 0.1), Indicate(p["glom"], color=TEAL, scale_factor=1.12), run_time=0.8)
        self.at("not a shared message")
        t1, t2 = spike_rows(P, 0.5, 0.12)
        parts_ = [P["l1"], P["l2"], P["r1"], P["r2"], P["breath"], P["ax"], P["axl"]]
        self.play(*[FadeIn(x) for x in parts_], run_time=0.7)
        self.play(LaggedStart(*[Create(t) for t in list(t1) + list(t2)], lag_ratio=0.1), run_time=0.8)
        msg = chip("same count, different timing", ORANGE, size=24).move_to([3.4, 2.7, 0])
        self.play(FadeIn(msg, shift=DOWN * 0.1), run_time=0.5)
        self.at("rate alone")
        cp = chip("rate alone: incomplete", GREEN, size=24).move_to([3.4, -3.0, 0])
        self.play(FadeIn(cp, scale=0.8), run_time=0.6)
        self.at("shows that sisters are not copies")
        self.play(Indicate(cp, color=GREEN), run_time=0.5)
        self.at("vary together")
        self.play(Indicate(cp, color=GREEN, scale_factor=1.05), run_time=0.7)
        self.at("disagree on when")
        self.play(Indicate(VGroup(t1, t2, P["breath"]), color=ORANGE, scale_factor=1.04), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "A shared glomerulus is a shared address, not a shared message."
