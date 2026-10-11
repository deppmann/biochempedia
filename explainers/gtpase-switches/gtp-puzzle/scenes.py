"""GTPase switches, section film: the puzzle of a requirement nobody expected  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole film)
  YELLOW = the hormone (glucagon)
  GREY   = membranes, buffer, outlines, de-emphasized
  BLUE   = ATP
  GREEN  = GTP (and "full response" bars)
  PURPLE = adenylyl cyclase
  TEAL   = cyclic AMP
  ORANGE = receptors
  GOLD   = the transducer (the separate protein)
  RED    = contaminant, "not", inactivated, missing link
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, size=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, size, 0], c + [size, -size, 0], color=color, stroke_width=w),
                  Line(c + [-size, -size, 0], c + [size, size, 0], color=color, stroke_width=w))


def membrane(x0, x1, y, h=0.4):
    return RoundedRectangle(corner_radius=0.1, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([(x0 + x1) / 2, y, 0])


def dot(color, r=0.22):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)


class S00Title(TitleCard):
    LESSON = "GTPase Switches: The Timer"
    TITLE = "The Hidden Requirement for GTP"


# ---------------------------------------------------------------------------------------------
class S01Stuck(SpokenScene):
    def construct(self):
        head = T("Rodbell's laboratory, around 1970", 30, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.at("Rodbell's laboratory")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)

        mem = membrane(-4.4, 4.4, -0.4)
        xs = [-3.0, -1.5, 0.0, 1.5, 3.0]
        gl = VGroup(*[dot(YELLOW).move_to([x, 0.0, 0]) for x in xs])
        gl_lbl = T("glucagon", 28, YELLOW).move_to([-5.8, 0.0, 0])
        gl_start = VGroup(*[g.copy().shift(UP * 1.3) for g in gl])
        self.at("how glucagon")
        self.play(FadeIn(mem), FadeIn(gl_lbl), FadeIn(gl_start), run_time=0.5)
        self.play(*[a.animate.shift(DOWN * 1.3) for a in gl_start], run_time=0.6)
        gl = gl_start

        cyc = bchip("adenylyl cyclase", PURPLE, 26).move_to([-3.4, -2.3, 0])
        self.at("switches on")
        self.play(FadeIn(cyc, shift=UP * 0.2), run_time=0.5)
        mem_lbl = T("liver membranes", 24, GREY).move_to([0, -1.05, 0])
        self.at("liver membranes")
        self.play(FadeIn(mem_lbl), run_time=0.5)

        mode = T("plain buffer", 30, GREY).move_to([0, 2.45, 0])
        self.at("In plain buffer")
        self.play(FadeIn(mode), run_time=0.5)

        wash = VGroup(*[arr([x - 0.6, 1.0, 0], [x + 0.6, 1.0, 0], GREY, w=5) for x in (-3.0, 0.0, 3.0)])
        wlbl = T("wash", 24, GREY).move_to([0, 1.55, 0])
        self.at("would not wash off")
        self.play(LaggedStart(*[GrowArrow(w) for w in wash], lag_ratio=0.25), FadeIn(wlbl), run_time=0.6)
        self.play(*[Wiggle(g, scale_value=1.0, rotation_angle=0.0, n_wiggles=4) for g in gl], run_time=0.5)
        self.play(FadeOut(wash), FadeOut(wlbl), run_time=0.25)

        mode2 = T("buffer + ATP", 30, GREY, t2c={"ATP": BLUE}).move_to([0, 2.45, 0])
        self.at("Add")
        self.play(ReplacementTransform(mode, mode2), run_time=0.5)

        offs = [(-1.2, 1.1), (-0.4, 0.7), (0.3, 1.0), (0.8, 0.6), (1.4, 0.9)]
        self.at("came off")
        self.play(*[g.animate.shift([dx, dy, 0]) for g, (dx, dy) in zip(gl, offs)], run_time=1.0)

        atp = bchip("ATP", BLUE, 28).move_to([-0.3, -3.0, 0])
        a_atp = arr(atp.get_left(), cyc.get_bottom() + DOWN * 0.02, BLUE)
        fuel = T("the enzyme's fuel", 24, GREY).next_to(atp, RIGHT, buff=0.3)
        self.at("fuel")
        self.play(FadeIn(atp), GrowArrow(a_atp), FadeIn(fuel), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Trace(SpokenScene):
    def construct(self):
        # --- the contaminant -------------------------------------------------------------
        bottle = bchip("commercial ATP", BLUE, 40, pad=0.5).move_to([0, 0.9, 0])
        cont = T("a contaminant", 34, RED, weight=BOLD).move_to([0, 2.7, 0])
        self.at("a contaminant")
        self.play(FadeIn(bottle, scale=0.9), FadeIn(cont, shift=DOWN * 0.1), run_time=0.7)
        speck = dot(GREEN, 0.13).move_to(bottle.get_bottom() + [0.9, 0.3, 0])
        sp_lbl = T("a little GTP", 30, GREEN).move_to([0.9, -1.4, 0])
        sp_arr = arr(sp_lbl.get_top() + UP * 0.05, speck.get_bottom(), GREEN)
        self.at("a little")
        self.play(FadeIn(speck, scale=3.0), FadeIn(sp_lbl), GrowArrow(sp_arr), run_time=0.8)

        # --- GTP required: two bars ---------------------------------------------------------
        base_y = -2.5
        axis = Line([-5.0, base_y, 0], [5.0, base_y, 0], color=GREY, stroke_width=3)
        bar_t = T("cyclase switched on (idealised)", 28, TEAL).move_to([0, 3.2, 0])
        bar_g = Rectangle(width=1.8, height=3.4, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                          fill_opacity=0.5).move_to([2.6, base_y + 1.7, 0])
        bar_n = Rectangle(width=1.8, height=0.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL,
                          fill_opacity=0.5).move_to([-2.6, base_y + 0.15, 0])
        lab_g = T("GTP added on purpose", 26, GREEN).move_to([2.6, base_y - 0.45, 0])
        lab_n = T("without GTP", 26, GREY).move_to([-2.6, base_y - 0.45, 0])
        note_n = T("barely on", 26, GREY).move_to([-2.6, base_y + 0.85, 0])
        self.at("Added on")
        self.play(FadeOut(VGroup(bottle, cont, speck, sp_lbl, sp_arr)), FadeIn(axis), FadeIn(bar_t), run_time=0.6)
        self.play(FadeIn(lab_g), FadeIn(bar_g, shift=UP * 0.4), run_time=0.7)
        self.at("Without it")
        self.play(FadeIn(lab_n), FadeIn(bar_n), run_time=0.5)
        self.at("barely")
        self.play(FadeIn(note_n), run_time=0.4)

        # --- not the fuel ---------------------------------------------------------------------
        self.at("was not the fuel")
        self.play(FadeOut(VGroup(axis, bar_t, bar_g, bar_n, lab_g, lab_n, note_n)), run_time=0.3)
        cyc = bchip("adenylyl cyclase", PURPLE, 32).move_to([1.2, -0.3, 0])
        gtp = bchip("GTP", GREEN, 32).move_to([-4.6, 1.4, 0])
        a_g = arr(gtp.get_right(), [cyc.get_left()[0], cyc.get_center()[1] + 0.3, 0], GREEN)
        x = cross(a_g.get_center(), 0.28)
        nf = T("not the fuel", 26, RED).next_to(a_g, UP, buff=0.35)
        self.play(FadeIn(cyc), FadeIn(gtp), GrowArrow(a_g), run_time=0.4)
        self.play(Create(x), FadeIn(nf), run_time=0.3)
        atp = bchip("ATP", BLUE, 32).move_to([-4.6, -2.0, 0])
        a_a = arr(atp.get_right(), [cyc.get_left()[0], cyc.get_center()[1] - 0.3, 0], BLUE)
        fl = T("the fuel", 26, BLUE).next_to(a_a, DOWN, buff=0.3)
        self.play(FadeIn(atp), GrowArrow(a_a), FadeIn(fl), run_time=0.4)

        # --- a trace is enough, used over and over -----------------------------------------------
        self.at("A trace was")
        trace = T("a trace", 28, GREEN).move_to([-4.6, 2.9, 0])
        self.play(gtp.animate.scale(0.65), FadeIn(trace), run_time=0.6)
        camps = VGroup(*[bchip("cyclic AMP", TEAL, 24) for _ in range(3)]).arrange(DOWN, buff=0.35).move_to([5.0, -0.3, 0])
        outs = VGroup(*[arr(cyc.get_right(), c.get_left(), TEAL, w=4) for c in camps])
        loop = Arc(radius=0.85, start_angle=PI / 6, angle=1.7 * PI, color=GREEN, stroke_width=5).move_to(gtp.get_center())
        loop.add_tip(tip_length=0.2)
        ideal = T("idealised", 24, GREY).move_to([5.0, -2.5, 0])
        self.at("used over and over")
        self.play(Create(loop), run_time=0.5)
        self.play(Rotate(loop, angle=-TAU, about_point=gtp.get_center()),
                  LaggedStart(*[AnimationGroup(GrowArrow(o), FadeIn(c)) for o, c in zip(outs, camps)], lag_ratio=0.35),
                  FadeIn(ideal), run_time=2.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tube(x, y, label, label_color):
    body = RoundedRectangle(corner_radius=0.4, width=1.9, height=2.8, stroke_color=GREY, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.12).move_to([x, y, 0])
    inner = VGroup(T("ATP", 26, BLUE), T("1% GTP", 24, GREEN)).arrange(DOWN, buff=0.12).move_to(body)
    lbl = T(label, 26, label_color).next_to(body, DOWN, buff=0.25)
    return body, inner, lbl


def resp_bar(x, base, color=GREEN):
    r = Rectangle(width=0.7, height=2.4, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
    r.move_to([x, base + 1.2, 0])
    t = T("full response", 24, color).next_to(r, UP, buff=0.2).shift(RIGHT * 0.35)
    return r, t


class S03Hidden(SpokenScene):
    def construct(self):
        # --- why nobody else saw it -----------------------------------------------------------
        a = bchip("Rodbell's membranes: clean", GREEN, 34).move_to([0, 1.1, 0])
        b = bchip("most other laboratories: not as clean", GREY, 34).move_to([0, -1.0, 0])
        none = T("effect not reproduced", 30, GREY).next_to(b, DOWN, buff=0.3)
        self.at("almost no other laboratory")
        self.play(FadeIn(b, shift=UP * 0.2), FadeIn(none), run_time=0.7)
        self.at("most were not")
        self.play(FadeIn(a, shift=DOWN * 0.2), run_time=0.6)

        # --- suppose the ATP is 1% GTP -------------------------------------------------------------
        t1, i1, l1 = tube(-4.6, 0.3, "no GTP added", GREY)
        r1, rt1 = resp_bar(-2.4, -1.1)
        ex = T("for example", 26, GREY).move_to([-3.5, 2.5, 0])
        self.at("Suppose")
        self.play(FadeOut(VGroup(a, b, none)), run_time=0.4)
        self.play(FadeIn(t1), FadeIn(l1), FadeIn(ex), run_time=0.5)
        self.at("Then the tube")
        self.play(FadeIn(i1), run_time=0.5)
        self.at("already holds")
        self.play(FadeIn(r1, shift=UP * 0.3), FadeIn(rt1), run_time=0.7)

        t2, i2, l2 = tube(1.4, 0.3, "GTP added", GREEN)
        i2[0].set_color(BLUE)
        r2, rt2 = resp_bar(3.6, -1.1)
        eq = T("no difference", 28, YELLOW).move_to([-0.5, -2.9, 0])
        self.at("so the difference")
        self.play(FadeIn(t2), FadeIn(l2), FadeIn(i2), run_time=0.5)
        self.play(FadeIn(r2, shift=UP * 0.3), FadeIn(rt2), run_time=0.5)
        self.at("never appears")
        self.play(FadeIn(eq), run_time=0.4)

        # --- Rodbell's second problem: many receptors, one enzyme ---------------------------------
        self.at("Many receptors")
        self.play(FadeOut(VGroup(t1, i1, l1, r1, rt1, ex, t2, i2, l2, r2, rt2, eq)), run_time=0.6)
        recs = [bchip("receptor", ORANGE, 28).move_to([x, 2.3, 0]) for x in (-4.2, 0.0, 4.2)]
        cyc = bchip("adenylyl cyclase", PURPLE, 28).move_to([0, -2.6, 0])
        direct = VGroup(*[arr(r.get_bottom(), cyc.get_top(), ORANGE, w=4) for r in recs])
        self.at("switch on")
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.2) for r in recs], lag_ratio=0.25), run_time=0.9)
        self.play(FadeIn(cyc), LaggedStart(*[GrowArrow(d) for d in direct], lag_ratio=0.2), run_time=0.9)

        box = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.6, height=0.9, stroke_color=GOLD,
                                              stroke_width=3), num_dashes=30).move_to([0, -0.15, 0])
        q = T("?", 34, GOLD).move_to(box)
        a_in = VGroup(*[arr(r.get_bottom(), [x, 0.35, 0], ORANGE, w=4) for r, x in zip(recs, (-1.0, 0.0, 1.0))])
        a_out = arr([0, -0.62, 0], cyc.get_top(), GOLD, w=5)
        self.at("So he proposed")
        self.play(FadeOut(direct), run_time=0.3)
        self.play(Create(box), FadeIn(q), LaggedStart(*[GrowArrow(i) for i in a_in], lag_ratio=0.15), GrowArrow(a_out), run_time=1.0)
        tr = bchip("transducer", GOLD, 30).move_to([0, -0.15, 0])
        self.at("transducer")
        self.play(FadeOut(box), ReplacementTransform(q, tr), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Rescue(SpokenScene):
    def construct(self):
        h1 = T("University of Virginia: Alfred Gilman's laboratory", 30, font=TITLE_FONT).move_to([0, 3.35, 0])
        self.at("The answer came")
        self.play(FadeIn(h1, shift=DOWN * 0.1), run_time=0.7)
        my = -0.5
        mem = membrane(-6.0, 6.0, my)
        rec = RoundedRectangle(corner_radius=0.2, width=0.8, height=1.5, stroke_color=ORANGE, stroke_width=4,
                               fill_color=ORANGE, fill_opacity=0.3).move_to([-3.6, my + 0.55, 0])
        rec_l = T("receptor", 26, ORANGE).next_to(rec, DOWN, buff=0.7)
        cyc = bchip("adenylyl cyclase", PURPLE, 26).move_to([3.4, my + 0.55, 0])
        mlbl = T("cyc− lymphoma cells", 26, GREY).move_to([0, my - 2.0, 0])
        self.at("laboratory at")
        self.play(FadeIn(mem), FadeIn(rec), FadeIn(rec_l), FadeIn(cyc), run_time=0.8)
        h2 = T("with Elliott Ross", 26, GREY).move_to([0, 2.8, 0])
        self.at("Elliot Ross")
        self.play(FadeIn(h2), run_time=0.5)

        self.at("lymphoma cells")
        self.play(FadeIn(mlbl), run_time=0.5)

        gap = DashedLine([-2.9, my + 0.55, 0], [2.0, my + 0.55, 0], color=RED, stroke_width=4)
        gq = T("?", 34, RED).move_to([-0.45, my + 0.9, 0])
        self.at("where the link")
        self.play(Create(gap), FadeIn(gq), run_time=0.7)

        # --- the extract --------------------------------------------------------------------------
        ext = RoundedRectangle(corner_radius=0.25, width=8.0, height=1.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.12).move_to([0, 2.7, 0])
        ext_l = T("extract from normal cells", 26, GREY).move_to([-1.4, 2.75, 0])
        cy2 = bchip("its own cyclase", PURPLE, 24).move_to([2.2, 2.75, 0])
        self.at("an extract")
        self.play(FadeOut(VGroup(h1, h2)), run_time=0.3)
        self.play(FadeIn(ext), FadeIn(ext_l), FadeIn(cy2), run_time=0.6)

        hor = dot(YELLOW, 0.24).move_to([-5.6, 1.05, 0])
        hor_l = T("hormone", 26, YELLOW).move_to([-3.6, 1.7, 0])
        camp2 = bchip("cyclic AMP", TEAL, 26).move_to([3.4, my - 1.1, 0])
        a_camp = arr([3.4, my + 0.2, 0], camp2.get_top() + UP * 0.02, TEAL)
        tr = bchip("transducer", GOLD, 24).move_to([-1.9, 2.75, 0])
        self.at("response came back")
        self.play(FadeOut(ext_l), FadeIn(tr, scale=1.2), run_time=0.4)
        gtr = bchip("transducer", GOLD, 24).move_to([-0.45, my + 0.55, 0])
        self.play(tr.animate.move_to(gtr.get_center()), FadeOut(gap), FadeOut(gq), run_time=0.8)
        link = VGroup(arr(rec.get_right(), tr.get_left(), GOLD, w=4),
                      arr(tr.get_right(), cyc.get_left(), GOLD, w=4))
        self.play(FadeIn(link), FadeIn(hor), FadeIn(hor_l), run_time=0.4)
        self.play(hor.animate.move_to([-3.6, 1.05, 0]), FadeIn(a_camp), FadeIn(camp2), run_time=0.6)
        xx = cross(cy2.get_center(), 0.3)
        inact = T("inactivated", 22, RED).next_to(cy2, DOWN, buff=0.2)
        self.at("inactivated")
        self.play(Create(xx), FadeIn(inact), run_time=0.5)

        self.at("So the transducer")
        self.play(Indicate(tr, color=GOLD, scale_factor=1.15), run_time=0.7)
        self.at("movable protein")
        self.play(Indicate(tr, color=GOLD, scale_factor=1.1), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "A trace of GTP was enough: it was used over and over."
