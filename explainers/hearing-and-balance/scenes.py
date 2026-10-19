"""Hearing and balance: pitch becomes a place along the cochlea  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
The cochlea is drawn only as an uncoiled schematic strip (base left, apex right); waves and
peaks are sketches ("in this sketch"); every number is the lesson's own.

COLOR MAP (one color per concept, whole video)
  YELLOW = sound / a tone in general (the violin A, sound entering, the untuned wave)
  BLUE   = the cochlea strip, the basilar membrane, the relay boxes
  ORANGE = high frequency (4,000 Hz; the base end of the map)
  PURPLE = low frequency (1,000 Hz; the apex end of the map)
  TEAL   = hair cells (outer hair cells in scene 5), the word tonotopy
  GREEN  = the amplifier: outer hair cells pushing, the sharpened living-ear peak
  GOLD   = stiffness
  GREY   = outlines, units, labels, the broad passive peak
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

# the uncoiled strip: base at the left, apex at the right, 35 mm of cochlea on LEN screen units
X0, X1 = -5.0, 6.0
LEN = X1 - X0
W_BASE, W_APEX = 0.7, 2.2        # schematic width of the membrane: narrow at the base, wide at the apex


def mm2x(mm):
    return X0 + mm * LEN / 35.0


def width_at(f):
    return W_BASE + (W_APEX - W_BASE) * f


def strip(cy, color=BLUE, op=0.3, n=48):
    top = [[X0 + LEN * i / n, cy + width_at(i / n) / 2, 0] for i in range(n + 1)]
    bot = [[X0 + LEN * i / n, cy - width_at(i / n) / 2, 0] for i in range(n, -1, -1)]
    return Polygon(*top, *bot, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op)


def strip_map(cy, n=40, op=0.6):
    """the strip coloured high (orange, base) to low (purple, apex)."""
    g = VGroup()
    for i in range(n):
        f0, f1 = i / n, (i + 1) / n
        pts = [[X0 + LEN * f0, cy + width_at(f0) / 2, 0], [X0 + LEN * f1, cy + width_at(f1) / 2, 0],
               [X0 + LEN * f1, cy - width_at(f1) / 2, 0], [X0 + LEN * f0, cy - width_at(f0) / 2, 0]]
        g.add(Polygon(*pts, stroke_width=0, fill_color=interpolate_color(ManimColor(ORANGE), ManimColor(PURPLE), (i + .5) / n),
                      fill_opacity=op))
    return g


def haircell(h=0.5, w=0.26, color=TEAL, sw=3):
    """a hair cell as a simple cell: a rounded body with a staircase bundle on top. Bottom of the body at the origin."""
    body = RoundedRectangle(corner_radius=w * 0.42, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=0.3).move_to([0, h / 2, 0])
    k = max(0.34, h * 0.7)
    bundle = VGroup(*[Line([dx * w, h, 0], [dx * w, h + k * f, 0], color=color, stroke_width=sw)
                      for dx, f in ((-0.30, 0.45), (0.0, 0.72), (0.30, 1.0))])
    g = VGroup(body, bundle)
    g.body, g.bundle = body, bundle
    return g


def sound_arrow(a, b, color=YELLOW):
    a, b = list(a)[:2] + [0], list(b)[:2] + [0]
    return Arrow(a, b, buff=0, color=color, stroke_width=6, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.5)


def end_labels(cy, sub_base=None, sub_apex=None):
    """'base' and 'apex' under the two ends of the strip."""
    base = VGroup(T("base", 30, TEXT, weight=BOLD))
    apex = VGroup(T("apex", 30, TEXT, weight=BOLD))
    base.move_to([X0 + 0.4, cy - 0.95, 0])
    apex.move_to([X1 - 0.5, cy - 1.4, 0])
    return base, apex


class S00Title(TitleCard):
    LESSON = "Hearing and balance"
    TITLE = "Pitch becomes a place along the cochlea"


# ---------------------------------------------------------------------------------------------
class S01Pitch(SpokenScene):
    """hair cell + a violin A -> a question on a coiled tube -> the tube uncoils into a strip: frequency becomes position."""

    def construct(self):
        # left: the hair cell and the violin's A
        hc = haircell(h=2.0, w=1.1, sw=6)
        hc.move_to([-4.2, -1.55, 0], aligned_edge=DOWN)
        hc_lbl = T("hair cell", 32, TEAL).move_to([-4.2, -2.15, 0])
        violin = chip("a violin plays an A", YELLOW, size=30).move_to([-4.2, 3.0, 0])
        down = sound_arrow([-4.2, 2.5, 0], [-4.2, 2.0, 0])
        self.at("One kind of cell")
        self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(hc_lbl), run_time=0.7)
        self.at("a violin")
        self.play(FadeIn(violin, shift=DOWN * 0.15), GrowArrow(down), run_time=0.7)

        # the hair cell turns a tiny movement into a graded voltage
        self.at("turns a tiny movement")
        pivot = hc.body.get_top()
        self.play(Rotate(hc.bundle, angle=-0.35, about_point=pivot), run_time=0.45)
        self.play(Rotate(hc.bundle, angle=0.7, about_point=pivot), run_time=0.6)
        self.play(Rotate(hc.bundle, angle=-0.35, about_point=pivot), run_time=0.45)
        out = T("graded voltage", 28, TEAL)
        out.move_to([-1.6, -0.5, 0])
        a2 = Arrow([-3.55, -0.5, 0], out.get_left() + LEFT * 0.08, buff=0.05, color=TEAL, stroke_width=4, tip_length=0.2)
        self.at("graded voltage")
        self.play(GrowArrow(a2), FadeIn(out, shift=RIGHT * 0.15), run_time=0.7)

        # the coiled tube and a question
        CX, CY = 3.3, 0.0
        tmax = 4.2 * np.pi

        def spiral_pt(t):
            r = 2.9 - 2.1 * t / tmax
            return np.array([CX - r * np.cos(t), CY + r * np.sin(t), 0])

        def line_pt(t):
            return np.array([X0 + LEN * t / tmax, -0.6, 0])

        k = ValueTracker(0.0)

        def coil():
            ts = np.linspace(0, tmax, 160)
            kk = k.get_value()
            pts = [(1 - kk) * spiral_pt(t) + kk * line_pt(t) for t in ts]
            m = VMobject().set_points_smoothly(pts)
            return m.set_stroke(BLUE, 16, opacity=1).set_fill(opacity=0)

        c = always_redraw(coil)
        q = T("?", 120, YELLOW, weight=BOLD).move_to([CX, CY, 0])
        self.at("But how does a coiled tube")
        self.play(FadeIn(c), run_time=0.8)
        self.play(FadeIn(q, scale=0.8), run_time=0.5)

        # uncoil
        self.at("Uncoil")
        self.play(FadeOut(VGroup(hc, hc_lbl, violin, down, out, a2)), FadeOut(q), run_time=0.7)
        self.play(k.animate.set_value(1.0), run_time=1.8, rate_func=smooth)
        st = strip(-0.6)
        base, apex = end_labels(-0.6)
        cap = T("cochlea, uncoiled (schematic)", 24, GREY).move_to([0.5, -2.75, 0])
        self.play(FadeIn(st), FadeOut(c), FadeIn(base), FadeIn(apex), FadeIn(cap), run_time=0.8)
        self.remove(c)

        # frequency becomes position
        f_chip = chip("frequency", YELLOW, size=32).move_to([-2.4, 1.9, 0])
        p_chip = chip("position", BLUE, size=32).move_to([2.6, 1.9, 0])
        arrow = arr_h(f_chip, p_chip)
        self.at("Frequency is turned")
        self.play(FadeIn(f_chip, shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(arrow), FadeIn(p_chip), run_time=0.6)
        self.finish()


def arr_h(a, b, color=GREY):
    return Arrow(a.get_right() + RIGHT * 0.1, b.get_left() + LEFT * 0.1, buff=0, color=color, stroke_width=5,
                 tip_length=0.22, max_tip_length_to_length_ratio=0.45)


# ---------------------------------------------------------------------------------------------
class S02Membrane(SpokenScene):
    """hair cells on the membrane; sound enters at the base; narrow+stiff to wide+compliant."""

    def construct(self):
        cy = 0.5
        st = strip(cy)
        base, apex = end_labels(cy)
        self.add(st, base, apex)

        # hair cells standing on the membrane
        cells = VGroup()
        n = 9
        for i in range(n):
            f = (i + 0.5) / n
            h = haircell(h=0.5, w=0.32)
            h.move_to([X0 + LEN * f, cy + width_at(f) / 2, 0], aligned_edge=DOWN)
            cells.add(h)
        mem_lbl = T("basilar membrane", 28, BLUE).move_to([0.2, cy - 1.25, 0])
        hc_lbl = T("hair cells", 28, TEAL).move_to([-0.5, cy + 1.75, 0])
        self.at("Cochlear hair cells sit")
        self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.1) for h in cells], lag_ratio=0.1), FadeIn(hc_lbl), run_time=1.4)
        self.at("basilar membrane")
        self.play(FadeIn(mem_lbl), Indicate(st, color=BLUE, scale_factor=1.0), run_time=0.8)

        # sound enters at the base
        snd = sound_arrow([X0 - 1.15, cy, 0], [X0 - 0.15, cy])
        snd_lbl = T("sound", 26, YELLOW).next_to(snd, UP, buff=0.12)
        self.at("where sound enters")
        self.play(GrowArrow(snd), FadeIn(snd_lbl), run_time=0.6)

        # narrow and stiff at the base
        wb = DoubleArrow([X0 + 0.45, cy - W_BASE / 2 + 0.03, 0], [X0 + 0.45, cy + W_BASE / 2 - 0.03, 0], buff=0, color=YELLOW,
                         stroke_width=4, tip_length=0.13)
        nb = T("narrow, stiff", 26, GOLD).next_to(base, DOWN, buff=0.12)
        self.at("narrow and stiff")
        self.play(GrowFromCenter(wb), FadeIn(nb), run_time=0.7)

        # wide and compliant at the apex
        wa = DoubleArrow([X1 - 0.45, cy - W_APEX / 2 + 0.03, 0], [X1 - 0.45, cy + W_APEX / 2 - 0.03, 0], buff=0, color=YELLOW,
                         stroke_width=4, tip_length=0.13)
        na = T("wide, compliant", 26, GOLD).next_to(apex, DOWN, buff=0.12).align_to([6.2, 0, 0], RIGHT)
        self.at("wider and more compliant")
        self.play(GrowFromCenter(wa), FadeIn(na), run_time=0.7)

        # the stiffness gradient
        m = 24
        bar = VGroup(*[Rectangle(width=LEN / m, height=0.34, stroke_width=0, fill_color=GOLD,
                                 fill_opacity=1.0 - 0.78 * i / (m - 1)) for i in range(m)]).arrange(RIGHT, buff=0)
        bar.move_to([(X0 + X1) / 2, cy - 2.75, 0])
        s_lbl = T("stiffness", 26, GOLD).next_to(bar, UP, buff=0.12).align_to(bar, LEFT)
        e1 = T("stiff", 24, GREY).next_to(bar, DOWN, buff=0.1).align_to(bar, LEFT)
        e2 = T("compliant", 24, GREY).next_to(bar, DOWN, buff=0.1).align_to(bar, RIGHT)
        self.at("stiffness gradient")
        self.play(LaggedStart(*[FadeIn(r) for r in bar], lag_ratio=0.03), FadeIn(s_lbl), FadeIn(e1), FadeIn(e2), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
def wave_pts(xp, n_cyc, t, amp, y0):
    """a sketched travelling wave on a baseline at y0, peaking at screen x = xp (units from X0)."""
    xs = np.linspace(0, LEN, 420)
    s = xs / xp
    env = np.exp(-(((s - 1) / np.where(s < 1, 0.62, 0.3)) ** 2))
    phi = 2 * np.pi * n_cyc * (1 - np.exp(-1.2 * s)) / (1 - np.exp(-1.2))
    ys = y0 + amp * env * np.sin(phi - 2 * np.pi * 0.7 * t)
    return [[X0 + x, y, 0] for x, y in zip(xs, ys)], env


class S03Wave(SpokenScene):
    """a sketched travelling wave runs base to apex, grows, peaks and dies; high tones peak near the base, low near the apex."""

    def construct(self):
        cy = -1.75
        y0 = 1.1
        st = strip(cy)
        base, apex = end_labels(cy)
        note = T("wave drawn in this sketch", 24, GREY).move_to([0.5, -3.3, 0])
        self.add(st, base, apex, note)

        t = ValueTracker(0.0)
        t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t)
        xp = ValueTracker(mm2x(16.0) - X0)     # where the wave peaks, units from X0
        ncy = ValueTracker(4.0)
        amp = ValueTracker(0.0)
        col = ValueTracker(0.0)                # 0 yellow, 1 orange, 2 purple

        def colour():
            c = col.get_value()
            a, b = (YELLOW, ORANGE) if c <= 1 else (ORANGE, PURPLE)
            return interpolate_color(ManimColor(a), ManimColor(b), min(c, 2 - c) if False else (c if c <= 1 else c - 1))

        def wave():
            pts, _ = wave_pts(xp.get_value(), ncy.get_value(), t.get_value(), amp.get_value(), y0)
            return VMobject().set_points_as_corners(pts).set_stroke(colour(), 6).set_fill(opacity=0)

        def envelope(sign):
            pts, env = wave_pts(xp.get_value(), ncy.get_value(), 0, 1, y0)
            e = [[p[0], y0 + sign * amp.get_value() * ev, 0] for p, ev in zip(pts, env)]
            return DashedVMobject(VMobject().set_points_as_corners(e).set_stroke(GREY, 3).set_fill(opacity=0), num_dashes=70)

        base_line = Line([X0, y0, 0], [X1, y0, 0], color=GREY, stroke_width=2)

        # sound enters at the base
        snd = sound_arrow([X0 - 1.15, y0, 0], [X0 - 0.15, y0])
        self.at("Sound entering")
        self.play(GrowArrow(snd), FadeIn(base_line), run_time=0.6)

        w = always_redraw(wave)
        self.at("traveling wave")
        self.add(w)
        self.play(amp.animate.set_value(1.15), run_time=1.2, rate_func=smooth)

        # base to apex
        dir_arrow = Arrow([X0 + 0.2, y0 - 1.25, 0], [X0 + 3.4, y0 - 1.25, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.2)
        self.at("moves from base")
        self.play(GrowArrow(dir_arrow), run_time=0.6)

        # grows ... peaks ... dies away
        env_top = always_redraw(lambda: envelope(1))
        env_bot = always_redraw(lambda: envelope(-1))
        grows = T("grows", 26, YELLOW).move_to([X0 + 2.4, y0 + 1.1, 0])
        self.at("and grows")
        self.play(FadeOut(dir_arrow), FadeIn(env_top), FadeIn(env_bot), FadeIn(grows), run_time=0.6)
        pk_line = always_redraw(lambda: DashedLine([X0 + xp.get_value(), y0 + 1.15 + 0.1, 0], [X0 + xp.get_value(), cy + width_at(xp.get_value() / LEN) / 2, 0],
                                                    color=TEXT, stroke_width=3, dash_length=0.12))
        pk_dot = always_redraw(lambda: Dot([X0 + xp.get_value(), cy + width_at(xp.get_value() / LEN) / 2, 0], radius=0.11, color=TEXT))
        pk_lbl = always_redraw(lambda: T("peak", 28, TEXT, weight=BOLD).move_to([X0 + xp.get_value(), y0 + 1.6, 0]))
        self.at("There it peaks")
        self.play(FadeOut(grows), Create(pk_line), FadeIn(pk_dot), FadeIn(pk_lbl), run_time=0.7)
        dies = T("dies away", 26, YELLOW).move_to([X0 + xp.get_value() + 1.6, y0 + 0.95, 0])
        self.at("dies away")
        self.play(FadeIn(dies, shift=RIGHT * 0.1), run_time=0.5)

        # high frequencies peak near the base, low near the apex
        g = strip_map(cy)
        hi = T("high frequency", 30, ORANGE, weight=BOLD).move_to([-4.2, 3.25, 0])
        lo = T("low frequency", 30, PURPLE, weight=BOLD).move_to([4.2, 3.25, 0])
        self.at("High frequencies")
        self.play(FadeOut(dies), FadeIn(g), st.animate.set_fill(opacity=0.0),
                  xp.animate.set_value(mm2x(11.7) - X0), col.animate.set_value(1.0), ncy.animate.set_value(6.5),
                  FadeIn(hi), run_time=1.5, rate_func=smooth)
        self.at("near the base")
        self.play(Indicate(pk_dot, color=ORANGE, scale_factor=1.8), run_time=0.7)
        self.at("Low frequencies")
        self.play(FadeOut(hi), xp.animate.set_value(mm2x(21.0) - X0), col.animate.set_value(2.0), ncy.animate.set_value(3.5),
                  FadeIn(lo), run_time=1.5, rate_func=smooth)
        self.at("near the apex")
        self.play(Indicate(pk_dot, color=PURPLE, scale_factor=1.8), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Place(SpokenScene):
    """Greenwood's map on a 35 mm strip: the lesson's worked arithmetic places 1,000 Hz and 4,000 Hz."""

    def construct(self):
        cy = 0.3
        g = strip_map(cy)
        st = strip(cy, color=GREY, op=0.0)
        base, apex = end_labels(cy)
        self.add(g, st, base, apex)

        eq = M("f = 165.4 × (10^(2.1x) − 0.88)", 28, TEXT).move_to([0, 3.15, 0])
        eqn = T("f in Hz; x is the fraction of length from the apex", 22, GREY).next_to(eq, DOWN, buff=0.15)
        self.at("Greenwood's function")
        self.play(FadeIn(eq, shift=DOWN * 0.1), FadeIn(eqn), run_time=0.8)

        # the 35 mm ruler
        ry = cy - 1.85
        ruler = Line([X0, ry, 0], [X1, ry, 0], color=GREY, stroke_width=3)
        t0 = Line([X0, ry - 0.12, 0], [X0, ry + 0.12, 0], color=GREY, stroke_width=3)
        t35 = Line([X1, ry - 0.12, 0], [X1, ry + 0.12, 0], color=GREY, stroke_width=3)
        l0 = M("0 mm", 22, GREY).next_to(t0, DOWN, buff=0.1)
        l35 = M("35 mm", 22, TEXT).next_to(t35, DOWN, buff=0.1)
        rul = T("ruler: mm from the base", 24, GREY).move_to([-2.9, ry + 0.3, 0])
        self.at("Assume a cochlea")
        self.play(Create(ruler), FadeIn(rul), FadeIn(t0), FadeIn(t35), FadeIn(l0), FadeIn(l35), run_time=1.0)

        card_y = -3.0

        def card(l1, l2, color):
            return VGroup(M(l1, 24, color), M(l2, 24, color)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([0, card_y, 0])

        def marker(mm, color, label, dy):
            x = mm2x(mm)
            line = DashedLine([x, cy + width_at(mm / 35) / 2 + 0.05, 0], [x, cy + 1.5, 0], color=color, stroke_width=3, dash_length=0.12)
            dot = Dot([x, cy, 0], radius=0.11, color=color)
            lbl = M(label, 26, color, weight=BOLD).move_to([x, cy + 1.8, 0])
            tick = Line([x, ry - 0.12, 0], [x, ry + 0.12, 0], color=color, stroke_width=4)
            tl = M(f"{mm:.1f}", 22, color).move_to([x, ry - 0.42, 0])
            return line, dot, lbl, tick, tl

        # 1,000 Hz
        c1a = card("x = 0.400:  0.400 × 35 mm = 14.0 mm from the apex", "", PURPLE)
        c1a = VGroup(M("x = 0.400:  0.400 × 35 mm = 14.0 mm from the apex", 24, PURPLE)).move_to([0, card_y + 0.3, 0])
        c1b = M("35 − 14.0 = 21.0 mm from the base", 24, PURPLE).move_to([0, card_y - 0.25, 0])
        m1 = marker(21.0, PURPLE, "1,000 Hz", 0)
        self.at("A tone of 1000")
        self.play(FadeIn(m1[2], shift=DOWN * 0.1), run_time=0.5)
        self.at("14 millimeters")
        self.play(FadeIn(c1a, shift=UP * 0.1), run_time=0.7)
        self.at("21 millimeters")
        self.play(FadeIn(c1b, shift=UP * 0.1), Create(m1[0]), FadeIn(m1[1]), FadeIn(m1[3]), FadeIn(m1[4]), run_time=0.8)

        # 4,000 Hz: clear the first card in the same beat as the new tone
        c2a = M("x = 0.666:  0.666 × 35 mm = 23.3 mm from the apex", 24, ORANGE).move_to([0, card_y + 0.3, 0])
        c2b = M("35 − 23.3 = 11.7 mm from the base", 24, ORANGE).move_to([0, card_y - 0.25, 0])
        m2 = marker(11.7, ORANGE, "4,000 Hz", 0)
        self.at("A tone of 4000")
        self.play(FadeOut(c1a), FadeOut(c1b), FadeIn(m2[2], shift=DOWN * 0.1), run_time=0.5)
        self.at("11 7 millimeters")
        self.play(FadeIn(c2a, shift=UP * 0.1), FadeIn(c2b, shift=UP * 0.1), Create(m2[0]), FadeIn(m2[1]), FadeIn(m2[3]), FadeIn(m2[4]), run_time=0.9)
        self.at("nearer than the lower tone")
        self.play(Indicate(m2[1], color=ORANGE, scale_factor=1.8), run_time=0.7)

        # two octaves, 9.3 mm apart
        self.at("two octaves apart")
        self.play(FadeOut(c2a), FadeOut(c2b), run_time=0.4)
        br = BraceBetweenPoints([mm2x(21.0), ry - 1.1, 0], [mm2x(11.7), ry - 1.1, 0], color=TEXT)
        brl = M("9.3 mm", 28, TEXT, weight=BOLD).next_to(br, DOWN, buff=0.12)
        oct_ = T("two octaves apart", 26, GREY).next_to(brl, RIGHT, buff=0.3)
        self.play(GrowFromCenter(br), FadeIn(brl), FadeIn(oct_), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def peak_curve(x, xp, h, wl, wr):
    """sketched size of motion along the cochlea: rises slowly to a peak at xp, falls quickly."""
    s = np.where(x < xp, (x - xp) / wl, (x - xp) / wr)
    return h * np.exp(-s ** 2)


class S05Amplifier(SpokenScene):
    """von Bekesy's broad peak -> outer hair cells push in step -> a taller, sharper peak."""

    def construct(self):
        y0 = 0.7
        xp0 = mm2x(21.0)
        axis = Line([X0, y0, 0], [X1, y0, 0], color=GREY, stroke_width=3)
        b_lbl = T("base", 26, GREY).move_to([X0 + 0.3, y0 - 0.35, 0])
        a_lbl = T("apex", 26, GREY).move_to([X1 - 0.3, y0 - 0.35, 0])
        ylab = T("size of the motion (relative units, in this sketch)", 22, GREY).move_to([0.5, 3.4, 0])

        def curve(h, wl, wr, color, dashed=False, sw=6):
            xs = np.linspace(X0, X1, 300)
            ys = y0 + peak_curve(xs, xp0, h, wl, wr)
            m = VMobject().set_points_as_corners([[a, b, 0] for a, b in zip(xs, ys)]).set_stroke(color, sw).set_fill(opacity=0)
            return DashedVMobject(m, num_dashes=90) if dashed else m

        passive = curve(1.2, 3.0, 1.3, GREY)
        active = curve(2.2, 1.0, 0.5, GREEN)
        ghost = curve(1.2, 3.0, 1.3, GREY, dashed=True, sw=4)

        self.at("measured these waves")
        self.play(Create(axis), FadeIn(b_lbl), FadeIn(a_lbl), FadeIn(ylab), run_time=0.4)
        self.play(Create(passive), run_time=0.9)
        vb = T("von Békésy's peak", 28, TEXT).move_to([X0 + 2.5, y0 + 1.45, 0])
        self.at("many of them")
        self.play(FadeIn(vb), run_time=0.4)

        wid = DoubleArrow([xp0 - 2.6, y0 + 0.62, 0], [xp0 + 1.3, y0 + 0.62, 0], buff=0, color=YELLOW, stroke_width=4, tip_length=0.16)
        wl = T("far broader", 26, YELLOW).move_to([xp0 - 0.65, y0 + 0.28, 0])
        self.at("far broader")
        self.play(GrowFromCenter(wid), FadeIn(wl), run_time=0.7)

        # the amplifier: outer hair cells standing on the membrane
        my = -2.35
        mem = RoundedRectangle(corner_radius=0.1, width=6.0, height=0.24, stroke_color=BLUE, stroke_width=3,
                               fill_color=BLUE, fill_opacity=0.35).move_to([xp0 + 0.2, my, 0])
        mem_l = T("membrane", 24, BLUE).next_to(mem, LEFT, buff=0.2)
        self.at("The difference is an amplifier")
        self.play(FadeOut(wid), FadeOut(wl), FadeIn(mem), FadeIn(mem_l), run_time=0.8)

        t = ValueTracker(0.0)
        t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t)
        on = ValueTracker(0.0)       # 0 = cells still, 1 = changing length
        xs_c = [xp0 + d for d in (-2.2, -1.1, 0.0, 1.1, 2.2)]
        top = my + 0.12

        def cell_at(x):
            def f():
                h = 0.95 + on.get_value() * 0.2 * np.sin(2 * np.pi * 1.4 * t.get_value())
                c = haircell(h=h, w=0.5, sw=4)
                c.move_to([x, top, 0], aligned_edge=DOWN)
                return c
            return f

        def push_at(x):
            def f():
                a = on.get_value() * (0.5 + 0.5 * np.sin(2 * np.pi * 1.4 * t.get_value()))
                ln = 0.15 + 0.45 * a
                return Arrow([x, top + 0.15 + ln, 0], [x, top + 0.03, 0], buff=0, color=GREEN, stroke_width=6,
                             tip_length=0.14, max_tip_length_to_length_ratio=0.9).set_opacity(min(1.0, on.get_value() * (0.25 + a)))
            return f

        cells = [always_redraw(cell_at(x)) for x in xs_c]
        pushes = [always_redraw(push_at(x + 0.55)) for x in xs_c[:-1]]
        oh_lbl = T("outer hair cells", 28, TEAL).move_to([xp0 - 4.5, my + 0.9, 0])
        oh_sch = T("schematic", 24, GREY).next_to(oh_lbl, DOWN, buff=0.1)
        self.play(*[FadeIn(c) for c in cells], FadeIn(oh_lbl), FadeIn(oh_sch), run_time=0.7)
        self.add(*pushes)

        self.at("change length when their voltage")
        vl = T("voltage changes, length changes", 26, TEAL).move_to([xp0 + 0.2, -3.3, 0])
        self.play(on.animate.set_value(1.0), FadeIn(vl), run_time=0.8)
        self.at("push on the membrane in step")
        push_l = T("pushing on the membrane in step", 26, GREEN).move_to([xp0 + 0.2, -3.3, 0])
        self.play(ReplacementTransform(vl, push_l), Indicate(mem, color=GREEN, scale_factor=1.0), run_time=0.8)

        # more energy at the peak: the broad peak becomes a taller, sharper one
        self.at("adds energy at the peak")
        self.add(ghost)
        ll = T("with the amplifier", 28, GREEN, weight=BOLD).move_to([xp0 + 3.0, y0 + 2.0, 0])
        self.play(Transform(passive, active), vb.animate.set_color(GREY), FadeIn(ll), run_time=1.4, rate_func=smooth)
        shp = T("sharper tuning", 26, GREEN).move_to([xp0 + 3.0, y0 + 1.4, 0])
        self.at("sharpens tuning")
        self.play(FadeIn(shp, shift=LEFT * 0.1), run_time=0.5)
        sens = T("higher sensitivity", 26, GREEN).move_to([xp0 + 3.0, y0 + 0.8, 0])
        self.at("raises sensitivity")
        self.play(FadeIn(sens, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Map(SpokenScene):
    """tonotopy is kept at every relay up to cortex: a column of relays, each with the same high-to-low bar."""

    def construct(self):
        names = ["auditory nerve", "cochlear nucleus", "superior olivary complex", "inferior colliculus",
                 "medial geniculate nucleus", "auditory cortex"]
        ys = [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
        bx0, bx1 = 0.8, 5.0

        def bar(y):
            n = 20
            return VGroup(*[Rectangle(width=(bx1 - bx0) / n, height=0.46, stroke_width=0,
                                      fill_color=interpolate_color(ManimColor(ORANGE), ManimColor(PURPLE), (i + .5) / n),
                                      fill_opacity=0.85) for i in range(n)]).arrange(RIGHT, buff=0).move_to([(bx0 + bx1) / 2, y, 0])

        def relay(nm, y):
            r = RoundedRectangle(corner_radius=0.14, width=4.7, height=0.66, stroke_color=BLUE, stroke_width=2.5,
                                 fill_color=BLUE, fill_opacity=0.16).move_to([-3.0, y, 0])
            return VGroup(r, T(nm, 26, BLUE).move_to(r))

        boxes = [relay(nm, y) for nm, y in zip(names, ys)]
        bars = [bar(y) for y in ys]
        hi = T("high", 24, ORANGE).next_to(bars[0], DOWN, buff=0.08).align_to(bars[0], LEFT)
        lo = T("low", 24, PURPLE).next_to(bars[0], DOWN, buff=0.08).align_to(bars[0], RIGHT)
        head = T("tonotopy", 40, TEAL, weight=BOLD).move_to([2.9, 3.3, 0])
        side = T("one side shown", 22, GREY).move_to([-3.0, -3.3, 0])

        self.at("This map of frequency")
        self.play(FadeIn(bars[0]), FadeIn(hi), FadeIn(lo), run_time=0.8)
        self.at("called tonotopy")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)

        self.at("The auditory nerve")
        self.play(FadeIn(boxes[0]), FadeIn(side), run_time=0.6)
        arrows = []
        for i in range(1, 6):
            arrows.append(Arrow([-3.0, ys[i - 1] + 0.35, 0], [-3.0, ys[i] - 0.35, 0], buff=0.0, color=GREY, stroke_width=5, tip_length=0.14,
                                max_tip_length_to_length_ratio=0.6))

        def reveal(i):
            self.play(GrowArrow(arrows[i - 1]), FadeIn(boxes[i], shift=UP * 0.15), FadeIn(bars[i]), run_time=0.7)

        self.at("cochlear nucleus")
        reveal(1)
        self.at("superior olivary complex")
        reveal(2)
        self.at("inferior colliculus")
        reveal(3)
        self.at("medial geniculate nucleus")
        reveal(4)
        self.at("auditory cortex")
        reveal(5)

        self.at("Keep this rule")
        keep = T("the map is kept at every relay", 24, TEAL).move_to([2.9, -3.45, 0])
        frame_r = Rectangle(width=bx1 - bx0 + 0.5, height=ys[-1] - ys[0] + 0.65, stroke_color=TEAL, stroke_width=3).move_to([(bx0 + bx1) / 2, (ys[0] + ys[-1]) / 2, 0])
        self.play(Create(frame_r), FadeIn(keep), run_time=1.0)
        self.finish()


def bchip(text, color=BLUE, size=26):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


class S07End(EndCard):
    LINE = "Frequency becomes position, and the map is kept up to cortex."
