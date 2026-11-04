"""Neurotrophins, Trk Receptors and p75, chapter 6: Reading One Factor Two Ways

COLOR MAP (one color per concept, shared by every chapter of this lesson)
  BLUE   = the neurotrophin (NGF) itself, mature or precursor body; the dial of free NGF
  ORANGE = the pro-domain (the extra stretch at the front of proNGF)
  PINK   = Trk receptors (TrkA) and the Trk-linked sites
  VIOLET = p75 and the p75-alone sites
  YELLOW = sortilin
  GOLD   = the cut (the cutting enzymes)
  GREEN  = survival
  RED    = death
  GREY   = membranes, cells, outlines, notebooks, unknowns, scope notes
  TEXT   = rules, questions and the takeaway

Every number on the bars and on the plot is computed from fraction occupied = [NGF] / ([NGF] + Kd).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E879B9"
ORANGE = "#F29E4C"
VIOLET = "#A98BE0"

# Illustration values from the script: orders of magnitude, in molar.
KD_TRK = 1e-11          # about 10 pM
KD_P75 = 1e-9           # about 1 nM (rounded)
KD_P75_MEASURED = 2e-9  # 2 nM, as measured


def occ(c, kd):
    return c / (c + kd)


# ------------------------------------------------------------------ small helpers
def lab(text, color, x, y, size=26, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def mono(text, color, x, y, size=26):
    return M(text, size, color).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.3, color=RED, w=7):
    cx, cy = center[0], center[1]
    return VGroup(Line([cx - size, cy - size, 0], [cx + size, cy + size, 0], color=color, stroke_width=w),
                  Line([cx - size, cy + size, 0], [cx + size, cy - size, 0], color=color, stroke_width=w))


def dimer(cx, cy, s=1.0, tails=False, color=BLUE):
    """NGF drawn as a pair of blobs; with tails=True the two ORANGE pro-domains stand up from it."""
    bodies, tl = [], []
    for sx in (-1, 1):
        b = Ellipse(width=0.95 * s, height=0.75 * s, stroke_color=color, stroke_width=3,
                    fill_color=color, fill_opacity=0.5).move_to([cx + sx * 0.5 * s, cy, 0])
        bodies.append(b)
        if tails:
            t = RoundedRectangle(corner_radius=0.1 * s, width=0.26 * s, height=0.8 * s, stroke_color=ORANGE,
                                 stroke_width=3, fill_color=ORANGE, fill_opacity=0.65)
            t.move_to([cx + sx * 0.5 * s, cy + 0.375 * s + 0.32 * s, 0])
            tl.append(t)
    g = VGroup(*bodies, *tl)
    g.bodies = VGroup(*bodies)
    g.tails = VGroup(*tl)
    return g


def site(angle_deg, center, r, color, top=1.4, foot=True):
    """A receptor standing radially on a round cell: extracellular bar outside, round foot inside."""
    bar = RoundedRectangle(corner_radius=0.16, width=0.42, height=top + 0.2, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.55).move_to([0, (top - 0.2) / 2, 0])
    parts = [bar]
    if foot:
        parts.append(Circle(radius=0.24, stroke_color=color, stroke_width=3, fill_color=color,
                            fill_opacity=0.4).move_to([0, -0.42, 0]))
    g = VGroup(*parts)
    a = np.deg2rad(angle_deg)
    g.rotate(a - PI / 2, about_point=ORIGIN)
    g.shift([center[0] + r * np.cos(a), center[1] + r * np.sin(a), 0])
    g.bar = bar
    return g


def round_cell(x, y, r, color=GREY, fill=0.12):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill).move_to([x, y, 0])


def flat_rcp(x, my, color, top=1.5, foot=True, w=0.45):
    """A receptor in a flat membrane at height my."""
    bar = RoundedRectangle(corner_radius=0.16, width=w, height=top + 0.45, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.55).move_to([x, my + (top - 0.45) / 2, 0])
    parts = [bar]
    ft = None
    if foot:
        ft = Circle(radius=0.27, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.4)
        ft.move_to([x, my - 0.7, 0])
        parts.append(ft)
    g = VGroup(*parts)
    g.bar, g.foot = bar, ft
    return g


def fmt_conc(c):
    if c < 1e-9:
        return f"{c * 1e12:.0f} pM"
    return f"{c * 1e9:.0f} nM"


def fmt_pct(f):
    if 0.99 < f < 0.9995:
        return ">99%"
    return f"{f * 100:.0f}%"




# ------------------------------------------------------------------ the dial and the two bars
DIAL_X = -5.0
DIAL_Y0 = -2.6
DIAL_DEC = 1.3
LOG0 = -12
BAR_Y0 = -2.6
BAR_H = 5.2
BAR_W = 1.6
BAR_X = {"t": -1.5, "p": 2.3}
BAR_COL = {"t": PINK, "p": VIOLET}
BAR_KD = {"t": KD_TRK, "p": KD_P75}
C2 = float(np.log10(2e-9))


def dial_y(logc):
    return DIAL_Y0 + (logc - LOG0) * DIAL_DEC


def dial_static():
    axis = Line([DIAL_X, DIAL_Y0, 0], [DIAL_X, dial_y(-8), 0], color=TEXT, stroke_width=5)
    parts = [axis]
    for lc, txt in [(-12, "1 pM"), (-11, "10 pM"), (-10, "100 pM"), (-9, "1 nM"), (-8, "10 nM")]:
        y = dial_y(lc)
        parts.append(Line([DIAL_X - 0.12, y, 0], [DIAL_X + 0.12, y, 0], color=TEXT, stroke_width=4))
        t = T(txt, 26, TEXT)
        t.move_to([DIAL_X - 0.22 - t.width / 2, y, 0])
        parts.append(t)
    parts.append(lab("free mature NGF", BLUE, DIAL_X + 0.4, 3.3, 28))
    return VGroup(*parts)


def bar_frames():
    return VGroup(*[Rectangle(width=BAR_W, height=BAR_H, stroke_color=GREY, stroke_width=3, fill_opacity=0)
                    .move_to([BAR_X[k], BAR_Y0 + BAR_H / 2, 0]) for k in "tp"])


def bar_names():
    a = lab("Trk-linked sites", PINK, BAR_X["t"], -3.0, 28)
    b = lab("p75-alone sites", VIOLET, BAR_X["p"], -3.0, 28)
    return VGroup(a, b)


def bar_kds(kdp="Kd about 1 nM"):
    a = mono("Kd about 10 pM", PINK, BAR_X["t"], -3.5, 26)
    b = mono(kdp, VIOLET, BAR_X["p"], -3.5, 26)
    return VGroup(a, b)


def pulse(scene, mob, color, base=GREY, rt=0.4):
    """Highlight a bar frame without drawing anything extra."""
    scene.play(mob.animate.set_stroke(color, 8), run_time=rt)
    scene.play(mob.animate.set_stroke(base, 3), run_time=rt)


class Stage:
    """The dial and the two occupancy bars. Rebuild it at the same place in every scene that uses it."""

    def __init__(self, logc=-12.0, rt=0.0, rp=0.0, kds=False, names=True, vis=1.0, band=False, rb=0.0,
                 kdp="Kd about 1 nM"):
        self.band = band
        self.c = ValueTracker(logc)
        self.vis = ValueTracker(vis)
        self.rb = ValueTracker(rb)
        self.r = {"t": ValueTracker(rt), "p": ValueTracker(rp)}
        self.dial = dial_static()
        self.frames = bar_frames()
        self.names = bar_names() if names else VGroup()
        self.kds = bar_kds(kdp) if kds else VGroup()
        self.pointer = always_redraw(self._pointer)
        self.fills = {k: always_redraw(lambda k=k: self._fill(k)) for k in "tp"}
        self.pcts = {k: always_redraw(lambda k=k: self._pct(k)) for k in "tp"}

    def conc(self):
        return 10 ** self.c.get_value()

    def lo(self):
        """p75 occupancy with the measured Kd (solid part of the band)."""
        return occ(self.conc(), KD_P75_MEASURED)

    def hi(self):
        """p75 occupancy with the rounded Kd (light extension of the band)."""
        return occ(self.conc(), KD_P75)

    def frac(self, k):
        if k == "p" and self.band:
            return self.r["p"].get_value() * self.lo()
        return self.r[k].get_value() * occ(self.conc(), BAR_KD[k])

    def _pointer(self):
        v = self.vis.get_value()
        y = dial_y(self.c.get_value())
        tri = Polygon([DIAL_X + 0.08, y, 0], [DIAL_X + 0.42, y + 0.17, 0], [DIAL_X + 0.42, y - 0.17, 0],
                      stroke_width=0, fill_color=BLUE, fill_opacity=v)
        rd = M(fmt_conc(self.conc()), 28, BLUE)
        rd.move_to([DIAL_X + 0.55 + rd.width / 2, y, 0])
        rd.set_opacity(v)
        return VGroup(tri, rd)

    def _rect(self, k, y_bottom, h, op):
        rect = Rectangle(width=BAR_W - 0.06, height=h, stroke_width=0, fill_color=BAR_COL[k], fill_opacity=op)
        rect.move_to([BAR_X[k], y_bottom + h / 2, 0])
        return rect

    def _fill(self, k):
        f = self.frac(k)
        out = VGroup()
        if f >= 0.002:
            h = max(f * BAR_H, 0.05)
            out.add(self._rect(k, BAR_Y0, h, 0.8))
        if k == "p" and self.band:
            ext = self.rb.get_value() * (self.hi() - self.lo()) * BAR_H
            if ext > 0.02:
                out.add(self._rect(k, BAR_Y0 + self.frac(k) * BAR_H, ext, 0.35))
        return out

    def _pct(self, k):
        r = self.r[k].get_value()
        if r < 0.02:
            return VGroup()
        if k == "p" and self.band:
            if r < 0.98:
                return VGroup()
            if self.rb.get_value() < 0.98:
                txt = f"{self.lo() * 100:.0f}%"
            else:
                txt = f"about {self.lo() * 100:.0f} to {self.hi() * 100:.0f}%"
            return M(txt, 28, BAR_COL[k]).move_to([BAR_X[k], 3.0, 0])
        return M(fmt_pct(self.frac(k)), 28, BAR_COL[k]).move_to([BAR_X[k], 3.0, 0])

    def mobs(self, dial=True):
        out = [self.frames, self.names, self.kds, self.fills["t"], self.fills["p"], self.pcts["t"], self.pcts["p"]]
        if dial:
            out += [self.dial, self.pointer]
        return out


# ------------------------------------------------------------------ dishes, notebooks, cards
def dish(cx, cy, w=4.6, h=3.2, rows=3, cols=4, r=0.3):
    box = RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])
    cells = VGroup()
    dx, dy = (w - 1.0) / cols, (h - 0.9) / rows
    for i in range(rows):
        for j in range(cols):
            c = Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
            c.move_to([cx - (cols - 1) / 2 * dx + j * dx, cy + (rows - 1) / 2 * dy - i * dy, 0])
            cells.add(c)
    g = VGroup(box, cells)
    g.box, g.cells = box, cells
    return g


def notebook(cx, cy, title, result, color, caption, w=3.3, h=4.4):
    body = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=GREY, stroke_width=4,
                            fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])
    spine = Rectangle(width=0.32, height=h - 0.1, stroke_width=0, fill_color=GREY,
                      fill_opacity=0.5).move_to([cx - w / 2 + 0.25, cy, 0])
    ttl = T(title, 30, TEXT).move_to([cx + 0.15, cy + h / 2 - 0.55, 0])
    cell = Circle(radius=0.62, stroke_color=color, stroke_width=5, fill_color=color,
                  fill_opacity=0.25 if color == GREEN else 0.4).move_to([cx + 0.15, cy + 0.15, 0])
    parts = [body, spine, ttl, cell]
    if result == "die":
        parts.append(cross([cx + 0.15, cy + 0.15, 0], 0.35, RED))
    parts.append(T(caption, 28, color).move_to([cx + 0.15, cy - h / 2 + 0.75, 0]))
    return VGroup(*parts)


def two_notebooks():
    return (notebook(-3.9, 0.0, "Lab 1", "die", RED, "neurons die"),
            notebook(3.9, 0.0, "Lab 2", "live", GREEN, "weak survival"))


def card_frame(cx, cy, w=4.1, h=5.0):
    return RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.07).move_to([cx, cy, 0])


def card_head(cx, cy, num, title, w=4.1, h=5.0):
    badge = VGroup(Circle(radius=0.28, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1),
                   T(num, 28, TEXT, weight=BOLD)).move_to([cx - w / 2 + 0.5, cy + h / 2 - 0.55, 0])
    t = T(title, 28, TEXT).move_to([cx + 0.4, cy + h / 2 - 0.55, 0])
    return VGroup(badge, t)


CARD_X = [-4.4, 0.0, 4.4]
CARD_Y = -0.15


def card1_icon(cx, cy):
    pro = dimer(cx, cy + 0.55, 1.1, tails=True)
    cutl = DashedLine([cx - 1.2, cy + 0.96, 0], [cx + 1.2, cy + 0.96, 0], color=GOLD, stroke_width=5)
    mat = dimer(cx - 0.3, cy - 0.7, 1.1)
    ml = lab("mature NGF", BLUE, cx - 0.2, cy - 1.6, 26)
    free = RoundedRectangle(corner_radius=0.1, width=0.25, height=0.75, stroke_color=ORANGE, stroke_width=3,
                            fill_color=ORANGE, fill_opacity=0.65).move_to([cx + 1.5, cy - 0.2, 0]).rotate(0.5)
    return pro, cutl, mat, ml, free


def card2_icon(cx, cy):
    rs = []
    for x, col, nm in zip([cx - 1.3, cx, cx + 1.3], [PINK, VIOLET, YELLOW], ["TrkA", "p75", "sortilin"]):
        bar = RoundedRectangle(corner_radius=0.16, width=0.5, height=1.7, stroke_color=col, stroke_width=3,
                               fill_color=col, fill_opacity=0.55).move_to([x, cy + 0.25, 0])
        ft = Circle(radius=0.28, stroke_color=col, stroke_width=3, fill_color=col,
                    fill_opacity=0.4).move_to([x, cy - 0.85, 0])
        rs.append(VGroup(bar, ft, lab(nm, col, x, cy - 1.5, 26)))
    return VGroup(*rs)


def card3_icon(cx, cy):
    def row(y, cols):
        items = [RoundedRectangle(corner_radius=0.08, width=0.3, height=0.9, stroke_color=c, stroke_width=3,
                                  fill_color=c, fill_opacity=0.55) for c in cols]
        return VGroup(*items).arrange(RIGHT, buff=0.14).move_to([cx, y, 0])
    r1 = row(cy + 1.0, [PINK] * 4 + [VIOLET])
    r2 = row(cy - 0.7, [PINK] + [VIOLET] * 2 + [YELLOW] * 2)
    l1 = lab("mostly TrkA", TEXT, cx, cy + 0.3, 26)
    l2 = lab("mostly p75 and sortilin", TEXT, cx, cy - 1.5, 26)
    return VGroup(VGroup(r1, l1), VGroup(r2, l2))


def mini_card(cx, cy, num, title, w=3.9, h=1.0):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.07).move_to([cx, cy, 0])
    badge = VGroup(Circle(radius=0.26, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1),
                   T(num, 26, TEXT, weight=BOLD)).move_to([cx - w / 2 + 0.5, cy, 0])
    t = T(title, 28, TEXT).move_to([cx + 0.45, cy, 0])
    return VGroup(box, badge, t)


# ------------------------------------------------------------------ question state shared by s08 to s10
def question_text():
    q = VGroup(T("Trk-linked", 36, PINK), T("or p75?", 36, VIOLET)).arrange(DOWN, buff=0.15)
    return q.move_to([5.2, 0.4, 0])


def chosen_label():
    return VGroup(T("chosen", 28, TEXT), T("example", 28, TEXT)).arrange(DOWN, buff=0.05).move_to(
        [-3.6, dial_y(-11) - 0.75, 0])


def p75_ticks():
    y50 = BAR_Y0 + occ(2e-9, KD_P75_MEASURED) * BAR_H
    y67 = BAR_Y0 + occ(2e-9, KD_P75) * BAR_H
    out = []
    for y, txt in [(y50, f"Kd 2 nM: {occ(2e-9, KD_P75_MEASURED) * 100:.0f}%"),
                   (y67, f"Kd 1 nM: {occ(2e-9, KD_P75) * 100:.0f}%")]:
        ln = Line([3.1, y, 0], [3.4, y, 0], color=VIOLET, stroke_width=4)
        tx = M(txt, 26, VIOLET).next_to(ln, RIGHT, buff=0.12)
        out.append(VGroup(ln, tx))
    return out


def band_bar(x, y0=BAR_Y0, h=BAR_H):
    """A p75 bar filled with the computed band: solid to the measured-Kd value, light to the rounded-Kd value."""
    lo, hi = occ(2e-9, KD_P75_MEASURED), occ(2e-9, KD_P75)
    fr = Rectangle(width=BAR_W, height=h, stroke_color=GREY, stroke_width=3).move_to([x, y0 + h / 2, 0])
    solid = Rectangle(width=BAR_W - 0.06, height=lo * h, stroke_width=0, fill_color=VIOLET,
                      fill_opacity=0.8).move_to([x, y0 + lo * h / 2, 0])
    light = Rectangle(width=BAR_W - 0.06, height=(hi - lo) * h, stroke_width=0, fill_color=VIOLET,
                      fill_opacity=0.35).move_to([x, y0 + lo * h + (hi - lo) * h / 2, 0])
    pct = M(f"about {lo * 100:.0f} to {hi * 100:.0f}%", 28, VIOLET).move_to([x, y0 + h + 0.4, 0])
    return fr, VGroup(solid, light), pct


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Neurotrophins, Trk Receptors and p75"
    TITLE = "Reading One Factor Two Ways"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=24, color=TEXT)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        # everything legible from the first frame; no fade-out, so the next scene cuts straight in
        self.add(brand, lesson, title)
        self.play(GrowFromCenter(rule), run_time=0.6)
        self.finish()


class S01(SpokenScene):
    def construct(self):
        n = round_cell(-3.6, -0.6, 1.7)
        n_sites = VGroup(site(120, [-3.6, -0.6], 1.7, PINK), site(95, [-3.6, -0.6], 1.7, PINK),
                         site(70, [-3.6, -0.6], 1.7, VIOLET), site(45, [-3.6, -0.6], 1.7, VIOLET))
        o = round_cell(3.6, -0.6, 1.7)
        procs = VGroup(*[Line([3.6 + 1.7 * np.cos(a), -0.6 + 1.7 * np.sin(a), 0],
                              [3.6 + 2.15 * np.cos(a), -0.6 + 2.15 * np.sin(a), 0], color=GREY, stroke_width=5)
                         for a in np.deg2rad([200, 245, 295, 340])])
        o_sites = VGroup(site(125, [3.6, -0.6], 1.7, VIOLET), site(90, [3.6, -0.6], 1.7, VIOLET),
                         site(55, [3.6, -0.6], 1.7, VIOLET))
        nl = lab("sympathetic neuron", TEXT, -3.6, -3.1, 28)
        ol = lab("oligodendrocyte", TEXT, 3.6, -3.1, 28)
        d0 = dimer(0, 2.55, 1.0)
        dl = lab("mature NGF", BLUE, 0, 1.55, 30)
        self.add(n, n_sites, o, procs, o_sites, nl, ol, d0, dl)
        self.at("keeps neurons alive")
        d1 = d0.copy()
        self.add(d1)
        self.play(d1.animate.move_to([-3.3, 3.2, 0]), run_time=0.6)
        alive = lab("alive", GREEN, -3.6, -0.6, 34)
        self.play(n.animate.set_stroke(GREEN), FadeIn(alive), run_time=0.4)
        self.at("kill cells")
        d2 = d0.copy()
        self.add(d2)
        self.play(d2.animate.move_to([3.4, 3.2, 0]), run_time=0.4)
        dying = lab("dying", RED, 3.6, -0.6, 34)
        self.play(o.animate.set_stroke(RED).set_fill(RED, 0.25), FadeIn(dying), run_time=0.3)
        self.at("lack track")
        nt = VGroup(T("lacks", 28, PINK), T("TrkA", 28, PINK)).arrange(DOWN, buff=0.05).move_to([5.95, 0.6, 0])
        self.play(FadeIn(nt), Indicate(o_sites, color=VIOLET), run_time=0.7)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        pro = dimer(0, 0.7, 1.3, tails=True)
        pl = lab("proNGF", BLUE, 0, -0.65, 32)
        self.add(pro, pl)
        self.at("kill neurons")
        nb1, nb2 = two_notebooks()
        self.play(FadeIn(nb1, shift=RIGHT * 0.3), run_time=0.7)
        self.at("keep them weakly")
        self.play(FadeIn(nb2, shift=LEFT * 0.3), run_time=0.7)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        st = Stage(logc=-12.0)
        self.add(st.dial, st.pointer, st.frames, st.names)
        self.at("first question")
        pulse(self, st.frames[0], PINK, rt=0.3)
        pulse(self, st.frames[1], VIOLET, rt=0.3)
        self.at("the precursor needs")
        pro = dimer(5.0, 0.3, 1.2, tails=True)
        prl = lab("precursor", BLUE, 5.0, -0.85, 30)
        self.play(FadeIn(pro), FadeIn(prl), run_time=0.6)
        self.at("pro domain")
        pd = lab("pro-domain", ORANGE, 5.0, 2.2, 30)
        self.play(*[t.animate.set_fill(ORANGE, 1.0) for t in pro.tails], FadeIn(pd), run_time=0.7)
        self.finish()


def neuron_group(sites_color=False):
    cell = round_cell(0, -1.4, 2.1)
    col_t = PINK if sites_color else GREY
    col_p = VIOLET if sites_color else GREY
    st = VGroup(*[site(a, [0, -1.4], 2.1, col_t) for a in [162, 140, 118]])
    sp = VGroup(*[site(a, [0, -1.4], 2.1, col_p) for a in [62, 40, 18]])
    nl = VGroup(T("chick sensory", 28, TEXT), T("neuron", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([0, -1.5, 0])
    return cell, st, sp, nl


KX_L, KX_R = -3.3, 3.3


class S04(SpokenScene):
    def construct(self):
        cell, st, sp, nl = neuron_group()
        self.add(cell, st, sp, nl)
        self.at("two classes")
        tl = lab("tight sites", PINK, KX_L, 3.3, 32)
        self.play(*[s.animate.set_color(PINK) for s in st], FadeIn(tl), run_time=0.8)
        self.at("ngf site")
        ll = lab("loose sites", VIOLET, KX_R, 3.3, 32)
        self.play(*[s.animate.set_color(VIOLET) for s in sp], FadeIn(ll), run_time=0.8)
        self.finish()


def neuron_state():
    cell, st, sp, nl = neuron_group(sites_color=True)
    tl = lab("tight sites", PINK, KX_L, 3.3, 32)
    ll = lab("loose sites", VIOLET, KX_R, 3.3, 32)
    return cell, st, sp, nl, tl, ll


class S05(SpokenScene):
    def construct(self):
        cell, st, sp, nl, tl, ll = neuron_state()
        self.add(cell, st, sp, nl, tl, ll)
        self.at("20 picomolar")
        k1 = mono("Kd about 20 pM", PINK, KX_L, 2.65, 28)
        self.play(FadeIn(k1, shift=DOWN * 0.15), run_time=0.7)
        self.at("2 nanomolar")
        k2 = mono("Kd about 2 nM", VIOLET, KX_R, 2.65, 28)
        self.play(FadeIn(k2, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        cell, st, sp, nl, tl, ll = neuron_state()
        k1 = mono("Kd about 20 pM", PINK, KX_L, 2.65, 28)
        k2 = mono("Kd about 2 nM", VIOLET, KX_R, 2.65, 28)
        self.add(cell, st, sp, nl, tl, ll, k1, k2)
        self.at("orders of magnitude")
        self.play(Indicate(k1, color=PINK), Indicate(k2, color=VIOLET), run_time=0.7)
        self.at("about 10 picomolar")
        n1 = mono("Kd about 10 pM", PINK, KX_L, 2.65, 28)
        n2 = mono("Kd about 1 nM", VIOLET, KX_R, 2.65, 28)
        t1 = lab("Trk-linked sites", PINK, KX_L, 3.3, 32)
        t2 = lab("p75-alone sites", VIOLET, KX_R, 3.3, 32)
        # both values and both names change in the same beat
        self.play(ReplacementTransform(k1, n1), ReplacementTransform(k2, n2),
                  ReplacementTransform(tl, t1), ReplacementTransform(ll, t2), run_time=0.8)
        self.at("100 fold")
        br = DoubleArrow([-1.0, 2.65, 0], [1.0, 2.65, 0], color=TEXT, buff=0, stroke_width=5, tip_length=0.2)
        hl = T("100-fold", 28, TEXT).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(hl), run_time=0.8)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        ax = Axes(x_range=[-2, 2, 1], y_range=[0, 1, 0.5], x_length=10.4, y_length=5.0,
                  axis_config={"color": GREY, "stroke_width": 4, "include_ticks": False, "include_tip": False})
        ax.move_to([0.2, 0.35, 0])
        ax.y_axis.set_opacity(0)
        yaxis = Line(ax.c2p(-2, 0), ax.c2p(-2, 1), color=GREY, stroke_width=4)
        f = lambda x: occ(10 ** x, 1.0)
        formula = M("fraction occupied = [NGF] / ([NGF] + Kd)", 32, TEXT)
        fit(formula, max_w=12.2)
        formula.move_to([0, 3.45, 0])
        yl = VGroup(*[T(s, 26, TEXT).move_to(ax.c2p(-2, v) + LEFT * 0.62) for s, v in
                      [("0", 0), ("50%", 0.5), ("100%", 1)]])
        ytitle = T("fraction of sites occupied", 28, TEXT).rotate(PI / 2).move_to([-6.45, 0.35, 0])
        xl = VGroup(*[T(s, 26, TEXT).move_to(ax.c2p(v, 0) + DOWN * 0.42) for s, v in
                      [("Kd/100", -2), ("Kd/10", -1), ("Kd", 0), ("10 Kd", 1), ("100 Kd", 2)]])
        xt = T("free NGF (log scale)", 28, BLUE).move_to([0.2, -3.45, 0])
        curve = ax.plot(f, x_range=[-2, 2], color=BLUE, stroke_width=7)
        self.add(formula)
        self.at("a dissociation constant", lead=0.0)
        self.play(Create(ax), Create(yaxis), FadeIn(yl), FadeIn(xl), FadeIn(xt), FadeIn(ytitle), run_time=1.0)
        self.at("free concentration")
        self.play(Create(curve), run_time=1.3)
        self.at("fills half")
        p = ax.c2p(0, 0.5)
        dot = Dot(p, radius=0.13, color=TEXT)
        v = DashedLine(ax.c2p(0, 0), p, color=TEXT, stroke_width=4)
        hz = DashedLine(ax.c2p(-2, 0.5), p, color=TEXT, stroke_width=4)
        hf = T("half full at Kd", 30, TEXT).move_to(ax.c2p(1.0, 0.3))
        hl = Line(p + DR * 0.1, hf.get_left() + LEFT * 0.08, color=TEXT, stroke_width=3)
        self.play(FadeIn(dot), Create(v), Create(hz), FadeIn(hf), Create(hl), run_time=0.9)
        self.at("below it")
        q = ax.c2p(-1, f(-1))
        seg = Line(ax.c2p(-2, 0), ax.c2p(0, 0), color=RED, stroke_width=9)
        dot2 = Dot(q, radius=0.13, color=RED)
        v2 = DashedLine(ax.c2p(-1, 0), q, color=RED, stroke_width=4)
        fw = VGroup(T("fewer than half:", 28, RED), T(f"about {f(-1) * 100:.0f}% at Kd/10", 28, RED)
                    ).arrange(DOWN, buff=0.08).move_to(ax.c2p(-1.3, 0.30))
        l2 = Line(q, fw.get_bottom() + DOWN * 0.05, color=RED, stroke_width=3)
        self.play(Create(seg), FadeIn(dot2), Create(v2), FadeIn(fw), Create(l2), run_time=0.8)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        st = Stage(logc=-12.0, kds=True)
        self.add(*st.mobs())
        self.at("pick a low level")
        self.play(st.c.animate.set_value(-11.0), run_time=0.9)
        self.at("for illustration")
        self.play(FadeIn(chosen_label()), run_time=0.5)
        self.at("which sites fill")
        self.play(FadeIn(question_text(), shift=LEFT * 0.2), run_time=0.6)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        st = Stage(logc=-11.0, kds=True)
        self.add(*st.mobs(), chosen_label(), question_text())
        self.wait(self.narration_s)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        st = Stage(logc=-11.0, kds=True)
        q = question_text()
        self.add(*st.mobs(), chosen_label(), q)
        self.at("track sites")
        self.play(FadeOut(q), st.r["t"].animate.set_value(1.0), run_time=1.3)
        self.at("only about")
        self.play(st.r["p"].animate.set_value(1.0), run_time=0.7)
        pulse(self, st.frames[1], VIOLET)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        st = Stage(logc=-11.0, rt=1.0, rp=1.0, kds=True)
        self.add(*st.mobs())
        self.play(st.vis.animate.set_value(0.0), FadeOut(st.dial), run_time=0.5)
        note = VGroup(T("fractions of sites,", 28, TEXT), T("not signal", 28, TEXT)).arrange(DOWN, buff=0.12)
        note.move_to([-4.7, 0.2, 0])
        self.at("much larger fraction")
        self.play(FadeIn(note), st.frames[0].animate.set_stroke(PINK, 8), run_time=0.6)
        self.play(st.frames[0].animate.set_stroke(GREY, 3), run_time=0.4)
        self.at("75 sites")
        pulse(self, st.frames[1], VIOLET)
        self.at("survival depends")
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=1.95, height=2.0, stroke_color=GREEN,
                                              stroke_width=3, fill_opacity=0), num_dashes=40).move_to([0.4, 0.2, 0])
        txt = VGroup(T("signals", 26, GREEN), T("this count", 26, GREEN), T("leaves out", 26, GREEN)).arrange(DOWN, buff=0.1)
        txt.move_to([0.4, 0.2, 0])
        self.play(FadeIn(box), FadeIn(txt), run_time=0.9)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        st = Stage(logc=-11.0, rt=1.0, rp=1.0, kds=True, vis=0.0)
        self.add(*st.mobs(dial=False), st.pointer)
        # clear the old answer in the same beat that the dial comes back
        self.play(st.vis.animate.set_value(1.0), FadeIn(st.dial), st.r["t"].animate.set_value(0.0),
                  st.r["p"].animate.set_value(0.0), run_time=0.4)
        self.at("turn the dial")
        self.play(st.c.animate.set_value(C2), run_time=1.6)
        self.at("culture experiments")
        n = VGroup(T("culture dose:", 28, TEXT), M("50 ng/mL", 28, TEXT), M("NGF dimer", 28, TEXT),
                   M("about 2 nM", 30, BLUE)).arrange(DOWN, buff=0.15).move_to([5.2, 0.8, 0])
        self.play(FadeIn(n, shift=LEFT * 0.2), run_time=0.8)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        st = Stage(logc=C2, kds=True, band=True)
        self.add(*st.mobs())
        t50, t67 = p75_ticks()
        newkd = mono("Kd 1 to 2 nM", VIOLET, BAR_X["p"], -3.5, 26)
        self.at("track sites are")
        self.play(st.r["t"].animate.set_value(1.0), run_time=1.0)
        self.at("roughly half")
        self.play(st.r["p"].animate.set_value(1.0), FadeIn(t50), ReplacementTransform(st.kds[1], newkd),
                  run_time=0.8)
        self.at("two thirds")
        self.play(st.rb.animate.set_value(1.0), FadeIn(t67), run_time=0.7)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        st = Stage(logc=C2, rt=1.0, rp=1.0, kds=True, band=True, rb=1.0, kdp="Kd 1 to 2 nM")
        t50, t67 = p75_ticks()
        self.add(*st.mobs(), t50, t67)
        self.at("fills many")
        pulse(self, st.frames[1], VIOLET)
        self.at("that fits")
        cx, cy = 4.9, -0.7
        oc = round_cell(cx, cy, 1.3)
        orc = VGroup(site(132, [cx, cy], 1.3, VIOLET, top=1.0), site(48, [cx, cy], 1.3, VIOLET, top=1.0))
        ol = lab("cell without TrkA", TEXT, cx, cy - 1.8, 28)
        fl = VGroup(T("fits the culture", 26, TEXT), T("results;", 26, TEXT), T("occupancy only", 26, TEXT)
                    ).arrange(DOWN, buff=0.06).move_to([cx, 2.0, 0])
        self.play(FadeOut(t50), FadeOut(t67), FadeIn(oc), FadeIn(orc), FadeIn(ol), FadeIn(fl), run_time=0.6)
        self.at("killing track")
        self.play(oc.animate.set_stroke(RED).set_fill(RED, 0.3), run_time=0.6)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        my = -1.1
        rx = -1.6
        mem = Rectangle(width=5.6, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([rx, my, 0])
        rc = flat_rcp(rx, my, VIOLET, top=2.6, w=0.6)
        lbl = lab("p75", VIOLET, rx + 1.0, my - 0.7, 30)
        d = dimer(rx, 3.0, 1.2)
        dl = lab("mature NGF", BLUE, 0, 0, 28).next_to(d, RIGHT, buff=0.3)
        self.add(mem, rc, lbl, d, dl)
        self.at("filling a site")
        shift = np.array([0, my + 2.6 + 0.45 - 3.0, 0])
        self.play(d.animate.shift(shift), dl.animate.shift(shift), run_time=0.7)
        sf = lab("site filled", BLUE, 0, 0, 30).next_to(d, RIGHT, buff=0.3)
        sf.shift(shift * 0)  # d already at its final place
        self.play(ReplacementTransform(dl, sf), rc.bar.animate.set_fill(VIOLET, 0.95), run_time=0.4)
        self.at("same as signaling")
        ne = VGroup(T("=", 100, TEXT), Line([-0.5, -0.65, 0], [0.5, 0.65, 0], color=RED, stroke_width=9)).move_to([3.0, 0.3, 0])
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=2.5, height=1.6, stroke_color=TEXT,
                                              stroke_width=4, fill_opacity=0), num_dashes=40).move_to([5.5, 0.3, 0])
        sg = lab("signal", TEXT, 5.5, 0.3, 34)
        self.play(FadeIn(ne), FadeIn(box), FadeIn(sg), run_time=0.7)
        self.at("the model has")
        fr, fill, pct = band_bar(-3.0)
        occl = lab("p75 sites filled", VIOLET, -3.0, -3.0, 28)
        self.play(FadeOut(VGroup(ne, box, sg, d, sf, mem, rc, lbl)), FadeIn(fr), FadeIn(fill), FadeIn(pct),
                  FadeIn(occl), run_time=0.5)
        self.at("no threshold")
        thl = VGroup(T("survival or death", 34, TEXT), T("threshold?", 34, TEXT)).arrange(DOWN, buff=0.12)
        thl.move_to([3.3, 0.9, 0])
        self.play(FadeIn(thl), run_time=0.6)
        self.at("survival or death")
        x = cross([0.4, 0.9, 0], 0.45, RED, 9)
        nn = T("none in this model", 32, RED).move_to([3.3, -0.4, 0])
        self.play(Create(x), FadeIn(nn), run_time=0.6)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        d1, d2 = dish(-3.5, -0.4, 4.6, 3.2), dish(3.5, -0.4, 4.6, 3.2)
        m = dimer(-3.5, 2.3, 0.85)
        p = dimer(3.5, 2.3, 0.85, tails=True)
        ml = lab("mature NGF", BLUE, -3.5, -2.6, 30)
        pl = lab("uncleavable proNGF", BLUE, 3.5, -2.6, 30)
        self.add(d1, d2, m, p, ml, pl)
        self.at("a low dose")
        self.play(FadeIn(lab("low dose", TEXT, 0, 3.4, 32)), run_time=0.5)
        self.at("added no death")
        nd = lab("no added death", GREEN, -3.5, -3.3, 30)
        self.play(FadeIn(nd), d1.box.animate.set_stroke(GREEN, 6), run_time=0.8)
        self.at("the precursor killed")
        dead = [1, 6, 10]
        self.play(*[d2.cells[i].animate.set_stroke(RED).set_fill(RED, 0.4).scale(0.6) for i in dead], run_time=0.9)
        self.play(FadeIn(lab("more cells die", RED, 3.5, -3.3, 30)), run_time=0.5)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        MY = -1.3
        XP, XS = -1.5, 2.5
        mem = Rectangle(width=13.0, height=0.34, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, MY, 0])
        p75 = flat_rcp(XP, MY, VIOLET, top=3.0)
        sor = flat_rcp(XS, MY, YELLOW, top=3.0, w=0.6)
        pl = lab("p75", VIOLET, XP - 1.0, MY - 0.7, 30)
        sl = lab("sortilin", YELLOW, XS + 1.3, MY - 0.7, 30)
        pro = dimer(XP, 2.15, 1.2, tails=True)
        prl = lab("proNGF", BLUE, XP - 2.6, 2.3, 30)
        self.add(mem, p75, sor, pl, sl, pro, prl)
        self.at("pro domain")
        pdl = lab("pro-domain", ORANGE, 1.4, 3.35, 30)
        self.play(*[t.animate.set_fill(ORANGE, 1.0) for t in pro.tails], FadeIn(pdl), run_time=0.8)
        self.at("grips it")
        tail = pro.tails[1]
        path = VMobject(color=ORANGE)
        path.set_points_smoothly([[XP + 0.6, 2.6, 0], [XP + 0.6, 3.2, 0], [XP + 1.2, 3.55, 0], [1.0, 3.55, 0],
                                  [2.1, 3.2, 0], [XS, 2.6, 0], [XS, 1.9, 0]])
        path.set_stroke(ORANGE, 30)
        path.set_cap_style(CapStyleType.ROUND)
        l_p = VGroup(T("p75 grips", 28, VIOLET), T("the mature part", 28, VIOLET)).arrange(DOWN, buff=0.08)
        l_p.move_to([-5.0, 0.9, 0])
        k_p = Line([-3.5, 1.3, 0], [XP - 0.2, 1.75, 0], color=VIOLET, stroke_width=3)
        l_s = VGroup(T("sortilin grips", 28, YELLOW), T("the pro-domain", 28, YELLOW)).arrange(DOWN, buff=0.08)
        l_s.move_to([5.1, 0.9, 0])
        k_s = Line([3.75, 1.3, 0], [XS + 0.25, 1.8, 0], color=YELLOW, stroke_width=3)
        self.play(FadeOut(pdl), FadeOut(prl), FadeOut(tail), pro.tails[0].animate.set_fill(ORANGE, 0.65),
                  Create(path), sor.bar.animate.set_fill(YELLOW, 0.95), run_time=0.9)
        self.play(FadeIn(l_p), Create(k_p), FadeIn(l_s), Create(k_s), run_time=0.6)
        self.at("cells tested")
        fy = MY - 0.7 - 0.27
        br = VMobject(color=RED)
        br.set_points_as_corners([[XP, fy - 0.03, 0], [XP, -2.6, 0], [XS, -2.6, 0], [XS, fy - 0.03, 0]])
        br.set_stroke(RED, 5)
        tag = lab("in the cells tested", TEXT, 4.2, -3.4, 28)
        self.play(Create(br), FadeIn(tag), run_time=0.6)
        self.at("death signal")
        mid = (XP + XS) / 2
        ds = chip("death signal", RED, 30).move_to([mid, -3.4, 0])
        a1 = arr([mid, -2.6, 0], [mid, -3.0, 0], RED)
        self.play(GrowArrow(a1), FadeIn(ds), run_time=0.7)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        pro = dimer(-4.3, 0.9, 1.7, tails=True)
        pl = lab("proNGF", BLUE, -4.3, -0.9, 38)
        self.add(pro, pl)
        self.at("no binding numbers")
        kd = M("Kd = ?", 54, TEXT).move_to([2.0, 2.4, 0])
        x = cross([-0.5, 2.4, 0], 0.45, RED, 9)
        nb = lab("no binding numbers", RED, 2.0, 1.5, 34)
        self.play(FadeIn(kd), Create(x), FadeIn(nb), run_time=0.9)
        self.at("compared by experiment")
        d1 = dish(1.3, -2.2, 3.4, 2.2, 2, 4, 0.21)
        d2 = dish(5.1, -2.2, 3.4, 2.2, 2, 4, 0.21)
        ar = arr([-3.0, -0.1, 0], [-0.6, -1.7, 0], TEXT)
        lc = lab("compared by experiment", TEXT, 3.2, 0.3, 32)
        t1 = lab("mature NGF", BLUE, 1.3, -0.8, 28)
        t2 = lab("proNGF", BLUE, 5.1, -0.8, 28)
        self.play(GrowArrow(ar), FadeIn(d1), FadeIn(d2), FadeIn(lc), FadeIn(t1), FadeIn(t2), run_time=0.9)
        o1 = lab("no added death", GREEN, 1.3, -3.55, 28)
        o2 = lab("more cells die", RED, 5.1, -3.55, 28)
        dead = [1, 4, 6]
        self.play(FadeIn(o1), FadeIn(o2),
                  *[d2.cells[i].animate.set_stroke(RED).set_fill(RED, 0.4).scale(0.6) for i in dead], run_time=0.8)
        self.finish()


PY = 0.7


def scale_group(theta, L=4.0):
    c, s = np.cos(theta), np.sin(theta)
    left_end = np.array([-L * c, PY + L * s, 0.0])    # theta > 0 raises the left (death) end
    right_end = np.array([L * c, PY - L * s, 0.0])    # and lowers the right (survival) end
    beam = Line(left_end, right_end, color=TEXT, stroke_width=8)
    post = Line([0, -2.2, 0], [0, PY, 0], color=GREY, stroke_width=8)
    base = Rectangle(width=2.0, height=0.2, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([0, -2.3, 0])
    piv = Dot([0, PY, 0], radius=0.14, color=TEXT)
    out = [post, base, beam, piv]
    for end, text, col in [(left_end, "death signaling", RED), (right_end, "survival signaling", GREEN)]:
        out.append(Line(end, [end[0], end[1] - 0.8, 0], color=GREY, stroke_width=4))
        ch = chip(text, col, 28)
        back = ch[0].copy().set_fill(BG, 1).set_stroke(width=0)
        out.append(VGroup(back, ch).move_to([end[0], end[1] - 0.8 - ch.height / 2, 0]))
    return VGroup(*out)


class S19(SpokenScene):
    def construct(self):
        th = ValueTracker(-0.12)   # starts leaning toward death: the uncut precursor
        sc = always_redraw(lambda: scale_group(th.get_value()))
        pro = dimer(0, PY + 0.75, 1.1, tails=True)
        prl = lab("proNGF", BLUE, 2.6, PY + 1.5, 30)
        self.add(sc, pro, prl)
        self.at("the cut shifts")
        cutl = DashedLine([-1.4, PY + 1.2, 0], [1.4, PY + 1.2, 0], color=GOLD, stroke_width=6)
        ct = lab("the cut", GOLD, -2.7, PY + 1.2, 30)
        self.play(Create(cutl), FadeIn(ct), run_time=0.4)
        mlab = lab("mature NGF", BLUE, 2.6, PY + 1.5, 30)
        pdl = lab("pro-domain leaves", ORANGE, -2.3, 3.7, 28)
        self.play(pro.tails.animate.shift(LEFT * 2.4 + UP * 0.7), FadeIn(pdl), ReplacementTransform(prl, mlab),
                  run_time=0.6)
        self.play(th.animate.set_value(0.17), run_time=1.0)
        n1 = VGroup(T("mature NGF reaches p75", 26, VIOLET), T("at culture doses", 26, VIOLET)).arrange(DOWN, buff=0.06)
        n2 = VGroup(T("proNGF gave weak TrkA", 26, GREEN), T("survival in one lab", 26, GREEN)).arrange(DOWN, buff=0.06)
        n1.move_to([-3.9, -0.85, 0])
        n2.move_to([3.9, -2.6, 0])
        c1 = Line([-3.94, 0.0, 0], [-3.94, -0.42, 0], color=VIOLET, stroke_width=4)
        c2 = Line([3.94, -1.45, 0], [3.94, -2.1, 0], color=GREEN, stroke_width=4)
        self.play(FadeIn(n1), FadeIn(n2), Create(c1), Create(c2), run_time=0.5)
        self.at("flip a switch")
        cx, cy = 5.3, 2.95
        sw = RoundedRectangle(corner_radius=0.45, width=2.2, height=0.9, stroke_color=TEXT, stroke_width=5,
                              fill_color=GREY, fill_opacity=0.25).move_to([cx, cy, 0])
        kn = Circle(radius=0.32, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([cx + 0.55, cy, 0])
        x = cross([cx, cy, 0], 0.5, RED, 9)
        sl = lab("not a switch", TEXT, cx, cy - 0.95, 30)
        self.play(FadeIn(sw), FadeIn(kn), Create(x), FadeIn(sl), run_time=0.6)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        nb1, nb2 = two_notebooks()
        self.add(nb1, nb2)
        self.at("that is still open")
        q = T("?", 140, TEXT).move_to([0, 0.2, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.7)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        nb1, nb2 = two_notebooks()
        q = T("?", 140, TEXT).move_to([0, 0.2, 0])
        self.add(nb1, nb2, q)
        self.at("the dose", lead=0.0)
        self.play(q.animate.scale(0.45).move_to([0, 3.1, 0]), run_time=0.4)

        def rung(text_mobs, y, h):
            box = RoundedRectangle(corner_radius=0.16, width=4.3, height=h, stroke_color=TEXT, stroke_width=3,
                                   fill_color=BG, fill_opacity=1).move_to([0, y, 0])
            return VGroup(box, text_mobs.move_to([0, y, 0]))
        t1 = rung(T("dose", 30, TEXT), 1.35, 0.8)
        t2 = rung(T("receptor balance", 30, TEXT), 0.1, 0.8)
        t3 = rung(VGroup(T("precursor cut", 28, TEXT), T("in the experiment", 28, TEXT)).arrange(DOWN, buff=0.08),
                  -1.3, 1.25)
        self.play(FadeIn(t1, shift=UP * 0.2), run_time=0.4)
        self.at("the receptor balance")
        self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.5)
        self.at("how much precursor")
        self.play(FadeIn(t3, shift=UP * 0.2), run_time=0.5)
        self.at("could each matter")
        self.add(lab("unsettled", TEXT, 0, -3.0, 38))
        self.wait(0.6)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        fr = [card_frame(x, CARD_Y) for x in CARD_X]
        self.add(*fr)
        self.at("first whether")
        pro, cutl, mat, ml, free = card1_icon(CARD_X[0], CARD_Y - 0.1)
        self.play(FadeIn(card_head(CARD_X[0], CARD_Y, "1", "the cut")), FadeIn(pro), run_time=0.7)
        self.at("has been cut")
        self.play(Create(cutl), run_time=0.5)
        self.play(FadeIn(mat), FadeIn(ml), FadeIn(free), run_time=0.7)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        fr = [card_frame(x, CARD_Y) for x in CARD_X]
        self.add(*fr, card_head(CARD_X[0], CARD_Y, "1", "the cut"), *card1_icon(CARD_X[0], CARD_Y - 0.1))
        self.at("second which")
        self.play(FadeIn(card_head(CARD_X[1], CARD_Y, "2", "the receptors")), run_time=0.4)
        self.play(FadeIn(card2_icon(CARD_X[1], CARD_Y - 0.1), lag_ratio=0.25), run_time=1.0)
        self.at("third how much")
        c3 = card3_icon(CARD_X[2], CARD_Y - 0.1)
        self.play(FadeIn(card_head(CARD_X[2], CARD_Y, "3", "the amounts")), run_time=0.4)
        self.play(FadeIn(c3[0]), run_time=0.6)
        self.play(FadeIn(c3[1]), run_time=0.6)
        self.finish()


def gauge_pointer(x):
    y = -2.15
    return Polygon([x, y, 0], [x - 0.28, y + 0.5, 0], [x + 0.28, y + 0.5, 0], stroke_width=0,
                   fill_color=TEXT, fill_opacity=1)


class S25(SpokenScene):
    def construct(self):
        cards = [mini_card(x, 3.2, n, t) for x, n, t in zip([-4.3, 0.0, 4.3], "123", ["the cut", "the receptors", "the amounts"])]
        cell = round_cell(0, 0.55, 1.45, TEXT, 0.14)
        cl = lab("one cell", TEXT, 0, 0.55, 34)
        ars = [arr([-4.0, 2.65, 0], [-1.1, 1.6, 0]), arr([0, 2.65, 0], [0, 2.05, 0]), arr([4.0, 2.65, 0], [1.1, 1.6, 0])]
        bar_l = Rectangle(width=5.8, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.7).move_to([-2.9, -2.6, 0])
        bar_r = Rectangle(width=5.8, height=0.5, stroke_width=0, fill_color=RED, fill_opacity=0.7).move_to([2.9, -2.6, 0])
        ll = lab("more survival signaling", GREEN, -2.9, -3.35, 28)
        rl = lab("more death signaling", RED, 2.9, -3.35, 28)
        p = gauge_pointer(0.0)
        self.add(*cards, cell, cl, *ars, bar_l, bar_r, ll, rl, p)
        # pulse each card in turn; the marker moves only after the pulse
        self.wait(0.15)
        self.play(cards[0][0].animate.set_stroke(GOLD, 9).set_fill(GOLD, 0.25), ars[0].animate.set_color(GOLD), run_time=0.2)
        self.play(cards[0][0].animate.set_stroke(GREY, 4).set_fill(GREY, 0.07), ars[0].animate.set_color(GREY), run_time=0.2)
        self.play(p.animate.move_to([-2.6, p.get_center()[1], 0]), run_time=0.45)
        self.wait(0.1)
        self.play(cards[1][0].animate.set_stroke(GOLD, 9).set_fill(GOLD, 0.25), ars[1].animate.set_color(GOLD), run_time=0.2)
        self.play(cards[1][0].animate.set_stroke(GREY, 4).set_fill(GREY, 0.07), ars[1].animate.set_color(GREY), run_time=0.2)
        self.play(p.animate.move_to([2.6, p.get_center()[1], 0]), run_time=0.55)
        self.wait(0.1)
        self.play(cards[2][0].animate.set_stroke(GOLD, 9).set_fill(GOLD, 0.25), ars[2].animate.set_color(GOLD), run_time=0.2)
        self.play(cards[2][0].animate.set_stroke(GREY, 4).set_fill(GREY, 0.07), ars[2].animate.set_color(GREY), run_time=0.2)
        self.play(p.animate.move_to([-0.9, p.get_center()[1], 0]), run_time=0.5)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        ym = -1.0
        tg = chip("target", GREY, 40).move_to([-5.3, ym, 0])
        fd = dimer(-1.9, ym, 1.3)
        fl = lab("the factor", BLUE, -1.9, ym - 0.95, 30)
        cell = round_cell(3.7, ym, 1.3)
        rec = VGroup(site(125, [3.7, ym], 1.3, PINK, top=1.0), site(90, [3.7, ym], 1.3, VIOLET, top=1.0),
                     site(55, [3.7, ym], 1.3, YELLOW, top=1.0))
        rl = VGroup(lab("TrkA", PINK, 2.0, 1.45, 28), lab("p75", VIOLET, 3.7, 1.7, 28),
                    lab("sortilin", YELLOW, 5.4, 1.45, 28))
        tag = lab("Remember the rule", GOLD, 0, 3.4, 42)
        self.add(tg, fd, fl, tag)
        self.at("the target supplies")
        a1 = arr([-4.2, ym, 0], [-3.2, ym, 0], TEXT)
        l1 = lab("The target supplies the factor.", TEXT, 0, 3.4, 40)
        self.play(GrowArrow(a1), FadeOut(tag), FadeIn(l1), run_time=0.7)
        self.at("the receptors decide")
        a2 = arr([-0.7, ym, 0], [1.3, ym, 0], TEXT)
        l2 = lab("The receptors decide what it means.", TEXT, 0, 2.7, 40)
        self.play(FadeIn(cell), FadeIn(rec), FadeIn(rl), GrowArrow(a2), FadeIn(l2), run_time=0.9)
        self.at("what it means")
        g = chip("survival", GREEN, 30).move_to([2.5, -3.25, 0])
        r = chip("death", RED, 30).move_to([4.9, -3.25, 0])
        self.play(FadeIn(g), FadeIn(r), run_time=0.7)
        self.finish()


class S27(SpokenScene):
    def construct(self):
        nx = T("Next lesson", 30, TEXT).move_to([0, 3.3, 0])
        ttl = T("Competition for targets", 54, TEXT, font=TITLE_FONT).move_to([0, 2.45, 0])
        tg = chip("target", GREY, 38).move_to([0, -0.9, 0])
        cA, cB = (-4.9, -0.9), (4.9, -0.9)
        n1 = round_cell(cA[0], cA[1], 1.3)
        n2 = round_cell(cB[0], cB[1], 1.3)
        s1 = site(0, cA, 1.3, VIOLET, top=1.0)
        s2 = site(180, cB, 1.3, VIOLET, top=1.0)
        l1 = lab("p75", VIOLET, cA[0] + 2.35, cA[1] - 0.75, 30)
        l2 = lab("p75", VIOLET, cB[0] - 2.35, cB[1] - 0.75, 30)
        self.add(nx, ttl, tg, n1, n2, s1, s2)
        self.at("competing neurons")
        a1 = arr([-2.3, -0.9, 0], [-1.35, -0.9, 0], VIOLET)
        a2 = arr([2.3, -0.9, 0], [1.35, -0.9, 0], VIOLET)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.at("use p 75")
        self.play(FadeIn(l1), FadeIn(l2), Indicate(s1, color=VIOLET), Indicate(s2, color=VIOLET), run_time=0.8)
        self.at("against each other")
        v1 = DashedLine([-2.6, -0.6, 0], [-2.6, 0.5, 0], color=RED, stroke_width=4)
        v2 = DashedLine([2.6, -0.6, 0], [2.6, 0.5, 0], color=RED, stroke_width=4)
        dbl = DoubleArrow([-2.6, 0.5, 0], [2.6, 0.5, 0], buff=0, color=RED, stroke_width=8, tip_length=0.3)
        cl = lab("compete", RED, 0, 1.0, 32)
        self.play(Create(v1), Create(v2), run_time=0.3)
        self.play(GrowFromCenter(dbl), FadeIn(cl), run_time=0.6)
        self.finish()


def dose_icon(cx, cy):
    """Two pairs of bars computed from the model: 10 pM and 2 nM."""
    H = 4.8
    out = []
    for dx, c, lbl in [(-1.6, 1e-11, "10 pM"), (1.6, 2e-9, "2 nM")]:
        for j, (f, col) in enumerate([(occ(c, KD_TRK), PINK), (occ(c, KD_P75), VIOLET)]):
            x = cx + dx + (j - 0.5) * 0.95
            h = max(H * f, 0.05)
            out += [Rectangle(width=0.8, height=H, stroke_color=GREY, stroke_width=3).move_to([x, cy + H / 2, 0]),
                    Rectangle(width=0.74, height=h, stroke_width=0, fill_color=col,
                              fill_opacity=0.8).move_to([x, cy + h / 2, 0])]
        out.append(M(lbl, 28, BLUE).move_to([cx + dx, cy - 0.4, 0]))
    return VGroup(*out)


class S28(SpokenScene):
    def construct(self):
        head = T("The takeaway", 56, TEXT, font=TITLE_FONT).move_to([0, 0.3, 0])
        self.add(head)
        self.at("dose changes", lead=0.0)
        cx, y0 = -3.4, -1.85
        ic = dose_icon(cx, y0)
        sq1 = Square(0.3, stroke_width=0, fill_color=PINK, fill_opacity=0.9).move_to([-6.2, 3.45, 0])
        lg1 = T("Trk-linked", 28, PINK).next_to(sq1, RIGHT, buff=0.15)
        sq2 = Square(0.3, stroke_width=0, fill_color=VIOLET, fill_opacity=0.9).move_to([-3.6, 3.45, 0])
        lg2 = T("p75-alone", 28, VIOLET).next_to(sq2, RIGHT, buff=0.15)
        t1 = VGroup(T("Dose changes", 30, TEXT), T("which sites fill.", 30, TEXT)).arrange(DOWN, buff=0.1).move_to([cx, -3.2, 0])
        self.play(FadeOut(head), FadeIn(ic), FadeIn(sq1), FadeIn(lg1),
                  FadeIn(sq2), FadeIn(lg2), FadeIn(t1), run_time=1.0)
        self.at("the cut changes")
        px = 4.9
        pro = dimer(px, 2.0, 1.1, tails=True)
        prl = lab("proNGF", BLUE, 6.3, 1.1, 28)
        cy_cut = 2.0 + 0.41
        cutl = DashedLine([px - 1.4, cy_cut, 0], [px + 1.4, cy_cut, 0], color=GOLD, stroke_width=5)
        cutt = lab("the cut", GOLD, 2.7, cy_cut, 26)
        mx = 2.5
        mat = dimer(mx, 0.9, 1.1)
        ml = lab("mature NGF", BLUE, mx, 1.6, 28)
        RX = {"t": 2.0, "p": 3.7, "s": 5.4}
        rcs = VGroup()
        for k, c, nm in [("t", PINK, "TrkA"), ("p", VIOLET, "p75"), ("s", YELLOW, "sortilin")]:
            b = RoundedRectangle(corner_radius=0.1, width=0.4, height=1.1, stroke_color=c, stroke_width=3,
                                 fill_color=c, fill_opacity=0.55).move_to([RX[k], -1.2, 0])
            rcs.add(VGroup(b, lab(nm, c, RX[k], -2.05, 28)))
        TOP = -0.62
        am1 = arr([mx - 0.3, 0.45, 0], [RX["t"], TOP, 0], PINK, 9)
        am2 = arr([mx + 0.3, 0.45, 0], [RX["p"] - 0.1, TOP, 0], VIOLET, 3)
        ap1 = arr([px - 0.3, 1.5, 0], [RX["p"] + 0.15, TOP, 0], VIOLET, 5)
        ap2 = arr([px + 0.4, 1.5, 0], [RX["s"], TOP, 0], ORANGE, 5)
        pdt = VGroup(T("via the", 22, ORANGE), T("pro-domain", 22, ORANGE)).arrange(DOWN, buff=0.05).move_to([6.2, 0.35, 0])
        t2 = VGroup(T("The cut changes", 28, TEXT), T("which receptors the factor", 28, TEXT),
                    T("works through best.", 28, TEXT)).arrange(DOWN, buff=0.08).move_to([3.7, -3.1, 0])
        self.play(FadeIn(pro), FadeIn(prl), run_time=0.5)
        self.play(Create(cutl), FadeIn(cutt), run_time=0.4)
        self.play(FadeIn(mat), FadeIn(ml), FadeIn(rcs), FadeIn(t2), run_time=0.6)
        self.play(GrowArrow(am1), GrowArrow(am2), GrowArrow(ap1), GrowArrow(ap2), FadeIn(pdt), run_time=0.7)
        self.finish()


class S29End(EndCard):
    LINE = "Dose sets which sites fill; the cut sets which receptors respond best."

    def construct(self):
        a = T("Dose sets which sites fill;", 46, font=TITLE_FONT)
        b = T("the cut sets which receptors respond best.", 46, font=TITLE_FONT)
        fit(b, max_w=12.0)
        sub = T("biochemistrypedia.com", 24, color=TEAL)
        g = VGroup(a, b, sub).arrange(DOWN, buff=0.35)
        g.move_to(ORIGIN)
        self.add(a, b)
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
