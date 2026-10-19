"""Emotion and stress: one source, two separate outputs  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the tone (conditioned stimulus)
  GOLD   = the shock (unconditioned stimulus)
  BLUE   = freezing (the response, its bars, and the route once the lesion result names it)
  ORANGE = the pressure rise (the response, its bars, and the route once the lesion result names it)
  TEAL   = amygdala boxes (lateral and central)
  PURPLE = the two route boxes below the central amygdala (until a lesion names what each carries)
  RED    = a lesion (the X)
  GREY   = unpaired control, frames, axes, and every unanswered or unmeasured thing (dashed)
  PINK   = people (patient SM, the panic dots)
  TEXT   = the learned difference and the claims

All rat numbers are the lesson's invented numbers (worked problem), laid out in the design of the
1988 study; they are not that study's data.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def nbox(text, color=BLUE, size=26, pad=0.2, dashed=False, min_w=0.0, min_h=0.0, fill=0.16):
    """A labelled box with an opaque backing. `text` may hold line breaks. Children: back, rect, label."""
    lines = VGroup(*[T(l, size, color if not dashed else GREY) for l in text.split("\n")]).arrange(DOWN, buff=0.07)
    w = max(lines.width + 2 * pad, min_w)
    h = max(lines.height + 2 * pad, min_h)
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    if dashed:
        rect = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=GREY,
                                               stroke_width=3), num_dashes=44)
    else:
        rect = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                                fill_color=color, fill_opacity=fill)
    lines.move_to(back)
    return VGroup(back, rect, lines)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def darr(a, b, color=GREY, w=4):
    """dashed arrow: the link is a question, not a result."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    line = DashedLine(a, b - d * 0.15, dash_length=0.14, color=color, stroke_width=w)
    perp = np.array([-d[1], d[0], 0])
    head = Polygon(b, b - d * 0.26 + perp * 0.13, b - d * 0.26 - perp * 0.13, stroke_width=0,
                   fill_color=color, fill_opacity=1)
    return VGroup(line, head)


def edge(src, dst, side_a="r", side_b="l"):
    """arrow between two nbox groups (box rect is child 1)."""
    pa = {"r": src[1].get_right(), "l": src[1].get_left(), "u": src[1].get_top(), "d": src[1].get_bottom()}[side_a]
    pb = {"r": dst[1].get_right(), "l": dst[1].get_left(), "u": dst[1].get_top(), "d": dst[1].get_bottom()}[side_b]
    return arr(pa, pb)


def sine(cx, cy, w, amp=0.17, cycles=3.5, color=YELLOW, sw=4):
    k = cycles * 2 * np.pi / w
    return ParametricFunction(lambda t: np.array([cx - w / 2 + t, cy + amp * np.sin(k * t), 0]),
                              t_range=[0, w], color=color, stroke_width=sw)


def zig(cx, cy, w, color=GOLD, sw=4):
    pts = [[-0.5, 0.18], [-0.2, -0.18], [0.05, 0.18], [0.3, -0.18], [0.5, 0.18]]
    return VMobject(color=color, stroke_width=sw).set_points_as_corners(
        [np.array([cx + p[0] * w, cy + p[1], 0]) for p in pts])


def tone_block(cx, cy, w=2.0, h=0.7):
    r = Rectangle(width=w, height=h, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.18)
    r.move_to([cx, cy, 0])
    return VGroup(r, sine(cx, cy, w * 0.8))


def shock_block(cx, cy, w=0.9, h=0.7):
    r = Rectangle(width=w, height=h, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.3)
    r.move_to([cx, cy, 0])
    return VGroup(r, zig(cx, cy, w * 0.8))


def xmark(box, color=RED, w=9, pad=0.12):
    r = box[1]
    x0, x1, y0, y1 = r.get_left()[0] + pad, r.get_right()[0] - pad, r.get_bottom()[1] + pad, r.get_top()[1] - pad
    return VGroup(Line([x0, y0, 0], [x1, y1, 0], color=color, stroke_width=w),
                  Line([x0, y1, 0], [x1, y0, 0], color=color, stroke_width=w))


def lesion_badge(box):
    """a red badge with a white cross on the box's top-right corner (the box label stays readable)."""
    c = box[1].get_corner(UR)
    disc = Circle(radius=0.24, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(c)
    k = 0.11
    cr = VGroup(Line(c + [-k, -k, 0], c + [k, k, 0], color=WHITE, stroke_width=5),
                Line(c + [-k, k, 0], c + [k, -k, 0], color=WHITE, stroke_width=5))
    return VGroup(disc, cr)


def hit(box, on=True, base=PURPLE):
    """animations: tint a box red (lesioned) or back to its colour."""
    if on:
        return box[1].animate.set_stroke(RED).set_fill(RED, 0.4)
    return box[1].animate.set_stroke(base).set_fill(base, 0.16)


def circuit(layout):
    """The rat circuit. layout 'wide' (scene 3) or 'compact' (scenes 4 and 5): same boxes, new places.
    Returns dict of boxes; arrows are built by circuit_arrows."""
    if layout == "wide":
        sz = 24
        pos = dict(tone=(-5.6, 0), la=(-3.45, 0), cea=(-0.9, 0), lh=(2.1, 1.65), pag=(2.1, -1.65))
    else:
        sz = 22
        pos = dict(tone=(-4.2, 3.1), la=(-4.2, 1.7), cea=(-4.2, 0.25), lh=(-5.05, -1.4), pag=(-2.3, -1.4))
    b = dict(
        tone=nbox("tone", YELLOW, sz, fill=0.18),
        la=nbox("lateral\namygdala", TEAL, sz),
        cea=nbox("central\namygdala", TEAL, sz),
        lh=nbox("lateral\nhypothalamus", PURPLE, sz),
        pag=nbox("caudal\nperiaqueductal\ngray", PURPLE, sz),
    )
    if layout != "wide":
        for k, t, col in (("tone", "tone", YELLOW), ("la", "lateral\namygdala", TEAL), ("cea", "central\namygdala", TEAL),
                          ("lh", "lateral\nhypothalamus", PURPLE), ("pag", "caudal\nperiaqueductal\ngray", PURPLE)):
            b[k] = nbox(t, col, sz, pad=0.12, fill=0.18 if k == "tone" else 0.16)
    for k, (x, y) in pos.items():
        b[k].move_to([x, y, 0])
    return b


def circuit_arrows(b, layout):
    if layout == "wide":
        return VGroup(edge(b["tone"], b["la"]), edge(b["la"], b["cea"]),
                      edge(b["cea"], b["lh"]), edge(b["cea"], b["pag"]))
    return VGroup(edge(b["tone"], b["la"], "d", "u"), edge(b["la"], b["cea"], "d", "u"),
                  edge(b["cea"], b["lh"], "d", "u"), edge(b["cea"], b["pag"], "d", "u"))


def sq_legend(color, text, size=22):
    sw = Square(0.26, stroke_color=color, fill_color=color, fill_opacity=0.6, stroke_width=3)
    return VGroup(sw, T(text, size, TEXT).next_to(sw, RIGHT, buff=0.15))


def routes_question(b):
    """the two response chips, the four dashed question links and the big question mark (scene 3, rebuilt in 4)."""
    freeze = nbox("freezing", BLUE, 26, min_w=1.9, min_h=0.9).move_to([5.3, 0.85, 0])
    press = nbox("pressure\nrise", ORANGE, 26, min_w=1.9, min_h=0.9).move_to([5.3, -0.85, 0])
    links = VGroup()
    for r in ("lh", "pag"):
        for t in (freeze, press):
            links.add(darr(b[r][1].get_right(), t[1].get_left()))
    qq = T("?", 56, YELLOW, weight=BOLD).move_to([3.85, 0, 0])
    return freeze, press, links, qq


# bar geometry shared by scenes 4 and 5: share of the learned response kept
CH_BASE = -1.9
CH_SC = 0.034            # scene units per percentage point
CH_AX = -0.3             # x of the y axis
CH_X = [1.2, 3.4, 5.6]   # group centres
CH_DX = 0.45


def share_axes():
    ax = VGroup(Line([CH_AX, CH_BASE, 0], [CH_AX, CH_BASE + 100 * CH_SC, 0], color=GREY, stroke_width=3),
                Line([CH_AX, CH_BASE, 0], [6.3, CH_BASE, 0], color=GREY, stroke_width=3))
    for v in (0, 50, 100):
        ax.add(M(str(v), 22, GREY).move_to([CH_AX - 0.32, CH_BASE + v * CH_SC, 0]))
    full = DashedLine([CH_AX, CH_BASE + 100 * CH_SC, 0], [6.3, CH_BASE + 100 * CH_SC, 0], dash_length=0.14,
                      color=GREY, stroke_width=2)
    title = T("Share of what was learned that is left (%)", 24, TEXT).move_to([3.0, 3.4, 0])
    tag = T("invented numbers, not the study's data", 22, GREY).move_to([3.0, 3.0, 0])
    return VGroup(ax, full, title, tag)


GROUP_LABEL = ["lateral\nhypothalamus", "caudal\nPAG", "central\namygdala"]


def group_labels():
    out = VGroup()
    for i, t in enumerate(GROUP_LABEL):
        lab = VGroup(*[T(l, 22, GREY) for l in t.split("\n")]).arrange(DOWN, buff=0.05)
        lab.move_to([CH_X[i], CH_BASE - 0.55, 0])
        out.add(lab)
    return out


def share_legend():
    a, b = sq_legend(BLUE, "freezing"), sq_legend(ORANGE, "pressure rise")
    return VGroup(a, b).arrange(RIGHT, buff=0.6).move_to([3.0, -3.45, 0])


def share_bar(g, which, value, label=None):
    """which 0 freezing (blue), 1 pressure (orange). Returns (bar, value label)."""
    col = BLUE if which == 0 else ORANGE
    x = CH_X[g] + (-CH_DX if which == 0 else CH_DX)
    h = max(value * CH_SC, 0.02)
    bar = Rectangle(width=0.8, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.6)
    bar.move_to([x, CH_BASE + h / 2, 0])
    txt = label if label is not None else f"{value}%"
    lab = M(txt, 22, TEXT).move_to([x, CH_BASE + h + 0.3, 0])
    lab.set_stroke(BG, width=8, background=True)
    return bar, lab


def work_lines(a, b):
    la = M(a, 22, BLUE).move_to([3.0, 2.55, 0])
    lb = M(b, 22, ORANGE).move_to([3.0, 2.15, 0])
    return VGroup(la, lb)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Emotion and stress"
    TITLE = "One source, two separate outputs"


# ---------------------------------------------------------------------------------------------
class S01Tone(SpokenScene):
    """training: tone then shock; test: tone -> rat -> freezing and pressure rise; is one pathway behind both?"""

    def construct(self):
        # training row (small, top)
        lab = T("training", 24, GREY).move_to([-5.2, 3.0, 0])
        tone = tone_block(-3.0, 3.0, 2.2)
        tone_l = T("tone", 22, YELLOW).next_to(tone, DOWN, buff=0.08)
        shock = shock_block(-1.35, 3.0)
        shock_l = T("shock", 22, GOLD).next_to(shock, DOWN, buff=0.08)
        self.at("hears a tone")
        self.play(FadeIn(lab), FadeIn(tone, shift=RIGHT * 0.2), FadeIn(tone_l), run_time=0.6)
        self.at("mild shock")
        self.play(FadeIn(shock, shift=RIGHT * 0.2), FadeIn(shock_l), run_time=0.5)

        # test row
        t_tone = tone_block(-5.3, -0.5, 1.9, 0.9)
        t_tl = T("tone", 22, YELLOW).next_to(t_tone, DOWN, buff=0.08)
        rat = nbox("rat", GREY, 32, min_w=1.3, min_h=1.0).move_to([-3.1, -0.5, 0])
        rat[1].set_stroke(TEXT).set_fill(TEXT, 0.1)
        rat[2].set_color(TEXT)
        freeze = nbox("freezing", BLUE, 30, min_w=2.5, min_h=0.95).move_to([3.0, 0.7, 0])
        press = nbox("pressure rise", ORANGE, 30, min_w=2.5, min_h=0.95).move_to([3.0, -1.7, 0])
        a_tr = arr(t_tone[0].get_right(), rat[1].get_left())
        a_rf = arr(rat[1].get_right(), freeze[1].get_left())
        a_rp = arr(rat[1].get_right(), press[1].get_left())
        self.at("it freezes")
        self.play(FadeIn(t_tone), FadeIn(t_tl), run_time=0.4)
        self.play(GrowArrow(a_tr), FadeIn(rat), run_time=0.4)
        self.play(GrowArrow(a_rf), FadeIn(freeze, shift=RIGHT * 0.2), run_time=0.5)
        self.at("pressure rises")
        self.play(GrowArrow(a_rp), FadeIn(press, shift=RIGHT * 0.2), run_time=0.5)

        # one pathway? a question box between the rat and both responses
        q = nbox("?", YELLOW, 52, min_w=1.2, min_h=1.2, fill=0.12).move_to([-0.55, -0.5, 0])
        q_cap = T("one pathway?", 24, YELLOW).next_to(q, UP, buff=0.18)
        b1 = arr(rat[1].get_right(), q[1].get_left())
        b2 = arr(q[1].get_right() + UP * 0.25, freeze[1].get_left())
        b3 = arr(q[1].get_right() + DOWN * 0.25, press[1].get_left())
        self.at("one pathway")
        self.play(FadeOut(a_rf), FadeOut(a_rp), run_time=0.3)
        self.play(FadeIn(q, scale=0.8), FadeIn(q_cap), GrowArrow(b1), GrowArrow(b2), GrowArrow(b3), run_time=0.6)

        # neither response is the feeling of fear; both can be measured
        feel = nbox("feeling of fear", GREY, 28, dashed=True, min_w=3.1).move_to([3.0, -3.3, 0])
        self.at("feeling of fear")
        self.play(FadeIn(feel, shift=UP * 0.15), run_time=0.5)
        br = Brace(VGroup(freeze, press), RIGHT, color=TEXT, buff=0.2)
        meas = T("measured", 24, TEXT).next_to(br, RIGHT, buff=0.12)
        self.at("both can be measured")
        self.play(GrowFromCenter(br), FadeIn(meas), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Learned(SpokenScene):
    """paired vs unpaired timelines, then freezing and pressure bars with the learned difference."""

    def construct(self):
        # --- timelines ---------------------------------------------------------------------
        def row(y, shocks, name, col):
            nm = T(name, 28, col, weight=BOLD)
            nm.move_to([-6.1 + nm.width / 2, y + 0.95, 0])
            axis = Line([-6.1, y - 0.55, 0], [6.2, y - 0.55, 0], color=GREY, stroke_width=2)
            g = VGroup(nm, axis)
            for k in range(3):
                g.add(tone_block(-5.0 + k * 4.0, y, 1.8, 0.8))
            for sx in shocks:
                g.add(shock_block(sx, y, 0.7, 0.8))
            return g

        paired = row(1.5, [-3.65, 0.35, 4.35], "paired group", BLUE)
        unpaired = row(-1.2, [-2.9, 1.4, 5.6], "unpaired control", GREY)
        ask = T("Is the response learned?", 38, TEXT).move_to([0, 0.2, 0])
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.6)
        self.at("One group of rats")
        self.play(FadeOut(ask), FadeIn(paired, shift=RIGHT * 0.2), run_time=0.9)
        self.at("A control group")
        self.play(FadeIn(unpaired, shift=RIGHT * 0.2), run_time=0.9)
        cap = T("only the difference is learning", 30, TEXT).move_to([0, -3.0, 0])
        self.at("only the difference")
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)

        # --- charts ------------------------------------------------------------------------
        tag = T("invented numbers, not the study's data", 22, GREY).move_to([0, 3.5, 0])
        self.at("In invented numbers")
        self.play(FadeOut(paired), FadeOut(unpaired), FadeOut(cap), FadeIn(tag), run_time=0.6)

        base = -2.2

        def chart(ax_x, unit, ticks, top, title, col, xs):
            sc = 4.0 / top
            ax = VGroup(Line([ax_x, base, 0], [ax_x, base + top * sc, 0], color=GREY, stroke_width=3),
                        Line([ax_x, base, 0], [ax_x + 5.0, base, 0], color=GREY, stroke_width=3))
            for v in ticks:
                ax.add(M(str(v), 22, GREY).move_to([ax_x - 0.34, base + v * sc, 0]))
            ttl = T(title, 24, col).move_to([ax_x + 2.6, 2.45, 0])
            xl = VGroup(T("unpaired", 22, GREY).move_to([xs[0], base - 0.32, 0]),
                        T("paired", 22, col).move_to([xs[1], base - 0.32, 0]))
            return sc, VGroup(ax, ttl, xl)

        xsA, xsB = [-4.5, -2.9], [1.6, 3.3]
        scA, axA = chart(-5.6, "%", (0, 50, 100), 100, "Freezing (% of the tone)", BLUE, xsA)
        scB, axB = chart(0.4, "mmHg", (0, 10, 20), 25, "Pressure rise (mmHg)", ORANGE, xsB)

        def bar(x, v, sc, col, lab):
            h = max(v * sc, 0.02)
            b = Rectangle(width=1.0, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.6)
            b.move_to([x, base + h / 2, 0])
            return b, M(lab, 24, TEXT).move_to([x, base + h + 0.3, 0])

        def diff(xr, v_lo, v_hi, sc, text, xl):
            """dashed line at the unpaired top, brace beside the paired bar, label."""
            y_lo, y_hi = base + v_lo * sc, base + v_hi * sc
            dl = DashedLine([xl, y_lo, 0], [xr + 0.55, y_lo, 0], dash_length=0.12, color=TEXT, stroke_width=2)
            br = Brace(Line([xr + 0.6, y_lo, 0], [xr + 0.6, y_hi, 0]), RIGHT, color=TEXT, buff=0.04)
            lb = T(text, 24, TEXT).next_to(br, RIGHT, buff=0.1)
            return VGroup(dl, br, lb)

        self.play(FadeIn(axA), FadeIn(axB), run_time=0.6)
        pA, lpA = bar(xsA[1], 60, scA, BLUE, "60")
        uA, luA = bar(xsA[0], 8, scA, GREY, "8")
        self.at("paired rats froze")
        self.play(GrowFromEdge(pA, DOWN), FadeIn(lpA), run_time=0.6)
        self.at("and unpaired rats")
        self.play(GrowFromEdge(uA, DOWN), FadeIn(luA), run_time=0.5)
        dA = diff(xsA[1], 8, 60, scA, "52 points", xsA[0] + 0.5)
        self.at("learned difference")
        self.play(Create(dA[0]), GrowFromCenter(dA[1]), FadeIn(dA[2]), run_time=0.7)

        pB, lpB = bar(xsB[1], 20, scB, ORANGE, "20")
        uB, luB = bar(xsB[0], 3, scB, GREY, "3")
        self.at("Pressure rose")
        self.play(GrowFromEdge(pB, DOWN), FadeIn(lpB), run_time=0.6)
        self.at("in unpaired rats")
        self.play(GrowFromEdge(uB, DOWN), FadeIn(luB), run_time=0.5)
        dB = diff(xsB[1], 3, 20, scB, "17 mmHg", xsB[0] + 0.5)
        self.at("learned difference", nth=1)
        self.play(Create(dB[0]), GrowFromCenter(dB[1]), FadeIn(dB[2]), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Routes(SpokenScene):
    """the rat circuit: tone -> lateral amygdala -> central amygdala -> two routes; which carries which response?"""

    def construct(self):
        b = circuit("wide")
        arrows = circuit_arrows(b, "wide")
        tag = T("in the rat", 26, GREY).move_to([-5.2, 3.2, 0])
        self.at("the rat")
        self.play(FadeIn(tag), run_time=0.3)
        self.at("the tone reaches")
        self.play(FadeIn(b["tone"]), GrowArrow(arrows[0]), FadeIn(b["la"], shift=RIGHT * 0.2), run_time=0.8)
        inp = T("input stage", 22, TEAL).next_to(b["la"], DOWN, buff=0.18)
        self.at("input stage")
        self.play(FadeIn(inp), run_time=0.4)
        self.at("central amygdala")
        self.play(GrowArrow(arrows[1]), FadeIn(b["cea"], shift=RIGHT * 0.2), run_time=0.7)
        self.at("lateral hypothalamus")
        self.play(GrowArrow(arrows[2]), FadeIn(b["lh"], shift=RIGHT * 0.2), run_time=0.7)
        self.at("caudal periaqueductal")
        self.play(GrowArrow(arrows[3]), FadeIn(b["pag"], shift=RIGHT * 0.2), run_time=0.7)

        # the question: which route carries which response?
        freeze, press, links, qq = routes_question(b)
        self.at("Which route")
        self.play(FadeIn(freeze), FadeIn(press), run_time=0.4)
        self.play(Create(links), run_time=0.7)
        self.play(FadeIn(qq, scale=1.4), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cut(SpokenScene):
    """circuit moves left; lesion one route at a time; bars of the share of the learned response left."""

    def construct(self):
        # rebuild the end of scene 3
        w = circuit("wide")
        wa = circuit_arrows(w, "wide")
        tag = T("in the rat", 26, GREY).move_to([-5.2, 3.2, 0])
        inp = T("input stage", 22, TEAL).next_to(w["la"], DOWN, buff=0.18)
        freeze, press, links, qq = routes_question(w)
        self.add(*w.values(), wa, tag, inp, freeze, press, links, qq)

        # to the compact layout
        c = circuit("compact")
        ca = circuit_arrows(c, "compact")
        self.at("cut one")
        self.play(FadeOut(wa), FadeOut(tag), FadeOut(inp), FadeOut(freeze), FadeOut(press), FadeOut(links),
                  FadeOut(qq), run_time=0.4)
        self.play(*[w[k].animate.scale(22 / 24).move_to(c[k].get_center()) for k in w], run_time=0.9)
        # swap to the exact compact boxes (same place) so the labels are the smaller size
        self.remove(*w.values())
        self.add(*c.values())
        self.play(FadeIn(ca), run_time=0.3)

        axes = share_axes()
        labs = group_labels()
        leg = share_legend()
        self.play(FadeIn(axes), FadeIn(labs), FadeIn(leg), run_time=0.6)

        rule = M("(lesion − unpaired) / learned", 22, GREY).move_to([3.0, 2.35, 0])
        self.at("taking away")
        self.play(FadeIn(rule), run_time=0.4)

        # --- lateral hypothalamus lesion ---------------------------------------------------
        x_lh = lesion_badge(c["lh"])
        wl1 = work_lines("freezing: (57 − 8) / 52 = 94%", "pressure: (4 − 3) / 17 = 6%")
        self.at("the lateral hypothalamus")
        self.play(FadeOut(rule), FadeIn(x_lh, scale=0.5), hit(c["lh"]), run_time=0.5)
        f1, lf1 = share_bar(0, 0, 94)
        p1, lp1 = share_bar(0, 1, 6)
        self.at("freezing keeps")
        self.play(FadeIn(wl1[0]), GrowFromEdge(f1, DOWN), FadeIn(lf1), run_time=0.6)
        self.at("pressure rise keeps")
        self.play(FadeIn(wl1[1]), GrowFromEdge(p1, DOWN), FadeIn(lp1), run_time=0.5)

        # --- caudal PAG lesion: clear the old working and the old X first ------------------
        x_pag = lesion_badge(c["pag"])
        wl2 = work_lines("freezing: (9 − 8) / 52 = 2%", "pressure: (19 − 3) / 17 = 94%")
        self.at("caudal periaqueductal")
        self.play(FadeOut(x_lh), FadeOut(wl1), hit(c["lh"], False),
                  FadeIn(x_pag, scale=0.5), hit(c["pag"]), run_time=0.6)
        f2, lf2 = share_bar(1, 0, 2)
        p2, lp2 = share_bar(1, 1, 94)
        self.at("Freezing keeps", nth=1)
        self.play(FadeIn(wl2[0]), GrowFromEdge(f2, DOWN), FadeIn(lf2), run_time=0.6)
        self.at("pressure keeps")
        self.play(FadeIn(wl2[1]), GrowFromEdge(p2, DOWN), FadeIn(lp2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Dissociation(SpokenScene):
    """central amygdala lesion removes both; the double dissociation; it says nothing yet about a feeling."""

    def construct(self):
        # rebuild the end of scene 4
        c = circuit("compact")
        ca = circuit_arrows(c, "compact")
        axes, labs, leg = share_axes(), group_labels(), share_legend()
        f1, lf1 = share_bar(0, 0, 94)
        p1, lp1 = share_bar(0, 1, 6)
        f2, lf2 = share_bar(1, 0, 2)
        p2, lp2 = share_bar(1, 1, 94)
        x_pag = lesion_badge(c["pag"])
        c["pag"][1].set_stroke(RED).set_fill(RED, 0.4)
        wl2 = work_lines("freezing: (9 − 8) / 52 = 2%", "pressure: (19 − 3) / 17 = 94%")
        self.add(*c.values(), ca, axes, labs, leg, f1, lf1, p1, lp1, f2, lf2, p2, lp2, x_pag, wl2)

        # --- central amygdala lesion: clear the old X and working in the same beat ---------
        x_cea = lesion_badge(c["cea"])
        wl3 = work_lines("freezing: (6 − 8) / 52, about 0%", "pressure: (3 − 3) / 17 = 0%")
        self.at("Lesion the central")
        self.play(FadeOut(x_pag), FadeOut(wl2), hit(c["pag"], False),
                  FadeIn(x_cea, scale=0.5), hit(c["cea"]), run_time=0.6)
        f3, lf3 = share_bar(2, 0, 0)
        p3, lp3 = share_bar(2, 1, 0, "0%")
        self.play(FadeIn(wl3[0]), FadeIn(wl3[1]), FadeIn(f3), FadeIn(lf3), FadeIn(p3), FadeIn(lp3), run_time=0.7)

        # --- each output lesion removed one and kept the other -----------------------------
        self.play(FadeOut(x_cea), FadeOut(wl3), hit(c["cea"], False, TEAL), run_time=0.4)
        fr1 = SurroundingRectangle(VGroup(f1, p1, lf1, lp1), color=TEXT, buff=0.12, stroke_width=2)
        fr2 = SurroundingRectangle(VGroup(f2, p2, lf2, lp2), color=TEXT, buff=0.12, stroke_width=2)
        tag_h = T("pressure route", 22, ORANGE).next_to(c["lh"], DOWN, buff=0.15)
        tag_p = T("freezing route", 22, BLUE).next_to(c["pag"], DOWN, buff=0.15)
        self.at("Each output lesion")
        self.play(Create(fr1), run_time=0.5)
        self.play(Create(fr2), run_time=0.5)

        dd = nbox("double dissociation", TEXT, 28, min_w=3.6).move_to([-3.9, -3.2, 0])
        dd[1].set_stroke(TEXT).set_fill(TEXT, 0.08)
        self.at("double dissociation")
        self.play(FadeIn(dd, shift=UP * 0.1), run_time=0.5)

        self.at("two separate routes")
        self.play(c["lh"][1].animate.set_stroke(ORANGE).set_fill(ORANGE, 0.16),
                  c["pag"][1].animate.set_stroke(BLUE).set_fill(BLUE, 0.16),
                  FadeIn(tag_h), FadeIn(tag_p), Indicate(ca[2], color=TEXT), Indicate(ca[3], color=TEXT),
                  run_time=0.8)
        self.at("locates the outputs")
        self.play(FadeOut(fr1), FadeOut(fr2), Indicate(c["lh"], color=ORANGE), Indicate(c["pag"], color=BLUE),
                  run_time=0.8)

        feel = nbox("a feeling?", GREY, 28, dashed=True, min_w=3.6).move_to([-3.9, -3.2, 0])
        self.at("nothing yet")
        self.play(FadeOut(dd), FadeIn(feel, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Feeling(SpokenScene):
    """SM and the CO2 breath (people), then what rat work can and cannot say."""

    def construct(self):
        # --- row 1: SM, minimal fear, external threats ---------------------------------------
        a = nbox("patient SM:\ndamage to both\namygdalae", PINK, 26, min_w=3.0).move_to([-4.3, 2.4, 0])
        cx = nbox("at most\nminimal fear", PINK, 26, min_w=3.0).move_to([4.3, 2.4, 0])
        bx = nbox("external threats\ntested", GREY, 26, min_w=3.0).move_to([0, 2.4, 0])
        r1 = arr(a[1].get_right(), cx[1].get_left())
        self.at("Patient SM")
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.6)
        self.at("at most minimal fear")
        self.play(GrowArrow(r1), FadeIn(cx, shift=RIGHT * 0.2), run_time=0.6)
        self.at("external threats")
        self.play(FadeIn(bx, scale=0.9), run_time=0.5)

        # --- row 2: one breath of 35% CO2 ----------------------------------------------------
        co2 = nbox("one breath of\n35% CO2", GREY, 26, min_w=3.0, min_h=1.3).move_to([-4.6, -1.3, 0])

        def dots(n, k, x0, y0, per_row):
            g = VGroup()
            for i in range(n):
                r, ci = divmod(i, per_row)
                d = Circle(radius=0.26, stroke_width=3)
                if i < k:
                    d.set_stroke(PINK).set_fill(PINK, 0.9)
                else:
                    d.set_stroke(GREY).set_fill(GREY, 0.0)
                d.move_to([x0 + ci * 0.7, y0 - r * 0.7, 0])
                g.add(d)
            return g

        def left(t, x, y):
            t.move_to([x + t.width / 2, y, 0])
            return t

        labA = left(T("damage to both amygdalae", 24, PINK), -2.4, 0.1)
        dotsA = dots(3, 3, -2.1, -0.45, 6)
        cntA = left(T("3 of 3 panicked", 26, TEXT), 0.3, -0.45)
        labB = left(T("comparison women", 24, GREY), -2.4, -1.45)
        dotsB = dots(12, 3, -2.1, -2.0, 6)
        cntB = left(T("3 of 12", 26, TEXT), 1.9, -2.35)
        self.at("all panicked", lead=0.0)
        self.play(FadeIn(labA), LaggedStart(*[GrowFromCenter(d) for d in dotsA], lag_ratio=0.25), run_time=0.8)
        self.play(FadeIn(cntA), run_time=0.3)
        self.at("one breath")
        self.play(FadeIn(co2, shift=RIGHT * 0.2), run_time=0.5)
        self.at("Three of twelve")
        self.play(FadeIn(labB), LaggedStart(*[FadeIn(d) for d in dotsB], lag_ratio=0.05), run_time=0.7)
        self.play(FadeIn(cntB), run_time=0.3)
        thr = VGroup(T("the difference lay", 26, TEXT), T("in the threat", 26, TEXT)).arrange(DOWN, buff=0.1)
        thr.move_to([4.7, -1.6, 0])
        self.at("lay in the threat")
        self.play(FadeIn(thr, shift=UP * 0.1), run_time=0.5)

        # --- row 3: rat work ----------------------------------------------------------------
        cea_i = nbox("central\namygdala", TEAL, 28, min_w=2.2, min_h=1.5).move_to([-5.0, 1.3, 0])
        lh = nbox("lateral\nhypothalamus", PURPLE, 26, min_w=2.5, min_h=1.1).move_to([-1.9, 2.05, 0])
        pg = nbox("caudal\nPAG", PURPLE, 26, min_w=2.5, min_h=1.1).move_to([-1.9, 0.55, 0])
        rp = nbox("pressure rise", ORANGE, 26, min_w=2.6, min_h=1.1).move_to([1.7, 2.05, 0])
        rf = nbox("freezing", BLUE, 26, min_w=2.6, min_h=1.1).move_to([1.7, 0.55, 0])
        ch = VGroup(edge(cea_i, lh), edge(cea_i, pg), edge(lh, rp), edge(pg, rf))
        frame = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=9.8, height=3.3, stroke_color=GREY,
                                                stroke_width=2), num_dashes=80).move_to([-1.55, 1.3, 0])
        frame_l = T("in rats, under defined conditions", 24, GREY).move_to([-1.55, 3.2, 0])
        self.at("can find necessary")
        self.play(FadeOut(a), FadeOut(bx), FadeOut(cx), FadeOut(r1), FadeOut(co2), FadeOut(labA), FadeOut(dotsA),
                  FadeOut(cntA), FadeOut(labB), FadeOut(dotsB), FadeOut(cntB), FadeOut(thr), run_time=0.6)
        self.play(FadeIn(cea_i), run_time=0.3)
        self.play(GrowArrow(ch[0]), GrowArrow(ch[1]), FadeIn(lh), FadeIn(pg), run_time=0.5)
        self.play(GrowArrow(ch[2]), GrowArrow(ch[3]), FadeIn(rp), FadeIn(rf), run_time=0.5)
        self.at("under defined conditions")
        self.play(Create(frame), FadeIn(frame_l), run_time=0.7)

        feels = nbox("what the animal\nfeels", GREY, 28, dashed=True, min_w=3.4, min_h=1.3).move_to([-2.3, -2.45, 0])
        human = nbox("a human\nfeeling", GREY, 28, dashed=True, min_w=3.4, min_h=1.3).move_to([3.0, -2.45, 0])
        d1 = darr(rf[1].get_bottom() + LEFT * 0.5, feels[1].get_top() + RIGHT * 0.8)
        d2 = darr(rf[1].get_bottom() + RIGHT * 0.5, human[1].get_top())
        q1 = T("?", 48, YELLOW, weight=BOLD).move_to([0.0, -1.0, 0])
        q2 = T("?", 48, YELLOW, weight=BOLD).move_to([3.0, -1.0, 0])
        self.at("cannot say what")
        self.play(Create(d1), FadeIn(feels), FadeIn(q1), run_time=0.7)
        self.at("human feeling")
        self.play(Create(d2), FadeIn(human), FadeIn(q2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Rat work finds necessary steps for a response, not a feeling."
