"""Chapter 3, "A Tap at the Back, a Drain at the Front": retinoic acid as the signal that helps set the front edges of the Hox code.

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, shared by every chapter of this film; taken from scenes.old.py)
  ORANGE = retinoic acid (the drops, the dye, the curve, the dose)
  GREEN  = made / switched on (Raldh2, the tap, mesoderm)
  RED    = destroyed / blocked (Cyp26, the drain, a plugged drain)
  BLUE   = the retinoic acid receptors (RAR, RXR)
  PURPLE = Hox genes and the Hox code (four shades = four gene groups, 3' lightest; seven abstract shades = each
           rhombomere's identity, shown with a colour key)
  GOLD   = the short DNA stretch the receptor pair binds; "?" marks; credits
  TEAL   = trigeminal identity (jaw)         YELLOW = facial identity (face)
  ROSE   = neural crest cells (new in this chapter)
  GREY   = bulges, DNA, nucleus, axes;  LG = lighter grey for labels and captions

LAYOUT: the hindbrain row (r1 to r7 plus a labelled spinal-cord box) is a thin strip across the top of every scene
that needs it, front at the left, and is dropped when it is not the subject. The bath, curve and gene bars sit below
it and are aligned to its columns. The bath has the tap at the back (bottom right) and the drain at the front
(bottom left), and its chips hang off the pipes.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
HOX = ["#DCC8F4", "#C39EE6", "#A573CF", "#8650B8"]            # four Hox gene groups, 3' to 5'
IDENT = ["#C9B6F0", "#B49BE8", "#9E80DD", "#8863CF", "#7347BF", "#5F34A6", "#4C2A86"]   # r1..r7 identity
ROSE = "#E58FB0"
LG = "#BAC1CE"                                                  # label grey, brighter than GREY for captions

# ---- geometry shared by every scene -------------------------------------------------------------------
SX = [-5.0 + 1.4 * i for i in range(7)]      # rhombomere centres r1..r7 (front at the left)
SW = 1.3
BACKX = 4.05                                 # back edge of r7
TUBEX = 5.425                                # spinal-cord box centre
TOPY = 3.3                                   # y of the thin strip


def ex(k):
    """x of the front edge of rhombomere k (1..7)."""
    return SX[k - 1] - 0.65


# ---- the signal profile: steady dye from a tap at the back, falling off toward the front --------------
LAM, XT = 3.2, 5.6          # fall-off length and tap position (schematic; the lesson's e-fold picture)
PX0, PX1 = -5.4, 5.2


def conc(x, k=1.0):
    return float(min(1.0, k * np.exp((x - XT) / LAM)))


T3 = conc(ex(4))            # lower threshold  (3' gene, edge at the front of r4)
T5 = conc(ex(7))            # higher threshold (5' gene, edge at the front of r7)


def lab_color(fill):
    r, g, b = ManimColor(fill).to_rgb()
    return BG if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.19 else TEXT


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def drop(r=0.15, color=ORANGE):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def strip(y=TOPY, h=0.85, fills=None, op=0.85, tube=True):
    """The hindbrain row: bulges, r labels, labelled spinal-cord box. Returns bulges, r labels, tube box, tube label."""
    cr = min(0.3, h / 3)
    bs = VGroup(*[RoundedRectangle(corner_radius=cr, width=SW, height=h, stroke_color=GREY, stroke_width=3,
                                   fill_color=(fills[i] if fills else GREY),
                                   fill_opacity=(op if fills else 0.12)).move_to([SX[i], y, 0]) for i in range(7)])
    ly = y if h < 1.3 else y + h / 2 - 0.4
    labs = VGroup(*[T(f"r{i + 1}", 26, (lab_color(fills[i]) if fills else LG),
                      weight=(BOLD if fills else NORMAL)).move_to([SX[i], ly, 0]) for i in range(7)])
    tb = RoundedRectangle(corner_radius=cr, width=2.55, height=min(h, 1.0), stroke_color=GREY, stroke_width=3,
                          fill_color=GREY, fill_opacity=0.12).move_to([TUBEX, y, 0])
    cord = T("spinal cord", 26, LG).move_to(tb)
    return bs, labs, tb, cord


def bar(x_front, y, color, h=0.55, op=0.9, x_back=BACKX):
    return Rectangle(width=x_back - x_front, height=h, stroke_width=0, fill_color=color,
                     fill_opacity=op).move_to([(x_front + x_back) / 2, y, 0])


# ---- the plot ----------------------------------------------------------------------------------------
def plot_build(pb, ph, thr=False):
    """One VGroup, always with the same structure, so Transform can resize it: [fill, curve, base, yaxis, ylabel,
    front, back, thr3 line, thr3 label, thr5 line, thr5 label]; the threshold parts are invisible unless thr."""
    pts = [np.array([x, pb + ph * conc(x), 0]) for x in np.linspace(PX0, PX1, 80)]
    line = VMobject(stroke_color=ORANGE, stroke_width=6)
    line.set_points_smoothly(pts)
    poly = Polygon(*([np.array([PX0, pb, 0])] + pts + [np.array([PX1, pb, 0])]), stroke_width=0,
                   fill_color=ORANGE, fill_opacity=0.2)
    base = Line([PX0 - 0.25, pb, 0], [PX1 + 0.3, pb, 0], color=GREY, stroke_width=3)
    yax = Line([PX0 - 0.25, pb, 0], [PX0 - 0.25, pb + ph + 0.2, 0], color=GREY, stroke_width=3)
    yl = T("retinoic acid level", 26, ORANGE).rotate(PI / 2).move_to([PX0 - 0.75, pb + ph / 2, 0])
    front = T("front", 26, LG).move_to([PX0 + 0.35, pb - 0.38, 0])
    back = T("back", 26, LG).move_to([PX1 - 0.3, pb - 0.38, 0])
    o = 1.0 if thr else 0.0
    l3 = Line([PX0 - 0.25, pb + ph * T3, 0], [PX1 + 0.3, pb + ph * T3, 0], color=HOX[0], stroke_width=4).set_opacity(o)
    t3 = T("3′ genes: lower dose", 26, HOX[0]).move_to([PX0 + 1.75, pb + ph * T3 + 0.3, 0]).set_opacity(o)
    l5 = Line([PX0 - 0.25, pb + ph * T5, 0], [PX1 + 0.3, pb + ph * T5, 0], color=HOX[3], stroke_width=4).set_opacity(o)
    t5 = T("5′ genes: higher dose", 26, HOX[2]).move_to([PX0 + 1.85, pb + ph * T5 + 0.3, 0]).set_opacity(o)
    return VGroup(poly, line, base, yax, yl, front, back, l3, t3, l5, t5)


def cyv(pb, ph, c):
    return pb + ph * c


# ---- the bath ----------------------------------------------------------------------------------------
BX0, BX1 = -5.6, 5.4


def dye_op(x, k=1.0):
    return 0.03 + 0.72 * conc(x, k)


def bath2(yc, h, k=1.0, dye=True, labels=True):
    """A long bath: trough, dye slices, the tap at the back (right) and the drain at the front (left).
    In a tall bath both pipes sit near the bottom corners; in a thin one at mid-height."""
    trough = RoundedRectangle(corner_radius=0.35, width=BX1 - BX0, height=h, stroke_color=GREY,
                              stroke_width=4).move_to([(BX0 + BX1) / 2, yc, 0])
    xs = np.linspace(BX0 + 0.25, BX1 - 0.25, 44)
    w = xs[1] - xs[0]
    slices = VGroup(*[Rectangle(width=w + 0.012, height=h - 0.2, stroke_width=0, fill_color=ORANGE,
                                fill_opacity=(dye_op(x, k) if dye else 0.0)).move_to([x, yc, 0]) for x in xs])
    pipe_y = (yc - h / 2 + 0.3) if h > 2 else yc
    pipe_t = Rectangle(width=1.15, height=0.34, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                       fill_opacity=0.3).move_to([5.975, pipe_y, 0])
    handle = VGroup(Line([6.1, pipe_y + 0.17, 0], [6.1, pipe_y + 0.5, 0], color=GREEN, stroke_width=5),
                    Line([5.85, pipe_y + 0.5, 0], [6.35, pipe_y + 0.5, 0], color=GREEN, stroke_width=5))
    tap = VGroup(pipe_t, handle)
    lab_y = yc - h / 2 - 0.32
    tap_label = T("the tap", 26, GREEN).move_to([5.9, lab_y, 0])
    pipe_d = Rectangle(width=1.15, height=0.34, stroke_color=RED, stroke_width=3, fill_color=RED,
                       fill_opacity=0.3).move_to([-5.975, pipe_y, 0])
    flow = arr([-5.5, pipe_y, 0], [-6.5, pipe_y, 0], RED, w=7, tip=0.2)
    drain = VGroup(pipe_d, flow)
    drain_label = T("the drain", 26, RED).move_to([-5.9, lab_y, 0])
    return dict(trough=trough, slices=slices, tap=tap, tap_label=tap_label, drain=drain, drain_label=drain_label,
                pipe_d=pipe_d, pipe_t=pipe_t, flow=flow, py=pipe_y, ly=lab_y)


def plug_block(b):
    return Rectangle(width=0.3, height=0.8, stroke_color=RED, stroke_width=3, fill_color=RED,
                     fill_opacity=1).move_to([-5.42, b["py"], 0])


def drain_chip(b, text="no Cyp26a1", color=RED):
    c = chip(text, color, 28).move_to([-5.15, b["ly"] - 0.35, 0])
    link = Line([-6.0, b["py"] - 0.17, 0], [-6.0, c.get_top()[1], 0], color=color, stroke_width=3)
    return c, link


def tap_chip(b, text="no Raldh2", color=GREEN):
    c = chip(text, color, 30).move_to([4.0, b["py"], 0])
    link = Line([5.4, b["py"], 0], [c.get_right()[0], b["py"], 0], color=color, stroke_width=4)
    return c, link


def think_ring(x=6.0, y=-0.6):
    ring = Circle(radius=0.5, color=GOLD, stroke_width=6).move_to([x, y, 0])
    back = Circle(radius=0.5, color=GREY, stroke_width=2).move_to([x, y, 0]).set_opacity(0.4)
    lab = T("think", 28, GOLD).next_to(back, DOWN, buff=0.2)
    return ring, back, lab


def ident_key(y=-3.25):
    lab = T("colour = Hox code (schematic)", 26, LG)
    sw = VGroup(*[Square(0.34, stroke_width=0, fill_color=c, fill_opacity=0.95) for c in IDENT]).arrange(RIGHT, buff=0.05)
    g = VGroup(lab, sw).arrange(RIGHT, buff=0.35).move_to([0, y, 0])
    return g


# ---- gene rows (the lesson's table: Hoxa2 r2-r7, Hoxb2 r3-r7, Hoxb1 strong in r4) -----------------------
GENES = [("Hoxa2", 1, 2, 7), ("Hoxb2", 1, 3, 7), ("Hoxb1", 0, 4, 4)]


# ======================================================================================================
class S00Title(TitleCard):
    LESSON = "Head to Tail: Hox Genes, Retinoic Acid and Rhombomeres"
    TITLE = "A Tap at the Back, a Drain at the Front"


class S01Q(SpokenScene):
    def construct(self):
        bs, labs, tb, cord = strip(y=2.55, h=1.5)
        ys = [0.85, -0.05, -0.95]
        bars, qs, names = VGroup(), VGroup(), VGroup()
        for (nm, g, a, b), y in zip(GENES, ys):
            x0, x1 = ex(a), SX[b - 1] + 0.65
            bars.add(bar(x0, y, HOX[g], h=0.62, x_back=x1))
            q = T("?", 56, HOX[g], weight=BOLD).move_to([x0 - 0.32, y - 0.02, 0])
            qs.add(q)
            names.add(T(nm, 28, HOX[g]).next_to(q, LEFT, buff=0.18))
        code = T("Hox gene domains: where does each front edge sit?", 30, LG).move_to([0, -1.95, 0])
        sig = chip("a signal made from vitamin A", ORANGE, 40).move_to([0, -3.0, 0])
        self.play(FadeIn(bs), FadeIn(labs), FadeIn(tb), FadeIn(cord), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(b, RIGHT) for b in bars], lag_ratio=0.12), FadeIn(names), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(q, scale=1.5) for q in qs], lag_ratio=0.1), run_time=0.5)
        self.at("front edges")
        self.play(*[Indicate(q, color=GOLD, scale_factor=1.3) for q in qs], run_time=0.7)
        self.at("hox code")
        self.play(FadeIn(code), run_time=0.4)
        self.at("signal made")
        self.play(FadeIn(sig, shift=UP * 0.2), run_time=0.7)
        self.finish()


CHAIN_Y = 0.75


def make_chain():
    rol = chip("retinol", GREY, 38)
    ral = chip("retinaldehyde", GREY, 38)
    ra = chip("retinoic acid", ORANGE, 38)
    ral.move_to([0, CHAIN_Y, 0])
    rol.move_to([ral.get_left()[0] - 1.6 - rol.width / 2, CHAIN_Y, 0])
    ra.move_to([ral.get_right()[0] + 1.6 + ra.width / 2, CHAIN_Y, 0])
    dx = -(rol.get_left()[0] + ra.get_right()[0]) / 2
    for m in (rol, ral, ra):
        m.shift(RIGHT * dx)
    a1 = arr(rol.get_right() + RIGHT * 0.05, ral.get_left() + LEFT * 0.05, w=8, tip=0.28)
    a2 = arr(ral.get_right() + RIGHT * 0.05, ra.get_left() + LEFT * 0.05, w=8, tip=0.28)
    ox1 = T("oxidation", 26, LG).move_to([a1.get_center()[0], CHAIN_Y - 0.75, 0])
    ox2 = T("oxidation", 26, LG).move_to([a2.get_center()[0], CHAIN_Y - 0.75, 0])
    vit = T("vitamin A", 32, LG).move_to([rol.get_center()[0] - 0.3, CHAIN_Y - 1.2, 0])
    return rol, ral, ra, a1, a2, ox1, ox2, vit


class S02Make(SpokenScene):
    def construct(self):
        rol, ral, ra, a1, a2, ox1, ox2, vit = make_chain()
        raldh = chip("Raldh2", GREEN, 40).move_to([a2.get_center()[0], CHAIN_Y + 1.7, 0])
        conn = Line(raldh.get_bottom(), a2.get_center() + UP * 0.12, color=GREEN, stroke_width=5)
        rol_home, vit_home = rol.get_center().copy(), vit.get_center().copy()
        rol.move_to([0, CHAIN_Y, 0]).scale(1.3)
        vit.move_to([0, CHAIN_Y - 1.0, 0])
        self.play(FadeIn(rol, shift=RIGHT * 0.2), run_time=0.5)
        self.at("vitamin a")
        self.play(FadeIn(vit), run_time=0.4)
        self.at("in two steps")
        self.play(rol.animate.scale(1 / 1.3).move_to(rol_home), vit.animate.move_to(vit_home), run_time=0.4)
        self.play(GrowArrow(a1), FadeIn(ox1), run_time=0.5)
        self.play(FadeIn(ral, shift=RIGHT * 0.2), run_time=0.3)
        self.play(GrowArrow(a2), FadeIn(ox2), FadeIn(ra, shift=RIGHT * 0.2), run_time=0.6)
        self.at("main enzyme")
        self.play(FadeIn(raldh, shift=DOWN * 0.2), Create(conn), run_time=0.6)
        self.at("last step")
        self.play(Indicate(a2, color=GREEN, scale_factor=1.15), run_time=0.7)
        # the body axis arrives; the chain shrinks to the bottom, the enzyme goes to the tissue that makes it
        bs, labs, tb, cord = strip(y=2.45, h=1.3)
        band = Rectangle(width=6.8, height=1.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                         fill_opacity=0.14).move_to([3.35, 0.95, 0])
        mlab = T("mesoderm", 34, GREEN).move_to([1.55, 0.95, 0])
        chain = VGroup(rol, ral, ra, a1, a2, ox1, ox2, vit)
        self.at("is made in")
        self.play(FadeOut(conn),
                  chain.animate.scale(0.8).move_to([0, -2.1, 0]),
                  raldh.animate.move_to([4.75, 0.95, 0]),
                  FadeIn(bs), FadeIn(labs), FadeIn(tb), FadeIn(cord), FadeIn(band), run_time=0.9)
        self.at("mesoderm")
        self.play(FadeIn(mlab), band.animate.set_fill(GREEN, 0.4).set_stroke(GREEN, 5), run_time=0.6)
        hind = T("posterior hindbrain", 28, GREEN).move_to([2.0, 3.5, 0])
        self.at("posterior hindbrain")
        self.play(*[bs[i].animate.set_stroke(GREEN, 5) for i in (4, 5, 6)], FadeIn(hind), run_time=0.6)
        self.at("spinal cord")
        self.play(tb.animate.set_stroke(GREEN, 5), cord.animate.set_color(GREEN), run_time=0.6)
        tap = T("= the tap", 34, GREEN, weight=BOLD).move_to([3.6, -0.55, 0])
        self.play(FadeIn(tap, shift=UP * 0.15), run_time=0.5)
        self.finish()


PLATE_Y = 0.55


class S03Cyp(SpokenScene):
    def construct(self):
        plate = RoundedRectangle(corner_radius=0.6, width=12.8, height=2.5, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.12).move_to([0, PLATE_Y, 0])
        plate_l = T("neural plate", 28, LG).move_to([4.2, PLATE_Y + 0.8, 0])
        band = Rectangle(width=5.8, height=1.3, stroke_color=GREEN, stroke_width=4, fill_color=GREEN,
                         fill_opacity=0.35).move_to([3.5, -1.85, 0])
        mlab = T("mesoderm", 30, GREEN).move_to([1.95, -1.85, 0])
        raldh = chip("Raldh2", GREEN, 32).move_to([4.9, -1.85, 0])
        red = RoundedRectangle(corner_radius=0.6, width=4.7, height=2.5, stroke_color=RED, stroke_width=3,
                               fill_color=RED, fill_opacity=0.0).move_to([-4.05, PLATE_Y, 0])
        cy26 = chip("Cyp26a1", RED, 42).move_to([-4.05, PLATE_Y, 0])
        dots = VGroup(*[drop(0.2).move_to([x, PLATE_Y - 0.15, 0]) for x in (3.0, 2.0, 1.0, 0.0, -1.0)])
        dlab = T("retinoic acid", 28, ORANGE).move_to([1.0, PLATE_Y + 0.75, 0])
        self.play(FadeIn(plate), FadeIn(band), FadeIn(mlab), FadeIn(raldh), FadeIn(plate_l), run_time=0.4)
        self.play(FadeIn(dots, scale=0.6), FadeIn(dlab), FadeIn(red), FadeIn(cy26, shift=RIGHT * 0.2), run_time=0.5)
        self.at("destroy")
        goals = [(-2.6, 0.7), (-2.3, 0.25), (-2.55, -0.2), (-2.2, -0.65), (-2.8, -0.75)]
        self.play(FadeOut(dlab), red.animate.set_fill(RED, 0.3),
                  *[d.animate.move_to([gx, PLATE_Y + gy, 0]) for d, (gx, gy) in zip(dots, goals)], run_time=1.0)
        self.play(*[d.animate.scale(0.05).set_opacity(0) for d in dots], run_time=0.5)
        self.at("cyp26", nth=1)
        self.play(Indicate(cy26, color=RED, scale_factor=1.12), run_time=0.4)
        self.at("is strong toward")
        self.play(red.animate.set_fill(RED, 0.5).set_stroke(RED, 6), run_time=0.7)
        plate_txt = T("front of the neural plate", 30, RED, weight=BOLD).move_to([-4.05, PLATE_Y + 1.15 + 0.5, 0])
        self.at("front of the neural")
        self.play(FadeIn(plate_txt, shift=DOWN * 0.15), Indicate(cy26, color=RED, scale_factor=1.08), run_time=0.7)
        self.finish()


def thin_bath_top(y=3.05, h=1.2, k=1.0):
    return bath2(y, h, k=k)


class S04Bath(SpokenScene):
    def construct(self):
        b = bath2(0.55, 3.4, dye=False)
        self.at("bath")
        self.play(FadeIn(b["trough"]), run_time=0.6)
        self.at("tap at the back")
        self.play(FadeIn(b["tap"], shift=LEFT * 0.3), FadeIn(b["tap_label"]), run_time=0.5)
        self.at("drain at the front")
        self.play(FadeIn(b["drain"], shift=RIGHT * 0.3), FadeIn(b["drain_label"]), run_time=0.5)
        self.add(b["slices"])
        dye = VGroup(T("like dye in the water,", 30, TEXT), T("not the water level, which evens out", 30, TEXT)
                     ).arrange(DOWN, buff=0.15).move_to([0, -2.55, 0])
        self.play(LaggedStart(*[s.animate.set_fill(ORANGE, dye_op(s.get_center()[0])) for s in reversed(list(b["slices"]))],
                              lag_ratio=0.02), FadeIn(dye, run_time=0.9), run_time=1.0)
        # the bath thins to a strip at the top; the concentration curve rises beneath it
        pb, ph = -3.0, 4.6
        thin = bath2(3.05, 1.2)
        big = VGroup(b["trough"], b["slices"], b["tap"], b["tap_label"], b["drain"], b["drain_label"])
        small = VGroup(thin["trough"], thin["slices"], thin["tap"], thin["tap_label"], thin["drain"], thin["drain_label"])
        plot = plot_build(pb, ph)
        self.at("retinoic acid ends")
        self.play(FadeOut(dye), Transform(big, small), run_time=0.9)
        self.play(Create(plot[2]), Create(plot[3]), FadeIn(plot[4]), FadeIn(plot[5]), FadeIn(plot[6]), run_time=0.5)
        sch = T("schematic, not a measured profile", 28, LG).move_to([-1.2, 0.35, 0])
        xb = 4.75
        hi = Circle(radius=0.3, color=ORANGE, stroke_width=5).move_to([xb, cyv(pb, ph, conc(xb)), 0])
        hi_l = T("high", 32, ORANGE, weight=BOLD).move_to([xb - 1.0, cyv(pb, ph, conc(xb)) + 0.75, 0])
        xf = -4.9
        lo = Circle(radius=0.3, color=ORANGE, stroke_width=5).move_to([xf, cyv(pb, ph, conc(xf)), 0])
        lo_l = T("low", 32, ORANGE, weight=BOLD).move_to([xf + 0.05, cyv(pb, ph, conc(xf)) + 0.75, 0])
        self.at("high at the back")
        self.play(Create(plot[1]), FadeIn(plot[0]), FadeIn(sch), run_time=0.7)
        self.play(Create(hi), FadeIn(hi_l), run_time=0.3)
        self.at("low at the front")
        self.play(Create(lo), FadeIn(lo_l), run_time=0.5)
        self.finish()


# ---- the nucleus scenes --------------------------------------------------------------------------------
NUC_C = np.array([0.0, -0.5, 0.0])
DNA_Y = -2.3
PAIR_X = 0.9


def nucleus_parts():
    nuc = Ellipse(width=13.4, height=6.4, stroke_color=LG, stroke_width=4, fill_color=GREY,
                  fill_opacity=0.07).move_to(NUC_C)
    nlab = T("nucleus", 38, TEXT, weight=BOLD).move_to([0, 2.15, 0])
    return nuc, nlab


def pair_chips():
    rar = chip("RAR", BLUE, 56)
    rxr = chip("RXR", BLUE, 56)
    rxr.next_to(rar, RIGHT, buff=0.05)
    grp = VGroup(rar, rxr)
    return rar, rxr, grp


def ra_badge(rar):
    d = drop(0.3).move_to(rar.get_top() + UP * 0.28)
    lab = T("retinoic acid", 28, ORANGE).next_to(d, LEFT, buff=0.15)
    return VGroup(d, lab)


class S05Rar(SpokenScene):
    def construct(self):
        nuc, nlab = nucleus_parts()
        self.play(FadeIn(nuc), FadeIn(nlab), run_time=0.4)
        ra_blob = drop(0.32).move_to([-5.9, 3.2, 0])
        ra_lab = T("retinoic acid", 28, ORANGE).next_to(ra_blob, RIGHT, buff=0.2)
        self.play(FadeIn(ra_blob, scale=1.3), FadeIn(ra_lab), run_time=0.4)
        rar, rxr_unused, _ = pair_chips()
        rar.move_to([-2.4, -0.2, 0])
        self.at("binds the retinoic")
        self.play(FadeIn(rar, scale=1.2), ra_blob.animate.move_to([-2.4, 0.65, 0]), FadeOut(ra_lab), run_time=1.0)
        lab_in = T("retinoic acid", 28, ORANGE).next_to(ra_blob, LEFT, buff=0.15)
        self.play(FadeIn(lab_in), run_time=0.3)
        self.at("rar")
        self.play(Indicate(rar, color=BLUE, scale_factor=1.12), run_time=0.7)
        rxr = chip("RXR", BLUE, 56).move_to([4.4, -0.2, 0])
        self.at("pairs with")
        self.play(FadeIn(rxr, shift=LEFT * 0.2), run_time=0.4)
        self.play(rxr.animate.next_to(rar, RIGHT, buff=0.05), run_time=0.8)
        self.at("rxr")
        self.play(Indicate(rxr, color=BLUE, scale_factor=1.12), run_time=0.7)
        dna = Line([-5.5, DNA_Y, 0], [5.5, DNA_Y, 0], color=LG, stroke_width=8)
        elem = Rectangle(width=1.9, height=0.5, stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                         fill_opacity=0.95).move_to([PAIR_X, DNA_Y, 0])
        self.at("short dna")
        self.play(Create(dna), run_time=0.5)
        self.play(FadeIn(elem, scale=1.3), run_time=0.4)
        pair = VGroup(ra_blob, lab_in, rar, rxr)
        self.at("called")
        delta = np.array([PAIR_X, DNA_Y + 1.0, 0]) - VGroup(rar, rxr).get_center()
        self.play(pair.animate.shift(delta), run_time=0.8)
        dock = Line([PAIR_X, DNA_Y + 1.0 - rar.height / 2, 0], [PAIR_X, DNA_Y + 0.25, 0], color=GOLD, stroke_width=6)
        self.play(Create(dock), run_time=0.3)
        rel = T("response element", 34, GOLD, weight=BOLD).move_to([PAIR_X, DNA_Y - 0.7, 0])
        self.at("elements")
        self.play(FadeIn(rel), run_time=0.5)
        self.finish()


def strand(y, ex_x, gene, gx, half=5.5):
    dna = Line([-half, y, 0], [half, y, 0], color=LG, stroke_width=8)
    elem = Rectangle(width=1.9, height=0.5, stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                     fill_opacity=0.95).move_to([ex_x, y, 0])
    gc = chip(gene, PURPLE, 38)
    gbg = RoundedRectangle(corner_radius=0.14, width=gc[0].width, height=gc[0].height, stroke_width=0,
                           fill_color=BG, fill_opacity=1).move_to([gx, y, 0])
    gc.move_to([gx, y, 0])
    rel = T("response element", 30, GOLD).move_to([ex_x, y - 0.65, 0])
    return dna, elem, gbg, gc, rel


class S06Rare(SpokenScene):
    def construct(self):
        nuc, nlab = nucleus_parts()
        # carried from s05: the pair docked on the response element of the lower strand
        dna, elem, gbg, gc, rel = strand(DNA_Y, PAIR_X, "Hoxb1", 3.9)
        rar, rxr, grp = pair_chips()
        pair = VGroup(ra_badge(rar), rar, rxr)
        pair.shift(np.array([PAIR_X, DNA_Y + 1.0, 0]) - grp.get_center())
        dock = Line([PAIR_X, DNA_Y + 1.0 - rar.height / 2, 0], [PAIR_X, DNA_Y + 0.25, 0], color=GOLD, stroke_width=6)
        rel_old = T("response element", 34, GOLD, weight=BOLD).move_to([PAIR_X, DNA_Y - 0.7, 0])
        self.add(nuc, nlab, dna, elem, dock, pair, rel_old)
        # strand A (Hoxa1) is a separate gene on a separate strand
        dna2, elem2, gbg2, gc2, rel2 = strand(1.15, -0.9, "Hoxa1", 2.9, half=4.3)
        self.at("hoxa1")
        self.play(FadeIn(dna2), FadeIn(elem2),
                  FadeIn(gbg2), FadeIn(gc2), FadeIn(rel2), run_time=0.7)
        self.at("hoxb1")
        self.play(FadeOut(rel_old), FadeIn(gbg), FadeIn(gc), FadeIn(rel), run_time=0.6)
        self.add(gc)
        self.at("carry these")
        self.play(Indicate(elem2, color=GOLD, scale_factor=1.2), Indicate(elem, color=GOLD, scale_factor=1.2), run_time=0.9)
        # to the dose picture
        pb, ph = -3.0, 5.2
        plot = plot_build(pb, ph, thr=True)
        cult = T("cell culture · illustration", 36, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        self.at("in cell culture")
        self.play(FadeOut(VGroup(nuc, nlab, dna, elem, dock, pair, rel, gbg, gc, dna2, elem2, gbg2, gc2, rel2)),
                  FadeIn(VGroup(plot[0], plot[1], plot[2], plot[3], plot[4], plot[5], plot[6])), run_time=0.7)
        self.play(FadeIn(cult), run_time=0.4)
        self.at("3' hox")
        self.play(plot[7].animate.set_opacity(1), run_time=0.5)
        self.at("genes respond")
        self.play(plot[8].animate.set_opacity(1), run_time=0.4)
        self.at("5' genes")
        self.play(plot[9].animate.set_opacity(1), run_time=0.5)
        self.play(plot[10].animate.set_opacity(1), run_time=0.4)
        self.finish()


# model bars: 3' on top, 5' below (so that the edge lines never cross a bar)
MB3, MB5 = 2.35, 1.65


def model_gene_bars(y3=MB3, y5=MB5, x3=None, x5=None, labels=True):
    x3 = ex(4) if x3 is None else x3
    x5 = ex(7) if x5 is None else x5
    b3, b5 = bar(x3, y3, HOX[0], h=0.5), bar(x5, y5, HOX[3], h=0.5)
    l3 = T("3′ gene", 28, HOX[0]).move_to([BACKX + 1.05, y3, 0])
    l5 = T("5′ gene", 28, HOX[2]).move_to([BACKX + 1.05, y5, 0])
    return b3, l3, b5, l5


class S07Front(SpokenScene):
    def construct(self):
        # s06's plot, as it ended, then resized to leave room for the row and the gene bars
        pb0, ph0 = -3.0, 5.2
        pb, ph = -2.9, 3.9
        old = plot_build(pb0, ph0, thr=True)
        cult = T("cell culture · illustration", 36, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        self.add(old, cult)
        new = plot_build(pb, ph, thr=True)
        bs, labs, tb, cord = strip()
        b3, l3, b5, l5 = model_gene_bars()
        model = VGroup(T("simple threshold model", 26, TEXT), T("an illustration", 26, TEXT)).arrange(DOWN, buff=0.12).move_to([-3.55, 0.6, 0])
        self.at("threshold model")
        self.play(Transform(old, new), FadeOut(cult), FadeIn(bs), FadeIn(labs), FadeIn(tb), FadeIn(cord), run_time=0.9)
        self.play(FadeIn(model), run_time=0.4)
        x3, x5 = ex(4), ex(7)
        d3 = DashedLine([x3, cyv(pb, ph, T3), 0], [x3, MB3 - 0.28, 0], color=HOX[0], stroke_width=3)
        d5 = DashedLine([x5, cyv(pb, ph, T5), 0], [x5, MB5 - 0.28, 0], color=HOX[3], stroke_width=3)
        dots = VGroup(Dot([x3, cyv(pb, ph, T3), 0], radius=0.11, color=TEXT),
                      Dot([x5, cyv(pb, ph, T5), 0], radius=0.11, color=TEXT))
        self.play(FadeIn(dots, scale=1.5), run_time=0.3)
        self.at("fewer hox genes")
        self.play(Create(d3), Create(d5), GrowFromEdge(b5, RIGHT), FadeIn(l5), GrowFromEdge(b3, RIGHT), FadeIn(l3),
                  run_time=0.9)
        nohox = T("no Hox expression here", 28, GOLD).move_to([-3.6, 2.0, 0])
        self.at("toward the front")
        self.play(*[bs[i].animate.set_stroke(GOLD, 5) for i in (0, 1, 2)], FadeIn(nohox), run_time=0.6)
        xr = -4.9
        ring = Circle(radius=0.35, color=ORANGE, stroke_width=5).move_to([xr, cyv(pb, ph, conc(xr)), 0])
        self.at("signal is lower")
        self.play(Create(ring), run_time=0.5)
        self.finish()


# ---- prediction 1 ---------------------------------------------------------------------------------------
P_B3, P_B5 = 0.3, -0.5
BATH_P = (1.95, 1.2)


def predict_state(scene, extra=False):
    bs, labs, tb, cord = strip()
    b = bath2(BATH_P[0], BATH_P[1], k=(2.4 if extra else 1.0))
    b3, l3, b5, l5 = model_gene_bars(y3=P_B3, y5=P_B5)
    x3, x5 = ex(4), ex(7)
    marks = VGroup(DashedLine([x3, P_B3 - 0.28, 0], [x3, -0.95, 0], color=HOX[0], stroke_width=3),
                   DashedLine([x5, P_B5 - 0.28, 0], [x5, -0.95, 0], color=HOX[3], stroke_width=3))
    arrows = VGroup(*[DoubleArrow([x - 1.2, -1.25, 0], [x + 1.2, -1.25, 0], color=GOLD, stroke_width=6, tip_length=0.25,
                                  buff=0) for x in (x3, x5)])
    qs = VGroup(*[T("?", 40, GOLD, weight=BOLD).move_to([x, -1.8, 0]) for x in (x3, x5)])
    c1 = chip("mouse embryos", TEXT, 30)
    c2 = chip("extra retinoic acid", ORANGE, 30)
    c3 = chip("early stage", TEXT, 30)
    chips = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.45).move_to([-0.2, -2.6, 0])
    q = T("Which way do the Hox edges move?", 38, TEXT, weight=BOLD).move_to([0, -3.42, 0])
    return dict(bs=bs, labs=labs, tb=tb, cord=cord, b=b, b3=b3, l3=l3, b5=b5, l5=l5, marks=marks, arrows=arrows,
                qs=qs, c1=c1, c2=c2, c3=c3, q=q)


class S08Predict(SpokenScene):
    def construct(self):
        f = predict_state(self)
        b = f["b"]
        self.add(f["bs"], f["labs"], f["tb"], f["cord"], b["trough"], b["slices"], b["tap"], b["tap_label"], b["drain"],
                 b["drain_label"], f["b3"], f["l3"], f["b5"], f["l5"])
        tag = T("Predict", 48, GOLD, weight=BOLD).move_to([0, -1.6, 0])
        self.play(FadeIn(tag), run_time=0.3)
        self.at("give mouse embryos")
        self.play(FadeIn(f["c1"], shift=UP * 0.2), run_time=0.4)
        self.at("extra retinoic acid")
        self.play(FadeIn(f["c2"], shift=UP * 0.2), b["pipe_t"].animate.set_stroke(ORANGE, 5).set_fill(ORANGE, 0.5),
                  *[s.animate.set_fill(ORANGE, dye_op(s.get_center()[0], 2.4)) for s in b["slices"]], run_time=1.3)
        self.at("early stage")
        self.play(FadeIn(f["c3"], shift=UP * 0.2), run_time=0.4)
        self.at("which way")
        self.play(FadeOut(tag), Create(f["marks"]), run_time=0.4)
        self.play(FadeIn(f["arrows"], scale=0.8), FadeIn(f["qs"]), run_time=0.5)
        self.at("edges move")
        self.play(FadeIn(f["q"], shift=UP * 0.15), run_time=0.5)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        f = predict_state(self, extra=True)
        b = f["b"]
        b["pipe_t"].set_stroke(ORANGE, 5).set_fill(ORANGE, 0.5)
        self.add(f["bs"], f["labs"], f["tb"], f["cord"], b["trough"], b["slices"], b["tap"], b["tap_label"], b["drain"],
                 b["drain_label"], f["b3"], f["l3"], f["b5"], f["l5"], f["marks"], f["arrows"], f["qs"],
                 f["c1"], f["c2"], f["c3"], f["q"])
        ring, back, lab = think_ring(6.1, -2.45)
        self.add(back, lab)
        self.play(Create(ring), run_time=self.narration_s - 0.25, rate_func=linear)
        self.finish()


# ---- reveal 1: forward ---------------------------------------------------------------------------------
RV_B3, RV_B5 = 1.55, 0.8


def credit_line(y=-1.75):
    c1 = T("1992", 34, GOLD, weight=BOLD)
    c2 = T("Marshall, Krumlauf, Lumsden and colleagues", 30, TEXT)
    return VGroup(c1, c2).arrange(RIGHT, buff=0.3).move_to([0, y, 0]), c1, c2


class S10Reveal(SpokenScene):
    def construct(self):
        bs, labs, tb, cord = strip(y=2.95, h=1.4, fills=IDENT)
        b3, l3, b5, l5 = model_gene_bars(y3=RV_B3, y5=RV_B5)
        card, c1, c2 = credit_line(-1.75)
        key = ident_key(-3.2)
        new = bar(ex(2), RV_B3, HOX[0], h=0.5)
        ghost = DashedLine([ex(4), RV_B3 - 0.3, 0], [ex(4), RV_B3 + 0.3, 0], color=TEXT, stroke_width=3)
        fwd = T("forward", 56, ORANGE, weight=BOLD)
        arrow = arr([0, 0, 0], [-3.0, 0, 0], ORANGE, w=10, tip=0.32)
        fa = VGroup(arrow, fwd).arrange(RIGHT, buff=0.35).move_to([0, -0.3, 0])
        self.add(bs, labs, tb, cord, b3, l3, b5, l5, card, key)
        self.play(FadeIn(ghost), b5.animate.set_opacity(0.25), l5.animate.set_opacity(0.3), run_time=0.4)
        self.play(FadeIn(fwd), GrowArrow(arrow), Transform(b3, new), run_time=1.3)
        self.at("domains changed")
        self.play(Indicate(b3, color=PURPLE, scale_factor=1.05), run_time=0.7)
        self.finish()


class S11Reveal2(SpokenScene):
    def construct(self):
        bs, labs, tb, cord = strip(y=2.95, h=1.4, fills=IDENT)
        b3, l3, b5, l5 = model_gene_bars(y3=RV_B3, y5=RV_B5, x3=ex(2))
        b5.set_opacity(0.25)
        l5.set_opacity(0.3)
        key = ident_key(-3.2)
        fwd = T("forward", 56, ORANGE, weight=BOLD)
        arrow = arr([0, 0, 0], [-3.0, 0, 0], ORANGE, w=10, tip=0.32)
        fa = VGroup(arrow, fwd).arrange(RIGHT, buff=0.35).move_to([0, -0.3, 0])
        self.add(bs, labs, tb, cord, b3, l3, b5, l5, fa, key)
        # the row grows; the bars and the arrow make way for the identity change
        big_y, big_h = 0.95, 2.4
        nbs, nlabs, ntb, ncord = strip(y=big_y, h=big_h, fills=IDENT)
        self.play(FadeOut(VGroup(b3, l3, b5, l5, fa)),
                  Transform(bs, nbs), Transform(labs, nlabs), Transform(tb, ntb), Transform(cord, ncord), run_time=0.9)
        # arrows: the identity of 4 and 5 copied toward 2 and 3, one above the row and one below it
        top_y = big_y + big_h / 2 + 0.12
        bot_y = big_y - big_h / 2 - 0.12
        a1 = CurvedArrow([SX[3], top_y, 0], [SX[1], top_y, 0], color=PURPLE, stroke_width=6, angle=TAU / 5)
        a2 = CurvedArrow([SX[4], bot_y, 0], [SX[2], bot_y, 0], color=PURPLE, stroke_width=6, angle=-TAU / 5)
        mix = lambda i, j: interpolate_color(ManimColor(IDENT[i]), ManimColor(IDENT[j]), 0.7)
        self.at("shifted toward")
        self.play(Create(a1), Create(a2), run_time=0.8)
        self.at("identity of")
        self.play(bs[1].animate.set_fill(mix(1, 3), 0.85), labs[1].animate.set_color(lab_color(mix(1, 3).to_hex())),
                  run_time=0.7)
        self.at("and 5")
        self.play(bs[2].animate.set_fill(mix(2, 4), 0.85), labs[2].animate.set_color(lab_color(mix(2, 4).to_hex())),
                  run_time=0.7)
        cap = T("too much shows a response, not the normal role", 34, TEXT).move_to([0, -2.3, 0])
        self.at("too much signal")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---- prediction 2 and its answers: the big bath ---------------------------------------------------------
BIG = (0.45, 3.5)


def big_state(scene, k=1.0, dye=True, ident=IDENT):
    bs, labs, tb, cord = strip(fills=ident)
    b = bath2(BIG[0], BIG[1], k=k, dye=dye)
    scene.add(bs, labs, tb, cord, b["trough"], b["slices"], b["tap"], b["tap_label"], b["drain"], b["drain_label"])
    return bs, labs, tb, cord, b


class S12Predict2(SpokenScene):
    def construct(self):
        bs, labs, tb, cord, b = big_state(self)
        tag = T("Predict", 48, GOLD, weight=BOLD).move_to([1.0, -2.65, 0])
        self.add(tag)
        plug = plug_block(b)
        chp, link = drain_chip(b)
        self.at("block the drain")
        self.play(FadeIn(plug, scale=2.0), b["flow"].animate.set_opacity(0.0), run_time=0.7)
        self.at("mice lacking")
        self.play(FadeOut(b["drain_label"]), FadeIn(chp, shift=UP * 0.2), Create(link), run_time=0.5)
        self.at("clear less")
        self.play(Indicate(plug, color=RED, scale_factor=1.5), run_time=0.7)
        q = T("What changes?", 48, TEXT, weight=BOLD).move_to([1.0, -2.65, 0])
        self.at("what changes")
        self.play(Transform(tag, q), run_time=0.5)
        self.finish()


def plugged_state(scene, k=1.0, with_q=True, ident=IDENT):
    bs, labs, tb, cord, b = big_state(scene, k=k, ident=ident)
    plug = plug_block(b)
    chp, link = drain_chip(b)
    b["flow"].set_opacity(0.0)
    scene.remove(b["drain_label"])
    scene.add(plug, chp, link)
    if with_q:
        scene.add(T("What changes?", 48, TEXT, weight=BOLD).move_to([1.0, -2.65, 0]))
    return bs, labs, tb, cord, b


class S13Pause(NarratedScene):
    def construct(self):
        plugged_state(self)
        ring, back, lab = think_ring(5.6, -2.55)
        self.add(back, lab)
        self.play(Create(ring), run_time=self.narration_s - 0.25, rate_func=linear)
        self.finish()


class S14Reveal3(SpokenScene):
    def construct(self):
        bs, labs, tb, cord, b = plugged_state(self, with_q=False)
        ko = T("mouse Cyp26a1 knockout", 26, LG)
        cred = T("Abu-Abed and colleagues, 2001", 26, GOLD)
        dot = T("·", 26, LG)
        line = VGroup(ko, dot, cred).arrange(RIGHT, buff=0.3).move_to([0, -3.4, 0])
        self.add(ko)
        k = 2.4
        self.at("front shifts")
        self.play(*[s.animate.set_fill(ORANGE, dye_op(s.get_center()[0], k)) for s in b["slices"]], run_time=1.4)
        mix = lambda i: interpolate_color(ManimColor(IDENT[i]), ManimColor(IDENT[i + 1]), 0.6)
        self.at("partly transformed")
        self.play(*[bs[i].animate.set_fill(mix(i), 0.95).set_stroke(TEXT, 4) for i in (0, 1, 2)],
                  *[labs[i].animate.set_color(lab_color(mix(i).to_hex())) for i in (0, 1, 2)], run_time=1.0)
        cap = T("front of the hindbrain: partly posterior-like", 32, TEXT).move_to([0.8, -2.65, 0])
        self.at("toward a more posterior")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
        self.at("character")
        self.play(FadeIn(dot), FadeIn(cred), run_time=0.5)
        self.finish()


PATCH = [0.42, 0.66, 0.5, 0.32]
PALE = "#C7A8EE"


def patchy(bs, labs):
    """r4 to r7 poorly patterned: pale, uneven fills with dashed outlines, labels kept."""
    anims = []
    for n, i in enumerate(range(3, 7)):
        anims.append(bs[i].animate.set_fill(PALE, PATCH[n]).set_stroke(LG, 2))
        anims.append(labs[i].animate.set_color(LG))
    return anims


class S15Raldh(SpokenScene):
    def construct(self):
        bs, labs, tb, cord, b = big_state(self)
        cross = Cross(b["tap"], stroke_color=GREEN, stroke_width=8).scale(1.1)
        chp, link = tap_chip(b)
        self.at("remove the tap")
        self.play(Create(cross), run_time=0.5)
        self.play(FadeOut(VGroup(b["tap"], cross)),
                  *[s.animate.set_fill(ORANGE, 0.04) for s in b["slices"]], run_time=1.0)
        self.at("mice lacking")
        self.play(FadeOut(b["tap_label"]), FadeIn(chp, shift=UP * 0.2), Create(link), run_time=0.6)
        cap = T("posterior hindbrain: poorly patterned", 34, TEXT).move_to([0, -2.65, 0])
        self.at("posterior hindbrain")
        self.play(*patchy(bs, labs), FadeIn(cap, shift=UP * 0.15), run_time=1.0)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        bs, labs, tb, cord, b = big_state(self, dye=True)
        for s in b["slices"]:
            s.set_fill(ORANGE, 0.04)
        for i in range(3, 7):
            bs[i].set_fill(PALE, PATCH[i - 3]).set_stroke(LG, 2)
            labs[i].set_color(LG)
        self.remove(b["tap"], b["tap_label"])
        chp, link = tap_chip(b)
        cap = T("posterior hindbrain: poorly patterned", 34, TEXT).move_to([0, -2.65, 0])
        self.add(chp, link, cap)
        self.finish()


# ---- the limit and the order --------------------------------------------------------------------------
class S17Limit(SpokenScene):
    def construct(self):
        y = 2.2
        line = Line([-5.0, y, 0], [5.0, y, 0], color=LG, stroke_width=6)
        xs = [-3.6, -1.2, 1.2, 3.6]
        blocks = VGroup(*[Square(1.0, stroke_color=HOX[j], stroke_width=3, fill_color=HOX[j], fill_opacity=0.9).move_to([x, y, 0])
                          for j, x in enumerate(xs)])
        cl = T("Hox cluster", 40, TEXT, weight=BOLD).move_to([0, y + 1.0, 0])
        e3 = T("3′ (head side)", 30, LG).move_to([-4.3, y - 1.0, 0])
        e5 = T("5′ (tail side)", 30, LG).move_to([4.3, y - 1.0, 0])
        # the exact-edges row is there from the start
        sy = -1.7
        bs, labs, tb, cord = strip(y=sy, h=0.85)
        qxs = [ex(2), ex(3), ex(4)]
        qs = VGroup(*[T("?", 40, GOLD, weight=BOLD).move_to([x, sy + 0.85, 0]) for x in qxs])
        ticks = VGroup(*[Line([x, sy - 0.45, 0], [x, sy + 0.45, 0], color=GOLD, stroke_width=5) for x in qxs])
        edl = T("exact edges", 40, LG, weight=BOLD).move_to([0, -3.15, 0])
        self.play(FadeIn(VGroup(line, blocks, cl, e3, e5)), FadeIn(bs), FadeIn(labs), FadeIn(tb), FadeIn(cord),
                  FadeIn(ticks), FadeIn(edl), run_time=0.5)
        sig = chip("retinoic acid signal", ORANGE, 32).move_to([4.4, 0.15, 0])
        direction = arr([2.0, 0.15, 0], [-4.4, 0.15, 0], PURPLE, w=10, tip=0.35)
        dl = T("direction", 40, PURPLE, weight=BOLD).move_to([-1.2, 0.8, 0])
        self.at("sets the direction")
        self.play(FadeIn(sig, shift=LEFT * 0.2), GrowArrow(direction), FadeIn(dl), run_time=0.8)
        self.at("not the exact")
        self.play(FadeIn(qs, scale=1.4), edl.animate.set_color(GOLD), run_time=0.6)
        self.finish()


def grid_rows(on_over=None):
    """The lesson's three rows, big, with the group shade. Returns cells, names, edge marks, row ys."""
    ys = [1.5, 0.55, -0.6]
    cells, names, marks, lines = VGroup(), VGroup(), VGroup(), VGroup()
    for (nm, g, a, b), y in zip(GENES, ys):
        lo, hi = (on_over[nm] if on_over and nm in on_over else (a, b))
        for k in range(2, 8):
            filled = lo <= k <= hi
            r = RoundedRectangle(corner_radius=0.1, width=1.2, height=0.8,
                                 stroke_color=(HOX[g] if filled else GREY), stroke_width=(3 if filled else 1.5),
                                 fill_color=HOX[g], fill_opacity=(0.88 if filled else 0.0)).move_to([SX[k - 1], y, 0])
            if not filled:
                r.set_stroke(opacity=0.35)
            cells.add(r)
        names.add(T(nm, 28, TEXT).move_to([SX[0], y, 0]))
        xm = ex(lo) + 0.02
        marks.add(Line([xm, y - 0.4, 0], [xm, y + 0.4, 0], color=GOLD, stroke_width=7))
        lines.add(DashedLine([xm, y - 0.46, 0], [xm, -2.0, 0], color=LG, stroke_width=2.5))
    return cells, names, marks, lines, ys


def group_labels(ys):
    br = VGroup(Line([4.55, ys[0] + 0.4, 0], [4.55, ys[1] - 0.4, 0], color=HOX[1], stroke_width=5),
                Line([4.55, ys[2] + 0.4, 0], [4.55, ys[2] - 0.4, 0], color=HOX[0], stroke_width=5))
    g2 = T("group 2", 30, HOX[1], weight=BOLD).move_to([5.65, (ys[0] + ys[1]) / 2, 0])
    g1 = T("group 1", 30, HOX[0], weight=BOLD).move_to([5.65, ys[2], 0])
    return br, g2, g1


class S18Order(SpokenScene):
    def construct(self):
        bs, labs, tb, cord = strip()
        cells, names, marks, lines, ys = grid_rows()
        br, g2, g1 = group_labels(ys)
        self.play(FadeIn(bs), FadeIn(labs), FadeIn(tb), FadeIn(cord), run_time=0.4)
        self.play(FadeIn(cells), FadeIn(names), run_time=0.5)
        self.at("group 2 genes")
        self.play(FadeIn(marks[0]), FadeIn(marks[1]), FadeIn(br[0]), FadeIn(g2),
                  Indicate(names[0], color=HOX[1]), Indicate(names[1], color=HOX[1]), run_time=0.8)
        self.at("than group 1")
        self.play(FadeIn(marks[2]), FadeIn(br[1]), FadeIn(g1), Indicate(names[2], color=HOX[0]), run_time=0.7)
        bend = T("in the hindbrain the order bends", 32, GOLD, weight=BOLD).move_to([-0.6, 2.5, 0])
        self.at("yet")
        self.play(FadeIn(bend, shift=DOWN * 0.1), run_time=0.5)
        less = T("3′ genes need less signal", 32, HOX[0], weight=BOLD).move_to([2.2, -1.3, 0])
        self.at("need less signal")
        self.play(FadeIn(less), run_time=0.5)
        oi = chip("other inputs", GREY, 36).move_to([-2.9, -3.05, 0])
        links = VGroup(*[arr(oi.get_top() + UP * 0.02, [m.get_center()[0], -2.05, 0], LG, w=5, tip=0.22) for m in marks])
        self.at("other inputs")
        self.play(FadeIn(oi, shift=UP * 0.2), run_time=0.5)
        self.at("set those edges")
        self.play(Create(lines), *[GrowArrow(a) for a in links], *[Indicate(m, color=GOLD, scale_factor=1.3) for m in marks],
                  run_time=0.9)
        self.finish()


class S19Terat(SpokenScene):
    def construct(self):
        big = chip("retinoids", ORANGE, 60).move_to([0, 1.5, 0])
        self.play(FadeIn(big, scale=0.9), run_time=0.5)
        terat = T("teratogens", 60, RED, weight=BOLD).move_to([0, 0.05, 0])
        self.at("teratogens")
        self.play(big[0].animate.set_stroke(RED), FadeIn(terat, shift=UP * 0.15), run_time=0.6)
        dfn = T("agents that cause birth defects", 40, TEXT).move_to([0, -1.3, 0])
        self.at("agents that cause")
        self.play(FadeIn(dfn), run_time=0.6)
        # on to the shifted code
        bs, labs, tb, cord = strip()
        cells, names, marks, lines, ys = grid_rows()
        br, g2, g1 = group_labels(ys)
        cap = T("teratogen: an agent that causes birth defects", 28, TEXT).move_to([0, -3.35, 0])
        mouse = T("mouse and chick", 32, LG).move_to([-0.2, 2.5, 0])
        self.at("in mouse and chick")
        self.play(FadeOut(VGroup(big, terat, dfn)), FadeIn(VGroup(bs, labs, tb, cord)), FadeIn(cells), FadeIn(names),
                  FadeIn(br), FadeIn(g2), FadeIn(g1), FadeIn(mouse), FadeIn(cap), run_time=0.8)
        extra = chip("+ extra retinoic acid, early", ORANGE, 34).move_to([0, -1.75, 0])
        self.at("acid early")
        self.play(FadeIn(extra, shift=UP * 0.2), run_time=0.5)
        # shifted rows: Hoxb2 gains r2, Hoxb1 gains r3 (one segment forward); Hoxa2 front edge is already at r1/r2
        new_cells = VGroup()
        ghosts = VGroup()
        for (nm, g, a, b), y, k in ((GENES[1], ys[1], 2), (GENES[2], ys[2], 3)):
            new_cells.add(RoundedRectangle(corner_radius=0.1, width=1.2, height=0.8, stroke_color=HOX[g], stroke_width=3,
                                           fill_color=HOX[g], fill_opacity=0.88).move_to([SX[k - 1], y, 0]))
            ghosts.add(Line([ex(a) + 0.02, y - 0.4, 0], [ex(a) + 0.02, y + 0.4, 0], color=TEXT, stroke_width=3))
        self.at("shifts the")
        self.play(FadeIn(ghosts), LaggedStart(*[FadeIn(c, shift=LEFT * 0.25) for c in new_cells], lag_ratio=0.4),
                  run_time=0.6)
        self.at("hox code")
        self.play(Indicate(new_cells, color=PURPLE, scale_factor=1.06), run_time=0.7)
        self.finish()


FACE_C = np.array([0.0, -0.75, 0.0])


def face_outline():
    f = Ellipse(width=3.8, height=4.0, stroke_color=YELLOW, stroke_width=6).move_to(FACE_C)
    lab = T("face", 40, YELLOW).move_to(FACE_C + DOWN * 0.3)
    return f, lab


def crest_paths(disturbed=False):
    """Curved routes from r2, r3, r4 down to the face; the disturbed set wanders and ends off target."""
    srcs = [np.array([SX[1] - 0.2, 2.8, 0]), np.array([SX[2], 2.8, 0]), np.array([SX[3] + 0.2, 2.8, 0])]
    ends = [FACE_C + np.array([-1.0, 1.55, 0]), FACE_C + np.array([0.0, 1.9, 0]), FACE_C + np.array([1.0, 1.55, 0])]
    rng = np.random.RandomState(4)
    paths = []
    for s, e in zip(srcs, ends):
        for j in range(3):
            if disturbed:
                e2 = e + np.array([rng.uniform(-1.6, 1.6), rng.uniform(-0.7, 0.5), 0])
                c1 = s + np.array([rng.uniform(-1.4, 1.4), -0.4, 0])
                c2 = e2 + np.array([rng.uniform(-1.4, 1.4), 0.7, 0])
            else:
                e2 = e + np.array([0.28 * (j - 1), 0.0, 0])
                c1 = s + np.array([(e[0] - s[0]) * 0.1, -1.0, 0])
                c2 = e2 + np.array([0, 0.9, 0])
            paths.append(CubicBezier(s, c1, c2, e2))
    return paths


class S20Crest(SpokenScene):
    def construct(self):
        bs, labs, tb, cord = strip()
        self.add(bs, labs, tb, cord)
        face, flab = face_outline()
        chp = chip("extra retinoic acid", ORANGE, 28).move_to([4.4, 1.6, 0])
        pour = arr([4.4, 2.0, 0], [3.0, 2.85, 0], ORANGE, w=6, tip=0.22)
        self.at("disturbs")
        self.play(FadeIn(chp, shift=UP * 0.15), GrowArrow(pour),
                  *[bs[i].animate.set_fill(ORANGE, 0.28) for i in range(7)], run_time=0.7)
        bad = crest_paths(False)
        ghost = VGroup(*[p.copy().set_stroke(ROSE, 4, opacity=0.75) for p in bad])
        dots = VGroup(*[Dot(p.get_start(), radius=0.15, color=ROSE) for p in bad])
        self.at("neural crest cells")
        self.play(FadeIn(dots, scale=0.6), FadeIn(ghost), run_time=0.6)
        self.at("build much of")
        self.play(Create(face), FadeIn(flab), run_time=0.5)
        self.play(LaggedStart(*[MoveAlongPath(d, p) for d, p in zip(dots, bad)], lag_ratio=0.08), run_time=1.8)
        full = T("in humans, inferred from animal work", 32, TEXT).move_to([0, -3.05, 0])
        n1 = len("in humans,".replace(" ", ""))
        part1, part2 = VGroup(*full[:n1]), VGroup(*full[n1:])
        self.at("in humans")
        self.play(FadeIn(part1), run_time=0.4)
        self.at("inferred from animal")
        self.play(FadeIn(part2), run_time=0.5)
        self.finish()


class S21Beat(NarratedScene):
    def construct(self):
        bs, labs, tb, cord = strip()
        for i in range(7):
            bs[i].set_fill(ORANGE, 0.28)
        face, flab = face_outline()
        bad = crest_paths(False)
        dots = VGroup(*[Dot(p.get_end(), radius=0.15, color=ROSE) for p in bad])
        ghost = VGroup(*[p.copy().set_stroke(ROSE, 4, opacity=0.75) for p in bad])
        chp = chip("extra retinoic acid", ORANGE, 28).move_to([4.4, 1.6, 0])
        pour = arr([4.4, 2.0, 0], [3.0, 2.85, 0], ORANGE, w=6, tip=0.22)
        full = T("in humans, inferred from animal work", 32, TEXT).move_to([0, -3.05, 0])
        self.add(bs, labs, tb, cord, face, flab, dots, ghost, chp, pour, full)
        self.finish()


class S22Take(SpokenScene):
    def construct(self):
        r1a = chip("more early retinoic acid", ORANGE, 34)
        r1b = chip("more posterior code", PURPLE, 34)
        a1 = arr(LEFT * 0.6, RIGHT * 0.6, LG, w=7)
        row1 = VGroup(r1a, a1, r1b).arrange(RIGHT, buff=0.3).move_to([0, 2.0, 0])
        r2a = chip("Hox code", PURPLE, 34)
        r2b = chip("neurons", TEXT, 34)
        a2 = arr(LEFT * 0.6, RIGHT * 0.6, LG, w=7)
        row2 = VGroup(r2a, a2, r2b).arrange(RIGHT, buff=0.3).move_to([0, 0.45, 0])
        lead = T("other inputs help draw the final edges:", 34, LG).move_to([0, -1.0, 0])
        ins = VGroup(chip("segment genes", LG, 32), chip("local signals", LG, 32), chip("repression", LG, 32)
                     ).arrange(RIGHT, buff=0.5).move_to([0, -2.3, 0])
        self.at("more early retinoic acid")
        self.play(FadeIn(r1a, shift=RIGHT * 0.2), run_time=0.5)
        self.at("gives a more posterior")
        self.play(GrowArrow(a1), FadeIn(r1b, shift=RIGHT * 0.2), run_time=0.7)
        self.at("the code helps")
        self.play(FadeIn(r2a, shift=RIGHT * 0.2), run_time=0.4)
        self.at("set the neurons")
        self.play(GrowArrow(a2), FadeIn(r2b, shift=RIGHT * 0.2), run_time=0.6)
        self.at("other inputs")
        self.play(FadeIn(lead), run_time=0.4)
        self.at("help draw")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in ins], lag_ratio=0.25), run_time=0.9)
        self.finish()


class S23End(EndCard):
    LINE = "More early retinoic acid gives a more posterior code."

    def construct(self):
        line = T(self.LINE, size=40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", size=30, color=TEXT)
        g = VGroup(line, sub).arrange(DOWN, buff=0.45)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
