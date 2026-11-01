"""Visual cortex: why a bar beats a spot  (Biochemistrypedia neuroscience explainer)

COLOR MAP (one colour per concept, whole film)
  BLUE   = the recorded cortical cell and its spikes (and the plotted tuning data)
  YELLOW = the light stimulus (spot, slit, bar, light patch)
  GREEN  = ON subregion / excitation / excitatory arrow / "firing changed" marker
  RED    = OFF subregion / inhibition
  PURPLE = complex cell
  ORANGE = measurement guides on the tuning plot (half height, width)
  GREY   = screen, outlines, structure, baseline, de-emphasized
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

SCR_C = np.array([-3.4, 0.1, 0.0])   # screen centre
SCR_W, SCR_H = 5.8, 4.4
STRIP_X0, STRIP_X1, STRIP_Y = 0.9, 6.2, -0.2
CELL_P = np.array([3.5, 2.0, 0.0])


def head(text):
    return T(text, 26, GREY).to_edge(UP, buff=0.35)


def screen(label=True):
    box = Rectangle(width=SCR_W, height=SCR_H, stroke_color=GREY, stroke_width=3,
                    fill_color=GREY, fill_opacity=0.08).move_to(SCR_C)
    g = VGroup(box)
    if label:
        g.add(T("screen in front of the cat", 22, GREY).next_to(box, DOWN, buff=0.18))
    return g


def cell_icon(color=BLUE, label="cortical cell"):
    soma = Circle(radius=0.34, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.3)
    parts = [soma]
    for ang in (150, 210, 90, 30):
        d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        parts.append(Line(d * 0.34, d * 0.85, color=color, stroke_width=3))
    parts.append(Line(DOWN * 0.34, DOWN * 0.95, color=color, stroke_width=3))
    g = VGroup(*parts).move_to(CELL_P)
    lbl = T(label, 24, color).next_to(g, LEFT, buff=0.3)
    return VGroup(g, lbl)


def electrode():
    tip = CELL_P + np.array([0.55, 0.25, 0])
    return VGroup(Line(tip + np.array([1.0, 1.0, 0]), tip, color=GREY, stroke_width=5),
                  T("electrode", 22, GREY).move_to(tip + np.array([1.55, 1.15, 0])))


def strip_base(label="spikes (schematic)"):
    base = Line([STRIP_X0, STRIP_Y, 0], [STRIP_X1, STRIP_Y, 0], color=GREY, stroke_width=2)
    lbl = T(label, 22, GREY).move_to([(STRIP_X0 + STRIP_X1) / 2, STRIP_Y - 0.5, 0])
    return VGroup(base, lbl)


def ticks(n, seed, color=BLUE, x0=STRIP_X0, x1=STRIP_X1, y=STRIP_Y, h=0.8):
    rng = np.random.default_rng(seed)
    xs = np.sort(x0 + 0.1 + (x1 - x0 - 0.2) * (np.arange(n) + rng.uniform(0.1, 0.9, n)) / max(n, 1))
    return VGroup(*[Line([x, y + 0.08, 0], [x, y + 0.08 + h, 0], color=color, stroke_width=4) for x in xs])


def show_ticks(scene, tk, t=0.7):
    if len(tk) == 0:
        return
    scene.play(LaggedStart(*[FadeIn(k, shift=UP * 0.08) for k in tk], lag_ratio=0.12), run_time=t)


def arrow_e(a, b):
    return Arrow(a, b, buff=0.08, color=GREEN, stroke_width=5, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45)


class S00Title(TitleCard):
    LESSON = "Visual Cortex"
    TITLE = "Why a bar beats a spot"


# ---------------------------------------------------------------------------------------------
class S01Spot(SpokenScene):
    def construct(self):
        hd = head("Anaesthetized cat · recording from visual cortex")
        scr = screen()
        cell = cell_icon()
        elec = electrode()
        base = strip_base()
        self.play(FadeIn(hd), FadeIn(scr), run_time=0.6)
        self.at("single cells")
        self.play(FadeIn(cell), Create(elec), Create(base), run_time=0.8)
        self.at("spots of light")
        spot = Circle(radius=0.28, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(SCR_C + LEFT * 0.4)
        spot_lbl = T("spot", 24, YELLOW).next_to(spot, DOWN, buff=0.25)
        self.play(FadeIn(spot, scale=0.5), FadeIn(spot_lbl), run_time=0.6)
        self.at("retina well")
        rchip = chip("retina: spots drive it well", GREEN, size=24).move_to([3.5, -1.65, 0])
        self.play(FadeIn(rchip), run_time=0.5)
        self.at("often did little")
        tk1 = ticks(3, 1)
        show_ticks(self, tk1, 0.6)
        cchip = chip("cortex: spot, little response", GREY, size=24).move_to([3.5, -2.45, 0])
        self.play(FadeIn(cchip), run_time=0.4)
        self.at("right orientation")
        bar = Rectangle(width=0.32, height=3.0, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(spot)
        bar_lbl = T("bar at the right orientation", 24, YELLOW).next_to(scr[0], UP, buff=-0.0).shift(DOWN * 0.0)
        bar_lbl = T("bar", 24, YELLOW).next_to(bar, RIGHT, buff=0.25)
        self.play(Transform(spot, bar), Transform(spot_lbl, bar_lbl), FadeOut(tk1), run_time=0.7)
        tk2 = ticks(16, 2)
        show_ticks(self, tk2, 1.0)
        cchip2 = chip("cortex: bar drives the cell hard", BLUE, size=24).move_to(cchip)
        self.play(Transform(cchip, cchip2), run_time=0.4)
        self.at("bar win")
        q = T("Why does the bar win?", 32, YELLOW, font=TITLE_FONT).move_to([3.5, -3.3, 0])
        self.play(Write(q), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Field(SpokenScene):
    def construct(self):
        hd = head("Receptive field")
        scr = screen()
        cell = cell_icon()
        elec = electrode()
        d1 = T("receptive field:", 24, GREEN, weight=BOLD)
        d2 = T("where a stimulus changes the cell's firing", 24, TEXT)
        dg = VGroup(d1, d2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.0, 0.6, 0])
        self.at("receptive field")
        self.play(FadeIn(hd), FadeIn(scr), FadeIn(dg, shift=UP * 0.1), run_time=0.6)
        self.at("electrode outside")
        self.play(FadeIn(cell), Create(elec), run_time=0.8)
        self.at("mapped each field")
        icons = VGroup(
            VGroup(Circle(radius=0.16, stroke_width=0, fill_color=YELLOW, fill_opacity=1), T("spot", 22, YELLOW)).arrange(RIGHT, buff=0.15),
            VGroup(Rectangle(width=0.08, height=0.6, stroke_width=0, fill_color=YELLOW, fill_opacity=1), T("slit", 22, YELLOW)).arrange(RIGHT, buff=0.15),
            VGroup(Rectangle(width=0.2, height=0.6, stroke_width=0, fill_color=YELLOW, fill_opacity=1), T("bar", 22, YELLOW)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.5).move_to([3.0, -0.8, 0])
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.1) for i in icons], lag_ratio=0.3), run_time=0.9)
        self.at("Moving a stimulus")
        field = Rectangle(width=2.2, height=1.5, stroke_width=0).move_to(SCR_C + np.array([-0.5, 0.5, 0]))
        spot = Circle(radius=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(SCR_C + np.array([-2.3, -1.6, 0]))
        self.play(FadeIn(spot), run_time=0.3)
        path = [(-2.3, 1.5), (-1.5, 0.5), (-0.5, 0.5), (0.5, 0.5), (1.0, -1.0), (-0.5, -1.0)]
        marks = VGroup()
        for px, py in path:
            p = SCR_C + np.array([px, py, 0])
            self.play(spot.animate.move_to(p), run_time=0.25)
            inside = abs(px + 0.5) <= 1.1 and abs(py - 0.5) <= 0.75
            m = Circle(radius=0.11, stroke_width=0, fill_color=GREEN if inside else GREY, fill_opacity=1).move_to(p)
            marks.add(m)
            self.add(m)
        self.play(FadeOut(spot), run_time=0.3)
        leg = VGroup(
            VGroup(Circle(radius=0.11, stroke_width=0, fill_color=GREEN, fill_opacity=1), T("firing changed", 22, GREEN)).arrange(RIGHT, buff=0.15),
            VGroup(Circle(radius=0.11, stroke_width=0, fill_color=GREY, fill_opacity=1), T("no change", 22, GREY)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.5).move_to([3.0, -2.2, 0])
        self.play(FadeIn(leg), run_time=0.4)
        self.at("where the field lies")
        outline = DashedVMobject(Rectangle(width=2.5, height=1.8, stroke_color=GREEN, stroke_width=4).move_to(field), num_dashes=40)
        olbl = T("receptive field", 24, GREEN).next_to(outline, UP, buff=0.1)
        self.play(Create(outline), FadeIn(olbl), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def on_off_map():
    on = Rectangle(width=1.0, height=3.6, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.28)
    off = Rectangle(width=1.0, height=3.6, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.28)
    on.move_to(SCR_C + LEFT * 0.5)
    off.move_to(SCR_C + RIGHT * 0.5)
    on_l = T("ON", 28, GREEN, weight=BOLD).move_to(on.get_top() + DOWN * 0.4)
    off_l = T("OFF", 28, RED, weight=BOLD).move_to(off.get_top() + DOWN * 0.4)
    return VGroup(on, off, on_l, off_l), on, off


class S03Simple(SpokenScene):
    def construct(self):
        hd = head("Simple cell · cat visual cortex")
        scr = screen(label=False)
        cell = cell_icon("#58C4DD", "simple cell")
        base = strip_base()
        self.play(FadeIn(hd), FadeIn(scr), FadeIn(cell), Create(base), run_time=0.7)
        self.at("simple cell")
        mp, on, off = on_off_map()
        self.play(FadeIn(mp), run_time=0.8)
        self.at("side by side")
        self.play(Indicate(VGroup(on, off), color=TEXT, scale_factor=1.04), run_time=0.8)
        self.at("excites the cell")
        patch = Rectangle(width=0.8, height=1.2, stroke_width=0, fill_color=YELLOW, fill_opacity=0.75).move_to(on.get_center() + DOWN * 0.3)
        state = chip("light on ON: excites", GREEN, size=26).move_to([3.5, -2.2, 0])
        self.play(FadeIn(patch), FadeIn(state), run_time=0.4)
        tk = ticks(16, 3)
        show_ticks(self, tk, 0.9)
        self.at("inhibits it")
        newstate = chip("light on OFF: inhibits", RED, size=26).move_to(state)
        self.play(FadeOut(tk), patch.animate.move_to(off.get_center() + DOWN * 0.3), Transform(state, newstate), run_time=0.7)
        self.at("removing that light")
        newstate = chip("light removed: excites", GREEN, size=26).move_to(state)
        self.play(FadeOut(patch), Transform(state, newstate), run_time=0.4)
        tk = ticks(12, 4)
        show_ticks(self, tk, 0.8)
        self.at("tended to cancel")
        both = Rectangle(width=2.0, height=1.2, stroke_width=0, fill_color=YELLOW, fill_opacity=0.75).move_to(SCR_C + DOWN * 0.3)
        newstate = chip("light on both: tends to cancel", GREY, size=26).move_to(state)
        self.play(FadeOut(tk), FadeIn(both), Transform(state, newstate), run_time=0.5)
        tk = ticks(3, 5)
        show_ticks(self, tk, 0.6)
        self.finish()


class S04Angle(SpokenScene):
    def construct(self):
        hd = head("Simple cell · does the bar's angle matter?")
        scr = screen(label=False)
        cell = cell_icon("#58C4DD", "simple cell")
        base = strip_base()
        mp, on, off = on_off_map()
        self.add(hd, scr, cell, base, mp)
        self.wait(0.3)
        self.at("elongated")
        self.play(Indicate(VGroup(on, off), color=TEXT, scale_factor=1.04), run_time=0.8)
        self.at("aligned with")
        bar = Rectangle(width=0.3, height=2.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85).move_to(on.get_center())
        state = chip("bar along the ON strip", GREEN, size=26).move_to([3.5, -2.2, 0])
        self.play(FadeIn(bar), FadeIn(state), run_time=0.5)
        tk = ticks(16, 6)
        show_ticks(self, tk, 0.9)
        self.at("across the strip")
        newstate = chip("bar across the strip: barely", GREY, size=26).move_to(state)
        self.play(FadeOut(tk), bar.animate.move_to(SCR_C), Transform(state, newstate), run_time=0.4)
        self.play(Rotate(bar, angle=-PI / 2, about_point=bar.get_center()), run_time=0.7)
        tk = ticks(3, 7)
        show_ticks(self, tk, 0.6)
        self.at("Turn the bar")
        newstate = chip("turn the bar: response changes", YELLOW, size=26).move_to(state)
        self.play(FadeOut(tk), Transform(state, newstate), Rotate(bar, angle=PI / 2, about_point=bar.get_center()), run_time=0.8)
        self.play(bar.animate.move_to(on.get_center()), run_time=0.4)
        tk = ticks(16, 8)
        show_ticks(self, tk, 0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
RATES = [(0, 2), (30, 6), (60, 24), (90, 40), (120, 22), (150, 5)]


class S05Tuning(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[0, 150, 30], y_range=[0, 45, 10], x_length=6.6, y_length=4.4, tips=False,
                  axis_config={"color": GREY, "include_ticks": True, "include_numbers": False, "stroke_width": 3})
        ax.move_to([-2.55, -0.2, 0])
        labels = VGroup()
        for x in range(0, 151, 30):
            labels.add(M(str(x), 22, GREY).next_to(ax.c2p(x, 0), DOWN, buff=0.15))
        for y in range(0, 41, 10):
            labels.add(M(str(y), 22, GREY).next_to(ax.c2p(0, y), LEFT, buff=0.15))
        xl = T("bar orientation (degrees)", 24, GREY).next_to(ax, DOWN, buff=0.55)
        yl = T("spikes/s", 24, GREY).next_to(ax.c2p(0, 45), UP, buff=0.12).align_to(ax.c2p(0, 45), LEFT)
        X0 = 1.8   # left edge of the callout column
        tag = T("made-up recording", 24, YELLOW)
        note = T("best bar position, many trials", 24, TEXT)
        s_lbl = T("no bar: 2 spikes/s", 24, GREY)
        pk = T("peak: 90\u00b0, 40 spikes/s", 24, BLUE, weight=BOLD)
        hlbl = T("half height: 21 spikes/s", 24, ORANGE)
        wlbl = T("about 67\u00b0 wide (interpolated)", 24, ORANGE)
        f1 = T("orientation index", 24, TEXT, weight=BOLD)
        f2 = M("(40 \u2212 2) / (40 + 2)", 24, TEXT)
        f3 = M("= 0.90", 28, GREEN)
        f4 = T("orthogonal = 0\u00b0, 90\u00b0 from the peak", 22, GREY)
        col1 = VGroup(tag, note, s_lbl, pk, hlbl, wlbl).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        col1.move_to([0, 0, 0]).align_to([X0, 0, 0], LEFT).to_edge(UP, buff=0.35)
        fg = VGroup(f1, f2, f3, f4).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fg.align_to([X0, 0, 0], LEFT).align_to([0, -0.5, 0], UP)
        self.play(FadeIn(ax), FadeIn(labels), FadeIn(xl), FadeIn(yl), FadeIn(tag), run_time=0.8)
        self.at("recording from")
        self.wait(0.1)
        self.at("best position")
        self.play(FadeIn(note), run_time=0.4)
        self.at("no bar")
        spont = DashedLine(ax.c2p(0, 2), ax.c2p(150, 2), color=GREY, stroke_width=3)
        self.play(Create(spont), FadeIn(s_lbl), run_time=0.5)
        self.at("orientations draw")
        dots, segs = VGroup(), VGroup()
        pts = [ax.c2p(x, y) for x, y in RATES]
        for i, p in enumerate(pts):
            d = Dot(p, radius=0.1, color=BLUE)
            anims = [FadeIn(d, scale=0.5)]
            if i:
                s = Line(pts[i - 1], p, color=BLUE, stroke_width=4)
                segs.add(s)
                anims = [Create(s)] + anims
            dots.add(d)
            self.play(*anims, run_time=0.2)
        self.at("tuning curve")
        self.play(Indicate(segs, color=BLUE, scale_factor=1.0), run_time=0.5)
        self.at("best orientation")
        self.play(Indicate(dots[3], color=TEXT, scale_factor=1.8), FadeIn(pk), run_time=0.6)
        self.at("half height")
        hh = DashedLine(ax.c2p(0, 21), ax.c2p(150, 21), color=ORANGE, stroke_width=3)
        x_lo, x_hi = 55.0, 121.8
        br = Line(ax.c2p(x_lo, 21), ax.c2p(x_hi, 21), color=ORANGE, stroke_width=7)
        e1 = Line(ax.c2p(x_lo, 21) + DOWN * 0.15, ax.c2p(x_lo, 21) + UP * 0.15, color=ORANGE, stroke_width=5)
        e2 = Line(ax.c2p(x_hi, 21) + DOWN * 0.15, ax.c2p(x_hi, 21) + UP * 0.15, color=ORANGE, stroke_width=5)
        self.play(Create(hh), FadeIn(hlbl), run_time=0.7)
        self.at("about")
        self.play(Create(br), Create(e1), Create(e2), FadeIn(wlbl), run_time=0.8)
        self.at("orientation index")
        self.play(FadeIn(fg, shift=UP * 0.1), run_time=0.8)
        self.at("strong preference")
        f5 = T("strong preference for the best", 22, GREEN)
        f6 = T("orientation over the orthogonal one;", 22, GREEN)
        f7 = T("not the tuning width", 22, GREEN)
        g5 = VGroup(f5, f6, f7).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(fg, DOWN, buff=0.3).align_to(fg, LEFT)
        self.play(Indicate(f3, color=GREEN), FadeIn(g5), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Complex(SpokenScene):
    def construct(self):
        hd = head("Complex cell · cat visual cortex")
        scr = screen(label=False)
        cell = cell_icon(PURPLE, "complex cell")
        base = strip_base()
        self.play(FadeIn(hd), FadeIn(scr), FadeIn(cell), Create(base), run_time=0.6)
        fld = DashedVMobject(Rectangle(width=4.6, height=3.4, stroke_color=PURPLE, stroke_width=3).move_to(SCR_C), num_dashes=50)
        flbl = T("receptive field", 22, PURPLE).next_to(fld, UP, buff=-0.45).shift(DOWN * 0.0)
        flbl.move_to(SCR_C + UP * 1.45)
        self.play(Create(fld), FadeIn(flbl), run_time=0.6)
        self.at("tolerate position")
        bar = Rectangle(width=0.3, height=2.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to(SCR_C + LEFT * 1.5)
        state = chip("same bar angle, new position", PURPLE, size=26).move_to([3.5, -2.4, 0])
        self.play(FadeIn(bar), FadeIn(state), run_time=0.4)
        tk = ticks(14, 9, color=PURPLE)
        show_ticks(self, tk, 0.6)
        for i, dx in enumerate([0.0, 1.5]):
            self.play(FadeOut(tk), bar.animate.move_to(SCR_C + RIGHT * dx), run_time=0.45)
            tk = ticks(14, 10 + i, color=PURPLE)
            show_ticks(self, tk, 0.6)
        self.at("No separate")
        nm = T("no separate ON and OFF regions", 24, TEXT).move_to([3.5, -3.2, 0])
        self.play(FadeIn(nm), run_time=0.6)
        self.at("suggested that geniculate")
        # switch to the proposed wiring: boxes and typed arrows
        self.play(*[FadeOut(m) for m in (scr, fld, flbl, bar, tk, base, nm, state, cell, hd)], run_time=0.6)
        hd2 = head("Proposed wiring (Hubel and Wiesel, 1962)")
        lgn = VGroup(*[chip("LGN cell", GREY, size=32) for _ in range(3)]).arrange(DOWN, buff=0.6).move_to([-3.3, -0.2, 0])
        simple = chip("simple cell", BLUE, size=34).move_to([2.0, -0.2, 0])
        arrows = VGroup(*[arrow_e(l.get_right(), simple.get_left() + UP * (0.15 * (1 - i))) for i, l in enumerate(lgn)])
        leg = VGroup(Line(ORIGIN, RIGHT * 0.7, color=GREEN, stroke_width=5), T("excitatory", 22, GREEN)).arrange(RIGHT, buff=0.2).move_to([-3.3, -3.0, 0])
        self.play(FadeIn(hd2), LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in lgn], lag_ratio=0.25), run_time=1.0)
        self.play(FadeIn(simple), LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), FadeIn(leg), run_time=1.0)
        self.at("simple cells converge")
        # relabel stage 1 into stage 2: simple cells -> complex cell
        lgn2 = VGroup(*[chip("simple cell", BLUE, size=32) for _ in range(3)]).arrange(DOWN, buff=0.6).move_to(lgn)
        cx = chip("complex cell", PURPLE, size=34).move_to(simple)
        note = T("same orientation, different positions", 24, GREY).move_to([-1.9, 2.55, 0])
        self.play(*[Transform(a, b) for a, b in zip(lgn, lgn2)], Transform(simple, cx), FadeIn(note), run_time=1.0)
        self.at("proposal")
        prop = chip("1962 proposal; step one later supported", YELLOW, size=28).move_to([2.6, 1.7, 0])
        self.play(FadeIn(prop), run_time=0.5)
        self.at("Keep the rule")
        rule = T("In cat visual cortex, bars at the right angle drive cells that spots often miss.", 26, TEXT)
        fit(rule, max_w=12.0)
        rule.move_to([0, -3.0, 0])
        self.play(FadeOut(leg), FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Bars at the right angle drive cells that spots often miss."
