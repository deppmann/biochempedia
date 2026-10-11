"""Cytochrome c, found in a test tube  (Biochemistrypedia section film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  RED     = caspases (a dashed outline is inactive, a solid one is active)
  ORANGE  = cytochrome c (the dashed white disc with a question mark is the unknown protein)
  TEAL    = APAF-1 and the wheel (apoptosome)
  GREY    = the soluble contents (idealised dots), the tube, labels
  GREEN   = the word "on" (reaction running)
  TEXT    = names, the dATP chip, the antibody chip

No molecular structures: proteins are dots, discs and labelled chips; the tube is an outline.

Story (the experiment, in the order the lesson tells it):
  1 tube     soluble contents of HeLa cells + dATP: caspase-3 switches on (Wang laboratory, 1996)
  2 narrow   fractionation narrows the requirement to one small protein; an antibody removes it: stops
  3 back     the pure protein added back: restored; it is cytochrome c, which has a second job
  4 partner  the next year APAF-1: cytochrome c and dATP, seven copies, the wheel, caspase-9; the rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F28C28"
TX, TY = -1.9, -0.2          # tube centre x, and the vertical centre of the tube
TW, TH = 2.6, 5.2
RX, RY = 3.7, -0.35          # readout (caspase-3) centre


def rr(w, h, r=None):
    return RoundedRectangle(corner_radius=r if r is not None else min(0.25, h / 2.2), width=w, height=h)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def casp(label, w=3.2, h=1.5, size=30, active=False, pos=ORIGIN):
    """[back, fill, dashed outline, solid outline, label]: dashed = inactive, solid = active"""
    back = rr(w, h).set_stroke(width=0).set_fill(BG, 1)
    fl = rr(w, h).set_stroke(width=0).set_fill(RED, 0.5 if active else 0.1)
    dash = DashedVMobject(rr(w, h), num_dashes=max(14, int(2 * (w + h) * 4))).set_stroke(RED, 3.5, opacity=0.0 if active else 1.0)
    solid = rr(w, h).set_stroke(RED, 4.5, opacity=1.0 if active else 0.0).set_fill(RED, 0)
    lbl = T(label, size, TEXT) if label else Dot(radius=0.001, color=BG)
    g = VGroup(back, fl, dash, solid, lbl)
    g.fl, g.dash, g.solid, g.lbl = fl, dash, solid, lbl
    return g.move_to(pos)


def casp_on(g):
    return [g.fl.animate.set_fill(RED, 0.5), g.dash.animate.set_stroke(opacity=0.0), g.solid.animate.set_stroke(opacity=1.0)]


def casp_off(g):
    return [g.fl.animate.set_fill(RED, 0.1), g.dash.animate.set_stroke(opacity=1.0), g.solid.animate.set_stroke(opacity=0.0)]


def tube(cx=TX, cy=TY, w=TW, h=TH):
    """an open-topped test tube outline with a rounded bottom; returns (outline, inner left, right, bottom, top)"""
    x0, x1, yt, yb = cx - w / 2, cx + w / 2, cy + h / 2, cy - h / 2
    r = w / 2
    pts = [[x0, yt, 0], [x0, yb + r, 0]]
    for a in np.linspace(PI, TAU, 14):
        pts.append([cx + r * np.cos(a), yb + r + r * np.sin(a), 0])
    pts += [[x1, yb + r, 0], [x1, yt, 0]]
    o = VMobject().set_points_as_corners(pts).set_stroke(GREY, 5).set_fill(opacity=0)
    return o


def liquid(cx=TX, cy=TY, w=TW, h=TH, top=1.0):
    """the liquid fill, up to height `top` above the bottom of the tube"""
    x0, yb = cx - w / 2, cy - h / 2
    r = w / 2
    pts = [[x0, yb + top, 0], [x0, yb + r, 0]]
    for a in np.linspace(PI, TAU, 14):
        pts.append([cx + r * np.cos(a), yb + r + r * np.sin(a), 0])
    pts += [[cx + w / 2, yb + r, 0], [cx + w / 2, yb + top, 0]]
    return Polygon(*pts, stroke_width=0, fill_color=GREY, fill_opacity=0.18)


LIQ = 3.7                    # liquid height
rng = np.random.RandomState(4)
BASE = []
for k in range(26):
    x = TX + rng.uniform(-1.0, 1.0)
    y = TY - TH / 2 + rng.uniform(0.6, 2.5)
    BASE.append((x, y, rng.uniform(0.07, 0.14)))


def dots():
    return [Circle(radius=r, stroke_width=0, fill_color=GREY, fill_opacity=0.85).move_to([x, y, 0]) for x, y, r in BASE]


def lamp(pos, on):
    return T("on" if on else "off", 34, GREEN if on else GREY, weight=BOLD).move_to(pos)


def disc(pos, r=0.3, unknown=False):
    if unknown:
        d = Circle(radius=r, stroke_color=TEXT, stroke_width=3.5, fill_color=TEXT, fill_opacity=0.1).move_to(pos)
        q = T("?", 28, TEXT, weight=BOLD).move_to(pos)
        return VGroup(d, q)
    return Circle(radius=r, stroke_color=ORANGE, stroke_width=3.5, fill_color=ORANGE, fill_opacity=0.85).move_to(pos)


class S00Title(TitleCard):
    LESSON = "Death Receptors, BCL-2 and Caspases"
    TITLE = "Cytochrome c, found in a test tube"


class S01Tube(SpokenScene):
    def construct(self):
        tb = tube()
        liq = liquid(top=LIQ)
        ctr = DashedVMobject(rr(3.2, 1.5), num_dashes=30)  # placeholder, replaced by casp below
        c3 = casp("caspase-3", pos=[RX, RY, 0])
        off = lamp([RX, RY - 1.2, 0], False)
        a = arr([TX + TW / 2 + 0.2, RY, 0], [RX - 1.75, RY, 0], GREY, w=6)
        tlab = T("test tube", 26, GREY).move_to([TX, TY - TH / 2 - 0.4, 0])

        self.at("Can a")
        self.play(Create(tb), FadeIn(tlab), run_time=0.8)
        self.play(FadeIn(c3, shift=LEFT * 0.2), FadeIn(off), GrowArrow(a), run_time=0.7)

        yr = T("1996", 44, TEXT, font=TITLE_FONT).move_to([RX, 2.75, 0])
        lab = T("Xiaodong Wang's laboratory", 26, GREY).move_to([RX, 2.0, 0])
        self.at("In 1996")
        self.play(FadeIn(yr, shift=DOWN * 0.1), run_time=0.5)
        self.at("laboratory made")
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)

        ds = dots()
        cl = T("soluble contents\nof HeLa cells", 26, GREY, line_spacing=0.9).move_to([-5.0, 0.7, 0])
        ptr = Line([-3.9, 0.45, 0], [TX - 1.25, 0.45, 0], color=GREY, stroke_width=3)
        idl = T("idealised", 22, GREY).move_to([-5.0, -0.2, 0])
        self.at("soluble contents")
        self.play(FadeIn(liq), LaggedStart(*[FadeIn(d, scale=0.4) for d in ds], lag_ratio=0.03),
                  FadeIn(cl), Create(ptr), FadeIn(idl), run_time=1.6)

        datp = chip("dATP", TEXT, size=28).move_to([TX, TY + TH / 2 + 0.5, 0])
        self.at("added the nucleotide")
        self.play(FadeIn(datp, shift=DOWN * 0.2), run_time=0.4)
        self.play(datp.animate.move_to([TX, TY + 1.0, 0]), run_time=0.8)
        self.at("Caspase")
        self.play(Indicate(c3, color=RED, scale_factor=1.08), run_time=0.6)
        self.at("switched on")
        on = lamp([RX, RY - 1.2, 0], True)
        self.play(*casp_on(c3), Transform(off, on), run_time=0.6)
        self.finish()


def build_state(scene_add=True, disc_in=True, c3_on=True):
    """rebuild the tube as it stands at the start of the next scene"""
    tb, liq = tube(), liquid(top=LIQ)
    ds = dots()
    datp = chip("dATP", TEXT, size=28).move_to([TX, TY + 1.0, 0])
    c3 = casp("caspase-3", pos=[RX, RY, 0])
    if c3_on:
        c3.fl.set_fill(RED, 0.5); c3.dash.set_stroke(opacity=0.0); c3.solid.set_stroke(opacity=1.0)
    a = arr([TX + TW / 2 + 0.2, RY, 0], [RX - 1.75, RY, 0], GREY, w=6)
    tlab = T("test tube", 26, GREY).move_to([TX, TY - TH / 2 - 0.4, 0])
    lp = lamp([RX, RY - 1.2, 0], c3_on)
    return tb, liq, ds, datp, c3, a, tlab, lp


class S02Narrow(SpokenScene):
    def construct(self):
        tb, liq, ds, datp, c3, a, tlab, lp = build_state()
        self.add(tb, liq, *ds, datp, c3, a, tlab, lp)

        q = disc([TX + 0.55, TY - 0.9, 0], 0.32, unknown=True)
        self.at("Which part")
        self.play(FadeIn(q, scale=0.5), Indicate(tb, color=TEXT, scale_factor=1.02), run_time=0.7)

        # fractionation: the dots sort into bands (idealised)
        bands = [TY - TH / 2 + 0.75 + i * 0.85 for i in range(4)]
        moves = []
        for i, d in enumerate(ds):
            b = bands[i % 4]
            moves.append(d.animate.move_to([TX - 0.95 + (i // 4) * 0.33, b, 0]))
        fl = T("fractions (idealised)", 24, GREY).move_to([-5.0, 0.6, 0])
        self.at("fractionated")
        self.play(*moves, FadeOut(datp), FadeIn(fl), run_time=1.3)

        # narrowed: everything else dims, one small protein remains
        one = T("one small\nprotein", 28, TEXT, line_spacing=0.9).move_to([-4.9, -1.3, 0])
        ptr = Line([-3.8, -1.2, 0], [TX + 0.15, -0.95, 0], color=TEXT, stroke_width=3)
        self.at("narrowed the requirement")
        self.play(*[d.animate.set_fill(GREY, 0.18) for d in ds], liq.animate.set_fill(GREY, 0.06), run_time=0.6)
        self.at("one small protein")
        self.play(FadeIn(one, shift=RIGHT * 0.1), Create(ptr), Indicate(q, color=TEXT, scale_factor=1.3), run_time=0.7)

        # back to the whole reaction for the test
        sc = [d.animate.move_to([x, y, 0]).set_fill(GREY, 0.85) for d, (x, y, r) in zip(ds, BASE)]
        self.at("Then came")
        self.play(*sc, liq.animate.set_fill(GREY, 0.18), FadeIn(datp), FadeOut(fl), FadeOut(one), FadeOut(ptr), run_time=1.0)
        ab = chip("antibody", TEXT, size=28).move_to([-5.4, TY - 0.4, 0])
        self.at("An antibody")
        self.play(FadeIn(ab), ab.animate.move_to([TX - 0.3, TY - 0.4, 0]), run_time=0.6)
        self.at("removed that protein")
        self.play(q.animate.move_to(ab.get_center() + [1.35, 0.0, 0]), run_time=0.35)
        self.play(AnimationGroup(q.animate.shift(UP * 4.1 + RIGHT * 0.5), ab.animate.shift(UP * 4.1 + LEFT * 0.7), run_time=1.0))
        self.at("reaction stopped")
        self.play(*casp_off(c3), Transform(lp, lamp([RX, RY - 1.2, 0], False)), run_time=0.6)
        self.play(FadeOut(q), FadeOut(ab), run_time=0.3)
        self.finish()


class S03Back(SpokenScene):
    def construct(self):
        tb, liq, ds, datp, c3, a, tlab, lp = build_state(c3_on=False)
        self.add(tb, liq, *ds, datp, c3, a, tlab, lp)

        d = disc([TX, TY + TH / 2 + 0.6, 0], 0.32)
        pl = T("pure protein", 26, ORANGE).move_to([-5.0, 2.5, 0])
        self.at("added the pure")
        self.play(FadeIn(d, scale=0.5), FadeIn(pl, shift=RIGHT * 0.1), run_time=0.6)
        self.at("protein back")
        self.play(d.animate.move_to([TX + 0.3, TY - 0.3, 0]), run_time=1.0)
        self.at("restored")
        self.play(*casp_on(c3), Transform(lp, lamp([RX, RY - 1.2, 0], True)), run_time=0.6)

        nm = T("cytochrome c", 30, ORANGE, weight=BOLD).move_to([-5.0, 0.3, 0])
        ptr = Line([-4.0, 0.15, 0], [TX - 0.1, TY - 0.2, 0], color=ORANGE, stroke_width=3)
        self.at("The protein was")
        self.play(FadeOut(pl), FadeIn(nm, shift=RIGHT * 0.1), Create(ptr), Indicate(d, color=ORANGE, scale_factor=1.4), run_time=0.8)

        j1 = chip("job one: carries electrons\nto complex IV", GREY, size=24)
        j2 = chip("job two: the order to take\nthe cell apart", ORANGE, size=24)
        j1.move_to([RX, 2.65, 0]); j2.move_to([RX, 1.2, 0])
        self.at("carries electrons")
        self.play(FadeIn(j1, shift=DOWN * 0.15), run_time=0.6)
        self.at("second job")
        self.play(FadeIn(j2, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


W4 = np.array([-1.6, 0.35, 0.0])
R4 = 2.0


def spoke(k, r=R4):
    a = PI / 2 + k * TAU / 7
    return W4 + r * np.array([np.cos(a), np.sin(a), 0])


class S04Partner(SpokenScene):
    def construct(self):
        scatter = [(-5.5, 2.4), (-3.9, 2.9), (-5.6, 0.7), (1.2, 3.0), (2.6, 2.2), (2.4, -1.6), (-5.2, -1.4)]
        ap = [Circle(radius=0.4, stroke_color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.3).move_to([x, y, 0]) for x, y in scatter]
        self.at("The next year")
        al = T("APAF-1", 36, TEAL, weight=BOLD).move_to([4.9, 1.3, 0])
        self.play(FadeIn(al, shift=LEFT * 0.1), LaggedStart(*[FadeIn(a, scale=0.5) for a in ap], lag_ratio=0.1), run_time=1.0)
        rel = T("a relative of the\nworm's CED-4", 26, GREY, line_spacing=0.9).move_to([4.9, 0.0, 0])
        self.at("a relative of")
        self.play(FadeIn(rel, shift=LEFT * 0.1), run_time=0.5)

        cy = disc([-0.6, -3.0, 0], 0.3)
        cyl = T("cytochrome c", 28, ORANGE).next_to(cy, RIGHT, buff=0.2)
        dp = chip("dATP", TEXT, size=26).move_to([-3.4, W4[1], 0])
        self.at("Cytochrome c and")
        self.play(FadeIn(cy, scale=0.5), FadeIn(cyl), FadeIn(dp, shift=RIGHT * 0.2), run_time=0.7)
        hub = Circle(radius=0.8, stroke_color=TEAL, stroke_width=3.5, fill_color=TEAL, fill_opacity=0.18).move_to(W4)
        self.at("seven copies")
        self.play(FadeOut(rel), FadeOut(al), FadeOut(cyl), cy.animate.move_to(W4).scale(0.5), dp.animate.move_to(W4).scale(0.3), FadeIn(hub, scale=0.5), run_time=0.7)
        self.play(FadeOut(cy), FadeOut(dp), run_time=0.2)
        self.at("assemble into a wheel")
        self.play(*[a.animate.move_to(spoke(k)) for k, a in enumerate(ap)], run_time=1.3)
        wl = T("apoptosome", 34, TEXT).move_to([4.2, 1.6, 0])
        wl2 = T("seven APAF-1", 28, TEAL).move_to([4.2, 0.95, 0])
        self.at("the apoptosome")
        self.play(FadeIn(wl, shift=LEFT * 0.1), FadeIn(wl2, shift=LEFT * 0.1), Indicate(hub, color=TEAL, scale_factor=1.1), run_time=0.7)
        caps = [casp("caspase-9", 1.9, 0.95, 22, pos=[-5.2, y, 0]) for y in (2.5, 1.4, 0.3, -0.8)]
        self.at("It gathers caspase")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in caps], lag_ratio=0.15), run_time=0.7)
        self.play(*[FadeOut(c.lbl) for c in caps], run_time=0.2)
        minis = [(-0.25, 0.25), (0.25, 0.25), (-0.25, -0.25), (0.25, -0.25)]
        self.play(*[Transform(c, casp("", 0.42, 0.42, pos=W4 + [mx, my, 0])) for c, (mx, my) in zip(caps, minis)], run_time=0.9)

        gl = T("caspase-9", 30, RED).move_to([4.2, 0.3, 0])
        self.play(FadeIn(gl, shift=LEFT * 0.1), run_time=0.4)

        # clear the wheel; the rule as two rows
        self.at("Take cytochrome c")
        wheel = VGroup(*ap, hub, wl, wl2, gl, *caps)
        title = T("cytochrome c", 38, ORANGE, weight=BOLD).move_to([0, 2.7, 0])
        r1 = T("taken away", 34, TEXT).move_to([-4.2, 0.7, 0])
        r2 = T("given back", 34, TEXT).move_to([-4.2, -1.6, 0])
        c1 = casp("caspase-3", 3.0, 1.3, 28, pos=[1.4, 0.7, 0])
        c2 = casp("caspase-3", 3.0, 1.3, 28, pos=[1.4, -1.6, 0], active=False)
        a1 = arr([-2.5, 0.7, 0], [-0.4, 0.7, 0], GREY, w=6)
        a2 = arr([-2.5, -1.6, 0], [-0.4, -1.6, 0], GREY, w=6)
        l1 = T("reaction stops", 30, GREY).move_to([5.0, 0.7, 0])
        l2 = T("restored", 30, GREEN).move_to([5.0, -1.6, 0])
        self.play(FadeOut(wheel), FadeIn(title), run_time=0.6)
        self.play(FadeIn(r1, shift=RIGHT * 0.1), GrowArrow(a1), FadeIn(c1), run_time=0.6)
        self.at("the reaction stops")
        self.play(FadeIn(l1, shift=LEFT * 0.1), run_time=0.5)
        self.at("Give it back")
        self.play(FadeIn(r2, shift=RIGHT * 0.1), GrowArrow(a2), FadeIn(c2), run_time=0.6)
        self.at("it is restored")
        self.play(*casp_on(c2), FadeIn(l2, shift=LEFT * 0.1), run_time=0.6)
        self.finish()


class S05End(EndCard):
    LINE = "Take cytochrome c away and the reaction stops."
