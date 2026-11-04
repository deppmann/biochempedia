"""Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube -- chapter 1, "The Tube Gains a Second Floor"
(Biochemistrypedia chaptered explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, the whole chapter series)
  YELLOW = Sonic hedgehog and the signalling it causes (gold, from below)
  DORSAL = BMP and the dorsal tissues that send it: roof plate, epidermis (blue-violet, from above)
  TEAL   = notochord and floor plate (the ventral source tissue), and anything induced to be floor plate
  BLUE   = class I factors / Pax6 / Pax7 side, and the motor neuron domain (pMN) and motor neurons
  ORANGE = class II factors / Nkx2.2 side, and the p3 domain                            (later chapters)
  RED    = repression (the T-bars) and nothing else                                      (later chapters)
  PURPLE = Patched1                                                                      (later chapters)
  GREY   = tube wall, neutral cells, axes; TEXT (white) = highlight outlines, icons, cell of interest
  PROG   = soft blue-grey fill for progenitor cells (the dividing wall cells)
Map geometry (every map scene rebuilds it in the same place, through the TM class): tube centred at x=0,
dorsal up, about 6.95 units (87%) of the frame height from the bottom of the notochord to the top of the
epidermis. The notochord is a rod that touches the floor plate. Small 22 pt tags stay on the map.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
DORSAL = "#7D8BFF"
LIGHT_TEAL = "#A6E6EA"
PROG = "#7C9CCB"
MOTOR = "#3A63F0"
TAG_TEAL = "#B8F0F2"
TAG_DORSAL = "#BCC4FF"
PROG_EDGE = "#C8D2E8"

RY = [-2.16 + 0.48 * i for i in range(10)]          # wall rows, bottom (0) to top (9), local units
STRIPE_ROW = {"p0": 4, "p1": 3, "p2": 2, "pMN": 1, "p3": 0}
NAMES = ["p0", "p1", "p2", "pMN", "p3"]
GRAFT = (2.3, 0.24)                                  # local position of the grafted notochord
GRAFT_ROWS = (4, 5, 6)                               # right-hand wall cells it touches
HL_ROW = 6                                           # the cell of interest (left wall)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def mix(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), float(np.clip(t, 0, 1)))


def put(t, x, y, anchor="c"):
    t.move_to([x, y, 0])
    if anchor == "l":
        t.shift(RIGHT * (x - t.get_left()[0]))
    elif anchor == "r":
        t.shift(RIGHT * (x - t.get_right()[0]))
    return t


def lab(s, x, y, color=TEXT, size=24, anchor="c", **kw):
    return put(T(s, size, color, **kw), x, y, anchor)


def style_neutral(c):
    return c.set_stroke(GREY, 2).set_fill(GREY, 0.18)


def style_prog(c):
    return c.set_stroke(PROG_EDGE, 2.5).set_fill(PROG, 0.62)


def style_teal(c):
    return c.set_stroke(TEAL, 4).set_fill(TEAL, 0.6)


def tealize(cells):
    return [c.animate.set_stroke(TEAL, 4).set_fill(TEAL, 0.6) for c in cells]


def teal_now(cells):
    for c in cells:
        style_teal(c)


# ------------------------------------------------------------------ the transverse neural tube map
class TM:
    """The map at scale s, centred on x=cx; local coordinates (x, y) are mapped to the world by p()."""

    def __init__(self, s=1.0, cx=0.0, cy=0.17):
        self.s, self.cx, self.cy = s, cx, cy

    def p(self, x, y):
        return np.array([self.cx + self.s * x, self.cy + self.s * y, 0.0])

    def rect(self, x, y, w, h, color, o=0.55, sw=3, r=0.07):
        return RoundedRectangle(corner_radius=r * self.s, width=w * self.s, height=h * self.s, stroke_color=color,
                                stroke_width=max(1.5, sw * self.s), fill_color=color, fill_opacity=o).move_to(self.p(x, y))

    def shell(self):
        return RoundedRectangle(corner_radius=0.8 * self.s, width=3.7 * self.s, height=5.5 * self.s, stroke_color=GREY,
                                stroke_width=max(2.5, 5 * self.s), fill_color=GREY, fill_opacity=0.06).move_to(self.p(0, 0))

    def canal(self):
        return RoundedRectangle(corner_radius=0.1 * self.s, width=0.32 * self.s, height=4.9 * self.s, stroke_color=GREY,
                                stroke_width=1.5, fill_color=BG, fill_opacity=0.9).move_to(self.p(0, 0))

    def cell(self, x, y, w=1.4, h=0.40):
        return style_neutral(self.rect(x, y, w, h, GREY, 0.18, 2))

    def wall(self, prog=False):
        rows = []
        for y in RY:
            L, R = self.cell(-0.9, y), self.cell(0.9, y)
            if prog:
                style_prog(L)
                style_prog(R)
            rows.append(VGroup(L, R))
        return VGroup(*rows)

    def floor(self, kind="neutral"):
        if kind == "teal":
            return self.rect(0, -2.62, 1.8, 0.24, TEAL, 0.6, 3)
        return self.rect(0, -2.62, 1.8, 0.24, GREY, 0.25, 3)

    def roof(self, kind="neutral"):
        if kind == "dorsal":
            return self.rect(0, 2.62, 1.8, 0.24, DORSAL, 0.6, 3)
        return self.rect(0, 2.62, 1.8, 0.24, GREY, 0.25, 3)

    def slot(self):
        r = RoundedRectangle(corner_radius=0.07 * self.s, width=1.8 * self.s, height=0.24 * self.s, stroke_color=TEXT,
                             stroke_width=3)
        return DashedVMobject(r, num_dashes=30).move_to(self.p(0, -2.62))

    def noto(self, x=0.0, y=-3.2, r=0.45, o=0.4):
        return Circle(radius=r * self.s, stroke_color=TEAL, stroke_width=max(2.5, 3 * self.s), fill_color=TEAL,
                      fill_opacity=o).move_to(self.p(x, y))

    def epi(self):
        return self.rect(0, 3.2, 3.9, 0.2, DORSAL, 0.55, 3)

    def graft(self):
        return self.noto(GRAFT[0], GRAFT[1])


def std(m, prog=False, floor="teal", roof="dorsal", epi=True, noto=True):
    """The usual stack of map pieces (z-order: bottom first)."""
    items = [m.shell(), m.canal(), m.wall(prog)]
    if floor:
        items.append(m.floor(floor))
    if roof:
        items.append(m.roof(roof))
    if noto:
        items.append(m.noto())
    if epi:
        items.append(m.epi())
    return items


# ------------------------------------------------------------------ persistent small tags (22 pt)
def tg(m, name, side=None, size=22):
    P = m.p
    if name == "noto":
        sd = side or "L"
        x = P(-0.62, 0)[0] if sd == "L" else P(0.62, 0)[0]
        return VGroup(lab("notochord", x, P(0, -3.2)[1], TAG_TEAL, size, "r" if sd == "L" else "l"))
    if name in ("floor", "roof"):
        sd = side or ("L" if name == "floor" else "R")
        sg = -1 if sd == "L" else 1
        y = -2.62 if name == "floor" else 2.62
        col = TEAL if name == "floor" else DORSAL
        tcol = TAG_TEAL if name == "floor" else TAG_DORSAL
        txt = "floor plate" if name == "floor" else "roof plate"
        t = lab(txt, P(sg * 2.2, 0)[0], P(0, y)[1], tcol, size, "r" if sg < 0 else "l")
        ln = Line(P(sg * 2.15, y), P(sg * 0.95, y), color=col, stroke_width=2.5)
        return VGroup(t, ln)
    if name == "epi":
        t = lab("epidermis", P(2.7, 0)[0], P(0, 3.35)[1], TAG_DORSAL, size, "l")
        ln = Line(P(2.65, 3.2), P(1.97, 3.2), color=DORSAL, stroke_width=2.5)
        return VGroup(t, ln)
    raise KeyError(name)


def axis_tags():
    a = arr([-6.15, -2.85, 0], [-6.15, 2.85, 0], GREY, 4, 0.25)
    d = lab("dorsal", -6.15, 3.3, GREY, 22)
    v = lab("ventral", -6.15, -3.3, GREY, 22)
    return VGroup(a, d, v)


def tag_set(m, names, sides=None):
    sides = sides or {}
    return [tg(m, n, sides.get(n)) for n in names]


# ------------------------------------------------------------------ small drawings
def neuron(x, y, flip=1, color=TEXT):
    """A cell body with short dendrites on one side and one long fibre on the other."""
    soma = Circle(radius=0.27, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x, y, 0])
    fibre = Line([x, y, 0], [x + flip * 1.75, y, 0], color=color, stroke_width=6)
    ds = [Line([x, y, 0], [x - flip * 0.5, y + dy, 0], color=color, stroke_width=4) for dy in (0.32, 0.0, -0.32)]
    return VGroup(*ds, fibre, soma)


def stripes(m, rows=range(5)):
    out = []
    for r in rows:
        for sx in (-0.9, 0.9):
            out.append(RoundedRectangle(corner_radius=0.07 * m.s, width=1.5 * m.s, height=0.45 * m.s, stroke_color=TEXT,
                                        stroke_width=3.5).move_to(m.p(sx, RY[r])))
    return VGroup(*out)


def qbox(n, y, x=1.9, w=9.6, h=1.1, hl=False):
    col = GOLD if hl else GREY
    b = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=col, stroke_width=3,
                         fill_color=col, fill_opacity=0.08).move_to([x, y, 0])
    num = T(str(n), 40, GOLD, weight=BOLD).move_to([x - w / 2 + 0.55, y, 0])
    return b, num


# ---------------------------------------------------------------------------------------------
class SS(SpokenScene):
    """SpokenScene that logs anything outside the safe frame or overlapping text at the end of the scene."""

    def finish(self):
        self._check()
        super().finish()

    def _check(self):
        import os
        from pathlib import Path
        texts, bad = [], []

        def walk(m, top):
            if isinstance(m, Text):
                texts.append(m)
                return
            for s in m.submobjects:
                walk(s, top)
        for m in self.mobjects:
            walk(m, m)
            if m.get_left()[0] < -6.85 or m.get_right()[0] > 6.85 or m.get_top()[1] > 3.85 or m.get_bottom()[1] < -3.85:
                if m.get_width() < 20:
                    bad.append(f"OUT {type(m).__name__} x[{m.get_left()[0]:.2f},{m.get_right()[0]:.2f}] y[{m.get_bottom()[1]:.2f},{m.get_top()[1]:.2f}]")
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                a, b = texts[i], texts[j]
                if (a.get_fill_opacity() or 0) < 0.05 or (b.get_fill_opacity() or 0) < 0.05:
                    continue
                if (min(a.get_right()[0], b.get_right()[0]) - max(a.get_left()[0], b.get_left()[0]) > 0.02 and
                        min(a.get_top()[1], b.get_top()[1]) - max(a.get_bottom()[1], b.get_bottom()[1]) > 0.02):
                    bad.append(f"OVERLAP '{a.text}' / '{b.text}'")
        with open(Path(os.environ["KX_SCRIPT"]).parent / "scratch" / "bounds.log", "a") as lg:
            for b in bad:
                lg.write(f"{os.environ.get('KX_SCENE_ID')}  {b}\n")


class S00Title(TitleCard):
    LESSON = "Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube"
    TITLE = "The Tube Gains a Second Floor"


# ---------------------------------------------------------------------------------------------
class S01Q(SS):
    def construct(self):
        m = TM()
        tube, can, w, fl, no = m.shell(), m.canal(), m.wall(), m.floor("teal"), m.noto()
        self.play(FadeIn(tube), FadeIn(can), FadeIn(w), FadeIn(fl), FadeIn(no), run_time=0.6)
        g = m.noto(0, 0)
        g.move_to([6.2, m.p(0, GRAFT[1])[1], 0])
        l_n = tg(m, "noto")
        l_g = lab("grafted notochord", m.p(2.85, 0)[0], m.p(0, GRAFT[1])[1], TEAL, 26, "l")
        l_t = lab("neural tube", m.p(-2.5, 0)[0], m.p(0, 1.9)[1], TEXT, 26, "r")
        l_tl = Line(m.p(-2.45, 1.9), m.p(-1.88, 1.9), color=TEXT, stroke_width=2.5)
        l_f = lab("behaves like\nfloor plate", m.p(2.85, 0)[0], m.p(0, -1.0)[1], TEAL, 26, "l", line_spacing=0.9)
        l_fl = Line(m.p(2.8, -0.8), m.p(1.65, -0.3), color=TEAL, stroke_width=2.5)
        self.at("a second notochord")
        self.play(g.animate.move_to(m.p(*GRAFT)), FadeIn(l_n), run_time=1.3)
        self.at("side of a")
        self.play(FadeIn(l_g), run_time=0.4)
        self.at("neural tube")
        self.play(FadeIn(l_t), Create(l_tl), run_time=0.4)
        self.at("start to behave")
        self.play(*tealize([w[i][1] for i in GRAFT_ROWS]), run_time=1.0)
        self.at("floor plate")
        self.play(FadeIn(l_f), Create(l_fl), run_time=0.5)
        self.finish()


class S02Q2(SS):
    def construct(self):
        m = TM()
        tube, can, w, fl, no = m.shell(), m.canal(), m.wall(), m.floor("teal"), m.noto()
        g = m.graft()
        teal_now([w[i][1] for i in GRAFT_ROWS])
        self.add(tube, can, w, fl, no, g)
        l_b = lab("bottom", m.p(-2.4, 0)[0], m.p(0, -2.62)[1], TEAL, 26, "r")
        l_bl = Line(m.p(-2.35, -2.62), m.p(-0.95, -2.62), color=TEAL, stroke_width=2.5)
        l_b2 = lab("second bottom", m.p(2.85, 0)[0], m.p(0, -1.0)[1], TEAL, 26, "l")
        l_b2l = Line(m.p(2.8, -0.85), m.p(1.65, -0.3), color=TEAL, stroke_width=2.5)
        self.at("a second bottom")
        self.play(Indicate(fl, color=TEAL), Indicate(VGroup(*[w[i][1] for i in GRAFT_ROWS]), color=TEAL),
                  FadeIn(l_b), Create(l_bl), FadeIn(l_b2), Create(l_b2l), run_time=1.0)
        self.at("a cell in the wall")
        hl = RoundedRectangle(corner_radius=0.07, width=1.4, height=0.4, stroke_color=TEXT, stroke_width=5,
                              fill_color=TEXT, fill_opacity=0.3).move_to(m.p(-0.9, RY[HL_ROW]))
        q = T("?", 64, TEXT, weight=BOLD).move_to(m.p(-2.4, RY[HL_ROW]))
        ql = DashedLine(m.p(-2.05, RY[HL_ROW]), m.p(-1.63, RY[HL_ROW]), color=TEXT, stroke_width=3)
        self.play(FadeIn(hl, scale=1.2), run_time=0.5)
        self.play(FadeIn(q, shift=UP * 0.15), Create(ql), run_time=0.4)
        self.at("far it sits")
        meas = DoubleArrow(m.p(0, RY[HL_ROW]), m.p(0, -2.42), color=TEXT, stroke_width=4, tip_length=0.18, buff=0)
        self.play(GrowFromPoint(meas, meas.get_top()), run_time=1.0)
        self.finish()


def blend_state(i, use_y=True, use_b=True):
    a = float(np.exp(-i / 3.0)) if use_y else 0.0
    b = float(np.exp(-(9 - i) / 3.0)) if use_b else 0.0
    t = b / (a + b) if (a + b) > 0 else 0
    col = mix(YELLOW, DORSAL, t)
    return col, 0.14 + 0.62 * min(1.0, a + b)


class S03Answer(SS):
    def construct(self):
        m = TM()
        items = std(m, floor="neutral", roof="neutral")
        w = items[2]
        self.play(*[FadeIn(i) for i in items], run_time=0.6)
        P = m.p
        ups = VGroup(*[arr(P(0, -3.0), P(x, -1.9), YELLOW, 6, 0.22) for x in (-0.9, 0.0, 0.9)])
        dns = VGroup(*[arr(P(x, 3.05), P(x, 2.0), DORSAL, 6, 0.22) for x in (-0.9, 0.0, 0.9)])
        t_n, t_e, t_f, t_r = tg(m, "noto"), tg(m, "epi"), tg(m, "floor"), tg(m, "roof")
        self.at("neighbors tell")
        self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in dns], lag_ratio=0.2),
                  FadeIn(t_n), FadeIn(t_e), FadeIn(t_f), FadeIn(t_r), run_time=1.0)
        self.at("cell's position")
        hl = RoundedRectangle(corner_radius=0.07, width=1.5, height=0.48, stroke_color=TEXT, stroke_width=5).move_to(P(-0.9, RY[HL_ROW]))
        self.play(Create(hl), run_time=0.5)
        self.at("how much signal")
        anims = []
        for i in range(10):
            col, op = blend_state(i, True, False)
            for c in w[i]:
                anims.append(c.animate.set_stroke(col, 3).set_fill(col, op))
        self.play(*anims, run_time=1.0)
        l_y = lab("signal from below", P(2.4, 0)[0], P(0, -1.3)[1], YELLOW, 26, "l")
        self.at("from below")
        self.play(FadeIn(l_y, shift=RIGHT * 0.15), run_time=0.4)
        self.at("and above")
        anims = []
        for i in range(10):
            col, op = blend_state(i, True, True)
            for c in w[i]:
                anims.append(c.animate.set_stroke(col, 3).set_fill(col, op))
        l_b = lab("signal from above", P(2.4, 0)[0], P(0, 1.5)[1], DORSAL, 26, "l")
        self.play(*anims, FadeIn(l_b, shift=RIGHT * 0.15), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Tube(SS):
    def construct(self):
        m = TM()
        P = m.p
        specs = []        # (flat x, flat y, flat w, flat h, closed center, closed w, closed h, delay, kind)
        for k in range(-10, 11):
            fx, fy, fw, fh = 0.44 * k, 0.45, 0.38, 2.9
            if k == 0:
                cc, cw, ch = P(0, -2.62), 1.8 * m.s, 0.24 * m.s
            else:
                cc, cw, ch = P(-0.9 if k < 0 else 0.9, RY[abs(k) - 1]), 1.4 * m.s, 0.40 * m.s
            specs.append((fx, fy, fw, fh, cc, cw, ch, abs(k) / 10 * 0.55, "n"))
        T_ = ValueTracker(0)

        def make(sp):
            fx, fy, fw, fh, cc, cw, ch, dl, kind = sp
            col = GREY
            op = 0.18

            def build(t):
                u = float(np.clip((t - dl) / 0.35, 0, 1))
                u = u * u * (3 - 2 * u)
                x = (1 - u) * fx + u * cc[0]
                y = (1 - u) * fy + u * cc[1]
                w_, h_ = (1 - u) * fw + u * cw, (1 - u) * fh + u * ch
                return RoundedRectangle(corner_radius=0.07, width=w_, height=h_, stroke_color=col, stroke_width=2.5,
                                        fill_color=col, fill_opacity=op).move_to([x, y, 0])
            c = build(0)
            c.add_updater(lambda mob, b=build: mob.become(b(T_.get_value())))
            return c
        cells = [make(sp) for sp in specs]
        sheet = VGroup(*cells)
        self.play(FadeIn(sheet, lag_ratio=0.03), run_time=0.8)
        l_p = lab("neural plate", -5.6, 3.1, TEXT, 28, "l")
        l_pl = Line([-5.0, 2.85, 0], [-4.5, 1.95, 0], color=TEXT, stroke_width=2.5)
        self.at("the map")
        self.play(FadeIn(l_p), Create(l_pl), run_time=0.5)
        self.at("rolls up", lead=0.6)
        self.play(FadeOut(l_p), FadeOut(l_pl), T_.animate.set_value(0.8), run_time=0.9, rate_func=smooth)
        tube, can = m.shell(), m.canal()
        self.play(T_.animate.set_value(1.2), FadeIn(tube), FadeIn(can), run_time=0.6, rate_func=smooth)
        for c in cells:
            c.clear_updaters()
        roof = m.roof("neutral")
        self.add(roof)
        # slicing: the tube runs back behind the cut face; the cut is drawn, then named
        off = np.array([-1.1, 0.0, 0.0])
        ghost = tube.copy().set_fill(opacity=0).set_stroke(GREY, 2.5, opacity=0.9).shift(off)
        gl = VGroup(*[Line(a, a + off, color=GREY, stroke_width=2.5, stroke_opacity=0.9) for a in
                      (P(-1.616, 2.516), P(-1.616, -2.516))])
        cut = DashedVMobject(RoundedRectangle(corner_radius=0.8, width=3.7, height=5.5, stroke_color=TEXT, stroke_width=5).move_to(P(0, 0)),
                             num_dashes=40)
        l_x = lab("cut across:\ncross-section", P(2.5, 0)[0], P(0, -1.0)[1], TEXT, 28, "l", line_spacing=0.9)
        l_xl = Line(P(2.45, -1.0), P(1.88, -1.0), color=TEXT, stroke_width=2.5)
        self.play(FadeIn(ghost), FadeIn(gl), run_time=0.5)
        self.play(Create(cut), FadeIn(l_x), Create(l_xl), run_time=0.6)
        ax = axis_tags()
        l_t = lab("neural tube", P(2.5, 0)[0], P(0, 1.6)[1], TEXT, 28, "l")
        l_tl = Line(P(2.45, 1.6), P(1.88, 1.6), color=TEXT, stroke_width=2.5)
        self.at("becomes")
        self.play(FadeOut(cut), FadeIn(l_t), Create(l_tl), FadeIn(ax), run_time=0.4)
        l_bs = lab("brain and\nspinal cord", P(2.5, 0)[0], P(0, 0.5)[1], TEXT, 28, "l", line_spacing=0.9)
        l_bsl = Line(P(2.45, 0.5), P(1.88, 0.5), color=TEXT, stroke_width=2.5)
        self.at("the brain")
        self.play(FadeIn(l_bs), Create(l_bsl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Noto(SS):
    def construct(self):
        m = TM()
        items = std(m, floor="neutral", roof="neutral", noto=False, epi=False)
        ax = axis_tags()
        self.add(*items, ax, *tag_set(m, ["floor", "roof"]))
        no = m.noto()
        l_no = tg(m, "noto")
        self.at("runs the")
        self.play(GrowFromCenter(no), run_time=0.5)
        self.at("the notochord")
        self.play(FadeIn(l_no), run_time=0.4)
        self.at("rod of mesoderm")
        self.play(Indicate(no, color=TEAL, scale_factor=1.25), run_time=0.8)
        ys = [-2.45, -3.0, -3.55]
        specs = [("outer layer", GREY, 2, 0.2, GREY), ("mesoderm", TEAL, 3, 0.5, TEXT), ("inner layer", GREY, 2, 0.2, GREY)]
        bars = [RoundedRectangle(corner_radius=0.07, width=3.4, height=0.5, stroke_color=c, stroke_width=sw, fill_color=c,
                                 fill_opacity=o).move_to([3.4, y, 0]) for y, (t, c, sw, o, tc) in zip(ys, specs)]
        names = [lab(t, 3.4, y, tc, 24) for y, (t, c, sw, o, tc) in zip(ys, specs)]
        stack = VGroup(*[VGroup(b, n) for b, n in zip(bars, names)])
        self.at("embryo's")
        self.play(FadeIn(stack, lag_ratio=0.25), run_time=0.9)
        lead = Line(m.p(0.45, -3.2), [1.7, ys[1], 0], color=TEAL, stroke_width=3.5)
        self.at("middle cell layer")
        self.play(Create(lead), Indicate(stack[1], color=TEAL, scale_factor=1.06), Indicate(no, color=TEAL), run_time=1.0)
        self.finish()


class S06Floor(SS):
    def construct(self):
        m = TM()
        items = std(m, floor="neutral", roof="neutral", epi=False)
        fl, rf = items[3], items[4]
        ax, t_n = axis_tags(), tg(m, "noto")
        t_f, t_r = tg(m, "floor"), tg(m, "roof")
        self.add(*items, ax, t_n, t_f, t_r)
        sub = lab("narrow line of\nspecialized cells", m.p(-2.65, 0)[0], m.p(0, -3.25)[1], TEAL, 22, "r", line_spacing=0.9)
        self.at("bottom strip")
        self.play(fl.animate.set_stroke(TEAL, 3).set_fill(TEAL, 0.6), run_time=0.7)
        self.at("the floor plate")
        self.play(Indicate(t_f[0], color=TEAL, scale_factor=1.15), run_time=0.5)
        self.at("narrow line")
        self.play(FadeIn(sub), Indicate(fl, color=TEAL, scale_factor=1.15), run_time=0.8)
        self.at("top strip")
        self.play(rf.animate.set_stroke(DORSAL, 3).set_fill(DORSAL, 0.6), run_time=0.7)
        self.at("roof plate")
        self.play(Indicate(t_r[0], color=DORSAL, scale_factor=1.15), run_time=0.5)
        self.finish()


class S07Epi(SS):
    def construct(self):
        m = TM()
        items = std(m, floor="teal", roof="dorsal", epi=False)
        ax = axis_tags()
        tags = tag_set(m, ["noto", "floor", "roof"], {"roof": "L"})
        self.add(*items, ax, *tags)
        halves = VGroup(m.rect(-1.2, 3.2, 1.95, 0.2, DORSAL, 0.55, 3), m.rect(1.2, 3.2, 1.95, 0.2, DORSAL, 0.55, 3))
        lx = m.p(2.5, 0)[0]
        l_e = lab("epidermis", lx, m.p(0, 3.4)[1], TAG_DORSAL, 22, "l")
        l_s = lab("(non-neural ectoderm)", lx, m.p(0, 3.03)[1], TAG_DORSAL, 22, "l")
        self.at("epidermis")
        self.play(FadeIn(halves), FadeIn(l_e), run_time=0.6)
        self.at("non neural ectoderm")
        self.play(FadeIn(l_s), run_time=0.5)
        self.at("ends up over")
        self.play(halves[0].animate.move_to(m.p(-0.975, 3.2)), halves[1].animate.move_to(m.p(0.975, 3.2)), run_time=1.3)
        ln = Line(m.p(2.45, 3.2), m.p(1.97, 3.2), color=DORSAL, stroke_width=2.5)
        self.play(Create(ln), run_time=0.4)
        self.finish()


def base_tags(m, sides=None):
    return [axis_tags()] + tag_set(m, ["noto", "floor", "roof", "epi"], sides)


class S08Prog(SS):
    def construct(self):
        m = TM()
        items = std(m)
        w, fl, rf = items[2], items[3], items[4]
        self.add(*items, *base_tags(m))
        self.at("between floor and roof")
        self.play(Indicate(fl, color=TEAL, scale_factor=1.2), Indicate(rf, color=DORSAL, scale_factor=1.2), run_time=1.2)
        self.at("dividing cells")
        self.play(Indicate(w[3][0], color=TEXT, scale_factor=1.25), Indicate(w[6][1], color=TEXT, scale_factor=1.25),
                  Indicate(w[2][1], color=TEXT, scale_factor=1.25), run_time=1.0)
        l_p = lab("progenitors", m.p(-2.35, 0)[0], m.p(0, 0.2)[1], TEXT, 26, "r")
        br = VGroup(Line(m.p(-2.1, -2.35), m.p(-2.1, 2.35), color=TEXT, stroke_width=3),
                    Line(m.p(-2.1, -2.35), m.p(-1.95, -2.35), color=TEXT, stroke_width=3),
                    Line(m.p(-2.1, 2.35), m.p(-1.95, 2.35), color=TEXT, stroke_width=3))
        self.at("called progenitors")
        fills = [AnimationGroup(*[c.animate.set_stroke(PROG_EDGE, 2.5).set_fill(PROG, 0.62) for c in r]) for r in w]
        self.play(FadeIn(l_p), Create(br), LaggedStart(*fills, lag_ratio=0.06), run_time=1.1)
        l_c = lab("central canal", m.p(2.75, 0)[0], m.p(0, 0.0)[1], TEXT, 26, "l")
        lead = Line(m.p(2.7, 0.0), m.p(0.0, 0.0), color=TEXT, stroke_width=2.5)
        dot = Dot(m.p(0.0, 0.0), radius=0.07, color=TEXT)
        self.at("central canal")
        self.play(Create(lead), FadeIn(dot), FadeIn(l_c), run_time=0.7)
        self.finish()


class S09Prog2(SS):
    def construct(self):
        m = TM()
        items = std(m, prog=True)
        w = items[2]
        self.add(*items, *base_tags(m, {"floor": "R"}))
        P = m.p
        m_ic = VGroup(neuron(-2.9, P(0, RY[0])[1], -1, MOTOR), neuron(-2.9, P(0, RY[2])[1], -1, MOTOR))
        m_l = lab("motor neurons", -4.0, -2.78, "#8FA8FF", 26)
        s_ic = VGroup(neuron(2.9, 1.0, 1, DORSAL), neuron(2.9, 1.85, 1, DORSAL))
        s_l = lab("relay neurons for\nbody sensation", 3.9, 0.15, DORSAL, 26, line_spacing=0.9)
        self.at("motor neurons")
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in m_ic], lag_ratio=0.25), FadeIn(m_l), run_time=1.0)
        self.at("near the bottom")
        self.play(*[Indicate(w[i][j], color=MOTOR, scale_factor=1.12) for i in (0, 1, 2) for j in (0, 1)], run_time=0.8)
        self.at("relay neurons")
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in s_ic], lag_ratio=0.25), FadeIn(s_l), run_time=1.0)
        self.at("near the top")
        self.play(*[Indicate(w[i][j], color=DORSAL, scale_factor=1.12) for i in (7, 8, 9) for j in (0, 1)], run_time=0.8)
        self.finish()


class S10Slots(SS):
    def construct(self):
        m = TM()
        items = std(m, prog=True)
        self.add(*items, *base_tags(m))
        P = m.p
        tint = Rectangle(width=3.3 * m.s, height=2.4 * m.s, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to(P(0, -1.2))
        dl = DashedLine(P(-1.85, 0), P(1.85, 0), color=TEXT, stroke_width=3.5)
        l_v = lab("ventral half", P(-2.45, 0)[0], P(0, -1.2)[1], TEXT, 28, "r")
        self.at("ventral half")
        self.play(FadeIn(tint), Create(dl), FadeIn(l_v), run_time=0.8)
        self.at("five stripes")
        st = stripes(m)
        self.play(FadeOut(l_v), FadeOut(dl), FadeOut(tint), LaggedStart(*[Create(s) for s in st], lag_ratio=0.1), run_time=1.3)
        labels = VGroup()
        for n in NAMES:
            y = RY[STRIPE_ROW[n]]
            labels.add(VGroup(lab(n, P(-2.35, 0)[0], P(0, y)[1], TEXT, 26, "r", weight=BOLD),
                              Line(P(-2.3, y), P(-1.68, y), color=TEXT, stroke_width=2.5)))
        h_d = lab("domains", P(-2.35, 0)[0], P(0, 0.35)[1], TEXT, 26, "r")
        self.at("called domains")
        self.play(FadeIn(h_d), LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in labels], lag_ratio=0.2), run_time=1.0)
        tags = VGroup()
        for n in NAMES:
            y = RY[STRIPE_ROW[n]]
            tags.add(VGroup(Line(P(1.68, y), P(2.5, y), color=GREY, stroke_width=2.5),
                            RoundedRectangle(corner_radius=0.07, width=1.5, height=0.36, stroke_color=GREY, stroke_width=2.5).move_to(P(3.25, y))))
        h_n = lab("neuron class", P(3.25, 0)[0], P(0, 0.35)[1], TEXT, 26)
        self.at("each makes")
        self.play(FadeIn(h_n), LaggedStart(*[FadeIn(t, shift=LEFT * 0.15) for t in tags], lag_ratio=0.15), run_time=0.6)
        self.at("one class of")
        self.play(LaggedStart(*[Indicate(t[1], color=TEXT, scale_factor=1.15) for t in tags], lag_ratio=0.25), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
PUZZLES = ["Who marks the bottom?", "What is the signal?", "How is a slope read?", "How does a slope become lines?"]
BOX_YS = [2.55, 0.85, -0.85, -2.55]
SMALL = dict(s=0.86, cx=-4.9, cy=0.15)


def map_stack(m, with_stripes=True):
    items = std(m, prog=True)
    if with_stripes:
        items.append(stripes(m))
    return VGroup(*items)


class S11Puzzles(SS):
    def construct(self):
        m = TM()
        g = map_stack(m)
        self.add(g)
        boxes = [qbox(i + 1, y) for i, y in enumerate(BOX_YS)]
        self.at("map raises")
        self.play(g.animate.scale(SMALL["s"]).move_to([SMALL["cx"], 0.0, 0]), FadeIn(boxes[0][0], rate_func=lambda t: max(0.0, 2 * t - 1)), FadeIn(boxes[0][1], rate_func=lambda t: max(0.0, 2 * t - 1)), run_time=0.8)
        self.at("four puzzles")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(b), FadeIn(n)) for b, n in boxes[1:]], lag_ratio=0.25), run_time=1.0)
        texts = [lab(t, -1.8, y, TEXT, 30, "l") for t, y in zip(PUZZLES, BOX_YS)]
        for cue, t in zip(["who marks the bottom", "what is the signal", "how is a slope read", "how does a slope become lines"], texts):
            self.at(cue)
            self.play(FadeIn(t, shift=RIGHT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def zoom_drawing():
    """Big close-up of the notochord touching the floor plate."""
    no = Circle(radius=1.1, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.4).move_to([0, -1.7, 0])
    fb = RoundedRectangle(corner_radius=0.07, width=3.4, height=0.55, stroke_color=TEAL, stroke_width=4, fill_color=TEAL,
                          fill_opacity=0.55).move_to([0, -0.33, 0])
    cells = VGroup(*[RoundedRectangle(corner_radius=0.07, width=0.82, height=0.42, stroke_color=GREY, stroke_width=2,
                                      fill_color=GREY, fill_opacity=0.18).move_to([x, y, 0])
                     for y in (0.28, 0.76, 1.24, 1.72, 2.2) for x in (-1.275, -0.425, 0.425, 1.275)])
    return no, fb, cells


class S12Likeness(SS):
    def construct(self):
        m = TM(**SMALL)
        g = map_stack(m)
        boxes = [qbox(i + 1, y) for i, y in enumerate(BOX_YS)]
        texts = [lab(t, -1.8, y, TEXT, 30, "l") for t, y in zip(PUZZLES, BOX_YS)]
        self.add(g)
        for (b, n), t in zip(boxes, texts):
            self.add(b, n, t)
        self.at("start with the first")
        b1, n1, t1 = boxes[0][0], boxes[0][1], texts[0]
        self.play(FadeOut(VGroup(*[boxes[i][k] for i in (1, 2, 3) for k in (0, 1)], *texts[1:])),
                  b1.animate.set_stroke(GOLD, 4).set_fill(GOLD, 0.15), run_time=0.6)
        top = VGroup(b1, n1, t1)
        no, fb, cells = zoom_drawing()
        l_n = lab("notochord", 0, -1.7, TEXT, 30)
        l_f = lab("floor plate", 0, -0.33, TEXT, 28)
        self.play(top.animate.move_to([0, 3.15, 0]), FadeOut(g, scale=1.6),
                  FadeIn(cells, scale=0.8), FadeIn(no, scale=0.8), FadeIn(fb, scale=0.8), run_time=0.9)
        self.at("and floor plate", lead=0.55)
        self.play(FadeIn(l_n), run_time=0.4)
        self.at("floor plate touch")
        self.play(FadeIn(l_f), run_time=0.4)
        self.at("touch and share")
        cl = Line([-1.0, -0.6, 0], [1.0, -0.6, 0], color=TEXT, stroke_width=5)
        self.play(Create(cl), run_time=0.5)
        sq = lambda x, y: Square(side_length=0.34, stroke_width=0, fill_color=LIGHT_TEAL, fill_opacity=1).move_to([x, y, 0])
        m_n = VGroup(sq(-0.6, -1.15), sq(0.6, -1.15))
        m_f = VGroup(sq(-1.45, -0.33), sq(1.45, -0.33))
        ln = VGroup(DashedLine(m_n[0].get_center(), m_f[0].get_center(), color=LIGHT_TEAL, stroke_width=3),
                    DashedLine(m_n[1].get_center(), m_f[1].get_center(), color=LIGHT_TEAL, stroke_width=3))
        l_sf = lab("shared features", 2.4, -1.95, LIGHT_TEAL, 28, "l")
        ll = VGroup(Line([2.35, -1.8, 0], [0.8, -1.2, 0], color=LIGHT_TEAL, stroke_width=2.5),
                    Line([2.35, -1.7, 0], [1.65, -0.45, 0], color=LIGHT_TEAL, stroke_width=2.5))
        self.at("share features")
        self.play(FadeIn(m_n, scale=0.5), FadeIn(m_f, scale=0.5), Create(ln), run_time=0.8)
        self.play(FadeIn(l_sf), Create(ll), run_time=0.4)
        c1 = lab("shared history?", -4.3, -0.55, TEXT, 30)
        anc = Dot([-4.3, 1.5, 0], radius=0.24, color=GREY)
        k1, k2 = Dot([-5.2, 0.4, 0], radius=0.24, color=TEAL), Dot([-3.4, 0.4, 0], radius=0.24, color=TEAL)
        fork = VGroup(Line(anc.get_center(), k1.get_center(), color=GREY, stroke_width=5),
                      Line(anc.get_center(), k2.get_center(), color=GREY, stroke_width=5), anc, k1, k2)
        self.at("shared history")
        self.play(FadeIn(c1), FadeIn(fork, lag_ratio=0.3), run_time=0.9)
        c2 = lab("instruction?", 4.4, -0.55, TEXT, 30)
        s1 = Dot([3.4, 0.95, 0], radius=0.3, color=TEAL)
        s2 = Dot([5.4, 0.95, 0], radius=0.3, color=GREY)
        ins = VGroup(s1, arr([3.75, 0.95, 0], [5.0, 0.95, 0], TEAL, 6, 0.25), s2)
        self.at("an instruction")
        self.play(FadeIn(c2), FadeIn(ins, lag_ratio=0.3), run_time=0.9)
        self.finish()


class S13Graft(SS):
    def construct(self):
        ex, ey = -3.9, -0.1
        eggs = Ellipse(width=4.6, height=6.2, stroke_color=TEXT, stroke_width=4, fill_color="#EDEBE4", fill_opacity=0.14).move_to([ex, ey, 0])
        alb = VGroup(eggs)
        yolk = Circle(radius=1.85, stroke_color="#E8D9A8", stroke_width=3, fill_color="#E8D9A8", fill_opacity=0.42).move_to([ex, ey + 0.45, 0])
        yc = np.array([ex, ey + 0.45, 0.0])
        vess = VGroup(*[Line(yc + 0.55 * np.array([np.cos(a_), np.sin(a_), 0]), yc + 1.75 * np.array([np.cos(a_ + 0.15), np.sin(a_ + 0.15), 0]),
                             color=TEXT, stroke_width=2, stroke_opacity=0.35) for a_ in np.linspace(0, TAU, 14, endpoint=False)])
        body = Arc(radius=0.8, start_angle=PI * 0.2, angle=PI * 1.2, stroke_color=TEXT, stroke_width=26).move_arc_center_to(yc + np.array([0.05, -0.1, 0]))
        head = Circle(radius=0.5, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=1).move_to(body.get_start() + np.array([0.05, 0.1, 0]))
        eye = VGroup(Circle(radius=0.15, stroke_width=0, fill_color=BG, fill_opacity=1), Dot(radius=0.06, color=TEXT)).move_to(head.get_center() + np.array([0.12, 0.1, 0]))
        tail = Line(body.get_end(), body.get_end() + np.array([0.2, -0.55, 0]), color=TEXT, stroke_width=10)
        limb = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(yc + np.array(p_)) for p_ in ((-0.55, 0.55, 0), (-0.55, -0.45, 0))])
        embryo = VGroup(body, head, eye, tail, limb)
        self.play(FadeIn(alb), FadeIn(yolk), run_time=0.5)
        yr = lab("1990", 0.1, -0.7, GOLD, 80, "l", weight=BOLD)
        self.at("1990")
        self.play(FadeIn(yr, shift=UP * 0.15), run_time=0.5)
        line1 = VGroup(*[T(s, 30, TEXT) for s in ("Placzek,", "Tessier-Lavigne,")]).arrange(RIGHT, buff=0.2)
        line2 = VGroup(*[T(s, 30, TEXT) for s in ("Yamada,", "Jessell", "and Dodd")]).arrange(RIGHT, buff=0.2)
        line1.move_to([0, 1.55, 0]).align_to([0.1, 0, 0], LEFT)
        line2.move_to([0, 0.95, 0]).align_to([0.1, 0, 0], LEFT)
        self.at("placzek")
        self.play(FadeIn(line1[0], shift=UP * 0.12), run_time=0.45)
        self.at("with thomas")
        self.play(FadeIn(line2[1], shift=UP * 0.12), run_time=0.45)
        self.at("jane dodd")
        self.play(FadeIn(line2[2], shift=UP * 0.12), run_time=0.45)
        self.at("colleagues")
        self.play(FadeIn(line1[1], shift=UP * 0.12), FadeIn(line2[0], shift=UP * 0.12), run_time=0.5)
        l_e = lab("chick embryo", ex, -3.55, TEXT, 30)
        l_el = Line([ex, -3.3, 0], [ex, -0.9, 0], color=TEXT, stroke_width=2.5)
        self.at("chick embryos")
        self.play(FadeIn(vess), Create(body), FadeIn(head), FadeIn(eye), Create(tail), FadeIn(limb), FadeIn(l_e), Create(l_el), run_time=1.0)
        self.finish()


class S14Graft2(SS):
    def construct(self):
        m = TM()
        items = std(m, prog=True)
        w = items[2]
        self.add(*items, *base_tags(m))
        g = m.noto(0, 0)
        g.move_to([6.2, m.p(0, GRAFT[1])[1], 0])
        l_g = lab("graft", m.p(2.85, 0)[0], m.p(0, GRAFT[1])[1], TEAL, 28, "l")
        l_p = lab("floor-plate\nproperties", m.p(2.85, 0)[0], m.p(0, -1.0)[1], TEAL, 28, "l", line_spacing=0.9)
        l_pl = Line(m.p(2.8, -0.8), m.p(1.65, -0.3), color=TEAL, stroke_width=2.5)
        self.at("grafted beside")
        self.play(g.animate.move_to(m.p(*GRAFT)), run_time=1.1)
        self.at("sidewall")
        self.play(FadeIn(l_g), run_time=0.4)
        self.at("nearby neural cells")
        self.play(*tealize([w[i][1] for i in GRAFT_ROWS]), run_time=1.2)
        self.at("floor plate properties")
        self.play(FadeIn(l_p), Create(l_pl), Indicate(VGroup(*[w[i][1] for i in GRAFT_ROWS]), color=TEAL), run_time=0.9)
        self.finish()


def midline_pieces(m):
    dl = DashedLine(m.p(0, -2.7), m.p(0, 2.7), color=TEXT, stroke_width=3.5)
    y = 1.92
    ld = Line(m.p(2.85, y), m.p(0.06, y), color=TEXT, stroke_width=2.5)
    tx = lab("midline", m.p(2.95, 0)[0], m.p(0, y)[1], TEXT, 26, "l")
    return dl, ld, tx


def qtext():
    return lab("Remove it early.\nWhat happens\nat the midline?", -5.75, 0.45, TEXT, 30, "l", line_spacing=0.95)


def removed_pieces(m):
    no = m.noto(3.2, -3.2).set_opacity(0.3)
    no.set_stroke(TEAL, opacity=0.5)
    rm = lab("removed", m.p(3.85, 0)[0], m.p(0, -3.2)[1], TEXT, 26, "l")
    return no, rm


class S15Predict(SS):
    def construct(self):
        m = TM()
        items = std(m, prog=True)
        w, fl, no = items[2], items[3], items[5]
        tags = base_tags(m)
        self.add(*items, *tags)
        q = qtext()
        self.at("predict what happens")
        self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=0.8)
        dl, ld, tx = midline_pieces(m)
        self.at("at the midline")
        self.play(Create(dl), Create(ld), FadeIn(tx), Indicate(fl, color=TEAL, scale_factor=1.25), run_time=0.9)
        no2, rm = removed_pieces(m)
        t_noto, t_floor = tags[1], tags[2]
        self.at("remove the normal")
        self.play(no.animate.move_to(m.p(3.2, -3.2)).set_opacity(0.3), FadeOut(t_noto), run_time=1.1)
        slot = m.slot()
        qm = T("?", 48, TEXT, weight=BOLD).move_to(m.p(0, -3.2))
        self.at("notochord early")
        self.play(FadeOut(fl), FadeOut(t_floor), FadeIn(slot), FadeIn(qm), FadeIn(rm), run_time=0.7)
        self.finish()


def removal_frame(m, q=True, qm=True):
    items = std(m, prog=True, floor=None)
    tags = [axis_tags()] + tag_set(m, ["roof", "epi"])
    no2, rm = removed_pieces(m)
    items[-2] = no2   # notochord
    out = items + tags + [m.slot(), rm]
    dl, ld, tx = midline_pieces(m)
    out += [dl, ld, tx]
    if qm:
        out.append(T("?", 48, TEXT, weight=BOLD).move_to(m.p(0, -3.2)))
    if q:
        out.append(qtext())
    return out


class S16Pause(NarratedScene):
    def construct(self):
        self.add(*removal_frame(TM()))
        self.finish()


class S17Reveal(SS):
    def construct(self):
        m = TM()
        out = removal_frame(m)
        self.add(*out)
        q_text, qm = out[-1], out[-2]
        self.play(FadeOut(q_text), run_time=0.5)
        res = lab("no floor-plate\nproperties at\nthe midline", m.p(2.3, 0)[0], m.p(0, -1.75)[1], TEXT, 28, "l", line_spacing=0.95)
        resl = Line(m.p(2.25, -2.45), m.p(0.98, -2.62), color=TEXT, stroke_width=2.5)
        self.at("failed to appear")
        self.play(FadeOut(qm), FadeIn(res, shift=RIGHT * 0.15), Create(resl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
PANEL = dict(s=0.86, cx=-4.7, cy=0.15)


def card(x=3.95, y=0.4, w=5.5, h=2.7):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.07).move_to([x, y, 0])


class S18Suff(SS):
    def construct(self):
        m = TM(**PANEL)
        items = std(m, prog=True)
        w = items[2]
        g = m.graft()
        teal_now([w[i][1] for i in GRAFT_ROWS])
        self.add(*items, g)
        cap = lab("grafted notochord", m.p(2.85, 0)[0], m.p(0, GRAFT[1])[1], TEAL, 26, "l")
        self.add(cap)
        cd = card()
        word = lab("sufficient", 3.95, 1.3, TEAL, 56, weight=BOLD)
        d1 = lab("enough to give the effect", 3.95, 0.35, TEXT, 32)
        d2 = lab("in a new place", 3.95, -0.45, TEXT, 32)
        self.play(FadeIn(cd), run_time=0.5)
        self.at("is sufficient")
        self.play(FadeIn(word, scale=0.9), run_time=0.7)
        self.at("enough to give")
        self.play(FadeIn(d1, shift=UP * 0.1), run_time=0.6)
        self.at("in a new place", lead=0.45)
        patch = VGroup(*[w[i][1] for i in GRAFT_ROWS])
        self.play(FadeIn(d2), Indicate(patch, color=TEAL, scale_factor=1.2), run_time=0.5)
        self.finish()


class S19Nec(SS):
    def construct(self):
        m = TM(**PANEL)
        items = std(m, prog=True, floor=None)
        no2 = m.noto(3.0, -3.2).set_opacity(0.3)
        no2.set_stroke(TEAL, opacity=0.5)
        items[-2] = no2
        slot = m.slot()
        qm = T("?", 36, TEXT, weight=BOLD).move_to(m.p(0, -3.2))
        cap = lab("removed notochord", m.p(3.55, 0)[0], m.p(0, -3.2)[1], TEXT, 26, "l")
        self.add(*items, slot, qm, cap)
        cd = card()
        word = lab("necessary", 3.95, 1.3, TEAL, 56, weight=BOLD)
        d1 = lab("without it,", 3.95, 0.35, TEXT, 32)
        d2 = lab("no normal floor plate", 3.95, -0.45, TEXT, 32)
        self.play(FadeIn(cd), run_time=0.5)
        self.at("is necessary")
        self.play(FadeIn(word, scale=0.9), run_time=0.7)
        self.at("without it")
        self.play(FadeIn(d1, shift=UP * 0.1), run_time=0.6)
        self.at("normal floor plate")
        self.play(FadeIn(d2, shift=UP * 0.1), run_time=0.7)
        self.at("does not form")
        self.play(Indicate(slot, color=TEXT, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20Homeo(SS):
    def construct(self):
        D = np.array([-0.8, 0.0, 0.0])
        dish = Circle(radius=3.35, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.05).move_to(D)
        cr = lab("Placzek, Jessell\nand Dodd, 1993", 2.75, 3.0, TEXT, 26, "l", line_spacing=0.95)
        blk = lambda x, y, col, o, sw=3: RoundedRectangle(corner_radius=0.1, width=2.1, height=1.3, stroke_color=col, stroke_width=sw,
                                                          fill_color=col, fill_opacity=o).move_to([D[0] + x, y, 0])
        fpb, nb = blk(-1.15, 1.2, TEAL, 0.5), blk(0.95, 1.2, GREY, 0.2, 2.5)
        l_f = lab("floor plate", D[0] - 1.15, 2.25, TEAL, 26)
        l_n = lab("neural plate\ntissue", D[0] + 0.95, 2.5, TEXT, 24, line_spacing=0.9)
        msg = arr([D[0] - 1.15, 0.3, 0], [D[0] + 0.95, 0.3, 0], TEXT, 5, 0.22)
        l_msg = lab("message", D[0] - 0.1, -0.1, TEXT, 24)
        self.play(FadeIn(dish), FadeIn(cr), run_time=0.5)
        self.at("floor plate")
        self.play(FadeIn(fpb), FadeIn(l_f), run_time=0.5)
        self.at("passes the message")
        self.play(FadeIn(nb), FadeIn(l_n), run_time=0.5)
        self.play(GrowArrow(msg), FadeIn(l_msg), run_time=0.6)
        l_c = lab("in culture", D[0], 0.0, TEXT, 26)
        self.at("in culture")
        self.play(FadeOut(msg), FadeOut(l_msg), run_time=0.3)
        self.play(FadeIn(l_c), run_time=0.4)
        mk = lambda cx, cy: VGroup(*[Dot([cx + dx, cy + dy, 0], radius=0.11, color=LIGHT_TEAL) for dx in (-0.55, 0.0, 0.55) for dy in (0.3, -0.3)])
        marks = mk(D[0] + 0.95, 1.2)
        self.at("floor plate induced")
        self.play(nb.animate.set_stroke(TEAL, 4).set_fill(TEAL, 0.5), LaggedStart(*[FadeIn(d, scale=0.4) for d in marks], lag_ratio=0.12),
                  run_time=1.0)
        r1 = lab("floor plate induces\nfloor-plate markers", 2.75, 1.2, TEAL, 28, "l", line_spacing=0.95)
        r1l = Line([2.7, 1.2, 0], [D[0] + 2.05, 1.2, 0], color=TEAL, stroke_width=2.5)
        self.at("markers")
        self.play(FadeIn(r1), Create(r1l), run_time=0.5)
        no2 = Circle(radius=0.9, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to([D[0] - 1.15, -1.4, 0])
        nb2 = blk(0.95, -1.4, GREY, 0.2, 2.5)
        l_no = lab("notochord", D[0] - 1.15, -1.4, TEXT, 24)
        self.at("just as")
        self.play(FadeIn(no2), FadeIn(nb2), FadeIn(l_no), run_time=0.7)
        marks2 = mk(D[0] + 0.95, -1.4)
        r2 = lab("just as\nnotochord did", 2.75, -1.4, TEAL, 28, "l", line_spacing=0.95)
        r2l = Line([2.7, -1.4, 0], [D[0] + 2.05, -1.4, 0], color=TEAL, stroke_width=2.5)
        self.at("noticord did")
        self.play(nb2.animate.set_stroke(TEAL, 4).set_fill(TEAL, 0.5), LaggedStart(*[FadeIn(d, scale=0.4) for d in marks2], lag_ratio=0.12),
                  FadeIn(r2), Create(r2l), run_time=0.9)
        self.finish()


class S21Homeo2(SS):
    def construct(self):
        NR, NC, PX, PY = 7, 6, 1.2, 0.96
        cx, gy0 = -2.1, -2.88
        grid = [[RoundedRectangle(corner_radius=0.07, width=1.1, height=0.84, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                                  fill_opacity=0.18).move_to([cx + (c - 2.5) * PX, gy0 + r * PY, 0]) for c in range(NC)] for r in range(NR)]
        for c in grid[0]:
            style_teal(c)
        allc = VGroup(*[c for row in grid for c in row])
        self.play(FadeIn(allc, lag_ratio=0.02), run_time=0.7)
        cl = Line([cx - 3.4, gy0 + PY / 2, 0], [cx + 3.4, gy0 + PY / 2, 0], color=TEXT, stroke_width=5)
        self.at("by contact")
        self.play(Create(cl), run_time=0.6)
        self.play(FadeOut(cl), run_time=0.3)
        title = lab("homeogenetic\ninduction", 4.4, 2.4, TEXT, 44, font=TITLE_FONT, line_spacing=0.9)
        self.at("homeogenetic induction")
        self.play(FadeIn(title, shift=UP * 0.12), run_time=0.7)
        l_i = lab("induced tissue", 2.0, gy0, TEAL, 28, "l")
        bi = Line([1.7, gy0 - 0.38, 0], [1.7, gy0 + 0.38, 0], color=TEAL, stroke_width=4)
        self.at("an induced tissue")
        self.play(FadeIn(l_i), Create(bi), run_time=0.5)
        l_nb = lab("its neighbors", 2.0, 0.4, TEXT, 28, "l")
        br = Line([1.7, gy0 + PY - 0.38, 0], [1.7, gy0 + 6 * PY + 0.38, 0], color=TEXT, stroke_width=3)
        self.at("recruits its neighbors")
        for r in range(1, NR):
            extra = [FadeIn(l_nb), Create(br)] if r == 1 else []
            self.play(*extra, *[c.animate.set_stroke(TEAL, 3).set_fill(TEAL, 0.6) for c in grid[r]], run_time=0.25)
        l_s = lab("same identity", 2.0, -0.8, TEAL, 28, "l")
        self.at("the same identity")
        self.play(FadeIn(l_s), run_time=0.5)
        self.finish()


class S22Rule(SS):
    def construct(self):
        N, SP, CH = 12, 0.52, 0.46
        ys = [(i - 5.5) * SP for i in range(N)]
        cells = VGroup(*[RoundedRectangle(corner_radius=0.07, width=1.9, height=CH, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                                          fill_opacity=0.18).move_to([-4.9, y, 0]) for y in ys])
        head = lab("One idea, every chapter", 2.6, 2.75, TEXT, 46, font=TITLE_FONT)
        self.play(FadeIn(cells, lag_ratio=0.03), run_time=0.6)
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.6)
        r1 = T("The neighbors supply\na slope.", 42, TEXT, t2c={"slope": YELLOW}, line_spacing=0.95).move_to([2.6, 0.95, 0])
        r2 = T("The progenitors draw\nthe lines.", 42, TEXT, line_spacing=0.95).move_to([2.6, -1.45, 0])
        l_sl = lab("slope", -4.9, -3.5, YELLOW, 28)
        self.at("neighbors supply a slope")
        self.play(FadeIn(r1, shift=RIGHT * 0.2), FadeIn(l_sl),
                  *[c.animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.1 + 0.7 * float(np.exp(-i / 3.5))) for i, c in enumerate(cells)],
                  run_time=1.4)
        groups = [(0, 1), (2, 4), (5, 6), (7, 9), (10, 11)]
        cols = [ORANGE, MOTOR, PURPLE, GREEN, DORSAL]
        bands = VGroup()
        for (a, b), col in zip(groups, cols):
            lo, hi = ys[a] - CH / 2, ys[b] + CH / 2
            bands.add(RoundedRectangle(corner_radius=0.07, width=0.6, height=hi - lo, stroke_color=col, stroke_width=3,
                                       fill_color=col, fill_opacity=0.55).move_to([-3.2, (lo + hi) / 2, 0]))
        l_d = lab("domains", -3.2, 3.5, TEXT, 28)
        self.at("progenitors draw")
        self.play(FadeIn(r2, shift=RIGHT * 0.2), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in bands], lag_ratio=0.3), FadeIn(l_d), run_time=1.3)
        self.finish()


class S23Takeaway(SS):
    def construct(self):
        m = TM(s=0.9, cx=-3.3, cy=0.15)
        items = std(m, prog=True)
        w, fl = items[2], items[3]
        tags = [axis_tags()] + tag_set(m, ["noto", "floor", "roof", "epi"], {"floor": "R"})
        self.add(*items, *tags)
        P = m.p
        bx, by, bw, bh = 3.85, 1.55, 5.9, 4.1
        b = RoundedRectangle(corner_radius=0.14, width=bw, height=bh, stroke_color=GOLD, stroke_width=4, fill_color=GOLD,
                             fill_opacity=0.1).move_to([bx, by, 0])
        n = T("1", 40, GOLD, weight=BOLD).move_to([bx - bw / 2 + 0.5, by + 1.2, 0])
        hd = lab("Who marks the bottom?", bx - bw / 2 + 1.0, by + 1.2, TEXT, 30, "l")
        tk = lab("TAKEAWAY", bx - bw / 2 + 0.3, by + bh / 2 - 0.3, GOLD, 22, "l")
        self.at("the takeaway")
        self.play(FadeIn(b), FadeIn(n), FadeIn(hd), FadeIn(tk), run_time=0.8)
        c_t = chip("told", TEAL, 30)
        c_r = chip("then recruits", TEAL, 30)
        a_tr = arr([0, 0, 0], [0.5, 0, 0], TEXT, 5, 0.2)
        row = VGroup(c_t, a_tr, c_r).arrange(RIGHT, buff=0.2).move_to([bx, by - 0.5, 0])
        self.at("is told")
        self.play(FadeIn(c_t, scale=0.9), Indicate(fl, color=TEAL, scale_factor=1.3), run_time=0.7)
        l_rec = lab("recruited to\nfloor-plate identity", P(2.2, 0)[0], P(0, -1.55)[1], TEAL, 24, "l", line_spacing=0.9)
        l_recl = Line(P(2.15, -1.9), P(1.68, -2.1), color=TEAL, stroke_width=2.5)
        self.at("it recruits")
        self.play(GrowArrow(a_tr), FadeIn(c_r, shift=LEFT * 0.2),
                  *[w[0][j].animate.set_stroke(TEAL, 3).set_fill(TEAL, 0.4) for j in (0, 1)], FadeIn(l_rec), Create(l_recl), run_time=1.0)
        qa = arr(P(0.55, -3.2), P(2.2, -3.2), TEXT, 6, 0.25)
        qm = T("?", 60, TEXT, weight=BOLD).move_to(P(2.75, -3.2))
        self.at("something passes")
        self.play(GrowArrow(qa), FadeIn(qm, scale=0.6), run_time=0.8)
        ans = lab("The notochord.", bx - bw / 2 + 1.0, by + 0.5, TEAL, 30, "l")
        self.at("noticord")
        self.play(FadeIn(ans, shift=RIGHT * 0.15), Indicate(items[5], color=TEAL, scale_factor=1.12), run_time=0.7)
        wi = lab("What is it?", 4.0, -2.35, TEXT, 54, font=TITLE_FONT)
        self.at("what is it")
        self.play(FadeIn(wi, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S24End(EndCard):
    LINE = "In these assays, the bottom is told, then recruits its neighbors."
