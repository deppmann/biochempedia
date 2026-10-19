"""The Retina: light turns the receptor off, and the retina reads that silence two ways.
(Biochemistrypedia neuroscience explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = light (the arrow, the "light on" bar, the photon)
  BLUE   = the photoreceptor and the dark current (sodium, calcium, cations entering a cell)
  TEAL   = glutamate (the dots crossing a synapse)
  PURPLE = cGMP
  ORANGE = the phototransduction chain and the G protein (rhodopsin, transducin, PDE6, Go)
  GREEN  = ON pathway (ON bipolar cell, ON ganglion cell, mGluR6)
  PINK   = OFF pathway (OFF bipolar cell, OFF ganglion cell, AMPA / kainate)
  RED    = inhibitory arrow (T-bar): one style for every "keeps it shut" or "inverts the sign"
  GOLD   = the retina's output (the ganglion cells)
  GREY   = membranes, closed channels, outlines, de-emphasised text
Arrow types: solid arrow = excitatory / drives; T-bar = inhibitory.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E879A8"
LIGHT = YELLOW
GLU = TEAL


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
class Flow(VGroup):
    """Dots that travel p0 -> p1 for ever. `gain` (a ValueTracker, 0..1) sets how visible the stream is."""

    def __init__(self, p0, p1, n=4, color=TEAL, r=0.1, speed=0.5, gain=1.0):
        super().__init__()
        self.p0, self.p1 = np.array(p0, float), np.array(p1, float)
        self.speed, self._tt, self._n = speed, 0.0, n
        self.gain = ValueTracker(gain)
        for _ in range(n):
            self.add(Dot(radius=r, color=color))
        self._place(0)
        self.add_updater(lambda m, dt: m._place(dt))

    def _place(self, dt):
        self._tt += dt * self.speed
        g = self.gain.get_value()
        for i, d in enumerate(self.submobjects):
            ph = (self._tt + i / self._n) % 1
            d.move_to(self.p0 + (self.p1 - self.p0) * ph)
            d.set_fill(opacity=g * min(1, ph * 6, (1 - ph) * 6))


class Channel(VGroup):
    """Two blocks in a membrane with a gap between them. gap tracker 0 = closed (grey), >= 0.4 = open (colour)."""

    def __init__(self, cx, cy, gap, color=BLUE, w=0.5, h=0.5, hole_h=0.14):
        super().__init__()
        self.cx, self.cy, self.w, self.color, self.gap = cx, cy, w, color, gap
        self.hole = Rectangle(width=0.01, height=hole_h, stroke_width=0, fill_color=BG, fill_opacity=1)
        self.l = RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_width=3)
        self.r = RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_width=3)
        self.add(self.hole, self.l, self.r)
        self._sync()
        self.add_updater(lambda m: m._sync())

    def _sync(self):
        g = self.gap.get_value()
        self.l.move_to([self.cx - g / 2 - self.w / 2, self.cy, 0])
        self.r.move_to([self.cx + g / 2 + self.w / 2, self.cy, 0])
        self.hole.stretch_to_fit_width(max(g, 0.01)).move_to([self.cx, self.cy, 0])
        c = interpolate_color(ManimColor(GREY), ManimColor(self.color), float(min(1, g / 0.4)))
        for b in (self.l, self.r):
            b.set_stroke(c).set_fill(c, 0.4)


def bchip(text, color=BLUE, size=24, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dimc(c, o=0.35):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def lit(c, color):
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tbar(a, b, color=RED, w=5):
    """inhibitory arrow: a line ending in a bar."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def make_rod(x, y_bot, s=1.0):
    """A rod as a simple cell: terminal on top, inner segment, outer segment (with discs) at the bottom."""
    ow, oh = 0.95 * s, 2.3 * s
    os_ = RoundedRectangle(corner_radius=0.12 * s, width=ow, height=oh, stroke_color=BLUE, stroke_width=3,
                           fill_color=BLUE, fill_opacity=0.22).move_to([x, y_bot + oh / 2, 0])
    discs = VGroup(*[Line([x - ow / 2 + 0.08 * s, y_bot + 0.22 * s + i * (oh - 0.44 * s) / 6, 0],
                          [x + ow / 2 - 0.08 * s, y_bot + 0.22 * s + i * (oh - 0.44 * s) / 6, 0],
                          stroke_color=BLUE, stroke_width=2, stroke_opacity=0.55) for i in range(7)])
    ih = 1.35 * s
    inner = RoundedRectangle(corner_radius=0.3 * s, width=1.15 * s, height=ih, stroke_color=BLUE, stroke_width=3,
                             fill_color=BLUE, fill_opacity=0.14).move_to([x, y_bot + oh + 0.1 * s + ih / 2, 0])
    th = 0.62 * s
    term = RoundedRectangle(corner_radius=0.2 * s, width=1.5 * s, height=th, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.14).move_to([x, inner.get_top()[1] + 0.1 * s + th / 2, 0])
    g = VGroup(os_, discs, inner, term)
    g.os_, g.inner, g.term = os_, inner, term
    return g


def bip_cell(x, y, w, h, color):
    return Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.14).move_to([x, y, 0])


def state_tag(text, color, pos=(4.4, 3.2), size=34):
    return T(text, size, color, weight=BOLD).move_to([pos[0], pos[1], 0])


# --- the shared sketch trace (bipolar-cell voltage, relative units) ------------------------------
PX0, PX1, PYM = 1.3, 6.4, -0.05     # panel left, right, baseline (dark level)
T_ON = 0.4                          # light comes on at 40% of the time axis


def px(t):
    return PX0 + 0.15 + t * (PX1 - PX0 - 0.3)


def panel_frame():
    title = T("bipolar cell voltage", 26, TEXT).move_to([3.85, 2.45, 0])
    sub = T("in this sketch, relative units", 22, GREY).move_to([3.85, 2.0, 0])
    yax = Line([PX0, PYM - 1.55, 0], [PX0, PYM + 1.5, 0], color=GREY, stroke_width=3)
    base = DashedLine([PX0, PYM, 0], [PX1, PYM, 0], color=GREY, stroke_width=2.5, dash_length=0.14)
    up = T("more depolarized", 22, GREY).move_to([PX0 + 0.2 + 1.2, PYM + 1.5, 0])
    dn = T("more hyperpolarized", 22, GREY).move_to([PX0 + 0.2 + 1.45, PYM - 1.55, 0])
    dk = T("dark level", 22, GREY).move_to([PX1 - 0.75, PYM + 0.28, 0])
    return VGroup(title, sub, yax, base, up, dn, dk)


def sketch_curve(sign, color, amp=0.95, tau=0.13):
    ts = np.linspace(0, 1, 140)
    ys = np.array([0.0 if t < T_ON else sign * amp * (1 - np.exp(-(t - T_ON) / tau)) for t in ts])
    pts = [[px(t), PYM + y, 0] for t, y in zip(ts, ys)]
    c = VMobject(color=color, stroke_width=6)
    c.set_points_as_corners(pts)
    return c


def light_bar(y=-2.55):
    ln = Line([px(T_ON), y, 0], [PX1 - 0.15, y, 0], color=LIGHT, stroke_width=9)
    lab = T("light on", 22, LIGHT).next_to(ln, DOWN, buff=0.12)
    return VGroup(ln, lab)


class S00Title(TitleCard):
    LESSON = "The retina"
    TITLE = "Light turns the receptor off"


# ---------------------------------------------------------------------------------------------
class S01Dark(SpokenScene):
    """a receptor excited by its stimulus, then a rod turned off by light; the question in the picture."""

    def construct(self):
        # opening contrast: ordinary receptor vs photoreceptor
        stim = arr([-5.2, 0.2, 0], [-3.2, 0.2, 0], YELLOW)
        stim_l = T("stimulus", 28, YELLOW).next_to(stim, UP, buff=0.15)
        rec = chip("sensory receptor", BLUE, size=30).move_to([-0.8, 0.2, 0])
        st = T("excited", 34, GREEN, weight=BOLD).move_to([4.3, 0.2, 0])
        a2 = arr([1.9, 0.2, 0], [2.7, 0.2, 0], GREY, tip=0.2)
        self.play(FadeIn(stim, shift=RIGHT * 0.3), FadeIn(stim_l), FadeIn(rec), run_time=0.8)
        self.play(FadeIn(a2), FadeIn(st), run_time=0.5)
        self.at("Vertebrate photoreceptors")
        rec2 = chip("photoreceptor", BLUE, size=30).move_to(rec)
        st2 = T("turned off", 34, GREY, weight=BOLD).move_to(st)
        stim2 = arr([-5.2, 0.2, 0], [-3.2, 0.2, 0], LIGHT)
        stim2_l = T("light", 28, LIGHT).next_to(stim2, UP, buff=0.15)
        self.play(ReplacementTransform(rec, rec2), ReplacementTransform(st, st2), ReplacementTransform(stim, stim2),
                  ReplacementTransform(stim_l, stim2_l), run_time=0.8)
        self.at("A rod sitting")
        self.play(FadeOut(VGroup(rec2, st2, stim2, stim2_l, a2)), run_time=0.4)

        # the rod in the dark
        rod = make_rod(-0.6, -3.5, 1.1)
        box = chip("?", GREY, size=44, pad=0.3).move_to([-0.6, 2.95, 0])
        dark = state_tag("DARK", GREY)
        self.play(FadeIn(rod), FadeIn(dark), run_time=0.7)
        cur = Flow([-3.7, -2.235, 0], [-1.2, -2.235, 0], n=4, color=BLUE, r=0.11, gain=0)
        cur_l = T("current in", 28, BLUE).move_to([-2.5, -1.6, 0])
        glu = Flow([-0.6, 1.5, 0], [-0.6, 2.5, 0], n=4, color=GLU, r=0.11, gain=0)
        glu_l = T("releasing glutamate", 28, GLU).move_to([2.1, 2.0, 0])
        dep = T("depolarized", 28, BLUE).move_to([1.6, -0.1, 0])
        self.add(cur, glu)
        self.at("depolarized")
        self.play(FadeIn(dep), run_time=0.3)
        self.at("Current flows")
        self.play(cur.gain.animate.set_value(1), FadeIn(cur_l), run_time=0.5)
        self.at("releases glutamate")
        self.play(FadeIn(box), glu.gain.animate.set_value(1), FadeIn(glu_l), run_time=0.6)
        self.at("Light makes")
        beam = arr([4.2, -2.235, 0], [0.0, -2.235, 0], LIGHT, w=7, tip=0.3)
        beam_l = T("light", 28, LIGHT).next_to(beam, UP, buff=0.12).shift(RIGHT * 1.2)
        lt = state_tag("LIGHT", LIGHT)
        self.play(GrowArrow(beam), FadeIn(beam_l), ReplacementTransform(dark, lt), run_time=0.6)
        self.play(cur.gain.animate.set_value(0), glu.gain.animate.set_value(0), FadeOut(cur_l), FadeOut(glu_l),
                  FadeOut(dep), run_time=0.7)
        self.at("How does")
        self.play(Indicate(box, color=TEXT, scale_factor=1.12), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Off(SpokenScene):
    """cGMP holds CNG channels open (dark current); photon -> rhodopsin -> transducin -> PDE6 -> cGMP gone -> channels close."""

    def construct(self):
        BX0, BX1, BY = -6.2, 2.4, 0.9
        bar = RoundedRectangle(corner_radius=0.1, width=BX1 - BX0, height=0.34, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([(BX0 + BX1) / 2, BY, 0])
        out_l = T("outside", 24, GREY).move_to([-5.3, 1.55, 0])
        in_l = T("inside the outer segment", 24, GREY).move_to([-3.9, 0.35, 0])
        gap = ValueTracker(0.0)
        cxs = [-4.4, -2.0, 0.4]
        chans = [Channel(cx, BY, gap, BLUE) for cx in cxs]
        cng = T("CNG channels", 26, BLUE).move_to([2.0, 1.5, 0])
        self.at("In darkness")
        self.play(FadeIn(bar), FadeIn(out_l), FadeIn(in_l), run_time=0.3)
        self.add(*chans)
        self.play(gap.animate.set_value(0.5), FadeIn(cng), run_time=0.4)

        # cGMP holds them open
        gdots = VGroup(*[Dot(radius=0.13, color=PURPLE).move_to([cx + dx, -0.5 + dy, 0])
                         for cx in cxs for dx, dy in [(-0.45, 0.0), (0.45, -0.18)]])
        g_l = T("cGMP", 28, PURPLE, weight=BOLD).move_to([-5.7, -0.95, 0])
        self.at("cyclic")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in gdots], lag_ratio=0.1), FadeIn(g_l), run_time=0.8)

        # sodium and calcium flow in
        ions = [Flow([cx, 3.1, 0], [cx, 0.3, 0], n=3, color=BLUE, r=0.1, speed=0.4, gain=0) for cx in cxs]
        self.add(*ions)
        na = chip("Na⁺", BLUE, size=26).move_to([-5.9, 3.0, 0])
        ca = chip("Ca²⁺", BLUE, size=26).move_to([-4.75, 3.0, 0])
        self.at("Sodium and calcium")
        self.play(FadeIn(na), FadeIn(ca), *[f.gain.animate.set_value(1) for f in ions], run_time=0.6)
        self.at("steady dark current")
        dc = T("dark current", 28, BLUE, weight=BOLD).move_to([2.7, 2.2, 0])
        self.play(FadeOut(cng), FadeIn(dc), run_time=0.4)

        # the readout on the right
        mt = Rectangle(width=0.7, height=3.2, stroke_color=GLU, stroke_width=3, fill_color=GLU, fill_opacity=0.5)
        mt.move_to([4.9, -0.7, 0])
        m_l = T("glutamate", 26, GLU).move_to([4.9, 1.85, 0])
        m_l2 = T("release", 26, GLU).next_to(m_l, DOWN, buff=0.08)
        vm = T("depolarized", 28, BLUE, weight=BOLD).move_to([4.9, -2.85, 0])
        self.at("keeps the rod")
        self.play(FadeIn(vm), run_time=0.3)
        self.at("so it releases")
        self.play(FadeIn(mt), FadeIn(m_l), FadeIn(m_l2), run_time=0.5)

        # photon -> rhodopsin
        rho = bchip("rhodopsin", ORANGE, size=26).move_to([-5.1, -2.35, 0])
        photon = Dot(radius=0.2, color=LIGHT).move_to([-6.3, -3.4, 0])
        ph_l = T("photon", 26, LIGHT).next_to(photon, DOWN, buff=0.1).shift(RIGHT * 0.3)
        self.at("Now a photon")
        self.play(FadeIn(rho), FadeIn(photon), FadeIn(ph_l), run_time=0.5)
        self.at("absorbed by")
        self.play(photon.animate.move_to(rho.get_left() + LEFT * 0.12), run_time=0.4)
        self.play(FadeOut(photon), FadeOut(ph_l), *lit(rho, ORANGE), Flash(rho, color=LIGHT, flash_radius=0.7), run_time=0.5)

        # transducins (many)
        tds = VGroup(*[bchip("transducin", ORANGE, size=22).move_to([-2.2, y, 0]) for y in (-1.5, -2.4, -3.3)])
        a1 = arr(rho.get_right(), [-3.35, -2.4, 0], ORANGE)
        self.at("activates many")
        self.play(GrowArrow(a1), LaggedStart(*[FadeIn(t, scale=0.8) for t in tds], lag_ratio=0.2), run_time=0.8)

        # PDE6
        pde = bchip("PDE6", ORANGE, size=26).move_to([1.1, -2.4, 0])
        a2 = arr([-0.95, -2.4, 0], pde.get_left(), ORANGE)
        self.at("Transducin activates")
        self.play(GrowArrow(a2), FadeIn(pde, scale=0.8), run_time=0.6)
        self.at("which breaks down")
        a3 = arr(pde.get_top(), [1.1, -0.95, 0], PURPLE)
        self.play(GrowArrow(a3), run_time=0.3)
        self.play(*[FadeOut(d, scale=0.3) for d in gdots], FadeOut(g_l), run_time=0.7)

        # channels close
        self.at("The channels close")
        self.play(gap.animate.set_value(0.0), *[f.gain.animate.set_value(0) for f in ions], run_time=0.8)
        self.at("dark current shrinks")
        self.play(FadeOut(dc), FadeOut(na), FadeOut(ca), run_time=0.4)
        vm2 = T("hyperpolarized", 28, GREY, weight=BOLD).move_to([4.9, -2.85, 0])
        self.at("The rod hyperpolarizes")
        self.play(ReplacementTransform(vm, vm2), run_time=0.4)
        self.at("release falls")
        self.play(mt.animate.stretch_to_fit_height(0.45).move_to([4.9, -2.1, 0]), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def closeup(kind):
    """The big picture of one bipolar cell facing the rod terminal. kind 'off' or 'on'."""
    CX = -3.3
    col = PINK if kind == "off" else GREEN
    term = RoundedRectangle(corner_radius=0.2, width=4.8, height=0.9, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.14).move_to([CX, -3.05, 0])
    tl = T("rod terminal", 24, BLUE).move_to(term)
    cell = RoundedRectangle(corner_radius=0.9, width=4.8, height=3.9, stroke_color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.12).move_to([CX, 0.75, 0])
    name = T(f"{kind.upper()} bipolar cell", 28, col, weight=BOLD).move_to([CX, 2.2, 0])
    glu_l = T("glutamate", 24, GLU).move_to([CX + 3.35, -1.95, 0])
    d = {"CX": CX, "col": col, "base": VGroup(term, tl, cell, name, glu_l)}
    # glutamate crossing the cleft, three columns
    d["glu"] = [Flow([CX + dx, -2.5, 0], [CX + dx, -1.3, 0], n=2, color=GLU, r=0.1, speed=0.45, gain=0) for dx in (-1.6, 0.0, 1.6)]
    d["gap"] = ValueTracker(0.0)
    return d


def curve_label(text, color, pos):
    return T(text, 26, color, weight=BOLD).move_to(pos)


class S03Split(SpokenScene):
    """one transmitter, two kinds of bipolar cell; then the OFF cell up close."""

    def construct(self):
        # --- phase 1: rod and two bipolar cells ------------------------------------------------
        rod = make_rod(0.0, -3.4, 0.95)
        top_y = rod.term.get_top()[1]
        cl = bip_cell(-1.75, 2.3, 3.0, 2.3, GREY)
        cr = bip_cell(1.75, 2.3, 3.0, 2.3, GREY)
        cl_t = T("bipolar cell", 22, GREY).move_to([-1.75, 2.93, 0])
        cr_t = T("bipolar cell", 22, GREY).move_to([1.75, 2.93, 0])
        fl = Flow([-0.45, top_y, 0], [-1.3, 1.2, 0], n=3, color=GLU, gain=0, speed=0.4)
        fr = Flow([0.45, top_y, 0], [1.3, 1.2, 0], n=3, color=GLU, gain=0, speed=0.4)
        glu_l = T("glutamate", 28, GLU).move_to([4.0, 0.9, 0])
        self.play(FadeIn(rod), FadeIn(cl), FadeIn(cr), FadeIn(cl_t), FadeIn(cr_t), run_time=0.4)
        self.add(fl, fr)
        dark = state_tag("DARK", GREY, pos=(4.6, 3.1))
        self.at("The rod releases")
        self.play(fl.gain.animate.set_value(1), fr.gain.animate.set_value(1), FadeIn(glu_l), FadeIn(dark), run_time=0.6)
        self.at("more in the dark")
        self.play(Indicate(glu_l, color=GLU, scale_factor=1.15), run_time=0.6)
        self.at("less in the light")
        beam = arr([4.2, -2.31, 0], [0.55, -2.31, 0], LIGHT, w=7, tip=0.3)
        beam_l = T("light", 28, LIGHT).next_to(beam, UP, buff=0.12).shift(RIGHT * 1.0)
        lt = state_tag("LIGHT", LIGHT, pos=(4.6, 3.1))
        self.play(GrowArrow(beam), FadeIn(beam_l), ReplacementTransform(dark, lt),
                  fl.gain.animate.set_value(0.35), fr.gain.animate.set_value(0.35), run_time=0.7)
        up = VGroup(T("▲", 22, GREY), T("depolarizes", 22, GREY)).arrange(RIGHT, buff=0.12).move_to([1.75, 2.3, 0])
        dn = VGroup(T("▼", 22, GREY), T("hyperpolarizes", 22, GREY)).arrange(RIGHT, buff=0.12).move_to([-1.75, 2.3, 0])
        self.at("Yet some bipolar")
        self.play(FadeIn(up, shift=UP * 0.2), run_time=0.5)
        self.at("and others")
        self.play(FadeIn(dn, shift=DOWN * 0.2), run_time=0.5)
        q1 = bchip("?", GREY, size=28).move_to([-1.75, 1.65, 0])
        q2 = bchip("?", GREY, size=28).move_to([1.75, 1.65, 0])
        self.at("set by the receptor")
        self.play(FadeIn(q1, scale=0.7), FadeIn(q2, scale=0.7), run_time=0.5)

        # --- phase 2: OFF cell up close ---------------------------------------------------------
        self.at("OFF bipolar cells use")
        for m in self.mobjects:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        c = closeup("off")
        CX = c["CX"]
        gap = c["gap"]
        chan = Channel(CX - 1.2, -1.2, gap, PINK)
        chip_r = bchip("AMPA / kainate", PINK, size=22).move_to([CX + 0.95, -0.55, 0])
        link = Line([CX - 1.2, -0.95, 0], chip_r.get_left(), color=PINK, stroke_width=3)
        cat_l = T("cations", 24, BLUE).move_to([CX - 1.2, -0.3, 0])
        ions = Flow([CX - 1.2, -1.9, 0], [CX - 1.2, -0.75, 0], n=3, color=BLUE, r=0.09, gain=0, speed=0.4)
        self.play(FadeIn(c["base"]), run_time=0.5)
        self.add(*c["glu"], chan, ions)
        self.play(FadeIn(chip_r, scale=0.8), Create(link), run_time=0.6)
        pf = panel_frame()
        self.at("glutamate opens")
        state = T("depolarized", 28, PINK, weight=BOLD).move_to([CX, 1.4, 0])
        darklab = state_tag("DARK", GREY, pos=(3.9, 3.35), size=32)
        self.play(*[f.gain.animate.set_value(1) for f in c["glu"]], gap.animate.set_value(0.5),
                  ions.gain.animate.set_value(1), FadeIn(cat_l), FadeIn(state), FadeIn(pf), FadeIn(darklab), run_time=0.8)
        self.at("Light removes")
        lb = light_bar()
        lt2 = state_tag("LIGHT", LIGHT, pos=(3.9, 3.35), size=32)
        self.play(Create(lb[0]), FadeIn(lb[1]), ReplacementTransform(darklab, lt2), run_time=0.5)
        curve = sketch_curve(-1, PINK)
        state2 = T("hyperpolarized", 28, PINK, weight=BOLD).move_to([CX, 1.4, 0])
        self.play(*[f.gain.animate.set_value(0.2) for f in c["glu"]], gap.animate.set_value(0.0),
                  ions.gain.animate.set_value(0), FadeOut(cat_l), ReplacementTransform(state, state2),
                  Create(curve, rate_func=linear), run_time=1.6)
        self.at("sign is preserved")
        self.play(FadeIn(curve_label("OFF: sign preserved", PINK, [3.7, 0.9, 0])), run_time=0.5)
        self.finish()


class S04On(SpokenScene):
    """the ON cell: glutamate -> mGluR6 -> Go keeps TRPM1 shut; light lowers glutamate and TRPM1 opens."""

    def construct(self):
        c = closeup("on")
        CX = c["CX"]
        gap = c["gap"]
        pf = panel_frame()
        ghost = sketch_curve(-1, PINK)
        ghost.set_stroke(opacity=0.5)
        ghost_l = T("OFF", 24, PINK).move_to([PX1 - 0.3, PYM - 1.2, 0])
        darklab = state_tag("DARK", GREY, pos=(3.9, 3.35), size=32)
        self.play(FadeIn(c["base"]), FadeIn(pf), FadeIn(darklab), run_time=0.7)
        self.add(*c["glu"])
        trpm_ch = Channel(CX + 1.3, -1.2, gap, GREEN)
        self.add(trpm_ch)
        mg = bchip("mGluR6", GREEN, size=24).move_to([CX - 1.4, -1.2, 0])
        go = bchip("Go", ORANGE, size=24).move_to([CX - 1.4, 0.15, 0])
        trp = bchip("TRPM1", GREEN, size=24).move_to([CX + 1.3, 0.15, 0])
        a_mg = arr(mg.get_top(), go.get_bottom(), ORANGE)
        blk = tbar(go.get_right(), trp.get_left(), RED)
        ions = Flow([CX + 1.3, -1.95, 0], [CX + 1.3, -0.5, 0], n=3, color=BLUE, r=0.09, gain=0, speed=0.4)
        self.add(ions)
        self.at("a different receptor")
        self.play(FadeIn(mg, scale=0.8), run_time=0.5)
        self.play(*[f.gain.animate.set_value(1) for f in c["glu"]], run_time=0.5)
        self.at("In the dark")
        self.at("G protein")
        self.play(GrowArrow(a_mg), FadeIn(go, scale=0.8), run_time=0.6)
        self.at("keeps the channel")
        self.play(FadeIn(trp, scale=0.8), Create(blk), run_time=0.7)
        self.at("Light lowers")
        lb = light_bar()
        lt2 = state_tag("LIGHT", LIGHT, pos=(3.9, 3.35), size=32)
        self.play(Create(lb[0]), FadeIn(lb[1]), ReplacementTransform(darklab, lt2), FadeIn(ghost), FadeIn(ghost_l),
                  *[f.gain.animate.set_value(0.2) for f in c["glu"]], run_time=0.6)
        self.at("Go activity declines")
        self.play(*dimc(mg), *dimc(go), FadeOut(a_mg), FadeOut(blk), run_time=0.7)
        self.at("opens")
        self.play(gap.animate.set_value(0.5), ions.gain.animate.set_value(1), run_time=0.6)
        self.at("The cell depolarizes")
        curve = sketch_curve(+1, GREEN)
        state2 = T("depolarized", 28, GREEN, weight=BOLD).move_to([CX, 1.4, 0])
        self.play(FadeIn(state2), Create(curve, rate_func=linear), run_time=1.4)
        self.at("sign is inverted")
        self.play(FadeIn(curve_label("ON: sign inverted", GREEN, [3.7, -0.85, 0])), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def spikes(x0, x1, y, times, color, h=0.4):
    return VGroup(*[Line([x0 + t * (x1 - x0), y - h / 2, 0], [x0 + t * (x1 - x0), y + h / 2, 0], color=color, stroke_width=4)
                    for t in times])


class S05Streams(SpokenScene):
    """photoreceptor -> ON / OFF bipolar -> ON / OFF ganglion; sketch spike trains."""

    def construct(self):
        rcpt = bchip("photoreceptor", BLUE, size=24).move_to([-5.05, 0.0, 0])
        on_b = bchip("ON bipolar", GREEN, size=26).move_to([-1.75, 1.7, 0])
        off_b = bchip("OFF bipolar", PINK, size=26).move_to([-1.75, -1.7, 0])
        on_g = bchip("ON ganglion", GREEN, size=26).move_to([1.15, 1.7, 0])
        off_g = bchip("OFF ganglion", PINK, size=26).move_to([1.15, -1.7, 0])
        self.at("So each photoreceptor")
        self.play(FadeIn(rcpt, scale=0.9), run_time=0.4)
        a_on = tbar(rcpt.get_right() + UP * 0.15, on_b.get_left(), RED)
        a_off = arr(rcpt.get_right() + DOWN * 0.15, off_b.get_left(), GREY)
        k_on = T("inverts the sign", 22, RED).next_to(on_b, UP, buff=0.12)
        k_off = T("keeps the sign", 22, GREY).next_to(off_b, DOWN, buff=0.12)
        self.at("two parallel streams")
        self.play(FadeIn(on_b, scale=0.9), FadeIn(off_b, scale=0.9), Create(a_on), GrowArrow(a_off),
                  FadeIn(k_on), FadeIn(k_off), run_time=0.9)
        lighter = T("signals lighter", 22, GREEN).next_to(on_b, DOWN, buff=0.12)
        darker = T("signals darker", 22, PINK).next_to(off_b, UP, buff=0.12)
        self.at("lighter")
        self.play(FadeIn(lighter), run_time=0.4)
        self.at("darker")
        self.play(FadeIn(darker), run_time=0.4)
        b_on = arr(on_b.get_right(), on_g.get_left(), GREY)
        b_off = arr(off_b.get_right(), off_g.get_left(), GREY)
        self.at("ON bipolar cells drive")
        self.play(GrowArrow(b_on), FadeIn(on_g, scale=0.9), run_time=0.6)
        self.at("OFF bipolar cells drive")
        self.play(GrowArrow(b_off), FadeIn(off_g, scale=0.9), run_time=0.6)

        # spike sketches
        RX0, RX1 = 3.4, 6.3
        pre = [0.08, 0.28, 0.5, 0.7, 0.9]           # baseline firing, before light (as fractions of the pre-light span)
        t_on = 0.38
        xs = [t_on * p for p in pre]
        post_on = [t_on + (1 - t_on) * q for q in np.linspace(0.05, 0.95, 11)]
        row_on = spikes(RX0, RX1, 1.7, xs + post_on, GREEN)
        row_off = spikes(RX0, RX1, -1.7, xs + [t_on + (1 - t_on) * q for q in (0.2, 0.75)], PINK)
        ax_on = Line([RX0, 1.3, 0], [RX1, 1.3, 0], color=GREY, stroke_width=2)
        ax_off = Line([RX0, -2.1, 0], [RX1, -2.1, 0], color=GREY, stroke_width=2)
        spk_t = T("spikes, in this sketch", 22, GREY).move_to([4.85, 2.75, 0])
        self.at("In cat retina")
        self.play(FadeIn(ax_on), FadeIn(ax_off), FadeIn(spk_t),
                  LaggedStart(*[Create(s) for s in list(row_on[:5]) + list(row_off[:5])], lag_ratio=0.08), run_time=0.9)
        lb = Line([RX0 + t_on * (RX1 - RX0), -2.75, 0], [RX1, -2.75, 0], color=LIGHT, stroke_width=9)
        lb_l = T("light on the centre", 22, LIGHT).move_to([4.85, -3.2, 0])
        self.at("of a field")
        self.play(Create(lb), FadeIn(lb_l), run_time=0.5)
        self.at("fire faster")
        self.play(LaggedStart(*[Create(s) for s in row_on[5:]], lag_ratio=0.12), run_time=1.0)
        quiet = T("suppressed", 22, PINK).move_to([RX0 + 0.62 * (RX1 - RX0) * 0.5 + 0.38 * (RX1 - RX0) + 0.0, -1.35, 0])
        self.at("suppresses")
        self.play(FadeIn(quiet), *[Create(t) for t in row_off[5:]], run_time=0.5)
        self.at("Ganglion cells fire")
        self.play(Indicate(VGroup(on_g, off_g), color=GOLD, scale_factor=1.1), run_time=0.8)
        self.at("only output")
        box = SurroundingRectangle(VGroup(on_g, off_g), color=GOLD, buff=0.25, stroke_width=4, corner_radius=0.2)
        out_l = T("the only output", 24, GOLD).move_to([1.15, 0.0, 0])
        self.play(Create(box), FadeIn(out_l), run_time=0.7)
        self.finish()


class S06Rule(SpokenScene):
    """one glutamate stream, two readers; the rule."""

    def construct(self):
        rcpt = bchip("photoreceptor", BLUE, size=28).move_to([-5.0, 0.4, 0])
        lt = arr([-6.3, -1.1, 0], [-5.4, -0.2, 0], LIGHT, w=6)
        lt_l = T("light", 26, LIGHT).move_to([-6.1, -1.55, 0])
        off_r = bchip("OFF bipolar: keeps the sign", PINK, size=26).move_to([0.6, 2.0, 0])
        on_r = bchip("ON bipolar: inverts the sign", GREEN, size=26).move_to([0.6, -1.2, 0])
        self.at("Light switches")
        self.play(FadeIn(rcpt, scale=0.9), GrowArrow(lt), FadeIn(lt_l), run_time=0.7)
        off_t = T("off", 28, GREY, weight=BOLD).next_to(rcpt, DOWN, buff=0.25)
        self.play(FadeIn(off_t), run_time=0.4)
        # the same glutamate reaches both readers
        a1 = arr(rcpt.get_right() + UP * 0.1, off_r.get_left(), GLU)
        a2 = arr(rcpt.get_right() + DOWN * 0.1, on_r.get_left(), GLU)
        gl = T("glutamate", 24, GLU).move_to([-2.5, 0.4, 0])
        self.at("two opposite ways")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(gl), FadeIn(off_r, scale=0.9), FadeIn(on_r, scale=0.9), run_time=0.9)
        # small sketch traces next to each reader
        def mini(sign, color, y):
            ts = np.linspace(0, 1, 80)
            pts = [[3.4 + 2.8 * t, y + (0 if t < 0.4 else sign * 0.5 * (1 - np.exp(-(t - 0.4) / 0.13))), 0] for t in ts]
            cv = VMobject(color=color, stroke_width=5)
            cv.set_points_as_corners(pts)
            base = DashedLine([3.4, y, 0], [6.2, y, 0], color=GREY, stroke_width=2, dash_length=0.12)
            return VGroup(base, cv)
        m_off, m_on = mini(-1, PINK, 2.0), mini(+1, GREEN, -1.2)
        self.at("OFF bipolar cells keep")
        self.play(Create(m_off[0]), Create(m_off[1], rate_func=linear), run_time=0.9)
        self.at("ON bipolar cells invert")
        self.play(Create(m_on[0]), Create(m_on[1], rate_func=linear), run_time=0.9)
        note = T("in this sketch", 22, GREY).move_to([4.8, 0.4, 0])
        self.play(FadeIn(note), run_time=0.3)
        self.at("Keep this rule")
        rule = T("The receptor, not the molecule, sets the sign.", 36, TEXT, font=TITLE_FONT).move_to([0.0, -3.0, 0])
        fit(rule, max_w=11.8)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The receptor, not the molecule, sets the sign."
