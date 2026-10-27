"""Insulin, glucagon and blood glucose: a beta cell burns glucose to read it  (Biochemistrypedia explainer, Physiology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = glucose
  GREEN  = glucokinase (the enzyme), "supported / required"
  ORANGE = glucose metabolism, ATP relative to ADP
  BLUE   = membrane proteins: transporters and ion channels (KATP, voltage-gated calcium)
  PINK   = potassium ions (K+)
  TEAL   = calcium ions (Ca2+)
  GOLD   = the electrical signal: membrane potential, depolarization
  PURPLE = insulin and its granule
  RED    = "not sufficient / not identified / not established", inhibition
  GREY   = membranes, cells, outlines, de-emphasized text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color=GREY, fill=0.10, sw=3, pos=(0, 0)):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill).move_to([pos[0], pos[1], 0])


def mem(x0, x1, y, h=0.34):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.40).move_to([(x0 + x1) / 2, y, 0])


def channel(x, y, gap=0.46, closed=False, w=0.42, h=0.95):
    """Two blue blocks straddling the membrane with a pore between them. Not a structure: a labelled gate."""
    off = (0.0 if closed else gap) / 2 + w / 2
    l = Rectangle(width=w, height=h, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.55).move_to([x - off, y, 0])
    r = Rectangle(width=w, height=h, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.55).move_to([x + off, y, 0])
    g = VGroup(l, r)
    g.l, g.r, g.gap, g.w = l, r, gap, w
    return g


def open_chan(ch, run=0.7):
    return [ch.l.animate.shift(LEFT * ch.gap / 2), ch.r.animate.shift(RIGHT * ch.gap / 2)]


def close_chan(ch):
    return [ch.l.animate.shift(RIGHT * ch.gap / 2), ch.r.animate.shift(LEFT * ch.gap / 2)]


def ion(label, color, r=0.3, size=22):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.28)
    return VGroup(c, T(label, size, color, weight=BOLD).move_to(c))


def dot(color, r=0.15):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)


def badge(pos, label="P"):
    c = Circle(radius=0.24, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=1)
    return VGroup(c, T(label, 24, BG, weight=BOLD).move_to(c)).move_to([pos[0], pos[1], 0])


def tick(pos, color=GREEN, s=0.28):
    x, y = pos
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.8, 0], color=color, stroke_width=8),
                  Line([x - s * 0.3, y - s * 0.8, 0], [x + s, y + s * 0.8, 0], color=color, stroke_width=8))


def cross(pos, color=RED, s=0.28):
    x, y = pos
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=8),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=8))


def mark(color, pos, kind):
    return tick(pos, color) if kind == "tick" else cross(pos, color)


def tagline(text="working model"):
    return T(text, 22, GREY).move_to([0, 3.3, 0])


# final rule row, shared by scenes 1 and 6 (rebuilt in the same place)
ROW_Y = 0.2


def rule_row():
    g = bchip("glucose", YELLOW, 26).move_to([-5.4, ROW_Y, 0])
    m = bchip("metabolism", ORANGE, 26).move_to([-2.4, ROW_Y, 0])
    s = bchip("electrical signal", GOLD, 26).move_to([1.5, ROW_Y, 0])
    i = bchip("insulin", PURPLE, 26).move_to([5.1, ROW_Y, 0])
    a1 = arr([g.get_right()[0], ROW_Y, 0], [m.get_left()[0], ROW_Y, 0], GREY)
    a2 = arr([m.get_right()[0], ROW_Y, 0], [s.get_left()[0], ROW_Y, 0], GREY)
    a3 = arr([s.get_right()[0], ROW_Y, 0], [i.get_left()[0], ROW_Y, 0], GREY)
    return g, m, s, i, a1, a2, a3


class S00Title(TitleCard):
    LESSON = "Insulin, glucagon and blood glucose"
    TITLE = "A beta cell burns glucose to read it"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """islet -> glucose in, insulin out -> how does glucose become an electrical signal? -> by burning it."""

    def construct(self):
        islet = box(7.2, 4.1, GREY, 0.06, pos=(0, 0.3))
        islet_l = T("islet: a cluster of endocrine cells in the pancreas", 24, GREY).move_to([0, 2.8, 0])
        cells = VGroup()
        for x in (-2.25, 0.0, 2.25):
            b = box(1.95, 2.5, GREY, 0.16, 3, pos=(x, 0.3))
            cells.add(VGroup(b, T("beta\ncell", 24, TEXT, line_spacing=0.8).move_to(b)))
        note = T("schematic, not to scale", 22, GREY).move_to([0, -2.1, 0])
        self.at("An islet")
        self.play(FadeIn(islet), run_time=0.6)
        self.at("pancreas")
        self.play(FadeIn(islet_l), run_time=0.5)
        self.at("Its beta cells")
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cells], lag_ratio=0.25), FadeIn(note), run_time=1.0)

        glu = bchip("glucose", YELLOW, 26).move_to([-5.4, 0.3, 0])
        a_in = arr([-4.5, 0.3, 0], [-3.7, 0.3, 0], YELLOW)
        gd = [dot(YELLOW).move_to([-4.2, 0.3 + (i - 1) * 0.45, 0]) for i in range(3)]
        self.at("Raise the glucose")
        self.play(FadeIn(glu, shift=RIGHT * 0.3), GrowArrow(a_in), run_time=0.7)
        self.play(*[FadeIn(d) for d in gd], run_time=0.2)
        self.play(*[d.animate.move_to([(-2.25, 0.0, 2.25)[i], 1.15, 0]) for i, d in enumerate(gd)],
                  run_time=1.0)
        self.play(*[FadeOut(d) for d in gd], run_time=0.2)

        ins = bchip("insulin", PURPLE, 26).move_to([5.3, 0.3, 0])
        a_out = arr([3.7, 0.3, 0], [4.35, 0.3, 0], PURPLE)
        idots = [dot(PURPLE).move_to(c[0].get_center() + np.array([0, 0.85, 0])) for c in cells]
        self.at("insulin comes out")
        self.play(*[FadeIn(d) for d in idots], run_time=0.2)
        self.play(*[d.animate.move_to([3.9, 0.3 + (i - 1) * 0.3, 0]) for i, d in enumerate(idots)],
                  GrowArrow(a_out), FadeIn(ins), run_time=0.8)
        self.play(*[FadeOut(d) for d in idots], run_time=0.2)

        org = bchip("other organs", GREY, 24).move_to([5.0, -1.7, 0])
        a_org = arr([5.3, -0.1, 0], [5.3, -1.25, 0], PURPLE)
        self.at("changes how glucose moves")
        self.play(GrowArrow(a_org), FadeIn(org), run_time=0.7)

        # --- the question ----------------------------------------------------------------
        self.at("But first")
        self.play(FadeOut(VGroup(islet, islet_l, cells, note, a_in, a_out, a_org, org)),
                  glu.animate.move_to([-5.4, ROW_Y, 0]), ins.animate.move_to([5.1, ROW_Y, 0]), run_time=0.9)
        g, m, s, i, a1, a2, a3 = rule_row()
        q_sig = bchip("electrical signal ?", GOLD, 26).move_to([1.5, ROW_Y, 0])
        q_arr = DashedLine([glu.get_right()[0] + 0.1, ROW_Y, 0], [q_sig.get_left()[0] - 0.1, ROW_Y, 0], color=YELLOW,
                           stroke_width=4, dash_length=0.2)
        q_mark = T("?", 54, YELLOW, weight=BOLD).move_to([-1.8, ROW_Y + 0.75, 0])
        a3_ = arr([q_sig.get_right()[0], ROW_Y, 0], [ins.get_left()[0], ROW_Y, 0], PURPLE)
        self.at("How does glucose become")
        self.play(Create(q_arr), FadeIn(q_sig, scale=0.9), FadeIn(q_mark), GrowArrow(a3_), run_time=1.1)
        self.at("electrical signal")
        self.play(Indicate(VGroup(*q_sig[1:]), color=GOLD, scale_factor=1.12), run_time=0.8)
        self.at("The cell reads")
        self.play(FadeOut(q_arr), FadeOut(q_mark), ReplacementTransform(q_sig, s), ReplacementTransform(a3_, a3),
                  FadeIn(m, scale=0.9), run_time=0.9)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.at("burning")
        self.play(Indicate(VGroup(*m[1:]), color=ORANGE, scale_factor=1.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Burn(SpokenScene):
    """glucose crosses the membrane (GLUT2 in mouse, GLUT1 in isolated human), glucokinase adds a phosphate,
    metabolism raises ATP relative to ADP."""

    def construct(self):
        cell = box(11.8, 5.5, GREY, 0.06, pos=(0, -0.75))
        memb = mem(-5.9, 5.9, 2.0)
        out_l = T("outside the cell", 22, GREY).move_to([4.6, 2.85, 0])
        in_l = T("inside the beta cell", 22, GREY).move_to([4.3, 1.4, 0])
        glu = bchip("glucose", YELLOW, 30).move_to([0, 2.9, 0])
        self.at("Glucose enters")
        self.play(FadeIn(cell), FadeIn(memb), FadeIn(out_l), FadeIn(in_l), FadeIn(glu), run_time=0.8)

        tr = bchip("GLUT2", BLUE, 30).move_to([0, 2.0, 0])
        tag_m = T("mouse beta cells", 24, TEXT).move_to([-4.3, 2.9, 0])
        self.at("Mouse beta cells")
        self.play(FadeIn(tr, scale=0.9), FadeIn(tag_m), run_time=0.6)
        self.at("take it up")
        self.play(glu.animate.move_to([0, -0.4, 0]), run_time=1.5)

        tag_h = T("isolated nondiabetic\nhuman beta cells", 24, TEXT, line_spacing=0.8).move_to([-4.3, 2.9, 0])
        tr2 = bchip("GLUT1", BLUE, 30).move_to([0, 2.0, 0])
        self.at("human beta cells")
        self.play(ReplacementTransform(tag_m, tag_h), ReplacementTransform(tr, tr2), run_time=0.5)
        note = T("predominates, not exclusively", 24, BLUE).move_to([0, 1.4, 0])
        self.at("Predominance does not")
        self.play(FadeIn(note), run_time=0.5)

        self.at("Inside")
        self.play(FadeOut(note), FadeOut(tag_h), glu.animate.move_to([-3.4, 0.3, 0]), run_time=0.9)
        gk = bchip("glucokinase", GREEN, 30).move_to([3.9, 0.3, 0])
        self.at("an enzyme called")
        self.play(FadeIn(gk, shift=LEFT * 0.3), run_time=0.6)
        self.at("adds a phosphate")
        self.play(gk.animate.move_to([-0.55, 0.3, 0]), run_time=0.8)
        pb = badge([-1.2, 0.8, 0])
        self.play(FadeIn(pb, scale=0.6), run_time=0.3)
        self.play(pb.animate.move_to([glu.get_corner(UR)[0] - 0.05, glu.get_corner(UR)[1] + 0.05, 0]), run_time=0.7)
        tag_w = tagline()
        self.at("In a working model")
        self.play(FadeIn(tag_w), run_time=0.4)
        rate = T("sets the rate", 26, GREEN).move_to([-0.55, -0.5, 0])
        self.at("sets the rate")
        self.play(Indicate(VGroup(*gk[1:]), color=GREEN, scale_factor=1.12), FadeIn(rate), run_time=0.8)

        met = bchip("further metabolism", ORANGE, 30).move_to([-2.0, -2.0, 0])
        a_m = arr([-3.4, -0.2, 0], [-2.9, -1.5, 0], ORANGE)
        self.at("Further metabolism")
        self.play(FadeOut(rate), GrowArrow(a_m), FadeIn(met, shift=DOWN * 0.2), run_time=0.8)

        bar = RoundedRectangle(corner_radius=0.1, width=1.1, height=2.5, stroke_color=ORANGE, stroke_width=3,
                               fill_opacity=0).move_to([4.4, -1.5, 0])
        fill0 = Rectangle(width=1.1, height=0.7, stroke_width=0, fill_color=ORANGE, fill_opacity=0.55)
        fill0.move_to(bar.get_bottom() + UP * 0.35)
        g_lab = T("ATP relative to ADP", 24, ORANGE).move_to([4.2, -3.05, 0])
        g_sk = T("in this sketch", 22, GREY).move_to([4.4, -0.0, 0])
        a_g = arr([0.2, -2.0, 0], [3.7, -2.0, 0], ORANGE)
        self.play(FadeIn(bar), FadeIn(fill0), FadeIn(g_lab), FadeIn(g_sk), GrowArrow(a_g), run_time=0.6)
        fill1 = Rectangle(width=1.1, height=2.1, stroke_width=0, fill_color=ORANGE, fill_opacity=0.55)
        fill1.move_to(bar.get_bottom() + UP * 1.05)
        self.at("raises")
        self.play(Transform(fill0, fill1), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Close(SpokenScene):
    """ATP up -> KATP channel closes, less outward K+ -> membrane potential rises -> calcium channels open, Ca2+ enters."""

    def construct(self):
        my = 0.5
        memb = mem(-6.2, 0.7, my, h=0.4)
        out_l = T("outside", 22, GREY).move_to([-5.5, 1.9, 0])
        in_l = T("inside", 22, GREY).move_to([-5.6, -0.55, 0])
        tag_w = tagline().move_to([5.0, 3.3, 0])
        kx = -4.0
        kch = channel(kx, my, closed=False)
        katp_l = T("KATP channel", 24, BLUE).move_to([kx, 2.95, 0])
        k_arrow = arr([kx, -0.2, 0], [kx, 2.3, 0], PINK, w=9, tip=0.3)
        k_lab = T("outward\nK⁺ current", 24, PINK, line_spacing=0.8).move_to([kx + 1.6, 1.5, 0])
        atp = bchip("ATP up relative to ADP", ORANGE, 24).move_to([-3.4, -1.6, 0])
        a_atp = arr([kx, -1.2, 0], [kx, -0.55, 0], ORANGE)
        k1 = ion("K⁺", PINK, 0.3, 22).move_to([kx, -0.5, 0])
        self.at("model")
        self.play(FadeIn(memb), FadeIn(out_l), FadeIn(in_l), FadeIn(tag_w), run_time=0.5)
        self.play(FadeIn(kch), FadeIn(katp_l), GrowArrow(k_arrow), FadeIn(k_lab), FadeIn(atp, shift=UP * 0.2), run_time=0.9)
        self.at("closure of")
        k_thin = DashedLine([kx, 1.15, 0], [kx, 2.2, 0], color=PINK, stroke_width=3, dash_length=0.18)
        self.play(GrowArrow(a_atp), *close_chan(kch), ReplacementTransform(k_arrow, k_thin), FadeOut(k_lab), run_time=0.6)
        self.at("potassium channels")
        self.play(Indicate(kch, color=BLUE, scale_factor=1.25), Indicate(katp_l, color=BLUE, scale_factor=1.1), run_time=0.9)
        self.at("nucleotides")
        self.play(Indicate(VGroup(*atp[1:]), color=ORANGE, scale_factor=1.08), run_time=0.9)
        kb = ion("K⁺", PINK, 0.3, 22).move_to([-2.7, -0.75, 0])
        self.at("With the channels closed")
        self.play(FadeIn(kb), run_time=0.3)
        self.play(kb.animate.move_to([-3.45, -0.3, 0]), run_time=0.8)
        self.play(kb.animate.move_to([-2.7, -0.8, 0]), run_time=0.6)
        self.play(FadeOut(kb), run_time=0.3)
        k_lab2 = T("less outward\nK⁺ current", 24, PINK, line_spacing=0.8).move_to([kx + 1.65, 1.5, 0])
        self.at("less outward")
        self.play(FadeIn(k_lab2), run_time=0.6)

        # voltage sketch
        ax_x0, ax_x1, ax_y0, ax_y1 = 2.0, 6.2, -2.9, 2.5
        yax = arr([ax_x0, ax_y0, 0], [ax_x0, ax_y1, 0], GREY, w=3, tip=0.2)
        xax = arr([ax_x0, ax_y0, 0], [ax_x1, ax_y0, 0], GREY, w=3, tip=0.2)
        ylab = T("membrane potential", 22, GOLD).rotate(PI / 2).move_to([1.35, -0.2, 0])
        top_l = T("less negative", 22, GREY).move_to([3.4, 2.5, 0])
        bot_l = T("more negative", 22, GREY).move_to([3.5, -2.45, 0])
        xlab = T("time, in this sketch", 22, GREY).move_to([4.1, -3.3, 0])

        def v(t):
            return -1.25 + 2.5 / (1.0 + np.exp(-(t - 0.55) / 0.06))

        trace = ParametricFunction(lambda t: np.array([ax_x0 + 0.3 + (ax_x1 - ax_x0 - 0.6) * t, v(t), 0.0]),
                                   t_range=[0, 1, 0.01], color=GOLD, stroke_width=6)
        self.at("depolarization")
        self.play(FadeIn(yax), FadeIn(xax), FadeIn(ylab), FadeIn(top_l), FadeIn(bot_l), FadeIn(xlab), run_time=0.7)
        self.play(Create(trace, rate_func=linear), run_time=2.4)

        cx = -1.0
        cch = channel(cx, my, closed=True)
        ca_l = T("voltage-gated\ncalcium channel", 22, BLUE, line_spacing=0.8).move_to([cx, 2.85, 0])
        self.at("voltage gated")
        self.play(FadeIn(cch), FadeIn(ca_l), run_time=0.6)
        self.at("channels open")
        self.play(*open_chan(cch), run_time=0.6)
        ca = [ion("Ca²⁺", TEAL, 0.33, 22).move_to([cx, 2.1 + 0.0 * i, 0]) for i in range(2)]
        ca[1].move_to([cx + 0.0, 2.1, 0])
        self.at("calcium enters")
        self.play(FadeIn(ca[0]), run_time=0.2)
        self.play(ca[0].animate.move_to([cx, -0.9, 0]), FadeIn(ca[1]), run_time=1.0)
        self.play(ca[1].animate.move_to([cx - 0.0, -0.1, 0]), ca[0].animate.move_to([cx + 0.5, -1.7, 0]), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Release(SpokenScene):
    """calcium enters, a granule fuses with the surface membrane and releases insulin; then the six-link chain."""

    def construct(self):
        my = 0.4
        memb = mem(-6.2, 6.2, my, h=0.4)
        out_l = T("outside", 22, GREY).move_to([5.4, 1.5, 0])
        in_l = T("inside", 22, GREY).move_to([5.5, -0.25, 0])
        tag_w = tagline().move_to([-5.0, 3.3, 0])
        cx = -4.2
        cch = channel(cx, my, closed=False)
        ca_l = T("calcium channel", 24, BLUE).move_to([cx, -0.4, 0])
        ca1 = ion("Ca²⁺", TEAL, 0.33, 22).move_to([cx, 2.1, 0])
        ca2 = ion("Ca²⁺", TEAL, 0.33, 22).move_to([cx, 3.1, 0])
        self.at("Once calcium enters")
        self.play(FadeIn(memb), FadeIn(out_l), FadeIn(in_l), FadeIn(tag_w), FadeIn(cch), FadeIn(ca_l), run_time=0.6)
        self.play(FadeIn(ca1), FadeIn(ca2), run_time=0.3)
        self.play(ca1.animate.move_to([cx, -2.0, 0]), ca2.animate.move_to([cx, -1.0, 0]), run_time=1.0)

        exo = T("exocytosis", 34, TEXT, weight=BOLD).move_to([3.4, -1.7, 0])
        self.at("exocytosis follows")
        self.play(FadeIn(exo, shift=UP * 0.1), FadeOut(ca1), FadeOut(ca2), run_time=0.6)

        gx = 0.4
        gr = Circle(radius=1.0, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.18).move_to([gx, -2.3, 0])
        gdots = VGroup(*[dot(PURPLE, 0.17).move_to([gx + dx, -2.3 + dy, 0])
                         for dx, dy in [(-0.4, 0.25), (0.35, 0.4), (-0.15, -0.4), (0.45, -0.2)]])
        gran = VGroup(gr, gdots)
        gran.set_z_index(2)
        g_l = T("insulin granule", 24, PURPLE).move_to([gx, -3.5, 0])
        self.at("a granule")
        self.play(FadeIn(gran, scale=0.8), FadeIn(g_l), run_time=0.6)
        self.at("fuses with the surface")
        self.play(gran.animate.move_to([gx, -0.55, 0]), g_l.animate.move_to([gx, -1.9, 0]), run_time=1.0)
        gap = Rectangle(width=1.2, height=0.36, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([gx, my, 0])
        gap.set_z_index(1)
        outs = [dot(PURPLE, 0.17).move_to([gx + dx, -0.55 + dy, 0])
                for dx, dy in [(-0.4, 0.25), (0.35, 0.4), (-0.15, -0.4), (0.45, -0.2)]]
        for o in outs:
            o.set_z_index(3)
        self.at("releases insulin")
        self.play(FadeIn(gap), FadeOut(gdots), *[FadeIn(o) for o in outs], run_time=0.4)
        ins_l = T("insulin", 28, PURPLE).move_to([gx, 3.0, 0])
        self.play(*[o.animate.move_to([gx + (-0.8, 0.6, -0.2, 1.1)[i], (1.5, 2.2, 1.9, 2.4)[i], 0]) for i, o in enumerate(outs)],
                  FadeIn(ins_l), run_time=1.0)
        self.play(FadeOut(gap), FadeOut(gr), run_time=0.4)

        # --- the chain -----------------------------------------------------------------------
        self.at("Now read the chain")
        self.play(FadeOut(VGroup(memb, out_l, in_l, cch, ca_l, exo, g_l, ins_l, tag_w, *outs)), run_time=0.7)
        items = [("glucose metabolized", ORANGE, "Glucose is metabolized"),
                 ("ATP up relative to ADP", ORANGE, "rises"),
                 ("KATP channels close", BLUE, "channels close"),
                 ("membrane depolarizes", GOLD, "depolarizes"),
                 ("calcium enters", TEAL, "Calcium enters"),
                 ("insulin released", PURPLE, "is released")]
        pos = [(-4.4, 1.6), (0.0, 1.6), (4.4, 1.6), (4.4, -1.2), (0.0, -1.2), (-4.4, -1.2)]
        chips = [bchip(txt, col, 24).move_to([x, y, 0]) for (txt, col, _), (x, y) in zip(items, pos)]
        arrows = []
        for k in range(5):
            a, b = chips[k], chips[k + 1]
            if pos[k][1] == pos[k + 1][1]:
                sgn = 1 if pos[k + 1][0] > pos[k][0] else -1
                st = [a.get_center()[0] + sgn * (a.width / 2 + 0.05), pos[k][1], 0]
                en = [b.get_center()[0] - sgn * (b.width / 2 + 0.05), pos[k][1], 0]
            else:
                st = [pos[k][0], pos[k][1] - 0.5, 0]
                en = [pos[k + 1][0], pos[k + 1][1] + 0.5, 0]
            arrows.append(arr(st, en, GREY, w=4, tip=0.18))
        self.at("Glucose is metabolized")
        self.play(FadeIn(chips[0], scale=0.9), run_time=0.5)
        for k in range(1, 6):
            self.at(items[k][2], nth=1 if items[k][2] == "Calcium enters" else 0)
            self.play(GrowArrow(arrows[k - 1]), FadeIn(chips[k], shift=DOWN * 0.15), run_time=0.5)
        wm = T("working model", 34, TEXT).move_to([0, -2.9, 0])
        wl = Line([-3.0, -2.5, 0], [3.0, -2.5, 0], color=GOLD, stroke_width=4)
        self.at("That is the working model")
        self.play(FadeIn(wm), Create(wl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pulses(x0, x1, y_closed, y_open, spans):
    """A schematic opening trace: baseline at y_closed, square pulses to y_open over the given (start, end) fractions."""
    pts = [[x0, y_closed, 0]]
    for a, b in spans:
        xa, xb = x0 + (x1 - x0) * a, x0 + (x1 - x0) * b
        pts += [[xa, y_closed, 0], [xa, y_open, 0], [xb, y_open, 0], [xb, y_closed, 0]]
    pts.append([x1, y_closed, 0])
    m = VMobject(color=BLUE, stroke_width=5)
    m.set_points_as_corners(pts)
    return m


def hypothesis_rows():
    """Two routes from glucose to channel closure: binding outside the cell, or metabolism."""
    ya, yb = 1.15, -1.35
    ga = bchip("glucose", YELLOW, 26).move_to([-5.15, ya, 0])
    gb = bchip("glucose", YELLOW, 26).move_to([-5.15, yb, 0])
    ma = bchip("binds outside the cell", GREY, 24).move_to([-1.55, ya, 0])
    mb = bchip("metabolism", ORANGE, 24).move_to([-1.55, yb, 0])
    ca = bchip("channel closes", BLUE, 24).move_to([4.55, ya, 0])
    cb = bchip("channel closes", BLUE, 24).move_to([4.55, yb, 0])
    aa1 = arr([ga.get_right()[0], ya, 0], [ma.get_left()[0], ya, 0], GREY)
    aa2 = arr([ma.get_right()[0], ya, 0], [ca.get_left()[0], ya, 0], GREY)
    ab1 = arr([gb.get_right()[0], yb, 0], [mb.get_left()[0], yb, 0], GREY)
    ab2 = arr([mb.get_right()[0], yb, 0], [cb.get_left()[0], yb, 0], GREY)
    rows = VGroup(ga, ma, ca, aa1, aa2, gb, mb, cb, ab1, ab2)
    rows.ya, rows.yb, rows.ma, rows.mb, rows.aa2, rows.ab2, rows.ca, rows.cb = ya, yb, ma, mb, aa2, ab2, ca, cb
    return rows


class S05Patch(SpokenScene):
    """The test: two routes; a patch clamp on an isolated rat beta cell; metabolism required, outside binding argued against."""

    def construct(self):
        rows = hypothesis_rows()
        q1 = T("?", 54, YELLOW, weight=BOLD).move_to([0.9, rows.ya + 0.5, 0])
        q2 = T("?", 54, YELLOW, weight=BOLD).move_to([0.9, rows.yb + 0.5, 0])
        self.at("How can we test")
        self.play(FadeIn(rows), run_time=0.8)
        self.at("metabolism links")
        self.play(FadeIn(q1), FadeIn(q2), Indicate(VGroup(*rows.mb[1:]), color=ORANGE, scale_factor=1.15), run_time=0.9)

        # --- the experiment --------------------------------------------------------------------------
        head = T("1984: Ashcroft, Harrison and Ashcroft", 22, TEXT).move_to([-3.3, 3.3, 0])
        cell = box(5.6, 3.5, GREY, 0.07, pos=(-3.4, -0.55))
        memb = mem(-6.15, -0.65, 1.2, h=0.34)
        cell_l = T("isolated rat beta cell", 24, TEXT).move_to([-3.4, -0.1, 0])
        kch = channel(-3.4, 1.2, gap=0.3, closed=False, w=0.34, h=0.7)
        self.at("Ashcroft")
        self.play(FadeOut(rows), FadeOut(q1), FadeOut(q2), run_time=0.5)
        self.play(FadeIn(head), FadeIn(cell), FadeIn(memb), run_time=0.5)
        self.at("single channels")
        self.play(FadeIn(kch, scale=0.8), run_time=0.5)
        self.at("isolated rat")
        self.play(FadeIn(cell_l), run_time=0.4)

        pip = Polygon([-4.15, 3.05, 0], [-2.65, 3.05, 0], [-3.17, 1.4, 0], [-3.63, 1.4, 0], stroke_color=GREY, stroke_width=3,
                      fill_color=GREY, fill_opacity=0.35)
        pip.shift(UP * 1.3)
        pip_l = T("pipette", 24, GREY).move_to([-5.45, 2.35, 0])
        pc_l = T("cell-attached patch clamp", 22, GREY).move_to([-3.4, -2.85, 0])
        self.at("patch clamp")
        self.play(FadeIn(pc_l), run_time=0.5)
        self.at("pipette seals")
        self.play(FadeIn(pip_l), pip.animate.shift(DOWN * 1.3), run_time=1.0)
        patch_l = T("membrane patch", 22, BLUE).move_to([-1.55, 2.0, 0])
        patch_ln = Line([-2.7, 1.9, 0], [-3.05, 1.35, 0], color=BLUE, stroke_width=3)
        intact = T("cell stays intact", 22, GREY).move_to([-3.4, -1.0, 0])
        self.at("the cell stays")
        self.play(FadeIn(patch_l), Create(patch_ln), FadeIn(intact), run_time=0.6)

        # traces: schematic, computed from fixed spans (not data)
        pa = box(6.2, 1.9, GREY, 0.05, 2, pos=(3.1, 2.15))
        pb = box(6.2, 1.9, GREY, 0.05, 2, pos=(3.1, -0.05))
        la = T("low glucose", 22, TEXT).move_to([1.1, 2.75, 0])
        lb = T("higher glucose", 22, TEXT).move_to([1.4, 0.55, 0])
        op_a = T("open", 22, GREY).move_to([0.45, 2.15, 0])
        cl_a = T("closed", 22, GREY).move_to([0.55, 1.55, 0])
        op_b = T("open", 22, GREY).move_to([0.45, -0.05, 0])
        cl_b = T("closed", 22, GREY).move_to([0.55, -0.65, 0])
        ta = pulses(1.35, 5.95, 1.55, 2.2, [(0.03, 0.12), (0.2, 0.24), (0.33, 0.47), (0.55, 0.6), (0.68, 0.84), (0.9, 0.95)])
        tb = pulses(1.35, 5.95, -0.65, -0.0, [])
        sk = T("schematic, not recorded data", 22, GREY).move_to([3.1, -1.45, 0])
        self.at("A potassium channel")
        self.play(Indicate(kch, color=BLUE, scale_factor=1.3), run_time=0.7)
        self.at("active at low")
        self.play(FadeIn(pa), FadeIn(la), FadeIn(op_a), FadeIn(cl_a), Create(ta, rate_func=linear), FadeIn(sk), run_time=1.6)
        self.at("closed when glucose")
        self.play(FadeIn(pb), FadeIn(lb), FadeIn(op_b), FadeIn(cl_b), run_time=0.5)
        self.play(Create(tb, rate_func=linear), *close_chan(kch), run_time=1.0)

        # --- the verdict ---------------------------------------------------------------------------
        rows2 = hypothesis_rows()
        self.at("The closure required")
        self.play(FadeOut(VGroup(head, cell, memb, cell_l, kch, pip, pip_l, pc_l, patch_l, patch_ln, intact, pa, pb, la, lb,
                                 op_a, cl_a, op_b, cl_b, ta, tb, sk)), run_time=0.5)
        self.play(FadeIn(rows2), run_time=0.6)
        self.at("glucose metabolism")
        yb = rows2.yb
        tk = tick([0.9, yb + 0.9], GREEN)
        req = T("closure required glucose metabolism", 24, GREEN).move_to([0.9, yb - 0.9, 0])
        self.play(Create(tk), FadeIn(req), Indicate(VGroup(*rows2.mb[1:]), color=ORANGE, scale_factor=1.12), run_time=0.9)
        ya = rows2.ya
        self.at("argued against")
        cx = cross([0.9, ya + 0.9], RED)
        arg = T("argued against as sufficient on its own", 24, RED).move_to([0.9, ya - 0.9, 0])
        self.play(Create(cx), FadeIn(arg), rows2.aa2.animate.set_color(RED), rows2.ma[1].animate.set_stroke(RED).set_fill(RED, 0.16),
                  rows2.ma[2].animate.set_color(RED), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Limits(SpokenScene):
    """What the 1984 result did and did not show; the excised-patch result; the rule."""

    def construct(self):
        ys = [1.6, -0.2, -1.8]
        specs = [("supported", GREEN, "a metabolic link to depolarization\nin this rat preparation", "tick"),
                 ("not identified", RED, "ATP as the messenger", "cross"),
                 ("not established", RED, "the entire secretion sequence", "cross")]
        cards = []
        for (lab, col, txt, kind), y in zip(specs, ys):
            c = bchip(lab, col, 30).move_to([-3.9, y, 0])
            t = T(txt, 30, TEXT, line_spacing=0.8)
            t.move_to([-1.5 + t.width / 2, y, 0])
            cards.append(VGroup(c, t))
        head = T("1984, isolated rat beta cells", 28, GREY).move_to([0, 3.0, 0])
        self.at("What did that show")
        self.play(FadeIn(head), run_time=0.5)
        self.at("metabolic link")
        self.play(FadeIn(cards[0], shift=RIGHT * 0.3), run_time=0.7)
        self.at("did not identify")
        self.play(FadeIn(cards[1], shift=RIGHT * 0.3), run_time=0.7)
        self.at("did not establish")
        self.play(FadeIn(cards[2], shift=RIGHT * 0.3), run_time=0.7)

        # --- Cook and Hales: excised patch -----------------------------------------------------------
        title = T("Cook and Hales, 1984: excised beta-cell membrane patch", 28, TEXT).move_to([0, 3.0, 0])
        memb = mem(-5.6, 5.6, 1.3, h=0.5)
        kch = channel(0, 1.3, gap=0.6, closed=False, w=0.6, h=1.3)
        k_l = T("potassium channel", 28, BLUE).move_to([3.2, 2.5, 0])
        cyt = T("cytoplasmic side", 28, GREY).move_to([-3.6, 0.3, 0])
        atp = bchip("ATP", ORANGE, 36).move_to([0, -1.6, 0])
        inh = VGroup(Line([0, -1.1, 0], [0, 0.25, 0], color=RED, stroke_width=7),
                     Line([-0.45, 0.25, 0], [0.45, 0.25, 0], color=RED, stroke_width=9))
        inh_l = T("inhibition", 30, RED).move_to([1.9, -0.4, 0])
        self.at("Cook and Hales")
        self.play(FadeOut(VGroup(head, *cards)), run_time=0.6)
        self.play(FadeIn(title), FadeIn(memb), FadeIn(kch), run_time=0.6)
        self.at("ATP inhibition")
        self.play(FadeIn(atp, shift=UP * 0.3), run_time=0.5)
        self.play(Create(inh), FadeIn(inh_l), *close_chan(kch), run_time=0.7)
        self.at("cytoplasmic side")
        self.play(FadeIn(cyt), run_time=0.5)
        self.at("excised")
        self.play(FadeIn(k_l), run_time=0.5)

        sup = bchip("supports the metabolic-channel model", GREEN, 28).move_to([0, -3.0, 0])
        self.at("support")
        self.play(FadeIn(sup, shift=UP * 0.2), run_time=0.7)

        # --- the rule ------------------------------------------------------------------------------
        self.at("Keep the rule")
        self.play(FadeOut(VGroup(title, memb, kch, k_l, cyt, atp, inh, inh_l, sup)), run_time=0.7)
        g, m, s, i, a1, a2, a3 = rule_row()
        self.play(FadeIn(g), FadeIn(m), FadeIn(s), FadeIn(i), GrowArrow(a1), GrowArrow(a2), GrowArrow(a3), run_time=0.9)
        self.at("burning")
        self.play(Indicate(VGroup(*m[1:]), color=ORANGE, scale_factor=1.2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "A beta cell reads glucose by burning it."
