"""Vibration corpuscles: is the onion the filter?  (Biochemistrypedia Sensory Systems explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  INDIGO = outer core of the corpuscle (the onion layers, the capsule)
  TEAL   = inner core / lamellar cells (the cells that touch the terminal)
  YELLOW = the nerve ending (terminal) and its impulses (spikes)
  GREEN  = graded signal of the ending (generator potential, transduction current)
  ORANGE = the mechanical stimulus (press, tap, vibration)
  RED    = what is not shown / not supported
  GREY   = labels, axes, preparation tags
All traces are sketches ("in this sketch"); the only numbers on screen are the lesson's own.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
INDIGO = "#9B8CF2"
SKETCH = "in this sketch"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def corpuscle(n_outer=5):
    """A corpuscle drawn as labelled layers around a nerve ending (schematic, never to scale)."""
    outer = VGroup(*[Ellipse(width=4.0 - 0.42 * i, height=3.2 - 0.4 * i, stroke_color=INDIGO, stroke_width=3,
                             fill_color=INDIGO, fill_opacity=0.05) for i in range(n_outer)])
    inner = VGroup(Ellipse(width=1.9, height=1.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.08),
                   Ellipse(width=1.45, height=0.95, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.08))
    axon = Line(LEFT * 2.45, LEFT * 0.3, color=YELLOW, stroke_width=7)
    term = RoundedRectangle(corner_radius=0.13, width=0.9, height=0.26, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.9).move_to(LEFT * 0.0)
    g = VGroup(outer, inner, axon, term)
    g.outer, g.inner, g.axon, g.term = outer, inner, axon, term
    return g


def place(g, x, y, s=0.85):
    g.scale(s).move_to([x, y, 0])
    return g


def spike(x, y, h=0.8, w=0.3, color=YELLOW, sw=5):
    pts = [[x - w, y, 0], [x - w / 3, y, 0], [x, y + h, 0], [x + w / 3, y - 0.12, 0], [x + w, y, 0]]
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_as_corners(pts)
    return m


def poly(pts, color, sw=5):
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_as_corners([[x, y, 0] for x, y in pts])
    return m


def tag(text, color=GREY, size=22):
    return T(text, size, color)


def fade_arrow(x, y_from, y_to, color=ORANGE, n=5, w=7):
    """a downward force arrow built from segments whose opacity falls off (force dissipated)."""
    ys = np.linspace(y_from, y_to, n + 1)
    segs = VGroup(*[Line([x, ys[i], 0], [x, ys[i + 1], 0], color=color, stroke_width=w,
                         stroke_opacity=max(0.1, 1 - 0.22 * i)) for i in range(n)])
    return segs


def press_arrow(x, y_from, y_to, color=ORANGE, w=8):
    return Arrow([x, y_from, 0], [x, y_to, 0], buff=0, color=color, stroke_width=w, tip_length=0.3,
                 max_tip_length_to_length_ratio=0.4)


def lead(a, b, color=GREY, w=2):
    return Line(a, b, color=color, stroke_width=w, stroke_opacity=0.8)


class S00Title(TitleCard):
    LESSON = "Meissner and Pacinian corpuscles"
    TITLE = "Is the Onion the Filter?"


# ---------------------------------------------------------------------------------------------
class S01Press(SpokenScene):
    """Pacinian corpuscle: a held press fires the fibre at onset and offset only; the onion gets the credit."""

    def construct(self):
        c = place(corpuscle(), -3.4, -0.5, 1.1)
        self.at("Press a")
        self.play(FadeIn(c), run_time=0.6)
        lbl = T("Pacinian corpuscle", 26, TEXT).move_to([-3.4, -2.8, 0])
        arr = press_arrow(-2.4, 3.0, 1.45)
        X0, X1 = 0.5, 6.0
        a, b = 1.9, 4.6
        ys, yi = 2.0, -0.7
        row1 = T("press", 24, ORANGE).move_to([X0 + 0.55, ys + 0.85, 0])
        row2 = T("impulses in the nerve fibre", 24, YELLOW).move_to([X0 + 2.0, yi + 1.3, 0])
        base1 = Line([X0, ys, 0], [X1, ys, 0], color=GREY, stroke_width=2)
        base2 = Line([X0, yi, 0], [X1, yi, 0], color=GREY, stroke_width=2)
        tlabel = T("time", 22, GREY).move_to([X1 - 0.3, yi + 0.35, 0])
        self.play(FadeIn(lbl), GrowArrow(arr), FadeIn(row1), Create(base1), run_time=0.6)
        sk1 = tag(SKETCH).move_to([5.0, 3.2, 0])
        self.at("and hold")
        self.add(sk1)
        step = poly([(X0, ys), (a, ys), (a, ys + 0.7), (b, ys + 0.7), (b, ys), (X1, ys)], ORANGE)
        self.play(Create(step), FadeIn(row2), Create(base2), FadeIn(tlabel), run_time=1.0)
        self.at("fires when the press starts")
        s1 = spike(a + 0.1, yi)
        self.play(Create(s1), run_time=0.4)
        self.at("when it ends")
        s2 = spike(b + 0.1, yi)
        self.play(Create(s2), run_time=0.4)
        self.at("It does not fire")
        none = T("no impulses during the hold", 24, GREY).move_to([(a + b) / 2 + 0.2, yi - 0.55, 0])
        self.play(FadeIn(none), run_time=0.4)
        self.at("wraps one nerve ending")
        self.play(Indicate(c.term, color=YELLOW, scale_factor=1.5), run_time=0.8)
        self.at("many concentric layers")
        ol = T("outer core: many layers", 22, INDIGO).move_to([-4.6, 2.55, 0])
        self.play(c.outer.animate.set_stroke(width=5), FadeIn(ol), run_time=0.5)
        self.at("got the credit")
        self.play(Indicate(c.outer, color=INDIGO, scale_factor=1.04), run_time=0.9)
        self.at("Was that right")
        q = T("?", 100, GOLD, weight=BOLD).move_to([-0.3, 0.4, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Filter(SpokenScene):
    """The 1966 model: fluid = viscosity, layers = elasticity; slow press dissipated, fast tap passes; high-pass sketch."""

    def construct(self):
        c = place(corpuscle(), -3.4, -0.3, 1.1)
        self.add(c)
        head = T("the 1966 model, Loewenstein and Skalak", 26, GREY).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        fl = T("fluid between layers: viscosity", 28, INDIGO).move_to([2.7, 2.0, 0])
        el = T("the layers: elasticity", 28, INDIGO).move_to([2.7, 1.1, 0])
        outer = c.outer
        pf = outer[1].point_from_proportion(0.0)
        pe = outer[3].point_from_proportion(0.0)
        l1 = lead(fl.get_left() + LEFT * 0.1, pf, INDIGO)
        l2 = lead(el.get_left() + LEFT * 0.1, pe, INDIGO)
        cap = T("the capsule: the layers", 28, INDIGO).move_to([2.7, 2.0, 0])
        lc_ = lead(cap.get_left() + LEFT * 0.1, outer[0].point_from_proportion(0.0), INDIGO)
        self.at("mechanical filter")
        self.play(FadeIn(cap), Create(lc_), run_time=0.6)
        self.at("modeled the capsule")
        self.play(Indicate(c.outer, color=INDIGO, scale_factor=1.04), run_time=0.9)
        self.at("fluid between the layers")
        self.play(FadeOut(cap), FadeOut(lc_), run_time=0.2)
        self.play(FadeIn(fl), Create(l1), run_time=0.6)
        self.at("The layers supply")
        self.play(FadeIn(el), Create(l2), run_time=0.6)
        self.at("A slow press")
        self.play(FadeOut(fl), FadeOut(el), FadeOut(l1), FadeOut(l2), run_time=0.4)
        top = c.get_top()[1]
        slow = fade_arrow(-3.4, top + 1.1, c.get_center()[1], n=8, w=9)
        sl = VGroup(T("slow press:", 30, ORANGE), T("dissipated before it", 30, ORANGE), T("reaches the core", 30, ORANGE)
                    ).arrange(DOWN, buff=0.15).move_to([2.2, 0.8, 0])
        self.play(Create(slow, lag_ratio=0.3), FadeIn(sl), run_time=1.6)
        self.at("A fast tap")
        self.play(FadeOut(slow), FadeOut(sl), run_time=0.3)
        fast = press_arrow(-3.4, top + 1.1, c.get_center()[1] + 0.15, w=10)
        fl2 = VGroup(T("fast tap:", 30, ORANGE), T("gets through", 30, ORANGE)).arrange(DOWN, buff=0.15).move_to([2.2, 0.8, 0])
        self.play(GrowArrow(fast), FadeIn(fl2), run_time=0.6)
        self.play(Indicate(c.term, color=YELLOW, scale_factor=1.5), run_time=0.7)
        self.at("decades this")
        self.play(FadeOut(fast), FadeOut(fl2), run_time=0.3)
        X0, X1, Y0, Y1 = 0.8, 5.8, -1.8, 1.4
        ax_x = Arrow([X0, Y0, 0], [X1 + 0.2, Y0, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        ax_y = Arrow([X0, Y0, 0], [X0, Y1 + 0.35, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        xs = np.linspace(-1.3, 1.3, 60)
        gain = lambda lf: 10 ** lf / np.sqrt(10 ** (2 * lf) + 1)
        pts = [(X0 + 0.15 + (x + 1.3) / 2.6 * (X1 - X0 - 0.35), Y0 + 0.1 + gain(x) * (Y1 - Y0 - 0.2)) for x in xs]
        curve = poly(pts, GREEN, 6)
        xl = T("slow to fast", 26, ORANGE).move_to([(X0 + X1) / 2 + 0.2, Y0 - 0.45, 0])
        yl = T("passed on", 26, GREEN).move_to([X0 + 0.9, Y1 + 0.6, 0])
        nm = T("high-pass filter", 32, TEXT, weight=BOLD).move_to([3.3, 2.7, 0])
        sk = tag(SKETCH).move_to([5.3, -3.15, 0])
        self.play(Create(ax_x), Create(ax_y), FadeIn(xl), FadeIn(yl), FadeIn(nm), FadeIn(sk), run_time=0.5)
        self.play(Create(curve), run_time=1.2)
        self.at("textbook explanation")
        self.play(Indicate(nm, color=GOLD, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cat(SpokenScene):
    """1965 isolated cat corpuscles: layers removed, generator potential lasts, one spike; two stages."""

    def construct(self):
        c = place(corpuscle(), -3.7, -0.2, 0.95)
        self.add(c)
        head = T("1965: isolated cat Pacinian corpuscles", 26, GREY).move_to([-2.6, 3.2, 0])
        self.play(FadeIn(head), run_time=0.5)
        self.at("removed most of the layers")
        self.play(*[FadeOut(c.outer[i]) for i in range(1, 5)], c.outer[0].animate.set_fill(INDIGO, 0).set_stroke(opacity=0.45),
                  run_time=1.3)
        rm = T("most layers removed", 24, RED).move_to([-3.7, -2.15, 0])
        self.play(FadeIn(rm), run_time=0.4)

        X0, X1 = -1.2, 6.1
        a, b = 1.9, 4.9
        y1, y2, y3 = 2.1, 0.4, -1.6
        for y, t_, col in ((y1, "press, held", ORANGE), (y2, "generator potential", GREEN), (y3, "impulses", YELLOW)):
            self.add(Line([X0, y, 0], [X1, y, 0], color=GREY, stroke_width=2))
            self.add(T(t_, 24, col).move_to([X0 + 1.55 if t_ != "press, held" else X0 + 1.0, y + 0.4, 0]))
        sk = tag(SKETCH).move_to([5.0, 3.2, 0])
        self.add(sk)
        arr = press_arrow(-3.7, 2.8, 1.15)
        self.at("held a press")
        self.play(GrowArrow(arr), Create(poly([(X0, y1), (a, y1), (a, y1 + 0.7), (b, y1 + 0.7), (b, y1), (X1, y1)], ORANGE)),
                  run_time=1.0)
        self.at("generator potential")
        gp = []
        for x in np.linspace(X0, X1, 90):
            if x < a:
                v = 0
            elif x < b:
                v = 0.95 * (1 - np.exp(-(x - a) / 0.2)) * (1 - 0.45 * (x - a) / (b - a))
            else:
                v = 0.95 * 0.55 * np.exp(-(x - b) / 0.25)
            gp.append((x, y2 + v * 0.8))
        ref = []
        for x in np.linspace(X0, X1, 90):
            if x < a:
                v = 0
            elif x < b:
                v = 0.95 * np.exp(-(x - a) / 0.35)
            else:
                v = 0
            ref.append((x, y2 + v * 0.8))
        refc = poly(ref, GREEN, 3).set_stroke(opacity=0.5)
        refl = T("layers on", 22, GREY).move_to([a + 0.15 + 0.9, y2 + 0.85, 0])
        self.play(Create(refc), FadeIn(refl), run_time=0.7)
        self.play(Create(poly(gp, GREEN)), run_time=1.2)
        self.at("much more slowly")
        bt = T("layers off: decays much more slowly", 24, TEXT).move_to([(a + b) / 2 + 0.3, y2 - 0.4, 0])
        self.play(FadeIn(bt), run_time=0.5)
        self.at("intense compression")
        bt2 = T("mainly under intense compression", 22, GREY).move_to([(a + b) / 2 + 0.3, y2 - 0.8, 0])
        self.play(FadeIn(bt2), run_time=0.5)
        self.at("single spike")
        sp = spike(a + 0.1, y3)
        self.play(Create(sp), run_time=0.5)
        self.at("two stages")
        st1 = T("1  mechanics around the ending", 24, INDIGO).move_to([-3.2, -3.1, 0])
        st2 = T("2  spike-generating membrane", 24, YELLOW).move_to([3.2, -3.1, 0])
        self.at("One lay in the mechanics")
        self.play(FadeIn(st1), Indicate(c.outer[0], color=INDIGO), run_time=0.8)
        self.at("The other lay")
        self.play(FadeIn(st2), Indicate(sp, color=YELLOW), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Duck(SpokenScene):
    """2025 duck Herbst corpuscle: pipette on the terminal, outer core removed, fast current and tuning stay."""

    def construct(self):
        c = place(corpuscle(), -3.6, -0.5, 1.05)
        self.add(c)
        head = T("2025: duck bill skin, late embryos, ex vivo", 26, GREY).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        nm = T("Herbst corpuscle (bird Pacinian)", 26, TEXT).move_to([-3.4, -2.75, 0])
        tip = c.term.get_right() + RIGHT * 0.05
        pip = Polygon(tip, tip + np.array([1.6, 0.35, 0]), tip + np.array([2.5, 1.9, 0]), tip + np.array([2.9, 1.75, 0]),
                      tip + np.array([2.0, 0.1, 0]), stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
        pl = T("pipette on the nerve terminal", 24, GREY).move_to(tip + np.array([2.2, 2.35, 0]))
        self.at("recorded directly")
        self.play(FadeIn(pip), FadeIn(pl), run_time=0.7)
        self.at("the bird version")
        self.play(FadeIn(nm), run_time=0.5)
        self.at("removed the outer core")
        self.play(*[FadeOut(c.outer[i]) for i in range(5)], run_time=1.3)
        X0, X1 = 1.4, 6.0
        yb = 0.3
        base = Line([X0, yb, 0], [X1, yb, 0], color=GREY, stroke_width=2)
        lab = T("transduction current", 26, GREEN).move_to([X0 + 1.7, yb + 0.9, 0])
        sk = tag(SKETCH).move_to([5.1, 3.2, 0])
        self.at("lamellar cells in place")
        ic = T("inner core: kept", 24, TEAL).move_to([-3.6, -1.55, 0])
        self.play(FadeIn(ic), c.inner.animate.set_stroke(width=5), run_time=0.6)
        self.at("The fast transduction current")
        self.play(Create(base), FadeIn(lab), FadeIn(sk), run_time=0.5)
        pts = [(X0, yb)]
        for x in np.linspace(X0, X1, 80):
            t = x - 2.4
            pts.append((x, yb - np.exp(-t / 0.22) * 1.1 if t >= 0 else yb))
        cur = poly(pts, GREEN, 6)
        self.play(Create(cur), run_time=1.0)
        res1 = T("fast kinetics: stayed", 28, TEXT).move_to([3.7, -1.2, 0])
        self.at("stayed")
        self.play(FadeIn(res1), run_time=0.4)
        self.at("frequency tuning")
        res2 = VGroup(T("frequency tuning:", 28, TEXT), T("no significant change", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([3.7, -2.4, 0])
        self.play(FadeIn(res2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Scope(SpokenScene):
    """Slower inactivation only as decapsulated terminals deteriorated; one reading of 1965; scope of the duck result."""

    def construct(self):
        X0, X1 = -6.0, 0.2
        yb = 1.9
        base = Line([X0, yb, 0], [X1, yb, 0], color=GREY, stroke_width=2)
        lab = T("transduction current, decapsulated duck terminal", 24, GREEN).move_to([-2.6, 3.1, 0])
        sk = tag(SKETCH).move_to([-0.9, -0.55, 0])
        self.at("Slower inactivation")
        self.play(Create(base), FadeIn(lab), FadeIn(sk), run_time=0.6)
        curves = []
        for tau, op in ((0.3, 1.0), (0.9, 0.7), (2.2, 0.45)):
            pts = [(X0, yb)]
            for x in np.linspace(X0, X1, 90):
                t = x - (X0 + 0.7)
                pts.append((x, yb - (np.exp(-t / tau) * 2.0 if t >= 0 else 0)))
            curves.append(poly(pts, GREEN, 6).set_stroke(opacity=op))
        self.play(Create(curves[0]), run_time=0.5)
        self.play(Create(curves[1]), run_time=0.5)
        self.play(Create(curves[2]), run_time=0.5)
        dt = VGroup(T("as the terminal deteriorates,", 28, TEXT), T("inactivation slows", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([-2.9, -1.6, 0])
        self.at("deteriorated")
        self.play(FadeIn(dt), run_time=0.5)
        self.at("a dying terminal")
        r1 = T("one reading of 1965:", 30, GOLD)
        r2 = T("a dying terminal looks like", 30, TEXT)
        r3 = T("a terminal that lost its filter", 30, TEXT)
        rr = VGroup(r1, r2, r3).arrange(DOWN, buff=0.22).move_to([3.4, 0.6, 0])
        self.play(FadeIn(rr, shift=UP * 0.1), run_time=0.8)
        self.at("Keep the scope")
        self.play(FadeOut(VGroup(base, lab, sk, dt, rr, *curves)), run_time=0.5)
        sc = T("the scope", 34, GOLD, weight=BOLD).move_to([0, 2.6, 0])
        self.play(FadeIn(sc), run_time=0.3)
        c1 = chip("a bird corpuscle", INDIGO, 30).move_to([-3.8, 1.1, 0])
        c2 = chip("ex vivo", GREY, 30).move_to([0.0, 1.1, 0])
        c3 = chip("late embryos", GREY, 30).move_to([3.6, 1.1, 0])
        self.at("bird corpuscle")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.4)
        self.at("ex vivo")
        self.play(FadeIn(c2, shift=UP * 0.1), FadeIn(c3, shift=UP * 0.1), run_time=0.5)
        self.at("does not show")
        n1 = T("not shown:", 34, RED, weight=BOLD).move_to([0, -0.6, 0])
        n2 = T("that the capsule does nothing", 36, TEXT).move_to([0, -1.5, 0])
        n3 = T("in a cat or a human hand", 36, TEXT).move_to([0, -2.3, 0])
        self.play(FadeIn(n1), run_time=0.3)
        self.play(FadeIn(VGroup(n2, n3), shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Cells(SpokenScene):
    """Lamellar cells feel force; depolarizing one drives the afferent, but 20 ms to 9 s vs a 5 ms cycle."""

    def construct(self):
        cx, cy = -3.0, 0.5
        top = Ellipse(width=4.0, height=1.1, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.15).move_to([cx, cy + 0.95, 0])
        bot = Ellipse(width=4.0, height=1.1, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.15).move_to([cx, cy - 0.95, 0])
        term = RoundedRectangle(corner_radius=0.15, width=2.0, height=0.5, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.9).move_to([cx, cy, 0])
        axon = Line([cx - 3.0, cy, 0], [cx - 1.0, cy, 0], color=YELLOW, stroke_width=7)
        name = T("duck Grandry corpuscle", 26, TEXT).move_to([cx, -2.8, 0])
        self.at("So what are the lamellar cells")
        lc = T("lamellar cell", 26, TEAL).move_to([cx - 1.5, cy + 1.95, 0])
        self.play(FadeIn(term), Create(axon), run_time=0.5)
        self.play(FadeIn(top), FadeIn(bot), FadeIn(lc), FadeIn(name), run_time=0.8)
        self.at("flattened cells wrap")
        self.play(Indicate(VGroup(top, bot), color=TEAL, scale_factor=1.04), run_time=0.8)
        tl = T("nerve terminal", 24, YELLOW).move_to([cx - 1.4, cy - 1.95, 0])
        self.play(FadeIn(tl), run_time=0.3)
        self.at("respond to force")
        fa = press_arrow(cx + 1.0, cy + 3.0, cy + 1.6, w=7)
        fl = T("force", 24, ORANGE).move_to([cx + 1.9, cy + 2.4, 0])
        self.play(GrowArrow(fa), FadeIn(fl), top.animate.set_fill(TEAL, 0.4), bot.animate.set_fill(TEAL, 0.4), run_time=0.7)
        self.at("Depolarizing one")
        self.play(FadeOut(fa), FadeOut(fl), bot.animate.set_fill(TEAL, 0.15), top.animate.set_fill(TEAL, 0.8), run_time=0.5)
        dep = T("depolarized", 24, TEAL).move_to([cx + 1.2, cy + 1.95, 0])
        link = DashedLine(top.get_bottom() + RIGHT * 0.5, term.get_top() + RIGHT * 0.5, color=TEAL, stroke_width=4)
        sp = spike(cx - 2.45, cy + 0.12, h=0.6, w=0.25)
        self.play(FadeIn(dep), Create(link), run_time=0.5)
        self.at("make its afferent fire")
        self.play(Create(sp), run_time=0.5)

        X0, X1, yb = 0.9, 5.7, -0.9
        self.at("the delay ran")
        axis = Line([X0, yb, 0], [X1, yb, 0], color=GREY, stroke_width=3)
        xmap = lambda ms: X0 + (np.log10(ms) / 4.0) * (X1 - X0)
        ticks = VGroup()
        for ms, txt in ((1, "1 ms"), (10, "10 ms"), (100, "100 ms"), (1000, "1 s"), (10000, "10 s")):
            ticks.add(Line([xmap(ms), yb - 0.1, 0], [xmap(ms), yb + 0.1, 0], color=GREY, stroke_width=3))
            ticks.add(T(txt, 22, GREY).move_to([xmap(ms), yb - 0.4, 0]))
        lat = Line([xmap(20), yb + 0.45, 0], [xmap(9000), yb + 0.45, 0], color=TEAL, stroke_width=14)
        lt = VGroup(T("in duck: lamellar cell", 24, TEAL), T("to afferent:", 24, TEAL), T("20 ms to about 9 s", 24, TEAL)
                    ).arrange(DOWN, buff=0.08).move_to([4.3, yb + 1.45, 0])
        lt2 = VGroup()
        self.play(Create(axis), FadeIn(ticks), run_time=0.5)
        self.play(Create(lat), FadeIn(lt), FadeIn(lt2), run_time=0.9)
        self.at("vibration repeats")
        cyc = Line([xmap(5), yb - 0.05, 0], [xmap(5), yb + 2.5, 0], color=YELLOW, stroke_width=5)
        ct = T("one cycle of 200 Hz: 5 ms", 24, YELLOW).move_to([xmap(5) + 1.95, yb + 2.95, 0])
        self.play(Create(cyc), FadeIn(ct), run_time=0.7)
        self.at("may set the")
        ms_ = VGroup(T("may set sensitivity,", 28, GOLD), T("not carry each cycle", 28, GOLD)).arrange(DOWN, buff=0.12).move_to([3.4, -2.5, 0])
        self.play(FadeIn(ms_), run_time=0.5)
        self.at("Keep this")
        self.play(FadeOut(VGroup(top, bot, lc, link, dep, tl, name, axis, ticks, lat, lt, lt2, cyc, ct, ms_, sp, axon)),
                  term.animate.move_to([0, 0.3, 0]).scale(1.5), run_time=0.8)
        bt = T("duck terminal, outer core gone", 34, YELLOW).move_to([0, 1.5, 0])
        bt2 = T("still adapts fast", 34, TEXT).move_to([0, -0.9, 0])
        self.at("outer core gone")
        self.play(FadeIn(bt), run_time=0.3)
        self.at("still adapts fast")
        self.play(FadeIn(bt2), Indicate(term, color=YELLOW), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "In duck, without the outer core, the terminal still adapts fast."
