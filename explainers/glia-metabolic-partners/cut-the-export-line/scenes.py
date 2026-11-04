"""Cut the Export Line  (chapter 3 of "Feeding the Axon: Glia as Metabolic Partners")

COLOR MAP (one color per concept, whole series; same as the earlier single film)
  BLUE   = the neuron / axon / motor neuron
  TEAL   = myelinating glia (oligodendrocyte, the glial cell that wraps axons)
  PURPLE = astrocyte
  ORANGE = lactate (and pyruvate, its partner), glycolysis
  YELLOW = ATP and mitochondria
  GREY   = myelin, membranes, transporter gates, outlines, small print
  GREEN  = evidence for / survived / axon intact
  RED    = blocked, deleted, died, evidence against
  GOLD   = an open question (predict card, "still unknown", "hypothesis")
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LESSON_TITLE = "Feeding the Axon: Glia as Metabolic Partners"


# ----------------------------------------------------------------------------- helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rrect(w, h, color, fo=0.15, sw=3, r=0.2):
    return RoundedRectangle(corner_radius=min(r, w / 2, h / 2), width=w, height=h, stroke_color=color,
                            stroke_width=sw, fill_color=color, fill_opacity=fo)


def mito(x, y, w=1.0, h=0.55, color=YELLOW):
    o = Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.18)
    pts = [[-w * .30, 0, 0], [-w * .18, h * .22, 0], [-w * .06, -h * .22, 0], [w * .06, h * .22, 0],
           [w * .18, -h * .22, 0], [w * .30, 0, 0]]
    ins = VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
    return VGroup(o, ins).move_to([x, y, 0])


def gate(x, y, color=GREY, h=0.95):
    """a transporter shown as a small gate: two blocks with a narrow passage between them."""
    a = rrect(0.5, h, color, 0.5, 3, 0.1).move_to([x - 0.45, y, 0])
    b = rrect(0.5, h, color, 0.5, 3, 0.1).move_to([x + 0.45, y, 0])
    return VGroup(a, b)


def cross(c, color=RED, s=0.3):
    c = np.array(c, dtype=float)
    return VGroup(Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=7),
                  Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=7))


def tick(c, s=0.3, color=GREEN):
    c = np.array(c, dtype=float)
    pts = [c + np.array([-s, 0.0, 0]), c + np.array([-s * 0.3, -s * 0.8, 0]), c + np.array([s, s * 0.9, 0])]
    return VMobject(color=color, stroke_width=9).set_points_as_corners(pts)


def lac_dot(x, y, r=0.17):
    """lactate = a filled orange dot."""
    return Circle(radius=r, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([x, y, 0])


def pyr_dot(x, y, r=0.17):
    """pyruvate = an open orange ring."""
    return Circle(radius=r * 0.9, stroke_color=ORANGE, stroke_width=5, fill_opacity=0).move_to([x, y, 0])


def lab(text, x, y, size=26, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def leader(a, b, color=GREY, w=3):
    return Line(a, b, color=color, stroke_width=w)


def chipn(lines, color, size=26, pad=0.25, gap=0.16):
    """a chip with several centred lines of text."""
    ts = VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, buff=gap)
    box = RoundedRectangle(corner_radius=0.16, width=ts.width + 2 * pad, height=ts.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.16)
    ts.move_to(box)
    return VGroup(box, ts)


def neuron_icon(c, r=0.95, color=BLUE):
    """a motor neuron as a cartoon: cell body, short dendrites, an axon stub (6 parts)."""
    k = r / 0.95
    soma = Circle(radius=r, stroke_color=color, stroke_width=max(3, 4 * k), fill_color=color, fill_opacity=0.3)
    parts = [soma]
    for a in (115, 160, 205, 250):
        d = np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
        parts.append(Line(d * r, d * (r + 0.7 * k), color=color, stroke_width=max(3, 4 * k)))
    parts.append(Line([r, 0, 0], [r + 1.0 * k, 0, 0], color=color, stroke_width=max(4, 7 * k)))
    g = VGroup(*parts)
    g.shift(np.array(c, dtype=float) - soma.get_center())
    return g


def neuron_dead(c, r=0.95):
    """the same six parts after the cell is lost: a shrunken grey body and scattered fragments."""
    k = r / 0.95
    col = GREY
    soma = Circle(radius=r * 0.5, stroke_color=col, stroke_width=4, stroke_opacity=0.9, fill_color=col, fill_opacity=0.25)
    parts = [soma]
    offs = [(0.30, 0.10), (0.15, -0.20), (-0.05, 0.25), (0.25, 0.15)]
    for a, (o1, o2) in zip((115, 160, 205, 250), offs):
        d = np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
        p = d * (r * 0.95 + 0.30 * k) + np.array([o1, o2, 0]) * k
        t = np.array([-d[1], d[0], 0])
        parts.append(Line(p - t * 0.14 * k, p + t * 0.14 * k, color=col, stroke_width=5, stroke_opacity=0.9))
    parts.append(Line([r * 1.15 + 0.15 * k, -0.15, 0], [r * 1.15 + 0.5 * k, -0.28, 0], color=col, stroke_width=6, stroke_opacity=0.9))
    g = VGroup(*parts)
    g.shift(np.array(c, dtype=float) - soma.get_center() + np.array([0, 0, 0]))
    # keep the shrunken body where the cell body was
    soma.move_to(np.array(c, dtype=float))
    return g


def seg_axon(x0, x1, y, n, h, color=BLUE):
    w = (x1 - x0) / n
    return VGroup(*[Rectangle(width=w - 0.03, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9)
                    .move_to([x0 + w * (i + 0.5), y, 0]) for i in range(n)])


def degraded(segs):
    """copies of the axon segments in a degenerating state (thin, broken, faded)."""
    out = []
    for i, s in enumerate(segs):
        c = s.copy()
        k = i % 3
        if k == 0:
            c.stretch(0.55, 0).set_opacity(0.55)
        elif k == 1:
            c.stretch(0.25, 0).set_opacity(0.35)
        else:
            c.stretch(0.8, 0).set_opacity(0.8)
        out.append(c)
    return out


def swellings(segs, idxs, h):
    """swellings drawn as red outlines around the axon, so the axon stays visible."""
    return VGroup(*[Ellipse(width=0.8, height=h, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.18)
                    .move_to(segs[i].get_center()) for i in idxs])


def strip(cx, y, w=5.8, n=8, ax_h=0.9, sl_h=1.6, thin=False):
    """a myelinated axon strip: three myelin sleeves with the axon running through."""
    s = w / 3
    h = sl_h * (0.55 if thin else 1.0)
    sleeves = VGroup(*[rrect(s - 0.18, h, GREY, 0.5, 3, 0.3).move_to([cx + (i - 1) * s, y, 0]) for i in range(3)])
    segs = seg_axon(cx - w / 2, cx + w / 2, y, n, ax_h)
    return sleeves, segs


# ------------------------------------------------------------- the big glia / axon stage
GLIA_C = np.array([0, 1.95, 0]); GLIA_W, GLIA_H = 11.8, 2.5
AX_C = np.array([0, -1.75, 0]); AX_W, AX_H = 11.8, 2.9
GATE_X = 3.6; GATE_Y = 0.2


def big_stage():
    glia = rrect(GLIA_W, GLIA_H, TEAL, 0.14, 4, 0.7).move_to(GLIA_C)
    ax = rrect(AX_W, AX_H, BLUE, 0.14, 4, 0.7).move_to(AX_C)
    return glia, ax


# ---------------------------------------------------------- the survival-bars frame (s03 to s08)
ROW_Y = [2.0, 0.0, -2.0]
BX0, BW = 0.7, 5.9
BCX = BX0 + BW / 2
ROW_TXT = ["glucose withheld", "+ MCT1 blocker", "+ MCT1 blocker + lactate"]
DISH_C = np.array([-3.45, -0.4, 0])
SLICE_C = np.array([-3.45, 0.15, 0])
NEU6 = [-4.4, 0.15, 0]
GLU_XY = [-3.45, 3.3, 0]
BLK_XY = [-4.7, -2.55, 0]
LAC_XY = [-1.9, -2.55, 0]


def row_label(i):
    t = T(ROW_TXT[i], 26, TEXT)
    return t.move_to([BX0 + t.width / 2, ROW_Y[i] + 0.78, 0])


def row_bar(i):
    return rrect(BW, 0.9, GREY, 0.0, 3, 0.2).move_to([BCX, ROW_Y[i], 0])


def row(i):
    return VGroup(row_label(i), row_bar(i))


def result(i, ok):
    color = GREEN if ok else RED
    rr = rrect(BW, 0.9, color, 0.5, 3, 0.2).move_to([BCX, ROW_Y[i], 0])
    tx = T("survived" if ok else "died", 30, TEXT, weight=BOLD)
    tx.move_to([BX0 + 0.3 + tx.width / 2, ROW_Y[i], 0])
    return rr, tx


def dish_parts():
    dish = rrect(6.0, 5.4, GREY, 0.08, 4, 0.5).move_to(DISH_C)
    outer = Ellipse(width=5.0, height=3.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.14)
    wing_l = Ellipse(width=1.4, height=2.3, stroke_width=0, fill_color=GREY, fill_opacity=0.4).rotate(0.35).shift(LEFT * 0.95)
    wing_r = Ellipse(width=1.4, height=2.3, stroke_width=0, fill_color=GREY, fill_opacity=0.4).rotate(-0.35).shift(RIGHT * 0.95)
    bridge = Rectangle(width=1.0, height=0.4, stroke_width=0, fill_color=GREY, fill_opacity=0.4)
    slc = VGroup(outer, wing_l, wing_r, bridge).move_to(SLICE_C)
    dl = lab("spinal cord slice", -3.45, 1.95, 26, TEXT)
    return dish, slc, dl


def glucose_out():
    """the withheld glucose: a chip with a red cross beside it (the word stays readable)."""
    c = chip("glucose", TEXT, 26).move_to(GLU_XY)
    x = cross([GLU_XY[0] + c.width / 2 + 0.45, GLU_XY[1], 0], RED, 0.25)
    return VGroup(c, x)


def blocker_chip():
    return chip("MCT1 blocker", RED, 26)


def lactate_chip():
    return chip("lactate", ORANGE, 26)


def predict_card():
    box = rrect(5.8, 7.0, GOLD, 0.06, 3, 0.3).move_to([-3.5, 0.0, 0])
    title = lab("Pause and predict", -4.1, 3.05, 30, GOLD, weight=BOLD)
    neus = VGroup(*[neuron_icon([-5.55, ROW_Y[i], 0], 0.36) for i in range(3)])
    qs = VGroup(*[VGroup(lab("motor neuron", -2.9, ROW_Y[i] + 0.28, 24, BLUE),
                         lab("survive or die?", -2.9, ROW_Y[i] - 0.2, 28, GOLD)) for i in range(3)])
    ask = lab("pause the video and decide", -3.5, -3.05, 26, TEXT)
    return box, title, neus, qs, ask


# =============================================================================== scenes
class S00Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = "Cut the Export Line"


# ----------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        glia, ax = big_stage()
        gl = lab("glial cell", -4.3, 2.75, 26, TEAL)
        al = lab("axon", -4.9, -2.75, 26, BLUE)
        g = gate(GATE_X, GATE_Y)
        lc = chip("lactate", ORANGE, 26).move_to([-1.2, 1.95, 0])
        dots = VGroup(lac_dot(1.6, 1.6), lac_dot(2.2, 2.3), lac_dot(2.9, 1.7), lac_dot(3.4, 2.4), lac_dot(4.3, 1.9),
                      lac_dot(4.9, 2.5))
        self.add(glia, ax, gl, al, g, lc, dots)
        self.at("feed axons")
        dash = DashedLine([GATE_X, 1.5, 0], [GATE_X, -0.8, 0], color=ORANGE, stroke_width=6, dash_length=0.18)
        dash.add_tip(tip_length=0.28)
        self.play(Create(dash), run_time=0.9)
        self.at("the fuel must leave")
        tgt = [[2.9, 1.15], [3.3, 1.35], [3.7, 1.15], [4.1, 1.4], [3.1, 0.95], [4.3, 1.0]]
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(dots, tgt)], run_time=1.2)
        self.at("leave the glial cell")
        self.play(Indicate(dots, color=ORANGE, scale_factor=1.25), run_time=0.8)
        self.at("What happens")
        self.play(Indicate(g, color=TEXT, scale_factor=1.12), run_time=0.8)
        self.at("block the exit")
        bar = Rectangle(width=2.0, height=0.26, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([GATE_X, 0.2, 0])
        q = lab("?", GATE_X, -1.35, 64, GOLD, weight=BOLD)
        self.play(FadeIn(bar, shift=DOWN * 0.7), g.animate.set_color(RED), run_time=0.5)
        self.play(FadeIn(q, scale=0.5), *[d.animate.shift(UP * 0.12) for d in dots], run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Mct(SpokenScene):
    def construct(self):
        MY = 0.0
        top = Rectangle(width=13.2, height=3.4, stroke_width=0, fill_color=TEAL, fill_opacity=0.08).move_to([0, 1.99, 0])
        left = rrect(5.9, 0.55, GREY, 0.45, 3, 0.1).move_to([-3.95, MY, 0])
        right = rrect(5.9, 0.55, GREY, 0.45, 3, 0.1).move_to([3.95, MY, 0])
        tr = rrect(1.7, 2.7, GREY, 0.45, 4, 0.35).move_to([0, MY, 0])
        slot = Rectangle(width=0.5, height=2.3, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, MY, 0])
        ins = lab("inside the glial cell", -4.1, 3.3, 26, TEAL)
        outs = lab("outside", -5.7, -2.45, 26, GREY)
        # legend: lactate = filled dot, pyruvate = open ring
        lg_l = VGroup(lac_dot(-6.0, 2.55), lab("lactate", -5.15, 2.55, 26, ORANGE))
        lg_p = VGroup(pyr_dot(-3.3, 2.55), lab("pyruvate", -2.3, 2.55, 26, ORANGE))
        ds = VGroup(lac_dot(-2.4, 1.55), pyr_dot(-1.95, 1.55), lac_dot(-1.5, 1.55))
        self.add(top, left, right, tr, slot, ins, outs, lg_l, lg_p, ds)

        def stream(items, t):
            paths = []
            for i, d in enumerate(items):
                p = VMobject().set_points_as_corners([d.get_center(), [0, 1.55, 0], [0, -1.55, 0], [1.9 + 0.55 * i, -1.9, 0]])
                paths.append(MoveAlongPath(d, p, rate_func=linear))
            return LaggedStart(*paths, lag_ratio=0.3, run_time=t)

        self.at("Lactate leaves", lead=0.3)
        trl = lab("transporter", 3.6, 1.2, 26, GREY)
        trl_line = leader([2.2, 1.12, 0], [0.9, 0.6, 0], GREY)
        self.play(stream(ds, 2.4), Succession(Wait(0.8), FadeIn(trl), FadeIn(trl_line)), run_time=2.4)
        self.at("In 2012")
        credit = lab("Lee, Rothstein and colleagues, 2012", 0.0, -3.1, 26, GREY)
        ds2 = VGroup(lac_dot(-2.4, 1.55), pyr_dot(-1.95, 1.55), lac_dot(-1.5, 1.55))
        self.play(FadeIn(credit), FadeIn(ds2), run_time=0.4)
        self.play(stream(ds2, 1.9), run_time=1.9)
        self.at("that one MCT1")
        mct = lab("MCT1", 3.6, 1.2, 30, GREY, weight=BOLD)
        self.play(FadeOut(trl), run_time=0.25)
        ds3 = VGroup(lac_dot(-2.4, 1.55), pyr_dot(-1.95, 1.55), lac_dot(-1.5, 1.55))
        self.play(FadeIn(mct), FadeIn(ds3), run_time=0.25)
        self.play(stream(ds3, 1.5), run_time=1.5)
        self.at("is concentrated")
        old = Group(*self.mobjects)
        panel = rrect(11.6, 5.7, GREY, 0.0, 3, 0.3).move_to([0, 0.1, 0])
        panel.set_fill("#171a24", 1)
        oligo_xy = [(-4.0, 0.6), (-0.9, -1.3), (2.6, 1.0), (4.3, -1.3)]
        oligos = VGroup()
        for (x, y) in oligo_xy:
            body = Ellipse(width=1.7, height=1.1, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.1)
            procs = VGroup(*[Line([0.7 * np.cos(np.radians(a)), 0.45 * np.sin(np.radians(a)), 0],
                                  [1.25 * np.cos(np.radians(a)), 0.85 * np.sin(np.radians(a)), 0], color=TEAL, stroke_width=3)
                             for a in (35, 145, 215, 325)])
            oligos.add(VGroup(body, procs).move_to([x, y, 0]))
        others_xy = [(-5.2, -1.1), (-1.6, 2.4), (-2.3, -0.2), (0.4, 1.4), (1.2, -2.1), (5.0, 2.2), (5.2, 0.3), (-5.2, 2.3)]
        others = VGroup(*[Circle(radius=0.3, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.18)
                          .move_to([x, y, 0]) for x, y in others_xy])
        self.play(FadeOut(old), FadeIn(panel), FadeIn(oligos), FadeIn(others), run_time=0.5)
        self.at("concentrated in")
        glow = [c[0] for c in oligos]
        sig = lab("MCT1 signal", 4.3, -2.3, 26, GREEN)
        self.play(*[g.animate.set_fill(GREEN, 0.8) for g in glow], FadeIn(sig), run_time=0.7)
        self.at("oligodendrocytes")
        ol = lab("oligodendrocyte", -3.9, 1.75, 26, TEAL)
        ot = lab("other cells", -4.2, -2.3, 26, GREY)
        self.play(FadeIn(ol), FadeIn(ot), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Setup(SpokenScene):
    def construct(self):
        dish, slc, dl = dish_parts()
        self.add(dish, slc, dl)
        self.at("withheld glucose")
        glu = glucose_out()
        r1 = row(0)
        self.play(FadeIn(glu[0], shift=DOWN * 0.1), FadeIn(r1), run_time=0.5)
        self.play(FadeIn(glu[1], scale=0.6), run_time=0.3)
        self.at("a drug that blocks")
        blk = blocker_chip().move_to(GLU_XY)
        r2 = row(1)
        self.play(FadeOut(glu), FadeIn(blk), FadeIn(r2), run_time=0.5)
        self.play(blk.animate.move_to(BLK_XY), run_time=0.9)
        self.at("also got lactate")
        lc = lactate_chip().move_to(GLU_XY)
        r3 = row(2)
        self.play(FadeIn(lc), FadeIn(r3), run_time=0.5)
        self.play(lc.animate.move_to(LAC_XY), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S04Q(SpokenScene):
    def construct(self):
        rows = VGroup(row(0), row(1), row(2))
        box, title, neus, qs, ask = predict_card()
        self.add(rows, box, title, ask)
        self.at("motor neurons")
        self.play(LaggedStart(*[FadeIn(n) for n in neus], lag_ratio=0.2), run_time=0.6)
        self.at("each condition")
        self.play(LaggedStart(*[FadeIn(q) for q in qs], lag_ratio=0.2), run_time=0.5)
        for r in rows:
            self.play(Indicate(r[1], color=TEXT, scale_factor=1.04), run_time=0.25)
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        rows = VGroup(row(0), row(1), row(2))
        box, title, neus, qs, ask = predict_card()
        bar = Rectangle(width=5.0, height=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([-3.5, -3.4, 0])
        self.add(rows, box, title, neus, qs, ask, bar)
        bar.add_updater(lambda m, dt: m.stretch(max(0.01, m.width - 1.0 * dt) / m.width, 0, about_edge=LEFT))
        nums = [lab(str(n), -1.15, 3.05, 44, GOLD, weight=BOLD) for n in (5, 4, 3, 2, 1)]
        seq = Succession(*[Succession(FadeIn(n, run_time=0.2), Wait(0.6), FadeOut(n, run_time=0.2)) for n in nums])
        self.play(seq)
        bar.clear_updaters()
        self.finish()


# ----------------------------------------------------------------------------------------------
def ring6():
    return Circle(radius=1.15, stroke_color=GREEN, stroke_width=6).move_to(NEU6)


def verdict_ok():
    return lab("motor neuron survives", -3.45, -1.75, 30, GREEN, weight=BOLD)


def verdict_bad():
    return lab("motor neuron lost", -3.45, -1.75, 30, RED, weight=BOLD)


def annot3():
    a1 = lab("lactate added,", 3.65, -2.95, 26, ORANGE)
    a2 = lab("MCT1 still blocked", 3.65, -3.42, 26, RED)
    return a1, a2


class S06Reveal(SpokenScene):
    def construct(self):
        dish, slc, dl = dish_parts()
        rows = VGroup(row(0), row(1), row(2))
        glu = glucose_out()
        cur = neuron_icon(NEU6, 0.8)
        self.add(dish, slc, dl, rows, glu, cur)
        self.at("glucose withheld")
        self.play(Indicate(rows[0][0], color=TEXT, scale_factor=1.05), run_time=0.6)
        self.at("they survived")
        rr, tx = result(0, True)
        rg, vd = ring6(), verdict_ok()
        self.play(GrowFromEdge(rr, LEFT), FadeIn(tx), Create(rg), FadeIn(vd), run_time=0.7)
        self.at("Add the blocker")
        blk = blocker_chip().move_to(GLU_XY)
        self.play(FadeOut(rg), FadeOut(vd), FadeOut(glu), FadeIn(blk), Indicate(rows[1][0], color=TEXT, scale_factor=1.05),
                  run_time=0.5)
        self.play(blk.animate.move_to(BLK_XY), run_time=0.7)
        self.at("they died")
        rr2, tx2 = result(1, False)
        dead = neuron_dead(NEU6, 0.8)
        vb = verdict_bad()
        self.play(GrowFromEdge(rr2, LEFT), FadeIn(tx2), ReplacementTransform(cur, dead), FadeIn(vb), run_time=1.0)
        cur = dead
        self.at("Add lactate")
        lc = lactate_chip().move_to(GLU_XY)
        alive = neuron_icon(NEU6, 0.8)
        self.play(FadeOut(vb), ReplacementTransform(cur, alive), FadeIn(lc), Indicate(rows[2][0], color=TEXT, scale_factor=1.05),
                  run_time=0.6)
        cur = alive
        self.play(lc.animate.move_to(LAC_XY), run_time=0.7)
        self.at("with the blocker still on")
        a1, a2 = annot3()
        self.play(FadeIn(a1), FadeIn(a2), run_time=0.5)
        self.at("they survived", nth=1)
        rr3, tx3 = result(2, True)
        rg, vd = ring6(), verdict_ok()
        self.play(GrowFromEdge(rr3, LEFT), FadeIn(tx3), Create(rg), FadeIn(vd), run_time=0.7)
        self.finish()


def final_state():
    dish, slc, dl = dish_parts()
    rows = [row(0), row(1), row(2)]
    res = [result(0, True), result(1, False), result(2, True)]
    a1, a2 = annot3()
    neu = neuron_icon(NEU6, 0.8)
    rg, vd = ring6(), verdict_ok()
    blk = blocker_chip().move_to(BLK_XY)
    lc = lactate_chip().move_to(LAC_XY)
    return dict(dish=dish, slc=slc, dl=dl, rows=rows, res=res, ann=(a1, a2), neu=neu, ring=rg, vd=vd, blk=blk, lc=lc)


def final_bars():
    rows = [row(0), row(1), row(2)]
    res = [result(0, True), result(1, False), result(2, True)]
    a1, a2 = annot3()
    return rows, res, (a1, a2)


class S07Beat(NarratedScene):
    def construct(self):
        f = final_state()
        hl = rrect(BW + 0.3, 1.15, YELLOW, 0.0, 6, 0.25).move_to([BCX, ROW_Y[2], 0])
        self.add(f["dish"], f["slc"], f["dl"], *f["rows"], *[m for p in f["res"] for m in p], *f["ann"],
                 f["neu"], f["ring"], f["vd"], f["blk"], f["lc"], hl)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S08Rescue(SpokenScene):
    def construct(self):
        rows, res, ann = final_bars()
        self.add(*rows, *[m for p in res for m in p], *ann)
        # the rescue arrow runs from the died bar to the survived bar, with a question mark
        ar = arr([5.9, -0.5, 0], [5.9, -1.5, 0], GREEN, 7, 0.28)
        qm = lab("?", 6.45, -1.0, 40, GOLD, weight=BOLD)
        self.at("a rescue", lead=0.1)
        word = T("rescue", 52, GREEN, font=TITLE_FONT).move_to([-3.55, 3.25, 0])
        self.play(FadeIn(word, shift=UP * 0.15), GrowArrow(ar), FadeIn(qm), run_time=0.6)
        self.at("best reading")
        tag_a = chip("block: is it necessary?", RED, 26).move_to([-3.2, 0.0, 0])
        la = DashedLine([tag_a.get_right()[0], 0.0, 0], [0.62, 0.0, 0], color=RED, stroke_width=4, dash_length=0.15)
        tag_b = chip("add back: is it enough?", ORANGE, 26).move_to([-3.55, -1.45, 0])
        lb = leader([tag_b.get_right()[0], -1.45, 0], [0.62, -1.85, 0], ORANGE, 4)
        self.play(FadeIn(tag_a, shift=RIGHT * 0.2), Create(la), run_time=0.5)
        self.play(FadeIn(tag_b, shift=RIGHT * 0.2), Create(lb), run_time=0.5)
        self.at("lacked lactate")
        self.play(Indicate(rows[1][1], color=TEXT, scale_factor=1.04), run_time=0.5)
        self.play(Indicate(rows[2][1], color=TEXT, scale_factor=1.04), run_time=0.5)
        self.at("which glia")
        tag_c = chip("lactate: glia are thought to supply it", TEAL, 26).move_to([-3.55, -2.55, 0])
        lc_ = leader([tag_c.get_right()[0], -2.55, 0], [0.62, -2.15, 0], TEAL, 4)
        self.play(FadeIn(tag_c, shift=UP * 0.15), Create(lc_), run_time=0.6)
        self.at("other drug effects")
        hedge = chipn(["other drug effects not ruled out", "the drug acts on every", "cell in the slice"], YELLOW, 26)
        hedge.move_to([-3.55, 1.55, 0])
        self.play(FadeIn(hedge, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S09Vivo(SpokenScene):
    def construct(self):
        ys = [2.35, 0.0, -2.35]
        somas = VGroup(*[Circle(radius=0.75, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3)
                         .move_to([-5.4, y, 0]) for y in ys])
        axs = [seg_axon(-4.5, 6.6, y, 9, 0.5) for y in ys]
        hdr = lab("living mice: the spinal cord", -2.2, 3.6, 28, GREY)
        cl = lab("motor neuron cell bodies", -3.6, -3.55, 26, BLUE)
        self.add(hdr, somas, cl)
        self.play(*[GrowFromEdge(a, LEFT) for a in axs], run_time=1.0)
        self.at("lowering MCT1")
        chp = chip("MCT1 lowered", RED, 26).move_to([4.6, 3.5, 0])
        self.play(FadeIn(chp, shift=DOWN * 0.1), run_time=0.5)
        self.at("made axons swell")
        h = 1.0
        sw = VGroup(swellings(axs[0], [3, 7], h), swellings(axs[1], [2, 5, 8], h), swellings(axs[2], [4, 6], h))
        sx = axs[2][6].get_center()[0]
        swl = lab("axon swellings", sx, -3.55, 26, RED)
        swl_ln = leader([sx, -3.3, 0], [sx, -2.35 - h / 2 - 0.02, 0], RED, 3)
        self.play(LaggedStart(*[GrowFromCenter(s) for g in sw for s in g], lag_ratio=0.1), run_time=1.1)
        self.play(FadeIn(swl), Create(swl_ln), run_time=0.4)
        self.at("and degenerate")
        anims = []
        for a in axs:
            anims += [Transform(s, t) for s, t in zip(a, degraded(a))]
        fx = axs[2][4].get_center()[0]
        frl = lab("axons fragment", fx + 0.9, -3.55, 26, RED)
        frl_ln = leader([fx, -3.3, 0], [fx, -2.35 - 0.3, 0], RED, 3)
        self.play(*anims, FadeOut(swl), FadeOut(swl_ln), run_time=0.5)
        self.play(FadeIn(frl), Create(frl_ln), run_time=0.6)
        self.at("Motor neurons were lost")
        lost = lab("cell bodies lost", -3.6, -3.55, 26, RED)
        ghosts = VGroup(*[DashedVMobject(Circle(radius=0.75, stroke_color=GREY, stroke_width=3).move_to(s.get_center()),
                                         num_dashes=18) for s in somas])
        deadsoma = [s.copy().set_color(GREY).set_stroke(opacity=0.2).set_fill(opacity=0.03) for s in somas]
        self.play(*[Transform(s, d) for s, d in zip(somas, deadsoma)], FadeIn(ghosts), FadeOut(cl), FadeIn(lost),
                  run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------------------------
# stage for the ageing timeline (s10, s11): glia band, myelinated axon, timeline
AG_Y = 0.2            # myelin / axon centre line
TL_Y = -2.6           # timeline
RES_Y = -1.85         # result text


def age_stage(thin=False):
    band = rrect(11.8, 1.5, TEAL, 0.14, 4, 0.6).move_to([0, 2.3, 0])
    sh = 1.1 if thin else 1.8
    sheaths = VGroup(*[rrect(2.0, sh, GREY, 0.5, 3, 0.35).move_to([x, AG_Y, 0]) for x in (-4.6, -2.3, 0, 2.3, 4.6)])
    segs = seg_axon(-5.9, 5.9, AG_Y, 10, 0.8)
    g = gate(3.45, 1.5, h=0.8)
    return band, sheaths, segs, g


def age_labels():
    ml = lab("myelin", -4.6, -1.15, 26, GREY)
    ml_ln = leader([-4.6, -0.95, 0], [-4.6, -0.45, 0], GREY)
    al = lab("axon", -1.15, -1.15, 26, BLUE)
    al_ln = leader([-1.15, -0.95, 0], [-1.15, -0.2, 0], BLUE)
    return ml, ml_ln, al, al_ln


def timeline():
    return Arrow([-5.8, TL_Y, 0], [5.8, TL_Y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)


class S10Clean(SpokenScene):
    def construct(self):
        band, sheaths, segs, g = age_stage()
        ml, ml_ln, al, al_ln = age_labels()
        mlab = lab("MCT1", 4.4, 2.3, 26, GREY)
        self.add(band, sheaths, segs, g, mlab, ml, ml_ln, al, al_ln)
        self.at("cleaner test")
        self.play(Indicate(g, color=TEXT, scale_factor=1.12), run_time=0.6)
        self.at("in 2021")
        credit = lab("Philips and colleagues, 2021", 0, 3.5, 26, GREY)
        tl = timeline()
        self.play(FadeIn(credit), Create(tl), run_time=0.6)
        self.at("Deleting MCT1")
        x = cross([3.45, 1.5, 0], RED, 0.4)
        mlab2 = lab("MCT1 deleted", 4.4, 2.3, 26, RED)
        self.play(g.animate.set_color(RED), FadeIn(x), FadeOut(mlab), FadeIn(mlab2), run_time=0.6)
        self.at("only in oligodendrocyte")
        ol = lab("oligodendrocyte lineage cells", -2.3, 2.3, 26, TEAL)
        self.play(FadeIn(ol), run_time=0.6)
        self.at("young mice")
        mk = Circle(radius=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([-4.5, TL_Y, 0])
        yl = lab("young", -4.5, TL_Y - 0.5, 26, GOLD)
        self.play(FadeIn(mk, scale=0.5), FadeIn(yl), run_time=0.5)
        self.at("normal")
        ok = lab("axons normal", 0.3, RES_Y, 30, GREEN, weight=BOLD)
        tk = tick([-1.9, RES_Y, 0], 0.25)
        self.play(FadeIn(ok), FadeIn(tk), run_time=0.4)
        self.finish()


class S11Age(SpokenScene):
    def construct(self):
        band, sheaths, segs, g = age_stage()
        ml, ml_ln, al, al_ln = age_labels()
        g.set_color(RED)
        x = cross([3.45, 1.5, 0], RED, 0.4)
        mlab2 = lab("MCT1 deleted", 4.4, 2.3, 26, RED)
        credit = lab("Philips and colleagues, 2021", 0, 3.5, 26, GREY)
        ol = lab("oligodendrocyte lineage cells", -2.3, 2.3, 26, TEAL)
        tl = timeline()
        mk = Circle(radius=0.2, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([-4.5, TL_Y, 0])
        yl = lab("young", -4.5, TL_Y - 0.5, 26, GOLD)
        ok = lab("axons normal", 0.3, RES_Y, 30, GREEN, weight=BOLD)
        tk = tick([-1.9, RES_Y, 0], 0.25)
        self.add(band, sheaths, segs, g, x, mlab2, credit, ol, tl, mk, yl, ok, tk, ml, ml_ln, al, al_ln)
        self.at("aged", lead=0.1)
        old_l = lab("old", 4.5, TL_Y - 0.5, 26, GOLD)
        self.play(mk.animate.move_to([4.5, TL_Y, 0]), FadeIn(old_l), FadeOut(ok), FadeOut(tk), run_time=0.9)
        self.at("axons degenerated", lead=0.1)
        sw = swellings(segs, [2, 5, 8], 1.05)
        bad = lab("axons degenerating", 0.3, RES_Y, 30, RED, weight=BOLD)
        self.play(*[Transform(s, t) for s, t in zip(segs, degraded(segs))],
                  LaggedStart(*[GrowFromCenter(s) for s in sw], lag_ratio=0.2), FadeIn(bad), run_time=0.9)
        self.at("myelin thinned", lead=0.55)
        thin = VGroup(*[rrect(2.0, 1.1, GREY, 0.5, 3, 0.35).move_to([xx, AG_Y, 0]) for xx in (-4.6, -2.3, 0, 2.3, 4.6)])
        ml2 = lab("myelin thinner", -4.6, -1.15, 26, GREY)
        self.play(Transform(sheaths, thin), FadeTransform(ml, ml2), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
# split screen (s12)
LX, RX = -3.55, 3.55
SW = 5.8
HDR_Y, CELL_Y, GATE_Y2, AXS_Y, THIN_Y, RES2_Y, CAP_Y = 3.55, 2.35, 0.95, -0.55, -1.7, -2.35, -3.2


def split_parts():
    p = {}
    p["div"] = DashedLine([0, 3.8, 0], [0, -3.6, 0], color=GREY, stroke_width=3, dash_length=0.2)
    for tag, cx in (("l", LX), ("r", RX)):
        p["cell_" + tag] = rrect(SW, 1.7, TEAL, 0.14, 4, 0.5).move_to([cx, CELL_Y, 0])
        p["ol_" + tag] = lab("oligodendrocyte", cx - 1.35, CELL_Y + 0.5, 26, TEAL)
        p["gt_" + tag] = gate(cx + 2.0, GATE_Y2, h=0.8)
        p["sl_" + tag], p["sg_" + tag] = strip(cx, AXS_Y, SW, 8, 0.9, 1.6)
    p["hdr_l"] = lab("adult CNS: Cox10 deleted", LX, HDR_Y, 26, TEAL)
    p["hdr_r"] = lab("ageing mice: MCT1 deleted", RX, HDR_Y, 26, TEAL)
    p["mito"] = mito(LX - 2.3, CELL_Y - 0.35, 1.0, 0.55)
    p["resp"] = lab("respiration", LX - 0.9, CELL_Y - 0.35, 26, YELLOW)
    p["mito_x"] = cross([LX - 2.3, CELL_Y - 0.35, 0], RED, 0.35)
    p["off"] = lab("respiration switched off", LX, CAP_Y, 26, GREY)
    p["mct_l"] = lab("MCT1 intact", LX - 0.4, GATE_Y2, 26, GREY)
    p["mct_r"] = lab("MCT1 removed", RX - 0.5, GATE_Y2, 26, RED)
    p["ver_l"] = lab("axon spared", LX + 0.4, RES2_Y, 30, GREEN, weight=BOLD)
    p["tick"] = tick([LX - 1.3, RES2_Y, 0], 0.25)
    p["gt_x"] = cross([RX + 2.0, GATE_Y2, 0], RED, 0.4)
    p["rem1"] = lab("monocarboxylate", RX, CAP_Y + 0.22, 26, GREY)
    p["rem2"] = lab("transport removed", RX, CAP_Y - 0.22, 26, GREY)
    p["ver_r"] = lab("axons degenerate", RX + 0.5, RES2_Y, 30, RED, weight=BOLD)
    p["x_r"] = cross([RX - 1.75, RES2_Y, 0], RED, 0.25)
    p["thin"] = lab("myelin thinner", RX, THIN_Y, 26, GREY)
    return p


class S12Split(SpokenScene):
    def construct(self):
        p = split_parts()
        self.add(p["div"], p["cell_l"], p["ol_l"], p["gt_l"], p["sl_l"], p["sg_l"],
                 p["cell_r"], p["ol_r"], p["gt_r"], p["sl_r"], p["sg_r"])
        self.at("with glial respiration")
        self.play(FadeIn(p["hdr_l"]), FadeIn(p["mito"]), FadeIn(p["resp"]), run_time=0.6)
        self.at("switched off")
        self.play(FadeIn(p["mito_x"]), p["mito"].animate.set_stroke(opacity=0.35).set_fill(opacity=0.05),
                  p["resp"].animate.set_opacity(0.4), FadeIn(p["off"]), run_time=0.7)
        self.at("adult brain axons")
        self.play(FadeIn(p["mct_l"]), Indicate(p["sg_l"], color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("were spared")
        self.play(FadeIn(p["ver_l"]), Create(p["tick"]), run_time=0.6)
        self.at("Remove MCT1")
        self.play(FadeIn(p["hdr_r"]), FadeIn(p["mct_r"]), p["gt_r"].animate.set_color(RED), FadeIn(p["gt_x"]), run_time=0.7)
        self.at("the proposed export route")
        self.play(FadeIn(p["rem1"]), FadeIn(p["rem2"]), Indicate(p["gt_r"], color=TEXT, scale_factor=1.15), run_time=0.7)
        self.at("axons degenerate")
        sw = swellings(p["sg_r"], [2, 5], 1.2)
        thin_sl, _ = strip(RX, AXS_Y, SW, 8, 0.9, 1.6, thin=True)
        self.play(*[Transform(s, t) for s, t in zip(p["sg_r"], degraded(p["sg_r"]))],
                  Transform(p["sl_r"], thin_sl),
                  LaggedStart(*[GrowFromCenter(s) for s in sw], lag_ratio=0.3),
                  FadeIn(p["ver_r"]), FadeIn(p["x_r"]), FadeIn(p["thin"]), run_time=1.1)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S13Caveat(SpokenScene):
    def construct(self):
        # top: the two outcomes, smaller (carried over from the split screen)
        AY = 2.35
        hdr_l = lab("adult CNS: Cox10 deleted", LX, 3.55, 26, TEAL)
        hdr_r = lab("ageing mice: MCT1 deleted", RX, 3.55, 26, TEAL)
        div = DashedLine([0, 3.8, 0], [0, -1.65, 0], color=GREY, stroke_width=3, dash_length=0.2)
        sl_l, sg_l = strip(LX, AY, SW, 8, 0.7, 1.2)
        sl_r, sg_r = strip(RX, AY, SW, 8, 0.7, 1.2, thin=True)
        for s, t in zip(sg_r, degraded(sg_r)):
            s.become(t)
        sw = swellings(sg_r, [2, 5], 0.95)
        ver_l = lab("axon spared", LX, 1.4, 26, GREEN, weight=BOLD)
        ver_r = lab("axons degenerate", RX, 1.4, 26, RED, weight=BOLD)
        self.add(hdr_l, hdr_r, div, sl_l, sg_l, sl_r, sg_r, sw, ver_l, ver_r)
        # bottom: the caution card, with the word "caution" above its two lines
        box = rrect(11.8, 1.9, YELLOW, 0.08, 3, 0.25).move_to([0, -2.75, 0])
        t0 = lab("caution", 0, -2.15, 28, YELLOW, weight=BOLD)
        self.at("One caution", lead=0.0)
        self.play(FadeIn(box), FadeIn(t0), run_time=0.4)
        self.at("not followed")
        l1 = lab("the two sets of mice were not followed over matched ages", 0, -2.7, 26, TEXT)
        # two timeline strips of different length
        BY = -0.15
        bl = rrect(3.2, 0.4, BLUE, 0.5, 3, 0.15).move_to([-6.2 + 1.6, BY, 0])
        br = rrect(5.8, 0.4, BLUE, 0.5, 3, 0.15).move_to([0.5 + 2.9, BY, 0])
        cl = lab("months studied", -4.6, BY - 0.55, 26, TEXT)
        cr = lab("ageing mice: to old age", 3.4, BY - 0.55, 26, TEXT)
        self.play(FadeIn(l1), GrowFromEdge(bl, LEFT), GrowFromEdge(br, LEFT), run_time=0.7)
        self.play(FadeIn(cl), FadeIn(cr), run_time=0.4)
        self.at("matched ages")
        g1 = DashedLine([-3.0, BY - 0.25, 0], [-3.0, -1.2, 0], color=YELLOW, stroke_width=3, dash_length=0.12)
        g2 = DashedLine([6.3, BY - 0.25, 0], [6.3, -1.2, 0], color=YELLOW, stroke_width=3, dash_length=0.12)
        da = DoubleArrow([-3.0, -1.2, 0], [6.3, -1.2, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.2)
        nm = lab("not matched", 1.65, -1.5, 26, YELLOW, weight=BOLD)
        self.play(Create(g1), Create(g2), GrowFromCenter(da), FadeIn(nm), run_time=0.7)
        self.at("myelin also thinned", lead=0.35)
        l2 = lab("myelin also thinned late", 0, -3.2, 26, TEXT)
        note = lab("myelin thinned late", RX, 0.88, 26, TEXT)
        self.play(FadeIn(l2), FadeIn(note), run_time=0.25)
        self.play(Indicate(sl_r, color=TEXT, scale_factor=1.0), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S14Picture(SpokenScene):
    def construct(self):
        glia = rrect(11.8, 2.2, TEAL, 0.14, 4, 0.7).move_to([0, 1.95, 0])
        ax = rrect(11.8, 3.4, BLUE, 0.14, 4, 0.7).move_to([0, -1.85, 0])
        title = lab("the picture that fits", 0, 3.5, 32, GOLD)
        self.add(glia, ax, title)
        self.at("Oligodendrocytes")
        gl = lab("oligodendrocyte", -4.0, 2.7, 26, TEAL)
        glu = chip("glucose", TEXT, 26).move_to([-4.75, 1.7, 0])
        self.play(FadeIn(gl), FadeIn(glu), run_time=0.5)
        self.at("run glycolysis")
        gly = chip("glycolysis", ORANGE, 26).move_to([-2.0, 1.7, 0])
        a1 = arr(glu.get_right() + RIGHT * 0.05, gly.get_left(), GREY)
        self.play(GrowArrow(a1), FadeIn(gly), run_time=0.7)
        self.at("export lactate")
        lc = chip("lactate or pyruvate", ORANGE, 26).move_to([2.0, 1.7, 0])
        a2 = arr(gly.get_right() + RIGHT * 0.05, lc.get_left(), ORANGE)
        g = gate(2.0, 0.35, h=0.95)
        self.play(GrowArrow(a2), FadeIn(lc), FadeIn(g), run_time=0.8)
        self.at("through MCT1")
        gtl = lab("MCT1", 3.5, 0.35, 26, GREY)
        dash = DashedLine([2.0, 1.35, 0], [2.0, -0.6, 0], color=ORANGE, stroke_width=6, dash_length=0.18)
        dash.add_tip(tip_length=0.28)
        d0 = lac_dot(2.0, 1.7, 0.2)
        path = VMobject().set_points_as_corners([[2.0, 1.7, 0], [2.0, 0.35, 0], [2.0, -1.1, 0]])
        self.add(d0)
        self.play(FadeIn(gtl), Create(dash), MoveAlongPath(d0, path, rate_func=linear), run_time=2.0)
        c2 = chip("lactate", ORANGE, 26).move_to([2.0, -1.2, 0])
        self.play(ReplacementTransform(d0, c2), run_time=0.3)
        self.at("axon turns")
        al = lab("axon", -5.1, -0.65, 26, BLUE)
        self.play(FadeIn(al), run_time=0.4)
        self.at("any lactate back")
        self.play(Indicate(c2, color=TEXT, scale_factor=1.15), run_time=0.7)
        self.at("into pyruvate")
        pyr = chip("pyruvate", ORANGE, 26).move_to([2.0, -1.2, 0])
        self.play(ReplacementTransform(c2, pyr), run_time=0.6)
        # Establish the large mitochondrion before the final spoken clause.
        self.at("burns it", lead=0.6)
        mt = mito(-0.8, -2.15, 3.7, 1.65)
        mtl = lab("own mitochondria", -0.8, -3.25, 28, YELLOW)
        a3 = arr([1.6, -1.5, 0], [0.9, -1.95, 0], ORANGE, 6, 0.24)
        self.play(FadeIn(mt), FadeIn(mtl), GrowArrow(a3), run_time=0.35)
        # The open orange chip is pyruvate; move it into the mitochondrion.
        self.at("own mitochondria", lead=1.0)
        self.play(pyr.animate.scale(0.7).move_to([-0.8, -2.15, 0]), run_time=0.35)
        atp = chip("ATP", YELLOW, 32).move_to([-4.55, -2.15, 0])
        a4 = arr([-2.7, -2.15, 0], [-3.8, -2.15, 0], YELLOW, 6, 0.24)
        self.play(FadeOut(pyr), GrowArrow(a4), FadeIn(atp), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------------------------
UNK_X = 2.65


def unknown_parts():
    p = {}
    p["box"] = rrect(4.9, 6.2, GOLD, 0.06, 3, 0.3).move_to([-4.25, 0.0, 0])
    p["title"] = lab("Still unknown", -4.25, 2.55, 38, GOLD, font=TITLE_FONT)
    p["l1"] = lab("the exact route", -4.25, 1.35, 28, TEXT)
    p["l2"] = VGroup(lab("how much of", -4.25, 0.25, 28, TEXT), lab("the axon's ATP", -4.25, -0.2, 28, TEXT),
                     lab("this supplies", -4.25, -0.65, 28, TEXT))
    p["inf"] = VGroup(lab("inferred,", -4.25, -1.85, 30, YELLOW, weight=BOLD), lab("not traced", -4.25, -2.35, 30, YELLOW, weight=BOLD))
    p["glia"] = rrect(7.4, 2.1, TEAL, 0.14, 4, 0.5).move_to([UNK_X, 2.65, 0])
    p["gl"] = lab("glial cell", UNK_X - 2.4, 3.3, 26, TEAL)
    p["ax"] = rrect(7.4, 2.1, BLUE, 0.14, 4, 0.5).move_to([UNK_X, -2.65, 0])
    p["axl"] = lab("axon", UNK_X - 2.6, -3.3, 26, BLUE)
    p["dot"] = lac_dot(UNK_X - 2.0, 2.3, 0.22)
    p["dotl"] = lab("lactate or pyruvate", UNK_X + 0.2, 2.3, 26, ORANGE)
    p["path"] = DashedLine([UNK_X, 1.55, 0], [UNK_X, -0.15, 0], color=ORANGE, stroke_width=7, dash_length=0.2)
    p["q1"] = lab("?", UNK_X, -0.85, 80, GOLD, weight=BOLD)
    p["atp"] = chip("ATP", YELLOW, 28).move_to([UNK_X - 1.2, -2.35, 0])
    p["q2"] = lab("?", UNK_X + 0.8, -2.35, 64, GOLD, weight=BOLD)
    return p


class S15Unknown(SpokenScene):
    def construct(self):
        p = unknown_parts()
        self.add(p["box"], p["title"], p["glia"], p["gl"], p["ax"], p["axl"], p["dot"], p["dotl"])
        self.at("exact root")
        self.play(FadeIn(p["l1"]), Create(p["path"]), run_time=0.7)
        self.play(FadeIn(p["q1"], scale=0.5), run_time=0.4)
        self.at("how much")
        self.play(FadeIn(p["l2"]), FadeIn(p["atp"]), run_time=0.6)
        self.at("ATP this")
        self.play(FadeIn(p["q2"], scale=0.5), Indicate(p["atp"], color=TEXT, scale_factor=1.15), run_time=0.6)
        self.at("infer the transfer")
        self.play(FadeIn(p["inf"]), Indicate(p["path"], color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("traces it", lead=0.3)
        d = lac_dot(UNK_X, 1.55, 0.22)
        self.add(d)
        self.play(d.animate.move_to([UNK_X, -0.45, 0]), run_time=0.9)
        self.play(FadeOut(d), Indicate(p["q1"], color=TEXT, scale_factor=1.3), run_time=0.6)
        self.finish()


class S15bBeat(NarratedScene):
    def construct(self):
        self.add(*unknown_parts().values())
        self.finish()


# ----------------------------------------------------------------------------------------------
AST_C = [-3.5, 0.35, 0]
NEU_B = [3.5, 0.35, 0]


def blobs():
    astro = Ellipse(width=5.8, height=4.2, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.14).move_to(AST_C)
    neuron = Ellipse(width=5.8, height=4.2, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.14).move_to(NEU_B)
    al = lab("astrocyte", -3.5, 1.9, 30, PURPLE)
    nl = lab("neuron", 3.5, 1.9, 30, BLUE)
    return astro, neuron, al, nl


def dots_in(cx, pts):
    return VGroup(*[lac_dot(cx + x, 0.35 + y, 0.14) for x, y in pts])


ASTRO_PTS = [(-1.6, 0.5), (-0.9, 0.9), (-0.3, 0.45), (0.5, 0.95), (1.2, 0.4), (-1.3, -0.4), (-0.5, -0.1), (0.4, -0.35),
             (1.2, -0.5), (-0.1, 0.0)]
NEU_PTS = [(-0.4, 0.2), (0.7, -0.2)]


class S16Astro(SpokenScene):
    def construct(self):
        astro, neuron, al, nl = blobs()
        da = dots_in(AST_C[0], ASTRO_PTS)
        dn = dots_in(NEU_B[0], NEU_PTS)
        hi = lab("lactate: high", -3.5, -1.2, 26, ORANGE)
        lo = lab("lactate: low", 3.5, -1.2, 26, ORANGE)
        strips = VGroup(*[Rectangle(width=0.9, height=0.3, stroke_width=0, fill_color=ORANGE,
                                    fill_opacity=0.95 - 0.10 * i).move_to([-3.6 + 0.9 * i, -2.55, 0]) for i in range(9)])
        gl = lab("lactate level", 0.0, -2.0, 26, ORANGE)
        sp = lab("a gradient, not a measured flow", 0, -2.95, 26, TEXT)
        # The comparison and its limitation are visible together from the first frame.
        self.add(astro, neuron, al, nl, da, dn, hi, lo, strips, gl, sp)
        self.at("contested candidate")
        cand = chip("second candidate: contested", GOLD, 26).move_to([-3.5, 3.2, 0])
        self.play(FadeIn(cand, shift=DOWN * 0.1), run_time=0.5)
        self.at("One sensor study")
        fr = chip("for: one sensor study", GREEN, 26).move_to([3.5, 3.2, 0])
        credit = lab("Mächler, Weber and colleagues, 2016", 0.0, -3.5, 26, GREY)
        self.play(FadeIn(fr, shift=DOWN * 0.1), FadeIn(credit), run_time=0.5)
        self.at("a lactate gradient")
        self.play(Indicate(strips, color=ORANGE, scale_factor=1.03), run_time=0.7)
        self.at("to neurons")
        self.play(Indicate(dn, color=ORANGE, scale_factor=1.25), run_time=0.5)
        self.finish()


class S17Against(SpokenScene):
    def construct(self):
        astro, neuron, al, nl = blobs()
        # Give the neuronal evidence most of the screen; compress the source cell.
        astro.stretch_to_fit_width(3.0).move_to([-4.7, 0.35, 0])
        al.move_to([-4.7, 1.9, 0])
        neuron.stretch_to_fit_width(7.5).move_to([2.4, 0.35, 0])
        nl.move_to([2.4, 1.9, 0])
        credit = lab("Yellen laboratory, 2017", 0.0, -3.4, 26, GREY)
        self.add(astro, neuron, al, nl)
        ag = chip("against: another study", RED, 26).move_to([3.5, 3.2, 0])
        self.play(FadeIn(ag, shift=DOWN * 0.1), FadeIn(credit), run_time=0.5)
        self.at("stimulated neurons")
        nl2 = lab("stimulated neuron", 2.4, 1.9, 30, BLUE)
        self.play(FadeTransform(nl, nl2), neuron.animate.set_fill(BLUE, 0.4), run_time=0.6)
        self.at("their own glycolysis")
        gly = chipn(["own glycolysis", "rises"], ORANGE, 38, pad=0.3).move_to([2.0, 0.1, 0])
        up = arr([5.0, -1.3, 0], [5.0, 1.25, 0], ORANGE, 22, 0.6)
        self.play(FadeIn(gly), run_time=0.4)
        self.play(GrowArrow(up), run_time=0.9)
        self.at("no sign of lactate import")
        ghost = DashedLine([-4.0, 0.35, 0], [-0.7, 0.35, 0], color=GREY, stroke_width=5, dash_length=0.18)
        ghost.add_tip(tip_length=0.25)
        xg = cross([-2.4, 0.35, 0], RED, 0.4)
        no = lab("no sign of lactate import", 0, -2.35, 26, RED)
        self.play(Create(ghost), run_time=0.4)
        self.play(FadeIn(xg), FadeIn(no), run_time=0.5)
        self.finish()


class S18AstroTake(SpokenScene):
    def construct(self):
        astro, neuron, al, nl = blobs()
        self.add(astro, neuron, al, nl)
        self.at("astrocyte shuttle")
        sh = DashedLine([-1.5, 0.35, 0], [1.5, 0.35, 0], color=ORANGE, stroke_width=7, dash_length=0.18)
        sh.add_tip(tip_length=0.28)
        shl = lab("astrocyte-neuron lactate shuttle", 0, 3.35, 30, ORANGE)
        q = lab("?", 0, 1.15, 64, GOLD, weight=BOLD)
        self.play(Create(sh), FadeIn(shl), FadeIn(q), run_time=0.9)
        self.at("a hypothesis")
        hyp = lab("a hypothesis", 0, -3.2, 44, GOLD, font=TITLE_FONT)
        self.play(FadeIn(hyp, shift=UP * 0.1), run_time=0.5)
        self.at("partial support")
        tf = chip("one study for", GREEN, 28).move_to([-2.9, -2.45, 0])
        ta = chip("one study against", RED, 28).move_to([2.9, -2.45, 0])
        self.play(FadeIn(tf, shift=UP * 0.1), FadeIn(ta, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S19Take(SpokenScene):
    def construct(self):
        sheaths = VGroup(*[rrect(2.0, 2.2, GREY, 0.5, 3, 0.35).move_to([x, -1.1, 0]) for x in (-4.6, -2.3, 0, 2.3, 4.6)])
        segs = seg_axon(-5.9, 5.9, -1.1, 10, 1.0)
        glia = Ellipse(width=6.4, height=1.7, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.18).move_to([0, 1.3, 0])
        procs = VGroup(*[Line([x * 0.55, 0.5, 0], [x, 0.0, 0], color=TEAL, stroke_width=6) for x in (-2.3, 0, 2.3)])
        self.add(sheaths, segs)
        self.play(FadeIn(glia), Create(procs), run_time=0.8)
        self.at("myelin")
        ml = lab("myelin", 0.0, -2.85, 26, GREY)
        al = lab("axon", -5.3, -2.85, 26, BLUE)
        ml_ln = leader([0.0, -2.62, 0], [0.0, -2.2, 0], GREY)
        al_ln = leader([-5.3, -2.62, 0], [-5.3, -1.62, 0], BLUE)
        self.play(FadeIn(ml), FadeIn(al), Create(ml_ln), Create(al_ln), run_time=0.5)
        self.at("evidence fits")
        gll = lab("oligodendrocyte", 0, 1.3, 30, TEAL)
        self.play(FadeIn(gll), run_time=0.5)
        self.at("Whoever wraps the axon")
        text = T("Whoever wraps the axon helps feed it.", 42, TEXT, font=TITLE_FONT)
        fit(text, max_w=12.2)
        text.move_to([0, 3.3, 0])
        self.play(FadeIn(text, shift=DOWN * 0.1), run_time=0.9)
        self.at("helps feed it")
        sm = lab("oligodendrocytes most clearly", 0, 2.6, 30, TEXT, weight=BOLD)
        ds = VGroup(*[lac_dot(x * 0.55, 0.55, 0.17) for x in (-2.3, 0, 2.3)])
        self.add(ds)
        self.play(FadeIn(sm), *[d.animate.move_to([x, -1.1, 0]) for d, x in zip(ds, (-2.3, 0, 2.3))], run_time=0.35)
        # Hold the fuel inside the blue axon so entry remains visible in the takeaway.
        self.play(Indicate(segs, color=GREEN, scale_factor=1.0), run_time=0.35)
        self.finish()


class S20End(EndCard):
    LINE = "Whoever wraps the axon helps feed it."
