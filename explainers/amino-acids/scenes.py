"""Amino acids: pH sets an amino acid's charge.

COLOR MAP (kept for the whole video)
  YELLOW = pH (the dial that moves)        GREEN = pKa (the fixed property of a group)
  RED    = positive charge / protonated    BLUE  = negative charge / deprotonated, and the base (OH-) in the burette
  GOLD   = net-zero / the pI               TEAL  = R group, side chain, histidine
  GREY   = backbone, neutral, labels       TEXT  = the proton token
No molecular structures are drawn anywhere: amino acids are labelled chips, the rest is plots from equations.
"""
import numpy as np
from bp_style import *

# ---------------------------------------------------------------- word times (seconds into each clip)
# taken from a word-level transcript of the actual slide audio


class AA(NarratedScene):
    def at(self, t):
        rem = t - self.elapsed()
        if rem > 0.02:
            self.wait(rem)

    def do(self, t, *anims, run=0.8, **kw):
        self.at(t)
        self.play(*anims, run_time=run, **kw)


def box(text, color, size=26, pad=0.2, fill=0.14, tcolor=TEXT, font=FONT, w=None):
    """Chip whose label stays readable white while the outline carries the concept colour."""
    label = Text(text, font=font, font_size=size, color=tcolor)
    width = max(label.width + 2 * pad, w or 0)
    r = RoundedRectangle(corner_radius=0.14, width=width, height=label.height + 2 * pad + 0.04,
                         stroke_color=color, stroke_width=2.8, fill_color=color, fill_opacity=fill)
    return VGroup(r, label.move_to(r))


def dim(mob, a):
    """Scale every fill/stroke opacity by a (set_opacity would flatten translucent fills to solid)."""
    for sm in mob.family_members_with_points():
        sm.set_fill(opacity=sm.get_fill_opacity() * a)
        sm.set_stroke(opacity=sm.get_stroke_opacity() * a)
    return mob


def smooth01(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# ================================================================== TITLE
class S00Title(TitleCard):
    LESSON = "Amino acids"
    TITLE = "pH Sets an Amino Acid's Charge"


# ================================================================== 1 ROADMAP
class S01Roadmap(AA):
    def construct(self):
        W, H, Y = 3.85, 4.9, -0.1
        xs = [-4.3, 0, 4.3]
        cards = [RoundedRectangle(corner_radius=0.22, width=W, height=H, stroke_color=GREY, stroke_width=2.5,
                                  fill_color=GREY, fill_opacity=0.07).move_to([x, Y, 0]) for x in xs]
        heads = [T(h, size=38, weight=BOLD).move_to(c.get_top() + DOWN * 0.65)
                 for h, c in zip(["1  Structure", "2  Charge", "3  Behavior"], cards)]
        backbone = box("backbone", GREY, 34).move_to(cards[0].get_center() + UP * 0.3)
        rgrp = box("R group", TEAL, 40, fill=0.25).move_to(cards[0].get_center() + DOWN * 1.1)
        plus = VGroup(Circle(radius=0.5, color=RED, fill_opacity=0.22, stroke_width=3), T("+", 56, RED, weight=BOLD))
        minus = VGroup(Circle(radius=0.5, color=BLUE, fill_opacity=0.22, stroke_width=3), T("−", 56, BLUE, weight=BOLD))
        tokens = VGroup(plus, minus).arrange(RIGHT, buff=0.5).move_to(cards[1].get_center() + UP * 0.45)
        phtag = box("pH 7.4", YELLOW, 36, tcolor=YELLOW, font=MONO).move_to(cards[1].get_center() + DOWN * 1.1)
        behs = VGroup(*[box(t, GREY, 34) for t in ["folding", "binding", "catalysis"]]).arrange(DOWN, buff=0.32)
        behs.move_to(cards[2].get_center() + DOWN * 0.55)
        arrows = [Arrow(cards[0].get_right() + LEFT * 0.0, cards[1].get_left() + RIGHT * 0.0, buff=0,
                        color=TEXT, stroke_width=6, max_tip_length_to_length_ratio=0.6),
                  Arrow(cards[1].get_right(), cards[2].get_left(), buff=0,
                        color=TEXT, stroke_width=6, max_tip_length_to_length_ratio=0.6)]
        caption = T("R group  →  charge  →  function", 42, TEXT, font=TITLE_FONT).move_to([0, -3.4, 0])

        self.do(1.5, LaggedStart(*[FadeIn(c, scale=0.95) for c in cards], lag_ratio=0.25), run=1.4)
        self.do(2.14, Write(heads[0]), run=0.6)
        self.do(3.96, Write(heads[1]), run=0.6)
        self.do(4.74, Write(heads[2]), run=0.6)
        self.do(7.2, FadeIn(backbone, shift=UP * 0.15), run=0.7)
        self.do(8.7, FadeIn(rgrp, scale=0.6), run=0.6)
        self.play(Indicate(rgrp, color=TEAL, scale_factor=1.12), run_time=0.7)
        self.do(9.9, GrowArrow(arrows[0]), run=0.4)
        self.do(10.0, FadeIn(tokens, scale=0.5), run=0.6)
        self.do(10.5, FadeIn(phtag, shift=UP * 0.1), run=0.6)
        self.do(12.76, GrowArrow(arrows[1]), run=0.5)
        self.do(15.3, FadeIn(behs[0], shift=UP * 0.1), run=0.5)
        self.do(16.9, FadeIn(behs[1], shift=UP * 0.1), run=0.5)
        self.do(17.8, FadeIn(behs[2], shift=UP * 0.1), run=0.5)
        self.do(19.06, FadeIn(caption, shift=UP * 0.1), run=0.8)
        self.do(20.76, cards[0].animate.set_stroke(GOLD, 5), run=0.4)
        self.do(21.74, cards[1].animate.set_stroke(GOLD, 5), run=0.4)
        self.do(22.52, cards[2].animate.set_stroke(GOLD, 5), run=0.4)
        self.finish()


# ================================================================== 2 ZWITTERION
class S02Zwitterion(AA):
    PKA1, PKA2 = 2.3, 9.6

    def construct(self):
        pH = ValueTracker(7.4)
        show_net, show_zw = ValueTracker(0), ValueTracker(0)
        X0, SC, SY = -5.6, 0.8, 2.55

        def px(p):
            return X0 + SC * p

        strip = Line([px(0), SY, 0], [px(14), SY, 0], color=GREY, stroke_width=7)
        ticks = VGroup(*[Line([px(i), SY - 0.12, 0], [px(i), SY + 0.12, 0], color=GREY, stroke_width=3)
                         for i in range(15)])
        nums = VGroup(*[M(str(n), 26, GREY).move_to([px(n), SY - 0.45, 0]) for n in (0, 14)])
        phlab = T("pH", 34, YELLOW, weight=BOLD).move_to([px(0) - 0.6, SY, 0])
        strip_g = VGroup(strip, ticks, nums, phlab)

        marker = always_redraw(lambda: VGroup(
            Triangle(color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.2).rotate(PI)
            .move_to([px(pH.get_value()), SY + 0.3, 0]),
            M(f"pH {pH.get_value():.1f}", 34, YELLOW).move_to([px(pH.get_value()), SY + 0.85, 0])))

        XA, XM, XC, YR = -3.7, 0.0, 3.7, -0.35
        container = RoundedRectangle(corner_radius=0.3, width=11.6, height=3.1, stroke_color=GREY, stroke_width=2.5,
                                     fill_color=GREY, fill_opacity=0.05).move_to([0, YR - 0.15, 0])
        ctitle = T("amino acid", 28, GREY).move_to([0, YR + 1.1, 0])

        def row():
            p = pH.get_value()
            amino = box("NH₃⁺", RED, 44, fill=0.25, font=MONO) if p < self.PKA2 else box("NH₂", GREY, 44, font=MONO)
            carb = box("COOH", GREY, 44, font=MONO) if p < self.PKA1 else box("COO⁻", BLUE, 44, fill=0.25, font=MONO)
            amino.move_to([XA, YR, 0]); carb.move_to([XC, YR, 0])
            mid = box("R group", TEAL, 38).move_to([XM, YR, 0])
            la = T("amino group", 28, GREY).move_to([XA, YR - 1.0, 0])
            lc = T("carboxyl group", 28, GREY).move_to([XC, YR - 1.0, 0])
            return VGroup(amino, mid, carb, la, lc)

        chips = always_redraw(row)

        def net():
            p = pH.get_value()
            n = (1 if p < self.PKA2 else 0) + (-1 if p >= self.PKA1 else 0)
            col = {1: RED, 0: GOLD, -1: BLUE}[n]
            txt = {1: "+1", 0: "0", -1: "−1"}[n]
            g = VGroup(T("net charge", 38, TEXT), M(txt, 56, col, weight=BOLD)).arrange(RIGHT, buff=0.4)
            g.move_to([-2.4, -3.1, 0]).set_opacity(show_net.get_value())
            return g

        netg = always_redraw(net)

        def zw():
            p = pH.get_value()
            on = self.PKA1 <= p < self.PKA2
            return T("zwitterion", 44, GOLD, weight=BOLD).move_to([3.7, -3.1, 0]).set_opacity(
                show_zw.get_value() * (1 if on else 0))

        zwtag = always_redraw(zw)

        plus = T("+", 56, RED, weight=BOLD).move_to([XA, YR + 0.92, 0])
        minus = T("−", 56, BLUE, weight=BOLD).move_to([XC, YR + 0.92, 0])

        self.do(0.3, FadeIn(strip_g), FadeIn(marker), run=1.2)
        self.do(2.0, FadeIn(container), FadeIn(ctitle), FadeIn(chips), run=1.2)
        self.add(netg, zwtag)
        self.do(3.86, show_net.animate.set_value(1), run=0.6)
        self.do(5.54, show_zw.animate.set_value(1), run=0.7)
        self.do(7.22, FadeIn(plus, scale=0.5), run=0.5)
        self.do(9.48, FadeIn(minus, scale=0.5), run=0.5)
        self.do(11.0, FadeOut(plus), FadeOut(minus), run=0.5)
        self.do(11.8, pH.animate.set_value(1.0), run=1.6, rate_func=linear)
        self.do(15.4, pH.animate.set_value(11.0), run=2.5, rate_func=linear)
        band = Rectangle(width=px(self.PKA2) - px(self.PKA1), height=0.22, stroke_width=0, fill_color=GOLD,
                         fill_opacity=0.55).move_to([(px(self.PKA1) + px(self.PKA2)) / 2, SY, 0])
        self.do(18.6, pH.animate.set_value(5.97), FadeIn(band), run=2.0, rate_func=smooth)
        pi_tick = VGroup(Line([px(5.97), SY - 0.2, 0], [px(5.97), SY - 0.7, 0], color=GOLD, stroke_width=5),
                         T("pI", 38, GOLD, weight=BOLD).move_to([px(5.97), SY - 1.0, 0]))
        self.do(21.4, Create(pi_tick[0]), run=0.5)
        self.do(22.9, FadeIn(pi_tick[1], scale=0.5), run=0.5)
        self.finish()


# ================================================================== 3 SEESAW
class S03Seesaw(AA):
    PKA = 6.0

    def construct(self):
        pH = ValueTracker(6.0)
        w_ph, w_pka, grp, st = ValueTracker(0), ValueTracker(0), ValueTracker(0), ValueTracker(0)
        off = ValueTracker(0)   # 0 = proton on the group, 1 = proton released
        PV = np.array([0.0, -1.0, 0.0])
        HALF = 3.9

        def ang():
            return float(np.clip(0.15 * (pH.get_value() - self.PKA), -0.42, 0.42))

        def rot(v, a):
            c, s = np.cos(a), np.sin(a)
            return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])

        fulcrum = VGroup(Polygon([-0.65, -1.9, 0], [0.65, -1.9, 0], PV + DOWN * 0.1, color=GREY, fill_opacity=0.5,
                                 stroke_width=3),
                         Line([-1.6, -1.9, 0], [1.6, -1.9, 0], color=GREY, stroke_width=5))

        def seesaw():
            a = ang()
            l, r = PV + rot(np.array([-HALF, 0, 0]), a), PV + rot(np.array([HALF, 0, 0]), a)
            beam = Line(l, r, color=TEXT, stroke_width=10)
            pc = PV + rot(np.array([-2.7, 1.0, 0]), a)
            kc = PV + rot(np.array([2.7, 1.0, 0]), a)
            wph = box(f"pH {pH.get_value():.1f}", YELLOW, 32, fill=0.3, font=MONO, w=2.4).move_to(pc)
            wpk = box(f"pKa {self.PKA:.1f}", GREEN, 32, fill=0.3, font=MONO, w=2.4).move_to(kc)
            dim(wph, w_ph.get_value()); dim(wpk, w_pka.get_value())
            return VGroup(beam, wph, wpk)

        see = always_redraw(seesaw)

        GX, GY = -1.4, 2.7

        def group():
            p = pH.get_value()
            s = off.get_value()
            go = grp.get_value()
            g = box("ionizable group", GREY, 34).move_to([GX, GY, 0])
            hx = GX + g.width / 2 + 0.6 + s * 2.4
            hy = GY + s * 0.2
            proton = VGroup(Circle(radius=0.34, color=TEXT, fill_color=TEXT, fill_opacity=1, stroke_width=0),
                            T("H⁺", 28, BG, weight=BOLD)).move_to([hx, hy, 0])
            dim(g, go); dim(proton, go)
            if p > self.PKA + 0.35:
                msg, col = "deprotonated", BLUE
            elif p < self.PKA - 0.35:
                msg, col = "protonated", RED
            else:
                msg, col = " ", TEXT
            lab = dim(T(msg, 34, col, weight=BOLD).move_to([GX, GY - 0.85, 0]), st.get_value() * go)
            return VGroup(g, proton, lab)

        gg = always_redraw(group)

        rule1 = M("pH > pKa  →  H⁺ off", 32, TEXT, t2c={"pH": YELLOW, "pKa": GREEN}).move_to([-3.4, -3.0, 0])
        rule2 = M("pH < pKa  →  H⁺ on", 32, TEXT, t2c={"pH": YELLOW, "pKa": GREEN}).move_to([3.4, -3.0, 0])

        self.do(0.3, FadeIn(fulcrum), run=1.0)
        self.add(see)
        self.do(4.3, w_ph.animate.set_value(1), run=0.6)
        self.do(5.4, w_pka.animate.set_value(1), run=0.6)
        self.add(gg)
        self.do(6.0, grp.animate.set_value(1), run=0.6)
        self.do(6.72, pH.animate.set_value(8.0), run=1.8, rate_func=smooth)
        self.do(9.4, off.animate.set_value(1), run=0.9, rate_func=smooth)
        self.do(11.0, st.animate.set_value(1), run=0.5)
        self.do(12.3, st.animate.set_value(0), run=0.3)
        self.do(12.68, pH.animate.set_value(4.0), run=1.9, rate_func=smooth)
        self.do(15.1, off.animate.set_value(0), run=0.8, rate_func=smooth)
        self.do(16.3, st.animate.set_value(1), run=0.5)
        self.do(19.0, pH.animate.set_value(8.0), FadeIn(rule1, shift=UP * 0.1), run=1.4, rate_func=smooth)
        self.do(21.2, off.animate.set_value(1), run=0.6, rate_func=smooth)
        self.do(22.3, pH.animate.set_value(4.0), FadeIn(rule2, shift=UP * 0.1), run=1.4, rate_func=smooth)
        self.do(24.3, off.animate.set_value(0), run=0.6, rate_func=smooth)
        self.do(25.6, pH.animate.set_value(8.0), off.animate.set_value(1), run=0.8, rate_func=smooth)
        self.do(26.5, pH.animate.set_value(4.0), off.animate.set_value(0), run=0.8, rate_func=smooth)
        self.do(27.4, pH.animate.set_value(6.0), grp.animate.set_value(0), st.animate.set_value(0), run=0.9,
                rate_func=smooth)
        cons = [box("titration curve", YELLOW, 32), box("buffer", GREEN, 32), box("charged side chain", TEAL, 32)]
        cg = VGroup(*cons).arrange(RIGHT, buff=0.45).move_to([0, 3.0, 0])
        frame = RoundedRectangle(corner_radius=0.25, width=10.6, height=3.9, stroke_color=GOLD, stroke_width=4).move_to(
            [0, -0.45, 0])
        for c in cons:
            c.save_state()
        self.do(28.2, FadeIn(cons[0], shift=DOWN * 0.15), run=0.6)
        self.do(29.4, FadeIn(cons[1], shift=DOWN * 0.15), run=0.6)
        self.do(30.8, FadeIn(cons[2], shift=DOWN * 0.15), run=0.6)
        arrs = [Arrow(c.get_bottom() + DOWN * 0.05, [c.get_center()[0], frame.get_top()[1] + 0.02, 0], buff=0,
                      color=GOLD, stroke_width=5, max_tip_length_to_length_ratio=0.35) for c in cons]
        self.do(34.1, LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), Create(frame), run=1.0)
        self.finish()


# ================================================================== 4 TITRATION
class S04Titration(AA):
    PKA1, PKA2, C = 2.34, 9.60, 0.1

    def e_of(self, h):
        d1 = 1 / (1 + 10 ** (self.PKA1 - h)); d2 = 1 / (1 + 10 ** (self.PKA2 - h))
        return d1 + d2 + (10 ** (h - 14) - 10 ** (-h)) / self.C

    def ph_of(self, e):
        lo, hi = 0.5, 13.5
        for _ in range(50):
            mid = (lo + hi) / 2
            if self.e_of(mid) < e:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    def construct(self):
        e = ValueTracker(0.0)
        drip = ValueTracker(0.0)
        clock = ValueTracker(0.0)
        a1, a2, a3 = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        EMAX = 2.1
        ax = Axes(x_range=[0, 2.4, 0.5], y_range=[0, 13, 2], x_length=7.6, y_length=4.8,
                  axis_config={"include_numbers": False, "color": GREY, "stroke_width": 3, "include_tip": False,
                               "include_ticks": False}).move_to([2.35, -0.5, 0])
        ytl = VGroup(*[M(str(v), 26, GREY).next_to(ax.c2p(0, v), LEFT, 0.15) for v in (0, 4, 8, 12)])
        xtl = VGroup(*[M(str(v), 26, GREY).next_to(ax.c2p(v, 0), DOWN, 0.15) for v in (0, 1, 2)])
        ylab = T("pH", 34, YELLOW, weight=BOLD).next_to(ax.c2p(0, 13), UP, 0.1)
        xlab = T("base added (equivalents)", 28, BLUE).next_to(ax, DOWN, 0.55)
        axg = VGroup(ax, ytl, xtl, ylab, xlab)

        labels = [("1  add base", BLUE), ("2  monitor pH", YELLOW), ("3  plot the curve", YELLOW)]
        sizes = [box(t, c, 32) for t, c in labels]
        total = sum(b.width for b in sizes) + 0.5 * 2
        xs, x = [], -total / 2
        for b in sizes:
            xs.append(x + b.width / 2); x += b.width + 0.5

        def mkstep(i, tr):
            def f():
                b = box(labels[i][0], labels[i][1], 32).move_to([xs[i], 3.15, 0])
                return dim(b, tr.get_value())
            return always_redraw(f)

        steps = [mkstep(0, a1), mkstep(1, a2), mkstep(2, a3)]

        BX = -4.55
        burette = RoundedRectangle(corner_radius=0.08, width=0.7, height=2.3, stroke_color=GREY, stroke_width=3,
                                   fill_color=BLUE, fill_opacity=0.35).move_to([BX, 1.4, 0])
        tip = Polygon([BX - 0.15, 0.25, 0], [BX + 0.15, 0.25, 0], [BX, -0.1, 0], color=GREY, stroke_width=3)
        blabel = T("base", 30, BLUE).next_to(burette, RIGHT, 0.2)
        beaker_pts = [[BX - 1.4, -0.95, 0], [BX - 1.4, -3.0, 0], [BX + 1.4, -3.0, 0], [BX + 1.4, -0.95, 0]]
        beaker = VMobject(color=GREY, stroke_width=4).set_points_as_corners(beaker_pts)
        liquid = Rectangle(width=2.78, height=1.3, stroke_width=0, fill_color=TEXT, fill_opacity=0.12)
        liquid.move_to([BX, -2.35, 0])
        sample = T("amino acid", 28, GREY).move_to([BX, -3.4, 0])
        readout = always_redraw(lambda: M(f"pH {self.ph_of(e.get_value()):.1f}", 36, YELLOW).move_to([BX, -2.35, 0]))
        drop = always_redraw(lambda: Dot([BX, 0.1 - 1.1 * ((clock.get_value() * 1.6) % 1) ** 2, 0], radius=0.1,
                                          color=BLUE).set_opacity(drip.get_value()))
        appar = VGroup(burette, tip, blabel, beaker, liquid, sample)

        def curve():
            ec = max(e.get_value(), 0.01)
            c = ax.plot(lambda x: self.ph_of(x), x_range=[0.0, ec, 0.02], color=YELLOW, stroke_width=7)
            head = Dot(ax.c2p(ec, self.ph_of(ec)), radius=0.13, color=YELLOW)
            return VGroup(c, head)

        live = always_redraw(curve)
        clock.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))
        self.add(clock)

        self.do(0.3, FadeIn(appar), FadeIn(readout), run=1.2)
        self.add(*steps)
        self.do(1.44, LaggedStart(a1.animate.set_value(0.4), a2.animate.set_value(0.4), a3.animate.set_value(0.4),
                                  lag_ratio=0.3), run=1.2)
        self.add(drop)
        self.do(2.62, a1.animate.set_value(1), drip.animate.set_value(1), run=0.4)
        self.do(2.9, e.animate.set_value(0.18), run=2.0, rate_func=linear)
        self.do(5.0, a2.animate.set_value(1), e.animate.set_value(0.3), run=1.2, rate_func=linear)
        self.play(Indicate(readout, color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.do(7.04, a3.animate.set_value(1), FadeIn(axg), run=0.6)
        self.add(live)
        self.play(e.animate.set_value(EMAX), run_time=4.4, rate_func=linear)
        self.do(11.5, drip.animate.set_value(0), run=0.2)

        def band(e0, e1, pad=0.5):
            y0, y1 = self.ph_of(e0) - pad, self.ph_of(e1) + pad
            r = Rectangle(width=ax.c2p(e1, 0)[0] - ax.c2p(e0, 0)[0], height=ax.c2p(0, y1)[1] - ax.c2p(0, y0)[1],
                          stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.18)
            return r.move_to([(ax.c2p(e0, 0)[0] + ax.c2p(e1, 0)[0]) / 2, (ax.c2p(0, y0)[1] + ax.c2p(0, y1)[1]) / 2, 0])

        p1, p2 = band(0.2, 0.7), band(1.3, 1.7)
        buf1 = T("buffering", 26, GREEN).next_to(p1, UP, 0.12)
        buf2 = T("buffering", 26, GREEN).next_to(p2, DOWN, 0.12)
        self.do(12.74, FadeIn(p1), FadeIn(p2), FadeIn(buf1), FadeIn(buf2), run=0.8)

        def hline(y, col):
            return DashedLine(ax.c2p(0, y), ax.c2p(2.4, y), color=col, dash_length=0.12, stroke_width=3.5)

        l1, l2 = hline(self.PKA1, GREEN), hline(self.PKA2, GREEN)
        d1 = Dot(ax.c2p(self.e_of(self.PKA1), self.PKA1), radius=0.12, color=GREEN)
        d2 = Dot(ax.c2p(self.e_of(self.PKA2), self.PKA2), radius=0.12, color=GREEN)
        rx = ax.c2p(2.4, 0)[0] + 0.1
        t1 = M("pKa₁ = 2.3", 26, GREEN); t1.next_to(ax.c2p(2.4, self.PKA1), UP, 0.1).align_to([rx, 0, 0], RIGHT)
        t2 = M("pKa₂ = 9.6", 26, GREEN); t2.next_to(ax.c2p(2.4, self.PKA2), DOWN, 0.1).align_to([rx, 0, 0], RIGHT)
        self.do(14.4, Create(l1), Create(l2), FadeIn(d1), FadeIn(d2), run=1.0)
        self.do(15.4, FadeIn(t1), FadeIn(t2), FadeOut(buf1), FadeOut(buf2), run=0.6)

        ypi = self.ph_of(1.0)
        mid_dot = Dot(ax.c2p(1.0, ypi), radius=0.15, color=GOLD)
        l3 = DashedLine(ax.c2p(0, ypi), ax.c2p(2.4, ypi), color=GOLD, dash_length=0.12, stroke_width=4)
        t3 = M("pI ≈ 6.0", 32, GOLD); t3.next_to(ax.c2p(2.4, ypi), UP, 0.1).align_to([rx, 0, 0], RIGHT)
        t4 = T("net charge = 0", 30, GOLD); t4.next_to(ax.c2p(2.4, ypi), DOWN, 0.1).align_to([rx, 0, 0], RIGHT)
        self.do(18.4, FadeIn(mid_dot, scale=2.0), run=0.6)
        self.do(19.6, Create(l3), run=0.8)
        self.do(20.1, FadeIn(t3, shift=UP * 0.1), run=0.6)
        self.do(21.7, FadeIn(t4, shift=UP * 0.1), run=0.6)
        self.finish()


# ================================================================== 5 pI LADDER
class S05PiLadder(AA):
    def construct(self):
        CX = -2.6
        ys = [2.1, 0.4, -1.3, -3.0]
        data = [("+2", "H₃A²⁺", RED), ("+1", "H₂A⁺", RED), ("0", "HA", GOLD), ("−1", "A⁻", BLUE)]

        def rung(i):
            q, name, col = data[i]
            a = M(q, 42, col, weight=BOLD)
            b = M(name, 30, GREY)
            inner = VGroup(a, b).arrange(RIGHT, buff=0.5)
            r = RoundedRectangle(corner_radius=0.16, width=3.5, height=0.9, stroke_color=col, stroke_width=3,
                                 fill_color=col, fill_opacity=0.14)
            inner.move_to(r)
            return VGroup(r, inner).move_to([CX, ys[i], 0])

        rungs = [rung(i) for i in range(4)]
        pkas = [1.8, 6.0, 9.2]
        steps, pk_labels = [], []
        for k in range(3):
            y0, y1 = ys[k] - 0.45, ys[k + 1] + 0.45
            steps.append(Arrow([CX - 1.2, y0, 0], [CX - 1.2, y1, 0], buff=0.02, color=GREY, stroke_width=5,
                               max_tip_length_to_length_ratio=0.5))
            pk_labels.append(M(f"pKa{'₁₂₃'[k]} = {pkas[k]:.1f}", 28, GREEN).move_to([CX + 0.5, (y0 + y1) / 2, 0]))

        c_amino = box("amino acid", GREY, 34)
        c_side = box("ionizable side chain", TEAL, 34, fill=0.22)
        intro = VGroup(c_amino, c_side).arrange(RIGHT, buff=0.4).move_to([-2.65, 0.9, 0])
        piq = M("pI = ?", 60, GOLD, weight=BOLD).move_to([4.35, 1.4, 0])

        title = T("charge ladder: histidine", 36, TEXT).move_to([CX, 3.35, 0])
        tag_top = T("most\npositive", 26, GREY, line_spacing=0.8).move_to([-5.55, ys[0], 0])
        tag_bot = T("most\nnegative", 26, GREY, line_spacing=0.8).move_to([-5.55, ys[3], 0])
        zw_tag = T("net zero\nzwitterion", 32, GOLD, line_spacing=0.8).move_to([0.7, ys[2], 0])
        glow = SurroundingRectangle(rungs[2], color=GOLD, buff=0.1, stroke_width=5, corner_radius=0.2)

        eq1 = VGroup(M("pI = average of", 30, GOLD), M("pKa₂ and pKa₃", 30, GREEN)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        eq1.move_to([4.35, 1.4, 0])
        eq2 = M("= (6.0 + 9.2) / 2", 28, TEXT).move_to([4.35, -0.15, 0])
        eq3 = M("= 7.6", 60, GOLD, weight=BOLD).move_to([4.35, -1.5, 0])

        self.do(0.3, FadeIn(intro, shift=DOWN * 0.1), run=1.3)
        self.do(3.24, Write(piq), run=0.9)
        self.do(6.7, FadeOut(intro), run=0.4)
        self.do(7.5, FadeIn(title, shift=DOWN * 0.1), run=0.6)
        self.do(9.4, FadeIn(rungs[0], shift=RIGHT * 0.2), run=0.5)
        self.do(10.4, FadeIn(rungs[1], shift=RIGHT * 0.2), FadeIn(steps[0]), run=0.5)
        self.do(11.2, FadeIn(rungs[2], shift=RIGHT * 0.2), FadeIn(steps[1]), FadeIn(tag_top), run=0.5)
        self.do(12.9, FadeIn(rungs[3], shift=RIGHT * 0.2), FadeIn(steps[2]), FadeIn(tag_bot), run=0.5)
        self.do(14.7, Create(glow), run=0.6)
        self.do(15.9, FadeIn(zw_tag, shift=LEFT * 0.1), run=0.6)
        self.do(17.9, LaggedStart(*[FadeIn(p, shift=LEFT * 0.1) for p in pk_labels], lag_ratio=0.3), run=1.2)
        self.do(19.5, Transform(piq, eq1), run=0.8)
        self.do(21.1, pk_labels[0].animate.set_opacity(0.25), steps[0].animate.set_opacity(0.25),
                steps[1].animate.set_color(GREEN).set_stroke(width=8),
                steps[2].animate.set_color(GREEN).set_stroke(width=8), run=0.8)
        self.do(22.9, Indicate(rungs[2], color=GOLD, scale_factor=1.1), run=0.9)
        self.do(25.4, FadeIn(eq2, shift=UP * 0.1), run=0.6)
        self.do(26.7, FadeIn(eq3, scale=0.7), run=0.6)
        self.finish()


# ================================================================== 6 HISTIDINE
class S06Histidine(AA):
    PKA = 6.0

    def f(self, ph):
        return 1 / (1 + 10 ** (ph - self.PKA))

    def construct(self):
        s = ValueTracker(0.0)        # 0 = neutral, 1 = protonated
        ax = Axes(x_range=[2, 12, 2], y_range=[0, 1, 0.5], x_length=7.4, y_length=4.5,
                  axis_config={"include_numbers": False, "color": GREY, "stroke_width": 3, "include_tip": False,
                               "include_ticks": False}).move_to([-2.4, -0.5, 0])
        xtl = VGroup(*[M(str(v), 26, GREY).next_to(ax.c2p(v, 0), DOWN, 0.15) for v in (2, 4, 6, 8, 10, 12)])
        ytl = VGroup(M("0", 26, GREY).next_to(ax.c2p(2, 0), LEFT, 0.15), M("1", 26, GREY).next_to(ax.c2p(2, 1), LEFT, 0.15))
        xlab = T("pH", 34, YELLOW, weight=BOLD).next_to(ax.c2p(12, 0), DOWN, 0.6)
        ylab = T("fraction protonated (+)", 30, RED).next_to(ax.c2p(2, 1), UP, 0.25).align_to(ax.c2p(2, 1), LEFT)
        axg = VGroup(ax, xtl, ytl, xlab, ylab)
        curve = ax.plot(lambda x: self.f(x), x_range=[2, 12, 0.05], color=TEAL, stroke_width=7)

        p74 = ax.c2p(7.4, self.f(7.4))
        yl = DashedLine(ax.c2p(7.4, 0), ax.c2p(7.4, 0.85), color=YELLOW, dash_length=0.1, stroke_width=4)
        yd = Dot(p74, radius=0.11, color=YELLOW)
        yt = M("pH 7.4", 30, YELLOW).next_to(ax.c2p(7.4, 0.85), RIGHT, 0.12)
        gl = DashedLine(ax.c2p(6.0, 0), ax.c2p(6.0, 0.85), color=GREEN, dash_length=0.1, stroke_width=4)
        gd = Dot(ax.c2p(6.0, 0.5), radius=0.13, color=GREEN)
        gt = M("pKa ≈ 6.0", 30, GREEN).next_to(ax.c2p(6.0, 0.22), LEFT, 0.15)
        gap = DoubleArrow(ax.c2p(6.0, 0.68), ax.c2p(7.4, 0.68), buff=0, color=TEXT, stroke_width=4,
                          max_tip_length_to_length_ratio=0.2, tip_length=0.15)
        gaplab = M("+1.4", 26, TEXT).next_to(gap, UP, 0.08)

        RX = 4.15
        hischip = box("His side chain", TEAL, 34, fill=0.22).move_to([RX, 3.0, 0])
        pill = RoundedRectangle(corner_radius=0.5, width=2.8, height=1.0, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.12).move_to([RX, 1.05, 0])
        KL, KR = RX - 0.9, RX + 0.9

        def knob():
            v = s.get_value()
            col = interpolate_color(ManimColor(GREY), ManimColor(RED), v)
            return Circle(radius=0.38, color=col, fill_color=col, fill_opacity=1, stroke_width=0).move_to(
                [KL + (KR - KL) * v, 1.05, 0])

        knobm = always_redraw(knob)
        l_neu = T("neutral", 26, GREY).move_to([RX - 1.0, 0.2, 0])
        l_pos = T("protonated", 26, RED).move_to([RX + 1.1, 0.2, 0])
        roles = [box("enzyme active sites", TEAL, 26), box("metal coordination", TEAL, 26), box("pH sensing", TEAL, 26)]
        rg = VGroup(*roles).arrange(DOWN, buff=0.3).move_to([RX, -1.7, 0])
        switchlab = T("molecular switch", 34, GOLD, weight=BOLD).move_to([RX, 2.05, 0])
        proton = VGroup(Circle(radius=0.3, color=TEXT, fill_color=TEXT, fill_opacity=1, stroke_width=0),
                        T("H⁺", 24, BG, weight=BOLD)).move_to([RX + 1.0, 1.05, 0]).set_opacity(0)

        self.do(0.2, FadeIn(axg), FadeIn(hischip), run=0.9)
        self.do(1.2, Create(curve), run=1.8, rate_func=smooth)
        self.do(3.1, Create(yl), FadeIn(yd), FadeIn(yt), run=0.9)
        self.do(5.76, Create(gl), FadeIn(gd, scale=2), FadeIn(gt), run=0.9)
        self.do(7.7, FadeIn(pill), FadeIn(knobm), FadeIn(l_neu), FadeIn(l_pos), run=0.8)
        self.do(9.3, GrowFromCenter(gap), FadeIn(gaplab), run=0.8)
        for t0, v in [(11.3, 1), (11.9, 0), (12.5, 1), (13.0, 0), (13.5, 1), (14.0, 0)]:
            self.do(t0, s.animate.set_value(v), run=0.3)
        self.do(15.1, s.animate.set_value(1), run=0.3)
        self.do(15.7, s.animate.set_value(0), run=0.3)
        self.do(17.9, FadeIn(roles[0], shift=LEFT * 0.15), run=0.5)
        self.do(19.8, FadeIn(roles[1], shift=LEFT * 0.15), run=0.5)
        self.do(21.1, FadeIn(roles[2], shift=LEFT * 0.15), run=0.5)
        self.do(22.5, FadeIn(switchlab, shift=DOWN * 0.1), run=0.6)
        self.play(Indicate(pill, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.do(24.8, s.animate.set_value(0.5), run=0.8)
        self.do(26.9, proton.animate.set_opacity(1), run=0.3)
        self.play(proton.animate.move_to([RX + 2.0, 1.75, 0]), run_time=0.8)
        self.do(28.2, proton.animate.move_to([RX + 1.0, 1.05, 0]), run=0.8)
        self.finish()


# ================================================================== END
class S07End(EndCard):
    LINE = "Now try the titrator and watch charge follow pH."
