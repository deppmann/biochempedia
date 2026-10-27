"""Calcium, phosphate and bone: a small step sets calcium loss  (Biochemistrypedia explainer, Physiology)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = filtered calcium, the filtered load
  GREEN  = reabsorbed calcium, back into the blood; the distal reabsorption step
  ORANGE = calcium excreted in urine (the sliver)
  YELLOW = ionized calcium in plasma (the fraction the parathyroid reads)
  TEAL   = complexed calcium
  PURPLE = PTH
  PINK   = the calcium-sensing receptor
  RED    = stop: not filtered, secretion inhibited
  GREY   = tissues, blocks, plasma bound to protein, outlines, de-emphasized text
All numbers on screen are the lesson's made-up round numbers for a reference adult at steady state.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB0"
TEAL2 = "#3FB8C0"

# lesson numbers
LOAD = 10800.0
FE1, FE2 = 200.0 / 10800.0, 324.0 / 10800.0      # 0.0185 and 0.030


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def box(w, h, color=GREY, fill=0.10, sw=3, pos=(0, 0)):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill).move_to([pos[0], pos[1], 0])


def rect(x_left, w, y, h, color, fill=0.5):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=fill).move_to(
        [x_left + w / 2, y, 0])


def Ln(a, b, **kw):
    return Line([a[0], a[1], 0], [b[0], b[1], 0], **kw)


def lft(m, x, y):
    return m.move_to([x + m.width / 2, y, 0])


def rgt(m, x, y):
    return m.move_to([x - m.width / 2, y, 0])


def lines(texts, color, size, x, y, align="L", gap=0.1, colors=None):
    ts = [T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)]
    g = VGroup(*ts).arrange(DOWN, buff=gap, aligned_edge=LEFT if align == "L" else RIGHT if align == "R" else ORIGIN)
    if align == "L":
        g.move_to([x + g.width / 2, y, 0])
    elif align == "R":
        g.move_to([x - g.width / 2, y, 0])
    else:
        g.move_to([x, y, 0])
    return g


class S00Title(TitleCard):
    LESSON = "Calcium, phosphate and bone"
    TITLE = "A small step sets calcium loss"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """Almost all filtered calcium goes back to blood; what sets the small fraction lost in urine?"""

    def construct(self):
        x0, W, y, H = -5.0, 10.0, 0.4, 2.0
        sl = W * 0.02
        big = rect(x0, W - sl, y, H, BLUE, 0.5)
        sliver = rect(x0 + W - sl, sl, y, H, BLUE, 0.5)
        top = lft(T("filtered per day: about 10 g", 34, BLUE), x0, y + H / 2 + 0.5)

        self.at("kidneys filter")
        self.play(GrowFromEdge(big, LEFT), FadeIn(sliver), FadeIn(top), run_time=1.1)

        urine = rgt(T("urine: about 0.2 g per day", 26, ORANGE), x0 + W, y - H / 2 - 0.55)
        lead = Ln([x0 + W - sl / 2, y - H / 2], [x0 + W - sl / 2, y - H / 2 - 0.3], color=ORANGE, stroke_width=3)
        self.at("You lose about")
        self.play(sliver.animate.set_fill(ORANGE, 0.95), FadeIn(urine), Create(lead), run_time=0.7)
        self.play(Indicate(sliver, color=ORANGE, scale_factor=1.5), run_time=0.7)

        back = lft(T("back into the blood", 30, GREEN), x0, y - H / 2 - 0.55)
        self.at("goes back")
        self.play(big.animate.set_fill(GREEN, 0.5), FadeIn(back), run_time=0.8)

        q = T("?", 84, TEXT, weight=BOLD).move_to([x0 + W - sl / 2, y + H / 2 + 0.95, 0])
        qa = arr([x0 + W - sl / 2, y + H / 2 + 0.5], [x0 + W - sl / 2, y + H / 2 + 0.05], TEXT, 4, 0.16)
        self.at("What sets")
        self.play(FadeIn(q, scale=0.7), GrowArrow(qa), run_time=0.7)

        c1 = bchip("made-up round numbers", GREY, 24).move_to([-3.9, -2.65, 0])
        c2 = bchip("reference adult", GREY, 24).move_to([0.2, -2.65, 0])
        c3 = bchip("steady state", GREY, 24).move_to([3.3, -2.65, 0])
        self.at("round numbers")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.5)
        self.at("reference adult")
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.5)
        self.at("steady state")
        self.play(FadeIn(c3, shift=UP * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Load(SpokenScene):
    """Three plasma pockets; protein-bound is not filtered; the arithmetic of the filtered load."""

    def construct(self):
        y, H = 2.1, 1.1
        title = T("adult plasma calcium", 26, GREY).move_to([0, 3.2, 0])
        ion = rect(-5.0, 5.0, y, H, YELLOW, 0.55)
        com = rect(0.0, 1.0, y, H, TEAL2, 0.6)
        pro = rect(1.0, 4.0, y, H, GREY, 0.5)
        l_ion = lines(["ionized", "roughly half"], None, 26, -2.5, 0.95, "C", 0.05, [YELLOW, GREY])
        l_com = lines(["complexed", "about 10 percent"], None, 24, 0.2, 0.95, "C", 0.05, [TEAL2, GREY])
        l_pro = lines(["bound to protein", "about 40 percent"], None, 24, 3.2, 0.95, "C", 0.05, [GREY, GREY])
        for m in (l_ion, l_com, l_pro):
            m[1].scale(0.92)

        self.at("adult plasma")
        self.play(FadeIn(title), run_time=0.4)
        self.at("roughly half")
        self.play(GrowFromEdge(ion, LEFT), FadeIn(l_ion), run_time=0.8)
        self.at("bound to protein")
        self.play(GrowFromEdge(pro, LEFT), FadeIn(l_pro), run_time=0.8)
        self.at("and about")
        self.play(GrowFromEdge(com, LEFT), FadeIn(l_com), run_time=0.7)

        nf = T("not filtered", 30, RED, weight=BOLD).move_to([3.0, y, 0])
        self.at("is not filtered")
        self.play(pro.animate.set_fill(GREY, 0.10).set_stroke(RED, 3), FadeIn(nf), run_time=0.7)

        r1 = M("GFR 125 mL/min = 180 L per day", 28, TEXT)
        r1 = lft(r1, -6.0, -1.0)
        self.at("per minute")
        self.play(FadeIn(r1, shift=RIGHT * 0.3), run_time=0.6)

        r2a = lft(M("total calcium 100 mg/L", 28, TEXT), -6.0, -1.85)
        r2b = lft(M("total calcium 100 mg/L x 60 percent filterable = 60 mg/L", 28, TEXT), -6.0, -1.85)
        fit(r2b, max_w=12.0)
        r2b.move_to([-6.0 + r2b.width / 2, -1.85, 0])
        self.at("Total calcium")
        self.play(FadeIn(r2a, shift=RIGHT * 0.3), run_time=0.5)

        brk = VGroup(Ln([-5.0, 0.28, 0], [1.0, 0.28, 0], color=BLUE, stroke_width=4),
                     Ln([-5.0, 0.28, 0], [-5.0, 0.48, 0], color=BLUE, stroke_width=4),
                     Ln([1.0, 0.28, 0], [1.0, 0.48, 0], color=BLUE, stroke_width=4))
        bl = T("filterable: 60 percent", 26, BLUE).move_to([-2.0, -0.12, 0])
        self.at("is filterable")
        self.play(Transform(r2a, r2b), Create(brk), FadeIn(bl), run_time=0.9)

        res = bchip("filtered load = 180 L x 60 mg/L = 10,800 mg per day", BLUE, 28)
        res.scale(min(1.0, 11.8 / res.width)).move_to([0, -3.0, 0])
        self.at("filtered load")
        self.play(FadeIn(res, scale=0.9), run_time=0.7)
        self.play(Indicate(res, color=BLUE, scale_factor=1.05), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Segments(SpokenScene):
    """Proximal tubule, thick ascending limb, distal tubules: the stream narrows, green arrows into blood."""

    def construct(self):
        cx = [-4.1, 0.0, 4.1]
        names = ["proximal\ntubule", "thick\nascending limb", "distal convoluted\nand connecting\ntubules"]
        boxes = []
        for c, n in zip(cx, names):
            b = box(2.9, 1.9, GREY, 0.12, 3, pos=(c, 0.35))
            t = T(n, 24, TEXT, line_spacing=0.8).move_to(b)
            boxes.append(VGroup(b, t))
        blood = box(12.4, 0.62, GREEN, 0.22, 3, pos=(0, 3.0))
        blood_l = T("blood", 26, GREEN).move_to(blood)

        inlet = bchip("filtered calcium", BLUE, 26).move_to([-4.2, -2.0, 0])
        a_in = arr([-4.6, -1.62], [-4.6, -0.62], BLUE, 14, 0.3)

        note = T("schematic, not to scale", 22, GREY).move_to([-4.3, -3.2, 0])
        self.at("Most of that")
        self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15), FadeIn(blood), FadeIn(blood_l),
                  FadeIn(inlet), GrowArrow(a_in), FadeIn(note), run_time=1.0)

        def up(c, w):
            return arr([c - 0.95, 1.32], [c - 0.95, 2.68], GREEN, w, 0.26)

        def lab(c, text):
            return lines(text, None, 24, c - 0.28, 2.0, "L", 0.12, [GREEN] * len(text))

        # proximal tubule
        u1, l1 = up(cx[0], 14), lab(cx[0], ["60 to 70", "percent"])
        s12 = arr([cx[0] + 1.5, 0.35], [cx[1] - 1.5, 0.35], BLUE, 9, 0.26)
        self.at("proximal tubule")
        self.play(GrowArrow(u1), FadeIn(l1), boxes[0][0].animate.set_stroke(GREEN, 4), run_time=0.8)
        self.play(GrowArrow(s12), run_time=0.5)

        # thick ascending limb
        u2, l2 = up(cx[1], 9), lab(cx[1], ["20 to 25", "percent"])
        s23 = arr([cx[1] + 1.5, 0.35], [cx[2] - 1.5, 0.35], BLUE, 5, 0.22)
        self.at("thick ascending limb")
        self.play(GrowArrow(u2), FadeIn(l2), boxes[1][0].animate.set_stroke(GREEN, 4), run_time=0.8)
        note2 = T("largely between cells", 22, GREEN).move_to([0.0, -0.95, 0])
        self.at("between cells")
        self.play(FadeIn(note2), run_time=0.5)
        self.play(GrowArrow(s23), run_time=0.5)

        # distal tubules
        u3, l3 = up(cx[2], 5), lab(cx[2], ["5 to 10", "percent"])
        note3 = T("through cells", 22, GREEN).move_to([4.1, -0.95, 0])
        urine_a = arr([5.3, -0.62], [5.3, -1.4], ORANGE, 4, 0.2)
        urine = bchip("urine", ORANGE, 26).move_to([5.3, -1.85, 0])
        self.at("distal convoluted")
        self.play(GrowArrow(u3), FadeIn(l3), boxes[2][0].animate.set_stroke(GREEN, 4), run_time=0.8)
        self.at("through cells")
        self.play(FadeIn(note3), run_time=0.4)
        self.play(GrowArrow(urine_a), FadeIn(urine), run_time=0.6)

        pth = bchip("PTH regulates this step", PURPLE, 26).move_to([2.3, -2.85, 0])
        pa = arr([2.9, -2.45], [2.9, -0.7], PURPLE, 5, 0.22)
        self.at("parathyroid hormone")
        self.play(FadeIn(pth, shift=UP * 0.2), GrowArrow(pa), boxes[2][0].animate.set_stroke(PURPLE, 6), run_time=0.8)
        self.play(Indicate(boxes[2][0], color=PURPLE, scale_factor=1.06), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Change(SpokenScene):
    """200 mg per day is 1.85 percent of 10,800; let reabsorption fall to 97 percent: 324 mg per day."""

    def construct(self):
        x0, W, y, H = -5.5, 11.0, 2.0, 1.0

        def split(fr):
            gw = W * fr
            return rect(x0, gw, y, H, GREEN, 0.5), rect(x0 + gw, W - gw, y, H, ORANGE, 0.95)

        def olab(l1, l2, fr):
            g = lines([l1, l2] if l2 else [l1], None, 26, x0 + W, y - H / 2 - 0.65, "R", 0.06,
                      [ORANGE] * (2 if l2 else 1))
            return g

        def glab(l2):
            return lines(["reabsorbed", l2], None, 26, x0, y - H / 2 - 0.65, "L", 0.06, [GREEN, GREEN])

        full = rect(x0, W, y, H, BLUE, 0.5)
        top = lft(T("filtered load: 10,800 mg per day", 30, BLUE), x0, 3.15)
        self.play(GrowFromEdge(full, LEFT), FadeIn(top), run_time=0.7)

        g1, o1 = split(1 - FE1)
        ol1 = olab("excreted: 200 mg per day", None, FE1)
        lead1 = Ln([x0 + W - W * FE1 / 2, y - H / 2], [x0 + W - W * FE1 / 2, y - H / 2 - 0.2], color=ORANGE, stroke_width=3)
        # chart
        base_y, sc = -3.0, 0.0068
        axis = Ln([-5.7, base_y, 0], [-0.7, base_y, 0], color=GREY, stroke_width=3)
        b1 = rect(-4.4 - 0.65, 1.3, base_y + 200 * sc / 2, 200 * sc, ORANGE, 0.6)
        b1.move_to([-4.4, base_y + 200 * sc / 2, 0])
        v1 = T("200 mg/day", 24, ORANGE).move_to([-4.4, base_y + 200 * sc + 0.3, 0])
        c1 = lines(["98.15 percent", "reabsorbed"], None, 22, -4.4, base_y - 0.45, "C", 0.0, [GREEN, GREEN])
        self.at("in the example")
        self.play(FadeOut(full), FadeIn(g1), FadeIn(o1), FadeIn(ol1), Create(lead1), run_time=0.7)
        self.play(Create(axis), GrowFromEdge(b1, DOWN), FadeIn(v1), run_time=0.8)

        ol1b = olab("excreted: 200 mg per day", "1.85 percent of the load", FE1)
        self.at("of the filtered load")
        self.play(Transform(ol1, ol1b), run_time=0.5)
        gl1 = glab("98.15 percent")
        self.at("is reabsorbed")
        self.play(FadeIn(gl1), FadeIn(c1), run_time=0.5)
        self.wait(self.beat(0.02))

        # ---- new case: reset every result to neutral together with the new case ---------------------
        g2, o2 = split(0.97)
        ol2 = olab("excreted", None, FE2)
        lead2 = Ln([x0 + W - W * FE2 / 2, y - H / 2], [x0 + W - W * FE2 / 2, y - H / 2 - 0.2], color=ORANGE, stroke_width=3)
        gl2 = glab("97.0 percent")
        c2 = lines(["97.0 percent", "reabsorbed"], None, 22, -2.2, base_y - 0.45, "C", 0.0, [GREEN, GREEN])
        pthc = bchip("PTH falls", PURPLE, 26).move_to([0.0, 0.1, 0])
        same = rgt(T("same filtered load", 24, GREY), x0 + W, 3.15)
        self.at("Now let reabsorption fall")
        self.play(Transform(g1, g2), Transform(o1, o2), Transform(ol1, ol2), Transform(lead1, lead2),
                  Transform(gl1, gl2), FadeIn(c2), FadeIn(same), run_time=0.9)
        self.at("as when")
        self.play(FadeIn(pthc, shift=DOWN * 0.15), run_time=0.5)

        b2 = rect(-2.2 - 0.65, 1.3, base_y + 324 * sc / 2, 324 * sc, ORANGE, 0.95)
        b2.move_to([-2.2, base_y + 324 * sc / 2, 0])
        v2 = T("324 mg/day", 24, ORANGE).move_to([-2.2, base_y + 324 * sc + 0.3, 0])
        ol3 = olab("excreted: 324 mg per day", "3.0 percent of the load", FE2)
        r1 = lft(T("200 to 324 mg per day", 28, ORANGE), 0.8, -1.15)
        self.at("Excretion becomes")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(v2), Transform(ol1, ol3), run_time=0.9)
        self.play(FadeIn(r1, shift=RIGHT * 0.2), run_time=0.5)
        r2 = lft(T("1.62 times the original", 28, ORANGE), 0.8, -1.8)
        self.at("times the original")
        self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=0.5)
        r3 = lines(["about 1.15 percentage points", "less reabsorbed moves", "excretion by 62 percent"], TEXT, 24,
                   0.8, -2.85, "L", 0.14)
        self.at("A fall of about")
        self.play(FadeIn(r3, shift=RIGHT * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Sensor(SpokenScene):
    """Ionized calcium rises: receptor inhibits PTH (steeply); PTH raises distal reabsorption; PTH falls: urine calcium rises."""

    def construct(self):
        sx = -4.0
        ion = bchip("ionized calcium", YELLOW, 28).move_to([sx, 3.0, 0])
        blk = box(4.4, 2.1, GREY, 0.12, 3, pos=(sx, 0.85))
        blk_t = T("parathyroid chief cells", 24, TEXT).move_to([sx, 1.55, 0])
        rec = bchip("calcium-sensing receptor", PINK, 24).move_to([sx, 0.45, 0])
        a_in = arr([sx, 2.55], [sx, 1.98], YELLOW, 5, 0.2)
        pth = bchip("PTH", PURPLE, 30).move_to([sx, -2.6, 0])

        self.at("chief cells")
        self.play(FadeIn(blk), FadeIn(blk_t), run_time=0.7)
        self.at("calcium sensing receptor")
        self.play(FadeIn(rec, scale=0.85), run_time=0.6)
        self.at("reads ionized")
        self.play(FadeIn(ion, shift=DOWN * 0.2), GrowArrow(a_in), run_time=0.7)

        up_ca = arr([sx + 2.0, 2.75], [sx + 2.0, 3.45], YELLOW, 6, 0.22)
        self.at("ionized calcium activates")
        self.play(GrowArrow(up_ca), run_time=0.5)
        self.at("activates the receptor")
        self.play(Indicate(rec, color=PINK, scale_factor=1.12), rec[0].animate.set_fill(PINK, 0.4), run_time=0.7)
        inh = arr([sx - 0.0, -0.25], [sx, -2.1], RED, 5, 0.2)
        stop = Ln([sx - 0.45, -1.2, 0], [sx + 0.45, -1.2, 0], color=RED, stroke_width=8)
        inh_l = T("inhibits", 26, RED).move_to([sx + 1.35, -1.2, 0])
        self.at("inhibits")
        self.play(GrowArrow(inh), FadeIn(stop), FadeIn(inh_l), FadeIn(pth), run_time=0.8)

        # steep inverse sigmoid, a sketch
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1.1, 0.5], x_length=5.2, y_length=3.0, tips=False,
                  axis_config={"stroke_width": 3, "color": GREY, "include_ticks": False, "include_numbers": False}
                  ).move_to([3.3, 1.55, 0])
        curve = ax.plot(lambda x: 1.0 / (1.0 + np.exp(14.0 * (x - 0.5))), x_range=[0, 1], color=PURPLE, stroke_width=5)
        xl = T("ionized calcium in plasma", 22, YELLOW).move_to([3.3, -0.2, 0])
        yl = T("PTH secretion", 22, PURPLE).rotate(PI / 2).move_to([0.2, 1.55, 0])
        tag = T("in this sketch, relative units", 22, GREY).move_to([3.3, 3.3, 0])
        self.at("The response")
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tag), Create(curve), run_time=1.0)

        f = lambda x: 1.0 / (1.0 + np.exp(14.0 * (x - 0.5)))
        dot = Dot(ax.c2p(0.40, f(0.40)), radius=0.13, color=YELLOW)
        g1 = DashedLine(ax.c2p(0.40, 0), ax.c2p(0.40, f(0.40)), color=YELLOW, stroke_width=3, dash_length=0.1)
        g2 = DashedLine(ax.c2p(0.55, 0), ax.c2p(0.55, f(0.55)), color=YELLOW, stroke_width=3, dash_length=0.1)
        h1 = DashedLine(ax.c2p(0, f(0.40)), ax.c2p(0.40, f(0.40)), color=PURPLE, stroke_width=3, dash_length=0.1)
        h2 = DashedLine(ax.c2p(0, f(0.55)), ax.c2p(0.55, f(0.55)), color=PURPLE, stroke_width=3, dash_length=0.1)
        self.at("small change in calcium")
        self.play(FadeIn(dot, scale=0.6), Create(g1), Create(h1), run_time=0.5)
        self.play(dot.animate.move_to(ax.c2p(0.55, f(0.55))), Create(g2), Create(h2), run_time=1.4)

        # PTH -> distal nephron -> urine
        dis = box(3.7, 1.3, GREY, 0.12, 3, pos=(0.05, -2.6))
        dis_t = VGroup(T("distal nephron", 24, TEXT), T("calcium reabsorption", 22, GREEN)).arrange(DOWN, buff=0.08).move_to(dis)
        a_pd = arr([sx + 0.9, -2.6], [-1.9, -2.6], PURPLE, 5, 0.22)
        urine = bchip("urinary calcium", ORANGE, 26).move_to([4.6, -2.6, 0])
        a_du = arr([1.95, -2.6], [3.0, -2.6], ORANGE, 5, 0.22)
        self.at("raises active")
        self.play(GrowArrow(a_pd), FadeIn(dis), FadeIn(dis_t), run_time=0.8)

        d_pth = arr([sx - 1.4, -2.2], [sx - 1.4, -3.1], PURPLE, 6, 0.2)
        d_dis = arr([1.4, -1.15], [1.4, -1.8], GREEN, 6, 0.2)
        self.at("So when")
        self.play(GrowArrow(d_pth), run_time=0.5)
        self.at("reabsorption falls")
        self.play(GrowArrow(d_dis), run_time=0.5)
        same = bchip("same filtered load", GREY, 24).move_to([4.6, -3.3, 0])
        self.at("same filtered load")
        self.play(FadeIn(same, shift=UP * 0.15), run_time=0.5)
        self.at("urinary calcium rises")
        self.play(GrowArrow(a_du), FadeIn(urine), run_time=0.5)
        d_urine = arr([4.6, -2.0], [4.6, -1.35], ORANGE, 6, 0.2)
        self.play(GrowArrow(d_urine), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """The rule: filtered about 10 g, about 98 percent reabsorbed, the distal step under a tenth sets the output."""

    def construct(self):
        x0, W, y, H = -5.0, 10.0, 0.5, 1.5
        gw, ow = W * (1 - FE1), W * FE1
        green = rect(x0, gw, y, H, BLUE, 0.5)
        orange = rect(x0 + gw, ow, y, H, BLUE, 0.5)
        top = lft(T("filtered: about 10 g of calcium a day", 30, BLUE), x0, 3.0)

        rule = T("the rule", 26, GOLD).move_to([5.0 - 0.6, 3.1, 0])
        self.at("Keep the rule")
        self.play(FadeIn(rule), run_time=0.4)
        self.at("filters about")
        self.play(GrowFromEdge(green, LEFT), FadeIn(orange), FadeIn(top), run_time=1.0)

        gl = T("reabsorbed: about 98 percent", 28, TEXT).move_to(green)
        ul = rgt(T("calcium lost in urine", 26, ORANGE), x0 + W, y + H / 2 + 0.7)
        lead = Ln([x0 + W - ow / 2, y + H / 2], [x0 + W - ow / 2, y + H / 2 + 0.45], color=ORANGE, stroke_width=3)
        self.at("reabsorbs about")
        self.play(green.animate.set_fill(GREEN, 0.5), orange.animate.set_fill(ORANGE, 0.95), FadeIn(gl),
                  FadeIn(ul), Create(lead), run_time=0.9)

        bx0 = x0 + gw - W * 0.075
        bw = W * 0.075
        brk = VGroup(Ln([bx0, y - H / 2 - 0.3, 0], [bx0 + bw, y - H / 2 - 0.3, 0], color=PURPLE, stroke_width=5),
                     Ln([bx0, y - H / 2 - 0.3, 0], [bx0, y - H / 2 - 0.1, 0], color=PURPLE, stroke_width=5),
                     Ln([bx0 + bw, y - H / 2 - 0.3, 0], [bx0 + bw, y - H / 2 - 0.1, 0], color=PURPLE, stroke_width=5))
        d1 = T("distal step: PTH regulates", 28, PURPLE).move_to([3.0, -1.5, 0])
        lead2 = Ln([bx0 + bw / 2, y - H / 2 - 0.3], [bx0 + bw / 2, -1.15], color=PURPLE, stroke_width=3)
        self.at("distal step")
        self.play(Create(brk), Create(lead2), FadeIn(d1), run_time=0.8)
        d2 = T("under a tenth of the load", 28, TEXT).move_to([3.0, -2.3, 0])
        self.at("handles under")
        self.play(FadeIn(d2, shift=UP * 0.1), run_time=0.6)

        wide = rect(x0 + W * (1 - FE2), W * FE2, y, H, ORANGE, 0.95)
        green2 = rect(x0, W * (1 - FE2), y, H, GREEN, 0.5)
        self.at("small change")
        self.play(Indicate(brk, color=PURPLE, scale_factor=1.15), run_time=0.7)
        self.play(Transform(orange, wide), Transform(green, green2), FadeOut(gl), run_time=0.9)
        fin = T("sets the daily calcium lost", 30, ORANGE, weight=BOLD).move_to([-1.0, -3.2, 0])
        self.at("daily calcium lost")
        self.play(FadeIn(fin, shift=UP * 0.15), Indicate(orange, color=ORANGE, scale_factor=1.4), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "The small distal step that PTH regulates sets daily calcium loss."
