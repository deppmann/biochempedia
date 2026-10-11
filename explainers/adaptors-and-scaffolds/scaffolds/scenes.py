"""Scaffolds: what a cell gets from holding a pathway together  (Biochemistrypedia section film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = pheromone (the signal outside the yeast cell)
  PURPLE = a kinase (Ste11, Ste7, Fus3 and the kinases drawn as "kinase")
  TEAL   = the scaffold, Ste5 (the long bar with slots)
  ORANGE = the response (mating)
  GREEN  = switched on / activated link
  GOLD   = a phosphate (the round "P" badge)
  RED    = ruled out (no phosphate, no mating, "nowhere near")
  GREY   = other cascades, proteins that are not named kinases of the story, labels

No molecular structures: kinases are labelled pills, the scaffold is a bar, a region of the scaffold is a
slot that a kinase's peg fits into (pegs and slots are idealised and not to scale).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

KW, KH = 1.9, 0.8        # kinase pill
PEG_L = 0.5              # peg length
SLOT_D = 0.5             # slot depth
BAR_H = 1.3


def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24):
    t = T(text, size, GREY)
    w, h = t.width + 0.4, t.height + 0.34
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h)
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(back, DashedVMobject(box, num_dashes=max(18, int(w * 9))).set_color(GREY), t)
    g.t = t
    return g


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(r=0.24):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22, BG, weight=BOLD).move_to(c))


def cross_at(p, r=0.24, color=RED, w=7):
    p = np.array(list(p)[:2] + [0], float)
    return VGroup(Line(p + [-r, -r, 0], p + [r, r, 0], color=color, stroke_width=w),
                  Line(p + [-r, r, 0], p + [r, -r, 0], color=color, stroke_width=w))


def kinase(name, pw=0.7, color=PURPLE, peg=True, w=KW, size=26, label_color=None):
    """a kinase pill, with an optional peg under it. Centre of the pill is the origin of the group. [back, body, label, peg]"""
    back = RoundedRectangle(corner_radius=0.3, width=w, height=KH, stroke_width=0, fill_color=BG, fill_opacity=1)
    body = RoundedRectangle(corner_radius=0.3, width=w, height=KH, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.25)
    lab = T(name, size, label_color or color, weight=BOLD)
    pegm = Rectangle(width=pw, height=PEG_L, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.55)
    pegm.move_to([0, -KH / 2 - PEG_L / 2 + 0.04, 0])
    if not peg:
        pegm.set_opacity(0)
    mirror = Rectangle(width=0.02, height=0.02, stroke_width=0, fill_opacity=0).move_to([0, KH / 2 + PEG_L - 0.04, 0])
    g = VGroup(back, body, lab, pegm, mirror)
    g.back, g.body, g.lab, g.peg, g.pw = back, body, lab, pegm, pw
    return g


def bar_group(width, y, x=0.0, slots=(), name="Ste5", name_size=34):
    """the scaffold: a bar; slots = [(x, width)] cut into its top edge. [bar, slotmarks, label]"""
    bar = RoundedRectangle(corner_radius=0.2, width=width, height=BAR_H, stroke_color=TEAL, stroke_width=4,
                           fill_color=TEAL, fill_opacity=0.28).move_to([x, y, 0])
    top = y + BAR_H / 2
    sl = VGroup()
    for sx, sw in slots:
        s = Rectangle(width=sw, height=SLOT_D, stroke_color=TEAL, stroke_width=3, fill_color=BG, fill_opacity=1)
        s.move_to([sx, top - SLOT_D / 2, 0])
        sl.add(s)
    lab = T(name, name_size, TEAL, weight=BOLD).move_to([x, y - 0.2, 0])
    g = VGroup(bar, sl, lab)
    g.bar, g.slots, g.lab, g.top = bar, sl, lab, top
    return g


def docked_y(bar_top):
    """pill-centre height at which a peg sits fully in a slot."""
    return bar_top - SLOT_D + KH / 2 + PEG_L - 0.04


def pop(m, s=1.15):
    return m.animate(rate_func=there_and_back).scale(s)


def dimline(x0, x1, y, text, color=RED):
    line = DashedLine([x0, y, 0], [x1, y, 0], color=color, stroke_width=5, dash_length=0.16)
    caps = VGroup(Line([x0, y - 0.2, 0], [x0, y + 0.2, 0], color=color, stroke_width=5),
                  Line([x1, y - 0.2, 0], [x1, y + 0.2, 0], color=color, stroke_width=5))
    lab = T(text, 26, color).move_to([(x0 + x1) / 2 - 0.35, y + 0.55, 0])
    return VGroup(line, caps, lab)


class S00Title(TitleCard):
    LESSON = "Adaptors, Docking Proteins and Scaffolds"
    TITLE = "The Yeast Protein That Holds Three Kinases"


# ---------------------------------------------------------------------------------------------
class S01Cascade(SpokenScene):
    """three kinases in a row for mating; the top one also starts two other cascades."""

    def construct(self):
        Y = 0.0
        ste11 = bchip("Ste11", PURPLE, 30).move_to([-5.0, Y, 0])
        ste7 = bchip("Ste7", PURPLE, 30).move_to([-2.3, Y, 0])
        fus3 = bchip("Fus3", PURPLE, 30).move_to([0.5, Y, 0])
        mating = bchip("mating", ORANGE, 30).move_to([4.9, Y, 0])
        a1 = arr(ste11.get_right(), ste7.get_left())
        a2 = arr(ste7.get_right(), fus3.get_left())
        a3 = arr(fus3.get_right(), mating.get_left())

        self.at("three kinases")
        self.play(LaggedStart(FadeIn(ste11, shift=UP * 0.15), FadeIn(ste7, shift=UP * 0.15), FadeIn(fus3, shift=UP * 0.15),
                              lag_ratio=0.35), run_time=1.0)
        self.at("switches on")
        self.play(GrowArrow(a1), run_time=0.5)
        self.at("switches on", nth=1)
        self.play(GrowArrow(a2), run_time=0.5)
        self.play(GrowArrow(a3), FadeIn(mating, shift=RIGHT * 0.15), run_time=0.7)

        salt = ghost_chip("high-salt cascade").move_to([-1.0, 2.35, 0])
        fila = ghost_chip("filament cascade").move_to([-1.0, -2.35, 0])
        a_s = arr([-4.35, 0.42, 0], salt.get_left())
        a_f = arr([-4.35, -0.42, 0], fila.get_left())
        self.at("too much salt")
        self.play(GrowArrow(a_s), FadeIn(salt, shift=RIGHT * 0.15), run_time=0.7)
        self.at("long filaments")
        self.play(GrowArrow(a_f), FadeIn(fila, shift=RIGHT * 0.15), run_time=0.7)

        self.at("One enzyme")
        self.play(pop(ste11, 1.2), run_time=0.8)
        self.at("three destinations")
        self.play(pop(mating, 1.15), pop(salt, 1.1),
                  pop(fila, 1.1), run_time=0.9)

        self.finish()


# ---------------------------------------------------------------------------------------------
BAR_Y = 0.2
SLOT_X = (-3.4, 0.0, 3.4)
SLOT_W = (0.8, 0.5, 1.1)          # idealised: a different width for each region
HOVER_Y = 2.3


class S02Ste5(SpokenScene):
    """what the lab was doing: three enzymes, one protein with no enzyme activity."""

    def construct(self):
        tag = T("Elion laboratory", 28, TEXT).move_to([0, 3.3, 0])
        ks = [kinase(n, pw, peg=False).move_to([x, HOVER_Y, 0]) for n, pw, x in
              zip(("Ste11", "Ste7", "Fus3"), SLOT_W, SLOT_X)]
        self.at("Elaine Elion's")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)
        qs = VGroup()
        for x in SLOT_X:
            qs.add(T("?", 40, GREY, weight=BOLD).move_to([x, 1.3, 0]))
        bar = bar_group(10.4, BAR_Y)
        barlab = bar.lab
        bar.remove(barlab)
        self.at("which parts")
        self.play(FadeIn(bar, shift=UP * 0.2), FadeIn(qs, scale=0.8), run_time=0.8)
        self.at("three enzymes")
        self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.15) for k in ks], lag_ratio=0.3), run_time=1.0)
        self.at("protein was")
        self.play(FadeIn(barlab, scale=0.8), run_time=0.5)

        nomate = T("no Ste5, no mating", 26, RED).move_to([3.3, -2.0, 0])
        self.at("cannot mate")
        self.play(FadeIn(nomate, shift=UP * 0.1), run_time=0.6)

        noenz = T("no enzyme activity", 28, GREY).move_to([0, -1.15, 0])
        self.at("no enzyme activity")
        self.play(FadeIn(noenz, shift=UP * 0.1), run_time=0.6)
        ph = pbadge().move_to([-4.6, -2.0, 0])
        cr = cross_at([-4.6, -2.0])
        none = T("none put on, none taken off", 24, GREY).move_to([-1.9, -2.0, 0])
        self.at("never put a phosphate")
        self.play(FadeIn(ph, scale=0.6), run_time=0.4)
        self.play(Create(cr), FadeIn(none, shift=RIGHT * 0.1), run_time=0.6)

        mech = T("no mechanism?", 34, RED, weight=BOLD).move_to([0, -3.0, 0])
        yr = T("1994", 30, GOLD).move_to([5.6, 3.2, 0])
        self.at("In 1994")
        self.play(FadeIn(yr, shift=DOWN * 0.1), run_time=0.5)
        self.at("no mechanism")
        self.play(FadeIn(mech, shift=UP * 0.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Regions(SpokenScene):
    """each kinase fits a different region of one Ste5."""

    def construct(self):
        ks = [kinase(n, pw, peg=True).move_to([x, HOVER_Y, 0]) for n, pw, x in
              zip(("Ste11", "Ste7", "Fus3"), SLOT_W, SLOT_X)]
        bar = bar_group(10.4, BAR_Y, slots=[])
        self.add(bar, *ks)
        yd = docked_y(bar.top)

        cell = T("Choi, Satterberg, Lyons and Elion  ·  Cell, 1994", 26, TEXT).move_to([0, 3.35, 0])
        self.at("reported that")
        self.play(FadeIn(cell, shift=DOWN * 0.1), run_time=0.6)

        # the slots open in the bar, then the pegs fit
        slots = bar_group(10.4, BAR_Y, slots=list(zip(SLOT_X, SLOT_W)))
        self.at("different regions")
        self.play(FadeIn(slots[1], scale=1.0), run_time=0.4)
        self.bring_to_front(*ks)
        self.play(LaggedStart(*[k.animate.move_to([x, yd, 0]) for k, x in zip(ks, SLOT_X)], lag_ratio=0.35),
                  run_time=1.6)
        note = T("regions and order idealised, not to scale", 22, GREY).move_to([4.2, -1.4, 0])
        self.play(FadeIn(note), run_time=0.4)

        one = Brace(VGroup(bar[0]), direction=DOWN, color=TEAL, buff=0.55)
        onel = T("one Ste5 molecule", 28, TEAL).next_to(one, DOWN, buff=0.12)
        self.at("molecule can hold")
        self.play(GrowFromCenter(one), FadeIn(onel), run_time=0.7)
        self.at("all three at once")
        self.play(*[pop(k.body, 1.1) for k in ks], run_time=0.9)

        w1 = ghost_chip("Michael Wigler's group, PNAS", 24)
        w2 = ghost_chip("George Sprague's group, Genetics", 24)
        for c in (w1, w2):
            c.t.set_color(TEXT)
        w1.move_to([-3.2, -2.55, 0])
        w2.move_to([3.2, -2.55, 0])
        self.at("Two other laboratories")
        self.play(FadeIn(w1, shift=UP * 0.12), FadeIn(w2, shift=UP * 0.12), run_time=0.8)
        tw = T("same result, same year", 24, GREY).move_to([0, -3.3, 0])
        self.at("same result")
        self.play(FadeIn(tw, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Buys(SpokenScene):
    """speed (free vs fastened), insulation (Ste11 beside Fus3, far from the drying-out kinase), the rule."""

    def construct(self):
        # --- speed ---------------------------------------------------------------------------
        lt = T("free in the cytoplasm", 28, GREY).move_to([-3.3, 2.75, 0])
        rt = T("fastened to one scaffold", 28, TEAL).move_to([3.4, 2.75, 0])
        div = Line([0, 3.0, 0], [0, -3.2, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        fk = kinase("kinase", peg=False, w=1.7, size=24).move_to([-5.0, 0.6, 0])
        ft = kinase("target", peg=False, w=1.7, size=24, color=GREY).move_to([-1.5, 0.6, 0])
        self.at("buys speed")
        self.play(FadeIn(div), FadeIn(lt), FadeIn(fk), FadeIn(ft), run_time=0.7)

        self.at("drifting at random")
        pk = [np.array(p, float) for p in [(-5.0, 0.6), (-4.4, 1.5), (-4.9, 0.0), (-4.2, -1.1), (-4.8, -1.8), (-4.4, -0.6)]]
        pt = [np.array(p, float) for p in [(-1.5, 0.6), (-2.0, -0.4), (-1.6, -1.6), (-2.2, -0.9), (-1.7, 0.4), (-2.1, 1.4)]]
        pk = [np.append(p[:2], 0) for p in pk]
        pt = [np.append(p[:2], 0) for p in pt]
        mk = VMobject().set_points_as_corners(pk)
        mt = VMobject().set_points_as_corners(pt)
        trail_k = DashedVMobject(mk, num_dashes=40).set_color(PURPLE).set_stroke(opacity=0.5, width=3)
        trail_t = DashedVMobject(mt, num_dashes=40).set_color(GREY).set_stroke(opacity=0.5, width=3)
        idl = T("idealised path", 22, GREY).move_to([-3.3, -3.0, 0])
        self.play(MoveAlongPath(fk, mk), MoveAlongPath(ft, mt), Create(trail_k), Create(trail_t), FadeIn(idl),
                  run_time=1.8, rate_func=linear)

        bar = bar_group(4.5, -0.6, x=3.4, slots=[(2.4, 0.7), (4.4, 0.7)], name="scaffold", name_size=30)
        yd = docked_y(bar.top)
        sk = kinase("kinase", 0.7, w=1.9, size=24).move_to([2.4, yd + 1.8, 0])
        st = kinase("target", 0.7, w=1.9, size=24, color=GREY).move_to([4.4, yd + 1.8, 0])
        # kinase and target each 1.9 wide, 2.0 apart: they touch once docked at 0.1 gap-free spacing
        self.at("On one scaffold")
        self.play(FadeIn(rt), FadeIn(bar), FadeIn(sk), FadeIn(st), run_time=0.6)
        self.play(sk.animate.move_to([2.45, yd, 0]), st.animate.move_to([4.35, yd, 0]), run_time=0.8)
        self.at("already touching")
        self.play(pop(sk.body, 1.08), pop(st.body, 1.08),
                  run_time=0.8)

        # --- insulation ----------------------------------------------------------------------
        self.at("buys insulation")
        clear = VGroup(lt, rt, div, fk, ft, trail_k, trail_t, idl, bar, sk, st)
        self.play(FadeOut(clear), run_time=0.6)

        b2 = bar_group(6.8, -1.5, x=-2.6, slots=[(-4.8, 0.8), (-2.9, 0.5), (-1.0, 1.1)], name="Ste5", name_size=34)
        yd2 = docked_y(b2.top)
        k11 = kinase("Ste11", 0.8).move_to([-4.8, yd2, 0])
        k7 = kinase("Ste7", 0.5, color=GREY).move_to([-2.9, yd2, 0])
        f3 = kinase("Fus3", 1.1).move_to([-1.0, yd2, 0])
        self.play(FadeIn(b2), FadeIn(k11), FadeIn(k7), FadeIn(f3), run_time=0.7)
        pher = bchip("pheromone", YELLOW, 26).move_to([-4.8, 2.5, 0])
        a_p = arr([-4.8, 2.15, 0], [-4.8, yd2 + 0.45, 0], YELLOW)
        self.at("pheromone switches on")
        self.play(FadeIn(pher, shift=DOWN * 0.15), GrowArrow(a_p), run_time=0.6)
        self.play(k11.body.animate.set_stroke(GREEN).set_fill(GREEN, 0.3), k11.lab.animate.set_color(GREEN),
                  k11.peg.animate.set_stroke(GREEN).set_fill(GREEN, 0.55), run_time=0.5)
        self.at("sits against")
        self.play(pop(k11.body, 1.06), pop(f3.body, 1.06),
                  run_time=0.8)

        dry = ghost_chip("drying-out kinase", 24).move_to([4.8, yd2, 0])
        gap = dimline(0.9, dry.get_left()[0] - 0.15, yd2, "nowhere near")
        self.at("nowhere near")
        self.play(Create(gap[0]), FadeIn(gap[1]), FadeIn(gap[2], shift=DOWN * 0.1), FadeIn(dry, shift=LEFT * 0.15),
                  run_time=0.9)

        # --- the rule ------------------------------------------------------------------------
        self.at("catalyzes nothing")
        zap = VGroup(pher, a_p, dry, gap)
        row = VGroup(b2, k11, k7, f3)
        nothing = T("no enzyme activity", 28, GREY).move_to([0, -2.3, 0])
        self.play(FadeOut(zap), row.animate.move_to([0, 0.4, 0]).shift(UP * 0), run_time=0.8)
        nothing.next_to(b2, DOWN, buff=0.35)
        self.play(FadeIn(nothing, shift=UP * 0.1), run_time=0.5)
        sp = bchip("speed", TEAL, 30).move_to([-2.2, -2.9, 0])
        ins = bchip("insulation", TEAL, 30).move_to([2.2, -2.9, 0])
        self.at("earns its place")
        self.play(FadeIn(sp, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(ins, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S05End(EndCard):
    LINE = "A protein that catalyzes nothing earns its place by what it buys."
