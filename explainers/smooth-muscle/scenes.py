"""Smooth muscle force is a balance  (Biochemistrypedia explainer, Physiology course)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = calcium
  GREEN  = myosin light-chain kinase (MLCK), the phosphorylating side
  RED    = myosin light-chain phosphatase (MLCP), and "no" / blocked marks
  GOLD   = a phosphate (the little "P" badge)
  BLUE   = myosin, the muscle in the wall, and the force gauge
  PURPLE = RhoA and Rho kinase (calcium sensitization input)
  ORANGE = nitric oxide, cGMP, protein kinase G (the opposite arrow)
  TEAL   = pressure
  GREY   = structure: actin, hose, beam, outlines, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def pbadge(size=0.24):
    c = Circle(radius=size, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def cross(center, s=0.35, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w),
                  Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w))


class Ring:
    """Cross-section of a vessel: wall annulus + lumen, with arrows that show the pressure.
    cx, r (lumen radius), p (pressure 0..1) and o (opacity 0..1) are ValueTrackers."""

    def __init__(self, cx, cy, r, thick, color, n=8):
        self.cx, self.cy, self.thick, self.color, self.n = ValueTracker(cx), cy, thick, color, n
        self.r, self.p, self.o = ValueTracker(r), ValueTracker(0.0), ValueTracker(0.0)
        self.wall = always_redraw(self._wall)
        self.arrows = always_redraw(self._arrows)

    def _wall(self):
        o = self.o.get_value()
        a = Annulus(inner_radius=self.r.get_value(), outer_radius=self.r.get_value() + self.thick,
                    color=self.color, fill_opacity=0.4 * o, stroke_width=3)
        a.set_stroke(self.color, width=3, opacity=o)
        return a.move_to([self.cx.get_value(), self.cy, 0])

    def _arrows(self):
        g = VGroup()
        o = self.o.get_value()
        p = self.p.get_value()
        if o < 0.02 or p < 0.02:
            return g
        c = np.array([self.cx.get_value(), self.cy, 0])
        rr = self.r.get_value()
        for k in range(self.n):
            ang = k * TAU / self.n + TAU / 16
            d = np.array([np.cos(ang), np.sin(ang), 0])
            g.add(Arrow(c + d * rr * 0.3, c + d * (rr - 0.1), buff=0, color=TEAL, stroke_width=2 + 6 * p,
                        tip_length=0.2, max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20))
        return g

    def mobs(self):
        return [self.wall, self.arrows]


H = 4.7      # half beam length
CY = -0.35   # beam height
GY = -2.75   # force gauge height


class See:
    """The kinase / phosphatase seesaw. wa = kinase weight, wb = phosphatase weight (ValueTrackers).
    Left end down means more phosphorylation, which is more force."""

    def __init__(self, wa=0.5, wb=0.5):
        self.wa, self.wb = ValueTracker(wa), ValueTracker(wb)
        self.ka = chip("MLCK kinase", GREEN, 30)
        self.pb = chip("MLCP phosphatase", RED, 30)
        self.h_a, self.h_b = self.ka.height, self.pb.height
        self.oa, self.ob = ValueTracker(1.0), ValueTracker(1.0)
        self.ka.add_updater(lambda m: self._place(m, self.wa, self.h_a, -1, self.oa))
        self.pb.add_updater(lambda m: self._place(m, self.wb, self.h_b, +1, self.ob))
        self.beam = always_redraw(self._beam)
        self.pivot = Triangle(color=GREY, fill_opacity=0.5, stroke_width=3).scale(0.5).move_to([0, CY - 0.5, 0])
        self.gauge_box = Rectangle(width=6, height=0.42, stroke_color=GREY, stroke_width=3).move_to([0, GY, 0])
        self.gauge_fill = always_redraw(self._fill)
        self.gauge_lbl = T("force", 26, BLUE).move_to([-4.2, GY, 0])
        self.note = T("schematic, not to scale", 22, GREY).move_to([-4.3, -3.35, 0])

    def th(self):
        return 0.35 * (self.wa.get_value() - self.wb.get_value())

    def force(self):
        return float(np.clip(0.5 + 1.4 * self.th(), 0.03, 0.98))

    def end(self, side):
        th = self.th()
        return np.array([side * H * np.cos(th), CY + side * H * np.sin(th), 0])

    def _place(self, m, w, h0, side, o):
        sc = 0.75 + 0.35 * w.get_value()
        m.scale(sc * h0 / m.height)
        e = self.end(side)
        lift = (m.width - 0.5) * np.tan(max(0.0, -side * self.th())) + 0.12
        m.move_to([e[0] - side * (m.width / 2 - 0.5), e[1] + 0.3 + m.height / 2 + lift, 0])
        ov = o.get_value()
        m[0].set_stroke(opacity=ov)
        m[0].set_fill(opacity=0.16 * ov)
        m[1].set_opacity(ov)

    def _beam(self):
        return Line(self.end(-1), self.end(1), color=GREY, stroke_width=10)

    def _fill(self):
        f = self.force()
        return Rectangle(width=6 * f, height=0.42, stroke_width=0, fill_color=BLUE, fill_opacity=0.85
                         ).move_to([-3 + 3 * f, GY, 0])

    def base_mobs(self):
        return [self.beam, self.pivot, self.gauge_box, self.gauge_fill, self.gauge_lbl, self.note]


def ca_chip(x=-4.9, y=2.75):
    return chip("calcium", YELLOW, 28).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Smooth muscle and the myogenic response"
    TITLE = "Smooth muscle force is a balance"


# ---------------------------------------------------------------------------------------------
class S01Hose(SpokenScene):
    """a hose bulges, a small artery narrows against the stretch; built into the wall, not the brain."""

    def construct(self):
        hose = Ring(-3.6, 0.0, 1.5, 0.35, GREY)
        art = Ring(3.6, 0.0, 1.5, 0.6, BLUE)
        hose_lbl = T("garden hose", 32, GREY).move_to([-3.6, 3.05, 0])
        art_lbl = T("small artery", 32, BLUE).move_to([3.6, 3.05, 0])
        wall_lbl = T("muscle in the wall", 26, BLUE).move_to([3.6, -2.8, 0])
        tip = T("pressure rises", 28, TEAL).move_to([0, 3.05, 0])
        self.add(*hose.mobs(), *art.mobs())

        self.at("garden hose")
        self.play(hose.o.animate.set_value(1), FadeIn(hose_lbl), run_time=0.5)
        self.at("bulges")
        self.play(FadeIn(tip), hose.p.animate.set_value(1), hose.r.animate.set_value(1.95), run_time=1.0)

        self.at("small artery")
        self.play(art.o.animate.set_value(1), FadeIn(art_lbl), run_time=0.5)
        self.at("in its wall")
        self.play(FadeIn(wall_lbl), run_time=0.4)
        self.at("pushes back")
        self.play(art.p.animate.set_value(1), run_time=0.5)
        self.at("narrows against")
        self.play(art.r.animate.set_value(1.05), run_time=0.9)

        # keep the artery, drop the hose
        self.at("built into the muscle")
        self.play(FadeOut(hose_lbl), hose.o.animate.set_value(0), hose.p.animate.set_value(0), FadeOut(tip),
                  art.cx.animate.set_value(2.4), art_lbl.animate.move_to([2.4, 3.05, 0]),
                  wall_lbl.animate.move_to([2.4, -2.8, 0]), run_time=1.0)
        brain = chip("brain", GREY, 30).move_to([-4.9, 0.0, 0])
        link = DashedLine([-3.6, 0.0, 0], [0.5, 0.0, 0], color=GREY, stroke_width=4, dash_length=0.18)
        x = cross([-1.5, 0.0, 0])
        self.at("wired in")
        self.play(FadeIn(brain), Create(link), run_time=0.7)
        self.play(FadeIn(x, scale=0.6), run_time=0.3)
        q = T("?", 96, TEXT, weight=BOLD).move_to([5.5, 0.0, 0])
        self.at("sensing")
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.play(Indicate(q, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Switch(SpokenScene):
    """no troponin; calcium -> calmodulin -> MLCK; a phosphate on the regulatory light chain; the head cycles."""

    def construct(self):
        ay = -2.75
        actin = Line([-5.8, ay, 0], [5.8, ay, 0], color=GREY, stroke_width=9)
        dots = VGroup(*[Dot([x, ay, 0], radius=0.11, color=TEXT) for x in np.arange(-5.0, 5.5, 0.9)])
        act_lbl = T("thin filament (actin)", 24, GREY).move_to([-3.8, ay - 0.5, 0])
        title = T("smooth muscle", 40, font=TITLE_FONT).move_to([0, 1.2, 0])
        self.at("smooth muscle")
        self.play(FadeIn(title), run_time=0.6)
        self.play(title.animate.move_to([0, 3.0, 0]).scale(0.75), FadeIn(actin), FadeIn(dots), run_time=0.7)

        trop = chip("troponin", GREY, 28).move_to([-2.4, -1.45, 0])
        xx = Line(trop.get_left() + LEFT * 0.15, trop.get_right() + RIGHT * 0.15, color=RED, stroke_width=7)
        no_lbl = T("not in smooth muscle", 24, RED).move_to([-2.4, -0.55, 0])
        self.at("no troponin")
        self.play(FadeIn(trop, shift=DOWN * 0.15), run_time=0.4)
        self.play(FadeIn(xx, scale=0.6), FadeIn(no_lbl), run_time=0.4)
        self.at("thin filament")
        self.play(Indicate(VGroup(actin, act_lbl), color=TEXT, scale_factor=1.03), FadeIn(act_lbl), run_time=0.7)

        # myosin
        blob = RoundedRectangle(corner_radius=0.3, width=9.4, height=1.0, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.25).move_to([0.2, -0.65, 0])
        m_lbl = T("myosin", 28, BLUE).move_to([-3.3, -0.65, 0])
        hx = 2.4
        head = RoundedRectangle(corner_radius=0.2, width=0.62, height=1.25, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.45).move_to([hx, -1.78, 0])
        tab = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.3, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.5).move_to([hx, -0.06, 0])
        self.at("switch sits")
        self.play(FadeOut(trop), FadeOut(xx), FadeOut(no_lbl), FadeOut(title), run_time=0.4)
        self.play(FadeIn(blob), FadeIn(m_lbl), FadeIn(head), FadeIn(tab), run_time=0.8)

        # the chain
        ca = chip("calcium", YELLOW, 28).move_to([-5.1, 2.5, 0])
        cam = chip("calmodulin", YELLOW, 28).move_to([-2.4, 2.5, 0])
        kin = chip("myosin light-chain kinase", GREEN, 26).move_to([2.55, 2.5, 0])
        a1 = arr(ca.get_right(), cam.get_left(), YELLOW)
        a2 = arr(cam.get_right(), kin.get_left(), YELLOW)
        self.at("Calcium binds")
        self.play(FadeIn(ca, shift=DOWN * 0.15), run_time=0.4)
        self.play(GrowArrow(a1), FadeIn(cam), run_time=0.6)
        self.at("together activate")
        self.play(GrowArrow(a2), FadeIn(kin), run_time=0.7)

        a3 = arr([hx, 2.05, 0], [hx, 0.3, 0], GREEN)
        self.at("puts a phosphate")
        self.play(GrowArrow(a3), run_time=0.4)
        pb = pbadge().move_to([hx, 1.7, 0])
        self.add(pb)
        self.play(pb.animate.move_to([hx + 0.55, 0.28, 0]), run_time=0.6)
        self.play(tab.animate.set_stroke(GREEN).set_fill(GREEN, 0.6), FadeOut(a3), run_time=0.4)
        rl = T("regulatory light chain", 24, GREEN).move_to([-0.35, 0.55, 0])
        rl_line = Line([1.25, 0.5, 0], [hx - 0.35, 0.05, 0], color=GREEN, stroke_width=3)
        self.at("regulatory light chain")
        self.play(FadeIn(rl), Create(rl_line), run_time=0.5)

        # the head cycles on actin
        top = np.array([hx, -1.15, 0])
        self.at("motor can cycle")
        for _ in range(2):
            self.play(Rotate(head, -0.45, about_point=top), *[d.animate.shift(LEFT * 0.35) for d in dots],
                      run_time=0.6, rate_func=smooth)
            self.play(Rotate(head, 0.45, about_point=top), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Balance(SpokenScene):
    """kinase alone tilts the seesaw; the phosphatase levels it; calcium tilts it; the phosphatase tilts it at the same calcium."""

    def construct(self):
        s = See(0.5, 0.0)
        ca = ca_chip()
        ca_arrow = always_redraw(lambda: arr([-4.55, 2.35, 0], [s.ka.get_top()[0], s.ka.get_top()[1] + 0.05, 0], YELLOW))
        up = Arrow([-3.6, 2.45, 0], [-3.6, 3.1, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=0.2)
        same = T("same calcium", 24, YELLOW).move_to([-4.9, 3.4, 0])
        s.oa.set_value(0)
        s.ob.set_value(0)
        self.add(*s.base_mobs(), s.ka, s.pb)
        self.at("But the kinase")
        self.play(s.oa.animate.set_value(1), run_time=0.7)

        # phosphatase arrives and takes the phosphate off, all the time
        self.at("takes the phosphate")
        self.play(s.ob.animate.set_value(1), s.wb.animate.set_value(0.5), run_time=1.0)
        for _ in range(2):
            b = pbadge().move_to(s.ka.get_corner(UR) + [0.0, 0.05, 0])
            self.play(FadeIn(b, scale=0.5), run_time=0.15)
            self.play(b.animate.move_to(s.pb.get_corner(UL) + [0.0, 0.05, 0]).scale(0.4).set_opacity(0),
                      run_time=0.55, rate_func=linear)
            self.remove(b)
        self.at("force follows")
        self.play(Indicate(s.gauge_box, color=BLUE, scale_factor=1.06), Indicate(s.gauge_lbl, color=BLUE), run_time=0.8)

        self.at("Calcium sets")
        self.add(ca_arrow)
        self.play(FadeIn(ca, shift=DOWN * 0.1), FadeIn(up), run_time=0.5)
        self.play(s.wa.animate.set_value(0.9), run_time=0.9)
        old = s.force()
        mark = always_redraw(lambda: Line([-3 + 6 * old, GY - 0.32, 0], [-3 + 6 * old, GY + 0.32, 0],
                                          color=TEXT, stroke_width=4))
        self.at("changes the phosphatase")
        self.add(mark)
        self.play(Indicate(s.pb, color=RED, scale_factor=1.05), run_time=0.6)
        self.play(s.wb.animate.set_value(0.15), run_time=1.0)
        self.at("same calcium")
        self.play(FadeOut(up), FadeIn(same), run_time=0.4)
        more = T("more force at the same calcium", 28, TEXT).move_to([1.2, -3.3, 0])
        self.at("calcium sensitization")
        self.play(FadeIn(more, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Inputs(SpokenScene):
    """Rho kinase inhibits the phosphatase (force up at the same calcium); nitric oxide runs the other way."""

    def construct(self):
        s = See(0.5, 0.5)
        ca = ca_chip()
        ca_arrow = always_redraw(lambda: arr([-4.55, 2.35, 0], [s.ka.get_top()[0], s.ka.get_top()[1] + 0.05, 0], YELLOW))
        same = T("same calcium", 24, YELLOW).move_to([-4.9, 3.4, 0])
        self.add(*s.base_mobs(), s.ka, s.pb, ca, ca_arrow, same)

        # Rho chain
        rho = chip("RhoA", PURPLE, 24).move_to([-0.7, 2.9, 0])
        rk = chip("Rho kinase", PURPLE, 24).move_to([3.3, 2.9, 0])
        r1 = arr(rho.get_right(), rk.get_left(), PURPLE)
        bar = always_redraw(lambda: inhib([rk.get_center()[0], rk.get_bottom()[1] - 0.05, 0],
                                           [rk.get_center()[0], s.pb.get_top()[1] + 0.12, 0], PURPLE))
        self.at("move the balance")
        self.play(Indicate(s.beam, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("activates")
        self.play(FadeIn(rho, shift=DOWN * 0.1), GrowArrow(r1), FadeIn(rk), run_time=0.8)
        self.at("inhibits the phosphatase")
        self.add(bar)
        self.play(FadeIn(bar), s.wb.animate.set_value(0.15), run_time=1.1)
        keep = T("phosphate stays on myosin", 28, TEXT).move_to([1.2, -3.3, 0])
        self.at("More phosphate stays")
        self.play(FadeIn(keep, shift=UP * 0.1), run_time=0.5)

        # clear the Rho answer before the nitric oxide question
        no = chip("nitric oxide", ORANGE, 24).move_to([-1.0, 2.9, 0])
        cg = chip("cGMP", ORANGE, 24).move_to([1.75, 2.9, 0])
        pk = chip("protein kinase G", ORANGE, 24).move_to([4.2, 2.9, 0])
        n1 = arr(no.get_right(), cg.get_left(), ORANGE)
        n2 = arr(cg.get_right(), pk.get_left(), ORANGE)
        up_bar = always_redraw(lambda: arr([pk.get_center()[0], pk.get_bottom()[1] - 0.05, 0],
                                           [pk.get_center()[0], s.pb.get_top()[1] + 0.12, 0], ORANGE))
        self.at("opposite arrow")
        self.remove(bar)
        self.play(FadeOut(rho), FadeOut(r1), FadeOut(rk), FadeOut(keep), s.wb.animate.set_value(0.5), run_time=0.9)
        self.at("nitric oxide")
        self.play(FadeIn(no, shift=DOWN * 0.1), run_time=0.4)
        self.at("protein kinase")
        self.play(GrowArrow(n1), FadeIn(cg), GrowArrow(n2), FadeIn(pk), run_time=0.8)
        rabbit = T("rabbit artery", 24, GREY).move_to([1.0, 2.15, 0])
        ind = T("authors' reading: indirect", 22, GREY).move_to([3.4, -1.95, 0])
        down_ca = Arrow([-3.6, 3.1, 0], [-3.6, 2.45, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=0.2)
        low = T("lower calcium", 24, YELLOW).move_to([-4.9, 3.4, 0])
        self.at("rabbit artery")
        self.play(FadeIn(rabbit), run_time=0.4)
        self.at("lower calcium")
        self.play(FadeOut(same), FadeIn(low), FadeIn(down_ca), s.wa.animate.set_value(0.3), run_time=0.9)
        self.at("indirect activation")
        self.add(up_bar)
        self.play(FadeIn(up_bar), s.wb.animate.set_value(0.85), FadeIn(ind), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Artery(SpokenScene):
    """control vs G12/G13-deleted mesenteric arteries: calcium rises in both, RhoA and constriction differ."""

    def construct(self):
        LX, RX = -3.2, 3.2
        rings = {}
        for key, cx in (("c", LX), ("k", RX)):
            rings[key] = Ring(cx, 1.1, 0.7, 0.3, BLUE)
        # bars: (frac tracker)
        bars = {}

        def make_bar(cx, y, color, fr):
            box = Rectangle(width=3.4, height=0.34, stroke_color=GREY, stroke_width=3).move_to([cx + 1.2, y, 0])
            fill = always_redraw(lambda: Rectangle(width=max(3.4 * fr.get_value(), 0.001), height=0.34, stroke_width=0,
                                                   fill_color=color, fill_opacity=0.9).move_to(
                [cx - 0.5 + 1.7 * fr.get_value() , y, 0]))
            return box, fill

        fr = {k: ValueTracker(0.0) for k in ("cCa", "kCa", "cRho", "kRho")}
        Y_CA, Y_RHO = -1.0, -1.9
        b = {}
        b["cCa"] = make_bar(LX, Y_CA, YELLOW, fr["cCa"])
        b["kCa"] = make_bar(RX, Y_CA, YELLOW, fr["kCa"])
        b["cRho"] = make_bar(LX, Y_RHO, PURPLE, fr["cRho"])
        b["kRho"] = make_bar(RX, Y_RHO, PURPLE, fr["kRho"])
        ca_l = {k: T("calcium", 24, YELLOW).move_to([cx - 2.1, Y_CA, 0]) for k, cx in (("c", LX), ("k", RX))}
        rho_l = {k: T("active RhoA", 24, PURPLE).move_to([cx - 1.95, Y_RHO, 0]) for k, cx in (("c", LX), ("k", RX))}
        for k in ca_l:
            ca_l[k].set_x(ca_l[k].get_x() + (ca_l[k].width - 1.2) / 2 * 0)
        title_c = T("control artery", 28, TEXT).move_to([LX, 3.05, 0])
        title_k = T("without G12 and G13", 26, TEXT).move_to([RX, 3.05, 0])
        sub_k = T("(in smooth muscle)", 22, GREY).move_to([RX, 2.62, 0])
        tip = T("pressure rises", 24, TEAL).move_to([0, 3.0, 0])
        out_c = T("active constriction", 24, TEXT).move_to([LX, -0.3, 0])
        out_c2 = T("no active constriction", 24, TEXT).move_to([LX, -0.3, 0])
        out_k = T("no active constriction", 24, TEXT).move_to([RX, -0.3, 0])
        note = T("schematic bars, not to scale", 22, GREY).move_to([0, -2.5, 0])
        self.add(*rings["c"].mobs(), *rings["k"].mobs())

        mouse = T("mouse mesenteric", 22, GREY).move_to([0, 2.35, 0])
        self.at("mesenteric")
        self.play(FadeIn(mouse), run_time=0.4)
        self.at("pressure myograph")
        self.play(rings["c"].o.animate.set_value(1), FadeIn(title_c), run_time=0.6)
        self.add(b["cCa"][0], b["cCa"][1])
        self.play(FadeIn(ca_l["c"]), FadeIn(b["cCa"][0]), run_time=0.4)
        self.at("with pressure")
        self.play(FadeIn(tip), rings["c"].p.animate.set_value(1), fr["cCa"].animate.set_value(0.75),
                  rings["c"].r.animate.set_value(0.5), FadeIn(out_c), run_time=1.2)

        self.at("Arteries lacking")
        self.add(b["kCa"][1])
        self.play(rings["k"].o.animate.set_value(1), FadeIn(title_k), FadeIn(sub_k), FadeIn(ca_l["k"]),
                  FadeIn(b["kCa"][0]), run_time=0.7)
        self.play(rings["k"].p.animate.set_value(1), fr["kCa"].animate.set_value(0.75), run_time=0.9)
        self.at("no active constriction")
        self.play(FadeIn(out_k), run_time=0.8)
        self.at("less active")
        self.add(b["cRho"][1], b["kRho"][1])
        self.play(FadeIn(rho_l["c"]), FadeIn(rho_l["k"]), FadeIn(b["cRho"][0]), FadeIn(b["kRho"][0]),
                  fr["cRho"].animate.set_value(0.8), fr["kRho"].animate.set_value(0.12), FadeIn(note), run_time=1.2)

        # inhibitor in the control artery
        title_c2 = VGroup(T("control artery", 28, TEXT), T("+ Rho kinase inhibitor", 26, PURPLE)
                          ).arrange(DOWN, buff=0.08).move_to([LX, 3.0, 0])
        self.at("inhibitor blocked")
        self.play(ReplacementTransform(title_c, title_c2), rings["c"].r.animate.set_value(0.7),
                  ReplacementTransform(out_c, out_c2), fr["cCa"].animate.set_value(0.0), fr["cRho"].animate.set_value(0.0),
                  FadeOut(ca_l["c"]), FadeOut(rho_l["c"]), FadeOut(b["cCa"][0]), FadeOut(b["cRho"][0]), run_time=1.1)

        stat = chip("a calcium rise + Rho-dependent sensitization", PURPLE, 26).move_to([0, -3.1, 0])
        self.at("two things")
        self.play(FadeOut(note), FadeIn(stat, shift=UP * 0.1), run_time=0.6)
        unk = chip("how the pathways are wired upstream: ?", GREY, 26).move_to([0, -3.1, 0])
        self.at("unsettled")
        self.play(ReplacementTransform(stat, unk), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Flow(SpokenScene):
    """idealized rigid arteriole: flow ratio against radius from the fourth-power law; the closing rule."""

    def construct(self):
        # --- left: the vessel ------------------------------------------------------------------
        LCX, LCY = -3.6, 0.55
        rad = ValueTracker(100.0)
        k = 0.0125   # drawing units per micrometre

        def wall():
            r = rad.get_value() * k
            a = Annulus(inner_radius=r, outer_radius=r + 0.25, color=BLUE, fill_opacity=0.4, stroke_width=3)
            return a.move_to([LCX, LCY, 0])

        ghost = DashedVMobject(Circle(radius=100 * k, color=GREY, stroke_width=3).move_to([LCX, LCY, 0]), num_dashes=40)
        vessel = always_redraw(wall)
        formula = M("Q  ∝  ΔP x r^4", 34, TEXT).move_to([-3.2, 2.95, 0])
        tag = T("idealized rigid arteriole, made-up numbers", 22, GREY).move_to([-3.2, -3.35, 0])
        dp = T("ΔP = 60 mmHg", 28, TEAL).move_to([-3.6, -2.0, 0])
        rl = T("radius = 100 µm", 28, BLUE).move_to([-3.6, -2.7, 0])

        # --- right: flow against radius, computed from the equation -----------------------------
        X0, Y0 = 0.2, -2.55          # origin (r = 88, Q = 0.4)
        sx, sy = 6.0 / 19.0, 4.0 / 1.5

        def P(r, q):
            return np.array([X0 + (r - 88) * sx, Y0 + (q - 0.4) * sy, 0])

        ax = VGroup(Line(P(88, 0.4), P(107, 0.4), color=GREY, stroke_width=3),
                    Line(P(88, 0.4), P(88, 1.9), color=GREY, stroke_width=3))
        ticks = VGroup()
        for r in (90, 100):
            ticks.add(Line(P(r, 0.4), P(r, 0.4) + DOWN * 0.1, color=GREY, stroke_width=3),
                      T(str(r), 22, GREY).move_to(P(r, 0.4) + DOWN * 0.35))
        for q in (1.0, 1.5):
            ticks.add(Line(P(88, q), P(88, q) + LEFT * 0.1, color=GREY, stroke_width=3),
                      T(f"{q:g}", 22, GREY).move_to(P(88, q) + LEFT * 0.4))
        xl = T("radius (µm)", 24, GREY).move_to(P(97.5, 0.4) + DOWN * 0.75)
        yl = T("flow, relative to baseline", 24, GREY).move_to([3.4, 2.5, 0])
        base = DashedLine(P(88, 1.0), P(107, 1.0), color=GREY, stroke_width=3, dash_length=0.15)
        curve = ParametricFunction(lambda t: P(t, (80 / 60) * (t / 100) ** 4), t_range=[89, 107], color=TEAL, stroke_width=5)
        crv_lbl = T("ΔP = 80 mmHg", 24, TEAL).move_to(P(104.6, 1.9) + LEFT * 0.35)

        self.at("proportional to")
        self.play(FadeIn(formula), run_time=0.6)
        self.at("numbers")
        self.play(FadeIn(ghost), FadeIn(vessel), FadeIn(tag), run_time=0.6)
        self.play(FadeIn(dp), FadeIn(rl), run_time=0.6)

        dot = Dot(P(100, 1.0), radius=0.13, color=TEXT)
        base_lbl = T("baseline", 24, TEXT).move_to(P(100, 1.0) + DOWN * 0.45)
        self.at("Raise the difference")
        self.play(Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), Create(base), run_time=0.9)
        self.play(FadeIn(dot, scale=0.6), FadeIn(base_lbl), Create(curve), FadeIn(crv_lbl),
                  Transform(dp, T("ΔP = 80 mmHg", 28, TEAL).move_to(dp)), run_time=1.0)
        d2 = Dot(P(105, 1.05 ** 4 * 80 / 60), radius=0.13, color=TEXT)
        lab_a = T("+62% flow", 26, TEXT).move_to(P(105, 1.62) + LEFT * 1.55 + DOWN * 0.05)
        self.at("stretched")
        self.play(FadeOut(base_lbl), ReplacementTransform(dot, d2), rad.animate.set_value(105),
                  Transform(rl, T("radius +5%", 28, BLUE).move_to(rl)), run_time=1.0)
        self.at("more flow")
        self.play(FadeIn(lab_a), run_time=0.5)

        t = ValueTracker(105.0)
        d3 = always_redraw(lambda: Dot(P(t.get_value(), (80 / 60) * (t.get_value() / 100) ** 4), radius=0.13, color=TEXT))
        lab_b = T("flow back to baseline", 26, TEXT).move_to(P(94.6, 1.0) + UP * 0.55 + RIGHT * 1.9)
        lab_c = T("radius = 93.1 µm (−6.9%)", 28, BLUE).move_to(rl)
        self.at("hold flow constant")
        self.remove(d2)
        self.add(d3)
        self.play(FadeOut(lab_a), run_time=0.3)
        self.at("must fall")
        self.play(t.animate.set_value(93.1), rad.animate.set_value(93.1), ReplacementTransform(rl, lab_c), run_time=1.5)
        self.at("narrowing")
        self.play(FadeIn(lab_b), run_time=0.5)

        # --- the rule ---------------------------------------------------------------------------
        l1 = Text("calcium sets the switch", font=TITLE_FONT, font_size=46, color=TEXT, t2c={"calcium": YELLOW})
        l2 = Text("sensitivity sets the gain", font=TITLE_FONT, font_size=46, color=TEXT, t2c={"sensitivity": RED})
        rule = VGroup(l1, l2).arrange(DOWN, buff=0.5).move_to([0, 0.2, 0])
        self.at("Keep one rule")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        self.at("calcium sets")
        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.6)
        self.at("sensitivity sets")
        self.play(FadeIn(l2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Calcium sets the switch; sensitivity sets the gain."
