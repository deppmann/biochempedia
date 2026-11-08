"""Adrenal glands: an enzyme guards the receptor  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = aldosterone
  PURPLE = cortisol (and corticosterone, its rat counterpart)
  BLUE   = the mineralocorticoid receptor
  GREEN  = the guard enzyme, 11-beta-HSD (when working)
  RED    = the enzyme switched off
  ORANGE = liquorice and its inhibitor, glycyrrhetinic acid
  TEAL   = sodium (ions, tracer, sodium transport)
  GREY   = cortisone (inactive), chambers, membranes, de-emphasized notes
Every shape is a labelled block, ring or dot: no molecular structures. Dots are schematic and
not to scale.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

RX = -4.6          # receptor centre x
SX = -4.0          # socket centre x (on the receptor's right edge)
EX = -1.9          # enzyme centre x


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def dot(color, r=0.18, x=0.0, y=0.0):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).move_to([x, y, 0])


def route(mob, pts, run_time):
    path = VMobject().set_points_smoothly([np.array([p[0], p[1], 0.0]) for p in pts])
    return MoveAlongPath(mob, path, run_time=run_time, rate_func=smooth)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def receptor(label="mineralocorticoid\nreceptor"):
    """tall blue block with a round socket bitten into its right edge; returns (body, ring, label)."""
    body = Difference(RoundedRectangle(corner_radius=0.2, width=1.2, height=3.6).move_to([RX, 0, 0]),
                      Circle(radius=0.36).move_to([SX, 0, 0]),
                      stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3)
    ring = Circle(radius=0.36, stroke_color=BLUE, stroke_width=4).move_to([SX, 0, 0])
    lbl = T(label, 22, BLUE, line_spacing=0.8).move_to([RX, -2.4, 0])
    return body, ring, lbl


def enzyme(color=GREEN):
    """green block with a round mouth on its right edge, labelled 11-beta-HSD; returns (body, mouth ring, label)."""
    body = Difference(RoundedRectangle(corner_radius=0.2, width=1.9, height=2.2).move_to([EX, 0, 0]),
                      Circle(radius=0.34).move_to([EX + 0.95, 0, 0]),
                      stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    ring = Circle(radius=0.34, stroke_color=color, stroke_width=3).move_to([EX + 0.95, 0, 0])
    lbl = T("11-beta\nHSD", 22, color, line_spacing=0.8).move_to([EX - 0.2, 0, 0])
    return body, ring, lbl


def unknown_box():
    box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=1.9, height=2.2).move_to([EX, 0, 0]),
                         num_dashes=36).set_color(GREY).set_stroke(width=4)
    q = T("?", 64, GREY, weight=BOLD).move_to([EX, 0, 0])
    return VGroup(box, q)


def tissue_box(label):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=5.9, height=5.2).move_to([-3.4, -0.3, 0]),
                         num_dashes=90).set_color(GREY).set_stroke(width=3)
    lb = T(label, 22, GREY).move_to([-3.4, -3.25, 0])
    return box, lb


def crowd(n_cols=4, n_rows=8):
    """cortisol crowd: dots on a grid at the right of the enzyme. Returns list of columns, each a list of dots."""
    cols = []
    for i in range(n_cols):
        cols.append([dot(PURPLE, 0.16, 0.3 + 0.42 * i, -1.47 + 0.42 * k) for k in range(n_rows)])
    return cols


def flat(cols):
    return VGroup(*[d for c in cols for d in c])


def ald_dot():
    return dot(YELLOW, 0.18, 0.3, 1.89)


def tag(text, color, size=24):
    return T(text, size, color)


def ald_label(ald):
    """'aldosterone' label that stays beside its dot."""
    lb = T("aldosterone", 24, YELLOW)
    lb.add_updater(lambda m: m.next_to(ald, RIGHT, buff=0.15))
    lb.next_to(ald, RIGHT, buff=0.15)
    return lb


class S00Title(TitleCard):
    LESSON = "The Adrenal Cortex and Medulla"
    TITLE = "An Enzyme Guards the Receptor"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """the receptor takes both steroids equally, cortisol vastly outnumbers aldosterone, sodium transport follows aldosterone: ?"""

    def construct(self):
        body, ring, lbl = receptor("aldosterone\nreceptor")
        self.play(FadeIn(body), FadeIn(ring), FadeIn(lbl), run_time=0.6)

        # --- cortisol docks, then aldosterone docks: the same grip ----------------------------
        c = dot(PURPLE, 0.2, -1.2, 0)
        ctag = tag("cortisol", PURPLE).move_to([-3.2, 0.75, 0])
        self.at("binds cortisol")
        self.play(FadeIn(c), run_time=0.2)
        self.play(route(c, [(-1.2, 0), (-2.6, 0), (SX, 0)], 0.7), ring.animate.set_stroke(PURPLE), FadeIn(ctag), run_time=0.7)
        a = dot(YELLOW, 0.2, -1.2, 0)
        atag = tag("aldosterone", YELLOW).move_to([-2.7, 0.75, 0])
        self.at("it binds aldosterone")
        self.play(c.animate.move_to([-1.2, 0, 0]).set_opacity(0), FadeOut(ctag), ring.animate.set_stroke(BLUE), run_time=0.5)
        self.play(FadeIn(a), run_time=0.15)
        self.play(route(a, [(-1.2, 0), (-2.6, 0), (SX, 0)], 0.7), ring.animate.set_stroke(YELLOW), FadeIn(atag), run_time=0.7)

        # --- far more cortisol -------------------------------------------------------------------
        cols = crowd()
        allc = flat(cols)
        ald = ald_dot()
        c_lbl = tag("cortisol", PURPLE).move_to([0.95, -2.1, 0])
        a_lbl = ald_label(ald)
        self.at("far more cortisol")
        self.play(FadeOut(a), FadeOut(atag), ring.animate.set_stroke(BLUE),
                  LaggedStart(*[FadeIn(d, scale=0.5) for d in allc], lag_ratio=0.03), FadeIn(c_lbl), run_time=1.4)
        self.play(FadeIn(ald, scale=0.5), FadeIn(a_lbl), run_time=0.4)

        ex1 = T("a hundredfold\nmolar excess", 26, TEXT, line_spacing=0.8).move_to([4.7, 1.2, 0])
        ex2 = T("a commonly\ncited figure", 22, GREY, line_spacing=0.8).move_to([4.7, 0.2, 0])
        ex3 = T("not to scale", 22, GREY).move_to([4.7, -0.55, 0])
        self.at("molar excess")
        self.play(FadeIn(ex1, shift=LEFT * 0.2), run_time=0.5)
        self.at("commonly cited figure")
        self.play(FadeIn(ex2), FadeIn(ex3), run_time=0.4)

        # --- sodium transport follows aldosterone ----------------------------------------------
        chip_a = chip("aldosterone", YELLOW, size=24, pad=0.16).move_to([4.7, -1.5, 0])
        chip_n = chip("sodium transport", TEAL, size=24, pad=0.16).move_to([4.7, -3.0, 0])
        a_arr = arr(chip_a.get_bottom(), chip_n.get_top(), TEAL)
        self.at("sodium transport")
        self.play(FadeIn(chip_n, shift=UP * 0.15), run_time=0.5)
        self.at("follows aldosterone")
        self.play(FadeIn(chip_a, shift=DOWN * 0.15), GrowArrow(a_arr), run_time=0.6)

        # --- the answer: an unknown box beside the receptor ------------------------------------
        q = unknown_box()
        q_lbl = tag("an enzyme?", GREY).move_to([EX, -1.65, 0])
        self.at("answer is")
        self.play(Create(q[0]), FadeIn(q[1]), run_time=0.7)
        self.at("beside the receptor")
        self.play(FadeIn(q_lbl), Indicate(body, color=BLUE, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Bladder(SpokenScene):
    """Crabbé's paired toad-bladder halves: aldosterone on one half; its current rises after about one hour."""

    def construct(self):
        def row(yr):
            left = Rectangle(width=2.6, height=1.9, stroke_color=GREY, stroke_width=3).move_to([-5.0, yr, 0])
            right = Rectangle(width=2.6, height=1.9, stroke_color=GREY, stroke_width=3).move_to([-2.1, yr, 0])
            sheet = Rectangle(width=0.18, height=1.9, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([-3.55, yr, 0])
            ltxt = T("urine side", 22, GREY).move_to([-5.0, yr + 0.62, 0])
            rtxt = T("blood side", 22, GREY).move_to([-2.1, yr + 0.62, 0])
            na = arr([-5.7, yr - 0.25, 0], [-2.5, yr - 0.25, 0], TEAL, w=4)
            nat = T("Na⁺", 24, TEAL).move_to([-4.55, yr + 0.1, 0])
            return left, right, sheet, ltxt, rtxt, na, nat

        head0 = T("Jean Crabbé, 1961", 28, font=TITLE_FONT).move_to([-3.5, 3.15, 0])
        self.play(FadeIn(head0, shift=DOWN * 0.1), run_time=0.6)
        head = T("Jean Crabbé, 1961: toad urinary bladder", 28, font=TITLE_FONT).move_to([-0.2, 3.15, 0])
        self.at("urinary bladder")
        r1 = row(1.3)
        self.play(ReplacementTransform(head0, head), *[FadeIn(m) for m in r1[:5]], run_time=0.8)
        self.at("moves sodium")
        self.play(GrowArrow(r1[5]), FadeIn(r1[6]), run_time=0.7)

        # --- paired halves -------------------------------------------------------------------------
        r2 = row(-1.4)
        lab1 = T("control half", 22, GREY).move_to([3.6, 2.0, 0])
        lab2 = T("partner half", 22, GREY).move_to([3.6, -0.7, 0])
        self.at("paired halves")
        self.play(*[FadeIn(m) for m in r2[:5]], GrowArrow(r2[5]), FadeIn(r2[6]), FadeIn(lab1), FadeIn(lab2), run_time=1.0)

        # --- aldosterone to one half -------------------------------------------------------------
        ald = dot(YELLOW, 0.2, -1.4, -0.2)
        ald_t = T("aldosterone", 22, YELLOW).move_to([-0.1, -0.2, 0])
        lab2b = T("aldosterone half", 22, YELLOW).move_to([3.6, -0.7, 0])
        self.at("gave aldosterone")
        self.play(FadeIn(ald, shift=DOWN * 0.3), FadeIn(ald_t), run_time=0.5)
        self.play(ald.animate.move_to([-1.4, -1.7, 0]), ReplacementTransform(lab2, lab2b), run_time=0.6)

        # --- about one hour, then the gauge --------------------------------------------------------
        clock = T("after about one hour", 24, TEXT).move_to([-3.2, -0.02, 0])
        self.at("about one hour")
        self.play(FadeOut(ald_t), FadeIn(clock), run_time=0.4)

        head_g = T("short-circuit current, in this sketch", 22, GREY).move_to([3.6, 2.55, 0])
        tr1 = Rectangle(width=5.2, height=0.5, stroke_color=GREY, stroke_width=3).move_to([3.6, 1.3, 0])
        tr2 = Rectangle(width=5.2, height=0.5, stroke_color=GREY, stroke_width=3).move_to([3.6, -1.4, 0])

        def bar(tr, w, color=TEAL):
            return Rectangle(width=w, height=0.5, stroke_width=0, fill_color=color, fill_opacity=0.8).align_to(tr, LEFT).align_to(tr, UP)

        b1 = bar(tr1, 1.4)
        b2 = bar(tr2, 1.4)
        self.at("short circuit")
        self.play(FadeIn(head_g), FadeIn(tr1), FadeIn(tr2), FadeIn(b1), FadeIn(b2), run_time=0.7)
        b2_big = bar(tr2, 3.7)
        na2_big = arr([-5.7, -1.65, 0], [-2.5, -1.65, 0], TEAL, w=11, tip=0.3)
        self.at("rose above")
        self.play(Transform(b2, b2_big), Transform(r2[5], na2_big), run_time=1.1)

        # --- tracer fluxes: net sodium transport --------------------------------------------------
        trc = T("tracer fluxes in\neight bladders", 22, GREY, line_spacing=0.8).move_to([3.6, -2.45, 0])
        self.at("tracer fluxes")
        self.play(FadeIn(trc), run_time=0.5)
        net = T("extra current = net sodium transport", 22, TEAL).move_to([3.6, -3.45, 0])
        self.at("net sodium transport")
        self.play(FadeIn(net), run_time=0.5)

        # --- direct action on the epithelium ---------------------------------------------------------
        ep = T("epithelium", 22, TEXT).move_to([-3.55, -2.85, 0])
        prep = T("in this preparation", 22, GREY).move_to([-3.2, -3.4, 0])
        self.at("in this preparation")
        self.play(FadeOut(clock), FadeIn(prep), run_time=0.4)
        self.at("epithelium directly")
        self.play(FadeIn(ep), r2[2].animate.set_fill(TEXT, 0.9), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Equal(SpokenScene):
    """equal grip in vitro; cortisol outnumbers aldosterone, so the socket should be mostly cortisol: selectivity is not in the receptor."""

    def construct(self):
        body, ring, lbl = receptor()
        self.play(FadeIn(body), FadeIn(ring), FadeIn(lbl), run_time=0.5)
        a_chip = chip("aldosterone", YELLOW, size=24, pad=0.16)
        eq = T("=", 40, TEXT)
        c_chip = chip("cortisol", PURPLE, size=24, pad=0.16)
        eqg = VGroup(a_chip, eq, c_chip).arrange(RIGHT, buff=0.3).move_to([2.3, 2.6, 0])
        eq_t = T("equal affinity", 24, GREY).move_to([2.3, 1.95, 0])
        ext = T("in extracts of kidney and other tissues", 24, GREY).move_to([1.8, 3.3, 0])

        a = dot(YELLOW, 0.2, -1.2, 0)
        c = dot(PURPLE, 0.2, -1.2, 0)
        self.at("extracts of kidney")
        self.play(FadeIn(ext), run_time=0.5)
        self.at("bound aldosterone")
        self.play(FadeIn(a), run_time=0.15)
        self.play(route(a, [(-1.2, 0), (-2.6, 0), (SX, 0)], 0.6), ring.animate.set_stroke(YELLOW), FadeIn(a_chip, shift=RIGHT * 0.2), run_time=0.6)
        self.at("physiological")
        self.play(a.animate.move_to([-1.2, 0, 0]).set_opacity(0), ring.animate.set_stroke(BLUE), run_time=0.35)
        self.play(FadeIn(c), run_time=0.1)
        self.play(route(c, [(-1.2, 0), (-2.6, 0), (SX, 0)], 0.6), ring.animate.set_stroke(PURPLE), FadeIn(c_chip, shift=LEFT * 0.2), run_time=0.6)
        self.at("equal affinity")
        self.play(FadeIn(eq, scale=0.6), FadeIn(eq_t), run_time=0.5)

        # --- cortisol is far more concentrated ---------------------------------------------------------
        cols = crowd()
        allc = flat(cols)
        ald = ald_dot()
        c_lbl = tag("cortisol", PURPLE).move_to([0.95, -2.1, 0])
        a_lbl = ald_label(ald)
        far = T("far higher\nconcentrations", 24, PURPLE, line_spacing=0.8).move_to([4.7, 0.2, 0])
        self.at("in humans")
        self.play(c.animate.move_to([-1.2, 0, 0]).set_opacity(0), ring.animate.set_stroke(BLUE), FadeOut(eqg), FadeOut(eq_t), FadeOut(ext), run_time=0.5)
        self.at("cortisol and it circulates")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in allc], lag_ratio=0.03), FadeIn(c_lbl), FadeIn(ald, scale=0.5), FadeIn(a_lbl), run_time=1.4)
        self.at("far higher")
        self.play(FadeIn(far, shift=LEFT * 0.2), run_time=0.5)

        # --- on those numbers, cortisol sits in the socket nearly all the time ---------------------------
        note = T("on those numbers", 24, GREY).move_to([4.7, -1.2, 0])
        occ = T("cortisol occupies\nthe receptor nearly\nall the time", 24, PURPLE, line_spacing=0.8).move_to([4.6, -2.45, 0])
        self.at("those numbers")
        self.play(FadeIn(note), run_time=0.4)
        d1, d2, d3 = cols[0][3], cols[0][4], cols[0][5]
        self.at("cortisol should occupy")
        self.play(route(d1, [(0.3, -0.21), (-1.5, -0.1), (SX, 0)], 0.8), ring.animate.set_stroke(PURPLE), FadeIn(occ),
                  route(ald, [(0.3, 1.89), (-1.4, 1.2), (-2.6, -0.6)], 0.9), run_time=0.9)
        self.play(route(ald, [(-2.6, -0.6), (-2.9, -0.3), (-2.7, -0.9)], 0.4), run_time=0.4)
        self.at("nearly all the time")
        self.play(d1.animate.move_to([-3.0, 0.9, 0]).set_opacity(0), run_time=0.3)
        self.play(route(d2, [(0.3, 0.21), (-1.5, 0.1), (SX, 0)], 0.5), run_time=0.5)
        self.play(d2.animate.move_to([-3.0, 0.9, 0]).set_opacity(0), run_time=0.3)
        self.play(route(d3, [(0.3, 0.63), (-1.5, 0.1), (SX, 0)], 0.5), run_time=0.5)

        # --- selectivity is not in the receptor -----------------------------------------------------
        sel = T("selectivity is not in the receptor", 28, TEXT).move_to([-0.2, -3.2, 0])
        self.at("selectivity is not")
        self.play(FadeIn(sel, shift=UP * 0.15), Indicate(body, color=BLUE, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def stage_base(box_label):
    """receptor, tissue box, crowd and aldosterone, as at the end of scene 3 (no enzyme yet)."""
    body, ring, lbl = receptor()
    box, box_lbl = tissue_box(box_label)
    cols = crowd()
    allc = flat(cols)
    ald = ald_dot()
    return body, ring, lbl, box, box_lbl, cols, allc, ald


class S04Guard(SpokenScene):
    """the question box becomes the enzyme; it turns cortisol into inactive cortisone; aldosterone escapes and docks."""

    def construct(self):
        body, ring, lbl, box, box_lbl, cols, allc, ald = stage_base("kidney, colon, parotid")
        q = unknown_box()
        self.add(body, ring, lbl, allc, ald)
        self.add(q)
        c_lbl = tag("cortisol", PURPLE).move_to([0.95, -2.1, 0])
        a_lbl = ald_label(ald)
        self.add(c_lbl, a_lbl)

        # --- 1988: Funder and colleagues ----------------------------------------------------------
        b1 = T("1988", 34, font=TITLE_FONT).move_to([1.2, 3.15, 0])
        self.at("answer came")
        self.play(FadeIn(b1, shift=DOWN * 0.1), run_time=0.5)
        b1b = T("1988: John Funder and colleagues", 28, font=TITLE_FONT).move_to([1.2, 3.15, 0])
        self.at("colleagues reported")
        self.play(ReplacementTransform(b1, b1b), run_time=0.6)

        # --- targets carry an enzyme ----------------------------------------------------------------
        self.at("colon and")
        self.play(Create(box), FadeIn(box_lbl), run_time=0.9)
        eb, er, el = enzyme()
        self.at("enzyme")
        self.play(FadeOut(q[0]), FadeOut(q[1]), FadeIn(eb), FadeIn(er), FadeIn(el), run_time=0.7)

        # --- converts cortisol to inactive cortisone ------------------------------------------------
        lg_p = VGroup(dot(PURPLE, 0.16), T("cortisol", 24, PURPLE)).arrange(RIGHT, buff=0.2).move_to([4.7, 0.9, 0])
        lg_g = VGroup(dot(GREY, 0.16), T("cortisone, inactive", 24, GREY)).arrange(RIGHT, buff=0.2).move_to([4.7, 0.0, 0])
        lg_y = VGroup(dot(YELLOW, 0.16), T("aldosterone", 24, YELLOW)).arrange(RIGHT, buff=0.2).move_to([4.7, -0.9, 0])
        for lg in (lg_p, lg_g, lg_y):
            lg.align_to(np.array([3.2, 0, 0]), LEFT)
        ds = [cols[0][3], cols[0][4], cols[0][5]]
        mouth = (EX + 0.95, 0)
        species = T("in rats: corticosterone\nin humans: cortisol", 22, GREY, line_spacing=0.8)
        species.move_to([4.7, -2.2, 0]).align_to(np.array([3.2, 0, 0]), LEFT)
        self.at("converts cortisol")
        self.play(FadeIn(lg_p), FadeIn(species), LaggedStart(*[route(d, [(0.3, y0), (-0.2, y0 * 0.4), mouth], 0.6)
                                              for d, y0 in zip(ds, (-0.21, 0.21, 0.63))], lag_ratio=0.2), run_time=1.0)
        self.at("inactive cortisone")
        rest = [(EX - 0.2, -1.55), (EX + 0.25, -1.55), (EX + 0.7, -1.55)]
        self.play(FadeIn(lg_g), *[d.animate(run_time=0.3).set_fill(GREY, 0.9).set_stroke(GREY) for d in ds], run_time=0.3)
        self.play(LaggedStart(*[route(d, [mouth, (mouth[0] - 0.1, -0.9), r], 0.6) for d, r in zip(ds, rest)], lag_ratio=0.2), run_time=1.0)

        # --- aldosterone escapes the conversion --------------------------------------------------
        self.at("Aldosterone escapes")
        self.play(FadeIn(lg_y), FadeOut(a_lbl), run_time=0.3)
        self.play(route(ald, [(0.3, 1.89), (-0.8, 1.75), (EX, 1.7), (-3.4, 0.45), (SX, 0)], 1.4), run_time=1.4)
        self.play(ring.animate.set_stroke(YELLOW), Indicate(body, color=BLUE, scale_factor=1.03), run_time=0.4)

        # --- less cortisol near the receptor; left to aldosterone ---------------------------------
        b2 = T("less cortisol near the receptor", 28, font=TITLE_FONT).move_to([1.2, 3.15, 0])
        self.at("lowers cortisol")
        self.play(ReplacementTransform(b1b, b2), run_time=0.6)
        self.at("left to aldosterone")
        self.play(Indicate(ald, color=YELLOW, scale_factor=1.5), run_time=0.8)

        # --- Edwards, the same year ---------------------------------------------------------------
        b3 = T("Edwards and colleagues, same year:\na similar conclusion", 26, font=TITLE_FONT, line_spacing=0.8).move_to([1.8, 3.0, 0])
        self.at("Edwards and colleagues")
        self.play(ReplacementTransform(b2, b3), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Liquorice(SpokenScene):
    """liquorice: sodium retained, potassium low, pressure up, renin and aldosterone low; inhibitor plugs the enzyme; cortisol reaches the receptor."""

    def construct(self):
        body, ring, lbl, box, box_lbl, cols, allc, ald = stage_base("kidney")
        eb, er, el = enzyme()
        c_lbl = tag("cortisol", PURPLE).move_to([0.95, -2.1, 0])
        self.add(body, ring, lbl, box, box_lbl, eb, er, el, allc, c_lbl)

        # --- liquorice fits this idea --------------------------------------------------------
        liq = chip("liquorice", ORANGE, size=28, pad=0.18).move_to([-2.9, 3.15, 0])
        self.at("fits this")
        self.play(FadeIn(liq, shift=DOWN * 0.15), run_time=0.5)

        # --- the readout panel ------------------------------------------------------------------------
        rows = []
        specs = [("sodium retention", UP, TEXT, 2.5), ("plasma potassium", DOWN, TEXT, 1.75), ("blood pressure", UP, TEXT, 1.0),
                 ("renin", DOWN, TEXT, 0.25), ("aldosterone", DOWN, YELLOW, -0.5)]
        for name, d, col, y in specs:
            t = T(name, 24, col).move_to([4.6, y, 0])
            t.align_to(np.array([2.9, 0, 0]), LEFT)
            a = Arrow([6.2, y - 0.3 * (1 if d is UP else -1), 0], [6.2, y + 0.3 * (1 if d is UP else -1), 0], buff=0, color=col,
                      stroke_width=6, tip_length=0.22, max_tip_length_to_length_ratio=0.5)
            rows.append(VGroup(t, a))
        self.at("sodium retention")
        self.play(FadeIn(rows[0], shift=LEFT * 0.2), run_time=0.5)
        self.at("low potassium")
        self.play(FadeIn(rows[1], shift=LEFT * 0.2), run_time=0.5)
        self.at("high blood pressure")
        self.play(FadeIn(rows[2], shift=LEFT * 0.2), run_time=0.5)
        self.at("aldosterone are both")
        self.play(FadeIn(rows[3], shift=LEFT * 0.2), FadeIn(rows[4], shift=LEFT * 0.2), run_time=0.6)

        # --- looks like excess, without the mineralocorticoid ----------------------------------------------
        look = T("looks like\nmineralocorticoid excess", 24, GREY, line_spacing=0.8).move_to([4.3, -1.5, 0])
        self.at("mineralocorticoid excess")
        self.play(FadeIn(look), run_time=0.5)
        self.at("without the mineralocorticoid")
        self.play(Indicate(rows[4], color=YELLOW, scale_factor=1.12), run_time=0.9)

        # --- the inhibitor plugs the enzyme -------------------------------------------------------------
        plug = RoundedRectangle(corner_radius=0.1, width=0.34, height=0.9, stroke_color=ORANGE, stroke_width=3,
                                fill_color=ORANGE, fill_opacity=0.9).move_to([-0.6, 2.5, 0])
        gly = chip("glycyrrhetinic acid", ORANGE, size=24, pad=0.14).move_to([-0.9, 3.1, 0])
        self.at("inhibits the enzyme")
        self.play(ReplacementTransform(liq, gly), FadeIn(plug), run_time=0.5)
        self.play(plug.animate.move_to([EX + 0.85, 0, 0]), eb.animate.set_stroke(RED).set_fill(RED, 0.2),
                  er.animate.set_stroke(RED), el.animate.set_color(RED), run_time=0.8)
        off = T("off", 24, RED, weight=BOLD).move_to([EX, 1.5, 0])
        self.play(FadeIn(off), run_time=0.3)

        # --- cortisol no longer inactivated, occupies the receptor -------------------------------------------
        self.at("no longer inactivated")
        ds = [cols[0][3], cols[0][4], cols[0][5]]
        self.play(route(ds[0], [(0.3, -0.21), (-0.7, -0.9), (EX, -1.6), (-3.3, -0.55), (SX, 0)], 1.7), run_time=1.7)
        self.play(ring.animate.set_stroke(PURPLE), run_time=0.3)
        self.play(route(ds[1], [(0.3, 0.21), (-0.7, -0.9), (EX, -1.6), (-3.3, -0.7)], 1.7), run_time=1.7)
        self.at("receptor itself")
        self.play(Circumscribe(ring, color=PURPLE, buff=0.12, run_time=0.9))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """limits of the conclusion, on a short timeline; then the rule that the enzyme beside a receptor helps define the target."""

    def construct(self):
        body, ring, lbl, box, box_lbl, cols, allc, ald = stage_base("kidney, colon, parotid")
        eb, er, el = enzyme()
        self.add(body, ring, lbl, box, box_lbl, eb, er, el)
        a = dot(YELLOW, 0.2, SX, 0)
        ring.set_stroke(YELLOW)
        self.add(a)

        head = T("limits of the conclusion", 28, font=TITLE_FONT).move_to([3.3, 3.1, 0])
        self.at("limits")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)

        line = Line([0.8, 0.2, 0], [6.2, 0.2, 0], color=GREY, stroke_width=4)
        t1 = Line([2.1, 0.05, 0], [2.1, 0.35, 0], color=GREY, stroke_width=4)
        t2 = Line([5.0, 0.05, 0], [5.0, 0.35, 0], color=GREY, stroke_width=4)
        y1 = T("1988", 26, TEXT).move_to([2.1, -0.35, 0])
        y2 = T("1990s", 26, TEXT).move_to([5.0, -0.35, 0])
        self.play(Create(line), FadeIn(t1), FadeIn(t2), FadeIn(y1), FadeIn(y2), run_time=0.6)

        c1 = chip("rats", GREY, size=24, pad=0.14).move_to([2.1, 1.9, 0])
        c1b = chip("corticosterone", PURPLE, size=24, pad=0.14).move_to([2.1, 1.1, 0])
        self.at("rats and")
        self.play(FadeIn(c1, shift=DOWN * 0.15), run_time=0.4)
        self.at("corticosterone")
        self.play(FadeIn(c1b, shift=DOWN * 0.15), run_time=0.4)

        c2 = chip("type 2 form\nof the enzyme", GREEN, size=24, pad=0.14).move_to([5.0, 1.5, 0])
        c2t = T("characterized", 24, GREEN).move_to([5.0, -1.0, 0])
        self.at("form of the enzyme")
        self.play(FadeIn(c2, shift=DOWN * 0.15), run_time=0.5)
        self.at("characterized")
        self.play(FadeIn(c2t), run_time=0.4)

        # --- the rule ---------------------------------------------------------------------------------------
        keep = T("the rule", 28, GOLD, weight=BOLD).move_to([3.3, 3.1, 0])
        self.at("Keep this rule")
        self.play(FadeOut(VGroup(line, t1, t2, y1, y2, c1, c1b, c2, c2t)), ReplacementTransform(head, keep), run_time=0.7)
        l1 = T("the enzyme beside a receptor", 30, GREEN)
        l2 = T("is part of what defines", 30, TEXT)
        l3 = T("a hormone's target tissue", 30, TEXT)
        rule = VGroup(l1, l2, l3).arrange(DOWN, buff=0.35).move_to([3.4, 0.2, 0])
        self.at("beside a receptor")
        self.play(FadeIn(l1, shift=LEFT * 0.2), Indicate(VGroup(eb, er, el), color=GREEN, scale_factor=1.06),
                  Indicate(body, color=BLUE, scale_factor=1.04), run_time=1.0)
        self.at("part of what defines")
        self.play(FadeIn(l2), box.animate.set_color(GOLD).set_stroke(width=5), FadeOut(box_lbl), run_time=0.7)
        self.at("target tissue")
        self.play(FadeIn(l3), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "The enzyme beside a receptor helps define the target tissue."
