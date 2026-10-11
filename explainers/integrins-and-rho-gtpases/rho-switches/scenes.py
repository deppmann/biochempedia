"""Three switches, three shapes  (Biochemistrypedia section film, lesson: Integrins and Rho GTPases)

Section: "Three switches for the actin skeleton". The experiment: Ridley and Hall (1992), then
Nobes and Hall and, separately, the Lim laboratory (1995).

COLOR MAP (one color per concept, whole video)
  ORANGE = Rho
  BLUE   = Rac
  PURPLE = Cdc42
  GREEN  = a switch that is on (GTP-bound)
  GREY   = the cell, off state, labels
  TEXT   = actin filaments (the pale line colour)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
COL = {"Rho": ORANGE, "Rac": BLUE, "Cdc42": PURPLE}


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def boundary(cx, cy, a, b, t, amp=0.0, ph=0.0, k=14):
    m = 1 + amp * np.sin(k * t + ph)
    return np.array([cx + a * np.cos(t) * m, cy + b * np.sin(t) * m, 0])


def outline(cx, cy, a, b, amp=0.0, ph=0.0, sw=4):
    return ParametricFunction(lambda t: boundary(cx, cy, a, b, t, amp, ph), t_range=[0, TAU, 0.02],
                              color=GREY, stroke_width=sw, fill_color=GREY, fill_opacity=0.08)


def sparse(cx, cy, a, b, op=0.35, sw=2.5):
    spots = [(-.5, .3, 20), (-.1, .5, 100), (.35, .4, 160), (.55, -.05, 60), (.25, -.45, 10),
             (-.2, -.35, 140), (-.55, -.2, 90), (.0, .0, 35)]
    g = VGroup()
    for fx, fy, ang in spots:
        c = np.array([cx + a * fx, cy + b * fy, 0])
        r = np.radians(ang)
        d = np.array([np.cos(r), np.sin(r), 0]) * 0.14 * a
        g.add(Line(c - d, c + d, color=TEXT, stroke_width=sw, stroke_opacity=op))
    return g


def cables(cx, cy, a, b, n=6, sw=7):
    g = VGroup()
    for i, f in enumerate(np.linspace(-0.62, 0.62, n)):
        y = cy + b * f
        hx = a * np.sqrt(1 - f * f) * 0.86
        tilt = 0.03 * b * (1 if i % 2 else -1)
        g.add(Line([cx - hx, y - tilt, 0], [cx + hx, y + tilt, 0], color=TEXT, stroke_width=sw, stroke_opacity=0.95))
    return g


def spikes(cx, cy, a, b, n=14, ln=0.6, sw=3.5, par=False):
    g = VGroup()
    for th in np.linspace(0.15, TAU + 0.15, n, endpoint=False):
        p = boundary(cx, cy, a, b, th)
        d = np.array([np.cos(th) * b, np.sin(th) * a, 0])
        d = d / np.linalg.norm(d)
        nrm = np.array([-d[1], d[0], 0])
        if par:
            for o in (-0.07, 0, 0.07):
                g.add(Line(p + nrm * o, p + nrm * o + d * ln, color=TEXT, stroke_width=sw))
        else:
            g.add(Line(p, p + d * ln, color=TEXT, stroke_width=sw))
    return g


def make_cell(kind, cx, cy, a, b, sw=4, cab=6, cabw=7, ln=0.6):
    if kind == "rac":
        out = outline(cx, cy, a, b, 0.1, 0.0, sw)
    else:
        out = outline(cx, cy, a, b, 0, 0, sw)
    if kind == "rho":
        inner = cables(cx, cy, a, b, cab, cabw)
    elif kind == "cdc":
        inner = VGroup(sparse(cx, cy, a, b), spikes(cx, cy, a, b, ln=ln, sw=3 if a < 3 else 3.5))
    else:
        inner = sparse(cx, cy, a, b)
    return VGroup(out, inner)


def toggle(on, x, y):
    col = GREEN if on else GREY
    pill = RoundedRectangle(corner_radius=0.3, width=1.2, height=0.6, stroke_color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.25).move_to([x, y, 0])
    knob = Circle(radius=0.22, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
        [x + (0.3 if on else -0.3), y, 0])
    return VGroup(pill, knob)


class S00Title(TitleCard):
    LESSON = "Integrins and Rho GTPases"
    TITLE = "Three switches, three shapes"


# ---------------------------------------------------------------------------------------------
class S01Shape(SpokenScene):
    def construct(self):
        cx, cy, a, b = -3.5, 0.2, 2.7, 2.3
        cell = outline(cx, cy, a, b)
        self.play(FadeIn(cell, scale=0.9), run_time=0.6)
        self.at("change shape", lead=0.3)
        self.play(Transform(cell, outline(cx, cy, a * 1.08, b * 0.94)), run_time=0.6)
        self.play(Transform(cell, outline(cx, cy, a, b)), run_time=0.5)
        fil = sparse(cx, cy, a, b, op=0.9, sw=4)
        fl = T("actin filaments", 26, GREY).move_to([cx, cy - b - 0.55, 0])
        self.at("actin filaments")
        self.play(FadeIn(fil), FadeIn(fl), run_time=0.6)

        ys = [2.0, 0.2, -1.6]
        names = ["Rho", "Rac", "Cdc42"]
        chips = [chip(n, COL[n], 36).move_to([1.9, y, 0]) for n, y in zip(names, ys)]
        self.at("Roe family")
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in chips], lag_ratio=0.25), run_time=1.0)
        tg = [toggle(False, 4.3, y) for y in ys]
        st = [T("GDP", 28, GREY).move_to([5.6, y, 0]) for y in ys]
        self.at("work as Ras")
        self.play(*[FadeIn(t) for t in tg], *[FadeIn(s) for s in st], run_time=0.6)
        gtp = [T("GTP", 28, GREEN).move_to([5.6, y, 0]) for y in ys]
        self.at("each one is on")
        self.play(*[Transform(tg[i], toggle(True, 4.3, ys[i])) for i in range(3)],
                  *[Transform(st[i], gtp[i]) for i in range(3)], run_time=0.6)
        gdp = [T("GDP", 28, GREY).move_to([5.6, y, 0]) for y in ys]
        self.at("it is off")
        self.play(*[Transform(tg[i], toggle(False, 4.3, ys[i])) for i in range(3)],
                  *[Transform(st[i], gdp[i]) for i in range(3)], run_time=0.6)
        bal = T("GEFs and GAPs set the balance", 28, GREY).move_to([3.4, -3.0, 0])
        self.at("set the balance")
        self.play(FadeIn(bal, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Inject(SpokenScene):
    def construct(self):
        cx, cy, a, b = -0.9, 0.0, 3.7, 2.0
        amp, ph = ValueTracker(0), ValueTracker(0)
        cell = always_redraw(lambda: outline(cx, cy, a, b, amp.get_value(), ph.get_value()))
        base = sparse(cx, cy, a, b)
        self.add(T("idealised drawings", 22, GREY).move_to([5.0, -3.3, 0]))
        who = T("Anne Ridley and Alan Hall, 1992", 28, GREY).move_to([0, 3.25, 0])
        self.play(FadeIn(cell), FadeIn(base), run_time=0.5)
        self.at("Anne Ridley")
        self.play(FadeIn(who, shift=DOWN * 0.1), run_time=0.5)
        pip = Line([5.6, 2.3, 0], [1.5, 0.6, 0], color=GREY, stroke_width=9)
        tip = Dot([1.5, 0.6, 0], radius=0.09, color=GREY)
        pp = chip("purified protein", GREY, 28).move_to([4.8, 3.0, 0])
        self.at("injected purified proteins")
        self.play(Create(pip), FadeIn(tip), FadeIn(pp, shift=DOWN * 0.1), run_time=0.8)
        lab = T("fibroblast, starved of serum", 28, GREY).move_to([cx, -3.2, 0])
        self.at("starved of serum")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        lab2 = T("little organised actin", 28, GREY).move_to([cx, -3.2, 0])
        self.at("little organized actin")
        self.play(Transform(lab, lab2), base.animate.set_stroke(opacity=0.9), run_time=0.5)

        rho = chip("active Rho", ORANGE, 30).move_to([4.8, 3.0, 0])
        cab = cables(cx, cy, a, b)
        res = T("thick actin cables", 28, ORANGE).move_to([cx, -3.2, 0])
        self.at("Active row")
        self.play(Transform(pp, rho), run_time=0.5)
        self.at("thick actin cables")
        self.play(FadeOut(base), Create(cab, lag_ratio=0.15), Transform(lab, res), run_time=1.2)
        rac = chip("active Rac", BLUE, 30).move_to([4.8, 3.0, 0])
        # reset: cables and result label cleared in the same beat as the new case label
        self.at("Active rack")
        base2 = sparse(cx, cy, a, b)
        self.play(Transform(pp, rac), FadeOut(cab), FadeOut(lab), FadeIn(base2), run_time=0.5)
        res2 = T("edges ruffle", 28, BLUE).move_to([cx, -3.2, 0])
        self.at("edges ruffle")
        self.play(amp.animate.set_value(0.1), FadeIn(res2, shift=UP * 0.1), run_time=0.8)
        self.play(ph.animate.set_value(TAU), run_time=2.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Spikes(SpokenScene):
    def construct(self):
        cx, cy, a, b = 0.8, 0.0, 3.7, 2.0
        cell = outline(cx, cy, a, b)
        base = sparse(cx, cy, a, b)
        self.play(FadeIn(cell), FadeIn(base), run_time=0.5)
        self.add(T("idealised drawings", 22, GREY).move_to([5.0, -3.3, 0]))
        n1 = chip("Catherine Nobes and Alan Hall", GREY, 26).move_to([-3.6, 3.05, 0])
        yr = T("1995", 28, GREY).move_to([0.2, 3.05, 0])
        self.at("Catherine Knobes")
        self.play(FadeIn(n1, shift=DOWN * 0.1), FadeIn(yr), run_time=0.6)
        c42 = chip("Cdc42", PURPLE, 36).move_to([-5.0, 0.0, 0])
        ca = arr([-4.1, 0.0, 0], [cx - a - 0.55, 0.0, 0], PURPLE)
        sp = spikes(cx, cy, a, b)
        res = T("thin spikes", 28, PURPLE).move_to([cx, -3.2, 0])
        self.at("produces thin spikes")
        self.play(FadeIn(c42, scale=0.8), GrowArrow(ca), run_time=0.5)
        self.play(LaggedStart(*[Create(s) for s in sp], lag_ratio=0.05), FadeIn(res, shift=UP * 0.1), run_time=1.0)
        n2 = chip("Louis Lim's laboratory", GREY, 26).move_to([3.4, 3.05, 0])
        self.at("laboratory of Lewis Lim")
        self.play(FadeIn(n2, shift=DOWN * 0.1), run_time=0.6)
        self.at("showed the same")
        self.play(Indicate(sp, color=PURPLE, scale_factor=1.0), Indicate(res, color=PURPLE), run_time=0.8)

        # three results side by side (same layout the next scene starts from)
        xs = [-4.2, 0, 4.2]
        kinds = ["rho", "rac", "cdc"]
        names = ["Rho", "Rac", "Cdc42"]
        row = [make_cell(k, x, 0.7, 1.7, 1.45, sw=3, cab=5, cabw=5, ln=0.35) for k, x in zip(kinds, xs)]
        nm = [chip(n, COL[n], 34).move_to([x, 3.1, 0]) for n, x in zip(names, xs)]
        self.at("three different shapes", lead=0.4)
        self.play(FadeOut(VGroup(cell, base, n1, n2, yr, c42, ca, sp, res)),
                  *[FadeIn(r) for r in row], *[FadeIn(c, shift=DOWN * 0.1) for c in nm], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Rule(SpokenScene):
    def construct(self):
        xs = [-4.2, 0, 4.2]
        kinds = ["rho", "rac", "cdc"]
        names = ["Rho", "Rac", "Cdc42"]
        row = [make_cell(k, x, 0.7, 1.7, 1.45, sw=3, cab=5, cabw=5, ln=0.35) for k, x in zip(kinds, xs)]
        nm = [chip(n, COL[n], 34).move_to([x, 3.1, 0]) for n, x in zip(names, xs)]
        self.add(*row, *nm)
        self.wait(0.3)

        def desc(x, head, body, col):
            h = T(head, 32, col, weight=BOLD)
            bd = T(body, 24, GREY, line_spacing=0.9)
            g = VGroup(h, bd).arrange(DOWN, buff=0.15)
            return g.move_to([x, -1.9, 0])

        d1 = desc(xs[0], "stress fibres", "actin and myosin II\ncables that contract", ORANGE)
        d2 = desc(xs[1], "lamellipodia", "broad, thin sheets,\npushed forward", BLUE)
        d3 = desc(xs[2], "filopodia", "thin fingers", PURPLE)
        self.at("builds stress fibers")
        self.play(FadeIn(d1, shift=UP * 0.15), Indicate(row[0][1], color=ORANGE, scale_factor=1.03), run_time=0.8)
        self.at("that contract")
        self.play(row[0][1].animate.stretch(0.93, 0), run_time=0.5)
        self.play(row[0][1].animate.stretch(1 / 0.93, 0), run_time=0.4)
        self.at("builds lamellipodia")
        self.play(FadeIn(d2, shift=UP * 0.15), Indicate(row[1][0], color=BLUE, scale_factor=1.03), run_time=0.8)
        # branching mesh near the edge of the sheet (schematic)
        mesh = VGroup()
        for py in (1.35, 0.8, 0.25):
            p = np.array([-0.2, py, 0])
            mesh.add(Line(p, p + np.array([1.2, 0, 0]), color=TEXT, stroke_width=3.5))
            for bx in (0.4, 0.8):
                q = p + np.array([bx, 0, 0])
                mesh.add(Line(q, q + np.array([0.35, 0.28, 0]), color=TEXT, stroke_width=3.5))
        self.at("branching mesh")
        self.play(Create(mesh, lag_ratio=0.2), run_time=0.9)
        self.at("builds filipodia")
        self.play(FadeIn(d3, shift=UP * 0.15), Indicate(row[2][1], color=PURPLE, scale_factor=1.03), run_time=0.8)
        d3b = desc(xs[2], "filopodia", "thin fingers with a\ncore of parallel filaments", PURPLE)
        par = spikes(xs[2], 0.7, 1.7, 1.45, ln=0.35, sw=2.5, par=True)
        self.at("parallel")
        self.play(Transform(d3, d3b), FadeOut(row[2][1][1]), FadeIn(par), run_time=0.8)
        rule = T("Each Rho family switch decides the shape", 30, TEXT)
        self.at("Keep this rule")
        self.play(FadeIn(rule.move_to([0, -3.35, 0]), shift=UP * 0.15), run_time=0.6)
        self.finish()


class S05End(EndCard):
    LINE = "Each Rho family switch decides which shape filaments build."
